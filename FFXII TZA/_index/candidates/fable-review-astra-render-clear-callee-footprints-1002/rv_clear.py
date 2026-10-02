"""rv_clear.py - FABLE independent re-derivation for ASTRA packet render-clear-callee-footprints (621dbd2cc).

Own reader (rvlib.py: struct + capstone 5).  Does not import ASTRA's prove.py or the shared role adapter.
Method: a small step emulator runs 0041F730 and the helpers it reaches, instruction by instruction, with the
record pointer symbolic (R+off), the stack symbolic (S+off) and every other value concrete or unknown.  The
memset import is the only modelled callee (the packet's library premise): it fills [rcx, rcx+r8) with dl and
clobbers the volatile registers.  Every memory write is logged with its site, so the footprints, carriers and
the final values of WORD +0 and DWORD +284h are functions of the image.  The controls patch a private copy of
the image and require at least one named check to fail.
"""
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rvlib import Img, Body, Report, check_manifest, fam  # noqa: E402
from capstone.x86 import X86_OP_MEM, X86_OP_IMM, X86_OP_REG  # noqa: E402

CALLER = (0x0041F730, 0x0041FBE8)
HELPERS = [(0x006C0520, 0x006C053A), (0x0046D110, 0x0046D11C), (0x00202C70, 0x00202C8F),
           (0x003E5D00, 0x003E5D2C), (0x003E37E0, 0x003E37EB)]
MEMSET = 0x00861EC0
REC = 0x740
U = None  # unknown value
VOLATILE = ["rax", "rcx", "rdx", "r8", "r9", "r10", "r11"] + ["xmm%d" % i for i in range(6)]
MASK = {1: 0xFF, 2: 0xFFFF, 4: 0xFFFFFFFF, 8: 0xFFFFFFFFFFFFFFFF}


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


