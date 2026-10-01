# EXP-175 — `233050` pos→cell converter execution-validated

Evidence class: NATIVE-REPLAY (deterministic Unicorn fixtures on the exact
shipping EXE, SHA256 73461D08…97f8). Fixture boundaries disclosed; no claim
of initialized-gameplay reachability.

Harness: `Temp\exp166_check.py` — **180/180, stable ×3**
(three independent processes).

## `233050(ctx, pos)` — staggered-grid pos→cell

Args: `rcx` = egrid ctx, `rdx` = position quad `{f x, f y, f z, f w}`.

- `wx = cvtdq2ps(d[ctx+0x38]) + f[pos]`; `wz = cvtdq2ps(d[ctx+0x3c]) +
  f[pos+8]` — integer cell-origin offsets added to world x/z.
- `wx < 0 || wz < 0` → **ret `0xFFFF`** (`movzx eax, r10w`, `r10d=-1` —
  the invalid sentinel is a *16-bit* one).
- `col = trunc(wx) / d[gdesc+0x10]` (cvttss2si + idiv, remainder
  discarded), `gdesc = q[ctx]`.
- **Stagger**: if `col & 1`, `zint = trunc(wz) − d[gdesc+0x14]/2`
  (`mov eax,cellh; cdq; sub eax,edx; sar eax,1; neg` — a constant
  −cellh/2 shift on odd columns, *not* remainder-dependent).
- `row = zint / d[gdesc+0x14]` — **signed idiv, truncates toward zero**:
  odd-column points with `wz < cellh/2` produce `zint ∈ (−cellh, 0)` →
  row `0`, never negative. Negative rows are unreachable when
  `wz ≥ 0` and `zint > −cellh`.
- Bounds: `col ≥ d[gdesc+8]` or `row ≥ d[gdesc+0xC]` → `0xFFFF`.
  Only the upper bounds are tested; negatives are precluded upstream.
- Return `row * gcols + col` (16-bit-significant — callers do
  `movzx r8d, ax; test ax, ax; js reject`, so bit-15 rejects).

## Executed cases (grid 8×8, cell 4×4, origin 0)

- `t233050-even`: (9,·,9) → col 2 even, row 2 → **18**.
- `t233050-odd`: (5,·,5) → col 1 odd → zint 5−2=3 → row 0 → **1**
  (unstaggered would give row 1 → cell 9 — proves the stagger shift).
- `t233050-stag0`: (5,·,1) → zint 1−2=−1 → idiv trunc → row 0 → **1**
  (proves trunc-toward-zero clamps the stagger underflow).
- `t233050-negx`/`negz`/`colhi`/`rowhi`: all → **0xFFFF** exactly.
- `t233050-orig`: `gox=4`, (1,·,9) → wx 5 → col 1 odd, zint 7 →
  row 1 → **9** — origin offset proven.

## Why it matters

`233050` fronts every egrid lookup (`231400`, `231900`, `233110`). The
16-bit sentinel, constant −cellh/2 odd-column stagger, and
truncation-clamped negative rows are now execution-pinned — the last
underspecified edge in the position-validation chain.
