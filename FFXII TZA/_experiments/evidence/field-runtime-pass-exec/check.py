#!/usr/bin/env python
"""EXP-106 field-runtime-pass-exec: execute the per-frame field pass
that CONTRACT-field-runtime-pass leaves "not executed" -- the pass body
0025DA5C..0025DEF1 plus its 49-callee closure, and the wait resolver
0025DF00 as co-subject.

Subjects (all shipped bytes under Unicorn):
  0025D9E0  PASS   whole function incl. the already-covered entry gate
                   (re-executed for stack discipline: the +0x11-bit2 path
                   jumps back into the gate epilogue)
  0025DF00  WRES   wait-slot resolver: 8-arm kind dispatch on a shipped
                   jump table, proceed/mark semantics, settle tail

Key measured semantics (from disassembly):
  gate:  00583920 busy -> ret 1; republish +0x11bit0 = +0x10>>7;
         +0x13==0 && !(+0x10&1) refuse; +0x11&8 refuse; 0032F6E0(slot)
         -> 0026A5F0 -> ret1; !(+0x10&1) -> ret1; 003603C0() -> ret1
  head:  +0x17&0x10 -> 0025E400(slot,slot+1) ret1; +0x11&4 -> ret1;
         publish 02099D70=slot, 02099D78=focus(003590D0->003588B0)
  +0x10<0x80 -> fold2: per actor 00358940+0025DF00(+25B740 on slot0),
         r12d &= rec+0x14>>6; tails 25C170/25B250/25B820
  +0x10>=0x80 -> slot0 deferred block (00377DB0/0032F6C0/globals gate
         -> 0032FC30(1,0xD4) + latch bit3); drive loop on +0x12!=0:
         exit A (settled bit6: +0x12 publish + 002620E0 init core) vs
         exit B (nibble clear: straight tail); +0x12==0 -> roster loop
         (4 members at 0209A1F0, mask bits, +0x200 bit1), fold1, +0x11
         bit1 set/clear, slot0 post-chain, bit7 republish of ebp
  tail:  slot0 -> 0025B600; ++d[+0x24]; ++d[+0x38]; ret r12d

Scripted boundaries (disclosed): 0025E4C0 interpreter (14.6KB VM --
its own contract), 00261F90 audio, 0032FC30 deferred request, the
002620E0 external chain (259B30/3E8980/25ACA0/17D490/26FAD0/379860/
379290/3DE920/363B40/3601C0), lifecycle helpers 25B600/25B740/25B820/
25C170/25B250/25E400/26A5F0/233AA0/263660/250960/259FB0/268690/3B7130/
2E1C40/254A90/234150/2EFD20/2F1A30/183070/2677B0/3148D0/314DA0/
2E4380/2E45E0/2E5610/263050/261F90-chain, planted fn-ptrs.

EXE: FFXII_TZA.exe sha256 73461d08..721f8, image base 0x120000.
"""
import ctypes, hashlib, json, struct, sys
from unicorn import Uc, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE, UC_HOOK_MEM_UNMAPPED, UC_PROT_ALL
from unicorn.x86_const import *

EXE = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe"
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
IMG_LO, IMG_HI = 0x120000, 0x2F800000
HEAP, STACK, RETQ, IMG32 = 0x40000000, 0x60000000, 0x62000000, 0x50000000

# ---- subjects -------------------------------------------------------------
PASS_ = 0x0025D9E0          # whole pass (gate + body, 1253B)
WRES  = 0x0025DF00          # wait resolver (1228B)

# ---- hooked real bodies ----------------------------------------------------
NOOP  = 0x0016D6A0          # shipped no-op ('d')
COOKIE = 0x00808C40         # stack-cookie check (silent)

# gate + global leaf getters (real; token = name)
F_BUSY  = 0x00583920        # dword[0x2CA99E8]                       ('busy')
F_PSLT  = 0x0032F6E0        # byte[0x22C6D20+slot]                   ('pslt')
F_GT3   = 0x003603C0        # byte[0x22CB726]                        ('gt3')
F_FH    = 0x003590D0        # dword[0x22C7FE0] focus handle          ('fh')
F_DEFR  = 0x00377DB0        # dword[0x2ADD0D8]                       ('dfr')
F_PCHK  = 0x0032F6C0        # qword[0x22C6E48+slot*8] & ~1           ('pck')
F_610   = 0x00361010        # byte[[0x22CBA50]+ecx*2] & 1            ('g610')
F_D60   = 0x00360D60        # qword[0x22CBA58] != 0                  ('gd60')
F_B40   = 0x0037CB40        # qword[0x2ADD968] == 0                  ('gb40')
F_8F0   = 0x003135C0        # 37C8F0 thunk target                  ('g8f0')
F_860   = 0x00303EC0        # 37C860 thunk target                  ('g860')
F_RC    = 0x0020E600        # rcx + [0x1F83530]                      ('rc')
F_D0    = 0x003148D0        # read-modify dword helper             ('gd0')
F_DA0   = 0x00314DA0        # write dword helper                   ('gda0')
F_REC   = 0x00358940        # record by ordinal                    ('grec')
F_RES   = 0x003588B0        # focus/record resolver (EXP-102)        ('gres')
F_550   = 0x003DB550        # [rcx+0xA0]+idx*20 accessor           ('g550')
F_9B8   = 0x00359B80        # [[rcx+0x30]] ? 31AD90 : 0            ('g9b8')
F_TAD   = 0x0031AD90        # 359B80 thunk target                  ('gtad')
F_97B   = 0x002E97B0        # [rcx+0xC0] getter                    ('g97b')
F_A71   = 0x003DA710        # two optional dword copies            ('ga71')
F_B64   = 0x003DB640        # wait checker (field read)            ('gb64')
F_C05   = 0x003DC050        # wait checker (field read)            ('gc05')
F_4A1   = 0x002E4A10        # preamble field body                  ('g4a1')
F_DDA   = 0x001EDDA0        # predicate leaf                       ('gdda')
HOOKS = {F_BUSY: "busy", F_PSLT: "pslt", F_GT3: "gt3", F_FH: "fh",
         F_DEFR: "dfr", F_PCHK: "pck", F_610: "g610", F_D60: "gd60",
         F_B40: "gb40", F_8F0: "g8f0", F_860: "g860", F_RC: "rc",
         F_D0: "gd0", F_DA0: "gda0", F_REC: "grec", F_RES: "gres",
         F_550: "g550", F_9B8: "g9b8", F_TAD: "gtad", F_97B: "g97b",
         F_A71: "ga71", F_B64: "gb64", F_C05: "gc05", F_4A1: "g4a1",
         F_DDA: "gdda", NOOP: "d", COOKIE: "K"}

# globals the real bodies touch (all image BSS; planted per case)
G_BUSY  = 0x02CA99E8        # dword busy flag
G_PSLT  = 0x022C6D20        # per-slot byte table (32F6E0)
G_GT3   = 0x022CB726        # gate byte (3603C0)
G_FH    = 0x022C7FE0        # focus handle dword (3590D0)
G_DEFR  = 0x02ADD0D8        # deferred counter (377DB0)
G_PCHK  = 0x022C6E48        # per-slot qword table (32F6C0, &~1)
G_610T  = 0x022CBA50        # ptr -> byte table (361010)
G_D60   = 0x022CBA58        # qword !=0 test (360D60)
G_B40   = 0x02ADD968        # qword ==0 test (37CB40)
G_E40   = 0x022BDEB4        # 2EFE40 write target
G_E50   = 0x022BDEB0        # 2EFE50 write target
G_A80   = 0x022CBA90        # 363A80 write target
G_RCV   = 0x01F83530        # 20E600 resolve base
G_777   = 0x022C7F88        # 357760/357770 dword
G_SLOT  = 0x02099D70        # published slot block
G_FOC   = 0x02099D78        # published focus record
G_DFA   = 0x020990A8        # deferred flag A (&1)  -- aliases slot1+0x10
G_DFB   = 0x020990AB        # deferred flag B (or)  -- aliases slot1+0x13
G_ROST  = 0x0209A1F0        # party roster (4 qwords)
G_CLF   = 0x02099DA7        # test-then-clear flag
G_SARR  = 0x02098E10        # slot array base (idx*0x288)
G_SKIP  = 0x022C7F85        # wres skip-publish dword (25E109)
G_STAB  = 0x022C6F28        # settle row table (stride 0x740, +0x284)
G_760   = 0x02099DE0        # 265760's read (1ED180 chain)
G_S1    = 0x02098E20        # 265270 read A (1ED130 chain)
G_S2    = 0x02098E58        # 265270 read B
G_A6F   = 0x02099ABC        # 26A5F0 read
G_DEF2  = 0x022C6D1D        # 32FC30 byte read
G_9D90  = 0x02099D80        # wres record publish (25E0BE/25E11E)

