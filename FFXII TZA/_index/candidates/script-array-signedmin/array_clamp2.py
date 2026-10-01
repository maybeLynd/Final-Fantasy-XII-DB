"""array_clamp2.py - the script VM's array index clamp in 32-bit arithmetic: dim - 1 wraps at INT_MIN (FABLE, Claude Opus 5.5,
2026-09-28, on ASTRA-REQ-FABLE-SCRIPT-ARRAY-SIGNEDMIN). Supersedes ../script-array-clamp/array_clamp.py's clamp() for negative dimensions; that file and
its output stay as they were. Decoded from the certified image; the six clamp instructions are interpreted, nothing native executed.

  K1 as array_clamp.py: ebx = 0 (0026245D); the index reaches 0026250C in eax from the int pop (0026257D), the float pop
     (00262571, cvttss2si) or ebx's 0 on an empty stack (002624DA); the dimension is a 32-bit load into esi (002624D5), which
     zero-extends into rsi
  K2 0026250C..00262518 are exactly 'test eax, eax / mov ecx, ebx / cmovns ecx, eax / lea eax, [rsi - 1] / cmp ecx, esi /
     cmovl eax, ecx'; an interpreter for those six decoded strings, with 32-bit registers and flags, is the model
  K3 the interpreter equals index' = ecx if ecx < dim (signed 32-bit) else signed32(low32(dim - 1)), with ecx = max(index, 0),
     on a grid of indices {INT_MIN, -1, 0, 1, 5, INT_MAX} x dimensions {INT_MIN, INT_MIN + 1, -2, 0, 1, 3, INT_MAX}
  K4 the boundary: at dim = INT_MIN (80000000) 'lea eax, [rsi - 1]' gives 7FFFFFFF, and since ecx >= 0 is never below INT_MIN the
     cmovl is not taken - index' = +2147483647 for every index; at INT_MIN + 1 dim - 1 = INT_MIN does not wrap
  K5 the earlier results stand: dim 3 clamps into [0, 2]; dim 0 gives -1; dim -2 gives -3
  C1 control, sensitive to the defect: array_clamp.py's clamp() (unbounded Python dim - 1) agrees with the interpreter on every
     grid cell except the dim = INT_MIN row, where it gives -2147483649
  C2 control: the interpreter with the dimension sign-extended and the subtraction left unbounded (as if movsxd + a 64-bit
     result) reproduces C1's wrong value; the image's 32-bit load zero-extends and its 32-bit lea keeps only the low dword, so
     K4 comes from those widths
  C3 control: with 'cmovle' in place of 'cmovl' dim 3 admits index 3 - one past the end - so the strict compare is the image's
  Not claimed: whether any shipped array has a dimension <= 0 or INT_MIN, upstream validation, the flatten product or its
  overflow, a storage fault, or any live array
"""
import hashlib, os, struct, sys
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
B = {i.address: (i.mnemonic + " " + i.op_str).strip() for i in MD.disasm(d[off(0x262440):off(0x262440) + 591], 0x262440)}
ok("K1", B[0x26245D] == "xor ebx, ebx" and B[0x2624D5] == "mov esi, dword ptr [rbp]" and B[0x2624DA] == "jle 0x26250a" and B[0x26250A] == "mov eax, ebx"
   and B[0x26257D] == "mov eax, dword ptr [r14 + rdx*4 + 0x184]" and B[0x262585] == "jmp 0x26250c"
   and B[0x262571].startswith("cvttss2si eax") and B[0x26257B] == "jmp 0x26250c",
   "ebx = 0; index in eax from the int or float pop paths (or 0 on an empty stack); dimension a 32-bit load into esi")
ADDRS = (0x26250C, 0x26250E, 0x262510, 0x262513, 0x262516, 0x262518)
SEQ = [B[a] for a in ADDRS]
ok("K2", SEQ == ["test eax, eax", "mov ecx, ebx", "cmovns ecx, eax", "lea eax, [rsi - 1]", "cmp ecx, esi", "cmovl eax, ecx"],
   "the six decoded instructions: %s" % " / ".join(SEQ))
