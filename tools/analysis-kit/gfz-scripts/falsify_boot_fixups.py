"""Falsification pass 1 on CONTRACT-boot-fixups (OPUS, 2026-09-29), from the shipping image. Killers first.

  B0  section 2: 0022A0B0's one caller is 0017D4C0; 0022BDF0 tail-jumps to 001EDDC0; the seed thunk 00379CF0 is 5 bytes, one
      jmp to 00863D30; the FrameLimit getter 0017D8F0 is 11 bytes                                         KILLER: any differs
  B1  I1 00863D30 seeds 0x1571 (5489) on first use, behind the 02EB4234 latch; boot reseeds 0x11B9 (4537)  KILLER: another seed
  B2  I2 the seed thunk has exactly two callers - boot (0022A410) and the save-load path (005843D3), which calls an import
      (_time64), multiplies 01FD4A80 by 600 and clears the sign before the seed          KILLER: a third caller or a missing step
  B3  I3 (REFUTES "evaluated once") 02064ACC has two writers: boot divides 2 by the frame limit, and the setter 00229F10 is
      called by 002695A0 (from the area transition 002628B0, 2 / limit again) and 0026DB10 (the mainloopallsyncv verb, arg / limit)
  B4  I4/I5 eleven allocations and nine registrations in 0022A0B0 totalling 257.1 and 255.6 MiB; every registration's size
      plus its fourth argument (0x10 / 0x100 / 0x400) is one of the allocated sizes             KILLER: another count or total
"""
import collections, io, os, re, struct
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_IMM, X86_OP_MEM, X86_REG_RIP

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
EXE = os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe")
FUNCS = os.path.join(ROOT, "Tools", "work", "graph", "functions.tsv")
blob = io.open(EXE, "rb").read()
pe = pefile.PE(EXE, fast_load=True); BASE = pe.OPTIONAL_HEADER.ImageBase
SECS = [(s.Name.rstrip(b"\0").decode(), BASE + s.VirtualAddress, max(s.Misc_VirtualSize, s.SizeOfRawData), s.PointerToRawData, s.SizeOfRawData)
        for s in pe.sections]
md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True
fails = 0


def OFF(va):
    for _n, start, size, raw, rawsz in SECS:
        if start <= va < start + min(size, rawsz):
            return raw + (va - start)
    raise ValueError("VA %08X in no raw section" % va)


def check(tag, ok, text):
    global fails
    fails += not ok
    print("%s  %s  %s" % ("SURVIVES" if ok else "BROKEN  ", tag, text))


sizes, names = {}, {}
for i, line in enumerate(io.open(FUNCS, encoding="utf-8", errors="replace")):
    p = line.rstrip("\n").split("\t")
    if i and len(p) > 2:
        try:
            sizes[int(p[0], 16)] = int(p[2]); names[p[1]] = int(p[0], 16)
        except ValueError:
            pass
S = lambda x: "%s %s" % (x.mnemonic, x.op_str)
rip = lambda x: [x.address + x.size + o.mem.disp for o in x.operands if o.type == X86_OP_MEM and o.mem.base == X86_REG_RIP]
T = lambda x: x.operands[0].imm if x.operands and x.operands[0].type == X86_OP_IMM else None
text = next(x for x in SECS if x[0] == ".text")

refs = collections.defaultdict(list)          # target -> [(function, insn)]
imm_sites = collections.defaultdict(list)     # immediate -> [(function, address)]
calls_to = collections.defaultdict(list)      # target -> [(function, address, mnemonic)]
bodies = {}
WATCH = [(0x02089300, 4), (0x0208E6B0, 4), (0x01FD4A80, 4), (0x02EB4234, 1), (0x01EF93E8, 4), (0x022C256C, 4)]
for fa in sorted(sizes):
    if not (text[1] <= fa < text[1] + text[2]):
        continue
    try:
        code = blob[OFF(fa):OFF(fa) + sizes[fa]]
    except ValueError:
        continue
    ins = list(md.disasm(code, fa))
    bodies[fa] = ins
    for x in ins:
        for t in rip(x):
            refs[t].append((fa, x))
        for o in x.operands:
            if o.type == X86_OP_IMM:
                imm_sites[o.imm & 0xFFFFFFFF].append((fa, x.address))
        if x.mnemonic in ("call", "jmp") and T(x) is not None:
            calls_to[T(x)].append((fa, x.address, x.mnemonic))


def acc(t):
    return [(f, x) for f, x in refs[t]]


def is_write(x):
    return x.operands and x.operands[0].type == X86_OP_MEM and x.mnemonic in ("mov", "inc", "dec", "add", "sub", "or", "and", "xor")


boot = bodies[0x0022A0B0]
def args_before(ins, k, reg, back=6):
    for y in reversed(ins[max(0, k - back):k]):
        if y.mnemonic == "mov" and y.op_str.startswith(reg + ","):
            return T(y) if False else (y.operands[1].imm if y.operands[1].type == X86_OP_IMM else None)
    return None
