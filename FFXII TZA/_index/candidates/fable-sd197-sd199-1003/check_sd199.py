"""check_sd199.py - FABLE verification record, 2026-10-03.

Re-derives from the shipping image every difference the cloud draft for SD-199 claims between 00437130 (F, `+0x1F1`
bit 3 set) and the inline path of 004355D0 (I, bit clear), and between 00444340 (G1, bit set) and 004434D0 (G0,
bit clear); bounds the inline path itself; tests the draft's "everything else is identical" claim by three
whole-body censuses; and adds what the draft did not compare: the same bit also picks the vertex transform in the
shared prep (00434CD0 / 00435050) and in the three grid walks.

Sections
  A0  the inline path's bounds (CFG reachability on the decoded body)
  A1  difference A-1: F's zero-first-qword corner skip (absent from I)
  A2  difference A-2: I's 1/1.15, x1.15 rescale of the pass pair param+0x50+8p (absent from F); 0053DD10 read whole;
      the pair's consumer 0039B880 executed under Unicorn (the pair is an additive UV offset of the emitted S,T)
  A3  "everything else": callee multisets, rip-relative globals, non-stack displacement/width sets
  B   the grid pair: B-1 (G1's zero-first-qword quad skip) and the same three censuses
  T   NOT in the draft: +0x1F1 bit 3 / definition bit 0 also selects 0039A150 (no reject) vs 00399B80 (whole-object
      reject) before every one of these draws
  P   shipped population for A-2 (from fable-k54-residue-1003/k54_modes.tsv)
  C   controls: fabricated differences that MUST fail

Run: python check_sd199.py > check_sd199.out   (exit 1 when any non-control check fails)
"""
import collections
import csv
import os
import struct
import sys

RV = r"C:\Users\Kristian\source\repos\XIIOnline\Database\FFXII TZA\_index\candidates\fable-review-astra-ov42-caller-quotient-bound-1002"
sys.path.insert(0, RV)
from rvlib import Img, Report, Body, expect  # noqa: E402
from unicorn import Uc, UC_ARCH_X86, UC_MODE_64, UC_HOOK_MEM_UNMAPPED  # noqa: E402
from unicorn.x86_const import (UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_RSP, UC_X86_REG_R8, UC_X86_REG_R9,  # noqa
                               UC_X86_REG_RIP)

HERE = os.path.dirname(os.path.abspath(__file__))
K54 = os.path.join(HERE, "..", "fable-k54-residue-1003", "k54_modes.tsv")

D = 0x4355D0
I0, I1 = 0x435699, 0x436D00          # inline path [start, end) - established in A0
F0, F1 = 0x437130, 0x437130 + 5930
G0s, G0e = 0x4434D0, 0x4434D0 + 3681
G1s, G1e = 0x444340, 0x444340 + 3979
EMIT = {0x39E820, 0x39EC30, 0x39E6B0, 0x39EA70, 0x39B840, 0x39B860, 0x39F4B0, 0x39F9F0, 0x39F2B0, 0x39F780}


def calls_in(B, s, e):
    return [(a, B[a].direct_target()) for a in B.order if s <= a < e and B[a].mnemonic == "call"]


def zero_tests(B, s, e):
    """Corner tests: `cmp qword ptr [..], 0` and `movq rax, xmm*` + `test rax, rax`, each followed by `je`."""
    out = []
    for k, a in enumerate(B.order):
        if not (s <= a < e):
            continue
        I = B[a]
        hit = (I.mnemonic == "cmp" and I.op_str.startswith("qword ptr [") and I.op_str.endswith(", 0")) or (
            I.text == "test rax, rax" and k and B[B.order[k - 1]].mnemonic == "movq"
            and B[B.order[k - 1]].op_str.startswith("rax, xmm")) or (
            I.text == "test rax, rax" and k > 1 and B[B.order[k - 2]].mnemonic == "movq"
            and B[B.order[k - 2]].op_str.startswith("rax, xmm"))
        if not hit:
            continue
        j = next(B[x] for x in B.order[k + 1:k + 4] if B[x].mnemonic.startswith("j"))
        out.append((a, j.mnemonic, j.direct_target()))
    return out


def groups(tests):
    """Consecutive tests sharing one je target = one primitive's corner group."""
    G = collections.OrderedDict()
    for a, m, t in tests:
        G.setdefault(t, []).append((a, m))
    return G


def censuses(img, s, e):
    B = Body(img, s, e)
    callee = collections.Counter(B[a].direct_target() for a in B.order if B[a].mnemonic == "call")
    rip = collections.Counter()
    disp = set()
    for a in B.order:
        I = B[a]
        if I.mnemonic == "nop" or I.mnemonic == "lea":
            continue
        for m in I.mems:
            if m["base"] == "rip":
                rip[a + I.size + m["disp"]] += 1
            elif m["base"] not in ("rsp", "rbp"):
                disp.add((m["disp"], m["scale"] if m["index"] else 0, m["size"]))
    return B, callee, rip, disp


