# EXP-118 transform-vec-writer-exec — native replay harness.
#
# Executes the real shipped bodies of the three-arm transform-vec
# writer family under Unicorn over the real shipping EXE image:
#
#   GETV 003E5B30  338B — get_vec(rec, field, out):
#     field==0xb : 00422D50 -> b[obj+0x328] sel -> 0041C970 scan ->
#                  q[entry+0x70] -> d[ptr+4]&3 selects +0x30/+0x60 base
#                  -> out={d[+34],d[+38],d[+3C],1.0f}, ret w[base+0x30];
#                  any null arm -> 003E6DA0 fallback
#                  -> out={d[p+4C],d[p+50],d[p+54],1.0f} or {0,0,0,1.0f}
#     field!=0xb : ftab=q[rec+0x400] -> off=w[ftab+0xC] ->
#                  rdx=sx32(ftab+off) -> entry=rdx+field*16 ->
#                  out={d[+4],f[+8],f[+C],1.0f}, ret w[entry];
#                  missing -> {0,0,0,1.0f}, ret 0xFFFFFFFF
#   G42  00422D50   57B — gate d[+0xC4]==-1 -> 0; else BASE(d[+0x10])
#                  -> rcx=q[base+0xDA8] -> jmp 0051B9E0 (scripted T51)
#   G41  0041C970   50B — scan leaf: sx16(w[rcx+0x28]) entries at
#                  rcx+0x30+i*0xA0, match d[entry+0x80]==edx -> entry
#   D6A  003E6DA0   67B — idx guard x2 + BASE + MIDS + tail 00370E20
#   MIDS 002ED570  146B — conditional deposits + signed product
#   RES  003AB7F0   99B — two-way dispatch + <=0x40 result bound
#   BASE 0020E600   10B — codec base
#
# Scripted boundaries (planted returns, args traced):
#   T51  0051B9E0 — G42's tail target (EXP-109's scripted T51)
#   HRES 0036B130 — RES mode!=0 resolver (executed real in EXP-084)
#   E20  00370E20 — D6A's deep tail (returns the fallback pointer)
#
# Native and model must agree on trace/rets/faults/out-vec4.

import ctypes
import hashlib
import json
import struct
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from unicorn import Uc, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE, \
    UC_HOOK_MEM_UNMAPPED, UC_PROT_ALL, UcError
from unicorn.x86_const import UC_X86_REG_RAX, UC_X86_REG_RCX, \
    UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_RSP, UC_X86_REG_RIP

EXE = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe"
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
RESULT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "result.json")

IMG_LO = 0x120000
IMG_HI = 0x30A0000
HEAP   = 0x40000000
STACK  = 0x61000000
RETQ   = 0x62000000

GETV = 0x003E5B30
G42  = 0x00422D50
G41  = 0x0041C970
D6A  = 0x003E6DA0
MIDS = 0x002ED570
RES  = 0x003AB7F0
BASE = 0x0020E600
T51  = 0x0051B9E0    # G42 tail    — scripted boundary
HRES = 0x0036B130    # RES mode arm — scripted boundary
E20  = 0x00370E20    # D6A tail    — scripted boundary

CODEC = 0x01F83530   # q: arena codec base (shipped global)

# planted fixture addresses
REC    = HEAP + 0x100000          # the record arg
OBJ    = HEAP + 0x200000          # t51 planted return (scan object)
PTR    = HEAP + 0x300000          # q[entry+0x70] payload ptr
FALLP  = HEAP + 0x400000          # e20 planted return (d6a result)
FTAB2  = HEAP + 0x500000          # arm-3 field table q[rec+0x400]
MCTX   = HEAP + 0x700000          # MIDS context object
OUTB   = HEAP + 0x800000          # out vec4 arg
ARENA  = HEAP + 0x600000          # arena base (codec value)
TCTX   = HEAP + 0x900000          # q[ARENA+coff+0xDA8] value


