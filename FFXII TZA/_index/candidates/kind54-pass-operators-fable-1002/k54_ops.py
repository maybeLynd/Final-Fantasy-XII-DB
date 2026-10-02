"""k54_ops.py - FABLE, 2026-10-02. The kind-0x54 effect-mesh per-pass UV operators 0043E7B0 / 00434630 / 00434760 /
00396F20 / 00394B70 / 0043E840 and the clipper 00521450 (with its edge helper 00521BB0), read and executed.

Instruments over the certified image (SHA-256 73461D08...21F8, image base 0x120000):
  static   txt(addr) compares exact capstone text at each cited site; ripref(addr) resolves rip-relative targets;
           a raw rel32 scan (E8 / E9 / 0F 8x) over every executable section lists every direct site into the seven;
  execute  the SD-140 Unicorn harness (../sd140-vertex-prep-kernel-0930/sd140_emu.py, imported, not copied) runs the
           shipped bodies on seeded random inputs. Each E-check compares native output with a float32 Python model (the
           model is the claim, the native run is the control). Each N-check scores a deliberately WRONG model against the
           same native outputs and passes only if that wrong model is rejected (misses > 0).
No stubs are used anywhere in this file: every executed body runs to its own ret.
Sections: S image; P positive controls; A static anchors (call sites, selectors, operands); K constants;
E execution vs model; N wrong expectations that must fail; X contradictions with published text (reported, not edited).
"""
import hashlib, os, random, struct, sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SD140 = os.path.abspath(os.path.join(HERE, "..", "sd140-vertex-prep-kernel-0930"))
KIT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts"))
sys.path.insert(0, SD140)
sys.path.insert(0, KIT)
import retool as T  # noqa: E402
import sd140_emu as U  # noqa: E402
from unicorn.x86_const import UC_X86_REG_RSP, UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_R9, \
    UC_X86_REG_RAX, UC_X86_REG_RIP  # noqa: E402

R = T.R
f32 = np.float32
fails = 0
checks = 0


def check(tag, ok, text):
    global fails, checks
    checks += 1
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


def ins(a):
    return next(R.md.disasm(R.at(a, 16), a, 1))


def txt(a):
    i = ins(a)
    return "%s %s" % (i.mnemonic, i.op_str)


def ripref(a):
    i = ins(a)
    s = i.op_str
    k = s.index("[rip ")
    sign = -1 if s[k + 5] == "-" else 1
    disp = int(s[k + 7:s.index("]", k)], 16)
    return i.address + i.size + sign * disp


def all_txt(pairs):
    bad = [("%08X" % a, txt(a), e) for a, e in pairs if txt(a) != e]
    for b in bad:
        print("      mismatch %s: got %r want %r" % b)
    return not bad


def fl(a):
    return struct.unpack("<f", R.at(a, 4))[0]


# ---------------------------------------------------------------------------------------------------------------- S
h = hashlib.sha256(open(U.EXE, "rb").read()).hexdigest().upper()
check("S1", h.startswith("73461D08") and h.endswith("21F8"), "image %s..%s" % (h[:8], h[-4:]))

# ---------------------------------------------------------------------------------------------------------------- E harness
E = U.Emu()
S = U.SCR
mu = E.mu


def call(fn, rcx=0, rdx=0, r8=0, r9=0, stack_args=(), count=5_000_000):
    """Like Emu.call, but enters with rsp = 8 mod 16 (as a real `call` leaves it), so movaps spills to the callee's own
    frame are aligned exactly as in the shipped program."""
    rsp = U.STACK + 0xF0000 - 8
    frame = struct.pack("<Q", U.RET) + b"\0" * 32 + b"".join(struct.pack("<Q", a) for a in stack_args)
    mu.mem_write(rsp, frame)
    mu.reg_write(UC_X86_REG_RSP, rsp)
    for r, v in ((UC_X86_REG_RCX, rcx), (UC_X86_REG_RDX, rdx), (UC_X86_REG_R8, r8), (UC_X86_REG_R9, r9)):
        mu.reg_write(r, v)
    E.fault = None
    try:
        mu.emu_start(fn, U.RET, count=count)
    except Exception as e:  # noqa: BLE001
        E.fault = E.fault or ("exception", str(e))
    done = mu.reg_read(UC_X86_REG_RIP) == U.RET
    return mu.reg_read(UC_X86_REG_RAX), (E.fault is None and done)


def wf(a, xs):
    E.w(a, struct.pack("<%df" % len(xs), *[float(x) for x in xs]))


def rf(a, n):
    return [f32(x) for x in struct.unpack("<%df" % n, E.r(a, 4 * n))]


def fb(x):
    return struct.unpack("<I", struct.pack("<f", float(x)))[0]


rnd = random.Random(54)

# ---------------------------------------------------------------------------------------------------------------- P
# P1 positive control (execution): the method recovers SD-140's established kernel formula for 00432300,
#    out byte = min(255, (e * c) >> 7), through THIS file's call wrapper; the >> 8 rival must miss.
bad = tot = alt = 0
for trial in range(30):
    n = rnd.randint(1, 16)
    src = bytes(rnd.randrange(256) for _ in range(4 * n + 4))
    blk = bytes(rnd.randrange(256) for _ in range(16))
    E.w(S, src); E.w(S + 0x1000, blk); E.w(S + 0x2000, b"\xAA" * (4 * n + 8))
    _, ok = call(0x00432300, S, S + 0x1000, S + 0x2000, n)
    out = E.r(S + 0x2000, 4 * n)
    for i in range(4 * n):
        tot += 1
        bad += out[i] != min(255, (src[i] * blk[i % 4]) >> 7)
        alt += out[i] != (src[i] * blk[i % 4]) >> 8
    bad += not ok
