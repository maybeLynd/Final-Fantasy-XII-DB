"""test_generation.py - generation.py's fault cases for acceptance-matrix A05-A09 (OPUS, 2026-09-29). Disposable
fixtures only; the CLI is exercised as a subprocess (the reader/export entry point).

  G1  valid build commits; open_current is clean; CURRENT names it; history has one row
  G2  (A07) an output edited after commit -> refused
  G3  (A07) the manifest edited -> the pointer's manifest hash refuses it
  G4  (A07) an extra file dropped into outputs -> membership refused
  G5  (A08) a source edited between begin and commit -> commit refused, previous CURRENT survives, FAILURE.json written,
      history unchanged, no partial left
  G6  (A08) the second required output never written -> refused the same way
  G7  (A08) a crash between the output writes and commit (an abandoned .partial) -> CURRENT still the previous one and
      the partial is not readable as current
  G8  (A06) a required input missing / zero-byte / present: missing and zero-byte refuse; zero-byte with allow_empty is
      accepted; an optional missing input is recorded as missing, not zero
  G9  (A05) a source changed after commit -> the generation stays valid but reads STALE with that input named; an
      unchanged source reads CURRENT (the no-change skip)
  G11 a VOLATILE input (declared snapshot-only) edited mid-build -> the commit succeeds from the snapshot and the change
      reads as drift; the strict rule (G5) still applies to every other input
  G12 an EXTERNAL input (snapshot: False, e.g. the game EXE) is hashed and strict but never copied or exported
  G10 (A05) byte-exact: CRLF vs LF of the same text are different fingerprints (no silent normalisation)
  E1  (A09) export -> the ZIP verifies (members exactly the manifest, hashes match), sidecar sha256 matches the file
  E2  (A09) a new generation committed during export does not change the exported generation (pinned id)
  E3  (A09) a hand-made ZIP (outputs of two generations, no manifest) -> UNVERIFIED; a ZIP with one member tampered -> UNVERIFIED
  E4  a ZIP with two physical entries under one name -> UNVERIFIED (duplicates), never a collapsed member count
  E5  a ZIP whose manifest format is unknown -> UNVERIFIED (UNSUPPORTED), as the folder reader already refuses
  E6  a ZIP whose manifest is not JSON, or has the wrong shape -> UNVERIFIED with a reason; the CLI prints UNVERIFIED
      and exits 1 without a traceback
  E7  a store generation whose manifest is not JSON -> open_generation reports it, never raises
  E8  an input relabelled with an unknown state and its snapshot removed -> UNVERIFIED (unknown state), library and CLI
      (ASTRA's second certification REJECT 7d9b5ec17, AUTO-REPAIR-OPUS-REQ-ASTRA-VERIFY-GENERATION-CERT-R2)
      (E4-E7: ASTRA's certification REJECT 97c4c1b65, ASTRA-RETURN-OPUS-GENERATION-ARCHIVE-CERTIFICATION)
  C1  CLI: `status` prints CURRENT / STALE, `verify-zip` exits 0 on a verified export and 1 on the mixed ZIP
  R1  (ASTRA-REQ-OPUS-A23-WINDOWS-SNAPSHOT-RESTORE) an input named `pkg:PKG-x.md` is snapshotted under its portable file
      name, reads clean, exports under its LOGICAL member name, and restore_zip (library and CLI) rebuilds a store the
      ordinary reader opens clean with that input's bytes; a plain name is its own file name (old generations unchanged)
  R2  the reader still opens a generation written before the escape (raw logical file name) - the legacy fallback
  R3  restore refuses an UNVERIFIED zip, a non-empty target, and a case-only pair of members (one file on a
      case-insensitive system), leaving no CURRENT behind; `a:b` beside `a%3Ab` restores to two distinct files
  R4  the escape is one-to-one over names that differ only by escaped characters or by '%' itself
"""
import json, os, shutil, subprocess, sys, tempfile, zipfile
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import generation as G  # noqa: E402
fails = 0
def check(tag, ok, text=""):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
T = tempfile.mkdtemp(prefix="gen_")
SRC = os.path.join(T, "src"); os.makedirs(SRC)
def wsrc(name, data):
    p = os.path.join(SRC, name); open(p, "wb").write(data); return p
