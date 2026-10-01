"""S-18: execute the ten entries of CONTRACT-facing-and-steering.md as shipped code over their whole static closure and test
the contract's section 4 / 7 / 10 / 12 claims by memory diff (OPUS, 2026-09-25, block 308).

Evidence class: NATIVE-REPLAY (unicorn), live_game false. Whole SHA-asserted image mapped. NO application stub.
ALLOWED = the union of the ten entries' static closures over edges.tsv (68 functions); entering anything else fails.
THREE IMPORT BRIDGES through their real IAT slots (PE import directory): 00861F02 -> 008C2BD0 atan2f, 00861F08 -> 008C2BA8
cosf, 00861F0E -> 008C2BB0 sinf (reached by the pop / mode-0 paths only).
TWO STOP BOUNDARIES (not stubs; the run ends there and the arguments are recorded): 004288B0 and 003B3CA0, the two calls of
the 003EC260 commit block. Nothing after a boundary is observed.
Fixtures (planted data only): the actor (+3 class, +0x0D, +0x18, +0xB8, +0xC0), the movement context (+0xA8, +0xAC,
+0xDC, +0xF0, the two SteeringRecords at +0x120 / +0x1A0), the secondary context (dword id at +0, +0x138 body), the
render-record array base [022C6F28] (003EC283's RIP operand) and one record, the FrameLimit base [01DFE0B4].
Writes result.json next to this file.
"""
import collections
import csv
import hashlib
import json
import math
import os
import struct

from unicorn import Uc, UcError, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE, UC_HOOK_MEM_UNMAPPED
from unicorn.x86_const import (UC_X86_REG_RSP, UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_RIP,
                               UC_X86_REG_XMM0, UC_X86_REG_XMM1)

EXE = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe"
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
GRAPH = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\graph"
IMG = 0x120000
STACK, STACK_SZ, RET, WORLD, BRIDGE = 0x70000000, 0x100000, 0x71000000, 0x72000000, 0x74000000
ACTOR, CTX, CTX2, BODY, RR = WORLD, WORLD + 0x1000, WORLD + 0x2000, WORLD + 0x3000, WORLD + 0x10000
SLOT0, SLOT1 = CTX + 0x120, CTX + 0x1A0
RR_BASE_PTR, FRAMELIMIT = 0x22C6F28, 0x1DFE0B4
E = {"set_facing_v0": 0x26B5A0, "set_facing_v1": 0x26B620, "apply_wrapped": 0x26B6A0, "facing_tail": 0x26C090,
     "set_steering_mode": 0x26AE90, "set_movement_mode": 0x26C120, "select_slot": 0x269F90, "push": 0x2EAB80,
     "pop": 0x2EAAA0, "normalise_loop": 0x3A1C50}
BOUNDARY = {0x4288B0: "004288B0", 0x3B3CA0: "003B3CA0"}
IAT = {0x8C2BD0: "atan2f", 0x8C2BA8: "cosf", 0x8C2BB0: "sinf"}

raw = open(EXE, "rb").read()
assert hashlib.sha256(raw).hexdigest() == SHA
graph = collections.defaultdict(set)
for r in csv.DictReader(open(GRAPH + r"\edges.tsv", encoding="utf-8"), delimiter="\t"):
    if r["callee_external"] != "true":
        graph[int(r["caller"], 16)].add(int(r["callee"], 16))


def closure(s):
    seen, st = set(), [s]
    while st:
        x = st.pop()
        if x in seen or x in BOUNDARY:
            continue
        seen.add(x)
        st.extend(graph[x])
    return seen


ALLOWED = set()
for e in E.values():
    ALLOWED |= closure(e)
FSTARTS = set(int(l.split("\t")[0], 16) for l in open(GRAPH + r"\functions.tsv", encoding="utf-8", errors="replace")
              if l[:1] in "0123456789ABCDEF")
pe = struct.unpack_from("<I", raw, 0x3C)[0]
nsec = struct.unpack_from("<H", raw, pe + 6)[0]
optsz = struct.unpack_from("<H", raw, pe + 20)[0]
secs, off = [], pe + 24 + optsz
for _ in range(nsec):
    vs, va, rs, ra = struct.unpack_from("<IIII", raw, off + 8)
    secs.append((va + IMG, vs, ra, rs))
    off += 40

