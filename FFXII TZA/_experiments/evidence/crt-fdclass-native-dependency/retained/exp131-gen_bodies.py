# EXP-131 body spans: sha256 over shipped bytes for each real body.
# Real bodies executed: the nav-mesh segment walk QWALK (0033D3E0),
# the {x,z}-pair wrapper WWRAP (00384130), the grid point query
# GGRID (00383F10), the root leaf ROOTL (00383840) on planted BSS
# q[0x2AEDFB0], the point-in-triangle test TTEST (00382D10), the
# thunk ETHUNK (0032A780 -> 0026E300), the edge-class bit query
# ECLASS (0026E300) on shipped rdata d[0x915760] + planted BSS
# d[0x209A3E0], the segment-orientation test SEGT (00468880), the
# BASE decoder BASE (0020E600) on planted BSS q[0x1F83530], plus
# VSUB (00203080) / XPROD (00202E10) inside SEGT and the real
# __security_check_cookie (00808C40, used by both QWALK and SEGT).
# Scripted boundaries (NOT executed):
#   FDC 0x63070000 — api-ms-win-crt-math-l1-1-0.dll!_fdclass via
#     real IAT cell q[0x8C2C10] (ships unbound record 0x1CCECCE...
#     verified against the PE import directory); the harness plants
#     the IAT cell to a host-computed trampoline implementing the
#     exact CRT float-class semantics (NaN 2, +-inf 1, finite -1,
#     denormal -2, zero 0).
# Fixture globals (planted, disclosed): q[0x2AEDFB0] root,
# q[0x1F83530] BASE pool, d[0x209A3E0] bit-pair table — all BSS.
import hashlib, json
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
import check

# (name, va, disasm-window hi). Trailing int3 padding is trimmed.
BODIES = [
    ("qwalk", check.QWALK, 0x33D660),
    ("wwrap", check.WWRAP, 0x384160),
    ("ggrid", check.GGRID, 0x384130),
    ("rootl", check.ROOTL, 0x383848),
    ("ttest", check.TTEST, 0x382EA0),
    ("ethunk", check.ETHUNK, 0x32A790),
    ("eclass", check.ECLASS, 0x26E350),
    ("segt", check.SEGT, 0x468A70),
    ("base", check.BASE, 0x20E610),
    ("vsub", check.VSUB, 0x2030E0),
    ("xprod", check.XPROD, 0x202E90),
    ("chkck", check.CHKCK, 0x808C61),
]
SCRIPTED = [check.FDC]


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
        if name == "qwalk":
            b["indirect"] = [
                {"site": s, "form": f, "src": src, "planted": pl}
                for s, f, src, pl in [
                    ("0x33d428", "call 0x384130",
                     "wwrap (real)", None),
                    ("0x33d45c", "call 0x384130",
                     "wwrap (real)", None),
                    ("0x33d496", "call 0x383840",
                     "rootl (real)", None),
                    ("0x33d4d5", "call 0x20e600",
                     "base (real)", None),
                    ("0x33d4f6", "call 0x20e600",
                     "base (real)", None),
                    ("0x33d503", "call 0x32a780",
                     "ethunk (real) -> eclass (real)", None),
                    ("0x33d518", "call 0x20e600",
                     "base (real)", None),
                    ("0x33d53a", "call 0x20e600",
                     "base (real)", None),
                    ("0x33d546", "call 0x20e600",
                     "base (real)", None),
                    ("0x33d561", "call 0x20e600",
                     "base (real)", None),
                    ("0x33d57d", "call 0x20e600",
                     "base (real)", None),
                    ("0x33d58a", "call 0x20e600",
                     "base (real)", None),
                    ("0x33d5a5", "call 0x20e600",
                     "base (real)", None),
                    ("0x33d5d2", "call 0x468880",
                     "segt (real)", None),
                    ("0x33d63c", "call 0x808c40",
                     "__security_check_cookie (real)", None)]]
        if name == "wwrap":
            b["indirect"] = [{"site": "0x38414e",
                              "form": "call 0x383f10",
                              "src": "ggrid (real)", "planted": None}]
        if name == "ggrid":
            b["indirect"] = [
                {"site": s, "form": f, "src": src, "planted": pl}
                for s, f, src, pl in [
                    ("0x383f26", "call 0x20e600",
                     "base (real)", None),
                    ("0x383f31", "call 0x20e600",
                     "base (real)", None),
                    ("0x383f3e", "call qword [rip+disp]",
                     "IAT q[0x8c2c10] (api-ms-win-crt-math-l1-1-0."
                     "dll!_fdclass; ships unbound record)",
                     "0x63070000 (scripted import)"),
                    ("0x383f54", "call qword [rip+disp]",
                     "IAT q[0x8c2c10] (_fdclass, second arg)",
                     "0x63070000 (scripted import)"),
                    ("0x383fd6", "call 0x20e600",
                     "base (real)", None),
                    ("0x384070", "call 0x20e600",
                     "base (real)", None),
                    ("0x38409a", "call 0x20e600",
                     "base (real)", None),
                    ("0x3840b8", "call 0x20e600",
                     "base (real)", None),
                    ("0x3840c4", "call 0x382d10",
                     "ttest (real)", None),
                    ("0x3840dd", "call 0x20e600",
                     "base (real)", None)]]
        if name == "ttest":
            b["indirect"] = [
                {"site": "0x%x" % s, "form": "call 0x20e600",
                 "src": "base (real)", "planted": None}
                for s in (0x382D6E, 0x382D89, 0x382DAC,
                          0x382DC7, 0x382DEA, 0x382E0B)]
        if name == "ethunk":
            b["indirect"] = [{"site": "0x32a780",
                              "form": "jmp 0x26e300",
                              "src": "eclass (real)",
                              "planted": None}]
        if name == "segt":
            b["indirect"] = [
                {"site": s, "form": f, "src": src, "planted": pl}
                for s, f, src, pl in [
                    ("0x46893b", "call 0x203080",
                     "vsub (real)", None),
                    ("0x46894c", "call 0x203080",
                     "vsub (real)", None),
                    ("0x46895d", "call 0x203080",
                     "vsub (real)", None),
                    ("0x468983", "call 0x202e10",
                     "xprod (real)", None),
                    ("0x468994", "call 0x202e10",
                     "xprod (real)", None),
                    ("0x4689ca", "call 0x203080",
                     "vsub (real)", None),
                    ("0x4689db", "call 0x203080",
                     "vsub (real)", None),
                    ("0x4689ec", "call 0x203080",
                     "vsub (real)", None),
                    ("0x468a12", "call 0x202e10",
                     "xprod (real)", None),
                    ("0x468a23", "call 0x202e10",
                     "xprod (real)", None),
                    ("0x468a5a", "call 0x808c40",
                     "__security_check_cookie (real)", None)]]
        if name == "chkck":
            b["indirect"] = [{"site": "0x808c5c",
                              "form": "jmp 0x809654",
                              "src": "__report_gsfailure (unreached "
                                     "in fixture)",
                              "planted": None}]
        print("%s 0x%x span=%d insns=%d" % (name, va, b["span"], b["insns"]))
        real.append(b)
    json.dump({"real": real,
               "scripted": ["0x%x" % v for v in SCRIPTED]},
              open("bodies.json", "w"), indent=1)
    print("scripted:", ["0x%x" % v for v in SCRIPTED])


if __name__ == "__main__":
    main()
