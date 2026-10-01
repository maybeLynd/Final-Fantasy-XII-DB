# EXP-130 transform-predicate-exec — native replay harness.
#
# Executes the transform-workbench predicate family real:
#
#   PRED  00335E50 305B — corridor-width probe. tmp = p1-p2
#         (VSUB), tmp.y flattened (movss [rsp+0x24],0),
#         normalize-or-zero in place + w=0 (NCOPY->NORM),
#         tmp = tmp x (0,1,0) (XPROD, const f[0x1F004B0]),
#         tmp *= xmm2 (VSCALE), then three nav queries:
#         Q(p1+off, p2+off) ==1 -> ret 1;
#         Q(p1-off, p2-off) ==1 -> ret 1;
#         Q(p2+off, p2-off) -> ret (eax==1).
#         GS cookie + real CHKCK.
#   VSUB  00203080 81B  — dst[i] = rdx[i]-r8[i] (all 4, stack temps).
#   VADD  00202B10 81B  — dst[i] = rdx[i]+r8[i] (all 4, stack temps).
#   VSCALE 00202FE0 67B — dst[i] = rdx[i]*xmm2 (all 4, stack temps).
#   NCOPY 00202DE0 33B  — movups [rdx]->[rcx]; call NORM; d[rcx+0xC]=0.
#   NORM  00216660 186B — normalize-or-zero in place. len2=x2+y2+z2;
#         cvtps2pd -> call q[0x86AC68] (nonzero -> zero path) ->
#         call q[0x86AC70] (zero -> zero path) ->
#         comiss len2, d[0x907698]=FLT_MIN (jbe -> zero path) ->
#         else v[i] *= 1.0f/sqrtf(len2) on x/y/z (w untouched).
#         Zero path 0x216701: q[v]=q[v+8]=0 (all 16B).
#   XPROD 00202E10 115B — dst = d x a (w=0), stack temps (EXP-129).
#   CHKCK 00808C40 — __security_check_cookie (real).
#   THUNK 00861F14 6B — jmp qword[IAT 0x8C2BB8] -> sqrtf import.
#
# Scripted boundaries (disclosed):
#   SQF  sqrtf import — real thunk + real IAT cell planted to the
#        SQF trampoline; host computes the same CRT sqrtf.
#   ISN/FIN — api-ms-win-crt-math-l1-1-0!_isnan / _finite via real
#        IAT cells q[0x8C2C68]/q[0x8C2C70] (ship unbound hint
#        records) planted to trampolines; host computes the same
#        predicates on the f64 len2 arg.
#   Q33  0033D3E0 nav-grid point query — deep tree (00384130 ->
#        00383F10 grid lookup w/ _fdclass IAT 0x8C2C10, 00383840
#        root q[0x5ADFB0], 0x382D10/0x32A780 walkers). Entry-
#        intercepted; eax planted per case. Follow-on package.
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
    UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_R9, \
    UC_X86_REG_RSP, UC_X86_REG_RIP, \
    UC_X86_REG_XMM0, UC_X86_REG_XMM2

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
ISN    = 0x63050000          # planted trampoline: isnan predicate
FIN    = 0x63060000          # planted trampoline: _finite predicate

PRED   = 0x00335E50
VSUB   = 0x00203080
VADD   = 0x00202B10
VSCALE = 0x00202FE0
NCOPY  = 0x00202DE0
NORM   = 0x00216660
XPROD  = 0x00202E10
Q33    = 0x0033D3E0          # scripted boundary (entry-intercept)
THUNKF = 0x00861F14          # real IAT thunk -> sqrtf
CHKCK  = 0x00808C40          # __security_check_cookie - real

SEEDF  = 0x1CEBBA8           # d: 1.0f (shared)
FLTM   = 0x907698            # d: FLT_MIN normalize gate (rdata)
CONSTV = 0x1F004B0           # f: (0,1,0,1) XZ axis
IATF   = 0x8C2BB8            # q: IAT slot for sqrtf
PC1    = 0x8C2C68            # q: IAT _isnan (ships hint 0x1CCECD8)
PC2    = 0x8C2C70            # q: IAT _finite (ships hint 0x1CCECCE)
COOK   = 0x1F44830           # q: __security_cookie (shipped)
GSCOOK = 0x2B992DDFA232      # shipped cookie value

