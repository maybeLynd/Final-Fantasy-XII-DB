# EXP-128 — exp109-poll-pump-exec
# Executes EXP-121's last two scripted boundaries — the queue poll-pump
# layer — end to end, plus the whole EXP-126 free path they reach:
#   E070 0032E070 (~620B): the task pump — loops on the active-task
#     global q[0x22C51C0], dispatches b[+0x20]-1 via a 6-entry jump
#     table at 0x22E2D0: S1 submit (init gate 3EADD0 scripted; d[+0x28]
#     count==0 -> E330+EC40 retire; b[+0x21]!=0xFF -> 46E030 submit-A
#     scripted / ==0xFF -> 2DF6C0 submit-B scripted; success stamps
#     q[+8]=tick, state=2); S2 timestamp (E810 x2: q[0]+=t,q[+8]=t,
#     state=3); S3/4 FLAG gate (real 0046DFE0; nonzero -> teardown) —
#     S4 optional q[+0x48] completion callback + EC40 retire, S3 poll
#     46E0E0 -> b[+0x20]=5+(d[FLAGG]<0); S5/6 b[+0x22] switch (0->
#     E330/E370 retire by state==5; 1-> b[+0x23]==2 requeue arm /
#     state==6 -> E370 retire / else progress arm); progress arm
#     accrues d[+0x2c]/q[+0x38], E3B0 progress callback, al==1 ->
#     d[+0x28]=min(d[+0x30],d[+0x34]), round d[+0x2c] to 0x800 with
#     +0x7ff bias, q[0]=0, state=1; exhausted d[+0x34] -> E330+EC40.
#     Teardown: 46DD50/16D6A0/3E9780/16D6A0/36FD50->(3BB790) scripted.
#   EA30 0035EA30 (5B): thunk — edx=0; jmp EB70.
#   EB70 0035EB70 (~0x101B): tick pacer — d[0x22D7FB0] (368C70 leaf)
#     vs 862090 tick (scripted): equal -> resync arm rewrites the
#     pacer dword cluster 0x22CA5C4..0x22CA628 (17D3E0 gate, 3691B0/
#     369190, 35E7A0 scripted); else spin on q[0x22CA5E0] until it
#     advances >= max(ecx,1), ret elapsed.
#   E330 0032E330 (61B) / E370 0032E370 (62B): retire helpers —
#     optional q[+0x40] callback (d[+0x60], q[+0x70], r8d=1 / gated
#     additionally on d[+0x28]==-1, r8d=0); b[+0x21]==0xFF -> tail
#     3697F0(sx32(d[+0x24])) -> real PREL free-if-nonnull.
#   E3B0 0032E3B0 (48B): progress callback q[+0x50](task); result
#     outside {1,2,3} -> real 8620C0 yield (tail into 16D6A0 ret-0).
#   EC40 0032EC40 (~148B): list splice — unlink task from the
#     +0x10/+0x18 list headed by q[0x22C51C8] (tail q[0x22C51C0]),
#     push onto q[0x22C51D0]'s idle list, d[+0x64]=-1, tail 16D6A0.
#   E810 0035E810 (8B): ret q[0x22CA5E0] tick leaf.
#   368C70 (7B) ret d[0x22D7FB0], 46E0E0 (7B) ret d[0x215EFF4],
#   16D6A0 (4B) ret-0, 8620C0 (10B) noop-tail — all real leaves.
#   3697F0 (12B) real PREL thunk -> EXP-126 PREL + full tree real.
#   Scripted boundaries (entry-intercepted): 3EADD0 init gate,
#   46E030/2DF780 submit-A pair, 2DF6C0 submit-B, 46DD50 + 3E9780 +
#   36FD50 + 3BB790 teardown externals, 862090 cell-jump tick source,
#   17D3E0/3691B0/369190/35E7A0 resync externals. Data-driven callback
#   slots q[+0x40]/q[+0x48]/q[+0x50] planted to observable trampolines.
#
# EXP-126 header below retained — the free path is re-executed here
# through E330/E370's tail-jmp into PREL.
#   PREL 00369860 (1008B): free(party ptr) — test rcx,rcx -> ret; _chkstk
#     0x1168 frame + GS cookie; r14b&3 misalign -> emit("might be
#     MHANDLE") + ret emit-residual; rbx = payload-0x40; w[rbx]!=0xFF12
#     -> 0xB0-byte header dump + 0xD0-byte aux dump (per-byte emit
#     "%02x ", \n every 16, "\nSTACK\n" tail) + final emit
#     "CannotFreeIlligalAdrs" + d[0x22D89BD]=kind + A570(kind,0xB,-1) +
#     hook(1) + int3; w[+0x3E]!=0 -> emit "MCB Broken" + same abort;
#     !(f14&1) -> emit "Allready Free" + ret emit-residual (NO crash);
#     else: desc=DTAB+b[+3]*0xA8 (kind>0xE -> desc=0 -> b[2] write
#     faults); b[desc+2]=1; f14&=~1; b[+2]=0xFF; d[desc+0x68+tag*4]-=key;
#     b[+0x17]!=0 -> d[0x22D8E10+b17*4]-=key; b[+0x34]=0; w[+0x1E]=0;
#     b[+0x17]=0; d[+0x30]=C620(0); w[+0x3E]=0; splice-in:
#     phys-prev free -> B670 splice-after; elif phys-next free ->
#     B730 splice-before; else rbx<q[desc+0x18] -> AE00 (find-below)
#     then ACE0 (find-above) fallback + B730-before / B670-after,
#     skip when found == stale d[+4]/d[+8] link; rbx>=bound -> ACE0
#     first then AE00; then B210 coalesce + B5F0 page-head insert.
#   AE00 0036AE00 (286B): find free block at-or-below node — pslot of
#     phys-prev via signed-16 floor, bitmap guard-mask scan, head-table
#     walk down, list-1 +8 walk while next<=node.
#   ACE0 0036ACE0 (285B): mirror — phys-next slot, forward bitmap scan
#     bounded by d[desc+0x58], head-table walk up, +4 walk while
#     prev>=node.
#   F17D2E0 0017D2E0 (91B): emit wrapper — GETOBJ 0016D670 (real 8B
#     leaf: returns &q[0x2E39ED0] BSS obj) -> hook(q[obj]|1, buf, -1,
#     fmt) via cell q[0x8C2F08] (ships rdata 0x1CCECB4 -> planted FLAG);
#     ret = flag residual (cmovs eax,-1 arm is dead: ret never <0).
#   CHKSTK 00808F10 (80B): _chkstk — probes pages from gs:[0x10] limit
#     down to new top; fixture plants a TEB page at GS base.
#   PINIT 004746F0 (26B): memcpy wrapper — movsxd r8,r8d; call thunk
#     00861EBA (real jmp qword[rip] -> IAT cell 0x8C2A68 =
#     VCRUNTIME140!memcpy in the shipped image; cell planted to a
#     fixture trampoline intercepted as the disclosed external-import
#     boundary); returns dst.
#   A2A0 cases rerun with PREL+PINIT real inside (integration).
#   BC60/BASE/C620/CHKCK/FLAG + BST helpers real (EXP-123/125 models).
#   ERRATUM vs EXP-123: q[0x8C2D80] ships 0x1CCF02C (rdata), not 0 —
#   same dormant-hook family as q[0x8C2F08]/q[0x8C2F70]; the planted
#   FLAG decision was and stays correct (calling rdata would fault).
#
# Fixture disclosure: all BSS globals + desc fields (+0x10 pool base,
#   +0x18 search bound, +0x20 bitmap, +0x28 page heads, +0x30 idx-table
#   base, +0x40/+0x48 idx chains, +0x50 BST root, +0x58 slot bound,
#   +0x60 seq, +0x68 use, +0x90/+0x98 free roots, b[+1] kind) planted;
#   pool + free headers fixture. CODEC=0 -> links raw u32 (the
#   EXP-083-proven valid configuration). Model reads fall back to
#   shipped image bytes where unplanted.


import ctypes, hashlib, json, struct
from unicorn import Uc
from unicorn.x86_const import (
    UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_R9,
    UC_X86_REG_RAX, UC_X86_REG_RIP, UC_X86_REG_RSP,
    UC_X86_REG_GS_BASE)
from unicorn import (UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE,
                     UC_HOOK_MEM_UNMAPPED, UC_HOOK_INTR,
                     UC_PROT_ALL, UcError)

EXE = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe"
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"

IMG_LO = 0x120000
IMG_HI = 0x30A0000
HEAP   = 0x40000000
POOL   = 0x30000000
STACK  = 0x61000000
RETQ   = 0x62000000

AAD0 = 0x0036AAD0
ABE0 = 0x0036ABE0
A2A0 = 0x0036A2A0
C790 = 0x0036C790
B410 = 0x0036B410
B490 = 0x0036B490
B4E0 = 0x0036B4E0
B5A0 = 0x0036B5A0     # +0x28 twin of B490 (right-child attach)
A570 = 0x0036A570
A850 = 0x0036A850
BC60 = 0x0036BC60
A490 = 0x0036A490
B210 = 0x0036B210
B2C0 = 0x0036B2C0
B5F0 = 0x0036B5F0
B670 = 0x0036B670
B730 = 0x0036B730
B7F0 = 0x0036B7F0
B8B0 = 0x0036B8B0
C900 = 0x0036C900
C9D0 = 0x0036C9D0
BASE = 0x0020E600
C620 = 0x0020E620
FLAG = 0x0046DFE0     # real leaf - planted output-cell target
CHKCK = 0x00808C40    # __security_check_cookie - real

PREL  = 0x00369860    # REAL: the free/release path (1008B)
AE00  = 0x0036AE00    # REAL: find free block at-or-below node
ACE0  = 0x0036ACE0    # REAL: find free block at-or-above node
EMIT  = 0x0017D2E0    # REAL: diagnostic emit wrapper
GETOBJ= 0x0016D670    # REAL: output-object getter leaf
CHKSTK= 0x00808F10    # REAL: _chkstk stack probe
PINIT = 0x004746F0    # REAL: memcpy wrapper (returns dst)
THUNK = 0x00861EBA    # REAL: jmp qword[rip] IAT thunk -> 0x8C2A68
MEMCPY= 0x63000000    # fixture trampoline: disclosed import boundary
TEB   = 0x6F000000    # fake TEB page for GS base (_chkstk gs:[0x10])
OUTC  = 0x8C2F70      # q: A570 output-hook cell (ships rdata 0x1CCEF16)
EMITC = 0x8C2F08      # q: F17D2E0 emit cell (ships rdata 0x1CCECB4)
IATC  = 0x8C2A68      # q: memcpy IAT cell (VCRUNTIME140!memcpy)
EMITO = 0x2E39ED0     # q: emit output-object global (BSS, ships 0)
CELLP = 0x8C2D80      # q: shared hook cell (ships rdata 0x1CCF02C)
SPIN_BC60 = 0x36BC87
INT3 = {B670: 0x36B6AE, B730: 0x36B76E,
        B7F0: 0x36B82E, B8B0: 0x36B8EE}
# PREL's own int3 sites (entry-keyed dict cannot hold two per body):
PREL_I3_MAGIC = 0x369A7F   # after hook(1) on the magic-mismatch abort
PREL_I3_MARK  = 0x369ABD   # after hook(1) on the w[+0x3E] abort
# return addresses seen at the planted FLAG cell classify the call:
EMIT_RET = 0x17D32E   # inside F17D2E0 (call site 0x17D328 +6)
OUT_RET  = 0x36A700   # inside A570 (call site 0x36A6FA +6)
CELL_RETS = {0x369A7F, 0x369ABD,  # PREL's two hook(1) + int3 sites
             0x36B6AE, 0x36B76E, 0x36B82E, 0x36B8EE}
# PREL format strings (shipped rdata)
F_MHAND = 0xD10E30    # "%p might be MHANDLE from %p"
F_HEX   = 0xD10E4C    # "%02x "
F_ILL   = 0xD10E60    # "CannotFreeIlligalAdrs %p from %p\n%s"
F_MCB   = 0xD10E88    # "TkFreeMain:MCB Broken:from %p\n"
F_FREE  = 0xD10EA8    # "TkFreeMain:Allready Free:%p from %p"
PREL_RSP = 0x6107EE88  # rsp at prel's cookie xor (frame 0x1168)

# ---- EXP-128 pump bodies ----
E070  = 0x0032E070    # REAL: task pump (six-arm state machine)
EA30  = 0x0035EA30    # REAL: thunk edx=0 -> EB70
EB70  = 0x0035EB70    # REAL: tick pacer (wait spin + resync arm)
E330  = 0x0032E330    # REAL: retire helper (cb + 3697F0 tail)
E370  = 0x0032E370    # REAL: retire helper (gated cb + 3697F0 tail)
E3B0  = 0x0032E3B0    # REAL: progress-callback wrapper
EC40  = 0x0032EC40    # REAL: task-list unlink + idle push
E810  = 0x0035E810    # REAL: tick getter leaf
G8C70 = 0x00368C70    # REAL: ret d[0x22D7FB0] leaf
GE0E0 = 0x0046E0E0    # REAL: ret d[0x215EFF4] leaf
G6A0  = 0x0016D6A0    # REAL: ret-0 leaf
G20C0 = 0x008620C0    # REAL: noop yield (tail -> 16D6A0)
G97F0 = 0x003697F0    # REAL: PREL thunk (free-if-nonnull)
XADD0 = 0x003EADD0    # scripted: init gate (eax)
X46E0 = 0x0046E030    # scripted: submit-A shim -> 2DF780 (ret 1)
X2DF6 = 0x002DF6C0    # scripted: submit-B (eax gate)
XDD50 = 0x0046DD50    # scripted: teardown pump
X9780 = 0x003E9780    # scripted: teardown pump
XFD50 = 0x0036FD50    # scripted: teardown gate (eax)
XBB79 = 0x003BB790    # scripted: conditional teardown tail
X2090 = 0x00862090    # scripted: cell-jump tick source (rax)
X17D3 = 0x0017D3E0    # scripted: resync gate (eax)
X91B0 = 0x003691B0    # scripted: resync helper
X9190 = 0x00369190    # scripted: resync helper
X5E7A = 0x0035E7A0    # scripted: resync value source (eax)
CB40  = 0x63010000    # fixture trampoline: task q[+0x40] callback
CB48  = 0x63020000    # fixture trampoline: task q[+0x48] callback
CB50  = 0x63030000    # fixture trampoline: task q[+0x50] callback
TASKG = 0x22C51C0     # q: active-task head (E070 loop + EC40 tail cell)
TASKH = 0x22C51C8     # q: active-list head cell
TASKI = 0x22C51D0     # q: idle-list head cell
TICKQ = 0x22CA5E0     # q: the tick global (E810/EB70)
TICKD = 0x22D7FB0     # d: secondary tick dword (368C70)
PACC  = 0x22CA5C4     # d: pacer-state cluster base (EB70 resync)
SPIN_EB70 = 0x35EBB0  # EB70's spin head — hook bumps TICKQ per visit
JTAB  = 0x32E2D0      # E070's six-entry jump-offset table (rdata)

MASKG  = 0x22D89B8
ST_W   = 0x22D89BC
QCOUNT = 0x22D89C0
TAGEP  = 0x22D8E1C
ST_B3  = 0x22D8E28
PTAGC  = 0x22D8E10    # d[] per-tag pool counters (A2A0 bumps)
CODEC  = 0x1F83530
DTAB   = 0x22D7FD0
FLAGG  = 0x215EFF4    # FLAG leaf's state cell
GSCOOK = 0x2B992DDFA232   # q[0x1F44830] shipped value
A2A0_RSP = 0x6107FF58     # rsp at a2a0's cookie xor (frame 0xA8)
A850_RSP = 0x6107FD98     # rsp at a850's cookie xor (frame 0x268)

PAGETAB = HEAP + 0x20000
BITMAP  = HEAP + 0x28000
ITAB   = HEAP + 0x40000        # 16B-entry index table for desc+0x30
NP = POOL + 0x800
N1 = POOL + 0x1000
N2 = POOL + 0x2000
N3 = POOL + 0x14000
N3B = POOL + 0x18000
N4 = POOL + 0x24000
P0 = POOL              # pool blocks physically start at arena base
P1 = POOL + 0x40000
P2 = POOL + 0x80000
P3 = POOL + 0xC0000
# EXP-128 task records live in HEAP (0x78B each)
T1 = HEAP + 0x60000
T2 = HEAP + 0x61000
T3 = HEAP + 0x62000
T4 = HEAP + 0x63000
P4 = POOL + 0x100000
DESCK = 2


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


