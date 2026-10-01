# EXP-119 body spans: sha256 over shipped bytes for each real body.
# Each body ends at its last ret/jmp before int3 padding / next
# function. 0036B130 (RES's nonzero-mode resolver) is the disclosed
# scripted boundary — executed real in EXP-084.
import hashlib, json
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
import check

BODIES = [
    ("t51t", check.T51T, 0x0051B9F0),   # int3 padding after jmp
    ("t51",  check.T51,  0x0051F2D0),   # int3 padding after ret
    ("e20",  check.E20,  0x00370E30),   # int3 padding after jmp
    ("res",  check.RES,  0x003AB860),   # int3 padding after ret
    ("base", check.BASE, 0x0020E610),   # next function
]
SCRIPTED = [check.HRES]


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