# ================================================================================================ A0
def a0(img, R, BD):
    R.note("-- A0: where the inline path starts and ends")
    for a, t in [(0x43566F, "movzx eax, byte ptr [r15 + 0x1f1]"), (0x435677, "cmp al, 0x80"),
                 (0x435681, "call 0x438860"), (0x435686, "jmp 0x435641"), (0x435688, "test al, 8"),
                 (0x43568A, "je 0x435699"), (0x435692, "call 0x437130"), (0x435697, "jmp 0x435641"),
                 (0x436CFB, "jmp 0x435641"), (0x435641, "mov rcx, qword ptr [rbp + 0xc0]"), (0x43565B, "ret")]:
        expect(R, BD, a, t)
    R.check("A0a 004355D0 decodes exactly over 5,936 bytes", BD.exact)
    reach = BD.reach(I0, avoid=[0x435641])
    R.check("A0b everything reachable from 00435699 (stopping at the shared epilogue 00435641) lies in "
            "[00435699, 00436CFB]", min(reach) == I0 and max(reach) == 0x436CFB, "%X..%X" % (min(reach), max(reach)))
    into = [(a, BD[a].direct_target()) for a in BD.order if not (I0 <= a < I1) and BD[a].mnemonic.startswith("j")
            and BD[a].direct_target() is not None and I0 <= BD[a].direct_target() < I1]
    R.check("A0c the only branch into the range from outside it is 0043568A `je 0x435699`", into == [(0x43568A, I0)],
            str(into))
    pre = BD.reach(D, avoid=[I0])
    R.check("A0d without passing 00435699 no inline instruction is reachable (the range is entered only there)",
            not any(I0 <= a < I1 for a in pre))
    R.check("A0e the range has no other exit than the jmp to the shared epilogue (no ret, no other out-branch)",
            not [a for a in BD.order if I0 <= a < I1 and BD[a].mnemonic == "ret"] and
            [(a, BD[a].direct_target()) for a in BD.order if I0 <= a < I1 and BD[a].mnemonic.startswith("j")
             and BD[a].direct_target() is not None and not (I0 <= BD[a].direct_target() < I1)] == [(0x436CFB, 0x435641)])


