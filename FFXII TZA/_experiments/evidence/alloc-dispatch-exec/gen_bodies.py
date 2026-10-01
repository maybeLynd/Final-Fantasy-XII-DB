# EXP-122 body spans: sha256 over shipped bytes for each real body.
# Scripted boundaries: BC60/AAD0/ABE0 (entry tokens, planted returns;
# NOT executed). The `call rax` indirect at 0x36C03B is NOT stubbed —
# the fixture plants q[desc+0xA0] = FLAG 0046DFE0, a real shipped leaf.
import hashlib, json
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
import check

BODIES = [
    ("a100", check.A100, 0x0036A181),   # int3 padding after ret
    ("bfe0", check.BFE0, 0x0036C0F0),   # int3 padding after ret
    ("c620", check.C620, 0x0020E630),   # int3 padding after ret
]
SCRIPTED = [check.BC60, check.AAD0, check.ABE0]


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
    # the indirect call site is real but its target is runtime-planted
    for b in real:
        if b["name"] == "bfe0":
            b["indirect"] = [{"site": "0x36c03b", "form": "call rax",
                              "src": "q[desc+0xA0]",
                              "planted": "0x46dfe0"}]
    json.dump({"real": real,
               "scripted": ["0x%x" % v for v in SCRIPTED]},
              open("bodies.json", "w"), indent=1)
    print("scripted:", len(SCRIPTED))


if __name__ == "__main__":
    main()
