# EXP-132 nav-consumer-exec — native replay harness.
#
# Executes the nav-query consumer layer real over the EXP-130
# (PRED family) and EXP-131 (nav-grid query tree) bodies — the
# corridor-blocked stack end to end with only CRT imports and one
# subsystem call scripted:
#
#   PATHW 0033A3D0 405B — path-width probe: Q(B->A)!=1 -> ret 1;
#         then twice: MLOAD const mat -> AWRAP(angle) -> RBUILD rot
#         -> MXVW w = mat*(A-B)*scale + B; round passes iff
#         Q(B->w)==1 or Q(w->A)==1; else jmp 0033A40B dead tail
#         (add [rax],al x2 -> fault on small ints); ret 0.
#   BLKCHK 00335F90 161B — corridor-blocked check over an agent
#         record: sub=q[rcx+0x108]; xmm2=d[sub+0x10c]*d[0x8FCC8C];
#         mode=b[sub+0x174]; PRED(agent,agent+0x20,scale,mode)!=0
#         -> 1; QWALK(agent,agent+0x20,mode)==1 -> 1; mode==3 ->
#         AGENTQ 00318CA0 (scripted) !=0 -> 1; else 0.
#   MLOAD 00203170 44B — copies a shipped 4x4 const matrix
#         (0x8C5F80..0x8C5FD0) to [rcx].
#   AWRAP 0033CB70 128B — angle wrap to [-pi,pi]: >4pi / <-4pi ->
#         mod-2pi via divss/cvttss2si; else addss/subss 2pi loops.
#   RBUILD 00202F00 56B — copy 4x4 [rdx]->[rcx], cosf/sinf via real
#         IAT thunks 00861F08/00861F0E -> ROTCOL.
#   ROTCOL 00217880 234B — per-column (x,z) -> (x*cos + z*sin,
#         z*cos - x*sin) in place.
#   MXVW 00202B70 31B -> MXV 00217060 235B — dst = mat * v (row
#         dots, native add order).
#
# Re-executed real (previous packages): the whole EXP-131 tree
# (QWALK/WWRAP/GGRID/ROOTL/TTEST/ETHUNK/ECLASS/SEGT/BASE) and the
# EXP-130 tree (PRED 00335E50, VSUB 00203080, VADD 00202B10,
# VSCALE 00202FE0, NCOPY 00202DE0, NORM 00216660, XPROD 00202E10,
# THUNKF 00861F14, CHKCK 00808C40).
#
# Scripted boundaries (disclosed):
#   FDC  _fdclass  via real IAT q[0x8C2C10] (EXP-131).
#   SQF  sqrtf     via real thunk+IAT q[0x8C2BB8] (EXP-130).
#   ISN  _isnan    via real IAT q[0x8C2C68] (EXP-130).
#   FIN  _finite   via real IAT q[0x8C2C70] (EXP-130).
#   COS  cosf      via real thunk 00861F08 + IAT q[0x8C2BA8]
#        (import-dir proven).
#   SIN  sinf      via real thunk 00861F0E + IAT q[0x8C2BB0]
#        (import-dir proven).
#   AGENTQ 00318CA0 — subsystem-object query chain (002315E0 ->
#        0022F430 -> ...); entry-intercepted, eax planted per case.
#
# Fixture (planted, disclosed): EXP-131 synthetic 4-triangle nav
# mesh wholesale (q[0x2AEDFB0] root, q[0x1F83530] BASE pool,
# d[0x209A3E0] bit-pair table — all BSS), plus an agent record for
# BLKCHK and matrix/vec buffers for the helper steps. Shipped
# rdata read from the image: class table 0x915760, tri idx array
# 0xD112B0, const matrix 0x8C5F80.., angle/scale consts, cookie.
#
# Native and model must agree on trace/rets/faults/watched memory.
#
#   QWALK 0033D3E0 631B — segment walk over the nav tri adjacency
#         matrix. grid(p1)->cur, grid(p2)->dst (0xFF -> ret 0/1);
#         root = q[0x2AEDFB0]; per tri: matrix[base(d[+0x1C]) +
#         (D*cur + slot)*2] (D = w[root+0xA]) -> edge rec idx (0 ->
#         skip; slots == cur or prev skipped) -> edge rec
#         base(d[+0x14])+idx*8: b[+5] class -> 0026E300 bit test
#         (==1 pass; !=0 skip; ==0 -> flag gate b[+6] & 1<<r15d) ->
#         verts base(d[+0xC]) w[+0]/w[+2] -> {x,0,y,1} vec4s ->
#         00468880 seg-vs-edge orientation test; crossing advances
#         r12=cur, cur=slot; r13 budget 0x80; cur==dst -> ret 0;
#         slot exhaust -> ret 1. GS cookie + real CHKCK.
#   WWRAP 00384130 40B  — builds {v.x, v.z} pair, calls GGRID.
#   GGRID 00383F10 542B — grid point query. gh = base(d[root+0x20]);
#         _fdclass(x)/(y) ==2 (NaN) -> 0xFF; origin w[gh+4]/w[gh+6]
#         + span b[0]*b[2]/b[1]*b[3] bounds -> 0xFF;
#         cell = w[base(d[gh+8]) + (row*b[2]+col)*2] (0xFFFF->0xFF);
#         byte-list walk base(d[gh+0xC])+cell until 0xFF: per
#         candidate b, list rec base(d[root+0x18])+b*0x22, slots
#         w[rec+2] -> w[rec+0x14+s*2] -> idx array base(d[root+0x10])
#         +sel*8 -> TTEST; ==1 -> ret b. Exhaust -> 0xFF.
#   TTEST 00382D10 384B — point-in-triangle: shipped index array
#         d[0xD112B0]={0,1,2,0} gives edge pairs over w[idxarr+i*2]
#         vertex indices; verts = f32 pairs in base(d[root+0xC]);
#         same-sign 2D edge crosses (zero/NaN neutral) -> 1 else 0.
#   ECLASS 0032A780 5B + 0026E300 73B — thunk to bit-class query:
#         cl = d[0x915760 + sx16(dx)*4]; <0 -> -1; bit 1<<cl in
#         d[0x209A3E0 + ecx*8]: w0&w1 -> 2, w0 only -> 1, absent -> 0.
#   SEGT 00468880 496B — seg-seg orientation test built from real
#         VSUB 00203080 x6 + XPROD 00202E10 x4 + CHKCK: endpoint
#         straddle signs both ways -> 1 (intersect) else 0.
#   BASE 0020E600 9B   — rax = ecx + q[0x1F83530].
#   ROOTL 00383840 8B  — rax = q[0x2AEDFB0].
#
# Scripted boundaries (disclosed):
#   FDC  api-ms-win-crt-math-l1-1-0!_fdclass via real IAT cell
#        q[0x8C2C10] (import-directory proven; ships unbound hint)
#        planted to a trampoline; host computes the same CRT
#        predicate on the f32 in xmm0's low dword.
#
# Fixture (planted, disclosed): q[0x2AEDFB0] root, q[0x1F83530] BASE
# pool base and q[0x209A3E0+c*8] class bit pairs are all BSS (ship
# 0) — planted. The BASE pool holds a synthetic 4-triangle strip
# mesh (MODEL-PROVEN fixture data, not shipped nav data). Shipped
# rdata tables read from the image: class table d[0x915760],
# triangle index array d[0xD112B0], security cookie q[0x1F44830].
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
    UC_X86_REG_XMM0, UC_X86_REG_XMM1, UC_X86_REG_XMM2

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
ISN    = 0x63050000          # planted trampoline: _isnan import
FIN    = 0x63060000          # planted trampoline: _finite import
FDC    = 0x63070000          # planted trampoline: _fdclass import
COS    = 0x63080000          # planted trampoline: cosf import
SIN    = 0x63090000          # planted trampoline: sinf import

QWALK  = 0x0033D3E0          # segment walk over tri adjacency
WWRAP  = 0x00384130          # {x,z} pair wrapper -> GGRID
GGRID  = 0x00383F10          # grid point query -> tri id / 0xFF
TTEST  = 0x00382D10          # point-in-triangle test
ETHUNK = 0x0032A780          # jmp 0026E300
ECLASS = 0x0026E300          # edge-class bit query
SEGT   = 0x00468880          # seg-seg orientation test
BASE   = 0x0020E600          # rax = ecx + q[0x1F83530]
ROOTL  = 0x00383840          # rax = q[0x2AEDFB0]
VSUB   = 0x00203080          # vec4 sub (real)
XPROD  = 0x00202E10          # vec4 cross (real)
CHKCK  = 0x00808C40          # __security_check_cookie - real
# EXP-130 PRED tree (re-executed real)
PRED   = 0x00335E50          # corridor-width probe
VADD   = 0x00202B10          # vec4 add
VSCALE = 0x00202FE0          # vec4 * xmm2
NCOPY  = 0x00202DE0          # movups + NORM + w=0
NORM   = 0x00216660          # normalize-or-zero in place
THUNKF = 0x00861F14          # real IAT thunk -> sqrtf
# EXP-132 new bodies
PATHW  = 0x0033A3D0          # path-width probe (5x QWALK)
BLKCHK = 0x00335F90          # corridor-blocked check
MLOAD  = 0x00203170          # const 4x4 matrix load
AWRAP  = 0x0033CB70          # angle wrap to [-pi,pi]
RBUILD = 0x00202F00          # mat copy + cosf/sinf -> ROTCOL
ROTCOL = 0x00217880          # in-place column (x,z) rotate
MXVW   = 0x00202B70          # mat*vec wrapper
MXV    = 0x00217060          # mat*vec
TCOS   = 0x00861F08          # real IAT thunk -> cosf
TSIN   = 0x00861F0E          # real IAT thunk -> sinf
AGENTQ = 0x00318CA0          # scripted: subsystem-object query

ROOTCELL = 0x2AEDFB0          # q: nav root global (BSS, ships 0)
BASECELL = 0x1F83530         # q: BASE pool base (BSS, ships 0)
FDCIAT   = 0x8C2C10          # q: IAT _fdclass (ships hint record)
IATF     = 0x8C2BB8          # q: IAT sqrtf
PC1      = 0x8C2C68          # q: IAT _isnan (ships hint 0x1CCECD8)
PC2      = 0x8C2C70          # q: IAT _finite (ships hint 0x1CCECCE)
IATCOS   = 0x8C2BA8          # q: IAT cosf (import-dir proven)
IATSIN   = 0x8C2BB0          # q: IAT sinf (import-dir proven)
CLSTAB   = 0x915760          # d: r15 -> class bit index (rdata)
BPTAB    = 0x209A3E0         # d: edge class -> bit pair (BSS)
TRIIDX   = 0xD112B0          # d: shipped tri edge index array
COOK     = 0x1F44830         # q: __security_cookie (shipped)
GSCOOK   = 0x2B992DDFA232    # shipped cookie value
FLTM     = 0x907698          # d: NORM epsilon = FLT_MIN (shipped)
SEEDF    = 0x1CEBBA8         # d: NORM 1.0f seed (shipped)
CONSTV   = 0x1F004B0         # f: PRED axis const (0,1,0,1) shipped
MLOADC   = 0x8C5F80          # f: MLOAD const 4x4 matrix (16 floats)
AWHI     = 0xD10B0C          # d: AWRAP +4pi bound
AWLO     = 0xD10B20          # d: AWRAP -4pi bound
AWPI     = 0x1CEBC50         # d: AWRAP +pi
AWNPI    = 0x915620          # d: AWRAP -pi
AWNEG2   = 0x915624          # d: AWRAP -2pi step
AW2PI    = 0x1CEBC78         # d: AWRAP +2pi / mod period
PWSC     = 0x1CEBB70         # d: PATHW scale const = 0.5f
PWANG1   = 0x915614          # d: PATHW round-1 angle = +pi/4
PWANG2   = 0xD10B18          # d: PATHW round-2 angle = -pi/4
BKSC     = 0x8FCC8C          # d: BLKCHK radius scale 0.9f
                             #    (misaligned read inside a string)

