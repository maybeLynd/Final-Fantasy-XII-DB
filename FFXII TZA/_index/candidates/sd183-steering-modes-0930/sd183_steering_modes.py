"""sd183_steering_modes.py - SD-183: what steering modes 1/4 (0033CEF0), 2 (0033D200) and 6 (0033BAA0) compute, and which
code writes the mode bits of the flag word the dispatcher 00339F00 reads (SWE2-ORACLE, 2026-09-30).

Evidence classes, printed with their tag:
  S*  static    decoded instructions / image data of the certified FFXII_TZA.exe (img.py, capstone)
  E*  executed  isolated execution of the shipped bytes in unicorn (emu.py): entry at the named body, RSP % 16 == 8,
                return to a sentinel. The solver context (0x110 bytes) and the locomotion state st (0x180 bytes) are
                zero-filled fixtures whose fields are set per case and printed; ctx+0x100 = ctx+0x108 = &st, as
                BuildSolverContext stores them (003367B4 / 003367BB). Injected globals: 0208E6A0 (the unit count) = 0, so
                BattleUnit_GetBySlotIndex 00236820 returns null; 01E0C2B8 (force-fight flag) = 1. IAT thunks answered in
                Python (float32): cosf, sinf, sqrtf. Stubs (0033BAA0 only): TestForwardStepClearance 00335B60 and
                CheckActorPairClearance 0033D660, value per case. Every other callee runs its shipped bytes; a fetch
                outside the listed code ranges aborts the run.
  M*  model     a Python transcription of the static reading, compared with E* on the same fixtures. Agreement shows the
                reading predicts the shipped code on these inputs; it is not independent evidence.
Run: python sd183_steering_modes.py > sd183_steering_modes.out
"""
import math, os, struct, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import img  # noqa: E402
import emu  # noqa: E402
from capstone.x86 import X86_OP_MEM, X86_OP_IMM  # noqa: E402

FAILS = []
PI = math.pi


def check(tag, ok, msg):
    print("%s  %-4s %s" % ("PASS" if ok else "FAIL", tag, msg))
    if not ok:
        FAILS.append(tag)


def txt(a):
    x = img.dis(a, 16)[0]
    return ("%s %s" % (x.mnemonic, x.op_str)).strip()


def f32(a):
    return struct.unpack("<f", img.rd(a, 4))[0]


# ============================================================== static: dispatch and the countdown gate
check("S1", [txt(a) for a in (0x0033A03D, 0x0033A047, 0x0033A050, 0x0033A05A, 0x0033A064, 0x0033A06E, 0x0033A077, 0x0033A081,
                              0x0033A08B, 0x0033A092, 0x0033A09C, 0x0033A0A6)]
      == ["cmp al, 1", "call 0x33cef0", "cmp al, 2", "call 0x33d200", "cmp al, 3", "call 0x33ce60", "cmp al, 4", "call 0x33cef0",
          "cmp al, 6", "call 0x33baa0", "cmp al, 5", "call 0x33cde0"]
      and txt(0x00339FF9) == "call 0x4687f0" and txt(0x0033A005) == "movaps xmm6, xmm0" and txt(0x00339FB3) == "movss xmm0, dword ptr [rdi + 4]",
      "00339F00: desired heading xmm6 = 004687F0 yaw toward the goal st+4/+8/+0xC; mode = dword[st] & 0x1F: 1 and 4 -> "
      "0033CEF0, 2 -> 0033D200, 3 -> 0033CE60, 4 -> 0033CEF0, 6 -> 0033BAA0 (no xmm1), 5 -> 0033CDE0")
check("S2", txt(0x003367B4) == "mov qword ptr [rcx + 0x108], rdx" and txt(0x003367BB) == "mov qword ptr [rcx + 0x100], rdx"
      and txt(0x0033BF47) == "test dword ptr [rdi], 0x7fe0" and txt(0x0033BF50) == "jne 0x33bf8d" and txt(0x0033BF8D) == "call 0x339f00"
      and [c[0] for c in img.calls_to(0x00339F00)] == [0x0033BF8D],
      "the flag word is dword[st+0] (= BattleUnit +0x80): ctx+0x100 and +0x108 both hold st; the dispatcher's only call "
      "(0033BF8D in SolveDefaultStep) is taken only while the countdown bits 5-14 are non-zero")