# planted fixture addresses
P1     = HEAP + 0x10000      # PRED arg p1 (vec4)
P2     = HEAP + 0x11000      # PRED arg p2 (vec4)
VDST   = HEAP + 0x20000      # helper dst
VA     = HEAP + 0x20010      # helper src a (rdx)
VB     = HEAP + 0x20020      # helper src b (r8)
VD2    = HEAP + 0x20030      # second dst

# PRED frame locals at entry rsp = STACK+0x80000 (3 pushes + sub 0x80)
STMP   = STACK + 0x7FF88     # rsp+0x20  tmp vec
SC30   = STACK + 0x7FF98     # rsp+0x30  candidate A
SC40   = STACK + 0x7FFA8     # rsp+0x40  candidate B
SC50   = STACK + 0x7FFB8     # rsp+0x50  candidate C


def qw(v): return struct.pack("<Q", v & 0xFFFFFFFFFFFFFFFF)
def dw(v): return struct.pack("<I", v & 0xFFFFFFFF)
def ff(v): return struct.pack("<f", v)


# ---------------- f32 helpers ----------------

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
    if e >= -126 and n >> 24:
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
    if math.isnan(x) or x < 0:
        return float("nan")
    if _CRT is not None:
        return _CRT.sqrtf(x)
    return f32(math.sqrt(x))


def sqrtf_bits(u):
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
    W.append((IATF, qw(SQF)))
    W.append((PC1, qw(ISN)))
    W.append((PC2, qw(FIN)))
    # PRED input vec4s
    W.append((P1, ff(case.get("p1x", 2.0)) + ff(case.get("p1y", 0.5)) +
              ff(case.get("p1z", 6.0)) + ff(case.get("p1w", 1.0))))
    W.append((P2, ff(case.get("p2x", 5.0)) + ff(case.get("p2y", 1.5)) +
              ff(case.get("p2z", 2.0)) + ff(case.get("p2w", 9.0))))
    # helper args: a (rdx), b (r8)
    W.append((VA, ff(case.get("ax", 3.0)) + ff(case.get("ay", 4.0)) +
              ff(case.get("az", 5.0)) + ff(case.get("aw", 6.0))))
    W.append((VB, ff(case.get("bx", 1.0)) + ff(case.get("by", 2.0)) +
              ff(case.get("bz", 0.5)) + ff(case.get("bw", 7.0))))
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
        gm.map(ISN, 0x1000, b"\xc3" * 0x1000)
        gm.map(FIN, 0x1000, b"\xc3" * 0x1000)
        for addr, dat in build_fixture(case):
            gm.w(addr, dat)
        for addr, dat in case.get("patch_bytes", []):
            gm.w(addr, dat)
        self.trace, self.faults, self.rets, self.ends = [], [], [], []
        self.qrets = list(case.get("qrets", []))
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
            x = uc.reg_read(UC_X86_REG_XMM0)
            lo = x & 0xFFFFFFFF
            r = sqrtf_bits(lo)
            uc.reg_write(UC_X86_REG_XMM0, (x & ~0xFFFFFFFF) | r)
            self.trace.append("sqrtf:%x:%x" % (lo, r))
            self._ret(uc)
        elif addr == ISN:
            x = uc.reg_read(UC_X86_REG_XMM0)
            lo = x & 0xFFFFFFFFFFFFFFFF
            v = struct.unpack("<d", struct.pack("<Q", lo))[0]
            r = 1 if math.isnan(v) else 0
            uc.reg_write(UC_X86_REG_RAX, r)
            self.trace.append("isnan:%x:%d" % (lo, r))
            self._ret(uc)
        elif addr == FIN:
            x = uc.reg_read(UC_X86_REG_XMM0)
            lo = x & 0xFFFFFFFFFFFFFFFF
            v = struct.unpack("<d", struct.pack("<Q", lo))[0]
            r = 1 if math.isfinite(v) else 0
            uc.reg_write(UC_X86_REG_RAX, r)
            self.trace.append("finit:%x:%d" % (lo, r))
            self._ret(uc)
        elif addr == Q33:
            # disclosed scripted boundary: nav-grid point query.
            # eax planted per case; args recorded as vec contents.
            rcx = uc.reg_read(UC_X86_REG_RCX)
            rdx = uc.reg_read(UC_X86_REG_RDX)
            r8 = uc.reg_read(UC_X86_REG_R8)
            try:
                va = self.gm.r(rcx, 0x10).hex()
            except KeyError:
                va = "unmapped:%x" % rcx
            try:
                vb = self.gm.r(rdx, 0x10).hex()
            except KeyError:
                vb = "unmapped:%x" % rdx
            r = self.qrets.pop(0) if self.qrets else 0
            uc.reg_write(UC_X86_REG_RAX, r)
            self.trace.append("q33:%s:%s:%x:%d" % (va, vb,
                                                   r8 & 0xFFFFFFFF, r))
            self._ret(uc)

    def run_one(self, entry, rcx, rdx=0, r8=0, r9=0, xmm2=0):
        uc = self.uc
        self.gm.w(RETQ, b"\xc3" * 0x100)
        rsp = STACK + 0x80000
        self.gm.w(rsp, qw(RETQ))
        uc.reg_write(UC_X86_REG_RSP, rsp)
        uc.reg_write(UC_X86_REG_RCX, rcx)
        uc.reg_write(UC_X86_REG_RDX, rdx)
        uc.reg_write(UC_X86_REG_R8, r8)
        uc.reg_write(UC_X86_REG_R9, r9)
        uc.reg_write(UC_X86_REG_XMM2, xmm2)
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
            r9 = step[4] if len(step) > 4 else 0
            xmm2 = step[5] if len(step) > 5 else 0
            self.run_one(entry, rcx, rdx, r8, r9, xmm2)

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

