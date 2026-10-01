# EXP-123 body spans: sha256 over shipped bytes for each real body.
# Scripted boundaries: A570 0036A570 (mask-gated diagnostic dump on
# the w[+0x3E]!=0 corruption path; entry-intercepted, NOT executed)
# and the shared hook cell q[0x8C2D80] which ships as 0 — the fixture
# plants it to FLAG 0046DFE0 (a real shipped leaf) so the corrupt-path
# indirect call runs real code before the int3 trap.
import hashlib, json
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
import check

# (name, va, disasm-window hi). The twins carry a mid-body int3 on
# the corrupt path, so the span ends at the last insn before the
# TRAILING int3 run, not the first int3.
BODIES = [
    ("bc60", check.BC60, 0x36BFE0),   # BFE0 starts right after
    ("a490", check.A490, 0x36A570),
    ("b210", check.B210, 0x36B2C0),
    ("b2c0", check.B2C0, 0x36B400),
    ("b5f0", check.B5F0, 0x36B670),
    ("b670", check.B670, 0x36B730),
    ("b730", check.B730, 0x36B7F0),
    ("b7f0", check.B7F0, 0x36B8B0),
    ("b8b0", check.B8B0, 0x36B970),
    ("c900", check.C900, 0x36C9D0),
    ("c9d0", check.C9D0, 0x36CACE),
    ("base", check.BASE, 0x20E610),
    ("c620", check.C620, 0x20E630),
]
SCRIPTED = [check.A570]
CELL_SITES = {"b670": "0x36b6a8", "b730": "0x36b768",
              "b7f0": "0x36b828", "b8b0": "0x36b8e8"}


def body(raw, secs, va, hi):
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    insns = list(md.disasm(check.img_rd(raw, secs, va, hi - va), va))
    end = len(insns)
    while end > 0 and insns[end - 1].mnemonic == "int3":
        end -= 1
    insns = insns[:end]
    hi2 = insns[-1].address + insns[-1].size
    blob = check.img_rd(raw, secs, va, hi2 - va)
    return {"va": "0x%x" % va, "lo": "0x%x" % va, "hi": "0x%x" % hi2,
            "span": hi2 - va, "insns": len(insns), "cov": 1.0,
            "sha256": hashlib.sha256(blob).hexdigest(), "indirect": []}


def main():
    raw, secs = check.load_image()
    real = []
    for name, va, hi in BODIES:
        b = body(raw, secs, va, hi)
        b["name"] = name
        if name in CELL_SITES:
            b["indirect"] = [{"site": CELL_SITES[name],
                              "form": "call qword [rip+disp]",
                              "src": "q[0x8c2d80] (ships 0)",
                              "planted": "0x46dfe0"}]
        print("%s 0x%x span=%d insns=%d" % (name, va, b["span"], b["insns"]))
        real.append(b)
    json.dump({"real": real,
               "scripted": ["0x%x" % v for v in SCRIPTED]},
              open("bodies.json", "w"), indent=1)
    print("scripted:", len(SCRIPTED))


if __name__ == "__main__":
    main()