# ---- scripted stubs (qret-controlled returns) --------------------------------
S_INTERP = 0x0025E4C0       # bytecode interpreter -- boundary contract
S_AUDIO  = 0x00261F90       # audio subsystem
S_DREQ   = 0x0032FC30       # deferred mode request (arg capture)
S_LC     = 0x0025B600       # common-tail lifecycle (slot0)
S_L740   = 0x0025B740       # fold2 slot0 helper
S_L820   = 0x0025B820       # fold2 tail helper 3
S_L170   = 0x0025C170       # fold2 tail helper 1
S_L250   = 0x0025B250       # fold2 tail helper 2
S_E400   = 0x0025E400       # early-exit helper (b17&0x10)
S_A5F    = 0x0026A5F0       # gate per-slot helper
S_3AA    = 0x00233AA0       # roster slot0 helper
S_366    = 0x00263660       # slot0-chain tail
S_096    = 0x00250960       # slot0-chain (flag clear path)
S_9FB    = 0x00259FB0       # slot0-chain
S_869    = 0x00268690       # slot0-chain
S_B71    = 0x003B7130       # slot0-chain (37C8F0!=0 arm)
S_1C4    = 0x002E1C40       # slot0-chain
S_4A9    = 0x00254A90       # slot0-chain
S_341    = 0x00234150       # slot0-chain
S_FD2    = 0x002EFD20       # slot0-chain gate
S_1A3    = 0x002F1A30       # fold1->+0x11bit1 gate
S_830    = 0x00183070       # slot0-chain
S_77B    = 0x002677B0       # slot0-chain gate
S_8D0    = 0x003148D0       # read src for 314DA0 -- REAL (see HOOKS)
S_IC_B   = 0x00259B30       # init-core chain
S_IC_C   = 0x003E8980
S_IC_D   = 0x0025ACA0
S_IC_E   = 0x0017D490
S_IC_F   = 0x0026FAD0
S_IC_G   = 0x00379860
S_IC_H   = 0x00379290
S_IC_I   = 0x003DE920
S_IC_J   = 0x00363B40
S_IC_K   = 0x003601C0
S_EFB    = 0x002EF2B0       # 2620E0 + pass: leaf getter -- REAL below
S_860T   = 0x00269860       # settle-mark helper (roster/fold arms)
S_A70    = 0x002EFA70       # slot0-chain
S_AA7    = 0x003EAA70       # esi mapper (b17>=0x80 path)
S_B2A    = 0x003DB2A0       # wres arm5 checker
S_BF6    = 0x003DBF60       # wres arm3 checker
S_74B    = 0x002674B0       # wres arm5 checker
S_742    = 0x00267420       # wres arm7 checker
S_2A0    = 0x003DB2A0
S_310    = 0x002E6310       # settle tail branch A
S_81E    = 0x002681E0       # settle tail notify
S_503    = 0x002E5030       # settle tail notify 2
S_EF0    = 0x003E6EF0       # settle row call A
S_8B0    = 0x003E68B0       # settle row call B
S_A702   = 0x003E6A70       # settle row call C
S_6F0    = 0x0026D6F0       # preamble velocity helper
S_760W   = 0x00357760       # wres: clears G_777 -- REAL leaf below
S_770W   = 0x00357770       # wres: reads G_777 -- REAL leaf below
S_1D1    = 0x001ED180       # wres loop predicate A (closure)
S_DE8    = 0x001EDE80       # wres loop predicate B (closure)
S_1D3    = 0x001ED130       # wres post-interp predicate
S_C5C    = 0x001EC5C0       # wres r15+0x28 gate A
S_C5E    = 0x001EC5E0       # wres r15+0x28 gate B
S_280    = 0x003DB280       # drive-loop dead-path helper (nibble arm)
S_575    = 0x002E5750       # settle tail notify 3 (rdi,ebp,&l40)
S_E7D    = 0x0017E7D0       # slot0-chain head helper
QSTUBS = {
    S_INTERP: "interp", S_AUDIO: "audio", S_DREQ: "dreq",
    S_LC: "lc", S_L740: "l740", S_L820: "l820", S_L170: "l170",
    S_L250: "l250", S_E400: "e400", S_A5F: "a5f", S_3AA: "a3aa",
    S_366: "x366", S_096: "x096", S_9FB: "x9fb", S_869: "x869",
    S_B71: "xb71", S_1C4: "x1c4", S_4A9: "x4a9", S_341: "x341",
    S_FD2: "xfd2", S_1A3: "x1a3", S_830: "x830", S_77B: "x77b",
    S_IC_B: "icb", S_IC_C: "icc", S_IC_D: "icd", S_IC_E: "ice",
    S_IC_F: "icf", S_IC_G: "icg", S_IC_H: "ich", S_IC_I: "ici",
    S_IC_J: "icj", S_IC_K: "ick", S_A70: "xa70",
    S_AA7: "xaa7", S_B2A: "xb2a", S_BF6: "xbf6", S_74B: "x74b",
    S_742: "x742", S_310: "x310", S_81E: "x81e", S_503: "x503",
    S_EF0: "xef0", S_8B0: "x8b0", S_A702: "xa70", S_6F0: "x6f0",
    S_280: "x280", S_575: "x575", S_E7D: "xe7d", S_1D1: "xd1",
    S_DE8: "xde8", S_1D3: "xd3", S_C5C: "xc5c", S_C5E: "xc5e",
}

# additional real leaves folded into HOOKS
for va, tok in ((0x00357760, "g760"), (0x00357770, "g770"),
                (0x002EF2B0, "gefb"), (0x003135C0, "g8f0"),
                (0x00303EC0, "g860"), (0x001EC560, "gc56"),
                (0x00265760, "g576"), (0x002E0540, "ge05"),
                (0x00314910, "g491"), (0x0022A030, "ga03"),
                (0x0022A080, "ga08"), (0x00265270, "g527"),
                (0x0020AA30, "gaa3"), (0x0020AA40, "gaa4"),
                (0x002EFE40, "xe40"), (0x002EFE50, "xe50"),
                (0x00363A80, "xa80"), (0x00377C20, "g7c2"),
                (0x003148F0, "g48f"), (0x002EF640, "gf64"),
                (0x00269860, "x986"), (0x0016D6A0, "d"),
                (HEAP + 0x900000, "cb")):
    HOOKS[va] = tok

# HOOKS whose return register is undefined/stale: token only, no =rv
NOWATCH = {F_A71, F_4A1, 0x00357760, 0x002EFE40, 0x002EFE50,
           0x00363A80}

# ---- fixture layout (heap) ---------------------------------------------------
SLOT   = G_SARR             # slot block lives at its real BSS address
RECTAB = HEAP + 0x000000    # slot+8 record table {+0:count,+8:ptrs}
REC    = HEAP + 0x100000    # record[0] (the driven record)
REC2   = HEAP + 0x180000    # record[1]
REC3   = HEAP + 0x200000    # record[2]
MEMA   = HEAP + 0x280000    # roster member record A
MEMB   = HEAP + 0x300000    # roster member record B
WAIT   = HEAP + 0x380000    # wait-list base (0x28 stride)
WSUB   = HEAP + 0x400000    # record+0xA0 sub-table (3DB550, 20B stride)
WCTX   = HEAP + 0x480000    # record+0xB8 context (preamble path)
ROW    = HEAP + 0x500000    # settle row table base (0x740 stride, G_STAB ptr)
WNODE  = HEAP + 0x580000    # 2E97B0's returned node (rec+0xC0)
R40    = HEAP + 0x600000    # record+0x40 target obj
T610   = HEAP + 0x680000    # 361010's byte table (G_610T target)
OBJ0   = HEAP + 0x700000    # slot+0 object (ordinal at +0x50)
FOCREC = HEAP + 0x780000    # resolved focus record
FTAB   = HEAP + 0x7C0000    # focus family record table {+0:count,+8:ptrs}
SCR    = HEAP + 0x800000    # scratch stub bodies
RSLOT  = HEAP + 0x880000    # resolver slot block for wres entries
CB     = HEAP + 0x900000    # record+0x38 callback target body
WSUB2  = HEAP + 0x980000    # [wctx+0xF0] preamble sub-object
MODEOBJ = HEAP + 0xA00000   # 30D9A0's mode object ([0x2EBF190]->+0x5B04)
M7T    = HEAP + 0xA80000    # 377C20's lookup table ([0x2ADF700])


def qw(v): return struct.pack("<Q", v & 0xFFFFFFFFFFFFFFFF)
def dw(v): return struct.pack("<I", v & 0xFFFFFFFF)
def hw(v): return struct.pack("<H", v & 0xFFFF)
def s32(v):
    v &= 0xFFFFFFFF
    return v - 0x100000000 if v & 0x80000000 else v


def load_image():
    raw = open(EXE, "rb").read()
    assert hashlib.sha256(raw).hexdigest() == SHA, "EXE hash mismatch"
    pe = struct.unpack_from("<I", raw, 0x3C)[0]
    nsec = struct.unpack_from("<H", raw, pe + 6)[0]
    optsz = struct.unpack_from("<H", raw, pe + 20)[0]
    secs, off = [], pe + 24 + optsz
    for _ in range(nsec):
        vs, va, rs, ra = struct.unpack_from("<IIII", raw, off + 8)
        secs.append((va, vs, ra, rs))
        off += 40
    return raw, secs


def img(raw, secs, va, n):
    rva = va - IMG_LO
    for sva, vs, ra, rs in secs:
        if sva <= rva and rva + n <= sva + vs:
            return raw[ra + rva - sva: ra + rva - sva + n]
    raise KeyError("va %x not in image" % va)


class GuestMem:
    def __init__(self, uc):
        self.uc, self.bufs, self.regions = uc, [], []
    def map(self, addr, size, init=b""):
        buf = ctypes.create_string_buffer(size)
        if init:
            ctypes.memmove(buf, init, min(len(init), size))
        self.bufs.append(buf)
        self.uc.mem_map_ptr(addr, size, UC_PROT_ALL, ctypes.addressof(buf))
        self.regions.append((addr, size, ctypes.addressof(buf)))
    def _ptr(self, addr, n):
        for base, size, ptr in self.regions:
            if base <= addr and addr + n <= base + size:
                return ptr + (addr - base)
        raise KeyError("fixture access to unmapped guest addr %x" % addr)
    def w(self, addr, data):
        ctypes.memmove(self._ptr(addr, len(data)), bytes(data), len(data))
    def r(self, addr, n):
        return ctypes.string_at(self._ptr(addr, n), n)


def fields(base, spec, w):
    for off, v in spec.get("b", {}).items():  w(base + off, bytes([v & 0xFF]))
    for off, v in spec.get("h", {}).items():  w(base + off, hw(v))
    for off, v in spec.get("d", {}).items():  w(base + off, dw(v))
    for off, v in spec.get("f", {}).items():  w(base + off, struct.pack("<f", v))
    for off, v in spec.get("q", {}).items():  w(base + off, qw(v))


RECS = {"rec": REC, "rec2": REC2, "rec3": REC3,
        "mema": MEMA, "memb": MEMB}