check("S3", txt(0x0033A0C5) == "and dword ptr [rdi], 0xffff801f" and txt(0x0033A0D7) == "shr eax, 5" and txt(0x0033A0DA) == "dec eax"
      and txt(0x0033A0E1) == "and eax, 0x7fe0" and txt(0x0033A0E8) == "mov dword ptr [rdi], eax",
      "after the body: countdown cleared when ctx+0xB0 exceeds the XZ distance to the goal, else decremented, mode bits kept")

# ============================================================== static: the mode-bit writers
check("S4", txt(0x0033CD78) == "mov eax, dword ptr [rcx]" and txt(0x0033CD7A) == "xor eax, edi" and txt(0x0033CD7C) == "and eax, 0x1f"
      and txt(0x0033CD7F) == "xor dword ptr [rcx], eax" and txt(0x0033CCCA) == "mov edi, edx"
      and all(txt(a).startswith("movss dword ptr [rax + %s]" % o) for a, o in ((0x0033CD8E, "4"), (0x0033CDA0, "8"), (0x0033CDB2, "0xc")))
      and txt(0x0033CCD4) == "and dword ptr [rax], 0xffff801f",
      "0033CC80(ctx, mode, yaw, pitch, dist): when dist > ctx+0xB0 it writes the goal st+4/+8/+0xC = ctx + dist * "
      "direction(yaw, pitch) and inserts `mode` into bits 0-4 (xor/and 0x1F/xor); otherwise it only clears the countdown")
check("S5", sorted(c[0] for c in img.calls_to(0x0033CC80)) == [0x0033B156, 0x0033B582] and txt(0x0033B14E) == "mov edx, 4"
      and txt(0x0033B580) == "mov edx, esi" and txt(0x0033B27F) == "cvttss2si esi, xmm0" and txt(0x0033B2F6) == "mov esi, eax"
      and txt(0x0033B370) == "mov esi, 1" and txt(0x0033B136) == "call 0x33cef0",
      "0033CC80's two callers are in 0033A720 (the obstacle-avoidance direction search): 0033B156 sets mode 4 after the "
      "candidate loop found no direction (0033CEF0 on the base heading first); 0033B582 sets mode esi = the chooser "
      "00339DF0's value, turned into 1 when the forward step is clear (0033B370) or into 0033D200's return (0033B2F6)")
rows = []
for i in range(48):
    a, b = struct.unpack("<2f", img.rd(0x01EED4C0 + 12 * i, 8))
    m1, m2 = img.rd(0x01EED4C0 + 12 * i + 8, 2)
    rows.append((a, b, m1 + 1, m2 + 1))
check("S6", txt(0x00339E0B) == "movzx eax, byte ptr [r9 + 0x175]" and txt(0x00339E4E) == "cmove rdx, rcx" and txt(0x00339EB0) ==
      "movss xmm0, dword ptr [rip + 0x5b9264]" and f32(0x008F311C) == 3.0 and txt(0x00339ED0) == "movzx eax, byte ptr [rdx + rcx*4 + 8]"
      and txt(0x00339EE3) == "movzx eax, byte ptr [rdx + rcx*4 + 9]" and f32(0x008F3138) == 180.0
      and sorted(set(r[2] for r in rows) | set(r[3] for r in rows)) == [1, 2],
      "the chooser 00339DF0 returns 3.0 (turn in place) when |wrap(candidate - st+0xE0)| > 0.01 and > row[0] degrees, "
      "else row byte 8 + 1 or byte 9 + 1 by row[1] degrees; row = 01EED4C0[(st+0x175 profile, <8 else 1) * 6 + "
      "(st+0x170 bit 3 clear ? 3 : 0) + speed band 0/1/2]; the 48 rows' byte pairs give only modes 1 and 2")
check("S7", txt(0x0033D2B5) == "mov eax, 5" and txt(0x0033D3BB) == "mov eax, 2" and txt(0x0033D28A) == "call 0x334220",
      "0033D200 returns 5 when the goal lies inside a turning circle (00334220), else 2 - so 0033B582 can also write mode 5")
