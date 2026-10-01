import json, os, struct
import world as W
HERE = os.path.dirname(os.path.abspath(__file__))
FX = json.load(open(os.path.join(HERE, "world.json")))
REQUEST, APPLY = 0x226BE0, 0x226280
W.ALLOWED |= {0x16D6A0} | W.closure(REQUEST) | W.closure(APPLY)
S = W.Session(FX["fixes"], FX["inits"]); uc = S.uc
IDLE = 0x76200000
for i, cell in enumerate((0x209BE80, 0x1F7FFE0, 0x215E6E0)):
    uc.mem_write(IDLE + i * 0x20000, bytes(0x20000)); uc.mem_write(cell, struct.pack("<Q", IDLE + i * 0x20000))
i32 = lambda a: struct.unpack("<i", bytes(uc.mem_read(a, 4)))[0]
def req(s, st):
    uc.mem_write(0x1FD46D4, struct.pack("<I", struct.unpack("<I", bytes(uc.mem_read(0x1FD46D4, 4)))[0] & ~(1 << s)))
    ok = S.call(REQUEST, s, 0, 0, 0, stack=st)
    return ok, i32(0x1FD4400 + s * 0x18 + 0x10), i32(0x1FD4160 + s * 0x18 + 0x10)
print(req(3, (5, 0xFFFFFFFF)), req(7, (0xFFFFFFFF, 9)))
req(9, (0xFFFFFFFF, 0xFFFFFFFF)); req(7, (0, 0xFFFFFFFF))
ok = S.call(APPLY)
print("apply", ok, S.st["bad"], S.st["faults"], ["%08X" % a for a in list(S.st["trace"])[-3:]])
print("fades after", [i32(0x1FD4400 + s * 0x18 + 0x10) for s in (3, 7, 9)], "dirty", uc.mem_read(0x1FD46D0, 1)[0])
