"""S-37 I-5, I-9, I-10, I-11, I-13 (OPUS, 2026-09-26): executed over block 313's harness (check.py, imported: its six cases run
first, unchanged) - the DynGeo variants Final 00214210, Shadow 00214540 and ShadowFinal 002143E0, the slot-11 thunks 00214890 /
002148B0 / 00214860, the deleting destructors 00213AD0 / 00213AA0 / 00213B00, and the interpreter 002AC5F0 with two painters.

Evidence class: NATIVE-REPLAY (unicorn), live_game false. No application stub; ALLOWED = block 313's closures plus the static
closures of the entries above. Harness changes, disclosed:
 - check.on_code is replaced by the same hook with two additions: (a) ONE more named import bridge, `free` (reached by the
   destructors through 00809950 -> 00210EB0 -> 0019C590), which records its argument and returns - any other unbridged import
   still fails by name; (b) three more recording callbacks on the planted render target's vtable (the fixture block 313 already
   declares): slot 6 (+0x30, records rcx/rdx and the 64 bytes at rdx), slot 15 (+0x78, records dl/r8d/r9d and the three stack
   arguments) and slot 35 (+0x118, records rcx/rdx/r8/r9). Entry into the base draw 002142A0 is logged in order with them.
 - Planted data only: the display object behind [01F82D18] (+0x00 mode, +0x10 width, +0x14 height) that the prefix predicate
   00182F50 and the float source 00229DE0 -> 00183280 read, and a second painter for I-5.
Cases:
 I9   Final and Shadow run their prefix and then enter the base 002142A0, whose draws equal a direct base call on the same ten
      layers; ShadowFinal never enters the base and draws only layer 0 (one bind, one map of the whole count, one copy, draw).
 I10  the Final prefix hands slot 6 a 4x4 whose rows are 008C5F80/90/B0/D0, except row 0's first float, which is replaced by
      00229DE0's result = height x 1.7777778 (008C5B38) / width: identity on a 16:9 display, not on 1280x1024; with the
      predicate false (display mode != 1) slot 6 is not called and the base still runs.
 I11  each thunk tail-jumps to target slot 35 with rcx = the target and edx = the incoming r8b; the third argument is 0
      (00214890), (r8b != 0) (002148B0), 2 x (r8b != 0) in r8w (00214860).
 I13  each deleting destructor stamps 00906DE8 and returns the object; with dl & 1 it frees the object with size
      0x160 / 0x170 / 0x168 (edx at 00809950); without it, no free.
 I5   the same four arguments on the same text give a different result when [0209CC40] points at another painter: the painter
      is an input the signature does not carry.
Writes i5_i9_i13_result.json.
"""
import json
import os
import struct

from unicorn.x86_const import UC_X86_REG_RAX, UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_R9, UC_X86_REG_RSP

import check as C

HERE = os.path.dirname(os.path.abspath(__file__))
uc = C.uc
FINAL, SHADOW, SHFINAL = 0x214210, 0x214540, 0x2143E0
TH_A, TH_B, TH_C = 0x214890, 0x2148B0, 0x214860
DTORS = {0x213AD0: 0x160, 0x213AA0: 0x170, 0x213B00: 0x168}
SPECIAL_VT, SIZED_DELETE = 0x906DE8, 0x809950
G_DISPLAY, DISP, P2, OBJ = 0x1F82D18, C.WORLD + 0x7000, C.WORLD + 0x30000, C.WORLD + 0x9000
for e in (FINAL, SHADOW, SHFINAL, TH_A, TH_B, TH_C, *DTORS):
    C.ALLOWED |= C.closure(e)
# the call graph's edges do not include tail jumps: 00229DE0 is `jmp 00183280`, 00186AA0 / 00186A90 are `jmp 00182EB0` /
# `jmp 00182E80`, which tail-jump to 00225680 / 002256A0, and 00210EB0 is `jmp 0019C590` (the free import's thunk); these targets
# are shipped code reached by those jumps, so their closures join ALLOWED (disclosed, not substituted)
TAILS = (0x183280, 0x182EB0, 0x182E80, 0x225680, 0x2256A0, 0x19C590)
for e in TAILS:
    C.ALLOWED |= C.closure(e)
XCB = {C.CB + 0x40: "slot6_matrix", C.CB + 0x50: "slot15_state", C.CB + 0x60: "slot35"}
C.XCB, C.EV, C.FREES, C.SIZES = XCB, [], [], []


