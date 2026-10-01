"""generation.py - coherent report generations and verified export (OPUS, 2026-09-29).

Workflow migration M1 1e (FF12-WORKFLOW-MIGRATION-20260928-01 section 9; acceptance matrix A05-A09). A library for a
report generator (the progress reporter first, under DATA's R3 task) and a CLI for readers and export.

THE MODEL. A report is a GENERATION: one directory holding every output of one build, the exact bytes of the inputs it
consumed, and MANIFEST.json binding them. Readers only see a generation through CURRENT, a small pointer file that names
the generation and the sha256 of its manifest. So:
  - a generation is built in `.<id>.partial/`; nothing reads that name;
  - commit() re-fingerprints the declared inputs (a source edited mid-build refuses the commit), checks every required
    output exists, hashes everything, writes the manifest, renames `.<id>.partial` -> `<id>`, and only then replaces
    CURRENT (write-temp + os.replace). A crash before the replace leaves the previous generation current;
  - a failed commit writes FAILURE.json (separate from success) and never touches CURRENT; history.jsonl gets a row
    only for a committed generation;
  - open_current() verifies the pointer's manifest hash, the membership (no missing and no extra files) and every
    file's hash; a tampered output, manifest or membership is refused, never shown as current;
  - drift() compares the generation's inputs with the live sources: moved sources make the generation STALE (still
    complete and valid as of its inputs), which a reader must show, not hide.

INPUT STATES (A06). Each declared input is `present` (sha256 + size of its exact bytes; no text normalisation), `empty`
(zero bytes), `missing` or `unsupported`. A `required` input (the default) must be present, or empty only when its spec
says `allow_empty: True` (a legitimately empty source, by the generator's explicit schema); anything else refuses the
generation at begin(), so an unavailable, zero-byte or unreadable source can never become a zero CURRENT.
VOLATILE INPUTS: `volatile: True` declares an input the generator reads ONLY from its snapshot (e.g. a board written every
few seconds). A change after the snapshot is then drift - the generation is still coherent as of the bytes it captured and
reads STALE - rather than a refused commit. Every other input keeps the strict rule: moved during the build = refused.
EXTERNAL INPUTS: `snapshot: False` declares a large or non-redistributable input (the certified game EXE) that is hashed
and strict but not copied: the manifest marks it `external`, the generator reads it at its path, the commit still refuses
it if it moved, and an export carries only its hash - never its bytes. Schema validity is the generator's job; it passes its
verdict per input (validated=...) and a failed validation refuses the commit.

EXPORT (A09). export() opens CURRENT verified, pins that generation id, writes a ZIP of its manifest, outputs and input
snapshot to a temp name, re-opens the ZIP and checks every member against the manifest, then renames it and writes a
sidecar `<zip>.sha256`. A generation committed during the export does not change what is exported. verify_zip() labels
any ZIP: VERIFIED (manifest present, members exactly the manifest's, hashes match) or UNVERIFIED with the reason - a
hand-made or mixed ZIP is detected and labelled, not certified.

RESTORE (ASTRA-REQ-OPUS-A23-WINDOWS-SNAPSHOT-RESTORE, 2026-09-29). An input's NAME is a logical key (`pkg:PKG-x.md`);
its snapshot's FILE name is snapshot_name(name), which percent-escapes the characters a Windows or POSIX file name cannot
hold ('%' itself included, so the mapping is one-to-one). A name with none of them is its own file name, so every
generation written before this reads unchanged; a generation written before it with an escaped character in a name keeps
its raw file name and is still read (legacy fallback). A ZIP export carries LOGICAL member names (`inputs/<name>`), which
is the contract verify_zip certifies - so a ZIP is not a directory image, and a generic extractor that rewrites names
(Python's ZipFile.extractall turns ':' into '_' on Windows) does not restore it. The supported method is
restore_zip(zip, root): verify the ZIP, refuse a non-empty target, write every member through snapshot_name, refuse two
members that land on one file of a case-insensitive file system, then re-open the result through the ordinary reader
and refuse unless it is clean.

CLI:  python generation.py status <root> | verify <root> | export <root> <zip> | verify-zip <zip> | restore <zip> <root>
      | --self-test
"""
import datetime, hashlib, json, os, shutil, sys, uuid, zipfile

