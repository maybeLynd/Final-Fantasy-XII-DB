# EXP-112 actor-record-init-exec
#
# Executes the SHIPPED bytes of the actor record-pool per-record init
# ctor 00266530 — the one body EXP-107 scripted as a boundary — under
# Unicorn, plus the real leaves it reaches.
#
#   00266530  CTOR (mgr, ptab, idx). rsi=q[mgr] (descriptor block);
#             rbx=q[ptab+8+idx*8] (record). ~150 field writes:
#             flag-byte mask chain, kind dispatch via 00266AD0 +
#             00266BD0, sub-flag table read b[0x1E0C329+kind*4]
#             (==1 -> r15d=6 & ebp stays 8, else ebp=0xA), link-byte
#             (b[entry+6]&0x80,!=0xFF) -> KTAB[link]=rbx + b_12/b_0F,
#             resolved entry offsets -> q[+0x48/0x50/0x58], 003DB580
#             slot-array init, A8 clear loop, C0-object field init +
#             00268380x2, rep stosw 0xFFFFx18 at +0xC8, link+C0 ->
#             002681E0, four 003DBB60 sites (w[rsi]>=0xA gate,
#             resolved-command-table args, three inc b[+0x10]), class
#             0x60 gate -> d[+0x1C] bit2/bit10 or-call sites, tail
#             jmp 003DB280 (queue walk + shr b[+0x63],1).
#
#   00266AD0  RMAP — 8-arm jt on kind&0x1F: writes q[+0xB8]/q[+0xC0]/
#             q[+0xA0]/q[+0xA8] (r8 + (subflag==1 ? 0xA0 : 0xC8)).
#   00266BD0  KINIT — 8-arm jt on kind&0x1F: d[+0x1C] in
#             {0,0x38,0x40,0x30004,0x34C85}, or b[+0x14],0x80 arms.
#   003DB580  SINIT — slot-array init on q[+0xA0], 0x14 stride:
#             b[+0x88]=edx, d[+0x24]=0, b[+0x89]=r8b, links
#             (b[0]=i+1,b[1]=i-1,d[+4]=0x80000000,w[+0x10]=0),
#             first/last sentinels, 0xFF x r11 pairs at +0x8C/+0x94,
#             w[+6]=0, b[+0x63]=0, w[+0x60]=0xFF00.
#   003DB280  TAIL — call 003DB6E0 then shr b[+0x63],1.
#   003DB6E0  QWALK — b[+0x63]==0 -> out (always under the ctor);
#             else walk queue, maybe 003DBDC0, b[+0x62], b[+0x14]&0x40.
#   0020E600  BASE — mov eax,ecx; add rax,[0x1F83530]; ret (base=0 in
#             image -> identity resolve).
#
# Scripted boundaries: 00265FF0 (rdx=q[+0xB8]), 00265B60, 00268380 x2,
#   002681E0, 003DBB60 x4 (edx/r8/r9/stk0 captured), 00268EA0 (DEAD —
#   b[+0xB] bit3 is masked off earlier), 003DBDC0 (DEAD — b[+0x63]==0).
#
import ctypes, hashlib, json, struct, sys

from unicorn import UC_ARCH_X86, UC_HOOK_CODE, UC_HOOK_MEM_UNMAPPED, \
    UC_MODE_64, UC_PROT_ALL, Uc
from unicorn.x86_const import UC_X86_REG_RAX, UC_X86_REG_RCX, \
    UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_R9, UC_X86_REG_RIP, \
    UC_X86_REG_RSP

EXE = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe"
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
IMG_LO, IMG_HI = 0x120000, 0x2F800000

HEAP   = 0x40000000
STACK  = 0x61000000
RETQ   = 0x62000000

CTOR   = 0x00266530
RMAP   = 0x00266AD0
KINIT  = 0x00266BD0
SINIT  = 0x003DB580
TAIL   = 0x003DB280
QWALK  = 0x003DB6E0
BASE   = 0x0020E600

# scripted boundaries
CFF0   = 0x00265FF0
CB60   = 0x00265B60
C380   = 0x00268380
C1E0   = 0x002681E0
DBB60  = 0x003DBB60
C8EA0  = 0x00268EA0
CDC0   = 0x003DBDC0

# globals the body touches
SUBF   = 0x01E0C329        # sub-flag table: b[SUBF + kind*4]
KTAB   = 0x0209A1F0        # q[0x80] kind-link table (BSS)
CELL   = 0x02F8F2A0        # registration cell (BSS): zeroed, q[+0xF8]=&it
BASEQ  = 0x01F83530        # 0020E600's addend (BSS zero -> identity)

# fixture layout
MGR    = HEAP + 0x000000
DESC   = HEAP + 0x010000
PTAB   = HEAP + 0x020000
REC    = HEAP + 0x030000
A8ARR  = HEAP + 0x040000
B8OBJ  = HEAP + 0x048000
C0OBJ  = HEAP + 0x050000
A0ARR  = HEAP + 0x060000
RECB   = 0x800               # record image bytes compared

