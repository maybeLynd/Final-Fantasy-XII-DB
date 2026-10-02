"""rv_close.py - FABLE independent re-derivation for ASTRA packet filecache-close-zero-sentinel (a30d4772a).

Own reader (rvlib.py: struct + capstone 5, copied unchanged from the route2-commit-key review) plus the reviewer's own
sandbox (unicorn over a private copy of the image's sections, every callee and import answered by a recording stub).
Does not import ASTRA's prove.py, capture drivers, freeze/publication scripts or reg_tracking.py.

Method: complete decode of Close 0059BD40 (.pdata) and the retained 27-byte IsOpen 0059D920 (int3-bounded); the four
entry -> ret paths enumerated with their calls and stores; guard width and signedness from capstone's operand detail;
dominance of the single `mov al, 1`; then Close run in the sandbox on the zero-view witness, on the four partitions,
and on a 96-case field grid followed by IsOpen, to state exactly when "Close returned true" is followed by IsOpen
false; finally the composed zero view (constructor -> resolver -> route-1 hit -> NULL allocation) closed and re-tested.
Controls patch a private in-memory copy of the image and require at least one named check to fail.
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

SLUG = "filecache-close-zero-sentinel"
MANIFEST_SHA = "460bdc9fcf554fb303a899edab7fb61db66ea05e36e84ad2879fc24770214d19"
OPEN_MANIFEST_SHA = "7479a4f8d544249b398a57419aab50ac4296bc14eb717c4517cd478320ad2f45"
M64 = 0xFFFFFFFFFFFFFFFF
REL_RET = 0x5EED00000000D0D0
RST_RET = 0x5EED00000000AAA0
KEY48 = 0x2B5E6
GRID28 = (M64, 0, 0x44, 0xFFFFFFFF)
GRID30 = (0, HEAP, 0x100000000)
GRID40 = (M64, M64 - 1, 0, 1, 0x7FFFFFFFFFFFFFFF, 0x8000000000000000, 0x8000000000000001, 0xFFFFFFFF)


def signed(v):
    return v - (1 << 64) if v >> 63 else v


def isopen_after_close(q28, q30, q40):
    """The reviewer's statement: Close leaves +0x28 alone, ends with +0x30 = 0, and sets +0x40 = -1 only when it was
    signed-positive; so the later IsOpen is false exactly when q28 == -1 and (q40 > 0 or q40 == -1)."""
    return 0 if (q28 == M64 and (signed(q40) > 0 or q40 == M64)) else 1


def close_sandbox(img):
    st = {0x2150D0: lambda S: REL_RET, 0x1D6AA0: lambda S: RST_RET}
    return Sandbox(img, [CLOSE_B, ISOPEN_B], st)


def run_close(S, q28, q30, q40):
    S.mu.mem_write(STREAM, b"\xcd" * 0x60)
    S.setq(STREAM + 0x28, q28)
    S.setq(STREAM + 0x30, q30)
    S.setq(STREAM + 0x40, q40)
    S.setd(STREAM + 0x48, KEY48)
    rv = S.call(CLOSE_B[0], {"rcx": STREAM})
    ev = list(S.events)
    al = S.call(ISOPEN_B[0], {"rcx": STREAM}) & 0xFF
    calls = [e for e in ev if e[0] == "call"]
    sw = [(e[2] - STREAM, e[3], e[4]) for e in ev if e[0] == "w" and STREAM <= e[2] < STREAM + 0x60]
    return rv, calls, sw, al


def checks(img, R):
    CL = Body(img, *CLOSE_B)
    IO = Body(img, *ISOPEN_B)

    ents, ok = img.pdata_cover(*CLOSE_B)
    R.check("Close 0059BD40 + 0x40 (64 B) decodes exactly and one .pdata record covers it exactly",
            CL.exact and ok and len(ents) == 1)
    rets, tails, outs = CL.exits()
    R.check("closed local CFG: one ret, the last instruction (+0x3F); no tail or out-of-body branch",
            rets == [0x59BD7F] and CL.order[-1] == 0x59BD7F and not tails and not outs)
    R.check("retained IsOpen 0059D920 + 0x1B (27 B) decodes exactly, int3-bounded, ten instructions",
            IO.exact and len(IO.order) == 10 and leaf_bounds(img, *ISOPEN_B) and
            T(IO, 0x59D92E) == "cmp qword ptr [rcx + 0x40], -1")
    R.check("buffer arm: `mov rcx, qword ptr [rcx + 0x30]` (8 B), `test rcx, rcx`, `je 0x59bd5f`; then call 002150D0 "
            "(rcx = the buffer) and `mov qword ptr [rbx + 0x30], 0` (8 B)",
            T(CL, 0x59BD49) == "mov rcx, qword ptr [rcx + 0x30]" and CL[0x59BD49].mems[0]["size"] == 8 and
            T(CL, 0x59BD4D) == "test rcx, rcx" and T(CL, 0x59BD50) == "je 0x59bd5f" and
            CL[0x59BD52].direct_target() == 0x2150D0 and T(CL, 0x59BD57) == "mov qword ptr [rbx + 0x30], 0" and
            CL[0x59BD57].mems[0]["size"] == 8)
    R.check("cache arm: `mov rdx, qword ptr [rbx + 0x40]` (8 B), `test rdx, rdx`, `jle 0x59bd78` (TEST clears OF, so "
            "JLE = signed <= 0 skips)", T(CL, 0x59BD5F) == "mov rdx, qword ptr [rbx + 0x40]" and
            CL[0x59BD5F].mems[0]["size"] == 8 and T(CL, 0x59BD63) == "test rdx, rdx" and
            T(CL, 0x59BD66) == "jle 0x59bd78")
    R.check("positive cache: ecx = dword +0x48 (4 B), call 001D6AA0 with rdx still the +0x40 value (rdx's only "
            "writer is +0x1F), then `mov qword ptr [rbx + 0x40], 0xffffffffffffffff` (8 B)",
            T(CL, 0x59BD68) == "mov ecx, dword ptr [rbx + 0x48]" and CL[0x59BD68].mems[0]["size"] == 4 and
            CL[0x59BD6B].direct_target() == 0x1D6AA0 and writers(CL, "rdx") == [0x59BD5F] and
            T(CL, 0x59BD70) == "mov qword ptr [rbx + 0x40], 0xffffffffffffffff" and CL[0x59BD70].mems[0]["size"] == 8)
    R.check("rbx = the incoming object (+0x6); rbx written only there and by the epilogue pop",
            T(CL, 0x59BD46) == "mov rbx, rcx" and writers(CL, "rbx") == [0x59BD46, 0x59BD7E])
    paths = all_paths(CL, CL.start, {0x59BD7F})
    shape = sorted(tuple((CL[x].direct_target() if CL[x].mnemonic == "call" else
                          "st%X" % CL[x].mems[0]["disp"]) for x in p
                         if CL[x].mnemonic == "call" or (CL[x].mems and CL[x].mems[0]["write"] and
                                                          CL[x].mems[0]["base"] == "rbx")) for p in paths)
    R.check("exactly four entry -> ret paths, with (call, store) sequences: none; 2150D0 then +0x30; 1D6AA0 then "
            "+0x40; 2150D0, +0x30, 1D6AA0, +0x40",
            len(paths) == 4 and shape == sorted([(), (0x2150D0, "st30"), (0x1D6AA0, "st40"),
                                                 (0x2150D0, "st30", 0x1D6AA0, "st40")]), str(shape))
    rw = [a for a in CL.order if "rax" in CL[a].reg_writes]
    R.check("the only rax writer is `mov al, 1` (+0x38); it dominates the ret, so every normal return sets AL = 1 and "
            "leaves RAX bits 8-63 unassigned", rw == [0x59BD78] and T(CL, 0x59BD78) == "mov al, 1" and
            CL.dominates(0x59BD78, 0x59BD7F))
    acc28 = [a for a in CL.order for m in CL[a].mems if m["base"] in ("rbx", "rcx") and 0x28 <= m["disp"] < 0x30]
    R.check("no instruction reads or writes the +0x28 handle field", not acc28, str(acc28))

    def witness():
        S = close_sandbox(img)
        rv, calls, sw, al = run_close(S, M64, 0, 0)
        f = (S.q(STREAM + 0x28), S.q(STREAM + 0x30), S.q(STREAM + 0x40))
        return (rv == (JUNK & ~0xFF) | 1 and not calls and not sw and f == (M64, 0, 0) and al == 1,
                "rax %X calls %d writes %s fields %s IsOpen %d" % (rv, len(calls), sw, ["%X" % x for x in f], al))
    safe(R, "witness q28 = -1, q30 = 0, q40 = 0: Close returns AL 1 (RAX bits 8-63 as on entry), no call, no object "
            "write, fields unchanged; the retained IsOpen then returns AL 1", witness)

    def partitions():
        S = close_sandbox(img)
        bad = []
        for q30 in (0, HEAP):
            for q40 in (M64 - 1, 0x77):
                rv, calls, sw, al = run_close(S, M64, q30, q40)
                want = []
                if q30:
                    want.append(0x2150D0)
                if signed(q40) > 0:
                    want.append(0x1D6AA0)
                got = [c[1] for c in calls]
                wst = ([(0x30, 8, 0)] if q30 else []) + ([(0x40, 8, M64)] if signed(q40) > 0 else [])
                args_ok = all(c[2][0] == HEAP for c in calls if c[1] == 0x2150D0) and \
                    all(c[2][0] & 0xFFFFFFFF == KEY48 and c[2][1] == q40 for c in calls if c[1] == 0x1D6AA0)
                if got != want or sw != wst or not args_ok or rv & 0xFF != 1:
                    bad.append((hex(q30), hex(q40), got, sw))
        return not bad, "4 partitions, bad %s" % bad
    safe(R, "sandbox, the four buffer x cache partitions: exactly the derived helper calls (2150D0(buffer); "
            "1D6AA0(ecx = +0x48 key, rdx = +0x40 value)) and stores, AL 1 on each", partitions)

    def grid():
        S = close_sandbox(img)
        bad, n, open_after = [], 0, 0
        for q28 in GRID28:
            for q30 in GRID30:
                for q40 in GRID40:
                    rv, calls, sw, al = run_close(S, q28, q30, q40)
                    n += 1
                    prior = calls[-1][1] if calls else None
                    upper = {None: JUNK, 0x2150D0: REL_RET, 0x1D6AA0: RST_RET}[prior] >> 8
                    open_after += al == 1
                    if rv & 0xFF != 1 or rv >> 8 != upper or al != isopen_after_close(q28, q30, q40) or \
                            S.q(STREAM + 0x28) != q28:
                        bad.append((hex(q28), hex(q30), hex(q40), hex(rv), al))
        R.note("grid: %d of %d Close calls returned AL 1 and were followed by IsOpen AL 1" % (open_after, n))
        return not bad and n == 96, "%d cases, mismatches %s" % (n, bad[:3])
    safe(R, "sandbox grid (96 cases): Close always returns AL 1 with RAX bits 8-63 not its own, never changes +0x28, "
            "and IsOpen afterwards is false exactly when q28 = -1 and (q40 signed > 0 or q40 = -1)", grid)

    def composed():
        out = []
        for mret in (0, HEAP + 0x400):
            S = composed_sandbox(img, malloc_ret=mret)
            S.call(CTOR[0], {"rcx": STREAM, "rdx": PATH, "r8": 3})
            rv = S.call(CLOSE_B[0], {"rcx": STREAM})
            cl = S.calls()
            sw = len(S.writes_in(STREAM, STREAM + 0x60))
            al = S.call(ISOPEN_B[0], {"rcx": STREAM}) & 0xFF
            out.append((rv & 0xFF, cl, sw, al))
        ok = out[0] == (1, [], 0, 1) and out[1][0] == 1 and out[1][1] == [0x1D6AA0] and out[1][3] == 0
        return ok, str(out)
    safe(R, "sandbox, composed: the NULL-allocation zero view closes with AL 1, no call, no write, and stays IsOpen "
            "AL 1; a real view closes through 001D6AA0 and IsOpen then returns AL 0", composed)


def packet(img, R):
    check_manifest(R, SLUG, MANIFEST_SHA)
    ev = os.path.join(EV_ROOT, SLUG)
    got, bad = range_hashes(img, [os.path.join(ev, f) for f in ("source-01.json", "retained-open/source-01.json")])
    R.check("packet's captured and retained range sha256 values equal this image (%d ranges: Close, IsOpen)" % len(got),
            not bad and CLOSE_B in got and ISOPEN_B in got, str(bad))
    h = hashlib.sha256(open(os.path.join(ev, "retained-open", "manifest.json"), "rb").read()).hexdigest()
    R.check("retained IsOpen manifest = filecache-open-sentinel's committed manifest (7479a4f8...)",
            h == OPEN_MANIFEST_SHA, h)


CONTROLS = [
    ("Close + 0x26 `jle` -> `jl` (zero cache would reset)", 0x59BD66, bytes([0x7C])),
    ("Close + 0x26 `jle` -> `je` (zero-only guard; negatives would reset)", 0x59BD66, bytes([0x74])),
    ("Close + 0x30 qword reset -> dword reset + nop", 0x59BD70, bytes.fromhex("c74340ffffffff90")),
    ("Close + 0x10 `je 0x59bd5f` -> `je 0x59bd78` (skipping release also skips reset)", 0x59BD51, bytes([0x26])),
    ("Close + 0x17 buffer clear [rbx+30h] -> [rbx+28h]", 0x59BD5A, bytes([0x28])),
    ("Close + 0x38 `mov al, 1` -> `xor al, al`", 0x59BD78, bytes.fromhex("32c0")),
    ("Close + 0x1F `mov rdx, [rbx+40h]` -> `mov edx, [rbx+40h]; nop` (32-bit guard)", 0x59BD5F,
     bytes.fromhex("8b534090")),
    ("IsOpen + 0xE `cmp [rcx+40h], -1` -> `cmp [rcx+40h], 0` (retained predicate rejects the zero view)", 0x59D932,
     bytes([0x00])),
]


if __name__ == "__main__":
    run_review("rv_close", checks, packet, CONTROLS, 0x59BD40)
