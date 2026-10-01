"""sd140_kernel.py - SD-140: what the vertex-prep byte kernel does to a kind-0x54 record's +0x28 entries with the draw
parameter block's +0x40 colour, and how the three draw paths pack +0x28 / +0x2C into the emitted vertex
(SWE2-ORACLE, 2026-09-30).

Instruments over the certified image (SHA-256 73461D08...21F8, image base 0x120000):
  static   txt(addr) compares the exact capstone mnemonic + operands at every cited site (the sd102/sd120 pattern) and
           ripref(addr) the absolute target of a rip-relative operand;
  census   the published kind-0x54 census TSV (effect-mesh-54-records.tsv) as an authored-data control;
  execute  sd140_emu.py runs shipped bodies in Unicorn on controlled memory (the image's own BSS for the PS2 register
           bank 022D8F10.. and the globals). Each E-check compares the native result with a Python model over seeded
           random trials; the model is the claim, the native run is the control. Stubs are listed per check and in
           STUBS below; they return fixed values and never write the memory the check measures.
Sections: S image; A consumer + draw-path anchors (static); C census control; E execution vs model; X contradictions
with published text (reported to OPUS, not edited).
"""
import csv, hashlib, os, random, struct, sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import retool as T  # noqa: E402
import sd140_emu as U  # noqa: E402

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


def fbits(x):
    return struct.unpack("<I", struct.pack("<f", float(x)))[0]


# ---------------------------------------------------------------------------------------------------------------- S
h = hashlib.sha256(open(U.EXE, "rb").read()).hexdigest().upper()
check("S1", h.startswith("73461D08") and h.endswith("21F8"), "image %s..%s" % (h[:8], h[-4:]))

# ---------------------------------------------------------------------------------------------------------------- A
# A1 00435050 (one record): staging layout off [02AEED50] and the kernel call.
#    rdi = base + 32*c16 (screen vertices), r14 = rdi + 16*c14 (colour), r13 = r14 + 8*c18 (UV), rbp = r13 + 16*c18
#    (per-position Q, the r8 output of 0039A150); 00432300(rcx = [rec+0x28] resolved, rdx = param + 0x40, r8 = r14,
#    r9d = c18); +0x2C memcpy 8*c18 -> r13; +0x24 memcpy 16*c16 -> base
check("A1", all_txt([(0x0043506C, "movzx ebp, word ptr [rcx + 0x18]"), (0x00435073, "movzx edi, word ptr [rcx + 0x16]"),
                     (0x0043507A, "movzx r14d, word ptr [rcx + 0x14]"), (0x00435090, "shl rdi, 5"), (0x00435097, "add rdi, r12"),
                     (0x0043509A, "shl r14, 4"), (0x0043509E, "add r14, rdi"), (0x004350A1, "lea r13, [r14 + rbp*8]"),
                     (0x004350A5, "shl rbp, 4"), (0x004350A9, "add rbp, r13"), (0x0043511C, "mov r8, rbp"),
                     (0x0043511F, "mov rdx, rdi"), (0x00435122, "call 0x39a150"),
                     (0x00435197, "mov ecx, dword ptr [rsi + 0x28]"), (0x004351A6, "lea rdx, [r15 + 0x40]"),
                     (0x004351AA, "mov r9d, ebx"), (0x004351AD, "mov r8, r14"), (0x004351B0, "call 0x432300"),
                     (0x004351B5, "mov ecx, dword ptr [rsi + 0x2c]"), (0x004351C7, "shl r8, 3"), (0x004351CB, "mov rcx, r13"),
                     (0x004351CE, "call 0x861eba")]) and ripref(0x00435082) == 0x02AEED50,
      "00435050: colour = 00432300([rec+0x28], param+0x40) -> base+32*c16+16*c14; UV copy 8*c18 right after; Q after that")
