# EXP-091 — commit-action callee execution  [REPAIRED COPY - SWE2-ORACLE]
#
# check_repaired.py (ASTRA-REQ-ORACLE-EXP091-RESOLVER-BASE-CONTROL-1003) is a
# copy of commit-callees-exec/check.py (sha256 3a802841...4064068, archived
# unchanged). Differences, and only these:
#   1. G_IMGB = 0x1F83530 (was 0x1F85D30): 0020E602 add rax, qword [rip+...]
#      -> 01F83530 is the cell the shipping resolver 0020E600 reads.
#   2. New case group "tv-row6-*" (direct 0030C0E0 resolver/action-row
#      control) and BASE_CONTROLS (the same cases with the base planted at the
#      old 0x1F85D30; the positive check must refuse them). Supporting fixture
#      keys, both inert unless a case sets them: "imgb_addr" (where the base is
#      planted) and "rowwatch" (code hooks at 0020E609 ret and 0030C1C6
#      cmp byte [rcx+6],0 that record the resolver result and the byte-6
#      effective address/value).
#   3. CLI: --only name[,name...] runs just the named cases / base controls;
#      the full run writes result_repaired.json (never the old result.json).
#
# CONTRACT-commit-action.md section 13 ran 0030F760 (commit) under
# diff_commit_action.py with NINE callees supplied as scripted oracles:
#   003105D0 cancel, 0031B7E0 param->unit resolver, 00316CF0 target-buffer
#   reset, 00316CD0 append, 0030AB40 relation check, 00236850 unit count,
#   00236820 unit getter, 00377C20 status fallback, 00313B30 notify.
# Section 14's open question 3 is "what 00313B30 does with the actor and
# target". This harness executes the six unexecuted bodies — and their
# bounded transitive closure — as shipped bytes at canonical VAs, then
# re-drives 0030F760 with the real callees. (00236850/00236820/00377C20
# already ran real inside EXP-090's closure; they run real here too.)
#
#   REAL (shipped bytes, canonical VA):
#     0030F760  commit body (re-drive; stack arg5 = cancelFirst)
#     003105D0  cancel: 00310780 chain, 0030C970 unlinks (+0x694/5/6),
#               00300280, flag masks, per-unit +0xEA0 clear, 00316CF0(+0x778),
#               vector copies, 003291B0->003839F0, 0016D6A0 (ret 0)
#     00310780  committed-target fixup: 0031B7E0(+0x710), bit0x16 of [unit],
#               +0xEA4 mask bit +0xEA8 dec, 00313B30, 002FEAD0, 00308270,
#               0030C970(+0x694), 00319420(+0xC4), 00319140(1), +0x714==0x414E
#               -> 00317E50
#     0031B7E0  param resolver: gate byte [0x2089340]&0x10 -> 003588B0 ->
#               00263E30 ([obj+0x30])
#     003588B0  packed id: nib=(id>>16)&0xF <5 -> ent=0x2098E10+nib*0x288;
#               [ent] and [ent+8] nonzero, idx<[ent+0x20], [ent+0x10]&1,
#               idx<[list], elem=[list+8+idx*8], word[elem+0x16]==(id>>20)&0x7FF
#     00263FF0 leaf base+n*0x288; 00263E30 leaf [rcx+0x30];
#     00263C20 leaf [rcx+0xE]&0xF (faction nibble)
#     00316CF0  reset: memset(rcx,0,0x208) preserving byte0 bit0; +1 word 0
#     00316CD0  append: [rcx+4]<0x20 -> [rcx+8+n*16]=rdx, ret n+1
#     0030AB40  relation: factn([x+0x10]) both; faction 5 / byte+0x10 bit4 /
#               action-block byte+5 / faction-3 rules; esi=r8&1 ? ecx :
#               bit5(+0x64|+0x3C); ret = (eax==ebp)+1
#     0030C970  unlink: table 0x22C17B0 32x48B {+0,+8}, heads 0x22BE978 /
#               0x22BEB88; cl>0x1F or ==0xFF -> no-op
#     00300280  post-cancel: stats byte+5==0 gate, word +0xDC8!=0xFFFF ->
#               003008A0(cx,1,0,1) then +0xDC8=0xFFFF; +0xE58 -> 00254EE0
#     003008A0  id resolve: 0xFFFF/0x1000/(id&0xF000)>0xE000 -> -1;
#               fam 0x1EEBCC0 + (id>>12)*0x58, bound [e+0x3C]-1, 00309F30,
#               then call [e+0x48] handler (STUBBED - see below)
#     00309F30  fam dispatcher: edx==4 -> 002FD970 else jmp [e+0x50]
#     002FD970  EXP-089 bitset resolver (edx==0 arm real)
#     002FEAD0  targeter fixup: mask gate -> 0030C0E0 -> bit0x14 of [unit+4];
#               else scan [unit+0xEA4] bits vs +0xEA9 / +0x6B6
#     0030C0E0  "committed target still valid" unit scan
#     00308270  post-cancel: bit0x16 -> +0x28=0, 0030C970(+0x695), +0x695=0xFF,
#               0x22C1DB0+idx*12 word->+0xDC8 dword->+0xE58, 0030EDA0, mask
#     0030EDA0  copy 0x4F0 bytes [unit+0xB88]->+0x6B0 (NOT +0x730: the
#               +0x80 at 30EDB6 is cursor advance cancelled by [rcx-0x80]
#               stores; ASTRA suspend-restore-copy-origin-1001, verified
#               cpys-dest-6b0); scan 8x0x4F0 at
#               0x22BEFC0 for self; btr a bit in 0x22BEFB0
#     00313B30  notify: stats [rdx+0x698] mask 0x80000003 + 00377C20;
#               r8d!=0 suppresses ONLY when the status check failed; actor
#               stats byte+5==0 -> collect <=4 party units via 0031B810 into
#               GLOBAL buf 0x22C1788; per-unit event {kind=2-(unit==actor),
#               flag=(r8==0), uid,aid,tid} on stack -> 002ED2A0([unit+8],&rec)
#     002ED2A0  dispatch: 003588B0 -> obj, [obj+0xC0] block word!=0xFFFF ->
#               rec=[0x22C6F28]+word*0x740, [rec+0x284]!=0 -> 003E6B50
#     003E6B50  add rcx,0x650; jmp sink (real; sink body stubbed)
#     plus EXP-089/090 closure bodies all real: 00236850/00236820,
#     00377C20+003148F0+002EF2B0+002EF640, 0031B810+00322C50+002367A0,
#     0020E600, 00808C40, 00253690, 00254EE0, 00316A50(+EXP-089 closure),
#     00290B90, 003BBC80, 0025AAD0, 002F1710(obj planted null),
#     00319420, 00319140, 00317E50, 003291B0, 003839F0
#
#   STUBBED (disclosed, logging):
#     00512F30  render event sink (Phyre-side dispatch) - ret + log rcx/rec
#     0033C9B0  render-matrix rebuild wrapper (00336710+0033E1F0 subtree is
#               the render-state subsystem) - ret + log rcx
#     002FC9D0 / 002FCBA0  fam +0x48 handlers - ret + log args + case eax.
#               (Contract status for these is unchanged: the handler bodies
#               stay oracle-class; what is now measured is WHICH handler
#               003008A0 selects and the argument tuple it passes.)
#     IAT 0x8C2A60 memset (thunk 00861EC0): hook performs real memset on
#               guest memory and logs
#     IAT 0x8C3098 timing source (called twice by 0033E1F0 - unreachable
#               while 0033C9B0 is stubbed; kept armed anyway)
#
#   FIXTURE-PLANTED GLOBALS (disclosed):
#     [0x2EBF190]=FRAME {member-id u16 table T1 +0x5A5A, mode +0x5B04,
#                  desig +0x5AD5}
#     [0x208E688]=UNITS stride 0xF50; [0x208E6A0]=count
#     [0x2EBF130]=OBJD {+4 count} arm-2 bound for 00322C50
#     [0x2ADD100]=U16T flag table {+4 count, +8 u16 @3-byte stride, bit15}
#     [0x21654C4]=index dword (003148F0)
#     [0x2089340]=param-gate byte bit0x10 (0031B7E0 / 00317E69)
#     [0x2098E10]=synthetic nibble table 5x0x288 written over the shipped
#                  .data region (shipped entries hold runtime pointers that
#                  are zero in the image; synthetic entries disclosed)
#     [0x1F83530]=0020E600 stored base planted to HEAP (RVA->fixture space)
#                  (REPAIRED: the original planted 0x1F85D30, which no
#                  shipped body on this path reads)
#     0x22C17B0 link table 32x48; heads 0x22BE978/0x22BEB88
#     0x22C1DB0 12-byte-stride posture/param table (32 entries; row+8 byte
#               is the 0030F760 posture read)
#     0x22BEFC0 8x0x4F0 copy-scan table; 0x22BEFB0 bitset byte
#     [0x22C6F28]=RENDT render table (0x740 stride, +0x284 dword gate)
#     [0x2EBF138]=COBJ {+8 word stride, +0xC dword rva} for 0030C0E0
#     [0x1F44830]=cookie; 0x22C1788 notify buffer; [0x209BE80]=listroot
#     0x2B457D0 64x0x50 zero-scan array; [0x22BE7D0]=0 (002F1710 object)
#     [0x20927C0]=SAVEB, [0x2092758]=PLAYT {+8 cur, +0xC sec},
#     [0x22C2550]=MROOT, [0x2098E20]=flag, [0x1F83450]=POBJ,
#     fam3+8 bitset planted (0x1EEBCC0 is shipped .data; +8 is a runtime
#     pointer field, zero in the image)
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

HEAP   = 0x40000000
STACK  = 0x61000000
RETQ   = 0x62000000
STUBS  = 0x63000000