class World:
    def __init__(self, case, raw, secs):
        self.case = case
        self.planted = {}
        self.uc = Uc(UC_ARCH_X86, UC_MODE_64)
        gm = self.gm = GuestMem(self.uc)
        gm.map(IMG_LO, IMG_HI - IMG_LO)
        for sva, vs, ra, rs in secs:
            if vs and rs:
                gm.w(IMG_LO + sva, raw[ra:ra + min(rs, vs)])
        gm.map(HEAP, 0x1000000)
        gm.map(IMG32, 0x400000)
        gm.map(STACK, 0x100000)

        def w(addr, data):
            gm.w(addr, data)
            for i, b in enumerate(data):
                self.planted[addr + i] = b
        self.w = w

        g = case.get("globals", {})
        slot = case.get("slot", 0)
        sb = SLOT + slot * 0x288
        self.slot_b = sb

        # ---- slot block ----
        sp = case.get("slotblk", {})
        w(sb + 0x00, qw(OBJ0))                   # +0 object (ordinal+0x50)
        w(OBJ0 + 0x50, hw(sp.get("ord", 0)))
        w(sb + 0x08, qw(RECTAB))                 # record table ptr
        w(sb + 0x10, bytes([sp.get("b10", 0x81)]))
        w(sb + 0x11, bytes([sp.get("b11", 0)]))
        w(sb + 0x12, bytes([sp.get("b12", 0)]))
        w(sb + 0x13, bytes([sp.get("b13", 1)]))
        w(sb + 0x17, bytes([sp.get("b17", 0)]))
        w(sb + 0x20, dw(sp.get("nact", 0)))
        w(sb + 0x28, dw(sp.get("b28", 0)))
        w(sb + 0x200, bytes([sp.get("b200", 0)]))

        # ---- record table: {+0:count, +8:ptr[]} ----
        recs = case.get("recs", [])
        w(RECTAB + 0, dw(len(recs)))
        self.recs = {}
        for i, rn in enumerate(recs):
            va = RECS.get(rn, rn) if isinstance(rn, str) else rn
            w(RECTAB + 8 + i * 8, qw(va))
            self.recs[rn] = va
        # record fixtures
        for rn, spec in case.get("rec_fields", {}).items():
            va = RECS.get(rn, rn)
            fields(va, spec, w)
            # default wiring: +0xA0 sub-table, +0xA8 wait list,
            # +0xB8 context, +0x38 callback, +0x40 obj
            if "q" not in spec or 0xA0 not in spec.get("q", {}):
                w(va + 0xA0, qw(WSUB))
            if 0xA8 not in spec.get("q", {}):
                w(va + 0xA8, qw(WAIT))
            if 0xB8 not in spec.get("q", {}):
                w(va + 0xB8, qw(WCTX))
            if 0x38 not in spec.get("q", {}):
                w(va + 0x38, qw(spec.get("cb", 0)))
            if 0x40 not in spec.get("q", {}):
                w(va + 0x40, qw(R40))

        # ---- wait slots (0x28 stride) ----
        for i, ws in enumerate(case.get("waits", [])):
            fields(WAIT + i * 0x28, ws, w)

        # ---- roster (4 qwords at G_ROST) ----
        rost = case.get("roster", [])
        for i in range(4):
            va = RECS.get(rost[i], rost[i]) if i < len(rost) else 0
            w(G_ROST + i * 8, qw(va))

        # ---- settle row + node ----
        fields(ROW + case.get("rowidx", 0) * 0x740, case.get("row", {}), w)
        fields(WNODE, case.get("wnode", {}), w)
        fields(WSUB, case.get("wsub", {}), w)
        fields(WCTX, case.get("wctx", {}), w)
        w(WCTX + 0xF0, qw(case.get("wctx_f0", WSUB2)))
        fields(WSUB2, case.get("wsub2", {}), w)
        fields(R40, case.get("r40", {}), w)
        fields(RSLOT, case.get("rslot", {}), w)

        # ---- focus handle -> fam-entry in slot array (263FF0 shape) ----
        fh = g.get("fh", 0)
        if fh:
            fam = (fh >> 0x10) & 0xF
            idx = fh & 0xFFFF
            tag = (fh >> 0x14) & 0x7FF
            fb = SLOT + fam * 0x288
            w(fb + 0x00, qw(HEAP))                   # hdr ptr != 0
            w(fb + 0x08, qw(FTAB))
            w(fb + 0x10, bytes([1]))
            w(fb + 0x20, dw(idx + 1))
            w(FTAB + 0, dw(idx + 1))
            w(FTAB + 8 + idx * 8, qw(FOCREC))
            w(FOCREC + 0x16, hw(tag))

        # ---- globals ----
        w(G_BUSY, dw(g.get("busy", 0)))
        w(G_PSLT + slot, bytes([g.get("pslt", 0)]))
        w(G_GT3, bytes([g.get("gt3", 0)]))
        w(G_FH, dw(g.get("fh", 0)))
        w(G_DEFR, dw(g.get("dfr", 1)))
        w(G_PCHK + 1 * 8, qw(g.get("pck", 0)))    # 32F6C0(ecx=1) const idx
        w(G_610T, qw(T610))
        w(G_D60, qw(g.get("d60", 0)))
        w(G_B40, qw(g.get("b40", 0)))
        w(G_RCV, qw(g.get("rcv", 0)))             # 20E600 additive base
        w(G_777, dw(g.get("g777", 0)))
        # G_DFA/G_DFB alias slot1+0x10/+0x13 -- skip when slot=1 so the
        # slotblk fixture isn't clobbered (deferred block is slot0-only)
        if slot != 1:
            w(G_DFA, bytes([g.get("dfa", 0)]))
            w(G_DFB, bytes([g.get("dfb", 0)]))
        w(G_CLF, bytes([g.get("clf", 0)]))
        w(G_SKIP, dw(g.get("skip", 0)))
        w(G_760, dw(g.get("g760", 0)))
        # G_S1/G_S2 alias slot0+0x10/+0x48 -- only when a wres case opts in
        if "gs1" in g:
            w(G_S1, qw(g["gs1"]))
        if "gs2" in g:
            w(G_S2, qw(g["gs2"]))
        # 1EDDA0 globals (shipped nonzero) -- only when a case overrides
        if "gdda1" in g:
            w(0x1DFE0C0, dw(g["gdda1"]))
        if "gdda2" in g:
            w(0x1F82E38, dw(g["gdda2"]))
        w(G_A6F, dw(g.get("a6f", 0)))
        w(G_DEF2, bytes([g.get("def2", 0)]))
        w(G_STAB, qw(ROW))                       # row-table base ptr (0x740 stride)
        for i, v in g.get("t610", {}).items():
            w(T610 + i * 2, bytes([v & 0xFF]))
        # 30D9A0 mode chain: [0x2EBF190]->obj, b[obj+0x5B04]=mode byte
        w(0x2EBF190, qw(MODEOBJ))
        w(MODEOBJ + 0x5B04, dw(g.get("mode30", 1)))
        # 377C20 table: [0x2ADD100]->tab, d[tab+4]=bound (0 -> ret 0)
        w(0x2ADD100, qw(M7T))
        w(M7T + 4, dw(g.get("m7bound", 0)))
        # resolver-family globals (1ED180 chain, 1ED130 chain)
        for a, v in g.get("raw", {}).items():
            self.w(a, dw(v) if not isinstance(v, bytes) else v)

        # scratch bodies: planted callback + fixture ret stubs
        w(CB, b"\x31\xc0\xc3")                  # xor eax;ret (fn-ptr)
        w(SCR + 0, b"\x31\xc0\xc3")

        self.trace, self.faults, self.fired = [], [], set()
        self.quiet = 0
        for va, data in case.get("patch_bytes", []):
            gm.w(va, data)
        uc = self.uc
        uc.hook_add(UC_HOOK_MEM_UNMAPPED, self.on_bad)
        for va in (list(HOOKS) + list(QSTUBS)):
            uc.hook_add(UC_HOOK_CODE, self.on_call, begin=va, end=va)

    # HOOKS entries whose arg register is part of the evidence
    ARGTOK = {F_REC: UC_X86_REG_RDX, F_610: UC_X86_REG_RCX,
              F_DA0: UC_X86_REG_RCX, CB: UC_X86_REG_RCX,
              F_B64: UC_X86_REG_RDX, F_C05: UC_X86_REG_RDX,
              0x002EFE40: UC_X86_REG_RCX, 0x002EFE50: UC_X86_REG_RCX,
              0x00363A80: UC_X86_REG_RCX, 0x00269860: UC_X86_REG_RCX}
    # QSTUBS entries with captured args: name -> tuple of regs
    ARGSTUB = {S_DREQ: (UC_X86_REG_RCX, UC_X86_REG_RDX),
               S_INTERP: (UC_X86_REG_RDX, UC_X86_REG_R8),
               S_E400: (UC_X86_REG_RCX, UC_X86_REG_RDX),
               S_BF6: (UC_X86_REG_RDX,),
               S_AA7: (UC_X86_REG_RCX,), S_1A3: (UC_X86_REG_RCX,),
               S_FD2: (UC_X86_REG_RCX,), S_A70: (UC_X86_REG_RCX,
                       UC_X86_REG_RDX, UC_X86_REG_R8),
               S_1C4: (UC_X86_REG_RCX, UC_X86_REG_RDX),
               S_869: (UC_X86_REG_RCX,), S_096: (UC_X86_REG_RCX,
                       UC_X86_REG_RDX),
               S_B71: (UC_X86_REG_RCX, UC_X86_REG_RDX),
               S_503: (UC_X86_REG_RDX,), S_575: (UC_X86_REG_RDX,),
               S_IC_C: (UC_X86_REG_RCX,),
               S_IC_F: (UC_X86_REG_RCX, UC_X86_REG_RDX,
                        UC_X86_REG_R8),
               S_IC_G: (UC_X86_REG_RCX,),
               S_IC_I: (UC_X86_REG_RCX, UC_X86_REG_RDX,
                        UC_X86_REG_R8),
               S_IC_K: (UC_X86_REG_RCX,)}

    def on_call(self, uc, addr, size, _):
        self.fired.add(addr)
        if self.quiet:
            if addr in QSTUBS:
                self._qstub(uc, addr)
            return
        if addr in QSTUBS:
            rv = self._qstub(uc, addr)
            tok = "~" + QSTUBS[addr]
            if addr in self.ARGSTUB:
                tok += ",".join("%x" % uc.reg_read(r)
                                for r in self.ARGSTUB[addr])
            self.trace.append("%s=%d" % (tok, s32(rv)))
            return
        if addr == NOOP:
            self.trace.append("d")
        elif addr == COOKIE:
            pass
        elif addr in HOOKS:
            tok = HOOKS[addr]
            if addr in self.ARGTOK:
                tok += "%x" % uc.reg_read(self.ARGTOK[addr])
            self.trace.append(tok)
            if addr not in NOWATCH:
                self._watch_ret()
        else:
            self.trace.append("?%x" % addr)

    def _qret(self, addr):
        q = self.case.get("qret", {})
        v = q.get(addr, 0)
        if isinstance(v, list):
            self._qseq = getattr(self, "_qseq", {})
            i = self._qseq.get(addr, 0)
            self._qseq[addr] = i + 1
            return v[min(i, len(v) - 1)]
        return v

    def _qstub(self, uc, addr):
        """Scripted boundary: emulate disclosed semantics, pop the call."""
        rv = self._qret(addr)
        self._stub(rv)
        return rv

    def _stub(self, ret):
        uc = self.uc
        sp = uc.reg_read(UC_X86_REG_RSP)
        back = struct.unpack("<Q", self.gm.r(sp, 8))[0]
        uc.reg_write(UC_X86_REG_RSP, sp + 8)
        uc.reg_write(UC_X86_REG_RAX, ret & 0xFFFFFFFFFFFFFFFF)
        uc.reg_write(UC_X86_REG_RIP, back)

    def _watch_ret(self):
        uc = self.uc
        sp = uc.reg_read(UC_X86_REG_RSP)
        back = struct.unpack("<Q", self.gm.r(sp, 8))[0]
        want = sp + 8
        idx = len(self.trace) - 1
        holder = {"fired": False}

        def on_ret(uc_, a, s, _u):
            if holder["fired"]:
                return
            if uc_.reg_read(UC_X86_REG_RSP) != want:
                return
            holder["fired"] = True
            self.trace[idx] += "=%d" % s32(uc_.reg_read(UC_X86_REG_RAX))

        uc.hook_add(UC_HOOK_CODE, on_ret, begin=back, end=back)

    def on_bad(self, uc, access, addr, size, value, _):
        self.faults.append(("MEM", hex(addr), "access=%d" % access,
                            "rip=%x" % uc.reg_read(UC_X86_REG_RIP)))
        return False