# ================================================================================================ A1
def a1(img, R, BD, BF):
    R.note("-- A1: the zero-first-qword corner skip")
    tf = zero_tests(BF, F0, F1)
    ti = zero_tests(BD, I0, I1)
    gf = groups(tf)
    R.check("A1a 00437130 has 42 corner tests (`cmp qword ptr [rbp+0x60/0x70/0x80(/0x90)], 0`, each `je`) in 12 "
            "groups (6 triangle loops x 3 corners, 6 quad loops x 4)", len(tf) == 42 and len(gf) == 12 and
            sorted(len(v) for v in gf.values()) == [3] * 6 + [4] * 6 and all(m == "je" for _, m, _ in tf),
            "%d tests %d groups" % (len(tf), len(gf)))
    R.check("A1b the inline path has no such test (0 in 00435699..00436CFB)", not ti, str(ti[:3]))
    ok, det = True, []
    for T, L in gf.items():
        last = max(a for a, _ in L)
        span = calls_in(BF, last, T)
        em = [c for c in span if c[1] in EMIT]
        # from T to the loop's back edge: counters only, no emitter
        k = BF.order.index(T)
        tail = []
        for a in BF.order[k:k + 40]:
            I = BF[a]
            if I.mnemonic == "call":
                tail.append(I.direct_target())
            if I.mnemonic.startswith("j") and I.direct_target() is not None and I.direct_target() < a:
                break
        good = bool(em) and not (set(tail) & EMIT)
        ok &= good
        det.append("%X:%d->%X emit %s" % (min(a for a, _ in L), len(L), T, ",".join("%X" % c[1] for c in em)))
    R.check("A1c every group's je target lies past that primitive's emitter call(s) and before the loop's back "
            "edge, with no emitter between the target and the back edge (the skip lands on the counter block)",
            ok, "; ".join(det[:12]))
    F_CLAIM = [(0x79C, 0x39E820), (0x876, 0x39EC30), (0x91E, 0x39E6B0), (0x9F6, 0x39EA70),
               (0xB61, 0x39B840), (0xB99, 0x39F4B0), (0xD1F, 0x39B860), (0xD57, 0x39F9F0),
               (0xE91, 0x39B840), (0xEC9, 0x39F2B0), (0x104F, 0x39B860), (0x1087, 0x39F780),
               (0x11CA, 0x39B840), (0x11F3, 0x39F4B0), (0x1374, 0x39B860), (0x139D, 0x39F9F0),
               (0x14C7, 0x39B840), (0x14F0, 0x39F2B0), (0x1668, 0x39B860), (0x1691, 0x39F780)]
    skipped = set()
    for T, L in gf.items():
        for a, t in calls_in(BF, max(a for a, _ in L), T):
            skipped.add(a)
    bad = [("%X" % o, "%X" % c) for o, c in F_CLAIM if not (F0 + o in BF.ins and BF[F0 + o].mnemonic == "call" and
                                                           BF[F0 + o].direct_target() == c and F0 + o in skipped)]
    R.check("A1d the draft's 20 skippable F call sites are calls to the named emitters/builders, each inside a "
            "skipped span", not bad, str(bad))
    I_CLAIM = [(0x87B, 0x39E820), (0x93B, 0x39EC30), (0x9DB, 0x39E6B0), (0xA9B, 0x39EA70),
               (0xBCD, 0x39B840), (0xC12, 0x39F4B0), (0xD93, 0x39B860), (0xDD6, 0x39F9F0),
               (0xEDC, 0x39B840), (0xF21, 0x39F2B0), (0x10A3, 0x39B860), (0x10E6, 0x39F780),
               (0x1210, 0x39B840), (0x123C, 0x39F4B0), (0x139B, 0x39B860), (0x13C7, 0x39F9F0),
               (0x14CE, 0x39B840), (0x14FA, 0x39F2B0), (0x165B, 0x39B860), (0x1687, 0x39F780)]
    bad = [("%X" % o, "%X" % c) for o, c in I_CLAIM if not (D + o in BD.ins and BD[D + o].mnemonic == "call" and
                                                           BD[D + o].direct_target() == c)]
    em_i = [a for a, t in calls_in(BD, I0, I1) if t in EMIT]
    R.check("A1e the draft's 20 corresponding inline call sites are calls to the same callees, and they are all of "
            "the inline path's emitter/builder calls", not bad and sorted(em_i) == sorted(D + o for o, _ in I_CLAIM),
            "%s; inline emitter calls %d" % (bad, len(em_i)))
    for a, t in [(0x437B90, "movzx eax, byte ptr [r13]"), (0x437B95, "inc r13")]:
        expect(R, BF, a, t, "A1f value-1 stream: byte read at %08X before the first test of its loop (%s)" % (a, t))
    reads = [a for a in BF.order if F0 <= a < F1 and BF[a].text == "movzx eax, byte ptr [r13]"]
    firsts = sorted(min(a for a, _ in L) for L in gf.values())
    ok = len(reads) == 4 and all(any(r < f and not any(r < g < f for g in firsts if g != f) for f in firsts)
                                 for r in reads)
    R.check("A1g the four value-1 loops each consume their per-primitive byte (`movzx eax, byte ptr [r13]`, then "
            "`inc r13`) before their corner tests: %s" % ", ".join("%08X" % r for r in reads), ok)


