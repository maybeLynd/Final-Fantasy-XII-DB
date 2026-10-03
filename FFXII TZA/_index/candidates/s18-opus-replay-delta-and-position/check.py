"""S-18: execute CONTRACT-heading-speed-to-position-delta.md's two entries, Movement_ComputeDeltaFromHeadingSpeed (002E4380)
and Actor_GetWorldPosition (00265020), as shipped code and compare every output bit-exactly with a decode of the contract
(LD-1..LD-6) and of the page it formalises (OPUS, 2026-09-25, block 307).

Evidence class: NATIVE-REPLAY (unicorn), live_game false. Whole SHA-asserted image mapped. NO application stub; entering any
function outside ALLOWED fails the case. THREE IMPORT BRIDGES, through their real IAT slots (PE import directory):
  00861F0E -> 008C2BB0 sinf, 00861F08 -> 008C2BA8 cosf, 00861F14 -> 008C2BB8 sqrtf (reached only via 003A1D30);
each returns float32(math.<fn>(x)) and RECORDS ITS ARGUMENT, which is how the angle wrap (LD-6) is measured directly.
Real helpers: 00267260 -> 003B7730 and 00264460 (the planar-branch predicate), 003A1D30 (sqrtf(fabs(x)) wrapper).
Not executed: 00424080 (the object-state override); the harness takes the body's own skip, [actor+0xC0] null or
dword [[actor+0xC0]] == -1.
Fixtures (planted data only): the actor (class byte +3, +8/+9 flags, +0xB8 movement block, +0xC0 context), the movement
block (+0xA0 pitch, +0xA4 yaw, +0xD0 speed, +0xF8), the context (+0x14F, +0x151, +0x138), the two globals 003B7730 reads
([02B40530], [02B40534]).
Writes result.json next to this file.
"""
import hashlib
import json
import math
import os
import struct

from unicorn import Uc, UcError, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE, UC_HOOK_MEM_UNMAPPED
from unicorn.x86_const import (UC_X86_REG_RSP, UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_R9, UC_X86_REG_RIP,
                               UC_X86_REG_XMM0)

EXE = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe"
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
FUNCS = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\graph\functions.tsv"
IMG = 0x120000
STACK, STACK_SZ, RET, WORLD, BRIDGE = 0x70000000, 0x100000, 0x71000000, 0x72000000, 0x74000000
ACTOR, MOVE, CTX, OUT, VEC, POS = WORLD, WORLD + 0x1000, WORLD + 0x2000, WORLD + 0x3000, WORLD + 0x3100, WORLD + 0x3200
DELTA, GETPOS = 0x2E4380, 0x265020
G1, G2 = 0x2B40530, 0x2B40534
IAT = {0x8C2BB0: "sinf", 0x8C2BA8: "cosf", 0x8C2BB8: "sqrtf"}
ALLOWED = {DELTA, GETPOS, 0x267260, 0x3B7730, 0x264460, 0x3A1D30, 0x861F0E, 0x861F08, 0x861F14}


def f32(x):
    try:
        return struct.unpack("<f", struct.pack("<f", x))[0]
    except OverflowError:                       # beyond FLT_MAX + half an ulp: single precision rounds to infinity
        return math.copysign(float("inf"), x)


def bits(x):
    return struct.unpack("<I", struct.pack("<f", x))[0]


FN = {"sinf": lambda x: f32(math.sin(x)), "cosf": lambda x: f32(math.cos(x)), "sqrtf": lambda x: f32(math.sqrt(x))}

raw = open(EXE, "rb").read()
assert hashlib.sha256(raw).hexdigest() == SHA
pe = struct.unpack_from("<I", raw, 0x3C)[0]
nsec = struct.unpack_from("<H", raw, pe + 6)[0]
optsz = struct.unpack_from("<H", raw, pe + 20)[0]
secs, off = [], pe + 24 + optsz
for _ in range(nsec):
    vs, va, rs, ra = struct.unpack_from("<IIII", raw, off + 8)
    secs.append((va + IMG, vs, ra, rs))
    off += 40
FSTARTS = set(int(l.split("\t")[0], 16) for l in open(FUNCS, encoding="utf-8", errors="replace") if l[:1] in "0123456789ABCDEF")

uc = Uc(UC_ARCH_X86, UC_MODE_64)
for v, vs, ra, rs in secs:
    lo, hi = v & ~0xFFF, (v + max(vs, rs) + 0xFFF) & ~0xFFF
    uc.mem_map(lo, hi - lo)
    uc.mem_write(v, raw[ra:ra + min(rs, max(vs, rs))])