# A2 00434CD0 (two records blended by w = param+0x1EC): +0x1F1 bit 4 SET -> the kernel on the current record's own
#    +0x28; CLEAR -> 00433830(cur +0x28, next +0x28, r15, c18, 1 - w) then the kernel in place (rcx = r8 = r15)
check("A2", all_txt([(0x00434D00, "mov r13, qword ptr [rdx + 0x48]"), (0x00434D08, "movss xmm6, dword ptr [rdx + 0x1ec]"),
                     (0x00434D21, "subss xmm7, xmm6"), (0x00434E97, "test byte ptr [r14 + 0x1f1], 0x10"),
                     (0x00434E9F, "je 0x434f09"), (0x00434EA1, "mov ecx, dword ptr [rbp + 0x28]"), (0x00434EB3, "jmp 0x434f40"),
                     (0x00434F09, "mov ecx, dword ptr [r13 + 0x28]"), (0x00434F16, "mov ecx, dword ptr [rbp + 0x28]"),
                     (0x00434F21, "mov rcx, rax"), (0x00434F24, "movss dword ptr [rsp + 0x20], xmm7"),
                     (0x00434F2D, "mov r8, r15"), (0x00434F30, "mov rdx, rbx"), (0x00434F33, "call 0x433830"),
                     (0x00434F3D, "mov rcx, r15"), (0x00434F40, "mov r8, r15"), (0x00434F43, "lea rdx, [r14 + 0x40]"),
                     (0x00434F47, "call 0x432300")])
      and ripref(0x00434D14) == 0x01CEBBA8 and struct.unpack("<f", R.at(0x01CEBBA8, 4))[0] == 1.0,
      "00434CD0: bit4 set -> kernel(cur +0x28); clear -> 00433830(cur, next, t = 1 - w) then kernel in place")
# A3 the three draw paths stage identically: colour r10 = base + 32*c16 + 16*c14, per-pass colour = r10 + 4*c18,
#    UV = r10 + 8*c18, UV' = UV + 8*c18, Q = UV' + 8*c18 (= 00435050's rbp)
check("A3", all_txt([(0x004356AC, "shl rax, 4"), (0x004356B9, "add rcx, rax"), (0x004356D5, "lea r14, [rax + rcx]"),
                     (0x004356DD, "add r10, r14"), (0x004356EA, "lea r9, [r10 + rax*8]"), (0x004356EE, "lea rdx, [r9 + rax*8]"),
                     (0x004356F7, "lea r13, [r10 + rax*4]"), (0x00435700, "lea rax, [rdx + rax*8]"),
                     (0x00437191, "lea r14, [rax + rcx]"), (0x00437199, "add r10, r14"), (0x004371A0, "lea r9, [r10 + rax*8]"),
                     (0x004371A4, "lea rcx, [r9 + rax*8]"), (0x004371AC, "lea rbx, [r10 + rax*4]"), (0x004371B5, "lea rax, [rcx + rax*8]"),
                     (0x0043896F, "add rax, rcx"), (0x00438976, "add r10, rax"), (0x00438989, "lea r8, [r10 + rax*8]"),
                     (0x0043898D, "lea rcx, [r8 + rax*8]"), (0x00438995, "lea r12, [r10 + rax*4]"), (0x0043899D, "lea rax, [rcx + rax*8]")])
      and ripref(0x00435699) == 0x02AEED50 and ripref(0x00437160) == 0x02AEED50 and ripref(0x00438946) == 0x02AEED50,
      "004355D0 / 00437130 / 00438860 address the prepared colour, a per-pass colour copy, UV, UV' and Q the same way")
# A4 per pass p (count param+0x1F0) the draw paths re-run the kernel: flat = kernel(param+0x40, param+0x138+4p, 1 entry)
#    broadcast to all c18 when byte param+0x1A8+p != 0; else per-vertex kernel(prepared, param+0x138+4p) unless that
#    colour is 0x80808080 (the kernel identity, E2); then 00432CC0 when byte param+0x1A4+p != 0
check("A4", all_txt([(0x0043570D, "cmp byte ptr [r15 + 0x1f0], cl"), (0x004357A6, "cmp byte ptr [r15 + rdi + 0x1a4], 0"),
                     (0x00435873, "cmp byte ptr [r15 + rdi + 0x1a8], 0"), (0x0043587E, "lea rdx, [rbx + 0x4e]"),
                     (0x0043588A, "lea rdx, [r15 + rdx*4]"), (0x0043588E, "mov r9d, ebx"), (0x00435891, "lea rcx, [r15 + 0x40]"),
                     (0x00435895, "call 0x432300"), (0x004358B0, "mov eax, dword ptr [r13]"), (0x004358B6, "mov dword ptr [rcx], eax"),
                     (0x004358DC, "cmp dword ptr [r15 + rdi*4 + 0x138], 0x80808080"), (0x004358F3, "mov rcx, qword ptr [rbp - 0x68]"),
                     (0x004358FB, "mov r8, r13"), (0x004358FE, "call 0x432300"), (0x004358C4, "mov ecx, dword ptr [rsi + 0x174]"),
                     (0x0043591C, "mov r8, qword ptr [rsp + 0x58]"), (0x00435924, "mov dword ptr [rsp + 0x28], ebx"),
                     (0x0043592B, "mov dword ptr [rsp + 0x20], edi"), (0x0043592F, "call 0x432cc0"), (0x004359E2, "mov r13, r10"),
                     (0x00438B7C, "cmp dword ptr [rbx + rdi*4 + 0x138], 0x80808080"), (0x00438B9D, "call 0x432300"),
                     (0x00438BCD, "call 0x432cc0"), (0x004373A7, "call 0x432300"), (0x004373DC, "call 0x432cc0")]),
      "per pass: flat param+0x40 x pass colour, or prepared x pass colour (skipped at 0x80808080), then 00432CC0 alpha")
