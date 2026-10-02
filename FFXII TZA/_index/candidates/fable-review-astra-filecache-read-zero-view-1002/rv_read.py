"""rv_read.py - FABLE independent re-derivation for ASTRA packet filecache-read-zero-view (4a818c6d3).

Own reader (rvlib.py: struct + capstone 5, copied unchanged from the route2-commit-key review) plus the reviewer's own
sandbox (unicorn over a private copy of the image's sections, every callee and import answered by a recording stub).
Does not import ASTRA's prove.py, capture drivers, freeze/publication scripts or reg_tracking.py.

Method: complete decode of Read 0059D4B0 (.pdata) and the retained 27-byte IsOpen 0059D920 (int3-bounded); every
entry -> ret path enumerated; each guard's width and signedness from capstone's operand detail; the import resolved
from the PE import directory; frame arithmetic for the count slot and the fifth argument; then every arm run in the
sandbox with width-sensitive field values, the ReadFile stub writing or not writing the count, and the composed
zero view (constructor -> resolver -> route-1 hit -> NULL allocation) read with zero and non-zero sizes.  Controls
patch a private in-memory copy of the image and require at least one named check to fail.
"""

# ==== common reviewer helpers (identical text in the four FABLE filecache 1002 reviews) ====
import hashlib
import json
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rvlib import Img, Body, Report, check_manifest, find_exe, SHA256 as SHA_PIN  # noqa: E402

from unicorn import Uc, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE, UC_HOOK_MEM_WRITE  # noqa: E402
from unicorn.x86_const import (UC_X86_REG_RAX, UC_X86_REG_RBX, UC_X86_REG_RCX, UC_X86_REG_RDX,  # noqa: E402
                               UC_X86_REG_RSI, UC_X86_REG_RDI, UC_X86_REG_RBP, UC_X86_REG_RSP,
                               UC_X86_REG_R8, UC_X86_REG_R9, UC_X86_REG_R10, UC_X86_REG_R11,
                               UC_X86_REG_R12, UC_X86_REG_R13, UC_X86_REG_R14, UC_X86_REG_R15,
                               UC_X86_REG_RIP)

EV_ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(find_exe())))),
                       "FFXII TZA", "_experiments", "evidence")


class Rep(Report):
    def __init__(self, title):
        Report.__init__(self, title)
        self.n = 0
        self.failed = []

    def check(self, name, cond, detail=""):
        self.n += 1
        if not cond:
            self.failed.append(name)
        return Report.check(self, name, cond, detail)


def T(B, a):
    I = B.ins.get(a)
    return I.text if I else "<no boundary>"


def writers(B, fam, lo=None, hi=None):
    return [a for a in B.order if fam in B[a].reg_writes and (lo is None or lo <= a) and (hi is None or a < hi)]


def rets_of(B):
    return [a for a in B.order if B[a].mnemonic == "ret"]


def on_paths(B, src, dst):
    """Instructions on some path src -> dst that does not pass dst first (dst excluded)."""
    fwd = B.reach(src, avoid=[dst])
    P = {}
    for a in B.order:
        for s in B.succ(a):
            P.setdefault(s, set()).add(a)
    back, st = set(), [dst]
    while st:
        a = st.pop()
        for q in P.get(a, ()):
            if q not in back:
                back.add(q)
                st.append(q)
    return fwd & back


def all_paths(B, frm, stop):
    """Every simple path frm -> an address in `stop` (or a ret / leaving the body) over B's local CFG."""
    out = []
    st = [(frm, (frm,))]
    while st:
        a, p = st.pop()
        if a in stop:
            out.append(p)
            continue
        nx = B.succ(a)
        if not nx:
            out.append(p)
            continue
        for n in nx:
            if n in p:
                raise ValueError("cycle at %X" % n)
            st.append((n, p + (n,)))
    return out


def leaf_bounds(img, s, e):
    """A body with no .pdata record: int3 before the entry, int3 (or the next .pdata entry) at the end."""
    return (img.pdata(s) is None and img.pdata(e - 1) is None and img.read(s - 1, 1) == b"\xcc" and
            img.read(e, 1) == b"\xcc")


