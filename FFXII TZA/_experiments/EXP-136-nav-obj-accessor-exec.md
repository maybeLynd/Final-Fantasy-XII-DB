---
experiment: EXP-136
title: nav object-accessor execution — the EXP-135 scripted leaf
  family promoted to real bodies: OBJD/A6A0/O3FW/O2FW/DA710/O1F/
  O1F2/O1F3/OVF/OPA/OPB/OF60/OSUB/MABESP/DE100/AGENTQ executed
  real, leaving seven one-hop scripted boundaries
contract: none — consumer anchor; no reciprocal contract names this
  experiment, so findings adoption is routed via REQ-OPUS
method: B
live_game: false
tool: evidence/nav-obj-accessor-exec/check.py
---
# EXP-136 — nav-obj-accessor-exec

**Status:** complete · **339/339 functional cases, 263/263 mutants,
stable across three processes**
**Evidence:** `evidence/nav-obj-accessor-exec/` (`check.py`,
`bodies.json`, `gen_bodies.py`, `result.json`)
**EXE:** `FFXII_TZA.exe` sha256 `73461d08…721f8` · image base `0x120000`

## Objective

The claimed slice was the EXP-135 scripted leaf set — the
object-accessor and subsystem-leaf family (~1 KB total) that GATE,
GFILT, the record writers, PVAL and BLKCHK call through entry
intercepts. All fourteen are now real bodies; every EXP-135 case was
re-fixtured to carry real object/pointer-record layouts (handles now
carry a `q[h+0x30]` object pointer; objects carry the `b[+3]` variant
byte, `q[+0xB8]`/`q[+0xC0]` record spine and `+0x138`/`+0xF0` chains),
and 64 direct cases cover each body's variants, nulls and fault
paths. Seven deeper calls stay scripted.

| VA | role | execution |
|---|---|---|
| `00263E30` | OBJD — `rax = q[h+0x30]` | **real** (5 B, 2 insns) |
| `002646A0` | A6A0 — `q[+0xC0]`→`q[+0x138]` chain | **real** (32 B, 10 insns) |
| `002646C0` | O3FW — variant dword/float copy+add | **real** (141 B, 40 insns) |
| `00265090` | O2FW — `0x60` gate → DA710 | **real** (27 B, 8 insns) |
| `003DA710` | DA710 — two-dword out writer | **real** (21 B, 9 insns) |
| `00265200` | O1F — v1 `f[qB8+0x38]` / v3 `f[qB8+0xA8]` | **real** (55 B, 16 insns) |
| `00263940` | O1F2 — v1 `f[qB8+0x68]` / v3 `fC0*f24` | **real** (55 B, 15 insns) |
| `00265830` | O1F3 — `0x60` → `f[q[qB8+0xF0]+0x24]` | **real** (34 B, 10 insns) |
| `002E9FE0` | OVF — `0x60` → c0/d164/b10/b11 flag walk | **real** (73 B, 26 insns) |
| `00314EB0` | OPA — c0→138 class/`+0x119` compare | **real** (118 B, 34 insns) |
| `00313F80` | OPB — A6A0 pair → N14F50 → opt store | **real** (115 B, 34 insns) |
| `00313F60` | OF60 — `jmp 00377C20` thunk | **real** (5 B, 1 insn) |
| `0026E350` | OSUB — two-stage word query | **real** (109 B, 33 insns) |
| `003588B0` | MABESP — bank/sel/gen handle decode | **real** (143 B, 46 insns) |
| `0026E100` | DE100 — arg reshuffle → N31400 | **real** (35 B, 8 insns) |
| `00318CA0` | AGENTQ — root → N315E0 → `cwde` | **real** (44 B, 14 insns) |

