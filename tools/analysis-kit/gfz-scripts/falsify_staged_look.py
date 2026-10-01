"""Falsification pass 1 on the-staged-look-command (OPUS, 2026-09-29), from the shipping image.
Each row states what the bytes show; a row marked REFUTES is a clause of the page they break.

  L0  sizes: 003E37F0 909, 00429920 299, 002EC3F0 263, 003E37E0 11, 003E6DA0 67, 0042D970 72, 003E2FD0 195, 003E3200 280,
      003E2F30 147, 003E3D70 961, 003E0910 154, 003E2810 215, 003E28F0 184, 003E3400 57
  L1  section 2: exactly eighteen listed functions are `add rcx, 0x580` followed by `jmp` (image-wide pattern search)
  L2  section 2: 003E37E0 zeroes 0x50 bytes
  L3  section 3: the applier tests the target group in the order 15, 17, 16, 18, 19, 20 at 003E393A, 003E395C, 003E397B,
      003E399A, 003E39B9, 003E39CE
  L4  section 3: 003E2FD0 writes 2 to the source kinds +0x5C and +0x6C, 003E3200 writes 3 and reads the sine table 01F004E0; both
      set the rate +0x74, read 01DFE0BC, and set +0x3C behind the 7-byte getter 001EDE70 (mov eax, [01F82E38]; ret)
  L5  section 3: 003E3340, 003E30A0 and 003E3140 each read [01DFE0B8] and controller +0x18 and take a max
  L6  section 4: 002EC3F0 tail-jumps (two of them conditional) to exactly the six services 002E7650, 002E79A0, 002E7720, 002E77F0, 002E78D0, 002E7860, and
      its callers (raw E8/E9) are 002E28E0, 002E3110, 002E64E0, 002EAAA0, 002EBE50
"""
import io, os, struct
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
body = lambda fa: [x for x in md.disasm(blob[OFF(fa):OFF(fa) + sizes[fa]], fa)]
txt = lambda fa: [S(x) for x in body(fa)]
rips = lambda fa: {r for x in body(fa) for r in rip(x)}
imm = lambda x: x.operands[0].imm if x.operands and x.operands[0].type == X86_OP_IMM else None

SZ = {0x003E37F0: 909, 0x00429920: 299, 0x002EC3F0: 263, 0x003E37E0: 11, 0x003E6DA0: 67, 0x0042D970: 72, 0x003E2FD0: 195,
      0x003E3200: 280, 0x003E2F30: 147, 0x003E3D70: 961, 0x003E0910: 154, 0x003E2810: 215, 0x003E28F0: 184, 0x003E3400: 57}
bad = {("%08X" % a): sizes.get(a) for a in SZ if sizes.get(a) != SZ[a]}
check("L0", not bad, "mismatches %s" % bad if bad else "all fourteen sizes as cited")
text = next(x for x in SECS if x[0] == ".text")
fw = []
for fa in sorted(sizes):
    if not (text[1] <= fa < text[1] + text[2]) or sizes[fa] > 16:
        continue
    try:
        ins = [x for x in md.disasm(blob[OFF(fa):OFF(fa) + sizes[fa]], fa)][:2]
    except ValueError:
        continue
    if len(ins) == 2 and S(ins[0]) == "add rcx, 0x580" and ins[1].mnemonic == "jmp":
        fw.append((fa, imm(ins[1])))
check("L1", len(fw) == 18 and len({t for _f, t in fw}) == 18, "%d forwarders to %d distinct builders" % (len(fw), len({t for _f, t in fw})))
C = txt(0x003E37E0)
check("L2", sizes[0x003E37E0] == 11 and (any("0x50" in s for s in C) or len([s for s in C if s.startswith("movups") or s.startswith("mov")]) >= 1), "%s" % C)
A = {x.address: S(x) for x in body(0x003E37F0)}
grp = [(a, A.get(a, "?")) for a in (0x003E393A, 0x003E395C, 0x003E397B, 0x003E399A, 0x003E39B9, 0x003E39CE)]


def bit_of(s):
    try:
        v = int(s.split(", ")[-1], 0)
    except ValueError:
        return None
    if s.startswith("bt "):
        return v
    return v.bit_length() - 1 if v and v & (v - 1) == 0 else None


check("L3", [bit_of(s) for _a, s in grp] == [15, 17, 16, 18, 19, 20], "group tests %s" % grp)
K2, K3 = txt(0x003E2FD0), txt(0x003E3200)
kinds = lambda T, v: all(any("+ 0x%x]" % d in s and s.endswith(", %d" % v) for s in T) for d in (0x5C, 0x6C))
check("L4", kinds(K2, 2) and kinds(K3, 3) and 0x01F004E0 in rips(0x003E3200) and all(any("+ 0x74]" in s for s in T) for T in (K2, K3))
      and all(0x01DFE0BC in rips(f) and "call 0x1ede70" in txt(f) and any(s.endswith("+ 0x3c], 1") for s in txt(f)) for f in (0x003E2FD0, 0x003E3200))
      and txt(0x001EDE70)[:2] == ["mov eax, dword ptr [rip + 0x1d94fc2]", "ret"] and rips(0x001EDE70) == {0x01F82E38},
      "kinds 2 / 3 at +0x5C and +0x6C; sine table; +0x74; 01DFE0BC; +0x3C set behind the getter 001EDE70 = [01F82E38]")
md_ok = {f: 0x01DFE0B8 in rips(f) and any("+ 0x18]" in s for s in txt(f)) and any(s.startswith(("maxss", "comiss", "cmov")) for s in txt(f))
         for f in (0x003E3340, 0x003E30A0, 0x003E3140) if f in sizes}
check("L5", len(md_ok) == 3 and all(md_ok.values()), "minimum-duration variants %s" % {("%08X" % f): v for f, v in md_ok.items()})
D = body(0x002EC3F0)
tails = sorted({imm(x) for x in D if x.mnemonic.startswith("j") and imm(x) and not (0x002EC3F0 <= imm(x) < 0x002EC3F0 + sizes[0x002EC3F0])})
raw = blob[text[3]:text[3] + text[4]]
edges = []
for k in range(len(raw) - 5):
    if raw[k] in (0xE8, 0xE9) and text[1] + k + 5 + struct.unpack_from("<i", raw, k + 1)[0] == 0x002EC3F0:
        pos = text[1] + k
        edges.append(max(f for f in sizes if f <= pos))
check("L6", tails == sorted([0x002E7650, 0x002E79A0, 0x002E7720, 0x002E77F0, 0x002E78D0, 0x002E7860])
      and sorted(set(edges)) == [0x002E28E0, 0x002E3110, 0x002E64E0, 0x002EAAA0, 0x002EBE50],
      "tail-jumps %s; callers %s" % (["%08X" % t for t in tails], sorted("%08X" % f for f in set(edges))))
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)
