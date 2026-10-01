---
experiment: EXP-137
title: nav subsystem-leaf execution — the EXP-136 scripted leaf
  family promoted to real bodies: N7C20/N48F0/N63FF0/DAE00/
  N33050/N30A40/N31890/N31820/N31900/N33110/N315E0/N31400/
  N2F830/N2F8B0/N4E10/N14F50 executed real, leaving five
  one-hop scripted boundaries
contract: none — consumer anchor; no reciprocal contract names this
  experiment, so findings adoption is routed via REQ-OPUS
method: B
live_game: false
tool: evidence/nav-subsystem-leaf-exec/check.py
---
# EXP-137 — nav-subsystem-leaf-exec

**Status:** complete · **449/449 functional cases, 385/385 mutants,
stable across three processes**
**Evidence:** `evidence/nav-subsystem-leaf-exec/` (`check.py`,
`bodies.json`, `gen_bodies.py`, `result.json`)
**EXE:** `FFXII_TZA.exe` sha256 `73461d08…721f8` · image base `0x120000`

## Objective

The claimed slice was the EXP-136 scripted leaf set — the seven
remaining entry-intercepts under the now-real nav path-validation
stack (~3.4 KB by first census). The seven opened into sixteen real
bodies (3,778 B): each leaf's own callees that stayed inside the
slice (N48F0 under N7C20, N33050/N30A40/N31890 under N31900,
N33110/N2F830/N2F8B0/N30A40 under N31400, N4E10/DAE00 under N14F50)
executed real with them, while five deeper calls (EF2B0, F4F0, F430,
EB0, D5A0) remain scripted boundaries. Every EXP-136 case was
re-fixtured — the nav-grid table roots, cell/edge/sub-record arrays,
EF2/T2AD objects and the CLST mask pairs are now planted heap
structures the real bodies dereference — and 106 direct cases cover
each body's variants, nulls and fault paths.

| VA | role | execution |
|---|---|---|
| `00377C20` | N7C20 — EF2 word → T2AD bitfield lookup | **real** (78 B, 23 insns) |
| `003148F0` | N48F0 — EF2B0 init ptr → `d[+0x1044]` clamp | **real** (27 B, 8 insns) |
| `00263FF0` | N63FF0 — `T3B + sx32(sel)*0x288` | **real** (21 B, 5 insns) |
| `003DAE00` | DAE00 — null-safe three-dword copy | **real** (61 B, 31 insns) |
| `00233050` | N33050 — staggered-grid cell resolve | **real** (144 B, 59 insns) |
| `00230A40` | N30A40 — CLST mask-mux predicate | **real** (279 B, 79 insns) |
| `00231890` | N31890 — edge y-projection → `xmm0` | **real** (97 B, 23 insns) |
| `00231820` | N31820 — y-projection store variant | **real** (105 B, 25 insns) |
| `00231900` | N31900 — best-edge scan → `ax` | **real** (393 B, 96 insns) |
| `00233110` | N33110 — cell edge scan → `w[out+0x52]` | **real** (299 B, 76 insns) |
| `002315E0` | N315E0 — ctx → F430 → `sx16` word | **real** (176 B, 38 insns) |
| `00231400` | N31400 — is-point-free dispatcher | **real** (474 B, 116 insns) |
| `0022F830` | N2F830 — flag-bit cell dispatch `call q[ctx]` | **real** (120 B, 38 insns) |
| `0022F8B0` | N2F8B0 — sub-record point-test loop → EB0 | **real** (270 B, 85 insns) |
| `00314E10` | N4E10 — material blend selector → `xmm0` | **real** (154 B, 50 insns) |
| `00314F50` | N14F50 — pair compare / capsule path | **real** (1080 B, 210 insns) |

