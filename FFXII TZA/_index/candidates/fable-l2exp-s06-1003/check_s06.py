"""check_s06.py - FABLE, 2026-10-03: S-06 I-4's step-constant table, measured at the bytes.

Defect under test (SWE2-AUDIT-SPEC L2 expansion, item 4 row 1): "the observed steps 0.005556, 0.52 and 1.1 are
missing from I-4's table". This script re-runs the census I-4 describes (every RIP-relative operand of
addss/subss/movss/mulss in the dispatcher body 001D1660, resolved through its section) and then executes the two
arms that produced 0.52 and 1.1 in the replay, under unicorn, to say where each value comes from.

Prints PASS/FAIL lines and FAILS N last. CONTROL lines are sensitivity controls: each evaluates the OLD reading with
the same predicate the corrected claim uses and must come out FALSE; a control that comes out TRUE is a FAIL.
"""
import collections
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "fable-review-astra-ov42-caller-quotient-bound-1002"))
from rvlib import Img  # noqa: E402
from capstone.x86 import X86_OP_MEM, X86_OP_IMM  # noqa: E402

img = Img.load()
cs = img.cs
BODY_S, BODY_E = 0x001D1660, 0x001D4C1C        # dispatcher body; the 282-entry table starts at 001D4C1C (I-1)
TABLE = 0x001D4C1C
MN = ("addss", "subss", "movss", "mulss")
fails = 0


def rec(ok, name, detail=""):
    global fails
    if not ok:
        fails += 1
    print("%s %s%s" % ("PASS" if ok else "FAIL", name, ("  " + detail) if detail else ""))


def control(old_reading_holds, name, detail=""):
    """A sensitivity control: the OLD reading must NOT hold."""
    global fails
    if old_reading_holds:
        fails += 1
    print("%s CONTROL %s%s" % ("FAIL" if old_reading_holds else "PASS", name, ("  " + detail) if detail else ""))


def section(va):
    r = va - img.base
    for name, sva, vs, ra, rs in img.secs:
        if sva <= r < sva + max(vs, rs):
            return name, (sva <= r < sva + rs)
    return "?", False


def f32(va):
    return struct.unpack("<f", img.read(va, 4))[0]


def arm_of(cid):
    return img.base + img.u32(TABLE + (cid - 12) * 4)


# ---- 1. linear decode of the body ------------------------------------------------------------------------------
ins = list(cs.disasm(img.read(BODY_S, BODY_E - BODY_S), BODY_S))
end = ins[-1].address + ins[-1].size
rec(end == BODY_E and ins[-2].mnemonic == "ret" and ins[-1].mnemonic == "nop",
    "body_decodes_contiguously", "%d instructions to %X: %d up to the final ret + one alignment nop" % (len(ins), end, len(ins) - 1))

# ---- 2. the census I-4 describes -------------------------------------------------------------------------------
ops = []   # (insn va, mnemonic, target, section, file_backed, value or None)
for i in ins:
    if i.mnemonic not in MN:
        continue
    for op in i.operands:
        if op.type == X86_OP_MEM and op.mem.base and i.reg_name(op.mem.base) == "rip":
            t = i.address + i.size + op.mem.disp
            sec, fb = section(t)
            ops.append((i.address, i.mnemonic, t, sec, fb, round(f32(t), 6) if fb else None))
by_mn = collections.Counter(o[1] for o in ops)
bss = [o for o in ops if not o[4]]
data_fb = [o for o in ops if o[4] and o[3] == ".data"]
rdata = [o for o in ops if o[4] and o[3] == ".rdata"]
other = [o for o in ops if o[4] and o[3] not in (".data", ".rdata")]
rec(len(ops) == 481 and dict(by_mn) == {"movss": 272, "addss": 149, "subss": 55, "mulss": 5},
    "census_denominator_481", "RIP-relative operands of the four mnemonics: %d %s" % (len(ops), dict(by_mn)))
rec(len(bss) == 249 and len(data_fb) == 6 and len(rdata) == 226 and not other,
    "census_splits_by_section", ".data past raw data (.bss settings cells) %d; file-backed .data %d; .rdata %d; other %d"
    % (len(bss), len(data_fb), len(rdata), len(other)))
rc = collections.Counter(o[5] for o in rdata)
FULL = {0.01: 88, -0.01: 28, 0.02: 19, 0.1: 18, 0.001: 13, 0.05: 12, -0.05: 8, 1.0: 8,
        -0.02: 3, -0.03: 3, -1.0: 3, 0.002: 3, 0.03: 3,
        0.005: 2, -0.005: 2, 0.005556: 2,
        -0.001: 1, -0.1: 1, -0.5: 1, 0.5: 1, 0.0722: 1, 0.2126: 1, 0.7152: 1, 0.99: 1, 1.01: 1, 10.0: 1, 48.0: 1}
rec(dict(rc) == FULL, "rdata_constant_set_is_the_27_values",
    "%d distinct .rdata values over %d references: %s" % (len(rc), sum(rc.values()),
                                                          ", ".join("%g x%d" % kv for kv in sorted(rc.items(), key=lambda kv: (-kv[1], kv[0])))))