# ================================================================================================ A2
def a2(img, R, BD, BF):
    R.note("-- A2: the 1.15 rescale of the pass pair, inline only")
    for a, t in [(0x43573D, "movss xmm6, dword ptr [rip + 0x8dcd37]"), (0x43574D, "movss xmm7, dword ptr [rip + 0x18b641b]"),
                 (0x435763, "lea r12, [rdi + 0xa]"), (0x43576F, "lea r12, [r15 + r12*8]"),
                 (0x435C8D, "movzx eax, byte ptr [r15 + 0x1f2]"), (0x435C95, "test al, 1"),
                 (0x435CC5, "mov dword ptr [r12], 0x3f000000"), (0x435CDB, "test al, 2"), (0x435CDD, "je 0x435d71"),
                 (0x435D23, "cmp byte ptr [r15 + rbx + 0x130], 4"), (0x435D2C, "jne 0x435d5a"),
                 (0x435D2E, "call 0x53dd10"), (0x435D33, "cmp eax, 1"), (0x435D36, "jne 0x435d5a"),
                 (0x435D45, "divss xmm0, xmm6"), (0x435D49, "mulss xmm1, xmm6"),
                 (0x435D4D, "movss dword ptr [r12], xmm0"), (0x435D53, "movss dword ptr [r12 + 4], xmm1"),
                 (0x435D67, "addss xmm0, xmm7"), (0x435D6B, "addss xmm1, xmm7"),
                 (0x435D71, "cmp byte ptr [r15 + rbx + 0x130], 4"), (0x435D7C, "call 0x53dd10"),
                 (0x435D81, "cmp eax, 1"), (0x435D93, "divss xmm0, xmm6"), (0x435D97, "mulss xmm1, xmm6"),
                 (0x435D9B, "movss dword ptr [r12 + 4], xmm1"), (0x435DA2, "movss dword ptr [r12], xmm0")]:
        expect(R, BD, a, t)
    R.check("A2a xmm6 = [00D1247C] = 1.15f (0x3F933333), xmm7 = [01CEBB70] = 0.5",
            0x435745 + 0x8DCD37 == 0xD1247C and img.read(0xD1247C, 4) == bytes.fromhex("3333933f") and
            0x435755 + 0x18B641B == 0x1CEBB70 and img.read(0x1CEBB70, 4) == struct.pack("<f", 0.5))
    w6 = [a for a in BD.order if 0x435745 <= a < 0x436CC0 and "xmm6" in BD[a].reg_writes]
    R.check("A2b xmm6 is not rewritten inside the pass loop (00435745..00436CC0)", not w6, str(["%X" % a for a in w6]))
    B5 = Body(img, 0x53DD10, 0x53DD16)
    expect(R, B5, 0x53DD10, "mov eax, 1", "A2c 0053DD10 is `mov eax, 1` / `ret` (6 bytes, read whole)")
    expect(R, B5, 0x53DD15, "ret")
    R.note("   => the `cmp eax, 1` / `jne` after each call never skips: whenever the pass's +0x130 byte is 4 and "
           "+0x1F2 bit 0 is clear, the pair is divided by 1.15 (lane 0) and multiplied by 1.15 (lane 1)")
    cF = [a for a in BF.order if BF[a].mnemonic == "call" and BF[a].direct_target() == 0x53DD10]
    rF = [a for a in BF.order for m in BF[a].mems if m["base"] == "rip" and a + BF[a].size + m["disp"] == 0xD1247C]
    R.check("A2d 00437130 never calls 0053DD10 and never reads 00D1247C", not cF and not rF)
    for a, t in [(0x4377B0, "test al, 2"), (0x4377B2, "je 0x437811"), (0x437800, "addss xmm0, xmm6"),
                 (0x437804, "addss xmm1, xmm6"), (0x437808, "movss dword ptr [rcx], xmm0"),
                 (0x4371F2, "movss xmm6, dword ptr [rip + 0x18b4976]")]:
        expect(R, BF, a, t)
    R.check("A2e F's xmm6 is 0.5 ([01CEBB70]); its bit-1 arm adds 0.5 with no rescale; with neither bit it does "
            "nothing (004377B2 -> 00437811)", 0x4371FA + 0x18B4976 == 0x1CEBB70)
    # the pair reaches the builders: r9 at each builder call
    def r9_before(B, a):
        k = B.order.index(a)
        for x in reversed(B.order[max(0, k - 14):k]):
            if "r9" in B[x].reg_writes:
                return B[x].text
        return None
    ib = [(D + o) for o in (0xBCD, 0xD93, 0xEDC, 0x10A3, 0x1210, 0x139B, 0x14CE, 0x165B)]
    fb = [(F0 + o) for o in (0xB61, 0xD1F, 0xE91, 0x104F, 0x11CA, 0x1374, 0x14C7, 0x1668)]
    ri = [r9_before(BD, a) for a in ib]
    rf = [r9_before(BF, a) for a in fb]
    R.check("A2f every builder call (0039B840/0039B860) gets r9 = the pass pair: `mov r9, r12` inline, "
            "`mov r9, qword ptr [rsp + 0x58]` in F", all(x == "mov r9, r12" for x in ri) and
            all(x == "mov r9, qword ptr [rsp + 0x58]" for x in rf), "%s | %s" % (ri, rf))
    for a, t in [(0x435DA8, "movzx eax, byte ptr [r15 + rbx + 0x130]"), (0x435DB1, "cmp al, 5"),
                 (0x435DB3, "jne 0x43608c")]:
        expect(R, BD, a, t)
    # 0039B880, executed: the pair is added to the UV before the multiply by the per-corner float
    for a, t, n in [(0x39B844, "mov qword ptr [rsp + 0x20], r9", 0x39B840), (0x39B864, "mov qword ptr [rsp + 0x20], r9",
                                                                            0x39B860),
                    (0x39B869, "mov r9d, 4", 0x39B860), (0x39B849, "mov r9d, 3", 0x39B840)]:
        expect(R, Body(img, n, n + 25), a, t)
    s, t = builder_exec(img)
    R.check("A2g 0039B860 executed: emitted (S, T) = ((u + pair.x) * q, (v + pair.y) * q) per corner, bit exact; "
            "changing the pair changes every corner", s, t)
    W = Body(img, 0x449C80, 0x44A180)
    for a, t in [(0x449C99, "lea rbx, [rdi + 0x50]"), (0x449FA0, "movss dword ptr [rbx], xmm0"),
                 (0x449FB6, "movss dword ptr [rbx + 4], xmm0"), (0x449FC4, "movss dword ptr [rbx], xmm1"),
                 (0x449FCC, "movss dword ptr [rbx + 4], xmm0"), (0x44A029, "add rbx, 8"),
                 (0x44A15B, "call 0x4355d0"), (0x449CE9, "mov byte ptr [r12 + rdi + 0x130], al"),
                 (0x449D30, "cmp ecx, 1")]:
        expect(R, W, a, t)
    R.note("   => the walk 00449AB0 rewrites param+0x50+8p from the slot's two tracks before its one draw call "
           "0044A15B, so the in-place rescale does not accumulate across frames; +0x130+p is slot byte +0 "
           "(00449CE9), and byte 4 takes the same texture-lookup arm as byte 2 (00449D30)")


