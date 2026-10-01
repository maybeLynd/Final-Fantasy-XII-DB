"""mark_model.py - a static model of the marking fragment 003923D6..0039242E, checked against ASTRA's executed observations
(FABLE, Claude Opus 5.5, 2026-09-28, on ASTRA-REQ-FABLE-NAV-MARK-WRITE-DOMAIN). Decoded from the certified image's bytes.

  M1 the fragment's instructions are, in order: cdq; imul ecx, edi; and edx, 7; add eax, edx; mov r8d, eax; and eax, 7; sub eax, edx;
     sar r8d, 3; ... movzx ecx, byte [r8 + rdx]; bts ecx, eax; mov byte [r8 + rdx], cl; ... inc byte [rcx + rax]
  M2 modelled in 32-bit arithmetic (bts on a register takes its bit offset mod 32), the byte / bit each id marks agrees with every
     ASTRA observation: id 0 -> byte 0 bit 0; 287 -> byte 35 bit 7 (0x80); 288 -> byte 36 (the next record's byte 0, or the
     first occupancy byte after the last cell); -1 -> byte 0 with bit 31 of the register, so the stored low byte is unchanged;
     -8 -> byte -1 bit 0 (the preceding byte); the occupancy byte is a u8 increment, 255 -> 0
  M3 the builder never passes a negative id: phase 1 ids start at 0 (the count is reset to 0 and incremented), phase 2 at 0x80
     (mov ebx, ebp with ebp = 0x80) and phase 3 at 0xA0 + i with i from 0 (xor esi, esi before the loop)
  C  control: the model without the cdq/and/sub sign correction (a plain arithmetic shift and mask) disagrees with the
     observation for id -1
"""
import hashlib, os, re, struct, sys
import capstone
EXE = os.environ.get("FFXII_EXE", r"C:/Users/Kristian/source/repos/XIIOnline/Database/Tools/work/exe/FFXII_TZA.exe")
d = open(EXE, "rb").read()
if hashlib.sha256(d).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8": print("REFUSED  not the certified image"); sys.exit(2)
pe = struct.unpack_from("<I", d, 0x3c)[0]; ns = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [struct.unpack_from("<IIII", d, pe + 24 + opt + 40 * i + 8) for i in range(ns)]
off = lambda v: next(ra + v - 0x120000 - va for vs, va, rs, ra in SECS if va <= v - 0x120000 < va + rs)
MD = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
fails = 0
def ok(tag, cond, msg):
    global fails
    print(("PASS " if cond else "FAIL ") + tag + "  " + msg); fails += (not cond)
F = [(i.mnemonic + " " + i.op_str).strip() for i in MD.disasm(d[off(0x3923D6):off(0x3923D6) + 0x58], 0x3923D6)]
want = ["cdq", "imul ecx, edi", "and edx, 7", "add eax, edx", "mov r8d, eax", "and eax, 7", "sub eax, edx", "sar r8d, 3"]
core = [s for s in F if not s.startswith(("mov ecx, dword", "mov eax, r12d", "mov rdx, qword", "add ecx", "imul ecx, dword", "add ecx, r8d", "movsxd"))]
ok("M1", all(w in F for w in want) and F.index("cdq") < F.index("sar r8d, 3") < F.index("bts ecx, eax") and "mov byte ptr [r8 + rdx], cl" in F
   and "inc byte ptr [rcx + rax]" in F, "fragment order: sign-corrected divide by 8, bts on the loaded byte, store, occupancy inc")
s32 = lambda v: ((v + (1 << 31)) % (1 << 32)) - (1 << 31)
def mark(i, n=0x24):
    eax = s32(i); edx = -1 if eax < 0 else 0                  # cdq
    edx &= 7; eax = s32(eax + edx); r8 = eax                  # and edx, 7; add eax, edx; mov r8d, eax
    eax = (eax & 7); eax = s32(eax - edx)                      # and eax, 7; sub eax, edx
    r8 >>= 3                                                   # sar r8d, 3 (Python >> is arithmetic)
    bit = eax % 32                                             # bts reg, reg: offset mod 32
    byte0 = 0x00; reg = byte0 | (1 << bit); stored = reg & 0xFF
    return r8, bit, stored
obs = {0: (0, 0, 0x01), 287: (35, 7, 0x80), 288: (36, 0, 0x01), -1: (0, 31, 0x00), -8: (-1, 0, 0x01)}
got = {i: mark(i) for i in obs}
occ = (255 + 1) & 0xFF
ok("M2", got == obs and occ == 0, "model vs ASTRA's executed cases (byte, bit, stored low byte): %s; occupancy 255 + 1 -> %d" % (got, occ))
P = {i.address: (i.mnemonic + " " + i.op_str).strip() for i in MD.disasm(d[off(0x392740):off(0x392740) + 702], 0x392740)}
ok("M3", P[0x392777] == "mov dword ptr [rip + 0x275b93f], esi" and P[0x392761] == "xor esi, esi" and P[0x3928AE].startswith("mov ecx, dword ptr [rip")
   and P[0x3928B9].startswith("inc dword ptr [rip") and P[0x3927FF] == "mov ebp, 0x80" and P[0x392917] == "mov ebx, ebp" and P[0x39295C] == "inc ebx"
   and P[0x3928CA] == "xor esi, esi" and P[0x3929BD] == "lea ecx, [rsi + 0xa0]" and P[0x3929DA] == "inc esi",
   "ids come from a count reset to 0, from 0x80 upward, and from 0xA0 + i with i from 0: none negative")
def naive(i): return (i >> 3, i & 7)
ok("C", naive(-1) != (obs[-1][0], obs[-1][1]), "a plain shift-and-mask gives %s for id -1, not the observed (0, 31)" % (naive(-1),))
print("FAILS", fails); sys.exit(1 if fails else 0)
