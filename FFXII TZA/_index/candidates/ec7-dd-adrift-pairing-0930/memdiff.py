"""memdiff.py REPO_DIR [REV] - for each members file changed vs REV (default HEAD) in the scratch repo, print the
membership difference (first-column addresses), ignoring column-only and line-ending changes."""
import re, subprocess, sys
D = sys.argv[1]
REV = sys.argv[2] if len(sys.argv) > 2 else "HEAD"


def mem(text):
    out, first = set(), True
    for l in text.splitlines():
        l = l.split("#", 1)[0].strip()
        if not l:
            continue
        tok = l.split()[0].replace("0x", "")
        if first:
            first = False
            if not re.fullmatch(r"[0-9A-Fa-f]{6,8}", tok):
                continue
        out.add(tok.upper().zfill(8))
    return out


files = subprocess.run(["git", "-C", D, "diff", "--name-only", REV], capture_output=True, text=True).stdout.split("\n")
for f in filter(None, files):
    old = subprocess.run(["git", "-C", D, "show", "%s:%s" % (REV, f)], capture_output=True, text=True, encoding="utf-8", errors="replace").stdout
    try:
        new = open(D + "/" + f, encoding="utf-8", errors="replace").read()
    except FileNotFoundError:
        new = ""
    if not f.endswith(".tsv"):
        print("NON-TSV changed:", f)
        continue
    a, b = mem(old), mem(new)
    print("%s: %d -> %d  dropped %d %s  admitted %d %s" % (f, len(a), len(b), len(a - b), " ".join(sorted(a - b))[:400],
                                                           len(b - a), " ".join(sorted(b - a))[:400]))
