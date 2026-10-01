"""test_check_links.py - check_links.py's three scope corrections of 2026-09-30, on a fixture tree (OPUS).

  L1  a broken link in an evidence PACKAGE-level file (README.md) is reported      (captures do not hide documents)
  L2  a broken link in a package SUBDIRECTORY (retained/) is not judged, and counted
  L3  link syntax inside an inline code span that contains `](` is not a link
  L4  a link whose label is a code span ([`name`](missing.md)) is still judged and reported
  L5  a %20-encoded target that exists after decoding resolves
  L6  a plain broken link in an ordinary page is reported                          (the gate still bites)
Runs check_links.py --raw --db <fixture> as a subprocess and reads its BROKEN lines.
"""
import os, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
fails = 0


def check(tag, ok, text=""):
    global fails
    fails += not ok
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


def w(root, rel, text):
    p = os.path.join(root, *rel.split("/"))
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(text)


T = tempfile.mkdtemp(prefix="cl_")
w(T, "_experiments/evidence/pkg/README.md", "see [gone](missing-readme-target.md)\n")
w(T, "_experiments/evidence/pkg/retained/page.md", "copy says [x](../../somewhere/else.md)\n")
w(T, "page.md", "code `vtbl[0xD0](+0x6C0, word)` here\nlabel [`name`](missing-label-target.md)\n"
                "spaced [ok](sub%20dir/f.md)\nplain [b](plain-missing.md)\n")
w(T, "sub dir/f.md", "exists\n")
r = subprocess.run([sys.executable, "-B", os.path.join(HERE, "check_links.py"), "--db", T, "--raw"],
                   capture_output=True, text=True)
bad = [l.split("\t") for l in r.stdout.splitlines() if l.startswith("BROKEN\t")]
targets = {b[2] for b in bad}
check("L1", "missing-readme-target.md" in targets, "package README link reported")
check("L2", not any("somewhere/else.md" in t for t in targets), "capture link not judged")
check("L3", not any("+0x6C0" in t for t in targets), "code-span link-like text ignored")
check("L4", "missing-label-target.md" in targets, "code-span label link still judged")
check("L5", not any("sub" in t and "f.md" in t for t in targets), "percent-encoded target resolves")
check("L6", "plain-missing.md" in targets, "plain broken link reported")
check("L7", len(bad) == 3, "exactly three broken: %s" % sorted(targets))
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
