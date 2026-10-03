"""rv_callerrow.py - FABLE independent re-derivation for ASTRA packet ov42-caller-row-preconditions (103aa3123, OV-42).

Own reader (rvlib.py: struct + capstone 5, copied unchanged from the kind-row review, sha256 69f9bc40be32abcc...).
Does not import or run ASTRA's prove.py, prove_owner_reload_order.py, run.py, control.py, capture*.py,
prepare-helper-extents.py, validate-title-source-annotations.py or the shared role adapter (reg_tracking.py).

Method:
  * image sha256; the battle-action routine 00304850 (seven chained .pdata records): 2034 code bytes decoded
    linearly and exactly to its one ret, the 13-DWORD phase table after the code, the entry latch of the unit's
    WORD +0x714 into R13, the entry guard, the R15 row formula, the phase-8/9 entries, the target-builder /
    helper / sequence argument transfers (register-write censuses on the local CFG), reach and dominance from
    the phase-8/9 entries;
  * the target builder 0030D160 (nine chained records, 1004 B): DX latch, its own row formation, caller R15 not
    read, its 22 calls and the two targets of its one indirect call;
  * the helper 00305430 (one record, 517 B): its two unsigned 16-bit bounds, the 278..542 arm, the bit-6 test of
    row byte +0x2C and the arm's return-0 tail;
  * the retained US action table (st2e, 543 rows x 60 B) read directly, and compared with the shipped
    battle_pack.bin in the game extract when that is present;
  * a concrete emulation (unicorn) of the ORIGINAL code: 00304850 from its entry at phases 8 and 9 with every
    callee stubbed by a code hook (returns at once with a scripted RAX and clobbers RCX/RDX/R8-R11); the helper
    00305430 from its entry with 0020E600 bound to the US table (it returns table + key) and its other callees
    stubbed; the builder 0030D160 from its entry up to its first non-lookup call;
  * a raw E8/E9 rel32 and 0F 8x census for 00304850, 0030D160, 00305430, 00306760 and the builder's two indirect
    targets; the caller's rip-relative accesses to the special-sequence cells 022C2158 .. 022C2180;
  * controls patch a private in-memory copy of the image (or a private copy of the table); the exe on disk is
    never written and its sha256 is rechecked at the end.
"""
import hashlib
import json
import os
import struct
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rvlib import Img, Body, Report, check_manifest, find_exe, SHA256 as SHA_PIN  # noqa: E402

F = 0x00304850                 # battle-action routine (the terminal caller)
CODE_END = F + 0x7F2           # 2034 code bytes
TBLOFF = F + 0x7F4             # 13 DWORD phase entries
END = F + 0x828
PH8, PH9 = F + 0x663, F + 0x66E
GETTER_CALL, BUILDER_CALL, HELPER_CALL = F + 0x67C, F + 0x692, F + 0x69E
PREVIEW_CALL, COST_CALL, SEQ_CALL = F + 0x6CD, F + 0x6E8, F + 0x6FD
B = 0x0030D160                 # target builder
B_END = B + 0x3EC
H = 0x00305430                 # helper
H_END = H + 0x205
GETTER, LOOKUP, RESOLVE = 0x00387090, 0x0020E600, 0x0031B7E0
PREVIEW, COST, SEQ, ALT = 0x00303830, 0x00305640, 0x00306760, 0x0030FE10
READY, ACQUIRE, PH8CALL = 0x0030CA80, 0x0030CFB0, 0x00319420
COOKIE_CHECK = 0x00808C40
H_EFFECT, H_CLASS, H_LIVE, H_NOTE = 0x00311F70, 0x002E9600, 0x00377C20, 0x003299B0
CB1, CB2 = 0x0030BB10, 0x0030BCB0
DESC = 0x02EBF138
STATE = 0x022C2160
SLUG = "ov42-caller-row-preconditions"
PRODUCER = "103aa31230175dbfe50ed445e3a3d2b4861ded56"
STOCK = list(range(511, 535))
EXTRACT = r"D:\FFXII_TZA_extract\ps2data\image\ff12\test_battle\us\binaryfile\battle_pack.bin"


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


def evdir():
    return os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(find_exe())))),
                        "FFXII TZA", "_experiments", "evidence", SLUG)


def load_table():
    return open(os.path.join(evdir(), "action_data_us.st2e"), "rb").read()


def trow(tb, i):
    n, st, off = struct.unpack_from("<IHxxI", tb, 4)
    return tb[off + st * i: off + st * (i + 1)]


def bit30(tb, i):
    return (struct.unpack_from("<I", trow(tb, i), 0xC)[0] >> 30) & 1


# ------------------------------------------------------------------ emulation of the original code
class Emu(object):
    STK, RET, UNIT, SCR, TBL = 0x7F000000, 0x7E000000, 0x41000000, 0x50000000, 0x30000000
    UNIT2 = 0x41008000
    JUNK = 0xC1C1C1C1C1C1C1C1

    def __init__(self, img, code_ranges, stubs):
        from unicorn import Uc, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE, UC_HOOK_MEM_WRITE, UC_HOOK_INTR
        from unicorn import UC_HOOK_MEM_READ_UNMAPPED, UC_HOOK_MEM_FETCH_UNMAPPED, UC_HOOK_MEM_WRITE_UNMAPPED
        from unicorn import x86_const as X
        self.X = X
        mu = self.mu = Uc(UC_ARCH_X86, UC_MODE_64)
        pages = set()
        spans = list(code_ranges) + [(0x01F44000, 0x01F45000), (0x022BE000, 0x022C7000), (0x02EBF000, 0x02EC0000)]
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
        for a in (self.STK, self.UNIT, self.SCR, self.TBL):
            mu.mem_map(a, 0x10000)
        mu.mem_map(self.RET, 0x1000)
        self.code_ranges = list(code_ranges)
        self.stubs = set(stubs)
        self.stub_rax, self.stub_fx = {}, {}
        self.until = None
        self.calls_n = {}
        self.trace, self.writes, self.intr, self.fault, self.left = [], [], None, None, None

        def ch(uc, addr, size, ud):
            if addr == self.until:
                uc.emu_stop()
                return
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
                if v is not None:      # None: the stub preserves RAX (the cookie check)
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

    def r16(self, a):
        return struct.unpack("<H", bytes(self.mu.mem_read(a, 2)))[0]

    def r8(self, a):
        return bytes(self.mu.mem_read(a, 1))[0]

    def setup(self, table, W=0, phase=9, desc=True, state=0):
        mu = self.mu
        for a in (self.UNIT, self.SCR, self.TBL):
            mu.mem_write(a, b"\0" * 0x10000)
        mu.mem_write(self.TBL, table)
        mu.mem_write(DESC, struct.pack("<Q", self.TBL if desc else 0))
        mu.mem_write(STATE, struct.pack("<I", state))
        U = self.UNIT
        mu.mem_write(U + 8, struct.pack("<I", 0xCAFE0008))
        mu.mem_write(U + 0x698, struct.pack("<Q", self.SCR + 0x800))
        mu.mem_write(U + 0x6B4, bytes([phase]))
        mu.mem_write(U + 0x710, struct.pack("<I", 0x777))
        mu.mem_write(U + 0x714, struct.pack("<H", W))
        mu.mem_write(U + 0x77C, struct.pack("<I", 1))
        self.calls_n = {}

    def run(self, start, regs, until=None, count=40000):
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
        self.until = self.RET if until is None else until
        try:
            self.mu.emu_start(start, self.until, count=count)
        except UcError as e:
            if self.intr is None and self.fault is None:
                self.fault = "UcError %s" % e
        r = dict((k, self.mu.reg_read(getattr(X, "UC_X86_REG_" + k.upper())))
                 for k in ("rax", "rbx", "rsi", "rdi", "rbp", "r12", "r13", "r14", "r15", "rip", "rsp"))
        r["trace"], r["intr"], r["fault"], r["left"] = list(self.trace), self.intr, self.fault, self.left
        r["writes"] = list(self.writes)
        r["ok"] = (r["rip"] == self.until and not r["fault"] and not r["intr"] and not r["left"])
        return r


