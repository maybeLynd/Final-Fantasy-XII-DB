"""sd184_facing_sources.py - SD-184 remainder: where the unnormalised heading stores get their values, and what
Angle_NormalizeRadiansPi (0033CB70) does at and beyond 4pi (SWE2-ORACLE, 2026-09-30).

Two evidence classes, printed with their tag:
  S*  static   - decoded instructions and image data of the certified FFXII_TZA.exe (img.py, capstone)
  E*  executed - isolated execution of the shipped bytes in unicorn (emu.py). Entry boundary: the named function's
                 entry, RSP % 16 == 8, return to a sentinel. Stubs: none for 0033CB70, 00334120, 00316DA0, 0026A0D0;
                 004687F0 runs its real callees (00469320, 00202D20, 0046F460, the cookie check 00808C40) with only the
                 IAT thunk sqrtf answered in Python (float32). Inputs are listed at each check. No other state is injected.
The script-corpus side (what setposparty is given) is sd184_setposparty_census.py / .out.
Run: python sd184_facing_sources.py > sd184_facing_sources.out
"""
import math, struct, sys, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import img  # noqa: E402
import emu  # noqa: E402
from capstone.x86 import X86_OP_REG, X86_OP_MEM  # noqa: E402

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


def writes_reg(x, name):
    """True when instruction x writes register `name` as its destination (first operand)."""
    if not x.operands or x.operands[0].type != X86_OP_REG:
        return False
    if x.mnemonic in ("comiss", "ucomiss", "cmp", "test", "push"):
        return False
    return x.reg_name(x.operands[0].reg) == name


# ---------------------------------------------------------------- static: the setposparty route
check("S1", txt(0x003571C0) == "call 0x267db0" and txt(0x003571D6) == "movaps xmm6, xmm0" and txt(0x003571FA) == "mov r8d, 1"
      and txt(0x00357206) == "movaps xmm1, xmm6" and txt(0x0035720E) == "call 0x37d000" and txt(0x0033F0CA) == "xor r8d, r8d"
      and txt(0x0033F0D3) == "movaps xmm1, xmm6",
      "setposparty (0x3B1 -> 003571A0) passes its FIRST pop (the last pushed argument) as xmm1 with r8d = 1; "
      "setposparty_mapjump (0x56D -> 0033F070) the same with r8d = 0")
check("S2", txt(0x0037D01E) == "movaps xmm6, xmm1" and txt(0x0037D024) == "test r8d, r8d" and txt(0x0037D027) == "jne 0x37d0a6"
      and txt(0x0037D0A4) == "jmp 0x37d0dd" and txt(0x0037D0D2) == "movaps xmm1, xmm6" and txt(0x0037D0D8) == "call 0x310920",
      "0037D000 reaches 00310920 (xmm1 = the facing, unchanged) only on r8d != 0, i.e. only from setposparty")
ins = img.fn_ins(0x00310920)
w6 = [x.address for x in ins if writes_reg(x, "xmm6")]
st160 = [x.address for x in ins if x.mnemonic == "movss" and x.operands[0].type == X86_OP_MEM and x.operands[0].mem.disp == 0x160]
check("S3", txt(0x0031094F) == "movaps xmm6, xmm1" and w6 == [0x0031094F, 0x00310D0A] and st160 == [0x00310B00, 0x00310BB1, 0x00310CA6]
      and all(txt(a).endswith("xmm6") for a in st160),
      "00310920: xmm6 is written only at entry (0031094F = the facing) and in the epilogue restore (00310D0A); its three "
      "BattleUnit +0x160 stores (00310B00, 00310BB1, 00310CA6) store that xmm6 raw (xmm6 is non-volatile across the calls)")

