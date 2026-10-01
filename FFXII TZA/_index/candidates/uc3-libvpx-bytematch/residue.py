"""Print every byte span of each head block not covered by an exact asm hit, with its disassembly."""
import pickle, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from coff import Exe

HERE = Path(__file__).parent
exe = Exe()
cs = Cs(CS_ARCH_X86, CS_MODE_64)
blocks, out = pickle.load(open(HERE / "cover.pkl", "rb"))
hits = pickle.load(open(HERE / "asm_hits.pkl", "rb"))
iv = sorted((h[0], h[0] + h[3]) for h in hits)
res = {}
for a, s in blocks:
    cov = bytearray(s)
    for x, y in iv:
        for q in range(max(x, a), min(y, a + s)):
            cov[q - a] = 1
    raw = exe.read(a, s)
    spans = []
    q = 0
    while q < s:
        if not cov[q]:
            r = q
            while r < s and not cov[r]:
                r += 1
            spans.append((a + q, raw[q:r]))
            q = r
        else:
            q += 1
    res[a] = spans
    for va, b in spans:
        ins = [(i.mnemonic + " " + i.op_str).strip() for i in cs.disasm(b, va)]
        allnop = all(i.startswith("nop") or i.startswith("int3") for i in ins) and sum(len(x) for x in []) == 0
        dec = sum(i.size for i in cs.disasm(b, va))
        kind = "PAD" if (allnop and dec == len(b)) or set(b) <= {0xCC} else "CODE?"
        print("%08X blk %08X %4d B %s  %s" % (va, a, len(b), kind, " | ".join(ins[:8]) if kind != "PAD" else b.hex()[:40]))
pickle.dump(res, open(HERE / "residue.pkl", "wb"))
