"""rv_qbound.py - FABLE independent re-derivation for ASTRA packet ov42-caller-quotient-bound (c51d5af60, OV-42).

Own reader (rvlib.py: struct + capstone 5, copied unchanged from the kind-row review, sha256 69f9bc40be32abcc...).
Does not import or run ASTRA's prove.py, prove_owner_reload_order.py, run.py, control.py, validation scripts or the
shared role adapter.

Method:
  * image sha256; manifest + every member; the retained copies equal their committed sources (git show);
  * the caller 00304850: .pdata extent, exact linear decode, the latch of WORD unit +0x714 into R13 at entry, the
    unsigned 542 guard on the latched register, the R13 writers, the row construction (second lookup's RAX, the
    descriptor's WORD stride, a 32-bit `imul`, a 32-bit `add r15d`), every R15 writer in the body, the three loads
    of the descriptor cell, the queue call and its RDX; the guard dominates the queue call over the CFG including
    the switch's jump-table edges;
  * the queue routine's kind-4 arm (already reviewed by FABLE in ov42-sequence-queue-source): its instruction text
    re-asserted at the bytes;
  * unicorn emulation of the ORIGINAL caller construction (00304910 .. 00304937, the lookup call stubbed) feeding the
    ORIGINAL queue arm (00306760 + 0x138 .. + 0x174, the lookup call stubbed): every i in 0..542 at chosen strides
    and bases, random cases, the packet's boundary cases and its three supplied-state countermodels;
  * the integer invariant checked arithmetically over all 543 ids x 65,535 strides (maximum product);
  * controls patch a private in-memory copy of the image; the exe on disk is never written; sha256 rechecked.
"""
import hashlib
import json
import os
import random
import struct
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from rvlib import Img, Body, Report, expect, run_control, check_manifest, find_exe, SHA256, fam  # noqa: E402

SLUG = "ov42-caller-quotient-bound"
COMMIT = "c51d5af60fe0241a7ce427df5454b3d4ae60997b"
CALLER, CALLER_END = 0x304850, 0x305042
Q = 0x306760
DESC = 0x2EBF138
LOOKUP = 0x20E600


def git(*a):
    return subprocess.run(["git"] + list(a), capture_output=True, cwd=os.path.dirname(find_exe())).stdout


def rip_target(I):
    for m in I.mems:
        if m["base"] == "rip":
            return I.address + I.size + m["disp"]
    return None


def switch_edges(img, B):
    """Extra CFG edges for `jmp rcx` switches of the form lea rdx,[image base]; mov ecx,[rdx+rax*4+T]; add rcx,rdx."""
    edges = {}
    for a in B.order:
        I = B[a]
        if I.mnemonic == "jmp" and I.direct_target() is None and I.op_str in ("rcx", "rax", "rdx"):
            k = B.order.index(a)
            ld, lea = B[B.order[k - 2]], None
            for j in range(k - 1, max(0, k - 8), -1):
                if B[B.order[j]].mnemonic == "lea" and B[B.order[j]].mems and B[B.order[j]].mems[0]["base"] == "rip":
                    lea = B[B.order[j]]
                    break
            bnd = None
            for j in range(k - 1, max(0, k - 10), -1):
                J = B[B.order[j]]
                if J.mnemonic == "cmp" and J.imm:
                    bnd = J.imm[0]
                    break
            if lea is None or bnd is None or not ld.mems:
                continue
            base = rip_target(lea)
            tab = base + ld.mems[0]["disp"]
            edges[a] = [base + img.u32(tab + 4 * i) for i in range(bnd + 1)]
    return edges


def reaching(B, edges, regfam, use):
    """Definitions of regfam (instructions writing it) that reach `use` along some CFG path with no other write."""
    W = [a for a in B.order if regfam in B[a].reg_writes]
    out = []
    for w in W:
        seen, st = set(), list(B.succ(w) + edges.get(w, []))
        while st:
            a = st.pop()
            if a in seen or a not in B.ins:
                continue
            seen.add(a)
            if a == use:
                out.append(w)
                break
            if a in W:
                continue
            st.extend(B.succ(a) + edges.get(a, []))
    return out