check("P1", bad == 0 and tot > 500 and alt > tot // 4,
      "positive control: 00432300 native == min(255, e*c >> 7) on %d bytes via this harness (SD-140 E1); the >> 8 rival "
      "misses %d" % (tot, alt))
# P2 positive control (static): the reader recovers call sites the published record already cites - SD-140 A7's clip call
#    and BI-3b's "+0x174 resolve then 00396F20" at 00435AF6
check("P2", all_txt([(0x004392AE, "call 0x521450"), (0x00439272, "call 0x431d30"), (0x004392EF, "call 0x3afdd0"),
                     (0x00435AF6, "mov ecx, dword ptr [rsi + 0x174]"), (0x00435B15, "call 0x396f20")]),
      "positive control: SD-140 A7's 004392AE clip call and BI-3b's 00435AF6 +0x174 resolve before 00396F20 read back")

# ---------------------------------------------------------------------------------------------------------------- A
# A0 raw rel32 index: every E8 / E9 / 0F 8x rel32 in an executable section whose target is one of the seven (+ 00521BB0)
TGT = {0x0043E7B0: "swap", 0x00434630: "scaleoff", 0x00434760: "scaleoff_swap", 0x00396F20: "gather",
       0x00394B70: "screen_add", 0x0043E840: "centre_scale", 0x00521450: "clipper", 0x00521BB0: "clip_edge"}
raw = {t: [] for t in TGT}
for s in U._pe.sections:
    if not s.Characteristics & 0x20000000:
        continue
    d = s.get_data()
    va = U.BASE + s.VirtualAddress
    for k in range(len(d) - 5):
        b0 = d[k]
        if b0 in (0xE8, 0xE9):
            tgt = va + k + 5 + struct.unpack_from("<i", d, k + 1)[0]
            if tgt in raw:
                raw[tgt].append((va + k, "call" if b0 == 0xE8 else "jmp"))
        elif b0 == 0x0F and 0x80 <= d[k + 1] <= 0x8F and k + 6 <= len(d):
            tgt = va + k + 6 + struct.unpack_from("<i", d, k + 2)[0]
            if tgt in raw:
                raw[tgt].append((va + k, "jcc"))
for t in TGT:
    print("      raw %08X %-13s %s" % (t, TGT[t], " ".join("%08X:%s" % s for s in raw[t])))
want = {0x0043E7B0: {0x00435C79, 0x00437746, 0x00438F24, 0x00443C41, 0x00444B05},
        0x00434630: {0x00435C5D, 0x00437727, 0x00438F07, 0x00443C17, 0x00444AED},
        0x00434760: {0x00435C32, 0x004376FE, 0x00438EE0, 0x00443BF1, 0x00444AC7},
        0x00396F20: {0x00435B15, 0x00435BF4, 0x004375E0, 0x004376C7, 0x00438DBA, 0x00438EA2},
        0x00394B70: {0x00435B37, 0x00437600, 0x00438DDD},
        0x0043E840: {0x00435CAE, 0x00435CC0, 0x00435D0C, 0x00435D1E, 0x00437785, 0x00437797, 0x004377DB, 0x004377ED,
                     0x00438F59, 0x00438F77, 0x00438FB6, 0x00438FC7},
        0x00521450: {0x004392AE, 0x0043965B, 0x004398C6, 0x00439C1E, 0x00439FCB, 0x0043A236, 0x0043A6E3, 0x0043AC57,
                     0x0043AF5E, 0x0043B453, 0x0043B9C7, 0x0043BCCE, 0x0043C1C3, 0x0043C702, 0x0043C9ED, 0x0043CEA3,
                     0x0043D3E2, 0x0043D6CD, 0x00501E91, 0x00501FA8, 0x00502985, 0x00502AE0},
        0x00521BB0: {0x00521B26}}
rawok = all({a for a, k in raw[t] if k == "call"} == want[t] and not [1 for a, k in raw[t] if k != "call"] for t in TGT)
check("A0", rawok,
      "raw rel32 index == the listed call sites, no jmp / jcc entries: the six operators are reached only from 004355D0 / "
      "00437130 / 00438860 (+ 004434D0 / 00444340 for the first three); the clipper from 00438860 (18 sites) and "
      "00501A50 / 00502280; 00521BB0 only from 00521450")

# A1 004355D0 staging slots (SD-140 A3 layout): [rsp+0x68] = base (normals copy), [rsp+0x58] = base + 16*c16 (lit
#    per-normal table L), r14 = base + 32*c16 (screen vertices), [rsp+0x78] = prepared UV, [rsp+0x50] = per-pass UV'
check("A1", all_txt([(0x004356B0, "mov qword ptr [rsp + 0x68], rcx"), (0x004356D0, "mov qword ptr [rsp + 0x58], rcx"),
                     (0x004356D5, "lea r14, [rax + rcx]"), (0x004356F2, "mov qword ptr [rsp + 0x78], r9"),
                     (0x004356FB, "mov qword ptr [rsp + 0x50], rdx")]) and ripref(0x00435699) == 0x02AEED50,
      "004355D0: [rsp+0x78] = prepared UV, [rsp+0x50] = per-pass UV', [rsp+0x58] = L, r14 = screen vertices")
