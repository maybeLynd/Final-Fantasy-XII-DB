#!/usr/bin/env python
"""EXP-103 autostatus-notify-exec: execute 002FEF30 NOTIFY (the stat-event
constructor) from shipped bytes under Unicorn, plus its complete helper
closure.  Scripted boundaries (disclosed): RESET 003105D0 and APPLY
00307D10 are entry-stubbed with rcx captured.

Real bodies: subject 002FEF30 (2859 B), MM3 002F8E50, MM2 002F9180,
RESOLVE 0020E600, FIND 0031B860 (+COUNT 00236850, GET 00236820),
EQGATE 0031E9A0 (+EQCLASS 0031E9F0), VALID 00322C50 arm 6 path.

EXE: FFXII_TZA.exe sha256 73461d08..721f8, image base 0x120000.
"""
import ctypes, hashlib, json, struct, sys
from unicorn import Uc, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE, UC_HOOK_MEM_UNMAPPED, UC_PROT_ALL
from unicorn.x86_const import *

EXE = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe"
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
IMG_LO, IMG_HI = 0x120000, 0x2F800000
HEAP, STACK, RETQ, IMG32 = 0x40000000, 0x60000000, 0x62000000, 0x50000000
STRIDE, MATCH = 0xF50, 0x698

SUBJ    = 0x002FEF30
MM3     = 0x002F8E50          # ((r8+1)*ecx*edx)/100 signed
MM2     = 0x002F9180          # (ecx*edx)/100 signed
RESET   = 0x003105D0          # scripted boundary
APPLY   = 0x00307D10          # scripted boundary
RESOLVE = 0x0020E600
FIND    = 0x0031B860
EQGATE  = 0x0031E9A0
EQCLASS = 0x0031E9F0
VALID   = 0x00322C50
CLS     = 0x00309440
COUNT   = 0x00236850
GET     = 0x00236820

G_POOL  = 0x0208E688
G_COUNT = 0x0208E6A0
G_RESB  = 0x01F83530
G_DRESB = 0x01F83538
G_DT0   = 0x02EBF130          # kind==0 def row / VALID arm2
G_DT1   = 0x02EBF120          # kind!=0 rowA
G_DT2   = 0x02EBF148          # rowB
G_DT3   = 0x02EBF140          # rowC
G_DT4   = 0x02EBF150          # rowD
G_DTEQ  = 0x02EBF0F8          # equipment rows / VALID arm6
G_DTST  = 0x02EBF040          # status rows (bitmask walks)
G_DDT0  = 0x02EBF138          # decoy twins
G_DDT1  = 0x02EBF128
G_DDEQ  = 0x02EBF100
G_DDST  = 0x02EBF048
T1, T2, T3 = 0xD10290, 0xD102A0, 0xD102B0   # real .rdata bitmask tables

POOL   = HEAP + 0x000000      # unit pool element 0 (= the unit)
POOL1  = POOL + STRIDE        # element 1
REC    = HEAP + 0x400000      # record (rcx)
OUT    = HEAP + 0x600000      # explicit out struct (rdx cases)
EQLIST = HEAP + 0x700000      # explicit equip list (r8 cases)
TABS   = IMG32 + 0x000000     # def-table headers (one per 0x100)
ROWS   = IMG32 + 0x200000     # resolved row arena
RESB   = ROWS                 # [G_RESB] points here

HOOKS = {COUNT: "n", GET: "g", VALID: "V", RESOLVE: "R", FIND: "F",
         EQGATE: "E", EQCLASS: "e", CLS: "c", MM3: "m", MM2: "M",
         RESET: "X", APPLY: "A"}


def qw(v): return struct.pack("<Q", v & 0xFFFFFFFFFFFFFFFF)
def dw(v): return struct.pack("<I", v & 0xFFFFFFFF)
def hw(v): return struct.pack("<H", v & 0xFFFF)
def s32(v):
    v &= 0xFFFFFFFF
    return v - 0x100000000 if v & 0x80000000 else v
def s16(v):
    v &= 0xFFFF
    return v - 0x10000 if v & 0x8000 else v
def sdiv100(v):
    return v // 100 if v >= 0 else -((-v) // 100)


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
    """Apply {b:{},h:{},d:{},f:{},q:{}} field writes at base."""
    for off, v in spec.get("b", {}).items():  w(base + off, bytes([v & 0xFF]))
    for off, v in spec.get("h", {}).items():  w(base + off, hw(v))
    for off, v in spec.get("d", {}).items():  w(base + off, dw(v))
    for off, v in spec.get("f", {}).items():  w(base + off, struct.pack("<f", v))
    for off, v in spec.get("q", {}).items():  w(base + off, qw(v))


# every def-table global the subject or VALID arm 6 touches
DEFTABS = (G_DT0, G_DT1, G_DT2, G_DT3, G_DT4, G_DTEQ, G_DTST)


class World:
    def __init__(self, case, raw, secs):
        self.case = case
        self.planted = {}                     # fixture byte view (model input)
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

        # unit pool: up to two elements; matches[i] -> element i matches rec
        w(G_POOL, qw(POOL))
        matches = case.get("matches", [case.get("unit") is not None])
        cnt = case.get("count", len(matches))
        w(G_COUNT, dw(cnt))
        for i, m in enumerate(matches):
            if m:
                w(POOL + i * STRIDE + MATCH, qw(case.get("rcx", REC)))
        # unit fields land on the FIRST matching element
        first = next((i for i, m in enumerate(matches) if m), 0)
        self.uaddr = POOL + first * STRIDE
        if case.get("unit") is not None:
            fields(self.uaddr, case["unit"], w)

        # record + default equip list at rec+0x50
        if case.get("rec") is not None:
            fields(REC, case.get("rec") or {}, w)
        eq = case.get("equip", [])
        for i, v in enumerate(eq):
            w(REC + 0x50 + i * 2, hw(v))
            w(EQLIST + i * 2, hw(v))

        # def-table headers: {+4 cnt, +8 stride(word), +0xC rarg(dword)}
        # each table gets its own 0x40-byte slot (the g&0xFFF spacing
        # collides: G_DTEQ's +0xC lands on G_DDEQ's header)
        slot = {}
        for i, g in enumerate(list(DEFTABS) + [G_DDT0, G_DDT1, G_DDEQ, G_DDST]):
            slot[g] = TABS + i * 0x40
        for g in DEFTABS:
            spec = case.get("tabs", {}).get(g, {})
            ptr = spec.get("ptr", slot[g])
            w(g, qw(ptr))
            if ptr:
                w(ptr + 4, dw(spec.get("cnt", 8)))
                w(ptr + 8, hw(spec.get("stride", 0x30)))
                w(ptr + 0xC, dw(spec.get("rarg", 0)))
        # decoy twins (mutant targets)
        for g in (G_DDT0, G_DDT1, G_DDEQ, G_DDST):
            ptr = slot[g]
            w(g, qw(ptr))
            w(ptr + 4, dw(8))
            w(ptr + 8, hw(0x30))
            w(ptr + 0xC, dw(0))

        for addr, b in case.get("rows", {}).items():
            w(addr, bytes([b & 0xFF]))
        w(G_RESB, qw(case.get("resb", RESB)))
        w(G_DRESB, qw(case.get("dresb", RESB + 0x80000)))

        self.trace, self.faults, self.fired = [], [], set()
        for va, data in case.get("patch_bytes", []):
            gm.w(va, data)
        uc = self.uc
        uc.hook_add(UC_HOOK_MEM_UNMAPPED, self.on_bad)
        for va in HOOKS:
            uc.hook_add(UC_HOOK_CODE, self.on_call, begin=va, end=va)

    # -- hooks -------------------------------------------------------------
    def on_call(self, uc, addr, size, _):
        self.fired.add(addr)
        rcx = uc.reg_read(UC_X86_REG_RCX)
        rdx = uc.reg_read(UC_X86_REG_RDX)
        r8 = uc.reg_read(UC_X86_REG_R8)
        if addr == COUNT:
            self.trace.append("n")
        elif addr == GET:
            self.trace.append("g%d" % s32(rcx))
        elif addr == FIND:
            self.trace.append("F%x" % (rcx & 0xFFFFFFFFFFFFFFFF))
            self._watch_ret()
        elif addr == VALID:
            self.trace.append("V%d:%X" % (rcx & 0xFFFFFFFF, rdx & 0xFFFF))
            self._watch_ret()
        elif addr == RESOLVE:
            self.trace.append("R%x" % (rcx & 0xFFFFFFFF))
            self._watch_ret()
        elif addr == EQGATE:
            self.trace.append("E%x" % (rcx & 0xFFFFFFFFFFFFFFFF))
            self._watch_ret()
        elif addr == EQCLASS:
            self.trace.append("e%x" % (rcx & 0xFFFFFFFFFFFFFFFF))
            self._watch_ret()
        elif addr == CLS:
            self.trace.append("c%X" % (rcx & 0xFFFF))
            self._watch_ret()
        elif addr == MM3:
            self.trace.append("m%d,%d,%d" % (s32(rcx), s32(rdx), s32(r8)))
            self._watch_ret()
        elif addr == MM2:
            self.trace.append("M%d,%d" % (s32(rcx), s32(rdx)))
            self._watch_ret()
        elif addr == RESET:
            self.trace.append("X%x" % (rcx & 0xFFFFFFFFFFFFFFFF))
            self._stub(self.case.get("stub_reset", 0))
        elif addr == APPLY:
            self.trace.append("A%x" % (rcx & 0xFFFFFFFFFFFFFFFF))
            self._stub(self.case.get("stub_apply", 0))

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
        idx = len(self.trace) - 1
        holder = {"fired": False}

        def on_ret(uc_, a, s, _u):
            if holder["fired"]:
                return
            holder["fired"] = True
            self.trace[idx] += "=%d" % s32(uc_.reg_read(UC_X86_REG_RAX))

        uc.hook_add(UC_HOOK_CODE, on_ret, begin=back, end=back)

    def on_bad(self, uc, access, addr, size, value, _):
        self.faults.append(("MEM", hex(addr), "access=%d" % access,
                            "rip=%x" % uc.reg_read(UC_X86_REG_RIP)))
        return False


