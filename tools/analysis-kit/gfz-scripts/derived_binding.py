"""derived_binding.py - bind a COMMITTED derived surface to the committed bytes it was computed from (OPUS, 2026-10-03).

WHY THIS EXISTS. A derived surface (PROGRESS.md and its route files, and any other generated current-state view) is
built by a generation (generation.py) in an ignored store and copied into the tracked tree. The store knows exactly
which input bytes a generation consumed; the COMMITTED copy did not. So on 2026-10-03 PROGRESS.md was committed reading
`freshness: CURRENT` and "52 MET of 52" (generated 07:11Z from 39bcb329b), L2-VERDICTS.md moved to 48 MET in 78b17b620
at 07:27Z, the watchdog regenerated the worktree copy, and nothing ever committed it: every commit after 78b17b620
carried a CURRENT label its own tree contradicted, and the return ZIP shipped it. Four mechanisms each allowed it:
  1. CURRENT was a generation-time assertion written into a file that outlives its inputs, with nothing binding it;
  2. publishing an authoritative input (L2-VERDICTS.md) neither regenerated nor invalidated its dependents;
  3. regeneration landed only in the worktree - publication of derived outputs depended on a lane remembering;
  4. no checkpoint validator compared committed derived surfaces with their committed inputs.

THE MECHANISM. A generator that publishes into the tracked tree also writes a binding sidecar,
`<dir>/GENERATION-BINDING.json`, naming:
  - `bound`: every non-volatile input that is a file in the repository, with the sha256 of the exact bytes consumed;
  - `as_of`: inputs that are recorded but cannot be bound to a commit (volatile board, derived preimages, files outside
    the repository) - a reader must present these as "as of <time>", never as current;
  - `outputs`: the committed output files with their sha256;
  - `regenerate`: the supported command that rebuilds the surface (run from the repository root);
  - `stale_labels`: how the outputs say STALE (text token or JSON key), applied when they cannot be made current.
state() evaluates a binding against ANY tree - the worktree, a git revision, or a private index - so the same rule is
checked at publish time, at a checkpoint and inside a return package.

THE INVARIANT (publish_paths.sh runs `gate` on every commit, before the tree is written):
  a committed surface whose binding says CURRENT has every bound input byte-identical in the commit's tree, and every
  output byte-identical to the binding.
When a commit would break it (it moves a bound input, or the binding already disagrees with the tree), the gate runs the
surface's supported regeneration and includes the new outputs and binding in the SAME commit if they bind to that commit's
tree; otherwise it stages the existing outputs relabelled STALE with the moved inputs named. A surface is never left
claiming CURRENT over moved inputs. The failure mode is an explicit STALE, never a silent green.

CLI:  python derived_binding.py check [--rev REV | --worktree] [--root ROOT]      exit 0 all CURRENT or declared STALE,
                                                                                  1 any FALSE-CURRENT or INCOHERENT
      python derived_binding.py gate --root ROOT --index INDEXFILE               (publish_paths.sh)
      python derived_binding.py --self-test
"""
import hashlib
import io
import json
import os
import re
import subprocess
import sys
import tempfile

FORMAT = "ff12-derived-binding-1"
NAME = "GENERATION-BINDING.json"
STATES = ("CURRENT", "STALE", "FALSE-CURRENT", "INCOHERENT", "MISSING")


def sha(b):
    """sha256 of the bytes with CRLF folded to LF. git's autocrlf stores LF and checks out CRLF, so a raw hash of a
    worktree file never equals the hash of its committed blob; the binding compares the same text across the
    worktree, the index and a commit, which this form makes possible."""
    return hashlib.sha256(b.replace(b"\r\n", b"\n")).hexdigest()


def raw_sha(b):
    return hashlib.sha256(b).hexdigest()


# ------------------------------------------------------------------ readers: rel path (posix) -> bytes or None
def worktree_reader(root):
    def read(rel):
        p = os.path.join(root, *rel.split("/"))
        try:
            with open(p, "rb") as f:
                return f.read()
        except OSError:
            return None
    return read


