"""Per head block: which asm hits fall inside it, and the uncovered spans (nop/int3 padding ignored)."""
import pickle, sys
from pathlib import Path
from coff import Exe

HERE = Path(__file__).parent
DB = Path(r"C:\Users\Kristian\source\repos\XIIOnline\Database\FFXII TZA\99-Unresolved-Residual\Unlisted-Code")
exe = Exe()
blocks = []
for l in open(DB / "unlisted-code-blocks.tsv", encoding="utf-8"):
    if l.startswith("#"):
        continue
    c = l.rstrip("\n").split("\t")
    try:
        a, s = int(c[0], 16), int(c[1])
    except (ValueError, IndexError):
        continue
    if a < 0x160000:
        blocks.append((a, s))
assert len(blocks) == 66, len(blocks)
hits = pickle.load(open(HERE / "asm_hits_ext.pkl", "rb"))
extra = []
if len(sys.argv) > 1:
    extra = pickle.load(open(sys.argv[1], "rb"))  # (va, len, name)


def pad(b):
    return b in (0x90, 0xCC, 0x66, 0x0F, 0x1F, 0x00, 0x40, 0x44, 0x80, 0x84)


out = {}
for a, s in blocks:
    cov = [None] * s
    inside = []
    for va, n, ob, ln, mk, chk in hits:
        if va < a + s and va + ln > a:
            inside.append((va, n, ln, "asm"))
            for q in range(max(va, a), min(va + ln, a + s)):
                cov[q - a] = n
    for va, ln, n in extra:
        if va < a + s and va + ln > a:
            inside.append((va, n, ln, "c"))
            for q in range(max(va, a), min(va + ln, a + s)):
                if cov[q - a] is None:
                    cov[q - a] = n
    raw = exe.read(a, s)
    # uncovered spans
    spans = []
    q = 0
    while q < s:
        if cov[q] is None:
            r = q
            while r < s and cov[r] is None:
                r += 1
            seg = raw[q:r]
            if not all(pad(x) for x in seg):
                spans.append((a + q, r - q))
            q = r
        else:
            q += 1
    covered = sum(1 for x in cov if x is not None)
    out[a] = dict(size=s, inside=inside, spans=spans, covered=covered)
    print("%08X %6d cov %6d (%5.1f%%) routines %3d  uncovered spans %s" % (
        a, s, covered, 100.0 * covered / s, len(inside), " ".join("%08X+%d" % sp for sp in spans[:6]) + (" ..." if len(spans) > 6 else "")))
pickle.dump((blocks, out), open(HERE / "cover_ext.pkl", "wb"))
