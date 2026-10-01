# EXP-121 body spans: sha256 over shipped bytes for each real body.
# Scripted boundaries: E070 + EA30 (the deep poll-loop callees — entry
# tokens only, planted returns; NOT executed).
import hashlib, json
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
import check

BODIES = [
    ("c140", check.C140, 0x0036C1D0),   # next function
    ("c1d0", check.C1D0, 0x0036C1F0),   # jmp tail -> C1F0
    ("c1f0", check.C1F0, 0x0036C290),   # int3 padding after ret
    ("e400", check.E400, 0x0032E450),   # next function — no pad
    ("de70", check.DE70, 0x0046DFE0),   # jmp thunk -> T2D
    ("t2d",  check.T2D,  0x002DF980),   # int3 padding after ret
    ("clr",  check.CLR,  0x00512F40),   # int3 padding after ret
    ("e520", check.E520, 0x0032E620),   # int3 padding after ret
    ("flag", check.FLAG, 0x0046E000),   # next function
]
SCRIPTED = [check.E070, check.EA30]


def body(raw, secs, va, hi):
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    insns = []
    for i in md.disasm(check.img_rd(raw, secs, va, hi - va), va):
        if i.mnemonic == "int3":
            break
        insns.append(i)
    lo, hi2 = va, insns[-1].address + insns[-1].size
    blob = check.img_rd(raw, secs, lo, hi2 - lo)
    return {"va": "0x%x" % va, "lo": "0x%x" % lo, "hi": "0x%x" % hi2,
            "span": hi2 - lo, "insns": len(insns), "cov": 1.0,
            "sha256": hashlib.sha256(blob).hexdigest(), "indirect": []}


def main():
    raw, secs = check.load_image()
    real = []
    for name, va, hi in BODIES:
        b = body(raw, secs, va, hi)
        b["name"] = name
        print("%s 0x%x span=%d insns=%d" % (name, va, b["span"], b["insns"]))
        real.append(b)
    json.dump({"real": real,
               "scripted": ["0x%x" % v for v in SCRIPTED]},
              open("bodies.json", "w"), indent=1)
    print("scripted:", len(SCRIPTED))


if __name__ == "__main__":
    main()
