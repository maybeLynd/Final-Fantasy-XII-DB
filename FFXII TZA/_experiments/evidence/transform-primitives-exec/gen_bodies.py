# EXP-115 body spans: sha256 over shipped bytes for each real body.
# Each body ends at its own ret; trailing int3 padding excluded.
# __report_gsfailure is a disclosed fault-token boundary, not measured.
import hashlib, json
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
import check

BODIES = [
    ("tpt",   check.TPT,   0x00399110),   # next function
    ("ct",    check.CT,    0x00397B50),   # next function
    ("chkck", check.CHKCK, 0x00808C90),   # next function
]
SCRIPTED = [check.GSFAIL]


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
