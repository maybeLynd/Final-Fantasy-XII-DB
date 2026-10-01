"""rc35_gap_readers.py - RC-35 (FABLE, 2026-09-30): what reads the 8-byte block between array C and array D of a
menumap_location.bin record? Array C starts at rec + 4 + 24*(countA+countB); the block starts at C + 20*countC and
array D 8 bytes later (lmap-menumap-location-graph.md section 10.2; 003BFF20 at 003BFF79-003BFFAA).

A reader of the block must form 20*countC. Census, image-wide: every listed function containing a stride-20 formation -
`imul r, r, 0x14`, or `lea r, [x + x*4]` followed within 6 instructions by `shl r, 2` / `lea r2, [r*4...]` / `[.. + r*4 ..]`.
Candidates are then restricted to functions that can hold an lmap record: those reachable (call closure, 3 hops) from the
world-map widget's code (loader 003BC2D0, message procedure 003BC4E0, creator 003BC450) or referring to its singleton
02B457E0 (rip or image-base-relative), plus the accessors 003BF430 / 003C0340 / 003BFF20 / 003C1070 / 003C0740.
Each candidate's stride-20 site is printed with the following 8 instructions, for reading: a D walker adds 8 before its
first load; a block reader loads at +0 / +4 of the C end.
Controls: 003BFF20 and 003C1070 (the known D walkers) and 003C0740 (the known C walker, loop-stepped by 0x14) must be
among the candidates. v2 adds the `add r, 0x14` / `lea r, [x + 0x14]` step form: v1 missed 003C0740."""
import sys, os, json, collections
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
import tk
HOPS = 3
IDX = json.load(open(r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\pub140-scratch\tools\rawcalls.json"))
callees = collections.defaultdict(set)
for tgt, sites in IDX.items():
    t = int(tgt, 16)
    for s in sites:
        o, how = tk.owner(int(s, 16))
        if o is not None and how == "listed":
            callees[o].add(t)
SEED = {0x003BC2D0, 0x003BC4E0, 0x003BC450, 0x003BF430, 0x003C0340, 0x003BFF20, 0x003C1070, 0x003C0740}
h, _ = tk.rip_refs(0x02B457E0, 0x02B457E8)
SEED |= {tk.owner(x.address)[0] for x, k, t in h if tk.owner(x.address)[1] == "listed"}
hb, _ = tk.disp_refs(0x02B457E0 - 0x120000, 0x02B457E8 - 0x120000)
SEED |= {tk.owner(x.address)[0] for x, k, v in hb}
R = set(SEED); fr = set(SEED)
for _ in range(HOPS):
    nx = set()
    for f in fr:
        nx |= {c for c in callees[f] if tk.fsize(c)}
    nx -= R; R |= nx; fr = nx
print("seed %d functions (singleton referrers + widget code + accessors); reach %d after %d hops" % (len(SEED), len(R), HOPS))


def stride20_sites(ins):
    out = []
    for i, x in enumerate(ins):
        if x.mnemonic == "imul" and x.op_str.replace(" ", "").endswith(",0x14"):
            out.append(i)
        elif x.mnemonic in ("add", "lea") and (x.op_str.replace(" ", "").endswith(",0x14")
                                                or x.op_str.replace(" ", "").endswith("+0x14]")):
            out.append(i)                     # pointer stepped by one C entry (loop walkers, v2)
        elif x.mnemonic == "lea" and "*4]" in x.op_str:
            parts = x.op_str.split("[")[1].rstrip("]").replace(" ", "")
            a = parts.split("+")
            if len(a) >= 2 and a[1].startswith(a[0] + "*4"):   # lea r, [x + x*4] = 5x
                for y in ins[i + 1:i + 7]:
                    s = y.op_str.replace(" ", "")
                    if (y.mnemonic == "shl" and s.endswith(",2")) or "*4]" in s:
                        out.append(i); break
    return out


hits = {}
for e, sz in tk.flist:
    if e not in R or sz <= 0 or sz > 0x20000:
        continue
    ins = list(tk.fdis(e))
    s = stride20_sites(ins)
    if s:
        hits[e] = (ins, s)
print("functions in reach with a stride-20 formation: %d" % len(hits))
for e, (ins, s) in sorted(hits.items()):
    print("== %s" % tk.fname(e))
    for i in s[:4]:
        print("   " + " | ".join("%08X %s %s" % (y.address, y.mnemonic, y.op_str) for y in ins[i:i + 9]))
ok = 0x003BFF20 in hits and 0x003C1070 in hits and 0x003C0740 in hits
print("CONTROL known walkers 003BFF20, 003C1070 (D) and 003C0740 (C, loop-stepped) found:", "PASS" if ok else "FAIL")
print("FAILS %d" % (0 if ok else 1))
sys.exit(0 if ok else 1)
