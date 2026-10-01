"""con191_196_sample.py - SWE2-AUDIT-SPEC (batch-9 review, 2026-09-29). Independent samples.

CON-192: the jump table the state machine 00581DA0 dispatches through (reported at 00582020): states 4/5/6 -> one arm
         00581E9E, 7 -> 00581EB0, 8 -> 00581FA8. Decodes the dispatch and reads the table itself.
CON-193: the template bytes at 00917268 = 35 00 00 00 00 04 62 00 -> dword1 = 0x00620400, bits 10, 17, 21, 22.
CON-194: 002DDD70's two arms.
CON-196: every rip-relative lea target in 0040A230 lies in .rdata and is a PS2Data ... obj_finish .cm path string.
"""
import os, struct, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "auditspec-review-ov31-type-store-0929"))
sys.path.insert(0, os.path.join(HERE, "..", "auditspec-review-opus-batch8-0929"))
import ov31_indep as T  # noqa: E402
import b8dis  # noqa: E402

fails = 0
print("== CON-192 dispatch in 00581DA0")
ins = T.dis_func(0x00581DA0, 0x800)
disp = [i for i in ins if "rax*4" in i.op_str or "rcx*4" in i.op_str or "jmp" == i.mnemonic and i.op_str in ("rax", "rcx", "rdx")]
for i in disp:
    print("  %08X  %s %s" % (i.address, i.mnemonic, i.op_str))
b8dis.dump(0x00581DB0, 0x00581DE8)
tab = 0x00582020
arms = [struct.unpack("<I", T.rd(tab + 4 * k, 4))[0] + T.IB for k in range(10)]
print("  table 00582020 (as rva32 + image base):", ["%08X" % a for a in arms])
print("== CON-193 template bytes 00917268:", T.rd(0x00917268, 8).hex(" "))
d1 = struct.unpack("<I", T.rd(0x0091726C, 4))[0]
bits = [b for b in range(32) if d1 >> b & 1]
ok = d1 == 0x00620400 and bits == [10, 17, 21, 22]
fails += not ok
print("  %s dword1 = %08X bits %s" % ("PASS" if ok else "FAIL", d1, bits))
print("== CON-194 002DDD70")
b8dis.dump(0x002DDD70, 0x002DDDA0)
print("== CON-196 lea targets in 0040A230")
ins = T.dis_func(0x0040A230, 0x20000)
rd = [s for s in T.SECS if s[0] == ".rdata"][0]
n = bad = 0
for i in ins:
    if i.mnemonic == "lea":
        for m, _ in T.mem_ops(i):
            if m.base == T.X86_REG_RIP:
                t = i.address + i.size + m.disp
                o = T.off(t)
                s = T.raw[o:o + 160].split(b"\0")[0].decode("latin1") if o is not None else ""
                n += 1
                good = rd[1] <= t < rd[1] + rd[2] and "PS2Data" in s and "obj_finish" in s and s.endswith(".cm")
                if not good:
                    bad += 1
                    print("  NOT A PATH  %08X -> %08X %r" % (i.address, t, s[:80]))
fails += bad > 0 or n == 0
print("  %s %d rip lea targets in 0040A230 (%d insns), %d not an .rdata PS2Data obj_finish .cm string" % (
    "PASS" if (n and not bad) else "FAIL", n, len(ins), bad))
print("FAILS %d" % fails)