# A2 pass byte +0x1B0+p (regeneration source): 1/2/3/4 refill L through a lighting-family routine, then 00396F20 gathers
#    L[normal index].xy per corner into UV' (count +0x18); value 2 then adds 00394B70's screen term (positions by +0x170,
#    count +0x1A, screen array r14). 0 or >= 5: UV source stays the prepared UV ([rsp+0x78])
check("A2", all_txt([(0x004359E5, "movzx ecx, byte ptr [r15 + rdi + 0x1b0]"), (0x00435A0A, "mov rdi, r9"),
                     (0x00435AF1, "call 0x3962f0"), (0x00435AF6, "mov ecx, dword ptr [rsi + 0x174]"),
                     (0x00435AFC, "movzx ebx, word ptr [rsi + 0x18]"), (0x00435B05, "mov r8, qword ptr [rsp + 0x50]"),
                     (0x00435B0D, "mov rcx, qword ptr [rsp + 0x58]"), (0x00435B15, "call 0x396f20"),
                     (0x00435B1A, "mov ecx, dword ptr [rsi + 0x170]"), (0x00435B20, "movzx ebx, word ptr [rsi + 0x1a]"),
                     (0x00435B29, "mov r8, qword ptr [rsp + 0x50]"), (0x00435B34, "mov rcx, r14"),
                     (0x00435B37, "call 0x394b70"), (0x00435BC9, "call 0x395cf0"), (0x00435BD0, "call 0x395780"),
                     (0x00435A80, "call 0x396a30"), (0x00435A8A, "call 0x396560"), (0x00435BF4, "call 0x396f20")])
      and ripref(0x00435B4B) == 0x02AEEA20 and ripref(0x00435A9E) == 0x02AEEBF0 and ripref(0x00435A1B) == 0x02AEEA20
      and ripref(0x00435A12) == 0x02AEEBF0,
      "+0x1B0+p in 1..4: L refilled (1, 3 over 02AEEA20; 2, 4 over 02AEEBF0), UV'[k] = L[+0x174[k]].xy by 00396F20; =2 adds 00394B70(screen, +0x170, UV', +0x1A)")
# A3 pass byte +0x1AC+p (operator): 1 -> 0043E7B0(src, UV', +0x1A); 2 -> 00434630(src, UV', param+0x150+16p, +0x1A);
#    3 -> 00434760(same); other -> no operator. src = rdi = the current UV source (prepared UV or UV' from A2)
check("A3", all_txt([(0x00435BFE, "movzx ecx, byte ptr [r15 + rbx + 0x1ac]"), (0x00435C16, "mov rax, qword ptr [rsp + 0x48]"),
                     (0x00435C1B, "mov rcx, rdi"), (0x00435C1E, "movzx r9d, word ptr [rsi + 0x1a]"),
                     (0x00435C23, "mov rdx, qword ptr [rsp + 0x50]"), (0x00435C28, "lea r8, [rax + 0x150]"),
                     (0x00435C2F, "add r8, r15"), (0x00435C32, "call 0x434760"), (0x00435C53, "lea r8, [rax + 0x150]"),
                     (0x00435C5D, "call 0x434630"), (0x00435C6C, "movzx r8d, word ptr [rsi + 0x1a]"),
                     (0x00435C71, "mov rcx, rdi"), (0x00435C79, "call 0x43e7b0"), (0x00435C3C, "mov rdi, rcx"),
                     (0x0043577B, "shl rax, 4")]),
      "+0x1AC+p: 1 swap (0043E7B0), 2 scale+offset (00434630), 3 scale+offset+swap (00434760) by param+0x150+16p -> UV'")
# A4 param +0x1F2: bit 0 -> 0043E840(src, UV', r8 = r12 = param+0x50+8p, +0x1A) then the pass pair := (0.5, 0.5);
#    else bit 1 -> 0043E840(src, UV', &(w, w), +0x1A) with w = param+0x1EC, then the pass pair += 0.5 (01CEBB70);
#    then, when pass mode +0x130+p == 4 and 0053DD10() == 1, pair.x /= 1.15, pair.y *= 1.15 (00D1247C) - 004355D0 only
check("A4", all_txt([(0x00435763, "lea r12, [rdi + 0xa]"), (0x0043576F, "lea r12, [r15 + r12*8]"),
                     (0x00435C8D, "movzx eax, byte ptr [r15 + 0x1f2]"), (0x00435C95, "test al, 1"),
                     (0x00435C99, "mov r8, r12"), (0x00435CA1, "cmp rdi, qword ptr [rsp + 0x78]"), (0x00435CAE, "call 0x43e840"),
                     (0x00435CC0, "call 0x43e840"), (0x00435CC5, "mov dword ptr [r12], 0x3f000000"),
                     (0x00435CCD, "mov dword ptr [r12 + 4], 0x3f000000"), (0x00435CDB, "test al, 2"),
                     (0x00435CE7, "movss xmm0, dword ptr [r15 + 0x1ec]"), (0x00435CF5, "movss dword ptr [rbp - 0x70], xmm0"),
                     (0x00435CFA, "movss dword ptr [rbp - 0x6c], xmm0"), (0x00435D0C, "call 0x43e840"),
                     (0x00435D23, "cmp byte ptr [r15 + rbx + 0x130], 4"), (0x00435D2E, "call 0x53dd10"),
                     (0x00435D45, "divss xmm0, xmm6"), (0x00435D49, "mulss xmm1, xmm6"), (0x00435D67, "addss xmm0, xmm7"),
                     (0x00435D6B, "addss xmm1, xmm7"), (0x00435D9B, "movss dword ptr [r12 + 4], xmm1"),
                     (0x00435DA2, "movss dword ptr [r12], xmm0")]),
      "+0x1F2 bit0: 0043E840 by the pass pair, pair := 0.5; bit1: 0043E840 by (w,w) w=+0x1EC, pair += 0.5; mode 4: /1.15 x1.15")
check("A4b", ripref(0x0043573D) == 0x00D1247C and ripref(0x0043574D) == 0x01CEBB70
      and bytes(R.at(0x0053DD10, 6)) == bytes.fromhex("b801000000c3"),
      "xmm6 = [00D1247C], xmm7 = [01CEBB70]; 0053DD10 is `mov eax, 1; ret` (the mode-4 aspect rewrite is unconditional)")