a, b = wsrc("a.md", b"alpha\n"), wsrc("b.tsv", b"x\ty\n")
INPUTS = {"a": {"path": a}, "b": {"path": b}}
st = G.Store(os.path.join(T, "gens"))
def build(outs=("report.md", "snapshot.json"), inputs=INPUTS, mutate=None):
    bd = st.begin(inputs, {"name": "fixture", "sha256": "0"})
    for i, o in enumerate(outs):
        open(bd.output_path(o), "wb").write(("out %s %d\n" % (o, i)).encode())
        if mutate and i == 0: mutate()
    return bd
def raises(fn):
    try: fn(); return None
    except G.GenerationError as e: return str(e)
g1 = st.commit(build(), ["report.md", "snapshot.json"])
man, d, probs = st.open_current()
hist = open(os.path.join(st.root, G.HISTORY)).read().splitlines()
check("G1", not probs and man["generation"] == g1 and st.current_id() == g1 and len(hist) == 1, "committed %s" % g1)
def tamper_and_restore(path, data, expect):
    old = open(path, "rb").read(); open(path, "wb").write(data)
    _, _, p = st.open_current(); open(path, "wb").write(old)
    return any(expect in x for x in p), p
ok, p = tamper_and_restore(os.path.join(d, "outputs", "report.md"), b"edited\n", "does not match the manifest"); check("G2", ok, p)
ok, p = tamper_and_restore(os.path.join(d, G.MANIFEST), open(os.path.join(d, G.MANIFEST), "rb").read().replace(b'"fixture"', b'"fixturX"'), "CURRENT pointer"); check("G3", ok, p)
xp = os.path.join(d, "outputs", "stray.md"); open(xp, "wb").write(b"stray"); _, _, p = st.open_current(); os.remove(xp)
check("G4", any("not in the manifest" in x for x in p), p)
def g5_mutate(): open(a, "wb").write(b"alpha edited mid-build\n")
why = raises(lambda: st.commit(build(mutate=g5_mutate), ["report.md", "snapshot.json"]))
open(a, "wb").write(b"alpha\n")
fp = os.path.join(st.root, G.FAILURE); fail = json.load(open(fp)) if os.path.exists(fp) else {}
parts = [x for x in os.listdir(st.root) if x.endswith(".partial")]
check("G5", why and "inputs moved" in why and st.current_id() == g1 and fail.get("current_unchanged") == g1
      and len(open(os.path.join(st.root, G.HISTORY)).read().splitlines()) == 1 and not parts, why)
why = raises(lambda: st.commit(build(outs=("report.md",)), ["report.md", "snapshot.json"]))
check("G6", why and "required outputs missing: snapshot.json" in why and st.current_id() == g1, why)
bd = build()          # the crash: outputs written, commit never called
_, _, p = st.open_current()
check("G7", st.current_id() == g1 and not p and os.path.isdir(bd.dir) and bd.id not in os.listdir(st.root), "abandoned %s ignored" % os.path.basename(bd.dir))
shutil.rmtree(bd.dir)
z = wsrc("zero.tsv", b"")
w1 = raises(lambda: st.begin({"a": {"path": a}, "m": {"path": os.path.join(SRC, "nope.tsv")}}))
w2 = raises(lambda: st.begin({"a": {"path": a}, "z": {"path": z}}))
bz = st.begin({"a": {"path": a}, "z": {"path": z, "allow_empty": True}, "o": {"path": os.path.join(SRC, "nope2.tsv"), "required": False}})
open(bz.output_path("report.md"), "wb").write(b"r"); gz = st.commit(bz, ["report.md"]); mz, _, pz = st.open_current()
check("G8", w1 and "m=missing" in w1 and w2 and "z=empty" in w2 and not pz and mz["inputs"]["z"]["state"] == "empty"
      and mz["inputs"]["o"]["state"] == "missing" and "sha256" not in mz["inputs"]["o"], "missing: %s | zero: %s" % (w1, w2))