def builder_exec(img):
    mu = Uc(UC_ARCH_X86, UC_MODE_64)
    pe = struct.unpack_from("<I", img.d, 0x3C)[0]
    size_img = (struct.unpack_from("<I", img.d, pe + 24 + 56)[0] + 0xFFF) & ~0xFFF
    mu.mem_map(0x120000, size_img)
    for name, va, vs, ra, rs in img.secs:
        mu.mem_write(0x120000 + va, img.d[ra:ra + min(rs, vs if vs else rs)])
    mu.mem_map(0x10000000, 0x10000)
    mu.mem_map(0x20000000, 0x10000)
    mu.mem_map(0x30000000, 0x1000)
    mu.mem_write(0x30000000, b"\xf4")
    import numpy as np
    f32 = np.float32
    UV, OUT, Q, PAIR = 0x10000000, 0x10001000, 0x10002000, 0x10003000
    uv = [(0.25, 0.75), (1.5, -0.5), (0.0, 1.0), (3.0, 2.0)]
    q = [1.0, 0.5, 2.0, 0.125]

    def run(pair):
        mu.mem_write(UV, b"".join(struct.pack("<ff", *p) for p in uv))
        mu.mem_write(Q, b"".join(struct.pack("<f", x) for x in q))
        mu.mem_write(PAIR, struct.pack("<ff", *pair))
        mu.mem_write(OUT, b"\0" * 64)
        rsp = 0x2000F000
        mu.mem_write(rsp, struct.pack("<Q", 0x30000000) + b"\0" * 0x40)
        mu.reg_write(UC_X86_REG_RSP, rsp)
        mu.reg_write(UC_X86_REG_RCX, UV)
        mu.reg_write(UC_X86_REG_RDX, OUT)
        mu.reg_write(UC_X86_REG_R8, Q)
        mu.reg_write(UC_X86_REG_R9, PAIR)
        mu.emu_start(0x39B860, 0x30000000, count=100000)
        return [struct.unpack_from("<ff", bytes(mu.mem_read(OUT + 8 * k, 8))) for k in range(4)]
    res = {}
    ok = True
    for pair in ((0.0, 0.0), (0.5, 0.5), (0.25 / 1.15, -0.5 * 1.15)):
        got = run(pair)
        want = [(float(f32(f32(f32(u) + f32(pair[0])) * f32(qq))), float(f32(f32(f32(v) + f32(pair[1])) * f32(qq))))
                for (u, v), qq in zip(uv, q)]
        ok &= all(struct.pack("<ff", *g) == struct.pack("<ff", *w) for g, w in zip(got, want))
        res[pair] = got
    differs = all(a != b for a, b in zip(res[(0.0, 0.0)], res[(0.5, 0.5)]))
    return ok and differs, "pair (0,0): %s; pair (0.5,0.5): %s" % (res[(0.0, 0.0)][:2], res[(0.5, 0.5)][:2])


# ================================================================================================ A3 / B censuses
def a3(img, R):
    R.note("-- A3: is everything else the same? (whole-range censuses)")
    BI, ci, ri, di = censuses(img, I0, I1)
    BF, cf, rf, df = censuses(img, F0, F1)
    dc = {"%08X" % k: (ci[k], cf[k]) for k in set(ci) | set(cf) if ci[k] != cf[k]}
    R.check("A3a callee multisets differ only in 0053DD10 (inline x2), 00808C40 (F's own cookie check) and the "
            "count of pure 0020E600 calls (76 vs 77)", dc == {"0053DD10": (2, 0), "00808C40": (0, 1),
                                                                  "0020E600": (76, 77)}, str(dc))
    B6 = Body(img, 0x20E600, 0x20E60A)
    R.check("A3b 0020E600 is pure: `mov eax, ecx` / `add rax, [01F83530]` / `ret` (no store)",
            [B6[a].text for a in B6.order] == ["mov eax, ecx", "add rax, qword ptr [rip + 0x1d74f27]", "ret"])
    dr = {"%08X" % k: (ri[k], rf[k]) for k in set(ri) | set(rf) if (k in ri) != (k in rf)}
    R.check("A3c rip-relative globals: the same set except 00D1247C (1.15, inline) and 01F44830 (F's cookie)",
            dr == {"00D1247C": (1, 0), "01F44830": (0, 1)}, str(dr))
    R.check("A3d non-stack memory operands: identical (displacement, scale, width) sets in I and F",
            di == df, "%s | %s" % (sorted(di - df), sorted(df - di)))
    R.check("A3e frame: inline shares 004355D0's 0x210 frame and epilogue; F has its own 0x1F0 frame; both return 1",
            BI is not None and Body(img, D, D + 32)[0x4355DD].text == "sub rsp, 0x210" and
            BF[0x437140].text == "sub rsp, 0x1f0" and BF[0x438837].text == "mov eax, 1" and
            Body(img, I0, I1)[0x436C86].text == "mov r8d, 1" and Body(img, I0, I1)[0x436CF0].text == "mov eax, r8d")


