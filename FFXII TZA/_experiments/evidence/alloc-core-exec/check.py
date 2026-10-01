# EXP-123 — alloc-core-exec
# Executes the 0036BC60 allocator core and its full callee tree:
#   BC60 0036BC60 (~888B): gate (ctx==0 && QCOUNT==0 -> jmp$),
#     r14d=align64(size); desc=DTAB+kind*0xA8 (kind>0xE -> b[2] write
#     fault); b[desc+2]=1; ctx!=0 -> carve caller node (tag=b[ctx+0x16])
#     else mask bt gate + free-list search (arg4==0: head walk via +8;
#     arg4!=0: tail walk via +4; first/last fit by ADDRESS, key>=r14d,
#     tag=d[TAGEP]); carve head (arg4==0, rsi=node) or tail (rsi=
#     node+key-r14d, rbp=node remainder); roots update; C900 page-table
#     remove; C9D0 unlink pairs (+4/+8, +0xC/+0x10) stamp 0xFF99; A490
#     header init x2 (magic 0xFF12, kind, null links, size, seq);
#     b[rsi+0x15]|=arg4; b[rsi+0x14]|=1; tag->b[rsi+0x16]; remainder ->
#     B5F0 page insert + phys splice (B7F0/B8B0); arg4!=0 also splices
#     rbp into list-1 (B670/B730) + B210 coalesce; usage d[desc+0x68+
#     sx32(tag)*4]+=r14d; w[desc+0x60]++; return rsi+0x40.
#   Helpers real: A490 0036A490 (header init), B210 0036B210 (back+
#     fwd coalesce via B2C0), B2C0 0036B2C0 (fwd coalesce), B5F0
#     0036B5F0 (page-head min-addr insert + bitmap), C900 0036C900
#     (page-head remove + bitmap), C9D0 0036C9D0 (list unlink),
#     B670/B730/B7F0/B8B0 twins (splice after/before on pairs
#     +4/+8 and +0xC/+0x10), BASE 0020E600, C620 0020E620.
#   Scripted boundaries (entry-intercepted, NOT executed): A570
#     0036A570 (mask-gated diagnostic dump on the w[+0x3E]!=0
#     corruption path; token recorded). The shared hook cell
#     q[0x8C2D80] ships as 0 (runtime-planted); the fixture plants it
#     to FLAG 0046DFE0 so the corrupt-path call runs a real leaf.
#
# Fixture disclosure: all BSS globals (MASKG/QCOUNT/TAGEP/ST_B3/CODEC/
#   desc table) planted; pool, page table, bitmap, and all block
#   headers are fixture. CODEC planted to 0 -> BASE(x)=u32(x),
#   C620(x)=x (the EXP-083-proven valid configuration); every guest
#   address <4GiB so encoded links are raw pointers. Model reads fall
#   back to shipped image bytes where unplanted.

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
A570 = 0x0036A570     # scripted boundary (corrupt-path dump)
BASE = 0x0020E600
C620 = 0x0020E620
FLAG = 0x0046DFE0     # real leaf - planted hook-cell target

SPIN_BC60 = 0x36BC87  # BC60 gate jmp$ site
CELLP    = 0x8C2D80   # shared twin hook cell (ships 0)
INT3 = {B670: 0x36B6AE, B730: 0x36B76E,
        B7F0: 0x36B82E, B8B0: 0x36B8EE}  # post-cell int3 sites

MASKG  = 0x22D89B8    # d: kind mask (bt eax, ecx)
ST_W   = 0x22D89BC    # d: staged word (A570's arg)
QCOUNT = 0x22D89C0    # d: gate count
TAGEP  = 0x22D8E1C    # d: tag epoch (search-path tag)
ST_B3  = 0x22D8E28    # d: gates b[blk+0x15]=8 in A490
CODEC  = 0x1F83530    # q: arena codec base cell (planted 0)
DTAB   = 0x22D7FD0    # kind descriptor table, stride 0xA8

