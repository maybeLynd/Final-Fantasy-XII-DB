# EXP-129 vec3-normalize-exec — native replay harness.
#
# Executes the vec3 normalize/perpendicular pair real:
#
#   DB70 0040DB70 49B — clears b[0x2CA4390], builds the local vec
#        {d[0x1CEBBA8]=1.0f, 0, 0, uninit w} at rsp+0x20, calls B430.
#        NOTE: the +0x2C (w) slot is never written — B430 copies it
#        into local.w which XPROD overwrites (dead field; fixture 0).
#   B430 0040B430 416B — two-stage normalize:
#        stage1: len = sqrtf(x^2+y^2+z^2) via the REAL 00861F14 IAT
#                thunk; s = (len >= d[0x908E10]=~1e-6f) ? 1.0/len : 0
#                (comiss jbe: unordered -> s=1/len, NaN propagates);
#                dir vec -> f[0x2CA43A0..+0xC].
#        stage2: XPROD(local={0,1.0f,d[0xD108A0]=~1e-5f,in.w}, dir)
#                -> renormalize (comiss ja: unordered -> s2=1/len too)
#                -> f[0x2CA43B0..+0xC]. GS cookie + real CHKCK; the
#                exit rax is the cookie ^ frame-rsp residual.
#   XPROD 00202E10 30i — dst = d x a (cross product, w=0), computed
#        in stack temporaries so dst==src aliasing is safe.
#   CHKCK 00808C40 — __security_check_cookie (real).
#   THUNK 00861F14 6B — jmp qword[IAT 0x8C2BB8]; the slot ships the
#        unbound hint record 0x1CCED52 -> api-ms-win-crt-math-l1-1-0!
#        sqrtf. Planted to the SQF trampoline; the import itself is a
#        disclosed scripted boundary computed by the same CRT on the
#        host (correctly-rounded f32 sqrt both sides).
#
# Native and model must agree on trace/rets/faults/watched memory.

import ctypes
import hashlib
import json
import math
import struct
import sys
import os
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from unicorn import Uc, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE, \
    UC_HOOK_MEM_UNMAPPED, UC_HOOK_INTR, UC_PROT_ALL, UcError
from unicorn.x86_const import UC_X86_REG_RAX, UC_X86_REG_RCX, \
    UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_RSP, UC_X86_REG_RIP, \
    UC_X86_REG_XMM0

EXE = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe"
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
RESULT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "result.json")

IMG_LO = 0x120000
IMG_HI = 0x30A0000
HEAP   = 0x40000000
STACK  = 0x61000000
RETQ   = 0x62000000
SQF    = 0x63040000          # planted trampoline: sqrtf import

DB70   = 0x0040DB70
B430   = 0x0040B430
XPROD  = 0x00202E10
THUNKF = 0x00861F14          # real IAT thunk -> sqrtf
CHKCK  = 0x00808C40          # __security_check_cookie - real

SEEDF  = 0x1CEBBA8           # d: 1.0f (rdata, shared by both stages)
EPSF   = 0x908E10            # d: ~1e-6f epsilon (rdata)
C2F    = 0xD108A0            # d: ~1e-5f stage-2 z constant (rdata)
FLAGB  = 0x2CA4390           # b: flag byte cleared by DB70
DIRA   = 0x2CA43A0           # f32 x3: stage-1 direction vec
DIRB   = 0x2CA43B0           # f32 x3: stage-2 direction vec
IATF   = 0x8C2BB8            # q: IAT slot for sqrtf (ships 0x1CCED52)
COOK   = 0x1F44830           # q: __security_cookie (shipped)
GSCOOK = 0x2B992DDFA232      # shipped cookie value

# planted fixture addresses
VEC    = HEAP + 0x10000      # B430's input vec4 arg
VDST   = HEAP + 0x20000      # XPROD dst
VSRC   = HEAP + 0x20010      # XPROD src (d vector)
VA     = HEAP + 0x20020      # XPROD a vector
VDS2   = HEAP + 0x20030      # second XPROD dst (two-call cases)


def qw(v): return struct.pack("<Q", v & 0xFFFFFFFFFFFFFFFF)
def dw(v): return struct.pack("<I", v & 0xFFFFFFFF)
def ff(v): return struct.pack("<f", v)