FRAME  = HEAP + 0x020000
UNITS  = HEAP + 0x100000
U16T   = HEAP + 0x300000
OBJD   = HEAP + 0x310000
SAVEB  = HEAP + 0x330000
PLAYT  = HEAP + 0x340000
MROOT  = HEAP + 0x350000
BITSET = HEAP + 0x360000
LISTB  = HEAP + 0x370000
RENDT  = HEAP + 0x380000
POBJ   = HEAP + 0x390000
COBJ   = HEAP + 0x3A0000
LISTR  = HEAP + 0x3B0000
ROWBUF = HEAP + 0x3C0000
ELEMB  = HEAP + 0x3D0000
BUF    = HEAP + 0x500000     # generic per-case object buffer
UA     = HEAP + 0x600000     # 0030AB40 arg objects
UB     = HEAP + 0x601000
FA     = HEAP + 0x610000     # faction objects
FB     = HEAP + 0x611000
AB     = HEAP + 0x612000     # action blocks
BB     = HEAP + 0x613000

G_FRAME  = 0x2EBF190
G_UNITS  = 0x208E688
G_UCNT   = 0x208E6A0
G_OBJD   = 0x2EBF130
G_U16T   = 0x2ADD100
G_IDX    = 0x21654C4
G_PGATE  = 0x2089340
G_IDXT   = 0x2098E10
# REPAIRED: 0020E600 is mov eax,ecx / 0020E602 add rax, qword [rip+0x1d74f27]
# -> 01F83530 / ret. The original EXP-091 harness planted 0x1F85D30 (0x2800
# higher), so the shipping resolver read the zero .data tail and returned the
# bare RVA. bazaar-callees-exec/check.py L90-91 already uses 0x1F83530.
G_IMGB   = 0x1F83530
G_IMGB_OLD_WRONG = 0x1F85D30   # used only by BASE_CONTROLS (negative control)
G_LH0    = 0x22BE978
G_LH1    = 0x22BEB88
LINKT    = 0x22C17B0
POSTT    = 0x22C1DB0        # 12B stride: +0 word->+0xDC8, +4 dword->+0xE58,
POSTB    = 0x22C1DB8        # +8 byte -> +0x6B9 (0030F760 posture read)
CSCANT   = 0x22BEFC0
CSBITS   = 0x22BEFB0
G_RENDT  = 0x22C6F28
G_COBJ   = 0x2EBF138
G_COOKIE = 0x1F44830
NTBUF    = 0x22C1788
G_290B   = 0x209BE80
G_3BBC   = 0x2B457D0
G_2F17   = 0x22BE7D0
G_SAVE   = 0x20927C0
G_PLAYT  = 0x2092758
G_MROOT  = 0x22C2550
G_FLAG   = 0x2098E20
G_POBJ   = 0x1F83450
FAMT     = 0x1EEBCC0
FAM3_BS  = FAMT + 3 * 0x58 + 8

IAT_MEMSET = 0x8C2A60
IAT_TICK   = 0x8C3098
STUB_MEMSET = STUBS + 0x100
STUB_TICK   = STUBS + 0x200
SINK        = 0x512F30
MRESET      = 0x33C9B0
FAMH0       = 0x2FC9D0
FAMH3       = 0x2FCBA0

IMGADD_RET  = 0x20E609   # 0020E600's ret (rax = resolved pointer)
TV_ROW6_CMP = 0x30C1C6   # 0030C0E0: cmp byte ptr [rcx+6], 0 (action row)

U_STATS  = 0x698
UNITSZ   = 0xF50

CALLS = {
    0x30F760: "commit",   0x3105D0: "cancel",   0x310780: "cfix",
    0x31B7E0: "resolv",   0x3588B0: "idres",    0x263FF0: "tabget",
    0x263E30: "fld30",    0x263C20: "factn",    0x316CF0: "treset",
    0x316CD0: "append",   0x30AB40: "relat",    0x30C970: "unlink",
    0x300280: "postc",    0x3008A0: "idres2",   0x309F30: "famd",
    0x2FD970: "bres",     0x2FEAD0: "tfix",     0x30C0E0: "tvalid",
    0x308270: "postf",    0x30EDA0: "cpys",     0x313B30: "notify",
    0x2ED2A0: "edisp",    0x3E6B50: "esink",
    0x236850: "ucount",   0x236820: "uget",     0x377C20: "flag77",
    0x3148F0: "idxget",   0x2EF2B0: "ef2b0",    0x2EF640: "ef640",
    0x31B810: "party",    0x322C50: "bound",    0x2367A0: "uscan",
    0x20E600: "imgadd",   0x808C40: "cookie",   0x253690: "pcur",
    0x254EE0: "padj",     0x316A50: "upd",
    0x290B90: "lwalk",    0x3BBC80: "zscan",
    0x25AAD0: "lastres",  0x319420: "c4fix",    0x319140: "fix2",
    0x317E50: "fix3",     0x3291B0: "vreset",   0x3839F0: "ffill",
    0x2F1710: "bitclear", 0x16D6A0: "ret0",     0x861EC0: "memset",
    0x325A00: "sldec",    0x317EC0: "ec0",      0x306570: "ownrel",
    0x3DC780: "recref",
    STUB_MEMSET: "hmemset", STUB_TICK: "htick",
    SINK: "eventsink",    MRESET: "mreset",
    FAMH0: "famh0",       FAMH3: "famh3",
}
BODYSTUBS = [SINK, MRESET, FAMH0, FAMH3]   # entry patched to ret; hook logs

def qw(v): return struct.pack("<Q", v & 0xFFFFFFFFFFFFFFFF)
def dw(v): return struct.pack("<I", v & 0xFFFFFFFF)
def hw(v): return struct.pack("<H", v & 0xFFFF)

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
    iat_names = {}
    def rva2off(rva):
        for sva, vs, ra, rs in secs:
            if sva <= rva < sva + rs:
                return ra + rva - sva
        return None
    imp_dir = pe + 24 + (112 if struct.unpack_from("<H", raw, pe + 24)[0] == 0x20B else 96) + 8
    imp_rva, _ = struct.unpack_from("<2I", raw, imp_dir)
    off2 = rva2off(imp_rva)
    i = 0
    while True:
        ilt, ts, fwd, name_rva, iat_rva = struct.unpack_from("<5I", raw, off2 + 20 * i)
        if name_rva == 0:
            break
        dll = raw[rva2off(name_rva):].split(b"\0")[0].decode()
        ilt = ilt or iat_rva
        j = 0
        while True:
            e = struct.unpack_from("<Q", raw, rva2off(ilt) + 8 * j)[0]
            if e == 0:
                break
            if e >> 63:
                nm = "#%x" % (e & 0xffff)
            else:
                no = rva2off(e & 0x7FFFFFFF)
                nm = raw[no + 2:].split(b"\0")[0].decode()
            iat_names[BASE + iat_rva + 8 * j] = "%s!%s" % (dll, nm)
            j += 1
        i += 1
    return raw, secs, iat_names

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

def stats_rec(idv=0, kind=0, m3c=0, m64=0, b5=0):
    r = bytearray(0x1C8)
    r[4] = idv & 0xFF
    r[5] = kind & 0xFF
    r[0xB] = b5 & 0xFF
    struct.pack_into("<I", r, 0x3C, m3c & 0xFFFFFFFF)
    struct.pack_into("<I", r, 0x64, m64 & 0xFFFFFFFF)
    return bytes(r)

def unit(stats=0, ea9=0, ea4=0, ea8=0, flags0=0, flags4=0, b6b6=0,
         u8=0, dc8=0xFFFF, e58=0, b710=0, b714=0, b770=0, b744=0,
         b740=0, b6b0=0, b24=0, b8=0, c4=-1, b694=0xFF, b695=0xFF,
         b696=0xFF, b88=0, f16=True):
    u = bytearray(UNITSZ)
    struct.pack_into("<Q", u, U_STATS, stats)
    u[0xEA9] = ea9 & 0xFF
    struct.pack_into("<I", u, 0xEA4, ea4 & 0xFFFFFFFF)
    u[0xEA8] = ea8 & 0xFF
    struct.pack_into("<Q", u, 0, flags0)
    struct.pack_into("<Q", u, 0xB88, b88)
    struct.pack_into("<I", u, 4, flags4)
    u[0x6B6] = b6b6 & 0xFF
    struct.pack_into("<I", u, 8, u8 & 0xFFFFFFFF)
    struct.pack_into("<H", u, 0xDC8, dc8 & 0xFFFF)
    struct.pack_into("<I", u, 0xE58, e58 & 0xFFFFFFFF)
    struct.pack_into("<I", u, 0x710, b710 & 0xFFFFFFFF)
    struct.pack_into("<H", u, 0x714, b714 & 0xFFFF)
    struct.pack_into("<I", u, 0x770, b770 & 0xFFFFFFFF)
    struct.pack_into("<H", u, 0x744, b744 & 0xFFFF)
    struct.pack_into("<I", u, 0x740, b740 & 0xFFFFFFFF)
    struct.pack_into("<I", u, 0x6B0, b6b0 & 0xFFFFFFFF)
    struct.pack_into("<I", u, 0x24, b24 & 0xFFFFFFFF)
    struct.pack_into("<I", u, 0xC4, c4 & 0xFFFFFFFF)
    u[0x694], u[0x695], u[0x696] = b694 & 0xFF, b695 & 0xFF, b696 & 0xFF
    if f16:
        u[0] |= 0x10
    return bytes(u)

