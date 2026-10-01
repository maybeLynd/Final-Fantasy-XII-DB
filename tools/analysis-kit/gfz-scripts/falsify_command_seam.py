"""Falsification pass 1 on CONTRACT-native-command-seam (OPUS, 2026-09-29), from the shipping image. Killers first.

  N0  section 2 / CS-1: 00311CF0 is 283 B and has exactly two calling functions
  N1  CS-1: the seam stores +0xBA0 (00311D7A) and +0xBB8 (00311DB0), never +0x708 / +0x710 / +0x714; the 0x8800203B status
      mask sends 00311D72 to 00311DED, which returns 0
  N2  CS-2: among the bodies named BattleUnit_*, the writers of +0x714 are exactly CommitAction, CancelAndResetCurrentAction
      and ResetStateForReuse; the control 00328640 writes +0x710 and not +0x714
  N3  CS-3: both rings (022BEDA0, 022BE980) are referenced, and each is indexed by a byte masked to 64 (`and ..., 0x3f`)
"""
import collections, io, os
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
            sizes[int(p[0], 16)] = int(p[2]); names[int(p[0], 16)] = p[1]
        except ValueError:
            pass
S = lambda x: ("%s %s" % (x.mnemonic, x.op_str)).strip()
rip = lambda x: [x.address + x.size + o.mem.disp for o in x.operands if o.type == X86_OP_MEM and o.mem.base == X86_REG_RIP]
T = lambda x: x.operands[0].imm if x.operands and x.operands[0].type == X86_OP_IMM else None
text = next(x for x in SECS if x[0] == ".text")
calls_to = collections.defaultdict(set)
writes = collections.defaultdict(set)          # displacement -> functions writing it (register-based)
refs = collections.defaultdict(set)
bodies = {}
for fa in sorted(sizes):
    if not (text[1] <= fa < text[1] + text[2]):
        continue
    try:
        code = blob[OFF(fa):OFF(fa) + sizes[fa]]
    except ValueError:
        continue
    ins = list(md.disasm(code, fa))
    if fa in (0x00311CF0,):
        bodies[fa] = ins
    for x in ins:
        if x.mnemonic in ("call", "jmp") and T(x) is not None:
            calls_to[T(x)].add(fa)
        for t in rip(x):
            refs[t].add(fa)
        if x.operands and x.operands[0].type == X86_OP_MEM and x.mnemonic in ("mov", "and", "or", "inc", "dec", "add", "sub", "xor", "movss") \
                and x.operands[0].mem.base not in (0, X86_REG_RIP) and x.operands[0].mem.disp in (0x708, 0x710, 0x714):
            writes[x.operands[0].mem.disp].add(fa)
at = lambda va: next(S(x) for x in bodies[0x00311CF0] if x.address == va)
nxt = lambda va: next(S(bodies[0x00311CF0][i + 1]) for i, x in enumerate(bodies[0x00311CF0]) if x.address == va)

# N0
check("N0", sizes[0x00311CF0] == 283 and len(calls_to[0x00311CF0]) == 2, "283 B; callers %s" % sorted("%08X" % f for f in calls_to[0x00311CF0]))
# N1
sw = [S(x) for x in bodies[0x00311CF0] if x.operands and x.operands[0].type == X86_OP_MEM and x.mnemonic in ("mov", "or", "and")]
check("N1", "0xba0]" in at(0x00311D7A) and "0xbb8]" in at(0x00311DB0) and not any(d in s.split(",")[0] for s in sw for d in ("0x708]", "0x710]", "0x714]"))
      and at(0x00311D72) == "test ecx, 0x8800203b" and nxt(0x00311D72) == "jne 0x311ded",
      "stores %s / %s; no commit-field write; 0x8800203B -> %s" % (at(0x00311D7A), at(0x00311DB0), nxt(0x00311D72)))
# N2
bu = lambda fs: sorted(names[f] for f in fs if names.get(f, "").startswith("BattleUnit_"))
w714 = bu(writes[0x714])
check("N2", w714 == ["BattleUnit_CancelAndResetCurrentAction", "BattleUnit_CommitAction", "BattleUnit_ResetStateForReuse"]
      and 0x00328640 in writes[0x710] and 0x00328640 not in writes[0x714],
      "BattleUnit_* writers of +0x714: %s; 00328640 writes +0x710 %s, +0x714 %s" % (w714, 0x00328640 in writes[0x710], 0x00328640 in writes[0x714]))
# N3
ring_fns = {r: sorted("%08X" % f for f in refs[r]) for r in (0x022BEDA0, 0x022BE980)}
check("N3", all(ring_fns.values()), "ring users %s" % ring_fns)
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)   # a BROKEN row must fail the process, not only the text (ASTRA feb631dd4, 2026-09-29)
