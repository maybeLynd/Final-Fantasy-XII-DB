"""script_var_ref.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only.
For ASTRA-REQ-OPUS-SCRIPT-STORE-SATURATION (_experiments/evidence/script-store-saturation/). Written without ASTRA's code.
The record the script VM's variable resolver fills and the store / load leaves read, and the store's per-width policy.

  S  THE STORE 0026D530 (no call anywhere in it): width = record +0x18 >> 28; above 5 it returns without a store. The table at
     image base + 0x14D5F4 (0026D5F4) sends 0..5 to: 0 u8 clamp [0, 255] (a negative stores 0); 1 s8 clamp [-128, 127];
     2 u16 clamp [0, 0xFFFF]; 3 s16 with floor 0xFFFF8001 (-32767) and ceiling 0x8000 (+32768), then a word store - so +32768
     and above store 0x8000, which a signed read gives back as -32768; 4 and 5 the raw dword. Destination = +0x10 + index
     (+0x1C, sign-extended) times the width's size
  R  THE RECORD: 00267E60 (POPV) and 00267FC0 (PUSHV) each pass a 0x30-byte stack local (rsp + 0x30 under `sub rsp, 0x60`;
     rbp - 0x30) as 00262440's fifth argument. 00262440 writes +0x00 = 6, word +0x04 (2 when descriptor bit 27 is set,
     else r13w), word +0x08 (the word at its second argument), word +0x0A (the operand, r9w), +0x0C (the table entry's
     descriptor), +0x10 (the resolved address: the class base chosen by descriptor bits 24..26 plus the low 24 bits),
     +0x18 (the final descriptor) and +0x1C (the element index). POPV stores the value at +0x20 and calls 0026D530 on the
     record; PUSHV reads by the same width table into +0x20. POPV reads +0x04 as a signed word
  C  THE INDEX (for ASTRA-REQ-OPUS-SCRIPT-ARRAY-CLAMP): 00262440 reads the array header's u16 rank at +4 (rank - 1 < 0 skips the
     loop) and s32 dimensions from +8, last first; each popped subscript (cvttss2si or a dword, 00262571 / 0026257D) becomes
     m = max(s, 0) (ebx = 0 is the floor, cmovns), then m if m < dim (signed 32-bit cmp against dim itself, cmovl) else the
     32-bit dim - 1 (lea eax, [rsi - 1]) - for a strictly positive dimension that is min(max(s, 0), dim - 1); dim 0 yields -1 and
     nothing rejects it; the product of later dimensions scales it and r10d is summed into +0x1C. (The first text here said
     "min(max(s, 0), dim - 1) ... cmovl against dim - 1" for every dimension; corrected by A)
  A  THE SIGNED MINIMUM (for ASTRA-REQ-OPUS-SCRIPT-ARRAY-SIGNEDMIN): the same instructions in 32-bit arithmetic: for any dim <= 0,
     m < dim is false (m >= 0), so the stage is the 32-bit dim - 1 whatever the subscript: dim 0 -> -1, dim -2 -> -3, and
     dim 0x80000000 (INT_MIN) -> 0x7FFFFFFF (2147483647), where unbounded min(max(s, 0), dim - 1) says -2147483649. The model
     agrees with that formula for dims 5, 1, 0, -2 and INT_MIN + 1 and differs only at INT_MIN (control). No shipped array has
     such a dimension to our knowledge, and the later-dimension products (32-bit imul) are not claimed
  L  THE FLATTEN WIDTH (for ASTRA-REQ-OPUS-SCRIPT-ARRAY-FLATTEN): the sum starts at 0 (00262487 mov r10d, ebx) and the product
     at 1 (002624AD mov r8d, r13d, r13d = 1 from 00262478); rbp starts at the last dimension (header + 8 + 4 * (rank - 1)) and
     steps back 4 (0026251B), so the first popped subscript pairs with the last dimension. Each pass is imul eax, r8d (stage
     times product), imul r8d, esi (product times dimension) and add r10d, eax - all 32-bit, with no jo / jc / overflow branch
     before the loop's jns, so products, contributions and the sum wrap modulo 2^32. r10d goes to +0x1C (00262672) and
     0026D530 reads it back signed (0026D537 movsxd). Conditional arithmetic, not execution or a shipped array: dims 2 x 3 at
     (1, 0) -> 3 and (1, 2) -> 5; 65536 x 65536 at (32768, 0) -> 0x80000000 = INT_MIN and at (65535, 65535) -> 0xFFFFFFFF = -1.
     Faults rejected: unbounded arithmetic (2147483648), saturation, forward pairing ((1, 0) -> 1)
  K  THE KIND AND THE ORDER (for ASTRA-REQ-OPUS-SCRIPT-POPV-CONVERSION): +0x04 is the value kind, not a count - the resolver writes
     2 when descriptor bit 27 is set, else 1; POPV branches on it: kind 1 truncates a float operand (cvttss2si) and copies an int,
     kind 2 converts an int (cvtdq2ps); an empty stack gives 0; the converted value goes to +0x20 and only then 0026D530 clamps by
     width. First named count04 (7f169f26f); renamed kind04 here
  N  THE LOOKUP (for ASTRA-REQ-OPUS-SCRIPT-POPV-LOOKUP): 0032F240 is 32 bytes, two rets, no call and no store - it reads a byte flag
     at 022C6D18 + i and returns the dword at 022C6D28 + 4i, or -1. POPV calls it only when [rdi + 0x28] - 1 <= 2 and the resolver
     returned 0, then 0026D530 loads eax from the record (0026D53B) before any read: the returned id is discarded on this path
  F  THE FLOAT ROUNDING (for ASTRA-REQ-OPUS-SCRIPT-FLOAT-ROUNDING): kind 2 with an integer operand is movd (00267EC9), cvtdq2ps
     (00267ED2), movss into +0x20 (00267ED5), then 0026D530's width 4 / 5 arm copies the dword raw. POPV has no ldmxcsr, fldcw or
     rounding override, so cvtdq2ps rounds by the MXCSR RC the thread already has. Arithmetic: every |n| <= 2^24 converts
     exactly, so RC shows only above 2^24; 16777217 gives 0x4B800000 (16777216) under round-to-nearest-even and 0x4B800001
     (16777218) under round-up, the two values ASTRA's isolated controls record. Which RC the game runs with is not claimed.
     SIGN (for ASTRA-REQ-OPUS-SCRIPT-NEGATIVE-ROUNDING): round-up moves toward +infinity, so for a negative value the raw bits
     step DOWN: -16777219 gives 0xCB800002 (-16777220) under nearest-even and 0xCB800001 (-16777218) under round-up. The first
     version of this check's helper added 1 to the bits for round-up whatever the sign; it was only ever run on the positive
     case, and on -16777219 it would say 0xCB800003 (-16777222). The helper is now sign-aware, and that old rule is a
     rejected control here
  P  PUSHP'S REFERENCE (for ASTRA-REQ-OPUS-SCRIPT-REFERENCE-CARRY): 00268100 reads descriptor18 (00268118) and index1C
     (00268120), scales the index by the width's stride through the table at image base + 0x1481A4 (widths 0/1 unscaled,
     2/3 add edx, edx, 4/5 lea edx, [rdx*4]; above 5 unscaled), writes the ORIGINAL width into the record's +0x00 (00268150)
     and pushes its low byte as the value's source kind (00268180 / 00268185), tag 1, and the dword
     low32((d & 0xFFFFFF) + scaled) | (d & 0x07000000) | 0x70000000 (00268158..0026816C, stored at 00268194). Nothing masks
     after the add, so the class is kept and the width is 7 only while the sum stays below 2^24. Conditional arithmetic, not
     execution: 02FFFFFE + 1 -> 72FFFFFF (class 2, width 7); 02FFFFFF + 1 -> 73000000 (class 3); 02000000 - 1 -> FFFFFFFF
     (class 7, width 15, bit 27 set); 42000000 - 1*4 -> FFFFFFFC. Rejected models: a final 24-bit mask (72000000) and an
     exact width-7 replacement (7FFFFFFC)
  W  REGRESSION (FAILS before): the type ScriptVariableRef30 is in the store and tiles; value20 states the RC dependence and
     the sign rule; kind00 and descriptor18 state PUSHP's use and its offset domain
Not claimed: why the s16 range is [-32767, +32768]; what +0x04 / +0x08 mean beyond their writers; +0x24..+0x2F.
Usage: python script_var_ref.py [--patch]
"""
import hashlib, os, struct, sys
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__)); DB = os.path.abspath(os.path.join(HERE, "..", "..", "..")); ROOT = os.path.dirname(DB)
EXEP = os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe")
d = open(EXEP, "rb").read()
if hashlib.sha256(d).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8":
    print("REFUSED  not the certified image"); sys.exit(2)
