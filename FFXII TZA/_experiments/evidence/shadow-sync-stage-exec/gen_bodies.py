# EXP-113 body spans: sha256 over shipped bytes for each real body.
# Bodies end at ret, or at a direct jmp outside the body window
# (tail calls). PASS/LODC are scripted boundaries, not measured.
import hashlib, json
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
import check

BODIES = [
    ("gate",  check.GATE,  0x428E70),   # tail jmp before shared epilogue
    ("walk",  check.WALK,  None),
    ("sync",  check.SYNC,  0x426413),   # tail-jmp arm before shared ret
    ("v1",    check.V1,    None),
    ("v2",    check.V2,    None),
    ("lods",  check.LODS,  None),
    ("thunk", check.THUNK, 0x521445),   # single jmp, no ret
]
SCRIPTED = [check.LODC, check.PASS]


def body(raw, secs, va, hi):
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    end = hi or va + 0x4000
    insns = []
    for i in md.disasm(check.img_slice(raw, secs, va, end - va), va):
        insns.append(i)
        if hi:
            if i.address + i.size >= hi:
                break
        elif i.mnemonic == "ret":
            break
        elif i.mnemonic == "jmp" and i.op_str.startswith("0x"):
            tgt = int(i.op_str, 16)
            if not (va <= tgt < i.address + i.size + 0x400):
                break
    lo, hi2 = va, insns[-1].address + insns[-1].size
    blob = check.img_slice(raw, secs, lo, hi2 - lo)
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