class World:
    def __init__(self, case, raw, secs, iat_names):
        self.case = case
        self.iat_names = iat_names
        self.uc = Uc(UC_ARCH_X86, UC_MODE_64)
        self.gm = GuestMem(self.uc)
        img = bytearray(IMG_HI - IMG_LO)
        for va, vs, ra, rs in secs:
            n = min(vs, rs)
            img[va:va + n] = raw[ra:ra + n]
        self.gm.map(IMG_LO, len(img), bytes(img))
        for a, s in [(HEAP, 0x800000), (STACK, 0x100000), (RETQ, 0x1000),
                     (STUBS, 0x1000)]:
            self.gm.map(a, s)
        gm = self.gm
        gm.w(RETQ, b"\xc3")
        gm.w(STUB_MEMSET, b"\xc3")
        gm.w(STUB_TICK, b"\xc3")
        for slot in iat_names:
            gm.w(slot, qw(0))
        gm.w(IAT_MEMSET, qw(STUB_MEMSET))
        gm.w(IAT_TICK,   qw(STUB_TICK))
        for va in BODYSTUBS:
            gm.w(va, b"\xc3")            # disclosed entry patch -> ret

        gm.w(G_FRAME, qw(case.get("frame", FRAME)))
        gm.w(G_UNITS, qw(case.get("units", UNITS)))
        gm.w(G_UCNT,  dw(case.get("ucount", 0)))
        gm.w(G_OBJD,  qw(case.get("objd", OBJD)))
        gm.w(G_U16T,  qw(case.get("u16t", U16T)))
        gm.w(G_IDX,   dw(case.get("idx", 0)))
        gm.w(OBJD + 4, dw(case.get("objd_count", 0x100)))
        gm.w(G_PGATE, bytes([case.get("pgate", 0x10) & 0xFF]))
        gm.w(case.get("imgb_addr", G_IMGB), qw(HEAP))
        gm.w(G_COOKIE, qw(0x0000C0FFEE00C0FE))  # top16 must be 0 (rol16 check)
        gm.w(G_RENDT, qw(case.get("rendt", RENDT)))
        gm.w(G_COBJ,  qw(case.get("cobj", COBJ)))
        gm.w(G_2F17,  qw(case.get("f1710_obj", 0)))
        gm.w(G_SAVE,  qw(case.get("save", SAVEB)))
        gm.w(G_PLAYT, qw(PLAYT))
        gm.w(G_MROOT, qw(case.get("mroot", MROOT)))
        gm.w(G_FLAG,  bytes([case.get("gate_flag", 1) & 0xFF]))
        gm.w(G_POBJ,  qw(case.get("pobj", POBJ)))
        gm.w(FAM3_BS, qw(case.get("fam3bs", BITSET)))
        gm.w(G_290B,  qw(case.get("obj290", LISTR)))

        for t, off in enumerate((0x5A48, 0x5A5A, 0x5A6C, 0x5A7E, 0x5A90)):
            for i, v in enumerate(case.get("t%d" % t, [])):
                gm.w(FRAME + off + i * 2, hw(v))
        gm.w(FRAME + 0x5B04, dw(case.get("mode", 0)))
        gm.w(FRAME + 0x5AD5, bytes([case.get("desig", 0) & 0xFF]))
        for i, rec in enumerate(case.get("recs", [])):
            gm.w(FRAME + 8 + i * 0x1C8, rec)

        u16e = case.get("u16", [])
        gm.w(U16T + 4, dw(len(u16e)))
        for i, v in enumerate(u16e):
            gm.w(U16T + 8 + i * 3, hw(v))

        for i, u in enumerate(case.get("units_l", [])):
            gm.w(UNITS + i * UNITSZ, u)

        for n, e in case.get("idxt", {}).items():
            b = G_IDXT + n * 0x288
            gm.w(b + 0x00, qw(e.get("mark", 1)))
            gm.w(b + 0x08, qw(e.get("list", 0)))
            gm.w(b + 0x10, bytes([e.get("bit10", 1) & 0xFF]))
            gm.w(b + 0x20, dw(e.get("bound", 0)))

        for i, e in case.get("links", {}).items():
            gm.w(LINKT + i * 48 + 0, qw(e[0]))
            gm.w(LINKT + i * 48 + 8, qw(e[1]))
        if "lh0" in case: gm.w(G_LH0, qw(case["lh0"]))
        if "lh1" in case: gm.w(G_LH1, qw(case["lh1"]))

        for i, v in enumerate(case.get("postb", [])):
            gm.w(POSTB + i * 12, bytes([v & 0xFF]))

        for i, v in enumerate(case.get("cscan", [])):
            gm.w(CSCANT + i * 0x4F0, qw(v))
        if "csbits" in case: gm.w(CSBITS, bytes(case["csbits"]))

        cobj = bytearray(0x20)
        struct.pack_into("<H", cobj, 8, case.get("cobj_stride", 8))
        struct.pack_into("<I", cobj, 0xC, case.get("cobj_rva", ROWBUF - HEAP))
        gm.w(COBJ, cobj)
        if "rowbytes" in case:
            gm.w(ROWBUF, bytes(case["rowbytes"]))

        for i, v in enumerate(case.get("rend", [])):
            e = bytearray(0x740)
            struct.pack_into("<I", e, 0x284, v.get("g284", 1))
            gm.w(RENDT + i * 0x740, e)

        pl = bytearray(0x20)
        struct.pack_into("<I", pl, 8, case.get("play_cur", 0))
        struct.pack_into("<I", pl, 0xC, case.get("play_sec", 0))
        gm.w(PLAYT, pl)
        if "savebytes" in case:
            gm.w(SAVEB, case["savebytes"])

        for a, d in case.get("fill", []):
            gm.w(a, d)
        for va, data in case.get("patch", []):
            gm.w(va, data)

        self.trace, self.faults = [], []
        self.tick = 1000
        uc = self.uc
        uc.hook_add(UC_HOOK_MEM_UNMAPPED, self.on_bad)
        for va in CALLS:
            uc.hook_add(UC_HOOK_CODE, self.on_call, begin=va, end=va)
        self.imgret, self.row6 = [], []
        if case.get("rowwatch"):
            uc.hook_add(UC_HOOK_CODE, self.on_imgret,
                        begin=IMGADD_RET, end=IMGADD_RET)
            uc.hook_add(UC_HOOK_CODE, self.on_row6,
                        begin=TV_ROW6_CMP, end=TV_ROW6_CMP)

    def on_imgret(self, uc, addr, size, _):
        self.imgret.append(hex(uc.reg_read(UC_X86_REG_RAX)))

    def on_row6(self, uc, addr, size, _):
        ea = (uc.reg_read(UC_X86_REG_RCX) + 6) & 0xFFFFFFFFFFFFFFFF
        try:
            b = self.gm.r(ea, 1).hex()
        except KeyError:
            b = "unmapped"
        self.row6.append([hex(ea), b])

    def on_call(self, uc, addr, size, _):
        name = CALLS[addr]
        rcx = uc.reg_read(UC_X86_REG_RCX)
        rdx = uc.reg_read(UC_X86_REG_RDX)
        if addr == STUB_MEMSET:
            n = uc.reg_read(UC_X86_REG_R8) & 0xFFFFFFFF
            try:
                self.gm.w(rcx, bytes([rdx & 0xFF]) * n)
            except KeyError:
                self.faults.append(("STUB", "memset dst=%x n=%x" % (rcx, n)))
            self.trace.append((name, "dst=%x" % rcx, "n=%x" % n,
                               "b=%x" % (rdx & 0xFF)))
            return
        if addr == STUB_TICK:
            self.tick += 37
            uc.reg_write(UC_X86_REG_RAX, self.tick)
            self.trace.append((name, "->%d" % self.tick))
            return
        if addr == SINK:
            rec = self.gm.r(rdx, 16) if rdx else b""
            self.trace.append((name, "rcx=%x" % rcx, "rec=" + rec.hex()))
            return
        if addr == MRESET:
            self.trace.append((name, "rcx=%x" % rcx))
            return
        if addr in (FAMH0, FAMH3):
            r = self.case.get("famh_ret", 1)
            uc.reg_write(UC_X86_REG_RAX, r)
            self.trace.append((name, "rcx=%x" % rcx, "rdx=%x" % rdx,
                               "->%x" % r))
            return
        self.trace.append((name, "rcx=%x" % rcx, "rdx=%x" % rdx))

    def on_bad(self, uc, access, addr, size, value, _):
        self.faults.append(("MEM", hex(addr), "access=%d" % access,
                            "rip=%x" % uc.reg_read(UC_X86_REG_RIP)))
        return False

def build(case, raw, secs, iat_names):
    return World(case, raw, secs, iat_names)

def invoke(w, va, rcx=0, rdx=0, r8=0, r9=0, stack=()):
    uc, gm = w.uc, w.gm
    sp = STACK + 0x80000
    gm.w(sp, qw(RETQ))
    for i, v in enumerate(stack):
        gm.w(sp + 0x28 + i * 8, qw(v))
    uc.reg_write(UC_X86_REG_RSP, sp)
    uc.reg_write(UC_X86_REG_RCX, rcx)
    uc.reg_write(UC_X86_REG_RDX, rdx)
    uc.reg_write(UC_X86_REG_R8, r8)
    uc.reg_write(UC_X86_REG_R9, r9)
    try:
        uc.emu_start(va, RETQ, count=16_000_000)
    except Exception as e:
        w.faults.append(("EMU", str(e), uc.reg_read(UC_X86_REG_RIP)))
    return uc.reg_read(UC_X86_REG_RAX)

def expect(name, snap, cond, why):
    ok = bool(cond)
    print(("PASS " if ok else "FAIL ") + name + ("  -- " + why if not ok else ""))
    return ok

def unit_addr(i): return UNITS + i * UNITSZ
def rec_addr(k):  return FRAME + 8 + k * 0x1C8
def link_e(i):    return LINKT + i * 48
def elem_a(n, i): return ELEMB + n * 0x4000 + i * 0x100

# ---- case list ---------------------------------------------------------------

def idxt_e(n, count, bound=None, bit10=1, mark=1, listp=None):
    return {"mark": mark, "list": listp if listp is not None else LISTB + n * 0x4000,
            "bit10": bit10, "bound": bound if bound is not None else count}

