# EXP-093 - hp-write callee execution
#
# CONTRACT-hp-write-and-lethal-transition.md section 5 ran diff_hp_write.py with
# TWELVE scripted callees (find_unit, gate1, field_bit15, rx, nb, find_tbuf,
# gate3, st, kh, clk, gd, ev). This harness re-drives 00300530 / 00300520 with
# every callee running as shipped bytes plus their bounded transitive closure.
#
#   ENTRY BODIES (shipped bytes, canonical VA):
#     00300530  (rcx=tgt stats, edx=delta, r8=src stats|0, r9d=flags)
#     00300520  absolute-set thunk: edx -= [rcx+0x48]; jmp 00300530
#
#   REAL CALLEES (the formerly scripted twelve):
#     0031B860 find_unit  - scans [0x208E6A0] slots of [0x208E688] for +0x698==rec
#     0030B9B0 gate1     - relat>1 -> flag_builder|context_gate low word test
#     00377C20 field15   - field-index -> [0x2ADD100] table row bit15
#     003283D0 rx        - proximity gate -> reaction record -> 003BBD00 post
#     0028F1F0 nb        - view-table scan -> 003F8980 {old,new} pair publish
#     00316D70 find_tbuf - count at [rcx+4], 16B entries at [rcx+8]
#     0030B8E0 gate3     - flag_builder|context_gate HIGH word test
#     0030E360 st        - status transition (EXP-086 fixture)
#     00469BB0 kh        - 002FA390 kind gate -> 0046AB10 ring insert
#     0032A150 clk       - mov eax,[0x208D45C]
#     00306F00 gd        - group-completion bitmask + side effects
#     003299B0 ev        - event id transform (|0x5000 for ids>=0x100) -> 002EB030
#
#   TRANSITIVE CLOSURE (real): 0x236850 0x236820 (slot machinery),
#     0x30AB40 relat, 0x30B770 flag_builder, 0x30B7F0 context_gate,
#     0x17D470 (ctx+0xC20 read), 0x1D50D0 singleton getter ([0x208F428] planted),
#     0x263C20 nibble, 0x2EF640/0x2EF2B0/0x3148F0 field-id chain,
#     0x2FA3B0 proximity, 0x3272A0 viewer-actor, 0x265020 pos copy,
#     0x3A1920 dist+sqrtf, 0x3589B0 composite id, 0x3588B0/0x263FF0 id resolve,
#     0x263E30 [rcx+0x30], 0x3BBD00 queue post (real ring at [0x2B447D0]),
#     0x28FBE0 entry init, 0x506700 entry fill, 0x3EFD00 0x24A5A0 0x2DD7E0
#     0x2DD7B0, 0x296280 view scan / 0x2962C0 default view, 0x3F8980 publish
#     (fnptr=0 -> flag-clear arm), 0x2FA390/0x2F8E90 kill kind, 0x46AB10 ring
#     insert + dedupe, 0x469570 kind lookup, 0x20E600 codec, 0x306F00 chain
#     0x263D30 member idx, 0x2360D0 member map, 0x307140 cap rows,
#     0x2E1C20/0x2E1CA0 cap set/clear on [0x215F1C0], 0x359200/0x359330
#     suppression on [0x22C8000..7], 0x26BD20 [0x209A2C4] byte, 0x238B70/0x238AE0
#     battle-state bits 5/7 + per-unit 0x2E7C10, 0x2EB030 event write +
#     0x2EB0D0 post (early-out arms), 0x808C40 cookie check, ST subtree per
#     EXP-086 (0x3848E0 0x386A50 0x386A70 0x3876D0 0x387730 0x20E600 0x16D6A0
#     0x861EC0 memset thunk).
#
#   STUBBED (disclosed boundaries, patched to ret, args logged):
#     0x5369C0  kill-ledger post-insert presentation callback (deep)
#     0x3112F0  ST transition-result applier
#     0x300FC0  ST KO-arm defeat cleanup (->003105D0 family, EXP-091 scope)
#     0x312280  ST rewards sink
#     0x301140  ST recover
#     0x300140  ST case4 action
#     0x307D10  ST case4 second
#     0x3284D0  ST reaction
#     0x30FED0  ST recompute
#     0x46A800  ST extra_add
#
#   FIXTURE-PLANTED IAT: memset [0x8C2A60]->CODE, sqrtf [0x8C2BB8]->CODE+0x10,
#     rand [0x8C3098]->CODE+0x20 (returns 0).
#
#   KEY GLOBALS: [0x208E6A0]=unit count, [0x208E688]=unit table,
#     [0x208F4C4]=active field idx (via 0x2EF640 static 0x208E280+0x200+0x1044),
#     [0x2ADD100]=field table, [0x2089340]=battle state, [0x22C2158] byte,
#     [0x22C2161] dword, [0x208F428]=ctx singleton, [0x208D45C]=tick,
#     [0x1DFE0B8]=float scale (ships 1.0f), [0x1DFE0B4]=beat/dedupe scale,
#     [0x2B447D0]=queue ptr, [0x2B443BF]/[0x2B443C0] cursors,
#     [0x2EBF018]=kill-kind registry hdr, [0x2EBB54C]=ring cursor,
#     ring [0x2EBB560..0x2EBB6A0] 10x0x20, [0x1F83530]=codec base (0 -> rva==va),
#     [0x22C7FE0]=actor id (0 -> 0x3588B0 early-out), [0x2EBF118]=status reg,
#     views at 0x22C5F40+i*0xC0 (+0x26/+0x7E listen bits, +0xB0 handle, +0x38
#     fnptr, +0x26 bit0 cleared on publish), default view 0x22C2240,
#     [0x209BE80] -> obj whose +0x10F78 gates 0x28FBE0's deep arm.
#
# Memory: GuestMem host buffers via mem_map_ptr (EXP-087 finding: this host's
# unicorn DLLs intermittently fail uc_mem_write/read on mapped pages).

import ctypes, hashlib, json, struct, sys, os
from unicorn import *
from unicorn.x86_const import *

EXE = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe"
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
BASE = 0x120000
IMG_LO, IMG_HI = 0x120000, 0x2F800000

_REPO = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                     "..", "..", "..", "..", ".."))
STATUS_BIN = os.path.join(_REPO, "Database", "Tools", "work", "repos-2d", "vbf",
                          "ps2data", "image", "ff12", "test_battle", "in",
                          "binaryfile", "status_data.bin")

HEAP   = 0x40000000
STACK  = 0x61000000
RETQ   = 0x62000000

# fixture blocks (all inside one HEAP mapping)
RECB    = HEAP + 0x000000    # stats records, stride 0x200
UNITB   = HEAP + 0x400000    # battle units, stride 0xF50
WORKB   = HEAP + 0x800000    # work objects, stride 0x200
SPAWNB  = HEAP + 0x900000    # spawn records, stride 0x40
MMAPB   = HEAP + 0x980000    # member-map tables, stride 0x40
POSB    = HEAP + 0xA00000    # position blocks {x,y,z}
EOBJB   = HEAP + 0xA80000    # event objects {dword}
CTX     = HEAP + 0xB00000    # singleton context (+0xC20 mode)
FLDT    = HEAP + 0xB80000    # field table {+4 count, rows +8 stride 3}
KREG    = HEAP + 0xC00000    # kill-kind registry hdr {+8 stride, +0xC rva}
KROW    = HEAP + 0xC10000    # kill-kind element rows
QUEUE   = HEAP + 0xD00000    # reaction queue 64 x 0x50
HDR     = HEAP + 0xE00000    # status registry hdr
TBL     = HEAP + 0xE10000    # status rows (status_data.bin)
MISC    = HEAP + 0xF00000    # misc objs (0x28FBE0's deep gate target)
CODE    = HEAP + 0xF80000    # fixture code (memset/sqrtf/rand/callback)