def img_byte(raw, secs, va):
    try:
        return img_rd(raw, secs, va, 1)[0]
    except KeyError:
        return 0


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
    """bytes/plants shared by native World and python model.
    CODEC=0 -> encoded links are raw u32 pointers."""
    W = []
    W.append((MASKG, dw(case.get("mask", 0))))
    W.append((QCOUNT, dw(case.get("qcount", 1))))
    W.append((TAGEP, dw(case.get("tagep", 0))))
    W.append((ST_B3, dw(case.get("stb3", 0))))
    W.append((ST_W, dw(case.get("stw", 0))))
    W.append((CODEC, qw(case.get("codec", 0))))
    W.append((CELLP, qw(case.get("cell", FLAG))))
    W.append((OUTC, qw(case.get("outc", FLAG))))
    W.append((EMITC, qw(case.get("emitc", FLAG))))
    W.append((IATC, qw(case.get("iatc", MEMCPY))))
    W.append((FLAGG, dw(case.get("flagg", 5))))
    W.append((TEB + 0x10, qw(case.get("teblim", 0))))
    if "emitobj" in case:
        W.append((EMITO, qw(case["emitobj"])))
    # ---- EXP-128 pump globals ----
    W.append((TASKG, qw(case.get("taskg", 0))))
    W.append((TASKH, qw(case.get("taskh", 0))))
    W.append((TASKI, qw(case.get("taski", 0))))
    W.append((TICKQ, qw(case.get("tickq", 0))))
    W.append((TICKD, dw(case.get("tickd", 0))))
    for off, v in case.get("pacc", {}).items():
        W.append((PACC + off, dw(v)))
    for t, v in case.get("ptagc", {}).items():
        W.append((PTAGC + t * 4, dw(v)))
    # descriptors
    for k, d in case.get("desc", {}).items():
        b = DTAB + k * 0xA8
        if "kind" in d: W.append((b + 1, bytes([d["kind"]])))
        if "pool" in d: W.append((b + 0x10, qw(d["pool"])))
        if "lim" in d:  W.append((b + 0x18, qw(d["lim"])))
        if "bmap" in d: W.append((b + 0x20, qw(d["bmap"])))
        if "ptab" in d: W.append((b + 0x28, qw(d["ptab"])))
        if "itab" in d: W.append((b + 0x30, qw(d["itab"])))
        if "chA" in d:  W.append((b + 0x48, qw(d["chA"])))
        if "chB" in d:  W.append((b + 0x40, qw(d["chB"])))
        if "bst" in d:  W.append((b + 0x50, qw(d["bst"])))
        if "bmax" in d: W.append((b + 0x58, dw(d["bmax"])))
        if "seq" in d:  W.append((b + 0x60, ww(d["seq"])))
        if "head" in d: W.append((b + 0x90, qw(d["head"])))
        if "tail" in d: W.append((b + 0x98, qw(d["tail"])))
        if "use" in d:
            for t, v in d["use"].items():
                W.append((b + 0x68 + t * 4, dw(v)))
    for s, v in case.get("ptab", {}).items():
        W.append((PAGETAB + s * 8, qw(v)))
    for s, v in case.get("bmap", {}).items():
        W.append((BITMAP + s * 4, dw(v)))
    # 16B index-table entries: w[+0] next-idx, q[+8] payload
    for i, e in case.get("itab", {}).items():
        W.append((ITAB + i * 0x10, ww(e.get("n", 0))))
        W.append((ITAB + i * 0x10 + 8, qw(e.get("p", 1))))
    # block headers (0x40): free + pool layouts share the header;
    # CODEC=0 -> encoded fields are raw u32 pointers
    for a, n in case.get("nodes", {}).items():
        hdr = bytearray(0x40)
        struct.pack_into("<H", hdr, 0x00, n.get("magic", 0xFF12))
        hdr[0x02] = n.get("b2", 0xFF)
        hdr[0x03] = n.get("kind", DESCK)
        struct.pack_into("<I", hdr, 0x04, n.get("prev", 0) & 0xFFFFFFFF)
        if "w6" in n:   # +6 overlaps prev's high word (pool-chain seq)
            struct.pack_into("<H", hdr, 0x06, n["w6"])
        struct.pack_into("<I", hdr, 0x08, n.get("next", 0) & 0xFFFFFFFF)
        struct.pack_into("<I", hdr, 0x0C, n.get("pprev", 0) & 0xFFFFFFFF)
        struct.pack_into("<I", hdr, 0x10, n.get("pnext", 0) & 0xFFFFFFFF)
        struct.pack_into("<H", hdr, 0x14, n.get("f14", 0))
        hdr[0x15] = n.get("f15", 0)
        hdr[0x16] = n.get("tag", 0)
        hdr[0x17] = n.get("t17", 0)
        struct.pack_into("<I", hdr, 0x18, n.get("key", 0) & 0xFFFFFFFF)
        struct.pack_into("<H", hdr, 0x1C, n.get("seq", 0))
        struct.pack_into("<H", hdr, 0x1E, n.get("w1e", 0))
        struct.pack_into("<I", hdr, 0x20, n.get("l20", 0) & 0xFFFFFFFF)
        struct.pack_into("<I", hdr, 0x24, n.get("left", 0) & 0xFFFFFFFF)
        struct.pack_into("<I", hdr, 0x28, n.get("right", 0) & 0xFFFFFFFF)
        struct.pack_into("<I", hdr, 0x2C, n.get("parent", 0) & 0xFFFFFFFF)
        struct.pack_into("<I", hdr, 0x30, n.get("d30", 0) & 0xFFFFFFFF)
        lbl = n.get("label", b"")
        hdr[0x34:0x34 + len(lbl)] = lbl[:0xC]
        struct.pack_into("<H", hdr, 0x3E, n.get("w3e", 0))
        W.append((a, bytes(hdr)))
        if len(lbl) > 0xC:   # long labels spill past the header
            W.append((a + 0x40, lbl[0xC:]))
    # ---- EXP-128 task objects (0x78 bytes): queue-pump task record ----
    for a, t in case.get("tasks", {}).items():
        rec = bytearray(0x78)
        struct.pack_into("<Q", rec, 0x00, t.get("acc", 0))
        struct.pack_into("<Q", rec, 0x08, t.get("t8", 0))
        struct.pack_into("<Q", rec, 0x10, t.get("prev", 0))
        struct.pack_into("<Q", rec, 0x18, t.get("next", 0))
        rec[0x20] = t.get("state", 0)
        rec[0x21] = t.get("b21", 0)
        rec[0x22] = t.get("b22", 0)
        rec[0x23] = t.get("b23", 0)
        struct.pack_into("<i", rec, 0x24, t.get("d24", 0))
        struct.pack_into("<i", rec, 0x28, t.get("d28", 0))
        struct.pack_into("<i", rec, 0x2C, t.get("d2c", 0))
        struct.pack_into("<i", rec, 0x30, t.get("d30", 0))
        struct.pack_into("<i", rec, 0x34, t.get("d34", 0))
        struct.pack_into("<Q", rec, 0x38, t.get("q38", 0))
        struct.pack_into("<Q", rec, 0x40, t.get("cb40", 0))
        struct.pack_into("<Q", rec, 0x48, t.get("cb48", 0))
        struct.pack_into("<Q", rec, 0x50, t.get("cb50", 0))
        struct.pack_into("<I", rec, 0x60, t.get("d60", 0))
        struct.pack_into("<I", rec, 0x64, t.get("d64", 0))
        struct.pack_into("<Q", rec, 0x70, t.get("q70", 0))
        W.append((a, bytes(rec)))
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
        gm.map(POOL, 0x200000)
        gm.map(STACK, 0x100000)
        gm.map(RETQ, 0x1000)
        gm.map(TEB, 0x1000)
        gm.map(MEMCPY, 0x1000, b"\xc3" * 0x1000)
        gm.map(CB40, 0x1000, b"\xc3" * 0x1000)
        gm.map(CB48, 0x1000, b"\xc3" * 0x1000)
        gm.map(CB50, 0x1000, b"\xc3" * 0x1000)
        self.uc.reg_write(UC_X86_REG_GS_BASE, TEB)
        for addr, dat in build_fixture(case):
            gm.w(addr, dat)
        for addr, dat in case.get("patch_bytes", []):
            gm.w(addr, dat)
        self.trace, self.faults, self.rets, self.ends = [], [], [], []
        self.xctr = {}
        self.uc.hook_add(UC_HOOK_CODE, self.on_code)
        self.uc.hook_add(UC_HOOK_MEM_UNMAPPED, self.on_bad)
        self.uc.hook_add(UC_HOOK_INTR, self.on_intr)

    def _xval(self, key, default=0):
        """scripted-boundary return plant; a list value is consumed
        in call order so multi-pass cases can sequence gates."""
        v = self.case.get(key, default)
        if isinstance(v, list):
            i = min(self.xctr.get(key, 0), len(v) - 1)
            self.xctr[key] = self.xctr.get(key, 0) + 1
            return v[i]
        return v

    def _ret(self, uc):
        uc.reg_write(UC_X86_REG_RIP, self.gm.qw(uc.reg_read(UC_X86_REG_RSP)))
        uc.reg_write(UC_X86_REG_RSP, uc.reg_read(UC_X86_REG_RSP) + 8)

    def on_intr(self, uc, intno, _):
        self.faults.append(("trap", uc.reg_read(UC_X86_REG_RIP)))
        uc.emu_stop()

    def on_code(self, uc, addr, size, _):
        if addr == SPIN_EB70:
            # EB70's wait spin re-reads the tick global each pass; the
            # fixture advances it one tick per visit so the loop exits
            # after max(ecx,1) iterations (model does the same).
            self.gm.w(TICKQ, qw(self.gm.qw(TICKQ) + 1))
        elif addr == XADD0:
            self.trace.append("xadd0")
            uc.reg_write(UC_X86_REG_RAX, self._xval("xadd0", 0))
            self._ret(uc)
        elif addr == X46E0:
            self.trace.append("x46e0:%x:%x:%x:%x:%x" % (
                uc.reg_read(UC_X86_REG_RCX) & 0xFFFFFFFF,
                uc.reg_read(UC_X86_REG_RDX) & 0xFFFFFFFF,
                uc.reg_read(UC_X86_REG_R8) & 0xFFFFFFFF,
                uc.reg_read(UC_X86_REG_R9) & 0xFFFFFFFF,
                self.gm.qw(uc.reg_read(UC_X86_REG_RSP) + 0x28)))
            uc.reg_write(UC_X86_REG_RAX, self._xval("x46e0", 1))
            self._ret(uc)
        elif addr == X2DF6:
            self.trace.append("x2df6:%x:%x:%x" % (
                uc.reg_read(UC_X86_REG_RCX) & 0xFFFFFFFFFFFFFFFF,
                uc.reg_read(UC_X86_REG_RDX) & 0xFFFFFFFFFFFFFFFF,
                uc.reg_read(UC_X86_REG_R9) & 0xFFFFFFFF))
            uc.reg_write(UC_X86_REG_RAX, self._xval("x2df6", 0))
            self._ret(uc)
        elif addr == XDD50:
            self.trace.append("x46dd")
            self._ret(uc)
        elif addr == X9780:
            self.trace.append("x3e97")
            self._ret(uc)
        elif addr == XFD50:
            self.trace.append("x36fd")
            uc.reg_write(UC_X86_REG_RAX, self._xval("x36fd", 0))
            self._ret(uc)
        elif addr == XBB79:
            self.trace.append("x3bb7")
            self._ret(uc)
        elif addr == X2090:
            self.trace.append("xtick")
            uc.reg_write(UC_X86_REG_RAX, self._xval("xtick", 0))
            self._ret(uc)
        elif addr == X17D3:
            self.trace.append("x17d3")
            uc.reg_write(UC_X86_REG_RAX, self._xval("x17d3", 0))
            self._ret(uc)
        elif addr == X91B0:
            self.trace.append("x91b0:%x" % (
                uc.reg_read(UC_X86_REG_RCX) & 0xFFFFFFFF))
            self._ret(uc)
        elif addr == X9190:
            self.trace.append("x9190:%x" % (
                uc.reg_read(UC_X86_REG_RCX) & 0xFFFFFFFF))
            self._ret(uc)
        elif addr == X5E7A:
            self.trace.append("x35e7")
            uc.reg_write(UC_X86_REG_RAX, self._xval("x35e7", 0))
            self._ret(uc)
        elif addr == CB40:
            self.trace.append("cb40:%x:%x:%x" % (
                uc.reg_read(UC_X86_REG_RCX) & 0xFFFFFFFF,
                uc.reg_read(UC_X86_REG_RDX) & 0xFFFFFFFFFFFFFFFF,
                uc.reg_read(UC_X86_REG_R8) & 0xFFFFFFFF))
            uc.reg_write(UC_X86_REG_RAX, self._xval("cb40ret", 0))
            self._ret(uc)
        elif addr == CB48:
            self.trace.append("cb48:%x" % (
                uc.reg_read(UC_X86_REG_RCX) & 0xFFFFFFFF))
            uc.reg_write(UC_X86_REG_RAX, self._xval("cb48ret", 0))
            self._ret(uc)
        elif addr == CB50:
            self.trace.append("cb50:%x" % (
                uc.reg_read(UC_X86_REG_RCX) & 0xFFFFFFFFFFFFFFFF))
            uc.reg_write(UC_X86_REG_RAX, self._xval("cb50ret", 0))
            self._ret(uc)
        elif addr == MEMCPY:
            # disclosed import boundary: VCRUNTIME140!memcpy reached via
            # the real PINIT body + real 00861EBA thunk; the cell is
            # planted to this trampoline so the copy is observable.
            dst = uc.reg_read(UC_X86_REG_RCX)
            src = uc.reg_read(UC_X86_REG_RDX)
            n = uc.reg_read(UC_X86_REG_R8) & 0xFFFFFFFFFFFFFFFF
            self.trace.append("memcpy:%x:%x:%x" % (dst, src, n))
            faddr = None
            i = 0
            while i < n and i < 0x100000:
                try:
                    b = self.gm.r(src + i, 1)
                except KeyError:
                    faddr = src + i
                    break
                try:
                    self.gm.w(dst + i, b)
                except KeyError:
                    faddr = dst + i
                    break
                i += 1
            if faddr is not None:
                self.faults.append((1, faddr, 1))
                uc.emu_stop()
                return
            uc.reg_write(UC_X86_REG_RAX, dst)
            self._ret(uc)
        elif addr == FLAG:
            # planted hook-cell target: real leaf executes; classify
            # the call by return address (which cell dispatched).
            ret = self.gm.qw(uc.reg_read(UC_X86_REG_RSP))
            if ret == EMIT_RET:
                # F17D2E0's hook(obj|1, buf, -1, fmt): r9 = fmt, rdx = buf
                self.trace.append("emit:%x:%x" % (
                    uc.reg_read(UC_X86_REG_R9) & 0xFFFFFFFFFFFFFFFF,
                    uc.reg_read(UC_X86_REG_RDX) & 0xFFFFFFFFFFFFFFFF))
            elif ret in CELL_RETS:
                # PREL/twin corrupt-path hook(1)
                self.trace.append("cell:%x" % (
                    uc.reg_read(UC_X86_REG_RCX) & 0xFF))
            else:
                # A570's out-hook: hook(buf, label, 8)
                self.trace.append("out:%x:%x" % (
                    uc.reg_read(UC_X86_REG_RDX) & 0xFFFFFFFFFFFFFFFF,
                    uc.reg_read(UC_X86_REG_R8) & 0xFFFFFFFF))

    def on_bad(self, uc, access, addr, size, value, _):
        self.faults.append((access, addr, size))
        uc.emu_stop()
        return True

    def run_one(self, entry, rcx, rdx=0, r8=0, r9=0):
        uc = self.uc
        self.gm.w(RETQ, b"\xc3" * 0x100)
        rsp = STACK + 0x80000
        self.gm.w(rsp, qw(RETQ))
        uc.reg_write(UC_X86_REG_RSP, rsp)
        uc.reg_write(UC_X86_REG_RCX, rcx)
        uc.reg_write(UC_X86_REG_RDX, rdx)
        uc.reg_write(UC_X86_REG_R8, r8)
        uc.reg_write(UC_X86_REG_R9, r9)
        try:
            uc.emu_start(entry, RETQ, count=300000)
        except UcError as e:
            if not self.faults:
                self.faults.append(("emuerr", str(e)))
        self.rets.append(uc.reg_read(UC_X86_REG_RAX))
        self.ends.append(uc.reg_read(UC_X86_REG_RIP))

    def run(self):
        for step in self.case.get("steps", []):
            self.run_one(*step)

    def obs(self):
        mem = {}
        for a, n in self.case.get("watch", []):
            mem["%x" % a] = self.gm.r(a, n).hex()
        return {"trace": self.trace, "faults": self.faults,
                "rets": self.rets, "ends": self.ends, "mem": mem}


# ---------------- python model ----------------

def sx32(v):
    v &= 0xFFFFFFFF
    return v - 0x100000000 if v & 0x80000000 else v


