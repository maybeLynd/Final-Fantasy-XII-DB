"""e3_shutdown_reach.py - after 001A11F0 nulls the read-layer pointer (0017D679 in 0017D670), can the teardown that
follows reach the pump 0032E070 (or its entries 0032E040 / 0032E520 / 0032E870)?  (OV-33 E3)

Direct-call BFS (E8 call and E9 jmp with rel32, and 0F 8x jcc tail-branches to other functions) from the callees that
0017D670 runs after 0017D679: 001DC4E0, 00198790, 001993B0, 0022A090, 0017DAC0. Indirect calls are listed per
function, not followed (limit, stated in README).
Positive control: BFS from 0022B6E0 (main-loop mode 0, which calls 0032E040 at 0022B7A9) must reach 0032E070.
Terminal line: FAILS n / STATUS.
"""
import sys
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
import tk
PUMP = {0x32E070, 0x32E040, 0x32E520, 0x32E870}
def callees(f):
    o, how = tk.owner(f)
    if o is None: return [], []
    sz = tk.fsize(o)
    if sz is None: sz = [e for b, e in tk.pdata if b == o][0] - o
    out = []; ind = []
    for x in tk.dis(o, o + sz):
        if (x.mnemonic in ("call", "jmp") or (x.mnemonic.startswith("j") and x.mnemonic != "jmp")) and x.op_str.startswith("0x"):
            t = int(x.op_str, 16)
            if not (o <= t < o + sz): out.append(t)
        elif x.mnemonic in ("call", "jmp") and not x.op_str.startswith("0x"):
            ind.append("%08X %s %s" % (x.address, x.mnemonic, x.op_str))
    return out, ind
def bfs(roots, depth=12):
    seen = set(); frontier = list(roots); hit = []; indirect = {}
    for d in range(depth):
        nf = []
        for f in frontier:
            if f in seen: continue
            seen.add(f)
            if f in PUMP: hit.append(f); continue
            c, ind = callees(f)
            if ind: indirect[f] = ind
            nf += c
        frontier = nf
    return seen, hit, indirect
fails = 0
seen, hit, ind = bfs([0x22B6E0])
print("control: from 0022B6E0 reaches pump:", bool(hit), ["%08X" % h for h in hit]); fails += not hit
roots = [0x1DC4E0, 0x198790, 0x1993B0, 0x22A090, 0x17DAC0]
seen, hit, ind = bfs(roots)
print("teardown roots:", ["%08X" % r for r in roots])
print("functions visited: %d" % len(seen))
print("pump entries reached: %s" % (["%08X" % h for h in hit] or "none"))
print("functions with indirect calls/jumps (not followed): %d" % len(ind))
for f in sorted(ind)[:60]: print("  %08X %s: %s" % (f, tk.names.get(f, "?"), "; ".join(ind[f][:4])))
print("FAILS %d" % fails)
print("STATUS %s" % ("COMPLETE" if fails == 0 else "INCOMPLETE"))