# ---------------------------------------------------------------- static: 00311F70's facing is 00336E40's +0x30
check("S4", txt(0x00311FC0) == "lea rcx, [rsp + 0x40]" and txt(0x00311FCE) == "call 0x336e40" and txt(0x00312096) == "movss xmm6, dword ptr [rsp + 0x70]"
      and txt(0x003120AF) == "movss dword ptr [rdi + 0x160], xmm6" and txt(0x003120F7) == "movss dword ptr [rax + 0x70], xmm6",
      "00311F70 (all seven call sites) publishes +0x30 of the record it hands 00336E40 (rsp+0x40 -> rsp+0x70), not a caller argument")
ins = img.fn_ins(0x00336E40)
st30 = [x.address for x in ins if x.operands and x.operands[0].type == X86_OP_MEM and x.operands[0].mem.disp == 0x30
        and x.reg_name(x.operands[0].mem.base) == "rdi" and x.mnemonic.startswith("mov")]
check("S5", st30 == [0x00336FAA, 0x00337429] and txt(0x00336FA2) == "movss xmm1, dword ptr [rip + 0x1f90e36]"
      and txt(0x00337381) == "call 0x4687f0" and txt(0x003373BD) == "jmp 0x337429" and txt(0x00337422) == "call 0x265200"
      and txt(0x00337414) == "xorps xmm0, xmm0" and txt(0x00337427) == "xor eax, eax",
      "00336E40 writes +0x30 twice: 00336FAA = [022C7DE0]; 00337429 = xmm0, which is 004687F0's yaw (00337381, "
      "via 003373BD) or 00265200's facing (00337422) or 0.0 (00337414)")
# every rip-relative store to 022C7DE0 in the image
w7de0 = []
for r in img.ROOTS:
    try:
        for x in img.fn_ins(r):
            if x.operands and x.operands[0].type == X86_OP_MEM and img.ripmem(x) == 0x022C7DE0 and not x.mnemonic.startswith(("cmp", "ucomi", "comi")):
                w7de0.append(x.address)
    except Exception:
        pass
check("S6", sorted(w7de0) == [0x0033CAE0] and txt(0x0033CADB) == "call 0x265200",
      "022C7DE0 has one store image-wide (0033CAE0), and it stores 00265200's facing (0033CADB)")

# ---------------------------------------------------------------- static: the BattleUnit +0x160 stores in the battle band
band = []
for r in img.ROOTS:
    if not 0x002F0000 <= r < 0x00340000:
        continue
    for x in img.fn_ins(r):
        if (x.operands and x.operands[0].type == X86_OP_MEM and x.operands[0].mem.disp == 0x160 and x.operands[0].mem.index == 0
                and x.mnemonic.startswith("mov") and x.reg_name(x.operands[0].mem.base) not in ("rsp", "rbp")):
            band.append(x.address)
band.sort()
EXPECT = [0x002F2BB2, 0x002F6B7A, 0x002F6C6D, 0x002FDB1B, 0x002FDCC7, 0x00300426, 0x003043A8, 0x00304BD3, 0x00307A0B, 0x00310B00, 0x00310BB1, 0x00310CA6,
          0x003120AF, 0x00312F77]
check("S7", band == EXPECT and txt(0x002FDA8E) == "lea rdi, [rcx + 0x80]" and txt(0x002FDC42) == "lea rdi, [rcx + 0x80]"
      and txt(0x002F2BA7) == "movups xmmword ptr [rbx + 0x150], xmm0" and txt(0x002F2BBD) == "movups xmmword ptr [rbx + 0x170], xmm0"
      and txt(0x002F6B01) == "mov rsi, rcx" and txt(0x0026E7B1) == "call 0x2f6ab0",
      "the +0x160 stores in 002F0000-0033FFFF are %s. Not headings: 002F2BB2 is the middle row of a 48-byte copy "
      "(+0x150/+0x160/+0x170) in 002F2530, and 002F6B7A / 002F6C6D are fields of the 0x240-byte object 002F6AB0 builds "
      "for 0026E760. 002FDB1B / 002FDCC7 / 00304BD3 go through st = unit+0x80 (= BattleUnit +0x1E0, the look-target kind). "
      "The other eight are BattleUnit +0x160 = st+0xE0" % ", ".join("%08X" % a for a in band))