def lookup_bound(hi=0):
    """0020E600 stub: the resolver bound to the retained table - returns table + key (+ optional upper bits)."""
    return lambda regs, k: (hi << 32) | (Emu.TBL + (regs[0] & 0xFFFFFFFF))


def ROW(W, hi=0):
    return (Emu.TBL + 0x20 + 60 * W) & 0xFFFFFFFF


def caller_emu(img):
    Bd = Body(img, F, CODE_END)
    stubs = sorted(set(t for a, t in Bd.calls() if t is not None))
    return Emu(img, [(F, CODE_END)], stubs)


GVAL = 0xFFFF00000001ABCD      # getter stub return: AX = ABCD, upper bits set


def run_caller(E, table, W, phase=9, getter=GVAL, helper_rax=0x5555, builder_fx=None, desc=True, lookup_hi=7,
               extra=None):
    E.setup(table, W=W, phase=phase, desc=desc)
    E.stub_rax = {LOOKUP: lookup_bound(lookup_hi), RESOLVE: Emu.UNIT2, GETTER: getter, H: helper_rax,
                  BUILDER_STUB_KEY: 0x3, COOKIE_CHECK: None}
    E.stub_rax.update(extra or {})
    E.stub_fx = {}
    if builder_fx:
        E.stub_fx[B] = builder_fx
    r = E.run(F, {"rcx": Emu.UNIT})
    r["phase"] = E.r8(Emu.UNIT + 0x6B4)
    return r


BUILDER_STUB_KEY = B


def calls_of(r):
    return [t[0] for t in r["trace"]]


def args_of(r, addr):
    return [t[1:] for t in r["trace"] if t[0] == addr]


def caller_emu_checks(img, R, tb, small=False):
    E = caller_emu(img)
    U = Emu.UNIT
    seqw = [LOOKUP, LOOKUP, GETTER, B, H, PREVIEW, COST, SEQ, COOKIE_CHECK]
    r9 = run_caller(E, tb, 511, phase=9)
    a = dict((t[0], t[1:]) for t in r9["trace"])
    R.check("emulated 00304850 from its entry, phase byte unit+0x6B4 = 9, unit WORD +0x714 = 511, the US table bound "
            "(lookup returns carry upper bits 7): calls 0020E600 twice (the entry row), then 00387090, 0030D160, 00305430, 00303830, 00305640, 00306760, "
            "then the cookie check, in that order; returns EAX 0 with R15 restored; the phase byte ends at 11",
            r9["ok"] and calls_of(r9) == seqw and r9["rax"] & 0xFFFFFFFF == 0 and
            r9["r15"] == 0x1515151515151515 and r9["phase"] == 11,
            "calls %s rax %X ok %s fault %s phase %d" % (["%X" % c for c in calls_of(r9)], r9["rax"], r9["ok"],
                                                         r9["fault"], r9["phase"]))
    okargs = (GETTER in a and a[GETTER][0] == Emu.SCR + 0x800 and
              B in a and a[B][0] == U and a[B][1] == 0xABCD and a[B][2] & 0xFFFFFFFF == 0x777 and a[B][3] == U + 0x778 and
              H in a and a[H][0] == U and a[H][1] == 511 and
              PREVIEW in a and a[PREVIEW][0] == U and a[PREVIEW][1] == ROW(511) and a[PREVIEW][2] == U + 0x778 and
              COST in a and a[COST][0] == U and a[COST][1] == ROW(511) and a[COST][2] & 0xFFFFFFFF == 1 and
              SEQ in a and a[SEQ][0] == U and a[SEQ][1] == ROW(511))
    R.check("emulated carriers: the getter gets RCX = unit QWORD +0x698; the builder gets RCX = unit, RDX = the getter's "
            "AX zero-extended (ABCD, upper bits dropped), R8D = unit DWORD +0x710, R9 = unit + 0x778; the helper gets "
            "RCX = unit, RDX = the entry WORD 511; 00303830 and 00305640 (R8D = 1) and the sequence 00306760 get RDX = "
            "R15 = low32(lookup + 60 * 511) zero-extended",
            okargs, str(dict(("%X" % k, tuple("%X" % x for x in v)) for k, v in a.items())))
    r8 = run_caller(E, tb, 511, phase=8)
    R.check("emulated phase 8: 0031B7E0 (the entry owner lookup, phase < 9), the two entry lookups, then 00319420 with RCX = unit + 0x6B0, then "
            "the phase-9 sequence unchanged (same carriers); neither run calls 0030CA80 or 0030CFB0",
            r8["ok"] and calls_of(r8) == [RESOLVE, LOOKUP, LOOKUP, PH8CALL] + seqw[2:] and args_of(r8, PH8CALL)[0][0] == U + 0x6B0 and
            args_of(r8, SEQ)[0][1] == ROW(511) and args_of(r8, B)[0][1] == 0xABCD and
            not set([READY, ACQUIRE]) & set(calls_of(r8) + calls_of(r9)),
            "calls %s" % ["%X" % c for c in calls_of(r8)])

    r6 = run_caller(E, tb, 511, phase=6, getter=lambda regs, k: 0x0AAA if k == 0 else 0x0BBB, extra={READY: 1})
    c6 = [x for x in calls_of(r6) if x in (GETTER, ACQUIRE, READY, PH8CALL, B, H, PREVIEW, COST, SEQ)]
    R.check("emulated phase 6 (0030CA80 stubbed to return 1): one invocation runs the getter and 0030CFB0 (case 6, R8 = "
            "the first getter word AAA), 0030CA80 (case 7), 00319420 (case 8), then the getter again and the terminal "
            "calls of case 9 - the builder gets the second getter word BBB, the helper 511 and the sequence the row of 511; "
            "the phase byte ends at 11",
            r6["ok"] and c6 == [GETTER, ACQUIRE, READY, PH8CALL, GETTER, B, H, PREVIEW, COST, SEQ] and
            args_of(r6, ACQUIRE)[0][2] & 0xFFFFFFFF == 0x0AAA and args_of(r6, B)[0][1] == 0x0BBB and
            args_of(r6, H)[0][1] == 511 and args_of(r6, SEQ)[0][1] == ROW(511) and r6["phase"] == 11,
            "calls %s phase %d" % (["%X" % c for c in c6], r6["phase"]))

    def fx(uc, regs, k):
        uc.mem_write(U + 0x714, struct.pack("<H", 0xD5))
    rl = run_caller(E, tb, 511, phase=9, builder_fx=fx)
    R.check("emulated latch: when the builder stub rewrites unit WORD +0x714 to D5, the helper still gets 511 and the "
            "sequence still gets the row of 511, and 00303830/00305640 are still called (R13 and R15 are not reloaded)",
            rl["ok"] and calls_of(rl) == seqw and args_of(rl, H)[0][1] == 511 and args_of(rl, SEQ)[0][1] == ROW(511),
            "calls %s" % ["%X" % c for c in calls_of(rl)])
    outs = set()
    for hv in (0, 1, 0xFFFFFFFF, 0xFFFFFFFFFFFFFFFF):
        rr = run_caller(E, tb, 511, phase=9, helper_rax=hv)
        outs.add((tuple((t[0],) + tuple(t[1:]) for t in rr["trace"] if t[0] not in (H,)),
                  tuple(w[1:] for w in rr["writes"]), rr["rax"] & 0xFFFFFFFF, rr["ok"]))
    R.check("emulated: 00305430 returning 0, 1, FFFFFFFF or 2^64 - 1 gives identical later calls, arguments, writes "
            "and return (its EAX is overwritten untested)", len(outs) == 1 and list(outs)[0][3], "%d outcomes" % len(outs))
    # the D0..F1 skip, the bit-30 test and the full sweep
    sweep = range(0, 543) if not small else [0, 0xCF, 0xD0, 0xE2, 0xF1, 0xF2, 0x113, 510, 511, 534, 535, 542]
    bad = []
    for W in sweep:
        rr = run_caller(E, tb, W, phase=9, getter=0x0BEE)
        c = calls_of(rr)
        skip = 0xD0 <= W <= 0xF1
        b30 = bit30(tb, W)
        want = [GETTER, B, H] + ([] if skip else [PREVIEW]) + ([COST] if (b30 and not skip) else []) + \
            ([SEQ] if b30 else [ALT])
        got = [x for x in c if x in (GETTER, B, H, PREVIEW, COST, SEQ, ALT)]
        if not rr["ok"] or got != want or args_of(rr, B)[0][1] != 0x0BEE or args_of(rr, H)[0][1] != W or \
                (b30 and args_of(rr, SEQ)[0][1] != ROW(W)):
            bad.append("W %X got %s want %s" % (W, ["%X" % x for x in got], ["%X" % x for x in want]))
    R.check("emulated sweep over %d entry words W (phase 9, getter AX = BEE): the builder always gets BEE and the "
            "helper W; 00303830 runs unless W is D0..F1; 00305640 runs iff row W has +0x0C bit 30 and W is outside "
            "D0..F1; the sequence gets the row of W iff bit 30, else 0030FE10 runs" % len(sweep), not bad,
            "; ".join(bad[:3]))
    rg = run_caller(E, tb, 0x21F, phase=9)
    rk = run_caller(E, tb, 0x21E, phase=9)
    R.check("emulated entry guard: W = 0x21F returns EAX FFFFFFFF after only the owner lookup (and the cookie check); "
            "W = 0x21E (542) runs the terminal sequence",
            rg["ok"] and rg["rax"] & 0xFFFFFFFF == 0xFFFFFFFF and calls_of(rg) == [RESOLVE, COOKIE_CHECK] and
            rk["ok"] and GETTER in calls_of(rk) and B in calls_of(rk),
            "21F calls %s rax %X; 21E calls %s" % (["%X" % c for c in calls_of(rg)], rg["rax"],
                                                   ["%X" % c for c in calls_of(rk)]))
    rn = run_caller(E, tb, 511, phase=9, desc=False)
    R.check("emulated: with a null descriptor R15 is 0, and the first row test reads address 0xC (no null guard; a source "
            "prediction)", rn["fault"] == 0xC and calls_of(rn) == [GETTER, B, H, PREVIEW],
            "fault %s calls %s" % (rn["fault"], ["%X" % c for c in calls_of(rn)]))