VALID = ((HEAP, HEAP + 0x100000), (IMG_LO, IMG_HI),
         (STACK, STACK + 0x100000))


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
        self.qrets = list(case.get("qrets", []))
        self.fault_end = RETQ

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
    def sq(self, a, v):
        for i in range(8):
            self.sb(a + i, (v >> (8 * i)) & 0xFF)
    def mf(self, a):
        return u2f(self.md(a))
    def sf(self, a, v):
        self.sd(a, f2u(v))

    def mapped(self, a):
        return any(lo <= a < hi for lo, hi in VALID)

    # ---------- scripted boundaries ----------
    def sqrtf(self, u):
        r = sqrtf_bits(u)
        self.trace.append("sqrtf:%x:%x" % (u & 0xFFFFFFFF,
                                           r & 0xFFFFFFFF))
        return u2f(r)

    def isnan_f64(self, f):
        u = struct.unpack("<Q", struct.pack("<d", f))[0]
        r = 1 if math.isnan(f) else 0
        self.trace.append("isnan:%x:%d" % (u, r))
        return r

    def isfinite_f64(self, f):
        u = struct.unpack("<Q", struct.pack("<d", f))[0]
        r = 1 if math.isfinite(f) else 0
        self.trace.append("finit:%x:%d" % (u, r))
        return r

    def q33(self, a, b, flag):
        va = "".join("%02x" % self.mb(a + i) for i in range(0x10))
        vb = "".join("%02x" % self.mb(b + i) for i in range(0x10))
        r = self.qrets.pop(0) if self.qrets else 0
        self.trace.append("q33:%s:%s:%x:%d" % (va, vb,
                                               flag & 0xFFFFFFFF, r))
        return r

    # ---------- bodies ----------
    # per-component read sites (rdx, r8) relative to function base —
    # identical layout for 00203080 and 00202B10
    _RD2 = {0: (0x04, 0x08), 4: (0x0D, 0x12),
            8: (0x1D, 0x22), 0xC: (0x2E, 0x33)}

    def _addsub(self, dst, a, b, base, sub):
        for off in (0, 4, 8, 0xC):
            da, db = self._RD2[off]
            for src, site in ((a, base + da), (b, base + db)):
                if not self.mapped(src + off):
                    self.faults.append(("memr", src + off, 4))
                    self.fault_end = site
                    return
        for off in (0, 4, 8, 0xC):
            v = self.mf(a + off) - self.mf(b + off) if sub else \
                self.mf(a + off) + self.mf(b + off)
            self.sf(dst + off, f32(v))

    def vsub(self, dst, a, b):
        """00203080 — dst = a - b, all 4 (reads a0,b0,a4,b4,...)."""
        self._addsub(dst, a, b, 0x203080, True)

    def vadd(self, dst, a, b):
        """00202B10 — dst = a + b, all 4."""
        self._addsub(dst, a, b, 0x202B10, False)

    def vscale(self, dst, a, s):
        """00202FE0 — dst[i] = a[i] * s (xmm2), all 4."""
        for off, site in ((0, 0x202FEA), (4, 0x202FEE),
                          (8, 0x202FFB), (0xC, 0x203000)):
            if not self.mapped(a + off):
                self.faults.append(("memr", a + off, 4))
                self.fault_end = site
                return
        for off in (0, 4, 8, 0xC):
            self.sf(dst + off, f32(self.mf(a + off) * s))

    def norm(self, v):
        """00216660 — normalize-or-zero in place (xyz; w untouched
        on the scale path, all 16B zeroed on the zero path).
        Returns the residual rax: _finite's 1 on the scale path,
        xor'd 0 on every zero path."""
        x, y, z = self.mf(v), self.mf(v + 4), self.mf(v + 8)
        len2 = f32(f32(f32(x * x) + f32(y * y)) + f32(z * z))
        # cvtps2pd arg to both predicate cells
        if self.isnan_f64(len2):
            self.sq(v, 0)
            self.sq(v + 8, 0)
            return 0
        if not self.isfinite_f64(len2):
            self.sq(v, 0)
            self.sq(v + 8, 0)
            return 0
        eps = self.mf(FLTM)
        # comiss len2, FLT_MIN; jbe -> zero. unordered -> CF=ZF=1
        # -> jbe taken -> zero. (len2 is never NaN here.)
        if len2 <= eps:
            self.sq(v, 0)
            self.sq(v + 8, 0)
            return 0
        ln = self.sqrtf(f2u(len2))
        s = f32div(self.mf(SEEDF), ln)
        self.sf(v, f32(x * s))
        self.sf(v + 4, f32(y * s))
        self.sf(v + 8, f32(z * s))
        return 1                      # _finite residual stays in rax

    def ncopy(self, dst, src):
        """00202DE0 — movups copy + NORM + d[dst+0xC]=0; rax is
        NORM's residual."""
        for off, site in ((0, 0x202DE6),):
            if not self.mapped(src + off) or \
               not self.mapped(src + off + 0xF):
                a = src + off if not self.mapped(src + off) \
                    else src + off + 0xF
                self.faults.append(("memr", a, 4))
                self.fault_end = site
                return 0
        for i in range(0x10):
            self.sb(dst + i, self.mb(src + i))
        r = self.norm(dst)
        self.sd(dst + 0xC, 0)
        return r

    def xprod(self, dst, d, a):
        """00202E10 — dst = d x a (w=0), stack temps (alias-safe)."""
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

    def pred(self, p1, p2, scale, flag, vsp):
        """00335E50 — corridor-width probe; returns 0/1."""
        # tmp = p1 - p2; tmp.y flattened; normalize-or-zero; w=0
        resid = GSCOOK ^ ((vsp - 0x98) & 0xFFFFFFFFFFFFFFFF)
        if not self.mapped(p1) or not self.mapped(p2):
            a = p1 if not self.mapped(p1) else p2
            self.faults.append(("memr", a, 4))
            self.fault_end = 0x203084
            return resid
        self.vsub(STMP, p1, p2)
        if self.faults:
            return resid
        self.sf(STMP + 4, 0.0)           # movss [rsp+0x24], xmm0
        self.ncopy(STMP, STMP)           # normalize-or-zero + w=0
        self.xprod(STMP, STMP, CONSTV)   # tmp x (0,1,0)
        self.vscale(STMP, STMP, scale)   # tmp *= xmm2
        # probe 1: (p1+off, p2+off)
        self.vadd(SC30, p1, STMP)
        self.vadd(SC50, p2, STMP)
        if self.q33(SC30, SC50, flag) == 1:
            return 1
        # probe 2: (p1-off, p2-off)
        self.vsub(SC30, p1, STMP)
        self.vsub(SC40, p2, STMP)
        if self.q33(SC30, SC40, flag) == 1:
            return 1
        # probe 3: (p2+off, p2-off)
        return 1 if self.q33(SC50, SC40, flag) == 1 else 0