class Fx:
    def __init__(self, planted):
        self.p = planted
    def b(self, a):   return self.p.get(a, 0)
    def h(self, a):   return self.b(a) | (self.b(a + 1) << 8)
    def d(self, a):   return self.h(a) | self.h(a + 2) << 16
    def q(self, a):   return self.d(a) | self.d(a + 4) << 32


# ---- model -----------------------------------------------------------------

class M:
    def __init__(self, w):
        self.w = w
        self.t = []
        self.obs = []
        self.qret = {}

    def emit(self, s):
        self.t.append(s)
        return len(self.t) - 1
    def done(self, i, r):
        self.t[i] += "=%d" % s32(r)
        return r
    def _qr(self, va):
        """qret value with sequence support (mirrors World._qret)."""
        v = self.qret.get(va, 0)
        if isinstance(v, list):
            self._qs = getattr(self, "_qs", {})
            i = self._qs.get(va, 0)
            self._qs[va] = i + 1
            return v[min(i, len(v) - 1)]
        return v
    def _s(self, va, tag, rv=None, args=()):
        """scripted stub token: ~tag<arg,arg>=rv"""
        r = self._qr(va) if rv is None else rv
        t = "~" + tag + ",".join("%x" % a for a in args)
        self.emit("%s=%d" % (t, s32(r)))
        return r
    def _set(self, addr, n, v):
        # last-write-wins per (addr, width): obs are final-memory asserts
        self.obs = [o for o in self.obs if (o[0], o[1]) != (addr, n)]
        self.obs.append((addr, n, v))
        for i in range(n):
            self.w.p[addr + i] = (v >> (8 * i)) & 0xFF


def model(case, w):
    m = M(w)
    m.qret = dict(case.get("qret", {}))
    m.g = case.get("globals", {})
    m.case = case
    if case.get("entry", "pass") == "pass":
        return m_pass(m, case, w)
    return m_wres(m, case, w)


def _gb(m, a):   return m.w.b(a)
def _gh(m, a):   return m.w.h(a)
def _gd(m, a):   return m.w.d(a)


def m_pass(m, c, w):
    slot = c.get("slot", 0)
    sb = SLOT + slot * 0x288
    sp = c.get("slotblk", {})
    b10 = sp.get("b10", 0x81)
    b11 = sp.get("b11", 0)
    b12 = sp.get("b12", 0)
    b13 = sp.get("b13", 1)
    b17 = sp.get("b17", 0)
    b28 = sp.get("b28", 0)
    nact = sp.get("nact", 0)
    b200 = sp.get("b200", 0)
    g = m.g

    # ---- entry gate (25d9e0) ----
    m.emit("busy=%d" % g.get("busy", 0))                  # 583920()
    if g.get("busy", 0):
        return _eax(m, 1)
    # republish +0x11bit0 = +0x10>>7
    b11 = (b11 & ~1) | ((b10 >> 7) & 1)
    m._set(sb + 0x11, 1, b11)
    skip_pslt = (b13 == 0 and not (b10 & 1)) or (b11 & 8)
    if not skip_pslt:
        m.emit("pslt=%d" % g.get("pslt", 0))              # 32F6E0(slot)
        if g.get("pslt", 0):
            m._s(S_A5F, "a5f")                            # 26A5F0(slot)
            return _eax(m, 1)
    if not (b10 & 1):
        return _eax(m, 1)
    m.emit("gt3=%d" % g.get("gt3", 0))                    # 3603C0()
    if g.get("gt3", 0):
        return _eax(m, 1)

    # ---- head ----
    if b17 & 0x10:
        m._s(S_E400, "e400", args=(slot, slot + 1))       # 25E400(slot,slot+1)
        return _eax(m, 1)
    if b11 & 4:
        return _eax(m, 1)                                 # via 25da3f
    fh = g.get("fh", 0)
    m.emit("fh=%d" % fh)                                  # 3590D0
    foc = 0
    if fh:
        fam = (fh >> 0x10) & 0xF
        idx = fh & 0xFFFF
        tag = (fh >> 0x14) & 0x7FF
        fb = SLOT + fam * 0x288
        ires = m.emit("gres")                             # 3588B0(fh)
        if fam < 5 and w.q(fb + 8) and w.q(fb) \
           and idx < w.d(fb + 0x20) and (w.b(fb + 0x10) & 1) \
           and idx < w.d(w.q(fb + 8)):
            elem = w.q(w.q(fb + 8) + 8 + idx * 8)
            if elem and w.h(elem + 0x16) == tag:
                foc = elem
        m.done(ires, foc)
    m._set(G_SLOT, 8, sb)
    m._set(G_FOC, 8, foc)
    r12 = 1
    r14 = slot                                            # r14d = slot

    if b10 < 0x80:
        # ---- fold2 path ----
        recs = c.get("recs", [])
        for i in range(nact):
            rdi = _rec(m, sb, i, recs)
            if rdi is None:
                break
            m_wres_body(m, c, w, sb, rdi)
            if r14 == 0:
                m._s(S_L740, "l740")
            r12 &= (w.b(rdi + 0x14) >> 6)                 # folds bits6-7
        m._s(S_L170, "l170")
        m._s(S_L250, "l250")
        m._s(S_L820, "l820")
        return _tail(m, c, w, sb, r12, r14)

    # ---- b10>=0x80: slot0 deferred block ----
    if r14 == 0:
        m.emit("dfr=%d" % g.get("dfr", 1))                # 377DB0
        if g.get("dfr", 1) == 0:
            return _eax(m, 1)                             # 25dedb epilogue
        if not (b10 & 0x10):
            if not (b10 & 8):
                m._s(S_DREQ, "dreq", args=(1, 0xD4))      # 32FC30(1,0xD4)
                b10 |= 8
                m._set(sb + 0x10, 1, b10)
                return _eax(m, 1)                         # epilogue eax=1
            pck = (g.get("pck", 0) & 0xFFFFFFFF) & ~1       # d[..]&~1
            m.emit("pck=%d" % pck)                        # 32F6C0(1)
            if pck:
                return _eax(m, 1)
            if (g.get("dfa", 0) & 1) | g.get("dfb", 0):
                return _eax(m, 1)
            b10 |= 0x10
            m._set(sb + 0x10, 1, b10)
    # 25db22
    if b12 != 0:
        # ---- drive loop ----
        ord_ = w.h(w.q(sb) + 0x50)
        rdi = _rec(m, sb, 0, c.get("recs", []),
                   ordinal=(ord_ ^ 0x8000) - 0x8000)      # movsx
        if rdi is None:
            return _fault(m, "0x18")                      # wres reads [0+0x18]
        r12 = 0
        while True:
            m_wres_body(m, c, w, sb, rdi)
            cl = w.b(rdi + 0x14)
            if cl & 0x40:
                # exit A: clear pending, init core, tail
                m._set(sb + 0x12, 1, 0)
                b10 = _initcore(m, c, w, sb, b10)
                return _tail(m, c, w, sb, r12, r14)
            if not (cl & 0xF):
                return _tail(m, c, w, sb, r12, r14)       # exit B
            m._s(S_280, "x280")                           # 3DB280 dead-path
    else:
        # ---- b12==0: audio + gate chain + roster/folds ----
        m._s(S_AUDIO, "audio")                            # 261F90
        ebp = 0
        if b17 >= 0x80:
            ebp = 1                                       # ebp = r12d = 1
            esi = _g48f(m)                                # 3148F0
            _gefb(m)                                      # 2EF2B0
            if _gb(m, G_EFB + 0x1063) & 0x40:             # b[gefb+0x1063]&0x40
                _gefb(m)
                esi = _gb(m, G_EFB + 0x1534)              # movzx b[+0x1534]
            else:
                esi = s32(m._s(S_AA7, "xaa7", args=(esi,)))  # 3EAA70
            # gate chain (25dbc8..25dbf6)
            clear = False
            if esi >= 0:
                bit = _gb(m, T610 + esi * 2) & 1
                m.emit("g610%x=%d" % (esi, bit))
                if bit == 0:
                    _mode_chain(m, g)
                m.emit("gd60=%d" % (1 if g.get("d60", 0) else 0))
                if not g.get("d60", 0):
                    clear = True
            else:
                v = _mode_chain(m, g)
                if not v:
                    clear = True
                else:
                    m.emit("gd60=%d" % (1 if g.get("d60", 0) else 0))
                    if not g.get("d60", 0):
                        clear = True
            if clear:
                b17 &= 0x7F
                m._set(sb + 0x17, 1, b17)
        if b10 & 0x20:
            ebp = 1
            m.emit("gb40=%d" % (1 if g.get("b40", 0) == 0 else 0))
            if g.get("b40", 0) == 0:                      # sete -> clear
                b10 &= 0xDF
                m._set(sb + 0x10, 1, b10)
        if b17 >= 0x80 or (b10 & 0x20):
            b10 = (b10 & 0x7F) | (ebp << 7)
            m._set(sb + 0x10, 1, b10)
            return _tail(m, c, w, sb, r12, r14)
        b10 = _initcore(m, c, w, sb, b10)                 # 2620E0 pre-roster
        if b200 & 2:
            # ---- roster loop ----
            # 25dc39: eax=1 -> d[rsp+0x68]=1 (flag), ebp=1 (mask),
            # r12d=edi=0, r14d=edi=0 (member mask accum), r15d=edi=0
            r12 = 0
            ebp_mask = 1                                  # rol ebp,1 per iter
            r14m = 0
            rost = c.get("roster", [])
            for i in range(4):
                va = RECS.get(rost[i], rost[i]) if i < len(rost) else 0
                if not va:
                    r14m |= ebp_mask
                else:
                    if b28 == 0 and not (w.b(va + 8) & 0x40):
                        if not (b17 & 4):
                            i986 = m.emit("x986%x" % va)  # 269860(rc)
                            m.done(i986, 0)               # early ret
                        m._set(va + 8, 1, w.b(va + 8) | 0x40)
                    if w.b(va + 0x10) != 0:
                        m_wres_body(m, c, w, sb, va)
                        r12 &= (w.b(va + 0x14) >> 6) & 1
                        if w.b(va + 0x10) == 0:
                            r14m |= ebp_mask
                    else:
                        r14m |= ebp_mask
                ebp_mask = ((ebp_mask << 1) | (ebp_mask >> 7)) & 0xFF
            if r14m == 0xF:
                b200 &= 0xFD
                m._set(sb + 0x200, 1, b200)
                if b28 == 0:
                    m._s(S_3AA, "a3aa")
            if b200 & 2:
                b10 = (b10 & 0x7F) | 0x80                 # ebp=[rsp+0x68]=1
                m._set(sb + 0x10, 1, b10)
                return _tail(m, c, w, sb, r12, r14)
            ebp = 1                                       # [rsp+0x68] init 1
        # ---- fold1 ----
        recs = c.get("recs", [])
        for i in range(nact):
            rdi = _rec(m, sb, i, recs)
            if rdi is None:
                break
            if b28 == 0 and not (w.b(rdi + 8) & 0x40):
                if not (b17 & 4):
                    i986 = m.emit("x986%x" % rdi)         # 269860(rc)
                    m.done(i986, 0)
                m._set(rdi + 8, 1, w.b(rdi + 8) | 0x40)
            if w.b(rdi + 0x10) != 0:
                ebp = 1
                m_wres_body(m, c, w, sb, rdi)
                r12 &= (w.b(rdi + 0x14) >> 6) & 1
        rv1a3 = m._s(S_1A3, "x1a3", args=(1,))            # 2F1A30(1)
        if rv1a3 and r14 == 0:
            b11 |= 2
            m._set(sb + 0x11, 1, b11)
        if b11 & 2:
            b11 &= 0xFD
            ebp = 1
            m._set(sb + 0x11, 1, b11)
        # ---- slot0 post-chain (b28==0, ebp==0) ----
        if b10 >= 0x80 and ebp == 0 and b28 == 0:
            m._s(S_E7D, "xe7d")                           # 17E7D0
            m.emit("xa801")                               # 363A80(1) real leaf
            m._set(G_A80, 1, 1)
            if _mode1(m, g):
                m._s(S_B71, "xb71", args=(0, 1))          # 3B7130(0,1)
            rvfd2 = m._s(S_FD2, "xfd2", args=(2,))        # 2EFD20(2)
            if rvfd2:
                m.emit("xe406")                           # 2EFE40(6)
                m._set(G_E40, 4, 6)
                m.emit("xe50ff")                          # 2EFE50(0xFF)
                m._set(G_E50, 4, 0xFF)
                m._s(S_830, "x830")
                m._s(S_A70, "xa70", args=(2, 8, 1))
                rv77b = m._s(S_77B, "x77b")
                if rv77b:
                    m._s(S_869, "x869", args=(9,))
                    i = m.emit("gd0")                     # 3148D0 (gefb inside)
                    _gefb(m)
                    dv = _gd(m, G_EFB + 0x1054)
                    m.done(i, dv)
                    masked = dv & 0xFFFFFFE7
                    i = m.emit("gda0%x" % masked)         # 314DA0(ecx)
                    _gefb(m)
                    m.done(i, G_EFB)                      # rax stays gefb ret
                    m._set(G_EFB + 0x1054, 4, masked)
            m._s(S_1C4, "x1c4", args=(1, 2))              # 2E1C40(1,2)
            b10 &= 0x7F
            m._s(S_4A9, "x4a9")
            m._s(S_9FB, "x9fb")
            m._s(S_341, "x341")
            if g.get("clf", 0):
                m._s(S_096, "x096", args=(0, 0))
                m._set(G_CLF, 1, 0)
            m._s(S_366, "x366")
            m._set(sb + 0x10, 1, b10)
        b10 = (b10 & 0x7F) | (ebp << 7)
        m._set(sb + 0x10, 1, b10)
        return _tail(m, c, w, sb, r12, r14)


