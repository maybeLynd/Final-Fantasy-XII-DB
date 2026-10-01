#!/usr/bin/env python
"""EXP-104 autostatus-sinks-exec: execute the auto-status tail sinks
00307D10 (SINK) and 0030E060 (TAIL) from shipped bytes under Unicorn,
plus their complete helper closures.

Scripted boundary (disclosed): 003BBD00 (the notify formatter) is
entry-stubbed with rcx captured -- it pulls a ~500-body CRT/string
closure.  Everything else executes real shipped code, including
0016D6A0 which is a shipped `ret 0` no-op.

Real bodies: SINK 00307D10 + 00253B90, 00263C20, 00307CE0, 0030AB40,
0030B050, 0030BB30, 0030BF20, 0030C210 (+EXP-102 reuse: 0031B760,
0031B7E0, 003588B0, 00263E30, 00263FF0; EXP-101: 00236820/00236850;
EXP-100: 0020E600; 003148F0/002EF2B0/002EF640 + 00377C20 for the
unit-index bit).

TAIL 0030E060 + FIND 0031B860, 0016D6A0 (ret-0), 003283D0,
002FA3B0 (+003272A0, 003590D0, 00265020, 003A1920), 00263C20,
00808C40 cookie check.

EXE: FFXII_TZA.exe sha256 73461d08..721f8, image base 0x120000.
"""
import ctypes, hashlib, json, math, struct, sys
from unicorn import Uc, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE, UC_HOOK_MEM_UNMAPPED, UC_PROT_ALL
from unicorn.x86_const import *

EXE = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe"
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
IMG_LO, IMG_HI = 0x120000, 0x2F800000
HEAP, STACK, RETQ, IMG32 = 0x40000000, 0x60000000, 0x62000000, 0x50000000
STRIDE, MATCH = 0xF50, 0x698

# ---- subjects -------------------------------------------------------------
SINK    = 0x00307D10          # unit+4 bit16 writer
TAIL    = 0x0030E060          # periodic byte[rec+0x4E] setter

# ---- closure entries ------------------------------------------------------
GCHK    = 0x00253B90          # dword[0x1E0C2B8] == 0
FAM     = 0x00263C20          # byte[rcx+0xE] & 0xF
ORC     = 0x00307CE0          # 30C210 || 30BB30
REL     = 0x0030AB40          # ally/enemy relation predicate
LSCAN   = 0x0030B050          # unit+0xbc8 list scan via REL
BRES    = 0x0030BB30          # def-row resolver + row-field bit
MEMB    = 0x0030BF20          # global-table membership test
BSCAN   = 0x0030C210          # unit+0xea4 bitmask scan via GET+REL
B7E0    = 0x0031B7E0          # flag-gated handle resolver (EXP-102)
HDEC    = 0x003588B0          # handle decoder (EXP-102)
B760    = 0x0031B760          # null-safe +0x30 follower (EXP-102)
E30     = 0x00263E30          # [rcx+0x30] accessor (EXP-102)
FAMIDX  = 0x00263FF0          # fam*0x288 indexer (EXP-102)
UFLAG   = 0x00377C20          # unit-index -> table bit15
UIDX    = 0x003148F0          # global index clamp >= 0
UBASE   = 0x002EF2B0          # global base + 0x200
UGLB    = 0x002EF640          # lea global base
RESOLVE = 0x0020E600          # resolver base accessor
COUNT   = 0x00236850          # pool count
GET     = 0x00236820          # pool element getter
FIND    = 0x0031B860          # owning-unit find (EXP-101)
NOOP    = 0x0016D6A0          # shipped `ret 0` no-op
UNOT    = 0x003283D0          # unit notify wrapper
RNG     = 0x002FA3B0          # range/vector check
GHDL    = 0x003272A0          # global-handle resolver
GHGET   = 0x003590D0          # dword[0x22C7FE0] accessor
VEXT    = 0x00265020          # 3-int vector extractor
VNORM   = 0x003A1920          # SSE vector norm (leaf)
FMT     = 0x003BBD00          # notify formatter -- SCRIPTED STUB
COOKIE  = 0x00808C40          # stack-cookie check

# ---- EXP-104 phase B: RESET/APPLY/CASCADE subjects ----
RESET   = 0x003105D0          # unit field reset sink
APPLY   = 0x0030E130          # unit+0x68/+0x78 bitmask apply sink
CASC    = 0x0030E360          # cascade sink
# quiet bodies: real execution, one entry token, inner hooked tokens
# suppressed until return (disclosed quiet zones)
R780    = 0x00310780          # RESET helper: detach + byte resets
C970    = 0x0030C970          # index detach (called 2x by RESET, 1x by R780)
O280    = 0x00300280          # RESET helper
K6CF0   = 0x00316CF0          # RESET helper (list init at unit+0x778)
W91B0   = 0x003291B0          # RESET helper on unit+0x80
ZC9B0   = 0x0033C9B0          # RESET helper on unit+0x80
# scripted stubs (ret 0) for mega-closure carriers -- silent inside quiet
S24FE30 = 0x0024FE30          # 950-body carrier via 319420->2EAEA0
S300FC0 = 0x00300FC0          # 1085-body eligibility eval (CASCADE)
S17D470 = 0x0017D470          # context carrier via 30B7F0 (CASCADE)
S3112F0 = 0x003112F0          # mega-dispatcher (APPLY)
S33E1F0 = 0x0033E1F0          # element serializer w/ CRT vararg tail (z9b)
# value stubs: scripted boundaries whose RETURNS steer the subject --
# ret comes from case["qret"][addr] (default 0), disclosed as ~s<tag>
V_B9B   = 0x0030B9B0          # CASC eligibility wrapper (30B7F0 carrier)
V_B8E   = 0x0030B8E0          # CASC eligibility wrapper (same closure)
V_773   = 0x00387730          # CASC arg4<0 decoder; ret -> dword write
V_76D   = 0x003876D0          # CASC arg5<0 decoder; ret -> word write
V_014   = 0x00300140          # CASC arm: RESET-family carrier
V_114   = 0x00301140          # CASC arm: carrier (2E9600 closure)
V_228   = 0x00312280          # CASC arm: serializer carrier
V_99B   = 0x003299B0          # CASC arm helper (46A7xx carrier)
V_4D0   = 0x003284D0          # CASC: range helper (RNG closure)
V_46A8  = 0x0046A800          # CASC flag60 helper, action in {3,4}
# APPLY/CASCADE depth-1 quiet callees
A_F22   = 0x00322C50          # APPLY index-gate dispatch (ecx=0x1d arm)
A_EA4   = 0x0030EA40          # APPLY helper (action in {0,2})
A_BE0   = 0x00386AE0          # APPLY builder (action in {2,3})
A_B50   = 0x00386A50          # builder (flag always cleared)
A_B70   = 0x00386A70          # CASC builder (action not in {3,4})
A_479   = 0x0046A790          # APPLY notify2 (action in {2,3})
A_472   = 0x0046A720          # APPLY notify2 (clear actions)
A_79B   = 0x003279B0          # APPLY bitidx 0x68..0x71 callback
A_4B1   = 0x00384B10          # ~be0 inner: rand() bit-picker (IAT)
A_FED   = 0x0030FED0          # family mask propagation

QUIET = {R780: "t78", C970: "c97", O280: "o28", K6CF0: "k6c",
         W91B0: "w91", ZC9B0: "z9b",
         A_F22: "f22", A_EA4: "ea4", A_BE0: "be0", A_B50: "b50",
         A_B70: "b70", A_479: "479", A_472: "472", A_79B: "79b",
         A_FED: "fed"}
QSTUBS = {S24FE30, S300FC0, S17D470, S3112F0, S33E1F0,
          V_B9B, V_B8E, V_773, V_76D, V_014, V_114, V_228,
          V_99B, V_4D0, V_46A8, A_4B1}
QST = {S24FE30: "sq24", S300FC0: "sfc", S17D470: "sd47",
       S3112F0: "s2f", S33E1F0: "se1", V_B9B: "sb9", V_B8E: "sb8",
       V_773: "s73", V_76D: "s6d", V_014: "s014", V_114: "s114",
       V_228: "s228", V_99B: "s99b", V_4D0: "s4d0", V_46A8: "sa8",
       A_4B1: "s4b1"}
MEMSET  = 0x00861EC0          # jmp-thunk into unresolved IAT (CRT memset)
SQRTF   = 0x00861F14          # jmp-thunk into unresolved IAT (CRT sqrtf)
G_F22T  = 0x02EBF040          # APPLY gate-table global (322C50 arm 0x1D)
G_CG    = 0x02EBF118          # CASC cascade-mask table global (BSS)
G_FEDT  = 0x02EBF130          # 30FED0 mask-table global (BSS)
G_B79T  = 0x02EBF190          # 3279B0 stat-table base (BSS)
# CASC post-dispatch arm per bitidx (byte map @0x30E8C4, arms @0x30E8A4)
CASC_ARM = [0,1,2,7,3,4,7,7,5,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,4,7,7,7,6]

# ---- globals ---------------------------------------------------------------
G_POOL  = 0x0208E688
G_COUNT = 0x0208E6A0
G_RESB  = 0x01F83530          # RESOLVE base qword
G_MODE  = 0x01E0C2B8          # dword; GCHK returns (==0)
G_GBYTE = 0x022C1F48          # &= 0xF9 in the GCHK-true path
G_GQW   = 0x022C1F40          # = 0 in the GCHK-true path
G_CNT1  = 0x01EEC320          # MEMB table1 count (byte)
G_CNT2  = 0x01EEC370          # MEMB table2 count (byte)
G_TB1   = 0x01EEC340          # MEMB table1 slot array, stride 24
G_TB2   = 0x01EEC390          # MEMB table2 slot array, stride 24
G_UIDX  = 0x021654C4          # dword global unit index (UGLB+0x200+0x1044)
G_UTAB  = 0x02ADD100          # qword; UFLAG table ptr (cnt +4, data +8 s3)
G_FLAG9 = 0x02089340          # byte; B7E0/GHDL gate bit 0x10
G_FAMT  = 0x02098E10          # fam records, stride 0x288 (EXP-102)
G_HDL   = 0x022C7FE0          # dword global handle (GHGET)
G_FMTI  = 0x01EED300          # UNOT idx*4 byte table
G_VECG  = 0x01EEBB00          # RNG writes object's vector here (3 dwords)
G_DSEL  = 0x01EEBB04          # ... then dword cleared
G_FCON  = 0x008F3128          # float constant (in image)
G_CTX29 = 0x0209BE80          # 290B90's list-context global (BSS)
G_BT    = 0x02EBF138          # BRES def-table global (read 4x)

