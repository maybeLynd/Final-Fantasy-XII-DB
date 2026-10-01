"""SWE2-AUDIT-SEM: the register rows that cite gitignored Tools/work paths or _experiments/EXP-*.md files, with each
row's state as documented_rule reads it (closed or open), and whether each cited _experiments file is tracked."""
import os, re, sys, io, subprocess
HERE = r"C:\Users\Kristian\source\repos\XIIOnline\Database\FFXII TZA\_index\candidates\status-currency-ruling-fable"
sys.path.insert(0, HERE)
import documented_rule as D
t = io.open(os.path.join(D.DB, "_index", "OPEN-QUESTIONS.md"), encoding="utf-8", errors="replace").read()
tracked = D.tracked_paths()
for rid, cell in re.findall(r"^\|\s*([A-Z][A-Za-z0-9/\-]*)\s*\|(.*)$", t, re.M):
    tw = re.findall(r"Tools/work/[^\s`)|,]+", cell)
    ex = [p.rstrip(".") for p in re.findall(r"_experiments/(?!evidence/)[^\s`)|,]+", cell)]
    if not (tw or ex):
        continue
    status = cell.split("|")[-2].strip()[:60] if cell.count("|") >= 2 else cell[:60]
    closed = bool(re.search(r"\b(ANSWERED|SUPERSEDED|WITHDRAWN|CLOSED|NO ADMISSIBLE SOURCE|OUT OF EVIDENCE BOUNDARY)\b", cell))
    extr = [(p, p in tracked) for p in ex]
    print("%-8s closed-word:%-5s Tools/work:%s  _experiments:%s" % (rid, closed, tw[:2], extr[:2]))
