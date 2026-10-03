"""rv_binding.py - FABLE independent re-derivation for ASTRA packet ov42-action-table-binding (ca2dd6483, OV-42).

Own reader (rvlib.py: struct + capstone 5, copied unchanged from the kind-row review, sha256 69f9bc40be32abcc...).
Does not import or run ASTRA's prove.py, prove_owner_reload_order.py, prove-before-conditional-order-correction.py,
capture*.py, control.py, prepare-*.py, run.py, validate-title-source-annotations.py or the shared role adapter
(reg_tracking.py).

Method:
  * image sha256; the .pdata extents of the four bodies (registrar 00236C30, slot wrapper 00237FC0, binder
    003845F0 with seven chained records, child binder 003846F0) and the two leaves without .pdata (decoder
    0020E600, encoder 0020E620), each decoded linearly and exactly;
  * the argument chain registrar + 0x14B .. + 0x155 -> wrapper + 0xF .. + 0x1E -> binder, read and emulated;
  * the binder read instruction by instruction: slot store first, the four plain rebases (+0xC through RDX, the
    other three through a reload of the slot), the +0x14 encode / decode / visit, the outer loop and its depth-0
    child calls, and the complete list of its own non-stack stores; the child binder's depth test;
  * a concrete emulation (unicorn) of the ORIGINAL binder, child binder and both leaves - no stubs, nothing else
    is called - on supplied descriptors: the packet's three countermodels, a two-level directory, zero and null
    descriptors, random plain fields, random leaf inputs;
  * a raw E8/E9 rel32 and 0F 8x census for the chain, and a rip-relative / image-base-relative disp32 census of
    the slot 02EBF138 and of the image-address base 01F83530, plus a re-read of the published indexed store that
    reaches 01F83530 (de52023ee);
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

SLUG = "ov42-action-table-binding"
PRODUCER = "ca2dd6483fdcd24535237d727d8ea2fa34e2c19b"
REG, REG_END = 0x00236C30, 0x0023703D      # registrar, 1037 B
WRAP, WRAP_END = 0x00237FC0, 0x00238154    # slot wrapper, 404 B
BIND, BIND_END = 0x003845F0, 0x003846EC    # binder, 252 B
CHILD, CHILD_END = 0x003846F0, 0x003847A1  # child binder, 177 B
DEC, DEC_END = 0x0020E600, 0x0020E60A      # decoder leaf, 10 B
ENC, ENC_END = 0x0020E620, 0x0020E629      # encoder leaf, 9 B
SLOT = 0x02EBF138
DIRCELL = 0x0208E680
ARENA = 0x01F83530
TEXLEAF, TEXLEAF_END = 0x00210570, 0x00210592
TEXTABLE = 0x01F83580


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


def nonstack_writes(B):
    out = []
    for a in B.order:
        for m in B[a].mems:
            if m["write"] and m["base"] not in ("rsp", "rbp") and B[a].mnemonic not in ("push", "call"):
                out.append((a, m))
    return out


def sext32(v):
    v &= 0xFFFFFFFF
    return v | 0xFFFFFFFF00000000 if v & 0x80000000 else v


def leaf(img, s, e):
    return list(img.cs.disasm(img.read(s, e - s), s))


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
            mu.mem_write(p, img.read(p, 0x1000))          # .text pages: file-backed
        self.zero = []
        for p in sorted(set(x & ~0xFFF for x in data_pages) - cpages):
            mu.mem_map(p, 0x1000)                          # data cells: zero-filled, inputs written explicitly
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
        self.until = None

        def ch(uc, addr, size, ud):
            if addr == self.until:
                uc.emu_stop()
                return
            if addr in self.watch or addr in self.stubs:
                rsp = uc.reg_read(X.UC_X86_REG_RSP)
                ra = struct.unpack("<Q", bytes(uc.mem_read(rsp, 8)))[0]
                self.trace.append((addr, uc.reg_read(X.UC_X86_REG_RCX), uc.reg_read(X.UC_X86_REG_RDX),
                                   uc.reg_read(X.UC_X86_REG_R8), ra))
            if addr in self.stubs:
                rsp = uc.reg_read(X.UC_X86_REG_RSP)
                uc.reg_write(X.UC_X86_REG_RAX, self.stub_rax.get(addr, 0))
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

    def w32(self, a, v):
        self.mu.mem_write(a, struct.pack("<I", v & 0xFFFFFFFF))

    def w64(self, a, v):
        self.mu.mem_write(a, struct.pack("<Q", v & 0xFFFFFFFFFFFFFFFF))

    def w16(self, a, v):
        self.mu.mem_write(a, struct.pack("<H", v & 0xFFFF))

    def u32(self, a):
        return struct.unpack("<I", bytes(self.mu.mem_read(a, 4)))[0]

    def u64(self, a):
        return struct.unpack("<Q", bytes(self.mu.mem_read(a, 8)))[0]

    def run(self, start, until=None, **regs):
        from unicorn import UcError
        X = self.X
        sp = self.STK + 0x8000
        self.mu.mem_write(sp, struct.pack("<Q", self.RET))
        self.mu.reg_write(X.UC_X86_REG_RSP, sp)
        base = {"rax": 0xAAAAAAAAAAAAAAAA, "rbx": 0xBBBBBBBBBBBBBBBB, "rbp": 0xB0B0B0B0B0B0B0B0,
                "rsi": 0x5151515151515151, "rdi": 0xDDDDDDDDDDDDDDDD, "r8": 0x8888888888888888,
                "r9": 0x9999999999999999, "r14": 0xEEEEEEEEEEEEEEEE, "r15": 0xFFFF0000FFFF0000,
                "rcx": 0, "rdx": 0}
        base.update(regs)
        for k, v in base.items():
            self.mu.reg_write(getattr(X, "UC_X86_REG_" + k.upper()), v)
        self.trace, self.writes, self.reads = [], [], []
        self.intr, self.fault, self.left = None, None, None
        self.until = self.RET if until is None else until
        try:
            self.mu.emu_start(start, self.until, count=200000)
        except UcError as e:
            if self.intr is None and self.fault is None:
                self.fault = "UcError %s" % e
        r = dict((k, self.mu.reg_read(getattr(X, "UC_X86_REG_" + k.upper())))
                 for k in ("rax", "rbx", "rcx", "rdx", "rbp", "rsi", "rdi", "r8", "r14", "r15", "rip", "rsp"))
        r["trace"], r["writes"], r["reads"] = list(self.trace), list(self.writes), list(self.reads)
        r["intr"], r["fault"], r["left"] = self.intr, self.fault, self.left
        r["ok"] = (r["rip"] == self.until and not r["fault"] and not r["intr"] and not r["left"])
        return r


D0 = 0x100000                  # supplied descriptor (valid, separate from the slot)
HI = 0x100100000               # where a 64-bit arena sends the CM2 sub-directory
SCRATCH = [(D0, 0x10000), (HI, 0x1000), (0x7FFF0000, 0x10000), (0x40001000, 0x1000)]
RAND_D = [D0, 0x7FFF0000, 0x40001000]


def binder_emu(img):
    return Emu(img, [(BIND, BIND_END), (CHILD, CHILD_END), (DEC, DEC_END), (ENC, ENC_END)],
               data_pages=[ARENA, SLOT], scratch=SCRATCH, watch=[CHILD, DEC, ENC])


def bind(E, D, fields, arena=0, prep=None, reset=True):
    if reset:
        E.reset()
    E.w64(ARENA, arena)
    E.w64(SLOT, 0x5A5A5A5A5A5A5A5A)
    for off, v in fields.items():
        E.w32(D + off, v)
    if prep:
        prep(E)
    return E.run(BIND, rcx=SLOT, rdx=D)


def own_writes(r):
    return [(w[0], w[1], w[2], w[3]) for w in r["writes"]]


def dec_leaf(E, ecx, arena):
    E.w64(ARENA, arena)
    return E.run(DEC, rcx=ecx)


def enc_leaf(E, ecx, arena):
    E.w64(ARENA, arena)
    return E.run(ENC, rcx=ecx)


def emu_results(img):
    """The emulated facts used by the checks (and compared with result-02)."""
    E = binder_emu(img)
    out = {}
    # CM1: same descriptor pointer bound twice
    r1 = bind(E, D0, {0xC: 0x20})
    a1 = E.u32(D0 + 0xC)
    s1 = E.u64(SLOT)
    r2 = bind(E, D0, {}, reset=False)
    a2 = E.u32(D0 + 0xC)
    s2 = E.u64(SLOT)
    d1 = dec_leaf(E, a1, 0)["rax"]
    d2 = dec_leaf(E, a2, 0)["rax"]
    out["cm1"] = dict(first=a1, second=a2, slot1=s1, slot2=s2, dec1=d1, dec2=d2, ok=r1["ok"] and r2["ok"],
                      w1=own_writes(r1))
    # CM2: 64-bit arena, +0x14 = 0x100 (M = 0x100100)
    A2 = 0x100001000

    def prep2(E):
        E.w16(HI + 0x100, 0)
        E.w32(HI + 0x104, 0x10)
    r = bind(E, D0, {0x14: 0x100}, arena=A2, prep=prep2)
    enc = E.u32(D0 + 0x14)
    dfull = dec_leaf(E, enc, A2)["rax"]
    out["cm2"] = dict(stored=enc, decoded=dfull, M=(0x100 + D0) & 0xFFFFFFFF, ok=r["ok"],
                      count_read=[(x[0], x[1], x[2]) for x in r["reads"] if x[0] == BIND + 0x98],
                      last_write=[w for w in r["writes"] if w[0] == BIND + 0xC9],
                      low_touched=[w for w in r["writes"] if 0x100100 <= w[1] < 0x100110],
                      after_hi=E.u32(HI + 0x104))
    # CM3: count-zero directory at D+4 overlapping the stride
    r = bind(E, D0, {0x14: 4, 0x4: 0, 0x8: 60})
    out["cm3"] = dict(after_dword=E.u32(D0 + 8), stored14=E.u32(D0 + 0x14), ok=r["ok"],
                      store_sites=[w for w in r["writes"] if w[1] == D0 + 8])
    # a two-level directory (the normal shape): count 2, children of count 1 and 0
    def prep5(E):
        E.w16(D0 + 0x200, 2)
        E.w32(D0 + 0x204, 0x300)
        E.w32(D0 + 0x208, 0x400)
        E.w32(D0 + 0x20C, 0x500)
        E.w16(D0 + 0x500, 1)
        E.w32(D0 + 0x504, 0x10)
        E.w32(D0 + 0x508, 0x20)
        E.w16(D0 + 0x600, 0)
        E.w32(D0 + 0x604, 0x30)
    r = bind(E, D0, {0x14: 0x200}, prep=prep5)
    out["nest"] = dict(ok=r["ok"], stored14=E.u32(D0 + 0x14),
                       e=[E.u32(D0 + o) for o in (0x204, 0x208, 0x20C, 0x504, 0x508, 0x604)],
                       child=[(t[1], t[2], t[3] & 0xFFFFFFFF, t[4]) for t in r["trace"] if t[0] == CHILD],
                       writes=own_writes(r))
    # null descriptor and an all-zero descriptor
    r = bind(E, 0, {})
    out["null"] = dict(ok=r["ok"], writes=own_writes(r), trace=r["trace"])
    r = bind(E, D0, {})
    out["zero"] = dict(ok=r["ok"], writes=own_writes(r), trace=r["trace"])
    # random plain fields
    rnd = random.Random(11)
    bad = []
    for i in range(60):
        D = RAND_D[i % 3]
        f = {}
        for off in (0xC, 0x10, 0x18, 0x1C):
            f[off] = 0 if rnd.random() < 0.25 else rnd.getrandbits(32)
        r = bind(E, D, f)
        got = [E.u32(D + o) for o in (0xC, 0x10, 0x18, 0x1C)]
        want = [0 if f[o] == 0 else (f[o] + D) & 0xFFFFFFFF for o in (0xC, 0x10, 0x18, 0x1C)]
        if not r["ok"] or got != want or E.u64(SLOT) != D or [t for t in r["trace"]]:
            bad.append("D %X f %s got %s want %s" % (D, f, got, want))
    out["rand"] = bad
    # leaves on random inputs
    bad = []
    for i in range(200):
        ecx = rnd.getrandbits(64)
        A = rnd.getrandbits(64)
        rd = dec_leaf(E, ecx, A)
        rr = [(x[1], x[2]) for x in rd["reads"]]
        if rd["rax"] != ((ecx & 0xFFFFFFFF) + A) & 0xFFFFFFFFFFFFFFFF or rd["writes"] or rr != [(ARENA, 8)] or \
                not rd["ok"]:
            bad.append("dec ecx %X A %X -> %X reads %s" % (ecx, A, rd["rax"], rr))
        re_ = enc_leaf(E, ecx, A)
        rr = [(x[1], x[2]) for x in re_["reads"]]
        if re_["rax"] != ((ecx & 0xFFFFFFFF) - (A & 0xFFFFFFFF)) & 0xFFFFFFFF or re_["writes"] or \
                rr != [(ARENA, 4)] or not re_["ok"]:
            bad.append("enc ecx %X A %X -> %X reads %s" % (ecx, A, re_["rax"], rr))
    out["leaves"] = bad
    return out


def chain_emu(img):
    """Registrar + 0x14B .. its call, and the wrapper's head up to the binder's entry."""
    out = {}
    E = Emu(img, [(REG, REG_END)], data_pages=[DIRCELL], scratch=[(D0, 0x10000)])
    E.reset()
    E.w64(DIRCELL, D0)
    E.w32(D0 + 0x3C, 0x80001000)
    r = E.run(REG + 0x14B, until=WRAP)
    out["reg"] = dict(ok=r["ok"], ecx=r["rcx"] & 0xFFFFFFFF)
    W = Emu(img, [(WRAP, WRAP_END)])
    res = []
    for rcx in (0xAAAAAAAA80001000, 0x0000000000001000, 0x12345678FFFFFFF0):
        r = W.run(WRAP, until=BIND, rcx=rcx)
        res.append((r["ok"], r["rcx"], r["rdx"], rcx))
    out["wrap"] = res
    return out


def texleaf_emu(img):
    E = Emu(img, [(TEXLEAF, TEXLEAF_END)], data_pages=[ARENA, TEXTABLE])
    E.reset()
    r = E.run(TEXLEAF, rcx=0xFFFB, rdx=0x1122334455667788, r8=0x99)
    r2 = E.run(TEXLEAF, rcx=0x4000, rdx=0x1122334455667788, r8=0x99)
    return r, r2


# ------------------------------------------------------------------ image checks (also run on the controls)
def checks(img, R, small=False):
    R.check("image sha256 = %s..." % SHA_PIN[:20], hashlib.sha256(img.d).hexdigest() == SHA_PIN or
            getattr(img, "_private", False))
    # ---------------- extents
    ext = {}
    for nm, s, e, recs in (("registrar", REG, REG_END, 1), ("wrapper", WRAP, WRAP_END, 1),
                           ("binder", BIND, BIND_END, 7), ("child", CHILD, CHILD_END, 3)):
        ents, ok = img.pdata_cover(s, e)
        B = Body(img, s, e)
        ext[nm] = (ok, len(ents), B.exact, e - s)
    R.check("four .pdata extents tile exactly and decode exactly: registrar 00236C30 (1 record, 1037 B), wrapper "
            "00237FC0 (1 record, 404 B), binder 003845F0 (7 chained records, 252 B), child 003846F0 (3 records, "
            "177 B); 1870 B in all",
            ext == {"registrar": (True, 1, True, 1037), "wrapper": (True, 1, True, 404),
                    "binder": (True, 7, True, 252), "child": (True, 3, True, 177)} and
            sum(v[3] for v in ext.values()) == 1870, str(ext))
    dl, el = leaf(img, DEC, DEC_END), leaf(img, ENC, ENC_END)
    R.check("the two leaves have no .pdata and decode exactly: 0020E600 (10 B) `mov eax, ecx` / `add rax, qword ptr "
            "[01F83530]` / `ret`; 0020E620 (9 B) `sub ecx, dword ptr [01F83530]` / `mov eax, ecx` / `ret`; "
            "no call and no memory write in either",
            img.pdata(DEC) is None and img.pdata(ENC) is None and
            [(c.mnemonic + " " + c.op_str).strip() for c in dl][0::2] == ["mov eax, ecx", "ret"] and
            dl[1].mnemonic == "add" and dl[1].op_str.startswith("rax, qword ptr [rip") and
            dl[1].address + dl[1].size + dl[1].operands[1].mem.disp == ARENA and dl[1].operands[1].size == 8 and
            sum(c.size for c in dl) == 10 and el[0].mnemonic == "sub" and el[0].op_str.startswith("ecx, dword ptr [rip")
            and el[0].address + el[0].size + el[0].operands[1].mem.disp == ARENA and el[0].operands[1].size == 4 and
            [(c.mnemonic + " " + c.op_str).strip() for c in el[1:]] == ["mov eax, ecx", "ret"] and sum(c.size for c in el) == 9,
            " | ".join(c.mnemonic + " " + c.op_str for c in dl + el))
    # ---------------- registrar and wrapper
    G = Body(img, REG, REG_END)
    R.check("registrar + 0x14B `mov rax, qword ptr [0208E680]` (8 B), + 0x152 `mov ecx, dword ptr [rax + 0x3c]`, "
            "+ 0x155 `call 00237FC0`",
            T(G, REG + 0x14B).startswith("mov rax, qword ptr [rip") and rip_target(G[REG + 0x14B]) == DIRCELL and
            G[REG + 0x14B].mems[0]["size"] == 8 and T(G, REG + 0x152) == "mov ecx, dword ptr [rax + 0x3c]" and
            T(G, REG + 0x155) == "call 0x237fc0")
    W = Body(img, WRAP, WRAP_END)
    R.check("wrapper: ECX untouched before + 0xF `movsxd rdx, ecx` (48 63 D1, sign extension); + 0x15 `lea rcx, "
            "[02EBF138]`; + 0x1E `call 003845F0`; nothing else writes RCX or RDX between + 0xF and the call",
            writers(W, "rcx", WRAP, WRAP + 0xF) == [] and T(W, WRAP + 0xF) == "movsxd rdx, ecx" and
            W[WRAP + 0xF].bytes == b"\x48\x63\xd1" and T(W, WRAP + 0x15).startswith("lea rcx, [rip") and
            rip_target(W[WRAP + 0x15]) == SLOT and T(W, WRAP + 0x1E) == "call 0x3845f0" and
            writers(W, "rcx", WRAP + 0x10, WRAP + 0x1E) == [WRAP + 0x15] and
            writers(W, "rdx", WRAP + 0x10, WRAP + 0x1E) == [])
    R.check("after the bind the wrapper reloads the slot each pass and reads +4 as the row bound (`cmp esi, dword ptr "
            "[rdx + 4]`, + 0x35), +0xC through the decoder (+ 0x3D, + 0x51) and +8 as a WORD stride (+ 0x5D); the row "
            "address is formed in 32 bits (+ 0x64 `add eax, ecx`, + 0x66 `mov ecx, eax`) and dereferenced as RCX",
            rip_target(W[WRAP + 0x23]) == SLOT and T(W, WRAP + 0x35) == "cmp esi, dword ptr [rdx + 4]" and
            T(W, WRAP + 0x3A) == "mov ecx, dword ptr [rdx + 0xc]" and T(W, WRAP + 0x3D) == "call 0x20e600" and
            T(W, WRAP + 0x51) == "call 0x20e600" and T(W, WRAP + 0x5D) == "movzx ecx, word ptr [rdx + 8]" and
            T(W, WRAP + 0x61) == "imul ecx, esi" and T(W, WRAP + 0x64) == "add eax, ecx" and
            T(W, WRAP + 0x66) == "mov ecx, eax" and T(W, WRAP + 0x73) == "movzx eax, byte ptr [rcx + 0x38]")
    # ---------------- binder
    B = Body(img, BIND, BIND_END)
    nw = nonstack_writes(B)
    R.check("binder slot store first: + 0x4 `mov qword ptr [rcx], rdx` (8 B) is the body's first non-stack write and "
            "comes before `test rdx, rdx` (+ 0x7) and the `je` to the epilogue (+ 0xA -> + 0xF7); it dominates every "
            "other store",
            T(B, BIND + 0x4) == "mov qword ptr [rcx], rdx" and B[BIND + 0x4].mems[0]["size"] == 8 and
            nw and nw[0][0] == BIND + 0x4 and T(B, BIND + 0x7) == "test rdx, rdx" and
            B[BIND + 0xA].direct_target() == BIND + 0xF7 and
            all(B.dominates(BIND + 0x4, a) for a, m in nw[1:]))
    R.check("+0xC: + 0x10 `mov eax, dword ptr [rdx + 0xc]`, + 0x18 `test eax, eax`, + 0x1A `je` + 0x21, + 0x1C "
            "`add eax, edx` (03 C2, 32-bit, low32(D)), + 0x1E `mov dword ptr [rdx + 0xc], eax` (4 B); before that store "
            "the only tests are `test rdx, rdx` and `test eax, eax` and the only memory read is +0xC itself (no "
            "already-rebased flag)",
            T(B, BIND + 0x10) == "mov eax, dword ptr [rdx + 0xc]" and T(B, BIND + 0x18) == "test eax, eax" and
            B[BIND + 0x1A].direct_target() == BIND + 0x21 and T(B, BIND + 0x1C) == "add eax, edx" and
            B[BIND + 0x1C].bytes == b"\x03\xc2" and T(B, BIND + 0x1E) == "mov dword ptr [rdx + 0xc], eax" and
            [T(B, a) for a in B.order if a < BIND + 0x1E and B[a].mnemonic in ("test", "cmp")] ==
            ["test rdx, rdx", "test eax, eax"] and
            [a for a in B.order if a < BIND + 0x1E and any(m["read"] and m["base"] not in ("rsp",) for m in B[a].mems)]
            == [BIND + 0x10])
    fields_ok = []
    for off, ld, rl in ((0x10, 0x24, 0x21), (0x18, 0x35, 0x32), (0x1C, 0x46, 0x43)):
        st = ld + 0xA
        fields_ok.append(T(B, BIND + rl) == "mov r8, qword ptr [rcx]" and
                         T(B, BIND + ld) == "mov eax, dword ptr [r8 + 0x%x]" % off and
                         T(B, BIND + ld + 4) == "test eax, eax" and B[BIND + ld + 6].direct_target() == BIND + ld + 0xE
                         and T(B, BIND + ld + 8) == "add eax, edx" and
                         T(B, BIND + st) == "mov dword ptr [r8 + 0x%x], eax" % off)
    R.check("+0x10 / +0x18 / +0x1C: the same zero-test-then-add-low32(D) shape, but each addressed through a fresh "
            "`mov r8, qword ptr [rcx]` (+ 0x21, + 0x32, + 0x43) - a reload of the slot just written - not through RDX",
            all(fields_ok) and writers(B, "rcx", BIND + 0x5, BIND + 0x54) == [], str(fields_ok))
    seq = [(0x54, "mov rdi, qword ptr [rcx]"), (0x57, "mov eax, dword ptr [rdi + 0x14]"), (0x5A, "test eax, eax"),
           (0x62, "add eax, edx"), (0x69, "mov ecx, eax"), (0x6B, "mov ebp, eax"), (0x6D, "call 0x20e620"),
           (0x72, "mov dword ptr [rdi + 0x14], eax"), (0x75, "test rbp, rbp"), (0x7F, "mov ecx, eax"),
           (0x90, "call 0x20e600"), (0x95, "mov ecx, dword ptr [rdi + 0x14]"), (0x98, "movzx r14d, word ptr [rax]"),
           (0x9C, "call 0x20e600"), (0xA3, "mov r15, rax")]
    R.check("+0x14: slot reload + 0x54; zero -> epilogue (+ 0x5C); M = low32(+0x14 + D) (+ 0x62) kept in EBP; "
            "`call 0020E620` (+ 0x6D) and its EAX stored to +0x14 (+ 0x72) BEFORE the M == 0 test (+ 0x75 -> + 0xED); "
            "then decode of that EAX (+ 0x90), WORD count from the result (+ 0x98), a second decode of +0x14 re-read "
            "(+ 0x95, + 0x9C) as the entry base R15",
            all(T(B, BIND + o) == t for o, t in seq) and B[BIND + 0x5C].direct_target() == BIND + 0xF2 and
            B[BIND + 0x78].direct_target() == BIND + 0xED,
            "; ".join("+%X %s" % (o, T(B, BIND + o)) for o, t in seq if T(B, BIND + o) != t))
    R.check("outer loop: for i = 0 .. count (inclusive, + 0xD4 `cmp rdi, r14` / + 0xD7 `jle`): i < count -> `call "
            "003846F0` (+ 0xC2) with RCX = entry address (R15 + 4 + 4i), EDX = low32(entry + M) (+ 0xB9 `add edx, "
            "ebp`), R8D = 0 (+ 0xB3); i == count -> `add dword ptr [rbx], ebp` (+ 0xC9): the last entry += M; EBP is "
            "not rewritten in the loop",
            T(B, BIND + 0xA8) == "cmp rsi, r14" and B[BIND + 0xAF].direct_target() == BIND + 0xC9 and
            T(B, BIND + 0xB1) == "mov edx, dword ptr [rbx]" and T(B, BIND + 0xB3) == "xor r8d, r8d" and
            T(B, BIND + 0xB9) == "add edx, ebp" and T(B, BIND + 0xBE) == "lea rcx, [r15 + rax*4]" and
            T(B, BIND + 0xC2) == "call 0x3846f0" and T(B, BIND + 0xC9) == "add dword ptr [rbx], ebp" and
            T(B, BIND + 0xD4) == "cmp rdi, r14" and B[BIND + 0xD7].mnemonic == "jle" and
            B[BIND + 0xD7].direct_target() == BIND + 0xAF and writers(B, "rbp", BIND + 0x6C, BIND + 0xED) == [])
    sites = [(a - BIND, m["base"], m["disp"], m["size"]) for a, m in nw]
    R.check("the binder's own non-stack stores are exactly seven: [rcx] QWORD (+ 0x4), [rdx + 0xc] (+ 0x1E), [r8 + "
            "0x10] (+ 0x2E), [r8 + 0x18] (+ 0x3F), [r8 + 0x1c] (+ 0x50), [rdi + 0x14] (+ 0x72), [rbx] (+ 0xC9); none "
            "has displacement 4 or 8",
            sites == [(0x4, "rcx", 0, 8), (0x1E, "rdx", 0xC, 4), (0x2E, "r8", 0x10, 4), (0x3F, "r8", 0x18, 4),
                      (0x50, "r8", 0x1C, 4), (0x72, "rdi", 0x14, 4), (0xC9, "rbx", 0, 4)] and
            not [s for s in sites if s[2] in (4, 8)], str(sites))
    R.check("conditional order (ASTRA's producer-01 rejection): from the entry the encoder call + 0x6D is reachable "
            "without the +0xC store + 0x1E (a zero +0xC skips it), but on the nonzero-+0xC path (from + 0x1C) every path "
            "to + 0x6D passes + 0x1E",
            BIND + 0x6D in B.reach(BIND, avoid=[BIND + 0x1E]) and
            BIND + 0x6D in B.reach(BIND + 0x1C) and BIND + 0x6D not in B.reach(BIND + 0x1C, avoid=[BIND + 0x1E]))
    C = Body(img, CHILD, CHILD_END)
    R.check("child binder: R8D homed (+ 0x0); + 0x14 `call 0020E620` on its RDX and + 0x19 `mov dword ptr [rdi], "
            "eax` - the encoded value into the entry; full RDX == 0 -> return (+ 0x1B / + 0x1E); two decodes (+ 0x30, "
            "+ 0x3A); depth = the homed R8D (+ 0x3F `mov ecx, dword ptr [rsp + 0x50]`); + 0x60 `test ecx, ecx` / "
            "+ 0x62 `je` + 0x90 `add dword ptr [rbx], ebp`: at depth 0 every one of the count + 1 entries gets += "
            "its base, and the only self-call (+ 0x7B, R8D = depth - 1) lies behind that test",
            T(C, CHILD) == "mov dword ptr [rsp + 0x18], r8d" and T(C, CHILD + 0x11) == "mov rcx, rdx" and
            T(C, CHILD + 0x14) == "call 0x20e620" and T(C, CHILD + 0x19) == "mov dword ptr [rdi], eax" and
            T(C, CHILD + 0x1B) == "test rbp, rbp" and C[CHILD + 0x1E].direct_target() == CHILD + 0xAA and
            T(C, CHILD + 0x30) == "call 0x20e600" and T(C, CHILD + 0x3A) == "call 0x20e600" and
            T(C, CHILD + 0x3F) == "mov ecx, dword ptr [rsp + 0x50]" and T(C, CHILD + 0x60) == "test ecx, ecx" and
            C[CHILD + 0x62].direct_target() == CHILD + 0x90 and T(C, CHILD + 0x90) == "add dword ptr [rbx], ebp" and
            [a for a, t in C.calls() if t == CHILD] == [CHILD + 0x7B] and
            CHILD + 0x7B not in C.reach(CHILD + 0x60, avoid=[CHILD + 0x64]) and
            T(C, CHILD + 0x6B) == "lea r8d, [rcx - 1]")
    # ---------------- the published indexed route into 01F83530 (re-read of de52023ee)
    tl = leaf(img, TEXLEAF, TEXLEAF_END)
    tt = [c.mnemonic + " " + c.op_str for c in tl]
    R.check("re-read (published de52023ee): the leaf 00210570 (no .pdata) bounds its 16-bit id with `cmp cx, ax` "
            "(AX = 0x4000) and a SIGNED `jge`, then `movsx rax, cx` and `mov qword ptr [rcx + rax*8], rdx` with RCX "
            "= 01F83580 and RAX doubled - 16-byte entries 0x50 above 01F83530",
            img.pdata(TEXLEAF) is None and tt[:4] == ["mov eax, 0x4000", "cmp cx, ax", "jge 0x210591", "movsx rax, cx"]
            and tl[4].address + tl[4].size + tl[4].operands[1].mem.disp == TEXTABLE and tt[5] == "add rax, rax" and
            tt[6] == "mov qword ptr [rcx + rax*8], rdx" and TEXTABLE - ARENA == 0x50, " | ".join(tt[:7]))
    emu_checks(img, R, small)


def emu_checks(img, R, small=False):
    o = emu_results(img)
    c = o["cm1"]
    R.check("emulated countermodel 1 (D = 0x100000, arena 0, +0xC = 0x20, other fields 0): the first bind stores "
            "0x100020, the second bind of the SAME pointer stores 0x200020; the slot holds 0x100000 after both; "
            "the decoder returns 0x100020 then 0x200020; the first bind's only stores are the slot and +0xC",
            c["ok"] and c["first"] == 0x100020 and c["second"] == 0x200020 and c["slot1"] == c["slot2"] == D0 and
            c["dec1"] == 0x100020 and c["dec2"] == 0x200020 and
            [(w[0], w[1], w[2]) for w in c["w1"]] == [(BIND + 0x4, SLOT, 8), (BIND + 0x1E, D0 + 0xC, 4)],
            "%X %X slot %X/%X dec %X/%X" % (c["first"], c["second"], c["slot1"], c["slot2"], c["dec1"], c["dec2"]))
    c = o["cm2"]
    R.check("emulated countermodel 2 (arena 0x100001000, +0x14 = 0x100, so M = 0x100100): +0x14 receives the "
            "ENCODED 0xFF100; the binder then reads the sub-directory count at the full 64-bit decode 0x100100100 "
            "(WORD, from + 0x98) and adds M to its last entry there (+ 0xC9); nothing at the low32 address 0x100100 "
            "is written; low32(decode) = M but decode != M",
            c["ok"] and c["stored"] == 0xFF100 and c["decoded"] == 0x100100100 and
            c["count_read"] == [(BIND + 0x98, HI + 0x100, 2)] and
            [(w[1], w[3]) for w in c["last_write"]] == [(HI + 0x104, 0x10 + 0x100100)] and not c["low_touched"] and
            c["decoded"] & 0xFFFFFFFF == c["M"] and c["decoded"] != c["M"],
            "stored %X decoded %X reads %s" % (c["stored"], c["decoded"], c["count_read"]))
    c = o["cm3"]
    R.check("emulated countermodel 3 (arena 0, +0x14 = 4, so the sub-directory is D+4 with WORD count 0): the "
            "last-entry add at + 0xC9 (003846B9) writes D+8: DWORD 60 becomes 0x100040, its WORD stride 64; +0x14 "
            "holds 0x100004",
            c["ok"] and c["after_dword"] == 0x100040 and c["after_dword"] & 0xFFFF == 64 and
            c["stored14"] == 0x100004 and [w[0] for w in c["store_sites"]] == [BIND + 0xC9],
            "after %X stored14 %X sites %s" % (c["after_dword"], c["stored14"],
                                                ["%X" % w[0] for w in c["store_sites"]]))
    c = o["nest"]
    R.check("emulated two-level directory (+0x14 = 0x200, M = 0x100200; count 2; children of count 1 and 0): "
            "003846F0 is entered exactly twice, from the binder (return + 0xC7), with (RCX, RDX, R8D) = (0x100204, "
            "0x100500, 0) and (0x100208, 0x100600, 0) - entry + M, not entry + D; each child stores its encoded base "
            "into its entry and adds that base to all count + 1 of its own entries; the binder's last entry += M; "
            "no child calls itself",
            c["ok"] and c["stored14"] == 0x100200 and
            c["child"] == [(0x100204, 0x100500, 0, BIND + 0xC7), (0x100208, 0x100600, 0, BIND + 0xC7)] and
            c["e"] == [0x100500, 0x100600, 0x100700, 0x100510, 0x100520, 0x100630],
            "child %s e %s" % ([("%X" % a, "%X" % b, d, "%X" % f) for a, b, d, f in c["child"]],
                               ["%X" % x for x in c["e"]]))
    R.check("emulated: a null descriptor stores the slot (QWORD 0) and returns with no other store or call; an "
            "all-zero descriptor stores only the slot",
            o["null"]["ok"] and [(w[0], w[1], w[3]) for w in o["null"]["writes"]] == [(BIND + 0x4, SLOT, 0)] and
            not o["null"]["trace"] and o["zero"]["ok"] and
            [(w[0], w[1], w[3]) for w in o["zero"]["writes"]] == [(BIND + 0x4, SLOT, D0)] and not o["zero"]["trace"])
    R.check("emulated 60 random plain-field binds at three descriptor addresses: each of +0xC/+0x10/+0x18/+0x1C "
            "becomes x == 0 ? 0 : low32(x + low32(D)), and the slot holds D", not o["rand"], "; ".join(o["rand"][:2]))
    R.check("emulated 200 random leaf inputs: 0020E600 returns zero-extend(ECX) + QWORD [01F83530] mod 2^64 and "
            "reads exactly those 8 bytes; 0020E620 returns low32(ECX - DWORD [01F83530]) zero-extended and reads "
            "exactly those 4 bytes; neither writes", not o["leaves"], "; ".join(o["leaves"][:2]))
    ch = chain_emu(img)
    R.check("emulated chain: registrar + 0x14B with QWORD [0208E680] -> a directory whose DWORD +0x3C is 0x80001000 "
            "reaches the wrapper with ECX = 0x80001000; the wrapper reaches the binder with RCX = 02EBF138 and RDX = "
            "sign-extended ECX (0xFFFFFFFF80001000, 0x1000, 0xFFFFFFFFFFFFFFF0), whatever RCX's upper half was",
            ch["reg"]["ok"] and ch["reg"]["ecx"] == 0x80001000 and
            all(ok and rcx_ == SLOT and rdx_ == sext32(inp) for ok, rcx_, rdx_, inp in ch["wrap"]) and [x[2] for x in ch["wrap"]] == [0xFFFFFFFF80001000, 0x1000, 0xFFFFFFFFFFFFFFF0],
            str([(x[0], "%X" % x[1], "%X" % x[2]) for x in ch["wrap"]]))
    r, r2 = texleaf_emu(img)
    R.check("emulated re-read of the published route: id 0xFFFB stores the QWORD argument at 01F83530 (and the DWORD "
            "at 01F83538); id 0x4000 stores nothing",
            r["ok"] and [(w[1], w[2], w[3]) for w in r["writes"]] == [(ARENA, 8, 0x1122334455667788), (ARENA + 8, 4, 0x99)]
            and r2["ok"] and not r2["writes"], str([("%X" % w[1], w[2]) for w in r["writes"]]))
    return o


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
    """Instructions in .text with a rip-relative or image-base-relative disp32 whose access (or lea) meets [lo, hi).
    Hits outside any .pdata record are decoded back 1..15 bytes and reported separately as unanchored."""
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
                    t = (mm.disp & 0xFFFFFFFF) + img.base
                else:
                    continue
                if t < hi and t + max(op.size, 1) > lo:
                    rec = (ci.mnemonic + " " + ci.op_str, t, op.size, ci.reg_name(mm.base) if mm.base else None)
                    if h in unresolved:
                        unanchored.append((ci.address, rec))
                    else:
                        found[ci.address] = rec
    return found, unresolved, unanchored


def census_checks(img, R):
    print("== raw direct-reference census (E8/E9 rel32 and 0F 8x jcc, .text)")
    rc = raw_refs(img, [REG, WRAP, BIND, CHILD])
    for t, nm in ((REG, "registrar"), (WRAP, "wrapper"), (BIND, "binder"), (CHILD, "child")):
        R.note("%s %08X raw direct references (%d): %s" % (nm, t, len(rc[t]), ", ".join(
            "%X %s" % x for x in rc[t][:12]) + (" ..." if len(rc[t]) > 12 else "")))
    R.check("the wrapper 00237FC0 has exactly one raw direct reference, the registrar's call at 00236D85 (+ 0x155); "
            "the registrar 00236C30 has exactly one, a tail `jmp` at 0023886F",
            rc[WRAP] == [(REG + 0x155, "call")] and rc[REG] == [(0x23886F, "jmp")])
    print("== slot census (rip-relative and image-base-relative disp32 meeting 02EBF138 .. + 8)")
    found, unres, unanch = disp_census(img, SLOT, SLOT + 8)
    lea = sorted(a for a in found if found[a][0].startswith("lea"))
    wr = sorted(a for a in found if not found[a][0].startswith(("lea", "cmp", "test")) and
                found[a][0].split(" ", 1)[1].startswith(("qword ptr [rip", "dword ptr [rip", "word ptr [rip",
                                                          "byte ptr [rip")))
    rd = sorted(a for a in found if a not in lea and a not in wr)
    R.note("02EBF138: %d anchored instructions - %d form its address (lea) %s, %d store to it %s, %d read it; "
           "unanchored readings %d" % (len(found), len(lea), ["%X" % a for a in lea], len(wr), ["%X" % a for a in wr],
                                       len(rd), len(unanch)))
    R.check("02EBF138 census: exactly one instruction forms the slot's address, the wrapper's `lea` (00237FC0 + 0x15); "
            "no instruction stores to it by displacement; every other hit is a read",
            lea == [WRAP + 0x15] and not wr and not unanch and
            all(found[a][0].startswith(("mov", "cmp")) for a in rd))
    print("== image-address base census (01F83530 .. + 8)")
    found, unres, unanch = disp_census(img, ARENA, ARENA + 8)
    R.note("01F83530: anchored %d %s; unresolved candidates %s; decode-back readings %s" % (
        len(found), ["%X %s" % (a, v[0]) for a, v in sorted(found.items())], ["%X" % h for h in unres],
        ["%X %s" % (a, v[0]) for a, v in unanch]))
    R.check("01F83530 census: no .pdata-anchored instruction accesses it by displacement; the candidates lie in the two "
            "leaves (no .pdata), whose true instructions are the decoder's QWORD read and the encoder's DWORD read",
            not found and all(DEC <= h < DEC_END or ENC <= h < ENC_END for h in unres) and len(unres) >= 2)


# ------------------------------------------------------------------ packet integrity
def evdir():
    return os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(find_exe())))),
                        "FFXII TZA", "_experiments", "evidence", SLUG)


def git(*args):
    top = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True,
                         cwd=os.path.dirname(os.path.abspath(__file__))).stdout.strip()
    return subprocess.run(["git"] + list(args), capture_output=True, cwd=top).stdout


def packet_checks(img, R, emu):
    ev = evdir()
    for fn in ("binding-source-01.json", "binding-helper-source-01.json", "retained-resolver-source-01.json",
               "retained-encoder-source-01.json"):
        s = json.load(open(os.path.join(ev, fn)))
        bad = []
        for r in s["ranges"]:
            a, b = int(r["start"], 16), int(r["end_exclusive"], 16)
            ok = hashlib.sha256(img.read(a, b - a)).hexdigest() == r["sha256"]
            if "instructions" in r:
                ok = ok and b"".join(bytes.fromhex(i["bytes"]) for i in r["instructions"]) == img.read(a, b - a)
            if not ok:
                bad.append(r["start"])
        R.check("%s: every range (%s) hashes to this image's bytes and its instruction records concatenate to them" % (
            fn, ", ".join("%s..%s" % (r["start"], r["end_exclusive"]) for r in s["ranges"])), not bad, str(bad))
    bad = []
    for fn in ("binding-extents-01.json", "binding-helper-extents-01.json"):
        x = json.load(open(os.path.join(ev, fn)))
        for b in x["bodies"]:
            s, e = int(b["entry"], 16), int(b["end_exclusive"], 16)
            ents, ok = img.pdata_cover(s, e)
            if not (ok and bytes.fromhex(b["physical_bytes"]) == img.read(s, e - s) and b["bytes"] == e - s and
                    hashlib.sha256(img.read(s, e - s)).hexdigest() == b["sha256"] and
                    [(int(r["begin"], 16), int(r["end_exclusive"], 16)) for r in b["records"]] ==
                    [(p, q) for p, q, fl, rr in ents]):
                bad.append(b["entry"])
    R.check("binding-extents-01 and binding-helper-extents-01: each body's physical bytes, size, sha256 and .pdata "
            "records equal this image's", not bad, str(bad))
    lin = [("retained-resolver-source-01.json", "d34aa6837ec0c0ed442d0cbfa0d71f5b3e442a02",
            "Database/FFXII TZA/_experiments/evidence/skeletonref-producer-slice/source-01.json"),
           ("retained-encoder-source-01.json", "134687c7d25bd0f1a4e46ae98d4088532e55537c",
            "Database/FFXII TZA/_experiments/evidence/ov21-count-publication-window/source-01.json")]
    bad = []
    for mine, commit, path in lin:
        b = git("show", "%s:%s" % (commit, path))
        if not b or b != open(os.path.join(ev, mine), "rb").read():
            bad.append(mine)
    R.check("lineage: retained-resolver-source-01.json is byte-identical to d34aa6837's skeletonref-producer-slice "
            "source-01.json and retained-encoder-source-01.json to 134687c7d's ov21-count-publication-window "
            "source-01.json", not bad, str(bad))
    res = json.load(open(os.path.join(ev, "result-02.json")))
    sf = [(int(f["offset"], 16), int(f["load"], 16), int(f["store"], 16)) for f in res["facts"]["scalar_fields"]]
    R.check("result-02's four scalar fields (offset, load, store) equal the binder's: +0xC 00384600/0038460E, +0x10 "
            "00384614/0038461E, +0x18 00384625/0038462F, +0x1C 00384636/00384640",
            sf == [(0xC, BIND + 0x10, BIND + 0x1E), (0x10, BIND + 0x24, BIND + 0x2E), (0x18, BIND + 0x35, BIND + 0x3F),
                   (0x1C, BIND + 0x46, BIND + 0x50)], str(sf))
    cm = res["facts"]["countermodels"]
    R.check("result-02's three countermodels equal this review's emulation of the original bytes: 0x100020 / "
            "0x200020; encoded 0xFF100, decoded 0x100100100; store 003846B9, stride 60 -> 64, DWORD 0x100040; all "
            "marked executed false",
            int(cm[0]["first_stored_rows"], 16) == emu["cm1"]["first"] and
            int(cm[0]["second_stored_rows"], 16) == emu["cm1"]["second"] and
            int(cm[1]["stored_encoded"], 16) == emu["cm2"]["stored"] and
            int(cm[1]["decoded_full64"], 16) == emu["cm2"]["decoded"] and
            int(cm[1]["rebased_subdir_low32"], 16) == emu["cm2"]["M"] and
            int(cm[2]["original_store"], 16) == emu["cm3"]["store_sites"][0][0] and cm[2]["before_stride"] == 60 and
            cm[2]["after_stride"] == emu["cm3"]["after_dword"] & 0xFFFF and
            int(cm[2]["after_dword"], 16) == emu["cm3"]["after_dword"] and all(c["executed"] is False for c in cm))
    rd = " ".join(open(os.path.join(ev, "README.md"), encoding="utf-8").read().split())
    R.check("packet README keeps open: call-window writer exclusion unresolved, the overlap model not a stock action "
            "table, ownership/lifetime and natural reachability OPEN, no natural double bind claimed",
            "Actual call-window writer exclusion remains unresolved" in rd and
            "not a stock action table" in rd and "remain OPEN" in rd and "not a native call" in rd and
            "proof of natural double binding" in rd)


CONTROLS = [
    ("binder + 0x4 slot store removed (`mov qword ptr [rcx], rdx` -> 3-byte NOP)", BIND + 0x4, bytes.fromhex("0f1f00")),
    ("binder + 0x1C `add eax, edx` -> `add eax, eax` (+0xC not rebased by D)", BIND + 0x1C, bytes.fromhex("03c0")),
    ("binder + 0x1A `je` -> `jmp` (+0xC never rebased)", BIND + 0x1A, bytes.fromhex("eb")),
    ("binder + 0x6D encoder call -> 5-byte NOP (+0x14 keeps the resolved M)", BIND + 0x6D, bytes.fromhex("0f1f440000")),
    ("decoder: REX.W dropped (`add eax, dword ptr [01F83530]`, a DWORD arena)", DEC + 0x2, bytes.fromhex("90")),
    ("encoder direction: `sub ecx, ...` -> `add ecx, ...`", ENC, bytes.fromhex("03")),
    ("wrapper + 0xF `movsxd rdx, ecx` -> `mov edx, ecx` + NOP (zero extension)", WRAP + 0xF, bytes.fromhex("8bd190")),
    ("wrapper + 0x15 slot lea -> 02EBF140", WRAP + 0x18, struct.pack("<i", 0x02EBF140 - (WRAP + 0x1C))),
    ("registrar + 0x152 directory field +0x3C -> +0x40", REG + 0x154, bytes([0x40])),
    ("binder + 0xC9 last-entry `add dword ptr [rbx], ebp` -> NOP", BIND + 0xC9, bytes.fromhex("6690")),
    ("binder + 0x1E +0xC store retargeted to +8 (`mov dword ptr [rdx + 8], eax`)", BIND + 0x20, bytes([0x08])),
    ("binder + 0xB3 `xor r8d, r8d` -> `mov r8d, ebp` (nonzero depth)", BIND + 0xB3, bytes.fromhex("448bc5")),
    ("child + 0x62 depth test's `je` -> NOP NOP", CHILD + 0x62, bytes.fromhex("9090")),
    ("encoder + 0x6 `mov eax, ecx` -> `mov dword ptr [rcx], eax` (a leaf store)", ENC + 0x6, bytes.fromhex("8901")),
    ("binder + 0x21 slot reload `mov r8, qword ptr [rcx]` -> `mov r8, rdx`", BIND + 0x21, bytes.fromhex("4c8bc2")),
    ("binder + 0x5C +0x14 zero test `je` -> always taken (`nop; jmp`)", BIND + 0x5C, bytes.fromhex("90e9")),
    ("route leaf + 0x8 signed `jge` -> unsigned `jae`", TEXLEAF + 0x8, bytes([0x73])),
]


def main():
    img = Img.load()
    R = Rep("rv_binding")
    print("== packet integrity")
    csha = hashlib.sha256(git("show", "%s:Database/FFXII TZA/_experiments/evidence/%s/manifest.json" %
                              (PRODUCER, SLUG))).hexdigest()
    check_manifest(R, SLUG, csha)
    R.note("committed manifest at %s: sha256 %s" % (PRODUCER[:9], csha))
    census_checks(img, R)
    print("== shipping-image re-derivation")
    checks(img, R)
    emu = emu_results(img)
    packet_checks(img, R, emu)
    print("== controls (each patched private image must FAIL at least one check above)")
    Rn = Rep("null")
    Rn.quiet = True
    P0 = img.patched(BIND + 0x4, img.read(BIND + 0x4, 3))
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
