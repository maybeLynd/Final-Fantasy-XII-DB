# EXP-179 — generational-handle record pool (`3AB960`/`3ABCA0`/`3ABD00`/`3ABD20`/`3ABB60`) + `265920`

Evidence class: NATIVE-REPLAY (deterministic Unicorn fixtures on the exact
shipping EXE, SHA256 73461D08…97f8). `17D490` and `3AC920` are scripted
boundaries (disclosed, tags in `calls`); all pool logic runs real.

Harness: `Temp\exp166_check.py` — **220/220, stable ×3**
(three independent processes).

## The pool

- Base `q[0x2B3F528]` → **0x80 records × 0x70 bytes**.
- `d[rec+0]` = live handle `(gen<<8) | slot`; **0 = free**.
- `q[rec+8]`/`q[rec+0x10]` = doubly-linked live list (prev/next).
- Payload `rec+0x20`, 0x50 bytes copied verbatim from caller template.
- Globals: count `b[0x2B3F500]`, generation `d[0x2B3F504]`
  (wraps `>0xFFFFFF → 1`), head `q[0x2B3F508]`, tail `q[0x2B3F510]`.

## `3AB960(tpl)` — alloc

- First-fit scan `d[rec]==0`, max 0x80 → **full pool returns 0**
  (proven `t3ab960-full`).
- `gen = ++d[0x2B3F504]`, handle `(gen<<8)|slot` stored `d[rec]`,
  `count++`, 0x50-byte template copy, then kind dispatch on
  `b[rec+0x20]`:
  - **kind 2**: `f[+0x50] = K / f[+0x2C]²`
  - **kind 3**: `f[+0x60] = K / f[+0x2C]²`
  - **kind 4**: `f[+0x68] = K/f[+0x2C]²`; `f[+0x6C] = K/(f[+0x60]−f[+0x64])`
  - **kind 5**: `f[+0x50] = K/f[+0x2C]²`; `f[+0x58] = |v(+0x40..48)|²`;
    `f[+0x5C] = v(+0x60..68)·v(+0x40..48)`;
    `f[+0x54] = K/(|w|² + |v|² − 2·dot)` — radius/extent
    precomputations for the occupancy volumes of EXP-173
    (sphere/capsule-style derived fields).
  - `K` = `f[0x1CEBBA8]` = **1.0f** (all four arms share it).
- Appends to tail; first record sets head=tail. Returns handle.
- Proven: first alloc `gen 0x40→0x41` → `0x4100`, second → `0x4101`
  with correct prev/next splicing, kinds 2/4/5 math exact.

## `3ABCA0(handle)` — free

- Walks live list head→next comparing `d[node]==handle`; miss →
  no-op (proven).
- Hit: `count--`, `d[node]=0`, standard unlink with head/tail fixup
  (mid/head/tail all proven).

## `3ABD00(handle)` — resolve → payload

- `slot = handle & 0xFF` (no bounds check — 0x80-slot array),
  `rec = base + slot*0x70`; returns `rec+0x20` iff `d[rec]==handle`
  else 0. **Generation check makes stale handles fail** (proven:
  `0x0902` vs live `0x1102` → 0).

## `3ABD20()` — find first live node with `b[+0x23]==5`

Returns `node+0x20` or 0. Both arms proven.

## `3ABB60()` — pool init

- Clears `d[rec]`/`b[rec+0x20]` for all 0x80 (descending),
  `count=0`, zeroes head+tail (`movdqu` over `0x2B3F508`).
- Then inline-allocates a **built-in kind-7 record** at slot 0:
  stack template `b[+0]=7, b[+3]=3` (rest zeroed), calls
  `3AC920(rec+0x20)` (scripted boundary — kind-7-specific init),
  appends. `count=1`, `gen++`. Whole flow proven incl. dirty-pool
  clearing.

## `265920()` — nav-generation source

- `n = 17D490()` (`d[1D50D0()+0xAAC]` — global counter, scripted).
- `n > 0` → tail-calls `17D490` again → returns it (2 calls proven).
- `n ≤ 0` → returns `b[2EF640()+0x1260] + 1` — a peek at the
  context-local counter (`2EF640` = static `0x2164280`, real).
  Does **not** store.

This closes the EXP-178 builder boundary: `379630`'s `3ABCA0`/`3AB960`
calls are now fully understood native code (the handle array at
`0x2ADD120` holds these generational handles), and `265920` is the
nav-generation value stored by `26E8D0`.
