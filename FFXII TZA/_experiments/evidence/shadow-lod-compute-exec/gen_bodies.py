# EXP-114 body spans: sha256 over shipped bytes for each real body.
# The six pool siblings are contiguous; each body's extent ends at the
# int3 padding before the next function (trailing padding excluded).
# RES2/GATE/sqrtf are scripted boundaries, not measured.
import hashlib, json
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
import check

BODIES = [
    ("lodc",  check.LODC,  check.ACC),    # 0x3B5980..pad..0x3B5C00
    ("acc",   check.ACC,   check.CPY),
    ("cpy",   check.CPY,   check.INIT),
    ("init",  check.INIT,  check.FSYNC),
    ("fsync", check.FSYNC, check.CLRE),
    ("clre",  check.CLRE,  0x003B6020),   # PASS is the scripted tail
    ("leaf",  check.LEAF,  0x0036DD90),   # next sibling leaf
]
SCRIPTED = [0x00421FF0, 0x003E6F70, 0x00861F14]


def body(raw, secs, va, hi):
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    insns = [i for i in md.disasm(check.img_rd(raw, secs, va, hi - va), va)]
    while insns and insns[-1].mnemonic == "int3":
        insns.pop()
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