uc.mem_map(STACK, STACK_SZ)
uc.mem_map(RET, 0x1000)
uc.mem_map(WORLD, 0x10000)
uc.mem_map(BRIDGE, 0x1000)
uc.mem_write(RET, bytes([0xF4]))
BR = {}
for i, (slot, name) in enumerate(sorted(IAT.items())):
    a = BRIDGE + 0x10 * i
    uc.mem_write(a, bytes([0xC3]))
    uc.mem_write(slot, struct.pack("<Q", a))
    BR[a] = name
state = {"bad": [], "faults": [], "entered": set(), "bridge": []}


def on_code(u, a, n, _):
    if a in BR:
        x = struct.unpack("<f", bytes(u.reg_read(UC_X86_REG_XMM0).to_bytes(16, "little")[:4]))[0]
        y = FN[BR[a]](x)
        u.reg_write(UC_X86_REG_XMM0, struct.unpack("<I", struct.pack("<f", y))[0])
        state["bridge"].append((BR[a], x))
        return
    if a in FSTARTS:
        state["entered"].add(a)
        if a not in ALLOWED:
            state["bad"].append("%08X" % a)
            u.emu_stop()


def on_bad(u, ac, a, n, v, _):
    state["faults"].append("%08X" % a)
    return False


uc.hook_add(UC_HOOK_CODE, on_code)
uc.hook_add(UC_HOOK_MEM_UNMAPPED, on_bad)


def call(entry, rcx, rdx=0, r8=0, r9=0):
    sp = STACK + STACK_SZ - 0x1000 - 8
    uc.mem_write(sp, struct.pack("<Q", RET))
    uc.reg_write(UC_X86_REG_RSP, sp)
    for r, v in ((UC_X86_REG_RCX, rcx), (UC_X86_REG_RDX, rdx), (UC_X86_REG_R8, r8), (UC_X86_REG_R9, r9)):
        uc.reg_write(r, v & 0xFFFFFFFFFFFFFFFF)
    state["bad"], state["faults"], state["entered"], state["bridge"] = [], [], set(), []
    try:
        uc.emu_start(entry, RET, count=100000)
    except UcError as e:
        state["faults"].append(str(e))
    return uc.reg_read(UC_X86_REG_RIP) == RET and not state["bad"] and not state["faults"]


def world(cls=0x60, pitch=0.0, yaw=0.0, speed=0.0, f8=0.5, ctx=False, ctx_id=0xFFFFFFFF, c14f=0, c151=0, c138=1,
          a8=0, a9=0, g=(1, 1)):
    uc.mem_write(WORLD, bytes(0x3400))
    a = bytearray(0x100)
    a[3] = cls
    a[8], a[9] = a8, a9
    struct.pack_into("<Q", a, 0xB8, MOVE)
    struct.pack_into("<Q", a, 0xC0, CTX if ctx else 0)
    uc.mem_write(ACTOR, bytes(a))
    m = bytearray(0x100)
    struct.pack_into("<fff", m, 0, 11.5, -2.25, 300.0)            # the position the getter reads (+0/+4/+8)
    struct.pack_into("<ff", m, 0xA0, pitch, yaw)
    struct.pack_into("<f", m, 0xD0, speed)
    struct.pack_into("<f", m, 0xF8, f8)
    uc.mem_write(MOVE, bytes(m))
    c = bytearray(0x200)
    struct.pack_into("<I", c, 0, ctx_id)
    c[0x14F], c[0x151] = c14f, c151
    struct.pack_into("<Q", c, 0x138, c138)
    uc.mem_write(CTX, bytes(c))
    uc.mem_write(G1, struct.pack("<ii", *g))


def read_out():
    return struct.unpack("<4f", bytes(uc.mem_read(OUT, 16)))


def rd_f(a):
    return struct.unpack("<f", bytes(uc.mem_read(a, 4)))[0]


# ---- decode ----
PI, NPI, TWOPI = struct.unpack("<fff", bytes.fromhex("db0f4940") + bytes.fromhex("db0f49c0") + bytes.fromhex("db0fc940"))


def cvtt(x):
    if math.isnan(x) or not (-2147483648.0 <= x < 2147483648.0):
        return -2147483648
    return int(x)


def wrap(a, pos_branch):
    """002E4464..002E44EF: c = +pi if the angle >= 0 (comiss; NaN -> -pi) else -pi; ((a + c) - trunc((a + c)/2pi)*2pi) - c,
    every step single precision."""
    c = PI if pos_branch else NPI
    t = f32(a + c)
    q = f32(t / TWOPI)
    t = f32(t - f32(f32(float(cvtt(q))) * TWOPI))
    return f32(t - c)


def planar_pred(w):
    ctx, g = w.get("ctx", False), w.get("g", (1, 1))
    p267 = (g[0] != 0 and g[1] != 0 and ctx and not (w.get("c14f", 0) & 1) and w.get("c138", 1) != 0
            and (w.get("a9", 0) & 1) and ((w.get("a8", 0) >> 1) & 1))
    p264 = ctx and ((w.get("c151", 0) | (w.get("c151", 0) >> 1)) & 1)
    return bool(p267) and not p264