MANIFEST, CURRENT, FAILURE, HISTORY, FAILURES = "MANIFEST.json", "CURRENT", "FAILURE.json", "history.jsonl", "failures.jsonl"
# THE IDENTITY CONTRACT (2026-09-29 incident, see _index/candidates/dashboard-incident-0929-exe/): the manifest format
# names the semantics a reader must understand. v2 = v1 plus the per-input flags `volatile` and `external` and the
# writer's `verifier` (this module's sha256). A reader that meets a format it does not know reports UNSUPPORTED - it
# never guesses (a v1-era reader misread a v2 external input as a corrupt snapshot and invalidated a valid generation).
FORMAT = "ff12-generation-2"
INPUT_STATES = ("present", "empty", "missing", "unsupported")   # exactly what input_state() emits
READABLE = ("ff12-generation-1", "ff12-generation-2")


_UNSAFE = set('<>:"/\\|?*%')


def snapshot_name(name):
    """The portable file name of an input's snapshot: percent-escape what a Windows or POSIX file name cannot hold, and
    '%' itself, so distinct logical names never share a file. A plain name is returned unchanged."""
    return "".join("%%%02X" % ord(c) if (c in _UNSAFE or ord(c) < 32) else c for c in name)


def input_file(gen_dir, name):
    """The snapshot file of input `name` in a generation directory: its portable name, or - for a generation written
    before snapshot_name existed - the raw logical name when only that exists."""
    p = os.path.join(gen_dir, "inputs", snapshot_name(name))
    if not os.path.isfile(p) and snapshot_name(name) != name:
        raw = os.path.join(gen_dir, "inputs", name)
        if os.path.isfile(raw):
            return raw
    return p


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def _module_sha():
    try:
        return sha256_file(os.path.abspath(__file__))
    except OSError:
        return None


VERIFIER_SHA = _module_sha()          # the code this process loaded; compare with reader_stale()


def reader_stale():
    """True when this module's file on disk differs from the code this process loaded (a long-running reader that
    predates a change must be restarted, not trusted)."""
    return _module_sha() != VERIFIER_SHA


def _now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _atomic_write(path, data):
    tmp = "%s.tmp-%s" % (path, uuid.uuid4().hex[:8])
    with open(tmp, "wb") as f:
        f.write(data); f.flush(); os.fsync(f.fileno())
    os.replace(tmp, path)


def input_state(path):
    if not os.path.exists(path):
        return {"state": "missing"}
    if not os.path.isfile(path):
        return {"state": "unsupported", "reason": "not a regular file"}
    size = os.path.getsize(path)
    return {"state": "empty" if size == 0 else "present", "size": size, "sha256": sha256_file(path)}


class GenerationError(Exception):
    pass


class Build:
    """One generation under construction. Use Store.begin(); write outputs into .dir; then Store.commit(build)."""

    def __init__(self, store, gen_id, inputs, generator):
        self.store, self.id, self.inputs, self.generator = store, gen_id, inputs, generator
        self.dir = os.path.join(store.root, ".%s.partial" % gen_id)
        self.outputs_dir = os.path.join(self.dir, "outputs")
        os.makedirs(self.outputs_dir)
        self.captured = {n: dict(spec, **input_state(spec["path"])) for n, spec in inputs.items()}
        def usable(n, c):
            return c["state"] == "present" or (c["state"] == "empty" and self.inputs[n].get("allow_empty", False))
        bad = [n for n, c in self.captured.items() if self.inputs[n].get("required", True) and not usable(n, c)]
        if bad:
            self.store._fail(self, "required input not usable at begin: %s" %
                             ", ".join("%s=%s" % (n, self.captured[n]["state"]) for n in bad))
        # snapshot the exact bytes consumed, so an export never reads live sources
        os.makedirs(os.path.join(self.dir, "inputs"))
        for n, c in self.captured.items():
            if c["state"] in ("present", "empty") and self.inputs[n].get("snapshot", True):
                shutil.copyfile(c["path"], self.input_path(n))
                if sha256_file(self.input_path(n)) != c["sha256"]:
                    self.store._fail(self, "input %s changed while being snapshotted" % n)

    def input_path(self, name):
        """Where input `name`'s snapshot lives in this build (its portable file name)."""
        return os.path.join(self.dir, "inputs", snapshot_name(name))

    def output_path(self, name):
        if os.sep in name or "/" in name or name.startswith("."):
            raise GenerationError("output names are flat file names: %r" % name)
        return os.path.join(self.outputs_dir, name)