def import_of_slot(img, slot_va):
    """(dll, name) for an IAT slot, read from the PE import directory (OriginalFirstThunk hint/name)."""
    d = img.d
    pe = struct.unpack_from("<I", d, 0x3C)[0]
    irva = struct.unpack_from("<I", d, pe + 24 + 112 + 8)[0]
    srva = slot_va - img.base
    o = img.off(img.base + irva)
    while True:
        oft, ts, fc, name, ft = struct.unpack_from("<IIIII", d, o)
        if not (oft or name or ft):
            return None
        i = 0
        while img.u64(img.base + ft + 8 * i):
            if ft + 8 * i == srva:
                ov = img.u64(img.base + (oft or ft) + 8 * i)
                dll = img.read(img.base + name, 64).split(b"\0")[0].decode()
                nm = "ordinal" if ov >> 63 else img.read(img.base + ov + 2, 64).split(b"\0")[0].decode()
                return dll, nm, img.base + ov
            i += 1
        o += 20


def rip_slot(I):
    """Absolute address of a rip-relative memory operand."""
    m = I.mems[0]
    return I.address + I.size + m["disp"]


def range_hashes(img, files):
    """Packet range files -> (ranges, mismatching starts) against this image."""
    got, bad = [], []
    for f in files:
        for r in json.load(open(f))["ranges"]:
            s_, e_ = int(r["start"], 16), int(r["end_exclusive"], 16)
            got.append((s_, e_))
            if hashlib.sha256(img.read(s_, e_ - s_)).hexdigest() != r["sha256"]:
                bad.append(r["start"])
    return got, bad


# ---------------- the reviewer's own sandbox: original bytes, recording stubs for every callee ----------------
STUB = 0x70000000       # every import slot is pointed into this page
RETM = 0x7F000000       # return address of the outermost frame; reaching it ends the run
OBJ = 0x50000000        # objects the review builds
HEAP = 0x58000000
STK = 0x60000000
JUNK = 0xA5A5A5A5A5A5A5A5
GPRS = [("rax", UC_X86_REG_RAX), ("rbx", UC_X86_REG_RBX), ("rcx", UC_X86_REG_RCX), ("rdx", UC_X86_REG_RDX),
        ("rsi", UC_X86_REG_RSI), ("rdi", UC_X86_REG_RDI), ("rbp", UC_X86_REG_RBP), ("r8", UC_X86_REG_R8),
        ("r9", UC_X86_REG_R9), ("r10", UC_X86_REG_R10), ("r11", UC_X86_REG_R11), ("r12", UC_X86_REG_R12),
        ("r13", UC_X86_REG_R13), ("r14", UC_X86_REG_R14), ("r15", UC_X86_REG_R15)]
RID = dict(GPRS)
VOLATILE = ("rcx", "rdx", "r8", "r9", "r10", "r11")


