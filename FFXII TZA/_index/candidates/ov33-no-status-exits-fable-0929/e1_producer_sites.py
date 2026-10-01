"""e1_producer_sites.py - census of every queue-slot producer site (OV-33 E1).

Producers of slot +0x21 kind / +0x24 index: 0032E870 fills them (0032E8CE..0032E97C). Its only callers are
0032E620 (x2), 0032E780, 0032E7C0 (raw call index). This script lists every raw E8/E9 site and every
0F 8x (jcc rel32) site targeting 0032E620 / 0032E780 / 0032E7C0 / 0032E7B0 / 0032E870, plus every
rip-relative address-take of those entries (an indirect-call producer), then for each site prints a
backward window of the owner function (from the owner's start, capped) so the kind/index/bytes source
can be read.

Positive controls: 002492F3 (a known 0032E620 call), 0032E84D (0032E7C0 -> 0032E870), 0032EC01 (0032EB40).
Terminal line: FAILS n / STATUS.
"""
import sys, struct, os
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
import tk

TARGETS = {0x32E620: "0032E620 builder", 0x32E780: "0032E780 head-insert", 0x32E7C0: "0032E7C0 string-keyed",
           0x32E7B0: "0032E7B0 thunk->0032E7C0", 0x32E870: "0032E870 slot fill"}
blob = tk.d[tk.TRO:tk.TRO + min(tk.TVS, tk.TRS)]
sites = []
for i in range(len(blob) - 6):
    b = blob[i]
    if b in (0xE8, 0xE9):
        t = tk.TVA + i + 5 + struct.unpack_from("<i", blob, i + 1)[0]
        if t in TARGETS: sites.append((tk.TVA + i, "call" if b == 0xE8 else "jmp", t))
    if b == 0x0F and 0x80 <= blob[i + 1] <= 0x8F:
        t = tk.TVA + i + 6 + struct.unpack_from("<i", blob, i + 2)[0]
        if t in TARGETS: sites.append((tk.TVA + i, "jcc", t))
# verify each raw site decodes on an instruction boundary of its owner
ver = []
for a, kind, t in sites:
    b = tk.boundaries(a)
    on = b is None or a in b
    ver.append((a, kind, t, on))
fails = 0
print("# raw sites (E8/E9/0F8x) targeting the producers")
for a, kind, t, on in ver:
    print("%08X %-4s -> %s  owner %s  %s" % (a, kind, TARGETS[t], tk.fname(a), "on-boundary" if on else "OFF-BOUNDARY (not code)"))
real = [(a, k, t) for a, k, t, on in ver if on]
print("# on-boundary sites: %d (of %d raw)" % (len(real), len(ver)))
# address-takes
for t in TARGETS:
    hits, raw = tk.rip_refs(t, t + 1)
    for x, k, tt in hits:
        print("ADDRESS-TAKE %08X %s %s -> %08X in %s" % (x.address, x.mnemonic, x.op_str, tt, tk.fname(x.address)))
    rel = tk.reloc_ptrs(t, t + 1)
    for a, q in rel: print("RELOC-PTR %08X -> %08X" % (a, q))
for c in (0x2492F3, 0x32E84D, 0x32EC01):
    ok = any(a == c for a, k, t in real)
    print("control %08X listed: %s" % (c, ok))
    if not ok: fails += 1
# per-site windows
out = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "e1_producer_windows.txt"), "w")
for a, k, t in real:
    o, how = tk.owner(a)
    start = max(o, a - 0x180)
    xs = tk.dis(start if start == o else start, a + 5)
    # realign: decode from owner start and keep the window
    xs = [x for x in tk.dis(o, a + 6) if x.address >= start]
    out.write("==== site %08X %s -> %s in %s\n" % (a, k, TARGETS[t], tk.fname(a)))
    for x in xs:
        out.write("  %08X %s %s\n" % (x.address, x.mnemonic, x.op_str))
out.close()
print("windows written: e1_producer_windows.txt")
print("FAILS %d" % fails)
print("STATUS %s" % ("COMPLETE" if fails == 0 else "INCOMPLETE"))