PAGETAB = HEAP + 0x20000   # qword array, per-64KB min-addr heads
BITMAP  = HEAP + 0x28000   # dword bitmap of occupied page slots
NP = POOL + 0x800          # free-predecessor fixture block
N1 = POOL + 0x1000         # fixture block addresses (slot 0)
N2 = POOL + 0x2000
N3 = POOL + 0x14000        # slot 1
N3B = POOL + 0x18000       # slot 1, higher address
N4 = POOL + 0x24000        # slot 2
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
    # descriptors
    for k, d in case.get("desc", {}).items():
        b = DTAB + k * 0xA8
        if "pool" in d: W.append((b + 0x10, qw(d["pool"])))
        if "bmap" in d: W.append((b + 0x20, qw(d["bmap"])))
        if "ptab" in d: W.append((b + 0x28, qw(d["ptab"])))
        if "seq" in d:  W.append((b + 0x60, ww(d["seq"])))
        if "head" in d: W.append((b + 0x90, qw(d["head"])))
        if "tail" in d: W.append((b + 0x98, qw(d["tail"])))
        if "use" in d:
            for t, v in d["use"].items():
                W.append((b + 0x68 + t * 4, dw(v)))
    # pre-seeded page table + bitmap
    for s, v in case.get("ptab", {}).items():
        W.append((PAGETAB + s * 8, qw(v)))
    for s, v in case.get("bmap", {}).items():
        W.append((BITMAP + s * 4, dw(v)))
    # block headers (0x40): links encoded with CODEC=0 -> raw u32
    for a, n in case.get("nodes", {}).items():
        hdr = bytearray(0x40)
        struct.pack_into("<H", hdr, 0x00, n.get("magic", 0xFF12))
        hdr[0x02] = n.get("b2", 0xFF)
        hdr[0x03] = n.get("kind", DESCK)
        struct.pack_into("<I", hdr, 0x04, n.get("prev", 0) & 0xFFFFFFFF)
        struct.pack_into("<I", hdr, 0x08, n.get("next", 0) & 0xFFFFFFFF)
        struct.pack_into("<I", hdr, 0x0C, n.get("pprev", 0) & 0xFFFFFFFF)
        struct.pack_into("<I", hdr, 0x10, n.get("pnext", 0) & 0xFFFFFFFF)
        struct.pack_into("<H", hdr, 0x14, n.get("f14", 0))
        hdr[0x15] = n.get("f15", 0)
        hdr[0x16] = n.get("tag", 0)
        struct.pack_into("<I", hdr, 0x18, n.get("key", 0) & 0xFFFFFFFF)
        struct.pack_into("<H", hdr, 0x1C, n.get("seq", 0))
        struct.pack_into("<H", hdr, 0x3E, n.get("w3e", 0))
        W.append((a, bytes(hdr)))
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
        gm.map(POOL, 0x100000)
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

    def on_intr(self, uc, intno, _):
        # int3 after the twin hook-cell call — noreturn boundary
        self.faults.append(("trap", uc.reg_read(UC_X86_REG_RIP)))
        uc.emu_stop()

    def on_code(self, uc, addr, size, _):
        if addr == A570:
            self.trace.append("a570:%x:%x" % (
                uc.reg_read(UC_X86_REG_RCX) & 0xFFFFFFFF,
                uc.reg_read(UC_X86_REG_RDX) & 0xFFFFFFFF))
            uc.reg_write(UC_X86_REG_RAX, 0)
            uc.reg_write(UC_X86_REG_RIP,
                         self.gm.qw(uc.reg_read(UC_X86_REG_RSP)))
            uc.reg_write(UC_X86_REG_RSP,
                         uc.reg_read(UC_X86_REG_RSP) + 8)

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
            uc.emu_start(entry, RETQ, count=20000)
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

    # ---- scripted boundary ----
    def a570_call(self, ecx, edx):
        self.trace.append("a570:%x:%x" % (ecx & 0xFFFFFFFF,
                                          edx & 0xFFFFFFFF))
        return 0

    # ---- helpers ----
    def pslot(self, desc, blk):
        d = blk - (self.mq(desc + 0x10) or 0)
        if d < 0:
            d += 0xFFFF            # cqo: add sign16 for sar floor
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
        """page-head remove: drop blk from the min-addr slot table.
        rax = head on the early-out arm, else the bitmap pointer."""
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
        """page-head insert: keep the lowest-addressed block per slot.
        rax = &ptab[slot] on the insert/keep arms, bm on replace."""
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
        """unlink node from list-1 (+4/+8); flag!=0 also list-2
        (+0xC/+0x10) and stamps magic 0xFF99."""
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
        """list splice: B670/B730 pair-1 after/before, B7F0/B8B0
        pair-2 after/before. w[blk+0x3E]!=0 -> A570 + hook cell,
        then int3 (noreturn; rip lands one past the int3). rax =
        c620(old next) for after-splices, c620(anchor) for before."""
        if not blk or self.trap: return 0
        if (self.mw(blk + 0x3E) or 0) != 0:
            self.a570_call(self.md(ST_W) or 0, 0xB)
            # hook cell -> FLAG (real leaf; return ignored), int3
            self.trap = INT3[va] + 1
            return 0
        lo, hi = (0xC, 0x10) if va in (B7F0, B8B0) else (4, 8)
        if va in (B670, B7F0):          # insert blk after anchor
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
        """forward-coalesce: absorb physically-adjacent free blocks."""
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
        """back-coalesce then forward-coalesce; fix roots; clear f15."""
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

    # ---- BC60 core ----
    def bc60(self, ecx, edx, r8, r9d):
        kind = ecx & 0xFFFFFFFF
        arg4 = r9d & 0xFFFFFFFF
        ctx = r8 & 0xFFFFFFFFFFFFFFFF
        if ctx == 0 and (self.md(QCOUNT) or 0) == 0:
            return ("spin", SPIN_BC60, 0)
        eax = edx & 0xFFFFFFFF
        if eax & 0x80000000: eax = 0          # cmovns: max(edx,0)
        eax = (eax + 0x3F) & 0xFFFFFFFF
        corr = 0x3F if eax & 0x80000000 else 0
        r14 = ((eax + corr) & 0xFFFFFFFF) & 0xFFFFFFC0
        rbx = DTAB + kind * 0xA8 if kind <= 0xE else 0
        if rbx == 0:
            # b[rbx+2]=1 writes to 0x2; rax still holds size+0x3F
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
        # carve: links out of the node
        r15 = self.base(self.md(rdi + 0xC)) or 0     # phys prev
        r12 = self.base(self.md(rdi + 0x10)) or 0    # phys next
        prev1 = self.base(self.md(rdi + 4)) or 0     # list prev
        next1 = self.base(self.md(rdi + 8)) or 0     # list next
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


