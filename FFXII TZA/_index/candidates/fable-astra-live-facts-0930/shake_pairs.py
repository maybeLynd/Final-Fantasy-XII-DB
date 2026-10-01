# shake_pairs.py - MT-CURSOR takeback (authored data): in the shipped decompiled scripts (corpus/us/*.txt, the corpus
# camerashake_census.py uses), is every camerashakestart followed LATER IN THE SAME SCRIPT FILE by a camerashakestop or
# camerashakeclear? File order is only a proxy for execution order; a start with no later stop/clear anywhere in its
# file is the case that can leave a finished shake drawing MT words until the world-tick reset 0037D890 or area exit.
# Control: totals must equal the committed census (328 starts, 315 clears, 178 stops).
import os, re, collections
CORPUS = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\pub140-scratch\corpus\us"
call = re.compile(r"\b(camerashake[a-z_0-9]*)\(([^)]*)\)")
tot = collections.Counter()
unpaired = []
files_with_start = 0
for fn in sorted(os.listdir(CORPUS)):
    if not fn.endswith(".txt"):
        continue
    t = open(os.path.join(CORPUS, fn), encoding="utf-8", errors="replace").read()
    ev = []
    for m in call.finditer(t):
        v = m.group(1)
        kind = ("start" if v.startswith("camerashakestart") else "stop" if v.startswith("camerashakestop")
                else "clear" if v.startswith("camerashakeclear") else "other")
        tot[kind] += 1
        ev.append((m.start(), kind, v, t.count("\n", 0, m.start()) + 1))
    starts = [e for e in ev if e[1] == "start"]
    if not starts:
        continue
    files_with_start += 1
    for s in starts:
        later = [e for e in ev if e[0] > s[0] and e[1] in ("stop", "clear")]
        if not later:
            unpaired.append((fn, s[3], s[2]))
print("totals", dict(tot), "| CONTROL census 328 starts, 315 clears, 178 stop_19e + 2 plain stop:",
      "PASS" if (tot["start"], tot["clear"], tot["stop"]) == (328, 315, 178 + 2) else "MISMATCH")
print("script files with a start:", files_with_start)
print("starts with NO later stop/clear in the same file:", len(unpaired))
for u in unpaired[:40]:
    print("  %s line %d %s" % u)
