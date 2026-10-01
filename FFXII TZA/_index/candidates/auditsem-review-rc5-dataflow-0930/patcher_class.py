"""SWE2-AUDIT-SEM: 0026D3E0's patch-entry class dispatch (table at image base + 0x14D510, 6 arms) and its copy - the
native writer of script storage at manager initialisation (called from 0026CE60 at 0026D300)."""
import struct
import img
base = 0x00120000
for c in range(6):
    d = struct.unpack_from("<I", img.rd(base + 0x14D510 + 4 * c, 4))[0]
    tgt = base + d
    x = next(img.md.disasm(img.rd(tgt, 16), tgt))
    print("class %d -> %08X %s %s" % (c, tgt, x.mnemonic, x.op_str))
for x in img.dis(0x0026D4BD, 8):
    print("   %08X %s %s" % (x.address, x.mnemonic, x.op_str))