def qw(v): return struct.pack("<Q", v & 0xFFFFFFFFFFFFFFFF)
def dw(v): return struct.pack("<I", v & 0xFFFFFFFF)
def ww(v): return struct.pack("<H", v & 0xFFFF)


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


def img_rd(raw, secs, va, n):
    rva = va - IMG_LO
    for sva, vs, ra, rs in secs:
        if sva <= rva and rva + n <= sva + rs:
            return raw[ra + (rva - sva): ra + (rva - sva) + n]
    raise KeyError("image read outside shipped bytes: %x" % va)


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
    def qw(self, addr):
        return struct.unpack("<Q", self.r(addr, 8))[0]
    def dw(self, addr):
        return struct.unpack("<I", self.r(addr, 4))[0]


ONE_F = 0x3F800000
ENT_ST = 0xA0          # G41 entry stride
ROW_ST = 16            # arm-3 table row stride


def build_fixture(case):
    """bytes/plants shared by native World and python model."""
    W = []
    # --- record ---
    coff = case.get("coff", 0)
    W.append((REC + 0x10, dw(coff)))
    W.append((REC + 0x18, dw(case.get("idx", 5) & 0xFFFFFFFF)))
    W.append((REC + 0xC4, dw(case.get("gate", 5) & 0xFFFFFFFF)))
    W.append((REC + 0x400, qw(case.get("ftab", 0))))
    # --- codec globals: BASE -> ARENA; G42 reads +0xDA8, D6A +0xD98 ---
    W.append((CODEC, qw(ARENA)))
    W.append((ARENA + coff + 0xDA8, qw(case.get("tctx", TCTX))))
    W.append((ARENA + coff + 0xD98, qw(case.get("midctx", MCTX))))
    # --- scan object (t51 planted return) ---
    obj = case.get("obj", OBJ)
    W.append((obj + 0x28, ww(case.get("cnt", 3) & 0xFFFF)))
    W.append((obj + 0x328, bytes([case.get("sel", 2) & 0xFF])))
    for i, e in case.get("entries", {}).items():
        base = obj + 0x30 + i * ENT_ST
        W.append((base + 0x70, qw(e.get("ptr", 0))))
        W.append((base + 0x80, dw(e.get("key", 0))))
    # --- payload ptr: d[+4] mode; bases +0x30 / +0x60 ---
    ptr = case.get("ptr", PTR)
    W.append((ptr + 4, dw(case.get("mode", 0))))
    for bn, bkey in ((0x30, "b30"), (0x60, "b60")):
        bl = case.get(bkey, {})
        base = ptr + bn
        W.append((base + 0x30, ww(bl.get("tag", 0))))
        W.append((base + 0x34, dw(bl.get("x", 0))))
        W.append((base + 0x38, dw(bl.get("y", 0))))
        W.append((base + 0x3C, dw(bl.get("z", 0))))
    # --- fallback pointer (e20 planted return): +0x4C/50/54 ---
    fp = case.get("fallp", FALLP)
    fl = case.get("fall", {})
    W.append((fp + 0x4C, dw(fl.get("x", 0))))
    W.append((fp + 0x50, dw(fl.get("y", 0))))
    W.append((fp + 0x54, dw(fl.get("z", 0))))
    # --- arm-3 field table ---
    ft = case.get("ftab", 0)
    if ft:
        W.append((ft + 0xC, ww(case.get("foff", 0x40))))
        rdx = (ft + case.get("foff", 0x40)) & 0xFFFFFFFF
        for f, row in case.get("rows", {}).items():
            e = (rdx + f * ROW_ST) & 0xFFFFFFFFFFFFFFFF
            W.append((e + 0, ww(row.get("tag", 0))))
            W.append((e + 4, dw(row.get("x", 0))))
            W.append((e + 8, dw(row.get("y", 0))))
            W.append((e + 0xC, dw(row.get("z", 0))))
    # --- MIDS context ---
    mc = case.get("mctx", {})
    W.append((MCTX + 0x30, qw(mc.get("h30", 0))))
    W.append((MCTX + 0x38, qw(0)))
    W.append((MCTX + 0x08, qw(mc.get("h08", 0))))
    W.append((MCTX + 0x10, qw(0)))
    W.append((MCTX + 0x4C, dw(mc.get("shift", 2))))
    W.append((MCTX + 0x48, dw(mc.get("mult", 0x40))))
    W.append((MCTX + 0x50, dw(mc.get("mask", 0xFF))))
    for edx, v in mc.get("elem", {}).items():
        W.append((mc.get("h30", 0) + edx * 16, dw(v & 0xFFFFFFFF)))
    for idx, v in mc.get("rt_e10", {}).items():
        W.append((mc.get("h08", 0) + idx * 32 + 0x10, dw(v)))
    return W


