# EXP-133 nav-los-exec — native replay harness.
#
# Executes the nav LOS/raycast query tree real — the segment-vs-
# wall-record family below consumer 00335B60 — with only CRT
# imports scripted:
#
#   LQUERY 00391410 758B — segment LOS query over a wall-record
#         grid. r13 = ROOTL (0 -> ret 0); AABB = p1/p2 min/max
#         +/- xmm2 radius, eps-biased, /d[0x2AEE090] cell size,
#         cvttss2si -> BMASK(ecx=xlo,edx=zlo,r8=xhi,r9=zhi) ->
#         row-bitmap at q[0x2AEE0B0]+0x10; dead DIST call
#         (result discarded); 160-iter loop (i): bit (i%8) of
#         b[mask+0x10+i/8] set -> i<0x20 reads 0x20-stride wall
#         record at BASE(d[root+0x28])+i*0x20 (w[+0] type: 0 ->
#         CAPT0 point capsule; 1 -> CAPT1 edge capsule; else
#         skip); i>=0x20 -> RDEC(i-0x20) nav-record decode ->
#         CAPT1. First nonzero -> ret 1; exhaust -> ret 0.
#   BMASK  003912E0 292B — memset(q[0x2AEE0B0],0,d[0x2AEE0B8])
#         via real thunk 00861EC0 -> q[0x8C2A60] VCRUNTIME140!
#         memset (import-dir proven); clamp cols [0,d[0x2AEE060])
#         rows [0,q[0x2AEE064]); per flagged cell b[q[0x2AEE0A8]
#         +row*W+col] OR d[0x2AEE0B8] bytes from q[0x2AEE0A0]+
#         idx*reclen into the mask; ret rax = q[0x2AEE0B0].
#   DIST   003A1920 53B  — sqrt(|a-b|^2) over x,y,z -> THUNKF.
#         Called by LQUERY with the result discarded (dead).
#   CAPT0  00468D50 250B — capsule test A: seg {p1,p2} at rcx,
#         point+radius at rdx. p1==p2 (x,z) -> dist p1->edge;
#         else CPSEG closest -> ==p1 -> ret 0; radius sum
#         d[rcx+0x20]+d[rdx+0x10] > sqrt(dist2) -> 1 else 0.
#   CAPT1  00468E50 281B — capsule test B: CPSEG first; point-seg
#         skips the ==p1 exclusion (real seg keeps it); then
#         TRIGD(edge, closest) + d[seg+0x20] > sqrt(|edge-
#         closest|^2) -> 1 else 0.
#   CPSEG  004691A0 315B — closest point on seg [rdx,r8] to pt
#         r9: t = dot(a-p, a-b)/|a-b|^2; t<0 -> a; t>1 -> b;
#         else a + t(b-a); 16B out to [rcx], rax = rcx.
#   TRIGD  00468580 325B — trig-table helper: angle d[rcx+0x18]/
#         d[0x915624](-2pi) * +/-32768 -> &0x7fff into shipped
#         table 0x1F004E0; t1=sin-ish,t2=cos-ish; xmm8=(t2*dz+
#         t1*dx)/d[rcx+0x10], xmm7=(t1*dz-t2*dx)/d[rcx+0x14];
#         d=sqrt(x8^2+x7^2); cvtss2sd comisd vs 1e-6 -> <=: ret
#         d[rcx+0x10]; else ret sqrt((x8*e10/d)^2+(x7*e14/d)^2).
#   CAPV   00469410 346B — sibling capsule variant (same dot/
#         clamp family; real body executed standalone).
#   RDEC   0032A6E0 153B — nav-record decode: q[0x209A670] root
#         -> rec pool +0x1a0 (16B stride), vtx pool +0x188 (64B);
#         out = {vtx+0x30,+0x34,+0x38, w[rec+4..8]*1/4096 fixed
#         point, atan2f(vtx+0x28, vtx+0x20)}; side-writes scaled
#         vec to global scratch 0x22D91B0.
#
# Re-executed real (previous packages): ROOTL 00383840, BASE
# 0020E600, CHKCK 00808C40, THUNKF 00861F14 (real IAT -> sqrtf
# trampoline), plus the EXP-131 mesh bodies kept for regression
# (QWALK/GGRID/TTEST/ECLASS/SEGT) and EXP-130/132 helpers.
#
# Scripted boundaries (disclosed):
#   FDC  _fdclass  via real IAT q[0x8C2C10] (EXP-131).
#   SQF  sqrtf     via real thunk+IAT q[0x8C2BB8] (EXP-130).
#   ISN  _isnan    via real IAT q[0x8C2C68] (EXP-130).
#   FIN  _finite   via real IAT q[0x8C2C70] (EXP-130).
#   COS  cosf      via real thunk 00861F08 + IAT q[0x8C2BA8].
#   SIN  sinf      via real thunk 00861F0E + IAT q[0x8C2BB0].
#   MSET memset    via real thunk 00861EC0 + IAT q[0x8C2A60]
#        (import-dir proven VCRUNTIME140!memset).
#   AT2  atan2f    via real thunk 00861F02 + IAT q[0x8C2BD0]
#        (import-dir proven).
#   AGENTQ 00318CA0 — kept from EXP-132 (unused by this tree).
#
# Fixture (planted, disclosed): EXP-131 synthetic nav mesh
# wholesale PLUS the LOS grid global block 0x2AEE060..0x2AEE0B8
# (gridW/H, cell size, eps pair, cell-flag map, per-cell record
# bitmasks, OR accumulator, reclen — all BSS, ships 0), wall
# record pool at BASE(root+0x28), nav-record root q[0x209A670]
# (+0x188 vtx pool / +0x1a0 rec pool — BSS). Shipped rdata:
# trig table 0x1F004E0, -2pi 0x915624, +-32768 0xD10820/28,
# 1e-6 threshold 0x9002C8, 1/4096 scale 0x908E30, 1.0f clamps.
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
MSET   = 0x630A0000          # planted trampoline: memset import
AT2    = 0x630B0000          # planted trampoline: atan2f import

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
# EXP-133 new bodies
LQUERY = 0x00391410          # segment LOS query over wall grid
BMASK  = 0x003912E0          # AABB -> OR'd record bitmask
DIST   = 0x003A1920          # 3D point distance -> THUNKF
CAPT0  = 0x00468D50          # capsule test A (point radius)
CAPT1  = 0x00468E50          # capsule test B (edge + TRIGD)
CPSEG  = 0x004691A0          # closest point on segment
TRIGD  = 0x00468580          # trig-table edge helper
CAPV   = 0x00469410          # sibling capsule variant
RDEC   = 0x0032A6E0          # nav-record decode + atan2f
TMS    = 0x00861EC0          # real IAT thunk -> memset
TAT2   = 0x00861F02          # real IAT thunk -> atan2f

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
IATMSET  = 0x8C2A60          # q: IAT memset (import-dir proven)
IATAT2   = 0x8C2BD0          # q: IAT atan2f (import-dir proven)
# LQUERY/BMASK grid global block — all BSS (ships 0, runtime
# populated by the nav loader): planted per case
LGW      = 0x2AEE060         # d: LOS grid width (cols)
LGH      = 0x2AEE064         # q: LOS grid height (rows)
LEPSX    = 0x2AEE070         # d: x-range epsilon (sub hi AND lo)
LEPSZ    = 0x2AEE078         # d: z-range epsilon (sub hi AND lo)
LCSZ     = 0x2AEE090         # d: cell size divisor
LLSRC    = 0x2AEE0A0         # q: per-cell record bitmask array
LCFLG    = 0x2AEE0A8         # q: cell-flag map (b per cell)
LBMSK    = 0x2AEE0B0         # q: bitmask accumulator/return
LRLEN    = 0x2AEE0B8         # d: record len = memset len = stride
NRROOT   = 0x209A670         # q: nav-record root (BSS, ships 0)
RSCRATCH = 0x22D91B0         # xmm: RDEC scaled-vec global scratch
TRIGT    = 0x1F004E0         # f: shipped 0x8000-entry trig table
NEG2PI   = 0x915624          # d: -2pi (== AWNEG2)
TRIGN    = 0xD10828          # d: -32768.0 table index scale
TRIGP    = 0xD10820          # d: +32768.0 table index scale
DISTEPS  = 0x9002C8          # d: 1e-6 double threshold (comisd)
SCLV     = 0x908E30          # xmm: 1/4096 fixed-point scale
CLAMP1   = 0x1CEBBA8         # d: 1.0f clamp (== SEEDF)

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
# EXP-133 LOS fixture
NRO    = HEAP + 0x1A000      # nav-record root {+0x188 vtx,+0x1a0 rec}
RECP   = HEAP + 0x1B000      # 16B-stride nav-record pool
VEXP   = HEAP + 0x1D000      # 64B-stride vertex pool
CFLGA  = HEAP + 0x1F000      # cell-flag map (b per cell)
LSRCA  = HEAP + 0x20000      # per-cell record bitmask array
BMSKA  = HEAP + 0x28000      # bitmask accumulator buffer
WPOOL  = 0x0800              # BASE offset: wall rec pool (0x20 stride)
SEGV   = HEAP + 0x2A000      # CAPT/CPSEG arg vecs

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
    _CRT.atan2f.restype = ctypes.c_float
    _CRT.atan2f.argtypes = (ctypes.c_float, ctypes.c_float)
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
    r = f32(float(Fraction(n) * unit))
    return -r if sgn else r


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