def git_reader(root, rev=None, index_file=None):
    """rev='HEAD' (or any commit) reads committed bytes; index_file reads a (private) index (`:path`)."""
    env = dict(os.environ)
    if index_file:
        env["GIT_INDEX_FILE"] = index_file

    def read(rel):
        spec = (":%s" % rel) if index_file or rev is None else ("%s:%s" % (rev, rel))
        r = subprocess.run(["git", "-C", root, "show", spec], capture_output=True, env=env)
        return r.stdout if r.returncode == 0 else None
    return read


def overlay(primary, secondary, paths):
    """Read `paths` from `primary`, everything else from `secondary`."""
    paths = set(paths)

    def read(rel):
        return primary(rel) if rel in paths else secondary(rel)
    return read


# ------------------------------------------------------------------ writing a binding
def write_binding(out_path, repo_root, surface, man, outputs, regenerate, stale_labels, as_of_names=()):
    """Write `<dir>/GENERATION-BINDING.json` for a committed generation `man` (generation.py manifest).
    outputs: {repo-relative path: absolute file path} of the copies just published. An input is BOUND when it is a
    present-or-missing file inside repo_root, not volatile, not external and not named in as_of_names."""
    root = os.path.abspath(repo_root)
    bound, as_of = {}, {}
    for name, c in sorted(man["inputs"].items()):
        p = os.path.abspath(c.get("path", ""))
        rel = os.path.relpath(p, root).replace(os.sep, "/") if p.startswith(root + os.sep) else None
        rec = {"sha256": c.get("sha256"), "state": c.get("state")}
        if rel is None:
            as_of[name] = dict(rec, reason="outside the repository")
        elif c.get("volatile"):
            as_of[name] = dict(rec, path=rel, reason="volatile (read only from its snapshot)")
        elif name in as_of_names:
            as_of[name] = dict(rec, path=rel, reason="derived preimage, recorded not bound")
        elif c.get("state") in ("present", "empty"):
            # bind the EOL-normalised hash, but only of the bytes the generation actually consumed
            try:
                with open(p, "rb") as f:
                    data = f.read()
            except OSError:
                data = None
            bound[rel] = sha(data) if data is not None and raw_sha(data) == c.get("sha256") \
                else "MOVED-SINCE-GENERATION"
        else:
            bound[rel] = "MISSING"
    outs = {}
    for rel, absp in sorted(outputs.items()):
        with open(absp, "rb") as f:
            outs[rel] = sha(f.read())
    b = {"format": FORMAT, "surface": surface, "state": "CURRENT", "generation": man.get("generation"),
         "committed_at": man.get("committed_at"), "bound": bound, "as_of": as_of, "outputs": outs,
         "regenerate": list(regenerate), "stale_labels": list(stale_labels), "hash": "sha256 of CRLF-folded bytes"}
    data = (json.dumps(b, indent=1, sort_keys=True) + "\n").encode("utf-8")
    tmp = out_path + ".tmp"
    with open(tmp, "wb") as f:
        f.write(data)
    os.replace(tmp, out_path)
    return b


# ------------------------------------------------------------------ evaluating a binding
def load(data):
    b = json.loads(data.decode("utf-8") if isinstance(data, bytes) else data)
    if b.get("format") != FORMAT:
        raise ValueError("unsupported binding format %r" % b.get("format"))
    return b


def state(b, read):
    """-> {'state', 'moved': [rel...], 'outputs_bad': [rel...]} for binding b against the tree `read` sees.
    CURRENT       bound inputs and outputs all match, binding declares CURRENT
    STALE         binding declares STALE (labelled) and its outputs match - an explicit, honest state
    FALSE-CURRENT binding declares CURRENT but a bound input moved: the forbidden state
    INCOHERENT    an output differs from the binding (hand-edited or mixed set)"""
    moved = []
    for rel, want in sorted(b["bound"].items()):
        data = read(rel)
        have = "MISSING" if data is None else sha(data)
        if have != want:
            moved.append(rel)
    bad = []
    for rel, want in sorted(b["outputs"].items()):
        data = read(rel)
        if data is None or sha(data) != want:
            bad.append(rel)
    if bad:
        st = "INCOHERENT"
    elif b.get("state") == "STALE":
        st = "STALE"
    elif moved:
        st = "FALSE-CURRENT"
    else:
        st = "CURRENT"
    return {"state": st, "moved": moved, "outputs_bad": bad}