class World:
    def __init__(self, case, raw, secs):
        self.case = case
        self.raw, self.secs = raw, secs
        self.uc = Uc(UC_ARCH_X86, UC_MODE_64)
        gm = self.gm = GuestMem(self.uc)
        gm.map(IMG_LO, IMG_HI - IMG_LO)
        for sva, vs, ra, rs in secs:
            if vs and rs:
                gm.w(IMG_LO + sva, raw[ra:ra + min(rs, vs)])
        gm.map(HEAP, 0x1000000)
        gm.map(STACK, 0x100000)
        gm.map(RETQ, 0x1000)
        for addr, dat in build_fixture(case):
            gm.w(addr, dat)
        for addr, dat in case.get("patch_bytes", []):
            gm.w(addr, dat)
        self.trace, self.faults, self.rets = [], [], []
        self.uc.hook_add(UC_HOOK_CODE, self.on_code)
        self.uc.hook_add(UC_HOOK_MEM_UNMAPPED, self.on_bad)

    def on_code(self, uc, addr, size, _):
        if addr == T51:
            # scripted boundary: record args, plant return, pop call
            self.trace.append("t51:%x:%x" % (
                uc.reg_read(UC_X86_REG_RCX),
                uc.reg_read(UC_X86_REG_RDX)))
            uc.reg_write(UC_X86_REG_RAX, self.case.get("t51_ret", 0))
            uc.reg_write(UC_X86_REG_RIP, self.gm.qw(
                uc.reg_read(UC_X86_REG_RSP)))
            uc.reg_write(UC_X86_REG_RSP,
                         uc.reg_read(UC_X86_REG_RSP) + 8)
        elif addr == HRES:
            self.trace.append("hres:%x" % uc.reg_read(UC_X86_REG_RCX))
            ret = self.case.get("hres_map", {}).get(
                uc.reg_read(UC_X86_REG_RCX), 0)
            uc.reg_write(UC_X86_REG_RAX, ret)
            uc.reg_write(UC_X86_REG_RIP, self.gm.qw(
                uc.reg_read(UC_X86_REG_RSP)))
            uc.reg_write(UC_X86_REG_RSP,
                         uc.reg_read(UC_X86_REG_RSP) + 8)
        elif addr == E20:
            # tail-call boundary: inherits caller's frame -> ret to it
            self.trace.append("e20:%x" % uc.reg_read(UC_X86_REG_RCX))
            uc.reg_write(UC_X86_REG_RAX,
                         self.case.get("e20_ret", 0))
            uc.reg_write(UC_X86_REG_RIP, self.gm.qw(
                uc.reg_read(UC_X86_REG_RSP)))
            uc.reg_write(UC_X86_REG_RSP,
                         uc.reg_read(UC_X86_REG_RSP) + 8)

    def on_bad(self, uc, access, addr, size, value, _):
        self.faults.append((access, addr, size))
        uc.emu_stop()
        return True

    def run_one(self, entry, rcx, rdx=0, r8=0):
        uc = self.uc
        self.gm.w(RETQ, b"\xc3" * 0x100)
        rsp = STACK + 0x80000
        self.gm.w(rsp, qw(RETQ))
        uc.reg_write(UC_X86_REG_RSP, rsp)
        uc.reg_write(UC_X86_REG_RCX, rcx)
        uc.reg_write(UC_X86_REG_RDX, rdx)
        uc.reg_write(UC_X86_REG_R8, r8)
        try:
            uc.emu_start(entry, RETQ, count=60000)
        except UcError as e:
            if not self.faults:
                self.faults.append(("emuerr", str(e)))
        self.rets.append(uc.reg_read(UC_X86_REG_RAX))

    def run(self):
        for entry, rcx, rdx, r8 in self.case.get("steps", []):
            self.run_one(entry, rcx, rdx, r8)

    def obs(self):
        return {"trace": self.trace, "faults": self.faults,
                "rets": self.rets,
                "out": self.gm.r(OUTB, 16).hex(),
                "m38": self.gm.qw(MCTX + 0x38),
                "m10": self.gm.qw(MCTX + 0x10)}


