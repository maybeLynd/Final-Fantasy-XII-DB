import sys, os, struct
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rawref import Img, sec
from capstone.x86 import X86_OP_IMM
img = Img.load()
_R = {}
def pdata_roots():
    if _R: return _R
    po = img.off(img.base + img.exc_rva)
    ents = []
    for i in range(img.exc_size // 12):
        b, e, u = struct.unpack_from("<III", img.d, po + i * 12)
        ui = img.off(img.base + u); fl = img.d[ui] >> 3; n = img.d[ui + 2]; r = b
        if fl & 4:
            r = struct.unpack_from("<I", img.d, ui + 4 + ((n + 1) & ~1) * 2)[0]
        ents.append((b + img.base, e + img.base, r + img.base))
    first = dict((b, r) for b, e, r in ents)
    for b, e, r in ents:
        k = 0
        while r in first and first[r] != r and k < 16:
            r = first[r]; k += 1
        _R.setdefault(r, []).append((b, e))
    return _R
def closure(root, skip=()):
    frags = pdata_roots(); tva, tvs = sec(img, ".text")[0], sec(img, ".text")[1]
    seen, st, ind = set(), [root], 0
    while st:
        f = st.pop()
        if f in seen or not (tva <= f < tva + tvs): continue
        seen.add(f)
        parts = frags.get(f) or ([img.pdata(f)] if img.pdata(f) else None)
        if parts is None:
            end = f
            for ci in img.cs.disasm(img.read(f, 0x800), f):
                end = ci.address + ci.size
                if ci.mnemonic in ("ret", "int3", "jmp"): break
            parts = [(f, end)]
        lo, hi = min(p[0] for p in parts), max(p[1] for p in parts)
        for s, e in parts:
            for ci in img.cs.disasm(img.read(s, e - s), s):
                if ci.mnemonic in ("call", "jmp"):
                    op = ci.operands[0]
                    if op.type == X86_OP_IMM:
                        if (ci.mnemonic == "call" or not (lo <= op.imm < hi)) and ci.address not in skip:
                            st.append(op.imm)
                    else: ind += 1
    return seen, ind
if __name__ == "__main__":
    for a in sys.argv[2:]:
        s, ind = closure(int(sys.argv[1], 16))
        print(sys.argv[1], "->", a, int(a, 16) in s, "size", len(s), "indirect", ind)