M32 = 0xFFFFFFFF
s32 = lambda u: u - (1 << 32) if u & 0x80000000 else u
INT_MIN, INT_MAX = -2 ** 31, 2 ** 31 - 1
def run(seq, index, dim, lea64=False):
    """interpret the decoded strings: 32-bit eax/ebx/ecx/esi, rsi = zero-extended esi; SF/OF as x86 sets them."""
    r = {"eax": index & M32, "ebx": 0, "ecx": 0, "esi": dim & M32}
    sf = of = zf = 0
    for s in seq:
        m, ops = s.split(None, 1); a = [p.strip() for p in ops.split(",")]
        if m == "test":
            v = r[a[0]] & r[a[1]]; sf, of = v >> 31, 0
        elif m == "mov":
            r[a[0]] = r[a[1]]
        elif m == "cmovns":
            r[a[0]] = r[a[1]] if not sf else r[a[0]]
        elif m == "lea":
            assert a[1] == "[rsi - 1]", a
            if not lea64: r[a[0]] = (r["esi"] - 1) & M32           # rsi is esi zero-extended; eax keeps the low 32 bits
            else: r[a[0]] = s32(r["esi"]) - 1                     # control C2: a sign-extended dimension, unbounded result
        elif m == "cmp":
            x, y = s32(r[a[0]]), s32(r[a[1]]); t = x - y
            sf = (t & M32) >> 31; of = int(not (INT_MIN <= t <= INT_MAX)); zf = int(t == 0)
        elif m in ("cmovl", "cmovle"):                             # cmovl: SF != OF; cmovle: ZF or SF != OF
            take = (sf != of) or (m == "cmovle" and zf)
            r[a[0]] = r[a[1]] if take else r[a[0]]
        else:
            raise ValueError(s)
    return r["eax"] if r["eax"] < 0 else s32(r["eax"])            # only the lea64 control leaves a negative Python int
def formula(index, dim):
    ecx = max(index, 0)
    return ecx if ecx < dim else s32((dim - 1) & M32)
def clamp_v1(i, dim, le=False):                                   # array_clamp.py's clamp(), verbatim
    ecx = i if i >= 0 else 0
    return ecx if (ecx <= dim if le else ecx < dim) else dim - 1
IDX = (INT_MIN, -1, 0, 1, 5, INT_MAX)
DIMS = (INT_MIN, INT_MIN + 1, -2, 0, 1, 3, INT_MAX)
grid = {(i, dm): run(SEQ, i, dm) for i in IDX for dm in DIMS}
ok("K3", all(grid[k] == formula(*k) for k in grid), "interpreter == signed32(low32(dim - 1)) formula on all %d cells" % len(grid))
row_min = {i: grid[(i, INT_MIN)] for i in IDX}
ok("K4", set(row_min.values()) == {INT_MAX} and run(["lea eax, [rsi - 1]"], 0, INT_MIN) == INT_MAX
   and {grid[(i, INT_MIN + 1)] for i in IDX} == {INT_MIN},
   "dim INT_MIN -> index' %s for every index; dim INT_MIN + 1 -> %d" % (sorted(set(row_min.values())), grid[(0, INT_MIN + 1)]))
k5 = {(5, 3): grid[(5, 3)], (-1, 3): grid[(-1, 3)], (1, 3): grid[(1, 3)], (0, 0): grid[(0, 0)], (5, 0): grid[(5, 0)], (1, -2): grid[(1, -2)]}
ok("K5", k5 == {(5, 3): 2, (-1, 3): 0, (1, 3): 1, (0, 0): -1, (5, 0): -1, (1, -2): -3}, "earlier cases unchanged: %s" % k5)
diff = sorted({dm for (i, dm) in grid if clamp_v1(i, dm) != grid[(i, dm)]})
ok("C1", diff == [INT_MIN] and clamp_v1(0, INT_MIN) == -2147483649,
   "array_clamp.py's clamp() differs only on dimension(s) %s, giving %d there" % (diff, clamp_v1(0, INT_MIN)))
ok("C2", run(SEQ, 0, INT_MIN, lea64=True) == -2147483649, "a sign-extended, unbounded dim - 1 gives %d at dim INT_MIN" % run(SEQ, 0, INT_MIN, lea64=True))
le = [s.replace("cmovl ", "cmovle ") for s in SEQ]
ok("C3", run(le, 3, 3) == 3 and run(SEQ, 3, 3) == 2, "a cmovle sequence admits index 3 for dim 3; the image's cmovl gives 2")
print("FAILS", fails); sys.exit(1 if fails else 0)