# ---- planted-byte model view ----------------------------------------------
class Fx:
    def __init__(self, planted):
        self.p = planted
    def b(self, a):   return self.p.get(a, 0)
    def h(self, a):   return self.b(a) | (self.b(a + 1) << 8)
    def d(self, a):   return self.h(a) | (self.h(a + 2) << 16)
    def q(self, a):   return self.d(a) | (self.d(a + 4) << 32)
    def f(self, a):   return struct.unpack("<f", dw(self.d(a)))[0]


def tab_spec(case, fx, g):
    """(ptr, cnt, stride, rarg) from the planted view."""
    ptr = fx.q(g)
    return ptr, fx.d(ptr + 4) if ptr else 0, \
        fx.h(ptr + 8) if ptr else 0, fx.d(ptr + 0xC) if ptr else 0


def eqclass(t9):
    """EQCLASS selector map, dumped from bytetab 0x31EA74 + jt 0x31EA50."""
    return {0: 1, 1: 2, 2: 3, 3: 3, 4: 3, 5: 3, 6: 3, 7: 4, 8: 4, 9: 4,
            0xA: 2, 0xB: 2, 0xC: 2, 0xD: 3, 0xE: 3, 0xF: 2, 0x10: 2,
            0x11: 4, 0x12: 6, 0x13: 7, 0x14: 8, 0x15: 9, 0x16: 9,
            0x17: 5, 0x18: 5, 0x19: 5, 0x1A: 5}.get(t9, 0)


def eqgate(cls):
    if cls <= 0:  return 0
    if cls <= 5:  return 1
    if cls == 6:  return 2
    if cls <= 9:  return 3
    return 0


def clamp_s(v, lo, hi):
    v = s32(v)
    return lo if v < lo else (hi if v > hi else v)


def run_case(case, raw, secs):
    w = World(case, raw, secs)
    uc = w.uc
    sp = STACK + 0x80000
    w.gm.w(sp, qw(RETQ))
    uc.reg_write(UC_X86_REG_RSP, sp)
    uc.reg_write(UC_X86_REG_RCX, case.get("rcx", REC))
    uc.reg_write(UC_X86_REG_RDX, case.get("rdx", 0))
    uc.reg_write(UC_X86_REG_R8, case.get("r8", 0))
    try:
        uc.emu_start(SUBJ, RETQ, count=4_000_000)
    except Exception as e:
        w.faults.append(("EMU", str(e),
                         "rip=%x" % uc.reg_read(UC_X86_REG_RIP)))
    rsi = case.get("rdx", 0) or (REC + 0x24)
    u = w.uaddr

    def rd(a, n):
        try:
            return w.gm.r(a, n)
        except KeyError:
            return b"\x00" * n
    obs = {"ret": uc.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFFFFFFFFFF,
           "out": rd(rsi, 0x24),
           "u_flags": rd(u, 8),
           "u_6b0": rd(u + 0x6B0, 8),
           "u_6f8": rd(u + 0x6F8, 8),
           "u_714": rd(u + 0x714, 4),
           "u_748": rd(u + 0x748, 0x10),
           "u_770": rd(u + 0x770, 8),
           "u_788": rd(u + 0x788, 8),
           "u_ba0": rd(u + 0xBA0, 4)}
    return " ".join(w.trace) or "-", w.faults, w, obs


