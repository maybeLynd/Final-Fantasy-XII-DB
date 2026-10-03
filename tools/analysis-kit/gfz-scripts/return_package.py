"""return_package.py - build and verify return packages whose provenance is derived from what was exported.

  python return_package.py build --spec SPEC.json --out PKG.zip [--repo DIR]
  python return_package.py verify PKG.zip [--repo DIR]
  python return_package.py --self-test

SPEC.json:
  {"commits":  [{"sha": "...", "representation": "FORMAT_PATCH" | "FINAL_SNAPSHOT" | "RECEIPT_ONLY", "reason": "..."}],
   "files":    ["repo/path", ...],        exported as files/<path> from HEAD (git show HEAD:<path>)
   "receipts": ["repo/path", ...],        exported as receipts/<path> from the working tree
   "report":   "repo/path/to/report.md"}  exported as REPORT.md

The builder writes patches/NNNN-<sha9>.patch (git format-patch -1 --stdout) for every FORMAT_PATCH commit, files/,
receipts/, REPORT.md, PROVENANCE.json and MANIFEST.json. PROVENANCE is derived from the members actually written: a
FINAL_SNAPSHOT commit is represented by the exported HEAD files that the commit touched (none -> the package fails
verify). The zip is written under a temporary name, re-opened, verified, and renamed only when VERIFIED. An existing
target is never overwritten.

verify fails (exit 1) and names every problem by rule:
  A_UNPROVENANCED_CITE   REPORT.md cites a token that resolves to a commit with no PROVENANCE entry
  B_PATCH_MISSING        a FORMAT_PATCH entry has no patch member
  B_PATCH_FROM_MISMATCH  a FORMAT_PATCH entry's patch has a "From <sha>" line naming another commit
  C_STRAY_PATCH          a patches/ member that no PROVENANCE entry lists
  D_BAD_REPRESENTATION   a PROVENANCE entry with no or an unknown representation (or a RECEIPT_ONLY with no reason)
  E_NAME_SHA_MISMATCH    a patch file name whose sha9 disagrees with its From line (or a malformed patch name)
  F_MANIFEST             a MANIFEST hash disagrees, or a member is missing from or extra to MANIFEST
  G_SNAPSHOT_NO_FILE     a FINAL_SNAPSHOT entry that names no existing files/ member
  R_OVERCLAIM            REPORT.md claims every/all commits are format-patches while some are not, or states a
                         patch/commit count that disagrees with the package
  X_STRUCTURE            missing REPORT.md/PROVENANCE.json/MANIFEST.json, unreadable JSON, duplicate or unresolvable sha,
                         or a PROVENANCE member that is not in the zip
"""
import argparse
import hashlib
import io
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import zipfile

REPRESENTATIONS = ("FORMAT_PATCH", "FINAL_SNAPSHOT", "RECEIPT_ONLY")
PATCH_NAME = re.compile(r"^patches/(\d{4})-([0-9a-f]{9})\.patch$")
FROM_LINE = re.compile(rb"^From ([0-9a-f]{40}) ")
HEX_TOKEN = re.compile(r"(?<![0-9A-Za-z])[0-9a-f]{7,40}(?![0-9A-Za-z])")
CLAIM = re.compile(r"\b(every|all)\b[^\n.]{0,120}?\b(commits?|patch(?:es)?)\b", re.I)
COUNT = re.compile(r"\b(\d+)\s+(?:listed\s+)?(commits?|format-patch(?:es)?|patch(?:es| files?)?)\b", re.I)
FIXED = ("REPORT.md", "PROVENANCE.json", "MANIFEST.json")


class BuildError(Exception):
    pass


def git(repo, *args, check=True):
    r = subprocess.run(["git", "-C", repo] + list(args), capture_output=True)
    if check and r.returncode:
        raise BuildError("git %s failed: %s" % (" ".join(args), r.stderr.decode("utf-8", "replace").strip()))
    return r


def resolve_commit(repo, tok):
    r = git(repo, "rev-parse", "--verify", "--quiet", tok + "^{commit}", check=False)
    return r.stdout.decode().strip() if r.returncode == 0 else None


def repo_path(p):
    p = p.replace("\\", "/").strip("/")
    if not p or p.startswith("/") or re.match(r"^[A-Za-z]:", p) or ".." in p.split("/"):
        raise BuildError("unsafe repo path: %r" % p)
    return p