# A5 the same selector ladder in 00437130 and 00438860 (+0x1AC operators, +0x1F2 0043E840, the 0.5 constant); neither
#    has the 1.15 rewrite
check("A5", all_txt([(0x004376CC, "movzx edx, byte ptr [r15 + r13 + 0x1ac]"), (0x004376E9, "lea r8, [r13 + 0x150]"),
                     (0x004376FE, "call 0x434760"), (0x00437727, "call 0x434630"), (0x00437746, "call 0x43e7b0"),
                     (0x00437764, "movzx eax, byte ptr [rbx + 0x1f2]"), (0x00437785, "call 0x43e840"),
                     (0x004377A1, "mov dword ptr [rax], 0x3f000000"), (0x004377B8, "movss xmm0, dword ptr [rbx + 0x1ec]"),
                     (0x004377DB, "call 0x43e840"), (0x00437800, "addss xmm0, xmm6"), (0x004375E0, "call 0x396f20"),
                     (0x00437600, "call 0x394b70"),
                     (0x00438EB0, "movzx edx, byte ptr [rax + rbx + 0x1ac]"), (0x00438ECC, "lea r8, [r15 + 0x150]"),
                     (0x00438EE0, "call 0x434760"), (0x00438F07, "call 0x434630"), (0x00438F24, "call 0x43e7b0"),
                     (0x00438F3A, "movzx eax, byte ptr [rbx + 0x1f2]"), (0x00438F59, "call 0x43e840"),
                     (0x00438F65, "mov dword ptr [rdi], 0x3f000000"), (0x00438F93, "movss xmm0, dword ptr [rbx + 0x1ec]"),
                     (0x00438FB6, "call 0x43e840"), (0x00438FD5, "addss xmm0, xmm8"), (0x00438DBA, "call 0x396f20"),
                     (0x00438DDD, "call 0x394b70")])
      and ripref(0x004371F2) == 0x01CEBB70 and ripref(0x004389E2) == 0x01CEBB70,
      "00437130 / 00438860 run the same +0x1B0 / +0x1AC / +0x1F2 ladder with +0.5 from 01CEBB70; no 1.15 rewrite there")
# A6 00438860's clip sites: three corners -> clip vertices of 0x40 B (+0 position float4, +0x10 colour float4 by
#    00431D30, +0x20 the corner's per-pass UV qword), clipper(rcx = matrix at rbp+0x30, rdx = vertex buffer); count 0 ->
#    the triangle is dropped; else each output vertex's +0 position is re-projected (0039A150), +0x10 packed back to
#    bytes (003AFDD0), +0x20 UV to ST (0039B880), and an n-gon builder emits count corners
check("A6", all_txt([(0x004392A3, "lea rdx, [rbp + 0x310]"), (0x004392AA, "lea rcx, [rbp + 0x30]"),
                     (0x004392B3, "mov r13d, eax"), (0x004392B6, "test eax, eax"), (0x004392B8, "je 0x43934b"),
                     (0x004392E2, "movaps xmm0, xmmword ptr [rdi]"), (0x004392EB, "movdqa xmmword ptr [rbx], xmm0"),
                     (0x004392EF, "call 0x3afdd0"), (0x004392F8, "lea rdi, [rdi + 0x40]"), (0x00439313, "mov r9d, r13d"),
                     (0x0043932B, "call 0x39a150"), (0x00439330, "mov r8d, r13d"), (0x00439341, "call 0x43e440"),
                     (0x0043B3F4, "mov qword ptr [rbp + 0x330], rax"), (0x0043B3FF, "mov qword ptr [rbp + 0x370], rax"),
                     (0x0043B409, "mov qword ptr [rbp + 0x3b0], rax"), (0x0043B453, "call 0x521450"),
                     (0x0043B462, "je 0x43b55d"), (0x0043B497, "mov rax, qword ptr [rbx]"), (0x0043B4A2, "mov qword ptr [rdi], rax"),
                     (0x0043B4EA, "call 0x39a150"), (0x0043B510, "call 0x39b880"), (0x0043B551, "call 0x43db90")]),
      "00438860: clipper(matrix, 3 corners); 0 -> drop; n -> re-project the clipped +0 positions, colour + UV per vertex, n-gon")
# A7 the clip matrix: rbp+0x30 = 00397910(02AEDDF0, 00397910(02AEEA20, param)) in 00438860's prologue
check("A7", all_txt([(0x0043891F, "lea r8, [rbp + 0x30]"), (0x00438923, "mov rdx, rbx"), (0x0043892D, "call 0x397910"),
                     (0x00438932, "lea r8, [rbp + 0x30]"), (0x00438936, "lea rdx, [rbp + 0x30]"), (0x00438941, "call 0x397910")])
      and ripref(0x00438926) == 0x02AEEA20 and ripref(0x0043893A) == 0x02AEDDF0,
      "clip matrix (rbp+0x30) = 00397910 over 02AEDDF0 and (00397910 over 02AEEA20 and the parameter block)")
# A8 the clipper's control: 3 input vertices, 6 passes over a 16-B plane table at 01F2C760 (sign float, outcode-pair
#    mask, axis index), ping-pong buffers rdx / rdx+0x400 (6 passes -> result back at rdx), returns the vertex count
check("A8", all_txt([(0x00521472, "lea rdi, [rdx + 0x400]"), (0x00521489, "mov r8d, 3"), (0x00521793, "lea r12d, [r8 + 3]"),
                     (0x005218D5, "movups xmmword ptr [rdx + 0x30], xmm1"), (0x005218E0, "movups xmmword ptr [rdx + 0x70], xmm0"),
                     (0x005218EB, "movups xmmword ptr [rdx + 0xb0], xmm1"), (0x00521913, "movaps xmmword ptr [rax + r14], xmm0"),
                     (0x00521981, "andps xmm0, xmm7"), (0x00521988, "comiss xmm2, xmm3"), (0x0052198D, "or eax, 1"),
                     (0x00521999, "xorps xmm0, xmm6"), (0x005219A1, "or eax, 2"), (0x005219C5, "or eax, 8"),
                     (0x005219E9, "or eax, 0x20"), (0x00521A12, "shl eax, 6"), (0x00521A8C, "mov ecx, dword ptr [rbp + 4]"),
                     (0x00521A9C, "and ecx, eax"), (0x00521AA4, "and ecx, 0xfff"), (0x00521AD6, "test cl, 0x3f"),
                     (0x00521ADB, "test ecx, 0xfc0"), (0x00521B26, "call 0x521bb0"), (0x00521B43, "add rbp, 0x10"),
                     (0x00521B4A, "mov r8d, ebx"), (0x00521B50, "sub r12, 1"), (0x00521B6C, "mov eax, ebx")])
      and ripref(0x0052177E) == 0x01F2C760,
      "00521450: outcode per vertex vs +-|w| on x, y, z; per plane keep / keep+split / split / drop by the edge's code pair")
