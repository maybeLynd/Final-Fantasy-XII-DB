# EXP-116 body spans: sha256 over shipped bytes for each real body.
# INSERT_C/INSERT_K end at their last ret; trailing int3 padding
# excluded.  Each init thunk is exactly 0x20 bytes ending in
# `jmp 00808B90` — all 240 were executed in .CRT-table order.
# The atexit registrar 00808B90 is a disclosed scripted boundary,
# not measured.
import hashlib, json
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
import check

BODIES = [
    ("insert-c", check.INSERT_C, 0x00879600),   # next function
    ("insert-k", check.INSERT_K, 0x00876D10),   # int3 pad boundary
]
BODIES += [("tk%02d" % i, tv, tv + 0x20)
           for i, tv in enumerate(check.KTHUNKS)]
BODIES += [("tc%03d" % i, tv, tv + 0x20)
           for i, tv in enumerate(check.CTHUNKS)]
SCRIPTED = [check.ATE]


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
        real.append(b)
    print("inserts:")
    for b in real[:2]:
        print("  %s 0x%x span=%d insns=%d" % (
            b["name"], b["va"] and int(b["va"], 16), b["span"],
            b["insns"]))
    print("thunks: %d key + %d channel = %d x 0x20" % (
        len(check.KTHUNKS), len(check.CTHUNKS),
        len(check.KTHUNKS) + len(check.CTHUNKS)))
    assert all(b["span"] == 0x20 for b in real[2:])
    json.dump({"real": real,
               "scripted": ["0x%x" % v for v in SCRIPTED]},
              open("bodies.json", "w"), indent=1)
    print("scripted:", len(SCRIPTED))


if __name__ == "__main__":
    main()
