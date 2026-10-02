"""rv_effid.py - FABLE independent re-derivation for ASTRA packet ov42-effective-id-source (2cce275ad, OV-42).

Own reader (rvlib.py: struct + capstone 5, copied unchanged from the filecache-route2-commit-key review, sha256
69f9bc40be32abcc...).  Does not import or run ASTRA's prove.py, prove_owner_reload_order.py, capture drivers,
control.py, feasibility.py, freeze/publication scripts or the shared role adapter (reg_tracking.py).

Method:
  * image sha256; complete linear decode of the effective-id getter 00387090 and the owner resolver 0031B860,
    each bound by the image's own .pdata (the getter's three records are a root plus two chained records) and by
    int3 padding up to the next .pdata root; closed local CFGs, every ret, every call;
  * register-write censuses for the query (RDI), the table pointer (RBX), the owner returns (RAX), the compare
    census, every memory read of the +0x714 / table words with its width, every memory write;
  * the battle-action routine 00304850's .pdata chain followed to its end; the whole chained body decoded; every
    direct branch target checked against the straight line that carries the query into the getter and the
    getter's AX into R8D before the acquire wrapper 0030CFB0;
  * a concrete emulation (unicorn) of the ORIGINAL getter + resolver, and of the caller's straight line through
    them, over synthetic query records, units, tables and a scripted registry (the registry count / by-index
    helpers 00236850 / 00236820 are stubbed by a code hook: they are the only code not run from the image);
  * a raw E8/E9 rel32 and 0F 8x census of direct references to both bodies;
  * controls patch a private in-memory copy of the image; the exe on disk is never written and its sha256 is
    rechecked at the end.
"""
import hashlib
import json
import os
import struct
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rvlib import Img, Body, Report, check_manifest, find_exe, SHA256 as SHA_PIN  # noqa: E402

GET = (0x00387090, 0x00387125)     # 149 B
RES = (0x0031B860, 0x0031B8B3)     # 83 B
CALLER = 0x00304850
CNT, BYIDX = 0x00236850, 0x00236820
WRAP = 0x0030CFB0
TQ, TO = 0x0208D480, 0x0208DE80    # query-indexed / owner-indexed 64-byte record banks
O1CELL = 0x02EBF188
SLUG = "ov42-effective-id-source"
PRODUCER = "2cce275ad"
RETAINED_FROM = "0ada5145"
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
    m = I.mems[0]
    return I.address + I.size + m["disp"]