check("S8", txt(0x003346CD) == "and dword ptr [rdi], 0xffffffe6" and txt(0x003346D4) == "or dword ptr [rdi], 6"
      and txt(0x003345B6) == "shl eax, 0xf" and txt(0x00334690) == "shl eax, 5" and txt(0x00334695) == "and eax, 0x7fe0"
      and txt(0x00334733) == "movss dword ptr [rdi + 4], xmm0" and txt(0x0033477A) == "movss dword ptr [rdi + 4], xmm6",
      "003343D0 (TryStartRandomizedAvoidanceManeuver) sets mode 6: bit 15 = a random orbit direction (rand & 1), "
      "countdown = trunc(st+0x12C / arc step), halved when 0031EA90 == 4, st+4 = the orbit radius +- (rand % 5 + 5) / 100")
check("S9", txt(0x0033E272) == "and dword ptr [rdi], 0xffff8000",
      "0033E1F0 (ResetAvoidanceStateRandomized) clears mode and countdown together (mode 0)")
# the census: every dword store through an st pointer obtained as [ctx+0x100]/[ctx+0x108] in the solver band
WR = {"mov", "and", "or", "xor", "add", "sub", "bts", "btr", "inc", "dec"}
found = []
for r in sorted(img.ROOTS):
    if not 0x00330000 <= r < 0x00342000:
        continue
    tagged = set()
    for x in img.fn_ins(r):
        ops = x.operands
        if x.mnemonic in WR and ops and ops[0].type == X86_OP_MEM and ops[0].size == 4 and ops[0].mem.disp == 0 and ops[0].mem.index == 0 \
                and ops[0].mem.base and x.reg_name(ops[0].mem.base) in tagged:
            found.append((x.address, "%s %s" % (x.mnemonic, x.op_str)))
        if len(ops) == 2 and ops[0].type == 1:
            d = x.reg_name(ops[0].reg)
            if x.mnemonic == "mov" and ops[1].type == X86_OP_MEM and ops[1].mem.disp in (0x100, 0x108) and ops[0].size == 8 \
                    and ops[1].mem.base and x.reg_name(ops[1].mem.base) not in ("rsp", "rbp", "rip"):
                tagged.add(d)
            else:
                tagged.discard(d)
MODE_WRITES = {0x0033CD7F: "xor-insert of the caller's mode", 0x003346CD: "clear bits 0, 3, 4", 0x003346D4: "or 6",
               0x0033E272: "clear bits 0-14"}
KEEPS = {}
for a, t in found:
    if a in MODE_WRITES:
        continue
    imm = None
    x = img.dis(a, 16)[0]
    if x.mnemonic == "and" and x.operands[1].type == X86_OP_IMM:
        imm = x.operands[1].imm & 0xFFFFFFFF
        KEEPS[a] = (imm & 0x1F) == 0x1F
    else:
        KEEPS[a] = None
# the register-store (mov/or/xor [st], reg) sites keep bits 0-4 by the code that builds reg:
REG_KEEP = {0x003345B9: txt(0x003345B6) == "shl eax, 0xf",                         # only bit 15
            0x00334607: txt(0x003345FF) == "and ecx, 0x8000",                      # xor-insert of bit 15
            0x0033469A: txt(0x00334695) == "and eax, 0x7fe0",                      # xor-insert of the countdown
            0x003346CB: txt(0x003346BE) == "and eax, 0xffff801f" and txt(0x003346C3) == "and ecx, 0x3fe0",
            0x0033A0E8: txt(0x0033A0E1) == "and eax, 0x7fe0",
            0x0033B507: txt(0x0033B4FD) == "and eax, 0xffff815f" and txt(0x0033B502) == "or eax, 0x140",
            0x0033CEC5: txt(0x0033CEBB) == "and eax, 0xffff815f" and txt(0x0033CEC0) == "or eax, 0x140",
            0x0033D1E1: txt(0x0033D1CF) == "mov eax, 0xa0" and txt(0x0033D1D6) == "mov eax, 0xc0",
            0x0033D3B9: txt(0x0033D3AF) == "and eax, 0xffff815f" and txt(0x0033D3B4) == "or eax, 0x140"}
keep_ok = all(KEEPS[a] is True or REG_KEEP.get(a) for a in KEEPS)
check("S10", sorted(MODE_WRITES) == sorted(a for a, _ in found if a in MODE_WRITES) and keep_ok and len(found) == 24,
      "census of dword stores through st = [ctx+0x100/0x108] in 00330000-00341FFF: %d stores; the only ones that change "
      "bits 0-4 are %s; the other %d keep bits 0-4 (and-masks ending in 0x1F, or registers built with 0x7FE0 / 0x8000 / "
      "0xFFFF815F|0x140 / 0xA0|0xC0)" % (len(found), ", ".join("%08X (%s)" % kv for kv in sorted(MODE_WRITES.items())), len(KEEPS)))

