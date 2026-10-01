# EXP-178 — slot-API wrappers + `379630` builder execution-validated

Evidence class: NATIVE-REPLAY (deterministic Unicorn fixtures on the exact
shipping EXE, SHA256 73461D08…97f8). Fixture boundaries disclosed; the
`3ED0xx`/`3ABxxx`/`265920`/`379760` calls are scripted boundaries (tags in
`calls`, disclosed). No claim of initialized-gameplay reachability.

Harness: `Temp\exp166_check.py` — **203/203, stable ×3**
(three independent processes).

## `0x209A3E0` slot-API dispatch wrappers (all tail-jumps)

The table partitions into slot ranges with dedicated entry points:

- **`3791D0(idx)`**: `idx<0` → `26E150(0, 0x20)` release slots
  `0..0x1F`; else `26E130(idx)`.
- **`379270(idx)`**: `idx<0` → `26E150(0x20, 0x20)` release slots
  `0x20..0x3F` — **the `22F8B0` entity-flag group**; else
  `26E130(idx+0x20)`.
- **`379220(idx)`**: `idx<0` → `26E150(0x40, 0x10)` release slots
  `0x40..0x4F`; else `26E130(idx+0x40)`.
- **`3791F0(slot,val)`** / **`379240(idx,val)`** (slot `idx+0x40`):
  `val<0` → `26E850(slot, 0x12, 5)` release; else
  `26E880(slot, val, 0x12, 5)` — **a 5-bit override field at bits
  18–22** (`mask = 0x1F<<0x12 = 0x7C0000`). Executed both arms;
  observed A `0x1234→0x7C1234`, B `0xAAAABBBB→0xAA9EBBBB` (val 7).

## `26E8D0(n)` — nav re-init without table reset

- `d[0x209A6E8] = n`; `d[0x209A708] = 1`.
- `d[0x209A2D0] = 3ED0B0()` — **the return lands on the same cell that
  is `230A40`'s table base AND `379630`'s alloc count** (triple-duty
  cell, confirmed by write-trace).
- Tail identical to `26E960`: `3ED020` ×3 on `0x209A6F0`,
  `3ECFD0(0x209A370)`, `3ED140`, `3B6BA0`, `jmp 3ED7B0` with
  `ecx = n-1`.

## `379290` gate → `26E8D0` | `379630`

- `q[0x2ADD090] != 0` → `b[0x2ADD0E9] = 1`, `26E8D0(265920())`.
- else → `b[0x2ADD0E9] = 0`, `jmp 0x379630` (full rebuild).
- Both arms executed.

## `379630` — the egrid/nav builder

- Frees handle array `d[0x2ADD120,+0x4,+0x8]` + extra `d[0x2ADD11C]`
  via `3ABCA0` per nonzero entry, then zeroes all four.
- `26E8D0(265920())` — re-init + count write.
- Alloc loop: `rsi = clamp(d[0x209A2D0], 0, 3)` — the value `26E8D0`
  just stored from `3ED0B0()`; per i: `861EC0` memset `0x50` on stack
  record → `movaps` template `0x2A5A2E0 + i*0x30` → patch
  `b[rec+7] = (b&3)|0x20`, `d[rec] = 0x1002001`, `b[rec+4]=1` →
  `3AB960(rec)` → `d[0x2ADD120+i*4] = eax` handle.
- Tail `379760`. Stack cookie real.
- Executed: `t379630-2` (count 2 → 2 allocs, 3 frees incl. extra),
  `-neg` (ret −1 → clamp 0), `-hi` (ret 9 → clamp 3).

## Harness fixes this round

- `t3*` case prefix added to the assert dispatch (same dead-branch
  class as EXP-172's `t2` fix).
- SCR tags land in `w.rets["calls"]` (with rcx/rdx/r8/r9 capture), not
  `w.trace` — script-boundary counts now use that list.

## Corrected cells (read/write-trace)

- `379290` gate `q[0x2ADD090]`, flag byte `b[0x2ADD0E9]`
- handle array `d[0x2ADD120..0x2ADD128]` + `d[0x2ADD11C]`
- count/`3ED0B0` ret cell `d[0x209A2D0]`; template `0x2A5A2E0`