def is_root(img, va):
    """True when a .pdata record begins at va and is not a CHAININFO record."""
    po = img.off(img.base + img.exc_rva)
    for i in range(img.exc_size // 12):
        b, en, u = struct.unpack_from("<III", img.d, po + i * 12)
        if b + img.base == va:
            return not ((img.d[img.off(img.base + u)] >> 3) & 4)
    return False


def chain_of(img, root, scan_to):
    """Records whose chain resolves to root, among records beginning in [root, scan_to)."""
    ents, _ = img.pdata_cover(root, scan_to)
    return [(b, e) for b, e, fl, r in ents if r == root]


# ------------------------------------------------------------------ emulation of the original code
class Emu(object):
    QREC, UNITS, STK, RET = 0x50000000, 0x40000000, 0x7F000000, 0x7E000000

    def __init__(self, img):
        from unicorn import Uc, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
        from unicorn import UC_HOOK_MEM_READ_UNMAPPED, UC_HOOK_MEM_FETCH_UNMAPPED, UC_HOOK_MEM_WRITE_UNMAPPED
        from unicorn import x86_const as X
        self.X = X
        mu = self.mu = Uc(UC_ARCH_X86, UC_MODE_64)
        pages = set()
        for s, e in (GET, RES, (0x304DF0, 0x304E30), (CNT, CNT + 8), (BYIDX, BYIDX + 8), (WRAP, WRAP + 8),
                     (TQ, TO + 256 * 64), (O1CELL, O1CELL + 8)):
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
        mu.mem_map(self.STK, 0x10000)
        mu.mem_map(self.RET, 0x1000)
        mu.mem_map(self.QREC, 0x1000)
        mu.mem_map(self.UNITS, 0x20000)
        mu.mem_map(0x60000000, 0x1000)   # caller's r12 target
        self.reg_seq = []    # one registry list per resolver scan, consumed in order
        self.cb = []         # (helper, arg) registry callbacks
        self.fault = None
        self.writes = []
        self.left = None
        allowed = [GET, RES, (0x304DFD, 0x304E29)]

        def ch(uc, addr, size, ud):
            if addr == CNT or addr == BYIDX:
                rsp = uc.reg_read(X.UC_X86_REG_RSP)
                if addr == CNT:
                    lst = self.cur()
                    val = len(lst)
                    self.cb.append(("count", None))
                else:
                    i = uc.reg_read(X.UC_X86_REG_RCX) & 0xFFFFFFFF
                    lst = self.cur()
                    val = lst[i] if i < len(lst) else 0
                    self.cb.append(("byidx", i))
                uc.reg_write(X.UC_X86_REG_RAX, val)
                uc.reg_write(X.UC_X86_REG_RIP, struct.unpack("<Q", bytes(uc.mem_read(rsp, 8)))[0])
                uc.reg_write(X.UC_X86_REG_RSP, rsp + 8)
                return
            if addr == RES[0]:
                self.cb.append(("ret", None))   # marks a new resolver call
            if addr != self.RET and addr != WRAP and not any(s <= addr < e for s, e in allowed):
                self.left = addr
                uc.emu_stop()

        def bad(uc, access, addr, size, value, ud):
            self.fault = addr
            return False

        def wh(uc, access, addr, size, value, ud):
            self.writes.append((uc.reg_read(X.UC_X86_REG_RIP), addr, size, value))

        mu.hook_add(UC_HOOK_CODE, ch)
        mu.hook_add(UC_HOOK_MEM_READ_UNMAPPED | UC_HOOK_MEM_FETCH_UNMAPPED | UC_HOOK_MEM_WRITE_UNMAPPED, bad)
        mu.hook_add(UC_HOOK_MEM_WRITE, wh)

    def cur(self):
        # scan index = number of resolver entries seen so far - 1
        k = sum(1 for c in self.cb if c[0] == "ret") - 1
        return self.reg_seq[k] if 0 <= k < len(self.reg_seq) else []

    def unit(self, k, key, word, ea9, ident=0):
        a = self.UNITS + k * 0x1000
        self.mu.mem_write(a, b"\0" * 0x1000)
        self.mu.mem_write(a + 0x698, struct.pack("<Q", key))
        self.mu.mem_write(a + 0x714, struct.pack("<H", word))
        self.mu.mem_write(a + 0xEA9, bytes([ea9]))
        self.mu.mem_write(a + 8, struct.pack("<I", ident))
        return a

    def query(self, b4, b5):
        self.mu.mem_write(self.QREC, b"\0" * 16)
        self.mu.mem_write(self.QREC + 4, bytes([b4, b5]))
        return self.QREC

    def table_word(self, base, idx, w):
        self.mu.mem_write(base + idx * 64 + 0x10, struct.pack("<H", w))

    def u64(self, a):
        return struct.unpack("<Q", bytes(self.mu.mem_read(a, 8)))[0]

    def run(self, start, regs, until):
        from unicorn import UcError
        X = self.X
        sp = self.STK + 0x8000
        self.mu.mem_write(sp, struct.pack("<Q", self.RET))
        self.mu.reg_write(X.UC_X86_REG_RSP, sp)
        base = {"rax": 0xAAAAAAAAAAAAAAAA, "rbx": 0xBBBBBBBBBBBBBBBB, "rdi": 0xDDDDDDDDDDDDDDDD,
                "r8": 0x8888888888888888, "r9": 0x9999999999999999, "rcx": 0, "rdx": 0, "r12": 0}
        base.update(regs)
        for k, v in base.items():
            self.mu.reg_write(getattr(X, "UC_X86_REG_" + k.upper()), v)
        self.mu.mem_write(O1CELL, struct.pack("<Q", 0x1234567812345678))
        self.cb, self.fault, self.left, self.writes = [], None, None, []
        try:
            self.mu.emu_start(start, until, count=5000)
        except UcError:
            pass
        r = dict((k, self.mu.reg_read(getattr(X, "UC_X86_REG_" + k.upper())))
                 for k in ("rax", "rbx", "rcx", "rdx", "rdi", "r8", "r9", "rip"))
        r["fault"], r["left"] = self.fault, self.left
        r["calls"] = [c for c in self.cb if c[0] != "ret"]
        r["resolver_entries"] = sum(1 for c in self.cb if c[0] == "ret")
        r["o1cell"] = self.u64(O1CELL)
        r["nonframe"] = [w for w in self.writes if not (self.STK <= w[1] < self.STK + 0x10000)]
        return r

    def getter(self, q, seq):
        self.reg_seq = seq
        return self.run(GET[0], {"rcx": q}, self.RET)


def emu_checks(img, R):
    E = Emu(img)
    U = Emu.UNITS
    # --- query leg: +5 == 0, index +4
    q = E.query(3, 0)
    ok, bad = True, []
    for w in CANDS + [0, 0x9E, 0xA0, 0x19F, 0x7FFF, 0x8000, 0xFFFF]:
        a = E.unit(1, q, w, 7)
        E.table_word(TQ, 3, 0x4242)
        r = E.getter(q, [[0, a]])
        good = (r["rax"] == w and r["rbx"] == 0xBBBBBBBBBBBBBBBB and r["rdi"] == 0xDDDDDDDDDDDDDDDD and
                r["resolver_entries"] == 1 and r["o1cell"] == 0x1234567812345678 and not r["fault"] and
                not r["left"] and r["nonframe"] == [])
        if not good:
            ok = False
            bad.append("%X: rax %X res %d fault %s" % (w, r["rax"], r["resolver_entries"], r["fault"]))
    R.check("emulated getter, query +5 = 0: each of 511..534 and 0, 9E, A0, 19F, 7FFF, 8000, FFFF at O2+0x714 is "
            "returned unchanged with RAX's upper bits zero; one resolver call; 2EBF188 untouched; RBX/RDI restored; "
            "no non-frame write", ok, "; ".join(bad[:3]))
    a = E.unit(1, q, 0x9F, 7)
    E.table_word(TQ, 3, 0x8123)
    r = E.getter(q, [[a]])
    R.check("emulated getter, query +5 = 0, +4 = 3, O2 word 9F: returns WORD 0208D480 + 3*64 + 0x10 = 8123 "
            "zero-extended (not sign-extended)", r["rax"] == 0x8123 and not r["fault"], "rax %X" % r["rax"])
    # --- O1 leg: +5 != 0
    q = E.query(3, 1)
    a = E.unit(1, q, 0x9F, 5)
    E.table_word(TO, 5, 0x0321)
    E.table_word(TQ, 3, 0x4242)
    r = E.getter(q, [[a], [a]])
    R.check("emulated getter, query +5 = 1, O1 = O2 = unit (+0xEA9 = 5), word 9F: two resolver calls; 2EBF188 = "
            "O1; returns WORD 0208DE80 + 5*64 + 0x10", r["rax"] == 0x321 and r["o1cell"] == a and
            r["resolver_entries"] == 2 and not r["fault"], "rax %X o1 %X" % (r["rax"], r["o1cell"]))
    ok = True
    for w in CANDS:
        a = E.unit(1, q, w, 5)
        r = E.getter(q, [[a], [a]])
        ok = ok and r["rax"] == w and r["o1cell"] == a
    R.check("emulated getter, O1 leg: each of 511..534 returned unchanged with a nonzero table pointer", ok)
    # --- distinct O1 / O2
    a = E.unit(1, q, 0x0200, 5)      # O1: not 9F, slot 5
    b = E.unit(2, q, 0x9F, 9)        # O2: 9F, slot 9
    E.table_word(TO, 5, 0x0555)
    E.table_word(TO, 9, 0x0999)
    r = E.getter(q, [[a], [0, b]])
    R.check("emulated getter, registry changes between the calls (O1 = unit A slot 5, O2 = unit B slot 9, B's word "
            "9F): the table is chosen by O1 and the word by O2 - returns A's slot record +0x10 (555), not B's (999)",
            r["rax"] == 0x555 and r["o1cell"] == a, "rax %X" % r["rax"])
    r = E.getter(q, [[], [b]])
    R.check("emulated getter, O1 null (empty registry on the first scan), O2 = B with word 9F: RBX = 0, so 9F is "
            "returned unchanged; 2EBF188 = 0", r["rax"] == 0x9F and r["o1cell"] == 0 and not r["fault"],
            "rax %X o1 %X" % (r["rax"], r["o1cell"]))
    # --- NULL paths
    r = E.getter(0, [[a], [a]])
    R.check("emulated getter(NULL): both resolver calls return 0 with no registry callback; 2EBF188 = 0; the "
            "getter then reads address 0x714 (unmapped-read fault) - no sentinel return",
            r["resolver_entries"] == 2 and r["calls"] == [] and r["o1cell"] == 0 and r["fault"] == 0x714,
            "calls %s fault %s rip %X" % (r["calls"][:3], r["fault"], r["rip"]))
    q = E.query(3, 0)
    r = E.getter(q, [[E.unit(1, q + 8, 0x9F, 5)]])
    R.check("emulated getter, non-null query whose owner is absent (O2 = 0): reads address 0x714 (fault), even "
            "with a nonzero table pointer", r["fault"] == 0x714, "fault %s rax %X" % (r["fault"], r["rax"]))
    # --- resolver alone: count re-read, null entries, first match
    E.reg_seq = [[0, E.unit(1, 0x77, 1, 1), E.unit(2, 0x99, 2, 2), E.unit(3, 0x99, 3, 3)]]
    r = E.run(RES[0], {"rcx": 0x99}, Emu.RET)
    ncount = sum(1 for c in r["calls"] if c[0] == "count")
    R.check("emulated resolver: entries [NULL, key 77, key 99 (A), key 99 (B)] -> returns A (first match); the "
            "count helper is called once before the scan and once per non-matching entry (3), the by-index helper "
            "for 0, 1, 2", r["rax"] == U + 0x2000 and ncount == 3 and
            [c[1] for c in r["calls"] if c[0] == "byidx"] == [0, 1, 2], str(r["calls"]))
    E.reg_seq = [[E.unit(1, 0x77, 1, 1)]]
    r = E.run(RES[0], {"rcx": 0x99}, Emu.RET)
    r2 = None
    E.reg_seq = [[]]
    r2 = E.run(RES[0], {"rcx": 0x99}, Emu.RET)
    R.check("emulated resolver: no match returns RAX = 0; an empty registry (count 0) returns 0 after one count call",
            r["rax"] == 0 and r2["rax"] == 0 and [c[0] for c in r2["calls"]] == ["count"])
    # --- caller straight line 304DFD .. 304E24 through the original getter + resolver
    q = E.query(3, 0)
    u = E.unit(4, q, 0x9F, 0x11, ident=0xCAFEBABE)
    E.table_word(TQ, 3, 0x0ABC)
    E.reg_seq = [[u]]
    r = E.run(0x304DFD, {"rdi": u, "r12": 0x60000000, "rbx": 0xBBBBBBBBBBBBBBBB}, WRAP)
    R.check("emulated caller line 304DFD -> 0030CFB0 (unit's own query, word 9F, query table word ABC): reaches "
            "0030CFB0 with R8 = ABC (upper bits zero), RCX = R12, EDX = unit DWORD +8, R9D = unit BYTE +0xEA9",
            r["rip"] == WRAP and r["r8"] == 0xABC and r["rcx"] == 0x60000000 and (r["rdx"] & 0xFFFFFFFF) == 0xCAFEBABE
            and (r["r9"] & 0xFFFFFFFF) == 0x11 and not r["fault"],
            "rip %X r8 %X rcx %X rdx %X r9 %X" % (r["rip"], r["r8"], r["rcx"], r["rdx"], r["r9"]))
    ok = True
    for w in CANDS:
        E.unit(4, q, w, 0x11, ident=1)
        E.reg_seq = [[u]]
        r = E.run(0x304DFD, {"rdi": u, "r12": 0x60000000}, WRAP)
        ok = ok and r["rip"] == WRAP and r["r8"] == w
    R.check("emulated caller line: each of 511..534 at the unit's +0x714 arrives at 0030CFB0 as R8 unchanged", ok)


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


def checks(img, R):
    G, S = Body(img, *GET), Body(img, *RES)
    # ---------------- bodies
    ents, ok = img.pdata_cover(*GET)
    R.check("getter 00387090, 149 B: decodes exactly; three .pdata records (the root 00387090 .. + 0x6 and two "
            "CHAININFO records + 0x6 .. + 0x6B, + 0x6B .. + 0x95, both rooted at 00387090) tile it exactly",
            G.exact and ok and [(b - GET[0], e - GET[0], r) for b, e, fl, r in ents] ==
            [(0, 6, GET[0]), (6, 0x6B, GET[0]), (0x6B, 0x95, GET[0])], str([(hex(b), hex(e)) for b, e, f, r in ents]))
    ents, ok = img.pdata_cover(*RES)
    R.check("resolver 0031B860, 83 B: decodes exactly; one .pdata record covers it exactly", S.exact and ok and
            len(ents) == 1)
    R.check("both bodies end in int3 padding up to the next .pdata root (00387125 .. 00387130, 0031B8B3 .. 0031B8C0 "
            "all CC; 00387130 and 0031B8C0 are root records)",
            img.read(GET[1], 0xB) == b"\xcc" * 0xB and img.read(RES[1], 0xD) == b"\xcc" * 0xD and
            is_root(img, 0x387130) and is_root(img, 0x31B8C0))
    rets, tails, outs = G.exits()
    R.check("getter local CFG closed: two rets (+ 0x87 after the table load, + 0x94 the last instruction), no tail, "
            "no out-of-body branch, no indirect jump; calls only 0031B860, twice (+ 0x2F, + 0x5C)",
            rets == [0x387117, 0x387124] and not tails and not outs and G.order[-1] == 0x387124 and
            G.calls() == [(0x3870BF, RES[0]), (0x3870EC, RES[0])])
    rets, tails, outs = S.exits()
    R.check("resolver local CFG closed: two rets (+ 0x15 null query, + 0x52 the last instruction), no tail; calls "
            "only 00236850 (+ 0x1D, + 0x3D) and 00236820 (+ 0x28)",
            rets == [0x31B875, 0x31B8B2] and not tails and not outs and
            S.calls() == [(0x31B87D, CNT), (0x31B888, BYIDX), (0x31B89D, CNT)])
    # ---------------- getter: the query and the table pointer
    R.check("query carrier: RDI = incoming RCX (+ 0xB) after its home save (+ 0x6); RDI written only there and at the "
            "reload + 0x61; no RCX write before the first call; the second call's RCX = RDI (+ 0x59, the "
            "instruction before the call)",
            T(G, 0x387096) == "mov qword ptr [rsp + 0x30], rdi" and T(G, 0x38709B) == "mov rdi, rcx" and
            writers(G, "rdi") == [0x38709B, 0x3870F1] and T(G, 0x3870F1) == "mov rdi, qword ptr [rsp + 0x30]" and
            not writers(G, "rcx", GET[0], 0x3870BF) and T(G, 0x3870E9) == "mov rcx, rdi" and
            writers(G, "rcx", 0x3870E9, 0x3870EC) == [0x3870E9])
    R.check("query leg: `test rcx, rcx` / `je` -> the first call (+ 0xE/+ 0x11); BYTE [rcx + 5] zero-extended, "
            "`test` / `jne` -> the first call (+ 0x13 .. + 0x19); else RBX = 0208D480 + (BYTE [rcx + 4] << 6) and "
            "`jmp` + 0x59, past the first call",
            T(G, 0x38709E) == "test rcx, rcx" and T(G, 0x3870A1) == "je 0x3870bf" and
            T(G, 0x3870A3) == "movzx eax, byte ptr [rcx + 5]" and G[0x3870A3].mems[0]["size"] == 1 and
            T(G, 0x3870A9) == "jne 0x3870bf" and T(G, 0x3870AB) == "movzx ebx, byte ptr [rcx + 4]" and
            rip_target(G[0x3870AF]) == TQ and T(G, 0x3870B6) == "shl rbx, 6" and T(G, 0x3870BA) == "add rbx, rax"
            and T(G, 0x3870BD) == "jmp 0x3870e9" and 0x3870BF not in G.reach(0x3870AB))
    R.check("O1 leg: the first return is stored as a QWORD to 02EBF188 (+ 0x34); `test rax` / `je` -> `xor ebx, ebx` "
            "(+ 0x57); else RBX = 0208DE80 + (BYTE [O1 + 0xEA9] << 6)",
            rip_target(G[0x3870C4]) == O1CELL and G[0x3870C4].mems[0]["size"] == 8 and
            T(G, 0x3870C4).startswith("mov qword ptr [rip") and T(G, 0x3870CE) == "je 0x3870e7" and
            T(G, 0x3870D0) == "movzx ebx, byte ptr [rax + 0xea9]" and rip_target(G[0x3870D7]) == TO and
            T(G, 0x3870DE) == "shl rbx, 6" and T(G, 0x3870E2) == "add rbx, rax" and T(G, 0x3870E7) == "xor ebx, ebx")
    R.check("RBX (table pointer) is written only on the two legs and by the two `pop rbx` restores; nothing writes it "
            "between the second call and the table test",
            writers(G, "rbx") == [0x3870AB, 0x3870B6, 0x3870BA, 0x3870D0, 0x3870DE, 0x3870E2, 0x3870E7, 0x387116,
                                  0x387123] and not writers(G, "rbx", 0x3870E9, 0x387112))
    R.check("the selected pointer is never 0 on the query leg (0208D480 + 64*k, k <= 255) or for a non-null O1; RBX "
            "= 0 only when the first resolver returned NULL",
            all(TQ + 64 * k != 0 and TO + 64 * k != 0 for k in range(256)) and
            [a for a in writers(G, "rbx", GET[0], 0x3870E9) if T(G, a).startswith("xor")] == [0x3870E7])
    # ---------------- getter: O2 and the result
    R.check("O2: RAX from the second call is tested (`test rax` / `je` + 0x88, at + 0x66/+ 0x69) and then only read; "
            "no RAX write between the second call's return and a result load",
            T(G, 0x3870F6) == "test rax, rax" and T(G, 0x3870F9) == "je 0x387118" and
            not writers(G, "rax", 0x3870F1, 0x38710E))
    R.check("the substitution: `test rbx, rbx` / `je` + 0x88 (+ 0x6B), ECX = 0x9F (+ 0x70), WORD compare "
            "[rax + 0x714] with CX (+ 0x75, 2 bytes), `jne` + 0x88; else `movzx eax, word ptr [rbx + 0x10]` (2 bytes) "
            "and ret",
            T(G, 0x3870FB) == "test rbx, rbx" and T(G, 0x3870FE) == "je 0x387118" and T(G, 0x387100) == "mov ecx, 0x9f"
            and T(G, 0x387105) == "cmp word ptr [rax + 0x714], cx" and G[0x387105].mems[0]["size"] == 2 and
            T(G, 0x38710C) == "jne 0x387118" and T(G, 0x38710E) == "movzx eax, word ptr [rbx + 0x10]" and
            G[0x38710E].mems[0]["size"] == 2 and G.reach(0x38710E) == {0x38710E, 0x387112, 0x387116, 0x387117})
    R.check("the direct leg: + 0x88 `movzx eax, word ptr [rax + 0x714]` (2 bytes) then ret; it is the target of all "
            "three `je`/`jne` (O2 null, RBX null, word != 9F)",
            T(G, 0x387118) == "movzx eax, word ptr [rax + 0x714]" and G[0x387118].mems[0]["size"] == 2 and
            sorted(a for a in G.order if G[a].direct_target() == 0x387118) == [0x3870F9, 0x3870FE, 0x38710C])
    R.check("no sentinel: O2 = NULL goes straight to the + 0x88 load through RAX (address 0 + 0x714); every path to "
            "a ret passes a load through RAX or RBX",
            G.dominates(0x387118, 0x387124) and G.dominates(0x38710E, 0x387117) and
            G[0x3870F9].direct_target() == 0x387118 and 0x387118 in G.succ(0x3870F9) and
            not [a for a in G.order if G[a].mnemonic == "xor" and a > 0x3870EC])
    cmps = [(a, G[a].text) for a in G.order if G[a].mnemonic in ("cmp", "test")]
    R.check("compare census: six compares/tests - query, BYTE +5, O1, O2, RBX, and the one WORD compare with 0x9F; "
            "nothing compares the +0x714 word with any bound (no local candidate bound)",
            [a for a, t in cmps] == [0x38709E, 0x3870A7, 0x3870CB, 0x3870F6, 0x3870FB, 0x387105] and
            [a for a in G.order if G[a].mems and G[a].mems[0]["disp"] == 0x714] == [0x387105, 0x387118],
            "; ".join("%X %s" % c for c in cmps))
    mw = [(a, m["base"], m["disp"], m["size"]) for a, m in G.mem_writes()]
    R.check("getter memory writes: the RDI home slot and the QWORD 02EBF188 only (plus the push)",
            mw == [(0x387096, "rsp", 0x30, 8), (0x3870C4, "rip", O1CELL - 0x3870CB, 8)],
            "; ".join("%X %s+%X/%d" % w for w in mw))
    R.check("both rets restore RBX (`pop rbx`) and RSP, and return EAX by `movzx` (a 32-bit write, so RAX's upper half "
            "is zero)", T(G, 0x387112) == "add rsp, 0x20" and T(G, 0x387116) == "pop rbx" and
            T(G, 0x38711F) == "add rsp, 0x20" and T(G, 0x387123) == "pop rbx")
    # ---------------- resolver
    R.check("resolver NULL query: `test rcx` / `jne` (+ 0x9/+ 0xC); NULL falls to `xor eax, eax` and ret with no "
            "call reachable", T(S, 0x31B869) == "test rcx, rcx" and T(S, 0x31B86C) == "jne 0x31b876" and
            T(S, 0x31B86E) == "xor eax, eax" and S.reach(0x31B86E) == {0x31B86E, 0x31B870, 0x31B874, 0x31B875})
    R.check("resolver scan: EBX = 0; count call, `jle` -> return 0; loop: ECX = EBX, by-index call, null entry "
            "skipped, QWORD [rax + 0x698] == RDI (the query) -> `je` + 0x48 returning that RAX; else `inc ebx`, count "
            "re-read (+ 0x3D), signed `cmp ebx, eax` / `jl`",
            T(S, 0x31B866) == "mov rdi, rcx" and writers(S, "rdi") == [0x31B866, 0x31B874, 0x31B8B1] and
            T(S, 0x31B87B) == "xor ebx, ebx" and T(S, 0x31B884) == "jle 0x31b8a6" and T(S, 0x31B886) == "mov ecx, ebx"
            and T(S, 0x31B890) == "je 0x31b89b" and T(S, 0x31B892) == "cmp qword ptr [rax + 0x698], rdi" and
            S[0x31B892].mems[0]["size"] == 8 and T(S, 0x31B899) == "je 0x31b8a8" and T(S, 0x31B89B) == "inc ebx" and
            T(S, 0x31B8A2) == "cmp ebx, eax" and T(S, 0x31B8A4) == "jl 0x31b886" and
            T(S, 0x31B8A6) == "xor eax, eax" and not writers(S, "rax", 0x31B8A8, RES[1]))
    mw = [(a, m["base"], m["disp"], m["size"]) for a, m in S.mem_writes()]
    R.check("resolver memory writes: the RBX home slot only", mw == [(0x31B876, "rsp", 0x30, 8)], str(mw))
    # ---------------- caller
    chain = chain_of(img, CALLER, 0x305080)
    R.check("00304850's .pdata chain: seven records 00304850 .. + 0x828 tile exactly (root + 0xA6, six CHAININFO "
            "records rooted at 00304850); 00304850 + 0x5C2 (the getter call) lies in the chained record + 0x520 .. "
            "+ 0x741, and + 0x520 is not a function entry (not a root record)",
            [(b - CALLER, e - CALLER) for b, e in chain] ==
            [(0, 0xA6), (0xA6, 0x1F6), (0x1F6, 0x520), (0x520, 0x741), (0x741, 0x7B6), (0x7B6, 0x7C7), (0x7C7, 0x828)]
            and img.pdata(0x304E12) == (0x304D70, 0x304F91) and not is_root(img, 0x304D70) and is_root(img, CALLER),
            str([(hex(b), hex(e)) for b, e in chain]))
    # The chain's last 0x34 bytes are a 13-entry DWORD jump table (image-base-relative RVAs), not code.
    C = Body(img, CALLER, 0x305044)
    ind = [a for a in C.order if C[a].mnemonic == "jmp" and C[a].direct_target() is None]
    jt = [img.base + img.u32(0x305044 + 4 * i) for i in range(13)]
    R.check("00304850's code 00304850 .. + 0x7F4 decodes exactly; its one indirect jmp (+ 0x10A) is a 13-way phase "
            "switch on BYTE [rsi + 4] (`cmp eax, 0xc` / `ja`), table = image base + 0x1E5044 = 00304850 + 0x7F4, "
            "13 DWORDs ending exactly at the chain end + 0x828",
            C.exact and ind == [0x30495A] and T(C, 0x30493C) == "movzx eax, byte ptr [rsi + 4]" and
            T(C, 0x304940) == "cmp eax, 0xc" and T(C, 0x304943) == "ja 0x305006" and
            T(C, 0x304949) == "lea rdx, [rip - 0x1e4950]" and rip_target(C[0x304949]) == img.base and
            T(C, 0x304950) == "mov ecx, dword ptr [rdx + rax*4 + 0x1e5044]" and
            0x305044 + 13 * 4 == 0x305078 and all(CALLER <= t < 0x305044 and t in C.ins for t in jt),
            " ".join("%X" % t for t in jt))
    into = sorted((a, C[a].direct_target()) for a in C.order
                  if C[a].mnemonic.startswith("j") and C[a].direct_target() is not None and
                  0x304DA5 < C[a].direct_target() <= 0x304E24)
    R.check("the getter call is in phase case 6: table entry 6 = 00304850 + 0x555; no other table entry and no "
            "direct jump or jcc anywhere in the body lands in + 0x555 .. + 0x5D4 except the case's own `jne` "
            "+ 0x55E -> + 0x56D; case 5 (+ 0x523) falls through into + 0x555 after `inc byte ptr [rsi + 4]`",
            jt[6] == 0x304DA5 and not [t for t in jt if 0x304DA5 < t <= 0x304E24] and
            into == [(0x304DAE, 0x304DBD)] and jt[5] == 0x304D73 and T(C, 0x304DA2) == "inc byte ptr [rsi + 4]" and
            C.succ(0x304DA2) == [0x304DA5] and C.succ(0x304D9D) == [0x304DA2],
            "into %s" % into)
    seq = [a for a in C.order if 0x304DFD <= a <= 0x304E24]
    R.check("the straight line + 0x5AD .. + 0x5D4: RCX = QWORD [rdi + 0x698] (+ 0x5AD), `or dword [rdi+4]`, "
            "EBX = BYTE [rdi + 0xEA9], `call 00387090` (+ 0x5C2), EDX = DWORD [rdi + 8], R8D = `movzx r8d, ax` "
            "(+ 0x5CA), R9D = EBX, RCX = R12, `call 0030CFB0` (+ 0x5D4)",
            [T(C, a) for a in seq] ==
            ["mov rcx, qword ptr [rdi + 0x698]", "or dword ptr [rdi + 4], 0x80", "movzx ebx, byte ptr [rdi + 0xea9]",
             "call 0x387090", "mov edx, dword ptr [rdi + 8]", "movzx r8d, ax", "mov r9d, ebx", "mov rcx, r12",
             "call 0x30cfb0"] and C[0x304DFD].mems[0]["size"] == 8)
    R.check("between the getter call and 0030CFB0: one call each end and none between; RAX not written before + 0x5CA; "
            "R8 written only at + 0x5CA; RCX not written between + 0x5AD and the getter call",
            [a for a in seq if C[a].mnemonic == "call"] == [0x304E12, 0x304E24] and
            not writers(C, "rax", 0x304E17, 0x304E1A) and writers(C, "r8", 0x304E17, 0x304E24) == [0x304E1A] and
            not writers(C, "rcx", 0x304E04, 0x304E12))
    emu_checks(img, R)


def packet_bytes(img, R):
    ev = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(find_exe())))),
                      "FFXII TZA", "_experiments", "evidence", SLUG)
    mism, got = [], []
    for f in ("source-01.json", "source-owner-01.json", "retained-callers-01.json"):
        for r in json.load(open(os.path.join(ev, f)))["ranges"]:
            s_, e_ = int(r["start"], 16), int(r["end_exclusive"], 16)
            got.append((s_, e_))
            if hashlib.sha256(img.read(s_, e_ - s_)).hexdigest() != r["sha256"]:
                mism.append(r["start"])
    R.check("packet's getter, resolver and retained caller range hashes equal this image's bytes (00387090 .. + 0x95, "
            "0031B860 .. + 0x53, 00304850 + 0x520 .. + 0x5D9, script adapter 0030EEA0 .. + 0x65)",
            not mism and got == [GET, RES, (0x304D70, 0x304E29), (0x30EEA0, 0x30EF05)],
            " ".join("%X..%X" % g for g in got))
    R.check("getter / resolver bytes hash to the README's pins (7fe99655..., 9a162077...)",
            hashlib.sha256(img.read(GET[0], 149)).hexdigest().startswith("7fe996559221d1aa") and
            hashlib.sha256(img.read(RES[0], 83)).hexdigest().startswith("9a162077226a0c37"))
    top = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True,
                         cwd=os.path.dirname(os.path.abspath(__file__))).stdout.strip()
    b = subprocess.run(["git", "show", "%s:Database/FFXII TZA/_experiments/evidence/ov42-slot-id-producer/retained/"
                        "slot-acquisition-callers-raw-01.json" % RETAINED_FROM], capture_output=True, cwd=top).stdout
    mine = open(os.path.join(ev, "retained-callers-01.json"), "rb").read()
    R.check("retained-callers-01.json is byte-identical to 0ada5145's retained/slot-acquisition-callers-raw-01.json "
            "(sha256 b27ee5a0...)", hashlib.sha256(b).hexdigest() == hashlib.sha256(mine).hexdigest() ==
            "b27ee5a03712f3d9bbfcf429fe3277e38de86f236f3ea593ec4aabd479c5e0ab")
    rd = open(os.path.join(ev, "README.md"), encoding="utf-8").read()
    R.check("packet keeps open: observed fault, natural null caller, table initialization, interior fragment, "
            "owner lifetime, whole OV-42",
            "not an observed crash/fault" in rd and "a normal caller passes null" in rd and
            "Table initialization" in rd and "interior fragment" in rd and "owner lifetime" in rd and
            "whole OV-42" in rd)