# every reader that compares the five bits, 00300000-00344FFF
readers = []
for r in sorted(img.ROOTS):
    if 0x00300000 <= r < 0x00345000:
        ins = img.fn_ins(r)
        for k, x in enumerate(ins[:-1]):
            if x.mnemonic == "and" and x.op_str.endswith(", 0x1f") and ins[k + 1].mnemonic == "cmp":
                readers.append((r, ins[k + 1].op_str))
check("S13", readers == [(0x003343D0, "al, 6")] + [(0x00339F00, "al, %d" % m) for m in (1, 2, 3, 4, 6, 5)],
      "the only code that compares the five bits is the dispatcher and 003343D0's 'already mode 6' guard (00334441): modes "
      "1 and 4 run the same body and nothing else tells them apart")

# ============================================================== executed fixtures
CODE = [(0x00200000, 0x00220000), (0x00236800, 0x00236850), (0x00253B90, 0x00253BA0), (0x0030C0D0, 0x0030C0D8),
        (0x00330000, 0x00342000), (0x003A1900, 0x003A1960), (0x00460000, 0x00470000), (0x00808C40, 0x00808C60)]
CTX, ST = emu.HEAP, emu.HEAP + 0x1000


def fixture(E, ctx=None, st=None, word=0):
    E.mu.mem_write(CTX, b"\0" * 0x200)
    E.mu.mem_write(ST, b"\0" * 0x200)
    E.mu.mem_write(CTX + 0x100, struct.pack("<QQ", ST, ST))
    E.mu.mem_write(0x0208E6A0, struct.pack("<I", 0))
    E.mu.mem_write(0x01E0C2B8, struct.pack("<I", 1))
    E.mu.mem_write(CTX + 0xC, struct.pack("<f", 1.0))
    E.mu.mem_write(CTX + 0x1C, struct.pack("<f", 1.0))
    for off, v in (ctx or {}).items():
        E.put_f32(CTX + off, v)
    for off, v in (st or {}).items():
        E.put_f32(ST + off, v)
    E.mu.mem_write(ST, struct.pack("<I", word))


def outs(E):
    return E.f32(CTX + 0xB4), E.f32(CTX + 0xBC), struct.unpack("<I", E.mu.mem_read(ST, 4))[0]


def wrap(x):
    while x > PI:
        x -= 2 * PI
    while x < -PI:
        x += 2 * PI
    return x


# ---- mode 1 / 4: 0033CEF0 --------------------------------------------------------------------------------------
def model_cef0(desired, ctx, st, word):
    dist = math.hypot(ctx.get(0x10, 0) - ctx.get(0, 0), ctx.get(0x18, 0) - ctx.get(8, 0))
    b0 = ctx.get(0xB0, 0.0)
    rate = st[0xE4] if (b0 > 0 and b0 > st.get(0x104, 0)) else st[0xE8]
    d0 = abs(wrap(ctx.get(0xBC, 0.0) - desired))
    t = 30.0 if st[0xE8] == 0 else d0 / st[0xE8]
    if d0 < f32(0x0091572C):
        rate = 0.5 * (1 - math.cos(3 * d0)) * (rate - f32(0x008C5F68)) + f32(0x008C5F68)
    cur = st[0xE0]

    def approach():
        d = wrap(desired - cur)
        if abs(d) > rate:
            return wrap(cur + rate if d > 0 else cur - rate)
        return desired
    if dist > t * st[0xF8]:
        bc = approach()
        d2 = wrap(bc - desired)
        cone = st[0x118]
        b4 = bc if abs(d2) <= cone else wrap(desired + cone if d2 > 0 else desired - cone)
    else:
        bc = cur if st.get(0xFC, 0) > dist else approach()
        b4 = desired
    if word & 0x7FE0 == 0:
        word = (word & 0xFFFF801F) | 0xC0          # unit slot null in the fixture -> 0xC0 (6)
    return b4, bc, word


