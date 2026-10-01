r"""OPUS reviewer check for NAS package 5 (DM-2), 2026-09-27: does any code compare the Win32 virtual-key codes of the
reserved keys (- = ] \ , . / and the Alts) while never comparing those of [ ; ' ? Every cmp-with-immediate in the listed
bodies (Tools/work/graph/functions.tsv) is counted per key. Self-contained; run from the Database directory.
Result 2026-09-27: - 0, = 0, ] 1, \ 2, , 0, . 2, / 1, Alt 0x12 107 (an everyday constant), LAlt 1, RAlt 0; [ 1, ; 1, ' 0.
The one function comparing several punctuation VKs (001EC760) compares [ with \ . / - no separation.
Usage: python vk_compare_scan.py [exe] [functions.tsv]"""
import collections, re, struct, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

EXE = sys.argv[1] if len(sys.argv) > 1 else "Tools/work/exe/FFXII_TZA.exe"
FUN = sys.argv[2] if len(sys.argv) > 2 else "Tools/work/graph/functions.tsv"
BASE = 0x120000
VK = {"-": 0xBD, "=": 0xBB, "]": 0xDD, "\\": 0xDC, ",": 0xBC, ".": 0xBE, "/": 0xBF,
      "Alt": 0x12, "LAlt": 0xA4, "RAlt": 0xA5, "[": 0xDB, ";": 0xBA, "'": 0xDE}
d = open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
off = lambda v: next((v - BASE - va + ro for vs, va, rs, ro in secs if BASE + va <= v < BASE + va + rs), None)
cs = Cs(CS_ARCH_X86, CS_MODE_64); hits = collections.defaultdict(set)
for l in open(FUN, encoding="utf-8"):
    c = l.split("\t")
    try: f, sz = int(c[0], 16), int(c[2])
    except (ValueError, IndexError): continue
    o = off(f)
    if o is None or not (0x121000 <= f < 0x900000): continue
    for x in cs.disasm(d[o:o + sz], f):
        if x.mnemonic != "cmp": continue
        m = re.search(r", (0x[0-9a-f]+|\d+)$", x.op_str)
        if not m: continue
        v = int(m.group(1), 0)
        for k, code in VK.items():
            if v == code: hits[k].add(f)
for k in VK: print("%-5s %4d functions %s" % (k, len(hits[k]), sorted("%08X" % f for f in hits[k])[:8]))
reserved = {k for k in VK if k not in ("[", ";", "'")}
sep = [f for f in set().union(*(hits[k] for k in reserved if k != "Alt")) if not any(f in hits[u] for u in ("[", ";", "'"))]
print("functions comparing a reserved punctuation / LAlt / RAlt VK but no unreserved one:", ["%08X" % f for f in sorted(sep)])
