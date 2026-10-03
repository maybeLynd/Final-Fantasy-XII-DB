"""k54_residue.py - FABLE, 2026-10-03. The residue of effect-mesh-records-kind-54.md after opus-k54-lighting-1002:
(A) the selectors of the draw paths 00437130, 00438860, 004434D0, 00444340; (B) whether the planar index k (the dword
003962F0 reads at param + 0x1D8 + 4k) is the pass index p; (C) where the pass bytes come from (census:
census_k54_modes.py).

Reader: rvlib.py (copied from fable-review-astra-ov42-caller-quotient-bound-1002), the affine reaching-definition pass
k54flow.py (this directory), and a Unicorn run of the four parameter-block writers over the certified image.
Sections:
  A1  static anchors: what selects each draw path (004355D0's +0x1F1 test; the grid walks' +0x672 / +0x6D2 test).
  A2  executed: 00449AB0 composes +0x1F1 / +0x1F2 from definition +0x590 (all 256 values); the grid walks pick
      00444340 / 004434D0 from +0x672 / +0x6D2 bit 0 and copy that bit to +0x1F1 bit 3.
  A3  per draw path, the pass-byte switch: which lighting routine each mode 0..6 x axis 0/1 reaches (CFG walk).
  B   per draw path, an inductive affine proof over the pass loop: the +0x1B0 / +0x1B4 reads index param + p and the
      planar call's r8 is param + 4p + 0x1D8 (so k = p).
  C1  who calls the draw paths (raw E8 / E9 / 0F 8x and absolute-pointer census) and who writes byte param+0x1B0.
  C2  executed: each of the four walks copies pass-slot byte +7 -> +0x1B0+p, +0xB bit 0 -> +0x1B4+p and the slot's
      +0x90 float track -> +0x1D8+4p, compacting skipped slots (byte +0 = 0 or a failed texture lookup) with ONE p.
  K   controls on patched copies: each must make its check fail.
Last line: 'FAILS n'.
"""
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from rvlib import Img, Report, expect, find_exe  # noqa: E402
from k54flow import Flow  # noqa: E402
from capstone.x86 import X86_OP_MEM  # noqa: E402
from unicorn import Uc, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE, UC_HOOK_MEM_UNMAPPED  # noqa: E402
from unicorn.x86_const import (UC_X86_REG_RAX, UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_RSP,  # noqa: E402
                               UC_X86_REG_RIP, UC_X86_REG_XMM0)

LIGHT = {0x395CF0: "395CF0", 0x395780: "395780", 0x3962F0: "3962F0", 0x396A30: "396A30", 0x396560: "396560"}
# draw path: (size, param register, record register, mode-read site, axis sites, planar call, +0x1AC site)
PATHS = {
    0x4355D0: (5936, "rdx", "rcx", 0x4359E5, (0x435A75, 0x435BBE), 0x435AF1, 0x435BFE),
    0x437130: (5930, "rdx", "rcx", 0x437486, (0x437527, 0x437693), 0x4375BE, 0x4376CC),
    0x438860: (20603, "rdx", "rcx", 0x438C70, (0x438D0A, 0x438E70), 0x438D98, 0x438EB0),
    0x4434D0: (3681, "rcx", None, 0x443865, (0x443942, 0x443B59), 0x4439AE, 0x443BBA),
    0x444340: (3979, "rcx", None, 0x444711, (0x44480D, 0x444A33), 0x444864, 0x444A89),
}
# what 004355D0's own switch reaches (opus-k54-lighting-1002 A-checks): mode -> {axis: routine}
EXPECT_MAP = {1: {0: {"395CF0"}, 1: {"395780"}}, 2: {0: {"3962F0"}, 1: {"3962F0"}},
              3: {0: {"396A30"}, 1: {"396560"}}, 4: {0: {"396A30"}, 1: {"396560"}}}
for _m in (0, 5, 6, 255):
    EXPECT_MAP[_m] = {0: set(), 1: set()}


