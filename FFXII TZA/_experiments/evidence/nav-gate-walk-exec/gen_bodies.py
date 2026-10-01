# EXP-135 body spans: sha256 over shipped bytes for each real body.
# Real bodies executed: the corridor gate GATE (003357B0; ctx idx
# b[r9+0xEA9] -> GTAB pool entry -> d[+8] handle -> MABE flag gate
# (&0x10 -> MABESP scripted) -> self -> flags&0x20 skip else GCHK
# validity chain -> ordered point-vs-segment compare on posA/posB
# -> GPT point query or GSEG segment query (wrapper: collector ->
# GFILT) -> per-handle loop: OBJD decode, self/exclusion skip, e68
# class-pair filter, flags&0x40 mode-3 pre-filter (O3FW/OSUB/O1F2),
# flags&2/&4/&0x10/&8 LHELP arms, ctx-mode==3 accept-path O3FW/O1F2
# y-cap, OPA/OPB accept -> esi/r12d counters -> ret 0/1/2), its
# leaves GTAB (00236820; d[idx*0xF50+8] pool read), MABE (0031ABE0;
# b[MABEF]&0x10 gate), GCHK (002EA7F0; +0x18/+0xC0/+0x14F/+0x138/
# +0xF0/+8 guard chain -> OVF -> b4==3 arm), OCLS (00263C20; class
# byte b[+0xE]&0xF), LHELP (00335760; q[+0x698] -> b[p+5] -> OCLS
# class -> 0/1/2), the record writers S3W (002FB500; O3FW+O2FW+O1F
# then d[out+4]=0) and S2W (002FB340; O3FW + maxss(O2FW) ->
# d[out+4]=0, d[out+0x10]=max), the capsule predicates CDST
# (00469060; TRIGD+rad vs dxz2 setae), CDZ0 (00468D10; rad+t.f10 vs
# dxz2 seta), CF90 (00468F90; CPSEG+TRIGD+sqrtf seta), the
# collectors GPC (00391A30; point+rad cell walk -> S3W/CDST or
# S2W/CDZ0 emit) and GSC (00391D90; segment bbox bmask + per-record
# S3W/CF90 or S2W/strip+d2 emit), the wrappers GPT (00391D10;
# GPC(tmp)+GFILT) / GSEG (003920F0; GSC(tmp)+GFILT), the handle
# filter GFILT (003911D0; OBJD + flags&2/&4(&0x698+OF60)/&8(GCHK)
# -> out[] emit), and the 5-byte OSUB thunk (0032A790; jmp
# 0026E350 scripted). Plus the whole EXP-130/131/132/133/134 trees
# re-executed: PVAL (00335B60; now drives REAL GATE), LQUERY
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
# (00216660), XPROD (00202E10), THUNKF (00861F14), MCPY (00202E90),
# ROTX (00217790), DE6A0 (0032A6A0) and __security_check_cookie
# CHKCK (00808C40).
# Scripted boundaries (NOT executed):
#   OBJD 00263E30 — handle -> object decode; entry-intercept,
#     planted eax per case.
#   O3FW 002646C0 / O2FW 00265090 / O1F 00265200 / O1F2 00263940 /
#     O1F3 00265830 — subsystem record field accessors;
#     entry-intercepts, planted writes/eax/xmm0 per case.
#   OPA 00314EB0 / OPB 00313F80 / OF60 00313F60 / OVF 002E9FE0 /
#     OSUB 0026E350 — object/subsystem predicates; entry-intercepts,
#     planted eax per case (OSUB reached via real thunk 0032A790).
#   MABESP 003588B0 — MABE slow-path subsystem handle resolve;
#     entry-intercept, planted eax per case.
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
# q[0x1F83530] BASE pool, d[0x209A3E0] bit-pair table, the GATE
# fixture block — GTAB pool q[0x209A500]/d[0x209A508] count,
# b[0x2089340] MABE flag, collector count d[0x2AEE0BC] + handle
# array q[0x2AEE0C0..], ctx object CTXA (+0xEA9 idx, +0x1F4 mode,
# +0x10/+0x698/+0xE68 qwords), GCHK records (+0xC0 chain, +0x138
# chain, +0xF0 float, +8/+4 bytes), candidate objects CANDA/CTXB —
# plus the CRT IAT cells above.
import hashlib, json
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
import check