STUBS = (CFF0, CB60, C380, C1E0, DBB60, C8EA0, CDC0)
SNAMES = {CFF0: "ff0", CB60: "b60", C380: "380", C1E0: "1e0",
          DBB60: "dbb", C8EA0: "8ea", CDC0: "dc0"}


def qw(v): return struct.pack("<Q", v & 0xFFFFFFFFFFFFFFFF)
def dw(v): return struct.pack("<I", v & 0xFFFFFFFF)
def s8(v):
    v &= 0xFF
    return v - 0x100 if v & 0x80 else v
def s16(v):
    v &= 0xFFFF
    return v - 0x10000 if v & 0x8000 else v


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


class MRec:
    """Python model of the record + neighbours the ctor writes.

    The RMAP arms point q[+0xA0]/+0xA8/+0xB8/+0xC0 INSIDE the record;
    writes through those pointers land in rec[] for kinds 0..7 and in
    the planted regions for kind>7 (or wherever the pointer points)."""
    def __init__(self, case):
        self.rec = bytearray(case.get("rec_bytes", b"\xAA" * RECB))
        self.rec[3] = case.get("b3", 0)
        # planted pointer fields (overwritten by RMAP for kinds 0..7)
        self.rec[0xA0:0xA8] = qw(case.get("a0p", A0ARR))
        self.rec[0xA8:0xB0] = qw(case.get("a8p", A8ARR))
        self.rec[0xB8:0xC0] = qw(case.get("b8", B8OBJ))
        self.rec[0xC0:0xC8] = qw(case.get("c0", C0OBJ))
        self.a0 = bytearray(b"\xBB" * 0x400)
        self.a8 = bytearray(b"\xCC" * 0x400)
        self.c0 = bytearray(b"\xDD" * 0x400)
        self.b8 = bytearray(b"\xEE" * 0x400)
        self.ktab = [case.get("ktab%d" % i, 0) for i in range(0x80)]
        self.ktab_img = {}
        for k in range(0x80):
            if self.ktab[k]:
                self.ktab_img[self.ktab[k]] = bytearray(b"\xEE" * RECB)
        self.cell = bytearray(b"\xAA" * 8)
        self.trace = []
        self.bufs = [(REC, self.rec), (A0ARR, self.a0),
                     (A8ARR, self.a8), (C0OBJ, self.c0),
                     (B8OBJ, self.b8)] + \
                    [(va, img) for va, img in self.ktab_img.items()]

    def _buf(self, va):
        for base, buf in self.bufs:
            if base <= va < base + len(buf):
                return buf, va - base
        return None, 0

    def wb(self, va, v):
        buf, off = self._buf(va)
        if buf is not None:
            buf[off] = v & 0xFF

    def wr(self, va, data):
        buf, off = self._buf(va)
        if buf is not None:
            buf[off:off + len(data)] = data

    def run(self, case):
        r = self.rec
        idx = case.get("idx", 0)
        flag0 = case.get("mgr28", 0) == 0
        fcount = self._w(DESC, case)
        kind = self.b(3) & 0x1F
        subf = case["subf"][kind]          # shipped table value
        r15 = 6 if subf == 1 else 8
        ebp = 8 if subf == 1 else 0xA

        self.sb(0x14, self.b(0x14) & 0x7F)
        self.sq(0xEC, 0)
        self.sb(0xF5, 0xFF)

        # ---- 00266AD0 region map (jt: A,B,B,C,C,D,D,D) ----
        if kind <= 7:
            arm = {0: 0, 1: 1, 2: 1, 3: 2, 4: 2, 5: 3, 6: 3, 7: 3}[kind]
            if arm == 0:
                self.sq(0xB8, 0); self.sq(0xC0, 0); r8 = REC + 0x120
            elif arm == 1:
                self.sq(0xC0, 0); self.sq(0xB8, REC + 0x120)
                r8 = REC + 0x1A0
            elif arm == 2:
                self.sq(0xC0, 0); self.sq(0xB8, REC + 0x120)
                r8 = REC + 0x140
            else:
                self.sq(0xB8, REC + 0x120); self.sq(0xC0, REC + 0x350)
                r8 = REC + 0x4D8
            self.sq(0xA0, r8)
            self.sq(0xA8, r8 + (0xA0 if subf == 1 else 0xC8))
        # kind>7: no arm — q[+0xA0]/+0xA8/+0xB8/+0xC0 untouched

        # ---- 00266BD0 kind leaf ----
        if kind <= 7:
            k1 = {0: 0, 1: 0x38, 2: 0x38, 3: 0x40, 4: 0x40,
                  5: 0x30004, 6: 0x30004, 7: 0x34C85}[kind]
            self.sd(0x1C, k1)
            if kind in (5, 7):
                self.sb(0x14, self.b(0x14) | 0x80)

        # ---- flag-byte mask chain ----
        cl = (self.b(0xD) & 0xFE) | 0x02
        cl &= 0xFB; cl &= 0xF7; cl &= 0xEF; cl &= 0xBF
        dl = (self.b(8) & 0xBF) | 0x01
        dl &= 0xDF
        if flag0:
            cl |= 0x80; dl |= 0x10
        else:
            cl &= 0x7F; dl &= 0xEF
        cl &= 0xDF; dl &= 0x7F
        self.sb(0xD, cl)
        self.sb(8, dl)
        self.sb(9, self.b(9) & 0x5F)
        self.sb(0xC, 0x08)     # ((b_c&0x70)|8)&0x8F = 8
        self.sb(0xB, self.b(0xB) & 0xC0)
        self.sb(0x13, self.b(0x13) & 0x3C)
        self.sb(0xE, 0xF0)
        self.sb(0x14, (self.b(0x14) & 0xB0) | 0x30)
        self.sb(0xF, 0)
        self.sb(0x12, 0xFF)
        self.sb(0x15, case.get("mgr28", 0) & 0xFF)
        self.sb(0xA, 0)
        self.sb(0x20, 0xFF)
        self.sw(0x00, idx & 0xFFFF)
        self.sw(0x04, 0xFF00)
        self.sw(0x10, 0)
        self.sw(0x16, 1)
        self.sw(0x21, 0)
        self.sw(0xF6, 0)
        self.sw(0x100, 0)
        self.sw(0x102, 0xFFFF)
        self.sw(0x104, 0xFFFF)
        self.sw(0x106, 0)
        self.sq(0x28, 0); self.sq(0x30, 0); self.sq(0x38, 0)
        self.sq(0x10C, 0)
        self.sq(0xF8, CELL)
        self.sd(0x18, 0xFFFF0000)
        self.sd(0x114, 0)
        self.sd(0x118, 0x3C0000)
        self.cell[0:4] = b"\x00" * 4
        if (self.b(3) & 0xE0) == 0x60:
            self.sd(0x1C, self.d(0x1C) & 0xFFFFDEFF)
        # b[+2] = (idx < w[desc + d[desc+0x14] + 2]) + 1
        offg = case.get("offg", 0x200)
        gcount = self._w(DESC + offg + 2, case)
        self.sb(2, (1 if idx < gcount else 0) + 1)
        # descriptor entry pointer
        offe = case.get("offe", 0x400)
        stride = 0x30 if fcount >= 8 else 0x20
        ent = DESC + offe + idx * stride + 4
        self.sq(0x40, ent)
        eb6 = self._b(ent + 6, case)
        # ---- link block (swap-out dead: b12==0xFF -> -1 > 3) ----
        if eb6 & 0x80 and eb6 != 0xFF:
            link = eb6 & 0x7F
            old = s8(self.b(0x12)) & 0xFFFFFFFF
            if old <= 3:
                od = self.ktab[old]
                self.ktab[old] = 0
                if od:
                    self.wr(od + 0x12, b"\xff")
                    self.wr(od + 0xF, b"\x03")
            self.ktab[link] = REC
            self.sb(0x12, link)
            self.sb(0xF, (1 if link > 3 else 0) + 2)
        # ---- resolved entry offsets ----
        self.sq(0x48, DESC + self._d(ent + 0x10, case))
        self.sq(0x50, DESC + self._d(ent + 0x14, case))
        self.sq(0x58, DESC + self._d(ent + 8, case))
        # ---- 003DB580 slot-array init (real body, modelled) ----
        self.sb(0x88, r15)
        self.sd(0x24, 0)
        self.sb(0x89, ebp)
        a0base = self.q(0xA0)
        for i in range(ebp):
            s = a0base + i * 0x14
            self.wr(s + 4, dw(0x80000000))
            self.wb(s, (i + 1) & 0xFF)
            self.wb(s + 1, (i - 1) & 0xFF)
            self.wr(s + 0x10, b"\x00\x00")
        self.wb(a0base + 1, 0xFF)
        self.wb(a0base + (ebp - 1) * 0x14, 0xFF)
        for i in range(r15):
            self.sb(0x8C + i, 0xFF)
            self.sb(0x94 + i, 0xFF)
        self.sw(6, 0)
        self.sb(0x63, 0)
        self.sw(0x60, 0xFF00)
        # ---- A8 clear loop (b[+0x88] = r15 elems, 0x28 stride) ----
        a8base = self.q(0xA8)
        for i in range(r15):
            self.wr(a8base + i * 0x28, b"\x00" * 0x17)
        # ---- boundary calls ----
        self.trace.append("ff0:%x:%x" % (REC, self.q(0xB8)))
        self.trace.append("b60:%x" % REC)
        c0 = self.q(0xC0)
        if c0:
            self.wr(c0 + 0x138, b"\x00" * 8)
            self.wr(c0 + 0x148, dw(0x3F800000))
            self.wb(c0 + 0x14E, 1)
            self.wr(c0 + 0x140, b"\x00" * 4)
            self.trace.append("380:%x" % REC)
            self.wr(c0 + 0x144, b"\x00" * 4)
            self.trace.append("380:%x" % REC)
        for i in range(0x12):
            self.sw(0xC8 + i * 2, 0xFFFF)
        if eb6 & 0x80 and eb6 != 0xFF and c0:
            self.wb(c0 + 0x152, 0)
            self.trace.append("1e0:%x" % REC)
        # ---- DBB60 sites (fcount>=0xA gates ONLY site1) ----
        tab = DESC + self._d(ent + 0x18, case)
        if fcount >= 0xA:
            # site1: w[+0xE6], bound 0xF, arg w[tab+0x20]
            r8v = self._site(0xE6, tab, 0xF, 0x20, case)
            if r8v >= 0:
                self.trace.append("dbb:%x:%x:%x:%x:%x" %
                                  (REC, r15 - 1, r8v, 2, 0))
                self.sb(0x10, (self.b(0x10) + 1) & 0xFF)
        # site2 (unconditional): edx = b88-1, r8=0
        self.trace.append("dbb:%x:%x:%x:%x:%x" %
                          (REC, r15 - 1, 0, 2, 0))
        self.sb(0x10, (self.b(0x10) + 1) & 0xFF)
        # site3: w[+0xDA], bound 9, arg w[tab+0x14], edx=esi=b88-1
        r8v = self._site(0xDA, tab, 9, 0x14, case)
        if r8v >= 0:
            self.trace.append("dbb:%x:%x:%x:%x:%x" %
                              (REC, r15 - 1, r8v, 2, 0))
            self.sb(0x10, (self.b(0x10) + 1) & 0xFF)
        # site4: w[+0xCA], bound 1, arg w[tab+4], edx=0 — no inc
        r8v = self._site(0xCA, tab, 1, 4, case)
        if r8v >= 0:
            self.trace.append("dbb:%x:%x:%x:%x:%x" %
                              (REC, 0, r8v, 2, 0))
        # ---- class-0x60 command sites (or/and on d[+0x1C]) ----
        if (self.b(3) & 0xE0) == 0x60:
            # 0xCC site: bound bp=2, arg w[tab+6] -> or 4 / and ~4
            v = self._site(0xCC, tab, 2, 6, case)
            if v >= 0:
                self.sd(0x1C, self.d(0x1C) | 4)
            else:
                self.sd(0x1C, self.d(0x1C) & ~4 & 0xFFFFFFFF)
            # 0xDC site: bound 0xA, arg w[tab+0x16]
            # ok -> |0x400 then &~4 ; fail -> &~0x400
            v = self._site(0xDC, tab, 0xA, 0x16, case)
            if v >= 0:
                self.sd(0x1C, (self.d(0x1C) | 0x400) & ~4 & 0xFFFFFFFF)
            else:
                self.sd(0x1C, self.d(0x1C) & ~0x400 & 0xFFFFFFFF)
        # ---- tail: shr b[+0x63],1 (always 0 under ctor) ----
        self.sb(0x63, self.b(0x63) >> 1)
        return self

    def _site(self, off, tab, bound, argoff, case):
        w = self.w_(off)
        if w != 0xFFFF:
            return w            # movzx literal arm (dead under ctor)
        if bound >= s16(self._w(tab, case)):
            return -1           # cmp bound, w[tab]; jge skip
        return s16(self._w(tab + argoff, case))

    # record field accessors
    def b(self, o): return self.rec[o]
    def w_(self, o): return struct.unpack_from("<H", self.rec, o)[0]
    def d(self, o): return struct.unpack_from("<I", self.rec, o)[0]
    def q(self, o): return struct.unpack_from("<Q", self.rec, o)[0]
    def sb(self, o, v): self.rec[o] = v & 0xFF
    def sw(self, o, v): struct.pack_into("<H", self.rec, o, v & 0xFFFF)
    def sd(self, o, v): struct.pack_into("<I", self.rec, o, v & 0xFFFFFFFF)
    def sq(self, o, v): struct.pack_into("<Q", self.rec, o,
                                         v & 0xFFFFFFFFFFFFFFFF)
    # fixture (descriptor / entry / tables) accessors
    def _b(self, va, case): return case["mem"].get(va, 0)
    def _w(self, va, case):
        return case["mem"].get(va, 0) | \
            (case["mem"].get(va + 1, 0) << 8)
    def _d(self, va, case):
        return case["mem"].get(va, 0) | \
            (case["mem"].get(va + 1, 0) << 8) | \
            (case["mem"].get(va + 2, 0) << 16) | \
            (case["mem"].get(va + 3, 0) << 24)


