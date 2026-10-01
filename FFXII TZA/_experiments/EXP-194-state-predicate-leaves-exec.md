# EXP-194 — Member state-step, dispatch arms, eligibility leaf execution

**Status:** complete — **186/186 cases, stable across 3 independent runs,
zero unexpected faults** (one disclosed expected fault: `a8ff0-nodesc`
@`30904A` on a null `02EBF138` descriptor).
**Evidence class:** `NATIVE-REPLAY` (`live_game: false`). Shipped bytes executed
under Unicorn; leaf callees intercepted at their real addresses and disclosed
below. Synthetic fixtures disclosed; none claim initialized-gameplay
reachability.
**Harness:** `_experiments/evidence/member-block-chain-exec/check.py` (extends
EXP-192/193; 156 inherited + 30 new `s8130-*`/`m8040-*`/`a8ff0-*`/`o4020-*`/
`s3c60-*` cases)
**Result:** `_experiments/evidence/member-block-chain-exec/result.json`
**Image authority:** FFXII TZA shipping EXE, SHA256
`73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`.

## Scope

Promotes the leaf/inner bodies behind EXP-193's `00308010` dispatch, the
`00324100` licence helpers, and `317930`'s final `00323C60` predicate to real
execution. All five EXP-193 entry bodies keep their SCR stubs for inherited
caller cases (SCR intercepts *calls*; direct `entry=` bodies run real).

- `00308130` — `b[member+5]==0` arm: member state-step.
- `00308040` — `b[+5]!=0` arm: presence/range predicate.
- `00308FF0` — indexed row accessor over `q[02EBF138]`.
- `00324020` — licence-bitmap popcount (pure).
- `00323C60` — final eligibility predicate → `323BB0`/`2F8FA0`.

## New executed facts

### `00308130` — member activity step (rcx = member row)

- `00307D10(member)` runs first: recomputes bit16 of `d[member+4]` as
  `ebx<<0x10`. `ebx=1` iff: (`b[rec+5]==0 && b[rec+4]==0x1A`), or
  `377C20`()==0 **and** `(d[rec+0x64]|d[rec+0x3C]) & 0x8000020`, or the
  `253B90`()==0 chain — `d[member+4]&0x200` → `30B050(member)`; `&0x400`
  → `307CE0` → `30BF20(q[member+0x708])`. `253B90`→1 side-effects:
  `b[02241F49]&=0xF9`, `q[02241F41]=0`, `d[member+0xDCC]=0`.
- Then `(d[rec+0x64]|d[rec+0x3C]) & 0x8000020` nonzero **or**
  `253B90`()==0 reach `bt d[member+4],0x10` (tests the bit `307D10` just
  wrote): set → ret 1; clear → `b[022C1F48]&1` gate → `3081E0(member)`
  real (LCG `328370` triple-advance `0x41C64E6D/0x3039` xor-fold +
  `32A150`) recomputes `d[member+0xDCC]` when `d[member]&0x800000==0 &&
  d[member+0xDCC]==0`; `b[rec+5]!=0` → ret 1; else `32A150()` >=
  `d[member+0xDCC]` → ret 1.
- `253B90` = `d[01E0C2B8]==0` — shipped value `1` → returns 0.

### `00308040` — presence/range predicate (rcx = member, edx = arg)

Null member/`q[+0x698]`/`b[rec+5]!=1`/`d[q[+0x6A0]]&0x20`/`edx!=0` → 0.
`d[flags]&0x48` nonzero: `f[obj+4] < -9.1765e12` (shipped const `0x5F1134`)
→ `30B050(member)` (scans `d[+0xBC4]` entries `q[+0xBC8+i*0x10]` →
`31B760` → `30AB40` pair-compare; ret>1 → 1) then `234DA0(member+0xE0,
&f²,0,0,1)` spatial query → `eax==0` → 1. `&0x48` zero → `q[member] &
1<<40` → 1 else `30B050`.

### `00308FF0` — indexed row accessor (edx = idx)

`dx <= 0x21E` → `row = 20E600(d[desc+0xC]) + w[desc+8]*dx` on
`q[02EBF138]`; `b[row+0x1E] ∈ {5,6}` → ret `b[row+0xA]`, else 0. Null
desc → fault reading `b[0+0x1E]` @`30904A`.

### `00324020` — licence popcount (pure)

Counts set bits over an 18-position window in `b[rec+0x194..]` (3
iterations × 6 unrolled tests, rotating `dl` mask). Measured: empty → 0,
bit0 → 1, bit0+bit15 → 2. **Correction**: EXP-193 described the `324100`
loop as a max-scan — the helper is a popcount used as the iteration bound.

### `00323C60` — final eligibility predicate (rcx = rec, edx = id)

- `322C50(1, id)`: kind-1 arm is a **class-nibble auto-dispatch** —
  `309440(id)` reads `d[01EE7CF8 + (id>>12)*0x58]` (class descriptor
  table) → `kind-1 ≤ 0x1F` re-dispatches through the same jump table.
  Member ids `0x1xxx` → kind 6 → `02EBF0F8` range check (real).
- Range pass → null rec / `b[rec+5]!=0` / `b[rec+4]>6` → ret 1 (allow
  under all vacuous states).
- Member row `b[+7]&0x10` → ret 1 early (no `323BB0`).
- Else tail `323BB0(rec, 0, id)`: `2F8FA0(0, id, buf)` compiles the
  requirement bitmap — iterates `d[02EBF038+4]` ABILD rows, keeps rows
  whose `323890(b[row+5])`==0 (i.e. `3241D0(b5)`==0x15 → arm 0 → 0;
  measured `b5 ∈ {1,2,3}`), and sets bit `edi` when `si` matches one of
  `w[row+8..+0x15]`. Intersect `buf` with `b[rec+0x194+i]` over `0x2E`
  bytes → any match → ret 1.
- `3241D0` table (measured real): ecx 1–3→0x15, 4–6→0x16, 7→0x17,
  8→0x18, 9–0xD→0x19, 0xE→0x1A, 0xF–0x11→0x1B, 0x12→0x1C,
  0x13–0x14→0x1D, 0x1E→0x1E, else 0.

## Disclosed scripted boundaries

`00234DA0` (spatial query, `sp234da0` retkey), `0x808C40`
(`__security_check_cookie` — ret-0 stub; return ignored), `263E30`
(reached only through `31B760` with a nonnull row — not exercised;
`30B050`'s loop kept to null entries). `308130`'s `307D10` subtree runs
`377C20`/`253B90`/`30B050`/`307CE0`/`30C210`/`30BB30`/`30BF20`/`3081E0`/
`328370`/`32A150` all real.

## Cases (30 new)

`s8130-*` (5): `fast`/`noor`/`b16clr`/`81e0`/`g25b` — bit16 recompute,
or-mask vs `253B90` join, `81E0` RNG+compare chain, global-gate ret0.
`m8040-*` (9): `698z`/`b5z`/`f20`/`edx`/`fhi`/`flo`/`b44`/`b050`/`b050e`.
`a8ff0-*` (5): `hi`/`ok`/`b1e6`/`bad`/`nodesc` (expected fault).
`o4020-*` (3): `zero`/`b0`/`bhi` popcount.
`s3c60-*` (7): `bad`/`null`/`b5`/`b4`/`bit10`/`scan`/`nomatch`/`nolid`.