# ---------------- python model ----------------
# the model interprets the same planted fixture bytes — md/mw/mq/mb
# read the shared image so there is no parallel param copy.

def sx16(v):
    v &= 0xFFFF
    return v - 0x10000 if v & 0x8000 else v


def sx32(v):
    v &= 0xFFFFFFFF
    return v - 0x100000000 if v & 0x80000000 else v


class Model:
    def __init__(self, case):
        self.case = case
        self.mem = {}
        for addr, dat in build_fixture(case):
            for i, b in enumerate(dat):
                self.mem[addr + i] = b
        self.trace, self.faults, self.rets = [], [], []

    def mb(self, a): return self.mem.get(a & 0xFFFFFFFFFFFFFFFF, 0)
    def mw(self, a): return self.mb(a) | (self.mb(a + 1) << 8)
    def md(self, a):
        return self.mb(a) | (self.mb(a + 1) << 8) | \
            (self.mb(a + 2) << 16) | (self.mb(a + 3) << 24)
    def mq(self, a): return self.md(a) | (self.md(a + 4) << 32)

    def res(self, h):
        """RES dispatch: null->0, low2==0->identity, else hres;
        resolved sx32 <= 0x40 zeroed (EXP-117)."""
        if h == 0:
            return 0
        if h & 3 == 0:
            return h
        self.trace.append("hres:%x" % h)
        r = self.case.get("hres_map", {}).get(h, 0)
        if sx32(r) & 0xFFFFFFFFFFFFFFFF <= 0x40:
            return 0
        return r

    def mids(self, edx):
        mc = self.case.get("mctx", {})
        h30 = self.res(mc.get("h30", 0))
        h08 = self.res(mc.get("h08", 0))
        # deposits hold the resolved handles; null fields skip the
        # RES call and leave the stale slot (fixture zero) alone
        self.d38 = h30 if mc.get("h30", 0) else 0
        self.d10 = h08 if mc.get("h08", 0) else 0
        shift = mc.get("shift", 2)
        mult = mc.get("mult", 0x40)
        mask = mc.get("mask", 0xFF)
        gate = self.md(h30 + edx * 16)
        e10 = self.md(h08 + (edx >> shift) * 32 + 0x10)
        base_v = (e10 + ARENA) & 0xFFFFFFFFFFFFFFFF
        if gate == 0xFFFFFFFF:
            return 0
        prod32 = ((mask & edx) * mult) & 0xFFFFFFFF
        return (base_v + sx32(prod32)) & 0xFFFFFFFFFFFFFFFF

    def d6a(self, rec):
        idx = sx32(self.md(rec + 0x18))
        if idx == -1:
            return 0
        base_v = (self.md(rec + 0x10) + ARENA) & 0xFFFFFFFFFFFFFFFF
        r = self.mids(idx)
        if r == 0:
            return 0
        self.trace.append("e20:%x" % r)
        return self.case.get("e20_ret", 0)

    def g42(self, rec):
        gate = sx32(self.md(rec + 0xC4))
        if gate == -1:
            return 0
        coff = self.md(rec + 0x10)
        tctx = self.mq(ARENA + coff + 0xDA8)
        self.trace.append("t51:%x:%x" % (tctx, gate & 0xFFFFFFFF))
        return self.case.get("t51_ret", 0)

    def g41(self, obj, sel):
        cnt = sx16(self.mw(obj + 0x28))
        for i in range(max(cnt, 0)):
            e = obj + 0x30 + i * ENT_ST
            if self.md(e + 0x80) == sel:
                return e
        return 0

    def getv(self, rec, field, out):
        """003E5B30 — returns (eax_ret, out16_bytes)."""
        field = sx32(field)
        b = bytearray(16)
        ret = 0
        if field == 0xB:
            base = 0
            obj = self.g42(rec)
            if obj:
                sel = self.mb(obj + 0x328)
                if sel:
                    e = self.g41(obj, sel)
                    if e:
                        ptr = self.mq(e + 0x70)
                        if ptr:
                            mode = self.md(ptr + 4) & 3
                            if mode == 0:
                                base = ptr + 0x30
                            elif mode == 1:
                                base = ptr + 0x60
            if base:
                b[0:4] = dw(self.md(base + 0x34))
                b[4:8] = dw(self.md(base + 0x38))
                b[8:0xC] = dw(self.md(base + 0x3C))
                b[0xC:0x10] = dw(ONE_F)
                ret = self.mw(base + 0x30)
            else:
                p = self.d6a(rec)
                if p:
                    b[0:4] = dw(self.md(p + 0x4C))
                    b[4:8] = dw(self.md(p + 0x50))
                    b[8:0xC] = dw(self.md(p + 0x54))
                    b[0xC:0x10] = dw(ONE_F)
                else:
                    b[0xC:0x10] = dw(ONE_F)
                ret = 0
        else:
            ft = self.mq(rec + 0x400)
            done = False
            if ft:
                off = self.mw(ft + 0xC)
                if off:
                    rdx = sx32((ft + off) & 0xFFFFFFFF)
                    if rdx:
                        e = (rdx + field * ROW_ST) & \
                            0xFFFFFFFFFFFFFFFF
                        b[0:4] = dw(self.md(e + 4))
                        b[4:8] = dw(self.md(e + 8))
                        b[8:0xC] = dw(self.md(e + 0xC))
                        b[0xC:0x10] = dw(ONE_F)
                        ret = self.mw(e)
                        done = True
            if not done:
                b[0xC:0x10] = dw(ONE_F)
                ret = 0xFFFFFFFF
        return ret, bytes(b)