tab = [struct.unpack("<fIII", R.at(0x01F2C760 + 16 * i, 16)) for i in range(6)]
check("A9", [(t[0], t[1], t[2]) for t in tab] == [(-1.0, 0x820, 2), (1.0, 0x410, 2), (-1.0, 0x208, 1), (1.0, 0x104, 1),
                                                   (-1.0, 0x82, 0), (1.0, 0x41, 0)],
      "plane table 01F2C760: z < -|w|, z > |w|, y < -|w|, y > |w|, x < -|w|, x > |w| (sign, both-vertex mask, axis)")

# ---------------------------------------------------------------------------------------------------------------- K
check("K1", (fl(0x008F30EC), fl(0x008C5B30), fl(0x00D113E0), fl(0x00D113E4)) == (0.0625, 0.001953125, 3.5, 3.5625)
      and ripref(0x00394B76) == 0x008F30EC and ripref(0x00394B80) == 0x008C5B30 and ripref(0x00394B8B) == 0x00D113E4
      and ripref(0x00394B96) == 0x00D113E0,
      "00394B70 constants: 1/16 (12.4 fixed point), 1/512, 3.5 (u), 3.5625 (v)")
check("K2", fl(0x00D1247C) == f32(1.15) and fl(0x01CEBB70) == 0.5 and fl(0x01EF93FC) == 1.0
      and txt(0x0043E84D) == "mov qword ptr [rip + 0x1e9a758], 0xffffffffbf000000",
      "1.15 (00D1247C), 0.5 (01CEBB70), 1.0 (01EF93FC, the operators' unit multiplier); 0043E840's -0.5 is an immediate")
check("K3", fl(0x00902EF4) == 10000.0 and fl(0x01CEBB60) == f32(1e-4) and ripref(0x0052146A) == 0x00902EF4
      and ripref(0x00521479) == 0x01CEBB60,
      "00521450: 10000.0 and 0.0001 - the colour lanes are scaled x1e4 before interpolation and x1e-4 after (00521BB0)")

# ---------------------------------------------------------------------------------------------------------------- E
SRC, DST, BLK = S, S + 0x4000, S + 0x8000


# E1 0043E7B0(src, dst, n): dst[i] = (src[i].v, src[i].u) - a per-pair swap of the two dwords; do-while (n = 0 -> 1 pair)
bad = runs = ident = 0
for trial in range(40):
    n = rnd.randint(1, 24)
    src = bytes(rnd.randrange(256) for _ in range(8 * n + 8))
    E.w(SRC, src); E.w(DST, b"\xAA" * (8 * n + 8))
    _, ok = call(0x0043E7B0, SRC, DST, n)
    out = E.r(DST, 8 * n + 8)
    want_ = b"".join(src[8 * i + 4:8 * i + 8] + src[8 * i:8 * i + 4] for i in range(n))
    bad += out[:8 * n] != want_ or out[8 * n:] != b"\xAA" * 8 or not ok
    ident += out[:8 * n] != src[:8 * n]
    runs += 1
E.w(DST, b"\xAA" * 16); call(0x0043E7B0, SRC, DST, 0)
zero1 = E.r(DST, 16)
check("E1", bad == 0 and zero1[:8] == E.r(SRC, 8)[4:8] + E.r(SRC, 8)[:4] and zero1[8:] == b"\xAA" * 8,
      "0043E7B0 native == (u, v) -> (v, u) per pair over %d trials (no stubs); count 0 still swaps one pair" % runs)
N1 = ident


def m_so(u, v, b):  # 00434630
    return (f32(b[0] * f32(1.0)) + f32(u * b[2]), f32(b[1] * f32(1.0)) + f32(v * b[3]))


# E2 00434630(src, dst, blk, n): dst = (b0 + u*b2, b1 + v*b3); E3 00434760: the same then swapped
res = {}
for fn, swap in ((0x00434630, False), (0x00434760, True)):
    bad = tot = altrole = altnoswap = 0
    for trial in range(40):
        n = rnd.randint(1, 20)
        uv = [f32(rnd.uniform(-3, 3)) for _ in range(2 * n + 2)]
        b = [f32(rnd.uniform(-4, 4)) for _ in range(4)]
        wf(SRC, uv); wf(BLK, b); E.w(DST, b"\xAA" * (8 * n + 8))
        _, ok = call(fn, SRC, DST, BLK, n)
        got = rf(DST, 2 * n)
        for i in range(n):
            x, y = m_so(uv[2 * i], uv[2 * i + 1], b)
            w_ = (y, x) if swap else (x, y)
            tot += 1
            bad += (got[2 * i], got[2 * i + 1]) != w_
            r = (f32(uv[2 * i] * b[0]) + b[2], f32(uv[2 * i + 1] * b[1]) + b[3])
            altrole += (got[2 * i], got[2 * i + 1]) != ((r[1], r[0]) if swap else r)
            altnoswap += (got[2 * i], got[2 * i + 1]) != (x, y)
        bad += E.r(DST + 8 * n, 8) != b"\xAA" * 8 or not ok
    res[fn] = (bad, tot, altrole, altnoswap)