class World:
    def __init__(self, case, raw, secs, patch=()):
        self.case = case
        self.uc = Uc(UC_ARCH_X86, UC_MODE_64)
        gm = self.gm = GuestMem(self.uc)
        gm.map(IMG_LO, IMG_HI - IMG_LO)
        for sva, vs, ra, rs in secs:
            if vs and rs:
                gm.w(IMG_LO + sva, raw[ra:ra + min(rs, vs)])
        gm.map(HEAP, 0x1000000)
        gm.map(STACK, 0x100000)
        gm.map(RETQ, 0x1000)
        gm.w(RETQ, b"\xc3" + b"\xcc" * 0xFF)

        idx = case.get("idx", 0)
        fcount = case.get("fcount", 4)
        stride = 0x30 if fcount >= 8 else 0x20
        offg = case.get("offg", 0x200)
        offe = case.get("offe", 0x400)

        # mgr + descriptor
        gm.w(MGR, qw(DESC))
        gm.w(MGR + 0x28, dw(case.get("mgr28", 0)))
        gm.w(DESC + 0, struct.pack("<H", fcount))
        gm.w(DESC + 0x14, dw(offg))
        gm.w(DESC + 0x18, dw(offe))
        # pointer table + record (planted pattern)
        gm.w(PTAB + 8 + idx * 8, qw(REC))
        rec0 = bytearray(case.get("rec_bytes", b"\xAA" * RECB))
        rec0[3] = case.get("b3", 0)
        rec0[0xA0:0xA8] = qw(case.get("a0p", A0ARR))
        rec0[0xA8:0xB0] = qw(case.get("a8p", A8ARR))
        rec0[0xB8:0xC0] = qw(case.get("b8", B8OBJ))
        rec0[0xC0:0xC8] = qw(case.get("c0", C0OBJ))
        gm.w(REC, bytes(rec0))
        # record-linked arrays
        gm.w(A8ARR, b"\xCC" * 0x400)
        gm.w(A0ARR, b"\xBB" * 0x400)
        gm.w(C0OBJ, b"\xDD" * 0x400)
        gm.w(B8OBJ, b"\xEE" * 0x400)
        # note: 00266AD0 overwrites q[+0xA0]/+0xA8 — plant them AFTER
        # knowing the arm; the record's planted pointers only matter on
        # the kind>7 path.
        # descriptor group-count cell + entries
        gm.w(DESC + offg + 2, struct.pack("<H",
                                          case.get("gcount", 0)))
        ent = DESC + offe + 4 + idx * stride
        gm.w(ent + 6, bytes([case.get("eb6", 0)]))
        gm.w(ent + 8, dw(case.get("e8", 0x600)))
        gm.w(ent + 0x10, dw(case.get("e10", 0x700)))
        gm.w(ent + 0x14, dw(case.get("e14", 0x800)))
        gm.w(ent + 0x18, dw(case.get("e18", 0x900)))
        # command table (length + args)
        tab = DESC + case.get("e18", 0x900)
        gm.w(tab, struct.pack("<H", case.get("tablen", 0)))
        for k, v in case.get("tabw", {}).items():
            gm.w(tab + k, struct.pack("<H", v))
        # kind-link table (BSS global) + old records
        for i in range(8):
            old = case.get("ktab%d" % i, 0)
            gm.w(KTAB + i * 8, qw(old))
            if old:
                gm.w(old, b"\xEE" * RECB)
        # registration cell
        gm.w(CELL, b"\xAA" * 8)
        # extra planted bytes (record field overrides etc.)
        for va_, data in case.get("plants", []):
            gm.w(va_, data)
        for va_, data in patch:
            gm.w(va_, data)

        self.trace, self.faults = [], []
        uc = self.uc
        uc.hook_add(UC_HOOK_MEM_UNMAPPED, self.on_bad)
        for va in STUBS:
            uc.hook_add(UC_HOOK_CODE, self.on_stub, begin=va, end=va)

    def on_bad(self, uc, acc, addr, sz, val, _):
        self.faults.append("mem %x addr=%x" % (acc, addr))
        return False

    def on_stub(self, uc, addr, size, _):
        rcx = uc.reg_read(UC_X86_REG_RCX) & 0xFFFFFFFFFFFFFFFF
        rdx = uc.reg_read(UC_X86_REG_RDX) & 0xFFFFFFFFFFFFFFFF
        r8 = uc.reg_read(UC_X86_REG_R8) & 0xFFFFFFFFFFFFFFFF
        r9 = uc.reg_read(UC_X86_REG_R9) & 0xFFFFFFFFFFFFFFFF
        sp = uc.reg_read(UC_X86_REG_RSP)
        stk0 = struct.unpack("<Q", self.gm.r(sp + 0x28, 8))[0] \
            if addr == DBB60 else 0
        if addr == DBB60:
            self.trace.append("dbb:%x:%x:%x:%x:%x" %
                              (rcx, rdx, r8, r9, stk0))
        else:
            self.trace.append("%s:%x%s" % (SNAMES[addr], rcx,
                              ":%x" % rdx if addr == CFF0 else ""))
        uc.reg_write(UC_X86_REG_RAX, 0)
        self._pop_ret()

    def _pop_ret(self):
        uc = self.uc
        sp = uc.reg_read(UC_X86_REG_RSP)
        back = struct.unpack("<Q", self.gm.r(sp, 8))[0]
        uc.reg_write(UC_X86_REG_RSP, sp + 8)
        uc.reg_write(UC_X86_REG_RIP, back)

    def run(self):
        uc = self.uc
        idx = self.case.get("idx", 0)
        uc.reg_write(UC_X86_REG_RCX, MGR)
        uc.reg_write(UC_X86_REG_RDX, PTAB)
        uc.reg_write(UC_X86_REG_R8, idx)
        uc.reg_write(UC_X86_REG_RSP, STACK + 0x8000)
        uc.reg_write(UC_X86_REG_RIP, CTOR)
        uc.mem_write(STACK + 0x8000, struct.pack("<Q", RETQ))
        try:
            uc.emu_start(CTOR, RETQ, count=40000)
        except Exception as e:
            self.faults.append("emu %s" % e)
        return self

    def obs(self):
        gm = self.gm
        return {
            "rec": gm.r(REC, RECB),
            "a0": gm.r(A0ARR, 0x400),
            "a8": gm.r(A8ARR, 0x400),
            "c0": gm.r(C0OBJ, 0x400),
            "b8": gm.r(B8OBJ, 0x400),
            "ktab": gm.r(KTAB, 0x400),
            "cell": gm.r(CELL, 8),
            "trace": list(self.trace),
            "faults": list(self.faults),
        }