# ---------------- f32 helpers ----------------
# mulss/addss/subss: the exact result of two f32 operands always fits a
# double, so f32(double op) is correctly rounded. divss is NOT exact in
# double -> f32_round(Fraction) (ties-to-even). sqrtf: the real CRT
# sqrtf on the host when available, else double-rounded fallback.

def f32(x):
    try:
        return struct.unpack("<f", struct.pack("<f", x))[0]
    except OverflowError:
        return math.copysign(float("inf"), x)


def f2u(x):
    return struct.unpack("<I", struct.pack("<f", x))[0]


def u2f(u):
    return struct.unpack("<f", struct.pack("<I", u & 0xFFFFFFFF))[0]


def f32_round(q):
    """Correctly rounded f32 (ties-to-even) of an exact Fraction."""
    if q == 0:
        return 0.0
    sgn = q < 0
    if sgn:
        q = -q
    e = q.numerator.bit_length() - q.denominator.bit_length()
    two = Fraction(2)
    if q < two ** e:
        e -= 1
    elif q >= two ** (e + 1):
        e += 1
    if e >= 128:
        return float("inf")
    unit = two ** (e - 23) if e >= -126 else two ** (-149)
    scaled = q / unit
    n = scaled.numerator // scaled.denominator
    rem = scaled - n
    if rem > Fraction(1, 2) or (rem == Fraction(1, 2) and n & 1):
        n += 1
    if e >= -126 and n >> 24:          # mantissa carry -> next binade
        e += 1
        if e >= 128:
            return float("inf")
        unit = two ** (e - 23)
        n >>= 1
    return f32(float(Fraction(n) * unit))


def _sgn(a, b):
    s = math.copysign(1.0, a) * math.copysign(1.0, b)
    return -1.0 if s < 0 else 1.0


def f32div(a, b):
    if math.isnan(a) or math.isnan(b):
        return float("nan")
    if math.isinf(a):
        return math.copysign(float("inf"), _sgn(a, b))
    if math.isinf(b):
        return math.copysign(0.0, _sgn(a, b))
    if b == 0:
        if a == 0:
            return float("nan")
        return math.copysign(float("inf"), _sgn(a, b))
    r = f32_round(Fraction(a) / Fraction(b))
    if r == 0:
        return math.copysign(0.0, _sgn(a, b))
    return r


_CRT = None
try:
    _CRT = ctypes.CDLL("api-ms-win-crt-math-l1-1-0.dll")
    _CRT.sqrtf.restype = ctypes.c_float
    _CRT.sqrtf.argtypes = (ctypes.c_float,)
except OSError:
    pass


def sqrtf32(x):
    """correctly-rounded f32 sqrt via the real CRT import."""
    if math.isnan(x) or x < 0:
        return float("nan")
    if _CRT is not None:
        return _CRT.sqrtf(x)
    return f32(math.sqrt(x))


def sqrtf_bits(u):
    """sqrtf on raw f32 bits; returns result bits (NaN canonical)."""
    return f2u(sqrtf32(u2f(u)))


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