# A5 untextured emit (pass mode byte param+0x130+p == 5): corners by +0x170 from the screen array r14; colour pointer
#    = pass colour + 4*k with k the running corner number (+3 per triangle, +4 per quad), not an index-list entry
check("A5", all_txt([(0x00435DA8, "movzx eax, byte ptr [r15 + rbx + 0x130]"), (0x00435DB1, "cmp al, 5"),
                     (0x00435DF2, "movaps xmm0, xmmword ptr [r14 + rcx*8]"), (0x00435E34, "lea rdx, [rax*4]"),
                     (0x00435E3C, "add rdx, r13"), (0x00435E4B, "call 0x39e820"), (0x00435E54, "add ebx, 3"),
                     (0x00435EFC, "add rdx, r13"), (0x00435F0B, "call 0x39ec30"), (0x00435F18, "add ebx, 4"),
                     (0x00435FAB, "call 0x39e6b0"), (0x0043606B, "call 0x39ea70"),
                     (0x00435790, "movzx eax, byte ptr [r15 + rdi + 0x134]"), (0x00435DBC, "cmp dword ptr [rip + 0x26b8b3d], r11d"),
                     (0x004378C8, "lea rdx, [r12 + rax*4]"), (0x004378CC, "call 0x39e820"), (0x004378D8, "add ebx, 3")])
      and ripref(0x00435799) == 0x02AEE900 and ripref(0x00435DBC) == 0x02AEE900,
      "mode 5: 0039E820 / 0039EC30 (02AEE900 = param+0x134+p != 0) or 0039E6B0 / 0039EA70 get 3 / 4 consecutive corner "
      "colours; 00437130 the same")
# A6 textured emit (mode 1): Q per corner from the Q array by position index; 0039B840(uv + 4*j, ST out, Q, offset
#    param+0x50+8p), j += 6 per triangle; then 0039F4B0(corners, ST, Q, texture slot param + 16*(prim byte + 11),
#    colours = pass colour + 4*k)
check("A6", all_txt([(0x0043608C, "cmp al, 1"), (0x00436139, "mov rax, qword ptr [rsp + 0x38]"),
                     (0x0043613E, "movss xmm0, dword ptr [rax + rcx*4]"), (0x00436172, "mov r9, r12"),
                     (0x00436199, "lea rcx, [rdi + rax*4]"), (0x0043619D, "call 0x39b840"), (0x004361AF, "movzx r9d, byte ptr [rax]"),
                     (0x004361B6, "add r9, 0xb"), (0x004361C4, "shl r9, 4"), (0x004361C8, "add r9, r15"),
                     (0x004361D3, "add rdx, r13"), (0x004361D6, "mov qword ptr [rsp + 0x20], rdx"), (0x004361E2, "call 0x39f4b0"),
                     (0x004361EF, "add dword ptr [rsp + 0x34], 3"), (0x004361F6, "add dword ptr [rsp + 0x30], 6"),
                     (0x00436363, "call 0x39b860"), (0x004363A6, "call 0x39f9f0"), (0x004363B4, "add dword ptr [rsp + 0x30], 8"),
                     (0x0043576F, "lea r12, [r15 + r12*8]"), (0x00435763, "lea r12, [rdi + 0xa]"),
                     (0x0043680C, "call 0x39f4b0"), (0x00436ACA, "call 0x39f2b0"), (0x00436C57, "call 0x39f780"),
                     (0x00435784, "add rax, 0x70"), (0x00435788, "add rax, r15"), (0x0043578B, "mov qword ptr [rsp + 0x60], rax"),
                     (0x004360A2, "mov qword ptr [rsp + 0x60], rax"), (0x004367E5, "mov r9, qword ptr [rsp + 0x60]"),
                     (0x00437C91, "call 0x39b840"), (0x00437CC0, "mov qword ptr [rsp + 0x20], rcx"), (0x00437CC9, "call 0x39f4b0")]),
      "mode 1 / other: ST = 0039B840/0039B860(corner UV, Q, pass offset); 0039F4B0/F9F0/F2B0/F780(ST, Q, texture = "
      "param+16*(prim byte+11) in mode 1, param+0x70+16p otherwise, colours); 00437130 the same")