POOL   = HEAP + 0x000000      # unit pool element 0 (= the unit)
REC    = HEAP + 0x400000      # record (unit[0x698] / TAIL rcx)
REC2   = HEAP + 0x500000      # second unit's record
UNIT2  = HEAP + 0x800000      # second unit (REL B side)
MISS   = HEAP + 0x880000      # blank B-side object (rel miss)
CARR   = HEAP + 0x980000      # list carrier objects ([+0x30] -> unit)
HDRP   = HEAP + 0xA00000      # fam-record element arena for HDEC
TABS   = IMG32 + 0x000000     # def-table headers (0x40 stride)
ROWS   = IMG32 + 0x200000     # resolved row arena
RESB   = ROWS                 # [G_RESB] points here
UTABP  = HEAP + 0xB00000      # UFLAG's stride-3 table
VECP   = HEAP + 0xC00000      # VEXT vector source ([+0xB8] -> 3 ints)
SRCP   = HEAP + 0xD00000      # unit+0xB88 copy source (30EDA0)
CTXP   = HEAP + 0xE00000      # 290B90 list-context global target
COBJ   = HEAP + 0x600000      # CASC rsi object (record-like status block)
F22TP  = HEAP + 0xF00000      # APPLY gate table (count at +4)
FEDTP  = IMG32 + 0x300000     # 30FED0 mask-table fixture (stride+key)
B79TP  = IMG32 + 0x380000     # 3279B0 stat-table base fixture
CGTP   = HEAP + 0xF80000      # CASC cascade-mask table (stride +8, key +C)
ALOC   = STACK + 0x80000 - 0x198   # APPLY's local struct addr (rcx->3112F0)
CLOC   = STACK + 0x80000 - 0x178   # CASC's local struct addr

HOOKS = {COUNT: "n", GET: "g", RESOLVE: "R", FIND: "F",
         GCHK: "G", FAM: "e", ORC: "o", REL: "r", LSCAN: "L",
         BRES: "b", MEMB: "M", BSCAN: "N", B7E0: "h", HDEC: "H",
         B760: "p", E30: "a", FAMIDX: "f", UFLAG: "u", UIDX: "i",
         UBASE: "q", UGLB: "Q", NOOP: "d", UNOT: "D", RNG: "v",
         GHDL: "s", GHGET: "j", VEXT: "w", VNORM: "z", FMT: "P",
         COOKIE: "K"}