class Emu(object):
    def __init__(self, img):
        self.img = img
        self.r = {"rcx": ("R", 0), "rsp": ("S", 0)}
        self.stack = {}            # S offset -> byte (int or U)
        self.rec = [U] * REC       # final record bytes (U = never written)
        self.writes = []           # (site, func, base, start, end)
        self.calls = []            # (site, target, rcx, rdx, r8)
        self.flags = None
        self.cur = None
        self.steps = 0

    # ---- values -------------------------------------------------------------
    def reg(self, name):
        f = fam(name)
        v = self.r.get(f, U)
        if name.startswith("xmm"):
            return self.r.get(name, U)
        w = regw(name)
        if isinstance(v, int):
            if name in ("ah", "bh", "ch", "dh"):
                return (v >> 8) & 0xFF
            return v & MASK[w]
        if w == 8:
            return v
        return U

    def setreg(self, name, v):
        if name.startswith("xmm"):
            self.r[name] = v
            return
        f = fam(name)
        w = regw(name)
        if w == 8:
            self.r[f] = v
        elif w == 4:
            self.r[f] = (v & 0xFFFFFFFF) if isinstance(v, int) else U
        else:
            old = self.r.get(f, U)
            if isinstance(old, int) and isinstance(v, int):
                self.r[f] = (old & ~MASK[w]) | (v & MASK[w])
            else:
                self.r[f] = U

    def addr(self, I, m):
        if m["base"] == "rip":
            return ("A", I.address + I.size + m["disp"])
        b = self.reg(m["base"]) if m["base"] else ("A", 0)
        idx = 0
        if m["index"]:
            iv = self.reg(m["index"])
            if not isinstance(iv, int):
                return U
            idx = iv * m["scale"]
        if isinstance(b, tuple):
            return (b[0], b[1] + m["disp"] + idx)
        if isinstance(b, int):
            return ("A", b + m["disp"] + idx)
        return U

    def load(self, a, n):
        if a is U:
            return U
        k, o = a
        if k == "A":
            try:
                return int.from_bytes(self.img.read(o, n), "little")
            except ValueError:
                return U
        src = self.stack if k == "S" else None
        bs = []
        for i in range(n):
            b = src.get(o + i, U) if src is not None else (self.rec[o + i] if 0 <= o + i < REC else U)
            if b is U:
                return U
            bs.append(b)
        return int.from_bytes(bytes(bs), "little")

    def store(self, site, a, n, v):
        if a is U:
            self.writes.append((site, self.cur, "?", 0, n))
            return
        k, o = a
        if k == "S":
            for i in range(n):
                self.stack[o + i] = ((v >> (8 * i)) & 0xFF) if isinstance(v, int) else U
            return
        self.writes.append((site, self.cur, k, o, o + n))
        if k == "R":
            for i in range(n):
                if 0 <= o + i < REC:
                    self.rec[o + i] = ((v >> (8 * i)) & 0xFF) if isinstance(v, int) else U

    def push(self, v):
        s = self.r["rsp"]
        self.r["rsp"] = (s[0], s[1] - 8)
        self.store(None, self.r["rsp"], 8, v if isinstance(v, int) else 0)
        self.stack[("ret", self.r["rsp"][1])] = v

    def pop(self):
        s = self.r["rsp"]
        v = self.stack.get(("ret", s[1]), self.load(s, 8))
        self.r["rsp"] = (s[0], s[1] + 8)
        return v

    # ---- execution -----------------------------------------------------------
    def opval(self, I, k):
        op = I.ci.operands[k]
        if op.type == X86_OP_REG:
            return self.reg(I.ci.reg_name(op.reg))
        if op.type == X86_OP_IMM:
            return op.imm & MASK[op.size if op.size in MASK else 8]
        m = [x for x in I.mems][0]
        return self.load(self.addr(I, m), op.size)

    def setop(self, I, k, v):
        op = I.ci.operands[k]
        if op.type == X86_OP_REG:
            self.setreg(I.ci.reg_name(op.reg), v)
        else:
            m = I.mems[0]
            self.store(I.address, self.addr(I, m), op.size, v)

    def run(self, entry, ret_sentinel=0xDEAD):
        self.push(ret_sentinel)
        pc = entry
        while True:
            self.steps += 1
            if self.steps > 5000:
                raise RuntimeError("step limit")
            if pc == ret_sentinel:
                return
            if pc == MEMSET:
                self.calls.append((pc, "memset-model", self.reg("rcx"), self.reg("rdx"), self.reg("r8")))
                a, d, n = self.reg("rcx"), self.reg("edx"), self.reg("r8")
                if not isinstance(n, int):
                    raise RuntimeError("memset size unknown")
                if a is U or not isinstance(a, tuple):
                    self.writes.append((pc, "memset", "?", 0, n))
                else:
                    self.cur_save = self.cur
                    self.cur = "memset"
                    self.store(pc, a, 0, 0)
                    self.writes.pop()
                    self.writes.append((pc, "memset", a[0], a[1], a[1] + n))
                    for i in range(n):
                        if a[0] == "R" and 0 <= a[1] + i < REC:
                            self.rec[a[1] + i] = (d & 0xFF) if isinstance(d, int) else U
                    self.cur = self.cur_save
                for v in VOLATILE:
                    self.r[v] = U
                self.r["rax"] = self.reg("rcx")
                pc = self.pop()
                continue
            ci = next(self.img.cs.disasm(self.img.read(pc, 16), pc))
            from rvlib import Insn
            I = Insn(self.img.cs, ci)
            nxt = pc + I.size
            m = I.mnemonic
            ops = ci.operands
            if m == "call":
                t = I.direct_target()
                self.calls.append((pc, t, self.reg("rcx"), self.reg("rdx"), self.reg("r8")))
                self.push(nxt)
                pc = t
                continue
            if m == "ret":
                pc = self.pop()
                continue
            if m == "jmp":
                if ops[0].type == X86_OP_IMM:
                    pc = I.direct_target()
                else:  # jmp [rip+x]: the memset thunk only
                    if pc != MEMSET:
                        raise RuntimeError("indirect jmp at %X" % pc)
                    pc = MEMSET
                continue
            if m.startswith("j"):
                a, b = self.flags
                if not (isinstance(a, int) and isinstance(b, int)):
                    raise RuntimeError("unknown branch at %X" % pc)
                sa = a - (1 << 32) if a >> 31 else a
                sb = b - (1 << 32) if b >> 31 else b
                take = {"jl": sa < sb, "jge": sa >= sb, "je": a == b, "jne": a != b}[m]
                pc = I.direct_target() if take else nxt
                continue
            if m == "push":
                self.push(self.opval(I, 0))
            elif m == "pop":
                self.setop(I, 0, self.pop())
            elif m in ("mov", "movaps", "movups", "movss", "movabs"):
                v = self.opval(I, 1)
                self.setop(I, 0, v)
            elif m in ("movzx",):
                self.setop(I, 0, self.opval(I, 1))
            elif m == "movsxd":
                v = self.opval(I, 1)
                self.setop(I, 0, (v - (1 << 32)) & MASK[8] if isinstance(v, int) and v >> 31 else v)
            elif m == "lea":
                a = self.addr(I, I.mems[0])
                if a is U:
                    v = U
                elif a[0] == "A":
                    v = a[1]
                else:
                    v = a
                self.setop(I, 0, v)
            elif m == "xor" and ops[0].type == X86_OP_REG and ops[1].type == X86_OP_REG and ops[0].reg == ops[1].reg:
                self.setop(I, 0, 0)
            elif m in ("and", "or", "sub", "add", "inc"):
                a = self.opval(I, 0)
                b = self.opval(I, 1) if m != "inc" else 1
                w = ops[0].size
                if m == "or" and isinstance(b, int) and b & MASK[w] == MASK[w]:
                    v = MASK[w]
                elif m == "and" and b == 0:
                    v = 0
                elif isinstance(a, tuple) and isinstance(b, int) and m in ("sub", "add"):
                    v = (a[0], a[1] + (b if m == "add" else -b))
                elif isinstance(a, int) and isinstance(b, int):
                    w = ops[0].size
                    v = {"and": a & b, "or": a | b, "sub": a - b, "add": a + b, "inc": a + 1}[m] & MASK[w]
                else:
                    v = U
                self.setop(I, 0, v)
            elif m == "nop":
                pass
            elif m == "cmp":
                self.flags = (self.opval(I, 0), self.opval(I, 1))
            elif m == "mulss":
                a, b = self.opval(I, 0), self.opval(I, 1)
                if isinstance(a, int) and isinstance(b, int):
                    fa = struct.unpack("<f", struct.pack("<I", a & 0xFFFFFFFF))[0]
                    fb = struct.unpack("<f", struct.pack("<I", b))[0]
                    v = struct.unpack("<I", struct.pack("<f", fa * fb))[0]
                else:
                    v = U
                self.setop(I, 0, v)
            elif m == "cvttss2si":
                a = self.opval(I, 1)
                v = int(struct.unpack("<f", struct.pack("<I", a & 0xFFFFFFFF))[0]) & 0xFFFFFFFF if isinstance(a, int) else U
                self.setop(I, 0, v)
            else:
                raise RuntimeError("unsupported %s at %X" % (I.text, pc))
            pc = nxt

    def runfn(self, entry):
        self.cur = None
        self._tagged_run(entry)

    def _tagged_run(self, entry):
        # tag each write with the function whose body contains the site
        self.run(entry)
        for i, w in enumerate(self.writes):
            site = w[0]
            fn = "memset" if site == MEMSET else owner(site)
            self.writes[i] = (site, fn) + tuple(w[2:])


