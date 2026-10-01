# EXP-134 body spans: sha256 over shipped bytes for each real body.
# Real bodies executed: the path validator PVAL (00335B60; tolerance
# guard -> cap clamp min(0.8,cap)/max(0.2) -> optional tol/cosf(angB)
# -> MLOAD+MCPY (ROTX(-angB) on the identity axis-bank copy) -> MXVW
# by const dir {0,0,1,1} -> MLOAD+RBUILD (ROTCOL(awrap(angA))) -> MXVW
# -> subsystem record reads +0x108/+0x110/+0x10C/+0x174/+0xE0/+0xF0
# -> three scaled points v50/v40/v60 -> GATE 003357B0 corridor gate
# (scripted, EXP-135) -> mode==3 AGENTQ (scripted) -> flags&8 QWALK
# vs PRED arm -> LQUERY -> DE6A0 dispatcher tail -> ret 0/1/2), the
# matrix-copy+rotate MCPY (00202E90; 4x movups + cosf/sinf via real
# IAT thunks + tail-jmp ROTX), the in-place column (y,z) rotator
# ROTX (00217790; y'=y*c-z*s, z'=y*s+z*c per 16B column), and the
# 5-byte dispatcher tail DE6A0 (0032A6A0; jmp 0026E100 scripted).
# Plus the whole EXP-130/131/132/133 trees re-executed: LQUERY
# (00391410), BMASK (003912E0), DIST (003A1920), CAPT0 (00468D50),
# CAPT1 (00468E50), CPSEG (004691A0), TRIGD (00468580), CAPV
# (00469410), RDEC (0032A6E0), TMS (00861EC0) / TAT2 (00861F02),
# PATHW (0033A3D0), BLKCHK (00335F90), AWRAP (0033CB70), MLOAD
# (00203170), RBUILD (00202F00), ROTCOL (00217880), MXV (00217060),
# MXVW (00202B70), CTHUNK (00861F08), STHUNK (00861F0E), QWALK
# (0033D3E0), WWRAP (00384130), GGRID (00383F10), ROOTL (00383840),
# TTEST (00382D10), ETHUNK (0032A780), ECLASS (0026E300), SEGT
# (00468880), BASE (0020E600), PRED (00335E50), VSUB (00203080),
# VADD (00202B10), VSCALE (00202FE0), NCOPY (00202DE0), NORM
# (00216660), XPROD (00202E10), THUNKF (00861F14) and
# __security_check_cookie CHKCK (00808C40).
# Scripted boundaries (NOT executed):
#   GATE 003357B0 — corridor gate / subsystem+nav-grid walk (944B);
#     entry-intercept, eax planted per case (deferred to EXP-135).
#   DE100 0026E100 — object-root dispatcher; entry-intercept, eax
#     planted per case (reached through the real DE6A0 jmp).
#   AGENTQ 00318CA0 — mode-3 subsystem query; entry-intercept
#     (EXP-132).
#   SQF 0x63040000 — sqrtf via real thunk 00861F14 + IAT q[0x8C2BB8]
#     (EXP-130, import-dir proven), planted host trampoline.
#   AT2 0x630B0000 — atan2f via real thunk 00861F02 + IAT
#     q[0x8C2BD0] (import-dir proven), planted host trampoline.
#   MSET 0x630A0000 — memset via real thunk 00861EC0 + IAT
#     q[0x8C2A60] (import-dir proven), planted host trampoline.
#   FDC 0x63070000 — _fdclass via real IAT q[0x8C2C10] (EXP-131).
#   COS 0x63080000 / SIN 0x63090000 — cosf/sinf via real thunks
#     00861F08/00861F0E + IATs q[0x8C2BA8]/q[0x8C2BB0] (EXP-132).
#   ISN 0x63050000 / FIN 0x63060000 — _isnan/_finite via real IATs
#     q[0x8C2C68]/q[0x8C2C70] (EXP-130, import-dir proven).
# Fixture globals (planted, disclosed): the PVAL stack args cap
# @entry-rsp+0x28 and flags @+0x30, the agent record (+0x108 subsys
# ptr, +0xE0/+0xF0 gate qwords), the subsystem record (+0x10C pred
# radius, +0x110 los radius, +0x174 mode byte), the whole LQUERY
# grid parameter block q/d[0x2AEE060..0x2AEE0B8] (all BSS), the
# nav-record root q[0x209A670] (BSS), q[0x2AEDFB0] root,
# q[0x1F83530] BASE pool, d[0x209A3E0] bit-pair table — plus the
# CRT IAT cells above.
import hashlib, json
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
import check