# ---- model -----------------------------------------------------------------
def model(case, w, raw, secs):
    fx = Fx(w.planted)
    tr = []
    out = bytearray(0x24)
    rcx = case.get("rcx", REC)
    rdx = case.get("rdx", 0)
    r8 = case.get("r8", 0)
    resb = fx.q(G_RESB)

    def R(arg):
        tr.append("R%x=%d" % (arg & 0xFFFFFFFF, s32(resb + arg)))
        return resb + arg

    def defrow(g, idx):
        """double-RESOLVE + stride*idx; returns row addr or 0."""
        ptr, cnt, stride, rarg = tab_spec(case, fx, g)
        if not ptr:
            return 0
        if not R(rarg):
            return 0
        return R(rarg) + stride * (idx & 0xFFFF)

    # -- FIND / out-struct base --
    unit = 0
    prior3c = 0
    if not rdx:
        tr.append("F%x" % (rcx & 0xFFFFFFFFFFFFFFFF))
        f_idx = len(tr) - 1
        matches = case.get("matches", [case.get("unit") is not None])
        found = 0
        if rcx:
            # FIND: initial COUNT, then per-iteration GET + COUNT recheck
            # (the recheck fires after every miss; a hit returns before it)
            tr.append("n")
            cnt = case.get("count", len(matches))
            if cnt > 0:
                i = 0
                while True:
                    tr.append("g%d" % i)
                    el = fx.q(POOL + i * STRIDE + MATCH)
                    hit = matches[i] if i < len(matches) else False
                    if hit and el == (rcx & 0xFFFFFFFFFFFFFFFF):
                        found = POOL + i * STRIDE
                        break
                    i += 1
                    tr.append("n")
                    if i >= cnt:
                        break
        unit = found
        tr[f_idx] += "=%d" % s32(unit)
        if unit:
            prior3c = fx.d(REC + 0x3C)
    # flag64 = 1 only on the FIND-hit path (0x2FEF89); FIND-miss or an
    # explicit rdx leaves it 0 -> the tail exits at `cmp [rsp+0x64],ebp`.
    flag64 = 1 if (not rdx and unit) else 0
    if not rcx:
        # rsi = rdi+0x24 = 0x24 -> memset qword faults on write (rdx==0);
        # with rdx!=0 the kind!=0 arm's byte[rdi+4] read faults at 4.
        if not rdx:
            return " ".join(tr), bytes(out), None, 0x24
    rsi = rdx or (REC + 0x24)
    eq_list = r8 or (REC + 0x50)

    kindb = 0xFF if not rcx else fx.b(REC + 5)
    # flag5c = kind0 && (byte[rdi+4]-0x1B)u8 <= 0xC; gates the 0x7fff
    # out[0] rewrite (cmp vs ebp==0).
    flag5c = 1 if (rcx and kindb == 0
                   and (fx.b(REC + 4) - 0x1B) & 0xFF <= 0xC) else 0

    acc40 = a28 = a2c = a30 = a34 = a38 = a48 = a50 = a54 = a58 = 0
    a20 = a24 = ad8 = ae8 = a60 = 0
    r12 = r13 = 0
    flag70 = 0            # written per-arm; [rsp+0x70] never touched in prologue
    flag4c = 1            # prologue inits [rsp+0x4c] = r15d = 1
    fault = None

    if kindb == 0:
        row = defrow(G_DT0, fx.b(REC + 4))
        if row == 0:
            # native proceeds to byte[row+0x18] -> fault
            return " ".join(tr) or "-", bytes(out), None, 0x18
        b18, b19 = fx.b(row + 0x18), fx.b(row + 0x19)
        ecx = s32(fx.d(REC + 8))
        p = s32(s32((b18 + 1) * ecx) * b19)
        a1 = sdiv100(p)
        tr.append("m%d,%d,%d=%d" % (ecx, b19, b18, a1))
        acc40 = a1
        cw = s16(fx.h(REC + 0xC))
        b1d = fx.b(row + 0x1D)
        a2 = sdiv100(s32(cw * b1d))
        tr.append("M%d,%d=%d" % (cw, b1d, a2))
        a28 = a2
        a50 = fx.b(row + 0x2A)
        a60 = fx.b(REC + 0x20)
        flag70 = 1
        a2c = int(fx.f(REC + 0x18))
        a30 = int(fx.f(REC + 0x1C))
        r12 = int(fx.f(REC + 0x10))
        r13 = int(fx.f(REC + 0x14))
        struct.pack_into("<I", out, 0x14, fx.d(row + 0x4C))
        struct.pack_into("<I", out, 0x18, fx.d(row + 0x48))
        flag4c = 1
    else:
        if not rcx:
            # rdi==0: byte[rdi+4] idx read faults at 4, but only after the
            # defrow's two resolves; a failed defrow makes rowA=0 and the
            # word[rowA+0x22] read faults at 0x22 instead.
            ptr, _, _, rarg = tab_spec(case, fx, G_DT1)
            if ptr and R(rarg) and R(rarg):
                return " ".join(tr), bytes(out), None, 4
            return " ".join(tr), bytes(out), None, 0x22
        rowA = defrow(G_DT1, fx.b(REC + 4))
        if rowA == 0:
            return " ".join(tr) or "-", bytes(out), None, 0x22
        rowB = defrow(G_DT2, fx.h(rowA + 0x22))
        rowC = defrow(G_DT3, fx.h(rowA + 0x24))
        rowD = defrow(G_DT4, fx.h(rowA))
        # accumulator reads fault on missing rows in this order:
        # rowC+0x24 word (0x2FF1FC) -> rowC+0x20 -> rowC+0x26 -> rowB+0x20..
        if rowC == 0:
            return " ".join(tr) or "-", bytes(out), None, 0x24
        if rowB == 0:
            return " ".join(tr) or "-", bytes(out), None, 0x20
        L = s32(fx.b(REC + 0x1C2) - fx.b(REC + 0x88))
        acc40 = s32(fx.d(rowC + 0x20) * L) + s32(fx.d(rowB + 0x20))
        a28 = s32(s16(fx.h(rowC + 0x24)) * L) + s16(fx.h(rowB + 0x24))
        r12 = s32(fx.b(rowC + 0x26) * L) + fx.b(rowB + 0x26) \
            + s16(fx.h(REC + 8))
        ad8 = s16(fx.h(REC + 0x1C))
        a48 = s32(fx.b(rowC + 0x27) * L) + fx.b(rowB + 0x27) \
            + s16(fx.h(REC + 0xA))
        a2c = s32(fx.b(rowC + 0x28) * L) + fx.b(rowB + 0x28) \
            + s16(fx.h(REC + 0xC))
        a30 = s32(fx.b(rowC + 0x29) * L) + fx.b(rowB + 0x29) \
            + s16(fx.h(REC + 0xE))
        a50 = s32(fx.b(rowC + 0x2A) * L) + fx.b(rowB + 0x2A) \
            + s16(fx.h(REC + 0x16))
        a34 = s32(fx.b(rowC + 0x2B) * L) + fx.b(rowB + 0x2B) \
            + s16(fx.h(REC + 0x12))
        a38 = s32(fx.b(rowC + 0x2C) * L) + fx.b(rowB + 0x2C) \
            + s16(fx.h(REC + 0x14))
        a54 = s16(fx.h(REC + 0x1E))
        ae8 = s16(fx.h(REC + 0x10))
        a58 = s16(fx.h(REC + 0x20))
        if rowD == 0:
            return " ".join(tr) or "-", bytes(out), None, 0x2C
        out[0x1C] = fx.b(rowD + 0x2C)
        out[0x1D] = fx.b(rowD + 0x29)
        out[0x1E] = fx.b(rowD + 0x2A)
        out[0x1F] = fx.b(rowD + 0x2B)
        out[0x20] = fx.b(rowD + 0x2D)
        a24 = s16(fx.h(REC + 0x18))
        a20 = s16(fx.h(REC + 0x1A))
        r13b = fx.b(rowA + 0x15)
        flag4c = 1
        if r13b & 1:
            L2 = s32(fx.b(REC + 0x1C2) - fx.b(REC + 0x88))
            ae8 = s32(ae8 + fx.b(rowB + 0x2D) + fx.b(rowC + 0x2D) * L2)
            flag4c = 0
            a24 = s32(a24 + fx.b(rowB + 0x2E) + fx.b(rowC + 0x2E) * L2)
        flag70 = 1
        if r13b & 2:
            L2 = s32(fx.b(REC + 0x1C2) - fx.b(REC + 0x88))
            a20 = s32(a20 + fx.b(rowB + 2) + fx.b(rowC + 2) * L2)
            ad8 = s32(ad8 + fx.b(rowB + 3) + fx.b(rowC + 3) * L2)
            flag70 = 0
        r13 = a48

    # -- shared tail: 5-slot equipment loop --
    edi = ad8
    r15 = a20
    r14 = a24
    eqtab_ptr, eqcnt, eqstride, eqrarg = tab_spec(case, fx, G_DTEQ)
    for i in range(5):
        eid = fx.h(eq_list + i * 2)
        tr.append("V6:%X" % (eid & 0xFFFF))
        ok = 1 if (0x1000 <= eid < 0x1000 + eqcnt) else 0
        tr[-1] += "=%d" % ok
        if not ok:
            continue
        eqrow = 0
        if eqtab_ptr:
            if not R(eqrarg):
                eqrow = 0
            else:
                eqrow = R(eqrarg) + eqstride * ((eid - 0x1000) & 0xFFFF)
        # EQGATE(eqrow) - eqrow==0 -> EQCLASS reads byte[9] -> fault
        tr.append("E%x" % (eqrow & 0xFFFFFFFFFFFFFFFF))
        if eqrow == 0:
            tr.append("e0")
            return " ".join(tr), bytes(out), None, 9
        t9 = fx.b(eqrow + 9)
        cls = eqclass(t9)
        gate = eqgate(cls)
        tr.append("e%x=%d" % (eqrow, cls))
        tr[-2] += "=%d" % gate
        if gate == 1:
            if flag4c:
                ae8 = s32(ae8 + fx.b(eqrow + 0x1A))
                r14 = s32(r14 + fx.b(eqrow + 0x1D))
        elif gate == 2:
            if flag70:
                r15 = s32(r15 + fx.b(eqrow + 0x18))
                edi = s32(edi + fx.b(eqrow + 0x19))
        elif gate == 3:
            a34 = s32(a34 + fx.b(eqrow + 0x18))
            a38 = s32(a38 + fx.b(eqrow + 0x19))
        rarg = fx.d(eqrow + 0x28)
        ra = R(rarg); acc40 += fx.h(ra)
        ra = R(rarg); a28 = s32(a28 + fx.h(ra + 2))
        ra = R(rarg); r12 = s32(r12 + fx.b(ra + 4))
        ra = R(rarg); r13 = s32(r13 + fx.b(ra + 5))
        ra = R(rarg); a2c = s32(a2c + fx.b(ra + 6))
        ra = R(rarg); a30 = s32(a30 + fx.b(ra + 7))
        ra = R(rarg)
        struct.pack_into("<I", out, 0x14,
                         struct.unpack("<I", out[0x14:0x18])[0] | fx.d(ra + 0xC))
        ra = R(rarg)
        struct.pack_into("<I", out, 0x18,
                         struct.unpack("<I", out[0x18:0x1C])[0] | fx.d(ra + 8))
        ra = R(rarg); out[0x1C] |= fx.b(ra + 0x13)
        ra = R(rarg); out[0x1D] |= fx.b(ra + 0x10)
        ra = R(rarg); out[0x1E] |= fx.b(ra + 0x12)
        ra = R(rarg); out[0x1F] |= fx.b(ra + 0x11)
        ra = R(rarg); out[0x20] |= fx.b(ra + 0x14)
    # -- writebacks (0x2FF591/596/5AD): a20=r15, ad8=edi, a24=r14 --
    a20, a24, ad8 = r15, r14, edi

    # -- three bitmask walks, i = ebp(=0) .. bound --
    # mask = r15d(=1 reloaded) << (sid&7); byte tests at rec+0x68 / +0x78.
    # status-tab null or resolve==0 -> rcx=rbp=0 -> word[4] fault.
    rdi_rec = rcx
    st_ptr, stcnt, ststride, strarg = tab_spec(case, fx, G_DTST)

    def bitwalk(tabva, bound):
        acc = 0
        for i in range(0, bound):
            sid = img(raw, secs, tabva + i, 1)[0]
            byte_i, bit_i = sid >> 3, sid & 7
            m = fx.b(rdi_rec + 0x68 + byte_i) | fx.b(rdi_rec + 0x78 + byte_i)
            if not (m & (1 << bit_i)):
                continue
            if not st_ptr or not R(strarg):
                return None           # rcx=rbp=0 -> word[4] fault
            row = R(strarg) + ststride * sid
            acc += fx.h(row + 4)
        return acc

    v = bitwalk(T1, 0x10)
    if v is None:
        return " ".join(tr), bytes(out), None, 4
    r12 = s32(r12 + v)
    v = bitwalk(T2, 0x10)
    if v is None:
        return " ".join(tr), bytes(out), None, 4
    r13 = s32(r13 + v)
    r14q = acc40
    v = bitwalk(T3, 0x0C)
    if v is None:
        return " ".join(tr), bytes(out), None, 4
    r14q += v

    # -- clamps + out writes --
    # out[0]: signed lo = r15 which is RELOADED to 1 at 0x2FF5A7 (the
    # bitmask mask base) -- not the gate2 accumulator; the gate2 sum is
    # already written back to the a20 slot.  hi = 9999 when kindb==0 else
    # 1e9; when flag5c (kind0&&band) a second write recaps at 0x7fff.
    def locl(v, lo, hi):
        return lo if v < lo else min(v, hi)
    out0 = locl(r14q, 1, 0x270F if kindb == 0 else 0x3B9ACA00)
    if flag5c:
        out0 = locl(r14q, 1, 0x7FFF)
    out[0:4] = dw(out0 & 0xFFFFFFFF)
    a54c = s32(a54 + a20 + a24 + a50)     # ebx = a54 + (a20+a24+a50)
    out[4:6] = hw(clamp_s(a28, 0, 0x3E7))
    out[6] = clamp_s(r12, 0, 0x63)
    out[7] = clamp_s(r13, 0, 0x63)
    out[8] = clamp_s(a2c, 0, 0x63)
    out[9] = clamp_s(a30, 0, 0x63)
    out[0x13] = min(a60 & 0xFFFFFFFF, 3)  # cmova: unsigned min vs 3
    out[0x11] = clamp_s(a54c, 0, 0x64)
    out[0x12] = clamp_s(s32(a58 + ad8), 0, 0x64)  # r11d = a58 + ad8
    out[0x0A] = clamp_s(ae8, 0, 0xFF)
    out[0x0B] = clamp_s(a34, 0, 0xFF)
    out[0x0C] = clamp_s(a38, 0, 0xFF)
    out[0x0D] = clamp_s(a50, 0, 0x64)
    out[0x0E] = clamp_s(a24, 0, 0x64)
    out[0x0F] = clamp_s(a20, 0, 0x64)
    # out[0x10]: eax = ad8 unconditionally -- loaded at 0x2ff7a7 for the
    # r11d add, reloaded at 0x2ff7d6 on the jge path; same value either way.
    out[0x10] = clamp_s(ad8, 0, 0x64)

    # -- reset/apply tail --
    # kind!=0 exits at `test edi,edi` (edi=kindb).  flag64==0 (FIND-miss
    # or explicit rdx) exits too.  Unit writes are ebp/rbp = 0.
    exp_u = {}          # expected unit writes {off: bytes}
    if kindb == 0 and flag64:
        diff = struct.unpack("<I", out[0x18:0x1C])[0] ^ prior3c
        if diff & 0x8000020:
            uf = fx.q(unit)
            ax = fx.h(unit + 0x714)
            b6b4 = fx.b(unit + 0x6B4)
            skip_reset = bool(uf & (1 << 0x18))
            if not skip_reset:
                if ax > 0x21E:
                    skip_reset = (ax == 0x113)
                else:
                    skip_reset = (b6b4 >= 9) or (ax == 0x113)
            if not skip_reset:
                tr.append("X%x" % (unit & 0xFFFFFFFFFFFFFFFF))
            exp_u[0x6F8] = qw(0)
            exp_u[0x748] = dw(0)
            exp_u[0x770] = dw(0)
            newf = uf
            if (uf & 0x4000) and fx.h(unit + 0xBA0) not in (0x113, 0x95):
                newf = uf & ~0x4000
            exp_u[0] = qw(newf)
            exp_u[0x788] = dw(fx.d(unit + 0x788) & 0xFFFFFBFF)
            exp_u[0x6B0] = dw(fx.d(unit + 0x6B0) & 0xFFFFFFFD)
            exp_u[0x750] = qw(0)
            exp_u[0x74C] = dw(0)
            exp_u[4] = dw(fx.d(unit + 4) | 0x200000)
            tr.append("A%x" % (unit & 0xFFFFFFFFFFFFFFFF))

    return " ".join(tr) or "-", bytes(out), exp_u, fault