g9 = st.commit(build(), ["report.md", "snapshot.json"]); m9, _, _ = st.open_current()
same = st.drift(m9); open(b, "wb").write(b"x\ty\nz\tw\n"); moved = st.drift(m9); _, _, p9 = st.open_current()
check("G9", same == {} and moved == {"b": "changed"} and not p9, "unchanged -> %s; after an edit -> %s" % (same, moved))
open(b, "wb").write(b"x\ty\n")
vol = wsrc("board.json", b'{"rev": 1}')
def g11_mutate(): open(vol, "wb").write(b'{"rev": 2}')
g11 = st.commit(build(inputs={"a": {"path": a}, "board": {"path": vol, "volatile": True}}, mutate=g11_mutate), ["report.md", "snapshot.json"])
m11, d11, p11 = st.open_current()
check("G11", not p11 and m11["generation"] == g11 and m11["inputs"]["board"].get("volatile") and st.drift(m11) == {"board": "changed"}
      and open(os.path.join(d11, "inputs", "board"), "rb").read() == b'{"rev": 1}',
      "a volatile input edited mid-build commits from its snapshot and reads as drift: %s" % st.drift(m11))
big = wsrc("game.exe", b"MZ" + b"\0" * 100)
g12 = st.commit(build(inputs={"a": {"path": a}, "exe": {"path": big, "snapshot": False}}), ["report.md", "snapshot.json"])
m12, d12, p12 = st.open_current()
z12 = os.path.join(T, "ext.zip"); st.export(z12); names12 = zipfile.ZipFile(z12).namelist()
def g12_mutate(): open(big, "ab").write(b"x")
w12 = raises(lambda: st.commit(build(inputs={"a": {"path": a}, "exe": {"path": big, "snapshot": False}}, mutate=g12_mutate), ["report.md", "snapshot.json"]))
check("G12", not p12 and m12["inputs"]["exe"].get("external") and m12["inputs"]["exe"]["sha256"] and not os.path.exists(os.path.join(d12, "inputs", "exe"))
      and "inputs/exe" not in names12 and "inputs/a" in names12 and w12 and "inputs moved during the build: exe" in w12,
      "external input hashed, not copied, not exported; moving it mid-build still refuses: %s" % w12)
# G13: the reader's own verification runs on the final on-disk candidate before CURRENT moves
cur13 = st.current_id(); hist13 = open(os.path.join(st.root, G.HISTORY)).read()
real_open = G.Store.open_generation
def reject_new(self, gid, sha=None):
    m, d, p = real_open(self, gid, sha)
    return (m, d, p + ["injected: reader rejects this candidate"]) if gid not in (cur13,) and sha is not None else (m, d, p)
G.Store.open_generation = reject_new
w13 = raises(lambda: st.commit(build(), ["report.md", "snapshot.json"]))
G.Store.open_generation = real_open
rejected = [x for x in os.listdir(st.root) if x.endswith(".rejected")]
flog = open(os.path.join(st.root, G.FAILURES)).read().splitlines()
check("G13", w13 and "failed the reader's verification" in w13 and st.current_id() == cur13 and open(os.path.join(st.root, G.HISTORY)).read() == hist13
      and len(rejected) == 1 and "failed the reader's verification" in json.loads(flog[-1])["reason"] and not st.open_current()[2],
      "rejected %s kept aside; CURRENT %s and history unchanged" % (rejected, cur13))
# G14: a manifest format this reader does not know -> UNSUPPORTED, never a guessed verdict
m14, d14, _ = st.open_current(); mp = os.path.join(d14, G.MANIFEST); keep14 = open(mp, "rb").read()
open(mp, "wb").write(keep14.replace(b'"ff12-generation-2"', b'"ff12-generation-9"'))
_, _, p14 = st.open_generation(m14["generation"])
open(mp, "wb").write(keep14)
check("G14", len(p14) == 1 and p14[0].startswith("UNSUPPORTED") and "ff12-generation-9" in p14[0], p14[0][:80] if p14 else "")
# G15: a reader whose module changed on disk since it loaded reports itself stale
real_sha = G.VERIFIER_SHA; G.VERIFIER_SHA = "0" * 64; s15 = G.reader_stale(); G.VERIFIER_SHA = real_sha
check("G15", s15 and not G.reader_stale() and m14.get("verifier") == G.VERIFIER_SHA and m14.get("format") == G.FORMAT,
      "a changed module -> stale; the manifest records format %s and verifier %s" % (m14.get("format"), (m14.get("verifier") or "")[:12]))