def b(img, R):
    R.note("-- B: the grid pair 004434D0 (G0, bit clear) / 00444340 (G1, bit set)")
    B0, c0, r0, d0 = censuses(img, G0s, G0e)
    B1, c1, r1, d1 = censuses(img, G1s, G1e)
    R.check("Ba both decode exactly over their extents", B0.exact and B1.exact)
    t1, t0 = zero_tests(B1, G1s, G1e), zero_tests(B0, G0s, G0e)
    g1 = groups(t1)
    R.check("Bb G1 has 16 corner tests in 4 quad groups (corner 0 by `movq rax, xmm2` / `test rax, rax`, corners 1-3 "
            "by `cmp qword ptr [rbp+0x40/0x50/0x60], 0`); G0 has none", len(t1) == 16 and len(g1) == 4 and
            all(len(v) == 4 for v in g1.values()) and not t0, "%d / %d" % (len(t1), len(t0)))
    skipped = set()
    for T, L in g1.items():
        skipped |= set(a for a, t in calls_in(B1, max(a for a, _ in L), T))
    claim1 = [(0x8D4, 0x39EC30), (0x9F4, 0x39EA70), (0xBF1, 0x39B860), (0xC1B, 0x39F9F0), (0xE41, 0x39B860),
              (0xE6B, 0x39F780)]
    claim0 = [(0x84D, 0x39EC30), (0x94D, 0x39EA70), (0xB19, 0x39B860), (0xB3B, 0x39F9F0), (0xD29, 0x39B860),
              (0xD4B, 0x39F780)]
    bad1 = [hex(o) for o, c in claim1 if not (G1s + o in skipped and B1[G1s + o].direct_target() == c)]
    bad0 = [hex(o) for o, c in claim0 if not (G0s + o in B0.ins and B0[G0s + o].direct_target() == c)]
    em0 = sorted(a for a, t in calls_in(B0, G0s, G0e) if t in EMIT)
    R.check("Bc the draft's six G1 call sites are skippable emitter/builder calls; its six G0 sites are the same "
            "callees and all of G0's emitter calls", not bad1 and not bad0 and em0 == sorted(G0s + o for o, _ in claim0),
            "%s %s" % (bad1, bad0))
    R.check("Bd callee multisets identical", c0 == c1, str({k: (c0[k], c1[k]) for k in set(c0) | set(c1)
                                                           if c0[k] != c1[k]}))
    R.check("Be rip-relative global sets identical", set(r0) == set(r1), str(set(r0) ^ set(r1)))
    R.check("Bf non-stack memory operand (displacement, scale, width) sets identical", d0 == d1,
            "%s | %s" % (sorted(d0 - d1), sorted(d1 - d0)))
    vals = [struct.unpack("<f", img.read(a, 4))[0] for a in (0x8F30EC, 0x8C5B30, 0xD113E4, 0xD113E0)]
    R.check("Bg the four grid constants: 0.0625, 0.001953125, 3.5625, 3.5", vals == [0.0625, 0.001953125, 3.5625, 3.5],
            str(vals))
    for B_, a, t in [(B0, 0x443A21, "movzx eax, word ptr [r9 + 2]"), (B0, 0x443A37, "movzx eax, word ptr [r9]"),
                     (B1, 0x4448E0, "movzx eax, word ptr [r8 + 2]"), (B1, 0x4448F6, "movzx eax, word ptr [r8]")]:
        expect(R, B_, a, t)
    for B_, a, t in [(B0, 0x4434D5, "push r14"), (B0, 0x4434E0, "sub rsp, 0x208"), (B1, 0x444345, "push rsi"),
                     (B1, 0x44434E, "sub rsp, 0x208"), (B0, 0x44431E, "call 0x808c40"), (B0, 0x444330, "ret"),
                     (B1, 0x4452BA, "call 0x808c40"), (B1, 0x4452CA, "ret")]:
        expect(R, B_, a, t)
    R.note("   => bookkeeping: same 0x208 frame, different pushed registers; neither sets eax after the cookie call")
    R.note("   => a grid entry's first 4 bytes are the two u16 the mode-2 screen term reads (X at +0, Y at +2); "
           "G1's test is on the entry's first 8 bytes")


