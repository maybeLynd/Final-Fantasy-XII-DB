"""relscan.py - raw E8/E9/0F8x rel32 sites (and rip-relative lea/mov qword pointer loads) targeting a VA.
Raw byte scan, no function list: counts every E8/E9 and 0F 80..8F whose rel32 lands on the target,
then decodes each to confirm. Also reports 8-byte absolute pointers to the target anywhere in the
image file (vtables/jump tables/data).
Usage: python relscan.py 0x003A9490 [...]
"""
import struct, sys
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
EXE = r"Database/Tools/work/exe/FFXII_TZA.exe"
pe = pefile.PE(EXE, fast_load=True)
IB = pe.OPTIONAL_HEADER.ImageBase
text = next(s for s in pe.sections if s.Name.rstrip(b"\0") == b".text")
data = text.get_data(); tva = IB + text.VirtualAddress
md = Cs(CS_ARCH_X86, CS_MODE_64)
raw = open(EXE, "rb").read()
for T in [int(a, 16) for a in sys.argv[1:]]:
    out = []
    for p in range(len(data) - 5):
        b = data[p]
        if b in (0xE8, 0xE9):
            if tva + p + 5 + struct.unpack_from("<i", data, p + 1)[0] == T:
                out.append(p)
        elif b == 0x0F and 0x80 <= data[p + 1] <= 0x8F and p + 6 <= len(data):
            if tva + p + 6 + struct.unpack_from("<i", data, p + 2)[0] == T:
                out.append(p)
    print("target %08X: %d raw rel32 sites" % (T, len(out)))
    for p in out:
        ins = next(md.disasm(data[p:p + 8], tva + p), None)
        print("  %08X  %s %s" % (tva + p, ins.mnemonic if ins else "?", ins.op_str if ins else ""))
    print("  absolute 8-byte pointers in file: %d" % raw.count(struct.pack("<Q", T)))
