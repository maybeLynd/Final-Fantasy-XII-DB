# EXP-242 — broadcast flag sinks `28EF70`/`28EF00` real

**Status:** complete — **542/542 cases, stable across 3 independent
runs, byte-identical `result.json` (SHA256 `92012b09` prefix; 542
cases), fault census unchanged at 20** (the same pre-existing
intentional-null fixtures).
**Evidence class:** `NATIVE-REPLAY` (`live_game: false`). Shipped bytes
executed under Unicorn; synthetic fixtures disclosed below; none claim
initialized-gameplay reachability.
**Harness:** `_experiments/evidence/member-block-chain-exec/check.py`
(extends EXP-192..241; `d228-gaterc` gains `fbdev=1`; asserts
retargeted and extended, none weakened).
**Result:** `_experiments/evidence/member-block-chain-exec/result.json`
**Image authority:** FFXII TZA shipping EXE, SHA256
`73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`.

## Bodies promoted real this round

EXP-236 surfaced `317ED0`'s two flag-writer sinks as scripted
boundaries because both dereference `q[0x209BE80]` without a guard
and no case planted the object. EXP-241's `fbdev` fixture plants
exactly that cell — this round wires it in and promotes both.

- **`0028EF70`** (`l28ef70`, ×1 on `d228-gaterc`) — broadcast-rate
  flag writer on `317ED0`'s in-sync arm:

```text
call 28F0C0            ; ecx passes through unmodified
rcx = q[0x209BE80]
d[rcx+0x7C7C] ^= ((edx+edx) ^ d[rcx+0x7C7C]) & 2   ; bit1 := edx&1
w[rcx+0x7C82] = r8w
```

- **`0028F0C0`** (`l28f0c0`, ×1 — REAL-listed for arg visibility;
  its `ecx==0` tail is not reached this run) — null-guards the cell
  itself, then on `ecx != 0`: `253770(0x12, ecx)` (a bare
  `jmp 316A50` thunk — **already real since EXP-226**, so the
  stat-accumulator notify executes shipped bytes), then
  `w[obj+0x7C78] = low16(ecx)`, `d[obj+0x7C7C] |= 1`,
  `d[obj+0x7C7C] &= ~8`. Its `ecx==0` tail (a `273A20`/`244F00`
  slot-clear chain over `obj+0x57E0/+0x58B0/+0x5980`) is gated off
  by the planted call's `ecx=1` and stays unexplored.

- **`0028EF00`** (`l28ef00`, ×0 — the epoch-mismatch arm) —
  `d[obj+0x7C7C] = 0` then `|=8`, `|=1`; reloads the cell, and if
  non-null stores `w[+0x7C78]=cx`, `w[+0x7C82]=dx`. Promoted real
  alongside — its only image caller is `317ED0`'s mismatch arm
  (unreached on `d228-gaterc`).

## Fixture (disclosed)

`d228-gaterc` gains `fbdev=1` — the EXP-241 extended `fbdev` key:
a 0x12000 object at `q[0x209BE80]` with an empty device list. All
offsets the sinks touch (`+0x7C78`, `+0x7C7C`, `+0x7C82`,
`28F0C0`'s `+0x57E0..+0x5A42` tail region) are inside the alloc.

## Shipped-value pins (all computed, none planted)

`d228-gaterc` calls `28EF70(ecx=1, edx=0, r8=0)` (unchanged from the
stub-era recording — `ecx` = `d[0x22C315C]` post-increment, `edx` =
the `LCG%100` rate flag 0, `r8d` = `d[0x22C3158]`). The real body
then leaves:

- `w[fbdev+0x7C78] == 1` (`28F0C0` store of `low16(ecx)`)
- `d[fbdev+0x7C7C] == 1` (`|=1`, `&=~8` in `28F0C0`; `28EF70`'s
  bit-1 fold writes `(0+0)&1 = 0`, clearing nothing further)
- `w[fbdev+0x7C82] == 0` (`r8w`)

plus the unchanged arg record `l28ef70(1, 0, 0)` ×1 and
`l28f0c0` ×1 in the trace (`t53770` fires ×3 total on the case —
two pre-existing notify thunks plus this one).

## Corrections of record

- `28EF70` and `28EF00` were described in EXP-236 as "deref
  `q[0x209BE80]` without a guard" — the record stands for `28EF00`
  (its first write precedes the null check); `28F0C0` does guard
  (`test rax,rax; je` before any store), and `28EF70`'s unguarded
  reload happens only after `28F0C0` already established the cell's
  use.
- `253770` needed no promotion — it was REAL-listed all along (a
  recorded thunk into the already-real `316A50`).

## Boundaries (unchanged disclosures)

`30E130` (`e130` ×0), `317E50` (`b7e50` ×0), `20CE60` (`v20ce60`
×0), `427320`/`422C20` (×1 each), `3377C0` (`v3377c0` ×19),
`2E8FD0` (`v2e8fd0` ×1), `28F0C0`'s `ecx==0` `273A20`/`244F00` tail,
`3B02A0`, `46AB10`, `210EC0`, `1CCB20`, `3180F0`, `319CA0`,
`426130` remain scripted or unexplored. `live_game: false`.