def run_model(case, raw, secs):
    m = Model(case, raw, secs)
    for step in case.get("steps", []):
        entry, rcx = step[0], step[1]
        rdx = step[2] if len(step) > 2 else 0
        r8 = step[3] if len(step) > 3 else 0
        r9 = step[4] if len(step) > 4 else 0
        xmm2 = step[5] if len(step) > 5 else 0
        scale = u2f(xmm2 & 0xFFFFFFFF)
        if entry == PRED:
            m.rets.append(m.pred(rcx, rdx, scale, r9,
                                 STACK + 0x80000))
        elif entry == VSUB:
            m.vsub(rcx, rdx, r8)
            m.rets.append(0)
        elif entry == VADD:
            m.vadd(rcx, rdx, r8)
            m.rets.append(0)
        elif entry == VSCALE:
            m.vscale(rcx, rdx, scale)
            m.rets.append(0)
        elif entry == NCOPY:
            m.rets.append(m.ncopy(rcx, rdx))
        elif entry == NORM:
            m.rets.append(m.norm(rcx))
        elif entry == XPROD:
            m.xprod(rcx, rdx, r8)
            m.rets.append(0)
        m.ends.append(m.fault_end)
        m.fault_end = RETQ
    mem = {}
    for addr, n in case.get("watch", []):
        mem["%x" % addr] = bytes(
            m.mb(addr + i) for i in range(n)).hex()
    return {"trace": m.trace, "faults": m.faults, "rets": m.rets,
            "ends": m.ends, "mem": mem}


