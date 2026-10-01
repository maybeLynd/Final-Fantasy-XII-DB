"""sd120_ops.py - SD-120: what each of the eight 0050xxxx binding operations does (SWE2-ORACLE, 2026-09-30).

Two instruments over the certified image (SHA-256 73461D08...21F8, image base 0x120000):
  static   txt(addr) compares the exact capstone mnemonic + operands at every cited site (the sd102 pattern), and
           ripref(addr) the absolute target of a rip-relative operand;
  execute  sd120_emu.py runs the shipped operation bodies in Unicorn on controlled memory (the image's own BSS
           buffers 02B477A0 / 02B487A0 / 02B497A0, a scratch record page). Bridged calls: VCRUNTIME140 memcpy
           (00861EBA, done in Python) and __chkstk (00808F10, returned). Everything else is the shipped code.
           Each M-check compares the native result with a Python model over seeded random trials; the model is the
           claim, the native run is the control. One harness instance is reused across trials (the PS2 register bank
           022D8F10.. carries over between calls; GPR[0] 022D8F10 is never written).
Sections: S image; D dispatcher arguments and record time fields; P per-operation anchors; M models; K codec and
curve controls; Q quirks (positive controls); X contradictions with published text (reported, not edited).
"""
import hashlib, os, random, struct, sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import retool as T  # noqa: E402
import sd120_emu as U  # noqa: E402
from unicorn.x86_const import UC_X86_REG_XMM0, UC_X86_REG_XMM1  # noqa: E402

R = T.R
fails = 0


def check(tag, ok, text):
    global fails
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


I32 = lambda x: max(-2 ** 31, min(2 ** 31 - 1, x))


def s16(x):
    x &= 0xFFFF
    return x - 0x10000 if x & 0x8000 else x


# ---------------------------------------------------------------------------------------------------------------- S
h = hashlib.sha256(open(U.EXE, "rb").read()).hexdigest().upper()
check("S1", h.startswith("73461D08") and h.endswith("21F8"), "image %s..%s" % (h[:8], h[-4:]))

# ---------------------------------------------------------------------------------------------------------------- D
# D1 003CCF20 passes (rcx = working buffer 02B477A0, rdx = the operation record) to ops 1,2,3,5,6,7
arms = {1: (0x003CD103, 0x003CD106, 0x003CD10D, "call 0x50ac20"), 2: (0x003CD117, 0x003CD11A, 0x003CD121, "call 0x506b40"),
        3: (0x003CD12B, 0x003CD12E, 0x003CD135, "call 0x5080a0"), 5: (0x003CD19F, 0x003CD1A2, 0x003CD1A9, "call 0x509bb0"),
        6: (0x003CD1B0, 0x003CD1B3, 0x003CD1BA, "call 0x507490"), 7: (0x003CD1C1, 0x003CD1C4, 0x003CD1CB, "call 0x508c90")}
check("D1", all(txt(a) == "mov rdx, rbx" and txt(b).startswith("lea rcx, [rip") and ripref(b) == U.A and txt(c) == e
                for a, b, c, e in arms.values()),
      "ops 1,2,3,5,6,7 get (rcx = 02B477A0 working buffer, rdx = record rbx)")
# D2 opcodes 4 and 8: source handle = record +0x20 into the 32 x 64 B handle table 02B47790, generation-checked;
#    its +0x10 (raw, or through 0036B130 when entry +1 & 0x3F) is decoded by 003CD840 with the entry's word +2 into
#    02B487A0 (op 4) / 02B497A0 (op 8); then (rcx = 02B477A0, rdx = that buffer, r8 = record)
check("D2", all_txt([(0x003CD13F, "mov ecx, dword ptr [rbx + 0x20]"), (0x003CD142, "movzx edi, cl"), (0x003CD145, "shl rdi, 6"),
                     (0x003CD150, "cmp dword ptr [rdi + 4], ecx"), (0x003CD159, "test byte ptr [rdi + 1], 0x3f"),
                     (0x003CD15F, "mov rsi, qword ptr [rdi + 0x10]"), (0x003CD165, "mov ecx, dword ptr [rdi + 0x10]"),
                     (0x003CD168, "call 0x36b130"), (0x003CD170, "movzx r8d, word ptr [rdi + 2]"), (0x003CD17F, "call 0x3cd840"),
                     (0x003CD184, "mov r8, rbx"), (0x003CD195, "call 0x50a100"),
                     (0x003CD1D2, "mov ecx, dword ptr [rbx + 0x20]"), (0x003CD1E3, "cmp dword ptr [rdi + 4], ecx"),
                     (0x003CD1FF, "movzx r8d, word ptr [rdi + 2]"), (0x003CD20E, "call 0x3cd840"), (0x003CD213, "mov r8, rbx"),
                     (0x003CD224, "call 0x507120")])
      and ripref(0x003CD149) == 0x02B47790 and ripref(0x003CD175) == U.B and ripref(0x003CD187) == U.B
      and ripref(0x003CD18E) == U.A and ripref(0x003CD204) == U.C and ripref(0x003CD216) == U.C and ripref(0x003CD21D) == U.A,
      "ops 4 / 8 get (02B477A0, a second CLUT decoded from the handle at record +0x20 into 02B487A0 / 02B497A0, record)")
