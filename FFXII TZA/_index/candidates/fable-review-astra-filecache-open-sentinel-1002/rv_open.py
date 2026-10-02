"""rv_open.py - FABLE independent re-derivation for ASTRA packet filecache-open-sentinel (446a56af9).

Own reader (rvlib.py: struct + capstone 5, copied unchanged from the route2-commit-key review) plus the reviewer's own
sandbox (unicorn over a private copy of the image's sections, every callee and import answered by a recording stub).
Does not import ASTRA's prove.py, capture drivers, freeze/publication scripts or reg_tracking.py.

Method: complete decode of the 27-byte IsOpen 0059D920 (no .pdata; int3-bounded, closed CFG) and of the retained
constructor 00597970 and resolver 0059EE90 (.pdata); every IsOpen arm by text and width; the predicate run in the
sandbox over a 64-case grid of field values chosen to expose width and polarity errors; the constructor's and the
resolver's writes to the three backing fields by census and reach; and the composed zero-view state built by running
constructor -> resolver -> route-1 hit -> NULL allocation, then IsOpen on it.  Controls patch a private in-memory copy
of the image and require at least one named check to fail.
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

SLUG = "filecache-open-sentinel"
MANIFEST_SHA = "7479a4f8d544249b398a57419aab50ac4296bc14eb717c4517cd478320ad2f45"
PARENT_SHAS = {"filecache-source-key-initialization": "d5cc7655d068357ee5bd9496b5674f82d4e4679d30d12356ba5411d8b713350e",
               "filecache-zero-handle-return": "93e2351f2132231d53da0597dbef418c7870e0a795e04e0090c4e5089c93c521"}
M64 = 0xFFFFFFFFFFFFFFFF
GRID28 = (M64, 0, 0xFFFFFFFF, 0xFFFFFFFF00000000)
GRID30 = (0, 1, 0x100000000, M64)
GRID40 = (M64, 0, 0xFFFFFFFF, 0x8000000000000000)
ISOPEN_TXT = ["cmp qword ptr [rcx + 0x28], -1", "jne 0x59d938", "cmp qword ptr [rcx + 0x30], 0", "jne 0x59d938",
              "cmp qword ptr [rcx + 0x40], -1", "jne 0x59d938", "xor al, al", "ret", "mov al, 1", "ret"]


def predicate(q28, q30, q40):
    """The packet's formula, stated independently: AL = !(q28 == -1 && q30 == 0 && q40 == -1)."""
    return 0 if (q28 == M64 and q30 == 0 and q40 == M64) else 1


def run_isopen(S, q28, q30, q40):
    S.setq(STREAM + 0x28, q28)
    S.setq(STREAM + 0x30, q30)
    S.setq(STREAM + 0x40, q40)
    return S.call(ISOPEN_B[0], {"rcx": STREAM})


