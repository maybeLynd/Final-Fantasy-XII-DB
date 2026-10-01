import sys, struct
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\SWE2-AUDIT-SEM\bucket0930")
import img, reqsites as R, wrappers as W
for t in (0x0040AAD0, 0x0040B3B0, 0x0040DB70, 0x0054B1F0):
    print("%08X <-" % t, ["%08X(%s) in %08X" % (c, k, W.root(c)) for c, k in R.refs.get(t, [])])
    import re
    q = [m.start() for m in re.finditer(re.escape(struct.pack("<Q", t)), img.raw)]
    print("   stored qword pointers:", len(q))
# preset block 01EFFA30: six 0x20 records
for p in range(6):
    b = img.rd(0x01EFFA30 + p * 0x20, 0x20)
    print("preset", p + 1, [round(x, 4) for x in struct.unpack("<8f", b)], struct.unpack("<8I", b)[6])