# ================================================================================================ T: the transform
def t_transform(img, R):
    R.note("-- T (not in the draft): the same bit picks the vertex transform before every one of these draws")
    f_before = R.fails
    P5 = Body(img, 0x435050, 0x435050 + 610)
    for a, t in [(0x4350FC, "test byte ptr [r15 + 0x1f1], 8"), (0x43510B, "je 0x43525d"), (0x435122, "call 0x39a150"),
                 (0x435127, "call 0x24e410"), (0x43514C, "mov dword ptr [rdi], 0x81b78d03"),
                 (0x43526E, "call 0x399b80"), (0x435273, "test eax, eax"), (0x435275, "je 0x435167"),
                 (0x435280, "xor eax, eax"), (0x4352AD, "jmp 0x4351f6"), (0x4351F1, "mov eax, 1"),
                 (0x4351B0, "call 0x432300")]:
        expect(R, P5, a, t)
    P4 = Body(img, 0x434CD0, 0x434CD0 + 896)
    for a, t in [(0x434DF1, "test byte ptr [r14 + 0x1f1], 8"), (0x434E07, "je 0x434ed9"), (0x434E0D, "call 0x39a150"),
                 (0x434E12, "call 0x24e410"), (0x434E25, "mov word ptr [rsi], cx"),
                 (0x434ED9, "call 0x399b80"), (0x434EDE, "test eax, eax"),
                 (0x434EE0, "je 0x434e77"), (0x434EEA, "xor eax, eax"), (0x434F04, "jmp 0x435017")]:
        expect(R, P4, a, t)
    BD = Body(img, D, D + 5936)
    for a, t in [(0x435636, "call 0x434cd0"), (0x43563B, "test eax, eax"), (0x43563D, "jne 0x43566f"),
                 (0x435666, "call 0x435050"), (0x43566B, "test eax, eax"), (0x43566D, "je 0x43563f"),
                 (0x43563F, "xor eax, eax")]:
        expect(R, BD, a, t)
    R.check("T1 mesh: with +0x1F1 bit 3 set both preps call 0039A150 and ignore its result; clear, they call "
            "00399B80 and a non-zero result makes the prep return 0, and 004355D0 then returns 0 before its "
            "path ladder: nothing of the element is drawn (00435273 / 00434EDE -> 0043563F); all anchors above",
            R.fails == f_before)
    walks = [(0x4453D0, 1914, 0x44576C, "test byte ptr [r13 + 0x672], 1", 0x44578A, 0x445791, 0x445798, 0x445B04,
              (0x445AF8, 0x445AFF)),
             (0x447020, 2062, 0x4473FE, "test byte ptr [r15 + 0x6d2], 1", 0x447463, 0x44746A, 0x447471, 0x4477E5,
              (0x4477D9, 0x4477E0)),
             (0x447ED0, 2350, 0x4483CA, "test byte ptr [r13 + 0x6d2], 1", 0x448426, 0x44842D, 0x448434, 0x4487AD,
              (0x4487A1, 0x4487A8))]
    ok = True
    for w, n, ta, tt, c1, c0, jn, tgt, draws in walks:
        Bw = Body(img, w, w + n)
        ok &= Bw[ta].text == tt and Bw[c1].text == "call 0x39a150" and Bw[c0].text == "call 0x399b80" and \
            Bw[jn].text == "jne 0x%x" % tgt and all(d < tgt for d in draws) and \
            Bw[draws[0]].text == "call 0x444340" and Bw[draws[1]].text == "call 0x4434d0"
    R.check("T2 grid: walks 004453D0 / 00447020 / 00447ED0 test the same definition bit that picks 00444340, call "
            "0039A150 when set and 00399B80 when clear, and a non-zero 00399B80 result jumps past both draw calls",
            ok)
    T0 = Body(img, 0x399B80, 0x399B80 + 1482)
    T1 = Body(img, 0x39A150, 0x39A150 + 1558)
    for B_, a, t in [(T0, 0x39A0C6, "cmp rcx, rax"), (T0, 0x39A0C9, "jne 0x39a122"),
                     (T0, 0x39A122, "mov eax, dword ptr [rip + 0x1f3ee08]"), (T0, 0x39A0F6, "mov qword ptr [r11], rcx"),
                     (T1, 0x39A6C8, "cmp rax, rcx"), (T1, 0x39A6CB, "je 0x39a6f0"),
                     (T1, 0x39A6CD, "mov qword ptr [r11], rcx"), (T1, 0x39A712, "mov qword ptr [r11], rcx")]:
        expect(R, B_, a, t)
    r0 = [a for a in T0.order if T0[a].mnemonic == "ret"]
    r1 = [a for a in T1.order if T1[a].mnemonic == "ret"]
    R.check("T3 shape: 00399B80 leaves its vertex loop at the first vertex whose per-vertex compare is unequal "
            "(0039A0C9 -> 0039A122, returning the dword at 022D8F30); 0039A150 writes an entry on both outcomes of "
            "the same compare and continues (0039A6CD / 0039A712); both are call-free with one ret", len(r0) == 1 and len(r1) == 1 and
            not any(T0[a].mnemonic == "call" for a in T0.order) and not any(T1[a].mnemonic == "call" for a in T1.order))
    R.note("   NOT established here: what the compare tests (it reads clip-flag style globals of a VU-style "
           "emulation) and whether 0039A150 ever writes a first qword of zero - the condition that fires A-1 / B-1")