Plus the whole EXP-130/131/132/133/134/135/136 trees re-executed
(GATE, GTAB, MABE, GCHK, OCLS, LHELP, S3W, S2W, CDST, CDZ0, CF90,
GPC, GSC, GPT, GSEG, GFILT, OTHUNK, PVAL, MCPY, ROTX, DE6A0,
LQUERY, BMASK, DIST, CAPT0, CAPT1, CPSEG, TRIGD, CAPV, RDEC, TMS,
TAT2, PATHW, BLKCHK, AWRAP, MLOAD, RBUILD, ROTCOL, MXV, MXVW,
CTHUNK, STHUNK, QWALK, WWRAP, GGRID, ROOTL, TTEST, ETHUNK, ECLASS,
SEGT, BASE, PRED, VSUB, VADD, VSCALE, NCOPY, NORM, XPROD, THUNKF,
CHKCK, OBJD, A6A0, O3FW, O2FW, DA710, O1F, O1F2, O1F3, OVF, OPA,
OPB, OF60, OSUB, MABESP, DE100, AGENTQ — 92 real bodies total).

Scripted boundaries (traced, NOT executed):

- `002EF2B0` EF2B0 — N48F0's init-ptr call; `rax` per case.
- `002324F0` F4F0 — N31900/N33110 edge predicate; `eax` per case
  (sign-tested).
- `0022F430` F430 — N315E0's ctx writer; `w[ctx+0x44]` per case.
- `00381EB0` EB0 — N2F8B0's point-in-subrec test; `eax` per case.
- `003DA5A0` D5A0 — N14F50's capsule distance; `xmm0` + 16 B out
  per case.
- CRT imports via real IAT/thunks: `sqrtf`, `atan2f`, `memset`,
  `_fdclass`, `cosf`, `sinf`, `_isnan`, `_finite` — planted host
  trampolines (import-dir proven).

## Verified behavior contract

- `N48F0()`: `eax = d[EF2B0()+0x1044]`; `<0 → 0`.
- `N7C20()`: `eax = N48F0()`; `r8 = q[0x2ADD100]`; `r8==0` or
  `eax >= d[r8+4] → 0`; else `(b[r8+3*eax+9]<<8 | b[r8+3*eax+8])
  >> 15`.
- `N63FF0(sel)`: `rax = 0x2098E10 + sx32(sel)*0x288` (no guard).
- `DAE00(src, dst)`: `src==0 → ret`; else `d[dst+0/4/8] =
  d[src+0x30/0x34/0x38]`.
- `N33050(tab, vec)`: `gx = cvtdq(d[tab+0x38])+f[vec]`,
  `gz = cvtdq(d[tab+0x3C])+f[vec+8]`; either `<0 → 0xFFFF`;
  `col = cvtt(gx)/d[q[tab]+0x10]`; odd col subtracts
  `trunc(d[+0x14]/2)` from row before `row = cvtt(gz)/ch`;
  either `idiv` on a zero cell-size traps (`#DE` at `0x233086` /
  `0x2330A1`); bounds `→ 0xFFFF`; ret `col + row*w`.
- `N30A40(tab, edge, sel)`: `edge<0 → 0`; `F = d[q[tab+0x10] +
  edge*32 + 0xC]`; two CLST mask pairs at slots
  `(F>>0xD)&0x1F` and `((F>>3)&0xF)+0x40` merge
  `ecx = (m1&m0 | F&~m0)&~n0 | (n1&n0)`; `ecx&7 → 0`;
  `sel ∈ {0,1,2,3,5}` tests bit `0x17/0x19/0x1A/0x1B/0x18`
  inverted; else `1`.
- `N31890(tab, vec, idx)` / `N31820(tab, vec, idx)`: `idx<0 →
  f[vec+4]`; `rec = q[tab+0x10] + sx16(idx)*32`;
  `f[rec+4] <= f[0x8C5B2C]` (0.001f) `→ f[vec+4]`; else the edge
  y-projection `((vtx.z−vec.z)·d[rec+0x14] + (vtx.x−vec.x)·
  d[rec+0x10])/f[rec+4] + vtx.y`. N31890 returns f32 bits in
  `xmm0`; N31820 stores back to `f[vec+4]` in both arms.
