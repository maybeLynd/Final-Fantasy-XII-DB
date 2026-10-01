"""sd4_bit24.py - every write of battle-unit flag bit 24 (+0 qword, 0x1000000) and what it travels with (OPUS, 2026-09-30;
register SD-4). Scans every catalogued function (Database/Tools/analysis-kit/gfz-scripts/retool.py) for OR / BTS that
set bit 24 and for AND masks that clear it - including wide masks (dword / qword immediates and `movabs reg, imm` then
`and [..], reg`), the shape SWE2-AUDIT-SEM's BIT46 review showed a single-bit search misses. Prints every site with its
mask and the other bits the same instruction changes. Asserts the named transitions (T1-T6) and the reader (R1).
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import retool as T  # noqa: E402

R = T.R
fails = 0
B = 24


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


def ins(a):
    return next(R.md.disasm(R.at(a, 16), a, 1))


sets, clears = [], []
for f, n in T.sizes().items():
    d = R.at(f, n)
    if not d:
        continue
    body = list(R.md.disasm(d, f))
    for k, i in enumerate(body):
        if i.mnemonic not in ("or", "and", "bts", "btr"):
            continue
        m = re.match(r"(dword|qword) ptr \[(r\w+)\], (0x[0-9a-f]+|\d+|r\w+)$", i.op_str)
        if not m:
            continue
        size, _, src = m.groups()
        if i.mnemonic in ("bts", "btr"):
            if src in ("0x18", "24"):
                (sets if i.mnemonic == "bts" else clears).append((f, i.address, i.op_str, "bit"))
            continue
        if src[0] == "r":
            v = None
            for j in body[max(0, k - 4):k][::-1]:
                mm = re.match(r"%s, (0x[0-9a-f]+)$" % src, j.op_str)
                if j.mnemonic in ("movabs", "mov") and mm:
                    v = int(mm.group(1), 16)
                    break
            if v is None:
                continue
        else:
            v = int(src, 0)
            if size == "qword" and v < (1 << 32) and v & 0x80000000:
                v |= 0xFFFFFFFF00000000
        width = 64 if size == "qword" else 32
        if i.mnemonic == "or" and (v >> B) & 1 and bin(v).count("1") <= 12:
            sets.append((f, i.address, i.op_str, [b for b in range(width) if (v >> b) & 1 and b != B]))
        if i.mnemonic == "and" and not (v >> B) & 1 and bin(v & ((1 << width) - 1)).count("1") >= width - 8:
            clears.append((f, i.address, i.op_str, [b for b in range(width) if not (v >> b) & 1 and b != B]))
print("sets of bit 24 (with the other bits the same instruction sets):")
for s in sorted(sets):
    print("  %08X %08X %-34s %s" % s)
print("clears of bit 24 (with the other bits the same mask clears):")
for s in sorted(clears):
    print("  %08X %08X %-34s %s" % s)
S = {(f, a): o for f, a, _, o in sets}
C = {(f, a): o for f, a, _, o in clears}
check("T1", (0x00313400, 0x00313469) in S and 50 in S[(0x00313400, 0x00313469)], "BattleUnit_EnterPartyCombatStance 00313400 sets 24 with 50")
check("T2", (0x00313480, 0x003134EB) in S and 51 in S[(0x00313480, 0x003134EB)], "BattleUnit_ExitPartyCombatStance 00313480 sets 24 with 51")
check("T3", (0x00313500, 0x00313537) in S and ins(0x00313531).op_str == "dword ptr [rbx], 0x2000100",
      "00313500 (from BattleUnit_UpdateCombatNavigationStep 00325BB0) sets 25 and 8, then 24")
check("T4", (0x00307300, 0x00307A97) in S and (0x00301140, 0x003012A1) in S,
      "Battle_ProcessActionTarget 00307300 and the revival 00301140 set 24")
check("T5", (0x003250F0, 0x0032517C) in C and (0x003083A0, 0x003083A6) in C and ins(0x003083A0).op_str == "dword ptr [rcx], 0xfdffffff"
      and ins(0x00325175).op_str == "0x3083a0",
      "the reaction-animation handler 003250F0 clears 24 (0032517C) or 24 with 25 (003083A0 via 00325175)")
check("T6", (0x003105D0, 0x0031066F) in C and {50, 51} <= set(C[(0x003105D0, 0x0031066F)])
      and (0x00307C70, 0x00307CA2) in C and (0x00307C70, 0x00307CD7) in C,
      "BattleUnit_CancelAndResetCurrentAction 003105D0 clears 24 with 50 and 51; 00307C70 clears 24 with 50 or with 51")
r = [ins(a) for a in (0x0023B12B, 0x0023B131, 0x0023B136, 0x0023B14F)]
check("R1", r[0].op_str == "eax, dword ptr [rdi]" and r[1].op_str == "rax, 0x18" and r[2].mnemonic == "jb" and r[3].op_str == "ebx, 2",
      "the capability recompute 0023B040 sets inhibit-mask bit 1 while bit 24 is set (0023B131-0023B14F)")
print("FAILS %d" % fails)
