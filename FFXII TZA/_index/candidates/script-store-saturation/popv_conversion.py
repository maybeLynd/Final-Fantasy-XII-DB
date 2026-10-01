"""popv_conversion.py - POPV converts a float operand to int BEFORE the width clamp (FABLE, Claude Opus 5.5, 2026-09-28, on
ASTRA-REQ-FABLE-SCRIPT-POPV-CONVERSION). Decoded from the certified image; the conversion is modelled, not executed.

  P1 POPV 00267E60, integer-kind stage: the popped operand's tag selects the read - tag 1 (sub ecx, 1 / je) takes the raw dword
     (00267F57), tag 2 takes 'cvttss2si' (00267F4C), an empty stack gives 0 (00267F18) - all into the record's +0x20 ([rsp + 0x50]
     with the record at rsp + 0x30), and only then is the width store 0026D530 called (00267F37)
  P2 modelled: cvttss2si truncates toward zero and turns any float at or above 2^31 (and NaN) into the integer indefinite 0x80000000;
     the store then clamps that as a negative number - so 1.75 stores 1, the largest float below 2^31 (4EFFFFFF = 2147483520) stores
     255 into a u8 and 0x8000 into an s16, while 2^31 itself (4F000000) stores 0 into a u8 and 0x8001 into an s16: a float one step
     larger lands at the bottom of the range instead of the top
  C  control: a model that rounds to nearest instead of truncating stores 2 for 1.75; a model that saturates the float before
     converting would store 255 for 2^31 - the image does neither
  Not claimed: the game's MXCSR (truncation ignores the rounding mode; the indefinite needs the invalid exception masked), whether
     any shipped script pushes such a float into an integer variable
"""
import hashlib, math, os, struct, sys
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
B = {i.address: (i.mnemonic + " " + i.op_str).strip() for i in MD.disasm(d[off(0x267E60):off(0x267E60) + 256], 0x267E60)}
ok("P1", B[0x267F04] == "sub ecx, 1" and B[0x267F07] == "je 0x267f57" and B[0x267F0C] == "je 0x267f4c"
   and B[0x267F57] == "mov eax, dword ptr [rbx + rdx*4 + 0x184]" and B[0x267F4C] == "cvttss2si eax, dword ptr [rbx + rdx*4 + 0x184]"
   and B[0x267F18] == "xor eax, eax" and B[0x267F1A] == "mov dword ptr [rsp + 0x50], eax" and B[0x267F32] == "lea rcx, [rsp + 0x30]"
   and B[0x267F37] == "call 0x26d530" and min(a for a in (0x267F4C, 0x267F57, 0x267F18)) < 0x267F37,
   "tag 1 raw, tag 2 cvttss2si, empty 0 -> record +0x20, then 0026D530")
f32 = lambda u: struct.unpack("<f", struct.pack("<I", u))[0]
def cvtt(x):
    if math.isnan(x) or x >= 2 ** 31 or x < -2 ** 31: return -2 ** 31
    return int(x)                                             # Python int() truncates toward zero
u8 = lambda v: 0 if v < 0 else min(v, 255)
s16 = lambda v: 0x8001 if v < -32767 else min(v, 32768) & 0xFFFF
below, at = f32(0x4EFFFFFF), f32(0x4F000000)
r = {"1.75": cvtt(1.75), "below": cvtt(below), "at": cvtt(at),
     "u8 below": u8(cvtt(below)), "u8 at": u8(cvtt(at)), "s16 below": s16(cvtt(below)), "s16 at": s16(cvtt(at))}
ok("P2", r == {"1.75": 1, "below": 2147483520, "at": -2147483648, "u8 below": 255, "u8 at": 0, "s16 below": 0x8000, "s16 at": 0x8001},
   "modelled: %s" % r)
ok("C", round(1.75) == 2 and u8(min(int(at), 2 ** 31 - 1)) == 255,
   "round-to-nearest would store 2 for 1.75; saturating the float first would store 255 for 2^31")
print("FAILS", fails); sys.exit(1 if fails else 0)