b, t_, a1, a2 = res[0x00434630]
check("E2", b == 0 and t_ > 300, "00434630 native == (b0 + u*b2, b1 + v*b3) with blk = param+0x150+16p, %d pairs (no stubs)" % t_)
N2 = a1
b, t_, a1, a2 = res[0x00434760]
check("E3", b == 0 and t_ > 300, "00434760 native == (b1 + v*b3, b0 + u*b2) - 00434630 then swapped, %d pairs (no stubs)" % t_)
N3 = a2

# E4 00396F20(table, list, dst, n): dst[i] = qword table[16*list[i]] (first two floats of a 16-B entry); list is s16;
#    the table address is used as 32 bits (movsxd / cdqe) - a low-4-GB pointer, which the staging buffer is
TAB, LST = S + 0x10000, S + 0x20000
z8f10 = E.r(0x022D8F10, 8)
bad = tot = altent = 0
for trial in range(40):
    n = rnd.randint(1, 30); m = rnd.randint(1, 12)
    tb = bytes(rnd.randrange(256) for _ in range(16 * m))
    li = [rnd.randrange(m) for _ in range(n + 1)]
    E.w(TAB, tb); E.w(LST, struct.pack("<%dh" % (n + 1), *li)); E.w(DST, b"\xAA" * (8 * n + 8))
    _, ok = call(0x00396F20, TAB, LST, DST, n)
    out = E.r(DST, 8 * n + 8)
    for i in range(n):
        tot += 1
        bad += out[8 * i:8 * i + 8] != tb[16 * li[i]:16 * li[i] + 8]
        altent += out[8 * i:8 * i + 8] != tb[16 * li[i] + 8:16 * li[i] + 16]
    bad += out[8 * n:] != b"\xAA" * 8 or not ok
check("E4", bad == 0 and tot > 300 and z8f10 == bytes(8),
      "00396F20 native == dst[k] = table[list[k]].xy (16-B stride, first 8 B), %d corners (no stubs); its loop ends on "
      "the image's zero cell 022D8F10 (= 0 here)" % tot)
N4 = altent


# E5 00394B70(screen, list, dst, n): dst[k].u += X/16/512 - 3.5, dst[k].v += Y/16/512 - 3.5625, X, Y the u16 at +0 / +2
#    of the 16-B screen vertex list[k] (GS XYZ, 12.4); accumulates; n < 1 writes nothing; 4-unrolled with a tail
def m_scr(X, Y, u, v):
    du = f32(f32(f32(f32(X) * f32(0.0625)) * f32(0.001953125)) - f32(3.5))
    dv = f32(f32(f32(f32(Y) * f32(0.0625)) * f32(0.001953125)) - f32(3.5625))
    return f32(du + u), f32(dv + v)


bad = tot = altover = altswap = 0
for trial in range(50):
    n = rnd.randint(1, 14); m = rnd.randint(1, 10)
    scr = b"".join(struct.pack("<HHIQ", rnd.randrange(65536), rnd.randrange(65536), rnd.getrandbits(32), rnd.getrandbits(64))
                   for _ in range(m))
    li = [rnd.randrange(m) for _ in range(n)]
    uv = [f32(rnd.uniform(-1, 1)) for _ in range(2 * n)]
    E.w(TAB, scr); E.w(LST, struct.pack("<%dH" % n, *li)); wf(DST, uv); E.w(DST + 8 * n, b"\xAA" * 8)
    _, ok = call(0x00394B70, TAB, LST, DST, n)
    got = rf(DST, 2 * n)
    for k in range(n):
        X, Y = struct.unpack_from("<HH", scr, 16 * li[k])
        w_ = m_scr(X, Y, uv[2 * k], uv[2 * k + 1])
        tot += 1
        bad += (got[2 * k], got[2 * k + 1]) != w_
        altover += (got[2 * k], got[2 * k + 1]) != m_scr(X, Y, f32(0), f32(0))
        d = m_scr(Y, X, uv[2 * k], uv[2 * k + 1])
        altswap += (got[2 * k], got[2 * k + 1]) != d
    bad += E.r(DST + 8 * n, 8) != b"\xAA" * 8 or not ok
wf(DST, [1.0, 2.0]); _, ok0 = call(0x00394B70, TAB, LST, DST, 0)
check("E5", bad == 0 and tot > 200 and rf(DST, 2) == [1.0, 2.0] and ok0,
      "00394B70 native == UV += ((X/16)/512 - 3.5, (Y/16)/512 - 3.5625) from the corner's screen vertex, %d corners, "
      "n = 1..14 (unrolled + tail), n = 0 no write (no stubs)" % tot)
N5 = (altover, altswap)


# E6 0043E840(src, dst, &(a, b), n): dst = ((u - 0.5)*a, (v - 0.5)*b), computed as -0.5*a + u*a; in place allowed
def m_cs(u, v, a, b):
    return f32(f32(f32(-0.5) * a) + f32(u * a)), f32(f32(f32(-0.5) * b) + f32(v * b))


bad = tot = altnooff = altrecentre = 0
for trial in range(50):
    n = rnd.randint(1, 20)
    uv = [f32(rnd.uniform(-2, 3)) for _ in range(2 * n + 2)]
    ab = [f32(rnd.uniform(-3, 3)) for _ in range(2)]
    inplace = trial % 2 == 1
    wf(SRC, uv); wf(BLK, ab); E.w(DST, b"\xAA" * (8 * n + 8))
    _, ok = call(0x0043E840, SRC, SRC if inplace else DST, BLK, n)
    got = rf(SRC if inplace else DST, 2 * n)
    for i in range(n):
        w_ = m_cs(uv[2 * i], uv[2 * i + 1], ab[0], ab[1])
        tot += 1
        bad += (got[2 * i], got[2 * i + 1]) != w_
        altnooff += (got[2 * i], got[2 * i + 1]) != (f32(uv[2 * i] * ab[0]), f32(uv[2 * i + 1] * ab[1]))
        altrecentre += (got[2 * i], got[2 * i + 1]) != (f32(w_[0] + f32(0.5)), f32(w_[1] + f32(0.5)))
    bad += (not inplace and E.r(DST + 8 * n, 8) != b"\xAA" * 8) or not ok
