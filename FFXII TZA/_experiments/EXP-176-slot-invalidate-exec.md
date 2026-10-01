# EXP-176 — `26E130`/`26E150` slot invalidate + `3278D0` sweep

Evidence class: NATIVE-REPLAY (deterministic Unicorn fixtures on the exact
shipping EXE, SHA256 73461D08…97f8). Fixture boundaries disclosed; no claim
of initialized-gameplay reachability.

Harness: `Temp\exp166_check.py` — **184/184, stable ×3**
(three independent processes).

## `26E130`/`26E150` — occupancy-slot invalidators

Siblings of `26E100` (the `231400` position-query thunk).

- `26E130(idx)`: `d[0x209A3E0 + idx*8] = 0` — clears the **low dword
  only** of a stride-8 slot-table entry (hi dword preserved; proven),
  then `jmp 0x3278D0`.
- `26E150(base, count)`: `count <= 0` → immediate ret. Else for
  `i = 0..count-1`: `d[0x209A3E0 + (base+i)*8] = 0`, then `call
  0x3278D0` — **the sweep runs once per cleared slot**, not once total.
- Table `0x209A3E0` is BSS (runtime-built), entries `{d lo, d hi}`.

## `3278D0` — flagged-object cache-reset sweep

- Loops `i = 0 .. d[0x208E6A0]-1` (object count; `236850` reads it).
- `236820(i)`: rejects `i < 0` or `i > count-1` → null; else
  `q[0x208E688] + i*0xF50` — the global object array, stride `0xF50`.
- Gate `b[obj] & 0x10` — unflagged objects untouched (proven).
- On flagged objects: `3839C0(obj+0x200)` writes
  `w[+0xC] = w[+0xE] = 0xFFFF`; `3839F0(obj+0x200)` writes
  `b[+0x10 .. +0x8F] = 0xFF` (0x80 bytes) — an invalidation of a
  cached cell/sector sub-record hanging off `obj+0x200`.

## Executed cases

- `t26e130-one`: slot 1 cleared (lo dword only), sweep ×1, flagged obj
  gets both invalidations (words `0xFFFF`, bytes `0xFF`).
- `t26e130-nofl`: slot cleared, flag-clear obj's `+0x210` stays `0xAA`,
  `z3839c0`/`z3839f0` never fire.
- `t26e150-loop`: slots 0–2 cleared, slot 3 preserved, `z3278d0` ×3,
  obj0 flagged → invalidated, obj1 clean → untouched.
- `t26e150-zero`: `edx=0` → no clears, no sweeps.

## Corrected cells (same RIP-slip class, caught by read-trace)

- object count: `d[0x208E6A0]` (not `0x209CAA0`)
- object array base: `q[0x208E688]` (not `0x209CA88`)

## Why it matters

This is the invalidation counterpart to the occupancy machinery of
EXP-173: when occupancy slots are freed (`26E130`/`26E150`), every
flag-`0x10` object's cached cell/sector record at `+0x200` is force-reset
to `0xFFFF`/`0xFF` — the "positions changed, re-resolve" broadcast.