- `N31900(tab, vec, sel)`: cell = `N33050`; `w[out]=0xFFFF` then
  scans the cell's edge range — `>0x3FFF` skipped, `N30A40` must
  pass, `F4F0(tab, edge, ctx) < 0` selects; returns the edge that
  minimizes `N31890`'s projection while `f4f` stays negative;
  `0xFFFF` if none.
- `N33110(tab, out, cell, vec)`: `w[out+0x52] = 0xFFFF`; `tab==0`
  or `q[tab]==0 → ret` (rax `0xFFFFFFFF`); `cnt==0 → ret` (rax
  `cell+1` via `cdqe`); per edge: `>0x3FFF` skip → `N30A40` gate
  → `F4F0<0` writes `w[out+0x52]=edge` and stops.
- `N315E0(tab, va, vb)`: `tab==0` or `q[tab]==0 → 0xFFFF`; builds
  a ctx at `rsp`-relative offsets (fn `0x22D4B0`, two 16 B vector
  copies, `w[+0x52]=0xFFFF`); `F430(tab, ctx)` writes
  `w[ctx+0x44]`; returns `sx16` of that word.
- `N31400(tab, vec, sel, mode)`: `w[out+0x50]=sel` → `N33050` →
  `N33110` → edge `w[out+0x52]` sign-bit `→ 0`; mode!=0 arms a
  y-gate (`y1 > f[vec+4] → 0`); then copies `vec` to a 16 B buf,
  inline re-resolves the cell (`x&1` stagger, second `idiv` pair,
  `col|row<0 or >=w/h → 0`), builds ctx `{fn=N2F8B0, tab, cell,
  &v16, fl=6}` → `N2F830`; `eax = 1` iff `d[ctx+0x20]==0`.
- `N2F830(ctx)`: for `b ∈ 0..3` with `b[ctx+0x16]&(1<<b)`:
  `cell' = w[ctx+0x10] + b*sx16(w[tab+0x40]+1)`; writes
  `w[ctx+0x12]`/`w[ctx+0x14]` from the `q[tab+0x20]` range words;
  `call q[ctx]` (N2F8B0 in every observed ctx). `rax` at exit is
  the callee's, the range pointer, or `dx+1` — preserved per
  site.
- `N2F8B0(ctx)`: `d[ctx+0x20]!=0 → ret`; loops `i <
  sx16(w[ctx+0x14])` (re-read each pass): `idx = w[q[tab+0x28] +
  (sx16(w[ctx+0x12])+i)*2]`; `(idx−0x4000)&0xFFFF <= 0xFFF →
  sub = q[tab+0x18] + (idx−0x4000)*144`; `d[ctx+0x24]` arm merges
  the BPTAB `((d[sub+4]>>0xD)&0x1F)+0x20` mask pair, skipped when
  the merged `r8d` has bit 31; `EB0(sub, q[ctx+0x18])!=0 →
  d[ctx+0x20]=1`, stop.
- `N4E10(a, b, x2, x3)`: `t = x3/(x2+x3)` (`den==0 → t=den`);
  material mux over `d[a/b + 0x110 | 0x114]` — masks OR'd, common
  high bits `r9`, cleared bits `ec`; both sides present after
  masking: shared `r9` bit `→ 0.0`, asymmetric `→ 0.0/1.0` by
  which side; `x2<0 → 0`, `x3<0 → 1.0`. Returns f32 bits.
- `N14F50(a, b, mode, outp)`: `a==0 → 0`; guards on
  `b[b+0x119]`/`b[b+0xB7]`/`b[a+0x119]`/`b[a+0xB7]` `→ 0`;
  `mode!=0` runs `DAE00` twice into stack bufs then `D5A0`
  capsule distance (`dist<0` = hit); `t = N4E10(a, b, x8, x9)`.
  `mode==0`: `f[outp]=t` → ret `2/3/4` by flag arm. `mode!=0`:
  bumps `+0xEC` counters and pushes the two objects' positions
  apart on hit → ret `1`.

