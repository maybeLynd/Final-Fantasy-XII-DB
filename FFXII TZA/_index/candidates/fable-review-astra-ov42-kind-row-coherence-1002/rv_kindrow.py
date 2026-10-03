"""rv_kindrow.py - FABLE independent re-derivation for ASTRA packet ov42-kind-row-coherence (d83287255, OV-42).

Own reader (rvlib.py: struct + capstone 5, copied unchanged from the sequence-queue review, sha256
69f9bc40be32abcc...).  Does not import or run ASTRA's prove.py, prove_owner_reload_order.py, capture*.py,
control.py, extent.py, validate-title-source-annotations.py, freeze/publication scripts or the shared role adapter
(reg_tracking.py).

Method:
  * image sha256; the .pdata chain of the classifier 00306BD0 followed record by record (three records, the last
    two CHAININFO, resolved to the root); the 440 physical bytes split into 284 code bytes (decoded linearly and
    exactly, ending at the last of three rets, + 0x11B), seven DWORDs at + 0x11C .. + 0x138 and 128 selector bytes
    at + 0x138 .. + 0x1B8 that the two indexed loads address; int3 padding up to the next root;
  * the quotient re-read (row carrier RSI, the 32-bit `sub`, the two descriptor loads, the zero-extended WORD
    divisor, the unsigned 32-bit `div`), then the guard (`add eax, -0x94`, `cmp eax, 0x7f`, `ja`): operand
    widths from the instruction bytes, register-write censuses between the `div` and the guard;
  * the 7 DWORD targets resolved and the published EBX value derived per target from a register-write census on
    the local CFG (kind 3 has no arm: it is EBX's initial 3); every one of the 128 selector bytes enumerated, giving
    the full q -> kind map;
  * the return-use of 0032FC30 on the kind-publishing path: a def-use read of RAX from its call to the next RAX
    definition, plus the first instruction of the callee 0032ED70;
  * a concrete emulation (unicorn) of the ORIGINAL classifier from its entry: 0032F6E0, 00309230, 0032FC30 and
    0020E600 are stubbed by a code hook (each returns at once with a scripted RAX); 0032ED70 (a 16-byte leaf) runs
    from the image.  Sweeps of q, full-32 edge cases, random rows, two descriptors, zero stride, the entry gate and
    the 0032FC30 return.  The queue writer's kind-4 arm (00306760 + 0xE8 .. + 0x17A) is emulated the same way as in
    the sequence-queue review for the consistency and countermodel checks;
  * a raw E8/E9 rel32 and 0F 8x census, a rip-relative/image-base-relative disp32 census and a pointer-value scan
    for references to 00306BD0; a disp32 census (rip-relative and image-base-relative) of instructions whose access
    covers the kind cell 022C215C;
  * controls patch a private in-memory copy of the image; the exe on disk is never written and its sha256 is
    rechecked at the end.
"""
import hashlib
import json
import os
import random
import struct
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rvlib import Img, Body, Report, check_manifest, find_exe, SHA256 as SHA_PIN  # noqa: E402
from capstone.x86 import X86_OP_MEM  # noqa: E402

F = 0x00306BD0
CODE_END = F + 0x11C      # 284 code bytes
DW = F + 0x11C            # seven DWORDs
SEL = F + 0x138           # 128 selector bytes
END = F + 0x1B8           # 440 physical bytes
NEXT_ROOT = 0x00306D90
DIV = F + 0xB2
GUARD_ADD, GUARD_CMP, GUARD_JA = F + 0xB4, F + 0xB9, F + 0xBC
STORE = F + 0x10B
KINDCELL = 0x022C215C
STATECELL = 0x022C2160
OWNERCELL = 0x022C2168
FLAGQ = 0x022C6E48
DESC = 0x02EBF138
LOOKUP = 0x0020E600
GATE = 0x0032F6E0
ROWWORD = 0x00309230
ARMER = 0x0032FC30
MARK = 0x0032ED70
CALLER, CALLER_END = 0x0030CE10, 0x0030CF3F
CALLSITE = CALLER + 0xFD
SLUG = "ov42-kind-row-coherence"
PRODUCER = "d83287255"
# queue writer (reviewed in fable-review-astra-ov42-sequence-queue-source-1002)
Q = 0x00306760
Q_END = Q + 0x38F
Q_ARM, Q_ARM_END, Q_STORE = Q + 0xE8, Q + 0x17A, Q + 0x174
QUEUE = 0x022C2178
SEQCTX = 0x02EBF190
Q_CALLEES = [0x306D90, 0x861EC0, 0x30D720, 0x30D550, LOOKUP]
CANDS = list(range(511, 535))


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


def readers(B, fam, lo=None, hi=None):
    return [a for a in B.order if fam in B[a].reg_reads and (lo is None or lo <= a) and (hi is None or a < hi)]


def rip_target(I):
    for m in I.mems:
        if m["base"] == "rip":
            return I.address + I.size + m["disp"]
    return None