def model_case(case):
    m = MRec(case)
    m.run(case)
    return {
        "rec": bytes(m.rec),
        "a0": bytes(m.a0),
        "a8": bytes(m.a8),
        "c0": bytes(m.c0),
        "b8": bytes(m.b8),
        "ktab": b"".join(qw(v) for v in m.ktab),
        "cell": bytes(m.cell),
        "trace": m.trace,
    }


def build_cases():
    """Each case: ctor args + fixture knobs + the shipped sub-flag
    table is read from the image (not modelled by hand)."""
    cases = {}
    # baseline: kind0, flag0 set, no link, c0 planted, g<8
    cases["base-k0"] = dict(b3=0x00, mgr28=1)
    cases["flag0"] = dict(b3=0x00, mgr28=0)
    # kind sweep (sub-flag table decides r15/ebp per kind)
    for k in range(8):
        cases["kind%d" % k] = dict(b3=k, mgr28=1)
    cases["kind15"] = dict(b3=0x0F, mgr28=1)   # >7: no rmap/kinit arm
    cases["kind31"] = dict(b3=0x1F, mgr28=1)
    # class gates (high3 of b3)
    cases["cls60"] = dict(b3=0x60, mgr28=1)
    cases["cls60-k5"] = dict(b3=0x65, mgr28=1)
    cases["cls80"] = dict(b3=0x80, mgr28=1)
    cases["clsE0"] = dict(b3=0xE7, mgr28=1)
    # link byte
    cases["link0"] = dict(b3=0, mgr28=1, eb6=0x80)
    cases["link3"] = dict(b3=0, mgr28=1, eb6=0x83)
    cases["link5"] = dict(b3=0, mgr28=1, eb6=0x85)
    cases["linkff"] = dict(b3=0, mgr28=1, eb6=0xFF)
    cases["link7f"] = dict(b3=0, mgr28=1, eb6=0x7F)
    cases["link-old"] = dict(b3=0, mgr28=1, eb6=0x81,
                           ktab1=HEAP + 0x090000)
    # field-count stride + site1 gate
    cases["f7"] = dict(b3=0, mgr28=1, fcount=7)
    cases["g8"] = dict(b3=0, mgr28=1, fcount=8)
    cases["gA"] = dict(b3=0, mgr28=1, fcount=0xA)
    cases["gA-tabs"] = dict(b3=0, mgr28=1, fcount=0xA, tablen=0x20,
                           tabw={0x20: 7, 0x14: 5, 4: 3, 6: 4, 0x16: 9})
    # kind2/4/7 take the subflag==1 arm (r15=6, ebp=8)
    cases["k2-subf"] = dict(b3=2, mgr28=1)
    cases["k7-subf"] = dict(b3=7, mgr28=1)
    # record-index gates
    cases["idx3"] = dict(b3=0, mgr28=1, idx=3)
    cases["idx3-gA"] = dict(b3=0, mgr28=1, idx=3, fcount=0xA,
                           gcount=4)
    # c0 absent (kind>7 keeps planted pointers)
    cases["noc0"] = dict(b3=0x0F, mgr28=1, c0=0)
    cases["noc0-link"] = dict(b3=0x0F, mgr28=1, c0=0, eb6=0x82)
    cases["k15-c0link"] = dict(b3=0x0F, mgr28=1, eb6=0x81)
    # cls60 site5/6 fail-paths (shared tab compare word)
    cases["cls60-t2"] = dict(b3=0x60, mgr28=1, fcount=0xA, tablen=2)
    cases["cls60-s6neg"] = dict(b3=0x60, mgr28=1, fcount=0xA,
                              tablen=0x20, tabw={6: 4, 0x16: 0x8000})
    # planted record words for the four sites (non-FFFF literals)
    lit = bytearray(b"\xAA" * RECB)
    for off, v in ((0xE6, 5), (0xDA, 0x8001), (0xCA, 3)):
        lit[off:off + 2] = struct.pack("<H", v)
    cases["dbb-lit"] = dict(b3=0, mgr28=1, fcount=0xA,
                           rec_bytes=bytes(lit))
    lit2 = bytearray(b"\xAA" * RECB)
    for off, v in ((0xCC, 4), (0xDC, 6)):
        lit2[off:off + 2] = struct.pack("<H", v)
    cases["cls60-lit"] = dict(b3=0x60, mgr28=1, rec_bytes=bytes(lit2))
    lit3 = bytearray(b"\xAA" * RECB)
    lit3[0xCC:0xCE] = struct.pack("<H", 0x8004)   # negative literal
    lit3[0xDC:0xDE] = struct.pack("<H", 0x8006)
    cases["cls60-neg"] = dict(b3=0x60, mgr28=1, rec_bytes=bytes(lit3))
    # non-default entry offsets
    cases["offvals"] = dict(b3=0, mgr28=1, e8=0x610, e10=0x720,
                           e14=0x830, e18=0x940)
    return cases