class Model:
    def __init__(self, case, raw, secs):
        self.case, self.raw, self.secs = case, raw, secs
        self.mem = {}
        for addr, dat in build_fixture(case):
            for i, b in enumerate(dat):
                self.mem[addr + i] = b
        for addr, dat in case.get("patch_bytes", []):
            for i, b in enumerate(dat):
                self.mem[addr + i] = b
        self.trace, self.faults, self.rets, self.ends = [], [], [], []
        self.trap = None
        self.deep = None     # nested fault tuple from a helper call
        self.vsp = 0x61080000  # virtual rsp at the current entry call
        self.xctr = {}
        self._rdx, self._r8 = 0, 0  # residual regs through scripted calls

    def mb(self, a):
        a &= 0xFFFFFFFFFFFFFFFF
        if a in self.mem:
            return self.mem[a]
        if IMG_LO <= a < IMG_HI:
            return img_byte(self.raw, self.secs, a)
        if self.mapped(a):
            return 0
        return None
    def mw(self, a):
        v0, v1 = self.mb(a), self.mb(a + 1)
        if v0 is None or v1 is None: return None
        return v0 | (v1 << 8)
    def md(self, a):
        r = 0
        for i in range(4):
            v = self.mb(a + i)
            if v is None: return None
            r |= v << (i * 8)
        return r
    def mq(self, a):
        lo, hi = self.md(a), self.md(a + 4)
        if lo is None or hi is None: return None
        return lo | (hi << 32)

    def stb(self, a, v): self.mem[a & 0xFFFFFFFFFFFFFFFF] = v & 0xFF
    def stw(self, a, v):
        self.stb(a, v); self.stb(a + 1, v >> 8)
    def std(self, a, v):
        for i in range(4): self.stb(a + i, v >> (i * 8))
    def stq(self, a, v):
        for i in range(8): self.stb(a + i, v >> (i * 8))

    def mapped(self, a):
        a &= 0xFFFFFFFFFFFFFFFF
        return (IMG_LO <= a < IMG_HI or HEAP <= a < HEAP + 0x1000000
                or POOL <= a < POOL + 0x200000
                or STACK <= a < STACK + 0x100000
                or RETQ <= a < RETQ + 0x1000
                or TEB <= a < TEB + 0x1000
                or MEMCPY <= a < MEMCPY + 0x1000
                or a in self.mem)

    # ---- codec (CODEC planted 0) ----
    def base(self, enc):
        if enc is None: return None
        return ((self.mq(CODEC) or 0) + (enc & 0xFFFFFFFF)) & 0xFFFFFFFFFFFFFFFF
    def c620(self, ptr):
        return (ptr - ((self.mq(CODEC) or 0) & 0xFFFFFFFF)) & 0xFFFFFFFF

    # ---- EXP-123 helper tree (ctx carve path is exercised for real) ----
    def pslot(self, desc, blk):
        d = blk - (self.mq(desc + 0x10) or 0)
        if d < 0:
            d += 0xFFFF
        return d >> 16

    def a490(self, kind, blk, size, seq):
        if not blk: return
        self.stw(blk, 0xFF12)
        self.stb(blk + 3, kind)
        self.stw(blk + 0x1E, 0)
        self.stb(blk + 2, 0xFF)
        self.stw(blk + 0x16, 0)
        for off in (4, 8, 0xC, 0x10):
            self.std(blk + off, self.c620(0))
        self.stw(blk + 0x14, 0)
        b15 = 8 if (self.md(ST_B3) or 0) != 0 else 0
        self.std(blk + 0x18, size)
        self.stb(blk + 0x15, b15)
        self.stw(blk + 0x1C, seq)
        for off in (0x20, 0x24, 0x28, 0x2C, 0x30):
            self.std(blk + off, self.c620(0))
        self.stb(blk + 0x34, 0)
        self.std(blk + 0x3C, 0)

    def c900(self, desc, blk):
        if not blk: return 0
        slot = self.pslot(desc, blk)
        ptab = self.mq(desc + 0x28) or 0
        head = self.mq(ptab + slot * 8)
        if not head or head != blk: return head or 0
        nxt = self.base(self.md(blk + 8))
        nslot = 0xFFFFFFFF
        if nxt:
            nslot = self.pslot(desc, nxt)
        bm = self.mq(desc + 0x20) or 0
        bit = 1 << (slot & 0x1F)
        widx = slot >> 5
        if nxt and nslot == slot:
            self.stq(ptab + slot * 8, nxt)
            self.std(bm + widx * 4, (self.md(bm + widx * 4) or 0) | bit)
        else:
            self.stq(ptab + slot * 8, 0)
            self.std(bm + widx * 4,
                     (self.md(bm + widx * 4) or 0) & ~bit & 0xFFFFFFFF)
        return bm

    def b5f0(self, desc, blk):
        if not blk: return 0
        slot = self.pslot(desc, blk)
        ptab = self.mq(desc + 0x28) or 0
        bm = self.mq(desc + 0x20) or 0
        cur = self.mq(ptab + slot * 8) or 0
        if cur == 0:
            self.stq(ptab + slot * 8, blk)
            self.std(bm + (slot >> 5) * 4,
                     (self.md(bm + (slot >> 5) * 4) or 0)
                     | (1 << (slot & 0x1F)))
            return ptab + slot * 8
        if (cur & 0xFFFFFFFF) > (blk & 0xFFFFFFFF):
            self.stq(ptab + slot * 8, blk)
            self.std(bm + (slot >> 5) * 4,
                     (self.md(bm + (slot >> 5) * 4) or 0)
                     | (1 << (slot & 0x1F)))
            return bm
        return ptab + slot * 8

    def c9d0(self, node, flag):
        if not node: return
        nxt = self.base(self.md(node + 8))
        prv = self.base(self.md(node + 4))
        if nxt:
            self.std(nxt + 4, self.c620(prv)); self.stw(nxt + 0x3E, 0)
        if prv:
            self.std(prv + 8, self.c620(nxt)); self.stw(prv + 0x3E, 0)
        self.std(node + 8, self.c620(0))
        self.std(node + 4, self.c620(0))
        if flag:
            nxt = self.base(self.md(node + 0x10))
            prv = self.base(self.md(node + 0xC))
            if nxt:
                self.std(nxt + 0xC, self.c620(prv))
                self.stw(nxt + 0x3E, 0)
            if prv:
                self.std(prv + 0x10, self.c620(nxt))
                self.stw(prv + 0x3E, 0)
            self.stw(node, 0xFF99)
            self.std(node + 0x10, self.c620(0))
            self.std(node + 0xC, self.c620(0))
        self.stw(node + 0x3E, 0)

    def twin(self, va, anchor, blk):
        if not blk or self.trap or self.deep: return 0
        if (self.mw(blk + 0x3E) or 0) != 0:
            # corrupt path: A570 real (mask-gated), hook(1), int3
            r = self.a570(self.md(ST_W) or 0, 0xB, 0xFFFFFFFF)
            if isinstance(r, tuple) and r[0] != "ret":
                self.deep = r
                return 0
            self.cellhook(1)
            self.trap = INT3[va] + 1
            return 0
        lo, hi = (0xC, 0x10) if va in (B7F0, B8B0) else (4, 8)
        # first write targets anchor+hi (after-twins) or anchor+lo
        woff = hi if va in (B670, B7F0) else lo
        if not self.mapped(anchor + woff):
            self.deep = ("fault", (anchor + woff) & 0xFFFFFFFFFFFFFFFF,
                         va, 0)
            return 0
        if va in (B670, B7F0):
            nxt = self.base(self.md(anchor + hi)) or 0
            self.std(anchor + hi, self.c620(blk))
            self.stw(anchor + 0x3E, 0)
            if nxt:
                self.std(nxt + lo, self.c620(blk))
                self.stw(nxt + 0x3E, 0)
            self.std(blk + lo, self.c620(anchor))
            self.stw(blk + 0x3E, 0)
            self.std(blk + hi, self.c620(nxt))
            return self.c620(nxt) & 0xFFFFFFFFFFFFFFFF
        prv = self.base(self.md(anchor + lo)) or 0
        self.std(anchor + lo, self.c620(blk))
        self.stw(anchor + 0x3E, 0)
        if prv:
            self.std(prv + hi, self.c620(blk))
            self.stw(prv + 0x3E, 0)
        self.std(blk + lo, self.c620(prv))
        self.stw(blk + 0x3E, 0)
        self.std(blk + hi, self.c620(anchor))
        return self.c620(anchor) & 0xFFFFFFFFFFFFFFFF

    def b2c0(self, desc, rdi):
        rbx = self.base(self.md(rdi + 8))
        while rbx and self.base(self.md(rdi + 0x10)) == rbx:
            self.c900(desc, rbx)
            self.c9d0(rbx, 1)
            add = (self.md(rbx + 0x18) or 0) + 0x40
            self.std(rdi + 0x18,
                     ((self.md(rdi + 0x18) or 0) + add) & 0xFFFFFFFF)
            rbx = self.base(self.md(rdi + 8))
        return rdi

    def b210(self, desc, blk):
        rbx = self.base(self.md(blk + 4))
        rdi = blk
        while rbx and self.base(self.md(rdi + 0xC)) == rbx:
            rdi = rbx
            rbx = self.base(self.md(rbx + 4))
        rax = self.b2c0(desc, rdi)
        if rax:
            self.stw(rax + 0x3E, 0)
            if (self.base(self.md(rax + 4)) or 0) == 0:
                self.stq(desc + 0x90, rax)
            if (self.base(self.md(rax + 8)) or 0) == 0:
                self.stq(desc + 0x98, rax)
            self.stb(rax + 0x15, 0)
            self.stw(rax + 0x3E, 0)
        return rax

    def bc60(self, ecx, edx, r8, r9d):
        kind = ecx & 0xFFFFFFFF
        arg4 = r9d & 0xFFFFFFFF
        ctx = r8 & 0xFFFFFFFFFFFFFFFF
        if ctx == 0 and (self.md(QCOUNT) or 0) == 0:
            return ("spin", SPIN_BC60, 0)
        eax = edx & 0xFFFFFFFF
        if eax & 0x80000000: eax = 0
        eax = (eax + 0x3F) & 0xFFFFFFFF
        corr = 0x3F if eax & 0x80000000 else 0
        r14 = ((eax + corr) & 0xFFFFFFFF) & 0xFFFFFFC0
        rbx = DTAB + kind * 0xA8 if kind <= 0xE else 0
        if rbx == 0:
            return ("fault", 0x2, 0x36BCC5, eax)
        self.stb(rbx + 2, 1)
        if ctx == 0:
            if not ((self.md(MASKG) or 0) >> (kind & 0x1F)) & 1:
                return ("ret", 0)
            edi = 0
            if arg4 == 0:
                cur = self.mq(rbx + 0x90) or 0
                while cur:
                    if sx32(self.md(cur + 0x18) or 0) >= sx32(r14):
                        edi = cur; break
                    cur = self.base(self.md(cur + 8)) or 0
            else:
                cur = self.mq(rbx + 0x98) or 0
                while cur:
                    if sx32(self.md(cur + 0x18) or 0) >= sx32(r14):
                        edi = cur; break
                    cur = self.base(self.md(cur + 4)) or 0
            tag = self.md(TAGEP) or 0
        else:
            edi = ctx
            tag = (self.mb(ctx + 0x16) or 0)
        rdi = edi
        if rdi == 0:
            self.stw(rbx + 0x60, ((self.mw(rbx + 0x60) or 0) + 1) & 0xFFFF)
            return ("ret", 0)
        r15 = self.base(self.md(rdi + 0xC)) or 0
        r12 = self.base(self.md(rdi + 0x10)) or 0
        prev1 = self.base(self.md(rdi + 4)) or 0
        next1 = self.base(self.md(rdi + 8)) or 0
        r13 = sx32(self.md(rdi + 0x18) or 0)
        if arg4 == 0:
            rsi = rdi
            rbp = rdi + 0x40 + r14
        else:
            rsi = rdi + (r13 - r14)
            rbp = rdi
        rem = r13 - r14 - 0x40
        if rem < 0:
            rbp = 0
            if (self.mq(rbx + 0x90) or 0) == rdi:
                self.stq(rbx + 0x90, next1)
            if (self.mq(rbx + 0x98) or 0) == rdi:
                self.stq(rbx + 0x98, prev1)
        else:
            if (self.mq(rbx + 0x90) or 0) == rdi:
                self.stq(rbx + 0x90, rbp)
            if (self.mq(rbx + 0x98) or 0) == rdi:
                self.stq(rbx + 0x98, rbp)
        self.c900(rbx, rdi)
        self.c9d0(rdi, 1)
        self.a490(kind, rsi, r14, (self.mw(rbx + 0x60) or 0))
        self.stb(rsi + 0x15,
                 (self.mb(rsi + 0x15) or 0) | (arg4 & 0xFF))
        self.a490(kind, rbp, rem & 0xFFFFFFFF,
                  (self.mw(rbx + 0x60) or 0))
        self.stb(rsi + 0x14, (self.mb(rsi + 0x14) or 0) | 1)
        tagi = sx32(tag)
        self.stb(rsi + 0x16, tagi & 0xFF)
        self.stw(rsi + 0x3E, 0)
        if rbp:
            self.stb(rbp + 0x14, (self.mb(rbp + 0x14) or 0) & 0xFE)
            self.stw(rbp + 0x3E, 0)
            self.b5f0(rbx, rbp)
        if arg4 == 0:
            if r15: self.twin(B7F0, r15, rsi)
            elif r12: self.twin(B8B0, r12, rsi)
            else:
                self.stq(rbx + 0x90, 0); self.stq(rbx + 0x98, 0)
            if rbp:
                self.twin(B7F0, rsi, rbp)
        elif rbp:
            if r15:
                self.twin(B7F0, r15, rbp)
                self.twin(B7F0, rbp, rsi)
            elif r12:
                self.twin(B8B0, r12, rsi)
                self.twin(B8B0, rsi, rbp)
            else:
                self.twin(B7F0, rbp, rsi)
        else:
            if r15: self.twin(B7F0, r15, rsi)
            elif r12: self.twin(B8B0, r12, rsi)
            else:
                self.std(rbx + 0x90, 0); self.stq(rbx + 0x98, 0)
        if rbp:
            if prev1: self.twin(B670, prev1, rbp)
            elif next1: self.twin(B730, next1, rbp)
            rax2 = self.b210(rbx, rbp)
            if rax2:
                self.stb(rax2 + 0x14,
                         (self.mb(rax2 + 0x14) or 0) & 0xFE)
                self.stw(rax2 + 0x3E, 0)
        if self.deep: return self.deep
        if self.trap:
            return ("trap", self.trap, 0)
        ua = rbx + tagi * 4 + 0x68
        self.std(ua, ((self.md(ua) or 0) + r14) & 0xFFFFFFFF)
        self.stw(rbx + 0x60, ((self.mw(rbx + 0x60) or 0) + 1) & 0xFFFF)
        return ("ret", rsi + 0x40)

    # ---- pool BST helpers ----
    def b490(self, rcx, rdx):
        """force-attach rdx as rcx's +0x24 child. rax = C620(rdx)."""
        if rdx:
            self.std(rdx + 0x2C, self.c620(rcx))
            self.stw(rdx + 0x3E, 0)
        self.std(rcx + 0x24, self.c620(rdx))
        self.stw(rcx + 0x3E, 0)
        return self.c620(rdx)

    def b5a0(self, rcx, rdx):
        """+0x28 twin of b490: force-attach rdx as rcx's right child."""
        if rdx:
            self.std(rdx + 0x2C, self.c620(rcx))
            self.stw(rdx + 0x3E, 0)
        rax = self.c620(rdx)
        self.std(rcx + 0x28, rax)
        self.stw(rcx + 0x3E, 0)
        return rax

    def b4e0(self, rcx, rdx, r8d=0):
        """keyed BST insert-under: descend +0x24 while anchor.key >
        node.key (signed), else +0x28. r8d tag is DEAD."""
        if rdx == 0: return 0
        rbx = rcx
        rdi = rdx
        rax = 0
        if rbx == 0: return rax
        nkey = sx32(self.md(rdi + 0x18) or 0)
        while True:
            akey = sx32(self.md(rbx + 0x18) or 0)
            if akey <= nkey:
                nxt = self.base(self.md(rbx + 0x28)) or 0
                if nxt:
                    rbx = nxt; continue
                self.std(rdi + 0x2C, self.c620(rbx))
                self.stw(rdi + 0x3E, 0)
                rax = self.c620(rdi)
                self.std(rbx + 0x28, rax)
                break
            nxt = self.base(self.md(rbx + 0x24)) or 0
            if nxt:
                rbx = nxt; continue
            self.std(rdi + 0x2C, self.c620(rbx))
            self.stw(rdi + 0x3E, 0)
            rax = self.c620(rdi)
            self.std(rbx + 0x24, rax)
            break
        self.stw(rbx + 0x3E, 0)
        return rax

    def b410(self, desc, node, tag=0):
        """BST insert: null node's links+parent, clear w3e; empty root
        -> node is root; else B4E0(root, node). rax = last C620."""
        if node == 0: return 0
        rax = self.c620(0)
        self.std(node + 0x2C, rax)
        self.std(node + 0x24, rax)
        self.std(node + 0x28, rax)
        self.stw(node + 0x3E, 0)
        rsi = self.mq(desc + 0x50) or 0
        if rsi == 0:
            self.stq(desc + 0x50, node)
            return rax
        return self.b4e0(rsi, node, tag)

    def c790(self, desc, node, tag=0):
        """BST unlink. tag is DEAD. Re-attaches the left subtree under
        the right child via B4E0 when both exist."""
        if node == 0: return 0
        rbx = self.base(self.md(node + 0x2C)) or 0   # parent
        rsi = self.base(self.md(node + 0x24)) or 0   # left
        rdi = self.base(self.md(node + 0x28)) or 0   # right
        rax = 0
        if rbx == 0:
            if rdi:
                self.stq(desc + 0x50, rdi)
                self.std(rdi + 0x2C, self.c620(0))
                self.stw(rdi + 0x3E, 0)
                rax = self.b4e0(rdi, rsi, tag)
            elif rsi:
                self.stq(desc + 0x50, rsi)
                self.std(rsi + 0x2C, self.c620(0))
                self.stw(rsi + 0x3E, 0)
            else:
                self.stq(desc + 0x50, 0)
            return rax
        if rdi:
            self.b4e0(rdi, rsi, tag)
            self.std(rdi + 0x2C, self.c620(rbx))
            if (self.base(self.md(rbx + 0x24)) or 0) == node:
                self.std(rbx + 0x24, self.c620(rdi))
            elif (self.base(self.md(rbx + 0x28)) or 0) == node:
                self.std(rbx + 0x28, self.c620(rdi))
            self.stw(rdi + 0x3E, 0)
            self.stw(rbx + 0x3E, 0)
            return 0   # xor eax,eax tails this arm
        if (self.base(self.md(rbx + 0x24)) or 0) == node:
            rax = self.b490(rbx, rsi)
        if (self.base(self.md(rbx + 0x28)) or 0) == node:
            rax = self.b5a0(rbx, rsi)
        return rax

    # ---- adopt-one ----
    def a2a0(self, desc, rbx, rbp):
        """A2A0(rcx=desc, rdx=rbx free node, r8=rbp pool block).
        Moves the pool block's identity onto a carve of rbx.
        Returns 0 (label-copy NUL residual)."""
        if rbp == 0 or self.mb(rbp + 0x14) is None:
            return ("fault", (rbp + 0x14) & 0xFFFFFFFFFFFFFFFF,
                    0x36A2C3,
                    GSCOOK ^ (self.vsp - 0xA8 & 0xFFFFFFFFFFFFFFFF))
        # snapshot src trailer + label (src fields read BEFORE C790)
        f14 = self.mb(rbp + 0x14) or 0
        f15 = self.mb(rbp + 0x15) or 0
        b2 = self.mb(rbp + 2) or 0
        b3 = self.mb(rbp + 3) or 0
        tag = self.mb(rbp + 0x16) or 0
        t17 = self.mb(rbp + 0x17) or 0
        w1e = self.mw(rbp + 0x1E) or 0
        d30 = self.md(rbp + 0x30) or 0
        label = bytearray()
        i = 0
        while True:
            ch = self.mb(rbp + 0x34 + i)
            label.append(ch if ch is not None else 0)
            i += 1
            if not ch or i > 0x20:
                break
        r15 = f15 & 2
        if r15:
            self.c790(desc, rbp, 0x14B6)
        rsi = self.base(self.md(rbp + 0x20)) or 0
        if rsi and rbx:
            self.stq(rsi + 8, rbx)
            self.std(rbx + 0x20, self.c620(rsi))
            self.stw(rsi + 6, self.mw(rbx + 0x1C) or 0)
            self.stw(rbx + 0x3E, 0)
        ua = PTAGC + t17 * 4
        self.std(ua, ((self.md(ua) or 0)
                      + (self.md(rbp + 0x18) or 0)) & 0xFFFFFFFF)
        # free the vacated source; prel's frame rsp = a2a0 entry rsp
        # - 0xB8 (callsite) - 0x1178 (prel prologue)
        r = self.prel(rbp + 0x40, 0,
                      (self.vsp - 0x1230) & 0xFFFFFFFFFFFFFFFF)
        if isinstance(r, tuple) and r[0] != "ret":
            return r
        r = self.pinit(rbx + 0x40, rbp + 0x40,
                       self.md(rbp + 0x18) or 0)
        if isinstance(r, tuple) and r[0] != "ret":
            return r
        r = self.bc60(self.mb(desc + 1) or 0,
                      self.md(rbp + 0x18) or 0, rbx, 0)
        if r[0] != "ret":
            return r
        # copy snapshot + label onto rbx (over the fresh header)
        self.stb(rbx + 0x14, f14)
        self.stb(rbx + 0x15, f15)
        self.stb(rbx + 2, b2)
        self.stb(rbx + 3, b3)
        self.stb(rbx + 0x16, tag)
        self.std(rbx + 0x30, d30)
        self.stw(rbx + 0x1E, w1e)
        self.stb(rbx + 0x17, t17)
        for i, ch in enumerate(label):
            self.stb(rbx + 0x34 + i, ch)
        rax = self.c620(rsi)          # unguarded d[rbx+0x20] write
        self.std(rbx + 0x20, rax)
        if r15:
            self.stb(rbx + 0x15, (self.mb(rbx + 0x15) or 0) & 0xFD)
            rax = self.b410(desc, rbx, 0x14E5)
            self.stb(rbx + 0x15, (self.mb(rbx + 0x15) or 0) | 2)
        if rsi:
            self.stq(rsi + 8, rbx)
            self.std(rbx + 0x20, self.c620(rsi))
            rax = self.mw(rbx + 0x1C) or 0   # movzx eax tails the arm
            self.stw(rsi + 6, rax)
        self.stw(rbx + 0x3E, 0)
        return ("ret", rax)

    # ---- adoption scans ----
    def aad0(self, desc, r12d):
        rsi = self.mq(desc + 0x90) or 0
        r15 = 0
        if rsi == 0: return ("ret", 0)
        while True:
            rbx = self.mq(desc + 0x50) or 0
            if rsi == 0:
                # re-read head can be 0 (adoption emptied the list):
                # d[0x18] deref faults, rax = a2a0's 0 residual
                return ("fault", 0x18, 0x36AB16, 0)
            r14d = sx32(self.md(rsi + 0x18) or 0)
            rdi = 0
            while rbx:
                rbp = self.base(self.md(rbx + 0x24)) or 0
                rcx_ = self.base(self.md(rbx + 0x28)) or 0
                eax = sx32(self.md(rbx + 0x18) or 0)
                if eax > r14d:
                    rbx = rbp
                    continue
                if eax == r14d:
                    if ((rbx & 0xFFFFFFFF) > (rsi & 0xFFFFFFFF)
                            and not ((self.mb(rbx + 0x15) or 0) & 4)):
                        saved = self.vsp
                        self.vsp = (self.vsp - 0x48) & 0xFFFFFFFFFFFFFFFF
                        r = self.a2a0(desc, rsi, rbx)
                        self.vsp = saved
                        r15 += 1
                        if self.deep: return self.deep
                        if self.trap or r[0] != "ret":
                            return r
                        if r12d & 0xFFFFFFFF:
                            rsi = self.mq(desc + 0x90) or 0
                            break
                        return ("ret", r15)
                else:
                    if (rdi == 0
                            or sx32(self.md(rdi + 0x18) or 0) <= eax):
                        if ((rbx & 0xFFFFFFFF) > (rsi & 0xFFFFFFFF)
                                and not ((self.mb(rbx + 0x15) or 0) & 4)):
                            rdi = rbx
                rbx = rcx_
            else:
                return ("ret", r15)
            # r12d arm re-entered the outer loop

    def abe0(self, desc):
        rdi = self.mq(desc + 0x90) or 0
        if rdi == 0: return ("ret", 0)
        while True:
            r8 = self.base(self.md(rdi + 0x10)) or 0
            if r8 == 0: return ("ret", 0)
            if ((self.mb(r8 + 0x15) or 0) & 6) == 2:
                # flag arm: src IS the phys-next node (r8 survives;
                # jne 0x36ac8f skips the mov r8,rbx reload)
                if (self.mb(r8 + 0x14) or 0) & 1:
                    saved = self.vsp
                    self.vsp = (self.vsp - 0x28) & 0xFFFFFFFFFFFFFFFF
                    r = self.a2a0(desc, rdi, r8)
                    self.vsp = saved
                    if self.deep: return self.deep
                    if self.trap or r[0] != "ret":
                        return r
                    return ("ret", 1)
                return ("ret", 0)   # marked-but-free: whole scan stops
            rbx = self.mq(desc + 0x50) or 0
            ebp = sx32(self.md(rdi + 0x18) or 0)
            while rbx:
                rsi_ = self.base(self.md(rbx + 0x24)) or 0
                rax_ = self.base(self.md(rbx + 0x28)) or 0
                ecx = sx32(self.md(rbx + 0x18) or 0)
                if ecx > ebp:
                    rbx = rsi_
                    continue
                if (ecx == ebp
                        and (rbx & 0xFFFFFFFF) > (rdi & 0xFFFFFFFF)
                        and not ((self.mb(rbx + 0x15) or 0) & 4)):
                    break
                rbx = rax_
            if rbx:
                saved = self.vsp
                self.vsp = (self.vsp - 0x28) & 0xFFFFFFFFFFFFFFFF
                r = self.a2a0(desc, rdi, rbx)
                self.vsp = saved
                if self.deep: return self.deep
                if self.trap or r[0] != "ret":
                    return r
                return ("ret", 1)
            rdi = self.base(self.md(rdi + 8)) or 0
            if rdi == 0: return ("ret", 0)

    # ---- EXP-126: free path + emit + memcpy wrapper ----
    def flag_resid(self):
        """FLAG leaf: eax = 2 iff d[FLAGG]==-1 else 0. No write."""
        return 2 if (self.md(FLAGG) or 0) == 0xFFFFFFFF else 0

    def emit(self, fmt, buf):
        """F17D2E0 real path: hook(obj|1, buf, -1, fmt) via EMITC ->
        planted FLAG leaf. Token carries fmt VA (r9) + buf (rdx).
        ret = flag residual (cmovs -1 arm is dead: ret never <0)."""
        self.trace.append("emit:%x:%x" % (fmt & 0xFFFFFFFFFFFFFFFF,
                                          buf & 0xFFFFFFFFFFFFFFFF))
        return self.flag_resid()

    def f17d2e0(self, buf, fmt, a3=0, a4=0):
        return ("ret", self.emit(fmt, buf))

    def cellhook(self, arg):
        """call q[CELLP] -> planted FLAG leaf; arg is ecx."""
        self.trace.append("cell:%x" % (arg & 0xFF))

    def chkstk(self, top):
        """_chkstk: probe pages from gs:[0x10] limit down to the new
        frame top. top = PREL_RSP for entry-level PREL frames only
        (nested a2a0->prel calls always run with teblim=0)."""
        lim = self.mq(TEB + 0x10) or 0
        if top < lim:
            top &= ~0xFFF & 0xFFFFFFFFFFFFFFFF
            p = (lim - 0x1000) & 0xFFFFFFFFFFFFFFFF
            while True:
                self.stb(p, 0)
                if p == top: break
                p = (p - 0x1000) & 0xFFFFFFFFFFFFFFFF

    def pinit(self, dst, src, n):
        """PINIT real body + real thunk; the memcpy import itself is a
        disclosed boundary (IAT cell planted to the trampoline).
        movsxd r8,r8d then memcpy(dst,src,n); returns dst."""
        n = sx32(n & 0xFFFFFFFF) & 0xFFFFFFFFFFFFFFFF
        self.trace.append("memcpy:%x:%x:%x" % (
            dst & 0xFFFFFFFFFFFFFFFF, src & 0xFFFFFFFFFFFFFFFF, n))
        i = 0
        while i < n and i < 0x100000:
            b = self.mb(src + i)
            if b is None:
                return ("fault", (src + i) & 0xFFFFFFFFFFFFFFFF,
                        MEMCPY, 0)
            if not self.mapped(dst + i):
                return ("fault", (dst + i) & 0xFFFFFFFFFFFFFFFF,
                        MEMCPY, 0)
            self.stb(dst + i, b)
            i += 1
        return ("ret", dst & 0xFFFFFFFFFFFFFFFF)

    def ae00(self, desc, node):
        """find free block at-or-below node: pslot of phys-prev via
        signed-16 floor; backward bitmap guard (bits <= slot); head-
        table descent skipping empty/oversized entries; then list-1
        +8 walk to the last free block whose next <= node."""
        if self.md(node + 0xC) is None:
            return ("fault", (node + 0xC) & 0xFFFFFFFFFFFFFFFF,
                    0x36AE1C, 0)
        ptab = self.mq(desc + 0x28) or 0
        bm = self.mq(desc + 0x20) or 0
        pp = self.base(self.md(node + 0xC)) or 0
        slot = self.pslot(desc, pp) if pp else -1
        if slot < 0:
            return 0
        word, bit = slot >> 5, slot & 0x1F
        w = self.md(bm + word * 4) or 0
        if bit < 0x1F:
            w &= (1 << (bit + 1)) - 1
        r8, r9 = slot, (word << 5) - 1
        rdx = bm + word * 4
        while not w:
            w = self.md(rdx - 4) or 0
            rdx -= 4
            r8, r9 = r9, r9 - 0x20
            if r8 < 0: break
        if r8 < 0:
            return 0
        rcx = ptab + r8 * 8
        while True:
            rax = self.mq(rcx) or 0
            if rax and rax < node:
                break
            rcx -= 8
            r8 -= 1
            if r8 < 0:
                return 0
        rbx = rax
        while True:
            nxt = self.base(self.md(rbx + 8)) or 0
            if nxt == 0 or nxt > node:
                return rbx
            rbx = nxt

    def ace0(self, desc, node):
        """find free block at-or-above node: pslot of phys-next;
        forward bitmap guard (bits >= slot) bounded by d[desc+0x58];
        head-table ascent; then list-1 +4 walk to the last free block
        whose prev >= node."""
        if self.md(node + 0x10) is None:
            return ("fault", (node + 0x10) & 0xFFFFFFFFFFFFFFFF,
                    0x36ACFC, 0)
        ptab = self.mq(desc + 0x28) or 0
        bm = self.mq(desc + 0x20) or 0
        bound = sx32(self.md(desc + 0x58) or 0)
        pn = self.base(self.md(node + 0x10)) or 0
        slot = self.pslot(desc, pn) if pn else -1
        if slot < 0:
            return 0
        word, bit = slot >> 5, slot & 0x1F
        edx = (~((1 << bit) - 1)) & (self.md(bm + word * 4) or 0)
        edx &= 0xFFFFFFFF
        r8 = slot
        if r8 < bound:
            r9, ecx = word, word << 5
            while True:
                if edx: break
                r9 += 1
                ecx += 0x20
                r8 = ecx
                edx = self.md(bm + r9 * 4) or 0
                if ecx >= bound: break
        if r8 >= bound:
            return 0
        rcx = ptab + r8 * 8
        while True:
            rax = self.mq(rcx) or 0
            if rax and rax > node:
                break
            r8 += 1
            rcx += 8
            if r8 >= bound:
                return 0
        rbx = rax
        while True:
            prv = self.base(self.md(rbx + 4)) or 0
            if prv == 0 or prv < node:
                return rbx
            rbx = prv

    def prel(self, rcx, rdx, rsp=PREL_RSP):
        """PREL free(rcx payload, rdx aux). Returns tuple.

        rsp is the frame base (entry rsp - pushes - 0x1168); nested
        callers (A2A0) pass their own so the emit buffers and the
        cookie residual land at the right addresses."""
        M64 = 0xFFFFFFFFFFFFFFFF
        if rcx == 0:
            return ("ret", 0)
        self.chkstk(rsp)
        r14 = rcx & M64
        r15 = rdx & M64
        rax = GSCOOK ^ rsp            # cookie residual until overwritten
        if r14 & 3:
            rax = self.emit(F_MHAND, rsp + 0x40)
            return ("ret", rax)
        rbx = (rcx - 0x40) & M64
        v = self.mw(rbx)
        if v is None:
            return ("fault", rbx, 0x3698D5, rax)
        if v != 0xFF12:
            # header dump: 0xB0 emit calls over rbx. The planted hook
            # writes nothing into rsp+0x30, so the dump at rsp+0x140
            # accumulates only the sep word w[0x8F3F58] = 0x000A every
            # 16th byte, then the "\nSTACK\n\0" qword tail.
            buf, off = rsp + 0x140, 0
            for i in range(0xB0):
                if self.mb(rbx + i) is None:
                    return ("fault", (rbx + i) & M64, 0x3698F0, rax)
                rax = self.emit(F_HEX, rsp + 0x30)
                if i & 0xF == 0xF:
                    self.stw(buf + off, 0x000A); off += 1
            self.stq(buf + off, 0x000A4B43415453_0A)
            rax = buf + off          # movsd dest is the aux-fault
            off += 7                 # residual (rsp+0x140+0xB on i=0)
            for i in range(0xD0):
                if self.mb(r15 + i) is None:
                    return ("fault", (r15 + i) & M64, 0x3699B0, rax)
                rax = self.emit(F_HEX, rsp + 0x30)
                if i & 0xF == 0xF:
                    self.stw(buf + off, 0x000A); off += 1
                    rax = 0x000A     # movzx eax,w[sep cell] residual
                else:
                    rax = i & 0xF    # mov eax,esi;and eax,0xf residual
            rax = self.emit(F_ILL, rsp + 0x940)
            kind = self.mb(rbx + 3) or 0
            self.std(ST_W, kind)
            r = self.a570(kind, 0xB, 0xFFFFFFFF)
            if isinstance(r, tuple) and r[0] != "ret":
                return r
            self.cellhook(1)
            rax = self.flag_resid()
            self.trap = PREL_I3_MAGIC + 1
            return ("trap", self.trap, rax)
        v3e = self.mw(rbx + 0x3E)
        if v3e is None:
            return ("fault", (rbx + 0x3E) & M64, 0x369A80, rax)
        if v3e != 0:
            rax = self.emit(F_MCB, rsp + 0x40)
            kind = self.mb(rbx + 3) or 0
            self.std(ST_W, kind)
            r = self.a570(kind, 0xB, 0xFFFFFFFF)
            if isinstance(r, tuple) and r[0] != "ret":
                return r
            self.cellhook(1)
            rax = self.flag_resid()
            self.trap = PREL_I3_MARK + 1
            return ("trap", self.trap, rax)
        f14 = self.mb(rbx + 0x14)
        if f14 is None:
            return ("fault", (rbx + 0x14) & M64, 0x369ABE, rax)
        if not (f14 & 1):
            rax = self.emit(F_FREE, rsp + 0x40)
            return ("ret", rax)
        # ---- real free ----
        kind = self.mb(rbx + 3) or 0
        if kind >= 0xF:
            return ("fault", 0x2, 0x369B01, kind)
        desc = DTAB + kind * 0xA8
        self.stb(desc + 2, 1)
        tag = self.mb(rbx + 0x16) or 0
        self.stb(rbx + 0x14, f14 & 0xFE)
        self.stb(rbx + 2, 0xFF)
        key = self.md(rbx + 0x18) or 0
        ua = desc + 0x68 + tag * 4
        self.std(ua, ((self.md(ua) or 0) - key) & 0xFFFFFFFF)
        b17 = self.mb(rbx + 0x17) or 0
        if b17:
            pa = PTAGC + b17 * 4
            self.std(pa, ((self.md(pa) or 0) - key) & 0xFFFFFFFF)
        self.stb(rbx + 0x34, 0)
        self.stw(rbx + 0x1E, 0)
        self.stb(rbx + 0x17, 0)
        rax = self.c620(0)
        self.std(rbx + 0x30, rax)
        self.stw(rbx + 0x3E, 0)
        pp = self.base(self.md(rbx + 0xC)) or 0
        done_splice = False
        if pp and not ((self.mb(pp + 0x14) or 0) & 1):
            self.twin(B670, pp, rbx)
            done_splice = True
        else:
            pn = self.base(self.md(rbx + 0x10)) or 0
            if pn and not ((self.mb(pn + 0x14) or 0) & 1):
                self.twin(B730, pn, rbx)
                done_splice = True
            else:
                bound = self.mq(desc + 0x18) or 0
                if rbx < bound:
                    rsi = self.ae00(desc, rbx)
                    if isinstance(rsi, tuple):
                        return rsi
                    if rsi:
                        stale = self.base(self.md(rbx + 4)) or 0
                        if rsi != stale:
                            self.twin(B670, rsi, rbx)
                    else:
                        rsi = self.ace0(desc, rbx)
                        if isinstance(rsi, tuple):
                            return rsi
                        stale = self.base(self.md(rbx + 8)) or 0
                        if rsi != stale:
                            self.twin(B730, rsi, rbx)
                else:
                    rsi = self.ace0(desc, rbx)
                    if isinstance(rsi, tuple):
                        return rsi
                    stale = self.base(self.md(rbx + 8)) or 0
                    if rsi != stale:
                        self.twin(B730, rsi, rbx)
                    else:
                        rsi = self.ae00(desc, rbx)
                        if isinstance(rsi, tuple):
                            return rsi
                        stale = self.base(self.md(rbx + 4)) or 0
                        if rsi != stale:
                            self.twin(B670, rsi, rbx)
                done_splice = True
        if self.deep: return self.deep
        if self.trap: return ("trap", self.trap, 0)
        rax2 = self.b210(desc, rbx)
        if self.deep: return self.deep
        if self.trap: return ("trap", self.trap, 0)
        rax = self.b5f0(desc, rax2)
        if self.deep: return self.deep
        if self.trap: return ("trap", self.trap, 0)
        return ("ret", rax)

    # ---- diagnostic ----
    def _label_pick(self, rbx):
        f14 = self.mb(rbx + 0x14) or 0
        f15 = self.mb(rbx + 0x15) or 0
        if not (f14 & 1): return "FREE"
        if f15 & 1: return "M2/l" if (f15 & 4) else "M2/U"
        if f15 & 2: return "M /l" if (f15 & 4) else "M /U"
        return "M /L"

    def a850(self, rcx):
        """pre-order BST label-format walk; stack-local output only.
        Returns the last advance decode (BASE(d[last+0x28]))."""
        rbx = rcx
        rax = 0
        while rbx:
            if self.mb(rbx + 0x14) is None:
                return ("fault", (rbx + 0x14) & 0xFFFFFFFFFFFFFFFF,
                        0x36A8A0,
                        GSCOOK ^ (self.vsp - 0x268 & 0xFFFFFFFFFFFFFFFF))
            self._label_pick(rbx)          # built on stack, discarded
            left = self.base(self.md(rbx + 0x24)) or 0
            if left:
                r = self.a850(left)
                if isinstance(r, tuple):
                    return r
            nxt = self.base(self.md(rbx + 0x28)) or 0
            rax = nxt
            rbx = nxt
        return rax

    def a570(self, ecx, edx, r8d):
        kind = ecx & 0xFFFFFFFF
        bpl = edx & 0xFFFFFFFF
        esi = r8d & 0xFFFFFFFF
        esi_s = sx32(esi)
        rax = self.md(MASKG) or 0
        if not ((rax >> (kind & 0x1F)) & 1):
            return ("ret", rax)
        rdi = DTAB + kind * 0xA8 if kind <= 0xE else 0
        if rdi == 0:
            return ("fault", 0x10, 0x36A5C7, rax)
        rax = DTAB     # lea rax,[rip+DTAB] feeds the imul/add
        rbx = self.mq(rdi + 0x10) or 0
        if (bpl & 1) and rbx:
            while True:
                if self.mb(rbx + 0x14) is None:
                    return ("fault",
                            (rbx + 0x14) & 0xFFFFFFFFFFFFFFFF,
                            0x36A60E, rax)
                f14 = self.mb(rbx + 0x14) or 0
                self._label_pick(rbx)      # stack-local build
                enter = False
                if f14 & 1:
                    enter = esi_s < 0 or (self.mb(rbx + 2) or 0) == esi_s
                else:
                    enter = esi_s < 0
                if enter and ((self.mw(rbx + 0x1E) or 0) != 0
                              or (self.mb(rbx + 0x34) or 0) != 0):
                    # hook(buf, rbx+0x34, 8) -> planted FLAG leaf;
                    # FLAG is a pure cmove leaf - no FLAGG write
                    self.trace.append("out:%x:%x" % (rbx + 0x34, 8))
                rax = self.base(self.md(rbx + 8)) or 0
                if rax == rbx:
                    break
                rbx = self.base(self.md(rbx + 0x10)) or 0
                rax = rbx
                if rbx == 0:
                    break
        if bpl & 2:
            rbx = self.mq(rdi + 0x90) or 0
            while rbx:
                if self.md(rbx + 8) is None:
                    return ("fault",
                            (rbx + 8) & 0xFFFFFFFFFFFFFFFF,
                            0x36A755, rax)
                rax = self.base(self.md(rbx + 8)) or 0
                if rax == rbx:
                    break
                rbx = rax
        itab_base = self.mq(rdi + 0x30) or 0
        if bpl & 8:
            rcx = self.mq(rdi + 0x48) or 0
            while rcx:
                edx_ = self.mw(rcx) or 0
                rax = ((rcx - (self.md(rdi + 0x30) or 0))
                       & 0xFFFFFFFF) >> 4
                if (rax == edx_ or (self.mq(rcx + 8) or 0) == 0
                        or edx_ == 0xFFFF):
                    break
                rcx = (itab_base + edx_ * 0x10) & 0xFFFFFFFFFFFFFFFF
        if bpl & 0x10:
            rcx = self.mq(rdi + 0x40) or 0
            while rcx:
                edx_ = self.mw(rcx) or 0
                rax = ((rcx - (self.md(rdi + 0x30) or 0))
                       & 0xFFFFFFFF) >> 4
                if rax == edx_ or edx_ == 0xFFFF:
                    break
                rcx = (itab_base + edx_ * 0x10) & 0xFFFFFFFFFFFFFFFF
        if bpl & 0x20:
            rcx = self.mq(rdi + 0x50) or 0
            if rcx:
                r = self.a850(rcx)
                if isinstance(r, tuple):
                    return r
                rax = r
        return ("ret", rax)

    # ---- EXP-128: queue poll-pump layer ----
    def _xval(self, key, default=0):
        """scripted-boundary return plant; a list value is consumed
        in call order so multi-pass cases can sequence gates."""
        v = self.case.get(key, default)
        if isinstance(v, list):
            i = min(self.xctr.get(key, 0), len(v) - 1)
            self.xctr[key] = self.xctr.get(key, 0) + 1
            return v[i]
        return v

    def e810(self):
        return self.mq(TICKQ) or 0

    def g8c70(self):
        return self.md(TICKD) or 0

    def ge0e0(self):
        return self.md(FLAGG) or 0

    def g97f0(self, rcx, rsp):
        """3697F0 free-if-nonnull: test rcx -> ret; else PREL(rcx,0).
        Tail-jmps land PREL on the caller's frame — rsp is prel's
        post-prologue rsp derived from the entry path."""
        if rcx == 0:
            return None
        return self.prel(rcx & 0xFFFFFFFFFFFFFFFF, 0, rsp=rsp)

    def e330(self, t, rspoff=0x1178):
        rax = 0
        if (self.mq(t + 0x40) or 0) != 0:
            self._rdx = self.mq(t + 0x70) or 0      # mov rdx,q[+0x70]
            self._r8 = 1                            # mov r8d,1
            self.trace.append("cb40:%x:%x:%x" % (
                self.md(t + 0x60) or 0, self._rdx, 1))
            rax = self._xval("cb40ret") & 0xFFFFFFFF
        if (self.mb(t + 0x21) or 0) == 0xFF:
            rcx = sx32(self.md(t + 0x24) or 0) & 0xFFFFFFFFFFFFFFFF
            r = self.g97f0(rcx, (self.vsp - rspoff) & 0xFFFFFFFFFFFFFFFF)
            if r is not None:
                return r
        return ("ret", rax)

    def e370(self, t, rspoff=0x1178):
        rax = 0
        cb = self.mq(t + 0x40) or 0
        if cb != 0:
            rax = cb          # gated-out path keeps the cb pointer
            if (self.md(t + 0x28) or 0) == 0xFFFFFFFF:
                self._rdx = self.mq(t + 0x70) or 0  # mov rdx,q[+0x70]
                self._r8 = 0                        # xor r8d,r8d
                self.trace.append("cb40:%x:%x:%x" % (
                    self.md(t + 0x60) or 0, self._rdx, 0))
                rax = self._xval("cb40ret") & 0xFFFFFFFF
        if (self.mb(t + 0x21) or 0) == 0xFF:
            rcx = sx32(self.md(t + 0x24) or 0) & 0xFFFFFFFFFFFFFFFF
            r = self.g97f0(rcx, (self.vsp - rspoff) & 0xFFFFFFFFFFFFFFFF)
            if r is not None:
                return r
        return ("ret", rax)

    def e3b0(self, t):
        if (self.mq(t + 0x50) or 0) == 0:
            return ("ret", 1)    # 32e3e0: mov eax,1
        self.trace.append("cb50:%x" % (t & 0xFFFFFFFFFFFFFFFF))
        ebx = self._xval("cb50ret") & 0xFFFFFFFF
        if (ebx - 1) & 0xFFFFFFFF > 2:
            self._rdx = 0x1CCF998   # real 8620C0: lea rdx,[rip+..]
        return ("ret", ebx)

    def ec40(self, t):
        """unlink t from the +0x10/+0x18 list (TASKH head, TASKG tail),
        push onto TASKI's idle list, d[+0x64]=-1, tail 16D6A0 noop."""
        nxt = self.mq(t + 0x18) or 0
        prv = self.mq(t + 0x10) or 0
        if nxt == 0:
            self.stq(TASKG, prv)
        if prv == 0:
            self.stq(TASKH, nxt)
        if nxt:
            self.stq(nxt + 0x10, prv)
        if prv:
            self.stq(prv + 0x18, nxt)
        old = self.mq(TASKI) or 0
        self.stq(t + 0x18, 0)
        if old:
            self.stq(old + 0x18, t)
        self.stq(t + 0x10, old)
        self.stq(TASKI, t)
        self.std(t + 0x64, 0xFFFFFFFF)
        self._r8, self._rdx = nxt, prv     # ec40's first two loads
        return ("ret", old)                # rax = old idle head

    def _e070_retire(self, rbx, which, clear23=False):
        """shared retire tail: e330/e370 -> [tail-B clears b[+0x23]]
        -> b[+0x20]=0 -> ec40."""
        r = (self.e330 if which == 5 else self.e370)(rbx, 0x11B8)
        if isinstance(r, tuple) and r[0] != "ret":
            return r
        if self.trap: return ("trap", self.trap, 0)
        if self.deep: return self.deep
        if clear23:
            self.stb(rbx + 0x23, 0)
        self.stb(rbx + 0x20, 0)
        self.ec40(rbx)
        return None

    def _e070_requeue(self, rbx, eax):
        """0x32e222 requeue block: d28=min-result, d2c rounding,
        q[0]=0, state=1, b23=0."""
        self.std(rbx + 0x28, eax)
        v = sx32(self.md(rbx + 0x2c) or 0)
        self._rdx = 0xFFFFFFFF if v < 0 else 0      # cdq
        edx = self._rdx & 0x7FF                      # and edx,0x7ff
        self.stq(rbx, 0)
        self.stb(rbx + 0x20, 1)
        nv = (v + edx) & 0xFFFFFFFF
        self.stb(rbx + 0x23, 0)
        self.std(rbx + 0x2c, nv & 0xFFFFF800)

    def e070(self):
        rax = 0
        for _ in range(64):
            rbx = self.mq(TASKG) or 0
            if rbx == 0:
                self.trace.append("xadd0")
                rax = self._xval("xadd0") & 0xFFFFFFFF
                break
            st = self.mb(rbx + 0x20) or 0
            if not (1 <= st <= 6):
                break                       # ja 0x32e2a0 teardown
            if st == 1:
                self.trace.append("xadd0")
                rax = self._xval("xadd0") & 0xFFFFFFFF
                if rax != 0:
                    break
                cnt = self.md(rbx + 0x28) or 0
                self._r8 = cnt                # mov r8d,d[+0x28]
                if cnt == 0:
                    r = self._e070_retire(rbx, 5)
                    if r is not None: return r
                    continue
                b21 = self.mb(rbx + 0x21) or 0
                if b21 != 0xFF:
                    self._rdx = self.md(rbx + 0x24) or 0   # mov edx
                    self._r8 = self.md(rbx + 0x2c) or 0    # mov r8d
                    self.trace.append("x46e0:%x:%x:%x:%x:%x" % (
                        b21, self._rdx, self._r8, cnt,
                        self.mq(rbx + 0x38) or 0))
                    rax = self._xval("x46e0") & 0xFFFFFFFF
                else:
                    rcx = sx32(self.md(rbx + 0x24) or 0)
                    self._rdx = self.mq(rbx + 0x38) or 0   # mov rdx
                    self.trace.append("x2df6:%x:%x:%x" % (
                        rcx & 0xFFFFFFFFFFFFFFFF,
                        self._rdx, self.md(rbx + 0x2c) or 0))
                    rax = self._xval("x2df6") & 0xFFFFFFFF
                    if rax != 0:
                        continue
                rax = self.e810()
                self.stq(rbx + 8, rax)
                self.stb(rbx + 0x20, 2)
                continue
            if st == 2:
                self.e810()
                rax = self.e810()
                self.stq(rbx, ((self.mq(rbx) or 0) + rax)
                         & 0xFFFFFFFFFFFFFFFF)
                self.stq(rbx + 8, rax)
                self.stb(rbx + 0x20, 3)
                continue
            if st in (3, 4):
                # the direct call 0x46dfe0 reaches the planted FLAG
                # leaf -> hooked as an unclassified call -> out:rdx:r8
                self.trace.append("out:%x:%x" % (
                    self._rdx & 0xFFFFFFFFFFFFFFFF,
                    self._r8 & 0xFFFFFFFFFFFFFFFF))
                rax = self.flag_resid()      # FLAG real: !=0 -> teardown
                if rax != 0:
                    break
                if st == 4:
                    if (self.mq(rbx + 0x48) or 0) != 0:
                        self.std(rbx + 0x28, 0)
                        self.trace.append("cb48:%x" % (
                            self.md(rbx + 0x60) or 0))
                        rax = self._xval("cb48ret") & 0xFFFFFFFF
                    self.stb(rbx + 0x20, 0)
                    self.ec40(rbx)
                    continue
                rax = self.ge0e0()           # poll: d[FLAGG]
                self.stb(rbx + 0x20, 5 + (1 if sx32(rax) < 0 else 0))
            # ---- S5/6 shared block (also entered from S3's poll) ----
            b22 = self.mb(rbx + 0x22) or 0
            if b22 == 0:
                cur = self.mb(rbx + 0x20) or 0
                r = self._e070_retire(rbx, cur)
                if r is not None: return r
                continue
            if b22 != 1:
                break
            b23 = self.mb(rbx + 0x23) or 0
            if b23 == 2:
                r = self.e3b0(rbx)
                if r[0] != "ret": return r
                al = r[1] & 0xFF
                self.stb(rbx + 0x23, al)
                if al != 1:
                    break
                e = sx32(self.md(rbx + 0x30) or 0)
                d34 = sx32(self.md(rbx + 0x34) or 0)
                self._e070_requeue(rbx, d34 if d34 < e else e)
                continue
            if (self.mb(rbx + 0x20) or 0) == 6:
                r = self._e070_retire(rbx, 6, clear23=True)
                if r is not None: return r
                continue
            # progress arm (state 5 only)
            step = sx32(self.md(rbx + 0x28) or 0)
            d34 = sx32(self.md(rbx + 0x34) or 0) - step
            self.std(rbx + 0x34, d34 & 0xFFFFFFFF)
            if d34 <= 0:
                r = self._e070_retire(rbx, 5, clear23=True)
                if r is not None: return r
                continue
            self.std(rbx + 0x2c, ((self.md(rbx + 0x2c) or 0) + step)
                     & 0xFFFFFFFF)
            self.stq(rbx + 0x38, ((self.mq(rbx + 0x38) or 0) + step)
                     & 0xFFFFFFFFFFFFFFFF)
            r = self.e3b0(rbx)
            if r[0] != "ret": return r
            al = r[1] & 0xFF
            self.stb(rbx + 0x23, al)
            if al != 1:
                break
            e = sx32(self.md(rbx + 0x30) or 0)
            d34 = sx32(self.md(rbx + 0x34) or 0)
            self._e070_requeue(rbx, d34 if d34 < e else e)
            continue
        else:
            return ("spin", 0x32E090, rax)  # runaway loop guard
        # ---- teardown: 46DD50 + 16D6A0 + 3E9780 + 16D6A0 + 36FD50
        self.trace.append("x46dd")
        self.trace.append("x3e97")
        self.trace.append("x36fd")
        rax = self._xval("x36fd") & 0xFFFFFFFF
        if rax != 0:
            self.trace.append("x3bb7")
        return ("ret", rax)

    def eb70(self, ecx, edx):
        M64 = 0xFFFFFFFFFFFFFFFF
        esi, edi = edx & 0xFFFFFFFF, ecx & 0xFFFFFFFF
        rbx = sx32(self.g8c70()) & M64
        self.trace.append("xtick")
        rax = self._xval("xtick") & M64
        if rbx == rax:
            # resync arm: rewrite the pacer dword cluster
            self.trace.append("x17d3")
            if (self._xval("x17d3") & 0xFFFFFFFF) == 0:
                self.trace.append("x91b0:%x" % 0)
                self.trace.append("x9190:%x" % 0)
            a = ((self.md(PACC) or 0) + (self.md(PACC + 0xC) or 0)) \
                & 0xFFFFFFFF
            self.std(PACC, a)
            self.std(PACC + 0x14, a)
            self.trace.append("x35e7")
            e7 = self._xval("x35e7") & 0xFFFFFFFF
            self.std(PACC + 0x18, e7)
            lim = edi if sx32(edi) > 0 else 1
            self.std(PACC + 0x30, lim)
            self.std(PACC + 0x40, esi)
            e = self.md(PACC + 0x2C) or 0
            self.std(PACC + 0x3C, 0)
            self.std(PACC + 0x2C, 0)
            c = self.md(PACC + 0x48) or 0
            self.std(PACC + 0x5C, c)
            self.std(PACC + 0x60, e)
            self.std(PACC + 0x64, lim)
            self.std(PACC, 0)
            return ("ret", e & M64)
        # wait arm: spin on TICKQ until it advances >= max(ecx,1)
        r8 = self.mq(TICKQ) or 0
        want = (r8 + sx32(edi if sx32(edi) > 0 else 1)) & M64
        while True:
            self.stq(TICKQ, ((self.mq(TICKQ) or 0) + 1) & M64)
            cur = self.mq(TICKQ) or 0
            if cur >= want:
                break
        return ("ret", (cur - r8) & M64)