check("S8", txt(0x003042FC) == "call 0x265200" and txt(0x0030430F) == "movaps xmm6, xmm0" and txt(0x003043A8) == "movss dword ptr [r15 + 0x160], xmm6"
      and txt(0x00307945) == "call 0x265200" and txt(0x00307958) == "movaps xmm6, xmm0" and txt(0x00307A0B) == "movss dword ptr [rbx + 0x160], xmm6"
      and txt(0x00312F59) == "call 0x265200" and txt(0x00312F65) == "call 0x31acc0" and txt(0x00312F77) == "movss dword ptr [rbx + 0x160], xmm0"
      and txt(0x0031AD6D) == "call 0x861f02" and txt(0x0031AD75) == "movaps xmm0, xmm6" and txt(0x0031ACDA) == "movaps xmm6, xmm1",
      "three facing publishes the page's table lacks: 003043A8 (00304180) and 00307A0B (00307300) store 00265200's facing; "
      "00312F77 (00312EE0) stores 0031ACC0's result = atan2f or its 00265200 argument")
check("S9", txt(0x00265216) == "mov rax, qword ptr [rcx + 0xb8]" and txt(0x0026521D) == "movss xmm0, dword ptr [rax + 0xa8]"
      and txt(0x0026522D) == "movss xmm0, dword ptr [rax + 0x38]" and txt(0x002E5EBE) == "movss dword ptr [rsi + 0xa8], xmm6"
      and txt(0x002E5EB3) == "subss xmm6, xmm1" and txt(0x0026B70D) == "movss dword ptr [rax + 0x38], xmm3" and txt(0x0026B6E9) == "subss xmm3, xmm1",
      "00265200 reads movementState +0xA8 (kind 3) or +0x38 (kind 1); their writers 002E5E10 and 0026B6A0 store the "
      "sign-biased wrap x - trunc((x +- pi) / 2pi) * 2pi (single writers per the movement-context census)")

# ---------------------------------------------------------------- static: Angle_ApproachWrappedRadians' nine targets
check("S10", txt(0x00334136) == "movaps xmm6, xmm1" and txt(0x00334153) == "jbe 0x334187" and txt(0x00334187) == "movaps xmm0, xmm6",
      "00334120's early path (|wrap(target - cur)| <= step) returns its target argument raw")
T = {
    0x0033A678: (0x0033A660, "call 0x4687f0", "004687F0 yaw"),
    0x0033A6A6: (0x0033A696, "movss xmm1, dword ptr [rsi + 0x150]", "st+0x150 when st+0x160 == 2 (the order's facing goal)"),
    0x0033BC39: (0x0033BC26, "movss xmm1, dword ptr [rdi + 0xa8]", "ctx+0xA8"),
    0x0033C183: (0x0033C144, "movzx eax, byte ptr [rbx + 0x20]", "byte st+0x20 * pi/128, wrapped once"),
    0x0033C807: (0x0033C7D2, "movzx eax, byte ptr [rbx + 0x20]", "byte st+0x20 * pi/128, wrapped once"),
    0x0033CE3C: (0x0033CDFC, "movaps xmm6, xmm1", "the dispatcher's desired heading (mode 5)"),
    0x0033CE9D: (0x0033CE8A, "movaps xmm6, xmm1", "the dispatcher's desired heading (mode 3)"),
    0x0033D2A8: (0x0033D29D, "movaps xmm1, xmm6", "0033D200's desired heading (dispatcher or 0033A720's candidate)"),
    0x0033E1B7: (0x0033E198, "call 0x4687f0", "004687F0 yaw"),
}
calls = sorted(a for a, k in img.calls_to(0x00334120) if k == "call")
check("S11", calls == sorted(T) and all(txt(v[0]) == v[1] for v in T.values()),
      "00334120 has exactly the nine direct calls; targets: " + "; ".join("%08X %s" % (a, T[a][2]) for a in sorted(T)))