check("E6", bad == 0 and tot > 300,
      "0043E840 native == ((u - 0.5)*a, (v - 0.5)*b) with (a, b) = [r8], %d pairs, half in place (no stubs)" % tot)
N6 = (altnooff, altrecentre)

# E7 00521450(matrix, vbuf): homogeneous clip of one triangle. Model: clip = x*M0 + y*M1 + z*M2 + w*M3 for the three
#    input +0 positions (stored at +0x30); Sutherland-Hodgman over the six table planes in order; outcode bits x>|w|,
#    -|w|>x, y.., z..; an edge with exactly one vertex outside a plane gets a new vertex at t = d0/(d0+d1),
#    d = |c[axis] - s*w|; +0 position, +0x20 (16 B) and +0x30 clip lerp as a + t*(b - a); +0x10 colour the same on
#    x1e4-scaled lanes, then x1e-4; returns the count, result in place at vbuf.
PL = [(-1.0, 0x820, 2), (1.0, 0x410, 2), (-1.0, 0x208, 1), (1.0, 0x104, 1), (-1.0, 0x82, 0), (1.0, 0x41, 0)]


def outcode(c, band=1.0, signed_w=False):
    w = c[3] if signed_w else f32(abs(c[3]))
    w = f32(w * f32(band))
    code = 0
    for k, (hi, lo) in enumerate(((1, 2), (4, 8), (0x10, 0x20))):
        if c[k] > w:
            code |= hi
        if f32(-w) > c[k]:
            code |= lo
    return code


def lerp(a, b, t):
    return [f32(f32(f32(b[i] - a[i]) * t) + a[i]) for i in range(4)]


def isect(a, b, s, ax, rev=False, noscale=False):
    d0 = f32(abs(f32(a["c"][ax] - f32(f32(s) * a["c"][3]))))
    d1 = f32(abs(f32(b["c"][ax] - f32(f32(s) * b["c"][3]))))
    t = f32(f32(d1 if rev else d0) / f32(d0 + d1))
    if noscale:
        col = lerp(a["col"], b["col"], t)
    else:
        ca = [f32(x * f32(10000.0)) for x in a["col"]]
        cb = [f32(x * f32(10000.0)) for x in b["col"]]
        col = [f32(x * f32(1e-4)) for x in lerp(ca, cb, t)]
    return {"p": lerp(a["p"], b["p"], t), "col": col,
            "uv": lerp(a["uv"], b["uv"], t), "c": lerp(a["c"], b["c"], t)}


def xform(M, p):
    return [f32(f32(f32(f32(p[0] * M[0][k]) + f32(p[1] * M[1][k])) + f32(p[2] * M[2][k])) + f32(p[3] * M[3][k]))
            for k in range(4)]


def clip_model(M, tri, band=1.0, signed_w=False, rev=False, noscale=False):
    cur = [dict(v, c=xform(M, v["p"])) for v in tri]
    for s, mask, ax in PL:
        if not cur:
            break
        ext = cur + [cur[0]]
        out = []
        for i in range(len(cur)):
            a, b = ext[i], ext[i + 1]
            code = ((outcode(a["c"], band, signed_w) << 6) | outcode(b["c"], band, signed_w)) & mask & 0xFFF
            if code == 0:
                out.append(a)
            elif code & 0x3F and not code & 0xFC0:
                out.append(a)
                out.append(isect(a, b, s, ax, rev, noscale))
            elif code & 0xFC0 and not code & 0x3F:
                out.append(isect(a, b, s, ax, rev, noscale))
        cur = out
    return cur


def same(mv, gv):
    return all(mv[k] == gv[k] for k in ("p", "col", "uv", "c"))


VB, MAT = S + 0x30000, S + 0x38000
stats = {}
bad = maxerr = 0
rivals = {"count3": 0, "rev_t": 0, "guard2": 0, "signed_w": 0}
noscale_miss = 0
onplane = onplane_neg = negtri = 0
trials = 400
for trial in range(trials):
    M = [[f32((1.0 if r == c_ else 0.0) + rnd.gauss(0, 0.6)) for c_ in range(4)] for r in range(4)]
    M[3][3] = f32(rnd.uniform(0.3, 2.0))
    tri = [{"p": [f32(rnd.uniform(-2.5, 2.5)) for _ in range(3)] + [f32(1.0)],
            "col": [f32(rnd.randrange(256)) for _ in range(4)],
            "uv": [f32(rnd.uniform(-1, 2)) for _ in range(2)] + [f32(rnd.uniform(-9, 9)) for _ in range(2)]} for _ in range(3)]
    wf(MAT, [x for row in M for x in row])
    E.w(VB, b"\xCC" * 0x800)
    for i, v in enumerate(tri):
        wf(VB + 0x40 * i, v["p"] + v["col"] + v["uv"] + [0, 0, 0, 0])
    plane8 = E.r(0x01F2C760, 0x60)
    cnt, ok = call(0x00521450, MAT, VB)
    cnt &= 0xFFFFFFFF
    model = clip_model(M, tri)
    stats[len(model)] = stats.get(len(model), 0) + 1
    got = []
    for i in range(cnt if cnt < 16 else 0):
        q = rf(VB + 0x40 * i, 16)
        got.append({"p": q[0:4], "col": q[4:8], "uv": q[8:12], "c": q[12:16]})
    good = ok and cnt == len(model) and all(same(m, g) for m, g in zip(model, got)) and E.r(0x01F2C760, 0x60) == plane8
    if not good and bad < 3:
        print("      E7 trial %d: native count %d model %d ok %s" % (trial, cnt, len(model), ok))
    bad += not good
    negw = any(float(v["c"][3]) <= 0 for v in [dict(v, c=xform(M, v["p"])) for v in tri])
    negtri += negw
    for g in got:  # every output vertex is inside |x|,|y|,|z| <= |w| up to float error
        w = abs(float(g["c"][3]))
        out_ = any(abs(float(g["c"][k])) > w * (1 + 1e-5) + 1e-5 for k in range(3))
        onplane += out_ and not negw
        onplane_neg += out_ and negw
    rivals["count3"] += cnt != 3
    rivals["rev_t"] += not (cnt == len(clip_model(M, tri, rev=True))
                            and all(same(m, g) for m, g in zip(clip_model(M, tri, rev=True), got)))
    rivals["guard2"] += cnt != len(clip_model(M, tri, band=2.0))
    ns = clip_model(M, tri, noscale=True)
    noscale_miss += not (cnt == len(ns) and all(same(m, g) for m, g in zip(ns, got)))
    rivals["signed_w"] += not (cnt == len(clip_model(M, tri, signed_w=True))
                               and all(same(m, g) for m, g in zip(clip_model(M, tri, signed_w=True), got)))
