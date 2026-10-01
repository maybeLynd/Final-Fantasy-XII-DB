"""Authored uses of the three party-control lock calls in the decompiled us scripts:
  0x03C0 setuclockstatus(on)             -> 00359200(on, bit 0)   movement-suppression dword 022C8000
  0x03E1 setucpcmovelockstatus(bit, on)  -> 00359250(bit, on)     owner byte 0 of the four at 022C8004
  0x2084 debug_TkRequireUCPCMoveLockStatus(bit, on) -> 003592C0   owner byte 1

Input: the BQ-10 decompile of every shipped us script (1,114 *.txt), kept in the gitignored
Database/Tools/work/FABLE/pub140-scratch/corpus/us/ (set FF12_CORPUS to override).
Positive control: mapsoundplay( is counted in the same files.
FABLE, 2026-09-19.
"""
import os, re, collections

HERE = os.path.dirname(os.path.abspath(__file__))
CORPUS = os.environ.get("FF12_CORPUS", os.path.join(HERE, "../../../../Tools/work/FABLE/pub140-scratch/corpus/us"))
files = sorted(f for f in os.listdir(CORPUS) if f.endswith(".txt"))
print("scripts:", len(files))
pat = re.compile(r"(setuclockstatus|setucpcmovelockstatus|debug_TkRequireUCPCMoveLockStatus|unkCall_3c0|unkCall_3e1|unkCall_2084)\(([^)]*)\)")
uses = collections.Counter(); where = collections.defaultdict(list); control = 0
for f in files:
    actor = fn = None
    for line in open(os.path.join(CORPUS, f), encoding="utf-8", errors="replace"):
        control += line.count("mapsoundplay(")
        m = re.match(r"^actor (\S+)", line)
        if m:
            actor = m.group(1)
        m = re.match(r"^\tfunction (\S+)", line)
        if m:
            fn = m.group(1)
        for name, args in pat.findall(line):
            uses[(name, args)] += 1
            where[(f, actor, fn)].append("%s(%s)" % (name, args))
print("control: mapsoundplay( occurrences:", control)
print("uses by call and arguments:")
for k, n in sorted(uses.items()):
    print("   %s(%s): %d" % (k[0], k[1], n))
print("files with a use:", sorted({k[0] for k in where}))
for (f, actor, fn), calls in sorted(where.items()):
    print("  %s, actor %s, function %s: %s" % (f, actor, fn, ", ".join(calls)))
