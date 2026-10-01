---
experiment: EXP-135
title: nav gate-walk execution — GATE 003357B0 corridor gate
  executed real over GTAB/MABE/GCHK/OCLS/LHELP/S3W/S2W/CDST/CDZ0/
  CF90/GPC/GSC/GPT/GSEG/GFILT plus the scripted subsystem leaves
  OBJD/O3FW/O2FW/O1F/O1F2/O1F3/OPA/OPB/OF60/OVF/OSUB/MABESP
contract: none — consumer anchor; no reciprocal contract names this
  experiment, so findings adoption is routed via REQ-OPUS
method: B
live_game: false
tool: evidence/nav-gate-walk-exec/check.py
---
# EXP-135 — nav-gate-walk-exec

**Status:** complete · **275/275 functional cases, 201/201 mutants,
stable across three processes**
**Evidence:** `evidence/nav-gate-walk-exec/` (`check.py`,
`bodies.json`, `gen_bodies.py`, `result.json`)
**EXE:** `FFXII_TZA.exe` sha256 `73461d08…721f8` · image base `0x120000`

## Objective

The claimed slice was `003357B0` (GATE) — the last scripted
boundary inside EXP-134's path-validator consumer — a 943-byte
corridor gate combining the object-pool lookup, a self validity
check, a nav-grid spatial query (point or segment), and a
per-candidate accept walk over subsystem leaves. All 24 pv-* cases
from EXP-134 were re-pointed at real GATE fixtures (the prior
package's scripted `gatrets` were removed entirely), and 46 new
direct cases cover GATE itself plus each leaf.

| VA | role | execution |
|---|---|---|
| `003357B0` | GATE — corridor gate / object-pool walk | **real** (943 B, 232 insns) |
| `00236820` | GTAB — pool table lookup `d[idx*0xF50+8]` | **real** (37 B, 12 insns) |
| `0031ABE0` | MABE — `b[0x2089340]&0x10` flag gate | **real** (21 B, 5 insns) |
| `002EA7F0` | GCHK — object validity guard chain | **real** (117 B, 35 insns) |
| `00263C20` | OCLS — class byte `b[+0xE]&0xF` | **real** (16 B, 7 insns) |
| `00335760` | LHELP — accept helper → OCLS class | **real** (66 B, 22 insns) |
| `002FB500` | S3W — O3FW+O2FW+O1F record writer | **real** (106 B, 33 insns) |
| `002FB340` | S2W — O3FW + maxss(O2FW) writer | **real** (98 B, 24 insns) |
| `00469060` | CDST — TRIGD+rad vs dxz² (setae) | **real** (79 B, 22 insns) |
| `00468D10` | CDZ0 — rad+t.f10 vs dxz² (seta) | **real** (53 B, 14 insns) |
| `00468F90` | CF90 — CPSEG+TRIGD+sqrtf capsule (seta) | **real** (205 B, 48 insns) |
| `00391A30` | GPC — point+rad cell collector | **real** (721 B, 176 insns) |
| `00391D90` | GSC — segment cell collector | **real** (851 B, 174 insns) |
| `00391D10` | GPT — point-query wrapper → GPC+GFILT | **real** (121 B, 29 insns) |
| `003920F0` | GSEG — segment wrapper → GSC+GFILT | **real** (142 B, 39 insns) |
| `003911D0` | GFILT — handle-array acceptance filter | **real** (263 B, 80 insns) |
| `0032A790` | OTHUNK — `jmp 0026E350` OSUB thunk | **real** (5 B, 1 insn) |

Plus the whole EXP-130/131/132/133/134 trees re-executed (PVAL,
MCPY, ROTX, DE6A0, LQUERY, BMASK, DIST, CAPT0, CAPT1, CPSEG,
TRIGD, CAPV, RDEC, TMS, TAT2, PATHW, BLKCHK, AWRAP, MLOAD, RBUILD,
ROTCOL, MXV, MXVW, CTHUNK, STHUNK, QWALK, WWRAP, GGRID, ROOTL,
TTEST, ETHUNK, ECLASS, SEGT, BASE, PRED, VSUB, VADD, VSCALE, NCOPY,
NORM, XPROD, THUNKF, CHKCK — identical spans/hashes to EXP-134).

Scripted boundaries (traced, NOT executed):

- `00263E30` OBJD — handle → object decode; `eax` per case.
- `002646C0` O3FW / `00265090` O2FW / `00265200` O1F /
  `00263940` O1F2 / `00265830` O1F3 — subsystem record field
  accessors; planted out-writes / `xmm0` per case.
- `00314EB0` OPA / `00313F80` OPB / `00313F60` OF60 /
  `002E9FE0` OVF / `0026E350` OSUB — object/subsystem predicates;
  `eax` per case. OSUB is reached through the real `0032A790`
  thunk from GATE's `0x3359C8` call.
- `003588B0` MABESP — MABE slow-path handle resolve (reached via
  MABE's `jne`); `eax` per case.
- `0026E100` DE100 / `00318CA0` AGENTQ — unchanged from EXP-134.
- CRT imports via real IAT/thunks: `sqrtf`, `atan2f`, `memset`,
  `_fdclass`, `cosf`, `sinf`, `_isnan`, `_finite` — planted host
  trampolines (import-dir proven).

## Verified behavior contract

`GATE(rcx=posA, rdx=posB, r9=ctx, xmm2=rad, [entry+0x28]=excl,
[entry+0x30]=flags)` — frame `rbp = entry-rsp − 0x148`,
`rsp = entry-rsp − 0x248`:

1. `idx = b[ctx+0xEA9]`; `pobj = GTAB(idx)`;
   `self = MABE(d[pobj+8])` — MABE returns `MABESP(handle)` when
   `b[0x2089340]&0x10`, else `0`.
2. `flags = d[rbp+0x178]` (callee stack arg). `flags&0x20 == 0` →
   `GCHK(self)`; `0 → ret 0`. GCHK guard chain: `obj!=0`,
   `b[+0x18]!=1`, `q[+0xC0]!=0`, `b[c0+0x14F]&1==0`,
   `q[c0+0x138]!=0`, `f[c138+0xF0]>0`, `b[+8]&8`, then `OVF(obj)` —
   nonzero accept; zero requires `b[obj+4]==3`.
3. Ordered `ucomiss` x/y/z on `posA`/`posB` (jp or jne → segment
   arm): equal → `GPT(&pq{posA,rad}, out, 0x20, r9f)`; else
   `GSEG(&sq{posA,posB,rad}, out, 0x20, r9f)` where
   `r9f = (~(flags>>4)&8)|0x14`. `n <= 0 → ret 0`.
4. Per-handle loop over `out[0..n)`: `obj = OBJD(h)`; `h==self` or
   `h==excl` → skip. `obj!=0` → e68 class filter: both
   `(b[e68+0x18]>>1)&7` — obj class 1 vs ctx class 4 → skip.
5. `flags&0x40` pre-filter: `b[ctx+0x1F4]!=3 && b[obj+0x1F4]==3` →
   `O3FW(q[obj+0x10] → F30)`, `V30={x,1,1,z}`+`OSUB(V30)`, then
   `f[F30+4] − d[rbp-0x2C] > O1F2(q[ctx+0x10]) → skip`.
6. Flag arms (only when `obj!=0`): `flags&2` → `LHELP(obj)==0` →
   `esi++`, next; `flags&4` → `LHELP(ctx)==0 && LHELP(obj)==0` →
   `esi++`, next; `flags&0x10` → `LHELP(obj)==0` →
   `O1F3(q[obj+0x10])==0 → esi++`, next either way; `flags&8` →
   `LHELP(ctx)!=LHELP(obj)` → skip, else `w[obj+0x714]==0x4021`
   required.
7. Accept path: `flags&0x40 && b[ctx+0x1F4]==3` →
   `O3FW(h→F70)`, `posA.y > O1F2(h)+f[F70+4]` → skip. `OPA(self,h)`
   — `0 → skip`. `r = OPB(self,h,&tmp)`: `(r-1)<=2 → esi++`, else
   `r12d++`.
8. Return `r12d!=0 ? 1 : (esi!=0 ? 2 : 0)`.

`LHELP(o)`: `o==0 → 0`; `p = q[o+0x698]`; `p==0 → 0`;
`b[p+5]!=1 → 0`; `cl = OCLS(q[o+0x10])`; `cl==3 → 0`;
`cl∈{1,2} → 1`; else `2`.

`GFILT(out, cnt, tmp, n, stk flags)`: per handle `obj=OBJD(h)`;
`flags&2 && obj==0 → skip`; `flags&4 && obj!=0` → `q[obj+0x698]==0`
skips, `d[p+0x64]|d[p+0x3C]` high bits set → `OF60(p)==0` skips;
`flags&8` → `GCHK(h)==0` skips. Survivors append to `out[]` (cap
`cnt`), return count.

`GPC(q, out, flag)` / `GSC(q, out, flag)`: read grid params from the
shared LQUERY BSS block; `memset` the record mask; per grid record
bit → handle `h`: `flag!=0` → `S3W(tmp,h)` + `CDST`/`CF90`; else
`S2W(tmp,h)` + `CDZ0`/strip+`d2` fallback. Accepted → `out[w++]`.

`S3W(out,obj)`: `O3FW(obj→out+0,+4,+8)`, `O2FW(obj→out+0x10,+0x14)`,
`d[out+0x18]=O1F(obj)`, then `d[out+4]=0`. `S2W(out,obj)`:
`O3FW(obj→out+0,+4,+8)`, `O2FW(obj→frame temps)`,
`d[out+4]=0`, `d[out+0x10]=maxss(f1,f2)` (also returned in xmm0).

`CDST(tmp,q)`: `(TRIGD(tmp,q)+d[q+0x10])² >= dxz²` → setae.
`CDZ0(q,tmp)`: `d[q+0x10]+f[tmp+0x10] > dxz²` → seta. `CF90(seg,tmp)`:
`CPSEG` closest point + `TRIGD` + `sqrtf` → seta.

## Findings

1. **Fixture records must not overlap.** `ob()` zero-fills a
   0x800-byte buffer; planting two GCHK record chains `0x100`
   apart let the second plant wipe the first's `q138`/`b14F`
   fields — GCHK failed before OVF with no trace, so GATE returned
   0 invisibly. Record plants now carry explicit sizes and the
   candidate chain sits `0x800` up.
2. **`ob()` slice-writes past its size silently append.** A `bEA9`
   field at `+0xEA9` on a default `0x800` object appended at the
   end instead — the mutant reading `ctx+0xEA9` saw `0` and was
   invisible. Any `ob()` field `≥ 0x800` now requires an explicit
   size argument.
3. **S2W/S3W zero `d[out+4]` after the O3FW write.** Both writers
   pass `out+4` to O3FW (y lands there) then overwrite it with `0`
   — the record format is `{x, 0, z, 0, …}`. S2W additionally
   stores `maxss` to `out+0x10`; S3W stores `O1F` to `out+0x18`.
4. **GATE's `flags&0x10` arm falls through on `LHELP!=0`.** The
   `continue` is inside the `LHELP(obj)==0` arm only — a nonzero
   LHELP proceeds to `flags&8`/accept, not the next candidate.
5. **GFILT `flags&4` skips zero `+0x698`.** A null `q[obj+0x698]`
   skips the candidate entirely; with both `p+0x64|p+0x3C` high
   bits clear the OF60 call is skipped too.
6. **The collector flags derive from the gate flags.**
   `r9f = (~(flags>>4)&8)|0x14` — gate `flags&0x40`-vs-`0x80`
   mutants change GFILT's `&8` GCHK arm through this remap, so
   flag mutants are observable even before the accept walk.
7. **Mutants on the gate-arg computation need populated walks.**
   `or10`/`and2`/`r9f0` sites sit in PVAL's flag/pointer math —
   they only diverge when a candidate actually reaches the
   affected flag arm or context field. Three new pv-* cases
   (`pv-flag6-pop`, `pv-flag6-m3`, `pv-gateptr` with a real
   `bEA9`) discriminate them.
8. **The `flags&0x40` pre-filter writes `V30 = {x, 1.0f, 1.0f, z}`**
   (dword `1.0f` at `+4` and `+0xC`, x/z from the O3FW'd sub
   record) and discards OSUB's return — it is a side-effect-only
   call inside the walk.

## Method

Same as EXP-133/134: Unicorn world vs Python model over planted
heap/BSS fixtures; trace = scripted-boundary hits; mem = watched
bytes; rets/faults/ends byte-compared. Mutants patch a single
shipped byte (old-byte asserted) and must diverge observable
state.

## Scope boundary

The scripted leaf set (OBJD, O3FW/O2FW/O1F/O1F2/O1F3, OPA, OPB,
OF60, OVF, OSUB, MABESP, DE100, AGENTQ) is the remaining
subsystem-accessor family — each is an entry-intercept awaiting
its own package. `pv-*` cases exercise GATE end-to-end through
real code; the leaf boundaries remain MODEL-PROVEN fixture
contracts, not native-authority semantics for those functions.