class Store:
    def __init__(self, root):
        self.root = root
        os.makedirs(root, exist_ok=True)

    # ---------------------------------------------------------------- writing
    def begin(self, inputs, generator=None):
        """inputs: {name: {"path": p, "required": bool (default True)}}; generator: {"name":..., "sha256":...}."""
        gen_id = "g%s-%s" % (datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ"), uuid.uuid4().hex[:6])
        return Build(self, gen_id, inputs, generator or {})

    def _record_failure(self, gen_id, reason):
        cur = self.current_id()
        man = self.open_generation(cur)[0] if cur else None
        rec = {"generation": gen_id, "failed_at": _now(), "reason": reason, "current_unchanged": cur,
               "current_committed_at": (man or {}).get("committed_at")}
        _atomic_write(os.path.join(self.root, FAILURE), json.dumps(rec, indent=1).encode())
        with open(os.path.join(self.root, FAILURES), "a", encoding="utf-8") as h:
            h.write(json.dumps(rec) + "\n")

    def _fail(self, build, reason):
        self._record_failure(build.id, reason)
        shutil.rmtree(build.dir, ignore_errors=True)
        raise GenerationError(reason)

    def commit(self, build, required_outputs, validated=None):
        """validated: {input_name: None | reason}; any reason refuses the commit."""
        for n, why in (validated or {}).items():
            if why:
                self._fail(build, "input %s failed validation: %s" % (n, why))
        now = {n: input_state(c["path"]) for n, c in build.captured.items()}
        moved = [n for n, c in build.captured.items() if not build.inputs[n].get("volatile")
                 and (now[n].get("sha256") != c.get("sha256") or now[n]["state"] != c["state"])]
        if moved:
            self._fail(build, "inputs moved during the build: %s" % ", ".join(sorted(moved)))
        have = sorted(os.listdir(build.outputs_dir))
        missing = [o for o in required_outputs if o not in have]
        if missing:
            self._fail(build, "required outputs missing: %s" % ", ".join(missing))
        outs = {o: {"sha256": sha256_file(os.path.join(build.outputs_dir, o)), "size": os.path.getsize(os.path.join(build.outputs_dir, o))} for o in have}
        ins = {n: dict({k: c[k] for k in ("path", "state", "size", "sha256") if k in c}, **({"volatile": True} if build.inputs[n].get("volatile") else {}),
                       **({"external": True} if not build.inputs[n].get("snapshot", True) else {}))
               for n, c in build.captured.items()}
        man = {"format": FORMAT, "generation": build.id, "committed_at": _now(), "parent": self.current_id(),
               "generator": build.generator, "verifier": VERIFIER_SHA, "inputs": ins, "outputs": outs}
        mbytes = json.dumps(man, indent=1, sort_keys=True).encode()
        _atomic_write(os.path.join(build.dir, MANIFEST), mbytes)
        final = os.path.join(self.root, build.id)
        os.replace(build.dir, final)
        pointer = {"generation": build.id, "manifest_sha256": hashlib.sha256(mbytes).hexdigest()}
        # verify the complete on-disk generation with the SAME function readers (the HTTP server) use, before it can
        # become CURRENT; a rejected candidate is kept aside for diagnosis and never replaces the known-good generation
        _, _, probs = self.open_generation(build.id, pointer["manifest_sha256"])
        if probs:
            os.replace(final, final + ".rejected")
            reason = "candidate failed the reader's verification: %s" % "; ".join(probs)
            self._record_failure(build.id, reason)
            raise GenerationError(reason)
        _atomic_write(os.path.join(self.root, CURRENT), json.dumps(pointer).encode())
        with open(os.path.join(self.root, HISTORY), "a", encoding="utf-8") as h:
            h.write(json.dumps({"generation": build.id, "committed_at": man["committed_at"], "manifest_sha256": pointer["manifest_sha256"]}) + "\n")
        return build.id

    # ---------------------------------------------------------------- reading
    def current_id(self):
        p = os.path.join(self.root, CURRENT)
        try:
            return json.load(open(p, encoding="utf-8"))["generation"]
        except (OSError, ValueError, KeyError):
            return None

    def open_current(self):
        """(manifest, generation_dir, problems). problems == [] means complete and untampered."""
        p = os.path.join(self.root, CURRENT)
        if not os.path.exists(p):
            return None, None, ["no CURRENT generation"]
        try:
            ptr = json.load(open(p, encoding="utf-8"))
        except ValueError as e:
            return None, None, ["CURRENT unreadable: %s" % e]
        return self.open_generation(ptr.get("generation"), ptr.get("manifest_sha256"))

    def open_generation(self, gen_id, manifest_sha=None):
        d = os.path.join(self.root, gen_id or "")
        mp = os.path.join(d, MANIFEST)
        if not gen_id or not os.path.isfile(mp):
            return None, None, ["generation %s has no manifest" % gen_id]
        mbytes = open(mp, "rb").read()
        probs = []
        if manifest_sha is not None and hashlib.sha256(mbytes).hexdigest() != manifest_sha:
            probs.append("manifest does not match the CURRENT pointer (tampered or replaced)")
        man, why = parse_manifest(mbytes)
        if why:
            return (man if isinstance(man, dict) else None), d, probs + [why]
        want = set(man["outputs"])
        have = set(os.listdir(os.path.join(d, "outputs"))) if os.path.isdir(os.path.join(d, "outputs")) else set()
        if want - have: probs.append("outputs missing: %s" % sorted(want - have))
        if have - want: probs.append("outputs not in the manifest: %s" % sorted(have - want))
        for o in sorted(want & have):
            if sha256_file(os.path.join(d, "outputs", o)) != man["outputs"][o]["sha256"]:
                probs.append("output %s does not match the manifest" % o)
        for n, c in man["inputs"].items():
            if c["state"] in ("present", "empty") and not c.get("external"):
                ip = input_file(d, n)
                if not os.path.isfile(ip) or sha256_file(ip) != c["sha256"]:
                    probs.append("input snapshot %s does not match the manifest" % n)
        return man, d, probs

    def drift(self, man):
        """{input: live state} for inputs whose live source no longer matches the generation (STALE, not invalid)."""
        out = {}
        for n, c in man["inputs"].items():
            live = input_state(c["path"])
            if live["state"] != c["state"] or live.get("sha256") != c.get("sha256"):
                out[n] = live["state"] if live["state"] != "present" else "changed"
        return out

    # ---------------------------------------------------------------- export
    def export(self, zip_path):
        man, d, probs = self.open_current()
        if probs:
            raise GenerationError("current generation not exportable: %s" % "; ".join(probs))
        gen = man["generation"]
        tmp = "%s.tmp-%s" % (zip_path, uuid.uuid4().hex[:8])
        members = {MANIFEST: os.path.join(d, MANIFEST)}
        members.update({"outputs/" + o: os.path.join(d, "outputs", o) for o in man["outputs"]})
        members.update({"inputs/" + n: input_file(d, n) for n, c in man["inputs"].items() if c["state"] in ("present", "empty") and not c.get("external")})
        with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as z:
            for arc, src in sorted(members.items()):
                z.write(src, arc)
        label, why = verify_zip(tmp)
        if label != "VERIFIED" or why.get("generation") != gen:
            os.remove(tmp)
            raise GenerationError("export did not verify: %s" % why)
        os.replace(tmp, zip_path)
        _atomic_write(zip_path + ".sha256", ("%s  %s\n" % (sha256_file(zip_path), os.path.basename(zip_path))).encode())
        return gen


def parse_manifest(mbytes):
    """(manifest, None) or (parsed-or-None, why). Both readers - the store folder and the exported ZIP - admit a manifest
    only through this: JSON, an object, a format this reader knows, a generation id, and outputs/inputs whose entries
    carry the hashes the membership check needs. (ASTRA's certification REJECT, 97c4c1b65: the ZIP path parsed with a
    bare json.loads, so malformed JSON raised instead of answering UNVERIFIED, and it never checked the format.)"""
    try:
        man = json.loads(mbytes)
    except (ValueError, UnicodeDecodeError) as e:
        return None, "manifest is not JSON: %s" % e
    if not isinstance(man, dict):
        return man, "manifest is %s, not an object" % type(man).__name__
    if man.get("format") not in READABLE:
        return man, ("UNSUPPORTED: manifest format %r is not one this reader knows %s - the reader is older than the writer; "
                     "restart it rather than trusting its verdict" % (man.get("format"), list(READABLE)))
    if not isinstance(man.get("generation"), str) or not man["generation"]:
        return man, "manifest names no generation id"
    for k in ("outputs", "inputs"):
        if not isinstance(man.get(k), dict):
            return man, "manifest %s is not an object" % k
    for o, v in man["outputs"].items():
        if not isinstance(v, dict) or not isinstance(v.get("sha256"), str):
            return man, "output %r carries no sha256" % o
    for n, c in man["inputs"].items():
        if not isinstance(c, dict) or not isinstance(c.get("state"), str):
            return man, "input %r carries no state" % n
        if c["state"] not in INPUT_STATES:
            # ASTRA's second certification REJECT (7d9b5ec17): an unknown state word skipped both membership paths, so an
            # archive could drop a captured input's snapshot by relabelling it. Only the states input_state() emits exist.
            return man, "input %r has unknown state %r (known: %s)" % (n, c["state"], ", ".join(INPUT_STATES))
        if c["state"] in ("present", "empty") and not c.get("external") and not isinstance(c.get("sha256"), str):
            return man, "input %r carries no sha256" % n
    return man, None


def verify_zip(zip_path):
    """('VERIFIED', info) or ('UNVERIFIED', info). A ZIP not produced from one manifest is labelled, never certified.
    Membership is counted over the ZIP's physical entries, not a set of names: two entries with one name (a later one
    shadowing an earlier one on extraction) are refused, not collapsed into one certified member."""
    try:
        z = zipfile.ZipFile(zip_path)
    except (OSError, zipfile.BadZipFile) as e:
        return "UNVERIFIED", {"reason": "not a readable zip: %s" % e}
    with z:
        entries = [i.filename for i in z.infolist() if not i.filename.endswith("/")]
        seen, dup = set(), set()
        for n in entries:
            (dup if n in seen else seen).add(n)
        if dup:
            return "UNVERIFIED", {"reason": "duplicate member names: one name, several physical entries", "duplicates": sorted(dup)[:5],
                                  "entries": len(entries)}
        names = seen
        if MANIFEST not in names:
            return "UNVERIFIED", {"reason": "no MANIFEST.json - not an exported generation (hand-made or mixed)", "members": len(names)}
        man, why = parse_manifest(z.read(MANIFEST))
        if why:
            return "UNVERIFIED", {"reason": why, "generation": man.get("generation") if isinstance(man, dict) else None}
        want = {"outputs/" + o: v["sha256"] for o, v in man["outputs"].items()}
        want.update({"inputs/" + n: c["sha256"] for n, c in man["inputs"].items() if c["state"] in ("present", "empty") and not c.get("external")})
        extra, missing = sorted(names - set(want) - {MANIFEST}), sorted(set(want) - names)
        bad = [n for n in sorted(set(want) & names) if hashlib.sha256(z.read(n)).hexdigest() != want[n]]
    if extra or missing or bad:
        return "UNVERIFIED", {"reason": "members do not match the manifest", "generation": man.get("generation"),
                              "extra": extra[:5], "missing": missing[:5], "hash_mismatch": bad[:5]}
    return "VERIFIED", {"generation": man["generation"], "members": len(want) + 1}


def restore_zip(zip_path, root):
    """Restore a VERIFIED export into a fresh store at `root` (the supported portable method; see RESTORE above). Returns
    the generation id; raises GenerationError, leaving no CURRENT behind, on an unverified ZIP, a non-empty target, two
    members that would share one file on a case-insensitive file system, or a result the ordinary reader does not open clean."""
    label, info = verify_zip(zip_path)
    if label != "VERIFIED":
        raise GenerationError("refusing to restore an UNVERIFIED zip: %s" % info.get("reason"))
    if os.path.exists(root) and os.listdir(root):
        raise GenerationError("refusing to restore into a non-empty directory: %s" % root)
    gen = info["generation"]
    with zipfile.ZipFile(zip_path) as z:
        man, _ = parse_manifest(z.read(MANIFEST))
        plan = {os.path.join(gen, MANIFEST): MANIFEST}
        for o in man["outputs"]:
            if os.sep in o or "/" in o or o.startswith("."):
                raise GenerationError("output name is not a flat file name: %r" % o)
            plan[os.path.join(gen, "outputs", o)] = "outputs/" + o
        for n, c in man["inputs"].items():
            if c["state"] in ("present", "empty") and not c.get("external"):
                plan[os.path.join(gen, "inputs", snapshot_name(n))] = "inputs/" + n   # snapshot_name is one-to-one
        folded = {}
        for dst in plan:                  # a case-insensitive file system folds names a case-sensitive archive keeps apart
            k = os.path.normcase(dst).lower()
            if k in folded:
                raise GenerationError("two members restore to one file on a case-insensitive system: %r and %r" % (plan[folded[k]], plan[dst]))
            folded[k] = dst
        os.makedirs(os.path.join(root, gen, "outputs"))
        os.makedirs(os.path.join(root, gen, "inputs"))
        for dst, arc in plan.items():
            with open(os.path.join(root, dst), "wb") as f:
                f.write(z.read(arc))
    mbytes = open(os.path.join(root, gen, MANIFEST), "rb").read()
    st = Store(root)
    _, _, probs = st.open_generation(gen, hashlib.sha256(mbytes).hexdigest())
    if probs:
        raise GenerationError("restored generation does not open clean: %s" % "; ".join(probs))
    _atomic_write(os.path.join(root, CURRENT), json.dumps({"generation": gen, "manifest_sha256": hashlib.sha256(mbytes).hexdigest()}).encode())
    return gen


def main(argv):
    if "--self-test" in argv:
        import subprocess
        return subprocess.call([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_generation.py")])
    if len(argv) < 3:
        print(__doc__.split("CLI:")[1].strip()); return 2
    cmd = argv[1]
    if cmd == "verify-zip":
        label, info = verify_zip(argv[2]); print(label, json.dumps(info)); return 0 if label == "VERIFIED" else 1
    if cmd == "restore" and len(argv) >= 4:
        try:
            print("RESTORED", restore_zip(argv[2], argv[3]), "->", argv[3]); return 0
        except GenerationError as e:
            print("REFUSED", e); return 1
    st = Store(argv[2])
    if cmd in ("status", "verify"):
        man, d, probs = st.open_current()
        if probs:
            print("INVALID", "; ".join(probs)); return 1
        drift = st.drift(man)
        print("%s %s committed %s; %d outputs; %s" % ("STALE" if drift else "CURRENT", man["generation"], man["committed_at"], len(man["outputs"]),
                                                   ("sources moved since: %s" % drift) if drift else "sources unchanged"))
        fp = os.path.join(st.root, FAILURE)
        if os.path.exists(fp):
            print("last failure:", open(fp, encoding="utf-8").read().strip().replace("\n", " "))
        return 0
    if cmd == "export" and len(argv) >= 4:
        print("EXPORTED", st.export(argv[3]), "->", argv[3]); return 0
    print("unknown command"); return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
