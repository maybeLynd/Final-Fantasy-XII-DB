"""sr3_numbering.py - control for SR-3's second half (FABLE, Claude Opus 5.5, 2026-09-26).

Question: is sebsoundplay_2c1's bank selector (003A1100 / 003A1070 / 003A1180) the same numbering the bank loaders use?
Answer read here: yes, and the shared number is the SE-block REGISTRY INDEX, not the .seb file's own block number.
  R1 registration 003A1650 validates its handle against the 02AEEDC0 entry (words +8 / +0xA rebuilt, bit 31 cleared)
     and passes the entry's word +8 - the handle's low word, the index - to 002DEF00.
  R2 002DEF00 keeps `ecx & 0x3F` and passes the file's word +8 separately (edx); 001DBD20 -> 00210B60
     (`mov rcx, [rcx+8]; jmp 0021B430`, registry +8) -> 0021B430 forwards edx and r8d unchanged into 00223AD0.
  R3 00223AD0 stores its edx (the index) at bank +0x3C and its r8d (the file's block number) at bank +0x38; the
     comparison of the two file copies (`cmp eax, r13d; sete cl; call 0016D6A0`) is inert, 0016D6A0 being a bare `ret`.
     (The first draft said r8d was used only in that check; the planted negative below caught the +0x38 store.)
  R4 each selector builds `(entry word +8 << 9) + cue` after the same validation: 003A1100 (handle 02AEF400),
     003A1070 (guard 02AEF400, handle 02AEF404), 003A1180 (handle 02AEF3FC).
  R5 the Seb controller's lookup 0021B5B0 splits an id with `sar 9` and compares the block against bank +0x3C.
Planted negative: R3 also asserts that the file-block register never reaches the +0x3C store (a matcher that credited
any register would fail); it is what caught the +0x38 store the first draft missed.
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import re, struct, sys, bisect
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

ROOT = Path(__file__).resolve().parents[5]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64)
STARTS = sorted(int(l.split("\t")[0], 16) for l in open(ROOT / "Database/Tools/work/graph/functions.tsv", encoding="utf-8",
                errors="replace") if re.match(r"[0-9A-Fa-f]{8}\t", l))
def whole(a):
    i = bisect.bisect_right(STARTS, a)
    return list(cs.disasm(d[off(a):off(STARTS[i])], a))
def T(a): return ["%s %s" % (x.mnemonic, x.op_str) for x in whole(a)]
def rip(x):
    m = re.search(r"\[rip ([+-]) (0x[0-9a-f]+)\]", x.op_str)
    return x.address + x.size + (1 if m.group(1) == "+" else -1) * int(m.group(2), 16) if m else None
def seq_in(lst, seq):
    i = 0
    for s in lst:
        if i < len(seq) and s == seq[i]: i += 1
    return i == len(seq)
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)

# R1
R = T(0x3A1650)
check("R1 003A1650: entry word +8 / +0xA rebuilt against the handle, word +8 passed to 002DEF00",
      seq_in(R, ["btr edi, 0x1f", "movzx ecx, word ptr [rbx + rax*8 + 8]", "movzx eax, word ptr [rbx + 0xa]",
                 "shl eax, 0x10", "or eax, ecx", "cmp eax, edi", "cmovne ecx, edx", "call 0x2def00"]))
# R2
check("R2 002DEF00: ecx & 0x3F, edx = file word +8, then 001DBD20",
      T(0x2DEF00)[:6] == ["and ecx, 0x3f", "mov r8, rdx", "test rdx, rdx", "je 0x2def14", "movsx edx, word ptr [rdx + 8]", "jmp 0x1dbd20"])
check("R2 001DBD20 -> 00210B60 with (edx=index, r8d=file block, r9=buffer); 00210B60 = registry +8 -> 0021B430",
      seq_in(T(0x1DBD20), ["mov edi, edx", "mov esi, ecx", "mov r9, rbx", "mov r8d, edi", "mov edx, esi", "jmp 0x210b60"])
      and T(0x210B60)[:2] == ["mov rcx, qword ptr [rcx + 8]", "jmp 0x21b430"])
check("R2 0021B430 forwards edx (edi) and r8d (ebp) into 00223AD0",
      seq_in(T(0x21B430), ["mov edi, edx", "mov ebp, r8d", "mov r8d, ebp", "mov edx, edi", "call 0x223ad0"]))
# R3
I = T(0x223AD0)
check("R3 00223AD0: edx -> [rsp+0x34] -> bank +0x3C",
      seq_in(I, ["mov dword ptr [rsp + 0x34], edx", "mov eax, dword ptr [rsp + 0x34]", "mov dword ptr [r15 + 0x3c], eax"]))
r13 = [s for s in I if "r13d" in s]
check("R3 planted negative: r8d (file block) goes to bank +0x38 and the inert check, never to +0x3C",
      r13 == ["mov r13d, r8d", "cmp eax, r13d", "mov dword ptr [r15 + 0x38], r13d"] and T(0x16D6A0)[0].startswith("ret")
      and not any(s.startswith("mov dword ptr [r15 + 0x3c], r13") for s in I), str(r13))
# R4
for sel, handle in ((0x3A1100, 0x2AEF400), (0x3A1070, 0x2AEF404), (0x3A1180, 0x2AEF3FC)):
    X = whole(sel); S = ["%s %s" % (x.mnemonic, x.op_str) for x in X]
    loads = [rip(x) for x in X if x.mnemonic == "mov" and x.op_str.startswith("r8d, dword ptr [rip")]
    check("R4 %08X: handle %08X validated, id = (word +8 << 9) + cue" % (sel, handle),
          loads == [handle] and seq_in(S, ["shl ecx, 0x10", "or ecx, edx", "cmp ecx, r8d", "shl edx, 9", "add edx, ebx"]),
          str([hex(v) for v in loads]))
# R5
C = T(0x21B5B0)
check("R5 0021B5B0 splits the id with sar 9 and matches bank +0x3C",
      seq_in(C, ["cdq ", "and edx, 0x1ff", "sar edi, 9", "cmp dword ptr [r10 + 0x3c], edi"]) or
      seq_in(C, ["cdq", "and edx, 0x1ff", "sar edi, 9", "cmp dword ptr [r10 + 0x3c], edi"]))
print("FAILS", fails)
sys.exit(1 if fails else 0)