def run_model(case):
    m = Model(case)
    for entry, rcx, rdx, r8 in case.get("steps", []):
        if entry == GETV:
            ret, out16 = m.getv(rcx, rdx, r8)
            m.rets.append(ret)
            m.out16 = out16
        elif entry == G42:
            m.rets.append(m.g42(rcx))
        elif entry == G41:
            m.rets.append(m.g41(rcx, rdx & 0xFFFFFFFF))
        elif entry == D6A:
            m.rets.append(m.d6a(rcx))
        elif entry == MIDS:
            m.rets.append(m.mids(sx32(rdx)))
        elif entry == RES:
            m.rets.append(m.res(rcx))
    return {"trace": m.trace, "faults": m.faults, "rets": m.rets,
            "out": getattr(m, "out16", bytes(16)).hex(),
            "m38": getattr(m, "d38", 0),
            "m10": getattr(m, "d10", 0)}


# ---------------- cases ----------------

E1 = {"key": 1, "ptr": 0}
E2 = {"key": 2, "ptr": PTR}
E3 = {"key": 3, "ptr": 0}
B30 = {"tag": 0x1234, "x": 0xAAAA0001, "y": 0xBBBB0002,
       "z": 0xCCCC0003}
B60 = {"tag": 0x5678, "x": 0xDDDD0004, "y": 0xEEEE0005,
       "z": 0xFFFF0006}