ctxa8 = []
for r in img.ROOTS:
    if 0x00330000 <= r < 0x00342000:
        for x in img.fn_ins(r):
            if x.operands and x.operands[0].type == X86_OP_MEM and x.operands[0].mem.disp == 0xA8 and x.mnemonic.startswith("mov") \
                    and x.reg_name(x.operands[0].mem.base) not in ("rsp", "rbp"):
                ctxa8.append(x.address)
check("S12", sorted(ctxa8) == [0x00336A5D] and txt(0x00336A54) == "call 0x4687f0",
      "ctx+0xA8 has one store in the solver band (00336A5D in BuildSolverContext), 004687F0's yaw toward the target")
check("S13", txt(0x0033C14F) == "mulss xmm1, xmm7" and txt(0x0033C153) == "mulss xmm1, dword ptr [rip + 0x5899d9]"
      and abs(f32(0x008C5B34) - 1 / 128) < 1e-9 and txt(0x0033C160) == "addss xmm1, xmm6" and abs(f32(0x00915624) + 2 * PI) < 1e-5
      and txt(0x0033C1CE) == "mov byte ptr [rbx + 0x20], al",
      "0033C183 / 0033C807: target = b * pi / 128 for a byte b, minus 2pi when above pi: always in (-pi, pi]")
# 002FDC30 -> st+0x150 (with st+0x160 = 2) = 00312B40's heading output
check("S14", txt(0x002FDC5C) == "movss xmm0, dword ptr [rdi + 0xe0]" and txt(0x002FDC95) == "call 0x312b40"
      and txt(0x002FDCB7) == "movss dword ptr [rdi + 0x150], xmm0" and txt(0x002FDCC7) == "mov dword ptr [rdi + 0x160], 2"
      and txt(0x002FDD4D) == "movss dword ptr [rdi + 0x150], xmm0",
      "002FDC30 sets st+0x160 = 2 and st+0x150 = the heading 00312B40 leaves in its in/out slot (seeded with st+0xE0)")
outs = [a for a in (0x00312BBE, 0x00312BF1, 0x00312C39, 0x00312C8C, 0x00312CD6, 0x00312CF5, 0x00312D11, 0x00312D2D, 0x00312D5E)]
check("S15", all("dword ptr [rbx]" in txt(a) for a in outs) and txt(0x00312BB9) == "call 0x316da0" and txt(0x00312BEC) == "call 0x31ac90"
      and txt(0x00312C84) == "mov ecx, dword ptr [rax + 0x70]" and txt(0x00316DAF) == "jbe 0x316dc9" and txt(0x00316DC7) == "ja 0x316dc0"
      and txt(0x0031ACB7) == "jmp 0x861f02" and txt(0x0031ACB3) == "movaps xmm0, xmm2",
      "00312B40's nine heading outputs are 00316DA0 (loop wrap, no fast path), 0031AC90 (atan2f, or the slot's current value), "
      "or the spawn record's +0x70")
sp70 = [0x0023929C, 0x0030046E, 0x00307A4F, 0x003120F7]
check("S16", all(txt(a).startswith("movss dword ptr [rax + 0x70]") for a in sp70) and txt(0x00239287) == "call 0x316da0",
      "spawn record +0x70 writers (00239210 = 00316DA0-wrapped degrees; 003003F0, 00307300, 00311F70 = the facings above) "
      "match the spawn-keep field map's writer list")
