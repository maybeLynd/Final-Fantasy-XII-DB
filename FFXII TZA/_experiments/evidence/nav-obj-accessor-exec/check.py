# EXP-136 nav-obj-accessor-exec — native replay harness.
#
# Executes the EXP-135 scripted object-accessor family real:
# handle decode, variant-dispatched field readers, chain walks,
# the handle-table decoder, and the subsystem query/dispatcher
# thunks — plus the whole EXP-135 tree that reaches them:
#
#   OBJD  00263E30 5B — rax = q[rcx+0x30] (handle->object).
#   O3FW  002646C0 141B — rcx==0 -> ret; v=b[+3]>>5: v==1 copy
#         d[qB8+0/4/8] -> [rdx/r8/r9]; v==3 copy + (b[+0x107]&1:
#         addss f[+0x40/44/48] into outs); else zero outs.
#   O2FW  00265090 27B — (b[+3]&0xE0)==0x60 -> tail 003DA710:
#         d[qB8+0x50]->[rdx], d[+0x54]->[r8] (nonnull outs).
#   O1F   00265200 38B — rcx==0 -> 0; v==1 f[qB8+0x38];
#         v==3 f[qB8+0xA8]; else 0.
#   O1F2  00263940 38B — v==1 f[qB8+0x68]; v==3
#         f[qB8+0xC0]*f[qB8+0x24]; else 0 (no null guard).
#   O1F3  00265830 34B — (b[+3]&0xE0)==0x60 ->
#         f[q[qB8+0xF0]+0x24]; else 0 (no null guard).
#   OVF   002E9FE0 73B — (b[+3]&0xE0)!=0x60 -> 1; else
#         c=q[+0xC0]: 0||d[c+0x164]!=0 -> 0; b11=c[+0x11],
#         b10=c[+0x10]: (b11&0x20 ? b10&3==3 : b10&0xB==0xB)
#         required else 0; ret (b11&6)==6.
#   OPA   00314EB0 109B — r10=a->+0xC0->+0x138, r9=b->+0xC0->
#         +0x138 (null-safe); both required; b[r10+6]==b[r9+6]
#         required; b[r10+0x119]==0 -> 1; ==b[r9+0x119] -> 0;
#         else 1.
#   A6A0  002646A0 31B — rcx==0||q[+0xC0]==0||q[+0x138]==0 -> 0
#         else that q.
#   OPB   00313F80 115B — rsi=A6A0(rcx), rax=A6A0(rdx); either
#         0 -> 0; eax=F50(rsi,rax,0,&tmp); r8!=0 -> f[r8]=f[tmp].
#   OF60  00313F60 5B — jmp 00377C20 (scripted bitfield lookup).
#   OSUB  0026E350 86B — q[0x209A670]==0 -> -1; rbx=
#         q[0x209A678]==0 -> -1; ax=N31900(rbx,rcx,1); ax<0 ->
#         -1; N31820(rbx,rcx,ax); ret 0.
#   MABESP 003588B0 143B — ecx==0 -> 0; sel=(ecx>>0x10)&0xF >=5
#         -> 0; T=N63FF0(sel); arr=q[T+8]; arr==0||q[T]==0 ->
#         0; id=cx: id>=d[T+0x20]||!(b[T+0x10]&1)||id>=d[arr] ->
#         0; o=q[arr+8+id*8]; o==0 -> 0; ret o iff
#         w[o+0x16]==(ecx>>0x14)&0x7FF else 0.
#   DE100 0026E100 35B — rcx=q[0x209A670]?q[0x209A678]:0,
#         rdx=arg1, r8=zx(arg2), r9=arg3 -> tail N31400.
#   AGENTQ 00318CA0 36B — rcx=q[0x2EC1378]; ==0 -> -1; else
#         cwde(N315E0(rcx,arg1,arg2,arg4)).
#
#   GATE  003357B0 944B — (rcx=posA vec, rdx=posB vec, xmm2=rad,
#         r8 dead, r9=ctx obj, [entry+0x28]=excl handle,
#         [entry+0x30]=flags -> r15d).
#         GTAB(b[ctx+0xEA9]) -> self=MABE(d[obj+8]); [rsp+0x20].
#         flags&0x20 clear -> GCHK(self)==0 -> ret 0.
#         posA.xyz == posB.xyz (ucomiss ordered) -> point query
#         GPT({posA@rbp-0x80,rad@+0x10}, out=rbp-0x20, 0x20,
#         ((~(f>>4))&8)|0x14); else GSEG({posA,posB@rbp-0x60,
#         rad@+0x20},out,0x20,same) segment query. count<=0 -> 0.
#         Loop candidates out[i] (r14):
#         OBJD(handle) -> rdi obj; handle==self or ==arg5 -> skip;
#         obj==0 -> accept path; q[obj+0xE68] && q[ctx+0xE68]
#         nonnull && (b[obj_e68+0x18]>>1&7)==1 &&
#         (b[ctx_e68+0x18]>>1&7)==4 -> skip; flags&0x40 &&
#         b[ctx+0x1F4]!=3 && b[obj+0x1F4]==3 -> O3FW(q[obj+0x10]
#         nonnull ->f30/34/38) -> T350 -> OSUB({f30,1,f38,1},
#         ret dead); xmm0=q[ctx+0x10]?O1F2(it):0;
#         f34-1.0f > xmm0 -> skip.
#         flags&2 && LHELP(obj)==0 ->
#         esi++ (early-out). flags&4 && LHELP(ctx)==0 &&
#         LHELP(obj)==0 -> esi++. flags&0x10 && LHELP(obj)==0 &&
#         O1F3(q[obj+0x10]) ordered==0 -> esi++. flags&8:
#         LHELP(ctx)!=LHELP(obj) -> skip, w[obj+0x714]!=0x4021 ->
#         skip. obj==0 or all tests fall through -> accept path:
#         flags&0x40 && b[ctx+0x1F4]==3 -> O3FW(handle ->f70/74/
#         78) + O1F2(handle) + f74 vs d[posA+4] -> ja skip.
#         OPA(self,handle)==0 -> skip. OPB(self,handle,&out):
#         (eax-1)<=2 -> esi++; else r12d++.
#         Ret: r12d>0 -> 1; else esi!=0 -> 2; else 0.
#   LHELP 00335760 — rcx==0||q[+0x698]==0||b[rax+5]!=1 -> 0;
#         OCLS(q[rcx+0x10])==3 -> 0; {1,2} -> 1; else 2.
#   OCLS  00263C20 — rcx==0 -> 0; else b[rcx+0xE]&0xF.
#   GTAB  00236820 — ecx<0||ecx>d[0x208E6A0]-1 -> 0; else
#         q[0x208E688]+ecx*0xF50.
#   MABE  0031ABE0 — b[0x2089340]&0x10 -> tail-jmp 0x3588B0
#         (scripted); else ret 0.
#   GCHK  002EA7F0 — rcx==0||b[+0x18]==1||q[+0xC0]==0||
#         b[rax+0x14F]&1||q[rax+0x138]==0||d[+0xF0]<=0||
#         b[+8]&8==0 -> 0; else OVF(rcx)!=0 || b[+4]==3.
#   T350  0032A790 — jmp 0026E350 (OSUB scripted).
#   GPT   00391D10 / GSEG 003920F0 — wrappers: collector into
#         rsp+0x30 temp then GFILT(out,0x20,tmp,cnt,flags).
#   GPC   00391A30 — point+rad cell walk: clamp cvtt bounds over
#         LGW/LGH, OR occupied cells' LSRC records into LBMSK,
#         then per set bit (d[0x2AEE0BC] recs, handles at
#         0x2AEE0C0): flag&0x10 -> S3W+CDST else S2W+CDZ0.
#   GSC   00391D90 — segment AABB (max/min ± rad) -> BMASK ->
#         DIST len==0 ordered -> 0; unit dxz = (p2-p1)/len; per
#         bit: flag&0x10 -> S3W+CF90 capsule; else S2W + inline
#         strip (0<dot<len && |cross|<rsum) or
#         DIST(tmp,p2)<rsum fallback.
#   GFILT 003911D0 — per tmp handle: OBJD; flags&2&&null->skip;
#         flags&4&&obj: q[+0x698]!=0 && (d[+0x64]|d[+0x3C])
#         &0x80000003 && OF60==0 -> skip; flags&8&&GCHK==0 ->
#         skip; else out[w++]=handle (w<outcnt). ret accepted.
#   S3W   002FB500 — O3FW(out+0/4/8) + O2FW(out+0x10/0x14) +
#         d[out+0x18]=O1F.
#   S2W   002FB340 — O3FW(out+0/4/8) + O2FW(frame) ->
#         ret maxss(f1,f2).
#   CDST  00469060 — (TRIGD(tmp,query)+q.rad10)^2 >=
#         (q.x-t.x)^2+(q.z-t.z)^2 -> setae.
#   CDZ0  00468D10 — (q.rad10+t.f10)^2 > (q.x-t.x)^2+(q.z-t.z)^2
#         -> seta.
#   CF90  00468F90 — CPSEG closest on seg to tmp; TRIGD(tmp,c)
#         + seg.rad20 > |tmp-c| -> seta.
#
# Re-executed real (previous packages): the entire EXP-130/131/
# 132/133/134 trees (incl. BMASK 003912E0, DIST 003A1920, CPSEG
# 004691A0, TRIGD 00468580, TMS 00861EC0, THUNKF 00861F14,
# CHKCK 00808C40 — all inside the new tree).
#
# Scripted boundaries (disclosed) — moved one hop deeper:
#   N7C20 00377C20 — OF60's bitfield lookup (of60rets).
#   N14F50 00314F50 — OPB's inner pair compare (opbrets eax,
#         f50v dword written to r9 out ptr).
#   N63FF0 00263FF0 — MABESP table select (t3frets rax).
#   N31900 00231900 — OSUB stage-1 word query (w19rets ax).
#   N31820 00231820 — OSUB stage-2 lookup (ret dead, traced).
#   N31400 00231400 — DE100's dispatcher (derets eax).
#   N315E0 002315E0 — AGENTQ's query (agrets eax, cwde'd).
#   Inherited: FDC/SQF/ISN/FIN/COS/SIN/MSET/AT2 real-thunk
#   trampolines.
#
# Fixture (planted, disclosed): EXP-135 fixture wholesale PLUS
# the object record spine — b[+3] variant byte, q[+0x30] objd
# target, q[+0xB8] field record (d0/4/8 vec, f24, f38, f40/44/
# 48, d50/54, f68, fA8, fC0, b107 flag, qF0->{f24}), q[+0x10]
# sub object, q[+0xC0] chain (q138->{fF0,b6,b119}, d164, b11,
# b10, b14F), MABESP table rec + entry array, subsystem globals
# q[0x209A670]/q[0x209A678]/q[0x2EC1378].
#
# Native and model must agree on trace/rets/faults/watched memory.
#
# Re-executed real body inventory (reference):
#
#   LQUERY 00391410 758B — segment LOS query over a wall-record
#         grid (EXP-133). 160-iter loop: bit (i%8) of
#         b[mask+0x10+i/8]; i<0x20 wall record BASE(d[root+0x28])
#         +i*0x20 type 0 -> CAPT0, 1 -> CAPT1; i>=0x20 ->
#         RDEC(i-0x20) + CAPT1. First hit -> 1 else 0.
#   BMASK  003912E0 292B — memset + clamp + per-flagged-cell OR
#         of reclen bytes into the row bitmap (EXP-133).
#   DIST   003A1920 53B  — sqrt(|a-b|^2), dead call in LQUERY.
#   CAPT0  00468D50 250B — capsule test A (point/seg; EXP-133).
#   CAPT1  00468E50 281B — capsule test B (CPSEG + TRIGD; EXP-133).
#   CPSEG  004691A0 315B — closest point on segment (EXP-133).
#   TRIGD  00468580 325B — trig-table distance helper (EXP-133).
#   CAPV   00469410 346B — sibling capsule variant (EXP-133).
#   RDEC   0032A6E0 153B — nav-record decode (EXP-133).
#   PATHW  0033A3D0 405B — path-width probe, 2 rounds of rotated
#         offsets + QWALK probes (EXP-132).
#   BLKCHK 00335F90 161B — corridor-blocked check: real PRED over
#         real QWALK inside (EXP-132).
#   AWRAP  0033CB70 128B — angle wrap to [-pi,pi] (EXP-132).
#   MLOAD  00203170 44B — picks {+X,+Y,+Z,W} from the signed
#         axis-basis bank 0x8C5F80..0x8C5FE0 -> identity (EXP-132).
#   RBUILD 00202F00 100B — mat copy + cosf/sinf -> ROTCOL.
#   ROTCOL 00217880 234B — per-column (x,z) rotation (EXP-132).
#   MXV    00217060 235B — mat * vec (EXP-132).
#   MXVW   00202B70 31B  — MXV via frame temp (EXP-132).
#   QWALK  0033D3E0 631B — segment walk over tri adjacency matrix
#         (EXP-131): grid(p1)->cur, grid(p2)->dst; per tri: edge
#         rec -> eclass/flag gate -> seg-vs-edge test; crossing
#         advances; cur==dst -> 0; exhaust -> 1.
#   WWRAP  00384130 40B  — {v.x,v.z} pair -> GGRID (EXP-131).
#   GGRID  00383F10 542B — grid point query -> tri index (EXP-131).
#   TTEST  00382D10 384B — point-in-triangle (EXP-131).
#   ECLASS 0032A780 5B + 0026E300 73B — bit-class query (EXP-131).
#   SEGT   00468880 496B — seg-seg orientation test (EXP-131).
#   PRED   00335E50 — corridor-width probe: 3 real QWALK probes
#         over +/- perpendicular offsets (EXP-130/132).
#   VSUB 00203080 / VADD 00202B10 / VSCALE 00202FE0 /
#   NORM 00216660 / NCOPY 00202DE0 / XPROD 00202E10 (EXP-130).
#   BASE   0020E600 9B — rax = ecx + q[0x1F83530].
#   ROOTL  00383840 8B — rax = q[0x2AEDFB0].
#   CHKCK  00808C40 — GS cookie check.
#
# Native and model must agree on trace/rets/faults/watched memory.

import ctypes
import hashlib
import json
import math
import struct
import sys
import os
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from unicorn import Uc, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE, \
    UC_HOOK_MEM_UNMAPPED, UC_HOOK_INTR, UC_PROT_ALL, UcError
from unicorn.x86_const import UC_X86_REG_RAX, UC_X86_REG_RCX, \
    UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_R9, \
    UC_X86_REG_RSP, UC_X86_REG_RIP, \
    UC_X86_REG_XMM0, UC_X86_REG_XMM1, UC_X86_REG_XMM2, \
    UC_X86_REG_XMM3

EXE = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe"
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
RESULT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "result.json")

IMG_LO = 0x120000
IMG_HI = 0x30A0000
HEAP   = 0x40000000
STACK  = 0x61000000
RETQ   = 0x62000000
SQF    = 0x63040000          # planted trampoline: sqrtf import
ISN    = 0x63050000          # planted trampoline: _isnan import
FIN    = 0x63060000          # planted trampoline: _finite import
FDC    = 0x63070000          # planted trampoline: _fdclass import
COS    = 0x63080000          # planted trampoline: cosf import
SIN    = 0x63090000          # planted trampoline: sinf import
MSET   = 0x630A0000          # planted trampoline: memset import
AT2    = 0x630B0000          # planted trampoline: atan2f import

QWALK  = 0x0033D3E0          # segment walk over tri adjacency
WWRAP  = 0x00384130          # {x,z} pair wrapper -> GGRID
GGRID  = 0x00383F10          # grid point query -> tri id / 0xFF
TTEST  = 0x00382D10          # point-in-triangle test
ETHUNK = 0x0032A780          # jmp 0026E300
ECLASS = 0x0026E300          # edge-class bit query
SEGT   = 0x00468880          # seg-seg orientation test
BASE   = 0x0020E600          # rax = ecx + q[0x1F83530]
ROOTL  = 0x00383840          # rax = q[0x2AEDFB0]
VSUB   = 0x00203080          # vec4 sub (real)
XPROD  = 0x00202E10          # vec4 cross (real)
CHKCK  = 0x00808C40          # __security_check_cookie - real
# EXP-130 PRED tree (re-executed real)
PRED   = 0x00335E50          # corridor-width probe
VADD   = 0x00202B10          # vec4 add
VSCALE = 0x00202FE0          # vec4 * xmm2
NCOPY  = 0x00202DE0          # movups + NORM + w=0
NORM   = 0x00216660          # normalize-or-zero in place
THUNKF = 0x00861F14          # real IAT thunk -> sqrtf
# EXP-132 new bodies
PATHW  = 0x0033A3D0          # path-width probe (5x QWALK)
BLKCHK = 0x00335F90          # corridor-blocked check
MLOAD  = 0x00203170          # const 4x4 matrix load
AWRAP  = 0x0033CB70          # angle wrap to [-pi,pi]
RBUILD = 0x00202F00          # mat copy + cosf/sinf -> ROTCOL
ROTCOL = 0x00217880          # in-place column (x,z) rotate
MXVW   = 0x00202B70          # mat*vec wrapper
MXV    = 0x00217060          # mat*vec
TCOS   = 0x00861F08          # real IAT thunk -> cosf
TSIN   = 0x00861F0E          # real IAT thunk -> sinf
AGENTQ = 0x00318CA0          # scripted: subsystem-object query
# EXP-133 new bodies
LQUERY = 0x00391410          # segment LOS query over wall grid
BMASK  = 0x003912E0          # AABB -> OR'd record bitmask
DIST   = 0x003A1920          # 3D point distance -> THUNKF
CAPT0  = 0x00468D50          # capsule test A (point radius)
CAPT1  = 0x00468E50          # capsule test B (edge + TRIGD)
CPSEG  = 0x004691A0          # closest point on segment
TRIGD  = 0x00468580          # trig-table edge helper
CAPV   = 0x00469410          # sibling capsule variant
RDEC   = 0x0032A6E0          # nav-record decode + atan2f
TMS    = 0x00861EC0          # real IAT thunk -> memset
TAT2   = 0x00861F02          # real IAT thunk -> atan2f
# EXP-134 new bodies + scripted gates
PVAL   = 0x00335B60          # top path validator consumer
MCPY   = 0x00202E90          # mat copy + cosf/sinf -> ROTX
ROTX   = 0x00217790          # in-place column (y,z) rotate
DE6A0  = 0x0032A6A0          # jmp 0026E100 dispatcher
GATE   = 0x003357B0          # corridor gate (now REAL)
DE100  = 0x0026E100          # scripted: object-root dispatcher
# EXP-135 new bodies — GATE tree
LHELP  = 0x00335760          # gate accept helper -> OCLS class
OCLS   = 0x00263C20          # object class byte (b[+0xE]&0xF)
GTAB   = 0x00236820          # object-pool table lookup
MABE   = 0x0031ABE0          # subsystem flag gate / handle ret
MABESP = 0x003588B0          # MABE slow-path tail (scripted)
GCHK   = 0x002EA7F0          # object validity check
T350   = 0x0032A790          # jmp 0026E350 -> OSUB (scripted)
GPT    = 0x00391D10          # point-query wrapper -> GPC+GFILT
GSEG   = 0x003920F0          # segment-query wrapper -> GSC+GFILT
GPC    = 0x00391A30          # point+rad cell collector
GSC    = 0x00391D90          # segment cell collector
GFILT  = 0x003911D0          # handle-array acceptance filter
S3W    = 0x002FB500          # O3FW+O2FW+O1F record writer
S2W    = 0x002FB340          # O3FW + max(O2FW) record writer
CDST   = 0x00469060          # TRIGD+rad vs dxz2 (setae)
CDZ0   = 0x00468D10          # rad+t.f10 vs dxz2 (seta)
CF90   = 0x00468F90          # CPSEG+TRIGD+sqrtf capsule (seta)
# EXP-135 scripted boundaries (subsystem-object leaves)
OBJD   = 0x00263E30          # handle -> object decode
O3FW   = 0x002646C0          # write 3 floats to out ptrs
O2FW   = 0x00265090          # write 2 floats to out ptrs
O1F    = 0x00265200          # return float
O1F2   = 0x00263940          # return float
O1F3   = 0x00265830          # return float
OPA    = 0x00314EB0          # pair check -> int
OPB    = 0x00313F80          # pair check -> int + writes
OF60   = 0x00313F60          # object check -> int
OVF    = 0x002E9FE0          # GCHK tail -> int
OSUB   = 0x0026E350          # subsystem query -> int

# EXP-135 BSS globals (ship 0, runtime-populated): planted
GTPOOL = 0x208E688           # q: GTAB object pool base
GTPCNT = 0x208E6A0           # d: GTAB pool count (limit = cnt-1)
MABEF  = 0x2089340           # b: MABE flag (&0x10 -> MABESP)
GHND   = 0x2AEE0C0           # q[0x2AEE0BC] handle array (collectors)
GRCNT  = 0x2AEE0BC           # d: collector record count

PVHI   = 0x8F3108            # d: PVAL cap hi clamp = 0.8f
PVLO   = 0x8F30F8            # d: PVAL cap lo clamp = 0.2f
SGNM   = 0x1CEBDA0           # xmm: sign mask for angB negate
CVEC   = 0x1F004C0           # f: const vec {0,0,1,1}

ROOTCELL = 0x2AEDFB0          # q: nav root global (BSS, ships 0)
BASECELL = 0x1F83530         # q: BASE pool base (BSS, ships 0)
FDCIAT   = 0x8C2C10          # q: IAT _fdclass (ships hint record)
IATF     = 0x8C2BB8          # q: IAT sqrtf
PC1      = 0x8C2C68          # q: IAT _isnan (ships hint 0x1CCECD8)
PC2      = 0x8C2C70          # q: IAT _finite (ships hint 0x1CCECCE)
IATCOS   = 0x8C2BA8          # q: IAT cosf (import-dir proven)
IATSIN   = 0x8C2BB0          # q: IAT sinf (import-dir proven)
CLSTAB   = 0x915760          # d: r15 -> class bit index (rdata)
BPTAB    = 0x209A3E0         # d: edge class -> bit pair (BSS)
TRIIDX   = 0xD112B0          # d: shipped tri edge index array
COOK     = 0x1F44830         # q: __security_cookie (shipped)
GSCOOK   = 0x2B992DDFA232    # shipped cookie value
FLTM     = 0x907698          # d: NORM epsilon = FLT_MIN (shipped)
SEEDF    = 0x1CEBBA8         # d: NORM 1.0f seed (shipped)
CONSTV   = 0x1F004B0         # f: PRED axis const (0,1,0,1) shipped
MLOADC   = 0x8C5F80          # f: MLOAD const 4x4 matrix (16 floats)
AWHI     = 0xD10B0C          # d: AWRAP +4pi bound
AWLO     = 0xD10B20          # d: AWRAP -4pi bound
AWPI     = 0x1CEBC50         # d: AWRAP +pi
AWNPI    = 0x915620          # d: AWRAP -pi
AWNEG2   = 0x915624          # d: AWRAP -2pi step
AW2PI    = 0x1CEBC78         # d: AWRAP +2pi / mod period
PWSC     = 0x1CEBB70         # d: PATHW scale const = 0.5f
PWANG1   = 0x915614          # d: PATHW round-1 angle = +pi/4
PWANG2   = 0xD10B18          # d: PATHW round-2 angle = -pi/4
BKSC     = 0x8FCC8C          # d: PRED radius scale = 0.9f (3F666666)
IATMSET  = 0x8C2A60          # q: IAT memset (import-dir proven)
IATAT2   = 0x8C2BD0          # q: IAT atan2f (import-dir proven)
# LQUERY/BMASK grid global block — all BSS (ships 0, runtime
# populated by the nav loader): planted per case
LGW      = 0x2AEE060         # d: LOS grid width (cols)
LGH      = 0x2AEE064         # q: LOS grid height (rows)
LEPSX    = 0x2AEE070         # d: x-range epsilon (sub hi AND lo)
LEPSZ    = 0x2AEE078         # d: z-range epsilon (sub hi AND lo)
LCSZ     = 0x2AEE090         # d: cell size divisor
LLSRC    = 0x2AEE0A0         # q: per-cell record bitmask array
LCFLG    = 0x2AEE0A8         # q: cell-flag map (b per cell)
LBMSK    = 0x2AEE0B0         # q: bitmask accumulator/return
LRLEN    = 0x2AEE0B8         # d: record len = memset len = stride
NRROOT   = 0x209A670         # q: nav-record root (BSS, ships 0)
RSCRATCH = 0x22D91B0         # xmm: RDEC scaled-vec global scratch
TRIGT    = 0x1F004E0         # f: shipped 0x8000-entry trig table
NEG2PI   = 0x915624          # d: -2pi (== AWNEG2)
TRIGN    = 0xD10828          # d: -32768.0 table index scale
TRIGP    = 0xD10820          # d: +32768.0 table index scale
DISTEPS  = 0x9002C8          # d: 1e-6 double threshold (comisd)
SCLV     = 0x908E30          # xmm: 1/4096 fixed-point scale
CLAMP1   = 0x1CEBBA8         # d: 1.0f clamp (== SEEDF)

# planted fixture addresses
BASEP  = HEAP + 0x30000      # BASE pool base -> BASE(i) = BASEP + i
ROOTA  = HEAP + 0x40000      # planted root struct
# BASE pool offsets
VPOOL  = 0x0000              # vertex pool: f32 (x,y) pairs
IDXA   = 0x0100              # idx arrays: 8B blocks (4 words)
EDGEP  = 0x0200              # edge records: 8B each
LISTR  = 0x0300              # list records: 0x22 stride
ADJM   = 0x0500              # tri adjacency matrix: words
GHDR   = 0x0600              # grid header
CMAP   = 0x0640              # cell map: words
BLIST  = 0x0680              # byte lists

P1     = HEAP + 0x10000      # walk arg p1 (vec4)
P2     = HEAP + 0x11000      # walk arg p2 (vec4)
PT     = HEAP + 0x12000      # point pair {x,y} for GGRID/TTEST
VECX   = HEAP + 0x13000      # extra vec4 (va)
VECY   = HEAP + 0x13010      # extra vec4 (vb)
IARR   = HEAP + 0x14000      # direct TTEST idx array (words)
AGENT  = HEAP + 0x15000      # BLKCHK agent record
SUBR   = HEAP + 0x16000      # BLKCHK sub-record q[agent+0x108]
MATB   = HEAP + 0x17000      # 4x4 matrix buffer (MLOAD/RBUILD/MXV)
VECQ   = HEAP + 0x18000      # vec4 arg buffer (MXV/MXVW)
DVB    = HEAP + 0x19000      # dst vec4 buffer
# EXP-133 LOS fixture
NRO    = HEAP + 0x1A000      # nav-record root {+0x188 vtx,+0x1a0 rec}
RECP   = HEAP + 0x1B000      # 16B-stride nav-record pool
VEXP   = HEAP + 0x1D000      # 64B-stride vertex pool
CFLGA  = HEAP + 0x1F000      # cell-flag map (b per cell)
LSRCA  = HEAP + 0x20000      # per-cell record bitmask array
BMSKA  = HEAP + 0x28000      # bitmask accumulator buffer
WPOOL  = 0x0800              # BASE offset: wall rec pool (0x20 stride)
SEGV   = HEAP + 0x2A000      # CAPT/CPSEG arg vecs
# EXP-135 gate object fixture
GTPA   = HEAP + 0x50000      # GTAB pool entries (0xF50 stride)
CTXA   = HEAP + 0x51000      # gate ctx object (r9)
SELFO  = HEAP + 0x52000      # self object (MABE ret / GCHK target)
CANDA  = HEAP + 0x53000      # candidate objects (0x400 stride)
E68A   = HEAP + 0x54000      # +0xE68 records (0x40 stride)
OSUBA  = HEAP + 0x55000      # +0x10 sub records (0x100 stride)
G698A  = HEAP + 0x56000      # +0x698 records (0x40 stride)
GC0A   = HEAP + 0x57000      # GCHK +0xC0 records (0x100 stride)
GC138A = HEAP + 0x58000      # GCHK +0x138 records (0x100 stride)
GOBJA  = HEAP + 0x59000      # scratch object arg buffer
CTXB   = HEAP + 0x5A000      # second ctx object (gateptr mutant)
# EXP-136 real callees + scripted boundary addrs
DA710  = 0x003DA710          # O2FW tail: conditional dword writer
A6A0   = 0x002646A0          # obj -> q[+0xC0] -> q[+0x138] chain
N7C20  = 0x00377C20          # OF60 target: bitfield lookup (scr)
N14F50 = 0x00314F50          # OPB inner pair compare (scripted)
N63FF0 = 0x00263FF0          # MABESP table select (scripted)
N31900 = 0x00231900          # OSUB stage-1 word query (scripted)
N31820 = 0x00231820          # OSUB stage-2 lookup (scripted)
N31400 = 0x00231400          # DE100 target dispatcher (scripted)
N315E0 = 0x002315E0          # AGENTQ target query (scripted)
SUBTB  = 0x209A678           # q: subsystem table (BSS)
AGQTB  = 0x2EC1378           # q: AGENTQ query table (BSS)
# EXP-136 fixture space (sub objects reuse the OSUBA region)
QB8A   = HEAP + 0x60000      # +0xB8 records (0x400 stride)
MSPT   = HEAP + 0x68000      # MABESP table record
MSPA   = HEAP + 0x68400      # MABESP entry array
SELF_B8 = QB8A + 0x1000      # SELFO's +0xB8 record
SELF_F0 = QB8A + 0x1200      # SELFO's +0xF0 record
CTX_B8  = QB8A + 0x1400      # ctx_sub's +0xB8 record
CTX_F0  = QB8A + 0x1600

# QWALK frame: rsp = STACK+0x80000 - 4 pushes - sub 0x98 = +0x7FF48
# locals: +0x40 {x@+0,z@+8} sparse pair, +0x50/+0x60 edge vert vecs
WQ40   = STACK + 0x7FF88
WQ50   = STACK + 0x7FF98
WQ60   = STACK + 0x7FFA8
# nested WWRAP inside QWALK: call -> rsp 0x7FF40, sub 0x28 ->
# 0x7FF18; contiguous pair at rsp+0x30 = STACK+0x7FF48
WPAIR  = STACK + 0x7FF48
# SEGT direct frame: entry rsp 0x80000, push rbp -> rbp=rsp-0x57
# = 0x7FFA1; sub 0xD0 -> rsp 0x7FF28. vec locals rbp-0x59/-0x49/
# -0x29/-0x19 = +0x7FF48/58/78/88
SQVA   = STACK + 0x7FF48        # rbp-0x59: p1 vec
SQVB   = STACK + 0x7FF58        # rbp-0x49: va vec
SQVC   = STACK + 0x7FF78        # rbp-0x29: vb vec
SQVD   = STACK + 0x7FF88        # rbp-0x19: p2 vec


def qw(v): return struct.pack("<Q", v & 0xFFFFFFFFFFFFFFFF)
def dw(v): return struct.pack("<I", v & 0xFFFFFFFF)
def ww(v): return struct.pack("<H", v & 0xFFFF)
def bb(v): return struct.pack("<B", v & 0xFF)
def ff(v): return struct.pack("<f", v)


# ---------------- f32 helpers ----------------

def f32(x):
    try:
        return struct.unpack("<f", struct.pack("<f", x))[0]
    except OverflowError:
        return math.copysign(float("inf"), x)


def f2u(x):
    return struct.unpack("<I", struct.pack("<f", x))[0]


def u2f(u):
    return struct.unpack("<f", struct.pack("<I", u & 0xFFFFFFFF))[0]


_CRT = None
try:
    _CRT = ctypes.CDLL("api-ms-win-crt-math-l1-1-0.dll")
    _CRT._fdclass.restype = ctypes.c_int
    _CRT._fdclass.argtypes = (ctypes.c_float,)
    _CRT.sqrtf.restype = ctypes.c_float
    _CRT.sqrtf.argtypes = (ctypes.c_float,)
    _CRT.cosf.restype = ctypes.c_float
    _CRT.cosf.argtypes = (ctypes.c_float,)
    _CRT.sinf.restype = ctypes.c_float
    _CRT.sinf.argtypes = (ctypes.c_float,)
    _CRT.atan2f.restype = ctypes.c_float
    _CRT.atan2f.argtypes = (ctypes.c_float, ctypes.c_float)
except OSError:
    pass


def f32_round(q):
    """Correctly rounded f32 (ties-to-even) of an exact Fraction."""
    if q == 0:
        return 0.0
    sgn = q < 0
    if sgn:
        q = -q
    e = q.numerator.bit_length() - q.denominator.bit_length()
    two = Fraction(2)
    if q < two ** e:
        e -= 1
    elif q >= two ** (e + 1):
        e += 1
    if e >= 128:
        return float("inf")
    unit = two ** (e - 23) if e >= -126 else two ** (-149)
    scaled = q / unit
    n = scaled.numerator // scaled.denominator
    rem = scaled - n
    if rem > Fraction(1, 2) or (rem == Fraction(1, 2) and n & 1):
        n += 1
    if e >= -126 and n >> 24:
        e += 1
        if e >= 128:
            return float("inf")
        unit = two ** (e - 23)
        n >>= 1
    r = f32(float(Fraction(n) * unit))
    return -r if sgn else r


def _sgn(a, b):
    s = math.copysign(1.0, a) * math.copysign(1.0, b)
    return -1.0 if s < 0 else 1.0


def f32div(a, b):
    """divss: correctly-rounded single-precision division."""
    if math.isnan(a) or math.isnan(b):
        return float("nan")
    if math.isinf(a):
        return math.copysign(float("inf"), _sgn(a, b))
    if math.isinf(b):
        return math.copysign(0.0, _sgn(a, b))
    if b == 0:
        if a == 0:
            return float("nan")
        return math.copysign(float("inf"), _sgn(a, b))
    r = f32_round(Fraction(a) / Fraction(b))
    if r == 0:
        return math.copysign(0.0, _sgn(a, b))
    return r


def sqrtf32(x):
    if math.isnan(x) or x < 0:
        return float("nan")
    if _CRT is not None:
        return _CRT.sqrtf(x)
    return f32(math.sqrt(x))


def sqrtf_bits(u):
    return f2u(sqrtf32(u2f(u)))


def cosf_bits(u):
    if _CRT is not None:
        return f2u(_CRT.cosf(u2f(u)))
    x = u2f(u)
    return f2u(float("nan") if math.isinf(x) or math.isnan(x)
               else f32(math.cos(x)))


def atan2f_bits(uy, ux):
    if _CRT is not None:
        return f2u(_CRT.atan2f(u2f(uy), u2f(ux)))
    y, x = u2f(uy), u2f(ux)
    if math.isnan(y) or math.isnan(x):
        return f2u(float("nan"))
    return f2u(f32(math.atan2(y, x)))


def sinf_bits(u):
    if _CRT is not None:
        return f2u(_CRT.sinf(u2f(u)))
    x = u2f(u)
    return f2u(float("nan") if math.isinf(x) or math.isnan(x)
               else f32(math.sin(x)))


def fdclass_f32(u):
    """Host CRT _fdclass on the f32 bit pattern (as the callee sees
    xmm0's low dword). -1 normal, -2 denormal, 0 zero, 1 inf, 2 NaN."""
    if _CRT is not None:
        return _CRT._fdclass(u2f(u))
    x = u2f(u)
    if math.isnan(x):
        return 2
    if math.isinf(x):
        return 1
    if x == 0:
        return 0
    return -2 if abs(x) < 1.1754943508222875e-38 else -1


def _cvtt(f):
    """cvttss2si: invalid/overflow -> 0x80000000 (signed -2**31)."""
    if math.isnan(f) or math.isinf(f) or \
            f >= 2147483648.0 or f < -2147483649.0:
        return -0x80000000
    return int(f)


def _idiv(a, b):
    """signed idiv: truncates toward zero (// floors for negatives)."""
    q = abs(a) // abs(b)
    return -q if (a < 0) != (b < 0) else q


def _ueq(a, b):
    """ucomiss ordered-equal: jp/jne both fall through."""
    return not math.isnan(a) and not math.isnan(b) and a == b


def _seta(a, b):
    """comiss a,b -> seta: CF=0 and ZF=0 -> a > b ordered."""
    return not math.isnan(a) and not math.isnan(b) and a > b


def _maxss(a, b):
    """maxss dst,src: unordered or src>=dst -> src."""
    return b if (math.isnan(a) or math.isnan(b) or b >= a) else a


def _minss(a, b):
    """minss dst,src: unordered or src<=dst -> src... inverse:
    dst = src if src < dst or unordered else dst."""
    return b if (math.isnan(a) or math.isnan(b) or b < a) else a


INDEF = u2f(0xFFC00000)          # x86 real-indefinite QNaN


def _qn(u):
    """NaN propagation: quieted u32 payload; None if not NaN."""
    return (u | 0x400000) if (u & 0x7FFFFFFF) > 0x7F800000 else None


def _n2(a, b):
    """SSE two-operand NaN rule: dest(a) NaN wins, then src(b)."""
    return _qn(f2u(a)) or _qn(f2u(b))


def _m(a, b):
    """mulss — NaN propagate; 0*inf -> real-indefinite."""
    n = _n2(a, b)
    if n is not None:
        return u2f(n)
    if (a == 0) != (b == 0) and (math.isinf(a) or math.isinf(b)):
        return INDEF
    return f32(a * b)


def _a(a, b):
    """addss — NaN propagate; +inf + -inf -> indefinite."""
    n = _n2(a, b)
    if n is not None:
        return u2f(n)
    if math.isinf(a) and math.isinf(b) and a != b:
        return INDEF
    return f32(a + b)


def _s(a, b):
    """subss — NaN propagate; inf - inf -> indefinite."""
    n = _n2(a, b)
    if n is not None:
        return u2f(n)
    if math.isinf(a) and math.isinf(b) and a == b:
        return INDEF
    return f32(a - b)


def _d(a, b):
    """divss — NaN propagate; 0/0, inf/inf -> indefinite."""
    n = _n2(a, b)
    if n is not None:
        return u2f(n)
    if (a == 0 and b == 0) or (math.isinf(a) and math.isinf(b)):
        return INDEF
    return f32div(a, b)


def load_image():
    raw = open(EXE, "rb").read()
    assert hashlib.sha256(raw).hexdigest() == SHA, "EXE hash mismatch"
    pe = struct.unpack_from("<I", raw, 0x3C)[0]
    nsec = struct.unpack_from("<H", raw, pe + 6)[0]
    optsz = struct.unpack_from("<H", raw, pe + 20)[0]
    secs, off = [], pe + 24 + optsz
    for _ in range(nsec):
        vs, va, rs, ra = struct.unpack_from("<IIII", raw, off + 8)
        secs.append((va, vs, ra, rs))
        off += 40
    return raw, secs


def img_rd(raw, secs, va, n):
    rva = va - IMG_LO
    for sva, vs, ra, rs in secs:
        if sva <= rva and rva + n <= sva + rs:
            return raw[ra + (rva - sva): ra + (rva - sva) + n]
    raise KeyError("image read outside shipped bytes: %x" % va)


class GuestMem:
    def __init__(self, uc):
        self.uc, self.bufs, self.regions = uc, [], []
    def map(self, addr, size, init=b""):
        buf = ctypes.create_string_buffer(size)
        if init:
            ctypes.memmove(buf, init, min(len(init), size))
        self.bufs.append(buf)
        self.uc.mem_map_ptr(addr, size, UC_PROT_ALL, ctypes.addressof(buf))
        self.regions.append((addr, size, ctypes.addressof(buf)))
    def _ptr(self, addr, n):
        for base, size, ptr in self.regions:
            if base <= addr and addr + n <= base + size:
                return ptr + (addr - base)
        raise KeyError("fixture access to unmapped guest addr %x" % addr)
    def w(self, addr, data):
        ctypes.memmove(self._ptr(addr, len(data)), bytes(data), len(data))
    def r(self, addr, n):
        return ctypes.string_at(self._ptr(addr, n), n)
    def qw(self, addr):
        return struct.unpack("<Q", self.r(addr, 8))[0]


# ---------------- synthetic mesh ----------------
# 4-triangle strip over an 8x4 area, origin (0,0), 2x2 cells:
#   T0={v0,v1,v2}  T1={v1,v3,v2}  T2={v1,v4,v3}  T3={v4,v5,v3}
#   e0 = v1-v2 (T0|T1)   e1 = v1-v3 (T1|T2)   e2 = v4-v3 (T2|T3)
VERTS = [(0.0, 0.0), (4.0, 0.0), (0.0, 4.0), (4.0, 4.0),
         (8.0, 0.0), (8.0, 4.0)]
TRIS = [(0, 1, 2), (1, 3, 2), (1, 4, 3), (4, 5, 3)]
# edge ids in the matrix index recs directly (id*8): rec0 is unused,
# id 1/2/3 = shared edges e0/e1/e2
EDGES = [(0, 0), (1, 2), (1, 3), (4, 3)]
# adjacency[t][n] = shared edge record index (0 = none)
ADJ = [[0, 1, 0, 0],
       [1, 0, 2, 0],
       [0, 2, 0, 3],
       [0, 0, 3, 0]]
# cell map: idx = col + row*4 -> byte-list offset
LISTS = [[0], [0, 1], [2], [2], [0, 1], [1], [2, 3], [3]]
CELLS = [0x00, 0x02, 0x05, 0x07, 0x09, 0x0C, 0x0E, 0x11]


def mesh_bytes(case):
    """BASE pool image: verts, idx arrays, edge recs, list recs,
    adjacency, grid header, cell map, byte lists."""
    verts = case.get("verts", VERTS)
    tris = case.get("tris", TRIS)
    edges = case.get("edges", EDGES)
    adj = case.get("adj", ADJ)
    lists = case.get("lists", LISTS)
    cells = case.get("cells", CELLS)
    eclass = case.get("eclass", [0] * len(edges))   # b[+5] per edge
    eflag = case.get("eflag", [0] * len(edges))     # b[+6] per edge
    ghd = case.get("ghdr", {})                   # grid hdr overrides
    buf = bytearray(0xC00 + WPOOL)
    for i, (x, y) in enumerate(verts):
        buf[VPOOL + i * 8: VPOOL + i * 8 + 8] = ff(x) + ff(y)
    for i, t in enumerate(tris):
        buf[IDXA + i * 8: IDXA + i * 8 + 6] = \
            ww(t[0]) + ww(t[1]) + ww(t[2])
    for i, (a, b) in enumerate(edges):
        rec = ww(a) + ww(b) + bb(0) + bb(eclass[i]) + \
            bb(eflag[i]) + bb(0)
        buf[EDGEP + i * 8: EDGEP + i * 8 + 8] = rec
    for i in range(len(tris)):
        rec = bytearray(0x22)
        rec[2:4] = ww(1)                       # 1 idx-array slot
        rec[0x14:0x16] = ww(i)                 # selector i
        buf[LISTR + i * 0x22: LISTR + i * 0x22 + 0x22] = rec
    for t in range(len(adj)):
        for n in range(len(adj)):
            buf[ADJM + (t * len(adj) + n) * 2:
                ADJM + (t * len(adj) + n) * 2 + 2] = ww(adj[t][n])
    # grid header: cellW/H, cols/rows, origin, cellmap, bytelist
    buf[GHDR + 0] = ghd.get("cw", 2)
    buf[GHDR + 1] = ghd.get("ch", 2)
    buf[GHDR + 2] = ghd.get("cols", 4)
    buf[GHDR + 3] = ghd.get("rows", 2)
    buf[GHDR + 4:GHDR + 8] = ww(ghd.get("ox", 0)) + \
        ww(ghd.get("oy", 0))
    buf[GHDR + 8:GHDR + 0x10] = dw(CMAP) + dw(BLIST)
    for i, c in enumerate(cells):
        buf[CMAP + i * 2: CMAP + i * 2 + 2] = ww(c)
    # byte lists at their declared offsets
    for ci, off in enumerate(cells):
        if off >= 0x180:
            continue
        for k, t in enumerate(lists[ci]):
            buf[BLIST + off + k] = t
        buf[BLIST + off + len(lists[ci])] = 0xFF
    # wall record pool at root+0x28 (0x20-stride records):
    # type-0 {w@0, x@4, z@8, rad@0xc}; type-1 {w@0, x@4, z@8,
    # x2@0xc, z2@0x10, angle@0x14}
    for i, r in enumerate(case.get("wrecs", [])):
        o = WPOOL + i * 0x20
        buf[o:o + 2] = ww(r[0])
        for k, v in enumerate(r[1:]):
            buf[o + 4 + k * 4:o + 8 + k * 4] = ff(v)
    return bytes(buf)


def build_fixture(case):
    """bytes/plants shared by native World and python model."""
    W = []
    W.append((FDCIAT, qw(FDC)))
    W.append((IATF, qw(SQF)))
    W.append((PC1, qw(ISN)))
    W.append((PC2, qw(FIN)))
    W.append((IATCOS, qw(COS)))
    W.append((IATSIN, qw(SIN)))
    W.append((BASECELL, qw(case.get("basep", BASEP))))
    W.append((ROOTCELL, qw(case.get("rootp", ROOTA))))
    # root struct: tri count + BASE'd pool offsets
    root = bytearray(0x30)
    root[0xA:0xC] = ww(case.get("tricnt", len(case.get("tris", TRIS))))
    for off, pool in ((0xC, VPOOL), (0x10, IDXA), (0x14, EDGEP),
                      (0x18, LISTR), (0x1C, ADJM), (0x20, GHDR),
                      (0x28, WPOOL)):
        root[off:off + 4] = dw(case.get("root_%x" % off, pool))
    W.append((ROOTA, bytes(root)))
    W.append((BASEP, mesh_bytes(case)))
    # class bit-pair table (BSS): per-case overrides
    for ci, (w0, w1) in enumerate(case.get(
            "bptab", [(1 << 23, 0), (1 << 25, 1 << 25),
                      (0, 1 << 26), (0, 0)])):
        W.append((BPTAB + ci * 8, dw(w0) + dw(w1)))
    # walk args (vec4s; only x,z read)
    W.append((P1, ff(case.get("p1x", 1.0)) + ff(case.get("p1y", 0.0)) +
              ff(case.get("p1z", 1.0)) + ff(case.get("p1w", 1.0))))
    W.append((P2, ff(case.get("p2x", 3.0)) + ff(case.get("p2y", 0.0)) +
              ff(case.get("p2z", 3.0)) + ff(case.get("p2w", 1.0))))
    # point pair + extra vecs + direct idx array
    W.append((PT, ff(case.get("ptx", 1.0)) + ff(case.get("pty", 1.0))))
    W.append((VECX, ff(case.get("vax", 4.0)) + ff(0.0) +
              ff(case.get("vay", 0.0)) + ff(1.0)))
    W.append((VECY, ff(case.get("vbx", 0.0)) + ff(0.0) +
              ff(case.get("vby", 4.0)) + ff(1.0)))
    W.append((IARR, ww(case.get("i0", 0)) + ww(case.get("i1", 1)) +
              ww(case.get("i2", 2)) + ww(0)))
    # BLKCHK agent record: +0x00 vec4 pos1, +0x20 vec4 pos2,
    # +0x108 q -> SUBR; SUBR+0x10C d radius, +0x174 b mode
    ag = bytearray(0x120)
    ag[0x00:0x10] = ff(case.get("ag1x", case.get("p1x", 1.0))) + \
        ff(case.get("ag1y", 0.0)) + \
        ff(case.get("ag1z", case.get("p1z", 1.0))) + ff(1.0)
    ag[0x20:0x30] = ff(case.get("ag2x", case.get("p2x", 3.0))) + \
        ff(case.get("ag2y", 0.0)) + \
        ff(case.get("ag2z", case.get("p2z", 3.0))) + ff(1.0)
    ag[0x108:0x110] = qw(case.get("subp", SUBR))
    ag[0xE0:0xE8] = qw(case.get("ge0", 0))
    ag[0xF0:0xF8] = qw(case.get("gf0", CTXA))
    W.append((AGENT, bytes(ag)))
    sub = bytearray(0x180)
    sub[0x10C:0x110] = ff(case.get("radius", 0.0))
    sub[0x110:0x114] = ff(case.get("rad2", 0.0))
    sub[0x174] = case.get("mode", 0) & 0xFF
    W.append((SUBR, bytes(sub)))
    # PVAL stack args: entry rsp = STACK+0x80000; cap @+0x28,
    # flags @+0x30 (read as [rbp+0x40]/[rbp+0x48], rbp=rsp-0x18)
    W.append((STACK + 0x80028, ff(case.get("cap", 0.5))))
    W.append((STACK + 0x80030, dw(case.get("pvflags", 0))))
    # GATE stack args (direct steps): [entry+0x28]=excl handle,
    # [entry+0x30]=flags dword — override PVAL slots when present
    if "garg5" in case or "gflags" in case:
        W.append((STACK + 0x80028, qw(case.get("garg5", 0))))
        W.append((STACK + 0x80030, dw(case.get("gflags", 0))))
    # matrix / vec buffers for helper-level steps
    mat = bytearray(0x40)
    for i in range(16):
        mat[i * 4:i * 4 + 4] = ff(case.get("m%d" % i,
                                           1.0 if i % 5 == 0 else 0.0))
    W.append((MATB, bytes(mat)))
    W.append((VECQ, ff(case.get("vx", 1.0)) + ff(case.get("vy", 2.0)) +
              ff(case.get("vz", 3.0)) + ff(case.get("vw", 4.0))))
    # ---- EXP-133 LOS grid block + record pools ----
    W.append((LGW, dw(case.get("lgw", 8))))
    W.append((LGH, qw(case.get("lgh", 8))))
    W.append((LEPSX, ff(case.get("lepsx", 0.5))))
    W.append((LEPSZ, ff(case.get("lepsz", 0.5))))
    W.append((LCSZ, ff(case.get("lcsz", 4.0))))
    W.append((LRLEN, dw(case.get("lrlen", 0x30))))
    W.append((LLSRC, qw(case.get("llsrc", LSRCA))))
    W.append((LCFLG, qw(case.get("lcflg", CFLGA))))
    W.append((LBMSK, qw(case.get("lbmsk", BMSKA))))
    W.append((IATMSET, qw(MSET)))
    W.append((IATAT2, qw(AT2)))
    # cell-flag map + per-cell record bitmasks
    W.append((CFLGA, bytes(case.get("cflags", [0] * 0x100))))
    lsrc = bytearray(0x8000)
    for ci, m in case.get("lsrc", {}).items():
        o = ci * case.get("lrlen", 0x30)
        lsrc[o:o + len(m)] = bytes(m)
    W.append((LSRCA, bytes(lsrc)))
    # nav-record root: +0x188 vtx pool ptr, +0x1a0 rec pool ptr
    nro = bytearray(0x200)
    nro[0x188:0x190] = qw(case.get("vexp", VEXP))
    nro[0x1a0:0x1a8] = qw(case.get("recp", RECP))
    W.append((NRO, bytes(nro)))
    W.append((NRROOT, qw(case.get("nroot", NRO))))
    # 16B-stride rec pool: w pad@0, w vtxidx@2, w x@4, w y@6, w z@8
    recs = bytearray(0x800)
    for i, r in enumerate(case.get("recs", [])):
        o = i * 0x10
        recs[o + 2:o + 4] = ww(r[0])
        recs[o + 4:o + 6] = ww(r[1])
        recs[o + 6:o + 8] = ww(r[2])
        recs[o + 8:o + 10] = ww(r[3])
    W.append((RECP, bytes(recs)))
    # 64B-stride vtx pool: +0x20/+0x28 atan2 args, +0x30..38 out
    vtxs = bytearray(0x2000)
    for i, v in enumerate(case.get("vtxs", [])):
        o = i * 0x40
        for k, f in enumerate(v):
            vtxs[o + 0x20 + k * 4:o + 0x24 + k * 4] = ff(f)
    W.append((VEXP, bytes(vtxs)))
    # standalone capsule arg vecs (floats at 4B lanes):
    # seg {p1v4@0, p2v4@0x10, srad@0x20}; edge/pt {x,y,z,w@0x30,
    # rad/e10@0x40, e14@0x44, ang@0x48}; out bufs +0x100/+0x200
    W.append((SEGV, b"".join(ff(f) for f in
                             case.get("segv", [0.0] * 0x100))))
    # ---- EXP-135 gate object pool / collector records ----
    W.append((GTPOOL, qw(case.get("gtpool", GTPA))))
    W.append((GTPCNT, dw(case.get("gtcnt", 4))))
    W.append((MABEF, bb(case.get("mabef", 0))))
    gtp = bytearray(0x2000)
    for i, v in enumerate(case.get("gtab", [0])):
        gtp[i * 0xF50 + 8:i * 0xF50 + 0xC] = dw(v)
    W.append((GTPA, bytes(gtp)))
    # collector record count + GHND handle array
    W.append((GRCNT, dw(case.get("grcnt", 0))))
    for i, h in enumerate(case.get("ghnd", [])):
        W.append((GHND + i * 8, qw(h)))
    # gate ctx object (r9): +0xEA9 idx, +0x10 sub, +0x698,
    # +0xE68, +0x1F4 mode
    ctxo = bytearray(0x1000)
    ctxo[0x10:0x18] = qw(case.get("ctx_sub", 0))
    ctxo[0x698:0x6A0] = qw(case.get("ctx_i698", 0))
    ctxo[0xE68:0xE70] = qw(case.get("ctx_e68", 0))
    ctxo[0x1F4] = case.get("ctx_mode", 0) & 0xFF
    ctxo[0xEA9] = case.get("ctx_ea9", 0) & 0xFF
    W.append((CTXA, bytes(ctxo)))
    # ---- EXP-136 subsystem globals + MABESP handle table ----
    # q[0x209A678] = subsystem table (OSUB/DE100), q[0x2EC1378]
    # = AGENTQ query table (NRROOT q[0x209A670] is the flag)
    W.append((SUBTB, qw(case.get("subtb", SUBR))))
    W.append((AGQTB, qw(case.get("agqtb", SUBR))))
    # MABESP table rec (N63FF0 -> MSPT): q+0 flag, q+8 entry
    # array, d+0x20 bound, b+0x10 enable; MSPA: d+0 bound,
    # q[8+i*8] entries, w[entry+0x16] generation
    W.append((MSPT, ob(0x100, q0=1, q8=MSPA, b10=1,
                       d20=case.get("mspn", 0x100))))
    arr = bytearray(0x2000)
    arr[0:4] = dw(case.get("mspn", 0x100))
    for i, o in case.get("msparr", {}).items():
        arr[8 + i * 8:8 + i * 8 + 8] = qw(o)
    W.append((MSPA, bytes(arr)))
    # generic object/substruct plants: (addr, bytes)
    for addr, dat in case.get("gplants", []):
        W.append((addr, bytes(dat)))
    return W


class World:
    def __init__(self, case, raw, secs):
        self.case = case
        self.raw, self.secs = raw, secs
        self.uc = Uc(UC_ARCH_X86, UC_MODE_64)
        gm = self.gm = GuestMem(self.uc)
        gm.map(IMG_LO, IMG_HI - IMG_LO)
        for sva, vs, ra, rs in secs:
            if vs and rs:
                gm.w(IMG_LO + sva, raw[ra:ra + min(rs, vs)])
        gm.map(HEAP, 0x100000)
        gm.map(STACK, 0x100000)
        gm.map(RETQ, 0x1000)
        gm.map(FDC, 0x1000, b"\xc3" * 0x1000)
        for t in (SQF, ISN, FIN, COS, SIN, MSET, AT2):
            gm.map(t, 0x1000, b"\xc3" * 0x1000)
        for addr, dat in build_fixture(case):
            gm.w(addr, dat)
        for addr, dat in case.get("patch_bytes", []):
            gm.w(addr, dat)
        self.trace, self.faults, self.rets, self.ends = [], [], [], []
        self.agrets = list(case.get("agrets", [0]))
        self.gatrets = list(case.get("gatrets", [0]))
        self.derets = list(case.get("derets", [1]))
        self.opbrets = list(case.get("opbrets", []))
        self.f50vs = list(case.get("f50v", [0]))
        self.of60rets = list(case.get("of60rets", []))
        self.t3frets = list(case.get("t3frets", [MSPT]))
        self.w19rets = list(case.get("w19rets", [0]))
        self.uc.hook_add(UC_HOOK_CODE, self.on_code)
        self.uc.hook_add(UC_HOOK_MEM_UNMAPPED, self.on_bad)
        self.uc.hook_add(UC_HOOK_INTR, self.on_intr)

    def _ret(self, uc):
        uc.reg_write(UC_X86_REG_RIP,
                     self.gm.qw(uc.reg_read(UC_X86_REG_RSP)))
        uc.reg_write(UC_X86_REG_RSP,
                     uc.reg_read(UC_X86_REG_RSP) + 8)

    def on_intr(self, uc, intno, _):
        self.faults.append(("trap", uc.reg_read(UC_X86_REG_RIP)))
        uc.emu_stop()

    def on_bad(self, uc, access, addr, size, value, _):
        kind = "memr" if access in (16, 19) else \
               "memf" if access in (18, 21) else "memw"
        self.faults.append((kind, addr, size))
        uc.emu_stop()
        return True

    def on_code(self, uc, addr, size, _):
        if addr == FDC:
            x = uc.reg_read(UC_X86_REG_XMM0)
            lo = x & 0xFFFFFFFF
            r = fdclass_f32(lo)
            uc.reg_write(UC_X86_REG_RAX, r & 0xFFFFFFFFFFFFFFFF)
            self.trace.append("fdc:%x:%d" % (lo, r))
            self._ret(uc)
        elif addr == SQF:
            x = uc.reg_read(UC_X86_REG_XMM0)
            lo = x & 0xFFFFFFFF
            r = sqrtf_bits(lo)
            uc.reg_write(UC_X86_REG_XMM0,
                         (x & ~0xFFFFFFFF) | (r & 0xFFFFFFFF))
            self.trace.append("sqrtf:%x:%x" % (lo, r))
            self._ret(uc)
        elif addr == ISN or addr == FIN:
            f = struct.unpack("<d", struct.pack(
                "<Q", uc.reg_read(UC_X86_REG_XMM0) &
                0xFFFFFFFFFFFFFFFF))[0]
            r = 1 if (math.isnan(f) if addr == ISN
                      else math.isfinite(f)) else 0
            uc.reg_write(UC_X86_REG_RAX, r)
            self.trace.append(
                "%s:%x:%d" % ("isnan" if addr == ISN else "finit",
                              uc.reg_read(UC_X86_REG_XMM0) &
                              0xFFFFFFFFFFFFFFFF, r))
            self._ret(uc)
        elif addr == COS or addr == SIN:
            x = uc.reg_read(UC_X86_REG_XMM0)
            lo = x & 0xFFFFFFFF
            r = cosf_bits(lo) if addr == COS else sinf_bits(lo)
            uc.reg_write(UC_X86_REG_XMM0,
                         (x & ~0xFFFFFFFF) | (r & 0xFFFFFFFF))
            self.trace.append(
                "%s:%x:%x" % ("cosf" if addr == COS else "sinf",
                              lo, r))
            self._ret(uc)
        elif addr == MSET:
            dst = uc.reg_read(UC_X86_REG_RCX)
            val = uc.reg_read(UC_X86_REG_RDX) & 0xFF
            cnt = uc.reg_read(UC_X86_REG_R8) & 0xFFFFFFFFFFFFFFFF
            self.gm.w(dst, bytes([val]) * cnt)
            self.trace.append("mset:%x:%x:%x" % (dst, val, cnt))
            self._ret(uc)
        elif addr == AT2:
            y = uc.reg_read(UC_X86_REG_XMM0) & 0xFFFFFFFF
            x = uc.reg_read(UC_X86_REG_XMM1) & 0xFFFFFFFF
            r = atan2f_bits(y, x)
            x0 = uc.reg_read(UC_X86_REG_XMM0)
            uc.reg_write(UC_X86_REG_XMM0,
                         (x0 & ~0xFFFFFFFF) | (r & 0xFFFFFFFF))
            self.trace.append("at2:%x:%x:%x" % (y, x, r))
            self._ret(uc)
        elif addr == N7C20:
            r = self.of60rets.pop(0) if self.of60rets else 0
            uc.reg_write(UC_X86_REG_RAX, r & 0xFFFFFFFFFFFFFFFF)
            self.trace.append("bfl:%x:%x" % (
                uc.reg_read(UC_X86_REG_RCX), r))
            self._ret(uc)
        elif addr == N14F50:
            r = self.opbrets.pop(0) if self.opbrets else 0
            v = self.f50vs.pop(0) if self.f50vs else 0
            outp = uc.reg_read(UC_X86_REG_R9)
            try:
                self.gm.w(outp, dw(v))
            except KeyError:
                self.faults.append(("memw", outp, 4))
                uc.emu_stop()
                return
            uc.reg_write(UC_X86_REG_RAX, r & 0xFFFFFFFFFFFFFFFF)
            self.trace.append("f50:%x:%x:%x:%x:%x:%x" % (
                uc.reg_read(UC_X86_REG_RCX),
                uc.reg_read(UC_X86_REG_RDX),
                uc.reg_read(UC_X86_REG_R8),
                outp, v & 0xFFFFFFFF, r & 0xFFFFFFFF))
            self._ret(uc)
        elif addr == N63FF0:
            r = self.t3frets.pop(0) if self.t3frets else MSPT
            uc.reg_write(UC_X86_REG_RAX, r & 0xFFFFFFFFFFFFFFFF)
            self.trace.append("t3f:%x:%x" % (
                uc.reg_read(UC_X86_REG_RCX) & 0xFFFFFFFF, r))
            self._ret(uc)
        elif addr == N31900:
            r = self.w19rets.pop(0) if self.w19rets else 0
            uc.reg_write(UC_X86_REG_RAX, r & 0xFFFF)
            self.trace.append("n19:%x:%x:%x:%x" % (
                uc.reg_read(UC_X86_REG_RCX),
                uc.reg_read(UC_X86_REG_RDX),
                uc.reg_read(UC_X86_REG_R8), r & 0xFFFF))
            self._ret(uc)
        elif addr == N31820:
            uc.reg_write(UC_X86_REG_RAX, 0)
            self.trace.append("n18:%x:%x:%x" % (
                uc.reg_read(UC_X86_REG_RCX),
                uc.reg_read(UC_X86_REG_RDX),
                uc.reg_read(UC_X86_REG_R8)))
            self._ret(uc)
        elif addr == N31400:
            r = self.derets.pop(0) if self.derets else 0
            uc.reg_write(UC_X86_REG_RAX, r & 0xFFFFFFFFFFFFFFFF)
            self.trace.append("de1:%x:%x:%x:%x:%x" % (
                uc.reg_read(UC_X86_REG_RCX),
                uc.reg_read(UC_X86_REG_RDX),
                uc.reg_read(UC_X86_REG_R8),
                uc.reg_read(UC_X86_REG_R9), r))
            self._ret(uc)
        elif addr == N315E0:
            r = self.agrets.pop(0) if self.agrets else 0
            uc.reg_write(UC_X86_REG_RAX, r & 0xFFFFFFFFFFFFFFFF)
            self.trace.append("agq:%x:%x:%x:%x:%x" % (
                uc.reg_read(UC_X86_REG_RCX),
                uc.reg_read(UC_X86_REG_RDX),
                uc.reg_read(UC_X86_REG_R8),
                uc.reg_read(UC_X86_REG_R9), r))
            self._ret(uc)

    def run_one(self, entry, rcx, rdx=0, r8=0, r9=0,
                xmm0=0, xmm2=0, xmm1=0, xmm3=0):
        uc = self.uc
        self.gm.w(RETQ, b"\xc3" * 0x100)
        rsp = STACK + 0x80000
        self.gm.w(rsp, qw(RETQ))
        uc.reg_write(UC_X86_REG_RSP, rsp)
        uc.reg_write(UC_X86_REG_RCX, rcx)
        uc.reg_write(UC_X86_REG_RDX, rdx)
        uc.reg_write(UC_X86_REG_R8, r8)
        uc.reg_write(UC_X86_REG_R9, r9)
        uc.reg_write(UC_X86_REG_XMM0, xmm0 & 0xFFFFFFFFFFFFFFFF)
        uc.reg_write(UC_X86_REG_XMM2, xmm2 & 0xFFFFFFFFFFFFFFFF)
        uc.reg_write(UC_X86_REG_XMM1, xmm1 & 0xFFFFFFFFFFFFFFFF)
        uc.reg_write(UC_X86_REG_XMM3, xmm3 & 0xFFFFFFFFFFFFFFFF)
        try:
            uc.emu_start(entry, RETQ, count=300000)
        except UcError as e:
            if not self.faults:
                self.faults.append(("emuerr", str(e)))
        self.ends.append(uc.reg_read(UC_X86_REG_RIP))
        self.rets.append(uc.reg_read(UC_X86_REG_RAX))

    def run(self):
        for step in self.case.get("steps", []):
            entry, rcx = step[0], step[1]
            rdx = step[2] if len(step) > 2 else 0
            r8 = step[3] if len(step) > 3 else 0
            r9 = step[4] if len(step) > 4 else 0
            xmm0 = step[5] if len(step) > 5 else 0
            xmm2 = step[6] if len(step) > 6 else 0
            xmm1 = step[7] if len(step) > 7 else 0
            xmm3 = step[8] if len(step) > 8 else 0
            self.run_one(entry, rcx, rdx, r8, r9,
                         xmm0, xmm2, xmm1, xmm3)

    def obs(self):
        mem = {}
        for addr, n in self.case.get("watch", []):
            try:
                mem["%x" % addr] = self.gm.r(addr, n).hex()
            except KeyError:
                mem["%x" % addr] = None
        return {"trace": self.trace, "faults": self.faults,
                "rets": self.rets, "ends": self.ends, "mem": mem}


# ---------------- python model ----------------

VALID = ((HEAP, HEAP + 0x100000), (IMG_LO, IMG_HI),
         (STACK, STACK + 0x100000))


class Model:
    def __init__(self, case, raw, secs):
        self.case = case
        self.raw, self.secs = raw, secs
        self.mem = {}
        for addr, dat in build_fixture(case):
            for i, b in enumerate(dat):
                self.mem[addr + i] = b
        for addr, dat in case.get("patch_bytes", []):
            for i, b in enumerate(dat):
                self.mem[addr + i] = b
        self.trace, self.faults, self.rets, self.ends = [], [], [], []
        self.fault_end = RETQ
        self._rax = 0
        self.agrets = list(case.get("agrets", [0]))
        self.gatrets = list(case.get("gatrets", [0]))
        self.derets = list(case.get("derets", [1]))
        self.opbrets = list(case.get("opbrets", []))
        self.f50vs = list(case.get("f50v", [0]))
        self.of60rets = list(case.get("of60rets", []))
        self.t3frets = list(case.get("t3frets", [MSPT]))
        self.w19rets = list(case.get("w19rets", [0]))

    # memory
    def mb(self, a):
        a &= 0xFFFFFFFFFFFFFFFF
        if a in self.mem:
            return self.mem[a]
        if IMG_LO <= a < IMG_HI:
            try:
                return img_rd(self.raw, self.secs, a, 1)[0]
            except KeyError:
                return 0
        return 0

    def mw(self, a): return self.mb(a) | (self.mb(a + 1) << 8)
    def md(self, a):
        return self.mb(a) | (self.mb(a + 1) << 8) | \
            (self.mb(a + 2) << 16) | (self.mb(a + 3) << 24)
    def mq(self, a): return self.md(a) | (self.md(a + 4) << 32)
    def sb(self, a, v): self.mem[a & 0xFFFFFFFFFFFFFFFF] = v & 0xFF
    def sd(self, a, v):
        for i in range(4):
            self.sb(a + i, (v >> (8 * i)) & 0xFF)
    def sq(self, a, v):
        for i in range(8):
            self.sb(a + i, (v >> (8 * i)) & 0xFF)
    def sf(self, a, v):
        self.sd(a, f2u(v))
    def mf(self, a):
        return u2f(self.md(a))

    def mapped(self, a):
        return any(lo <= a < hi for lo, hi in VALID)

    def _rd(self, a, n, site):
        """ordered read: records ('memr', a, n) + fault_end on
        unmapped and returns None."""
        if not self.mapped(a):
            self.faults.append(("memr", a & 0xFFFFFFFFFFFFFFFF, n))
            self.fault_end = site
            return None
        if n == 1:
            return self.mb(a)
        if n == 2:
            return self.mw(a)
        if n == 4:
            return self.md(a)
        return self.mq(a)

    def _wr(self, a, n, site):
        """ordered write check: records ('memw', a, n) + fault_end
        on unmapped; returns False so caller early-returns _rax."""
        if self.mapped(a):
            return True
        self.faults.append(("memw", a & 0xFFFFFFFFFFFFFFFF, n))
        self.fault_end = site
        return False

    def _sd_flt(self, a, v, site):
        """dword store with fault check."""
        if not self._wr(a, 4, site):
            return False
        self.sd(a, v)
        return True

    def _sf_flt(self, a, v, site):
        """float store with fault check."""
        if not self._wr(a, 4, site):
            return False
        self.sf(a, v)
        return True

    def _rd16(self, a, site):
        """movaps 16B read: (lo, hi) qwords or None + fault."""
        if not self.mapped(a):
            self.faults.append(("memr", a & 0xFFFFFFFFFFFFFFFF, 16))
            self.fault_end = site
            return None
        if not self.mapped(a + 15):
            self.faults.append(
                ("memr", (a + 8) & 0xFFFFFFFFFFFFFFFF, 8))
            self.fault_end = site
            return None
        return self.mq(a), self.mq(a + 8)

    def _wr16(self, a, v, site):
        """movdqa 16B store of a (lo, hi) pair; fault-checked."""
        if not self.mapped(a):
            self.faults.append(("memw", a & 0xFFFFFFFFFFFFFFFF, 16))
            self.fault_end = site
            return False
        if not self.mapped(a + 15):
            self.faults.append(
                ("memw", (a + 8) & 0xFFFFFFFFFFFFFFFF, 8))
            self.fault_end = site
            return False
        self.sq(a, v[0])
        self.sq(a + 8, v[1])
        return True

    def _sq_flt(self, a, v, site):
        """qword store with fault check."""
        if not self._wr(a, 8, site):
            return False
        self.sq(a, v)
        return True

    # ---------- scripted boundaries ----------
    def fdc(self, u):
        r = fdclass_f32(u)
        self.trace.append("fdc:%x:%d" % (u & 0xFFFFFFFF, r))
        return r

    def sqrtf(self, u):
        r = sqrtf_bits(u)
        self.trace.append("sqrtf:%x:%x" % (u & 0xFFFFFFFF,
                                           r & 0xFFFFFFFF))
        return u2f(r)

    def cosf(self, u):
        r = cosf_bits(u)
        self.trace.append("cosf:%x:%x" % (u & 0xFFFFFFFF,
                                          r & 0xFFFFFFFF))
        return u2f(r)

    def sinf(self, u):
        r = sinf_bits(u)
        self.trace.append("sinf:%x:%x" % (u & 0xFFFFFFFF,
                                          r & 0xFFFFFFFF))
        return u2f(r)

    def isnan_f64(self, f):
        u = struct.unpack("<Q", struct.pack("<d", f))[0]
        r = 1 if math.isnan(f) else 0
        self.trace.append("isnan:%x:%d" % (u, r))
        return r

    def isfinite_f64(self, f):
        u = struct.unpack("<Q", struct.pack("<d", f))[0]
        r = 1 if math.isfinite(f) else 0
        self.trace.append("finit:%x:%d" % (u, r))
        return r

    def agq(self, obj, out, a3, a4):
        """00318CA0 — rcx=q[0x2EC1378]; ==0 -> -1; else
        cwde(N315E0(rcx,obj,out,a4))."""
        t = self._rd(AGQTB, 8, 0x318CA7)
        if t is None:
            return self._rax
        if t == 0:
            self._rax = 0xFFFFFFFF
            return self._rax
        r = self.n15(t, obj, out, a4)
        if self.faults:
            return self._rax
        ax = r & 0xFFFF
        self._rax = (ax | 0xFFFF0000) if ax & 0x8000 else ax
        return self._rax

    def de100(self, rcx, rdx, r8):
        """0026E100 — rcx=q[0x209A670]?q[0x209A678]:0; rdx=arg1;
        r8=zx(arg2); r9=arg3; tail N31400."""
        root = self._rd(NRROOT, 8, 0x26E10C)
        if root is None:
            return self._rax
        t = self._rd(SUBTB, 8, 0x26E116)
        if t is None:
            return self._rax
        tab = t if root != 0 else 0
        r = self.n14(tab, rcx, rdx & 0xFFFF, r8)
        if self.faults:
            return self._rax
        self._rax = r
        return r

    def mset(self, dst, val, cnt):
        """memset trampoline — writes into model memory."""
        cnt &= 0xFFFFFFFFFFFFFFFF
        for i in range(cnt):
            self.sb(dst + i, val & 0xFF)
        self.trace.append("mset:%x:%x:%x" % (
            dst & 0xFFFFFFFFFFFFFFFF, val & 0xFF, cnt))

    def at2(self, uy, ux):
        r = atan2f_bits(uy, ux)
        self.trace.append("at2:%x:%x:%x" % (uy & 0xFFFFFFFF,
                                            ux & 0xFFFFFFFF,
                                            r & 0xFFFFFFFF))
        return u2f(r)

    # ---------- EXP-136 scripted boundaries (one hop deeper) --
    def n7c(self, o):
        """00377C20 entry-intercept — OF60's bitfield lookup;
        eax planted per case."""
        r = self.of60rets.pop(0) if self.of60rets else 0
        self.trace.append("bfl:%x:%x" % (o & 0xFFFFFFFFFFFFFFFF,
                                         r))
        return r

    def f50(self, a, b, c, outp):
        """00314F50 entry-intercept — eax planted (opbrets);
        f[outp] = planted f50v."""
        r = self.opbrets.pop(0) if self.opbrets else 0
        v = self.f50vs.pop(0) if self.f50vs else 0
        if not self._sd_flt(outp, v, N14F50):
            return self._rax
        self.trace.append("f50:%x:%x:%x:%x:%x:%x" % (
            a & 0xFFFFFFFFFFFFFFFF, b & 0xFFFFFFFFFFFFFFFF,
            c & 0xFFFFFFFFFFFFFFFF, outp & 0xFFFFFFFFFFFFFFFF,
            v & 0xFFFFFFFF, r & 0xFFFFFFFF))
        return r

    def t3f(self, sel):
        """00263FF0 entry-intercept — MABESP table select;
        rax planted (t3frets, default MSPT)."""
        r = self.t3frets.pop(0) if self.t3frets else MSPT
        self.trace.append("t3f:%x:%x" % (sel & 0xFFFFFFFF, r))
        return r

    def n19(self, t, vec, fl):
        """00231900 entry-intercept — OSUB stage-1; ax planted."""
        r = self.w19rets.pop(0) if self.w19rets else 0
        self.trace.append("n19:%x:%x:%x:%x" % (
            t & 0xFFFFFFFFFFFFFFFF, vec & 0xFFFFFFFFFFFFFFFF,
            fl & 0xFFFFFFFFFFFFFFFF, r & 0xFFFF))
        return r & 0xFFFF

    def n18(self, t, vec, idx):
        """00231820 entry-intercept — OSUB stage-2; ret dead."""
        self.trace.append("n18:%x:%x:%x" % (
            t & 0xFFFFFFFFFFFFFFFF, vec & 0xFFFFFFFFFFFFFFFF,
            idx & 0xFFFFFFFFFFFFFFFF))
        return 0

    def n14(self, tab, obj, idx, fl):
        """00231400 entry-intercept — DE100's dispatcher;
        eax planted (derets)."""
        r = self.derets.pop(0) if self.derets else 0
        self.trace.append("de1:%x:%x:%x:%x:%x" % (
            tab & 0xFFFFFFFFFFFFFFFF, obj & 0xFFFFFFFFFFFFFFFF,
            idx & 0xFFFFFFFFFFFFFFFF, fl & 0xFFFFFFFFFFFFFFFF, r))
        return r

    def n15(self, tab, obj, out, fl):
        """002315E0 entry-intercept — AGENTQ's query;
        eax planted (agrets), caller cwde's."""
        r = self.agrets.pop(0) if self.agrets else 0
        self.trace.append("agq:%x:%x:%x:%x:%x" % (
            tab & 0xFFFFFFFFFFFFFFFF, obj & 0xFFFFFFFFFFFFFFFF,
            out & 0xFFFFFFFFFFFFFFFF, fl & 0xFFFFFFFFFFFFFFFF, r))
        return r

    # ---------- EXP-136 real bodies (object accessors) -------
    def objd(self, h):
        """00263E30 — rax = q[h+0x30]."""
        r = self._rd(h + 0x30, 8, 0x263E30)
        if r is None:
            return self._rax
        self._rax = r
        return r

    def o3fw(self, o, p1, p2, p3):
        """002646C0 — v=b[+3]>>5: v1 copy d[qB8+0/4/8]; v3 copy +
        (b[+0x107]&1: addss f[+0x40/44/48]); else zero outs."""
        if o == 0:
            return                              # je ret
        v = self._rd(o + 3, 1, 0x2646C9)
        if v is None:
            return
        v = (v >> 5) - 1
        if v == 0:                              # variant 1: copy
            rc = self._rd(o + 0xB8, 8, 0x264735)
            if rc is None:
                return
            for off, p, sr, sw in ((0, p1, 0x26473C, 0x26473E),
                                   (4, p2, 0x264740, 0x264743),
                                   (8, p3, 0x264746, 0x264749)):
                x = self._rd(rc + off, 4, sr)
                if x is None:
                    return
                self._rax = x                   # mov eax,d[rc+off]
                if not self._sd_flt(p, x, sw):
                    return
            return
        if v == 2:                              # variant 3: copy+add
            rc = self._rd(o + 0xB8, 8, 0x2646E9)
            if rc is None:
                return
            for off, p, sr, sw in ((0, p1, 0x2646F0, 0x2646F2),
                                   (4, p2, 0x2646F4, 0x2646F7),
                                   (8, p3, 0x2646FA, 0x2646FD)):
                x = self._rd(rc + off, 4, sr)
                if x is None:
                    return
                self._rax = x                   # mov eax,d[rc+off]
                if not self._sd_flt(p, x, sw):
                    return
            t = self._rd(rc + 0x107, 1, 0x264700)
            if t is None:
                return
            if not (t & 1):
                return
            for off, p, sr, sr2, sw in (
                    (0x40, p1, 0x264709, 0x26470E, 0x264712),
                    (0x44, p2, 0x264716, 0x26471B, 0x264720),
                    (0x48, p3, 0x264725, 0x26472A, 0x26472F)):
                x = self._rd(rc + off, 4, sr)
                if x is None:
                    return
                y = self._rd(p, 4, sr2)
                if y is None:
                    return
                # addss xmm_dst=field bits, src=[p]
                if not self._sf_flt(p, _a(u2f(x), u2f(y)), sw):
                    return
            return
        self._rax = 0                           # xor eax,eax
        for p, sw in ((p1, 0x2646E0), (p2, 0x2646E2),
                      (p3, 0x2646E5)):
            if not self._sd_flt(p, 0, sw):
                return

    def da710(self, rc, p1, p2):
        """003DA710 — d[rc]->[rdx], d[rc+4]->[r8] (nonnull)."""
        if p1 != 0:
            x = self._rd(rc, 4, 0x3DA715)
            if x is None:
                return
            self._rax = x                       # mov eax,d[rc]
            if not self._sd_flt(p1, x, 0x3DA717):
                return
        if p2 != 0:
            x = self._rd(rc + 4, 4, 0x3DA71E)
            if x is None:
                return
            self._rax = x                       # mov eax,d[rc+4]
            if not self._sd_flt(p2, x, 0x3DA721):
                return

    def o2fw(self, o, p1, p2):
        """00265090 — (b[+3]&0xE0)==0x60 -> DA710(qB8+0x50)."""
        v = self._rd(o + 3, 1, 0x265090)
        if v is None:
            return
        self._rax = v & 0xE0                    # movzx+and
        if (v & 0xE0) != 0x60:
            return
        rc = self._rd(o + 0xB8, 8, 0x26509A)
        if rc is None:
            return
        self.da710(rc + 0x50, p1, p2)

    def o1f(self, o):
        """00265200 — v1 f[qB8+0x38]; v3 f[qB8+0xA8]; else 0."""
        if o == 0:
            return 0
        v = self._rd(o + 3, 1, 0x265205)
        if v is None:
            return 0
        v = (v >> 5) - 1
        if v == 0:
            rc = self._rd(o + 0xB8, 8, 0x265226)
            if rc is None:
                return 0
            self._rax = rc
            return self._rd(rc + 0x38, 4, 0x26522D)
        if v == 2:
            rc = self._rd(o + 0xB8, 8, 0x265216)
            if rc is None:
                return 0
            self._rax = rc
            return self._rd(rc + 0xA8, 4, 0x26521D)
        return 0

    def o1f2(self, o):
        """00263940 — v1 f[qB8+0x68]; v3 f[qB8+0xC0]*f[qB8+0x24];
        else 0. No null guard — b[+3] read faults."""
        v = self._rd(o + 3, 1, 0x263940)
        if v is None:
            return 0
        v = (v >> 5) - 1
        if v == 0:
            rc = self._rd(o + 0xB8, 8, 0x26396A)
            if rc is None:
                return 0
            self._rax = rc
            return self._rd(rc + 0x68, 4, 0x263971)
        if v == 2:
            rc = self._rd(o + 0xB8, 8, 0x263951)
            if rc is None:
                return 0
            self._rax = rc
            x = self._rd(rc + 0xC0, 4, 0x263958)
            if x is None:
                return 0
            y = self._rd(rc + 0x24, 4, 0x263960)
            if y is None:
                return 0
            # mulss xmm_dst=fC0, src=f24
            return f2u(_m(u2f(x), u2f(y)))
        return 0

    def o1f3(self, o):
        """00265830 — (b[+3]&0xE0)==0x60 -> f[q[qB8+0xF0]+0x24];
        else 0. No null guard."""
        v = self._rd(o + 3, 1, 0x265830)
        if v is None:
            return 0
        self._rax = v & 0xE0                    # movzx+and
        if (v & 0xE0) != 0x60:
            return 0
        rc = self._rd(o + 0xB8, 8, 0x26583E)
        if rc is None:
            return 0
        self._rax = rc                          # mov rax,qB8
        f0 = self._rd(rc + 0xF0, 8, 0x265845)
        if f0 is None:
            return 0
        return self._rd(f0 + 0x24, 4, 0x26584C)

    def ovf(self, o):
        """002E9FE0 — (b[+3]&0xE0)!=0x60 -> 1; else +0xC0 flags:
        null||d[+0x164] -> 0; b11&0x20 ? b10&3==3 : b10&0xB==0xB;
        ret (b11&6)==6."""
        v = self._rd(o + 3, 1, 0x2E9FE0)
        if v is None:
            return self._rax
        if (v & 0xE0) != 0x60:
            self._rax = 1
            return 1
        c = self._rd(o + 0xC0, 8, 0x2E9FF0)
        if c is None:
            return self._rax
        if c == 0:
            self._rax = 0
            return 0
        d = self._rd(c + 0x164, 4, 0x2E9FFC)
        if d is None:
            return self._rax
        if d != 0:
            self._rax = 0
            return 0
        b11 = self._rd(c + 0x11, 1, 0x2EA005)
        if b11 is None:
            return self._rax
        b10 = self._rd(c + 0x10, 1, 0x2EA009)
        if b10 is None:
            return self._rax
        if b11 & 0x20:
            ok = (b10 & 3) == 3
        else:
            ok = (b10 & 0xB) == 0xB
        if not ok:
            self._rax = 0
            return 0
        r = 1 if (b11 & 6) == 6 else 0
        self._rax = r
        return r

    def a6a0(self, o):
        """002646A0 — o -> q[+0xC0] -> q[+0x138] (null-safe)."""
        if o == 0:
            return 0
        c = self._rd(o + 0xC0, 8, 0x2646A5)
        if c is None:
            return self._rax
        if c == 0:
            return 0
        r = self._rd(c + 0x138, 8, 0x2646B1)
        if r is None:
            return self._rax
        self._rax = r
        return r

    def opa(self, a, b):
        """00314EB0 — r10=a->+0xC0->+0x138, r9=b->+0xC0->+0x138;
        b[r10+6]==b[r9+6] required; b[r10+0x119]==0 -> 1;
        !=0&&==b[r9+0x119] -> 0; else 1."""
        r10 = 0
        if a != 0:
            c = self._rd(a + 0xC0, 8, 0x314EBE)
            if c is None:
                return self._rax
            if c != 0:
                r10 = self._rd(c + 0x138, 8, 0x314ECA)
                if r10 is None:
                    return self._rax
        r9 = 0
        if b != 0:
            c = self._rd(b + 0xC0, 8, 0x314ED6)
            if c is None:
                return self._rax
            if c != 0:
                r9 = self._rd(c + 0x138, 8, 0x314EE2)
                if r9 is None:
                    return self._rax
        if r10 == 0 or r9 == 0:
            self._rax = 0
            return 0
        x = self._rd(r9 + 6, 1, 0x314EF3)
        if x is None:
            return self._rax
        y = self._rd(r10 + 6, 1, 0x314EF8)
        if y is None:
            return self._rax
        if y != x:
            self._rax = 0
            return 0
        al = self._rd(r10 + 0x119, 1, 0x314EFE)
        if al is None:
            return self._rax
        if al == 0:
            self._rax = 1
            return 1
        z = self._rd(r9 + 0x119, 1, 0x314F0A)
        if z is None:
            return self._rax
        if al == z:
            self._rax = 0
            return 0
        self._rax = 1
        return 1

    def opb(self, a, b, outp, vsp):
        """00313F80 — rsi=A6A0(a), rax=A6A0(b); either 0 -> 0;
        eax=F50(rsi,rax,0,&tmp); outp!=0 -> f[outp]=f[tmp].
        vsp = entry rsp; tmp = vsp-0x28+0x48 = vsp+0x20."""
        if not self._wr(vsp + 8, 8, 0x313F80):
            return self._rax
        if not self._wr(vsp + 0x10, 8, 0x313F85):
            return self._rax
        if not self._wr(vsp - 8, 8, 0x313F8A):
            return self._rax
        si = self.a6a0(a)
        if self.faults:
            return self._rax
        ax = self.a6a0(b)
        if self.faults:
            return self._rax
        self._rax = ax
        if si == 0 or ax == 0:
            return 0
        TMP = vsp + 0x20
        r = self.f50(si, ax, 0, TMP)
        if self.faults:
            return self._rax
        if outp != 0:
            x = self._rd(TMP, 4, 0x313FC7)
            if x is None:
                return self._rax
            if not self._sd_flt(outp, x, 0x313FCD):
                return self._rax
        self._rax = r & 0xFFFFFFFFFFFFFFFF
        return r

    def of60(self, o):
        """00313F60 — tail-jump to scripted 00377C20."""
        return self.n7c(o)

    def osub(self, vec):
        """0026E350 — q[0x209A670]==0 -> -1; t=q[0x209A678]==0 ->
        -1; ax=N31900(t,vec,1)<0 -> -1; N31820(t,vec,ax); ret 0."""
        root = self._rd(NRROOT, 8, 0x26E356)
        if root is None:
            return self._rax
        if root == 0:
            self._rax = 0xFFFFFFFF
            return self._rax
        t = self._rd(SUBTB, 8, 0x26E368)
        if t is None:
            return self._rax
        if t == 0:
            self._rax = 0xFFFFFFFF
            return self._rax
        ax = self.n19(t, vec, 1) & 0xFFFF
        if self.faults:
            return self._rax
        if ax & 0x8000:
            self._rax = 0xFFFFFFFF
            return self._rax
        self.n18(t, vec, ax)
        self._rax = 0
        return 0

    def mabesp(self, ecx):
        """003588B0 — handle decode: sel=(ecx>>0x10)&0xF <5;
        T=N63FF0(sel); arr=q[T+8]; bounds+flag checks; entry
        q[arr+8+id*8] iff w[entry+0x16]==(ecx>>0x14)&0x7FF."""
        ecx &= 0xFFFFFFFF
        if ecx == 0:
            self._rax = 0
            return 0
        idx = ecx & 0xFFFF
        bank = (ecx >> 0x14) & 0x7FF
        sel = (ecx >> 0x10) & 0xF
        if sel >= 5:
            self._rax = 0
            return 0
        t = self.t3f(sel)
        if self.faults:
            return self._rax
        arr = self._rd(t + 8, 8, 0x3588EB)
        if arr is None:
            return self._rax
        if arr == 0:
            self._rax = 0
            return 0
        q0 = self._rd(t, 8, 0x3588F4)
        if q0 is None:
            return self._rax
        if q0 == 0:
            self._rax = 0
            return 0
        d20 = self._rd(t + 0x20, 4, 0x3588FA)
        if d20 is None:
            return self._rax
        if idx >= d20:
            self._rax = 0
            return 0
        fl = self._rd(t + 0x10, 1, 0x3588FF)
        if fl is None:
            return self._rax
        if not (fl & 1):
            self._rax = 0
            return 0
        cap = self._rd(arr, 4, 0x358905)
        if cap is None:
            return self._rax
        if idx >= cap:
            self._rax = 0
            return 0
        o = self._rd(arr + 8 + idx * 8, 8, 0x358909)
        if o is None:
            return self._rax
        if o == 0:
            self._rax = 0
            return 0
        g = self._rd(o + 0x16, 2, 0x358913)
        if g is None:
            return self._rax
        self._rax = o if g == bank else 0
        return self._rax

    # ---------- bodies ----------
    def base(self, i):
        """0020E600 — rax = ecx + q[0x1F83530]."""
        return (i + self.mq(BASECELL)) & 0xFFFFFFFFFFFFFFFF

    def eclass(self, cls, flag):
        """0026E300 — cl = classtab[sx16(flag)]; <0 -> -1;
        bit 1<<cl vs bitpair[class]: w0&w1 -> 2, w0 -> 1, else 0."""
        idx = flag & 0xFFFF
        if idx >= 0x8000:
            idx -= 0x10000
        cl = self.md(CLSTAB + idx * 4)
        if cl & 0x80000000:
            return 0xFFFFFFFF              # or eax,0xffffffff
        bit = (1 << (cl & 0x1F)) & 0xFFFFFFFF
        i32 = cls & 0xFFFFFFFF               # movsxd r8,ecx
        if i32 >= 0x80000000:
            i32 -= 0x100000000
        pair = (BPTAB + i32 * 8) & 0xFFFFFFFFFFFFFFFF
        if self.md(pair) & bit:
            return 2 if (self.md(pair + 4) & bit) else 1
        return 0

    def ttest(self, idxarr, pt):
        """00382D10 — point-in-triangle over shipped index array
        {0,1,2,0}; same-sign 2D edge crosses -> 1 else 0.
        Ordered reads: w[idxarr+ib*2] first (0x382D7A), then
        va.x/wa/vb.x/va.y/wa/vb.y/pt.x/wa/vb.x/[ucomiss]/wa/pt.y/vb.y."""
        ship = [self.md(TRIIDX + k * 4) for k in range(4)]
        root = self.mq(ROOTCELL)
        coff = self._rd(root + 0xC, 4, 0x382D6B)
        if coff is None:
            return self._rax
        vpool = self.base(coff)
        self._rax = vpool
        acc = 0.0
        for e in range(3):
            ia, ib = ship[e], ship[e + 1]
            wb = self._rd(idxarr + ib * 2, 2, 0x382D7A)
            if wb is None:
                return self._rax
            vax = self._rd(vpool + wb * 8, 4, 0x382D91)
            if vax is None:
                return self._rax
            wa = self._rd(idxarr + ia * 2, 2, 0x382D97)
            if wa is None:
                return self._rax
            vbx = self._rd(vpool + wa * 8, 4, 0x382D9C)
            if vbx is None:
                return self._rax
            ex = f32(u2f(vax) - u2f(vbx))
            vay = self._rd(vpool + wb * 8 + 4, 4, 0x382DCF)
            if vay is None:
                return self._rax
            if self._rd(idxarr + ia * 2, 2, 0x382DD5) is None:
                return self._rax
            vby = self._rd(vpool + wa * 8 + 4, 4, 0x382DDA)
            if vby is None:
                return self._rax
            ey = f32(u2f(vay) - u2f(vby))
            ptx = self._rd(pt, 4, 0x382DF2)
            if ptx is None:
                return self._rax
            if self._rd(idxarr + ia * 2, 2, 0x382DF7) is None:
                return self._rax
            vbx2 = self._rd(vpool + wa * 8, 4, 0x382DFC)
            if vbx2 is None:
                return self._rax
            px = f32(u2f(ptx) - u2f(vbx2))
            unordered = math.isnan(acc)
            if self._rd(idxarr + ia * 2, 2, 0x382E17) is None:
                return self._rax
            pty = self._rd(pt + 4, 4, 0x382E1C)
            if pty is None:
                return self._rax
            vby2 = self._rd(vpool + wa * 8 + 4, 4, 0x382E22)
            if vby2 is None:
                return self._rax
            py = f32(u2f(pty) - u2f(vby2))
            cross = f32(f32(py * ex) - f32(px * ey))
            # jp/jne from the ucomiss(acc,0) taken BEFORE cross:
            if unordered or acc != 0.0:
                prod = f32(cross * acc)
                # comiss 0,prod; ja -> ret0. unordered -> pass
                if not math.isnan(prod) and 0.0 > prod:
                    return 0
            else:
                acc = cross
        return 1

    def ggrid(self, pt):
        """00383F10 — grid point query -> tri id / 0xFF."""
        root = self.mq(ROOTCELL)
        self._rax = root
        if self._rd(root + 0x20, 4, 0x383F23) is None:
            return self._rax
        gh = self.base(self.md(root + 0x20))
        self._rax = gh
        if self._rd(gh + 0xC, 4, 0x383F2E) is None:
            return self._rax
        bl = self.base(self.md(gh + 0xC))
        self._rax = bl
        x = self._rd(pt, 4, 0x383F36)
        if x is None:
            return self._rax
        if self.fdc(x) == 2:
            return 0xFF
        y = self._rd(pt + 4, 4, 0x383F4E)
        if y is None:
            return self._rax
        if self.fdc(y) == 2:
            return 0xFF
        xf, yf = u2f(x), u2f(y)
        ox = self.mw(gh + 4)
        if ox >= 0x8000:
            ox -= 0x10000
        # comiss (float)ox, x; ja -> 0xFF  (unordered: ja not taken)
        if not math.isnan(xf) and float(ox) > xf:
            return 0xFF
        oy = self.mw(gh + 6)
        if oy >= 0x8000:
            oy -= 0x10000
        if not math.isnan(yf) and float(oy) > yf:
            return 0xFF
        bx = ox + self.mb(gh + 2) * self.mb(gh)
        if not math.isnan(xf) and xf > float(bx):
            return 0xFF
        by = oy + self.mb(gh + 3) * self.mb(gh + 1)
        if not math.isnan(yf) and yf > float(by):
            return 0xFF
        cmap = self.base(self.md(gh + 8))
        row = _idiv(_cvtt(f32(yf - oy)), self.mb(gh + 1))
        col = _idiv(_cvtt(f32(xf - ox)), self.mb(gh))
        idx = row * self.mb(gh + 2) + col
        self._rax = idx & 0xFFFFFFFFFFFFFFFF   # cdqe leaves idx in rax
        cell = self._rd((cmap + idx * 2) & 0xFFFFFFFFFFFFFFFF, 2,
                        0x38402C)
        if cell is None:
            return self._rax
        if cell == 0xFFFF:
            return 0xFF
        li = bl + cell
        while True:
            b = self._rd(li, 1, 0x38404F)
            if b is None:
                return self._rax
            if b == 0xFF:
                return 0xFF
            rec = self.base(self.md(root + 0x18)) + b * 0x22
            n = self.mw(rec + 2)
            for s in range(n):
                sel = self.mw(rec + 0x14 + s * 2)
                iarr = self.base(self.md(root + 0x10)) + sel * 8
                if self.ttest(iarr, pt) == 1:
                    return b
            li += 1

    def wwrap(self, vec, pdst):
        """00384130 — builds contiguous {v.x, v.z} pair at pdst,
        calls GGRID on it."""
        x = self._rd(vec, 4, 0x384134)
        if x is None:
            return self._rax
        self.sd(pdst, x)
        z = self._rd(vec + 8, 4, 0x384138)
        if z is None:
            return self._rax
        self.sd(pdst + 4, z)
        return self.ggrid(pdst)

    def segt(self, p1, p2, va, vb, vsp):
        """00468880 — seg-seg orientation test; real VSUB/XPROD.
        Entry rsp = vsp; rbp = vsp-0x5F; frame rsp = vsp-0xD8;
        cookie residual = GSCOOK ^ (vsp-0xD8)."""
        resid = GSCOOK ^ ((vsp - 0xD8) & 0xFFFFFFFFFFFFFFFF)
        rbp = vsp - 0x5F
        A, B, C, D = rbp - 0x59, rbp - 0x19, rbp - 0x49, rbp - 0x29
        # local vec4s {x,0,z,1}; native read order: p1.x, p2.x,
        # p1.z, p2.z, va.z, va.x, vb.z, vb.x
        for src, off, site in (
                (p1, 0, 0x4688A4), (p2, 0, 0x4688AB),
                (p1, 8, 0x4688B4), (p2, 8, 0x4688C2),
                (va, 8, 0x4688D0), (va, 0, 0x4688DB),
                (vb, 8, 0x4688E9), (vb, 0, 0x4688F4)):
            v = self._rd(src + off, 4, site)
            if v is None:
                return resid
        self.sf(A, self.mf(p1))
        self.sf(A + 4, 0.0)
        self.sf(A + 8, self.mf(p1 + 8))
        self.sf(A + 0xC, 1.0)
        self.sf(B, self.mf(p2))
        self.sf(B + 4, 0.0)
        self.sf(B + 8, self.mf(p2 + 8))
        self.sf(B + 0xC, 1.0)
        self.sf(C, self.mf(va))
        self.sf(C + 4, 0.0)
        self.sf(C + 8, self.mf(va + 8))
        self.sf(C + 0xC, 1.0)
        self.sf(D, self.mf(vb))
        self.sf(D + 4, 0.0)
        self.sf(D + 8, self.mf(vb + 8))
        self.sf(D + 0xC, 1.0)

        def vsub4(dst, a, b):
            for o in (0, 4, 8, 0xC):
                self.sf(dst + o, f32(self.mf(a + o) - self.mf(b + o)))

        def xprod(dst, d, a):
            dx, dy, dz = self.mf(d), self.mf(d + 4), self.mf(d + 8)
            ax, ay, az = self.mf(a), self.mf(a + 4), self.mf(a + 8)
            self.sf(dst, f32(f32(dy * az) - f32(dz * ay)))
            self.sf(dst + 4, f32(f32(dz * ax) - f32(dx * az)))
            self.sf(dst + 8, f32(f32(dx * ay) - f32(dy * ax)))
            self.sf(dst + 0xC, 0.0)

        def le(a, b):
            """comiss a,b; jbe — unordered counts as taken."""
            return math.isnan(a) or math.isnan(b) or a <= b

        def gt(a, b):
            """comiss a,b; ja — unordered never taken."""
            return not (math.isnan(a) or math.isnan(b)) and a > b

        # stage 1: va/vb endpoints vs segment line (p1->p2)
        E, F, G, H, I = rbp - 0x39, rbp - 9, rbp + 7, \
            rbp + 0x27, rbp + 0x17
        vsub4(E, B, A)
        vsub4(F, C, A)
        vsub4(G, D, A)
        xprod(H, F, E)
        xprod(I, G, E)
        h1, i1 = self.mf(H + 4), self.mf(I + 4)
        if gt(h1, 0.0) and gt(i1, 0.0):
            return 0
        if gt(0.0, h1) and gt(0.0, i1):
            return 0
        # stage 2: p1/p2 endpoints vs edge line (va->vb)
        E2, F2, G2 = rbp - 0x39, rbp - 9, rbp + 7
        vsub4(E2, D, C)
        vsub4(F2, A, C)
        vsub4(G2, B, C)
        xprod(H, F2, E2)
        xprod(I, G2, E2)
        h2, i2 = self.mf(H + 4), self.mf(I + 4)
        if gt(h2, 0.0) and gt(i2, 0.0):
            return 0
        if gt(0.0, h2) and gt(0.0, i2):
            return 0
        return 1

    def qwalk(self, p1, p2, flag, vsp):
        """0033D3E0 — segment walk over the tri adjacency matrix.
        Frame: rsp = vsp - 0xB8 (4 pushes + sub 0x98)."""
        resid = GSCOOK ^ ((vsp - 0xB8) & 0xFFFFFFFFFFFFFFFF)
        L40 = vsp - 0xB8 + 0x40          # {x,z} pair local
        L50 = vsp - 0xB8 + 0x50          # edge vert vec A
        L60 = vsp - 0xB8 + 0x60          # edge vert vec B
        x = self._rd(p1, 4, 0x33D3FE)
        if x is None:
            return resid
        self.sd(L40, x)
        z = self._rd(p1 + 8, 4, 0x33D405)
        if z is None:
            return resid
        self.sd(L40 + 8, z)
        cur = self.wwrap(L40, vsp - 0xB8)
        if self.faults:
            return self._rax
        if cur == 0xFF:
            return 0
        x = self._rd(p2, 4, 0x33D442)
        if x is None:
            return cur          # rax still holds ggrid result
        self.sd(L40, x)
        z = self._rd(p2 + 8, 4, 0x33D44B)
        if z is None:
            return cur
        self.sd(L40 + 8, z)
        dst = self.wwrap(L40, vsp - 0xB8)
        if self.faults:
            return self._rax
        if dst == 0xFF:
            return 1
        root = self.mq(ROOTCELL)
        prev, budget = 0xFF, 0
        while True:
            if cur == dst:
                return 0
            deg = self.mw(root + 0xA)
            slot = 0
            while slot < deg:
                if slot == cur or slot == prev:
                    slot += 1
                    continue
                e = self.mw(self.base(self.md(root + 0x1C)) +
                            (deg * cur + slot) * 2)
                if e == 0:
                    slot += 1
                    continue
                ep = self.base(self.md(root + 0x14)) + e * 8
                c = self.eclass(self.mb(ep + 5), flag)
                ok = c == 1 or (c == 0 and
                                (self.mb(ep + 6) &
                                 (1 << (flag & 0x1F))) != 0)
                if ok:
                    vp = self.base(self.md(root + 0xC))
                    v0 = self.mw(ep)
                    v1 = self.mw(ep + 2)
                    self.sf(L50, self.mf(vp + v0 * 8))
                    self.sf(L50 + 4, 0.0)
                    self.sf(L50 + 8, self.mf(vp + v0 * 8 + 4))
                    self.sf(L50 + 0xC, 1.0)
                    self.sf(L60, self.mf(vp + v1 * 8))
                    self.sf(L60 + 4, 0.0)
                    self.sf(L60 + 8, self.mf(vp + v1 * 8 + 4))
                    self.sf(L60 + 0xC, 1.0)
                    if self.segt(p1, p2, L50, L60,
                                 vsp - 0xB8 - 8) != 0:
                        prev, cur = cur, slot
                        break
                slot += 1
            else:
                if slot == deg:
                    return 1
            budget += 1
            if budget >= 0x80:
                return 0

    # ---------- EXP-130 vec/predicate bodies (re-executed) ----
    # per-component read sites (rdx, r8) relative to function base —
    # identical layout for 00203080 and 00202B10
    _RD2 = {0: (0x04, 0x08), 4: (0x0D, 0x12),
            8: (0x1D, 0x22), 0xC: (0x2E, 0x33)}

    def _addsub(self, dst, a, b, base, sub):
        for off in (0, 4, 8, 0xC):
            da, db = self._RD2[off]
            for src, site in ((a, base + da), (b, base + db)):
                if not self.mapped(src + off):
                    self.faults.append(("memr", src + off, 4))
                    self.fault_end = site
                    return
        for off in (0, 4, 8, 0xC):
            v = self.mf(a + off) - self.mf(b + off) if sub else \
                self.mf(a + off) + self.mf(b + off)
            self.sf(dst + off, f32(v))

    def vsub(self, dst, a, b):
        """00203080 — dst = a - b, all 4 (reads a0,b0,a4,b4,...)."""
        self._addsub(dst, a, b, 0x203080, True)

    def vadd(self, dst, a, b):
        """00202B10 — dst = a + b, all 4."""
        self._addsub(dst, a, b, 0x202B10, False)

    def vscale(self, dst, a, s):
        """00202FE0 — dst[i] = a[i] * s (xmm2), all 4."""
        for off, site in ((0, 0x202FEA), (4, 0x202FEE),
                          (8, 0x202FFB), (0xC, 0x203000)):
            if not self.mapped(a + off):
                self.faults.append(("memr", a + off, 4))
                self.fault_end = site
                return
        for off in (0, 4, 8, 0xC):
            self.sf(dst + off, _m(s, self.mf(a + off)))

    def norm(self, v):
        """00216660 — normalize-or-zero in place (xyz; w untouched
        on the scale path, all 16B zeroed on the zero path).
        Returns the residual rax: _finite's 1 on the scale path,
        xor'd 0 on every zero path."""
        x, y, z = self.mf(v), self.mf(v + 4), self.mf(v + 8)
        len2 = f32(f32(f32(x * x) + f32(y * y)) + f32(z * z))
        if self.isnan_f64(len2):
            self.sq(v, 0)
            self.sq(v + 8, 0)
            return 0
        if not self.isfinite_f64(len2):
            self.sq(v, 0)
            self.sq(v + 8, 0)
            return 0
        eps = self.mf(FLTM)
        if len2 <= eps:
            self.sq(v, 0)
            self.sq(v + 8, 0)
            return 0
        ln = self.sqrtf(f2u(len2))
        s = f32div(self.mf(SEEDF), ln)
        self.sf(v, f32(x * s))
        self.sf(v + 4, f32(y * s))
        self.sf(v + 8, f32(z * s))
        return 1                      # _finite residual stays in rax

    def ncopy(self, dst, src):
        """00202DE0 — movups copy + NORM + d[dst+0xC]=0; rax is
        NORM's residual."""
        for off, site in ((0, 0x202DE6),):
            if not self.mapped(src + off) or \
               not self.mapped(src + off + 0xF):
                a = src + off if not self.mapped(src + off) \
                    else src + off + 0xF
                self.faults.append(("memr", a, 4))
                self.fault_end = site
                return 0
        for i in range(0x10):
            self.sb(dst + i, self.mb(src + i))
        r = self.norm(dst)
        self.sd(dst + 0xC, 0)
        return r

    def xprod(self, dst, d, a):
        """00202E10 — dst = d x a (w=0), stack temps (alias-safe)."""
        dx, dy, dz = self.mf(d), self.mf(d + 4), self.mf(d + 8)
        ax, ay, az = self.mf(a), self.mf(a + 4), self.mf(a + 8)
        rx = f32(dy * az) - f32(dz * ay)
        ry = f32(dz * ax) - f32(dx * az)
        rz = f32(dx * ay) - f32(dy * ax)
        rx, ry, rz = f32(rx), f32(ry), f32(rz)
        self.sf(dst, rx)
        self.sf(dst + 4, ry)
        self.sf(dst + 8, rz)
        self.sf(dst + 0xC, 0.0)

    def pred(self, p1, p2, scale, flag, vsp):
        """00335E50 — corridor-width probe; the three nav probes
        run the REAL QWALK tree (EXP-130's scripted boundary closed).
        Frame: rsp = vsp - 0x98; nested QWALK entry rsp = vsp - 0xA0."""
        resid = GSCOOK ^ ((vsp - 0x98) & 0xFFFFFFFFFFFFFFFF)
        STMP = vsp - 0x78                # rsp+0x20 flattened tmp
        SC30 = vsp - 0x68                # rsp+0x30 candidate A
        SC40 = vsp - 0x58                # rsp+0x40 candidate B
        SC50 = vsp - 0x48                # rsp+0x50 candidate C
        if not self.mapped(p1) or not self.mapped(p2):
            a = p1 if not self.mapped(p1) else p2
            self.faults.append(("memr", a, 4))
            self.fault_end = 0x203084
            return resid
        self.vsub(STMP, p1, p2)
        if self.faults:
            return resid
        self.sf(STMP + 4, 0.0)           # movss [rsp+0x24], xmm0
        self.ncopy(STMP, STMP)           # normalize-or-zero + w=0
        self.xprod(STMP, STMP, CONSTV)   # tmp x (0,1,0)
        self.vscale(STMP, STMP, scale)   # tmp *= xmm2
        # probe 1: (p1+off, p2+off)
        self.vadd(SC30, p1, STMP)
        self.vadd(SC50, p2, STMP)
        r = self.qwalk(SC30, SC50, flag, vsp - 0xA0)
        if self.faults:
            return r
        self._rax = r
        if r == 1:
            return 1
        # probe 2: (p1-off, p2-off)
        self.vsub(SC30, p1, STMP)
        self.vsub(SC40, p2, STMP)
        r = self.qwalk(SC30, SC40, flag, vsp - 0xA0)
        if self.faults:
            return r
        self._rax = r
        if r == 1:
            return 1
        # probe 3: (p2+off, p2-off)
        r = self.qwalk(SC50, SC40, flag, vsp - 0xA0)
        if self.faults:
            return r
        self._rax = r
        return 1 if r == 1 else 0

    # ---------- EXP-132 new bodies ----------
    def mload(self, dst):
        """00203170 — 4x movups copy of the shipped const 4x4 to
        [dst]. Sources 0x8C5F80/90/B0/D0 select {+X,+Y,+Z,W} from
        the shared signed axis-basis bank 0x8C5F80..0x8C5FE0
        (-Y at 0x8C5FA0 and -Z at 0x8C5FC0 are skipped)."""
        for i, cell in enumerate((0x8C5F80, 0x8C5F90,
                                  0x8C5FB0, 0x8C5FD0)):
            for k in range(16):
                self.sb(dst + i * 16 + k, self.mb(cell + k))

    def awrap(self, x):
        """0033CB70 — angle wrap to [-pi,pi]. |x|>4pi -> mod-2pi via
        divss/cvttss2si/cvtdq2ps/mulss/subss (NO [-pi,pi] wrap after);
        else subss -2pi / addss +2pi loops."""
        hi = self.mf(AWHI)               # +4pi
        lo = self.mf(AWLO)               # -4pi
        if (not math.isnan(x) and x > hi) or \
           (not math.isnan(x) and lo > x):
            per = self.mf(AW2PI)         # 2pi
            n = _cvtt(f32(x / per))
            self._rax = n & 0xFFFFFFFF   # cvttss2si eax (zero-extends)
            x = f32(x - f32(f32(n) * per))
            return x
        pi = self.mf(AWPI)               # +pi
        while not math.isnan(x) and x > pi:
            x = f32(x + self.mf(AWNEG2))  # addss -2pi
        npi = self.mf(AWNPI)             # -pi
        while not math.isnan(x) and npi > x:
            x = f32(x + self.mf(AW2PI))   # addss +2pi
        return x

    def rotcol(self, mat, s, c):
        """00217880 — per-column (x,z) -> (x*c + z*s, z*c - x*s)
        in place; columns at +0,+0x10,+0x20,+0x30."""
        self._rax = mat                 # mov rax,rcx at 0x217888
        for k in range(4):
            b = mat + k * 16
            x = self.mf(b)
            z = self.mf(b + 8)
            self.sf(b, f32(f32(z * s) + f32(x * c)))
            self.sf(b + 8, f32(f32(z * c) - f32(x * s)))

    def rbuild(self, dst, src, ang):
        """00202F00 — 4x movups [src]->[dst], cosf(ang)->xmm6,
        sinf(ang)->xmm1 via real IAT thunks, tail ROTCOL."""
        for i in range(4):
            for k in range(16):
                self.sb(dst + i * 16 + k, self.mb(src + i * 16 + k))
        co = self.cosf(f2u(ang))
        si = self.sinf(f2u(ang))
        self.rotcol(dst, si, co)
        self._rax = dst

    def mxv(self, dst, mat, v):
        """00217060 — dst = mat * v. v read order x,z,w,y
        (0x217064/06C/086/090); per component o: dst[o] =
        w*m[o+0x30] + ((y*m[o+0x10] + x*m[o]) + z*m[o+0x20]),
        each op f32-rounded in native add order."""
        vx = self._rd(v, 4, 0x217064)
        if vx is None:
            return
        self._rax = dst                 # mov rax,rcx at 0x217069
        vz = self._rd(v + 8, 4, 0x21706C)
        if vz is None:
            return
        vw = self._rd(v + 0xC, 4, 0x217086)
        if vw is None:
            return
        vy = self._rd(v + 4, 4, 0x217090)
        if vy is None:
            return
        x, y, z, w = u2f(vx), u2f(vy), u2f(vz), u2f(vw)
        for o in (0, 4, 8, 0xC):
            r = f32(f32(w * self.mf(mat + o + 0x30)) +
                    f32(f32(f32(y * self.mf(mat + o + 0x10)) +
                            f32(x * self.mf(mat + o))) +
                        f32(z * self.mf(mat + o + 0x20))))
            self.sf(dst + o, r)

    def mxvw(self, dst, mat, v, vsp):
        """00202B70 — MXV into a frame temp, movups copy to dst.
        Frame: rsp = vsp - 0x38; temp at rsp+0x20 = vsp - 0x18.
        rax = temp on exit (MXV's rcx residual survives the copy)."""
        t = vsp - 0x18
        self.mxv(t, mat, v)
        self._rax = t
        for i in range(0x10):
            self.sb(dst + i, self.mb(t + i))

    def pathw(self, a, b, vsp):
        """0033A3D0 — path-width probe. Frame rsp = vsp - 0x98:
        w@+0x20=vsp-0x78, v@+0x30=vsp-0x68, mat@+0x40=vsp-0x58;
        nested QWALK entry rsp = vsp - 0xA0."""
        resid = GSCOOK ^ ((vsp - 0x98) & 0xFFFFFFFFFFFFFFFF)
        W = vsp - 0x78
        V = vsp - 0x68
        MAT = vsp - 0x58
        r = self.qwalk(b, a, 1, vsp - 0xA0)
        if self.faults:
            return r
        self._rax = r
        if r != 1:
            return 1
        self.vsub(V, a, b)               # v = A - B
        if self.faults:
            return resid
        self.vscale(V, V, self.mf(PWSC))
        for ang in (PWANG1, PWANG2):
            self.mload(MAT)
            self.rbuild(MAT, MAT, self.awrap(self.mf(ang)))
            self.mxvw(W, MAT, V, vsp - 0xA0)
            if self.faults:
                return self._rax
            self.vadd(W, W, b)           # w += B
            r1 = self.qwalk(b, W, 1, vsp - 0xA0)
            if self.faults:
                return r1
            self._rax = r1
            ok = r1 == 1
            if not ok:
                r2 = self.qwalk(W, a, 1, vsp - 0xA0)
                if self.faults:
                    return r2
                self._rax = r2
                ok = r2 == 1
            if not ok:
                return 1
        return 0

    def blkchk(self, agent, vsp):
        """00335F90 — corridor-blocked check. Frame rsp = vsp-0x28;
        nested PRED/QWALK entry rsp = vsp - 0x30."""
        sub = self._rd(agent + 0x108, 8, 0x335F9F)
        if sub is None:
            return self._rax
        self._rax = sub
        rad = self._rd(sub + 0x10C, 4, 0x335FAD)
        if rad is None:
            return self._rax
        mode = self._rd(sub + 0x174, 1, 0x335FB5)
        if mode is None:
            return self._rax
        scale = f32(u2f(rad) * self.mf(BKSC))
        r = self.pred(agent, agent + 0x20, scale, mode, vsp - 0x30)
        if self.faults:
            return r
        self._rax = r
        if r != 0:
            return 1
        r = self.qwalk(agent, agent + 0x20, mode, vsp - 0x30)
        if self.faults:
            return r
        self._rax = r
        if r == 1:
            return 1
        sub = self._rd(agent + 0x108, 8, 0x335FE4)
        if sub is None:
            return self._rax
        self._rax = sub
        mode = self._rd(sub + 0x174, 1, 0x335FEB)
        if mode is None:
            return self._rax
        if mode == 3:
            r = self.agq(agent, agent + 0x20, 0, 0)
            if r != 0:
                return 1
            self._rax = r
        return 0

    # ---------- EXP-134 bodies ----------

    def rotx(self, mat, s, c):
        """00217790 — per-column (y,z) -> (y*c - z*s, y*s + z*c)
        in place; all four columns (+4/+8 per 16B column).
        rax = mat via mov rax,rcx at 0x217799."""
        self._rax = mat
        for k in range(4):
            b = mat + k * 16
            y = self.mf(b + 4)
            z = self.mf(b + 8)
            self.sf(b + 4, _s(_m(y, c), _m(z, s)))
            self.sf(b + 8, _a(_m(y, s), _m(z, c)))

    def mcpy(self, dst, src, ang):
        """00202E90 — 4x movups [src]->[dst] (interleaved read/write
        per row), cosf(ang)->xmm6, sinf(ang)->xmm1 via real IAT
        thunks, tail-jmp ROTX(dst, sin, cos). rax = dst."""
        for i, (rsite, wsite) in enumerate(
                ((0x202E96, 0x202EA1), (0x202EA4, 0x202EB0),
                 (0x202EB4, 0x202EB8), (0x202EBC, 0x202EC0))):
            # movups faults as two 8-byte accesses under emulation
            self._rd(src + i * 16, 8, rsite)
            if self.faults:
                return
            self._rd(src + i * 16 + 8, 8, rsite)
            if self.faults:
                return
            self._wr(dst + i * 16, 8, wsite)
            if self.faults:
                return
            self._wr(dst + i * 16 + 8, 8, wsite)
            if self.faults:
                return
            for k in range(16):
                self.sb(dst + i * 16 + k, self.mb(src + i * 16 + k))
        co = self.cosf(f2u(ang))
        si = self.sinf(f2u(ang))
        self.rotx(dst, si, co)
        self._rax = dst

    def de6a0(self, rcx, rdx, r8):
        """0032A6A0 — jmp 0026E100; the scripted dispatcher sees
        the caller's regs unchanged."""
        return self.de100(rcx, rdx, r8)

    def pathval(self, sub, angA, angB, tol, vsp):
        """00335B60 — path validator. rbp = vsp-0x18, rsp =
        vsp-0x118. Locals: v30@+0x30=vsp-0xE8, v40@+0x40=vsp-0xD8,
        v50@+0x50=vsp-0xC8, v60@+0x60=vsp-0xB8, mat@+0x70=vsp-0xA8.
        Stack args: cap @vsp+0x28 ([rbp+0x40]), flags @vsp+0x30
        ([rbp+0x48]). Nested call entry rsp = vsp-0x120."""
        V30 = vsp - 0xE8
        V40 = vsp - 0xD8
        V50 = vsp - 0xC8
        V60 = vsp - 0xB8
        MAT = vsp - 0xA8
        self._rax = GSCOOK ^ (vsp & 0xFFFFFFFFFFFFFFFF)
        if _ueq(tol, 0.0):                   # ucomiss xmm7,0: ret 0
            return 0
        cap = self._rd(vsp + 0x28, 4, 0x335BBC)
        if cap is None:
            return self._rax
        clamp = _maxss(self.mf(PVLO), _minss(self.mf(PVHI),
                                           u2f(cap)))
        if math.isnan(angB) or angB != 0.0:  # jp/je on angB==0
            cf = self.cosf(f2u(angB))
            tol = _d(tol, cf)
        self.mload(MAT)
        self.mcpy(MAT, MAT, u2f(f2u(angB) ^ 0x80000000))
        if self.faults:
            return self._rax
        self.mxvw(V30, MAT, CVEC, vsp - 0x120)
        if self.faults:
            return self._rax
        self.mload(MAT)
        self.rbuild(MAT, MAT, self.awrap(angA))
        self.mxvw(V30, MAT, V30, vsp - 0x120)
        if self.faults:
            return self._rax
        subp = self._rd(sub + 0x108, 8, 0x335C5A)
        if subp is None:
            return self._rax
        self._rax = subp
        rad = self._rd(subp + 0x110, 4, 0x335C6E)
        if rad is None:
            return self._rax
        self.vscale(V50, V30, _a(tol, u2f(rad)))
        if self.faults:
            return self._rax
        self.vadd(V50, V50, sub)
        if self.faults:
            return self._rax
        self.sd(V50 + 0xC, 0x3F800000)       # v50.w = 1.0f
        self.vscale(V40, V30, tol)
        if self.faults:
            return self._rax
        self.vadd(V40, V40, sub)
        if self.faults:
            return self._rax
        subp = self._rd(sub + 0x108, 8, 0x335CB9)
        if subp is None:
            return self._rax
        self._rax = subp
        self.sd(V40 + 0xC, 0x3F800000)       # v40.w = 1.0f
        rad = self._rd(subp + 0x110, 4, 0x335CD2)
        if rad is None:
            return self._rax
        s60 = _a(_s(u2f(rad), _m(u2f(rad), clamp)), tol)
        self.vscale(V60, V30, s60)
        if self.faults:
            return self._rax
        self.vadd(V60, V60, sub)
        if self.faults:
            return self._rax
        flags = self._rd(vsp + 0x30, 4, 0x335D01)
        if flags is None:
            return self._rax
        flags2 = self._rd(vsp + 0x30, 4, 0x335D09)
        if flags2 is None:
            return self._rax
        gf = (((flags & 4) | 0x10) << 2 | (flags2 & 2)) & 0xFFFFFFFF
        r9 = self._rd(sub + 0xF0, 8, 0x335D0F)
        if r9 is None:
            return self._rax
        g0 = self._rd(sub + 0xE0, 8, 0x335D24)
        if g0 is None:
            return self._rax
        self._rax = g0
        if not self._sd_flt(vsp - 0xF0, gf, 0x335D2B):
            return self._rax
        if not self._sq_flt(vsp - 0xF8, g0, 0x335D32):
            return self._rax
        gate = self.gate(sub, V60, sub, r9, s60, vsp - 0x120)
        self._rax = gate
        if self.faults:
            return self._rax
        if gate == 1:
            return 1
        subp = self._rd(sub + 0x108, 8, 0x335D43)
        if subp is None:
            return self._rax
        self._rax = subp
        mode = self._rd(subp + 0x174, 1, 0x335D4A)
        if mode is None:
            return self._rax
        if mode == 3:
            r = self.agq(sub, V50, 0, 0)
            if r != 0:
                return 1
            self._rax = r
        fl = self._rd(vsp + 0x30, 1, 0x335D6A)
        if fl is None:
            return self._rax
        subp = self._rd(sub + 0x108, 8, 0x335D73)
        if subp is None:
            return self._rax
        self._rax = subp
        if fl & 8:
            mode = self._rd(subp + 0x174, 1, 0x335D7F)
            if mode is None:
                return self._rax
            r = self.qwalk(sub, V40, mode, vsp - 0x120)
            if self.faults:
                return r
            self._rax = r
            if r == 1:
                return 1
        else:
            rad = self._rd(subp + 0x10C, 4, 0x335D98)
            if rad is None:
                return self._rax
            mode = self._rd(subp + 0x174, 1, 0x335DA8)
            if mode is None:
                return self._rax
            sc = _m(u2f(rad), self.mf(BKSC))
            r = self.pred(sub, V40, sc, mode, vsp - 0x120)
            if self.faults:
                return r
            self._rax = r
            if r != 0:
                return 1
        subp = self._rd(sub + 0x108, 8, 0x335DB9)
        if subp is None:
            return self._rax
        self._rax = subp
        rad = self._rd(subp + 0x110, 4, 0x335DC8)
        if rad is None:
            return self._rax
        lr = self.lquery(sub, V60, f2u(_m(clamp, u2f(rad))),
                         vsp - 0x120)
        if self.faults:
            return lr
        self._rax = lr
        if lr != 0:
            return 1
        subp = self._rd(sub + 0x108, 8, 0x335DDE)
        if subp is None:
            return self._rax
        self._rax = subp
        mode = self._rd(subp + 0x174, 1, 0x335DEF)
        if mode is None:
            return self._rax
        dr = self.de6a0(V50, mode, 1 if mode == 3 else 0)
        self._rax = dr
        if dr == 0:
            return 1
        return 2 if gate == 2 else 0

    # ---------- EXP-135 GATE tree ----------

    def gtab(self, ecx):
        """00236820 — pool table: ecx<0 || ecx>d[GTPCNT]-1 -> 0;
        else q[GTPOOL]+ecx*0xF50."""
        i = ecx & 0xFFFFFFFF
        if i >= 0x80000000:
            return 0                        # js 0x236842
        cnt = self._rd(GTPCNT, 4, 0x236824)
        if cnt is None:
            return self._rax
        c = cnt - 0x100000000 if cnt >= 0x80000000 else cnt
        if i > c - 1:
            return 0                        # jg 0x236842
        base = self._rd(GTPOOL, 8, 0x23683A)
        if base is None:
            return self._rax
        self._rax = (base + i * 0xF50) & 0xFFFFFFFFFFFFFFFF
        return self._rax

    def mabe(self, ecx):
        """0031ABE0 — b[MABEF]&0x10 -> tail MABESP else ret 0."""
        f = self._rd(MABEF, 1, 0x31ABE0)
        if f is None:
            return self._rax
        if f & 0x10:
            r = self.mabesp(ecx)
            self._rax = r                   # rax = MABESP ret
            return r
        return 0                            # xor eax,eax

    def gchk(self, rcx):
        """002EA7F0 — object validity chain -> 0/1."""
        if rcx == 0:
            return 0
        b = self._rd(rcx + 0x18, 1, 0x2EA804)
        if b is None:
            return self._rax
        if b == 1:
            return 0
        r1 = self._rd(rcx + 0xC0, 8, 0x2EA80A)
        if r1 is None:
            return self._rax
        self._rax = r1                      # rax = q[+0xC0]
        if r1 == 0:
            return 0
        f = self._rd(r1 + 0x14F, 1, 0x2EA816)
        if f is None:
            return self._rax
        if f & 1:
            return 0
        r2 = self._rd(r1 + 0x138, 8, 0x2EA81F)
        if r2 is None:
            return self._rax
        if r2 == 0:
            return 0
        v = self._rd(r2 + 0xF0, 4, 0x2EA82B)
        if v is None:
            return self._rax
        if not (u2f(v) > 0.0):              # comiss jbe / NaN -> 0
            return 0
        b8 = self._rd(rcx + 8, 1, 0x2EA83B)
        if b8 is None:
            return self._rax
        if not (b8 & 8):
            return 0
        r = self.ovf(rcx)
        self._rax = r                       # rax = OVF ret
        if r != 0:
            return 1
        b4 = self._rd(rcx + 4, 1, 0x2EA84D)
        if b4 is None:
            return self._rax
        return 1 if b4 == 3 else 0

    def ocls(self, rcx):
        """00263C20 — null-safe class byte b[+0xE]&0xF."""
        if rcx == 0:
            return 0
        b = self._rd(rcx + 0xE, 1, 0x263C25)
        if b is None:
            return self._rax
        self._rax = b & 0xF
        return self._rax

    def lhelp(self, rcx):
        """00335760 — accept helper: 0 bad; OCLS==3 -> 0;
        OCLS {1,2} -> 1; else 2."""
        if rcx == 0:
            return 0
        p = self._rd(rcx + 0x698, 8, 0x335769)
        if p is None:
            return self._rax
        self._rax = p                       # rax = q[+0x698]
        if p == 0:
            return 0
        b = self._rd(p + 5, 1, 0x335775)
        if b is None:
            return self._rax
        if b != 1:
            return 0
        sub = self._rd(rcx + 0x10, 8, 0x33577B)
        if sub is None:
            return self._rax
        cl = self.ocls(sub)
        if self.faults:
            return self._rax
        self._rax = cl                      # rax = OCLS ret
        if cl == 3:
            return 0
        return 1 if ((cl - 1) & 0xFFFFFFFF) <= 1 else 2

    def s3w(self, out, obj):
        """002FB500 — O3FW(out+0/4/8) + O2FW(out+0x10/0x14) +
        d[out+0x18] = O1F(obj); then d[out+4] = 0."""
        self.o3fw(obj, out, out + 4, out + 8)
        if self.faults:
            return self._rax
        self.o2fw(obj, out + 0x10, out + 0x14)
        if self.faults:
            return self._rax
        r = self.o1f(obj)
        if self.faults:
            return self._rax
        if not self._sf_flt(out + 0x18, u2f(r), 0x2FB545):
            return self._rax
        if not self._sd_flt(out + 4, 0, 0x2FB54A):
            return self._rax

    def s2w(self, out, obj, srsp):
        """002FB340 — O3FW(out+0/4/8) + O2FW(frame temps
        srsp+0x08/+0x18); d[out+4]=0; d[out+0x10]=maxss(f1,f2)
        (also ret float in xmm0)."""
        self.o3fw(obj, out, out + 4, out + 8)
        if self.faults:
            return self._rax
        self.o2fw(obj, srsp + 0x08, srsp + 0x18)
        if self.faults:
            return self._rax
        f1 = self._rd(srsp + 0x08, 4, 0x2FB37A)
        if f1 is None:
            return self._rax
        f2 = self._rd(srsp + 0x18, 4, 0x2FB380)
        if f2 is None:
            return self._rax
        m = _maxss(u2f(f1), u2f(f2))
        if not self._sd_flt(out + 4, 0, 0x2FB38B):
            return self._rax
        if not self._sf_flt(out + 0x10, m, 0x2FB392):
            return self._rax
        return m

    def cdst(self, tmp, query):
        """00469060 — (TRIGD(tmp,query)+d[q+0x10])^2 >=
        (q.x-t.x)^2+(q.z-t.z)^2 -> setae int."""
        t = self.trigd(tmp, query)
        if self.faults:
            return self._rax
        qx = self._rd(query, 4, 0x469075)
        if qx is None:
            return self._rax
        qz = self._rd(query + 8, 4, 0x46907B)
        if qz is None:
            return self._rax
        r = self._rd(query + 0x10, 4, 0x469085)
        if r is None:
            return self._rax
        tx = self._rd(tmp, 4, 0x46908A)
        if tx is None:
            return self._rax
        tz = self._rd(tmp + 8, 4, 0x469080)
        if tz is None:
            return self._rax
        dz = _s(u2f(qz), u2f(tz))
        rs = _a(t, u2f(r))
        dx = _s(u2f(qx), u2f(tx))
        lhs = _m(rs, rs)
        rhs = _a(_m(dz, dz), _m(dx, dx))
        # comiss xmm0(lhs), xmm1(rhs); setae -> lhs >= rhs ordered
        if math.isnan(lhs) or math.isnan(rhs):
            return 0
        return 1 if lhs >= rhs else 0

    def cdz0(self, query, tmp):
        """00468D10 — (d[q+0x10]+d[t+0x10])^2 >
        (q.x-t.x)^2+(q.z-t.z)^2 -> seta int."""
        qx = self._rd(query, 4, 0x468D10)
        if qx is None:
            return self._rax
        qz = self._rd(query + 8, 4, 0x468D16)
        if qz is None:
            return self._rax
        tz = self._rd(tmp + 8, 4, 0x468D1B)
        if tz is None:
            return self._rax
        tx = self._rd(tmp, 4, 0x468D20)
        if tx is None:
            return self._rax
        qr = self._rd(query + 0x10, 4, 0x468D24)
        if qr is None:
            return self._rax
        tr = self._rd(tmp + 0x10, 4, 0x468D29)
        if tr is None:
            return self._rax
        dz = _s(u2f(qz), u2f(tz))
        dx = _s(u2f(qx), u2f(tx))
        rs = _a(u2f(qr), u2f(tr))
        lhs = _m(rs, rs)
        rhs = _a(_m(dz, dz), _m(dx, dx))
        return 1 if _seta(lhs, rhs) else 0   # comiss seta: strict >

    def cf90(self, seg, tmp, vsp):
        """00468F90 — CPSEG closest on seg to tmp;
        (TRIGD(tmp,c)+d[seg+0x20]) > |tmp-c| -> seta.
        vsp = entry rsp; c20 = vsp-0x58 (push rdi+sub 0x70)."""
        c20 = vsp - 0x58
        cp = self.cpseg(c20, seg, tmp, seg + 0x10)
        if self.faults:
            return self._rax
        cx = self._rd(cp, 4, 0x468FE2)
        if cx is None:
            return self._rax
        cy = self._rd(cp + 4, 4, 0x468FED)
        if cy is None:
            return self._rax
        cz = self._rd(cp + 8, 4, 0x468FF6)
        if cz is None:
            return self._rax
        tx = self._rd(tmp, 4, 0x468FCA)
        if tx is None:
            return self._rax
        ty = self._rd(tmp + 4, 4, 0x468FD4)
        if ty is None:
            return self._rax
        tz = self._rd(tmp + 8, 4, 0x468FDD)
        if tz is None:
            return self._rax
        dx = _s(u2f(tx), u2f(cx))
        dy = _s(u2f(ty), u2f(cy))
        dz = _s(u2f(tz), u2f(cz))
        t = self.trigd(tmp, cp)
        if self.faults:
            return self._rax
        sr = self._rd(seg + 0x20, 4, 0x469010)
        if sr is None:
            return self._rax
        rs = _a(t, u2f(sr))
        d2 = _a(_a(_m(dx, dx), _m(dy, dy)), _m(dz, dz))
        d = self.sqrtf(f2u(d2))
        return 1 if _seta(rs, d) else 0      # comiss seta: strict >

    def gfilt(self, out, cnt, tmp, n, vsp):
        """003911D0 — handle filter: OBJD + flag checks;
        accepted -> out[w++]. ret accepted count.
        flags = d[vsp+0x28] stack arg (site 0x39120C)."""
        flags = self._rd(vsp + 0x28, 4, 0x39120C)
        if flags is None:
            return self._rax
        edi = 0
        w = 0
        n32 = n & 0xFFFFFFFF
        if n32 >= 0x80000000:
            n32 -= 0x100000000
        if n32 <= 0:
            return 0                        # jle -> eax = edi = 0
        cnt32 = cnt & 0xFFFFFFFF
        if cnt32 >= 0x80000000:
            cnt32 -= 0x100000000
        for i in range(n32):
            h = self._rd(tmp + i * 8, 8, 0x391221)
            if h is None:
                return self._rax
            obj = self.objd(h)
            self._rax = obj                 # rax = OBJD ret
            if (flags & 2) and obj == 0:
                continue                    # 0x391294 next
            if (flags & 4) and obj != 0:
                p = self._rd(obj + 0x698, 8, 0x391244)
                if p is None:
                    return self._rax
                if p == 0:
                    continue                # je 0x391294 -> skip
                a = self._rd(p + 0x64, 4, 0x391250)
                if a is None:
                    return self._rax
                b = self._rd(p + 0x3C, 4, 0x391253)
                if b is None:
                    return self._rax
                if (a | b) & 0x80000003:
                    r = self.of60(p)
                    self._rax = r
                    if r == 0:
                        continue            # OF60==0 -> skip
            if flags & 8:
                r = self.gchk(h)
                if self.faults:
                    return self._rax
                self._rax = r               # rax = GCHK ret
                if r == 0:
                    continue
            if out != 0:
                if w >= cnt32:
                    break                   # jge -> exit loop
                h2 = self._rd(tmp + i * 8, 8, 0x391287)
                if h2 is None:
                    return self._rax
                if not self._sq_flt(out + w * 8, h2, 0x39128B):
                    return self._rax
            edi += 1
            w += 1
        return edi

    def gpc(self, query, out, flag, vsp):
        """00391A30 — point+rad collector. vsp = entry rsp;
        frsp = vsp-0xC8; tmp30 = frsp+0x30; tmp50 = frsp+0x50."""
        resid = GSCOOK ^ ((vsp - 0xC8) & 0xFFFFFFFFFFFFFFFF)
        self._rax = resid
        frsp = vsp - 0xC8
        T30 = frsp + 0x30
        T50 = frsp + 0x50
        if not self._sd_flt(frsp + 0x20, flag, 0x391A55):
            return self._rax
        if not self._sq_flt(frsp + 0x28, query, 0x391A5D):
            return self._rax
        lsrc = self._rd(LLSRC, 8, 0x391A4A)
        if lsrc is None:
            return self._rax
        if lsrc == 0:
            return 0
        rl0 = self._rd(LRLEN, 4, 0x391A6B)
        if rl0 is None:
            return self._rax
        rl = rl0 - 0x100000000 if rl0 >= 0x80000000 else rl0
        dst = self._rd(LBMSK, 8, 0x391A74)
        if dst is None:
            return self._rax
        self._rax = dst
        self.mset(dst, 0, rl)
        rad = self._rd(query + 0x10, 4, 0x391AB0)
        if rad is None:
            return self._rax
        csz = self.mf(LCSZ)
        qx = self._rd(query, 4, 0x391ABD)
        if qx is None:
            return self._rax
        qz = self._rd(query + 8, 4, 0x391AC1)
        if qz is None:
            return self._rax
        w = self._rd(LGW, 4, 0x391AC9)
        if w is None:
            return self._rax
        w = w - 0x100000000 if w >= 0x80000000 else w
        epsx, epsz = self.mf(LEPSX), self.mf(LEPSZ)
        radf, qxf, qzf = u2f(rad), u2f(qx), u2f(qz)
        xlo = _cvtt(_d(_s(_s(qxf, radf), epsx), csz))
        zhi = _cvtt(_d(_s(_a(qzf, radf), epsz), csz))
        zlo = _cvtt(_d(_s(_s(qzf, radf), epsz), csz))
        xhi = _cvtt(_d(_s(_a(radf, qxf), epsx), csz))
        hq = self._rd(LGH, 8, 0x391B3E)
        if hq is None:
            return self._rax
        h = hq & 0xFFFFFFFF                 # lea eax,[rcx-1] low32
        h = h - 0x100000000 if h >= 0x80000000 else h

        def cl(v, m):                       # jns + cmovg -> [0, m-1]
            return 0 if v < 0 else (m - 1 if v > m - 1 else v)

        xlo, zlo = cl(xlo, w), cl(zlo, h)
        xhi, zhi = cl(xhi, w), cl(zhi, h)
        if zlo <= zhi:
            for row in range(zlo, zhi + 1):
                for col in range(xlo, xhi + 1):
                    idx = row * w + col
                    cmap = self._rd(LCFLG, 8, 0x391B90)
                    if cmap is None:
                        return self._rax
                    self._rax = cmap
                    fl = self._rd(
                        (cmap + idx) & 0xFFFFFFFFFFFFFFFF,
                        1, 0x391BA2)
                    if fl is None:
                        return self._rax
                    if fl == 0:
                        continue
                    src = (lsrc + idx * rl) & 0xFFFFFFFFFFFFFFFF
                    for k in range(rl):
                        self._rax = src + k
                        sv = self._rd(src + k, 1, 0x391BC0)
                        if sv is None:
                            return self._rax
                        d2 = self._rd(LBMSK, 8, 0x391BC9)
                        if d2 is None:
                            return self._rax
                        self._rax = d2
                        if not self._wr(d2 + k, 1, 0x391BD3):
                            return self._rax
                        self.sb(d2 + k, self.mb(d2 + k) | sv)
        # bit loop over d[GRCNT] records
        n = self._rd(GRCNT, 4, 0x391BFD)
        if n is None:
            return self._rax
        n = n - 0x100000000 if n >= 0x80000000 else n
        cnt = 0
        rsi = GHND
        bit, byte = 1, 0
        for i in range(n):
            bm = self._rd(LBMSK, 8, 0x391C30)
            if bm is None:
                return self._rax
            self._rax = bm
            fl = self._rd(bm + byte, 1, 0x391C37)
            if fl is None:
                return self._rax
            if fl & bit:
                h = self._rd(rsi, 8, 0x391C42)
                if h is None:
                    return self._rax
                if flag:
                    self.s3w(T30, h)
                    r = self.cdst(T30, query)
                else:
                    self.s2w(T50, h, frsp - 8)
                    r = self.cdz0(query, T50)
                if self.faults:
                    return self._rax
                self._rax = r               # rax = test ret
                if r != 0:
                    if out != 0:
                        self._rax = h       # mov rax,[rsi]
                        if not self._sq_flt(out, h, 0x391C87):
                            return self._rax
                    cnt += 1
                    out += 8
            bit = (bit << 1) & 0xFF
            if bit == 0:
                bit = 1
                byte += 1
            rsi += 8
        self._rax = cnt
        return cnt

    def gsc(self, query, out, flag, vsp):
        """00391D90 — segment collector. vsp = entry rsp;
        rbp = vsp-0x38; frsp = vsp-0x138; SEG = frsp+0x30;
        T80 = vsp-0xB8; T60 = frsp+0x60."""
        resid = GSCOOK ^ ((vsp - 0x138) & 0xFFFFFFFFFFFFFFFF)
        self._rax = resid
        frsp = vsp - 0x138
        SEG = frsp + 0x30
        T80 = vsp - 0xB8
        T60 = frsp + 0x60
        if not self._sd_flt(frsp + 0x20, flag, 0x391DB9):
            return self._rax
        if not self._sq_flt(frsp + 0x28, out, 0x391DC1):
            return self._rax
        lsrc = self._rd(LLSRC, 8, 0x391DAE)
        if lsrc is None:
            return self._rax
        if lsrc == 0:
            return 0
        rl0 = self._rd(LRLEN, 4, 0x391DCF)
        if rl0 is None:
            return self._rax
        rl = rl0 - 0x100000000 if rl0 >= 0x80000000 else rl0
        dst = self._rd(LBMSK, 8, 0x391DD8)
        if dst is None:
            return self._rax
        self._rax = dst
        self.mset(dst, 0, rl)
        radv = self._rd16(query + 0x20, 0x391E06)
        if radv is None:
            return self._rax
        rad = u2f(radv[0] & 0xFFFFFFFF)
        csz = self.mf(LCSZ)
        p1v = self._rd16(query, 0x391E17)
        if p1v is None:
            return self._rax
        p2v = self._rd16(query + 0x10, 0x391E1A)
        if p2v is None:
            return self._rax
        # seg local copy + w-lane zeroing
        if not self._wr16(SEG, p1v, 0x391E1E):
            return self._rax
        if not self._wr16(SEG + 0x10, p2v, 0x391E32):
            return self._rax
        if not self._wr16(SEG + 0x20, radv, 0x391E43):
            return self._rax
        if not self._sd_flt(SEG + 4 + 0x10, 0, 0x391E49):
            return self._rax
        if not self._sd_flt(SEG + 4, 0, 0x391E51):
            return self._rax
        p1x = self._rd(SEG, 4, 0x391E29)
        if p1x is None:
            return self._rax
        p1z = self._rd(SEG + 8, 4, 0x391E23)
        if p1z is None:
            return self._rax
        p2x = self._rd(SEG + 0x10, 4, 0x391E83)
        if p2x is None:
            return self._rax
        p2z = self._rd(SEG + 0x18, 4, 0x391E37)
        if p2z is None:
            return self._rax
        epsx, epsz = self.mf(LEPSX), self.mf(LEPSZ)
        p1xf, p1zf = u2f(p1x), u2f(p1z)
        p2xf, p2zf = u2f(p2x), u2f(p2z)
        maxz, minz = _maxss(p1zf, p2zf), _minss(p1zf, p2zf)
        maxx, minx = _maxss(p1xf, p2xf), _minss(p1xf, p2xf)
        zhi = _cvtt(_d(_s(_a(maxz, rad), epsz), csz))
        zlo = _cvtt(_d(_s(_s(minz, rad), epsz), csz))
        xhi = _cvtt(_d(_s(_a(maxx, rad), epsx), csz))
        xlo = _cvtt(_d(_s(_s(minx, rad), epsx), csz))
        self.bmask(xlo, zlo, xhi, zhi)
        if self.faults:
            return self._rax
        ln = self.dist(SEG, SEG + 0x10)
        if self.faults:
            return self._rax
        if _ueq(ln, 0.0):
            return 0                        # ordered-equal -> ret 0
        dzu = _d(_s(p2zf, p1zf), ln)
        dxu = _d(_s(p2xf, p1xf), ln)
        n = self._rd(GRCNT, 4, 0x391F1E)
        if n is None:
            return self._rax
        n = n - 0x100000000 if n >= 0x80000000 else n
        cnt = 0
        rsi = GHND
        bit, byte = 1, 0
        for i in range(n):
            bm = self._rd(LBMSK, 8, 0x391F70)
            if bm is None:
                return self._rax
            self._rax = bm
            fl = self._rd(bm + byte, 1, 0x391F77)
            if fl is None:
                return self._rax
            if fl & bit:
                h = self._rd(rsi, 8, 0x391F86)
                if h is None:
                    return self._rax
                if flag:
                    self.s3w(T80, h)
                    if self.faults:
                        return self._rax
                    r = self.cf90(SEG, T80, frsp - 8)
                    self._rax = r           # rax = CF90 ret
                    acc = r != 0
                else:
                    self.s2w(T60, h, frsp - 8)
                    if self.faults:
                        return self._rax
                    dx = _s(u2f(self.md(T60)), u2f(self.md(SEG)))
                    dz = _s(u2f(self.md(T60 + 8)),
                            u2f(self.md(SEG + 8)))
                    dot = _a(_m(dz, dzu), _m(dx, dxu))
                    cross = _s(_m(dx, dzu), _m(dz, dxu))
                    acc = False
                    if not math.isnan(dot) and dot > 0.0 and \
                            not math.isnan(ln) and ln > dot:
                        rs = _a(u2f(self.md(T60 + 0x10)),
                                u2f(self.md(SEG + 0x20)))
                        if not math.isnan(cross) and \
                                not math.isnan(rs) and \
                                cross > -rs and rs > cross:
                            acc = True
                    if not acc:
                        d2 = self.dist(T60, SEG + 0x10)
                        if self.faults:
                            return self._rax
                        rs = _a(u2f(self.md(T60 + 0x10)),
                                u2f(self.md(SEG + 0x20)))
                        if not math.isnan(rs) and \
                                not math.isnan(d2) and rs > d2:
                            acc = True
                if self.faults:
                    return self._rax
                if acc:
                    if out != 0:
                        self._rax = h       # mov rax,[rsi]
                        if not self._sq_flt(out, h, 0x392043):
                            return self._rax
                    cnt += 1
                    out += 8
            bit = (bit << 1) & 0xFF
            if bit == 0:
                bit = 1
                byte += 1
            rsi += 8
        self._rax = cnt
        return cnt

    def gpt(self, query, out, cnt, flags, vsp):
        """00391D10 — point-query wrapper: GPC(tmp) -> GFILT.
        vsp = entry rsp; frame = vsp-0x848; tmp = frame+0x30."""
        resid = GSCOOK ^ ((vsp - 0x848) & 0xFFFFFFFFFFFFFFFF)
        self._rax = resid
        tmp = vsp - 0x848 + 0x30
        n = self.gpc(query, tmp, flags & 0x10, vsp - 0x850)
        if self.faults:
            return self._rax
        self._rax = n                       # mov r9d,eax
        if not self._sd_flt(vsp - 0x848 + 0x20, flags, 0x391D51):
            return self._rax
        r = self.gfilt(out, cnt, tmp, n, vsp - 0x850)
        if self.faults:
            return self._rax
        return r

    def gseg(self, query, out, cnt, flags, vsp):
        """003920F0 — segment-query wrapper: GSC(tmp) -> GFILT.
        frame = vsp-0x848; tmp = frame+0x30."""
        resid = GSCOOK ^ ((vsp - 0x848) & 0xFFFFFFFFFFFFFFFF)
        self._rax = resid
        tmp = vsp - 0x848 + 0x30
        n = self.gsc(query, tmp, flags & 0x10, vsp - 0x850)
        if self.faults:
            return self._rax
        self._rax = n                       # mov r9d,eax
        if not self._sd_flt(vsp - 0x848 + 0x20, flags, 0x392131):
            return self._rax
        r = self.gfilt(out, cnt, tmp, n, vsp - 0x850)
        if self.faults:
            return self._rax
        return r

    def gate(self, rcx, rdx, r8, r9, xmm2, vsp):
        """003357B0 — corridor gate. vsp = entry rsp;
        rbp = vsp-0x148; frsp = vsp-0x248; out = rbp-0x20."""
        resid = GSCOOK ^ ((vsp - 0x248) & 0xFFFFFFFFFFFFFFFF)
        self._rax = resid
        rbp = vsp - 0x148
        frsp = vsp - 0x248
        OUT = rbp - 0x20
        SELF = frsp + 0x20
        if not self._wr(rbp + 0xE0, 8, 0x3357D9):
            return self._rax
        self.sq(rbp + 0xE0, resid)
        idx = self._rd(r9 + 0xEA9, 1, 0x3357E8)
        if idx is None:
            return self._rax
        if not self._wr(frsp + 0x58, 8, 0x3357E3):
            return self._rax
        self.sq(frsp + 0x58, rcx)           # saved posA
        pobj = self.gtab(idx)
        if self.faults:
            return self._rax
        self._rax = pobj                    # rax = GTAB result
        d8 = self._rd(pobj + 8, 4, 0x3357FE)
        if d8 is None:
            return self._rax
        s = self.mabe(d8)
        if self.faults:
            return self._rax
        self._rax = s                       # rax = MABE ret
        flags = self._rd(rbp + 0x178, 4, 0x335806)
        if flags is None:
            return self._rax
        if not self._sq_flt(SELF, s, 0x33580D):
            return self._rax
        if not (flags & 0x20):
            r = self.gchk(s)
            if self.faults:
                return self._rax
            if r == 0:
                return 0                    # -> epilogue ret 0
        # posA vs posB ordered compare on x,y,z
        ax = self._rd(rcx, 4, 0x335828)
        if ax is None:
            return self._rax
        r9f = ((~(flags >> 4)) & 8 | 0x14) & 0xFFFFFFFF
        bx = self._rd(rdx, 4, 0x335856)
        if bx is None:
            return self._rax
        eq = _ueq(u2f(ax), u2f(bx))
        if eq:
            ay = self._rd(rcx + 4, 4, 0x33585D)
            if ay is None:
                return self._rax
            by = self._rd(rdx + 4, 4, 0x335862)
            if by is None:
                return self._rax
            eq = _ueq(u2f(ay), u2f(by))
            if eq:
                az = self._rd(rcx + 8, 4, 0x33586A)
                if az is None:
                    return self._rax
                bz = self._rd(rdx + 8, 4, 0x33586F)
                if bz is None:
                    return self._rax
                eq = _ueq(u2f(az), u2f(bz))
        if eq:
            PQ = rbp - 0x80
            v = self._rd16(rcx, 0x335877)
            if v is None:
                return self._rax
            if not self._wr16(PQ, v, 0x335884):
                return self._rax
            if not self._sf_flt(rbp - 0x70, xmm2, 0x33588D):
                return self._rax
            n = self.gpt(PQ, OUT, 0x20, r9f, frsp - 8)
        else:
            SQ = rbp - 0x60
            v = self._rd16(rcx, 0x335899)
            if v is None:
                return self._rax
            if not self._wr16(SQ, v, 0x3358AD):
                return self._rax
            v = self._rd16(rdx, 0x3358A0)
            if v is None:
                return self._rax
            if not self._wr16(SQ + 0x10, v, 0x3358B2):
                return self._rax
            if not self._sf_flt(rbp - 0x40, xmm2, 0x3358B7):
                return self._rax
            n = self.gseg(SQ, OUT, 0x20, r9f, frsp - 8)
        if self.faults:
            return self._rax
        self._rax = n                       # cdqe rax = count
        if n <= 0:
            return 0                        # jle -> eax 0
        esi = 0
        r12d = 0
        for i in range(n):
            h = self._rd(OUT + i * 8, 8, 0x3358E0)
            if h is None:
                return self._rax
            obj = self.objd(h)
            self._rax = obj                 # rax = OBJD ret
            slf = self._rd(SELF, 8, 0x3358EA)
            if slf is None:
                return self._rax
            h2 = self._rd(OUT + i * 8, 8, 0x3358F2)
            if h2 is None:
                return self._rax
            self._rax = h2                  # rax = raw handle
            if slf == h2:
                continue                    # handle==self -> skip
            e = self._rd(rbp + 0x170, 8, 0x335900)
            if e is None:
                return self._rax
            if e != 0 and e == h2:
                continue                    # handle==arg5 -> skip
            accept = obj == 0
            if not accept:
                p68 = self._rd(obj + 0xE68, 8, 0x33591E)
                if p68 is None:
                    return self._rax
                self._rax = p68
                if p68 != 0:
                    b = self._rd(p68 + 0x18, 1, 0x33592A)
                    if b is None:
                        return self._rax
                    self._rax = (b >> 1) & 7   # movzx+shr+and
                    if ((b >> 1) & 7) == 1:
                        p68c = self._rd(r9 + 0xE68, 8, 0x335938)
                        if p68c is None:
                            return self._rax
                        self._rax = p68c
                        if p68c != 0:
                            b2 = self._rd(p68c + 0x18, 1, 0x335944)
                            if b2 is None:
                                return self._rax
                            self._rax = (b2 >> 1) & 7
                            if ((b2 >> 1) & 7) == 4:
                                continue    # e68 pair -> skip
                # flag&0x40 block: ctx!=3 && obj==3
                if flags & 0x40:
                    bc = self._rd(r9 + 0x1F4, 1, 0x335960)
                    if bc is None:
                        return self._rax
                    if bc != 3:
                        bo = self._rd(obj + 0x1F4, 1, 0x33596E)
                        if bo is None:
                            return self._rax
                        if bo == 3:
                            F30 = frsp + 0x30
                            sb = self._rd(obj + 0x10, 8, 0x335977)
                            if sb is None:
                                return self._rax
                            if not self._wr16(
                                    F30, (0, 0), 0x335982):
                                return self._rax
                            if sb != 0:
                                self.o3fw(sb, F30, F30 + 4, F30 + 8)
                            V30 = rbp - 0x30
                            f30 = self._rd(F30, 4, 0x3359A0)
                            if f30 is None:
                                return self._rax
                            f38 = self._rd(F30 + 8, 4, 0x3359AA)
                            if f38 is None:
                                return self._rax
                            if not self._sd_flt(V30, f30, 0x3359B0):
                                return self._rax
                            if not self._sd_flt(
                                    V30 + 8, f38, 0x3359B5):
                                return self._rax
                            if not self._sd_flt(
                                    V30 + 0xC, 0x3F800000,
                                    0x3359BA):
                                return self._rax
                            if not self._sd_flt(
                                    V30 + 4, 0x3F800000,
                                    0x3359C1):
                                return self._rax
                            self._rax = self.osub(V30)
                            c10 = self._rd(r9 + 0x10, 8, 0x3359CD)
                            if c10 is None:
                                return self._rax
                            x0 = 0.0 if c10 == 0 else u2f(
                                self.o1f2(c10))
                            f34 = self._rd(F30 + 4, 4, 0x3359E0)
                            if f34 is None:
                                return self._rax
                            c1 = self._rd(rbp - 0x2C, 4, 0x3359E6)
                            if c1 is None:
                                return self._rax
                            if _seta(_s(u2f(f34), u2f(c1)), x0):
                                continue    # ja -> skip
            if not accept:
                if flags & 2:
                    l = self.lhelp(obj)
                    if self.faults:
                        return self._rax
                    self._rax = l
                    if l == 0:
                        esi += 1
                        continue            # early-out esi++
                if flags & 4:
                    l = self.lhelp(r9)
                    if self.faults:
                        return self._rax
                    self._rax = l
                    if l == 0:
                        l = self.lhelp(obj)
                        if self.faults:
                            return self._rax
                        self._rax = l
                        if l == 0:
                            esi += 1
                            continue
                if flags & 0x10:
                    l = self.lhelp(obj)
                    if self.faults:
                        return self._rax
                    self._rax = l
                    if l == 0:
                        sb = self._rd(obj + 0x10, 8, 0x335A32)
                        if sb is None:
                            return self._rax
                        x = self.o1f3(sb)
                        if _ueq(u2f(x), 0.0):
                            esi += 1
                        continue            # LHELP==0 arm -> next iter
                if flags & 8:
                    lc = self.lhelp(r9)
                    if self.faults:
                        return self._rax
                    self._rax = lc
                    lo = self.lhelp(obj)
                    if self.faults:
                        return self._rax
                    self._rax = lo
                    if lc != lo:
                        continue
                    self._rax = 0x4021      # mov eax,0x4021
                    w14 = self._rd(obj + 0x714, 2, 0x335A86)
                    if w14 is None:
                        return self._rax
                    if w14 != 0x4021:
                        continue
                    slf = self._rd(SELF, 8, 0x335A8F)
                    if slf is None:
                        return self._rax
            # accept path
            if flags & 0x40:
                bc = self._rd(r9 + 0x1F4, 1, 0x335A9A)
                if bc is None:
                    return self._rax
                if bc == 3:
                    F70 = frsp + 0x70
                    self.o3fw(h2, F70, F70 + 4, F70 + 8)
                    x = self.o1f2(h2)
                    p = self._rd(frsp + 0x58, 8, 0x335AC7)
                    if p is None:
                        return self._rax
                    self._rax = p             # rax = saved posA
                    y = self._rd(p + 4, 4, 0x335AD2)
                    if y is None:
                        return self._rax
                    f74 = self._rd(F70 + 4, 4, 0x335ACC)
                    if f74 is None:
                        return self._rax
                    if _seta(u2f(y), _a(u2f(x), u2f(f74))):
                        continue            # ja -> skip
            r = self.opa(slf, h2)
            self._rax = r
            if r == 0:
                continue
            r = self.opb(slf, h2, frsp + 0x50, frsp - 8)
            self._rax = r
            if (r - 1) & 0xFFFFFFFF <= 2:
                esi += 1
            else:
                r12d += 1
        return 1 if r12d != 0 else (2 if esi != 0 else 0)

    # ---------- EXP-133 LOS tree ----------

    def bmask(self, c0, r0, c1, r1):
        """003912E0 — memset + clamp + OR per-cell record masks.
        args ecx=c0 edx=r0 r8d=c1 r9d=r1 (all sx32)."""
        dst = self.mq(LBMSK)
        rlen = self.md(LRLEN)
        rl = rlen - 0x100000000 if rlen >= 0x80000000 else rlen
        self.mset(dst, 0, rl)              # movsxd r8 count
        w = self.md(LGW)
        if w >= 0x80000000:
            w -= 0x100000000
        h = self.mq(LGH) & 0xFFFFFFFF      # lea eax,[rcx-1] low32
        if h >= 0x80000000:
            h -= 0x100000000

        def sx(v):
            v &= 0xFFFFFFFF
            return v - 0x100000000 if v >= 0x80000000 else v

        def clamp(v, m):                   # jns: <0 -> 0; >m-1 -> m-1
            v = sx(v)
            return 0 if v < 0 else (m - 1 if v > m - 1 else v)

        c0 = clamp(c0, w)
        r0 = clamp(r0, h)
        c1 = clamp(c1, w)
        r1 = clamp(r1, h)
        if r0 <= r1:
            cmap = self.mq(LCFLG)
            lsrc = self.mq(LLSRC)
            for row in range(r0, r1 + 1):
                for col in range(c0, c1 + 1):
                    idx = sx(row * w + col)
                    self._rax = cmap            # rax = q[LCFLG]
                    fl = self._rd((cmap + idx) & 0xFFFFFFFFFFFFFFFF,
                                  1, 0x391394)
                    if fl is None:
                        return self._rax
                    if fl == 0:
                        continue
                    src = (lsrc + sx(idx * rlen)) & 0xFFFFFFFFFFFFFFFF
                    for k in range(rlen):
                        self._rax = k           # byte-index counter
                        sv = self._rd(src + k, 1, 0x3913BB)
                        if sv is None:
                            return self._rax
                        self._rax = k + 1       # lea rax,[rax+1]
                        dv = self._rd(dst + k, 1, 0x3913C4)
                        if dv is None:
                            return self._rax
                        self.sb(dst + k, dv | sv)
        return dst

    def dist(self, a, b):
        """003A1920 — sqrt(|a-b|^2) -> THUNKF; result in xmm0."""
        x0 = self._rd(a, 4, 0x3A1920)
        if x0 is None:
            return self._rax
        y0 = self._rd(a + 4, 4, 0x3A1924)
        if y0 is None:
            return self._rax
        y1 = self._rd(b + 4, 4, 0x3A1929)
        if y1 is None:
            return self._rax
        x1 = self._rd(b, 4, 0x3A192E)
        if x1 is None:
            return self._rax
        z0 = self._rd(a + 8, 4, 0x3A1932)
        if z0 is None:
            return self._rax
        z1 = self._rd(b + 8, 4, 0x3A1937)
        if z1 is None:
            return self._rax
        dx = _s(u2f(x0), u2f(x1))
        dy = _s(u2f(y0), u2f(y1))
        dz = _s(u2f(z0), u2f(z1))
        d2 = _a(_a(_m(dy, dy), _m(dx, dx)), _m(dz, dz))
        return self.sqrtf(f2u(d2))

    def cpseg(self, out, a, p, b):
        """004691A0 — closest point on seg [a,b] to p.
        t = dot(a-p, a-b)/|a-b|^2; t<0 -> a, t>1 -> b,
        else a + t*(b-a). 16B out, rax = out."""
        bx = self._rd(b, 4, 0x4691A4)
        if bx is None:
            return self._rax
        by = self._rd(b + 4, 4, 0x4691AE)
        if by is None:
            return self._rax
        bz = self._rd(b + 8, 4, 0x4691B9)
        if bz is None:
            return self._rax
        ay = self._rd(a + 4, 4, 0x4691CB)
        if ay is None:
            return self._rax
        ax = self._rd(a, 4, 0x4691DB)
        if ax is None:
            return self._rax
        px = self._rd(p, 4, 0x4691EE)
        if px is None:
            return self._rax
        az = self._rd(a + 8, 4, 0x4691F3)
        if az is None:
            return self._rax
        py = self._rd(p + 4, 4, 0x469205)
        if py is None:
            return self._rax
        pz = self._rd(p + 8, 4, 0x469213)
        if pz is None:
            return self._rax
        ax, ay, az = u2f(ax), u2f(ay), u2f(az)
        bx, by, bz = u2f(bx), u2f(by), u2f(bz)
        px, py, pz = u2f(px), u2f(py), u2f(pz)
        apx, apy, apz = _s(ax, px), _s(ay, py), _s(az, pz)
        abx, aby, abz = _s(ax, bx), _s(ay, by), _s(az, bz)
        dot = _a(_a(_m(apy, aby), _m(apx, abx)), _m(apz, abz))
        l2 = _a(_a(_m(abx, abx), _m(aby, aby)), _m(abz, abz))
        t = _d(dot, l2)
        if not math.isnan(t) and 0.0 > t:
            # movaps xmm0,[rdx] — full 16B endpoint vec
            res = (ax, ay, az, self.mf(a + 0xC))
        elif not math.isnan(t) and t > 1.0:
            res = (bx, by, bz, self.mf(b + 0xC))
        else:
            # t<=1 or unordered (jbe on comiss t,1.0f): mid-lerp
            res = (_a(_m(_s(bx, ax), t), ax),
                   _a(_m(_s(by, ay), t), ay),
                   _a(_m(_s(bz, az), t), az), 0)
        self._rax = out                    # mov rax,rcx
        if not self.mapped(out) or not self.mapped(out + 8):
            # movaps [rcx] — single 16B store (fault size 8)
            a0 = out if not self.mapped(out) else out + 8
            self.faults.append(("memw", a0, 8))
            self.fault_end = 0x4692D2
            return self._rax
        for k, v in enumerate(res):
            self.sf(out + k * 4, v)
        return out

    def trigd(self, edge, cpt):
        """00468580 — trig-table edge helper -> xmm0 float."""
        an = self._rd(edge + 0x18, 4, 0x468584)
        if an is None:
            return self._rax
        frac = _d(u2f(an), self.mf(NEG2PI))
        cx = self._rd(cpt, 4, 0x468598)
        if cx is None:
            return self._rax
        cz = self._rd(cpt + 8, 4, 0x46859C)
        if cz is None:
            return self._rax
        f0 = _m(frac, self.mf(TRIGN))
        f1 = _m(frac, self.mf(TRIGP))
        ex = self._rd(edge, 4, 0x4685B9)
        if ex is None:
            return self._rax
        ez = self._rd(edge + 8, 4, 0x4685BD)
        if ez is None:
            return self._rax
        dx = _s(u2f(cx), u2f(ex))
        dz = _s(u2f(cz), u2f(ez))
        i1 = (0x2000 - _cvtt(f0)) & 0x7FFF
        e10 = self._rd(edge + 0x10, 4, 0x4685CB)
        if e10 is None:
            return self._rax
        i2 = _cvtt(f1) & 0x7FFF
        self._rax = i2            # last eax write = cvttss2si+and
        t1 = self.mf(TRIGT + i1 * 4)
        t2 = self.mf(TRIGT + i2 * 4)
        e14 = self._rd(edge + 0x14, 4, 0x46860F)
        if e14 is None:
            return self._rax
        e10, e14 = u2f(e10), u2f(e14)
        x8 = _d(_a(_m(t2, dz), _m(t1, dx)), e10)
        x7 = _d(_s(_m(t1, dz), _m(t2, dx)), e14)
        d2 = _a(_a(_m(x8, x8), 0.0), _m(x7, x7))
        d = self.sqrtf(f2u(d2))
        eps = struct.unpack(
            "<d", img_rd(self.raw, self.secs, DISTEPS, 8))[0]
        if math.isnan(d) or d <= eps:
            return e10            # comisd jbe: <= OR unordered
        inv = _d(self.mf(CLAMP1), d)
        t8 = _m(_m(inv, x8), e10)
        t7 = _m(_m(inv, x7), e14)
        r2 = _a(_a(_m(t8, t8), 0.0), _m(t7, t7))
        return self.sqrtf(f2u(r2))

    def capt0(self, seg, edge, cbuf):
        """00468D50 — capsule A: point-seg shortcut or CPSEG;
        closest==p1 -> 0; radsum > dist -> 1."""
        p1x = self._rd(seg, 4, 0x468D6B)
        if p1x is None:
            return self._rax
        p2x = self._rd(seg + 0x10, 4, 0x468D72)
        if p2x is None:
            return self._rax
        p1z = self._rd(seg + 8, 4, 0x468D7A)
        if p1z is None:
            return self._rax
        p2z = self._rd(seg + 0x18, 4, 0x468D7F)
        if p2z is None:
            return self._rax
        p1x, p1z = u2f(p1x), u2f(p1z)
        p2x, p2z = u2f(p2x), u2f(p2z)
        if _ueq(p1x, p2x) and _ueq(p1z, p2z):
            ex = self._rd(edge, 4, 0x468D87)
            if ex is None:
                return self._rax
            ez = self._rd(edge + 8, 4, 0x468D8B)
            if ez is None:
                return self._rax
            p1y = self._rd(seg + 4, 4, 0x468D90)
            if p1y is None:
                return self._rax
            ey = self._rd(edge + 4, 4, 0x468D95)
            if ey is None:
                return self._rax
            sr = self._rd(seg + 0x20, 4, 0x468D9A)
            if sr is None:
                return self._rax
            er = self._rd(edge + 0x10, 4, 0x468D9F)
            if er is None:
                return self._rax
            dx = _s(p1x, u2f(ex))
            dz = _s(p1z, u2f(ez))
            dy = _s(u2f(p1y), u2f(ey))
            rad = _a(u2f(sr), u2f(er))
            d2 = _a(_a(_m(dx, dx), _m(dy, dy)), _m(dz, dz))
            return 1 if _seta(rad, self.sqrtf(f2u(d2))) else 0
        self.cpseg(cbuf, seg, edge, seg + 0x10)
        if self.fault_end != RETQ:
            return self._rax
        cv = self._rd(cbuf, 4, 0x468DCD)
        if cv is None:
            return self._rax
        czv = self._rd(cbuf + 8, 4, 0x468DD8)
        if czv is None:
            return self._rax
        cx, cz = u2f(cv), u2f(czv)
        if _ueq(cx, p1x):
            p1z2 = self._rd(seg + 8, 4, 0x468DE2)
            if p1z2 is None:
                return self._rax
            if _ueq(cz, u2f(p1z2)):
                return 0
        ey = self._rd(edge + 4, 4, 0x468DEE)
        if ey is None:
            return self._rax
        ex = self._rd(edge, 4, 0x468DF3)
        if ex is None:
            return self._rax
        cy = self._rd(cbuf + 4, 4, 0x468DF7)
        if cy is None:
            return self._rax
        sr = self._rd(seg + 0x20, 4, 0x468DFD)
        if sr is None:
            return self._rax
        ez = self._rd(edge + 8, 4, 0x468E06)
        if ez is None:
            return self._rax
        er = self._rd(edge + 0x10, 4, 0x468E0B)
        if er is None:
            return self._rax
        rad = _a(u2f(sr), u2f(er))
        dy = _s(u2f(ey), u2f(cy))
        dx = _s(u2f(ex), cx)
        dz = _s(u2f(ez), cz)
        d2 = _a(_a(_m(dx, dx), _m(dy, dy)), _m(dz, dz))
        return 1 if _seta(rad, self.sqrtf(f2u(d2))) else 0

    def capt1(self, seg, edge, cbuf):
        """00468E50 — capsule B: CPSEG first; point-seg skips the
        ==p1 exclusion; TRIGD(edge,closest)+d[seg+0x20] > dist."""
        self.cpseg(cbuf, seg, edge, seg + 0x10)
        if self.fault_end != RETQ:
            return self._rax
        p1x = self._rd(seg, 4, 0x468E7C)
        if p1x is None:
            return self._rax
        p2x = self._rd(seg + 0x10, 4, 0x468E80)
        if p2x is None:
            return self._rax
        cv = self._rd(cbuf, 4, 0x468E8C)
        if cv is None:
            return self._rax
        czv = self._rd(cbuf + 8, 4, 0x468E95)
        if czv is None:
            return self._rax
        p1x, p2x = u2f(p1x), u2f(p2x)
        cx, cz = u2f(cv), u2f(czv)
        point = _ueq(p1x, p2x)
        if point:
            p1z = self._rd(seg + 8, 4, 0x468EA5)
            if p1z is None:
                return self._rax
            p2z = self._rd(seg + 0x18, 4, 0x468EAA)
            if p2z is None:
                return self._rax
            p1z, p2z = u2f(p1z), u2f(p2z)
            point = _ueq(p1z, p2z)
        else:
            p1z = p2z = None
        if not point:
            if _ueq(cx, p1x):
                p1z = self._rd(seg + 8, 4, 0x468EB9)
                if p1z is None:
                    return self._rax
                if _ueq(cz, u2f(p1z)):
                    return 0
        ez = self._rd(edge + 8, 4, 0x468EE3)
        if ez is None:
            return self._rax
        ey = self._rd(edge + 4, 4, 0x468EF2)
        if ey is None:
            return self._rax
        ex = self._rd(edge, 4, 0x468F05)
        if ex is None:
            return self._rax
        cy = self.mf(cbuf + 4)
        tg = self.trigd(edge, cbuf)
        if self.fault_end != RETQ:
            return self._rax
        sr = self._rd(seg + 0x20, 4, 0x468F1C)
        if sr is None:
            return self._rax
        lim = _a(tg, u2f(sr))
        dz = _s(u2f(ez), cz)
        dy = _s(u2f(ey), cy)
        dx = _s(u2f(ex), cx)
        d2 = _a(_a(_m(dx, dx), _m(dy, dy)), _m(dz, dz))
        return 1 if _seta(lim, self.sqrtf(f2u(d2))) else 0

    def capv(self, a, b, rad, p):
        """00469410 — sibling capsule variant: t<0 uses (a-p)^2;
        t>1 uses b; ret (rad+d[r9+0x10])^2 > |closest-p|^2 (x,z)."""
        bz = self._rd(b + 8, 4, 0x469414)
        if bz is None:
            return self._rax
        pr = self._rd(p + 0x10, 4, 0x469421)
        if pr is None:
            return self._rax
        bx = self._rd(b, 4, 0x46942C)
        if bx is None:
            return self._rax
        ay = self._rd(a + 4, 4, 0x469442)
        if ay is None:
            return self._rax
        by = self._rd(b + 4, 4, 0x469452)
        if by is None:
            return self._rax
        py = self._rd(p + 4, 4, 0x469457)
        if py is None:
            return self._rax
        ax = self._rd(a, 4, 0x46945D)
        if ax is None:
            return self._rax
        az = self._rd(a + 8, 4, 0x46946B)
        if az is None:
            return self._rax
        px = self._rd(p, 4, 0x469475)
        if px is None:
            return self._rax
        pz = self._rd(p + 8, 4, 0x46948B)
        if pz is None:
            return self._rax
        ax, ay, az = u2f(ax), u2f(ay), u2f(az)
        bx, by, bz = u2f(bx), u2f(by), u2f(bz)
        px, py, pz = u2f(px), u2f(py), u2f(pz)
        lim2 = _m(_a(rad, u2f(pr)), _a(rad, u2f(pr)))
        apx, apy, apz = _s(ax, px), _s(ay, py), _s(az, pz)
        abx, aby, abz = _s(ax, bx), _s(ay, by), _s(az, bz)
        dot = _a(_a(_m(apy, aby), _m(apx, abx)), _m(apz, abz))
        l2 = _a(_a(_m(aby, aby), _m(abx, abx)), _m(abz, abz))
        t = _d(dot, l2)
        if not math.isnan(t) and 0.0 > t:
            d2 = _a(_m(apz, apz), _m(apx, apx))
            return 1 if _seta(lim2, d2) else 0
        if math.isnan(t) or t <= 1.0:
            # comiss t,1.0f; ja skips lerp only on ordered t>1
            cx = _a(_m(_s(bx, ax), t), ax)
            cz = _a(_m(_s(bz, az), t), az)
        else:
            cx, cz = bx, bz
        dz_ = _s(cz, pz)
        dx_ = _s(cx, px)
        d2 = _a(_m(dz_, dz_), _m(dx_, dx_))
        return 1 if _seta(lim2, d2) else 0

    def rdec(self, idx, out, vsp):
        """0032A6E0 — nav-record decode. rec = q[NRO+0x1a0] +
        sx32(idx)*16; vtx = q[NRO+0x188] + sx16(w[rec+2])*64."""
        nro = self.mq(NRROOT)
        self._rax = nro & 0xFFFFFFFFFFFFFFFF  # mov rax,[rip]
        i = idx & 0xFFFFFFFF
        if i >= 0x80000000:
            i -= 0x100000000
        rp = self._rd(nro + 0x1A0, 8, 0x32A6F7)
        if rp is None:
            return self._rax
        rec = (rp + i * 16) & 0xFFFFFFFFFFFFFFFF
        vi = self._rd(rec + 2, 2, 0x32A6FE)
        if vi is None:
            return self._rax
        if vi >= 0x8000:
            vi -= 0x10000
        vp = self._rd(nro + 0x188, 8, 0x32A707)
        if vp is None:
            return self._rax
        vtx = (vp + vi * 64) & 0xFFFFFFFFFFFFFFFF
        iv = []
        for k, site in enumerate((0x32A70E, 0x32A717, 0x32A720)):
            v = self._rd(rec + 4 + k * 2, 2, site)
            if v is None:
                return self._rax
            sv16 = v - 0x10000 if v >= 0x8000 else v
            self._rax = sv16 & 0xFFFFFFFF     # movsx eax
            self.sd(vsp + 0x20 + k * 4, sv16 & 0xFFFFFFFF)
            iv.append(sv16)
        iv.append(self.md(vsp + 0x2C))        # stale stack lane
        scl = [self.mf(SCLV + k * 4) for k in range(4)]
        sv = [_m(float(iv[k]), scl[k]) for k in range(4)]
        if not self.mapped(RSCRATCH):         # movdqu scratch
            self.faults.append(("memw", RSCRATCH, 16))
            self.fault_end = 0x32A735
            return self._rax
        for k in range(4):
            self.sf(RSCRATCH + k * 4, sv[k])
        f30 = self._rd(vtx + 0x30, 4, 0x32A73D)
        if f30 is None:
            return self._rax
        self._rax = f30                       # mov eax
        if not self._sd_flt(out, f30, 0x32A740):
            return self._rax
        f34 = self._rd(vtx + 0x34, 4, 0x32A745)
        if f34 is None:
            return self._rax
        self._rax = f34
        if not self._sd_flt(out + 4, f34, 0x32A748):
            return self._rax
        f38 = self._rd(vtx + 0x38, 4, 0x32A74B)
        if f38 is None:
            return self._rax
        self._rax = f38
        if not self._sf_flt(out + 0xC, sv[0], 0x32A752):
            return self._rax
        if not self._sf_flt(out + 0x10, sv[1], 0x32A757):
            return self._rax
        if not self._sd_flt(out + 8, f38, 0x32A75C):
            return self._rax
        f20 = self._rd(vtx + 0x20, 4, 0x32A75F)
        if f20 is None:
            return self._rax
        f28 = self._rd(vtx + 0x28, 4, 0x32A764)
        if f28 is None:
            return self._rax
        if not self._sf_flt(out + 0x14, self.at2(f28, f20),
                            0x32A76E):
            return self._rax
        return out

    def lquery(self, p1, p2, rad_u, vsp):
        """00391410 — segment LOS query over the wall-record grid.
        Frame rsp = vsp-0x128; seg v1 at +0x40=vsp-0xE8, v2 +0x50=
        vsp-0xD8, tmp +0x20=vsp-0x108, tmp2 +0x30=vsp-0xF8, rec vec
        +0x70=vsp-0xB8, rdec out rbp-0x70=vsp-0x98, rad rbp-0x80=
        vsp-0xA8. CAPT scratch cbuf = vsp-0x160."""
        root = self.mq(ROOTCELL)
        self._rax = root
        if root == 0:
            return 0
        csz = self.mf(LCSZ)
        epsx = self.mf(LEPSX)
        epsz = self.mf(LEPSZ)
        rad = u2f(rad_u)
        p1z = self._rd(p1 + 8, 4, 0x39145C)
        if p1z is None:
            return self._rax
        p2z = self._rd(p2 + 8, 4, 0x391461)
        if p2z is None:
            return self._rax
        p2x = self._rd(p2, 4, 0x391497)
        if p2x is None:
            return self._rax
        p1x = self._rd(p1, 4, 0x3914AD)
        if p1x is None:
            return self._rax
        p1x, p2x, p1z, p2z = u2f(p1x), u2f(p2x), u2f(p1z), u2f(p2z)
        z1 = _maxss(p1z, p2z)
        z0 = _minss(p1z, p2z)
        x1 = _maxss(p1x, p2x)
        x0 = _minss(p1x, p2x)
        zhi = _cvtt(_d(_s(_a(z1, rad), epsz), csz))
        zlo = _cvtt(_d(_s(_s(z0, rad), epsz), csz))
        xhi = _cvtt(_d(_s(_a(x1, rad), epsx), csz))
        xlo = _cvtt(_d(_s(_s(x0, rad), epsx), csz))
        self._rax = self.bmask(xlo, zlo, xhi, zhi)
        if self.fault_end != RETQ:
            return self._rax
        S1 = (vsp - 0xE8) & 0xFFFFFFFFFFFFFFFF
        S2 = (vsp - 0xD8) & 0xFFFFFFFFFFFFFFFF
        TMP = (vsp - 0x108) & 0xFFFFFFFFFFFFFFFF
        TMP2 = (vsp - 0xF8) & 0xFFFFFFFFFFFFFFFF
        V70 = (vsp - 0xB8) & 0xFFFFFFFFFFFFFFFF
        RBP70 = (vsp - 0x98) & 0xFFFFFFFFFFFFFFFF
        RBP80 = (vsp - 0xA8) & 0xFFFFFFFFFFFFFFFF
        CBUF = (vsp - 0x160) & 0xFFFFFFFFFFFFFFFF
        # seg vecs {x,0,z,uninit} — radius at S2+0x10 = rsp+0x60
        self.sf(S1, p1x)
        self.sd(S1 + 4, 0)
        self.sf(S1 + 8, p1z)
        self.sf(S2, p2x)
        self.sd(S2 + 4, 0)
        self.sf(S2 + 8, p2z)
        self.sf(S2 + 0x10, rad)
        self.dist(S1, S2)                    # dead call, traced
        if self.fault_end != RETQ:
            return self._rax
        for i in range(160):
            msk = self.mq(LBMSK)
            self._rax = msk               # mov rax,[rip+LBMSK]
            bit = self._rd(msk + 0x10 + i // 8, 1, 0x391579)
            if bit is None:
                return self._rax
            self._rax = 1                 # mov eax,1 (shl src)
            if not (bit & (1 << (i % 8))):
                continue
            if i < 0x20:
                po = self._rd(root + 0x28, 4, 0x391597)
                if po is None:
                    return self._rax
                rec = (self.base(po) + i * 0x20) & 0xFFFFFFFFFFFFFFFF
                self._rax = rec               # add rax, rdi
                t = self._rd(rec, 2, 0x3915A3)
                if t is None:
                    return self._rax
                if t == 0:
                    x = self._rd(rec + 4, 4, 0x3915F9)
                    if x is None:
                        return self._rax
                    z = self._rd(rec + 8, 4, 0x391616)
                    if z is None:
                        return self._rax
                    rr = self._rd(rec + 0xC, 4, 0x391629)
                    if rr is None:
                        return self._rax
                    self.sf(V70, u2f(x))
                    self.sd(V70 + 4, 0)
                    self.sf(V70 + 8, u2f(z))
                    self.sf(V70 + 0xC, 1.0)
                    self.sd(RBP80, rr)       # rdx+0x10 = rsp+0x80
                    r = self.capt0(S1, V70, CBUF)
                    if self.fault_end != RETQ:
                        return self._rax
                elif t == 1:
                    x = self._rd(rec + 4, 4, 0x3915B3)
                    if x is None:
                        return self._rax
                    z = self._rd(rec + 8, 4, 0x3915C6)
                    if z is None:
                        return self._rax
                    x2 = self._rd(rec + 0xC, 4, 0x3915D9)
                    if x2 is None:
                        return self._rax
                    z2 = self._rd(rec + 0x10, 4, 0x3915E4)
                    if z2 is None:
                        return self._rax
                    an = self._rd(rec + 0x14, 4, 0x3915EF)
                    if an is None:
                        return self._rax
                    self.sf(TMP, u2f(x))
                    self.sd(TMP + 4, 0)
                    self.sf(TMP + 8, u2f(z))
                    self.sf(TMP + 0xC, 1.0)
                    self.sf(TMP2, u2f(x2))
                    self.sf(TMP2 + 4, u2f(z2))
                    self.sf(TMP2 + 8, u2f(an))
                    r = self.capt1(S1, TMP, CBUF)
                    if self.fault_end != RETQ:
                        return self._rax
                else:
                    continue
            else:
                self.rdec(i - 0x20, RBP70,
                          (vsp - 0x168) & 0xFFFFFFFFFFFFFFFF)
                if self.fault_end != RETQ:
                    return self._rax
                x = self.mf(RBP70)
                z = self.mf(RBP70 + 8)
                x2 = self.mf(RBP70 + 0xC)
                z2 = self.mf(RBP70 + 0x10)
                an = self.mf(RBP70 + 0x14)
                self.sf(TMP, x)
                self.sd(TMP + 4, 0)
                self.sf(TMP + 8, z)
                self.sf(TMP + 0xC, 1.0)
                self.sf(TMP2, x2)
                self.sf(TMP2 + 4, z2)
                self.sf(TMP2 + 8, an)
                r = self.capt1(S1, TMP, CBUF)
                if self.fault_end != RETQ:
                    return self._rax
            if r != 0:
                return 1
        return 0


def run_model(case, raw, secs):
    m = Model(case, raw, secs)
    for step in case.get("steps", []):
        entry, rcx = step[0], step[1]
        rdx = step[2] if len(step) > 2 else 0
        r8 = step[3] if len(step) > 3 else 0
        r9 = step[4] if len(step) > 4 else 0
        if entry == QWALK:
            m.rets.append(m.qwalk(rcx, rdx, r8, STACK + 0x80000))
        elif entry == WWRAP:
            m.rets.append(m.wwrap(rcx, STACK + 0x80008))
        elif entry == GGRID:
            m.rets.append(m.ggrid(rcx))
        elif entry == TTEST:
            m.rets.append(m.ttest(rcx, rdx))
        elif entry in (ETHUNK, ECLASS):
            m.rets.append(m.eclass(rcx, rdx))
        elif entry == SEGT:
            m.rets.append(m.segt(rcx, rdx, r8, r9, STACK + 0x80000))
        elif entry == BASE:
            m.rets.append(m.base(rcx))
        elif entry == ROOTL:
            m.rets.append(m.mq(ROOTCELL))
        elif entry == PRED:
            xmm2 = step[6] if len(step) > 6 else 0
            m.rets.append(m.pred(rcx, rdx, u2f(xmm2 & 0xFFFFFFFF),
                                 r9, STACK + 0x80000))
        elif entry == PATHW:
            m.rets.append(m.pathw(rcx, rdx, STACK + 0x80000))
        elif entry == BLKCHK:
            m.rets.append(m.blkchk(rcx, STACK + 0x80000))
        elif entry == MLOAD:
            m.mload(rcx)
            m.rets.append(m._rax)
        elif entry == AWRAP:
            xmm0 = step[5] if len(step) > 5 else 0
            m.awrap(u2f(xmm0 & 0xFFFFFFFF))
            m.rets.append(m._rax)
        elif entry == RBUILD:
            xmm2 = step[6] if len(step) > 6 else 0
            m.rbuild(rcx, rdx, u2f(xmm2 & 0xFFFFFFFF))
            m.rets.append(m._rax)
        elif entry == ROTCOL:
            xmm2 = step[6] if len(step) > 6 else 0
            xmm1 = step[7] if len(step) > 7 else 0
            m.rotcol(rcx, u2f(xmm1 & 0xFFFFFFFF),
                     u2f(xmm2 & 0xFFFFFFFF))
            m.rets.append(m._rax)
        elif entry == MXVW:
            m.mxvw(rcx, rdx, r8, STACK + 0x80000)
            m.rets.append(m._rax)
        elif entry == MXV:
            m.mxv(rcx, rdx, r8)
            m.rets.append(m._rax)
        elif entry == LQUERY:
            xmm2 = step[6] if len(step) > 6 else 0
            m.rets.append(m.lquery(rcx, rdx, xmm2, STACK + 0x80000))
        elif entry == BMASK:
            m.rets.append(m.bmask(rcx, rdx, r8, r9))
        elif entry == DIST:
            m.dist(rcx, rdx)
            m.rets.append(m._rax)
        elif entry == CAPT0:
            m.rets.append(m.capt0(rcx, rdx, SEGV + 0x100))
        elif entry == CAPT1:
            m.rets.append(m.capt1(rcx, rdx, SEGV + 0x100))
        elif entry == CPSEG:
            m.cpseg(rcx, rdx, r9, r8)   # native: rdx=a r8=b r9=p
            m.rets.append(m._rax)
        elif entry == TRIGD:
            m.trigd(rcx, rdx)
            m.rets.append(m._rax)
        elif entry == CAPV:
            xmm2 = step[6] if len(step) > 6 else 0
            m.rets.append(m.capv(rcx, rdx, u2f(xmm2 & 0xFFFFFFFF),
                                 r9))
        elif entry == RDEC:
            m.rdec(rcx, rdx, STACK + 0x80000 - 0x40)
            m.rets.append(m._rax)
        elif entry == PVAL:
            xmm1 = step[7] if len(step) > 7 else 0
            xmm2 = step[6] if len(step) > 6 else 0
            xmm3 = step[8] if len(step) > 8 else 0
            m.rets.append(m.pathval(rcx,
                                    u2f(xmm1 & 0xFFFFFFFF),
                                    u2f(xmm2 & 0xFFFFFFFF),
                                    u2f(xmm3 & 0xFFFFFFFF),
                                    STACK + 0x80000))
        elif entry == MCPY:
            xmm2 = step[6] if len(step) > 6 else 0
            m.mcpy(rcx, rdx, u2f(xmm2 & 0xFFFFFFFF))
            m.rets.append(m._rax)
        elif entry == ROTX:
            xmm2 = step[6] if len(step) > 6 else 0
            xmm1 = step[7] if len(step) > 7 else 0
            m.rotx(rcx, u2f(xmm1 & 0xFFFFFFFF),
                   u2f(xmm2 & 0xFFFFFFFF))
            m.rets.append(m._rax)
        elif entry == DE6A0:
            m.rets.append(m.de6a0(rcx, rdx, r8))
        elif entry == GATE:
            xmm2 = step[6] if len(step) > 6 else 0
            m.rets.append(m.gate(rcx, rdx, r8, r9,
                                 u2f(xmm2 & 0xFFFFFFFF),
                                 STACK + 0x80000))
        elif entry == LHELP:
            m.rets.append(m.lhelp(rcx))
        elif entry == OCLS:
            m.rets.append(m.ocls(rcx))
        elif entry == GTAB:
            m.rets.append(m.gtab(rcx))
        elif entry == MABE:
            m.rets.append(m.mabe(rcx))
        elif entry == GCHK:
            m.rets.append(m.gchk(rcx))
        elif entry == GPT:
            m.rets.append(m.gpt(rcx, rdx, r8, r9, STACK + 0x80000))
        elif entry == GSEG:
            m.rets.append(m.gseg(rcx, rdx, r8, r9, STACK + 0x80000))
        elif entry == GPC:
            m.rets.append(m.gpc(rcx, rdx, r8, STACK + 0x80000))
        elif entry == GSC:
            m.rets.append(m.gsc(rcx, rdx, r8, STACK + 0x80000))
        elif entry == GFILT:
            m.rets.append(m.gfilt(rcx, rdx, r8, r9, STACK + 0x80000))
        elif entry == S3W:
            m.s3w(rcx, rdx)
            m.rets.append(m._rax)
        elif entry == S2W:
            m.s2w(rcx, rdx, STACK + 0x80000)
            m.rets.append(m._rax)
        elif entry == CDST:
            m.rets.append(m.cdst(rcx, rdx))
        elif entry == CDZ0:
            m.rets.append(m.cdz0(rcx, rdx))
        elif entry == CF90:
            m.rets.append(m.cf90(rcx, rdx, STACK + 0x80000))
        # ---- EXP-136 direct accessor steps ----
        elif entry == OBJD:
            m.rets.append(m.objd(rcx))
        elif entry == O3FW:
            m.o3fw(rcx, rdx, r8, r9)
            m.rets.append(m._rax)
        elif entry == O2FW:
            m.o2fw(rcx, rdx, r8)
            m.rets.append(m._rax)
        elif entry == O1F:
            m.o1f(rcx)
            m.rets.append(m._rax)
        elif entry == O1F2:
            m.o1f2(rcx)
            m.rets.append(m._rax)
        elif entry == O1F3:
            m.o1f3(rcx)
            m.rets.append(m._rax)
        elif entry == OVF:
            m.rets.append(m.ovf(rcx))
        elif entry == OPA:
            m.rets.append(m.opa(rcx, rdx))
        elif entry == OPB:
            m.rets.append(m.opb(rcx, rdx, r8,
                                STACK + 0x80000))
        elif entry == OF60:
            m.rets.append(m.of60(rcx))
        elif entry == OSUB:
            m.rets.append(m.osub(rcx))
        elif entry == MABESP:
            m.rets.append(m.mabesp(rcx))
        elif entry == DE100:
            m.rets.append(m.de100(rcx, rdx, r8))
        elif entry == AGENTQ:
            m.rets.append(m.agq(rcx, rdx, r8, r9))
        m.ends.append(m.fault_end)
        m.fault_end = RETQ
    mem = {}
    for addr, n in case.get("watch", []):
        mem["%x" % addr] = bytes(
            m.mb(addr + i) for i in range(n)).hex()
    return {"trace": m.trace, "faults": m.faults, "rets": m.rets,
            "ends": m.ends, "mem": mem}


# ---------------- cases ----------------

W_PT = [(PT, 8)]
W_VV = [(VECX, 0x10), (VECY, 0x10)]
W_WALK = [(WQ40, 8), (WQ50, 0x10), (WQ60, 0x10)]
W_SEGT = [(SQVA, 0x10), (SQVB, 0x10), (SQVC, 0x10), (SQVD, 0x10)]


def ob(sz=0x800, **kw):
    """object bytes: keys b<off>/w<off>/d<off>/q<off>/f<off> hex."""
    o = bytearray(sz)
    for k, v in kw.items():
        t, a = k[0], int(k[1:], 16)
        o[a:a + {"b": 1, "w": 2, "d": 4, "q": 8, "f": 4}[t]] = \
            {"b": bb, "w": ww, "d": dw, "q": qw, "f": ff}[t](v)
    return bytes(o)


def b8r(addr, f0a=None, f0=None, **kw):
    """+0xB8 record plant pair: record (kw fields: d0/d4/d8 vec,
    f24, f38, f40/44/48, d50/54, f68, fA8, fC0, b107, qF0) plus
    its +0xF0 sub-record (f0 fields: f24)."""
    f0a = addr + 0x200 if f0a is None else f0a
    kw["qF0"] = f0a
    return [(addr, ob(0x200, **kw)),
            (f0a, ob(0x100, **(f0 or {})))]


def gchkpl(obj, c0, c138, **kw):
    """gplants making `obj` a full object record: q30 self-
    decode, variant 3 (b3=0x60), GCHK-valid (OVF real arm ->
    c0 flags ret 0 -> b4==3 arm)."""
    kw2 = {"qC0": c0, "b8": 8, "b4": 3, "b3": 0x60, "q30": obj}
    kw2.update(kw)
    return [(obj, ob(**kw2)),
            (c0, ob(0x200, q138=c138)),
            (c138, ob(0x100, fF0=1.0))]


def gfix(extra=(), **kw):
    """standard GATE fixture: self=SELFO via real MABESP decode
    (handle 0x42 -> msparr[0x42]=SELFO) + GCHK-valid; empty
    collector (grcnt=0) -> gate returns 0."""
    d = {"mabef": 0x10, "gtab": [0x42],
         "msparr": {0x42: SELFO},
         "gplants": gchkpl(SELFO, GC0A, GC138A, qB8=SELF_B8)
                    + b8r(SELF_B8, f0a=SELF_F0)
                    + list(extra)}
    d.update(kw)
    return d


def gpop(extra=(), crec=(2.0, 0.0, 2.0), **kw):
    """populated GATE fixture: one candidate handle CANDA through
    collector+filter+walk. CANDA: self-decoding q30, variant-3
    b3, qB8=crec (on-seg tmp; (2,0,2) for P1->P2 direct steps,
    (1,0,2) for the pv path), q10=OSUBA sub, GCHK-valid."""
    d = gfix(gchkpl(CANDA, GC0A + 0x800, GC138A + 0x800,
                    q698=G698A, qB8=QB8A, q10=OSUBA)
             + b8r(QB8A, d0=f2u(crec[0]), d4=f2u(crec[1]),
                   d8=f2u(crec[2]))
             + [(OSUBA, ob(b3=0x60, qB8=CTX_B8))]
             + b8r(CTX_B8, f0a=CTX_F0)
             + list(extra),
             grcnt=1, ghnd=[CANDA],
             cflags=[1] * 0x100,
             lsrc={ci: b"\x01" for ci in range(64)},
             opbrets=[4])
    d.update(kw)
    return d


def cases():
    C = {}
    # --- BASE / ROOTL leaves ---
    C["base-0"] = {"steps": [(BASE, 0)]}
    C["base-off"] = {"steps": [(BASE, 0x1234)]}
    C["rootl"] = {"steps": [(ROOTL, 0)]}
    # --- ECLASS via real thunk 0x32A780 (ecx=class, dx=flag) ---
    C["cls-w0"] = {"steps": [(ETHUNK, 0, 0)]}        # cl=23 in w0 -> 1
    C["cls-both"] = {"steps": [(ETHUNK, 1, 1)]}      # cl=25 w0&w1 -> 2
    C["cls-w1"] = {"steps": [(ETHUNK, 2, 2)]}        # cl=26 w1 -> 0
    C["cls-none"] = {"steps": [(ETHUNK, 3, 0)]}      # absent -> 0
    C["cls-neg"] = {"steps": [(ETHUNK, 0, 4)]}       # classtab -1 -> -1
    C["cls-b24"] = {"bptab": [(0, 1 << 24)],
                    "steps": [(ETHUNK, 0, 5)]}       # cl=24 w1 -> 0
    # --- TTEST direct (idx array = planted {i0,i1,i2}) ---
    C["tri-in"] = {"steps": [(TTEST, IARR, PT)]}     # (1,1) in T0
    C["tri-out"] = {"ptx": 3.0, "pty": 3.5,
                    "steps": [(TTEST, IARR, PT)]}   # x+y>4 -> 0
    C["tri-below"] = {"ptx": 1.0, "pty": -1.0,     # below v0-v1 edge
                      "steps": [(TTEST, IARR, PT)]}  # edge0 cross flips -> 0
    C["tri-edge"] = {"ptx": 2.0, "pty": 2.0,       # on v1-v2 edge
                     "steps": [(TTEST, IARR, PT)]}
    C["tri-vtx"] = {"ptx": 0.0, "pty": 0.0,        # on v0
                    "steps": [(TTEST, IARR, PT)]}
    C["tri-nan"] = {"ptx": float("nan"),
                    "steps": [(TTEST, IARR, PT)]}   # NaN -> inside
    C["tri-badptr"] = {"steps": [(TTEST, 0xFFFFFFF0, PT)]}
    # --- SEGT direct (p1,p2,va,vb vec4s) ---
    C["seg-cross"] = {"steps": [(SEGT, P1, P2, VECX, VECY)],
                      "watch": W_SEGT}
    C["seg-para"] = {"p2x": 1.0, "p2z": 0.0,
                     "steps": [(SEGT, P1, P2, VECX, VECY)]}
    C["seg-far"] = {"p2x": 1.2, "p2z": 0.5,
                    "steps": [(SEGT, P1, P2, VECX, VECY)]}
    C["seg-touch"] = {"p2x": 2.0, "p2z": 2.0,      # p2 on edge
                      "steps": [(SEGT, P1, P2, VECX, VECY)]}
    C["seg-rev"] = {"p1x": 2.0, "p1z": 2.0, "p2x": 1.0, "p2z": 1.0,
                    "steps": [(SEGT, P1, P2, VECX, VECY)]}  # h1>0,i1<0 -> 1
    C["seg-vert"] = {"p1x": 1.0, "p1z": 1.0, "p2x": 1.0, "p2z": 2.0,
                     "steps": [(SEGT, P1, P2, VECX, VECY)]}  # h2,i2>0 -> 0
    C["seg-beyond2"] = {"p1x": 4.0, "p1z": 4.0, "p2x": 5.0, "p2z": 5.0,
                        "steps": [(SEGT, P1, P2, VECX, VECY)]}  # h2,i2<0
    C["seg-vline"] = {"p1x": 5.0, "p1z": 9.0, "p2x": 5.0, "p2z": -2.0,
                      "steps": [(SEGT, P1, P2, VECX, VECY)]}  # h1,i1<0
    C["seg-badptr"] = {"steps": [(SEGT, 0xFFFFFFF0, P2, VECX, VECY)]}
    # --- WWRAP {x,z} pair ---
    C["wrap-t0"] = {"steps": [(WWRAP, P1)]}         # (1,1) -> 0
    C["wrap-t1"] = {"steps": [(WWRAP, P2)]}         # (3,3) -> 1
    # --- GGRID direct ---
    C["grid-t0"] = {"steps": [(GGRID, PT)]}
    C["grid-t1"] = {"ptx": 3.0, "pty": 3.0,
                    "steps": [(GGRID, PT)]}
    C["grid-multi"] = {"ptx": 3.0, "pty": 0.5,     # cell{0,1}->T0
                       "steps": [(GGRID, PT)]}
    C["grid-multi2"] = {"ptx": 1.0, "pty": 3.5,    # {0,1}->T1
                        "steps": [(GGRID, PT)]}
    C["grid-nanx"] = {"ptx": float("nan"),
                      "steps": [(GGRID, PT)]}
    C["grid-nany"] = {"pty": float("nan"),
                      "steps": [(GGRID, PT)]}
    C["grid-neg"] = {"ptx": -1.0, "steps": [(GGRID, PT)]}
    C["grid-beyond"] = {"ptx": 9.0, "steps": [(GGRID, PT)]}
    C["grid-orig"] = {"ptx": 0.0, "pty": 0.0,
                      "steps": [(GGRID, PT)]}
    C["grid-cw4"] = {"ghdr": {"ch": 4}, "ptx": 5.0, "pty": 1.0,
                     "steps": [(GGRID, PT)]}   # cellH=4: (5,1)->T2
    C["grid-ffff"] = {"cells": [0xFFFF] + CELLS[1:],
                      "steps": [(GGRID, PT)]}
    C["grid-empty"] = {"cells": [0x14] + CELLS[1:],
                       "lists": [[]] + LISTS[1:],
                       "steps": [(GGRID, PT)]}
    C["grid-badptr"] = {"steps": [(GGRID, 0xFFFFFFF0)]}
    C["grid-badroot"] = {"rootp": 0xFFFFFFF0,
                         "steps": [(GGRID, PT)]}
    # --- QWALK ---
    C["walk-same"] = {"steps": [(QWALK, P1, P2, 0)],
                      "watch": W_WALK}
    C["walk-same2"] = {"p2x": 1.5, "p2z": 1.5,
                       "steps": [(QWALK, P1, P2, 0)],
                       "watch": W_WALK}
    C["walk-p1off"] = {"p1x": -1.0, "p1z": -1.0,
                       "steps": [(QWALK, P1, P2, 0)]}
    C["walk-p2off"] = {"p2x": 9.0, "p2z": 9.0,
                       "steps": [(QWALK, P1, P2, 0)]}
    C["walk-p2cyc"] = {"p2x": 9.0, "p2z": 9.0,     # p2 off + cycle adj
                       "adj": [[0, 1, 0, 0], [0, 0, 2, 0],
                               [1, 0, 0, 0], [0, 0, 0, 0]],
                       "steps": [(QWALK, P1, P2, 0)]}
    C["walk-2hop"] = {"p2x": 6.0, "p2z": 1.0,      # T0->T1->T2
                      "eflag": [0, 4, 0, 0],       # e0 flag byte != class
                      "steps": [(QWALK, P1, P2, 0)],
                      "watch": W_WALK}
    C["walk-3hop"] = {"p2x": 6.0, "p2z": 3.0,      # ->T3
                      "steps": [(QWALK, P1, P2, 0)],
                      "watch": W_WALK}
    C["walk-negcls"] = {"steps": [(QWALK, P1, P2, 4)]}
    C["walk-cls2"] = {"eclass": [0, 1, 0, 0],      # e0 w0&w1 b25
                      "steps": [(QWALK, P1, P2, 1)]}
    C["walk-flag"] = {"eclass": [0, 2, 0, 0],      # e0 w1 b26
                      "eflag": [0, 4, 0, 0],       # b6 bit2 set
                      "steps": [(QWALK, P1, P2, 2)],
                      "watch": W_WALK}
    C["walk-noflag"] = {"eclass": [0, 2, 0, 0],
                        "eflag": [0, 0, 0, 0],
                        "steps": [(QWALK, P1, P2, 2)]}
    C["walk-cycle"] = {
        # T3 unreachable (dst=3); seg crosses e0/e1 -> closed
        # T0->T1->T2->T0 cycle -> 0x80 budget -> ret 0
        "adj": [[0, 1, 0, 0], [0, 0, 2, 0], [1, 0, 0, 0],
                [0, 0, 0, 0]],
        "p2x": 6.0, "p2z": 3.0,
        "steps": [(QWALK, P1, P2, 0)]}
    C["walk-badptr"] = {"steps": [(QWALK, 0xFFFFFFF0, P2, 0)]}
    # ---------- EXP-132 consumer cases ----------
    # --- helper-level ---
    C["mload-const"] = {"steps": [(MLOAD, MATB)],
                        "watch": [(MATB, 0x40)]}
    C["awrap-zero"] = {"steps": [(AWRAP, 0, 0, 0, 0, f2u(0.0))]}
    C["awrap-pi2"] = {"steps": [(AWRAP, 0, 0, 0, 0,
                                 f2u(math.pi / 2))]}
    C["awrap-3pi2"] = {"steps": [(AWRAP, 0, 0, 0, 0,
                                  f2u(3 * math.pi / 2))]}  # -> -pi/2
    C["awrap-n3pi2"] = {"steps": [(AWRAP, 0, 0, 0, 0,
                                   f2u(-3 * math.pi / 2))]}
    C["awrap-pi"] = {"steps": [(AWRAP, 0, 0, 0, 0,
                                f2u(math.pi))]}            # edge
    C["awrap-4pi"] = {"steps": [(AWRAP, 0, 0, 0, 0,
                                 f2u(4 * math.pi))]}       # edge
    C["awrap-big"] = {"steps": [(AWRAP, 0, 0, 0, 0,
                                 f2u(40.0))]}              # mod path
    C["awrap-negbig"] = {"steps": [(AWRAP, 0, 0, 0, 0,
                                    f2u(-40.0))]}
    C["awrap-nan"] = {"steps": [(AWRAP, 0, 0, 0, 0,
                                 f2u(float("nan")))]}
    C["awrap-inf"] = {"steps": [(AWRAP, 0, 0, 0, 0,
                                 f2u(float("inf")))]}
    C["awrap-neginf"] = {"steps": [(AWRAP, 0, 0, 0, 0,
                                    f2u(float("-inf")))]}
    C["awrap-n7pi2"] = {"steps": [(AWRAP, 0, 0, 0, 0,
                                   f2u(-7 * math.pi / 2))]}
    C["awrap-13"] = {"steps": [(AWRAP, 0, 0, 0, 0, f2u(13.0))]}
    C["awrap-n7"] = {"steps": [(AWRAP, 0, 0, 0, 0, f2u(-7.0))]}
    C["rbuild-rot"] = {"steps": [(RBUILD, MATB + 0x100, MATB,
                                 0, 0, 0, f2u(math.pi / 4))],
                       "watch": [(MATB + 0x100, 0x40)]}
    C["rbuild-zero"] = {"steps": [(RBUILD, MATB + 0x100, MATB,
                                  0, 0, 0, f2u(0.0))],
                        "watch": [(MATB + 0x100, 0x40)]}
    C["rotcol-mix"] = {"m1": 2.0, "m2": 3.0, "m5": 4.0,
                       "m8": 5.0, "m11": 6.0,
                       "steps": [(ROTCOL, MATB, 0, 0, 0, 0,
                                  f2u(0.6), f2u(0.8))],   # sin .8 cos .6
                       "watch": [(MATB, 0x40)]}
    C["mxv-gen"] = {"m0": 2.0, "m4": 0.5, "m8": 0.25,
                    "m12": 1.0, "m5": 3.0, "m10": 4.0,
                    "steps": [(MXV, DVB, MATB, VECQ)],
                    "watch": [(DVB, 0x10)]}
    C["mxv-badptr"] = {"steps": [(MXV, DVB, MATB, 0xFFFFFFF0)]}
    C["mxvw-gen"] = {"m0": 2.0, "m5": 3.0, "m10": 4.0,
                     "m15": 5.0,
                     "steps": [(MXVW, DVB, MATB, VECQ)],
                     "watch": [(DVB, 0x10)]}
    # --- PATHW 0033A3D0 (rcx=A, rdx=B) ---
    # watch: adj-vec w (frame+0x20) and rotated mat (frame+0x40)
    W_PATHW = [(STACK + 0x7FF88, 0x10), (STACK + 0x7FFA8, 0x40)]
    # direct B->A blocked at T3 exhaust (no e2 crossing) ->
    # rotated offsets reachable -> ret 1
    C["pathw-open"] = {"p1x": 1.0, "p1z": 1.0, "p2x": 6.0,
                       "p2z": 3.0,
                       "eflag": [2, 2, 2, 2],   # bit1 for flag=1
                       "steps": [(PATHW, P1, P2)],
                       "watch": W_PATHW}
    # all edges class-rejected: Q(B->A)=1, both rotated probes
    # blocked -> ret 0
    C["pathw-block"] = {"p1x": 1.0, "p1z": 1.0, "p2x": 6.0,
                        "p2z": 3.0,
                        "eclass": [0, 2, 2, 2],
                        "steps": [(PATHW, P1, P2)],
                        "watch": W_PATHW}
    # direct blocked AND rotated offsets off-grid -> ret 0
    C["pathw-rotfail"] = {"p1x": 0.5, "p1z": 0.5, "p2x": 7.5,
                          "p2z": 3.5,
                          "steps": [(PATHW, P1, P2)],
                          "watch": W_PATHW}
    # direct reachable -> ret 1 immediately
    C["pathw-direct"] = {"p1x": 1.0, "p1z": 1.0, "p2x": 3.0,
                         "p2z": 3.0,
                         "eflag": [2, 2, 2, 2],
                         "steps": [(PATHW, P1, P2)]}
    # direct blocked (e1); r1 arm reaches (e2 flag-bit1), r2
    # blocked (e1) -> ret 0 via round probes
    C["pathw-mixed"] = {"p1x": 1.0, "p1z": 1.0, "p2x": 6.0,
                        "p2z": 3.0,
                        "eclass": [0, 2, 0, 0],
                        "eflag": [2, 0, 2, 0],
                        "steps": [(PATHW, P1, P2)],
                        "watch": W_PATHW}
    # faults: B unmapped (first read 0x33D3FE), A unmapped
    # (second pair read 0x33D442)
    C["pathw-badptrB"] = {"steps": [(PATHW, P1, 0xFFFFFFF0)]}
    C["pathw-badptrA"] = {"steps": [(PATHW, 0xFFFFFFF0, P2)]}
    # r1 probe1 B->w1 same-tri (w1 lands inside T3);
    # r1 probe2 w1->A blocked at e1 -> the probe2 jne site
    # executes; native continues -> ret 0
    C["pathw-r1p2"] = {"p1x": 1.0, "p1z": 1.0, "p2x": 7.0,
                       "p2z": 2.0,
                       "eclass": [0, 0, 2, 0],
                       "eflag": [0, 2, 0, 2],
                       "steps": [(PATHW, P1, P2)]}
    # r1 w1 off-grid (skips r1p2); r2 probe1 B->w2 reachable
    # (w2 in T2 via e2), r2 probe2 w2->A blocked at e1 ->
    # the round-2 jne executes; native continues -> ret 0
    C["pathw-r2p2"] = {"p1x": 1.0, "p1z": 1.0, "p2x": 6.0,
                       "p2z": 3.0,
                       "eclass": [0, 0, 2, 0],
                       "eflag": [0, 2, 0, 2],
                       "steps": [(PATHW, P1, P2)]}
    # --- BLKCHK 00335F90 (rcx=agent) ---
    # watch: nested QWALK frame locals
    W_BLK = [(STACK + 0x7FF58, 8), (STACK + 0x7FF68, 0x10),
             (STACK + 0x7FF78, 0x10)]
    # cross-tri walk, flag bit0 passable, tiny radius scale
    # -> PRED 0 -> walk 0 -> mode 0 -> ret 0
    C["blk-clear"] = {"ag2x": 6.0, "radius": 1e-28,
                      "eflag": [1, 1, 1, 1],
                      "steps": [(BLKCHK, AGENT)],
                      "watch": W_BLK}
    # visible radius -> scale 0.45 shifts the PRED probes
    # (m-blk-sc disp mutant reads 1.2f -> different coords)
    C["blk-scale"] = {"ag2x": 6.0, "radius": 0.5,
                      "eflag": [1, 1, 1, 1],
                      "steps": [(BLKCHK, AGENT)]}
    # all edges class-rejected -> PRED probe exhaust -> ret 1
    C["blk-predblock"] = {"ag2x": 6.0, "eclass": [2, 2, 2, 2],
                          "steps": [(BLKCHK, AGENT)],
                          "watch": W_BLK}
    # class-0 edges, flag byte 0 -> flag gate rejects (mode 0)
    # -> PRED 1 -> ret 1
    C["blk-walkblock"] = {"ag2x": 6.0,
                          "steps": [(BLKCHK, AGENT)],
                          "watch": W_BLK}
    # mode 3 (flag bit3 passable) -> AGENTQ scripted boundary
    C["blk-mode3-0"] = {"mode": 3, "agrets": [0], "ag2x": 6.0,
                        "eflag": [8, 8, 8, 8],
                        "steps": [(BLKCHK, AGENT)],
                        "watch": W_BLK}
    C["blk-mode3-1"] = {"mode": 3, "agrets": [1], "ag2x": 6.0,
                        "eflag": [8, 8, 8, 8],
                        "steps": [(BLKCHK, AGENT)],
                        "watch": W_BLK}
    C["blk-mode3-neg"] = {"mode": 3, "agrets": [-1], "ag2x": 6.0,
                          "eflag": [8, 8, 8, 8],
                          "steps": [(BLKCHK, AGENT)]}
    C["blk-mode7"] = {"mode": 7, "ag2x": 6.0,
                      "eflag": [0x80, 0x80, 0x80, 0x80],
                      "steps": [(BLKCHK, AGENT)]}
    # NaN radius -> scale NaN -> offsets NaN -> probes p1-off -> 0
    C["blk-radiusnan"] = {"radius": float("nan"),
                          "steps": [(BLKCHK, AGENT)]}
    # fault: agent unmapped -> first read 0x335F9F
    C["blk-badptr"] = {"steps": [(BLKCHK, 0xFFFFFFF0)]}
    # fault: sub-record unmapped -> second read 0x335FAD
    C["blk-subbad"] = {"subp": 0xFFFFFFF0,
                       "steps": [(BLKCHK, AGENT)]}
    # --- PRED direct (probes now run real QWALK) ---
    C["pred-clear"] = {"steps": [(PRED, P1, P2, 0, 0, 0, f2u(0.5))]}
    C["pred-blocked"] = {"eclass": [2, 2, 2, 2],
                         "steps": [(PRED, P1, P2, 0, 0, 0,
                                    f2u(0.5))]}
    C["pred-offgrid"] = {"steps": [(PRED, P1, P2, 0, 0, 0,
                                    f2u(10.0))]}
    # ---------- EXP-133 nav-LOS cases ----------
    SEG = SEGV
    EDG = SEGV + 0x30
    OUTB = SEGV + 0x100
    OUTB2 = SEGV + 0x200
    W_BMSK = [(BMSKA, 0x30)]
    W_RBP70 = [(STACK + 0x80000 - 0x98, 0x18)]
    # --- LQUERY 00391410 (rcx=p1, rdx=p2, xmm2=rad) ---
    # grid 8x8 cell 4.0 eps .5 -> (1,1)-(3,3) r.5 covers cell(0,0)
    C["los-null"] = {"rootp": 0,
                     "steps": [(LQUERY, P1, P2, 0, 0, 0, f2u(0.5))]}
    C["los-empty"] = {"steps": [(LQUERY, P1, P2, 0, 0, 0,
                                 f2u(0.5))]}
    # type-0 wall rec (2,2) r.1 on the segment -> capt0 blocks
    C["los-t0-block"] = {"cflags": [1] + [0] * 0xFF,
                         "lsrc": {0: [0] * 0x10 + [1]},
                         "wrecs": [[0, 2.0, 2.0, 0.1]],
                         "steps": [(LQUERY, P1, P2, 0, 0, 0,
                                    f2u(0.5))],
                         "watch": W_BMSK}
    # type-0 wall rec far away -> capt0 miss -> exhaust -> 0
    C["los-t0-miss"] = {"cflags": [1] + [0] * 0xFF,
                        "lsrc": {0: [0] * 0x10 + [1]},
                        "wrecs": [[0, 20.0, 20.0, 0.1]],
                        "steps": [(LQUERY, P1, P2, 0, 0, 0,
                                   f2u(0.5))],
                        "watch": W_BMSK}
    # type-1 wall edge (2,2) e10=1 -> capt1 blocks
    C["los-t1-block"] = {"cflags": [1] + [0] * 0xFF,
                         "lsrc": {0: [0] * 0x10 + [1]},
                         "wrecs": [[1, 2.0, 2.0, 1.0, 4.0, 0.0]],
                         "steps": [(LQUERY, P1, P2, 0, 0, 0,
                                    f2u(0.5))],
                         "watch": W_BMSK}
    # type-5 record -> skipped -> 0
    C["los-tskip"] = {"cflags": [1] + [0] * 0xFF,
                      "lsrc": {0: [0] * 0x10 + [1]},
                      "wrecs": [[5, 2.0, 2.0, 0.1]],
                      "steps": [(LQUERY, P1, P2, 0, 0, 0,
                                 f2u(0.5))]}
    # bit 0x20 -> RDEC nav decode -> capt1 blocks
    C["los-nav"] = {"cflags": [1] + [0] * 0xFF,
                    "lsrc": {0: [0] * 0x14 + [1]},
                    "recs": [[0, 4096, 0, 8192]],
                    "vtxs": [[1.0, 0.0, 1.0, 0.0,
                              2.0, 0.5, 2.0, 0.0]],
                    "steps": [(LQUERY, P1, P2, 0, 0, 0,
                               f2u(0.5))],
                    "watch": W_RBP70}
    # bit0 miss + bit0x20 block -> iterates both decode paths
    C["los-multi"] = {"cflags": [1] + [0] * 0xFF,
                      "lsrc": {0: [0] * 0x10 + [1, 0, 0, 0, 1]},
                      "wrecs": [[0, 20.0, 20.0, 0.1]],
                      "recs": [[0, 4096, 0, 8192]],
                      "vtxs": [[1.0, 0.0, 1.0, 0.0,
                                2.0, 0.5, 2.0, 0.0]],
                      "steps": [(LQUERY, P1, P2, 0, 0, 0,
                                 f2u(0.5))],
                      "watch": W_RBP70}
    # nav edge far -> capt1 miss -> 0
    C["los-nav-miss"] = {"cflags": [1] + [0] * 0xFF,
                         "lsrc": {0: [0] * 0x14 + [1]},
                         "recs": [[0, 4096, 0, 8192]],
                         "vtxs": [[1.0, 0.0, 1.0, 0.0,
                                   20.0, 0.5, 20.0, 0.0]],
                         "steps": [(LQUERY, P1, P2, 0, 0, 0,
                                    f2u(0.5))],
                         "watch": W_RBP70}
    # off-grid segment -> clamps to whole grid; flag0 -> block
    C["los-clamp"] = {"p1x": -10.0, "p1z": -10.0,
                      "p2x": 30.0, "p2z": 30.0,
                      "cflags": [1] + [0] * 0xFF,
                      "lsrc": {0: [0] * 0x10 + [1]},
                      "wrecs": [[0, 2.0, 2.0, 0.1]],
                      "steps": [(LQUERY, P1, P2, 0, 0, 0,
                                 f2u(1.0))],
                      "watch": W_BMSK}
    # mask bit8 (rec8) -> column-wrap boundary coverage
    C["los-bit8"] = {"cflags": [1] + [0] * 0xFF,
                     "lsrc": {0: [0] * 0x11 + [1]},
                     "wrecs": [[0, 0.0, 0.0, 0.0]] * 8 +
                              [[0, 2.0, 2.0, 0.1]],
                     "steps": [(LQUERY, P1, P2, 0, 0, 0,
                                f2u(0.5))],
                     "watch": W_BMSK}
    # mask bit1 (rec1) -> shl bit position coverage
    C["los-bit1"] = {"cflags": [1] + [0] * 0xFF,
                     "lsrc": {0: [0] * 0x10 + [2]},
                     "wrecs": [[0, 0.0, 0.0, 0.0],
                               [0, 2.0, 2.0, 0.1]],
                     "steps": [(LQUERY, P1, P2, 0, 0, 0,
                                f2u(0.5))],
                     "watch": W_BMSK}
    # wide z-range: p2z=9 -> rows 0..2; flag row2 only
    C["los-zwide"] = {"p2z": 9.0,
                      "cflags": [0] * 16 + [1] + [0] * 0xEF,
                      "lsrc": {16: [0] * 0x10 + [1]},
                      "wrecs": [[0, 2.0, 2.0, 1.0]],
                      "steps": [(LQUERY, P1, P2, 0, 0, 0,
                                 f2u(0.5))],
                      "watch": W_BMSK}
    # flag at cell(2,0)=16: inside mutant-expanded zhi (mulss),
    # outside native zhi=0
    C["los-far3"] = {"cflags": [0] * 16 + [1] + [0] * 0xEF,
                     "lsrc": {16: [0] * 0x10 + [1]},
                     "wrecs": [[0, 2.0, 2.0, 0.1]],
                     "steps": [(LQUERY, P1, P2, 0, 0, 0,
                                f2u(0.5))],
                     "watch": W_BMSK}
    # null root + flag set: mutant je->jne proceeds into a wild
    # d[root+0x28] read
    C["los-null-f"] = {"rootp": 0,
                       "cflags": [1] + [0] * 0xFF,
                       "lsrc": {0: [0] * 0x10 + [1]},
                       "wrecs": [[0, 2.0, 2.0, 0.1]],
                       "steps": [(LQUERY, P1, P2, 0, 0, 0,
                                  f2u(0.5))]}
    # edge x beyond p2 -> closest=p2 (dx!=0); native lim < dist
    # but a mutant x7*=e14 inflates it (m-trg-div)
    C["capt1-divlim"] = {"segv": [0, 0, 0, 0, 4, 0, 0, 0, 1.0,
                                 0, 0, 0, 4.5, 0, 1.5, 0,
                                 1.0, 0.5, 0.0] + [0] * 0xE9,
                         "steps": [(CAPT1, SEG, EDG)]}
    # faults
    C["los-badp1"] = {"steps": [(LQUERY, 0xFFFFFFF0, P2, 0, 0,
                                 0, f2u(0.5))]}
    C["los-badroot"] = {"rootp": 0xFFFFFFF0,
                        "cflags": [1] + [0] * 0xFF,
                        "lsrc": {0: [0] * 0x10 + [1]},
                        "wrecs": [[0, 2.0, 2.0, 0.1]],
                        "steps": [(LQUERY, P1, P2, 0, 0, 0,
                                   f2u(0.5))]}
    C["los-badcflg"] = {"lcflg": 0xFFFFFFF0,
                        "steps": [(LQUERY, P1, P2, 0, 0, 0,
                                   f2u(0.5))]}
    C["los-badrec"] = {"root_0x28": 0xFFFF0000,
                       "cflags": [1] + [0] * 0xFF,
                       "lsrc": {0: [0] * 0x10 + [1]},
                       "steps": [(LQUERY, P1, P2, 0, 0, 0,
                                  f2u(0.5))]}
    C["los-badnroot"] = {"nroot": 0,
                         "cflags": [1] + [0] * 0xFF,
                         "lsrc": {0: [0] * 0x14 + [1]},
                         "steps": [(LQUERY, P1, P2, 0, 0, 0,
                                    f2u(0.5))]}
    C["los-badnav"] = {"recp": 0,
                       "cflags": [1] + [0] * 0xFF,
                       "lsrc": {0: [0] * 0x14 + [1]},
                       "steps": [(LQUERY, P1, P2, 0, 0, 0,
                                  f2u(0.5))]}
    # --- BMASK 003912E0 (ecx=c0 edx=r0 r8=c1 r9=r1) ---
    C["bmask-1"] = {"cflags": [1] + [0] * 0xFF,
                    "lsrc": {0: [0x27] + [0x55] * 0x2F},
                    "steps": [(BMASK, 0, 0, 0, 0)],
                    "watch": W_BMSK}
    C["bmask-range"] = {"cflags": [1] + [0] * 8 + [1] +
                        [0] * 7 + [1] + [0] * 0xEE,
                        "lsrc": {0: [1], 9: [2], 17: [4]},
                        "steps": [(BMASK, 0, 0, 1, 2)],
                        "watch": W_BMSK}
    C["bmask-clamp"] = {"cflags": [1] + [0] * 62 +
                        [1] + [0] * 0xC0,
                        "lsrc": {0: [1], 63: [8]},
                        "steps": [(BMASK, -3, -2, 99, 50)],
                        "watch": W_BMSK}
    C["bmask-invrow"] = {"cflags": [1] + [0] * 0xFF,
                         "lsrc": {0: [9]},
                         "steps": [(BMASK, 0, 2, 7, 0)],
                         "watch": W_BMSK}
    C["bmask-rlen4"] = {"lrlen": 4,
                        "cflags": [1] + [0] * 0xFF,
                        "lsrc": {0: [9, 0, 0, 0]},
                        "steps": [(BMASK, 0, 0, 0, 0)],
                        "watch": W_BMSK}
    C["bmask-flip"] = {"cflags": [0, 1] + [0] * 0xFE,
                       "lsrc": {0: [9], 1: [3]},
                       "steps": [(BMASK, 0, 0, 1, 0)],
                       "watch": W_BMSK}
    # c0=0x100000: native clamps to w-1=7 and reads flag7 -> OR;
    # cmovl mutant keeps 0x100000 > c1 -> col guard skips -> dst 0
    C["bmask-wild"] = {"cflags": [0] * 7 + [1] + [0] * 0xF8,
                       "lsrc": {7: [0] * 0x10 + [0xA5]},
                       "steps": [(BMASK, 0x100000, 0,
                                  0x100000, 0)],
                       "watch": W_BMSK}
    C["bmask-badcflg"] = {"lcflg": 0xFFFFFFF0,
                          "steps": [(BMASK, 0, 0, 0, 0)]}
    C["bmask-badlsrc"] = {"llsrc": 0xFFFFFFF0,
                          "cflags": [1] + [0] * 0xFF,
                          "steps": [(BMASK, 0, 0, 0, 0)]}
    # --- DIST 003A1920 (rcx=a, rdx=b) ---
    C["dist-1"] = {"steps": [(DIST, P1, P2)]}
    C["dist-badptr"] = {"steps": [(DIST, 0xFFFFFFF0, P2)]}
    # --- CPSEG 004691A0 (rcx=out rdx=a r8=b r9=p) ---
    # segv: p1v4,p2v4,srad,pad3, edgev4, e10/prad,e14,ang,pad
    C["cpseg-mid"] = {"segv": [0, 0, 0, 0, 10, 0, 0, 0,
                              0, 0, 0, 0, 5, 0, 2, 0] +
                              [0] * 0xF0,
                      "steps": [(CPSEG, OUTB, SEG, SEG + 0x10,
                                 EDG)],
                      "watch": [(OUTB, 0x10)]}
    C["cpseg-pre"] = {"segv": [0, 0, 0, 0, 10, 0, 0, 0,
                              0, 0, 0, 0, -3, 0, 0, 0] +
                              [0] * 0xF0,
                      "steps": [(CPSEG, OUTB, SEG, SEG + 0x10,
                                 EDG)],
                      "watch": [(OUTB, 0x10)]}
    C["cpseg-post"] = {"segv": [0, 0, 0, 0, 10, 0, 0, 0,
                               0, 0, 0, 0, 20, 0, 0, 0] +
                               [0] * 0xF0,
                       "steps": [(CPSEG, OUTB, SEG, SEG + 0x10,
                                  EDG)],
                       "watch": [(OUTB, 0x10)]}
    C["cpseg-degen"] = {"segv": [0, 0, 0, 0, 0, 0, 0, 0,
                                0, 0, 0, 0, 5, 0, 2, 0] +
                                [0] * 0xF0,
                        "steps": [(CPSEG, OUTB, SEG, SEG + 0x10,
                                   EDG)],
                        "watch": [(OUTB, 0x10)]}
    C["cpseg-nanp"] = {"segv": [0, 0, 0, 0, 10, 0, 0, 0,
                               0, 0, 0, 0, 5, float("nan"), 2,
                               0] + [0] * 0xF0,
                       "steps": [(CPSEG, OUTB, SEG, SEG + 0x10,
                                  EDG)],
                       "watch": [(OUTB, 0x10)]}
    C["cpseg-badout"] = {"segv": [0, 0, 0, 0, 10, 0, 0, 0,
                                 0, 0, 0, 0, 5, 0, 2, 0] +
                                 [0] * 0xF0,
                         "steps": [(CPSEG, 0xFFFFFFF0, SEG,
                                    SEG + 0x10, EDG)]}
    C["cpseg-badb"] = {"steps": [(CPSEG, OUTB, SEG,
                                 0xFFFFFFF0, EDG)]}
    # --- TRIGD 00468580 (rcx=edge, rdx=cpt) ---
    C["trigd-eps"] = {"segv": [2, 0, 2, 0] + [0] * 8 +
                      [2, 0, 2, 0, 1.0, 1.0, 0.0] + [0] * 0xE5,
                      "steps": [(TRIGD, EDG, SEG)]}
    C["trigd-1"] = {"segv": [2, 0, 3.5, 0] + [0] * 8 +
                    [2, 0, 2, 0, 1.0, 1.0, 0.0] + [0] * 0xE5,
                    "steps": [(TRIGD, EDG, SEG)]}
    C["trigd-nan"] = {"segv": [2, 0, 3.5, 0] + [0] * 8 +
                      [2, 0, 2, 0, 1.0, 1.0, float("nan")] +
                      [0] * 0xE5,
                      "steps": [(TRIGD, EDG, SEG)]}
    C["trigd-badptr"] = {"steps": [(TRIGD, 0xFFFFFFF0, SEG)]}
    # --- CAPT0 00468D50 (rcx=seg, rdx=edge) ---
    C["capt0-block"] = {"segv": [0, 0, 0, 0, 4, 0, 0, 0, 1.0,
                                0, 0, 0, 2, 0, 1.5, 0, 0.6] +
                                [0] * 0xEB,
                        "steps": [(CAPT0, SEG, EDG)]}
    C["capt0-miss"] = {"segv": [0, 0, 0, 0, 4, 0, 0, 0, 1.0,
                               0, 0, 0, 2, 0, 3.0, 0, 0.6] +
                               [0] * 0xEB,
                       "steps": [(CAPT0, SEG, EDG)]}
    C["capt0-degen"] = {"segv": [0, 0, 0, 0, 0, 0, 0, 0, 1.0,
                                0, 0, 0, 0, 0, 0.5, 0, 0.6] +
                                [0] * 0xEB,
                        "steps": [(CAPT0, SEG, EDG)]}
    C["capt0-p1eq"] = {"segv": [0, 0, 0, 0, 4, 0, 0, 0, 1.0,
                               0, 0, 0, -1, 0, 0, 0, 0.6] +
                               [0] * 0xEB,
                       "steps": [(CAPT0, SEG, EDG)]}
    C["capt0-nan"] = {"segv": [0, 0, 0, 0, 4, 0, 0, 0, 1.0,
                              0, 0, 0, 2, 0, 1.5, 0,
                              float("nan")] + [0] * 0xEB,
                      "steps": [(CAPT0, SEG, EDG)]}
    C["capt0-badedge"] = {"segv": [0, 0, 0, 0, 4, 0, 0, 0,
                                   1.0] + [0] * 0xF3,
                          "steps": [(CAPT0, SEG,
                                     0xFFFFFFF0)]}
    # --- CAPT1 00468E50 (rcx=seg, rdx=edge) ---
    C["capt1-block"] = {"segv": [0, 0, 0, 0, 4, 0, 0, 0, 1.0,
                                0, 0, 0, 2, 0, 1.5, 0,
                                1.0, 1.0, 0.0] + [0] * 0xE9,
                        "steps": [(CAPT1, SEG, EDG)]}
    C["capt1-miss"] = {"segv": [0, 0, 0, 0, 4, 0, 0, 0, 1.0,
                               0, 0, 0, 2, 0, 5.0, 0,
                               1.0, 1.0, 0.0] + [0] * 0xE9,
                       "steps": [(CAPT1, SEG, EDG)]}
    # edge pt on the segment -> closest==edge -> TRIGD eps path
    C["capt1-eps"] = {"segv": [0, 0, 0, 0, 4, 0, 0, 0, 0.5,
                              0, 0, 0, 2, 0, 0, 0,
                              0.01, 1.0, 0.0] + [0] * 0xE9,
                      "steps": [(CAPT1, SEG, EDG)]}
    C["capt1-degen"] = {"segv": [0, 0, 0, 0, 0, 0, 0, 0, 1.0,
                                0, 0, 0, 0, 0, 0.5, 0,
                                1.0, 1.0, 0.0] + [0] * 0xE9,
                        "steps": [(CAPT1, SEG, EDG)]}
    C["capt1-p1eq"] = {"segv": [0, 0, 0, 0, 4, 0, 0, 0, 1.0,
                               0, 0, 0, -1, 0, 0, 0,
                               1.0, 1.0, 0.0] + [0] * 0xE9,
                       "steps": [(CAPT1, SEG, EDG)]}
    C["capt1-badedge"] = {"segv": [0, 0, 0, 0, 4, 0, 0, 0,
                                   1.0] + [0] * 0xF3,
                          "steps": [(CAPT1, SEG,
                                     0xFFFFFFF0)]}
    # --- CAPV 00469410 (rcx=a rdx=b r9=p xmm2=rad) ---
    C["capv-block"] = {"segv": [0, 0, 0, 0, 4, 0, 0, 0, 0,
                               0, 0, 0, 2, 0, 1.0, 0, 0.6] +
                               [0] * 0xEB,
                       "steps": [(CAPV, SEG, SEG + 0x10, 0,
                                  EDG, 0, f2u(1.0))]}
    C["capv-miss"] = {"segv": [0, 0, 0, 0, 4, 0, 0, 0, 0,
                              0, 0, 0, 2, 0, 3.0, 0, 0.6] +
                              [0] * 0xEB,
                      "steps": [(CAPV, SEG, SEG + 0x10, 0,
                                 EDG, 0, f2u(1.0))]}
    C["capv-pre"] = {"segv": [0, 0, 0, 0, 4, 0, 0, 0, 0,
                             0, 0, 0, -1, 0, 0, 0, 0.6] +
                             [0] * 0xEB,
                     "steps": [(CAPV, SEG, SEG + 0x10, 0,
                                EDG, 0, f2u(1.0))]}
    # t<0 with small lim: native early-d2 > lim^2 -> 0; a lerp
    # would land closest on p -> used by m-capv-t0
    C["capv-pre2"] = {"segv": [0, 0, 0, 0, 4, 0, 0, 0, 0,
                              0, 0, 0, -1, 0, 1.0, 0, 0.1] +
                              [0] * 0xEB,
                      "steps": [(CAPV, SEG, SEG + 0x10, 0,
                                 EDG, 0, f2u(1.0))]}
    C["capv-post"] = {"segv": [0, 0, 0, 0, 4, 0, 0, 0, 0,
                              0, 0, 0, 10, 0, 0, 0, 0.6] +
                              [0] * 0xEB,
                      "steps": [(CAPV, SEG, SEG + 0x10, 0,
                                 EDG, 0, f2u(1.0))]}
    C["capv-nan"] = {"segv": [0, 0, 0, 0, 4, 0, 0, 0, 0,
                             0, 0, 0, float("nan"), 0, 1.0,
                             0, 0.6] + [0] * 0xEB,
                     "steps": [(CAPV, SEG, SEG + 0x10, 0,
                                EDG, 0, f2u(1.0))]}
    C["capv-badp"] = {"steps": [(CAPV, SEG, SEG + 0x10, 0,
                                0xFFFFFFF0, 0, f2u(1.0))]}
    # --- RDEC 0032A6E0 (ecx=idx, rdx=out) ---
    C["rdec-1"] = {"recs": [[0, 0, 0, 0], [1, 4096, -2048,
                                          8192]],
                   "vtxs": [[1.0, 0.0, 1.0, 0.0,
                             2.0, 0.5, 2.0, 0.0],
                            [3.0, 0.0, 4.0, 0.0,
                             5.0, 1.5, 6.0, 0.0]],
                   "steps": [(RDEC, 1, OUTB2)],
                   "watch": [(OUTB2, 0x18)]}
    C["rdec-neg"] = {"steps": [(RDEC,
                               (-0x2000) & 0xFFFFFFFFFFFFFFFF,
                               OUTB2)]}
    C["rdec-noroot"] = {"nroot": 0,
                        "steps": [(RDEC, 1, OUTB2)]}
    C["rdec-badvtx"] = {"recs": [[0x4000, 0, 0, 0]],
                        "steps": [(RDEC, 0, OUTB2)]}

    # ---------------- EXP-134: 00335B60 path validator ----------------
    # step tuple: (PVAL, rcx=sub, rdx, r8, r9, xmm0, xmm2=angB,
    #              xmm1=angA, xmm3=tol); cap @stk+0x28, pvflags @+0x30
    PV = STACK + 0x80000
    W_PV = [(PV - 0xE8, 0x10), (PV - 0xD8, 0x10),
            (PV - 0xC8, 0x10), (PV - 0xB8, 0x10),
            (PV - 0xA8, 0x40)]
    # --- ROTX 00217790 standalone (rcx=mat xmm1=sin xmm2=cos) ---
    C["rotx-gen"] = {"m1": 0.5, "m2": 0.75, "m4": 2.0, "m8": 3.0,
                     "steps": [(ROTX, MATB, 0, 0, 0, 0,
                                f2u(0.8), f2u(0.6))],
                     "watch": [(MATB, 0x40)]}
    C["rotx-90"] = {"m4": 2.0, "m8": 3.0, "m20": 5.0, "m24": 7.0,
                    "steps": [(ROTX, MATB, 0, 0, 0, 0,
                               f2u(0.0), f2u(1.0))],
                    "watch": [(MATB, 0x40)]}
    C["rotx-neg"] = {"m4": 2.0, "m8": 3.0,
                     "steps": [(ROTX, MATB, 0, 0, 0, 0,
                                f2u(0.0), f2u(-1.0))],
                     "watch": [(MATB, 0x40)]}
    C["rotx-nan"] = {"m4": 2.0, "m8": 3.0,
                     "steps": [(ROTX, MATB, 0, 0, 0, 0,
                                f2u(0.5), f2u(float("nan")))],
                     "watch": [(MATB, 0x40)]}
    # --- MCPY 00202E90 (rcx=dst rdx=src xmm2=angle) ---
    C["mcpy-gen"] = {"steps": [(MCPY, DVB, MATB, 0, 0, 0,
                              f2u(0.9))],
                     "watch": [(DVB, 0x40)]}
    C["mcpy-inplace"] = {"m4": 2.0, "m8": 3.0,
                         "steps": [(MCPY, MATB, MATB, 0, 0, 0,
                                    f2u(0.9))],
                         "watch": [(MATB, 0x40)]}
    C["mcpy-badsrc"] = {"steps": [(MCPY, DVB, 0xFFFFFFF0, 0, 0,
                                  0, f2u(0.9))]}
    C["mcpy-baddst"] = {"steps": [(MCPY, 0xFFFFFFF0, MATB, 0, 0,
                                  0, f2u(0.9))]}
    # --- DE6A0 0032A6A0 -> DE100 scripted ---
    C["de6a0-0"] = {"derets": [0],
                    "steps": [(DE6A0, 0x1234, 0x5678, 0x9A)]}
    C["de6a0-1"] = {"derets": [5],
                    "steps": [(DE6A0, 0x1234, 0x5678, 0x9A)]}
    # --- PVAL guards ---
    C["pv-tol0"] = {"steps": [(PVAL, AGENT, 0, 0, 0, 0,
                              f2u(0.0), f2u(0.0), f2u(0.0))]}
    C["pv-angb0"] = {**gfix(), "derets": [1],
                     "rad2": 0.5, "tol": 0,
                     "steps": [(PVAL, AGENT, 0, 0, 0, 0,
                                f2u(0.0), f2u(0.0), f2u(1.0))],
                     "watch": W_PV}
    # --- PVAL clear pass: dir=+z, tol=1 -> v40=(1,0,2) same tri ---
    C["pv-clear"] = {**gfix(), "derets": [1], "rad2": 0.5,
                     "steps": [(PVAL, AGENT, 0, 0, 0, 0,
                                f2u(0.0), f2u(0.0), f2u(1.0))],
                     "watch": W_PV}
    # --- gate result routing (real tree: CANDA through
    # collector+filter+walk; opb=4 -> hard -> gate 1, opb=2 -> 2) ---
    C["pv-gate1"] = {**gpop(crec=(1.0, 0.0, 2.0)), "rad2": 0.5,
                     "steps": [(PVAL, AGENT, 0, 0, 0, 0,
                                f2u(0.0), f2u(0.0), f2u(1.0))]}
    C["pv-gate2"] = {**gpop(opbrets=[2], crec=(1.0, 0.0, 2.0)),
                     "derets": [1],
                     "rad2": 0.5,
                     "steps": [(PVAL, AGENT, 0, 0, 0, 0,
                                f2u(0.0), f2u(0.0), f2u(1.0))]}
    C["pv-gate2-de0"] = {**gpop(opbrets=[2], crec=(1.0, 0.0, 2.0)),
                         "derets": [0],
                         "rad2": 0.5,
                         "steps": [(PVAL, AGENT, 0, 0, 0, 0,
                                    f2u(0.0), f2u(0.0),
                                    f2u(1.0))]}
    C["pv-gate0-de0"] = {**gfix(), "derets": [0],
                         "rad2": 0.5,
                         "steps": [(PVAL, AGENT, 0, 0, 0, 0,
                                    f2u(0.0), f2u(0.0),
                                    f2u(1.0))]}
    # --- mode-3 AGENTQ arm ---
    C["pv-mode3-agq"] = {**gfix(), "mode": 3, "agrets": [1],
                         "rad2": 0.5,
                         "steps": [(PVAL, AGENT, 0, 0, 0, 0,
                                    f2u(0.0), f2u(0.0),
                                    f2u(1.0))]}
    C["pv-mode3-clear"] = {**gfix(), "mode": 3,
                           "agrets": [0], "derets": [1],
                           "rad2": 0.5,
                           "steps": [(PVAL, AGENT, 0, 0, 0, 0,
                                      f2u(0.0), f2u(0.0),
                                      f2u(1.0))]}
    # --- flag-8 QWALK arm vs PRED arm ---
    C["pv-qwalk-block"] = {**gfix(), "pvflags": 8,
                           "rad2": 0.5,
                           "steps": [(PVAL, AGENT, 0, 0, 0, 0,
                                      f2u(0.0), f2u(0.0),
                                      f2u(6.0))]}
    C["pv-qwalk-clear"] = {**gfix(), "pvflags": 8,
                           "derets": [1], "rad2": 0.5,
                           "steps": [(PVAL, AGENT, 0, 0, 0, 0,
                                      f2u(0.0), f2u(0.0),
                                      f2u(1.0))],
                           "watch": W_PV}
    C["pv-pred-block"] = {**gfix(), "radius": 4.0,
                          "rad2": 0.5,
                          "steps": [(PVAL, AGENT, 0, 0, 0, 0,
                                     f2u(0.0), f2u(0.0),
                                     f2u(1.0))]}
    # sc=rad*0.9=0.9 probes pass; a rad+0.9=1.9 mutant probe fails
    C["pv-pred-rad1"] = {**gfix(), "derets": [1],
                         "radius": 1.0, "rad2": 0.5,
                         "steps": [(PVAL, AGENT, 0, 0, 0, 0,
                                    f2u(0.0), f2u(0.0),
                                    f2u(1.0))]}
    # --- LQUERY arm: wall rec blocks seg (1,1)->(1,3) rad 1.0 ---
    C["pv-los-block"] = {**gfix(), "derets": [1], "rad2": 2.0,
                         "cflags": [1] + [0] * 7 + [1] + [0] * 0xF7,
                         "lsrc": {0: [0] * 0x10 + [1],
                                  8: [0] * 0x10 + [1]},
                         "wrecs": [[0, 1.5, 2.0, 0.1]],
                         "steps": [(PVAL, AGENT, 0, 0, 0, 0,
                                    f2u(0.0), f2u(0.0),
                                    f2u(1.0))],
                         "watch": W_PV}
    # --- transforms / clamps ---
    C["pv-angb60"] = {**gfix(), "derets": [1], "rad2": 0.5,
                      "steps": [(PVAL, AGENT, 0, 0, 0, 0,
                                 f2u(math.pi / 3), f2u(0.0),
                                 f2u(1.0))],
                      "watch": W_PV}
    C["pv-angb-nan"] = {**gfix(), "derets": [1], "rad2": 0.5,
                        "steps": [(PVAL, AGENT, 0, 0, 0, 0,
                                   f2u(float("nan")), f2u(0.0),
                                   f2u(1.0))],
                        "watch": W_PV}
    C["pv-anga90"] = {**gfix(), "derets": [1], "rad2": 0.5,
                      "steps": [(PVAL, AGENT, 0, 0, 0, 0,
                                 f2u(0.0), f2u(math.pi / 2),
                                 f2u(1.0))],
                      "watch": W_PV}
    C["pv-anga-3pi"] = {**gfix(), "derets": [1], "rad2": 0.5,
                        "steps": [(PVAL, AGENT, 0, 0, 0, 0,
                                   f2u(0.0), f2u(3 * math.pi),
                                   f2u(1.0))],
                        "watch": W_PV}
    C["pv-caplo"] = {**gfix(), "derets": [1], "rad2": 0.5,
                     "cap": 0.1,
                     "steps": [(PVAL, AGENT, 0, 0, 0, 0,
                                f2u(0.0), f2u(0.0), f2u(1.0))],
                     "watch": W_PV}
    C["pv-caphi"] = {**gfix(), "derets": [1], "rad2": 0.5,
                     "cap": 5.0,
                     "steps": [(PVAL, AGENT, 0, 0, 0, 0,
                                f2u(0.0), f2u(0.0), f2u(1.0))],
                     "watch": W_PV}
    C["pv-capnan"] = {**gfix(), "derets": [1], "rad2": 0.5,
                      "cap": float("nan"),
                      "steps": [(PVAL, AGENT, 0, 0, 0, 0,
                                 f2u(0.0), f2u(0.0), f2u(1.0))],
                      "watch": W_PV}
    # --- gate flag math ---
    # pvflags=6 -> gf=0x52; bad self fails GCHK -> gate 0.
    # shl2 mutant (gf=0xA2) sets &0x20 -> GCHK skipped -> walk
    # -> &2 arm -> esi -> gate 2.
    C["pv-flag6"] = {**gpop(
            gchkpl(SELFO, GC0A, GC138A, qB8=SELF_B8, b4=9),
            crec=(1.0, 0.0, 2.0)),
                     "derets": [1], "rad2": 0.5,
                     "pvflags": 6,
                     "steps": [(PVAL, AGENT, 0, 0, 0, 0,
                                f2u(0.0), f2u(0.0), f2u(1.0))]}
    # pvflags=0xC -> gf=0x50: &0x10 arm -> O1F3==0 -> esi -> 2.
    # and4 mutant (gf=0x60) clears all flag arms -> accept -> 1.
    C["pv-flag12"] = {**gpop(crec=(1.0, 0.0, 2.0)),
                      "derets": [1], "rad2": 0.5,
                      "pvflags": 0xC,
                      "steps": [(PVAL, AGENT, 0, 0, 0, 0,
                                 f2u(0.0), f2u(0.0), f2u(1.0))]}
    C["pv-mode7"] = {**gfix(), "derets": [1], "rad2": 0.5,
                     "mode": 7,
                     "steps": [(PVAL, AGENT, 0, 0, 0, 0,
                                f2u(0.0), f2u(0.0), f2u(1.0))]}
    # flags=8 native takes QWALK arm (passes, tol=1 same-tri);
    # a flags&0x10 mutant takes PRED arm -> radius=4 probes fail
    C["pv-flag8-rad4"] = {**gfix(), "derets": [1], "rad2": 0.5,
                          "pvflags": 8, "radius": 4.0,
                          "steps": [(PVAL, AGENT, 0, 0, 0, 0,
                                     f2u(0.0), f2u(0.0),
                                     f2u(1.0))]}
    # gate r9/g0 args: r9=ag+0xF0=CTXA ctx(ea9=0), g0=ag+0xE0=
    # CTXB (the collected handle -> excluded). r9f0 mutant reads
    # +0xE0 -> CTXB(ea9=2) -> mabe ecx differs; raxe0 mutant makes
    # g0=CTXA -> CTXB handle no longer excluded -> walk runs.
    C["pv-gateptr"] = {**gpop(
            [(CTXB, ob(0x1000, qC0=GC0A + 0x200, b8=8, b4=3,
                       b3=0x60, q30=CTXB, qB8=GC0A + 0x400,
                       q698=G698A + 0x40, bEA9=2)),
             (GC0A + 0x200, ob(0x200, q138=GC138A + 0x200)),
             (GC138A + 0x200, ob(0x100, fF0=1.0)),
             (GC0A + 0x400, ob(0x200, qF0=GC0A + 0x600,
                               d0=f2u(1.0), d4=f2u(0.0),
                               d8=f2u(2.0))),
             (GC0A + 0x600, ob(0x100))],
            ge0=CTXB, ghnd=[CTXB], gtab=[0x42, 0, 0x99],
            opbrets=[4]),
        "derets": [1], "rad2": 0.5,
        "steps": [(PVAL, AGENT, 0, 0, 0, 0,
                   f2u(0.0), f2u(0.0), f2u(1.0))]}
    # negative angB: native xorps flips to +pi/3; an orps mutant
    # keeps -pi/3 -> different rotation
    C["pv-angb-neg"] = {**gfix(), "derets": [1], "rad2": 0.5,
                        "steps": [(PVAL, AGENT, 0, 0, 0, 0,
                                   f2u(-math.pi / 3), f2u(0.0),
                                   f2u(1.0))],
                        "watch": W_PV}
    # --- flag-bit discriminators (populated gate) ---
    # pvflags=6 -> gf=0x52: flags&2 fires LHELP(obj)==0 ->
    # esi++ ret 2; and2 mutant (gf=0x50) falls to flags&0x10
    # -> O1F3 nonzero -> candidate skipped -> ret 0.
    C["pv-flag6-pop"] = {**gpop([(CTX_F0, ob(0x100, f24=1.0))],
                                crec=(1.0, 0.0, 2.0)),
                         "pvflags": 6, "derets": [1],
                         "rad2": 0.5,
                         "steps": [(PVAL, AGENT, 0, 0, 0, 0,
                                    f2u(0.0), f2u(0.0),
                                    f2u(1.0))]}
    # pvflags=6 -> gf=0x52: flags&0x40 mode-3 pre-filter block
    # fires (O3FW+OSUB on cand sub); or10 mutant (gf=0x92)
    # skips the block entirely.
    C["pv-flag6-m3"] = {**gpop(
            [(CANDA + 0x1F4, bb(3)),
             (CTX_B8, ob(0x200, qF0=CTX_F0, d0=f2u(9.0),
                         d4=f2u(0.5), d8=f2u(9.0)))],
            ctx_sub=OSUBA, crec=(1.0, 0.0, 2.0)),
        "pvflags": 6, "derets": [1], "rad2": 0.5,
        "steps": [(PVAL, AGENT, 0, 0, 0, 0,
                   f2u(0.0), f2u(0.0), f2u(1.0))]}
    # --- fault paths ---
    C["pv-badsub"] = {**gfix(), "rad2": 0.5,
                      "steps": [(PVAL, 0xFFFFFFF0, 0, 0, 0, 0,
                                 f2u(0.0), f2u(0.0), f2u(1.0))]}
    C["pv-badsubp"] = {**gfix(), "subp": 0xFFFFFFF0,
                       "rad2": 0.5,
                       "steps": [(PVAL, AGENT, 0, 0, 0, 0,
                                  f2u(0.0), f2u(0.0), f2u(1.0))]}
    C["pv-badsubp2"] = {**gfix(), "subp": HEAP + 0xFFF00,
                        "rad2": 0.5,
                        "steps": [(PVAL, AGENT, 0, 0, 0, 0,
                                   f2u(0.0), f2u(0.0), f2u(1.0))]}

    # ================= EXP-135 direct cases =================
    # GATE 003357B0: rcx=posA rdx=posB r8=unused r9=ctx xmm2=rad;
    # stack: [entry+0x28]=excl handle, [entry+0x30]=flags dword.
    # Default seg P1(1,0,1)->P2(3,0,3): on-seg tmp = (2,0,2).
    # point query (posA==posB), empty collector -> 0
    C["gate-pt0"] = {**gfix(), "gflags": 0x40,
                     "steps": [(GATE, P1, P1, CTXA, CTXA,
                                0, f2u(0.5))]}
    # segment query, empty collector -> 0
    C["gate-seg0"] = {**gfix(), "gflags": 0x40,
                      "steps": [(GATE, P1, P2, CTXA, CTXA,
                                 0, f2u(0.5))]}
    # one candidate through the full walk -> hard count -> 1
    C["gate-acc1"] = {**gpop(), "gflags": 0x40,
                      "steps": [(GATE, P1, P2, CTXA, CTXA,
                                 0, f2u(0.5))]}
    # opb=2 -> ordinary count -> 2
    C["gate-acc2"] = {**gpop(opbrets=[2]),
                      "gflags": 0x40,
                      "steps": [(GATE, P1, P2, CTXA, CTXA,
                                 0, f2u(0.5))]}
    # opa=0 (c138 b6 mismatch) -> candidate skipped -> 0
    C["gate-opa0"] = {**gpop(
            [(GC138A + 0x800, ob(0x100, fF0=1.0, b6=1))]),
                      "gflags": 0x40,
                      "steps": [(GATE, P1, P2, CTXA, CTXA,
                                 0, f2u(0.5))]}
    # handle == self -> skipped -> 0
    C["gate-selfskip"] = {**gpop(ghnd=[SELFO]),
                          "gflags": 0x40,
                          "steps": [(GATE, P1, P2, CTXA, CTXA,
                                     0, f2u(0.5))]}
    # handle == exclusion arg -> skipped -> 0
    C["gate-excl"] = {**gpop(), "garg5": CANDA,
                      "gflags": 0x40,
                      "steps": [(GATE, P1, P2, CTXA, CTXA,
                                 0, f2u(0.5))]}
    # gate-loop objd -> 0 (q30=0) -> accept path -> opa -> 1
    C["gate-nullobj"] = {**gpop([(CANDA + 0x30, qw(0))]),
                         "gflags": 0x40,
                         "steps": [(GATE, P1, P2, CTXA, CTXA,
                                    0, f2u(0.5))]}
    # GCHK(self) fails (b4 != 3), flags&0x20 clear -> gate 0
    C["gate-gchkfail"] = {**gfix(
            gchkpl(SELFO, GC0A, GC138A, qB8=SELF_B8, b4=9)),
        "gflags": 0x40,
        "steps": [(GATE, P1, P2, CTXA, CTXA, 0, f2u(0.5))]}
    # flags&0x20 skips GCHK -> invalid self still walks -> 1
    C["gate-f20skip"] = {**gpop(
            gchkpl(SELFO, GC0A, GC138A, qB8=SELF_B8, b4=9)),
        "gflags": 0x60,
        "steps": [(GATE, P1, P2, CTXA, CTXA, 0, f2u(0.5))]}
    # mabef clear -> MABE -> 0 -> self=0 -> GCHK(0)=0 -> gate 0
    C["gate-mabe0"] = {**gpop(), "mabef": 0,
                       "gflags": 0x40,
                       "steps": [(GATE, P1, P2, CTXA, CTXA,
                                  0, f2u(0.5))]}
    # e68 class filter: obj cls1 vs ctx cls4 -> skip -> 0
    C["gate-e68skip"] = {**gpop(
            [(CANDA + 0xE68, qw(E68A)),
             (E68A, ob(b18=0x02)),
             (E68A + 0x40, ob(b18=0x08))],
            ctx_e68=E68A + 0x40),
        "gflags": 0x40,
        "steps": [(GATE, P1, P2, CTXA, CTXA, 0, f2u(0.5))]}
    # flags&0x40 + ctx mode!=3 + obj mode==3 -> O3FW/O1F2 block;
    # f34-c1 <= o1f2 -> proceed -> accept -> 1
    C["gate-mode3blk"] = {**gpop(
            [(CANDA + 0x1F4, bb(3)),
             (CTX_B8, ob(0x200, qF0=CTX_F0, d0=f2u(9.0),
                         d4=f2u(0.5), d8=f2u(9.0)))],
            ctx_sub=OSUBA),
        "gflags": 0x40,
        "steps": [(GATE, P1, P2, CTXA, CTXA, 0, f2u(0.5))]}
    # mode-3 block with f34-c1 > o1f2 -> skip -> 0
    C["gate-mode3skip"] = {**gpop(
            [(CANDA + 0x1F4, bb(3)),
             (CTX_B8, ob(0x200, qF0=CTX_F0, d0=f2u(9.0),
                         d4=f2u(0.5), d8=f2u(9.0), fC0=-2.0,
                         f24=1.0))],
            ctx_sub=OSUBA),
        "gflags": 0x40,
        "steps": [(GATE, P1, P2, CTXA, CTXA, 0, f2u(0.5))]}
    # ctx mode==3 -> accept-path f74 compare: posA.y <= x+f74 -> opa
    C["gate-acc3"] = {**gpop(
            [(QB8A, ob(0x200, qF0=QB8A + 0x200, d0=f2u(2.0),
                       d4=f2u(0.0), d8=f2u(2.0), fC0=1.0,
                       f24=1.0))],
            ctx_mode=3),
        "gflags": 0x40,
        "steps": [(GATE, P1, P2, CTXA, CTXA, 0, f2u(0.5))]}
    # ctx mode==3 + posA.y > x+f74 -> candidate skipped -> 0
    C["gate-acc3skip"] = {**gpop(
            [(QB8A, ob(0x200, qF0=QB8A + 0x200, d0=f2u(2.0),
                       d4=f2u(0.0), d8=f2u(2.0), fC0=-2.0,
                       f24=1.0))],
            ctx_mode=3),
        "gflags": 0x40,
        "steps": [(GATE, P1, P2, CTXA, CTXA, 0, f2u(0.5))]}
    # v1 candidate: o1f2 reads f68 (not fC0*f24) -> accept;
    # f68->f6C mutant gives -1 -> skip.
    C["gate-acc3v1"] = {**gpop(
            [(CANDA + 3, bb(0x20)),
             (QB8A, ob(0x200, qF0=QB8A + 0x200, d0=f2u(2.0),
                       d4=f2u(0.0), d8=f2u(2.0), f68=1.0,
                       f6C=-1.0))],
            ctx_mode=3),
        "gflags": 0x40,
        "steps": [(GATE, P1, P2, CTXA, CTXA, 0, f2u(0.5))]}
    # x = fC0*f24 = -6 -> skip; mul->add mutant gives +1 -> accept.
    C["gate-acc3m"] = {**gpop(
            [(QB8A, ob(0x200, qF0=QB8A + 0x200, d0=f2u(2.0),
                       d4=f2u(0.0), d8=f2u(2.0), fC0=-2.0,
                       f24=3.0))],
            ctx_mode=3),
        "gflags": 0x40,
        "steps": [(GATE, P1, P2, CTXA, CTXA, 0, f2u(0.5))]}
    # flags&2 + LHELP(obj)==0 -> ordinary accept -> 2
    C["gate-f2"] = {**gpop(), "gflags": 0x42,
                    "steps": [(GATE, P1, P2, CTXA, CTXA,
                               0, f2u(0.5))]}
    # flags&4 + LHELP(ctx)==0 + LHELP(obj)==0 -> ordinary -> 2
    C["gate-f4"] = {**gpop(), "gflags": 0x44,
                    "steps": [(GATE, P1, P2, CTXA, CTXA,
                               0, f2u(0.5))]}
    # flags&4 + LHELP(ctx)!=0 -> falls through -> accept -> 1
    C["gate-f4fall"] = {**gpop(
            [(G698A + 0x40, ob(b5=1)), (OSUBA, ob(bE=1))],
            ctx_i698=G698A + 0x40, ctx_sub=OSUBA),
        "gflags": 0x44,
        "steps": [(GATE, P1, P2, CTXA, CTXA, 0, f2u(0.5))]}
    # flags&8 + LHELP match + w714==0x4021 -> accept -> 1
    C["gate-f8"] = {**gpop(
            [(CANDA + 0x714, ww(0x4021))],
            ctx_i698=G698A),
        "gflags": 0x48,
        "steps": [(GATE, P1, P2, CTXA, CTXA, 0, f2u(0.5))]}
    # flags&8 + LHELP mismatch -> skip -> 0
    C["gate-f8lmm"] = {**gpop(
            [(G698A + 0x40, ob(b5=1)), (OSUBA, ob(bE=1))],
            ctx_i698=G698A + 0x40, ctx_sub=OSUBA),
        "gflags": 0x48,
        "steps": [(GATE, P1, P2, CTXA, CTXA, 0, f2u(0.5))]}
    # flags&8 + match + w714!=0x4021 -> skip -> 0
    C["gate-f8badw"] = {**gpop(),
            "ctx_i698": G698A, "gflags": 0x48,
            "steps": [(GATE, P1, P2, CTXA, CTXA, 0, f2u(0.5))]}
    # flags&0x10 + LHELP(obj)==0 + O1F3==0 -> ordinary -> 2
    C["gate-f10"] = {**gpop(), "gflags": 0x50,
                     "steps": [(GATE, P1, P2, CTXA, CTXA,
                                0, f2u(0.5))]}
    # flags&0x10 + O1F3!=0 -> skip -> 0
    C["gate-f10skip"] = {**gpop([(CTX_F0, ob(0x100, f24=1.0))]),
                         "gflags": 0x50,
                         "steps": [(GATE, P1, P2, CTXA, CTXA,
                                    0, f2u(0.5))]}
    # bad ctx -> fault at first r9 deref (0x3357E8)
    C["gate-badctx"] = {**gfix(), "gflags": 0x40,
                        "steps": [(GATE, P1, P2, CTXA,
                                   0xFFFFFFF0, 0, f2u(0.5))]}
    # gtab idx out of range -> pool ptr 0 -> d[0+8] fault 0x3357FE
    C["gate-badgtab"] = {**gfix(), "ctx_ea9": 9, "gtcnt": 4,
                         "gflags": 0x40,
                         "steps": [(GATE, P1, P2, CTXA, CTXA,
                                    0, f2u(0.5))]}
    # --- GTAB 00236820 (ecx=idx) ---
    C["gtab-0"] = {"gtab": [0x11, 0x22],
                   "steps": [(GTAB, 0)]}
    C["gtab-1"] = {"gtab": [0x11, 0x22],
                   "steps": [(GTAB, 1)]}
    C["gtab-oob"] = {"gtab": [0x11], "gtcnt": 1,
                     "steps": [(GTAB, 4)]}
    C["gtab-neg"] = {"steps": [(GTAB, (-1) & 0xFFFFFFFFFFFFFFFF)]}
    # --- MABE 0031ABE0 (rcx=val) ---
    C["mabe-fast"] = {"mabef": 0x10, "msparr": {0x42: SELFO},
                      "gplants": [(SELFO, ob())],
                      "steps": [(MABE, 0x42)]}
    C["mabe-off"] = {"mabef": 0, "msparr": {0x42: SELFO},
                     "gplants": [(SELFO, ob())],
                     "steps": [(MABE, 0x42)]}
    # --- GCHK 002EA7F0 (rcx=obj) ---
    C["gchk-ok"] = {"gplants": gchkpl(SELFO, GC0A, GC138A),
                    "steps": [(GCHK, SELFO)]}
    C["gchk-null"] = {"steps": [(GCHK, 0)]}
    C["gchk-b18"] = {"gplants": [(SELFO, ob(b18=1))],
                     "steps": [(GCHK, SELFO)]}
    C["gchk-c0null"] = {"gplants": [(SELFO, ob(b18=0))],
                        "steps": [(GCHK, SELFO)]}
    C["gchk-f14f"] = {"gplants": [(SELFO, ob(qC0=GC0A)),
                                  (GC0A, ob(b14F=1))],
                      "steps": [(GCHK, SELFO)]}
    C["gchk-138null"] = {"gplants": [(SELFO, ob(qC0=GC0A))],
                         "steps": [(GCHK, SELFO)]}
    C["gchk-f0neg"] = {"gplants": [(SELFO, ob(qC0=GC0A)),
                                   (GC0A, ob(q138=GC138A)),
                                   (GC138A, ob(fF0=-1.0))],
                       "steps": [(GCHK, SELFO)]}
    C["gchk-b8"] = {"gplants": [(SELFO, ob(qC0=GC0A, b8=0)),
                                (GC0A, ob(q138=GC138A)),
                                (GC138A, ob(fF0=1.0))],
                    "steps": [(GCHK, SELFO)]}
    # b3=0 -> OVF variant!=0x60 -> ret 1 -> accept via OVF arm
    C["gchk-ovf1"] = {"gplants": [(SELFO, ob(qC0=GC0A, b8=8)),
                                  (GC0A, ob(q138=GC138A)),
                                  (GC138A, ob(fF0=1.0))],
                      "steps": [(GCHK, SELFO)]}
    # b3=0x60 -> OVF real arm -> c0 flags ret 0 -> b4==9 -> 0
    C["gchk-b4"] = {"gplants": [(SELFO, ob(qC0=GC0A, b8=8,
                                           b3=0x60, b4=9)),
                                (GC0A, ob(q138=GC138A)),
                                (GC138A, ob(fF0=1.0))],
                    "steps": [(GCHK, SELFO)]}
    # --- OCLS 00263C20 / LHELP 00335760 (rcx=obj) ---
    C["ocls-null"] = {"steps": [(OCLS, 0)]}
    C["ocls-cls"] = {"gplants": [(SELFO, ob(bE=0x2B))],
                     "steps": [(OCLS, SELFO)]}
    C["lhelp-null"] = {"steps": [(LHELP, 0)]}
    C["lhelp-i698"] = {"gplants": [(SELFO, ob())],
                       "steps": [(LHELP, SELFO)]}
    C["lhelp-b5"] = {"gplants": [(SELFO, ob(q698=G698A))],
                     "steps": [(LHELP, SELFO)]}
    C["lhelp-cls0"] = {"gplants": [(SELFO, ob(q698=G698A,
                                             q10=OSUBA)),
                                   (G698A, ob(b5=1)),
                                   (OSUBA, ob(bE=0))],
                       "steps": [(LHELP, SELFO)]}
    C["lhelp-cls1"] = {"gplants": [(SELFO, ob(q698=G698A,
                                             q10=OSUBA)),
                                   (G698A, ob(b5=1)),
                                   (OSUBA, ob(bE=1))],
                       "steps": [(LHELP, SELFO)]}
    C["lhelp-cls2"] = {"gplants": [(SELFO, ob(q698=G698A,
                                             q10=OSUBA)),
                                   (G698A, ob(b5=1)),
                                   (OSUBA, ob(bE=2))],
                       "steps": [(LHELP, SELFO)]}
    C["lhelp-cls3"] = {"gplants": [(SELFO, ob(q698=G698A,
                                             q10=OSUBA)),
                                   (G698A, ob(b5=1)),
                                   (OSUBA, ob(bE=3))],
                       "steps": [(LHELP, SELFO)]}
    C["lhelp-cls5"] = {"gplants": [(SELFO, ob(q698=G698A,
                                             q10=OSUBA)),
                                   (G698A, ob(b5=1)),
                                   (OSUBA, ob(bE=5))],
                       "steps": [(LHELP, SELFO)]}
    C["lhelp-bad698"] = {"gplants": [(SELFO,
                                      ob(q698=0xFFFFFFF0))],
                         "steps": [(LHELP, SELFO)]}
    # --- record writers S3W 002FB500 / S2W 002FB340
    # (rcx=out rec, rdx=handle object) ---
    C["s3w-gen"] = {"gplants": [
                        (CANDA, ob(b3=0x60, qB8=QB8A)),
                        (QB8A, ob(0x200, d0=f2u(1.0), d4=f2u(2.0),
                                  d8=f2u(3.0), d50=f2u(4.0),
                                  d54=f2u(5.0), fA8=6.0))],
                    "steps": [(S3W, GOBJA, CANDA)],
                    "watch": [(GOBJA, 0x20)]}
    C["s2w-gen"] = {"gplants": [
                        (CANDA, ob(b3=0x60, qB8=QB8A)),
                        (QB8A, ob(0x200, d0=f2u(1.0), d4=f2u(2.0),
                                  d8=f2u(3.0), d50=f2u(4.0),
                                  d54=f2u(5.0)))],
                    "steps": [(S2W, GOBJA, CANDA)],
                    "watch": [(GOBJA, 0x14)]}
    # v1 object: o1f reads f38 -> out+0x18; f38->f3C mutant -> 0.
    C["s3w-v1"] = {"gplants": [
                       (CANDA, ob(b3=0x20, qB8=QB8A)),
                       (QB8A, ob(0x200, d0=f2u(1.0), d4=f2u(2.0),
                                 d8=f2u(3.0), f38=6.0))],
                   "steps": [(S3W, GOBJA, CANDA)],
                   "watch": [(GOBJA, 0x20)]}
    # --- capsule tests CDST 00469060 / CDZ0 00468D10 /
    # CF90 00468F90 (segv: seg@0, tmp rec@0x40) ---
    C["cdst-in"] = {"segv": [0, 0, 0, 0, 1.0] + [0.0] * 0xB +
                            [0, 0, 0.5, 0] + [0.0] * 0xEC,
                    "steps": [(CDST, SEGV + 0x40, SEGV)]}
    C["cdst-out"] = {"segv": [0, 0, 0, 0, 1.0] + [0.0] * 0xB +
                             [0, 0, 8.0, 0] + [0.0] * 0xEC,
                     "steps": [(CDST, SEGV + 0x40, SEGV)]}
    C["cdz0-in"] = {"segv": [0, 0, 0, 0, 1.0] + [0.0] * 0xB +
                            [0, 0, 0.5, 0] + [0.0] * 0xEC,
                    "steps": [(CDZ0, SEGV, SEGV + 0x40)]}
    C["cf90-in"] = {"segv": [0, 0, 0, 0, 0, 0, 4, 0, 1.0] +
                            [0.0] * 7 +
                            [0, 0, 2.0, 0] + [0.0] * 0xEC,
                    "steps": [(CF90, SEGV, SEGV + 0x40)]}
    C["cf90-out"] = {"segv": [0, 0, 0, 0, 0, 0, 4, 0, 1.0] +
                             [0.0] * 7 +
                             [0, 0, 8.0, 0] + [0.0] * 0xEC,
                     "steps": [(CF90, SEGV, SEGV + 0x40)]}
    # --- collectors GPC 00391A30 / GSC 00391D90 (rcx=query
    # rdx=out r8=flag); query = segv (pt {v4,rad} / seg layout) ---
    C["gpc-empty"] = {"grcnt": 0,
                      "steps": [(GPC, SEGV, GHND, 0x10)]}
    C["gpc-hit"] = {"grcnt": 1, "ghnd": [CANDA],
                    "cflags": [1] * 0x100,
                    "lsrc": {ci: b"\x01" for ci in range(64)},
                    "gplants": [
                        (CANDA, ob(b3=0x60, qB8=QB8A)),
                        (QB8A, ob(0x200, d0=f2u(1.0), d4=f2u(0.0),
                                  d8=f2u(2.0)))],
                    "segv": [1.0, 0, 2.0, 0, 2.0] + [0.0] * 0xFB,
                    "steps": [(GPC, SEGV, GHND, 0x10)],
                    "watch": [(GHND, 8)]}
    C["gpc-hit0"] = {"grcnt": 1, "ghnd": [CANDA],
                     "cflags": [1] * 0x100,
                     "lsrc": {ci: b"\x01" for ci in range(64)},
                     "gplants": [
                         (CANDA, ob(b3=0x60, qB8=QB8A)),
                         (QB8A, ob(0x200, d0=f2u(1.0),
                                   d4=f2u(0.0), d8=f2u(2.0)))],
                     "segv": [1.0, 0, 2.0, 0, 2.0] + [0.0] * 0xFB,
                     "steps": [(GPC, SEGV, GHND, 0)],
                     "watch": [(GHND, 8)]}
    C["gsc-empty"] = {"grcnt": 0,
                      "steps": [(GSC, SEGV, GHND, 0x10)]}
    C["gsc-hit"] = {"grcnt": 1, "ghnd": [CANDA],
                    "cflags": [1] * 0x100,
                    "lsrc": {ci: b"\x01" for ci in range(64)},
                    "gplants": [
                        (CANDA, ob(b3=0x60, qB8=QB8A)),
                        (QB8A, ob(0x200, d0=f2u(0.0), d4=f2u(0.0),
                                  d8=f2u(2.0)))],
                    "segv": [0, 0, 0, 0, 0, 0, 4, 0, 1.0] +
                            [0.0] * 0xF7,
                    "steps": [(GSC, SEGV, GHND, 0x10)],
                    "watch": [(GHND, 8)]}
    # --- wrappers GPT 00391D10 / GSEG 003920F0
    # (rcx=query rdx=out r8d=cnt r9d=flags) ---
    C["gpt-0"] = {"grcnt": 0,
                  "steps": [(GPT, SEGV, GHND, 0, 0)]}
    C["gseg-0"] = {"grcnt": 0,
                   "steps": [(GSEG, SEGV, GHND, 0, 0)]}
    # --- GFILT 003911D0 (rcx=out rdx=cnt r8=tmp r9d=n;
    # flags at entry+0x28 -> "garg5" slot) ---
    C["gfilt-0"] = {"garg5": 0x1C,
                    "steps": [(GFILT, GOBJA, 4, GHND, 0)]}

    # ================= EXP-136 direct cases =================
    # OBJD 00263E30 (rcx=handle): rax = q[h+0x30]; no guard.
    C["objd-ok"] = {"gplants": [(CANDA, ob(q30=SELFO))],
                    "steps": [(OBJD, CANDA)]}
    C["objd-null"] = {"steps": [(OBJD, 0)]}
    # O3FW 002646C0 (rcx=obj rdx/r8/r9=outs): v=(b[+3]>>5)-1;
    # v1 copy d[qB8+0/4/8]; v3 copy +(b[+0x107]&1: add f40/44/48);
    # else zero outs; null obj -> no writes.
    C["o3fw-v1"] = {"gplants": [
                        (CANDA, ob(b3=0x20, qB8=QB8A)),
                        (QB8A, ob(0x200, d0=f2u(1.0), d4=f2u(2.0),
                                  d8=f2u(3.0)))],
                    "steps": [(O3FW, CANDA, GOBJA, GOBJA + 0x10,
                               GOBJA + 0x20)],
                    "watch": [(GOBJA, 0x30)]}
    C["o3fw-v3"] = {"gplants": [
                        (CANDA, ob(b3=0x60, qB8=QB8A)),
                        (QB8A, ob(0x200, d0=f2u(1.0), d4=f2u(2.0),
                                  d8=f2u(3.0), b107=1, f40=0.5,
                                  f44=0.25, f48=1.5))],
                    "steps": [(O3FW, CANDA, GOBJA, GOBJA + 0x10,
                               GOBJA + 0x20)],
                    "watch": [(GOBJA, 0x30)]}
    C["o3fw-v3no"] = {"gplants": [
                        (CANDA, ob(b3=0x60, qB8=QB8A)),
                        (QB8A, ob(0x200, d0=f2u(1.0), d4=f2u(2.0),
                                  d8=f2u(3.0), f40=0.5, f44=0.25,
                                  f48=1.5))],
                      "steps": [(O3FW, CANDA, GOBJA, GOBJA + 0x10,
                                 GOBJA + 0x20)],
                      "watch": [(GOBJA, 0x30)]}
    C["o3fw-v0"] = {"gplants": [(CANDA, ob(b3=0x00, qB8=QB8A))],
                    "steps": [(O3FW, CANDA, GOBJA, GOBJA + 0x10,
                               GOBJA + 0x20)],
                    "watch": [(GOBJA, 0x30)]}
    C["o3fw-null"] = {"gplants": [(GOBJA, ob(d0=0x11, d4=0x22,
                                             d8=0x33))],
                      "steps": [(O3FW, 0, GOBJA, GOBJA + 0x10,
                                 GOBJA + 0x20)],
                      "watch": [(GOBJA, 0x30)]}
    # O2FW 00265090 (rcx=obj rdx/r8=outs): (b[+3]&0xE0)==0x60 ->
    # DA710(qB8+0x50): d50->rdx, d54->r8 (nonnull outs only).
    C["o2fw-yes"] = {"gplants": [
                        (CANDA, ob(b3=0x60, qB8=QB8A)),
                        (QB8A, ob(0x200, d50=f2u(4.0),
                                  d54=f2u(5.0)))],
                     "steps": [(O2FW, CANDA, GOBJA, GOBJA + 0x10)],
                     "watch": [(GOBJA, 0x20)]}
    C["o2fw-no"] = {"gplants": [
                        (CANDA, ob(b3=0x40, qB8=QB8A)),
                        (QB8A, ob(0x200, d50=f2u(4.0),
                                  d54=f2u(5.0)))],
                    "steps": [(O2FW, CANDA, GOBJA, GOBJA + 0x10)],
                    "watch": [(GOBJA, 0x20)]}
    C["o2fw-nulp"] = {"gplants": [
                        (CANDA, ob(b3=0x60, qB8=QB8A)),
                        (QB8A, ob(0x200, d50=f2u(4.0),
                                  d54=f2u(5.0)))],
                      "steps": [(O2FW, CANDA, 0, GOBJA + 0x10)],
                      "watch": [(GOBJA, 0x20)]}
    # O1F 00265200 (rcx=obj): v1 f[qB8+0x38]; v3 f[qB8+0xA8];
    # else/null -> 0.
    C["o1f-v1"] = {"gplants": [
                       (CANDA, ob(b3=0x20, qB8=QB8A)),
                       (QB8A, ob(0x200, f38=7.0, fA8=9.0))],
                   "steps": [(O1F, CANDA)]}
    C["o1f-v3"] = {"gplants": [
                       (CANDA, ob(b3=0x60, qB8=QB8A)),
                       (QB8A, ob(0x200, f38=7.0, fA8=9.0))],
                   "steps": [(O1F, CANDA)]}
    C["o1f-v0"] = {"gplants": [(CANDA, ob(b3=0x00, qB8=QB8A))],
                   "steps": [(O1F, CANDA)]}
    C["o1f-null"] = {"steps": [(O1F, 0)]}
    # O1F2 00263940 (rcx=obj): v1 f[qB8+0x68]; v3
    # f[qB8+0xC0]*f[qB8+0x24]; else 0. No null guard.
    C["o1f2-v1"] = {"gplants": [
                        (CANDA, ob(b3=0x20, qB8=QB8A)),
                        (QB8A, ob(0x200, f68=6.0, fC0=2.0,
                                  f24=3.0))],
                    "steps": [(O1F2, CANDA)]}
    C["o1f2-v3"] = {"gplants": [
                        (CANDA, ob(b3=0x60, qB8=QB8A)),
                        (QB8A, ob(0x200, f68=6.0, fC0=2.0,
                                  f24=3.0))],
                    "steps": [(O1F2, CANDA)]}
    C["o1f2-v0"] = {"gplants": [(CANDA, ob(b3=0x00, qB8=QB8A))],
                    "steps": [(O1F2, CANDA)]}
    C["o1f2-null"] = {"steps": [(O1F2, 0)]}
    # O1F3 00265830 (rcx=obj): (b[+3]&0xE0)==0x60 ->
    # f[q[qB8+0xF0]+0x24]; else 0. No null guard.
    C["o1f3-yes"] = {"gplants": [
                        (CANDA, ob(b3=0x60, qB8=QB8A)),
                        (QB8A, ob(0x200, qF0=QB8A + 0x200)),
                        (QB8A + 0x200, ob(0x100, f24=8.0))],
                     "steps": [(O1F3, CANDA)]}
    C["o1f3-no"] = {"gplants": [
                        (CANDA, ob(b3=0x40, qB8=QB8A)),
                        (QB8A, ob(0x200, qF0=QB8A + 0x200)),
                        (QB8A + 0x200, ob(0x100, f24=8.0))],
                    "steps": [(O1F3, CANDA)]}
    C["o1f3-null"] = {"steps": [(O1F3, 0)]}
    # OVF 002E9FE0 (rcx=obj): (b[+3]&0xE0)!=0x60 -> 1; else c0:
    # null||d[+0x164] -> 0; b11&0x20 ? b10&3==3 : b10&0xB==0xB;
    # ret (b11&6)==6.
    C["ovf-fast"] = {"gplants": [(CANDA, ob(b3=0x40))],
                     "steps": [(OVF, CANDA)]}
    C["ovf-c0null"] = {"gplants": [(CANDA, ob(b3=0x60))],
                       "steps": [(OVF, CANDA)]}
    C["ovf-d164"] = {"gplants": [
                         (CANDA, ob(b3=0x60, qC0=GC0A)),
                         (GC0A, ob(0x200, d164=1))],
                     "steps": [(OVF, CANDA)]}
    C["ovf-b10a"] = {"gplants": [
                         (CANDA, ob(b3=0x60, qC0=GC0A)),
                         (GC0A, ob(0x200, b10=0x03, b11=0x26))],
                     "steps": [(OVF, CANDA)]}
    C["ovf-b10af"] = {"gplants": [
                          (CANDA, ob(b3=0x60, qC0=GC0A)),
                          (GC0A, ob(0x200, b10=0x01, b11=0x26))],
                      "steps": [(OVF, CANDA)]}
    C["ovf-b10b"] = {"gplants": [
                         (CANDA, ob(b3=0x60, qC0=GC0A)),
                         (GC0A, ob(0x200, b10=0x0B, b11=0x06))],
                     "steps": [(OVF, CANDA)]}
    C["ovf-b11f"] = {"gplants": [
                         (CANDA, ob(b3=0x60, qC0=GC0A)),
                         (GC0A, ob(0x200, b10=0x03, b11=0x24))],
                     "steps": [(OVF, CANDA)]}
    # d164=1 with flag fields that would pass -> 0; a mutant
    # reading +0x168 skips the gate -> 1.
    C["ovf-d164p"] = {"gplants": [
                          (CANDA, ob(b3=0x60, qC0=GC0A)),
                          (GC0A, ob(0x200, d164=1, b10=0x03, b11=0x26))],
                      "steps": [(OVF, CANDA)]}
    # b10=7: &3==3 -> 1; a mutant masking &7 gives 7 -> 0.
    C["ovf-b107"] = {"gplants": [
                         (CANDA, ob(b3=0x60, qC0=GC0A)),
                         (GC0A, ob(0x200, b10=0x07, b11=0x26))],
                     "steps": [(OVF, CANDA)]}
    # b11=0x27: &6==6 -> 1; a mutant masking &7 gives 7 -> 0.
    C["ovf-b1127"] = {"gplants": [
                          (CANDA, ob(b3=0x60, qC0=GC0A)),
                          (GC0A, ob(0x200, b10=0x03, b11=0x27))],
                      "steps": [(OVF, CANDA)]}
    # OPA 00314EB0 (rcx=a rdx=b): r10=a->c0->138, r9=b->c0->138;
    # b[r10+6]==b[r9+6] req; b[r10+0x119]==0 -> 1;
    # !=0&&==b[r9+0x119] -> 0; else 1.
    C["opa-eq"] = {"gplants": [
                       (SELFO, ob(qC0=GC0A)),
                       (CANDA, ob(qC0=GC0A + 0x800)),
                       (GC0A, ob(0x200, q138=GC138A)),
                       (GC0A + 0x800, ob(0x200, q138=GC138A + 0x800)),
                       (GC138A, ob(0x200)),
                       (GC138A + 0x800, ob(0x200))],
                   "steps": [(OPA, SELFO, CANDA)]}
    C["opa-b6"] = {"gplants": [
                       (SELFO, ob(qC0=GC0A)),
                       (CANDA, ob(qC0=GC0A + 0x800)),
                       (GC0A, ob(0x200, q138=GC138A)),
                       (GC0A + 0x800, ob(0x200, q138=GC138A + 0x800)),
                       (GC138A, ob(0x200)),
                       (GC138A + 0x800, ob(0x200, b6=1))],
                   "steps": [(OPA, SELFO, CANDA)]}
    C["opa-119"] = {"gplants": [
                        (SELFO, ob(qC0=GC0A)),
                        (CANDA, ob(qC0=GC0A + 0x800)),
                        (GC0A, ob(0x200, q138=GC138A)),
                        (GC0A + 0x800, ob(0x200, q138=GC138A + 0x800)),
                        (GC138A, ob(0x200, b119=5)),
                        (GC138A + 0x800, ob(0x200, b119=7))],
                    "steps": [(OPA, SELFO, CANDA)]}
    C["opa-119eq"] = {"gplants": [
                          (SELFO, ob(qC0=GC0A)),
                          (CANDA, ob(qC0=GC0A + 0x800)),
                          (GC0A, ob(0x200, q138=GC138A)),
                          (GC0A + 0x800, ob(0x200,
                                            q138=GC138A + 0x800)),
                          (GC138A, ob(0x200, b119=5)),
                          (GC138A + 0x800, ob(0x200, b119=5))],
                      "steps": [(OPA, SELFO, CANDA)]}
    C["opa-anull"] = {"gplants": [(CANDA, ob(qC0=GC0A)),
                                  (GC0A, ob(0x200, q138=GC138A))],
                      "steps": [(OPA, 0, CANDA)]}
    # a+7==b+6 but a+6!=b+6 -> 0; [r10+6]->+7 mutant compares 1==1
    # -> 1.
    C["opa-b67"] = {"gplants": [
                        (SELFO, ob(qC0=GC0A)),
                        (CANDA, ob(qC0=GC0A + 0x800)),
                        (GC0A, ob(0x200, q138=GC138A)),
                        (GC0A + 0x800, ob(0x200, q138=GC138A + 0x800)),
                        (GC138A, ob(0x200, b7=1)),
                        (GC138A + 0x800, ob(0x200, b6=1))],
                    "steps": [(OPA, SELFO, CANDA)]}
    C["opa-c0null"] = {"gplants": [
                           (SELFO, ob()),
                           (CANDA, ob(qC0=GC0A + 0x800)),
                           (GC0A + 0x800, ob(0x200,
                                             q138=GC138A + 0x800))],
                       "steps": [(OPA, SELFO, CANDA)]}
    # OPB 00313F80 (rcx=a rdx=b r8=outp): A6A0 both -> F50 -> ret;
    # outp!=0 -> f[outp]=f50v.
    C["opb-ok"] = {"opbrets": [7], "f50v": [f2u(1.25)],
                   "gplants": [
                       (SELFO, ob(qC0=GC0A)),
                       (CANDA, ob(qC0=GC0A + 0x800)),
                       (GC0A, ob(0x200, q138=GC138A)),
                       (GC0A + 0x800, ob(0x200, q138=GC138A + 0x800))],
                   "steps": [(OPB, SELFO, CANDA, GOBJA)],
                   "watch": [(GOBJA, 8)]}
    C["opb-out0"] = {"opbrets": [3],
                     "gplants": [
                         (SELFO, ob(qC0=GC0A)),
                         (CANDA, ob(qC0=GC0A + 0x800)),
                         (GC0A, ob(0x200, q138=GC138A)),
                         (GC0A + 0x800, ob(0x200,
                                           q138=GC138A + 0x800))],
                     "steps": [(OPB, SELFO, CANDA, 0)]}
    C["opb-nul1"] = {"gplants": [(CANDA, ob(qC0=GC0A)),
                                 (GC0A, ob(0x200, q138=GC138A))],
                     "steps": [(OPB, 0, CANDA, GOBJA)]}
    C["opb-nul2"] = {"gplants": [(SELFO, ob(qC0=GC0A)),
                                 (GC0A, ob(0x200, q138=GC138A))],
                     "steps": [(OPB, SELFO, 0, GOBJA)]}
    # OF60 00313F60 (rcx=obj): tail-jump N7C20 -> of60rets.
    C["of60-ret"] = {"of60rets": [0x11],
                     "steps": [(OF60, SELFO)]}
    # OSUB 0026E350 (rcx=vec): root/table -> N31900(t,vec,1) ->
    # ax<0 -> -1; else N31820(t,vec,ax); ret 0.
    C["osub-ok"] = {"w19rets": [5],
                    "steps": [(OSUB, VECQ)]}
    C["osub-neg"] = {"w19rets": [0xFFFF],
                     "steps": [(OSUB, VECQ)]}
    C["osub-noroot"] = {"nroot": 0,
                        "steps": [(OSUB, VECQ)]}
    C["osub-notab"] = {"subtb": 0,
                       "steps": [(OSUB, VECQ)]}
    # MABESP 003588B0 (ecx=handle): bank=(h>>0x14)&0x7FF,
    # sel=(h>>0x10)&0xF (<5), gen=h&0xFFFF; T=N63FF0(sel);
    # entry q[arr+8+gen*8] iff w[entry+0x16]==bank.
    C["mabesp-ok"] = {"msparr": {0x42: SELFO},
                      "gplants": [(SELFO, ob())],
                      "steps": [(MABESP, 0x42)]}
    C["mabesp-0"] = {"steps": [(MABESP, 0)]}
    C["mabesp-sel5"] = {"steps": [(MABESP, 0x50042)]}
    C["mabesp-gen"] = {"msparr": {0x42: SELFO},
                       "mspn": 0x40,
                       "gplants": [(SELFO, ob())],
                       "steps": [(MABESP, 0x42)]}
    C["mabesp-bank"] = {"msparr": {0x42: SELFO},
                        "gplants": [(SELFO, ob(w16=1))],
                        "steps": [(MABESP, 0x100042)]}
    C["mabesp-bankf"] = {"msparr": {0x42: SELFO},
                         "gplants": [(SELFO, ob(w16=1))],
                         "steps": [(MABESP, 0x200042)]}
    C["mabesp-noent"] = {"msparr": {0x42: 0},
                         "steps": [(MABESP, 0x42)]}
    C["mabesp-notab"] = {"t3frets": [0],
                         "steps": [(MABESP, 0x42)]}
    C["mabesp-noarr"] = {"t3frets": [GC0A],
                         "gplants": [(GC0A, ob(0x100))],
                         "steps": [(MABESP, 0x42)]}
    # DE100 0026E100: rcx=tab(root?SUBTB:0), rdx=obj,
    # r8=zx(arg1), r9=arg2 -> tail N31400.
    C["de100-on"] = {"derets": [3],
                     "steps": [(DE100, CANDA, 0x12345678, 9)]}
    C["de100-off"] = {"derets": [3], "nroot": 0,
                      "steps": [(DE100, CANDA, 0x12345678, 9)]}
    # AGENTQ 00318CA0: rcx=q[0x2EC1378]; null -> -1;
    # else cwde(N315E0(rcx,obj,out,a4)).
    C["agq-pos"] = {"agrets": [0x7F00],
                    "steps": [(AGENTQ, CANDA, GOBJA, 0, 2)]}
    C["agq-neg"] = {"agrets": [-2],
                    "steps": [(AGENTQ, CANDA, GOBJA, 0, 2)]}
    C["agq-null"] = {"agqtb": 0,
                     "steps": [(AGENTQ, CANDA, GOBJA, 0, 2)]}
    return C


# ---------------- mutations (verified byte-precise) ----------------

MUTS = [
    # QWALK 0033D3E0 (sites byte-verified against shipped image)
    ("m-walk-sameje", "walk-negcls", 0x33D4A7, 0x84, 0x85),  # cur==dst je->jne
    ("m-walk-budget", "walk-cycle",  0x33D607, 0xFD, 0xFC),  # r13d -> r12d
    ("m-walk-degw",   "walk-2hop",   0x33D4B1, 0x0A, 0x0C),  # w[rbp+0xa]->+0xc
    ("m-walk-mat",    "walk-2hop",   0x33D4EA, 0x48, 0x88),  # adj *2 -> *4
    ("m-walk-b5",     "walk-2hop",   0x33D502, 0x05, 0x06),  # edge b+5 -> +6
    ("m-walk-cmp1",   "walk-2hop",   0x33D50A, 0x01, 0x00),  # cmp eax,1 -> 0
    ("m-walk-je",     "walk-2hop",   0x33D50B, 0x74, 0x75),  # ==1 je -> jne
    ("m-walk-flgshl", "walk-flag",   0x33D52B, 0xE0, 0xE8),  # shl eax,cl->shr
    ("m-walk-ftest",  "walk-2hop",   0x33D4EE, 0x84, 0x85),  # e==0 je -> jne
    ("m-walk-segjn",  "walk-2hop",   0x33D5D9, 0x75, 0x74),  # seg jne -> je
    ("m-walk-adv",    "walk-2hop",   0x33D5F0, 0xF6, 0xF0),  # r14d=esi -> eax
    ("m-walk-grid1",  "walk-p1off",  0x33D439, 0x75, 0x74),  # p1 jne -> je
    ("m-walk-grid2",  "walk-p2cyc",  0x33D46A, 0x75, 0x74),  # p2 jne -> je
    ("m-walk-p1x",    "walk-3hop",   0x33D402, 0x45, 0x55),  # [rcx+0] -> [rdx+0]
    ("m-walk-jae",    "walk-negcls", 0x33D4B3, 0x83, 0x82),  # jae -> jb
    ("m-walk-slotsk", "walk-2hop",   0x33D4CB, 0xF4, 0xF6),  # prev-skip -> cur-skip
    # GGRID 00383F10
    ("m-grid-fdcx",   "grid-nanx",   0x383F47, 0x02, 0x03),  # cmp ax,2 -> 3
    ("m-grid-fdcy",   "grid-nany",   0x383F5D, 0x02, 0x03),  # cmp ax,2 -> 3
    ("m-grid-boundx", "grid-t0",     0x383F78, 0x87, 0x86),  # ja -> jbe
    ("m-grid-boundy", "grid-t0",     0x383F94, 0x87, 0x86),  # ja -> jbe
    ("m-grid-bxup",   "grid-t0",     0x383FB0, 0x87, 0x86),  # x up ja -> jbe
    ("m-grid-byup",   "grid-t0",     0x383FCE, 0x87, 0x86),  # y up ja -> jbe
    ("m-grid-cellh",  "grid-multi2", 0x383FEF, 0x01, 0x02),  # b[rbx+1]->+2
    ("m-grid-orgx",   "grid-cw4",    0x384011, 0x04, 0x08),  # w[rbx+4]->+8
    ("m-grid-ffff",   "grid-ffff",   0x384033, 0xFF, 0xFE),  # cell 0xFFFF cmp
    ("m-grid-0xff",   "grid-empty",  0x384051, 0xFF, 0xFE),  # list end 0xFF
    ("m-grid-stride", "grid-multi2", 0x38407B, 0x22, 0x24),  # rec *0x22->*0x24
    ("m-grid-sel",    "grid-multi2", 0x3840AD, 0x14, 0x16),  # rec +0x14->+0x16
    ("m-grid-trije",  "grid-multi2", 0x3840CC, 0x74, 0x75),  # ttest je->jne
    ("m-grid-listjn", "grid-multi2", 0x3840F9, 0x85, 0x84),  # next list jne
    ("m-grid-cntcmp", "grid-multi",  0x384081, 0x02, 0x04),  # rec +2 -> +4
    # TTEST 00382D10
    ("m-tri-arr",     "tri-below",   0x382D34, 0x78, 0x7C),  # idx arr lea +4
    ("m-tri-mul1",    "tri-in",      0x382E2A, 0x59, 0x58),  # mulss -> addss
    ("m-tri-mul2",    "tri-in",      0x382E30, 0xC0, 0xC1),  # py*ex -> py*acc
    ("m-tri-sub",     "tri-in",      0x382E33, 0x5C, 0x58),  # subss -> addss
    ("m-tri-ucmp",    "tri-below",   0x382E13, 0xCA, 0xC8),  # vs xmm10 -> xmm8
    ("m-tri-jne",     "tri-below",   0x382E37, 0x75, 0x74),  # jne -> je
    ("m-tri-ja",      "tri-edge",    0x382E48, 0x77, 0x76),  # ja -> jbe
    ("m-tri-loop",    "tri-below",   0x382E51, 0x8C, 0x8D),  # jl -> jge
    ("m-tri-vscale",  "tri-below",   0x382D96, 0xDF, 0x9F),  # vert *8 -> *4
    ("m-tri-esub",    "tri-out",     0x382DA1, 0xD0, 0x90),  # edge *8 -> *4
    # SEGT 00468880
    ("m-seg-jbe1",    "seg-cross",   0x4689A6, 0x76, 0x77),  # h1 jbe -> ja
    ("m-seg-jbe2",    "seg-rev",     0x4689AB, 0x76, 0x77),  # i1 jbe -> ja
    ("m-seg-jbe3",    "seg-vline",   0x4689B7, 0x76, 0x77),  # 0<=h1 jbe->ja
    ("m-seg-ja4",     "seg-vline",   0x4689BC, 0x77, 0x76),  # i1 ja -> jbe
    ("m-seg-ja5",     "seg-cross",   0x468A3B, 0x87, 0x86),  # h2 ja -> jbe
    ("m-seg-jbe6",    "seg-beyond2", 0x468A43, 0x76, 0x77),  # 0<=h2 jbe->ja
    ("m-seg-call",    "seg-cross",   0x46893C, 0x40, 0x44),  # vsub rel32 +4
    ("m-seg-call2",   "seg-cross",   0x46894D, 0x2F, 0x33),  # vsub2 rel32 +4
    ("m-seg-xcall",   "seg-cross",   0x468984, 0x88, 0x8C),  # xprod rel32 +4
    ("m-seg-xcall2",  "seg-cross",   0x468995, 0x77, 0x7B),  # xprod2 rel32 +4
    ("m-seg-cook",    "seg-cross",   0x468899, 0x93, 0x9B),  # cookie cell disp
    # ECLASS 0026E300 (+ thunk 0x32A780)
    ("m-cls-js",      "cls-neg",     0x26E317, 0x78, 0x79),  # js -> jns
    ("m-cls-shl",     "cls-w0",      0x26E32F, 0xE2, 0xE8),  # shl edx,cl->shr
    ("m-cls-w0d",     "cls-both",    0x26E338, 0x04, 0x08),  # test [r8+4]->+8
    ("m-cls-je",      "cls-w0",      0x26E333, 0x74, 0x75),  # w0 je -> jne
    ("m-cls-cmov",    "cls-both",    0x26E33F, 0x45, 0x44),  # cmovne -> cmove
    ("m-cls-thunk",   "walk-2hop",   0x32A781, 0x7B, 0x7F),  # jmp rel32 +4
    ("m-cls-tab",     "cls-w0",      0x26E311, 0x60, 0x64),  # classtab -> +4
    # WWRAP 00384130
    ("m-wrap-z",      "wrap-t1",     0x38413C, 0x08, 0x04),  # vec.z -> vec.y
    # BASE 0020E600
    ("m-base-add",    "base-off",    0x20E605, 0x27, 0x2B),  # pool cell disp
    # ---------- EXP-132 new bodies (sites byte-verified) ----------
    # PATHW 0033A3D0
    ("m-pw-cmp1",   "pathw-block",   0x33A408, 0x01, 0x02),  # probe0 cmp eax,1->2
    ("m-pw-je0",    "pathw-block",   0x33A409, 0x74, 0x75),  # probe0 je -> jne
    ("m-pw-cmp1b",  "pathw-rotfail", 0x33A4A0, 0x01, 0x02),  # r1 cmp 1 -> 2
    ("m-pw-je1",    "pathw-rotfail", 0x33A4A1, 0x74, 0x75),  # r1 je -> jne
    ("m-pw-jne1",   "pathw-r1p2",    0x33A4BA, 0x85, 0x84),  # r1 p2 jne -> je
    ("m-pw-cmp2a",  "pathw-rotfail", 0x33A523, 0x01, 0x02),  # r1' cmp 1 -> 2
    ("m-pw-je2",    "pathw-rotfail", 0x33A524, 0x74, 0x75),  # r1' je -> jne
    ("m-pw-jne2",   "pathw-r2p2",    0x33A53D, 0x85, 0x84),  # r2 p2 jne -> je
    ("m-pw-ret1",   "pathw-direct",  0x33A40C, 0x01, 0x02),  # mov eax,1 -> 2
    ("m-pw-sc",     "pathw-mixed",   0x33A429, 0x43, 0x47),  # scale const +4
    ("m-pw-ang1",   "pathw-mixed",   0x33A44A, 0xC6, 0xCA),  # angle1 cell +4
    ("m-pw-ang2",   "pathw-mixed",   0x33A4CD, 0x47, 0x4B),  # angle2 cell +4
    # BLKCHK 00335F90
    ("m-blk-predje", "blk-clear",    0x335FCE, 0x75, 0x74),  # pred jne -> je
    ("m-blk-walkje", "blk-clear",    0x335FE1, 0x01, 0x00),  # walk cmp 1 -> 0
    ("m-blk-mode7",  "blk-mode3-0",  0x335FF1, 0x03, 0x07),  # mode cmp 3 -> 7
    ("m-blk-agq",    "blk-mode3-0",  0x336002, 0x9A, 0xA2),  # agq call retarget
    ("m-blk-agqje",  "blk-mode3-1",  0x336006, 0x85, 0x29),  # test -> sub eax
    ("m-blk-sc",     "blk-scale",    0x335FC0, 0xC8, 0xCC),  # BKSC disp +4
    ("m-blk-subf",   "blk-clear",    0x335FA2, 0x08, 0x0C),  # agent+0x108->+0x10C
    # AWRAP 0033CB70
    ("m-aw-hi",     "awrap-inf",     0x33CB7A, 0x77, 0x76),  # hi gate ja->jbe
    ("m-aw-lo",     "awrap-neginf",  0x33CB87, 0x77, 0x76),  # lo gate ja->jbe
    ("m-aw-ja1",    "awrap-3pi2",    0x33CBA7, 0x77, 0x76),  # loop1 back ja->jbe
    ("m-aw-add1",   "awrap-3pi2",    0x33CBA2, 0x58, 0x5C),  # addss -2pi -> subss
    ("m-aw-add2",   "awrap-n3pi2",   0x33CBC2, 0x58, 0x5C),  # addss +2pi -> subss
    ("m-aw-cvtt",   "awrap-big",     0x33CBD7, 0x2C, 0x2A),  # cvttss2si->cvtsi2ss
    ("m-aw-hidisp", "awrap-13",      0x33CB76, 0x92, 0x96),  # hi gate cell +4
    ("m-aw-lodisp", "awrap-n7",      0x33CB80, 0x9C, 0xA0),  # lo gate cell +4
    ("m-aw-n2disp", "awrap-3pi2",    0x33CB9A, 0x86, 0x8A),  # -2pi cell -> 3e29
    ("m-aw-npdisp", "awrap-n3pi2",   0x33CBAD, 0x6F, 0x77),  # -pi cell -> 3e29
    ("m-aw-div",    "awrap-big",     0x33CBCF, 0x5E, 0x59),  # divss -> mulss
    # MLOAD 00203170
    ("m-ml-disp",   "mload-const",   0x203173, 0x09, 0x0D),  # src1 +4
    ("m-ml-disp2",  "mload-const",   0x20317D, 0x0F, 0x13),  # src2 +4
    # RBUILD 00202F00
    ("m-rb-call1",  "rbuild-zero",   0x202F38, 0xCC, 0xD2),  # cosf -> sinf
    ("m-rb-call2",  "rbuild-zero",   0x202F43, 0xC7, 0xC1),  # sinf -> cosf
    # ROTCOL 00217880
    ("m-rc-sub",    "rotcol-mix",    0x2178D7, 0x5C, 0x58),  # subss -> addss
    ("m-rc-disp",   "rotcol-mix",    0x21788F, 0x08, 0x0C),  # [rcx+8]->+0xC
    # MXV 00217060
    ("m-mxv-add",   "mxv-gen",       0x2170A8, 0x58, 0x5C),  # addss -> subss
    ("m-mxv-disp",  "mxv-gen",       0x2170A5, 0x14, 0x18),  # m[0x14]->m[0x18]
    # ---------- EXP-133 nav-LOS ----------
    # LQUERY 00391410
    ("m-los-nullje", "los-null-f",   0x39144F, 0x84, 0x85),  # null je -> jne
    ("m-los-maxss",  "los-zwide",    0x391471, 0x5F, 0x5D),  # maxss -> minss
    ("m-los-divss",  "los-far3",     0x3914F4, 0x5E, 0x59),  # divss -> mulss
    ("m-los-shl",    "los-bit1",     0x391584, 0xE0, 0xE8),  # shl -> shr
    ("m-los-cmp32",  "los-nav",      0x391590, 0x20, 0x21),  # i>=0x20 -> 0x21
    ("m-los-je0",    "los-t0-block", 0x3915A8, 0x74, 0x75),  # type0 je -> jne
    ("m-los-cmp1",   "los-t1-block", 0x3915AC, 0x01, 0x02),  # type cmp 1 -> 2
    ("m-los-r28",    "los-t0-block", 0x39159A, 0x28, 0x2C),  # root+0x28->+0x2C
    ("m-los-jne",    "los-t0-block", 0x39169E, 0x75, 0x74),  # ret1 jne -> je
    ("m-los-cmp8",   "los-bit8",     0x3916A4, 0x08, 0x09),  # col wrap 8 -> 9
    ("m-los-lea50",  "los-t0-block", 0x39153A, 0x50, 0x60),  # dist arg +0x50
    # BMASK 003912E0
    ("m-bm-flgje",   "bmask-flip",   0x391398, 0x74, 0x75),  # flag0 je -> jne
    ("m-bm-imul",    "bmask-range",  0x39139D, 0xC2, 0xC0),  # *rlen -> *eax
    ("m-bm-jl",      "bmask-1",      0x3913D1, 0x7C, 0x7D),  # copy jl -> jge
    ("m-bm-cmovl",   "bmask-wild",   0x391329, 0x4F, 0x4C),  # cmovg -> cmovl
    # DIST 003A1920
    ("m-dist-sub",   "dist-1",       0x3A194A, 0x58, 0x5C),  # addss -> subss
    # CPSEG 004691A0
    ("m-cps-div",    "cpseg-mid",    0x46924E, 0x5E, 0x59),  # divss -> mulss
    ("m-cps-jbe0",   "cpseg-pre",    0x469254, 0x76, 0x77),  # t<0 jbe -> ja
    ("m-cps-jbe1",   "cpseg-post",   0x469263, 0x76, 0x77),  # t<=1 jbe -> ja
    # TRIGD 00468580
    ("m-trg-jbe",    "capt1-eps",    0x468666, 0x76, 0x77),  # eps jbe -> ja
    ("m-trg-div",    "capt1-divlim", 0x468637, 0x5E, 0x59),  # x7 /= e14 -> *
    # CAPT0 00468D50
    ("m-c0-seta",    "capt0-block",  0x468E33, 0x97, 0x96),  # seta -> setbe
    ("m-c0-jnex",    "capt0-block",  0x468D78, 0x75, 0x74),  # x-eq jne -> je
    ("m-c0-jnecx",   "capt0-p1eq",   0x468DE0, 0x75, 0x74),  # cx-eq jne -> je
    # CAPT1 00468E50
    ("m-c1-jnex",    "capt1-p1eq",   0x468EB7, 0x75, 0x74),  # cx-eq jne -> je
    ("m-c1-seta",    "capt1-block",  0x468F61, 0x97, 0x96),  # seta -> setbe
    # CAPV 00469410
    ("m-cv-jbe0",    "capv-pre2",    0x4694D3, 0x76, 0x77),  # t<0 jbe -> ja
    ("m-cv-ja1",     "capv-post",    0x4694F9, 0x77, 0x76),  # t>1 ja -> jbe
    ("m-cv-jbee",    "capv-pre",     0x4694E8, 0x76, 0x77),  # early jbe -> ja
    # RDEC 0032A6E0
    ("m-rd-shl4",    "rdec-1",       0x32A6F6, 0x04, 0x05),  # rec stride 16->32
    ("m-rd-shl6",    "rdec-1",       0x32A706, 0x06, 0x07),  # vtx stride 64->128
    ("m-rd-movsx4",  "rdec-1",       0x32A712, 0x04, 0x06),  # rec.x -> rec.y
    ("m-rd-movsx2",  "rdec-1",       0x32A702, 0x02, 0x04),  # vtx idx -> rec.x

    # ---- EXP-134: PVAL 00335B60 ----
    ("m-pv-jp",      "pv-tol0",      0x335B9E, 0x7A, 0xEB),  # jp -> jmp: tol==0 continues
    ("m-pv-jne",     "pv-clear",     0x335BA0, 0x75, 0x74),  # tol!=0 jne->je
    ("m-pv-min",     "pv-caplo",     0x335BBE, 0x5D, 0x5F),  # cap minss->maxss
    ("m-pv-max",     "pv-clear",     0x335BD6, 0x5F, 0x5D),  # clamp maxss->minss
    ("m-pv-bjp",     "pv-clear",     0x335BD8, 0x7A, 0xEB),  # jp -> jmp: always divide
    ("m-pv-bje",     "pv-clear",     0x335BDA, 0x74, 0x75),  # angB==0 je->jne
    ("m-pv-div",     "pv-angb60",    0x335BE6, 0x5E, 0x59),  # tol/cos -> tol*cos
    ("m-pv-xorps",   "pv-angb-neg",  0x335BF3, 0x57, 0x56),  # xorps->orps sign
    ("m-pv-mload",   "pv-clear",     0x335BEE, 0x7E, 0x9E),  # mload rel32 +0x20: row3 only
    ("m-pv-mcpy",    "pv-clear",     0x335C07, 0x85, 0x8D),  # mcpy rel32 +8
    ("m-pv-mxvw1",   "pv-clear",     0x335C1D, 0x4F, 0x57),  # mxvw rel32 +8
    ("m-pv-awrap",   "pv-clear",     0x335C30, 0x3C, 0x44),  # awrap rel32 +8
    ("m-pv-rbuild",  "pv-clear",     0x335C42, 0xBA, 0xC2),  # rbuild rel32 +8
    ("m-pv-mxvw2",   "pv-clear",     0x335C56, 0x16, 0x1E),  # mxvw2 rel32 +8
    ("m-pv-rad110",  "pv-clear",     0x335C72, 0x10, 0x0C),  # v50 rad +0x110->+0x10C
    ("m-pv-vsc1",    "pv-clear",     0x335C77, 0x65, 0x6D),  # vscale rel32 +8
    ("m-pv-vad1",    "pv-clear",     0x335C89, 0x83, 0x8B),  # vadd rel32 +8
    ("m-pv-v50w",    "pv-clear",     0x335C97, 0x3F, 0x40),  # v50.w 1.0->2.0
    ("m-pv-v40w",    "pv-clear",     0x335CCC, 0x3F, 0x40),  # v40.w 1.0->2.0
    ("m-pv-rad2",    "pv-clear",     0x335CD6, 0x10, 0x0C),  # s60 rad +0x110->+0x10C
    ("m-pv-mulc",    "pv-clear",     0x335CE0, 0x59, 0x58),  # rad*clamp -> +
    ("m-pv-subc",    "pv-clear",     0x335CE4, 0x5C, 0x58),  # rad-rad*c -> +
    ("m-pv-addt",    "pv-clear",     0x335CE8, 0x58, 0x5C),  # s60 +tol -> -tol
    ("m-pv-and4",    "pv-flag12",    0x335D0E, 0x04, 0x08),  # flags&4 -> &8
    ("m-pv-or10",    "pv-flag6-m3",  0x335D18, 0x10, 0x20),  # |0x10 -> |0x20
    ("m-pv-shl2",    "pv-flag6",     0x335D1B, 0x02, 0x03),  # <<2 -> <<3
    ("m-pv-and2",    "pv-flag6-pop", 0x335D1E, 0x02, 0x01),  # flags&2 -> &1
    ("m-pv-r9f0",    "pv-gateptr",   0x335D12, 0xF0, 0xE0),  # gate r9 +0xF0->+0xE0
    ("m-pv-raxe0",   "pv-gateptr",   0x335D27, 0xE0, 0xF0),  # gate stk +0xE0->+0xF0
    ("m-pv-gate",    "pv-clear",     0x335D38, 0x74, 0x7C),  # gate rel32 +8
    ("m-pv-cmp1",    "pv-gate2",     0x335D40, 0x01, 0x02),  # gate==1 -> ==2
    ("m-pv-je1",     "pv-gate1",     0x335D41, 0x74, 0x75),  # gate je->jne
    ("m-pv-mode3",   "pv-mode3-agq", 0x335D50, 0x03, 0x04),  # mode==3 -> ==4
    ("m-pv-mjne",    "pv-mode3-clear", 0x335D51, 0x75, 0x74),  # mode jne->je
    ("m-pv-agq",     "pv-mode3-agq", 0x335D62, 0x3A, 0x42),  # agq rel32 +8
    ("m-pv-agqtst",  "pv-mode3-agq", 0x335D66, 0x85, 0x31),  # test->xor: agq=0
    ("m-pv-agqjne",  "pv-mode3-agq", 0x335D68, 0x75, 0x74),  # agq jne->je
    ("m-pv-tst8",    "pv-flag8-rad4", 0x335D6D, 0x08, 0x10),  # flags&8 -> &0x10
    ("m-pv-fje",     "pv-pred-block", 0x335D7D, 0x74, 0x75),  # flag je->jne
    ("m-pv-wcmp",    "pv-qwalk-clear", 0x335D8E, 0x01, 0x00),  # qwalk==1 -> ==0
    ("m-pv-wjne",    "pv-qwalk-block", 0x335D8F, 0x75, 0x74),  # qwalk jne->je
    ("m-pv-bksc",    "pv-pred-rad1", 0x335DA2, 0x59, 0x58),  # rad*0.9 -> rad+0.9
    ("m-pv-ptst",    "pv-pred-block", 0x335DB5, 0x85, 0x31),  # pred test->xor
    ("m-pv-pjne",    "pv-clear",     0x335DB7, 0x75, 0x74),  # pred jne->je
    ("m-pv-lqrad",   "pv-los-block", 0x335DCD, 0x10, 0x0C),  # lq rad +0x110->+0x10C
    ("m-pv-lq",      "pv-clear",     0x335DD6, 0x36, 0x3E),  # lquery rel32 +8
    ("m-pv-lqtst",   "pv-los-block", 0x335DDA, 0x85, 0x31),  # lq test->xor
    ("m-pv-lqjne",   "pv-clear",     0x335DDC, 0x75, 0x74),  # lq jne->je
    ("m-pv-dl3",     "pv-mode3-clear", 0x335DF8, 0x03, 0x04),  # cmp dl,3 -> 4
    ("m-pv-de",      "pv-clear",     0x335DFE, 0x9E, 0xA6),  # de6a0 rel32 +8
    ("m-pv-detst",   "pv-clear",     0x335E02, 0x85, 0x31),  # de test->xor
    ("m-pv-deje",    "pv-gate2-de0", 0x335E04, 0x74, 0x75),  # de je->jne
    ("m-pv-mov2",    "pv-gate2",     0x335E07, 0x02, 0x03),  # ret2 -> ret3
    ("m-pv-cmove",   "pv-clear",     0x335E0E, 0x44, 0x45),  # cmove->cmovne
    # ---- ROTX 00217790 ----
    ("m-rx-zmul",    "rotx-gen",     0x2177B8, 0x59, 0x58),  # z*s -> z+s
    ("m-rx-ysub",    "rotx-gen",     0x2177C9, 0x5C, 0x58),  # yc-zs -> +
    ("m-rx-ymul",    "rotx-gen",     0x2177CD, 0x59, 0x5C),  # y*s -> y-s
    ("m-rx-zadd",    "rotx-gen",     0x2177DC, 0x58, 0x5C),  # ys+zc -> -
    ("m-rx-zrd",     "rotx-gen",     0x217798, 0x08, 0x04),  # [rcx+8] -> [rcx+4]
    ("m-rx-ywr",     "rotx-gen",     0x2177E7, 0x04, 0x08),  # y' -> z slot
    ("m-rx-c1z",     "rotx-gen",     0x2177BE, 0x18, 0x08),  # col1 z <- col0 z
    ("m-rx-ycmul",   "rotx-gen",     0x2177C1, 0x59, 0x5C),  # y*c -> y-c
    ("m-rx-zcmul",   "rotx-gen",     0x2177C5, 0x59, 0x58),  # z*c -> z+c
    # ---- MCPY 00202E90 ----
    ("m-cp-movups",  "mcpy-gen",     0x202E97, 0x10, 0x11),  # movups ld -> st
    ("m-cp-movaps",  "mcpy-gen",     0x202EC6, 0xC2, 0xC6),  # cos arg xmm2->xmm6
    ("m-cp-swap",    "mcpy-gen",     0x202EDC, 0xD6, 0xD0),  # xmm2<-cos -> <-sin
    ("m-cp-cosf",    "mcpy-gen",     0x202EC8, 0x3C, 0x42),  # cosf -> sinf
    ("m-cp-sinf",    "mcpy-gen",     0x202ED3, 0x37, 0x31),  # sinf -> cosf
    ("m-cp-jmp",     "mcpy-gen",     0x202EF0, 0x9C, 0xA4),  # jmp rotx +8

    # ---- EXP-136: object accessors / subsystem leaves ----
    # OBJD 00263E30
    ("m-oa-objd30", "objd-ok",      0x263E33, 0x30, 0x38),  # h+0x30 -> +0x38
    # O3FW 002646C0
    ("m-oa-3fshr",  "o3fw-v1",      0x2646D1, 0x05, 0x04),  # shr 5 -> 4
    ("m-oa-3fje1",  "o3fw-v1",      0x2646D6, 0x74, 0x75),  # v1 je -> jne
    ("m-oa-3fcmp",  "o3fw-v3",      0x2646DB, 0x02, 0x03),  # cmp 2 -> 3
    ("m-oa-3fb8",   "o3fw-v3",      0x2646EC, 0xB8, 0xC0),  # qB8 -> qC0
    ("m-oa-3f107",  "o3fw-v3",      0x264706, 0x01, 0x02),  # b107 &1 -> &2
    ("m-oa-3ff40",  "o3fw-v3",      0x26470D, 0x40, 0x44),  # f40 -> f44
    ("m-oa-3fadd",  "o3fw-v3",      0x264710, 0x58, 0x5C),  # addss -> subss
    # O2FW 00265090 / DA710 003DA710
    ("m-oa-2fand",  "o2fw-yes",     0x265095, 0xE0, 0xC0),  # &0xE0 -> &0xC0
    ("m-oa-2fcmp",  "o2fw-yes",     0x265097, 0x60, 0x40),  # cmp 0x60 -> 0x40
    ("m-oa-2fb8",   "o2fw-yes",     0x26509D, 0xB8, 0xC0),  # qB8 -> qC0
    ("m-oa-2f50",   "o2fw-yes",     0x2650A4, 0x50, 0x54),  # +0x50 -> +0x54
    ("m-oa-2fd54",  "o2fw-yes",     0x3DA720, 0x04, 0x08),  # DA710 d4 -> d8
    # O1F 00265200
    ("m-oa-1fshr",  "o1f-v1",       0x26520B, 0x05, 0x04),  # shr 5 -> 4
    ("m-oa-1fsub",  "o1f-v1",       0x26520E, 0x01, 0x02),  # sub 1 -> 2
    ("m-oa-1f38",   "s3w-v1",       0x265231, 0x38, 0x3C),  # f38 -> f3C
    ("m-oa-1fa8",   "s3w-gen",      0x265221, 0xA8, 0xAC),  # fA8 -> fAC
    # O1F2 00263940
    ("m-oa-12f68",  "gate-acc3v1",  0x263975, 0x68, 0x6C),  # f68 -> f6C
    ("m-oa-12fc0",  "gate-acc3skip", 0x26395C, 0xC0, 0xC4),  # fC0 -> fC4
    ("m-oa-12f24",  "gate-acc3skip", 0x263964, 0x24, 0x28),  # f24 -> f28
    ("m-oa-12mul",  "gate-acc3m",   0x263962, 0x59, 0x58),  # mulss -> addss
    # O1F3 00265830
    ("m-oa-13fand", "o1f3-yes",     0x265835, 0xE0, 0xC0),  # &0xE0 -> &0xC0
    ("m-oa-13fcmp", "o1f3-yes",     0x265837, 0x60, 0x40),  # cmp 0x60 -> 0x40
    ("m-oa-13ff0",  "o1f3-yes",     0x265848, 0xF0, 0xF8),  # qF0 -> qF8
    ("m-oa-13f24",  "gate-f10skip", 0x265850, 0x24, 0x28),  # f24 -> f28
    # OVF 002E9FE0
    ("m-oa-ovfand", "ovf-c0null",   0x2E9FE5, 0xE0, 0xC0),  # &0xE0 -> &0xC0
    ("m-oa-ovfcmp", "ovf-fast",     0x2E9FE7, 0x60, 0x40),  # cmp 0x60 -> 0x40
    ("m-oa-ovf164", "ovf-d164p",    0x2E9FFE, 0x64, 0x68),  # d164 -> d168
    ("m-oa-ovfje20", "ovf-b10a",    0x2EA010, 0x75, 0x74),  # arm jne -> je
    ("m-oa-ovfandb", "ovf-b10b",    0x2EA013, 0x0B, 0x0C),  # b10 &0xB -> &0xC
    ("m-oa-ovfcmpb", "ovf-b10b",    0x2EA015, 0x0B, 0x0A),  # cmp 0xB -> 0xA
    ("m-oa-ovfand3", "ovf-b107",    0x2EA019, 0x03, 0x07),  # b10 &3 -> &7
    ("m-oa-ovfand6", "ovf-b1127",   0x2EA020, 0x06, 0x07),  # b11 &6 -> &7
    ("m-oa-ovfcmp6", "ovf-b10a",    0x2EA023, 0x06, 0x07),  # cmp 6 -> 7
    # OPA 00314EB0
    ("m-oa-opa6",   "opa-b6",       0x314EF7, 0x06, 0x07),  # movzx [r9+6] -> +7
    ("m-oa-opacmp6", "opa-b67",     0x314EFB, 0x06, 0x07),  # cmp [r10+6] -> +7
    ("m-oa-opaje",  "opa-eq",       0x314EFC, 0x75, 0x74),  # class jne -> je
    ("m-oa-opa10",  "opa-eq",       0x314F08, 0x74, 0x75),  # b119==0 je -> jne
    ("m-oa-opa119", "opa-119eq",    0x314F02, 0x19, 0x1A),  # +0x119 -> +0x11A
    ("m-oa-opa11e", "opa-119eq",    0x314F11, 0x74, 0x75),  # equal je -> jne
    # OPB 00313F80
    ("m-oa-opbje1", "opb-nul1",     0x313FA8, 0x74, 0x75),  # rsi je -> jne
    ("m-oa-opbje2", "opb-nul2",     0x313FAD, 0x74, 0x75),  # rax je -> jne
    ("m-oa-opb48",  "opb-ok",       0x313FB3, 0x48, 0x4C),  # lea tmp +4
    ("m-oa-opbst",  "opb-ok",       0x313FCC, 0x48, 0x50),  # movss tmp +8
    # OF60 00313F60
    ("m-oa-f60rel", "of60-ret",     0x313F61, 0xBB, 0xBF),  # jmp N7C20 +4
    # OSUB 0026E350
    ("m-oa-osubje", "osub-ok",      0x26E372, 0x74, 0x75),  # table je -> jne
    ("m-oa-osubjs", "osub-neg",     0x26E388, 0x78, 0x79),  # ax js -> jns
    ("m-oa-osubr8", "osub-ok",      0x26E379, 0x01, 0x02),  # flag arg 1 -> 2
    # MABESP 003588B0
    ("m-oa-mbshr14", "mabesp-bank", 0x3588CF, 0x14, 0x15),  # bank shr 0x14->0x15
    ("m-oa-mbshr10", "mabesp-sel5", 0x3588D2, 0x10, 0x11),  # sel shr 0x10->0x11
    ("m-oa-mb7ff",  "mabesp-bank",  0x3588D5, 0xFF, 0xFE),  # bank &0x7FF->&0x7FE
    ("m-oa-mbmask", "mabesp-sel5",  0x3588DB, 0x0F, 0x0B),  # sel &0xF -> &0xB
    ("m-oa-mbcmp5", "mabesp-sel5",  0x3588E1, 0x05, 0x06),  # sel cmp 5 -> 6
    ("m-oa-mb20",   "mabesp-ok",    0x3588FC, 0x20, 0x24),  # cap d+0x20 -> +0x24
    ("m-oa-mb10",   "mabesp-ok",    0x358902, 0x01, 0x02),  # flag &1 -> &2
    ("m-oa-mbent",  "mabesp-ok",    0x35890C, 0xD9, 0x99),  # entry scale 8 -> 4
    ("m-oa-mb16",   "mabesp-bank",  0x358916, 0x16, 0x18),  # bank w+0x16 -> +0x18
    # DE100 0026E100
    ("m-oa-dezx",   "de100-on",     0x26E10B, 0xC2, 0xC1),  # movzx dx -> cx
    ("m-oa-decmov", "de100-on",     0x26E118, 0x45, 0x44),  # cmovne -> cmove
    # AGENTQ 00318CA0
    ("m-oa-aqje",   "agq-pos",      0x318CB1, 0x74, 0x75),  # table je -> jne
    ("m-oa-aqcwde", "agq-neg",      0x318CBE, 0x98, 0x90),  # cwde -> nop
    ("m-oa-aqrel",  "agq-pos",      0x318CBA, 0x22, 0x26),  # call N315E0 +4
]


def differs(a, b):
    out = []
    for k in ("trace", "rets", "ends", "faults"):
        if a[k] != b[k]:
            out.append(k)
    if a["mem"] != b["mem"]:
        out.append("mem")
    return out


def run_case(name, case, raw, secs):
    w = World(case, raw, secs)
    w.run()
    native = w.obs()
    model = run_model(case, raw, secs)
    return native, model, differs(native, model)


def main():
    raw, secs = load_image()
    cs = cases()
    fails = {}
    for name in sorted(cs):
        native, model, diff = run_case(name, cs[name], raw, secs)
        if diff:
            fails[name] = diff
    print("functional: %d/%d" % (len(cs) - len(fails), len(cs)))
    for name, diff in sorted(fails.items()):
        print("  FAIL %s: %s" % (name, diff))
    mkilled, msurv = [], []
    for mname, cname, addr, orig, mut in MUTS:
        base = dict(cs[cname])
        ob = img_rd(raw, secs, addr, 1)[0]
        assert ob == orig, \
            "%s: byte %x is %02x not %02x" % (mname, addr, ob, orig)
        base["patch_bytes"] = [(addr, bytes([mut]))]
        native, model, diff = run_case(mname, base, raw, secs)
        if diff:
            mkilled.append(mname)
        else:
            msurv.append(mname)
    print("mutants: %d/%d killed" % (len(mkilled), len(MUTS)))
    for mname in msurv:
        print("  SURVIVED %s" % mname)
    res = {"functional_total": len(cs),
           "functional_pass": len(cs) - len(fails),
           "functional_fail": sorted(fails),
           "mutants_total": len(MUTS),
           "mutants_killed": len(mkilled),
           "mutants_survived": msurv}
    with open(RESULT, "w") as f:
        json.dump(res, f, indent=2, sort_keys=True)
    sys.exit(1 if (fails or msurv) else 0)


if __name__ == "__main__":
    main()
