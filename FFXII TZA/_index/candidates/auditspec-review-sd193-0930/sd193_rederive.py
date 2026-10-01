"""sd193_rederive.py - SWE2-AUDIT-SPEC independent re-derivation for SD-193 (003EC040's turn), 2026-09-30.

Own loader / harness (rvimg.py; sha asserted). Three evidence kinds, kept apart:
  D  decoded instructions of 003EC040 and its helpers (static), printed as the branch facts they establish.
  X  isolated execution (unicorn) of the ORIGINAL bytes of 003A1AD0, 003EC510, 003A1980, and of 003EC040 itself with
     injected state (a render-record table, a rate record); compared against a reference written here from the decode
     (not against the package's M1 model).  Stubs: only 00422D50 in the X6 hold case (named there).
  W  every instruction image-wide that addresses 01DFE0BC (rip-relative, or image-base-relative 0x1CDE0BC displacement)
     classified read / write by mnemonic + first operand.
"""
import math, struct, random
import rvimg as V
from rvimg import r32

PI, TWO_PI = V.f32(0x01CEBC50), V.f32(0x01CEBC78)
fails = 0


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


def txt(a):
    i = V.dis(a, a + 16)[0]
    return ("%s %s" % (i.mnemonic, i.op_str)).strip()


# ---------------------------------------------------------------- D: decode facts
print("== D: decoded branch structure of 003EC040")
D = {
    0x003EC05E: "cmp cx, -1", 0x003EC062: "je 0x3ec1ec",                                  # index -1 -> 0
    0x003EC07C: "cmp dword ptr [rbx + 0x284], eax", 0x003EC082: "cmove rbx, rax",          # +0x284 == 0 -> 0
    0x003EC094: "mov ebp, dword ptr [rbx + 0x290]", 0x003EC09A: "and ebp, 0x100000",
    0x003EC0A2: "test dword ptr [rbx + 0x284], 0x8000000", 0x003EC0AE: "cmp word ptr [rbx + 6], -1",
    0x003EC0B5: "xorps xmm0, xmm0",
    0x003EC10C: "test ebp, ebp", 0x003EC10E: "jne 0x3ec117", 0x003EC110: "cmp word ptr [rbx + 6], -1",
    0x003EC115: "jne 0x3ec124", 0x003EC124: "movaps xmm0, xmm7",                          # <- the unlisted target return
    0x003EC11A: "call 0x3e56c0",
    0x003EC1C3: "comiss xmm6, xmm0", 0x003EC1C6: "ja 0x3ec1e7",
    0x003EC1CC: "addss xmm6, dword ptr [rbx + 0x124]", 0x003EC1E1: "subss xmm0, xmm6", 0x003EC1E5: "jmp 0x3ec184",
}
bad = [("%08X" % a, t, txt(a)) for a, t in D.items() if txt(a) != t]
check("D1", not bad, "003EC040 branch instructions as read (%d checked) %s" % (len(D), bad))
# the mode-0/1 result goes to 003EC184 -> epilogue with no wrap call between
tail = [txt(a) for a in (0x003EC184, 0x003EC189, 0x003EC18E, 0x003EC193, 0x003EC198, 0x003EC19D, 0x003EC1A2, 0x003EC1A6, 0x003EC1A8)]
check("D2", all(not t.startswith("call") for t in tail) and tail[-1] == "ret",
      "modes 0/1 return cur +- step with no wrap (003EC184..003EC1A8 is the epilogue only)")
mul_rip = 0x003EC136 + 0x1A11F86, 0x003EC15A + 0x1A11F62 - 8 + 8
check("D3", 0x003EC136 + 0x1A11F86 == 0x01DFE0BC and 0x003EC15A + 0x1A11F62 == 0x01DFE0BC,
      "both step multipliers read 01DFE0BC")
# the boot fixup writes 0.5 only on the ecx != 0 arm of 001EDDC0
check("D4", txt(0x001EDDC4) == "test ecx, ecx" and txt(0x001EDDC6) == "je 0x1ede1f" and 0x001EDDD8 + 0x1AFDD98 == 0x01CEBB70
      and V.f32(0x01CEBB70) == 0.5 and txt(0x001EDDE0) == "movss dword ptr [rip + 0x1c102d4], xmm1" and V.f32(0x01DFE0BC) == 1.0,
      "01DFE0BC = 1.0 in the file; 001EDDE0 stores 0.5 only when 001EDDC0's ecx != 0 (je 0x1ede1f skips it)")