FALL = {"x": 0x11110001, "y": 0x22220002, "z": 0x33330003}
ROWS = {0: {"tag": 0xA0, "x": 0x100, "y": 0x200, "z": 0x300},
        3: {"tag": 0xB0, "x": 0x400, "y": 0x500, "z": 0x600},
        7: {"tag": 0xC0, "x": 0x700, "y": 0x800, "z": 0x900},
        -1: {"tag": 0xD0, "x": 0xA00, "y": 0xB00, "z": 0xC00}}
MC = {"h30": HEAP + 0x780000, "h08": HEAP + 0x790000,
      "elem": {5: 3}, "rt_e10": {1: 0x10}}
# shared fallback fixture: arm-1 null paths reach d6a -> mids -> e20
# -> FALLP, producing the FALL vec instead of {0,0,0,1.0f}
FB = {"idx": 5, "mctx": MC, "e20_ret": FALLP, "fall": FALL}


def arm1(extra=None, **kw):
    c = {"gate": 5, "t51_ret": OBJ, "sel": 2, "cnt": 3,
         "entries": {0: E1, 1: E2, 2: E3},
         "mode": 0, "b30": B30, "b60": B60,
         "idx": -1,
         "steps": [(GETV, REC, 0xB, OUTB)]}
    c.update(kw)
    if extra:
        c.update(extra)
    return c


def build_cases():
    C = {}
    # ---- arm 1: field 0xb happy paths ----
    C["arm1-mode0"] = arm1()
    C["arm1-mode1"] = arm1(mode=1)
    # mode=4: &3==0 -> +0x30 base; discriminates the &7 mask mutant
    C["arm1-mode4"] = arm1(mode=4)
    # mode 2/3: the jne routes to the d6a fallback
    C["arm1-mode2"] = arm1(mode=2, **FB)
    C["arm1-mode3"] = arm1(mode=3, **FB)
    # ---- arm 1 null-path fallthroughs -> arm 2 ----
    C["arm1-gate-neg1"] = arm1(gate=-1, **FB)
    C["arm1-t51-zero"] = arm1(t51_ret=0, **FB)
    C["arm1-sel-zero"] = arm1(sel=0, **FB)
    C["arm1-noscan"] = arm1(sel=9, **FB)
    C["arm1-null70"] = arm1(entries={0: E1, 1: {"key": 2, "ptr": 0},
                                   2: E3}, **FB)
    C["arm1-count-neg"] = arm1(cnt=0xFFFF, **FB)  # sx16 -> -1 -> jle
    # ---- arm 2: the d6a fallback proper ----
    C["arm2-happy"] = arm1(gate=-1, idx=5, mctx=MC,
                           e20_ret=FALLP, fall=FALL)
    C["arm2-mids-zero"] = arm1(gate=-1, idx=5,
                              mctx={"h30": HEAP + 0x780000,
                                    "h08": HEAP + 0x790000,
                                    "elem": {5: -1},
                                    "rt_e10": {1: 0x10}},
                              e20_ret=FALLP, fall=FALL)
    C["arm2-e20-zero"] = arm1(gate=-1, idx=5, mctx=MC,
                              e20_ret=0, fall=FALL)
    C["arm2-d6a-neg"] = arm1(gate=-1, idx=-1, fall=FALL)
    # ---- arm 3: indexed table ----
    C["arm3-basic"] = {"ftab": FTAB2, "rows": ROWS,
                       "steps": [(GETV, REC, 3, OUTB)]}
    C["arm3-field0"] = {"ftab": FTAB2, "rows": ROWS,
                        "steps": [(GETV, REC, 0, OUTB)]}
    C["arm3-field7"] = {"ftab": FTAB2, "rows": ROWS,
                        "steps": [(GETV, REC, 7, OUTB)]}
    # negative field: rcx*8 wraps to rdx-16 — discriminates sx/add
    C["arm3-negfield"] = {"ftab": FTAB2, "rows": ROWS,
                          "steps": [(GETV, REC, 0xFFFFFFFF, OUTB)]}
    C["arm3-noftab"] = {"steps": [(GETV, REC, 3, OUTB)]}
    C["arm3-nooff"] = {"ftab": FTAB2, "foff": 0, "rows": ROWS,
                       "steps": [(GETV, REC, 3, OUTB)]}
    # ---- direct helper entries ----
    C["g42-ok"] = {"gate": 7, "coff": 0x40,
                   "steps": [(G42, REC, 0, 0)]}
    C["g42-neg1"] = {"gate": -1, "steps": [(G42, REC, 0, 0)]}
    C["g41-scan"] = {"cnt": 3, "sel": 2,
                     "entries": {0: E1, 1: E2, 2: E3},
                     "steps": [(G41, OBJ, 2, 0)]}
    C["g41-nomatch"] = {"cnt": 3, "entries": {0: E1, 1: E2, 2: E3},
                        "steps": [(G41, OBJ, 9, 0)]}
    C["g41-count0"] = {"cnt": 0, "entries": {0: E1},
                       "steps": [(G41, OBJ, 1, 0)]}
    return C


