# EXP-181 — nav-row accessor family un-stubbed; `26E8D0` runs fully real

Evidence class: NATIVE-REPLAY (deterministic Unicorn fixtures on the exact
shipping EXE, SHA256 73461D08…97f8). The former `3ED0xx`/`3ECFD0`/`3B6BA0`
scripted boundary is eliminated — all six accessors now execute real code
against a planted nav-row table. `265920`/`3AB960`/`3ABCA0`/`379760`
remain scripted in the builder paths only (all have direct-entry real
coverage).

Harness: `Temp\exp166_check.py` — **237/237, stable ×3**.

## The nav row table

`q[0x2EBB7F0]` → rows of stride **0x180**, indexed
`row = d[0x209A6E8] − 1` (the value `26E8D0(n)` stores). All accessors
early-out on null table.

- **`3ED0B0()`** = `d[row+4]` — the sub-record count that lands on
  `d[0x209A2D0]` (triple-duty cell) and drives `379630`'s
  `clamp(count,0,3)` alloc loop. Null → −1. Both proven.
- **`3ECFD0(out)`** = copies `row+0xF0..0xFF` quad → out. `26E8D0`/
  `26E960` call it with `0x209A370` — **the scale quad `379760` reads
  is literally the selected nav row's +0xF0 field.**
- **`3ED140()`** = `f[row+8]` in xmm0; null → `f[0x1CEBBA8]` = 1.0f
  (the shared `K` constant).
- **`3B6BA0()`** = `f[0x1EFE314] = xmm0` — stores `3ED140`'s result.
- **`3ED020(i, out, out2)`** = copies row `+0x90+i*0x20` quad → out
  and row `+(i+5)*0x20` quad → out2 — two interleaved 0x20-stride
  arrays at +0x90/+0xA0. `26E8D0` fills 3 records at `0x209A2F0`
  (stride 0x30; +0x20..0x2F untouched).
- **`3ED7B0(i)`** = `d[0x2EBB7F8]=d[row(i)+0x10]`,
  `d[0x2EBB7FC]=+0x14`, `d[0x2EBB804]=+0x1C` — indexes row **i
  directly** (not n−1); `26E8D0` calls it with `ecx = n−1`.

## `26E8D0(n)` — fully real now

`d[0x209A6E8]=n`, `d[0x209A708]=1`, `d[0x209A2D0]=3ED0B0()`,
3× `3ED020` → `0x209A2F0..0x209A37F`, `3ECFD0(0x209A370)`,
`3ED140`→`3B6BA0`→`f[0x1EFE314]`, `3ED7B0(n−1)`. Zero `3278D0`
sweeps. Every store verified against the planted row's deterministic
fill (`d[row r + off] = 0x10000000|r<<16|off`).

## `379630` count path now real

`t379630-*` drive the alloc count through the real chain
`265920→26E8D0→3ED0B0→d[0x209A2D0]` instead of a stub return:
`navcnt` 2 → 2 allocs, −1 → 0, 9 → 3 (clamp). `d[0x209A2D0]`
asserted = 2.

## Corrected cells (read/write-trace)

- nav table `q[0x2EBB7F0]` (was `0x26B9CF0`)
- `3ED140` default `f[0x1CEBBA8]` (was `0x1CECBA8`) — same K cell
- `3ED020` record dest `0x209A2F0` (was `0x209A8F0`)
