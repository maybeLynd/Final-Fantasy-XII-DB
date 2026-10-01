---
experiment: EXP-138
title: nav residual-boundary execution — the five remaining scripted
  boundaries promoted to real bodies: EF2B0/F4F0/F430/EB0/D5A0 plus
  their whole geometry subtree executed real, leaving D0D0 and the
  f64 sqrt/acosf imports scripted
contract: none — consumer anchor; no reciprocal contract names this
  experiment, so findings adoption is routed via REQ-OPUS
method: B
live_game: false
tool: evidence/nav-residual-boundary-exec/check.py
---
# EXP-138 — nav-residual-boundary-exec

**Status:** complete · **449/449 functional cases, 384/384 mutants,
stable across three processes**
**Evidence:** `evidence/nav-residual-boundary-exec/` (`check.py`,
`bodies.json`, `gen_bodies.py`, `result.json`)
**EXE:** `FFXII_TZA.exe` sha256 `73461d08…721f8` · image base `0x120000`

## Objective

The claimed slice was EXP-137's five remaining scripted boundaries —
EF2B0, F4F0, F430, EB0, D5A0 (~4 KB by first census). The five opened
into twenty-one real bodies (~7 KB): the waypoint walker's planted
callback (`q[ctx+0x28]` = `0022D4B0`, written by N315E0), the
edge-scan geometry pair (E6D0 projected distance, CF50 winding test),
the seg-vs-shape dispatcher FA0 with its three unit-shape primitives
and plane helpers, the point-in-shape EB0 subtree, and D5A0's
anisotropic-metric helpers. Two calls stay scripted: `0022D0D0` (the
region query — its own ~10-body subtree is a future package) and the
CRT imports, which grew by two (f64 `sqrt` via thunk `00861F5C`/IAT
`0x8C2C60`, `acosf` via thunk `00861F56`/IAT `0x8C2C78`, both
import-dir proven). Existing cases were re-fixtured rather than
replaced: F430's walk terminates on planted `d0d0rets`/`d0d0o`
queues, and two cases now plant real triangle recs so the D4B0 claim
path (`w[ctx+0x44]=2`, `*B=Aout`) executes for the first time.

| VA | role | execution |
|---|---|---|
| `002EF640` | EF640 — `rax = 0x2164280` | **real** (8 B, 2 insns) |
| `002EF2B0` | EF2B0 — init ptr = `EF640()+0x200` | **real** (20 B, 5 insns) |
| `0026E500` | E500 — CLST root selector | **real** (40 B, 11 insns) |
| `002324F0` | F4F0 — 3-slot edge predicate | **real** (624 B, 140 insns) |
| `0022F430` | F430 — waypoint walker | **real** (1021 B, 249 insns) |
| `0022D4B0` | D4B0 — F430's callback scan | **real** (815 B, 202 insns) |
| `0022E6D0` | E6D0 — signed projected distance | **real** (249 B, 50 insns) |
| `0022CF50` | CF50 — triangle winding test | **real** (381 B, 85 insns) |
| `00380FA0` | FA0 — seg-vs-shape distance | **real** (263 B, 71 insns) |
| `00381AC0` | sphere primitive | **real** (708 B, 157 insns) |
| `00381630` | cylinder primitive | **real** (1168 B, 252 insns) |
| `00381450` | box primitive | **real** (477 B, 113 insns) |
| `00382020` | D2020 — unit-cylinder point test | **real** (154 B, 42 insns) |
| `0046BF60` | BF60 — point-plane dot | **real** (54 B, 12 insns) |
| `0046BFA0` | BFA0 — signed projected distance | **real** (294 B, 60 insns) |
| `00381EB0` | EB0 — point-in-unit-shape test | **real** (365 B, 88 insns) |
| `003DA5A0` | D5A0 — capsule distance | **real** (246 B, 59 insns) |
| `003A1D30` | A1D30 — `sqrtf(|x|)` via f64 | **real** (23 B, 5 insns) |
| `003DA730` | DA730 — anisotropic XZ metric | **real** (244 B, 57 insns) |
| `00861F56` | TACF — thunk → IAT `acosf` | **real** (6 B) |
| `00861F5C` | TSQD — thunk → IAT `sqrt` (f64) | **real** (6 B) |

Plus the whole EXP-130…137 trees re-executed — 113 real bodies total
(`bodies.json`).

Scripted boundaries (traced, NOT executed):

- `0022D0D0` D0D0 — F430's region query; `eax` per case
  (`d0d0rets`, sign-bit exits the walk) + optional `out16`
  (`d0d0o`).
- CRT imports via real IAT/thunks: `sqrtf`, `sqrt` (f64), `acosf`,
  `atan2f`, `memset`, `_fdclass`, `cosf`, `sinf`, `_isnan`,
  `_finite` — planted host trampolines (import-dir proven).

## Verified behavior contract