def exp_obs(case, w, raw, secs):
    """Compute expected observables dict matching run_case's obs."""
    exp_tr, exp_out, exp_u, fault = model(case, w, raw, secs)
    fx = Fx(w.planted)
    obs = {"out": exp_out, "fault": fault}
    u = w.uaddr

    def span(off, n):
        b = bytearray()
        for i in range(n):
            b.append(fx.b(u + off + i))
        if exp_u:
            for wo, data in exp_u.items():
                for i, v in enumerate(data):
                    if off <= wo + i < off + n:
                        b[wo + i - off] = v
        return bytes(b)
    obs["u_flags"] = span(0, 8)
    obs["u_6b0"] = span(0x6B0, 8)
    obs["u_6f8"] = span(0x6F8, 8)
    obs["u_714"] = span(0x714, 4)
    obs["u_748"] = span(0x748, 0x10)
    obs["u_770"] = span(0x770, 8)
    obs["u_788"] = span(0x788, 8)
    obs["u_ba0"] = span(0xBA0, 4)
    return exp_tr, obs


# ---- cases ------------------------------------------------------------------
def base_rec(kind=0, b4=0x1B):
    return {"b": {4: b4, 5: kind, 0x20: 2, 0x88: 1, 0x1C2: 5,
                  0x68: 0, 0x78: 0},
            "d": {8: 50, 0x3C: 0},
            "h": {0x0C: 10},
            "f": {0x10: 0.0, 0x14: 0.0, 0x18: 0.0, 0x1C: 0.0}}