uc = Uc(UC_ARCH_X86, UC_MODE_64)
for v, vs, ra, rs in secs:
    lo, hi = v & ~0xFFF, (v + max(vs, rs) + 0xFFF) & ~0xFFF
    uc.mem_map(lo, hi - lo)
    uc.mem_write(v, raw[ra:ra + min(rs, max(vs, rs))])
uc.mem_map(STACK, STACK_SZ)
uc.mem_map(RET, 0x1000)
uc.mem_map(WORLD, 0x40000)
uc.mem_map(BRIDGE, 0x1000)
uc.mem_write(RET, bytes([0xF4]))
BR = {}
for i, (slot, name) in enumerate(sorted(IAT.items())):
    uc.mem_write(BRIDGE + 0x10 * i, bytes([0xC3]))
    uc.mem_write(slot, struct.pack("<Q", BRIDGE + 0x10 * i))
    BR[BRIDGE + 0x10 * i] = name
state = {"bad": [], "faults": [], "entered": set(), "boundary": None, "bridge": []}


def f32(x):
    return struct.unpack("<f", struct.pack("<f", x))[0]


def fbits(x):
    return struct.unpack("<I", struct.pack("<f", x))[0]


def _xf(u, r):
    return struct.unpack("<f", struct.pack("<I", u.reg_read(r) & 0xFFFFFFFF))[0]


def on_code(u, a, n, _):
    if a in BR:
        x = _xf(u, UC_X86_REG_XMM0)
        y = math.atan2(x, _xf(u, UC_X86_REG_XMM1)) if BR[a] == "atan2f" else (math.cos(x) if BR[a] == "cosf" else math.sin(x))
        u.reg_write(UC_X86_REG_XMM0, fbits(f32(y)))
        state["bridge"].append(BR[a])
        return
    if a in BOUNDARY:
        state["boundary"] = [BOUNDARY[a], u.reg_read(UC_X86_REG_RCX), u.reg_read(UC_X86_REG_RDX) & 0xFFFFFFFF]
        u.emu_stop()
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


def call(entry, rcx=0, rdx=0, r8=0, xmm0=None, xmm1=None):
    sp = STACK + STACK_SZ - 0x1000 - 8
    uc.mem_write(sp, struct.pack("<Q", RET))
    uc.reg_write(UC_X86_REG_RSP, sp)
    for r, v in ((UC_X86_REG_RCX, rcx), (UC_X86_REG_RDX, rdx), (UC_X86_REG_R8, r8)):
        uc.reg_write(r, v & 0xFFFFFFFFFFFFFFFF)
    if xmm0 is not None:
        uc.reg_write(UC_X86_REG_XMM0, fbits(xmm0))
    if xmm1 is not None:
        uc.reg_write(UC_X86_REG_XMM1, fbits(xmm1))
    state.update(bad=[], faults=[], entered=set(), boundary=None, bridge=[])
    try:
        uc.emu_start(entry, RET, count=500000)
    except UcError as e:
        state["faults"].append(str(e))
    if state["bad"] or state["faults"]:
        return False
    return uc.reg_read(UC_X86_REG_RIP) == RET or state["boundary"] is not None


def world(kind=3, a0d=0, a18=0, sel=0, ctx2=False, ctx2_id=0xFFFFFFFF, body=False, cursor=None):
    uc.mem_write(WORLD, bytes(0x40000))
    seq = {0: 0, 1: 1, 2: 3, 3: 5}.get(kind, 0)
    uc.mem_write(ACTOR + 3, bytes([(kind << 5) | seq]))
    uc.mem_write(ACTOR + 0x0D, bytes([a0d]))
    uc.mem_write(ACTOR + 0x18, bytes([a18]))
    uc.mem_write(ACTOR + 0xB8, struct.pack("<Q", CTX))
    uc.mem_write(ACTOR + 0xC0, struct.pack("<Q", CTX2 if ctx2 else 0))
    uc.mem_write(CTX + 0xDC, bytes([sel]))
    uc.mem_write(CTX + 0xF0, struct.pack("<Q", cursor if cursor is not None else SLOT0 + (sel << 7)))
    uc.mem_write(CTX2, struct.pack("<I", ctx2_id))
    uc.mem_write(CTX2 + 0x138, struct.pack("<Q", BODY if body else 0))
    uc.mem_write(RR_BASE_PTR, struct.pack("<Q", RR))