def qw(v): return struct.pack("<Q", v & 0xFFFFFFFFFFFFFFFF)
def dw(v): return struct.pack("<I", v & 0xFFFFFFFF)
def hw(v): return struct.pack("<H", v & 0xFFFF)
def s32(v):
    v &= 0xFFFFFFFF
    return v - 0x100000000 if v & 0x80000000 else v
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

        # unit pool: matches[i] -> element i's +0x698 equals the FIND key
        w(G_POOL, qw(POOL))
        matches = case.get("matches", [case.get("unit") is not None])
        cnt = case.get("count", len(matches))
        w(G_COUNT, dw(cnt))
        first = next((i for i, m in enumerate(matches) if m), 0)
        self.uaddr = POOL + first * STRIDE
        # per-pool-element field specs (element i)
        poolspec = case.get("poolspec", {})
        for i, spec in poolspec.items():
            fields(POOL + i * STRIDE, spec, w)
        if case.get("unit") is not None:
            fields(self.uaddr, case["unit"], w)
        # plant FIND keys AFTER field specs so specs win on 0x698
        for i, m in enumerate(matches):
            if m:
                el = POOL + i * STRIDE
                have = self.planted.get(el + MATCH)
                if not have and not case.get("unit") or i != first:
                    w(el + MATCH, qw(case.get("rec_ptr", REC)))

        if case.get("rec") is not None:
            fields(REC, case["rec"] or {}, w)
        if case.get("rec2") is not None:
            fields(REC2, case["rec2"] or {}, w)
        if case.get("unit2") is not None:
            fields(UNIT2, case["unit2"] or {}, w)
        for i, cspec in enumerate(case.get("carriers", [])):
            fields(CARR + i * 0x40, cspec, w)
        for addr, spec in case.get("objs", {}).items():
            fields(addr, spec, w)

        g = case.get("globals", {})
        w(G_MODE, dw(g.get("mode", 1)))
        w(G_GBYTE, bytes([g.get("gbyte", 0xFF)]))
        w(G_GQW, qw(g.get("gqw", 0x1111)))
        w(G_CNT1, bytes([g.get("cnt1", 0)]))
        w(G_CNT2, bytes([g.get("cnt2", 0)]))
        w(G_UIDX, dw(g.get("uidx", 0)))
        w(G_UTAB, qw(g.get("utab", UTABP)))
        w(UTABP + 4, dw(g.get("utabcnt", 4)))
        for i, ent in enumerate(g.get("utab_entries", [])):
            w(UTABP + 8 + i * 3, bytes([ent & 0xFF, (ent >> 8) & 0xFF]))
        w(G_FLAG9, bytes([g.get("flag9", 0x10)]))
        w(G_HDL, dw(g.get("hdl", 0)))
        w(G_RESB, qw(case.get("resb", RESB)))
        w(G_F22T, qw(g.get("f22tab", 0)))   # APPLY gate table
        w(G_CG, qw(g.get("cgtab", 0)))      # CASC cascade-mask table
        # 30FED0 mask-table: benign (zero masks) by default for
        # apply/casc; globals["fedtab"]=0 restores the null fault
        fedt = g.get("fedtab", -1)
        if fedt == -1:
            fedt = FEDTP if case.get("entry") in ("apply", "casc") else 0
        w(G_FEDT, qw(fedt))
        if fedt == FEDTP:
            w(FEDTP + 8, hw(g.get("fedstride", 0x20)))
            w(FEDTP + 0xC, dw(g.get("fedkey", 0x180)))
        # 3279B0 stat-table: benign by default for apply
        b79t = g.get("b79tab", -1)
        if b79t == -1:
            b79t = B79TP if case.get("entry") == "apply" else 0
        w(G_B79T, qw(b79t))
        for i, ptr in enumerate(g.get("tb1", [])):
            w(G_TB1 + i * 24, qw(ptr))
        for i, ptr in enumerate(g.get("tb2", [])):
            w(G_TB2 + i * 24, qw(ptr))
        w(G_DSEL, dw(g.get("dsel", 0x1234)))
        # UNOT byte table (idx*4 entries) at G_FMTI
        for i in range(8):
            w(G_FMTI + i * 4, dw(g.get("fmt%d" % i, i * 0x11)))
        # BRES def-table global + its tab header
        btspec = g.get("btab", {})
        bptr = btspec.get("ptr", TABS + 0x40)
        w(G_BT, qw(bptr))
        if bptr:
            w(bptr + 4, dw(btspec.get("cnt", 8)))
            w(bptr + 8, hw(btspec.get("stride", 0x30)))
            w(bptr + 0xC, dw(btspec.get("rarg", 0)))
        for addr, b in case.get("rows", {}).items():
            w(addr, bytes([b & 0xFF]))
        # fam records for HDEC (EXP-102 shape): rec {+0 hdr, +8 elems
        # ptr, +0x10 live(qword), +0x20 bound(dword)}; elems array is
        # {+0 count dword, +8+i*8 element POINTERS}; element object has
        # u16 tag at +0x16 and the object ptr at +0x30.
        for fami, spec in g.get("fam_recs", {}).items():
            base = G_FAMT + fami * 0x288
            elems = spec.get("elems", HDRP + fami * 0x1000)
            w(base + 0, qw(spec.get("hdr", 1)))
            w(base + 8, qw(elems))
            w(base + 0x10, qw(spec.get("live", 1)))
            w(base + 0x20, dw(spec.get("bound", 4)))
            w(elems + 0, dw(spec.get("count", 4)))
            for j, e in enumerate(spec.get("elements", [])):
                ep = elems + 0x400 + j * 0x100
                w(elems + 8 + j * 8, qw(ep))
                w(ep + 0x16, hw(e.get("tag", 0)))
                w(ep + 0x30, qw(e.get("obj", UNIT2)))
                if e.get("fields"):
                    fields(ep, e["fields"], w)
        # VEXT vector source: [u10+0xB8] -> 3 floats
        w(VECP + 0xB8, qw(VECP + 0x100))
        v = g.get("vec", (0.0, 0.0, 0.0))
        w(VECP + 0x100, struct.pack("<f", v[0]))
        w(VECP + 0x104, struct.pack("<f", v[1]))
        w(VECP + 0x108, struct.pack("<f", v[2]))
        w(VECP + 3, bytes([g.get("vectype", 0x20)]))
        # 290B90 list context: [G_CTX29]+0x10F10 is the list head
        w(G_CTX29, qw(g.get("ctx29", CTXP)))
        # second vector source for the global object
        w(VECP + 0x200 + 0xB8, qw(VECP + 0x300))
        v2 = g.get("vec2", (0.0, 0.0, 0.0))
        w(VECP + 0x300, struct.pack("<f", v2[0]))
        w(VECP + 0x304, struct.pack("<f", v2[1]))
        w(VECP + 0x308, struct.pack("<f", v2[2]))
        w(VECP + 0x203, bytes([g.get("vectype2", 0x20)]))

        self.trace, self.faults, self.fired = [], [], set()
        self.quiet = 0
        for va, data in case.get("patch_bytes", []):
            gm.w(va, data)
        uc = self.uc
        uc.hook_add(UC_HOOK_MEM_UNMAPPED, self.on_bad)
        for va in (list(HOOKS) + list(QUIET) + list(QSTUBS)
                   + [MEMSET, SQRTF, CASC]):
            uc.hook_add(UC_HOOK_CODE, self.on_call, begin=va, end=va)

    def on_call(self, uc, addr, size, _):
        self.fired.add(addr)
        rcx = uc.reg_read(UC_X86_REG_RCX)
        rdx = uc.reg_read(UC_X86_REG_RDX)
        if self.quiet:
            # inside a quiet zone: hooked tokens are suppressed, but
            # scripted boundaries must still fire (real path unreachable)
            if addr == VNORM:
                self._vnorm_stub(uc)
            elif addr == FMT:
                self._stub(self.case.get("stub_fmt", 0))
            elif addr == MEMSET:
                self._memset_stub(uc)
            elif addr == SQRTF:
                self._sqrtf_stub(uc)
            elif addr in QSTUBS:
                self._stub(self.case.get("qret", {}).get(addr, 0))
            return
        if addr == CASC:
            # recursive cascade call (return addr inside the body) --
            # real body, full inner tokens; entry call emits nothing
            sp = uc.reg_read(UC_X86_REG_RSP)
            back = struct.unpack("<Q", self.gm.r(sp, 8))[0]
            if 0x30E360 <= back < 0x30E890:
                self.trace.append(
                    "C%x" % (uc.reg_read(UC_X86_REG_R8) & 0xFF))
            return
        if addr in QSTUBS:
            # scripted boundary: disclosed token + case-controlled ret
            rv = self.case.get("qret", {}).get(addr, 0)
            self.trace.append("~%s%x" % (QST[addr],
                                         rcx & 0xFFFFFFFFFFFFFFFF))
            self._stub(rv)
            self.trace[-1] += "=%d" % s32(rv)
            return
        if addr in QUIET:
            self.trace.append("~%s%x" % (QUIET[addr],
                                         rcx & 0xFFFFFFFFFFFFFFFF))
            self._quiet_enter()
            return
        if addr == COUNT:
            self.trace.append("n")
        elif addr == GET:
            self.trace.append("g%d" % s32(rcx))
            self._watch_ret()
        elif addr == RESOLVE:
            self.trace.append("R%x" % (rcx & 0xFFFFFFFF))
            self._watch_ret()
        elif addr == FIND:
            self.trace.append("F%x" % (rcx & 0xFFFFFFFFFFFFFFFF))
            self._watch_ret()
        elif addr in (REL, UNOT):
            self.trace.append("%s%x,%x" % (HOOKS[addr], rcx & 0xFFFFFFFF,
                                           rdx & 0xFFFFFFFF))
            self._watch_ret()
        elif addr in (FAM, B7E0, HDEC, FAMIDX, B760, E30, MEMB):
            self.trace.append("%s%x" % (HOOKS[addr], rcx & 0xFFFFFFFF))
            self._watch_ret()
        elif addr == FMT:
            self.trace.append("P%x" % (rcx & 0xFFFFFFFFFFFFFFFF))
            self._stub(self.case.get("stub_fmt", 0))
        elif addr == VNORM:
            self.trace.append("z")
            self._vnorm_stub(uc)
        elif addr == MEMSET:
            self._memset_stub(uc)
        elif addr == SQRTF:
            self._sqrtf_stub(uc)
        elif addr == NOOP:
            self.trace.append("d")
        elif addr == COOKIE:
            pass
        else:
            self.trace.append(HOOKS[addr])
            self._watch_ret()

    def _vnorm_stub(self, uc):
        # SSE leaf tail-jumps an IAT thunk (unmapped CRT sqrt) --
        # compute the float norm and put it in xmm0, then return.
        def f3(p):
            return [struct.unpack("<f", self.gm.r(p + 4 * i, 4))[0]
                    for i in range(3)]
        c = f3(uc.reg_read(UC_X86_REG_RCX))
        d = f3(uc.reg_read(UC_X86_REG_RDX))
        norm = math.sqrt(sum((a - b) * (a - b)
                             for a, b in zip(c, d)))
        uc.reg_write(UC_X86_REG_XMM0,
                     struct.unpack("<I", struct.pack("<f", norm))[0])
        self._stub(0)

    def _memset_stub(self, uc):
        # 861EC0 jmp-thunks into an unresolved IAT entry (lands on
        # import-name data). Callers use the CRT memset signature
        # rcx=dst, dl=val, r8=size; emulate and return dst.
        dst = uc.reg_read(UC_X86_REG_RCX)
        val = uc.reg_read(UC_X86_REG_RDX) & 0xFF
        n = uc.reg_read(UC_X86_REG_R8)
        if n:
            uc.mem_write(dst, bytes([val]) * n)
        self._stub(dst)

    def _sqrtf_stub(self, uc):
        # 861F14 jmp-thunks into an unresolved IAT entry; callers use
        # the CRT sqrtf signature xmm0 -> xmm0.
        x = struct.unpack("<f", struct.pack(
            "<I", uc.reg_read(UC_X86_REG_XMM0) & 0xFFFFFFFF))[0]
        uc.reg_write(UC_X86_REG_XMM0, struct.unpack(
            "<I", struct.pack("<f", math.sqrt(abs(x))))[0])
        self._stub(0)

    def _quiet_enter(self):
        # real execution continues; hooked tokens suppressed until this
        # body's return address executes. The rsp guard is required:
        # quiet bodies can call back into the caller's own function
        # (30FED0 -> APPLY), whose epilogue shares the return address.
        uc = self.uc
        sp = uc.reg_read(UC_X86_REG_RSP)
        back = struct.unpack("<Q", self.gm.r(sp, 8))[0]
        want = sp + 8          # rsp after the real ret pops 'back'
        self.quiet += 1

        def on_ret(uc_, a, s, _u):
            if uc_.reg_read(UC_X86_REG_RSP) != want:
                return          # nested body hit the same address
            self.quiet -= 1

        uc.hook_add(UC_HOOK_CODE, on_ret, begin=back, end=back)

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
        want = sp + 8          # rsp after the real ret pops 'back'
        idx = len(self.trace) - 1
        holder = {"fired": False}

        def on_ret(uc_, a, s, _u):
            if holder["fired"]:
                return
            if uc_.reg_read(UC_X86_REG_RSP) != want:
                return          # same address hit at a deeper call level
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
    """Model-side trace emitter matching native token nesting."""
    def __init__(self, w):
        self.w = w
        self.t = []
        self.obs = []
        self.qret = {}
        self.vstate = {}          # model-predicted writes (nested reads)

    def _vd(self, addr):
        return self.vstate.get(addr, self.w.d(addr))

    def _vb(self, addr):
        return self.vstate.get(addr, self.w.b(addr))

    def _vset_d(self, addr, v):
        self.vstate[addr] = v
        self.obs.append((addr, 4, v))

    def _vset_b(self, addr, v):
        self.vstate[addr] = v
        self.obs.append((addr, 1, v))

    def _vset_h(self, addr, v):
        self.vstate[addr] = v
        self.obs.append((addr, 2, v))
    def emit(self, s):
        self.t.append(s)
        return len(self.t) - 1
    def done(self, i, r):
        self.t[i] += "=%d" % s32(r)
        return r

    # -- leaf/small callees --
    def m_fam(self, x):
        i = self.emit("e%x" % (x & 0xFFFFFFFF))
        v = (self.w.b(x + 0xE) & 0xF) if x else 0
        return self.done(i, v)

    def m_e30(self, x):
        i = self.emit("a%x" % (x & 0xFFFFFFFF))
        return self.done(i, self.w.q(x + 0x30) if x else 0)

    def m_b760(self, x):
        i = self.emit("p%x" % (x & 0xFFFFFFFF))
        r = self.m_e30(x) if x else 0
        return self.done(i, r)

    def m_famidx(self, x):
        i = self.emit("f%x" % (x & 0xFFFFFFFF))
        return self.done(i, G_FAMT + s32(x) * 0x288)

    def m_hdec(self, h):
        i = self.emit("H%x" % (h & 0xFFFFFFFF))
        r = 0
        if h:
            fam = (h >> 16) & 0xF
            idx = h & 0xFFFF
            tag = (h >> 20) & 0x7FF
            if fam < 5:
                rec = self.m_famidx(fam)
                elems = self.w.q(rec + 8)
                if elems and self.w.q(rec) and idx < self.w.d(rec + 0x20) \
                        and (self.w.q(rec + 0x10) & 1) \
                        and idx < self.w.d(elems):
                    ep = self.w.q(elems + 8 + idx * 8)
                    if ep and self.w.h(ep + 0x16) == tag:
                        r = ep
        return self.done(i, r)

    def m_b7e0(self, h):
        i = self.emit("h%x" % (h & 0xFFFFFFFF))
        r = 0
        if self.w.b(G_FLAG9) & 0x10:
            e = self.m_hdec(h)
            if e:
                r = self.m_e30(e)
        return self.done(i, r)

    def m_resolve(self, arg):
        i = self.emit("R%x" % (arg & 0xFFFFFFFF))
        return self.done(i, self.w.q(G_RESB) + arg)

    def m_get(self, idx):
        i = self.emit("g%d" % s32(idx))
        cnt = self.w.d(G_COUNT)
        r = self.w.q(G_POOL) + idx * STRIDE if 0 <= idx < cnt else 0
        return self.done(i, r)

    def m_uflag(self):
        i = self.emit("u")
        ii = self.emit("i")
        iq = self.emit("q")
        iQ = self.emit("Q")
        self.done(iQ, 0x2164280)
        self.done(iq, 0x2164480)
        idx = max(0, s32(self.w.d(G_UIDX)))
        self.done(ii, idx)
        r = 0
        tab = self.w.q(G_UTAB)
        if tab and idx < self.w.d(tab + 4):
            e = tab + 8 + idx * 3
            r = ((self.w.b(e + 1) << 8) + self.w.b(e)) >> 15
        return self.done(i, r)

    def m_rel(self, ua, ub):
        i = self.emit("r%x,%x" % (ua & 0xFFFFFFFF, ub & 0xFFFFFFFF))
        w = self.w
        if not ua or not ub:
            return self.done(i, 0)
        fa = self.m_fam(w.q(ua + 0x10))
        fb = self.m_fam(w.q(ub + 0x10))
        if fa == 5 or fb == 5 or not (w.b(ua) & 0x10) \
                or not (w.b(ub) & 0x10):
            return self.done(i, 0)
        recA, recB = w.q(ua + 0x698), w.q(ub + 0x698)
        okA = bool(recA and w.b(recA + 5) == 0) or fa == 3
        okB = bool(recB and w.b(recB + 5) == 0) or fb == 3
        ebp = 1 if okA == okB else 0
        if not recA:
            self.done(i, "FAULT")          # reads [0+0x64]
            return "FAULT64"
        eax = ((w.d(recA + 0x64) | w.d(recA + 0x3C)) >> 5) & 1
        return self.done(i, (1 if eax == ebp else 0) + 1)

    def m_lscan(self, ua):
        i = self.emit("L")
        cnt = s32(self.w.d(ua + 0xBC4))
        r = 0
        if cnt > 0:
            for k in range(cnt):
                ep = self.w.q(ua + 0xBC8 + k * 0x10)
                e2 = self.m_b760(ep)
                if not e2:
                    continue
                rv = self.m_rel(ua, e2)
                if rv == "FAULT64":
                    self.done(i, "FAULT")
                    return "FAULT64"
                if rv > 1:
                    r = 1
                    break
        return self.done(i, r)

    def m_bscan(self, ua):
        i = self.emit("N")
        w = self.w
        r = 0
        rec = w.q(ua + 0x698)
        ok = bool(ua and rec)
        if ok and (w.d(rec + 0x64) | w.d(rec + 0x3C)) & 0x80000003:
            u = self.m_uflag()
            if u == 0:
                ok = False
        if ok and w.d(ua + 0xEA4):
            for k in range(0x20):
                if not (w.d(ua + 0xEA4) >> k) & 1:
                    continue
                if k == w.b(ua + 0xEA9) and w.b(ua + 0x6B6):
                    continue
                e2 = self.m_get(k)
                if not e2:
                    continue
                rv = self.m_rel(ua, e2)
                if rv == "FAULT64":
                    self.done(i, "FAULT")
                    return "FAULT64"
                if rv > 1:
                    r = 1
                    break
        return self.done(i, r)

    def m_bres(self, ua, wid):
        i = self.emit("b")
        w = self.w
        if wid > 0x21E:
            return self.done(i, 0)
        h = self.m_b7e0(w.d(ua + 0x710))
        if not h:
            return self.done(i, 0)
        rv = self.m_rel(ua, h)
        if rv == "FAULT64":
            self.done(i, "FAULT")
            return "FAULT64"
        if rv > 1:
            return self.done(i, 1)
        tab = w.q(G_BT)
        base = 0
        if tab:
            base = self.m_resolve(w.d(tab + 0xC))
            if base:
                base = self.m_resolve(w.d(tab + 0xC))
        p1 = (base + wid * w.h(tab + 8)) if base else 0
        if not p1:
            self.done(i, "FAULT")
            return "FAULT1C"             # byte[0+0x1C]
        if (w.b(p1 + 0x1C) - 1) > 7:
            return self.done(i, 1)
        p2 = 0
        if tab:
            base = self.m_resolve(w.d(tab + 0xC))
            if base:
                base = self.m_resolve(w.d(tab + 0xC))
                p2 = base + wid * w.h(tab + 8)
        if not p2:
            self.done(i, "FAULT")
            return "FAULT2C"             # word[0+0x2C]
        return self.done(i, (w.h(p2 + 0x2C) >> 14) & 1)

    def m_orc(self, ua):
        i = self.emit("o")
        r = self.m_bscan(ua)
        if not r:
            r = self.m_bres(ua, self.w.h(ua + 0x714))
        return self.done(i, r)

    def m_memb(self, arg):
        # MEMB: pointer-membership test -- arg must equal one of the
        # 24-byte-stride slot addresses in table1 or table2.
        i = self.emit("M%x" % (arg & 0xFFFFFFFF))
        r = 0
        for k in range(self.w.b(G_CNT1)):
            if G_TB1 + k * 24 == arg:
                r = 1
        for k in range(self.w.b(G_CNT2)):
            if G_TB2 + k * 24 == arg:
                r = 1
        return self.done(i, r)

    def m_gchk(self):
        i = self.emit("G")
        return self.done(i, 1 if self.w.d(G_MODE) == 0 else 0)

    def m_find(self, key):
        i = self.emit("F%x" % (key & 0xFFFFFFFFFFFFFFFF))
        cnt = self.w.d(G_COUNT)
        r = 0
        self.emit("n")
        for k in range(cnt):
            e = self.m_get(k)
            if e and self.w.q(e + 0x698) == key:
                r = e
                break
            self.emit("n")          # recheck fires after every miss
        return self.done(i, r)

    def m_ghdl(self):
        i = self.emit("s")
        r = 0
        ii = self.emit("j")
        h = self.w.d(G_HDL)
        self.done(ii, h)
        if self.w.b(G_FLAG9) & 0x10:
            e = self.m_hdec(h)
            if e:
                o = self.m_e30(e)
                if o and (self.w.b(o) & 8):
                    r = o
        return self.done(i, r)

    def _f3(self, p):
        return [struct.unpack("<f", dw(self.w.d(p + 4 * i)))[0]
                for i in range(3)]

    def _vext_vec(self, x):
        """VEXT(x): returns (ok, vec). ok iff (b[x+3]>>5)-1 in {1,2};
        on failure the outputs are zeroed."""
        if x and ((self.w.b(x + 3) >> 5) - 1) in (1, 2):
            return 1, self._f3(self.w.q(x + 0xB8))
        return 0, [0.0, 0.0, 0.0]

    def m_vext(self, x):
        i = self.emit("w")
        r, _v = self._vext_vec(x)
        return self.done(i, r)

    def m_vnorm(self):
        self.emit("z")               # stubbed IAT leaf; no ret token

    def m_rng(self, u10):
        i = self.emit("v")
        w = self.w
        r = 0
        if u10:
            obj = self.m_ghdl()
            ovec = [0.0, 0.0, 0.0]
            if obj:
                ok, ovec = self._vext_vec(w.q(obj + 0x10))
                self.m_vext(w.q(obj + 0x10))
                if ok:
                    ovec[1] = 0.0    # dword[G_VECG+4] cleared after VEXT
            self.m_vext(u10)
            _ok, uvec = self._vext_vec(u10)
            self.m_vnorm()
            norm = math.sqrt(sum((a - b) * (a - b)
                                 for a, b in zip(uvec, ovec)))
            fc = struct.unpack("<f", img(raw_, secs_, G_FCON, 4))[0]
            r = 1 if norm < fc else 0
        return self.done(i, r)


    def m_reset(self, u):
        """003105D0: unit field reset. Depth-1 callees are quiet zones
        (~tag tokens); COUNT/GET and the shipped no-op stay hooked."""
        w = self.w
        if not u or w.q(u + 0x698) == 0:
            return
        # 308270 (inside t78, gated on u0 bit22) sets byte[u+0x695]=0xFF
        # before RESET reads it back for its first 30C970 call.
        gated = bool(w.d(u) & 0x400000)
        self.emit("~t78%x" % (u & 0xFFFFFFFFFFFFFFFF))
        self.emit("~c97%x" % (0xFF if gated else w.b(u + 0x695)))
        self.emit("~c97%x" % w.b(u + 0x696))
        self.emit("~o28%x" % (u & 0xFFFFFFFFFFFFFFFF))
        self.emit("d")
        self.emit("n")
        for i in range(self.w.d(G_COUNT)):
            self.m_get(i)
            self.emit("n")
        self.emit("~k6c%x" % ((u + 0x778) & 0xFFFFFFFFFFFFFFFF))
        self.emit("~w91%x" % ((u + 0x80) & 0xFFFFFFFFFFFFFFFF))
        self.emit("~z9b%x" % ((u + 0x80) & 0xFFFFFFFFFFFFFFFF))

    # -- APPLY / CASCADE subjects --
    def _vstub(self, addr, rcx):
        rv = self.qret.get(addr, 0)
        i = self.emit("~%s%x" % (QST[addr], rcx & 0xFFFFFFFFFFFFFFFF))
        return self.done(i, rv)

    def m_apply(self, u, bitidx, arg3, flags, action):
        """0030E130: action-indexed bit ops on u+0x68 (state A) and
        u+0x78 (state B); builder + notify fan-out on transitions.
        Depth-1 callees are quiet zones; 3112F0/30FED0 boundaries."""
        w = self.w
        rbx = u + (bitidx >> 3)
        esi = 1 << (bitidx & 7)
        before = 1 if (self._vb(rbx + 0x68) | self._vb(rbx + 0x78)) & esi else 0
        # 322C50 arm 0x1d: bounds check vs dword[table+4]; null -> 0.
        # quiet zone: real body runs, token carries no return value.
        self.emit("~f22%x" % 0x1D)
        tab = w.q(G_F22T)
        gate = bool(tab) and 0 <= bitidx < w.d(tab + 4)
        if not gate:
            return
        # dispatch on action: a0 clr+0x68, a1 clr+0x78, a2 set+0x68,
        # a3 set+0x78 -- early exit when bit already in target state
        if action == 0:
            if not self._vb(rbx + 0x68) & esi:
                return
            self._vset_b(rbx + 0x68, self._vb(rbx + 0x68) & ~esi & 0xFF)
        elif action == 1:
            if not self._vb(rbx + 0x78) & esi:
                return
            self._vset_b(rbx + 0x78, self._vb(rbx + 0x78) & ~esi & 0xFF)
        elif action == 2:
            if self._vb(rbx + 0x68) & esi:
                return
            self._vset_b(rbx + 0x68, self._vb(rbx + 0x68) | esi)
        elif action == 3:
            if self._vb(rbx + 0x78) & esi:
                return
            self._vset_b(rbx + 0x78, self._vb(rbx + 0x78) | esi)
        else:
            return
        if action in (0, 2):
            self.emit("~ea4%x" % (u & 0xFFFFFFFFFFFFFFFF))
        after = 1 if (self._vb(rbx + 0x68) | self._vb(rbx + 0x78)) & esi else 0
        if after == before:
            return
        # notify: memset local 0x148 (silent), then builder
        self.emit("~be0%x" % (u & 0xFFFFFFFFFFFFFFFF)
                  if action in (2, 3) else
                  "~b50%x" % (u & 0xFFFFFFFFFFFFFFFF))
        # 386AE0 leaves local+0x2c bit0 only for bitidx 0x34;
        # 386A50 always clears -> 3112F0 stub only on that path
        if action in (2, 3) and bitidx == 0x34:
            self._vstub(S3112F0, ALOC)
        if not (flags & 2):
            self.emit("~479%x" % (u & 0xFFFFFFFFFFFFFFFF)
                      if action in (2, 3) else
                      "~472%x" % (u & 0xFFFFFFFFFFFFFFFF))
        if 0 <= bitidx - 0x68 <= 9:
            # 3279B0: 3 clamped byte writes at
            # base + 0x5B42 + (3*b[u+4] + i)*0x34, i=0..2
            edx = 1 if action in (2, 3) else -1
            self.emit("~79b%x" % (u & 0xFFFFFFFFFFFFFFFF))
            base = w.q(G_B79T)
            if base and w.b(u + 5) == 0:
                b4 = w.b(u + 4)
                for i in range(3):
                    a = base + 0x5B42 + (3 * b4 + i) * 0x34
                    nv = max(0, min(0xC, self._vb(a) + edx))
                    if nv != self._vb(a):
                        self._vset_b(a, nv)
        if not (flags & 0x200):
            # 30FED0: desired-mask propagator. Under the zeroed
            # fixtures its desired mask is empty, so its nested
            # APPLY(...,action=1) calls re-clear every set bit in
            # u+0x78..0x87 below the F22 gate count.
            self.emit("~fed%x" % (u & 0xFFFFFFFFFFFFFFFF))
            tab = w.q(G_F22T)
            lim = w.d(tab + 4) if tab else 0
            for i in range(8):
                a = u + 0x78 + i
                b = self._vb(a)
                keep = max(0, lim - i * 8)
                nv = b & (((1 << keep) - 1) ^ 0xFF) if keep < 8 else 0
                if nv != b:
                    self._vset_b(a, nv)
            # its trailing NOTIFY(u,0,0) zeroes u+0x24..0x47 then
            # rebuilds; under zeroed rows the rebuild is 0
            if w.b(u + 5) == 0:
                for a in (u + 0x38, u + 0x3C):
                    if self._vd(a):
                        self._vset_d(a, 0)

    def m_casc(self, rsi, u2, bitidx, arg4, arg5, flags, action):
        """0030E360: recursive cascade over u+0x38/+0x3C/+0x64 masks.
        rbx = FIND(rsi) owner unit; eligibility wrappers, dispatch,
        per-action arrays, recursion mask, post-dispatch arms."""
        w = self.w
        f1 = self.m_find(u2)
        f2 = self.m_find(rsi)          # rbx
        edi = (1 << bitidx) & 0xFFFFFFFF if bitidx < 32 else 0
        is34 = 1 if action - 3 in (0, 1) else 0
        flag58 = 1 if action in (0, 3) else 0
        flag5c = 1 - ((flags >> 4) & 1)
        flag60 = 1 - ((flags >> 1) & 1)
        before = 1 if (self._vd(rsi + 0x3C) | self._vd(rsi + 0x64)) & edi else 0
        if not (flags & 1):
            r = self._vstub(V_B9B, f2)
            if r:
                return
            # 30B8E0 runs only when is34 != b9b_ret(0) i.e. action{3,4}
            if is34:
                r = self._vstub(V_B8E, f2)
                if r and bitidx in (0, 1, 31):
                    return
        # eligibility block gated on is34 (je skips when 0)
        if is34:
            rec = f2 and w.q(f2 + 0x698)
            recok = bool(f2 and rec and w.b(rec + 5) == 0
                         and 0 <= w.b(rec + 4) - 0x1B <= 0xC)
            if recok:
                if bitidx in (0, 1, 31):
                    self._vstub(S300FC0, f2)
                    return
            elif bitidx in (0, 1, 31):
                if (w.d(rsi + 0x3C) | w.d(rsi + 0x64)) & 0x80000003:
                    if self.m_uflag() == 0:
                        return
        if action > 5:
            return
        # dispatch arms (reads/writes through vstate so nested
        # cascade calls see post-mutation values like native memory)
        d38 = self._vd(rsi + 0x38)
        d3c = self._vd(rsi + 0x3C)
        d64 = self._vd(rsi + 0x64)
        if action == 0:
            if not d64 & edi:
                return
            self._vset_d(rsi + 0x64, d64 & ~edi & 0xFFFFFFFF)
        elif action == 1:
            if not d3c & edi:
                return
            self._vset_d(rsi + 0x3C, d3c & ~edi & 0xFFFFFFFF)
        elif action == 2:
            if not d38 & edi:
                return
            self._vset_d(rsi + 0x38, d38 & ~edi & 0xFFFFFFFF)
        elif action == 3:
            if (d64 & edi) or (d38 & edi):
                return
            self._vset_d(rsi + 0x64, d64 | edi)
        elif action == 4:
            if d3c & edi:
                return
            self._vset_d(rsi + 0x3C, d3c | edi)
        elif action == 5:
            if d38 & edi:
                return
            self._vset_d(rsi + 0x38, d38 | edi)
        if flag58:
            ecx = arg4 & 0xFFFFFFFF
            if arg4 < 0:
                ecx = self._vstub(V_773, 0)
            self._vset_d(rsi + bitidx * 4 + 0xBC, ecx)
            ax = arg5 & 0xFFFF
            if arg5 < 0:
                ax = self._vstub(V_76D, bitidx) & 0xFFFF
            self._vset_h(rsi + bitidx * 2 + 0x13C, ax)
        # presence recheck uses the POST-dispatch values
        nd3c = self._vd(rsi + 0x3C)
        nd64 = self._vd(rsi + 0x64)
        after = 1 if (nd3c | nd64) & edi else 0
        if after == before:
            return
        # notify: memset local (silent), builder
        self.emit("~b50%x" % (rsi & 0xFFFFFFFFFFFFFFFF)
                  if is34 else
                  "~b70%x" % (rsi & 0xFFFFFFFFFFFFFFFF))
        # 386A70 leaves flag only for bitidx 0x1C with rsi+0x48 set
        if not is34 and bitidx == 0x1C and w.d(rsi + 0x48):
            self._vstub(S3112F0, CLOC)
        if is34:
            # cascade mask via RESOLVE chain: T=[G_CG]; key=d[T+0xC];
            # row=RESB+key; stride=h[T+8]; mask=d[row+bitidx*stride+0xC]
            T = w.q(G_CG)
            mask = 0
            if T:
                key = w.d(T + 0xC)
                row = self.m_resolve(key)
                if row:
                    row2 = self.m_resolve(key)
                    stride = w.h(T + 8)
                    rcx = (row2 + bitidx * stride) & 0xFFFFFFFF
                    mask = w.d(rcx + 0xC)
            for i in range(32):
                if mask >> i & 1:
                    self.emit("C%x" % i)
                    self.m_casc(rsi, u2, i, 0, 0, flags | 0x200, 0)
        if flag5c and is34 and f2:
            self._vstub(V_4D0, f2)
        if flag60:
            # is34 -> 0x46A800 (stub); else -> shipped ret-0 no-op
            if is34:
                self._vstub(V_46A8, rsi)
            else:
                self.emit("d")
        if f2 and bitidx <= 0x1F:
            arm = CASC_ARM[bitidx]
            e9a = self._vb(f2 + 0xE9A)
            ok5 = bool(u2 and w.b(u2 + 5) == 0)
            if arm == 0:          # bitidx 0
                if not is34:
                    self._vstub(V_114, f2)
                else:
                    self._vstub(S300FC0, f2)
                    self._vstub(V_228, u2)
            elif arm == 1:        # bitidx 1
                if not is34:
                    self._vstub(V_114, f2)
                else:
                    self._vstub(V_99B, f2)
                    self._vstub(S300FC0, f2)
                    self._vstub(V_228, u2)
            elif arm == 2:        # bitidx 2 -> e9a bit1
                if is34:
                    nv = (e9a & ~2 & 0xFF) | ((1 if ok5 else 0) << 1)
                    self._vset_b(f2 + 0xE9A, nv)
            elif arm == 3:        # bitidx 4
                self._vstub(V_99B, f2)
            elif arm == 4:        # bitidx 5,27 -> RESET+SINK
                ebp = 1
                if w.d(f2) & 0x1000000:
                    ebp = 0
                else:
                    a714 = w.h(f2 + 0x714)
                    if a714 > 0x21E:
                        if a714 != 0x113:
                            ebp = 1
                        else:
                            ebp = 0
                    elif w.b(f2 + 0x6B4) >= 9:
                        ebp = 0
                    elif a714 == 0x113:
                        ebp = 0
                self._vstub(V_014, f2)
                self.m_sink_nested(f2)
            elif arm == 5:        # bitidx 8 -> e9a bit0
                if is34:
                    nv = (e9a & ~1 & 0xFF) | (1 if ok5 else 0)
                    self._vset_b(f2 + 0xE9A, nv)
            elif arm == 6:        # bitidx 31
                if not is34:
                    self._vstub(V_114, f2)
                else:
                    self._vstub(V_99B, f2)
                    self._vstub(S300FC0, f2)
                    self._vstub(V_228, u2)
        if not (flags & 0x200):
            # 30FED0 zero-fixture behaviour: nested APPLY calls
            # re-clear set bits in rsi+0x78..0x87 below the F22 bound
            self.emit("~fed%x" % (rsi & 0xFFFFFFFFFFFFFFFF))
            tab = w.q(G_F22T)
            lim = w.d(tab + 4) if tab else 0
            for i in range(8):
                a = rsi + 0x78 + i
                b = self._vb(a)
                keep = max(0, lim - i * 8)
                nv = b & (((1 << keep) - 1) ^ 0xFF) if keep < 8 else 0
                if nv != b:
                    self._vset_b(a, nv)
            # its trailing NOTIFY(rsi,0,0) zeroes rsi+0x24..0x47
            # then rebuilds; under zeroed rows the rebuild is 0
            if w.b(rsi + 5) == 0:
                for a in (rsi + 0x38, rsi + 0x3C):
                    if self._vd(a):
                        self._vset_d(a, 0)

    def _obsget(self, addr, default):
        for a, n, v in reversed(self.obs):
            if a == addr:
                return v
        return default

    def m_sink_body(self, ua, out):
        """00307D10 inner eligibility chain -> ebx decision (None on
        fault, whose addr lands in out["fault"]). Emits the hooked
        callee tokens; side-effect keys (gbyte/gqw/udcc/u4clr400)
        go to out."""
        w = self.w
        rec = w.q(ua + 0x698)
        band = rec and w.b(rec + 5) == 0 and w.b(rec + 4) == 0x1A
        if band:
            return 1
        u = self.m_uflag()
        if u:
            return 0
        if not rec:
            out["fault"] = "0x64"
            return None
        if (w.d(rec + 0x64) | w.d(rec + 0x3C)) & 0x8000020:
            return 1
        gv = self.m_gchk()
        if gv:
            out["gbyte"] = w.b(G_GBYTE) & 0xF9
            out["gqw"] = 0
            out["udcc"] = 0
            return 0
        u4 = w.d(ua + 4)
        if u4 & 0x200:
            lv = self.m_lscan(ua)
            if lv == "FAULT64":
                out["fault"] = "0x64"
                return None
            if lv:
                out["u4clr400"] = True
                return 1
            return 1 if u4 & 0x400 else 0
        ov = self.m_orc(ua)
        if ov == "FAULT64":
            out["fault"] = "0x64"
            return None
        if ov == "FAULT1C":
            out["fault"] = "0x1c"
            return None
        if ov == "FAULT2C":
            out["fault"] = "0x2c"
            return None
        if ov:
            mv = self.m_memb(w.q(ua + 0x708))
            return 1 if mv == 0 else 0
        return 0

    def m_sink_nested(self, f2):
        """nested SINK call from CASC arm (bitidx 5/27): real body
        emits its inner tokens; u+4 bit16 write lands in obs."""
        out = {}
        ebx = self.m_sink_body(f2, out)
        if ebx is None:
            return
        u4 = self.w.d(f2 + 4)
        if ebx:
            nv = (u4 & ~0x10000 & 0xFFFFFFFF) | 0x10000
            if out.get("u4clr400"):
                nv = ((u4 & ~0x400 & ~0x10000) & 0xFFFFFFFF) | 0x10000
        else:
            nv = u4 & ~0x10600 & 0xFFFFFFFF
        self.obs.append((f2 + 4, 4, nv))