def on_code(u, a, n, _):
    if a in BR:
        nm = BR[a]
        if nm == "free":
            FREES.append([u.reg_read(UC_X86_REG_RCX), u.reg_read(UC_X86_REG_RDX) & 0xFFFFFFFF])
            return
        if nm not in BRIDGED:
            state["bad"].append("import " + nm)
            u.emu_stop()
            return
        d, s, c = u.reg_read(UC_X86_REG_RCX), u.reg_read(UC_X86_REG_RDX), u.reg_read(UC_X86_REG_R8)
        u.mem_write(d, bytes(u.mem_read(s, c)) if c else b"")
        state["copies"].append([d, s, c])
        u.reg_write(UC_X86_REG_RAX, d)
        return
    if a in CBS:
        nm = CBS[a]
        rec = {"cb": nm, "rdx": u.reg_read(UC_X86_REG_RDX), "r8": u.reg_read(UC_X86_REG_R8), "r9": u.reg_read(UC_X86_REG_R9) & 0xFFFFFFFF}
        state["cb"].append(rec)
        EV.append([nm, rec["rdx"] & 0xFFFFFFFF, rec["r8"] & 0xFFFFFFFF, rec["r9"]])
        if nm == "slot0_map":
            u.reg_write(UC_X86_REG_RAX, VBUF)
        elif nm == "slot1_unmap":
            u.reg_write(UC_X86_REG_RAX, 0x1234)
        return
    if a in XCB:
        nm, sp = XCB[a], u.reg_read(UC_X86_REG_RSP)
        rec = [nm, u.reg_read(UC_X86_REG_RCX), u.reg_read(UC_X86_REG_RDX), u.reg_read(UC_X86_REG_R8), u.reg_read(UC_X86_REG_R9)]
        if nm == "slot6_matrix":
            rec.append(list(struct.unpack("<16f", bytes(u.mem_read(rec[2], 64)))))
        elif nm == "slot15_state":
            rec.append(list(struct.unpack("<III", bytes(u.mem_read(sp + 0x28, 4))
                                          + bytes(u.mem_read(sp + 0x30, 4)) + bytes(u.mem_read(sp + 0x38, 4)))))
        EV.append(rec)
        return
    if a == SIZED_DELETE_:
        SIZES.append(u.reg_read(UC_X86_REG_RDX) & 0xFFFFFFFF)
    if a == DYN_DRAW:
        EV.append(["base 002142A0"])
    if a in FSTARTS:
        state["entered"].add(a)
        if a not in ALLOWED:
            state["bad"].append("%08X" % a)
            u.emu_stop()


C.SIZED_DELETE_ = SIZED_DELETE
C.on_code.__code__ = on_code.__code__
uc.ctl_flush_tb()


def f32(x):
    return struct.unpack("<f", struct.pack("<f", x))[0]


def q(a):
    return struct.unpack("<Q", bytes(uc.mem_read(a, 8)))[0]


def plant(mode=1, width=1920, height=1080, layers=None):
    """block 313's case-F world, the extended target vtable and the display object"""
    C.world()
    uc.mem_write(C.TARGET, struct.pack("<Q", C.TVT))
    for k, v in {0: 0x00, 1: 0x10, 4: 0x20, 8: 0x30, 6: 0x40, 15: 0x50, 35: 0x60}.items():
        uc.mem_write(C.TVT + 8 * k, struct.pack("<Q", C.CB + v))
    layers = {0: (1000, True), 1: (0, True), 2: (300, False), 3: (480, True), 9: (481, True)} if layers is None else layers
    vert = C.WORLD + 0x20000
    for i, (cnt, src) in layers.items():
        uc.mem_write(C.DYN + 0x08 + 8 * i, struct.pack("<Q", 0x5000 + i if src else 0))
        uc.mem_write(C.DYN + 0x58 + 8 * i, struct.pack("<Q", vert + 0x1000 * i))
        uc.mem_write(C.DYN + 0xA8 + 4 * i, struct.pack("<I", cnt))
    uc.mem_write(DISP, struct.pack("<I12xII", mode, width, height))
    uc.mem_write(G_DISPLAY, struct.pack("<Q", DISP))


def run(entry, rcx, rdx, r8=0, r9=0):
    del C.EV[:]
    del C.FREES[:]
    del C.SIZES[:]
    ok = C.call(entry, rcx, rdx, r8, r9)
    return {"ok": ok, "stopped_at": (C.state["bad"] or C.state["faults"])[:2], "events": [list(e) for e in C.EV],
            "copies": [[s - (C.WORLD + 0x20000), c] for d, s, c in C.state["copies"]], "rax": uc.reg_read(UC_X86_REG_RAX)}


def draws_of(r):
    return [e for e in r["events"] if e[0] in ("slot0_map", "slot1_unmap", "slot4_draw", "slot8_bind")]