def reach(B, edges, frm, avoid=()):
    seen, st = set(), [frm]
    while st:
        a = st.pop()
        if a in seen or a in avoid or a not in B.ins:
            continue
        seen.add(a)
        st.extend(B.succ(a) + edges.get(a, []))
    return seen


# ---------------------------------------------------------------- emulation of the original bytes
class Emu(object):
    TEXT_LO, TEXT_HI = 0x300000, 0x310000

    def __init__(self, img):
        from unicorn import Uc, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE
        from unicorn.x86_const import UC_X86_REG_RAX
        self.img = img
        u = Uc(UC_ARCH_X86, UC_MODE_64)
        u.mem_map(self.TEXT_LO, self.TEXT_HI - self.TEXT_LO)
        u.mem_write(self.TEXT_LO, img.read(self.TEXT_LO, self.TEXT_HI - self.TEXT_LO))
        u.mem_map(0x20E000, 0x1000)
        u.mem_write(LOOKUP, b"\xC3")                       # stub: ret (RAX scripted by the hook)
        u.mem_map(DESC & ~0xFFF, 0x1000)                    # descriptor cell page
        u.mem_map(0x7000000, 0x10000)                       # fake descriptor, unit
        u.mem_map(0x8000000, 0x100000)                      # stack
        self.u = u
        self.RAX = UC_X86_REG_RAX
        self.lookup_rax = 0
        u.hook_add(UC_HOOK_CODE, self._hook, begin=LOOKUP, end=LOOKUP)

    def _hook(self, uc, addr, size, ud):
        uc.reg_write(self.RAX, self.lookup_rax)

    def desc(self, stride, key=0x1D74):
        u = self.u
        u.mem_write(DESC, struct.pack("<Q", 0x7000000))
        u.mem_write(0x7000000 + 8, struct.pack("<H", stride & 0xFFFF))
        u.mem_write(0x7000000 + 0xC, struct.pack("<I", key))

    def run(self, start, until, regs):
        from unicorn.x86_const import (UC_X86_REG_RSP, UC_X86_REG_R13, UC_X86_REG_R15, UC_X86_REG_RDI,
                                       UC_X86_REG_RBX, UC_X86_REG_RCX, UC_X86_REG_RDX)
        names = {"r13": UC_X86_REG_R13, "r15": UC_X86_REG_R15, "rdi": UC_X86_REG_RDI, "rbx": UC_X86_REG_RBX,
                 "rcx": UC_X86_REG_RCX, "rdx": UC_X86_REG_RDX}
        u = self.u
        u.reg_write(UC_X86_REG_RSP, 0x8080000)
        for k, v in regs.items():
            u.reg_write(names[k], v)
        u.emu_start(start, until, count=200)
        return {k: u.reg_read(names[k]) for k in ("r15", "rdi")}, u.reg_read(self.RAX)

    def row(self, i, base, stride):
        """Original caller construction 00304910 .. 00304937 (second lookup call stubbed to `base`)."""
        self.desc(stride)
        self.lookup_rax = base
        regs, _ = self.run(0x304910, 0x304937, {"r13": i, "r15": 0xDEADBEEFDEADBEEF})
        return regs["r15"]

    def queue(self, row, base, stride):
        """Original kind-4 arm 00306760 + 0x138 .. the store + 0x174 (lookup stubbed to `base`); returns EAX."""
        self.desc(stride)
        self.lookup_rax = base
        self.u.mem_write(0x7001000 + 8, struct.pack("<I", 0x1234))
        _, rax = self.run(Q + 0x138, Q + 0x174, {"rdi": row, "rbx": 0x7001000})
        return rax & 0xFFFFFFFF