def _mode1(m, g):
    """37C8F0 (3135C0): 30D9A0()==1. Nested g7c2/g491 inside."""
    i = m.emit("g8f0")
    mo = _mode30(m, g)
    m.done(i, 1 if mo == 1 else 0)
    return mo == 1


def _mode2(m, g):
    """37C860 (303EC0): 30D9A0()==2."""
    i = m.emit("g860")
    mo = _mode30(m, g)
    m.done(i, 1 if mo == 2 else 0)
    return mo == 2


def _mode_chain(m, g):
    """37C8F0 then 37C860 if mode!=1. Returns truthy if either hit."""
    if _mode1(m, g):
        return True
    return _mode2(m, g)


G_F64   = 0x02164280        # 2EF640 lea target
G_EFB   = 0x02164480        # gefb = gf64+0x200


def _gefb(m):
    """2EF2B0: gf64()+0x200 -> 0x2164480. Nested gf64 inside."""
    i = m.emit("gefb")
    j = m.emit("gf64")
    m.done(j, G_F64)                                      # 2EF640: lea rip
    m.done(i, G_EFB)


def _g48f(m):
    """3148F0: gefb(); max(0, s32 d[gefb+0x1044]). Nested gefb/gf64."""
    i = m.emit("g48f")
    _gefb(m)
    return m.done(i, max(0, s32(_gd(m, G_EFB + 0x1044))))


def _g7c2(m):
    """377C20: g48f(); tab=[0x2ADD100]; !tab or eax>=d[tab+4] -> 0;
    else bit15 of LE word at tab+eax*3+8. Nested g48f/gefb/gf64."""
    i = m.emit("g7c2")
    eax = _g48f(m)
    tab = m.w.q(0x2ADD100)
    rv = 0
    if tab and eax < m.w.d(tab + 4):
        rv = (m.w.h(tab + eax * 3 + 8) >> 15) & 1
    m.done(i, rv)
    return rv


def _mode30(m, g):
    """30D9A0: dword bit-scan. bit3->5,bit2->4,377C20!=0->3,bit1->2,bit0->1."""
    mb = g.get("mode30", 1) & 0xF
    if mb & 8:
        return 5
    if mb & 4:
        return 4
    if _g7c2(m):
        return 3
    if mb & 2:
        return 2
    return mb & 1


def _rec(m, sb, i, recs, ordinal=None):
    """358940: record table lookup. edx arg is the table index."""
    edx = ordinal if ordinal is not None else i
    rv = RECS.get(recs[edx], recs[edx]) if 0 <= edx < len(recs) else 0
    m.emit("grec%x=%x" % (edx & 0xFFFFFFFF, rv))
    return rv or None


def _eax(m, v):
    return {"trace": m.t, "eax": v, "obs": m.obs}


def _fault(m, addr):
    return {"trace": m.t, "fault": str(addr), "obs": m.obs}


def _tail(m, c, w, sb, r12, r14):
    """common tail 25decb: r14==0 -> 25B600; ++d[+0x24]; ++d[+0x38]."""
    if r14 == 0:
        m._s(S_LC, "lc")
    m._set(sb + 0x24, 4, w.d(sb + 0x24) + 1)
    m._set(sb + 0x38, 4, w.d(sb + 0x38) + 1)
    return _eax(m, r12)


def _initcore(m, c, w, sb, b10):
    """2620E0: b28!=0 -> silent ret; !(b10&4) -> chain + b10|=4;
    always 3601C0(0xB), 3601C0(0xC) when reached.
    Returns the effective b10 byte (callers republish it)."""
    if w.d(sb + 0x28) != 0:
        return b10                                        # silent early ret
    if not (b10 & 4):
        m._s(S_IC_B, "icb")                               # 259B30
        m._s(S_IC_C, "icc", args=(0,))                    # 3E8980(0)
        m._s(S_IC_D, "icd")                               # 25ACA0
        for ecx in (0, 0x1F):
            rv = m._s(S_IC_E, "ice")                      # 17D490
            if s32(rv) > 0:
                rv = m._s(S_IC_E, "ice")                  # 17D490 again
            else:
                _gefb(m)
                rv = (w.b(G_EFB + 0x1060) ^ 0x80) - 0x80 + 1
            m._s(S_IC_F, "icf",
                 args=(ecx, rv & 0xFFFFFFFF, w.d(sb + 0x28)))
        rv = m._s(S_IC_E, "ice")
        if s32(rv) > 0:
            rv = m._s(S_IC_E, "ice")
        else:
            _gefb(m)
            rv = (w.b(G_EFB + 0x1060) ^ 0x80) - 0x80 + 1
        m._s(S_IC_G, "icg", args=(rv & 0xFFFFFFFF,))      # 379860(eax)
        m._s(S_IC_H, "ich")                               # 379290
        m._s(S_IC_I, "ici", args=(0, 1, 0))               # 3DE920(0,1,0)
        m._s(S_IC_J, "icj")                               # 363B40
        b10 |= 4
        m._set(sb + 0x10, 1, b10)
    m._s(S_IC_K, "ick", args=(0xB,))                      # 3601C0(0xB)
    m._s(S_IC_K, "ick", args=(0xC,))                      # 3601C0(0xC)
    return b10


def m_wres(m, c, w):
    sp = c.get("slot_p", RSLOT)
    rp = c.get("rec_p", REC)
    sp = RECS.get(sp, sp)
    rp = RECS.get(rp, rp)
    m_wres_body(m, c, w, sp, rp)
    return {"trace": m.t, "obs": m.obs}


