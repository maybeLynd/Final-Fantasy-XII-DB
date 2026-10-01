"""Authored uses of the load-mode verb 0x7067 and the stash-flag verb 0x308D, and where field 0x483 is tested.

Input: the BQ-10 decompile of every shipped us script (gitignored Database/Tools/work/FABLE/pub140-scratch/corpus/us,
set FF12_CORPUS to override). Unnamed verbs print as unkCall_<id>().
Reports: every unkCall_7067(<arg>) with its script and enclosing function, the value that selects the argument when
the call sits in a two-way switch, the unkCall_308d count (control: unkCall_308c, the neighbouring id), and the
scripts that compare nowmap() with 0x0483 plus the lowest and highest map id the trial director tests.
FABLE, 2026-09-13.
"""
import os, re, collections

HERE = os.path.dirname(os.path.abspath(__file__))
CORPUS = os.environ.get("FF12_CORPUS", os.path.join(HERE, "../../../../Tools/work/FABLE/pub140-scratch/corpus/us"))
files = sorted(f for f in os.listdir(CORPUS) if f.endswith(".txt"))
print("scripts:", len(files))
c308c = c308d = 0
uses = []
map483 = []
trial_ids = set()
for f in files:
    text = open(os.path.join(CORPUS, f), encoding="utf-8", errors="replace").read()
    c308c += text.count("unkCall_308c(")
    c308d += text.count("unkCall_308d(")
    fn = None
    lines = text.splitlines()
    for i, line in enumerate(lines):
        m = re.match(r"^\tfunction (\S+)", line)
        if m:
            fn = m.group(1)
        for arg in re.findall(r"unkCall_7067\(([^)]*)\)", line):
            ctx = " / ".join(l.strip() for l in lines[max(0, i - 4):i] if l.strip().startswith(("switch", "case", "default")))
            uses.append((f, fn, arg, ctx))
    if "nowmap() == 0x0483" in text:
        map483.append(f)
    if f.startswith("tri_"):
        trial_ids.update(int(x, 16) for x in re.findall(r"nowmap\(\) == (0x[0-9a-f]+)", text))
print("control: unkCall_308c( occurrences:", c308c, "; unkCall_308d( occurrences:", c308d)
print("unkCall_7067 uses:", len(uses))
for u in uses:
    print("  %s in %s: arg %s; preceding switch/case lines: %s" % u)
pre = collections.Counter(re.sub(r"\d+\.txt$", "", f) for f in map483)
print("scripts comparing nowmap() with 0x0483:", len(map483), sorted(pre.items()))
if trial_ids:
    print("map ids the tri_* scripts compare nowmap() with: %d distinct, lowest 0x%04X, highest 0x%04X" % (len(trial_ids), min(trial_ids), max(trial_ids)))