B = 0x120000
pe = pefile.PE(EXEP, fast_load=True)
off = lambda v: pe.get_offset_from_rva(v - B)
cs = Cs(CS_ARCH_X86, CS_MODE_64)
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
def has(lo, hi, pairs):
    A = {x.address: (x.mnemonic, x.op_str) for x in cs.disasm(d[off(lo):off(hi)], lo)}
    miss = [hex(a) for a, v in pairs if A.get(a) != v]
    if miss: print("   missing", miss)
    return not miss
L = list(cs.disasm(d[off(0x26D530):off(0x26D5F2)], 0x26D530))
table = [struct.unpack_from("<I", d, off(0x26D5F4) + 4 * i)[0] + B for i in range(6)]
check("S", not any(x.mnemonic == "call" for x in L) and table == [0x26D55F, 0x26D57E, 0x26D5A1, 0x26D5C4, 0x26D5E9, 0x26D5E9]
      and has(0x26D530, 0x26D5F2, [(0x26D537, ("movsxd", "rcx, dword ptr [rcx + 0x1c]")), (0x26D53F, ("shr", "eax, 0x1c")), (0x26D542, ("cmp", "eax, 5")),
                                   (0x26D545, ("ja", "0x26d5f1")), (0x26D54B, ("lea", "r10, [rip - 0x14d552]")), (0x26D552, ("mov", "edx, dword ptr [r10 + rax*4 + 0x14d5f4]")),
                                   (0x26D568, ("jns", "0x26d570")), (0x26D56A, ("xor", "eax, eax")), (0x26D570, ("mov", "ecx, 0xff")), (0x26D577, ("cmovg", "eax, ecx")),
                                   (0x26D585, ("cmp", "eax, -0x80")), (0x26D58A, ("mov", "eax, 0xffffff80")), (0x26D593, ("mov", "ecx, 0x7f")),
                                   (0x26D5B4, ("mov", "ecx, 0xffff")), (0x26D5BE, ("mov", "word ptr [r8 + rdx*2], ax")),
                                   (0x26D5C7, ("mov", "eax, 0xffff8001")), (0x26D5D2, ("jl", "0x26d5e3")), (0x26D5D4, ("mov", "r9d, 0x8000")), (0x26D5DF, ("cmovg", "eax, r9d")),
                                   (0x26D5E3, ("mov", "word ptr [r8 + rdx*2], ax")), (0x26D5ED, ("mov", "dword ptr [r8 + rcx*4], eax")), (0x26D5F1, ("ret", ""))])
      and 0x26D552 - 0x14D552 == B,
      "0026D530: no call; width > 5 returns; 0 u8 [0,255], 1 s8 [-128,127], 2 u16 [0,0xFFFF], 3 s16 [-32767,+32768] then a word store, 4/5 raw dword")