## Findings

1. **The leaf census under-counted the real set.** Each of the
   seven promoted leaves opened into internal callees that stayed
   inside the slice — N7C20→N48F0, N31900→{N33050, N30A40,
   N31890}, N31400→{N33110, N2F830, N2F8B0}, N14F50→{N4E10,
   DAE00}. Sixteen bodies execute real; only five second-level
   calls (EF2B0, F4F0, F430, EB0, D5A0) stay scripted — the
   `0x2EF2B0`/`0x2F050`/`0x316480`/`0x316670` deeper roots each
   fan out past package scope.
2. **Packed siblings inflated two first-pass spans.** N31900
   read as 1344 B / N14F50 as 1184 B because a span scan ran past
   `ret` into the next function; trimmed extents are 393 B and
   1080 B (`0x231A90`/`0x315390` siblings excluded).
3. **`rax` at exit is load-bearing.** `rets` compares `rax` at
   every exit including faults: N31400's prologue leaves the
   `__security_cookie ^ rsp` residual live through every fault
   path; N33050's `idiv` traps carry the `cvtt` dividend; N33110
   exits `0xFFFFFFFF` (tab-null), `cell+1` (`cdqe`, cnt==0), the
   range pointer, or the callee's ret; N2F8B0's loop bottom
   `movsx eax, word[ctx+0x14]` re-latches `cnt`. Fourteen initial
   case failures were all `rax`-bookkeeping, zero semantic
   divergence.
4. **N33050 has no table-null guard and two trap sites.**
   `q[tab]==0` faults on `idiv [r8+0x10]` (reads at `+0x10`/`+0x14`
   run unconditionally); zero cell width/height traps `#DE` at
   `0x233086`/`0x2330A1` — modeled as `"trap"` faults with the
   dividend in `rax`.
5. **N14F50's mode is a path select, not a flag.** `mode==0`
   writes `t` to `outp` and returns `2/3/4`; `mode!=0` runs the
   capsule-distance hit test (`D5A0 < 0`) and, on hit, adds
   `+0xEC` counters and pushes both objects' `+0x30..0x38`
   positions apart by `±t·(B−A)/2` — the caller-visible
   difference between OPB's `f[outp]` consumer and PVAL's
   mode-1/3 arms.
6. **Equivalent and unobservable mutants were retired, not
   counted.** One byte (`movsx→movzx` in N31890 at `0x2318A0`)
   is unobservable because the preceding `test r8w; js` exits on
   every bit-15 index — removed from the table rather than
   claimed. Every remaining mutant's site byte is asserted
   against the shipped image and discriminated by a case where
   the byte change reaches a watched observable.
7. **Fixture overlap is a parity hazard.** `T2ADA =
   HEAP+0x6A000` landed inside `EF2P`'s `0x1080`-byte object, so
   the `ef2v` plant was silently overwritten — moved to
   `HEAP+0x74000`. Heap plants need span checks, not just base
   addresses.

## Method

Same as EXP-133/134/135/136: Unicorn world vs Python model over
planted heap/BSS fixtures; trace = scripted-boundary hits; mem =
watched bytes; rets/faults/ends byte-compared. Mutants patch a
single shipped byte (old-byte asserted) and must diverge
observable state. The `call q[ctx]` indirect dispatch in N2F830
executes natively (the planted fn is real N2F8B0 code); an
unmapped fn records a `memf` fetch fault.

## Scope boundary

The five remaining scripted boundaries (EF2B0, F4F0, F430, EB0,
D5A0) are one-hop entries into the `0x2Exxxx` object-init,
`0x22xxxx`/`0x38xxxx` geometry and `0x3DAxxx` math families —
each awaits its own package. Fixture-backed parity remains
MODEL-PROVEN; hand-built records do not become replay authority.