def run_model(case, raw, secs):
    m = Model(case, raw, secs)
    for step in case.get("steps", []):
        entry = step[0]
        args = list(step[1:]) + [0] * (4 - len(step[1:]))
        if entry == BC60:
            r = m.bc60(*args)
        elif entry == A490:
            m.a490(*args); r = ("ret", 0)
        elif entry == C9D0:
            m.c9d0(args[0], args[1]); r = ("ret", 0)
        elif entry == B5F0:
            r = ("ret", m.b5f0(args[0], args[1]))
        elif entry == B210:
            r = ("ret", m.b210(args[0], args[1]))
        elif entry == C900:
            r = ("ret", m.c900(args[0], args[1]))
        elif entry in (B670, B730, B7F0, B8B0):
            rax = m.twin(entry, args[0], args[1])
            r = ("trap", m.trap, 0) if m.trap else ("ret", rax)
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
# node helper: (addr, key, prev, next, pprev, pnext, extra)
def nd(a, key, prev=0, nxt=0, pp=0, pn=0, **kw):
    return dict(key=key, prev=prev, next=nxt,
                pprev=pp, pnext=pn, **kw)

D2 = {"pool": POOL, "bmap": BITMAP, "ptab": PAGETAB, "seq": 5}
W_N1 = [(N1, 0x40)]
W_N2 = [(N2, 0x40)]
W_N3 = [(N3, 0x40)]
W_NP = [(NP, 0x40)]
W_DSC = [(DTAB + DESCK * 0xA8, 0x10),
         (DTAB + DESCK * 0xA8 + 0x60, 8),
         (DTAB + DESCK * 0xA8 + 0x68, 0x40),
         (DTAB + DESCK * 0xA8 + 0x90, 0x10)]
W_PG = [(PAGETAB, 0x40), (BITMAP, 0x20)]