def m_wres_body(m, c, w, r15, rdi, label=""):
    """0025DF00 transcription. r15=slotblock, rdi=record."""
    b18 = w.b(rdi + 0x18)
    if b18 != 1:
        m.emit("g4a1")
        # 2E4A10: b[rdi+3]&0xE0==0x60 -> ctx copies on [rdi+0xB8]
        if (w.b(rdi + 3) & 0xE0) == 0x60:
            ctx = w.q(rdi + 0xB8)
            for i in range(3):
                m._set(ctx + 0x10 + i * 4, 4, w.d(ctx + i * 4))
            sub = w.q(ctx + 0xF0)
            if sub and w.b(sub + 0x29):
                m._s(S_6F0, "x6f0")
    # wait loop
    while True:
        xd1 = m._s(S_1D1, "xd1")
        if xd1 != 0:
            if m._s(S_DE8, "xde8") == 0:
                break                                   # exit loop
        idx = ((w.b(rdi + 0x11) ^ 0x80) - 0x80)           # movsx
        rsi = w.q(rdi + 0xA8) + idx * 0x28
        m.emit("gdda=%d" % _wres_gdda(w))
        if _wres_gdda(w) != 0:
            m._set(rsi + 0x16, 1, 0)
        else:
            if w.b(rsi + 0x16) != 0:
                m._set(rsi + 0x16, 1, 0)
                if m._s(S_1D1, "xd1") == 0:
                    break
        kind = w.b(rsi + 0x14)
        if kind == 0 or kind > 7:
            m._set(rsi + 0x16, 1, 1)
            break
        elif kind == 5:
            if m._s(S_74B, "x74b") != 0:
                m._set(rsi + 0x16, 1, 1)
                break
            m._set(rsi + 0x14, 1, 1)
            continue
        elif kind == 3:
            i = m.emit("rc")                              # 20E600(d[+0x18])
            m.done(i, (w.d(rsi + 0x18) + w.q(G_RCV))
                   & 0xFFFFFFFFFFFFFFFF)
            if m._s(S_BF6, "xbf6", args=(w.h(rsi + 0x20),)) == 0xFF:
                m._set(rsi + 0x14, 1, 1)
                m._set(rsi + 0x27, 1, 1)
                continue
            m._set(rsi + 0x16, 1, 1)
            break
        elif kind == 6:
            i = m.emit("rc")                              # 20E600(d[+0x18])
            m.done(i, (w.d(rsi + 0x18) + w.q(G_RCV))
                   & 0xFFFFFFFFFFFFFFFF)
            edx = w.b(rsi + 0x26)
            rcx = (w.d(rsi + 0x18) + w.q(G_RCV)) & 0xFFFFFFFFFFFFFFFF
            i = m.emit("gb64%x" % edx)
            m.done(i, _b640(w, rcx, edx))
            if _b640(w, rcx, edx) != 0:
                m._set(rsi + 0x16, 1, 1)
                break
            m._set(rsi + 0x14, 1, 1)
            m._set(rsi + 0x27, 1, 1)
            continue
        elif kind == 7:
            if m._s(S_742, "x742") != 0:
                m._set(rsi + 0x16, 1, 1)
                break
            m._set(rsi + 0x14, 1, 1)
            m._set(rsi + 0x27, 1, 1)
            continue
        elif kind == 4:
            c5 = _c050(m, w, rdi, rsi)
            if c5 == 0xFF:
                m._set(rsi + 0x16, 1, 1)
                break
            m._s(S_B2A, "xb2a")
            m._set(rsi + 0x14, 1, 1)
            continue
        else:
            # kinds 1,2: interpreter arm
            m._set(G_9D90, 8, rdi)
            m.emit("g760")
            m._set(G_777, 4, 0)
            rv = m._s(S_INTERP, "interp", args=(rdi, rsi))
            if rv != 0:
                _post_mark(m, w, rsi)
                break
            if m._s(S_1D3, "xd3") != 0:
                v28 = w.d(r15 + 0x28)
                if 0 <= v28 - 1 <= 1:
                    if m._s(S_C5C, "xc5c") == 0:
                        _post_mark(m, w, rsi)
                        break
            if w.d(r15 + 0x28) == 3:
                if m._s(S_C5E, "xc5e") != 0:
                    _post_mark(m, w, rsi)
                    break
            if w.d(G_SKIP) == 0:
                m._set(G_9D90, 8, 0)
                break
            _post_mark(m, w, rsi)
            break
    _settle(m, c, w, r15, rdi)


def _b640(w, rcx, edx):
    """3DB640: bt w[rcx+6], edx -> 0/1. Emitted as gb64 by caller."""
    return (w.h(rcx + 6) >> edx) & 1


def _post_mark(m, w, rsi):
    """25e111: g770()==0 -> +0x16=1; G_9D90=0."""
    i = m.emit("g770")
    rv = w.d(G_777)                                      # 357770 reads it
    m.done(i, rv)
    if rv == 0:
        m._set(rsi + 0x16, 1, 1)
    m._set(G_9D90, 8, 0)


def _wres_gdda(w):
    """1EDDA0: ret0 iff d[0x1DFE0C0]==0 && d[0x1F82E38]!=0; else 1."""
    return 0 if (w.d(0x1DFE0C0) == 0 and w.d(0x1F82E38) != 0) else 1


def _c050(m, w, rdi, rsi):
    """3DC050(rcx=rdi, edx=movsx b[rdi+0x11], r8d=d[rsi]-d[rdi+0x58]).
    Chained row scan on [rdi+0xA0] (20B rows): start idx b[rdi+0x61],
    hop bound b[rdi+0x89]; row matches when d[row+0xC]==r8d and
    movsx b[row+2]==edx -> return row idx; else follow b[row]; 0xFF end."""
    edx = ((w.b(rdi + 0x11) ^ 0x80) - 0x80)
    i = m.emit("gc05%x" % (edx & 0xFFFFFFFF))
    r8d = (w.d(rsi) - w.d(rdi + 0x58)) & 0xFFFFFFFF
    tab = w.q(rdi + 0xA0)
    r9, r10, r11 = w.b(rdi + 0x61), 0, w.b(rdi + 0x89)
    rv = 0xFF
    while r9 != 0xFF:
        row = tab + r9 * 20
        if w.d(row + 0xC) == r8d \
           and ((w.b(row + 2) ^ 0x80) - 0x80) == edx:
            rv = r9
            break
        if r10 > r11:
            break
        r9 = w.b(row)
        r10 += 1
    m.done(i, rv)
    return rv


def _settle(m, c, w, r15, rdi):
    """25e12b settle tail."""
    esi = 0
    m._set(rdi + 0x108, 4, 0)
    if (w.d(rdi + 0x1C) & 0x800) and not (w.b(rdi + 0x14) & 0x40):
        i = m.emit("g550")
        # 3DB550(rdi, zx b[rdi+0x62]): edx==0xFF -> rax=0 (native
        # then reads [rax+4] -> fault); else [rdi+0xA0]+edx*20
        rax = 0 if w.b(rdi + 0x62) == 0xFF else w.q(rdi + 0xA0) \
              + w.b(rdi + 0x62) * 20
        m.done(i, rax)
        r14w = w.h(rax + 4)
        if w.b(rdi + 0x18) != 1:
            ax = w.h(rdi + 0xDE)
            if ax == 0xFFFF:
                ecx = w.d(w.q(rdi + 0x40) + 0x18)
                i = m.emit("rc")                          # 20E600
                base = (ecx + w.q(G_RCV)) & 0xFFFFFFFFFFFFFFFF
                m.done(i, base)
                base = ((ecx + w.q(G_RCV)) & 0xFFFFFFFF) + w.q(r15)
                w0 = (w.h(base) ^ 0x8000) - 0x8000        # s16 word
                # cmp 0xB,w; jge -> r12w stays 0xFFFF
                r12w = (0xFFFF if w0 <= 0xB else
                        (w.h(base + 0x18) ^ 0x8000) - 0x8000) & 0xFFFF
            else:
                r12w = ax
            if r12w and r14w == r12w:
                esi = 1
                m._set(rdi + 0xC, 1, w.b(rdi + 0xC) | 1)
            else:
                m._set(rdi + 0xC, 1, w.b(rdi + 0xC) & ~1)
        else:
            m._set(rdi + 0xC, 1, w.b(rdi + 0xC) & ~1)
    else:
        m._set(rdi + 0xC, 1, w.b(rdi + 0xC) & ~1)
    m._set(rdi + 0xD, 1, w.b(rdi + 0xD) & ~0x40)
    if w.b(rdi + 0x10) == 0 and ((w.b(rdi + 0x14) & 0x40) or esi):
        i = m.emit("g9b8")
        rax = 0
        if w.q(rdi + 0x30):
            rax = w.q(rdi + 0x30) + 0xED0                   # 31AD90: obj+0xED0
            j = m.emit("gtad")
            m.done(j, rax)
        m.done(i, rax)
        edx = w.d(rax + 0x40) if rax else 0
        ecx = (((w.b(rdi + 0x13) & 2) | (w.b(rdi + 9) >> 6)) >> 1) | edx
        if ecx == 0 and (w.b(rdi + 0x14) & 0x10) and w.b(rdi + 0x18) == 0 \
           and not (w.b(rdi + 9) & 0x20) and w.q(rdi + 0x38):
            m._set(rdi + 0xD, 1, w.b(rdi + 0xD) | 0x40)
            i = m.emit("cb%x" % w.d(r15 + 0x28))          # rcx=d[r15+0x28]
            m.done(i, 0)                                  # planted xor;ret
    if ((w.b(rdi + 0x13) & 1) | w.d(rdi + 0x10C)) != 0 \
       and not (w.b(rdi + 0xB) & 0x20):
        m._s(S_310, "x310")
        return
    i = m.emit("g97b")
    rbx = w.q(rdi + 0xC0)
    m.done(i, rbx)
    esi = 0                                                # 25e255 reset
    ebp = 0
    if rbx:
        m._set(rbx + 0x10, 1, w.b(rbx + 0x10) & ~4)
        if w.d(rbx) != 0xFFFFFFFF:
            if (w.b(rdi + 3) & 0xE0) == 0x60:
                m.emit("ga71")                            # 3DA710 locals
            ax = w.h(rbx)
            row = 0
            if ax != 0xFFFF:
                row = (w.q(G_STAB) + ((ax ^ 0x8000) - 0x8000) * 0x740) \
                      & 0xFFFFFFFFFFFFFFFF
            if row and w.d(row + 0x284) != esi:
                m._s(S_EF0, "xef0")
            ecx = 0
            if row and w.d(row + 0x284) != esi:
                ecx = m._s(S_8B0, "x8b0")
            eax = ecx if (w.b(rdi + 0xD) & 2) else 0
            if eax and row and w.d(row + 0x284) != esi:
                rv = m._s(S_A702, "xa70")
                if rv != 0:
                    esi = (rv >> 1) & 1
                    if rv & 1:
                        ebp = 1
        m._set(rbx + 0x10, 1,
               (w.b(rbx + 0x10) & ~4) | ((esi & 1) << 2))
        if esi:
            m._set(rdi + 0xC, 1, w.b(rdi + 0xC) | 0x10)
    m._s(S_81E, "x81e")
    m._s(S_503, "x503", args=(esi,))
    m._s(S_575, "x575", args=(ebp,))


def compare(case, world):
    w = Fx(world.planted)
    exp = model(case, w)
    got = " ".join(world.trace)
    expt = " ".join(exp.get("trace", []))
    import re
    norm = lambda s: re.sub(r"[0-9a-f]{6,}", "A", s)
    ok = norm(got) == norm(expt)
    diffs = []
    if not ok:
        diffs.append("trace")
    if "eax" in exp:
        gv = world.uc.reg_read(UC_X86_REG_RAX)
        if s32(gv) != s32(exp["eax"]):
            ok = False
            diffs.append("eax got=%x exp=%x" % (s32(gv), s32(exp["eax"])))
    for addr, n, v in exp.get("obs", []):
        gv = int.from_bytes(world.gm.r(addr, n), "little")
        if gv != v:
            ok = False
            diffs.append("obs %x got=%x exp=%x" % (addr, gv, v))
    if "fault" in exp:
        if not world.faults:
            ok = False
            diffs.append("expected fault, none")
        else:
            faddr = int(world.faults[0][1], 16)
            if faddr != int(exp["fault"], 16):
                ok = False
                diffs.append("fault got=%s exp=%s"
                             % (world.faults[0][1], exp["fault"]))
    elif world.faults:
        ok = False
        diffs.append("faults %s" % world.faults[:2])
    return ok, diffs, got, expt