# (name, va, disasm-window hi). Trailing int3 padding is trimmed.
BODIES = [
    ("pval", check.PVAL, 0x335E60),
    ("mcpy", check.MCPY, 0x202F00),
    ("rotx", check.ROTX, 0x217880),
    ("de6a0", check.DE6A0, 0x32A6B0),
    ("lquery", check.LQUERY, 0x391710),
    ("bmask", check.BMASK, 0x391400),
    ("dist", check.DIST, 0x3A1960),
    ("capt0", check.CAPT0, 0x468E50),
    ("capt1", check.CAPT1, 0x468F90),
    ("cpseg", check.CPSEG, 0x4692E0),
    ("trigd", check.TRIGD, 0x4686D0),
    ("capv", check.CAPV, 0x469560),
    ("rdec", check.RDEC, 0x32A780),
    ("tms", check.TMS, 0x861EC8),
    ("tat2", check.TAT2, 0x861F0A),
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
SCRIPTED = [check.GATE, check.DE100, check.SQF, check.AT2,
            check.MSET, check.FDC, check.COS, check.SIN,
            check.ISN, check.FIN, check.AGENTQ]


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


def _ind(entries):
    return [{"site": s, "form": f, "src": src, "planted": pl}
            for s, f, src, pl in entries]


IND = {
    "pval": [
        ("0x335bdf", "call 0x861f08",
         "cthunk (real) -> IAT q[0x8c2ba8] cosf",
         "0x63080000 (scripted import)"),
        ("0x335bed", "call 0x203170", "mload (real)", None),
        ("0x335c06", "call 0x202e90", "mcpy (real)", None),
        ("0x335c1c", "call 0x202b70", "mxvw (real)", None),
        ("0x335c26", "call 0x203170", "mload (real)", None),
        ("0x335c2f", "call 0x33cb70", "awrap (real)", None),
        ("0x335c41", "call 0x202f00", "rbuild (real)", None),
        ("0x335c55", "call 0x202b70", "mxvw (real)", None),
        ("0x335c76", "call 0x202fe0", "vscale (real)", None),
        ("0x335c88", "call 0x202b10", "vadd (real)", None),
        ("0x335ca2", "call 0x202fe0", "vscale (real)", None),
        ("0x335cb4", "call 0x202b10", "vadd (real)", None),
        ("0x335cea", "call 0x202fe0", "vscale (real)", None),
        ("0x335cfc", "call 0x202b10", "vadd (real)", None),
        ("0x335d37", "call 0x3357b0",
         "gate (scripted entry-intercept, EXP-135)",
         "planted eax per case"),
        ("0x335d61", "call 0x318ca0",
         "agentq (scripted entry-intercept)",
         "planted eax per case"),
        ("0x335d87", "call 0x33d3e0", "qwalk (real)", None),
        ("0x335db0", "call 0x335e50", "pred (real)", None),
        ("0x335dd5", "call 0x391410", "lquery (real)", None),
        ("0x335dfd", "call 0x32a6a0", "de6a0 (real)", None),
        ("0x335e2a", "call 0x808c40",
         "__security_check_cookie (real)", None)],
    "mcpy": [
        ("0x202ec7", "call 0x861f08",
         "cthunk (real) -> IAT q[0x8c2ba8] cosf",
         "0x63080000 (scripted import)"),
        ("0x202ed2", "call 0x861f0e",
         "sthunk (real) -> IAT q[0x8c2bb0] sinf",
         "0x63090000 (scripted import)"),
        ("0x202eef", "jmp 0x217790",
         "rotx (real tail call)", None)],
    "de6a0": [
        ("0x32a6a0", "jmp 0x26e100",
         "de100 (scripted entry-intercept)",
         "planted eax per case")],
    "lquery": [
        ("0x391443", "call 0x383840", "rootl (real)", None),
        ("0x391531", "call 0x3912e0", "bmask (real)", None),
        ("0x391540", "call 0x3a1920", "dist (real)", None),
        ("0x39159b", "call 0x20e600", "base (real)", None),
        ("0x391633", "call 0x468d50", "capt0 (real)", None),
        ("0x391641", "call 0x32a6e0", "rdec (real)", None),
        ("0x391697", "call 0x468e50", "capt1 (real)", None),
        ("0x3916e4", "call 0x808c40",
         "__security_check_cookie (real)", None)],
    "bmask": [
        ("0x39130e", "call 0x861ec0",
         "tms (real) -> IAT q[0x8c2a60] memset",
         "0x630a0000 (scripted import)")],
    "dist": [
        ("0x3a1950", "jmp 0x861f14",
         "thunkf (real tail) -> IAT q[0x8c2bb8] sqrtf",
         "0x63040000 (scripted import)")],
    "capt0": [
        ("0x468dc8", "call 0x4691a0", "cpseg (real)", None),
        ("0x468e28", "call 0x861f14",
         "thunkf (real) -> IAT q[0x8c2bb8] sqrtf",
         "0x63040000 (scripted import)")],
    "capt1": [
        ("0x468e77", "call 0x4691a0", "cpseg (real)", None),
        ("0x468f0f", "call 0x468580", "trigd (real)", None),
        ("0x468f38", "call 0x861f14",
         "thunkf (real) -> IAT q[0x8c2bb8] sqrtf",
         "0x63040000 (scripted import)")],
    "trigd": [
        ("0x468652", "call 0x861f14",
         "thunkf (real) -> IAT q[0x8c2bb8] sqrtf",
         "0x63040000 (scripted import)"),
        ("0x46869a", "call 0x861f14",
         "thunkf (real) -> IAT q[0x8c2bb8] sqrtf",
         "0x63040000 (scripted import)")],
    "rdec": [
        ("0x32a769", "call 0x861f02",
         "tat2 (real) -> IAT q[0x8c2bd0] atan2f",
         "0x630b0000 (scripted import)")],
    "tms": [
        ("0x861ec0", "jmp qword [rip+disp]",
         "IAT q[0x8c2a60] memset", "0x630a0000")],
    "tat2": [
        ("0x861f02", "jmp qword [rip+disp]",
         "IAT q[0x8c2bd0] atan2f", "0x630b0000")],
    "pathw": [
        ("0x33a401", "call 0x33d3e0", "qwalk (real)", None),
        ("0x33a420", "call 0x203080", "vsub (real)", None),
        ("0x33a437", "call 0x202fe0", "vscale (real)", None),
        ("0x33a441", "call 0x203170", "mload (real)", None),
        ("0x33a44e", "call 0x33cb70", "awrap (real)", None),
        ("0x33a460", "call 0x202f00", "rbuild (real)", None),
        ("0x33a474", "call 0x202b70", "mxvw (real)", None),
        ("0x33a486", "call 0x202b10", "vadd (real)", None),
        ("0x33a499", "call 0x33d3e0", "qwalk (real)", None),
        ("0x33a4b1", "call 0x33d3e0", "qwalk (real)", None),
        ("0x33a4c4", "call 0x203170", "mload (real)", None),
        ("0x33a4d1", "call 0x33cb70", "awrap (real)", None),
        ("0x33a4e3", "call 0x202f00", "rbuild (real)", None),
        ("0x33a4f7", "call 0x202b70", "mxvw (real)", None),
        ("0x33a509", "call 0x202b10", "vadd (real)", None),
        ("0x33a51c", "call 0x33d3e0", "qwalk (real)", None),
        ("0x33a534", "call 0x33d3e0", "qwalk (real)", None),
        ("0x33a54f", "call 0x808c40",
         "__security_check_cookie (real)", None)],
    "blkchk": [
        ("0x335fc7", "call 0x335e50", "pred (real)", None),
        ("0x335fda", "call 0x33d3e0", "qwalk (real)", None),
        ("0x336001", "call 0x318ca0",
         "agentq (scripted entry-intercept)",
         "planted eax per case")],
    "rbuild": [
        ("0x202f37", "call 0x861f08",
         "cthunk (real) -> IAT q[0x8c2ba8] cosf",
         "0x63080000 (scripted import)"),
        ("0x202f42", "call 0x861f0e",
         "sthunk (real) -> IAT q[0x8c2bb0] sinf",
         "0x63090000 (scripted import)"),
        ("0x202f5f", "jmp 0x217880",
         "rotcol (real tail call)", None)],
    "mxvw": [
        ("0x202b7e", "call 0x217060", "mxv (real)", None)],
    "cthunk": [
        ("0x861f08", "jmp qword [rip+disp]",
         "IAT q[0x8c2ba8] cosf", "0x63080000")],
    "sthunk": [
        ("0x861f0e", "jmp qword [rip+disp]",
         "IAT q[0x8c2bb0] sinf", "0x63090000")],
}


def main():
    raw, secs = check.load_image()
    real = []
    for name, va, hi in BODIES:
        b = body(raw, secs, va, hi)
        b["name"] = name
        b["indirect"] = _ind(IND.get(name, []))
        print("%s 0x%x span=%d insns=%d" % (name, va, b["span"], b["insns"]))
        real.append(b)
    json.dump({"real": real,
               "scripted": ["0x%x" % v for v in SCRIPTED]},
              open("bodies.json", "w"), indent=1)
    print("scripted:", ["0x%x" % v for v in SCRIPTED])


if __name__ == "__main__":
    main()