def rowbytes(g, idx, fields_, stride=0x30, off=0):
    """Produce {addr: byte} entries for a def-row field dict at
    RESB + idx*stride + off.  values may be int or byte-list."""
    base = RESB + idx * stride + off
    d = {}
    for o, v in fields_.items():
        if isinstance(v, (list, bytes, tuple)):
            for i, b in enumerate(v):
                d[base + o + i] = b
        else:
            d[base + o] = v
    return d


def merge(*dicts):
    out = {}
    for d in dicts:
        for k, v in d.items():
            out[k] = v
    return out


CASES = []
def case(name, **kw):
    kw["name"] = name
    kw.setdefault("rec", base_rec())
    kw.setdefault("unit", {"d": {}, "h": {}})
    CASES.append(kw)


def build_cases():
    R = RESB
    cases = []

    def k0_row(f):
        return rowbytes(G_DT0, 0x1B, f)

    # 1: kind==0 happy path, one valid gate-3 equip slot, tail runs
    rows = k0_row({0x18: 3, 0x19: 40, 0x1D: 20, 0x2A: 7, 0x48: dw(0x20),
                     0x4C: dw(0x8000000)})
    # eq slot0: id 0x1000, gate3 (t9=0x13) -> a34/a38 + RESOLVE block
    eqbase = RESB + 0 * 0x30
    rows[eqbase + 9] = 0x13
    rows[eqbase + 0x18] = 11; rows[eqbase + 0x19] = 13
    for i, b in enumerate(dw(0x900)): rows[eqbase + 0x28 + i] = b
    rres = RESB + 0x900
    for o, v in {0: [3, 0], 2: [5, 0], 4: 6, 5: 7, 6: 8, 7: 9,
                 8: list(dw(0x100)), 0xC: list(dw(0x200)),
                 0x10: 1, 0x11: 2, 0x12: 4, 0x13: 8, 0x14: 0x10}.items():
        if isinstance(v, list):
            for i, b in enumerate(v): rows[rres + o + i] = b
        else:
            rows[rres + o] = v
    cases.append({"name": "kind0-basic-gate3", "equip": [0x1000, 0, 0, 0, 0],
                  "rows": rows,
                  "rec": {"b": {4: 0x1B, 5: 0, 0x20: 2, 0x88: 1, 0x1C2: 5},
                          "d": {8: 50, 0x3C: 0},
                          "h": {0x0C: 10},
                          "f": {0x10: 0.0, 0x14: 0.0, 0x18: 0.0, 0x1C: 0.0}},
                  "unit": {"d": {0: 0}, "h": {0x714: 0x100},
                           "b": {0x6B4: 1}}})

    # 2: all slots invalid -> V6=0 x5, no eq tokens
    cases.append({"name": "kind0-empty-slots", "equip": [0, 0, 0, 0, 0],
                  "rows": k0_row({0x18: 1, 0x19: 10, 0x1D: 5, 0x2A: 0,
                                    0x48: dw(0), 0x4C: dw(0)})})

    # 3: all five slots valid, mixed gates
    rows = k0_row({0x18: 0, 0x19: 0, 0x1D: 0, 0x2A: 0, 0x48: dw(0),
                     0x4C: dw(0)})
    t9s = [0x13, 0x12, 0x05, 0x30, 0x15]   # g3, g2, g1, g0(t9>0x1a), g3
    for i, t9 in enumerate(t9s):
        eb = RESB + i * 0x30
        rows[eb + 9] = t9
        rows[eb + 0x18] = 10 + i; rows[eb + 0x19] = 20 + i
        rows[eb + 0x1A] = 30 + i; rows[eb + 0x1D] = 40 + i
        for j, b in enumerate(dw(0xA00 + i * 0x20)):
            rows[eb + 0x28 + j] = b
    cases.append({"name": "kind0-all-gates",
                  "equip": [0x1000, 0x1001, 0x1002, 0x1003, 0x1004],
                  "rows": rows})

    # kind!=0 fixture: rowA at idx 0x1B (byte[rec+4]=0x1B), rowB/rowC/rowD
    # at separated rarg arenas; eqspec = [(t9, r28), ...] per valid slot
    def k1_fixture(rowa15=3, eqspec=None):
        rows = dict(rowbytes(G_DT1, 0x1B,
                             {0x15: rowa15, 0x22: [0, 0],
                              0x24: [1, 0], 0x00: [2, 0]}))
        tabs = {G_DT2: {"rarg": 0x1000}, G_DT3: {"rarg": 0x2000},
                G_DT4: {"rarg": 0x3000}}
        rb_, rc_, rd_ = RESB + 0x1000, RESB + 0x2000 + 0x30, \
            RESB + 0x3000 + 0x60
        for o in range(0x20, 0x2F):
            rows[rb_ + o] = (o * 3) & 0xFF
            rows[rc_ + o] = (o * 5) & 0xFF
        for o in (0x29, 0x2A, 0x2B, 0x2C, 0x2D):
            rows[rd_ + o] = 0x40 + o
        for o in (2, 3):
            rows[rb_ + o] = 1
            rows[rc_ + o] = 2
        if eqspec:
            for i, (t9, r28) in enumerate(eqspec):
                eb = RESB + i * 0x30
                rows[eb + 9] = t9
                rows[eb + 0x18] = 10 + i
                rows[eb + 0x19] = 20 + i
                rows[eb + 0x1A] = 30 + i
                rows[eb + 0x1D] = 40 + i
                for j, b in enumerate(dw(r28)):
                    rows[eb + 0x28 + j] = b
        return tabs, rows

    # 4: kind!=0 arm - four defrows, L=4, rowA+0x15 bit0+bit1
    tabs, rows = k1_fixture()
    cases.append({"name": "kind1-four-rows", "equip": [0] * 5,
                  "tabs": tabs, "rows": rows,
                  "rec": {"b": {4: 0x1B, 5: 1, 0x20: 0, 0x88: 1, 0x1C2: 5},
                          "d": {8: 0, 0x3C: 0}, "h": {0x0C: 0},
                          "f": {0x10: 0.0, 0x14: 0.0, 0x18: 0.0, 0x1C: 0.0}}})

    # 5: FIND-miss + out[0x18] bits unset -> clean early exit
    cases.append({"name": "kind0-find-miss-clean",
                  "unit": None, "matches": [],
                  "equip": [0] * 5,
                  "rows": k0_row({0x18: 0, 0x19: 0, 0x1D: 0, 0x2A: 0,
                                    0x48: dw(0), 0x4C: dw(0)})})

    # 6: FIND-miss + out[0x18] bit31 set -> diff bits fire BUT flag64==0
    # -> tail exits cleanly (flag64 gates the whole reset/apply block)
    cases.append({"name": "kind0-find-miss-tailskip",
                  "unit": None, "matches": [],
                  "equip": [0] * 5,
                  "rows": k0_row({0x18: 0, 0x19: 0, 0x1D: 0, 0x2A: 0,
                                    0x48: dw(0x80000000), 0x4C: dw(0)})})

    # 7: rdx-supplied out struct -> no FIND; out[0x18] unset -> exit clean
    cases.append({"name": "kind0-rdx-out-clean", "rdx": OUT,
                  "equip": [0] * 5,
                  "rows": k0_row({0x18: 0, 0x19: 0, 0x1D: 0, 0x2A: 0,
                                    0x48: dw(0), 0x4C: dw(0)})})

    # 8: rdx-supplied + bit5 -> diff bits fire BUT flag64==0 -> tail-skip
    cases.append({"name": "kind0-rdx-tailskip", "rdx": OUT,
                  "equip": [0] * 5,
                  "rows": k0_row({0x18: 0, 0x19: 0, 0x1D: 0, 0x2A: 0,
                                    0x48: dw(0x20), 0x4C: dw(0)})})

    # 9: null def table -> no R tokens, fault at byte[0x18]
    cases.append({"name": "kind0-tab-null",
                  "tabs": {G_DT0: {"ptr": 0}},
                  "equip": [0] * 5, "exp_fault": True})

    # 10: resolve returns 0 -> R=0 -> fault at byte[0x18]
    cases.append({"name": "kind0-resb-null", "resb": 0,
                  "equip": [0] * 5, "exp_fault": True})

    # 11: eq table null -> VALID arm6 returns 0 for every slot, no fault
    cases.append({"name": "kind0-eqtab-null",
                  "tabs": {G_DTEQ: {"ptr": 0}},
                  "equip": [0x1000] * 5,
                  "rows": k0_row({0x18: 0, 0x19: 0, 0x1D: 0, 0x2A: 0,
                                    0x48: dw(0), 0x4C: dw(0)})})

    # 12: (eqrow==0 is unreachable: resb+rarg cannot be 0 and a null eq
    # table makes VALID return 0, so EQGATE(0) never fires -- finding)

    # 13: clamps - huge acc40 (>0x7fff) -> out[0]=0x7fff; stats over caps
    rows = k0_row({0x18: 0xFF, 0x19: 0xFF, 0x1D: 0xFF, 0x2A: 0xFF,
                     0x48: dw(0), 0x4C: dw(0)})
    cases.append({"name": "kind0-clamps", "equip": [0] * 5, "rows": rows,
                  "rec": {"b": {4: 0x1B, 5: 0, 0x20: 9, 0x88: 0, 0x1C2: 0},
                          "d": {8: 0x7FFFFFFF, 0x3C: 0},
                          "h": {0x0C: 0x7FFF},
                          "f": {0x10: 500.0, 0x14: 600.0,
                                0x18: 700.0, 0x1C: 800.0}}})

    # 14: negative MM2 -> a28<0 -> clamps to 0
    cases.append({"name": "kind0-neg-mm2", "equip": [0] * 5,
                  "rows": k0_row({0x18: 1, 0x19: 10, 0x1D: 50, 0x2A: 0,
                                    0x48: dw(0), 0x4C: dw(0)}),
                  "rec": {"b": {4: 0x1B, 5: 0, 0x20: 0, 0x88: 0, 0x1C2: 0},
                          "d": {8: 10, 0x3C: 0},
                          "h": {0x0C: 0xFF38},          # -200
                          "f": {0x10: 0.0, 0x14: 0.0, 0x18: 0.0, 0x1C: 0.0}}})

    # 15: bitmask walk - set bits matching T1/T2/T3 entries at i>=5
    cases.append({"name": "kind0-bitmask",
                  "equip": [0] * 5, "rows": k0_row({0x18: 0, 0x19: 0,
                      0x1D: 0, 0x2A: 0, 0x48: dw(0), 0x4C: dw(0)}),
                  "unit": {"d": {0: 0}, "h": {0x714: 0x100},
                           "b": {0x6B4: 1}},
                  "mask_bits": True})

    # 16: bitmask bit set + status tab null -> fault at word[9]
    cases.append({"name": "kind0-bitmask-tabnull",
                  "tabs": {G_DTST: {"ptr": 0}},
                  "equip": [0] * 5, "mask_bits": True,
                  "rows": k0_row({0x18: 0, 0x19: 0, 0x1D: 0, 0x2A: 0,
                                    0x48: dw(0), 0x4C: dw(0)}),
                  "exp_fault": True})

    # 17: r8-supplied equip list (same ids) -> identical path
    cases.append({"name": "kind0-r8-list", "r8": EQLIST,
                  "equip": [0x1000, 0, 0, 0, 0],
                  "rows": merge(k0_row({0x18: 0, 0x19: 0, 0x1D: 0, 0x2A: 0,
                                          0x48: dw(0), 0x4C: dw(0)}),
                                {RESB + 9: 0x13,
                                 RESB + 0x18: 1, RESB + 0x19: 2,
                                 RESB + 0x28: 0, RESB + 0x29: 0,
                                 RESB + 0x2A: 0, RESB + 0x2B: 0})})

    # 18: reset-skip via bit24 set -> no X, still clears + A
    cases.append({"name": "kind0-skipreset-bit24",
                  "equip": [0] * 5,
                  "rows": k0_row({0x18: 0, 0x19: 0, 0x1D: 0, 0x2A: 0,
                                    0x48: dw(0x20), 0x4C: dw(0x20)}),
                  "rec": base_rec(), "unit": {"d": {0: 0x1000000}, "h": {0x714: 0x100},
                           "b": {0x6B4: 1}}})

    # 19: reset-skip via ax>0x21e && ax==0x113
    cases.append({"name": "kind0-skipreset-ax113",
                  "equip": [0] * 5,
                  "rows": k0_row({0x18: 0, 0x19: 0, 0x1D: 0, 0x2A: 0,
                                    0x48: dw(0x20), 0x4C: dw(0x20)}),
                  "rec": base_rec(), "unit": {"d": {0: 0}, "h": {0x714: 0x113},
                           "b": {0x6B4: 1}}})

    # 20: reset runs: bit24 clear, ax<=0x21e, b6b4<9, ax!=0x113;
    # +0x788/+0x6B0 bits set so the tail's AND masks are observable, and
    # +0x6F8/0x748/0x770/0x750/0x74C nonzero so the ebp/rbp=0 writes clear
    cases.append({"name": "kind0-reset-runs",
                  "equip": [0] * 5,
                  "rows": k0_row({0x18: 0, 0x19: 0, 0x1D: 0, 0x2A: 0,
                                    0x48: dw(0x20), 0x4C: dw(0x20)}),
                  "rec": base_rec(), "unit": {"d": {0: 0xC000, 0x788: 0xFFFFF,
                                 0x6B0: 0xFFFFF, 4: 0,
                                 0x748: 0xDEAD, 0x770: 0xBEEF,
                                 0x74C: 0xF00D},
                           "q": {0x6F8: 0x1122334455, 0x750: 0x667788},
                           "h": {0x714: 0x100, 0xBA0: 0x42},
                           "b": {0x6B4: 1}}})

    # 21: bit14 set + ba0==0x113 -> skip bit14 clear
    cases.append({"name": "kind0-ba0-113",
                  "equip": [0] * 5,
                  "rows": k0_row({0x18: 0, 0x19: 0, 0x1D: 0, 0x2A: 0,
                                    0x48: dw(0x20), 0x4C: dw(0x20)}),
                  "rec": base_rec(), "unit": {"d": {0: 0x4000}, "h": {0x714: 0x113, 0xBA0: 0x113},
                           "b": {0x6B4: 1}}})

    # 22: bit14 set + ba0==0x95 -> skip bit14 clear
    cases.append({"name": "kind0-ba0-95",
                  "equip": [0] * 5,
                  "rows": k0_row({0x18: 0, 0x19: 0, 0x1D: 0, 0x2A: 0,
                                    0x48: dw(0x20), 0x4C: dw(0x20)}),
                  "rec": base_rec(), "unit": {"d": {0: 0x4000}, "h": {0x714: 0x113, 0xBA0: 0x95},
                           "b": {0x6B4: 1}}})

    # 23: bit14 set + ba0 other -> clear bit14
    cases.append({"name": "kind0-ba0-clear",
                  "equip": [0] * 5,
                  "rows": k0_row({0x18: 0, 0x19: 0, 0x1D: 0, 0x2A: 0,
                                    0x48: dw(0x20), 0x4C: dw(0x20)}),
                  "rec": base_rec(), "unit": {"d": {0: 0x4000}, "h": {0x714: 0x113, 0xBA0: 0x42},
                           "b": {0x6B4: 1}}})

    # 24: no diff bits -> tail exits before unit touch (unit still present)
    cases.append({"name": "kind0-nodiff",
                  "equip": [0] * 5,
                  "rows": k0_row({0x18: 0, 0x19: 0, 0x1D: 0, 0x2A: 0,
                                    0x48: dw(0x40), 0x4C: dw(0)}),
                  "unit": {"d": {0: 0}, "h": {0x714: 0x100},
                           "b": {0x6B4: 1}}})

    # 25: rcx=0 -> memset writes [0x24] -> fault
    cases.append({"name": "null-record", "rcx": 0, "rec": None,
                  "equip": [0] * 5, "exp_fault": True})

    # 26: FIND with two-pool-element scan (element1 match)
    cases.append({"name": "kind0-find-second",
                  "matches": [False, True], "count": 2,
                  "equip": [0] * 5,
                  "rows": k0_row({0x18: 0, 0x19: 0, 0x1D: 0, 0x2A: 0,
                                    0x48: dw(0), 0x4C: dw(0)}),
                  "unit": {"d": {0: 0}, "h": {0x714: 0x100},
                           "b": {0x6B4: 1}}})

    # 27: flag5c==0 (byte[4] outside 0x1B..0x27 band) -> out[0] keeps the
    # first write's 9999 cap instead of the 0x7fff rewrite
    cases.append({"name": "kind0-noband-cap",
                  "equip": [0] * 5,
                  "rows": rowbytes(G_DT0, 0,
                                   {0x18: 0xFF, 0x19: 0xFF, 0x1D: 0xFF,
                                    0x2A: 0, 0x48: dw(0), 0x4C: dw(0)}),
                  "rec": {"b": {4: 0x00, 5: 0, 0x20: 0, 0x88: 0, 0x1C2: 0},
                          "d": {8: 0x7FFFFFFF, 0x3C: 0},
                          "h": {0x0C: 0},
                          "f": {0x10: 0.0, 0x14: 0.0, 0x18: 0.0, 0x1C: 0.0}}})

    # 28: gate2 arm (t9=0x12) - r15 += row+0x18 -> a20/out[0x0f],
    # edi += row+0x19 -> ad8/out[0x10]/out[0x12]; row+0x19=0 leaves ad8=0
    rows = k0_row({0x18: 0, 0x19: 0, 0x1D: 0, 0x2A: 77,
                     0x48: dw(0), 0x4C: dw(0)})
    eb = RESB + 0 * 0x30
    rows[eb + 9] = 0x12                      # t9=0x12 -> cls6 -> gate2
    rows[eb + 0x18] = 100                    # r15 += 100 -> a20=100
    rows[eb + 0x19] = 0                      # edi += 0 -> ad8 stays 0
    for j, b in enumerate(dw(0x900)):
        rows[eb + 0x28 + j] = b
    rres = RESB + 0x900
    for o in range(0x15):
        rows[rres + o] = 0
    cases.append({"name": "kind0-gate2-arm",
                  "equip": [0x1000, 0, 0, 0, 0], "rows": rows,
                  "rec": {"b": {4: 0x1B, 5: 0, 0x20: 0, 0x88: 0, 0x1C2: 0},
                          "d": {8: 0, 0x3C: 0}, "h": {0x0C: 0},
                          "f": {0x10: 0.0, 0x14: 0.0, 0x18: 0.0, 0x1C: 0.0}}})

    # 29: flag5c=1 with acc40 in (0x3fff, 0x7fff) -> the second write's
    # 0x7fff cap is observable (mutant to 0x3fff must diverge)
    cases.append({"name": "kind0-cap7fff",
                  "equip": [0] * 5,
                  "rows": k0_row({0x18: 0x3F, 0x19: 0x40, 0x1D: 0, 0x2A: 0,
                                    0x48: dw(0), 0x4C: dw(0)}),
                  "rec": {"b": {4: 0x1B, 5: 0, 0x20: 0, 0x88: 0, 0x1C2: 0},
                          "d": {8: 0x200, 0x3C: 0}, "h": {0x0C: 0},
                          "f": {0x10: 0.0, 0x14: 0.0, 0x18: 0.0, 0x1C: 0.0}}})

    # 30: kind!=0, rowA[0x15]&1 -> flag4c=0 -> gate1 arm skipped
    # (ae8/r14 do NOT take row+0x1A/0x1D); bit0 block also adds to ae8/a24
    tabs, rows = k1_fixture(rowa15=1, eqspec=[(0x05, 0x900)])
    cases.append({"name": "kind1-flag4c-off", "equip": [0x1000, 0, 0, 0, 0],
                  "tabs": tabs, "rows": rows,
                  "rec": {"b": {4: 0x1B, 5: 1, 0x20: 0, 0x88: 1, 0x1C2: 5},
                          "d": {8: 0, 0x3C: 0}, "h": {0x0C: 0},
                          "f": {0x10: 0.0, 0x14: 0.0, 0x18: 0.0, 0x1C: 0.0}}})

    # 30: kind!=0, rowA[0x15]&2 -> flag70=0 -> gate2 arm skipped
    tabs, rows = k1_fixture(rowa15=2, eqspec=[(0x12, 0x900)])
    cases.append({"name": "kind1-flag70-off", "equip": [0x1000, 0, 0, 0, 0],
                  "tabs": tabs, "rows": rows,
                  "rec": {"b": {4: 0x1B, 5: 1, 0x20: 0, 0x88: 1, 0x1C2: 5},
                          "d": {8: 0, 0x3C: 0}, "h": {0x0C: 0},
                          "f": {0x10: 0.0, 0x14: 0.0, 0x18: 0.0, 0x1C: 0.0}}})

    # 31: rcx=0 + rdx-supplied -> memset ok, kindb=0xFF arm reads
    # byte[rdi+4]=[4] after the rowA defrow's two resolves -> fault at 4
    cases.append({"name": "kind0-rcx0-rdx", "rcx": 0, "rdx": OUT,
                  "rec": None, "equip": [0] * 5, "exp_fault": True})

    return cases


