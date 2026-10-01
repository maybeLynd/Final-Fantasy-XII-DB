# EXP-130 body spans: sha256 over shipped bytes for each real body.
# Real bodies executed: the corridor-width probe PRED (00335E50),
# the vec4 helpers VSUB (00203080) / VADD (00202B10) / VSCALE
# (00202FE0), the copy+normalize wrapper NCOPY (00202DE0), the
# normalize-or-zero NORM (00216660), the cross product XPROD
# (00202E10, re-executed from EXP-129), the real sqrtf IAT thunk
# (00861F14) and __security_check_cookie (00808C40). RGSF 00809654
# executes for real only under the cookie-corrupting mutant
# m-pred-cook; it faults deeper through an unplanted cell —
# disclosed, partial.
# Scripted boundaries (NOT executed):
#   Q33 0x33d3e0 — nav-grid point query; entry-intercepted, eax
#     planted per case (deep tree: 00384130->00383F10 grid lookup
#     w/ _fdclass IAT 0x8c2c10, 00383840 root q[0x5ADFB0],
#     0x382d10/0x32a780 walkers) — follow-on package.
#   SQF 0x63040000 — api-ms-win-crt-math-l1-1-0.dll!sqrtf via real
#     thunk 00861F14 + real IAT q[0x8C2BB8] (unbound hint 0x1CCED52).
#   ISN 0x63050000 — _isnan via real IAT q[0x8C2C68] (0x1CCECD8).
#   FIN 0x63060000 — _finite via real IAT q[0x8C2C70] (0x1CCECCE).
#   All three host-computed, correctly-rounded/predicate-exact.
import hashlib, json
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
import check

# (name, va, disasm-window hi). Trailing int3 padding is trimmed.
BODIES = [
    ("pred", check.PRED, 0x335F90),
    ("vsub", check.VSUB, 0x2030E0),
    ("vadd", check.VADD, 0x202B70),
    ("vscale", check.VSCALE, 0x203030),
    ("ncopy", check.NCOPY, 0x202E10),
    ("norm", check.NORM, 0x216720),
    ("xprod", check.XPROD, 0x202E90),
    ("thunkf", check.THUNKF, 0x861F1A),
    ("chkck", check.CHKCK, 0x808C61),
    ("rgsf", 0x809654, 0x809725),
]
SCRIPTED = [check.Q33, check.SQF, check.ISN, check.FIN]


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
        if name == "pred":
            b["indirect"] = [
                {"site": s, "form": f,
                 "src": src, "planted": pl}
                for s, f, src, pl in [
                    ("0x335e86", "call 0x203080",
                     "vsub (real)", None),
                    ("0x335e9e", "call 0x202de0",
                     "ncopy (real) -> norm (real)", None),
                    ("0x335eb4", "call 0x202e10",
                     "xprod (real)", None),
                    ("0x335ec6", "call 0x202fe0",
                     "vscale (real)", None),
                    ("0x335ed8", "call 0x202b10",
                     "vadd (real)", None),
                    ("0x335eea", "call 0x202b10",
                     "vadd (real)", None),
                    ("0x335f1a", "call 0x203080",
                     "vsub (real)", None),
                    ("0x335f2c", "call 0x203080",
                     "vsub (real)", None),
                    ("0x335efc", "call 0x33d3e0",
                     "nav-grid query (scripted boundary)",
                     "eax planted per case"),
                    ("0x335f3e", "call 0x33d3e0",
                     "nav-grid query (scripted boundary)",
                     "eax planted per case"),
                    ("0x335f55", "call 0x33d3e0",
                     "nav-grid query (scripted boundary)",
                     "eax planted per case"),
                    ("0x335f6c", "call 0x808c40",
                     "__security_check_cookie (real)", None)]]
        if name == "ncopy":
            b["indirect"] = [{"site": "0x202def",
                              "form": "call 0x216660",
                              "src": "norm (real)", "planted": None}]
        if name == "norm":
            b["indirect"] = [
                {"site": "0x21669b", "form": "call qword [rip+disp]",
                 "src": "IAT q[0x8c2c68] (api-ms-win-crt-math-l1-1-0."
                        "dll!_isnan; ships unbound record 0x1ccecd8)",
                 "planted": "0x63050000 (scripted import)"},
                {"site": "0x2166a8", "form": "call qword [rip+disp]",
                 "src": "IAT q[0x8c2c70] (api-ms-win-crt-math-l1-1-0."
                        "dll!_finite; ships unbound record 0x1ccecce)",
                 "planted": "0x63060000 (scripted import)"},
                {"site": "0x2166be", "form": "call 0x861f14",
                 "src": "sqrtf thunk (real) -> IAT q[0x8c2bb8]",
                 "planted": "0x63040000 (scripted import)"}]
        if name == "thunkf":
            b["indirect"] = [{"site": "0x861f14",
                              "form": "jmp qword [rip+disp]",
                              "src": "q[0x8c2bb8] (IAT "
                                     "api-ms-win-crt-math-l1-1-0.dll!"
                                     "sqrtf)",
                              "planted": "0x63040000 (scripted import)"}]
        if name == "chkck":
            b["indirect"] = [{"site": "0x808c5c",
                              "form": "jmp 0x809654",
                              "src": "__report_gsfailure (real; "
                                     "reached under m-pred-cook)",
                              "planted": None}]
        if name == "rgsf":
            b["note"] = "partial replay: only the head executes under " \
                        "the cookie-fail mutant; the call at 0x809662 " \
                        "faults deeper through an unplanted cell"
            b["indirect"] = [{"site": "0x809662",
                              "form": "call 0x87af34",
                              "src": "feature-check helper; faults "
                                     "deeper through unplanted cell "
                                     "under the mutant",
                              "planted": None},
                             {"site": "0x809679",
                              "form": "call 0x809848",
                              "src": "report/terminate helper "
                                     "(unreached in fixture)",
                              "planted": None}]
        print("%s 0x%x span=%d insns=%d" % (name, va, b["span"], b["insns"]))
        real.append(b)
    json.dump({"real": real,
               "scripted": ["0x%x" % v for v in SCRIPTED]},
              open("bodies.json", "w"), indent=1)
    print("scripted:", ["0x%x" % v for v in SCRIPTED])


if __name__ == "__main__":
    main()