def owner(site):
    if site is None:
        return "stack"
    for s, e in [CALLER] + HELPERS:
        if s <= site < e:
            return "%08X" % s
    return "?"


def regw(name):
    if name.startswith("xmm"):
        return 16
    if name.startswith("r") and (name[1:].isdigit() or name in ("rax", "rbx", "rcx", "rdx", "rsi", "rdi", "rbp", "rsp", "rip")):
        return 8
    if name.endswith("d") and name.startswith("r"):
        return 4
    if name.startswith("e"):
        return 4
    if name.endswith("w") or name in ("ax", "bx", "cx", "dx", "si", "di", "bp", "sp"):
        return 2
    return 1


def emulate(img):
    E = Emu(img)
    E.runfn(CALLER[0])
    return E


def spans(ws):
    return sorted((w[3], w[4]) for w in ws)


def merge(sp):
    out = []
    for s, e in sorted(sp):
        if out and s <= out[-1][1]:
            out[-1] = (out[-1][0], max(out[-1][1], e))
        else:
            out.append((s, e))
    return out


def checks(img, R):
    # --- bodies --------------------------------------------------------------
    B = Body(img, *CALLER)
    ents, pok = img.pdata_cover(*CALLER)
    R.check("caller 0041F730..0041FBE8 decodes exactly and .pdata tiles it", B.exact and pok)
    tot = 0
    for s, e in HELPERS:
        H = Body(img, s, e)
        R.check("helper %08X..%08X decodes exactly, has no call, ends in ret/jmp" % (s, e),
                H.exact and not H.calls() and H[H.order[-1]].mnemonic in ("ret", "jmp"))
        tot += e - s
    R.check("helper bytes total 124", tot == 124, str(tot))
    R.check("00861EC0 is the IAT thunk for memset", img.import_name_of_thunk(MEMSET) == "memset")
    calls = [(a, t) for a, t in B.calls()]
    exp_calls = [(0x41F754, MEMSET), (0x41F95F, 0x6C0520), (0x41F97A, 0x6C0520), (0x41F990, 0x46D110),
                 (0x41F99C, 0x46D110), (0x41FAFA, 0x3E5D00), (0x41FB5A, 0x3E37E0)]
    R.check("caller's direct calls are exactly the seven supplied sites", calls == exp_calls,
            " ".join("%X->%X" % c for c in calls))
    # helper register hygiene from bytes (no ABI premise needed for these leaves)
    clob = set()
    for s, e in HELPERS:
        H = Body(img, s, e)
        for a in H.order:
            clob |= H[a].reg_writes
    R.check("leaf helpers write none of rbx/rbp/rsi/rdi/xmm6", not (clob & {"rbx", "rbp", "rsi", "rdi", "xmm6"}),
            str(sorted(clob)))
    # --- emulation -------------------------------------------------------------
    E = emulate(img)
    R.check("emulation returns to the sentinel with rsp balanced", E.r["rsp"] == ("S", 0), str(E.r["rsp"]))
    cs = [(c[0], c[1], c[2], c[3], c[4]) for c in E.calls]
    by = {}
    for site, t, rcx, rdx, r8 in cs:
        by.setdefault(site, []).append((t, rcx, rdx, r8))
    R.check("41F754 memset rcx=R+0 edx=0 r8=740h", by.get(0x41F754, [None])[0] and
            by[0x41F754][0][1:] == (("R", 0), 0, 0x740), str(by.get(0x41F754)))
    R.check("6C0520 calls: rcx = R+210h then R+220h",
            [x[1] for x in by.get(0x41F95F, []) + by.get(0x41F97A, [])] == [("R", 0x210), ("R", 0x220)])
    R.check("46D110 calls: rcx = R+180h then R+1C0h",
            [x[1] for x in by.get(0x41F990, []) + by.get(0x41F99C, [])] == [("R", 0x180), ("R", 0x1C0)])
    idx = [x[2] & 0xFFFFFFFF if isinstance(x[2], int) else x[2] for x in by.get(0x41FAFA, [])]
    R.check("3E5D00 called 10 times with rcx=R+0 and edx = 0..9", idx == list(range(10)) and
            all(x[1] == ("R", 0) for x in by.get(0x41FAFA, [])), str(idx))
    R.check("3E37E0 called once with rcx = R+580h", [x[1] for x in by.get(0x41FB5A, [])] == [("R", 0x580)])
    ms = [c for c in E.calls if c[1] == "memset-model"]
    R.check("library fill reached twice: (R+0, 0, 740h) then (R+580h, 0, 50h)",
            [(c[2], c[3] & 0xFF if isinstance(c[3], int) else c[3], c[4]) for c in ms] ==
            [(("R", 0), 0, 0x740), (("R", 0x580), 0, 0x50)], str(ms))
    # --- footprints ------------------------------------------------------------
    W = E.writes
    rw = [w for w in W if w[2] == "R"]
    R.check("no write with an unresolved address or a non-record, non-stack base", all(w[2] in ("R",) for w in W),
            str([w for w in W if w[2] != "R"][:4]))
    own = [w for w in rw if w[1] == "%08X" % CALLER[0]]
    R.check("caller's own record writes (static sites, w and rw, LEA excluded) = 125", len(own) == 125, str(len(own)))
    helper = [w for w in rw if w[1] not in ("%08X" % CALLER[0],) and not (w[0] == MEMSET and w[3] == 0 and w[4] == REC)]
    R.check("composed helper writes (6C0520 x2, 46D110 x2, 3E5D00 x10, 3E37E0 fill) = 47", len(helper) == 47,
            str(len(helper)))
    fp = {}
    for w in helper:
        fp.setdefault(w[1], []).append((w[3], w[4]))
    R.check("6C0520 footprint = 210h..230h, 4-byte stores", merge(fp.get("006C0520", [])) == [(0x210, 0x230)] and
            all(e - s == 4 for s, e in fp.get("006C0520", [])), str(merge(fp.get("006C0520", []))))
    R.check("46D110->202C70 footprint = 180h..200h, 16-byte stores",
            merge(fp.get("00202C70", [])) == [(0x180, 0x200)] and all(e - s == 16 for s, e in fp.get("00202C70", [])),
            str(merge(fp.get("00202C70", []))))
    R.check("3E5D00 footprint = 4C0h..510h (WORD/DWORD/WORD per index)", merge(fp.get("003E5D00", [])) == [(0x4C0, 0x510)],
            str(merge(fp.get("003E5D00", []))))
    R.check("3E37E0 tail fill footprint = 580h..5D0h", merge(fp.get("memset", [])) == [(0x580, 0x5D0)],
            str(merge(fp.get("memset", []))))
    R.check("every record write lies inside [0, 740h)", all(0 <= w[3] and w[4] <= REC for w in rw),
            str([w for w in rw if not (0 <= w[3] and w[4] <= REC)][:3]))
    id0 = [w for w in rw if w[3] < 2 and w[4] > 0 and not (w[0] == MEMSET and w[3] == 0 and w[4] == REC)]
    R.check("exactly one write overlaps WORD +0 after the 740h fill: 41F795",
            [w[0] for w in id0] == [0x41F795], str([(hex(w[0]), w[3], w[4]) for w in id0]))
    a284 = [w for w in rw if w[3] < 0x288 and w[4] > 0x284 and not (w[0] == MEMSET and w[3] == 0 and w[4] == REC)]
    R.check("no write overlaps DWORD +284h after the 740h fill (full width)", not a284,
            str([(hex(w[0]), hex(w[3]), hex(w[4])) for w in a284]))
    hov = [w for w in helper if (w[3] < 2 and w[4] > 0) or (w[3] < 0x288 and w[4] > 0x284)]
    R.check("no helper write overlaps WORD +0 or DWORD +284h", not hov)
    # --- final values ----------------------------------------------------------
    def fin(o, n):
        bs = E.rec[o:o + n]
        return None if any(b is U for b in bs) else int.from_bytes(bytes(bs), "little")
    R.check("final WORD +0 = FFFFh", fin(0, 2) == 0xFFFF, str(fin(0, 2)))
    R.check("final DWORD +284h = 0", fin(0x284, 4) == 0, str(fin(0x284, 4)))
    # --- values that the packet left unsampled ---------------------------------
    src = 0x46D117 + struct.unpack_from("<i", img.read(0x46D113, 4))[0]
    R.check("46D110 copy source is 01F204E0 (in .data)", src == 0x01F204E0, "%X" % src)
    R.note("46D110 source initial bytes (file image): %s" % img.read(src, 64).hex())
    R.note("46D110 copies the file-initial identity matrix: %s" %
           (fin(0x180, 4) == 0x3F800000 and fin(0x194, 4) == 0x3F800000 and fin(0x184, 4) == 0))
    R.note("6C0520 stores (xmm1..3 and stack +28h) = %s" % [hex(fin(0x210 + 4 * i, 4) or 0) for i in range(8)])
    R.note("3E5D00 WORD at 4C0h + 8i = %s" % [fin(0x4C0 + 8 * i, 2) for i in range(10)])
    return E


