"""float_rounding2.py - POPV's int -> float conversion (cvtdq2ps) for signed inputs, all four MXCSR rounding modes (FABLE, Claude
Opus 5.5, 2026-09-28, on ASTRA-REQ-FABLE-SCRIPT-NEGATIVE-ROUNDING). Supersedes ../script-store-saturation/float_rounding.py's
cvt() helper, whose round-up step added one to the raw bits - correct above zero, wrong below it; that file and its output stay
as they were. Decoded from the certified image; the rounding is modelled, nothing native executed.

  F1, F2 as float_rounding.py: a tag-1 int reaches 'cvtdq2ps xmm0, xmm0' (00267ED2) and the f32 store copies the result raw
  F3 the model: for a signed 32-bit i, ulp = 2^max(e - 23, 0) with e = floor(log2 |i|); RD = floor(i / ulp) * ulp and
     RU = ceil(i / ulp) * ulp (toward -inf / +inf, whatever the sign), RZ = the one of the two nearer zero, RN = the nearer, a tie
     going to the even significand
  F4 its RN equals Python's own double -> float32 conversion (an independent round-to-nearest-even) on a signed grid:
     +-(2^24 - 2 .. 2^24 + 66), +-(2^25 + 0 .. 70), INT_MIN, INT_MAX, INT_MIN + 1..64 and INT_MAX - 64..
  F5 every mode's result is a float32 (round-trips), RD <= i <= RU, RD and RU are adjacent float32 values when i is not exact,
     and RZ / RN are one of the two - on the same grid
  F6 the stated values: 16,777,217 -> RN 4B800000, RU 4B800001 (unchanged); -16,777,219 -> RN CB800002 (-16,777,220),
     RU CB800001 (-16,777,218), RD CB800002, RZ CB800001 - the RN and RU pair are ASTRA's executed results (MXCSR 1F80, 5F80);
     INT_MAX -> RN and RU 4F000000 (2^31), RD and RZ 4EFFFFFF; INT_MIN exact (CF000000) in all four
  C1 control, sensitive to the defect: float_rounding.py's cvt() (copied verbatim) agrees with F3 on every positive grid value
     and gives CB800003 (-16,777,222) for -16,777,219 under RU - it rounded a negative value away from +inf
  C2 control: with ties going away from zero instead of to even, RN changes on the grid's tie values (16,777,217 becomes
     4B800001 instead of 4B800000), so F4's agreement exercises the tie rule
  Not claimed: the game's MXCSR, native flags or unmasked exceptions, which inputs a shipped script stores, or the float -> int
  direction (popv_conversion.py)
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
S = {i.address: (i.mnemonic + " " + i.op_str).strip() for i in MD.disasm(d[off(0x26D530):off(0x26D530) + 0xC2], 0x26D530)}
ST = [0x120000 + struct.unpack_from("<I", d, off(0x120000 + 0x14D5F4) + 4 * k)[0] for k in range(6)]
ok("F1F2", B[0x267EC9] == "movd xmm0, dword ptr [rbx + rdx*4 + 0x184]" and B[0x267ED2] == "cvtdq2ps xmm0, xmm0"
   and B[0x267ED5] == "movss dword ptr [rsp + 0x50], xmm0" and ST[5] == 0x26D5E9 and S[0x26D5E9] == "mov eax, dword ptr [r9 + 0x20]"
   and S[0x26D5ED] == "mov dword ptr [r8 + rcx*4], eax", "int -> cvtdq2ps -> raw dword store (width 5)")
bits = lambda v: struct.unpack("<I", struct.pack("<f", float(v)))[0]
def cvt(i, mode, tie_even=True):
    if i == 0: return 0
    e = abs(i).bit_length() - 1; ulp = 1 << max(e - 23, 0)
    dn = (i // ulp) * ulp; up = -((-i) // ulp) * ulp
    if dn == up: return i
    if mode == "RD": return dn
    if mode == "RU": return up
    if mode == "RZ": return up if i < 0 else dn
    if i - dn != up - i: return dn if i - dn < up - i else up
    if tie_even: return dn if (dn // ulp) % 2 == 0 else up
    return up if i > 0 else dn                                            # ties away from zero (control C2)
INT_MIN, INT_MAX = -2 ** 31, 2 ** 31 - 1
POS = list(range(2 ** 24 - 2, 2 ** 24 + 67)) + list(range(2 ** 25, 2 ** 25 + 71))
GRID = POS + [-v for v in POS] + [INT_MIN, INT_MAX] + list(range(INT_MIN + 1, INT_MIN + 65)) + list(range(INT_MAX - 64, INT_MAX))
MODES = ("RN", "RD", "RU", "RZ")
ok("F3", all(cvt(v, m) is not None for v in GRID for m in MODES), "model defined on %d signed values x 4 modes" % len(GRID))
rn_bad = [v for v in GRID if bits(cvt(v, "RN")) != bits(struct.unpack("<f", struct.pack("<f", float(v)))[0])]
ok("F4", not rn_bad, "RN equals Python's double -> float32 rounding on all %d; mismatches %s" % (len(GRID), rn_bad[:4]))
f32 = lambda u: struct.unpack("<f", struct.pack("<I", u))[0]
def nxt_up(v):                                                            # next float32 toward +inf, from the bits
    b = bits(v); return f32(b + 1) if v >= 0 else f32(b - 1)
bad5 = []
for v in GRID:
    r = {m: cvt(v, m) for m in MODES}
    if any(f32(bits(x)) != x for x in r.values()) or not r["RD"] <= v <= r["RU"]: bad5.append(v); continue
    if r["RD"] != v and (nxt_up(r["RD"]) != r["RU"] or r["RZ"] not in (r["RD"], r["RU"]) or r["RN"] not in (r["RD"], r["RU"])): bad5.append(v)
ok("F5", not bad5, "results representable, bracketing, adjacent; failures %s" % bad5[:4])
got = {(v, m): bits(cvt(v, m)) for v in (16777217, -16777219, INT_MAX, INT_MIN) for m in MODES}
ok("F6", got[(16777217, "RN")] == 0x4B800000 and got[(16777217, "RU")] == 0x4B800001
   and [got[(-16777219, m)] for m in MODES] == [0xCB800002, 0xCB800002, 0xCB800001, 0xCB800001]
   and [got[(INT_MAX, m)] for m in MODES] == [0x4F000000, 0x4EFFFFFF, 0x4F000000, 0x4EFFFFFF]
   and {got[(INT_MIN, m)] for m in MODES} == {0xCF000000},
   "-16777219: RN %08X RD %08X RU %08X RZ %08X; INT_MAX RN %08X RD %08X" % tuple([got[(-16777219, m)] for m in MODES] + [got[(INT_MAX, "RN")], got[(INT_MAX, "RD")]]))
def cvt_v1(i, mode):                                                      # float_rounding.py's cvt(), verbatim
    lo = struct.unpack("<f", struct.pack("<f", float(i)))[0]           # round-to-nearest-even
    if mode == "RN" or lo == i: return bits(lo)
    if mode == "RU": return bits(lo) + (1 if lo < i else 0)            # next representable up (positive values)
    raise ValueError(mode)
pos_ok = all(cvt_v1(v, m) == bits(cvt(v, m)) for v in POS for m in ("RN", "RU"))
ok("C1", pos_ok and cvt_v1(-16777219, "RU") == 0xCB800003 and bits(cvt(-16777219, "RU")) == 0xCB800001,
   "old cvt() agrees on the positive grid; at -16777219 RU it gives %08X, the model %08X" % (cvt_v1(-16777219, "RU"), bits(cvt(-16777219, "RU"))))
ties = [v for v in GRID if bits(cvt(v, "RN")) != bits(cvt(v, "RN", tie_even=False))]
ok("C2", 16777217 in ties and bits(cvt(16777217, "RN", tie_even=False)) == 0x4B800001, "ties-away-from-zero differs on %d grid values (16777217 among them), so F4 tests the tie rule" % len(ties))
print("FAILS", fails); sys.exit(1 if fails else 0)
