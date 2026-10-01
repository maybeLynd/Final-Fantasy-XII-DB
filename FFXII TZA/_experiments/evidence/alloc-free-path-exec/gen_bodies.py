# EXP-126 body spans: sha256 over shipped bytes for each real body.
# Real bodies executed: the free/release path (PREL 00369860), the
# find-free-below/above pair (AE00/ACE0), the diagnostic emit wrapper
# (F17D2E0) + its object getter (F16D670), _chkstk 00808F10, the memcpy
# wrapper PINIT 004746F0 + its real IAT thunk 00861EBA, plus the full
# EXP-123/125 tree re-executed (A2A0 calls PREL+PINIT for real now).
# Planted hook cells (all the same dormant-rdata family):
#   q[0x8C2D80] ships rdata ptr 0x1CCF02C  (EXP-123 erratum: not 0)
#   q[0x8C2F08] ships rdata ptr 0x1CCECB4  (emit hook)
#   q[0x8C2F70] ships rdata ptr 0x1CCEF16  (a570 out hook)
# Scripted boundary (entry-intercepted, NOT executed):
#   MEMCPY 0x63000000 — VCRUNTIME140!memcpy reached via the real IAT
#   thunk; the import body itself is a disclosed scripted boundary.
import hashlib, json
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
import check

# (name, va, disasm-window hi). Bodies with mid-body int3s (the four
# EXP-123 splice twins) keep their trailing-int3 trimming.
BODIES = [
    ("prel", check.PREL, 0x369C60),
    ("ae00", check.AE00, 0x36AF30),
    ("ace0", check.ACE0, 0x36AE00),
    ("emit", check.EMIT, 0x17D340),
    ("getobj", check.GETOBJ, 0x16D680),
    ("chkstk", check.CHKSTK, 0x808F70),
    ("pinit", check.PINIT, 0x474710),
    ("thunk", check.THUNK, 0x861EC0),
    ("aad0", check.AAD0, 0x36ABE0),
    ("abe0", check.ABE0, 0x36ACD3),
    ("a2a0", check.A2A0, 0x36A490),
    ("c790", check.C790, 0x36C900),
    ("b410", check.B410, 0x36B490),
    ("b490", check.B490, 0x36B4E0),
    ("b4e0", check.B4E0, 0x36B5A0),
    ("b5a0", check.B5A0, 0x36B5F0),
    ("a570", check.A570, 0x36A850),
    ("a850", check.A850, 0x36A9D0),
    ("bc60", check.BC60, 0x36BFE0),
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
    ("flag", check.FLAG, 0x46DFF2),
    ("chkck", check.CHKCK, 0x808C80),
]
SCRIPTED = [check.MEMCPY]
CELL_SITES = {"b670": "0x36b6a8", "b730": "0x36b768",
              "b7f0": "0x36b828", "b8b0": "0x36b8e8"}
OUT_SITE = "0x36a6fa"   # a570's call qword [rip+disp] -> q[0x8C2F70]
PREL_SITES = ["0x369a79", "0x369ab7"]  # prel's two corrupt-path calls
EMIT_SITE = "0x17d328"  # emit's call qword [rip+disp] -> q[0x8C2F08]
THUNK_SITE = "0x861eba"  # jmp qword [rip+disp] -> IAT q[0x8C2A68]


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
                              "src": "q[0x8c2d80] (ships rdata ptr "
                                     "0x1ccf02c; EXP-123 recorded 0 — "
                                     "erratum)",
                              "planted": "0x46dfe0"}]
        if name == "prel":
            b["indirect"] = [{"site": s,
                              "form": "call qword [rip+disp]",
                              "src": "q[0x8c2d80] (ships rdata ptr "
                                     "0x1ccf02c; EXP-123 recorded 0 — "
                                     "erratum)",
                              "planted": "0x46dfe0"}
                             for s in PREL_SITES]
        if name == "a570":
            b["indirect"] = [{"site": OUT_SITE,
                              "form": "call qword [rip+disp]",
                              "src": "q[0x8c2f70] (ships rdata ptr 0x1ccef16)",
                              "planted": "0x46dfe0"}]
        if name == "emit":
            b["indirect"] = [{"site": EMIT_SITE,
                              "form": "call qword [rip+disp]",
                              "src": "q[0x8c2f08] (ships rdata ptr 0x1ccecb4)",
                              "planted": "0x46dfe0"}]
        if name == "thunk":
            b["indirect"] = [{"site": THUNK_SITE,
                              "form": "jmp qword [rip+disp]",
                              "src": "q[0x8c2a68] (IAT "
                                     "VCRUNTIME140.dll!memcpy)",
                              "planted": "0x63000000 (scripted import)"}]
        if name == "chkstk":
            b["indirect"] = [{"site": "0x808f2c",
                              "form": "mov r11, qword gs:[0x10]",
                              "src": "TEB stack limit",
                              "planted": "fake TEB 0x6f000000 via "
                                         "UC_X86_REG_GS_BASE"}]
        print("%s 0x%x span=%d insns=%d" % (name, va, b["span"], b["insns"]))
        real.append(b)
    json.dump({"real": real,
               "scripted": ["0x%x" % v for v in SCRIPTED]},
              open("bodies.json", "w"), indent=1)
    print("scripted:", ["0x%x" % v for v in SCRIPTED])


if __name__ == "__main__":
    main()