# ---------------- cases ----------------

W_HLP = [(VDST, 0x10)]
W_SRC = [(VA, 0x10), (VB, 0x10)]
W_STK = [(STMP, 0x10), (SC30, 0x10), (SC40, 0x10), (SC50, 0x10)]
SC2   = f2u(2.0)             # scale=2.0f for PRED steps


def cases():
    C = {}
    # --- direct helper entries ---
    C["vsub-basic"] = {
        "steps": [(VSUB, VDST, VA, VB)],
        "watch": W_HLP + W_SRC}
    C["vsub-neg"] = {
        "ax": -1.5, "ay": 2.5, "az": -3.5, "aw": -4.5,
        "bx": 4.0, "by": -5.0, "bz": 6.0, "bw": 1.25,
        "steps": [(VSUB, VDST, VA, VB)],
        "watch": W_HLP + W_SRC}
    C["vsub-alias"] = {
        "steps": [(VSUB, VA, VA, VB)],
        "watch": W_SRC}
    C["vsub-badptr"] = {
        "steps": [(VSUB, VDST, 0xFFFFFFF0, VB)],
        "watch": W_HLP}
    C["vadd-basic"] = {
        "steps": [(VADD, VDST, VA, VB)],
        "watch": W_HLP + W_SRC}
    C["vadd-neg"] = {
        "ax": -1.5, "ay": 2.5, "az": -3.5, "aw": -4.5,
        "bx": 4.0, "by": -5.0, "bz": 6.0, "bw": 1.25,
        "steps": [(VADD, VDST, VA, VB)],
        "watch": W_HLP + W_SRC}
    C["vadd-alias"] = {
        "steps": [(VADD, VA, VA, VB)],
        "watch": W_SRC}
    C["vscale-basic"] = {
        "steps": [(VSCALE, VDST, VA, 0, 0, f2u(2.5))],
        "watch": W_HLP + W_SRC}
    C["vscale-neg"] = {
        "ax": -1.5, "ay": 2.5, "az": -3.5, "aw": -4.5,
        "steps": [(VSCALE, VDST, VA, 0, 0, f2u(-0.25))],
        "watch": W_HLP + W_SRC}
    C["vscale-zero"] = {
        "steps": [(VSCALE, VDST, VA, 0, 0, 0)],
        "watch": W_HLP}
    # --- NCOPY / NORM ---
    C["ncopy-basic"] = {
        "ax": 0.0, "ay": 0.0, "az": 4.0, "aw": 7.5,
        "steps": [(NCOPY, VDST, VA)],
        "watch": W_HLP + W_SRC}
    C["ncopy-neg"] = {
        "ax": -2.0, "ay": -3.0, "az": -6.0, "aw": 0.0,
        "steps": [(NCOPY, VDST, VA)],
        "watch": W_HLP}
    C["ncopy-zero"] = {
        "ax": 0.0, "ay": 0.0, "az": 0.0, "aw": 3.0,
        "steps": [(NCOPY, VDST, VA)],
        "watch": W_HLP}
    C["ncopy-den"] = {
        # len2 denormal (< FLT_MIN) -> zero path
        "ax": 1e-40, "ay": 0.0, "az": 0.0, "aw": 0.0,
        "steps": [(NCOPY, VDST, VA)],
        "watch": W_HLP}
    C["ncopy-inf"] = {
        # len2 overflows to +inf -> _finite=0 -> zero path
        "ax": 1e38, "ay": 1e38, "az": 1e38, "aw": 0.0,
        "steps": [(NCOPY, VDST, VA)],
        "watch": W_HLP}
    C["ncopy-nan"] = {
        "ax": float("nan"), "ay": 1.0, "az": 0.0, "aw": 0.0,
        "steps": [(NCOPY, VDST, VA)],
        "watch": W_HLP}
    C["norm-w"] = {
        # NORM direct: w is NOT touched on the scale path
        "ax": 1.0, "ay": 0.0, "az": 0.0, "aw": 7.5,
        "steps": [(NORM, VA)],
        "watch": W_SRC}
    C["norm-eps-edge"] = {
        # len2 == FLT_MIN exactly -> jbe -> zero
        "ax": 1.1754943508222875e-38, "ay": 0.0, "az": 0.0,
        "steps": [(NORM, VA)],
        "watch": W_SRC}
    C["norm-small"] = {
        # len2 = 2.5e-5: > FLT_MIN -> normalize (but < 6.1e-5,
        # which discriminates the eps-cell disp mutant)
        "ax": 0.005, "ay": 0.0, "az": 0.0, "aw": 0.0,
        "steps": [(NORM, VA)],
        "watch": W_SRC}
    C["norm-zerow"] = {
        # zero path with nonzero w: all 16B zeroed (incl w)
        "ax": 0.0, "ay": 0.0, "az": 0.0, "aw": 6.0,
        "steps": [(NORM, VA)],
        "watch": W_SRC}
    C["xprod-basic"] = {
        "steps": [(XPROD, VDST, VA, VB)],
        "watch": W_HLP}
    C["xprod-neg"] = {
        "ax": -1.5, "ay": 2.5, "az": -3.5, "aw": -4.5,
        "bx": 4.0, "by": -5.0, "bz": 6.0, "bw": 1.25,
        "steps": [(XPROD, VDST, VA, VB)],
        "watch": W_HLP}
    # --- PRED (scale=2.0, flag in r9d) ---
    C["pred-t1"] = {
        "qrets": [1],
        "steps": [(PRED, P1, P2, 0, 7, SC2)],
        "watch": W_STK}
    C["pred-t2"] = {
        "qrets": [0, 1],
        "steps": [(PRED, P1, P2, 0, 7, SC2)],
        "watch": W_STK}
    C["pred-t3"] = {
        "qrets": [0, 0, 1],
        "steps": [(PRED, P1, P2, 0, 7, SC2)],
        "watch": W_STK}
    C["pred-none"] = {
        "qrets": [0, 0, 0],
        "steps": [(PRED, P1, P2, 0, 7, SC2)],
        "watch": W_STK}
    C["pred-ret2"] = {
        # t3 returns 2 -> sete -> 0 (only ==1 counts)
        "qrets": [0, 0, 2],
        "steps": [(PRED, P1, P2, 0, 7, SC2)],
        "watch": W_STK}
    C["pred-eq"] = {
        # p1 == p2 -> tmp=0 -> norm zero path -> off=0:
        # all three probes see (p1, p2) unchanged
        "p2x": 2.0, "p2y": 0.5, "p2z": 6.0, "p2w": 1.0,
        "qrets": [0, 0, 1],
        "steps": [(PRED, P1, P2, 0, 3, SC2)],
        "watch": W_STK}
    C["pred-nan"] = {
        # NaN p1.z -> len2 NaN -> tmp=0 -> off=0
        "p1z": float("nan"),
        "qrets": [0, 0, 1],
        "steps": [(PRED, P1, P2, 0, 5, SC2)],
        "watch": W_STK}
    C["pred-scale0"] = {
        "qrets": [0, 0, 0],
        "steps": [(PRED, P1, P2, 0, 1, 0)],
        "watch": W_STK}
    C["pred-scale-neg"] = {
        "qrets": [0, 0, 0],
        "steps": [(PRED, P1, P2, 0, 2, f2u(-3.0))],
        "watch": W_STK}
    C["pred-degen-y"] = {
        # p1.y forced to 0 before normalize — a pure-Y delta
        # flattens to 0 -> tmp=0 -> off=0 (norm zero path)
        "p1x": 5.0, "p1y": 8.0, "p1z": 2.0,
        "p2x": 5.0, "p2y": 0.0, "p2z": 2.0,
        "qrets": [0, 0, 0],
        "steps": [(PRED, P1, P2, 0, 9, SC2)],
        "watch": W_STK}
    C["pred-y-same"] = {
        # delta.y is flattened: p1.y != p2.y yet tmp.y=0 anyway —
        # probes shift in XZ only
        "qrets": [0, 1],
        "steps": [(PRED, P1, P2, 0, 4, SC2)],
        "watch": W_STK}
    C["pred-badptr"] = {
        "steps": [(PRED, 0xFFFFFFF0, P2, 0, 0, SC2)],
        "watch": []}
    C["pred-two"] = {
        "qrets": [1, 0, 0, 1],
        "steps": [(PRED, P1, P2, 0, 7, SC2),
                  (PRED, P1, P2, 0, 7, SC2)],
        "watch": W_STK}
    return C