HP_WRITE = 0x300530
HP_ABS   = 0x300520

# entry hooks on every real body - logging only, no patching
CALLS = {
    0x31B860: "find_unit", 0x30B9B0: "gate1", 0x377C20: "field15",
    0x3283D0: "rx",        0x28F1F0: "nb",    0x316D70: "find_tbuf",
    0x30B8E0: "gate3",     0x30E360: "st",    0x469BB0: "kh",
    0x32A150: "clk",       0x306F00: "gd",    0x3299B0: "ev",
    0x30AB40: "relat",     0x30B770: "fbuild", 0x30B7F0: "cgate",
    0x17D470: "ctxrd",     0x1D50D0: "sing",   0x2FA3B0: "prox",
    0x3272A0: "viewer",    0x265020: "poscp",  0x3A1920: "dist",
    0x3BBD00: "rxpost",    0x296280: "vscan",  0x2962C0: "vdef",
    0x3F8980: "vpublish",  0x2FA390: "kkind",  0x2F8E90: "kkind_t",
    0x46AB10: "kring",     0x469570: "klookup", 0x20E600: "codec",
    0x263D30: "memidx",    0x2360D0: "mmap",   0x307140: "caprow",
    0x2E1C20: "capset",    0x2E1CA0: "capclr", 0x359200: "supw",
    0x359330: "supb",      0x26BD20: "cdw",    0x238B70: "bset",
    0x238AE0: "bclr",      0x2E7C10: "centry", 0x2EB030: "evwr",
    0x2EB0D0: "evpost",    0x808C40: "cookie", 0x3589B0: "wid",
    0x3588B0: "idres",     0x506700: "qfill",  0x28FBE0: "qinit",
    0x3590D0: "actorid",   0x263FF0: "clsget", 0x263E30: "lnk",
    0x236850: "ucount",    0x236820: "uslot",  0x3EFD00: "digits",
    0x24A5A0: "strfind",   0x2DD7E0: "catdw",  0x2DD7B0: "catb",
    0x3848E0: "st_init",   0x386A50: "st_add", 0x386A70: "st_rm",
    0x3876D0: "st_beat",   0x387730: "st_dur", 0x16D6A0: "st_extra",
    0x861EC0: "memset_t",  0x861F14: "sqrtf_t",
}

# stubbed boundaries: patched to ret, args+order logged, return via rets
STUBS = {
    0x5369C0: "kill_presenter",
    0x3112F0: "applier",
    0x300FC0: "defeat_cleanup",
    0x312280: "rewards",
    0x301140: "recover",
    0x300140: "case4_action",
    0x307D10: "case4_second",
    0x3284D0: "reaction",
    0x30FED0: "recompute",
    0x46A800: "extra_add",
}

COOKIE = 0x0000DEADBEEF

# canonical image VAs the fixture writes (all resolved programmatically from
# rip-relative operands in the shipped bodies)
G_UCOUNT   = 0x208E6A0    # unit count (dword)
G_UTBL     = 0x208E688    # unit table base (qword)
G_FIELDIDX = 0x21654C4    # active field idx: 0x2EF640()->0x2164280 +0x200 +0x1044
G_FLDTBL   = 0x2ADD100    # field table ptr
G_BSTATE   = 0x2089340    # battle state dword
G_FLG2158  = 0x22C2158    # flag byte (flag_builder bit1)
G_MODE2161 = 0x22C2160    # mode dword (context_gate byte+4&0x20 skip on 5/6)
G_CTX      = 0x1F81428    # singleton slot (0x1D50D0)
G_TICK     = 0x208D45C    # raw tick
G_SCALE    = 0x1DFE0B8    # float scale (ships 1.0f)
G_BEAT     = 0x1DFE0B4    # beat/dedupe scale dword (x0x1C2 window)
G_QUEUE    = 0x2B457D0    # reaction queue ptr
G_QCUR     = 0x2B443C0    # queue cursor byte
G_KREG     = 0x2EBF018    # kill-kind registry ptr
G_KCUR     = 0x2EBB54C    # kill-ring cursor
KRING      = 0x2EBB560    # kill-ring base (10 x 0x20, to 0x2EBB6A0)
G_CODEC    = 0x1F83530    # codec base for 0x20E600
G_ACTOR    = 0x22C7FE0    # actor id for 0x3590D0/0x3272A0/0x359200/0x359330
G_SREG     = 0x2EBF118    # status registry slot
G_DEEP     = 0x209BE80    # 0x28FBE0 deep gate obj ptr
G_STRTAB0  = 0x1E0C1E8    # 0x506700 kind-0 arm string-table obj
G_STRTAB1  = 0x1E0C1F0    # kind-1 arm string-table obj
VIEWB      = 0x209BF40    # view objects, stride 0xC0 (scanner marks at +0x7E)
VIEWDEF    = 0x209C240    # default view
VPOST      = 0x1EEBB00    # static viewer pos (3 floats)
GTAB       = 0x2EC13C0    # group bitmask rows (stride 24: +0 exp,+8 dead,+0x10 latch)
CAPT       = 0x215F1C0    # capability table (16 rows dword)
SUPW       = 0x22C8000    # suppression word
SUPB       = 0x22C8004    # suppression byte array
CDW        = 0x209A2C4    # completion dword array
G_COOKIE   = 0x1F44830
IAT_MEMSET = 0x8C2A60
IAT_SQRTF  = 0x8C2BB8
IAT_RAND   = 0x8C3098

def qw(v): return struct.pack("<Q", v & 0xFFFFFFFFFFFFFFFF)
def dw(v): return struct.pack("<I", v & 0xFFFFFFFF)
def hw(v): return struct.pack("<H", v & 0xFFFF)
def db(v): return struct.pack("<B", v & 0xFF)
def fl(v): return struct.pack("<f", v)

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

# fixture routines in CODE:
#   +0x00 memset: rcx=dst, dl=fill, r8=len -> rax=dst
#   +0x10 sqrtf:  sqrtss xmm0,xmm0; ret
#   +0x20 rand:   xor eax,eax; ret   (deterministic 0)
#   +0x40 view callback: writes {rcx,rdx,r8} into CBLOG then xor eax;ret
MEMSET_FN = bytes.fromhex("4889c8574889cf88d04c89c1f3aa5fc3")
SQRTF_FN  = bytes.fromhex("f30f51c0c3")
RAND_FN   = bytes.fromhex("31c0c3")
CBLOG     = CODE + 0x800
# callback: mov [CBLOG],rcx; mov [CBLOG+8],rdx; mov [CBLOG+0x10],r8; xor eax,eax; ret
CB_FN     = bytes.fromhex("48890d" + "00000000" ) # placeholder - built below
def _cb_fn():
    # lea rax,[rip+7]; jmp over data? simpler: absolute mov via movabs
    # 48 c7 c0 <CBLOG lo32> 90 90 90 -> mov rax,imm64 is 48 b8 +8B
    b = bytearray()
    b += b"\x48\xb8" + qw(CBLOG)          # movabs rax, CBLOG
    b += b"\x48\x89\x08"                  # mov [rax],rcx
    b += b"\x48\x89\x50\x08"              # mov [rax+8],rdx
    b += b"\x4c\x89\x40\x10"              # mov [rax+0x10],r8
    b += b"\x31\xc0"                      # xor eax,eax
    b += b"\xc3"
    return bytes(b)
