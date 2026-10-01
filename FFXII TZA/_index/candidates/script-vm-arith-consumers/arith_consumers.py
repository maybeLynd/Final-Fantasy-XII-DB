"""arith_consumers.py - the ScriptVM's compare, divide, array-flatten and reference-packing arithmetic, read from the certified
image for the canonical pages that consume it (FABLE, Claude Opus 5.5, 2026-09-28). STATIC: nothing here executes game code.
The small models below are executable specifications of what the bytes do; their example values are calculations, not
observations of any shipped script, and not native or live behaviour.

Consumes (re-derived here, not copied): ASTRA's packages 74 script-array-flatten-width, 76 script-reference-offset-carry,
77 script-comparison-unordered, 78 script-comparison-mixed-precision, 79 script-division-unordered-guard, 80
script-integer-divide-overflow; OPUS's script-comparator-opus and script-var-ref-opus records.

  C  COMPARATOR 0025D740 and its six consumers. Integer fast path only when depth >= 2 and both top tags are 1 (0025D754,
     0025D7B8, 0025D7BD); every other pair goes through the float path, an int converted with cvtdq2ps (0025D8A6). The float
     path: ucomiss xmm6, xmm7 / jp / jne, so an unordered pair never reaches the equal return; then or eax, -1 / comiss xmm7,
     xmm6 / cmova edi, eax with edi = 1: -1 only when right > left (ordered), +1 otherwise, including every NaN. OPEQ..OPLSE
     (0025EA18 + 0x18 i) test eax and set cl with sete / setne / setg / sets / setns / setle.
     The integer path's inlined pops carry float arms (cvttss2si at 0025D813 / 0025D827), but that path is entered only after
     both tags compared equal to 1 (0025D7BD / 0025D7C0 jne 0025D760), so those arms are not reached from it: a mixed pair is
     never truncated to int, its int side is converted to float (cvtdq2ps 0025D869 / 0025D8A6).
     Model: with a NaN operand EQ 0, NE 1, GT 1, LS 0, GTE 1, LSE 0; int 1 vs float 1.5 -> -1. Rejected: host IEEE operators
     (NaN > x is false); truncating the float side (1 vs trunc(1.5) = 1 -> 0).
  D  OPDIV float path (0025F0E3..0025F1D1). The top pops into xmm6 (the divisor), the next into xmm0 (the dividend); xmm7 is
     the interpreter's zero (xorps xmm7, xmm7 at 0025E55F). ucomiss xmm6, xmm7 / jp / jne -> divss xmm0, xmm6; only an ordered
     equal-to-zero divisor (+0 or -0) takes movaps xmm0, xmm7. Result pushed as a float (tag 2).
     Model: lower / top; divisor +-0 -> +0.0; NaN divisor -> divides (NaN). Rejected: a zero guard that also catches NaN
     (drops the jp), and top / lower (reversed operands).
  I  OPDIV integer path (0025F0AC..0025F0DE), taken when 00267560 says depth >= 2 and both top tags are 1. First pop -> ebx
     (divisor), second -> eax (dividend); test ebx, ebx / je 0025E682 (which pushes int 0); then cdq / idiv ebx with nothing
     between the je and the idiv. So INT_MIN / -1 reaches idiv, whose quotient 2^31 does not fit: the CPU raises a divide
     error at 0025F0DA. Model: 20 / 3 = 6, -20 / 3 = -6 (truncation), x / 0 = 0, INT_MIN / -1 = fault. Rejected: wrap to
     INT_MIN, saturate to INT_MAX. What the process does after the fault (handler, crash) is not read here.
  F  ARRAY FLATTEN in the resolver 00262440. Sum 0 (ebx, 0026245D / 00262474), product 1 (00262478 / 002624AD); the walk
     starts at the LAST dimension (002624CD lea rbp, [rbp + r13*4], r13 = count - 1) and pops one index per dimension;
     imul eax, r8d / imul r8d, esi / add r10d, eax (0026251F..00262527) are 32-bit; the sum is stored as a dword at record
     +0x1C (00262672), and the store helper reads it sign-extended (0026D537 movsxd rcx, dword [rcx + 0x1C]).
     Model: flat = low32(sum clamp(idx_i) * prod_{j > i} dim_j), read as signed. dims (2, 3), indices (1, 0) -> 3;
     dims (65536, 65536), indices (32768, 0) -> 0x80000000 = INT_MIN as the signed index. Rejected: first-dimension-fastest
     (gives 1), unbounded 64-bit (gives +2147483648).
  R  PUSHP 00268100 packing. edx = the flat index (record +0x1C) scaled x1 / x2 / x4 by width (00268142 add edx, edx;
     00268146 lea edx, [rdx*4]); then and r8d, 0xFFFFFF / and r9d, 0x7000000 / add r8d, edx / or r8d, r9d / or r8d,
     0x70000000 (00268158..0026816C), and r8d is stored at 00268194 with no mask in between. The byte stored at +0x44 is the
     ORIGINAL width (shr 0x1C at 00268124), separate from the packed word.
     Model: packed = ((desc & 0xFFFFFF) + scaled) | (desc & 0x07000000) | 0x70000000, in 32 bits. The class is preserved and
     the width is 7 only while 0 <= (desc & 0xFFFFFF) + scaled <= 0xFFFFFF. Examples: 02FFFFFE + 1 -> 72FFFFFF (class 2,
     width 7); 02FFFFFF + 1 -> 73000000 (class 3); 02000000 + -1 -> FFFFFFFF (class 7, width 15). Rejected: a final 24-bit
     mask (would give 72000000), an exact width replacement (would give 7xxxxxxx always).
  M  OPMOD (0025F1D6): pops top -> ebx, lower -> eax, then cdq / idiv ebx with no test or branch before it and pushes the
     remainder (edx). So MOD 0 and INT_MIN MOD -1 both fault at 0025F1F4. Model: 7 % 3 = 1, -7 % 3 = -1.
  Negative scans (C's "no jump into the int path", I's "only cdq between", R's "no r8d write", M's "no test") count only when
  the decode covers their span contiguously (covered()); `--truncate` cuts every listing in half and they must FAIL.
  Not claimed: game MXCSR, native exception policy or handler, authored values, which scripts divide, compare NaNs, build
  arrays or pass references of these sizes, reachability, or live behaviour.
Usage: python arith_consumers.py   (exit 1 on any FAIL; refuses an image that is not the certified one)
"""
import hashlib, math, os, struct, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

