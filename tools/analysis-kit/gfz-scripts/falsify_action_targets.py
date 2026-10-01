"""Falsification pass 1 on how-an-action-gathers-its-targets (OPUS, 2026-09-29), from the shipping image.
Each row states what the bytes show; a row marked REFUTES is a clause of the page they break. The 543-row census
(_experiments/evidence/action-area-bytes) is carried, not re-run.

  T0  sizes: 0030D160 1004, 002FFEF0 85, 0030BB10 27, 0030BCB0 24, 0031A990 154, 002FFED0 23; the gatherer's one caller
      00304EE2; 002FFED0's one caller 00322490 with (unit, 0, 3); the shape wrapper 0031AA30's three callers
  T1  section 2: radius byte +0x06 at 0030D255, squared; bit 21 of +0x0C at 0030D271; +0x07 at 0030D2EC scaled by
      2 pi (01CEBC78) / 360 (00902438); the cone bit 24 at 0030D3B1 and the line bit 25 at 0030D3E3
  T2  section 2 / 3: the eligibility call 002FFEF0(candidate, actor, 1), whose classifier call passes 0 as its third argument
      with the candidate first
  T3  section 3 - competing case: a raw E8/E9 sweep finds no call from the gatherer to 0030BB10 or 0030BCB0; the gatherer
      loads 0030BB10 with lea, keeps 0030BCB0 in rbp, picks by +0x36 bit 2 with cmovne and calls through rax
      (0030D37C..0030D38D) with (primary r12, candidate rdi, 1); bit 3 skips the test
  T4  section 3: 0030BB10 = ((class & ~2) == 0) and 0030BCB0 = (class <= 1); a non-zero answer skips the candidate
  T5  section 4: the slot tail on +0x6B6; the whole-party tail on +0x0C bit 1 with the 0x80000003 mask
  T6  section 5: 0031A990 - radius 0 or bit 12 -> 5 with bit 1 else 0; bit 24 -> 3 with radius and radians; bit 25 -> 4 with
      radius; else bit 21 -> 2 or 1
  T7  the SWE2-EC7-96 notes on 0030BB10 and 002FFEF0
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
at = lambda fa: {x.address: S(x) for x in body(fa)}
txt = lambda fa: [S(x) for x in body(fa)]
f32 = lambda va: struct.unpack("<f", blob[OFF(va):OFF(va) + 4])[0]
text = next(x for x in SECS if x[0] == ".text")
raw = blob[text[3]:text[3] + text[4]]


def callers(t):
    return sorted(text[1] + k for k in range(len(raw) - 5)
                  if raw[k] in (0xE8, 0xE9) and text[1] + k + 5 + struct.unpack_from("<i", raw, k + 1)[0] == t)


SZ = {0x0030D160: 1004, 0x002FFEF0: 85, 0x0030BB10: 27, 0x0030BCB0: 24, 0x0031A990: 154, 0x002FFED0: 23}
bad = {("%08X" % a): sizes.get(a) for a in SZ if sizes.get(a) != SZ[a]}
check("T0", not bad and callers(0x0030D160) == [0x00304EE2] and callers(0x002FFED0) == [0x003224ED]
      and at(0x00322490).get(0x003224E9) == "lea r8d, [rdx + 3]" and len(callers(0x0031AA30)) == 3,
      "sizes %s; the gatherer's caller 00304EE2; 002FFED0 (unit, 0, 3); three wrapper callers" % (bad or "all six as cited"))
G = {x.address: (S(x), rip(x)) for x in body(0x0030D160)}
check("T1", G[0x0030D255][0] == "movzx edx, byte ptr [rsi + 6]" and G[0x0030D2BD][0] == "imul eax, eax"
      and G[0x0030D271][0] == "test dword ptr [rsi + 0xc], 0x200000" and G[0x0030D2EC][0] == "movzx eax, byte ptr [rsi + 7]"
      and G[0x0030D300][1] == [0x01CEBC78] and abs(f32(0x01CEBC78) - 6.283185) < 1e-5 and f32(0x00902438) == 360.0
      and G[0x0030D3B1][0] == "bt eax, 0x18" and G[0x0030D3E3][0] == "bt eax, 0x19",
      "radius +0x06 squared; bit 21 centre; +0x07 x 2 pi / 360; cone bit 24; line bit 25")
E = at(0x002FFEF0)
check("T2", G[0x0030D353][0] == "mov r8d, 1" and G[0x0030D35C][0] == "mov rcx, rax" and G[0x0030D35F][0] == "call 0x2ffef0"
      and E.get(0x002FFF11) == "xor r8d, r8d" and E.get(0x002FFF14) == "call 0x30ab40",
      "002FFEF0(candidate, actor, 1); inside, 0030AB40(candidate, actor, 0)")
check("T3", 0x0030D160 not in {c for c in callers(0x0030BB10)} and not any(0x0030D160 <= c < 0x0030D54C for c in callers(0x0030BB10) + callers(0x0030BCB0))
      and G[0x0030D326][1] == [0x0030BCB0] and G[0x0030D326][0].startswith("lea rbp") and G[0x0030D37C][1] == [0x0030BB10]
      and G[0x0030D374][0] == "test al, 4" and G[0x0030D386][0] == "cmovne rax, rbp" and G[0x0030D38D][0] == "call rax"
      and G[0x0030D38A][0] == "mov rcx, r12" and G[0x0030D383][0] == "mov rdx, rdi" and G[0x0030D370][0] == "test al, 8",
      "competing case: no direct call from the gatherer (raw sweep); the predicate is picked into rax and called indirectly "
      "at 0030D38D with (primary, candidate, 1); bit 3 bypasses")
check("T4", txt(0x0030BB10)[1:4] == ["call 0x30ab40", "test eax, 0xfffffffd", "mov eax, 0"] and txt(0x0030BCB0)[1:5] == ["call 0x30ab40", "xor ecx, ecx", "cmp eax, 1", "setbe cl"]
      and G[0x0030D391][0] == "jne 0x30d42e",
      "0030BB10 true on class 0 or 2; 0030BCB0 true on 0 or 1; true skips")
check("T5", G[0x0030D205][0] == "cmp byte ptr [r13 + 0x6b6], bl" and G[0x0030D249][0] == "mov byte ptr [r13 + 0x6b6], bl"
      and G[0x0030D461][0] == "test byte ptr [rsi + 0xc], 2" and G[0x0030D4A1][0] == "test ecx, 0x80000003",
      "the +0x6B6 slot tail; the bit-1 whole-party tail with the KO / Stone / Vanish mask")
D = at(0x0031A990)
check("T6", D.get(0x0031A995) == "cmp byte ptr [rcx + 6], al" and D.get(0x0031A99E) == "bt r8d, 0xc" and D.get(0x0031A9AC) == "mov dword ptr [rdx], 3"
      and D.get(0x0031A9EC) == "mov dword ptr [rdx], 4" and D.get(0x0031A9F4) == "bt r8d, 0x15" and D.get(0x0031A9FC) == "inc eax"
      and D.get(0x0031AA19) == "mov dword ptr [rdx], 5" and D.get(0x0031AA27) == "mov dword ptr [rdx], eax",
      "shapes 0-5 with bit 12 as 'no area'")
check("T7", sorted(callers(0x0030BB10)) == [0x00323182] and 0x0030D35F in callers(0x002FFEF0) and 0x00324941 in callers(0x002FFEF0)
      and E.get(0x002FFF1C) == "cmp eax, 1" and E.get(0x002FFF1F) == "ja 0x2fff23" and E.get(0x002FFF35) == "sete bl",
      "the EC7-96 notes hold: 0030BB10 wrapped by 003230E0 (directly) and the gatherer (indirectly); 002FFEF0's gated apply")
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)