def sha256(b):
    return hashlib.sha256(b).hexdigest()


def write_zip(path, members):
    with zipfile.ZipFile(path, "x", zipfile.ZIP_DEFLATED) as z:
        for name in sorted(members):
            z.writestr(name, members[name])


def read_zip(path):
    with zipfile.ZipFile(path) as z:
        return {n: z.read(n) for n in z.namelist() if not n.endswith("/")}


# ---------------------------------------------------------------------------------------------------------- build

def assemble(spec, repo):
    """Return the member dict for SPEC, with PROVENANCE and MANIFEST derived from the exported members."""
    members = {}
    commits = spec.get("commits") or []
    files = [repo_path(p) for p in spec.get("files") or []]
    receipts = [repo_path(p) for p in spec.get("receipts") or []]
    if not spec.get("report"):
        raise BuildError("spec has no report")
    for p in files:
        members["files/" + p] = git(repo, "show", "HEAD:" + p).stdout
    for p in receipts:
        with open(os.path.join(repo, p), "rb") as f:
            members["receipts/" + p] = f.read()
    with open(os.path.join(repo, repo_path(spec["report"])), "rb") as f:
        members["REPORT.md"] = f.read()

    prov, seen, n = [], set(), 0
    for c in commits:
        sha = resolve_commit(repo, str(c.get("sha", "")))
        if not sha:
            raise BuildError("spec commit %r does not resolve to a commit" % c.get("sha"))
        if sha in seen:
            raise BuildError("spec lists commit %s twice" % sha)
        seen.add(sha)
        rep = c.get("representation")
        entry = {"sha": sha, "representation": rep, "members": []}
        if rep == "FORMAT_PATCH":
            n += 1
            name = "patches/%04d-%s.patch" % (n, sha[:9])
            members[name] = git(repo, "format-patch", "-1", "--stdout", sha).stdout
            entry["members"].append(name)
        elif rep == "FINAL_SNAPSHOT":
            touched = git(repo, "diff-tree", "--root", "--no-commit-id", "--name-only", "-r", "-z", sha).stdout
            touched = {t.decode("utf-8") for t in touched.split(b"\0") if t}
            entry["members"] = sorted("files/" + p for p in files if p in touched)
        elif rep == "RECEIPT_ONLY":
            entry["reason"] = c.get("reason") or ""
        if c.get("reason") and "reason" not in entry:
            entry["reason"] = c["reason"]
        prov.append(entry)
    members["PROVENANCE.json"] = json.dumps({"commits": prov}, indent=1).encode("utf-8")
    members["MANIFEST.json"] = manifest_bytes(members)
    return members


def manifest_bytes(members):
    return json.dumps({n: sha256(b) for n, b in sorted(members.items()) if n != "MANIFEST.json"},
                      indent=1).encode("utf-8")


def build(spec_path, out, repo):
    if os.path.exists(out):
        raise BuildError("refusing to overwrite existing %s" % out)
    with open(spec_path, encoding="utf-8") as f:
        spec = json.load(f)
    members = assemble(spec, repo)
    tmp = out + ".tmp-%d" % os.getpid()
    if os.path.exists(tmp):
        raise BuildError("temporary path %s already exists" % tmp)
    write_zip(tmp, members)
    problems = verify(tmp, repo)
    if problems:
        os.remove(tmp)
        raise BuildError("package failed verify, not written:\n  " + "\n  ".join(problems))
    if os.path.exists(out):
        os.remove(tmp)
        raise BuildError("refusing to overwrite existing %s" % out)
    os.rename(tmp, out)
    return members


# --------------------------------------------------------------------------------------------------------- verify

def verify(zip_path, repo):
    try:
        members = read_zip(zip_path)
    except (OSError, zipfile.BadZipFile) as e:
        return ["X_STRUCTURE: cannot read %s: %s" % (zip_path, e)]
    return verify_members(members, repo)