Plus the whole EXP-130/131/132/133/134/135 trees re-executed (GATE,
GTAB, MABE, GCHK, OCLS, LHELP, S3W, S2W, CDST, CDZ0, CF90, GPC, GSC,
GPT, GSEG, GFILT, OTHUNK, PVAL, MCPY, ROTX, DE6A0, LQUERY, BMASK,
DIST, CAPT0, CAPT1, CPSEG, TRIGD, CAPV, RDEC, TMS, TAT2, PATHW,
BLKCHK, AWRAP, MLOAD, RBUILD, ROTCOL, MXV, MXVW, CTHUNK, STHUNK,
QWALK, WWRAP, GGRID, ROOTL, TTEST, ETHUNK, ECLASS, SEGT, BASE, PRED,
VSUB, VADD, VSCALE, NCOPY, NORM, XPROD, THUNKF, CHKCK — 76 real
bodies total).

Scripted boundaries (traced, NOT executed):

- `00377C20` N7C20 — OF60's bitfield lookup; `eax` per case.
- `00314F50` N14F50 — OPB's inner pair compare; `eax` + out float.
- `00263FF0` N63FF0 — MABESP table select; `rax` per case.
- `00231900` N31900 / `00231820` N31820 — OSUB stage-1 word query
  (`ax` per case) and stage-2 lookup (ret dead, traced).
- `00231400` N31400 — DE100's dispatcher; `eax` per case.
- `002315E0` N315E0 — AGENTQ's query; `eax` per case (caller
  `cwde`s).
- CRT imports via real IAT/thunks: `sqrtf`, `atan2f`, `memset`,
  `_fdclass`, `cosf`, `sinf`, `_isnan`, `_finite` — planted host
  trampolines (import-dir proven).

## Verified behavior contract

- `OBJD(h)`: `rax = q[h+0x30]`; no null guard (h=0 → fault at
  `0x263E30`, addr `0x30`).
- `O3FW(obj, p1, p2, p3)`: `obj==0` → no writes. `v = (b[obj+3]>>5)-1`:
  `v==0` copies `d[qB8+0/4/8]`; `v==2` copies then, iff
  `b[qB8+0x107]&1`, `addss`es `f[qB8+0x40/44/48]` into the outs; else
  zeroes all three outs.
- `O2FW(obj, p1, p2)`: `(b[obj+3]&0xE0)==0x60` → tail `DA710(qB8+0x50)`;
  DA710 writes `d[rc]→[rdx]`, `d[rc+4]→[r8]` for non-null outs only.
- `O1F(obj)`: `obj==0 → 0`; v1 `f[qB8+0x38]`; v3 `f[qB8+0xA8]`; else 0
  (returned in `xmm0`).
- `O1F2(obj)`: no null guard — `b[obj+3]` read faults; v1
  `f[qB8+0x68]`; v3 `f[qB8+0xC0]*f[qB8+0x24]`; else 0.
- `O1F3(obj)`: no null guard; `(b[obj+3]&0xE0)==0x60` →
  `f[q[qB8+0xF0]+0x24]`; else 0.
- `OVF(obj)`: `(b[obj+3]&0xE0)!=0x60 → 1`; else `c=q[obj+0xC0]`,
  `c==0 → 0`, `d[c+0x164]!=0 → 0`, then `b[c+0x11]&0x20 ?
  (b[c+0x10]&3)==3 : (b[c+0x10]&0xB)==0xB`, and finally
  `(b[c+0x11]&6)==6` → ret 1 via the `mov eax,1` fallthrough.
- `OPA(a, b)`: `r10 = a? q[q[a+0xC0]+0x138] : 0`,
  `r9 = b? q[q[b+0xC0]+0x138] : 0`; either 0 → 0. `b[r10+6] !=
  b[r9+6] → 0`; `b[r10+0x119]==0 → 1`; `== b[r9+0x119] → 0`; else 1.
- `OPB(a, b, outp)`: `rsi = A6A0(a)`, `rax = A6A0(b)`; either 0 → 0.
  `r = N14F50(rsi, rax, 0, &tmp)`; `outp!=0 → f[outp] = f[tmp]`; ret r.