def listw(n, vers, f30=None):
    """nibble-n list: [count][pad][elem ptrs]; elems get +0x16=ver, +0x30=f30 or default."""
    out = [(LISTB + n * 0x4000, dw(len(vers)))]
    for k, ver in enumerate(vers):
        e = elem_a(n, k)
        out.append((LISTB + n * 0x4000 + 8 + k * 8, qw(e)))
        out.append((e + 0x16, hw(ver)))
        out.append((e + 0x30, qw(f30[k] if f30 else 0x50000000 + n * 0x1000 + k)))
    return out

def relcase(name, a5=0, b5=0, fa=1, fb=1, m64=0x20, r8=0, abblk=True,
            bbblk=True, **kw):
    ua = bytearray(UNITSZ); ub = bytearray(UNITSZ)
    struct.pack_into("<Q", ua, 0x10, FA); struct.pack_into("<Q", ub, 0x10, FB)
    struct.pack_into("<Q", ua, 0x698, AB if abblk else 0)
    struct.pack_into("<Q", ub, 0x698, BB if bbblk else 0)
    ua[0] |= 0x10; ub[0] |= 0x10
    c = {"name": name, "entry": 0x30AB40, "rcx": UA, "rdx": UB, "r8": r8,
         "fill": [(UA, bytes(ua)), (UB, bytes(ub)),
                  (FA + 0xE, bytes([fa])), (FB + 0xE, bytes([fb])),
                  (AB + 5, bytes([a5])), (BB + 5, bytes([b5])),
                  (AB + 0x64, dw(m64)), (AB + 0x3C, dw(0))]}
    c.update(kw)
    return c