def run_model(case, raw, secs):
    m = Model(case, raw, secs)
    for step in case.get("steps", []):
        m.vsp = 0x61080000
        entry = step[0]
        args = list(step[1:]) + [0] * (4 - len(step[1:]))
        m._rdx, m._r8 = args[1], args[2]
        if entry == AAD0:
            r = m.aad0(args[0], args[1])
        elif entry == ABE0:
            r = m.abe0(args[0])
        elif entry == A2A0:
            r = m.a2a0(args[0], args[1], args[2])
        elif entry == C790:
            r = ("ret", m.c790(args[0], args[1], args[2]))
        elif entry == B410:
            r = ("ret", m.b410(args[0], args[1], args[2]))
        elif entry == B4E0:
            r = ("ret", m.b4e0(args[0], args[1], args[2]))
        elif entry == B490:
            r = ("ret", m.b490(args[0], args[1]))
        elif entry == B5A0:
            r = ("ret", m.b5a0(args[0], args[1]))
        elif entry == A570:
            r = m.a570(args[0], args[1], args[2])
        elif entry == A850:
            r2 = m.a850(args[0])
            r = r2 if isinstance(r2, tuple) else ("ret", r2)
        elif entry == BC60:
            r = m.bc60(*args)
        elif entry == B410:
            r = ("ret", m.b410(args[0], args[1]))
        elif entry == BASE:
            r = ("ret", m.base(args[0] & 0xFFFFFFFF))
        elif entry == C620:
            r = ("ret", m.c620(args[0] & 0xFFFFFFFF))
        elif entry == PREL:
            r = m.prel(args[0], args[1])
        elif entry == AE00:
            r2 = m.ae00(args[0], args[1])
            r = r2 if isinstance(r2, tuple) else ("ret", r2)
        elif entry == ACE0:
            r2 = m.ace0(args[0], args[1])
            r = r2 if isinstance(r2, tuple) else ("ret", r2)
        elif entry == EMIT:
            r = m.f17d2e0(args[0], args[1], args[2], args[3])
        elif entry == PINIT:
            r = m.pinit(args[0], args[1], args[2])
        elif entry == E070:
            r = m.e070()
        elif entry == EA30:
            r = m.eb70(args[0], 0)
        elif entry == EB70:
            r = m.eb70(args[0], args[1])
        elif entry == E330:
            r = m.e330(args[0])
        elif entry == E370:
            r = m.e370(args[0])
        elif entry == E3B0:
            r = m.e3b0(args[0])
        elif entry == EC40:
            r = m.ec40(args[0])
        elif entry == E810:
            r = ("ret", m.e810())
        elif entry == G8C70:
            r = ("ret", m.g8c70())
        elif entry == GE0E0:
            r = ("ret", m.ge0e0())
        elif entry == G6A0:
            r = ("ret", 0)
        elif entry == G20C0:
            r = ("ret", 0)
        elif entry == G97F0:
            r = m.g97f0(args[0], (0x61080000 - 0x1178) & 0xFFFFFFFFFFFFFFFF)
            if r is None:
                r = ("ret", 0)
        else:
            raise ValueError("bad entry %x" % entry)
        if r[0] == "ret":
            m.rets.append(r[1]); m.ends.append(RETQ)
        elif r[0] == "spin":
            m.rets.append(r[2]); m.ends.append(r[1])
        elif r[0] == "fault":
            m.faults.append(("exp", r[1])); m.rets.append(r[3])
            m.ends.append(r[2])
            break
        elif r[0] == "trap":
            m.faults.append(("trap", r[1])); m.rets.append(r[2])
            m.ends.append(r[1])
            break
    mem = {}
    for a, n in case.get("watch", []):
        mem["%x" % a] = bytes(
            m.mem.get(a + i, img_byte(raw, secs, a + i)
                      if IMG_LO <= a + i < IMG_HI else 0)
            for i in range(n)).hex()
    return {"trace": m.trace, "faults": m.faults,
            "rets": m.rets, "ends": m.ends, "mem": mem}