def build_fixture(case):
    """bytes/plants shared by native World and python model."""
    W = []
    # sqrtf IAT slot -> SQF trampoline
    W.append((IATF, qw(SQF)))
    # flag byte + dir globals (BSS)
    W.append((FLAGB, bytes([case.get("flagb", 1) & 0xFF])))
    W.append((DIRA, b"\x00" * 0x10))
    W.append((DIRB, b"\x00" * 0x10))
    # B430 input vec4 {x, y, z, w}
    vx = case.get("vx", 3.0)
    vy = case.get("vy", 4.0)
    vz = case.get("vz", 0.0)
    vw = case.get("vw", 0.0)
    W.append((VEC, ff(vx) + ff(vy) + ff(vz) + ff(vw)))
    # XPROD direct args: dst/src/a as three vec4s
    W.append((VSRC, ff(case.get("dx", 1.0)) + ff(case.get("dy", 0.0)) +
              ff(case.get("dz", 0.0)) + ff(case.get("dw", 0.0))))
    W.append((VA, ff(case.get("ax", 0.0)) + ff(case.get("ay", 1.0)) +
              ff(case.get("az", 0.0)) + ff(case.get("aw", 0.0))))
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
        gm.map(HEAP, 0x100000)
        gm.map(STACK, 0x100000)
        gm.map(RETQ, 0x1000)
        gm.map(SQF, 0x1000, b"\xc3" * 0x1000)
        for addr, dat in build_fixture(case):
            gm.w(addr, dat)
        for addr, dat in case.get("patch_bytes", []):
            gm.w(addr, dat)
        self.trace, self.faults, self.rets, self.ends = [], [], [], []
        self.uc.hook_add(UC_HOOK_CODE, self.on_code)
        self.uc.hook_add(UC_HOOK_MEM_UNMAPPED, self.on_bad)
        self.uc.hook_add(UC_HOOK_INTR, self.on_intr)

    def _ret(self, uc):
        uc.reg_write(UC_X86_REG_RIP,
                     self.gm.qw(uc.reg_read(UC_X86_REG_RSP)))
        uc.reg_write(UC_X86_REG_RSP,
                     uc.reg_read(UC_X86_REG_RSP) + 8)

    def on_intr(self, uc, intno, _):
        self.faults.append(("trap", uc.reg_read(UC_X86_REG_RIP)))
        uc.emu_stop()

    def on_bad(self, uc, access, addr, size, value, _):
        kind = "memr" if access in (16, 19) else \
               "memf" if access in (18, 21) else "memw"
        self.faults.append((kind, addr, size))
        uc.emu_stop()
        return True

    def on_code(self, uc, addr, size, _):
        if addr == SQF:
            # disclosed import boundary: api-ms-win-crt-math-l1-1-0!
            # sqrtf reached via the real 00861F14 thunk + real IAT
            # slot planted to this trampoline; the host computes the
            # same CRT sqrtf (correctly rounded f32).
            x = uc.reg_read(UC_X86_REG_XMM0)
            lo = x & 0xFFFFFFFF
            r = sqrtf_bits(lo)
            uc.reg_write(UC_X86_REG_XMM0, (x & ~0xFFFFFFFF) | r)
            self.trace.append("sqrtf:%x:%x" % (lo, r))
            self._ret(uc)

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
            uc.emu_start(entry, RETQ, count=200000)
        except UcError as e:
            if not self.faults:
                self.faults.append(("emuerr", str(e)))
        self.ends.append(uc.reg_read(UC_X86_REG_RIP))
        self.rets.append(uc.reg_read(UC_X86_REG_RAX))

    def run(self):
        for step in self.case.get("steps", []):
            entry, rcx = step[0], step[1]
            rdx = step[2] if len(step) > 2 else 0
            r8 = step[3] if len(step) > 3 else 0
            self.run_one(entry, rcx, rdx, r8)

    def obs(self):
        mem = {}
        for addr, n in self.case.get("watch", []):
            try:
                mem["%x" % addr] = self.gm.r(addr, n).hex()
            except KeyError:
                mem["%x" % addr] = None
        return {"trace": self.trace, "faults": self.faults,
                "rets": self.rets, "ends": self.ends, "mem": mem}


# ---------------- python model ----------------

VALID = ((HEAP, HEAP + 0x100000), (IMG_LO, IMG_HI), (STACK, STACK + 0x100000))