# ---- 3. the table as printed in I-4 ----------------------------------------------------------------------------
PRINTED = {0.01: 88, -0.01: 28, 0.02: 19, 0.1: 18, 0.001: 13, 0.05: 12, -0.05: 8, -1.0: 3, -0.03: 3, 0.03: 3}
rec(all(rc.get(k) == v for k, v in PRINTED.items()), "printed_rows_are_each_right",
    "all ten printed (constant, refs) pairs match the .rdata census")
missing = {k: v for k, v in FULL.items() if k not in PRINTED}
control(set(rc) == set(PRINTED), "old_reading_printed_table_is_the_whole_set",
        "the printed table covers %d of %d values and %d of %d references; missing: %s"
        % (len(PRINTED), len(rc), sum(PRINTED.values()), sum(rc.values()),
           ", ".join("%g x%d" % kv for kv in sorted(missing.items(), key=lambda kv: (-kv[1], kv[0])))))
control(all(v > 3 or k in PRINTED for k, v in rc.items() if v >= 3), "old_reading_the_cut_is_a_reference_threshold",
        "-0.02 x3, 0.002 x3 and 1.0 x8 are omitted while -1.0/-0.03/0.03 x3 are printed: the cut is not a count threshold")

# ---- 4. the 1.0 x11 / 0.5 x4 figures: three of each are .data setting cells, not constants -----------------------
d_cells = collections.Counter((o[2], o[5]) for o in data_fb)
rec(d_cells == collections.Counter({(0x01DFE194, 0.5): 3, (0x01DFE1AC, 1.0): 3}), "data_operands_are_two_setting_cells",
    "file-backed .data operands: " + ", ".join("%X=%g x%d" % (a, v, n) for (a, v), n in sorted(d_cells.items())))
rec(rc[1.0] + sum(n for (a, v), n in d_cells.items() if v == 1.0) == 11 and rc[1.0] == 8,
    "one_point_zero_x11_is_8_rdata_plus_3_data", "the contract's 1.0 x11 = %d .rdata + 3 .data (01DFE1AC)" % rc[1.0])
rec(rc[0.5] + sum(n for (a, v), n in d_cells.items() if v == 0.5) == 4,
    "zero_point_five_x4_is_1_rdata_plus_3_data", "falsification pass 1's 0.5 x4 = %d .rdata (01CEBB70) + 3 .data (01DFE194)" % rc[0.5])

# ---- 5. 0.005556 is a literal, and it belongs to the FOV arm (id 104) -------------------------------------------
s5 = [o for o in rdata if o[5] == 0.005556]
rec([(o[0], o[1], o[2]) for o in s5] == [(0x001D2B59, "subss", 0x009002B8), (0x001D2B6E, "addss", 0x009002B8)]
    and arm_of(104) == 0x001D2B4D and 0x001D2B4D < 0x001D2B59 < 0x001D2B6E < 0x001D2B83,
    "step_0_005556_is_rdata_009002B8_in_arm_104", "f32 %r (1/180 = %r); subss 001D2B59, addss 001D2B6E; table[104] = %X"
    % (f32(0x009002B8), 1 / 180.0, arm_of(104)))

# ---- 6. 0.52 and 1.1 are not constants anywhere the body can reach them -----------------------------------------
pat = {0.52: struct.pack("<f", 0.52), 1.1: struct.pack("<f", 1.1)}
body = img.read(BODY_S, BODY_E - BODY_S)
any_rip_value = collections.Counter()
imm_hits = []
for i in ins:
    for op in i.operands:
        if op.type == X86_OP_MEM and op.mem.base and i.reg_name(op.mem.base) == "rip":
            t = i.address + i.size + op.mem.disp
            if section(t)[1]:
                any_rip_value[round(f32(t), 6)] += 1
        if op.type == X86_OP_IMM and (op.imm & 0xFFFFFFFF) in (0x3F051EB8, 0x3F8CCCCD):
            imm_hits.append(i.address)
rec(any_rip_value[0.52] == 0 and any_rip_value[1.1] == 0 and not imm_hits and all(p not in body for p in pat.values()),
    "no_0_52_or_1_1_operand_immediate_or_byte_pattern_in_body",
    "rip operands of ANY mnemonic with value 0.52: %d, 1.1: %d; imm32 hits %d; raw f32 patterns in body: %s"
    % (any_rip_value[0.52], any_rip_value[1.1], len(imm_hits), [hex(BODY_S + body.find(p)) for p in pat.values() if p in body]))

# ---- 7. execute the two arms (unicorn 2.1.4) --------------------------------------------------------------------
from unicorn import Uc, UC_ARCH_X86, UC_MODE_64  # noqa: E402
from unicorn.x86_const import UC_X86_REG_RBX, UC_X86_REG_RSP  # noqa: E402
import unicorn  # noqa: E402

PAGES = (0x001D2000, 0x001D4000, 0x008C5000, 0x00900000, 0x01DFE000)