c1, c2 = wsrc("crlf.md", b"a\r\nb\r\n"), wsrc("lf.md", b"a\nb\n")
check("G10", G.input_state(c1)["sha256"] != G.input_state(c2)["sha256"], "CRLF and LF fingerprints differ")
zp = os.path.join(T, "export.zip"); gx = st.current_id()
eg = st.export(zp)
label, info = G.verify_zip(zp)
side = open(zp + ".sha256").read().split()[0]
check("E1", label == "VERIFIED" and info["generation"] == gx == eg and side == G.sha256_file(zp), "%s %s" % (label, info))
# E2: a generation committed while an export is in flight - export pins the id it opened
orig = G.verify_zip
def racing_verify(p):
    st.commit(build(), ["report.md", "snapshot.json"])     # lands mid-export
    return orig(p)
G.verify_zip = racing_verify
zp2 = os.path.join(T, "export2.zip"); eg2 = st.export(zp2); G.verify_zip = orig
l2, i2 = G.verify_zip(zp2)
check("E2", eg2 == gx and l2 == "VERIFIED" and i2["generation"] == gx and st.current_id() != gx, "exported %s while CURRENT moved to %s" % (eg2, st.current_id()))
mixed = os.path.join(T, "mixed.zip")
with zipfile.ZipFile(mixed, "w") as zz:
    zz.write(os.path.join(st.root, g1, "outputs", "report.md"), "outputs/report.md")
    zz.write(os.path.join(st.root, st.current_id(), "outputs", "snapshot.json"), "outputs/snapshot.json")
lm, im = G.verify_zip(mixed)
tz = os.path.join(T, "tampered.zip")
with zipfile.ZipFile(zp) as src, zipfile.ZipFile(tz, "w") as dst:
    for n in src.namelist():
        dst.writestr(n, b"tampered" if n == "outputs/report.md" else src.read(n))
lt, it = G.verify_zip(tz)
check("E3", lm == "UNVERIFIED" and "no MANIFEST" in im["reason"] and lt == "UNVERIFIED" and it["hash_mismatch"] == ["outputs/report.md"], "%s / %s" % (im["reason"], it))
# E4-E7: ASTRA's certification REJECT (97c4c1b65) - member multiplicity, unknown format, malformed manifest
import warnings, zipfile
def rezip(dst, edit=None, extra=()):
    with zipfile.ZipFile(zp) as src, zipfile.ZipFile(dst, "w") as out, warnings.catch_warnings():
        warnings.simplefilter("ignore")                      # zipfile warns on a duplicate name; the duplicate is the case
        for i in src.infolist():
            data = src.read(i.filename)
            out.writestr(i.filename, edit(i.filename, data) if edit else data)
        for n, data in extra:
            out.writestr(n, data)
out_name = next(n for n in zipfile.ZipFile(zp).namelist() if n.startswith("outputs/"))
dz = os.path.join(T, "dup.zip"); rezip(dz, extra=[(out_name, b"a second, different body under the same name")])
ld, idd = G.verify_zip(dz)
check("E4", ld == "UNVERIFIED" and "duplicate" in idd["reason"] and idd["duplicates"] == [out_name], "%s %s" % (ld, idd))
uz = os.path.join(T, "unknown.zip")
rezip(uz, edit=lambda n, d: json.dumps(dict(json.loads(d), format="ff12-generation-99")).encode() if n == G.MANIFEST else d)
lu, iu = G.verify_zip(uz)
check("E5", lu == "UNVERIFIED" and iu["reason"].startswith("UNSUPPORTED"), "%s %s" % (lu, iu.get("reason", "")[:70]))
jz = os.path.join(T, "badjson.zip"); rezip(jz, edit=lambda n, d: b"{not json" if n == G.MANIFEST else d)
lj, ij = G.verify_zip(jz)
sz = os.path.join(T, "shape.zip"); rezip(sz, edit=lambda n, d: json.dumps(dict(json.loads(d), outputs=["x"])).encode() if n == G.MANIFEST else d)
ls_, is_ = G.verify_zip(sz)
rj = subprocess.run([sys.executable, os.path.join(HERE, "generation.py"), "verify-zip", jz], capture_output=True, text=True)
check("E6", lj == "UNVERIFIED" and "not JSON" in ij["reason"] and ls_ == "UNVERIFIED" and "outputs is not an object" in is_["reason"]
      and rj.returncode == 1 and rj.stdout.startswith("UNVERIFIED") and "Traceback" not in rj.stderr,
      "%s / %s / cli rc %d %s" % (ij["reason"][:40], is_["reason"], rj.returncode, rj.stdout[:30]))