# A7 00438860's clip path (a corner flagged zero by the projection): colour bytes -> clip-vertex float4 +0x10
#    (00431D30), UV qword -> clip-vertex +0x20, clipper 00521450, back to bytes (003AFDD0), re-projection, ST by
#    0039B880, emitted as an n-gon by 0043E440 / 0043D8F0 (colour) or 0043DB90 / 0043DF80 (textured)
check("A7", all_txt([(0x0043909B, "cmp qword ptr [rbp + 0xd0], 0"), (0x004390D5, "call 0x39e820"),
                     (0x0043926E, "lea rcx, [r12 + rax*4]"), (0x00439272, "call 0x431d30"), (0x004392AE, "call 0x521450"),
                     (0x004392EF, "call 0x3afdd0"), (0x0043932B, "call 0x39a150"), (0x00439333, "lea rdx, [rbp + 0x190]"),
                     (0x00439341, "call 0x43e440"), (0x0043B3F4, "mov qword ptr [rbp + 0x330], rax"),
                     (0x0043B510, "call 0x39b880"), (0x0043B545, "mov qword ptr [rsp + 0x20], rax"), (0x0043B551, "call 0x43db90")]),
      "00438860: unclipped corners use the same builders; clipped polygons carry colour + UV through the clipper")

# ---------------------------------------------------------------------------------------------------------------- C
tsv = os.path.join(HERE, "..", "..", "..", "17-Presentation-Rendering", "Effect-File-Formats", "members", "effect-mesh-54-records.tsv")
rows = list(csv.DictReader(open(tsv, encoding="utf-8", newline=""), delimiter="\t"))
corner = sum(1 for r in rows if int(r["c18"]) == 3 * int(r["tri"]) + 4 * int(r["quad"]))
check("C1", len(rows) == 2252 and corner == 2252 and all(int(r["c18"]) == int(r["c1A"]) for r in rows),
      "census: c18 = c1A = 3*tri + 4*quad in %d / %d records - one +0x28 / +0x2C entry per primitive corner" % (corner, len(rows)))
check("C2", min(int(r["c18"]) for r in rows) >= 1,
      "census: c18 >= 1 everywhere, so the kernels' count-0 write (E2) is unreachable from the two consumers")

# ---------------------------------------------------------------------------------------------------------------- E
E = U.Emu()
S = U.SCR
rnd = random.Random(140)


def kmodel(s, m):
    return min(255, (s * m) >> 7)


# E1 00432300: out byte c = min(255, (entry byte c * colour byte c) >> 7), c = 0..3, per entry
bad = tot = alt8 = alt255 = 0
for trial in range(60):
    n = rnd.randint(1, 24)
    src = bytes(rnd.randrange(256) for _ in range(4 * n + 4))
    blk = bytes(rnd.randrange(256) for _ in range(16))
    E.w(S, src); E.w(S + 0x10000, blk); E.w(S + 0x20000, b"\xAA" * (4 * n + 16))
    E.call(0x00432300, S, S + 0x10000, S + 0x20000, n)
    out = E.r(S + 0x20000, 4 * n + 4)
    for i in range(4 * n):
        tot += 1
        bad += out[i] != kmodel(src[i], blk[i % 4])
        alt8 += out[i] != (src[i] * blk[i % 4]) >> 8
        alt255 += out[i] != src[i] * blk[i % 4] // 255
    bad += out[4 * n:] != b"\xAA" * 4 or E.fault is not None
check("E1", bad == 0 and tot > 1000 and alt8 > tot // 4 and alt255 > tot // 4,
      "00432300 native == min(255, (e*c) >> 7) per byte on %d bytes (no stubs); the same outputs reject e*c >> 8 (%d "
      "misses) and e*c / 255 (%d misses)" % (tot, alt8, alt255))

