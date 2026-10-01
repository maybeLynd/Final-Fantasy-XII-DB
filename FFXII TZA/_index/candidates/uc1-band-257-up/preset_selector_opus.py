"""preset_selector_opus.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only; no execution.
Independent review of ASTRA-REQ-OPUS-PRESET-SELECTOR-COUPLING (_experiments/evidence/native-preset-selector-coupling/) for
00712180 (the YEBIS preset setter, FABLE yebis-preset-selector 10308fd02), written without ASTRA's code.

  D  00712180(target rcx, s1 edx, s2 r8d, s3 r9d), decoded:
       null target -> return it; s1 >= 0 -> row min(s1, 7) of 8-byte table 01F3C5B0 -> +0x4C, +0x54;
       s2 >= 0 -> cap 19 when the .rdata byte 00D9F05E is non-zero (it is 1 in the image), else 10; row min(s2, cap) of
       0x1C-byte table 01F3C5F0 -> +0x7C, +0x84, +0x88, +0xCC, +0x8C (from row +0x10, kept in edx), +0xE4, +0xE8;
       then if s3 < 0 it takes edx (0071222A) - only on this path; s2 < 0 jumps straight to the s3 sign test (0071222D);
       s3 still < 0 -> return; else row min(s3, 9) of 0x38-byte table 01F3C820 -> +0x90..+0xC4 (14 dwords)
  T  the 20 rows reachable under cap 19 all hold a row +0x10 default of 1..5, so with s2 >= 0 a negative s3 selects a
     third-table row (the default) and never skips; with s2 < 0 a negative s3 skips
  M  model and control: a model of D gives, for (s2, s3) = (0, -1), third row 1 (row 0's default) and 21 stores; the
     control with the 0071222A transfer removed gives no third row and 7 stores for the second block only
Usage: python preset_selector_opus.py
"""
import hashlib, os, struct, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__)); DB = os.path.abspath(os.path.join(HERE, "..", "..", "..")); ROOT = os.path.dirname(DB)
d = open(os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe"), "rb").read()
if hashlib.sha256(d).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8":
    print("REFUSED  not the certified image"); sys.exit(2)
B = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [(d[pe + 24 + opt + i * 40:pe + 24 + opt + i * 40 + 8].rstrip(b"\0"),) + struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for nm, vs, va, rs, ro in SECS:
        if B + va <= v < B + va + rs: return v - B - va + ro
def sec(v): return next(nm for nm, vs, va, rs, ro in SECS if B + va <= v < B + va + max(vs, rs))
cs = Cs(CS_ARCH_X86, CS_MODE_64)
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
A = {x.address: (x.mnemonic, x.op_str) for x in cs.disasm(d[off(0x712180):off(0x712180) + 353], 0x712180)}
KEY = [(0x712186, ("je", "0x7122dd")), (0x71218E, ("js", "0x7121b3")), (0x712190, ("mov", "eax, 7")), (0x71219E, ("cmovl", "eax, edx")),
       (0x7121A7, ("mov", "dword ptr [r10 + 0x4c], eax")), (0x7121AF, ("mov", "dword ptr [r10 + 0x54], eax")), (0x7121B6, ("js", "0x71222d")),
       (0x7121B8, ("cmp", "byte ptr [rip + 0x68ce9f], 0")), (0x7121BF, ("mov", "eax, 0xa")), (0x7121C4, ("mov", "ecx, 0x13")), (0x7121C9, ("cmovne", "eax, ecx")),
       (0x7121CF, ("cmovl", "eax, r8d")), (0x7121D5, ("imul", "rcx, rax, 0x1c")), (0x712207, ("mov", "edx, dword ptr [rcx + 0x10]")),
       (0x71220A, ("mov", "dword ptr [r10 + 0x8c], edx")), (0x712225, ("test", "r9d, r9d")), (0x712228, ("jns", "0x712236")), (0x71222A, ("mov", "r9d, edx")),
       (0x71222D, ("test", "r9d, r9d")), (0x712230, ("js", "0x7122dd")), (0x712236, ("mov", "eax, 9")), (0x71223E, ("cmovl", "eax, r9d")),
       (0x712244, ("imul", "rcx, rax, 0x38")), (0x712254, ("mov", "dword ptr [r10 + 0x90], eax")), (0x7122D6, ("mov", "dword ptr [r10 + 0xc4], eax")), (0x7122E0, ("ret", ""))]
T1, T2, T3, MODE = 0x712195 + 7 + 0x182A414, 0x7121E0 + 0x182A410, 0x712248 + 7 + 0x182A5D1, 0x7121BF + 0x68CE9F
check("D", all(A.get(a) == v for a, v in KEY) and (T1, T2, T3, MODE) == (0x1F3C5B0, 0x1F3C5F0, 0x1F3C820, 0xD9F05E) and sec(MODE) == b".rdata" and d[off(MODE)] == 1,
      "00712180: caps 7 / (19 when .rdata 00D9F05E = %d) / 9; the negative-s3 transfer 0071222A lies only on the s2 >= 0 path" % d[off(MODE)])
defaults = [struct.unpack_from("<i", d, off(T2 + 0x1C * i + 0x10))[0] for i in range(20)]
check("T", all(1 <= v <= 5 for v in defaults), "row +0x10 defaults of the 20 reachable second-table rows: %s" % defaults)
def model(s1, s2, s3, transfer=True):
    stores = 0; third = None
    if s1 >= 0: stores += 2
    edx = None
    if s2 >= 0:
        row = min(s2, 19 if d[off(MODE)] else 10); stores += 7; edx = defaults[row] if row < 20 else None
        if s3 < 0 and transfer: s3 = edx
    if s3 >= 0: third = min(s3, 9); stores += 14
    return third, stores
m, c, skip = model(-1, 0, -1), model(-1, 0, -1, transfer=False), model(-1, -1, -1)
check("M", m == (1, 21) and c == (None, 7) and skip == (None, 0),
      "(s2, s3) = (0, -1): third row %s with %d stores; without the transfer: %s; s2 < 0 and s3 < 0: %s" % (m[0], m[1], c, skip))
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