def is_root(img, va):
    po = img.off(img.base + img.exc_rva)
    for i in range(img.exc_size // 12):
        b, en, u = struct.unpack_from("<III", img.d, po + i * 12)
        if b + img.base == va:
            return not ((img.d[img.off(img.base + u)] >> 3) & 4)
    return False


def table(img):
    """The 7 DWORD targets and the 128 selector bytes, read from the image."""
    tg = [img.base + img.u32(DW + 4 * i) for i in range(7)]
    sel = list(img.read(SEL, 128))
    return tg, sel


def ext_reach(B, frm, extra, avoid=()):
    """Local CFG reach with extra edges (the indirect jump's table targets)."""
    avoid = set(avoid)
    seen, stack = set(), [frm]
    while stack:
        a = stack.pop()
        if a in seen or a in avoid or a not in B.ins:
            continue
        seen.add(a)
        stack.extend(B.succ(a))
        stack.extend(extra.get(a, []))
    return seen


def published_by_target(img, B, t):
    """Follow the straight line from a table target to the kind store; return the last EBX writer on it."""
    a, last = t, None
    steps = 0
    while a != STORE and steps < 20:
        I = B.ins.get(a)
        if I is None:
            return None, None
        if "rbx" in I.reg_writes:
            last = a
        s = B.succ(a)
        if len(s) != 1:
            return None, None
        a = s[0]
        steps += 1
    return (last, a == STORE)


def derived_map(img, B):
    """q -> kind for q in 148..275 from the image's tables and the per-target EBX writer; None if not derivable."""
    tg, sel = table(img)
    kind_of_target = {}
    for i, t in enumerate(tg):
        w, ok = published_by_target(img, B, t)
        if not ok:
            kind_of_target[i] = None
        elif w is None:
            kind_of_target[i] = "EBX0"     # EBX as it stands at the indirect jump
        else:
            I = B[w]
            kind_of_target[i] = I.imm[0] if (I.mnemonic == "mov" and I.imm) else None
    init = None
    if T(B, F + 0x3A).startswith("mov ebx, "):
        init = B[F + 0x3A].imm[0]
    m = {}
    for x, s in enumerate(sel):
        k = kind_of_target.get(s) if s < 7 else None
        if k == "EBX0":
            k = init
        m[0x94 + x] = k
    return m, kind_of_target, tg, sel


def kind_of_q(m, q):
    q &= 0xFFFFFFFF
    x = (q - 0x94) & 0xFFFFFFFF
    return m[0x94 + x] if x <= 0x7F else 7


def queue_formula(q):
    w = q & 0xFFFF
    return 0xFFFFFFFF if w == 0xFFFF else (w - 0xD0) & 0xFFFFFFFF


def ranges_of(m):
    out, cur = [], None
    for q in sorted(m):
        if cur and cur[2] == m[q] and cur[1] == q - 1:
            cur[1] = q
        else:
            cur = [q, q, m[q]]
            out.append(cur)
    return out


# ------------------------------------------------------------------ emulation of the original code
class Emu(object):
    STK, RET, SCR, UNIT, DSC = 0x7F000000, 0x7E000000, 0x50000000, 0x41000000, 0x42000000
    OWNER = 0x0000000061000000

    def __init__(self, img, code_ranges, stubs):
        from unicorn import Uc, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE, UC_HOOK_MEM_WRITE, UC_HOOK_INTR
        from unicorn import UC_HOOK_MEM_READ_UNMAPPED, UC_HOOK_MEM_FETCH_UNMAPPED, UC_HOOK_MEM_WRITE_UNMAPPED
        from unicorn import x86_const as X
        self.X = X
        mu = self.mu = Uc(UC_ARCH_X86, UC_MODE_64)
        pages = set()
        spans = list(code_ranges) + [(0x022BE000, 0x022C7000), (0x02EBF000, 0x02EC0000)]
        for c in stubs:
            spans.append((c, c + 1))
        for s, e in spans:
            for p in range(s & ~0xFFF, (e + 0xFFF) & ~0xFFF, 0x1000):
                pages.add(p)
        for p in sorted(pages):
            mu.mem_map(p, 0x1000)
            buf = bytearray(0x1000)
            try:
                o = img.off(p)
                buf[:] = img.d[o:o + 0x1000].ljust(0x1000, b"\0")
            except ValueError:
                pass  # .data virtual tail: zero
            mu.mem_write(p, bytes(buf))
        for a in (self.STK, self.SCR, self.UNIT, self.DSC):
            mu.mem_map(a, 0x10000)
        mu.mem_map(self.RET, 0x1000)
        self.code_ranges = list(code_ranges)
        self.stubs = set(stubs)
        self.stub_rax = {}
        self.swap_desc = None
        self.until = None
        self.trace, self.writes, self.intr, self.fault, self.left = [], [], None, None, None

        def ch(uc, addr, size, ud):
            if addr == self.until:
                uc.emu_stop()
                return
            if addr in self.stubs:
                rsp = uc.reg_read(X.UC_X86_REG_RSP)
                self.trace.append((addr, uc.reg_read(X.UC_X86_REG_RCX), uc.reg_read(X.UC_X86_REG_RDX)))
                if addr == LOOKUP and self.swap_desc is not None:
                    uc.mem_write(DESC, struct.pack("<Q", self.swap_desc))
                uc.reg_write(X.UC_X86_REG_RAX, self.stub_rax.get(addr, self.SCR + 0x100))
                uc.reg_write(X.UC_X86_REG_RIP, struct.unpack("<Q", bytes(uc.mem_read(rsp, 8)))[0])
                uc.reg_write(X.UC_X86_REG_RSP, rsp + 8)
                return
            if addr == MARK:
                self.trace.append((addr, uc.reg_read(X.UC_X86_REG_RCX), uc.reg_read(X.UC_X86_REG_RDX)))
            if addr != self.RET and not any(s <= addr < e for s, e in self.code_ranges):
                self.left = addr
                uc.emu_stop()

        def bad(uc, access, addr, size, value, ud):
            self.fault = addr
            return False

        def wh(uc, access, addr, size, value, ud):
            if not (self.STK <= addr < self.STK + 0x10000):
                self.writes.append((uc.reg_read(X.UC_X86_REG_RIP), addr, size, value & ((1 << (8 * size)) - 1)))

        def ih(uc, intno, ud):
            self.intr = (intno, uc.reg_read(X.UC_X86_REG_RIP))
            uc.emu_stop()

        mu.hook_add(UC_HOOK_CODE, ch)
        mu.hook_add(UC_HOOK_MEM_READ_UNMAPPED | UC_HOOK_MEM_FETCH_UNMAPPED | UC_HOOK_MEM_WRITE_UNMAPPED, bad)
        mu.hook_add(UC_HOOK_MEM_WRITE, wh)
        mu.hook_add(UC_HOOK_INTR, ih)

    def u32(self, a):
        return struct.unpack("<I", bytes(self.mu.mem_read(a, 4)))[0]

    def u64(self, a):
        return struct.unpack("<Q", bytes(self.mu.mem_read(a, 8)))[0]

    def setup(self, stride, key, state=0, owner=0, desc2=None):
        mu = self.mu
        for a in (self.SCR, self.UNIT, self.DSC):
            mu.mem_write(a, b"\0" * 0x10000)
        mu.mem_write(KINDCELL, struct.pack("<I", 0xA5A5A5A5))
        mu.mem_write(STATECELL, struct.pack("<I", state))
        mu.mem_write(OWNERCELL, struct.pack("<Q", owner))
        mu.mem_write(QUEUE, struct.pack("<I", 0x5A5A5A5A))
        mu.mem_write(FLAGQ + 24, struct.pack("<Q", 0))
        mu.mem_write(self.DSC + 8, struct.pack("<H", stride))
        mu.mem_write(self.DSC + 0xC, struct.pack("<I", key))
        if desc2 is not None:
            mu.mem_write(self.DSC + 0x108, struct.pack("<H", desc2[0]))
            mu.mem_write(self.DSC + 0x10C, struct.pack("<I", desc2[1]))
        mu.mem_write(DESC, struct.pack("<Q", self.DSC))
        mu.mem_write(SEQCTX, struct.pack("<Q", self.SCR))
        mu.mem_write(self.UNIT + 0x694, b"\xff\xff\xff")
        mu.mem_write(self.UNIT + 0x698, struct.pack("<Q", self.SCR + 0x800))
        mu.mem_write(self.UNIT + 8, struct.pack("<I", 0xCAFE0008))

    def run(self, start, rcx, rdx, until, regs=None):
        from unicorn import UcError
        X = self.X
        sp = self.STK + 0x8000
        self.mu.mem_write(sp, struct.pack("<Q", self.RET))
        self.mu.reg_write(X.UC_X86_REG_RSP, sp)
        base = {"rax": 0xAAAAAAAAAAAAAAAA, "rbx": 0xBBBBBBBBBBBBBBBB, "rdi": 0xDDDDDDDDDDDDDDDD,
                "rsi": 0x5151515151515151, "r14": 0xEEEEEEEEEEEEEEEE, "rcx": rcx, "rdx": rdx}
        base.update(regs or {})
        for k, v in base.items():
            self.mu.reg_write(getattr(X, "UC_X86_REG_" + k.upper()), v)
        self.trace, self.writes, self.intr, self.fault, self.left = [], [], None, None, None
        self.until = until
        try:
            self.mu.emu_start(start, until, count=20000)
        except UcError as e:
            if self.intr is None and self.fault is None:
                self.fault = "UcError %s" % e
        r = dict((k, self.mu.reg_read(getattr(X, "UC_X86_REG_" + k.upper())))
                 for k in ("rax", "rbx", "rdi", "rsi", "r14", "rip", "rsp"))
        r["kind"] = self.u32(KINDCELL)
        r["state"] = self.u32(STATECELL)
        r["owner"] = self.u64(OWNERCELL)
        r["queue"] = self.u32(QUEUE)
        r["flag3"] = self.u64(FLAGQ + 24)
        r["kwrites"] = [w for w in self.writes if w[1] <= KINDCELL < w[1] + w[2]]
        r["qwrites"] = [w for w in self.writes if w[1] == QUEUE]
        r["trace"], r["intr"], r["fault"], r["left"] = list(self.trace), self.intr, self.fault, self.left
        r["writes"] = list(self.writes)
        r["ok"] = (r["rip"] == Emu.RET and not r["fault"] and not r["intr"] and not r["left"])
        return r


BASEV = 0x0000000123450000     # 0020E600's stub return (only its low 32 bits matter)


def classifier_emu(img):
    return Emu(img, [(F, CODE_END), (MARK, MARK + 0x10)], [GATE, ROWWORD, ARMER, LOOKUP])


def classify(E, q=None, stride=60, row=None, rem=0, hi=0, state=0, owner=0, gate=0, armer_rax=0x77,
             base=BASEV, desc2=None, rcx=None):
    E.setup(stride, 0x1D74, state=state, owner=owner, desc2=desc2)
    E.stub_rax = {GATE: gate, ROWWORD: 0x1234, ARMER: armer_rax, LOOKUP: base}
    E.swap_desc = (Emu.DSC + 0x100) if desc2 is not None else None
    if row is None:
        row = (hi << 32) | (((base & 0xFFFFFFFF) + q * stride + rem) & 0xFFFFFFFF)
    r = E.run(F, Emu.OWNER if rcx is None else rcx, row, Emu.RET)
    E.swap_desc = None
    return r


def emu_checks(img, R, small=False):
    B = Body(img, F, CODE_END)
    m, kot, tg, sel = derived_map(img, B)
    E = classifier_emu(img)
    # ---- one normal run, inspected in full
    r = classify(E, q=210)
    tr = [t[0] for t in r["trace"]]
    R.check("emulated full classifier from the entry (state 022C2160 = 0, 0032F6E0 -> 0, q = 210): returns EAX = 1 "
            "with RBX/RSI/RDI restored; writes state 1, the owner QWORD 022C2168 = entry RCX, state 2, then kind 4 to "
            "022C215C (one 4-byte store from 00306BD0 + 0x10B); calls 0032F6E0, 00309230, 0032FC30, 0032ED70 (run "
            "from the image), 0020E600 in that order",
            r["ok"] and r["rax"] & 0xFFFFFFFF == 1 and r["rbx"] == 0xBBBBBBBBBBBBBBBB and
            r["rsi"] == 0x5151515151515151 and r["rdi"] == 0xDDDDDDDDDDDDDDDD and r["kind"] == 4 and
            r["state"] == 2 and r["owner"] == Emu.OWNER and
            [(w[0], w[2]) for w in r["kwrites"]] == [(STORE, 4)] and
            [w[3] for w in r["writes"] if w[1] == STATECELL] == [1, 2] and
            tr == [GATE, ROWWORD, ARMER, MARK, LOOKUP],
            "rax %X kind %X state %X owner %X trace %s kw %s ok %s" % (
                r["rax"], r["kind"], r["state"], r["owner"], ["%X" % t for t in tr],
                [("%X" % w[0], w[2]) for w in r["kwrites"]], r["ok"]))
    args = dict((t[0], (t[1], t[2])) for t in r["trace"])
    for k_ in (GATE, ROWWORD, ARMER, MARK, LOOKUP):
        args.setdefault(k_, (None, None))
    R.check("emulated: 0032F6E0 gets ECX = 3; 00309230 gets RCX = entry RCX, RDX = entry RDX (the row); 0032FC30 gets "
            "ECX = 3, EDX = 00309230's EAX; 0032ED70 gets ECX = 3 and ORs 1 into QWORD 022C6E48 + 3*8; the lookup "
            "gets ECX = descriptor DWORD +0xC",
            None not in [v[0] for v in args.values()] and args[GATE][0] & 0xFFFFFFFF == 3 and args[ROWWORD][0] == Emu.OWNER and
            args[ROWWORD][1] == ((BASEV & 0xFFFFFFFF) + 210 * 60) and args[ARMER][0] & 0xFFFFFFFF == 3 and
            args[ARMER][1] & 0xFFFFFFFF == 0x1234 and args[MARK][0] & 0xFFFFFFFF == 3 and r["flag3"] == 1 and
            args[LOOKUP][0] & 0xFFFFFFFF == 0x1D74,
            str(dict(("%X" % k, ("%X" % v[0] if v[0] is not None else None, "%X" % v[1] if v[1] is not None else None))
                     for k, v in args.items())))
    # ---- sweep q 0..0x200 with stride 60 and varying in-stride remainder
    bad, k4 = [], []
    for q in range(0, 0x201):
        r = classify(E, q=q, rem=q % 60)
        want = kind_of_q(m, q)
        if not r["ok"] or r["kind"] != want or r["rax"] & 0xFFFFFFFF != 1:
            bad.append("q %d kind %X want %s" % (q, r["kind"], want))
        if r["kind"] == 4:
            k4.append(q)
    R.check("emulated sweep q = 0..512 (stride 60, row = base + 60q + q mod 60): the published kind equals the map "
            "derived from the bytes for every q, and kind 4 is published exactly for q = 208..225",
            not bad and k4 == list(range(208, 226)), "; ".join(bad[:3]) + " k4 %s" % (k4[:3] + k4[-3:]))
    # ---- full-32 edge cases
    edge = [
        ("q 65744 (0x100D0, low16 208) -> kind 7", dict(q=65744), 7),
        ("q 0x10000 + 225 (low16 225) -> kind 7", dict(q=0x10000 + 225), 7),
        ("q 0x10094 (low16 148) -> kind 7", dict(q=0x10094), 7),
        ("q 147 -> 7 (add wraps to FFFFFFFF, above 0x7F unsigned)", dict(q=147), 7),
        ("q 0 -> 7", dict(q=0), 7),
        ("q 0xFFFFFFFF (stride 1, row = base - 1) -> 7", dict(q=0xFFFFFFFF, stride=1), 7),
        ("q 0x80000000 + 210 (stride 1) -> 7", dict(q=0x80000000 + 210, stride=1), 7),
        ("q 208 with row upper 32 bits 7 -> 4 (only low32 enters)", dict(q=208, hi=7), 4),
        ("q 225 with lookup return upper 32 bits 0x123 -> 4", dict(q=225, base=(0x123 << 32) | 0x23450000), 4),
        ("row 60 below the base (D = 2^32 - 60, q = 71582787) -> 7", dict(q=-1, rem=0), 7),
        ("stride 0xFFFF (zero-extended), q 210 -> 4", dict(q=210, stride=0xFFFF), 4),
        ("stride 0x8000, q 226 -> 7", dict(q=226, stride=0x8000), 7),
        ("q 275 -> kind 2; q 276 -> 7", dict(q=275), 2),
        ("q 276 -> 7", dict(q=276), 7),
        ("q 148 -> kind 5", dict(q=148), 5),
    ]
    bad = []
    for name, kw, want in edge:
        r = classify(E, **kw)
        if not r["ok"] or r["kind"] != want:
            bad.append("%s: got %X fault %s intr %s" % (name, r["kind"], r["fault"], r["intr"]))
    R.check("emulated full-32 edge cases (%d): quotients whose low 16 bits lie in 148..275 (208..225 among them) but "
            "whose full value lies outside 148..275 publish kind 7; wraps, upper row/lookup bits, stride FFFF and the band ends behave as the full "
            "unsigned 32-bit formula" % len(edge), not bad, "; ".join(bad[:3]))
    rnd = random.Random(7)
    n = 20 if small else 200
    bad = []
    for _ in range(n):
        row = rnd.getrandbits(64)
        base = rnd.getrandbits(64)
        s = rnd.choice([1, 2, 60, 0x3C, 0x80, 0x1234, 0xFFFF, rnd.randrange(1, 0x10000)])
        if rnd.random() < 0.5:   # bias toward the band
            row = (rnd.getrandbits(32) << 32) | (((base & 0xFFFFFFFF) + s * rnd.randrange(140, 290) +
                                                  rnd.randrange(s)) & 0xFFFFFFFF)
        r = classify(E, row=row, stride=s, base=base)
        q = (((row & 0xFFFFFFFF) - (base & 0xFFFFFFFF)) & 0xFFFFFFFF) // s
        if not r["ok"] or r["kind"] != kind_of_q(m, q):
            bad.append("row %X base %X s %X: %X vs %s" % (row, base, s, r["kind"], kind_of_q(m, q)))
    R.check("emulated %d random 64-bit rows / lookup returns / strides: each published kind equals "
            "map(((low32(row) - low32(base)) mod 2^32) // u16 stride)" % n, not bad, "; ".join(bad[:2]))
    # ---- two descriptors
    r = classify(E, q=0, row=(BASEV & 0xFFFFFFFF) + 60 * 104, desc2=(30, 0x9999))
    key = ([t[1] for t in r["trace"] if t[0] == LOOKUP] + [None])[0]
    key = None if key is None else key & 0xFFFFFFFF
    R.check("emulated: when 02EBF138 is repointed during the lookup call, the key came from the first descriptor "
            "(+0xC = 1D74) and the divisor from the second (+8 = 30): 60*104 / 30 = 208 -> kind 4 (the first "
            "descriptor's stride 60 would give q 104 -> kind 7)",
            key == 0x1D74 and r["kind"] == 4, "key %s kind %X" % (key, r["kind"]))
    # ---- zero stride
    r = classify(E, q=210, stride=0)
    R.check("emulated: stride WORD 0 -> divide error (#DE, interrupt 0) at the DIV 00306BD0 + 0xB2; the kind cell "
            "is not written (no zero-divisor guard), state 022C2160 already holds 2",
            r["intr"] is not None and r["intr"][0] == 0 and r["intr"][1] == DIV and not r["kwrites"] and
            r["state"] == 2, "intr %s fault %s kind %X state %X" % (r["intr"], r["fault"], r["kind"], r["state"]))
    # ---- the entry gate
    g = {}
    g["same"] = classify(E, q=210, state=1, owner=Emu.OWNER)
    g["other"] = classify(E, q=210, state=1, owner=Emu.OWNER + 0x10)
    g["s2"] = classify(E, q=210, state=2, owner=Emu.OWNER)
    g["s5"] = classify(E, q=210, state=5, owner=Emu.OWNER)
    g["gate"] = classify(E, q=210, gate=1)
    R.check("emulated entry gate: state 1 with the same owner QWORD publishes (EAX 1, kind 4); state 1 with another "
            "owner, state 2 and state 5 return EAX 0 with no call and no write to kind/state/owner; 0032F6E0 "
            "returning nonzero returns EAX 0 after writing state 1 and the owner, with the kind cell untouched",
            g["same"]["ok"] and g["same"]["rax"] & 0xFFFFFFFF == 1 and g["same"]["kind"] == 4 and
            all(g[k]["ok"] and g[k]["rax"] & 0xFFFFFFFF == 0 and not g[k]["trace"] and not g[k]["kwrites"] and
                not [w for w in g[k]["writes"] if w[1] in (STATECELL, OWNERCELL)] for k in ("other", "s2", "s5")) and
            g["gate"]["ok"] and g["gate"]["rax"] & 0xFFFFFFFF == 0 and not g["gate"]["kwrites"] and
            g["gate"]["state"] == 1 and g["gate"]["owner"] == Emu.OWNER and
            [t[0] for t in g["gate"]["trace"]] == [GATE],
            " ".join("%s:rax %X kind %X st %X tr %d" % (k, v["rax"] & 0xFFFFFFFF, v["kind"], v["state"],
                                                      len(v["trace"])) for k, v in g.items()))
    # ---- the 0032FC30 return is dead
    outs = set()
    for ax in (0, 1, 0xFFFFFFFF, 0x8000000000000000, 0xFFFFFFFFFFFFFFFF):
        for q in (207, 208, 225, 226):
            r = classify(E, q=q, armer_rax=ax)
            outs.add((q, r["kind"], r["rax"] & 0xFFFFFFFF, r["flag3"], r["ok"],
                      tuple((w[1], w[2], w[3]) for w in r["writes"])))
    R.check("emulated: 0032FC30 returning 0, 1, FFFFFFFF, 2^63 or 2^64 - 1 gives the same kind, return, writes and "
            "0032ED70 effect for q 207/208/225/226 (its return is not used)",
            len(outs) == 4 and all(o[4] for o in outs), "%d distinct outcomes" % len(outs))
    queue_emu_checks(img, R, m)


def queue_emu_checks(img, R, m):
    """The queue writer's kind-4 arm, as in the sequence-queue review, used for the consistency checks."""
    E = Emu(img, [(Q, Q_END)], Q_CALLEES)

    def arm(q, stride=60):
        E.setup(stride, 0x1D74)
        E.stub_rax = {LOOKUP: BASEV}
        row = (BASEV & 0xFFFFFFFF) + stride * q
        return E.run(Q_ARM, 0, 0, Q_ARM_END, regs={"rbx": Emu.UNIT, "rdi": row & 0xFFFFFFFF, "r14": img.base})

    bad = []
    for q in range(208, 226):
        r = arm(q)
        if r["queue"] != q - 208 or r["fault"] or r["intr"] or r["rip"] != Q_ARM_END:
            bad.append("%d -> %X" % (q, r["queue"]))
    k4 = [q for q in range(0x94, 0x114) if kind_of_q(m, q) == 4]
    R.check("conditional invariant: the classifier's kind-4 band is q = 208..225; the emulated queue arm, given the "
            "same quotient, stores q - 208 = 0..17 for each, none of 303..326 (the queue values of ids 511..534)",
            k4 == list(range(208, 226)) and not bad and not set(range(0, 18)) & set(range(303, 327)),
            "; ".join(bad[:3]))
    r1 = arm(511)
    r2 = arm(65744)
    R.check("countermodel 1: classifier q 208 publishes kind 4 (map) while a later queue quotient 511 stores 303 "
            "(emulated queue arm)", kind_of_q(m, 208) == 4 and r1["queue"] == 303 == queue_formula(511),
            "queue %X" % r1["queue"])
    R.check("countermodel 2: q 65744 (0x100D0) - the classifier publishes kind 7 (map), while the queue arm narrows "
            "it to low16 208 and stores 0 (emulated)", kind_of_q(m, 65744) == 7 and r2["queue"] == 0 ==
            queue_formula(65744), "queue %X" % r2["queue"])
    allq = [q for q in range(0, 0x30000) if kind_of_q(m, q) == 4]
    R.check("over q = 0 .. 0x2FFFF only 208..225 publish kind 4 (the full-32 guard does not alias at 0x100D0 / "
            "0x200D0); the queue arm's low16 formula maps 0x100D0..0x100E1 and 0x200D0..0x200E1 to 0..17 as well",
            allq == list(range(208, 226)) and all(queue_formula(q) == q - 0x100D0 for q in range(0x100D0, 0x100E2))
            and all(queue_formula(q) == q - 0x200D0 for q in range(0x200D0, 0x200E2)), str(allq[:3] + allq[-3:]))


def raw_refs(img, targets):
    name, va, vs, ra, rs = [s for s in img.secs if s[0] == ".text"][0]
    code = img.d[ra:ra + min(vs, rs)]
    base = img.base + va
    out = {t: [] for t in targets}
    for i in range(len(code) - 5):
        op = code[i]
        if op in (0xE8, 0xE9):
            t = base + i + 5 + struct.unpack_from("<i", code, i + 1)[0]
            if t in out:
                out[t].append((base + i, "call" if op == 0xE8 else "jmp"))
        elif op == 0x0F and 0x80 <= code[i + 1] <= 0x8F and i + 6 <= len(code):
            t = base + i + 6 + struct.unpack_from("<i", code, i + 2)[0]
            if t in out:
                out[t].append((base + i, "jcc"))
    return out


def insn_covering(img, va):
    """Decode the .pdata record containing va linearly from its begin; return the instruction covering va."""
    rec = img.pdata(va)
    if rec is None:
        return None
    b, e = rec
    pos = b
    for ci in img.cs.disasm(img.read(b, e - b), b):
        if ci.address != pos:
            return None
        if ci.address <= va < ci.address + ci.size:
            return ci
        pos = ci.address + ci.size
    return None


def disp_census(img, lo, hi):
    """Instructions in .text with a rip-relative or image-base-relative disp32 whose ACCESS range meets [lo, hi)."""
    name, va, vs, ra, rs = [s for s in img.secs if s[0] == ".text"][0]
    code = img.d[ra:ra + min(vs, rs)]
    tb = img.base + va
    cand = set()
    for i in range(len(code) - 4):
        disp = struct.unpack_from("<i", code, i)[0]
        for imm in (0, 1, 2, 4):
            t = tb + i + 4 + imm + disp
            if lo - 16 <= t < hi:
                cand.add(tb + i)
        ud = struct.unpack_from("<I", code, i)[0] + img.base
        if lo - 16 <= ud < hi:
            cand.add(tb + i)
    found, unresolved, unanchored = {}, [], []
    for h in sorted(cand):
        ci = insn_covering(img, h)
        cis = [ci]
        if ci is None:
            # no .pdata record (a leaf) or a decode desync: decode back 1..15 bytes, keep every reading whose
            # displacement field is this hit; reported separately as unanchored
            cis = []
            for k in range(1, 16):
                try:
                    c2 = next(img.cs.disasm(img.read(h - k, 16), h - k))
                except StopIteration:
                    continue
                if c2.address + c2.size >= h + 4 and c2.address < h:
                    cis.append(c2)
            unresolved.append(h)
        for ci in cis:
            for op in ci.operands:
                if op.type != X86_OP_MEM:
                    continue
                mm = op.mem
                if mm.base and ci.reg_name(mm.base) == "rip":
                    t = ci.address + ci.size + mm.disp
                elif mm.disp + img.base >= lo - 16 and mm.disp + img.base < hi:
                    t = (mm.disp & 0xFFFFFFFF) + img.base      # image-base-relative (base register holds 0x120000)
                else:
                    continue
                if t < hi and t + op.size > lo:
                    rec = (ci.mnemonic + " " + ci.op_str, t, op.size, ci.reg_name(mm.base) if mm.base else None)
                    if h in unresolved:
                        unanchored.append((ci.address, rec))
                    else:
                        found[ci.address] = rec
    return found, unresolved, unanchored


def census_checks(img, R):
    print("== raw direct-reference census (E8/E9 rel32 and 0F 8x jcc, .text)")
    rc = raw_refs(img, [F, F + 0xE7, STORE, DIV])
    R.note("00306BD0 raw direct references (%d): %s (indirect callers not covered)" %
           (len(rc[F]), ", ".join("%X %s" % x for x in rc[F])))
    R.check("00306BD0 has exactly one raw direct reference, the call at 0030CE10 + 0xFD (0030CF0D)",
            rc[F] == [(CALLSITE, "call")])
    R.note("raw direct references to the kind-4 arm + 0xE7: %d; to the kind store + 0x10B: %d; to the DIV + 0xB2: %d"
           % (len(rc[F + 0xE7]), len(rc[STORE]), len(rc[DIV])))
    found, unres, unanch = disp_census(img, F, F + 1)
    R.note("rip-relative / image-base-relative disp32 references to 00306BD0 (e.g. a `lea` forming its address): %d"
           " %s; unresolved candidates %d, unanchored readings %d" % (
               len(found), ["%X %s" % (a, v[0]) for a, v in sorted(found.items())], len(unres), len(unanch)))
    rva = struct.pack("<I", F - img.base)
    hits, i = [], img.d.find(rva)
    while i >= 0:
        hits.append(i)
        i = img.d.find(rva, i + 1)
    secs = []
    for h in hits:
        for nm, sva, svs, sra, srs in img.secs:
            if sra <= h < sra + srs:
                secs.append((nm, img.base + sva + (h - sra)))
    vahits = img.d.count(struct.pack("<Q", F))
    R.note("the RVA DWORD %08X occurs %d times in the file: %s; the 8-byte VA occurs %d times" % (
        F - img.base, len(hits), ", ".join("%s %X" % s for s in secs), vahits))
    R.check("no stored or formed pointer to 00306BD0 outside unwind metadata: no disp32 reference, no 8-byte VA, "
            "and the RVA DWORD occurs only in .pdata (the root record) and in .rdata at the two CHAININFO footers "
            "(01D74FAC, 01D74FC0)",
            not found and not unanch and vahits == 0 and sorted(s[0] for s in secs) == [".pdata", ".rdata", ".rdata"] and
            sorted(s[1] for s in secs if s[0] == ".rdata") == [0x1D74FAC, 0x1D74FC0])
    C = Body(img, CALLER, CALLER_END)
    R.check("the caller 0030CE10 (three chained .pdata records, decodes exactly to + 0x12F): RSI = entry RCX (+ 0xA), "
            "RBP = entry RDX (+ 0xD), neither rewritten before the call; + 0xF7 `mov rdx, rbp`, + 0xFA `mov rcx, rsi`, "
            "+ 0xFD `call 00306BD0`; a nonzero EAX sets bit 29 of QWORD [rsi] (+ 0x106)",
            img.pdata_cover(CALLER, CALLER_END)[1] and C.exact and
            T(C, CALLER + 0xA) == "mov rsi, rcx" and T(C, CALLER + 0xD) == "mov rbp, rdx" and
            writers(C, "rsi", CALLER + 0xB, CALLSITE) == [] and writers(C, "rbp", CALLER + 0xE, CALLSITE) == [] and
            T(C, CALLER + 0xF7) == "mov rdx, rbp" and T(C, CALLER + 0xFA) == "mov rcx, rsi" and
            T(C, CALLSITE) == "call 0x306bd0" and T(C, CALLER + 0x102) == "test eax, eax" and
            T(C, CALLER + 0x106) == "or qword ptr [rsi], 0x20000000")
    rc2 = raw_refs(img, [CALLER])
    ents, ok = img.pdata_cover(0x30CBE0, 0x30CE01)
    R.note("0030CE10 raw direct references (%d): %s" % (len(rc2[CALLER]), ", ".join("%X %s" % x for x in rc2[CALLER])))
    R.check("0030CE10 has exactly one raw direct reference, the call at 0030CD99 = 0030CBE0 + 0x1B9 (0030CBE0's "
            ".pdata chain tiles 0030CBE0 .. 0030CE01 and resolves to that root)",
            rc2[CALLER] == [(0x30CD99, "call")] and ok and ents[-1][0] <= 0x30CD99 < ents[-1][1],
            str([(hex(b), hex(e), fl) for b, e, fl, rr in ents]))
    print("== kind-cell access census (rip-relative and image-base-relative disp32 whose access covers 022C215C)")
    found, unres, unanch = disp_census(img, KINDCELL, KINDCELL + 4)
    for a in sorted(found):
        txt, t, sz, bs = found[a]
        rec = img.pdata(a)
        R.note("%X  %-44s target %X size %d  (.pdata record %X..%X)" % (a, txt, t, sz, rec[0], rec[1]))
    R.note("unresolved candidates (no .pdata record or decode desync): %d %s; their decode-back readings that "
           "access the cell: %s" % (len(unres), ["%X" % h for h in unres], ["%X %s" % (a, v[0]) for a, v in unanch]))
    for h in unres:
        rd_ = []
        for k in range(1, 16):
            try:
                c2 = next(img.cs.disasm(img.read(h - k, 16), h - k))
            except StopIteration:
                continue
            if c2.address + c2.size >= h + 4 and c2.address < h:
                for op in c2.operands:
                    if op.type == X86_OP_MEM and op.mem.base and c2.reg_name(op.mem.base) == "rip":
                        rd_.append("%X `%s %s` -> %X (%d B)" % (c2.address, c2.mnemonic, c2.op_str,
                                                               c2.address + c2.size + op.mem.disp, op.size))
        R.note("unresolved %X decode-back readings: %s" % (h, "; ".join(rd_) or "none"))
    wr = sorted(a for a in found if found[a][0].startswith("mov") and "ptr [rip" in found[a][0].split(",")[0])
    rd = sorted(a for a in found if a not in wr)
    R.check("kind cell 022C215C: five instructions access it - writes at 00306BD0 + 0x10B (DWORD, EBX), 003065A1 "
            "(QWORD 022C215C..022C2163, RAX) and 0030670F (QWORD, RSI); reads at 00306633 and 003067AA (00306760 + "
            "0x4A, the dispatch); nothing else in this census",
            wr == [0x3065A1, 0x30670F, STORE] and rd == [0x306633, Q + 0x4A] and found[STORE][2] == 4 and
            found[0x3065A1][2] == 8 and found[0x30670F][2] == 8 and found[0x3065A1][1] == KINDCELL and
            found[0x30670F][1] == KINDCELL and not unanch, "writes %s reads %s" % (["%X" % a for a in wr], ["%X" % a for a in rd]))
    # the two QWORD stores write zero
    Z1 = Body(img, 0x306570, 0x3065C7)
    Z2 = Body(img, 0x3065D0, 0x306739)
    R.check("both QWORD stores write 0: 00306570 + 0x2F `xor eax, eax` then + 0x31 / + 0x38 store RAX to 022C215C and "
            "022C2168 (no RAX write between); 003065D0 + 0x5B `xor esi, esi`, RSI written nowhere else in "
            "003065D0 .. + 0x169 but the restore + 0x15C, then + 0x13F / + 0x146 store RSI to 022C215C and 022C2168",
            Z1.exact and T(Z1, 0x30659F) == "xor eax, eax" and writers(Z1, "rax", 0x3065A0, 0x3065AF) == [] and
            rip_target(Z1[0x3065A8]) == OWNERCELL and Z2.exact and T(Z2, 0x30662B) == "xor esi, esi" and
            writers(Z2, "rsi") == [0x30662B, 0x30672C] and rip_target(Z2[0x306716]) == OWNERCELL and
            T(Z2, 0x30670F).endswith(", rsi") and 0x30672C > 0x306716 and
            Z2.dominates(0x30662B, 0x30670F))
    found2, _, unanch2 = disp_census(img, OWNERCELL, OWNERCELL + 8)
    R.note("owner cell 022C2168 accessors (same census): %s" % ", ".join(
        "%X %s" % (a, found2[a][0]) for a in sorted(found2)))
    R.check("00306760 (the queue writer, .. + 0x3A8) has no access to the owner cell 022C2168 in this census",
            not [a for a in found2 if Q <= a < Q + 0x3A8] and not [a for a, v in unanch2 if Q <= a < Q + 0x3A8])


def checks(img, R, small=False):
    R.check("image sha256 = %s..." % SHA_PIN[:20], hashlib.sha256(img.d).hexdigest() == SHA_PIN or
            getattr(img, "_private", False))
    # ---------------- extent
    ents, ok = img.pdata_cover(F, END)
    R.check("00306BD0's .pdata: three records tile 00306BD0 .. + 0x1B8 (440 B) exactly - the root .. + 0x35, then "
            "CHAININFO records + 0x35 .. + 0x6D and + 0x6D .. + 0x1B8, each resolving to the root 00306BD0",
            ok and [(b - F, e - F, fl & 4, r) for b, e, fl, r in ents] ==
            [(0, 0x35, 0, F), (0x35, 0x6D, 4, F), (0x6D, 0x1B8, 4, F)],
            str([(hex(b - F), hex(e - F), fl) for b, e, fl, r in ents]))
    R.check("int3 padding 00306BD0 + 0x1B8 .. + 0x1C0 up to the next root record 00306D90",
            img.read(END, NEXT_ROOT - END) == b"\xcc" * (NEXT_ROOT - END) and is_root(img, NEXT_ROOT) and
            img.pdata(END) is None)
    B = Body(img, F, CODE_END)
    rets = [a for a in B.order if B[a].mnemonic == "ret"]
    R.check("code: 00306BD0 .. + 0x11C (284 B) decodes exactly; its last instruction is a `ret` at 00306CEB (+ 0x11B); "
            "there are three rets (+ 0x2B, + 0x6C, + 0x11B)",
            B.exact and B.order[-1] == F + 0x11B and rets == [F + 0x2B, F + 0x6C, F + 0x11B])
    r_, tails, outs = B.exits()
    ind = [a for a in B.order if B[a].mnemonic == "jmp" and B[a].direct_target() is None]
    dt = [B[a].direct_target() for a in B.order if B[a].direct_target() is not None and B[a].mnemonic != "call"]
    R.check("local CFG closed: no tail jump other than the one indirect `jmp rcx` (+ 0xD7), no branch leaves the code, "
            "no direct branch targets + 0x11C .. + 0x1B8",
            tails == [(F + 0xD7, None)] and not outs and ind == [F + 0xD7] and all(F <= t < CODE_END for t in dt))
    R.check("+ 0x11C .. + 0x138 are seven DWORDs (28 B) and + 0x138 .. + 0x1B8 are 128 selector bytes: the indexed "
            "loads address exactly 00306CEC and 00306D08 from the image base",
            SEL - DW == 28 and END - SEL == 128 and img.base + 0x1E6CEC == DW and img.base + 0x1E6D08 == SEL)
    # ---------------- row carrier and quotient
    R.check("RSI = entry RDX: home save `mov qword ptr [rsp + 0x10], rsi` (+ 0x0), `mov rsi, rdx` (+ 0x10), no RDX "
            "write before it; RSI written only at + 0x10, the two early-return restores (+ 0x21, + 0x62), `sub esi, "
            "eax` (+ 0xA1) and the restore + 0x101; the restores do not reach + 0xA1",
            T(B, F) == "mov qword ptr [rsp + 0x10], rsi" and T(B, F + 0x10) == "mov rsi, rdx" and
            not writers(B, "rdx", F, F + 0x10) and
            writers(B, "rsi") == [F + 0x10, F + 0x21, F + 0x62, F + 0xA1, F + 0x101] and
            F + 0xA1 not in B.reach(F + 0x21) and F + 0xA1 not in B.reach(F + 0x62))
    R.check("first descriptor: + 0x92 RAX = QWORD [02EBF138] (8 B); + 0x99 ECX = DWORD [rax + 0xC] (4 B); + 0x9C "
            "`call 0020E600`; + 0xA1 `sub esi, eax` (2B F0) - a 32-bit subtraction: D = (low32(row) - low32(base)) "
            "mod 2^32",
            T(B, F + 0x92).startswith("mov rax, qword ptr [rip") and rip_target(B[F + 0x92]) == DESC and
            B[F + 0x92].mems[0]["size"] == 8 and T(B, F + 0x99) == "mov ecx, dword ptr [rax + 0xc]" and
            B[F + 0x99].mems[0]["size"] == 4 and T(B, F + 0x9C) == "call 0x20e600" and
            T(B, F + 0xA1) == "sub esi, eax" and B[F + 0xA1].bytes == b"\x2b\xf0")
    R.check("second descriptor: + 0xA3 `xor edx, edx`; + 0xA5 RAX = QWORD [02EBF138] again (8 B); + 0xAC `movzx ecx, "
            "word ptr [rax + 8]` (2 B, zero-extended); + 0xB0 `mov eax, esi`; + 0xB2 `div ecx` (F7 F1: unsigned "
            "32-bit EDX:EAX / ECX)",
            T(B, F + 0xA3) == "xor edx, edx" and T(B, F + 0xA5).startswith("mov rax, qword ptr [rip") and
            rip_target(B[F + 0xA5]) == DESC and B[F + 0xA5].mems[0]["size"] == 8 and
            T(B, F + 0xAC) == "movzx ecx, word ptr [rax + 8]" and B[F + 0xAC].mems[0]["size"] == 2 and
            T(B, F + 0xB0) == "mov eax, esi" and T(B, DIV) == "div ecx" and B[DIV].bytes == b"\xf7\xf1")
    R.check("two separate loads, no divisor guard: the only 02EBF138 loads in the body are + 0x92 and + 0xA5 with the "
            "lookup call between; no cmp/test/jcc from + 0x8B to the DIV; ECX not written between the WORD load and "
            "the DIV; EDX written there only by the `xor`",
            [a for a in B.order if rip_target(B[a]) == DESC] == [F + 0x92, F + 0xA5] and
            not [a for a in B.order if F + 0x8B <= a < DIV and
                 (B[a].mnemonic in ("cmp", "test") or B[a].mnemonic.startswith("j"))] and
            writers(B, "rcx", F + 0xAD, DIV) == [] and writers(B, "rdx", F + 0x9D, DIV) == [F + 0xA3])
    # ---------------- the guard (no narrowing)
    R.check("the guard: + 0xB4 `add eax, 0xffffff6c` (05 6C FF FF FF: 32-bit, no 66 prefix) immediately after the "
            "DIV; + 0xB9 `cmp eax, 0x7f` (83 F8 7F: 32-bit); + 0xBC `ja` + 0xFC (77: unsigned) - the full 32-bit "
            "quotient, not a WORD of it, is biased by -0x94 and compared unsigned with 0x7F",
            B.order[B.order.index(DIV) + 1] == GUARD_ADD and T(B, GUARD_ADD) == "add eax, 0xffffff6c" and
            B[GUARD_ADD].bytes == bytes.fromhex("056cffffff") and T(B, GUARD_CMP) == "cmp eax, 0x7f" and
            B[GUARD_CMP].bytes == bytes.fromhex("83f87f") and B[GUARD_JA].bytes[0] == 0x77 and
            B[GUARD_JA].direct_target() == F + 0xFC)
    R.check("between the DIV and the `ja`, RAX is written only by the `add` (no movzx/cwde/and narrowing); the "
            "index loads use RAX zero-extended by that 32-bit `add`",
            writers(B, "rax", DIV + 1, GUARD_JA + 2) == [GUARD_ADD] and
            not [a for a in B.order if DIV < a <= GUARD_JA and B[a].bytes[:1] == b"\x66"])
    # ---------------- dispatch
    R.check("dispatch: + 0xBE RDX = image base (`lea`, rip-relative); + 0xC5 `movzx eax, byte ptr [rdx + rax + "
            "0x1e6d08]` (1 B) = selector 00306D08 + x; + 0xCD `mov ecx, dword ptr [rdx + rax*4 + 0x1e6cec]` (4 B) = "
            "DWORD 00306CEC + 4*sel; + 0xD4 `add rcx, rdx`; + 0xD7 `jmp rcx`; no RDX write between + 0xBE and + 0xD7",
            T(B, F + 0xBE).startswith("lea rdx, [rip") and rip_target(B[F + 0xBE]) == img.base and
            T(B, F + 0xC5) == "movzx eax, byte ptr [rdx + rax + 0x1e6d08]" and B[F + 0xC5].mems[0]["size"] == 1 and
            T(B, F + 0xCD) == "mov ecx, dword ptr [rdx + rax*4 + 0x1e6cec]" and B[F + 0xCD].mems[0]["size"] == 4 and
            T(B, F + 0xD4) == "add rcx, rdx" and T(B, F + 0xD7) == "jmp rcx" and
            writers(B, "rdx", F + 0xBF, F + 0xD7) == [])
    m, kot, tg, sel = derived_map(img, B)
    R.check("all 128 selector bytes are in 0..6, so every in-range x selects one of the seven DWORDs",
            max(sel) <= 6, "max %d" % max(sel))
    R.check("the seven DWORDs resolve to instruction boundaries: sel 0 + 0xEE, sel 1 + 0xF5, sel 2 + 0x101, sel 3 "
            "+ 0xE7, sel 4 + 0xD9, sel 5 + 0xE0, sel 6 + 0xFC",
            [t - F for t in tg] == [0xEE, 0xF5, 0x101, 0xE7, 0xD9, 0xE0, 0xFC] and all(t in B.ins for t in tg),
            " ".join("+%X" % (t - F) for t in tg))
    R.check("published EBX per selector (CFG straight line from each target to the store + 0x10B, last EBX writer): "
            "sel 0 -> 5, 1 -> 6, 2 -> no writer (EBX as at the jump), 3 -> 4, 4 -> 1, 5 -> 2, 6 -> 7; the `ja` default "
            "+ 0xFC -> 7",
            [kot[i] for i in range(7)] == [5, 6, "EBX0", 4, 1, 2, 7] and
            published_by_target(img, B, F + 0xFC) == (F + 0xFC, True), str(kot))
    R.check("kind 3 is EBX's initial value: + 0x3A `mov ebx, 3`; EBX's other writers are the six arms, the early-"
            "return restore + 0x5D (whose block ends in `ret` + 0x6C) and the restore + 0x111 after the store; none "
            "between + 0x3A and the indirect jump on the publishing path (calls preserve RBX only by the Win64 ABI)",
            T(B, F + 0x3A) == "mov ebx, 3" and
            writers(B, "rbx") == [F + 0x3A, F + 0x5D, F + 0xD9, F + 0xE0, F + 0xE7, F + 0xEE, F + 0xF5, F + 0xFC,
                                  F + 0x111] and F + 0xD7 not in B.reach(F + 0x5D))
    rg = ranges_of(m)
    R.check("the q -> kind map from the bytes, q = 0x94 + x for selector index x: 148 -> 5; 149 -> 6; 150..181 -> 7; "
            "182..207 -> 3; 208..225 -> 4; 226..261 -> 7; 262..274 -> 1; 275 -> 2; every other 32-bit q -> 7 (the "
            "unsigned `ja`); kind 4 exactly for q = 208..225",
            [tuple(x) for x in rg] == [(148, 148, 5), (149, 149, 6), (150, 181, 7), (182, 207, 3), (208, 225, 4),
                                       (226, 261, 7), (262, 274, 1), (275, 275, 2)],
            "; ".join("%d..%d -> %s" % tuple(x) for x in rg))
    # ---------------- the store and the return
    extra = {F + 0xD7: tg}
    R.check("the kind store: + 0x10B `mov dword ptr [rip + ...], ebx` to 022C215C (4 B), the body's only write to it; "
            "with the table edges added, every path from the entry to it passes the DIV; it is followed by EAX = 1 "
            "(+ 0x106) and the ret + 0x11B, while the two other rets return EAX = 0 (+ 0x1F, + 0x5B) without it",
            T(B, STORE).startswith("mov dword ptr [rip") and T(B, STORE).endswith(", ebx") and
            rip_target(B[STORE]) == KINDCELL and B[STORE].mems[0]["size"] == 4 and
            [a for a, mm in B.mem_writes() if rip_target(B[a]) == KINDCELL] == [STORE] and
            STORE in ext_reach(B, F, extra) and STORE not in ext_reach(B, F, extra, avoid=[DIV]) and
            T(B, F + 0x106) == "mov eax, 1" and T(B, F + 0x1F) == "xor eax, eax" and T(B, F + 0x5B) == "xor eax, eax"
            and STORE not in B.reach(F + 0x1F) and STORE not in B.reach(F + 0x5B))
    R.check("the entry gate: + 0xA EAX = DWORD [022C2160]; 0 -> + 0x35; 1 -> `cmp rdi, qword ptr [022C2168]` (+ 0x2C, "
            "RDI = entry RCX from + 0x13), equal -> + 0x35, else return 0; then + 0x41 state := 1, + 0x4B owner QWORD "
            "022C2168 := RDI, + 0x52 `call 0032F6E0` with ECX = 3, nonzero -> return 0; + 0x70 state := 2",
            rip_target(B[F + 0xA]) == STATECELL and T(B, F + 0x13) == "mov rdi, rcx" and
            T(B, F + 0x16) == "test eax, eax" and B[F + 0x18].direct_target() == F + 0x35 and
            T(B, F + 0x1A) == "cmp eax, 1" and B[F + 0x1D].direct_target() == F + 0x2C and
            T(B, F + 0x2C).startswith("cmp rdi, qword ptr [rip") and rip_target(B[F + 0x2C]) == OWNERCELL and
            B[F + 0x33].direct_target() == F + 0x1F and rip_target(B[F + 0x41]) == STATECELL and
            T(B, F + 0x41).endswith(", 1") and rip_target(B[F + 0x4B]) == OWNERCELL and
            T(B, F + 0x4B).endswith(", rdi") and T(B, F + 0x52) == "call 0x32f6e0" and
            T(B, F + 0x57) == "test eax, eax" and B[F + 0x59].direct_target() == F + 0x6D and
            rip_target(B[F + 0x70]) == STATECELL and T(B, F + 0x70).endswith(", 2"))
    # ---------------- the return use of 0032FC30
    after = [a for a in B.order if F + 0x86 < a <= F + 0x92]
    R.check("0032FC30's return is unused: after `call 0032FC30` (+ 0x86) the instructions are `mov ecx, ebx` (+ 0x8B), "
            "`call 0032ED70` (+ 0x8D) and `mov rax, qword ptr [02EBF138]` (+ 0x92), which writes RAX without reading "
            "it; no instruction in between reads RAX or the flags, and none branches",
            T(B, F + 0x86) == "call 0x32fc30" and [T(B, a) for a in after[:2]] == ["mov ecx, ebx", "call 0x32ed70"] and
            after[2] == F + 0x92 and "rax" in B[F + 0x92].reg_writes and "rax" not in B[F + 0x92].reg_reads and
            not readers(B, "rax", F + 0x8B, F + 0x92) and not readers(B, "rflags", F + 0x8B, F + 0x92) and
            not [a for a in after if B[a].mnemonic.startswith("j")])
    mk = list(img.cs.disasm(img.read(MARK, 16), MARK))
    R.check("the callee 0032ED70 (no .pdata, a 16-byte leaf) starts `movsxd rax, ecx` - it writes RAX from ECX "
            "without reading it - then `lea rcx, [022C6E48]`, `or qword ptr [rcx + rax*8], 1`, `ret`",
            img.pdata(MARK) is None and [c.mnemonic for c in mk[:4]] == ["movsxd", "lea", "or", "ret"] and
            mk[0].op_str == "rax, ecx" and mk[1].address + mk[1].size + mk[1].operands[1].mem.disp == FLAGQ and
            mk[2].op_str == "qword ptr [rcx + rax*8], 1")
    R.check("by contrast the other two returns are used: 0032F6E0's EAX is tested (+ 0x57) and 00309230's EAX is "
            "passed as EDX to 0032FC30 (+ 0x82 `mov edx, eax`, + 0x84 `mov ecx, ebx`)",
            T(B, F + 0x57) == "test eax, eax" and T(B, F + 0x7D) == "call 0x309230" and
            T(B, F + 0x82) == "mov edx, eax" and T(B, F + 0x84) == "mov ecx, ebx")
    # ---------------- the queue writer's narrowing (consistency with the sequence-queue review)
    QB = Body(img, Q, Q_END)
    R.check("queue writer 00306760 kind-4 arm (re-read): + 0x147 `sub edi, eax`; + 0x152 `movzx ecx, word ptr [rax + "
            "8]`; + 0x158 `div ecx`; + 0x162 `cmp ax, dx` (66 3B C2, low 16 bits); + 0x167 `movzx eax, ax`; + 0x16A "
            "`sub eax, 0xd0`; + 0x174 DWORD store to 022C2178 - the queue narrows its own quotient to 16 bits",
            T(QB, Q + 0x147) == "sub edi, eax" and T(QB, Q + 0x152) == "movzx ecx, word ptr [rax + 8]" and
            T(QB, Q + 0x158) == "div ecx" and QB[Q + 0x162].bytes == b"\x66\x3b\xc2" and
            T(QB, Q + 0x167) == "movzx eax, ax" and T(QB, Q + 0x16A) == "sub eax, 0xd0" and
            rip_target(QB[Q_STORE]) == QUEUE and QB[Q_STORE].mems[0]["size"] == 4)
    emu_checks(img, R, small)


def packet_bytes(img, R):
    ev = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(find_exe())))),
                      "FFXII TZA", "_experiments", "evidence", SLUG)
    s = json.load(open(os.path.join(ev, "source-01.json")))
    rg = [(int(r["start"], 16), int(r["end_exclusive"], 16), r["sha256"]) for r in s["ranges"]]
    insb = b"".join(bytes.fromhex(i["bytes"]) for i in s["ranges"][0]["instructions"])
    R.check("packet's new source range 00306C5B .. 00306CEC (145 B) hashes to this image's bytes, and its 37 "
            "instruction records concatenate to them",
            len(rg) == 1 and rg[0][:2] == (F + 0x8B, CODE_END) and CODE_END - (F + 0x8B) == 145 and
            hashlib.sha256(img.read(F + 0x8B, 145)).hexdigest() == rg[0][2] and insb == img.read(F + 0x8B, 145) and
            len(s["ranges"][0]["instructions"]) == 37)
    p = json.load(open(os.path.join(ev, "retained-prefix-01.json")))
    pr = [r for r in p["ranges"] if int(r["start"], 16) == F]
    R.check("packet's retained prefix 00306BD0 .. 00306C5B (139 B) hashes to this image's bytes",
            len(pr) == 1 and int(pr[0]["end_exclusive"], 16) == F + 0x8B and
            hashlib.sha256(img.read(F, 0x8B)).hexdigest() == pr[0]["sha256"])
    qs = json.load(open(os.path.join(ev, "retained", "queue-source-02.json")))
    qr = [r for r in qs["ranges"] if int(r["start"], 16) == Q]
    R.check("packet's retained queue range 00306760 .. + 0x38F hashes to this image's bytes",
            len(qr) == 1 and int(qr[0]["end_exclusive"], 16) == Q_END and
            hashlib.sha256(img.read(Q, Q_END - Q)).hexdigest() == qr[0]["sha256"])
    d = json.load(open(os.path.join(ev, "data-01.json")))
    R.check("packet's physical body (440 B), seven DWORDs and 128 selector bytes equal this image's (body sha256 "
            "%s...)" % d["physical_body_sha256"][:12],
            hashlib.sha256(img.read(F, END - F)).hexdigest() == d["physical_body_sha256"] and
            bytes.fromhex(d["physical_body_hex"]) == img.read(F, END - F) and
            bytes.fromhex(d["jump_hex"]) == img.read(DW, 28) and bytes.fromhex(d["mapping_hex"]) == img.read(SEL, 128)
            and d["mapping"] == list(img.read(SEL, 128)))
    x = json.load(open(os.path.join(ev, "extent-01.json")))
    ents, ok = img.pdata_cover(F, END)
    R.check("packet's extent-01 records equal the image's .pdata records",
            [(int(r["begin"], 16), int(r["end_exclusive"], 16)) for r in x["records"]] ==
            [(b, e) for b, e, fl, rr in ents] and x["bytes"] == 440)
    res = json.load(open(os.path.join(ev, "result-02.json")))
    tg, sel = table(img)
    R.check("result-02's seven arms (selector -> target -> kind) equal the reviewer's derivation",
            [(a["selector"], int(a["target"], 16), a["published_kind"]) for a in res["facts"]["arms"]] ==
            [(i, tg[i], k) for i, k in enumerate([5, 6, 3, 4, 1, 2, 7])])
    rd = open(os.path.join(ev, "README.md"), encoding="utf-8").read()
    R.check("packet README keeps open: natural caller consistency, the equalities for normal callers, and the list of "
            "things not established; it forbids a natural impossibility claim",
            "Natural caller consistency remains OPEN" in rd and "Neither equality is established for normal callers"
            in rd and "**Not established:**" in rd and "natural impossibility claim" in rd)
    # the method addendum: the 145-byte suffix was already retained
    ap = os.path.join(os.path.dirname(ev), "autoattack-commit-exception", "retained", "current-row-source-01.json")
    a = json.load(open(ap))
    ar = [r for r in a["ranges"] if int(r["start"], 16) <= F + 0x8B and int(r["end_exclusive"], 16) >= CODE_END]
    R.check("ASTRA's addendum (19e732aa6) holds: the 145-byte suffix 00306C5B .. 00306CEC is already a range of "
            "autoattack-commit-exception/retained/current-row-source-01.json with the same sha256",
            any(int(r["start"], 16) == F + 0x8B and int(r["end_exclusive"], 16) == CODE_END and
                r["sha256"] == rg[0][2] for r in ar))