# 0033A720: the candidate headings are 004687F0's base plus table offsets of magnitude <= 3pi/4
offs = list(struct.unpack("<48f", img.rd(0x00D10B30, 192)))
imms = [struct.unpack("<f", struct.pack("<I", v))[0] for v in (0x3F060A92, 0x3FC90FDB, 0xBFC90FDB, 0x3F490FDB)] + [f32(0x0091572C), f32(0x00915730), f32(0x00D10B1C)]
mo = max(abs(v) for v in offs + imms)
check("S17", txt(0x0033A9EA) == "call 0x4687f0" and txt(0x0033A9F8) == "movaps xmm7, xmm0" and txt(0x0033ACC1) == "addss xmm3, dword ptr [r14 + rax*4]"
      and mo <= 0.75 * PI + 1e-6,
      "0033A720's candidate heading = 004687F0's yaw + a table offset; max |offset| over 00D10B30-00D10BEF and the "
      "immediates = %.4f (3pi/4 = %.4f), so every sum is < 4pi and its inline wrap takes the loop path" % (mo, 0.75 * PI))
lut = struct.unpack("<16384f", img.rd(0x00D12590, 16384 * 4))
check("S18", txt(0x0046F4A0) == "and eax, 0x3fff" and txt(0x0046F4A5) == "movss xmm0, dword ptr [rcx + rax*4]"
      and min(lut) >= 0.0 and max(lut) <= PI + 1e-6 and txt(0x0046885B) == "comiss xmm6, dword ptr [rbx]"
      and txt(0x00468860) == "mulss xmm0, dword ptr [rip + 0x1883434]",
      "004687F0's angle is the 16,384-entry table at 00D12590 (min %.4f, max %.4f) negated for x < 0: in [-pi, pi]"
      % (min(lut), max(lut)))

# ---------------------------------------------------------------- executed: 0033CB70 at and beyond 4pi
E = emu.Emu([(0x0033CB70, 0x0033CBF0)])
FOUR = f32(0x00D10B0C)
TWO = f32(0x01CEBC78)


def norm(x):
    return E.call(0x0033CB70, [x])[0]


def model(x):
    """OPUS's M1 model (sd184_range.py), in float32."""
    x = emu.r32(x)
    if x > FOUR or -FOUR > x:
        return emu.r32(x - emu.r32(float(int(emu.r32(x / TWO))) * TWO))
    while x > f32(0x01CEBC50):
        x = emu.r32(x - TWO)
    while f32(0x00915620) > x:
        x = emu.r32(x + TWO)
    return x


up = emu.b2f(emu.f2b(FOUR) + 1)
res = {x: norm(x) for x in (FOUR, up, -FOUR, emu.b2f(emu.f2b(-FOUR) + 1), 13.0, 16.0, -16.0, 5.846853, 20.0)}
check("E1", -PI <= res[FOUR] <= PI and -PI <= res[up] <= PI and abs(res[16.0] - 3.4336) < 1e-3 and abs(res[-16.0] + 3.4336) < 1e-3
      and -PI <= res[5.846853] <= PI,
      "executed 0033CB70: 4pi -> %.6f (loop path), next float up %.7f -> %.6f (fast path, in range), 16.0 -> %.4f, "
      "-16.0 -> %.4f, 13.0 -> %.4f, 20.0 -> %.4f, the largest authored facing 5.846853 -> %.6f"
      % (res[FOUR], up, res[up], res[16.0], res[-16.0], res[13.0], res[20.0], res[5.846853]))
grid = [i * 0.001 for i in range(-40000, 40001)]
bad_in = [x for x in grid if abs(emu.r32(x)) <= FOUR and not (-PI - 1e-6 <= norm(x) <= PI + 1e-6)]
out = [x for x in grid if not (-PI - 1e-6 <= norm(x) <= PI + 1e-6)]
mism = [x for x in grid[::7] if norm(x) != model(x)]
first = min(x for x in out if x > 0)
check("E2", not bad_in and not mism and abs(first - 5 * PI) < 2e-3 and all(abs(x) > 5 * PI - 2e-3 for x in out),
      "executed sweep of 80,001 inputs in [-40, 40]: none with |x| <= 4pi leaves [-pi, pi]; %d inputs do, the smallest "
      "positive %.3f (5pi = %.4f): the defect needs |x| > 5pi, not just > 4pi; OPUS's model agrees on every 7th point (%d mismatches)"
      % (len(out), first, 5 * PI, len(mism)))