# ------------------------------------------------------------------------------------------------ A3: switch walk
def switch_map(img, f, n, site, uvsel):
    F = Flow(img, f, f + n)
    B = F.B
    I = B[site]
    reg = I.ci.reg_name(I.ci.operands[0].reg)
    from rvlib import fam
    R = fam(reg)
    out = {}
    arms = {}
    for v in sorted(EXPECT_MAP):
        val, Z, pc = v, None, site + I.size
        steps = 0
        while steps < 40:
            steps += 1
            J = B[pc]
            m = J.mnemonic
            ops = J.ci.operands
            if m in ("sub", "cmp") and fam(J.ci.reg_name(ops[0].reg)) == R and J.imm:
                r = val - J.imm[0]
                Z = (r == 0)
                if m == "sub":
                    val = r
                pc += J.size
            elif m in ("je", "jne"):
                take = Z if m == "je" else (not Z)
                pc = J.direct_target() if take else pc + J.size
            elif m == "jmp":
                pc = J.direct_target()
                break
            elif m == "mov" and ops[0].type == X86_OP_MEM:     # a spill between the switch's tests (00438C78)
                pc += J.size
            else:
                break
        arms[v] = pc
        res = {}
        for axis in (0, 1):
            got = set()
            seen = set()
            stack = [(pc, None)]
            while stack:
                a, flag = stack.pop()
                if a in seen or a == uvsel or a not in B.ins:
                    continue
                seen.add(a)
                J = B[a]
                m = J.mnemonic
                if m == "call" and J.direct_target() in LIGHT:
                    got.add(LIGHT[J.direct_target()])
                if m == "cmp" and any(x["disp"] == 0x1B4 for x in J.mems):
                    flag = "axis"
                elif m in ("cmp", "test", "sub", "add", "and", "or", "xor", "inc", "dec", "shl", "shr"):
                    flag = None
                if m in ("je", "jne") and flag == "axis":
                    taken = (axis == 0) if m == "je" else (axis != 0)
                    stack.append((J.direct_target() if taken else a + J.size, flag))
                    continue
                for t in B.succ(a):
                    stack.append((t, flag))
            res[axis] = got
        out[v] = res
    return out, arms, B


def arm_calls(B, start, stop):
    """direct calls on the straight-line+branches region from `start` up to `stop` (first 40 instructions)."""
    calls, seen, stack = [], set(), [start]
    while stack:
        a = stack.pop()
        if a in seen or a == stop or a not in B.ins or len(seen) > 200:
            continue
        seen.add(a)
        J = B[a]
        if J.mnemonic == "call":
            calls.append((a, J.direct_target()))
        stack.extend(B.succ(a))
    return sorted(calls)


