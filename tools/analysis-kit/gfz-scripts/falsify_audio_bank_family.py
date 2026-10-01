"""Falsification pass 1 on CONTRACT-audio-bank-and-controller-family (OPUS, 2026-09-29), from the shipping image.
Each row states what the bytes show; a row marked REFUTES is a clause of the page they break.

  A0  section 2: each vtable's slot 0 and slot 7 are the cited bodies; the slot count (consecutive qwords pointing into .text)
      is 11 for every bank and 7 / 8 for the controllers as tabulated
  A1  AC-1 / AC-2: every bank's slot 7 is 52 B and calls a destructor, tests bl bit 0, loads a size into edx and calls the
      free routine; slot 0 of every controller is a body that contains the same free call
  A2  AC-3: the four 8-slot controllers' slot 7 is 9 B, `add rcx, 0x20` then `jmp`, to four distinct targets of 161 B each
  A3  AC-4: 00222550 calls [rax + 0x48] per entry, and 00222580 `mov rax, qword ptr [rdi]` is the loop-back target (00222596)
  A4  AC-5: five banks share slot 0 = 00222550; MusicAudioBank's 00222C00 is 101 B and calls no free routine
  A5  AC-6 (as corrected): slot 10 is 00222C70 (Music), 00223540 (Sep), 00224B30 (Seb), 00225440 (Shout and Stream), and
      AudioBank's is a _purecall; each reads byte [manager + 0x3C] with the tabulated masks
  A6  AC-7 (as corrected): 00223100 and 002230D0 compute [+0x38] - 0x249F0 and return below 0x3E8 (unsigned), 00223130 acts
      at-or-above; Seb's copies divide by 1000 with 0x10624DD3 / sar 6 and compare 0x96
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
pe = pefile.PE(EXE); BASE = pe.OPTIONAL_HEADER.ImageBase
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
q = lambda va: struct.unpack("<Q", blob[OFF(va):OFF(va) + 8])[0]
text = next(x for x in SECS if x[0] == ".text")
ins = lambda fa, n=None: list(md.disasm(blob[OFF(fa):OFF(fa) + (n or sizes[fa])], fa))
imm = lambda x: x.operands[0].imm if x.operands and x.operands[0].type == X86_OP_IMM else None
iat = {}
for e in pe.DIRECTORY_ENTRY_IMPORT:
    for imp in e.imports:
        if imp.name:
            iat[imp.address] = imp.name.decode()


def slots(vt):
    n = 0
    while text[1] <= q(vt + 8 * n) < text[1] + text[2]:
        n += 1
    return n


BANK = {"AudioBank": (0x009078B0, 0x00222550, 0x00218260), "MusicAudioBank": (0x00907910, 0x00222C00, 0x002182A0),
        "SebAudioBank": (0x00907D80, 0x00222550, 0x0021ABC0), "SepAudioBank": (0x00907B48, 0x00222550, 0x002195D0),
        "ShoutAudioBank": (0x00907F90, 0x00222550, 0x0021BF20), "StreamAudioBank": (0x009081A0, 0x00222550, 0x0021CD80)}
CTRL = {"AudioController": (0x00906CD0, 7, 0x002127D0, None), "MusicAudioController": (0x00907970, 8, 0x002182E0, 0x00218980),
        "SebAudioController": (0x00907DE0, 8, 0x0021AC00, 0x0021B150), "SepAudioController": (0x00907BA8, 8, 0x00219610, 0x00219B10),
        "ShoutAudioController": (0x00907FF0, 8, 0x0021BF60, 0x0021C440), "StreamAudioController": (0x00908200, 7, 0x0021CDC0, None)}
bs = {k: (slots(v[0]), q(v[0]), q(v[0] + 56)) for k, v in BANK.items()}
cs = {k: (slots(v[0]), q(v[0]), q(v[0] + 56) if v[1] == 8 else None) for k, v in CTRL.items()}
check("A0", all(bs[k] == (11, v[1], v[2]) for k, v in BANK.items()) and all(cs[k] == (v[1], v[2], v[3]) for k, v in CTRL.items()),
      "banks (slots, s0, s7) %s; controllers %s" % ({k: (v[0], "%08X" % v[1], "%08X" % v[2]) for k, v in bs.items()},
                                                   {k: (v[0], "%08X" % v[1], "%08X" % v[2] if v[2] else None) for k, v in cs.items()}))


def frees(fa):
    out = []
    for x in ins(fa):
        if x.mnemonic in ("call", "jmp"):
            t = imm(x)
            if t is None and x.operands[0].type == X86_OP_MEM and x.operands[0].mem.base == X86_REG_RIP:
                t = x.address + x.size + x.operands[0].mem.disp
            out.append(t)
    return out


s7 = {k: [S(x) for x in ins(v[2])] for k, v in BANK.items()}
freefn = collections.Counter(c[-1] for c in (frees(v[2]) for v in BANK.values()) if c)
FREE = freefn.most_common(1)[0][0]
idiom = {k: sizes[v[2]] == 52 and any(s == "test bl, 1" for s in s7[k]) and any(s.startswith("mov edx, ") for s in s7[k]) and FREE in frees(v[2]) for k, v in BANK.items()}
ctrl0 = {k: FREE in frees(v[2]) for k, v in CTRL.items()}
check("A1", all(idiom.values()) and all(ctrl0.values()), "bank slot 7 = 52 B sized delete (free %08X): %s; controller slot 0 calls it: %s" % (FREE, idiom, ctrl0))
th = {k: [S(x) for x in ins(v[3], 9)] for k, v in CTRL.items() if v[3]}
tg = {k: int(v[1].split()[-1], 16) for k, v in th.items()}
check("A2", all(sizes[CTRL[k][3]] == 9 and v[0] == "add rcx, 0x20" and v[1].startswith("jmp") for k, v in th.items())
      and len(set(tg.values())) == 4 and all(sizes.get(t) == 161 for t in tg.values()),
      "thunks %s; targets %s" % ({k: v[:2] for k, v in th.items()}, {k: ("%08X" % t, sizes.get(t)) for k, t in tg.items()}))
L = {x.address: x for x in ins(0x00222550)}
check("A3", S(L[0x00222580]) == "mov rax, qword ptr [rdi]" and S(L[0x00222596]) == "jne 0x222580" and any("[rax + 0x48]" in S(x) and x.mnemonic == "call" for x in L.values()),
      "%s / %s; slot-9 call inside the loop" % (S(L[0x00222580]), S(L[0x00222596])))
check("A4", sum(1 for v in BANK.values() if v[1] == 0x00222550) == 5 and sizes[0x00222C00] == 101 and FREE not in frees(0x00222C00),
      "five share 00222550; 00222C00 %d B, calls %s" % (sizes[0x00222C00], ["%08X" % c for c in frees(0x00222C00) if c]))
s10 = {k: q(v[0] + 80) for k, v in BANK.items()}
pure = s10["AudioBank"]
px = next(md.disasm(blob[OFF(pure):OFF(pure) + 16], pure))
pure_ok = iat.get(px.address + px.size + px.operands[0].mem.disp) if px.mnemonic == "jmp" and px.operands[0].type == X86_OP_MEM else None
reads = {f: any("+ 0x3c]" in S(x) for x in ins(f)) for f in (0x00222C70, 0x00223540, 0x00224B30, 0x00225440)}
check("A5", s10["MusicAudioBank"] == 0x00222C70 and s10["SepAudioBank"] == 0x00223540 and s10["SebAudioBank"] == 0x00224B30
      and s10["ShoutAudioBank"] == s10["StreamAudioBank"] == 0x00225440 and all(reads.values()) and pure_ok == "_purecall",
      "slot 10 %s; AudioBank's %08X jumps through the IAT to %s; each reads +0x3C %s" % ({k: "%08X" % v for k, v in s10.items()}, pure, pure_ok, {"%08X" % f: v for f, v in reads.items()}))
g3, g4, g5 = ([S(x) for x in ins(f)] for f in (0x00223100, 0x002230D0, 0x00223130))
band = lambda g: any("0x249f0" in s for s in g) and any("0x3e8" in s for s in g)
seb = [f for f in sizes if 0x00223000 <= f < 0x00226000 and any("0x10624dd3" in S(x) for x in ins(f))]
sebok = [f for f in seb if any(S(x).startswith("sar") and x.op_str.endswith(", 6") for x in ins(f)) and any("0x96" in S(x) and x.mnemonic == "cmp" for x in ins(f))]
check("A6", band(g3) and band(g4) and band(g5) and any(s.startswith("jb ") for s in g3 + g4) and any(s.startswith("jae ") for s in g5) and len(sebok) >= 3,
      "Sep slots 3/4/5 test 0x249F0 +- 0x3E8; Seb copies with the /1000 == 150 test: %s" % ["%08X" % f for f in sebok])
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)