check("R", has(0x267E60, 0x267E90, [(0x267E6B, ("sub", "rsp, 0x60")), (0x267E6F, ("lea", "rax, [rsp + 0x30]")), (0x267E77, ("mov", "qword ptr [rsp + 0x20], rax")),
                                     (0x267E7F, ("call", "0x262440")), (0x267E84, ("movsx", "r8d, word ptr [rsp + 0x34]"))])
      and has(0x267F1A, 0x267F3C, [(0x267F1A, ("mov", "dword ptr [rsp + 0x50], eax")), (0x267F32, ("lea", "rcx, [rsp + 0x30]")), (0x267F37, ("call", "0x26d530"))])
      and has(0x267FC0, 0x268010, [(0x267FC9, ("sub", "rsp, 0x60")), (0x267FCD, ("lea", "rax, [rbp - 0x30]")), (0x267FD4, ("mov", "qword ptr [rsp + 0x20], rax")),
                                   (0x267FD9, ("call", "0x262440")), (0x267FDE, ("mov", "eax, dword ptr [rbp - 0x18]")), (0x267FFC, ("movsxd", "rcx, dword ptr [rbp - 0x14]")),
                                   (0x268000, ("mov", "rax, qword ptr [rbp - 0x20]")), (0x268008, ("mov", "dword ptr [rbp - 0x10], ecx"))])
      and has(0x262440, 0x26268F, [(0x26245F, ("mov", "r15, qword ptr [rsp + 0x80]")), (0x26248D, ("mov", "word ptr [r15 + 0xa], r9w")), (0x262492, ("mov", "dword ptr [r15 + 0xc], r12d")),
                                   (0x262644, ("bt", "r12d, 0x1b")), (0x262650, ("mov", "word ptr [r15 + 4], cx")), (0x262657, ("mov", "word ptr [r15 + 4], r13w")),
                                   (0x262661, ("mov", "qword ptr [r15 + 0x10], rax")), (0x262667, ("mov", "dword ptr [r15], 6")), (0x26266E, ("mov", "dword ptr [r15 + 0x18], r12d")),
                                   (0x262672, ("mov", "dword ptr [r15 + 0x1c], r10d")), (0x262676, ("movzx", "ecx, word ptr [rbp]")), (0x26267A, ("mov", "word ptr [r15 + 8], cx"))]),
      "POPV / PUSHV pass a 0x30-byte local to 00262440 (5th argument); the resolver's writes, POPV's value at +0x20 and the store call")
check("C", has(0x262440, 0x26268F, [(0x26245D, ("xor", "ebx, ebx")), (0x262478, ("lea", "r13d, [rbx + 1]")), (0x262487, ("mov", "r10d, ebx")),
                                     (0x2624B3, ("movzx", "eax, word ptr [rcx + 4]")), (0x2624BA, ("sub", "eax, r13d")), (0x2624BD, ("movsxd", "r13, eax")), (0x2624C0, ("js", "0x262546")),
                                     (0x2624D5, ("mov", "esi, dword ptr [rbp]")), (0x26250A, ("mov", "eax, ebx")), (0x26250C, ("test", "eax, eax")), (0x26250E, ("mov", "ecx, ebx")),
                                     (0x262510, ("cmovns", "ecx, eax")), (0x262513, ("lea", "eax, [rsi - 1]")), (0x262516, ("cmp", "ecx, esi")), (0x262518, ("cmovl", "eax, ecx")),
                                     (0x26251F, ("imul", "eax, r8d")), (0x262523, ("imul", "r8d, esi")), (0x262527, ("add", "r10d, eax")),
                                     (0x262571, ("cvttss2si", "eax, dword ptr [r14 + rdx*4 + 0x184]")), (0x26257B, ("jmp", "0x26250c")),
                                     (0x26257D, ("mov", "eax, dword ptr [r14 + rdx*4 + 0x184]")), (0x262585, ("jmp", "0x26250c")),
                                     (0x262672, ("mov", "dword ptr [r15 + 0x1c], r10d"))]),
      "index1C: a u16 rank at header +4 (rank 0 skips the loop), s32 dimensions from header +8 last first; each popped subscript -> m = max(s, 0), "
      "then m if m < dim (signed) else the 32-bit dim - 1 (no dimension check: dim 0 gives -1), times the product of the later dimensions, summed into r10d -> +0x1C")
