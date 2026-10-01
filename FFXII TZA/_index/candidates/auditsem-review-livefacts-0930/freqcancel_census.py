"""SWE2-AUDIT-SEM: shipped uses of the cancel verbs whose handlers call ActorResource_RecycleEntryRange 003DB420
(scriptvm-verb-table.tsv: freqcancel 0x4A7 / freqcancel2 0x574 -> 00352980; freqcancel_4a8 / freqcancel2_575 ->
00353660), counted in the decompiled us corpus by argument."""
import glob, os, re, collections
CORPUS = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\pub140-scratch\corpus\us"
c = collections.Counter()
files = collections.defaultdict(set)
for f in glob.glob(os.path.join(CORPUS, "*.txt")):
    for m in re.finditer(r"\b(freqcancel2?(?:_4a8|_575)?)\(([^)]*)\)", open(f, encoding="utf-8", errors="replace").read()):
        c[(m.group(1), m.group(2).strip())] += 1
        files[m.group(1)].add(os.path.basename(f))
for (v, a), n in sorted(c.items(), key=lambda t: -t[1]):
    print("%-18s (%s)  x%d" % (v, a, n))
for v, fs in sorted(files.items()):
    print("%s: %d files, e.g. %s" % (v, len(fs), ", ".join(sorted(fs)[:6])))
print("total:", sum(c.values()))
