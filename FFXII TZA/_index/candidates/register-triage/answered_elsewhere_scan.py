"""answered_elsewhere_scan.py - list OPEN / PARTIAL / BLOCKED register rows whose id appears on a page line together with
an answer word (FABLE, Claude Opus 5.5, 2026-09-26).

Why: a row can stay OPEN in OPEN-QUESTIONS.md while a page already answers it, often under ANOTHER id (PH-4 was
answered as CU-4; AA-2 as UQ-138) or in a section a peer added (RS-1, SWE2-DATA). check_questions compares boxes
with rows by id only, so neither case reaches it.
Output: candidates, never verdicts. Every hit must be read, and most are "narrowed, not answered" or an answer to a
neighbouring id. Of today's 25 hits, four were real (PH-4, RS-1, J-4, AA-2), found by reading.
Usage: python answered_elsewhere_scan.py [--db "Database/FFXII TZA"]
"""
import argparse, importlib.util, os, re, sys
ap = argparse.ArgumentParser(); ap.add_argument("--db", default="Database/FFXII TZA"); a = ap.parse_args()
KIT = os.path.join(os.path.dirname(a.db.rstrip("/\\")), "Tools", "analysis-kit", "gfz-scripts", "check_questions.py")
spec = importlib.util.spec_from_file_location("cq", KIT); cq = importlib.util.module_from_spec(spec)
sys.argv = ["x"]; spec.loader.exec_module(cq)
openids = {}
for l in open(os.path.join(a.db, "_index", "OPEN-QUESTIONS.md"), encoding="utf-8"):
    m = re.match(r"\| ([A-Z]+-\d+[a-z]?(?:/[a-z])?) \|", l)
    if m:
        c = cq.classify(l[2:])[0]
        if c in ("OPEN", "PARTIAL", "BLOCKED"): openids[m.group(1)] = c
ANS = re.compile(r"\b(ANSWERED|answered|CLOSED|RESOLVED|DISPOSITIONED)\b")
hits = {}
for root, dirs, files in os.walk(a.db):
    if "_index" in root.replace("\\", "/").split("/"): continue
    for f in files:
        if not f.endswith(".md"): continue
        p = os.path.join(root, f)
        lines = open(p, encoding="utf-8", errors="replace").read().splitlines()
        for i, line in enumerate(lines):
            # the verdict often sits on the line after the id (a box line, then its answer line)
            line = line + " " + (lines[i + 1] if i + 1 < len(lines) else "")
            if not ANS.search(line): continue
            for q in set(re.findall(r"\b([A-Z]{1,4}-\d+[a-z]?)\b", line)):
                if q in openids and re.search(r"(ANSWERED|answered|CLOSED|RESOLVED|DISPOSITIONED)[^.|]{0,80}\b%s\b|\b%s\b[^.|]{0,80}(ANSWERED|answered|CLOSED|RESOLVED|DISPOSITIONED)"
                                              % (re.escape(q), re.escape(q)), line):
                    hits.setdefault(q, []).append("%s:%d" % (os.path.relpath(p, a.db), i + 1))
print("open/partial/blocked rows:", len(openids), " candidates:", len(hits))
for q in sorted(hits): print("%-8s %-8s %s" % (q, openids[q], "; ".join(hits[q][:3])))