def w32(v): v &= 0xFFFFFFFF; return v - (1 << 32) if v & 0x80000000 else v
def stage(s, dim):                                         # 0026250A..00262518 in 32-bit arithmetic
    m = s if s >= 0 else 0; lim = w32((dim & 0xFFFFFFFF) - 1)
    return m if m < dim else lim
IMIN, IMAX = -(1 << 31), (1 << 31) - 1
def flatten(dims, subs):                                   # subs in source order; the loop pops the last one first
    acc, prod = 0, 1
    for dm, s in zip(reversed(dims), reversed(subs)):     # rbp walks from the last dimension back
        acc = (acc + stage(s, dm) * prod) & 0xFFFFFFFF; prod = (prod * dm) & 0xFFFFFFFF
    return w32(acc)
def unbounded(dims, subs):
    acc, prod = 0, 1
    for dm, s in zip(reversed(dims), reversed(subs)): acc += min(max(s, 0), dm - 1) * prod; prod *= dm
    return acc
def saturating(dims, subs): return max(IMIN, min(IMAX, unbounded(dims, subs)))
def forward(dims, subs):
    acc, prod = 0, 1
    for dm, s in zip(dims, subs): acc += min(max(s, 0), dm - 1) * prod; prod *= dm
    return acc
Lp = list(cs.disasm(d[off(0x262440):off(0x26268F)], 0x262440))
Lr = [x for x in Lp if 0x26250A <= x.address <= 0x262537]
cases = {((2, 3), (1, 0)): 3, ((2, 3), (1, 2)): 5, ((65536, 65536), (0, 0)): 0, ((65536, 65536), (32768, 0)): IMIN, ((65536, 65536), (65535, 65535)): -1}
check("L", has(0x262478, 0x26253A, [(0x262478, ("lea", "r13d, [rbx + 1]")), (0x262487, ("mov", "r10d, ebx")), (0x2624AD, ("mov", "r8d, r13d")),
                                     (0x2624C6, ("lea", "rbp, [rcx + 8]")), (0x2624CD, ("lea", "rbp, [rbp + r13*4]")), (0x2624D5, ("mov", "esi, dword ptr [rbp]")),
                                     (0x26251B, ("sub", "rbp, 4")), (0x26251F, ("imul", "eax, r8d")), (0x262523, ("imul", "r8d, esi")), (0x262527, ("add", "r10d, eax")),
                                     (0x26252A, ("sub", "r13, r15")), (0x26252D, ("mov", "dword ptr [rsp + 0x78], r10d")), (0x262537, ("jns", "0x2624d2"))])
      and has(0x262672, 0x262676, [(0x262672, ("mov", "dword ptr [r15 + 0x1c], r10d"))]) and has(0x26D530, 0x26D53B, [(0x26D537, ("movsxd", "rcx, dword ptr [rcx + 0x1c]"))])
      and not any(x.mnemonic in ("jo", "jno", "jc", "jb", "jae", "jnc") for x in Lr)
      and all(flatten(dm, sb) == v for (dm, sb), v in cases.items())
      and unbounded((65536, 65536), (32768, 0)) == 2147483648 and saturating((65536, 65536), (32768, 0)) == IMAX and forward((2, 3), (1, 0)) == 1,
      "sum 0, product 1, last dimension first; imul / imul / add in 32 bits with no overflow branch; +0x1C read back with movsxd: "
      "2x3 (1,0) -> 3, 65536x65536 (32768,0) -> INT_MIN, (65535,65535) -> -1; unbounded, saturating and forward models rejected")
subs = (-1, 0, 3, IMAX)
naive = lambda s, dim: min(max(s, 0), dim - 1)
agree = all(stage(s, dm) == naive(s, dm) for dm in (5, 1, 0, -2, IMIN + 1) for s in subs)
check("A", has(0x26250C, 0x26251C, [(0x262510, ("cmovns", "ecx, eax")), (0x262513, ("lea", "eax, [rsi - 1]")), (0x262516, ("cmp", "ecx, esi")),
                                     (0x262518, ("cmovl", "eax, ecx"))]) and agree
      and [stage(s, IMIN) for s in subs] == [IMAX] * 4 and naive(0, IMIN) == -2147483649 and stage(0, 0) == -1 and stage(7, -2) == -3,
      "the compare is against dim and the fallback is the 32-bit dim - 1: INT_MIN gives 0x7FFFFFFF for every subscript (unbounded formula: -2147483649); "
      "dims 5, 1, 0, -2, INT_MIN + 1 agree with min(max(s, 0), dim - 1)")
