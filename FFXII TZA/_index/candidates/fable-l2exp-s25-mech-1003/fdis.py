"""dis.py - FABLE helper: print a linear disassembly of [va, va+n) or of the .pdata function holding va."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rawref import Img  # noqa: E402

img = Img.load()
va = int(sys.argv[1], 16)
if len(sys.argv) > 2:
    n = int(sys.argv[2], 16)
    s = va
else:
    s, e = img.pdata(va)
    n = e - s
    print("pdata %08X-%08X (%d B)" % (s, e, n))
for ci in img.cs.disasm(img.read(s, n), s):
    print("%08X  %-24s %s %s" % (ci.address, ci.bytes.hex(), ci.mnemonic, ci.op_str))
