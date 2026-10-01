"""Falsification pass 1 on how-a-path-is-resolved-to-bytes.md (OPUS, 2026-09-29), from the shipping image. Killers first.

  R0  section 1: 00D26C60 is slot 0 (00598210) plus four _purecall; 00D26C90's seven slots are 00598280, 0059BD40, 0059D920,
      0059ED70, 0059FAC0, 0059D4B0, 0059FDA0
  R1  section 2: slot 2 (0059D920) is 27 bytes and returns !(+0x28 == -1 && +0x30 == 0 && +0x40 == -1)
  R2  section 2a: the ownership bit is tested at three sites - slot 3, slot 4 and the base destructor 00598100
  R3  (REFUTES the selector census's "24") 00597970 has 18 call sites and 00597930 two; the selector is r8b for 00597970 and
      r9b for 00597930. At 001DAFCC the selector is `lea r8d, [r14 + 3]`, and every path to it writes r14b first - 0 at
      001DAEA2 or 1 at 001DAFB5 - so that site passes 3 or 4, never 24
  R4  section 3: the prefetch token loop 001DA810..001DA83F passes 5, constructs, closes (0059BD40), destroys (00598100)
  R5  section 4: 0059EE90 has six call sites - five in Resource bodies (three constructors, two rebinds including slot 3)
      and one in the Audio body 00225BA0
  R6  section 4: the three tags sit at 00D27930, 00D27910 and 00D27948 and 0059EE90 references all three
  R7  section 5: route 1 is 001D6D20 -> 0020C1B0, which builds the key with 0020C440 and hashes it with 00674A00: seed
      0x1505, `imul eax, eax, 0x21` plus the signed char, `btr eax, 0x1f`
  R8  section 6: the resolver calls 0019AEE0, which holds CryptCreateHash's ALG_ID 0x8003 and is the only caller of the digest
      tree 001F47D0 (+0x18 then +0x20); the resolver returns 10 on failure
"""
import collections, io, os, struct
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


sizes, names, layer = {}, {}, {}
for i, line in enumerate(io.open(FUNCS, encoding="utf-8", errors="replace")):
    p = line.rstrip("\n").split("\t")
    if i and len(p) > 3:
        try:
            a = int(p[0], 16); sizes[a] = int(p[2]); names[p[1]] = a; layer[a] = p[3]
        except ValueError:
            pass
S = lambda x: ("%s %s" % (x.mnemonic, x.op_str)).strip()
rip = lambda x: [x.address + x.size + o.mem.disp for o in x.operands if o.type == X86_OP_MEM and o.mem.base == X86_REG_RIP]
T = lambda x: x.operands[0].imm if x.operands and x.operands[0].type == X86_OP_IMM else None
text = next(x for x in SECS if x[0] == ".text")

refs = collections.defaultdict(list)          # target -> [(function, insn)]
calls_to = collections.defaultdict(list)      # target -> [(function, address, mnemonic)]
bodies = {}
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
        if x.mnemonic in ("call", "jmp") and T(x) is not None:
            calls_to[T(x)].append((fa, x.address, x.mnemonic))


def run(fa, lo, hi):
    return [S(x) for x in bodies[fa] if lo <= x.address <= hi]


q = lambda va: struct.unpack("<Q", blob[OFF(va):OFF(va) + 8])[0]

# R0
v0 = [q(0x00D26C60 + 8 * i) for i in range(5)]
v1 = [q(0x00D26C90 + 8 * i) for i in range(7)]
pc = names.get("_purecall")
check("R0", v0 == [0x00598210] + [pc] * 4 and v1 == [0x00598280, 0x0059BD40, 0x0059D920, 0x0059ED70, 0x0059FAC0, 0x0059D4B0, 0x0059FDA0],
      "PStream %s; PStreamReaderFile %s" % (["%08X" % v for v in v0], ["%08X" % v for v in v1]))
# R1
check("R1", sizes.get(0x0059D920) == 27 and [S(x) for x in bodies[0x0059D920]][:6] == ["cmp qword ptr [rcx + 0x28], -1", "jne 0x59d938", "cmp qword ptr [rcx + 0x30], 0",
                                                                                    "jne 0x59d938", "cmp qword ptr [rcx + 0x40], -1", "jne 0x59d938"],
      "0059D920 %d B: false only when +0x28 == -1, +0x30 == 0 and +0x40 == -1" % sizes.get(0x0059D920))
# R2
bit = {f: [S(x) for x in bodies[f] if lo <= x.address <= hi] for f, lo, hi in ((0x0059ED70, 0x0059EDBF, 0x0059EDC9), (0x0059FAC0, 0x0059FADB, 0x0059FAE9), (0x00598100, 0x00598120, 0x0059812B))}
check("R2", all(any(("1" in s and s.startswith(("test", "and"))) for s in v) for v in bit.values()),
      "; ".join("%08X %s" % (f, v) for f, v in bit.items()))
# R3 the selector census
def sel(fa, call_va, reg):
    b = bodies[fa]; k = next(i for i, x in enumerate(b) if x.address == call_va)
    for y in reversed(b[max(0, k - 10):k]):
        s = S(y)
        if s.startswith(("mov %sb," % reg, "mov %sd," % reg, "xor %sd, %sd" % (reg, reg), "lea %sd," % reg)):
            return s
    return None