# E2 identity, operand extent, count semantics
src = bytes(rnd.randrange(256) for _ in range(4 * 9))
E.w(S, src); E.w(S + 0x10000, b"\x80\x80\x80\x80" + bytes(rnd.randrange(256) for _ in range(12)))
E.w(S + 0x20000, b"\xAA" * 64)
E.watch = (S, S + 0x20000)
E.call(0x00432300, S, S + 0x10000, S + 0x20000, 8)
reads = sorted(set(E.reads))
ident = E.r(S + 0x20000, 32) == src[:32]
blk_reads = [(a - S - 0x10000, z) for a, z in reads if a >= S + 0x10000]
src_reads = [(a - S, z) for a, z in reads if a < S + 0x10000]
E.w(S + 0x20000, b"\xAA" * 16)
E.watch = None
E.call(0x00432300, S, S + 0x10000, S + 0x20000, 0)
zero = E.r(S + 0x20000, 8)
check("E2", ident and blk_reads == [(0, 4)] and src_reads == [(4 * i, 4) for i in range(9)]
      and zero[:4] == src[:4] and zero[4:] == b"\xAA" * 4,
      "0x80808080 is the identity; only dword [rdx] is read; n+1 entries read (prefetch past the end); count 0 writes one")


# E3 00433830: out = trunc(a*t + 0.5 + b*(1 - t)) per byte, a = rcx entries, b = rdx entries, t = 5th argument (float)
def bmodel(a, b, t):
    t = f32(t)
    return max(0, min(255, int(f32(f32(f32(a) * t) + f32(0.5)) + f32(f32(b) * f32(f32(1.0) - t)))))


bad = tot = altt = 0
for trial in range(60):
    n = rnd.randint(1, 16)
    a = bytes(rnd.randrange(256) for _ in range(4 * n + 4))
    b = bytes(rnd.randrange(256) for _ in range(4 * n + 4))
    t = rnd.choice([0.0, 1.0, 0.5, 0.25, rnd.random(), rnd.random()])
    E.w(S, a); E.w(S + 0x10000, b); E.w(S + 0x20000, b"\xAA" * (4 * n + 16))
    E.call(0x00433830, S, S + 0x10000, S + 0x20000, n, stack_args=(fbits(t),))
    out = E.r(S + 0x20000, 4 * n + 4)
    for i in range(4 * n):
        tot += 1
        bad += out[i] != bmodel(a[i], b[i], t)
        altt += out[i] != int(f32(f32(a[i]) * f32(t)) + f32(f32(b[i]) * f32(f32(1.0) - f32(t))))
    bad += out[4 * n:] != b"\xAA" * 4 or E.fault is not None
check("E3", bad == 0 and tot > 1000 and altt > 100,
      "00433830 native == round-half-up lerp trunc(a*t + 0.5 + b*(1-t)) on %d bytes (no stubs; the unbiased trunc "
      "misses %d); with A2's operands that is cur*(1-w) + next*w" % (tot, altt))

# E4 00432CC0(src, dst, table, +0x174 list, n, m): RGB copied; A = trunc(A * table[key].w) & 0xFF, key = list[i] mod m
#    (entry 0's key is used unreduced - Q1); the table is the per-normal float4 array at base + 16*c16
bad = tot = 0
for trial in range(40):
    n = rnd.randint(1, 16); m = rnd.randint(1, 6)
    src = bytes(rnd.randrange(256) for _ in range(4 * n + 4))
    lit = [f32(rnd.uniform(0, 1.99)) for _ in range(4 * m)]
    lst = [rnd.randrange(m) for _ in range(n + 1)]
    E.w(S, src); E.w(S + 0x1000, b"\xAA" * (4 * n + 16)); E.w(S + 0x2000, struct.pack("<%df" % (4 * m), *lit))
    E.w(S + 0x3000, struct.pack("<%dH" % (n + 1), *lst))
    E.call(0x00432CC0, S, S + 0x1000, S + 0x2000, S + 0x3000, stack_args=(n, m))
    out = E.r(S + 0x1000, 4 * n + 4)
    for i in range(n):
        k = lst[i] % m
        want = list(src[4 * i:4 * i + 3]) + [int(f32(src[4 * i + 3]) * lit[4 * k + 3]) & 0xFF]
        tot += 4
        bad += list(out[4 * i:4 * i + 4]) != want
    bad += out[4 * n:] != b"\xAA" * 4 or E.fault is not None