class Model:
    def __init__(self, case, raw, secs):
        self.case = case
        self.raw, self.secs = raw, secs
        self.mem = {}
        for addr, dat in build_fixture(case):
            for i, b in enumerate(dat):
                self.mem[addr + i] = b
        for addr, dat in case.get("patch_bytes", []):
            for i, b in enumerate(dat):
                self.mem[addr + i] = b
        self.trace, self.faults, self.rets, self.ends = [], [], [], []

    # memory
    def mb(self, a):
        a &= 0xFFFFFFFFFFFFFFFF
        if a in self.mem:
            return self.mem[a]
        if IMG_LO <= a < IMG_HI:
            try:
                return img_rd(self.raw, self.secs, a, 1)[0]
            except KeyError:
                return 0
        return 0

    def mw(self, a): return self.mb(a) | (self.mb(a + 1) << 8)
    def md(self, a):
        return self.mb(a) | (self.mb(a + 1) << 8) | \
            (self.mb(a + 2) << 16) | (self.mb(a + 3) << 24)
    def mq(self, a): return self.md(a) | (self.md(a + 4) << 32)
    def sb(self, a, v): self.mem[a & 0xFFFFFFFFFFFFFFFF] = v & 0xFF
    def sd(self, a, v):
        for i in range(4):
            self.sb(a + i, (v >> (8 * i)) & 0xFF)
    def mf(self, a):
        return u2f(self.md(a))
    def sf(self, a, v):
        self.sd(a, f2u(v))

    def mapped(self, a):
        return any(lo <= a < hi for lo, hi in VALID)

    # ---------- bodies ----------
    def sqrtf(self, u):
        r = sqrtf_bits(u)
        self.trace.append("sqrtf:%x:%x" % (u & 0xFFFFFFFF,
                                           r & 0xFFFFFFFF))
        return u2f(r)

    def xprod(self, dst, d, a):
        """00202E10 — dst = d x a (cross, w=0); stack temps first,
        so dst==src aliasing is safe."""
        dx, dy, dz = self.mf(d), self.mf(d + 4), self.mf(d + 8)
        ax, ay, az = self.mf(a), self.mf(a + 4), self.mf(a + 8)
        rx = f32(dy * az) - f32(dz * ay)
        ry = f32(dz * ax) - f32(dx * az)
        rz = f32(dx * ay) - f32(dy * ax)
        rx, ry, rz = f32(rx), f32(ry), f32(rz)
        self.sf(dst, rx)
        self.sf(dst + 4, ry)
        self.sf(dst + 8, rz)
        self.sf(dst + 0xC, 0.0)

    def b430(self, v, vsp):
        """0040B430 — two-stage normalize; returns the cookie^rsp
        residual rax. Native reads +4, +0, +8, then +0xC — the
        fault rip tracks the first unmapped read in that order."""
        for off, site in ((4, 0x40B461), (0, 0x40B46A),
                          (8, 0x40B472), (0xC, 0x40B4EF)):
            if not self.mapped(v + off):
                self.faults.append(("memr", v + off, 4))
                self.fault_end = site
                # rax already holds the cookie^rsp residual
                return GSCOOK ^ ((vsp - 0x98) & 0xFFFFFFFFFFFFFFFF)
        x, y, z = self.mf(v), self.mf(v + 4), self.mf(v + 8)
        eps = self.mf(EPSF)
        # stage 1: len = sqrtf(x^2+y^2+z^2); s = eps<=len ? 1/len : 0
        # (comiss unordered -> jbe -> 1/len)
        len2 = f32(f32(f32(x * x) + f32(y * y)) + f32(z * z))
        ln = self.sqrtf(f2u(len2))
        if math.isnan(ln) or eps <= ln:
            s = f32div(self.mf(SEEDF), ln)
        else:
            s = 0.0
        x, y, z = f32(x * s), f32(y * s), f32(z * s)
        self.sf(DIRA, x)
        self.sf(DIRA + 4, y)
        self.sf(DIRA + 8, z)
        # stage 2: local = {0, 1.0, c2, w}; dst = local x dir
        # (w flows into local.w; XPROD overwrites it — dead field)
        c2 = self.mf(C2F)
        lx, ly, lz = 0.0, self.mf(SEEDF), c2
        rx = f32(f32(ly * z) - f32(lz * y))
        ry = f32(f32(lz * x) - f32(lx * z))
        rz = f32(f32(lx * y) - f32(ly * x))
        len2b = f32(f32(f32(rx * rx) + f32(ry * ry)) + f32(rz * rz))
        ln2 = self.sqrtf(f2u(len2b))
        # comiss eps, ln2; ja -> s2 = 0; else s2 = 1/ln2
        # (unordered -> ja not taken -> 1/ln2)
        if not math.isnan(ln2) and eps > ln2:
            s2 = 0.0
        else:
            s2 = f32div(self.mf(SEEDF), ln2)
        self.sf(DIRB, f32(rx * s2))
        self.sf(DIRB + 4, f32(ry * s2))
        self.sf(DIRB + 8, f32(rz * s2))
        return GSCOOK ^ ((vsp - 0x98) & 0xFFFFFFFFFFFFFFFF)

    def db70(self, vsp):
        """0040DB70 — flag clear + vec {1.0,0,0,uninit} -> B430."""
        self.sb(FLAGB, 0)
        return self.b430_seed(vsp)

    def b430_seed(self, vsp):
        """DB70's nested B430 call on {1.0, 0, 0, 0}: the caller's
        frame places the callee vsp at vsp-0x40 (sub rsp,0x38 + call),
        so the cookie residual is GSCOOK ^ (vsp-0xD8)."""
        x, y, z, w = self.mf(SEEDF), 0.0, 0.0, 0.0
        eps = self.mf(EPSF)
        len2 = f32(f32(f32(x * x) + f32(y * y)) + f32(z * z))
        ln = self.sqrtf(f2u(len2))
        if math.isnan(ln) or eps <= ln:
            s = f32div(self.mf(SEEDF), ln)
        else:
            s = 0.0
        x, y, z = f32(x * s), f32(y * s), f32(z * s)
        self.sf(DIRA, x)
        self.sf(DIRA + 4, y)
        self.sf(DIRA + 8, z)
        c2 = self.mf(C2F)
        lx, ly, lz = 0.0, self.mf(SEEDF), c2
        rx = f32(f32(ly * z) - f32(lz * y))
        ry = f32(f32(lz * x) - f32(lx * z))
        rz = f32(f32(lx * y) - f32(ly * x))
        len2b = f32(f32(f32(rx * rx) + f32(ry * ry)) + f32(rz * rz))
        ln2 = self.sqrtf(f2u(len2b))
        if not math.isnan(ln2) and eps > ln2:
            s2 = 0.0
        else:
            s2 = f32div(self.mf(SEEDF), ln2)
        self.sf(DIRB, f32(rx * s2))
        self.sf(DIRB + 4, f32(ry * s2))
        self.sf(DIRB + 8, f32(rz * s2))
        return GSCOOK ^ ((vsp - 0xD8) & 0xFFFFFFFFFFFFFFFF)


