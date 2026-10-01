# EXP-132 body spans: sha256 over shipped bytes for each real body.
# Real bodies executed: the path-width probe PATHW (0033A3D0; five
# real QWALK calls around two rotate-offset rounds), the corridor-
# blocked check BLKCHK (00335F90; real PRED over the real QWALK
# tree — closing EXP-130's last scripted seam — plus the mode-3
# scripted AGENTQ boundary), the angle wrapper AWRAP (0033CB70),
# the const-matrix loader MLOAD (00203170), the rotation-matrix
# builder RBUILD (00202F00; tail-jmp ROTCOL), the in-place column
# rotation ROTCOL (00217880), the matrix*vector MXV (00217060),
# the frame-temp wrapper MXVW (00202B70), and the cosf/sinf IAT
# thunks CTHUNK (00861F08) / STHUNK (00861F0E); plus the whole
# EXP-130/EXP-131 trees re-executed: QWALK (0033D3E0), WWRAP
# (00384130), GGRID (00383F10), ROOTL (00383840), TTEST (00382D10),
# ETHUNK (0032A780), ECLASS (0026E300), SEGT (00468880), BASE
# (0020E600), PRED (00335E50), VSUB (00203080), VADD (00202B10),
# VSCALE (00202FE0), NCOPY (00202DE0), NORM (00216660), XPROD
# (00202E10), the sqrtf thunk THUNKF (00861F14) and
# __security_check_cookie CHKCK (00808C40).
# Scripted boundaries (NOT executed):
#   COS 0x63080000 — cosf via real thunk 00861F08 + IAT q[0x8C2BA8]
#     (api-ms-win-crt-math-l1-1-0.dll!cosf; import-dir proven); the
#     harness plants the IAT cell to a host trampoline.
#   SIN 0x63090000 — sinf via real thunk 00861F0E + IAT q[0x8C2BB0]
#     (same DLL; import-dir proven), planted host trampoline.
#   FDC 0x63070000 — _fdclass via real IAT q[0x8C2C10] (EXP-131).
#   SQF 0x63040000 — sqrtf via real thunk 00861F14 + IAT q[0x8C2BB8]
#     (EXP-130).
#   ISN 0x63050000 / FIN 0x63060000 — _isnan/_finite via real IATs
#     q[0x8C2C68]/q[0x8C2C70] (EXP-130, import-dir proven).
#   AGENTQ 00318CA0 — mode-3 subsystem query; entry-intercept with
#     per-case planted eax (its callee chain enters an object tree).
# Fixture globals (planted, disclosed): q[0x2AEDFB0] root,
# q[0x1F83530] BASE pool, d[0x209A3E0] bit-pair table — all BSS —
# plus the five CRT IAT cells above.
import hashlib, json
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
import check

