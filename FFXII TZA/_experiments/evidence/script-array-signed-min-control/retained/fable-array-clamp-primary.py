"""array_clamp.py - the script VM's array index clamp holds only for a positive dimension (FABLE, Claude Opus 5.5, 2026-09-28, on
ASTRA-REQ-FABLE-SCRIPT-ARRAY-CLAMP). Decoded from the certified image; nothing executed.

  K1 the resolver 00262440 zeroes ebx (0026245D); each popped index reaches 0026250C in eax - as an int (0026257D) or a truncated
     float (00262571), or ebx's 0 when the stack is empty (002624DA) - and the dimension is a signed 32-bit read (002624D5 mov esi)
  K2 0026250C..00262518 compute index' = min(max(index, 0), dim - 1): 'mov ecx, ebx / cmovns ecx, eax' is max(index, 0), and
     'lea eax, [rsi - 1] / cmp ecx, esi / cmovl eax, ecx' keeps it only when it is below dim, else dim - 1
  K3 so the edge element is read only for dim >= 1: a dimension of 0 gives index' = -1, one element before the array, and a
     negative dimension gives dim - 1; nothing in this stage rejects a dimension <= 0
  C  control: modelled with 'cmovle' in place of 'cmovl' (keep the index when it equals dim), dim 3 would admit index 3 - one past
     the end - so K2's bound is the strict compare the image has
  Not claimed: whether any shipped array has a dimension <= 0, upstream validation, product overflow, or a storage fault.
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
   "ebx = 0; index in eax from the int or float pop paths (or 0 on an empty stack); dimension a signed dword")
ok("K2", [B[a] for a in (0x26250C, 0x26250E, 0x262510, 0x262513, 0x262516, 0x262518)] ==
   ["test eax, eax", "mov ecx, ebx", "cmovns ecx, eax", "lea eax, [rsi - 1]", "cmp ecx, esi", "cmovl eax, ecx"],
   "index' = min(max(index, 0), dim - 1), strict compare")
def clamp(i, dim, le=False):
    ecx = i if i >= 0 else 0
    return ecx if (ecx <= dim if le else ecx < dim) else dim - 1
res = {(i, dim): clamp(i, dim) for i, dim in ((5, 3), (-2, 3), (1, 3), (0, 0), (4, 0), (2, -2))}
ok("K3", res == {(5, 3): 2, (-2, 3): 0, (1, 3): 1, (0, 0): -1, (4, 0): -1, (2, -2): -3},
   "(index, dim) -> index': %s" % res)
ok("C", clamp(3, 3, le=True) == 3 and clamp(3, 3) == 2, "a cmovle model admits index 3 for dim 3; the image's cmovl gives 2")
print("FAILS", fails); sys.exit(1 if fails else 0)