def run_model(case, raw, secs):
    m = Model(case, raw, secs)
    for step in case.get("steps", []):
        entry, rcx = step[0], step[1]
        vsp = STACK + 0x80000
        if entry == DB70:
            m.rets.append(m.db70(vsp))
        elif entry == B430:
            m.rets.append(m.b430(rcx, vsp))
        elif entry == XPROD:
            rdx = step[2] if len(step) > 2 else 0
            r8 = step[3] if len(step) > 3 else 0
            m.xprod(rcx, rdx, r8)
            m.rets.append(0)
        m.ends.append(getattr(m, "fault_end", RETQ))
        m.fault_end = RETQ
    mem = {}
    for addr, n in case.get("watch", []):
        mem["%x" % addr] = bytes(
            m.mb(addr + i) for i in range(n)).hex()
    return {"trace": m.trace, "faults": m.faults, "rets": m.rets,
            "ends": m.ends, "mem": mem}


# ---------------- cases ----------------

W_GLB = [(FLAGB, 1), (DIRA, 0x10), (DIRB, 0x10)]
W_XP = [(VDST, 0x10), (VDS2, 0x10)]


def cases():
    C = {}
    C["db70-basic"] = {
        "flagb": 7,
        "steps": [(DB70, 0)],
        "watch": W_GLB}
    C["b430-basic"] = {
        "steps": [(B430, VEC)],
        "watch": W_GLB}
    C["b430-neg"] = {
        "vx": -2.0, "vy": -3.0, "vz": -6.0, "vw": 9.0,
        "steps": [(B430, VEC)],
        "watch": W_GLB}
    C["b430-eps-zero"] = {
        "vx": 0.0, "vy": 0.0, "vz": 0.0,
        "steps": [(B430, VEC)],
        "watch": W_GLB}
    C["b430-eps-under"] = {
        "vx": 1e-8, "vy": 0.0, "vz": 0.0,
        "steps": [(B430, VEC)],
        "watch": W_GLB}
    C["b430-eps-edge"] = {
        # len == eps exactly: comiss equal -> ZF=1 -> jbe -> s=1/len
        "vx": 9.999999974752427e-07, "vy": 0.0, "vz": 0.0,
        "steps": [(B430, VEC)],
        "watch": W_GLB}
    C["b430-inf"] = {
        # len2 overflows f32 to inf -> len=inf -> s=1/inf=0 -> zeros
        "vx": 1e38, "vy": 1e38, "vz": 1e38,
        "steps": [(B430, VEC)],
        "watch": W_GLB}
    C["b430-nan"] = {
        "vx": float("nan"), "vy": 1.0, "vz": 0.0,
        "steps": [(B430, VEC)],
        "watch": W_GLB}
    C["b430-w-dead"] = {
        # input w is copied into local.w then overwritten by XPROD:
        # two calls, different w, same output
        "vx": 1.0, "vy": 0.0, "vz": 0.0, "vw": 7.5,
        "steps": [(B430, VEC)],
        "watch": W_GLB}
    C["b430-two"] = {
        "steps": [(B430, VEC), (DB70, 0)],
        "watch": W_GLB}
    C["b430-badptr"] = {
        "steps": [(B430, 0xFFFFFFF0)],
        "watch": W_GLB}
    C["xprod-basic"] = {
        "steps": [(XPROD, VDST, VSRC, VA)],
        "watch": W_XP}
    C["xprod-neg"] = {
        "dx": -1.5, "dy": 2.5, "dz": -3.5,
        "ax": 4.0, "ay": -5.0, "az": 6.0,
        "steps": [(XPROD, VDST, VSRC, VA)],
        "watch": W_XP}
    C["xprod-alias"] = {
        # dst == src: native computes in stack temps first
        "steps": [(XPROD, VSRC, VSRC, VA)],
        "watch": [(VSRC, 0x10), (VDST, 0x10)]}
    C["xprod-two"] = {
        "steps": [(XPROD, VDST, VSRC, VA),
                  (XPROD, VDS2, VA, VSRC)],
        "watch": W_XP}
    return C


