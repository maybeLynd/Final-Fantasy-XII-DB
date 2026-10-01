"""Falsification pass 1 on CONTRACT-weapon-recipes (OPUS, 2026-09-29), from the shipping image. Killers first.

  W0  section 2: 00385F60 is 2,302 B
  W1  RW-1: the 109 pointers at 01EF96C0 all land in .data, and the next qword is 000000B4FFFFFFFF
  W2  RW-2 / RW-4: recipes decode as two -1-terminated i32 lists; 25 and 26 are the stated lists and differ in exactly three
      slots; 25's preview names 5, 6, 22, 33 and 34, none of which its committed list names; recipes 2 and 6's committed lists
      are the ones the page quotes
  W3  RW-2: `cmp dword ptr [rip -> 02AEDFB8], 1` at 003863D7; the skip mask 0x4000140000004E appears in the body and decodes to
      ids 1, 2, 3, 6, 34, 36, 54
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
q = lambda va: struct.unpack("<Q", blob[OFF(va):OFF(va) + 8])[0]
i32 = lambda va: struct.unpack("<i", blob[OFF(va):OFF(va) + 4])[0]
data = next(x for x in SECS if x[0] == ".data")
TB = 0x01EF96C0

check("W0", sizes[0x00385F60] == 2302, "%d B" % sizes[0x00385F60])
ptrs = [q(TB + 8 * i) for i in range(109)]
check("W1", all(data[1] <= p < data[1] + data[2] for p in ptrs) and q(TB + 8 * 109) == 0x000000B4FFFFFFFF, "109 in .data; next %016X" % q(TB + 8 * 109))


def recipe(n):
    va, lists, cur = ptrs[n], [], []
    while len(lists) < 2:
        v = i32(va); va += 4
        if v == -1:
            lists.append(cur); cur = []
        else:
            cur.append(v)
    return lists
r25, r26, r2, r6 = recipe(25), recipe(26), recipe(2), recipe(6)
diff = sum(1 for a, b in zip(r25[0] + r25[1], r26[0] + r26[1]) if a != b) if [len(x) for x in r25] == [len(x) for x in r26] else None
check("W2", r25 == [[5, 6, 22, 33, 34, 35, 42], [29, 66, 96, 97, 98, 99, 125, 165, 171, 176, 182]]
      and r26 == [[5, 6, 22, 33, 34, 36, 43], [29, 65, 96, 97, 98, 99, 125, 165, 171, 176, 182]] and diff == 3
      and not ({5, 6, 22, 33, 34} & set(r25[1])) and r6[1] == [3, 4, 61, 90, 91, 112, 180] and r2[1] == [20, 30, 32, 40, 181],
      "25 %s; 26 %s; %s slots differ; 2 committed %s; 6 committed %s" % (r25, r26, diff, r2[1], r6[1]))
b = list(md.disasm(blob[OFF(0x00385F60):OFF(0x00385F60) + sizes[0x00385F60]], 0x00385F60))
flag = [x for x in b if x.address == 0x003863D7]
mask = [S(x) for x in b if "0x4000140000004e" in x.op_str]
ids = [i for i in range(64) if (0x4000140000004E >> i) & 1]
check("W3", flag and rip(flag[0]) == [0x02AEDFB8] and S(flag[0]).endswith(", 1") and mask and ids == [1, 2, 3, 6, 34, 36, 54],
      "stop test %s; mask %s -> ids %s" % (S(flag[0]) if flag else "?", mask, ids))
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)   # a BROKEN row must fail the process, not only the text (ASTRA feb631dd4, 2026-09-29)
