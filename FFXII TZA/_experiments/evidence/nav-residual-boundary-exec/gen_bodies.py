# EXP-138 body spans: sha256 over shipped bytes for each real body.
# EXP-138 promotes the five residual scripted boundaries to real
# bodies: EF2B0 (002EF2B0; init-ptr accessor -> EF640 +0x200),
# F4F0 (002324F0; 3-slot edge predicate, argmin|t-0.5| over
# crossy<-1e-4 candidates), F430 (0022F430; waypoint walker:
# cell resolve -> bank-loop callback scan -> grid re-resolve ->
# D0D0 scripted region query, repeat), EB0 (00381EB0;
# point-in-unit-shape via inverse-matrix transform + type
# 0/1/2 test), D5A0 (003DA5A0; capsule distance: two
# anisotropic XZ metrics + f64 sqrt). Plus their real subtree:
# EF640 (002EF640; rax=0x2164280), E500 (0026E500; CLST root
# selector), D4B0 (0022D4B0; F430's planted callback: edge
# range scan, CLST mask merge, e6d0/cf50/fa0 candidates),
# E6D0 (0022E6D0; signed projected distance), CF50
# (0022CF50; triangle winding test over 0x908DE8), FA0
# (00380FA0; seg-vs-shape distance dispatch), the unit-shape
# primitives P1AC0 (00381AC0; sphere), P1630 (00381630;
# cylinder), P1450 (00381450; box), D2020 (00382020;
# unit-cylinder point test), plane helpers BF60 (0046BF60) /
# BFA0 (0046BFA0), A1D30 (003A1D30; sqrtf(|x|) via f64),
# DA730 (003DA730; rotated anisotropic XZ metric), and the
# real import thunks TACF (00861F56; -> acosf) / TSQD
# (00861F5C; -> sqrt f64).
# EXP-137 promotes the EXP-136 scripted leaf family to real bodies:
# N7C20 (00377C20; EF2 word -> T2AD bitfield lookup), N48F0
# (003148F0; EF2B0 init-ptr -> d[+0x1044] signed clamp), N63FF0
# (00263FF0; indexed T3B address calc), DAE00 (003DAE00; null-safe
# 3-dword copy), N33050 (00233050; staggered-grid cell resolve),
# N30A40 (00230A40; CLST mask-mux predicate), N31890 (00231890;
# edge y-projection -> xmm0), N31820 (00231820; y-projection store
# variant), N31900 (00231900; best-edge scan -> ax), N33110
# (00233110; cell edge scan -> w[out+0x52]), N315E0 (002315E0;
# ctx -> F430 -> sx16 word), N31400 (00231400; point-free
# dispatcher: cell -> edge scan -> flag ctx -> N2F830), N2F830
# (0022F830; flag-bit cell dispatch, call q[ctx] -> N2F8B0),
# N2F8B0 (0022F8B0; sub-record point-test loop -> EB0), N4E10
# (00314E10; material blend selector -> xmm0), N14F50 (00314F50;
# pair compare / capsule path -> t/outp + writeback).
# EXP-136 promoted the EXP-135 scripted leaf family to real bodies:
# OBJD (00263E30; rax=q[h+0x30]), A6A0 (002646A0; ->q[+0xC0]->
# q[+0x138] chain), O3FW (002646C0; v=b[+3]>>5: v1 copy d[qB8+0/4/8],
# v3 copy + (b[+0x107]&1: addss f40/44/48), else zero outs), O2FW
# (00265090; (b[+3]&0xE0)==0x60 -> DA710(qB8+0x50)), DA710 (003DA710;
# d[rc]->[rdx], d[rc+4]->[r8]), O1F (00265200; v1 f[qB8+0x38], v3
# f[qB8+0xA8]), O1F2 (00263940; v1 f[qB8+0x68], v3 fC0*f24), O1F3
# (00265830; 0x60 -> f[q[qB8+0xF0]+0x24]), OVF (002E9FE0; 0x60 ->
# c0/d164/b10/b11 flag walk), OPA (00314EB0; c0->138 chain class
# +0x119 compare), OPB (00313F80; A6A0 pair -> N14F50 scripted ->
# opt f[outp]), OF60 (00313F60; jmp N7C20 scripted), OSUB (0026E350;
# roots -> N31900 -> N31820 scripted), MABESP (003588B0; bank/sel/gen
# handle decode -> N63FF0 table -> arr entry + w16 bank check), DE100
# (0026E100; arg reshuffle -> N31400 scripted), AGENTQ (00318CA0;
# q[0x2EC1378] -> N315E0 -> cwde). EXP-135 real bodies re-executed:
# the corridor gate GATE (003357B0; ctx idx
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
# -> out[] emit), and the 5-byte OSUB thunk (0032A790; jmp 0026E350,
# now real). Plus the whole EXP-130/131/132/133/134 trees
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
#   D0D0 0022D0D0 — F430's region query; entry-intercept,
#     planted eax per case (d0d0rets) + optional out16
#     (d0d0o).
#   SQD 0x630C0000 — sqrt (f64) via real thunk 00861F5C + IAT
#     q[0x8C2C60] (import-dir proven), planted host trampoline.
#   ACF 0x630D0000 — acosf via real thunk 00861F56 + IAT
#     q[0x8C2C78] (import-dir proven), planted host trampoline.
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
    ("objd", check.OBJD, 0x263E38),
    ("a6a0", check.A6A0, 0x2646C0),
    ("o3fw", check.O3FW, 0x264750),
    ("o2fw", check.O2FW, 0x2650B0),
    ("da710", 0x3DA710, 0x3DA728),
    ("o1f", check.O1F, 0x265240),
    ("o1f2", check.O1F2, 0x263980),
    ("o1f3", check.O1F3, 0x265860),
    ("ovf", check.OVF, 0x2EA030),
    ("opa", check.OPA, 0x314F30),
    ("opb", check.OPB, 0x314000),
    ("of60", check.OF60, 0x313F68),
    ("osub", check.OSUB, 0x26E3C0),
    ("mabesp", check.MABESP, 0x358940),
    ("de100", check.DE100, 0x26E130),
    ("agentq", check.AGENTQ, 0x318CD0),
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
    ("n7c20", check.N7C20, 0x377C70),
    ("n48f0", check.N48F0, 0x314910),
    ("n63ff0", check.N63FF0, 0x264010),
    ("dae00", check.DAE00, 0x3DAE40),
    ("n33050", check.N33050, 0x2330E0),
    ("n30a40", check.N30A40, 0x230B60),
    ("n31890", check.N31890, 0x231900),
    ("n31820", check.N31820, 0x231890),
    ("n31900", check.N31900, 0x231A90),
    ("n33110", check.N33110, 0x233240),
    ("n315e0", check.N315E0, 0x231690),
    ("n31400", check.N31400, 0x2315E0),
    ("n2f830", check.N2F830, 0x22F8B0),
    ("n2f8b0", check.N2F8B0, 0x22F9C0),
    ("n4e10", check.N4E10, 0x314EB0),
    ("n14f50", check.N14F50, 0x315390),
    ("e500", 0x26E500, 0x26E530),
    ("ef640", 0x2EF640, 0x2EF650),
    ("ef2b0", check.EF2B0, 0x2EF2D0),
    ("a1d30", 0x3A1D30, 0x3A1D50),
    ("da730", 0x3DA730, 0x3DA830),
    ("bf60", 0x46BF60, 0x46BFA0),
    ("bfa0", 0x46BFA0, 0x46C0D0),
    ("d2020", 0x382020, 0x3820C0),
    ("e6d0", 0x22E6D0, 0x22E7D0),
    ("cf50", 0x22CF50, 0x22D0D0),
    ("d4b0", 0x22D4B0, 0x22D7DF),
    ("f430", check.F430, 0x22F830),
    ("fa0", 0x380FA0, 0x3810B0),
    ("p1ac0", 0x381AC0, 0x381D90),
    ("p1630", 0x381630, 0x381AC0),
    ("p1450", 0x381450, 0x381630),
    ("eb0", check.EB0, 0x382020),
    ("f4f0", check.F4F0, 0x232760),
    ("d5a0", check.D5A0, 0x3DA6A0),
    ("tacf", check.TACF, 0x861F5C),
    ("tsqd", check.TSQD, 0x861F64),
]
SCRIPTED = [check.D0D0, check.SQD, check.ACF, check.SQF,
            check.AT2, check.MSET, check.FDC, check.COS,
            check.SIN, check.ISN, check.FIN]


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
        ("0x3358e5", "call 0x263e30", "objd (real)", None),
        ("0x33599b", "call 0x2646c0", "o3fw (real)", None),
        ("0x3359c8", "call 0x32a790",
         "othunk (real) -> osub (real)", None),
        ("0x3359db", "call 0x263940", "o1f2 (real)", None),
        ("0x3359f9", "call 0x335760", "lhelp (real)", None),
        ("0x335a0b", "call 0x335760", "lhelp (real)", None),
        ("0x335a17", "call 0x335760", "lhelp (real)", None),
        ("0x335a29", "call 0x335760", "lhelp (real)", None),
        ("0x335a36", "call 0x265830", "o1f3 (real)", None),
        ("0x335a6e", "call 0x335760", "lhelp (real)", None),
        ("0x335a78", "call 0x335760", "lhelp (real)", None),
        ("0x335ab8", "call 0x2646c0", "o3fw (real)", None),
        ("0x335ac2", "call 0x263940", "o1f2 (real)", None),
        ("0x335ae8", "call 0x314eb0", "opa (real)", None),
        ("0x335b02", "call 0x313f80", "opb (real)", None),
        ("0x335b43", "call 0x808c40",
         "__security_check_cookie (real)", None)],
    "mabe": [
        ("0x31abe7", "jne 0x3588b0", "mabesp (real)", None)],
    "gchk": [
        ("0x2ea844", "call 0x2e9fe0", "ovf (real)", None)],
    "lhelp": [
        ("0x33577f", "call 0x263c20", "ocls (real)", None)],
    "s3w": [
        ("0x2fb523", "call 0x2646c0", "o3fw (real)", None),
        ("0x2fb533", "call 0x265090", "o2fw (real)", None),
        ("0x2fb53b", "call 0x265200", "o1f (real)", None)],
    "s2w": [
        ("0x2fb363", "call 0x2646c0", "o3fw (real)", None),
        ("0x2fb375", "call 0x265090", "o2fw (real)", None)],
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
        ("0x391228", "call 0x263e30", "objd (real)", None),
        ("0x39125d", "call 0x313f60",
         "of60 (real) -> n7c20 (real)", None),
        ("0x39126f", "call 0x2ea7f0", "gchk (real)", None)],
    "othunk": [
        ("0x32a790", "jmp 0x26e350", "osub (real)", None)],
    "o2fw": [
        ("0x2650a5", "jmp 0x3da710", "da710 (real tail)", None)],
    "opb": [
        ("0x313f95", "call 0x2646a0", "a6a0 (real)", None),
        ("0x313fa0", "call 0x2646a0", "a6a0 (real)", None),
        ("0x313fbd", "call 0x314f50", "n14f50 (real)", None)],
    "of60": [
        ("0x313f60", "jmp 0x377c20", "n7c20 (real)", None)],
    "osub": [
        ("0x26e380", "call 0x231900", "n31900 (real)", None),
        ("0x26e394", "call 0x231820", "n31820 (real)", None)],
    "mabesp": [
        ("0x3588e6", "call 0x263ff0", "n63ff0 (real)", None)],
    "de100": [
        ("0x26e11e", "jmp 0x231400", "n31400 (real)", None)],
    "agentq": [
        ("0x318cb9", "call 0x2315e0", "n315e0 (real)", None)],
    "n7c20": [
        ("0x377c24", "call 0x3148f0", "n48f0 (real)", None)],
    "n48f0": [
        ("0x3148f4", "call 0x2ef2b0", "ef2b0 (real)", None)],
    "n31900": [
        ("0x231936", "call 0x233050", "n33050 (real)", None),
        ("0x2319fc", "call 0x2324f0", "f4f0 (real)", None),
        ("0x231a0f", "call 0x231890", "n31890 (real)", None),
        ("0x231a6c", "call 0x808c40",
         "__security_check_cookie (real)", None)],
    "n33110": [
        ("0x2331c0", "call 0x230a40", "n30a40 (real)", None),
        ("0x2331d4", "call 0x2324f0", "f4f0 (real)", None),
        ("0x23321d", "call 0x808c40",
         "__security_check_cookie (real)", None)],
    "n315e0": [
        ("0x231652", "call 0x22f430", "f430 (real)", None),
        ("0x231667", "call 0x808c40",
         "__security_check_cookie (real)", None),
        ("0x231683", "call 0x808c40",
         "__security_check_cookie (real)", None)],
    "n31400": [
        ("0x231435", "call 0x233050", "n33050 (real)", None),
        ("0x231449", "call 0x233110", "n33110 (real)", None),
        ("0x2315a9", "call 0x22f830", "n2f830 (real)", None),
        ("0x2315c2", "call 0x808c40",
         "__security_check_cookie (real)", None)],
    "n2f830": [
        ("0x22f894", "call qword ptr [rdi]",
         "n2f8b0 (real, indirect dispatch)", None)],
    "n2f8b0": [
        ("0x22f968", "call 0x381eb0", "eb0 (real)", None)],
    "n14f50": [
        ("0x315091", "call 0x3dae00", "dae00 (real)", None),
        ("0x31509e", "call 0x3dae00", "dae00 (real)", None),
        ("0x315152", "call 0x3da5a0", "d5a0 (real)", None),
        ("0x3151ab", "call 0x808c40",
         "__security_check_cookie (real)", None),
        ("0x3151f9", "call 0x202de0", "ncopy (real)", None),
        ("0x31523c", "call 0x314e10", "n4e10 (real)", None)],
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
        ("0x335d61", "call 0x318ca0", "agentq (real)", None),
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
        ("0x32a6a0", "jmp 0x26e100", "de100 (real)", None)],
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
        ("0x336001", "call 0x318ca0", "agentq (real)", None)],
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
    "ef2b0": [
        ("0x2ef2b4", "call 0x2ef640", "ef640 (real)", None)],
    "a1d30": [
        ("0x3a1d42", "jmp 0x861f14",
         "thunkf (real tail) -> IAT q[0x8c2bb8] sqrtf",
         "0x63040000 (scripted import)")],
    "da730": [
        ("0x3da775", "call 0x861f08",
         "cthunk (real) -> IAT q[0x8c2ba8] cosf",
         "0x63080000 (scripted import)"),
        ("0x3da780", "call 0x861f0e",
         "sthunk (real) -> IAT q[0x8c2bb0] sinf",
         "0x63090000 (scripted import)")],
    "bfa0": [
        ("0x46c03c", "call 0x861f14",
         "thunkf (real) -> IAT q[0x8c2bb8] sqrtf",
         "0x63040000 (scripted import)")],
    "d2020": [
        ("0x382059", "call 0x861f14",
         "thunkf (real) -> IAT q[0x8c2bb8] sqrtf",
         "0x63040000 (scripted import)")],
    "e6d0": [
        ("0x22e753", "call 0x861f14",
         "thunkf (real) -> IAT q[0x8c2bb8] sqrtf",
         "0x63040000 (scripted import)")],
    "cf50": [
        ("0x22d055", "call 0x202e10", "xprod (real)", None),
        ("0x22d0a9", "call 0x808c40",
         "__security_check_cookie (real)", None)],
    "d4b0": [
        ("0x22d5d2", "call 0x380fa0", "fa0 (real)", None),
        ("0x22d6b6", "call 0x22e6d0", "e6d0 (real)", None),
        ("0x22d73a", "call 0x22cf50", "cf50 (real)", None),
        ("0x22d7cb", "call 0x808c40",
         "__security_check_cookie (real)", None)],
    "f430": [
        ("0x22f461", "call 0x26e500", "e500 (real)", None),
        ("0x22f486", "call 0x233050", "n33050 (real)", None),
        ("0x22f4ad", "call 0x233050", "n33050 (real)", None),
        ("0x22f570", "call 0x861f14",
         "thunkf (real) -> IAT q[0x8c2bb8] sqrtf",
         "0x63040000 (scripted import)"),
        ("0x22f5bb", "call qword ptr [rbx + 0x28]",
         "d4b0 (real, indirect via ctx+0x28)", None),
        ("0x22f611", "call 0x861f14",
         "thunkf (real) -> IAT q[0x8c2bb8] sqrtf",
         "0x63040000 (scripted import)"),
        ("0x22f729", "call 0x22d0d0",
         "d0d0 (scripted entry-intercept)",
         "planted eax/out16 per case"),
        ("0x22f808", "call 0x808c40",
         "__security_check_cookie (real)", None)],
    "fa0": [
        ("0x380fcf", "call 0x202b70", "mxvw (real)", None),
        ("0x380fe0", "call 0x202b70", "mxvw (real)", None),
        ("0x381009", "call 0x381450", "p1450 (real)", None),
        ("0x38101f", "call 0x381630", "p1630 (real)", None),
        ("0x381035", "call 0x381ac0", "p1ac0 (real)", None),
        ("0x38104a", "call 0x202b70", "mxvw (real)", None),
        ("0x381080", "call 0x861f14",
         "thunkf (real) -> IAT q[0x8c2bb8] sqrtf",
         "0x63040000 (scripted import)"),
        ("0x381097", "call 0x808c40",
         "__security_check_cookie (real)", None)],
    "p1ac0": [
        ("0x381b63", "call 0x861f14",
         "thunkf (real) -> IAT q[0x8c2bb8] sqrtf",
         "0x63040000 (scripted import)"),
        ("0x381bc7", "call 0x46bf60", "bf60 (real)", None),
        ("0x381c4b", "call 0x861f14",
         "thunkf (real) -> IAT q[0x8c2bb8] sqrtf",
         "0x63040000 (scripted import)"),
        ("0x381c71", "call 0x861f14",
         "thunkf (real) -> IAT q[0x8c2bb8] sqrtf",
         "0x63040000 (scripted import)"),
        ("0x381ca7", "call 0x861f14",
         "thunkf (real) -> IAT q[0x8c2bb8] sqrtf",
         "0x63040000 (scripted import)"),
        ("0x381ce5", "call 0x861f56",
         "tacf (real) -> IAT q[0x8c2c78] acosf",
         "0x630d0000 (scripted import)"),
        ("0x381cea", "call 0x861f0e",
         "sthunk (real) -> IAT q[0x8c2bb0] sinf",
         "0x63090000 (scripted import)"),
        ("0x381d36", "call 0x808c40",
         "__security_check_cookie (real)", None)],
    "p1630": [
        ("0x3816e8", "call 0x861f14",
         "thunkf (real) -> IAT q[0x8c2bb8] sqrtf",
         "0x63040000 (scripted import)"),
        ("0x381728", "call 0x46bfa0", "bfa0 (real)", None),
        ("0x381793", "call 0x861f14",
         "thunkf (real) -> IAT q[0x8c2bb8] sqrtf",
         "0x63040000 (scripted import)"),
        ("0x38180e", "call 0x46bfa0", "bfa0 (real)", None),
        ("0x381879", "call 0x861f14",
         "thunkf (real) -> IAT q[0x8c2bb8] sqrtf",
         "0x63040000 (scripted import)"),
        ("0x3818fd", "call 0x861f14",
         "thunkf (real) -> IAT q[0x8c2bb8] sqrtf",
         "0x63040000 (scripted import)"),
        ("0x381959", "call 0x46bf60", "bf60 (real)", None),
        ("0x38196f", "call 0x861f14",
         "thunkf (real) -> IAT q[0x8c2bb8] sqrtf",
         "0x63040000 (scripted import)"),
        ("0x3819ba", "call 0x861f14",
         "thunkf (real) -> IAT q[0x8c2bb8] sqrtf",
         "0x63040000 (scripted import)"),
        ("0x3819c5", "call 0x382020", "d2020 (real)", None),
        ("0x3819d1", "call 0x382020", "d2020 (real)", None),
        ("0x3819f7", "call 0x861f56",
         "tacf (real) -> IAT q[0x8c2c78] acosf",
         "0x630d0000 (scripted import)"),
        ("0x3819fc", "call 0x861f0e",
         "sthunk (real) -> IAT q[0x8c2bb0] sinf",
         "0x63090000 (scripted import)"),
        ("0x381a80", "call 0x808c40",
         "__security_check_cookie (real)", None)],
    "p1450": [
        ("0x3814e2", "call 0x861f14",
         "thunkf (real) -> IAT q[0x8c2bb8] sqrtf",
         "0x63040000 (scripted import)"),
        ("0x38151f", "call 0x46bfa0", "bfa0 (real)", None),
        ("0x3815fb", "call 0x808c40",
         "__security_check_cookie (real)", None)],
    "eb0": [
        ("0x381edb", "call 0x202b70", "mxvw (real)", None),
        ("0x381fa3", "call 0x861f14",
         "thunkf (real) -> IAT q[0x8c2bb8] sqrtf",
         "0x63040000 (scripted import)"),
        ("0x381ff4", "call 0x861f14",
         "thunkf (real) -> IAT q[0x8c2bb8] sqrtf",
         "0x63040000 (scripted import)"),
        ("0x381f5f", "call 0x808c40",
         "__security_check_cookie (real)", None),
        ("0x381fbf", "call 0x808c40",
         "__security_check_cookie (real)", None),
        ("0x382012", "call 0x808c40",
         "__security_check_cookie (real)", None)],
    "f4f0": [
        ("0x232646", "call 0x861f14",
         "thunkf (real) -> IAT q[0x8c2bb8] sqrtf",
         "0x63040000 (scripted import)"),
        ("0x23268a", "call 0x202e10", "xprod (real)", None)],
    "d5a0": [
        ("0x3da5de", "call 0x3da730", "da730 (real)", None),
        ("0x3da5e3", "call 0x3a1d30", "a1d30 (real)", None),
        ("0x3da5f4", "call 0x3da730", "da730 (real)", None),
        ("0x3da5f9", "call 0x3a1d30", "a1d30 (real)", None),
        ("0x3da655", "call 0x861f5c",
         "tsqd (real) -> IAT q[0x8c2c60] sqrt f64",
         "0x630c0000 (scripted import)")],
    "tacf": [
        ("0x861f56", "jmp qword ptr [rip+disp]",
         "IAT q[0x8c2c78] acosf", "0x630d0000")],
    "tsqd": [
        ("0x861f5c", "jmp qword ptr [rip+disp]",
         "IAT q[0x8c2c60] sqrt f64", "0x630c0000")],
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
