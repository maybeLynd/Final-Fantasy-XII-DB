"""unpack_strides.py - UQ-215: the source stride each UNPACK arm of 0022BFF0 actually uses, against the PS2 packed element
size (FABLE, Claude Opus 5.5, 2026-09-26).

The arm table is the branch tree on vn (esi) and vl (r8d) already published on the VIF page. For each arm, the
INNER loop is the span from a backward jcc's target to that jcc. Inside it:
  * every memory READ whose base is the source register (rax or rdx, whichever the arm reads through) is collected;
  * the per-iteration advance of that register's index is measured: `inc r8` times the operand's scale for
    [rax + r8*s], or the `lea/add` displacement for a pointer that walks itself.
Expected PS2 packed size per element: (vn + 1) * (32 >> vl) / 8 bytes, and 2 for V4-5.
  U1 the stride table is printed for all 13 arms.
  U2 V2-32 advances 4 bytes per element, but its packed element is 8 (0022C2D0 / 0022C2DA read [rax+r8*4] and
     [rax+r8*4+4], 0022C2DF `inc r8`): consecutive elements OVERLAP by a dword.
  U3 V4-5 advances 8 bytes per element, but its packed element is 2 (0022C840.. read word [rax+r8*8], 0022C879
     `inc r8`): it takes one halfword in four.
  U4 planted control: S-16 advances 2 = its packed size 2 (0022C17B word [rax+r8*2], `inc r8`), so the instrument
     reports a correct arm as correct.
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_OP_REG

ROOT = Path(__file__).resolve().parents[5]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64); cs.detail = True
F = list(cs.disasm(d[off(0x22BFF0):off(0x22BFF0) + 0x8DC], 0x22BFF0))
fails = 0
def check(nm, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, detail)); fails += (not ok)
# arm entry ranges from the published branch tree (vn, vl, first, end)
ARMS = [("S-32", 0, 0, 0x22C0A3, 0x22C12A), ("S-16", 0, 1, 0x22C134, 0x22C1DA), ("S-8", 0, 2, 0x22C1E4, 0x22C271),
        ("V2-32", 1, 0, 0x22C27A, 0x22C2FF), ("V2-16", 1, 1, 0x22C305, 0x22C38C), ("V2-8", 1, 2, 0x22C396, 0x22C41C),
        ("V3-32", 2, 0, 0x22C425, 0x22C4B6), ("V3-16", 2, 1, 0x22C4BC, 0x22C556), ("V3-8", 2, 2, 0x22C560, 0x22C5F6),
        ("V4-32", 3, 0, 0x22C5FF, 0x22C68D), ("V4-16", 3, 1, 0x22C693, 0x22C734), ("V4-8", 3, 2, 0x22C73A, 0x22C7E3),
        ("V4-5", 3, 3, 0x22C7ED, 0x22C89E)]
def rn(r): return cs.reg_name(r) if r else ""
res = {}
for name, vn, vl, lo, hi in ARMS:
    ins = [x for x in F if lo <= x.address < hi]
    # innermost loop: the backward jcc with the smallest span
    loops = [(int(x.op_str, 16), x.address) for x in ins if x.mnemonic.startswith("j") and x.mnemonic != "jmp"
             and x.op_str.startswith("0x") and int(x.op_str, 16) < x.address and int(x.op_str, 16) >= lo]
    if not loops: res[name] = None; continue
    tgt, jend = min(loops, key=lambda t: t[1] - t[0])
    body = [x for x in ins if tgt <= x.address <= jend]
    reads = []
    for x in body:
        if x.mnemonic in ("mov", "movzx", "movsx", "movss", "movups", "movsxd") and len(x.operands) == 2 \
                and x.operands[1].type == X86_OP_MEM and rn(x.operands[1].mem.base) in ("rax", "rdx", "rcx", "r9", "r10"):
            m = x.operands[1].mem
            reads.append((x.address, rn(m.base), rn(m.index), m.scale, m.disp, x.operands[1].size))
    # the source register is the one read through (not written through)
    step = None
    if reads:
        base, idx, scale = reads[0][1], reads[0][2], reads[0][3]
        if idx:
            k = sum(1 for x in body if x.mnemonic == "inc" and rn(x.operands[0].reg) == idx) + \
                sum(x.operands[1].imm for x in body if x.mnemonic == "add" and x.operands[0].type == X86_OP_REG
                    and rn(x.operands[0].reg) == idx and x.operands[1].type != X86_OP_MEM)
            step = k * scale
        else:
            step = sum(x.operands[1].mem.disp for x in body if x.mnemonic == "lea" and rn(x.operands[0].reg) == base
                       and rn(x.operands[1].mem.base) == base) + \
                   sum(x.operands[1].imm for x in body if x.mnemonic == "add" and x.operands[0].type == X86_OP_REG
                       and rn(x.operands[0].reg) == base and x.operands[1].type != X86_OP_MEM)
    packed = 2 if name == "V4-5" else (vn + 1) * (32 >> vl) // 8
    res[name] = (step, packed, [(hex(a), b, i, s, dd, sz) for a, b, i, s, dd, sz in reads][:4])
# Two arms address through a register the generic matcher does not follow; they are read explicitly.
# S-8 reads byte [r8] with `inc r8`; V4-32 reads [r8 + rdx - 4 .. + 8] with r8 = src - dst and rdx advancing 0x10.
X = {x.address: "%s %s" % (x.mnemonic, x.op_str) for x in F}
if X.get(0x22C21B) == "movzx ecx, byte ptr [r8]" and X.get(0x22C251) == "inc r8":
    res["S-8"] = (1, 1, [("0x22c21b", "r8", "", 1, 0, 1)])
if X.get(0x22C650) == "mov ecx, dword ptr [r8 + rdx - 4]" and X.get(0x22C66E) == "lea rdx, [rdx + 0x10]" \
        and X.get(0x22C647) == "sub r8, r10":
    res["V4-32"] = (16, 16, [("0x22c650", "r8+rdx", "", 1, -4, 4)])
for name, *_ in ARMS:
    r = res[name]
    print("info  %-6s %s" % (name, "no loop found" if r is None else "stride %s / packed %d  %s%s" % (
        r[0], r[1], "" if r[0] == r[1] else "MISMATCH  ", r[2][:2])))
check("U1 every arm has an inner loop and a measured stride", all(res[a[0]] and res[a[0]][0] is not None for a in ARMS),
      str([a[0] for a in ARMS if not (res[a[0]] and res[a[0]][0] is not None)]))
check("U1 exactly two arms mismatch, V2-32 and V4-5",
      sorted(a[0] for a in ARMS if res[a[0]] and res[a[0]][0] != res[a[0]][1]) == ["V2-32", "V4-5"])
check("U2 V2-32: stride 4 against packed 8", res["V2-32"] and res["V2-32"][:2] == (4, 8))
check("U3 V4-5: stride 8 against packed 2", res["V4-5"] and res["V4-5"][:2] == (8, 2))
check("U4 planted control: S-16 stride 2 = packed 2", res["S-16"] and res["S-16"][:2] == (2, 2))
print("FAILS", fails)
sys.exit(1 if fails else 0)
