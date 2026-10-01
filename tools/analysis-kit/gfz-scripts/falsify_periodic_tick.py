"""falsify_periodic_tick.py - falsification pass 1 on 10-Status-Periodic-Terminal/CONTRACT-periodic-tick.md
(OPUS, 2026-09-30). Static; reads only the shipping image. Each check is one of the contract's clauses at its bytes.

T1  §2 the builder 00385DF0 is 83 bytes: five calls in order at the stated sites, the fifth a tail jmp, no branch
T2  §3 the record: mov r8d, 0x148 at 00310F6C, memset at 00310F7A, builder at 00310F8B, sink 003112F0 at 00310FAC
T3  §4 gate 1: cmp qword [unit + 0x698], 0 at 00310DCB; its exit at 00310DD6 goes to the epilogue 003112D1
T4  I-1 the deadline: 00310DEF reads the tick counter, 00310DF4 compares [unit + 0xDD0], 00310DFC clears 0x40000000
T5  §4 postcondition: 00310DE4 stores 00305E70's result to [unit + 0x24], 00310DEC stores 002E8100's to [unit + 0x60]
T6  §2 the entry is 1,338 bytes
T7  I-3 stage 1 memsets 0x140 bytes from +0x08 (003848EF-003848F5)
T8  I-4 stage 3 reads +0x17C at 00385625, writes result + 0x42 + 2*slot at 00385645, and its expiry index has no bound
T9  §9 the one generator draw: 00386D17 cmp edi, 0x19; 00386D27 call 00379CD0; 00386D3A add [rbx + 0x24], eax;
    and no other generator call in the five stages
T10 I-7 the frame base 01DFE0B4 is read by stages 2, 4 and 5
T11 §5 stage 5's counter records 0208D494 / 0208DE94; increment at 00386A27, zero at 00386A2C
T12 §11 stage 4 stores +0x2A = maxMP / -50 (00385DBC-00385DCD) and +0x24 = maxHP / -100 (00385D51-00385D62),
    gated by the field word 022C314C
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "FFXII TZA", "_index", "candidates", "rc9-log-channels-0930"))
import rc9_channels as R  # noqa: E402
from capstone import x86 as X  # noqa: E402

at, md, ext = R.at, R.md, R.ext
results = []
ENTRY, BUILDER = 0x00310DB0, 0x00385DF0
STAGES = [0x003848E0, 0x00386C70, 0x00385570, 0x00385CA0, 0x00386860]
GEN = (0x00379CD0, 0x00863BF0)


def check(cid, ok, what):
    results.append((cid, ok))
    print("%-4s %-9s %s" % (cid, "SURVIVES" if ok else "BROKEN", what))


def body(f):
    return list(md.disasm(at(f, ext[f]), f))


def rip(i):
    for op in i.operands:
        if op.type == X.X86_OP_MEM and op.mem.base == X.X86_REG_RIP:
            return i.address + i.size + op.mem.disp
    return None


def imm0(i):
    return i.operands[0].imm if i.operands and i.operands[0].type == X.X86_OP_IMM else None


def ins(a):
    i = R.dec(a)
    return "%s %s" % (i.mnemonic, i.op_str)


# T1
b = body(BUILDER)
calls = [(i.address, i.mnemonic, imm0(i)) for i in b if i.mnemonic in ("call", "jmp")]
branches = [i for i in b if i.mnemonic.startswith("j") and i.mnemonic != "jmp"]
want = [(0x00385E08, "call", STAGES[0]), (0x00385E13, "call", STAGES[1]), (0x00385E1E, "call", STAGES[2]),
        (0x00385E29, "call", STAGES[3]), (0x00385E3E, "jmp", STAGES[4])]
check("T1", ext[BUILDER] == 83 and calls == want and not branches,
      "00385DF0 extent %d B; calls %s; conditional branches %d" % (
          ext[BUILDER], " ".join("%08X:%s:%08X" % c for c in calls), len(branches)))

# T2
t2 = [ins(0x00310F6C), ins(0x00310F7A), ins(0x00310F8B), ins(0x00310FAC)]
check("T2", t2 == ["mov r8d, 0x148", "call 0x861ec0", "call 0x385df0", "call 0x3112f0"], "; ".join(t2))

# T3
g1 = R.dec(0x00310DCB)
ex = R.dec(0x00310DD6)
check("T3", g1.mnemonic == "cmp" and g1.op_str.endswith("+ 0x698], 0") and ex.mnemonic in ("je", "jz") and imm0(ex) == 0x003112D1,
      "00310DCB `%s %s`; 00310DD6 `%s %s`" % (g1.mnemonic, g1.op_str, ex.mnemonic, ex.op_str))

# T4
e = body(ENTRY)
ex_ = {i.address: k for k, i in enumerate(e)}
seg = ["%08X %s %s" % (i.address, i.mnemonic, i.op_str) for i in e[ex_[0x00310DEF]:ex_[0x00310DFC] + 1]]
tick_call = any("0x32a150" in s for s in seg[:2]) or "call" in seg[0]
cmp_dd0 = any("+ 0xdd0]" in s and (" cmp " in s or "cmp " in s.split(" ", 1)[1]) for s in seg)
clear = e[ex_[0x00310DFC]]
clr = (clear.mnemonic == "and" and ("0xffffffffbfffffff" in clear.op_str or "0xbfffffff" in clear.op_str)) or \
      (clear.mnemonic == "btr" and clear.op_str.endswith(", 0x1e"))
check("T4", tick_call and cmp_dd0 and clr, "%s" % " | ".join(seg))

# T5
w24, w60 = R.dec(0x00310DE4), R.dec(0x00310DEC)
pre = ["%08X %s %s" % (i.address, i.mnemonic, i.op_str) for i in e[:ex_[0x00310DEC] + 1] if i.mnemonic == "call"]
check("T5", w24.op_str.split(",")[0].endswith("+ 0x24]") and w60.op_str.split(",")[0].endswith("+ 0x60]")
      and any("0x305e70" in p for p in pre) and any("0x2e8100" in p for p in pre),
      "00310DE4 `%s %s`; 00310DEC `%s %s`; calls before: %s" % (w24.mnemonic, w24.op_str, w60.mnemonic, w60.op_str, "; ".join(pre)))

# T6
check("T6", ext[ENTRY] == 1338, "00310DB0 extent %d B" % ext[ENTRY])

# T7
s1 = ["%08X %s %s" % (i.address, i.mnemonic, i.op_str) for i in body(STAGES[0]) if 0x003848E0 <= i.address <= 0x003848F5]
check("T7", any("0x140" in x for x in s1) and any("+ 8]" in x or ", 8" in x for x in s1) and any("0x861ec0" in x for x in s1),
      " | ".join(s1))

# T8
r17c, w42 = R.dec(0x00385625), R.dec(0x00385645)
s3 = body(STAGES[2])
s3x = {i.address: k for k, i in enumerate(s3)}
inc = ["%s %s" % (i.mnemonic, i.op_str) for i in s3[s3x[0x0038563C]:s3x[0x00385640] + 1]]
idx_reg = None
for i in s3[s3x[0x0038563C]:s3x[0x00385640] + 1]:
    if i.mnemonic in ("inc", "add") and i.operands and i.operands[0].type == X.X86_OP_REG:
        idx_reg = md.reg_name(i.operands[0].reg)
bounded = [i for i in s3 if i.mnemonic == "cmp" and idx_reg and i.op_str.startswith(idx_reg + ",")
           and i.operands[1].type == X.X86_OP_IMM and i.operands[1].imm in (4, 5, 8)]
check("T8", "0x17c]" in r17c.op_str and "+ 0x42]" in w42.op_str.split(",")[0] and idx_reg is not None and not bounded,
      "00385625 `%s %s`; 00385645 `%s %s`; increment %s (register %s); bound compares on it: %d" % (
          r17c.mnemonic, r17c.op_str, w42.mnemonic, w42.op_str, inc, idx_reg, len(bounded)))

# T9
seq = [ins(a) for a in (0x00386D17, 0x00386D27, 0x00386D3A)]
gen_sites = [(f, i.address) for f in STAGES for i in body(f) if i.mnemonic in ("call", "jmp") and imm0(i) in GEN]
check("T9", seq == ["cmp edi, 0x19", "call 0x379cd0", "add dword ptr [rbx + 0x24], eax"] and gen_sites == [(STAGES[1], 0x00386D27)],
      "%s; generator calls in the five stages: %s" % ("; ".join(seq), " ".join("%08X@%08X" % g for g in gen_sites)))

# T10
fb = {("stage %d" % (k + 1)): any(rip(i) == 0x01DFE0B4 for i in body(f)) for k, f in enumerate(STAGES)}
check("T10", fb["stage 2"] and fb["stage 4"] and fb["stage 5"], "01DFE0B4 read by %s" % fb)

# T11
s5 = body(STAGES[4])
refs = sorted(set(rip(i) for i in s5 if rip(i) in (0x0208D494, 0x0208DE94)))
i27, i2c = R.dec(0x00386A27), R.dec(0x00386A2C)
check("T11", refs == [0x0208D494, 0x0208DE94] and i27.mnemonic in ("inc", "add") and i2c.mnemonic in ("mov", "and"),
      "stage 5 references %s; 00386A27 `%s %s`; 00386A2C `%s %s`" % (
          " ".join("%08X" % r for r in refs), i27.mnemonic, i27.op_str, i2c.mnemonic, i2c.op_str))

# T12: the two drain arms. Each is gated by 0031A900 (`test [022C314C], ecx; setne al`) with a mask in ecx; the
# divisions by -50 / -100 are the compiler's reciprocal multiply: 0xAE147AE1 = -0x51EB851F, the /100 magic at shift 5
# and the /50 magic at shift 4
s4 = body(STAGES[3])
s4x = {i.address: k for k, i in enumerate(s4)}
gate = [ins(a) for a in (0x0031A900, 0x0031A906, 0x0031A90B)]
masks = []
for k, i in enumerate(s4):
    if i.mnemonic == "call" and imm0(i) == 0x0031A900:
        m = None
        for w in reversed(s4[max(0, k - 8):k]):
            if w.op_str.startswith("ecx, "):
                src = w.op_str.split(", ")[1]
                if src.startswith("0x") or src.isdigit():
                    m = int(src, 0)
                else:  # a register copy: that register's last immediate
                    for v in reversed(s4[:s4x[w.address]]):
                        if v.mnemonic == "mov" and v.op_str.startswith(src + ", ") and v.operands[1].type == X.X86_OP_IMM:
                            m = v.operands[1].imm
                            break
                break
        masks.append((i.address, m))
mp = ["%s %s" % (i.mnemonic, i.op_str) for i in s4[s4x[0x00385DBC]:s4x[0x00385DCD] + 1]]
hp = ["%s %s" % (i.mnemonic, i.op_str) for i in s4[s4x[0x00385D51]:s4x[0x00385D62] + 1]]
mp_ok = "mov eax, 0xae147ae1" in mp and "sar edx, 4" in mp and any(x.endswith("+ 0x2a], dx") for x in mp)
hp_ok = "mov eax, 0xae147ae1" in hp and "sar edx, 5" in hp and any(x.endswith("+ 0x24], edx") for x in hp)
order = [a for a, _ in masks]
hp_gate = [m for a, m in masks if a < 0x00385D51]
mp_gate = [m for a, m in masks if 0x00385D62 < a < 0x00385DBC]
check("T12", gate == ["test dword ptr [rip + 0x1fa8846], ecx", "mov eax, 0", "setne al"] and mp_ok and hp_ok
      and hp_gate[-1:] == [1] and mp_gate[-1:] == [2],
      "0031A900 tests [022C314C] with ecx; gate calls (site, mask) %s; HP arm (mask 1 expected) %s: /-100 %s; "
      "MP arm (mask 2 expected) %s: /-50 %s" % (
          " ".join("%08X:%s" % (a, m) for a, m in masks), hp_gate, hp_ok, mp_gate, mp_ok))

broken = [c for c, ok in results if not ok]
print("BROKEN %d: %s" % (len(broken), " ".join(broken) or "none"))
sys.exit(0)