E1 = emu.Emu(CODE, thunks=[0x00861F08, 0x00861F0E, 0x00861F14])
base_st = {0xE0: 0.0, 0xE4: 0.2, 0xE8: 0.1, 0xF8: 0.2, 0xFC: 0.5, 0x104: 1.0, 0x118: 0.5}
cases1 = [
    ("far, full-rate turn, cone clamp", 1.5, {0x10: 10.0, 0xBC: 0.0}, dict(base_st)),
    ("far, eased rate near alignment", 1.5, {0x10: 10.0, 0xBC: 1.4}, {**base_st, 0xE0: 1.4}),
    ("close to goal, inside stop radius: hold", 1.5, {0x10: 0.3, 0xBC: 0.0}, dict(base_st)),
    ("close, outside stop radius: turn, move along desired", 1.5, {0x10: 1.0, 0xBC: 0.0}, {**base_st, 0xFC: 0.2}),
    ("within one step: the jbe fallback stores desired raw", 1.5, {0x10: 10.0, 0xBC: 0.0}, {**base_st, 0xE0: 1.45}),
    ("fast rate while ctx+0xB0 > st+0x104", -2.0, {0x10: 10.0, 0xB0: 2.0, 0xBC: 0.0}, dict(base_st)),
    ("wrap across +-pi", -3.0, {0x10: 10.0, 0xBC: 3.0}, {**base_st, 0xE0: 3.0}),
]
res1 = []
for name, des, c, s in cases1:
    fixture(E1, c, s, word=1)
    E1.call(0x0033CEF0, [0.0, des], rcx=CTX)
    got = outs(E1)
    exp = model_cef0(des, c, s, 1)
    ok = abs(got[0] - exp[0]) < 2e-5 and abs(got[1] - exp[1]) < 2e-5 and got[2] == exp[2]
    res1.append(ok)
    print("      E-1/4 %-52s desired %+.4f -> B4 %+.6f BC %+.6f word %04X | model %+.6f %+.6f %04X" % (name, des, got[0], got[1], got[2], *exp))
check("E1", all(res1), "executed 0033CEF0 on %d fixtures: B4 (move heading) and BC (limited facing) and the countdown arm match "
      "the static reading (M1) on every case" % len(cases1))
check("S11", txt(0x0033CFF5) == "mulss xmm0, dword ptr [rip + 0x5b611f]" and f32(0x008F311C) == 3.0 and txt(0x0033CFFD) == "call 0x861f08"
      and abs(f32(0x0091572C) - PI / 3) < 1e-6 and abs(f32(0x008C5F68) - PI / 180) < 1e-7 and f32(0x008F8D80) == 30.0
      and txt(0x0033D099) == "movaps xmm4, xmm6" and txt(0x0033D15A) == "movaps xmm0, xmm6" and txt(0x0033D102) == "mov eax, dword ptr [rdi + 0xe0]",
      "0033CEF0's constants: easing below pi/3 as 0.5 (1 - cos 3d) blending the rate down to 1 degree; 30 ticks when st+0xE8 == 0; "
      "fallbacks 0033D099 / 0033D15A store the desired heading raw, 0033D102 holds st+0xE0")


# ---- mode 2: 0033D200 --------------------------------------------------------------------------------------------
def model_d200(desired, ctx, st, word):
    b0 = ctx.get(0xB0, 0.0)
    rate = st[0xE4] if (b0 > 0 and b0 > st.get(0x104, 0)) else st[0xE8]
    cur = st[0xE0]
    # turning circles: radius = max(2pi/E8 * F8, 2pi/E4 * FC) / pi * 0.5, centres at pos + r*dir(BC +- pi/2)
    r = max(2 * PI / st[0xE8] * st[0xF8], 2 * PI / st[0xE4] * st[0xFC]) / PI * 0.5
    bc0 = ctx.get(0xBC, 0.0)
    gx, gz = ctx.get(0x10, 0.0), ctx.get(0x18, 0.0)
    inside = any(math.hypot(gx - r * math.sin(wrap(bc0 + s)), gz - r * math.cos(wrap(bc0 + s))) < r for s in (PI / 2, -PI / 2))

    def approach(rt):
        d = wrap(desired - cur)
        if abs(d) > rt:
            return wrap(cur + rt if d > 0 else cur - rt)
        return desired
    if word & 0x7FE0 == 0 and inside:
        return desired, approach(rate), word, 5          # 0033D2AD / 0033D2BA: B4 = the desired heading
    d0 = abs(wrap(bc0 - desired))
    if d0 < PI / 4:
        rate = (d0 * 80.0 / (PI / 4) + 20.0) * rate / 100.0
    dist = math.hypot(gx, gz)
    # 0033D385 overwrites xmm6 with the turned heading, so 0033D39E stores it as B4 too; the fallback and the hold keep
    # xmm6 = the desired heading
    bc = approach(rate) if dist > st[0xF8] * 5.0 else cur
    b4 = bc if dist > st[0xF8] * 5.0 else desired
    if word & 0x7FE0 == 0:
        word = (word & 0xFFFF815F) | 0x140
    return b4, bc, word, 2


