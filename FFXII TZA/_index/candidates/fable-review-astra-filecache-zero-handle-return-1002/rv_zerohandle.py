"""rv_zerohandle.py - FABLE independent re-derivation for ASTRA packet filecache-zero-handle-return (5b659b28d).

Own reader (rvlib.py: struct + capstone 5, copied unchanged from the route2-commit-key review) plus the reviewer's own
sandbox (unicorn over a private copy of the image's sections, every callee and import answered by a recording stub).
Does not import ASTRA's prove.py, capture drivers, freeze/publication scripts or reg_tracking.py.

Method: complete linear decode of 0020C300 (.pdata), the 00210EC0 allocation wrapper and the 0085E730 import thunk
(no .pdata; int3-bounded), the security-cookie check 00808C40 (.pdata), and the retained lookup 0020C1B0, wrapper
001D6D20 and resolver 0059EE90 (.pdata); every entry -> allocation path enumerated; the import resolved from the PE
import directory; the zero result followed by dominance and reach sets; then the shipped bytes run in the sandbox over
every selector/kind arm with the allocation returning NULL and non-NULL, and once composed from the resolver.
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

SLUG = "filecache-zero-handle-return"
MANIFEST_SHA = "93e2351f2132231d53da0597dbef418c7870e0a795e04e0090c4e5089c93c521"
ROUTE2_MANIFEST_SHA = "f3365d0eb049fb0c84b6150f1d410a2d1e2b01e36f4025973dc3063c4215392d"
INCS = (0x20C354, 0x20C38B, 0x20C3F8)
SELECTORS = range(8)
KINDS = range(7)


def stack(a):
    return STK <= a < STK + 0x100000


def expected_extra(sel, kind):
    """The reviewer's reading of 0020C300's arms: which record field (offset, width) each (selector, kind) stamps."""
    if 1 <= kind <= 4 and sel == 5:
        return {(0x14, 4)}
    if kind == 5 or sel == 5:
        return set()
    if sel == 3:
        return {(0x0E, 2)}
    if sel in (1, 2, 4):
        return {(0x0C, 2)}
    return set()


def create_sandbox(img, malloc_ret):
    st = {0x20B5F0: lambda S: RECSLOT, ("iat", MALLOC_SLOT): lambda S: malloc_ret,
          0x217A60: lambda S: 0x5EED0000BEEF0000}
    S = Sandbox(img, [CREATE, ALLOC, MALLOC_THUNK], st)
    S.setq(MGR + 0x18, MGR + 0x800)
    S.setd(MGR + 0x88, 0x10)
    S.mu.mem_write(MGR + 0x80, b"\x42\x42")
    S.mu.mem_write(MGR + 0x8E8, b"\x31\x31")
    S.setq(RECSLOT, RECORD)
    S.mu.mem_write(RECORD + 0x10, b"\x03")
    return S


def run_create(S, sel, kind):
    S.setd(MGR + 0x88, 0x10)
    S.mu.mem_write(RECORD + 0x10, b"\x03")
    rv = S.call(CREATE[0], {"rcx": MGR, "rdx": 0x2B5E6, "r8": ENTRY, "r9": ENTRY_SIZE}, stack_args=(sel, kind))
    ev = S.events
    mc = [i for i, e in enumerate(ev) if e[0] == "call" and e[1] == ("iat", MALLOC_SLOT)]
    objw = [(i, e) for i, e in enumerate(ev) if e[0] == "w" and not stack(e[2])]
    return rv, ev, mc, objw


def checks(img, R):
    B = {k: Body(img, *r) for k, r in (("create", CREATE), ("alloc", ALLOC), ("thunk", MALLOC_THUNK),
                                        ("cookie", COOKIE), ("look", LOOKUP), ("wrap", WRAPPER), ("res", RESOLVER))}
    CR, LK, WR, RS, CK = B["create"], B["look"], B["wrap"], B["res"], B["cookie"]

    # ---------------- bodies ----------------
    for k, (s, e) in (("create", CREATE), ("cookie", COOKIE), ("look", LOOKUP), ("wrap", WRAPPER), ("res", RESOLVER)):
        ents, ok = img.pdata_cover(s, e)
        R.check("body %08X + 0x%X (%d B) decodes exactly and one .pdata record covers it exactly" % (s, e - s, e - s),
                B[k].exact and ok and len(ents) == 1)
    for k, (s, e) in (("alloc", ALLOC), ("thunk", MALLOC_THUNK)):
        R.check("thunk %08X + 0x%X (%d B) decodes exactly, has no .pdata record, int3 before and after" %
                (s, e - s, e - s), B[k].exact and leaf_bounds(img, s, e))
    tot = sum(e - s for s, e in (CREATE, ALLOC, MALLOC_THUNK))
    R.check("source-01 bodies total 330 B (312 + 11 + 7); with the 33 B cookie body 363 B",
            tot == 330 and tot + COOKIE[1] - COOKIE[0] == 363, "%d" % tot)
    rets, tails, outs = CR.exits()
    R.check("0020C300 local CFG closed: single ret is the last instruction, no tail or out-of-body branch",
            rets == [CR.order[-1]] and not tails and not outs, "rets=%s" % ["%X" % x for x in rets])
    R.check("00210EC0 = `or r8d, 0xffffffff; xor edx, edx; jmp 0x85e730`",
            [T(B["alloc"], a) for a in B["alloc"].order] == ["or r8d, 0xffffffff", "xor edx, edx", "jmp 0x85e730"])
    th = B["thunk"][MALLOC_THUNK[0]]
    imp = import_of_slot(img, rip_slot(th)) if th.mnemonic == "jmp" and th.mems else None
    R.check("0085E730 is `jmp qword ptr [rip + ...]` through IAT 008C2B40 = api-ms-win-crt-heap-l1-1-0.dll!malloc, "
            "hint/name at 01DEEE88 (PE import directory)",
            th.mnemonic == "jmp" and th.mems and rip_slot(th) == MALLOC_SLOT and imp and
            imp[:2] == ("api-ms-win-crt-heap-l1-1-0.dll", "malloc") and imp[2] == 0x1DEEE88, str(imp))

    # ---------------- counters before the allocation ----------------
    R.check("0020C300 + 0x28: `inc dword ptr [rcx + 0x88]` (4 B) with rcx still the incoming first argument",
            T(CR, 0x20C328) == "inc dword ptr [rcx + 0x88]" and CR[0x20C328].mems[0]["size"] == 4 and
            writers(CR, "rcx", CR.start, 0x20C328) == [])
    R.check("0020C300 + 0xFB/+0x100: `mov ecx, 0x10` then the call to 00210EC0 (a 16-byte request)",
            T(CR, 0x20C3FB) == "mov ecx, 0x10" and CR[0x20C400].direct_target() == ALLOC[0])
    R.check("the +0x88 increment dominates the allocation call", CR.dominates(0x20C328, 0x20C400))
    paths = all_paths(CR, CR.start, {0x20C400})
    to_alloc = [p for p in paths if p[-1] == 0x20C400]
    R.check("every entry -> allocation path (%d paths) passes exactly one record `inc byte ptr [r + 0x10]` "
            "(+0x54, +0x8B or +0xF8)" % len(to_alloc),
            len(to_alloc) == len(paths) and all(sum(1 for x in p if x in INCS) == 1 for p in to_alloc) and
            all(CR[x].mnemonic == "inc" and CR[x].mems[0]["disp"] == 0x10 and CR[x].mems[0]["size"] == 1
                for x in INCS), "%d paths" % len(paths))
    R.check("each incremented record is loaded as [rax] straight after a call to 0020B5F0",
            all(CR.order[CR.order.index(x) - 2] in CR.ins and CR[CR.order[CR.order.index(x) - 2]].direct_target()
                == 0x20B5F0 and CR[CR.order[CR.order.index(x) - 1]].op_str.endswith("qword ptr [rax]") for x in INCS))
    FI = Body(img, 0x20B5F0, 0x20B675)
    sites = [a for a in CR.order if CR[a].direct_target() == 0x20B5F0]
    prev2 = [set(T(CR, CR.order[CR.order.index(a) - k]) for k in (1, 2)) for a in sites]
    R.check("the incremented record is the hit entry itself: 0020B5F0 walks root [rcx+18h] against header rcx+8 with "
            "key [rdx] and returns node+0x28; all %d calls in 0020C300 pass rcx = manager+0x20 (so root +0x38, header "
            "+0x28: the lookup's tree) and rdx = &[rsp+58h] = entry SP+10h, where +0x0 saved the key (edx)" % len(sites),
            FI.exact and T(FI, 0x20B5F4) == "mov r8, qword ptr [rcx + 0x18]" and T(FI, 0x20B5FB) == "add rcx, 8" and
            T(FI, 0x20B607) == "mov r9d, dword ptr [rdx]" and T(FI, 0x20B66C) == "add rax, 0x28" and
            len(sites) == 6 and all(p == {"lea rcx, [rdi + 0x20]", "lea rdx, [rsp + 0x58]"} for p in prev2) and
            T(CR, 0x20C300) == "mov dword ptr [rsp + 0x10], edx" and 0x58 - 0x48 == 0x10 and
            T(LK, 0x20C2A2) == "mov edx, dword ptr [r14]", "%d sites" % len(sites))
    R.check("the lookup holds its lock across the 0020C300 call: lock 005CD4F0 (0020C1B0 + 0x8C) dominates it and the "
            "unlock 005CD820 (+0x103) follows it on the hit path",
            LK[0x20C23C].direct_target() == 0x5CD4F0 and LK.dominates(0x20C23C, 0x20C2A8) and
            0x20C2B3 in LK.reach(0x20C2AD) and LK[0x20C2B3].direct_target() == 0x5CD820)
    pre = sorted(set((a, m["disp"], m["size"]) for a, m in CR.mem_writes() if a < 0x20C400 and m["base"] != "rsp"))
    R.check("all non-stack writes before the allocation: +0x88 dword, the three +0x10 bytes, +0x14 dword (+0x68), "
            "+0x0E word (+0xC3), +0x0C word (+0xE1)",
            pre == [(0x20C328, 0x88, 4), (0x20C354, 0x10, 1), (0x20C368, 0x14, 4), (0x20C38B, 0x10, 1),
                    (0x20C3C3, 0x0E, 2), (0x20C3E1, 0x0C, 2), (0x20C3F8, 0x10, 1)],
            str([("%X" % a, hex(d), s) for a, d, s in pre]))
    R.check("the fifth argument (ebx, entry SP+28h) and sixth (ecx, entry SP+30h) drive the arms: frame = 3 pushes + 30h",
            T(CR, 0x20C335) == "mov ebx, dword ptr [rsp + 0x70]" and T(CR, 0x20C32E) == "mov ecx, dword ptr [rsp + 0x78]"
            and 0x70 - 0x48 == 0x28)

    # ---------------- the NULL arm ----------------
    R.check("0020C300 + 0x10A/+0x10D: `test rax, rax` / `je 0x20c423` on the allocation result",
            T(CR, 0x20C40A) == "test rax, rax" and T(CR, 0x20C40D) == "je 0x20c423")
    nul = CR.reach(0x20C423)
    R.check("NULL arm: `xor eax, eax` (full RAX 0), then no call, no memory write and no rax writer to the ret; "
            "the constructor 00217A60 is unreachable from it",
            T(CR, 0x20C423) == "xor eax, eax" and not [x for x in nul if CR[x].mnemonic == "call"] and
            not [x for x in nul if CR[x].mems and any(m["write"] for m in CR[x].mems)] and
            not [x for x in nul if x != 0x20C423 and "rax" in CR[x].reg_writes] and 0x20C41B not in nul and
            CR.order[-1] in nul)
    nn = CR.reach(0x20C420)
    R.check("non-NULL arm: 00217A60 gets rcx = the allocation (+0x118), and its RAX is returned unchanged",
            T(CR, 0x20C418) == "mov rcx, rax" and CR[0x20C41B].direct_target() == 0x217A60 and
            not [x for x in nn if "rax" in CR[x].reg_writes])

    # ---------------- the lookup hit path and the cookie ----------------
    R.check("0020C1B0 hit path: `mov dword ptr [r15], r9d` (+0xDC, the size out) dominates the 0020C300 call (+0xF8)",
            T(LK, 0x20C28C) == "mov dword ptr [r15], r9d" and LK.dominates(0x20C28C, 0x20C2A8) and
            LK[0x20C2A8].direct_target() == CREATE[0])
    R.check("0020C1B0 passes 0020C300 the selector as the fifth argument: ebp = incoming r8d (+0x35), "
            "`mov dword ptr [rsp + 0x20], ebp` (+0xEB); sixth = entry dword +0x14 (+0xE3/+0xE7)",
            T(LK, 0x20C1E5) == "mov ebp, r8d" and writers(LK, "rbp") == [0x20C1E5, 0x20C2F0] and
            T(LK, 0x20C29B) == "mov dword ptr [rsp + 0x20], ebp" and T(LK, 0x20C293) == "mov eax, dword ptr [r8 + 0x14]"
            and T(LK, 0x20C297) == "mov dword ptr [rsp + 0x28], eax")
    found = LK.reach(0x20C2AD)
    R.check("hit return: rbx = rax (+0xFD), unlock 005CD820 (+0x103), rax = rbx (+0x109), jmp to the cookie block; "
            "the miss arm's `or rax, -1` (+0x117) is not on that path",
            T(LK, 0x20C2AD) == "mov rbx, rax" and LK[0x20C2B3].direct_target() == 0x5CD820 and
            T(LK, 0x20C2B9) == "mov rax, rbx" and T(LK, 0x20C2BC) == "jmp 0x20c2cb" and 0x20C2C7 not in found)
    tail = LK.reach(0x20C2BC)
    R.check("from +0x10C to the ret the only call is the cookie check 00808C40 and nothing writes rax",
            [LK[x].direct_target() for x in tail if LK[x].mnemonic == "call"] == [COOKIE[0]] and
            not [x for x in tail if "rax" in LK[x].reg_writes and LK[x].mnemonic != "call"])
    # rvlib's CFG does not treat the `bnd`-prefixed jcc/ret as branches, so this body is checked by its exact text.
    ck_txt = ["cmp rcx, qword ptr [rip + 0x173bbe9]", "bnd jne 0x808c5c", "rol rcx, 0x10", "test cx, 0xffff",
              "bnd jne 0x808c58", "bnd ret", "ror rcx, 0x10", "jmp 0x809654"]
    ret_path = (0x808C40, 0x808C47, 0x808C4A, 0x808C4E, 0x808C53, 0x808C56)
    R.check("00808C40 is exactly cmp / bnd jne / rol rcx / test cx / bnd jne / bnd ret / ror rcx / jmp 00809654; "
            "the returning path (both jne not taken) writes no rax",
            [T(CK, a) for a in CK.order] == ck_txt and list(CK.order[:6]) == list(ret_path) and
            not [a for a in ret_path if "rax" in CK[a].reg_writes])
    R.check("001D6D20 returns 0020C1B0's RAX: no rax writer after the +0x35 call",
            WR[0x1D6D55].direct_target() == LOOKUP[0] and not writers(WR, "rax", 0x1D6D5A))

    # ---------------- the resolver ----------------
    R.check("resolver: `mov qword ptr [r15 + 0x20], rax` (8 B) directly after the lookup call (0059EE90 + 0x15A)",
            RS[0x59EFE5].direct_target() == WRAPPER[0] and T(RS, 0x59EFEA) == "mov qword ptr [r15 + 0x20], rax" and
            RS[0x59EFEA].mems[0]["size"] == 8)
    R.check("the only test of the result is `test rax, rax` / `js 0x59f000` (+0x15E/+0x161): negative only",
            T(RS, 0x59EFEE) == "test rax, rax" and T(RS, 0x59EFF1) == "js 0x59f000")
    zr = RS.reach(0x59EFF3)
    R.check("zero/positive arm: eax = dword [rbp] (the size out), stored to [r15]; `xor eax, eax`; jmp to the "
            "epilogue; its only call is the cookie check, and no archive call (0019AEE0, 0059A9B0) is reachable",
            T(RS, 0x59EFF3) == "mov eax, dword ptr [rbp]" and T(RS, 0x59EFF6) == "mov dword ptr [r15], eax" and
            T(RS, 0x59EFF9) == "xor eax, eax" and
            [RS[x].direct_target() for x in zr if RS[x].mnemonic == "call"] == [COOKIE[0]] and
            not [x for x in zr if x > 0x59EFF9 and "rax" in RS[x].reg_writes and RS[x].mnemonic != "call"])

    # ---------------- sandbox: every arm, NULL and non-NULL ----------------
    def arms():
        bad, n, extras = [], 0, {}
        for mret in (0, HEAP + 0x400):
            S = create_sandbox(img, mret)
            for sel in SELECTORS:
                for kind in KINDS:
                    rv, ev, mc, objw = run_create(S, sel, kind)
                    n += 1
                    m88 = [i for i, e in objw if e[2] == MGR + 0x88]
                    r10 = [i for i, e in objw if e[2] == RECORD + 0x10]
                    ok = (len(mc) == 1 and len(m88) == 1 and m88[0] < mc[0] and S.d32(MGR + 0x88) == 0x11 and
                          len(r10) == 1 and r10[0] < mc[0] and S.q(RECORD + 0x10) & 0xFF == 4)
                    ex = set((e[2] - RECORD, e[3]) for i, e in objw if RECORD <= e[2] < RECORD + 0x100 and
                             e[2] != RECORD + 0x10)
                    ok = ok and ex == expected_extra(sel, kind)
                    ctor = [e for e in ev if e[0] == "call" and e[1] == 0x217A60]
                    if mret == 0:
                        ok = ok and rv == 0 and not ctor and not [e for i, e in objw if i > mc[0]]
                    else:
                        ok = ok and len(ctor) == 1 and ctor[0][2][0] == mret and rv == 0x5EED0000BEEF0000
                    extras[tuple(sorted(ex))] = extras.get(tuple(sorted(ex)), 0) + 1
                    if not ok:
                        bad.append((mret, sel, kind))
        R.note("record stamps by arm (offset, width) -> runs: %s" % sorted(extras.items()))
        return not bad and n == 2 * len(SELECTORS) * len(KINDS), "%d runs, bad %s" % (n, bad[:4])
    safe(R, "sandbox, 0020C300 over selectors 0-7 x kinds 0-6, allocation NULL and non-NULL: +0x88 +1 and record "
            "+0x10 +1 exactly once, both before the malloc call; NULL -> full RAX 0, no constructor, no later "
            "non-stack write; non-NULL -> constructor(rcx = block), its RAX returned", arms)

    def composed():
        S = composed_sandbox(img, malloc_ret=0)
        S.call(CTOR[0], {"rcx": STREAM, "rdx": 0, "r8": 3})
        rv = S.call(RESOLVER[0], {"rcx": STREAM + 0x20, "rdx": PATH, "r8": 1})
        f = fields(S)
        cl = S.calls()
        ok = (rv == 0 and f["q40"] == 0 and f["q30"] == 0 and f["q28"] == 0xFFFFFFFFFFFFFFFF and
              f["d20"] == ENTRY_SIZE and ("iat", MALLOC_SLOT) in cl and 0x217A60 not in cl and
              0x19AEE0 not in cl and 0x59A9B0 not in cl and S.d32(MGR + 0x88) == 0x11 and
              S.q(RECORD + 0x10) & 0xFF == 4 and f["d48"] == key_hash(KEYTEXT))
        return ok, "status %X fields %s calls %s" % (rv, {k: "%X" % v for k, v in f.items()},
                                                      ["%X" % c if isinstance(c, int) else "iat" for c in cl])
    safe(R, "sandbox, resolver over a route-1 hit whose allocation is NULL: status RAX 0, stream +0x40 = 0, +0x30 = 0, "
            "+0x28 = -1, +0x20 = the entry size; no archive call; counters +1", composed)

    def miss():
        S = composed_sandbox(img, malloc_ret=0)
        S.setd(NODE + 0x20, key_hash(KEYTEXT) ^ 0x40)
        S.call(CTOR[0], {"rcx": STREAM, "rdx": 0, "r8": 3})
        S.call(RESOLVER[0], {"rcx": STREAM + 0x20, "rdx": PATH, "r8": 1}, until=0x59F000)
        f = fields(S)
        cl = S.calls()
        return (f["q40"] == 0xFFFFFFFFFFFFFFFF and ("iat", MALLOC_SLOT) not in cl and S.d32(MGR + 0x88) == 0x10,
                "+0x40 %X" % f["q40"])
    safe(R, "sandbox contrast, a route-1 miss: the lookup returns -1, +0x40 = -1, no allocation or counter, and the "
            "resolver reaches the archive fallback 0059EE90 + 0x170", miss)


def packet(img, R):
    check_manifest(R, SLUG, MANIFEST_SHA)
    ev = os.path.join(EV_ROOT, SLUG)
    got, bad = range_hashes(img, [os.path.join(ev, f) for f in (
        "source-01.json", "source-02.json", "retained/source-01.json",
        "retained/filecache-key-boundaries-source-02.json")])
    need = [CREATE, ALLOC, MALLOC_THUNK, COOKIE, LOOKUP, RESOLVER, WRAPPER]
    R.check("packet's captured and retained range sha256 values equal this image (%d ranges, incl. all seven bodies "
            "reviewed)" % len(got), not bad and all(n in got for n in need), str(bad))
    rm = hashlib.sha256(open(os.path.join(ev, "retained", "manifest.json"), "rb").read()).hexdigest()
    R.check("retained manifest = filecache-route2-commit-key's (f3365d0e..., FABLE-reviewed ACCEPT-WITH-NARROWING)",
            rm == ROUTE2_MANIFEST_SHA, rm)


CONTROLS = [
    ("0020C300 + 0x10D NULL `je` -> `jne` (NULL constructs, non-NULL returns 0)", 0x20C40D, bytes([0x75])),
    ("0020C300 + 0x123 `xor eax, eax` -> `xor al, al` (upper RAX kept)", 0x20C423, bytes.fromhex("32c0")),
    ("0020C300 + 0x28 `inc [rcx + 0x88]` -> `inc [rcx + 0x8c]`", 0x20C328, bytes.fromhex("ff818c000000")),
    ("0020C300 + 0xF8 `inc byte [rcx + 0x10]` -> three nops (one arm without the record increment)", 0x20C3F8,
     bytes([0x90] * 3)),
    ("0020C300 + 0xFB `mov ecx, 0x10` -> `mov ecx, 0x20`", 0x20C3FB, bytes.fromhex("b920000000")),
    ("0020C300 + 0x48 `lea rcx, [rdi+20h]` -> `[rdi+28h]` (another tree)", 0x20C34B, bytes([0x28])),
    ("0020C1B0 + 0x109 `mov rax, rbx` -> `mov rax, rsi` (hit result dropped)", 0x20C2B9, bytes.fromhex("488bc6")),
    ("0059EE90 + 0x161 `js` -> `jle` (zero takes the archive fallback)", 0x59EFF1, bytes([0x7E])),
    ("001D6D20 + 0x3A `mov rbx, [rsp+40h]` -> `mov rax, [rsp+40h]` (wrapper clobbers RAX)", 0x1D6D5A,
     bytes.fromhex("488b442440")),
    ("0085E730 IAT slot moved 8 bytes (another import)", 0x85E733, struct.pack("<i", 0x64409 + 8)),
    ("00808C40 + 0xA `rol rcx, 0x10` -> `rol rax, 0x10` (a RAX writer on the cookie's return path)", 0x808C4A,
     bytes.fromhex("48c1c010")),
]


if __name__ == "__main__":
    run_review("rv_zerohandle", checks, packet, CONTROLS, 0x20C328)