def build_cases():
    C = []
    A = C.append

    # --- 00316CD0 append ---------------------------------------------------
    # real layout: count at +4; entries at +8 + count*16 (rax=cnt*2, stride 8);
    # bound is count < 0x20; negative counts are NOT guarded (write before +8)
    def bufcase(name, cnt, val=0xDEADBEEF):
        slot = BUF + 8 + (cnt if cnt < 0x80000000 else
                          ctypes.c_int32(cnt).value) * 16
        return {"name": name, "entry": 0x316CD0, "rcx": BUF, "rdx": val,
                "fill": [(BUF + 4, dw(cnt))],
                "memprobe": [(BUF + 4, 4), (slot, 8)]}
    A(dict(bufcase("app-first", 0),
           check=lambda s: s["rets"][0] == "0x1" and s["mem"][1][1] ==
                           qw(0xDEADBEEF).hex()))
    A(dict(bufcase("app-ok", 7),
           check=lambda s: s["rets"][0] == "0x8" and s["mem"][0][1] ==
                           dw(8).hex() and s["mem"][1][1] == qw(0xDEADBEEF).hex()))
    A(dict(bufcase("app-edge", 0x1F),
           check=lambda s: s["rets"][0] == "0x20" and s["mem"][1][1] ==
                           qw(0xDEADBEEF).hex()))
    A(dict(bufcase("app-full", 0x20),
           check=lambda s: s["rets"][0] == "0x20" and s["mem"][1][1] ==
                           "00" * 8))
    # count=-1 slips the jge and writes 8 bytes before the entry array
    A(dict(bufcase("app-neg", 0xFFFFFFFF),
           check=lambda s: s["rets"][0] == "0x0" and
                           s["mem"][0][1] == "00000000" and
                           s["mem"][1][1] == qw(0xDEADBEEF).hex()))

    # --- 00263C20 faction nibble --------------------------------------------
    A({"name": "fact-null", "entry": 0x263C20, "rcx": 0,
       "check": lambda s: s["rets"][0] == "0x0"})
    A({"name": "fact-nib", "entry": 0x263C20, "rcx": BUF,
       "fill": [(BUF + 0xE, b"\xab")],
       "check": lambda s: s["rets"][0] == "0xb"})
    A({"name": "fact-nib0", "entry": 0x263C20, "rcx": BUF,
       "fill": [(BUF + 0xE, b"\xa0")],
       "check": lambda s: s["rets"][0] == "0x0"})

    # --- 00316CF0 reset ------------------------------------------------------
    A({"name": "treset-bit1", "entry": 0x316CF0, "rcx": BUF,
       "fill": [(BUF, b"\x83" + b"\x77" * 0x207)],
       "memprobe": [(BUF, 4), (BUF + 0x204, 4)],
       "check": lambda s: s["mem"][0][1] == "01000000" and
                          s["mem"][1][1] == "00000000" and
                          "hmemset" in [t[0] for t in s["trace"]]})
    A({"name": "treset-bit0", "entry": 0x316CF0, "rcx": BUF,
       "fill": [(BUF, b"\x82" + b"\x77" * 0x207)],
       "memprobe": [(BUF, 4)],
       "check": lambda s: s["mem"][0][1] == "00000000"})

    # --- 0030C970 unlink ------------------------------------------------------
    # entry {+0 a, +8 b}: if [e+8] -> [[e+8]] = [e] else head0=[e];
    #                     if [e]   -> [[e]+8] = [e+8] else head1=[e+8];
    #                     entry zeroed. (measured, not assumed)
    A({"name": "unlink-mid", "entry": 0x30C970, "rcx": 2,
       "links": {1: (link_e(2), link_e(3)), 2: (link_e(1), link_e(3)),
                 3: (link_e(2), 0)},
       "lh0": link_e(1), "lh1": link_e(3),
       "memprobe": [(link_e(2), 16), (link_e(3), 8), (link_e(1) + 8, 8),
                    (link_e(2) + 0x1C, 2), (link_e(2) + 0x24, 4),
                    (link_e(2) + 0x28, 4)],
       "check": lambda s: s["mem"][0][1] == "00" * 16 and
                          s["mem"][1][1] == qw(link_e(1)).hex() and
                          s["mem"][2][1] == qw(link_e(3)).hex() and
                          s["mem"][3][1] == "ffff" and
                          s["mem"][4][1] == "ffffffff" and
                          s["mem"][5][1] == "00000080"})
    A({"name": "unlink-ff", "entry": 0x30C970, "rcx": 0xFF,
       "links": {2: (link_e(1), link_e(3))},
       "memprobe": [(link_e(2), 16)],
       "check": lambda s: s["mem"][0][1] == (qw(link_e(1)) + qw(link_e(3))).hex()})
    A({"name": "unlink-oob", "entry": 0x30C970, "rcx": 0x20,
       "links": {2: (link_e(1), link_e(3))},
       "memprobe": [(link_e(2), 16)],
       "check": lambda s: s["mem"][0][1] == (qw(link_e(1)) + qw(link_e(3))).hex()})
    A({"name": "unlink-last", "entry": 0x30C970, "rcx": 0x1F,
       "links": {0x1F: (link_e(1), 0), 1: (0, link_e(0x1F))},
       "lh0": link_e(1), "lh1": link_e(0x1F),
       "memprobe": [(link_e(0x1F), 16), (link_e(1) + 8, 8), (G_LH0, 8)],
       "check": lambda s: s["mem"][0][1] == "00" * 16 and
                          s["mem"][1][1] == "00" * 8 and
                          s["mem"][2][1] == qw(link_e(1)).hex()})
    # entry+0x18!=0 arm: resolv(entry+0x20) -> 00306570; global gate != rcx
    A({"name": "unlink-own", "entry": 0x30C970, "rcx": 2,
       "links": {2: (link_e(1), link_e(3))},
       "lh0": link_e(1), "lh1": link_e(3),
       "idxt": {2: idxt_e(2, 2)},
       "fill": (listw(2, [0, 0], f30=[0, unit_addr(1)]) +
                [(link_e(2) + 0x18, dw(1)),
                 (link_e(2) + 0x20, dw((2 << 16) | 1)),
                 (0x2262168, qw(0xDEADBEEF))]),
       "check": lambda s: "resolv" in [t[0] for t in s["trace"]] and
                          "ownrel" in [t[0] for t in s["trace"]]})

    # --- 003588B0 packed-id resolver ------------------------------------------
    A({"name": "idr-hit", "entry": 0x3588B0, "rcx": (0x33 << 20) | (2 << 16) | 1,
       "idxt": {2: idxt_e(2, 2)},
       "fill": listw(2, [0x77, 0x33]),
       "check": lambda s: s["rets64"][0] == hex(elem_a(2, 1))})
    A({"name": "idr-zero", "entry": 0x3588B0, "rcx": 0,
       "check": lambda s: s["rets"][0] == "0x0"})
    A({"name": "idr-nib5", "entry": 0x3588B0, "rcx": (5 << 16) | 1,
       "idxt": {5: idxt_e(5, 2)},
       "fill": listw(5, [0, 0]),
       "check": lambda s: s["rets"][0] == "0x0"})
    A({"name": "idr-nib4", "entry": 0x3588B0, "rcx": (4 << 16) | 0,
       "idxt": {4: idxt_e(4, 1)},
       "fill": listw(4, [0]),
       "check": lambda s: s["rets64"][0] == hex(elem_a(4, 0))})
    A({"name": "idr-nomark", "entry": 0x3588B0, "rcx": (2 << 16) | 0,
       "idxt": {2: idxt_e(2, 1, mark=0)},
       "fill": listw(2, [0]),
       "check": lambda s: s["rets"][0] == "0x0"})
    A({"name": "idr-nolist", "entry": 0x3588B0, "rcx": (2 << 16) | 0,
       "idxt": {2: idxt_e(2, 1, listp=0)},
       "check": lambda s: s["rets"][0] == "0x0"})
    A({"name": "idr-bound", "entry": 0x3588B0, "rcx": (2 << 16) | 3,
       "idxt": {2: idxt_e(2, 4, bound=3)},
       "fill": listw(2, [0, 0, 0, 0]),
       "check": lambda s: s["rets"][0] == "0x0"})
    A({"name": "idr-bit10", "entry": 0x3588B0, "rcx": (2 << 16) | 0,
       "idxt": {2: idxt_e(2, 1, bit10=0)},
       "fill": listw(2, [0]),
       "check": lambda s: s["rets"][0] == "0x0"})
    A({"name": "idr-lcnt", "entry": 0x3588B0, "rcx": (2 << 16) | 2,
       "idxt": {2: idxt_e(2, 2, bound=5)},
       "fill": listw(2, [0, 0]),
       "check": lambda s: s["rets"][0] == "0x0"})
    A({"name": "idr-vermis", "entry": 0x3588B0,
       "rcx": (0x44 << 20) | (2 << 16) | 1,
       "idxt": {2: idxt_e(2, 2)},
       "fill": listw(2, [0x77, 0x33]),
       "check": lambda s: s["rets"][0] == "0x0"})
    A({"name": "idr-elemnull", "entry": 0x3588B0, "rcx": (2 << 16) | 0,
       "idxt": {2: idxt_e(2, 1)},
       "fill": [(LISTB + 2 * 0x4000, dw(1))],   # count=1, elem ptr = 0
       "check": lambda s: s["rets"][0] == "0x0"})

    # --- 0031B7E0 param resolver ----------------------------------------------
    A({"name": "res-gateoff", "entry": 0x31B7E0, "rcx": (2 << 16) | 1,
       "pgate": 0, "idxt": {2: idxt_e(2, 2)},
       "fill": listw(2, [0, 0]),
       "check": lambda s: s["rets"][0] == "0x0" and
                          "idres" not in [t[0] for t in s["trace"]]})
    A({"name": "res-hit", "entry": 0x31B7E0, "rcx": (2 << 16) | 1,
       "pgate": 0x10, "idxt": {2: idxt_e(2, 2)},
       "fill": listw(2, [0, 0]),
       "check": lambda s: s["rets64"][0] == hex(0x50000000 + 2 * 0x1000 + 1)})
    A({"name": "res-miss", "entry": 0x31B7E0, "rcx": (2 << 16) | 9,
       "pgate": 0x10, "idxt": {2: idxt_e(2, 1)},
       "fill": listw(2, [0]),
       "check": lambda s: s["rets"][0] == "0x0"})

    # --- 0030AB40 relation -----------------------------------------------------
    A(dict(relcase("rel-same", fa=1, fb=1, m64=0x20),
           check=lambda s: s["rets"][0] == "0x2"))
    A(dict(relcase("rel-diff", fa=1, fb=2, m64=0x20),
           check=lambda s: s["rets"][0] == "0x2"))  # fb 1 vs 2: same result
    A(dict(relcase("rel-null-a"), rcx=0,
           check=lambda s: s["rets"][0] == "0x0"))
    A(dict(relcase("rel-null-b"), rdx=0,
           check=lambda s: s["rets"][0] == "0x0"))
    A(dict(relcase("rel-fa5", fa=5, fb=1),
           check=lambda s: s["rets"][0] == "0x0"))
    A(dict(relcase("rel-fb5", fa=1, fb=5),
           check=lambda s: s["rets"][0] == "0x0"))
    A(dict(relcase("rel-fa4", fa=4, fb=1),
           check=lambda s: s["rets"][0] == "0x2"))
    A(dict(relcase("rel-sbit0", fa=1, fb=1, m64=0),
           check=lambda s: s["rets"][0] == "0x1"))
    A(dict(relcase("rel-a5x-fa3", a5=1, fa=3, fb=1, m64=0x20),
           check=lambda s: s["rets"][0] == "0x2"))
    # a5!=0 and actorfac!=3: ebp=0 when target +5==0 -> vs bit5=1 -> 1
    A(dict(relcase("rel-a5x-fa1", a5=1, fa=1, fb=1, m64=0x20),
           check=lambda s: s["rets"][0] == "0x1"))
    A(dict(relcase("rel-r8", fa=1, fb=1, m64=0x20, r8=1),
           check=lambda s: s["rets"][0] == "0x1"))
    # byte+0x10 bit4 missing on either side -> 0
    rc = relcase("rel-nof4a", fa=1, fb=1)
    ua = bytearray(rc["fill"][0][1]); ua[0] &= ~0x10
    rc["fill"][0] = (UA, bytes(ua))
    A(dict(rc, check=lambda s: s["rets"][0] == "0x0"))
    # action-block absent on A: faction rules resolve ebp, then esi==0
    # dereferences the NULL actor block at 0x30AC14 -- a real crash input
    A(dict(relcase("rel-ablk0-fault", abblk=False, fa=3, fb=3, m64=0x20),
           expect_fault=True,
           check=lambda s: any(f[3] == "rip=30ac14" for f in s["faults"])))
    # ... but esi==1 (r8&1) skips the deref entirely: returns via ecx=0
    A(dict(relcase("rel-ablk0-r8", abblk=False, fa=1, fb=1, r8=1),
           check=lambda s: s["rets"][0] == "0x2"))

    # --- 003105D0 cancel ---------------------------------------------------------
    A({"name": "canc-null", "entry": 0x3105D0, "rcx": 0,
       "check": lambda s: [t[0] for t in s["trace"]] == ["cancel"]})
    A({"name": "canc-noblk", "entry": 0x3105D0, "rcx": unit_addr(0),
       "ucount": 1, "units_l": [unit(stats=0)],
       "check": lambda s: [t[0] for t in s["trace"]] == ["cancel"]})
    # full cancel. cfix semantics (measured): bit22 of [unit] SET skips the
    # committed-target fixup entirely; CLEAR + resolved unit + target's
    # +0xEA4 has actor's +0xEA9 bit -> dec +0xEA8, clear bit, notify, tfix.
    # postf(00308270) only runs its body when bit22 is SET.
    def canc_fixture(**kw):
        recs = [stats_rec() for _ in range(0x28)]
        recs[0] = stats_rec(idv=3, kind=0)          # actor stats
        recs[1] = stats_rec(idv=9, kind=1)          # committed-target stats
        u0 = unit(stats=rec_addr(0), ea9=2,
                  flags0=kw.pop("flags0", 1 << 0x16),
                  b88=kw.pop("b88", HEAP + 0x540000),
                  b710=kw.pop("u0_710", (2 << 16) | 1),
                  b714=kw.pop("b714", 0x100),
                  dc8=kw.pop("dc8", 0xFFFF), e58=kw.pop("e58", 0))
        u1 = kw.pop("tunit", unit(stats=rec_addr(1), ea4=1 << 2, ea8=3))
        case = {"entry": 0x3105D0, "rcx": unit_addr(0),
                "ucount": 2, "objd_count": 0x20,
                "units_l": kw.pop("units_l", [u0, u1]), "recs": recs,
                "idxt": {2: idxt_e(2, 2)},
                "pgate": 0x10, "t1": [0xFF] * 9, "idx": 0, "u16": [0],
                "csbits": [0xFF] * 8,
                "memprobe": [(unit_addr(1) + 0xEA4, 4),
                             (unit_addr(1) + 0xEA8, 1),
                             (unit_addr(0) + 0x6B6, 1),
                             (unit_addr(0) + 0x695, 1),
                             (unit_addr(0) + 0x690, 4),
                             (unit_addr(0) + 0x778 + 4, 4),
                             (unit_addr(0) + 0x210, 8),
                             (CSBITS, 1)]}
        case.update(kw)
        f = list(case["fill"]) if "fill" in case else []
        f += listw(2, [0, 0], f30=[0, unit_addr(1)])
        case["fill"] = f
        return case
    # bit22 set: fixup skipped (EA4/EA8 untouched, no notify), but postf runs:
    # +0x695->0xFF via its own unlink, cpys copies 0x4F0 from [u0+0xB88],
    # +0x690=0; cancel tail: +0x6B6=0, target-buffer reset, vreset ffill.
    A(dict(canc_fixture(), name="canc-full",
           check=lambda s: "cfix" in [t[0] for t in s["trace"]] and
                           "postf" in [t[0] for t in s["trace"]] and
                           "notify" not in [t[0] for t in s["trace"]] and
                           s["mem"][0][1] == dw(4).hex() and     # EA4 untouched
                           s["mem"][1][1] == "03" and            # EA8 untouched
                           s["mem"][2][1] == "00" and            # +0x6B6 zeroed
                           s["mem"][3][1] == "ff" and            # +0x695 -> 0xFF
                           s["mem"][4][1] == "00000000" and      # +0x690 zeroed
                           s["mem"][5][1] == "00000000" and      # +0x778 count 0
                           s["mem"][6][1] == "ff" * 8 and        # 003839F0 fill
                           s["mem"][7][1] == "ff"))              # no cscan match
    # bit22 clear + target mask bit set -> fixup: EA8 dec, EA4 clear,
    # notify + tfix real; postf skips its body (bit22 now clear)
    cu = unit(stats=rec_addr(0), ea9=2, flags0=0,
              b710=(2 << 16) | 1, b88=HEAP + 0x540000)
    A(dict(canc_fixture(), name="canc-fixup",
           units_l=[cu, unit(stats=rec_addr(1), ea4=1 << 2, ea8=3)],
           check=lambda s: "notify" in [t[0] for t in s["trace"]] and
                           "tfix" in [t[0] for t in s["trace"]] and
                           s["mem"][0][1] == dw(0).hex() and     # EA4 cleared
                           s["mem"][1][1] == "02"))              # EA8 3->2
    # bit22 clear + target mask bit NOT set -> no fixup, no notify
    A(dict(canc_fixture(),
           units_l=[cu, unit(stats=rec_addr(1), ea4=0, ea8=3)],
           name="canc-maskclear",
           check=lambda s: "notify" not in [t[0] for t in s["trace"]] and
                           "tfix" not in [t[0] for t in s["trace"]] and
                           s["mem"][1][1] == "03"))
    # no committed target -> resolver 0 -> postf-only path
    cu2 = unit(stats=rec_addr(0), ea9=2, flags0=0, b710=0,
               b88=HEAP + 0x540000)
    A(dict(canc_fixture(),
           units_l=[cu2, unit(stats=rec_addr(1), ea4=1 << 2, ea8=3)],
           name="canc-notarget",
           check=lambda s: "notify" not in [t[0] for t in s["trace"]] and
                           s["mem"][5][1] == "00000000"))
    # cpys table hit: source ptr == CSCANT+2*0x4F0 -> btr clears CSBITS bit2
    cu3 = unit(stats=rec_addr(0), ea9=2, flags0=1 << 0x16, b710=0,
               b88=CSCANT + 2 * 0x4F0)
    A(dict(canc_fixture(),
           units_l=[cu3, unit(stats=rec_addr(1))],
           name="canc-cpyhit",
           check=lambda s: "cpys" in [t[0] for t in s["trace"]] and
                           s["mem"][7][1] == "fb"))

    # --- EXP-091 destination regression (ASTRA-REQ-ORACLE-SUSPEND-COPY-
    # REGRESSION-1001): 30EDA0 writes unit[0x6B0,0xBA0), NOT [0x730,0xC20).
    # Direct entry at 0030EDA0. Source = patterned slot 2 of CSCANT; the
    # pattern's +0x4D8 qword (which lands on unit+0xB88) is slot 5's base,
    # so an implementation that re-read the overwritten +B88 instead of the
    # incoming r8 would clear bit5 -- the shipped body must clear bit2.
    src2 = CSCANT + 2 * 0x4F0
    pat = bytearray((0xA5 + i * 0x11) & 0xFF for i in range(0x4F0))
    struct.pack_into("<Q", pat, 0x4D8, CSCANT + 5 * 0x4F0)
    A({"name": "cpys-dest-6b0", "entry": 0x30EDA0, "rcx": unit_addr(0),
       "ucount": 1, "units_l": [unit(stats=0, b88=src2)],
       "csbits": [0xFF] * 8,
       "fill": [(src2, bytes(pat)),
                (unit_addr(0) + 0x6A8, b"\xcc" * 8),      # pre-canary
                (unit_addr(0) + 0x6B0, b"\xdd" * 0x4F0),  # poison dest
                (unit_addr(0) + 0xB88, qw(src2)),         # incoming src ptr
                (unit_addr(0) + 0xBA0, b"\xcc" * 8)],     # post-canary
       "memprobe": [(unit_addr(0) + 0x6B0, 0x4F0),
                    (unit_addr(0) + 0x6A8, 8),
                    (unit_addr(0) + 0xBA0, 8),
                    (unit_addr(0) + 0xB88, 8),
                    (CSBITS, 1)],
       "check": lambda s: s["mem"][0][1] == bytes(pat).hex() and
                          s["mem"][1][1] == "cc" * 8 and
                          s["mem"][2][1] == "cc" * 8 and
                          s["mem"][3][1] == qw(CSCANT + 5 * 0x4F0).hex() and
                          s["mem"][4][1] == "fb" and
                          s["rets"][0] == "0x1"})
    # source outside the 8-slot table: copy still runs, bitmap untouched
    src9 = HEAP + 0x700000
    pat2 = bytes((0x3C + i * 0x07) & 0xFF for i in range(0x4F0))
    A({"name": "cpys-nohit", "entry": 0x30EDA0, "rcx": unit_addr(0),
       "ucount": 1, "units_l": [unit(stats=0, b88=src9)],
       "csbits": [0xFF] * 8,
       "fill": [(src9, pat2), (unit_addr(0) + 0x6B0, b"\xdd" * 0x4F0),
                (unit_addr(0) + 0xB88, qw(src9))],
       "memprobe": [(unit_addr(0) + 0x6B0, 0x4F0), (CSBITS, 1)],
       "check": lambda s: s["mem"][0][1] == pat2.hex() and
                          s["mem"][1][1] == "ff" and
                          s["rets"][0] == "0x1"})

    # --- 00313B30 notify / dispatch --------------------------------------------
    # actor=u0 stats rec0 (kind0 -> collect path), target=u1 stats rec1.
    # unit2 is the party member (t1[0]=7 -> uscan matches stats+4==7).
    # idxt{0} + elem(0,5) +0xC0->block + rendt makes u8=5 resolvable so the
    # event record reaches the (stubbed, logging) sink with real bytes.
    def ntf_fixture(**kw):
        recs = [stats_rec() for _ in range(0x28)]
        recs[0] = kw.pop("arec", stats_rec(idv=3, kind=0))
        recs[1] = kw.pop("trec", stats_rec(idv=9, kind=1))
        recs[2] = kw.pop("mrec", stats_rec(idv=7, kind=0))
        case = {"entry": 0x313B30, "rcx": unit_addr(0), "rdx": unit_addr(1),
                "r8": kw.pop("r8", 0), "ucount": 3, "objd_count": 0x20,
                "units_l": kw.pop("units_l",
                    [unit(stats=rec_addr(0), u8=0x11),
                     unit(stats=rec_addr(1), u8=0x22),
                     unit(stats=rec_addr(2), u8=5)]),
                "recs": recs, "t1": [7, 0xFF, 0xFF, 0xFF] + [0] * 5,
                "idx": 0, "u16": [0], "pgate": 0x10,
                "idxt": {0: idxt_e(0, 6)},
                "rend": [{"g284": 1}] * 8}
        f = listw(0, [0] * 6)
        f += [(elem_a(0, 5) + 0xC0, qw(HEAP + 0x531000)),
              (HEAP + 0x531000, dw(3))]
        case["fill"] = f
        case.update(kw)
        return case
    # collect + dispatch: eventsink receives {kind=2 (other), flag=1 (r8==0),
    # uid=5, aid=0x11, tid=0x22} = "02010000 05000000 11000000 22000000"
    A(dict(ntf_fixture(), name="ntf-dispatch",
           check=lambda s: "party" in [t[0] for t in s["trace"]] and
                           any(t[0] == "eventsink" and
                               "02010000050000001100000022000000" in t[2]
                               for t in s["trace"])))
    # r8=1 + masked target stats + flag77 fail -> jne 0x313cb4: NO dispatch
    A(dict(ntf_fixture(r8=1, trec=stats_rec(idv=9, kind=1, m64=1)),
           name="ntf-suppress",
           check=lambda s: "edisp" not in [t[0] for t in s["trace"]]))
    # r8=1 but target stats clean -> still dispatches (flag byte = 0)
    A(dict(ntf_fixture(r8=1), name="ntf-r8-live",
           check=lambda s: any(t[0] == "eventsink" and
                               "02000000050000001100000022000000" in t[2]
                               for t in s["trace"])))
    # target stats null: status check skipped -> r8 decides
    A(dict(ntf_fixture(r8=0,
           units_l=[unit(stats=rec_addr(0), u8=0x11), unit(stats=0),
                    unit(stats=rec_addr(2), u8=5)]),
           name="ntf-nostat-r0",
           check=lambda s: "edisp" in [t[0] for t in s["trace"]]))
    A(dict(ntf_fixture(r8=1,
           units_l=[unit(stats=rec_addr(0), u8=0x11), unit(stats=0),
                    unit(stats=rec_addr(2), u8=5)]),
           name="ntf-nostat-r1",
           check=lambda s: "edisp" not in [t[0] for t in s["trace"]]))
    # masked stats + flag77 SET -> dispatch even with r8=1
    A(dict(ntf_fixture(r8=1, trec=stats_rec(idv=9, kind=1, m64=1),
           u16=[0x8000]),
           name="ntf-flag77",
           check=lambda s: "edisp" in [t[0] for t in s["trace"]]))
    # actor stats byte+5 != 0 -> single self-record path (kind=1): one edisp
    # with the ACTOR's id (0x11), not the party member's
    A(dict(ntf_fixture(arec=stats_rec(idv=3, kind=1)),
           name="ntf-actorbusy",
           check=lambda s: [t for t in s["trace"] if t[0] == "edisp"] and
                           all(t[1] == "rcx=11" for t in s["trace"]
                               if t[0] == "edisp")))
    # collected member masked + flag77 fail -> not collected -> no dispatch
    A(dict(ntf_fixture(mrec=stats_rec(idv=7, kind=0, m64=1)),
           name="ntf-member-masked",
           check=lambda s: "edisp" not in [t[0] for t in s["trace"]]))
    # rdx==0 -> unconditional [rdx+0x698] deref at 0x313B4F: real crash input
    A(dict(ntf_fixture(), name="ntf-nulltgt", rdx=0, expect_fault=True,
           check=lambda s: any(f[3] == "rip=313b4f" for f in s["faults"])))

    # 002ED2A0 dispatch gates: idres(rcx) -> elem; [elem+0xC0] block;
    # dword != -1; word -> rec = RENDT + word*0x740; [rec+0x284]!=0 -> sink
    BLK = HEAP + 0x531000
    def ed_fixture(**kw):
        case = {"entry": 0x2ED2A0, "rcx": (2 << 16) | 0, "rdx": BUF,
                "idxt": {2: idxt_e(2, 1)},
                "fill": (listw(2, [0]) +
                         [(BUF, b"\x02\x01" + dw(5) + dw(6) + dw(7))]),
                "rend": [{"g284": 1}] * 8}
        case.update(kw)
        return case
    edf = ed_fixture()
    edf["fill"] += [(elem_a(2, 0) + 0xC0, qw(BLK)), (BLK, dw(7))]
    A(dict(edf, name="ed-full",
           check=lambda s: "eventsink" in [t[0] for t in s["trace"]]))
    A(dict(ed_fixture(), name="ed-nores",
           check=lambda s: "eventsink" not in [t[0] for t in s["trace"]]))
    A(dict(ed_fixture(fill=listw(2, [0])), name="ed-noblk",
           check=lambda s: "eventsink" not in [t[0] for t in s["trace"]]))
    edf3 = ed_fixture()
    edf3["fill"] += [(elem_a(2, 0) + 0xC0, qw(BLK)), (BLK, dw(0xFFFFFFFF))]
    A(dict(edf3, name="ed-blkneg1",
           check=lambda s: "eventsink" not in [t[0] for t in s["trace"]]))
    edf4 = ed_fixture()
    edf4["fill"] += [(elem_a(2, 0) + 0xC0, qw(BLK)), (BLK, dw(7))]
    edf4["rend"] = [{"g284": 1}] * 7 + [{"g284": 0}]
    A(dict(edf4, name="ed-g284zero",
           check=lambda s: "eventsink" not in [t[0] for t in s["trace"]]))

    # --- 0030F760 commit re-drive -----------------------------------------------
    def com_fixture(**kw):
        recs = [stats_rec() for _ in range(0x28)]
        recs[0] = stats_rec(idv=3, kind=0)
        recs[1] = kw.pop("trec", stats_rec(idv=9, kind=1))
        u0 = unit(stats=rec_addr(0), ea9=2, b6b0=kw.pop("b6b0", 0),
                  b770=kw.pop("b770", 0), b744=kw.pop("b744", 0),
                  b740=kw.pop("b740", 0), b24=kw.pop("b24", 0),
                  u8=kw.pop("u0_u8", 0), dc8=kw.pop("dc8", 0xFFFF),
                  e58=kw.pop("e58", 0), b710=kw.pop("u0_710", 0),
                  b88=HEAP + 0x540000)
        u1 = kw.pop("tunit", unit(stats=rec_addr(1), ea4=0, ea8=0, u8=0x22))
        case = {"entry": 0x30F760, "rcx": unit_addr(0), "rdx": kw.pop("wrk", 0),
                "r8": kw.pop("aid", 0x100), "r9": kw.pop("param", (2 << 16) | 1),
                "ucount": 2, "objd_count": 0x20,
                "units_l": kw.pop("units_l", [u0, u1]), "recs": recs,
                "idxt": {2: idxt_e(2, 2)},
                "mode": 1, "desig": 0, "t1": [0xFF] * 9,
                "pgate": 0x10, "idx": 0, "u16": [0],
                "postb": kw.pop("postb", [0x55] * 32),
                "memprobe": [(unit_addr(0) + 0x778 + 4, 4),     # 0 buf count
                             (unit_addr(0) + 0x778 + 8, 8),     # 1 buf[0]
                             (unit_addr(0) + 0x710, 4),         # 2 param
                             (unit_addr(0) + 0x714, 2),         # 3 action id
                             (unit_addr(0) + 0x6B9, 1),         # 4 posture byte
                             (unit_addr(0) + 0x6B6, 1),         # 5 posture flag
                             (unit_addr(0) + 0x750, 4),         # 6 mask dst
                             (unit_addr(0) + 0x754, 4),         # 7 related dst
                             (unit_addr(1) + 0xEA8, 1),         # 8 target EA8
                             (unit_addr(1) + 0xEA4, 4),         # 9 target EA4
                             (unit_addr(0) + 0x770, 4)]}        # 10 latch
        case.update(kw)
        f = list(case.get("fill", []))
        f += listw(2, [0, 0], f30=[0, unit_addr(1)])
        case["fill"] = f
        return case

    A(dict(com_fixture(), name="com-b1-basic",
           check=lambda s: s["rets"][0] == "0x1" and
                           s["mem"][0][1] == dw(1).hex() and     # buf count 1
                           s["mem"][2][1] == dw((2 << 16) | 1).hex() and
                           s["mem"][3][1] == hw(0x100).hex() and
                           "relat" in [t[0] for t in s["trace"]] and
                           s["mem"][6][1] == dw((2 << 16) | 1).hex() and
                           s["mem"][7][1] == dw((2 << 16) | 1).hex() and
                           s["mem"][8][1] == "01" and            # EA8 0->1
                           s["mem"][9][1] == dw(4).hex()))       # EA4 bit2 set
    A(dict(com_fixture(aid=0x300), name="com-badid",
           check=lambda s: s["rets"][0] == "0x0"))
    A(dict(com_fixture(aid=0x21E), name="com-b1-edge",
           check=lambda s: s["rets"][0] == "0x1"))
    A(dict(com_fixture(aid=0x21F), name="com-b1-edge2",
           check=lambda s: s["rets"][0] == "0x0"))
    A(dict(com_fixture(aid=0x4000), name="com-b2-lo",
           check=lambda s: s["rets"][0] == "0x1" and
                           s["mem"][0][1] == dw(0).hex()))       # no reset/append
    A(dict(com_fixture(aid=0x4166), name="com-b2-hi",
           check=lambda s: s["rets"][0] == "0x1"))
    A(dict(com_fixture(aid=0x4167), name="com-b2-oob",
           check=lambda s: s["rets"][0] == "0x0"))
    fc = com_fixture()
    fc["stack"] = [1]
    fc["name"] = "com-cancel-first"
    fc["check"] = (lambda s: s["rets"][0] == "0x1" and
                   [t[0] for t in s["trace"]][:2] == ["commit", "cancel"])
    A(fc)
    A(dict(com_fixture(param=0), name="com-notarget",
           check=lambda s: s["rets"][0] == "0x1" and
                           "relat" not in [t[0] for t in s["trace"]]))
    # gate byte bit0x10 clear -> 0031B7E0 returns 0 before calling idres
    A(dict(com_fixture(pgate=0), name="com-gateoff",
           check=lambda s: s["rets"][0] == "0x1" and
                           "resolv" in [t[0] for t in s["trace"]] and
                           "idres" not in [t[0] for t in s["trace"]] and
                           "relat" not in [t[0] for t in s["trace"]]))
    # +0x770 latch: stats+5==0 and id/param match prior -> +0x770 preserved
    A(dict(com_fixture(b770=1, b744=0x100, b740=(2 << 16) | 1),
           name="com-770-same",
           check=lambda s: s["rets"][0] == "0x1" and
                           s["mem"][10][1] == "01000000"))
    # latch mismatch on committed id -> +0x770 cleared
    A(dict(com_fixture(b770=1, b744=0x999, b740=(2 << 16) | 1),
           name="com-770-diff",
           check=lambda s: s["rets"][0] == "0x1" and
                           s["mem"][10][1] == "00000000"))
    # +0x6B0 bit1 -> consumed, posture byte +0x6B9 = postb[ea9], +0x6B6=1
    A(dict(com_fixture(b6b0=2), name="com-posture",
           check=lambda s: s["rets"][0] == "0x1" and
                           s["mem"][4][1] == "55" and
                           s["mem"][5][1] == "01"))
    # +0x24 != +8 (actor unit id 1 vs group 0): +0x750 cleared early,
    # +0x754 still gets param (relat>=2), propagation loop skipped
    A(dict(com_fixture(b24=0, u0_u8=1),
           name="com-noprop",
           check=lambda s: s["rets"][0] == "0x1" and
                           s["mem"][6][1] == "00000000" and
                           s["mem"][7][1] == dw((2 << 16) | 1).hex() and
                           "ucount" not in [t[0] for t in s["trace"]]))
    # target already has actor's bit in +0xEA4 -> no notify
    A(dict(com_fixture(tunit=unit(stats=rec_addr(1), ea4=1 << 2, ea8=1,
                                  u8=0x22)),
           name="com-masked",
           check=lambda s: s["rets"][0] == "0x1" and
                           s["mem"][8][1] == "01" and
                           "notify" not in [t[0] for t in s["trace"]]))

    # --- 003008A0 id resolver -----------------------------------------------------
    A({"name": "ir2-ffff", "entry": 0x3008A0, "rcx": 0xFFFF,
       "check": lambda s: s["rets"][0] == "0xffffffff"})
    A({"name": "ir2-1000", "entry": 0x3008A0, "rcx": 0x1000,
       "check": lambda s: s["rets"][0] == "0xffffffff"})
    A({"name": "ir2-f000", "entry": 0x3008A0, "rcx": 0xF000,
       "check": lambda s: s["rets"][0] == "0xffffffff"})
    # 0xE000 is IN bounds (nibble >0xE000 fails): fam14 count 0xFFF passes,
    # famd returns 0 (fam14 +0x50==0), resolver 0x2FD880 r9!=1 -> 0
    A({"name": "ir2-e000", "entry": 0x3008A0, "rcx": 0xE000, "rdx": 1,
       "r8": 0, "r9": 1,
       "check": lambda s: s["rets"][0] == "0x0" and
                          "famd" in [t[0] for t in s["trace"]]})
    # fam3 entry: count 0x51 -> idx (id&0xFFF) must be <= 0x50
    A({"name": "ir2-fam3-oob", "entry": 0x3008A0, "rcx": 0x3051, "rdx": 1,
       "r8": 0, "r9": 1,
       "check": lambda s: s["rets"][0] == "0xffffffff"})
    A({"name": "ir2-fam3-hit", "entry": 0x3008A0, "rcx": 0x3005, "rdx": 1,
       "r8": 0, "r9": 1,
       "check": lambda s: "famh3" in [t[0] for t in s["trace"]] or
                          "famd" in [t[0] for t in s["trace"]]})

    # --- REPAIR CONTROL: 0030C0E0 -> 0020E600 -> action-row byte 6 ---------------
    # (ASTRA-REQ-ORACLE-EXP091-RESOLVER-BASE-CONTROL-1003; SWE2-ORACLE)
    # Smallest roster that reaches 0030C196 call 0x20e600: unit0 is valid
    # ([0]&0x10, stats rec0 with clean 0x80000003 masks, +0x6B6==0), its
    # +0x710 resolves through 0031B7E0 to unit1 whose stats byte+5 == 0
    # (party kind 0), and unit0 +0x714 = TV_AID <= 0x21E. Descriptor COBJ
    # {+8 stride 8, +0xC rva ROWBUF-HEAP}; [01F83530]=HEAP makes 0020E600
    # return ROWBUF, so row = ROWBUF + TV_AID*8 and 0030C1C6 tests row+6.
    # -set : only byte 6 of that row is nonzero         -> returns 1
    # -zero: every row byte is 0xFF EXCEPT that byte 6  -> returns 0
    # so the return value depends on exactly row byte 6. unit1's own +0x710
    # is 0, so in -zero the loop's second iteration exits at 0031B7E0.
    TV_AID = 0x10
    TV_ROW6 = ROWBUF + TV_AID * 8 + 6
    def tv_fixture(row6):
        recs = [stats_rec() for _ in range(0x28)]
        recs[0] = stats_rec(idv=3, kind=0)      # roster unit stats
        recs[1] = stats_rec(idv=9, kind=0)      # target: party kind 0
        rows = bytearray((0 if row6 else 0xFF) for _ in range(0x21F * 8))
        rows[TV_AID * 8 + 6] = row6
        return {"entry": 0x30C0E0, "rcx": 0xBAD0BAD0,   # rcx is ignored
                "ucount": 2, "objd_count": 0x20,
                "units_l": [unit(stats=rec_addr(0), b710=(2 << 16) | 1,
                                 b714=TV_AID),
                            unit(stats=rec_addr(1))],
                "recs": recs, "idxt": {2: idxt_e(2, 2)}, "pgate": 0x10,
                "fill": listw(2, [0, 0], f30=[0, unit_addr(1)]),
                "rowbytes": bytes(rows), "rowwatch": True}
    def tv_check(want):
        def chk(s):
            img = [t for t in s["trace"] if t[0] == "imgadd"]
            return (s["rets"][0] == hex(want) and
                    len(img) == 2 and
                    all(t[1] == "rcx=%x" % (ROWBUF - HEAP) for t in img) and
                    s["imgret"] == [hex(ROWBUF)] * 2 and
                    s["row6"][:1] == [[hex(TV_ROW6), "%02x" % (want and 1)]])
        return chk
    A(dict(tv_fixture(1), name="tv-row6-set", check=tv_check(1)))
    A(dict(tv_fixture(0), name="tv-row6-zero", check=tv_check(0)))

    # --- mutants ------------------------------------------------------------------
    M = []
    def mut(name, va, data, probe):
        M.append({"name": name, "patch": [(va, data)], "probe": probe})
    mut("mut-append-20->1f",   0x316CD6, b"\x1f", "app-edge")
    # 30C9A1 cmp cl,0x1f is the actual unlink gate (30C983 only selects rbx)
    mut("mut-unlink-1f->1e",   0x30C9A3, b"\x1e", "unlink-last")
    mut("mut-idr-nib5->4",     0x3588E1, b"\x04", "idr-nib4")
    mut("mut-pgate-10->20",    0x31B7EA, b"\x20", "res-hit")
    mut("mut-fact5->4",        0x30AB96, b"\x04", "rel-fa4")
    # 3105E9 is a 6-byte 0F 84 JE; patch the opcode byte at +1
    mut("mut-canc-je->jne",    0x3105EA, b"\x85", "canc-noblk")
    mut("mut-band1-21e->21d",  0x30F79A, dw(0x21D), "com-b1-edge")
    mut("mut-band2-166->165",  0x30F7E5, dw(0x165), "com-b2-hi")
    mut("mut-notify-mask-3->2", 0x313B68, dw(0x80000002), "ntf-suppress")
    # 2ED2E1 cmp dword[rcx+0x284],0: imm sits at +3
    mut("mut-ed2-284->285",    0x2ED2E4, dw(0x285), "ed-full")

    return C, M