# ---------------- mutations (verified byte-precise) ----------------

MUTS = [
    # DB70 (sites byte-verified against shipped image)
    ("m-db70-flag",  "db70-basic",   0x40DB8D, 0x00, 0x01),  # flag imm 0->1
    ("m-db70-seed",  "db70-basic",   0x40DB78, 0x2C, 0x30),  # seed cell disp
    ("m-db70-lea",   "db70-basic",   0x40DB80, 0x20, 0x24),  # rcx slot +20->+24
    ("m-db70-qw",    "db70-basic",   0x40DB93, 0x00, 0x01),  # vec.yz imm 0->1
    # B430 stage-1
    ("m-b430-eps",   "b430-eps-under",0x40B49F, 0x6D, 0x69), # eps cell disp
    ("m-b430-jbe",   "b430-eps-edge", 0x40B4AD, 0x76, 0x77), # jbe->ja
    ("m-b430-div",   "b430-basic",   0x40B4BE, 0x5E, 0x59),  # divss->mulss
    ("m-b430-one",   "b430-basic",   0x40B4B8, 0xEC, 0xE8),  # 1.0 cell disp
    ("m-b430-mul7",  "b430-basic",   0x40B4C3, 0xF8, 0xF9),  # mulss xmm7,x0->x1
    ("m-b430-dira0", "b430-basic",   0x40B50C, 0x90, 0x94),  # DIRA+0 disp
    ("m-b430-dira4", "b430-basic",   0x40B515, 0x8B, 0x8F),  # DIRA+4 disp
    ("m-b430-dira8", "b430-neg",     0x40B51E, 0x86, 0x8A),  # DIRA+8 disp
    # local build
    ("m-b430-loc0",  "b430-basic",   0x40B4D7, 0x00, 0x3F),  # local.x 0->~0.5f
    ("m-b430-loc4",  "b430-basic",   0x40B4E8, 0x80, 0x00),  # local.y 1.0->0.5
    ("m-b430-loc8",  "b430-basic",   0x40B4FE, 0x9E, 0x9A),  # c2 cell disp
    ("m-b430-mul9",  "b430-neg",     0x40B4EE, 0xC8, 0xC9),  # mulss xmm9,x0->x1
    # XPROD call + stage-2
    ("m-b430-xcall", "b430-basic",   0x40B523, 0xE9, 0xED),  # 202e10 rel32
    ("m-b430-ja",    "b430-eps-zero",0x40B565, 0x77, 0x76),  # ja->jbe
    ("m-b430-div2",  "b430-basic",   0x40B571, 0x5E, 0x59),  # divss->mulss
    ("m-b430-one2",  "b430-basic",   0x40B56B, 0x39, 0x35),  # 1.0 cell disp2
    ("m-b430-dirb0", "b430-basic",   0x40B586, 0x26, 0x2A),  # DIRB+0 disp
    ("m-b430-dirb4", "b430-basic",   0x40B58E, 0x22, 0x26),  # DIRB+4 disp
    ("m-b430-dirb8", "b430-basic",   0x40B597, 0x1D, 0x21),  # DIRB+8 disp
    ("m-b430-xor",   "b430-basic",   0x40B45B, 0xC4, 0xC0),  # xor rax,rsp->rax,rax
    # XPROD
    ("m-xp-sub1",    "xprod-neg",    0x202E38, 0x5C, 0x58),  # subss->addss
    ("m-xp-a4",      "xprod-neg",    0x202E26, 0x04, 0x08),  # a.y -> a.z
    ("m-xp-a8",      "xprod-neg",    0x202E2C, 0x08, 0x04),  # a.z -> a.y
    ("m-xp-sub2",    "xprod-neg",    0x202E5C, 0x5C, 0x58),  # subss->addss
    ("m-xp-sub3",    "xprod-neg",    0x202E60, 0x5C, 0x58),  # subss->addss
    ("m-xp-slot8",   "xprod-basic",  0x202E70, 0x08, 0x0C),  # dst.z slot 8->0xC
    ("m-xp-slot4",   "xprod-basic",  0x202E76, 0x04, 0x08),  # dst.y slot 4->8
    ("m-xp-d4",      "xprod-neg",    0x202E55, 0x04, 0x08),  # d.y -> d.z
    ("m-xp-dst",     "xprod-basic",  0x202E7D, 0x01, 0x02),  # movups [rcx]->[rdx]
    # thunk
    ("m-thunk-disp", "b430-basic",   0x861F16, 0x9E, 0x9A),  # IAT cell disp
]


