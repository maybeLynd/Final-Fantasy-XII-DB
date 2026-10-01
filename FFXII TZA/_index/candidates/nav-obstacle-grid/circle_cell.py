"""circle_cell.py - the nav rasterizer's circle-cell test 004690B0 (237 B), read from the certified image and modelled in float32
(FABLE, Claude Opus 5.5, 2026-09-28, on ASTRA-REQ-FABLE-NAV-CIRCLE-CELL). Rectangle at rcx {x0 +0, z0 +8, x1 +0x10, z1 +0x18};
circle at rdx {cx +0, cz +8, r +0x10}.

  K1 the instruction sequence: band 1 (centre in [x0 - r, x1 + r] x [z0, z1], every compare falling through on equality - jb
     fails), band 2 (centre in [x0, x1] x [z0 - r, z1 + r], the same), then the four corners by r*r > dx*dx + dz*dz with ja /
     seta - strict; the order of the adds and multiplies is the image's
  K2 a float32 model of that order reproduces ASTRA's executed cases on rectangle 0..10, r = 5: edge contact (-5, 5) -> 1; the
     four 3-4-5 corner tangencies -> 0; r one ulp above 5 (40A00001) at corner (-3, -4) -> r*r = 41C80003 -> 1; r one ulp below
     (409FFFFF) -> 41C7FFFE -> 0
  K3 NaN in any coordinate returns 0 once the compares complete (unordered sets CF: every band compare fails, no corner ja taken)
  C  control: a model with the first corner compare made inclusive (jae) accepts the exact corner tangency, as ASTRA's private
     mutant did - so K2's 0 is the strict compare, not an artefact of the model
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
I = [(i.address, (i.mnemonic + " " + i.op_str).strip()) for i in MD.disasm(d[off(0x4690B0):off(0x4690B0) + 237], 0x4690B0)]
T = dict(I)
ok("K1", I[-1] == (0x46919C, "ret") and I[-1][0] + 1 == 0x4690B0 + 237
   and [T[a] for a in (0x4690C7, 0x4690D2, 0x4690DF, 0x4690E9, 0x4690F4, 0x469107, 0x469111)] == ["jb 0x4690f1"] * 4 + ["jb 0x469120"] * 3
   and T[0x46911E] == "jae 0x4690eb" and [T[a] for a in (0x469147, 0x469165, 0x469182)] == ["ja 0x4690eb"] * 3 and T[0x469199] == "seta al"
   and T[0x46912E] == "mulss xmm2, xmm2" and T[0x469140] == "addss xmm1, xmm0",
   "bands close on equality (jb fails / jae passes); corners compare r*r > d*d strictly (ja, seta); %d instructions" % len(I))
f = lambda v: struct.unpack("<f", struct.pack("<f", v))[0]
fb = lambda u: struct.unpack("<f", struct.pack("<I", u))[0]
bits = lambda v: struct.unpack("<I", struct.pack("<f", v))[0]
def ge(a, b): return not (math.isnan(a) or math.isnan(b)) and a >= b        # comiss a, b; jb fail  => pass iff a >= b (ordered)
def gt(a, b): return not (math.isnan(a) or math.isnan(b)) and a > b         # comiss a, b; ja / seta
def test(rect, circ, corner_incl=False):
    x0, z0, x1, z1 = map(f, rect); cx, cz, r = map(f, circ)
    if ge(cx, f(x0 - r)) and ge(cz, z0) and ge(f(r + x1), cx) and ge(z1, cz): return 1   # band 1 (as ordered in the image)
    if ge(cx, x0) and ge(cz, f(z0 - r)) and ge(x1, cx) and ge(f(r + z1), cz): return 1                  # band 2
    r2 = f(r * r)
    dx0, dz0 = f(x0 - cx), f(z0 - cz)
    first = f(f(dz0 * dz0) + f(dx0 * dx0))
    if (ge(r2, first) if corner_incl else gt(r2, first)): return 1
    dz1 = f(z1 - cz)
    if gt(r2, f(f(dz1 * dz1) + f(dx0 * dx0))): return 1
    dx1 = f(x1 - cx)
    if gt(r2, f(f(dz0 * dz0) + f(dx1 * dx1))): return 1
    return int(gt(r2, f(f(dz1 * dz1) + f(dx1 * dx1))))
R = (0.0, 0.0, 10.0, 10.0)
corners = [(-3.0, -4.0), (13.0, -4.0), (-3.0, 14.0), (13.0, 14.0)]
up, dn = fb(0x40A00001), fb(0x409FFFFF)
ok("K2", test(R, (-5.0, 5.0, 5.0)) == 1 and all(test(R, (x, z, 5.0)) == 0 for x, z in corners)
   and bits(f(up * up)) == 0x41C80003 and test(R, (-3.0, -4.0, up)) == 1 and bits(f(dn * dn)) == 0x41C7FFFE and test(R, (-3.0, -4.0, dn)) == 0,
   "edge (-5, 5) -> 1; four corner tangencies -> 0; r 40A00001 -> r*r %08X -> 1; r 409FFFFF -> %08X -> 0" % (bits(f(up * up)), bits(f(dn * dn))))
nan = float("nan")
ok("K3", test(R, (nan, 5.0, 5.0)) == 0 and test(R, (5.0, nan, 5.0)) == 0 and test(R, (5.0, 5.0, nan)) == 0, "NaN centre or radius -> 0")
ok("C", test(R, (-3.0, -4.0, 5.0), corner_incl=True) == 1, "an inclusive first corner compare accepts the exact tangency")
print("FAILS", fails); sys.exit(1 if fails else 0)