# NEGATIVE CONTROL for the repair: the tv-row6-* fixture with the base planted
# at the OLD wrong cell. "detected" means the probe's positive check refused
# the run (or it faulted); a positive check that still passes is a FAIL.
BASE_CONTROLS = [
    {"name": "neg-oldbase-tv-row6-set",  "probe": "tv-row6-set",
     "override": {"imgb_addr": G_IMGB_OLD_WRONG}},
    {"name": "neg-oldbase-tv-row6-zero", "probe": "tv-row6-zero",
     "override": {"imgb_addr": G_IMGB_OLD_WRONG}},
]

def run_base_control(bc, by_name, raw, secs, iat_names):
    probe = by_name[bc["probe"]]
    c = dict(probe)
    c.update(bc["override"])
    snap, w = run_case(c, raw, secs, iat_names)
    try:
        passed = probe["check"](snap) and not snap["faults"]
    except Exception:
        passed = False
    snap["name"] = bc["name"]
    snap["probe"] = bc["probe"]
    snap["detected"] = not passed
    return snap

def detail(snap):
    img = [t[1] for t in snap["trace"] if t[0] == "imgadd"]
    return ("    detail %s: ret=%s imgadd=%d %s imgret=%s row6=%s faults=%s" %
            (snap["name"], snap["rets"][0], len(img), img,
             snap.get("imgret"), snap.get("row6"), snap["faults"]))

