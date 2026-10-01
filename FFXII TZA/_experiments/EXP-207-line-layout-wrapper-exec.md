# EXP-207 — `002B24B0` line-layout save/reset/restore wrapper, executed

**Status:** complete — **441/441 cases, stable across 3 independent runs,
byte-identical `result.json` (SHA256
`c49b4c6426df229726d40c99b2f9748c8245dca9d2713a8e80990bb42d1fee02`), zero
unexpected faults.**
**Evidence class:** `NATIVE-REPLAY` (`live_game: false`). Shipped bytes executed
under Unicorn; synthetic fixtures disclosed below; none claim
initialized-gameplay reachability.
**Harness:** `_experiments/evidence/member-block-chain-exec/check.py` (extends
EXP-192..206; 438 inherited + 3 new `b24b0-*` cases)
**Result:** `_experiments/evidence/member-block-chain-exec/result.json`
**Image authority:** FFXII TZA shipping EXE, SHA256
`73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`.

## Scope

EXP-206 promoted the wrapper shell `002B3050`/`002B3120` and left the
evaluator `002B24B0` itself as the last boundary — this package promotes it.
Its own body (~0x330B) is fully proven; the inner measurers `002B2150`/
`002AF340` and the `ceilf` import (`00861F4A` → `api-ms-win-crt-math`,
identified via `external-import-stubs-map.tsv`) are boundary-stubbed.

## `002B24B0(state, const, r8, out-cell-ptrs)` — scoped text measure

The shared text context `q[0209CC40]` is a single object whose fields the
function **snapshots, resets, measures with, distributes, then restores** —
the DB's "scoped, not global" reading of it (GJ-4/GJ-10) confirmed
instruction-for-instruction:

- `r12 = q[0209CC48]` — the outer context pointer is swapped to `0` for
  the nested measure and restored at the end. `b24b0-run` observes it
  `0` mid-eval (`cc48mid`) and `0x5EED` after (`ctx48` sentinel).
- Saved/restored: `d[+0x10D8]` (`esi`), `f[+0x10E8]` (`xmm6`),
  `q[+0x10C8]` (`r14`), `b[+0x10FC]` (`bpl`), `b[+0x10FF]` (`r15`) — the
  progressive-reveal/typewriter state plus the arg-pointer slot.
- Cleared for the measure: `d[+0x10D8]`, `d[+0x10FC]` (a dword store —
  a **bulk clear of `+0x10FC..+0x10FF`**, the byte-flag span, not four
  fields), `q[+0x10EC]`, `q[+0x10F4]`, `w[+0x1100]`; `q[+0x10C8]` gets
  the caller's `rdx` (the `009166EC` const-double pointer from `2B3120`).
- `002B2150(&state-copy, r8, frame-arg-area, &ctx+0x10E8)` — the ctx
  evaluator (stubbed; fills `+0x10EC/+0x10F0/+0x10F4/+0x10FD/+0x1100`
  via `ctxr*` fixtures).
- `002AF340(&state-copy2, r8, &params-block, 0)` — the measure
  evaluator (stubbed; writes `f[params+0x30]`/`f[+0x34]` via `af340f`).
- Each measure float gets **`ceilf`** (`00861F4A` → `01CCEF90` IAT stub):
  `f[out+0x54] = ceil(x)`, `f[out+0x58] = ceil(y)` — dims round up to
  whole pixels.

## Result distribution (all proven)

- `b[+0x50] = b[ctx+0x10FD]` — the byte `002B3120` returns; `b[+0x51] =
  b[ctx+0x1100]`; `d[+0x5C] = d[ctx+0x10F0]` (the max-width field).
- `d[+0x60] = d[ctx+0x10EC]` (current-line width) — **but** the merge
  can overwrite it: `acc+ec > f[out+0x54]` → `f[+0x54] = acc+ec` (the
  running total wins over this measure); else `f[+0x60] = f54 − acc`
  (the remainder goes to the second out slot). `b24b0-merge` pins the
  `==` boundary: `comiss` is strict `>` — equal takes the else.
- `b[ctx+0x10FE]` set → `f[+0x10F4] += 2*d[01E0CDC0]*f[state+0x34]*
  f[state+0x38]` — `d[01E0CDC0]` ships `0x10` → `+32·scale` line-height
  accumulate (`b24b0-acc`: `3.5 + 32 = 35.5`, `+2.0 → 37.5` wins the
  merge).
- The `+0x10EC` field is dual-read: `d[ctx+0x10EC]` (dword → `d[+0x60]`)
  and `f[ctx+0x10EC]` (float → `acc+ec` sum) — same bits, two views.
- `movaps` save/restore of `xmm6`; return `0`.

## Harness changes

- `REAL` += `0x2B24B0`; the old `s2b24b0` cell-stub removed.
- Custom stubs: `0x2B2150` (`ctxrd`/`ctxrf`/`ctxrb` field writes onto
  `ctxo`, records `cc48mid`), `0x2AF340` (`f32[r8+0x30..0x34]` from
  `af340f`), `0x1CCEF90` (`ceilf` math, `f861` selects transform).
- `run()` now writes `a5..a9` at `rsp+0x28..0x48` (all via `rarg`) —
  five stack out-ptrs were needed for direct `2B24B0` entry; `sarg`
  also `rarg`-resolved.
- Fixtures: `ctxo` (always planted at `q[0209CC40]`), `ctx48`,
  `ctxd/ctxf/ctxq/ctxb` (pre-eval save sentinels), `e312f` (float
  fields on the arg struct), `c54` out-cell block + `c54r9`/`c54a5..a9`
  pointer attrs.

## Still scripted (disclosed)

`002B2150`/`002AF340` (the glyph-run measurers — the 131-body text
machinery inside), `ceilf` (real transform, fixture-selected), the five
`2B3050` leaves, cookie. The byte-3 segment counters `002B28F0`/`002B2930`
and the `cvtt` wrappers `2B27E0`/`2B2880`/`2B28B0` were decoded but are
off this path.

## Corrections of record

- `b24b0-run`'s `ctxrd={0x10EC:0x44}` was replaced by `ctxrf` floats —
  `+0x10EC` feeds `addss` (float view), not a dword sum.
- `cvtt` semantics under real `ceilf`: `bd00-t2`/`b3050-run` dims are
  now `18/5` and `b3120-ok` `31` — the EXP-206 stub wrote floors; the
  real function is `ceilf` (import-map identified), not `floorf`.

## Validation

`python check.py` — 441/441, three independent runs, `result.json` SHA256
`c49b4c6426df229726d40c99b2f9748c8245dca9d2713a8e80990bb42d1fee02`
(byte-identical), zero unexpected faults.