# E8: ASTRA's second REJECT (7d9b5ec17) - relabel one present, non-external input with an unknown state and drop its snapshot
with zipfile.ZipFile(zp) as src:
    m8 = json.loads(src.read(G.MANIFEST))
    victim = next(n for n, c in m8["inputs"].items() if c["state"] == "present" and not c.get("external"))
    m8["inputs"][victim]["state"] = "ASTRA_LABELLED_UNKNOWN_STATE"
    uz8 = os.path.join(T, "unknown-state.zip")
    with zipfile.ZipFile(uz8, "w") as out:
        for i in src.infolist():
            if i.filename == "inputs/" + victim:
                continue
            out.writestr(i.filename, json.dumps(m8).encode() if i.filename == G.MANIFEST else src.read(i.filename))
l8, i8 = G.verify_zip(uz8)
r8 = subprocess.run([sys.executable, os.path.join(HERE, "generation.py"), "verify-zip", uz8], capture_output=True, text=True)
check("E8", l8 == "UNVERIFIED" and "unknown state" in i8["reason"] and r8.returncode == 1 and r8.stdout.startswith("UNVERIFIED"),
      "%s %s / cli %d" % (l8, i8.get("reason", "")[:70], r8.returncode))
cur_id = st.current_id(); mpath = os.path.join(st.root, cur_id, G.MANIFEST); keep = open(mpath, "rb").read()
open(mpath, "wb").write(b"{not json")
try:
    m7, _d7, p7 = st.open_generation(cur_id); raised = None
except Exception as e:  # noqa: BLE001 - the case is that nothing raises
    m7, p7, raised = None, [], e
open(mpath, "wb").write(keep)
check("E7", raised is None and m7 is None and any("not JSON" in p for p in p7) and not st.open_current()[2],
      "store-folder malformed manifest -> %s (restored clean)" % (p7 or raised))
def cli(*args):
    r = subprocess.run([sys.executable, os.path.join(HERE, "generation.py")] + list(args), capture_output=True, text=True)
    return r.returncode, r.stdout.strip()
r1 = cli("status", st.root); open(a, "wb").write(b"alpha moved\n"); r2 = cli("status", st.root)
r3, r4 = cli("verify-zip", zp), cli("verify-zip", mixed)
check("C1", r1[0] == 0 and r1[1].startswith("CURRENT") and r2[1].startswith("STALE") and "'a'" in r2[1] and r3[0] == 0 and r4[0] == 1,
      "%s | %s | %s | %s" % (r1[1][:40], r2[1][:60], r3[1][:30], r4[1][:40]))