cen = collections.Counter()
detail = []
for tgt, reg in ((0x00597970, "r8"), (0x00597930, "r9")):
    for f, a, _m in calls_to[tgt]:
        s = sel(f, a, reg)
        v = 0 if s and s.startswith("xor") else (int(s.split(", ")[1], 16) if s and s.startswith("mov") else s)
        cen[v] += 1; detail.append(("%08X" % a, v))
b = bodies[0x001DADC0]; idx = {x.address: i for i, x in enumerate(b)}
kill = [x.address for x in b if x.op_str.startswith(("r14b,", "r14d,", "r14,")) and x.mnemonic in ("mov", "xor", "lea", "movzx")]
seen, st, reach = set(), [b[0].address], False
while st:
    a = st.pop()
    if a in seen or a not in idx:
        continue
    seen.add(a); x = b[idx[a]]
    if a in kill:
        continue
    if a == 0x001DAFCC:
        reach = True; break
    nxt = []
    if x.mnemonic == "jmp":
        nxt = [T(x)] if T(x) is not None else []
    elif x.mnemonic.startswith("j"):
        nxt = ([T(x)] if T(x) is not None else []) + ([b[idx[a] + 1].address] if idx[a] + 1 < len(b) else [])
    elif x.mnemonic != "ret":
        nxt = [b[idx[a] + 1].address] if idx[a] + 1 < len(b) else []
    st += nxt
kv = [S(x) for x in b if x.address in kill]
check("R3", len(calls_to[0x00597970]) == 18 and len(calls_to[0x00597930]) == 2 and "mov byte ptr [rcx + 0x18], r9b" in [S(x) for x in bodies[0x00597930]]
      and cen[0] == 5 and cen[5] == 1 and ("lea r8d, [r14 + 3]" in cen) and kv == ["xor r14b, r14b", "mov r14b, 1"] and not reach,
      "census %s; 001DAFCC 'lea r8d, [r14 + 3]' is reached only after %s, so it passes 3 or 4" % (dict(cen), kv))
# R4
check("R4", run(0x001DA610, 0x001DA810, 0x001DA81B) == ["mov r8b, 5", "mov rdx, qword ptr [rbx + 0x10]", "lea rcx, [rsp + 0x38]", "call 0x597970"]
      or (run(0x001DA610, 0x001DA810, 0x001DA810) == ["mov r8b, 5"] and "call 0x597970" in run(0x001DA610, 0x001DA810, 0x001DA81B)
          and "call 0x59bd40" in run(0x001DA610, 0x001DA81C, 0x001DA830) and "call 0x598100" in run(0x001DA610, 0x001DA81C, 0x001DA835)),
      "%s" % run(0x001DA610, 0x001DA810, 0x001DA83F))
# R5
rc = sorted(("%08X" % f, layer.get(f)) for f, _a, _m in calls_to[0x0059EE90])
check("R5", len(calls_to[0x0059EE90]) == 6 and [l for _f, l in rc].count("Resource") == 5 and ("00225BA0", "Audio") in rc
      and {"00597930", "00597970", "00597A70", "0059ED70", "0059EE10"} <= {f for f, _l in rc}, "%s" % rc)
# R6
tags = {va: blob[OFF(va):OFF(va) + 48].split(b"\0")[0] for va in (0x00D27930, 0x00D27910, 0x00D27948)}
used = {va: any(f == 0x0059EE90 for f, _x in refs[va]) for va in tags}
check("R6", tags[0x00D27930].startswith(b"[FFXII_data] %s") and tags[0x00D27910].startswith(b"[FFXII_data_notcache]")
      and tags[0x00D27948].startswith(b"[FFXII_ERROR] Big file open failed") and all(used.values()), "%s; referenced by 0059EE90 %s" % (tags, used))
# R7 route 1: 001D6D20 -> 0020C1B0, which builds the key with 0020C440 and hashes it with 00674A00
chain = [T(x) for x in bodies[0x001D6D20] if x.mnemonic in ("call", "jmp")]
k1 = [T(x) for x in bodies[0x0020C1B0] if x.mnemonic == "call"]
hb = [S(x) for x in bodies[0x00674A00]]
check("R7", 0x0020C1B0 in chain and 0x0020C440 in k1 and 0x00674A00 in k1 and "mov eax, 0x1505" in hb and "imul eax, eax, 0x21" in hb
      and "movsx edx, dl" in hb and "btr eax, 0x1f" in hb,
      "001D6D20 -> 0020C1B0 -> key 0020C440, hash 00674A00: %s" % [s for s in hb if s.startswith(("mov eax, 0x", "imul", "movsx", "btr"))])
# R8 route 2: the MD5 body 0019AEE0 (called by the resolver) and its digest tree 001F47D0
md5 = [S(x) for x in bodies[0x0019AEE0]]
rs = [S(x) for x in bodies[0x0059EE90]]
tree = [S(x) for x in bodies[0x001F47D0]]
check("R8", 0x0019AEE0 in [T(x) for x in bodies[0x0059EE90] if x.mnemonic == "call"] and any("0x8003" in s for s in md5)
      and [f for f, _a, _m in calls_to[0x001F47D0]] == [0x0019AEE0] and "mov rax, qword ptr [rdx + 0x18]" in tree
      and "cmp qword ptr [rdx + 0x20], r9" in tree and "mov eax, 0xa" in rs,
      "0059EE90 -> 0019AEE0 (CryptCreateHash ALG 0x8003) -> 001F47D0 (+0x18 then +0x20); failure returns 10")
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)   # a BROKEN row must fail the process, not only the text (ASTRA feb631dd4, 2026-09-29)
