"""rvlib.py - FABLE independent reviewer's minimal PE + capstone reader (struct + capstone only).

Not derived from ASTRA's prover or the shared role adapter. Reads the shipping image, checks its
sha256, decodes complete bodies linearly, builds a local CFG (direct jumps/jcc only) and exposes
memory-operand widths/roles from capstone's own detail.  A private patched copy of the image can
be made (Img.patched) so a control can show a check is sensitive to the defect it tests.
"""
import hashlib
import os
import struct
import sys

from capstone import Cs, CS_ARCH_X86, CS_MODE_64, CS_AC_READ, CS_AC_WRITE
from capstone.x86 import X86_OP_MEM, X86_OP_IMM, X86_OP_REG

SHA256 = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"


def find_exe():
    d = os.path.dirname(os.path.abspath(__file__))
    while True:
        p = os.path.join(d, "Database", "Tools", "work", "exe", "FFXII_TZA.exe")
        if os.path.exists(p):
            return p
        nd = os.path.dirname(d)
        if nd == d:
            fb = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\exe\FFXII_TZA.exe"
            if os.path.exists(fb):
                return fb
            raise SystemExit("cannot find Database/Tools/work/exe/FFXII_TZA.exe above " + __file__)
        d = nd


class Img(object):
    def __init__(self, data, check_sha=True):
        self.d = bytes(data)
        if check_sha:
            h = hashlib.sha256(self.d).hexdigest()
            if h != SHA256:
                raise SystemExit("EXE sha256 mismatch: " + h)
        pe = struct.unpack_from("<I", self.d, 0x3C)[0]
        nsec = struct.unpack_from("<H", self.d, pe + 6)[0]
        optsz = struct.unpack_from("<H", self.d, pe + 20)[0]
        opt = pe + 24
        self.base = struct.unpack_from("<Q", self.d, opt + 24)[0]
        # data directory 3 = exception (.pdata)
        self.exc_rva, self.exc_size = struct.unpack_from("<II", self.d, opt + 112 + 3 * 8)
        self.secs = []
        off = opt + optsz
        for _ in range(nsec):
            name = self.d[off:off + 8].rstrip(b"\0").decode("ascii", "replace")
            vs, va, rs, ra = struct.unpack_from("<IIII", self.d, off + 8)
            self.secs.append((name, va, vs, ra, rs))
            off += 40
        self.cs = Cs(CS_ARCH_X86, CS_MODE_64)
        self.cs.detail = True

    @classmethod
    def load(cls):
        p = find_exe()
        return cls(open(p, "rb").read())

    def off(self, va):
        r = va - self.base
        for name, sva, vs, ra, rs in self.secs:
            if sva <= r < sva + rs and r - sva < rs:
                return ra + (r - sva)
        raise ValueError("va %X not file-backed" % va)

    def read(self, va, n):
        o = self.off(va)
        return self.d[o:o + n]

    def u32(self, va):
        return struct.unpack("<I", self.read(va, 4))[0]

    def u64(self, va):
        return struct.unpack("<Q", self.read(va, 8))[0]

    def patched(self, va, newbytes):
        o = self.off(va)
        b = bytearray(self.d)
        b[o:o + len(newbytes)] = newbytes
        im = Img(bytes(b), check_sha=False)
        return im

    def pdata(self, va):
        """RUNTIME_FUNCTION (begin_va, end_va) containing va, by binary search."""
        rva = va - self.base
        n = self.exc_size // 12
        lo, hi = 0, n - 1
        po = self.off(self.base + self.exc_rva)
        while lo <= hi:
            m = (lo + hi) // 2
            b, e, u = struct.unpack_from("<III", self.d, po + m * 12)
            if rva < b:
                hi = m - 1
            elif rva >= e:
                lo = m + 1
            else:
                return (self.base + b, self.base + e)
        return None

    def pdata_cover(self, s, e):
        """All .pdata entries inside [s,e): returns (entries, ok) where ok means they tile [s,e) exactly,
        the first begins at s and every later one is a CHAININFO record whose chain root begins at s."""
        po = self.off(self.base + self.exc_rva)
        ents = []
        for i in range(self.exc_size // 12):
            b, en, u = struct.unpack_from("<III", self.d, po + i * 12)
            b += self.base
            en += self.base
            if s <= b < e:
                ui = self.off(self.base + u)
                fl = self.d[ui] >> 3
                n = self.d[ui + 2]
                root = b
                if fl & 4:
                    co = ui + 4 + ((n + 1) & ~1) * 2
                    root = struct.unpack_from("<I", self.d, co)[0] + self.base
                ents.append((b, en, fl, root))
        ents.sort()
        link = dict((b, root) for b, en, fl, root in ents)
        res = []
        for b, en, fl, root in ents:
            seen = 0
            while root in link and link[root] != root and seen < 16:
                root = link[root]
                seen += 1
            res.append((b, en, fl, root))
        ents = res
        ok = bool(ents) and ents[0][0] == s and ents[-1][1] == e and all(
            ents[i][1] == ents[i + 1][0] for i in range(len(ents) - 1)) and all(
            x[3] == s for x in ents[1:]) and all(not (x[2] & 4) for x in ents[:1])
        return ents, ok

    def import_name_of_thunk(self, va):
        """For an `FF 25` jmp thunk, read the IAT slot's on-disk value (hint/name RVA) and the name."""
        ins = next(self.cs.disasm(self.read(va, 6), va))
        if ins.mnemonic != "jmp" or ins.operands[0].type != X86_OP_MEM:
            return None
        slot = ins.address + ins.size + ins.operands[0].mem.disp
        hn = self.u64(slot)
        if hn >> 63:
            return "ordinal"
        s = self.read(self.base + hn + 2, 64)
        return s.split(b"\0")[0].decode("ascii", "replace")


GPR = {}
for fam in ("ax", "bx", "cx", "dx"):
    GPR["r" + fam] = GPR["e" + fam] = GPR[fam] = GPR[fam[0] + "l"] = GPR[fam[0] + "h"] = "r" + fam
for fam in ("si", "di", "bp", "sp"):
    GPR["r" + fam] = GPR["e" + fam] = GPR[fam] = GPR[fam + "l"] = "r" + fam
for i in range(8, 16):
    for suf in ("", "d", "w", "b"):
        GPR["r%d%s" % (i, suf)] = "r%d" % i


# capstone 5.0.7 reports some SSE stores (e.g. 0F 11 01 movups [rcx], xmm0) as READ only.  Treat a memory
# operand in destination position as written unless the mnemonic only reads its first operand.
NOT_DEST_WRITE = set("cmp test bt ucomiss ucomisd comiss comisd nop lea push call jmp prefetch prefetchw "
                     "prefetcht0 prefetcht1 prefetcht2 prefetchnta ptest".split())


def fam(regname):
    return GPR.get(regname, regname)


class Insn(object):
    def __init__(self, cs, ci):
        self.ci = ci
        self.address = ci.address
        self.size = ci.size
        self.bytes = bytes(ci.bytes)
        self.mnemonic = ci.mnemonic
        self.op_str = ci.op_str
        self.text = (ci.mnemonic + " " + ci.op_str).strip()
        self.mems = []
        for k, op in enumerate(ci.operands):
            if op.type == X86_OP_MEM:
                m = op.mem
                self.mems.append({
                    "base": ci.reg_name(m.base) if m.base else None,
                    "index": ci.reg_name(m.index) if m.index else None,
                    "scale": m.scale,
                    "disp": m.disp,
                    "size": op.size,
                    "read": bool(op.access & CS_AC_READ),
                    "write": bool(op.access & CS_AC_WRITE) or (k == 0 and ci.mnemonic not in NOT_DEST_WRITE),
                    "cs_write": bool(op.access & CS_AC_WRITE),
                })
        try:
            rr, ww = ci.regs_access()
            self.reg_reads = set(fam(ci.reg_name(r)) for r in rr)
            self.reg_writes = set(fam(ci.reg_name(r)) for r in ww)
        except Exception:
            self.reg_reads, self.reg_writes = set(), set()
        self.imm = [op.imm for op in ci.operands if op.type == X86_OP_IMM]

    def direct_target(self):
        if self.imm and (self.mnemonic == "call" or self.mnemonic.startswith("j")):
            return self.imm[0] & 0xFFFFFFFFFFFFFFFF
        return None

    def __repr__(self):
        return "%08X  %s" % (self.address, self.text)


class Body(object):
    """Linear decode of [start, end). Records whether decode covers the range exactly."""

    def __init__(self, img, start, end):
        self.img, self.start, self.end = img, start, end
        code = img.read(start, end - start)
        self.ins = {}
        self.order = []
        pos = start
        for ci in img.cs.disasm(code, start):
            if ci.address != pos:
                break
            I = Insn(img.cs, ci)
            self.ins[I.address] = I
            self.order.append(I.address)
            pos = ci.address + ci.size
        self.exact = (pos == end)

    def __getitem__(self, a):
        return self.ins[a]

    def succ(self, a):
        I = self.ins[a]
        m = I.mnemonic
        nxt = a + I.size
        if m == "ret" or m == "int3":
            return []
        if m == "jmp":
            t = I.direct_target()
            if t is not None and self.start <= t < self.end:
                return [t]
            return []  # tail jump / indirect: leaves the body
        if m.startswith("j"):
            t = I.direct_target()
            out = [nxt]
            if t is not None and self.start <= t < self.end:
                out.append(t)
            return out
        return [nxt] if nxt < self.end else []

    def exits(self):
        """(rets, tail_jumps_out, branch_targets_outside)."""
        rets, tails, outs = [], [], []
        for a in self.order:
            I = self.ins[a]
            if I.mnemonic == "ret":
                rets.append(a)
            elif I.mnemonic == "jmp":
                t = I.direct_target()
                if t is None or not (self.start <= t < self.end):
                    tails.append((a, t))
            elif I.mnemonic.startswith("j"):
                t = I.direct_target()
                if t is not None and not (self.start <= t < self.end):
                    outs.append((a, t))
        return rets, tails, outs

    def reach(self, frm, avoid=()):
        avoid = set(avoid)
        seen = set()
        stack = [frm]
        while stack:
            a = stack.pop()
            if a in seen or a in avoid or a not in self.ins:
                continue
            seen.add(a)
            stack.extend(self.succ(a))
        return seen

    def dominates(self, a, b, entry=None):
        """True when every path entry->b passes a (a != b)."""
        entry = self.start if entry is None else entry
        if a == entry:
            return True
        return b not in self.reach(entry, avoid=[a])

    def calls(self):
        return [(a, self.ins[a].direct_target()) for a in self.order if self.ins[a].mnemonic == "call"]

    def mem_writes(self, pred=lambda m: True):
        out = []
        for a in self.order:
            for m in self.ins[a].mems:
                if m["write"] and pred(m):
                    out.append((a, m))
        return out


class Report(object):
    def __init__(self, title):
        self.title = title
        self.lines = []
        self.fails = 0
        self.quiet = False

    def check(self, name, cond, detail=""):
        ok = bool(cond)
        if not ok:
            self.fails += 1
        if not self.quiet:
            line = "%s  %s%s" % ("PASS" if ok else "FAIL", name, ("  | " + detail) if detail else "")
            print(line)
        return ok

    def note(self, s):
        if not self.quiet:
            print("NOTE  " + s)


def expect(R, B, a, text, name=None):
    I = B.ins.get(a)
    got = I.text if I else "<no instruction boundary>"
    return R.check(name or ("%08X is `%s`" % (a, text)), got == text, "" if got == text else "got `%s`" % got)


def run_control(label, img_factory, check_fn, must_fail=True):
    """Run check_fn(img, Report) on a mutated image; the control PASSES when the check now FAILS."""
    R = Report(label)
    R.quiet = True
    try:
        check_fn(img_factory(), R)
        failed = R.fails > 0
    except Exception as e:  # a refusal by exception also counts as a rejection
        failed = True
    return failed if must_fail else not failed


def check_manifest(R, slug, expected_sha):
    """Hash the packet manifest and every member it lists (working tree)."""
    import json
    exe = find_exe()
    db = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(exe))))  # .../Database
    ev = os.path.join(db, "FFXII TZA", "_experiments", "evidence", slug)
    mb = open(os.path.join(ev, "manifest.json"), "rb").read()
    R.check("manifest.json sha256 = %s..." % expected_sha[:16], hashlib.sha256(mb).hexdigest() == expected_sha,
            hashlib.sha256(mb).hexdigest())
    mem = json.loads(mb)["members"]
    bad = []
    for m in mem:
        p = os.path.join(ev, m["path"])
        if not os.path.exists(p) or hashlib.sha256(open(p, "rb").read()).hexdigest() != m["sha256"]:
            bad.append(m["path"])
    R.check("all %d manifest members hash as listed" % len(mem), not bad, str(bad[:5]))