def atan2f_bits(uy, ux):
    if _CRT is not None:
        return f2u(_CRT.atan2f(u2f(uy), u2f(ux)))
    y, x = u2f(uy), u2f(ux)
    if math.isnan(y) or math.isnan(x):
        return f2u(float("nan"))
    return f2u(f32(math.atan2(y, x)))


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


def _ueq(a, b):
    """ucomiss ordered-equal: jp/jne both fall through."""
    return not math.isnan(a) and not math.isnan(b) and a == b


def _seta(a, b):
    """comiss a,b -> seta: CF=0 and ZF=0 -> a > b ordered."""
    return not math.isnan(a) and not math.isnan(b) and a > b


def _maxss(a, b):
    """maxss dst,src: unordered or src>=dst -> src."""
    return b if (math.isnan(a) or math.isnan(b) or b >= a) else a


def _minss(a, b):
    """minss dst,src: unordered or src<=dst -> src... inverse:
    dst = src if src < dst or unordered else dst."""
    return b if (math.isnan(a) or math.isnan(b) or b < a) else a


INDEF = u2f(0xFFC00000)          # x86 real-indefinite QNaN


def _qn(u):
    """NaN propagation: quieted u32 payload; None if not NaN."""
    return (u | 0x400000) if (u & 0x7FFFFFFF) > 0x7F800000 else None


def _n2(a, b):
    """SSE two-operand NaN rule: source(b) NaN wins, then dest(a)."""
    return _qn(f2u(b)) or _qn(f2u(a))


def _m(a, b):
    """mulss — NaN propagate; 0*inf -> real-indefinite."""
    n = _n2(a, b)
    if n is not None:
        return u2f(n)
    if (a == 0) != (b == 0) and (math.isinf(a) or math.isinf(b)):
        return INDEF
    return f32(a * b)


def _a(a, b):
    """addss — NaN propagate; +inf + -inf -> indefinite."""
    n = _n2(a, b)
    if n is not None:
        return u2f(n)
    if math.isinf(a) and math.isinf(b) and a != b:
        return INDEF
    return f32(a + b)


def _s(a, b):
    """subss — NaN propagate; inf - inf -> indefinite."""
    n = _n2(a, b)
    if n is not None:
        return u2f(n)
    if math.isinf(a) and math.isinf(b) and a == b:
        return INDEF
    return f32(a - b)


