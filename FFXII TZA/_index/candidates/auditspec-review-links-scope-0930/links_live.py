"""links_live.py - SWE2-AUDIT-SPEC census of what 145ac7e3b's three scope corrections exempt at HEAD.

Independent scanner (does not import check_links.py): reads every .md blob under `Database/FFXII TZA` at HEAD via
git, extracts links the way the checker does (fence strip; LINK regex), and splits the exemptions by correction:
  A  links in files under _experiments/evidence/<pkg>/<subdir>/  - resolved against the HEAD tree; each such file is
     tagged CAPTURE if its blob id also occurs outside _experiments/evidence at HEAD or in any ancestor commit's tree
     at a non-evidence path (a real byte-exact capture), else UNMATCHED (possibly authored in place)
  B  links present before code-span blanking and absent after it
  C  links whose target changes under urllib.parse.unquote
For every exempted link it reports whether the target resolves (exact-case) in the HEAD tree.
"""
import os, re, subprocess, sys, urllib.parse, posixpath, collections
REPO = r"C:\Users\Kristian\source\repos\XIIOnline"
PFX = "Database/FFXII TZA/"
LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
FENCE = re.compile(r"```.*?```", re.S)
CODE_SPAN = re.compile(r"`[^`\n]*`")
def git(*a, inp=None):
    return subprocess.run(["git", "-C", REPO] + list(a), input=inp, capture_output=True).stdout
tree = git("ls-tree", "-r", "HEAD", "--", PFX).decode("utf-8", "replace").splitlines()
files, blob_of = set(), {}
for l in tree:
    meta, path = l.split("\t", 1)
    if path.startswith('"'): path = path.strip('"').encode().decode("unicode_escape").encode("latin-1").decode("utf-8")
    files.add(path); blob_of[path] = meta.split()[2]
dirs = {posixpath.dirname(p) for p in files}
for d in list(dirs):
    while d:
        dirs.add(d); d = posixpath.dirname(d)
def exists(p): return p in files or p in dirs
def resolve(src, t):
    return posixpath.normpath(posixpath.join(posixpath.dirname(src), t))
# blob ids outside evidence, at HEAD and in history (rev-list --objects over all commits touching PFX)
outside = {b for p, b in blob_of.items() if "/_experiments/evidence/" not in p}
hist = git("rev-list", "--objects", "HEAD", "--", PFX).decode("utf-8", "replace").splitlines()
for l in hist:
    parts = l.split(" ", 1)
    if len(parts) == 2 and parts[1].endswith(".md") and "_experiments/evidence/" not in parts[1]:
        outside.add(parts[0])
md = sorted(p for p in files if p.endswith(".md"))
BASE_OUT = {posixpath.basename(q) for q in files if "/_experiments/evidence/" not in q}
batch = git("cat-file", "--batch", inp=("\n".join(blob_of[p] for p in md) + "\n").encode())
texts, pos = {}, 0
for p in md:
    hdr_end = batch.index(b"\n", pos); size = int(batch[pos:hdr_end].split()[2])
    texts[p] = batch[hdr_end + 1:hdr_end + 1 + size].decode("utf-8", "replace"); pos = hdr_end + 1 + size + 1
def is_ext(t): return t.startswith(("http://", "https://", "#", "mailto:"))
A = collections.Counter(); Afiles = collections.defaultdict(list); B, C = [], []
for p in md:
    rel = p[len(PFX):].split("/")
    t0 = FENCE.sub("", texts[p])
    t1 = CODE_SPAN.sub(lambda c: " " * len(c.group(0)) if "](" in c.group(0) else c.group(0), t0)
    cap = len(rel) >= 5 and rel[0] == "_experiments" and rel[1] == "evidence"   # file inside pkg/<subdir>/
    links1 = [m.group(1).strip() for m in LINK.finditer(t1)]
    if cap:
        base_out = BASE_OUT
        kind = ("CAPTURE" if blob_of[p] in outside else
                "MIRROR" if ("/Database/FFXII TZA/" in p[len(PFX):] or posixpath.basename(p) in base_out) else
                "UNMATCHED")
        for t in links1:
            if is_ext(t): continue
            tt = urllib.parse.unquote(t.split("#", 1)[0])
            if not tt: continue
            ok = exists(resolve(p, tt)); A[(kind, ok)] += 1
            if not ok: Afiles[kind].append((p, t))
        continue
    s1 = collections.Counter(links1)
    for m in LINK.finditer(t0):
        t = m.group(1).strip()
        if s1[t] > 0: s1[t] -= 1; continue
        if is_ext(t): continue
        tt = t.split("#", 1)[0]
        B.append((p, t, exists(resolve(p, urllib.parse.unquote(tt))) if tt else True))
    for t in links1:
        if is_ext(t): continue
        tt = t.split("#", 1)[0]
        if tt and urllib.parse.unquote(tt) != tt:
            C.append((p, t, exists(resolve(p, tt)), exists(resolve(p, urllib.parse.unquote(tt)))))
print("HEAD %s; .md files %d" % (git("rev-parse", "--short", "HEAD").decode().strip(), len(md)))
print("A captures (subdirectory files): links by (file kind, target resolves):", dict(A))
ua = sorted({p for p, _ in Afiles["UNMATCHED"]})
print("A UNMATCHED files with broken links: %d files, %d links" % (len(ua), len(Afiles["UNMATCHED"])))
bn = collections.Counter(posixpath.basename(p) for p in ua)
print("A UNMATCHED broken-link files by basename (top):", bn.most_common(12))
for p in ua[:25]: print("    UNMATCHED file:", p[len(PFX):], "(%d broken)" % sum(1 for q, _ in Afiles["UNMATCHED"] if q == p))
print("B lines (code-span exemptions that RESOLVE, i.e. real links blanked):")
for p, t, ok in B:
    if ok:
        for ln in texts[p].splitlines():
            if "(" + t + ")" in ln: print("    %s: %s" % (p[len(PFX):], ln.strip()[:170])); break
authored = [(p, t) for p, t in Afiles["UNMATCHED"] if re.match(r"(README|RESULT|PLAN|NOTES|METHODS|SUMMARY|REPORT|REVIEW)", posixpath.basename(p), re.I)]
print("A UNMATCHED broken links in files named README/RESULT/PLAN/NOTES/METHODS/SUMMARY/REPORT/REVIEW: %d" % len(authored))
for p, t in authored[:12]: print("   ", p[len(PFX):], "->", t)
print("B code-span exemptions: %d (resolving %d)" % (len(B), sum(1 for b in B if b[2])))
for p, t, ok in B: print("   ", p[len(PFX):], "->", t[:60], "resolves" if ok else "missing")
print("C percent-decoded targets: %d" % len(C))
for p, t, raw, dec in C: print("   ", p[len(PFX):], "->", t[:70], "raw-exists=%s decoded-exists=%s" % (raw, dec))