res, cases = {}, {}
# I9 / I10: the base alone, then each variant on the same layers
plant()
base = run(C.DYN_DRAW, C.DYN, C.TARGET)
fin = {}
for nm, (mode, w, h) in {"16x9": (1, 1920, 1080), "5x4": (1, 1280, 1024), "pred_false": (0, 1920, 1080)}.items():
    plant(mode, w, h)
    fin[nm] = run(FINAL, C.DYN, C.TARGET)
plant()
sha = run(SHADOW, C.DYN, C.TARGET)
shf = {}
for nm, (mode, w, h) in {"16x9": (1, 1920, 1080), "pred_false": (0, 1920, 1080)}.items():
    plant(mode, w, h)
    shf[nm] = run(SHFINAL, C.DYN, C.TARGET)
plant(layers={0: (0, False), 1: (5, True)})
shf["layer0_null_source"] = run(SHFINAL, C.DYN, C.TARGET)
res.update(base=base, final=fin, shadow=sha, shadowfinal=shf)


def after_base(r):
    names = [e[0] for e in r["events"]]
    return names.index("base 002142A0") if "base 002142A0" in names else None


ident = [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]
f54 = f32(f32(1024 * f32(16 / 9)) / 1280)
mat = {k: [e[5] for e in v["events"] if e[0] == "slot6_matrix"] for k, v in fin.items()}
cases["I9_final_runs_prefix_then_enters_base_with_identical_draws"] = all(
    fin[k]["ok"] and after_base(fin[k]) is not None and draws_of(fin[k]) == draws_of(base)
    and fin[k]["copies"] == base["copies"] for k in fin) and base["ok"] and fin["16x9"]["events"][0][0] == "slot6_matrix"
st15 = [e for e in sha["events"] if e[0] == "slot15_state"]
cases["I9_shadow_sets_state_then_enters_base_with_identical_draws"] = sha["ok"] and [e[0] for e in sha["events"][:2]] == \
    ["slot15_state", "base 002142A0"] and draws_of(sha) == draws_of(base) and len(st15) == 1 \
    and [st15[0][2] & 0xFF, st15[0][3] & 0xFFFFFFFF, st15[0][4] & 0xFFFFFFFF, st15[0][5]] == [1, 6, 7, [6, 7, 9]]
sf = shf["16x9"]
sf15 = [e for e in sf["events"] if e[0] == "slot15_state"]
cases["I9_shadowfinal_never_enters_base_and_draws_layer0_only"] = all(v["ok"] and after_base(v) is None for v in shf.values()) \
    and [e[0] for e in sf["events"]] == ["slot6_matrix", "slot15_state", "slot8_bind", "slot0_map", "slot1_unmap", "slot4_draw"] \
    and [e[0] for e in shf["pred_false"]["events"]] == ["slot15_state", "slot8_bind", "slot0_map", "slot1_unmap", "slot4_draw"] \
    and draws_of(sf)[0][1] == 0x5000 and draws_of(sf)[1][1] == 1000 and sf["copies"] == [[0, 1000 * 48]] \
    and draws_of(sf)[3][1:3] == [3, 0x1234] and draws_of(sf)[3][3] == 1000 \
    and [sf15[0][2] & 0xFF, sf15[0][3] & 0xFFFFFFFF, sf15[0][4] & 0xFFFFFFFF, sf15[0][5]] == [1, 6, 7, [6, 7, 10]]
cases["I10_final_matrix_rows_from_pool_row0_x_is_aspect"] = mat["16x9"] == [ident] and len(mat["5x4"]) == 1 \
    and mat["5x4"][0][1:] == ident[1:] and mat["5x4"][0][0] == f54 and f54 != 1.0 and mat["pred_false"] == []
res["i10"] = {"matrix_16x9": mat["16x9"], "matrix_1280x1024": mat["5x4"], "expected_row0_x_1280x1024": f54,
              "pred_false_slot6_calls": len(mat["pred_false"])}

# I11: the slot-11 thunks
th = {}
for fn in (TH_A, TH_B, TH_C):
    for b in (0, 1, 0x80, 0xFF):
        plant()
        r = run(fn, C.DYN, C.TARGET, 0xABCD0000 | b, 0x7777)
        e = [x for x in r["events"] if x[0] == "slot35"]
        th["%08X_%02X" % (fn, b)] = {"ok": r["ok"], "rcx": "%X" % e[0][1] if e else None, "rdx": e[0][2] if e else None,
                                     "r8": "%X" % e[0][3] if e else None, "r9": "%X" % e[0][4] if e else None, "calls": len(e)}