def prep_case(case, raw, secs):
    """Derive mask_bits fixture: set rec mask bits for all T1/T2/T3
    entries with index >= 5, and plant status rows."""
    if not case.get("mask_bits"):
        return case
    rows = dict(case.get("rows", {}))
    rec = case.get("rec") or base_rec()
    b = dict(rec.get("b", {}))
    for tab, bound in ((T1, 0x10), (T2, 0x10), (T3, 0x0C)):
        for i in range(0, bound):
            sid = img(raw, secs, tab + i, 1)[0]
            bi, bit = sid >> 3, sid & 7
            b[0x68 + bi] = b.get(0x68 + bi, 0) | (1 << bit)
            # plant a status row word[+4] = sid+1
            rows[RESB + sid * 0x30 + 4] = (sid + 1) & 0xFF
            rows[RESB + sid * 0x30 + 5] = ((sid + 1) >> 8) & 0xFF
    rec["b"] = b
    case["rec"] = rec
    case["rows"] = rows
    return case


# ---- mutants -----------------------------------------------------------------
def mutants(raw, secs):
    """(name, va, orig, patch). orig verified against shipped bytes."""
    M = []
    def add(name, va, orig, patch):
        assert img(raw, secs, va, len(orig)) == orig, \
            "mutant %s orig mismatch at %x" % (name, va)
        M.append({"name": name, "va": va, "patch": patch})

    add("m-eqloop-bound", 0x2FF57A, b"\x05", b"\x03")          # cmp rbp,5->3
    add("m-t1-bound", 0x2FF63B, b"\x10", b"\x08")              # cmp rbx,0x10->8
    add("m-t3-bound", 0x2FF779, b"\x0c", b"\x08")              # cmp rbx,0x0c->8
    add("m-eq-sub", 0x2FF43D, b"\x00\x10\x00\x00",
        b"\x00\x20\x00\x00")                                    # sub 0x1000->0x2000
    add("m-g1-srcoff", 0x2FF498, b"\x1a", b"\x1b")             # row+0x1A->+0x1B
    add("m-diffmask", 0x2FF98A, b"\x20\x00\x00\x08",
        b"\x40\x00\x00\x08")                                    # test mask
    add("m-bt-bit", 0x2FF9A0, b"\x18", b"\x19")                # bt rax,0x18->0x19
    add("m-btr-bit", 0x2FFA10, b"\x0e", b"\x0f")               # btr rcx,0xe->0xf
    add("m-or-flag", 0x2FFA3C, b"\x00\x00\x20\x00",
        b"\x00\x00\x40\x00")                                    # or +4,0x200000->0x400000
    add("m-788-mask", 0x2FFA1B, b"\xff\xfb\xff\xff",
        b"\xff\xf7\xff\xff")                                    # &~0x400->&~0x800
    add("m-6b0-mask", 0x2FFA29, b"\xfd", b"\xfe")              # &~2 -> &~1
    add("m-cap7fff", 0x2FF7F7, b"\xff\x7f\x00\x00",
        b"\xff\x3f\x00\x00")                                    # 0x7fff->0x3fff
    add("m-clamp63", 0x2FF82B, b"\x63\x00\x00\x00",
        b"\x32\x00\x00\x00")                                    # 0x63->0x32
    add("m-kind-off", 0x2FEFFE, b"\x05", b"\x04")              # byte[rdi+5]->+4
    add("m-lvldelta", 0x2FF200, b"\x2b\xc8", b"\x03\xc8")      # sub->add
    return M


