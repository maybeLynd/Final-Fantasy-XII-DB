"""Falsification pass 1 on CONTRACT-native-command-lifecycle (OPUS, 2026-09-29), from the shipping image. Killers first.

  L0  section 2: sizes 461 / 89 / 39 / 39 / 41
  L1  N-1: 002621D0 splits the id with `sar ..., 0xc` and `and ..., 0xfff`
  L2  N-2: 003DC2D0 fills sixteen slots at 02B57EF0 with 01F26720 (`rep stosq`) and overwrites index 0, 3, 5 and 7
  L3  section 3: the five tables' first dwords are 1,496 / 147 / 1 / 104 / 212
  L4  N-3: begin reads [rax + rcx + 8], poll [rax + rcx + 0x10], result `inc rax` then [rax + rcx], each after `shl rax, 5`
  L5  N-4: result(count - 1) at tbl + 32 * count is 00342560 in family 0, 00510970 in family 7, NULL in the other three;
      family 3's rows end at 01F29410 and family 5's count is at 01F29418; family 5's rows end at 01F29438 and family 7 starts
      at 01F29440
  L6  N-5: all three accessors `test rcx, rcx / je` then `cmp edx, dword ptr [rcx] / jge`
"""
import io, os, struct
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_REG_RIP

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


sizes = {}
for i, line in enumerate(io.open(FUNCS, encoding="utf-8", errors="replace")):
    p = line.rstrip("\n").split("\t")
    if i and len(p) > 2:
        try:
            sizes[int(p[0], 16)] = int(p[2])
        except ValueError:
            pass
S = lambda x: ("%s %s" % (x.mnemonic, x.op_str)).strip()
rip = lambda x: [x.address + x.size + o.mem.disp for o in x.operands if o.type == X86_OP_MEM and o.mem.base == X86_REG_RIP]
dis = lambda fa: list(md.disasm(blob[OFF(fa):OFF(fa) + sizes[fa]], fa))
u32 = lambda va: struct.unpack("<i", blob[OFF(va):OFF(va) + 4])[0]
q = lambda va: struct.unpack("<Q", blob[OFF(va):OFF(va) + 8])[0]
E = [0x002621D0, 0x003DC2D0, 0x003DC270, 0x003DC240, 0x003DC2A0]
B = {f: dis(f) for f in E}
T = {f: [S(x) for x in b] for f, b in B.items()}

check("L0", [sizes[f] for f in E] == [461, 89, 39, 39, 41], "%s" % [sizes[f] for f in E])
check("L1", any(s.startswith("sar") and s.endswith(", 0xc") for s in T[0x002621D0]) and any(s.startswith("and") and s.endswith(", 0xfff") for s in T[0x002621D0]),
      "sar 0xc / and 0xfff in the executor")
init = B[0x003DC2D0]
refs = sorted({t for x in init for t in rip(x)})
check("L2", any(x.mnemonic.startswith("rep stosq") or S(x).startswith("rep stosq") for x in init)
      and {0x01F26720, 0x02B57EF0} <= set(refs) and {0x01EED700, 0x01F281B0, 0x01F29418, 0x01F29440} <= set(refs),
      "rip refs %s" % ["%08X" % r for r in refs])
TB = {0: 0x01EED700, 3: 0x01F281B0, 5: 0x01F29418, 7: 0x01F29440, "other": 0x01F26720}
cnt = {k: u32(v) for k, v in TB.items()}
check("L3", cnt == {0: 1496, 3: 147, 5: 1, 7: 104, "other": 212}, "%s" % cnt)
check("L4", "shl rax, 5" in T[0x003DC270] and any("+ 8]" in s and "rax + rcx" in s for s in T[0x003DC270])
      and "shl rax, 5" in T[0x003DC240] and any("+ 0x10]" in s and "rax + rcx" in s for s in T[0x003DC240])
      and "inc rax" in T[0x003DC2A0] and T[0x003DC2A0].index("inc rax") < T[0x003DC2A0].index("shl rax, 5") and any("[rax + rcx]" in s for s in T[0x003DC2A0]),
      "begin +8, poll +0x10, result (N + 1) * 32")
past = {k: q(v + 32 * cnt[k]) for k, v in TB.items()}
check("L5", past[0] == 0x00342560 and past[7] == 0x00510970 and past[3] == 0 and past[5] == 0 and past["other"] == 0
      and TB[3] + 32 * cnt[3] == 0x01F29410 and TB[5] + 32 * cnt[5] == 0x01F29438,
      "past-the-end result slots %s; family 3 ends %08X, family 5 ends %08X" % ({k: "%08X" % v for k, v in past.items()}, TB[3] + 32 * cnt[3], TB[5] + 32 * cnt[5]))
ref = lambda t: any(s.startswith("test rcx, rcx") for s in t) and any(s.startswith("cmp edx, dword ptr [rcx]") for s in t) and any(s.startswith("jge") for s in t)
check("L6", all(ref(T[f]) for f in E[2:]), "all three accessors refuse a null table and N >= count")
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)   # a BROKEN row must fail the process, not only the text (ASTRA feb631dd4, 2026-09-29)
