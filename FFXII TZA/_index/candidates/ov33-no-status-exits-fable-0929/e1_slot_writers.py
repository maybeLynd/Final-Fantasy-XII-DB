"""e1_slot_writers.py - who else writes request-slot +0x21 (kind) / +0x24 (index)?  (OV-33 E1)

Step 1: every function that addresses the queue storage [022C31C0, 022C5200) (pool 022C31C0, heads 022C51C0/C8/D0,
selector globals 022C51D8/DC) by rip-relative, image-base-relative (disp = VA - 0x120000) or absolute form.
Step 2: in each such function, every store whose memory operand has displacement 0x21 (any width covering it) or
0x24 (covering 0x24..0x27) - i.e. any store that could touch the kind byte or the index dword of a slot pointer.
Also any wide store (>= 8 bytes) with disp in [0x1A, 0x27] (covers +0x21 or +0x24).
Positive controls: 0032E943 (kind) and 0032E902 (index) must be listed, in 0032E870.
Limits: slot pointers passed to functions that do not themselves address the queue storage are not followed here;
see README (the callbacks receive arg/dest0, not the slot; the per-slot onPart +0x50 is zeroed by every builder).
Terminal line: FAILS n / STATUS.
"""
import sys
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
import tk
from capstone.x86 import X86_OP_MEM
LO, HI = 0x22C31C0, 0x22C5200
fns = {}
h, raw = tk.rip_refs(LO, HI)
for x, k, t in h:
    o, how = tk.owner(x.address); fns.setdefault(o, []).append("rip %08X->%08X" % (x.address, t))
h2, raw2 = tk.disp_refs(LO - tk.BASE, HI - tk.BASE)
for x, k, v in h2:
    o, how = tk.owner(x.address); fns.setdefault(o, []).append("disp %08X" % x.address)
h3, raw3 = tk.abs_refs(LO, HI)
for x, v in h3:
    o, how = tk.owner(x.address); fns.setdefault(o, []).append("abs %08X" % x.address)
print("# functions addressing the queue storage: %d  (raw-only unverified: rip %d disp %d abs %d)" % (len(fns), len(raw), len(raw2), len(raw3)))
for p, t in raw: print("  raw-only rip disp at %08X -> %08X in %s" % (p, t, tk.fname(p)))
fails = 0; hits = []
for o in sorted(k for k in fns if k is not None):
    print("%08X %s : %s" % (o, tk.names.get(o, "[pdata]"), ", ".join(fns[o][:6]) + (" ..." if len(fns[o]) > 6 else "")))
    sz = tk.fsize(o)
    if sz is None:
        j = [b for b, e in tk.pdata if b == o]; sz = ([e for b, e in tk.pdata if b == o] or [o + 0x400])[0] - o
    for x in tk.dis(o, o + sz):
        for k, op in enumerate(x.operands):
            if op.type != X86_OP_MEM or not tk.is_store(x, k): continue
            if op.mem.base != 0 and x.reg_name(op.mem.base) in ("rsp", "rip"): continue
            dsp = op.mem.disp; n = op.size
            if dsp <= 0x21 < dsp + n or dsp <= 0x24 < dsp + n:
                hits.append((x.address, o, "%s %s" % (x.mnemonic, x.op_str)))
print("\n# stores covering +0x21 or +0x24 (non-stack, non-rip) inside those functions:")
for a, o, s in hits: print("  %08X in %08X  %s" % (a, o, s))
for c in (0x32E943, 0x32E902):
    ok = any(a == c for a, o, s in hits); print("control %08X listed: %s" % (c, ok)); fails += not ok
print("FAILS %d" % fails)
print("STATUS %s" % ("COMPLETE" if fails == 0 else "INCOMPLETE"))
