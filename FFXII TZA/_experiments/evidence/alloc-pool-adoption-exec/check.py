# EXP-125 — alloc-pool-adoption-exec
# Executes the allocator pool-adoption (compaction) layer end to end:
#   AAD0 0036AAD0 (~258B): pool-BST scan vs free-list head — descends
#     the keyed BST rooted at q[desc+0x50] (+0x24 smaller / +0x28
#     larger-or-equal children, +0x2C parent), key==d[head+0x18] &&
#     addr>head && !(f15&4) -> A2A0 adopt; r15d counts adoptions;
#     edx!=0 re-reads the head and rescans. The < arm's best-candidate
#     tracking (rdi) is dead — never consumed before the return.
#   ABE0 0036ABE0 (~242B): per-free-node scan — walks the free list via
#     +8; for each node rdi reads phys-next r8=BASE(d[rdi+0x10]);
#     (b[r8+0x15]&6)==2 && (b[r8+0x14]&1) -> A2A0(desc, rdi, STALE rbx)
#     (rbx is register residue — 0 on the first iteration, a real fault
#     path through A2A0's b[r8+0x14] deref); else BST-scan for key==
#     d[rdi+0x18], addr>rdi, !f15&4 -> A2A0(desc, rdi, found); ret 1 on
#     any adoption, 0 at list end / null phys-next.
#   A2A0 0036A2A0 (~495B): adopt-one — snapshot src trailer (+0x14/+0x15/
#     +2/+3/+0x16/+0x17/+0x1E/+0x30) + label string (+0x34); f15&2 ->
#     C790 BST-unlink src; splice rbx after BASE(d[src+0x20]) in the
#     threaded chain (q[rsi+8]=rbx, d[rbx+0x20]=C620(rsi), w[rsi+6]=
#     w[rbx+0x1C]); d[0x22D8E10 + b[src+0x17]*4] += d[src+0x18]; PREL
#     00369860 + PINIT 004746F0 scripted; BC60(b[desc+1], srckey, rbx,
#     0) ctx-carve REAL; copy snapshot+label onto rbx; f15&2 -> clear,
#     B410 reinsert, set; re-splice chain; w[rbx+0x3E]=0; GS cookie.
#   C790 0036C790 (~367B): BST unlink — parent==0 arms (right promotes
#     + B4E0 reattach-left / left promotes / clear root); parent!=0
#     arms (B4E0 left-under-right + slot fix, or B490 left-attach for
#     BOTH child slots — asymmetric, writes +0x24 unconditionally).
#   B410 0036B410 (124B): BST insert — null links+parent, w[+0x3E]=0;
#     root==0 -> node becomes root; else B4E0(root, node, 0x50e).
#   B4E0 0036B4E0 (176B): keyed insert-under — descend +0x24 while
#     anchor.key > node.key else +0x28; leaf insert + parent back-link.
#     r8d tag arg DEAD.
#   B490 0036B490 (77B): force-attach rdx as rcx's +0x24 child.
#   A570 0036A570 (~729B): REAL this time — mask-gated diagnostic:
#     bt(d[0x22D89B8],kind) silent ret on clear; desc or fault q[0x10]
#     for kind>0xE; flag walks: &1 pool chain via +0x10 (label grid +
#     sel match + hook q[0x8C2F70] -> planted FLAG leaf, args traced),
#     &2 free list via +8 self-loop, &8/&0x10 index tables q[+0x48]/
#     q[+0x40] over 16B entries at q[+0x30], &0x20 -> A850 on the BST.
#   A850 0036A850 (~430B): pre-order BST label-format walk — builds the
#     same M2/U..FREE strings + /I//C suffix on the STACK and discards
#     them (no output call) — observable only via traversal/faults.
#   BC60/BASE/C620/CHKCK real (EXP-123 model reused for the ctx carve).
#   Scripted boundaries (entry-intercepted, NOT executed): PREL
#     00369860 (deep payload-release diag), PINIT 004746F0 (deep float
#     payload copy). The output cell q[0x8C2F70] ships pointing at
#     rdata (0x1CCEF16 — not code); fixture plants it to FLAG 0046DFE0
#     so the dispatch executes real shipped code AND the call args are
#     traced at the FLAG entry.
#
# Fixture disclosure: all BSS globals + desc fields (+0x10 pool base,
#   +0x30 idx-table base, +0x40/+0x48 idx chains, +0x50 BST root,
#   +0x60 seq, +0x68 use, +0x90/+0x98 free roots, b[+1] kind) planted;
#   pool + free headers fixture. CODEC=0 -> links raw u32 (the
#   EXP-083-proven valid configuration). Model reads fall back to
#   shipped image bytes where unplanted.

import ctypes, hashlib, json, struct
from unicorn import Uc
from unicorn.x86_const import (
    UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_R9,
    UC_X86_REG_RAX, UC_X86_REG_RIP, UC_X86_REG_RSP)
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