def build_cases():
    C = []
    def add(name, **kw):
        kw["name"] = name
        C.append(kw)

    # ---- gate ------------------------------------------------------------
    add("gate-busy", globals={"busy": 1})
    add("gate-idle-refuse", slotblk={"b10": 0x80, "b13": 0})
    add("gate-pslt", globals={"pslt": 1})
    add("gate-b10clear", slotblk={"b10": 0x80})
    add("gate-b11bit8", slotblk={"b11": 8}, globals={"gt3": 1})
    add("gate-b11bit8-b10", slotblk={"b10": 0x80, "b11": 8})
    add("gate-b13-taken", slotblk={"b10": 0x81, "b13": 0})
    # ---- head --------------------------------------------------------------
    add("head-e400", slotblk={"b17": 0x10})
    add("head-b11bit2", slotblk={"b11": 4})
    # ---- fold2 (b10 < 0x80) -------------------------------------------------
    add("fold2-idle", slotblk={"b10": 1})
    add("fold2-focus",
        slotblk={"b10": 1},
        globals={"fh": 0x00010000 | (2 << 0x14)})
    add("fold2-rec",
        slotblk={"b10": 1, "nact": 1}, recs=["rec"],
        rec_fields={"rec": {"b": {0x18: 1, 0x14: 0x40}}},
        waits=[{"b": {0x14: 0}}])
    add("fold2-rec2",
        slotblk={"b10": 1, "nact": 2}, recs=["rec", "rec2"],
        rec_fields={"rec":  {"b": {0x18: 1, 0x14: 0x40}},
                    "rec2": {"b": {0x18: 1, 0x14: 0xC0}}},
        waits=[{"b": {0x14: 0}}])
    add("fold2-slot1", slot=1,
        slotblk={"b10": 1, "nact": 1}, recs=["rec"],
        rec_fields={"rec": {"b": {0x18: 1, 0x14: 0x40}}},
        waits=[{"b": {0x14: 0}}])
    # ---- deferred block ----------------------------------------------------
    add("deferred-dfr0", globals={"dfr": 0})
    add("deferred-dreq", slotblk={"b10": 0x81})
    add("deferred-pck", slotblk={"b10": 0x89}, globals={"pck": 2})
    add("deferred-dfa", slotblk={"b10": 0x89}, globals={"dfa": 1})
    add("deferred-dfb", slotblk={"b10": 0x89}, globals={"dfb": 1})
    add("deferred-latch", slotblk={"b10": 0x89, "b12": 0},
        globals={"pck": 0, "dfa": 0, "dfb": 0})
    # ---- drive loop --------------------------------------------------------
    add("drive-exit-a",
        slotblk={"b10": 0x91, "b12": 1, "ord": 0}, recs=["rec"],
        rec_fields={"rec": {"b": {0x18: 1, 0x14: 0x40}}},
        waits=[{"b": {0x14: 0}}])
    add("drive-exit-b",
        slotblk={"b10": 0x91, "b12": 1, "ord": 0}, recs=["rec"],
        rec_fields={"rec": {"b": {0x18: 1, 0x14: 0x00}}},
        waits=[{"b": {0x14: 0}}])
    add("drive-fault", slotblk={"b10": 0x91, "b12": 1, "ord": 5},
        recs=["rec"])
    # ---- audio path ----------------------------------------------------------
    add("audio-base", slotblk={"b10": 0x91, "b12": 0})
    add("audio-b28", slotblk={"b10": 0x91, "b12": 0, "b28": 1})
    add("audio-fold1",
        slotblk={"b10": 0x91, "b12": 0, "nact": 1}, recs=["rec"],
        rec_fields={"rec": {"b": {0x18: 1, 0x14: 0x40, 0x10: 1}}},
        waits=[{"b": {0x14: 0}}])
    # ---- roster --------------------------------------------------------------
    add("roster-settle",
        slotblk={"b10": 0x91, "b12": 0, "b200": 2},
        roster=["mema", 0, 0, 0],
        rec_fields={"mema": {"b": {0x08: 0, 0x10: 0}}})
    add("roster-active",
        slotblk={"b10": 0x91, "b12": 0, "b200": 2},
        roster=["mema", 0, 0, 0],
        rec_fields={"mema": {"b": {0x08: 0, 0x10: 1, 0x18: 1, 0x14: 0x40}}},
        waits=[{"b": {0x14: 0}}])
    add("roster-busy",
        slotblk={"b10": 0x91, "b12": 0, "b200": 2},
        roster=["mema", "memb", 0, 0],
        rec_fields={"mema": {"b": {0x08: 0, 0x10: 1, 0x18: 1, 0x14: 0x40}},
                    "memb": {"b": {0x08: 0, 0x10: 1, 0x18: 1, 0x14: 0x40}}},
        waits=[{"b": {0x14: 0}}])
    # ---- b17 >= 0x80 chain ----------------------------------------------------
    add("b17-mode", slotblk={"b10": 0x91, "b12": 0, "b17": 0x80})
    add("b17-clear", slotblk={"b10": 0x91, "b12": 0, "b17": 0x80},
        globals={"d60": 0, "mode30": 0})
    add("b17-t610", slotblk={"b10": 0x91, "b12": 0, "b17": 0x80},
        globals={"t610": {1: 1}}, qret={S_AA7: 1})
    add("b10-20", slotblk={"b10": 0xB1, "b12": 0}, globals={"b40": 0})
    add("b10-20-keep", slotblk={"b10": 0xB1, "b12": 0}, globals={"b40": 1})
    # ---- slot0 post-chain ------------------------------------------------------
    add("chain-fd2", slotblk={"b10": 0x91, "b12": 0},
        qret={S_FD2: 1})
    add("chain-77b", slotblk={"b10": 0x91, "b12": 0},
        globals={"raw": {0x21654D4: 0x1F}},
        qret={S_FD2: 1, S_77B: 1})
    add("chain-clf", slotblk={"b10": 0x91, "b12": 0},
        globals={"clf": 1})
    add("chain-x1a3", slotblk={"b10": 0x91, "b12": 0, "b11": 2},
        qret={S_1A3: 1})
    # ---- wres direct entries ---------------------------------------------------
    add("wres-kind0", entry="wres",
        rec_fields={"rec": {"b": {0x18: 1, 0x14: 0x40}}},
        waits=[{"b": {0x14: 0}}])
    add("wres-kind1", entry="wres",
        rec_fields={"rec": {"b": {0x18: 1, 0x14: 0x40}}},
        waits=[{"b": {0x14: 1}}])
    add("wres-kind1-interp1", entry="wres",
        rec_fields={"rec": {"b": {0x18: 1, 0x14: 0x40}}},
        waits=[{"b": {0x14: 1}}],
        qret={S_INTERP: 1})
    add("wres-kind3", entry="wres",
        rec_fields={"rec": {"b": {0x18: 1, 0x14: 0x40}}},
        waits=[{"b": {0x14: 3, 0x18: 0, 0x20: 1}}],
        qret={S_BF6: 0})
    add("wres-kind3-miss", entry="wres",
        rec_fields={"rec": {"b": {0x18: 1, 0x14: 0x40}}},
        waits=[{"b": {0x14: 3, 0x18: 0, 0x20: 1}}],
        qret={S_BF6: 0xFF})
    add("wres-kind4", entry="wres",
        rec_fields={"rec": {"b": {0x18: 1, 0x14: 0x40, 0x58: 0, 0x61: 0,
                                  0x89: 3}}},
        wsub={"d": {0x0C: 7}, "b": {0x02: 0, 0x00: 0xFF}},
        waits=[{"b": {0x14: 4}, "d": {0x00: 7}}],
        qret={S_B2A: 0})
    add("wres-kind4-miss", entry="wres",
        rec_fields={"rec": {"b": {0x18: 1, 0x14: 0x40, 0x61: 0xFF}}},
        waits=[{"b": {0x14: 4}}])
    add("wres-kind5", entry="wres",
        rec_fields={"rec": {"b": {0x18: 1, 0x14: 0x40}}},
        waits=[{"b": {0x14: 5}}], qret={S_74B: 0})
    add("wres-kind5-stop", entry="wres",
        rec_fields={"rec": {"b": {0x18: 1, 0x14: 0x40}}},
        waits=[{"b": {0x14: 5}}], qret={S_74B: 1})
    add("wres-kind6", entry="wres",
        rec_fields={"rec": {"b": {0x18: 1, 0x14: 0x40}}},
        waits=[{"b": {0x14: 6, 0x26: 2}, "d": {0x18: WSUB}}],
        wsub={"h": {0x06: 4}})
    add("wres-kind6-proceed", entry="wres",
        rec_fields={"rec": {"b": {0x18: 1, 0x14: 0x40}}},
        waits=[{"b": {0x14: 6, 0x26: 2}, "d": {0x18: WSUB}}],
        wsub={"h": {0x06: 0}})
    add("wres-kind7", entry="wres",
        rec_fields={"rec": {"b": {0x18: 1, 0x14: 0x40}}},
        waits=[{"b": {0x14: 7}}], qret={S_742: 0})
    add("wres-kind8", entry="wres",
        rec_fields={"rec": {"b": {0x18: 1, 0x14: 0x40}}},
        waits=[{"b": {0x14: 8}}])
    add("wres-preamble", entry="wres",
        rec_fields={"rec": {"b": {0x18: 0, 0x14: 0x40, 0x03: 0x60}}},
        wsub2={"b": {0x29: 1}},
        waits=[{"b": {0x14: 0}}])
    add("wres-xd1-exit", entry="wres",
        rec_fields={"rec": {"b": {0x18: 1, 0x14: 0x40}}},
        qret={S_1D1: 1, S_DE8: 0})
    add("wres-settle-cb", entry="wres",
        rec_fields={"rec": {"b": {0x18: 0, 0x14: 0x50, 0x10: 0,
                                  0x13: 0, 0x09: 0},
                            "q": {0x38: CB}}},
        waits=[{"b": {0x14: 0}}],
        rslot={"d": {0x28: 3}})
    add("wres-settle-row", entry="wres",
        rec_fields={"rec": {"b": {0x18: 1, 0x14: 0x40, 0x0D: 2},
                            "q": {0xC0: WNODE}}},
        wnode={"d": {0x00: 1}, "b": {0x10: 7}},
        rowidx=1, row={"d": {0x284: 1}},
        qret={S_8B0: 1, S_A702: 3},
        waits=[{"b": {0x14: 0}}])
    add("wres-settle-x310", entry="wres",
        rec_fields={"rec": {"b": {0x18: 1, 0x14: 0x40, 0x13: 1}}},
        waits=[{"b": {0x14: 0}}])
    add("wres-settle-800", entry="wres",
        rec_fields={"rec": {"b": {0x18: 0, 0x62: 0, 0x0D: 0x40},
                            "d": {0x1C: 0x800},
                            "h": {0xDE: 5}}},
        wsub={"h": {0x04: 5}},
        waits=[{"b": {0x14: 0}}])
    add("wres-settle-800miss", entry="wres",
        rec_fields={"rec": {"b": {0x18: 0, 0x62: 0},
                            "d": {0x1C: 0x800},
                            "h": {0xDE: 9}}},
        wsub={"h": {0x04: 5}},
        waits=[{"b": {0x14: 0}}])
    return C