def snap():
    return bytes(uc.mem_read(WORLD, 0x40000))


def changed(a, b):
    return sorted({(i - (i % 4)) for i in range(len(a)) if a[i] != b[i]})


def rdf(a):
    return struct.unpack("<f", bytes(uc.mem_read(a, 4)))[0]


def wrf(a, x):
    uc.mem_write(a, struct.pack("<f", x))


def rdb(a):
    return uc.mem_read(a, 1)[0]


# ---- decode (contract section 10 / 12) ----
PI, NPI, TWOPI = struct.unpack("<fff", bytes.fromhex("db0f4940db0f49c0db0fc940"))


def wrap(h):
    """section 10's facing wrap: bias by sign (comiss: NaN -> -pi), truncating fmod, unbias - every step single precision"""
    bias = PI if h >= 0.0 else NPI
    t = f32(h + bias)
    q = f32(t / TWOPI)
    i = int(q) if (not math.isnan(q) and -2147483648.0 <= q < 2147483648.0) else -2147483648
    t = f32(t - f32(f32(float(i)) * TWOPI))
    return f32(t - bias)


def loop_norm(x):
    """section 10's steering normaliser 003A1C50"""
    while NPI > x:
        x = f32(x + TWOPI)
    while x > PI:
        x = f32(x - TWOPI)
    return x


results, allok = {}, True


def record(name, ok, **kw):
    global allok
    allok &= ok
    results[name] = dict(pass_=ok, **kw)
    print("%-38s %s  %s" % (name, "PASS" if ok else "FAIL", {k: v for k, v in kw.items() if k in ("n", "violations", "note")}))


def rel(offs):
    names = []
    for o in offs:
        a = WORLD + o
        for base, nm in ((RR, "rr"), (BODY, "body"), (CTX2, "ctx2"), (SLOT1, "slot1"), (SLOT0, "slot0"), (CTX, "ctx"), (ACTOR, "actor")):
            if a >= base:
                names.append("%s+%X" % (nm, a - base))
                break
    return names


# 1. select_slot 00269F90: section 4 "0 or 1 and nothing else", fail-open
viol = []
for sel in range(256):
    world(sel=0)
    uc.mem_write(CTX + 0xDC, bytes([sel]))
    uc.mem_write(CTX + 0xF0, struct.pack("<Q", 0x1122334455667788))
    b = snap()
    ok = call(E["select_slot"], CTX)
    exp = SLOT0 + (sel << 7) if sel <= 1 else 0x1122334455667788
    got = struct.unpack("<Q", bytes(uc.mem_read(CTX + 0xF0, 8)))[0]
    ch = changed(b, snap())
    if not ok or got != exp or any(o not in (0x10F0, 0x10F4) for o in ch):
        viol.append([sel, hex(got), hex(exp), rel(ch)])
record("select_slot_00269F90", not viol, n=256, violations=len(viol), detail=viol[:8], note="0/1 select; 2..255 leave the cursor")

# 2. kind dispatch of the four facing entries, kinds 0..7, two headings
viol, n = [], 0
for kind in range(8):
    for h in (1.0, 7.0, -2.5):
        for name in ("set_facing_v0", "set_facing_v1", "apply_wrapped", "facing_tail"):
            world(kind=kind)
            b = snap()
            ok = call(E[name], ACTOR, xmm1=h, r8=0)
            n += 1
            ch = rel(changed(b, snap()))
            w1 = wrap(f32(h))
            if kind == 1:
                stored = {"apply_wrapped": w1, "facing_tail": wrap(wrap(w1))}.get(name, wrap(wrap(w1)))
                if name in ("set_facing_v0", "set_facing_v1"):
                    stored = wrap(wrap(w1))            # 0026B6A0(wrap(w1)) then 0026C090(w1) -> 0026B6A0(wrap(w1)) -> wrap(wrap(w1))
                elif name == "facing_tail":
                    stored = wrap(w1)                  # 0026C090 wraps h -> w1, calls 0026B6A0(w1, 1) which wraps again
                    stored = wrap(stored)
                good = ch == ["ctx+38", "ctx+48"] and fbits(rdf(CTX + 0x38)) == fbits(stored) == fbits(rdf(CTX + 0x48))
            elif kind == 3:
                if name == "apply_wrapped":
                    good = ch == []                    # [actor+0xC0] null: the kind-3 arm writes nothing (002E5E5F)
                else:
                    tgt = w1 if name == "facing_tail" else wrap(w1)
                    good = ch == ["slot0+34"] and fbits(rdf(SLOT0 + 0x34)) == fbits(tgt)
            else:
                good = ch == []
            if not ok or not good:
                viol.append([kind, h, name, ch, ok])
