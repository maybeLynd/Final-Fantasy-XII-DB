"""SWE2-AUDIT-SPEC: the unlisted leaf that stores [rcx+0xCB8] at 00707657 - its entry and every raw caller / pointer to it.
2026-09-30."""
import sys, json
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
import tk
RAW = json.load(open(r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\pub140-scratch\tools\rawcalls.json"))
# entry: first non-int3/nop byte after the previous function's end (007075EE)
o = tk.off(0x7075EE)
a = 0x7075EE
while tk.d[o] in (0xCC, 0x90): o += 1; a += 1
print("leaf entry candidates from %08X:" % a)
for x in tk.dis(a, 0x707628): print("  %08X %s %s" % (x.address, x.mnemonic, x.op_str))
for e in range(a, 0x707628):
    cs = RAW.get("%X" % e, [])
    if cs: print("raw calls/jmps to %08X: %s" % (e, " ".join("%s(in %08X)" % (c, tk.owner(int(c, 16))[0] or 0) for c in cs)))
    rel = tk.reloc_ptrs(e, e + 1)
    if rel: print("relocated pointers to %08X: %s" % (e, " ".join("%08X" % p for p, _ in rel)))
    rr, _ = tk.rip_refs(e, e + 1)
    if rr: print("rip refs to %08X: %s" % (e, " ".join("%08X" % r[0] for r in rr)))