def model(case, w, world):
    m = M(w)
    out = {"trace": m.t}
    ua = world.uaddr
    ent = case.get("entry", "sink")

    if ent == "reset":
        if ua and w.q(ua + 0x698):
            gated = bool(w.d(ua) & 0x400000)   # 308270 body runs
            b88 = w.q(ua + 0xB88)
            if gated and not b88:
                # 30EDA0 dereferences the null B88 source
                m.emit("~t78%x" % (ua & 0xFFFFFFFFFFFFFFFF))
                out["fault"] = "0x0"
                return out
            m.m_reset(ua)
            # u+0 is written by three qword masks (308270 gated,
            # 310780, subject x2) whose high dwords also shape u+4;
            # the subject's own dword AND at u+4 lands between the
            # two subject qword masks.
            q0 = w.q(ua)
            lo, hi = q0 & 0xFFFFFFFF, q0 >> 32
            if gated:
                lo &= 0xFFBFFFFF
                hi &= 0xFFFFBFFF
            lo &= 0xEFFFFFDF                       # 310780 qword mask
            lo &= 0x5FFFCFFF; hi &= 0xFFFFBFF7     # subject mask 1
            hi &= 0xFFDFFF7F                       # subject dword AND +4
            lo &= 0xFEFFFFFF; hi &= 0xFFF3FFFF     # subject mask 2
            q0f = lo | (hi << 32)

            def src(o, n):
                return int.from_bytes(
                    w.q(b88 + o).to_bytes(8, "little")[:n], "little") \
                    if b88 else 0
            # 30EDA0 copies src[0..0x4EF] -> u+0x6B0..0xB9F before
            # RESET's own writes; u+0x730.. = q[u+0x718..] post-copy.
            v730 = src(0x68, 8) if gated else w.q(ua + 0x718)
            v738 = src(0x70, 8) if gated else w.q(ua + 0x720)
            v740 = src(0x78, 8) if gated else w.q(ua + 0x728)
            v700 = (src(0x50, 4) if gated else w.d(ua + 0x700)) \
                & 0xFFFFFFFC
            v778 = (src(0xC8, 1) if gated else w.b(ua + 0x778)) & 1
            v980 = src(0x2D0, 8) if gated else w.q(ua + 0x980)
            obs = [
                (ua + 0, 8, q0f),
                (ua + 4, 4, hi),
                (ua + 0x690, 4, 0),
                (ua + 0x694, 1, 0xFF),
                (ua + 0x695, 1, 0xFF),
                (ua + 0x696, 1, 0xFF),
                (ua + 0x6B4, 1, 0),
                (ua + 0x6B6, 1, 0),
                (ua + 0x6B7, 2, 0),
                (ua + 0x6D0, 8, 0),
                (ua + 0x6D8, 8, 0),
                (ua + 0x700, 4, v700),
                (ua + 0x708, 8, 0),
                (ua + 0x710, 4, 0),
                (ua + 0x714, 2, 0xFFFF),
                (ua + 0x730, 8, v730),
                (ua + 0x738, 8, v738),
                (ua + 0x740, 8, v740),
                (ua + 0x75C, 4, 0),
                (ua + 0x760, 8, 0),
                (ua + 0x768, 8, 0),
                (ua + 0x778, 1, v778),
                (ua + 0x779, 2, 0),
                (ua + 0x780, 8, 0),
                (ua + 0x978, 8, 0),
                (ua + 0x980, 8, v980),
                (ua + 0x80 + 0x120, 4, 0),
                (ua + 0x80 + 0x124, 8, 0),
                (ua + 0x80 + 0x170, 4,
                 w.d(ua + 0x80 + 0x170) & 0xFFFFFFDF),
            ]
            if gated:
                obs += [
                    (ua + 0x28, 4, 0),
                    (ua + 0x6C0, 8, src(0x10, 8)),
                    (ua + 0x6F0, 8, src(0x40, 8)),
                    (ua + 0xB00, 8, src(0x450, 8)),
                    (ua + 0xB88, 8, src(0x4D8, 8)),
                    (ua + 0xDC8, 2, 0),   # in-image table is BSS
                    (ua + 0xE58, 4, 0),
                ]
            bit = ~(1 << w.b(ua + 0xEA9)) & 0xFFFFFFFF
            for i in range(w.d(G_COUNT)):
                el = w.q(G_POOL) + i * STRIDE
                obs.append((el + 0xEA0, 4, w.d(el + 0xEA0) & bit))
            out["obs"] = obs
            # 336710 (inside ~z9b) runs GET(byte[u+0x1F7]); count 0
            # returns null -> read [rax+8] faults.
            if w.d(G_COUNT) == 0:
                out["fault"] = "0x8"
        return out

    if ent == "sink":
        ebx = m.m_sink_body(ua, out)
        if ebx is None:
            return out
        u4 = w.d(ua + 4)
        if ebx:
            out["u4"] = (u4 & ~0x10000 & 0xFFFFFFFF) | 0x10000
            if out.get("u4clr400"):
                out["u4"] = ((u4 & ~0x400 & ~0x10000) & 0xFFFFFFFF) | 0x10000
        else:
            out["u4"] = u4 & ~0x10600 & 0xFFFFFFFF
        return out

    # ---- APPLY / CASCADE ----
    if ent == "apply":
        m.qret = case.get("qret", {})
        m.m_apply(ua, case.get("bitidx", 0), case.get("arg3", 0),
                  case.get("aflags", 0), case.get("aaction", 0))
        # ~fed's nested APPLY re-clears bits the dispatch set: last wins
        seen = {}
        for a, n, v in m.obs:
            seen[(a, n)] = (a, n, v)
        out["obs"] = list(seen.values())
        return out

    if ent == "casc":
        m.qret = case.get("qret", {})
        rsi = case.get("cobj", COBJ)
        m.m_casc(rsi, case.get("u2obj", REC), case.get("bitidx", 0),
                 s32(case.get("arg4", 0)), s32(case.get("arg5", 0)),
                 case.get("cflags", 0), case.get("caction", 0))
        # nested cascade writes can overwrite parent fields: last wins
        seen = {}
        for a, n, v in m.obs:
            seen[(a, n)] = (a, n, v)
        out["obs"] = list(seen.values())
        return out

    # ---- TAIL ----
    rc = case.get("rec_ptr", REC)
    fl = case.get("tflags", 0)
    ebp = (~(fl >> 1)) & 1
    r15 = fl & 0x410
    u12 = m.m_find(rc)
    cx = s16(w.h(rc + 0x28))
    if cx <= 0:
        out["rc4e"] = w.b(rc + 0x4E)
        return out
    esi = w.b(rc + 0x4E)
    ebx = (s16(w.h(rc + 6)) // cx) if w.b(rc + 0x37) else 0
    if ebp and esi != ebx:
        m.emit("d")                    # shipped ret-0 no-op
    if r15 == 0x400 and u12 and esi != ebx:
        iD = m.emit("D%x,%x" % (u12 & 0xFFFFFFFF,
                                (ebx - esi) & 0xFFFFFFFF))
        rv = m.m_rng(w.q(u12 + 0x10))
        if rv:
            fidx = ((1 if ebx > esi else 0) * 2) | 1
            rec_ = w.q(u12 + 0x698)
            if not rec_ or w.b(rec_ + 5) != 0:
                fv = m.m_fam(w.q(u12 + 0x10))
                if fv != 3:
                    fidx += 4
            m.emit("P%x" % case["_paddr"])
        m.done(iD, 0)
    out["rc4e"] = ebx & 0xFF
    return out


def compare(case, world):
    w = Fx(world.planted)
    exp = model(case, w, world)
    got = " ".join(world.trace)
    expt = " ".join(exp.get("trace", []))
    # FMT arg is a stack address -- normalize
    import re
    norm = lambda s: re.sub(r"P[0-9a-f]+", "P", s)
    ok = norm(got) == norm(expt)
    diffs = []
    if not ok:
        diffs.append("trace")
    ua = world.uaddr
    if case.get("entry", "sink") == "sink":
        got_u4 = struct.unpack("<I", world.gm.r(ua + 4, 4))[0]
        if "u4" in exp and got_u4 != exp["u4"]:
            ok = False
            diffs.append("u4 got=%x exp=%x" % (got_u4, exp["u4"]))
        for k, addr, n in (("gbyte", G_GBYTE, 1), ("gqw", G_GQW, 8),
                           ("udcc", ua + 0xDCC, 4)):
            if k in exp:
                gv = int.from_bytes(world.gm.r(addr, n), "little")
                if gv != exp[k]:
                    ok = False
                    diffs.append("%s got=%x exp=%x" % (k, gv, exp[k]))
    else:
        got = world.gm.r(case.get("rec_ptr", REC) + 0x4E, 1)[0]
        if "rc4e" in exp and got != exp["rc4e"]:
            ok = False
            diffs.append("rc4e got=%x exp=%x" % (got, exp["rc4e"]))
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
    return ok, diffs, " ".join(world.trace), expt


def unit_spec(rec=REC, u4=0x200, u708=0, bc4=0, ea4=0, ea9=0, b6b6=0,
              w714=0, d710=0, u10=0, b0=0x10, dcc=0x9999, bc8=(), **kw):
    spec = {"q": {0x698: rec, 0x708: u708, 0x10: u10},
            "d": {0x4: u4, 0xBC4: bc4, 0xEA4: ea4,
                  0x710: d710, 0xDCC: dcc},
            "h": {0x714: w714},
            "b": {0x0: b0, 0x6B6: b6b6}}
    for i, p in enumerate(bc8):
        spec["q"][0xBC8 + i * 0x10] = p
    return spec


def build_cases():
    C = []
    def add(name, **kw):
        kw["name"] = name
        C.append(kw)

    # ---- SINK ----
    add("sink-band1a", entry="sink",
        unit=unit_spec(u4=0x200),
        rec={"b": {4: 0x1A, 5: 0}}, matches=[True])
    add("sink-flag-hit", entry="sink",
        unit=unit_spec(u4=0x600),
        rec={"b": {4: 0x10, 5: 0}, "d": {0x64: 0x8000000}},
        matches=[True])
    add("sink-uflag-clear", entry="sink",
        unit=unit_spec(u4=0x10600),
        rec={"b": {4: 0x10, 5: 0}}, matches=[True],
        globals={"utab_entries": [0x8000]})
    add("sink-gchk-sidefx", entry="sink",
        unit=unit_spec(u4=0x10600),
        rec={"b": {4: 0x10, 5: 0}}, matches=[True],
        globals={"mode": 0})
    # LSCAN hit: two carriers -- first a miss (blank B), second UNIT2.
    # rel=2 needs ebp==eax==0: A NOT ok (rec+5!=0, famA!=3) + B ok.
    add("sink-lscan-hit", entry="sink",
        unit=unit_spec(u4=0x600, bc4=2, bc8=(CARR, CARR + 0x40),
                       u10=VECP),
        rec={"b": {4: 0x10, 5: 1}},
        carriers=[{"q": {0x30: MISS}}, {"q": {0x30: UNIT2}}],
        objs={MISS: {"q": {0x10: VECP}}},
        unit2={"q": {0x698: REC2, 0x10: VECP}, "b": {0: 0x10}},
        rec2={"b": {5: 0}},
        matches=[True])
    # LSCAN true miss + 0x400 -> set bit16: both-ok (ebp=1) != eax=0
    add("sink-lscan-miss-400", entry="sink",
        unit=unit_spec(u4=0x600, bc4=1, bc8=(CARR,), u10=VECP),
        rec={"b": {4: 0x10, 5: 0}},
        carriers=[{"q": {0x30: UNIT2}}],
        unit2={"q": {0x698: REC2, 0x10: VECP}, "b": {0: 0x10}},
        rec2={"b": {5: 0}},
        matches=[True])
    # LSCAN true miss + no 0x400 -> clear
    add("sink-lscan-miss-clear", entry="sink",
        unit=unit_spec(u4=0x200, bc4=1, bc8=(CARR,), u10=VECP),
        rec={"b": {4: 0x10, 5: 0}},
        carriers=[{"q": {0x30: UNIT2}}],
        unit2={"q": {0x698: REC2, 0x10: VECP}, "b": {0: 0x10}},
        rec2={"b": {5: 0}},
        matches=[True])
    # BSCAN hit (A not-ok + B ok -> rel=2) + MEMB miss -> set
    add("sink-bscan-memb-miss", entry="sink",
        unit=unit_spec(u4=0, ea4=0x4, u708=0x9999, u10=VECP),
        rec={"b": {4: 0x10, 5: 1}},
        poolspec={2: {"q": {0x698: REC2, 0x10: VECP}, "b": {0: 0x10}}},
        rec2={"b": {5: 0}},
        matches=[True], count=3,
        globals={"cnt1": 1})
    # BSCAN hit + MEMB hit (u708 == G_TB1+24, slot idx1) -> clear
    # (u4 has 0x400 but NOT 0x200 so the u4mask mutant flips into LSCAN)
    add("sink-bscan-memb-hit", entry="sink",
        unit=unit_spec(u4=0x10400, ea4=0x4, u708=G_TB1 + 24, u10=VECP),
        rec={"b": {4: 0x10, 5: 1}},
        poolspec={2: {"q": {0x698: REC2, 0x10: VECP}, "b": {0: 0x10}}},
        rec2={"b": {5: 0}},
        matches=[True], count=3,
        globals={"cnt1": 2})
    # BSCAN high bit (k=18 >= 0x10): exercises the 0x20 loop bound
    add("sink-bscan-highbit", entry="sink",
        unit=unit_spec(u4=0x10400, ea4=0x40000, u708=0x9999, u10=VECP),
        rec={"b": {4: 0x10, 5: 1}},
        poolspec={18: {"q": {0x698: REC2, 0x10: VECP}, "b": {0: 0x10}}},
        rec2={"b": {5: 0}},
        matches=[True], count=19,
        globals={"cnt1": 0, "cnt2": 0})
    # BRES path: BSCAN miss (ea4=0) -> ORC calls BRES; w714 id + handle
    add("sink-bres-rel", entry="sink",
        unit=unit_spec(u4=0, ea4=0, w714=0x42, d710=0x330000, u10=VECP),
        rec={"b": {4: 0x10, 5: 1}},
        unit2={"q": {0x698: REC2, 0x10: VECP}, "b": {0: 0x10}},
        rec2={"b": {5: 0}},
        matches=[True], count=1,
        globals={"fam_recs": {3: {"bound": 4, "count": 1,
                                  "elements": [{"tag": 3,
                                                "obj": UNIT2}]}}})
    # rec null -> UFLAG then fault reading [0+0x64]
    add("sink-norec-fault", entry="sink",
        unit=unit_spec(rec=0, u4=0x10600),
        matches=[False], count=1)
    # REL A-rec-null fault through LSCAN: rec=0 but famA!=5 path
    add("sink-rel-fault", entry="sink",
        unit=unit_spec(rec=0, u4=0x200, bc4=1, bc8=(CARR,), u10=VECP),
        rec2={"b": {5: 0}},
        carriers=[{"q": {0x30: UNIT2}}],
        unit2={"q": {0x698: REC2, 0x10: VECP}, "b": {0: 0x10}},
        matches=[False], count=1,
        globals={"mode": 1, "gbyte": 0xFF})
    # u4&0x200 path needs GCHK false first: mode=1 default ok
    # MEMB table2 coverage (u708 == G_TB2 slot 0) -> clear
    add("sink-bscan-memb-t2", entry="sink",
        unit=unit_spec(u4=0x10400, ea4=0x4, u708=G_TB2, u10=VECP),
        rec={"b": {4: 0x10, 5: 1}},
        poolspec={2: {"q": {0x698: REC2, 0x10: VECP}, "b": {0: 0x10}}},
        rec2={"b": {5: 0}},
        matches=[True], count=3,
        globals={"cnt2": 1})
    # fam5 refusal inside REL (B's fam nibble = 5)
    add("sink-rel-fam5", entry="sink",
        unit=unit_spec(u4=0x200, bc4=1, bc8=(CARR,), u10=VECP),
        rec={"b": {4: 0x10, 5: 0}},
        carriers=[{"q": {0x30: UNIT2}}],
        unit2={"q": {0x698: REC2, 0x10: VECP + 0x200},
               "b": {0: 0x10}},
        rec2={"b": {5: 0}},
        rows={VECP + 0x20E: 5},
        matches=[True])

    # ---- TAIL ----
    add("tail-basic", entry="tail", tflags=0x0,
        rec={"b": {0x37: 1, 0x4E: 3}, "h": {0x28: 4, 0x6: 40}},
        matches=[True])
    add("tail-notify", entry="tail", tflags=0x400,
        rec={"b": {0x37: 1, 0x4E: 3}, "h": {0x28: 4, 0x6: 40}},
        unit=unit_spec(u10=VECP),
        matches=[True])
    add("tail-nodiv", entry="tail", tflags=0x400,
        rec={"b": {0x37: 1, 0x4E: 3}, "h": {0x28: 0, 0x6: 40}},
        matches=[True])
    add("tail-zero", entry="tail", tflags=0x400,
        rec={"b": {0x37: 0, 0x4E: 3}, "h": {0x28: 4, 0x6: 40}},
        matches=[True])
    add("tail-findmiss", entry="tail", tflags=0x400,
        rec={"b": {0x37: 1, 0x4E: 3}, "h": {0x28: 4, 0x6: 40}},
        matches=[False], count=1)
    add("tail-noebp", entry="tail", tflags=0x402,
        rec={"b": {0x37: 1, 0x4E: 3}, "h": {0x28: 4, 0x6: 40}},
        unit=unit_spec(u10=VECP),
        matches=[True])
    add("tail-equal", entry="tail", tflags=0x400,
        rec={"b": {0x37: 1, 0x4E: 10}, "h": {0x28: 4, 0x6: 40}},
        unit=unit_spec(u10=VECP),
        matches=[True])
    add("tail-rng-fail", entry="tail", tflags=0x400,
        rec={"b": {0x37: 1, 0x4E: 3}, "h": {0x28: 4, 0x6: 40}},
        unit=unit_spec(u10=0),
        matches=[True])
    # rec+5 != 0 -> UNOT calls FAM on u12[0x10]; fam==3 -> ecx stays 0
    add("tail-notify-fam3", entry="tail", tflags=0x400,
        rec={"b": {0x37: 1, 0x4E: 3, 5: 1}, "h": {0x28: 4, 0x6: 40}},
        unit=unit_spec(u10=VECP + 0x200),
        rows={VECP + 0x20E: 3},
        matches=[True])

    # ---- RESET (003105D0) ----
    def reset_spec(b694=7, b695=3, b696=5, ea9=2, w714=0x1234, rec=REC,
                   b88=SRCP, u0=0xFFFFFFFFFFFFFFFF):
        return {"q": {0x698: rec, 0x0: u0, 0xB88: b88,
                      0x6D0: 0x1111, 0x6D8: 0x2222, 0x708: 0x3333,
                      0x718: 0xAAAA, 0x720: 0xBBBB, 0x728: 0xCCCC,
                      0x760: 0x4444, 0x768: 0x5555,
                      0x778: 0xFFFFFFFFFFFFFFFF,
                      0x780: 0xAAAABBBBCCCCDDDD,
                      0x978: 0x1111222233334444,
                      0x980: 0x5A5A5A5A5A5A5A5A},
                "d": {0x4: 0xFFFFFFFF, 0x690: 0x777, 0x700: 0xFFFFFFFF,
                      0x710: 0x888, 0x75C: 0x999, 0x1F0: 0xFFFFFFFF},
                "h": {0x6B7: 0xABC, 0x714: w714},
                "b": {0x694: b694, 0x695: b695, 0x696: b696,
                      0x6B4: 0x66, 0x6B6: 0x77, 0xEA9: ea9,
                      0x1F7: 1}}
    srcpat = {SRCP: {"q": {i * 8: 0x5000 + i for i in range(0x9E)}}}
    add("reset-basic", entry="reset",
        unit=reset_spec(),
        rec={"b": {4: 0x10, 5: 1}}, matches=[True, False, False], count=3,
        poolspec={0: {"d": {0xEA0: 0xFFFFFFFF}},
                  1: {"d": {0xEA0: 0xFFFFFFFF}},
                  2: {"d": {0xEA0: 0xFFFFFFFF}}},
        objs=srcpat)
    add("reset-norec", entry="reset",
        unit=reset_spec(rec=0), matches=[False], count=1)
    add("reset-count0", entry="reset",
        unit=reset_spec(),
        rec={"b": {4: 0x10, 5: 1}}, matches=[True], count=0,
        objs=srcpat)
    add("reset-ea9-31", entry="reset",
        unit=reset_spec(ea9=31),
        rec={"b": {4: 0x10, 5: 1}}, matches=[True, False], count=2,
        poolspec={0: {"d": {0xEA0: 0xFFFFFFFF}},
                  1: {"d": {0xEA0: 0xFFFFFFFF}}},
        objs=srcpat)
    add("reset-b88-null", entry="reset",
        unit=reset_spec(b88=0),
        rec={"b": {4: 0x10, 5: 1}}, matches=[True], count=1)
    add("reset-bit22-clear", entry="reset",
        unit=reset_spec(u0=0xFFFFFFFFFFBFFFFF),
        rec={"b": {4: 0x10, 5: 1}}, matches=[True, False], count=2,
        poolspec={0: {"d": {0xEA0: 0xFFFFFFFF}},
                  1: {"d": {0xEA0: 0xFFFFFFFF}}},
        objs=srcpat)

    # ---- APPLY ----
    # gate table: G_F22T -> F22TP; dword[F22TP+4] = count
    F22 = {"f22tab": F22TP}
    T4 = {F22TP: {"d": {4: 4}}}
    T40 = {F22TP: {"d": {4: 0x40}}}
    T80 = {F22TP: {"d": {4: 0x80}}}

    add("apply-gate-null", entry="apply",
        unit={"b": {0x68: 1}}, matches=[True], bitidx=0, aaction=0)
    add("apply-gate-oob", entry="apply",
        unit={"b": {0x68: 1}}, matches=[True], bitidx=8, aaction=0,
        globals=F22, objs=T4)
    add("apply-gate-edge", entry="apply",
        unit={"b": {0x68: 1}}, matches=[True], bitidx=4, aaction=0,
        globals=F22, objs=T4)
    add("apply-clr68", entry="apply",
        unit={"b": {0x68: 1}}, matches=[True], bitidx=0, aaction=0,
        globals=F22, objs=T40)
    add("apply-clr68-noop", entry="apply",
        unit={"b": {0x68: 0}}, matches=[True], bitidx=0, aaction=0,
        globals=F22, objs=T40)
    add("apply-clr-wrong", entry="apply",
        unit={"b": {0x78: 1}}, matches=[True], bitidx=0, aaction=0,
        globals=F22, objs=T40)
    add("apply-set78", entry="apply",
        unit={"b": {0x78: 0}}, matches=[True], bitidx=1, aaction=3,
        globals=F22, objs=T40)
    add("apply-set78-noop", entry="apply",
        unit={"b": {0x78: 2}}, matches=[True], bitidx=1, aaction=3,
        globals=F22, objs=T40)
    add("apply-stub34", entry="apply",
        unit={"b": {0x6E: 0}}, matches=[True], bitidx=0x34, aaction=2,
        globals=F22, objs=T40)
    add("apply-flag2-skip", entry="apply",
        unit={"b": {0x68: 1}}, matches=[True], bitidx=0, aaction=0,
        aflags=2, globals=F22, objs=T40)
    add("apply-flag9-skip", entry="apply",
        unit={"b": {0x68: 1}}, matches=[True], bitidx=0, aaction=0,
        aflags=0x200, globals=F22, objs=T40)
    add("apply-b79b", entry="apply",
        unit={"b": {0x75: 0}}, matches=[True], bitidx=0x68, aaction=2,
        globals=F22, objs=T80)
    add("apply-action-oob", entry="apply",
        unit={"b": {0x68: 1}}, matches=[True], bitidx=0, aaction=7,
        globals=F22, objs=T40)
    add("apply-set68-highidx", entry="apply",
        unit={"b": {0x6F: 0}}, matches=[True], bitidx=63, aaction=2,
        globals=F22, objs=T40)

    # ---- CASCADE ----
    # rsi=COBJ (status object), u2=REC -> owner uaddr; COBJ's owner is
    # pool element 1 (poolspec plants its +0x698). count=2.
    CB = dict(entry="casc", cobj=COBJ, u2obj=REC, matches=[True], count=2)
    E1 = {1: {"q": {0x698: COBJ}}}

    def cspec(d38=0, d3c=0, d64=0, d48=0, b4=0, b5=0):
        return {"d": {0x38: d38, 0x3C: d3c, 0x64: d64, 0x48: d48},
                "b": {4: b4, 5: b5}}

    add("casc-clr64", **CB, bitidx=2, caction=0, cflags=1,
        arg4=0x1234, arg5=0x5678,
        objs={COBJ: cspec(d64=4)}, poolspec=E1)
    add("casc-set38", **CB, bitidx=3, caction=5, cflags=1,
        objs={COBJ: cspec()}, poolspec=E1)
    add("casc-set64-gate", **CB, bitidx=1, caction=3, cflags=1,
        objs={COBJ: cspec(d38=2)}, poolspec=E1)
    add("casc-elig-fail", **CB, bitidx=4, caction=0, cflags=0,
        objs={COBJ: cspec(d64=0x10)}, poolspec=E1,
        qret={V_B9B: 1})
    add("casc-elig-b8e", **CB, bitidx=0, caction=3, cflags=0,
        objs={COBJ: cspec(d64=1)}, poolspec=E1,
        qret={V_B8E: 1})
    add("casc-elig-non34", **CB, bitidx=4, caction=0, cflags=0,
        arg4=0x99, arg5=0xAA,
        objs={COBJ: cspec(d64=0x10)}, poolspec=E1)
    add("casc-recok-dispatch", **CB, bitidx=4, caction=4, cflags=0,
        arg4=0x99, arg5=0xAA,
        objs={COBJ: cspec(d64=0x10, b4=0x1B),
              CGTP: {"h": {8: 0x20}, "d": {0xC: 0x100}}},
        poolspec=E1, globals={"cgtab": CGTP})
    add("casc-sfc-exit", **CB, bitidx=0, caction=3, cflags=0,
        objs={COBJ: cspec(d64=1, b4=0x1B)}, poolspec=E1)
    add("casc-uflag-pass", **CB, bitidx=0, caction=3, cflags=0,
        objs={COBJ: cspec(d3c=1, b4=0x40),
              CGTP: {"h": {8: 0x20}, "d": {0xC: 0x100}}},
        poolspec=E1, globals={"utab_entries": [0x8000],
                              "cgtab": CGTP})
    add("casc-uflag-fail", **CB, bitidx=0, caction=3, cflags=0,
        objs={COBJ: cspec(d3c=1, b4=0x40)}, poolspec=E1,
        globals={"utab_entries": [0x0000]})
    add("casc-action-oob", **CB, bitidx=2, caction=9, cflags=1,
        objs={COBJ: cspec(d64=4)}, poolspec=E1)
    add("casc-flag9-skip", **CB, bitidx=2, caction=0, cflags=0x201,
        objs={COBJ: cspec(d64=4)}, poolspec=E1)
    add("casc-arg4neg", **CB, bitidx=1, caction=0, cflags=1,
        arg4=-1, arg5=-1,
        objs={COBJ: cspec(d64=2)}, poolspec=E1,
        qret={V_773: 0xB, V_76D: 0x21E})
    add("casc-arm-99b", **CB, bitidx=4, caction=4, cflags=1,
        objs={COBJ: cspec(), CGTP: {"h": {8: 0x20}, "d": {0xC: 0x100}}},
        poolspec=E1, globals={"cgtab": CGTP})
    add("casc-arm-114", **CB, bitidx=0, caction=0, cflags=1,
        objs={COBJ: cspec(d64=1)}, poolspec=E1)
    add("casc-arm-e9a0", **CB, bitidx=8, caction=3, cflags=1,
        objs={COBJ: cspec(), CGTP: {"h": {8: 0x20}, "d": {0xC: 0x100}}},
        poolspec={1: {"q": {0x698: COBJ}, "b": {0xE9A: 1}}},
        rec={"b": {5: 1}},
        globals={"cgtab": CGTP})
    add("casc-arm-sink", **CB, bitidx=5, caction=0, cflags=1,
        objs={COBJ: cspec(d64=0x20, b4=0x1A)},
        poolspec={1: {"q": {0x698: COBJ}, "b": {0x6B4: 5},
                      "d": {4: 0x200}}})
    add("casc-arm27-sink", **CB, bitidx=27, caction=0, cflags=1,
        objs={COBJ: cspec(d64=0x8000000, b4=0x1A)},
        poolspec={1: {"q": {0x698: COBJ}, "b": {0x6B4: 5},
                      "d": {4: 0x200}}})
    add("casc-arm-full", **CB, bitidx=0, caction=3, cflags=1,
        objs={COBJ: cspec(), CGTP: {"h": {8: 0x20}, "d": {0xC: 0x100}}},
        poolspec=E1, globals={"cgtab": CGTP})
    add("casc-arm31", **CB, bitidx=31, caction=3, cflags=1,
        objs={COBJ: cspec(), CGTP: {"h": {8: 0x20}, "d": {0xC: 0x100}}},
        poolspec=E1, globals={"cgtab": CGTP})
    add("casc-recurse", **CB, bitidx=2, caction=3, cflags=1,
        objs={COBJ: cspec(), CGTP: {"h": {8: 0x20}, "d": {0xC: 0x100}},
              RESB + 0x14C: {"d": {0: 0x25}}},
        poolspec=E1, globals={"cgtab": CGTP})
    return C


def run_case(case, raw, secs):
    world = World(case, raw, secs)
    uc = world.uc
    ent = case.get("entry", "sink")
    entry = {"sink": SINK, "tail": TAIL, "reset": RESET,
             "apply": APPLY, "casc": CASC}[ent]
    sp = STACK + 0x80000
    uc.reg_write(UC_X86_REG_RSP, sp)
    world.w(sp, qw(RETQ))
    if ent == "tail":
        uc.reg_write(UC_X86_REG_RCX, case.get("rec_ptr", REC))
    elif ent == "casc":
        uc.reg_write(UC_X86_REG_RCX, case.get("cobj", COBJ))
    else:
        uc.reg_write(UC_X86_REG_RCX, world.uaddr)
    uc.reg_write(UC_X86_REG_RDX, case.get("tflags", 0))
    if ent == "apply":
        uc.reg_write(UC_X86_REG_RDX, case.get("bitidx", 0))
        uc.reg_write(UC_X86_REG_R8, case.get("arg3", 0))
        uc.reg_write(UC_X86_REG_R9, case.get("aflags", 0))
        world.w(sp + 0x28, qw(case.get("aaction", 0)))
    elif ent == "casc":
        uc.reg_write(UC_X86_REG_RDX, case.get("u2obj", REC))
        uc.reg_write(UC_X86_REG_R8, case.get("bitidx", 0))
        uc.reg_write(UC_X86_REG_R9,
                     case.get("arg4", 0) & 0xFFFFFFFFFFFFFFFF)
        world.w(sp + 0x28, qw(case.get("arg5", 0)))
        world.w(sp + 0x30, qw(case.get("cflags", 0)))
        world.w(sp + 0x38, qw(case.get("caction", 0)))
    uc.reg_write(UC_X86_REG_RIP, entry)
    # FMT arg is &local inside UNOT: TAIL frame = 3 pushes + sub 0x20
    # (0x38), call pushes ret (-8), UNOT pushes rdi + sub 0x30 (0x38) ->
    # arg = rsp+0x20 = entry_sp - 0x58.
    case["_paddr"] = sp - 0x58
    try:
        uc.emu_start(entry, RETQ, count=600000)
    except Exception as e:
        world.faults.append(("EMU", str(e),
                             "rip=%x" % uc.reg_read(UC_X86_REG_RIP)))
    return world


def build_mutants():
    M = []
    def add(name, va, orig, patch):
        M.append({"name": name, "va": va, "orig": orig, "patch": patch})
    add("m-sink-band", 0x307D34, b"\x1a", b"\x1b")        # rec+4 band 0x1a->0x1b
    add("m-sink-diffmask", 0x307D5D, b"\x20\x00\x00\x08",
        b"\x20\x00\x00\x04")                             # 0x8000020 -> 0x4000020
    add("m-sink-u4mask", 0x307D87, b"\x00\x02\x00\x00",
        b"\x00\x04\x00\x00")                             # test 0x200 -> 0x400
    add("m-sink-bit16", 0x307DE1, b"\x10", b"\x11")      # shl ebx,0x10 -> 0x11
    add("m-sink-clrmask", 0x307DD4, b"\xff\xf9\xff\xff",
        b"\xff\xfb\xff\xff")                             # ~0x600 -> ~0x400
    add("m-memb-stride", 0x30BF4E, b"\x52", b"\x92")     # idx*3 -> idx*5
    add("m-lscan-stride", 0x30B0A7, b"\x10", b"\x08")    # entry step +0x10 -> +8
    add("m-bscan-bound", 0x30C29D, b"\x20", b"\x10")     # bit bound 0x20 -> 0x10
    add("m-tail-mask", 0x30E07D, b"\x10\x04\x00\x00",
        b"\x10\x02\x00\x00")                             # &0x410 -> &0x210
    add("m-tail-write", 0x30E113, b"\x4e", b"\x4f")      # [rdi+0x4e] -> +0x4f
    add("m-gchk-sete", 0x253B98, b"\x0f\x94\xc0",
        b"\x0f\x95\xc0")                                 # sete -> setne
    add("m-rel-sete", 0x30AC22, b"\x0f\x94\xc1",
        b"\x0f\x95\xc1")                                 # sete cl -> setne
    add("m-apply-gate", 0x323030, b"\x0f\x8c",
        b"\x0f\x8d")                                     # bitidx<0 exit jl -> jge
    add("m-apply-a0exit", 0x30E244, b"\x0f\x84",
        b"\x0f\x85")                                     # bit-set exit je -> jne
    add("m-apply-notifygate", 0x30E2E4, b"\x74\x1d",
        b"\x75\x1d")                                     # ~472/~479 gate je -> jne
    add("m-apply-a02flag", 0x30E191, b"\xfd\xff\xff\xff",
        b"\xfb\xff\xff\xff")                             # flag {0,2} -> {0,4}
    add("m-apply-fedskip", 0x30E320, b"\x09", b"\x08")   # bt r12d,9 -> 8
    add("m-casc-a0exit", 0x30E4EC, b"\x0f\x84",
        b"\x0f\x85")                                     # a0 bit-clear exit je -> jne
    add("m-casc-a3gate", 0x30E52B, b"\x0f\x85",
        b"\x0f\x84")                                     # a3 bit-set jne -> je
    add("m-casc-is34", 0x30E43D, b"\x0f\x84",
        b"\x0f\x85")                                     # is34 gate je -> jne
    add("m-casc-armmap", 0x30E8C8, b"\x03", b"\x04")     # arm 3 -> 4 (bitidx4)
    add("m-casc-presence", 0x30E407, b"\x0b\x46\x64",
        b"\x0b\x46\x65")                                 # or eax,[rsi+0x64] -> +0x65
    return M


MSPEC = {
    "m-sink-band": "sink-band1a",
    "m-sink-diffmask": "sink-flag-hit",
    "m-sink-u4mask": "sink-bscan-memb-hit",
    "m-sink-bit16": "sink-band1a",
    "m-sink-clrmask": "sink-uflag-clear",
    "m-memb-stride": "sink-bscan-memb-hit",
    "m-lscan-stride": "sink-lscan-hit",
    "m-bscan-bound": "sink-bscan-highbit",
    "m-tail-mask": "tail-notify",
    "m-tail-write": "tail-basic",
    "m-gchk-sete": "sink-gchk-sidefx",
    "m-rel-sete": "sink-lscan-hit",
    "m-apply-gate": "apply-clr68",
    "m-apply-a0exit": "apply-clr68",
    "m-apply-notifygate": "apply-clr68",
    "m-apply-a02flag": "apply-stub34",
    "m-apply-fedskip": "apply-flag9-skip",
    "m-casc-a0exit": "casc-clr64",
    "m-casc-a3gate": "casc-arm-full",
    "m-casc-is34": "casc-elig-non34",
    "m-casc-armmap": "casc-arm-99b",
    "m-casc-presence": "casc-clr64",
}


def main():
    global raw_, secs_
    raw, secs = load_image()
    raw_, secs_ = raw, secs
    cases = build_cases()
    res = {"exe_sha256": SHA,
           "subjects": {"sink": "0x307D10", "tail": "0x30E060",
                        "reset": "0x3105D0", "apply": "0x30E130",
                        "casc": "0x30E360"},
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
        print("CASE %-4s %-24s %s" % ("ok" if ok else "FAIL",
                                      c["name"], got_t[:110]))
        if not ok:
            print("      exp: %s" % exp_t[:110])
            for d in diffs:
                print("      diff: %s" % d)
    print("cases: %d/%d" % (npass, len(cases)))

    print("\n-- mutants --")
    mkilled = 0
    muts = build_mutants()
    for m in muts:
        orig = img(raw, secs, m["va"], len(m["orig"]))
        assert orig == m["orig"], "%s site bytes %s != %s" % (
            m["name"], orig.hex(), m["orig"].hex())
    for m in muts:
        cname = MSPEC[m["name"]]
        c = dict(next(x for x in cases if x["name"] == cname))
        c["patch_bytes"] = [(m["va"], m["patch"])]
        world = run_case(c, raw, secs)
        ok, diffs, got_t, exp_t = compare(c, world)
        if not ok:
            mkilled += 1
            print("MUT KILLED %-18s case=%-24s" % (m["name"], cname))
        else:
            print("MUT ALIVE  %-18s case=%s" % (m["name"], cname))
    print("mutants: %d/%d killed" % (mkilled, len(muts)))
    json.dump(res, open("result.json", "w"), indent=1)


raw_ = secs_ = None
if __name__ == "__main__":
    main()