def checks(img, R):
    IO = Body(img, *ISOPEN_B)
    CT = Body(img, *CTOR)
    RS = Body(img, *RESOLVER)

    # ---------------- IsOpen ----------------
    s, e = ISOPEN_B
    R.check("IsOpen 0059D920 + 0x1B (27 B) decodes exactly into 10 instructions; no .pdata record; int3 before the "
            "entry and after the last ret", IO.exact and len(IO.order) == 10 and leaf_bounds(img, s, e))
    rets, tails, outs = IO.exits()
    R.check("closed local CFG: two rets (+0x17, +0x1A), no tail or out-of-body branch, no call, no memory write",
            rets == [0x59D937, 0x59D93A] and not tails and not outs and not IO.calls() and not IO.mem_writes())
    R.check("instruction text is exactly: cmp q[+28h],-1 / jne / cmp q[+30h],0 / jne / cmp q[+40h],-1 / jne / "
            "xor al,al / ret / mov al,1 / ret", [T(IO, a) for a in IO.order] == ISOPEN_TXT)
    cmps = [IO[a] for a in IO.order if IO[a].mnemonic == "cmp"]
    R.check("all three compares are full 64-bit (8-byte memory operand, sign-extended immediate)",
            [c.mems[0]["size"] for c in cmps] == [8, 8, 8] and [c.mems[0]["disp"] for c in cmps] == [0x28, 0x30, 0x40]
            and [c.imm[0] for c in cmps] == [-1, 0, -1] and all(c.bytes[0] == 0x48 for c in cmps))
    rw = [a for a in IO.order if "rax" in IO[a].reg_writes]
    R.check("only AL is assigned: the two rax writers are `xor al, al` (+0x15) and `mov al, 1` (+0x18)",
            rw == [0x59D935, 0x59D938] and all(IO[a].op_str.startswith("al,") for a in rw))

    def grid():
        S = Sandbox(img, [ISOPEN_B])
        bad, n, zeros = [], 0, 0
        for q28 in GRID28:
            for q30 in GRID30:
                for q40 in GRID40:
                    rv = run_isopen(S, q28, q30, q40)
                    n += 1
                    al = rv & 0xFF
                    zeros += al == 0
                    if al != predicate(q28, q30, q40) or (rv >> 8) != (JUNK >> 8) or S.events:
                        bad.append((hex(q28), hex(q30), hex(q40), hex(rv)))
        return not bad and n == 64 and zeros == 1, "%d cases, %d false, mismatches %s" % (n, zeros, bad[:3])
    safe(R, "sandbox grid (q28 x q30 x q40 over -1/0/FFFFFFFF/high-half values, 64 cases): AL equals the formula, "
            "false only in the all-sentinel case, RAX bits 8-63 untouched, no call or write", grid)

    def witness():
        S = Sandbox(img, [ISOPEN_B])
        rv = run_isopen(S, M64, 0, 0)
        return (rv & 0xFF == 1 and S.trace == [0x59D920, 0x59D925, 0x59D927, 0x59D92C, 0x59D92E, 0x59D933, 0x59D938,
                                                 0x59D93A], "rax %X trace %s" % (rv, ["%X" % a for a in S.trace]))
    safe(R, "witness q28 = -1, q30 = 0, q40 = 0: the +0x40 compare's jne (+0x13) goes to `mov al, 1`; AL = 1", witness)

    # ---------------- constructor ----------------
    ents, ok = img.pdata_cover(*CTOR)
    R.check("constructor 00597970 + 0xA2 (162 B) decodes exactly and one .pdata record covers it exactly",
            CT.exact and ok and len(ents) == 1)
    pre = [(a, m["disp"], m["size"]) for a, m in CT.mem_writes() if a < 0x5979B6 and m["base"] == "rcx"]
    R.check("before the resolver call it writes +0x28 = -1 (8 B), +0x20 = 0 (4), +0x30 = 0 (8), +0x40 = -1 (8), "
            "+0x48 = 0 (4), +0x38 = selector byte; ebp is `xor ebp, ebp`",
            pre == [(0x597986, 0x28, 8), (0x59798E, 0x20, 4), (0x597994, 0x30, 8), (0x59799B, 0x40, 8),
                    (0x5979A3, 0x48, 4), (0x5979A6, 0x38, 1)] and T(CT, 0x597984) == "xor ebp, ebp" and
            T(CT, 0x597986) == "mov qword ptr [rcx + 0x28], 0xffffffffffffffff" and
            T(CT, 0x59799B) == "mov qword ptr [rcx + 0x40], 0xffffffffffffffff" and
            T(CT, 0x597994) == "mov qword ptr [rcx + 0x30], rbp", str([("%X" % a, hex(d), s_) for a, d, s_ in pre]))
    R.check("the resolver is called only with a non-null path (`test rdx, rdx` / `je 0x5979bb`), with r8b = 1 and "
            "rcx = this + 0x20", T(CT, 0x5979AA) == "test rdx, rdx" and T(CT, 0x5979AD) == "je 0x5979bb" and
            T(CT, 0x5979AF) == "mov r8b, 1" and T(CT, 0x5979B2) == "add rcx, 0x20" and
            CT[0x5979B6].direct_target() == RESOLVER[0])
    post = [(a, m["disp"], m["size"]) for a, m in CT.mem_writes() if a > 0x5979B6 and m["base"] == "rdi"]
    R.check("after the resolver call no constructor write touches +0x28..+0x47 (writes: +8, +0, +0x10, +0x1C, +0x18)",
            post and all(not (d < 0x48 and d + s_ > 0x28) for a, d, s_ in post) and
            writers(CT, "rdi") == [0x597998, 0x597A10], str([("%X" % a, hex(d), s_) for a, d, s_ in post]))
    R.check("the resolver's status is discarded: the first instruction after the call (+0x4B) overwrites rax, and the "
            "constructor returns rax = this (+0x99)", T(CT, 0x5979BB).startswith("lea rax, [rip") and
            CT.order[CT.order.index(0x5979B6) + 1] == 0x5979BB and T(CT, 0x597A09) == "mov rax, rdi")

    # ---------------- resolver ----------------
    r15w = sorted(set((m["disp"], m["size"]) for a, m in RS.mem_writes() if m["base"] == "r15"))
    R.check("resolver writes through r15 (= this + 0x20) only at +0/4, +0x10/8, +0x18/1, +0x20/8: stream +0x20, "
            "+0x30, +0x38, +0x40, never stream +0x28", r15w == [(0, 4), (0x10, 8), (0x18, 1), (0x20, 8)] and
            T(RS, 0x59EEC4) == "mov r15, rcx", str(r15w))
    seg = on_paths(RS, RS.start, 0x59EFE5)
    before = sorted(a for a, m in RS.mem_writes() if m["base"] == "r15" and a in seg)
    R.check("on every entry -> lookup-call path (%d instructions) the only r15 write is the forced selector byte "
            "+0x18 (0059EE90 + 0x61)" % len(seg), before == [0x59EEF1], str(["%X" % a for a in before]))
    zr = RS.reach(0x59EFF3)
    zw = [(a, m["disp"], m["size"]) for a in zr for m in RS[a].mems if m["write"] and m["base"] == "r15"]
    R.check("after a non-negative lookup result the only r15 write is +0/4 (the size, 0059EE90 + 0x166); the +0x10 "
            "store (0059EE90 + 0x307) is unreachable", zw == [(0x59EFF6, 0, 4)] and 0x59F197 not in zr, str(zw))

    # ---------------- composed ----------------
    def nopath():
        S = composed_sandbox(img, malloc_ret=0)
        rv = S.call(CTOR[0], {"rcx": STREAM, "rdx": 0, "r8": 3})
        f = fields(S)
        al = S.call(ISOPEN_B[0], {"rcx": STREAM}) & 0xFF
        return (rv == STREAM and f["q28"] == M64 and f["q30"] == 0 and f["q40"] == M64 and al == 0,
                "fields %s IsOpen %d" % ({k: "%X" % v for k, v in f.items()}, al))
    safe(R, "sandbox: constructed with a null path, the stream is -1 / 0 / -1 and IsOpen returns AL 0", nopath)

    def zero_view():
        out = []
        for mret in (0, HEAP + 0x400):
            S = composed_sandbox(img, malloc_ret=mret)
            rv = S.call(CTOR[0], {"rcx": STREAM, "rdx": PATH, "r8": 3})
            f = fields(S)
            al = S.call(ISOPEN_B[0], {"rcx": STREAM}) & 0xFF
            out.append((rv, f["q28"], f["q30"], f["q40"], al))
        ok = (out[0] == (STREAM, M64, 0, 0, 1) and out[1] == (STREAM, M64, 0, HEAP + 0x400, 1))
        return ok, str([tuple("%X" % x for x in o) for o in out])
    safe(R, "sandbox, constructor -> resolver -> route-1 hit: with a NULL allocation the stream is -1 / 0 / 0 and "
            "IsOpen returns AL 1; with a real view (+0x40 = the block) it also returns AL 1", zero_view)