def _d(a, b):
    """divss — NaN propagate; 0/0, inf/inf -> indefinite."""
    n = _n2(a, b)
    if n is not None:
        return u2f(n)
    if (a == 0 and b == 0) or (math.isinf(a) and math.isinf(b)):
        return INDEF
    return f32div(a, b)


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
    buf = bytearray(0xC00 + WPOOL)
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
    # wall record pool at root+0x28 (0x20-stride records):
    # type-0 {w@0, x@4, z@8, rad@0xc}; type-1 {w@0, x@4, z@8,
    # x2@0xc, z2@0x10, angle@0x14}
    for i, r in enumerate(case.get("wrecs", [])):
        o = WPOOL + i * 0x20
        buf[o:o + 2] = ww(r[0])
        for k, v in enumerate(r[1:]):
            buf[o + 4 + k * 4:o + 8 + k * 4] = ff(v)
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
                      (0x18, LISTR), (0x1C, ADJM), (0x20, GHDR),
                      (0x28, WPOOL)):
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
    # ---- EXP-133 LOS grid block + record pools ----
    W.append((LGW, dw(case.get("lgw", 8))))
    W.append((LGH, qw(case.get("lgh", 8))))
    W.append((LEPSX, ff(case.get("lepsx", 0.5))))
    W.append((LEPSZ, ff(case.get("lepsz", 0.5))))
    W.append((LCSZ, ff(case.get("lcsz", 4.0))))
    W.append((LRLEN, dw(case.get("lrlen", 0x30))))
    W.append((LLSRC, qw(case.get("llsrc", LSRCA))))
    W.append((LCFLG, qw(case.get("lcflg", CFLGA))))
    W.append((LBMSK, qw(case.get("lbmsk", BMSKA))))
    W.append((IATMSET, qw(MSET)))
    W.append((IATAT2, qw(AT2)))
    # cell-flag map + per-cell record bitmasks
    W.append((CFLGA, bytes(case.get("cflags", [0] * 0x100))))
    lsrc = bytearray(0x8000)
    for ci, m in case.get("lsrc", {}).items():
        o = ci * case.get("lrlen", 0x30)
        lsrc[o:o + len(m)] = bytes(m)
    W.append((LSRCA, bytes(lsrc)))
    # nav-record root: +0x188 vtx pool ptr, +0x1a0 rec pool ptr
    nro = bytearray(0x200)
    nro[0x188:0x190] = qw(case.get("vexp", VEXP))
    nro[0x1a0:0x1a8] = qw(case.get("recp", RECP))
    W.append((NRO, bytes(nro)))
    W.append((NRROOT, qw(case.get("nroot", NRO))))
    # 16B-stride rec pool: w pad@0, w vtxidx@2, w x@4, w y@6, w z@8
    recs = bytearray(0x800)
    for i, r in enumerate(case.get("recs", [])):
        o = i * 0x10
        recs[o + 2:o + 4] = ww(r[0])
        recs[o + 4:o + 6] = ww(r[1])
        recs[o + 6:o + 8] = ww(r[2])
        recs[o + 8:o + 10] = ww(r[3])
    W.append((RECP, bytes(recs)))
    # 64B-stride vtx pool: +0x20/+0x28 atan2 args, +0x30..38 out
    vtxs = bytearray(0x2000)
    for i, v in enumerate(case.get("vtxs", [])):
        o = i * 0x40
        for k, f in enumerate(v):
            vtxs[o + 0x20 + k * 4:o + 0x24 + k * 4] = ff(f)
    W.append((VEXP, bytes(vtxs)))
    # standalone capsule arg vecs (floats at 4B lanes):
    # seg {p1v4@0, p2v4@0x10, srad@0x20}; edge/pt {x,y,z,w@0x30,
    # rad/e10@0x40, e14@0x44, ang@0x48}; out bufs +0x100/+0x200
    W.append((SEGV, b"".join(ff(f) for f in
                             case.get("segv", [0.0] * 0x100))))
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
        for t in (SQF, ISN, FIN, COS, SIN, MSET, AT2):
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
        elif addr == MSET:
            dst = uc.reg_read(UC_X86_REG_RCX)
            val = uc.reg_read(UC_X86_REG_RDX) & 0xFF
            cnt = uc.reg_read(UC_X86_REG_R8) & 0xFFFFFFFFFFFFFFFF
            self.gm.w(dst, bytes([val]) * cnt)
            self.trace.append("mset:%x:%x:%x" % (dst, val, cnt))
            self._ret(uc)
        elif addr == AT2:
            y = uc.reg_read(UC_X86_REG_XMM0) & 0xFFFFFFFF
            x = uc.reg_read(UC_X86_REG_XMM1) & 0xFFFFFFFF
            r = atan2f_bits(y, x)
            x0 = uc.reg_read(UC_X86_REG_XMM0)
            uc.reg_write(UC_X86_REG_XMM0,
                         (x0 & ~0xFFFFFFFF) | (r & 0xFFFFFFFF))
            self.trace.append("at2:%x:%x:%x" % (y, x, r))
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

    def _wr(self, a, n, site):
        """ordered write check: records ('memw', a, n) + fault_end
        on unmapped; returns False so caller early-returns _rax."""
        if self.mapped(a):
            return True
        self.faults.append(("memw", a & 0xFFFFFFFFFFFFFFFF, n))
        self.fault_end = site
        return False

    def _sd_flt(self, a, v, site):
        """dword store with fault check."""
        if not self._wr(a, 4, site):
            return False
        self.sd(a, v)
        return True

    def _sf_flt(self, a, v, site):
        """float store with fault check."""
        if not self._wr(a, 4, site):
            return False
        self.sf(a, v)
        return True

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

    def mset(self, dst, val, cnt):
        """memset trampoline — writes into model memory."""
        cnt &= 0xFFFFFFFFFFFFFFFF
        for i in range(cnt):
            self.sb(dst + i, val & 0xFF)
        self.trace.append("mset:%x:%x:%x" % (
            dst & 0xFFFFFFFFFFFFFFFF, val & 0xFF, cnt))

    def at2(self, uy, ux):
        r = atan2f_bits(uy, ux)
        self.trace.append("at2:%x:%x:%x" % (uy & 0xFFFFFFFF,
                                            ux & 0xFFFFFFFF,
                                            r & 0xFFFFFFFF))
        return u2f(r)

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
        [dst]. Sources are NON-contiguous: 0x8C5F80, 0x8C5F90,
        0x8C5FB0, 0x8C5FD0 (0x8C5FA0 skipped)."""
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

    # ---------- EXP-133 LOS tree ----------

    def bmask(self, c0, r0, c1, r1):
        """003912E0 — memset + clamp + OR per-cell record masks.
        args ecx=c0 edx=r0 r8d=c1 r9d=r1 (all sx32)."""
        dst = self.mq(LBMSK)
        rlen = self.md(LRLEN)
        rl = rlen - 0x100000000 if rlen >= 0x80000000 else rlen
        self.mset(dst, 0, rl)              # movsxd r8 count
        w = self.md(LGW)
        if w >= 0x80000000:
            w -= 0x100000000
        h = self.mq(LGH) & 0xFFFFFFFF      # lea eax,[rcx-1] low32
        if h >= 0x80000000:
            h -= 0x100000000

        def sx(v):
            v &= 0xFFFFFFFF
            return v - 0x100000000 if v >= 0x80000000 else v

        def clamp(v, m):                   # jns: <0 -> 0; >m-1 -> m-1
            v = sx(v)
            return 0 if v < 0 else (m - 1 if v > m - 1 else v)

        c0 = clamp(c0, w)
        r0 = clamp(r0, h)
        c1 = clamp(c1, w)
        r1 = clamp(r1, h)
        if r0 <= r1:
            cmap = self.mq(LCFLG)
            lsrc = self.mq(LLSRC)
            for row in range(r0, r1 + 1):
                for col in range(c0, c1 + 1):
                    idx = sx(row * w + col)
                    self._rax = cmap            # rax = q[LCFLG]
                    fl = self._rd((cmap + idx) & 0xFFFFFFFFFFFFFFFF,
                                  1, 0x391394)
                    if fl is None:
                        return self._rax
                    if fl == 0:
                        continue
                    src = (lsrc + sx(idx * rlen)) & 0xFFFFFFFFFFFFFFFF
                    for k in range(rlen):
                        self._rax = k           # byte-index counter
                        sv = self._rd(src + k, 1, 0x3913BB)
                        if sv is None:
                            return self._rax
                        self._rax = k + 1       # lea rax,[rax+1]
                        dv = self._rd(dst + k, 1, 0x3913C4)
                        if dv is None:
                            return self._rax
                        self.sb(dst + k, dv | sv)
        return dst

    def dist(self, a, b):
        """003A1920 — sqrt(|a-b|^2) -> THUNKF; result in xmm0."""
        x0 = self._rd(a, 4, 0x3A1920)
        if x0 is None:
            return self._rax
        y0 = self._rd(a + 4, 4, 0x3A1924)
        if y0 is None:
            return self._rax
        y1 = self._rd(b + 4, 4, 0x3A1929)
        if y1 is None:
            return self._rax
        x1 = self._rd(b, 4, 0x3A192E)
        if x1 is None:
            return self._rax
        z0 = self._rd(a + 8, 4, 0x3A1932)
        if z0 is None:
            return self._rax
        z1 = self._rd(b + 8, 4, 0x3A1937)
        if z1 is None:
            return self._rax
        dx = _s(u2f(x0), u2f(x1))
        dy = _s(u2f(y0), u2f(y1))
        dz = _s(u2f(z0), u2f(z1))
        d2 = _a(_a(_m(dy, dy), _m(dx, dx)), _m(dz, dz))
        return self.sqrtf(f2u(d2))

    def cpseg(self, out, a, p, b):
        """004691A0 — closest point on seg [a,b] to p.
        t = dot(a-p, a-b)/|a-b|^2; t<0 -> a, t>1 -> b,
        else a + t*(b-a). 16B out, rax = out."""
        bx = self._rd(b, 4, 0x4691A4)
        if bx is None:
            return self._rax
        by = self._rd(b + 4, 4, 0x4691AE)
        if by is None:
            return self._rax
        bz = self._rd(b + 8, 4, 0x4691B9)
        if bz is None:
            return self._rax
        ay = self._rd(a + 4, 4, 0x4691CB)
        if ay is None:
            return self._rax
        ax = self._rd(a, 4, 0x4691DB)
        if ax is None:
            return self._rax
        px = self._rd(p, 4, 0x4691EE)
        if px is None:
            return self._rax
        az = self._rd(a + 8, 4, 0x4691F3)
        if az is None:
            return self._rax
        py = self._rd(p + 4, 4, 0x469205)
        if py is None:
            return self._rax
        pz = self._rd(p + 8, 4, 0x469213)
        if pz is None:
            return self._rax
        ax, ay, az = u2f(ax), u2f(ay), u2f(az)
        bx, by, bz = u2f(bx), u2f(by), u2f(bz)
        px, py, pz = u2f(px), u2f(py), u2f(pz)
        apx, apy, apz = _s(ax, px), _s(ay, py), _s(az, pz)
        abx, aby, abz = _s(ax, bx), _s(ay, by), _s(az, bz)
        dot = _a(_a(_m(apy, aby), _m(apx, abx)), _m(apz, abz))
        l2 = _a(_a(_m(abx, abx), _m(aby, aby)), _m(abz, abz))
        t = _d(dot, l2)
        if not math.isnan(t) and 0.0 > t:
            # movaps xmm0,[rdx] — full 16B endpoint vec
            res = (ax, ay, az, self.mf(a + 0xC))
        elif not math.isnan(t) and t > 1.0:
            res = (bx, by, bz, self.mf(b + 0xC))
        else:
            # t<=1 or unordered (jbe on comiss t,1.0f): mid-lerp
            res = (_a(_m(_s(bx, ax), t), ax),
                   _a(_m(_s(by, ay), t), ay),
                   _a(_m(_s(bz, az), t), az), 0)
        self._rax = out                    # mov rax,rcx
        if not self.mapped(out) or not self.mapped(out + 8):
            # movaps [rcx] — single 16B store (fault size 8)
            a0 = out if not self.mapped(out) else out + 8
            self.faults.append(("memw", a0, 8))
            self.fault_end = 0x4692D2
            return self._rax
        for k, v in enumerate(res):
            self.sf(out + k * 4, v)
        return out

    def trigd(self, edge, cpt):
        """00468580 — trig-table edge helper -> xmm0 float."""
        an = self._rd(edge + 0x18, 4, 0x468584)
        if an is None:
            return self._rax
        frac = _d(u2f(an), self.mf(NEG2PI))
        cx = self._rd(cpt, 4, 0x468598)
        if cx is None:
            return self._rax
        cz = self._rd(cpt + 8, 4, 0x46859C)
        if cz is None:
            return self._rax
        f0 = _m(frac, self.mf(TRIGN))
        f1 = _m(frac, self.mf(TRIGP))
        ex = self._rd(edge, 4, 0x4685B9)
        if ex is None:
            return self._rax
        ez = self._rd(edge + 8, 4, 0x4685BD)
        if ez is None:
            return self._rax
        dx = _s(u2f(cx), u2f(ex))
        dz = _s(u2f(cz), u2f(ez))
        i1 = (0x2000 - _cvtt(f0)) & 0x7FFF
        e10 = self._rd(edge + 0x10, 4, 0x4685CB)
        if e10 is None:
            return self._rax
        i2 = _cvtt(f1) & 0x7FFF
        self._rax = i2            # last eax write = cvttss2si+and
        t1 = self.mf(TRIGT + i1 * 4)
        t2 = self.mf(TRIGT + i2 * 4)
        e14 = self._rd(edge + 0x14, 4, 0x46860F)
        if e14 is None:
            return self._rax
        e10, e14 = u2f(e10), u2f(e14)
        x8 = _d(_a(_m(t2, dz), _m(t1, dx)), e10)
        x7 = _d(_s(_m(t1, dz), _m(t2, dx)), e14)
        d2 = _a(_a(_m(x8, x8), 0.0), _m(x7, x7))
        d = self.sqrtf(f2u(d2))
        eps = struct.unpack(
            "<d", img_rd(self.raw, self.secs, DISTEPS, 8))[0]
        if math.isnan(d) or d <= eps:
            return e10            # comisd jbe: <= OR unordered
        inv = _d(self.mf(CLAMP1), d)
        t8 = _m(_m(inv, x8), e10)
        t7 = _m(_m(inv, x7), e14)
        r2 = _a(_a(_m(t8, t8), 0.0), _m(t7, t7))
        return self.sqrtf(f2u(r2))

    def capt0(self, seg, edge, cbuf):
        """00468D50 — capsule A: point-seg shortcut or CPSEG;
        closest==p1 -> 0; radsum > dist -> 1."""
        p1x = self._rd(seg, 4, 0x468D6B)
        if p1x is None:
            return self._rax
        p2x = self._rd(seg + 0x10, 4, 0x468D72)
        if p2x is None:
            return self._rax
        p1z = self._rd(seg + 8, 4, 0x468D7A)
        if p1z is None:
            return self._rax
        p2z = self._rd(seg + 0x18, 4, 0x468D7F)
        if p2z is None:
            return self._rax
        p1x, p1z = u2f(p1x), u2f(p1z)
        p2x, p2z = u2f(p2x), u2f(p2z)
        if _ueq(p1x, p2x) and _ueq(p1z, p2z):
            ex = self._rd(edge, 4, 0x468D87)
            if ex is None:
                return self._rax
            ez = self._rd(edge + 8, 4, 0x468D8B)
            if ez is None:
                return self._rax
            p1y = self._rd(seg + 4, 4, 0x468D90)
            if p1y is None:
                return self._rax
            ey = self._rd(edge + 4, 4, 0x468D95)
            if ey is None:
                return self._rax
            sr = self._rd(seg + 0x20, 4, 0x468D9A)
            if sr is None:
                return self._rax
            er = self._rd(edge + 0x10, 4, 0x468D9F)
            if er is None:
                return self._rax
            dx = _s(p1x, u2f(ex))
            dz = _s(p1z, u2f(ez))
            dy = _s(u2f(p1y), u2f(ey))
            rad = _a(u2f(sr), u2f(er))
            d2 = _a(_a(_m(dx, dx), _m(dy, dy)), _m(dz, dz))
            return 1 if _seta(rad, self.sqrtf(f2u(d2))) else 0
        self.cpseg(cbuf, seg, edge, seg + 0x10)
        if self.fault_end != RETQ:
            return self._rax
        cv = self._rd(cbuf, 4, 0x468DCD)
        if cv is None:
            return self._rax
        czv = self._rd(cbuf + 8, 4, 0x468DD8)
        if czv is None:
            return self._rax
        cx, cz = u2f(cv), u2f(czv)
        if _ueq(cx, p1x):
            p1z2 = self._rd(seg + 8, 4, 0x468DE2)
            if p1z2 is None:
                return self._rax
            if _ueq(cz, u2f(p1z2)):
                return 0
        ey = self._rd(edge + 4, 4, 0x468DEE)
        if ey is None:
            return self._rax
        ex = self._rd(edge, 4, 0x468DF3)
        if ex is None:
            return self._rax
        cy = self._rd(cbuf + 4, 4, 0x468DF7)
        if cy is None:
            return self._rax
        sr = self._rd(seg + 0x20, 4, 0x468DFD)
        if sr is None:
            return self._rax
        ez = self._rd(edge + 8, 4, 0x468E06)
        if ez is None:
            return self._rax
        er = self._rd(edge + 0x10, 4, 0x468E0B)
        if er is None:
            return self._rax
        rad = _a(u2f(sr), u2f(er))
        dy = _s(u2f(ey), u2f(cy))
        dx = _s(u2f(ex), cx)
        dz = _s(u2f(ez), cz)
        d2 = _a(_a(_m(dx, dx), _m(dy, dy)), _m(dz, dz))
        return 1 if _seta(rad, self.sqrtf(f2u(d2))) else 0

    def capt1(self, seg, edge, cbuf):
        """00468E50 — capsule B: CPSEG first; point-seg skips the
        ==p1 exclusion; TRIGD(edge,closest)+d[seg+0x20] > dist."""
        self.cpseg(cbuf, seg, edge, seg + 0x10)
        if self.fault_end != RETQ:
            return self._rax
        p1x = self._rd(seg, 4, 0x468E7C)
        if p1x is None:
            return self._rax
        p2x = self._rd(seg + 0x10, 4, 0x468E80)
        if p2x is None:
            return self._rax
        cv = self._rd(cbuf, 4, 0x468E8C)
        if cv is None:
            return self._rax
        czv = self._rd(cbuf + 8, 4, 0x468E95)
        if czv is None:
            return self._rax
        p1x, p2x = u2f(p1x), u2f(p2x)
        cx, cz = u2f(cv), u2f(czv)
        point = _ueq(p1x, p2x)
        if point:
            p1z = self._rd(seg + 8, 4, 0x468EA5)
            if p1z is None:
                return self._rax
            p2z = self._rd(seg + 0x18, 4, 0x468EAA)
            if p2z is None:
                return self._rax
            p1z, p2z = u2f(p1z), u2f(p2z)
            point = _ueq(p1z, p2z)
        else:
            p1z = p2z = None
        if not point:
            if _ueq(cx, p1x):
                p1z = self._rd(seg + 8, 4, 0x468EB9)
                if p1z is None:
                    return self._rax
                if _ueq(cz, u2f(p1z)):
                    return 0
        ez = self._rd(edge + 8, 4, 0x468EE3)
        if ez is None:
            return self._rax
        ey = self._rd(edge + 4, 4, 0x468EF2)
        if ey is None:
            return self._rax
        ex = self._rd(edge, 4, 0x468F05)
        if ex is None:
            return self._rax
        cy = self.mf(cbuf + 4)
        tg = self.trigd(edge, cbuf)
        if self.fault_end != RETQ:
            return self._rax
        sr = self._rd(seg + 0x20, 4, 0x468F1C)
        if sr is None:
            return self._rax
        lim = _a(tg, u2f(sr))
        dz = _s(u2f(ez), cz)
        dy = _s(u2f(ey), cy)
        dx = _s(u2f(ex), cx)
        d2 = _a(_a(_m(dx, dx), _m(dy, dy)), _m(dz, dz))
        return 1 if _seta(lim, self.sqrtf(f2u(d2))) else 0

    def capv(self, a, b, rad, p):
        """00469410 — sibling capsule variant: t<0 uses (a-p)^2;
        t>1 uses b; ret (rad+d[r9+0x10])^2 > |closest-p|^2 (x,z)."""
        bz = self._rd(b + 8, 4, 0x469414)
        if bz is None:
            return self._rax
        pr = self._rd(p + 0x10, 4, 0x469421)
        if pr is None:
            return self._rax
        bx = self._rd(b, 4, 0x46942C)
        if bx is None:
            return self._rax
        ay = self._rd(a + 4, 4, 0x469442)
        if ay is None:
            return self._rax
        by = self._rd(b + 4, 4, 0x469452)
        if by is None:
            return self._rax
        py = self._rd(p + 4, 4, 0x469457)
        if py is None:
            return self._rax
        ax = self._rd(a, 4, 0x46945D)
        if ax is None:
            return self._rax
        az = self._rd(a + 8, 4, 0x46946B)
        if az is None:
            return self._rax
        px = self._rd(p, 4, 0x469475)
        if px is None:
            return self._rax
        pz = self._rd(p + 8, 4, 0x46948B)
        if pz is None:
            return self._rax
        ax, ay, az = u2f(ax), u2f(ay), u2f(az)
        bx, by, bz = u2f(bx), u2f(by), u2f(bz)
        px, py, pz = u2f(px), u2f(py), u2f(pz)
        lim2 = _m(_a(rad, u2f(pr)), _a(rad, u2f(pr)))
        apx, apy, apz = _s(ax, px), _s(ay, py), _s(az, pz)
        abx, aby, abz = _s(ax, bx), _s(ay, by), _s(az, bz)
        dot = _a(_a(_m(apy, aby), _m(apx, abx)), _m(apz, abz))
        l2 = _a(_a(_m(aby, aby), _m(abx, abx)), _m(abz, abz))
        t = _d(dot, l2)
        if not math.isnan(t) and 0.0 > t:
            d2 = _a(_m(apz, apz), _m(apx, apx))
            return 1 if _seta(lim2, d2) else 0
        if math.isnan(t) or t <= 1.0:
            # comiss t,1.0f; ja skips lerp only on ordered t>1
            cx = _a(_m(_s(bx, ax), t), ax)
            cz = _a(_m(_s(bz, az), t), az)
        else:
            cx, cz = bx, bz
        dz_ = _s(cz, pz)
        dx_ = _s(cx, px)
        d2 = _a(_m(dz_, dz_), _m(dx_, dx_))
        return 1 if _seta(lim2, d2) else 0

    def rdec(self, idx, out, vsp):
        """0032A6E0 — nav-record decode. rec = q[NRO+0x1a0] +
        sx32(idx)*16; vtx = q[NRO+0x188] + sx16(w[rec+2])*64."""
        nro = self.mq(NRROOT)
        self._rax = nro & 0xFFFFFFFFFFFFFFFF  # mov rax,[rip]
        i = idx & 0xFFFFFFFF
        if i >= 0x80000000:
            i -= 0x100000000
        rp = self._rd(nro + 0x1A0, 8, 0x32A6F7)
        if rp is None:
            return self._rax
        rec = (rp + i * 16) & 0xFFFFFFFFFFFFFFFF
        vi = self._rd(rec + 2, 2, 0x32A6FE)
        if vi is None:
            return self._rax
        if vi >= 0x8000:
            vi -= 0x10000
        vp = self._rd(nro + 0x188, 8, 0x32A707)
        if vp is None:
            return self._rax
        vtx = (vp + vi * 64) & 0xFFFFFFFFFFFFFFFF
        iv = []
        for k, site in enumerate((0x32A70E, 0x32A717, 0x32A720)):
            v = self._rd(rec + 4 + k * 2, 2, site)
            if v is None:
                return self._rax
            sv16 = v - 0x10000 if v >= 0x8000 else v
            self._rax = sv16 & 0xFFFFFFFF     # movsx eax
            self.sd(vsp + 0x20 + k * 4, sv16 & 0xFFFFFFFF)
            iv.append(sv16)
        iv.append(self.md(vsp + 0x2C))        # stale stack lane
        scl = [self.mf(SCLV + k * 4) for k in range(4)]
        sv = [_m(float(iv[k]), scl[k]) for k in range(4)]
        if not self.mapped(RSCRATCH):         # movdqu scratch
            self.faults.append(("memw", RSCRATCH, 16))
            self.fault_end = 0x32A735
            return self._rax
        for k in range(4):
            self.sf(RSCRATCH + k * 4, sv[k])
        f30 = self._rd(vtx + 0x30, 4, 0x32A73D)
        if f30 is None:
            return self._rax
        self._rax = f30                       # mov eax
        if not self._sd_flt(out, f30, 0x32A740):
            return self._rax
        f34 = self._rd(vtx + 0x34, 4, 0x32A745)
        if f34 is None:
            return self._rax
        self._rax = f34
        if not self._sd_flt(out + 4, f34, 0x32A748):
            return self._rax
        f38 = self._rd(vtx + 0x38, 4, 0x32A74B)
        if f38 is None:
            return self._rax
        self._rax = f38
        if not self._sf_flt(out + 0xC, sv[0], 0x32A752):
            return self._rax
        if not self._sf_flt(out + 0x10, sv[1], 0x32A757):
            return self._rax
        if not self._sd_flt(out + 8, f38, 0x32A75C):
            return self._rax
        f20 = self._rd(vtx + 0x20, 4, 0x32A75F)
        if f20 is None:
            return self._rax
        f28 = self._rd(vtx + 0x28, 4, 0x32A764)
        if f28 is None:
            return self._rax
        if not self._sf_flt(out + 0x14, self.at2(f28, f20),
                            0x32A76E):
            return self._rax
        return out

    def lquery(self, p1, p2, rad_u, vsp):
        """00391410 — segment LOS query over the wall-record grid.
        Frame rsp = vsp-0x128; seg v1 at +0x40=vsp-0xE8, v2 +0x50=
        vsp-0xD8, tmp +0x20=vsp-0x108, tmp2 +0x30=vsp-0xF8, rec vec
        +0x70=vsp-0xB8, rdec out rbp-0x70=vsp-0x98, rad rbp-0x80=
        vsp-0xA8. CAPT scratch cbuf = vsp-0x160."""
        root = self.mq(ROOTCELL)
        self._rax = root
        if root == 0:
            return 0
        csz = self.mf(LCSZ)
        epsx = self.mf(LEPSX)
        epsz = self.mf(LEPSZ)
        rad = u2f(rad_u)
        p1z = self._rd(p1 + 8, 4, 0x39145C)
        if p1z is None:
            return self._rax
        p2z = self._rd(p2 + 8, 4, 0x391461)
        if p2z is None:
            return self._rax
        p2x = self._rd(p2, 4, 0x391497)
        if p2x is None:
            return self._rax
        p1x = self._rd(p1, 4, 0x3914AD)
        if p1x is None:
            return self._rax
        p1x, p2x, p1z, p2z = u2f(p1x), u2f(p2x), u2f(p1z), u2f(p2z)
        z1 = _maxss(p1z, p2z)
        z0 = _minss(p1z, p2z)
        x1 = _maxss(p1x, p2x)
        x0 = _minss(p1x, p2x)
        zhi = _cvtt(_d(_s(_a(z1, rad), epsz), csz))
        zlo = _cvtt(_d(_s(_s(z0, rad), epsz), csz))
        xhi = _cvtt(_d(_s(_a(x1, rad), epsx), csz))
        xlo = _cvtt(_d(_s(_s(x0, rad), epsx), csz))
        self._rax = self.bmask(xlo, zlo, xhi, zhi)
        if self.fault_end != RETQ:
            return self._rax
        S1 = (vsp - 0xE8) & 0xFFFFFFFFFFFFFFFF
        S2 = (vsp - 0xD8) & 0xFFFFFFFFFFFFFFFF
        TMP = (vsp - 0x108) & 0xFFFFFFFFFFFFFFFF
        TMP2 = (vsp - 0xF8) & 0xFFFFFFFFFFFFFFFF
        V70 = (vsp - 0xB8) & 0xFFFFFFFFFFFFFFFF
        RBP70 = (vsp - 0x98) & 0xFFFFFFFFFFFFFFFF
        RBP80 = (vsp - 0xA8) & 0xFFFFFFFFFFFFFFFF
        CBUF = (vsp - 0x160) & 0xFFFFFFFFFFFFFFFF
        # seg vecs {x,0,z,uninit} — radius at S2+0x10 = rsp+0x60
        self.sf(S1, p1x)
        self.sd(S1 + 4, 0)
        self.sf(S1 + 8, p1z)
        self.sf(S2, p2x)
        self.sd(S2 + 4, 0)
        self.sf(S2 + 8, p2z)
        self.sf(S2 + 0x10, rad)
        self.dist(S1, S2)                    # dead call, traced
        if self.fault_end != RETQ:
            return self._rax
        for i in range(160):
            msk = self.mq(LBMSK)
            self._rax = msk               # mov rax,[rip+LBMSK]
            bit = self._rd(msk + 0x10 + i // 8, 1, 0x391579)
            if bit is None:
                return self._rax
            self._rax = 1                 # mov eax,1 (shl src)
            if not (bit & (1 << (i % 8))):
                continue
            if i < 0x20:
                po = self._rd(root + 0x28, 4, 0x391597)
                if po is None:
                    return self._rax
                rec = (self.base(po) + i * 0x20) & 0xFFFFFFFFFFFFFFFF
                self._rax = rec               # add rax, rdi
                t = self._rd(rec, 2, 0x3915A3)
                if t is None:
                    return self._rax
                if t == 0:
                    x = self._rd(rec + 4, 4, 0x3915F9)
                    if x is None:
                        return self._rax
                    z = self._rd(rec + 8, 4, 0x391616)
                    if z is None:
                        return self._rax
                    rr = self._rd(rec + 0xC, 4, 0x391629)
                    if rr is None:
                        return self._rax
                    self.sf(V70, u2f(x))
                    self.sd(V70 + 4, 0)
                    self.sf(V70 + 8, u2f(z))
                    self.sf(V70 + 0xC, 1.0)
                    self.sd(RBP80, rr)       # rdx+0x10 = rsp+0x80
                    r = self.capt0(S1, V70, CBUF)
                    if self.fault_end != RETQ:
                        return self._rax
                elif t == 1:
                    x = self._rd(rec + 4, 4, 0x3915B3)
                    if x is None:
                        return self._rax
                    z = self._rd(rec + 8, 4, 0x3915C6)
                    if z is None:
                        return self._rax
                    x2 = self._rd(rec + 0xC, 4, 0x3915D9)
                    if x2 is None:
                        return self._rax
                    z2 = self._rd(rec + 0x10, 4, 0x3915E4)
                    if z2 is None:
                        return self._rax
                    an = self._rd(rec + 0x14, 4, 0x3915EF)
                    if an is None:
                        return self._rax
                    self.sf(TMP, u2f(x))
                    self.sd(TMP + 4, 0)
                    self.sf(TMP + 8, u2f(z))
                    self.sf(TMP + 0xC, 1.0)
                    self.sf(TMP2, u2f(x2))
                    self.sf(TMP2 + 4, u2f(z2))
                    self.sf(TMP2 + 8, u2f(an))
                    r = self.capt1(S1, TMP, CBUF)
                    if self.fault_end != RETQ:
                        return self._rax
                else:
                    continue
            else:
                self.rdec(i - 0x20, RBP70,
                          (vsp - 0x168) & 0xFFFFFFFFFFFFFFFF)
                if self.fault_end != RETQ:
                    return self._rax
                x = self.mf(RBP70)
                z = self.mf(RBP70 + 8)
                x2 = self.mf(RBP70 + 0xC)
                z2 = self.mf(RBP70 + 0x10)
                an = self.mf(RBP70 + 0x14)
                self.sf(TMP, x)
                self.sd(TMP + 4, 0)
                self.sf(TMP + 8, z)
                self.sf(TMP + 0xC, 1.0)
                self.sf(TMP2, x2)
                self.sf(TMP2 + 4, z2)
                self.sf(TMP2 + 8, an)
                r = self.capt1(S1, TMP, CBUF)
                if self.fault_end != RETQ:
                    return self._rax
            if r != 0:
                return 1
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
        elif entry == LQUERY:
            xmm2 = step[6] if len(step) > 6 else 0
            m.rets.append(m.lquery(rcx, rdx, xmm2, STACK + 0x80000))
        elif entry == BMASK:
            m.rets.append(m.bmask(rcx, rdx, r8, r9))
        elif entry == DIST:
            m.dist(rcx, rdx)
            m.rets.append(m._rax)
        elif entry == CAPT0:
            m.rets.append(m.capt0(rcx, rdx, SEGV + 0x100))
        elif entry == CAPT1:
            m.rets.append(m.capt1(rcx, rdx, SEGV + 0x100))
        elif entry == CPSEG:
            m.cpseg(rcx, rdx, r9, r8)   # native: rdx=a r8=b r9=p
            m.rets.append(m._rax)
        elif entry == TRIGD:
            m.trigd(rcx, rdx)
            m.rets.append(m._rax)
        elif entry == CAPV:
            xmm2 = step[6] if len(step) > 6 else 0
            m.rets.append(m.capv(rcx, rdx, u2f(xmm2 & 0xFFFFFFFF),
                                 r9))
        elif entry == RDEC:
            m.rdec(rcx, rdx, STACK + 0x80000 - 0x40)
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
    # ---------- EXP-133 nav-LOS cases ----------
    SEG = SEGV
    EDG = SEGV + 0x30
    OUTB = SEGV + 0x100
    OUTB2 = SEGV + 0x200
    W_BMSK = [(BMSKA, 0x30)]
    W_RBP70 = [(STACK + 0x80000 - 0x98, 0x18)]
    # --- LQUERY 00391410 (rcx=p1, rdx=p2, xmm2=rad) ---
    # grid 8x8 cell 4.0 eps .5 -> (1,1)-(3,3) r.5 covers cell(0,0)
    C["los-null"] = {"rootp": 0,
                     "steps": [(LQUERY, P1, P2, 0, 0, 0, f2u(0.5))]}
    C["los-empty"] = {"steps": [(LQUERY, P1, P2, 0, 0, 0,
                                 f2u(0.5))]}
    # type-0 wall rec (2,2) r.1 on the segment -> capt0 blocks
    C["los-t0-block"] = {"cflags": [1] + [0] * 0xFF,
                         "lsrc": {0: [0] * 0x10 + [1]},
                         "wrecs": [[0, 2.0, 2.0, 0.1]],
                         "steps": [(LQUERY, P1, P2, 0, 0, 0,
                                    f2u(0.5))],
                         "watch": W_BMSK}
    # type-0 wall rec far away -> capt0 miss -> exhaust -> 0
    C["los-t0-miss"] = {"cflags": [1] + [0] * 0xFF,
                        "lsrc": {0: [0] * 0x10 + [1]},
                        "wrecs": [[0, 20.0, 20.0, 0.1]],
                        "steps": [(LQUERY, P1, P2, 0, 0, 0,
                                   f2u(0.5))],
                        "watch": W_BMSK}
    # type-1 wall edge (2,2) e10=1 -> capt1 blocks
    C["los-t1-block"] = {"cflags": [1] + [0] * 0xFF,
                         "lsrc": {0: [0] * 0x10 + [1]},
                         "wrecs": [[1, 2.0, 2.0, 1.0, 4.0, 0.0]],
                         "steps": [(LQUERY, P1, P2, 0, 0, 0,
                                    f2u(0.5))],
                         "watch": W_BMSK}
    # type-5 record -> skipped -> 0
    C["los-tskip"] = {"cflags": [1] + [0] * 0xFF,
                      "lsrc": {0: [0] * 0x10 + [1]},
                      "wrecs": [[5, 2.0, 2.0, 0.1]],
                      "steps": [(LQUERY, P1, P2, 0, 0, 0,
                                 f2u(0.5))]}
    # bit 0x20 -> RDEC nav decode -> capt1 blocks
    C["los-nav"] = {"cflags": [1] + [0] * 0xFF,
                    "lsrc": {0: [0] * 0x14 + [1]},
                    "recs": [[0, 4096, 0, 8192]],
                    "vtxs": [[1.0, 0.0, 1.0, 0.0,
                              2.0, 0.5, 2.0, 0.0]],
                    "steps": [(LQUERY, P1, P2, 0, 0, 0,
                               f2u(0.5))],
                    "watch": W_RBP70}
    # bit0 miss + bit0x20 block -> iterates both decode paths
    C["los-multi"] = {"cflags": [1] + [0] * 0xFF,
                      "lsrc": {0: [0] * 0x10 + [1, 0, 0, 0, 1]},
                      "wrecs": [[0, 20.0, 20.0, 0.1]],
                      "recs": [[0, 4096, 0, 8192]],
                      "vtxs": [[1.0, 0.0, 1.0, 0.0,
                                2.0, 0.5, 2.0, 0.0]],
                      "steps": [(LQUERY, P1, P2, 0, 0, 0,
                                 f2u(0.5))],
                      "watch": W_RBP70}
    # nav edge far -> capt1 miss -> 0
    C["los-nav-miss"] = {"cflags": [1] + [0] * 0xFF,
                         "lsrc": {0: [0] * 0x14 + [1]},
                         "recs": [[0, 4096, 0, 8192]],
                         "vtxs": [[1.0, 0.0, 1.0, 0.0,
                                   20.0, 0.5, 20.0, 0.0]],
                         "steps": [(LQUERY, P1, P2, 0, 0, 0,
                                    f2u(0.5))],
                         "watch": W_RBP70}
    # off-grid segment -> clamps to whole grid; flag0 -> block
    C["los-clamp"] = {"p1x": -10.0, "p1z": -10.0,
                      "p2x": 30.0, "p2z": 30.0,
                      "cflags": [1] + [0] * 0xFF,
                      "lsrc": {0: [0] * 0x10 + [1]},
                      "wrecs": [[0, 2.0, 2.0, 0.1]],
                      "steps": [(LQUERY, P1, P2, 0, 0, 0,
                                 f2u(1.0))],
                      "watch": W_BMSK}
    # mask bit8 (rec8) -> column-wrap boundary coverage
    C["los-bit8"] = {"cflags": [1] + [0] * 0xFF,
                     "lsrc": {0: [0] * 0x11 + [1]},
                     "wrecs": [[0, 0.0, 0.0, 0.0]] * 8 +
                              [[0, 2.0, 2.0, 0.1]],
                     "steps": [(LQUERY, P1, P2, 0, 0, 0,
                                f2u(0.5))],
                     "watch": W_BMSK}
    # mask bit1 (rec1) -> shl bit position coverage
    C["los-bit1"] = {"cflags": [1] + [0] * 0xFF,
                     "lsrc": {0: [0] * 0x10 + [2]},
                     "wrecs": [[0, 0.0, 0.0, 0.0],
                               [0, 2.0, 2.0, 0.1]],
                     "steps": [(LQUERY, P1, P2, 0, 0, 0,
                                f2u(0.5))],
                     "watch": W_BMSK}
    # wide z-range: p2z=9 -> rows 0..2; flag row2 only
    C["los-zwide"] = {"p2z": 9.0,
                      "cflags": [0] * 16 + [1] + [0] * 0xEF,
                      "lsrc": {16: [0] * 0x10 + [1]},
                      "wrecs": [[0, 2.0, 2.0, 1.0]],
                      "steps": [(LQUERY, P1, P2, 0, 0, 0,
                                 f2u(0.5))],
                      "watch": W_BMSK}
    # flag at cell(2,0)=16: inside mutant-expanded zhi (mulss),
    # outside native zhi=0
    C["los-far3"] = {"cflags": [0] * 16 + [1] + [0] * 0xEF,
                     "lsrc": {16: [0] * 0x10 + [1]},
                     "wrecs": [[0, 2.0, 2.0, 0.1]],
                     "steps": [(LQUERY, P1, P2, 0, 0, 0,
                                f2u(0.5))],
                     "watch": W_BMSK}
    # null root + flag set: mutant je->jne proceeds into a wild
    # d[root+0x28] read
    C["los-null-f"] = {"rootp": 0,
                       "cflags": [1] + [0] * 0xFF,
                       "lsrc": {0: [0] * 0x10 + [1]},
                       "wrecs": [[0, 2.0, 2.0, 0.1]],
                       "steps": [(LQUERY, P1, P2, 0, 0, 0,
                                  f2u(0.5))]}
    # edge x beyond p2 -> closest=p2 (dx!=0); native lim < dist
    # but a mutant x7*=e14 inflates it (m-trg-div)
    C["capt1-divlim"] = {"segv": [0, 0, 0, 0, 4, 0, 0, 0, 1.0,
                                 0, 0, 0, 4.5, 0, 1.5, 0,
                                 1.0, 0.5, 0.0] + [0] * 0xE9,
                         "steps": [(CAPT1, SEG, EDG)]}
    # faults
    C["los-badp1"] = {"steps": [(LQUERY, 0xFFFFFFF0, P2, 0, 0,
                                 0, f2u(0.5))]}
    C["los-badroot"] = {"rootp": 0xFFFFFFF0,
                        "cflags": [1] + [0] * 0xFF,
                        "lsrc": {0: [0] * 0x10 + [1]},
                        "wrecs": [[0, 2.0, 2.0, 0.1]],
                        "steps": [(LQUERY, P1, P2, 0, 0, 0,
                                   f2u(0.5))]}
    C["los-badcflg"] = {"lcflg": 0xFFFFFFF0,
                        "steps": [(LQUERY, P1, P2, 0, 0, 0,
                                   f2u(0.5))]}
    C["los-badrec"] = {"root_0x28": 0xFFFF0000,
                       "cflags": [1] + [0] * 0xFF,
                       "lsrc": {0: [0] * 0x10 + [1]},
                       "steps": [(LQUERY, P1, P2, 0, 0, 0,
                                  f2u(0.5))]}
    C["los-badnroot"] = {"nroot": 0,
                         "cflags": [1] + [0] * 0xFF,
                         "lsrc": {0: [0] * 0x14 + [1]},
                         "steps": [(LQUERY, P1, P2, 0, 0, 0,
                                    f2u(0.5))]}
    C["los-badnav"] = {"recp": 0,
                       "cflags": [1] + [0] * 0xFF,
                       "lsrc": {0: [0] * 0x14 + [1]},
                       "steps": [(LQUERY, P1, P2, 0, 0, 0,
                                  f2u(0.5))]}
    # --- BMASK 003912E0 (ecx=c0 edx=r0 r8=c1 r9=r1) ---
    C["bmask-1"] = {"cflags": [1] + [0] * 0xFF,
                    "lsrc": {0: [0x27] + [0x55] * 0x2F},
                    "steps": [(BMASK, 0, 0, 0, 0)],
                    "watch": W_BMSK}
    C["bmask-range"] = {"cflags": [1] + [0] * 8 + [1] +
                        [0] * 7 + [1] + [0] * 0xEE,
                        "lsrc": {0: [1], 9: [2], 17: [4]},
                        "steps": [(BMASK, 0, 0, 1, 2)],
                        "watch": W_BMSK}
    C["bmask-clamp"] = {"cflags": [1] + [0] * 62 +
                        [1] + [0] * 0xC0,
                        "lsrc": {0: [1], 63: [8]},
                        "steps": [(BMASK, -3, -2, 99, 50)],
                        "watch": W_BMSK}
    C["bmask-invrow"] = {"cflags": [1] + [0] * 0xFF,
                         "lsrc": {0: [9]},
                         "steps": [(BMASK, 0, 2, 7, 0)],
                         "watch": W_BMSK}
    C["bmask-rlen4"] = {"lrlen": 4,
                        "cflags": [1] + [0] * 0xFF,
                        "lsrc": {0: [9, 0, 0, 0]},
                        "steps": [(BMASK, 0, 0, 0, 0)],
                        "watch": W_BMSK}
    C["bmask-flip"] = {"cflags": [0, 1] + [0] * 0xFE,
                       "lsrc": {0: [9], 1: [3]},
                       "steps": [(BMASK, 0, 0, 1, 0)],
                       "watch": W_BMSK}
    # c0=0x100000: native clamps to w-1=7 and reads flag7 -> OR;
    # cmovl mutant keeps 0x100000 > c1 -> col guard skips -> dst 0
    C["bmask-wild"] = {"cflags": [0] * 7 + [1] + [0] * 0xF8,
                       "lsrc": {7: [0] * 0x10 + [0xA5]},
                       "steps": [(BMASK, 0x100000, 0,
                                  0x100000, 0)],
                       "watch": W_BMSK}
    C["bmask-badcflg"] = {"lcflg": 0xFFFFFFF0,
                          "steps": [(BMASK, 0, 0, 0, 0)]}
    C["bmask-badlsrc"] = {"llsrc": 0xFFFFFFF0,
                          "cflags": [1] + [0] * 0xFF,
                          "steps": [(BMASK, 0, 0, 0, 0)]}
    # --- DIST 003A1920 (rcx=a, rdx=b) ---
    C["dist-1"] = {"steps": [(DIST, P1, P2)]}
    C["dist-badptr"] = {"steps": [(DIST, 0xFFFFFFF0, P2)]}
    # --- CPSEG 004691A0 (rcx=out rdx=a r8=b r9=p) ---
    # segv: p1v4,p2v4,srad,pad3, edgev4, e10/prad,e14,ang,pad
    C["cpseg-mid"] = {"segv": [0, 0, 0, 0, 10, 0, 0, 0,
                              0, 0, 0, 0, 5, 0, 2, 0] +
                              [0] * 0xF0,
                      "steps": [(CPSEG, OUTB, SEG, SEG + 0x10,
                                 EDG)],
                      "watch": [(OUTB, 0x10)]}
    C["cpseg-pre"] = {"segv": [0, 0, 0, 0, 10, 0, 0, 0,
                              0, 0, 0, 0, -3, 0, 0, 0] +
                              [0] * 0xF0,
                      "steps": [(CPSEG, OUTB, SEG, SEG + 0x10,
                                 EDG)],
                      "watch": [(OUTB, 0x10)]}
    C["cpseg-post"] = {"segv": [0, 0, 0, 0, 10, 0, 0, 0,
                               0, 0, 0, 0, 20, 0, 0, 0] +
                               [0] * 0xF0,
                       "steps": [(CPSEG, OUTB, SEG, SEG + 0x10,
                                  EDG)],
                       "watch": [(OUTB, 0x10)]}
    C["cpseg-degen"] = {"segv": [0, 0, 0, 0, 0, 0, 0, 0,
                                0, 0, 0, 0, 5, 0, 2, 0] +
                                [0] * 0xF0,
                        "steps": [(CPSEG, OUTB, SEG, SEG + 0x10,
                                   EDG)],
                        "watch": [(OUTB, 0x10)]}
    C["cpseg-nanp"] = {"segv": [0, 0, 0, 0, 10, 0, 0, 0,
                               0, 0, 0, 0, 5, float("nan"), 2,
                               0] + [0] * 0xF0,
                       "steps": [(CPSEG, OUTB, SEG, SEG + 0x10,
                                  EDG)],
                       "watch": [(OUTB, 0x10)]}
    C["cpseg-badout"] = {"segv": [0, 0, 0, 0, 10, 0, 0, 0,
                                 0, 0, 0, 0, 5, 0, 2, 0] +
                                 [0] * 0xF0,
                         "steps": [(CPSEG, 0xFFFFFFF0, SEG,
                                    SEG + 0x10, EDG)]}
    C["cpseg-badb"] = {"steps": [(CPSEG, OUTB, SEG,
                                 0xFFFFFFF0, EDG)]}
    # --- TRIGD 00468580 (rcx=edge, rdx=cpt) ---
    C["trigd-eps"] = {"segv": [2, 0, 2, 0] + [0] * 8 +
                      [2, 0, 2, 0, 1.0, 1.0, 0.0] + [0] * 0xE5,
                      "steps": [(TRIGD, EDG, SEG)]}
    C["trigd-1"] = {"segv": [2, 0, 3.5, 0] + [0] * 8 +
                    [2, 0, 2, 0, 1.0, 1.0, 0.0] + [0] * 0xE5,
                    "steps": [(TRIGD, EDG, SEG)]}
    C["trigd-nan"] = {"segv": [2, 0, 3.5, 0] + [0] * 8 +
                      [2, 0, 2, 0, 1.0, 1.0, float("nan")] +
                      [0] * 0xE5,
                      "steps": [(TRIGD, EDG, SEG)]}
    C["trigd-badptr"] = {"steps": [(TRIGD, 0xFFFFFFF0, SEG)]}
    # --- CAPT0 00468D50 (rcx=seg, rdx=edge) ---
    C["capt0-block"] = {"segv": [0, 0, 0, 0, 4, 0, 0, 0, 1.0,
                                0, 0, 0, 2, 0, 1.5, 0, 0.6] +
                                [0] * 0xEB,
                        "steps": [(CAPT0, SEG, EDG)]}
    C["capt0-miss"] = {"segv": [0, 0, 0, 0, 4, 0, 0, 0, 1.0,
                               0, 0, 0, 2, 0, 3.0, 0, 0.6] +
                               [0] * 0xEB,
                       "steps": [(CAPT0, SEG, EDG)]}
    C["capt0-degen"] = {"segv": [0, 0, 0, 0, 0, 0, 0, 0, 1.0,
                                0, 0, 0, 0, 0, 0.5, 0, 0.6] +
                                [0] * 0xEB,
                        "steps": [(CAPT0, SEG, EDG)]}
    C["capt0-p1eq"] = {"segv": [0, 0, 0, 0, 4, 0, 0, 0, 1.0,
                               0, 0, 0, -1, 0, 0, 0, 0.6] +
                               [0] * 0xEB,
                       "steps": [(CAPT0, SEG, EDG)]}
    C["capt0-nan"] = {"segv": [0, 0, 0, 0, 4, 0, 0, 0, 1.0,
                              0, 0, 0, 2, 0, 1.5, 0,
                              float("nan")] + [0] * 0xEB,
                      "steps": [(CAPT0, SEG, EDG)]}
    C["capt0-badedge"] = {"segv": [0, 0, 0, 0, 4, 0, 0, 0,
                                   1.0] + [0] * 0xF3,
                          "steps": [(CAPT0, SEG,
                                     0xFFFFFFF0)]}
    # --- CAPT1 00468E50 (rcx=seg, rdx=edge) ---
    C["capt1-block"] = {"segv": [0, 0, 0, 0, 4, 0, 0, 0, 1.0,
                                0, 0, 0, 2, 0, 1.5, 0,
                                1.0, 1.0, 0.0] + [0] * 0xE9,
                        "steps": [(CAPT1, SEG, EDG)]}
    C["capt1-miss"] = {"segv": [0, 0, 0, 0, 4, 0, 0, 0, 1.0,
                               0, 0, 0, 2, 0, 5.0, 0,
                               1.0, 1.0, 0.0] + [0] * 0xE9,
                       "steps": [(CAPT1, SEG, EDG)]}
    # edge pt on the segment -> closest==edge -> TRIGD eps path
    C["capt1-eps"] = {"segv": [0, 0, 0, 0, 4, 0, 0, 0, 0.5,
                              0, 0, 0, 2, 0, 0, 0,
                              0.01, 1.0, 0.0] + [0] * 0xE9,
                      "steps": [(CAPT1, SEG, EDG)]}
    C["capt1-degen"] = {"segv": [0, 0, 0, 0, 0, 0, 0, 0, 1.0,
                                0, 0, 0, 0, 0, 0.5, 0,
                                1.0, 1.0, 0.0] + [0] * 0xE9,
                        "steps": [(CAPT1, SEG, EDG)]}
    C["capt1-p1eq"] = {"segv": [0, 0, 0, 0, 4, 0, 0, 0, 1.0,
                               0, 0, 0, -1, 0, 0, 0,
                               1.0, 1.0, 0.0] + [0] * 0xE9,
                       "steps": [(CAPT1, SEG, EDG)]}
    C["capt1-badedge"] = {"segv": [0, 0, 0, 0, 4, 0, 0, 0,
                                   1.0] + [0] * 0xF3,
                          "steps": [(CAPT1, SEG,
                                     0xFFFFFFF0)]}
    # --- CAPV 00469410 (rcx=a rdx=b r9=p xmm2=rad) ---
    C["capv-block"] = {"segv": [0, 0, 0, 0, 4, 0, 0, 0, 0,
                               0, 0, 0, 2, 0, 1.0, 0, 0.6] +
                               [0] * 0xEB,
                       "steps": [(CAPV, SEG, SEG + 0x10, 0,
                                  EDG, 0, f2u(1.0))]}
    C["capv-miss"] = {"segv": [0, 0, 0, 0, 4, 0, 0, 0, 0,
                              0, 0, 0, 2, 0, 3.0, 0, 0.6] +
                              [0] * 0xEB,
                      "steps": [(CAPV, SEG, SEG + 0x10, 0,
                                 EDG, 0, f2u(1.0))]}
    C["capv-pre"] = {"segv": [0, 0, 0, 0, 4, 0, 0, 0, 0,
                             0, 0, 0, -1, 0, 0, 0, 0.6] +
                             [0] * 0xEB,
                     "steps": [(CAPV, SEG, SEG + 0x10, 0,
                                EDG, 0, f2u(1.0))]}
    # t<0 with small lim: native early-d2 > lim^2 -> 0; a lerp
    # would land closest on p -> used by m-capv-t0
    C["capv-pre2"] = {"segv": [0, 0, 0, 0, 4, 0, 0, 0, 0,
                              0, 0, 0, -1, 0, 1.0, 0, 0.1] +
                              [0] * 0xEB,
                      "steps": [(CAPV, SEG, SEG + 0x10, 0,
                                 EDG, 0, f2u(1.0))]}
    C["capv-post"] = {"segv": [0, 0, 0, 0, 4, 0, 0, 0, 0,
                              0, 0, 0, 10, 0, 0, 0, 0.6] +
                              [0] * 0xEB,
                      "steps": [(CAPV, SEG, SEG + 0x10, 0,
                                 EDG, 0, f2u(1.0))]}
    C["capv-nan"] = {"segv": [0, 0, 0, 0, 4, 0, 0, 0, 0,
                             0, 0, 0, float("nan"), 0, 1.0,
                             0, 0.6] + [0] * 0xEB,
                     "steps": [(CAPV, SEG, SEG + 0x10, 0,
                                EDG, 0, f2u(1.0))]}
    C["capv-badp"] = {"steps": [(CAPV, SEG, SEG + 0x10, 0,
                                0xFFFFFFF0, 0, f2u(1.0))]}
    # --- RDEC 0032A6E0 (ecx=idx, rdx=out) ---
    C["rdec-1"] = {"recs": [[0, 0, 0, 0], [1, 4096, -2048,
                                          8192]],
                   "vtxs": [[1.0, 0.0, 1.0, 0.0,
                             2.0, 0.5, 2.0, 0.0],
                            [3.0, 0.0, 4.0, 0.0,
                             5.0, 1.5, 6.0, 0.0]],
                   "steps": [(RDEC, 1, OUTB2)],
                   "watch": [(OUTB2, 0x18)]}
    C["rdec-neg"] = {"steps": [(RDEC,
                               (-0x2000) & 0xFFFFFFFFFFFFFFFF,
                               OUTB2)]}
    C["rdec-noroot"] = {"nroot": 0,
                        "steps": [(RDEC, 1, OUTB2)]}
    C["rdec-badvtx"] = {"recs": [[0x4000, 0, 0, 0]],
                        "steps": [(RDEC, 0, OUTB2)]}
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
    # ---------- EXP-133 nav-LOS ----------
    # LQUERY 00391410
    ("m-los-nullje", "los-null-f",   0x39144F, 0x84, 0x85),  # null je -> jne
    ("m-los-maxss",  "los-zwide",    0x391471, 0x5F, 0x5D),  # maxss -> minss
    ("m-los-divss",  "los-far3",     0x3914F4, 0x5E, 0x59),  # divss -> mulss
    ("m-los-shl",    "los-bit1",     0x391584, 0xE0, 0xE8),  # shl -> shr
    ("m-los-cmp32",  "los-nav",      0x391590, 0x20, 0x21),  # i>=0x20 -> 0x21
    ("m-los-je0",    "los-t0-block", 0x3915A8, 0x74, 0x75),  # type0 je -> jne
    ("m-los-cmp1",   "los-t1-block", 0x3915AC, 0x01, 0x02),  # type cmp 1 -> 2
    ("m-los-r28",    "los-t0-block", 0x39159A, 0x28, 0x2C),  # root+0x28->+0x2C
    ("m-los-jne",    "los-t0-block", 0x39169E, 0x75, 0x74),  # ret1 jne -> je
    ("m-los-cmp8",   "los-bit8",     0x3916A4, 0x08, 0x09),  # col wrap 8 -> 9
    ("m-los-lea50",  "los-t0-block", 0x39153A, 0x50, 0x60),  # dist arg +0x50
    # BMASK 003912E0
    ("m-bm-flgje",   "bmask-flip",   0x391398, 0x74, 0x75),  # flag0 je -> jne
    ("m-bm-imul",    "bmask-range",  0x39139D, 0xC2, 0xC0),  # *rlen -> *eax
    ("m-bm-jl",      "bmask-1",      0x3913D1, 0x7C, 0x7D),  # copy jl -> jge
    ("m-bm-cmovl",   "bmask-wild",   0x391329, 0x4F, 0x4C),  # cmovg -> cmovl
    # DIST 003A1920
    ("m-dist-sub",   "dist-1",       0x3A194A, 0x58, 0x5C),  # addss -> subss
    # CPSEG 004691A0
    ("m-cps-div",    "cpseg-mid",    0x46924E, 0x5E, 0x59),  # divss -> mulss
    ("m-cps-jbe0",   "cpseg-pre",    0x469254, 0x76, 0x77),  # t<0 jbe -> ja
    ("m-cps-jbe1",   "cpseg-post",   0x469263, 0x76, 0x77),  # t<=1 jbe -> ja
    # TRIGD 00468580
    ("m-trg-jbe",    "capt1-eps",    0x468666, 0x76, 0x77),  # eps jbe -> ja
    ("m-trg-div",    "capt1-divlim", 0x468637, 0x5E, 0x59),  # x7 /= e14 -> *
    # CAPT0 00468D50
    ("m-c0-seta",    "capt0-block",  0x468E33, 0x97, 0x96),  # seta -> setbe
    ("m-c0-jnex",    "capt0-block",  0x468D78, 0x75, 0x74),  # x-eq jne -> je
    ("m-c0-jnecx",   "capt0-p1eq",   0x468DE0, 0x75, 0x74),  # cx-eq jne -> je
    # CAPT1 00468E50
    ("m-c1-jnex",    "capt1-p1eq",   0x468EB7, 0x75, 0x74),  # cx-eq jne -> je
    ("m-c1-seta",    "capt1-block",  0x468F61, 0x97, 0x96),  # seta -> setbe
    # CAPV 00469410
    ("m-cv-jbe0",    "capv-pre2",    0x4694D3, 0x76, 0x77),  # t<0 jbe -> ja
    ("m-cv-ja1",     "capv-post",    0x4694F9, 0x77, 0x76),  # t>1 ja -> jbe
    ("m-cv-jbee",    "capv-pre",     0x4694E8, 0x76, 0x77),  # early jbe -> ja
    # RDEC 0032A6E0
    ("m-rd-shl4",    "rdec-1",       0x32A6F6, 0x04, 0x05),  # rec stride 16->32
    ("m-rd-shl6",    "rdec-1",       0x32A706, 0x06, 0x07),  # vtx stride 64->128
    ("m-rd-movsx4",  "rdec-1",       0x32A712, 0x04, 0x06),  # rec.x -> rec.y
    ("m-rd-movsx2",  "rdec-1",       0x32A702, 0x02, 0x04),  # vtx idx -> rec.x
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