check("K", has(0x267E60, 0x267F60, [(0x267E84, ("movsx", "r8d, word ptr [rsp + 0x34]")), (0x267E8C, ("sub", "r8d, 1")), (0x267E90, ("je", "0x267ef2")),
                                     (0x267E92, ("cmp", "r8d, 1")), (0x267EC9, ("movd", "xmm0, dword ptr [rbx + rdx*4 + 0x184]")), (0x267ED2, ("cvtdq2ps", "xmm0, xmm0")),
                                     (0x267EB8, ("movss", "xmm0, dword ptr [rbx + rdx*4 + 0x184]")), (0x267F18, ("xor", "eax, eax")), (0x267F1A, ("mov", "dword ptr [rsp + 0x50], eax")),
                                     (0x267F37, ("call", "0x26d530")), (0x267F4C, ("cvttss2si", "eax, dword ptr [rbx + rdx*4 + 0x184]")), (0x267F55, ("jmp", "0x267f1a")),
                                     (0x267F57, ("mov", "eax, dword ptr [rbx + rdx*4 + 0x184]"))])
      and has(0x262640, 0x26265C, [(0x262644, ("bt", "r12d, 0x1b")), (0x26264B, ("mov", "ecx, 2")), (0x262650, ("mov", "word ptr [r15 + 4], cx"))]),
      "POPV converts by +0x04 (1 integer: float tag cvttss2si, int raw; 2 float: int tag cvtdq2ps, float raw; empty stack 0) into +0x20, then calls 0026D530")
Lk = list(cs.disasm(d[off(0x32F240):off(0x32F260)], 0x32F240))
check("N", [(x.address, x.mnemonic) for x in Lk if x.mnemonic in ("call", "ret")] == [(0x32F25B, "ret"), (0x32F25F, "ret")]
      and not any(x.op_str.startswith(("byte ptr", "word ptr", "dword ptr", "qword ptr")) and x.mnemonic == "mov" for x in Lk)
      and has(0x32F240, 0x32F260, [(0x32F243, ("lea", "rcx, [rip - 0x20f24a]")), (0x32F24A, ("cmp", "byte ptr [rax + rcx + 0x21a6d18], 0")),
                                   (0x32F254, ("mov", "eax, dword ptr [rcx + rax*4 + 0x21a6d28]"))]) and 0x32F24A - 0x20F24A == B
      and has(0x267F1E, 0x267F3C, [(0x267F1E, ("mov", "ecx, dword ptr [rdi + 0x28]")), (0x267F21, ("lea", "eax, [rcx - 1]")), (0x267F24, ("cmp", "eax, 2")),
                                   (0x267F27, ("ja", "0x267f32")), (0x267F29, ("test", "esi, esi")), (0x267F2D, ("call", "0x32f240")),
                                   (0x267F32, ("lea", "rcx, [rsp + 0x30]")), (0x267F37, ("call", "0x26d530"))])
      and [(x.mnemonic, x.op_str) for x in L[:4]] == [("mov", "r8, qword ptr [rcx + 0x10]"), ("mov", "r9, rcx"), ("movsxd", "rcx, dword ptr [rcx + 0x1c]"), ("mov", "eax, dword ptr [r9 + 0x18]")],
      "0032F240: two rets, no call, no store - a read of the byte flags at 022C6D18 and the dword ids at 022C6D28 (-1 when off); POPV calls it only "
      "when [rdi+0x28]-1 <= 2 and the resolver returned 0, and 0026D530 overwrites eax (0026D53B) before reading it: the returned id is discarded")
Pf = list(cs.disasm(d[off(0x267E60):off(0x267F60)], 0x267E60))
def f32_bits(n, up):
    lo = struct.unpack("<I", struct.pack("<f", float(n)))[0]            # Python rounds to nearest-even
    v = struct.unpack("<f", struct.pack("<I", lo))[0]
    if not up or v >= n: return lo
    return lo - 1 if lo & 0x80000000 else lo + 1                         # toward +infinity: a negative's magnitude shrinks
def f32_bits_first_version(n, up):                                       # the rule this check first used: +1 whatever the sign
    lo = struct.unpack("<I", struct.pack("<f", float(n)))[0]
    v = struct.unpack("<f", struct.pack("<I", lo))[0]
    return lo + 1 if up and v < n else lo
exact = all(struct.unpack("<f", struct.pack("<f", float(n)))[0] == n for n in (2 ** 24, -(2 ** 24), 2 ** 24 - 1, 12345678))
check("F", has(0x267EC9, 0x267EE0, [(0x267EC9, ("movd", "xmm0, dword ptr [rbx + rdx*4 + 0x184]")), (0x267ED2, ("cvtdq2ps", "xmm0, xmm0")),
                                     (0x267ED5, ("movss", "dword ptr [rsp + 0x50], xmm0")), (0x267EDB, ("jmp", "0x267f1e"))])
      and not any(x.mnemonic in ("ldmxcsr", "vldmxcsr", "fldcw", "fnstcw", "stmxcsr") for x in Pf) and Pf[-1].address + Pf[-1].size == 0x267F60
      and exact and f32_bits(16777217, False) == 0x4B800000 and f32_bits(16777217, True) == 0x4B800001
      and f32_bits(-16777219, False) == 0xCB800002 and f32_bits(-16777219, True) == 0xCB800001
      and f32_bits_first_version(-16777219, True) == 0xCB800003 and f32_bits_first_version(16777217, True) == 0x4B800001,
      "kind 2, int operand: movd, cvtdq2ps, movss to +0x20 with no RC override in POPV; 16777217 -> 0x4B800000 (RN) / 0x4B800001 (RU); "
      "-16777219 -> 0xCB800002 (RN) / 0xCB800001 (RU); the sign-blind first rule would say 0xCB800003")
