"""variable_binding.py - SN-1: a sampled bytecode variable operand names the T0 entry its source statement uses (FABLE, Claude
Opus 5.5, 2026-09-28, on ASTRA-REQ-FABLE-SN1-VARIABLE-BINDING). DATA from the archive; T0 read as OPUS decodes it in
../sn1-layouts/sn1_front_tables.py ({u32 count; u32 nameOffset[count]} at header +0x04, names in the pool at header +0x08).

  V1 five sampled operands, each the 16-bit operand of the 3-byte instruction after a push, index T0 to the variable the source
     statement names: evctrl scope 1 pc 19 (the POPV of pc 16's assignment) -> T0[0x61] = test_load_flg; btlctrl scope 1 pc 534 and
     pc 540 -> T0[0x0D] = loop_flg and T0[0x0E] = mapjump_menu_flg; mapctrl scope 1 pc 732 and pc 739 -> T0[0x52] = test and
     T0[0x20] = mp_debugmenu_flg - the names in 'test_load_flg = 0', 'loop_flg = 0;', 'mapjump_menu_flg = 1;', 'dvar(2, test);',
     'dvar(3, mp_debugmenu_flg);'
  V2 so evctrl pc 16's assignment - which carries the same q0 line (417) as the askpos call at pc 22 (logical_lines2.py L4) - writes
     test_load_flg, the variable of the statement just before the call: the q0 line groups the assignment with the next statement
  C  controls: each operand + 1 names a different variable in all five, and so does each operand read against the neighbouring
     module's T0, so V1 depends on the stored operand and on the module's own table
  Not claimed: a universal operand-to-T0 rule, name scoping, or the native descriptor fields ASTRA reads through 00262440
"""
import os, struct, sys
DIR = sys.argv[1] if len(sys.argv) > 1 else r"D:/FFXII_TZA_extract/ps2data/image/ff12/in/bin"
fails = 0
def ok(tag, cond, msg):
    global fails
    print(("PASS " if cond else "FAIL ") + tag + "  " + msg); fails += (not cond)
def t0(m):
    b = open(os.path.join(DIR, m + ".dbg"), "rb").read()
    h = struct.unpack_from("<16I", b, 0); pool, T0 = h[2], h[1]
    c = struct.unpack_from("<I", b, T0)[0]
    return [b[pool + x:b.index(bytes([0]), pool + x)].decode("latin-1") for x in struct.unpack_from("<%dI" % c, b, T0 + 4)]
def q0(m, sc):
    b = open(os.path.join(DIR, m + ".dbg"), "rb").read()
    o0 = struct.unpack_from("<I", b, 0)[0]; ns = struct.unpack_from("<I", b, o0)[0]
    offs = struct.unpack_from("<%dI" % (4 * ns + 1), b, o0 + 4)
    a, z = offs[4 * sc], offs[4 * sc + 1]
    return [struct.unpack_from("<HBB", b, a + 4 * k) for k in range((z - a) // 4)]
def code(m, sc):
    e = open(os.path.join(DIR, m + ".ebp"), "rb").read()
    ins0 = sum(r[2] for r in q0(m, 0))
    for o in range(0, len(e) - 0x40, 4):
        if struct.unpack_from("<I", e, o + 0xC)[0] == ins0 and struct.unpack_from("<I", e, o + 0x24)[0] == 0:
            for bs in range(0, o, 4):
                if struct.unpack_from("<I", e, bs + 0x18)[0] + 4 + bs == o:
                    return e[bs + struct.unpack_from("<I", e, o + 0x30 * sc + 8)[0]:]
SAMPLES = [("evctrl", 1, 16, "test_load_flg"), ("btlctrl", 1, 531, "loop_flg"), ("btlctrl", 1, 537, "mapjump_menu_flg"),
           ("mapctrl", 1, 729, "test"), ("mapctrl", 1, 736, "mp_debugmenu_flg")]
rows = []
for m, sc, pc, want in SAMPLES:
    c = code(m, sc); T = t0(m)
    push_ok = c[pc] == 0x4F                                     # the push that starts the statement
    op_pc = pc + 3; opcode = c[op_pc]; operand = struct.unpack_from("<H", c, op_pc + 1)[0]
    rows.append((m, pc, op_pc, "%02X" % opcode, operand, T[operand] if operand < len(T) else None, want, push_ok,
                 T[operand + 1] if operand + 1 < len(T) else None))
ok("V1", all(r[7] and r[5] == r[6] for r in rows),
   "; ".join("%s pc %d: op %s %#x -> %s" % (r[0], r[2], r[3], r[4], r[5]) for r in rows))
Q = q0("evctrl", 1)
ok("V2", Q[16][0] == Q[22][0] == 417 and rows[0][5] == "test_load_flg",
   "evctrl pc 16's assignment (line %d, the same as pc 22's call) writes %s" % (Q[16][0], rows[0][5]))
other = {"evctrl": "btlctrl", "btlctrl": "mapctrl", "mapctrl": "evctrl"}
neigh = [(r[0], r[4], (t0(other[r[0]])[r[4]] if r[4] < len(t0(other[r[0]])) else None)) for r in rows]
ok("C", all(r[8] != r[6] for r in rows) and all(n[2] != r[6] for n, r in zip(neigh, rows)),
   "operand + 1 names %s; the neighbouring module's T0 names %s" % ([r[8] for r in rows], [n[2] for n in neigh]))
print("FAILS", fails); sys.exit(1 if fails else 0)