HERE = os.path.dirname(os.path.abspath(__file__))
EXE = os.path.join(HERE, "..", "..", "..", "..", "Tools", "work", "exe", "FFXII_TZA.exe")
d = open(EXE, "rb").read()
if hashlib.sha256(d).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8":
    print("REFUSED  not the certified image"); sys.exit(2)
B = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in SECS:
        if B + va <= v < B + va + rs: return v - B - va + ro
    raise ValueError("%08X not in a section" % v)
cs = Cs(CS_ARCH_X86, CS_MODE_64)
SIZES = {}
def dis(a, b):
    out = {}
    for x in cs.disasm(d[off(a):off(b)], a):
        out[x.address] = ("%s %s" % (x.mnemonic, x.op_str)).strip(); SIZES[x.address] = x.size
    return out
def covered(code, lo, hi):
    """a NEGATIVE scan over [lo, hi) is evidence only if the decode covers that span contiguously: capstone stops at the
    first undecodable byte, and a scan over a truncated listing finds nothing and would pass (ASTRA 84's cutoff control)"""
    a = lo
    while a < hi:
        if a not in code: return False
        a += SIZES[a]
    return True
if "--truncate" in sys.argv:          # self-test: cut every listing short; each negative-scan check must then FAIL
    _dis = dis
    def dis(a, b): c = _dis(a, b); return {k: v for k, v in c.items() if k < a + (b - a) // 2}
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
def at(code, want): return all(code.get(a) == s for a, s in want.items())

# ---- C: comparator ----------------------------------------------------------------------------------------------
cmpc = dis(0x25D740, 0x25D8DD)
C_BYTES = {0x25D74F: "mov edi, 1", 0x25D754: "cmp edx, 2", 0x25D757: "jge 0x25d7a1", 0x25D7B8: "cmp r8d, eax",
           0x25D7BD: "cmp r8d, edi", 0x25D8A6: "cvtdq2ps xmm6, xmm6", 0x25D8B2: "ucomiss xmm6, xmm7", 0x25D8B5: "jp 0x25d8d0",
           0x25D8B7: "jne 0x25d8d0", 0x25D8B9: "xor eax, eax", 0x25D8D0: "or eax, 0xffffffff", 0x25D8D3: "comiss xmm7, xmm6",
           0x25D8D6: "cmova edi, eax", 0x25D8D9: "mov eax, edi", 0x25D7C0: "jne 0x25d760", 0x25D869: "cvtdq2ps xmm7, xmm7",
           0x25D813: "cvttss2si ebp, dword ptr [rbx + rdx*4 + 0x184]", 0x25D827: "cvttss2si esi, dword ptr [rbx + rdx*4 + 0x184]",
           0x25D857: "cmp esi, ebp", 0x25D859: "cmovl edi, eax"}
# the only jumps into the integer path's pop arms come from inside it (0025D7C2..0025D838), which is entered only past 0025D7C0
into_int = [a for a, s in cmpc.items() if s.split(" ")[0].startswith("j") and s.split(" ")[-1].startswith("0x")
            and 0x25D7C2 <= int(s.split(" ")[-1], 16) < 0x25D839 and not 0x25D7C2 <= a < 0x25D839]
SETS = ["sete", "setne", "setg", "sets", "setns", "setle"]
cons = []
for i, s in enumerate(SETS):
    a = 0x25EA18 + 0x18 * i; c = dis(a, a + 0x18); v = list(c.values())
    cons.append(v[1] == "call 0x25d740" and "test eax, eax" in v and ("%s cl" % s) in v)
def cmp3(left, right):
    """the float path of 0025D740: 0 equal; +1 on any NaN; -1 only when right > left"""
    if not (math.isnan(left) or math.isnan(right)) and left == right: return 0
    return -1 if (not math.isnan(left) and not math.isnan(right) and right > left) else 1
DEC = {"EQ": lambda r: r == 0, "NE": lambda r: r != 0, "GT": lambda r: r > 0, "LS": lambda r: r < 0, "GTE": lambda r: r >= 0, "LSE": lambda r: r <= 0}
nan = float("nan")
fin = (cmp3(1, 2), cmp3(1, 1), cmp3(2, 1))
nanres = {k: int(f(cmp3(nan, 1.0))) for k, f in DEC.items()}
host = {"GT": int(nan > 1.0), "GTE": int(nan >= 1.0)}
mixed, trunc = cmp3(1.0, 1.5), (0 if 1 == int(1.5) else 1)
check("C", at(cmpc, C_BYTES) and cons == [True] * 6 and fin == (-1, 0, 1) and (cmp3(1, nan), cmp3(nan, nan)) == (1, 1)
      and nanres == {"EQ": 0, "NE": 1, "GT": 1, "LS": 0, "GTE": 1, "LSE": 0} and host == {"GT": 0, "GTE": 0}
      and into_int == [] and covered(cmpc, 0x25D740, 0x25D8DD) and mixed == -1 and trunc == 0,
      "0025D740 anchors %s; consumers 0A..0F %s; finite %s; NaN decisions %s; host IEEE GT/GTE on NaN %s (rejected); "
      "jumps into the int path from outside it %s; int 1 vs float 1.5 -> %d, truncating model -> %d (rejected)"
      % (at(cmpc, C_BYTES), cons, fin, nanres, host, ["%08X" % a for a in into_int], mixed, trunc))

# ---- D / I: OPDIV --------------------------------------------------------------------------------------------------
div = dis(0x25F0AC, 0x25F1D6); ent = dis(0x25E550, 0x25E567); zero = dis(0x25E682, 0x25E6C2); both = dis(0x267560, 0x2675B5)
D_BYTES = {0x25F111: "movss xmm6, dword ptr [r10 + rdx*4 + 0x184]", 0x25F127: "cvtdq2ps xmm6, xmm6",
           0x25F164: "movss xmm0, dword ptr [r10 + rdx*4 + 0x184]", 0x25F17A: "cvtdq2ps xmm0, xmm0",
           0x25F197: "ucomiss xmm6, xmm7", 0x25F19A: "jp 0x25f1a3", 0x25F19C: "jne 0x25f1a3", 0x25F19E: "movaps xmm0, xmm7",
           0x25F1A3: "divss xmm0, xmm6", 0x25F1B3: "mov byte ptr [rax + r10 + 4], 2"}
E_BYTES = {0x25E555: "mov ebp, 1", 0x25E55F: "xorps xmm7, xmm7"}
def fdiv(lower, top):
    """OPDIV float path: an ordered divisor equal to 0 gives +0.0 (xmm7); anything else, NaN included, divides"""
    if not math.isnan(top) and top == 0.0: return 0.0
    if math.isnan(top) or math.isnan(lower): return nan
    return lower / top if top != 0 else math.copysign(math.inf, lower)
def fdiv_nan_is_zero(lower, top): return 0.0 if (math.isnan(top) or top == 0.0) else lower / top
dres = (fdiv(6.0, 3.0), fdiv(6.0, 0.0), fdiv(6.0, -0.0), math.isnan(fdiv(6.0, nan)))
check("D", at(div, D_BYTES) and at(ent, E_BYTES) and dres == (2.0, 0.0, 0.0, True)
      and fdiv_nan_is_zero(6.0, nan) == 0.0 and fdiv(3.0, 6.0) != fdiv(6.0, 3.0),
      "anchors %s, entry ebp = 1 / xmm7 = 0 %s; model 6/3, 6/0, 6/-0, 6/NaN -> %s; rejected: NaN-as-zero gives 0.0 for 6/NaN, "
      "reversed operands give %s for 6/3" % (at(div, D_BYTES), at(ent, E_BYTES), dres, fdiv(3.0, 6.0)))
I_BYTES = {0x25F0AF: "call 0x267560", 0x25F0B6: "je 0x25f0e3", 0x25F0C2: "call 0x267e10", 0x25F0CA: "mov ebx, eax",
           0x25F0CC: "call 0x267e10", 0x25F0D1: "test ebx, ebx", 0x25F0D3: "je 0x25e682", 0x25F0D9: "cdq", 0x25F0DA: "idiv ebx",
           0x25F0DC: "mov ecx, eax"}
between = [a for a in div if 0x25F0D3 < a < 0x25F0DA]
Z_BYTES = {0x25E682: "xor r11d, r11d", 0x25E685: "mov ecx, r11d", 0x25E6BA: "mov dword ptr [r10 + r9*4 + 0x184], ecx"}
BOTH = {0x26756E: "cmp r8d, 2", 0x26759D: "cmp r9d, ecx", 0x2675A2: "mov eax, 1", 0x2675A7: "cmp r9d, eax", 0x2675AA: "cmove ebx, eax"}
INT_MIN = -2 ** 31
def idiv(lower, top):
    """OPDIV integer path: 0 for a zero divisor, else x86 idiv (truncating); a quotient outside int32 is a divide error"""
    if top == 0: return 0
    q = abs(lower) // abs(top) * (1 if (lower < 0) == (top < 0) else -1)
    if not INT_MIN <= q < 2 ** 31: return "FAULT"
    return q
ires = (idiv(20, 3), idiv(-20, 3), idiv(INT_MIN, 1), idiv(7, 0), idiv(INT_MIN, -1))
check("I", at(div, I_BYTES) and between == [0x25F0D9] and covered(div, 0x25F0D3, 0x25F0DC) and at(zero, Z_BYTES) and at(both, BOTH)
      and ires == (6, -6, INT_MIN, 0, "FAULT"),
      "anchors %s, only cdq between the zero test and idiv %s, zero -> push int 0 %s, both-int test %s; model 20/3, -20/3, "
      "MIN/1, 7/0, MIN/-1 -> %s; rejected: wrap (MIN) and saturate (MAX) for MIN/-1"
      % (at(div, I_BYTES), between == [0x25F0D9], at(zero, Z_BYTES), at(both, BOTH), ires))

# ---- F: flatten -------------------------------------------------------------------------------------------------
res = dis(0x262440, 0x262690); st = dis(0x26D530, 0x26D548)
F_BYTES = {0x26245D: "xor ebx, ebx", 0x262474: "mov dword ptr [rsp + 0x78], ebx", 0x262478: "lea r13d, [rbx + 1]",
           0x2624AD: "mov r8d, r13d", 0x2624BA: "sub eax, r13d", 0x2624CD: "lea rbp, [rbp + r13*4]",
           0x262510: "cmovns ecx, eax", 0x262513: "lea eax, [rsi - 1]", 0x262518: "cmovl eax, ecx", 0x26251B: "sub rbp, 4",
           0x26251F: "imul eax, r8d", 0x262523: "imul r8d, esi", 0x262527: "add r10d, eax", 0x262537: "jns 0x2624d2",
           0x262672: "mov dword ptr [r15 + 0x1c], r10d"}
S_BYTES = {0x26D537: "movsxd rcx, dword ptr [rcx + 0x1c]"}
def s32(x): x &= 0xFFFFFFFF; return x - 2 ** 32 if x & 0x80000000 else x
def flat(dims, idx, bits=32, last_first=True):
    """row-major flatten as the resolver walks it: last dimension first, product and sum kept to `bits`"""
    m = (1 << bits) - 1; s, p = 0, 1
    order = range(len(dims) - 1, -1, -1) if last_first else range(len(dims))
    for i in order:
        c = min(max(idx[i], 0), dims[i] - 1)
        s = (s + c * p) & m; p = (p * dims[i]) & m
    return s32(s) if bits == 32 else s
fres = (flat((2, 3), (1, 0)), flat((65536, 65536), (32768, 0)), flat((65536, 65536), (65535, 65535)))
check("F", at(res, F_BYTES) and at(st, S_BYTES) and fres == (3, INT_MIN, -1)
      and flat((2, 3), (1, 0), last_first=False) == 1 and flat((65536, 65536), (32768, 0), bits=64) == 2 ** 31,
      "anchors %s, store helper sign-extends +0x1C %s; model (2,3)[1,0], (65536,65536)[32768,0], [65535,65535] -> %s; rejected: "
      "first-dimension-fastest gives 1, 64-bit gives 2^31" % (at(res, F_BYTES), at(st, S_BYTES), fres))

# ---- R: PUSHP -----------------------------------------------------------------------------------------------------
pp = dis(0x268100, 0x2681A4)
R_BYTES = {0x268113: "call 0x262440", 0x268118: "mov r9d, dword ptr [rsp + 0x48]", 0x268120: "mov edx, dword ptr [rsp + 0x4c]",
           0x268124: "shr r8d, 0x1c", 0x268142: "add edx, edx", 0x268146: "lea edx, [rdx*4]", 0x268158: "and r8d, 0xffffff",
           0x26815F: "and r9d, 0x7000000", 0x268166: "add r8d, edx", 0x268169: "or r8d, r9d", 0x26816C: "or r8d, 0x70000000",
           0x268185: "mov byte ptr [rcx + rbx + 0x44], al", 0x268194: "mov dword ptr [rbx + rcx*4 + 0x184], r8d"}
r8_writes = [a for a, s in pp.items() if 0x26816C < a < 0x268194 and s.split(" ")[1:2] in (["r8d,"], ["r8,"])]
def pack(desc, scaled): return ((((desc & 0xFFFFFF) + scaled) & 0xFFFFFFFF) | (desc & 0x07000000) | 0x70000000) & 0xFFFFFFFF
def fields(w): return ((w >> 24) & 7, w >> 28)
rres = [pack(0x02FFFFFE, 1), pack(0x02FFFFFF, 1), pack(0x02000000, -1)]
masked = ((0x02FFFFFF + 1) & 0xFFFFFF) | 0x02000000 | 0x70000000
check("R", at(pp, R_BYTES) and not r8_writes and covered(pp, 0x26816C, 0x268194) and rres == [0x72FFFFFF, 0x73000000, 0xFFFFFFFF]
      and [fields(w) for w in rres] == [(2, 7), (3, 7), (7, 15)] and masked == 0x72000000 and masked != rres[1],
      "anchors %s, no r8d write between the width OR and the store %s; model 02FFFFFE+1, 02FFFFFF+1, 02000000-1 -> %s "
      "(class, width) %s; rejected: a final 24-bit mask gives %08X" % (at(pp, R_BYTES), not r8_writes,
      ["%08X" % w for w in rres], [fields(w) for w in rres], masked))
# ---- M: OPMOD ----------------------------------------------------------------------------------------------------
md = dis(0x25F1D6, 0x25F226)
M_BYTES = {0x25F1D9: "call 0x267e10", 0x25F1E5: "mov ebx, eax", 0x25F1E7: "call 0x267e10", 0x25F1F3: "cdq", 0x25F1F4: "idiv ebx",
           0x25F219: "mov dword ptr [r10 + r9*4 + 0x184], edx"}
tests = [a for a, s_ in md.items() if 0x25F1D6 <= a < 0x25F1F4 and s_.split(" ")[0] in ("test", "cmp", "je", "jne", "jz", "jnz")]
def imod(lower, top):
    """OPMOD: no test at all; idiv faults on a zero divisor and on INT_MIN / -1; else the remainder (sign of the dividend)"""
    if top == 0: return "FAULT"
    q = abs(lower) // abs(top) * (1 if (lower < 0) == (top < 0) else -1)
    if not INT_MIN <= q < 2 ** 31: return "FAULT"
    return lower - q * top
mres = (imod(7, 3), imod(-7, 3), imod(7, 0), imod(INT_MIN, -1))
check("M", at(md, M_BYTES) and tests == [] and covered(md, 0x25F1D6, 0x25F1F6) and mres == (1, -1, "FAULT", "FAULT"),
      "OPMOD anchors %s; no test or branch before the idiv %s; model 7%%3, -7%%3, 7%%0, MIN%%-1 -> %s" % (at(md, M_BYTES), tests == [], mres))
# ---- U: underflow and bad tags (PKG-TECH-SCRIPTVM-VALUE T4, 2026-09-29) -------------------------------------------
pop = dis(0x267E10, 0x267E5E); rs = dis(0x2624D2, 0x262510); cm = dis(0x25D760, 0x25D878); bail = dis(0x8620C0, 0x8620CE)
U_OK = (at(pop, {0x267E1A: "dec eax", 0x267E1F: "mov dword ptr [rcx], eax", 0x267E21: "movzx edx, byte ptr [r8 + rcx + 4]",
                 0x267E36: "call 0x8620c0", 0x267E3B: "xor eax, eax"})
        and at(rs, {0x2624DC: "dec eax", 0x2624E1: "mov dword ptr [r14], eax", 0x2624E4: "movzx ecx, byte ptr [rdx + r14 + 4]"})
        and at(cm, {0x25D767: "xorps xmm6, xmm6", 0x25D77C: "mov dword ptr [rbx], eax", 0x25D875: "movaps xmm7, xmm6"})
        and at(bail, {0x8620C7: "xor ecx, ecx", 0x8620C9: "jmp 0x16d6a0"}) and d[off(0x16D6A0):off(0x16D6A0) + 3] == bytes([0xC2, 0, 0]))
check("U", U_OK, "each pop stores the decremented count before its tag test (00267E1F, 002624E1, 0025D77C); a bad tag reads int 0 "
      "(00267E3B) or float 0.0 in the comparator (0025D875 from 0025D767); 008620C0 tail-jumps to 0016D6A0 = C2 00 00 (ret 0): %s" % U_OK)
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