def mem_of(case, secs, raw):
    """byte-level fixture map for the model's _b/_w/_d reads."""
    mem = {}
    idx = case.get("idx", 0)
    fcount = case.get("fcount", 4)
    stride = 0x30 if fcount >= 8 else 0x20
    offg = case.get("offg", 0x200)
    offe = case.get("offe", 0x400)

    def putb(va, v): mem[va] = v & 0xFF
    def putw(va, v):
        mem[va] = v & 0xFF; mem[va + 1] = (v >> 8) & 0xFF
    def putd(va, v):
        for i in range(4):
            mem[va + i] = (v >> (8 * i)) & 0xFF
    putw(DESC, fcount)
    putd(DESC + 0x14, offg)
    putd(DESC + 0x18, offe)
    putw(DESC + offg + 2, case.get("gcount", 0))
    ent = DESC + offe + 4 + idx * stride
    putb(ent + 6, case.get("eb6", 0))
    putd(ent + 8, case.get("e8", 0x600))
    putd(ent + 0x10, case.get("e10", 0x700))
    putd(ent + 0x14, case.get("e14", 0x800))
    putd(ent + 0x18, case.get("e18", 0x900))
    tab = DESC + case.get("e18", 0x900)
    putw(tab, case.get("tablen", 0))
    for k, v in case.get("tabw", {}).items():
        putw(tab + k, v)
    # shipped sub-flag table (read from the image, not transcribed)
    subf = []
    rva = SUBF - IMG_LO
    for sva, vs, ra, rs in secs:
        if sva <= rva < sva + rs:
            for k in range(32):
                subf.append(raw[ra + rva - sva + k * 4])
    case["subf"] = subf
    case["mem"] = mem
    return case