def model(i, bc, sc, bq, sq):
    r = (bc + i * sc) & 0xFFFFFFFF
    d = (r - (bq & 0xFFFFFFFF)) & 0xFFFFFFFF
    q = d // sq
    w = q & 0xFFFF
    return 0xFFFFFFFF if w == 0xFFFF else (w - 0xD0) & 0xFFFFFFFF


# ---------------------------------------------------------------- checks
def caller_checks(img, R):
    pd = img.pdata(CALLER)
    ents, ok = img.pdata_cover(CALLER, CALLER + 0x828)
    tail = img.read(CALLER_END, CALLER + 0x828 - CALLER_END)
    B0 = Body(img, CALLER, CALLER_END)
    sw = list(switch_edges(img, B0).values())
    tab = [img.base + struct.unpack_from("<I", tail, 2 + 4 * k)[0] for k in range(13)]
    R.check("00304850's .pdata chain: %d records tile 00304850 .. + 0x828, all chained to the root; the code ends at the"
            " one `ret` (+ 0x7F1); the %d bytes after it are a 2-byte NOP and the switch's 13 DWORD offsets (+ 0x7F4),"
            " each resolving to a switch target" % (len(ents), len(tail)),
            ok and tail[:2] == b"\x66\x90" and len(tail) == 2 + 52 and sw and tab == sw[0],
            str([(hex(a), hex(b)) for a, b, f, r in ents]))
    B = Body(img, CALLER, CALLER_END)
    R.check("the caller decodes linearly and exactly to + 0x7F2 (%d instructions)" % len(B.order), B.exact)
    expect(R, B, 0x30487F, "lea rsi, [rcx + 0x6b0]")
    expect(R, B, 0x30488D, "movzx r13d, word ptr [rsi + 0x64]",
           "the latch: + 0x3D `movzx r13d, word ptr [rsi + 0x64]` = zero-extended WORD unit +0x714 (RSI = RCX + 0x6B0)")
    early = [a for a in B.order if a < 0x30488D and ("rcx" in B[a].reg_writes or "rsi" in B[a].reg_writes)]
    R.check("no RCX write before + 0x2F and RSI written only by the + 0x2F `lea` before the latch",
            [a for a in early if a != 0x30487F] == [], str([hex(a) for a in early]))
    E0 = switch_edges(img, B)
    for use, name in ((0x3048DE, "the guard + 0x8E"), (0x30492D, "the row's `movzx eax, r13w` + 0xDD")):
        rd = reaching(B, E0, "r13", use)
        R.check("the only R13 definition reaching %s is the latch + 0x3D" % name, rd == [0x30488D],
                str([hex(a) for a in rd]))
    expect(R, B, 0x3048A8, "mov ebx, 0x21e")
    expect(R, B, 0x3048DE, "cmp r13w, bx", "the guard: + 0x8E `cmp r13w, bx` on the LATCHED register (EBX = 0x21E = 542)")
    I = B[0x3048E2]
    R.check("+ 0x92 `ja` (unsigned) to + 0x7C7, the rejecting exit", I.mnemonic == "ja" and I.direct_target() == 0x305017,
            I.text)
    wbx = [a for a in B.order if 0x3048A8 < a < 0x3048DE and "rbx" in B[a].reg_writes]
    R.check("EBX is not written between + 0x58 and the guard (the one call between, + 0x7C, preserves RBX under Win64)",
            not wbx, str([hex(a) for a in wbx]))
    # row construction
    for a, t in ((0x30491A, "call 0x20e600"), (0x30491F, "mov r15, rax"), (0x304929, "movzx ecx, word ptr [rax + 8]"),
                 (0x30492D, "movzx eax, r13w"), (0x304931, "imul ecx, eax"), (0x304934, "add r15d, ecx"),
                 (0x304939, "mov r15, r14")):
        expect(R, B, a, t)
    loads = [a for a in B.order if rip_target(B[a]) == DESC]
    R.check("before the switch the caller loads the descriptor cell 02EBF138 three times: + 0x98 (the null test "
            "before the first lookup), + 0xC0 (the second lookup's key) and + 0xD2 (the stride)",
            [a for a in loads if a < 0x30495A] == [0x3048E8, 0x304910, 0x304922], str([hex(a) for a in loads]))
    rd15 = reaching(B, E0, "r15", 0x304F47)
    R.check("the R15 definitions reaching the queue call's `mov rdx, r15` are exactly + 0xE4 (`add r15d, ecx`) and "
            "+ 0xE9 (`mov r15, r14`); the five other R15 writes restore the saved R15 on exit paths",
            sorted(rd15) == [0x304934, 0x304939], str([hex(a) for a in rd15]))
    rest = [a for a in B.order if "r15" in B[a].reg_writes and a not in (0x30491F, 0x304934, 0x304939)]
    R.check("each of those other writes is `mov r15, qword ptr [rsp + 0x108]` (the restore of the + 0xA6 save)",
            rest and all(B[a].text == "mov r15, qword ptr [rsp + 0x108]" for a in rest), str([hex(a) for a in rest]))
    rd14 = reaching(B, E0, "r14", 0x304939)
    R.check("the only R14 definition reaching the null row + 0xE9 is + 0x2C `xor r14d, r14d`, so that row is 0",
            rd14 == [0x30487C], str([hex(a) for a in rd14]))
    expect(R, B, 0x304F47, "mov rdx, r15")
    expect(R, B, 0x304F4D, "call 0x306760", "the queue call + 0x6FD `call 00306760` with RDX = R15 (+ 0x6F7)")
    E = switch_edges(img, B)
    R.check("one jump-table switch in the body (+ 0x10A, 13 targets), its edges added to the CFG",
            len(E) == 1 and len(list(E.values())[0]) == 13, str({hex(k): len(v) for k, v in E.items()}))
    rs = reach(B, E, CALLER)
    R.check("the queue call is reachable from the entry over that CFG", 0x304F4D in rs)
    R.check("the 542 guard dominates the queue call (unreachable when + 0x8E is removed)",
            0x304F4D not in reach(B, E, CALLER, avoid=[0x3048DE]))
    R.check("the row construction (+ 0xE4) or the null row (+ 0xE9) dominates the queue call",
            0x304F4D not in reach(B, E, CALLER, avoid=[0x304934, 0x304939]))
    # the two routes into the call
    expect(R, B, 0x304F05, "sub r13w, ax")
    expect(R, B, 0x304F09, "cmp r13w, 0x21")
    expect(R, B, 0x304F3D, "test dword ptr [r15 + 0xc], 0x40000000")
    R.check("ids 208..241 jump past 00303830 / 00305640 to + 0x6ED; other ids reach the queue call only through both, "
            "and both routes test bit 30 of DWORD [r15 + 0xC] (+ 0x6D2, + 0x6ED)",
            B[0x304F0E].mnemonic == "jbe" and B[0x304F0E].direct_target() == 0x304F3D
            and B[0x304F1D].direct_target() == 0x303830 and B[0x304F38].direct_target() == 0x305640
            and B[0x304F22].text == "test dword ptr [r15 + 0xc], 0x40000000")
    R.check("the bit-30 test + 0x6ED dominates the queue call (a null row reads address 0xC before any call)",
            0x304F4D not in reach(B, E, CALLER, avoid=[0x304F3D]))
    return B