# D3 the entry frame around the operations: entry +8 decoded into 02B477A0 before the list, entry +0x10 re-encoded
#    from it by 003D2B60 after the list (both with the entry's word +2)
check("D3", all_txt([(0x003CCF9C, "mov rsi, qword ptr [rbp + 8]"), (0x003CCFAF, "movzx r8d, word ptr [rbp + 2]"),
                     (0x003CCFBE, "call 0x3cd840"), (0x003CD244, "mov rax, qword ptr [rbp + 0x10]"),
                     (0x003CD252, "movzx r8d, word ptr [rbp + 2]"), (0x003CD261, "call 0x3d2b60")])
      and ripref(0x003CCFB4) == U.A and ripref(0x003CD257) == U.A,
      "per entry: 003CD840(entry+8 -> 02B477A0, n = word +2); ops; 003D2B60(02B477A0 -> entry+0x10, n)")
# D4 record time fields the operations consume: +0xA start delay (counted down by the dt argument r14), +0x34
#    elapsed, +8 lifetime (expired record released inline and unlinked), +0x10 loop length with +0x15 = 0 wrap / 1
#    ping-pong, giving +0x36 = the local time every operation reads; +0 = opcode
check("D4", all_txt([(0x003CCF2F, "mov r14d, ecx"), (0x003CCFD0, "movzx eax, word ptr [rbx + 0xa]"), (0x003CCFD9, "sub ax, r14w"),
                     (0x003CCFEA, "mov word ptr [rbx + 0x34], ax"), (0x003CCFF5, "add word ptr [rbx + 0x34], r14w"),
                     (0x003CCFFA, "movzx eax, word ptr [rbx + 8]"), (0x003CD003, "cmp ax, word ptr [rbx + 0x34]"),
                     (0x003CD009, "mov edx, dword ptr [rbx + 0x30]"), (0x003CD028, "mov dword ptr [r8 + 0x30], r15d"),
                     (0x003CD042, "dec byte ptr [rcx]"), (0x003CD07A, "movzx r8d, word ptr [rbx + 0x10]"),
                     (0x003CD085, "movzx ecx, byte ptr [rbx + 0x15]"), (0x003CD0CF, "mov word ptr [rbx + 0x36], dx"),
                     (0x003CD0B0, "mov word ptr [rbx + 0x36], r9w"), (0x003CD0BD, "sub ax, r9w"),
                     (0x003CD0D9, "mov word ptr [rbx + 0x36], ax"), (0x003CD0E6, "movzx eax, byte ptr [rbx]")]),
      "+0xA delay, +0x34 elapsed, +8 lifetime -> release, +0x10/+0x15 loop -> +0x36 local time, +0 opcode")
# D5 003CD2C0 (one binding by handle, immediately) runs the same eight on its own buffers 02B4A7A0 / 02B4B7A0 / 02B4C7A0
check("D5", ripref(0x003CD30E) == 0x02B4A7A0 and ripref(0x003CD468) == 0x02B4B7A0 and ripref(0x003CD4F4) == 0x02B4C7A0
      and txt(0x003CD403) == "call 0x50ac20" and txt(0x003CD488) == "call 0x50a100" and txt(0x003CD514) == "call 0x507120"
      and txt(0x003CD565) == "jmp 0x3d2b60" and txt(0x003CD370) == "call 0x3cd650",
      "003CD2C0: same ops on 02B4A7A0 (+ 02B4B7A0 / 02B4C7A0 for ops 4 / 8), expired records released by 003CD650")
# D6 the expression path 00431B10 builds a record on its stack (rbp-0x60) from a 16-byte authored item and calls six
#    of the eight on buffer 02CA4EE0; its kind table has 7 entries, kind 4 returns 0 (no two-source blend there)
kt = [0x120000 + struct.unpack("<I", R.at(0x00431D14 + 4 * k, 4))[0] for k in range(7)]
check("D6", all_txt([(0x00431B49, "call 0x3cd840"), (0x00431B54, "call 0x4314e0"), (0x00431B5D, "mov word ptr [rbp - 0x2a], ax"),
                     (0x00431B6B, "mov byte ptr [rbp - 0x5d], 0xff"), (0x00431B6F, "mov word ptr [rbp - 0x4e], si"),
                     (0x00431B83, "mov byte ptr [rbp - 0x4c], 1"), (0x00431B90, "cmp eax, 6"),
                     (0x00431BCA, "call 0x50ac20"), (0x00431C0B, "call 0x506b40"), (0x00431C4B, "call 0x5080a0"),
                     (0x00431C69, "call 0x509bb0"), (0x00431CA0, "call 0x507490"), (0x00431CDD, "call 0x508c90"),
                     (0x00431CEE, "call 0x3a9c10")])
      and ripref(0x00431B39) == 0x02CA4EE0 and kt == [0x431BAF, 0x431BD4, 0x431C15, 0x431CF5, 0x431C55, 0x431C70, 0x431CA7],
      "00431B10: record +0x36 = 004314E0 time, +3 = 0xFF, +0x12 = count, kinds 1,2,3,5,6,7 -> ops 1,2,3,5,6,7; kind 4 -> none")