def cases():
    C = {}
    # ---- BC60 search path (ctx=0) ----
    C["bc60-empty"] = {
        "desc": {DESCK: dict(D2)}, "mask": 1 << DESCK, "qcount": 1,
        "watch": W_DSC, "steps": [(BC60, DESCK, 0x80, 0, 0)]}
    C["bc60-spin"] = {
        "desc": {DESCK: dict(D2)}, "mask": 1 << DESCK, "qcount": 0,
        "steps": [(BC60, DESCK, 0x80, 0, 0)]}
    C["bc60-maskclr"] = {
        "desc": {DESCK: dict(D2)}, "mask": 0, "qcount": 1,
        "watch": W_DSC, "steps": [(BC60, DESCK, 0x80, 0, 0)]}
    C["bc60-kind-hi"] = {
        "desc": {DESCK: dict(D2)}, "mask": 0xFFFFFFFF, "qcount": 1,
        "steps": [(BC60, 0xF, 0x80, 0, 0)]}
    C["bc60-head-exact"] = {
        "desc": {DESCK: dict(D2, head=N1, tail=N1)},
        "mask": 1 << DESCK, "qcount": 1, "tagep": 3,
        "nodes": {N1: nd(N1, 0x80)},
        "watch": W_N1 + W_DSC + W_PG,
        "steps": [(BC60, DESCK, 0x80, 0, 0)]}
    C["bc60-head-split"] = {
        "desc": {DESCK: dict(D2, head=N1, tail=N1)},
        "mask": 1 << DESCK, "qcount": 1, "tagep": 3,
        "nodes": {N1: nd(N1, 0x140)},
        "watch": [(N1, 0x40), (N1 + 0xC0, 0x40)] + W_DSC + W_PG,
        "steps": [(BC60, DESCK, 0x80, 0, 0)]}
    C["bc60-exact-phys"] = {
        # exact fit with a phys predecessor: the root-update writes
        # are NOT masked by the no-neighbor zero arm (r15 != 0)
        "desc": {DESCK: dict(D2, head=N1, tail=N1)},
        "mask": 1 << DESCK, "qcount": 1, "tagep": 0,
        "nodes": {NP: nd(NP, 0x40, pn=N1),
                  N1: nd(N1, 0x80, pp=NP)},
        "watch": W_NP + W_N1 + W_DSC + W_PG,
        "steps": [(BC60, DESCK, 0x80, 0, 0)]}
    C["bc60-tail-split"] = {
        "desc": {DESCK: dict(D2, head=N1, tail=N1)},
        "mask": 1 << DESCK, "qcount": 1, "tagep": 2,
        "nodes": {N1: nd(N1, 0x140)},
        "watch": [(N1, 0x40), (N1 + 0xC0, 0x40)] + W_DSC + W_PG,
        "steps": [(BC60, DESCK, 0x80, 0, 1)]}
    C["bc60-tail-exact"] = {
        "desc": {DESCK: dict(D2, head=N1, tail=N1)},
        "mask": 1 << DESCK, "qcount": 1, "tagep": 2,
        "nodes": {N1: nd(N1, 0x80)},
        "watch": W_N1 + W_DSC + W_PG,
        "steps": [(BC60, DESCK, 0x80, 0, 1)]}
    C["bc60-two-best"] = {
        "desc": {DESCK: dict(D2, head=N1, tail=N2)},
        "mask": 1 << DESCK, "qcount": 1, "tagep": 0,
        "nodes": {N1: nd(N1, 0x80, nxt=N2, pn=N2),
                  N2: nd(N2, 0x140, prev=N1, pp=N1)},
        "watch": W_N1 + W_N2 + W_DSC + W_PG,
        "steps": [(BC60, DESCK, 0x70, 0, 0)]}
    C["bc60-two-second"] = {
        "desc": {DESCK: dict(D2, head=N1, tail=N2)},
        "mask": 1 << DESCK, "qcount": 1, "tagep": 0,
        "nodes": {N1: nd(N1, 0x80, nxt=N2, pn=N2),
                  N2: nd(N2, 0x140, prev=N1, pp=N1)},
        "watch": W_N1 + W_N2 + W_DSC + W_PG,
        "steps": [(BC60, DESCK, 0x100, 0, 0)]}
    C["bc60-neg-size"] = {
        "desc": {DESCK: dict(D2, head=N1, tail=N1)},
        "mask": 1 << DESCK, "qcount": 1, "tagep": 1,
        "nodes": {N1: nd(N1, 0x100)},
        "watch": W_N1 + W_DSC,
        "steps": [(BC60, DESCK, 0xFFFFFFFF, 0, 0)]}
    C["bc60-stb3"] = {
        "desc": {DESCK: dict(D2, head=N1, tail=N1)},
        "mask": 1 << DESCK, "qcount": 1, "stb3": 1, "tagep": 0,
        "nodes": {N1: nd(N1, 0x80)},
        "watch": W_N1 + W_DSC,
        "steps": [(BC60, DESCK, 0x80, 0, 0)]}
    C["bc60-coalesce"] = {
        # tail carve: the remainder (rbp=N1) is contiguous with the
        # free predecessor NP — B210 back-walks then B2C0 merges
        "desc": {DESCK: dict(D2, head=NP, tail=N1)},
        "mask": 1 << DESCK, "qcount": 1, "tagep": 0,
        "nodes": {NP: nd(NP, 0x40, nxt=N1, pn=N1),
                  N1: nd(N1, 0x140, prev=NP, pp=NP)},
        "watch": W_NP + W_N1 + W_DSC + W_PG,
        "steps": [(BC60, DESCK, 0x80, 0, 1)]}
    C["bc60-kind-e"] = {
        "desc": {0xE: dict(D2, head=N1, tail=N1)},
        "mask": 1 << 0xE, "qcount": 1, "tagep": 0,
        "nodes": {N1: nd(N1, 0x80)},
        "watch": W_N1 + [(DTAB + 0xE * 0xA8 + 0x90, 0x10)],
        "steps": [(BC60, 0xE, 0x80, 0, 0)]}
    C["bc60-align"] = {
        # size 0x41: +0x3F rounds to 0x80 (not 0x40) — the addend
        # is what pushes it over the boundary
        "desc": {DESCK: dict(D2, head=N1, tail=N1)},
        "mask": 1 << DESCK, "qcount": 1, "tagep": 0,
        "nodes": {N1: nd(N1, 0x140)},
        "watch": [(N1, 0x40), (N1 + 0xC0, 0x40)] + W_DSC + W_PG,
        "steps": [(BC60, DESCK, 0x41, 0, 0)]}
    C["bc60-direct"] = {
        # ctx!=0: carve the caller node directly, tag = b[ctx+0x16]
        "desc": {DESCK: dict(D2, head=N1, tail=N1)},
        "mask": 0, "qcount": 0,
        "nodes": {N1: nd(N1, 0x140, tag=7)},
        "watch": [(N1, 0x40), (N1 + 0xC0, 0x40)] + W_DSC + W_PG,
        "steps": [(BC60, DESCK, 0x80, N1, 0)]}
    C["bc60-direct-nolist"] = {
        "desc": {DESCK: dict(D2)}, "mask": 0, "qcount": 0,
        "nodes": {N1: nd(N1, 0x80, tag=1)},
        "watch": W_N1 + W_DSC + W_PG,
        "steps": [(BC60, DESCK, 0x80, N1, 0)]}
    # ---- direct helpers ----
    C["a490-basic"] = {
        "desc": {DESCK: dict(D2)}, "watch": [(N1, 0x40)],
        "nodes": {N1: nd(N1, 0)},
        "steps": [(A490, DESCK, N1, 0x100, 9)]}
    C["c9d0-mid"] = {
        "nodes": {N1: nd(N1, 0x40, nxt=N2, pn=N2),
                  N2: nd(N2, 0x40, prev=N1, nxt=N3, pp=N1, pn=N3),
                  N3: nd(N3, 0x40, prev=N2, pp=N2)},
        "watch": W_N1 + W_N2 + W_N3,
        "steps": [(C9D0, N2, 1)]}
    C["b5f0-min"] = {
        # slot 1 head exists at a higher address -> blk wins
        "desc": {DESCK: dict(D2)},
        "ptab": {1: N3B}, "bmap": {0: 0x6},
        "watch": W_PG,
        "steps": [(B5F0, DTAB + DESCK * 0xA8, N3)]}
    C["b5f0-keep"] = {
        # slot 1 head already at the lower address -> keep
        "desc": {DESCK: dict(D2)},
        "ptab": {1: N3}, "bmap": {0: 0x6},
        "watch": W_PG,
        "steps": [(B5F0, DTAB + DESCK * 0xA8, N3B)]}
    C["c900-swap"] = {
        # head's +8 next is in the same 64KB page -> becomes head
        "desc": {DESCK: dict(D2)},
        "ptab": {1: N3}, "bmap": {0: 0x6},
        "nodes": {N3: nd(N3, 0x40, nxt=N3B)},
        "watch": W_PG + W_N3,
        "steps": [(C900, DTAB + DESCK * 0xA8, N3)]}
    C["c900-clear"] = {
        # head's +8 next is in a different page -> head 0 + bit clear
        "desc": {DESCK: dict(D2)},
        "ptab": {1: N3}, "bmap": {0: 0x6},
        "nodes": {N3: nd(N3, 0x40, nxt=N4)},
        "watch": W_PG + W_N3,
        "steps": [(C900, DTAB + DESCK * 0xA8, N3)]}
    C["b210-merge"] = {
        # N1,N2 adjacent frees; insert-at-end path merges both
        "desc": {DESCK: dict(D2, head=N1, tail=N2)},
        "nodes": {N1: nd(N1, 0x40, nxt=N2, pn=N2),
                  N2: nd(N2, 0x40, prev=N1, pp=N1)},
        "watch": W_N1 + W_N2 + W_DSC + W_PG,
        "steps": [(B210, DTAB + DESCK * 0xA8, N2)]}
    C["b670-corrupt"] = {
        # blk stamped w[+0x3E]!=0 -> A570 boundary + hook cell
        "nodes": {N1: nd(N1, 0x40), N2: nd(N2, 0x40, w3e=1)},
        "steps": [(B670, N1, N2)]}
    C["b730-splice"] = {
        "nodes": {N1: nd(N1, 0x40, nxt=N3), N2: nd(N2, 0x40),
                  N3: nd(N3, 0x40, prev=N1)},
        "watch": W_N1 + W_N2 + W_N3,
        "steps": [(B730, N3, N2)]}
    C["b7f0-phys"] = {
        "nodes": {N1: nd(N1, 0x40, pn=N3), N2: nd(N2, 0x40),
                  N3: nd(N3, 0x40, pp=N1)},
        "watch": W_N1 + W_N2 + W_N3,
        "steps": [(B7F0, N1, N2)]}
    return C