def queue_checks(img, R):
    B = Body(img, Q, Q + 0x38F)
    R.check("queue routine 00306760 decodes exactly to + 0x38F", B.exact)
    for off, t in ((0x138, None), (0x142, "call 0x20e600"), (0x147, "sub edi, eax"), (0x149, "xor edx, edx"),
                   (0x152, "movzx ecx, word ptr [rax + 8]"), (0x156, "mov eax, edi"), (0x158, "div ecx"),
                   (0x162, "cmp ax, dx"), (0x167, "movzx eax, ax"), (0x16A, "sub eax, 0xd0")):
        if t:
            expect(R, B, Q + off, t, "queue + 0x%X `%s`" % (off, t))
    R.check("queue + 0x138 and + 0x14B both load 02EBF138", rip_target(B[Q + 0x138]) == DESC and
            rip_target(B[Q + 0x14B]) == DESC)
    I = B[Q + 0x174]
    R.check("queue + 0x174 stores EAX as a DWORD to 022C2178", I.mnemonic == "mov" and rip_target(I) == 0x22C2178
            and I.mems[0]["size"] == 4, I.text)


def emu_checks(img, R, small=False):
    E = Emu(img)
    rnd = random.Random(1002)
    strides = [1, 2, 60, 0x3C, 0x100, 0x7FFF, 0x8000, 0xFFFE, 0xFFFF] if not small else [60, 0xFFFF]
    bases = [0x100000, 0xFFFFFFF0, 0xFFFFFFFF, 0x12345678, 0x7FFFFFFF00001000] if not small else [0xFFFFFFF0]
    ids = range(0, 543) if not small else (0, 207, 208, 225, 542)
    bad = []
    n = 0
    for s in strides:
        for b in bases:
            for i in ids:
                row = E.row(i, b, s)
                if row != ((b + i * s) & 0xFFFFFFFF):
                    bad.append(("row", i, s, hex(b), hex(row)))
                    continue
                out = E.queue(row, b, s)
                n += 1
                want = (i - 0xD0) & 0xFFFFFFFF
                if out != want:
                    bad.append(("queue", i, s, hex(b), hex(out)))
    R.check("emulated original construction -> original queue arm, equal base and stride, %d cases (every id 0..542 x "
            "%d strides x %d bases): the row is zero-extended low32(base + i*stride) and the stored DWORD is i - 0xD0"
            % (n, len(strides), len(bases)), not bad, str(bad[:4]))
    outs = set()
    for _ in range(40 if small else 400):
        i, s, b = rnd.randrange(543), rnd.randrange(1, 0x10000), rnd.getrandbits(64)
        o = E.queue(E.row(i, b, s), b, s)
        outs.add(o)
        if o != (i - 0xD0) & 0xFFFFFFFF:
            bad.append(("rand", i, s, hex(b), hex(o)))
    R.check("emulated random ids / strides / 64-bit bases: stored DWORD = i - 0xD0 in every case", not bad, str(bad[:4]))
    allv = [E.queue(E.row(i, 0x100000, 60), 0x100000, 60) for i in range(543)]
    dom = sorted(set(allv))
    R.check("domain of the stored DWORD over ids 0..542: 0..334 and FFFFFF30..FFFFFFFF; none of 511..534",
            dom == sorted(set(list(range(0, 335)) + list(range(0xFFFFFF30, 0x100000000)))) and
            not any(511 <= v <= 534 for v in dom), "%d values" % len(dom))
    R.check("id 207 stores FFFFFFFF by subtraction (the FFFF sentinel compare is not taken: q = 207)",
            allv[207] == 0xFFFFFFFF)
    cm = [(208, 0x100000, 60, 0xF883C, 60, 511), (360, 0x100000, 60, 0x100000, 30, 512),
          (720, 0x100000, 60, 0x100000, 60, 512)]
    got = [E.queue(E.row(i, bc, sc), bq, sq) for i, bc, sc, bq, sq, _ in cm]
    R.check("the packet's three supplied-state countermodels, run through the original bytes: base changed -> 511, "
            "stride halved -> 512, id 720 (guard bypassed) -> 512", got == [x[5] for x in cm], str(got))
    bd = [(0xFFFFFFF0, 542, 65535, 0x14E), (0xFFFFFFFF, 208, 60, 0), (0x100000, 0, 1, 0xFFFFFF30),
          (0x100000, 207, 65535, 0xFFFFFFFF)]
    got2 = [E.queue(E.row(i, b, s), b, s) for b, i, s, _ in bd]
    R.check("the packet's four boundary checks reproduce through the original bytes", got2 == [x[3] for x in bd],
            str([hex(x) for x in got2]))