def main():
    raw, secs, iat_names = load_image()
    cases, mutants = build_cases()
    by_name = {c["name"]: c for c in cases}
    results, npass = [], 0
    for c in cases:
        snap, w = run_case(c, raw, secs, iat_names)
        snap["name"] = c["name"]
        results.append(snap)
        try:
            ok = c["check"](snap) and \
                 (c.get("expect_fault") or not snap["faults"])
        except Exception as e:
            ok = False
            snap["check_error"] = str(e)
        npass += ok
        expect(c["name"], snap, ok, repr(snap)[:400])
    print("%d/%d cases" % (npass, len(cases)))
    ndet = 0
    for m in mutants:
        probe = by_name[m["probe"]]
        c = dict(probe)
        c["patch"] = list(c.get("patch", [])) + m["patch"]
        snap, w = run_case(c, raw, secs, iat_names)
        try:
            detected = not probe["check"](snap)
        except Exception:
            detected = True
        ndet += detected
        snap["name"] = m["name"]
        snap["detected"] = detected
        snap["probe"] = m["probe"]
        results.append(snap)
        expect(m["name"], snap, detected, repr(snap)[:300])
    print("%d/%d mutants detected" % (ndet, len(mutants)))
    nbc = 0
    for bc in BASE_CONTROLS:
        snap = run_base_control(bc, by_name, raw, secs, iat_names)
        results.append(snap)
        nbc += snap["detected"]
        expect(bc["name"], snap, snap["detected"], repr(snap)[:300])
    print("%d/%d base controls detected" % (nbc, len(BASE_CONTROLS)))
    out = {"exe_sha256": SHA, "image_base": hex(BASE),
           "cases": npass, "cases_total": len(cases),
           "mutants_detected": ndet, "mutants_total": len(mutants),
           "base_controls_detected": nbc,
           "base_controls_total": len(BASE_CONTROLS),
           "results": results}
    open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "result_repaired.json"), "w").write(json.dumps(out, indent=1))
    return (npass == len(cases) and ndet == len(mutants) and
            nbc == len(BASE_CONTROLS))