CB_FN = _cb_fn()

class World:
    def __init__(self, case, raw, secs):
        self.case = case
        self.uc = Uc(UC_ARCH_X86, UC_MODE_64)
        self.gm = GuestMem(self.uc)
        img = bytearray(IMG_HI - IMG_LO)
        for va, vs, ra, rs in secs:
            n = min(vs, rs)
            img[va:va + n] = raw[ra:ra + n]
        self.gm.map(IMG_LO, len(img), bytes(img))
        for a, s in [(HEAP, 0x1100000), (STACK, 0x100000), (RETQ, 0x1000)]:
            self.gm.map(a, s)
        gm = self.gm
        gm.w(RETQ, b"\xc3")

        # fixture routines + IAT
        gm.w(CODE, MEMSET_FN)
        gm.w(CODE + 0x10, SQRTF_FN)
        gm.w(CODE + 0x20, RAND_FN)
        gm.w(CODE + 0x40, CB_FN)
        gm.w(IAT_MEMSET, qw(CODE))
        gm.w(IAT_SQRTF, qw(CODE + 0x10))
        gm.w(IAT_RAND,  qw(CODE + 0x20))

        # ---- globals
        gm.w(G_COOKIE, qw(COOKIE))
        gm.w(G_UTBL, qw(UNITB))
        gm.w(G_UCOUNT, dw(case.get("ucount", 2)))
        gm.w(G_FIELDIDX, dw(case.get("field_idx", 0)))
        gm.w(G_FLDTBL, qw(case.get("fldtbl", FLDT)))
        gm.w(G_BSTATE, dw(case.get("bstate", 0)))
        gm.w(G_FLG2158, db(case.get("b2158", 0)))
        gm.w(G_MODE2161, dw(case.get("mode2161", 0)))
        gm.w(G_CTX, qw(CTX))
        gm.w(G_TICK, dw(case.get("tick", 0x300)))
        gm.w(G_SCALE, fl(case.get("scale", 1.0)))
        gm.w(G_BEAT, dw(case.get("beat", 4)))
        gm.w(G_QUEUE, qw(case.get("queue", QUEUE)))
        gm.w(G_QCUR, db(case.get("qcur", 0)))
        # 0x506700's kind arms pass a string-table object to 0x24A5A0; a planted
        # NUL string keeps the scan real and bounded (no match -> +0x30 = 0)
        gm.w(G_STRTAB0, qw(MISC + 0x100))
        gm.w(G_STRTAB1, qw(MISC + 0x100))
        gm.w(MISC + 0x100, b"\0")
        gm.w(G_KREG, qw(KREG))
        gm.w(G_KCUR, dw(case.get("kcur", 0)))
        gm.w(G_CODEC, qw(0))            # rva fields are absolute VAs
        gm.w(G_ACTOR, dw(case.get("actor", 0)))
        gm.w(G_SREG, qw(case.get("sreg", HDR)))
        gm.w(G_DEEP, qw(MISC))
        gm.w(CTX + 0xC20, dw(case.get("ctx_mode", 0)))

        # ---- field table {+4 count, rows +8 stride3: word flags}
        gm.w(FLDT + 4, dw(case.get("fld_count", 1)))
        for i, flags in enumerate(case.get("fld_rows", [0])):
            gm.w(FLDT + 8 + i * 3 + 0, db(flags & 0xFF))
            gm.w(FLDT + 8 + i * 3 + 1, db((flags >> 8) & 0xFF))

        # ---- kill-kind registry {+8 stride word, +0xC rva} -> KROW elems
        gm.w(KREG + 8, hw(case.get("kreg_stride", 0x10)))
        gm.w(KREG + 0xC, dw(KROW))
        for i, (b3, b4) in enumerate(case.get("krows", [(0, 0)] * 0x20)):
            gm.w(KROW + i * case.get("kreg_stride", 0x10) + 3, db(b3))
            gm.w(KROW + i * case.get("kreg_stride", 0x10) + 4, db(b4))

        # ---- kill ring
        for i, e in enumerate(case.get("kring", [])):
            gm.w(KRING + i * 0x20 + 0, hw(e.get("kind", 0)))
            gm.w(KRING + i * 0x20 + 4, dw(e.get("tick", 0)))
            gm.w(KRING + i * 0x20 + 8, qw(e.get("src", 0)))

        # ---- status registry (EXP-086 layout: +8 stride word, +0xC table va)
        gm.w(TBL, open(STATUS_BIN, "rb").read()[0x20:])
        if case.get("sreg", HDR):
            gm.w(HDR + 8, hw(0x28))
            gm.w(HDR + 0xC, dw(TBL))

        # ---- group bitmask rows (0x2BC13C0 + (grp-1)*24: +0 exp, +8 dead, +0x10 latch)
        for grp, row in case.get("groups", {}).items():
            base = GTAB + (grp - 1) * 24
            gm.w(base + 0, qw(row.get("expect", 0)))
            gm.w(base + 8, qw(row.get("dead", 0)))
            gm.w(base + 0x10, db(row.get("latch", 0)))

        # ---- capability table / suppression / completion dword
        for row, v in case.get("captab", {}).items():
            gm.w(CAPT + row * 4, dw(v))
        gm.w(SUPW, dw(case.get("supw", 0)))
        for i in range(4):
            gm.w(SUPB + i, db(case.get("supb", [0] * 4)[i]))
        gm.w(CDW, b"\0" * 0x20)

        # ---- views (4 x 0xC0 at VIEWB; scanner marks at +0x26/+0x7E, handle +0xB0)
        for i, v in enumerate(case.get("views", [])):
            base = VIEWB + i * 0xC0
            gm.w(base + 0x26, hw(v.get("f26", 0)))
            gm.w(base + 0x7E, db(v.get("f7e", 0)))
            gm.w(base + 0xB0, dw(v.get("handle", 0)))
            gm.w(base + 0x38, qw(v.get("fnptr", 0)))
        gm.w(VIEWDEF + 0xB0, dw(case.get("vdef_handle", 0)))

        # ---- static viewer pos
        for i, f in enumerate(case.get("vpost", [0.0, 0.0, 0.0])):
            gm.w(VPOST + i * 4, fl(f))

        # ---- queue (zeroed by default)
        gm.w(QUEUE, b"\0" * (64 * 0x50))

        # ---- records
        def stats_rec(base, spec):
            gm.w(base, b"\0" * 0x200)
            gm.w(base + 0x24, dw(spec.get("cap", 200)))
            gm.w(base + 0x2C, db(spec.get("vit", 50)))
            gm.w(base + 0x38, dw(spec.get("m38", 0)))
            gm.w(base + 0x3C, dw(spec.get("m3C", 0)))
            gm.w(base + 0x48, dw(spec.get("hp", 100) & 0xFFFFFFFF))
            gm.w(base + 0x64, dw(spec.get("m64", 0)))
            gm.w(base + 4, db(spec.get("atype", 0)))
            gm.w(base + 5, db(spec.get("kind", 0)))
        stats_rec(RECB,          case.get("tgt", {}))
        stats_rec(RECB + 0x200,  case.get("src", {"hp": 100, "cap": 200}))

        # ---- work objects
        def work(base, spec):
            gm.w(base, b"\0" * 0x200)
            gm.w(base + 0x3, db(spec.get("cls", 0x20)))     # >>5 -> 1
            gm.w(base + 0xE, db(spec.get("nib", 0)))
            gm.w(base + 0x15, db(spec.get("b15", 0)))
            gm.w(base + 0x16, hw(spec.get("w16", 0)))
            gm.w(base + 0x18, db(spec.get("evgate", 0)))
            gm.w(base + 0xB8, qw(spec.get("pos", POSB)))
            gm.w(base + 0xC0, qw(spec.get("eobj", 0)))
            gm.w(base + 0xF6, hw(spec.get("member", 0)))
        work(WORKB,          case.get("twork", {}))
        work(WORKB + 0x200,  case.get("swork", {}))
        # position + event-obj blocks
        for i, p in enumerate(case.get("pos", [[0.0, 0.0, 0.0]] * 4)):
            for j, f in enumerate(p):
                gm.w(POSB + i * 0x10 + j * 4, fl(f))
        for i, v in enumerate(case.get("eobj", [-1] * 4)):
            gm.w(EOBJB + i * 0x10, dw(v & 0xFFFFFFFF))

        # ---- units
        def unit(idx, spec):
            base = UNITB + idx * 0xF50
            gm.w(base, b"\0" * 0xF50)
            gm.w(base + 0x0, dw(spec.get("flags", 0x10)))   # relat needs bit4
            gm.w(base + 0x4, db(spec.get("uflag4", 0)))
            gm.w(base + 0x8, dw(spec.get("uid", 7 + idx)))
            gm.w(base + 0x10, qw(spec.get("work", WORKB + idx * 0x200)))
            gm.w(base + 0x40, qw(spec.get("mmap", MMAPB + idx * 0x40)))
            rec = spec.get("rec", RECB + idx * 0x200)
            gm.w(base + 0x698, qw(rec))
            gm.w(base + 0x6A0, qw(spec.get("spawn", SPAWNB + idx * 0x40)))
            gm.w(base + 0x48, dw(spec.get("floor", 0) & 0xFFFFFFFF))
            gm.w(base + 0xE98, db(spec.get("group", 0)))
            gm.w(base + 0xE99, db(spec.get("gflag", 0)))
            # target buffer at +0x778: count +4, entries +0x780 stride 0x10
            tb = spec.get("tbuf", None)
            gm.w(base + 0x77C, dw(tb["count"] if tb else 0))
            if tb:
                for i, (key, fl8) in enumerate(tb["entries"]):
                    gm.w(base + 0x780 + i * 0x10 + 0, qw(key))
                    gm.w(base + 0x780 + i * 0x10 + 8, dw(fl8))
            # member-map {count byte, slots}
            mm = spec.get("mmaptab", None)
            mp = spec.get("mmap", MMAPB + idx * 0x40)
            if mm is not None:
                gm.w(mp, db(mm[0]))
                for i, b in enumerate(mm[1:]):
                    gm.w(mp + 1 + i, db(b))
            return base
        self.tunit = unit(0, case.get("tunit", {}))
        self.sunit = unit(1, case.get("sunit", {"uid": 9}))

        # ---- spawns
        for i, sp in enumerate(case.get("spawns", [{}] * 4)):
            gm.w(SPAWNB + i * 0x40 + 8, dw(sp.get("counter", 0)))
            gm.w(SPAWNB + i * 0x40 + 0xC, dw(sp.get("time", 0)))

        # ---- mutants
        for va, data in case.get("patch", []):
            gm.w(va, data)

        # ---- stubs patched to ret
        for va in STUBS:
            gm.w(va, b"\xc3")

        self.trace, self.faults = [], []
        rets = case.get("rets", {})
        uc = self.uc
        uc.hook_add(UC_HOOK_MEM_UNMAPPED, self.on_bad)
        for va in CALLS:
            uc.hook_add(UC_HOOK_CODE, self.on_call, begin=va, end=va)
        for va in STUBS:
            uc.hook_add(UC_HOOK_CODE, self.on_stub, begin=va, end=va)
        self.rets = rets

    def on_call(self, uc, addr, size, _):
        rcx = uc.reg_read(UC_X86_REG_RCX) & 0xFFFFFFFFFFFFFFFF
        rdx = uc.reg_read(UC_X86_REG_RDX) & 0xFFFFFFFFFFFFFFFF
        r8  = uc.reg_read(UC_X86_REG_R8)  & 0xFFFFFFFF
        r9  = uc.reg_read(UC_X86_REG_R9)  & 0xFFFFFFFF
        self.trace.append((CALLS[addr], "rcx=%x" % rcx, "edx=%x" % rdx,
                           "r8d=%x" % r8, "r9d=%x" % r9))

    def on_stub(self, uc, addr, size, _):
        rcx = uc.reg_read(UC_X86_REG_RCX) & 0xFFFFFFFFFFFFFFFF
        rdx = uc.reg_read(UC_X86_REG_RDX) & 0xFFFFFFFFFFFFFFFF
        self.trace.append(("STUB", STUBS[addr], "rcx=%x" % rcx,
                           "rdx=%x" % rdx))
        uc.reg_write(UC_X86_REG_RAX, self.rets.get(addr, 0))

    def on_bad(self, uc, access, addr, size, value, _):
        self.faults.append(("MEM", hex(addr), "access=%d" % access,
                            "rip=%x" % uc.reg_read(UC_X86_REG_RIP)))
        return False