check("E4", bad == 0 and tot > 300, "00432CC0 native: RGB unchanged, alpha = trunc(alpha * L[normal index].w) mod 256 (%d bytes)" % tot)

# E5 0039B840 / 0039B860: ST_i = (uv_i + offset) * Q_i for 3 / 4 corners (no stubs)
bad = 0
for trial in range(40):
    n = rnd.choice([3, 4])
    uv = [f32(rnd.uniform(-2, 3)) for _ in range(2 * n)]
    q = [f32(rnd.uniform(0.01, 4)) for _ in range(n)]
    of = [f32(rnd.uniform(-1, 1)) for _ in range(2)]
    E.w(S, struct.pack("<%df" % (2 * n), *uv)); E.w(S + 0x100, struct.pack("<%df" % n, *q)); E.w(S + 0x200, struct.pack("<2f", *of))
    E.call(0x0039B840 if n == 3 else 0x0039B860, S, S + 0x300, S + 0x100, S + 0x200)
    got = struct.unpack("<%df" % (2 * n), E.r(S + 0x300, 8 * n))
    bad += any(f32(got[2 * i + k]) != f32(f32(uv[2 * i + k] + of[k]) * q[i]) for i in range(n) for k in range(2))
    bad += E.fault is not None
check("E5", bad == 0, "0039B840/0039B860 native: S,T = (u + ou) * Q, (v + ov) * Q per corner - the GS STQ form")

# E6 the ten builders. STUBS (disclosed): 0020E680 -> a context pointer; 008642A0 -> a primitive whose +0 / +8 / +0x10
#    point at three 16-B-per-vertex arrays (the layout 00864210 allocates); 00864D10 -> a 0x100-B quad object (vertices
#    +0, UV +0x40, colour +0x80, the layout 0039F9F0 addresses); 0039CDC0 (GS XYZ -> float position), 0020E670,
#    0020E630, 00182F50 -> return; 0024E460 / 003A3D20 / 003A2C70 -> 0. The stubs do not touch the UV / colour arrays.
CTX, P, VTX, UVB, COLB, SLOT, OBJ = S + 0x1000, S + 0x2000, S + 0x3000, S + 0x4000, S + 0x5000, S + 0x6000, S + 0x8000
E.q(P, VTX); E.q(P + 8, UVB); E.q(P + 0x10, COLB); E.q(0x02F8F2F8, SLOT)
E.stub(0x0020E680, "ctx", lambda e: CTX)
E.stub(0x008642A0, "prim", lambda e: P)
E.stub(0x00864D10, "quadobj", lambda e: OBJ)
for a, nm in ((0x0039CDC0, "xyz"), (0x0020E670, "rel"), (0x0020E630, "free"), (0x00182F50, "submit")):
    E.stub(a, nm)
for a, nm in ((0x0024E460, "g1"), (0x003A3D20, "g2"), (0x003A2C70, "g3")):
    E.stub(a, nm, lambda e: 0)
VIN, ST, Q, TEX, COL = S, S + 0x100, S + 0x200, S + 0x300, S + 0x400
builders = [(0x0039E820, 3, "c"), (0x0039EC30, 4, "c"), (0x0039E6B0, 3, "c"), (0x0039EA70, 4, "c"),
            (0x0039F4B0, 3, "t"), (0x0039F9F0, 4, "t"), (0x0039F2B0, 3, "t"), (0x0039F780, 4, "t"),
            (0x0043D8F0, 0, "cn"), (0x0043E440, 0, "cn"), (0x0043DB90, 0, "tn"), (0x0043DF80, 0, "tn")]