_VAL = r"(?:[^()\n]|\([^()\n]*\))*"   # a placeholder's value: anything on the line, parentheses balanced one deep


def _stale_patterns(replace, stale_tok):
    """-> (exact, loose): `exact` matches an annotation this rule's `replace` template produced, whatever moved set and
    generation it named; `loose` matches the stale token plus an optional parenthesised reason directly after it
    (an annotation written by an earlier wording of the template)."""
    parts = re.split(r"(\{moved\}|\{generation\})", replace)
    exact = re.compile("".join(_VAL if p in ("{moved}", "{generation}") else re.escape(p) for p in parts))
    loose = re.compile(re.escape(stale_tok) + r"(?: \(" + _VAL + r"\))?")
    return exact, loose


def relabel(data, rule, moved, generation):
    """Apply one stale_label rule to output bytes. kind 'text': replace `find` with `replace` on lines matching
    `line_regex` (at least one must match); kind 'json': set the key path to `value` and add `stale_moved`.
    Relabelling an output that already says STALE is legal and rewrites its annotation to the CURRENT moved set, so
    the output names exactly what the binding's `stale_moved` names; an unchanged moved set reproduces the same bytes."""
    note = ", ".join(moved) or "unknown"
    if rule["kind"] == "text":
        text = data.decode("utf-8")
        rx = re.compile(rule["line_regex"])
        out, hit = [], 0
        stale_tok = rule["replace"].split(" ", 1)[0]   # e.g. "`STALE`"
        label = rule["replace"].format(moved=note, generation=generation)
        exact, loose = _stale_patterns(rule["replace"], stale_tok) if stale_tok else (None, None)
        for line in text.splitlines(keepends=True):
            if rx.search(line) and rule["find"] in line:
                line = line.replace(rule["find"], label, 1)
                hit += 1
            elif rx.search(line) and stale_tok and stale_tok in line:
                # already labelled stale by an earlier publish: relabelling is legal (SWE2-FRONTIER 2026-10-03; before
                # that, every publish was refused once the committed surface said STALE) and REWRITES the annotation
                # to the moved set of this relabel (OPUS 2026-10-03; before that, `STALE (moved: old.txt)` stayed
                # when new.txt moved, so the output and GENERATION-BINDING.json named different inputs)
                m = exact.search(line) or loose.search(line)
                line = line[:m.start()] + label + line[m.end():]
                hit += 1
            out.append(line)
        if not hit:
            raise ValueError("stale label: no line of %s matches %r" % (rule["path"], rule["line_regex"]))
        return "".join(out).encode("utf-8")
    if rule["kind"] == "json":
        j = json.loads(data.decode("utf-8"))
        node = j
        for k in rule["key"][:-1]:
            node = node[k]
        node[rule["key"][-1]] = rule["value"]
        node["stale_moved"] = moved
        return (json.dumps(j, indent=1, ensure_ascii=False) + "\n").encode("utf-8")
    raise ValueError("unknown stale label kind %r" % rule["kind"])


# ------------------------------------------------------------------ discovery
def bindings_in(root, index_file=None, rev=None):
    env = dict(os.environ)
    if index_file:
        env["GIT_INDEX_FILE"] = index_file
    if rev:
        r = subprocess.run(["git", "-C", root, "ls-tree", "-r", "--name-only", rev], capture_output=True, text=True)
    else:
        r = subprocess.run(["git", "-C", root, "ls-files"], capture_output=True, text=True, env=env)
    return sorted(p for p in r.stdout.splitlines() if p.endswith("/" + NAME) or p == NAME)


