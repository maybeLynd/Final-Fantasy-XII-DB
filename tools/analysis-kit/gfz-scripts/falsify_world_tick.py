"""Falsification pass 1 on CONTRACT-world-simulation-tick (OPUS, 2026-09-29), from the shipping image. Killers first.

  T0  section 2: 00314020 is 845 B with three call sites (two pass ecx = 1, one xor ecx); 00314960 is 7 B, mov eax, [022C2548]; ret
  T1  WT-1: the mode lives in r14d (00314042) and is tested at 003140CF, 003140DC, 00314103/00314108 and 00314249/0031424E
  T2  WT-2: 0025BFB0 is called at 00314078, before the first mode test
  T3  WT-3: 022C2548 has exactly three rip-relative accesses image-wide - writes 00314047 (1) and 0031435D (0), read 00314960;
      the body has exactly one ret (0031436C)
  T4  WT-4: 01EED064 has 16 rip-relative accesses, 4 writes and 12 reads; 01EED060 and 01EED064 hold 0xFFFFFFFF in the image
  T5  WT-5: `cmp ebx, 5` at 00314132, 003141E9, 00314218, 00314270; `cmp ebp, 5` at 0031425D; `cmp esi, 0x10` at 0031421F;
      mode 1 starts at slot 3 (003140D9 `xor r13d, r13d`, 003140FF `lea ebp, [r13 + 3]`)
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
T = lambda x: x.operands[0].imm if x.operands and x.operands[0].type == X86_OP_IMM else None
text = next(x for x in SECS if x[0] == ".text")
refs = collections.defaultdict(list)
calls = []
bodies = {}
for fa in sorted(sizes):
    if not (text[1] <= fa < text[1] + text[2]):
        continue
    try:
        code = blob[OFF(fa):OFF(fa) + sizes[fa]]
    except ValueError:
        continue
    ins = list(md.disasm(code, fa))
    if fa in (0x00314020, 0x00314960):
        bodies[fa] = ins
    for i, x in enumerate(ins):
        for t in rip(x):
            refs[t].append(x)
        if x.mnemonic == "call" and T(x) == 0x00314020:
            calls.append([S(y) for y in ins[max(0, i - 4):i]])
b = bodies[0x00314020]
I = {x.address: x for x in b}
at = lambda va: S(I[va]) if va in I else "?"
is_w = lambda x: x.operands and x.operands[0].type == X86_OP_MEM and x.mnemonic in ("mov", "and", "or", "inc", "dec", "add", "sub")

modes = sorted(0 if c[-1] == "xor ecx, ecx" else 1 if (c[-1] == "mov ecx, 1" or (c[-1] == "mov ecx, edx" and "mov edx, 1" in c)) else -1 for c in calls)
check("T0", sizes[0x00314020] == 845 and len(calls) == 3 and modes == [0, 1, 1]
      and [S(x) for x in bodies[0x00314960]][:2] == ["mov eax, dword ptr [rip + 0x1fadbe2]", "ret"] and sizes[0x00314960] == 7,
      "845 B; call-site modes %s; getter %s" % (modes, [S(x) for x in bodies[0x00314960]][:2]))
check("T1", at(0x00314042) == "mov r14d, ecx" and all("r14" in at(a) for a in (0x003140CF, 0x003140DC, 0x00314103, 0x00314249)),
      "%s; tests %s" % (at(0x00314042), [at(a) for a in (0x003140CF, 0x003140DC, 0x00314103, 0x00314249)]))
check("T2", at(0x00314078) == "call 0x25bfb0" and 0x00314078 < 0x003140CF and not any("r14" in S(x) for x in b if 0x00314042 < x.address < 0x003140CF),
      "the queue drain at 00314078 precedes every mode test")
a = refs[0x022C2548]
rets = [x for x in b if x.mnemonic == "ret"]
check("T3", sorted(("%08X" % x.address, is_w(x)) for x in a) == [("00314047", True), ("0031435D", True), ("00314960", False)]
      and len(rets) == 1 and rets[0].address == 0x0031436C, "accesses %s; rets %s" % ([("%08X" % x.address, S(x)) for x in a], ["%08X" % x.address for x in rets]))
d = refs[0x01EED064]
u32 = lambda va: struct.unpack("<I", blob[OFF(va):OFF(va) + 4])[0]
check("T4", len(d) == 16 and sum(1 for x in d if is_w(x)) == 4 and u32(0x01EED060) == 0xFFFFFFFF and u32(0x01EED064) == 0xFFFFFFFF,
      "%d accesses, %d writes; image values %08X / %08X" % (len(d), sum(1 for x in d if is_w(x)), u32(0x01EED060), u32(0x01EED064)))
check("T5", all(at(v) == "cmp ebx, 5" for v in (0x00314132, 0x003141E9, 0x00314218, 0x00314270)) and at(0x0031425D) == "cmp ebp, 5"
      and at(0x0031421F) == "cmp esi, 0x10" and at(0x003140D9) == "xor r13d, r13d" and at(0x003140FF) == "lea ebp, [r13 + 3]",
      "bounds are immediates; mode 1 starts at 3")
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)   # a BROKEN row must fail the process, not only the text (ASTRA feb631dd4, 2026-09-29)
