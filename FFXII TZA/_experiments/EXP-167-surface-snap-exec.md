---
id: EXP-167
title: "26E350/231900 walkable-surface snap — the 32A790 scripted boundary promoted real"
status: executed
evidence: NATIVE-REPLAY
exe_sha256: 73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8
harness: exp166_check.py
result: 144/144 (stable x3)
---

# EXP-167 — surface snap chain, executed

Promotes the last scripted boundary on `336E40`'s aux arm
(`32A790`) to real — it was a one-insn `jmp 0x26E350` trampoline
all along. The whole chain shares the `q[0x209A670]`/`q[0x209A678]`
entity-grid ctx fixture landed in EXP-166.

## `32A790` → `26E350(ctx?, pos)` — executed

- Gate `q[0x209A670] != 0`, ctx `rbx = q[0x209A678]`.
- `231900(ctx, pos, mask=1)` → row idx or −1; found →
  `231820(ctx, pos, idx)` snaps `f[pos+4]` = surface height.

## `231900(ctx, pos, mask)` — decoded + executed

Best-walkable-row finder:

- `cell = 233050(ctx, pos)` → −1 bail.
- Span `w[q[ctx+0x20] + cell*2] .. [+1]` (same ridx pattern as
  `233110`).
- Per row idx `bx` (`bx < 0x4000`):
  - `row = q[ctx+0x10] + bx*0x20`; **`f[row+4] > 0.001f` gate**
    (const at `0x8C5B2C`).
  - `bt mask, (d[row+0xC] & 7)` — layer/mask filter.
  - `2324F0(ctx, bx, &scratch)` — surface eval; **negative =
    usable** (`jns` skips).
  - `231890(ctx, pos, bx)` — plane solve:
    `(sec.z−pos.z)*row.f8 + (sec.x−pos.x)*row.f0` `/f[row+4]`
    `+sec.f4`; skip-solve → `pos.y`.
  - max-select into `si`.
- ret `si` = best row or −1.

## `231890` / `231820` — executed

Twin plane-solvers over `q[ctx+0x10]` row (`w[+0x10]` sector idx)
→ `q[ctx+8]` 16-byte sector plane record. `231890` returns
height in `xmm0`; **`231820` writes `f[pos+4]`** — the actual
snap-to-surface mutation.

## Proven

- `t26e350`: pos (1, 99, 2) → cell 0, row 0 → `z233050`,
  `z2324f0`, `z231890`, **`z231820` ×1** → `f[pos+4]` 99.0 →
  **0.0** — the snap write executed and observed.
- `t1f70-aux`/`t1f70-mode1`: the aux transform chain now calls
  `z32a790` ×2 → `z26e350` → `z231900` → `z233050` real —
  bail paths (`cell −1` / empty span) execute natively.
- `t2730-accept` re-proven with full tag coverage:
  `z231400`/`z233050`/`z233110`/`z230a40`/`z2324f0`/`z22f830`
  ×5, `z22f8b0` ×10 — every body in the commit path is now
  tagged real.
- All 143 prior cases re-proven — 144/144 across three
  processes.

## Fixture disclosures

- `erow` now also plants `f[rowtab+4] = erowf4` (default 1.0)
  to clear the `0.001f` gate const.
- `epos`: pos buffer `{1.0, 99.0, 2.0, 0.0}` for direct
  `26E350` entry.
- Everything else inherited from EXP-166 (zonectx, egrid,
  IAT stubs, MATH hooks).

NATIVE-REPLAY only — planted ctx is a disclosed fixture; no
initialized-gameplay reachability claimed.