# ---------------------------------------------------------------- W: who writes 01DFE0BC
print("== W: image-wide references to 01DFE0BC")
TARGET = 0x01DFE0BC
WRITE_MN = ("mov", "movss", "movd", "movaps", "movups", "movq", "movlps", "movhps", "add", "sub", "and", "or", "xor",
            "inc", "dec", "addss", "subss", "mulss", "divss", "stos")
hits = []
for n, va, vs, p, rs, x in V.SECS:
    if not x:
        continue
    blob = V.raw[p:p + min(vs, rs)]
    # rip-relative: disp32 = TARGET - next_ip ; find candidate disp positions by arithmetic, then decode back
    for k in range(0, len(blob) - 4):
        d = struct.unpack_from("<i", blob, k)[0]
        site = va + k
        cand = None
        for ln in range(4, 12):            # disp at k, instruction end = k + 4 + imm bytes (0..4)
            pass
        # image-base relative: displacement 0x1CDE0BC
        if d == TARGET - V.IB:
            cand = "ib"
        elif 0 <= (TARGET - (site + 4)) - d <= 4 and -0x7FFFFFFF < d:
            cand = "rip"
        if cand:
            best = None
            for back in range(2, 11):
                st = site - back
                ins = V.dis(st, st + 15)
                if not ins:
                    continue
                i = ins[0]
                if i.address != st or not (st < site < st + i.size):
                    continue
                # pin: the dword AT site must be this operand's disp field; ghosts that merely
                # cover site while their own disp sits elsewhere are rejected.
                disp_at_site = struct.unpack("<i", i.bytes[site - st:site - st + 4])[0] if 0 <= site - st <= i.size - 4 else None
                ok = False
                for o in i.operands:
                    if o.type == 3:
                        m = o.mem
                        if m.base == 41 and i.address + i.size + m.disp == TARGET and m.disp == disp_at_site:    # X86_REG_RIP = 41
                            ok = True
                        elif m.base not in (0, 41) and m.disp == TARGET - V.IB and m.disp == disp_at_site:
                            ok = True
                if ok and (best is None or i.address < best.address):
                    best = i          # earliest start wins: a ghost starts inside the real instruction
            if best is not None:
                hits.append(best)
seen = {}
for i in hits:
    seen[i.address] = i
writes = []
for a in sorted(seen):
    i = seen[a]
    first = i.op_str.split(",")[0]
    w = i.mnemonic in WRITE_MN and "ptr [" in first
    if w:
        writes.append("%08X %s %s" % (a, i.mnemonic, i.op_str))
print("   referencing instructions: %d; writes: %s" % (len(seen), writes))
check("W1", writes == ["001EDDE0 movss dword ptr [rip + 0x1c102d4], xmm1"],
      "01DFE0BC has exactly one writing instruction image-wide (%d references)" % len(seen))
# positive control for W: the sweep must find the known reads in 003EC040 itself
check("W2", 0x003EC12E in seen and 0x003EC152 in seen, "control: the sweep finds 003EC040's two reads (003EC12E, 003EC152)")


# ---------------------------------------------------------------- X: isolated execution of the original bytes
print("== X: unicorn runs of the original bytes")
CODE = [(0x003EC040, 0x003EC1F1), (0x003EC510, 0x003EC577), (0x003A1980, 0x003A1997), (0x003A1AD0, 0x003A1BB0),
        (0x003E56C0, 0x003E56E0), (0x00422D50, 0x00422D6A)]


def ref_wrap(x):          # 003EC510 / 003A1AD0 loops: while -pi > x: x += 2pi ; while x > pi: x += -2pi (float32)
    while -PI > x:
        x = r32(x + TWO_PI)
    while x > PI:
        x = r32(x + -TWO_PI)
    return x


def ref_approach(cur, tgt, step):
    d = ref_wrap(r32(tgt - cur))
    a = r32(abs(d))
    m = a if a < step else step
    if m == step:
        out = r32(cur - m) if 0 > d else r32(cur + m)
    else:
        out = tgt
    return ref_wrap(out)


def ref_force(d, dr):
    d = ref_wrap(d)
    if d == 0.0:
        return 0.0
    if dr == 0:
        return r32(d + TWO_PI) if 0 > d else d
    if dr == 1:
        return r32(d + -TWO_PI) if d > 0 else d
    return d


E = V.Emu(CODE)
rnd = random.Random(193)
samples = [(r32(rnd.uniform(-7, 7)), r32(rnd.uniform(-7, 7)), r32(rnd.choice([0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 3.0])))
           for _ in range(4000)]