- `OF60(obj)`: tail `jmp 00377C20` (scripted).
- `OSUB(vec)`: `q[0x209A670]==0 → -1`; `t = q[0x209A678]`, `t==0 →
  -1`; `ax = N31900(t, vec, 1)`, `ax<0 → -1`; `N31820(t, vec, ax)`;
  ret 0.
- `MABESP(h)`: `h==0 → 0`; `bank=(h>>0x14)&0x7FF`, `sel=(h>>0x10)&0xF`,
  `sel>=5 → 0`; `T=N63FF0(sel)`; `arr=q[T+8]` (no T guard — T==0
  faults at `0x3588EB`); `arr==0 → 0`, `q[T]==0 → 0`,
  `gen>=d[T+0x20] → 0`, `b[T+0x10]&1==0 → 0`, `gen>=d[arr] → 0`;
  `e = q[arr+8+gen*8]`, `e==0 → 0`; `w[e+0x16]==bank ? e : 0`.
- `DE100(tab_obj, a1, a2)`: `r9d=a2`; `r8d = a1&0xFFFF`;
  `rdx = tab_obj`; `rcx = q[0x209A670]!=0 ? q[0x209A678] : 0`; tail
  `jmp 00231400`.
- `AGENTQ(obj, out, a3, a4)`: `rcx = q[0x2EC1378]`, `==0 → -1`; else
  `cwde(N315E0(rcx, obj, out, a4))`.

## Findings

1. **The "leaf" census was inflated by packed neighbors.** An early
   span scan ran past each `ret` into the next function — OPB read as
   a 54-callee root; it is 115 B with three call sites. All spans
   are now trimmed to real control-flow extents (16 bodies,
   1012 bytes).
2. **`rets` compares `rax` only — xmm0-returning leaves need
   consumers.** O1F/O1F2/O1F3 field mutants are invisible at their
   own `ret`; they discriminate through S3W's `d[out+0x18]` store
   (watched memory), GATE's `flags&0x40` accept-path y-cap compare
   and the `flags&0x10` arm's `O1F3==0` test. Four direct mutant
   repoints plus three new cases (`s3w-v1`, `gate-acc3v1`,
   `gate-acc3m`, `opa-b67`) close the gap.
3. **MABESP has no table-null guard.** `arr = q[T+8]` at `0x3588EB`
   runs unconditionally after `N63FF0` — a null table faults there
   rather than returning 0; only `arr`, `q[T]`, capacity, flag and
   generation checks gate the entry read.
4. **OPA's class compare is asymmetric.** `b[r10+0x119]` (a's flag
   byte) decides the `+0x119` equality arm: `a.119==0 → accept`,
   `a.119==b.119 → reject`, else accept — b's flag alone never
   decides.
5. **Fault stop-ordering is part of the contract.** O3FW's variant
   byte lands in `r10d`, so a fault mid-copy leaves the caller's
   `rax` live — the model must halt at the faulted instruction and
   preserve `_rax` exactly; continuing past a fault rewrites rax
   and desyncs `rets`.
6. **Direct cases now execute the full leaf set inside GATE.** The
   24 pv-* and 46 gate-* fixtures plant real `q[h+0x30]` handle
   pointers, `b[+3]` variant bytes and `qB8`/`qC0`/`+0x138`/`+0xF0`
   record spines — the collectors emit raw handles that real OBJD
   dereferences, so record-layout bugs surface as native-visible
   faults, not silent queue misses.

## Method

Same as EXP-133/134/135: Unicorn world vs Python model over planted
heap/BSS fixtures; trace = scripted-boundary hits; mem = watched
bytes; rets/faults/ends byte-compared. Mutants patch a single
shipped byte (old-byte asserted) and must diverge observable state.

## Scope boundary

The seven remaining scripted leaves (N7C20, N14F50, N63FF0, N31900,
N31820, N31400, N315E0) are one-hop boundaries into the nav
`0x23xxxx`/`0x31xxxx` query family and the `0x377xxx` bitfield
lookup — each awaits its own package. Fixture-backed parity remains
MODEL-PROVEN; hand-built records do not become replay authority.
