"""Authored uses of call ids 0x05BE (get 0209AC10) and 0x05BF (clear 0209AC10) in the decompiled us scripts.

Input: the BQ-10 decompile of every shipped us script (1,114 *.txt), kept in the gitignored
Database/Tools/work/FABLE/pub140-scratch/corpus/us/ (set FF12_CORPUS to override). The decompiler prints the
two calls as unkCall_5be() / unkCall_5bf(). For each use it reports the enclosing actor and function.
Positive control: mapsoundplay( is counted in the same files.
FABLE, 2026-09-13.
"""
import os, re, collections

HERE = os.path.dirname(os.path.abspath(__file__))
CORPUS = os.environ.get("FF12_CORPUS", os.path.join(HERE, "../../../../Tools/work/FABLE/pub140-scratch/corpus/us"))
files = sorted(f for f in os.listdir(CORPUS) if f.endswith(".txt"))
print("scripts:", len(files))
uses = collections.Counter(); where = collections.Counter(); per_file = collections.Counter(); control = 0
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
        for call in re.findall(r"unkCall_5b[ef]\(\)", line):
            uses[call] += 1
            where[(call, actor, fn)] += 1
            per_file[f] += 1
print("control: mapsoundplay( occurrences:", control)
print("uses:", sorted(uses.items()))
print("files with a use:", len(per_file), "; prefixes:", sorted(collections.Counter(re.sub(r"\d+\.txt$", "", f) for f in per_file).items()))
print("uses per file:", sorted(collections.Counter(per_file.values()).items()))
for (call, actor, fn), n in sorted(where.items()):
    print("  %s in actor %s, function %s: %d" % (call, actor, fn, n))