def differs(nat, mod):
    d = []
    for a, b in (("trace", nat["trace"] == mod["trace"]),
                 ("rets", nat["rets"] == mod["rets"]),
                 ("ends", nat["ends"] == mod["ends"]),
                 ("mem", nat["mem"] == mod["mem"])):
        if not b:
            d.append(a)
    nf, mf = nat["faults"], mod["faults"]
    if bool(nf) != bool(mf):
        d.append("faults")
    elif nf and mf:
        naddr = nf[0][1] if isinstance(nf[0][1], int) else None
        if naddr != mf[0][1]:
            d.append("faults")
    return d


# ---------------- cases ----------------
def nd(a, key, prev=0, nxt=0, pp=0, pn=0, **kw):
    kw.setdefault("next", nxt)
    kw.setdefault("pprev", pp)
    kw.setdefault("pnext", pn)
    return dict(key=key, prev=prev, **kw)

DK = DESCK
D2 = {"kind": DK, "pool": POOL, "bmap": BITMAP, "ptab": PAGETAB,
      "seq": 5, "lim": POOL + 0x180000, "bmax": 0x20}
D3 = dict(D2, itab=ITAB)
W_N1 = [(N1, 0x40)]
W_N2 = [(N2, 0x40)]
W_NP = [(NP, 0x40)]
W_P0 = [(P0, 0x40)]
W_P1 = [(P1, 0x40)]
W_P2 = [(P2, 0x40)]
W_DSC = [(DTAB + DK * 0xA8, 0x10),
         (DTAB + DK * 0xA8 + 0x30, 0x30),
         (DTAB + DK * 0xA8 + 0x60, 8),
         (DTAB + DK * 0xA8 + 0x68, 0x40),
         (DTAB + DK * 0xA8 + 0x90, 0x10)]
W_PTC = [(PTAGC, 0x20)]
W_FLG = [(FLAGG, 4)]