# ---------------------------------------------------------------------------------------------------------------- P
# common prologue: t = word +0x36 / word +0xE (when +0xE != 0), channel mask from byte +3 bits 0-3 (sbb masks)
check("P0", all_txt([(0x0050AC51, "movzx ecx, word ptr [rdx + 0xe]"), (0x0050AC5A, "movzx eax, word ptr [rdx + 0x36]"),
                     (0x00506B4F, "movzx edx, word ptr [rdx + 0xe]"), (0x005080B3, "movzx ecx, word ptr [rdx + 0xe]"),
                     (0x0050A113, "movzx r8d, word ptr [r8 + 0xe]"), (0x00509BBF, "movzx edx, word ptr [rdx + 0xe]"),
                     (0x005074B1, "movzx edx, word ptr [rdx + 0xe]"), (0x00508CA9, "movzx ecx, word ptr [rdx + 0xe]"),
                     (0x00507128, "movzx r9d, word ptr [r8 + 0xe]"), (0x00507139, "movzx eax, word ptr [r8 + 0x36]"),
                     (0x00507144, "div r9d"), (0x00507151, "movzx ecx, byte ptr [r8 + 3]"),
                     (0x00507156, "movzx esi, word ptr [r8 + 0x12]"), (0x00507199, "movzx eax, byte ptr [r8 + 0x14]")]),
      "all eight: t = +0x36 / +0xE, mask = +3 bits 0-3, entries [+0x14, +0x14 + +0x12) of 16 B")
check("P1", all_txt([(0x0050AC32, "call 0x808f10"), (0x0050AC75, "movsx eax, word ptr [rbx + 0x20]"), (0x0050AC79, "imul r9d, eax"),
                     (0x0050ACD5, "movzx ecx, byte ptr [rbx + 0x22]"), (0x0050ACE5, "je 0x50beb3"), (0x0050ACEE, "je 0x50b7e1"),
                     (0x0050ACF7, "jne 0x50c41d"), (0x0050BEB3, "movzx esi, word ptr [rbx + 0x12]"), (0x0050BEBB, "idiv esi"),
                     (0x0050B807, "cmp r9d, r10d"), (0x0050AD05, "lea ecx, [rsi + rsi]"), (0x0050AD08, "idiv ecx"),
                     (0x0050AD1D, "cmp edx, esi"), (0x0050B274, "cmp edi, esi"), (0x0050B276, "jge 0x50b509"),
                     (0x0050AD18, "lea rcx, [rsp + 0x60]"), (0x0050AD36, "call 0x861eba")]),
      "op1 0050AC20: shift = t * s16 +0x20; mode +0x22: 0 rotate (mod n), 1 clamped shift, 2 mirror (mod 2n); memcpy via a stack copy")
check("P2", all_txt([(0x00506B80, "movzx eax, word ptr [r9 + 0x28]"), (0x00506B90, "cmovge r8d, eax"),
                     (0x00506BDA, "movzx ecx, byte ptr [r9 + 0x2a]"), (0x00506BE6, "je 0x506f7e"), (0x00506BEF, "jne 0x507103"),
                     (0x00506BF5, "movsx eax, word ptr [r9 + 0x20]"), (0x00506C25, "movsx eax, word ptr [r9 + 0x26]"),
                     (0x00506CD9, "sar eax, 8"), (0x00506D7B, "sar r11d, 7"), (0x00506D8A, "and r11d, 0x1ffffff"),
                     (0x00506F8F, "mov eax, 0xff"), (0x00506F9A, "cmovge r8d, eax"), (0x00507036, "call 0x506a40"),
                     (0x0050704A, "mov eax, 8"), (0x00507069, "pslld xmm1, xmm0"), (0x0050706D, "pand xmm1, xmm2")]),
      "op2 00506B40: t capped by +0x28; s16 x4 vector +0x20..+0x26; mode +0x2A: 0 additive (t <= 255, 00506A40 product, << 8), 1 proportional (>>8, *v >>7)")
check("P3", all_txt([(0x00508109, "movsxd rax, dword ptr [r9 + 0x20]"), (0x00508305, "movzx edx, byte ptr [r9 + 0x26]"),
                     (0x0050832B, "je 0x5086d0"), (0x00508334, "jne 0x508c7d"), (0x0050833A, "movzx r10d, word ptr [r9 + 0x24]"),
                     (0x0050833F, "cmp r8d, r10d"), (0x0050843A, "shl r8d, 8"), (0x00508442, "idiv r10d"),
                     (0x005086D7, "cmp r8d, 0xff")]),
      "op3 005080A0: target colour RGBA8 dword +0x20; mode +0x26: 1 crossfade over +0x24 frames, 0 fixed-step approach (copy at t >= 255)")
check("P4", all_txt([(0x0050A16A, "je 0x50ac14"), (0x0050A1B2, "movzx edx, byte ptr [r9 + 0x26]"), (0x0050A1E5, "je 0x50a5ee"),
                     (0x0050A1EE, "jne 0x50ac0a"), (0x0050A1F4, "movzx r9d, word ptr [r9 + 0x24]"), (0x0050A1F9, "cmp r8d, r9d"),
                     (0x0050A330, "shl r8d, 8"), (0x0050A338, "idiv r9d"), (0x0050A5EE, "cmp r8d, 0xff"),
                     (0x0050A79F, "mov eax, 8"), (0x0050A7BA, "movd xmm5, eax")]),
      "op4 0050A100: the same two modes as op3 with the second decoded CLUT as the per-entry target")