# planted fixture addresses
BASEP  = HEAP + 0x30000      # BASE pool base -> BASE(i) = BASEP + i
ROOTA  = HEAP + 0x40000      # planted root struct
# BASE pool offsets
VPOOL  = 0x0000              # vertex pool: f32 (x,y) pairs
IDXA   = 0x0100              # idx arrays: 8B blocks (4 words)
EDGEP  = 0x0200              # edge records: 8B each
LISTR  = 0x0300              # list records: 0x22 stride
ADJM   = 0x0500              # tri adjacency matrix: words
GHDR   = 0x0600              # grid header
CMAP   = 0x0640              # cell map: words
BLIST  = 0x0680              # byte lists

P1     = HEAP + 0x10000      # walk arg p1 (vec4)
P2     = HEAP + 0x11000      # walk arg p2 (vec4)
PT     = HEAP + 0x12000      # point pair {x,y} for GGRID/TTEST
VECX   = HEAP + 0x13000      # extra vec4 (va)
VECY   = HEAP + 0x13010      # extra vec4 (vb)
IARR   = HEAP + 0x14000      # direct TTEST idx array (words)
AGENT  = HEAP + 0x15000      # BLKCHK agent record
SUBR   = HEAP + 0x16000      # BLKCHK sub-record q[agent+0x108]
MATB   = HEAP + 0x17000      # 4x4 matrix buffer (MLOAD/RBUILD/MXV)
VECQ   = HEAP + 0x18000      # vec4 arg buffer (MXV/MXVW)
DVB    = HEAP + 0x19000      # dst vec4 buffer

# QWALK frame: rsp = STACK+0x80000 - 4 pushes - sub 0x98 = +0x7FF48
# locals: +0x40 {x@+0,z@+8} sparse pair, +0x50/+0x60 edge vert vecs
WQ40   = STACK + 0x7FF88
WQ50   = STACK + 0x7FF98
WQ60   = STACK + 0x7FFA8
# nested WWRAP inside QWALK: call -> rsp 0x7FF40, sub 0x28 ->
# 0x7FF18; contiguous pair at rsp+0x30 = STACK+0x7FF48
WPAIR  = STACK + 0x7FF48
# SEGT direct frame: entry rsp 0x80000, push rbp -> rbp=rsp-0x57
# = 0x7FFA1; sub 0xD0 -> rsp 0x7FF28. vec locals rbp-0x59/-0x49/
# -0x29/-0x19 = +0x7FF48/58/78/88
SQVA   = STACK + 0x7FF48        # rbp-0x59: p1 vec
SQVB   = STACK + 0x7FF58        # rbp-0x49: va vec
SQVC   = STACK + 0x7FF78        # rbp-0x29: vb vec
SQVD   = STACK + 0x7FF88        # rbp-0x19: p2 vec


def qw(v): return struct.pack("<Q", v & 0xFFFFFFFFFFFFFFFF)
def dw(v): return struct.pack("<I", v & 0xFFFFFFFF)
def ww(v): return struct.pack("<H", v & 0xFFFF)
def bb(v): return struct.pack("<B", v & 0xFF)
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


_CRT = None
try:
    _CRT = ctypes.CDLL("api-ms-win-crt-math-l1-1-0.dll")
    _CRT._fdclass.restype = ctypes.c_int
    _CRT._fdclass.argtypes = (ctypes.c_float,)
    _CRT.sqrtf.restype = ctypes.c_float
    _CRT.sqrtf.argtypes = (ctypes.c_float,)
    _CRT.cosf.restype = ctypes.c_float
    _CRT.cosf.argtypes = (ctypes.c_float,)
    _CRT.sinf.restype = ctypes.c_float
    _CRT.sinf.argtypes = (ctypes.c_float,)
except OSError:
    pass


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
    """divss: correctly-rounded single-precision division."""
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


def sqrtf32(x):
    if math.isnan(x) or x < 0:
        return float("nan")
    if _CRT is not None:
        return _CRT.sqrtf(x)
    return f32(math.sqrt(x))


def sqrtf_bits(u):
    return f2u(sqrtf32(u2f(u)))


def cosf_bits(u):
    if _CRT is not None:
        return f2u(_CRT.cosf(u2f(u)))
    x = u2f(u)
    return f2u(float("nan") if math.isinf(x) or math.isnan(x)
               else f32(math.cos(x)))


def sinf_bits(u):
    if _CRT is not None:
        return f2u(_CRT.sinf(u2f(u)))
    x = u2f(u)
    return f2u(float("nan") if math.isinf(x) or math.isnan(x)
               else f32(math.sin(x)))


def fdclass_f32(u):
    """Host CRT _fdclass on the f32 bit pattern (as the callee sees
    xmm0's low dword). -1 normal, -2 denormal, 0 zero, 1 inf, 2 NaN."""
    if _CRT is not None:
        return _CRT._fdclass(u2f(u))
    x = u2f(u)
    if math.isnan(x):
        return 2
    if math.isinf(x):
        return 1
    if x == 0:
        return 0
    return -2 if abs(x) < 1.1754943508222875e-38 else -1


def _cvtt(f):
    """cvttss2si: invalid/overflow -> 0x80000000 (signed -2**31)."""
    if math.isnan(f) or math.isinf(f) or \
            f >= 2147483648.0 or f < -2147483649.0:
        return -0x80000000
    return int(f)


def _idiv(a, b):
    """signed idiv: truncates toward zero (// floors for negatives)."""
    q = abs(a) // abs(b)
    return -q if (a < 0) != (b < 0) else q


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


# ---------------- synthetic mesh ----------------
# 4-triangle strip over an 8x4 area, origin (0,0), 2x2 cells:
#   T0={v0,v1,v2}  T1={v1,v3,v2}  T2={v1,v4,v3}  T3={v4,v5,v3}
#   e0 = v1-v2 (T0|T1)   e1 = v1-v3 (T1|T2)   e2 = v4-v3 (T2|T3)
VERTS = [(0.0, 0.0), (4.0, 0.0), (0.0, 4.0), (4.0, 4.0),
         (8.0, 0.0), (8.0, 4.0)]
TRIS = [(0, 1, 2), (1, 3, 2), (1, 4, 3), (4, 5, 3)]
# edge ids in the matrix index recs directly (id*8): rec0 is unused,
# id 1/2/3 = shared edges e0/e1/e2
EDGES = [(0, 0), (1, 2), (1, 3), (4, 3)]
# adjacency[t][n] = shared edge record index (0 = none)
ADJ = [[0, 1, 0, 0],
       [1, 0, 2, 0],
       [0, 2, 0, 3],
       [0, 0, 3, 0]]
# cell map: idx = col + row*4 -> byte-list offset
LISTS = [[0], [0, 1], [2], [2], [0, 1], [1], [2, 3], [3]]
CELLS = [0x00, 0x02, 0x05, 0x07, 0x09, 0x0C, 0x0E, 0x11]


def mesh_bytes(case):
    """BASE pool image: verts, idx arrays, edge recs, list recs,
    adjacency, grid header, cell map, byte lists."""
    verts = case.get("verts", VERTS)
    tris = case.get("tris", TRIS)
    edges = case.get("edges", EDGES)
    adj = case.get("adj", ADJ)
    lists = case.get("lists", LISTS)
    cells = case.get("cells", CELLS)
    eclass = case.get("eclass", [0] * len(edges))   # b[+5] per edge
    eflag = case.get("eflag", [0] * len(edges))     # b[+6] per edge
    ghd = case.get("ghdr", {})                   # grid hdr overrides
    buf = bytearray(0x800)
    for i, (x, y) in enumerate(verts):
        buf[VPOOL + i * 8: VPOOL + i * 8 + 8] = ff(x) + ff(y)
    for i, t in enumerate(tris):
        buf[IDXA + i * 8: IDXA + i * 8 + 6] = \
            ww(t[0]) + ww(t[1]) + ww(t[2])
    for i, (a, b) in enumerate(edges):
        rec = ww(a) + ww(b) + bb(0) + bb(eclass[i]) + \
            bb(eflag[i]) + bb(0)
        buf[EDGEP + i * 8: EDGEP + i * 8 + 8] = rec
    for i in range(len(tris)):
        rec = bytearray(0x22)
        rec[2:4] = ww(1)                       # 1 idx-array slot
        rec[0x14:0x16] = ww(i)                 # selector i
        buf[LISTR + i * 0x22: LISTR + i * 0x22 + 0x22] = rec
    for t in range(len(adj)):
        for n in range(len(adj)):
            buf[ADJM + (t * len(adj) + n) * 2:
                ADJM + (t * len(adj) + n) * 2 + 2] = ww(adj[t][n])
    # grid header: cellW/H, cols/rows, origin, cellmap, bytelist
    buf[GHDR + 0] = ghd.get("cw", 2)
    buf[GHDR + 1] = ghd.get("ch", 2)
    buf[GHDR + 2] = ghd.get("cols", 4)
    buf[GHDR + 3] = ghd.get("rows", 2)
    buf[GHDR + 4:GHDR + 8] = ww(ghd.get("ox", 0)) + \
        ww(ghd.get("oy", 0))
    buf[GHDR + 8:GHDR + 0x10] = dw(CMAP) + dw(BLIST)
    for i, c in enumerate(cells):
        buf[CMAP + i * 2: CMAP + i * 2 + 2] = ww(c)
    # byte lists at their declared offsets
    for ci, off in enumerate(cells):
        if off >= 0x180:
            continue
        for k, t in enumerate(lists[ci]):
            buf[BLIST + off + k] = t
        buf[BLIST + off + len(lists[ci])] = 0xFF
    return bytes(buf)


