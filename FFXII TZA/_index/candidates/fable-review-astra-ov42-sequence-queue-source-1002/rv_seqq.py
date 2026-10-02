"""rv_seqq.py - FABLE independent re-derivation for ASTRA packet ov42-sequence-queue-source (0c4215736, OV-42).

Own reader (rvlib.py: struct + capstone 5, copied unchanged from the filecache-route2-commit-key review, sha256
69f9bc40be32abcc...).  Does not import or run ASTRA's prove.py, prove_owner_reload_order.py, capture drivers,
control.py, extent.py, freeze/publication scripts or the shared role adapter (reg_tracking.py).

Method:
  * image sha256; the .pdata chain of the special-presentation sequence routine 00306760 followed record by record
    (five records, the last four CHAININFO, resolved to the root); the 936 physical bytes split into 911 code bytes
    (decoded linearly and exactly, ending at the one ret), the NOP at + 0x38F and six DWORDs at + 0x390 .. + 0x3A8
    that the dispatch load addresses; int3 padding up to the next root;
  * the dispatch head re-read (DEC, unsigned bound, CDQE, image-base LEA, indexed DWORD load, ADD, JMP); the six
    table targets resolved and the local CFG walked from each: which kinds reach the queue store 00306760 + 0x174;
  * RDI provenance, the subtraction width, the two descriptor loads, the DIV operand width and signedness, the
    absence of any test of the divisor, the FFFF compare width and the - 0xD0, the store width and target;
  * a concrete emulation (unicorn) of the ORIGINAL routine: a full run from the entry for kinds 0..7, and the kind-4
    arm over synthetic rows, descriptors and lookup returns.  Every direct callee is stubbed by a code hook (it
    returns at once with a scripted RAX); those callees are the only code not run from the image;
  * a raw E8/E9 rel32 and 0F 8x census of direct references to 00306760;
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

F = 0x00306760
CODE_END = F + 0x38F      # 911 code bytes
NOP = F + 0x38F
TBL = F + 0x390
END = F + 0x3A8           # 936 physical bytes
NEXT_ROOT = 0x00306B10
KIND = {1: F + 0x1D1, 2: F + 0x2DD, 3: F + 0x7B, 4: F + 0xE8, 5: F + 0x298, 6: F + 0x32E}
STORE = F + 0x174
KINDCELL = 0x022C215C
QUEUE = 0x022C2178
UNITCELL = 0x022C218C
COUNTCELL = 0x022C21B4
STATECELL = 0x022C2160
DESC = 0x02EBF138
SEQCTX = 0x02EBF190
LOOKUP = 0x0020E600
SLUG = "ov42-sequence-queue-source"
PRODUCER = "0c4215736"
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


def queue_formula(row, base, stride):
    d = (row - base) & 0xFFFFFFFF
    q = d // stride
    w = q & 0xFFFF
    return 0xFFFFFFFF if w == 0xFFFF else (w - 0xD0) & 0xFFFFFFFF


# ------------------------------------------------------------------ emulation of the original code
class Emu(object):
    STK, RET, SCR, ROW, UNIT, DSC = 0x7F000000, 0x7E000000, 0x50000000, 0x40000000, 0x41000000, 0x42000000

    def __init__(self, img, callees):
        from unicorn import Uc, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE, UC_HOOK_MEM_WRITE, UC_HOOK_INTR
        from unicorn import UC_HOOK_MEM_READ_UNMAPPED, UC_HOOK_MEM_FETCH_UNMAPPED, UC_HOOK_MEM_WRITE_UNMAPPED
        from unicorn import x86_const as X
        self.X = X
        mu = self.mu = Uc(UC_ARCH_X86, UC_MODE_64)
        pages = set()
        spans = [(F, END), (0x022BE000, 0x022C3000), (0x02EBF000, 0x02EC0000)]
        for c in callees:
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
        for a in (self.STK, self.SCR, self.ROW, self.UNIT, self.DSC):
            mu.mem_map(a, 0x10000)
        mu.mem_map(self.RET, 0x1000)
        self.callees = set(callees)
        self.stub_rax = {}
        self.swap_desc = None
        self.until = None
        self.trace, self.writes, self.intr, self.fault, self.left = [], [], None, None, None

        def ch(uc, addr, size, ud):
            if addr == self.until:
                uc.emu_stop()
                return
            if addr in self.callees:
                rsp = uc.reg_read(X.UC_X86_REG_RSP)
                self.trace.append((addr, uc.reg_read(X.UC_X86_REG_RCX), uc.reg_read(X.UC_X86_REG_RDX)))
                if addr == LOOKUP and self.swap_desc is not None:
                    uc.mem_write(DESC, struct.pack("<Q", self.swap_desc))
                uc.reg_write(X.UC_X86_REG_RAX, self.stub_rax.get(addr, self.SCR + 0x100))
                uc.reg_write(X.UC_X86_REG_RIP, struct.unpack("<Q", bytes(uc.mem_read(rsp, 8)))[0])
                uc.reg_write(X.UC_X86_REG_RSP, rsp + 8)
                return
            if addr != self.RET and not (F <= addr < CODE_END):
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

    def setup(self, kind, stride, key, row_hi=0, row_off=0, b1c=0, desc2=None):
        mu = self.mu
        for a in (self.SCR, self.ROW, self.UNIT, self.DSC):
            mu.mem_write(a, b"\0" * 0x10000)
        mu.mem_write(KINDCELL, struct.pack("<I", kind & 0xFFFFFFFF))
        mu.mem_write(QUEUE, struct.pack("<I", 0x5A5A5A5A))
        mu.mem_write(UNITCELL, struct.pack("<I", 0x5A5A5A5A))
        mu.mem_write(STATECELL, struct.pack("<I", 0x5A5A5A5A))
        # descriptor A at DSC, descriptor B at DSC+0x100
        mu.mem_write(self.DSC + 8, struct.pack("<H", stride))
        mu.mem_write(self.DSC + 0xC, struct.pack("<I", key))
        if desc2 is not None:
            mu.mem_write(self.DSC + 0x108, struct.pack("<H", desc2[0]))
            mu.mem_write(self.DSC + 0x10C, struct.pack("<I", desc2[1]))
        mu.mem_write(DESC, struct.pack("<Q", self.DSC))
        mu.mem_write(SEQCTX, struct.pack("<Q", self.SCR))
        # unit (RCX): +0x694/+0x695/+0x696 empty, +0x698 -> a scratch record, +8 identity, +0x77C count 0
        mu.mem_write(self.UNIT + 0x694, b"\xff\xff\xff")
        mu.mem_write(self.UNIT + 0x698, struct.pack("<Q", self.SCR + 0x800))
        mu.mem_write(self.UNIT + 8, struct.pack("<I", 0xCAFE0008))
        mu.mem_write(self.ROW + row_off + 0x1C, bytes([b1c]))
        return (row_hi << 32) | (self.ROW + row_off)

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
        r["queue"] = struct.unpack("<I", bytes(self.mu.mem_read(QUEUE, 4)))[0]
        r["qwrites"] = [w for w in self.writes if w[1] == QUEUE]
        r["trace"], r["intr"], r["fault"], r["left"] = list(self.trace), self.intr, self.fault, self.left
        return r


def emu_checks(img, R, small=False):
    B = Body(img, F, CODE_END)
    callees = sorted(set(t for a, t in B.calls()))
    E = Emu(img, callees)
    BASEV = 0x0000000123450000    # 20E600 return (only its low 32 bits matter)
    # ---- full routine from the entry, kinds 0..7
    res = {}
    for k in range(0, 8):
        row = E.setup(k, 60, 0x1D74, row_off=0x200 + 60 * 3)
        E.stub_rax = {LOOKUP: Emu.ROW + 0x200, 0x00236850: 0}
        r = E.run(F, Emu.UNIT, row, Emu.RET)
        res[k] = r
    writers_k = [k for k in range(8) if res[k]["qwrites"]]
    clean = all(res[k]["rip"] == Emu.RET and not res[k]["fault"] and not res[k]["intr"] and not res[k]["left"]
                and res[k]["rdi"] == 0xDDDDDDDDDDDDDDDD and res[k]["rbx"] == 0xBBBBBBBBBBBBBBBB
                and res[k]["rsi"] == 0x5151515151515151 and res[k]["r14"] == 0xEEEEEEEEEEEEEEEE for k in range(8))
    R.check("emulated full routine from the entry, kind cell 022C215C = 0..7 (row + 0x1C != 8): every run returns "
            "with RBX/RSI/RDI/R14 restored; the queue 022C2178 is written in exactly one run, kind 4, once, as a "
            "4-byte store from 00306760 + 0x174",
            clean and writers_k == [4] and [(w[0], w[2]) for w in res[4]["qwrites"]] == [(STORE, 4)],
            "writers %s; %s" % (writers_k, "; ".join("k%d rip %X fault %s intr %s left %s" % (
                k, res[k]["rip"], res[k]["fault"], res[k]["intr"], res[k]["left"]) for k in range(8)
                if res[k]["rip"] != Emu.RET or res[k]["fault"] or res[k]["intr"])))
    R.check("emulated: kinds 0 and 7 call no arm callee - their first callee is the tail's 00236850 (the "
            "`ja` to 00306760 + 0x33A); kind 4's callees run 00306D90, 00861EC0, 0030D720, 0030D550, 0020E600, then "
            "the tail",
            [t[0] for t in res[0]["trace"]][:1] == [0x236850] and [t[0] for t in res[7]["trace"]][:1] == [0x236850]
            and [t[0] for t in res[4]["trace"]][:5] == [0x306D90, 0x861EC0, 0x30D720, 0x30D550, LOOKUP],
            "k0 %s / k4 %s" % (["%X" % t[0] for t in res[0]["trace"]], ["%X" % t[0] for t in res[4]["trace"]]))
    R.check("emulated: kind 4 queues the coherent row 3 (row = base + 3*60) as (3 - 0xD0) mod 2^32 = FFFFFF33, and "
            "the lookup receives ECX = descriptor DWORD +0xC (1D74)",
            res[4]["queue"] == 0xFFFFFF33 and [t for t in res[4]["trace"] if t[0] == LOOKUP][0][1] & 0xFFFFFFFF == 0x1D74,
            "queue %X" % res[4]["queue"])
    # ---- kind-4 arm alone, 00306760 + 0xE8 .. + 0x17A, RBX = unit, RDI = row
    ARM_END = F + 0x17A

    def arm(row, stride, base=BASEV, desc2=None, key=0x1D74):
        E.setup(4, stride, key, desc2=desc2)
        E.stub_rax = {LOOKUP: base}
        E.swap_desc = (Emu.DSC + 0x100) if desc2 is not None else None
        r = E.run(KIND[4], 0, 0, ARM_END, regs={"rbx": Emu.UNIT, "rdi": row, "r14": img.base})
        E.swap_desc = None
        return r

    bad = []
    for i in CANDS:
        r = arm((BASEV & 0xFFFFFFFF) + 60 * i, 60)
        if r["queue"] != i - 208 or r["rip"] != ARM_END or r["fault"] or r["intr"]:
            bad.append("%d -> %X rip %X fault %s intr %s left %s" % (i, r["queue"], r["rip"], r["fault"], r["intr"], r["left"]))
    R.check("emulated kind-4 arm, coherent row = base + 60*id: each of 511..534 queues id - 208 = 303..326", not bad,
            "; ".join(bad[:3]))
    edge = [
        ("row 0x113 (275)", (BASEV & 0xFFFFFFFF) + 60 * 0x113, 60, 0x113 - 208),
        ("id 0xCF -> FFFFFFFF (the same DWORD as the sentinel)", (BASEV & 0xFFFFFFFF) + 60 * 0xCF, 60, 0xFFFFFFFF),
        ("id 0 -> FFFFFF30", (BASEV & 0xFFFFFFFF), 60, 0xFFFFFF30),
        ("quotient FFFF -> FFFFFFFF", (BASEV & 0xFFFFFFFF) + 0xFFFF, 1, 0xFFFFFFFF),
        ("quotient 1FFFF (low16 FFFF) -> FFFFFFFF", (BASEV & 0xFFFFFFFF) + 0x1FFFF, 1, 0xFFFFFFFF),
        ("quotient 10005 (low16 5) -> FFFFFF35", (BASEV & 0xFFFFFFFF) + 0x10005, 1, 0xFFFFFF35),
        ("off-stride row: floor ((60*511 + 59) / 60) = 511 -> 303", (BASEV & 0xFFFFFFFF) + 60 * 511 + 59, 60, 303),
        ("row 60 below base: D = 2^32 - 60 unsigned", (BASEV & 0xFFFFFFFF) - 60, 60,
         queue_formula((BASEV & 0xFFFFFFFF) - 60, BASEV & 0xFFFFFFFF, 60)),
        ("row with other upper 32 bits (7_xxxxxxxx): only low32 enters", (7 << 32) | ((BASEV & 0xFFFFFFFF) + 60 * 520),
         60, 520 - 208),
        ("stride 0xFFFF (u16 max, zero-extended)", (BASEV & 0xFFFFFFFF) + 0xFFFF * 600, 0xFFFF, 600 - 208),
    ]
    bad = []
    for name, row, s, want in edge:
        r = arm(row, s)
        if r["queue"] != want or r["queue"] != queue_formula(row, BASEV, s) or r["fault"] or r["intr"]:
            bad.append("%s: got %X want %X" % (name, r["queue"], want))
    R.check("emulated kind-4 arm, %d edge cases (row 0x113; id 0xCF and quotients FFFF / 1FFFF give FFFFFFFF; "
            "low16 wrap; floor; a row below the base wraps as unsigned 32-bit; upper 32 bits of the row ignored; "
            "stride FFFF): each equals the packet formula" % len(edge), not bad, "; ".join(bad[:3]))
    rnd = random.Random(42)
    n = 10 if small else 60
    bad = []
    for _ in range(n):
        row = rnd.getrandbits(64)
        base = rnd.getrandbits(64)
        s = rnd.choice([1, 2, 3, 60, 0x3C, 0x80, 0x1234, 0xFFFF, rnd.randrange(1, 0x10000)])
        r = arm(row, s, base=base)
        if r["queue"] != queue_formula(row, base, s) or r["fault"] or r["intr"]:
            bad.append("row %X base %X s %X: %X vs %X" % (row, base, s, r["queue"], queue_formula(row, base, s)))
    R.check("emulated kind-4 arm, %d random 64-bit rows / lookup returns / strides 1..FFFF: each queue DWORD equals "
            "((low32(row) - low32(base)) mod 2^32) // S, low 16 bits, FFFF -> FFFFFFFF else - 0xD0" % n, not bad,
            "; ".join(bad[:2]))
    # two descriptors: the lookup stub repoints 02EBF138 between the two loads
    r = arm((BASEV & 0xFFFFFFFF) + 60 * 520, 60, desc2=(30, 0x9999))
    key = [t for t in r["trace"] if t[0] == LOOKUP][0][1] & 0xFFFFFFFF
    R.check("emulated: when 02EBF138 is repointed during the lookup call, the key came from the first descriptor "
            "(+0xC = 1D74) and the divisor from the second (+8 = 30): 60*520 / 30 = 1040 -> queue 1040 - 208 = 832",
            key == 0x1D74 and r["queue"] == 1040 - 208, "key %X queue %X" % (key, r["queue"]))
    r = arm((BASEV & 0xFFFFFFFF) + 60 * 520, 0)
    R.check("emulated: stride WORD 0 -> divide error (#DE, interrupt 0) at the DIV 00306760 + 0x158; the queue is not "
            "written (no zero-divisor guard)",
            r["intr"] is not None and r["intr"][0] == 0 and r["intr"][1] == F + 0x158 and not r["qwrites"],
            "intr %s fault %s rip %X" % (r["intr"], r["fault"], r["rip"]))


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


def checks(img, R, small=False):
    R.check("image sha256 = %s..." % SHA_PIN[:20], hashlib.sha256(img.d).hexdigest() == SHA_PIN or
            getattr(img, "_private", False))
    # ---------------- extent
    ents, ok = img.pdata_cover(F, END)
    R.check("00306760's .pdata: five records tile 00306760 .. + 0x3A8 (936 B) exactly - the root .. + 0x10, then "
            "CHAININFO records + 0x10 .. + 0x62, + 0x62 .. + 0x33A, + 0x33A .. + 0x356, + 0x356 .. + 0x3A8, each "
            "resolving to the root 00306760",
            ok and [(b - F, e - F, fl & 4, r) for b, e, fl, r in ents] ==
            [(0, 0x10, 0, F), (0x10, 0x62, 4, F), (0x62, 0x33A, 4, F), (0x33A, 0x356, 4, F), (0x356, 0x3A8, 4, F)],
            str([(hex(b - F), hex(e - F), fl) for b, e, fl, r in ents]))
    R.check("int3 padding 00306760 + 0x3A8 .. + 0x3B0 up to the next root record 00306B10",
            img.read(END, NEXT_ROOT - END) == b"\xcc" * (NEXT_ROOT - END) and is_root(img, NEXT_ROOT) and
            img.pdata(END) is None)
    B = Body(img, F, CODE_END)
    R.check("code: 00306760 .. + 0x38F (911 B) decodes exactly, and its last instruction is the one `ret` (+ 0x38E)",
            B.exact and B.order[-1] == F + 0x38E and T(B, F + 0x38E) == "ret" and
            [a for a in B.order if B[a].mnemonic == "ret"] == [F + 0x38E])
    R.check("+ 0x38F is a one-byte NOP (90) that no instruction falls into or branches to; + 0x390 .. + 0x3A8 are "
            "six DWORDs (24 B) addressed by the dispatch load, not code",
            img.read(NOP, 1) == b"\x90" and not [a for a in B.order if B[a].direct_target() == NOP] and
            TBL + 24 == END)
    rets, tails, outs = B.exits()
    ind = [a for a in B.order if B[a].mnemonic == "jmp" and B[a].direct_target() is None]
    R.check("local CFG closed: one ret, no tail jump other than the one indirect `jmp rax` (+ 0x79), no branch "
            "leaves the code", rets == [F + 0x38E] and tails == [(F + 0x79, None)] and not outs and ind == [F + 0x79])
    # ---------------- dispatch
    R.check("dispatch head: + 0x4A EAX = DWORD [022C215C] (4 B); + 0x50 `dec eax`; + 0x57 `cmp eax, 5`; + 0x5A "
            "`ja` + 0x33A (unsigned); + 0x60 `cdqe`; + 0x67 R14 = image base (`lea`, rip-relative); + 0x6E EAX = "
            "DWORD [r14 + rax*4 + 0x1E6AF0] = 00306760 + 0x390 + 4*(kind - 1); + 0x76 `add rax, r14`; + 0x79 "
            "`jmp rax`",
            T(B, F + 0x4A).startswith("mov eax, dword ptr [rip") and rip_target(B[F + 0x4A]) == KINDCELL and
            B[F + 0x4A].mems[0]["size"] == 4 and T(B, F + 0x50) == "dec eax" and T(B, F + 0x57) == "cmp eax, 5" and
            T(B, F + 0x5A) == "ja 0x306a9a" and T(B, F + 0x60) == "cdqe" and
            T(B, F + 0x67).startswith("lea r14, [rip") and rip_target(B[F + 0x67]) == img.base and
            T(B, F + 0x6E) == "mov eax, dword ptr [r14 + rax*4 + 0x1e6af0]" and img.base + 0x1E6AF0 == TBL and
            B[F + 0x6E].mems[0]["size"] == 4 and T(B, F + 0x76) == "add rax, r14" and T(B, F + 0x79) == "jmp rax")
    R.check("between the kind load and the jump only the dispatch writes RAX (+ 0x4A, + 0x50, + 0x60, + 0x6E, "
            "+ 0x76) and R14 is written only by the `lea` (+ 0x67)",
            writers(B, "rax", F + 0x4A, F + 0x79) == [F + 0x4A, F + 0x50, F + 0x60, F + 0x6E, F + 0x76] and
            writers(B, "r14", F + 0x4A, F + 0x79) == [F + 0x67])
    tbl = [img.base + img.u32(TBL + 4 * i) for i in range(6)]
    R.check("the six DWORDs resolve to arm entries on instruction boundaries: kind 1 + 0x1D1, kind 2 + 0x2DD, kind 3 "
            "+ 0x7B, kind 4 + 0xE8, kind 5 + 0x298, kind 6 + 0x32E",
            tbl == [KIND[k] for k in range(1, 7)] and all(t in B.ins for t in tbl),
            " ".join("+%X" % (t - F) for t in tbl))
    reach = dict((k, STORE in B.reach(KIND[k])) for k in range(1, 7))
    R.check("local CFG from each arm entry: only kind 4 reaches the queue store + 0x174; the entry's own direct CFG "
            "(the indirect jump and the `ja` default + 0x33A) does not",
            reach == {1: False, 2: False, 3: False, 4: True, 5: False, 6: False} and STORE not in B.reach(F) and
            STORE not in B.reach(F + 0x33A), str(reach))
    into = sorted((a, B[a].direct_target()) for a in B.order if B[a].direct_target() is not None and
                  B[a].mnemonic.startswith("j") and KIND[4] < B[a].direct_target() <= STORE and
                  not (KIND[4] <= a < STORE))
    R.check("no direct branch from outside the kind-4 arm lands in + 0xE8 .. + 0x174, and kind 3's arm ends with "
            "`jmp` + 0x335 at + 0xE3 (no fall-through into kind 4)",
            not into and T(B, F + 0xE3) == "jmp 0x306a95" and B.succ(F + 0xE3) == [F + 0x335], str(into))
    # ---------------- RDI
    R.check("RDI = entry RDX: home save `mov qword ptr [rsp + 0x38], rdi` (+ 0x10), `mov rdi, rdx` (+ 0x15), no "
            "RDX write before it; RDI written only at + 0x15, + 0xBC (kind 3's `sub`), + 0x147 (kind 4's `sub`) "
            "and the reload + 0x348; none on the kind-4 arm before + 0x147",
            T(B, F + 0x10) == "mov qword ptr [rsp + 0x38], rdi" and T(B, F + 0x15) == "mov rdi, rdx" and
            not writers(B, "rdx", F, F + 0x15) and
            writers(B, "rdi") == [F + 0x15, F + 0xBC, F + 0x147, F + 0x348] and
            not writers(B, "rdi", KIND[4], F + 0x147) and F + 0xBC not in B.reach(KIND[4]))
    R.check("the entry path reads row BYTE [rdx + 0x1C] (+ 0x32, `cmp ... , 8`) before the dispatch; the arm "
            "callees between + 0x15 and + 0x147 (00306D90, 00861EC0, 0030D720, 0030D550, 0020E600, and on the "
            "+ 0x1C == 8 path 003098D0 / 003299B0) are trusted to preserve RDI by the Win64 ABI",
            T(B, F + 0x32) == "cmp byte ptr [rdx + 0x1c], 8" and
            [t for a, t in B.calls() if F + 0x15 < a < F + 0x4A] == [0x3098D0, 0x3299B0] and
            [t for a, t in B.calls() if KIND[4] <= a < F + 0x147] == [0x306D90, 0x861EC0, 0x30D720, 0x30D550, LOOKUP])
    # ---------------- the arithmetic
    R.check("first descriptor: + 0x138 RAX = QWORD [02EBF138] (8 B); + 0x13F ECX = DWORD [rax + 0xC] (4 B); "
            "+ 0x142 `call 0020E600`; + 0x147 `sub edi, eax` - a 32-bit subtraction of the lookup's EAX from EDI",
            T(B, F + 0x138).startswith("mov rax, qword ptr [rip") and rip_target(B[F + 0x138]) == DESC and
            B[F + 0x138].mems[0]["size"] == 8 and T(B, F + 0x13F) == "mov ecx, dword ptr [rax + 0xc]" and
            B[F + 0x13F].mems[0]["size"] == 4 and T(B, F + 0x142) == "call 0x20e600" and
            T(B, F + 0x147) == "sub edi, eax" and B[F + 0x147].bytes == b"\x2b\xf8")
    R.check("second descriptor: + 0x149 `xor edx, edx`; + 0x14B RAX = QWORD [02EBF138] again (8 B); + 0x152 ECX = "
            "`movzx ecx, word ptr [rax + 8]` (2 B, zero-extended); + 0x156 `mov eax, edi`; + 0x158 `div ecx` "
            "(F7 F1: unsigned, 32-bit, EDX:EAX / ECX)",
            T(B, F + 0x149) == "xor edx, edx" and T(B, F + 0x14B).startswith("mov rax, qword ptr [rip") and
            rip_target(B[F + 0x14B]) == DESC and B[F + 0x14B].mems[0]["size"] == 8 and
            T(B, F + 0x152) == "movzx ecx, word ptr [rax + 8]" and B[F + 0x152].mems[0]["size"] == 2 and
            T(B, F + 0x156) == "mov eax, edi" and T(B, F + 0x158) == "div ecx" and B[F + 0x158].bytes == b"\xf7\xf1")
    seg = [a for a in B.order if F + 0x142 < a < F + 0x158]
    R.check("two separate descriptor loads: the call 0020E600 (+ 0x142) lies between them; apart from the + 0x11E / + 0x122 byte tests, no compare, test or "
            "branch from the arm entry to the DIV; nothing writes ECX between the WORD load and the DIV, "
            "and EDX is written only by the `xor` there (no zero-divisor guard)",
            [a for a in B.order if rip_target(B[a]) == DESC and KIND[4] <= a < STORE] == [F + 0x138, F + 0x14B] and
            not [a for a in B.order if KIND[4] <= a < F + 0x158 and B[a].mnemonic in ("cmp", "test")
                 and a not in (F + 0x11E, F + 0x122)] and
            not [a for a in seg if B[a].mnemonic.startswith("j")] and
            writers(B, "rcx", F + 0x153, F + 0x158) == [] and writers(B, "rdx", F + 0x142, F + 0x158) == [F + 0x149])
    R.check("the only compares on the arm before the DIV are the two `+0x695`/`+0x696` byte tests (+ 0x11E, "
            "+ 0x122); their branches rejoin at + 0x138; the DIV dominates the store",
            [a for a in B.order if KIND[4] <= a < F + 0x158 and B[a].mnemonic in ("cmp", "test")] ==
            [F + 0x11E, F + 0x122] and B[F + 0x120].direct_target() == F + 0x138 and
            B[F + 0x129].direct_target() == F + 0x138 and B.dominates(F + 0x158, STORE, entry=KIND[4]) and
            B.dominates(F + 0x147, STORE, entry=KIND[4]))
    R.check("the remap: + 0x15A ECX = DWORD [rbx + 8]; + 0x15D EDX = 0xFFFF; + 0x162 `cmp ax, dx` (16-bit); + 0x165 "
            "`je` + 0x171; + 0x167 `movzx eax, ax`; + 0x16A `sub eax, 0xd0`; + 0x16F `jmp` + 0x174; + 0x171 "
            "`or eax, 0xffffffff`; no EAX write between the DIV and the compare",
            T(B, F + 0x15A) == "mov ecx, dword ptr [rbx + 8]" and T(B, F + 0x15D) == "mov edx, 0xffff" and
            T(B, F + 0x162) == "cmp ax, dx" and B[F + 0x162].bytes == b"\x66\x3b\xc2" and
            T(B, F + 0x165) == "je 0x3068d1" and T(B, F + 0x167) == "movzx eax, ax" and
            T(B, F + 0x16A) == "sub eax, 0xd0" and T(B, F + 0x16F) == "jmp 0x3068d4" and
            T(B, F + 0x171) == "or eax, 0xffffffff" and not writers(B, "rax", F + 0x15A, F + 0x162))
    R.check("the store: + 0x174 `mov dword ptr [rip + ...], eax` to 022C2178 (4 B); it is the routine's only write "
            "to the queue",
            T(B, STORE).startswith("mov dword ptr [rip") and rip_target(B[STORE]) == QUEUE and
            B[STORE].mems[0]["size"] == 4 and
            [a for a, m in B.mem_writes() if m["base"] == "rip" and rip_target(B[a]) == QUEUE] == [STORE])
    # ---------------- side facts
    R.check("after the store the arm writes DWORD 0 to 022C21B4 (+ 0x17C) and the unit DWORD +8 (ECX from + 0x15A) "
            "to 022C218C (+ 0x185) - the unit value the queue reader returns - then copies unit +0x77C QWORDs "
            "from +0x780 (stride 0x10) to 022C21B8 + 8*i",
            rip_target(B[F + 0x17C]) == COUNTCELL and rip_target(B[F + 0x185]) == UNITCELL and
            T(B, F + 0x185).endswith("ecx") and not writers(B, "rcx", F + 0x15B, F + 0x185) and
            T(B, F + 0x1AD) == "mov qword ptr [r14 + rcx*8 + 0x21a21b8], rax" and img.base + 0x21A21B8 == 0x022C21B8)
    R.check("kind 3's arm computes the same quotient (+ 0xAD .. + 0xCD: first load, key +0xC, 0020E600, `sub edi, "
            "eax`, second load, WORD +8, unsigned `div ecx`) but passes the full 32-bit EAX as EDX to 0030EC00 "
            "(+ 0xD4) with no FFFF test or - 0xD0, and does not reach the queue",
            rip_target(B[F + 0xAD]) == DESC and T(B, F + 0xB4) == "mov ecx, dword ptr [rax + 0xc]" and
            T(B, F + 0xBC) == "sub edi, eax" and rip_target(B[F + 0xC0]) == DESC and
            T(B, F + 0xC7) == "movzx ecx, word ptr [rax + 8]" and T(B, F + 0xCD) == "div ecx" and
            T(B, F + 0xD2) == "mov edx, eax" and T(B, F + 0xD4) == "call 0x30ec00")
    R.check("every path to the ret passes + 0x37F, which writes DWORD 5 to 022C2160",
            rip_target(B[F + 0x37F]) == STATECELL and T(B, F + 0x37F).endswith(", 5") and
            B.dominates(F + 0x37F, F + 0x38E) and B.dominates(F + 0x37F, F + 0x38E, entry=F + 0x33A))
    emu_checks(img, R, small)
    caller_checks(img, R)


CALLER, CALLER_TBL = 0x00304850, 0x00305044
CALLSITE = CALLER + 0x6FD


def caller_checks(img, R):
    """Reviewer observation (not a packet claim): the one raw direct caller and the row it passes."""
    C = Body(img, CALLER, CALLER_TBL)
    jt = [img.base + img.u32(CALLER_TBL + 4 * i) for i in range(13)]
    R.check("the one raw direct call 00304850 + 0x6FD: RDX = R15 (+ 0x6F7), RCX = RDI (+ 0x6FA), reached only when "
            "`test dword ptr [r15 + 0xc], 0x40000000` (+ 0x6ED) / `je` (+ 0x6F5) finds bit 30 set; then `jmp` + 0x70F",
            C.exact and T(C, CALLER + 0x6F7) == "mov rdx, r15" and T(C, CALLER + 0x6FA) == "mov rcx, rdi" and
            T(C, CALLSITE) == "call 0x306760" and T(C, CALLER + 0x6ED) == "test dword ptr [r15 + 0xc], 0x40000000"
            and T(C, CALLER + 0x6F5) == "je 0x304f54" and T(C, CALLER + 0x702) == "jmp 0x304f5f")
    R.check("R15 before the 13-way phase switch: R13 = WORD [rsi + 0x64] (+ 0x3D), `cmp r13w, bx` (BX = 0x21E) / "
            "`ja` exit (+ 0x8E/+ 0x92); then R15 = 0020E600([02EBF138] + 0xC) (+ 0xCF) and `add r15d, ecx` with ECX = "
            "WORD [02EBF138 reloaded] + 8 * R13W (+ 0xD9 .. + 0xE4, a 32-bit add); a null descriptor or lookup gives "
            "R15 = R14 (+ 0xE9)",
            T(C, CALLER + 0x3D) == "movzx r13d, word ptr [rsi + 0x64]" and T(C, CALLER + 0x58) == "mov ebx, 0x21e" and
            T(C, CALLER + 0x8E) == "cmp r13w, bx" and T(C, CALLER + 0x92) == "ja 0x305017" and
            rip_target(C[CALLER + 0x98]) == DESC and rip_target(C[CALLER + 0xC0]) == DESC and
            T(C, CALLER + 0xC7) == "mov ecx, dword ptr [rax + 0xc]" and T(C, CALLER + 0xCA) == "call 0x20e600" and
            T(C, CALLER + 0xCF) == "mov r15, rax" and rip_target(C[CALLER + 0xD2]) == DESC and
            T(C, CALLER + 0xD9) == "movzx ecx, word ptr [rax + 8]" and T(C, CALLER + 0xDD) == "movzx eax, r13w" and
            T(C, CALLER + 0xE1) == "imul ecx, eax" and T(C, CALLER + 0xE4) == "add r15d, ecx" and
            T(C, CALLER + 0xE9) == "mov r15, r14" and
            CALLER + 0x10A not in C.reach(CALLER, avoid=[CALLER + 0xE4, CALLER + 0xE9]))
    hits = [i for i, t in enumerate(jt) if CALLSITE in C.reach(t)]
    rw = [a for a in C.order if "r15" in C[a].reg_writes and a > CALLER + 0xE9]
    bad = [(i, a) for i in hits for a in rw if a in C.reach(jt[i]) and CALLSITE in C.reach(a)]
    R.check("the call sits in phase case 9 (+ 0x66E .. + 0x70F); in the local CFG, case entries 0..9 reach it (earlier "
            "cases continue into later ones) and 10..12 do not; no R15 write after + 0xE9 lies on any path from a case "
            "entry to the call, so RDX at the call is the R15 formed before the switch",
            hits == list(range(10)) and jt[9] == CALLER + 0x66E and jt[10] == CALLER + 0x712 and not bad,
            "hits %s bad %s" % (hits, bad))


def packet_bytes(img, R):
    ev = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(find_exe())))),
                      "FFXII TZA", "_experiments", "evidence", SLUG)
    s = json.load(open(os.path.join(ev, "source-02.json")))
    rg = [(int(r["start"], 16), int(r["end_exclusive"], 16), r["sha256"]) for r in s["ranges"]]
    R.check("packet's source range 00306760 .. + 0x38F hashes to this image's bytes",
            len(rg) == 1 and rg[0][:2] == (F, CODE_END) and
            hashlib.sha256(img.read(F, CODE_END - F)).hexdigest() == rg[0][2])
    d = json.load(open(os.path.join(ev, "data-01.json")))
    R.check("packet's physical body (936 B) and table bytes equal this image's: body sha256 %s..., table at + 0x390"
            % d["physical_body_sha256"][:12],
            hashlib.sha256(img.read(F, END - F)).hexdigest() == d["physical_body_sha256"] and
            bytes.fromhex(d["table_hex"]) == img.read(TBL, 24) and int(str(d["table_va"]), 16) == TBL)
    rd = open(os.path.join(ev, "README.md"), encoding="utf-8").read()
    R.check("packet README keeps open: kind-to-row/caller/owner consistency, S > 0 as a precondition, arithmetic not "
            "native runs, descriptor initialization, whole OV-42",
            "kind-to-row/caller/owner consistency invariant" in rd and "S>0 is a precondition" in rd and
            "not executed FF12 instructions" in rd and "descriptor initialization" in rd and "whole OV-42" in rd)


def committed_manifest_sha():
    top = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True,
                         cwd=os.path.dirname(os.path.abspath(__file__))).stdout.strip()
    b = subprocess.run(["git", "show", "%s:Database/FFXII TZA/_experiments/evidence/%s/manifest.json" %
                        (PRODUCER, SLUG)], capture_output=True, cwd=top).stdout
    return hashlib.sha256(b).hexdigest()


CONTROLS = [
    ("table cell kind 4 -> kind 3's arm (+ 0x39C := RVA of + 0x7B)", TBL + 12, struct.pack("<I", KIND[3] - 0x120000)),
    ("table cell kind 1 -> kind 4's arm (+ 0x390 := RVA of + 0xE8)", TBL, struct.pack("<I", KIND[4] - 0x120000)),
    ("+ 0x50 `dec eax` -> `inc eax` (kind index shifted)", F + 0x50, bytes.fromhex("ffc0")),
    ("+ 0x5A `ja` -> `jg` (signed bound)", F + 0x5B, bytes([0x8F])),
    ("+ 0x15 `mov rdi, rdx` -> `mov rdi, rcx` (RDI from the unit)", F + 0x15, bytes.fromhex("488bf9")),
    ("+ 0x147 `sub edi, eax` -> `sub edi, ecx`", F + 0x147, bytes.fromhex("2bf9")),
    ("+ 0x13F key DWORD +0xC -> +0x10", F + 0x141, bytes([0x10])),
    ("+ 0x14B second descriptor cell 02EBF138 -> 02EBF140", F + 0x14E, struct.pack("<I", DESC + 8 - (F + 0x152))),
    ("+ 0x152 stride WORD -> BYTE (`movzx ecx, byte ptr [rax + 8]`)", F + 0x153, bytes([0xB6])),
    ("+ 0x158 `div ecx` -> `idiv ecx` (signed division)", F + 0x158, bytes.fromhex("f7f9")),
    ("+ 0x156 `mov eax, edi` -> `test ecx, ecx` (a divisor test inserted before the DIV)", F + 0x156,
     bytes.fromhex("85c9")),
    ("+ 0x162 `cmp ax, dx` -> `cmp eax, edx` + NOP (32-bit sentinel compare)", F + 0x162, bytes.fromhex("3bc290")),
    ("+ 0x16A `sub eax, 0xd0` -> `sub eax, 0xd1`", F + 0x16B, bytes([0xD1])),
    ("+ 0x171 `or eax, 0xffffffff` -> `or eax, 0` (no FFFFFFFF sentinel)", F + 0x173, bytes([0x00])),
    ("+ 0x167 `movzx eax, ax` -> `movzx eax, al` (BYTE queue width)", F + 0x168, bytes([0xB6])),
    ("+ 0x174 store target 022C2178 -> 022C217C", F + 0x176, struct.pack("<I", QUEUE + 4 - (STORE + 6))),
    ("+ 0x165 `je` + 0x171 -> `jne` (sentinel test inverted)", F + 0x165, bytes([0x75])),
]


def main():
    img = Img.load()
    R = Rep("rv_seqq")
    print("== packet integrity")
    csha = committed_manifest_sha()
    check_manifest(R, SLUG, csha)
    R.note("committed manifest at %s: sha256 %s" % (PRODUCER, csha))
    packet_bytes(img, R)
    print("== raw direct-reference census (E8/E9 rel32 and 0F 8x jcc, .text)")
    rc = raw_refs(img, [F, STORE, KIND[4]])
    R.note("00306760 raw direct references (%d): %s (indirect callers not covered)" %
           (len(rc[F]), ", ".join("%X %s" % x for x in rc[F])))
    R.check("00306760 has exactly one raw direct reference, the call at 00304850 + 0x6FD (indirect callers not "
            "covered)", rc[F] == [(0x304F4D, "call")])
    R.note("raw direct references to the kind-4 arm entry + 0xE8: %d; to the store + 0x174 from outside the "
           "routine: %d" % (len(rc[KIND[4]]), len([x for x in rc[STORE] if not (F <= x[0] < END)])))
    print("== shipping-image re-derivation")
    checks(img, R)
    print("== controls (each patched private image must FAIL at least one check above)")
    Rn = Rep("null")
    Rn.quiet = True
    P0 = img.patched(F + 0x50, img.read(F + 0x50, 2))
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