E2 = emu.Emu(CODE, thunks=[0x00861F08, 0x00861F0E, 0x00861F14])
cases2 = [
    ("goal ahead, outside both turning circles", 0.2, {0x10: 1.0, 0x18: 10.0, 0xBC: 0.0}, dict(base_st), 2),
    ("goal inside a turning circle -> returns 5", 1.5, {0x10: 0.8, 0x18: 0.1, 0xBC: 0.0}, {**base_st, 0xF8: 0.5}, 2),
    ("eased below pi/4", 0.3, {0x10: 3.0, 0x18: 10.0, 0xBC: 0.1}, {**base_st, 0xE0: 0.1}, 2),
    ("close (dist <= 5 speed), countdown running: hold", 1.0, {0x10: 0.5, 0x18: 0.5, 0xBC: 0.0}, dict(base_st), 2 | (3 << 5)),
    ("countdown running: no circle test, no re-arm", 1.5, {0x10: 0.8, 0x18: 0.1, 0xBC: 0.0}, {**base_st, 0xF8: 0.5}, 2 | (4 << 5)),
]
res2 = []
for name, des, c, s, w in cases2:
    fixture(E2, c, s, word=w)
    _, rax = E2.call(0x0033D200, [0.0, des], rcx=CTX)
    got = outs(E2)
    exp = model_d200(des, c, s, w)
    ok = abs(got[0] - exp[0]) < 2e-5 and abs(got[1] - exp[1]) < 2e-5 and got[2] == exp[2] and (rax & 0xFFFFFFFF) == exp[3]
    res2.append(ok)
    print("      E-2   %-52s desired %+.4f -> B4 %+.6f BC %+.6f word %04X ret %d | model %+.6f %+.6f %04X %d"
          % (name, des, got[0], got[1], got[2], rax & 0xFFFFFFFF, *exp))
check("E2", all(res2) and any(r for r, cs in zip(res2, cases2) if "returns 5" in cs[0]),
      "executed 0033D200 on %d fixtures (its turning-circle test 00334220 runs its shipped bytes): outputs, returned 2 / 5 and the "
      "countdown arm match the reading (M2)" % len(cases2))
check("S12", abs(f32(0x00915614) - PI / 4) < 1e-6 and f32(0x008F6D58) == 80.0 and f32(0x00901988) == 20.0 and f32(0x008F3134) == 100.0
      and f32(0x009146E4) == 5.0 and txt(0x0033D3AF) == "and eax, 0xffff815f" and txt(0x0033D3B4) == "or eax, 0x140",
      "0033D200's constants: below pi/4 the rate scales by (80 d / (pi/4) + 20) %; it holds st+0xE0 within 5 steps of the "
      "goal; its order-word store 0033D3B9 arms the countdown at 10 and keeps bits 0-4 (no mode change)")


# ---- mode 6: 0033BAA0 ----------------------------------------------------------------------------------------------
def model_orbit_heading(pos, centre, speed, word, radius_target):
    vx, vz = pos[0] - centre[0], pos[2] - centre[2]
    r = math.hypot(vx, vz)
    circ = 2 * PI * r
    if speed > circ:
        return 0.0
    a = speed / circ * 2 * PI
    if word & 0x8000:
        a = -a
    a = wrap(a)
    # 00202F00 builds the rotation; the executed result decides its handedness (see E3's second case)
    return a, r, circ


E3 = emu.Emu(CODE, thunks=[0x00861F08, 0x00861F0E, 0x00861F14],
             stubs={0x00335B60: lambda e: (e.clear, None), 0x0033D660: lambda e: (0, None)})