def build_fixture(case):
    """bytes/plants shared by native World and python model."""
    W = []
    W.append((FDCIAT, qw(FDC)))
    W.append((IATF, qw(SQF)))
    W.append((PC1, qw(ISN)))
    W.append((PC2, qw(FIN)))
    W.append((IATCOS, qw(COS)))
    W.append((IATSIN, qw(SIN)))
    W.append((BASECELL, qw(case.get("basep", BASEP))))
    W.append((ROOTCELL, qw(case.get("rootp", ROOTA))))
    # root struct: tri count + BASE'd pool offsets
    root = bytearray(0x30)
    root[0xA:0xC] = ww(case.get("tricnt", len(case.get("tris", TRIS))))
    for off, pool in ((0xC, VPOOL), (0x10, IDXA), (0x14, EDGEP),
                      (0x18, LISTR), (0x1C, ADJM), (0x20, GHDR)):
        root[off:off + 4] = dw(case.get("root_%x" % off, pool))
    W.append((ROOTA, bytes(root)))
    W.append((BASEP, mesh_bytes(case)))
    # class bit-pair table (BSS): per-case overrides
    for ci, (w0, w1) in enumerate(case.get(
            "bptab", [(1 << 23, 0), (1 << 25, 1 << 25),
                      (0, 1 << 26), (0, 0)])):
        W.append((BPTAB + ci * 8, dw(w0) + dw(w1)))
    # walk args (vec4s; only x,z read)
    W.append((P1, ff(case.get("p1x", 1.0)) + ff(case.get("p1y", 0.0)) +
              ff(case.get("p1z", 1.0)) + ff(case.get("p1w", 1.0))))
    W.append((P2, ff(case.get("p2x", 3.0)) + ff(case.get("p2y", 0.0)) +
              ff(case.get("p2z", 3.0)) + ff(case.get("p2w", 1.0))))
    # point pair + extra vecs + direct idx array
    W.append((PT, ff(case.get("ptx", 1.0)) + ff(case.get("pty", 1.0))))
    W.append((VECX, ff(case.get("vax", 4.0)) + ff(0.0) +
              ff(case.get("vay", 0.0)) + ff(1.0)))
    W.append((VECY, ff(case.get("vbx", 0.0)) + ff(0.0) +
              ff(case.get("vby", 4.0)) + ff(1.0)))
    W.append((IARR, ww(case.get("i0", 0)) + ww(case.get("i1", 1)) +
              ww(case.get("i2", 2)) + ww(0)))
    # BLKCHK agent record: +0x00 vec4 pos1, +0x20 vec4 pos2,
    # +0x108 q -> SUBR; SUBR+0x10C d radius, +0x174 b mode
    ag = bytearray(0x120)
    ag[0x00:0x10] = ff(case.get("ag1x", case.get("p1x", 1.0))) + \
        ff(case.get("ag1y", 0.0)) + \
        ff(case.get("ag1z", case.get("p1z", 1.0))) + ff(1.0)
    ag[0x20:0x30] = ff(case.get("ag2x", case.get("p2x", 3.0))) + \
        ff(case.get("ag2y", 0.0)) + \
        ff(case.get("ag2z", case.get("p2z", 3.0))) + ff(1.0)
    ag[0x108:0x110] = qw(case.get("subp", SUBR))
    W.append((AGENT, bytes(ag)))
    sub = bytearray(0x180)
    sub[0x10C:0x110] = ff(case.get("radius", 0.0))
    sub[0x174] = case.get("mode", 0) & 0xFF
    W.append((SUBR, bytes(sub)))
    # matrix / vec buffers for helper-level steps
    mat = bytearray(0x40)
    for i in range(16):
        mat[i * 4:i * 4 + 4] = ff(case.get("m%d" % i,
                                           1.0 if i % 5 == 0 else 0.0))
    W.append((MATB, bytes(mat)))
    W.append((VECQ, ff(case.get("vx", 1.0)) + ff(case.get("vy", 2.0)) +
              ff(case.get("vz", 3.0)) + ff(case.get("vw", 4.0))))
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
        gm.map(FDC, 0x1000, b"\xc3" * 0x1000)
        for t in (SQF, ISN, FIN, COS, SIN):
            gm.map(t, 0x1000, b"\xc3" * 0x1000)
        for addr, dat in build_fixture(case):
            gm.w(addr, dat)
        for addr, dat in case.get("patch_bytes", []):
            gm.w(addr, dat)
        self.trace, self.faults, self.rets, self.ends = [], [], [], []
        self.agrets = list(case.get("agrets", [0]))
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
        if addr == FDC:
            x = uc.reg_read(UC_X86_REG_XMM0)
            lo = x & 0xFFFFFFFF
            r = fdclass_f32(lo)
            uc.reg_write(UC_X86_REG_RAX, r & 0xFFFFFFFFFFFFFFFF)
            self.trace.append("fdc:%x:%d" % (lo, r))
            self._ret(uc)
        elif addr == SQF:
            x = uc.reg_read(UC_X86_REG_XMM0)
            lo = x & 0xFFFFFFFF
            r = sqrtf_bits(lo)
            uc.reg_write(UC_X86_REG_XMM0,
                         (x & ~0xFFFFFFFF) | (r & 0xFFFFFFFF))
            self.trace.append("sqrtf:%x:%x" % (lo, r))
            self._ret(uc)
        elif addr == ISN or addr == FIN:
            f = struct.unpack("<d", struct.pack(
                "<Q", uc.reg_read(UC_X86_REG_XMM0) &
                0xFFFFFFFFFFFFFFFF))[0]
            r = 1 if (math.isnan(f) if addr == ISN
                      else math.isfinite(f)) else 0
            uc.reg_write(UC_X86_REG_RAX, r)
            self.trace.append(
                "%s:%x:%d" % ("isnan" if addr == ISN else "finit",
                              uc.reg_read(UC_X86_REG_XMM0) &
                              0xFFFFFFFFFFFFFFFF, r))
            self._ret(uc)
        elif addr == COS or addr == SIN:
            x = uc.reg_read(UC_X86_REG_XMM0)
            lo = x & 0xFFFFFFFF
            r = cosf_bits(lo) if addr == COS else sinf_bits(lo)
            uc.reg_write(UC_X86_REG_XMM0,
                         (x & ~0xFFFFFFFF) | (r & 0xFFFFFFFF))
            self.trace.append(
                "%s:%x:%x" % ("cosf" if addr == COS else "sinf",
                              lo, r))
            self._ret(uc)
        elif addr == AGENTQ:
            r = self.agrets.pop(0) if self.agrets else 0
            uc.reg_write(UC_X86_REG_RAX, r & 0xFFFFFFFFFFFFFFFF)
            self.trace.append(
                "agq:%x:%x:%x:%x:%x" % (
                    uc.reg_read(UC_X86_REG_RCX),
                    uc.reg_read(UC_X86_REG_RDX),
                    uc.reg_read(UC_X86_REG_R8),
                    uc.reg_read(UC_X86_REG_R9), r))
            self._ret(uc)

    def run_one(self, entry, rcx, rdx=0, r8=0, r9=0,
                xmm0=0, xmm2=0, xmm1=0):
        uc = self.uc
        self.gm.w(RETQ, b"\xc3" * 0x100)
        rsp = STACK + 0x80000
        self.gm.w(rsp, qw(RETQ))
        uc.reg_write(UC_X86_REG_RSP, rsp)
        uc.reg_write(UC_X86_REG_RCX, rcx)
        uc.reg_write(UC_X86_REG_RDX, rdx)
        uc.reg_write(UC_X86_REG_R8, r8)
        uc.reg_write(UC_X86_REG_R9, r9)
        uc.reg_write(UC_X86_REG_XMM0, xmm0 & 0xFFFFFFFFFFFFFFFF)
        uc.reg_write(UC_X86_REG_XMM2, xmm2 & 0xFFFFFFFFFFFFFFFF)
        uc.reg_write(UC_X86_REG_XMM1, xmm1 & 0xFFFFFFFFFFFFFFFF)
        try:
            uc.emu_start(entry, RETQ, count=300000)
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
            xmm0 = step[5] if len(step) > 5 else 0
            xmm2 = step[6] if len(step) > 6 else 0
            xmm1 = step[7] if len(step) > 7 else 0
            self.run_one(entry, rcx, rdx, r8, r9, xmm0, xmm2, xmm1)

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
        self.fault_end = RETQ
        self._rax = 0
        self.agrets = list(case.get("agrets", [0]))

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
    def sf(self, a, v):
        self.sd(a, f2u(v))
    def mf(self, a):
        return u2f(self.md(a))

    def mapped(self, a):
        return any(lo <= a < hi for lo, hi in VALID)

    def _rd(self, a, n, site):
        """ordered read: records ('memr', a, n) + fault_end on
        unmapped and returns None."""
        if not self.mapped(a):
            self.faults.append(("memr", a & 0xFFFFFFFFFFFFFFFF, n))
            self.fault_end = site
            return None
        if n == 1:
            return self.mb(a)
        if n == 2:
            return self.mw(a)
        if n == 4:
            return self.md(a)
        return self.mq(a)

    # ---------- scripted boundaries ----------
    def fdc(self, u):
        r = fdclass_f32(u)
        self.trace.append("fdc:%x:%d" % (u & 0xFFFFFFFF, r))
        return r

    def sqrtf(self, u):
        r = sqrtf_bits(u)
        self.trace.append("sqrtf:%x:%x" % (u & 0xFFFFFFFF,
                                           r & 0xFFFFFFFF))
        return u2f(r)

    def cosf(self, u):
        r = cosf_bits(u)
        self.trace.append("cosf:%x:%x" % (u & 0xFFFFFFFF,
                                          r & 0xFFFFFFFF))
        return u2f(r)

    def sinf(self, u):
        r = sinf_bits(u)
        self.trace.append("sinf:%x:%x" % (u & 0xFFFFFFFF,
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

    def agq(self, rcx, rdx, r8, r9):
        """00318CA0 entry-intercept — eax planted per case."""
        r = self.agrets.pop(0) if self.agrets else 0
        self.trace.append("agq:%x:%x:%x:%x:%x" % (
            rcx & 0xFFFFFFFFFFFFFFFF, rdx & 0xFFFFFFFFFFFFFFFF,
            r8 & 0xFFFFFFFFFFFFFFFF, r9 & 0xFFFFFFFFFFFFFFFF,
            r))
        return r

    # ---------- bodies ----------
    def base(self, i):
        """0020E600 — rax = ecx + q[0x1F83530]."""
        return (i + self.mq(BASECELL)) & 0xFFFFFFFFFFFFFFFF

    def eclass(self, cls, flag):
        """0026E300 — cl = classtab[sx16(flag)]; <0 -> -1;
        bit 1<<cl vs bitpair[class]: w0&w1 -> 2, w0 -> 1, else 0."""
        idx = flag & 0xFFFF
        if idx >= 0x8000:
            idx -= 0x10000
        cl = self.md(CLSTAB + idx * 4)
        if cl & 0x80000000:
            return 0xFFFFFFFF              # or eax,0xffffffff
        bit = (1 << (cl & 0x1F)) & 0xFFFFFFFF
        i32 = cls & 0xFFFFFFFF               # movsxd r8,ecx
        if i32 >= 0x80000000:
            i32 -= 0x100000000
        pair = (BPTAB + i32 * 8) & 0xFFFFFFFFFFFFFFFF
        if self.md(pair) & bit:
            return 2 if (self.md(pair + 4) & bit) else 1
        return 0

    def ttest(self, idxarr, pt):
        """00382D10 — point-in-triangle over shipped index array
        {0,1,2,0}; same-sign 2D edge crosses -> 1 else 0.
        Ordered reads: w[idxarr+ib*2] first (0x382D7A), then
        va.x/wa/vb.x/va.y/wa/vb.y/pt.x/wa/vb.x/[ucomiss]/wa/pt.y/vb.y."""
        ship = [self.md(TRIIDX + k * 4) for k in range(4)]
        root = self.mq(ROOTCELL)
        coff = self._rd(root + 0xC, 4, 0x382D6B)
        if coff is None:
            return self._rax
        vpool = self.base(coff)
        self._rax = vpool
        acc = 0.0
        for e in range(3):
            ia, ib = ship[e], ship[e + 1]
            wb = self._rd(idxarr + ib * 2, 2, 0x382D7A)
            if wb is None:
                return self._rax
            vax = self._rd(vpool + wb * 8, 4, 0x382D91)
            if vax is None:
                return self._rax
            wa = self._rd(idxarr + ia * 2, 2, 0x382D97)
            if wa is None:
                return self._rax
            vbx = self._rd(vpool + wa * 8, 4, 0x382D9C)
            if vbx is None:
                return self._rax
            ex = f32(u2f(vax) - u2f(vbx))
            vay = self._rd(vpool + wb * 8 + 4, 4, 0x382DCF)
            if vay is None:
                return self._rax
            if self._rd(idxarr + ia * 2, 2, 0x382DD5) is None:
                return self._rax
            vby = self._rd(vpool + wa * 8 + 4, 4, 0x382DDA)
            if vby is None:
                return self._rax
            ey = f32(u2f(vay) - u2f(vby))
            ptx = self._rd(pt, 4, 0x382DF2)
            if ptx is None:
                return self._rax
            if self._rd(idxarr + ia * 2, 2, 0x382DF7) is None:
                return self._rax
            vbx2 = self._rd(vpool + wa * 8, 4, 0x382DFC)
            if vbx2 is None:
                return self._rax
            px = f32(u2f(ptx) - u2f(vbx2))
            unordered = math.isnan(acc)
            if self._rd(idxarr + ia * 2, 2, 0x382E17) is None:
                return self._rax
            pty = self._rd(pt + 4, 4, 0x382E1C)
            if pty is None:
                return self._rax
            vby2 = self._rd(vpool + wa * 8 + 4, 4, 0x382E22)
            if vby2 is None:
                return self._rax
            py = f32(u2f(pty) - u2f(vby2))
            cross = f32(f32(py * ex) - f32(px * ey))
            # jp/jne from the ucomiss(acc,0) taken BEFORE cross:
            if unordered or acc != 0.0:
                prod = f32(cross * acc)
                # comiss 0,prod; ja -> ret0. unordered -> pass
                if not math.isnan(prod) and 0.0 > prod:
                    return 0
            else:
                acc = cross
        return 1

    def ggrid(self, pt):
        """00383F10 — grid point query -> tri id / 0xFF."""
        root = self.mq(ROOTCELL)
        self._rax = root
        if self._rd(root + 0x20, 4, 0x383F23) is None:
            return self._rax
        gh = self.base(self.md(root + 0x20))
        self._rax = gh
        if self._rd(gh + 0xC, 4, 0x383F2E) is None:
            return self._rax
        bl = self.base(self.md(gh + 0xC))
        self._rax = bl
        x = self._rd(pt, 4, 0x383F36)
        if x is None:
            return self._rax
        if self.fdc(x) == 2:
            return 0xFF
        y = self._rd(pt + 4, 4, 0x383F4E)
        if y is None:
            return self._rax
        if self.fdc(y) == 2:
            return 0xFF
        xf, yf = u2f(x), u2f(y)
        ox = self.mw(gh + 4)
        if ox >= 0x8000:
            ox -= 0x10000
        # comiss (float)ox, x; ja -> 0xFF  (unordered: ja not taken)
        if not math.isnan(xf) and float(ox) > xf:
            return 0xFF
        oy = self.mw(gh + 6)
        if oy >= 0x8000:
            oy -= 0x10000
        if not math.isnan(yf) and float(oy) > yf:
            return 0xFF
        bx = ox + self.mb(gh + 2) * self.mb(gh)
        if not math.isnan(xf) and xf > float(bx):
            return 0xFF
        by = oy + self.mb(gh + 3) * self.mb(gh + 1)
        if not math.isnan(yf) and yf > float(by):
            return 0xFF
        cmap = self.base(self.md(gh + 8))
        row = _idiv(_cvtt(f32(yf - oy)), self.mb(gh + 1))
        col = _idiv(_cvtt(f32(xf - ox)), self.mb(gh))
        idx = row * self.mb(gh + 2) + col
        self._rax = idx & 0xFFFFFFFFFFFFFFFF   # cdqe leaves idx in rax
        cell = self._rd((cmap + idx * 2) & 0xFFFFFFFFFFFFFFFF, 2,
                        0x38402C)
        if cell is None:
            return self._rax
        if cell == 0xFFFF:
            return 0xFF
        li = bl + cell
        while True:
            b = self._rd(li, 1, 0x38404F)
            if b is None:
                return self._rax
            if b == 0xFF:
                return 0xFF
            rec = self.base(self.md(root + 0x18)) + b * 0x22
            n = self.mw(rec + 2)
            for s in range(n):
                sel = self.mw(rec + 0x14 + s * 2)
                iarr = self.base(self.md(root + 0x10)) + sel * 8
                if self.ttest(iarr, pt) == 1:
                    return b
            li += 1

    def wwrap(self, vec, pdst):
        """00384130 — builds contiguous {v.x, v.z} pair at pdst,
        calls GGRID on it."""
        x = self._rd(vec, 4, 0x384134)
        if x is None:
            return self._rax
        self.sd(pdst, x)
        z = self._rd(vec + 8, 4, 0x384138)
        if z is None:
            return self._rax
        self.sd(pdst + 4, z)
        return self.ggrid(pdst)

    def segt(self, p1, p2, va, vb, vsp):
        """00468880 — seg-seg orientation test; real VSUB/XPROD.
        Entry rsp = vsp; rbp = vsp-0x5F; frame rsp = vsp-0xD8;
        cookie residual = GSCOOK ^ (vsp-0xD8)."""
        resid = GSCOOK ^ ((vsp - 0xD8) & 0xFFFFFFFFFFFFFFFF)
        rbp = vsp - 0x5F
        A, B, C, D = rbp - 0x59, rbp - 0x19, rbp - 0x49, rbp - 0x29
        # local vec4s {x,0,z,1}; native read order: p1.x, p2.x,
        # p1.z, p2.z, va.z, va.x, vb.z, vb.x
        for src, off, site in (
                (p1, 0, 0x4688A4), (p2, 0, 0x4688AB),
                (p1, 8, 0x4688B4), (p2, 8, 0x4688C2),
                (va, 8, 0x4688D0), (va, 0, 0x4688DB),
                (vb, 8, 0x4688E9), (vb, 0, 0x4688F4)):
            v = self._rd(src + off, 4, site)
            if v is None:
                return resid
        self.sf(A, self.mf(p1))
        self.sf(A + 4, 0.0)
        self.sf(A + 8, self.mf(p1 + 8))
        self.sf(A + 0xC, 1.0)
        self.sf(B, self.mf(p2))
        self.sf(B + 4, 0.0)
        self.sf(B + 8, self.mf(p2 + 8))
        self.sf(B + 0xC, 1.0)
        self.sf(C, self.mf(va))
        self.sf(C + 4, 0.0)
        self.sf(C + 8, self.mf(va + 8))
        self.sf(C + 0xC, 1.0)
        self.sf(D, self.mf(vb))
        self.sf(D + 4, 0.0)
        self.sf(D + 8, self.mf(vb + 8))
        self.sf(D + 0xC, 1.0)

        def vsub4(dst, a, b):
            for o in (0, 4, 8, 0xC):
                self.sf(dst + o, f32(self.mf(a + o) - self.mf(b + o)))

        def xprod(dst, d, a):
            dx, dy, dz = self.mf(d), self.mf(d + 4), self.mf(d + 8)
            ax, ay, az = self.mf(a), self.mf(a + 4), self.mf(a + 8)
            self.sf(dst, f32(f32(dy * az) - f32(dz * ay)))
            self.sf(dst + 4, f32(f32(dz * ax) - f32(dx * az)))
            self.sf(dst + 8, f32(f32(dx * ay) - f32(dy * ax)))
            self.sf(dst + 0xC, 0.0)

        def le(a, b):
            """comiss a,b; jbe — unordered counts as taken."""
            return math.isnan(a) or math.isnan(b) or a <= b

        def gt(a, b):
            """comiss a,b; ja — unordered never taken."""
            return not (math.isnan(a) or math.isnan(b)) and a > b

        # stage 1: va/vb endpoints vs segment line (p1->p2)
        E, F, G, H, I = rbp - 0x39, rbp - 9, rbp + 7, \
            rbp + 0x27, rbp + 0x17
        vsub4(E, B, A)
        vsub4(F, C, A)
        vsub4(G, D, A)
        xprod(H, F, E)
        xprod(I, G, E)
        h1, i1 = self.mf(H + 4), self.mf(I + 4)
        if gt(h1, 0.0) and gt(i1, 0.0):
            return 0
        if gt(0.0, h1) and gt(0.0, i1):
            return 0
        # stage 2: p1/p2 endpoints vs edge line (va->vb)
        E2, F2, G2 = rbp - 0x39, rbp - 9, rbp + 7
        vsub4(E2, D, C)
        vsub4(F2, A, C)
        vsub4(G2, B, C)
        xprod(H, F2, E2)
        xprod(I, G2, E2)
        h2, i2 = self.mf(H + 4), self.mf(I + 4)
        if gt(h2, 0.0) and gt(i2, 0.0):
            return 0
        if gt(0.0, h2) and gt(0.0, i2):
            return 0
        return 1

    def qwalk(self, p1, p2, flag, vsp):
        """0033D3E0 — segment walk over the tri adjacency matrix.
        Frame: rsp = vsp - 0xB8 (4 pushes + sub 0x98)."""
        resid = GSCOOK ^ ((vsp - 0xB8) & 0xFFFFFFFFFFFFFFFF)
        L40 = vsp - 0xB8 + 0x40          # {x,z} pair local
        L50 = vsp - 0xB8 + 0x50          # edge vert vec A
        L60 = vsp - 0xB8 + 0x60          # edge vert vec B
        x = self._rd(p1, 4, 0x33D3FE)
        if x is None:
            return resid
        self.sd(L40, x)
        z = self._rd(p1 + 8, 4, 0x33D405)
        if z is None:
            return resid
        self.sd(L40 + 8, z)
        cur = self.wwrap(L40, vsp - 0xB8)
        if self.faults:
            return self._rax
        if cur == 0xFF:
            return 0
        x = self._rd(p2, 4, 0x33D442)
        if x is None:
            return cur          # rax still holds ggrid result
        self.sd(L40, x)
        z = self._rd(p2 + 8, 4, 0x33D44B)
        if z is None:
            return cur
        self.sd(L40 + 8, z)
        dst = self.wwrap(L40, vsp - 0xB8)
        if self.faults:
            return self._rax
        if dst == 0xFF:
            return 1
        root = self.mq(ROOTCELL)
        prev, budget = 0xFF, 0
        while True:
            if cur == dst:
                return 0
            deg = self.mw(root + 0xA)
            slot = 0
            while slot < deg:
                if slot == cur or slot == prev:
                    slot += 1
                    continue
                e = self.mw(self.base(self.md(root + 0x1C)) +
                            (deg * cur + slot) * 2)
                if e == 0:
                    slot += 1
                    continue
                ep = self.base(self.md(root + 0x14)) + e * 8
                c = self.eclass(self.mb(ep + 5), flag)
                ok = c == 1 or (c == 0 and
                                (self.mb(ep + 6) &
                                 (1 << (flag & 0x1F))) != 0)
                if ok:
                    vp = self.base(self.md(root + 0xC))
                    v0 = self.mw(ep)
                    v1 = self.mw(ep + 2)
                    self.sf(L50, self.mf(vp + v0 * 8))
                    self.sf(L50 + 4, 0.0)
                    self.sf(L50 + 8, self.mf(vp + v0 * 8 + 4))
                    self.sf(L50 + 0xC, 1.0)
                    self.sf(L60, self.mf(vp + v1 * 8))
                    self.sf(L60 + 4, 0.0)
                    self.sf(L60 + 8, self.mf(vp + v1 * 8 + 4))
                    self.sf(L60 + 0xC, 1.0)
                    if self.segt(p1, p2, L50, L60,
                                 vsp - 0xB8 - 8) != 0:
                        prev, cur = cur, slot
                        break
                slot += 1
            else:
                if slot == deg:
                    return 1
            budget += 1
            if budget >= 0x80:
                return 0

    # ---------- EXP-130 vec/predicate bodies (re-executed) ----
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
        if self.isnan_f64(len2):
            self.sq(v, 0)
            self.sq(v + 8, 0)
            return 0
        if not self.isfinite_f64(len2):
            self.sq(v, 0)
            self.sq(v + 8, 0)
            return 0
        eps = self.mf(FLTM)
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
        """00335E50 — corridor-width probe; the three nav probes
        run the REAL QWALK tree (EXP-130's scripted boundary closed).
        Frame: rsp = vsp - 0x98; nested QWALK entry rsp = vsp - 0xA0."""
        resid = GSCOOK ^ ((vsp - 0x98) & 0xFFFFFFFFFFFFFFFF)
        STMP = vsp - 0x78                # rsp+0x20 flattened tmp
        SC30 = vsp - 0x68                # rsp+0x30 candidate A
        SC40 = vsp - 0x58                # rsp+0x40 candidate B
        SC50 = vsp - 0x48                # rsp+0x50 candidate C
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
        r = self.qwalk(SC30, SC50, flag, vsp - 0xA0)
        if self.faults:
            return r
        self._rax = r
        if r == 1:
            return 1
        # probe 2: (p1-off, p2-off)
        self.vsub(SC30, p1, STMP)
        self.vsub(SC40, p2, STMP)
        r = self.qwalk(SC30, SC40, flag, vsp - 0xA0)
        if self.faults:
            return r
        self._rax = r
        if r == 1:
            return 1
        # probe 3: (p2+off, p2-off)
        r = self.qwalk(SC50, SC40, flag, vsp - 0xA0)
        if self.faults:
            return r
        self._rax = r
        return 1 if r == 1 else 0

    # ---------- EXP-132 new bodies ----------
    def mload(self, dst):
        """00203170 — 4x movups copy of the shipped const 4x4 to
        [dst]. Sources 0x8C5F80/90/B0/D0 select {+X,+Y,+Z,W} from
        the shared signed axis-basis bank 0x8C5F80..0x8C5FE0
        (-Y at 0x8C5FA0 and -Z at 0x8C5FC0 are skipped)."""
        for i, cell in enumerate((0x8C5F80, 0x8C5F90,
                                  0x8C5FB0, 0x8C5FD0)):
            for k in range(16):
                self.sb(dst + i * 16 + k, self.mb(cell + k))

    def awrap(self, x):
        """0033CB70 — angle wrap to [-pi,pi]. |x|>4pi -> mod-2pi via
        divss/cvttss2si/cvtdq2ps/mulss/subss (NO [-pi,pi] wrap after);
        else subss -2pi / addss +2pi loops."""
        hi = self.mf(AWHI)               # +4pi
        lo = self.mf(AWLO)               # -4pi
        if (not math.isnan(x) and x > hi) or \
           (not math.isnan(x) and lo > x):
            per = self.mf(AW2PI)         # 2pi
            n = _cvtt(f32(x / per))
            self._rax = n & 0xFFFFFFFF   # cvttss2si eax (zero-extends)
            x = f32(x - f32(f32(n) * per))
            return x
        pi = self.mf(AWPI)               # +pi
        while not math.isnan(x) and x > pi:
            x = f32(x + self.mf(AWNEG2))  # addss -2pi
        npi = self.mf(AWNPI)             # -pi
        while not math.isnan(x) and npi > x:
            x = f32(x + self.mf(AW2PI))   # addss +2pi
        return x

    def rotcol(self, mat, s, c):
        """00217880 — per-column (x,z) -> (x*c + z*s, z*c - x*s)
        in place; columns at +0,+0x10,+0x20,+0x30."""
        self._rax = mat                 # mov rax,rcx at 0x217888
        for k in range(4):
            b = mat + k * 16
            x = self.mf(b)
            z = self.mf(b + 8)
            self.sf(b, f32(f32(z * s) + f32(x * c)))
            self.sf(b + 8, f32(f32(z * c) - f32(x * s)))

    def rbuild(self, dst, src, ang):
        """00202F00 — 4x movups [src]->[dst], cosf(ang)->xmm6,
        sinf(ang)->xmm1 via real IAT thunks, tail ROTCOL."""
        for i in range(4):
            for k in range(16):
                self.sb(dst + i * 16 + k, self.mb(src + i * 16 + k))
        co = self.cosf(f2u(ang))
        si = self.sinf(f2u(ang))
        self.rotcol(dst, si, co)
        self._rax = dst

    def mxv(self, dst, mat, v):
        """00217060 — dst = mat * v. v read order x,z,w,y
        (0x217064/06C/086/090); per component o: dst[o] =
        w*m[o+0x30] + ((y*m[o+0x10] + x*m[o]) + z*m[o+0x20]),
        each op f32-rounded in native add order."""
        vx = self._rd(v, 4, 0x217064)
        if vx is None:
            return
        self._rax = dst                 # mov rax,rcx at 0x217069
        vz = self._rd(v + 8, 4, 0x21706C)
        if vz is None:
            return
        vw = self._rd(v + 0xC, 4, 0x217086)
        if vw is None:
            return
        vy = self._rd(v + 4, 4, 0x217090)
        if vy is None:
            return
        x, y, z, w = u2f(vx), u2f(vy), u2f(vz), u2f(vw)
        for o in (0, 4, 8, 0xC):
            r = f32(f32(w * self.mf(mat + o + 0x30)) +
                    f32(f32(f32(y * self.mf(mat + o + 0x10)) +
                            f32(x * self.mf(mat + o))) +
                        f32(z * self.mf(mat + o + 0x20))))
            self.sf(dst + o, r)

    def mxvw(self, dst, mat, v, vsp):
        """00202B70 — MXV into a frame temp, movups copy to dst.
        Frame: rsp = vsp - 0x38; temp at rsp+0x20 = vsp - 0x18.
        rax = temp on exit (MXV's rcx residual survives the copy)."""
        t = vsp - 0x18
        self.mxv(t, mat, v)
        self._rax = t
        for i in range(0x10):
            self.sb(dst + i, self.mb(t + i))

    def pathw(self, a, b, vsp):
        """0033A3D0 — path-width probe. Frame rsp = vsp - 0x98:
        w@+0x20=vsp-0x78, v@+0x30=vsp-0x68, mat@+0x40=vsp-0x58;
        nested QWALK entry rsp = vsp - 0xA0."""
        resid = GSCOOK ^ ((vsp - 0x98) & 0xFFFFFFFFFFFFFFFF)
        W = vsp - 0x78
        V = vsp - 0x68
        MAT = vsp - 0x58
        r = self.qwalk(b, a, 1, vsp - 0xA0)
        if self.faults:
            return r
        self._rax = r
        if r != 1:
            return 1
        self.vsub(V, a, b)               # v = A - B
        if self.faults:
            return resid
        self.vscale(V, V, self.mf(PWSC))
        for ang in (PWANG1, PWANG2):
            self.mload(MAT)
            self.rbuild(MAT, MAT, self.awrap(self.mf(ang)))
            self.mxvw(W, MAT, V, vsp - 0xA0)
            if self.faults:
                return self._rax
            self.vadd(W, W, b)           # w += B
            r1 = self.qwalk(b, W, 1, vsp - 0xA0)
            if self.faults:
                return r1
            self._rax = r1
            ok = r1 == 1
            if not ok:
                r2 = self.qwalk(W, a, 1, vsp - 0xA0)
                if self.faults:
                    return r2
                self._rax = r2
                ok = r2 == 1
            if not ok:
                return 1
        return 0

    def blkchk(self, agent, vsp):
        """00335F90 — corridor-blocked check. Frame rsp = vsp-0x28;
        nested PRED/QWALK entry rsp = vsp - 0x30."""
        sub = self._rd(agent + 0x108, 8, 0x335F9F)
        if sub is None:
            return self._rax
        self._rax = sub
        rad = self._rd(sub + 0x10C, 4, 0x335FAD)
        if rad is None:
            return self._rax
        mode = self._rd(sub + 0x174, 1, 0x335FB5)
        if mode is None:
            return self._rax
        scale = f32(u2f(rad) * self.mf(BKSC))
        r = self.pred(agent, agent + 0x20, scale, mode, vsp - 0x30)
        if self.faults:
            return r
        self._rax = r
        if r != 0:
            return 1
        r = self.qwalk(agent, agent + 0x20, mode, vsp - 0x30)
        if self.faults:
            return r
        self._rax = r
        if r == 1:
            return 1
        sub = self._rd(agent + 0x108, 8, 0x335FE4)
        if sub is None:
            return self._rax
        self._rax = sub
        mode = self._rd(sub + 0x174, 1, 0x335FEB)
        if mode is None:
            return self._rax
        if mode == 3:
            r = self.agq(agent, agent + 0x20, 0, 0)
            if r != 0:
                return 1
            self._rax = r
        return 0


def run_model(case, raw, secs):
    m = Model(case, raw, secs)
    for step in case.get("steps", []):
        entry, rcx = step[0], step[1]
        rdx = step[2] if len(step) > 2 else 0
        r8 = step[3] if len(step) > 3 else 0
        r9 = step[4] if len(step) > 4 else 0
        if entry == QWALK:
            m.rets.append(m.qwalk(rcx, rdx, r8, STACK + 0x80000))
        elif entry == WWRAP:
            m.rets.append(m.wwrap(rcx, STACK + 0x80008))
        elif entry == GGRID:
            m.rets.append(m.ggrid(rcx))
        elif entry == TTEST:
            m.rets.append(m.ttest(rcx, rdx))
        elif entry in (ETHUNK, ECLASS):
            m.rets.append(m.eclass(rcx, rdx))
        elif entry == SEGT:
            m.rets.append(m.segt(rcx, rdx, r8, r9, STACK + 0x80000))
        elif entry == BASE:
            m.rets.append(m.base(rcx))
        elif entry == ROOTL:
            m.rets.append(m.mq(ROOTCELL))
        elif entry == PRED:
            xmm2 = step[6] if len(step) > 6 else 0
            m.rets.append(m.pred(rcx, rdx, u2f(xmm2 & 0xFFFFFFFF),
                                 r9, STACK + 0x80000))
        elif entry == PATHW:
            m.rets.append(m.pathw(rcx, rdx, STACK + 0x80000))
        elif entry == BLKCHK:
            m.rets.append(m.blkchk(rcx, STACK + 0x80000))
        elif entry == MLOAD:
            m.mload(rcx)
            m.rets.append(m._rax)
        elif entry == AWRAP:
            xmm0 = step[5] if len(step) > 5 else 0
            m.awrap(u2f(xmm0 & 0xFFFFFFFF))
            m.rets.append(m._rax)
        elif entry == RBUILD:
            xmm2 = step[6] if len(step) > 6 else 0
            m.rbuild(rcx, rdx, u2f(xmm2 & 0xFFFFFFFF))
            m.rets.append(m._rax)
        elif entry == ROTCOL:
            xmm2 = step[6] if len(step) > 6 else 0
            xmm1 = step[7] if len(step) > 7 else 0
            m.rotcol(rcx, u2f(xmm1 & 0xFFFFFFFF),
                     u2f(xmm2 & 0xFFFFFFFF))
            m.rets.append(m._rax)
        elif entry == MXVW:
            m.mxvw(rcx, rdx, r8, STACK + 0x80000)
            m.rets.append(m._rax)
        elif entry == MXV:
            m.mxv(rcx, rdx, r8)
            m.rets.append(m._rax)
        m.ends.append(m.fault_end)
        m.fault_end = RETQ
    mem = {}
    for addr, n in case.get("watch", []):
        mem["%x" % addr] = bytes(
            m.mb(addr + i) for i in range(n)).hex()
    return {"trace": m.trace, "faults": m.faults, "rets": m.rets,
            "ends": m.ends, "mem": mem}


# ---------------- cases ----------------

W_PT = [(PT, 8)]
W_VV = [(VECX, 0x10), (VECY, 0x10)]
W_WALK = [(WQ40, 8), (WQ50, 0x10), (WQ60, 0x10)]
W_SEGT = [(SQVA, 0x10), (SQVB, 0x10), (SQVC, 0x10), (SQVD, 0x10)]


def cases():
    C = {}
    # --- BASE / ROOTL leaves ---
    C["base-0"] = {"steps": [(BASE, 0)]}
    C["base-off"] = {"steps": [(BASE, 0x1234)]}
    C["rootl"] = {"steps": [(ROOTL, 0)]}
    # --- ECLASS via real thunk 0x32A780 (ecx=class, dx=flag) ---
    C["cls-w0"] = {"steps": [(ETHUNK, 0, 0)]}        # cl=23 in w0 -> 1
    C["cls-both"] = {"steps": [(ETHUNK, 1, 1)]}      # cl=25 w0&w1 -> 2
    C["cls-w1"] = {"steps": [(ETHUNK, 2, 2)]}        # cl=26 w1 -> 0
    C["cls-none"] = {"steps": [(ETHUNK, 3, 0)]}      # absent -> 0
    C["cls-neg"] = {"steps": [(ETHUNK, 0, 4)]}       # classtab -1 -> -1
    C["cls-b24"] = {"bptab": [(0, 1 << 24)],
                    "steps": [(ETHUNK, 0, 5)]}       # cl=24 w1 -> 0
    # --- TTEST direct (idx array = planted {i0,i1,i2}) ---
    C["tri-in"] = {"steps": [(TTEST, IARR, PT)]}     # (1,1) in T0
    C["tri-out"] = {"ptx": 3.0, "pty": 3.5,
                    "steps": [(TTEST, IARR, PT)]}   # x+y>4 -> 0
    C["tri-below"] = {"ptx": 1.0, "pty": -1.0,     # below v0-v1 edge
                      "steps": [(TTEST, IARR, PT)]}  # edge0 cross flips -> 0
    C["tri-edge"] = {"ptx": 2.0, "pty": 2.0,       # on v1-v2 edge
                     "steps": [(TTEST, IARR, PT)]}
    C["tri-vtx"] = {"ptx": 0.0, "pty": 0.0,        # on v0
                    "steps": [(TTEST, IARR, PT)]}
    C["tri-nan"] = {"ptx": float("nan"),
                    "steps": [(TTEST, IARR, PT)]}   # NaN -> inside
    C["tri-badptr"] = {"steps": [(TTEST, 0xFFFFFFF0, PT)]}
    # --- SEGT direct (p1,p2,va,vb vec4s) ---
    C["seg-cross"] = {"steps": [(SEGT, P1, P2, VECX, VECY)],
                      "watch": W_SEGT}
    C["seg-para"] = {"p2x": 1.0, "p2z": 0.0,
                     "steps": [(SEGT, P1, P2, VECX, VECY)]}
    C["seg-far"] = {"p2x": 1.2, "p2z": 0.5,
                    "steps": [(SEGT, P1, P2, VECX, VECY)]}
    C["seg-touch"] = {"p2x": 2.0, "p2z": 2.0,      # p2 on edge
                      "steps": [(SEGT, P1, P2, VECX, VECY)]}
    C["seg-rev"] = {"p1x": 2.0, "p1z": 2.0, "p2x": 1.0, "p2z": 1.0,
                    "steps": [(SEGT, P1, P2, VECX, VECY)]}  # h1>0,i1<0 -> 1
    C["seg-vert"] = {"p1x": 1.0, "p1z": 1.0, "p2x": 1.0, "p2z": 2.0,
                     "steps": [(SEGT, P1, P2, VECX, VECY)]}  # h2,i2>0 -> 0
    C["seg-beyond2"] = {"p1x": 4.0, "p1z": 4.0, "p2x": 5.0, "p2z": 5.0,
                        "steps": [(SEGT, P1, P2, VECX, VECY)]}  # h2,i2<0
    C["seg-vline"] = {"p1x": 5.0, "p1z": 9.0, "p2x": 5.0, "p2z": -2.0,
                      "steps": [(SEGT, P1, P2, VECX, VECY)]}  # h1,i1<0
    C["seg-badptr"] = {"steps": [(SEGT, 0xFFFFFFF0, P2, VECX, VECY)]}
    # --- WWRAP {x,z} pair ---
    C["wrap-t0"] = {"steps": [(WWRAP, P1)]}         # (1,1) -> 0
    C["wrap-t1"] = {"steps": [(WWRAP, P2)]}         # (3,3) -> 1
    # --- GGRID direct ---
    C["grid-t0"] = {"steps": [(GGRID, PT)]}
    C["grid-t1"] = {"ptx": 3.0, "pty": 3.0,
                    "steps": [(GGRID, PT)]}
    C["grid-multi"] = {"ptx": 3.0, "pty": 0.5,     # cell{0,1}->T0
                       "steps": [(GGRID, PT)]}
    C["grid-multi2"] = {"ptx": 1.0, "pty": 3.5,    # {0,1}->T1
                        "steps": [(GGRID, PT)]}
    C["grid-nanx"] = {"ptx": float("nan"),
                      "steps": [(GGRID, PT)]}
    C["grid-nany"] = {"pty": float("nan"),
                      "steps": [(GGRID, PT)]}
    C["grid-neg"] = {"ptx": -1.0, "steps": [(GGRID, PT)]}
    C["grid-beyond"] = {"ptx": 9.0, "steps": [(GGRID, PT)]}
    C["grid-orig"] = {"ptx": 0.0, "pty": 0.0,
                      "steps": [(GGRID, PT)]}
    C["grid-cw4"] = {"ghdr": {"ch": 4}, "ptx": 5.0, "pty": 1.0,
                     "steps": [(GGRID, PT)]}   # cellH=4: (5,1)->T2
    C["grid-ffff"] = {"cells": [0xFFFF] + CELLS[1:],
                      "steps": [(GGRID, PT)]}
    C["grid-empty"] = {"cells": [0x14] + CELLS[1:],
                       "lists": [[]] + LISTS[1:],
                       "steps": [(GGRID, PT)]}
    C["grid-badptr"] = {"steps": [(GGRID, 0xFFFFFFF0)]}
    C["grid-badroot"] = {"rootp": 0xFFFFFFF0,
                         "steps": [(GGRID, PT)]}
    # --- QWALK ---
    C["walk-same"] = {"steps": [(QWALK, P1, P2, 0)],
                      "watch": W_WALK}
    C["walk-same2"] = {"p2x": 1.5, "p2z": 1.5,
                       "steps": [(QWALK, P1, P2, 0)],
                       "watch": W_WALK}
    C["walk-p1off"] = {"p1x": -1.0, "p1z": -1.0,
                       "steps": [(QWALK, P1, P2, 0)]}
    C["walk-p2off"] = {"p2x": 9.0, "p2z": 9.0,
                       "steps": [(QWALK, P1, P2, 0)]}
    C["walk-p2cyc"] = {"p2x": 9.0, "p2z": 9.0,     # p2 off + cycle adj
                       "adj": [[0, 1, 0, 0], [0, 0, 2, 0],
                               [1, 0, 0, 0], [0, 0, 0, 0]],
                       "steps": [(QWALK, P1, P2, 0)]}
    C["walk-2hop"] = {"p2x": 6.0, "p2z": 1.0,      # T0->T1->T2
                      "eflag": [0, 4, 0, 0],       # e0 flag byte != class
                      "steps": [(QWALK, P1, P2, 0)],
                      "watch": W_WALK}
    C["walk-3hop"] = {"p2x": 6.0, "p2z": 3.0,      # ->T3
                      "steps": [(QWALK, P1, P2, 0)],
                      "watch": W_WALK}
    C["walk-negcls"] = {"steps": [(QWALK, P1, P2, 4)]}
    C["walk-cls2"] = {"eclass": [0, 1, 0, 0],      # e0 w0&w1 b25
                      "steps": [(QWALK, P1, P2, 1)]}
    C["walk-flag"] = {"eclass": [0, 2, 0, 0],      # e0 w1 b26
                      "eflag": [0, 4, 0, 0],       # b6 bit2 set
                      "steps": [(QWALK, P1, P2, 2)],
                      "watch": W_WALK}
    C["walk-noflag"] = {"eclass": [0, 2, 0, 0],
                        "eflag": [0, 0, 0, 0],
                        "steps": [(QWALK, P1, P2, 2)]}
    C["walk-cycle"] = {
        # T3 unreachable (dst=3); seg crosses e0/e1 -> closed
        # T0->T1->T2->T0 cycle -> 0x80 budget -> ret 0
        "adj": [[0, 1, 0, 0], [0, 0, 2, 0], [1, 0, 0, 0],
                [0, 0, 0, 0]],
        "p2x": 6.0, "p2z": 3.0,
        "steps": [(QWALK, P1, P2, 0)]}
    C["walk-badptr"] = {"steps": [(QWALK, 0xFFFFFFF0, P2, 0)]}
    # ---------- EXP-132 consumer cases ----------
    # --- helper-level ---
    C["mload-const"] = {"steps": [(MLOAD, MATB)],
                        "watch": [(MATB, 0x40)]}
    C["awrap-zero"] = {"steps": [(AWRAP, 0, 0, 0, 0, f2u(0.0))]}
    C["awrap-pi2"] = {"steps": [(AWRAP, 0, 0, 0, 0,
                                 f2u(math.pi / 2))]}
    C["awrap-3pi2"] = {"steps": [(AWRAP, 0, 0, 0, 0,
                                  f2u(3 * math.pi / 2))]}  # -> -pi/2
    C["awrap-n3pi2"] = {"steps": [(AWRAP, 0, 0, 0, 0,
                                   f2u(-3 * math.pi / 2))]}
    C["awrap-pi"] = {"steps": [(AWRAP, 0, 0, 0, 0,
                                f2u(math.pi))]}            # edge
    C["awrap-4pi"] = {"steps": [(AWRAP, 0, 0, 0, 0,
                                 f2u(4 * math.pi))]}       # edge
    C["awrap-big"] = {"steps": [(AWRAP, 0, 0, 0, 0,
                                 f2u(40.0))]}              # mod path
    C["awrap-negbig"] = {"steps": [(AWRAP, 0, 0, 0, 0,
                                    f2u(-40.0))]}
    C["awrap-nan"] = {"steps": [(AWRAP, 0, 0, 0, 0,
                                 f2u(float("nan")))]}
    C["awrap-inf"] = {"steps": [(AWRAP, 0, 0, 0, 0,
                                 f2u(float("inf")))]}
    C["awrap-neginf"] = {"steps": [(AWRAP, 0, 0, 0, 0,
                                    f2u(float("-inf")))]}
    C["awrap-n7pi2"] = {"steps": [(AWRAP, 0, 0, 0, 0,
                                   f2u(-7 * math.pi / 2))]}
    C["awrap-13"] = {"steps": [(AWRAP, 0, 0, 0, 0, f2u(13.0))]}
    C["awrap-n7"] = {"steps": [(AWRAP, 0, 0, 0, 0, f2u(-7.0))]}
    C["rbuild-rot"] = {"steps": [(RBUILD, MATB + 0x100, MATB,
                                 0, 0, 0, f2u(math.pi / 4))],
                       "watch": [(MATB + 0x100, 0x40)]}
    C["rbuild-zero"] = {"steps": [(RBUILD, MATB + 0x100, MATB,
                                  0, 0, 0, f2u(0.0))],
                        "watch": [(MATB + 0x100, 0x40)]}
    C["rotcol-mix"] = {"m1": 2.0, "m2": 3.0, "m5": 4.0,
                       "m8": 5.0, "m11": 6.0,
                       "steps": [(ROTCOL, MATB, 0, 0, 0, 0,
                                  f2u(0.6), f2u(0.8))],   # sin .8 cos .6
                       "watch": [(MATB, 0x40)]}
    C["mxv-gen"] = {"m0": 2.0, "m4": 0.5, "m8": 0.25,
                    "m12": 1.0, "m5": 3.0, "m10": 4.0,
                    "steps": [(MXV, DVB, MATB, VECQ)],
                    "watch": [(DVB, 0x10)]}
    C["mxv-badptr"] = {"steps": [(MXV, DVB, MATB, 0xFFFFFFF0)]}
    C["mxvw-gen"] = {"m0": 2.0, "m5": 3.0, "m10": 4.0,
                     "m15": 5.0,
                     "steps": [(MXVW, DVB, MATB, VECQ)],
                     "watch": [(DVB, 0x10)]}
    # --- PATHW 0033A3D0 (rcx=A, rdx=B) ---
    # watch: adj-vec w (frame+0x20) and rotated mat (frame+0x40)
    W_PATHW = [(STACK + 0x7FF88, 0x10), (STACK + 0x7FFA8, 0x40)]
    # direct B->A blocked at T3 exhaust (no e2 crossing) ->
    # rotated offsets reachable -> ret 1
    C["pathw-open"] = {"p1x": 1.0, "p1z": 1.0, "p2x": 6.0,
                       "p2z": 3.0,
                       "eflag": [2, 2, 2, 2],   # bit1 for flag=1
                       "steps": [(PATHW, P1, P2)],
                       "watch": W_PATHW}
    # all edges class-rejected: Q(B->A)=1, both rotated probes
    # blocked -> ret 0
    C["pathw-block"] = {"p1x": 1.0, "p1z": 1.0, "p2x": 6.0,
                        "p2z": 3.0,
                        "eclass": [0, 2, 2, 2],
                        "steps": [(PATHW, P1, P2)],
                        "watch": W_PATHW}
    # direct blocked AND rotated offsets off-grid -> ret 0
    C["pathw-rotfail"] = {"p1x": 0.5, "p1z": 0.5, "p2x": 7.5,
                          "p2z": 3.5,
                          "steps": [(PATHW, P1, P2)],
                          "watch": W_PATHW}
    # direct reachable -> ret 1 immediately
    C["pathw-direct"] = {"p1x": 1.0, "p1z": 1.0, "p2x": 3.0,
                         "p2z": 3.0,
                         "eflag": [2, 2, 2, 2],
                         "steps": [(PATHW, P1, P2)]}
    # direct blocked (e1); r1 arm reaches (e2 flag-bit1), r2
    # blocked (e1) -> ret 0 via round probes
    C["pathw-mixed"] = {"p1x": 1.0, "p1z": 1.0, "p2x": 6.0,
                        "p2z": 3.0,
                        "eclass": [0, 2, 0, 0],
                        "eflag": [2, 0, 2, 0],
                        "steps": [(PATHW, P1, P2)],
                        "watch": W_PATHW}
    # faults: B unmapped (first read 0x33D3FE), A unmapped
    # (second pair read 0x33D442)
    C["pathw-badptrB"] = {"steps": [(PATHW, P1, 0xFFFFFFF0)]}
    C["pathw-badptrA"] = {"steps": [(PATHW, 0xFFFFFFF0, P2)]}
    # r1 probe1 B->w1 same-tri (w1 lands inside T3);
    # r1 probe2 w1->A blocked at e1 -> the probe2 jne site
    # executes; native continues -> ret 0
    C["pathw-r1p2"] = {"p1x": 1.0, "p1z": 1.0, "p2x": 7.0,
                       "p2z": 2.0,
                       "eclass": [0, 0, 2, 0],
                       "eflag": [0, 2, 0, 2],
                       "steps": [(PATHW, P1, P2)]}
    # r1 w1 off-grid (skips r1p2); r2 probe1 B->w2 reachable
    # (w2 in T2 via e2), r2 probe2 w2->A blocked at e1 ->
    # the round-2 jne executes; native continues -> ret 0
    C["pathw-r2p2"] = {"p1x": 1.0, "p1z": 1.0, "p2x": 6.0,
                       "p2z": 3.0,
                       "eclass": [0, 0, 2, 0],
                       "eflag": [0, 2, 0, 2],
                       "steps": [(PATHW, P1, P2)]}
    # --- BLKCHK 00335F90 (rcx=agent) ---
    # watch: nested QWALK frame locals
    W_BLK = [(STACK + 0x7FF58, 8), (STACK + 0x7FF68, 0x10),
             (STACK + 0x7FF78, 0x10)]
    # cross-tri walk, flag bit0 passable, tiny radius scale
    # -> PRED 0 -> walk 0 -> mode 0 -> ret 0
    C["blk-clear"] = {"ag2x": 6.0, "radius": 1e-28,
                      "eflag": [1, 1, 1, 1],
                      "steps": [(BLKCHK, AGENT)],
                      "watch": W_BLK}
    # visible radius -> scale 0.45 shifts the PRED probes
    # (m-blk-sc disp mutant reads 1.2f -> different coords)
    C["blk-scale"] = {"ag2x": 6.0, "radius": 0.5,
                      "eflag": [1, 1, 1, 1],
                      "steps": [(BLKCHK, AGENT)]}
    # all edges class-rejected -> PRED probe exhaust -> ret 1
    C["blk-predblock"] = {"ag2x": 6.0, "eclass": [2, 2, 2, 2],
                          "steps": [(BLKCHK, AGENT)],
                          "watch": W_BLK}
    # class-0 edges, flag byte 0 -> flag gate rejects (mode 0)
    # -> PRED 1 -> ret 1
    C["blk-walkblock"] = {"ag2x": 6.0,
                          "steps": [(BLKCHK, AGENT)],
                          "watch": W_BLK}
    # mode 3 (flag bit3 passable) -> AGENTQ scripted boundary
    C["blk-mode3-0"] = {"mode": 3, "agrets": [0], "ag2x": 6.0,
                        "eflag": [8, 8, 8, 8],
                        "steps": [(BLKCHK, AGENT)],
                        "watch": W_BLK}
    C["blk-mode3-1"] = {"mode": 3, "agrets": [1], "ag2x": 6.0,
                        "eflag": [8, 8, 8, 8],
                        "steps": [(BLKCHK, AGENT)],
                        "watch": W_BLK}
    C["blk-mode3-neg"] = {"mode": 3, "agrets": [-1], "ag2x": 6.0,
                          "eflag": [8, 8, 8, 8],
                          "steps": [(BLKCHK, AGENT)]}
    C["blk-mode7"] = {"mode": 7, "ag2x": 6.0,
                      "eflag": [0x80, 0x80, 0x80, 0x80],
                      "steps": [(BLKCHK, AGENT)]}
    # NaN radius -> scale NaN -> offsets NaN -> probes p1-off -> 0
    C["blk-radiusnan"] = {"radius": float("nan"),
                          "steps": [(BLKCHK, AGENT)]}
    # fault: agent unmapped -> first read 0x335F9F
    C["blk-badptr"] = {"steps": [(BLKCHK, 0xFFFFFFF0)]}
    # fault: sub-record unmapped -> second read 0x335FAD
    C["blk-subbad"] = {"subp": 0xFFFFFFF0,
                       "steps": [(BLKCHK, AGENT)]}
    # --- PRED direct (probes now run real QWALK) ---
    C["pred-clear"] = {"steps": [(PRED, P1, P2, 0, 0, 0, f2u(0.5))]}
    C["pred-blocked"] = {"eclass": [2, 2, 2, 2],
                         "steps": [(PRED, P1, P2, 0, 0, 0,
                                    f2u(0.5))]}
    C["pred-offgrid"] = {"steps": [(PRED, P1, P2, 0, 0, 0,
                                    f2u(10.0))]}
    return C


# ---------------- mutations (verified byte-precise) ----------------

MUTS = [
    # QWALK 0033D3E0 (sites byte-verified against shipped image)
    ("m-walk-sameje", "walk-negcls", 0x33D4A7, 0x84, 0x85),  # cur==dst je->jne
    ("m-walk-budget", "walk-cycle",  0x33D607, 0xFD, 0xFC),  # r13d -> r12d
    ("m-walk-degw",   "walk-2hop",   0x33D4B1, 0x0A, 0x0C),  # w[rbp+0xa]->+0xc
    ("m-walk-mat",    "walk-2hop",   0x33D4EA, 0x48, 0x88),  # adj *2 -> *4
    ("m-walk-b5",     "walk-2hop",   0x33D502, 0x05, 0x06),  # edge b+5 -> +6
    ("m-walk-cmp1",   "walk-2hop",   0x33D50A, 0x01, 0x00),  # cmp eax,1 -> 0
    ("m-walk-je",     "walk-2hop",   0x33D50B, 0x74, 0x75),  # ==1 je -> jne
    ("m-walk-flgshl", "walk-flag",   0x33D52B, 0xE0, 0xE8),  # shl eax,cl->shr
    ("m-walk-ftest",  "walk-2hop",   0x33D4EE, 0x84, 0x85),  # e==0 je -> jne
    ("m-walk-segjn",  "walk-2hop",   0x33D5D9, 0x75, 0x74),  # seg jne -> je
    ("m-walk-adv",    "walk-2hop",   0x33D5F0, 0xF6, 0xF0),  # r14d=esi -> eax
    ("m-walk-grid1",  "walk-p1off",  0x33D439, 0x75, 0x74),  # p1 jne -> je
    ("m-walk-grid2",  "walk-p2cyc",  0x33D46A, 0x75, 0x74),  # p2 jne -> je
    ("m-walk-p1x",    "walk-3hop",   0x33D402, 0x45, 0x55),  # [rcx+0] -> [rdx+0]
    ("m-walk-jae",    "walk-negcls", 0x33D4B3, 0x83, 0x82),  # jae -> jb
    ("m-walk-slotsk", "walk-2hop",   0x33D4CB, 0xF4, 0xF6),  # prev-skip -> cur-skip
    # GGRID 00383F10
    ("m-grid-fdcx",   "grid-nanx",   0x383F47, 0x02, 0x03),  # cmp ax,2 -> 3
    ("m-grid-fdcy",   "grid-nany",   0x383F5D, 0x02, 0x03),  # cmp ax,2 -> 3
    ("m-grid-boundx", "grid-t0",     0x383F78, 0x87, 0x86),  # ja -> jbe
    ("m-grid-boundy", "grid-t0",     0x383F94, 0x87, 0x86),  # ja -> jbe
    ("m-grid-bxup",   "grid-t0",     0x383FB0, 0x87, 0x86),  # x up ja -> jbe
    ("m-grid-byup",   "grid-t0",     0x383FCE, 0x87, 0x86),  # y up ja -> jbe
    ("m-grid-cellh",  "grid-multi2", 0x383FEF, 0x01, 0x02),  # b[rbx+1]->+2
    ("m-grid-orgx",   "grid-cw4",    0x384011, 0x04, 0x08),  # w[rbx+4]->+8
    ("m-grid-ffff",   "grid-ffff",   0x384033, 0xFF, 0xFE),  # cell 0xFFFF cmp
    ("m-grid-0xff",   "grid-empty",  0x384051, 0xFF, 0xFE),  # list end 0xFF
    ("m-grid-stride", "grid-multi2", 0x38407B, 0x22, 0x24),  # rec *0x22->*0x24
    ("m-grid-sel",    "grid-multi2", 0x3840AD, 0x14, 0x16),  # rec +0x14->+0x16
    ("m-grid-trije",  "grid-multi2", 0x3840CC, 0x74, 0x75),  # ttest je->jne
    ("m-grid-listjn", "grid-multi2", 0x3840F9, 0x85, 0x84),  # next list jne
    ("m-grid-cntcmp", "grid-multi",  0x384081, 0x02, 0x04),  # rec +2 -> +4
    # TTEST 00382D10
    ("m-tri-arr",     "tri-below",   0x382D34, 0x78, 0x7C),  # idx arr lea +4
    ("m-tri-mul1",    "tri-in",      0x382E2A, 0x59, 0x58),  # mulss -> addss
    ("m-tri-mul2",    "tri-in",      0x382E30, 0xC0, 0xC1),  # py*ex -> py*acc
    ("m-tri-sub",     "tri-in",      0x382E33, 0x5C, 0x58),  # subss -> addss
    ("m-tri-ucmp",    "tri-below",   0x382E13, 0xCA, 0xC8),  # vs xmm10 -> xmm8
    ("m-tri-jne",     "tri-below",   0x382E37, 0x75, 0x74),  # jne -> je
    ("m-tri-ja",      "tri-edge",    0x382E48, 0x77, 0x76),  # ja -> jbe
    ("m-tri-loop",    "tri-below",   0x382E51, 0x8C, 0x8D),  # jl -> jge
    ("m-tri-vscale",  "tri-below",   0x382D96, 0xDF, 0x9F),  # vert *8 -> *4
    ("m-tri-esub",    "tri-out",     0x382DA1, 0xD0, 0x90),  # edge *8 -> *4
    # SEGT 00468880
    ("m-seg-jbe1",    "seg-cross",   0x4689A6, 0x76, 0x77),  # h1 jbe -> ja
    ("m-seg-jbe2",    "seg-rev",     0x4689AB, 0x76, 0x77),  # i1 jbe -> ja
    ("m-seg-jbe3",    "seg-vline",   0x4689B7, 0x76, 0x77),  # 0<=h1 jbe->ja
    ("m-seg-ja4",     "seg-vline",   0x4689BC, 0x77, 0x76),  # i1 ja -> jbe
    ("m-seg-ja5",     "seg-cross",   0x468A3B, 0x87, 0x86),  # h2 ja -> jbe
    ("m-seg-jbe6",    "seg-beyond2", 0x468A43, 0x76, 0x77),  # 0<=h2 jbe->ja
    ("m-seg-call",    "seg-cross",   0x46893C, 0x40, 0x44),  # vsub rel32 +4
    ("m-seg-call2",   "seg-cross",   0x46894D, 0x2F, 0x33),  # vsub2 rel32 +4
    ("m-seg-xcall",   "seg-cross",   0x468984, 0x88, 0x8C),  # xprod rel32 +4
    ("m-seg-xcall2",  "seg-cross",   0x468995, 0x77, 0x7B),  # xprod2 rel32 +4
    ("m-seg-cook",    "seg-cross",   0x468899, 0x93, 0x9B),  # cookie cell disp
    # ECLASS 0026E300 (+ thunk 0x32A780)
    ("m-cls-js",      "cls-neg",     0x26E317, 0x78, 0x79),  # js -> jns
    ("m-cls-shl",     "cls-w0",      0x26E32F, 0xE2, 0xE8),  # shl edx,cl->shr
    ("m-cls-w0d",     "cls-both",    0x26E338, 0x04, 0x08),  # test [r8+4]->+8
    ("m-cls-je",      "cls-w0",      0x26E333, 0x74, 0x75),  # w0 je -> jne
    ("m-cls-cmov",    "cls-both",    0x26E33F, 0x45, 0x44),  # cmovne -> cmove
    ("m-cls-thunk",   "walk-2hop",   0x32A781, 0x7B, 0x7F),  # jmp rel32 +4
    ("m-cls-tab",     "cls-w0",      0x26E311, 0x60, 0x64),  # classtab -> +4
    # WWRAP 00384130
    ("m-wrap-z",      "wrap-t1",     0x38413C, 0x08, 0x04),  # vec.z -> vec.y
    # BASE 0020E600
    ("m-base-add",    "base-off",    0x20E605, 0x27, 0x2B),  # pool cell disp
    # ---------- EXP-132 new bodies (sites byte-verified) ----------
    # PATHW 0033A3D0
    ("m-pw-cmp1",   "pathw-block",   0x33A408, 0x01, 0x02),  # probe0 cmp eax,1->2
    ("m-pw-je0",    "pathw-block",   0x33A409, 0x74, 0x75),  # probe0 je -> jne
    ("m-pw-cmp1b",  "pathw-rotfail", 0x33A4A0, 0x01, 0x02),  # r1 cmp 1 -> 2
    ("m-pw-je1",    "pathw-rotfail", 0x33A4A1, 0x74, 0x75),  # r1 je -> jne
    ("m-pw-jne1",   "pathw-r1p2",    0x33A4BA, 0x85, 0x84),  # r1 p2 jne -> je
    ("m-pw-cmp2a",  "pathw-rotfail", 0x33A523, 0x01, 0x02),  # r1' cmp 1 -> 2
    ("m-pw-je2",    "pathw-rotfail", 0x33A524, 0x74, 0x75),  # r1' je -> jne
    ("m-pw-jne2",   "pathw-r2p2",    0x33A53D, 0x85, 0x84),  # r2 p2 jne -> je
    ("m-pw-ret1",   "pathw-direct",  0x33A40C, 0x01, 0x02),  # mov eax,1 -> 2
    ("m-pw-sc",     "pathw-mixed",   0x33A429, 0x43, 0x47),  # scale const +4
    ("m-pw-ang1",   "pathw-mixed",   0x33A44A, 0xC6, 0xCA),  # angle1 cell +4
    ("m-pw-ang2",   "pathw-mixed",   0x33A4CD, 0x47, 0x4B),  # angle2 cell +4
    # BLKCHK 00335F90
    ("m-blk-predje", "blk-clear",    0x335FCE, 0x75, 0x74),  # pred jne -> je
    ("m-blk-walkje", "blk-clear",    0x335FE1, 0x01, 0x00),  # walk cmp 1 -> 0
    ("m-blk-mode7",  "blk-mode3-0",  0x335FF1, 0x03, 0x07),  # mode cmp 3 -> 7
    ("m-blk-agq",    "blk-mode3-0",  0x336002, 0x9A, 0xA2),  # agq call retarget
    ("m-blk-agqje",  "blk-mode3-1",  0x336006, 0x85, 0x29),  # test -> sub eax
    ("m-blk-sc",     "blk-scale",    0x335FC0, 0xC8, 0xCC),  # BKSC disp +4
    ("m-blk-subf",   "blk-clear",    0x335FA2, 0x08, 0x0C),  # agent+0x108->+0x10C
    # AWRAP 0033CB70
    ("m-aw-hi",     "awrap-inf",     0x33CB7A, 0x77, 0x76),  # hi gate ja->jbe
    ("m-aw-lo",     "awrap-neginf",  0x33CB87, 0x77, 0x76),  # lo gate ja->jbe
    ("m-aw-ja1",    "awrap-3pi2",    0x33CBA7, 0x77, 0x76),  # loop1 back ja->jbe
    ("m-aw-add1",   "awrap-3pi2",    0x33CBA2, 0x58, 0x5C),  # addss -2pi -> subss
    ("m-aw-add2",   "awrap-n3pi2",   0x33CBC2, 0x58, 0x5C),  # addss +2pi -> subss
    ("m-aw-cvtt",   "awrap-big",     0x33CBD7, 0x2C, 0x2A),  # cvttss2si->cvtsi2ss
    ("m-aw-hidisp", "awrap-13",      0x33CB76, 0x92, 0x96),  # hi gate cell +4
    ("m-aw-lodisp", "awrap-n7",      0x33CB80, 0x9C, 0xA0),  # lo gate cell +4
    ("m-aw-n2disp", "awrap-3pi2",    0x33CB9A, 0x86, 0x8A),  # -2pi cell -> 3e29
    ("m-aw-npdisp", "awrap-n3pi2",   0x33CBAD, 0x6F, 0x77),  # -pi cell -> 3e29
    ("m-aw-div",    "awrap-big",     0x33CBCF, 0x5E, 0x59),  # divss -> mulss
    # MLOAD 00203170
    ("m-ml-disp",   "mload-const",   0x203173, 0x09, 0x0D),  # src1 +4
    ("m-ml-disp2",  "mload-const",   0x20317D, 0x0F, 0x13),  # src2 +4
    # RBUILD 00202F00
    ("m-rb-call1",  "rbuild-zero",   0x202F38, 0xCC, 0xD2),  # cosf -> sinf
    ("m-rb-call2",  "rbuild-zero",   0x202F43, 0xC7, 0xC1),  # sinf -> cosf
    # ROTCOL 00217880
    ("m-rc-sub",    "rotcol-mix",    0x2178D7, 0x5C, 0x58),  # subss -> addss
    ("m-rc-disp",   "rotcol-mix",    0x21788F, 0x08, 0x0C),  # [rcx+8]->+0xC
    # MXV 00217060
    ("m-mxv-add",   "mxv-gen",       0x2170A8, 0x58, 0x5C),  # addss -> subss
    ("m-mxv-disp",  "mxv-gen",       0x2170A5, 0x14, 0x18),  # m[0x14]->m[0x18]
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
