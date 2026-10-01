"""S-24 D-6 probe (OPUS, 2026-09-26): the world of block 342 (check.py of s24-opus-replay-stat-derivation), plus
 - the item classifier 0031E9A0 run over the shipped item rows to find real weapons (kind 1) and shields (kind 2);
 - hooks that capture, during a foe derivation, the definition row (r13 at 002FF325) and the base / growth rows
   (rbp / rbx at 002FF32F).
No application stub, no stop boundary. Exploratory helpers shared with check.py.
"""
import hashlib
import json
import os
import struct

from unicorn import UC_HOOK_CODE
from unicorn.x86_const import UC_X86_REG_R13, UC_X86_REG_RBP, UC_X86_REG_RBX

import world as W
import shipped_pack as SP

HERE = os.path.dirname(os.path.abspath(__file__))
FX = json.load(open(os.path.join(HERE, "world.json")))
ARD_PATH = r"D:\FFXII_TZA_extract\ps2data\plan_master\in\plan_map\rsn_b\area\rsn_b.ard"
ARD = open(ARD_PATH, "rb").read()
ARD_SHA = hashlib.sha256(ARD).hexdigest()
DERIVE, BINDER, CLASSIFY = 0x2FEF30, 0x3EA710, 0x31E9A0
ITEMS = 0x2EBF0F8                       # the item-table registry slot 002FF408 / 002FF421 / 002FF434 read
W.ALLOWED |= {0x16D6A0} | SP.allowed(W) | W.closure(DERIVE) | W.closure(BINDER) | W.closure(CLASSIFY)
S = W.Session(FX["fixes"], FX["inits"])
uc = S.uc
for fam in range(15):
    for o in (0x48, 0x50):
        h = struct.unpack("<Q", bytes(uc.mem_read(0x1EEBCC0 + fam * 0x58 + o, 8)))[0]
        if h:
            W.ALLOWED |= {h} | W.closure(h)
made, skipped = SP.bind(W, S)
IDLE = 0x76200000
for i, cell in enumerate((0x209BE80, 0x1F7FFE0, 0x215E6E0, 0x209CC40)):
    uc.mem_write(IDLE + i * 0x20000, bytes(0x20000))
    uc.mem_write(cell, struct.pack("<Q", IDLE + i * 0x20000))


def w(a, fmt, *v):
    uc.mem_write(a, struct.pack(fmt, *v))


def r(a, fmt):
    return struct.unpack(fmt, bytes(uc.mem_read(a, struct.calcsize(fmt))))


BUF = 0x76400000
uc.mem_map(BUF, (len(ARD) + 0x1000 + 0xFFFF) & ~0xFFFF)
uc.mem_write(BUF + 0x1000, ARD)
assert S.call(BINDER, BUF + 0x1000), ("binder", S.st["faults"][:2], S.st["bad"][:2])

POOL, FOE, ACTOR = 0x76280000, 0x76291000, 0x762A0000
cap = {}


def grab(u, a, n, _):
    if a == 0x2FF325:
        cap["def"] = u.reg_read(UC_X86_REG_R13)
    elif a == 0x2FF32F or a == 0x2FF388:
        cap["base"], cap["growth"] = u.reg_read(UC_X86_REG_RBP), u.reg_read(UC_X86_REG_RBX)


for a in (0x2FF325, 0x2FF32F, 0x2FF388):
    uc.hook_add(UC_HOOK_CODE, grab, begin=a, end=a)


def item_row(item_id):
    hdr = r(ITEMS, "<Q")[0]
    base = r(hdr + 0xC, "<I")[0] + r(0x1F83530, "<Q")[0]      # 0020E600: rax = ecx + [01F83530]
    stride = r(hdr + 8, "<H")[0]
    return base + (item_id - 0x1000) * stride


def items_by_kind(limit=0x200):
    hdr = r(ITEMS, "<Q")[0]
    n = r(hdr + 4, "<I")[0]
    out = {}
    for k in range(min(n, limit)):
        row = item_row(0x1000 + k)
        ok = S.call(CLASSIFY, row)
        from unicorn.x86_const import UC_X86_REG_RAX
        kind = uc.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF
        out.setdefault(kind, []).append((0x1000 + k, bytes(uc.mem_read(row, 0x30)).hex()))
    return n, out


def foe(d, lo, hi, equip=(0xFFFF,) * 5):
    uc.mem_write(POOL, bytes(0xF50))
    uc.mem_write(FOE, bytes(0x400))
    w(FOE + 0x50, "<5H", *equip)
    uc.mem_write(ACTOR, bytes(0x1000))
    w(POOL + 0x10, "<Q", ACTOR)
    w(POOL + 0x698, "<Q", FOE)
    w(FOE + 5, "<B", 1)
    w(FOE + 4, "<B", d)
    w(FOE + 0x88, "<B", lo)
    w(FOE + 0x1C2, "<B", hi)
    w(0x208E688, "<Q", POOL)
    w(0x208E6A0, "<I", 1)
    cap.clear()
    ok = S.call(DERIVE, FOE, 0, 0)
    return ok, bytes(uc.mem_read(FOE, 0x60))


if __name__ == "__main__":
    n, kinds = items_by_kind()
    print("item rows", n, {k: len(v) for k, v in kinds.items()})
    for k in (1, 2):
        print("kind", k, kinds.get(k, [])[:3])
    ok, b = foe(0, 0, 50)
    print("foe d0 ok", ok, "def %X base %X growth %X" % (cap.get("def", 0), cap.get("base", 0), cap.get("growth", 0)))
    print("def+0x15 =", r(cap["def"] + 0x15, "<B")[0] if "def" in cap else None)
    print(b[0x20:0x40].hex())