- `EF640()`: `rax = 0x2164280`. `EF2B0()`: `rax = EF640()+0x200 =
  0x2164480` — N48F0's `d[+0x1044]` read lands at image
  `0x21654C4` (BSS).
- `E500(ecx)`: `q[0x209A670]==0 → 0`; else `q[CLST + (ecx? 0x3B0 :
  0x3A8)]`.
- `F4F0(tab, edge, ctx)`: three slot iterations over the
  `0x908DE8` winding table `{1,2,0}` build per-edge geometry ctxs;
  among candidates with `crossy < −1e-4` it returns the slot
  minimizing `|t−0.5|` (first qualifier always stores; later ones
  only strictly closer). `eax` is 32-bit — `-1` propagates as
  `0xFFFFFFFF`, not `0xFFFFFFFFFFFFFFFF`; home saves of caller
  `rbx/rbp/rsi` are skipped when caller-carried values are
  indeterminate.
- `F430(tab, ctx)`: `r15 = N33050(*B)`; `w[ctx+0x44]=0`,
  `w[ctx+0x42]=0xFFFF`; loop: store `delta=*B−*A` at `ctx`,
  `f[ctx+0x30]=f[ctx+0x34]=|delta|`; three bank iterations
  (`0x908DF8` `{0,1,2,-1}`, `cell=(w[tab+0x40]+1)*bank+w[ctx+0x3C]`)
  write `w[ctx+0x3E]/w[ctx+0x40]` from the `q[tab+0x20]` range
  words then `call q[ctx+0x28]`; `sel<0x8000` accepts (writes
  `*B=*Aout`, `fl!=0 → w[ctx+0x3C]=0xFFFF`) else restores
  `w[ctx+0x44]/w[ctx+0x42]`; `w[ctx+0x3C]==r15 → 0xFFFF`; then an
  inline staggered-grid re-resolve (col-parity half-cell offset,
  `idiv` traps at `0x22F678`/`0x22F77B`/`0x22F798`, `0x908E18`
  rect `+1.569`/`−0.5` margins) → `D0D0` region query; `eax&0x8000…`
  → `w[ctx+0x3C]=0xFFFF` exit, else `*A=out16`, convert back to
  cell, repeat.
- `D4B0(tab, ctx)`: scans `w[ctx+0x3E..0x40]` of the edge arr;
  `si>=0x5000` skip; `0x4000<=si<0x5000` subrecord
  (`sub=q[tab+0x18]+(si−0x4000)*144`, `d[sub+4]` → CLST pair at
  slot `((m>>0xD)&0x1F)+0x20` → `FA0`); `si<0x4000` plain edge
  (`edge=q[tab+0x10]+si*32`, `d[edge+0xC]` → same CLST merge →
  `E6D0` + inline candidate point + `CF50`). Class filter on
  `ebx&7`: `0` proceeds; `1` needs sign clear and not
  (`bit30 & cx==4`); `4` needs `cx==4`; else skip. `d>=0` and
  `d<f[ctx+0x30]` gates a candidate; `ebx` bit23 → one-shot
  `w[ctx+0x44]=1` (when 0), clear → `f[ctx+0x30]=d` + shared
  store tail (`*q[ctx+0x20]=out16`, `w[ctx+0x42]=si`,
  `w[ctx+0x44]=2`). `cnt` re-read at loop bottom.
- `E6D0(A, ctx, {edge, vtx})`: `L=sqrtf(ctx²)`;
  `num=(A−vtx)·edge.n`, `den=ctx·edge.n`; returns f32 bits
  `−L·num/den` (negative/NaN → candidate rejected by caller).
- `CF50(tab, si, pt)`: for `b∈0..2` over table `{1,2,0}`:
  `cross(vb−va, pt−va)·f[rec..rec+8] > 0` must hold; `eax=1/0`.
- `FA0(out, shape, A, B)`: transforms both endpoints into the
  shape's local frame (`MXVW` ×3: `(shape+0x50)⁻¹`), dispatches
  `d[shape]==0/1/2 → sphere/cylinder/box` primitive, maps the
  closest point back through `shape+0x10`, returns 3-D distance
  or `−1.0`.
- Unit primitives: sphere projects `A` onto the segment dir and
  solves the unit-sphere surface (`acosf`/`sinf`); cylinder runs
  top/bottom cap plane tests (`BF60`/`BFA0`) plus the XZ-radial
  side solve (`acosf`/`sinf`), `D2020` tests inside-cap; box runs
  the 6-face table at `0xD11200` with margin `1.001`/eps `−0.001`.
- `D2020(pt)`: `−1<y<1` and `sqrtf(x²+z²)<1` → `eax=1/0`.
- `EB0(sub, pt)`: `local = (sub+0x50)⁻¹·pt` via `MXVW`; type 0
  `sqrtf(x²+y²+z²)<1`, type 1 `D2020`-equivalent, type 2
  `|x|,|y|,|z|<1` → `eax=1/0`; caller `rbx` saved at `vsp+0x18`.
