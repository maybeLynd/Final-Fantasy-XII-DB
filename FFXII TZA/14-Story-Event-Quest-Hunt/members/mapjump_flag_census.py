"""Census of the map-jump-group flag verbs in the decompiled `us` scripts.

For every literal id passed to setmapjumpgroupflag / releasemapjumpgroupflag / ismapjumpgroupflag (the three script
verbs over the Primary persistent bank): how often each verb uses it, in how many scripts, which script areas
(the file-name prefix before the first underscore), and whether mapjumpgroupinit.bin pre-sets it on a new game.
Ids of 0x4000 and above are threshold queries, not flag reads, and are listed separately at the end.
"""
import os, re, sys, struct, collections

CORPUS = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\pub140-scratch\corpus\us"
INIT = r"D:\FFXII_TZA_extract\ps2data\image\ff12\us\bin\mapjumpgroupinit.bin"
b = open(INIT, "rb").read()
n = struct.unpack_from("<H", b, 8)[0]
init = {i for i in struct.unpack_from("<%dH" % n, b, 10) if 2 <= i <= 0x1FF}

pat = re.compile(r"\b(set|release|is)mapjumpgroupflag\((0x[0-9a-fA-F]+|\d+)\)")
nonlit = collections.Counter()
use = collections.defaultdict(lambda: collections.Counter())
files = collections.defaultdict(set)
areas = collections.defaultdict(collections.Counter)
any_call = re.compile(r"\b(set|release|is)mapjumpgroupflag\(")
for fn in sorted(os.listdir(CORPUS)):
    if not fn.endswith(".txt"):
        continue
    t = open(os.path.join(CORPUS, fn), encoding="utf-8", errors="replace").read()
    total = len(any_call.findall(t))
    lit = 0
    for m in pat.finditer(t):
        v = m.group(2)
        i = int(v, 16) if v.lower().startswith("0x") else int(v)
        use[i][m.group(1)] += 1
        files[i].add(fn)
        areas[i][fn.split("_")[0]] += 1
        lit += 1
    if total - lit:
        nonlit[fn] = total - lit

flags = sorted(i for i in use if i < 0x4000)
thr = sorted(i for i in use if i >= 0x4000)
print("# scripts scanned %d; literal-id calls %d; calls with a computed id %d in %d scripts"
      % (len([f for f in os.listdir(CORPUS) if f.endswith('.txt')]), sum(sum(c.values()) for c in use.values()),
         sum(nonlit.values()), len(nonlit)))
print("# distinct flag ids %d (of which pre-set on a new game %d of %d); distinct threshold-query ids %d"
      % (len(flags), len(init & set(flags)), len(init), len(thr)))
print("# pre-set ids no script names literally: " + " ".join("0x%X" % i for i in sorted(init - set(flags))))
print("id\tpreset\tset\trelease\tis\tscripts\tareas")
for i in flags + thr:
    c = use[i]
    ar = ", ".join("%s %d" % kv for kv in sorted(areas[i].items(), key=lambda kv: (-kv[1], kv[0]))[:6])
    print("0x%X\t%s\t%d\t%d\t%d\t%d\t%s" % (i, "yes" if i in init else ("threshold" if i >= 0x4000 else ""),
                                          c["set"], c["release"], c["is"], len(files[i]), ar))
