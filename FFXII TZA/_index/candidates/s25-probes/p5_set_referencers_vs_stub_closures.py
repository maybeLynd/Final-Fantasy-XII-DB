"""P5 (static) - can a stubbed callee of the walk write the order set (the subgroup count bytes
that section 4 says are re-read every iteration, or the record flags that section 6 tests)?

Method:
1. `data_xref_scan.py` lists every function that references the AiOrderSet array base 02089378.
   The control is 022C7FE0 (18 refs, from the S-28 work). The types store says the base "is taken
   5 times across 4 bodies"; elements are reached as base + index, so the per-element addresses
   have no direct references.
2. The direct-call closure (Tools/work/graph/edges.tsv, internal edges only) of each substituted
   callee (commit 0030F760, slot resolver 00301AD0) and of each real callee (evaluator 003014C0,
   notify 004697C0) is intersected with those referencers.

Limits: indirect calls, and pointer-passed access to a set whose address was formed elsewhere, are
not covered. A hit means only "statically reachable". This probe executes nothing, so there is no
RIP status to report.
"""
import collections, os, re, subprocess, sys

DB = r"C:\Users\Kristian\source\repos\XIIOnline\Database"
EXE = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe"
scan = subprocess.run([sys.executable, os.path.join(DB, r"Tools\analysis-kit\gfz-scripts\data_xref_scan.py"),
                       "--exe", EXE, "--funcs", os.path.join(DB, r"Tools\work\graph\functions.tsv"),
                       "--addr", "0x02089378", "--control", "0x022C7FE0"],
                      capture_output=True, text=True, env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
print("---- data_xref_scan 02089378 (control 022C7FE0) ----")
print(scan.stdout.strip()[-3000:])
refs = sorted(set(re.findall(r"\[fn ([0-9A-F]{8})\]", scan.stdout)))
print("referencing functions: %s" % refs)

E = collections.defaultdict(set)
with open(os.path.join(DB, r"Tools\work\graph\edges.tsv")) as f:
    next(f)
    for line in f:
        p = line.rstrip("\n").split("\t")
        if len(p) >= 3 and p[2] == "false":
            E[p[0]].add(p[1])


def path(src, dst):
    prev = {src: None}; q = collections.deque([src])
    while q:
        n = q.popleft()
        if n == dst:
            out = []
            while n:
                out.append(n); n = prev[n]
            return out[::-1]
        for m in E[n]:
            if m not in prev:
                prev[m] = n; q.append(m)
    return None


def closure(s):
    seen = {s}; st = [s]
    while st:
        n = st.pop()
        for m in E[n]:
            if m not in seen:
                seen.add(m); st.append(m)
    return seen


print("---- closures ----")
for name, s in (("commit (STUB)", "0030F760"), ("slot resolver (STUB)", "00301AD0"),
                ("evaluator (real)", "003014C0"), ("notify (real)", "004697C0")):
    c = closure(s)
    hits = [r for r in refs if r in c]
    print("%-22s %s closure=%d  set-referencers reached=%s" % (name, s, len(c), hits))
    for h in hits:
        print("    path: %s" % " > ".join(path(s, h)))