def cases():
    C = {}
    # ---- AAD0 ----
    C["aad0-empty"] = {
        "desc": {DK: D2}, "steps": [(AAD0, DTAB + DK * 0xA8, 0)],
        "watch": W_DSC}
    C["aad0-nobst"] = {
        "desc": {DK: dict(D2, head=N1)},
        "nodes": {N1: nd(N1, 0x80)},
        "steps": [(AAD0, DTAB + DK * 0xA8, 0)],
        "watch": W_DSC + W_N1}
    C["aad0-adopt"] = {
        # free head key 0x80; BST root P1 key==0x80, addr>head, flag4=0
        "desc": {DK: dict(D2, head=N1, tail=N1, bst=P1)},
        "nodes": {N1: nd(N1, 0x80),
                  P1: nd(P1, 0x80, f15=0, t17=3, label=b"OBJ1")},
        "qcount": 1,
        "steps": [(AAD0, DTAB + DK * 0xA8, 0)],
        "watch": W_DSC + W_N1 + W_P1 + W_PTC}
    C["aad0-descend"] = {
        # BST root key>target descends +0x24 to a matching leaf
        "desc": {DK: dict(D2, head=N1, tail=N1, bst=P1)},
        "nodes": {N1: nd(N1, 0x80),
                  P1: nd(P1, 0x200, left=P2),
                  P2: nd(P2, 0x80, t17=1, label=b"LEAF")},
        "steps": [(AAD0, DTAB + DK * 0xA8, 0)],
        "watch": W_DSC + W_N1 + W_P2 + W_PTC}
    C["aad0-nomatch"] = {
        # only BST key < head key -> dead candidate tracking, ret 0
        "desc": {DK: dict(D2, head=N1, tail=N1, bst=P1)},
        "nodes": {N1: nd(N1, 0x80), P1: nd(P1, 0x40)},
        "steps": [(AAD0, DTAB + DK * 0xA8, 0)],
        "watch": W_DSC + W_N1 + W_P1}
    C["aad0-below-head"] = {
        # matching key but addr <= head -> ineligible
        "desc": {DK: dict(D2, head=N3, tail=N3, bst=P1)},
        "nodes": {N3: nd(N3, 0x80), P1: nd(P1, 0x80)},
        "steps": [(AAD0, DTAB + DK * 0xA8, 0)],
        "watch": W_DSC + [(N3, 0x40)] + W_P1}
    C["aad0-flag4"] = {
        # matching key+addr but f15&4 -> ineligible
        "desc": {DK: dict(D2, head=N1, tail=N1, bst=P1)},
        "nodes": {N1: nd(N1, 0x80), P1: nd(P1, 0x80, f15=4)},
        "steps": [(AAD0, DTAB + DK * 0xA8, 0)],
        "watch": W_DSC + W_N1 + W_P1}
    C["aad0-repeat"] = {
        # edx!=0: after adopt re-reads head; second head N2 also matches
        "desc": {DK: dict(D2, head=N1, tail=N2, bst=P1)},
        "nodes": {N1: nd(N1, 0x80, next=N2),
                  N2: nd(N2, 0x80, prev=N1, pprev=N1, pnext=0),
                  P1: nd(P1, 0x80, right=P2, t17=2, label=b"R1"),
                  P2: nd(P2, 0x80, parent=P1, t17=4, label=b"R2")},
        "steps": [(AAD0, DTAB + DK * 0xA8, 1)],
        "watch": W_DSC + W_N1 + W_N2 + W_P1 + W_P2 + W_PTC}
    # ---- ABE0 ----
    C["abe0-empty"] = {
        "desc": {DK: D2}, "steps": [(ABE0, DTAB + DK * 0xA8)],
        "watch": W_DSC}
    C["abe0-nophysnext"] = {
        "desc": {DK: dict(D2, head=N1, tail=N1)},
        "nodes": {N1: nd(N1, 0x80)},
        "steps": [(ABE0, DTAB + DK * 0xA8)],
        "watch": W_DSC + W_N1}
    C["abe0-skip-f2"] = {
        # phys-next f15&6==2 but f14&1 clear -> ret 0, scan aborted
        "desc": {DK: dict(D2, head=N1, tail=N1, bst=P1)},
        "nodes": {N1: nd(N1, 0x80, pnext=N2),
                  N2: nd(N2, 0x80, f15=2),
                  P1: nd(P1, 0x80, t17=5, label=b"SC")},
        "steps": [(ABE0, DTAB + DK * 0xA8)],
        "watch": W_DSC + W_N1 + W_N2 + W_P1 + W_PTC}
    C["abe0-f4direct"] = {
        # phys-next f15=4 -> native &6==4 != 2 -> scan arm;
        # the cmp-al-2->4 mutant takes the flag arm instead
        "desc": {DK: dict(D2, head=N1, tail=N1)},
        "nodes": {N1: nd(N1, 0x80, pnext=NP),
                  NP: nd(NP, 0x80, f14=1, f15=4)},
        "steps": [(ABE0, DTAB + DK * 0xA8)],
        "watch": W_DSC + W_N1 + W_NP}
    C["abe0-adopt"] = {
        "desc": {DK: dict(D2, head=N1, tail=N1, bst=P1)},
        "nodes": {N1: nd(N1, 0x80, pnext=N2),
                  N2: nd(N2, 0x80, f15=0),
                  P1: nd(P1, 0x80, t17=1, label=b"AD")},
        "steps": [(ABE0, DTAB + DK * 0xA8)],
        "watch": W_DSC + W_N1 + W_N2 + W_P1 + W_PTC}
    C["abe0-stale-rbx"] = {
        # flag arm: phys-next N2 IS the adoption src (r8 survives;
        # jne skips the mov r8,rbx reload) - N2 moves into N1
        "desc": {DK: dict(D2, head=N1, tail=N1)},
        "nodes": {N1: nd(N1, 0x80, pnext=N2),
                  N2: nd(N2, 0x80, f14=1, f15=2, t17=2, label=b"MV")},
        "steps": [(ABE0, DTAB + DK * 0xA8)],
        "watch": W_DSC + W_N1 + W_N2 + W_PTC}
    C["abe0-walk"] = {
        # iter1: NP f15=6 -> &6!=2 -> scan misses -> advance.
        # iter2: N3 f15=4 -> &6!=2 -> scan hits P1 -> adopt, ret 1
        "desc": {DK: dict(D2, head=N1, tail=N2, bst=P1)},
        "nodes": {N1: nd(N1, 0x40, next=N2, pnext=NP),
                  NP: nd(NP, 0x40, f15=6),
                  N2: nd(N2, 0x80, prev=N1, pnext=N3),
                  N3: nd(N3, 0x80, f15=4),
                  P1: nd(P1, 0x80, t17=2, label=b"W")},
        "steps": [(ABE0, DTAB + DK * 0xA8)],
        "watch": W_DSC + W_N1 + W_NP + W_N2 + [(N3, 0x40)] + W_P1 + W_PTC}
    # ---- A2A0 direct ----
    C["a2a0-basic"] = {
        # src P1 f15&2 set -> C790 unlink; free node N1 carved ctx-path
        "desc": {DK: dict(D2, head=N1, tail=N1, bst=P1)},
        "nodes": {N1: nd(N1, 0x200, tag=9),
                  P1: nd(P1, 0x80, f14=1, f15=2|8, tag=7, t17=3,
                         w1e=0x1234, d30=0xABCD, label=b"MOVER")},
        "ptagc": {3: 0x100},
        "steps": [(A2A0, DTAB + DK * 0xA8, N1, P1)],
        "watch": W_DSC + W_N1 + W_P1 + W_PTC}
    C["a2a0-nobst"] = {
        # f15&2 clear: no unlink, no reinsert
        "desc": {DK: dict(D2, head=N1, tail=N1)},
        "nodes": {N1: nd(N1, 0x100, tag=4),
                  P1: nd(P1, 0x60, f14=1, f15=0, tag=2, t17=0,
                         label=b"NB")},
        "ptagc": {0: 0x50},
        "steps": [(A2A0, DTAB + DK * 0xA8, N1, P1)],
        "watch": W_DSC + W_N1 + W_P1 + W_PTC}
    C["a2a0-chained"] = {
        # src has l20 prev P2 -> rbx splices into the threaded chain
        "desc": {DK: dict(D2, head=N1, tail=N1, bst=P1)},
        "nodes": {N1: nd(N1, 0x200, tag=1),
                  P1: nd(P1, 0x80, f14=1, f15=2, t17=1, l20=P2,
                         label=b"CN"),
                  P2: nd(P2, 0x60, f14=1, f15=2, t17=1, seq=0x77)},
        "ptagc": {1: 0x20},
        "steps": [(A2A0, DTAB + DK * 0xA8, N1, P1)],
        "watch": W_DSC + W_N1 + W_P1 + W_P2 + W_PTC}
    C["a2a0-nullsrc"] = {
        # r8=0 -> first src deref b[0x14] faults
        "desc": {DK: dict(D2, head=N1, tail=N1)},
        "nodes": {N1: nd(N1, 0x100)},
        "steps": [(A2A0, DTAB + DK * 0xA8, N1, 0)],
        "watch": W_DSC + W_N1}
    # ---- C790/B410/B4E0/B490 direct ----
    C["c790-root-both"] = {
        # root with both subtrees: right promotes, left re-attached
        "desc": {DK: dict(D2, bst=P1)},
        "nodes": {P1: nd(P1, 0x80, left=P2, right=P3),
                  P2: nd(P2, 0x40, parent=P1),
                  P3: nd(P3, 0xC0, parent=P1)},
        "steps": [(C790, DTAB + DK * 0xA8, P1, 0x14B6)],
        "watch": W_DSC + W_P1 + W_P2 + [(P3, 0x40)]}
    C["c790-root-left"] = {
        "desc": {DK: dict(D2, bst=P1)},
        "nodes": {P1: nd(P1, 0x80, left=P2),
                  P2: nd(P2, 0x40, parent=P1)},
        "steps": [(C790, DTAB + DK * 0xA8, P1, 0)],
        "watch": W_DSC + W_P1 + W_P2}
    C["c790-root-null"] = {
        "desc": {DK: dict(D2, bst=P1)},
        "nodes": {P1: nd(P1, 0x80)},
        "steps": [(C790, DTAB + DK * 0xA8, P1, 0)],
        "watch": W_DSC + W_P1}
    C["c790-child-right"] = {
        # P1 is left child of P2, has right child P3 + left P4
        "desc": {DK: dict(D2, bst=P2)},
        "nodes": {P2: nd(P2, 0x80, left=P1),
                  P1: nd(P1, 0x40, parent=P2, left=P4, right=P3),
                  P4: nd(P4, 0x20, parent=P1),
                  P3: nd(P3, 0x60, parent=P1)},
        "steps": [(C790, DTAB + DK * 0xA8, P1, 0)],
        "watch": W_DSC + W_P1 + W_P2 + [(P3, 0x40)] + [(P4, 0x40)]}
    C["c790-child-leftonly"] = {
        # P1 is RIGHT child of P2, left subtree only -> B490 writes
        # parent's +0x24 (the asymmetric arm)
        "desc": {DK: dict(D2, bst=P2)},
        "nodes": {P2: nd(P2, 0x40, right=P1),
                  P1: nd(P1, 0x80, parent=P2, left=P3),
                  P3: nd(P3, 0x60, parent=P1)},
        "steps": [(C790, DTAB + DK * 0xA8, P1, 0)],
        "watch": W_DSC + W_P1 + W_P2 + [(P3, 0x40)]}
    C["b410-root"] = {
        "desc": {DK: D2},
        "nodes": {P1: nd(P1, 0x80, l20=0xDEAD, left=0xBEEF,
                         right=0xCAFE, parent=0xF00D)},
        "steps": [(B410, DTAB + DK * 0xA8, P1)],
        "watch": W_DSC + W_P1}
    C["b410-descend"] = {
        # root key 0x80, node key 0x40 -> lands as +0x24 of root
        "desc": {DK: dict(D2, bst=P1)},
        "nodes": {P1: nd(P1, 0x80), P2: nd(P2, 0x40)},
        "steps": [(B410, DTAB + DK * 0xA8, P2)],
        "watch": W_DSC + W_P1 + W_P2}
    C["b4e0-right"] = {
        # anchor key 0x40, node key 0x80 -> +0x28 insert
        "nodes": {P1: nd(P1, 0x40), P2: nd(P2, 0x80)},
        "steps": [(B4E0, P1, P2, 0x50E)],
        "watch": W_P1 + W_P2}
    C["b4e0-eq"] = {
        # anchor.key <= node.key -> right; equality goes right too
        "nodes": {P1: nd(P1, 0x80), P2: nd(P2, 0x80)},
        "steps": [(B4E0, P1, P2, 0)],
        "watch": W_P1 + W_P2}
    C["b4e0-deep"] = {
        # descend two levels: root 0x80 -> left 0x40; node 0x60 -> +0x28 of 0x40
        "nodes": {P1: nd(P1, 0x80, left=P2),
                  P2: nd(P2, 0x40, parent=P1),
                  P3: nd(P3, 0x60)},
        "steps": [(B4E0, P1, P3, 0)],
        "watch": W_P1 + W_P2 + [(P3, 0x40)]}
    C["b490-force"] = {
        "nodes": {P1: nd(P1, 0x80, left=0x1234),
                  P2: nd(P2, 0x40, parent=0x5678)},
        "steps": [(B490, P1, P2)],
        "watch": W_P1 + W_P2}
    C["b5a0-force"] = {
        "nodes": {P1: nd(P1, 0x80, right=0x1234),
                  P2: nd(P2, 0x40, parent=0x5678)},
        "steps": [(B5A0, P1, P2)],
        "watch": W_P1 + W_P2}
    # ---- A570 ----
    C["a570-maskclr"] = {
        "desc": {DK: D3}, "mask": 0,
        "steps": [(A570, DK, 0x3F, 0)],
        "watch": W_DSC}
    C["a570-kind-hi"] = {
        # kind>0xE -> desc=0 -> q[0x10] fault
        "desc": {DK: D3}, "mask": 1 << DK,
        "steps": [(A570, 0xF, 1, 0)],
        "watch": W_DSC}
    C["a570-poolwalk"] = {
        # &1: pool block self-loops via +8; w1e!=0 (label empty) prints
        # through the hook; FLAGG=-1 exercises the hook's cmove arm
        "desc": {DK: dict(D3, pool=P0)},
        "mask": 1 << DK, "flagg": 0xFFFFFFFF,
        "nodes": {P0: nd(P0, 0x80, f14=1, f15=2|8, b2=7, w1e=0x1234,
                         next=P0, pnext=P1),
                  P1: nd(P1, 0x40, f14=1, f15=0, b2=9,
                         next=P1, label=b"L2")},
        "steps": [(A570, DK, 1, 7)],
        "watch": W_DSC + W_P0 + W_P1 + W_FLG}
    C["a570-freewalk"] = {
        # &2: free list N1->N2->self terminates
        "desc": {DK: dict(D3, head=N1, tail=N2)},
        "mask": 1 << DK,
        "nodes": {N1: nd(N1, 0x80, next=N2),
                  N2: nd(N2, 0x40, prev=N1, next=N2)},
        "steps": [(A570, DK, 2, 0)],
        "watch": W_DSC + W_N1 + W_N2}
    C["a570-itabA"] = {
        # &8: chain at desc+0x48 walks entries by next-idx
        "desc": {DK: dict(D3, chA=ITAB)},
        "mask": 1 << DK,
        "itab": {0: {"n": 1, "p": 1}, 1: {"n": 2, "p": 1},
                 2: {"n": 0xFFFF, "p": 1}},
        "steps": [(A570, DK, 8, 0)],
        "watch": W_DSC + [(ITAB, 0x40)]}
    C["a570-itabB"] = {
        # &0x10: chain at desc+0x40; q[+8]==0 does NOT stop it here
        "desc": {DK: dict(D3, chB=ITAB)},
        "mask": 1 << DK,
        "itab": {0: {"n": 1, "p": 0}, 1: {"n": 0xFFFF, "p": 0}},
        "steps": [(A570, DK, 0x10, 0)],
        "watch": W_DSC + [(ITAB, 0x40)]}
    C["a570-bstwalk"] = {
        # &0x20: A850 in-order over the BST (no observable output;
        # case pins clean return over a 3-node tree)
        "desc": {DK: dict(D3, bst=P1)},
        "mask": 1 << DK,
        "nodes": {P1: nd(P1, 0x80, left=P2, right=P3),
                  P2: nd(P2, 0x40, parent=P1, f14=1, f15=8),
                  P3: nd(P3, 0xC0, parent=P1, f14=1, f15=5)},
        "steps": [(A570, DK, 0x20, 0)],
        "watch": W_DSC + W_P1 + W_P2 + [(P3, 0x40)]}
    C["a570-sel-free"] = {
        # free node + esi>=0 -> no print; sel<0 would print
        "desc": {DK: dict(D3, pool=P0)},
        "mask": 1 << DK,
        "nodes": {P0: nd(P0, 0x80, f14=0, next=P0, label=b"X")},
        "steps": [(A570, DK, 1, 3)],
        "watch": W_DSC + W_P0}
    C["a570-neg-sel"] = {
        # esi<0 prints both alloc and free nodes; P0's +8 points at P1
        # (not self) so the walk advances via +0x10
        "desc": {DK: dict(D3, pool=P0)},
        "mask": 1 << DK,
        "nodes": {P0: nd(P0, 0x80, f14=0, pnext=P1, next=P1,
                         label=b"F1"),
                  P1: nd(P1, 0x40, f14=1, f15=1, next=P1,
                         label=b"A2")},
        "steps": [(A570, DK, 1, 0xFFFFFFFF)],
        "watch": W_DSC + W_P0 + W_P1 + W_FLG}
    C["a570-kindE"] = {
        # kind==0xE is in range (bound is <=0xE)
        "desc": {0xE: dict(D3)},
        "mask": 1 << 0xE,
        "steps": [(A570, 0xE, 0x2, 0)],
        "watch": [(DTAB + 0xE * 0xA8, 0x10)]}
    C["a850-leftdangle"] = {
        # BST left subtree dangles -> A850 faults on its flag read
        "desc": {DK: dict(D3, bst=P1)},
        "mask": 1 << DK,
        "nodes": {P1: nd(P1, 0x80, left=0xDEADBEE0, f14=1, f15=8)},
        "steps": [(A570, DK, 0x20, 0)],
        "watch": W_DSC + W_P1}
    C["a850-leaf"] = {
        "nodes": {P1: nd(P1, 0x80, f14=1, f15=0xF)},
        "steps": [(A850, P1)],
        "watch": W_P1}
    # ================= EXP-126: free path =================
    # PREL(rcx=payload ptr, rdx=aux dump region)
    C["prel-null"] = {
        "steps": [(PREL, 0, 0)], "watch": W_DSC}
    C["prel-misalign"] = {
        # r14b&3 -> emit "%p might be MHANDLE" -> ret emit residual
        "steps": [(PREL, N1 + 0x42, N2)],
        "watch": W_DSC}
    C["prel-misalign-neg"] = {
        # FLAGG=-1 -> FLAG ret 2 -> emit ret 2
        "flagg": 0xFFFFFFFF,
        "steps": [(PREL, N1 + 0x41, N2)],
        "watch": W_DSC + W_FLG}
    C["prel-free-phys-below"] = {
        # phys-prev NP free -> B670 splice-after
        "desc": {DK: D2},
        "nodes": {NP: nd(NP, 0x40, pnext=N1),
                  N1: nd(N1, 0x80, f14=1, pprev=NP, tag=3)},
        "steps": [(PREL, N1 + 0x40, 0)],
        "watch": W_DSC + W_NP + W_N1}
    C["prel-free-phys-above"] = {
        # phys-next N2 free -> B730 splice-before
        "desc": {DK: D2},
        "nodes": {N1: nd(N1, 0x80, f14=1, pnext=N2, tag=5),
                  N2: nd(N2, 0x100, pprev=N1)},
        "steps": [(PREL, N1 + 0x40, 0)],
        "watch": W_DSC + W_N1 + W_N2}
    C["prel-free-phys-both"] = {
        # phys-prev AND phys-next free, all three linked list-1:
        # prev arm wins (B670), B210 merges all three physically-
        # adjacent blocks through the relink chain
        "desc": {DK: D2},
        "nodes": {NP: nd(NP, 0x40, pnext=N1, next=N2),
                  N1: nd(N1, 0x80, f14=1, pprev=NP, pnext=N2),
                  N2: nd(N2, 0x100, pprev=N1, prev=NP)},
        "steps": [(PREL, N1 + 0x40, 0)],
        "watch": W_DSC + W_NP + W_N1 + W_N2}
    C["prel-free-ae00"] = {
        # no free phys neighbours, rbx < lim -> AE00 finds the
        # free-below via ptab[0]=NP, splices N1 after it
        "desc": {DK: D2},
        "nodes": {N1: nd(N1, 0x80, f14=1, pprev=NP, pnext=N2),
                  NP: nd(NP, 0x40, f14=1),   # alloc'd -> not free
                  N2: nd(N2, 0x40, f14=1),
                  P0: nd(P0, 0x40)},
        "ptab": {0: P0}, "bmap": {0: 1},
        "steps": [(PREL, N1 + 0x40, 0)],
        "watch": W_DSC + W_N1 + W_P0}
    C["prel-free-ace0"] = {
        # rbx >= lim -> ACE0 arm: find free-above via ptab, splice before
        "desc": {DK: dict(D2, lim=POOL)},
        "nodes": {N1: nd(N1, 0x80, f14=1, pprev=NP, pnext=N2),
                  NP: nd(NP, 0x40, f14=1),
                  N2: nd(N2, 0x40, f14=1),
                  P1: nd(P1, 0x40)},
        "ptab": {4: P1}, "bmap": {0: 1 << 4},
        "steps": [(PREL, N1 + 0x40, 0)],
        "watch": W_DSC + W_N1 + W_P1}
    C["prel-free-ae00-miss"] = {
        # below-bound arm: AE00 misses (pprev=0), ACE0 finds P1
        # above -> B730(P1,N1) splice
        "desc": {DK: D2},
        "nodes": {N1: nd(N1, 0x80, f14=1, pnext=N2),
                  N2: nd(N2, 0x40, f14=1),
                  P1: nd(P1, 0x40)},
        "ptab": {4: P1}, "bmap": {0: 1 << 4},
        "steps": [(PREL, N1 + 0x40, 0)],
        "watch": W_DSC + W_N1 + W_P1}
    C["prel-free-bothdir"] = {
        # free below AND above reachable via ptab, rbx < lim:
        # correct -> AE00-first -> B670(P0,N1); the bound-flip
        # mutant takes ACE0-first -> B730(P1,N1)
        "desc": {DK: D2},
        "nodes": {N1: nd(N1, 0x80, f14=1, pprev=NP, pnext=N2),
                  NP: nd(NP, 0x40, f14=1),
                  N2: nd(N2, 0x40, f14=1),
                  P0: nd(P0, 0x40),
                  P1: nd(P1, 0x40)},
        "ptab": {0: P0, 4: P1}, "bmap": {0: 0x11},
        "steps": [(PREL, N1 + 0x40, 0)],
        "watch": W_DSC + W_N1 + W_P0 + W_P1}
    C["prel-free-skip-below"] = {
        # AE00's found == stale d[+4] link -> skip splice entirely
        "desc": {DK: D2},
        "nodes": {N1: nd(N1, 0x80, f14=1, pprev=NP, prev=P0),
                  NP: nd(NP, 0x40, f14=1),
                  P0: nd(P0, 0x40)},
        "ptab": {0: P0}, "bmap": {0: 1},
        "steps": [(PREL, N1 + 0x40, 0)],
        "watch": W_DSC + W_N1 + W_P0}
    C["prel-free-skip-above"] = {
        # bound arm: ACE0's found == stale d[+8] -> fall to AE00
        "desc": {DK: dict(D2, lim=POOL)},
        "nodes": {N1: nd(N1, 0x80, f14=1, pnext=N2, next=P1),
                  N2: nd(N2, 0x40, f14=1),
                  P1: nd(P1, 0x40)},
        "ptab": {4: P1}, "bmap": {0: 1 << 4},
        "steps": [(PREL, N1 + 0x40, 0)],
        "watch": W_DSC + W_N1 + W_P1}
    C["prel-free-empty"] = {
        # no free anything: splice skipped, B210 roots -> head=tail=N1,
        # B5F0 page-head insert at slot 0
        "desc": {DK: D2},
        "nodes": {N1: nd(N1, 0x80, f14=1)},
        "steps": [(PREL, N1 + 0x40, 0)],
        "watch": W_DSC + W_N1}
    C["prel-free-coalesce"] = {
        # phys-prev free AND adjacent -> B210 merges NP+N1 forward;
        # page-head slot 0 tracks the merged block
        "desc": {DK: dict(D2, head=NP, tail=NP)},
        "nodes": {NP: nd(NP, 0x40, pnext=N1, next=0),
                  N1: nd(N1, 0x80, f14=1, pprev=NP)},
        "steps": [(PREL, N1 + 0x40, 0)],
        "watch": W_DSC + W_NP + W_N1}
    C["prel-free-subctr"] = {
        # b[+0x17]=7 -> d[PTAGC+7*4] decremented by key too
        "desc": {DK: dict(D2, use={3: 0x300})},
        "ptagc": {7: 0x50},
        "nodes": {N1: nd(N1, 0x80, f14=1, tag=3, t17=7,
                         label=b"ABCDEFGHIJKL", w1e=0x99, d30=0x55)},
        "steps": [(PREL, N1 + 0x40, 0)],
        "watch": W_DSC + W_N1 + W_PTC}
    C["prel-free-badkind"] = {
        # kind>=0xF -> desc=0 -> b[2] write faults at 0x2
        "desc": {DK: D2},
        "nodes": {N1: nd(N1, 0x80, f14=1, kind=0xF)},
        "steps": [(PREL, N1 + 0x40, 0)],
        "watch": W_DSC + W_N1}
    C["prel-mark"] = {
        # w[+0x3E]!=0 -> emit MCB + ST_W write + A570 + hook + int3
        "desc": {DK: D3}, "mask": 1 << DK,
        "nodes": {N1: nd(N1, 0x80, f14=1, w3e=0x1234)},
        "steps": [(PREL, N1 + 0x40, 0)],
        "watch": W_DSC + W_N1 + [(ST_W, 8)]}
    C["prel-badmagic"] = {
        # bad magic -> dual dump + emit + A570 + hook + int3.
        # r15=N2 mapped aux so both dump loops complete.
        "desc": {DK: D3}, "mask": 1 << DK,
        "nodes": {N1: nd(N1, 0x80, f14=1, magic=0xDEAD),
                  N2: nd(N2, 0x40)},
        "steps": [(PREL, N1 + 0x40, N2)],
        "watch": W_DSC + W_N1 + [(ST_W, 8),
                 (STACK + 0x7EFC8, 0x30)]}   # rsp+0x140 dump buf
    C["prel-badmagic-nor15"] = {
        # r15=0 -> aux-dump loop faults reading b[0]
        "desc": {DK: D3}, "mask": 1 << DK,
        "nodes": {N1: nd(N1, 0x80, f14=1, magic=0xDEAD)},
        "steps": [(PREL, N1 + 0x40, 0)],
        "watch": W_DSC + W_N1}
    C["prel-alreadyfree"] = {
        # f14&1 clear -> emit "Allready Free" -> ret emit residual
        "desc": {DK: D2},
        "nodes": {N1: nd(N1, 0x80, f14=0)},
        "steps": [(PREL, N1 + 0x40, 0)],
        "watch": W_DSC + W_N1}
    C["prel-chkstk"] = {
        # teblim high -> _chkstk probes touch 0x6107F000/0x6107E000
        "teblim": STACK + 0x80000,
        "desc": {DK: D2},
        "nodes": {N1: nd(N1, 0x80, f14=1),
                  STACK + 0x7F000: nd(STACK + 0x7F000, 0x40),
                  STACK + 0x7E000: nd(STACK + 0x7E000, 0x40)},
        "steps": [(PREL, N1 + 0x40, 0)],
        "watch": W_DSC + W_N1 + [(STACK + 0x7F000, 4),
                                (STACK + 0x7E000, 4)]}
    # ---- AE00/ACE0 direct ----
    C["ae00-nopp"] = {
        # phys_prev=0 -> ret 0
        "desc": {DK: D2},
        "nodes": {N1: nd(N1, 0x80)},
        "steps": [(AE00, DTAB + DK * 0xA8, N1)],
        "watch": W_N1}
    C["ae00-below"] = {
        # ptab[0]=NP -> walk +8 while next<=node: NP->NP2 both <= N1
        "desc": {DK: D2},
        "nodes": {N1: nd(N1, 0x80, pprev=NP),
                  NP: nd(NP, 0x40, next=POOL + 0x900),
                  POOL + 0x900: nd(POOL + 0x900, 0x40)},
        "ptab": {0: NP}, "bmap": {0: 1},
        "steps": [(AE00, DTAB + DK * 0xA8, N1)],
        "watch": W_N1 + W_NP + [(POOL + 0x900, 0x40)]}
    C["ae00-head-ge"] = {
        # ptab head >= node -> descent falls off -> ret 0
        "desc": {DK: D2},
        "nodes": {N1: nd(N1, 0x80, pprev=NP)},
        "ptab": {0: N2}, "bmap": {0: 1},
        "steps": [(AE00, DTAB + DK * 0xA8, N1)],
        "watch": W_N1}
    C["ae00-nobit"] = {
        # bitmap empty below -> r8 goes negative -> ret 0
        "desc": {DK: D2},
        "nodes": {N1: nd(N1, 0x80, pprev=NP)},
        "steps": [(AE00, DTAB + DK * 0xA8, N1)],
        "watch": W_N1}
    C["ae00-masked-bit"] = {
        # only bit 4 set (above slot 0) -> masked out -> scan down ->
        # ret 0; an unmasked mutant keeps the bit -> walk finds NP
        "desc": {DK: D2},
        "nodes": {N1: nd(N1, 0x80, pprev=NP),
                  NP: nd(NP, 0x40)},
        "ptab": {0: NP}, "bmap": {0: 1 << 4},
        "steps": [(AE00, DTAB + DK * 0xA8, N1)],
        "watch": W_N1}
    C["ae00-nopp-scan"] = {
        # phys_prev=0 -> correct ret 0; the or-r8d,0 mutant proceeds
        # to scan slot 0 and finds NP
        "desc": {DK: D2},
        "nodes": {N1: nd(N1, 0x80),
                  NP: nd(NP, 0x40)},
        "ptab": {0: NP}, "bmap": {0: 1},
        "steps": [(AE00, DTAB + DK * 0xA8, N1)],
        "watch": W_N1}
    C["ae00-slot2"] = {
        # phys_prev at 0x18000 -> slot 1 (d+0xFFFF-truncated sar16);
        # sar-0x20 mutant computes slot 0 -> different walk start
        "desc": {DK: D2},
        "nodes": {N1: nd(N1, 0x80, pprev=N3B),
                  NP: nd(NP, 0x40)},
        "ptab": {1: NP}, "bmap": {0: 2},
        "steps": [(AE00, DTAB + DK * 0xA8, N1)],
        "watch": W_N1}
    C["ae00-mask-hi"] = {
        # slot 0x21: bit idx 1 with &0x1F -> mask keeps bit2 off ->
        # ret 0; &0x3F mutant makes r11d=0x21>=0x1F -> no mask ->
        # w=4 -> head-walk at slot 0x21 -> ret NP
        "desc": {DK: D2},
        "nodes": {N1: nd(N1, 0x80, pprev=POOL + 0x210000),
                  NP: nd(NP, 0x40)},
        "ptab": {0x21: NP}, "bmap": {1: 4},
        "steps": [(AE00, DTAB + DK * 0xA8, N1)],
        "watch": W_N1}
    C["ace0-nopn"] = {
        "desc": {DK: D2},
        "nodes": {N1: nd(N1, 0x80)},
        "steps": [(ACE0, DTAB + DK * 0xA8, N1)],
        "watch": W_N1}
    C["ace0-above"] = {
        # ptab[4]=P1 > N1 -> found; prev-walk returns smallest >= N1
        "desc": {DK: D2},
        "nodes": {N1: nd(N1, 0x80, pnext=N2),
                  N2: nd(N2, 0x40, f14=1),
                  P1: nd(P1, 0x40, prev=P2),
                  P2: nd(P2, 0x40)},
        "ptab": {4: P1}, "bmap": {0: 1 << 4},
        "steps": [(ACE0, DTAB + DK * 0xA8, N1)],
        "watch": W_N1 + W_P1 + W_P2}
    C["ace0-bound"] = {
        # pslot >= bmax(0) -> ret 0 before any scan; the +0x50
        # mutant reads bound=P1(0x30040000) instead -> scans and
        # finds P1 via ptab[4]
        "desc": {DK: dict(D2, bmax=0, bst=P1)},
        "nodes": {N1: nd(N1, 0x80, pnext=N2),
                  N2: nd(N2, 0x40),
                  P1: nd(P1, 0x40)},
        "ptab": {4: P1}, "bmap": {0: 1 << 4},
        "steps": [(ACE0, DTAB + DK * 0xA8, N1)],
        "watch": W_N1}
    C["ace0-masked-below"] = {
        # only bit0 set (below pslot 1) -> masked out -> word1 scan
        # finds nothing (bmap[1]=0) -> ret 0; unmasked mutant keeps
        # bit0 -> head-walk starts at slot1 -> ptab[1]=P3 -> ret P3
        "desc": {DK: D2},
        "nodes": {N1: nd(N1, 0x80, pnext=POOL + 0x11000),
                  P3: nd(P3, 0x40)},
        "ptab": {1: P3}, "bmap": {0: 1},
        "steps": [(ACE0, DTAB + DK * 0xA8, N1)],
        "watch": W_N1}
    # ---- EMIT / PINIT direct ----
    C["emit-basic"] = {
        # F17D2E0 real: GETOBJ leaf -> cell -> FLAG; ret flag resid
        "steps": [(EMIT, HEAP + 0x50000, F_MHAND)],
        "watch": W_FLG}
    C["emit-neg"] = {
        # FLAGG=-1 -> FLAG ret 2 -> emit ret 2 (cmovs dead)
        "flagg": 0xFFFFFFFF,
        "steps": [(EMIT, HEAP + 0x50000, F_MHAND)],
        "watch": W_FLG}
    C["emit-obj"] = {
        # emitobj planted -> rcx = obj|1 at the hook (unobservable
        # payload but pinned via real path)
        "emitobj": HEAP + 0x51000,
        "steps": [(EMIT, HEAP + 0x50000, F_HEX)],
        "watch": W_FLG}
    C["pinit-copy"] = {
        "nodes": {N1: nd(N1, 0x80), N2: nd(N2, 0x80)},
        "steps": [(PINIT, N2 + 0x40, N1 + 0x40, 0x30)],
        "watch": [(N2 + 0x40, 0x30), (N1 + 0x40, 0x30)]}
    C["pinit-zero"] = {
        "steps": [(PINIT, N1 + 0x40, N2 + 0x40, 0)],
        "watch": []}
    C["pinit-neg"] = {
        # movsxd r8d<0 -> huge count -> first unmapped byte faults
        "nodes": {N1: nd(N1, 0x80)},
        "steps": [(PINIT, N1 + 0x40, N2 + 0x40, 0xFFFFFFFF)],
        "watch": W_N1}
    # ================= EXP-128: poll-pump layer =================
    W_T1, W_T2, W_T3, W_T4 = ([(t, 0x78)] for t in (T1, T2, T3, T4))
    W_GLB = [(TASKG, 8), (TASKH, 8), (TASKI, 8)]
    # ---- tick/poll leaves ----
    C["e810-tick"] = {
        "tickq": 0x1234,
        "steps": [(E810, 0)],
        "watch": [(TICKQ, 8)]}
    C["g8c70-read"] = {
        "tickd": 0x77,
        "steps": [(G8C70, 0)],
        "watch": [(TICKD, 4)]}
    C["ge0e0-read"] = {
        "flagg": 0x55,
        "steps": [(GE0E0, 0)],
        "watch": W_FLG}
    C["g6a0-leaf"] = {"steps": [(G6A0, 0)], "watch": []}
    C["g20c0-leaf"] = {"steps": [(G20C0, 0)], "watch": []}
    # ---- G97F0 free-if-nonnull ----
    C["g97f0-null"] = {
        "steps": [(G97F0, 0)],
        "watch": []}
    C["g97f0-free"] = {
        # rcx!=0 -> tail into real PREL: frees N1's payload
        "desc": {DK: D2},
        "nodes": {N1: nd(N1, 0x80, f14=1)},
        "steps": [(G97F0, N1 + 0x40)],
        "watch": W_DSC + W_N1}
    # ---- E330/E370 retire helpers ----
    C["e330-cb"] = {
        # cb40 planted: (d60, q70, r8=1); b21!=0xFF -> ret cb ret
        "cb40ret": 0x42,
        "tasks": {T1: {"cb40": CB40, "d60": 0x11, "q70": 0x2222}},
        "steps": [(E330, T1)],
        "watch": W_T1}
    C["e330-nocb"] = {
        "tasks": {T1: {}},
        "steps": [(E330, T1)],
        "watch": W_T1}
    C["e330-free"] = {
        # b21==0xFF -> 3697F0(sx32(d24)) -> real PREL frees N1
        "desc": {DK: D2},
        "nodes": {N1: nd(N1, 0x80, f14=1)},
        "tasks": {T1: {"b21": 0xFF, "d24": N1 + 0x40}},
        "steps": [(E330, T1)],
        "watch": W_T1 + W_DSC + W_N1}
    C["e330-nullfree"] = {
        # b21==0xFF + d24=0 -> g97f0's null guard -> plain ret
        "tasks": {T1: {"b21": 0xFF, "d24": 0}},
        "steps": [(E330, T1)],
        "watch": W_T1}
    C["e370-cb"] = {
        # cb40 + d28==-1 -> callback with r8=0
        "cb40ret": 7,
        "tasks": {T1: {"cb40": CB40, "d28": -1, "d60": 0x22,
                       "q70": 0x3333}},
        "steps": [(E370, T1)],
        "watch": W_T1}
    C["e370-gated"] = {
        # cb40 planted but d28!=-1 -> callback skipped
        "tasks": {T1: {"cb40": CB40, "d28": 5}},
        "steps": [(E370, T1)],
        "watch": W_T1}
    C["e370-free"] = {
        "desc": {DK: D2},
        "nodes": {N1: nd(N1, 0x80, f14=1)},
        "tasks": {T1: {"cb40": CB40, "d28": -1, "b21": 0xFF,
                       "d24": N1 + 0x40}},
        "steps": [(E370, T1)],
        "watch": W_T1 + W_DSC + W_N1}
    # ---- E3B0 progress-callback wrapper ----
    C["e3b0-null"] = {
        # q[+0x50]==0 -> ret 1 (the mov eax,1 arm)
        "tasks": {T1: {}},
        "steps": [(E3B0, T1)],
        "watch": W_T1}
    C["e3b0-ok"] = {
        # ret 2 inside {1,2,3} -> no yield
        "cb50ret": 2,
        "tasks": {T1: {"cb50": CB50}},
        "steps": [(E3B0, T1)],
        "watch": W_T1}
    C["e3b0-yield"] = {
        # ret 9 -> eax-1=8 >u 2 -> real 8620C0 yield, ret 9
        "cb50ret": 9,
        "tasks": {T1: {"cb50": CB50}},
        "steps": [(E3B0, T1)],
        "watch": W_T1}
    # ---- EC40 unlink + idle push ----
    C["ec40-sole"] = {
        # sole task: both cells = T1 -> unlink -> both 0; push idle
        "taskg": T1, "taskh": T1,
        "tasks": {T1: {}},
        "steps": [(EC40, T1)],
        "watch": W_GLB + W_T1}
    C["ec40-mid"] = {
        # T1<->T2<->T3: unlink T2; head/tail cells unchanged
        "taskg": T3, "taskh": T1,
        "tasks": {T1: {"next": T2},
                  T2: {"prev": T1, "next": T3},
                  T3: {"prev": T2}},
        "steps": [(EC40, T2)],
        "watch": W_GLB + W_T1 + W_T2 + W_T3}
    C["ec40-head"] = {
        # unlink head T1 (prev==0): TASKH <- next
        "taskg": T2, "taskh": T1,
        "tasks": {T1: {"next": T2}, T2: {"prev": T1}},
        "steps": [(EC40, T1)],
        "watch": W_GLB + W_T1 + W_T2}
    C["ec40-tail"] = {
        # unlink tail T2 (next==0): TASKG <- prev
        "taskg": T2, "taskh": T1,
        "tasks": {T1: {"next": T2}, T2: {"prev": T1}},
        "steps": [(EC40, T2)],
        "watch": W_GLB + W_T1 + W_T2}
    C["ec40-idle"] = {
        # idle list nonempty: T2 pushes behind old idle head T4
        "taskg": T2, "taskh": T2, "taski": T4,
        "tasks": {T2: {}, T4: {}},
        "steps": [(EC40, T2)],
        "watch": W_GLB + W_T2 + W_T4}
    # ---- EB70/EA30 tick pacer ----
    C["eb70-wait"] = {
        # tickd(5) != xtick(7) -> spin until TICKQ advances ecx=3
        "tickd": 5, "xtick": 7, "tickq": 0x100,
        "steps": [(EB70, 3, 0)],
        "watch": [(TICKQ, 8)]}
    C["eb70-wait-zero"] = {
        # ecx=0 -> clamp to 1 tick
        "tickd": 5, "xtick": 7, "tickq": 0x200,
        "steps": [(EB70, 0, 0)],
        "watch": [(TICKQ, 8)]}
    C["eb70-resync"] = {
        # tickd == sx32(xtick) -> resync arm rewrites pacer cluster
        "tickd": 7, "xtick": 7, "x35e7": 0x99,
        "pacc": {0x0: 0x10, 0xC: 0x20, 0x2C: 0x44, 0x48: 0x55},
        "steps": [(EB70, 4, 0xABC)],
        "watch": [(PACC, 0x68)]}
    C["eb70-resync-gated"] = {
        # x17d3!=0 -> skips the 3691b0/369190 pair
        "tickd": 7, "xtick": 7, "x17d3": 1, "x35e7": 0x99,
        "steps": [(EB70, 4, 0xABC)],
        "watch": [(PACC, 0x68)]}
    C["ea30-wait"] = {
        # EA30 = EB70(ecx, edx=0): wait arm with ecx=4
        "tickd": 5, "xtick": 7, "tickq": 0x300,
        "steps": [(EA30, 4)],
        "watch": [(TICKQ, 8)]}
    C["ea30-resync"] = {
        "tickd": 9, "xtick": 9,
        "steps": [(EA30, 2)],
        "watch": [(PACC, 0x68)]}
    # ---- E070 pump ----
    C["e070-empty"] = {
        # taskg=0 -> xadd0 then straight to teardown
        "steps": [(E070, 0)],
        "watch": [(TASKG, 8)]}
    C["e070-empty-tail"] = {
        # x36fd!=0 -> conditional 3bb790 tail fires
        "x36fd": 1,
        "steps": [(E070, 0)],
        "watch": [(TASKG, 8)]}
    C["e070-badstate"] = {
        # state 0 -> ja teardown without xadd0
        "taskg": T1, "taskh": T1,
        "tasks": {T1: {"state": 0}},
        "steps": [(E070, 0)],
        "watch": W_T1}
    C["e070-badstate7"] = {
        "taskg": T1, "taskh": T1,
        "tasks": {T1: {"state": 7}},
        "steps": [(E070, 0)],
        "watch": W_T1}
    C["e070-s1-initfail"] = {
        # state1 + xadd0!=0 -> teardown
        "xadd0": 1,
        "taskg": T1, "taskh": T1,
        "tasks": {T1: {"state": 1, "d28": 4}},
        "steps": [(E070, 0)],
        "watch": W_T1}
    C["e070-s1-retire"] = {
        # state1 + d28==0 -> E330 + ec40 retire; sole task -> idle
        "taskg": T1, "taskh": T1,
        "tasks": {T1: {"state": 1, "d28": 0}},
        "steps": [(E070, 0)],
        "watch": W_GLB + W_T1}
    C["e070-s1-submit-a"] = {
        # b21!=0xFF -> submit-A -> tick stamp -> state2 -> ...
        # flagg=-1 -> S3 FLAG gate raises -> teardown
        "flagg": 0xFFFFFFFF,
        "taskg": T1, "taskh": T1, "tickq": 0x9999,
        "tasks": {T1: {"state": 1, "d28": 4, "b21": 3, "d24": 0x55,
                       "d2c": 0x100, "q38": 0x777}},
        "steps": [(E070, 0)],
        "watch": W_T1}
    C["e070-s1-submit-b"] = {
        # b21==0xFF -> submit-B; x2df6=[3,0]: first nonzero loops
        # (re-reads task, re-runs xadd0), second proceeds to state2
        "flagg": 0xFFFFFFFF,
        "x2df6": [3, 0],
        "taskg": T1, "taskh": T1, "tickq": 0x8888,
        "tasks": {T1: {"state": 1, "d28": 4, "b21": 0xFF,
                       "d24": 0x66, "d2c": 0x200, "q38": 0x888}},
        "steps": [(E070, 0)],
        "watch": W_T1}
    C["e070-s2"] = {
        # state2 -> two tick reads: q[0]+=t2, q[+8]=t2, state=3;
        # flagg=-1 -> S3 gate -> teardown
        "flagg": 0xFFFFFFFF,
        "taskg": T1, "taskh": T1, "tickq": 0x7777,
        "tasks": {T1: {"state": 2, "acc": 0x1000}},
        "steps": [(E070, 0)],
        "watch": W_T1}
    C["e070-s3-flag"] = {
        # flagg=-1 -> FLAG ret 2 -> teardown from the gate
        "flagg": 0xFFFFFFFF,
        "taskg": T1, "taskh": T1,
        "tasks": {T1: {"state": 3}},
        "steps": [(E070, 0)],
        "watch": W_T1}
    C["e070-s3-poll5"] = {
        # flagg=0 -> gate passes; poll sets al=0 -> state5;
        # b22=0 -> E330 retire
        "flagg": 0,
        "taskg": T1, "taskh": T1,
        "tasks": {T1: {"state": 3, "b22": 0}},
        "steps": [(E070, 0)],
        "watch": W_GLB + W_T1}
    C["e070-s3-poll6"] = {
        # flagg=0x80000000 (negative, not -1): gate passes (FLAG
        # only fires on ==-1), poll sets al=1 -> state6; b22=0 ->
        # E370 retire (cb40+d28==-1 -> r8=0 distinguishes E370/E330)
        "flagg": 0x80000000,
        "taskg": T1, "taskh": T1,
        "tasks": {T1: {"state": 3, "b22": 0, "cb40": CB40,
                       "d28": -1, "d60": 0x55, "q70": 0x66}},
        "steps": [(E070, 0)],
        "watch": W_GLB + W_T1}
    C["e070-s4-cb"] = {
        # state4 + cb48 planted: d28=0, cb48(d60), b20=0, ec40
        "cb48ret": 0x55,
        "taskg": T1, "taskh": T1,
        "tasks": {T1: {"state": 4, "cb48": CB48, "d60": 0x33,
                       "d28": 0x44}},
        "steps": [(E070, 0)],
        "watch": W_GLB + W_T1}
    C["e070-s4-nocb"] = {
        # state4, cb48 slot 0 -> skip callback, straight retire
        "taskg": T1, "taskh": T1,
        "tasks": {T1: {"state": 4, "d28": 0x44}},
        "steps": [(E070, 0)],
        "watch": W_GLB + W_T1}
    C["e070-s5-b22-0"] = {
        # direct state5 + b22=0 -> E330 retire arm; cb40+d28==-1
        # makes E330(r8=1)/E370(r8=0) distinguishable
        "taskg": T1, "taskh": T1,
        "tasks": {T1: {"state": 5, "b22": 0, "cb40": CB40,
                       "d28": -1, "d60": 0x55, "q70": 0x66}},
        "steps": [(E070, 0)],
        "watch": W_GLB + W_T1}
    C["e070-s6-b22-0"] = {
        # direct state6 + b22=0 -> E370 retire arm
        "taskg": T1, "taskh": T1,
        "tasks": {T1: {"state": 6, "b22": 0}},
        "steps": [(E070, 0)],
        "watch": W_GLB + W_T1}
    C["e070-s5-b22-bad"] = {
        # b22=2 -> teardown
        "taskg": T1, "taskh": T1,
        "tasks": {T1: {"state": 5, "b22": 2}},
        "steps": [(E070, 0)],
        "watch": W_T1}
    C["e070-s5-b23-2"] = {
        # b22=1,b23=2 -> E3B0 arm: cb50 ret 1 -> min(d30,d34)
        # requeue -> state1 -> xadd0 -> d28!=0 -> submit-A ->
        # ... flagg=-1 cuts it at the S3 gate
        "flagg": 0xFFFFFFFF,
        "cb50ret": 1,
        "taskg": T1, "taskh": T1, "tickq": 0x50,
        "tasks": {T1: {"state": 5, "b22": 1, "b23": 2,
                       "cb50": CB50, "d28": 9, "d30": 0x40,
                       "d34": 0x50, "d2c": 0x700, "b21": 3}},
        "steps": [(E070, 0)],
        "watch": W_GLB + W_T1}
    C["e070-s5-b23-2-stop"] = {
        # same arm but cb50 ret 2 -> b23=2, teardown
        "flagg": 0,
        "cb50ret": 2,
        "taskg": T1, "taskh": T1,
        "tasks": {T1: {"state": 5, "b22": 1, "b23": 2,
                       "cb50": CB50}},
        "steps": [(E070, 0)],
        "watch": W_T1}
    C["e070-s6-b23-0"] = {
        # state6 + b22=1 + b23=0 -> E370 retire arm (tail-B
        # clears b23); nonzero d28/d34 expose a stray progress
        # arm (the cmp-b20-6->5 mutant accrues d34)
        "taskg": T1, "taskh": T1,
        "tasks": {T1: {"state": 6, "b22": 1, "b23": 5,
                       "d28": 0x100, "d34": 0x300}},
        "steps": [(E070, 0)],
        "watch": W_GLB + W_T1}
    C["e070-s5-progress"] = {
        # state5 progress arm: d34-=d28>0 -> accrue d2c/q38,
        # cb50 ret 1 -> min(d30,d34) requeue -> state1 loop ->
        # xadd0 -> submit-A -> flagg=-1 cuts at S3 gate.
        # d2c=0x800: +0x100 rounds to 0x800, -0x100 rounds to 0
        "flagg": 0xFFFFFFFF,
        "cb50ret": 1,
        "taskg": T1, "taskh": T1, "tickq": 0x60,
        "tasks": {T1: {"state": 5, "b22": 1, "b23": 0,
                       "cb50": CB50, "d28": 0x100, "d2c": 0x800,
                       "q38": 0x900, "d30": 0x400, "d34": 0x300,
                       "b21": 3, "d24": 0x77}},
        "steps": [(E070, 0)],
        "watch": W_GLB + W_T1}
    C["e070-s5-progress-done"] = {
        # d34-d28 <= 0 -> exhausted: E330 + tail-B retire
        "taskg": T1, "taskh": T1,
        "tasks": {T1: {"state": 5, "b22": 1, "b23": 3,
                       "d28": 0x200, "d34": 0x100}},
        "steps": [(E070, 0)],
        "watch": W_GLB + W_T1}
    C["e070-s5-progress-stop"] = {
        # cb50 ret 2 -> b23=2, teardown after accrual
        "flagg": 0,
        "cb50ret": 2,
        "taskg": T1, "taskh": T1,
        "tasks": {T1: {"state": 5, "b22": 1, "b23": 0,
                       "cb50": CB50, "d28": 0x100, "d2c": 0x50,
                       "q38": 0x900, "d34": 0x300}},
        "steps": [(E070, 0)],
        "watch": W_T1}
    C["e070-s5-neg"] = {
        # b23-2 arm, d2c negative: cdq bias 0x7ff rounds -0x7ff
        # up to 0; a 0x7fe mutant rounds to -0x800
        "flagg": 0xFFFFFFFF,
        "cb50ret": 1,
        "taskg": T1, "taskh": T1,
        "tasks": {T1: {"state": 5, "b22": 1, "b23": 2,
                       "cb50": CB50, "d28": 9, "d30": 0x400,
                       "d34": 0x500, "d2c": -0x7FF, "b21": 3}},
        "steps": [(E070, 0)],
        "watch": W_T1}
    C["e070-s5-round"] = {
        # b23-2 arm, d2c=0x1FFF: rounds to 0x1800 with the
        # 0xfffff800 mask (0xfffff000 mutant -> 0x1000)
        "flagg": 0xFFFFFFFF,
        "cb50ret": 1,
        "taskg": T1, "taskh": T1,
        "tasks": {T1: {"state": 5, "b22": 1, "b23": 2,
                       "cb50": CB50, "d28": 9, "d30": 0x400,
                       "d34": 0x500, "d2c": 0x1FFF, "b21": 3}},
        "steps": [(E070, 0)],
        "watch": W_T1}
    C["e070-lifecycle"] = {
        # full duty cycle in one pump: S1 submit-A -> S2 -> S3
        # poll -> S5 progress (d34 0x400->0x200) -> requeue S1 ->
        # submit-A -> S2 -> S3 poll -> S5 progress (0x200->0) ->
        # exhausted retire -> empty -> teardown. flagg=0 so the
        # gate passes every pass; xadd0 clamped at 0.
        "flagg": 0,
        "cb50ret": 1,
        "taskg": T1, "taskh": T1, "tickq": 0x42,
        "tasks": {T1: {"state": 1, "d28": 0x200, "b21": 3,
                       "d24": 0x11, "d2c": 0, "q38": 0, "acc": 0,
                       "b22": 1, "b23": 0, "cb50": CB50,
                       "d30": 0x400, "d34": 0x400}},
        "steps": [(E070, 0)],
        "watch": W_GLB + W_T1}
    C["e070-two-tasks"] = {
        # T2 retires (state1, d28=0) -> TASKG moves to T1 ->
        # T1 pumped: state1 d28!=0 submit-A -> ... -> flagg cut
        "flagg": 0xFFFFFFFF,
        "taskg": T2, "taskh": T1, "tickq": 0x11,
        "tasks": {T1: {"state": 1, "d28": 4, "b21": 3, "next": T2},
                  T2: {"state": 1, "d28": 0, "prev": T1}},
        "steps": [(E070, 0)],
        "watch": W_GLB + W_T1 + W_T2}
    return C