# ================================================================================================ P / C
def population(R):
    rows = list(csv.DictReader(open(K54), delimiter="\t"))
    c = collections.Counter((r["type"], r["path"]) for r in rows if r["byte0"] == "4")
    R.note("   active slots with slot byte +0 = 4 (param +0x130+p = 4), by (type, path): %s" % sorted(c.items()))
    R.check("P1 shipped: 57 inline type-0x05 slots have +0x130 byte 4 (the rescale applies to them); 00437130 "
            "elements author none (so no shipped bit-3 element would show A-2)",
            c[("0x05", "inline")] == 57 and c[("0x05", "00437130")] == 0)


def controls(img, R):
    def must_fail(label, cond):
        R.check("C control: the fabricated difference '%s' is rejected" % label, not cond)
    BF, cf, rf, df = censuses(img, F0, F1)
    must_fail("00437130 calls 0053DD10", cf[0x53DD10] > 0)
    BD = Body(img, D, D + 5936)
    must_fail("the inline path tests a corner's first qword for zero", bool(zero_tests(BD, I0, I1)))
    B0, c0, r0, d0 = censuses(img, G0s, G0e)
    B1, c1, r1, d1 = censuses(img, G1s, G1e)
    must_fail("00444340 reads a global 004434D0 does not (e.g. 00D1247C)", 0xD1247C in r1 and 0xD1247C not in r0)
    must_fail("004434D0 skips null corners too", bool(zero_tests(B0, G0s, G0e)))
    P = img.patched(0x53DD10, b"\x31\xc0\xc3\x90\x90\x90")      # xor eax,eax / ret: a 0053DD10 that returns 0
    B5 = Body(P, 0x53DD10, 0x53DD16)
    R.check("C control: on a patched image where 0053DD10 returns 0 the A2c anchor fails (the check reads the body)",
            B5[0x53DD10].text != "mov eax, 1")


def main():
    img = Img.load()
    img.cs.detail = True
    R = Report("sd199")
    BD = Body(img, D, D + 5936)
    BF = Body(img, F0, F1)
    R.check("00437130 decodes exactly over 5,930 bytes (00437130..00438859) and its .pdata tiles it",
            BF.exact and img.pdata_cover(F0, F1)[1])
    a0(img, R, BD)
    a1(img, R, BD, BF)
    a2(img, R, BD, BF)
    a3(img, R)
    b(img, R)
    t_transform(img, R)
    print("== P: shipped population")
    population(R)
    print("== C: controls")
    controls(img, R)
    print("== classification")
    for k, v in [("A-1 zero-first-qword corner skip (F only)", "DRAWN when it fires: the primitive is not emitted; "
                  "whether any entry has a zero first qword is not established"),
                 ("A-2 1/1.15, x1.15 pass-pair rescale (inline only)", "DRAWN: the pair is the additive UV offset of "
                  "the emitted S,T (A2g); always applied when +0x130 = 4 and +0x1F2 bit 0 is clear (0053DD10 returns 1)"),
                 ("B-1 zero-first-qword quad skip (G1 only)", "DRAWN when it fires; same open condition as A-1"),
                 ("T transform choice 0039A150 / 00399B80 (both preps, three grid walks)", "DRAWN: bit clear can "
                  "reject the whole element; bit set never rejects it"),
                 ("register/stack allocation, frame size, own vs shared epilogue, 0020E600 call count",
                  "BOOKKEEPING")]:
        print("CLASS  %-75s %s" % (k, v))
    print("FAILS %d" % R.fails)
    return 1 if R.fails else 0


if __name__ == "__main__":
    sys.exit(main())