# (name, va, disasm-window hi). Trailing int3 padding is trimmed.
BODIES = [
    ("gate", check.GATE, 0x335B60),
    ("gtab", check.GTAB, 0x236850),
    ("mabe", check.MABE, 0x31AC00),
    ("gchk", check.GCHK, 0x2EA870),
    ("ocls", check.OCLS, 0x263C30),
    ("lhelp", check.LHELP, 0x3357B0),
    ("s3w", check.S3W, 0x2FB570),
    ("s2w", check.S2W, 0x2FB3B0),
    ("cdst", check.CDST, 0x4690B0),
    ("cdz0", check.CDZ0, 0x468D50),
    ("cf90", check.CF90, 0x469060),
    ("gpc", check.GPC, 0x391D10),
    ("gsc", check.GSC, 0x3920F0),
    ("gpt", check.GPT, 0x391D90),
    ("gseg", check.GSEG, 0x392180),
    ("gfilt", check.GFILT, 0x3912E0),
    ("othunk", 0x32A790, 0x32A7A0),
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
SCRIPTED = [check.OBJD, check.O3FW, check.O2FW, check.O1F,
            check.O1F2, check.O1F3, check.OPA, check.OPB,
            check.OF60, check.OVF, check.OSUB, check.MABESP,
            check.DE100, check.AGENTQ, check.SQF, check.AT2,
            check.MSET, check.FDC, check.COS, check.SIN,
            check.ISN, check.FIN]


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
    "gate": [
        ("0x3357f9", "call 0x236820", "gtab (real)", None),
        ("0x335801", "call 0x31abe0", "mabe (real)", None),
        ("0x33581b", "call 0x2ea7f0", "gchk (real)", None),
        ("0x335892", "call 0x391d10", "gpt (real)", None),
        ("0x3358bc", "call 0x3920f0", "gseg (real)", None),
        ("0x3358e5", "call 0x263e30",
         "objd (scripted entry-intercept)",
         "planted eax per case"),
        ("0x33599b", "call 0x2646c0",
         "o3fw (scripted entry-intercept)",
         "planted writes per case"),
        ("0x3359c8", "call 0x32a790",
         "othunk (real) -> osub (scripted entry-intercept)",
         "planted eax per case"),
        ("0x3359db", "call 0x263940",
         "o1f2 (scripted entry-intercept)",
         "planted xmm0 per case"),
        ("0x3359f9", "call 0x335760", "lhelp (real)", None),
        ("0x335a0b", "call 0x335760", "lhelp (real)", None),
        ("0x335a17", "call 0x335760", "lhelp (real)", None),
        ("0x335a29", "call 0x335760", "lhelp (real)", None),
        ("0x335a36", "call 0x265830",
         "o1f3 (scripted entry-intercept)",
         "planted xmm0 per case"),
        ("0x335a6e", "call 0x335760", "lhelp (real)", None),
        ("0x335a78", "call 0x335760", "lhelp (real)", None),
        ("0x335ab8", "call 0x2646c0",
         "o3fw (scripted entry-intercept)",
         "planted writes per case"),
        ("0x335ac2", "call 0x263940",
         "o1f2 (scripted entry-intercept)",
         "planted xmm0 per case"),
        ("0x335ae8", "call 0x314eb0",
         "opa (scripted entry-intercept)",
         "planted eax per case"),
        ("0x335b02", "call 0x313f80",
         "opb (scripted entry-intercept)",
         "planted eax per case"),
        ("0x335b43", "call 0x808c40",
         "__security_check_cookie (real)", None)],
    "mabe": [
        ("0x31abe7", "jne 0x3588b0",
         "mabesp (scripted entry-intercept)",
         "planted eax per case")],
    "gchk": [
        ("0x2ea844", "call 0x2e9fe0",
         "ovf (scripted entry-intercept)",
         "planted eax per case")],
    "lhelp": [
        ("0x33577f", "call 0x263c20", "ocls (real)", None)],
    "s3w": [
        ("0x2fb523", "call 0x2646c0",
         "o3fw (scripted entry-intercept)",
         "planted writes per case"),
        ("0x2fb533", "call 0x265090",
         "o2fw (scripted entry-intercept)",
         "planted writes per case"),
        ("0x2fb53b", "call 0x265200",
         "o1f (scripted entry-intercept)",
         "planted xmm0 per case")],
    "s2w": [
        ("0x2fb363", "call 0x2646c0",
         "o3fw (scripted entry-intercept)",
         "planted writes per case"),
        ("0x2fb375", "call 0x265090",
         "o2fw (scripted entry-intercept)",
         "planted writes per case")],
    "cdst": [
        ("0x469070", "call 0x468580", "trigd (real)", None)],
    "cf90": [
        ("0x468fc5", "call 0x4691a0", "cpseg (real)", None),
        ("0x469003", "call 0x468580", "trigd (real)", None),
        ("0x46902c", "call 0x861f14",
         "thunkf (real) -> IAT q[0x8c2bb8] sqrtf",
         "0x63040000 (scripted import)")],
    "gpc": [
        ("0x391aab", "call 0x861ec0",
         "tms (real) -> IAT q[0x8c2a60] memset",
         "0x630a0000 (scripted import)"),
        ("0x391c4c", "call 0x2fb500", "s3w (real)", None),
        ("0x391c5b", "call 0x469060", "cdst (real)", None),
        ("0x391c67", "call 0x2fb340", "s2w (real)", None),
        ("0x391c76", "call 0x468d10", "cdz0 (real)", None),
        ("0x391cf1", "call 0x808c40",
         "__security_check_cookie (real)", None)],
    "gsc": [
        ("0x391e01", "call 0x861ec0",
         "tms (real) -> IAT q[0x8c2a60] memset",
         "0x630a0000 (scripted import)"),
        ("0x391ebe", "call 0x3912e0", "bmask (real)", None),
        ("0x391ecd", "call 0x3a1920", "dist (real)", None),
        ("0x391f8f", "call 0x2fb500", "s3w (real)", None),
        ("0x391f9d", "call 0x468f90", "cf90 (real)", None),
        ("0x391fb4", "call 0x2fb340", "s2w (real)", None),
        ("0x392022", "call 0x3a1920", "dist (real)", None),
        ("0x3920d3", "call 0x808c40",
         "__security_check_cookie (real)", None)],
    "gpt": [
        ("0x391d49", "call 0x391a30", "gpc (real)", None),
        ("0x391d5f", "call 0x3911d0", "gfilt (real)", None),
        ("0x391d6f", "call 0x808c40",
         "__security_check_cookie (real)", None)],
    "gseg": [
        ("0x392129", "call 0x391d90", "gsc (real)", None),
        ("0x39213f", "call 0x3911d0", "gfilt (real)", None),
        ("0x39214f", "call 0x808c40",
         "__security_check_cookie (real)", None)],
    "gfilt": [
        ("0x391228", "call 0x263e30",
         "objd (scripted entry-intercept)",
         "planted eax per case"),
        ("0x39125d", "call 0x313f60",
         "of60 (scripted entry-intercept)",
         "planted eax per case"),
        ("0x39126f", "call 0x2ea7f0", "gchk (real)", None)],
    "othunk": [
        ("0x32a790", "jmp 0x26e350",
         "osub (scripted entry-intercept)",
         "planted eax per case")],
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
        ("0x335d37", "call 0x3357b0", "gate (real)", None),
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
    "ethunk": [
        ("0x32a780", "jmp 0x26e300",
         "eclass (real)", None)],
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
