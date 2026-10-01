"""SWE2-AUDIT-SEM RC-15 spot check of two of FABLE's corrected base typings: 002ED6A0's rdx at its two callers
(002E4AED in 002E4A40, 002E5B16 / jmp at 002E5B5A), and 003A4290's frame pointer."""
import img
def show(lo, hi):
    for x in img.md.disasm(img.rd(lo, hi - lo + 16), lo):
        if x.address > hi:
            break
        print("  %08X %s %s" % (x.address, x.mnemonic, x.op_str))
print("== 002ED6A0 head"); show(0x002ED6A0, 0x002ED6E6)
print("== caller 002E4AC0..002E4AED"); show(0x002E4AC0, 0x002E4AED)
print("== caller 002E5AF0..002E5B5A"); show(0x002E5AF0, 0x002E5B5A)
print("== 003A4290 prologue"); show(0x003A4290, 0x003A42C8)