def builder_emu_checks(img, R, tb):
    E = Emu(img, [(B, B_END)], [RESOLVE, LOOKUP])
    outs = []
    for r15 in (0x1515151515151515, 0, Emu.TBL + 0x20 + 60 * 99):
        E.setup(tb)
        E.stub_rax = {RESOLVE: Emu.UNIT2, LOOKUP: lookup_bound(3)}
        r = E.run(B, {"rcx": Emu.UNIT, "rdx": 0xFFFFFFFF00000201, "r8": 0xABCD00000777, "r9": Emu.UNIT + 0x778,
                      "r15": r15}, until=B + 0x93)
        outs.append(r)
    R.check("emulated builder 0030D160 from its entry to its first other call (+ 0x93): with DX = 0x201 (513) it forms "
            "RSI = low32(lookup + 60 * 513) from its own three descriptor reads and two lookups, for any incoming R15; "
            "its owner lookup gets ECX = R8D (777); R15 then holds R9",
            all(r["ok"] and r["rsi"] == ROW(513) and r["r15"] == Emu.UNIT + 0x778 and
                [t[0] for t in r["trace"]] == [RESOLVE, LOOKUP, LOOKUP] and r["trace"][0][1] & 0xFFFFFFFF == 0x777
                for r in outs), "; ".join("rsi %X ok %s" % (r["rsi"], r["ok"]) for r in outs))


def helper_emu(img):
    return Emu(img, [(H, H_END)], [LOOKUP, RESOLVE, H_EFFECT, H_CLASS, H_LIVE, H_NOTE])


def run_helper(E, tb, W, desc=True, first_null=False, lookup_hi=0):
    E.setup(tb, desc=desc)
    lb = lookup_bound(lookup_hi)
    E.stub_rax = {LOOKUP: (lambda regs, k: 0 if (first_null and k == 0) else lb(regs, k)), RESOLVE: Emu.UNIT2,
                  H_EFFECT: 0x99, H_CLASS: 0, H_LIVE: 0}
    return E.run(H, {"rcx": Emu.UNIT, "rdx": 0xFFFF0000 | W})


