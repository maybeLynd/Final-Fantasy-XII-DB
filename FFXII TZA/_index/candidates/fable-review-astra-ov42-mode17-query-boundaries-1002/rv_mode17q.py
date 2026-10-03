"""rv_mode17q.py - FABLE independent re-derivation for ASTRA publication ov42-mode17-query-boundaries
(7b4e2b92c, OV-42): the two evidence folders ov42-resource-mutator-mode17 and ov42-resource-eligibility-domain.

Own reader (rvlib.py: struct + capstone 5, copied unchanged from the kind-row review, sha256 69f9bc40be32abcc...).
Does not import or run ASTRA's prove.py, prove_owner_reload_order.py, prove-before-*.py, qualify-singleton*.py,
capture*.py, prepare-*.py, control.py, run.py, validate-title-source-annotations.py or the shared role adapter
(reg_tracking.py).

Method:
  * image sha256; .pdata extents and exact linear decode of the primary and secondary resource modifiers 00300CE0
    and 00300BC0, the global and unit eligibility queries 0030B770 and 0030B7F0, the C20 getter 0017D470, the
    singleton accessor 001D50D0 and the retained constructor 001CCB20;
  * instruction-level reads: flag decoding, the entry and late query legs, the vetoes, the stores and the order of
    calls; the queries' complete store lists; the accessor's fast and NULL paths; the constructor's own C20 store
    and the calls after it;
  * a concrete emulation (unicorn) of the ORIGINAL queries, getter and accessor (run from the image), and of the
    ORIGINAL modifiers with their outside callees stubbed (31B860, 3283D0, 28F1F0, 2FA540, 300BC0 / 30E060,
    210EC0, 1CCB20): every global-query input bit at eight stack alignments over a 0xFF-filled stack; a grid of
    unit-query states; two different C20 reads; the lazy path, a NULL allocation, and a constructor whose return
    differs from the allocation; the modifier's call / store order in mode 17, 16, 1 and 0x91;
  * raw E8/E9 rel32 and 0F 8x census for the bodies; disp32 census of the singleton root 01F81428;
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
from rvlib import Img, Body, Report, find_exe, SHA256 as SHA_PIN  # noqa: E402
from capstone.x86 import X86_OP_MEM  # noqa: E402

PRODUCER = "7b4e2b92cc1e33177baf166812827ad16356600c"
MUT, ELIG = "ov42-resource-mutator-mode17", "ov42-resource-eligibility-domain"
NAMED_RECORD = "ov42-mode17-query-boundaries"
PRIM, PRIM_END = 0x00300CE0, 0x00300E3F
SEC, SEC_END = 0x00300BC0, 0x00300C8F
GQ, GQ_END = 0x0030B770, 0x0030B7E7
UQ, UQ_END = 0x0030B7F0, 0x0030B8D2
GET, GET_END = 0x0017D470, 0x0017D484
ACC, ACC_END = 0x001D50D0, 0x001D5112
ACC2, ACC2_END = 0x001D5090, 0x001D50D0
CTOR, CTOR_END = 0x001CCB20, 0x001CCFDA
CALLER = 0x00305640
OWNER_OF, PUB_A, PUB_B, ACCUM, SECCB, ALLOC = 0x0031B860, 0x003283D0, 0x0028F1F0, 0x002FA540, 0x0030E060, 0x00210EC0
ROOT = 0x01F81428
GFLAGS, GBYTE, STATE = 0x02089340, 0x022C2158, 0x022C2160
U, P, S, X = 0x41000000, 0x42000000, 0x43000000, 0x44000000


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


def rip_target(I):
    for m in I.mems:
        if m["base"] == "rip":
            return I.address + I.size + m["disp"]
    return None


def all_writes(B):
    return [(a, m) for a in B.order for m in B[a].mems if m["write"] and B[a].mnemonic not in ("push", "call")]


# ------------------------------------------------------------------ emulation of the original code
class Emu(object):
    STK, RET = 0x7F000000, 0x7E000000

    def __init__(self, img, code_ranges, data_pages=(), scratch=(), stubs=(), watch=()):
        from unicorn import Uc, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE, UC_HOOK_MEM_WRITE, UC_HOOK_MEM_READ
        from unicorn import UC_HOOK_INTR, UC_HOOK_MEM_READ_UNMAPPED, UC_HOOK_MEM_FETCH_UNMAPPED
        from unicorn import UC_HOOK_MEM_WRITE_UNMAPPED
        from unicorn import x86_const as X
        self.X = X
        mu = self.mu = Uc(UC_ARCH_X86, UC_MODE_64)
        cpages = set()
        for s, e in list(code_ranges) + [(c, c + 1) for c in stubs]:
            for p in range(s & ~0xFFF, (e + 0xFFF) & ~0xFFF, 0x1000):
                cpages.add(p)
        for p in sorted(cpages):
            mu.mem_map(p, 0x1000)
            mu.mem_write(p, img.read(p, 0x1000))
        self.zero = []
        for p in sorted(set(x & ~0xFFF for x in data_pages) - cpages):
            mu.mem_map(p, 0x1000)
            self.zero.append((p, 0x1000))
        for a, n in scratch:
            mu.mem_map(a, n)
            self.zero.append((a, n))
        mu.mem_map(self.STK, 0x10000)
        mu.mem_map(self.RET, 0x1000)
        self.code_ranges = list(code_ranges)
        self.stubs = set(stubs)
        self.watch = set(watch)
        self.stub_rax = {}
        self.cb = {}
        self.until = None

        def ch(uc, addr, size, ud):
            if addr == self.until:
                uc.emu_stop()
                return
            if addr in self.watch or addr in self.stubs:
                self.events.append(("C", addr, uc.reg_read(X.UC_X86_REG_RCX), uc.reg_read(X.UC_X86_REG_RDX),
                                    uc.reg_read(X.UC_X86_REG_R8), uc.reg_read(X.UC_X86_REG_R9)))
                self.count[addr] = self.count.get(addr, 0) + 1
            if addr in self.cb:
                self.cb[addr](self, self.count.get(addr, 0))
            if addr in self.stubs:
                rsp = uc.reg_read(X.UC_X86_REG_RSP)
                v = self.stub_rax.get(addr, 0)
                uc.reg_write(X.UC_X86_REG_RAX, v(self) if callable(v) else v)
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
            rec = (uc.reg_read(X.UC_X86_REG_RIP), addr, size, value & ((1 << (8 * size)) - 1))
            self.allw.append(rec)
            if not (self.STK <= addr < self.STK + 0x10000):
                self.events.append(("W",) + rec)

        def rh(uc, access, addr, size, value, ud):
            if not (self.STK <= addr < self.STK + 0x10000):
                self.reads.append((uc.reg_read(X.UC_X86_REG_RIP), addr, size))

        def ih(uc, intno, ud):
            self.intr = (intno, uc.reg_read(X.UC_X86_REG_RIP))
            uc.emu_stop()

        mu.hook_add(UC_HOOK_CODE, ch)
        mu.hook_add(UC_HOOK_MEM_READ_UNMAPPED | UC_HOOK_MEM_FETCH_UNMAPPED | UC_HOOK_MEM_WRITE_UNMAPPED, bad)
        mu.hook_add(UC_HOOK_MEM_WRITE, wh)
        mu.hook_add(UC_HOOK_MEM_READ, rh)
        mu.hook_add(UC_HOOK_INTR, ih)

    def reset(self):
        for a, n in self.zero:
            self.mu.mem_write(a, b"\0" * n)

    def w8(self, a, v):
        self.mu.mem_write(a, bytes([v & 0xFF]))

    def w16(self, a, v):
        self.mu.mem_write(a, struct.pack("<H", v & 0xFFFF))

    def w32(self, a, v):
        self.mu.mem_write(a, struct.pack("<I", v & 0xFFFFFFFF))

    def w64(self, a, v):
        self.mu.mem_write(a, struct.pack("<Q", v & 0xFFFFFFFFFFFFFFFF))

    def u16(self, a):
        return struct.unpack("<H", bytes(self.mu.mem_read(a, 2)))[0]

    def u64(self, a):
        return struct.unpack("<Q", bytes(self.mu.mem_read(a, 8)))[0]

    def run(self, start, until=None, sp_adj=0, fill=None, **regs):
        from unicorn import UcError
        X = self.X
        if fill is not None:
            self.mu.mem_write(self.STK, bytes([fill]) * 0x10000)
        sp = self.STK + 0x8000 - sp_adj
        self.sp = sp
        self.mu.mem_write(sp, struct.pack("<Q", self.RET))
        self.mu.reg_write(X.UC_X86_REG_RSP, sp)
        base = {"rax": 0xAAAAAAAAAAAAAAAA, "rbx": 0xBBBBBBBBBBBBBBBB, "rbp": 0xB0B0B0B0B0B0B0B0,
                "rsi": 0x5151515151515151, "rdi": 0xDDDDDDDDDDDDDDDD, "r8": 0, "r9": 0x9999999999999999,
                "r12": 0x1212121212121212, "r13": 0x1313131313131313, "r14": 0xEEEEEEEEEEEEEEEE,
                "r15": 0xF0F0F0F0F0F0F0F0, "rcx": 0, "rdx": 0}
        base.update(regs)
        for k, v in base.items():
            self.mu.reg_write(getattr(X, "UC_X86_REG_" + k.upper()), v)
        self.events, self.allw, self.reads, self.count = [], [], [], {}
        self.intr, self.fault, self.left = None, None, None
        self.until = self.RET if until is None else until
        try:
            self.mu.emu_start(start, self.until, count=200000)
        except UcError as e:
            if self.intr is None and self.fault is None:
                self.fault = "UcError %s" % e
        r = dict((k, self.mu.reg_read(getattr(X, "UC_X86_REG_" + k.upper())))
                 for k in ("rax", "rbx", "rsi", "rdi", "rbp", "r12", "r13", "r14", "r15", "rip", "rsp"))
        r["events"], r["allw"], r["reads"] = list(self.events), list(self.allw), list(self.reads)
        r["intr"], r["fault"], r["left"], r["sp"] = self.intr, self.fault, self.left, sp
        r["ok"] = (r["rip"] == self.until and not r["fault"] and not r["intr"] and not r["left"])
        return r


DATA = [GFLAGS, GBYTE, ROOT]
SCR = [(U, 0x1000), (P, 0x1000), (S, 0x2000), (X, 0x2000)]
QUERY_CODE = [(GQ, GQ_END), (UQ, UQ_END), (GET, GET_END), (ACC, ACC_END)]


def query_emu(img):
    return Emu(img, QUERY_CODE, data_pages=DATA, scratch=SCR, stubs=[ALLOC, CTOR], watch=[GET, ACC])


def gformula(ecx, byte):
    v = 1 if ecx & 0x3080 else 0
    v |= 2 if byte & 1 else 0
    v |= 4 if ecx & (1 << 10) else 0
    v |= 8 if ecx & (1 << 9) else 0
    v |= 0x10 if ecx & (1 << 11) else 0
    return v


def uformula(unit, flags, b4, stats, s5, s4, v1, v2, edx, state):
    if not unit or not (flags & 0x10):
        return 0
    lo = 0
    if b4 & 0x20 and not (((state - 5) & 0xFFFFFFFF) <= 1):
        lo |= 8
    lo |= 1 if flags & (1 << 8) else 0
    lo |= 2 if (flags & (1 << 30)) and edx else 0
    lo |= 0x10 if stats and s5 == 0 and s4 == 0x1A else 0
    hi = (1 if (v1 == 1 and stats and s5 == 0) else 0) | (2 if v2 == 2 else 0)
    return (hi << 16) | lo


def set_unit(E, flags, b4, stats, s5, s4, state, owner8=0x1234):
    E.w32(U, flags)
    E.w8(U + 4, b4)
    E.w32(U + 8, owner8)
    E.w64(U + 0x698, P if stats else 0)
    E.w8(P + 4, s4)
    E.w8(P + 5, s5)
    E.w32(STATE, state)


def run_uq(E, unit, flags, b4, stats, s5, s4, v1, v2, edx, state, root=S):
    E.reset()
    set_unit(E, flags, b4, stats, s5, s4, state)
    E.w64(ROOT, root)
    E.w32(S + 0xC20, v1)
    E.cb = {}
    if v2 != v1:
        def second(e, n):
            if n == 2:
                e.w32(S + 0xC20, v2)
        E.cb[GET] = second
    return E.run(UQ, rcx=U if unit else 0, rdx=edx | 0xABCD000000000000)


def query_results(img, small=False):
    o = {}
    E = query_emu(img)
    # ---- global query: every input bit, eight stack alignments, a 0xFF-filled stack
    rnd = random.Random(5)
    bad, n = [], 0
    bits = [7, 12, 13, 9, 10, 11]
    for combo in range(0, 128, 1 if not small else 9):
        ecx = sum(1 << b for i, b in enumerate(bits) if combo >> i & 1)
        byte = combo >> 6 & 1
        for adj in range(0, 64, 8):
            junk = rnd.getrandbits(32) & ~sum(1 << b for b in bits)
            E.reset()
            E.w32(GFLAGS, ecx | junk)
            E.w8(GBYTE, byte | (rnd.getrandbits(8) & 0xFE))
            r = E.run(GQ, sp_adj=adj, fill=0xFF)
            n += 1
            got = r["rax"] & 0xFFFFFFFF
            if not r["ok"] or got >> 16 != 0 or got != gformula(ecx | junk, byte) or r["events"]:
                bad.append("ecx %X byte %d adj %d -> %X" % (ecx | junk, byte, adj, got))
    o["gq"] = (n, bad)
    # ---- unit query grid, one C20 value read twice through the initialized fast path
    bad, n, hi_seen, reads_bad = [], 0, set(), []
    grid = []
    for unit in (0, 1):
        for flags in (0, 0x10, 0x10 | 0x100 | 0x40000000):
            for b4 in (0, 0x20):
                for stats in (0, 1):
                    for s5 in (0, 1):
                        for s4 in (0, 0x1A):
                            for v in (0, 1, 2, 3, 0x101, 0xFFFFFFFF):
                                for edx in (0, 1):
                                    for state in (0, 5, 6):
                                        grid.append((unit, flags, b4, stats, s5, s4, v, edx, state))
    if small:
        grid = random.Random(3).sample(grid, 300)
    for g in grid:
        unit, flags, b4, stats, s5, s4, v, edx, state = g
        r = run_uq(E, unit, flags, b4, stats, s5, s4, v, v, edx, state)
        n += 1
        got = r["rax"] & 0xFFFFFFFF
        want = uformula(unit, flags, b4, stats, s5, s4, v, v, edx, state)
        if not r["ok"] or got != want:
            bad.append("%s -> %X want %X" % (g, got, want))
        hi_seen.add(got >> 16)
        c20 = [(x[0], x[2]) for x in r["reads"] if x[1] == S + 0xC20]
        nonstack = [e for e in r["events"] if e[0] == "W"]
        calls = [e[1] for e in r["events"] if e[0] == "C"]
        eligible = unit and flags & 0x10
        if eligible and (c20 != [(GET + 9, 4), (GET + 9, 4)] or nonstack or calls != [GET, ACC, GET, ACC]):
            reads_bad.append("%s c20 %s w %d calls %s" % (g, c20, len(nonstack), calls))
        if not eligible and (c20 or calls):
            reads_bad.append("%s ineligible but c20 %s calls %s" % (g, c20, calls))
    o["uq"] = (n, bad, sorted(hi_seen), reads_bad)
    # ---- two different reads
    tab, bad = {}, []
    for v1 in (0, 1, 2, 3):
        for v2 in (0, 1, 2, 3):
            r = run_uq(E, 1, 0x10, 0, 1, 0, 0, v1, v2, 0, 0)
            got = (r["rax"] & 0xFFFFFFFF) >> 16
            tab[(v1, v2)] = got
            if got != (1 if v1 == 1 else 0) | (2 if v2 == 2 else 0) or not r["ok"]:
                bad.append((v1, v2, got))
    o["two"] = (tab, bad)
    # ---- the packet's four conditional-control rows, through the original bytes
    rows = []
    for eligible, first, second, stats0 in ((True, 1, 1, True), (True, 2, 2, False), (True, 1, 2, True),
                                            (False, 1, 2, True)):
        r = run_uq(E, 1, 0x10 if eligible else 0, 0, 1, 0 if stats0 else 1, 0, first, second, 0, 0)
        rows.append((eligible, first, second, stats0, (r["rax"] & 0xFFFFFFFF) >> 16))
    o["rows"] = rows
    # ---- lazy path, NULL allocation, constructor return != allocation
    lz = {}
    for label, alloc_ret, ctor_ret in (("lazy", X, X), ("nullalloc", 0, 0), ("ctor-other", X, X + 0x1000)):
        E.reset()
        set_unit(E, 0x10, 0, 1, 0, 0, 0)
        E.w64(ROOT, 0)
        E.w32(X + 0xC20, 2)
        E.w32(X + 0x1000 + 0xC20, 1)
        E.cb = {}
        E.stub_rax = {ALLOC: alloc_ret, CTOR: ctor_ret}
        r = E.run(UQ, rcx=U, rdx=0)
        lz[label] = dict(r=r, root=E.u64(ROOT), calls=[(e[1], e[2]) for e in r["events"] if e[0] == "C" and
                                                       e[1] in (ALLOC, CTOR)],
                         rootw=[(e[1], e[4]) for e in r["events"] if e[0] == "W" and e[2] == ROOT])
    E.stub_rax = {}
    o["lazy"] = lz
    return o


PRIM_STUBS = [OWNER_OF, PUB_A, PUB_B, ACCUM, SEC, ALLOC, CTOR]


def prim_emu(img, stub_gq=False):
    code = [(PRIM, PRIM_END), (UQ, UQ_END), (GET, GET_END), (ACC, ACC_END)]
    stubs = list(PRIM_STUBS)
    if stub_gq:
        stubs.append(GQ)
    else:
        code.append((GQ, GQ_END))
    return Emu(img, code, data_pages=DATA, scratch=SCR, stubs=stubs, watch=[GQ, UQ])


def run_prim(E, flags, delta, v=0, s5=0, eligible=True, owner=True, gq_ret=None):
    E.reset()
    set_unit(E, 0x10 if eligible else 0, 0, 1, s5, 0, 0)
    E.w16(P + 0x4C, 50)
    E.w16(P + 0x28, 99)
    E.w64(ROOT, S)
    E.w32(S + 0xC20, v)
    E.cb = {}
    E.stub_rax = {OWNER_OF: U if owner else 0}
    if gq_ret is not None:
        E.stub_rax[GQ] = gq_ret
    r = E.run(PRIM, rcx=P, rdx=delta & 0xFFFFFFFF, r8=flags)
    seq = []
    for e in r["events"]:
        if e[0] == "C" and e[1] in (OWNER_OF, PUB_A, PUB_B, GQ, UQ, ACCUM, SEC):
            seq.append(("%X" % e[1]))
        elif e[0] == "W" and e[2] == P + 0x4C:
            seq.append("W4C=%d" % e[4])
    r["seq"] = seq
    r["args"] = dict((e[1], (e[2], e[3] & 0xFFFFFFFF, e[4] & 0xFFFFFFFF, e[5] & 0xFFFFFFFF))
                     for e in r["events"] if e[0] == "C")
    r["mp"] = E.u16(P + 0x4C)
    return r


def prim_results(img):
    o = {}
    E = prim_emu(img)
    o["a"] = run_prim(E, 0x11, -10, v=0)
    o["b"] = run_prim(E, 0x11, -10, v=1, s5=0)
    o["c"] = run_prim(E, 0x11, -10, v=2)
    o["d"] = run_prim(E, 0x11, -10, v=1, s5=1)
    o["e"] = run_prim(E, 0x11, -10, v=2, eligible=False)
    o["g"] = run_prim(E, 0x10, -10, v=0)
    o["h"] = run_prim(E, 0x11, 10, v=2)
    o["i1"] = run_prim(E, 0x01, -10, v=0)
    o["i2"] = run_prim(E, 0x91, -10, v=0)
    o["j"] = run_prim(E, 0x11, -10, v=2, owner=False)
    # the frame: the global result saved at the modifier's RDX home slot survives the unit-query call
    a = o["a"]
    home = a["sp"] + 0x10
    o["home"] = [(w[0], w[3]) for w in a["allw"] if home <= w[1] < home + 4]
    Ei = prim_emu(img, stub_gq=True)
    o["f"] = run_prim(Ei, 0x11, -10, v=0, gq_ret=0x10000)
    o["f0"] = run_prim(Ei, 0x11, -10, v=0, gq_ret=0x1F)
    return o


def sec_results(img):
    E = Emu(img, [(SEC, SEC_END), (GQ, GQ_END), (UQ, UQ_END), (GET, GET_END), (ACC, ACC_END)], data_pages=DATA,
            scratch=SCR, stubs=[OWNER_OF, SECCB, ALLOC, CTOR], watch=[GQ, UQ])
    out = {}
    for flags in (0x11, 0x10):
        E.reset()
        set_unit(E, 0x10, 0, 1, 0, 0, 0)
        E.w16(P + 6, 20)
        E.w16(P + 0x28, 99)
        E.w64(ROOT, S)
        E.stub_rax = {OWNER_OF: U}
        r = E.run(SEC, rcx=P, rdx=(-5) & 0xFFFFFFFF, r8=flags)
        seq = []
        for e in r["events"]:
            if e[0] == "C" and e[1] in (OWNER_OF, GQ, UQ, SECCB):
                seq.append("%X" % e[1])
            elif e[0] == "W" and e[2] == P + 6:
                seq.append("W6=%d" % e[4])
        cb = [(e[2], e[3] & 0xFFFFFFFF) for e in r["events"] if e[0] == "C" and e[1] == SECCB]
        out[flags] = dict(ok=r["ok"], seq=seq, cb=cb)
    return out


# ------------------------------------------------------------------ image checks (also run on the controls)
def checks(img, R, small=False):
    R.check("image sha256 = %s..." % SHA_PIN[:20], hashlib.sha256(img.d).hexdigest() == SHA_PIN or
            getattr(img, "_private", False))
    ext = {}
    for nm, s, e in (("primary", PRIM, PRIM_END), ("secondary", SEC, SEC_END), ("global", GQ, GQ_END),
                     ("unit", UQ, UQ_END), ("getter", GET, GET_END), ("accessor", ACC, ACC_END),
                     ("ctor", CTOR, CTOR_END), ("twin", ACC2, ACC2_END)):
        ents, ok = img.pdata_cover(s, e)
        ext[nm] = (ok, len(ents), Body(img, s, e).exact, e - s)
    R.check(".pdata extents tile and decode exactly: primary 00300CE0 351 B (1 record), secondary 00300BC0 207 B (3 "
            "chained), global query 0030B770 119 B, unit query 0030B7F0 226 B, getter 0017D470 20 B, accessor 001D50D0 "
            "66 B, constructor 001CCB20 1210 B, twin accessor 001D5090 64 B",
            ext == {"primary": (True, 1, True, 351), "secondary": (True, 3, True, 207), "global": (True, 1, True, 119),
                    "unit": (True, 1, True, 226), "getter": (True, 1, True, 20), "accessor": (True, 1, True, 66),
                    "ctor": (True, 1, True, 1210), "twin": (True, 1, True, 64)}, str(ext))
    # ---------------- global query
    G = Body(img, GQ, GQ_END)
    gw = [(a - GQ, m["base"], m["disp"], m["size"]) for a, m in all_writes(G)]
    R.check("global query: no call; its stores are exactly `mov dword ptr [rbp], 0` (+ 0x15) and five `mov word ptr "
            "[rbp], ax` (+ 0x29, + 0x40, + 0x4E, + 0x5C, + 0x6A); RBP = (RSP + 0x40) & ~0x3F, set once; it returns "
            "DWORD [rbp] (+ 0x6E) - the upper WORD is written only by the zeroing DWORD store",
            not G.calls() and gw == [(0x15, "rbp", 0, 4), (0x29, "rbp", 0, 2), (0x40, "rbp", 0, 2), (0x4E, "rbp", 0, 2),
                                     (0x5C, "rbp", 0, 2), (0x6A, "rbp", 0, 2)] and
            T(G, GQ + 0x15) == "mov dword ptr [rbp], 0" and T(G, GQ + 0x6) == "lea rbp, [rsp + 0x40]" and
            T(G, GQ + 0xB) == "and rbp, 0xffffffffffffffc0" and writers(G, "rbp", GQ + 0xC, GQ + 0x71) == [] and
            T(G, GQ + 0x6E) == "mov eax, dword ptr [rbp]" and rip_target(G[GQ + 0xF]) == GFLAGS and
            rip_target(G[GQ + 0x33]) == GBYTE, str(gw))
    # ---------------- unit query
    Q = Body(img, UQ, UQ_END)
    qw = [(a - UQ, m["base"], m["disp"], m["size"]) for a, m in all_writes(Q)]
    R.check("unit query: its stores are the DWORD 0 at [rsp + 0x30] (+ 0x6), WORD stores to [rsp + 0x30] (+ 0x40, "
            "+ 0x57, + 0x6B, + 0x8E) and WORD stores to [rsp + 0x32] only at + 0xBA and + 0xD3; its only calls are "
            "two to 0017D470 (+ 0x93, + 0xC6); NULL unit (+ 0x14) or DWORD bit 4 clear (+ 0x1D / + 0x21) returns the "
            "zeroed DWORD before either call",
            qw == [(0x6, "rsp", 0x30, 4), (0x40, "rsp", 0x30, 2), (0x57, "rsp", 0x30, 2), (0x6B, "rsp", 0x30, 2),
                   (0x8E, "rsp", 0x30, 2), (0xBA, "rsp", 0x32, 2), (0xD3, "rsp", 0x32, 2)] and
            Q.calls() == [(UQ + 0x93, GET), (UQ + 0xC6, GET)] and Q[UQ + 0x14].direct_target() == UQ + 0xD8 and
            T(Q, UQ + 0x1D) == "test r8b, 0x10" and Q[UQ + 0x21].direct_target() == UQ + 0xD8 and
            T(Q, UQ + 0xD8) == "mov eax, dword ptr [rsp + 0x30]", str(qw))
    R.check("unit query upper WORD: first read `cmp eax, 1` (+ 0x98), then [unit + 0x698] nonNULL (+ 0xA4) and its "
            "byte +5 == 0 (+ 0xA9 .. + 0xAF) -> `or bx, 1`; second read `cmp eax, 2` (+ 0xCB) -> `or bx, ax`; RBX "
            "holds the unit across the first call and the WORD across the second (Win64 nonvolatile)",
            T(Q, UQ + 0x98) == "cmp eax, 1" and Q[UQ + 0x9B].direct_target() == UQ + 0xC1 and
            T(Q, UQ + 0x9D) == "mov rax, qword ptr [rbx + 0x698]" and T(Q, UQ + 0xA9) == "movzx eax, byte ptr [rax + 5]"
            and Q[UQ + 0xAF].direct_target() == UQ + 0xC1 and T(Q, UQ + 0xB6) == "or bx, 1" and
            T(Q, UQ + 0xCB) == "cmp eax, 2" and Q[UQ + 0xCE].direct_target() == UQ + 0xD8 and
            T(Q, UQ + 0xD0) == "or bx, ax")
    R.check("the low-WORD arm that needs a nonzero EDX: + 0x5C `bt r8d, 0x1e`, + 0x63 `test edx, edx` -> `or cx, 2`; "
            "the primary modifier zeroes EDX before both of its unit-query calls (+ 0x6B, + 0x102 `xor edx, edx`)",
            T(Q, UQ + 0x5C) == "bt r8d, 0x1e" and T(Q, UQ + 0x63) == "test edx, edx" and
            T(Q, UQ + 0x67) == "or cx, 2" and T(Body(img, PRIM, PRIM_END), PRIM + 0x6B) == "xor edx, edx" and
            T(Body(img, PRIM, PRIM_END), PRIM + 0x102) == "xor edx, edx")
    # ---------------- getter / accessor
    g = Body(img, GET, GET_END)
    R.check("getter 0017D470: `call 001D50D0` then `mov eax, dword ptr [rax + 0xc20]` (4 B) and return",
            T(g, GET + 4) == "call 0x1d50d0" and T(g, GET + 9) == "mov eax, dword ptr [rax + 0xc20]" and
            g[GET + 9].mems[0]["size"] == 4)
    A = Body(img, ACC, ACC_END)
    aw = [(a - ACC, m["base"], m["size"]) for a, m in all_writes(A)]
    R.check("accessor 001D50D0: + 0xD loads QWORD 01F81428; nonNULL -> + 0x3D epilogue (only the stack store + 0x4 "
            "on that path); NULL -> `mov ecx, 0x10e8`, `call 00210EC0`, nonNULL result -> `call 001CCB20` with RCX = "
            "the allocation, then + 0x36 stores RAX to 01F81428 (on the NULL path only)",
            rip_target(A[ACC + 0xD]) == ROOT and A[ACC + 0x17].direct_target() == ACC + 0x3D and
            T(A, ACC + 0x19) == "mov ecx, 0x10e8" and T(A, ACC + 0x1E) == "call 0x210ec0" and
            A[ACC + 0x2B].direct_target() == ACC + 0x36 and T(A, ACC + 0x2D) == "mov rcx, rax" and
            T(A, ACC + 0x30) == "call 0x1ccb20" and rip_target(A[ACC + 0x36]) == ROOT and
            T(A, ACC + 0x36).endswith(", rax") and ACC + 0x36 not in A.reach(ACC + 0x3D) and
            [x for x in aw if x[1] != "rsp"] == [(0x36, "rip", 8)] and
            not [a for a in A.reach(ACC + 0x3D) if A[a].mnemonic == "call"], str(aw))
    # ---------------- constructor
    Cn = Body(img, CTOR, CTOR_END)
    c20 = [a for a, m in all_writes(Cn) if m["base"] == "rdi" and m["disp"] <= 0xC20 < m["disp"] + m["size"]]
    after = [(a, t) for a, t in Cn.calls() if a > CTOR + 0x12B]
    R.check("constructor: + 0x22 `mov rdi, rcx`, + 0x25 `xor ebp, ebp`; RBP and RDI not rewritten before + 0x12B "
            "`mov dword ptr [rdi + 0xc20], ebp` (the body's only store covering +0xC20); seven calls follow it "
            "(001CCE7E, 001CCEA4, 001CCEB0, 001CCF04 and three to 0019C5D0)",
            T(Cn, CTOR + 0x22) == "mov rdi, rcx" and T(Cn, CTOR + 0x25) == "xor ebp, ebp" and
            writers(Cn, "rbp", CTOR + 0x26, CTOR + 0x12B) == [] and writers(Cn, "rdi", CTOR + 0x23, CTOR + 0x12B) == []
            and T(Cn, CTOR + 0x12B) == "mov dword ptr [rdi + 0xc20], ebp" and c20 == [CTOR + 0x12B] and
            after == [(0x1CCE7E, 0x861EC0), (0x1CCEA4, 0x1D0390), (0x1CCEB0, 0x202880), (0x1CCF04, 0x5CC930),
                      (0x1CCF2A, 0x19C5D0), (0x1CCF40, 0x19C5D0), (0x1CCF56, 0x19C5D0)],
            "c20 %s after %s" % (["%X" % a for a in c20], ["%X" % a for a, t in after]))
    # ---------------- primary modifier
    M = Body(img, PRIM, PRIM_END)
    R.check("primary modifier flags: R8D -> EBX (+ 0x19) and homed (+ 0x5); bit 0 -> EAX (+ 0x31, + 0x36); "
            "inverted bit 4 -> R13D (+ 0x2A .. + 0x39); inverted bit 7 -> R15D (+ 0x54 .. + 0x5E); bit 0 set skips the "
            "entry leg (+ 0x62 / + 0x64 -> + 0x89)",
            T(M, PRIM + 0x5) == "mov dword ptr [rsp + 0x18], r8d" and T(M, PRIM + 0x19) == "mov ebx, r8d" and
            T(M, PRIM + 0x2D) == "shr r13d, 4" and T(M, PRIM + 0x33) == "not r13d" and
            T(M, PRIM + 0x39) == "and r13d, 1" and T(M, PRIM + 0x57) == "shr r15d, 7" and
            T(M, PRIM + 0x5B) == "not r15d" and T(M, PRIM + 0x36) == "and eax, 1" and
            M[PRIM + 0x64].direct_target() == PRIM + 0x89)
    R.check("entry leg tests the LOW WORDs: + 0x66 `call 0030B770`, + 0x72 `call 0030B7F0`, + 0x77 `test bx, bx`, + 0x80 "
            "`test ax, ax`, either nonzero -> return (+ 0x14A)",
            T(M, PRIM + 0x66) == "call 0x30b770" and T(M, PRIM + 0x72) == "call 0x30b7f0" and
            T(M, PRIM + 0x77) == "test bx, bx" and M[PRIM + 0x7A].direct_target() == PRIM + 0x14A and
            T(M, PRIM + 0x80) == "test ax, ax" and M[PRIM + 0x83].direct_target() == PRIM + 0x14A)
    R.check("notifications then late leg: owner NULL skips both (+ 0xC1 / + 0xC4); R13D gates `call 003283D0` (+ 0xDA); "
            "R15D gates `call 0028F1F0` (+ 0xF3) with ECX = DWORD [owner + 8], EDX = old signed WORD +0x4C, R8D = "
            "candidate, R9D = 1; then a negative delta (+ 0xF8 / + 0xFB `jns`) calls 0030B770 (+ 0xFD), saves its EAX "
            "at [rsp + 0x68] (+ 0x104), calls 0030B7F0 (+ 0x10B), and returns if WORD [rsp + 0x6a] (+ 0x110) or the unit "
            "result's upper WORD (+ 0x118 / + 0x11B) is nonzero",
            M[PRIM + 0xC4].direct_target() == PRIM + 0xF8 and T(M, PRIM + 0xDA) == "call 0x3283d0" and
            T(M, PRIM + 0xE4) == "mov ecx, dword ptr [r14 + 8]" and T(M, PRIM + 0xE8) == "mov r9d, 1" and
            T(M, PRIM + 0xEE) == "mov r8d, edi" and T(M, PRIM + 0xF1) == "mov edx, ebx" and
            T(M, PRIM + 0xF3) == "call 0x28f1f0" and T(M, PRIM + 0xF8) == "test r12d, r12d" and
            M[PRIM + 0xFB].mnemonic == "jns" and M[PRIM + 0xFB].direct_target() == PRIM + 0x120 and
            T(M, PRIM + 0xFD) == "call 0x30b770" and T(M, PRIM + 0x104) == "mov dword ptr [rsp + 0x68], eax" and
            T(M, PRIM + 0x10B) == "call 0x30b7f0" and T(M, PRIM + 0x110) == "cmp word ptr [rsp + 0x6a], 0" and
            M[PRIM + 0x116].direct_target() == PRIM + 0x14A and T(M, PRIM + 0x118) == "shr eax, 0x10" and
            T(M, PRIM + 0x11B) == "test ax, ax" and M[PRIM + 0x11E].direct_target() == PRIM + 0x14A)
    R.check("the store and what follows it: + 0x120 `mov word ptr [rsi + 0x4c], di`; on the negative leg it is "
            "reachable from + 0xFD only through both late tests; then delta > 0 -> `call 00300BC0` (+ 0x134) with "
            "R8D = the homed flags [rsp + 0x70]; owner and candidate < old -> `call 002FA540` (+ 0x145)",
            T(M, PRIM + 0x120) == "mov word ptr [rsi + 0x4c], di" and
            PRIM + 0x120 not in M.reach(PRIM + 0xFD, avoid=[PRIM + 0x118]) and
            PRIM + 0x120 not in M.reach(PRIM + 0xFD, avoid=[PRIM + 0x11B]) and
            T(M, PRIM + 0x129) == "mov r8d, dword ptr [rsp + 0x70]" and T(M, PRIM + 0x134) == "call 0x300bc0" and
            T(M, PRIM + 0x145) == "call 0x2fa540" and PRIM + 0x145 not in M.reach(PRIM + 0xFD, avoid=[PRIM + 0x120]))
    # ---------------- secondary modifier
    Sc = Body(img, SEC, SEC_END)
    R.check("secondary modifier: flags in R14D (+ 0x15); bit 0 set skips its entry leg (+ 0x25 / + 0x29 -> + 0x50); "
            "+ 0xAA `mov word ptr [rdi + 6], cx` dominates + 0xB4 `call 0030E060`, whose EDX is the full R14D (+ 0xAE)",
            T(Sc, SEC + 0x15) == "mov r14d, r8d" and T(Sc, SEC + 0x25) == "test r14b, 1" and
            Sc[SEC + 0x29].direct_target() == SEC + 0x50 and T(Sc, SEC + 0xAA) == "mov word ptr [rdi + 6], cx" and
            T(Sc, SEC + 0xAE) == "mov edx, r14d" and T(Sc, SEC + 0xB4) == "call 0x30e060" and
            Sc.dominates(SEC + 0xAA, SEC + 0xB4) and writers(Sc, "r14", SEC + 0x16) == [SEC + 0xCC])
    emu_checks(img, R, small)


def emu_checks(img, R, small=False):
    q = query_results(img, small)
    n, bad = q["gq"]
    R.check("emulated global query over every combination of its six mask bits and the flag byte's bit 0, at eight "
            "stack alignments, on a stack filled with 0xFF (%d runs): the upper WORD is 0 every time and the low WORD "
            "equals the bit map (0..31); no call" % n, not bad, "; ".join(bad[:2]))
    n, bad, his, rb = q["uq"]
    R.check("emulated unit query, %d states (unit NULL / flags / +4 bit 5 / stats NULL / byte +5 / byte +4 / C20 in "
            "0, 1, 2, 3, 0x101, 2^32 - 1 / EDX / state 0, 5, 6), C20 read twice through the initialized accessor: the "
            "result equals the formula every time, and the upper WORD is only ever 0, 1 or 2" % n,
            not bad and his == [0, 1, 2], "; ".join(bad[:2]) + " his %s" % his)
    R.check("emulated: for an eligible unit the C20 DWORD is read exactly twice, both from 0017D470 + 0x9, and the "
            "fast path makes no non-stack store and no call beyond the two getter / accessor entries; an ineligible "
            "unit reads it zero times", not rb, "; ".join(rb[:2]))
    tab, bad = q["two"]
    R.check("emulated two different reads (C20 changed between the getter calls): upper = (first == 1 ? 1) | (second "
            "== 2 ? 2); first 1 / second 2 gives 3",
            not bad and tab[(1, 2)] == 3 and tab[(1, 1)] == 1 and tab[(2, 2)] == 2, str(bad))
    R.check("the packet's four conditional-control rows reproduce through the original bytes: (1, 1, stats) -> 1, "
            "(2, 2, no stats) -> 2, (1, 2, stats) -> 3, ineligible -> 0",
            [x[4] for x in q["rows"]] == [1, 2, 3, 0], str(q["rows"]))
    lz = q["lazy"]
    a, b, c = lz["lazy"], lz["nullalloc"], lz["ctor-other"]
    R.check("emulated lazy path: with the root NULL the first getter call allocates 0x10E8 bytes, calls the "
            "constructor with RCX = the allocation and publishes its RAX; the second getter call takes the fast path "
            "(one allocation, one constructor call in all)",
            a["r"]["ok"] and a["calls"] == [(ALLOC, 0x10E8), (CTOR, X)] and a["root"] == X and
            a["rootw"] == [(ACC + 0x36, X)] and (a["r"]["rax"] & 0xFFFFFFFF) >> 16 == 2, str(a["calls"]))
    R.check("emulated NULL allocation: no constructor call, the root is stored as 0, and the getter then reads address "
            "0xC20 (an unmapped-read fault in emulation; a source prediction, not an observed fault)",
            b["calls"] == [(ALLOC, 0x10E8)] and b["rootw"] == [(ACC + 0x36, 0)] and b["r"]["fault"] == 0xC20,
            "calls %s fault %s" % (b["calls"], b["r"]["fault"]))
    R.check("emulated: the root receives the constructor's RAX, not the allocation, when the two differ",
            c["root"] == X + 0x1000 and c["rootw"] == [(ACC + 0x36, X + 0x1000)], "%X" % c["root"])
    p = prim_results(img)
    R.check("emulated mode 17, delta -10, C20 0: owner lookup, `0028F1F0` (ECX = owner DWORD 8, EDX = 50, R8D = 40, "
            "R9D = 1), then 0030B770, 0030B7F0, the +0x4C store of 40, then `002FA540`; no `003283D0`; no query "
            "before the notification",
            p["a"]["ok"] and p["a"]["seq"] == ["31B860", "28F1F0", "30B770", "30B7F0", "W4C=40", "2FA540"] and
            p["a"]["args"][PUB_B][1:] == (50, 40, 1) and p["a"]["args"][PUB_B][0] & 0xFFFFFFFF == 0x1234,
            str(p["a"]["seq"]))
    veto = ["31B860", "28F1F0", "30B770", "30B7F0"]
    R.check("emulated mode 17 veto: C20 1 (stats byte +5 = 0) and C20 2 each stop the +0x4C store and the `002FA540` "
            "call after the notification was already attempted; MP stays 50",
            p["b"]["seq"] == veto and p["c"]["seq"] == veto and p["b"]["mp"] == 50 and p["c"]["mp"] == 50 and
            p["b"]["ok"] and p["c"]["ok"], "%s %s" % (p["b"]["seq"], p["c"]["seq"]))
    R.check("emulated: no veto for C20 1 with stats byte +5 = 1, nor for C20 2 on an ineligible unit",
            p["d"]["seq"] == p["a"]["seq"] and p["e"]["seq"] == p["a"]["seq"], "%s %s" % (p["d"]["seq"], p["e"]["seq"]))
    R.check("emulated intervention: with 0030B770 REPLACED by a stub returning 0x10000 the store is vetoed; the same "
            "stub returning 0x1F (a low-WORD-only mask) does not veto - the shipping body never returns the former",
            p["f"]["seq"] == veto and p["f0"]["seq"] == p["a"]["seq"], "%s %s" % (p["f"]["seq"], p["f0"]["seq"]))
    R.check("emulated frame: in the whole mode-17 run the only write to the modifier's RDX home slot is its own save "
            "of the global result (+ 0x104); nothing the unit query runs overwrites it before the WORD test (+ 0x110)",
            p["home"] == [(PRIM + 0x104, 0)], str([("%X" % a, v) for a, v in p["home"]]))
    R.check("emulated mode 16 (bit 0 clear): the entry leg runs first - 0030B770, 0030B7F0 - before the "
            "notification, then the late leg",
            p["g"]["seq"] == ["31B860", "30B770", "30B7F0", "28F1F0", "30B770", "30B7F0", "W4C=40", "2FA540"] and
            p["g"]["args"][UQ][1] == 0, str(p["g"]["seq"]))
    R.check("emulated mode 17, delta +10 (C20 2): no query, the store of 60, then `00300BC0` with (stats, 10, 0x11); "
            "no `002FA540`",
            p["h"]["seq"] == ["31B860", "28F1F0", "W4C=60", "300BC0"] and p["h"]["args"][SEC][0] == P and
            p["h"]["args"][SEC][1:3] == (10, 0x11), str(p["h"]["seq"]))
    R.check("emulated flag roles: mode 1 (bit 4 clear) calls `003283D0` before `0028F1F0`; mode 0x91 (bit 7 set) "
            "does not call `0028F1F0`; a NULL owner skips both notifications, its unit query returns 0 and the store "
            "happens",
            p["i1"]["seq"][:3] == ["31B860", "3283D0", "28F1F0"] and "28F1F0" not in p["i2"]["seq"] and
            p["j"]["seq"] == ["31B860", "30B770", "30B7F0", "W4C=40"], "%s %s %s" % (
                p["i1"]["seq"], p["i2"]["seq"], p["j"]["seq"]))
    s = sec_results(img)
    R.check("emulated secondary: mode 17 stores WORD +6 (20 - 5 = 15) and then calls `0030E060` with (stats, 0x11), "
            "no query; mode 16 runs both queries first",
            s[0x11]["seq"] == ["31B860", "W6=15", "30E060"] and s[0x11]["cb"] == [(P, 0x11)] and
            s[0x10]["seq"] == ["31B860", "30B770", "30B7F0", "W6=15", "30E060"], "%s %s" % (s[0x11]["seq"],
                                                                                         s[0x10]["seq"]))
    return q, p


# ------------------------------------------------------------------ censuses (shipping image only)
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
    found, unresolved = {}, []
    for h in sorted(cand):
        ci = insn_covering(img, h)
        if ci is None:
            unresolved.append(h)
            continue
        for op in ci.operands:
            if op.type != X86_OP_MEM:
                continue
            mm = op.mem
            if mm.base and ci.reg_name(mm.base) == "rip":
                t = ci.address + ci.size + mm.disp
            elif mm.disp + img.base >= lo - 16 and mm.disp + img.base < hi:
                t = (mm.disp & 0xFFFFFFFF) + img.base
            else:
                continue
            if t < hi and t + max(op.size, 1) > lo:
                found[ci.address] = (ci.mnemonic + " " + ci.op_str, t, op.size)
    return found, unresolved


def census_checks(img, R):
    print("== raw direct-reference census (E8/E9 rel32 and 0F 8x jcc, .text)")
    rc = raw_refs(img, [PRIM, SEC, GQ, UQ, GET, ACC, ACC2, CTOR])
    for t in (PRIM, SEC, GQ, UQ, GET, ACC2, CTOR):
        R.note("%08X raw direct references (%d): %s" % (t, len(rc[t]), ", ".join("%X %s" % x for x in rc[t][:10])))
    R.note("001D50D0 raw direct references: %d" % len(rc[ACC]))
    R.check("0017D470 (the C20 getter) has exactly two raw direct references, both in the unit query (+ 0x93, + 0xC6); "
            "the constructor 001CCB20 has exactly two, the accessor 001D50D0 + 0x30 and its twin 001D5090 + 0x2E",
            rc[GET] == [(UQ + 0x93, "call"), (UQ + 0xC6, "call")] and
            sorted(rc[CTOR]) == [(ACC2 + 0x2E, "call"), (ACC + 0x30, "call")])
    print("== singleton root census (rip-relative and image-base-relative disp32 meeting 01F81428 .. + 8)")
    found, unres = disp_census(img, ROOT, ROOT + 8)
    for a in sorted(found):
        R.note("%X  %-44s (.pdata record %X..%X)" % ((a, found[a][0]) + img.pdata(a)))
    R.note("unresolved candidates (no .pdata record or decode desync): %s" % ["%X" % h for h in unres])
    wr = sorted(a for a in found if found[a][0].startswith("mov qword ptr [rip"))
    T2 = Body(img, ACC2, ACC2_END)
    R.check("01F81428 census: four instructions; the only stores are 001D5090 + 0x34 and 001D50D0 + 0x36, each on its "
            "body's NULL path (the nonNULL branch skips it): no instruction in the census replaces a nonNULL root",
            sorted(found) == [ACC2 + 0xD, ACC2 + 0x34, ACC + 0xD, ACC + 0x36] and wr == [ACC2 + 0x34, ACC + 0x36] and
            T(T2, ACC2 + 0xD).startswith("cmp qword ptr [rip") and T2[ACC2 + 0x15].direct_target() == ACC2 + 0x3B and
            ACC2 + 0x34 not in T2.reach(ACC2 + 0x3B) and T(T2, ACC2 + 0x2E) == "call 0x1ccb20" and not unres,
            str(["%X" % a for a in sorted(found)]))
    Cb = Body(img, CALLER, 0x003057C9)
    R.check("the consume path 00305640 + 0xB4 calls the primary modifier with R8D = 0x10 + (R12D != 0) (+ 0x42 `xor "
            "r15d, r15d`, + 0xA0 `mov esi, r15d`, + 0xA8 `setne sil`, + 0xB0 `lea r8d, [rsi + 0x10]`) and EDX = -cost "
            "(+ 0xAC `neg ebx`, + 0xAE); + 0xCD calls the secondary with the same R8D (+ 0xC0): mode 16 or 17",
            T(Cb, CALLER + 0x42) == "xor r15d, r15d" and writers(Cb, "r15", CALLER + 0x43, CALLER + 0xB4) == [] and
            T(Cb, CALLER + 0xA0) == "mov esi, r15d" and T(Cb, CALLER + 0xA3) == "test r12d, r12d" and
            T(Cb, CALLER + 0xA8) == "setne sil" and T(Cb, CALLER + 0xAC) == "neg ebx" and
            T(Cb, CALLER + 0xAE) == "mov edx, ebx" and T(Cb, CALLER + 0xB0) == "lea r8d, [rsi + 0x10]" and
            T(Cb, CALLER + 0xB4) == "call 0x300ce0" and T(Cb, CALLER + 0xC0) == "lea r8d, [rsi + 0x10]" and
            T(Cb, CALLER + 0xCD) == "call 0x300bc0" and writers(Cb, "rsi", CALLER + 0xA9, CALLER + 0xCD) == [])


# ------------------------------------------------------------------ packet integrity
def evdir(slug):
    return os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(find_exe())))),
                        "FFXII TZA", "_experiments", "evidence", slug)


def git(*args):
    top = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True,
                         cwd=os.path.dirname(os.path.abspath(__file__))).stdout.strip()
    return subprocess.run(["git"] + list(args), capture_output=True, cwd=top).stdout


def manifest_check(R, slug):
    ev = evdir(slug)
    mb = open(os.path.join(ev, "manifest.json"), "rb").read()
    committed = git("show", "%s:Database/FFXII TZA/_experiments/evidence/%s/manifest.json" % (PRODUCER, slug))
    mem = json.loads(mb)["members"]
    bad = [m["path"] for m in mem if not os.path.exists(os.path.join(ev, m["path"])) or
           hashlib.sha256(open(os.path.join(ev, m["path"]), "rb").read()).hexdigest() != m["sha256"]]
    R.check("%s manifest sha256 %s... equals the manifest committed at 7b4e2b92c; all %d members hash as listed" % (
        slug, hashlib.sha256(mb).hexdigest()[:16], len(mem)), mb == committed and not bad, str(bad[:5]))
    return hashlib.sha256(mb).hexdigest(), len(mem)


def packet_checks(img, R, q, p):
    top = os.path.dirname(evdir(MUT))
    R.check("the record path the board request names (%s/README.md) does not exist; the publication's evidence is the "
            "two folders %s and %s, both first committed in 7b4e2b92c" % (NAMED_RECORD, MUT, ELIG),
            not os.path.exists(os.path.join(top, NAMED_RECORD)) and
            git("log", "--format=%H", "--diff-filter=A", "--", "Database/FFXII TZA/_experiments/evidence/%s/README.md"
                % MUT).split() == [PRODUCER.encode()] and
            git("log", "--format=%H", "--diff-filter=A", "--", "Database/FFXII TZA/_experiments/evidence/%s/README.md"
                % ELIG).split() == [PRODUCER.encode()])
    msha, mn = manifest_check(R, MUT)
    esha, en = manifest_check(R, ELIG)
    R.note("mutator manifest sha256 %s (%d members) - the 'frozen mode17 package 6db69c8e'; eligibility manifest "
           "sha256 %s (%d members)" % (msha, mn, esha, en))
    R.check("the eligibility README's 'frozen mode17 package 6db69c8e' is the mutator folder's manifest hash (32 "
            "members), not a commit", msha.startswith("6db69c8e") and mn == 32)
    bad = []
    for slug, fn in ((MUT, "source-01.json"), (ELIG, "source-01.json"), (ELIG, "mode-source-01.json"),
                     (ELIG, "caller-mutators-source-01.json"), (ELIG, "singleton-source-01.json"),
                     (ELIG, "retained-constructor-source-01.json")):
        s = json.load(open(os.path.join(evdir(slug), fn)))
        for r in s["ranges"]:
            a, b = int(r["start"], 16), int(r["end_exclusive"], 16)
            ok = hashlib.sha256(img.read(a, b - a)).hexdigest() == r["sha256"]
            if "instructions" in r:
                ok = ok and b"".join(bytes.fromhex(i["bytes"]) for i in r["instructions"]) == img.read(a, b - a)
            if not ok:
                bad.append("%s %s" % (fn, r["start"]))
    R.check("every source range in both folders (00300CE0, 00300BC0, 0030B770, 0030B7F0, 0017D470, 001D50D0, "
            "001CCB20) hashes to this image's bytes and its instruction records concatenate to them", not bad, str(bad))
    bad = []
    for slug, fn in ((MUT, "extents-01.json"), (ELIG, "extents-01.json"), (ELIG, "mode-extents-01.json"),
                     (ELIG, "singleton-extents-01.json")):
        x = json.load(open(os.path.join(evdir(slug), fn)))
        for b in x["bodies"]:
            s, e = int(b["entry"], 16), int(b["end_exclusive"], 16)
            ents, ok = img.pdata_cover(s, e)
            if not (ok and bytes.fromhex(b["physical_bytes"]) == img.read(s, e - s) and b["bytes"] == e - s and
                    [(int(r["begin"], 16), int(r["end_exclusive"], 16)) for r in b["records"]] ==
                    [(pp, qq) for pp, qq, fl, rr in ents]):
                bad.append("%s %s" % (fn, b["entry"]))
    R.check("every extents file's bodies equal this image's physical bytes, sizes and .pdata records", not bad, str(bad))
    lin = json.load(open(os.path.join(evdir(ELIG), "retained-constructor-lineage-01.json")))
    blob = git("show", "%s:%s" % (lin["commit"], lin["path"]))
    R.check("retained-constructor-source-01.json is byte-identical to %s's %s (sha256 %s...)" % (
        lin["commit"][:9], lin["path"].split("/")[-1], lin["sha256"][:12]),
        blob and blob == open(os.path.join(evdir(ELIG), "retained-constructor-source-01.json"), "rb").read() and
        hashlib.sha256(blob).hexdigest() == lin["sha256"])
    qr = json.load(open(os.path.join(evdir(ELIG), "qualified-result-02.json")))
    R.check("qualified-result-02's seven post-store calls equal this review's list",
            [(int(a, 16), int(t, 16)) for a, t in qr["facts"]["post_store_opaque_calls"]] ==
            [(0x1CCE7E, 0x861EC0), (0x1CCEA4, 0x1D0390), (0x1CCEB0, 0x202880), (0x1CCF04, 0x5CC930),
             (0x1CCF2A, 0x19C5D0), (0x1CCF40, 0x19C5D0), (0x1CCF56, 0x19C5D0)])
    rr = json.load(open(os.path.join(evdir(ELIG), "result-02.json")))
    R.check("result-02's four conditional-control rows equal the emulated original bytes",
            [(c["eligible"], c["first"], c["second"], c["stats0"], c["upper"]) for c in
             rr["facts"]["conditional_controls"]] == q["rows"], str(q["rows"]))
    mr = json.load(open(os.path.join(evdir(MUT), "result-02.json")))
    want = {"both-upper-words-zero": "W4C=40" in p["a"]["seq"], "first-upper-word-nonzero": "W4C=40" in p["f"]["seq"],
            "second-upper-word-nonzero": "W4C=40" in p["c"]["seq"]}
    R.check("the mutator result-02's three cases (own +0x4C store true / false / false, notification before the late "
            "queries, no 003283D0) agree with the emulation (the first-upper case only with 0030B770 replaced)",
            all(c["own_word4c_store"] == want[c["label"]] and c["notification_attempt_before_post_queries"] and
                c["initial_3283d0_attempt"] is False for c in mr["facts"]["cases"]) and
            p["a"]["seq"].index("28F1F0") < p["a"]["seq"].index("30B770"))
    rd = " ".join(open(os.path.join(evdir(ELIG), "README.md"), encoding="utf-8").read().split())
    rm = " ".join(open(os.path.join(evdir(MUT), "README.md"), encoding="utf-8").read().split())
    R.check("both READMEs keep their limits: no natural initialization or lifetime proof, no whole-call no-effects "
            "claim, the call attempt is not visible presentation",
            "Natural initialization, ownership/lifetime, concurrent/alias mutation remain explicit premises" in rd and
            "This does not promise that the whole operation has no effects" in rd and
            "28F1F0 callattempt isnotvisible presentation" in rm and "ownveto isnot whole-call no-write" in rm)


CONTROLS = [
    ("global query + 0x15 zeroing store writes 0x10000", GQ + 0x15, bytes.fromhex("c7450000000100")),
    ("global query + 0x15 zeroing store -> 7-byte NOP", GQ + 0x15, bytes.fromhex("0f1f8000000000")),
    ("global query + 0x40 WORD store -> DWORD store (66 prefix -> NOP)", GQ + 0x40, bytes.fromhex("90")),
    ("unit query + 0xCB `cmp eax, 2` -> `cmp eax, 1`", UQ + 0xCD, bytes([0x01])),
    ("unit query + 0x98 `cmp eax, 1` -> `cmp eax, 2`", UQ + 0x9A, bytes([0x02])),
    ("unit query + 0xAF byte +5 test's `jne` -> NOP NOP", UQ + 0xAF, bytes.fromhex("9090")),
    ("getter field +0xC20 -> +0xC24", GET + 0xB, bytes([0x24])),
    ("accessor + 0x17 `jne` -> `je` (fast path inverted)", ACC + 0x17, bytes([0x74])),
    ("accessor + 0x17 `jne` retargeted to the root store + 0x36", ACC + 0x18, bytes([0x1D])),
    ("primary + 0x116 global-upper veto `jne` -> NOP NOP", PRIM + 0x116, bytes.fromhex("9090")),
    ("primary + 0x11E unit-upper veto `jne` -> NOP NOP", PRIM + 0x11E, bytes.fromhex("9090")),
    ("primary + 0x64 bit-0 bypass `jne` -> NOP NOP", PRIM + 0x64, bytes.fromhex("9090")),
    ("primary + 0xFB `jns` -> `jmp` (late leg never runs)", PRIM + 0xFB, bytes([0xEB])),
    ("primary + 0x102 `xor edx, edx` -> `mov edx, ebx`", PRIM + 0x102, bytes.fromhex("8bd3")),
    ("secondary + 0xAA WORD +6 store -> 4-byte NOP", SEC + 0xAA, bytes.fromhex("0f1f4000")),
    ("secondary + 0xAE `mov edx, r14d` -> `mov edx, esi` + NOP", SEC + 0xAE, bytes.fromhex("8bd690")),
    ("constructor + 0x12B C20 store -> +0xC24", CTOR + 0x12D, bytes([0x24])),
    ("constructor + 0x25 `xor ebp, ebp` -> `mov ebp, ebx`", CTOR + 0x25, bytes.fromhex("8beb")),
]


def main():
    img = Img.load()
    R = Rep("rv_mode17q")
    census_checks(img, R)
    print("== shipping-image re-derivation")
    checks(img, R)
    q = query_results(img)
    p = prim_results(img)
    print("== packet integrity")
    packet_checks(img, R, q, p)
    print("== controls (each patched private image must FAIL at least one check above)")
    Rn = Rep("null")
    Rn.quiet = True
    P0 = img.patched(GQ + 0x15, img.read(GQ + 0x15, 7))
    P0._private = True
    checks(P0, Rn, small=True)
    R.check("null control: an unchanged private copy passes every image check", Rn.fails == 0 and Rn.n > 0,
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