def run_case(case, raw, secs):
    world = World(case, raw, secs)
    uc = world.uc
    ent = case.get("entry", "pass")
    entry = {"pass": PASS_, "wres": WRES}[ent]
    sp = STACK + 0x80000
    uc.reg_write(UC_X86_REG_RSP, sp)
    world.w(sp, qw(RETQ))
    if ent == "pass":
        uc.reg_write(UC_X86_REG_RCX, case.get("slot", 0))
    else:
        sp_ = case.get("slot_p", RSLOT)
        rp_ = case.get("rec_p", REC)
        uc.reg_write(UC_X86_REG_RCX, RECS.get(sp_, sp_))
        uc.reg_write(UC_X86_REG_RDX, RECS.get(rp_, rp_))
    uc.reg_write(UC_X86_REG_RIP, entry)
    try:
        uc.emu_start(entry, RETQ, count=900000)
    except Exception as e:
        world.faults.append(("EMU", str(e),
                             "rip=%x" % uc.reg_read(UC_X86_REG_RIP)))
    return world


def build_mutants():
    M = []
    def add(name, va, orig, patch):
        M.append({"name": name, "va": va,
                  "orig": bytes.fromhex(orig),
                  "patch": bytes.fromhex(patch)})
    # ---- gate / head ----
    add("m-stride",    0x25D9F9, "88020000", "90020000")  # slot stride
    add("m-rep-shr",   0x25DA16, "07", "06")              # shr al,7 -> 6
    add("m-gate-b13",  0x25DA22, "01", "02")              # test cl,1 -> 2
    add("m-gate-b11b8", 0x25DA28, "08", "04")             # test b11,8 -> 4
    add("m-gate-b10t", 0x25DA50, "01", "02")              # test b10,1 -> 2
    add("m-head-b17",  0x25DA5F, "10", "20")              # b17 mask
    add("m-e400-arg",  0x25DA64, "01", "02")              # edx +1 -> +2
    add("m-head-b11b2", 0x25DA7E, "04", "08")             # b11 mask
    add("m-r12-init",  0x25DA88, "01000000", "00000000")  # r12d=1 -> 0
    # ---- deferred / drive ----
    add("m-dreq-imm",  0x25DAE9, "d4", "d5")              # edx 0xd4
    add("m-deferred-or", 0x25DAF5, "08", "10")            # or b10,8
    add("m-deferred-flags", 0x25DB12, "0a", "22")         # or -> and
    add("m-deferred-latch", 0x25DB21, "10", "20")         # or b10,0x10
    add("m-drive-bit6", 0x25DB4E, "40", "80")             # test cl,0x40
    add("m-drive-exitA", 0x25DB4F, "75", "74")            # jne -> je
    # ---- audio / roster / fold ----
    add("m-g610-mask", 0x361029, "01", "02")              # and eax,1
    add("m-roster-or", 0x25DC91, "40", "80")              # or b+8,0x40
    add("m-roster-acc", 0x25DCBF, "440bf5", "4423f5")     # or -> and
    add("m-fold-shr",  0x25DEAA, "06", "05")              # shr eax,6
    add("m-b11-set",   0x25DD7F, "02", "04")              # or b11,2
    add("m-slot0-b10", 0x25DD96, "0f82", "0f83")          # jb -> jae
    add("m-slot0-ebp", 0x25DD9E, "0f85", "0f84")          # jne -> je
    # ---- slot0 chain ----
    add("m-xa80-arg",  0x25DDB4, "01", "02")              # lea ecx,+1
    add("m-xfd2-arg",  0x25DDCE, "02", "03")              # ecx 2 -> 3
    add("m-gda0-mask", 0x25DE21, "e7", "cf")              # and ~0x18
    add("m-clr-b10",   0x25DE39, "7f", "6f")              # and b10,0x7f
    add("m-clf-gate",  0x25DE50, "74", "75")              # je -> jne
    # ---- init core ----
    add("m-ic-b10t",   0x2620F6, "04", "80")              # test b10,4
    add("m-ic-b10or",  0x2621A7, "04", "08")              # or b10,4 -> 8
    add("m-ic-jle",    0x262115, "7e", "7f")              # jle -> jg
    add("m-icf1f",     0x26215E, "1f", "1e")              # ecx 0x1f
    add("m-ick-arg",   0x2621A9, "0b", "0a")              # ecx 0xb
    # ---- wait resolver ----
    add("m-wres-mark", 0x25E11D, "01", "00")              # mov b+0x16,1
    add("m-wres-skip", 0x25E10F, "74", "75")              # je -> jne
    add("m-wres-tbl",  0x25DFF6, "07", "06")              # cmp eax,7
    add("m-xbf6-cmp",  0x25E041, "ff", "fe")              # cmp eax,0xff
    add("m-gc05-cmp",  0x25E0A5, "ff", "fe")              # cmp eax,0xff
    add("m-settle-or", 0x25E1A3, "4008770c", "4020770c")  # or -> and
    add("m-settle-and", 0x25E1B0, "bf", "ff")             # and b+d,0xbf
    add("m-cb-set",    0x25E21A, "40", "80")              # or b+d,0x40
    add("m-node-clr",  0x25E27A, "fb", "fe")              # and b+10,0xfb
    add("m-row-je",    0x25E2E7, "74", "75")              # je -> jne
    add("m-row-td",    0x25E32B, "02", "04")              # test b+d,2
    add("m-xa70-je",   0x25E361, "74", "75")              # je -> jne
    add("m-node-shl",  0x25E37D, "02", "03")              # shl al,2 -> 3
    add("m-rec-set",   0x25E388, "10", "20")              # or b+c,0x10
    return M


MSPEC = {
    "m-stride": "fold2-slot1", "m-rep-shr": "audio-base",
    "m-gate-b13": "gate-b13-taken", "m-gate-b11b8": "gate-b11bit8",
    "m-gate-b10t": "fold2-idle", "m-head-b17": "head-e400",
    "m-e400-arg": "head-e400", "m-head-b11b2": "head-b11bit2",
    "m-r12-init": "fold2-idle", "m-dreq-imm": "deferred-dreq",
    "m-deferred-or": "deferred-dreq", "m-deferred-flags": "deferred-dfb",
    "m-deferred-latch": "deferred-latch", "m-drive-bit6": "drive-exit-a",
    "m-drive-exitA": "drive-exit-b", "m-g610-mask": "b17-t610",
    "m-roster-or": "roster-active", "m-roster-acc": "roster-settle",
    "m-fold-shr": "fold2-rec2", "m-b11-set": "chain-x1a3",
    "m-slot0-b10": "chain-fd2", "m-slot0-ebp": "chain-fd2",
    "m-xa80-arg": "chain-77b", "m-xfd2-arg": "chain-fd2",
    "m-gda0-mask": "chain-77b", "m-clr-b10": "chain-77b",
    "m-clf-gate": "chain-clf", "m-ic-b10t": "audio-base",
    "m-ic-b10or": "audio-base", "m-ic-jle": "audio-base",
    "m-icf1f": "audio-base", "m-ick-arg": "audio-base",
    "m-wres-mark": "wres-kind1-interp1", "m-wres-skip": "wres-kind1",
    "m-wres-tbl": "wres-kind7", "m-xbf6-cmp": "wres-kind3-miss",
    "m-gc05-cmp": "wres-kind4-miss", "m-settle-or": "wres-settle-800",
    "m-settle-and": "wres-settle-800", "m-cb-set": "wres-settle-cb",
    "m-node-clr": "wres-settle-row", "m-row-je": "wres-settle-row",
    "m-row-td": "wres-settle-row", "m-xa70-je": "wres-settle-row",
    "m-node-shl": "wres-settle-row", "m-rec-set": "wres-settle-row",
}


def main():
    raw, secs = load_image()
    cases = build_cases()
    res = {"exe_sha256": SHA,
           "subjects": {"pass": "0x25D9E0", "wres": "0x25DF00"},
           "cases": []}
    npass = 0
    for c in cases:
        world = run_case(c, raw, secs)
        ok, diffs, got_t, exp_t = compare(c, world)
        res["cases"].append({"name": c["name"], "ok": ok,
                             "trace": got_t, "exp": exp_t,
                             "diffs": diffs,
                             "faults": world.faults[:3]})
        if ok:
            npass += 1
        print("CASE %-4s %-22s %s" % ("ok" if ok else "FAIL",
                                      c["name"], got_t[:110]))
        if not ok:
            print("      exp: %s" % exp_t[:110])
            for d in diffs:
                print("      %s" % d)
    print("cases: %d/%d" % (npass, len(cases)))

    nk = 0
    muts = build_mutants()
    for m in muts:
        base = img(raw, secs, m["va"], len(m["orig"]))
        assert base == m["orig"], "%s site bytes %s != %s" % (
            m["name"], base.hex(), m["orig"].hex())
        cname = MSPEC[m["name"]]
        case = dict(next(c for c in cases if c["name"] == cname))
        case["patch_bytes"] = [(m["va"], m["patch"])]
        world = run_case(case, raw, secs)
        ok, diffs, got_t, exp_t = compare(case, world)
        alive = ok
        print("MUT  %-4s %-16s on %-20s %s" % ("ALIVE" if alive else "kill",
              m["name"], cname, got_t[:80]))
        if not alive:
            nk += 1
    print("mutants: %d/%d killed" % (nk, len(muts)))
    res["mutants"] = {"killed": nk, "total": len(muts)}
    res["pass"] = npass == len(cases) and nk == len(muts)
    open("result.json", "w").write(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
