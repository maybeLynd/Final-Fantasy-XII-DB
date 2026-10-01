"""sign_check.py - OPUS (Claude Opus 5.5), 2026-09-28: non-author review of FABLE's UQ-38 OUT OF EVIDENCE BOUNDARY package
(../uq38-oeb-package/, FABLE-REQ-OPUS-SIGN-OEB-UQ38). STATIC, certified EXE only.

  K1 FABLE's own check re-run unchanged: uq38_provenance.py P1 / P2 / P3 (exit 0)
  O1 the discriminator FABLE suggested - SECTION ORDERING - tested: MSVC links an object's functions contiguously, so
     if authoring class were a per-object (per-source-file) fact, runs of consecutive listed functions that are all
     members would be class-pure. They are not: runs holding both a whole-shaped member and an agreed-C member exist
     (e.g. `CUWW` at 0044A620, `CCW` at 005188C0), so link order does not partition the members by class, and cannot
     supply the provenance the residue asks for
  B1 the row's bracket recounted from the two instruments' own columns (uq38_carry.tsv: `frontier` = FRONTIER's
     census, `verdict` = ee_member_calls): whole 47; BOTH instruments C+fragments 31 - not 41: of FRONTIER's 41
     C+fragments, 5 are 'whole' and 5 'mostly' under ee_member_calls, so the stated 47 / 41 / 95 counts 5 members twice
Exit 0 when K1 and O1 hold; B1 prints the recount (the correction is a condition of the signature, not a failure).
"""
import collections, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); CAND = os.path.abspath(os.path.join(HERE, ".."))
ROOT = os.path.abspath(os.path.join(CAND, "..", "..", ".."))
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
r = subprocess.run([sys.executable, os.path.join(CAND, "uq38-oeb-package", "uq38_provenance.py")], capture_output=True, text=True)
check("K1", r.returncode == 0 and r.stdout.count("PASS") >= 3, "uq38_provenance.py exit %d: %s" %
      (r.returncode, " | ".join(l[:60] for l in r.stdout.splitlines() if l.startswith(("PASS", "FAIL")))))
T = [l.rstrip("\n").split("\t") for l in open(os.path.join(CAND, "uq38-carry-criterion", "uq38_carry.tsv"), encoding="utf-8")][1:]
cls = {}
for f, verdict, frontier in ((t[0], t[1], t[2]) for t in T):
    cls[f] = "W" if verdict == "whole" else "C" if (verdict, frontier) == ("C+fragments", "C+fragments") else \
             "U" if (verdict, frontier) == ("C+fragments", "translated") else "o"
fn = []
for l in open(os.path.join(ROOT, "Tools", "work", "graph", "functions.tsv"), encoding="utf-8"):
    c = l.split("\t")
    try: fn.append("%08X" % int(c[0], 16))
    except ValueError: pass
fn.sort(key=lambda h: int(h, 16))
runs, cur = [], []
for h in fn:
    if h in cls: cur.append(h)
    elif cur: runs.append(cur); cur = []
if cur: runs.append(cur)
mixed = [(r[0], "".join(cls[x] for x in r)) for r in runs if {"W", "C"} <= {cls[x] for x in r}]
check("O1", sum(len(r) for r in runs) == 267 and len(mixed) >= 2 and ("0044A620", "CUWW") in mixed and ("005188C0", "CCW") in mixed,
      "%d member runs; %d hold both a whole-shaped and an agreed-C member: %s" % (len(runs), len(mixed), mixed))
pair = collections.Counter((t[2], t[1]) for t in T)
fc = {k[1]: v for k, v in pair.items() if k[0] == "C+fragments"}
print("B1  bracket recount: whole %d; both instruments C+fragments %d; FRONTIER C+fragments by ee_member_calls %s; "
      "disagreements (FRONTIER translated, ee C+fragments) %d"
      % (sum(v for k, v in pair.items() if k[1] == "whole"), pair[("C+fragments", "C+fragments")], fc,
         pair[("translated", "C+fragments")]))
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