bad = runs = 0
for fn, n0, kind in builders:
    for trial in range(6):
        n = n0 or rnd.randint(3, 9)
        st = [f32(rnd.uniform(-4, 4)) for _ in range(2 * n)]
        q = [f32(rnd.uniform(0.05, 3)) for _ in range(n)]
        col = bytes(rnd.randrange(256) for _ in range(4 * n))
        E.w(VIN, bytes(16 * n)); E.w(ST, struct.pack("<%df" % (2 * n), *st)); E.w(Q, struct.pack("<%df" % n, *q))
        E.w(COL, col); E.w(TEX, struct.pack("<QQ", 0x1111, 0x2222))
        for b in (UVB, COLB, OBJ):
            E.w(b, b"\0" * 0x100)
        E.w(0x02F8F2C6, b"\0\0")
        if kind == "c":
            E.call(fn, VIN, COL)
        elif kind == "cn":
            E.call(fn, VIN, COL, n)
        elif kind == "t":
            E.call(fn, VIN, ST, Q, TEX, stack_args=(COL,))
        else:
            E.call(fn, VIN, ST, Q, TEX, stack_args=(COL, n))
        quad = any(c[0] == "quadobj" for c in E.calls)
        uvb, colb = (OBJ + 0x40, OBJ + 0x80) if quad else (UVB, COLB)
        gc = struct.unpack("<%df" % (4 * n), E.r(colb, 16 * n))
        ok = E.fault is None and all(gc[i] == float(col[i]) for i in range(4 * n))
        if kind in ("t", "tn"):
            gu = struct.unpack("<%df" % (4 * n), E.r(uvb, 16 * n))
            ok = ok and all(f32(gu[4 * i + k]) == f32(st[2 * i + k] / q[i]) for i in range(n) for k in range(2))
        runs += 1
        bad += not ok
check("E6", bad == 0 and runs == 6 * len(builders),
      "12 builders native (stubs disclosed): colour lane c = float(byte c) unscaled, 16 B per vertex; textured: U,V = S/Q, T/Q")

# E7 the chain for one textured triangle: 0039B840 then 0039F4B0 on its output returns u + ou, v + ov to within the
#    float round trip (x*Q)/Q - the emitted UV is the prepared +0x2C pair plus the pass offset, never texel-scaled
worst = 0.0
bad = 0
for trial in range(40):
    uv = [f32(rnd.uniform(-2, 3)) for _ in range(6)]
    q = [f32(rnd.uniform(0.05, 4)) for _ in range(3)]
    of = [f32(rnd.uniform(-1, 1)) for _ in range(2)]
    E.w(S + 0x500, struct.pack("<6f", *uv)); E.w(Q, struct.pack("<3f", *q)); E.w(S + 0x600, struct.pack("<2f", *of))
    E.call(0x0039B840, S + 0x500, ST, Q, S + 0x600)
    E.w(0x02F8F2C6, b"\0\0")
    E.call(0x0039F4B0, VIN, ST, Q, TEX, stack_args=(COL,))
    gu = struct.unpack("<12f", E.r(UVB, 48))
    for i in range(3):
        for k in range(2):
            d = abs(gu[4 * i + k] - float(uv[2 * i + k] + of[k]))
            worst = max(worst, d)
    bad += E.fault is not None
check("E7", bad == 0 and worst < 1e-5, "chain 0039B840 -> 0039F4B0: emitted UV = +0x2C pair + pass offset (max error %.2e)" % worst)

# E8 the clip-path colour carriers: 00431D30 byte -> float (unscaled), 003AFDD0 float -> byte by truncation (low byte)
bad = 0
for trial in range(60):
    c = bytes(rnd.randrange(256) for _ in range(4))
    E.w(S, c); E.w(S + 0x100, bytes(16))
    E.call(0x00431D30, S, S + 0x100)
    bad += list(struct.unpack("<4f", E.r(S + 0x100, 16))) != [float(x) for x in c]
    fv = [f32(rnd.uniform(0, 255.99)) for _ in range(4)]
    E.w(S, struct.pack("<4f", *fv)); E.w(S + 0x100, b"\xAA" * 8)
    E.call(0x003AFDD0, S, S + 0x100)
    bad += list(E.r(S + 0x100, 4)) != [int(x) for x in fv] or E.r(S + 0x104, 4) != b"\xAA" * 4
E.w(S, struct.pack("<4f", 300.0, -5.0, 256.0, 255.9)); E.call(0x003AFDD0, S, S + 0x100)
wrap = E.r(S + 0x100, 4) == bytes([300 & 0xFF, (-5) & 0xFF, 0, 255])
check("E8", bad == 0 and wrap and E.fault is None,
      "00431D30 / 003AFDD0 native: clip vertices carry colour as float(byte); packed back by truncation, low byte (no clamp)")

# ---------------------------------------------------------------------------------------------------------------- Q
# Q1 00432CC0 keys entry 0 by list[0] without the mod-m reduction the loop applies (positive control: a list[0] >= m
#    makes entry 0 read past the table while the model with the reduction disagrees)
E.w(S, bytes([10, 20, 30, 200]) * 2); E.w(S + 0x2000, struct.pack("<8f", 1, 1, 1, 0.5, 1, 1, 1, 0.25))
E.w(S + 0x3000, struct.pack("<3H", 1, 1, 0))
E.call(0x00432CC0, S, S + 0x1000, S + 0x2000, S + 0x3000, stack_args=(2, 1))
o = E.r(S + 0x1000, 8)
check("Q1", o[3] == 50 and o[7] == 100 and o[:3] == bytes([10, 20, 30]),
      "00432CC0 entry 0 uses table[list[0]] unreduced (alpha 200*0.25 = %d; reduced would give 100); later entries reduce mod m" % o[3])