# (name, va, disasm-window hi). Trailing int3 padding is trimmed.
BODIES = [
    ("pathw", check.PATHW, 0x33A570),
    ("blkchk", check.BLKCHK, 0x336040),
    ("awrap", check.AWRAP, 0x33CBF0),
    ("mload", check.MLOAD, 0x2031A0),
    ("rbuild", check.RBUILD, 0x202F70),
    ("rotcol", check.ROTCOL, 0x217970),
    ("mxv", check.MXV, 0x217150),
    ("mxvw", check.MXVW, 0x202B90),
    ("cthunk", 0x861F08, 0x861F10),
    ("sthunk", 0x861F0E, 0x861F16),
    ("qwalk", check.QWALK, 0x33D660),
    ("wwrap", check.WWRAP, 0x384160),
    ("ggrid", check.GGRID, 0x384130),
    ("rootl", check.ROOTL, 0x383848),
    ("ttest", check.TTEST, 0x382EA0),
    ("ethunk", check.ETHUNK, 0x32A790),
    ("eclass", check.ECLASS, 0x26E350),
    ("segt", check.SEGT, 0x468A70),
    ("base", check.BASE, 0x20E610),
    ("pred", check.PRED, 0x335F90),
    ("vsub", check.VSUB, 0x2030E0),
    ("vadd", check.VADD, 0x202B70),
    ("vscale", check.VSCALE, 0x203030),
    ("ncopy", check.NCOPY, 0x202E10),
    ("norm", check.NORM, 0x216720),
    ("xprod", check.XPROD, 0x202E90),
    ("thunkf", check.THUNKF, 0x861F1C),
    ("chkck", check.CHKCK, 0x808C61),
]
SCRIPTED = [check.COS, check.SIN, check.FDC, check.SQF, check.ISN,
            check.FIN, check.AGENTQ]


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
        if name == "pathw":
            b["indirect"] = [
                {"site": s, "form": f, "src": src, "planted": pl}
                for s, f, src, pl in [
                    ("0x33a401", "call 0x33d3e0",
                     "qwalk (real)", None),
                    ("0x33a420", "call 0x203080",
                     "vsub (real)", None),
                    ("0x33a437", "call 0x202fe0",
                     "vscale (real)", None),
                    ("0x33a441", "call 0x203170",
                     "mload (real)", None),
                    ("0x33a44e", "call 0x33cb70",
                     "awrap (real)", None),
                    ("0x33a460", "call 0x202f00",
                     "rbuild (real)", None),
                    ("0x33a474", "call 0x202b70",
                     "mxvw (real)", None),
                    ("0x33a486", "call 0x202b10",
                     "vadd (real)", None),
                    ("0x33a499", "call 0x33d3e0",
                     "qwalk (real)", None),
                    ("0x33a4b1", "call 0x33d3e0",
                     "qwalk (real)", None),
                    ("0x33a4c4", "call 0x203170",
                     "mload (real)", None),
                    ("0x33a4d1", "call 0x33cb70",
                     "awrap (real)", None),
                    ("0x33a4e3", "call 0x202f00",
                     "rbuild (real)", None),
                    ("0x33a4f7", "call 0x202b70",
                     "mxvw (real)", None),
                    ("0x33a509", "call 0x202b10",
                     "vadd (real)", None),
                    ("0x33a51c", "call 0x33d3e0",
                     "qwalk (real)", None),
                    ("0x33a534", "call 0x33d3e0",
                     "qwalk (real)", None),
                    ("0x33a54f", "call 0x808c40",
                     "__security_check_cookie (real)", None)]]
        if name == "blkchk":
            b["indirect"] = [
                {"site": s, "form": f, "src": src, "planted": pl}
                for s, f, src, pl in [
                    ("0x335fc7", "call 0x335e50",
                     "pred (real)", None),
                    ("0x335fda", "call 0x33d3e0",
                     "qwalk (real)", None),
                    ("0x336001", "call 0x318ca0",
                     "agentq (scripted entry-intercept)",
                     "planted eax per case")]]
        if name == "rbuild":
            b["indirect"] = [
                {"site": s, "form": f, "src": src, "planted": pl}
                for s, f, src, pl in [
                    ("0x202f37", "call 0x861f08",
                     "cthunk (real) -> IAT q[0x8c2ba8] cosf",
                     "0x63080000 (scripted import)"),
                    ("0x202f42", "call 0x861f0e",
                     "sthunk (real) -> IAT q[0x8c2bb0] sinf",
                     "0x63090000 (scripted import)"),
                    ("0x202f5f", "jmp 0x217880",
                     "rotcol (real tail call)", None)]]
        if name == "mxvw":
            b["indirect"] = [{"site": "0x202b7e",
                              "form": "call 0x217060",
                              "src": "mxv (real)", "planted": None}]
        if name == "cthunk":
            b["indirect"] = [{"site": "0x861f08",
                              "form": "jmp qword [rip+disp]",
                              "src": "IAT q[0x8c2ba8] cosf",
                              "planted": "0x63080000"}]
        if name == "sthunk":
            b["indirect"] = [{"site": "0x861f0e",
                              "form": "jmp qword [rip+disp]",
                              "src": "IAT q[0x8c2bb0] sinf",
                              "planted": "0x63090000"}]
        print("%s 0x%x span=%d insns=%d" % (name, va, b["span"], b["insns"]))
        real.append(b)
    json.dump({"real": real,
               "scripted": ["0x%x" % v for v in SCRIPTED]},
              open("bodies.json", "w"), indent=1)
    print("scripted:", ["0x%x" % v for v in SCRIPTED])


if __name__ == "__main__":
    main()