# ---------------- mutations (verified byte-precise) ----------------

def B(x): return bytes([x])
def W(x): return struct.pack("<i", x)

MUTS = [
    # GETV: field cmp 0xb -> 0xc (arm1 unreachable for 0xb)
    ("m-gtv-field",  0x3E5B46, B(0x0B), B(0x0C), "arm1-mode0"),
    # GETV: sel byte disp +0x328 -> +0x329
    ("m-gtv-sel",    0x3E5B5A, B(0x28), B(0x29), "arm1-mode0"),
    # GETV: entry ptr disp +0x70 -> +0x78
    ("m-gtv-70",     0x3E5B75, B(0x70), B(0x78), "arm1-mode0"),
    # GETV: and eax,3 -> and eax,7 (mode 4 falls to fallback)
    ("m-gtv-and",    0x3E5B80, B(0x03), B(0x07), "arm1-mode4"),
    # GETV: cmp eax,1 -> cmp eax,0 (mode-1 arm unreachable)
    ("m-gtv-mode",   0x3E5B85, B(0x01), B(0x00), "arm1-mode1"),
    # GETV: mode-1 base +0x60 -> +0x70
    ("m-gtv-b60",    0x3E5B8B, B(0x60), B(0x70), "arm1-mode1"),
    # GETV: mode-0 base +0x30 -> +0x40
    ("m-gtv-b30",    0x3E5B91, B(0x30), B(0x40), "arm1-mode0"),
    # GETV: out.x source +0x34 -> +0x38 (x = y)
    ("m-gtv-x",      0x3E5B99, B(0x34), B(0x38), "arm1-mode0"),
    # GETV: out.w imm 0x3F800000 -> 0x3F800001
    ("m-gtv-w",      0x3E5BAC, B(0x00), B(0x01), "arm1-mode0"),
    # GETV: ret word disp +0x30 -> +0x34 (ret = out.x low)
    ("m-gtv-ret",    0x3E5BB2, B(0x30), B(0x34), "arm1-mode0"),
    # GETV: fallback out.x source +0x4C -> +0x50
    ("m-gtv-4c",     0x3E5BCF, B(0x4C), B(0x50), "arm2-happy"),
    # GETV: ftab qword disp +0x400 -> +0x408 (zero -> zero-out)
    ("m-gtv-ftab",   0x3E5C11, B(0x00), B(0x08), "arm3-basic"),
    # GETV: off word disp +0xC -> +0xE
    ("m-gtv-off",    0x3E5C1D, B(0x0C), B(0x0E), "arm3-basic"),
    # GETV: add rcx,rcx -> sub rcx,rcx (field index -> 0)
    ("m-gtv-addrc",  0x3E5C31, B(0x03), B(0x2B), "arm3-basic"),
    # GETV: arm3 z disp +0xC -> +0x10
    ("m-gtv-e8",     0x3E5C3C, B(0x0C), B(0x10), "arm3-basic"),
    # GETV: arm3 out.w imm -> 0x3F800001
    ("m-gtv-one",    0x3E5C53, B(0x00), B(0x01), "arm3-basic"),
    # G42: gate cmp -1 -> cmp 0 (gate=-1 proceeds to BASE/t51)
    ("m-g42-gate",   0x422D5C, B(0xFF), B(0x00), "g42-neg1"),
    # G42: coff disp +0x10 -> +0x14
    ("m-g42-coff",   0x422D6C, B(0x10), B(0x14), "g42-ok"),
    # G42: ctx qword disp +0xDA8 -> +0xDA0
    ("m-g42-da8",    0x422D7B, B(0xA8), B(0xA0), "g42-ok"),
    # G41: count word disp +0x28 -> +0x2A
    ("m-g41-count",  0x41C974, B(0x28), B(0x2A), "g41-scan"),
    # G41: key disp +0x80 -> +0x88
    ("m-g41-key",    0x41C983, B(0x80), B(0x88), "g41-scan"),
    # G41: entry stride +0xA0 -> +0xA8
    ("m-g41-stride", 0x41C98E, B(0xA0), B(0xA8), "g41-scan"),
]