check("P5", all_txt([(0x00509BF3, "and dl, 7"), (0x00509C3C, "movzx ecx, word ptr [r11 + 0x20]"), (0x00509C59, "cmp r8d, ecx"),
                     (0x0050A021, "shl r8d, 8"), (0x0050A02E, "idiv ecx"), (0x0050A07B, "imul ecx, ecx, 0x96"),
                     (0x0050A081, "imul r8d, eax, 0x1d"), (0x0050A09B, "imul edx, edx, 0x4d")])
      and ripref(0x00509C82) == 0x00D22850 and struct.unpack("<4i", R.at(0x00D22850, 16)) == (77, 150, 29, 0),
      "op5 00509BB0: luma weights (77, 150, 29) / 256 at 00D22850; duration word +0x20; lanes 0-2 only")
check("P6", all_txt([(0x005074DA, "movups xmm2, xmmword ptr [rbx + 0x23]"), (0x005074DE, "mov rax, qword ptr [rbx + 0x23]"),
                     (0x00507554, "movsxd rax, dword ptr [rbx + 0x20]"), (0x005077E0, "mov edi, 0x80"), (0x00507801, "sub rdi, rax"),
                     (0x00507821, "and dl, 7"), (0x00507859, "movzx ecx, word ptr [rbx + 0x24]"), (0x00507877, "cmp r10d, ecx"),
                     (0x0050794E, "sar eax, 7"), (0x00507951, "and eax, 0x1ffffff"), (0x00507BAB, "shl r10d, 8"),
                     (0x00507BBF, "idiv ecx"), (0x0050807F, "call 0x808c40")]),
      "op6 00507490: tint colour +0x20..+0x22, strength = the halfword at +0x23 (0x80 = 1.0), duration word +0x24; lanes 0-2")
check("P7", all_txt([(0x00508CD2, "movsx eax, word ptr [r9 + 0x24]"), (0x00508CE6, "imul r8d, eax"),
                     (0x00508CEA, "movsxd rax, dword ptr [r9 + 0x20]"), (0x00508EAB, "movzx ebx, byte ptr [r9 + 0x26]"),
                     (0x00508EF6, "test r8d, r8d"), (0x00508EF9, "jle 0x50952b"), (0x00508F07, "sub eax, ebx"),
                     (0x0050903C, "divss xmm1, xmm0"), (0x005091CD, "pand xmm1, xmm3"), (0x005092AA, "cvttps2dq xmm1, xmm0"),
                     (0x0050952B, "jns 0x509b76"), (0x005096BF, "sub r11d, eax"), (0x005096C5, "add r11d, r8d")])
      and ripref(0x00509023) == 0x00915A00 and struct.unpack("<f", R.at(0x00915A00, 4))[0] == 256.0
      and ripref(0x005091C6) == 0x022D92F0 and ripref(0x00509200) == 0x022D92F0,
      "op7 00508C90: head = t * s16 +0x24, colour +0x20, ramp width byte +0x26 (256.0 / width, float), the unmasked step kept at 022D92F0")
check("P8", all_txt([(0x0050718F, "mov rcx, qword ptr [r8 + 0x28]"), (0x005071B3, "call 0x53db50"),
                     (0x005071DC, "cvttss2si eax, xmm0"), (0x005072E2, "psrad xmm0, xmm3")])
      and ripref(0x005071B8) == 0x00915A00,
      "op8 00507120: weight = (int)(256 * curve(t)), curve = the key table at qword +0x28 through 0053DB50")

# ---------------------------------------------------------------------------------------------------------------- M
E = U.Emu()
REC = U.REC


def newrec(kv):
    raw = bytearray(0x100)
    for off, (fmt, v) in kv.items():
        struct.pack_into("<" + fmt, raw, off, v)
    return raw


def run(fn, raw, *args):
    E.mu.mem_write(REC, bytes(raw))
    E.call(fn, *args)


def rows8(rnd):
    return [[rnd.randrange(0, 256) << 8 for _ in range(4)] for _ in range(256)]


def lerp(a, target, w, mask, lo, n):
    out = [r[:] for r in a]
    for i in range(lo, lo + n):
        for c in range(4):
            wc = w if mask >> c & 1 else 0
            out[i][c] = I32(a[i][c] + s16(I32(target[i][c] - a[i][c]) >> 8) * s16(wc))
    return out


def approach(a, target, t, mask, lo, n):
    out = [r[:] for r in a]
    for i in range(lo, lo + n):
        for c in range(4):
            if not mask >> c & 1:
                continue
            if t >= 255:
                out[i][c] = target[i][c]
                continue
            d, s = target[i][c] - a[i][c], t << 8
            out[i][c] = a[i][c] + (min(s, d) if d > 0 else max(-s, d) if d < 0 else 0)
    return out


