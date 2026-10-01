"""WidgetSingleton02CA99C0: +0xD8..+0x397 is a queue of eight 0x58-byte save-storage operations (OPUS, 2026-09-27).
Control. Static.
  Q1 00582240 (SaveStorageQueue_CompleteFrontOperationAndNotify) takes rdx = this + 0xD8, decrements the count byte
     +0x398, shifts every entry down by 0x58 (0x58 bytes copied per entry: five 16-byte moves and one 8-byte move,
     00582290-005822D9) and clears the dword at this + 0xD8 + count * 0x58 (005822E6); bit 1 of the front entry's +0x04
     decides whether the notify callback at +0xC0 is called (0058225D-00582272, 00582373-0058238E)
  Q2 the layout closes: 0xD8 + 8 * 0x58 = 0x398, the count byte
  Q3 the start routine 00582040 switches on the front entry's +0x00 dword (kinds 0..12, jump table at 00582092), sets
     its +0x04 bit 0 (005820BD), and reads the payload at mixed widths - +0x08 as a qword and +0x10 as a dword copied
     into the parent's +0xC0 / +0xC8 (0058209E-005820B2), +0x08 as a byte (005820E7), +0x08 by address (00582110 and
     five more), +0x48 as a qword or a byte, +0x4C as a dword, +0x50 as a dword or a byte
  Q4 STORE REGRESSION: +0xD8 is WidgetSingleton02CA99C0QueueEntry[8] and no parent row starts inside +0xD8..+0x397
Not claimed: what each kind does; the payload's per-kind layout (it is a union read at several widths, so it stays one
mixed span); what the callback at +0xC0 is.
"""
import os, struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]; DB = HERE.parents[2]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes(); BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in SECS:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def I(f, size): return {x.address: "%s %s" % (x.mnemonic, x.op_str) for x in cs.disasm(d[off(f):off(f) + size], f)}
C, S = I(0x582240, 357), I(0x582040, 460)
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)
check("Q1 the completion shifts 0x58-byte entries from +0xD8 down, count byte +0x398, clears the vacated entry",
      C.get(0x582256) == "lea rdx, [rcx + 0xd8]" and C.get(0x582278) == "mov byte ptr [rcx + 0x398], al"
      and C.get(0x582290) == "movups xmm0, xmmword ptr [rdx + 0x58]" and C.get(0x58229A) == "movups xmmword ptr [rdx], xmm0"
      and C.get(0x5822BB) == "movsd xmm1, qword ptr [rdx + 0xa8]" and C.get(0x5822C7) == "movsd qword ptr [rdx + 0x50], xmm1"
      and C.get(0x5822CC) == "lea rdx, [rdx + 0x58]" and C.get(0x5822E2) == "imul rcx, rax, 0x58"
      and C.get(0x5822E6) == "mov dword ptr [rcx + rbx + 0xd8], ebp"
      and C.get(0x58225D) == "mov r8d, dword ptr [rcx + 0xdc]" and C.get(0x58226C) == "shr r8d, 1"
      and C.get(0x582373) == "mov rax, qword ptr [rbx + 0xc0]" and C.get(0x58238E) == "call rax")
check("Q2 eight entries end exactly at the count byte", 0xD8 + 8 * 0x58 == 0x398)
check("Q3 the start routine switches on +0x00, sets +0x04 bit 0 and reads the payload at mixed widths",
      S.get(0x58207F) == "movsxd rax, dword ptr [rcx + 0xd8]" and S.get(0x582086) == "cmp eax, 0xc"
      and S.get(0x5820BD) == "or dword ptr [rbx + 0xdc], 1"
      and S.get(0x58209E) == "mov rax, qword ptr [rbx + 0xe0]" and S.get(0x5820A5) == "mov qword ptr [rbx + 0xc0], rax"
      and S.get(0x5820AC) == "mov eax, dword ptr [rbx + 0xe8]" and S.get(0x5820B2) == "mov dword ptr [rbx + 0xc8], eax"
      and S.get(0x5820E7) == "movzx ecx, byte ptr [rbx + 0xe0]" and S.get(0x582110) == "lea rcx, [rbx + 0xe0]"
      and S.get(0x582157) == "mov r8, qword ptr [rbx + 0x120]" and S.get(0x58212B) == "movzx ecx, byte ptr [rbx + 0x120]"
      and S.get(0x58211E) == "mov eax, dword ptr [rbx + 0x124]" and S.get(0x582149) == "mov r9d, dword ptr [rbx + 0x128]"
      and S.get(0x58216A) == "movzx r8d, byte ptr [rbx + 0x128]")
rows = []
for l in open(os.environ.get("FIELDS_PATH") or DB / "_types/fields.tsv", encoding="utf-8"):
    c = l.rstrip("\r\n").split("\t")
    if len(c) == 9 and c[0] == "WidgetSingleton02CA99C0": rows.append((int(c[1], 16), int(c[2]), c[3], c[4]))
inside = [r[2] for r in rows if 0xD8 < r[0] < 0x398]
check("Q4 STORE REGRESSION: +0xD8 is QueueEntry[8], nothing starts inside it",
      any(r[0] == 0xD8 and r[3] == "WidgetSingleton02CA99C0QueueEntry[8]" for r in rows) and not inside, str(inside[:6]))
print("FAILS", fails)
sys.exit(1 if fails else 0)