# ---------------- mutants ----------------
def B(v): return bytes([v])

MUTS = [
    # BC60: gate cell QCOUNT -> ST_W (reads wrong count)
    ("m-gate-cell",  0x36BC81, B(0x3B), B(0x3C), "bc60-empty"),
    # BC60: gate jne -> je (spins when count!=0)
    ("m-gate-jne",   0x36BC85, B(0x75), B(0x74), "bc60-empty"),
    # BC60: align addend 0x3F -> 0x3E (size 0x41: 0x80 -> 0x40)
    ("m-align-add",  0x36BC94, B(0x3F), B(0x3E), "bc60-align"),
    # BC60: align mask C0 -> E0 (32-align)
    ("m-align-mask", 0x36BCA0, B(0xC0), B(0xE0), "bc60-head-split"),
    # BC60: kind bound 0xE -> 0xD
    ("m-kind-bound", 0x36BCA3, B(0x0E), B(0x0D), "bc60-kind-e"),
    # BC60: desc stride 0xA8 -> 0xA0
    ("m-desc-str",   0x36BCB3, B(0xA8), B(0xA0), "bc60-head-exact"),
    # BC60: live mark +2 -> +3
    ("m-live-off",   0x36BCC7, B(0x02), B(0x03), "bc60-head-exact"),
    # BC60: mask cell MASKG -> QCOUNT
    ("m-mask-cell",  0x36BCD4, B(0xE0), B(0xE4), "bc60-head-exact"),
    # BC60: mask jb -> jae (bit set returns 0)
    ("m-mask-jb",    0x36BCDB, B(0x72), B(0x73), "bc60-head-exact"),
    # BC60: node key +0x18 -> +0x1C
    ("m-key-off",    0x36BD06, B(0x18), B(0x1C), "bc60-two-best"),
    # BC60: found jge -> jl
    ("m-found-jge",  0x36BD07, B(0x7D), B(0x7C), "bc60-two-second"),
    # BC60: head-walk link +8 -> +4
    ("m-walk-link",  0x36BD0B, B(0x08), B(0x04), "bc60-two-second"),
    # BC60: head-carve remainder +0x40 -> +0x30
    ("m-rem-off",    0x36BDBF, B(0x40), B(0x30), "bc60-head-split"),
    # BC60: remainder size -0x40 -> -0x30
    ("m-rem-size",   0x36BDDF, B(0x40), B(0x30), "bc60-head-split"),
    # BC60: root update +0x90 -> +0x98
    ("m-root-off",   0x36BDF0, B(0x90), B(0x98), "bc60-exact-phys"),
    # BC60: arg4 OR +0x15 -> +0x14
    ("m-arg4-off",   0x36BE69, B(0x15), B(0x14), "bc60-tail-split"),
    # BC60: alloc bit +0x14 -> +0x15
    ("m-alloc-off",  0x36BE80, B(0x14), B(0x15), "bc60-head-exact"),
    # BC60: tag byte +0x16 -> +0x15
    ("m-tag-off",    0x36BE90, B(0x16), B(0x15), "bc60-direct"),
    # BC60: usage base +0x68 -> +0x6C
    ("m-use-base",   0x36BFB1, B(0x68), B(0x6C), "bc60-head-exact"),
    # BC60: seq inc +0x60 -> +0x62
    ("m-seq-off",    0x36BFC8, B(0x60), B(0x62), "bc60-head-exact"),
    # BC60: return +0x40 -> +0x38
    ("m-ret-off",    0x36BFBA, B(0x40), B(0x38), "bc60-head-exact"),
    # A490: magic 0xFF12 -> 0xFF13
    ("m-magic",      0x36A4A9, B(0x12), B(0x13), "a490-basic"),
    # A490: seq field +0x1C -> +0x1E
    ("m-hdr-seq",    0x36A51A, B(0x1C), B(0x1E), "a490-basic"),
    # A490: size field +0x18 -> +0x14
    ("m-hdr-size",   0x36A511, B(0x18), B(0x14), "a490-basic"),
    # C9D0: stamp 0xFF99 -> 0xFF98
    ("m-stamp",      0x36CA93, B(0x99), B(0x98), "c9d0-mid"),
    # C9D0: flag je -> jne (pair-2 unlink skipped)
    ("m-c9d0-flag",  0x36CA50, B(0x74), B(0x75), "c9d0-mid"),
    # B5F0: slot sar 0x10 -> 0x11
    ("m-slot-sh",    0x36B611, B(0x10), B(0x11), "b5f0-min"),
    # B5F0: bitmap or -> and (clears instead of sets)
    ("m-bitmap-op",  0x36B668, B(0x09), B(0x21), "b5f0-min"),
    # B670: corrupt check +0x3E -> +0x3C
    ("m-corrupt",    0x36B686, B(0x3E), B(0x3C), "b670-corrupt"),
    # B2C0: size add +0x18 -> +0x1C
    ("m-merge-off",  0x36B3BE, B(0x18), B(0x1C), "b210-merge"),
]