def main():
    raw, secs = load_image()
    cases = build_cases()
    npass = nfail = 0
    for name, case in sorted(cases.items()):
        case = mem_of(dict(case), secs, raw)
        exp = model_case(case)
        w = World(case, raw, secs).run()
        obs = w.obs()
        bad = []
        for k in ("rec", "a0", "a8", "c0", "b8", "ktab", "cell",
                  "trace"):
            if obs[k] != exp[k]:
                if isinstance(obs[k], (bytes, bytearray)):
                    diffs = [i for i in range(min(len(obs[k]),
                             len(exp[k]))) if obs[k][i] != exp[k][i]]
                    bad.append("%s: %d byte diffs e.g. %s" %
                               (k, len(diffs), diffs[:12]))
                else:
                    bad.append("%s:\n   obs %s\n   exp %s" %
                               (k, obs[k], exp[k]))
        if obs["faults"]:
            bad.append("faults %s" % obs["faults"])
        if bad:
            nfail += 1
            print("FAIL", name)
            for b in bad:
                print("   ", b)
        else:
            npass += 1
            print("pass", name)
    print("== %d/%d cases passed" % (npass, npass + nfail))

    # ---- mutation campaign ----
    # mutant base cases: mutbase exercises cls60 + site1 gate + link +
    # c0 (kind0); variants cover kind/subflag/tab/index-dependent sites.
    cases["mutbase"] = dict(b3=0x60, mgr28=1, fcount=0xA, eb6=0x81,
                           tablen=0x20,
                           tabw={0x20: 7, 0x14: 5, 4: 3, 6: 4,
                                 0x16: 9, 0x18: 0x8000})
    cases["mutbase-i1"] = dict(cases["mutbase"], idx=1)
    cases["mutbase-k2"] = dict(cases["mutbase"], b3=0x62)
    cases["mutbase-k5"] = dict(cases["mutbase"], b3=0x65)
    cases["mutbase-k7"] = dict(cases["mutbase"], b3=0x67)
    cases["mutbase-k16"] = dict(cases["mutbase"], b3=0x70)
    cases["mutbase-k18"] = dict(cases["mutbase"], b3=0x72)
    cases["mutbase-t2"] = dict(cases["mutbase"], tablen=2)
    cases["mutbase-t3"] = dict(cases["mutbase"], tablen=3)
    cases["mutbase-tA"] = dict(cases["mutbase"], tablen=0xA)
    cases["mutbase-tB"] = dict(cases["mutbase"], tablen=0xB)
    cases["mutbase-t16"] = dict(cases["mutbase"], tablen=0x10)
    MUTS = [
        # (name, va, orig, patch, case)
        ("m-14-7f",   0x266576, 0x7F, 0xFF, "mutbase"),
        ("m-ec-q",    0x26657D, 0xEC, 0xF0, "mutbase"),
        ("m-f5-ff",   0x266587, 0xFF, 0xFE, "mutbase"),
        ("m-kind1f",  0x266579, 0x1F, 0x0F, "mutbase-k18"),
        ("m-sf-cmp",  0x266593, 0x01, 0x02, "mutbase-k2"),
        ("m-sf-je",   0x266594, 0x75, 0x74, "mutbase-k2"),
        ("m-ebp-a",   0x26659B, 0x0A, 0x0B, "mutbase"),
        ("m-b8-mgr",  0x266649, 0x28, 0x2C, "mutbase"),
        ("m-c-8f",    0x2666AF, 0x8F, 0xFF, "mutbase"),
        ("m-e-f0",    0x26665D, 0xF0, 0x0F, "mutbase"),
        ("m-18-val",  0x2666CC, 0x00, 0x01, "mutbase"),
        ("m-118-v",   0x266634, 0x00, 0x01, "mutbase"),
        ("m-b2-setl", 0x266709, 0x9C, 0x9E, "mutbase"),
        ("m-ent-st",  0x266726, 0x04, 0x05, "mutbase-i1"),
        ("m-e10",     0x266797, 0x10, 0x14, "mutbase"),
        ("m-e14",     0x2667A8, 0x14, 0x10, "mutbase"),
        ("m-e8",      0x2667C2, 0x08, 0x0C, "mutbase"),
        ("m-a8-28",   0x266809, 0x28, 0x20, "mutbase"),
        ("m-c0-148",  0x266849, 0x48, 0x4C, "mutbase-k16"),
        ("m-1e0-g",   0x2668CE, 0x74, 0xEB, "mutbase-k5"),
        ("m-stosw",   0x2668AC, 0x12, 0x10, "mutbase"),
        ("m-wr-cnt",  0x2668E9, 0x0A, 0x0B, "mutbase"),
        ("m-e6-w",    0x2668EF, 0xE6, 0xF0, "mutbase"),
        ("m-t1-cmp",  0x26690B, 0x0F, 0x10, "mutbase-t16"),
        ("m-t1-arg",  0x26691A, 0x20, 0x22, "mutbase"),
        ("m-inc10",   0x26693C, 0x10, 0x11, "mutbase"),
        ("m-s2-88",   0x266940, 0x88, 0x89, "mutbase"),
        ("m-t3-cmp",  0x26697E, 0x09, 0x0A, "mutbase-tA"),
        ("m-t3-arg",  0x26698D, 0x14, 0x16, "mutbase"),
        ("m-t4-cmp",  0x2669CD, 0x01, 0x02, "mutbase-t2"),
        ("m-t4-arg",  0x2669DC, 0x04, 0x06, "mutbase"),
        ("m-cls-cmp", 0x266A01, 0x60, 0x40, "mutbase"),
        ("m-cc-bound",0x2668E3, 0x02, 0x03, "mutbase-t3"),
        ("m-or4",     0x266A3D, 0x04, 0x08, "mutbase"),
        ("m-link-js", 0x266777, 0x78, 0x79, "mutbase"),
        ("m-dc-bound",0x266A71, 0x0A, 0x0B, "mutbase-tB"),
        ("m-dc-arg",  0x266A7F, 0x16, 0x18, "mutbase"),
        ("m-or400",   0x266A8D, 0x04, 0x08, "mutbase"),
        ("m-deff",    0x2666F4, 0xFF, 0xFE, "mutbase-k7"),
        ("m-rmap",    0x266B0F, 0x20, 0x28, "mutbase"),
        ("m-kinit",   0x266BF9, 0x00, 0x01, "mutbase"),
        ("m-s88",     0x3DB597, 0x88, 0x89, "mutbase"),
        ("m-s8000",   0x3DB5BA, 0x80, 0x00, "mutbase"),
        ("m-sinit-n", 0x3DB5B2, 0x01, 0x02, "mutbase"),
        ("m-qwalk-c", 0x3DB6E9, 0x00, 0x01, "mutbase"),
        ("m-shr63",   0x3DB290, 0x63, 0x64, "mutbase"),
    ]
    OBS_KEYS = ("rec", "a0", "a8", "c0", "b8", "ktab", "cell", "trace")
    bases = {}
    for cn in list(cases):
        if cn.startswith("mutbase"):
            bc = mem_of(dict(cases[cn]), secs, raw)
            bases[cn] = (bc, World(bc, raw, secs).run().obs())
    killed = alive = badsite = 0
    for name, va, orig, pat, cn in MUTS:
        rva = va - IMG_LO
        img_byte = None
        for sva, vs, ra, rs in secs:
            if sva <= rva < sva + rs:
                img_byte = raw[ra + rva - sva]
        if img_byte != orig:
            badsite += 1
            print("   BADSITE %s site byte %02x != orig %02x" %
                  (name, img_byte if img_byte is not None else -1,
                   orig))
            continue
        bc, base = bases[cn]
        w = World(bc, raw, secs,
                  patch=[(va, bytes([pat]))]).run()
        obs = w.obs()
        if obs["faults"] or any(obs[k] != base[k] for k in OBS_KEYS):
            killed += 1
        else:
            alive += 1
            print("   ALIVE %s" % name)
    print("== mutants: %d killed, %d alive, %d badsite" %
          (killed, alive, badsite))
    json.dump({"cases": npass + nfail, "pass": npass,
               "mutants": {"killed": killed, "alive": alive,
                           "badsite": badsite}},
              open("result.json", "w"), indent=1)
    return 0 if (nfail == 0 and alive == 0 and badsite == 0) else 1


if __name__ == "__main__":
    sys.exit(main())