# ---------------- mutants ----------------
# (name, case, addr, expected-byte, patch-byte)
# Sites are the displacement/immediate/opcode byte, not the insn head.
MUTS = [
    # AAD0
    ("m-aad0-root",   "aad0-adopt",  0x36AB13, 0x50, 0x48),   # BST root +0x50->+0x48
    ("m-aad0-keydisp","aad0-adopt",  0x36AB19, 0x18, 0x1C),   # head key +0x18->+0x1C
    ("m-aad0-left",   "aad0-descend",0x36AB25, 0x24, 0x28),   # descend +0x24->+0x28
    ("m-aad0-jle",    "aad0-adopt",  0x36AB3F, 0x7E, 0x7F),   # jle->jg: == arm dead
    ("m-aad0-jbe",    "aad0-adopt",  0x36AB4A, 0x76, 0x73),   # jbe->jae: eligibility inverted
    ("m-aad0-flagm",  "aad0-flag4",  0x36AB4F, 0x04, 0x02),   # f15&4->&2
    ("m-aad0-rty",    "aad0-repeat", 0x36AB6B, 0x74, 0xEB),   # je->jmp: exit even on r12!=0
    # ABE0
    ("m-abe0-pnxt",   "abe0-adopt",  0x36AC12, 0x10, 0x0C),   # phys-next +0x10->+0xC
    ("m-abe0-fm6",    "abe0-walk",   0x36AC29, 0x06, 0x02),   # flag mask 6->2 (f15=6 hits)
    ("m-abe0-f2eq",   "abe0-f4direct",0x36AC2B, 0x02, 0x04),  # cmp 2->4 (f15=4 hits flag arm)
    ("m-abe0-adv",    "abe0-walk",   0x36AC7C, 0x08, 0x04),   # free advance +8->+4
    ("m-abe0-alloc",  "abe0-stale-rbx",0x36ACBD, 0x14, 0x15), # alloc bit +0x14->+0x15
    # A2A0
    ("m-a2a0-bstm",   "a2a0-basic",  0x36A335, 0x02, 0x04),   # f15&2->&4 (BST unlink gate)
    ("m-a2a0-l20",    "a2a0-chained",0x36A34B, 0x20, 0x24),   # chain prev +0x20->+0x24
    ("m-a2a0-seqcp",  "a2a0-chained",0x36A460, 0x1C, 0x1E),   # post-carve w[rbx+0x1C]->+0x1E
    ("m-a2a0-cntidx", "a2a0-basic",  0x36A380, 0x17, 0x16),   # counter idx +0x17->+0x16
    ("m-a2a0-kind",   "a2a0-basic",  0x36A3B1, 0x01, 0x02),   # bc60 kind b[desc+1]->b[desc+2]
    # C790
    ("m-c790-parent", "c790-child-right", 0x36C7AE, 0x2C, 0x28), # parent +0x2C->+0x28
    ("m-c790-left",   "c790-root-both",   0x36C7C3, 0x24, 0x28), # left +0x24->+0x28
    ("m-c790-rootw",  "c790-root-null",   0x36C831, 0x50, 0x48), # root write +0x50->+0x48
    ("m-c790-slot",   "c790-child-leftonly",0x36C8A2, 0x24, 0x28), # slot test +0x24->+0x28
    # B410/B4E0/B490
    ("m-b410-nullp",  "b410-root",   0x36B439, 0x2C, 0x24),   # null +0x2C->+0x24
    ("m-b4e0-cmp",    "b4e0-right",  0x36B50D, 0x7E, 0x7D),   # jle->jge: side flip
    ("m-b490-slot",   "b490-force",  0x36B4D0, 0x24, 0x28),   # writes +0x24->+0x28
    ("m-b5a0-slot",   "b5a0-force",  0x36B5E0, 0x28, 0x24),   # writes +0x28->+0x24
    # A570
    ("m-a570-gate",   "a570-poolwalk",0x36A59D, 0x83, 0x82),  # jae->jb: mask gate inverted
    ("m-a570-kind",   "a570-kindE",  0x36A5AC, 0x0E, 0x0D),   # kind bound 0xE->0xD
    ("m-a570-walkf",  "a570-poolwalk",0x36A5CE, 0x01, 0x02),  # bpl&1->&2
    ("m-a570-print",  "a570-poolwalk",0x36A6E3, 0x1E, 0x1C),  # w[+0x1E]->+0x1C
    ("m-a570-selfchk","a570-poolwalk",0x36A724, 0x08, 0x0C),  # self-check +8->+0xC
    ("m-a570-adv",    "a570-neg-sel",0x36A731, 0x10, 0x0C),   # advance +0x10->+0xC
    ("m-a570-sent",   "a570-itabA",  0x36A7C8, 0xFF, 0xFE),   # sentinel 0xFFFF->0xFFFE
    ("m-a570-bstw",   "a570-bstwalk",0x36A816, 0x20, 0x40),   # bpl&0x20->&0x40
    ("m-a850-left",   "a850-leftdangle",0x36A95F,0x24, 0x28), # A850 recurse +0x24->+0x28
    # ================= EXP-126 =================
    # PREL gates
    ("m-prel-nullje", "prel-null",   0x369864, 0x84, 0x85),   # je->jne: null goes to frame path
    ("m-prel-aln",    "prel-misalign",0x369896,0x74, 0xEB),   # je->jmp: aligned -> misalign emit
    ("m-prel-magic",  "prel-alreadyfree",0x3698D9,0x84,0x85), # je->jne: good magic -> dump abort
    ("m-prel-markje", "prel-mark",   0x369A85, 0x74, 0xEB),   # je->jmp: mark always aborts
    ("m-prel-alloc",  "prel-alreadyfree",0x369AC2,0x75,0x74), # jne->je: free block -> real free
    # PREL free body
    ("m-prel-kind",   "prel-free-badkind",0x369AE9,0x73,0x72),# jae->jb: kind 0xF -> desc path
    ("m-prel-f14clr", "prel-free-phys-below",0x369B0C,0xFE,0xFD), # f14&=~1 -> &=~2
    ("m-prel-state",  "prel-free-phys-below",0x369B10,0xFF,0xFE), # b[+2]=0xFF -> 0xFE
    ("m-prel-used",   "prel-free-subctr",0x369B1A,0x68,0x6C), # use ctr +0x68 -> +0x6C
    ("m-prel-p17",    "prel-free-subctr",0x369B34,0x29,0x01), # sub -> add: PTAGC grows
    ("m-prel-l34",    "prel-free-subctr",0x369B39,0x34,0x35), # label +0x34 -> +0x35
    ("m-prel-w1e",    "prel-free-subctr",0x369B3F,0x1E,0x1C), # w[+0x1E] -> +0x1C
    ("m-prel-b17",    "prel-free-subctr",0x369B43,0x17,0x16), # b[+0x17] -> +0x16
    ("m-prel-d30",    "prel-free-subctr",0x369B4E,0x30,0x34), # d[+0x30] -> +0x34
    ("m-prel-w3e",    "prel-free-subctr",0x369B52,0x3E,0x3C), # w[+0x3E] -> +0x3C
    # PREL splice arms
    ("m-prel-pptest", "prel-free-phys-below",0x369B61,0x75,0x74), # free-prev jne->je
    ("m-prel-pntest", "prel-free-phys-above",0x369B7C,0x75,0x74), # free-next jne->je
    ("m-prel-bound",  "prel-free-bothdir",0x369B95,0x73,0x72),   # jae->jb: bound arm flip
    ("m-prel-skipn",  "prel-free-ae00-miss",0x369BBD,0x74,0xEB), # stale-next je->jmp
    ("m-prel-skipn2", "prel-free-skip-above",0x369BE2,0x75,0x74), # jne->je flip
    ("m-prel-skipp",  "prel-free-ae00",0x369BFA,0x74,0xEB), # stale-prev je->jmp
    # AE00
    ("m-ae00-nul",    "ae00-nopp-scan",0x36AE2C, 0xFF, 0x00),   # or r8d,-1 -> or r8d,0
    ("m-ae00-sar",    "ae00-slot2",  0x36AE42, 0x10, 0x20),   # sar 0x10 -> 0x20
    ("m-ae00-bit",    "ae00-mask-hi",0x36AE61, 0x1F, 0x3F),   # &0x1F -> &0x3F
    ("m-ae00-mask",   "ae00-masked-bit",0x36AE8A,0x23,0x0B),  # and -> or
    ("m-ae00-head",   "ae00-head-ge",0x36AEC3,0x72,0x73),     # jb->jae head<node
    ("m-ae00-nxt",    "ae00-below",  0x36AEEC, 0x77, 0x76),   # ja->jbe next>node
    # ACE0
    ("m-ace0-bnd",    "ace0-bound",  0x36AD39, 0x58, 0x50),   # bound +0x58 -> +0x50
    ("m-ace0-bcmp",   "ace0-above",  0x36AD88, 0x7D, 0x7C),   # jge->jl head-walk guard
    ("m-ace0-mask",   "ace0-masked-below",0x36AD5A,0x23,0x0B),# not edx -> nop prefix
    ("m-ace0-head",   "ace0-above",  0x36AD9B, 0x77, 0x76),   # ja->jbe head>node
    ("m-ace0-prv",    "ace0-above",  0x36ADCB, 0x72, 0x73),   # jb->jae prev<node
    # CHKSTK / PINIT / EMIT / THUNK
    ("m-chk-jae",     "prel-chkstk", 0x808F39, 0x73, 0x72),   # bnd jae->jb: probes skipped
    ("m-pinit-sx",    "pinit-neg",   0x4746F7, 0x63, 0x89),   # movsxd->mov r8d (zero-ext)
    ("m-emit-r9",     "emit-basic",  0x17D308, 0xCB, 0xCF),   # r9=fmt -> r9=rdx (buf)
    ("m-emit-rdx",    "emit-basic",  0x17D320, 0xD7, 0xD3),   # rdx=buf -> rdx=rbx (-1)
    ("m-thunk-disp",  "pinit-copy",  0x861EBC, 0xA8, 0xA0),   # IAT cell disp low byte
    # ---------------- EXP-128: poll-pump layer ----------------
    # E070 dispatch + gates
    ("m-e070-cmp5",   "e070-s6-b22-0",0x32E0A8,0x05,0x04),    # cmp eax,5->4: state6 ja's to teardown
    ("m-e070-initjne","e070-s1-initfail",0x32E0C5,0x85,0x84), # xadd0!=0 proceeds to submit
    ("m-e070-d28je",  "e070-s1-retire",0x32E0D1,0x74,0x75),   # d28==0 falls into submit-A
    ("m-e070-b21ff",  "e070-s1-submit-b",0x32E0D8,0xFF,0xFE), # b21==0xFF -> submit-A not B
    ("m-e070-s2b20",  "e070-s1-submit-a",0x32E102,0x02,0x03), # stamp state 2->3 (S2 skipped)
    ("m-e070-s2acc",  "e070-s2",       0x32E154,0x01,0x29),   # q[0]+=tick -> -=
    ("m-e070-flagjne","e070-s3-flag",  0x32E16B,0x85,0x84),   # FLAG!=0 proceeds to poll
    ("m-e070-cmp4",   "e070-s4-cb",    0x32E173,0x04,0x05),   # state4 -> poll arm not cb arm
    ("m-e070-sets",   "e070-s3-poll6", 0x32E1A4,0x98,0x99),   # sets->setns: state5 vs 6 swap
    ("m-e070-b22cmp", "e070-s5-progress",0x32E1B9,0x01,0x02), # b22==1 -> !=2 -> teardown
    ("m-e070-b23cmp", "e070-s5-b23-2", 0x32E1C3,0x02,0x01),   # b23==2 -> progress arm instead
    ("m-e070-s6cmp",  "e070-s6-b23-0", 0x32E1D0,0x06,0x05),   # state6 -> progress arm not retire
    ("m-e070-d34sub", "e070-s5-progress",0x32E1F1,0x29,0x01), # d34-=step -> +=step
    ("m-e070-jg",     "e070-s5-progress",0x32E1F8,0x7F,0x7E), # d34>0 -> retire instead
    ("m-e070-d2cadd", "e070-s5-progress",0x32E201,0x01,0x29), # d2c+=step -> -=
    ("m-e070-q38add", "e070-s5-progress",0x32E205,0x01,0x29), # q38+=step -> -=
    ("m-e070-al1",    "e070-s5-progress",0x32E211,0x01,0x02), # cb50ret==1 -> teardown
    ("m-e070-cmovl",  "e070-s5-progress",0x32E21F,0x4C,0x4D), # cmovl->cmovge: min->max
    ("m-e070-mask7ff","e070-s5-neg",   0x32E232,0xFF,0xFE),   # cdq bias 0x7ff->0x7fe
    ("m-e070-mask800","e070-s5-round", 0x32E242,0xF8,0xF0),   # mask 0xfffff800->0xfffff000
    ("m-e070-s5cmp",  "e070-s5-b22-0", 0x32E269,0x05,0x06),   # retire cmp 5->6: E370 not E330
    ("m-e070-q0clr",  "e070-s5-b23-2", 0x32E22C,0x00,0x01),   # q[0]=0 -> q[0]=1
    ("m-e070-s1clr",  "e070-s1-retire",0x32E13E,0x00,0x03),   # b20=0 -> 3 (S1 retire tail)
    ("m-e070-s4clr",  "e070-s4-cb",    0x32E191,0x00,0x03),   # b20=0 -> 3 (S4 retire tail)
    ("m-e070-b23clr", "e070-s6-b23-0", 0x32E1DE,0x00,0x01),   # tail-B b23=0 -> 1
    ("m-e070-s5clr",  "e070-s5-b22-0", 0x32E27A,0x00,0x03),   # b20=0 -> 3 (E330 tail)
    ("m-e070-s6clr",  "e070-s6-b22-0", 0x32E290,0x00,0x03),   # b20=0 -> 3 (E370 tail)
    ("m-e070-jtab",   "e070-s1-retire",0x32E2D0,0xBD,0x49),   # JTAB[0]: S1 arm -> S2 arm
    # E330 / E370
    ("m-e330-cbje",   "e330-nocb",     0x32E340,0x74,0x75),   # cb40==0 -> call rax(0) fault
    ("m-e330-r8",     "e330-cb",       0x32E348,0x01,0x00),   # cb r8d=1 -> 0
    ("m-e330-b21jne", "e330-free",     0x32E355,0x75,0x74),   # b21==0xFF skips the free
    ("m-e370-d28cmp", "e370-cb",       0x32E385,0xFF,0x00),   # d28==-1 gate -> ==0
    # E3B0
    ("m-e3b0-je",     "e3b0-null",     0x32E3BB,0x74,0x75),   # cb50==0 -> call rax(0) fault
    ("m-e3b0-eax1",   "e3b0-null",     0x32E3E1,0x01,0x02),   # null arm ret 1 -> 2
    # EC40
    ("m-ec40-cmove",  "ec40-sole",     0x32EC54,0x44,0x45),   # tail cell: cmove->cmovne
    ("m-ec40-cmove2", "ec40-head",     0x32EC69,0x44,0x45),   # head cell: cmove->cmovne
    ("m-ec40-np",     "ec40-mid",      0x32EC7A,0x10,0x18),   # next.prev -> next.next
    ("m-ec40-pn",     "ec40-mid",      0x32EC94,0x18,0x10),   # prev.next -> prev.prev
    ("m-ec40-taski",  "ec40-sole",     0x32ECC1,0x0B,0x03),   # TASKI store -> TASKH
    ("m-ec40-d64",    "ec40-sole",     0x32ECC8,0xFF,0x00),   # d[+0x64]=-1 -> 0
    # EB70 / EA30
    ("m-eb70-je",     "eb70-wait",     0x35EB93,0x74,0x75),   # equal-tick -> wait arm swap
    ("m-eb70-cmovg",  "eb70-wait",     0x35EBA4,0x4F,0x4C),   # cmovg->cmovl: edx=1
    ("m-eb70-jb",     "eb70-wait",     0x35EBBA,0x72,0x73),   # jb->jae: spin exits at 1
    ("m-eb70-sub",    "eb70-wait",     0x35EBC4,0x2B,0x03),   # ret rax-r8 -> rax+r8
    ("m-eb70-jne",    "eb70-resync-gated",0x35EBDD,0x75,0x74),# x17d3!=0 runs helpers
    ("m-eb70-cmovg2", "eb70-resync",   0x35EC1D,0x4F,0x4C),   # PACC+0x30 lim: cmovg->cmovl
    ("m-eb70-si",     "eb70-resync",   0x35EC2A,0xD6,0xD2),   # esi store +0x40 -> +0x3C
    # leaves
    ("m-g97f0-je",    "g97f0-free",    0x3697F3,0x74,0xEB),   # rcx!=0 also skips PREL
    ("m-e810-disp",   "e810-tick",     0x35E813,0xC9,0xC8),   # reads TICKQ-1
    ("m-g8c70-disp",  "g8c70-read",    0x368C72,0x3A,0x38),   # reads TICKD-2
    ("m-ge0e0-disp",  "ge0e0-read",    0x46E0E2,0x0E,0x0C),   # reads FLAGG-2
    ("m-g6a0-ret",    "e070-empty",    0x16D6A1,0x00,0x08),   # ret 0 -> ret 8
]