def build(case, raw, secs):
    return World(case, raw, secs)

def invoke(w, va, rcx=0, rdx=0, r8=0, r9=0):
    uc, gm = w.uc, w.gm
    sp = STACK + 0x80000
    gm.w(sp, qw(RETQ))
    gm.w(sp + 0x28, b"\xCD" * 0x30)   # 0xCD fill: catches phantom stack args
    uc.reg_write(UC_X86_REG_RSP, sp)
    uc.reg_write(UC_X86_REG_RCX, rcx & 0xFFFFFFFFFFFFFFFF)
    uc.reg_write(UC_X86_REG_RDX, rdx & 0xFFFFFFFFFFFFFFFF)
    uc.reg_write(UC_X86_REG_R8, r8 & 0xFFFFFFFFFFFFFFFF)
    uc.reg_write(UC_X86_REG_R9, r9 & 0xFFFFFFFFFFFFFFFF)
    try:
        uc.emu_start(va, RETQ, count=16_000_000)
    except Exception as e:
        w.faults.append(("EMU", str(e), uc.reg_read(UC_X86_REG_RIP)))
    return uc.reg_read(UC_X86_REG_RAX)

def expect(name, snap, cond, why):
    ok = bool(cond)
    print(("PASS " if ok else "FAIL ") + name + ("  -- " + why if not ok else ""))
    return ok

def rd8(a, gm):  return gm.r(a, 1)[0]
def rd16(a, gm): return struct.unpack("<H", gm.r(a, 2))[0]
def rd32(a, gm): return struct.unpack("<I", gm.r(a, 4))[0]
def rd64(a, gm): return struct.unpack("<Q", gm.r(a, 8))[0]

# ---- case list ---------------------------------------------------------------