PREL  = 0x00369860    # scripted: payload release/diag
PINIT = 0x004746F0    # scripted: float payload init/copy
OUTC  = 0x8C2F70      # q: output-hook cell (ships a data ptr)
CELLP = 0x8C2D80      # q: shared twin hook cell (ships 0)
SPIN_BC60 = 0x36BC87
INT3 = {B670: 0x36B6AE, B730: 0x36B76E,
        B7F0: 0x36B82E, B8B0: 0x36B8EE}

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
    W.append((FLAGG, dw(case.get("flagg", 5))))
    for t, v in case.get("ptagc", {}).items():
        W.append((PTAGC + t * 4, dw(v)))
    # descriptors
    for k, d in case.get("desc", {}).items():
        b = DTAB + k * 0xA8
        if "kind" in d: W.append((b + 1, bytes([d["kind"]])))
        if "pool" in d: W.append((b + 0x10, qw(d["pool"])))
        if "bmap" in d: W.append((b + 0x20, qw(d["bmap"])))
        if "ptab" in d: W.append((b + 0x28, qw(d["ptab"])))
        if "itab" in d: W.append((b + 0x30, qw(d["itab"])))
        if "chA" in d:  W.append((b + 0x48, qw(d["chA"])))
        if "chB" in d:  W.append((b + 0x40, qw(d["chB"])))
        if "bst" in d:  W.append((b + 0x50, qw(d["bst"])))
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
        for addr, dat in build_fixture(case):
            gm.w(addr, dat)
        for addr, dat in case.get("patch_bytes", []):
            gm.w(addr, dat)
        self.trace, self.faults, self.rets, self.ends = [], [], [], []
        self.uc.hook_add(UC_HOOK_CODE, self.on_code)
        self.uc.hook_add(UC_HOOK_MEM_UNMAPPED, self.on_bad)
        self.uc.hook_add(UC_HOOK_INTR, self.on_intr)

    def _ret(self, uc):
        uc.reg_write(UC_X86_REG_RIP, self.gm.qw(uc.reg_read(UC_X86_REG_RSP)))
        uc.reg_write(UC_X86_REG_RSP, uc.reg_read(UC_X86_REG_RSP) + 8)

    def on_intr(self, uc, intno, _):
        self.faults.append(("trap", uc.reg_read(UC_X86_REG_RIP)))
        uc.emu_stop()

    def on_code(self, uc, addr, size, _):
        if addr == PREL:
            self.trace.append("prel:%x" % uc.reg_read(UC_X86_REG_RCX))
            uc.reg_write(UC_X86_REG_RAX, 0)
            self._ret(uc)
        elif addr == PINIT:
            self.trace.append("pinit:%x:%x:%x" % (
                uc.reg_read(UC_X86_REG_RCX), uc.reg_read(UC_X86_REG_RDX),
                uc.reg_read(UC_X86_REG_R8) & 0xFFFFFFFF))
            uc.reg_write(UC_X86_REG_RAX, 0)
            self._ret(uc)
        elif addr == FLAG:
            # planted out-hook target: real leaf executes; trace args.
            # FLAG semantics: d[FLAGG]==-1 -> 2 (cmove); ret = old
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
            uc.emu_start(entry, RETQ, count=40000)
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

    def mb(self, a):
        a &= 0xFFFFFFFFFFFFFFFF
        if a in self.mem:
            return self.mem[a]
        if IMG_LO <= a < IMG_HI:
            return img_byte(self.raw, self.secs, a)
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
        if not blk or self.trap: return 0
        if (self.mw(blk + 0x3E) or 0) != 0:
            self.trace.append("a570:%x:%x" % (self.md(ST_W) or 0, 0xB))
            self.trap = INT3[va] + 1
            return 0
        lo, hi = (0xC, 0x10) if va in (B7F0, B8B0) else (4, 8)
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
                    0x36A2C3, GSCOOK ^ A2A0_RSP)
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
        self.trace.append("prel:%x" % (rbp + 0x40))
        self.trace.append("pinit:%x:%x:%x" % (
            rbx + 0x40, rbp + 0x40, self.md(rbp + 0x18) or 0))
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
                        r = self.a2a0(desc, rsi, rbx)
                        r15 += 1
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
                    r = self.a2a0(desc, rdi, r8)
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
                r = self.a2a0(desc, rdi, rbx)
                if self.trap or r[0] != "ret":
                    return r
                return ("ret", 1)
            rdi = self.base(self.md(rdi + 8)) or 0
            if rdi == 0: return ("ret", 0)

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
                        0x36A8A0, GSCOOK ^ A850_RSP)
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


def run_model(case, raw, secs):
    m = Model(case, raw, secs)
    for step in case.get("steps", []):
        entry = step[0]
        args = list(step[1:]) + [0] * (4 - len(step[1:]))
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
      "seq": 5}
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
