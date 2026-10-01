"""sd60_rederive.py - SWE2-AUDIT-SPEC independent re-derivation for SD-60 (2026-09-30). Read-only on the image.
Uses tk.py (raw rip/disp sweeps, not the function list) for writer censuses."""
import os, sys, struct
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
import tk

def show(a, n):
    o = tk.off(a)
    for x in list(tk.md.disasm(tk.d[o:o + 0x200], a))[:n]:
        print("  %08X %s %s" % (x.address, x.mnemonic, x.op_str))

print("== 00678B50 (depth-term rewrite), full body")
show(0x00678B50, 40)
print("== 00864E90 execute (first 30)")
show(0x00864E90, 30)

def writers(lo, hi, label):
    hits, raw = tk.rip_refs(lo, hi)
    w = [(x.address, x.mnemonic, x.op_str, tk.fname(x.address)) for x, k, t in hits if tk.is_store(x, k)]
    r = [(x.address, x.mnemonic, x.op_str, tk.fname(x.address)) for x, k, t in hits if not tk.is_store(x, k)]
    dh, draw = tk.disp_refs(lo - tk.BASE, hi - tk.BASE)
    print("== %s rip refs %d (stores %d), raw-only %d; image-base disp forms %d (raw-only %d)" % (label, len(hits), len(w), len(raw), len(dh), len(draw)))
    for a, m, o, f in w: print("  W %08X %s %s   in %s" % (a, m, o, f))
    for a, m, o, f in r: print("  R %08X %s %s   in %s" % (a, m, o, f))
    for x, k, v in dh: print("  D %08X %s %s   in %s" % (x.address, x.mnemonic, x.op_str, tk.fname(x.address)))

writers(0x02AEEBA0, 0x02AEEBA8, "floats 02AEEBA0..A7")
writers(0x02AEEB20, 0x02AEEB60, "block-1 source 02AEEB20..5F")
writers(0x01FD3620, 0x01FD3668, "execute targets 01FD3620..67")
# slot +0x30 of PrimitiveRendererD3D11 vtable, and the store run in 006CAF40
print("== vtable 00D86960 +0x30 = %08X" % tk.u64(0x00D86990))
show(0x006CAF40, 40)
