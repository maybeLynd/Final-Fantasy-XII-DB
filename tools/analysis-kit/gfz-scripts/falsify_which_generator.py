"""Falsification pass 1 on CONTRACT-which-generator-serves-which-roll (OPUS, 2026-09-29), from the shipping image.

Each check states its KILLER first; a claim survives only if the killer is absent. Whole-image sweeps decode every listed
body in .text (functions.tsv extents).

  W0  §3 02089300: five references - three reads, all comparisons; writes at 002368F8 and 00236A44   KILLER: another access
  W1  §3 / I4 0208E6B0: exactly two instructions, both in 002342F0 - read 00234301, write 00234315   KILLER: a third access
  W2  §3 01FD4A80: `inc` at 0022A59F; read once, at 005843B4, by `imul ..., 0x258`                 KILLER: another access
  W3  §3 02EB4234: six references, all byte-wide - `cmp byte, 0` x3 and `mov byte, 1` x3           KILLER: a wider access
  W4  I1 [02EB3870, +0x9C4): touched in exactly four functions, and not by 0018D740 / 0018EE20     KILLER: a fifth, or the pair
  W5  I2 the multiplier 0x41C64E6D appears at 24 instruction sites; calls to 00328370: 23 sites in 15 functions
  W6  I3 every function holding the multiplier references 022C256C                                   KILLER: an inliner that does not
  W7  I4 RNG_SharedGameplayLCG_SetState has exactly one caller                                        KILLER: a second
  W8  I5 01F7F600 is taken by exactly four `lea` sites (0015BD13, 0015BD1F, 0019483B, 001948C9) in 0015BCF0 / 001946E0;
      nothing addresses the interior of the 0x9C0-byte array [01F7F600, +0x9C0); the only cells above it, 01F7FFC0 (walked as a
      pointer at 00194855-00194862) and 01F7FFC8, are 001946E0's; 0018D740 holds
      `lea rdx, [rcx + 0x9bc]` (the old clause "0018EE20 has no displacement >= 0x9A0" is W11's to test)
  W9  §2 the boot seeds the gameplay MT with 4537 (0x11B9) through 00379CF0; its consumers are 66 functions
  W10 §2 the presentation PRNG 01EF93E8 is seeded with the constant 0x458DC800
  W11 (REFUTES I5 / CON-155) the twist 0018EE20 itself resets both cells above the array: [rcx+0x9C8] = 624, [rcx+0x9C0] = rcx
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


# W0
a0 = acc(0x02089300)
reads0 = [x for _f, x in a0 if not is_write(x)]
writes0 = sorted("%08X" % x.address for _f, x in a0 if is_write(x))
check("W0", len(a0) == 5 and len(reads0) == 3 and all(x.mnemonic == "cmp" for x in reads0) and writes0 == ["002368F8", "00236A44"],
      "%d references: reads %s; writes %s" % (len(a0), [S(x) for x in reads0], writes0))
# W1
a1 = acc(0x0208E6B0)
check("W1", sorted(("%08X" % f, "%08X" % x.address, is_write(x)) for f, x in a1) == [("002342F0", "00234301", False), ("002342F0", "00234315", True)],
      "%s" % [("%08X" % f, "%08X" % x.address, S(x)) for f, x in a1])
# W2
a2 = acc(0x01FD4A80)
check("W2", sorted("%08X %s" % (x.address, x.mnemonic) for _f, x in a2) == ["0022A59F inc", "005843B4 imul"]
      and any("0x258" in x.op_str for _f, x in a2 if x.mnemonic == "imul"), "%s" % [("%08X" % x.address, S(x)) for _f, x in a2])
# W3
a3 = acc(0x02EB4234)
kinds3 = collections.Counter((x.mnemonic, "byte ptr" in x.op_str, x.op_str.split(", ")[-1]) for _f, x in a3)
check("W3", len(a3) == 6 and all(x.op_str.startswith("byte ptr") for _f, x in a3)
      and kinds3 == collections.Counter({("cmp", True, "0"): 3, ("mov", True, "1"): 3}), "%s" % dict(kinds3))
# W4
fn4 = sorted({f for t, lst in refs.items() if 0x02EB3870 <= t < 0x02EB3870 + 0x9C4 for f, _x in lst})
check("W4", len(fn4) == 4 and 0x0018D740 not in fn4 and 0x0018EE20 not in fn4, "functions %s" % ["%08X" % f for f in fn4])
# W5
mul = imm_sites[0x41C64E6D]
lcg = calls_to[0x00328370]
check("W5", len(mul) == 24 and len(lcg) == 23 and len({f for f, _a, _m in lcg}) == 15,
      "multiplier at %d sites in %d functions; 00328370 reached from %d sites in %d functions"
      % (len(mul), len({f for f, _a in mul}), len(lcg), len({f for f, _a, _m in lcg})))
# W6
mulf = sorted({f for f, _a in mul})
noshare = ["%08X" % f for f in mulf if not any(0x022C256C in rip(x) for x in bodies[f])]
check("W6", not noshare, "inliners without 022C256C: %s (of %d)" % (noshare or "none", len(mulf)))
# W7
setter = names.get("RNG_SharedGameplayLCG_SetState")
c7 = calls_to.get(setter, []) if setter else []
check("W7", setter is not None and len(c7) == 1, "SetState %s; callers %s" % ("%08X" % setter if setter else "?", [("%08X" % f, "%08X" % a) for f, a, _m in c7]))
# W8
base8 = acc(0x01F7F600)
lea8 = sorted(("%08X" % f, "%08X" % x.address) for f, x in base8 if x.mnemonic == "lea")
interior = [("%08X" % f, "%08X" % x.address) for t, lst in refs.items() if 0x01F7F600 < t < 0x01F7F600 + 0x9C0 for f, x in lst]
# the page bounded its census at +0x9C4, the TYPE extent; the 624-dword ARRAY ends at +0x9C0, and +0x9C0 (01F7FFC0) is the
# consumer's walk pointer, +0x9C8 (01F7FFC8) its refill count - both expected, both in 001946E0 only
cells = sorted({("%08X" % t, "%08X" % f) for t, lst in refs.items() if 0x01F7F600 + 0x9C0 <= t < 0x01F7F600 + 0x9D0 for f, _x in lst})
walk = [S(x) for x in bodies.get(0x001946E0, []) if 0x00194855 <= x.address <= 0x00194862]
disp_hi = [S(x) for x in bodies.get(0x0018EE20, []) for o in x.operands if o.type == X86_OP_MEM and o.mem.base != X86_REG_RIP and o.mem.disp >= 0x9A0]
sentinel = any(S(x) == "lea rdx, [rcx + 0x9bc]" for x in bodies.get(0x0018D740, []))
check("W8", lea8 == [("0015BCF0", "0015BD13"), ("0015BCF0", "0015BD1F"), ("001946E0", "0019483B"), ("001946E0", "001948C9")]
      and len(base8) == 4 and not interior and cells == [("01F7FFC0", "001946E0"), ("01F7FFC8", "001946E0")] and len(walk) == 4 and sentinel,
      "lea sites %s; refs inside the 0x9C0-byte array %s; cells above it %s; walk %s; 0018EE20 disp>=0x9A0 %s; sentinel %s" % (lea8, interior or "none", cells, walk, disp_hi or "none", sentinel))
# W9
boot = bodies.get(0x0022A0B0, [])
seed9 = [boot[k - 1] for k, x in enumerate(boot) if x.mnemonic in ("call", "jmp") and T(x) == 0x00379CF0 and k]
consumers = sorted({f for f, _a, _m in calls_to[0x00379CD0]} | {f for f, _a, _m in calls_to[0x00863BF0] if f != 0x00379CD0})
check("W9", any("0x11b9" in S(x) for x in seed9) and len(consumers) == 66,
      "boot seed %s; gameplay MT consumer functions %d" % ([S(x) for x in seed9], len(consumers)))
# W10
st10 = [(("%08X" % f), S(x)) for f, x in acc(0x01EF93E8) if is_write(x) and "0x458dc800" in x.op_str]
check("W10", len(st10) >= 1, "seed stores %s" % st10)
# W11 - the claim the page and CON-155 made, and this pass REFUTES: "neither generator routine touches either cell; 0018EE20 has no
# operand at or above +0x9A0". The twist's last two stores reset both cells through r10 (= rcx, the state base), register-
# relative, which is why a rip-relative census could not see them.
tw = bodies.get(0x0018EE20, [])
tail = [S(x).strip() for x in tw[-3:]]
head = [S(x) for x in tw[:1]]
check("W11", head == ["mov r10, rcx"] and tail == ["mov dword ptr [r10 + 0x9c8], 0x270", "mov qword ptr [r10 + 0x9c0], r10", "ret"],
      "0018EE20 opens %s and ends %s: the twist resets the count to 624 and the cursor to the state base" % (head, tail))
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)   # a BROKEN row must fail the process, not only the text (ASTRA feb631dd4, 2026-09-29)