def arithmetic_checks(R):
    mx = 542 * 65535
    R.check("max i*S over ids 0..542 and strides 1..65535 = %d < 2^32, so low32(B + i*S) - low32(B) = i*S exactly and"
            " q = i for every equal-base, equal-stride pair" % mx, mx == 35519970 and mx < 2 ** 32)
    # exhaustive over the 543 x 65535 grid is the inequality above; spot the model against it
    ok = all(model(i, b, s, b, s) == (i - 0xD0) & 0xFFFFFFFF
             for i in (0, 207, 208, 334 + 208, 542) for s in (1, 65535) for b in (0, 0xFFFFFFFF, 0xFFFF0000))
    R.check("the integer model agrees at the grid's corners", ok)


def checks(img, R, small=False):
    caller_checks(img, R)
    queue_checks(img, R)
    emu_checks(img, R, small)


def main():
    exe = find_exe()
    raw = open(exe, "rb").read()
    R = Report("rv_qbound")
    R.check("exe sha256 = %s..." % SHA256[:16], hashlib.sha256(raw).hexdigest() == SHA256)
    committed = hashlib.sha256(git("show", COMMIT + ":Database/FFXII TZA/_experiments/evidence/%s/manifest.json"
                                   % SLUG)).hexdigest()
    check_manifest(R, SLUG, committed)
    ev = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(exe)))),
                      "FFXII TZA", "_experiments", "evidence", SLUG)
    lin = json.load(open(os.path.join(ev, "result-02.json"), encoding="utf-8"))["retained_lineage"]
    badl = []
    for L in lin:
        src = git("show", "%s:%s" % (L["commit"], L["member"]))
        mine = open(os.path.join(ev, L["copy"]), "rb").read()
        if not src or src != mine or hashlib.sha256(mine).hexdigest() != L["sha256"]:
            badl.append(L["copy"])
    R.check("the %d retained copies are byte-identical to their committed sources" % len(lin), not badl, str(badl))
    img = Img(raw)
    checks(img, R)
    arithmetic_checks(R)
    print("== controls (each patched private image must FAIL at least one check)")
    ctl = [
        ("null control: an unchanged private copy passes", lambda: Img(raw), False),
        ("+ 0x92 `ja` -> `jg` (signed guard)", lambda: img.patched(0x3048E2, b"\x0F\x8F"), True),
        ("+ 0x3D latch WORD -> BYTE (`movzx r13d, byte ptr [rsi + 0x64]`)",
         lambda: img.patched(0x30488D, b"\x44\x0F\xB6\x6E\x64"), True),
        ("+ 0xE4 `add r15d, ecx` -> `add r15, rcx` (64-bit row)", lambda: img.patched(0x304934, b"\x49\x01\xCF"), True),
        ("+ 0xD9 stride WORD -> BYTE (`movzx ecx, byte ptr [rax + 8]`)", lambda: img.patched(0x304929, b"\x0F\xB6\x48\x08"),
         True),
        ("+ 0xE1 `imul ecx, eax` -> `add ecx, eax`", lambda: img.patched(0x304931, b"\x01\xC1\x90"), True),
        ("+ 0x6F7 `mov rdx, r15` -> `mov rdx, r14`", lambda: img.patched(0x304F47, b"\x4C\x89\xF2"), True),
        ("queue + 0x16A `sub eax, 0xd0` -> `sub eax, 0xd1`", lambda: img.patched(Q + 0x16A, b"\x2D\xD1\x00\x00\x00"), True),
        ("queue + 0x158 `div ecx` -> `idiv ecx`", lambda: img.patched(Q + 0x158, b"\xF7\xF9"), True),
    ]
    for label, fac, must in ctl:
        ok = run_control(label, fac, lambda im, RR: checks(im, RR, small=True), must_fail=must)
        R.check("control: " + label, ok)
    R.check("exe on disk unchanged after the controls", hashlib.sha256(open(exe, "rb").read()).hexdigest() == SHA256)
    print("FAILS %d" % R.fails)


if __name__ == "__main__":
    main()
