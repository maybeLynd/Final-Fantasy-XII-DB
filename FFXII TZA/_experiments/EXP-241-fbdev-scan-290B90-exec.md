# EXP-241 — fbdev device-list scan `290B90` real

**Status:** complete — **542/542 cases, stable across 3 independent
runs, byte-identical `result.json` (SHA256 `1ba3c747` prefix; 542
cases), fault census unchanged at 20** (the same pre-existing
intentional-null fixtures).
**Evidence class:** `NATIVE-REPLAY` (`live_game: false`). Shipped bytes
executed under Unicorn; synthetic fixtures disclosed below; none claim
initialized-gameplay reachability.
**Harness:** `_experiments/evidence/member-block-chain-exec/check.py`
(extends EXP-192..240; 34 existing cases gained `fbdev` plants;
asserts retargeted and extended, none weakened).
**Result:** `_experiments/evidence/member-block-chain-exec/result.json`
**Image authority:** FFXII TZA shipping EXE, SHA256
`73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`.

## Body promoted real this round

`00290B90` (`l290b90`, ×34 — the largest remaining scripted tag) —
the device-list scanner `319140`'s `edx&1` arm (and siblings) call
with `ecx` = `d[obj+8]` id:

```text
o = q[0x209BE80]                 ; fbdev device-owner cell (BSS-null
rdx = q[o+0x10F10]               ;   shipped -> stub era)
if !rdx: ret 0
loop:
    if d[rdx+0x810] == ecx:      ; node id match
        eax = low32(rdx)         ; truncated pointer — nodes live
        if w[rax+0x850] == 2:    ;   below 4GB in-game and in the
            w[rax+0x850] = 3     ;   fixture arena alike
        eax = 1
    rdx = q[rdx+0x868]           ; next
ret al                           ; 1 if any match, else 0
```

## Fixture (disclosed)

`fbdev` already existed as a truthy plant for `28FB80`'s paired
writes (`d228-gate5` uses `fbdev=1`). This round widened its alloc
0x6000→0x12000 so `q[obj+0x10F10]` (the list head) is in-bounds, and
added `fbdev={"nodes":[{id, w850}, …]}` — each node gets
`d[+0x810]=id`, `w[+0x850]=w850`, chained on `q[+0x868]`.

- **33 cases** (`f340-bit10`, `b140-td`, `a630r9-*` ×9, `u43f0-*` ×5,
  `w4450-set`, `g3910-e5`, `u0fc0-*` ×8, `l01140-*` ×7) plant
  `fbdev=1` — object present, **list empty** → real scan returns 0,
  matching the stub era's observable output but now shipped-computed.
- **`u0fc0-s800`** (the sole `ecx=9` caller — `d[obj+8]`=9) plants
  `fbdev={"nodes":[{"id":9,"w850":2}]}` → the real match arm folds
  `w[+0x850]` **2→3** and returns 1 — pinned: `l290b90(rcx=9)` ×1 and
  `gm.w16(node+0x850)==3`.

## Blast-radius check

`q[0x209BE80]` readers besides `290B90` (`290BE0`/`290C00`/`290C50`/
`290C60`/`290C80`/`290CA0`/`290CF0`, and EXP-236's `28EF70`/`28EF00`)
are either scripted (no memory reads) or have **no harness-reached
caller** — verified by `.text` E8/E9/data scans; the only image edge
into `290B90` is direct calls from `319140`'s arm and family. The
`fbdev` plant is per-case (`fbdev` key), so non-calling cases keep
the BSS-zero cell.

## Shipped-value pins

`u0fc0-def` retarget `by("s290b90")` → `byr("l290b90")` (rcx==0).
`u0fc0-s800` new pins: `l290b90` ×1 rcx==9; `w[node+0x850]`==3 (the
2→3 fold that only runs on a real match).

## Corrections of record

- `fbdev` reused rather than duplicated — an earlier session's
  `fbdev=1` key already planted `q[0x209BE80]` for `28FB80`; the
  node-list wiring extends it, and the alloc widened for `+0x10F10`.
  A `fbdev={}` empty-dict plant is falsy under `case.get` — the 33
  callers use `fbdev=1` (same convention as `d228-gate5`).
- All 33 empty-list calls now return an explicit `eax=0` where the
  stub preserved `rax` — observable callers don't read the result on
  those paths (suite green, no assert changed).

## Boundaries (unchanged disclosures)

`30E130` (`e130` ×0), `317E50` (`b7e50` ×0), `20CE60` (`v20ce60` ×0),
`427320` (`v427320` ×1), `422C20` (`v422c20` ×1), `3377C0`
(`v3377c0` ×19), `28EF70`/`28EF00` (×1/×0 — same `q[0x209BE80]`
cell, but scripted handlers read no memory; an fbdev-planted case
reaching them would now observe the object), `2E8FD0` (`v2e8fd0`
×1), `3B02A0`, `46AB10`, `210EC0`, `1CCB20`, `3180F0`, `319CA0`,
`426130` remain scripted. `live_game: false`.