PH = list(cs.disasm(d[off(0x268100):off(0x2681A4)], 0x268100))
PHA = {x.address: (x.mnemonic, x.op_str) for x in PH}
def pushp(desc, index):
    w = desc >> 28
    stride = {0: 1, 1: 1, 2: 2, 3: 2, 4: 4, 5: 4}.get(w, 1)
    scaled = (index * stride) & 0xFFFFFFFF
    return (((desc & 0xFFFFFF) + scaled) & 0xFFFFFFFF) | (desc & 0x07000000) | 0x70000000
def mask24_model(desc, index): return ((pushp(desc, index) & 0xFFFFFF) | (desc & 0x07000000) | 0x70000000)
def exact7_model(desc, index): return (pushp(desc, index) & 0x0FFFFFFF) | 0x70000000
PC = {(0x02FFFFFE, 1): 0x72FFFFFF, (0x02FFFFFF, 1): 0x73000000, (0x02000000, -1): 0xFFFFFFFF, (0x42000000, -1): 0xFFFFFFFC}
tbl = [B + struct.unpack_from("<I", d, off(B + 0x1481A4) + 4 * k)[0] for k in range(6)]
check("P", PHA.get(0x268113) == ("call", "0x262440") and PHA.get(0x268118) == ("mov", "r9d, dword ptr [rsp + 0x48]") and PHA.get(0x268120) == ("mov", "edx, dword ptr [rsp + 0x4c]")
      and PHA.get(0x268124) == ("shr", "r8d, 0x1c") and PHA.get(0x26812C) == ("ja", "0x26814d") and tbl == [0x26814D, 0x26814D, 0x268142, 0x268142, 0x268146, 0x268146]
      and PHA.get(0x268142) == ("add", "edx, edx") and PHA.get(0x268146) == ("lea", "edx, [rdx*4]") and PHA.get(0x268150) == ("mov", "dword ptr [rsp + 0x30], r8d")
      and PHA.get(0x268158) == ("and", "r8d, 0xffffff") and PHA.get(0x26815F) == ("and", "r9d, 0x7000000") and PHA.get(0x268166) == ("add", "r8d, edx")
      and PHA.get(0x268169) == ("or", "r8d, r9d") and PHA.get(0x26816C) == ("or", "r8d, 0x70000000") and PHA.get(0x26817B) == ("mov", "byte ptr [rax + rbx + 4], 1")
      and PHA.get(0x268180) == ("movzx", "eax, byte ptr [rsp + 0x30]") and PHA.get(0x268185) == ("mov", "byte ptr [rcx + rbx + 0x44], al")
      and PHA.get(0x268194) == ("mov", "dword ptr [rbx + rcx*4 + 0x184], r8d")
      and not any(x.mnemonic == "and" and x.op_str.startswith("r8d") for x in PH if 0x268166 < x.address < 0x268194)
      and all(pushp(dd, ix) == v for (dd, ix), v in PC.items())
      and mask24_model(0x02FFFFFF, 1) == 0x72000000 and exact7_model(0x42000000, -1) == 0x7FFFFFFC,
      "PUSHP: descriptor18 + index1C, stride by width (table: widths 0-1 -> 0026814D x1, 2-3 -> 00268142 x2, 4-5 -> 00268146 x4), original width to +0x00 and pushed as the "
      "source kind, low32(offset + scaled) | class | 0x70000000 with no mask after the add: 02FFFFFF+1 -> 73000000, 02000000-1 -> FFFFFFFF; "
      "mask-24 (72000000) and exact-width-7 (7FFFFFFC) models rejected")