def helper_emu_checks(img, R, tb, small=False):
    E = helper_emu(img)
    bad = []
    for W in STOCK:
        r = run_helper(E, tb, W)
        if not (r["ok"] and r["rax"] == 0 and [t[0] for t in r["trace"]] == [LOOKUP, LOOKUP] and not r["writes"]):
            bad.append("%d: rax %X calls %s writes %d fault %s" % (W, r["rax"], ["%X" % t[0] for t in r["trace"]],
                                                                    len(r["writes"]), r["fault"]))
    R.check("emulated helper 00305430 (EDX upper half FFFF), ids 511..534 with the US table bound: each returns RAX = 0 "
            "after exactly two 0020E600 calls and no write outside its stack", not bad, "; ".join(bad[:3]))
    arm = range(278, 543) if not small else [278, 325, 455, 511, 542]
    b6 = [i for i in range(278, 543) if trow(tb, i)[0x2C] & 0x40]
    bad = []
    for W in arm:
        r = run_helper(E, tb, W)
        c = [t[0] for t in r["trace"]]
        if W in b6:
            want = [LOOKUP, LOOKUP, RESOLVE] + ([] if W == 0x1C7 else [H_EFFECT])
        else:
            want = [LOOKUP, LOOKUP]
        if not r["ok"] or c != want or r["rax"] != 0:
            bad.append("%d: %s rax %X" % (W, ["%X" % x for x in c], r["rax"]))
        if W in b6 and W != 0x1C7:
            eff = ([t for t in r["trace"] if t[0] == H_EFFECT] + [None])[0]
            if not eff or not (eff[1] == Emu.UNIT and eff[2] == Emu.UNIT2 and eff[3] & 0xFFFFFFFF == 1):
                bad.append("%d effect args" % W)
    R.check("emulated arm 278..542 (%d ids): bit 6 of +0x2C clear -> two lookups and return 0; bit 6 set (US rows %s) -> "
            "0031B7E0 then 00311F70(unit, owner, 1), except 455 (0x1C7), which returns 0 after the owner lookup"
            % (len(arm), b6), not bad, "; ".join(bad[:3]))
    tb2 = bytearray(tb)
    n, st, off = struct.unpack_from("<IHxxI", tb, 4)
    tb2[off + st * 511 + 0x2C] |= 0x40
    r = run_helper(E, bytes(tb2), 511)
    R.check("emulated positive control (supplied table copy, row 511 +0x2C bit 6 set): 0031B7E0, then 00311F70 with "
            "RCX = unit, RDX = the owner, R8D = 1; returns 0",
            r["ok"] and [t[0] for t in r["trace"]] == [LOOKUP, LOOKUP, RESOLVE, H_EFFECT] and r["rax"] == 0,
            str(["%X" % t[0] for t in r["trace"]]))
    rn = run_helper(E, tb, 511, desc=False)
    rf = run_helper(E, tb, 511, first_null=True)
    rh = run_helper(E, tb, 520, lookup_hi=5)
    R.check("emulated null cases: a null descriptor reads address 0x2C with no lookup; a null first lookup reads 0x2C "
            "after one lookup (no null guard; source predictions); a lookup return with upper bits 5 still reads the "
            "row at low32 (the row is formed by a 32-bit add)",
            rn["fault"] == 0x2C and not rn["trace"] and rf["fault"] == 0x2C and [t[0] for t in rf["trace"]] == [LOOKUP]
            and rh["ok"] and rh["rax"] == 0 and len(rh["trace"]) == 2,
            "null-desc fault %s; first-null fault %s; hi ok %s" % (rn["fault"], rf["fault"], rh["ok"]))


def ext_reach(Bd, frm, extra, avoid=()):
    """Local CFG reach with extra edges (an indirect jump's chosen table targets)."""
    avoid = set(avoid)
    seen, stack = set(), [frm]
    while stack:
        a = stack.pop()
        if a in seen or a in avoid or a not in Bd.ins:
            continue
        seen.add(a)
        stack.extend(Bd.succ(a))
        stack.extend(extra.get(a, []))
    return seen


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