samples += [(0.0, 1.0, 0.25), (0.0, -1.0, 0.25), (0.0, r32(0.1), 0.25), (3.0, -3.0, 0.2), (0.0, 0.25, 0.25), (1.0, 1.0, 0.1)]
mis = [(c, t, s, E.call(0x003A1AD0, (c, t, s))[0], ref_approach(c, t, s)) for c, t, s in samples]
mis = [m for m in mis if m[3] != m[4]]
check("X1", not mis, "003A1AD0 executed on %d (cur, target, step) points equals the decoded reference bit-for-bit %s"
      % (len(samples), mis[:3]))
seam = E.call(0x003A1AD0, (3.0, -3.0, 0.2))[0]
check("X1b", abs(seam - r32(3.2 - TWO_PI)) < 1e-6, "seam: 003A1AD0(3.0, -3.0, 0.2) = %.6f (crosses +-pi the short way, re-wrapped)" % seam)
fs = [(r32(rnd.uniform(-20, 20)), dr) for _ in range(3000) for dr in (0, 1, 2)] + [(0.0, 0), (0.0, 1), (-0.0, 0)]
mis = [(d, dr, E.call(0x003EC510, (d,), ints=(0, dr))[0], ref_force(d, dr)) for d, dr in fs]
mis = [m for m in mis if m[2] != m[3]]
rng0 = [E.call(0x003EC510, (d,), ints=(0, 0))[0] for d, _ in fs[:600:3]]
rng1 = [E.call(0x003EC510, (d,), ints=(0, 1))[0] for d, _ in fs[:600:3]]
check("X2", not mis and min(rng0) >= 0.0 and max(rng1) <= 0.0,
      "003EC510 executed on %d (d, dir) points equals the reference; dir 0 output in [%.4f, %.4f], dir 1 in [%.4f, %.4f]"
      % (len(fs), min(rng0), max(rng0), min(rng1), max(rng1)))
mis = [(x, s) for x, s in [(r32(rnd.uniform(-9, 9)), r32(rnd.uniform(0, 4))) for _ in range(2000)]
       if E.call(0x003A1980, (x, s))[0] != min(r32(abs(x)), s)]
check("X3", not mis, "003A1980 executed = min(|x|, s) on 2000 points %s" % mis[:3])

# ---- 003EC040 itself, with an injected render-record table and rate record
TBL, IDX = V.HEAP, 1
REC = TBL + IDX * 0x740
BLK = V.HEAP + 0x8000
RATE = BLK + 0x40


def setup(cur, r24, r28, f290=0x100000, f284=1, w6=-1, anim=0x01, c4=-1, mult=None, have_rate=True):
    E.w(0x022C6F28, struct.pack("<Q", TBL))
    E.w(REC, b"\0" * 0x740)
    E.w(REC + 6, struct.pack("<h", w6))
    E.w(REC + 0xC4, struct.pack("<i", c4))
    E.w(REC + 0xCC, struct.pack("<h", anim))
    E.w32f(REC + 0x124, cur)
    E.w(REC + 0x284, struct.pack("<I", f284))
    E.w(REC + 0x290, struct.pack("<I", f290))
    E.w(REC + 0x400, struct.pack("<Q", BLK if have_rate else 0))
    E.w(BLK, b"\0" * 0x80)
    E.w(BLK + 0x12, struct.pack("<H", RATE - BLK))
    E.w32f(RATE + 0x24, r24)
    E.w32f(RATE + 0x28, r28)
    E.w32f(0x01DFE0BC, V.f32(0x01DFE0BC) if mult is None else mult)


def turn(tgt, mode, fast, idx=IDX):
    return E.call(0x003EC040, (None, tgt), ints=(idx & 0xFFFF, 0, mode, fast))[0]


res = {}
setup(0.0, 0.1, 0.3)
res["mode2"] = turn(1.0, 2, 0)
res["mode2_neg"] = turn(-1.0, 2, 0)
res["fast"] = turn(1.0, 2, 1)
res["fast_mode7"] = turn(1.0, 7, 1)
res["mode0"] = turn(-1.0, 0, 0)          # forced positive way round although -1 is nearer
res["mode1"] = turn(1.0, 1, 0)           # forced negative way round
res["mode0_snap"] = turn(0.05, 0, 0)
res["mode3"] = turn(1.0, 3, 0)
res["mode_neg"] = turn(1.0, -1, 0)
setup(0.0, 0.1, 0.3, mult=0.5)
res["mode2_mult05"] = turn(1.0, 2, 0)
setup(0.0, 0.1, 0.3, have_rate=False)
res["norate"] = turn(1.0, 2, 0)
setup(0.0, 0.1, 0.3, f284=0)
res["invalid"] = turn(1.0, 2, 0)
res["idx_m1"] = turn(1.0, 2, 0, idx=-1)
setup(0.0, 0.1, 0.3, f290=0, f284=0x8000000 | 1, w6=5)
res["parked"] = turn(1.0, 2, 0)
setup(0.0, 0.1, 0.3, f290=0, f284=1, w6=5)
res["flag_clear_w6_set"] = turn(1.0, 2, 0)            # the branch 003EC115 -> 003EC124
setup(0.0, 0.1, 0.3, f290=0, f284=1, w6=-1)
res["flag_clear_w6_m1"] = turn(1.0, 2, 0)
setup(2.0, 0.1, 0.3, f290=0, f284=1, w6=-1)
res["mode0_unwrapped"] = None
setup(3.1, 0.1, 0.3)
res["mode0_past_pi"] = turn(-3.0, 0, 0)
for k, v in res.items():
    if v is not None:
        print("   %-18s %.6f" % (k, v))