def main_only(names):
    """Run only the named cases and base controls (impacted-case re-run)."""
    raw, secs, iat_names = load_image()
    cases, mutants = build_cases()
    by_name = {c["name"]: c for c in cases}
    bcs = {b["name"]: b for b in BASE_CONTROLS}
    unknown = [n for n in names if n not in by_name and n not in bcs]
    if unknown:
        print("UNKNOWN case names: %s" % unknown)
        return False
    results, nok = [], 0
    for n in names:
        if n in by_name:
            c = by_name[n]
            snap, w = run_case(c, raw, secs, iat_names)
            snap["name"] = n
            try:
                ok = c["check"](snap) and \
                     (c.get("expect_fault") or not snap["faults"])
            except Exception as e:
                ok = False
                snap["check_error"] = str(e)
            expect(n, snap, ok, repr(snap)[:400])
        else:
            snap = run_base_control(bcs[n], by_name, raw, secs, iat_names)
            ok = snap["detected"]
            expect(n + " (old-base run refused by the positive check)",
                   snap, ok, "positive check PASSED on the wrong base: " +
                   repr(snap)[:300])
        print(detail(snap))
        results.append(snap)
        nok += ok
    print("%d/%d selected" % (nok, len(names)))
    out = {"exe_sha256": SHA, "image_base": hex(BASE), "selected": names,
           "ok": nok, "total": len(names), "results": results}
    open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "result_repaired_only.json"), "w").write(
        json.dumps(out, indent=1))
    return nok == len(names)

def run_case(case, raw, secs, iat_names):
    w = build(case, raw, secs, iat_names)
    rets = []
    for ph in case.get("phases", [{}]):
        rets.append(invoke(w, ph.get("entry", case.get("entry")),
                           rcx=ph.get("rcx", case.get("rcx", 0)),
                           rdx=ph.get("rdx", case.get("rdx", 0)),
                           r8=ph.get("r8", case.get("r8", 0)),
                           r9=ph.get("r9", case.get("r9", 0)),
                           stack=ph.get("stack", case.get("stack", ()))))
    gm = w.gm
    snap = {
        "rets": [hex(r & 0xFFFFFFFF) for r in rets],
        "rets64": [hex(r & 0xFFFFFFFFFFFFFFFF) for r in rets],
        "trace": [list(t) if isinstance(t, tuple) else t for t in w.trace],
        "faults": [list(f) if isinstance(f, tuple) else f for f in w.faults],
        "mem": [[hex(a), gm.r(a, n).hex()] for a, n in
                case.get("memprobe", [])],
    }
    if case.get("rowwatch"):
        snap["imgret"] = list(w.imgret)
        snap["row6"] = list(w.row6)
    return snap, w

if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--only":
        sys.exit(0 if main_only(sys.argv[2].split(",")) else 1)
    elif len(sys.argv) > 1:
        raw, secs, iat_names = load_image()
        cases, mutants = build_cases()
        for c in cases:
            if c["name"] == sys.argv[1]:
                snap, w = run_case(c, raw, secs, iat_names)
                print(repr(snap))
                break
    else:
        sys.exit(0 if main() else 1)