def build_cases():
    C = []
    A = C.append
    def trhas(s, *names):
        return all(any(x[0] == n for x in s["trace"]) for n in names)
    def stubhas(s, name):
        return any(x[0] == "STUB" and x[1] == name for x in s["trace"])
    def trabsent(s, *names):
        return not any(x[0] in names or (x[0] == "STUB" and x[1] in names)
                       for x in s["trace"])
    def trcnt(s, name):
        return sum(1 for x in s["trace"] if x[0] == name or
                   (x[0] == "STUB" and x[1] == name))
    def trorder(s, *names):
        seq = [x[0] if x[0] != "STUB" else x[1] for x in s["trace"]]
        pos = []
        for n in names:
            try:
                pos.append(seq.index(n))
            except ValueError:
                return False
        return pos == sorted(pos)

    def evids(s):
        return [int(x[2][4:], 16) for x in s["trace"] if x[0] == "ev"]

    # ======== ABI / delta basics ============================================
    # EV(0x2005) fires on ordinary damage too - the "alive" event is not
    # restricted to heals; the lethal path only changes which variant runs.
    A({"name": "dmg-basic", "rcx": RECB, "edx": -30, "r8": RECB + 0x200,
       "check": lambda s: s["hp"] == 70 and
                          trhas(s, "find_unit", "gate1", "rx", "nb",
                                "find_tbuf", "gate3") and
                          evids(s) == [0x2005] and
                          s["queue0_work"] == WORKB and
                          s["queue0_dv"] == 0x80808080 and
                          trabsent(s, "st", "kh", "gd")})
    A({"name": "heal-basic", "rcx": RECB, "edx": 30, "r8": RECB + 0x200,
       "check": lambda s: s["hp"] == 130 and
                          trhas(s, "gate1", "rx", "nb") and
                          trabsent(s, "gate3", "st", "kh", "ev")})
    # publishers run BEFORE the store; gate3 suppresses only the store
    A({"name": "order-pub-then-store", "rcx": RECB, "edx": -30,
       "r8": RECB + 0x200,
       "check": lambda s: s["hp"] == 70 and
                          trorder(s, "rx", "nb", "gate3")})
    # null source: variant 0, no killer, ev r8d=0
    A({"name": "nullsrc-dmg", "rcx": RECB, "edx": -30, "r8": 0,
       "check": lambda s: s["hp"] == 70 and trabsent(s, "find_tbuf") and
                          s["u0_killer"] == 0})
    A({"name": "nullsrc-kill", "rcx": RECB, "edx": -150, "r8": 0,
       "tgt": {"hp": 100},
       "check": lambda s: s["hp"] == 0 and s["u0_killer"] == 0 and
                          any(x[0] == "ev" and "r8d=0" in x[3]
                              for x in s["trace"])})
    # no target unit: publishers skipped, no killer, store+KO still happen
    A({"name": "no-tunit-dmg", "rcx": RECB, "edx": -30, "r8": RECB + 0x200,
       "tunit": {"rec": 0},   # no unit points at RECB
       "check": lambda s: s["hp"] == 70 and
                          trabsent(s, "rx", "nb", "ev")})
    A({"name": "no-tunit-kill", "rcx": RECB, "edx": -150, "r8": RECB + 0x200,
       "tunit": {"rec": 0},
       "check": lambda s: s["hp"] == 0 and s["ko64"] & 1 and
                          trabsent(s, "ev", "gd")})
    # no source unit: FI skipped
    A({"name": "no-sunit", "rcx": RECB, "edx": -30, "r8": RECB + 0x200,
       "sunit": {"rec": 0},
       "check": lambda s: s["hp"] == 70 and trabsent(s, "find_tbuf")})

    # ======== delta zero =====================================================
    # delta==0 takes the damage path (jle): field15 gate, publishers, gate3,
    # and the alive event all still run on a living target.
    A({"name": "d0-live", "rcx": RECB, "edx": 0, "r8": RECB + 0x200,
       "tgt": {"hp": 50},
       "check": lambda s: s["hp"] == 50 and s["ko64"] == 0 and
                          trabsent(s, "st") and evids(s) == [0x2005]})
    A({"name": "d0-live-b5", "rcx": RECB, "edx": 0, "r8": RECB + 0x200,
       "tgt": {"hp": 50}, "r9": 0x20,
       "check": lambda s: s["hp"] == 50 and trabsent(s, "st")})
    # delta 0 on a floor unit reruns the WHOLE lethal cascade (kh+st+gd+ev);
    # flag bit5 does not divert it into the heal arm.
    A({"name": "d0-dead", "rcx": RECB, "edx": 0, "r8": RECB + 0x200,
       "tgt": {"hp": 0},
       "check": lambda s: s["hp"] == 0 and stubhas(s, "defeat_cleanup")})
    A({"name": "d0-dead-b5", "rcx": RECB, "edx": 0, "r8": RECB + 0x200,
       "tgt": {"hp": 0}, "r9": 0x20,
       "check": lambda s: s["hp"] == 0 and s["ko64"] & 1 and
                          trhas(s, "st", "kh") and
                          stubhas(s, "defeat_cleanup")})

    # ======== floor ==========================================================
    A({"name": "floor-exact", "rcx": RECB, "edx": -80, "r8": RECB + 0x200,
       "tgt": {"hp": 100}, "tunit": {"floor": 20},
       "check": lambda s: s["hp"] == 20 and s["ko64"] & 1})
    A({"name": "floor-above", "rcx": RECB, "edx": -79, "r8": RECB + 0x200,
       "tgt": {"hp": 100}, "tunit": {"floor": 20},
       "check": lambda s: s["hp"] == 21 and not s["ko64"] & 1})
    A({"name": "floor-under", "rcx": RECB, "edx": -1000, "r8": RECB + 0x200,
       "tgt": {"hp": 100}, "tunit": {"floor": 20},
       "check": lambda s: s["hp"] == 20 and s["ko64"] & 1})

    # ======== cap ============================================================
    A({"name": "cap-clamp", "rcx": RECB, "edx": 100, "r8": RECB + 0x200,
       "tgt": {"hp": 150, "cap": 200},
       "check": lambda s: s["hp"] == 200})
    A({"name": "cap-under", "rcx": RECB, "edx": 49, "r8": RECB + 0x200,
       "tgt": {"hp": 150, "cap": 200},
       "check": lambda s: s["hp"] == 199})
    # doubling bit (0x64|0x3C bit28)
    A({"name": "cap-double", "rcx": RECB, "edx": 100, "r8": RECB + 0x200,
       "tgt": {"hp": 150, "cap": 200, "m64": 0x10000000},
       "check": lambda s: s["hp"] == 250})
    A({"name": "cap-double-3C", "rcx": RECB, "edx": 100, "r8": RECB + 0x200,
       "tgt": {"hp": 150, "cap": 200, "m3C": 0x10000000},
       "check": lambda s: s["hp"] == 250})
    # freeze bit (bit16): cap is max(old,1)
    A({"name": "freeze-cap", "rcx": RECB, "edx": 100, "r8": RECB + 0x200,
       "tgt": {"hp": 150, "cap": 200, "m64": 0x10000},
       "check": lambda s: s["hp"] == 150})
    A({"name": "freeze-cap-zero", "rcx": RECB, "edx": 50, "r8": RECB + 0x200,
       "tgt": {"hp": 0, "cap": 200, "m64": 0x10000},
       "tunit": {"floor": -5},
       "check": lambda s: s["hp"] == 1})
    A({"name": "freeze-dmg", "rcx": RECB, "edx": -100, "r8": RECB + 0x200,
       "tgt": {"hp": 150, "cap": 200, "m64": 0x10000},
       "check": lambda s: s["hp"] == 50})

    # ======== status refusal (downed) ========================================
    for st in (1, 2, 0x80000000, 3):
        A({"name": "downed-neg-%x" % st, "rcx": RECB, "edx": -5,
           "r8": RECB + 0x200, "tgt": {"hp": 10, "m64": st},
           "check": lambda s: s["hp"] == 10 and trhas(s, "field15")})
        A({"name": "downed-neg-ovr-%x" % st, "rcx": RECB, "edx": -5,
           "r8": RECB + 0x200, "tgt": {"hp": 10, "m64": st},
           "fld_rows": [0x8000],
           "check": lambda s: s["hp"] == 5 and trhas(s, "field15")})
    # positive delta bypasses the refusal entirely (field15 never asked)
    A({"name": "downed-pos", "rcx": RECB, "edx": 5, "r8": RECB + 0x200,
       "tgt": {"hp": 0, "m64": 1},
       "check": lambda s: s["hp"] == 5 and s["ko64"] == 0 and
                          trabsent(s, "field15")})
    # zero delta: the refusal gate at 0030062E is SKIPPED by jns
    # (delta>=0) — the field15 token here fires at a later call site of
    # the same callee inside lethal re-processing.
    A({"name": "downed-zero", "rcx": RECB, "edx": 0, "r8": RECB + 0x200,
       "tgt": {"hp": 0, "m64": 1},
       "check": lambda s: trhas(s, "field15") and evids(s) == [0x2008]})
    A({"name": "downed-zero-b5", "rcx": RECB, "edx": 0, "r8": RECB + 0x200,
       "tgt": {"hp": 0, "m64": 1}, "r9": 0x20,
       "check": lambda s: trhas(s, "field15") and evids(s) == [0x2008]})

    # ======== gates ===========================================================
    # gate1 refusal: unit flag bit8 on the target drives ctxgate lo bit0
    A({"name": "g1-bit8", "rcx": RECB, "edx": -30, "r8": RECB + 0x200,
       "tunit": {"flags": 0x110},
       "check": lambda s: s["hp"] == 100 and trhas(s, "gate1") and
                          trabsent(s, "gate3", "rx", "nb")})
    # bit0 skips gate1 entirely
    A({"name": "g1-skip", "rcx": RECB, "edx": -30, "r8": RECB + 0x200,
       "tunit": {"flags": 0x110}, "r9": 1,
       "check": lambda s: s["hp"] == 70 and trabsent(s, "gate1")})
    # flag_builder refuse: bstate & 0x3080
    A({"name": "g1-bstate", "rcx": RECB, "edx": -30, "r8": RECB + 0x200,
       "bstate": 0x80,
       "check": lambda s: s["hp"] == 100 and trabsent(s, "gate3", "rx")})
    # gate3 suppresses only the store; publishers still ran
    A({"name": "g3-ctxmode1", "rcx": RECB, "edx": -30, "r8": RECB + 0x200,
       "ctx_mode": 1,
       "check": lambda s: s["hp"] == 100 and
                          trhas(s, "rx", "nb", "gate3") and
                          trabsent(s, "st")})
    # gate3 not asked for positive delta
    A({"name": "g3-heal-skip", "rcx": RECB, "edx": 30, "r8": RECB + 0x200,
       "ctx_mode": 2,
       "check": lambda s: s["hp"] == 130 and trabsent(s, "gate3")})
    # gate3 asked on the kill: refusal skips the store AND the whole lethal
    # block, then falls through to the alive-event tail (0x2005 still posts)
    A({"name": "g3-kill-suppress", "rcx": RECB, "edx": -150,
       "r8": RECB + 0x200, "tgt": {"hp": 100}, "ctx_mode": 1,
       "check": lambda s: s["hp"] == 100 and trabsent(s, "st", "kh") and
                          evids(s) == [0x2005]})

    # ======== revive ==========================================================
    A({"name": "revive", "rcx": RECB, "edx": 10, "r8": RECB + 0x200,
       "tgt": {"hp": 0, "m64": 1},
       "check": lambda s: s["hp"] == 10 and s["ko64"] == 0 and
                          trhas(s, "st") and stubhas(s, "recover")})
    A({"name": "revive-smallest", "rcx": RECB, "edx": 1, "r8": RECB + 0x200,
       "tgt": {"hp": 0, "m64": 1},
       "check": lambda s: s["hp"] == 1 and s["ko64"] == 0})
    # old hp 1 is NOT <= 0: no revive processing
    A({"name": "heal-at-1", "rcx": RECB, "edx": 10, "r8": RECB + 0x200,
       "tgt": {"hp": 1, "m64": 1},
       "check": lambda s: s["hp"] == 11 and s["ko64"] == 1 and
                          trabsent(s, "st")})

    # ======== event variants (FI-driven r13) ==================================
    # src tbuf entry {key=[tgtunit+0x10], flags<<8}; r13 = flags bit8 of entry+8
    def tbuf_for(wk, flag):
        return {"count": 3,
                "entries": [(0x100, 0), (wk, flag), (0x155, 0)]}
    tw = WORKB  # tgt unit's work ptr
    A({"name": "ev-alive-v0", "rcx": RECB, "edx": -30, "r8": RECB + 0x200,
       "sunit": {"uid": 9, "tbuf": tbuf_for(tw, 0)},
       "check": lambda s: s["hp"] == 70 and
                          any(x[0] == "ev" and "edx=2005" in x[2]
                              for x in s["trace"])})
    A({"name": "ev-alive-v1", "rcx": RECB, "edx": -30, "r8": RECB + 0x200,
       "sunit": {"uid": 9, "tbuf": tbuf_for(tw, 0x100)},
       "check": lambda s: any(x[0] == "ev" and "edx=2006" in x[2]
                              for x in s["trace"])})
    A({"name": "ev-dead-v0", "rcx": RECB, "edx": -150, "r8": RECB + 0x200,
       "tgt": {"hp": 100}, "sunit": {"uid": 9, "tbuf": tbuf_for(tw, 0)},
       "check": lambda s: s["hp"] == 0 and
                          any(x[0] == "ev" and "edx=2008" in x[2]
                              for x in s["trace"])})
    A({"name": "ev-dead-v1", "rcx": RECB, "edx": -150, "r8": RECB + 0x200,
       "tgt": {"hp": 100}, "sunit": {"uid": 9, "tbuf": tbuf_for(tw, 0x100)},
       "check": lambda s: s["hp"] == 0 and
                          any(x[0] == "ev" and "edx=2007" in x[2]
                              for x in s["trace"])})
    # FI miss -> r13=0 -> default variants
    A({"name": "ev-dead-miss", "rcx": RECB, "edx": -150, "r8": RECB + 0x200,
       "tgt": {"hp": 100},
       "sunit": {"uid": 9, "tbuf": {"count": 1, "entries": [(0x100, 0x100)]}},
       "check": lambda s: s["hp"] == 0 and
                          any(x[0] == "ev" and "edx=2008" in x[2]
                              for x in s["trace"])})
    # alt death event on flag bit8 (ignores variant)
    A({"name": "ev-dead-alt", "rcx": RECB, "edx": -150, "r8": RECB + 0x200,
       "tgt": {"hp": 100}, "r9": 0x100,
       "sunit": {"uid": 9, "tbuf": tbuf_for(tw, 0x100)},
       "check": lambda s: s["hp"] == 0 and
                          any(x[0] == "ev" and "edx=200e" in x[2]
                              for x in s["trace"])})

    # ======== suppression bits ================================================
    # bit2 suppresses BOTH events; bit6 suppresses alive only
    A({"name": "sup-b2-kill", "rcx": RECB, "edx": -150, "r8": RECB + 0x200,
       "tgt": {"hp": 100}, "r9": 4,
       "check": lambda s: s["hp"] == 0 and trabsent(s, "ev")})
    A({"name": "sup-b2-alive", "rcx": RECB, "edx": -30, "r8": RECB + 0x200,
       "r9": 4,
       "check": lambda s: s["hp"] == 70 and trabsent(s, "ev")})
    A({"name": "sup-b6-alive", "rcx": RECB, "edx": -30, "r8": RECB + 0x200,
       "r9": 0x40,
       "check": lambda s: s["hp"] == 70 and trabsent(s, "ev")})
    A({"name": "sup-b6-kill", "rcx": RECB, "edx": -150, "r8": RECB + 0x200,
       "tgt": {"hp": 100}, "r9": 0x40,
       "check": lambda s: s["hp"] == 0 and trhas(s, "ev")})
    # bit4 suppresses rx only
    A({"name": "sup-b4", "rcx": RECB, "edx": -30, "r8": RECB + 0x200, "r9": 0x10,
       "check": lambda s: s["hp"] == 70 and trabsent(s, "rx") and
                          trhas(s, "nb")})
    # bit7 suppresses nb only
    A({"name": "sup-b7", "rcx": RECB, "edx": -30, "r8": RECB + 0x200, "r9": 0x80,
       "check": lambda s: s["hp"] == 70 and trhas(s, "rx") and
                          trabsent(s, "nb")})
    # nb reaching 0x3F8980: a view listening on handle 7 (tgt uid) gets its
    # +0x26 bit0 cleared when no fnptr is planted
    A({"name": "nb-publish", "rcx": RECB, "edx": -30, "r8": RECB + 0x200,
       "views": [{"f26": 3, "handle": 7}],
       "check": lambda s: s["hp"] == 70 and trhas(s, "nb", "vpublish") and
                          s["view0_f26"] == 2})
    # nb with a planted view callback: 0x3F8980 calls view+0x38 with
    # (view, &{old,new}, 1) - the fixture callback records its args
    A({"name": "nb-callback", "rcx": RECB, "edx": -30, "r8": RECB + 0x200,
       "views": [{"f26": 3, "handle": 7, "fnptr": CODE + 0x40}],
       "check": lambda s: trhas(s, "vpublish") and
                          s["cblog0"] == VIEWB and s["cblog1"] == 1})
    # bit1 suppresses kh
    A({"name": "sup-b1", "rcx": RECB, "edx": -150, "r8": RECB + 0x200,
       "tgt": {"hp": 100}, "r9": 2,
       "check": lambda s: s["hp"] == 0 and trabsent(s, "kh") and
                          trhas(s, "st", "ev")})

    # ======== kill sequence ===================================================
    # atype in the 0x1B..0x27 monster band: ST's KO cascade does NOT run - a
    # single st(status=0, mode=-1) call, no +0x64 write (KO is handled by the
    # despawn/cleanup path, not the status mask). Kill bookkeeping still runs.
    A({"name": "kill-party", "rcx": RECB, "edx": -150, "r8": RECB + 0x200,
       "tgt": {"hp": 100, "atype": 0x1B, "kind": 0},
       "sunit": {"uid": 9},
       "check": lambda s: s["hp"] == 0 and s["u0_killer"] == 9 and
                          trhas(s, "kh", "kring", "clk", "gd", "ev") and
                          stubhas(s, "kill_presenter") and
                          s["kring0_kind"] == 0x10 and
                          s["kring0_src"] == RECB + 0x200 and
                          s["kcur"] == 1 and
                          any(x[0] == "st" and x[4] == "r9d=ffffffff"
                              for x in s["trace"])})
    # spawn-backed kill: counter++, time = tick/(scale*30)
    A({"name": "kill-spawn", "rcx": RECB, "edx": -150, "r8": RECB + 0x200,
       "tgt": {"hp": 100, "kind": 1}, "tick": 0x300, "scale": 1.0,
       "swork": {"nib": 3},
       "check": lambda s: s["hp"] == 0 and s["spawn_cnt"] == 1 and
                          s["spawn_time"] == 0x300 // 30 and
                          s["u0_killer"] == 9})
    # group completion suppresses the body's death event but GD emits its own
    # completion event (0x2005 when the latch flag is set, else 0x2008)
    A({"name": "kill-group-done", "rcx": RECB, "edx": -150,
       "r8": RECB + 0x200, "tgt": {"hp": 100, "kind": 1},
       "tunit": {"group": 1, "gflag": 1, "mmaptab": (1, 0)},
       "twork": {"member": 0},
       "groups": {1: {"expect": 1, "dead": 0}},
       "check": lambda s: s["hp"] == 0 and trhas(s, "gd", "caprow") and
                          evids(s) == [0x2005] and
                          s["grp_dead"] == 1 and s["grp_latch"] == 1})
    # group incomplete: death event still fires
    A({"name": "kill-group-partial", "rcx": RECB, "edx": -150,
       "r8": RECB + 0x200, "tgt": {"hp": 100, "kind": 1},
       "tunit": {"group": 1, "mmaptab": (2, 0, 1)},
       "twork": {"member": 0},
       "groups": {1: {"expect": 3, "dead": 0}},
       "check": lambda s: s["hp"] == 0 and trhas(s, "gd") and
                          evids(s) == [0x2008] and
                          s["grp_dead"] == 1})

    # ======== absolute-set thunk ==============================================
    A({"name": "abs-set", "rcx": RECB, "edx": 50, "r8": RECB + 0x200,
       "entry": HP_ABS, "tgt": {"hp": 100, "cap": 150},
       "check": lambda s: s["hp"] == 50})
    A({"name": "abs-zero", "rcx": RECB, "edx": 0, "r8": RECB + 0x200,
       "entry": HP_ABS, "tgt": {"hp": 100},
       "check": lambda s: s["hp"] == 0 and s["ko64"] & 1})
    A({"name": "abs-overcap", "rcx": RECB, "edx": 200, "r8": RECB + 0x200,
       "entry": HP_ABS, "tgt": {"hp": 100, "cap": 150},
       "check": lambda s: s["hp"] == 150})

    # ======== mutants =========================================================
    # each entry: patch site (bytes verified against the shipped image), the
    # probe case fields, and the assertion that MUST hold on the mutant.
    M = []
    B = M.append
    # stored>floor -> non-lethal (0f 8f -> 0f 8d flips jg to jge)
    B({"name": "mut-floor", "patch": [(0x30078E, b"\x0f\x8d")],
       "case": {"rcx": RECB, "edx": -80, "r8": RECB + 0x200,
                "tgt": {"hp": 100}, "tunit": {"floor": 20}},
       "check": lambda s: s["hp"] == 20 and evids(s) == [0x2005] and
                          not s["ko64"] & 1})
    # alive event imm 0x2005 -> 0x2105 (imm32 inside lea edx,[r13+0x2005])
    B({"name": "mut-aliveev", "patch": [(0x30087D, dw(0x2105))],
       "case": {"rcx": RECB, "edx": -30, "r8": RECB + 0x200},
       "check": lambda s: evids(s) == [0x2105]})
    # death event imm 0x2008 -> 0x2018 (imm32 inside add edx,0x2008)
    B({"name": "mut-deadev", "patch": [(0x30085B, dw(0x2018))],
       "case": {"rcx": RECB, "edx": -150, "r8": RECB + 0x200,
                "tgt": {"hp": 100}},
       "check": lambda s: evids(s) == [0x2018]})
    # killer-id store nop'd
    B({"name": "mut-killer", "patch": [(0x3007E5, b"\x90\x90\x90")],
       "case": {"rcx": RECB, "edx": -150, "r8": RECB + 0x200,
                "tgt": {"hp": 100}},
       "check": lambda s: s["u0_killer"] == 0})
    # spawn counter increment nop'd
    B({"name": "mut-spawn", "patch": [(0x300801, b"\x90\x90\x90\x90")],
       "case": {"rcx": RECB, "edx": -150, "r8": RECB + 0x200,
                "tgt": {"hp": 100, "kind": 1}},
       "check": lambda s: s["spawn_cnt"] == 0})
    # gate3's delta<=0 test: jg -> jmp (gate3 never asked)
    B({"name": "mut-gate3", "patch": [(0x300738, b"\xeb")],
       "case": {"rcx": RECB, "edx": -30, "r8": RECB + 0x200,
                "ctx_mode": 1},
       "check": lambda s: s["hp"] == 70 and trabsent(s, "gate3")})
    # downed mask imm 0x80000003 -> 0x80000002 (KO bit0 dropped)
    B({"name": "mut-downmask", "patch": [(0x300628, dw(0x80000002))],
       "case": {"rcx": RECB, "edx": -5, "r8": RECB + 0x200,
                "tgt": {"hp": 10, "m64": 1}},
       "check": lambda s: s["hp"] == 5 and trabsent(s, "field15")})
    # rx-suppress bit4 -> bit5 (shr imm 4 -> 5)
    B({"name": "mut-rxbit", "patch": [(0x300590, b"\x05")],
       "case": {"rcx": RECB, "edx": -30, "r8": RECB + 0x200, "r9": 0x10},
       "check": lambda s: trhas(s, "rx")})
    # kh-suppress invert: not eax nop'd -> bit1 set now ENABLES kh
    B({"name": "mut-kh-inv", "patch": [(0x300591, b"\x90\x90")],
       "case": {"rcx": RECB, "edx": -150, "r8": RECB + 0x200,
                "tgt": {"hp": 100}},
       "check": lambda s: trabsent(s, "kh")})
    # cap-double bit 0x1c -> 0x1d (bt imm, tested twice: compare-cap and clamp)
    B({"name": "mut-capdbl", "patch": [(0x30067F, b"\x1d"),
                                       (0x3006A1, b"\x1d")],
       "case": {"rcx": RECB, "edx": 100, "r8": RECB + 0x200,
                "tgt": {"hp": 150, "cap": 200, "m64": 0x10000000}},
       "check": lambda s: s["hp"] == 200})
    # freeze bit 0x10000 -> 0x20000 (and imm)
    B({"name": "mut-freeze", "patch": [(0x300668, dw(0x20000))],
       "case": {"rcx": RECB, "edx": 100, "r8": RECB + 0x200,
                "tgt": {"hp": 150, "cap": 200, "m64": 0x10000}},
       "check": lambda s: s["hp"] == 200})
    # event-suppress bit2 -> bit3 (test r15b imm)
    B({"name": "mut-evsup", "patch": [(0x3005D5, b"\x08")],
       "case": {"rcx": RECB, "edx": -150, "r8": RECB + 0x200,
                "tgt": {"hp": 100}, "r9": 4},
       "check": lambda s: s["hp"] == 0 and evids(s) == [0x2008]})
    return C, M