check("X4", res["mode2"] == r32(0.1) and res["mode2_neg"] == r32(-0.1) and res["fast"] == r32(0.3)
      and res["fast_mode7"] == r32(0.3) and res["mode0"] == r32(0.1) and res["mode1"] == r32(-0.1)
      and res["mode0_snap"] == r32(0.05) and res["mode3"] == r32(1.0) and res["mode_neg"] == r32(1.0)
      and res["mode2_mult05"] == r32(0.05) and res["norate"] == r32(1.0),
      "executed 003EC040: mode 2 steps +-rate(+0x24); fast steps rate(+0x28) for any mode; mode 0 / 1 step the forced way; "
      "snap within a step; modes 3 / -1 and no rate record return the target; multiplier 0.5 halves the step")
check("X5", res["invalid"] == 0.0 and res["idx_m1"] == 0.0 and res["parked"] == 0.0,
      "executed: +0x284 == 0, index -1, and (+0x290 bit 0x100000 clear, +0x284 bit 0x8000000 set, +6 != -1) return 0")
check("X6", res["flag_clear_w6_set"] == r32(1.0) and res["flag_clear_w6_m1"] == r32(0.1),
      "executed: +0x290 bit 0x100000 clear and +6 != -1 (bit 0x8000000 clear) returns the TARGET at once, in every mode "
      "(the package's case table lacks this row); with +6 == -1 it steps")
check("X7", res["mode0_past_pi"] > PI, "executed: mode 0 from 3.1 by 0.1 returns %.6f > pi (the mode-0/1 result is not wrapped)"
      % res["mode0_past_pi"])

# hold case: stub 00422D50 (and only it) to return an object whose +0x370 + +0x378 names a byte pair with [+1] == 1
OBJ, ST = V.HEAP + 0x9000, V.HEAP + 0xA000
E.w(OBJ, b"\0" * 0x400)
E.w(OBJ + 0x370, struct.pack("<I", ST))
E.w(OBJ + 0x378, struct.pack("<I", 0))
E.w(ST, b"\0\x01")
E.stubs[0x00422D50] = lambda emu: (OBJ, None)
holds = {}
for anim in (0x0D, 0x35, 0x36, 0x0E, 0x1035):
    setup(0.7, 0.1, 0.3, anim=anim)
    holds[anim] = turn(2.0, 2, 0)
E.w(ST, b"\0\x02")
setup(0.7, 0.1, 0.3, anim=0x35)
holds["state2"] = turn(2.0, 2, 0)
del E.stubs[0x00422D50]
print("   hold (stub 00422D50):", {("%X" % k if isinstance(k, int) else k): round(v, 6) for k, v in holds.items()})
check("X8", holds[0x0D] == r32(0.7) and holds[0x35] == r32(0.7) and holds[0x36] == r32(0.7) and holds[0x1035] == r32(0.7)
      and holds[0x0E] == r32(0.8) and holds["state2"] == r32(0.8),
      "executed (00422D50 stubbed): animation id 0x0D/0x35/0x36 (low 12 bits) in state byte 1 holds +0x124; other ids or "
      "state 2 step")

# constant rate: iterate the executed function, feeding its result back into +0x124
setup(0.0, 0.1, 0.3)
seq, cur = [], 0.0
for _ in range(14):
    E.w32f(REC + 0x124, cur)
    nxt = turn(1.25, 2, 0)
    seq.append(r32(nxt - cur))
    cur = nxt
print("   per-call deltas toward 1.25 at rate 0.1:", ["%.4f" % d for d in seq])
steps = [d for d in seq if d != 0.0]
check("X9", all(abs(d - r32(0.1)) < 2e-7 for d in steps[:-1]) and cur == r32(1.25) and 0 < steps[-1] <= r32(0.1) + 1e-7,
      "executed loop: %d equal steps of 0.1 then a final %.4f landing exactly on the target, then 0 - no easing"
      % (len(steps) - 1, steps[-1]))
print("FAILS %d" % fails)