def crossfade(a, target, t, dur, mask, lo, n):
    if t >= dur:
        out = [r[:] for r in a]
        for i in range(lo, lo + n):
            for c in range(4):
                if mask >> c & 1:
                    out[i][c] = target[i][c]
        return out
    return lerp(a, target, (t << 8) // dur, mask, lo, n)


def m_trials(tag, n_trials, seed, body, text):
    rnd, bad = random.Random(seed), 0
    for k in range(n_trials):
        got, exp, info = body(rnd, k)
        if got != exp:
            bad += 1
            if bad <= 2:
                print("      %s trial %d mismatch %s" % (tag, k, info))
    check(tag, bad == 0, "%s (%d/%d trials exact)" % (text, n_trials - bad, n_trials))


# M1 op1: new[k] = old[src(k)] over the range, masked lanes only; s = t * speed
def src1(mode, k, s, n):
    if mode == 0:
        return (k - s) % n
    if mode == 1:
        return min(max(k - s, 0), n - 1)
    r = abs(s) % (2 * n) * (1 if s >= 0 else -1)          # C remainder (0050AD08 idiv)
    if r <= -n:
        return abs(k - (2 * n + r - 1))                  # 0050B509 arm
    j = (k - r) % (2 * n)
    return j if j < n else 2 * n - 1 - j


def b1(rnd, k):
    mode = k % 4
    a = [[rnd.randrange(-2 ** 20, 2 ** 20) for _ in range(4)] for _ in range(256)]
    lo, n, mask, t, sp = rnd.randrange(0, 120), rnd.randrange(1, 120), rnd.randrange(16), rnd.randrange(0, 60), rnd.randrange(-9, 10)
    E.put_buf(U.A, a)
    run(0x0050AC20, newrec({3: ("B", mask), 0x36: ("H", t), 0x12: ("H", n), 0x14: ("B", lo), 0x20: ("h", sp), 0x22: ("B", mode)}), U.A, REC)
    exp = [r[:] for r in a]
    if mode < 3:
        for kk in range(n):
            src = a[lo + src1(mode, kk, t * sp, n)]
            for c in range(4):
                if mask >> c & 1:
                    exp[lo + kk][c] = src[c]
    return E.get_buf(U.A), exp, (mode, t, sp, lo, n, mask)


m_trials("M1", 400, 11, b1, "op1 = permute the range: rotate / clamped shift / mirror by t*speed; mode 3+ no-op")


def b2(rnd, k):
    mode = k % 2
    a = rows8(rnd)
    lo, n, mask = rnd.randrange(0, 100), rnd.randrange(1, 100), rnd.randrange(16)
    t, cap = rnd.choice([1, 2, 5, 30, 100, 254, 255, 300]), rnd.choice([0, 0, 10, 50])
    v = [rnd.randrange(-128, 128) for _ in range(4)]
    E.put_buf(U.A, a)
    run(0x00506B40, newrec({3: ("B", mask), 0x36: ("H", t), 0x12: ("H", n), 0x14: ("B", lo), 0x2A: ("B", mode), 0x28: ("H", cap),
                              0x20: ("h", v[0]), 0x22: ("h", v[1]), 0x24: ("h", v[2]), 0x26: ("h", v[3])}), U.A, REC)
    tt = min(t, cap) if cap else t
    exp = [r[:] for r in a]
    for i in range(lo, lo + n):
        for c in range(4):
            vc = v[c] if mask >> c & 1 else 0
            if mode == 0:
                add = I32((s16(vc) * s16(min(tt, 255))) << 8)
            else:
                x = (((a[i][c] >> 8) & 0xFFFFFF) * vc & 0xFFFFFFFF) >> 7
                add = I32((s16(x) * s16(tt)) << 8)
            exp[i][c] = I32(a[i][c] + add)
    return E.get_buf(U.A), exp, (mode, t, cap, v, mask)


m_trials("M2", 160, 12, b2, "op2 = mode 0: add v*t (colour units); mode 1: add (c*v/128)*t; t capped by +0x28")


def b3(rnd, k):
    mode = k % 2
    a = rows8(rnd)
    lo, n, mask = rnd.randrange(0, 100), rnd.randrange(1, 100), rnd.randrange(16)
    t, dur = rnd.choice([1, 2, 5, 30, 100, 254, 255, 300]), rnd.randrange(1, 300)
    col = [rnd.randrange(256) for _ in range(4)]
    E.put_buf(U.A, a)
    run(0x005080A0, newrec({3: ("B", mask), 0x36: ("H", t), 0x12: ("H", n), 0x14: ("B", lo), 0x26: ("B", mode), 0x24: ("H", dur),
                              0x20: ("I", struct.unpack("<I", bytes(col))[0])}), U.A, REC)
    tgt = [[c << 8 for c in col]] * 256
    exp = crossfade(a, tgt, t, dur, mask, lo, n) if mode else approach(a, tgt, t, mask, lo, n)
    return E.get_buf(U.A), exp, (mode, t, dur, col, mask)


m_trials("M3", 160, 13, b3, "op3 = fade the range to one RGBA8 colour: mode 1 crossfade over +0x24, mode 0 step t per channel")


def b4(rnd, k):
    mode = k % 2
    a, b = rows8(rnd), rows8(rnd)
    lo, n, mask = rnd.randrange(0, 100), rnd.randrange(1, 100), rnd.randrange(16)
    t, dur = rnd.choice([1, 2, 5, 30, 100, 254, 255, 300]), rnd.randrange(1, 300)
    E.put_buf(U.A, a)
    E.put_buf(U.B, b)
    run(0x0050A100, newrec({3: ("B", mask), 0x36: ("H", t), 0x12: ("H", n), 0x14: ("B", lo), 0x26: ("B", mode), 0x24: ("H", dur)}), U.A, U.B, REC)
    exp = crossfade(a, b, t, dur, mask, lo, n) if mode else approach(a, b, t, mask, lo, n)
    return E.get_buf(U.A), exp, (mode, t, dur, mask)


m_trials("M4", 160, 14, b4, "op4 = fade the range to the second CLUT's entries, the same two modes as op3")


def b5(rnd, k):
    a = rows8(rnd)
    lo, n, mask = rnd.randrange(0, 100), rnd.randrange(1, 100), rnd.randrange(16)
    t, dur = rnd.choice([1, 2, 5, 30, 100, 254, 255, 300]), rnd.randrange(1, 300)
    E.put_buf(U.A, a)
    run(0x00509BB0, newrec({3: ("B", mask), 0x36: ("H", t), 0x12: ("H", n), 0x14: ("B", lo), 0x20: ("H", dur)}), U.A, REC)
    exp = [r[:] for r in a]
    f = ((t << 8) // dur) & 0xFF
    for i in range(lo, lo + n):
        y = (a[i][0] >> 8) * 77 + (a[i][1] >> 8) * 150 + (a[i][2] >> 8) * 29
        for c in range(3):
            if mask >> c & 1:
                exp[i][c] = y if t >= dur else a[i][c] + ((y - a[i][c]) >> 8) * f
    return E.get_buf(U.A), exp, (t, dur, mask)


m_trials("M5", 160, 15, b5, "op5 = desaturate lanes 0-2 toward Y = (77 R + 150 G + 29 B) / 256 over +0x20 frames")


def b6(rnd, k):
    a = rows8(rnd)
    lo, n, mask = rnd.randrange(0, 100), rnd.randrange(1, 100), rnd.randrange(16)
    t, dur = rnd.choice([1, 2, 5, 30, 100, 254, 255, 300]), rnd.choice([rnd.randrange(1, 300), 0x100, 0x200])
    col = [rnd.randrange(256) for _ in range(4)]
    raw = newrec({3: ("B", mask), 0x36: ("H", t), 0x12: ("H", n), 0x14: ("B", lo), 0x20: ("I", struct.unpack("<I", bytes(col))[0]), 0x24: ("H", dur)})
    for j in range(0x26, 0x2B):
        raw[j] = rnd.randrange(256)
    E.put_buf(U.A, a)
    run(0x00507490, raw, U.A, REC)
    g = struct.unpack_from("<I", raw, 0x23)[0]
    exp = [r[:] for r in a]
    for i in range(lo, lo + n):
        for c in range(3):
            if mask >> c & 1:
                f = I32(s16(2 * col[c]) * s16(g) + s16((a[i][c] >> 7) & 0x1FFFFFF) * s16(0x80 - g))
                exp[i][c] = f if t >= dur else I32(a[i][c] + s16(I32(f - a[i][c]) >> 8) * s16((t << 8) // dur))
    return E.get_buf(U.A), exp, (t, dur, col, hex(g), mask)


m_trials("M6", 200, 16, b6, "op6 = tint lanes 0-2 toward colour: F = A + (G/128)(col*256 - A), G = halfword +0x23; crossfade to F over +0x24")

PAD = 32
f32 = np.float32


def model7(a, col, mask, lo, n, t, speed, width):
    out = {i: r[:] for i, r in a.items()}
    p = t * speed
    if p == 0:
        return out
    colv = [(col[c] << 8) if mask >> c & 1 else 0 for c in range(4)]

    def full(i):
        for c in range(4):
            if mask >> c & 1:
                out[i][c] = colv[c]

    def ramp(i, w):           # all four lanes: the step vector is not masked (022D92F0), the colour is
        for c in range(4):
            out[i][c] = I32(out[i][c] + s16(I32(colv[c] - out[i][c]) >> 8) * s16(w))

    q = abs(p)
    if q - width >= n:
        for i in range(lo, lo + n):
            full(i)
        return out
    step, acc = f32(256.0) / f32(width), f32(0.0)
    if q > n:
        acc, q = f32(f32(q - n) * step), n
    band, ws = min(width, q), []
    for _ in range(band):
        acc = f32(acc + step)
        ws.append(int(acc))
    if p > 0:
        head = lo + q - 1
        for k in range(band):
            ramp(head - k, ws[k])
        for k in range(q - band):
            full(head - band - k)
    else:
        head = n - lo - q     # 005096BF: the start byte is subtracted, not added
        for k in range(band):
            ramp(head + k, ws[k])
        for k in range(q - band):
            full(head + band + k)
    return out


below = [0]


def b7(rnd, k):
    rows = {i: [rnd.randrange(0, 256) << 8 for _ in range(4)] for i in range(-PAD, 256)}
    E.mu.mem_write(U.A - 16 * PAD, b"".join(struct.pack("<4i", *rows[i]) for i in range(-PAD, 256)))
    lo, n, mask = rnd.choice([0, 0, rnd.randrange(0, 30)]), rnd.randrange(1, 60), rnd.randrange(16)
    t, speed, width = rnd.randrange(1, 40), rnd.choice([1, 2, 3, -1, -2, -3]), rnd.randrange(1, 20)
    col = [rnd.randrange(256) for _ in range(4)]
    run(0x00508C90, newrec({3: ("B", mask), 0x36: ("H", t), 0x12: ("H", n), 0x14: ("B", lo), 0x20: ("I", struct.unpack("<I", bytes(col))[0]),
                              0x24: ("h", speed), 0x26: ("B", width)}), U.A, REC)
    d = bytes(E.mu.mem_read(U.A - 16 * PAD, 16 * (PAD + 256)))
    got = {i: list(struct.unpack_from("<4i", d, 16 * (i + PAD))) for i in range(-PAD, 256)}
    if any(got[i] != rows[i] for i in range(-PAD, 0)):
        below[0] += 1
    return got, model7(rows, col, mask, lo, n, t, speed, width), (t, speed, width, lo, n, mask)


m_trials("M7", 300, 17, b7, "op7 = sweep the colour through the range at t*speed entries with a linear ramp of +0x26 entries")


def b8(rnd, k):
    a, b = rows8(rnd), rows8(rnd)
    lo, n, mask = rnd.randrange(0, 100), rnd.randrange(1, 100), rnd.randrange(16)
    val = rnd.random()
    cur = REC + 0x800
    E.mu.mem_write(cur, struct.pack("<iiii", 0, 1, 0, 0) + struct.pack("<4f", 1000.0, val, 0.0, 0.0))
    E.put_buf(U.A, a)
    E.put_buf(U.C, b)
    run(0x00507120, newrec({3: ("B", mask), 0x36: ("H", 5), 0x12: ("H", n), 0x14: ("B", lo), 0x28: ("Q", cur)}), U.A, U.C, REC)
    w = int(float(f32(val)) * 256.0)
    return E.get_buf(U.A), lerp(a, b, w, mask, lo, n), (val, w, mask)


m_trials("M8", 60, 18, b8, "op8 = crossfade the range to the second CLUT by weight (int)(256 * curve(t))")

# ---------------------------------------------------------------------------------------------------------------- K
SRC, DST = REC + 0x1000, REC + 0x3000


def csm(i):
    return (i & ~0x18) | {0: 0, 8: 16, 16: 8, 24: 24}[i & 0x18]


E.mu.mem_write(SRC, bytes((i * 7 + 3) & 255 for i in range(1024)))
srcb = bytes(E.mu.mem_read(SRC, 1024))
ok = True
for fmt in (1, 16, 256):
    E.put_buf(U.A, [[0x7777] * 4] * 256)
    E.call(0x003CD840, SRC, U.A, fmt)
    g = E.get_buf(U.A)
    order = csm if fmt == 256 else (lambda i: i)
    ok &= all(g[i] == [srcb[4 * order(i) + c] << 8 for c in range(4)] for i in range(fmt))
    ok &= all(r == [0x7777] * 4 for r in g[fmt:])
check("K1", ok and txt(0x003CD848) == "cmp r8d, 1" and txt(0x003CD9FB) == "cmp r8d, 0x10" and txt(0x003CF46C) == "cmp r8d, 0x100",
      "003CD840(src, buf, n): n = 1 / 16 / 256 RGBA8 CLUT entries -> 4 x s32 lanes byte << 8; n = 256 read in PS2 CSM1 order")
rnd, ok = random.Random(19), True
for fmt in (1, 16, 256):
    rows = [[rnd.randrange(-300 * 256, 600 * 256) for _ in range(4)] for _ in range(256)]
    E.put_buf(U.A, rows)
    E.mu.mem_write(DST, b"\x55" * 1028)
    E.call(0x003D2B60, U.A, DST, fmt)
    d = bytes(E.mu.mem_read(DST, 1028))
    order = csm if fmt == 256 else (lambda i: i)
    ok &= all(d[4 * i + c] == max(0, min(255, rows[order(i)][c] >> 8)) for i in range(fmt) for c in range(4))
    ok &= d[4 * fmt:4 * fmt + 4] == b"\x55" * 4
check("K2", ok and txt(0x003D2B71) == "cmp r8d, 1" and txt(0x003D2E40) == "cmp r8d, 0x10",
      "003D2B60(buf, dst, n): lanes >> 8 clamped to 0..255, packed back to RGBA8 in the same order - the working buffer is a CLUT")


def curve(keys, t):
    cur = REC + 0x2000
    E.mu.mem_write(cur, struct.pack("<iiii", 0, len(keys), 0, 0) + b"".join(struct.pack("<4f", *k) for k in keys))
    E.mu.reg_write(UC_X86_REG_XMM1, struct.unpack("<I", struct.pack("<f", t))[0])
    E.call(0x0053DB50, cur, 0)
    return struct.unpack("<f", struct.pack("<I", E.mu.reg_read(UC_X86_REG_XMM0) & 0xFFFFFFFF))[0]


rnd, worst = random.Random(20), 0.0
for _ in range(200):
    k0 = rnd.uniform(-5, 5)
    k1 = k0 + rnd.uniform(0.5, 5)
    v0, v1, a0, b0, a1, b1_ = [rnd.uniform(-3, 3) for _ in range(6)]
    tt = rnd.uniform(k0, k1)
    s, dd = (tt - k0) / (k1 - k0), k1 - k0
    herm = v0 * (2 * s ** 3 - 3 * s ** 2 + 1) + v1 * (-2 * s ** 3 + 3 * s ** 2) + b0 * dd * (s ** 3 - 2 * s ** 2 + s) + a1 * dd * (s ** 3 - s ** 2)
    worst = max(worst, abs(curve([(k0, v0, a0, b0), (k1, v1, a1, b1_)], tt) - herm))
check("K3", worst < 1e-4 and curve([(0, 0, 0, 0), (10, 1, 0, 0)], 2.5) == 0.15625
      and all_txt([(0x0053DB54, "mov edx, dword ptr [rcx + 4]"), (0x0053DB57, "lea r9, [rcx + 0x10]"), (0x0053DBA4, "sar eax, 1"),
                   (0x0053DBA9, "add rcx, rcx"), (0x0053DBAC, "movss xmm0, dword ptr [r9 + rcx*8]"), (0x0053DC1B, "divss xmm5, xmm1")]),
      "0053DB50: 16-byte keys (time, value, in-tangent +8, out-tangent +0xC), bisection, cubic Hermite (max err %.1e; 0.25 -> 0.15625, not linear)" % worst)

# ---------------------------------------------------------------------------------------------------------------- Q
check("Q1", below[0] > 0, "op7 negative speed with a non-zero start byte writes below 02B477A0 (%d of 300 M7 trials; modelled exactly)" % below[0])
g6 = 0x6400 | 0xAB
check("Q2", txt(0x00431C70) == "mov eax, 0x64" and txt(0x00431C79) == "mov word ptr [rbp - 0x3c], ax" and txt(0x00431C99) == "movzx eax, byte ptr [rdi + 7]"
      and txt(0x00431C9D) == "mov byte ptr [rbp - 0x3d], al" and s16(g6) == 25771,
      "00431B10 kind 5 writes duration 100 at record +0x24 and item byte 7 at +0x23, so op6's strength halfword is 0x64xx (~200x the 0x80 unit)")
E.put_buf(U.A, [[i] * 4 for i in range(256)])
run(0x0050AC20, newrec({3: ("B", 15), 0x36: ("H", 1), 0x12: ("H", 6), 0x14: ("B", 0), 0x20: ("h", -7), 0x22: ("B", 2)}), U.A, REC)
neg7 = [r[0] for r in E.get_buf(U.A, 6)]
E.put_buf(U.A, [[i] * 4 for i in range(256)])
run(0x0050AC20, newrec({3: ("B", 15), 0x36: ("H", 1), 0x12: ("H", 6), 0x14: ("B", 0), 0x20: ("h", 5), 0x22: ("B", 2)}), U.A, REC)
pos5 = [r[0] for r in E.get_buf(U.A, 6)]
check("Q3", neg7 == [4, 3, 2, 1, 0, 1] and pos5 == [4, 3, 2, 1, 0, 0],
      "op1 mode 2 is not periodic in s: shift -7 gives %s, shift +5 (same residue mod 12) gives %s" % (neg7, pos5))

# ---------------------------------------------------------------------------------------------------------------- X
check("X1", all_txt([(0x003CCC7E, "movups xmm0, xmmword ptr [r9]"), (0x003CCC85, "movups xmm1, xmmword ptr [r9 + 0x10]"),
                     (0x003CCC8E, "movups xmm0, xmmword ptr [r9 + 0x20]"), (0x003CCC93, "movups xmmword ptr [rbx + 0x20], xmm0"),
                     (0x003CCC2D, "xor r8d, r8d"), (0x003CCC5C, "mov dword ptr [rbx + 0x34], r8d"),
                     (0x003CCC65, "mov qword ptr [rbx + 0x40], r8"), (0x003CCC69, "mov qword ptr [rbx + 0x38], r8")]),
      "allocator 003CCC20 copies 48 bytes (+0x00..+0x2F, the operands the ops read at +0x20..+0x2A) and zeroes +0x34 / +0x38 / +0x40 "
      "- the largest-unclassified page section 18 says a 32-byte payload")
check("X2", all_txt([(0x003CCFC3, "mov rbx, qword ptr [rbp + 0x28]"), (0x003CD31D, "mov rbx, qword ptr [rdi + 0x28]"),
                     (0x003CD229, "mov rax, qword ptr [rbx + 0x38]"), (0x003CCE7E, "mov qword ptr [rdi + 0x28], rbx"),
                     (0x003CCE82, "mov qword ptr [rdi + 0x30], rbx"), (0x003CCEB2, "mov qword ptr [rax + 0x38], rbx"),
                     (0x003CCEBA, "mov qword ptr [rbx + 0x40], rax"), (0x003CCEBE, "mov qword ptr [rdi + 0x30], rbx"),
                     (0x003CD051, "mov qword ptr [rdx + 0x38], rax"), (0x003CD057, "mov qword ptr [rcx + 0x28], rax"),
                     (0x003CD068, "mov qword ptr [rdx + 0x40], rax"), (0x003CD071, "mov qword ptr [rcx + 0x30], rax")]),
      "handle entry +0x28 / +0x30 = operation-list head / tail (read by both dispatchers), record +0x38 / +0x40 = next / prev; "
      "writers 003CCC20 (link) and 003CCF20 (unlink) - section 18 says +0x28/+0x30 'written only' and +0x38/+0x40 writers not found")
check("X3", all_txt([(0x00431BAF, "movzx eax, byte ptr [rdi + 1]"), (0x00431BBF, "mov word ptr [rbp - 0x40], ax"),
                     (0x00431CA7, "movzx eax, byte ptr [rdi + 1]"), (0x00431CAF, "mov word ptr [rbp - 0x3c], ax")]),
      "00431B10 zero-extends the op1 / op7 speed byte, so the expression path never takes op7's negative arm (Q1) or op1's negative shifts")
print("FAILS %d" % fails)