def checks(img, R, small=False):
    tb = R.table
    R.check("image sha256 = %s..." % SHA_PIN[:20], hashlib.sha256(img.d).hexdigest() == SHA_PIN or
            getattr(img, "_private", False))
    # ---------------- the caller's extent
    ents, ok = img.pdata_cover(F, END)
    R.check("00304850's .pdata: seven records tile 00304850 .. + 0x828 exactly (the root, then six CHAININFO records "
            "resolving to it)", ok and len(ents) == 7 and all(e[3] == F for e in ents), str(len(ents)))
    C = Body(img, F, CODE_END)
    rets = [a for a in C.order if C[a].mnemonic == "ret"]
    R.check("code: 00304850 .. + 0x7F2 (2034 B) decodes exactly; its one `ret` is the last instruction (+ 0x7F1); a "
            "2-byte NOP (66 90) and 13 DWORDs (+ 0x7F4 .. + 0x828) follow",
            C.exact and rets == [F + 0x7F1] and C.order[-1] == F + 0x7F1 and img.read(CODE_END, 2) == b"\x66\x90" and
            END - TBLOFF == 52)
    ind = [a for a in C.order if C[a].mnemonic == "jmp" and C[a].direct_target() is None]
    tg = [img.base + img.u32(TBLOFF + 4 * i) for i in range(13)]
    R.check("the phase switch: + 0xEC `movzx eax, byte ptr [rsi + 4]` (unit + 0x6B4), + 0xF0 `cmp eax, 0xc`, + 0xF3 `ja` "
            "+ 0x7B6, + 0xF9 RDX = image base, + 0x100 DWORD [rdx + rax*4 + 0x1e5044] (= the 13 entries after the code), "
            "+ 0x10A `jmp rcx` - the body's only indirect jump",
            T(C, F + 0xEC) == "movzx eax, byte ptr [rsi + 4]" and T(C, F + 0xF0) == "cmp eax, 0xc" and
            C[F + 0xF3].direct_target() == F + 0x7B6 and rip_target(C[F + 0xF9]) == img.base and
            T(C, F + 0x100) == "mov ecx, dword ptr [rdx + rax*4 + 0x1e5044]" and img.base + 0x1E5044 == TBLOFF and
            T(C, F + 0x10A) == "jmp rcx" and ind == [F + 0x10A])
    R.check("the 13 entries land on instruction boundaries; entry 8 = + 0x663 (00304EB3) and entry 9 = + 0x66E "
            "(00304EBE); entry 6 = + 0x555, entry 7 = + 0x5DC",
            all(t in C.ins for t in tg) and tg[8] == PH8 and tg[9] == PH9 and tg[6] == F + 0x555 and tg[7] == F + 0x5DC,
            " ".join("+%X" % (t - F) for t in tg))
    # ---------------- registers and the entry latch
    R.check("RDI = entry RCX (the unit, + 0x42), RSI = unit + 0x6B0 (+ 0x2F), R12 = unit + 0x690 (+ 0x36), R14 = 0 "
            "(+ 0x2C); each written nowhere else but the epilogue restores",
            T(C, F + 0x42) == "mov rdi, rcx" and T(C, F + 0x2F) == "lea rsi, [rcx + 0x6b0]" and
            T(C, F + 0x36) == "lea r12, [rcx + 0x690]" and T(C, F + 0x2C) == "xor r14d, r14d" and
            writers(C, "rdi") == [F + 0x42, F + 0x7EF] and writers(C, "rsi") == [F + 0x2F, F + 0x7E2] and
            writers(C, "r12") == [F + 0x36, F + 0x7ED] and writers(C, "r14") == [F + 0x2C, F + 0x7AB, F + 0x7B6, F + 0x7E9],
            "rdi %s rsi %s r12 %s r14 %s" % tuple(["%X" % (a - F) for a in writers(C, x)] for x in ("rdi", "rsi", "r12", "r14")))
    R.check("the entry latch: + 0x3D `movzx r13d, word ptr [rsi + 0x64]` (2 B; RSI + 0x64 = unit + 0x714); R13 is written "
            "only there, by `sub r13w, ax` (+ 0x6B5, after the helper call) and by the restore + 0x7EB",
            T(C, F + 0x3D) == "movzx r13d, word ptr [rsi + 0x64]" and C[F + 0x3D].mems[0]["size"] == 2 and
            writers(C, "r13") == [F + 0x3D, F + 0x6B5, F + 0x7EB])
    R.check("the entry guard: + 0x58 `mov ebx, 0x21e`; + 0x8E `cmp r13w, bx` (16-bit) and + 0x92 `ja` (unsigned) to + 0x7C7 "
            "`or eax, 0xffffffff` - an entry word above 542 returns -1 before the phase switch; EBX unchanged between "
            "+ 0x58 and + 0x8E except by the ABI across the owner lookup",
            T(C, F + 0x58) == "mov ebx, 0x21e" and T(C, F + 0x8E) == "cmp r13w, bx" and
            C[F + 0x92].bytes[:2] == b"\x0f\x87" and C[F + 0x92].direct_target() == F + 0x7C7 and
            T(C, F + 0x7C7) == "or eax, 0xffffffff" and writers(C, "rbx", F + 0x59, F + 0x8E) == [])
    R.check("R15 at entry: three QWORD loads of 02EBF138 (+ 0x98, + 0xC0, + 0xD2); + 0xB6 and + 0xCA call 0020E600 with "
            "ECX = descriptor +0xC; + 0xCF R15 = the second return; + 0xD9 `movzx ecx, word ptr [rax + 8]`, + 0xDD "
            "`movzx eax, r13w`, + 0xE1 `imul ecx, eax`, + 0xE4 `add r15d, ecx` (32-bit, zero-extends R15); a null "
            "descriptor or null first return gives R15 = R14 = 0 (+ 0xE9)",
            [a for a in C.order if rip_target(C[a]) == DESC and F + 0x90 <= a < F + 0xEC] == [F + 0x98, F + 0xC0, F + 0xD2]
            and T(C, F + 0xB6) == "call 0x20e600" and T(C, F + 0xCA) == "call 0x20e600" and
            T(C, F + 0xCF) == "mov r15, rax" and T(C, F + 0xD9) == "movzx ecx, word ptr [rax + 8]" and
            T(C, F + 0xDD) == "movzx eax, r13w" and T(C, F + 0xE1) == "imul ecx, eax" and
            T(C, F + 0xE4) == "add r15d, ecx" and C[F + 0xE4].bytes == bytes.fromhex("4403f9") and
            T(C, F + 0xE9) == "mov r15, r14" and C[F + 0xB1].direct_target() == F + 0xE9 and
            C[F + 0xBE].direct_target() == F + 0xE9)
    r8set = C.reach(PH8)
    r9set = C.reach(PH9)
    e8 = ext_reach(C, F, {F + 0x10A: [PH8]})
    e9 = ext_reach(C, F, {F + 0x10A: [PH9]})
    R.note("local-CFG reach (direct edges, calls return): from + 0x663 %d instructions, from + 0x66E %d; from the "
           "routine entry with the switch resolved to entry 8 / 9: %d / %d" % (len(r8set), len(r9set), len(e8), len(e9)))
    R.check("reach from the routine entry with the switch resolved to entry 8 or 9 is 161 or 158 instructions (the "
            "packet's 'visited'); the case reach from + 0x663 / + 0x66E stays at + 0x663 and above: no edge back to the "
            "readiness call 0030CA80 (+ 0x5EE) or the acquire call 0030CFB0 (+ 0x5D4); R15 is not written before the "
            "sequence call on either reach",
            len(e8) == 161 and len(e9) == 158 and F + 0x5EE not in e8 and F + 0x5D4 not in e8 and
            min(r8set) == PH8 and min(r9set) == PH9 and
            F + 0x5EE not in r8set and F + 0x5D4 not in r8set and
            not [a for a in writers(C, "r15") if a in r8set and a < SEQ_CALL] and
            T(C, F + 0x5EE) == "call 0x30ca80" and T(C, F + 0x5D4) == "call 0x30cfb0")
    R.check("the earlier cases fall through: case 6 ends `inc byte ptr [rsi + 4]` (+ 0x5D9) into case 7 (+ 0x5DC); case 7 "
            "keeps 0030CA80's EAX in EBX (+ 0x5F3), leaves on EBX = 0 (+ 0x64D) or unit bit 12 set (+ 0x65A), else ends "
            "`inc` (+ 0x660) into case 8 (+ 0x663) - so an invocation entering at 6 or 7 can reach the terminal calls",
            T(C, F + 0x5D9) == "inc byte ptr [rsi + 4]" and C.order[C.order.index(F + 0x5D9) + 1] == F + 0x5DC and
            T(C, F + 0x5F3) == "mov ebx, eax" and C[F + 0x64D].direct_target() == F + 0x7BA and
            C[F + 0x65A].direct_target() == F + 0x7BA and T(C, F + 0x655) == "bt rax, 0xc" and
            T(C, F + 0x660) == "inc byte ptr [rsi + 4]" and C.order[C.order.index(F + 0x660) + 1] == PH8 and
            SEQ_CALL in C.reach(F + 0x555) and SEQ_CALL in C.reach(F + 0x5DC))
    R.check("from both entries the builder call (+ 0x692) and the helper call (+ 0x69E) dominate the sequence call "
            "(+ 0x6FD)", all(SEQ_CALL in C.reach(e) and SEQ_CALL not in C.reach(e, avoid=[x])
                             for e in (PH8, PH9) for x in (BUILDER_CALL, HELPER_CALL)))
    R.check("phase 9's transfer to the builder: + 0x675 RCX = QWORD [rdi + 0x698], + 0x67C `call 00387090`, + 0x681 "
            "R8D = DWORD [rsi + 0x60] (unit + 0x710), + 0x685 R9 = rsi + 0xc8 (unit + 0x778), + 0x68C `movzx edx, ax`, "
            "+ 0x68F RCX = RDI, + 0x692 `call 0030D160`; RAX not written and RDX written only by the `movzx` between the "
            "two calls",
            T(C, F + 0x675) == "mov rcx, qword ptr [rdi + 0x698]" and T(C, GETTER_CALL) == "call 0x387090" and
            T(C, F + 0x681) == "mov r8d, dword ptr [rsi + 0x60]" and T(C, F + 0x685) == "lea r9, [rsi + 0xc8]" and
            T(C, F + 0x68C) == "movzx edx, ax" and T(C, F + 0x68F) == "mov rcx, rdi" and
            T(C, BUILDER_CALL) == "call 0x30d160" and writers(C, "rax", F + 0x681, BUILDER_CALL) == [] and
            writers(C, "rdx", F + 0x681, BUILDER_CALL) == [F + 0x68C])
    R.check("the helper and its ignored return: + 0x697 `movzx edx, r13w`, + 0x69B RCX = RDI, + 0x69E `call 00305430`; "
            "the next instruction + 0x6A3 `movabs rax, 0x400000000000` writes RAX without reading it or the flags",
            T(C, F + 0x697) == "movzx edx, r13w" and T(C, F + 0x69B) == "mov rcx, rdi" and
            T(C, HELPER_CALL) == "call 0x305430" and C.order[C.order.index(HELPER_CALL) + 1] == F + 0x6A3 and
            T(C, F + 0x6A3) == "movabs rax, 0x400000000000" and "rax" not in C[F + 0x6A3].reg_reads and
            "rflags" not in C[F + 0x6A3].reg_reads)
    R.check("the sequence leg: + 0x6B0/+ 0x6B5 `sub r13w, 0xd0` (16-bit), + 0x6B9 `cmp r13w, 0x21`, + 0x6BE `jbe` + 0x6ED "
            "skips 00303830 (+ 0x6CD) and 00305640 (+ 0x6E8) for words D0..F1; + 0x6ED `test dword ptr [r15 + 0xc], "
            "0x40000000`, `je` 0030FE10; + 0x6F7 `mov rdx, r15`, + 0x6FA `mov rcx, rdi`, + 0x6FD `call 00306760`",
            T(C, F + 0x6B0) == "mov eax, 0xd0" and T(C, F + 0x6B5) == "sub r13w, ax" and
            T(C, F + 0x6B9) == "cmp r13w, 0x21" and C[F + 0x6BE].direct_target() == F + 0x6ED and
            C[F + 0x6BE].mnemonic == "jbe" and T(C, PREVIEW_CALL) == "call 0x303830" and
            T(C, COST_CALL) == "call 0x305640" and T(C, F + 0x6ED) == "test dword ptr [r15 + 0xc], 0x40000000" and
            C[F + 0x6F5].direct_target() == F + 0x704 and T(C, F + 0x70A) == "call 0x30fe10" and
            T(C, F + 0x6F7) == "mov rdx, r15" and T(C, F + 0x6FA) == "mov rcx, rdi" and T(C, SEQ_CALL) == "call 0x306760")
    sc = sorted((a, rip_target(C[a])) for a in C.order if rip_target(C[a]) is not None and
                0x022C2150 <= rip_target(C[a]) < 0x022C2180)
    R.check("no owner or kind reference in the caller: its rip-relative accesses to 022C2150 .. 022C2180 are the one-shot "
            "flag test of 022C2158 (+ 0x4F9, not on the phase-8/9 reach) and the state read of 022C2160 (+ 0x71C, after "
            "the sequence call); nothing reads the kind 022C215C or the owner 022C2168",
            sc == [(F + 0x4F9, 0x022C2158), (F + 0x71C, STATE)] and F + 0x4F9 not in r8set and F + 0x71C in r9set,
            str([("%X" % a, "%X" % t) for a, t in sc]))
    # ---------------- the target builder
    bents, bok = img.pdata_cover(B, B_END)
    BB = Body(img, B, B_END)
    R.check("0030D160: nine chained records tile 0030D160 .. + 0x3EC (1004 B) exactly; the body decodes exactly and ends "
            "in its one `ret` (+ 0x3EB)", bok and len(bents) == 9 and BB.exact and
            [a for a in BB.order if BB[a].mnemonic == "ret"] == [B + 0x3EB])
    R.check("the builder latches DX: + 0x27 `movzx edi, dx` is its only RDX read before its first call; EDI is not "
            "written again before + 0x83 `movzx eax, di`",
            T(BB, B + 0x27) == "movzx edi, dx" and readers(BB, "rdx", B, B + 0x2A) == [B + 0x27] and
            writers(BB, "rdi", B + 0x28, B + 0x83) == [] and T(BB, B + 0x83) == "movzx eax, di")
    R.check("the builder's own row: three QWORD loads of 02EBF138 (+ 0x3B, + 0x66, + 0x78), lookups + 0x5C and + 0x70, "
            "+ 0x75 RSI = the second return, + 0x7F WORD stride, + 0x86 `imul ecx, eax`, + 0x89 `add esi, ecx` "
            "(32-bit); null descriptor or first return -> RSI = 0 (+ 0x8D)",
            [a for a in BB.order if rip_target(BB[a]) == DESC] == [B + 0x3B, B + 0x66, B + 0x78] and
            T(BB, B + 0x5C) == "call 0x20e600" and T(BB, B + 0x70) == "call 0x20e600" and
            T(BB, B + 0x75) == "mov rsi, rax" and T(BB, B + 0x7F) == "movzx ecx, word ptr [rax + 8]" and
            T(BB, B + 0x86) == "imul ecx, eax" and T(BB, B + 0x89) == "add esi, ecx" and T(BB, B + 0x8D) == "mov rsi, rbx")
    R.check("the builder does not read the caller's R15: before + 0x21 `mov r15, r9` the only R15 access is the save "
            "`push r15` (+ 0x6); R9 (unit + 0x778) is its target list",
            T(BB, B + 0x6) == "push r15" and T(BB, B + 0x21) == "mov r15, r9" and
            readers(BB, "r15", B, B + 0x21) == [B + 0x6])
    bcalls = [(a, t) for a, t in BB.calls()]
    rs = json.load(open(os.path.join(evdir(), "result-01.json")))
    pk = [(int(x["pc"], 16), x["target"]) for x in rs["facts"]["builder_opaque_boundaries"]]
    R.check("the builder makes 22 calls, and they are exactly the packet's 22 opaque boundaries (one of them the "
            "indirect `call rax`, + 0x22D)",
            len(bcalls) == 22 and [(a, ("rax" if t is None else hex(t))) for a, t in bcalls] == pk,
            "%d calls" % len(bcalls))
    R.check("the indirect `call rax` (+ 0x22D) has two fixed targets: + 0x21C `lea rax` = 0030BB10, or (WORD row +0x36 "
            "bit 2 set, + 0x226 `cmovne rax, rbp`) RBP = 0030BCB0 from the `lea` at + 0x1C6 / + 0x2C7; RBP's other "
            "writes (+ 0x327, + 0x3B4) do not reach + 0x22D; both targets are .pdata roots",
            rip_target(BB[B + 0x21C]) == CB1 and T(BB, B + 0x226) == "cmovne rax, rbp" and
            rip_target(BB[B + 0x1C6]) == CB2 and rip_target(BB[B + 0x2C7]) == CB2 and T(BB, B + 0x22D) == "call rax" and
            sorted(set(writers(BB, "rbp")) - {B + 0x1C6, B + 0x2C7}) == [B + 0x327, B + 0x3B4] and
            B + 0x22D not in BB.reach(B + 0x327) and B + 0x22D not in BB.reach(B + 0x3B4) and
            root_of(img, CB1) == CB1 and root_of(img, CB2) == CB2 and T(BB, B + 0x214) == "test al, 4",
            "rbp writers %s" % ["+%X" % (a - B) for a in writers(BB, "rbp")])
    # ---------------- the helper
    HB = Body(img, H, H_END)
    hents, hok = img.pdata_cover(H, H_END)
    R.check("00305430: one .pdata record 00305430 .. + 0x205 (517 B); decodes exactly; rets at + 0xE5, + 0x147, + 0x1D8, "
            "+ 0x204", hok and len(hents) == 1 and HB.exact and
            [a for a in HB.order if HB[a].mnemonic == "ret"] == [H + 0xE5, H + 0x147, H + 0x1D8, H + 0x204])
    R.check("helper bounds, unsigned 16-bit: + 0x1D `movzx edi, dx`; + 0x23 `cmp dx, ax` with AX = 0x115 (66 3B D0) and "
            "+ 0x26 `ja` + 0x148; there + 0x150 `sub ax, cx` (DI - 0x116) and + 0x158 `cmp ax, cx` with 0x108 (66 "
            "prefixes), + 0x15B `ja` + 0x1D9 - so DI 278..542 enter the arm at + 0x15D",
            T(HB, H + 0x1D) == "movzx edi, dx" and T(HB, H + 0x16) == "mov eax, 0x115" and
            HB[H + 0x23].bytes == bytes.fromhex("663bd0") and HB[H + 0x26].bytes[:2] == b"\x0f\x87" and
            HB[H + 0x26].direct_target() == H + 0x148 and T(HB, H + 0x148) == "mov ecx, 0x116" and
            T(HB, H + 0x150) == "sub ax, cx" and T(HB, H + 0x153) == "mov ecx, 0x108" and
            HB[H + 0x158].bytes == bytes.fromhex("663bc1") and HB[H + 0x15B].bytes[0] == 0x77 and
            HB[H + 0x15B].direct_target() == H + 0x1D9)
    arm_path = sorted(set(HB.reach(H + 0x15D)))
    arm_w = [(a, m) for a, m in HB.mem_writes() if a in arm_path and m["base"] not in ("rsp",)]
    arm_calls = [a for a in arm_path if HB[a].mnemonic == "call"]
    R.check("the arm: R8 = the descriptor loaded at + 0xF (not rewritten before + 0x15D on the `ja` path); lookups "
            "+ 0x166 and + 0x17A; + 0x186 `movzx ebx, word ptr [rcx + 8]`, + 0x18D `imul ebx, ecx`, + 0x190 `add ebx, "
            "eax` (32-bit row); + 0x192 `test byte ptr [rbx + 0x2c], 0x40`, + 0x196 `je` + 0x1D9; + 0x1D9 `cmp di, 0x113` "
            "`jne` + 0x1F3 `xor eax, eax` / ret. With bit 6 clear the arm's calls are the two lookups only (0x113 is "
            "outside 278..542), and it writes nothing but its stack",
            rip_target(HB[H + 0xF]) == DESC and writers(HB, "r8", H + 0x10, H + 0x2C) == [] and
            T(HB, H + 0x166) == "call 0x20e600" and T(HB, H + 0x17A) == "call 0x20e600" and
            T(HB, H + 0x186) == "movzx ebx, word ptr [rcx + 8]" and T(HB, H + 0x18D) == "imul ebx, ecx" and
            T(HB, H + 0x190) == "add ebx, eax" and T(HB, H + 0x192) == "test byte ptr [rbx + 0x2c], 0x40" and
            HB[H + 0x196].direct_target() == H + 0x1D9 and HB[H + 0x196].mnemonic == "je" and
            T(HB, H + 0x1DE) == "cmp di, ax" and HB[H + 0x1E1].direct_target() == H + 0x1F3 and
            T(HB, H + 0x1F8) == "xor eax, eax" and
            set(a for a in arm_calls if a not in (H + 0x166, H + 0x17A)) == {H + 0x19E, H + 0x1C2, H + 0x1EE} and
            H + 0x19E not in HB.reach(H + 0x1D9) and not [a for a, m in arm_w if a in HB.reach(H + 0x1D9)],
            "arm writes %s" % ["+%X" % (a - H) for a, m in arm_w])
    # ---------------- the table
    n, st, off = struct.unpack_from("<IHxxI", tb, 4)
    b6 = [i for i in range(278, 543) if trow(tb, i)[0x2C] & 0x40]
    R.check("the retained US table: st2e header count 543, stride 60, data at + 0x20, 32612 bytes; rows 511..534 have "
            "+0x2C = 0 (bit 6 clear), +0x0C bit 30 set and +0x1E = 7; in 278..542 bit 6 is set only on rows "
            "325, 326, 416, 417, 436 and 455",
            tb[:4] == b"st2e" and (n, st, off) == (543, 60, 0x20) and len(tb) == 32612 and
            all(trow(tb, i)[0x2C] == 0 and bit30(tb, i) and trow(tb, i)[0x1E] == 7 for i in STOCK) and
            b6 == [325, 326, 416, 417, 436, 455], str(b6))
    caller_emu_checks(img, R, tb, small)
    builder_emu_checks(img, R, tb)
    helper_emu_checks(img, R, tb, small)


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


