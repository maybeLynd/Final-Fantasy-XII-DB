"""SWE2-AUDIT-SEM: read the record-adjacent inline loops flagged by t5_inline.out."""
import img
def show(lo, hi):
    for x in img.md.disasm(img.rd(lo, hi - lo + 16), lo):
        if x.address > hi:
            break
        print("  %08X %s %s" % (x.address, x.mnemonic, x.op_str))
for name, lo, hi in (("0046BAC0 (r12 = [rax+0x1F0])", 0x0046BAC0, 0x0046BB50), ("002E1450", 0x002E1450, 0x002E1540),
                     ("002686D0 (r14 = r11-0x48)", 0x00268690, 0x002686E8), ("00267B3C (r15+0x1D0)", 0x00267B30, 0x00267B60)):
    print("==", name)
    show(lo, hi)