record("facing_kind_dispatch", not viol, n=n, violations=len(viol), detail=viol[:8],
       note="kind 1 -> ctx+0x38 / +0x48; kind 3 -> the cursor record's +0x34; every other kind writes nothing")

# 3. section 4 "wraps again ... idempotent, so harmless": the stored kind-1 heading from 0026B5A0 is wrap^3(h)
hs = sorted({f32(-8.0 + 16.0 * i / 4095) for i in range(4096)} | {PI, NPI, f32(4 - PI), f32(-(4 - PI)), 1.0, -1.0, 0.0, -0.0})
diff_n, exact_viol, examples = 0, [], []
for h in hs:
    world(kind=1)
    call(E["set_facing_v0"], ACTOR, xmm1=h)
    got = rdf(CTX + 0x38)
    w3 = wrap(wrap(wrap(h)))
    if fbits(got) != fbits(w3):
        exact_viol.append([h, got, w3])
    if fbits(got) != fbits(wrap(h)):
        diff_n += 1
        if len(examples) < 8:
            examples.append([repr(h), repr(wrap(h)), repr(got)])
record("rewrap_idempotent", not exact_viol and diff_n == 0, n=len(hs), violations=len(exact_viol), stored_differs_from_single_wrap=diff_n,
       examples=examples, note="%d of %d stored headings differ from a single wrap" % (diff_n, len(hs)))

# 4. kind 3 with a secondary context: the 002E5E10 steering-record write
viol = []
for a0d in (0x00, 0x20):
    for bodyp in (False, True):
        world(kind=3, a0d=a0d, ctx2=True, body=bodyp)
        wrf(CTX + 0xAC, 2.5)
        b = snap()
        ok = call(E["set_facing_v1"], ACTOR, xmm1=1.0)
        ch = rel(changed(b, snap()))
        w1 = wrap(1.0)
        w3 = wrap(wrap(w1))
        exp = {"ctx+A8": w3, "ctx+58": w3, "slot0+34": wrap(w1)}
        if not (a0d & 0x20):
            exp.update({"ctx+68": w3, "ctx+78": w3})
        if bodyp:
            exp["body+F8"] = w3
        body_003DAF20 = {"body+40", "body+48", "body+4C"} if bodyp else set()      # 003DAF20(body, ctx +0x104..+0x106)
        vals_ok = all(fbits(rdf({"ctx": CTX, "slot0": SLOT0, "body": BODY}[k.split("+")[0]] + int(k.split("+")[1], 16))) == fbits(v)
                      for k, v in exp.items())
        extra = [c for c in ch if c not in exp and c != "ctx+AC" and c not in body_003DAF20]
        if not ok or not vals_ok or extra or state["boundary"]:
            viol.append([a0d, bodyp, ch, ok])
record("kind3_steering_record_write", not viol, n=4, violations=len(viol), detail=viol,
       note="+0xA8 and the +0x50/+0x60/+0x70 sub-records get wrap^3; actor+0x0D bit 5 skips +0x60/+0x70; a body adds +0xF8 and 003DAF20's +0x40/+0x48/+0x4C; dword [ctx2] = -1 skips 003EC260")

# 5. ED-2: the 003EC260 commit block reached through kind 3 with a live id
REC = RR + 2 * 0x740


