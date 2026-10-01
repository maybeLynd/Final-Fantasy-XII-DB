"""textcache.py - linear decode of all of .text (every .pdata range, plus each gap between ranges decoded from its first
non-int3 byte, so leaf functions without unwind data are included). Writes a TSV (va, size, mnemonic, op_str, owner)
to the path given (scratch, not the review folder). owner = the .pdata root VA, or 'gap:<first VA of the gap run>'.
Used for image-wide text sweeps by the review scripts (load with load()).
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ind as I  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

DEFAULT = r"C:\Users\Kristian\AppData\Local\Temp\claude\C--Users-Kristian-source-repos\0aca3c35-4792-4b08-9423-be894cfa848b\scratchpad\SWE2-AUDIT-SPEC\text_decode.tsv"


def build(path):
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    n, v, vs, p, rs = I.TEXT[0]
    end = v + min(vs, rs)
    ranges = sorted((I.IB + a, I.IB + b) for a, b, u in I.PD)
    with open(path, "w", encoding="utf-8", newline="\n") as fo:
        cur = v
        for a, b in ranges + [(end, end)]:
            if a > cur:  # gap
                o = I.off(cur)
                blob = I.raw[o:o + (a - cur)]
                k = 0
                while k < len(blob) and blob[k] in (0xCC, 0x90):
                    k += 1
                if k < len(blob):
                    g = cur + k
                    for (addr, size, mn, ops) in md.disasm_lite(blob[k:], g):
                        fo.write("%X\t%d\t%s\t%s\tgap:%X\n" % (addr, size, mn, ops, g))
            if b > a:
                o = I.off(a)
                root = I.ROOT_OF[a]
                for (addr, size, mn, ops) in md.disasm_lite(I.raw[o:o + (b - a)], a):
                    fo.write("%X\t%d\t%s\t%s\t%X\n" % (addr, size, mn, ops, root))
            cur = max(cur, b)


def load(path=DEFAULT):
    out = []
    with open(path, encoding="utf-8") as fi:
        for line in fi:
            a, s, m, o, w = line.rstrip("\n").split("\t")
            out.append((int(a, 16), int(s), m, o, w))
    return out


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else DEFAULT)
