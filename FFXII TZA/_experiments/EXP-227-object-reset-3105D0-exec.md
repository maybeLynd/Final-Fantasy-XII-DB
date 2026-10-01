# EXP-227 — object reset `3105D0` real (full teardown write chain + embedded-ctx compose)

**Status:** complete — **542/542 cases, stable across 3 independent
runs, byte-identical `result.json` (SHA256 `dfe49da6` prefix; 542
cases), zero unexpected faults** (the 20 fault records across 10
cases are the same pre-existing intentional-null fixtures that assert
the fault).
**Evidence class:** `NATIVE-REPLAY` (`live_game: false`). Shipped bytes
executed under Unicorn; synthetic fixtures disclosed below; none claim
initialized-gameplay reachability.
**Harness:** `_experiments/evidence/member-block-chain-exec/check.py`
(extends EXP-192..226; no new cases — existing `u3105d0` call sites
now execute the shipped body and asserts retargeted to the real tag +
write/trace evidence)
**Result:** `_experiments/evidence/member-block-chain-exec/result.json`
**Image authority:** FFXII TZA shipping EXE, SHA256
`73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`.

## Body promoted real this round

`003105D0` (`u3105d0`, ×28 — the third-largest scripted call) — the
full object reset reached from `300140`/`300FC0`/`301140`/`3243F0`/
`31A630` teardown paths.

| body | semantics | hits |
|------|-----------|------|
| `003105D0` (`l3105d0`) | null/`q[obj+0x698]` gate → `310780(obj)` detach → `b[+0x6B6]`=0 → `30C970(b[+0x695])` + `b[+0x695]`=FF → same for `+0x696` → `300280(obj)` → `q[obj] &= 0xFFFFBFF75FFFCFFF` + `d[obj+4] &= 0xFFDFFF7F` + `d[+0x690]`=0 → `16D6A0(obj)` → `q[obj] &= 0xFFF3FFFFFEFFFFFF` → loop `i < 236850()`: `236820(i)` non-null → `d[elem+0xEA0] &= ~(1<<b[obj+0xEA9])` → `316CF0(obj+0x778)` → copy `+0x718`→`+0x730` (16B) + `+0x728`→`+0x740` (8B), `d[+0x700] &= ~3` → reset `w[+0x6B7]`, `b[+0x6B4]`, `q[+0x768]`, `q[+0x760]`, `q[+0x6D8]`, `q[+0x6D0]`, `d[+0x75C]`, `w[+0x714]`=FFFF, `q[+0x708]`, `d[+0x710]` → `3291B0(obj+0x80,0,0)` → `q[obj+0x1A4]`=0, `d[obj+0x1A0]`=0, `q[+0x6D8]`=0, `d[+0x6D4]`=0, `d[obj+0x1F0] &= ~0x20` → `33C9B0(obj+0x80)`. | ×28 |

Callees newly exercised as shipped bytes (all native-unmapped, zero
scripted shims added or removed beyond `u3105d0` itself):

- `00300280` — `q[obj+0x698]`/`b[rec+5]` gate → `w[obj+0xDC8]`≠FFFF →
  `3008A0(w,1,0,1)` + `w[+0xDC8]`=FFFF; `d[obj+0xE58]`≠0 → `253690`+
  `254EE0` clamp + zero.
- `003008A0` (`a08a0` — already real) — registry dispatch: `id`&F000
  ≤E000 → `309F30(id,r14d)` → `q[page+0x48]`=`2FD150` handler. Under
  `w[obj+0xDC8]`=0 the shipped page-0 descriptor lands both `2FD8D0`
  and `2FD150` on their null-table (`q[desc+8]`=0 shipped) early-outs —
  bounded, real.
- `00236850`/`00236820` — `d[0x208E6A0]` count getter / bounds-checked
  `q[0x208E688]+i*0xF50` row getter — the existing `OBJCNT`/`OBJARR`
  fixture cells, so the `d[elem+0xEA0]` bit-clear loop runs live
  (`e6850`/`e6820` tags already real).
- `00316CF0` — `b[rcx]` bit0 latch → `861EC0(rcx,0,0x208)` memset →
  restore bit0 + `w[+1]`=0 — zeroes `obj+0x778..0x97F`.
- `003291B0` — `3839F0(ctx+0x180)` (0x80-byte FF fill →
  `obj+0x200..0x27F`) + two 16B copies `ctx+0x50`→`ctx+0x80`/`+0x90`
  when the explicit srcs are null.