# B0 section 2: the boot fixer's one caller; the frame-base selector's tail; the 5-byte seed thunk; the 11-byte getter
c0 = [("%08X" % f) for f, _a, _m in calls_to[0x0022A0B0]]
t0 = bodies[0x0022BDF0][-1]
thunk = bodies.get(0x00379CF0, [])
check("B0", c0 == ["0017D4C0"] and t0.mnemonic == "jmp" and T(t0) == 0x001EDDC0 and sizes.get(0x00379CF0) == 5 and len(thunk) == 1
      and T(thunk[0]) == 0x00863D30 and sizes.get(0x0017D8F0) == 11,
      "0022A0B0 <- %s; 0022BDF0 ends %s; 00379CF0 %d B %s; 0017D8F0 %s B" % (c0, S(t0), sizes.get(0x00379CF0), [S(x) for x in thunk], sizes.get(0x0017D8F0)))
# B1 I1: first use seeds 0x1571 (5489) behind the 02EB4234 latch; boot reseeds 0x11B9 (4537)
fu = bodies[0x00863D30]
s1 = [S(x) for x in fu if "0x1571" in x.op_str]
latch = any(0x02EB4234 in rip(x) for x in fu)
k1 = [k for k, x in enumerate(boot) if x.mnemonic in ("call", "jmp") and T(x) == 0x00379CF0]
check("B1", bool(s1) and latch and len(k1) == 1 and args_before(boot, k1[0], "ecx") == 0x11B9,
      "first use %s behind the latch %s; boot reseed ecx=%s" % (s1, latch, hex(args_before(boot, k1[0], "ecx") or 0)))
# B2 I2: exactly two callers of the seed thunk - boot and 005843D3; the save-load path calls _time64, multiplies 01FD4A80 by 600, clears the sign
c2 = sorted(("%08X" % f, "%08X" % a) for f, a, _m in calls_to[0x00379CF0])
sl = bodies[0x00584210]
k2 = [k for k, x in enumerate(sl) if x.address == 0x005843D3]
win = sl[max(0, k2[0] - 25):k2[0] + 1] if k2 else []
imp = [S(x) for x in win if x.mnemonic == "call" and x.op_str.startswith("qword ptr [rip")]
mul = [S(x) for x in win if x.mnemonic == "imul" and "0x258" in x.op_str]
sign = [S(x) for x in win if (x.mnemonic == "and" and "0x7fffffff" in x.op_str) or x.mnemonic == "btr"]
check("B2", c2 == [("0022A0B0", "0022A410"), ("00584210", "005843D3")] and imp and mul and sign,
      "seed callers %s; before 005843D3: import %s, %s, sign %s" % (c2, imp, mul, sign))
# B3 I3 (REFUTES "evaluated once"): 02064ACC has two writers - boot (0022A1A7, 2 / [01DFE0B4]) and the 7-byte setter 00229F10.
# The setter's callers re-evaluate it: 002695A0 (reached from the area transition 002628B0) stores 2 / [01DFE0B4] again, and
# 0026DB10 (the mainloopallsyncv verb's native, from 003464B0) stores arg / [01DFE0B4], or 2 / [01DFE0B4] for a negative arg.
w3 = sorted(("%08X" % f, "%08X" % x.address) for f, x in acc(0x02064ACC) if is_write(x))
setter = [S(x).strip() for x in bodies.get(0x00229F10, [])]
sc = sorted(("%08X" % f) for f, _a, _m in calls_to[0x00229F10])
def divides_limit(fa):
    return any(x.mnemonic == "div" and 0x01DFE0B4 in rip(x) for x in bodies.get(fa, []))
verb = [S(x).strip() for x in bodies.get(0x0026DB10, [])]
check("B3", w3 == [("00229F10", "00229F10"), ("0022A0B0", "0022A1A7")] and setter[:2] == ["mov dword ptr [rip + 0x1e3abb6], ecx", "ret"]
      and sc == ["002695A0", "0026DB10"] and divides_limit(0x0022A0B0) and divides_limit(0x002695A0) and divides_limit(0x0026DB10)
      and "js 0x26db1b" in verb and [f for f, _a, _m in calls_to[0x002695A0]] == [0x002628B0] and [f for f, _a, _m in calls_to[0x0026DB10]] == [0x003464B0],
      "writers %s; setter %s; setter callers %s (002695A0 <- 002628B0, 0026DB10 <- 003464B0), each dividing by 01DFE0B4" % (w3, setter[:2], sc))
# B4 I4: eleven allocations, nine registrations, the totals; I5: each registered size + its fourth argument = an allocated size
allocs = [args_before(boot, k, "ecx") for k, x in enumerate(boot) if x.mnemonic == "call" and T(x) == 0x0036D240]
regs = [(args_before(boot, k, "r8d", 10), args_before(boot, k, "r9d", 10)) for k, x in enumerate(boot) if x.mnemonic == "call" and T(x) == 0x00369D30]
reg_total, alloc_total = sum(r for r, _t in regs), sum(allocs)
pairs_ok = all((r + t) in allocs for r, t in regs)
check("B4", len(allocs) == 11 and len(regs) == 9 and round(reg_total / 2**20, 1) == 255.6 and round(alloc_total / 2**20, 1) == 257.1
      and pairs_ok and {t for _r, t in regs} == {0x10, 0x100, 0x400},
      "%d allocations %.1f MiB; %d registrations %.1f MiB; every registration is size + its fourth argument: %s; tails %s"
      % (len(allocs), alloc_total / 2**20, len(regs), reg_total / 2**20, pairs_ok, sorted({hex(t) for _r, t in regs})))
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)   # a BROKEN row must fail the process, not only the text (ASTRA feb631dd4, 2026-09-29)
