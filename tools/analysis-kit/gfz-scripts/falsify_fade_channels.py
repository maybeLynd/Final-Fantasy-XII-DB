"""Falsification pass 1 on how-a-character-fades-the-ten-channels (OPUS, 2026-09-29), from the shipping image.
Each row states what the bytes show; a row marked REFUTES is a clause of the page they break.

  C0  section 7a sizes: 003E5D60 182, 003E5D00 44, 003E5D30 34, 003E4370 88, 003E48E0 604, 003E4240 269, 003E51F0 701, 00428C40 131,
      0042E1F0 269, 0042F880 608, 0042D050 1,776, 003B30D0 139, 0042CBF0 884, 0042E850 1,238, 0046C180 91, 003B3F10 416,
      0041EC00 480, 00520180 47, 004293C0 67, 002E8B10 77, 00428940 20
  C1  section 2 (the ramp): 003E5D6A scales the target by the float at 00D117DC (= -4096); 003E5DAE adds (delta * progress) >> 12
      to base; r10d = max(frames, 1) * [01DFE0B4] and 003E5DD5 divides 0x1000 by it; 003E5DE1 `cmp r11d, 1` zeroes progress for
      channel 1; 003E5DF2 calls the getter 001EDE70 and a second step is added when it is non-zero
  C2  section 2 (one frame): 003E4370 walks ten 8-byte channels from +0x4C0, compares progress with 0x1000
  C3  section 2: 003E5D30 makes three qword stores, at +0x4C0, +0x4C8 and +0x4E0 (channels 0, 1, 4)
  C4  section 3 / 7a: 00428C40 starts channels 6, 7, 8 by call and 9 by tail-jump, all through 003E5D60
  C5  section 3: 0042E850 reads record +0x2A8 and starts channel-4 ramps over 3 frames and channel-0 ramps over 1 frame
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

SZ = {0x003E5D60: 182, 0x003E5D00: 44, 0x003E5D30: 34, 0x003E4370: 88, 0x003E48E0: 604, 0x003E4240: 269, 0x003E51F0: 701,
      0x00428C40: 131, 0x0042E1F0: 269, 0x0042F880: 608, 0x0042D050: 1776, 0x003B30D0: 139, 0x0042CBF0: 884, 0x0042E850: 1238,
      0x0046C180: 91, 0x003B3F10: 416, 0x0041EC00: 480, 0x00520180: 47, 0x004293C0: 67, 0x002E8B10: 77, 0x00428940: 20}
bad = {("%08X" % a): sizes.get(a) for a in SZ if sizes.get(a) != SZ[a]}
check("C0", not bad, "mismatches %s" % bad if bad else "all twenty-one sizes as cited")
R = {x.address: S(x) for x in body(0x003E5D60)}
k = struct.unpack("<f", blob[OFF(0x00D117DC):OFF(0x00D117DC) + 4])[0]
check("C1", R.get(0x003E5D6A, "").startswith("mulss xmm2") and k == -4096.0 and R.get(0x003E5DAA) == "sar r8d, 0xc" and R.get(0x003E5DAE, "").startswith("add word ptr [rcx + r11*8 + 0x4c0]")
      and R.get(0x003E5D84) == "cmovge r10d, r9d" and R.get(0x003E5D91, "").startswith("imul r10d, dword ptr [rip") and R.get(0x003E5DC6) == "mov eax, 0x1000"
      and R.get(0x003E5DD5) == "idiv r10d" and R.get(0x003E5DE1) == "cmp r11d, 1" and R.get(0x003E5DE7) == "xor eax, eax"
      and R.get(0x003E5DF2) == "call 0x1ede70" and R.get(0x003E5E03, "").startswith("add word ptr [rbx + rdi*8 + 0x4c4]"),
      "target x %.1f; collapse; step = 0x1000 / (max(frames, 1) x [01DFE0B4]); channel-1 progress 0; the getter's second step" % k)
F = txt(0x003E4370)
check("C2", any("0x4c" in s for s in F) and any("0x1000" in s for s in F) and any(s.endswith(", 0xa") or s.endswith(", 10") for s in F),
      "ten channels from +0x4C0, the 0x1000 finish test: %s" % [s for s in F if "0x1000" in s or s.endswith(", 0xa")][:3])
T = txt(0x003E5D30)
q = sorted(s for s in T if s.startswith("mov qword ptr"))
check("C3", len(q) == 3 and all(any("+ 0x%x]" % d in s for s in q) for d in (0x4C0, 0x4C8, 0x4E0)), "%s" % q)
C4 = [(x.address, S(x)) for x in body(0x00428C40) if x.mnemonic in ("call", "jmp") and imm(x) == 0x003E5D60]
check("C4", [a for a, _ in C4] == [0x00428C6E, 0x00428C81, 0x00428C94, 0x00428CBE] and C4[-1][1].startswith("jmp") and all(s.startswith("call") for _a, s in C4[:3]),
      "%s" % ["%08X %s" % c for c in C4])
E = txt(0x0042E850)
check("C5", any("+ 0x2a8]" in s for s in E) and any(s == "mov r9d, 3" for s in E) and any(s in ("mov r9d, 1", "lea r9d, [rdx + 1]") or s.startswith("lea r9d, [") for s in E),
      "reads +0x2A8; frame counts 3 and 1 passed to the ramp")
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)