- `0033C9B0` — `336710(stack_ctx, obj+0x80)` compose (field copies +
  `ctx+0xF0 = 236820(b[q[obj+0x1E8]+0x177])` elem resolve +
  `3272A0()` singleton gate — null under fixtures → deep arm skipped)
  → `33E1F0(stack_ctx)` (`q[ctx+0xF0]`/`q[+0xE68]`/`b[+0x18]>>1&7==2`
  deep arm — not taken; then unconditional `and dword [q[ctx+0x100]],
  0xFFFF8000` / `and byte [+0x21], 0xFE`) → `808C40` cookie.
- `00310780` (`l310780`, already real), `0016D6A0` (`l16d6a0`,
  shipped no-op), `0031B7E0` (`l31b7e0`, real) — unchanged.

## Corrections of record

- **`3105D0` calls `310780(obj)` unconditionally after the `+0x698`
  gate** — the stub hid the detach call; `u0fc0-fast`'s `l310780`
  count is now 1 (was 0). `bc970` gains the internal `30C970` hits
  (`b[+0x694]` inside `310780`, `b[+0x695]`/`b[+0x696]` inside
  `3105D0`) — 88 total, all recorded with real arg bytes.
- **`300280`→`3008A0` runs inside every real `3105D0`** when
  `b[rec+5]`==0 — `a630r9-swap`'s `a08a0`/`v2fd8d0`/`m2fd150` pins
  move 2→3 / 3→4 / 2→3, and `a630r9-oldff`/`oldfoe`/`new1k`/`newff`
  `a08a0` 1→2. These are count-pin corrections to the shipped call
  surface, not weakened asserts.
- **`d[obj+0x788]` ends 0, not 0xFF** (`l01140-rel`): `301140`'s own
  `d[+0x788] &= ~0x400` runs *before* `3105D0`, and `316CF0`'s
  `+0x778..+0x97F` memset zeroes it after — shipped ordering verified
  end-to-end.
- `w[obj+0xDC8]`=FFFF after `300280` under `b[rec+5]`==0 — the
  shipped registry dispatch (`309F30`→`2FD8D0`, `q[+0x48]`→`2FD150`)
  executes and bails on shipped-null page tables.

## Fixture disclosure

| fixture | maps to | notes |
|---------|---------|-------|
| `objlink` (extended) | `q[objrow+0x1E0]`/`q[objrow+0x1E8]` | `33E1F0` and-writes `q[ctx+0x100]` (=obj+0x1E0) unconditionally; `336710` derefs `q[obj+0x1E8]` (+0x177 idx byte for `236820`, +0x108 float). 0x40/0x200 byte scratch blocks. |
| `OBJCNT`/`OBJARR` (pre-existing) | `d[0x208E6A0]`/`q[0x208E688]` | the `236850`/`236820` loop runs live under `objlink` — `d[oarr+i*0xF50+0xEA0] &= ~(1<<b[obj+0xEA9])`. |
| `rec_b[5]` (pre-existing) | `b[q[obj+0x698]+5]` | `300280` gate — 1 → skip `3008A0`/`254EE0` arms; 0 → real dispatch. |

## Assert upgrades

`by("u3105d0")` → `byr("l3105d0")` ×10 assert sites across
`b140-*`/`a630r9-swap`/`u43f0-gate0`/`w4450-*`/`g3910-e5`/
`u0fc0-*`/`l01140-*` (same arg slots — rcx=obj). New write evidence
on `u0fc0-fast` (`w[obj+0x714]`=FFFF, `d[+0x690]`=0, `d[+0x768]`=0,
`b[+0x694..0x696]`=FF) and the `l01140-rel` ordering correction.

## Scripted boundaries still recorded

`30FED0` (`fed0` ×196), `2EB0D0` (`kb0d0` ×26), `319490` (×19),
`2E42D0` (×18), `3B02A0`, `46AB10`, `8632B0` (`b32b0`),
`30C970` (`bc970` ×88 — `3105D0`/`310780`'s mode-byte sink),
`319420` (`b9420`), `319140` (`b9140`), `238BF0` (`d8bf0`),
`317ED0`/`3180F0`/`319CA0`, allocators.

## Fault census

20 intentional-null fixture fault records across 10 cases, unchanged:
`ac80-member-nulld`, `ac80-foe-nulld`, `ac80-foe-oidx28`,
`ac80-foe-globnull`, `l8b40-nomemt`, `a8ff0-nodesc`, `c650-nolvl`,
`u0fc0-norec`, `l01140-norec`, `d228-globn`.