def ed2(variant, rr284=0x200, word6=0xFFFF, rr290=0, old=(9.0, 8.0, 7.0), rr288=0xFFFFFFFF, same=False):
    world(kind=3, ctx2=True, ctx2_id=2)
    wrf(CTX + 0xAC, 2.5)
    w3 = wrap(wrap(wrap(1.0)))
    uc.mem_write(REC + 6, struct.pack("<H", word6))
    uc.mem_write(REC + 0x284, struct.pack("<I", rr284))
    uc.mem_write(REC + 0x288, struct.pack("<I", rr288))
    uc.mem_write(REC + 0x290, struct.pack("<I", rr290))
    uc.mem_write(REC + 0x120, struct.pack("<fff", *((2.5, w3, 0.0) if same else old)))
    uc.mem_write(REC + 0x250, struct.pack("<fff", 1.0, 1.0, 1.0))
    b = snap()
    ok = call(E["set_facing_v1" if variant else "set_facing_v0"], ACTOR, xmm1=1.0)
    rr = [c for c in rel(changed(b, snap())) if c.startswith("rr")]
    t120 = struct.unpack("<fff", bytes(uc.mem_read(REC + 0x120, 12)))
    t250 = struct.unpack("<fff", bytes(uc.mem_read(REC + 0x250, 12)))
    return {"ok": ok, "rr_changed": rr, "t120": list(t120), "t250": list(t250), "f12C": rdf(REC + 0x12C),
            "f284": struct.unpack("<I", bytes(uc.mem_read(REC + 0x284, 4)))[0],
            "boundary": state["boundary"] and [state["boundary"][0], hex(state["boundary"][1]), hex(state["boundary"][2])], "w3": w3}


cases = {}
cases["v0_changed"] = ed2(0)
cases["v1_changed"] = ed2(1)
cases["v1_changed_bit20000_rr288_7"] = ed2(1, rr284=0x20200, rr288=7)
cases["v1_changed_bit20000_rr288_none"] = ed2(1, rr284=0x20200)
cases["v0_same_triple"] = ed2(0, same=True)
cases["v1_same_triple"] = ed2(1, same=True)
cases["v0_word6_set"] = ed2(0, word6=5)
cases["v1_word6_set"] = ed2(1, word6=5)
cases["v1_word6_set_bit8000000"] = ed2(1, word6=5, rr284=0x8000200)
cases["v1_rr284_zero"] = ed2(1, rr284=0)
w3 = cases["v0_changed"]["w3"]
new = [2.5, w3, 0.0]
chk = {
    "v0_changed": lambda c: c["t120"] == new and c["t250"] == [9.0, 8.0, 7.0] and c["f12C"] == 1.0 and c["f284"] == 0 and not c["boundary"],
    "v1_changed": lambda c: c["t120"] == new and c["t250"] == new and c["boundary"] == ["004288B0", hex(REC), "0xffffffff"],
    "v1_changed_bit20000_rr288_7": lambda c: c["t250"] == new and c["boundary"] == ["003B3CA0", "0x7", "0x1e"],
    "v1_changed_bit20000_rr288_none": lambda c: c["t250"] == new and not c["boundary"] and c["ok"],
    "v0_same_triple": lambda c: c["rr_changed"] == [] and not c["boundary"],
    "v1_same_triple": lambda c: c["t250"] == new and c["boundary"] == ["004288B0", hex(REC), "0xffffffff"],
    "v0_word6_set": lambda c: c["t120"] == [0.0, 0.0, 0.0] and c["f12C"] == 1.0 and not c["boundary"],
    "v1_word6_set": lambda c: c["t120"] == [0.0, 0.0, 0.0] and c["t250"] == [1.0, 1.0, 1.0] and not c["boundary"],
    "v1_word6_set_bit8000000": lambda c: c["rr_changed"] == [] and not c["boundary"],
    "v1_rr284_zero": lambda c: c["rr_changed"] == [] and not c["boundary"],
}
viol = [k for k, f in chk.items() if not (cases[k]["ok"] and f(cases[k]))]
record("ED2_commit_block_003EC260", not viol, n=len(cases), violations=len(viol), failing=viol, cases=cases,
       note="flag 0 stages AND shifts the old triple to +0x250 when it changed; flag 1 copies the new triple to +0x250, then "
            "004288B0 (bit 0x20000 clear) and/or 003B3CA0 ([+0x288] != -1); word +6 != -1 resets; +0x284 == 0 is 'no record'")