def fragments(img):
    """every .pdata entry as (begin, end, root begin), CHAININFO followed to its root."""
    po = img.off(img.base + img.exc_rva)
    ents = {}
    for i in range(img.exc_size // 12):
        b, e, u = struct.unpack_from("<III", img.d, po + i * 12)
        ui = img.off(img.base + u)
        fl = img.d[ui] >> 3
        n = img.d[ui + 2]
        parent = None
        if fl & 4:
            co = ui + 4 + ((n + 1) & ~1) * 2
            parent = struct.unpack_from("<I", img.d, co)[0] + img.base
        ents[b + img.base] = (e + img.base, parent)
    out = []
    for b, (e, parent) in ents.items():
        root, k = b, 0
        while ents.get(root, (0, None))[1] is not None and k < 16:
            root = ents[root][1]
            k += 1
        out.append((b, e, root))
    return sorted(out)


def arm_globals(B, start):
    """rip-relative operands in the matrix area 02AEEA00..02AEEC40 on the paths from `start` to the first lighting call."""
    out, seen, stack = set(), set(), [start]
    while stack:
        a = stack.pop()
        if a in seen or a not in B.ins:
            continue
        seen.add(a)
        J = B[a]
        if J.mnemonic == "call" and J.direct_target() in LIGHT:
            continue
        for m in J.mems:
            if m["base"] == "rip":
                g = a + J.size + m["disp"]
                if 0x2AEEA00 <= g < 0x2AEEC40:
                    out.add(g & ~0xF)
        stack.extend(B.succ(a))
    return sorted(out)


# ------------------------------------------------------------------------------------------------ B: loop proof
def loop_check(img, f, R, tag="", quiet=False):
    n, preg, rreg, msite, asites, planar, uvsel = PATHS[f]
    F = Flow(img, f, f + n)
    hdrs = []
    for a in F.B.order:
        I = F.B[a]
        t = I.direct_target()
        if I.mnemonic.startswith("j") and I.mnemonic != "jmp" and t is not None and t < a and t <= msite < a:
            near = [x for x in F.B.order if a - 0x40 <= x < a and any(m["disp"] == 0x1F0 for m in F.B[x].mems)]
            if near:
                hdrs.append(t)
    ok_h = len(hdrs) == 1
    R.check("%s%08X: one pass-loop back edge (after a +0x1F0 read) encloses the mode read" % (tag, f), ok_h,
            str(["%08X" % h for h in hdrs]))
    if not ok_h:
        return None
    h = hdrs[0]
    dom = all(F.B.dominates(h, s) for s in (msite, planar) + tuple(asites))
    R.check("%s%08X: header %08X dominates the mode read, both axis reads and the planar call" % (tag, f, h), dom)
    ok, hyp, ins, log = F.loop_proof(h, preg, rreg)
    R.check("%s%08X: inductive proof reaches a fixpoint" % (tag, f), ok, "; ".join(log))
    ctr = sorted(("SP0%+#x" % L) if isinstance(L, int) else L for L, v in hyp.items() if v == (None, 1, 0))
    if not quiet:
        R.note("%08X pass counters equal to p at the header (start 0, +1 per pass): %s" % (f, ", ".join(ctr)))
    st = ins.get(msite)
    I = F.B[msite]
    a_mode = F.addr(st, I.mems[0]) if st else None
    R.check("%s%08X: mode read %08X `%s` addresses param + p + 0x1B0" % (tag, f, msite, I.text),
            a_mode == ("PARAM", 1, 0x1B0), str(a_mode))
    for s in asites:
        J = F.B[s]
        a_ax = F.addr(ins[s], J.mems[0]) if s in ins else None
        R.check("%s%08X: axis read %08X addresses param + p + 0x1B4" % (tag, f, s), a_ax == ("PARAM", 1, 0x1B4),
                str(a_ax))
    r8 = ins[planar].get("r8") if planar in ins else None
    R.check("%s%08X: planar call %08X passes r8 = param + 4p + 0x1D8 (k = p)" % (tag, f, planar),
            r8 == ("PARAM", 4, 0x1D8), str(r8))
    return h


# ------------------------------------------------------------------------------------------------ C2: emulation
BASE = 0x120000
SCR = 0x10000000
STACK = 0x20000000
RET = 0x30000000
NULLPAGE = 0x100000          # [0, 0x100000) mapped: the walks write vertex staging through BSS pointers that are 0
GPARAM = 0x01FD4A78          # [01FD4A78] + 0x800 is the draw-parameter block


class Emu(object):
    def __init__(self, img):
        mu = Uc(UC_ARCH_X86, UC_MODE_64)
        pe = struct.unpack_from("<I", img.d, 0x3C)[0]
        opt = pe + 24
        size_img = (struct.unpack_from("<I", img.d, opt + 56)[0] + 0xFFF) & ~0xFFF
        mu.mem_map(BASE, size_img)
        mu.mem_write(BASE, img.d[:0x1000])
        for name, va, vs, ra, rs in img.secs:
            mu.mem_write(BASE + va, img.d[ra:ra + min(rs, vs if vs else rs)])
        mu.mem_map(0, NULLPAGE)
        mu.mem_map(SCR, 0x400000)
        mu.mem_map(STACK, 0x100000)
        mu.mem_map(RET, 0x1000)
        mu.mem_write(RET, b"\xf4")
        self.mu = mu
        self.fault = None
        self.log = []
        mu.hook_add(UC_HOOK_MEM_UNMAPPED, self._unm)

    def _unm(self, mu, access, addr, size, value, ud):
        self.fault = ("unmapped", access, hex(addr), hex(mu.reg_read(UC_X86_REG_RIP)))
        return False

    def stub(self, addr, fn):
        def hit(mu, a, size, ud):
            fn(self)
            rsp = mu.reg_read(UC_X86_REG_RSP)
            mu.reg_write(UC_X86_REG_RIP, struct.unpack("<Q", mu.mem_read(rsp, 8))[0])
            mu.reg_write(UC_X86_REG_RSP, rsp + 8)
        self.mu.hook_add(UC_HOOK_CODE, hit, begin=addr, end=addr)

    def w(self, a, b):
        self.mu.mem_write(a, bytes(b))

    def r(self, a, n):
        return bytes(self.mu.mem_read(a, n))

    def call(self, fn, rcx):
        mu = self.mu
        rsp = STACK + 0xF0000
        mu.mem_write(rsp, struct.pack("<Q", RET) + b"\0" * 0x40)
        mu.reg_write(UC_X86_REG_RSP, rsp)
        mu.reg_write(UC_X86_REG_RCX, rcx)
        self.fault = None
        self.log = []
        self.captured = []
        try:
            mu.emu_start(fn, RET, count=3_000_000)
        except Exception as e:  # noqa: BLE001
            self.fault = self.fault or ("exception", str(e))
        return self.fault is None and mu.reg_read(UC_X86_REG_RIP) == RET


INST, DEF, PARAMB, RES, RES2, TEX = SCR + 0x10000, SCR + 0x20000, SCR + 0x40000, SCR + 0x50000, SCR + 0x51000, SCR + 0x52000
# walk: (definition slot-byte base, path byte, draw callees, instance count fields)
WALKS = {
    0x449AB0: dict(slots=0x250, pathb=0x590, draws=(0x4355D0,), dims={}),
    0x4453D0: dict(slots=0x350, pathb=0x672, draws=(0x4434D0, 0x444340), dims={0x254: 2}),
    0x447020: dict(slots=0x3B0, pathb=0x6D2, draws=(0x4434D0, 0x444340), dims={0x268: 2, 0x26C: 2}),
    0x447ED0: dict(slots=0x3B0, pathb=0x6D2, draws=(0x4434D0, 0x444340), dims={0x270: 2, 0x274: 2}),
}
WSIZE = {0x449AB0: 1741, 0x4453D0: 1914, 0x447020: 2062, 0x447ED0: 2350}


def make_walk_emu(img, walk):
    E = Emu(img)
    E.tex_ok = True
    E.captured = []
    body = Flow(img, walk, walk + WSIZE[walk]).B
    targets = sorted(set(t for _, t in body.calls() if t is not None))
    draws = WALKS[walk]["draws"]

    def f32(x):
        return struct.unpack("<I", struct.pack("<f", x))[0]

    def generic(E_):
        E_.mu.reg_write(UC_X86_REG_RAX, 0)
        E_.mu.reg_write(UC_X86_REG_XMM0, f32(0.5))

    def track(E_):                  # 004309C0: the float track; return its own definition offset as the value
        rcx = E_.mu.reg_read(UC_X86_REG_RCX)
        E_.mu.reg_write(UC_X86_REG_XMM0, f32(float(rcx - DEF) if DEF <= rcx < DEF + 0x1000 else 1.0))

    def colour(E_):                 # 0042FDB0
        rcx = E_.mu.reg_read(UC_X86_REG_RCX)
        E_.mu.reg_write(UC_X86_REG_RAX, 0xC0000000 | ((rcx - DEF) & 0xFFFF))

    def tex(E_):                    # 00431830: texture lookup
        E_.mu.reg_write(UC_X86_REG_RAX, TEX if E_.tex_ok else 0)

    def resolve(E_):                # 0020E600: resource id -> record
        E_.mu.reg_write(UC_X86_REG_RAX, RES)

    def mk_capture(addr):
        def cap(E_):
            p = E_.mu.reg_read(UC_X86_REG_RDX if addr == 0x4355D0 else UC_X86_REG_RCX)
            E_.captured.append((addr, p, E_.r(p, 0x200)))
        return cap

    special = {0x4309C0: track, 0x42FDB0: colour, 0x431830: tex, 0x20E600: resolve}
    for t in targets:
        if t in draws:
            E.stub(t, mk_capture(t))
        else:
            E.stub(t, special.get(t, generic))
    E.stubbed = targets
    return E


def setup_walk(E, walk, byte0, pathbyte=0, flag4a=0):
    W = WALKS[walk]
    E.w(INST, b"\0" * 0x800)
    E.w(DEF, b"\0" * 0x1000)
    E.w(PARAMB - 0x800, b"\0" * 0xC00)
    E.w(INST, b"\x01")
    E.w(INST + 0x20, struct.pack("<Q", DEF))
    E.w(INST + 0x40, struct.pack("<I", 1))
    for off, v in W["dims"].items():
        E.w(INST + off, struct.pack("<I", v))
    E.w(DEF + 0x4A, bytes([flag4a]))
    E.w(DEF + W["pathb"], bytes([pathbyte]))
    if walk == 0x4453D0:
        E.w(DEF + 0x670, struct.pack("<H", 1))
    if walk in (0x447020, 0x447ED0):
        E.w(DEF + 0x6D0, struct.pack("<H", 1))
    if walk == 0x449AB0:
        E.w(DEF + 0x5A0, struct.pack("<8I", *([7] * 8)))
        E.w(DEF + 0x570, b"\x01" * 4)
    for j in range(4):
        s = DEF + W["slots"] + 0xF0 * j
        E.w(s, bytes([byte0[j]]))
        E.w(s + 7, bytes([0x10 + j]))
        E.w(s + 0xA, bytes([0x08 if j & 1 else 0x00]))
        E.w(s + 0xB, bytes([(j & 1) | 0x40]))
    E.w(RES, b"\0" * 0x400)
    E.w(RES, struct.pack("<Q", RES2))
    E.w(RES + 0x1C, struct.pack("<H", 1))
    E.w(RES2, b"\0" * 0x40)
    E.w(GPARAM, struct.pack("<Q", PARAMB - 0x800))


def expected(walk, byte0, tex_ok):
    W = WALKS[walk]
    act = []
    for j, b in enumerate(byte0):
        if b == 0:
            continue
        if b >= 5:
            act.append(j)
        elif b == 1 and walk == 0x449AB0:
            act.append(j)             # mode 1 of the mesh walk resolves the record's own texture (stubbed present)
        elif tex_ok:
            act.append(j)
    return act


def check_capture(walk, cap, act):
    W = WALKS[walk]
    blk = cap[2]
    bad = []
    if blk[0x1F0] != len(act):
        bad.append("count %d != %d" % (blk[0x1F0], len(act)))
    for p, j in enumerate(act):
        if blk[0x1B0 + p] != 0x10 + j:
            bad.append("+0x1B0+%d=%#x" % (p, blk[0x1B0 + p]))
        if blk[0x1B4 + p] != (j & 1):
            bad.append("+0x1B4+%d=%#x" % (p, blk[0x1B4 + p]))
        want = float(W["slots"] - 0xA0 + 0xF0 * j + 0x90)
        got = struct.unpack_from("<f", blk, 0x1D8 + 4 * p)[0]
        if got != want:
            bad.append("+0x1D8+4*%d=%r want %r" % (p, got, want))
        if (blk[0x1AC + p] & 1) != (1 if j & 1 else 0):
            bad.append("+0x1AC+%d=%#x" % (p, blk[0x1AC + p]))
    return bad


def run_walk_matrix(img, walk, R, tag="", values=(0, 1, 2, 3, 4, 5), quiet=False):
    E = make_walk_emu(img, walk)
    runs = bad_runs = faults = empty_draws = 0
    first_bad = None
    import itertools
    for byte0 in itertools.product(values, repeat=4):
        for tex_ok in (True, False):
            setup_walk(E, walk, byte0)
            E.tex_ok = tex_ok
            ok = E.call(walk, INST)
            runs += 1
            act = expected(walk, byte0, tex_ok)
            caps = [c for c in E.captured]
            if not ok:
                faults += 1
                first_bad = first_bad or (byte0, tex_ok, E.fault)
                continue
            if not act:
                # 00449AB0 and 004453D0 test +0x1F0 before drawing; 00447020 / 00447ED0 call the draw anyway, whose
                # own loop guard (+0x1F0 == 0) then draws nothing
                if walk in (0x447020, 0x447ED0):
                    if len(caps) != 1 or caps[0][2][0x1F0] != 0:
                        bad_runs += 1
                        first_bad = first_bad or (byte0, tex_ok, "no pass: captures %d" % len(caps))
                    else:
                        empty_draws += 1
                elif caps:
                    bad_runs += 1
                    first_bad = first_bad or (byte0, tex_ok, "drew with no pass")
                continue
            if len(caps) != 1:
                bad_runs += 1
                first_bad = first_bad or (byte0, tex_ok, "captures %d" % len(caps))
                continue
            b = check_capture(walk, caps[0], act)
            if b:
                bad_runs += 1
                first_bad = first_bad or (byte0, tex_ok, b)
    R.check("%s%08X: over %d runs (slot byte +0 in %s x4, texture lookup present / absent) the block holds, for the "
            "p-th kept slot j: +0x1B0+p = slot j byte +7, +0x1B4+p = byte +0xB bit 0, +0x1D8+4p = slot j's +0x90 "
            "track, +0x1F0 = kept count" % (tag, walk, runs, list(values)),
            bad_runs == 0 and faults == 0, "bad %d faults %d first %s" % (bad_runs, faults, first_bad))
    if not quiet:
        R.note("%08X: runs with no kept slot that still called the draw (with +0x1F0 = 0): %d" % (walk, empty_draws))
    return E


def run_setups(img, R, only=None):
    import random
    rnd = random.Random(1003)
    for setup, sl, types in ((0x538DB0, 0x250, "0x05"), (0x538C80, 0x350, "0x04"), (0x538EB0, 0x3B0, "0x06/0x07")):
        if only and setup not in only:
            continue
        Es = Emu(img)
        Es.stub(0x20E600, lambda E_: E_.mu.reg_write(UC_X86_REG_RAX, RES))
        Es.stub(0x20E620, lambda E_: E_.mu.reg_write(UC_X86_REG_RAX, 0x1234))
        Es.stub(0x3AA280, lambda E_: E_.mu.reg_write(UC_X86_REG_RAX, RES))
        runs = changed = faults = moved = 0
        for t in range(48):
            blob = bytearray(rnd.getrandbits(8) for _ in range(0x800))
            for j in range(4):
                blob[sl + 0xF0 * j] = (t + j) % 6
            Es.w(RES, b"\0" * 0x400)
            Es.w(DEF, bytes(blob))
            mu = Es.mu
            rsp = STACK + 0xF0000
            mu.mem_write(rsp, struct.pack("<Q", RET) + b"\0" * 0x40)
            mu.reg_write(UC_X86_REG_RSP, rsp)
            mu.reg_write(UC_X86_REG_RCX, DEF)
            mu.reg_write(UC_X86_REG_RDX, 0x5000)
            Es.fault = None
            try:
                mu.emu_start(setup, RET, count=2_000_000)
            except Exception as e:  # noqa: BLE001
                Es.fault = Es.fault or str(e)
            runs += 1
            if Es.fault or mu.reg_read(UC_X86_REG_RIP) != RET:
                faults += 1
                continue
            after = Es.r(DEF, 0x800)
            moved += sum(1 for a, b in zip(blob, after) if a != b)
            for j in range(4):
                for o in (0, 7, 0xB):
                    if after[sl + 0xF0 * j + o] != blob[sl + 0xF0 * j + o]:
                        changed += 1
        R.check("C3 %08X (type %s setup), %d random definitions: slot bytes +0 / +7 / +0xB at definition +0x%X + "
                "0xF0j unchanged (0 of %d differ), while the setup rewrote %d other bytes (it does run)"
                % (setup, types, runs, sl, runs * 12, moved), changed == 0 and faults == 0 and moved > 0,
                "changed %d faults %d" % (changed, faults))


def main(img):
    R = Report("k54_residue")
    print("== k54_residue.py (FABLE 2026-10-03); image sha256 checked by rvlib: %s" % find_exe())

    # -------------------------------------------------------------- A1
    print("\n== A1 what selects each draw path (static anchors)")
    B = Flow(img, 0x4355D0, 0x4355D0 + 5936).B
    for a, t in ((0x43566F, "movzx eax, byte ptr [r15 + 0x1f1]"), (0x435677, "cmp al, 0x80"),
                 (0x435679, "jb 0x435688"), (0x435681, "call 0x438860"), (0x435688, "test al, 8"),
                 (0x43568A, "je 0x435699"), (0x435692, "call 0x437130")):
        expect(R, B, a, t)
    for w, rows in ((0x4453D0, ((0x445AEC, "test byte ptr [rcx + 0x672], 1"), (0x445AF6, "je 0x445aff"),
                                (0x445AF8, "call 0x444340"), (0x445AFF, "call 0x4434d0"))),
                    (0x447020, ((0x4477CD, "test byte ptr [rcx + 0x6d2], 1"), (0x4477D7, "je 0x4477e0"),
                                (0x4477D9, "call 0x444340"), (0x4477E0, "call 0x4434d0"))),
                    (0x447ED0, ((0x448797, "test byte ptr [r13 + 0x6d2], 1"), (0x44879F, "je 0x4487a8"),
                                (0x4487A1, "call 0x444340"), (0x4487A8, "call 0x4434d0")))):
        Bw = Flow(img, w, w + WSIZE[w]).B
        for a, t in rows:
            expect(R, Bw, a, t)

    # -------------------------------------------------------------- A2
    print("\n== A2 executed: the walks compose the selector bytes")
    E = make_walk_emu(img, 0x449AB0)
    bad = []
    paths = {}
    for m in range(256):
        setup_walk(E, 0x449AB0, (5, 0, 0, 0), pathbyte=m, flag4a=0x14)
        ok = E.call(0x449AB0, INST)
        if not ok or len(E.captured) != 1:
            bad.append((m, "run", E.fault, len(E.captured)))
            continue
        blk = E.captured[0][2]
        f1, f2 = blk[0x1F1], blk[0x1F2]
        bit = lambda k: (m >> k) & 1
        want1 = 5 | ((bit(0) | bit(5)) << 3) | (bit(1) << 4) | (bit(2) << 5) | (bit(3) << 6) | (bit(5) << 7)
        want2 = (m >> 6) & 3
        if f1 != want1 or f2 != want2:
            bad.append((m, hex(f1), hex(want1), hex(f2), hex(want2)))
        path = "00438860" if f1 >= 0x80 else ("00437130" if f1 & 8 else "inline")
        paths.setdefault(path, []).append(m)
    R.check("A2 00449AB0, all 256 values of definition +0x590: +0x1F1 = (+0x4A >> 2 & 7) | (bit 0 OR bit 5) << 3 | "
            "bit 1 << 4 | bit 2 << 5 | bit 3 << 6 | bit 5 << 7, and +0x1F2 = +0x590 >> 6 (from a zeroed block)",
            not bad, str(bad[:4]))
    R.note("so 004355D0 takes 00438860 when +0x590 bit 5 is set, else 00437130 when bit 0 is set, else its inline "
           "path (of the 256 values: %s)" % {k: len(v) for k, v in sorted(paths.items())})
    for w in (0x4453D0, 0x447020, 0x447ED0):
        Ew = make_walk_emu(img, w)
        res = {}
        for bit in (0, 1):
            setup_walk(Ew, w, (5, 0, 0, 0), pathbyte=bit | 0xFE, flag4a=0x14)
            ok = Ew.call(w, INST)
            res[bit] = (ok, [("%08X" % c[0], c[2][0x1F1]) for c in Ew.captured], Ew.fault)
        good = (res[0][0] and res[1][0] and len(res[0][1]) == 1 and len(res[1][1]) == 1
                and res[0][1][0][0] == "004434D0" and res[1][1][0][0] == "00444340"
                and not (res[0][1][0][1] & 8) and (res[1][1][0][1] & 8) and (res[0][1][0][1] & 7) == 5)
        R.check("A2 %08X: definition +0x%X bit 0 = 0 draws through 004434D0, = 1 through 00444340, and the same bit "
                "lands in +0x1F1 bit 3 (other bits of that byte 0xFE)" % (w, WALKS[w]["pathb"]), good, str(res))

    # -------------------------------------------------------------- A3
    print("\n== A3 the pass-mode switch of each draw path (mode 0..6 and 255 x axis 0/1 -> lighting routine)")
    for f, (n, preg, rreg, msite, asites, planar, uvsel) in PATHS.items():
        mp, arms, Bf = switch_map(img, f, n, msite, uvsel)
        same = all(mp[v] == EXPECT_MAP[v] for v in EXPECT_MAP)
        R.check("A3 %08X: modes 1/2/3/4 reach 395CF0|395780 / 3962F0 / 396A30|396560 / 396A30|396560 by +0x1B4 "
                "(0 and 0 -> y, else z), modes 0, 5, 6, 255 none - the same switch as 004355D0" % f, same,
                "" if same else str({v: {a: sorted(s) for a, s in d.items()} for v, d in mp.items()}))
        pl = [a for a, t in arm_calls(Bf, arms[2], uvsel) if t == 0x3962F0]
        R.check("A3 %08X: the planar call %08X is on the mode-2 arm only" % (f, planar),
                pl == [planar] and all(planar not in [a for a, t in arm_calls(Bf, arms[v], uvsel)]
                                       for v in (0, 1, 3, 4, 5)), str(["%08X" % x for x in pl]))
        for v in (1, 2, 3, 4):
            cs = [t for a, t in arm_calls(Bf, arms[v], uvsel)]
            R.note("%08X mode %d arm at %08X calls: %s; matrix globals read before its lighting call: %s" % (
                f, v, arms[v], " ".join("%08X" % t for t in cs), " ".join("%08X" % g for g in arm_globals(Bf, arms[v]))))

    # -------------------------------------------------------------- B
    print("\n== B the planar index k against the pass index p (inductive affine proof over each pass loop)")
    for f in PATHS:
        loop_check(img, f, R)

    # -------------------------------------------------------------- C1
    print("\n== C1 who reaches the draw paths, who writes byte param + 0x1B0")
    txt = [s for s in img.secs if s[0] == ".text"][0]
    _, va, vs, ra, rs = txt
    data, base = img.d[ra:ra + rs], img.base + va
    want = {0x4355D0, 0x437130, 0x438860, 0x4434D0, 0x444340}
    refs = {t: [] for t in want}
    for i in range(len(data) - 6):
        b0 = data[i]
        if b0 in (0xE8, 0xE9):
            t = base + i + 5 + struct.unpack_from("<i", data, i + 1)[0]
            if t in refs:
                refs[t].append(("E8" if b0 == 0xE8 else "E9", base + i))
        if b0 == 0x0F and 0x80 <= data[i + 1] <= 0x8F:
            t = base + i + 6 + struct.unpack_from("<i", data, i + 2)[0]
            if t in refs:
                refs[t].append(("0F8x", base + i))
    ptr = {t: [] for t in want}
    va8 = {t: 0 for t in want}
    for t in want:
        p8 = struct.pack("<Q", t)
        va8[t] = img.d.count(p8)
        pat = struct.pack("<I", t - img.base)
        j = img.d.find(pat)
        while j >= 0:
            b_, e_, u_ = struct.unpack_from("<III", img.d, j)
            # a RUNTIME_FUNCTION-shaped triple: .pdata itself, or the CHAININFO copy inside a chained unwind record
            ptr[t].append(b_ < e_ < b_ + 0x10000 and 0x7A2000 <= u_ < 0x1CD0000)
            j = img.d.find(pat, j + 1)
    exp_refs = {0x4355D0: [0x44A15B], 0x437130: [0x435692], 0x438860: [0x435681],
                0x4434D0: [0x445AFF, 0x4477E0, 0x4487A8], 0x444340: [0x445AF8, 0x4477D9, 0x4487A1]}
    for t in sorted(want):
        sites = sorted(a for k, a in refs[t])
        R.check("C1 %08X: raw E8/E9/0F8x references are exactly %s" % (t, " ".join("%08X" % x for x in exp_refs[t])),
                sites == exp_refs[t], " ".join("%s@%08X" % x for x in refs[t]))
        R.check("C1 %08X: no 8-byte VA of the entry anywhere in the file, and each of its %d 4-byte RVA occurrences "
                "is a (begin, end, unwind) RUNTIME_FUNCTION triple (.pdata or a chained-unwind copy), not a pointer"
                % (t, len(ptr[t])), va8[t] == 0 and ptr[t] and all(ptr[t]), "va8 %d rva %s" % (va8[t], ptr[t]))
    # byte stores with displacement 0x1B0 (any base, with an index) in functions that load [01FD4A78]
    gl = []
    for i in range(len(data) - 4):
        if base + i + 4 + struct.unpack_from("<i", data, i)[0] == GPARAM:
            gl.append(base + i)
    frag = fragments(img)
    roots = {}
    for b_, e_, root in frag:
        roots.setdefault(root, []).append((b_, e_))
    owner = {}
    for root, fr in roots.items():
        for b_, e_ in fr:
            owner[b_] = root
    funcs = sorted(set(owner[img.pdata(a)[0]] for a in gl if img.pdata(a)))
    writers = []
    for fs in funcs:
        for b_, e_ in roots[fs]:
            Bf = Flow(img, b_, e_).B
            for a in Bf.order:
                for m in Bf[a].mems:
                    if m["write"] and m["disp"] == 0x1B0 and m["size"] == 1:
                        writers.append((fs, a))
    R.note("rip-relative references to 01FD4A78: %d, in %d functions (.pdata roots, all chained fragments decoded): %s"
           % (len(gl), len(funcs), " ".join("%08X" % f_ for f_ in funcs)))
    R.check("C1 among those functions, the byte stores at displacement 0x1B0 are the four walks' slot copies only",
            sorted(writers) == [(0x4453D0, 0x4458FB), (0x447020, 0x4475E9), (0x447ED0, 0x4485BB), (0x449AB0, 0x449D08)],
            " ".join("%08X@%08X" % w for w in writers))

    # -------------------------------------------------------------- C2
    print("\n== C2 executed: the four walks fill the pass bytes from the definition's slots")
    for w in WALKS:
        run_walk_matrix(img, w, R)
    R.note("stubbed callees (a disclosed return each: 004309C0 -> its own definition offset as a float, 0042FDB0 -> a "
           "marker, 00431830 -> a texture or 0, 0020E600 -> a record, every other call rax 0 / xmm0 0.5; the draw "
           "callees capture the block)")

    # -------------------------------------------------------------- C3
    print("\n== C3 executed: the element setups leave each slot's byte +0, +7 and +0xB as loaded")
    run_setups(img, R)


    # -------------------------------------------------------------- K controls
    print("\n== K controls on patched copies (each check must now FAIL)")

    def ctl(label, va, old, new, fn):
        cur = img.read(va, len(old))
        R.check("K precondition %08X holds %s" % (va, old.hex()), cur == old, cur.hex())
        P = img.patched(va, new)
        RR = Report(label)
        RR.quiet = True
        names = []
        orig = RR.check

        def rec(name, cond, detail=""):
            if not cond:
                names.append(name.split(":")[-1].strip()[:70])
            return orig(name, cond, detail)
        RR.check = rec
        try:
            fn(P, RR)
            failed = RR.fails > 0
        except Exception as e:  # noqa: BLE001
            failed = True
            names.append("exception %s" % e)
        R.check("K %s -> the check fails" % label, failed, "; ".join(names[:3]))

    ctl("004355D0 `inc ecx` at 00436C91 -> `dec ecx` (k counts down while p counts up)", 0x436C91,
        b"\xff\xc1", b"\xff\xc9", lambda P, RR: loop_check(P, 0x4355D0, RR, quiet=True))
    ctl("00437130 `inc rdi` at 004387F0 -> `dec rdi` (the mode index stops being p)", 0x4387F0,
        b"\x48\xff\xc7", b"\x48\xff\xcf", lambda P, RR: loop_check(P, 0x437130, RR, quiet=True))
    ctl("004434D0 `add rax, 0x76` at 004439A6 -> `add rax, 0x77` (planar slot one dword off)", 0x4439A6,
        b"\x48\x83\xc0\x76", b"\x48\x83\xc0\x77", lambda P, RR: loop_check(P, 0x4434D0, RR, quiet=True))

    def a3(P, RR):
        n, preg, rreg, msite, asites, planar, uvsel = PATHS[0x4355D0]
        mp, arms, Bf = switch_map(P, 0x4355D0, n, msite, uvsel)
        RR.check("map", all(mp[v] == EXPECT_MAP[v] for v in EXPECT_MAP))
    ctl("004355D0 `jne` at 00435A7E -> `je` (axis sense of modes 3/4 swapped)", 0x435A7E, b"\x75", b"\x74", a3)

    def c2(P, RR):
        run_walk_matrix(P, 0x449AB0, RR, values=(0, 5), quiet=True)
    ctl("00449AB0 `movzx eax, byte ptr [r13 + 7]` at 00449D03 -> `[r13 + 8]`", 0x449D03,
        b"\x41\x0f\xb6\x45\x07", b"\x41\x0f\xb6\x45\x08", c2)

    def c2b(P, RR):
        run_walk_matrix(P, 0x4453D0, RR, values=(0, 5), quiet=True)
    ctl("004453D0 `inc r15` at 00445A54 -> `nop` x3 (p no longer advances)", 0x445A54,
        b"\x49\xff\xc7", b"\x90\x90\x90", c2b)

    ctl("00431770 `mov byte ptr [rdi + 0xa9], 0` at 00431800 -> `[rdi + 0xa7]` (the setup now clears the mode byte "
        "when +0xAA & 0x30 is 0)", 0x431800, b"\xc6\x87\xa9\x00\x00\x00\x00", b"\xc6\x87\xa7\x00\x00\x00\x00",
        lambda P, RR: run_setups(P, RR, only=(0x538DB0,)))

    print("\nFAILS %d" % R.fails)
    return R.fails


if __name__ == "__main__":
    sys.exit(1 if main(Img.load()) else 0)