def run_one_case(name, case, raw, secs, mut=None):
    if mut:
        _, va, exp, new, _ = mut
        got = img_byte(raw, secs, va)
        if got != exp[0]:
            return {"site": "bad", "want": exp[0], "got": got}
        case = dict(case)
        case["patch_bytes"] = [(va, new)]
    w = World(case, raw, secs)
    w.run()
    nat = w.obs()
    mod = run_model(case, raw, secs)
    return {"diff": differs(nat, mod), "nat": nat, "mod": mod}


def main():
    raw, secs = load_image()
    cs = cases()
    out = {"cases": {}, "mutants": {}}
    for name, case in cs.items():
        r = run_one_case(name, case, raw, secs)
        if r.get("site") == "bad":
            out["cases"][name] = {"ok": False, "site": r}
            print("BAD SITE (case setup)", name, r)
            continue
        ok = not r["diff"]
        out["cases"][name] = {"ok": ok, "diff": r["diff"],
                              "nat": r["nat"], "mod": r["mod"]}
        print(("PASS" if ok else "FAIL"), name, r["diff"] or "")
    for m in MUTS:
        name, va, exp, new, cname = m
        r = run_one_case(name, cs[cname], raw, secs, mut=m)
        if r.get("site") == "bad":
            out["mutants"][name] = {"ok": False, "site": r}
            print("BAD SITE", name, hex(va), r)
            continue
        killed = bool(r["diff"])
        out["mutants"][name] = {"killed": killed, "diff": r["diff"]}
        print(("KILL" if killed else "ALIVE"), name, r["diff"])
    json.dump(out, open("result.json", "w"), indent=1, default=str)
    npass = sum(1 for v in out["cases"].values() if v["ok"])
    nkill = sum(1 for v in out["mutants"].values() if v.get("killed"))
    print("functional: %d/%d  mutants: %d/%d killed"
          % (npass, len(cs), nkill, len(MUTS)))


if __name__ == "__main__":
    main()