# ---------------- mutations (verified byte-precise) ----------------

MUTS = [
    # PRED 00335E50 (sites byte-verified against shipped image)
    ("m-pred-yflat", "pred-y-same",  0x335E9D, 0x24, 0x28),  # tmp.y=0 -> tmp.z=0
    ("m-pred-constv","pred-t3",      0x335EA6, 0x06, 0x08),  # axis lea disp +2
    ("m-pred-cmp1",  "pred-none",    0x335F03, 0x01, 0x00),  # cmp eax,1 -> ==0
    ("m-pred-je2",   "pred-t2",      0x335F46, 0x74, 0x75),  # je -> jne
    ("m-pred-sete",  "pred-ret2",    0x335F60, 0x94, 0x95),  # sete -> setne
    ("m-pred-xmm6",  "pred-t3",      0x335E85, 0xF2, 0xF0),  # xmm6,xmm2->xmm0
    ("m-pred-r8d",   "pred-t1",      0x335EF1, 0xC3, 0xC0),  # r8d=ebx -> eax
    ("m-pred-call0", "pred-t3",      0x335E87, 0xF5, 0xF9),  # vsub rel32 +4
    ("m-pred-call1", "pred-t3",      0x335EB5, 0x57, 0x5B),  # xprod rel32 +4
    ("m-pred-call2", "pred-t3",      0x335EC7, 0x15, 0x19),  # vscale rel32 +4
    ("m-pred-call3", "pred-t3",      0x335ED9, 0x33, 0x37),  # vadd rel32 +4
    ("m-pred-call4", "pred-t3",      0x335EFD, 0xDF, 0xE3),  # q33 rel32 +4
    ("m-pred-cook",  "pred-t3",      0x335E63, 0xC9, 0xD1),  # cookie cell disp
    # NORM 00216660
    ("m-norm-eps",   "norm-small",   0x2166B5, 0xDF, 0xE3),  # eps -> 6.1e-5
    ("m-norm-jbe",   "norm-eps-edge",0x2166B9, 0x76, 0x77),  # jbe -> ja
    ("m-norm-jne",   "ncopy-basic",  0x2166A3, 0x75, 0x74),  # isnan jne -> je
    ("m-norm-je",    "ncopy-basic",  0x2166B0, 0x74, 0x75),  # _finite je -> jne
    ("m-norm-div",   "ncopy-basic",  0x2166CD, 0x5E, 0x59),  # divss -> mulss
    ("m-norm-one",   "ncopy-basic",  0x2166C7, 0xDD, 0xE1),  # 1.0 cell -> 0.0
    ("m-norm-call1", "ncopy-basic",  0x21669D, 0xC7, 0xCF),  # cell1 -> FIN cell
    ("m-norm-call2", "ncopy-basic",  0x2166AA, 0xC2, 0xBA),  # cell2 -> ISN cell
    ("m-norm-mulx",  "ncopy-basic",  0x2166D7, 0x59, 0x58),  # mulss -> addss
    ("m-norm-muly",  "ncopy-basic",  0x2166E1, 0x04, 0x08),  # [rbx+4] -> +8
    ("m-norm-mulz",  "ncopy-basic",  0x2166EB, 0x08, 0x04),  # [rbx+8] -> +4
    ("m-norm-zero8", "norm-zerow",   0x216710, 0x08, 0x10),  # zero q[v+8] -> +0x10
    # NCOPY 00202DE0
    ("m-ncopy-wimm", "ncopy-basic",  0x202DF8, 0x00, 0x01),  # w imm 0 -> ~1e-45
    ("m-ncopy-cpy",  "ncopy-basic",  0x202DE8, 0x02, 0x12),  # movups xmm0->xmm2
    # VSCALE 00202FE0
    ("m-vscale-mul", "vscale-basic", 0x202FEC, 0x59, 0x58),  # mulss -> addss
    ("m-vscale-mv",  "vscale-basic", 0x202FE6, 0xC2, 0xC0),  # xmm0,xmm2->xmm0
    # VSUB 00203080 / VADD 00202B10
    ("m-vsub-op",    "vsub-basic",   0x20308B, 0x5C, 0x58),  # subss -> addss
    ("m-vsub-d4",    "vsub-basic",   0x203091, 0x04, 0x08),  # [rdx+4] -> +8
    ("m-vadd-op",    "vadd-basic",   0x202B1B, 0x58, 0x5C),  # addss -> subss
    ("m-vadd-d4",    "vadd-basic",   0x202B21, 0x04, 0x08),  # [rdx+4] -> +8
    # XPROD 00202E10 (sites proven in EXP-129)
    ("m-xp-sub1",    "xprod-neg",    0x202E38, 0x5C, 0x58),  # subss -> addss
    ("m-xp-slot8",   "xprod-basic",  0x202E70, 0x08, 0x0C),  # dst.z -> dst.w
    ("m-xp-dst",     "xprod-basic",  0x202E7D, 0x01, 0x02),  # movups [rcx]->[rdx]
]