- `D5A0(out, capA, posB, capB, posA=stack)`: `ellA =
  A1D30(DA730(capA, posB, posA))`, `ellB` symmetric;
  `*out={posA−posB, 1.0}` when `out!=0`; `f[out+0xC]=sqrt_f64
  (dx²+dz²)`; `xmm0 = dist − (ellA+capA.w + ellB+capB.w)` f32
  bits. No `rax` writes inside; 5th arg from the caller
  stack/home area (`q[vsp+0x28]`).
- `A1D30(x)`: `cvtps2pd`/`andps` abs → `jmp 0x861F14` sqrtf.
- `DA730(cap, p1, p2)`: rotated anisotropic XZ metric —
  `cosf`/`sinf` of `−f[cap+8]` rotate `(p2−p1)`, with
  semi-axes `f[cap]`/`f[cap+4]` squared and reciprocal-divided
  (`u²+v²` over `v²/rx²+u²/rz²`); returns squared-ish f32
  consumed by `A1D30`.

## Findings

1. **The census under/over-counted in both directions.** EF2B0
   first read as ~1496 B of "deep roots" that were all packed
   siblings — the real body is a 20-byte accessor. D5A0 first
   read as 1450 B because a mid-body `ret;int3` boundary was
   missed — the real body is 246 B ending `0x3DA696`. F4F0's
   real end is `ret @0x23275F` (624 B); the later `jmp 0x22F250`
   belongs to a packed sibling. `0x381AC0`'s sphere primitive
   ends `ret @0x381D83` (708 B) — calls to `0x380E00/0x380EB0/
   0x380800` live in the sibling at `0x381D90`. `0x380B80` and
   `0x3DA830` dropped out entirely — no real body calls them.
2. **`eax` is 32-bit even on "return −1" paths.** F4F0's
   reject returns through `eax`, so Python `-1` had to be
   re-latched as `0xFFFFFFFF` before callers' `&0xFFFFFFFFFFFFFFFF`
   turned it into `0xFFFFFFFFFFFFFFFF` — three `n331-*` cases
   caught exactly that.
3. **The walk is genuinely unbounded without a terminating
   D0D0.** With the scripted region query returning
   cell-re-resolving outputs, F430 loops forever on both sides
   (Unicorn stopped at its 300000-insn cap mid-loop at
   `0x22F555`). The fixtures now plant `d0d0rets=[0x80000000]`
   (one-shot exit) or `d0d0o` out16s that resolve `*A` into B's
   cell — the model's defensive budget counts zero hits.
4. **Claim-path coverage required real triangle geometry.** No
   prior case ever claimed: `w[ctx+0x44]` only ever takes
   `{0,1,2}` under the real body, so the `movsx→movzx` mutant on
   N315E0's return word was equivalent — retired, not counted.
   Two cases (`blk-mode3-1`, `pv-mode3-agq`) now plant triangle
   recs whose planes their segments cross inside the winding
   (`v/v1/v2` fixture keys added at `rec+0x10/+0x12/+0x14`),
   driving `D4B0`'s full store (`w44=2`, `*B=Aout`) and
   re-arming the two `agq`-return mutants.
5. **Caller-register home saves are caller-carried state.**
   F4F0/D4B0 spill `rbx/rbp/rsi/r13` into the caller frame;
   where callers' registers are indeterminate the model passes
   `None` slots and skips those stores rather than planting
   fabricated values — N33110's loop passes the determinate
   tuple `(i, cnt, tab, tab)`, N19 writes `q[ctx+8]=vec` at
   `0x23196E` before its F4F0 call.
6. **F430's callback is a real planted pointer, not a
   boundary.** `q[ctx+0x28]` comes from the caller (N315E0
   plants `0x22D4B0`); unmapped values record a `memf` fetch
   fault like N2F830's `call q[rdi]`. The bank ctx it receives
   is the walker's own ctx — `D4B0` re-reads `cnt` at every
   loop bottom because `w[ctx+0x40]` is written per bank.

## Method

Same as EXP-133…137: Unicorn world vs Python model over planted
heap/BSS fixtures; trace = scripted-boundary hits; mem = watched
bytes; rets/faults/ends byte-compared. Mutants patch a single
shipped byte (old-byte asserted) and must diverge observable
state. The `call q[ctx+0x28]` callback dispatch executes
natively (the planted fn is real `0022D4B0` code); `d0d0rets`
queues and `d0d0o` out16s drive the scripted region query, and
two new IAT cells (`0x8C2C60` sqrt f64, `0x8C2C78` acosf) are
planted with host trampolines like the existing CRT set.

## Scope boundary

`0022D0D0` D0D0 — F430's region query — stays scripted; its own
~10-body subtree (`0x22D0D0`'s callees) is the next package's
scope. The alloc/free family opened by `0x4FE420`/`0x3697F0`
(`0x3EC8D0`/`0x369860`) stays boundary — it is the heap
subsystem, not nav. Fixture-backed parity remains MODEL-PROVEN;
hand-built records do not become replay authority.