def run_native(case, raw, secs):
    w = World(case, raw, secs)
    w.run()
    return w.obs()


def differs(k, nv, mv):
    if k == "rets":
        if len(nv) != len(mv):
            return True
        return any(m is not None and n != m for n, m in zip(nv, mv))
    if k == "faults":
        naddrs = sorted(t[1] if isinstance(t[1], int) else -1
                        for t in nv)
        return naddrs != sorted(mv)
    return nv != mv


def main():
    raw, secs = load_image()
    cases = build_cases()
    keys = ("trace", "rets", "out", "m38", "m10", "faults")
    results = {"cases": {}, "mutants": {}, "bad_sites": []}
    fails = 0
    for name, case in cases.items():
        nat = run_native(case, raw, secs)
        mod = run_model(case)
        d = [k for k in keys if k in nat and differs(k, nat[k], mod.get(k))]
        results["cases"][name] = "ok" if not d else {"diff": d}
        if d:
            fails += 1
            print("CASE", name, "DIFF", d)
            for k in d:
                print("  nat:", str(nat.get(k))[:180])
                print("  mod:", str(mod.get(k))[:180])
    print("functional: %d/%d" % (len(cases) - fails, len(cases)))

    for mid, va, orig, mut, cname in MUTS:
        got = img_rd(raw, secs, va, len(orig))
        if got != orig:
            results["bad_sites"].append((mid, hex(va), got.hex()))
            print("BAD SITE", mid, hex(va), "want", orig.hex(),
                  "got", got.hex())
    if results["bad_sites"]:
        print("aborting mutant run — fix sites first")
        json.dump(results, open(RESULT, "w"), indent=1)
        return

    alive = 0
    for mid, va, orig, mut, cname in MUTS:
        case = dict(cases[cname])
        case["patch_bytes"] = list(case.get("patch_bytes", [])) + \
            [(va, mut)]
        try:
            nat = run_native(case, raw, secs)
        except Exception as e:
            print("MUTANT CRASH", mid, repr(e), flush=True)
            results["mutants"][mid] = "crash: %r" % e
            continue
        mod = run_model(case)
        if [k for k in keys if k in nat and differs(k, nat[k], mod.get(k))]:
            results["mutants"][mid] = "killed"
        else:
            results["mutants"][mid] = "ALIVE"
            alive += 1
            print("MUTANT ALIVE", mid, flush=True)
    print("mutants: %d/%d killed" % (len(MUTS) - alive, len(MUTS)))
    json.dump(results, open(RESULT, "w"), indent=1)


if __name__ == "__main__":
    main()