# 6. set_steering_mode 0026AE90 (section 7 / 10)
viol, n = [], 0
for kind in range(8):
    for mode in (0, 1, 2, 3, 4, 5, -1):
        for en in (0.0, -0.0, 0.5):
            world(kind=kind, a0d=0x1F)
            wrf(SLOT0 + 0x2C, en)
            uc.mem_write(SLOT0 + 0x7C, struct.pack("<I", 0xDEADBEEF))
            b = snap()
            ok = call(E["set_steering_mode"], ACTOR, mode)
            n += 1
            ch = rel(changed(b, snap()))
            if kind != 3:
                good = ch == []
            else:
                want = 1 if (2 <= mode <= 4 and en == 0.0) else mode & 0xFF
                good = rdb(SLOT0 + 0x29) == want
                if want == 0:
                    good &= rdb(ACTOR + 0x0D) == 0x0F and struct.unpack("<I", bytes(uc.mem_read(SLOT0 + 0x7C, 4)))[0] == 0 \
                        and 0x2E55C0 in state["entered"]
                else:
                    good &= rdb(ACTOR + 0x0D) == 0x1F and 0x2E55C0 not in state["entered"] and all(c in ("slot0+28",) for c in ch)
            if not ok or not good:
                viol.append([kind, mode, en, ch, ok])
record("set_steering_mode_0026AE90", not viol, n=n, violations=len(viol), detail=viol[:8],
       note="kind gate; modes 2-4 collapse to 1 when +0x2C == 0.0 (-0.0 too); the mode byte is record +0x29; mode 0 clears actor+0x0D bit 4, runs 002E55C0, zeroes +0x7C")

# 7. set_movement_mode 0026C120 (section 7 table)
viol, n = [], 0
for kind in range(8):
    world(kind=kind)
    b = snap()
    ok = call(E["set_movement_mode"], ACTOR, 2)
    n += 1
    if kind != 3 and (not ok or changed(b, snap())):
        viol.append(["gate", kind])
for tgt, hd in ((1.0, 0.0), (-1.0, 0.0), (3.0, -3.0), (-3.0, 3.0)):
    for mode in (2, 3):
        world()
        wrf(SLOT0 + 0x34, tgt)
        wrf(CTX + 0xA8, hd)
        uc.mem_write(SLOT0 + 0x62, bytes([0x40 if tgt > 0 else 0x00]))
        ok = call(E["set_movement_mode"], ACTOR, mode)
        n += 1
        neg = loop_norm(f32(f32(tgt) - f32(hd))) < 0
        good = (rdb(SLOT0 + 0x28) == mode and struct.unpack("<I", bytes(uc.mem_read(SLOT0 + 0x58, 4)))[0] == 0x3E20D97C
                and struct.unpack("<I", bytes(uc.mem_read(SLOT0 + 0x5C, 4)))[0] == 0x40490FDB and bool(rdb(SLOT0 + 0x62) & 0x40) == neg)
        if not ok or not good:
            viol.append(["turn", tgt, hd, mode])
m4 = {}
for limit in (1, 2):
    for cd in (-1, 0, 1, 2, 3):
        world()
        uc.mem_write(FRAMELIMIT, struct.pack("<i", limit))
        uc.mem_write(SLOT0 + 0x68, struct.pack("<h", cd))
        wrf(SLOT0 + 0x34, 0.75)
        ok = call(E["set_movement_mode"], ACTOR, 4)
        n += 1
        completed = 0x26B620 in state["entered"]
        m4["limit%d_cd%d" % (limit, cd)] = [completed, rdb(SLOT0 + 0x28)]
        want = 0 <= cd <= limit
        if not ok or completed != want or rdb(SLOT0 + 0x28) != (0 if want else 4):
            viol.append(["mode4", limit, cd, completed])
for mode in (1, 5, 255):
    world()
    ok = call(E["set_movement_mode"], ACTOR, mode)
    n += 1
    if not ok or rdb(SLOT0 + 0x28) != mode:
        viol.append(["store", mode])
for gate in (0, 1):
    world()
    uc.mem_write(SLOT0 + 0x65, bytes([gate]))
    ok = call(E["set_movement_mode"], ACTOR, 0)
    n += 1
    ent = state["entered"]
    good = 0x2E6300 in ent and ((0x2EBE50 in ent and 0x2E8EE0 in ent) if gate else (0x2EBE50 not in ent))
    if not ok or not good:
        viol.append(["mode0", gate, sorted("%08X" % x for x in ent)])
record("set_movement_mode_0026C120", not viol, n=n, violations=len(viol), detail=viol[:8], mode4=m4,
       note="mode 4 completes iff 0 <= (int16)countdown <= FrameLimit: the compare is unsigned, a negative countdown never completes")