def decode_delta(w):
    """Returns (out4, f8_after, expected bridge args) for r8d == 0."""
    cls = w.get("cls", 0x60)
    if cls & 0xE0 != 0x60:
        return (0.0, 0.0, 0.0, 1.0), w.get("f8", 0.5), []
    pitch, yaw, speed, f8 = (f32(w.get(k, d)) for k, d in (("pitch", 0.0), ("yaw", 0.0), ("speed", 0.0), ("f8", 0.5)))
    if 0.0 > f8:
        f8 = speed
    yw = wrap(yaw, not (yaw < 0.0 or math.isnan(yaw)))
    pw = wrap(pitch, pitch >= 0.0)
    if speed == 0.0:
        return (0.0, 0.0, 0.0, 1.0), f8, []
    args = []
    if planar_pred(w):
        y, h = 0.0, speed
    else:
        y = f32(FN["sinf"](pw) * speed)
        h = f32(speed * FN["cosf"](pw))
        args += [("sinf", pw), ("cosf", pw)]
    x = f32(FN["sinf"](yw) * h)
    z = f32(FN["cosf"](yw) * h)
    args += [("sinf", yw), ("cosf", yw)]
    return (x, y, z, 1.0), f8, args


def same(a, b):
    return all(bits(p) == bits(q) for p, q in zip(a, b))


results, allok = {}, True


def record(name, ok, **kw):
    global allok
    allok &= ok
    results[name] = dict(pass_=ok, **kw)
    print("%-30s %s  %s" % (name, "PASS" if ok else "FAIL", {k: v for k, v in kw.items() if k in ("n", "mismatches", "note")}))


# 1. LD-1 / LD-3 / LD-5: all 256 class bytes; output pre-filled with 0xAA; refused -> exactly {0,0,0,1.0}, no bridge call
mism, n = [], 0
for cls in range(256):
    world(cls=cls, pitch=0.3, yaw=1.1, speed=2.0)
    uc.mem_write(OUT, b"\xAA" * 16)
    ok = call(DELTA, ACTOR, OUT, 0, VEC)
    n += 1
    exp, _, args = decode_delta({"cls": cls, "pitch": 0.3, "yaw": 1.1, "speed": 2.0})
    got = read_out()
    if not ok or not same(got, exp) or [b[0] for b in state["bridge"]] != [a[0] for a in args]:
        mism.append([cls, list(got), list(exp), ok])
accepted = [c for c in range(256) if c & 0xE0 == 0x60]
record("delta_class_gate_LD1_LD3_LD5", not mism, n=n, mismatches=len(mism), detail=mism[:10],
       accepted_class_bytes="0x%02X..0x%02X (%d)" % (accepted[0], accepted[-1], len(accepted)),
       note="refused output exactly {0,0,0,1.0} over a 0xAA-filled buffer")

# 2. LD-4 + LD-6 + the speed/F8 edges: a grid, spherical branch (no context)
angles = [0.0, 0.5, -0.5, 1.5707964, -1.5707964, 3.0, -3.0, PI, NPI, 3.1415925, -3.1415925, 4.0, -4.0, 7.0, -7.0,
          6.2831855, -6.2831855, 100.0, -100.0, 12345.678]
speeds = [0.0, 1.5, 7.25, -2.0]
mism, n, wrap_seen = [], 0, {}
for yaw in angles:
    for pitch in angles:
        for speed in speeds:
            for f8 in (0.5, -1.0):
                w = {"pitch": pitch, "yaw": yaw, "speed": speed, "f8": f8}
                world(**w)
                uc.mem_write(OUT, b"\xAA" * 16)
                ok = call(DELTA, ACTOR, OUT, 0, VEC)
                n += 1
                exp, f8e, args = decode_delta(w)
                got, f8g = read_out(), rd_f(MOVE + 0xF8)
                gargs = [(b[0], bits(b[1])) for b in state["bridge"]]
                eargs = [(b[0], bits(b[1])) for b in args]
                if not ok or not same(got, exp) or bits(f8g) != bits(f8e) or gargs != eargs:
                    mism.append([yaw, pitch, speed, f8, list(got), list(exp), f8g, f8e, ok])
                if speed != 0.0 and state["bridge"]:
                    wrap_seen[repr(f32(yaw))] = state["bridge"][-1][1]
rng = sorted(set(wrap_seen.values()))
record("delta_spherical_LD4_LD6_grid", not mism, n=n, mismatches=len(mism), detail=mism[:10],
       wrapped_yaw_min=rng[0], wrapped_yaw_max=rng[-1],
       wrap_of_plus_pi=wrap_seen.get(repr(PI)), wrap_of_minus_pi=wrap_seen.get(repr(NPI)),
       note="every output bit-exact; the sinf/cosf arguments are the wrapped angles")