def git(*args):
    top = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True,
                         cwd=os.path.dirname(os.path.abspath(__file__))).stdout.strip()
    return subprocess.run(["git"] + list(args), capture_output=True, cwd=top).stdout


def committed_manifest_sha():
    b = git("show", "%s:Database/FFXII TZA/_experiments/evidence/%s/manifest.json" % (PRODUCER, SLUG))
    return hashlib.sha256(b).hexdigest()


def lineage_check(R):
    b = git("show", "318e510c6692309620b468b4d6101582072d8019:Database/FFXII TZA/_experiments/evidence/"
            "ov42-special-action-preconditions/special-admission-raw-01.json")
    exe = find_exe()
    ev = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(exe)))),
                      "FFXII TZA", "_experiments", "evidence", SLUG)
    mine = open(os.path.join(ev, "retained-prefix-01.json"), "rb").read()
    R.check("retained-prefix-01.json is byte-identical to 318e510c's special-admission-raw-01.json (sha256 %s...)" %
            hashlib.sha256(b).hexdigest()[:16], b == mine and len(b) > 0)


def u32le(v):
    return struct.pack("<I", v & 0xFFFFFFFF)


CONTROLS = [
    ("guard narrowed to 16 bits: + 0xB4..+ 0xBC `add ax, 0xff6c` / `cmp ax, 0x7f` (66 prefixes), `ja` kept",
     GUARD_ADD, bytes.fromhex("66056cff6683f87f")),
    ("+ 0xBC `ja` -> `jg` (signed guard)", GUARD_JA, bytes([0x7F])),
    ("+ 0xB4 bias -0x94 -> -0x93 (`add eax, 0xffffff6d`)", GUARD_ADD + 1, bytes([0x6D])),
    ("kind-4 arm publishes 7 (+ 0xE7 `mov ebx, 4` -> `mov ebx, 7`)", F + 0xE8, bytes([0x07])),
    ("selector byte x = 60 (q 208) 03 -> 06", SEL + 60, bytes([0x06])),
    ("selector byte x = 59 (q 207) 02 -> 03", SEL + 59, bytes([0x03])),
    ("selector byte x = 100 -> 07 (outside the seven DWORDs)", SEL + 100, bytes([0x07])),
    ("DWORD for selector 3 -> the kind-7 arm (+ 0xFC)", DW + 12, u32le(F + 0xFC - 0x120000)),
    ("+ 0x10 `mov rsi, rdx` -> `mov rsi, rcx` (the owner as row)", F + 0x10, bytes.fromhex("488bf1")),
    ("+ 0xA1 `sub esi, eax` -> `sub esi, ecx`", F + 0xA1, bytes.fromhex("2bf1")),
    ("+ 0xAC divisor WORD -> BYTE (`movzx ecx, byte ptr [rax + 8]`)", F + 0xAD, bytes([0xB6])),
    ("+ 0xB2 `div ecx` -> `idiv ecx` (signed)", DIV, bytes.fromhex("f7f9")),
    ("+ 0xA5 second descriptor cell 02EBF138 -> 02EBF140", F + 0xA8, u32le(DESC + 8 - (F + 0xAC))),
    ("+ 0x10B kind store target 022C215C -> 022C2160", STORE + 2, u32le(KINDCELL + 4 - (STORE + 6))),
    ("+ 0x8B `mov ecx, ebx` -> `mov ecx, eax` (0032FC30's return used as 0032ED70's argument)", F + 0x8B,
     bytes.fromhex("8bc8")),
    ("+ 0x18 `je` + 0x35 -> `jne` (entry gate inverted)", F + 0x18, bytes([0x75])),
    ("queue + 0x167 `movzx eax, ax` -> `mov eax, eax` + NOP (no low16 narrowing in the queue)", Q + 0x167,
     bytes.fromhex("89c090")),
    ("queue + 0x16A `sub eax, 0xd0` -> `sub eax, 0xd1`", Q + 0x16B, bytes([0xD1])),
]