def check(root, rev=None, worktree=False):
    read = worktree_reader(root) if worktree else git_reader(root, rev=rev or "HEAD")
    paths = bindings_in(root, rev=None if worktree else (rev or "HEAD"))
    if worktree:
        extra = subprocess.run(["git", "-C", root, "ls-files", "--others", "--exclude-standard"], capture_output=True,
                               text=True).stdout.splitlines()
        paths = sorted(set(paths) | {p for p in extra if p.endswith("/" + NAME) or p == NAME})
        paths = [p for p in paths if os.path.exists(os.path.join(root, p))]
    worst = 0
    for p in paths:
        data = read(p)
        if data is None:
            print("MISSING     %s" % p)
            worst = 1
            continue
        b = load(data)
        s = state(b, read)
        print("%-12s %s (%s, generation %s)%s%s" % (
            s["state"], p, b["surface"], b.get("generation"),
            ("; bound inputs moved: " + ", ".join(s["moved"])) if s["moved"] else "",
            ("; outputs differ: " + ", ".join(s["outputs_bad"])) if s["outputs_bad"] else ""))
        if s["state"] in ("FALSE-CURRENT", "INCOHERENT"):
            worst = 1
    if not paths:
        print("no derived-surface bindings in %s" % ("the worktree" if worktree else (rev or "HEAD")))
    return worst


# ------------------------------------------------------------------ the publish gate
def _stage_blob(root, index_file, rel, data):
    env = dict(os.environ, GIT_INDEX_FILE=index_file)
    h = subprocess.run(["git", "-C", root, "hash-object", "-w", "--stdin"], input=data, capture_output=True, env=env)
    if h.returncode:
        raise RuntimeError("hash-object failed for %s: %s" % (rel, h.stderr.decode(errors="replace")))
    oid = h.stdout.decode().strip()
    u = subprocess.run(["git", "-C", root, "update-index", "--add", "--cacheinfo", "100644,%s,%s" % (oid, rel)],
                       capture_output=True, env=env)
    if u.returncode:
        raise RuntimeError("update-index failed for %s: %s" % (rel, u.stderr.decode(errors="replace")))


def gate(root, index_file, regen=True, tries=3, log=print, staged_out=None):
    """Make every binding in the private index CURRENT or honestly STALE before the commit tree is written.
    Returns 0, or 1 when a binding could not be evaluated (the caller refuses the publish). Every path the gate stages
    is appended to `staged_out` (a list) when given."""
    idx = git_reader(root, index_file=index_file)
    wt = worktree_reader(root)
    staged_out = staged_out if staged_out is not None else []
    regen_env = {k: v for k, v in os.environ.items() if k != "GIT_INDEX_FILE"}
    rc = 0
    for bp in bindings_in(root, index_file=index_file):
        try:
            b = load(idx(bp))
        except Exception as e:
            log("derived: %s unreadable in the commit: %s - publish refused" % (bp, e))
            rc = 1
            continue
        s = state(b, idx)
        if s["state"] == "CURRENT":
            log("derived: %s CURRENT for this commit" % b["surface"])
            continue
        log("derived: %s is %s for this commit%s" % (b["surface"], s["state"],
            (" (bound inputs moved: %s)" % ", ".join(s["moved"])) if s["moved"] else ""))
        # 1. the supported regeneration, then include it if it binds to THIS commit's tree
        if regen and b.get("regenerate"):
            for _ in range(tries):
                r = subprocess.run(b["regenerate"], cwd=root, capture_output=True, text=True, timeout=600,
                                   env=regen_env)
                tail = (r.stdout + r.stderr).strip().splitlines()[-1:] or [""]
                if r.returncode == 0:
                    break
                log("derived: regeneration attempt failed: %s" % tail[0][:200])
            else:
                r = None
            if r is not None and r.returncode == 0:
                try:
                    nb = load(wt(bp))
                except Exception as e:
                    nb = None
                    log("derived: regenerated binding unreadable: %s" % e)
                if nb is not None:
                    staged = set(nb["outputs"]) | {bp}
                    view = overlay(wt, idx, staged)
                    ns = state(nb, view)
                    if ns["state"] == "CURRENT":
                        for rel in sorted(staged):
                            _stage_blob(root, index_file, rel, wt(rel))
                            staged_out.append(rel)
                        log("derived: %s regenerated (generation %s) and INCLUDED in this commit: %s" % (
                            nb["surface"], nb.get("generation"), ", ".join(sorted(staged))))
                        continue
                    log("derived: regenerated %s does not bind to this commit's tree (moved: %s) - the worktree holds "
                        "uncommitted input edits" % (nb["surface"], ", ".join(ns["moved"]) or "-"))
        # 2. no current generation for this tree: the committed outputs say STALE, naming what moved
        moved = s["moved"] or ["(binding disagreed with its outputs)"]
        newb = dict(b, state="STALE", stale_moved=moved)
        outs = dict(b["outputs"])
        try:
            for rule in b.get("stale_labels", []):
                data = idx(rule["path"])
                if data is None:
                    raise ValueError("output %s missing from the commit" % rule["path"])
                data = relabel(data, rule, moved, b.get("generation"))
                _stage_blob(root, index_file, rule["path"], data)
                staged_out.append(rule["path"])
                outs[rule["path"]] = sha(data)
            newb["outputs"] = outs
            _stage_blob(root, index_file, bp, (json.dumps(newb, indent=1, sort_keys=True) + "\n").encode("utf-8"))
            staged_out.append(bp)
            log("derived: %s committed as STALE (moved: %s); a later publish regenerates it" % (
                b["surface"], ", ".join(moved)))
        except Exception as e:
            log("derived: could not label %s STALE: %s - publish refused" % (b["surface"], e))
            rc = 1
    return rc