def packet(img, R):
    check_manifest(R, SLUG, MANIFEST_SHA)
    ev = os.path.join(EV_ROOT, SLUG)
    got, bad = range_hashes(img, [os.path.join(ev, f) for f in (
        "source-01.json", "parents/filecache-source-key-initialization/source-01.json",
        "parents/filecache-zero-handle-return/retained/source-01.json")])
    R.check("packet's captured and parent range sha256 values equal this image (%d ranges, incl. IsOpen, the "
            "constructor and the resolver)" % len(got), not bad and all(n in got for n in (ISOPEN_B, CTOR, RESOLVER)),
            str(bad))
    for p, sha in sorted(PARENT_SHAS.items()):
        h = hashlib.sha256(open(os.path.join(ev, "parents", p, "manifest.json"), "rb").read()).hexdigest()
        R.check("parent %s manifest = %s..." % (p, sha[:16]), h == sha, h)


CONTROLS = [
    ("IsOpen + 0x0 `cmp [rcx+28h], -1` -> `cmp [rcx+28h], 0` (wrong sentinel)", 0x59D924, bytes([0x00])),
    ("IsOpen + 0x0 qword compare -> dword compare + nop (width)", 0x59D920, bytes.fromhex("837928ff90")),
    ("IsOpen + 0x15 `xor al, al` -> `xor eax, eax` (full-register result)", 0x59D935, bytes.fromhex("31c0")),
    ("IsOpen + 0x13 `jne` -> `je` (polarity)", 0x59D933, bytes([0x74])),
    ("IsOpen + 0xE compare +0x40 -> +0x48", 0x59D931, bytes([0x48])),
    ("constructor + 0x2B `mov [rcx+40h], -1` -> `[rcx+48h]` (cache field not initialised)", 0x59799E, bytes([0x48])),
    ("constructor + 0x24 `mov [rcx+30h], rbp` -> `[rcx+38h]`", 0x597997, bytes([0x38])),
    ("resolver + 0x15A `mov [r15+20h], rax` -> `[r15+28h]` (zero not stored to stream +0x40)", 0x59EFED,
     bytes([0x28])),
]


if __name__ == "__main__":
    run_review("rv_open", checks, packet, CONTROLS, 0x59D920)