# 8. push / pop (section 6 / 10)
viol = []
pattern = bytearray((i * 7 + 3) & 0xFF for i in range(0x80))
pattern[0x62] = 0x02                      # resume shape 2 (nothing replayed): the pattern's other bytes are not valid ids
pattern = bytes(pattern)
for kind, a18, sel in ((3, 1, 0), (1, 0, 0), (3, 0, 1)):
    world(kind=kind, a18=a18, sel=sel)
    b = snap()
    ok = call(E["push"], ACTOR)
    if not ok or changed(b, snap()):
        viol.append(["push-refuse", kind, a18, sel])
for kind, a18, sel in ((3, 1, 1), (1, 0, 1), (3, 0, 0)):
    world(kind=kind, a18=a18, sel=sel)
    b = snap()
    ok = call(E["pop"], ACTOR)
    if not ok or changed(b, snap()):
        viol.append(["pop-refuse", kind, a18, sel])
world()
uc.mem_write(SLOT0, pattern)
before0 = bytes(uc.mem_read(SLOT0, 0x80))
ok = call(E["push"], ACTOR)
s1 = bytes(uc.mem_read(SLOT1, 0x80))
push_slot1_diff = [i for i in range(0x80) if s1[i] != before0[i]]
push_ok = ok and rdb(CTX + 0xDC) == 1 and struct.unpack("<Q", bytes(uc.mem_read(CTX + 0xF0, 8)))[0] == SLOT1 \
    and bytes(uc.mem_read(SLOT0, 0x80)) == before0 and {0x2627C0, 0x26AE90, 0x26C120} <= state["entered"]
ok2 = call(E["pop"], ACTOR)
pop_ok = ok2 and rdb(CTX + 0xDC) == 0 and struct.unpack("<Q", bytes(uc.mem_read(CTX + 0xF0, 8)))[0] == SLOT0 \
    and {0x2EC3F0, 0x2E8EE0} <= state["entered"]
after0 = bytes(uc.mem_read(SLOT0, 0x80))
slot0_after_pop_diff = [i for i in range(0x80) if after0[i] != before0[i]]
if not push_ok:
    viol.append(["push", ok])
if not pop_ok:
    viol.append(["pop", ok2])
shapes = {}
for shape in range(8):
    world(sel=1)
    uc.mem_write(SLOT0 + 0x62, bytes([shape]))
    ok = call(E["pop"], ACTOR)
    ent = state["entered"]
    shapes[shape] = [0x2EC2C0 in ent, 0x2EBFA0 in ent]
    want = [shape == 0, shape == 1]
    if not ok or shapes[shape] != want or not ({0x2EC3F0, 0x2E8EE0} <= ent):
        viol.append(["shape", shape, shapes[shape], ok])
world()
b = snap()
ok = call(E["push"], ACTOR)
second = snap()
ok2 = call(E["push"], ACTOR)
if changed(second, snap()):
    viol.append(["second push changed state"])
record("push_pop_002EAB80_002EAAA0", not viol, n=6 + 2 + 8 + 2, violations=len(viol), detail=viol[:8],
       push_clone_differs_from_slot0_at=push_slot1_diff, slot0_changed_by_push_pop_at=slot0_after_pop_diff,
       resume_shapes={str(k): v for k, v in shapes.items()},
       note="refusals write nothing; push clones slot 0 -> 1 and leaves slot 0 intact; pop replays shape 0 / 1 only")

# 9. 003A1C50 endpoints (section 2: closed at both ends)
got = {}
for x in (NPI, PI, f32(3 * math.pi), f32(-3 * math.pi), 0.5):
    call(E["normalise_loop"], xmm0=x)
    got[repr(x)] = struct.unpack("<f", struct.pack("<I", uc.reg_read(UC_X86_REG_XMM0) & 0xFFFFFFFF))[0]
okn = got[repr(NPI)] == NPI and got[repr(PI)] == PI and all(loop_norm(float(k)) == v for k, v in got.items())
record("normalise_loop_003A1C50", okn, n=len(got), violations=0 if okn else 1, values=got, note="-pi and +pi are returned unchanged")

json.dump({"pass": sum(1 for v in results.values() if v["pass_"]), "total": len(results), "ok": allok, "allowed_functions": len(ALLOWED),
           "results": results}, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "result.json"), "w"), indent=1, default=str)
print("%d/%d pass (allowed closure %d functions)" % (sum(1 for v in results.values() if v["pass_"]), len(results), len(ALLOWED)))