# ---------------------------------------------------------------------------------------------------------------- X
# X1 the-two-transform-primitives.md (00434CD0 subtree) says "Bit 4 sends the +0x28 sections through 00433830",
#    "Bit 5 sends +0x2C through 004344C0 ... clear -> a plain 00861EBA copy", "Bit 6 sends +0x24 through 00432030 ...
#    clear -> 00861EBA": each branch is taken when the bit is CLEAR (je after test) - the polarity is inverted
check("X1", all_txt([(0x00434E97, "test byte ptr [r14 + 0x1f1], 0x10"), (0x00434E9F, "je 0x434f09"),
                     (0x00434F4C, "test byte ptr [r14 + 0x1f1], 0x20"), (0x00434F54, "je 0x434f7b"), (0x00434FAA, "call 0x4344c0"),
                     (0x00434F74, "call 0x861eba"), (0x00434FAF, "test byte ptr [r14 + 0x1f1], 0x40"), (0x00434FB7, "je 0x434fde"),
                     (0x0043500D, "call 0x432030"), (0x00434FD7, "call 0x861eba")]),
      "00434CD0: bits 4/5/6 SET select the copy / no blend; the blend helpers run when the bit is clear (page inverted)")
# X2 the same page calls 00432300 "pure staging ... no external calls" - it writes one packed dword per entry to [r8]
check("X2", all_txt([(0x00432A4E, "sar eax, 7"), (0x00432A51, "and eax, 0x1ffffff"), (0x00432C89, "mov dword ptr [r8], eax"),
                     (0x00432C8C, "add edx, 4"), (0x00432C9C, "test r9d, r9d"), (0x00432C9F, "jle 0x432cb1")]),
      "00432300 is the modulate kernel: >>7, clamp, one dword stored per entry at [r8] (not pure staging)")
# X3 the page reads 0043DB90 / 0043E440 as record-walk "field math" helpers and 0043D8F0 as an authored-number
#    channel converter: all three allocate a primitive through 008642A0 and fill its UV / colour arrays (E6)
check("X3", all_txt([(0x0043DBC4, "call 0x8642a0"), (0x0043E524, "call 0x8642a0"), (0x0043D920, "call 0x8642a0"),
                     (0x0043DB4D, "mov qword ptr [rsi + 0x40], 5")]),
      "0043D8F0 / 0043E440 / 0043DB90 (and 0043DF80) are n-gon primitive builders for 00438860's clipped polygons")
# X4 page section 8 names the kernel's second operand "the element's +0x40 block": it is the draw parameter block
#    ([01FD4A78] + 0x800, rdx of 004355D0) whose +0x40 0026EE00 writes from the element instance's +0x240
check("X4", all_txt([(0x00449AC5, "add rdi, 0x800"), (0x00449B4C, "lea rdx, [r15 + 0x240]"), (0x00449B53, "lea rcx, [rdi + 0x40]"),
                     (0x00449B5F, "call 0x26ee00"), (0x0044A158, "mov rdx, rdi"), (0x0044A15B, "call 0x4355d0")])
      and ripref(0x00449ABB) == 0x01FD4A78,
      "the +0x40 colour is param[+0x40] = 0026EE00(instance +0x240, ...), param = [01FD4A78] + 0x800 (a precision, not a code conflict)")

print("RESULT the +0x28 entries are per-corner RGBA8 vertex colours (0x80 = 1.0): 00432300 modulates each byte by the "
      "draw parameter block's +0x40 colour, min(255, e*c >> 7), after 00433830's rounded lerp when two meshes blend; per "
      "pass the paths modulate again by the pass colour (+ optional alpha x per-normal w) and every builder emits the four "
      "bytes as float lanes 0..255. The +0x2C pairs are per-corner texture coordinates: copied or lerped as floats, offset "
      "per pass, sent as GS STQ (S = (u+ou)*Q) and turned back into U = S/Q by the textured builders")
print("CHECKS %d" % checks)
print("FAILS %d" % fails)