def run_arm(arm, cell, start_value, bl_seq):
    """Run the arm once per bl in bl_seq on ONE persistent cell; return the cell after each run."""
    u = Uc(UC_ARCH_X86, UC_MODE_64)
    for p in PAGES:
        u.mem_map(p, 0x1000)
        try:
            u.mem_write(p, img.read(p, 0x1000))
        except ValueError:
            pass
    u.mem_map(0x7000000, 0x10000)
    u.reg_write(UC_X86_REG_RSP, 0x700F000)
    if start_value is not None:
        u.mem_write(cell, struct.pack("<f", start_value))
    out = []
    for bl in bl_seq:
        u.reg_write(UC_X86_REG_RBX, bl)
        u.emu_start(arm, 0x001D4BFA, count=64)
        out.append(round(struct.unpack("<f", bytes(u.mem_read(cell, 4)))[0], 6))
    return out


rec(unicorn.__version__ == "2.1.4", "unicorn_pinned", unicorn.__version__)
A111, A169 = arm_of(111), arm_of(169)
rec(A111 == 0x001D2881 and A169 == 0x001D29CC, "arms_from_the_table", "table[111] = %X, table[169] = %X" % (A111, A169))
r111 = run_arm(A111, 0x01DFE194, None, (0, 1))
r169 = run_arm(A169, 0x01DFE1AC, None, (0, 1))
rec(r111 == [0.52, 0.5] and r169 == [1.1, 1.0], "image_start_reproduces_the_replay_values",
    "from the image's own cell values (01DFE194 = %g, 01DFE1AC = %g), bl=0 then bl=1 on one cell: id 111 %s, id 169 %s"
    % (f32(0x01DFE194), f32(0x01DFE1AC), r111, r169))
z111 = run_arm(A111, 0x01DFE194, 0.0, (0,))
z169 = run_arm(A169, 0x01DFE1AC, 0.0, (0,))
rec(z111 == [0.02] and z169 == [0.1], "zero_start_gives_the_steps",
    "with the cell planted 0: id 111 writes %s (step 0.02, .rdata 009002BC), id 169 writes %s (step 0.1, .rdata 008C5F6C)" % (z111, z169))
control(r111[0] in rc or r169[0] in rc, "old_reading_0_52_and_1_1_are_step_constants",
        "0.52 in the .rdata set: %s; 1.1 in the .rdata set: %s" % (r111[0] in rc, r169[0] in rc))

# ---- 8. the runtime-step paragraph's arm counts, recounted from the replay's own result.json (read-only) --------
import json  # noqa: E402
RES = os.path.join(HERE, "..", "s06-opus-replay-console-arms", "result.json")
per_id = json.load(open(RES))["results"]["per_id"]
arm_vals = collections.defaultdict(set)
for row in per_id:
    for k in ("inc", "dec"):
        v = row[k]
        if v.get("ok") and 12 <= row["id"] <= 293 and v.get("float_values"):
            arm_vals[v["arm"]].update(v["float_values"])
signed = collections.Counter()          # the replay's tally: one count per arm per |signed value|
for vals in arm_vals.values():
    for f in vals:
        signed[abs(f)] += 1
PRINTED_RUNTIME = {0.01: 56, 0.1: 7, 0.02: 7, 0.001: 6, 0.05: 5, 1.0: 4, 0.005: 4, 0.03: 3, 0.005556: 2}
rec(all(signed[k] == v for k, v in PRINTED_RUNTIME.items()), "printed_runtime_counts_are_the_replays_signed_tally",
    "the paragraph's nine counts equal the replay's per-signed-value tally")
both = sorted(a for a, vals in arm_vals.items() if any(f < 0 for f in vals) and any(f > 0 for f in vals))
OVERRIDE = {"%08X" % A111: z111[0], "%08X" % A169: z169[0]}   # measured zero-start steps of the two .data-cell arms
arms_per_step = collections.Counter()
for a, vals in arm_vals.items():
    if a in OVERRIDE:
        arms_per_step[OVERRIDE[a]] += 1
    else:
        for m in set(abs(f) for f in vals):
            arms_per_step[m] += 1
CORRECT = {0.01: 55, 0.02: 8, 0.1: 7, 0.001: 6, 0.05: 5, 0.03: 3, 1.0: 2, 0.005: 2, 0.005556: 1}
rec(dict(arms_per_step) == CORRECT and sum(CORRECT.values()) == 89, "arms_per_step_deduplicated",
    "%s = %d arms; arms seen writing both signs: %s" % (
        ", ".join("%g (%d)" % kv for kv in sorted(arms_per_step.items(), key=lambda kv: (-kv[1], kv[0]))),
        sum(arms_per_step.values()), " ".join(both)))
control(all(arms_per_step.get(k) == v for k, v in PRINTED_RUNTIME.items()), "old_reading_printed_counts_are_arm_counts",
        "differs at: %s" % ", ".join("%g printed %d, arms %d" % (k, v, arms_per_step.get(k, 0))
                                    for k, v in PRINTED_RUNTIME.items() if arms_per_step.get(k) != v))

print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