CONTROLS = [
    # (label, va, new bytes, why it must fail)
    ("first 6C0520 receiver moved to R+27Ch (helper span 27C..28C overlaps 284)", 0x41F764, bytes([0x7C, 0x02])),
    ("41F771 WORD store moved from +2 to +0 (a second ID0 store)", 0x41F774, bytes([0x00])),
    ("41FA2A DWORD store moved from +288h to +286h (overlaps 284 by width)", 0x41FA2C, bytes([0x86, 0x02])),
    ("41F843 QWORD store of zero moved to +280h (starts below 284, overlaps by width, value still 0)", 0x41F846,
     bytes([0x80, 0x02])),
    ("loop bound 10 -> 80 at 41FB01 (3E5D00 span grows past 510h)", 0x41FB03, bytes([0x50])),
    ("3E37E0 fill size 50h -> 60h", 0x3E37E5, bytes([0x60])),
    ("41F9C0 `mov edi, esi` NOPed (index stays FFFFh)", 0x41F9C0, bytes([0x90, 0x90])),
    ("41F74B memset size 740h -> 280h (284 no longer filled)", 0x41F74D, bytes([0x80, 0x02])),
    ("46D110 copy source moved +40h", 0x46D113, None),
]


def main():
    img = Img.load()
    R = Rep("rv_clear")
    print("== packet integrity")
    check_manifest(R, "render-clear-callee-footprints", "c3e8141dc7fafc01b3fc7651abc3f5be49cf623f66e12c72b8a6615ef08439fc")
    print("== shipping-image re-derivation")
    E = checks(img, R)
    print("== composed write log (record writes only, in program order)")
    for w in E.writes:
        if w[2] == "R" and w[1] != "%08X" % CALLER[0]:
            print("      %s %-9s %03X..%03X" % ("%08X" % w[0], w[1], w[3], w[4]))
    print("== controls (each patched private image must FAIL at least one check above)")
    for label, va, nb in CONTROLS:
        if nb is None:
            d = struct.unpack_from("<i", img.read(va, 4))[0] + 0x40
            nb = struct.pack("<i", d)
        P = img.patched(va, nb)
        Rc = Rep(label)
        Rc.quiet = True
        try:
            checks(P, Rc)
            failed = Rc.fails
            why = "%d failed, e.g. %s" % (failed, "; ".join(Rc.failed[:4]))
        except Exception as e:
            failed = 1
            why = "refused: %s" % e
        R.check("control: " + label, failed > 0, why)
    print("TOTAL: %d checks, %d PASS, %d FAIL" % (R.n, R.n - R.fails, R.fails))


if __name__ == "__main__":
    main()