T = "ScriptVariableRef30"; REC = "_index/candidates/script-var-ref-opus/script_var_ref.py"; EXE = "exe 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
P, M, U = ("TYPE RESOLVED", "PROVEN"), ("TYPE RESOLVED", "PROBABLE"), ("DISCOVERED", "UNKNOWN")
ROWS = [(0x00, 4, "kind00", "uint32", "6, stored by the resolver 00262440 (00262667); PUSHP then overwrites it with the original width nibble (descriptor18 >> 28, 00268150) "
                                     "and pushes its low byte as the pushed value's source kind (00268180 / 00268185) (check P)", P),
        (0x04, 2, "kind04", "int16", "the value kind (check K): 2 (float) when descriptor bit 27 is set, else the resolver's r13w, 1 (integer) on the "
                                     "class routes (00262650 / 00262657); POPV reads it signed (00267E84) and converts the popped value by it before the store", P),
        (0x06, 2, "unobservedSpan06", "u8[2]", "not written by the resolver", U),
        (0x08, 2, "source08", "uint16", "the word at the resolver's second argument (00262676 / 0026267A)", P),
        (0x0A, 2, "operand0A", "uint16", "the variable operand, the resolver's r9w (0026248D) - the table index", P),
        (0x0C, 4, "tableDescriptor0C", "uint32", "the operand table entry's descriptor dword (read at 0026247C, stored at 00262492)", P),
        (0x10, 8, "address10", "void*", "the resolved base: the class base selected by descriptor bits 24..26 plus the low 24 bits (00262639..00262661); "
                                       "0026D530 and PUSHV index it", P),
        (0x18, 4, "descriptor18", "uint32", "the final descriptor; bits 28..31 select the width 0026D530 and PUSHV dispatch on (0..5; above 5 no access): "
                                            "0 u8, 1 s8, 2 u16, 3 s16, 4 / 5 dword. PUSHP (check P) reads it (00268118) and pushes the reference "
                                            "low32((d & 0xFFFFFF) + low32(index1C * stride)) | (d & 0x07000000) | 0x70000000, stride 1 / 2 / 4 for widths 0-1 / 2-3 / 4-5 "
                                            "(unscaled above 5), with no mask after the add (00268166): the class is kept and the width is 7 only while the sum stays "
                                            "below 2^24 - conditionally 02FFFFFF + 1 gives 73000000 (class 3) and 02000000 - 1 gives FFFFFFFF (class 7, width 15, bit 27 set)", P),
        (0x1C, 4, "index1C", "int32", "the element index, read sign-extended by 0026D530 and PUSHV (00262672 stores r10d). For an array (a u16 rank at the array header +4, s32 dimensions from +8) the resolver sums, last dimension first, each stage times the product of the later dimensions (check C): the stage is m = max(subscript, 0) if m < dim (signed 32-bit), else the 32-bit dim - 1 (check A) - min(max(subscript, 0), dim - 1) for strictly positive dimensions, the only case it stays in range; a zero dimension gives -1, a negative one dim - 1, and INT_MIN (0x80000000) wraps to 0x7FFFFFFF for every subscript; nothing validates the dimensions. The first popped subscript pairs with the last dimension, and the products, contributions and sum are all 32-bit (imul, imul, add; no overflow branch), so they wrap modulo 2^32 and the store reads the result signed (check L): e.g. dims 65536 x 65536 at (32768, 0) give 0x80000000, read as INT_MIN. PUSHP reads it too (00268120) and scales it by the width's stride in 32 bits (check P)", P),
        (0x20, 4, "value20", "uint32", "the value: POPV stores it before calling 0026D530 (00267F1A for kind 1; 00267EC1 / 00267ED5 / 00267EEA for kind 2), PUSHV loads the variable into it (00268008..). "
                                       "POPV converts FIRST, by kind04 (check K): kind 1 truncates a float operand with cvttss2si (1.75 -> 1; 2^31 and above, "
                                       "NaN -> 0x80000000 under masked MXCSR) and copies an int raw; kind 2 converts an int with cvtdq2ps, which rounds by the thread's MXCSR RC (POPV sets none; check F): exact "
                                       "for |n| <= 2^24, above that the mode decides (16777217 -> 16777216 under nearest-even, 16777218 under round-up; "
                                       "round-up moves toward +infinity, so -16777219 -> -16777220 under nearest-even and -16777218 under round-up - "
                                       "the values ASTRA's isolated controls record; the game's RC is not claimed); an empty stack gives 0. "
                                       "Then 0026D530 clamps the signed result by width - so a float >= 2^31 popped into a u8 variable stores 0x00: u8 [0, 255], s8 [-128, 127], u16 [0, 0xFFFF], s16 [-32767, +32768] then the low word "
                                       "(so +32768 stores 0x8000, read back signed as -32768), dword raw", P),
        (0x24, 12, "unobservedSpan24", "u8[12]", "no access by the resolver, POPV, PUSHV or 0026D530", U)]
TROW = [T, "0x30", "01-Script-VM-Native-Bridge", "a stack local of 00267E60 (POPV, rsp + 0x30) and 00267FC0 (PUSHV, rbp - 0x30); one per variable access",
        "STACK - the callers' frames bound it to 0x30", "none - 00262440 fills it (its fifth argument)", "none", P[0], P[1], "L1",
        "CARVED 2026-09-28 (OPUS, %s S R), for ASTRA-REQ-OPUS-SCRIPT-STORE-SATURATION. %s" % (REC, EXE),
        "01-Script-VM-Native-Bridge/Interpreter-Core/script-variables-and-their-storage-classes.md", "DYNAMIC - a stack local passed as 00262440's fifth argument"]