res["i11"] = th


def third(fn, b, r8):
    v = int(r8, 16)
    return v if fn in (TH_A, TH_B) else v & 0xFFFF


i11 = True
for fn, want in ((TH_A, lambda b: 0), (TH_B, lambda b: int(b != 0)), (TH_C, lambda b: 2 * int(b != 0))):
    for b in (0, 1, 0x80, 0xFF):
        t = th["%08X_%02X" % (fn, b)]
        i11 &= t["ok"] and t["calls"] == 1 and t["rcx"] == "%X" % C.TARGET and t["rdx"] == b and third(fn, b, t["r8"]) == want(b)
cases["I11_thunks_shift_into_slot35_differ_only_in_third"] = i11

# I13: the deleting destructors
dt = {}
for fn, size in DTORS.items():
    for dl in (0, 1):
        plant()
        uc.mem_write(OBJ, struct.pack("<Q", 0x1111111111111111))
        r = run(fn, OBJ, dl)
        dt["%08X_dl%d" % (fn, dl)] = {"ok": r["ok"], "stopped_at": r["stopped_at"], "vtable": "%X" % q(OBJ), "rax": "%X" % r["rax"],
                                      "sized_delete_edx": ["%X" % s for s in C.SIZES], "free": [["%X" % p, "%X" % s] for p, s in C.FREES]}
res["i13"] = dt
cases["I13_destructors_stamp_one_vtable_and_differ_by_free_size"] = all(
    dt["%08X_dl%d" % (fn, dl)]["ok"] and dt["%08X_dl%d" % (fn, dl)]["vtable"] == "%X" % SPECIAL_VT
    and dt["%08X_dl%d" % (fn, dl)]["rax"] == "%X" % OBJ
    and (dt["%08X_dl%d" % (fn, dl)]["sized_delete_edx"] == ["%X" % size] and [f[0] for f in dt["%08X_dl%d" % (fn, dl)]["free"]] == ["%X" % OBJ]
         if dl else dt["%08X_dl%d" % (fn, dl)]["sized_delete_edx"] == [] and dt["%08X_dl%d" % (fn, dl)]["free"] == [])
    for fn, size in DTORS.items() for dl in (0, 1))

# I5: the painter through [0209CC40]. An ordinary byte and a stop both return 0 with the cursor unmoved (case A / case B), so the
# observable is the end-of-run exit 002AE31C: it calls the one-store setter 0017FAE0, which writes the sink's +0x28 (I-6).
SINK_F = C.SINK + 0x28


def interp_obs(text):
    uc.mem_write(SINK_F, struct.pack("<Q", 0x5A5A5A5A5A5A5A5A))
    ok, eax, adv, o2, _ = C.interp(text)
    return [ok, eax, adv, o2, 0x17FAE0 in C.state["entered"], q(SINK_F) != 0x5A5A5A5A5A5A5A5A]


C.world()
uc.mem_write(C.PAINTER + 0x10C8, struct.pack("<Q", C.WORLD + 0x3F00))
uc.mem_write(C.WORLD + 0x3F00, b"AB")
p1 = interp_obs(b"ABC")
uc.mem_write(C.G_PAINTER, struct.pack("<Q", P2))           # same text, same four arguments, another painter
p2 = interp_obs(b"ABC")
uc.mem_write(P2 + 0x10C8, struct.pack("<Q", C.WORLD + 0x3F80))
uc.mem_write(C.WORLD + 0x3F80, b"AB")
p2t = interp_obs(b"ABC")
uc.mem_write(C.G_PAINTER, struct.pack("<Q", C.PAINTER))
p1b = interp_obs(b"ABC")
res["i5"] = {"fields": ["ok", "eax", "advance", "out2", "entered_0017FAE0", "sink_28_written"], "painter_A_terminator_AB": p1,
             "painter_B_no_terminator": p2, "painter_B_terminator_AB": p2t, "painter_A_again": p1b}
cases["I5_painter_is_read_through_the_global"] = p1[0] and p1[4] and p1[5] and p2[0] and not p2[4] and not p2[5]     and p2t[0] and p2t[4] and p2t[5] and p1b == p1

out = {"ok": all(cases.values()), "cases": cases, "allowed_functions": len(C.ALLOWED), **res}
json.dump(out, open(os.path.join(HERE, "i5_i9_i13_result.json"), "w"), indent=1, sort_keys=True, default=str)
for k, v in cases.items():
    print("%-64s %s" % (k, "PASS" if v else "FAIL"))
print("ALL PASS" if out["ok"] else "FAILED")