bands = sorted(set(int(abs(x) / PI) for x in out))
check("E3", bands == [5, 7, 9, 11],
      "the mis-normalised inputs fill the odd bands |x| in (5pi, 6pi), (7pi, 8pi), ... (bands seen: %s): the fast path "
      "leaves x mod 2pi in [0, 2pi) instead of [-pi, pi]" % bands)

# ---------------------------------------------------------------- executed: the approach helper with an authored out-of-range facing
A = emu.Emu([(0x00334120, 0x00334194), (0x0033CB70, 0x0033CBF0)])
r_early = A.call(0x00334120, [0.0, 5.846853, 10.0])[0]
r_turn = A.call(0x00334120, [5.846853, 0.5, 0.1])[0]
r_near = A.call(0x00334120, [5.846853, 0.5, 2.0])[0]
check("E4", abs(r_early - 5.846853) < 1e-6 and -PI <= r_turn <= PI and abs(r_near - 0.5) < 1e-6,
      "executed 00334120(cur, target, step): (0, 5.846853, 10) -> %.6f (early path, target returned raw); "
      "(5.846853, 0.5, 0.1) -> %.6f (cur - step wrapped by the loop path); (5.846853, 0.5, 2.0) -> %.6f"
      % (r_early, r_turn, r_near))
r_big = A.call(0x00334120, [16.5, 0.0, 0.1])[0]
check("E5", not (-PI <= r_big <= PI),
      "executed 00334120(16.5, 0, 0.1) -> %.4f: a current heading beyond 5pi comes back outside [-pi, pi] "
      "(the defect reaches st+0xE0 only if a caller feeds such a heading)" % r_big)

# ---------------------------------------------------------------- executed controls: the wraps that do not share the defect
W = emu.Emu([(0x00316DA0, 0x00316DEA)])
wv = [W.call(0x00316DA0, [x, 0.0])[0] for x in (16.0, -16.0, 5.846853, 40.0)]
O = emu.Emu([(0x0026A0D0, 0x0026A131)])
obj, ms = emu.HEAP, emu.HEAP + 0x1000
O.mu.mem_write(obj + 3, bytes([0x60]))
O.mu.mem_write(obj + 0xB8, struct.pack("<Q", ms))
av = []
for x in (16.0, -16.0, 5.846853, 40.0):
    O.call(0x0026A0D0, [0.0, x], rcx=obj)
    av.append(O.f32(ms + 0xA4))
check("E6", all(-PI <= v <= PI for v in wv + av),
      "executed controls: 00316DA0 (loop wrap) gives %s and 0026A0D0 (the sign-biased wrap into movementState +0xA4, "
      "object kind byte 0x60 injected) gives %s for 16, -16, 5.846853, 40 - all in [-pi, pi]"
      % (["%.4f" % v for v in wv], ["%.4f" % v for v in av]))
Y = emu.Emu([(0x00460000, 0x00470000), (0x00202000, 0x00204000), (0x00808C40, 0x00808C60)], thunks=[0x00861F14])
vec = emu.HEAP + 0x2000
yaws = []
for k in range(0, 360, 5):
    a = math.radians(k)
    Y.mu.mem_write(vec, struct.pack("<4f", math.sin(a) * 3.0, 0.0, math.cos(a) * 3.0, 1.0))
    yaws.append(Y.call(0x004687F0, [], rcx=vec)[0])
check("E7", all(-PI - 1e-6 <= v <= PI + 1e-6 for v in yaws) and min(yaws) < -3.0 and max(yaws) > 3.0,
      "executed 004687F0 on 72 directions around the circle: yaw in [%.4f, %.4f] (float32 pi = 3.1415927 allowed) (stub: sqrtf answered in Python; %s)"
      % (min(yaws), max(yaws), sorted(set(Y.calls))))
print("FAILS %d" % len(FAILS))