def committed_manifest_sha():
    top = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True,
                         cwd=os.path.dirname(os.path.abspath(__file__))).stdout.strip()
    b = subprocess.run(["git", "show", "%s:Database/FFXII TZA/_experiments/evidence/%s/manifest.json" %
                        (PRODUCER, SLUG)], capture_output=True, cwd=top).stdout
    return hashlib.sha256(b).hexdigest()


CONTROLS = [
    ("00387090 + 0x70 `mov ecx, 0x9f` -> 0xA0 (wrong replacement id)", 0x387101, bytes([0xA0])),
    ("00387090 + 0x88 WORD read -> BYTE read (`movzx eax, byte ptr [rax + 0x714]`)", 0x387119, bytes([0xB6])),
    ("00387090 + 0x7E table word +0x10 -> +0x12", 0x387111, bytes([0x12])),
    ("00387090 + 0x7E `movzx` -> `movsx` (sign-extended table word)", 0x38710F, bytes([0xBF])),
    ("00387090 + 0x6E table-pointer `je` -> two nops (RBX = 0 no longer skips the substitution)", 0x3870FE,
     bytes.fromhex("9090")),
    ("00387090 + 0x69 O2-null `je + 0x88` -> `je + 0x82` (an invented safe-null return of 0)", 0x3870F9,
     bytes.fromhex("7417")),
    ("00387090 + 0x59 second resolver input `mov rcx, rdi` -> `mov rcx, rax` (O1 passed as the query)", 0x3870E9,
     bytes.fromhex("488bc8")),
    ("00387090 + 0x1B table index BYTE +4 -> +5", 0x3870AE, bytes([0x05])),
    ("00387090 + 0x1F query table base 0208D480 -> 0208D4C0", 0x3870B2, bytes([0x0A, 0x64])),
    ("00387090 + 0x34 O1 cell 02EBF188 -> 02EBF190", 0x3870C7, bytes([0xC5])),
    ("0031B860 + 0xC null-query `jne` -> `jmp` (NULL enters the registry scan)", 0x31B86C, bytes([0xEB])),
    ("0031B860 + 0x32 match key +0x698 -> +0x6A0", 0x31B895, bytes([0xA0])),
    ("0031B860 + 0x39 match `je + 0x48` -> `je + 0x46` (a match returns 0)", 0x31B899, bytes.fromhex("740b")),
    ("00304850 + 0x5CA `movzx r8d, ax` -> `movzx r8d, bx`", 0x304E1A, bytes.fromhex("440fb7c3")),
    ("00304850 + 0x5CE `mov r9d, ebx` -> `mov r8d, ebx` (an R8 write after the transfer)", 0x304E1E,
     bytes.fromhex("448bc3")),
    ("00304850 + 0x5AD query QWORD +0x698 -> +0x6A0", 0x304E00, bytes([0xA0])),
]


