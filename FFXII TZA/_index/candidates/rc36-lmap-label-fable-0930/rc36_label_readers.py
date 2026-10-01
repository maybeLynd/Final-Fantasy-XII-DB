"""rc36_label_readers.py - RC-36 (FABLE, 2026-09-30): which code reads a menumap_location.bin array-B marker's +0x0C
destination-label id (60,201..60,244)?

Part 1, the accessor route. 003BF430(n, i, &kind) returns point i of record n and kind 0 (array A) or 1 (array B)
(lmap-menumap-location-graph.md section 10.2). For each of its call sites (raw index) the script finds every word load at
+0xC in the caller and reports whether it is reached only when kind == 0, i.e. only for A points, whose +0xC is a field id.
The kind==0 guard is recognised as `cmp dword [rsp+X], 0` / `jne` on the kind out-slot, or the kind moved to a register
followed by `test r, r` / `jne`, between the call and the load.
Part 2, direct arithmetic. Every word load at +0xC in the call closure (3 hops) of the world-map widget's code and the
referrers of its singleton 02B457E0, excluding the Part-1 loads, is listed for reading.
Control: the known A-point reader 003C0416 (in 003C0380; lmap section 10.4's membership test) is classified kind-0-guarded."""
import sys, json, collections
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
import tk
IDX = json.load(open(r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\pub140-scratch\tools\rawcalls.json"))
sites = sorted(int(s, 16) for k, v in IDX.items() if k.upper().lstrip("0X").lstrip("0") == "3BF430" for s in v)
part1 = {}
for site in sites:
    o, _ = tk.owner(site)
    ins = list(tk.fdis(o))
    j = [i for i, x in enumerate(ins) if x.address == site][0]
    slot = None
    for x in ins[j - 4:j]:
        if x.mnemonic == "lea" and x.op_str.startswith("r8,"):
            slot = x.op_str.split("[")[1].rstrip("]").replace(" ", "")
    guard, kreg = False, None
    for x in ins[j + 1:j + 40]:
        s = x.op_str.replace(" ", "")
        if slot and x.mnemonic == "cmp" and slot in s and s.endswith(",0"):
            guard = True
        if slot and x.mnemonic == "mov" and slot in s and not s.startswith("dwordptr"):
            kreg = s.split(",")[0]
        if kreg and x.mnemonic == "test" and s == "%s,%s" % (kreg, kreg):
            guard = True
        if x.mnemonic == "movzx" and "wordptr" in s and s.endswith("+0xc]") or (x.mnemonic == "cmp" and "wordptr" in s and "+0xc]" in s):
            part1[x.address] = (site, o, guard)
            break
print("003BF430 call sites: %d; +0xC loads after a call: %d" % (len(sites), len(part1)))
for a, (site, o, g) in sorted(part1.items()):
    print("  load %08X after call %08X in %08X: %s" % (a, site, o, "kind==0 only (A point)" if g else "NOT shown guarded - read"))
unguarded = [a for a, v in part1.items() if not v[2]]
ctl = part1.get(0x003C0416, (0, 0, False))[2]
# Part 2
callees = collections.defaultdict(set)
for tgt, ss in IDX.items():
    t = int(tgt, 16)
    for s in ss:
        o, how = tk.owner(int(s, 16))
        if o is not None and how == "listed":
            callees[o].add(t)
SEED = {0x003BC2D0, 0x003BC4E0, 0x003BC450}
h, _ = tk.rip_refs(0x02B457E0, 0x02B457E8)
SEED |= {tk.owner(x.address)[0] for x, k, t in h if tk.owner(x.address)[1] == "listed"}
R = set(SEED); fr = set(SEED)
for _ in range(3):
    nx = set()
    for f in fr:
        nx |= {c for c in callees[f] if tk.fsize(c)}
    nx -= R; R |= nx; fr = nx
other = []
for e, sz in tk.flist:
    if e not in R or sz <= 0 or sz > 0x20000:
        continue
    for x in tk.fdis(e):
        s = x.op_str.replace(" ", "")
        if "wordptr" in s and s.endswith("+0xc]") and x.mnemonic in ("movzx", "movsx", "mov", "cmp") and x.address not in part1:
            other.append((e, x.address, x.mnemonic + " " + x.op_str))
print("\nPart 2: other word loads at +0xC in the widget's reach (%d functions): %d" % (len(R), len(other)))
byf = collections.defaultdict(list)
for e, a, t in other:
    byf[e].append("%08X %s" % (a, t))
for e in sorted(byf):
    print("  %s: %s" % (tk.fname(e), byf[e][:4]))
print("CONTROL 003C0416 (known A-point reader) classified kind==0 only:", "PASS" if ctl else "FAIL")
print("Part-1 loads not shown kind-0-guarded: %s" % (["%08X" % a for a in unguarded] or "NONE"))
print("FAILS %d" % (0 if ctl else 1))
sys.exit(0 if ctl else 1)
