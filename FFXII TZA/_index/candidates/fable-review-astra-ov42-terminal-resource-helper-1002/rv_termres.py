"""rv_termres.py - FABLE independent re-derivation for ASTRA packet ov42-terminal-resource-helper (d66234298, OV-42).

Own reader (rvlib.py: struct + capstone 5, copied unchanged from the kind-row review, sha256 69f9bc40be32abcc...).
Does not import or run ASTRA's prove.py, prove-before-prerequisite-hardening.py, prove_owner_reload_order.py, run.py,
control.py, capture.py, capture_prerequisites.py, capture-index-path.py, prepare-extents.py, qualify-binding.py,
validate-title-source-annotations.py or the shared role adapter (reg_tracking.py).

Method:
  * image sha256; the helper 00305640 (one .pdata record, 393 B) decoded linearly and exactly; its first row
    quotient (two descriptor loads around one lookup, a 32-bit subtraction, an unsigned 32-bit `div`), the two
    cost callees' WORD inputs, the 16 + (R8D != 0) mode, the two stats-callee arguments, the gil request, the
    NULL tests, every own memory write, the row-type switch and the type-10 counter leg's recomputed quotient -
    all from register-write censuses on the local CFG and operand widths from the instruction bytes;
  * the terminal caller's call (00304850 + 0x6E8) and its two guards, re-read from the image;
  * a raw E8/E9 census of 00305640's direct callers and the R8D each passes;
  * the retained US action table (from the predecessor packet 103aa3123) for the row types the terminal call
    can meet under the equal-binding premise; the other shipped language tables when the game extract is present;
  * a concrete emulation (unicorn) of the ORIGINAL 00305640 from its entry: 0020E600, 00309110, 00308FF0,
    00300CE0, 00300BC0, 00253690, 00254EE0, 00316440 and 00253770 are stubbed by a code hook (each returns at once
    with a scripted RAX and clobbers RCX/RDX/R8-R11); sweeps of quotients, strides, modes, row types and units;
  * the producer-repair artifacts are inspected as recorded (exit codes, flags), not re-run;
  * controls patch a private in-memory copy of the image (or a private copy of the table); the exe on disk is
    never written and its sha256 is rechecked at the end.
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

C2 = 0x00305640
C2_END = C2 + 0x189            # 393 B
NEXT_ROOT = 0x003057D0
LOOKUP, COSTA, COSTB = 0x0020E600, 0x00309110, 0x00308FF0
STAT1, STAT2, GILGET, GILSET = 0x00300CE0, 0x00300BC0, 0x00253690, 0x00254EE0
PRE10, COUNTER = 0x00316440, 0x00253770
STUBS = [LOOKUP, COSTA, COSTB, STAT1, STAT2, GILGET, GILSET, PRE10, COUNTER]
F = 0x00304850                 # the terminal caller
CALLSITE = F + 0x6E8
DESC = 0x02EBF138
SLUG = "ov42-terminal-resource-helper"
PRODUCER = "d66234298945443e781991e1106faa82940ac005"
PRED = "103aa31230175dbfe50ed445e3a3d2b4861ded56"
STOCK = list(range(511, 535))
EXTRACT = r"D:\FFXII_TZA_extract\ps2data\image\ff12\test_battle"
LANGS = ["us", "ch", "cn", "de", "es", "fr", "in", "it", "kr"]


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


def T(Bd, a):
    I = Bd.ins.get(a)
    return I.text if I else "<no boundary>"


def writers(Bd, fam, lo=None, hi=None):
    return [a for a in Bd.order if fam in Bd[a].reg_writes and (lo is None or lo <= a) and (hi is None or a < hi)]


def readers(Bd, fam, lo=None, hi=None):
    return [a for a in Bd.order if fam in Bd[a].reg_reads and (lo is None or lo <= a) and (hi is None or a < hi)]


def rip_target(I):
    for m in I.mems:
        if m["base"] == "rip":
            return I.address + I.size + m["disp"]
    return None


def evdir(slug=SLUG):
    return os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(find_exe())))),
                        "FFXII TZA", "_experiments", "evidence", slug)


def load_table():
    return open(os.path.join(evdir("ov42-caller-row-preconditions"), "action_data_us.st2e"), "rb").read()


def trow(tb, i):
    n, st, off = struct.unpack_from("<IHxxI", tb, 4)
    return tb[off + st * i: off + st * (i + 1)]


def bit30(tb, i):
    return (struct.unpack_from("<I", trow(tb, i), 0xC)[0] >> 30) & 1


# ------------------------------------------------------------------ emulation of the original code
class Emu(object):
    STK, RET, UNIT, SCR, TBL, DSC = 0x7F000000, 0x7E000000, 0x41000000, 0x50000000, 0x30000000, 0x42000000
    REC = 0x50000800
    JUNK = 0xC1C1C1C1C1C1C1C1

    def __init__(self, img, code_ranges, stubs):
        from unicorn import Uc, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE, UC_HOOK_MEM_WRITE, UC_HOOK_INTR
        from unicorn import UC_HOOK_MEM_READ_UNMAPPED, UC_HOOK_MEM_FETCH_UNMAPPED, UC_HOOK_MEM_WRITE_UNMAPPED
        from unicorn import x86_const as X
        self.X = X
        mu = self.mu = Uc(UC_ARCH_X86, UC_MODE_64)
        pages = set()
        spans = list(code_ranges) + [(0x02EBF000, 0x02EC0000)]
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
        for a in (self.STK, self.UNIT, self.SCR, self.DSC):
            mu.mem_map(a, 0x10000)
        mu.mem_map(self.TBL, 0x40000)
        mu.mem_map(self.RET, 0x1000)
        self.code_ranges = list(code_ranges)
        self.stubs = set(stubs)
        self.stub_rax, self.stub_fx = {}, {}
        self.calls_n = {}
        self.trace, self.writes, self.intr, self.fault, self.left = [], [], None, None, None

        def ch(uc, addr, size, ud):
            if addr in self.stubs:
                rsp = uc.reg_read(X.UC_X86_REG_RSP)
                regs = tuple(uc.reg_read(getattr(X, "UC_X86_REG_" + r)) for r in ("RCX", "RDX", "R8", "R9"))
                self.trace.append((addr,) + regs)
                k = self.calls_n.get(addr, 0)
                self.calls_n[addr] = k + 1
                if addr in self.stub_fx:
                    self.stub_fx[addr](uc, regs, k)
                v = self.stub_rax.get(addr, 0)
                if callable(v):
                    v = v(regs, k)
                uc.reg_write(X.UC_X86_REG_RAX, v & 0xFFFFFFFFFFFFFFFF)
                for r in ("RCX", "RDX", "R8", "R9", "R10", "R11"):
                    uc.reg_write(getattr(X, "UC_X86_REG_" + r), self.JUNK)
                uc.reg_write(X.UC_X86_REG_RIP, struct.unpack("<Q", bytes(uc.mem_read(rsp, 8)))[0])
                uc.reg_write(X.UC_X86_REG_RSP, rsp + 8)
                return
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

    def w(self, a, b):
        self.mu.mem_write(a, b)

    def run(self, start, regs, count=20000):
        from unicorn import UcError
        X = self.X
        sp = self.STK + 0x8000
        self.mu.mem_write(sp, struct.pack("<Q", self.RET))
        self.mu.reg_write(X.UC_X86_REG_RSP, sp)
        base = {"rax": 0xAAAAAAAAAAAAAAAA, "rbx": 0xBBBBBBBBBBBBBBBB, "rdi": 0xDDDDDDDDDDDDDDDD,
                "rsi": 0x5151515151515151, "rbp": 0xB0B0B0B0B0B0B0B0, "r12": 0x1212121212121212,
                "r13": 0x1313131313131313, "r14": 0x1414141414141414, "r15": 0x1515151515151515,
                "rcx": 0, "rdx": 0, "r8": 0, "r9": 0}
        base.update(regs)
        for k, v in base.items():
            self.mu.reg_write(getattr(X, "UC_X86_REG_" + k.upper()), v)
        self.trace, self.writes, self.intr, self.fault, self.left = [], [], None, None, None
        self.calls_n = {}
        try:
            self.mu.emu_start(start, self.RET, count=count)
        except UcError as e:
            if self.intr is None and self.fault is None:
                self.fault = "UcError %s" % e
        r = dict((k, self.mu.reg_read(getattr(X, "UC_X86_REG_" + k.upper())))
                 for k in ("rax", "rbx", "rsi", "rdi", "rbp", "r12", "r13", "r14", "r15", "rip"))
        r["trace"], r["intr"], r["fault"], r["left"] = list(self.trace), self.intr, self.fault, self.left
        r["writes"] = list(self.writes)
        r["ok"] = (r["rip"] == self.RET and not r["fault"] and not r["intr"] and not r["left"])
        return r


def helper_emu(img):
    return Emu(img, [(C2, C2_END)], STUBS)


def setup(E, stride=60, key=0x20, rec=True, b5=0, w28=0xFFFE, e54=30, typ=10, row=None, table=None):
    """Unit at UNIT (+0x698 -> record), descriptor at DSC (+8 stride, +0xC key), lookup bound to TBL + key."""
    E.w(E.UNIT, b"\0" * 0x10000)
    E.w(E.SCR, b"\0" * 0x10000)
    E.w(E.DSC, b"\0" * 0x10000)
    E.w(E.TBL, b"\0" * 0x40000)
    if table is not None:
        E.w(E.TBL, table)
    E.w(E.UNIT + 0x698, struct.pack("<Q", E.REC if rec else 0))
    E.w(E.UNIT + 0xE54, struct.pack("<I", e54 & 0xFFFFFFFF))
    E.w(E.UNIT + 0xE58, struct.pack("<I", 0x5A5A5A5A))
    E.w(E.UNIT + 0xDC8, struct.pack("<H", 0x1234))
    E.w(E.REC + 5, bytes([b5]))
    E.w(E.REC + 0x28, struct.pack("<H", w28))
    E.w(E.DSC + 8, struct.pack("<H", stride))
    E.w(E.DSC + 0xC, struct.pack("<I", key))
    E.w(DESC, struct.pack("<Q", E.DSC))
    if row is not None and typ is not None:
        E.w(row + 0x1E, bytes([typ]))


def lookup_bound(hi=0, base=None):
    return lambda regs, k: (hi << 32) | ((Emu.TBL + (regs[0] & 0xFFFFFFFF)) if base is None else base)


def call(E, row, r8=1, unit=None, rax=None, fx=None):
    E.stub_rax = {LOOKUP: lookup_bound(0), COSTA: 7, COSTB: 3, GILGET: 100}
    E.stub_rax.update(rax or {})
    E.stub_fx = fx or {}
    return E.run(C2, {"rcx": Emu.UNIT if unit is None else unit, "rdx": row, "r8": r8})


def calls_of(r):
    return [t[0] for t in r["trace"]]


def args_of(r, a):
    return [t[1:] for t in r["trace"] if t[0] == a]


def first_args(r, a):
    """First call's (RCX, RDX, R8, R9), or Nones when the callee was not called."""
    return (args_of(r, a) + [(None, None, None, None)])[0]


