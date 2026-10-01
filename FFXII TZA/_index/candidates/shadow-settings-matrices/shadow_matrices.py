"""shadow_matrices.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only.

ShadowSettings01F82EA8 (0xB08) holds EIGHT 4x4 float matrices 0xD8 apart, at +0x1C0 + 0xD8*i (i = 0..7). The store carried
each as the head of an 84-byte 'span' row (DISCOVERED u8[84]). 001F0AD0 reads every one the same way:
  M1 per matrix, four 16-byte loads - movups of +0x10 / +0x20 / +0x30 into xmm3 / xmm4 / xmm5 and of +0x00 into xmm0 -
     at +0x1C0, +0x298, +0x370, +0x448, +0x520, +0x5F8, +0x6D0, +0x7A8 (0x1C0 + 0xD8*i)
  M2 each loaded row is split into its four float lanes (shufps 0x55 / 0xaa / 0xff and movss stores to globals): the
     rows are float[4], so each matrix is float[4][4]
Not claimed: a 0xD8 element type. Only these 64 bytes are read uniformly in all eight strides; the bytes after them are
touched element by element, and the eighth stride's tail (+0x82C..) holds the container's own named fields
(decayDistance +0x830, mapHeightMin / Max, cascadePartition0-2), so the stride is not an element size here. What the
matrices transform is NOT claimed.
  S  REGRESSION: the store has +0x1C0 + 0xD8*i float[4][4] (64) for i = 0..7, each followed by a 20-byte remainder span
     (FAILS before the patch)
Usage: python shadow_matrices.py [--patch]
"""
import hashlib, os, struct, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__)); DB = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
d = open(os.path.join(os.path.dirname(DB), "Tools", "work", "exe", "FFXII_TZA.exe"), "rb").read()
if hashlib.sha256(d).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8":
    print("REFUSED  not the certified image"); sys.exit(2)
FIELDS = os.path.join(DB, "_types", "fields.tsv"); REC = "_index/candidates/shadow-settings-matrices/shadow_matrices.py"
T = "ShadowSettings01F82EA8"; BASES = [0x1C0 + 0xD8 * i for i in range(8)]
B = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
off = lambda v: next(v - B - va + ro for vs, va, rs, ro in SECS if B + va <= v < B + va + rs)
cs = Cs(CS_ARCH_X86, CS_MODE_64)
body = [(x.address, x.mnemonic, x.op_str) for x in cs.disasm(d[off(0x1F0AD0):off(0x1F0AD0) + 2738], 0x1F0AD0)]
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
loads = {(o.split(", ")[0], int(o.split("+ ")[1].rstrip("]"), 16)) for a, m, o in body
         if m == "movups" and o.startswith("xmm") and "[rbx + " in o}
m1 = all({("xmm0", b), ("xmm3", b + 0x10), ("xmm4", b + 0x20), ("xmm5", b + 0x30)} <= loads for b in BASES)
check("M1", m1, "four 16-byte row loads at each of %s" % [hex(b) for b in BASES])
shuf = [o for a, m, o in body if m == "shufps"]
lanes = sum(1 for o in shuf if o.endswith(("0x55", "0xaa", "0xff")))
movss_g = sum(1 for a, m, o in body if m == "movss" and o.startswith("dword ptr [rip"))
check("M2", lanes >= 8 * 12 and movss_g >= 8 * 16,
      "rows split into float lanes: %d lane shuffles, %d movss stores of lanes to globals" % (lanes, movss_g))
fl = open(FIELDS, "rb").read().decode("utf-8").splitlines(keepends=True)
def cells(l): return l.rstrip("\r\n").split("\t")
if "--patch" in sys.argv:
    out = list(fl); done = 0
    for i in range(len(out) - 1, -1, -1):
        c = cells(out[i])
        if c[0] != T or int(c[1], 16) not in BASES or c[4] != "u8[84]": continue
        b = int(c[1], 16); k = BASES.index(b); eol = out[i][len(out[i].rstrip("\r\n")):]; w = len(c)
        row = lambda r: "\t".join(r + [""] * (w - len(r))) + eol
        out[i:i + 1] = [
            row([T, "0x%04X" % b, "64", "matrix%d" % k, "float[4][4]",
                 "4x4 FLOAT MATRIX %d of 8, 0xD8 apart from +0x1C0: 001F0AD0 loads its four rows as 16-byte movups and splits each "
                 "into float lanes; those are the only accesses the four-seed census finds inside it (no writer reached). What it transforms is NOT claimed; no 0xD8 element type is claimed" % k,
                 "TYPE RESOLVED", "PROVEN", "RE-CUT 2026-09-28 (OPUS, %s M1 M2). || WAS %s %s %s %s: %s" % (REC, c[1], c[2], c[3], c[4], c[5])]),
            row([T, "0x%04X" % (b + 0x40), "20", "span%04X" % (b + 0x40), "u8[20]",
                 "the 20 bytes after matrix %d, kept from the former span row: %s" % (k, c[5]), "DISCOVERED", c[7],
                 "RE-CUT REMAINDER 2026-09-28 (OPUS, %s): %s" % (REC, c[8])])]
        done += 1
    open(FIELDS, "wb").write("".join(out).encode("utf-8")); print("re-cut %d spans" % done); sys.exit(0)
F = {int(cells(l)[1], 16): cells(l) for l in fl if cells(l)[0] == T}
check("S", all(F.get(b, [0] * 5)[4] == "float[4][4]" and F[b][2] == "64" and F.get(b + 0x40, [0] * 5)[2] == "20" for b in BASES),
      "eight float[4][4] rows at 0x1C0 + 0xD8*i with 20-byte remainders")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
