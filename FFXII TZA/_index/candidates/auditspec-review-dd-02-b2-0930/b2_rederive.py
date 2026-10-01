"""b2_rederive.py - SWE2-AUDIT-SPEC own-tool checks behind the batch-2 review (2026-09-30). Reads only.

Uses ../auditspec-review-ddres-b6-0930/ind.py (pefile + capstone, sha asserted).
  M  OPUS's new fact: the MRP header relocator 002A00F0 - every [reg+disp] operand in its body (+0x24 / +0x28 read,
     +0x2C never), and a positive control (+0x24 must be found)
  A  as7 walker 0024AA00: the reads of bytes +2 / +3 (count) - is the page's `+0x02 count` "reader not isolated" stale?
  L  lst readers 0037EFC0 / 0037E5B0: u16 [+0x08], u16 [+0x0E], directory +0/+2/+4 - are §3's "not isolated" rows stale?
  G  mg: 00274780's directory read; 00563110's name table 00D23270 strings; the sub-mesh header +0x14 (slot count, file
     +0x24 for sub 0) read in 005556A0's body
"""
import os, re, struct, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "auditspec-review-ddres-b6-0930"))
import ind as I  # noqa: E402


def body(f):
    r = I.func_of(f)
    if r == f:
        return I.body(r)
    seq = []
    for i in I.dis(f, f + 0x400):
        seq.append(i)
        if i.mnemonic == "ret":
            break
    return seq


def memops(seq, pat=None):
    out = []
    for i in seq:
        for k, op in I.mem_ops(i):
            if op.mem.base == I.X86_REG_RIP:
                continue
            s = "%08X %s" % (i.address, I.txt(i))
            if pat is None or re.search(pat, i.op_str):
                out.append(s)
    return out


b = body(0x002A00F0)
print("M 002A00F0: %d instructions (.pdata root %s)" % (len(b), "%08X" % I.func_of(0x002A00F0) if I.func_of(0x002A00F0) else None))
for s in memops(b):
    print("M   " + s)
print("M   operands with +0x2c:", memops(b, r"\+ 0x2c\]"), " control +0x24 present:", bool(memops(b, r"\+ 0x24\]")))

print("A 0024AA00 first 24 instructions:")
for i in I.dis(0x0024AA00, 0x0024AA70)[:24]:
    print("A   %08X %s" % (i.address, I.txt(i)))

for f in (0x0037EFC0, 0x0037E5B0):
    seq = body(f)
    print("L %08X: %d instructions; memory operands:" % (f, len(seq)))
    for s in memops(seq)[:40]:
        print("L   " + s)

print("G 00274780:")
for i in I.dis(0x00274780, 0x002747A0):
    print("G   %08X %s" % (i.address, I.txt(i)))
    if i.mnemonic == "ret":
        break
print("G 00D23270 name table (qword pointers -> strings):")
for k in range(8):
    q = I.rd(0x00D23270 + 8 * k, 8)
    p = struct.unpack("<Q", q)[0]
    s = (I.rd(p, 32) or b"").split(b"\0")[0].decode("latin-1") if 0x00120000 <= p < 0x04000000 else None
    print("G   +%02X %016X %s %s" % (8 * k, p, s, "reloc" if (0x00D23270 + 8 * k) in I.relocs() else ""))
seq = body(0x005556A0)
print("G 005556A0: %d instructions; operands with +0x10 / +0x14 displacements:" % len(seq))
for s in memops(seq, r"\+ 0x1[04]\]"):
    print("G   " + s)