def emu_checks(img, R, tb, small=False):
    E = helper_emu(img)
    U = Emu.UNIT
    # ---- the 65744 discriminator: stride 1, row = base + 65744
    row = Emu.TBL + 0x20 + 65744
    setup(E, stride=1, row=row)
    r = call(E, row)
    R.check("emulated 00305640 (stride 1, row = lookup + 65744, row type 10, record byte +5 = 0, R8D = 1): 00309110 and "
            "00308FF0 get EDX = 208 (the quotient's low 16 bits) with RCX = unit; 00253770 gets ECX = 13 and EDX = 65744 "
            "(the recomputed full quotient); calls in order 0020E600, 00309110, 00308FF0, 00300CE0, 00300BC0, "
            "00253690, 00254EE0, 00316440, 0020E600, 00253770",
            r["ok"] and calls_of(r) == [LOOKUP, COSTA, COSTB, STAT1, STAT2, GILGET, GILSET, PRE10, LOOKUP, COUNTER] and
            args_of(r, COSTA)[0][:2] == (U, 208) and args_of(r, COSTB)[0][:2] == (U, 208) and
            args_of(r, COUNTER)[0][0] & 0xFFFFFFFF == 13 and args_of(r, COUNTER)[0][1] == 65744,
            "calls %s costA %s counter %s" % (["%X" % c for c in calls_of(r)], args_of(r, COSTA)[:1],
                                              args_of(r, COUNTER)[:1]))
    rnd = random.Random(11)
    bad = []
    for _ in range(20 if small else 200):
        s = rnd.choice([1, 2, 60, 0x80, 0x1234, 0xFFFF, rnd.randrange(1, 0x10000)])
        rem = rnd.randrange(s)
        q = rnd.randrange(0, (0xFFFFFFFF - rem) // s + 1)
        rw = Emu.TBL + 0x100
        bl = (rw - s * q - rem) & 0xFFFFFFFF
        hi = rnd.getrandbits(32)
        setup(E, stride=s, row=rw)
        E.stub_rax = {LOOKUP: (lambda regs, k, bl=bl, hi=hi: (hi << 32) | bl), COSTA: 7, COSTB: 3, GILGET: 100}
        E.stub_fx = {}
        rr = E.run(C2, {"rcx": U, "rdx": rw, "r8": 1})
        ca, cb, cn = args_of(rr, COSTA), args_of(rr, COSTB), args_of(rr, COUNTER)
        if not (rr["ok"] and ca and ca[0][1] == q & 0xFFFF and cb[0][1] == q & 0xFFFF and cn and cn[0][1] == q):
            bad.append("s %X q %X: %s %s" % (s, q, ca[:1], cn[:1]))
    R.check("emulated %d random strides / quotients / lookup upper halves (type 10, stable descriptor): the cost callees "
            "get q mod 65536 and the counter gets q, q = ((low32(row) - low32(lookup)) mod 2^32) / u16 stride"
            % (20 if small else 200), not bad, "; ".join(bad[:2]))
    # ---- the mode
    outs = []
    for r8, want in ((0, 16), (1, 17), (2, 17), (0x80000000, 17), (0xFFFFFFFF, 17), (0x100000000, 16)):
        setup(E, row=Emu.TBL + 0x20 + 60 * 511)
        rr = call(E, Emu.TBL + 0x20 + 60 * 511, r8=r8)
        got = (args_of(rr, STAT1)[0][2] & 0xFFFFFFFF, args_of(rr, STAT2)[0][2] & 0xFFFFFFFF) if rr["ok"] else None
        outs.append((r8, want, got))
    R.check("emulated mode: entry R8 = 0, 1, 2, 0x80000000, FFFFFFFF and 2^32 give R8D = 16, 17, 17, 17, 17, 16 at both "
            "00300CE0 and 00300BC0 (only the low 32 bits are tested; the raw value is not forwarded)",
            all(g == (w_, w_) for r8, w_, g in outs), str([(hex(a), b, c) for a, b, c in outs]))
    # ---- the stats arguments
    res = []
    for w28, cb, cost_a in ((0xFFFE, 3, 7), (0x8000, 3, 7), (0x0005, 0xFFFFFFFF, 0x80000000)):
        setup(E, w28=w28, row=Emu.TBL + 0x20 + 60 * 511)
        rr = call(E, Emu.TBL + 0x20 + 60 * 511, rax={COSTA: cost_a, COSTB: cb})
        a1, a2 = args_of(rr, STAT1)[0], args_of(rr, STAT2)[0]
        sw = w28 - 0x10000 if w28 & 0x8000 else w28
        res.append(rr["ok"] and a1[0] == Emu.REC and a1[1] & 0xFFFFFFFF == (-cost_a) & 0xFFFFFFFF and
                   a2[0] == Emu.REC and a2[1] & 0xFFFFFFFF == (-(sw * cb)) & 0xFFFFFFFF)
    R.check("emulated stats arguments: 00300CE0 gets RCX = the unit's record (+0x698) and EDX = -(00309110's EAX); "
            "00300BC0 gets the record again and EDX = -(sign-extended WORD record+0x28 * 00308FF0's EAX), 32-bit "
            "(cases -2*3, -32768*3, 5*FFFFFFFF)", all(res), str(res))
    # ---- the gil request
    res = []
    for g, c, want in ((100, 30, 70), (30, 100, 0), (0x7FFFFFFF, 0xFFFFFFFF, 0), (5, 5, 0), (0x80000005, 10, 0x7FFFFFFB),
                       (0x70000000, 0x10, 0x6FFFFFF0)):
        setup(E, e54=c, row=Emu.TBL + 0x20 + 60 * 511)
        rr = call(E, Emu.TBL + 0x20 + 60 * 511, rax={GILGET: g})
        res.append((g, c, want, args_of(rr, GILSET)[0][0] & 0xFFFFFFFF if rr["ok"] else None))
    R.check("emulated gil request: 00254EE0 gets ECX = low32(00253690's EAX - unit DWORD +0xE54) when that is signed "
            "non-negative, else 0 (32-bit wraps: 7FFFFFFF - (-1) gives 0, 80000005 - 10 gives 7FFFFFFB)",
            all(a[2] == a[3] for a in res), str([tuple(hex(x) if x is not None else None for x in a) for a in res]))
    # ---- own writes and the NULL tests
    rowp = Emu.TBL + 0x20 + 60 * 511
    setup(E, b5=0, row=rowp)
    r0 = call(E, rowp)
    setup(E, b5=1, row=rowp)
    r1 = call(E, rowp)
    w0 = [(w[0] - C2, w[1], w[2], w[3]) for w in r0["writes"]]
    R.check("emulated own writes: with record byte +5 = 0 the helper writes exactly DWORD unit+0xE58 := 0 (+ 0x73) and "
            "WORD unit+0xDC8 := FFFF (+ 0x7A) outside its stack; with byte +5 = 1 it writes nothing and makes no "
            "00253770 call",
            r0["ok"] and w0 == [(0x73, U + 0xE58, 4, 0), (0x7A, U + 0xDC8, 2, 0xFFFF)] and r1["ok"] and not r1["writes"]
            and COUNTER not in calls_of(r1), "writes %s" % [(hex(a), hex(b), c, hex(d)) for a, b, c, d in w0])
    setup(E, row=rowp)
    rn = call(E, rowp, unit=0)
    setup(E, rec=False, row=rowp)
    rr_ = call(E, rowp)
    R.check("emulated NULL cases: a NULL unit skips the reset, calls 00309110 and 00308FF0, then reads address 0x698 (no "
            "further test); a NULL record reads address 0x28 after 00300CE0 (source predictions, not observed faults)",
            rn["fault"] == 0x698 and calls_of(rn) == [LOOKUP, COSTA, COSTB] and not rn["writes"] and
            rr_["fault"] == 0x28 and calls_of(rr_) == [LOOKUP, COSTA, COSTB, STAT1] and not rr_["writes"],
            "unit: fault %s calls %s; record: fault %s calls %s" % (rn["fault"], ["%X" % c for c in calls_of(rn)],
                                                                    rr_["fault"], ["%X" % c for c in calls_of(rr_)]))
    # ---- the type switch
    got = {}
    for typ in (0, 1, 2, 3, 7, 9, 10, 255):
        setup(E, typ=typ, row=rowp)
        rr = call(E, rowp)
        cn = args_of(rr, COUNTER)
        got[typ] = (cn[0][0] & 0xFFFFFFFF, cn[0][1] & 0xFFFFFFFF) if cn else None
        if not rr["ok"]:
            got[typ] = "fault"
    R.check("emulated row-type switch (row +0x1E, q = 511): 0 -> 00253770(0, 1), 1 -> (1, 1), 2 -> (2, 1), 10 -> (13, "
            "511) after 00316440; 3, 7, 9 and 255 make no 00253770 call",
            got == {0: (0, 1), 1: (1, 1), 2: (2, 1), 3: None, 7: None, 9: None, 10: (13, 511), 255: None}, str(got))
    # ---- independent reads: the descriptor repointed during 00316440
    setup(E, row=rowp)
    E.w(E.DSC + 0x108, struct.pack("<H", 30))
    E.w(E.DSC + 0x10C, struct.pack("<I", 0x20))
    rr = call(E, rowp, fx={PRE10: lambda uc, regs, k: uc.mem_write(DESC, struct.pack("<Q", Emu.DSC + 0x100))})
    R.check("emulated: when 02EBF138 is repointed during 00316440 to a descriptor with stride 30, the cost callees got "
            "511 and the counter gets 1022 - the counter leg rereads the descriptor and calls the lookup again",
            rr["ok"] and first_args(rr, COSTA)[1] == 511 and first_args(rr, COUNTER)[1] == 1022,
            "%s %s" % (args_of(rr, COSTA)[:1], args_of(rr, COUNTER)[:1]))
    setup(E, row=rowp)
    E.w(E.DSC + 0x108, struct.pack("<H", 30))
    E.w(E.DSC + 0x10C, struct.pack("<I", 0x20))
    rr = call(E, rowp, fx={LOOKUP: lambda uc, regs, k: uc.mem_write(DESC, struct.pack("<Q", Emu.DSC + 0x100))
                           if k == 0 else None})
    R.check("emulated: when 02EBF138 is repointed during the first lookup, the first quotient divides by the second "
            "descriptor's stride (511 * 60 / 30 = 1022 -> cost input 1022): the key and the divisor come from two loads",
            rr["ok"] and first_args(rr, COSTA)[1] == 1022, str(args_of(rr, COSTA)[:1]))
    # ---- the US table: which row types the terminal call can meet under the equal-binding premise
    met, bad = {}, []
    for W in (range(0, 543) if not small else list(range(500, 543)) + [10, 100, 300]):
        if 0xD0 <= W <= 0xF1 or not bit30(tb, W):
            continue
        rw = Emu.TBL + 0x20 + 60 * W
        setup(E, row=None, table=tb)
        rr = call(E, rw)
        cn = args_of(rr, COUNTER)
        k = (cn[0][0] & 0xFFFFFFFF) if cn else None
        met.setdefault(k, []).append(W)
        if not rr["ok"] or (cn and cn[0][0] & 0xFFFFFFFF == 13) or args_of(rr, COSTA)[0][1] != W:
            bad.append(W)
    import collections
    R.note("US table, bit-30 rows outside D0..F1 run through 00305640 (row = lookup + 60 W): 00253770 ECX -> ids: " +
           "; ".join("%s: %d ids" % (k, len(v)) for k, v in sorted(met.items(), key=lambda x: str(x[0]))) +
           "; their row types: %s; ids %s" % (dict(sorted(collections.Counter(trow(tb, w_)[0x1E] for v in met.values()
                                                                          for w_ in v).items())),
                                             sorted(w_ for v in met.values() for w_ in v)))
    R.check("emulated with the retained US table: for every bit-30 row outside D0..F1 (the terminal call's condition, "
            "row = lookup + 60 W) the cost callees get W and 00253770 is not called at all (those rows have types 5, 7, 9 "
            "and 255); rows 511..534 among them",
            not bad and set(met) == {None} and all(w_ in met[None] for w_ in STOCK) and
            (small or len(met[None]) == 53),
            "bad %s" % bad[:5])


def checks(img, R, small=False):
    tb = R.table
    R.check("image sha256 = %s..." % SHA_PIN[:20], hashlib.sha256(img.d).hexdigest() == SHA_PIN or
            getattr(img, "_private", False))
    ents, ok = img.pdata_cover(C2, C2_END)
    R.check("00305640: one .pdata record 00305640 .. + 0x189 (393 B), int3 padding to the next root 003057D0",
            ok and len(ents) == 1 and img.read(C2_END, NEXT_ROOT - C2_END) == b"\xcc" * (NEXT_ROOT - C2_END) and
            img.pdata(NEXT_ROOT) is not None and img.pdata(NEXT_ROOT)[0] == NEXT_ROOT)
    Bd = Body(img, C2, C2_END)
    rets, tails, outs = Bd.exits()
    R.check("the body decodes exactly; one `ret` (+ 0x188, the last instruction); no tail jump, indirect branch or "
            "branch out", Bd.exact and rets == [C2 + 0x188] and Bd.order[-1] == C2 + 0x188 and not tails and not outs)
    R.check("entry carriers: + 0x25 RBP = RCX (unit), + 0x28 R12D = R8D, + 0x2B R14 = RDX (row); each written nowhere "
            "else except R14's counter-leg `sub` (+ 0x130) and the restores",
            T(Bd, C2 + 0x25) == "mov rbp, rcx" and T(Bd, C2 + 0x28) == "mov r12d, r8d" and
            T(Bd, C2 + 0x2B) == "mov r14, rdx" and writers(Bd, "rbp") == [C2 + 0x25, C2 + 0x16F] and
            writers(Bd, "r12") == [C2 + 0x28, C2 + 0x186] and writers(Bd, "r14") == [C2 + 0x2B, C2 + 0x130, C2 + 0x184],
            "rbp %s r12 %s r14 %s" % tuple(["+%X" % (a - C2) for a in writers(Bd, x)] for x in ("rbp", "r12", "r14")))
    R.check("first quotient: + 0x1E RAX = QWORD [02EBF138] and + 0x2E ECX = DWORD [rax + 0xc] with no test between (no "
            "null guard); + 0x31 `call 0020E600`; + 0x36 R9 = QWORD [02EBF138] again; + 0x3F/+ 0x45 `sub r11d, eax` "
            "(32-bit, from R14D); + 0x4B `movzx r10d, word ptr [r9 + 8]` (2 B); + 0x50 `div r10d` (unsigned 32-bit, EDX "
            "zeroed at + 0x3D, no zero test); + 0x53 EDI = EAX",
            rip_target(Bd[C2 + 0x1E]) == DESC and Bd[C2 + 0x1E].mems[0]["size"] == 8 and
            T(Bd, C2 + 0x2E) == "mov ecx, dword ptr [rax + 0xc]" and
            not [a for a in Bd.order if C2 + 0x1E < a < C2 + 0x50 and (Bd[a].mnemonic in ("cmp", "test") or
                                                                      Bd[a].mnemonic.startswith("j"))] and
            T(Bd, C2 + 0x31) == "call 0x20e600" and rip_target(Bd[C2 + 0x36]) == DESC and
            T(Bd, C2 + 0x3D) == "xor edx, edx" and T(Bd, C2 + 0x3F) == "mov r11d, r14d" and
            T(Bd, C2 + 0x45) == "sub r11d, eax" and T(Bd, C2 + 0x48) == "mov eax, r11d" and
            T(Bd, C2 + 0x4B) == "movzx r10d, word ptr [r9 + 8]" and Bd[C2 + 0x4B].mems[0]["size"] == 2 and
            T(Bd, C2 + 0x50) == "div r10d" and Bd[C2 + 0x50].bytes == bytes.fromhex("41f7f2") and
            T(Bd, C2 + 0x53) == "mov edi, eax" and writers(Bd, "rdx", C2 + 0x3E, C2 + 0x50) == [])
    R.check("cost inputs: + 0x81 and + 0x8C `movzx edx, di` (the quotient's low 16 bits) with RCX = RBP, before "
            "`call 00309110` (+ 0x87) and `call 00308FF0` (+ 0x94); EDI is not written between + 0x53 and + 0x8C; "
            "EBX = 00309110's EAX (+ 0x92), EDI = 00308FF0's EAX (+ 0xA6); both null-test outcomes reach + 0x81",
            T(Bd, C2 + 0x81) == "movzx edx, di" and T(Bd, C2 + 0x8C) == "movzx edx, di" and
            T(Bd, C2 + 0x84) == "mov rcx, rbp" and T(Bd, C2 + 0x8F) == "mov rcx, rbp" and
            T(Bd, C2 + 0x87) == "call 0x309110" and T(Bd, C2 + 0x94) == "call 0x308ff0" and
            writers(Bd, "rdi", C2 + 0x54, C2 + 0x8D) == [] and T(Bd, C2 + 0x92) == "mov ebx, eax" and
            T(Bd, C2 + 0xA6) == "mov edi, eax" and Bd[C2 + 0x58].direct_target() == C2 + 0x81 and
            Bd[C2 + 0x64].direct_target() == C2 + 0x81 and Bd[C2 + 0x6C].direct_target() == C2 + 0x81)
    R.check("the mode: R15D = 0 (+ 0x42) until the `cmovns` (+ 0xE4); + 0xA0 ESI = R15D (0); + 0xA3 `test r12d, r12d`; "
            "+ 0xA6 `mov edi, eax` (no flags); + 0xA8 `setne sil`; + 0xB0 and + 0xC0 `lea r8d, [rsi + 0x10]`, ESI not "
            "written between - 16 + (low32(R8) != 0) to both stats callees",
            T(Bd, C2 + 0x42) == "xor r15d, r15d" and writers(Bd, "r15") == [C2 + 0x42, C2 + 0xE4, C2 + 0x182] and
            T(Bd, C2 + 0xA0) == "mov esi, r15d" and T(Bd, C2 + 0xA3) == "test r12d, r12d" and
            T(Bd, C2 + 0xA8) == "setne sil" and T(Bd, C2 + 0xB0) == "lea r8d, [rsi + 0x10]" and
            T(Bd, C2 + 0xC0) == "lea r8d, [rsi + 0x10]" and writers(Bd, "rsi", C2 + 0xA9, C2 + 0xC1) == [] and
            "rflags" not in Bd[C2 + 0xA6].reg_writes)
    R.check("stats arguments: + 0x99 RCX = QWORD [rbp + 0x698], + 0xAC `neg ebx`, + 0xAE EDX = EBX, + 0xB4 `call "
            "00300CE0`; + 0xB9 RCX = QWORD [rbp + 0x698] again, + 0xC4 `movsx edx, word ptr [rcx + 0x28]` (2 B, signed), "
            "+ 0xC8 `imul edx, edi`, + 0xCB `neg edx`, + 0xCD `call 00300BC0`",
            T(Bd, C2 + 0x99) == "mov rcx, qword ptr [rbp + 0x698]" and T(Bd, C2 + 0xAC) == "neg ebx" and
            T(Bd, C2 + 0xAE) == "mov edx, ebx" and T(Bd, C2 + 0xB4) == "call 0x300ce0" and
            T(Bd, C2 + 0xB9) == "mov rcx, qword ptr [rbp + 0x698]" and
            T(Bd, C2 + 0xC4) == "movsx edx, word ptr [rcx + 0x28]" and Bd[C2 + 0xC4].mems[0]["size"] == 2 and
            T(Bd, C2 + 0xC8) == "imul edx, edi" and T(Bd, C2 + 0xCB) == "neg edx" and T(Bd, C2 + 0xCD) == "call 0x300bc0")
    R.check("gil: + 0xD2 EBX = DWORD [rbp + 0xe54], `neg`, + 0xDA `call 00253690`, + 0xDF `lea edx, [rax + rbx]` "
            "(32-bit), + 0xE2 `test edx, edx`, + 0xE4 `cmovns r15d, edx`, + 0xE8 ECX = R15D, + 0xEB `call 00254EE0`",
            T(Bd, C2 + 0xD2) == "mov ebx, dword ptr [rbp + 0xe54]" and T(Bd, C2 + 0xD8) == "neg ebx" and
            T(Bd, C2 + 0xDA) == "call 0x253690" and T(Bd, C2 + 0xDF) == "lea edx, [rax + rbx]" and
            T(Bd, C2 + 0xE2) == "test edx, edx" and T(Bd, C2 + 0xE4) == "cmovns r15d, edx" and
            T(Bd, C2 + 0xE8) == "mov ecx, r15d" and T(Bd, C2 + 0xEB) == "call 0x254ee0")
    tests_rbp = [a for a in Bd.order if Bd[a].mnemonic == "test" and "rbp" in Bd[a].reg_reads]
    R.check("NULL: the only test of RBP is + 0x55 (`je` + 0x81), which skips only the reset; every path from the entry "
            "to the ret passes + 0x99, which reads [rbp + 0x698] with no test; the record is not null-tested before "
            "+ 0xC4 reads its WORD +0x28",
            tests_rbp == [C2 + 0x55] and Bd.dominates(C2 + 0x99, C2 + 0x188) and
            not [a for a in Bd.order if C2 + 0x99 < a < C2 + 0xC4 and Bd[a].mnemonic in ("test", "cmp") and
                 "rcx" in Bd[a].reg_reads])
    ow = [(a, m) for a, m in Bd.mem_writes() if m["base"] != "rsp"]
    R.check("own non-stack writes: exactly + 0x73 DWORD [rbp + 0xe58] := R15D (0) and + 0x7A WORD [rbp + 0xdc8] := AX "
            "(FFFF, + 0x6E), both behind the unit, record and record-byte +5 = 0 tests (+ 0x58, + 0x64, + 0x6C)",
            [(a, m["disp"], m["size"]) for a, m in ow] == [(C2 + 0x73, 0xE58, 4), (C2 + 0x7A, 0xDC8, 2)] and
            T(Bd, C2 + 0x6E) == "mov eax, 0xffff" and writers(Bd, "r15", C2 + 0x43, C2 + 0x73) == [] and
            C2 + 0x73 not in Bd.reach(C2, avoid=[C2 + 0x6E]),
            str([("+%X" % (a - C2), hex(m["disp"]), m["size"]) for a, m in ow]))
    R.check("the type switch: + 0xF0 record reload, null -> ret, + 0xFC byte +5 nonzero -> ret; + 0x104 `movzx ecx, "
            "byte ptr [r14 + 0x1e]` (the row at the entry RDX); 0 -> + 0x15E, 1 -> + 0x155, 2 -> + 0x14E, `cmp ecx, 8` "
            "after two subtractions (type 10) -> + 0x11C, anything else -> ret",
            T(Bd, C2 + 0xF0) == "mov rax, qword ptr [rbp + 0x698]" and Bd[C2 + 0xFA].direct_target() == C2 + 0x16A and
            Bd[C2 + 0x102].direct_target() == C2 + 0x16A and T(Bd, C2 + 0x104) == "movzx ecx, byte ptr [r14 + 0x1e]" and
            Bd[C2 + 0x10B].direct_target() == C2 + 0x15E and Bd[C2 + 0x110].direct_target() == C2 + 0x155 and
            Bd[C2 + 0x115].direct_target() == C2 + 0x14E and T(Bd, C2 + 0x117) == "cmp ecx, 8" and
            Bd[C2 + 0x11A].direct_target() == C2 + 0x16A)
    R.check("the type-10 counter leg: + 0x11C `call 00316440`; + 0x121 QWORD [02EBF138], + 0x128 key, + 0x12B `call "
            "0020E600`, + 0x130 `sub r14d, eax` (32-bit); + 0x135 QWORD [02EBF138] again, + 0x13C `movzx ecx, word ptr "
            "[rax + 8]`, + 0x140 EAX = R14D, + 0x143 `div ecx` (unsigned 32-bit); + 0x145 ECX = 13, + 0x14A `mov edx, "
            "eax` (no 16-bit narrowing), + 0x165 `call 00253770`",
            T(Bd, C2 + 0x11C) == "call 0x316440" and rip_target(Bd[C2 + 0x121]) == DESC and
            T(Bd, C2 + 0x128) == "mov ecx, dword ptr [rax + 0xc]" and T(Bd, C2 + 0x12B) == "call 0x20e600" and
            T(Bd, C2 + 0x130) == "sub r14d, eax" and rip_target(Bd[C2 + 0x135]) == DESC and
            T(Bd, C2 + 0x13C) == "movzx ecx, word ptr [rax + 8]" and T(Bd, C2 + 0x140) == "mov eax, r14d" and
            T(Bd, C2 + 0x143) == "div ecx" and Bd[C2 + 0x143].bytes == b"\xf7\xf1" and
            T(Bd, C2 + 0x145) == "mov ecx, 0xd" and T(Bd, C2 + 0x14A) == "mov edx, eax" and
            Bd[C2 + 0x14A].bytes == b"\x8b\xd0" and T(Bd, C2 + 0x165) == "call 0x253770")
    calls = [(a, t) for a, t in Bd.calls()]
    R.check("the helper's calls are exactly ten direct calls (0020E600 twice, 00309110, 00308FF0, 00300CE0, 00300BC0, "
            "00253690, 00254EE0, 00316440, 00253770), none indirect",
            [t for a, t in calls] == [LOOKUP, COSTA, COSTB, STAT1, STAT2, GILGET, GILSET, PRE10, LOOKUP, COUNTER])
    # ---- the terminal caller's call
    Cb = Body(img, F, F + 0x7F2)
    R.check("the terminal call 00304850 + 0x6E8: + 0x6DC `mov r8d, 1`, + 0x6E2 `mov rdx, r15`, + 0x6E5 `mov rcx, rdi`; "
            "reached only past + 0x6BE (entry word minus 0xD0 above 0x21, i.e. outside D0..F1) and the row bit-30 test "
            "+ 0x6D2, after 00303830 (+ 0x6CD); the sequence call + 0x6FD follows only after a second bit-30 test (+ 0x6ED)",
            T(Cb, F + 0x6DC) == "mov r8d, 1" and T(Cb, F + 0x6E2) == "mov rdx, r15" and
            T(Cb, F + 0x6E5) == "mov rcx, rdi" and T(Cb, CALLSITE) == "call 0x305640" and
            Cb[F + 0x6BE].direct_target() == F + 0x6ED and T(Cb, F + 0x6D2) == "test dword ptr [r15 + 0xc], 0x40000000"
            and Cb[F + 0x6DA].direct_target() == F + 0x704 and T(Cb, F + 0x6CD) == "call 0x303830" and
            T(Cb, F + 0x6ED) == "test dword ptr [r15 + 0xc], 0x40000000" and T(Cb, F + 0x6FD) == "call 0x306760" and
            CALLSITE in Cb.reach(F + 0x663) and CALLSITE not in Cb.reach(F + 0x663, avoid=[F + 0x6BE]) and
            CALLSITE not in Cb.reach(F + 0x663, avoid=[F + 0x6DA]) and T(Cb, F + 0x8E) == "cmp r13w, bx")
    pv = Body(img, 0x00303830, 0x00303981)
    R.check("the preview call that precedes this one (00304850 + 0x6CD -> 00303830) stores a DWORD to [r14 + 0xe54] at "
            "00303830 + 0x124, inside 00303830's .pdata chain (the field map's 'preview gil amount'; R14 = the unit is "
            "not re-derived here)",
            pv.exact and T(pv, 0x00303954) == "mov dword ptr [r14 + 0xe54], eax" and root_of(img, 0x00303954) == 0x00303830)
    # ---- the table
    t10 = [i for i in range(543) if trow(tb, i)[0x1E] == 10]
    R.check("the retained US table: the type-10 rows are 226..241, all inside D0..F1 (208..241); rows 511..534 have "
            "type 7", t10 == list(range(226, 242)) and all(trow(tb, i)[0x1E] == 7 for i in STOCK), str(t10))
    emu_checks(img, R, tb, small)


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


def root_of(img, va):
    po = img.off(img.base + img.exc_rva)
    for i in range(img.exc_size // 12):
        b, e, u = struct.unpack_from("<III", img.d, po + i * 12)
        if b + img.base <= va < e + img.base:
            for _ in range(16):
                ui = img.off(img.base + u)
                if not ((img.d[ui] >> 3) & 4):
                    return b + img.base
                n = img.d[ui + 2]
                co = ui + 4 + ((n + 1) & ~1) * 2
                b, e, u = struct.unpack_from("<III", img.d, co)
            return None
    return None


def r8_before(img, site):
    """Decode the .pdata record holding the call and return the last instruction before it that writes R8."""
    b, e = img.pdata(site)
    ins = [c for c in img.cs.disasm(img.read(b, e - b), b)]
    idx = [i for i, c in enumerate(ins) if c.address == site][0]
    for c in reversed(ins[max(0, idx - 6):idx]):
        txt = c.mnemonic + " " + c.op_str
        if c.op_str.startswith("r8d,") or c.op_str.startswith("r8,") or c.op_str.startswith("r8b,"):
            return txt
    return None


def census_checks(img, R):
    print("== raw direct-reference census (E8/E9 rel32 and 0F 8x jcc, .text)")
    rc = raw_refs(img, [C2])
    rows = [(a, k, root_of(img, a), r8_before(img, a)) for a, k in rc[C2]]
    for a, k, rt, r8 in rows:
        R.note("00305640 raw direct reference %X %s (root %X, + 0x%X): R8 set by `%s`" % (a, k, rt, a - rt, r8))
    R.check("00305640 has four raw direct callers: the terminal call (00304850 + 0x6E8, `mov r8d, 1`), two more with "
            "`mov r8d, 1` and one with `xor r8d, r8d` (mode 16)",
            len(rows) == 4 and (CALLSITE, "call", F, "mov r8d, 1") in rows and
            sorted(r[3] for r in rows) == ["mov r8d, 1", "mov r8d, 1", "mov r8d, 1", "xor r8d, r8d"])


def git(*args):
    top = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True,
                         cwd=os.path.dirname(os.path.abspath(__file__))).stdout.strip()
    return subprocess.run(["git"] + list(args), capture_output=True, cwd=top).stdout


def git_member(commit, member):
    out = git("ls-tree", "-z", commit, "--", member)
    if not out:
        return None
    oid = out.split(b"\t")[0].split()[2].decode()
    return git("cat-file", "blob", oid)


def packet_bytes(img, R):
    ev = evdir()
    P = "Database/FFXII TZA/_experiments/evidence/"
    cm = git_member(PRODUCER, P + SLUG + "/manifest.json")
    check_manifest(R, SLUG, hashlib.sha256(cm).hexdigest())
    R.note("committed manifest at d66234298: sha256 %s" % hashlib.sha256(cm).hexdigest())
    s = json.load(open(os.path.join(ev, "source-01.json")))
    bad, tot = [], 0
    for rg in s["ranges"]:
        a, e = int(rg["start"], 16), int(rg["end_exclusive"], 16)
        tot += 1
        ib = b"".join(bytes.fromhex(i["bytes"]) for i in rg["instructions"])
        if hashlib.sha256(img.read(a, e - a)).hexdigest() != rg["sha256"] or ib != img.read(a, e - a):
            bad.append("%X" % a)
    R.check("source-01's range(s) (%d) hash to this image's bytes, instruction records concatenate, and cover 00305640 "
            ".. + 0x189" % tot, not bad and [(int(r["start"], 16), int(r["end_exclusive"], 16)) for r in s["ranges"]]
            == [(C2, C2_END)], str(bad))
    pred = git_member(PRED, P + "ov42-caller-row-preconditions/current-row-source-01.json")
    R.check("caller-source-01.json is byte-identical to 103aa3123's current-row-source-01.json (git ls-tree + cat-file)",
            pred is not None and pred == open(os.path.join(ev, "caller-source-01.json"), "rb").read())
    x = json.load(open(os.path.join(ev, "extents-01.json")))
    okx = x["complete"]
    for b in x["bodies"]:
        e0 = int(b["entry"], 16)
        ents, ok = img.pdata_cover(e0, int(b["end_exclusive"], 16))
        okx = okx and ok and b["bytes"] == 393 and hashlib.sha256(img.read(e0, b["bytes"])).hexdigest() == b["sha256"]
    R.check("extents-01 (complete) equals this image's .pdata record and bytes for 00305640 (393 B)",
            okx and len(x["bodies"]) == 1)
    res = json.load(open(os.path.join(ev, "result-02.json")))
    fa = res["facts"]
    Bd = Body(img, C2, C2_END)
    R.check("result-02's own non-stack writes (0x3056b3, 0x3056ba) and ten callee boundaries equal this review's census",
            [int(w["pc"], 16) for w in fa["own_nonstack_writes"]] == [C2 + 0x73, C2 + 0x7A] and
            [(int(c["pc"], 16), int(c["target"], 16)) for c in fa["callee_boundaries"]] == Bd.calls())
    cmod = fa["countermodel"]
    R.check("result-02's countermodel (first 65744 -> cost WORD 208, counter DWORD 65744, executed false) equals the "
            "arithmetic this review emulates",
            (cmod["first_full_quotient"], cmod["cost_input_word"], cmod["second_full_quotient"],
             cmod["counter_input_dword"], cmod["executed"]) == (65744, 65744 & 0xFFFF, 65744, 65744, False))
    cd = os.path.join(ev, "controls-01")

    def js(*p):
        return json.load(open(os.path.join(cd, *p)))
    ok1 = (js("false-extent-result", "extents-01.json")["complete"] is False and
           js("false-extent-result", "old-accepted.json")["producer_complete"] is True and
           js("false-extent-result", "old-producer.status.json")["exit"] == 0 and
           js("false-extent-result", "current-producer.status.json")["exit"] == 1 and
           "required complete current extent artifact" in open(os.path.join(cd, "false-extent-result",
                                                                            "current-producer.stderr")).read())
    ok2 = (js("binding-false-extent", "binding-extents-01.json")["complete"] is False and
           js("binding-false-extent", "old-accepted.json")["producer_complete"] is True and
           js("binding-false-extent", "old-binding-producer.status.json")["exit"] == 0 and
           js("binding-false-extent", "binding-qualification.status.json")["exit"] == 1)
    others = [js(d, "current-producer.status.json")["exit"] for d in ("changed-physical-extent", "false-capture-wrapper",
                                                                      "missing-metadata")]
    R.check("the recorded producer-repair artifacts agree with the README (inspected, not re-run): with extent "
            "complete = false the old helper producer exited 0 with producer_complete true and the current one exited 1 "
            "('required complete current extent artifact'); the same for the old binding producer and the new "
            "qualification; the other three helper cases exited 1",
            ok1 and ok2 and others == [1, 1, 1], "ok1 %s ok2 %s others %s" % (ok1, ok2, others))
    bq = json.load(open(os.path.join(ev, "binding-qualified-01.json")))
    R.check("binding-qualified-01: complete, base commit ca2dd6483, two VERIFIED_ACTUAL_CAPTURE_PREREQUISITES checks",
            bq["complete"] is True and bq["base_commit"].startswith("ca2dd6483") and
            [c["status"] for c in bq["actual_capture_checks"]] == ["VERIFIED_ACTUAL_CAPTURE_PREREQUISITES"] * 2)
    rd = " ".join(open(os.path.join(ev, "README.md"), encoding="utf-8").read().split())
    R.check("packet README keeps broader consequences, initialization, callbacks, aliasing and ownership OPEN and makes "
            "no whole-OV closure",
            "table/arena initialization, callbacks, aliasing and ownership remain OPEN" in rd and
            "no wholeOV closure" in rd)
    if os.path.isdir(EXTRACT):
        sets = {}
        for lg in LANGS:
            p = os.path.join(EXTRACT, lg, "binaryfile", "battle_pack.bin")
            if not os.path.exists(p):
                continue
            d = open(p, "rb").read()
            i = d.find(b"st2e\x1f\x02\x00\x00<\x00\x00\x00")
            if i < 0:
                sets[lg] = None
                continue
            t = d[i:i + 0x20 + 543 * 60]
            sets[lg] = ([k for k in range(543) if trow(t, k)[0x1E] == 10],
                        all(trow(t, k)[0x1E] == 7 and bit30(t, k) for k in STOCK))
        R.note("shipped language tables found: %s" % sorted(sets))
        R.check("every shipped language table found in the game extract (%d) has the same type-10 rows 226..241 and "
                "type 7 with bit 30 on 511..534" % len(sets),
                sets and all(v == (list(range(226, 242)), True) for v in sets.values()), str(sets)[:200])
    else:
        R.note("game extract not present; only the retained US table was read")


def u32le(v):
    return struct.pack("<I", v & 0xFFFFFFFF)


CONTROLS = [
    ("+ 0x81 `movzx edx, di` -> `mov edx, edi` + NOP (00309110 gets the full quotient)", C2 + 0x81,
     bytes.fromhex("8bd790")),
    ("+ 0x8C `movzx edx, di` -> `mov edx, edi` + NOP (00308FF0 gets the full quotient)", C2 + 0x8C,
     bytes.fromhex("8bd790")),
    ("+ 0x145 counter input narrowed: `movzx edx, ax` / `mov cl, 0xd` / NOPs", C2 + 0x145,
     bytes.fromhex("0fb7d0b10d9090")),
    ("+ 0xA8 `setne sil` -> `sete sil` (mode inverted)", C2 + 0xA9, bytes([0x0F, 0x94])),
    ("+ 0x28 `mov r12d, r8d` -> `mov r12d, r9d` (the mode from the wrong argument)", C2 + 0x28, bytes.fromhex("458be1")),
    ("+ 0x58 the NULL-unit `je` -> NOPs", C2 + 0x58, bytes.fromhex("9090")),
    ("+ 0x6C byte +5 `jne` -> `je` (reset when +5 is nonzero)", C2 + 0x6C, bytes([0x74])),
    ("+ 0x73 reset target +0xE58 -> +0xE5C", C2 + 0x76, bytes([0x5C])),
    ("+ 0x117 type compare `cmp ecx, 8` -> `cmp ecx, 7` (type 9 takes the counter leg)", C2 + 0x119, bytes([0x07])),
    ("+ 0xE4 `cmovns` -> `cmovs`", C2 + 0xE5, bytes.fromhex("0f48")),
    ("+ 0x135 counter-leg descriptor cell 02EBF138 -> 02EBF140", C2 + 0x138,
     u32le(DESC + 8 - (C2 + 0x13C))),
    ("caller + 0x6DC `mov r8d, 1` -> `mov r8d, 0`", F + 0x6DE, u32le(0)),
]


def main():
    img = Img.load()
    R = Rep("rv_termres")
    R.table = load_table()
    print("== packet integrity")
    packet_bytes(img, R)
    census_checks(img, R)
    print("== shipping-image re-derivation")
    checks(img, R)
    print("== controls (each patched private image or table copy must FAIL at least one check above)")
    Rn = Rep("null")
    Rn.quiet = True
    Rn.table = R.table
    P0 = img.patched(C2 + 0x25, img.read(C2 + 0x25, 3))
    P0._private = True
    checks(P0, Rn, small=True)
    R.check("null control: an unchanged private copy passes every image check", Rn.fails == 0 and Rn.n > 0,
            "%d of %d; %s" % (Rn.n - Rn.fails, Rn.n, Rn.failed[:2]))
    R.note("null control: %d image checks" % Rn.n)
    nctl = 0
    for label, va, nb in CONTROLS:
        Pimg = img.patched(va, nb)
        Pimg._private = True
        if Pimg.d == img.d:
            raise SystemExit("control %s did not change the image" % label)
        Rc = Rep(label)
        Rc.quiet = True
        Rc.table = R.table
        try:
            checks(Pimg, Rc, small=True)
            failed = Rc.fails
            why = "%d failed: %s" % (failed, "; ".join(f[:60] for f in Rc.failed[:3]))
        except Exception as e:
            failed = 1
            why = "refused: %r after %d failed: %s" % (e, Rc.fails, "; ".join(f[:60] for f in Rc.failed[:3]))
        nctl += 1
        R.check("control: " + label, failed > 0, why)
    tb2 = bytearray(R.table)
    tb2[0x20 + 60 * 511 + 0x1E] = 10
    Rc = Rep("table")
    Rc.quiet = True
    Rc.table = bytes(tb2)
    P1 = img.patched(C2 + 0x25, img.read(C2 + 0x25, 3))
    P1._private = True
    checks(P1, Rc, small=False)
    nctl += 1
    R.check("control: table copy, row 511 type 7 -> 10", Rc.fails > 0,
            "%d failed: %s" % (Rc.fails, "; ".join(f[:60] for f in Rc.failed[:3])))
    disk = hashlib.sha256(open(find_exe(), "rb").read()).hexdigest()
    R.check("exe on disk still hashes to the pinned sha256 after all controls", disk == SHA_PIN, disk)
    print("TOTAL: %d checks, %d PASS, %d FAIL (%d controls)" % (R.n, R.n - R.fails, R.fails, nctl))


if __name__ == "__main__":
    main()