class Sandbox(object):
    """Unicorn over a private copy of the image's sections.  Code inside `bodies` runs as shipped; reaching any other
    address (a direct callee, or an import through the IAT, whose slots are pointed at STUB) is recorded as a call and
    answered by a stub: the stub may write memory, returns a value in RAX, clobbers the volatile argument registers
    with junk (Win64 ABI) and returns to the caller.  Not native execution of the game."""

    def __init__(self, img, bodies, stubs=None):
        self.img = img
        self.bodies = list(bodies)
        self.stubs = stubs or {}
        mu = Uc(UC_ARCH_X86, UC_MODE_64)
        d = img.d
        pe = struct.unpack_from("<I", d, 0x3C)[0]
        soi = struct.unpack_from("<I", d, pe + 24 + 56)[0]
        mu.mem_map(img.base, (soi + 0xFFF) & ~0xFFF)
        for name, va, vs, ra, rs in img.secs:
            mu.mem_write(img.base + va, d[ra:ra + min(vs, rs)])
        iat_rva, iat_sz = struct.unpack_from("<II", d, pe + 24 + 112 + 12 * 8)
        self.slot_of_stub = {}
        for i in range(iat_sz // 8):
            if img.u64(img.base + iat_rva + 8 * i):
                mu.mem_write(img.base + iat_rva + 8 * i, struct.pack("<Q", STUB + 16 * i))
                self.slot_of_stub[STUB + 16 * i] = img.base + iat_rva + 8 * i
        for a in (STUB, RETM):
            mu.mem_map(a, 0x10000)
            mu.mem_write(a, b"\xcc" * 0x10000)
        mu.mem_map(OBJ, 0x100000)
        mu.mem_map(HEAP, 0x100000)
        mu.mem_map(STK, 0x100000)
        self.mu = mu
        self.events = []     # ("call", target, slot_or_None, args) / ("w", pc, addr, size, value)
        self.trace = []
        self.pc = None
        mu.hook_add(UC_HOOK_CODE, self._code)
        mu.hook_add(UC_HOOK_MEM_WRITE, self._write)

    def inside(self, a):
        return any(s <= a < e for s, e in self.bodies)

    def r(self, n):
        return self.mu.reg_read(RID[n])

    def w(self, n, v):
        self.mu.reg_write(RID[n], v & 0xFFFFFFFFFFFFFFFF)

    def q(self, a):
        return struct.unpack("<Q", bytes(self.mu.mem_read(a, 8)))[0]

    def d32(self, a):
        return struct.unpack("<I", bytes(self.mu.mem_read(a, 4)))[0]

    def setq(self, a, v):
        self.mu.mem_write(a, struct.pack("<Q", v & 0xFFFFFFFFFFFFFFFF))

    def setd(self, a, v):
        self.mu.mem_write(a, struct.pack("<I", v & 0xFFFFFFFF))

    def _code(self, mu, addr, size, ud):
        if addr == RETM:
            mu.emu_stop()
            return
        if self.inside(addr):
            self.trace.append(addr)
            self.pc = addr
            return
        slot = self.slot_of_stub.get(addr)
        key = ("iat", slot) if slot else addr
        args = tuple(self.r(n) for n in ("rcx", "rdx", "r8", "r9"))
        self.events.append(("call", key, args, self.pc))
        fn = self.stubs.get(key)
        rv = fn(self) if fn else 0x5EED00000000C0DE
        for n in VOLATILE:
            self.w(n, JUNK ^ 0x1111)
        self.w("rax", rv)
        rsp = self.mu.reg_read(UC_X86_REG_RSP)
        ret = self.q(rsp)
        self.mu.reg_write(UC_X86_REG_RSP, rsp + 8)
        self.mu.reg_write(UC_X86_REG_RIP, ret)

    def _write(self, mu, access, addr, size, value, ud):
        self.events.append(("w", self.pc, addr, size, value & ((1 << (8 * size)) - 1)))

    def call(self, entry, regs, stack_args=(), limit=200000, until=RETM):
        """Run entry(...) with every GPR = JUNK except `regs`; stack_args are the 5th, 6th ... arguments.  The stack
        below and above the entry SP is refilled with junk bytes first.  `until` stops early at that address."""
        for n, rid in GPRS:
            self.mu.reg_write(rid, JUNK)
        for n, v in regs.items():
            self.w(n, v)
        rsp = STK + 0x80000 - 8
        self.mu.mem_write(STK + 0x60000, bytes([0xA5]) * 0x30000)
        self.setq(rsp, RETM)
        for i, v in enumerate(stack_args):
            self.setq(rsp + 0x28 + 8 * i, v)
        self.mu.reg_write(UC_X86_REG_RSP, rsp)
        self.events, self.trace = [], []
        self.mu.emu_start(entry, until, count=limit)
        if self.mu.reg_read(UC_X86_REG_RIP) != until:
            raise RuntimeError("run of %X did not return (rip %X)" % (entry, self.mu.reg_read(UC_X86_REG_RIP)))
        return self.r("rax")

    def calls(self):
        return [e[1] for e in self.events if e[0] == "call"]

    def writes_in(self, lo, hi):
        return [e for e in self.events if e[0] == "w" and lo <= e[2] < hi]


# ---------------- one composed run: construct -> resolve -> route-1 hit -> 16-byte allocation ----------------
CTOR = (0x00597970, 0x00597A12)
RESOLVER = (0x0059EE90, 0x0059F1FC)
WRAPPER = (0x001D6D20, 0x001D6D6F)
LOOKUP = (0x0020C1B0, 0x0020C2F2)
CREATE = (0x0020C300, 0x0020C438)
ALLOC = (0x00210EC0, 0x00210ECB)
MALLOC_THUNK = (0x0085E730, 0x0085E737)
COOKIE = (0x00808C40, 0x00808C61)
HASH = (0x00674A00, 0x00674A28)
ISOPEN_B = (0x0059D920, 0x0059D93B)
READ_B = (0x0059D4B0, 0x0059D50C)
CLOSE_B = (0x0059BD40, 0x0059BD80)
MALLOC_SLOT = 0x008C2B40
READFILE_SLOT = 0x008C2140
STREAM = OBJ + 0x1000
MGR = OBJ + 0x4000
NODE = OBJ + 0x6000
ENTRY = OBJ + 0x7000
RECSLOT = OBJ + 0x8000
RECORD = OBJ + 0x9000
PATH = OBJ + 0xA000
NAME = b"c\\a.phyre\0"
KEYTEXT = b"A"
ENTRY_SIZE = 0x1234


def key_hash(s):
    """The reviewer's own statement of route 1's key hash (seed 1505h, *33 + signed byte, bit 31 cleared)."""
    h = 0x1505
    for c in s:
        h = (h * 33 + (c - 256 if c > 127 else c)) & 0xFFFFFFFF
    return h & 0x7FFFFFFF


def composed_sandbox(img, malloc_ret=0, kind=2):
    """A private sandbox wired so that a reader constructed on NAME resolves through route 1 to a cache HIT whose
    16-byte allocation returns `malloc_ret`.  Opaque callees are stubs (listed in the returned dict)."""
    st = {}

    def memset(S):
        S.mu.mem_write(S.r("rcx"), bytes([S.r("rdx") & 0xFF]) * (S.r("r8") & 0xFFFF))
        return S.r("rcx")

    def normalise(S):
        S.mu.mem_write(S.r("r8"), KEYTEXT + b"\0")
        return 0

    st[0x1D6B20] = lambda S: 1            # cache enabled
    st[0x865390] = lambda S: 0            # not one of the four forced-selector-5 folders
    st[0x5CDAA0] = lambda S: 0            # log
    st[0x1D6B90] = lambda S: 0            # not low-memory mode
    st[0x1D6B70] = lambda S: 1            # backfill flag (irrelevant on a hit)
    st[0x20C700] = lambda S: MGR          # manager
    st[0x861EC0] = memset
    st[0x20C440] = normalise              # normalised key "A"
    st[0x5CD4F0] = lambda S: 0            # lock
    st[0x5CD820] = lambda S: 0            # unlock
    st[0x20B5F0] = lambda S: RECSLOT      # find-or-insert returns the node's value slot
    st[("iat", MALLOC_SLOT)] = lambda S: malloc_ret
    st[0x217A60] = lambda S: S.r("rcx")   # view constructor returns this
    st[0x1C26B0] = lambda S: HEAP + 0x100  # strdup
    st[("iat", READFILE_SLOT)] = lambda S: 1
    S = Sandbox(img, [CTOR, RESOLVER, WRAPPER, LOOKUP, CREATE, ALLOC, MALLOC_THUNK, COOKIE, HASH, ISOPEN_B, READ_B,
                      CLOSE_B], st)
    S.mu.mem_write(STREAM, b"\xcd" * 0x60)
    S.mu.mem_write(PATH, NAME)
    S.setq(MGR + 0x38, NODE)
    S.setq(MGR + 0x18, MGR + 0x800)
    S.setd(MGR + 0x88, 0x10)
    S.setq(NODE + 0, 0)
    S.setq(NODE + 8, 0)
    S.setd(NODE + 0x20, key_hash(KEYTEXT))
    S.setq(NODE + 0x28, ENTRY)
    S.setq(ENTRY + 0, HEAP + 0x200)
    S.setd(ENTRY + 8, ENTRY_SIZE)
    S.setd(ENTRY + 0x14, kind)
    S.setq(RECSLOT, RECORD)
    S.mu.mem_write(RECORD + 0x10, b"\x03")
    return S


def construct(S, selector=3):
    rv = S.call(CTOR[0], {"rcx": STREAM, "rdx": PATH, "r8": selector})
    return rv


def fields(S):
    return {"q28": S.q(STREAM + 0x28), "q30": S.q(STREAM + 0x30), "q40": S.q(STREAM + 0x40),
            "d20": S.d32(STREAM + 0x20), "d48": S.d32(STREAM + 0x48), "b38": S.q(STREAM + 0x38) & 0xFF}


def safe(R, name, fn, detail=""):
    """Run an emulation-backed check; an exception is a FAIL of that named check, not a crash of the review."""
    try:
        ok, det = fn()
    except Exception as e:  # noqa: BLE001
        ok, det = False, "raised %r" % (e,)
    return R.check(name, ok, det or detail)


def run_review(title, checks, packet, controls, null_va):
    img = Img.load()
    R = Rep(title)
    print("== packet integrity")
    packet(img, R)
    print("== shipping-image re-derivation")
    checks(img, R)
    print("== controls (each patched private image must FAIL at least one check above)")
    Rn = Rep("null control")
    Rn.quiet = True
    checks(img.patched(null_va, img.read(null_va, 4)), Rn)
    R.check("null control: an unchanged private copy (sha check off) passes every image check",
            Rn.fails == 0 and Rn.n > 0, "%d of %d" % (Rn.n - Rn.fails, Rn.n))
    nctl = 0
    for label, va, nb in controls:
        P = img.patched(va, nb)
        if P.d == img.d:
            raise SystemExit("control %s did not change the image" % label)
        Rc = Rep(label)
        Rc.quiet = True
        try:
            checks(P, Rc)
            failed = Rc.fails
            why = "%d failed: %s" % (failed, "; ".join(Rc.failed[:3]))
        except Exception as e:  # noqa: BLE001
            failed = 1
            why = "refused: %r" % (e,)
        nctl += 1
        R.check("control: " + label, failed > 0, why)
    disk = hashlib.sha256(open(find_exe(), "rb").read()).hexdigest()
    R.check("exe on disk still hashes to the pinned sha256 after all controls", disk == SHA_PIN, disk)
    print("TOTAL: %d checks, %d PASS, %d FAIL (%d controls)" % (R.n, R.n - R.fails, R.fails, nctl))

# ==== end of common helpers ====

SLUG = "filecache-read-zero-view"
MANIFEST_SHA = "43e05ee2e8590e069317987d26526716c7f59833018855d8315528c75901e7f2"
OPEN_MANIFEST_SHA = "7479a4f8d544249b398a57419aab50ac4296bc14eb717c4517cd478320ad2f45"
M64 = 0xFFFFFFFFFFFFFFFF
BUFMARK = 0x5EED0000000B0F00
CACHEMARK = 0x5EED00000000CAC4
DST = HEAP + 0x800
ENTRY_SP = STK + 0x80000 - 8


def read_sandbox(img, count_written=0x0C, bool_ret=1):
    seen = {}

    def readfile(S):
        rsp = S.mu.reg_read(UC_X86_REG_RSP)
        seen["args"] = (S.r("rcx"), S.r("rdx"), S.r("r8"), S.r("r9"), S.q(rsp + 0x28))
        if count_written is not None:
            S.setd(S.r("r9"), count_written)
        return bool_ret
    st = {0x2150E0: lambda S: BUFMARK, 0x1D6CA0: lambda S: CACHEMARK, ("iat", READFILE_SLOT): readfile}
    S = Sandbox(img, [READ_B, ISOPEN_B], st)
    S.seen = seen
    return S


def run_read(S, q28, q30, q40, n):
    S.mu.mem_write(STREAM, b"\xcd" * 0x60)
    S.setq(STREAM + 0x28, q28)
    S.setq(STREAM + 0x30, q30)
    S.setq(STREAM + 0x40, q40)
    S.seen.clear()
    rv = S.call(READ_B[0], {"rcx": STREAM, "rdx": DST, "r8": n})
    return rv, S.calls(), S.writes_in(OBJ, OBJ + 0x100000)


def checks(img, R):
    RD = Body(img, *READ_B)
    IO = Body(img, *ISOPEN_B)

    ents, ok = img.pdata_cover(*READ_B)
    R.check("Read 0059D4B0 + 0x5C (92 B) decodes exactly and one .pdata record covers it exactly",
            RD.exact and ok and len(ents) == 1)
    rets, tails, outs = RD.exits()
    R.check("closed local CFG: three rets (+0x19, +0x48, +0x5B), no tail or out-of-body branch",
            rets == [0x59D4C9, 0x59D4F8, 0x59D50B] and not tails and not outs)
    paths = all_paths(RD, RD.start, set(rets))
    R.check("exactly five entry -> ret paths", len(paths) == 5, "%d" % len(paths))
    R.check("retained IsOpen 0059D920 + 0x1B (27 B) decodes exactly, int3-bounded, same ten instructions",
            IO.exact and len(IO.order) == 10 and leaf_bounds(img, *ISOPEN_B) and
            T(IO, 0x59D92E) == "cmp qword ptr [rcx + 0x40], -1")

    R.check("buffer test is full 64-bit: `mov rax, qword ptr [rcx + 0x30]` (8 B) / `test rax, rax` / `je 0x59d4ca`",
            T(RD, 0x59D4B4) == "mov rax, qword ptr [rcx + 0x30]" and RD[0x59D4B4].mems[0]["size"] == 8 and
            T(RD, 0x59D4B8) == "test rax, rax" and T(RD, 0x59D4BB) == "je 0x59d4ca")
    ba = RD.reach(0x59D4BD)
    R.check("non-zero buffer: rcx = buffer, the first and only call is 002150E0 (+0x10), then ret with its RAX",
            T(RD, 0x59D4BD) == "mov rcx, rax" and [RD[x].direct_target() for x in ba if RD[x].mnemonic == "call"]
            == [0x2150E0] and not [x for x in ba if x > 0x59D4C0 and "rax" in RD[x].reg_writes])
    R.check("zero buffer: `mov dword ptr [rsp + 0x40], eax` (+0x1A) stores EAX = 0 into entry SP+8 (frame 38h, the "
            "caller's home slot) before any other test", T(RD, 0x59D4CA) == "mov dword ptr [rsp + 0x40], eax" and
            T(RD, 0x59D4B0) == "sub rsp, 0x38" and 0x40 - 0x38 == 8 and RD[0x59D4CA].mems[0]["size"] == 4)
    tr = RD[0x59D4CE]
    R.check("size guard is the low 32 bits only: `test r8d, r8d` (+0x1E) / `je 0x59d507`",
            T(RD, 0x59D4CE) == "test r8d, r8d" and tr.bytes[0] == 0x45 and T(RD, 0x59D4D1) == "je 0x59d507")
    R.check("handle test is full 64-bit: `mov r10, qword ptr [rcx + 0x28]` / `cmp r10, -1` / `je 0x59d4f9`",
            T(RD, 0x59D4D3) == "mov r10, qword ptr [rcx + 0x28]" and RD[0x59D4D3].mems[0]["size"] == 8 and
            T(RD, 0x59D4D7) == "cmp r10, -1" and RD[0x59D4D7].bytes[0] == 0x49 and T(RD, 0x59D4DB) == "je 0x59d4f9")
    ci = RD[0x59D4EA]
    imp = import_of_slot(img, rip_slot(ci)) if ci.mems else None
    R.check("the handle arm calls through IAT 008C2140 = KERNEL32.dll!ReadFile (PE import directory)",
            ci.mnemonic == "call" and ci.mems and rip_slot(ci) == READFILE_SLOT and imp and
            imp[:2] == ("KERNEL32.dll", "ReadFile"), str(imp))
    R.check("ReadFile arguments: rcx = handle, rdx/r8 the caller's (no rdx/r8 writer in the body), r9 = &[rsp+40h] "
            "(the pre-zeroed count slot), fifth [rsp+20h] = rax (0 on this arm)",
            T(RD, 0x59D4DD) == "lea r9, [rsp + 0x40]" and T(RD, 0x59D4E2) == "mov qword ptr [rsp + 0x20], rax" and
            T(RD, 0x59D4E7) == "mov rcx, r10" and not writers(RD, "rdx") and not writers(RD, "r8"))
    R.check("after ReadFile, `mov eax, dword ptr [rsp + 0x40]` (+0x40, 4 B, zero-extending) replaces the API return",
            T(RD, 0x59D4F0) == "mov eax, dword ptr [rsp + 0x40]" and RD[0x59D4F0].mems[0]["size"] == 4 and
            RD.order[RD.order.index(0x59D4EA) + 1] == 0x59D4F0)
    R.check("cache arm: `mov rcx, qword ptr [rcx + 0x40]` / `test rcx, rcx` / `jle 0x59d507` (signed <= 0 skips), "
            "else call 001D6CA0",
            T(RD, 0x59D4F9) == "mov rcx, qword ptr [rcx + 0x40]" and RD[0x59D4F9].mems[0]["size"] == 8 and
            T(RD, 0x59D4FD) == "test rcx, rcx" and T(RD, 0x59D500) == "jle 0x59d507" and
            RD[0x59D502].direct_target() == 0x1D6CA0)
    nocall = [p for p in paths if not any(RD[x].mnemonic == "call" for x in p)]
    R.check("the two no-call paths end at +0x5B and their only rax writer is the +0x4 qword load (RAX = the zero "
            "buffer value)", len(nocall) == 2 and all(p[-1] == 0x59D50B for p in nocall) and
            all([x for x in p if "rax" in RD[x].reg_writes] == [0x59D4B4] for p in nocall))
    owr = [(a, m["base"]) for a, m in RD.mem_writes() if m["base"] != "rsp"]
    R.check("Read writes no memory except its own stack/home slots (no stream write)", not owr, str(owr))

    def arms():
        S = read_sandbox(img)
        cases = [
            ("buffer", (M64, HEAP, 0, 0x10), [0x2150E0], BUFMARK),
            ("buffer high half", (M64, 0x100000000, 0, 0x10), [0x2150E0], BUFMARK),
            ("size 0", (M64, 0, 0, 0), [], 0),
            ("size high half only, handle bound", (0x44, 0, 0, 0x100000000), [], 0),
            ("handle", (0x44, 0, 0, 0x10), [("iat", READFILE_SLOT)], 0x0C),
            ("handle FFFFFFFF", (0xFFFFFFFF, 0, 0, 0x10), [("iat", READFILE_SLOT)], 0x0C),
            ("cache positive", (M64, 0, 0x77, 0x10), [0x1D6CA0], CACHEMARK),
            ("cache FFFFFFFF", (M64, 0, 0xFFFFFFFF, 0x10), [0x1D6CA0], CACHEMARK),
            ("cache 0", (M64, 0, 0, 0x10), [], 0),
            ("cache -1", (M64, 0, M64, 0x10), [], 0),
            ("cache min", (M64, 0, 0x8000000000000000, 0x10), [], 0),
        ]
        bad = []
        for name, (q28, q30, q40, n), want_calls, want_rax in cases:
            rv, cl, wr = run_read(S, q28, q30, q40, n)
            if cl != want_calls or rv != want_rax or wr:
                bad.append((name, "%X" % rv, cl, len(wr)))
        return not bad, "%d cases, bad %s" % (len(cases), bad)
    safe(R, "sandbox, eleven arm cases (buffer, size, handle, cache; width- and sign-sensitive values): calls and full "
            "RAX as derived, no stream write", arms)

    def rf_args():
        S = read_sandbox(img, count_written=0x0C, bool_ret=1)
        rv, cl, wr = run_read(S, 0x44, 0, 0, 0x110)
        a = S.seen.get("args")
        ok = a is not None and a[0] == 0x44 and a[1] == DST and a[2] & 0xFFFFFFFF == 0x110 and \
            a[3] == ENTRY_SP + 8 and a[4] == 0 and rv == 0x0C
        S2 = read_sandbox(img, count_written=None, bool_ret=0)
        rv2, cl2, wr2 = run_read(S2, 0x44, 0, 0, 0x110)
        return ok and rv2 == 0, "args %s rax %X; no count written -> rax %X" % (
            a and ["%X" % x for x in a], rv, rv2)
    safe(R, "sandbox, ReadFile arm: handle, caller's buffer and size, &count = entry SP+8, lpOverlapped 0; RAX = the "
            "DWORD count (BOOL ignored); a call that writes no count returns 0 (slot pre-zeroed)", rf_args)

    def witness():
        S = read_sandbox(img)
        S.setq(STREAM + 0x28, M64)
        S.setq(STREAM + 0x30, 0)
        S.setq(STREAM + 0x40, 0)
        al = S.call(ISOPEN_B[0], {"rcx": STREAM}) & 0xFF
        out = []
        for n in (0, 0x100):
            rv, cl, wr = run_read(S, M64, 0, 0, n)
            out.append((rv, cl, len(wr)))
        return al == 1 and out == [(0, [], 0), (0, [], 0)], "IsOpen AL %d; Read %s" % (al, out)
    safe(R, "witness q28 = -1, q30 = 0, q40 = 0: IsOpen AL 1; Read with size 0 and 0x100 returns full RAX 0 with no "
            "call and no stream write", witness)

    def composed():
        S = composed_sandbox(img, malloc_ret=0)
        S.call(CTOR[0], {"rcx": STREAM, "rdx": PATH, "r8": 3})
        al = S.call(ISOPEN_B[0], {"rcx": STREAM}) & 0xFF
        out = []
        for n in (0, 0x100):
            rv = S.call(READ_B[0], {"rcx": STREAM, "rdx": DST, "r8": n})
            out.append((rv, S.calls(), len(S.writes_in(STREAM, STREAM + 0x60))))
        return al == 1 and out == [(0, [], 0), (0, [], 0)], "IsOpen AL %d; Read %s" % (al, out)
    safe(R, "sandbox, the composed zero view (constructor -> resolver -> route-1 hit -> NULL allocation): IsOpen AL 1, "
            "Read returns 0 with no call for size 0 and 0x100", composed)


def packet(img, R):
    check_manifest(R, SLUG, MANIFEST_SHA)
    ev = os.path.join(EV_ROOT, SLUG)
    got, bad = range_hashes(img, [os.path.join(ev, f) for f in ("source-01.json", "retained-open/source-01.json")])
    R.check("packet's captured and retained range sha256 values equal this image (%d ranges: Read, IsOpen)" % len(got),
            not bad and READ_B in got and ISOPEN_B in got, str(bad))
    h = hashlib.sha256(open(os.path.join(ev, "retained-open", "manifest.json"), "rb").read()).hexdigest()
    R.check("retained IsOpen manifest = filecache-open-sentinel's committed manifest (7479a4f8...)", h == OPEN_MANIFEST_SHA,
            h)
    R.check("metadata-correction-01.json is present (producer01's inherited Close metadata corrected before "
            "publication)", os.path.exists(os.path.join(ev, "metadata-correction-01.json")))


CONTROLS = [
    ("Read + 0x1E `test r8d, r8d` -> `test r8, r8` (size guard widened)", 0x59D4CE, bytes.fromhex("4d85c0")),
    ("Read + 0x4 `mov rax, [rcx+30h]` -> `mov eax, [rcx+30h]; nop` (buffer read narrowed)", 0x59D4B4,
     bytes.fromhex("8b413090")),
    ("Read + 0x50 `jle` -> `jl` (cache 0 would call)", 0x59D500, bytes([0x7C])),
    ("Read + 0x40 `mov eax, [rsp+40h]` -> four nops (API BOOL returned)", 0x59D4F0, bytes([0x90] * 4)),
    ("Read + 0x3A call through IAT slot + 8 (SetEndOfFile)", 0x59D4EC, struct.pack("<i", 0x324C50 + 8)),
    ("Read + 0x1A `mov [rsp+40h], eax` -> four nops (count slot not pre-zeroed)", 0x59D4CA, bytes([0x90] * 4)),
    ("Read + 0x27 `cmp r10, -1` -> `cmp r10d, -1` (handle sentinel narrowed)", 0x59D4D7, bytes.fromhex("4183faff")),
    ("IsOpen + 0xE `cmp [rcx+40h], -1` -> `cmp [rcx+40h], 0` (retained predicate rejects the zero view)", 0x59D932,
     bytes([0x00])),
]


if __name__ == "__main__":
    run_review("rv_read", checks, packet, CONTROLS, 0x59D4B0)