def verify_members(members, repo):
    P = []
    for name in FIXED:
        if name not in members:
            P.append("X_STRUCTURE: %s is missing" % name)
    try:
        manifest = json.loads(members.get("MANIFEST.json", b"{}"))
        if not isinstance(manifest, dict):
            raise ValueError("not an object")
    except ValueError as e:
        P.append("X_STRUCTURE: MANIFEST.json unreadable (%s)" % e)
        manifest = {}
    try:
        prov = json.loads(members.get("PROVENANCE.json", b"{}")).get("commits", [])
        if not isinstance(prov, list):
            raise ValueError("commits is not a list")
    except (ValueError, AttributeError) as e:
        P.append("X_STRUCTURE: PROVENANCE.json unreadable (%s)" % e)
        prov = []
    report = members.get("REPORT.md", b"").decode("utf-8", "replace")

    # (f) manifest
    for name, b in sorted(members.items()):
        if name == "MANIFEST.json":
            continue
        if name not in manifest:
            P.append("F_MANIFEST: member %s is not in MANIFEST.json" % name)
        elif manifest[name] != sha256(b):
            P.append("F_MANIFEST: hash of %s disagrees with MANIFEST.json" % name)
    for name in sorted(manifest):
        if name not in members:
            P.append("F_MANIFEST: MANIFEST.json lists %s, which is not in the zip" % name)

    # PROVENANCE entries: (d), (b), (g), members
    shas, listed = set(), set()
    for i, e in enumerate(prov):
        if not isinstance(e, dict):
            P.append("X_STRUCTURE: PROVENANCE entry %d is not an object" % i)
            continue
        sha = str(e.get("sha", ""))
        tag = "PROVENANCE entry %d (%s)" % (i, sha[:12] or "no sha")
        if not re.fullmatch(r"[0-9a-f]{40}", sha):
            P.append("X_STRUCTURE: %s has no full 40-hex sha" % tag)
        elif sha in shas:
            P.append("X_STRUCTURE: %s duplicates an earlier entry" % tag)
        shas.add(sha)
        rep = e.get("representation")
        ms = e.get("members") or []
        listed.update(ms)
        for m in ms:
            if m not in members:
                P.append("X_STRUCTURE: %s lists member %s, which is not in the zip" % (tag, m))
        if rep not in REPRESENTATIONS:
            P.append("D_BAD_REPRESENTATION: %s has %s representation" % (tag, "no" if rep is None else "unknown %r" % rep))
        elif rep == "FORMAT_PATCH":
            patches = [m for m in ms if m.startswith("patches/") and m in members]
            if not patches:
                P.append("B_PATCH_MISSING: %s is FORMAT_PATCH but has no patch member" % tag)
            for m in patches:
                fm = FROM_LINE.match(members[m])
                if not fm or fm.group(1).decode() != sha:
                    P.append("B_PATCH_FROM_MISMATCH: %s patch %s has From %s" %
                             (tag, m, fm.group(1).decode() if fm else "(no From line)"))
        elif rep == "FINAL_SNAPSHOT":
            if not [m for m in ms if m.startswith("files/") and m in members]:
                P.append("G_SNAPSHOT_NO_FILE: %s is FINAL_SNAPSHOT but names no files/ member" % tag)
        elif rep == "RECEIPT_ONLY" and not str(e.get("reason") or "").strip():
            P.append("D_BAD_REPRESENTATION: %s is RECEIPT_ONLY with no reason" % tag)

    # (c), (e) every patch member
    for name in sorted(n for n in members if n.startswith("patches/")):
        if name not in listed:
            P.append("C_STRAY_PATCH: %s is not listed by any PROVENANCE entry" % name)
        pm = PATCH_NAME.match(name)
        fm = FROM_LINE.match(members[name])
        if not pm:
            P.append("E_NAME_SHA_MISMATCH: %s is not named patches/NNNN-<sha9>.patch" % name)
        elif not fm or not fm.group(1).decode().startswith(pm.group(2)):
            P.append("E_NAME_SHA_MISMATCH: %s names %s but its From line is %s" %
                     (name, pm.group(2), fm.group(1).decode() if fm else "(missing)"))

    # (a) report cites
    if repo:
        cache = {}
        for tok in sorted(set(HEX_TOKEN.findall(report))):
            full = cache.setdefault(tok, resolve_commit(repo, tok))
            if full and full not in shas:
                P.append("A_UNPROVENANCED_CITE: REPORT.md cites %s (commit %s), which has no PROVENANCE entry" %
                         (tok, full[:12]))
    else:
        P.append("X_STRUCTURE: no repository given, report cites cannot be resolved")

    # overclaim rule
    reps = [e.get("representation") for e in prov if isinstance(e, dict)]
    n_fp = sum(1 for r in reps if r == "FORMAT_PATCH")
    n_patch = sum(1 for n in members if n.startswith("patches/"))
    for line in report.splitlines():
        if "format-patch" not in line.lower() and "format patch" not in line.lower():
            continue
        if CLAIM.search(line) and n_fp != len(reps):
            P.append("R_OVERCLAIM: REPORT.md claims every/all commits are format-patches (%r) but %d of %d PROVENANCE "
                     "commits are FORMAT_PATCH" % (line.strip()[:120], n_fp, len(reps)))
        for cm in COUNT.finditer(line):
            k, what = int(cm.group(1)), cm.group(2).lower()
            want = len(reps) if what.startswith("commit") else n_patch
            if k != want:
                P.append("R_OVERCLAIM: REPORT.md states %d %s (%r) but the package has %d" %
                         (k, what, line.strip()[:120], want))
    return P