def main():
    raw, secs = load_image()
    muts = mutants(raw, secs)
    npass = nfail = 0
    out = {"exe_sha256": SHA, "subject": "0x%X" % SUBJ,
           "cases": [], "mutants": []}
    base_results = {}
    for case in build_cases():
        case = prep_case(case, raw, secs)
        tr, faults, w, obs = run_case(case, raw, secs)
        exp_tr, exp = exp_obs(case, w, raw, secs)
        fault_seen = [f for f in faults if f[0] == "MEM"]
        if case.get("exp_fault"):
            ok = bool(fault_seen) and tr == exp_tr
            if ok and exp.get("fault") is not None:
                ok = any(f[1] == hex(exp["fault"]) for f in fault_seen)
        else:
            ok = (tr == exp_tr and obs["out"] == exp["out"]
                  and not fault_seen
                  and all(obs[k] == exp[k] for k in exp if k != "out"
                          and k != "fault"))
        npass += ok
        nfail += (not ok)
        base_results[case["name"]] = (tr, obs, bool(fault_seen))
        if not ok:
            print("FAIL %s\n  got:  %s\n  want: %s\n  out got %s\n  out exp %s\n"
                  "  faults=%s" % (case["name"], tr, exp_tr,
                                   obs["out"].hex(), exp["out"].hex(),
                                   faults))
        else:
            print("PASS %s" % case["name"])
        out["cases"].append({"name": case["name"], "trace": tr,
                             "ok": bool(ok),
                             "obs": {k: (v.hex() if isinstance(v, bytes)
                                     else v) for k, v in obs.items()},
                             "exp_trace": exp_tr, "faults": faults})
    print("cases: %d/%d" % (npass, npass + nfail))

    # mutants: pick a case that exercises each site and expect divergence
    mspec = {
        "m-eqloop-bound": "kind0-all-gates",
        "m-t1-bound": "kind0-bitmask",
        "m-t3-bound": "kind0-bitmask",
        "m-eq-sub": "kind0-basic-gate3",
        "m-g1-srcoff": "kind0-all-gates",
        "m-diffmask": "kind0-reset-runs",
        "m-bt-bit": "kind0-skipreset-bit24",
        "m-btr-bit": "kind0-ba0-clear",
        "m-or-flag": "kind0-reset-runs",
        "m-788-mask": "kind0-reset-runs",
        "m-6b0-mask": "kind0-reset-runs",
        "m-cap7fff": "kind0-cap7fff",
        "m-clamp63": "kind0-clamps",
        "m-kind-off": "kind0-basic-gate3",
        "m-lvldelta": "kind1-four-rows",
    }
    mkilled = 0
    for m in muts:
        cname = mspec[m["name"]]
        case = next(c for c in build_cases() if c["name"] == cname)
        case = prep_case(case, raw, secs)
        case = dict(case)
        case["patch_bytes"] = [(m["va"], m["patch"])]
        tr, faults, w, obs = run_case(case, raw, secs)
        btr, bobs, bflt = base_results[cname]
        diverged = (tr != btr) or (obs["out"] != bobs["out"]) \
            or bool([f for f in faults if f[0] == "MEM"]) != bflt \
            or any(obs[k] != bobs[k] for k in obs
                   if k not in ("out", "ret"))
        mkilled += diverged
        print("MUT %s %-18s case=%-22s %s" %
              ("KILLED" if diverged else "ALIVE ", m["name"], cname,
               tr[:110]))
        out["mutants"].append({"name": m["name"], "va": "0x%X" % m["va"],
                               "case": cname, "killed": bool(diverged),
                               "trace": tr})
    print("mutants: %d/%d killed" % (mkilled, len(muts)))
    json.dump(out, open("result.json", "w"), indent=1,
              default=lambda o: o.hex() if isinstance(o, bytes) else str(o))
    return 0 if (nfail == 0 and mkilled == len(muts)) else 1


if __name__ == "__main__":
    sys.exit(main())