def differs(a, b):
    out = []
    for k in ("trace", "rets", "ends", "faults"):
        if a[k] != b[k]:
            out.append(k)
    if a["mem"] != b["mem"]:
        out.append("mem")
    return out


def run_case(name, case, raw, secs):
    w = World(case, raw, secs)
    w.run()
    native = w.obs()
    model = run_model(case, raw, secs)
    return native, model, differs(native, model)


def main():
    raw, secs = load_image()
    cs = cases()
    fails = {}
    for name in sorted(cs):
        native, model, diff = run_case(name, cs[name], raw, secs)
        if diff:
            fails[name] = diff
    print("functional: %d/%d" % (len(cs) - len(fails), len(cs)))
    for name, diff in sorted(fails.items()):
        print("  FAIL %s: %s" % (name, diff))
    mkilled, msurv = [], []
    for mname, cname, addr, orig, mut in MUTS:
        base = dict(cs[cname])
        ob = img_rd(raw, secs, addr, 1)[0]
        assert ob == orig, \
            "%s: byte %x is %02x not %02x" % (mname, addr, ob, orig)
        base["patch_bytes"] = [(addr, bytes([mut]))]
        native, model, diff = run_case(mname, base, raw, secs)
        if diff:
            mkilled.append(mname)
        else:
            msurv.append(mname)
    print("mutants: %d/%d killed" % (len(mkilled), len(MUTS)))
    for mname in msurv:
        print("  SURVIVED %s" % mname)
    res = {"functional_total": len(cs),
           "functional_pass": len(cs) - len(fails),
           "functional_fail": sorted(fails),
           "mutants_total": len(MUTS),
           "mutants_killed": len(mkilled),
           "mutants_survived": msurv}
    with open(RESULT, "w") as f:
        json.dump(res, f, indent=2, sort_keys=True)
    sys.exit(1 if (fails or msurv) else 0)


if __name__ == "__main__":
    main()
