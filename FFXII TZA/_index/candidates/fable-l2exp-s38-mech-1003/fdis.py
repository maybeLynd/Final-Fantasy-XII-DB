"""dis.py - FABLE helper: print a function body. Usage: python dis.py VA [VA ...]  (hex).
A .pdata body is printed whole (chained entries resolved by rvlib's pdata); a leaf outside .pdata is decoded linearly
from VA until the first int3 padding after a ret/jmp."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rawref import Img

img = Img.load()
img.cs.detail = True
for a in sys.argv[1:]:
    va = int(a, 16)
    pd = img.pdata(va)
    if pd and pd[0] == va:
        s, e = pd
        print("== %08X .. %08X (.pdata, %d B)" % (s, e, e - s))
        for ci in img.cs.disasm(img.read(s, e - s), s):
            print("  %08X  %s %s" % (ci.address, ci.mnemonic, ci.op_str))
    else:
        print("== %08X (%s)" % (va, "inside .pdata %08X..%08X" % pd if pd else "NOPDATA leaf"))
        n = 0
        for ci in img.cs.disasm(img.read(va, 0x400), va):
            print("  %08X  %s %s" % (ci.address, ci.mnemonic, ci.op_str))
            n += 1
            if ci.mnemonic in ("ret", "jmp", "int3") and img.read(ci.address + ci.size, 1) == b"\xcc":
                break
            if n > 400:
                break