# R1-R4: portable snapshot names and the supported restore (ASTRA-REQ-OPUS-A23-WINDOWS-SNAPSHOT-RESTORE)
rs = G.Store(os.path.join(T, "rgens")); pk = wsrc("PKG-X.md", b"package x\n")
rb = rs.begin({"a": {"path": a}, "pkg:PKG-X.md": {"path": pk}}, {"name": "fixture", "sha256": "0"})
open(rb.output_path("report.md"), "wb").write(b"r\n"); gr = rs.commit(rb, ["report.md"]); mr, dr, pr = rs.open_current()
phys = os.listdir(os.path.join(dr, "inputs"))
zr = os.path.join(T, "r.zip"); rs.export(zr); zn = zipfile.ZipFile(zr).namelist()
dest = os.path.join(T, "restored"); gg = G.restore_zip(zr, dest)
m_r, d_r, p_r = G.Store(dest).open_current()
cli = subprocess.run([sys.executable, os.path.join(HERE, "generation.py"), "restore", zr, os.path.join(T, "restored-cli")], capture_output=True, text=True)
_, _, p_cli = G.Store(os.path.join(T, "restored-cli")).open_current()
check("R1", not pr and sorted(phys) == ["a", "pkg%3APKG-X.md"] and "inputs/pkg:PKG-X.md" in zn and gg == gr and not p_r
      and open(os.path.join(d_r, "inputs", "pkg%3APKG-X.md"), "rb").read() == b"package x\n" and cli.returncode == 0
      and cli.stdout.startswith("RESTORED") and not p_cli, "physical %s; zip %s; restored %s %s" % (phys, [n for n in zn if "pkg" in n], gg, p_r or "clean"))
# R2: a generation written before the escape kept the raw logical name; rename the portable file back to a raw name that
# every file system can hold (':' cannot be tested portably, so use a name whose only escaped character is '%')
lb = rs.begin({"a": {"path": a}, "p%1": {"path": pk}}, {"name": "fixture", "sha256": "0"})
open(lb.output_path("report.md"), "wb").write(b"r\n"); gl = rs.commit(lb, ["report.md"]); ml, dl, _ = rs.open_current()
os.rename(os.path.join(dl, "inputs", "p%251"), os.path.join(dl, "inputs", "p%1")); _, _, pl = rs.open_current()
os.remove(os.path.join(dl, "inputs", "p%1")); _, _, pgone = rs.open_current()
check("R2", not pl and any("input snapshot p%1" in x for x in pgone), "legacy raw name reads clean; removing it is still refused: %s" % pgone)
# R3
bad = os.path.join(T, "bad.zip"); shutil.copyfile(zr, bad)
with zipfile.ZipFile(bad, "a") as zb: zb.writestr("outputs/extra.md", b"x")
w_unv = raises(lambda: G.restore_zip(bad, os.path.join(T, "r3a")))
os.makedirs(os.path.join(T, "r3b")); open(os.path.join(T, "r3b", "keep"), "w").write("x")
w_full = raises(lambda: G.restore_zip(zr, os.path.join(T, "r3b")))
def col_zip(path, names):
    man = {"format": G.FORMAT, "generation": "gcol", "outputs": {}, "inputs": {}}
    with zipfile.ZipFile(path, "w") as zc:
        for n in names:
            man["inputs"][n] = {"state": "present", "sha256": G.hashlib.sha256(n.encode()).hexdigest(), "path": n}
            zc.writestr("inputs/" + n, n.encode())
        zc.writestr(G.MANIFEST, json.dumps(man))
zc1, zc2 = os.path.join(T, "c1.zip"), os.path.join(T, "c2.zip"); col_zip(zc1, ["a:b", "a%3Ab"]); col_zip(zc2, ["Name", "name"])
w_col = raises(lambda: G.restore_zip(zc1, os.path.join(T, "r3c"))); w_case = raises(lambda: G.restore_zip(zc2, os.path.join(T, "r3d")))
check("R3", w_unv and "UNVERIFIED" in w_unv and w_full and "non-empty" in w_full and w_col is None and w_case and "case-insensitive" in w_case
      and not os.path.exists(os.path.join(T, "r3a", G.CURRENT)) and not os.path.exists(os.path.join(T, "r3d", G.CURRENT)),
      "unverified: %s | non-empty: %s | 'a:b'+'a%%3Ab': %s | case pair: %s" % (w_unv, w_full, w_col or "distinct files (escape is one-to-one)", w_case))
# R4
names = ["a:b", "a%3Ab", "a_b", "a%b", "a%25b", "x/y", "x\\y", "plain.md"]
check("R4", len(set(G.snapshot_name(n) for n in names)) == len(names) and G.snapshot_name("plain.md") == "plain.md"
      and all(not set(G.snapshot_name(n)) & set('<>:"/\\|?*') for n in names), [G.snapshot_name(n) for n in names])
shutil.rmtree(T, ignore_errors=True)
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