# ------------------------------------------------------------------ self-test (the regression for 2026-10-03)
def _self_test():
    import shutil
    fails = []

    def ok(cond, what):
        print(("ok   " if cond else "FAIL ") + what)
        if not cond:
            fails.append(what)

    d = tempfile.mkdtemp(prefix="dbind-")
    try:
        def git(*a, **kw):
            return subprocess.run(["git", "-C", d] + list(a), capture_output=True, text=True, **kw)
        git("init", "-q")
        git("config", "user.email", "t@t")
        git("config", "user.name", "t")
        os.makedirs(os.path.join(d, "reg"))
        os.makedirs(os.path.join(d, "out"))
        gen_py = os.path.join(d, "gen.py")
        # a tiny generator: counts MET rows in reg/L2.md, writes out/P.md + out/s.json + the binding
        io.open(gen_py, "w", encoding="utf-8").write(
            "import json,os,sys,hashlib\n"
            "sys.path.insert(0,%r)\n"
            "import derived_binding as B\n"
            "d=os.path.dirname(os.path.abspath(__file__))\n"
            "src=open(os.path.join(d,'reg','L2.md'),'rb').read()\n"
            "n=src.decode().count('MET')-src.decode().count('NOT MET')\n"
            "open(os.path.join(d,'out','P.md'),'w').write('**freshness:** `CURRENT`\\n%%d MET\\n' %% n)\n"
            "json.dump({'freshness':{'state':'CURRENT'},'met':n},open(os.path.join(d,'out','s.json'),'w'))\n"
            "man={'generation':'g'+hashlib.sha256(src).hexdigest()[:6],'committed_at':'t','inputs':{\n"
            " 'in:reg/L2.md':{'path':os.path.join(d,'reg','L2.md'),'state':'present','sha256':hashlib.sha256(src).hexdigest()},\n"
            " 'in:board':{'path':os.path.join(d,'board.json'),'state':'present','sha256':'x','volatile':True}}}\n"
            "B.write_binding(os.path.join(d,'out','GENERATION-BINDING.json'),d,'t',man,\n"
            " {'out/P.md':os.path.join(d,'out','P.md'),'out/s.json':os.path.join(d,'out','s.json')},\n"
            " [sys.executable,'-B','gen.py'],\n"
            " [{'path':'out/P.md','kind':'text','line_regex':'freshness','find':'`CURRENT`','replace':'`STALE` (moved: {moved})'},\n"
            "  {'path':'out/s.json','kind':'json','key':['freshness','state'],'value':'STALE'}])\n"
            % os.path.dirname(os.path.abspath(__file__)))
        open(os.path.join(d, "reg", "L2.md"), "w").write("S-1 MET\nS-2 MET\n")
        subprocess.run([sys.executable, "-B", gen_py], cwd=d, check=True)
        git("add", "-A")
        git("commit", "-qm", "base")
        ok(check(d) == 0, "1 a valid generation committed with its inputs is CURRENT")
        # 2. an authoritative input changes in a commit WITHOUT the gate: the committed surface is FALSE-CURRENT
        open(os.path.join(d, "reg", "L2.md"), "w").write("S-1 MET\nS-2 NOT MET\n")
        git("add", "reg/L2.md")
        git("commit", "-qm", "verdict moves, dependents not regenerated")
        b = load(git_reader(d, rev="HEAD")("out/" + NAME))
        s = state(b, git_reader(d, rev="HEAD"))
        ok(s["state"] == "FALSE-CURRENT" and s["moved"] == ["reg/L2.md"],
           "2 the old generation is no longer CURRENT once its verdict input moved (FALSE-CURRENT, names reg/L2.md)")
        ok(check(d) == 1, "2b the checkpoint check fails on it")
        # 3. the supported path: a publish through the gate regenerates and includes the outputs in the same commit
        open(os.path.join(d, "reg", "L2.md"), "w").write("S-1 NOT MET\nS-2 NOT MET\n")
        idx = os.path.join(d, ".git", "private-index")
        env = dict(os.environ, GIT_INDEX_FILE=idx)
        subprocess.run(["git", "-C", d, "read-tree", "HEAD"], env=env, check=True)
        subprocess.run(["git", "-C", d, "add", "--", "reg/L2.md"], env=env, check=True)
        logs = []
        ok(gate(d, idx, log=logs.append) == 0, "3 the gate accepts the publish")
        tree = subprocess.run(["git", "-C", d, "write-tree"], env=env, capture_output=True, text=True).stdout.strip()
        cm = subprocess.run(["git", "-C", d, "commit-tree", tree, "-p", "HEAD", "-m", "gated"], capture_output=True,
                            text=True).stdout.strip()
        git("update-ref", "HEAD", cm)
        git("reset", "-q")          # the ordinary index follows HEAD again (a commit from a stale index reverts files)
        p_md = git_reader(d, rev="HEAD")("out/P.md").decode()
        ok("0 MET" in p_md and "`CURRENT`" in p_md, "4 the regenerated, included output reflects the changed verdict")
        ok(check(d) == 0, "5 the gated commit is CURRENT")
        # 6. regeneration impossible (generator broken): the gate labels the committed outputs STALE, never CURRENT
        io.open(gen_py, "a", encoding="utf-8").write("raise SystemExit(3)\n")
        git("add", "gen.py")
        git("commit", "-qm", "break the generator (untracked by the binding)")
        open(os.path.join(d, "reg", "L2.md"), "w").write("S-1 MET\nS-2 MET\nS-3 MET\n")
        subprocess.run(["git", "-C", d, "read-tree", "HEAD"], env=env, check=True)
        subprocess.run(["git", "-C", d, "add", "--", "reg/L2.md"], env=env, check=True)
        logs = []
        ok(gate(d, idx, log=logs.append, tries=1) == 0, "6 the gate still lets a source edit publish (never blocked "
                                                          "on a derived surface)")
        tree = subprocess.run(["git", "-C", d, "write-tree"], env=env, capture_output=True, text=True).stdout.strip()
        cm = subprocess.run(["git", "-C", d, "commit-tree", tree, "-p", "HEAD", "-m", "stale"], capture_output=True,
                            text=True).stdout.strip()
        git("update-ref", "HEAD", cm)
        git("reset", "-q")
        rd = git_reader(d, rev="HEAD")
        p_md = rd("out/P.md").decode()
        sj = json.loads(rd("out/s.json"))
        ok("`STALE` (moved: reg/L2.md)" in p_md and "`CURRENT`" not in p_md, "7 the committed text says STALE and names "
                                                                              "the moved input")
        ok(sj["freshness"]["state"] == "STALE", "8 the committed JSON says STALE")
        ok(check(d) == 0, "9 an honestly STALE surface passes the checkpoint check (explicit stale is legal)")
        # 10. a hand edit to a committed output is INCOHERENT
        open(os.path.join(d, "out", "P.md"), "a").write("hand edit\n")
        git("add", "out/P.md")
        git("commit", "-qm", "hand edit")
        ok(check(d) == 1, "10 a hand-edited output is INCOHERENT and fails the check")
        # 11. a volatile input never makes a surface stale
        b = load(rd("out/" + NAME))
        ok("in:board" in b["as_of"] and not any("board" in k for k in b["bound"]),
           "11 the volatile board is recorded as-of, never bound")
        # 12. relabelling an output that already says STALE is idempotent (never refuses the publish)
        r12 = {"path": "out/P.md", "kind": "text", "line_regex": "freshness", "find": "`CURRENT`",
               "replace": "`STALE` (moved: {moved})"}
        o12 = ""
        try:
            o12 = relabel(b"**freshness:** `STALE` (moved: old)\n", r12, ["reg/L2.md"], "g1").decode()
            ok("`STALE`" in o12 and "`CURRENT`" not in o12, "12 relabelling an already-STALE output is idempotent")
        except ValueError:
            ok(False, "12 relabelling an already-STALE output is idempotent")
        try:
            relabel(b"no label here\n", r12, ["reg/L2.md"], "g1")
            ok(False, "13 an output with no freshness line is still refused")
        except ValueError:
            ok(True, "13 an output with no freshness line is still refused")
        # 14-18. relabelling an already-STALE output rewrites the reason to the CURRENT moved set (the regression for
        # `STALE (moved: old.txt)` staying in place after new.txt moved)
        ok("(moved: reg/L2.md)" in o12 and "old" not in o12,
           "14 STALE (moved: A) + new moved set B -> displayed STALE reason names B, not A")
        rp = {"path": "o.md", "kind": "text", "line_regex": r"\*\*freshness:\*\*", "find": "`CURRENT`",
              "replace": "`STALE` (bound inputs moved since generation {generation}: {moved}; regenerate with "
                         "progress_report.py generate)"}
        base = b"# P\n**as of:** t \xc2\xb7 **freshness:** `CURRENT` (fp `f1`)\nbody `STALE` mention\n"
        a1 = relabel(base, rp, ["x/old.txt"], "g7")
        b1 = relabel(a1, rp, ["x/new.txt", "x/two.txt"], "g7")
        b2 = relabel(b1, rp, ["x/new.txt", "x/two.txt"], "g7")
        want = (b"# P\n**as of:** t \xc2\xb7 **freshness:** `STALE` (bound inputs moved since generation g7: x/new.txt, "
                b"x/two.txt; regenerate with progress_report.py generate) (fp `f1`)\nbody `STALE` mention\n")
        ok(b1 == want, "15 the live template's reason is rewritten in place to B; the rest of the line and the "
                       "unmatched lines are untouched")
        ok(b2 == b1 and relabel(a1, rp, ["x/old.txt"], "g7") == a1,
           "16 a relabel with an unchanged moved set changes nothing")
        rn = {"path": "o.md", "kind": "text", "line_regex": "freshness", "find": "`CURRENT`",
              "replace": "`STALE` (moved: {moved})"}
        n1 = relabel(b"**freshness:** `STALE` (moved: (binding disagreed with its outputs)) tail\n", rn, ["a.txt"], "g")
        n2 = relabel(b"**freshness:** `STALE` (an older wording: old.txt) tail\n", rn, ["a.txt"], "g")
        ok(n1 == n2 == b"**freshness:** `STALE` (moved: a.txt) tail\n",
           "17 a nested-parenthesis reason and an older wording are both replaced whole")
        rj = {"path": "s.json", "kind": "json", "key": ["freshness", "state"], "value": "STALE"}
        j1 = relabel(b'{"freshness": {"state": "STALE", "stale_moved": ["old.txt"]}}', rj, ["new.txt"], "g")
        ok(json.loads(j1)["freshness"]["stale_moved"] == ["new.txt"], "18 the JSON stale_moved names B")
        # 19. end to end through the gate: two publishes with different moved sets; the committed output names exactly
        # the binding's stale_moved each time, and a third publish with the same moved set leaves the tree unchanged
        os.makedirs(os.path.join(d, "two"))
        for n in ("a", "b"):
            open(os.path.join(d, "two", n + ".txt"), "w").write(n + "0\n")
        open(os.path.join(d, "two", "O.md"), "w").write("**freshness:** `CURRENT`\n")

        def raw(rel):
            return hashlib.sha256(open(os.path.join(d, rel), "rb").read()).hexdigest()
        man2 = {"generation": "g2", "committed_at": "t", "inputs": {
            n: {"path": os.path.join(d, "two", n + ".txt"), "state": "present", "sha256": raw("two/%s.txt" % n)}
            for n in ("a", "b")}}
        write_binding(os.path.join(d, "two", NAME), d, "two", man2, {"two/O.md": os.path.join(d, "two", "O.md")}, [],
                      [dict(rn, path="two/O.md")])
        git("add", "two")
        git("commit", "-qm", "second surface")

        def publish(a, b_):
            open(os.path.join(d, "two", "a.txt"), "w").write(a)
            open(os.path.join(d, "two", "b.txt"), "w").write(b_)
            subprocess.run(["git", "-C", d, "read-tree", "HEAD"], env=env, check=True)
            subprocess.run(["git", "-C", d, "add", "--", "two/a.txt", "two/b.txt"], env=env, check=True)
            rc = gate(d, idx, regen=False, log=[].append)
            t = subprocess.run(["git", "-C", d, "write-tree"], env=env, capture_output=True, text=True).stdout.strip()
            c = subprocess.run(["git", "-C", d, "commit-tree", t, "-p", "HEAD", "-m", "p"], capture_output=True,
                               text=True).stdout.strip()
            git("update-ref", "HEAD", c)
            git("reset", "-q")
            r = git_reader(d, rev="HEAD")
            bb = load(r("two/" + NAME))
            return rc, t, r("two/O.md").decode(), bb, state(bb, r)["state"]
        rc1, _, o1, bb1, s1 = publish("a1\n", "b0\n")
        rc2, t2, o2, bb2, s2 = publish("a0\n", "b1\n")
        rc3, t3, o3, bb3, s3 = publish("a0\n", "b1\n")
        ok(rc1 == 0 and s1 == "STALE" and bb1["stale_moved"] == ["two/a.txt"] and "(moved: two/a.txt)" in o1,
           "19a publish 1: output and binding both name A = two/a.txt")
        ok(rc2 == 0 and s2 == "STALE" and bb2["stale_moved"] == ["two/b.txt"] and "(moved: two/b.txt)" in o2
           and "a.txt" not in o2, "19b publish 2: output and binding both name B = two/b.txt, A is gone")
        ok(rc3 == 0 and s3 == "STALE" and t3 == t2 and o3 == o2 and bb3 == bb2,
           "19c publish 3 with the same moved set commits an identical tree")
    finally:
        shutil.rmtree(d, ignore_errors=True)
    print("self-test: %d failure(s)" % len(fails))
    return 1 if fails else 0


def main(argv):
    if "--self-test" in argv:
        return _self_test()
    if len(argv) < 2:
        print(__doc__.split("CLI:")[1])
        return 2
    cmd = argv[1]

    def opt(k, default=None):
        return argv[argv.index(k) + 1] if k in argv else default
    root = opt("--root", os.getcwd())
    if cmd == "check":
        return check(root, rev=opt("--rev"), worktree="--worktree" in argv)
    if cmd == "gate":
        staged = []
        rc = gate(root, opt("--index"), regen="--no-regen" not in argv, staged_out=staged)
        if opt("--list"):
            with io.open(opt("--list"), "w", encoding="utf-8", newline="\n") as f:
                f.write("".join(p + "\n" for p in sorted(set(staged))))
        return rc
    print("unknown command")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