def census_checks(img, R):
    print("== raw direct-reference census (E8/E9 rel32 and 0F 8x jcc, .text)")
    rc = raw_refs(img, [F, B, H, SEQ, CB1, CB2])
    for t in (F, B, H, SEQ, CB1, CB2):
        R.note("%08X raw direct references (%d): %s" % (t, len(rc[t]), ", ".join(
            "%X %s (root %X)" % (a, k, root_of(img, a) or 0) for a, k in rc[t])))
    R.check("00304850 has one raw direct reference (00307C19 = 00307BE0 + 0x39); 0030D160, 00305430 and 00306760 each "
            "have exactly one, from 00304850 (+ 0x692, + 0x69E, + 0x6FD)",
            rc[F] == [(0x307C19, "call")] and root_of(img, 0x307C19) == 0x307BE0 and
            rc[B] == [(BUILDER_CALL, "call")] and rc[H] == [(HELPER_CALL, "call")] and rc[SEQ] == [(SEQ_CALL, "call")])


def git(*args):
    top = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True,
                         cwd=os.path.dirname(os.path.abspath(__file__))).stdout.strip()
    return subprocess.run(["git"] + list(args), capture_output=True, cwd=top).stdout


def git_member(commit, member):
    """git ls-tree -z then cat-file (avoids the long-path `git show` failure)."""
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
    R.note("committed manifest at 103aa3123: sha256 %s" % hashlib.sha256(cm).hexdigest())
    tot, bad = 0, []
    for fn in ("current-row-source-01.json", "current-row-source-02.json", "helper-source-01.json"):
        s = json.load(open(os.path.join(ev, fn)))
        for rg in s["ranges"]:
            a, e = int(rg["start"], 16), int(rg["end_exclusive"], 16)
            tot += 1
            ib = b"".join(bytes.fromhex(i["bytes"]) for i in rg["instructions"])
            if hashlib.sha256(img.read(a, e - a)).hexdigest() != rg["sha256"] or ib != img.read(a, e - a):
                bad.append("%s %X" % (fn, a))
    R.check("every source range of current-row-source-01/02 and helper-source-01 (%d ranges) hashes to this image's "
            "bytes and its instruction records concatenate to them" % tot, not bad and tot > 0, str(bad))
    hs = json.load(open(os.path.join(ev, "helper-source-01.json")))
    R.check("helper-source-01's two ranges are 00305430 .. + 0x205 and 0030D160 .. + 0x3EC",
            sorted((int(r["start"], 16), int(r["end_exclusive"], 16)) for r in hs["ranges"]) == [(H, H_END), (B, B_END)])
    cr = json.load(open(os.path.join(ev, "current-row-source-01.json")))
    cov = sorted((int(r["start"], 16), int(r["end_exclusive"], 16)) for r in cr["ranges"])
    R.note("current-row-source-01 ranges: %s" % ", ".join("%X..%X" % x for x in cov))
    hx = json.load(open(os.path.join(ev, "helper-extents-01.json")))
    okx = hx["complete"]
    for b in hx["bodies"]:
        e0 = int(b["entry"], 16)
        ents, ok = img.pdata_cover(e0, int(b["end_exclusive"], 16))
        okx = okx and ok and [(int(r["begin"], 16), int(r["end_exclusive"], 16)) for r in b["records"]] == \
            [(x[0], x[1]) for x in ents] and hashlib.sha256(img.read(e0, b["bytes"])).hexdigest() == b["sha256"]
    R.check("helper-extents-01's two bodies equal this image's .pdata records and bytes (517 B and 1004 B)",
            okx and sorted(b["bytes"] for b in hx["bodies"]) == [517, 1004])
    lin = [("current-row-source-01.json", "fd45553c7d715dbe3e9e1a919b7961114f0df8e4",
            P + "autoattack-commit-exception/retained/current-row-source-01.json"),
           ("current-row-source-02.json", "fd45553c7d715dbe3e9e1a919b7961114f0df8e4",
            P + "autoattack-commit-exception/retained/current-row-source-02.json"),
           ("carrier-manifest.json", "c40b243400bea566a89600d77e4d12cc3440a1cd", P + "summon-kind-row-carrier/manifest.json"),
           ("carrier-result-01.json", "c40b243400bea566a89600d77e4d12cc3440a1cd", P + "summon-kind-row-carrier/result-01.json"),
           ("action_data_us.st2e", "c40b243400bea566a89600d77e4d12cc3440a1cd",
            P + "summon-kind-row-carrier/retained/action-selector-local-exclusions-special-action-frozen-ready--"
            "action-selectors-01--tables--action_data_us.st2e")]
    bad = []
    for copy, c, m in lin:
        b = git_member(c, m)
        if b is None or b != open(os.path.join(ev, copy), "rb").read():
            bad.append(copy)
    R.check("retained lineage: current-row-source-01/02 are byte-identical to fd45553c's autoattack-commit-exception "
            "members, and carrier-manifest, carrier-result-01 and action_data_us.st2e to c40b24340's members (git ls-tree "
            "+ cat-file)", not bad, str(bad))
    tb = R.table
    if os.path.exists(EXTRACT):
        d = open(EXTRACT, "rb").read()
        i = d.find(tb)
        R.check("action_data_us.st2e is the byte-identical slice of the shipped US battle_pack.bin at offset 78352 (game "
                "extract on D:)", i == 78352 and d.count(b"st2e\x1f\x02\x00\x00<\x00") == 1, "offset %d" % i)
    else:
        R.note("game extract not present; the st2e was not compared with the shipped battle_pack.bin")
    res = json.load(open(os.path.join(ev, "result-01.json")))
    te = res["facts"]["terminal_entry"]
    R.check("result-01's terminal entries: phase 8 -> 0x304eb3 (161 visited), phase 9 -> 0x304ebe (158), builder dominates "
            "the sequence, no earlier readiness call - equal to this review's reading",
            [(x["entry_phase"], int(x["dispatch_target"], 16), x["visited"], x["target_builder_dominates_sequence"],
              x["earlier_slot_readiness_calls"]) for x in te] == [(8, PH8, 161, True, []), (9, PH9, 158, True, [])])
    sh = res["facts"]["stock_helper"]["cases"]
    R.check("result-01's 24 stock cases (511..534: +0x2C 0, return 0, calls [0020E600, 0020E600], no own non-stack "
            "writes) equal this review's table reading and emulation",
            [x["id"] for x in sh] == STOCK and all(x["row_byte_2c"] == trow(tb, x["id"])[0x2C] == 0 and
                                                   x["helper_return"] == 0 and x["calls"] == ["0x20e600", "0x20e600"]
                                                   and x["own_nonstack_writes"] == [] for x in sh))
    rd = " ".join(open(os.path.join(ev, "README.md"), encoding="utf-8").read().split())
    R.check("packet README keeps natural pairing, initialization and opaque helper interference open and forbids closing "
            "OV-42 or inferring natural impossibility",
            "Natural pairing, initialization and opaque helper interference are still open" in rd and
            "Do not close allOV42 or infer natural impossibility" in rd)