res3 = []
for name, pos, word, clear in [("orbit clockwise bit 15 = 0", (5.0, 0.0, 0.0), 6 | (10 << 5), 0),
                               ("orbit bit 15 = 1 (reverse)", (5.0, 0.0, 0.0), 6 | (10 << 5) | 0x8000, 0),
                               ("step clear and no actor pair blocks -> ends", (5.0, 0.0, 0.0), 6 | (10 << 5), 1)]:
    E3.clear = clear
    fixture(E3, {0x00: pos[0], 0x08: pos[2], 0x40: 0.0, 0x48: 0.0, 0xBC: 1.0, 0xB0: 0.3},
            {**base_st, 0xF8: 0.5, 0x04: 5.0}, word=word)
    E3.mu.mem_write(ST + 0x174, b"\x01")
    E3.call(0x0033BAA0, [], rcx=CTX)
    b4, bc, w = outs(E3)
    b0, b8 = E3.f32(CTX + 0xB0), E3.f32(CTX + 0xB8)
    print("      E-6   %-52s -> B4 %+.6f BC %+.6f B0 %.4f B8 %.4f word %04X" % (name, b4, bc, b0, b8, w))
    res3.append((name, b4, bc, b0, b8, w))
a, r, circ = model_orbit_heading((5.0, 0, 0), (0, 0, 0), 0.5, 0, 5.0)
cw, ccw, end = res3
# the orbit step turns the radius vector (5, 0) (x, z) about the centre by a = speed / circumference * 2pi; the heading
# is the chord's yaw (004687F0: acos of the z share, negated for x < 0): the chord (5 cos a - 5, +-5 sin a) has x < 0 and
# z share +-cos(a/2), so the two directions give -a/2 and -(pi - a/2)
chords = sorted([-a / 2, -(PI - a / 2)])
check("E3", all(abs(g - e) < 5e-3 for g, e in zip(sorted([cw[1], ccw[1]]), chords)) and cw[3] == 0.5 and cw[4] == 0.0
      and end[5] & 0x7FE0 == 0 and end[3] == 0.0 and end[5] & 0x1F == 6,
      "executed 0033BAA0 (stubs 00335B60 = 0 / 1, 0033D660 = 0): on the orbit branch ctx+0xB4 = the chord heading of one "
      "arc step, %+.6f / %+.6f for a = speed/circumference*2pi = %.6f (to the acos table's step, 5e-3), the direction set "
      "by bit 15; ctx+0xB0 = st+0xF8, "
      "ctx+0xB8 = 0; with the step clear and no pair blocking it clears the countdown and ctx+0xB0 (mode bits kept)"
      % (cw[1], ccw[1], a))
rate_exp = 0.5 / (2 * PI * 5.0) * 2 * PI * 1.5
check("E4", abs(cw[2] - (1.0 - rate_exp)) < 2e-4 and abs(ccw[2] - (1.0 - rate_exp)) < 2e-4,
      "the limited facing turns from ctx+0xBC = 1.0 toward ctx+0xA8 (0 in the fixture; BuildSolverContext writes it as the "
      "yaw toward the target) by 1.5 x the arc angle = %.4f: BC = %+.6f" % (rate_exp, cw[2]))

# ---- positive control from the documents: mode 3 (0033CE60) as the locomotion page's AM-7 answer describes it
E5 = emu.Emu(CODE, thunks=[0x00861F08, 0x00861F0E, 0x00861F14])
ctl = []
for des, cur, word in ((1.0, 0.0, 3), (0.05, 0.0, 3 | (7 << 5))):
    fixture(E5, {0xB0: 0.4, 0xBC: cur}, {**base_st, 0xE0: cur, 0xEC: 0.1}, word=word)
    E5.call(0x0033CE60, [0.0, des], rcx=CTX)
    ctl.append(outs(E5) + (E5.f32(CTX + 0xB0),))
check("E5", abs(ctl[0][0] - 0.1) < 1e-6 and ctl[0][1] == ctl[0][0] and (ctl[0][2] >> 5) & 0x3FF == 10 and ctl[0][3] == 0.0
      and abs(ctl[1][0] - 0.05) < 1e-6 and ctl[1][2] & 0x7FE0 == 0,
      "control from the page's AM-7 text, executed 0033CE60: speed +0xB0 zeroed, B4 = BC = cur turned by the slow rate "
      "st+0xEC (%.4f), countdown armed at %d; on arrival (%.4f) the countdown is cleared (word %04X)"
      % (ctl[0][0], (ctl[0][2] >> 5) & 0x3FF, ctl[1][0], ctl[1][2]))
print("FAILS %d" % len(FAILS))