def snap_case(w, case):
    gm = w.gm
    tunit = w.tunit
    return {
        "hp": rd32(RECB + 0x48, gm),
        "ko64": rd32(RECB + 0x64, gm),
        "u0_killer": rd32(tunit + 0x30, gm),
        "u0_ev": rd32(tunit + 0x5C, gm),
        "spawn_cnt": rd32(SPAWNB + 8, gm),
        "spawn_time": rd32(SPAWNB + 0xC, gm),
        "grp_dead": rd64(GTAB + 8, gm),
        "grp_latch": rd8(GTAB + 0x10, gm),
        "cap12": rd32(CAPT + 12 * 4, gm),
        "supw": rd32(SUPW, gm),
        "bstate": rd32(G_BSTATE, gm),
        "kring0_kind": rd16(KRING + 0, gm),
        "kring0_src": rd64(KRING + 8, gm),
        "kcur": rd32(G_KCUR, gm),
        "tick": rd32(G_TICK, gm),
        "view0_f26": rd16(VIEWB + 0x26, gm),
        "cblog0": rd64(CBLOG, gm),
        "cblog1": rd64(CBLOG + 8, gm),
        "cblog2": rd64(CBLOG + 0x10, gm),
        "queue0_work": rd64(QUEUE + 0, gm),
        "queue0_dv": rd32(QUEUE + 0xC, gm),
        "trace": w.trace,
        "faults": w.faults,
    }