def u32le(v):
    return struct.pack("<I", v & 0xFFFFFFFF)


CONTROLS = [
    ("caller + 0x68C `movzx edx, ax` -> `mov edx, eax` + NOP (builder gets the full EAX)", F + 0x68C,
     bytes.fromhex("8bd090")),
    ("caller + 0x697 `movzx edx, r13w` -> `movzx edx, ax` + NOP (helper gets RAX, not the latched word)", F + 0x697,
     bytes.fromhex("0fb7d090")),
    ("caller + 0x6F7 `mov rdx, r15` -> `mov rdx, r14` (sequence gets 0)", F + 0x6F7, bytes.fromhex("498bd6")),
    ("caller + 0x6A3 `movabs rax` -> `test eax, eax` / `jne` + 0x7BA (the helper's return tested)", F + 0x6A3,
     bytes.fromhex("85c00f85") + u32le(0x7BA - 0x6AB) + bytes.fromhex("6690")),
    ("caller + 0x3D latch WORD [rsi + 0x64] -> [rsi + 0x66]", F + 0x41, bytes([0x66])),
    ("caller phase entry 9 -> + 0x5DC (the phase-7 entry, which calls 0030CA80)", TBLOFF + 36, u32le(F + 0x5DC - 0x120000)),
    ("caller + 0x92 entry guard `ja` -> `jae`", F + 0x93, bytes([0x83])),
    ("caller + 0x6B9 `cmp r13w, 0x21` -> 0x22 (the D0..F1 skip widened)", F + 0x6BD, bytes([0x22])),
    ("caller + 0xE4 `add r15d, ecx` -> `add r15d, eax` (row = base + id)", F + 0xE4, bytes.fromhex("4403f8")),
    ("builder + 0x27 `movzx edi, dx` -> `mov edi, r8d`", B + 0x27, bytes.fromhex("418bf8")),
    ("builder + 0x21 `mov r15, r9` -> `mov r9, r15` (the caller's R15 read)", B + 0x21, bytes.fromhex("4d8bcf")),
    ("helper + 0x196 `je` + 0x1D9 -> `jne` (bit 6 inverted)", H + 0x196, bytes([0x75])),
    ("helper + 0x1E1 `jne` + 0x1F3 -> `je`", H + 0x1E1, bytes([0x74])),
    ("helper arm base 0x116 -> 0x200 (+ 0x148 `mov ecx, 0x200`)", H + 0x149, u32le(0x200)),
]


def main():
    img = Img.load()
    R = Rep("rv_callerrow")
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
    P0 = img.patched(F + 0x10, img.read(F + 0x10, 3))
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
    # a table control: a private copy of the US table with row 520's +0x2C bit 6 set
    tb2 = bytearray(R.table)
    tb2[0x20 + 60 * 520 + 0x2C] |= 0x40
    Rc = Rep("table")
    Rc.quiet = True
    Rc.table = bytes(tb2)
    P1 = img.patched(F + 0x10, img.read(F + 0x10, 3))
    P1._private = True
    checks(P1, Rc, small=True)
    nctl += 1
    R.check("control: table copy, row 520 +0x2C bit 6 set", Rc.fails > 0,
            "%d failed: %s" % (Rc.fails, "; ".join(f[:60] for f in Rc.failed[:3])))
    disk = hashlib.sha256(open(find_exe(), "rb").read()).hexdigest()
    R.check("exe on disk still hashes to the pinned sha256 after all controls", disk == SHA_PIN, disk)
    print("TOTAL: %d checks, %d PASS, %d FAIL (%d controls)" % (R.n, R.n - R.fails, R.fails, nctl))


if __name__ == "__main__":
    main()
