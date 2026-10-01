"""falsify_defeat_rewards.py - falsification pass 1 on 13-Rewards-Progression-Economy/CONTRACT-defeat-rewards-sequence.md
(OPUS, 2026-09-30). Static; reads only the shipping image. Each check is one of the contract's clauses at its bytes.

D1  §2 00312280 is 857 B; its last calls are 00317090 and the stack-cookie check
D2  DR-2 ECX is zeroed at 003124BC and 003124C6 for 002F8BB0 and 002F90C0; a flag test at 00312505/00312513 precedes 0028FB80
D3  DR-3 the walk (00312432-00312460) reads +0x1C2 and +0x18C; 003124A3 calls 0030C650
D4  DR-4 0031251D-00312532 reads the defeated unit's stats +0x1C2 and +0x88; 0031253B / 00312546 read [unit + 0xE78] + 0x30
    and [unit + 0xE70] + 0x30
D5  DR-5 00312409 / 0031240F test status bit 4 of byte 1 in the two layers; 00312421 lea eax, [r12 + rcx]; 00312425
    lea r12d, [rax + rcx*4]
D6  DR-6 00312556 test edx, edx / 00312558 cmovns; 0031255D calls 00254EE0; 00312562 forms requested - old; 00312566 calls 00469E80
D7  §10 caps 0xF423F / 0x3E7 / 0x5F5E0FF / 0x1869F at 003123ED / 003123FF / 00312438 / 0031247C, and the display clamps
    0xF423F at 003124E6 and 0x3E7 at 003124FB-00312502
D8  §14 00469E80 stores the delta at [rsp + 0x30], skips at 00469EA5 test / 00469EA7 jle, and dispatches 0x26 through 0046AB10
D9  §3 the install 0023A965-0023A9F4 sets +0xE70 from [02EBF148] by definition +0x22 and +0xE78 from [02EBF140] by +0x24
D10 DR-6 the setter 00254EE0 clamps to 99,999,999
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "FFXII TZA", "_index", "candidates", "rc9-log-channels-0930"))
import rc9_channels as R  # noqa: E402
from capstone import x86 as X  # noqa: E402

at, md, ext = R.at, R.md, R.ext
F = 0x00312280
results = []


def check(cid, ok, what):
    results.append((cid, ok))
    print("%-4s %-9s %s" % (cid, "SURVIVES" if ok else "BROKEN", what))


def body(f):
    return list(md.disasm(at(f, ext[f]), f))


def win(f, lo, hi):
    return ["%s %s" % (i.mnemonic, i.op_str) for i in body(f) if lo <= i.address <= hi]


def ins(a):
    i = R.dec(a)
    return "%s %s" % (i.mnemonic, i.op_str)


def rip(i):
    for op in i.operands:
        if op.type == X.X86_OP_MEM and op.mem.base == X.X86_REG_RIP:
            return i.address + i.size + op.mem.disp
    return None


b = body(F)
calls = [i.operands[0].imm for i in b if i.mnemonic == "call" and i.operands[0].type == X.X86_OP_IMM]
check("D1", ext[F] == 857 and calls[-2:] == [0x00317090, 0x00808C40],
      "extent %d B; last two direct calls %s" % (ext[F], ["%08X" % c for c in calls[-2:]]))

d2 = [ins(a) for a in (0x003124BC, 0x003124C6)]
calls2 = [i.operands[0].imm for i in b if i.mnemonic == "call" and 0x003124BC <= i.address <= 0x003124D0]
flag = win(F, 0x00312505, 0x00312513)
pre28 = [i.address for i in b if i.mnemonic == "call" and i.operands[0].type == X.X86_OP_IMM and i.operands[0].imm == 0x0028FB80]
check("D2", all(x == "xor ecx, ecx" for x in d2) and calls2 == [0x002F8BB0, 0x002F90C0] and any(x.startswith(("test", "bt", "cmp")) for x in flag)
      and pre28 and pre28[0] > 0x00312513, "%s; calls %s; flag window %s; 0028FB80 at %s" % (
          d2, ["%08X" % c for c in calls2], flag, ["%08X" % a for a in pre28]))

w3 = win(F, 0x00312432, 0x00312460)
check("D3", any("+ 0x1c2]" in x for x in w3 + win(F, 0x00312400, 0x00312432)) and any("+ 0x18c]" in x for x in w3)
      and ins(0x003124A3) == "call 0x30c650", "walk %s ... ; 003124A3 `%s`" % (w3[:6], ins(0x003124A3)))

w4 = win(F, 0x0031251D, 0x00312546)
check("D4", any("+ 0x1c2]" in x for x in w4) and any("+ 0x88]" in x for x in w4) and any("+ 0xe78]" in x for x in w4)
      and any("+ 0xe70]" in x for x in w4) and sum("+ 0x30]" in x for x in w4) >= 2, "%s" % w4)

t5 = [ins(0x00312409), ins(0x0031240F)]
check("D5", all(x.startswith("test byte ptr [") and x.endswith(", 0x10") for x in t5)
      and ins(0x00312421) == "lea eax, [r12 + rcx]" and ins(0x00312425) == "lea r12d, [rax + rcx*4]",
      "%s; %s; %s" % (t5, ins(0x00312421), ins(0x00312425)))

d6 = [ins(a) for a in (0x00312556, 0x00312558, 0x0031255D, 0x00312562, 0x00312566)]
check("D6", d6[0] == "test edx, edx" and d6[1].startswith("cmovns") and d6[2] == "call 0x254ee0" and d6[3].startswith("sub")
      and d6[4] == "call 0x469e80", "%s" % d6)

caps = {a: ins(a) for a in (0x003123ED, 0x003123FF, 0x00312438, 0x0031247C)}
want = {0x003123ED: "0xf423f", 0x003123FF: "0x3e7", 0x00312438: "0x5f5e0ff", 0x0031247C: "0x1869f"}
# the display clamp of the fresh EXP compares with esi, which 003124B4 loads with 0xF423F
disp = [ins(0x003124B4), ins(0x003124E6), ins(0x003124E8)] + win(F, 0x003124FB, 0x00312502)
esi_kept = not any(i.op_str.startswith(("esi,", "rsi,")) and i.mnemonic not in ("cmp", "test") for i in b if 0x003124B4 < i.address < 0x003124E6)
check("D7", all(want[a] in c for a, c in caps.items()) and disp[0] == "mov esi, 0xf423f" and disp[1] == "cmp edi, esi"
      and disp[2] == "cmovg edi, esi" and esi_kept and any("0x3e7" in x for x in disp[3:]),
      "caps %s; display clamps %s" % (caps, disp))

nb = body(0x00469E80)
store = [i for i in nb if "[rsp + 0x30]" in i.op_str and i.mnemonic == "mov" and i.op_str.startswith("dword ptr [rsp + 0x30]")]
d8 = [ins(0x00469EA5), ins(0x00469EA7)]
# edx = 0x26 is formed as `lea edx, [rax + 0x26]` with rax zeroed at the top of the body
rax0 = any(i.mnemonic == "xor" and i.op_str == "eax, eax" for i in nb)
disp26 = (any(i.mnemonic == "mov" and i.op_str == "edx, 0x26" for i in nb) or (rax0 and any(i.op_str == "edx, [rax + 0x26]" for i in nb))) and any(
    i.mnemonic in ("call", "jmp") and i.operands[0].type == X.X86_OP_IMM and i.operands[0].imm == 0x0046AB10 for i in nb)
check("D8", bool(store) and d8[0].startswith("test") and d8[1].startswith("jle") and disp26,
      "delta stored at [rsp + 0x30]: %s; %s; event 0x26 through 0046AB10: %s" % (bool(store), d8, disp26))

inst = [i for i in body(0x0023A7C0 if 0x0023A7C0 in ext else next(f for f in sorted(ext) if f <= 0x0023A965 < f + ext[f]))
        if 0x0023A965 <= i.address <= 0x0023A9F4]
refs = sorted(set(rip(i) for i in inst if rip(i) in (0x02EBF140, 0x02EBF148)))
d9 = " ; ".join("%s %s" % (i.mnemonic, i.op_str) for i in inst)
check("D9", refs == [0x02EBF140, 0x02EBF148] and "+ 0xe70]" in d9 and "+ 0xe78]" in d9 and "+ 0x22]" in d9 and "+ 0x24]" in d9,
      "install window reads %s; +0xE70/+0xE78 stored and definition +0x22/+0x24 read: %s" % (
          ["%08X" % r for r in refs], all(x in d9 for x in ("+ 0xe70]", "+ 0xe78]", "+ 0x22]", "+ 0x24]"))))

sb = " ; ".join("%s %s" % (i.mnemonic, i.op_str) for i in body(0x00254EE0))
check("D10", "0x5f5e0ff" in sb, "00254EE0 carries the 99,999,999 bound (0x5F5E0FF): %s" % ("0x5f5e0ff" in sb))

broken = [c for c, ok in results if not ok]
print("BROKEN %d: %s" % (len(broken), " ".join(broken) or "none"))
sys.exit(0)
