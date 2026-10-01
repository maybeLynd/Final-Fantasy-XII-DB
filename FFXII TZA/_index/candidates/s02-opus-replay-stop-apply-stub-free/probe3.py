import json, os, struct, time
import world as W
HERE = os.path.dirname(os.path.abspath(__file__))
FX = json.load(open(os.path.join(HERE, "world.json")))
REQUEST, APPLY = 0x226BE0, 0x226280
INIT = 0x226B30
W.ALLOWED |= {0x16D6A0} | W.closure(REQUEST) | W.closure(APPLY) | W.closure(INIT)
t=time.time(); res={}
for s in range(28):
    S = W.Session(FX["fixes"], FX["inits"]); uc = S.uc
    IDLE = 0x76200000
    for i, cell in enumerate((0x209BE80, 0x1F7FFE0, 0x215E6E0)):
        uc.mem_write(IDLE + i * 0x20000, bytes(0x20000)); uc.mem_write(cell, struct.pack("<Q", IDLE + i * 0x20000))
    oki = S.call(INIT); A0 = struct.unpack('<Q', bytes(uc.mem_read(0x1FD4160, 8)))[0]
    uc.mem_write(0x1FD46D4, bytes(4))
    okr = S.call(REQUEST, s, 0, 0, 0, stack=(0, 0xFFFFFFFF))
    B = struct.unpack("<Q", bytes(uc.mem_read(0x1FD4400 + s * 0x18, 8)))[0]
    oka = S.call(APPLY)
    res[s] = (oki, "%X" % A0, okr, oka, "%016X" % B, (S.st["faults"] or [""])[0], "%08X" % list(S.st["trace"])[-1])
    print(s, res[s], flush=True)
print("secs", round(time.time()-t))
