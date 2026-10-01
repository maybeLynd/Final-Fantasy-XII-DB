"""rc19_rate_readers.py - every float access at displacement +0x354 in the image (the blend leaves store 1.0/blend at a presentation entry +0x354). ORACLE, 2026-09-30."""
import img
from capstone.x86 import X86_OP_MEM
hits={}
for r in sorted(img.ROOTS):
    for b,e in img.fragments(r):
        if e-b>0x20000: continue
        for x in img.dis(b,e-b):
            for o in x.operands:
                if o.type==X86_OP_MEM and o.mem.disp==0x354 and o.mem.base!=0 and x.mnemonic in ("movss","addss","subss","mulss","comiss","ucomiss","divss","minss","maxss"):
                    hits.setdefault(r,[]).append("%08X %s %s"%(x.address,x.mnemonic,x.op_str))
for r,v in hits.items(): print("%08X"%r, v[:6])