def main():
    img = Img.load()
    R = Rep("rv_effid")
    print("== packet integrity")
    csha = committed_manifest_sha()
    check_manifest(R, SLUG, csha)
    R.note("committed manifest at %s: sha256 %s" % (PRODUCER, csha))
    packet_bytes(img, R)
    print("== raw direct-reference census (E8/E9 rel32 and 0F 8x jcc, .text)")
    rc = raw_refs(img, [GET[0], RES[0]])
    R.note("00387090 raw direct references (%d): %s (indirect callers not covered)" %
           (len(rc[GET[0]]), ", ".join("%X %s" % x for x in rc[GET[0]])))
    R.check("00387090 is called directly at 00304850 + 0x5C2 (among its raw references)",
            (0x304E12, "call") in rc[GET[0]])
    R.note("0031B860 raw direct references: %d (the getter's two among them: %s)" %
           (len(rc[RES[0]]), ["%X" % x[0] for x in rc[RES[0]] if GET[0] <= x[0] < GET[1]]))
    rc2 = raw_refs(img, [CALLER])
    R.note("00304850 raw direct references: %s (so neither 00387090 nor any other body cited here calls it "
           "directly; indirect callers not covered)" % ", ".join("%X %s" % x for x in rc2[CALLER]))
    print("== shipping-image re-derivation")
    checks(img, R)
    print("== controls (each patched private image must FAIL at least one check above)")
    Rn = Rep("null")
    Rn.quiet = True
    checks(img.patched(0x387101, img.read(0x387101, 1)), Rn)
    R.check("null control: an unchanged private copy (sha check off) passes every check", Rn.fails == 0 and Rn.n > 0,
            "%d of %d" % (Rn.n - Rn.fails, Rn.n))
    nctl = 0
    for label, va, nb in CONTROLS:
        Pimg = img.patched(va, nb)
        if Pimg.d == img.d:
            raise SystemExit("control %s did not change the image" % label)
        Rc = Rep(label)
        Rc.quiet = True
        try:
            checks(Pimg, Rc)
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