# ------------------------------------------------------------------------------------------------------ self-test

def _rmtree(path):
    def onerr(func, p, _exc):
        os.chmod(p, stat.S_IWRITE)
        func(p)
    shutil.rmtree(path, onerror=onerr)


def self_test():
    root = tempfile.mkdtemp(prefix="return_package_selftest_")
    fails = []

    def check(label, ok):
        print("%s  %s" % ("ok  " if ok else "FAIL", label))
        if not ok:
            fails.append(label)

    try:
        repo = os.path.join(root, "repo")
        os.mkdir(repo)
        g = lambda *a: git(repo, "-c", "user.name=selftest", "-c", "user.email=", *a)
        g("init", "-q")

        def commit(path, text, msg):
            full = os.path.join(repo, path)
            os.makedirs(os.path.dirname(full) or repo, exist_ok=True)
            with open(full, "w", encoding="utf-8", newline="\n") as f:
                f.write(text)
            g("add", path)
            g("commit", "-q", "-m", msg)
            return git(repo, "rev-parse", "HEAD").stdout.decode().strip()

        c1 = commit("a.txt", "alpha\n", "c1 add a")
        c2 = commit("docs/b.md", "beta\n", "c2 add b")
        c3 = commit("c.txt", "gamma\n", "c3 add c")
        c4 = commit("d.txt", "delta\n", "c4 add d (never packaged)")
        with open(os.path.join(repo, "receipt.txt"), "w", encoding="utf-8") as f:
            f.write("receipt for c3\n")

        def write_report(text):
            with open(os.path.join(repo, "REPORT-src.md"), "w", encoding="utf-8", newline="\n") as f:
                f.write(text)

        good_report = ("# Report\n\nCommit %s is included as a format-patch; %s is carried by the final snapshot of "
                       "docs/b.md; %s is receipt-only.\nThis package holds 3 commits and 1 patch.\n"
                       % (c1[:9], c2[:10], c3[:12]))
        write_report(good_report)
        spec = {"commits": [{"sha": c1[:9], "representation": "FORMAT_PATCH", "reason": "full history"},
                            {"sha": c2, "representation": "FINAL_SNAPSHOT", "reason": "only final state matters"},
                            {"sha": c3, "representation": "RECEIPT_ONLY", "reason": "content superseded"}],
                "files": ["docs/b.md"], "receipts": ["receipt.txt"], "report": "REPORT-src.md"}
        spec_path = os.path.join(root, "spec.json")
        with open(spec_path, "w", encoding="utf-8") as f:
            json.dump(spec, f)

        good_zip = os.path.join(root, "good.zip")
        try:
            build(spec_path, good_zip, repo)
            built = True
        except BuildError as e:
            print("   ", e)
            built = False
        check("correct package builds and is VERIFIED", built and not verify(good_zip, repo))
        base = read_zip(good_zip) if built else {}

        try:
            build(spec_path, good_zip, repo)
            check("build refuses an existing target", False)
        except BuildError as e:
            check("build refuses an existing target", "refusing to overwrite" in str(e))

        def variant(label, rule, mutate, remanifest=True):
            m = {k: v for k, v in base.items()}
            mutate(m)
            if remanifest:
                m["MANIFEST.json"] = manifest_bytes(m)
            problems = verify_members(m, repo)
            hit = [p for p in problems if p.startswith(rule)]
            check("%s -> %s" % (label, rule), bool(hit))

        def prov_edit(fn):
            def mutate(m):
                d = json.loads(m["PROVENANCE.json"])
                fn(d["commits"], m)
                m["PROVENANCE.json"] = json.dumps(d, indent=1).encode()
            return mutate

        pname = "patches/0001-%s.patch" % c1[:9]

        variant("(a) report cites a commit with no PROVENANCE entry", "A_UNPROVENANCED_CITE",
                lambda m: m.__setitem__("REPORT.md", m["REPORT.md"] + ("Also see %s.\n" % c4[:8]).encode()))
        variant("(b) FORMAT_PATCH entry with its patch removed", "B_PATCH_MISSING",
                prov_edit(lambda c, m: (m.pop(pname), c[0].__setitem__("members", []))))
        variant("(b) patch From line names another commit", "B_PATCH_FROM_MISMATCH",
                lambda m: m.__setitem__(pname, m[pname].replace(c1.encode(), c3.encode(), 1)))
        variant("(c) patch member not in PROVENANCE", "C_STRAY_PATCH",
                lambda m: m.__setitem__("patches/0002-%s.patch" % c4[:9],
                                        git(repo, "format-patch", "-1", "--stdout", c4).stdout))
        variant("(d) unknown representation", "D_BAD_REPRESENTATION",
                prov_edit(lambda c, m: c[2].__setitem__("representation", "PATCHISH")))
        variant("(d) missing representation", "D_BAD_REPRESENTATION",
                prov_edit(lambda c, m: c[2].pop("representation")))

        def rename_patch(c, m):
            bad = "patches/0001-%s.patch" % c3[:9]
            m[bad] = m.pop(pname)
            c[0]["members"] = [bad]
        variant("(e) patch name sha9 disagrees with From line", "E_NAME_SHA_MISMATCH", prov_edit(rename_patch))
        variant("(f) member changed without MANIFEST update", "F_MANIFEST",
                lambda m: m.__setitem__("files/docs/b.md", b"tampered\n"), remanifest=False)
        variant("(f) member missing from MANIFEST", "F_MANIFEST",
                lambda m: m.__setitem__("files/extra.txt", b"x\n"), remanifest=False)
        variant("(g) FINAL_SNAPSHOT names no file member", "G_SNAPSHOT_NO_FILE",
                prov_edit(lambda c, m: c[1].__setitem__("members", [])))
        variant("(overclaim) 'every listed commit ... format-patch' with non-patch commits", "R_OVERCLAIM",
                lambda m: m.__setitem__("REPORT.md", m["REPORT.md"] +
                                        b"Every listed commit is included as a format-patch.\n"))
        variant("(overclaim) stated patch count disagrees", "R_OVERCLAIM",
                lambda m: m.__setitem__("REPORT.md", m["REPORT.md"] + b"It carries 3 format-patches.\n"))

        # the original defect end to end: report cites a commit the builder never exported
        write_report(good_report + "Every listed commit is included as a format-patch, including %s.\n" % c4[:9])
        bad_zip = os.path.join(root, "bad.zip")
        try:
            build(spec_path, bad_zip, repo)
            check("build refuses a report that cites an unexported commit and overclaims", False)
        except BuildError as e:
            s = str(e)
            check("build refuses a report that cites an unexported commit and overclaims",
                  "A_UNPROVENANCED_CITE" in s and "R_OVERCLAIM" in s and not os.path.exists(bad_zip)
                  and not os.path.exists(bad_zip + ".tmp-%d" % os.getpid()))
    finally:
        _rmtree(root)
    print("self-test: %d failure(s)" % len(fails))
    return 1 if fails else 0


# ----------------------------------------------------------------------------------------------------------- main

def default_repo():
    r = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True)
    return r.stdout.decode().strip() if r.returncode == 0 else None


def main(argv):
    if argv == ["--self-test"]:
        return self_test()
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build")
    b.add_argument("--spec", required=True)
    b.add_argument("--out", required=True)
    b.add_argument("--repo")
    v = sub.add_parser("verify")
    v.add_argument("zip")
    v.add_argument("--repo")
    a = ap.parse_args(argv)
    repo = a.repo or default_repo()
    if not repo:
        print("not in a git repository; pass --repo", file=sys.stderr)
        return 2
    if a.cmd == "build":
        try:
            members = build(a.spec, a.out, repo)
        except BuildError as e:
            print("NOT BUILT: %s" % e, file=sys.stderr)
            return 1
        print("VERIFIED %s (%d members)" % (a.out, len(members)))
        return 0
    problems = verify(a.zip, repo)
    for p in problems:
        print(p)
    print(("FAILED: %d problem(s)" % len(problems)) if problems else "VERIFIED %s" % a.zip)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