def run_native(case, raw, secs):
    w = World(case, raw, secs)
    w.run()
    return w.obs()


def differs(nv, mv):
    if nv.keys() != mv.keys():
        return True
    for k in nv:
        if k == "faults":
            na = sorted(str(t) for t in nv[k])
            ma = sorted(str(t) for t in mv[k])
            if na != ma:
                return True
        elif nv[k] != mv[k]:
            return True
    return False


def main():
    raw, secs = load_image()
    C = cases()
    fails = []
    results = {}
    for name, case in C.items():
        nat = run_native(case, raw, secs)
        mod = run_model(case, raw, secs)
        d = differs(nat, mod)
        results[name] = {"ok": not d,
                         "nat": nat, "mod": mod}
        if d:
            fails.append((name, nat, mod))
    print("functional: %d/%d" % (len(C) - len(fails), len(C)))
    for n, nat, mod in fails:
        print("  FAIL %s" % n)
        for k in ("trace", "rets", "ends", "faults", "mem"):
            if nat.get(k) != mod.get(k):
                print("    %s nat: %s" % (k, str(nat.get(k))[:200]))
                print("    %s mod: %s" % (k, str(mod.get(k))[:200]))

    mfails = []
    for mname, cname, va, exp, patch in MUTS:
        orig = img_rd(raw, secs, va, 1)[0]
        if orig != exp:
            mfails.append((mname, "site byte %02x != expected %02x"
                           % (orig, exp)))
            continue
        case = dict(C[cname])
        case["patch_bytes"] = [(va, bytes([patch]))]
        nat = run_native(case, raw, secs)
        if not differs(nat, run_model(case, raw, secs)):
            mfails.append((mname, "mutant survived"))
    print("mutants: %d/%d killed" % (len(MUTS) - len(mfails), len(MUTS)))
    for m, why in mfails:
        print("  LIVE %s %s" % (m, why))
    json.dump({"cases": results,
               "mutants": len(MUTS) - len(mfails),
               "mfails": [m for m, _ in mfails]},
              open(RESULT, "w"), indent=1)


if __name__ == "__main__":
    main()