print("      E7 output vertex-count histogram (model): %s" % dict(sorted(stats.items())))
check("E7", bad == 0 and len(stats) >= 5 and stats.get(0, 0) > 10 and stats.get(3, 0) > 10,
      "00521450 native == Sutherland-Hodgman against |x|,|y|,|z| <= |w| (6 table planes), bit-exact on count and all four "
      "64-B vertex fields over %d seeded triangles, plane table restored (no stubs)" % trials)
check("E8", onplane == 0 and onplane_neg > 0,
      "when all three corners have clip w > 0 every output vertex satisfies |x|,|y|,|z| <= w (+0x30) within float error; "
      "in the %d trials with a corner at w <= 0 the |w| outcodes and the signed-w split leave %d output vertices outside "
      "the box - the clipper has no w > 0 plane" % (negtri, onplane_neg))

print("      E7 sensitivity: a model WITHOUT the x1e4 / x1e-4 colour scaling differs bit-wise in %d of %d trials "
      "(the scaling is a float-rounding detail; the colour is still a linear interpolation)" % (noscale_miss, trials))

# ---------------------------------------------------------------------------------------------------------------- N
check("N1", N1 > 0, "wrong expectation '0043E7B0 is a plain counted copy' rejected (%d of 40 trials differ)" % N1)
check("N2", N2 > 300, "wrong expectation '00434630 = u*b0 + b2 (offset and scale roles exchanged)' rejected (%d misses)" % N2)
check("N3", N3 > 300, "wrong expectation '00434760 = 00434630 without the swap' rejected (%d misses)" % N3)
check("N4", N4 > 300, "wrong expectation '00396F20 copies the entry's second qword (z, w)' rejected (%d misses)" % N4)
check("N5", N5[0] > 200 and N5[1] > 200,
      "wrong expectations '00394B70 overwrites' and 'X feeds v' rejected (%d / %d misses)" % N5)
check("N6", N6[0] > 300 and N6[1] > 300,
      "wrong expectations '0043E840 = u*a' and '0043E840 re-centres (+0.5)' rejected (%d / %d misses)" % N6)
check("N7", all(v > 20 for v in rivals.values()),
      "wrong clipper expectations rejected: always-3 / flag-only %(count3)d, t = d1/(d0+d1) %(rev_t)d, guard band 2|w| "
      "%(guard2)d, signed-w outcodes %(signed_w)d trials differ" % rivals)

# ---------------------------------------------------------------------------------------------------------------- X
# X1 the-two-transform-primitives.md (SWE2-EC7-83 / later blocks) names these bodies by their scratch traffic:
#    0043E7B0 "a counted copy driving the global ring", 00434760 / 00434630 "bank-transform", 0043E840 "a call-free
#    publish of the workbench header", 00396F20 "index scatter", 00394B70 "the weight scatter"; and it cites 02EB87xx /
#    02EB8Fxx / 02EB9xxx scratch addresses the bodies do not touch (they address 022D8F90 / 022D92E0 / 022D94A0)
check("X1", ripref(0x0043E7D7) == 0x022D8F90 and ripref(0x00434654) == 0x022D92F0 and ripref(0x0043E973) == 0x022D94A0,
      "the operators address 022D8F90 / 022D92F0 / 022D94A0, not the 02EB87xx-02EB94xx cells that page cites")
# X2 how-an-authored-number-gets-its-randomness.md (SWE2-EC7-83) calls 00521450 "call-free ... a pure-SSE 4x4 transform
#    fold with no calls": it calls 00521BB0 (A8, raw index A0) and is a six-plane polygon clipper (E7)
check("X2", txt(0x00521B26) == "call 0x521bb0", "00521450 is not call-free: 00521B26 calls 00521BB0 (the edge split)")

print("RESULT pass byte +0x1B0 can regenerate the per-pass UV from L[normal].xy (00396F20) plus, for value 2, a screen-"
      "position term (00394B70); byte +0x1AC then swaps (0043E7B0) or scales+offsets (00434630, 00434760 = +swap) by "
      "param+0x150+16p; param+0x1F2 scales about the 0.5 centre (0043E840) by the pass pair or by +0x1EC; 00521450 "
      "clips each triangle in homogeneous space against |x|,|y|,|z| <= |w|, interpolating position, colour, UV and "
      "clip position, and returns the polygon's vertex count (0 = culled)")
print("CHECKS %d  FAILS %d" % (checks, fails))