def main():
    img = Img.load()
    R = Rep("rv_kindrow")
    print("== packet integrity")
    csha = committed_manifest_sha()
    check_manifest(R, SLUG, csha)
    R.note("committed manifest at %s: sha256 %s" % (PRODUCER, csha))
    lineage_check(R)
    packet_bytes(img, R)
    census_checks(img, R)
    print("== shipping-image re-derivation")
    B = Body(img, F, CODE_END)
    m = derived_map(img, B)[0]
    R.note("q -> kind (from the bytes): " + "; ".join("%d..%d -> %s" % tuple(x) for x in ranges_of(m)) +
           "; all other q -> 7")
    checks(img, R)
    print("== controls (each patched private image must FAIL at least one check above)")
    Rn = Rep("null")
    Rn.quiet = True
    P0 = img.patched(F + 0x10, img.read(F + 0x10, 3))
    P0._private = True
    checks(P0, Rn, small=True)
    R.check("null control: an unchanged private copy passes every check", Rn.fails == 0 and Rn.n > 0,
            "%d of %d; %s" % (Rn.n - Rn.fails, Rn.n, Rn.failed[:2]))
    nctl = 0
    for label, va, nb in CONTROLS:
        Pimg = img.patched(va, nb)
        Pimg._private = True
        if Pimg.d == img.d:
            raise SystemExit("control %s did not change the image" % label)
        Rc = Rep(label)
        Rc.quiet = True
        try:
            checks(Pimg, Rc, small=True)
            failed = Rc.fails
            why = "%d failed: %s" % (failed, "; ".join(f[:60] for f in Rc.failed[:3]))
        except Exception as e:
            failed = 1
            why = "refused: %r after %d failed: %s" % (e, Rc.fails, "; ".join(f[:60] for f in Rc.failed[:3]))
        nctl += 1
        R.check("control: " + label, failed > 0, why)
    disk = hashlib.sha256(open(find_exe(), "rb").read()).hexdigest()
    R.check("exe on disk still hashes to the pinned sha256 after all controls", disk == SHA_PIN, disk)
    print("TOTAL: %d checks, %d PASS, %d FAIL (%d controls)" % (R.n, R.n - R.fails, R.fails, nctl))


if __name__ == "__main__":
    main()
