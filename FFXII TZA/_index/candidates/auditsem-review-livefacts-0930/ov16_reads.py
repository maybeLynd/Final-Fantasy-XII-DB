"""SWE2-AUDIT-SEM OV-16 re-read: raw E8/E9 callers of 003DB2A0 and 003DB420; the RETN / REQCANCEL handlers
(00261301..0026133F); the head of 003DB420 (channel walk)."""
import struct
import img
t0, t1, rp = img.text_range()
text = img.raw[rp:rp + (t1 - t0)]
va0 = img.BASE + t0
for T in (0x003DB2A0, 0x003DB420):
    s = []
    for i in range(len(text) - 5):
        if text[i] in (0xE8, 0xE9) and va0 + i + 5 + struct.unpack_from("<i", text, i + 1)[0] == T:
            s.append("%08X %s" % (va0 + i, "call" if text[i] == 0xE8 else "jmp"))
    print("direct sites into %08X: %d %s" % (T, len(s), s))
def show(lo, hi):
    for x in img.md.disasm(img.rd(lo, hi - lo + 16), lo):
        if x.address > hi:
            break
        print("  %08X %s %s" % (x.address, x.mnemonic, x.op_str))
print("== handlers 00261301..0026133F"); show(0x00261301, 0x0026133F)
print("== 003DB420 head"); show(0x003DB420, 0x003DB4B0)
print("== the four non-interpreter callers of 003DB420 (12 instructions before each)")
for s in (0x002697B2, 0x002697C0, 0x0035299C, 0x00353695):
    for back in range(48, 10, -1):
        xs = list(img.md.disasm(img.rd(s - back, back + 5), s - back))
        if any(x.address == s for x in xs):
            break
    print(" -- %08X" % s)
    for x in [x for x in xs if x.address <= s][-12:]:
        print("   %08X %s %s" % (x.address, x.mnemonic, x.op_str))
