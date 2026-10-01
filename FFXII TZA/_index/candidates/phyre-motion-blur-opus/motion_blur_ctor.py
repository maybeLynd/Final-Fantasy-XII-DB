"""motion_blur_ctor.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only.
CORRECTION of OPUS's own PMotionBlurBase rows (2026-09-19 / 2026-09-20): 'the element is 0x14, not 0x40', 'the identity
reading is WRONG', 'the constructor initialises only SIX records' and 'the setter writes nothing between +0xD0 and +0xD10'.
The same constructor refutes all four - the earlier reading stopped before its loop.

  C  00646000 (PMotionBlurBase's constructor: 006461B0, then vtable 00D620D0) writes 0x40-byte blocks, each exactly
     {1.0f at +0x00, +0x14, +0x28, +0x3C; zero elsewhere} - the 4x4 identity: two at +0x50 / +0x90, then a 16-pass loop
     (rcx = 0x10, rax = this + 0x528, rax += 0x40) writing the block at rax - 0x18 (+0x510 + 0x40k) and at rax - 0x418
     (+0x110 + 0x40k); then +0xD10 = 10.0f and ten zero qwords +0xD18..+0xD60
  R  REGRESSION AGAINST THE 0x14 READING: a 0x14 record {1.0f, 16 zero bytes} predicts 1.0f at +0xA0 and none at +0x90; the
     constructor stores zero at +0xA0 (`mov dword ptr [rbx + 0xa0], edx`) and 1.0f at +0x90 - the step +0x8C -> +0x90 is the
     block boundary. Over all 34 blocks the 1.0f offsets are exactly base + {0, 0x14, 0x28, 0x3C}
  D  0063F580, PMotionBlurD3D11's descriptor slot +0x50 (00D5A140 + 0x50), runs 00646000, installs 00D62120 and zeroes +0xD68;
     PMotionBlurBase's placement thunk 0063E9C0 calls 00646000
  N  the vtable census of 00D620D0 (9 methods) and 00D62120 (10) reaches nothing in +0x50..+0xD67: the matrices' readers are
     outside the classes' own methods, so float typing rests on the constructor's identity pattern (PROBABLE)
  W  REGRESSION (FAILS before): the rows state the 0x40 blocks and the loop, and keep the old text in their evidence
Not claimed: what the 34 matrices are for; who fills +0xD0..+0x10F and +0x910..+0xD0F (the sampled default buffer's
1.0f pattern there came from a path this constructor is not).
Usage: python motion_blur_ctor.py [--patch]
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
pe = pefile.PE(EXEP, fast_load=True); IB = pe.OPTIONAL_HEADER.ImageBase
off = lambda v: pe.get_offset_from_rva(v - B)
cs = Cs(CS_ARCH_X86, CS_MODE_64)
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
L = list(cs.disasm(d[off(0x646000):off(0x6461AD)], 0x646000))
A = {x.address: (x.mnemonic, x.op_str) for x in L}
def stores(base_reg, lo, hi):
    """(displacement, width, value) of every store off base_reg in [lo, hi); value 1.0f / 0 (rdx / edx) / other."""
    out = []
    for x in L:
        if not (lo <= x.address < hi) or x.mnemonic != "mov" or not x.op_str.startswith(("qword ptr [%s" % base_reg, "dword ptr [%s" % base_reg)): continue
        dst, src = x.op_str.split(", ")
        disp = dst.split("[")[1].rstrip("]").replace(base_reg, "").replace(" ", "")
        disp = int(disp, 16) if disp else 0
        if dst.startswith("qword"): val = {"0x3f800000": (1.0, 0.0), "rdx": (0.0, 0.0)}.get(src)
        else: val = {"0x3f800000": (1.0,), "edx": (0.0,)}.get(src)
        out.append((disp, val))
    return out
def floats(st):
    m = {}
    for disp, val in st:
        if val is None: return None
        for i, v in enumerate(val): m[disp + 4 * i] = v
    return m
blk = lambda base: {base + 4 * i: (1.0 if 4 * i in (0, 0x14, 0x28, 0x3C) else 0.0) for i in range(16)}
head = floats(stores("rbx", 0x646074, 0x646103))
loop = floats(stores("rax", 0x646110, 0x646196))
want_loop = {k - 0x528: v for k, v in blk(0x528 - 0x18).items()}
want_loop.update({k - 0x528: v for k, v in blk(0x528 - 0x418).items()})
check("C", A.get(0x646009) == ("call", "0x6461b0") and A.get(0x646021) == ("lea", "rax, [rip + 0x71c0a8]") and 0x646028 + 0x71C0A8 == 0xD620D0
      and head == {**blk(0x50), **blk(0x90)} and loop == want_loop
      and A.get(0x64602B) == ("lea", "rax, [rbx + 0x528]") and A.get(0x646040) == ("lea", "ecx, [rdx + 0x10]") and A.get(0x646196) == ("lea", "rax, [rax + 0x40]")
      and A.get(0x64619A) == ("sub", "rcx, 1") and A.get(0x64619E) == ("jne", "0x646110")
      and A.get(0x646010) == ("mov", "dword ptr [rbx + 0xd10], 0x41200000")
      and [A.get(a) for a in (0x64601A, 0x646032, 0x646039, 0x646043, 0x64604A, 0x646051, 0x646058, 0x64605F, 0x646066, 0x64606D)]
          == [("mov", "qword ptr [rbx + 0x%x], rdx" % o) for o in range(0xD18, 0xD68, 8)],
      "00646000: identity blocks at +0x50 / +0x90 and, by a 16-pass loop, +0x110 + 0x40k and +0x510 + 0x40k; +0xD10 = 10.0f; +0xD18..+0xD60 zero")
ones = sorted([o for o, v in head.items() if v == 1.0] + [0x528 + k * 0x40 + o for k in range(16) for o, v in loop.items() if v == 1.0])
check("R", A.get(0x6460C3) == ("mov", "dword ptr [rbx + 0xa0], edx") and head.get(0xA0) == 0.0 and head.get(0x90) == 1.0
      and len(ones) == 34 * 4 and all(((o - 0x10) % 0x40) in (0, 0x14, 0x28, 0x3C) for o in ones),   # every block starts at 0x10 mod 0x40
      "+0xA0 is written 0 and +0x90 1.0f (a 0x14 record predicts the reverse); all 136 1.0f stores sit at block + {0, 0x14, 0x28, 0x3C}")
q = lambda va: struct.unpack_from("<Q", d, off(va))[0] - IB + B
T = list(cs.disasm(d[off(0x63F580):off(0x63F5C5)], 0x63F580)); TA = {x.address: (x.mnemonic, x.op_str) for x in T}
check("D", q(0xD5A140 + 0x50) == 0x63F580 and TA.get(0x63F5A3) == ("call", "0x646000") and TA.get(0x63F5A8) == ("lea", "rax, [rip + 0x722b71]")
      and 0x63F5AF + 0x722B71 == 0xD62120 and TA.get(0x63F5B2) == ("mov", "qword ptr [rbx + 0xd68], 0")
      and any(x.mnemonic == "call" and x.op_str == "0x646000" for x in cs.disasm(d[off(0x63E9C0):off(0x63E9F0)], 0x63E9C0)),
      "0063F580 = PMotionBlurD3D11's placement constructor (00646000, vtable 00D62120, +0xD68 = 0); 0063E9C0 is PMotionBlurBase's")
REC = "_index/candidates/phyre-motion-blur-opus/motion_blur_ctor.py"; EXE = "exe 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
TY_ = "PMotionBlurBase"
P, U, M = ("TYPE RESOLVED", "PROVEN"), ("DISCOVERED", "UNKNOWN"), ("TYPE RESOLVED", "PROBABLE")
ID = "each 0x40 block is the 4x4 identity 00646000 writes (1.0f at +0x00 / +0x14 / +0x28 / +0x3C, zero elsewhere)"
NEW = [(0x50, 128, "identity50", "float[2][16]", "two identity matrices at +0x50 / +0x90; " + ID, M),
       (0xD0, 64, "unobservedSpan00D0", "u8[64]", "not written by 00646000; no access by the classes' own methods", U),
       (0x110, 1024, "matrices110", "float[16][16]", "sixteen matrices written by 00646000's loop at rax - 0x418; " + ID, M),
       (0x510, 1024, "matrices510", "float[16][16]", "sixteen matrices written by the same loop at rax - 0x18; " + ID, M),
       (0x910, 1024, "unobservedSpan0910", "u8[1024]", "not written by 00646000; no access by the classes' own methods", U),
       (0xD14, 4, "unobservedSpan0D14", "u8[4]", "not written by 00646000 (padding before the qword run)", U),
       (0xD18, 80, "qwordsD18", "uint64[10]", "ten qwords 00646000 zeroes (+0xD18..+0xD60); no reader found", U)]
FI = os.path.join(DB, "_types", "fields.tsv"); TYP = os.path.join(DB, "_types", "types.tsv")
def cells(l): return l.rstrip("\r\n").split("\t")
if "--patch" in sys.argv:
    fl = open(FI, "rb").read().decode("utf-8").splitlines(keepends=True); out = []; old = {}; done = False
    for l in fl:
        c = cells(l)
        if c[0] == TY_ and c[1] in ("0x0050", "0x00D0", "0x0D14"): old[c[1]] = c; continue
        out.append(l)
    assert set(old) == {"0x0050", "0x00D0", "0x0D14"}
    e = fl[1][len(fl[1].rstrip("\r\n")):]
    was = " /// ".join("%s %s %s %s: %s" % (c[1], c[2], c[3], c[4], c[5]) for c in old.values())
    rows = ["\t".join([TY_, "0x%04X" % o, str(n), nm, ct, m, rd[0], rd[1],
                      "CORRECTED 2026-09-28 (OPUS, %s C R D N): the rows below +0xD10 and after it re-cut from 00646000's full body. "
                      "WAS (kept verbatim, superseded): %s. %s" % (REC, was, EXE)]) + e for o, n, nm, ct, m, rd in NEW]
    idx = max(i for i, l in enumerate(out) if cells(l)[0] == TY_); out[idx + 1:idx + 1] = rows
    open(FI, "wb").write("".join(out).encode("utf-8"))
    tl = open(TYP, "rb").read().decode("utf-8").splitlines(keepends=True)
    for i, l in enumerate(tl):
        c = cells(l); ee = l[len(l.rstrip("\r\n")):]
        if c[0] == TY_ and not c[5]: c[5] = "00646000 (after 006461B0; installs 00D620D0), through the placement thunk 0063E9C0"; tl[i] = "\t".join(c) + ee
        if c[0] == "PMotionBlurD3D11" and not c[5]: c[5] = "0063F580 (descriptor slot +0x50): 00646000, then 00D62120 and +0xD68 = 0"; tl[i] = "\t".join(c) + ee
    open(TYP, "wb").write("".join(tl).encode("utf-8")); print("patched"); sys.exit(0)
R = {int(c[1], 16): c for c in (cells(l) for l in open(FI, "rb").read().decode("utf-8").splitlines()) if c[0] == TY_}
tiles = sorted((o, int(c[2])) for o, c in R.items())
check("W", R.get(0x50, [""] * 9)[3] == "identity50" and R.get(0x110, [""] * 9)[4] == "float[16][16]" and "WAS (kept verbatim" in R.get(0x510, [""] * 9)[8]
      and all(a[0] + a[1] == b[0] for a, b in zip(tiles, tiles[1:])) and tiles[-1][0] + tiles[-1][1] == 0xD68,
      "PMotionBlurBase states the 0x40 identity blocks and the loop; old text kept; rows tile to 0xD68")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