def main():
    raw, secs = load_image()
    C = cases()
    fails = []
    results = {}
    for name, case in C.items():
        nat = World(case, raw, secs)
        nat.run()
        nres = nat.obs()
        mres = run_model(case, raw, secs)
        d = differs(nres, mres)
        results[name] = {"ok": not d, "diff": d,
                         "nat": nres, "mod": mres}
        if d:
            fails.append((name, d))
    print("functional: %d/%d" % (len(C) - len(fails), len(C)))
    for n, d in fails:
        print("  FAIL %s %s" % (n, d))

    # mutation campaign
    mfails = []
    for mname, cname, va, exp, patch in MUTS:
        orig = img_rd(raw, secs, va, 1)[0]
        if orig != exp:
            mfails.append((mname, "site byte %02x != expected %02x"
                           % (orig, exp)))
            continue
        case = dict(C[cname])
        case["patch_bytes"] = [(va, bytes([patch]))]
        nat = World(case, raw, secs)
        nat.run()
        nres = nat.obs()
        mres = run_model(case, raw, secs)
        if not differs(nres, mres):
            mfails.append((mname, "mutant survived"))
    print("mutants: %d/%d killed" % (len(MUTS) - len(mfails), len(MUTS)))
    for n, w in mfails:
        print("  LIVE %s %s" % (n, w))

    json.dump({"cases": results,
               "mutants": [{"name": m[0], "case": m[1],
                            "site": "%x" % m[2], "exp": m[3],
                            "patch": m[4]} for m in MUTS]},
              open("result.json", "w"), indent=1)
    return 1 if fails or mfails else 0


if __name__ == "__main__":
    raise SystemExit(main())
