"""float_rounding.py - POPV converts an int operand for a float variable with cvtdq2ps, which rounds by the MXCSR rounding mode
(FABLE, Claude Opus 5.5, 2026-09-28, on ASTRA-REQ-FABLE-SCRIPT-FLOAT-ROUNDING). Decoded from the certified image; rounding modelled.

  F1 POPV's float-kind stage: a tag-1 (int) operand takes 'movd xmm0, [..] / cvtdq2ps xmm0, xmm0 / movss [rsp + 0x50], xmm0'
     (00267EC9..00267ED5); a tag-2 (float) operand is copied as it is (00267EB8); an empty stack stores 0.0 (00267EE7)
  F2 the store 0026D530 copies width 5 (f32) as a raw dword, so the conversion is the only rounding step
  F3 modelled: 16,777,217 (2^24 + 1, not representable in float32) becomes 4B800000 (16,777,216) under round-to-nearest-even and
     4B800001 (16,777,218) under round-up - the value stored depends on MXCSR's rounding control, which the game's state does not
     fix here; every int of magnitude up to 2^24 converts exactly
  C  control: a truncating model (as cvttss2si does on the other path) would give 16,777,216 under both modes, so F3's mode
     dependence is cvtdq2ps's, not the model's
  Not claimed: the game's MXCSR, native flags, or whether a shipped script stores such an int into a float variable
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
ok("F1", B[0x267EC9] == "movd xmm0, dword ptr [rbx + rdx*4 + 0x184]" and B[0x267ED2] == "cvtdq2ps xmm0, xmm0"
   and B[0x267ED5] == "movss dword ptr [rsp + 0x50], xmm0" and B[0x267EB8] == "movss xmm0, dword ptr [rbx + rdx*4 + 0x184]"
   and B[0x267EE7] == "xorps xmm0, xmm0", "int -> cvtdq2ps; float copied; empty -> 0.0")
S = {i.address: (i.mnemonic + " " + i.op_str).strip() for i in MD.disasm(d[off(0x26D530):off(0x26D530) + 0xC2], 0x26D530)}
ST = [0x120000 + struct.unpack_from("<I", d, off(0x120000 + 0x14D5F4) + 4 * k)[0] for k in range(6)]
ok("F2", ST[5] == 0x26D5E9 and S[0x26D5E9] == "mov eax, dword ptr [r9 + 0x20]" and S[0x26D5ED] == "mov dword ptr [r8 + rcx*4], eax",
   "width 5 -> raw dword copy")
bits = lambda f: struct.unpack("<I", struct.pack("<f", f))[0]
def cvt(i, mode):
    lo = struct.unpack("<f", struct.pack("<f", float(i)))[0]           # round-to-nearest-even
    if mode == "RN" or lo == i: return bits(lo)
    if mode == "RU": return bits(lo) + (1 if lo < i else 0)            # next representable up (positive values)
    raise ValueError(mode)
r = {m: cvt(16777217, m) for m in ("RN", "RU")}
exact = all(cvt(v, "RN") == cvt(v, "RU") for v in (0, 1, 16777215, 16777216, -16777216))
ok("F3", r == {"RN": 0x4B800000, "RU": 0x4B800001} and exact,
   "16777217 -> RN %08X, RU %08X; ints up to 2^24 are exact under both" % (r["RN"], r["RU"]))
trunc = lambda i: bits(float(math.trunc(i / 2) * 2)) if i > 2 ** 24 else bits(float(i))
ok("C", trunc(16777217) == 0x4B800000 and r["RU"] != trunc(16777217), "a truncating model gives 4B800000 regardless of mode")
print("FAILS", fails); sys.exit(1 if fails else 0)
