"""SWE2-AUDIT-SEM own checks for dd-leftovers-0930.
S  SD-24: the two walkers' use of [this+0x30] and the vtable they compare (007E5930..007E5945, 007E6815..007E6830);
   the RTTI name of vtable 01CB43E0 (COL at vtable-8, type descriptor +0x10); the bind 007BDDA0's +0x30 store and
   its +0x4E read.
I  the input channel record: the initialiser 0035F260's pointer set-up and every byte store through rdi; the analog
   builder's dead-zone read at 0035F7BD."""
import struct, re
import img
raw, BASE = img.raw, img.BASE
def show(lo, hi, filt=None):
    for x in img.md.disasm(img.rd(lo, hi - lo + 16), lo):
        if x.address > hi:
            break
        if filt is None or re.search(filt, x.op_str):
            print("   %08X %s %s" % (x.address, x.mnemonic, x.op_str))
print("S walker 1"); show(0x007E5920, 0x007E5948)
print("S walker 2"); show(0x007E6808, 0x007E6830)
col = struct.unpack_from("<Q", img.rd(0x01CB43E0 - 8, 8))[0]
o = img.off(col)
sig, off, cdo, td, ch, selfr = struct.unpack_from("<IIIIII", raw, o)
name = img.rd(td + BASE + 0x10, 80).split(b"\0")[0]
print("S vtable 01CB43E0: COL %08X sig %d self-RVA ok %s class %s" % (col, sig, selfr == col - BASE, name))
print("S bind 007BDDA0 (+0x30 / +0x4E / +0x18)"); show(0x007BDDA0, 0x007BDE60, r"0x30\]|0x4e\]|0x18\]")
print("I initialiser 0035F260: pointer set-up and stores through rdi / rbx"); show(0x0035F260, 0x0035F3A0, r"rdi|rbx|022ca|rip")
print("I analog builder 0035F7B0..0035F7C4"); show(0x0035F7B0, 0x0035F7C4)