FI = os.path.join(DB, "_types", "fields.tsv"); TY = os.path.join(DB, "_types", "types.tsv")
def cells(l): return l.rstrip("\r\n").split("\t")
if "--patch" in sys.argv:
    fl = open(FI, "rb").read().decode("utf-8").splitlines(keepends=True); e = fl[1][len(fl[1].rstrip("\r\n")):]
    if not any(cells(l)[0] == T for l in fl):
        fl += ["\t".join([T, "0x%02X" % o, str(n), nm, ct, m, rd[0], rd[1], "CARVED 2026-09-28 (OPUS, %s S R). %s" % (REC, EXE)]) + e for o, n, nm, ct, m, rd in ROWS]
    for nm_old, nm_new in (("count04", "kind04"), ("value20", "value20")):
        new = next(r for r in ROWS if r[2] == nm_new)
        for i_, l in enumerate(fl):
            c = cells(l); ee = l[len(l.rstrip("\r\n")):]
            if c[0] == T and c[3] == nm_old and "(check K)" not in c[5]:
                was = "%s: %s" % (c[3], c[5]); c[3] = nm_new; c[5] = new[4]
                c[8] += " || CORRECTED 2026-09-28 (OPUS, %s K, ASTRA-REQ-OPUS-SCRIPT-POPV-CONVERSION). was %s" % (REC, was); fl[i_] = "\t".join(c) + ee
    v20 = next(r for r in ROWS if r[2] == "value20")
    for i_, l in enumerate(fl):
        c = cells(l); ee = l[len(l.rstrip("\r\n")):]
        if c[0] == T and c[3] == "value20" and "(check K)" in c[5] and c[5] != v20[4]:
            c[5] = v20[4]
            if "ASTRA-REQ-OPUS-SCRIPT-FLOAT-ROUNDING" not in c[8]:
                c[8] += " || QUALIFIED 2026-09-28 (OPUS, %s F, for ASTRA-REQ-OPUS-SCRIPT-FLOAT-ROUNDING): cvtdq2ps rounds by MXCSR RC; kind 2's own +0x20 stores cited" % REC
            fl[i_] = "\t".join(c) + ee
    for nm, tag, note in (("kind00", "check P", "PUSHP overwrites +0x00 with the original width and pushes it as the source kind"),
                          ("descriptor18", "check P", "PUSHP's packing and its offset domain"),
                          ("value20", "-16777219", "the sign rule of round-up"),
                          ("index1C", "check P", "PUSHP also reads and scales it")):
        new = next(r for r in ROWS if r[2] == nm)
        for i_, l in enumerate(fl):
            c = cells(l); ee = l[len(l.rstrip("\r\n")):]
            if c[0] == T and c[3] == nm and tag not in c[5] and ("(check C)" in c[5] or nm != "index1C"):
                c[5] = new[4]; c[8] += " || QUALIFIED 2026-09-28 (OPUS, %s %s, for %s): %s" % (
                    REC, "F" if nm == "value20" else "P",
                    "ASTRA-REQ-OPUS-SCRIPT-NEGATIVE-ROUNDING" if nm == "value20" else "ASTRA-REQ-OPUS-SCRIPT-REFERENCE-CARRY", note)
                fl[i_] = "\t".join(c) + ee
    idx = next(r for r in ROWS if r[2] == "index1C")
    for i_, l in enumerate(fl):
        c = cells(l); ee = l[len(l.rstrip("\r\n")):]
        if c[0] == T and c[3] == "index1C" and "(check A)" in c[5] and "(check L)" not in c[5]:
            c[5] = idx[4]; c[8] += " || QUALIFIED 2026-09-28 (OPUS, %s L, for ASTRA-REQ-OPUS-SCRIPT-ARRAY-FLATTEN): the flatten is 32-bit, wraps modulo 2^32, read back signed" % REC
            fl[i_] = "\t".join(c) + ee; continue
        if c[0] == T and c[3] == "index1C" and "(check A)" not in c[5]:
            if "(check C)" in c[5]:
                c[5] = idx[4]; c[8] += " || CORRECTED 2026-09-28 (OPUS, %s A, for ASTRA-REQ-OPUS-SCRIPT-ARRAY-SIGNEDMIN): the compare is against dim and the fallback the 32-bit dim - 1, so INT_MIN gives 0x7FFFFFFF, not the unbounded min formula" % REC
                fl[i_] = "\t".join(c) + ee; continue
            c[5] = idx[4]; c[8] += " || QUALIFIED 2026-09-28 (OPUS, %s C, for ASTRA-REQ-OPUS-SCRIPT-ARRAY-CLAMP): the clamp holds only for strictly positive dimensions" % REC
            fl[i_] = "\t".join(c) + ee
    open(FI, "wb").write("".join(fl).encode("utf-8"))
    tl = open(TY, "rb").read().decode("utf-8").splitlines(keepends=True); te = tl[1][len(tl[1].rstrip("\r\n")):]
    if not any(cells(l)[0] == T for l in tl): tl.append("\t".join(TROW) + te)
    open(TY, "wb").write("".join(tl).encode("utf-8")); print("patched"); sys.exit(0)
F = [cells(l) for l in open(FI, "rb").read().decode("utf-8").splitlines() if cells(l)[0] == T]
Tt = [cells(l) for l in open(TY, "rb").read().decode("utf-8").splitlines() if cells(l)[0] == T]
check("W", len(Tt) == 1 and sum(int(c[2]) for c in F) == 0x30 and len(F) == len(ROWS) and any(c[3] == "index1C" and "(check C)" in c[5] and "0x7FFFFFFF" in c[5] and "(check L)" in c[5] for c in F) and any(c[3] == "kind04" for c in F) and not any(c[3] == "count04" for c in F)
      and any(c[3] == "value20" and "MXCSR RC" in c[5] and "check F" in c[5] and "-16777219" in c[5] for c in F)
      and any(c[3] == "kind00" and "check P" in c[5] for c in F) and any(c[3] == "descriptor18" and "below 2^24" in c[5] for c in F)
      and any(c[3] == "index1C" and "check P" in c[5] for c in F),
      "ScriptVariableRef30 is in the store, tiles 0x30, index1C states the clamp's positive-dimension condition, value20 the RC dependence")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
