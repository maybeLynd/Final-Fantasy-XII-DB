"""SWE2-AUDIT-SEM: the fifteen registry rows' shipped +0x3C counts (01EEBCC0, stride 0x58) and their sum."""
import sys, struct
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\SWE2-AUDIT-SEM\bucket0930")
import img
c = [struct.unpack("<I", img.rd(0x01EEBCC0 + i * 0x58 + 0x3C, 4))[0] for i in range(15)]
print("row +3C counts:", c, " sum:", sum(c), " row 8 (ids 0x8000-0x8FFF):", hex(c[8]))