# 3. the planar branch: the predicate's truth table (context present, override skipped by dword [ctx] == -1)
mism, n, planar_n = [], 0, 0
for g in ((1, 1), (0, 1), (1, 0)):
    for c14f in (0, 1):
        for c138 in (0, 1):
            for a9 in (0, 1):
                for a8 in (0, 2):
                    for c151 in (0, 1, 2):
                        w = {"pitch": 0.7, "yaw": -2.2, "speed": 3.5, "ctx": True, "g": g, "c14f": c14f, "c138": c138,
                             "a9": a9, "a8": a8, "c151": c151}
                        world(**w)
                        ok = call(DELTA, ACTOR, OUT, 0, VEC)
                        n += 1
                        planar_n += planar_pred(w)
                        exp, _, _ = decode_delta(w)
                        if not ok or not same(read_out(), exp):
                            mism.append([g, c14f, c138, a9, a8, c151, list(read_out()), list(exp), ok])
world(pitch=0.7, yaw=-2.2, speed=3.5, ctx=True, g=(1, 1), a9=1, a8=2)
call(DELTA, ACTOR, OUT, 0, VEC)
planar_example = list(read_out())
record("delta_planar_branch", not mism, n=n, mismatches=len(mism), detail=mism[:10], planar_cases=planar_n,
       planar_example_pitch_0p7=planar_example,
       note="planar when 00267260(actor) != 0 and 00264460(actor) == 0: Y = 0 and no cos(pitch) on X/Z")

# 4. the r8d != 0 arm: out = the caller's vector, W = 1.0, +0xF8 = sqrtf(|x*x + y*y + z*z|) via 003A1D30
mism, n = [], 0
for v in ((3.0, 4.0, 12.0), (0.0, 0.0, 0.0), (-1.5, 2.5, -0.25), (1e20, 1e20, 0.0)):
    world(pitch=0.3, yaw=1.0, speed=9.0, f8=0.5)
    uc.mem_write(VEC, struct.pack("<3f", *v))
    ok = call(DELTA, ACTOR, OUT, 1, VEC)
    n += 1
    x, y, z = (f32(c) for c in v)
    s = f32(f32(f32(x * x) + f32(y * y)) + f32(z * z))
    e8 = FN["sqrtf"](abs(s)) if not math.isinf(s) else float("inf")
    exp = (x, y, z, 1.0)
    if not ok or not same(read_out(), exp) or bits(rd_f(MOVE + 0xF8)) != bits(f32(e8)):
        mism.append([list(v), list(read_out()), rd_f(MOVE + 0xF8), e8, ok])
record("delta_vector_arm_r8_nonzero", not mism, n=n, mismatches=len(mism), detail=mism,
       note="not in the contract; the page's section 8 describes it")

# 5. LD-2: the position getter over all 256 class bytes and a null actor
mism, n, admitted = [], 0, set()
for cls in range(256):
    world(cls=cls)
    uc.mem_write(POS, b"\xAA" * 12)
    ok = call(GETPOS, ACTOR, POS, POS + 4, POS + 8)
    n += 1
    got = struct.unpack("<3f", bytes(uc.mem_read(POS, 12)))
    exp = (11.5, -2.25, 300.0) if (cls >> 5) in (1, 3) else (0.0, 0.0, 0.0)
    if (cls >> 5) in (1, 3):
        admitted.add(cls >> 5)
    if not ok or not same(got, exp):
        mism.append([cls, list(got), list(exp), ok])
uc.mem_write(POS, b"\xAA" * 12)
okn = call(GETPOS, 0, POS, POS + 4, POS + 8)
null_got = struct.unpack("<3f", bytes(uc.mem_read(POS, 12)))
record("getpos_LD2", not mism and okn and null_got == (0.0, 0.0, 0.0), n=n + 1, mismatches=len(mism), detail=mism[:10],
       admitted_classes=sorted(admitted), null_actor=list(null_got), note="classes {1,3} read +0xB8; others and null -> (0,0,0)")

json.dump({"pass": sum(1 for v in results.values() if v["pass_"]), "total": len(results), "ok": allok, "results": results},
          open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "result.json"), "w"), indent=1)
print("%d/%d pass" % (sum(1 for v in results.values() if v["pass_"]), len(results)))


# EXIT STATUS FOLLOWS THE RECORDED VERDICT (OPUS, 2026-10-03, the user's root-cause directive item 4): this package
# recorded "ok" in result.json but always exited 0, so no automated re-run could see it fail.
import json as _ej, os as _eo, sys as _es
_es.exit(0 if _ej.load(open(_eo.path.join(_eo.path.dirname(_eo.path.abspath(__file__)), "result.json"),
                            encoding="utf-8")).get("ok") is True else 1)
