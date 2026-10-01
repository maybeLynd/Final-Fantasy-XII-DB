# EXP-129 body spans: sha256 over shipped bytes for each real body.
# Real bodies executed: the DB70 wrapper (0040DB70), the two-stage
# vec3 normalize (B430 0040B430), the cross-product helper
# (XPROD 00202E10), the real sqrtf IAT thunk (00861F14), and
# __security_check_cookie (CHKCK 00808C40). RGSF 00809654
# (__report_gsfailure) is reached for real only under the
# cookie-corrupting mutant m-b430-xor; it faults deeper inside its own
# call tree (call qword through an unplanted cell) — disclosed, partial.
# Scripted boundary (entry-intercepted, NOT executed):
#   SQF 0x63040000 — api-ms-win-crt-math-l1-1-0.dll!sqrtf reached via
#   the real 00861F14 thunk + the real IAT slot q[0x8C2BB8] (ships the
#   unbound hint record 0x1CCED52); planted to the trampoline. The host
#   computes the same CRT sqrtf (correctly-rounded f32) — the import
#   body itself is a disclosed scripted boundary.
import hashlib, json
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
import check

# (name, va, disasm-window hi). Trailing int3 padding is trimmed.
BODIES = [
    ("db70", check.DB70, 0x40DBB0),
    ("b430", check.B430, 0x40B5D0),
    ("xprod", check.XPROD, 0x202E90),
    ("thunkf", check.THUNKF, 0x861F1A),
    ("chkck", check.CHKCK, 0x808C61),
    ("rgsf", 0x809654, 0x809725),
]
SCRIPTED = [check.SQF]
SQF_SITES = ["0x40b495", "0x40b55c"]  # b430's two call 0x861f14 sites


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
        if name == "b430":
            b["indirect"] = [
                {"site": s, "form": "call 0x861f14",
                 "src": "IAT q[0x8c2bb8] via real thunk "
                        "(ships unbound record 0x1cced52; "
                        "api-ms-win-crt-math-l1-1-0.dll!sqrtf)",
                 "planted": "0x63040000 (scripted import)"}
                for s in SQF_SITES] + [
                {"site": "0x40b522", "form": "call 0x202e10",
                 "src": "xprod (real)", "planted": None},
                {"site": "0x40b5a3", "form": "call 0x808c40",
                 "src": "__security_check_cookie (real)",
                 "planted": None}]
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
                                     "reached under m-b430-xor)",
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