def run_case(case, raw, secs):
    w = build(case, raw, secs)
    invoke(w, case.get("entry", HP_WRITE),
           case.get("rcx", 0), case.get("edx", 0),
           case.get("r8", 0), case.get("r9", 0))
    snap = snap_case(w, case)
    ok = False
    try:
        ok = bool(case["check"](snap))
    except Exception as e:
        snap["checkerr"] = str(e)
    return snap, ok

def run_all():
    raw, secs = load_image()
    cases, mutants = build_cases()
    passed, total = 0, len(cases)
    results = []
    for case in cases:
        snap, ok = run_case(case, raw, secs)
        if ok:
            passed += 1
        else:
            print("FAIL " + case["name"])
        results.append({"name": case["name"], "ok": ok, "snap": snap})

    mkilled, mtotal = 0, len(mutants)
    mres = []
    for mut in mutants:
        case = dict(mut["case"])
        case["patch"] = mut["patch"]
        case["name"] = mut["name"]
        case["check"] = mut["check"]
        snap, ok = run_case(case, raw, secs)
        if ok:
            mkilled += 1
        else:
            print("MUTANT SURVIVED " + mut["name"])
        mres.append({"name": mut["name"], "killed": ok, "snap": snap})

    print("\n=== SUMMARY ===")
    print("%d/%d cases passed, %d/%d mutants killed" %
          (passed, total, mkilled, mtotal))
    for r in results + mres:
        if ("ok" in r and r["ok"]) or ("killed" in r and r["killed"]):
            continue
        s = r["snap"]
        print("  %s hp=%d ko64=%x killer=%d ev=%x" %
              (r["name"], s["hp"], s["ko64"], s["u0_killer"], s["u0_ev"]))
        print("    trace:", [x[:2] for x in s["trace"]][:24])
        if s["faults"]:
            print("    faults:", s["faults"][:4])
        if "checkerr" in s:
            print("    checkerr:", s["checkerr"])
    with open("result.json", "w") as f:
        json.dump({"total": total, "passed": passed,
                   "mutants": mtotal, "killed": mkilled,
                   "results": results, "mutant_results": mres},
                  f, indent=2)

if __name__ == "__main__":
    run_all()
