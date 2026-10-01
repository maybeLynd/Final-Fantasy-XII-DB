# EXP-208 — `002B2150`/`002AF340` segment-string walkers, executed

**Status:** complete — **450/450 cases, stable across 3 independent runs,
byte-identical `result.json` (SHA256
`78ec7301de9ff9e9f484071fa7a195d3d4dd637c1b52c2925b6dd41e172a12c1`), zero
unexpected faults.**
**Evidence class:** `NATIVE-REPLAY` (`live_game: false`). Shipped bytes executed
under Unicorn; synthetic fixtures disclosed below; none claim
initialized-gameplay reachability.
**Harness:** `_experiments/evidence/member-block-chain-exec/check.py` (extends
EXP-192..207; 441 inherited + 9 new `b2150-*`/`af340-*` cases)
**Result:** `_experiments/evidence/member-block-chain-exec/result.json`
**Image authority:** FFXII TZA shipping EXE, SHA256
`73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`.

## Scope

EXP-207 promoted `002B24B0` and left the two inner measurers scripted.
This package promotes both walkers plus the `0xD0` state initializer
`002AC1E0` — the display path is now native from `002B3050` all the way
through the per-character walk. Their heavy helper subtree stays bounded:
control-code decode (`002AC2F0`), the text-control interpreter/glyph
measure (`002AC5F0`), the tag-`0xE` params adjuster (`002B3E30`), and the
`0017Fxxx` font shims (`17F940`/`17FAE0`/`17F8C0`) are scripted
boundaries; `0020E600` (element-base thunk), `00861ED2` (`memcmp` via
VCRUNTIME IAT) and the cookie check run native.

## `002B2150(&state0xD0, cursor, &width_out, &height_out)`

Single-line segment-string walker. Copies the `0xD0` state onto its frame,
then:

- **Save/clear/restore set:** `b[ctx+0x10FC]`, `b[ctx+0x10FF]` (the
  typewriter mode bytes — restored on exit; `b2150-lite` proves `0xAB`/
  `0xCD` round-trip), outer ptr `q[0209CC48]` (cleared for the walk,
  restored — `cc48mid=0` inside `s2ac5f0`, `0x77` after), the font ctx
  `+0x28` value via `17F940` getter / two `17FAE0` setter calls
  (recorded `[0, 0x1234]` — clear-then-restore), `q[0209E598]`, and the
  `0209CC60`-band scratch cells.
- **Per-byte walk** (`rbx` cursor over `rdx`, `r15` = entry `rdx`):
  - `b > 0x0F` (control code): `002AC2F0(&copy, &cursor)` → `eax` index;
    `d[q[copy+0x60]+0xC]` selects the element offset via `0020E600`;
    `0017F8C0` remap; flag `d[elemb+off+idx*8]` tested vs `0x80000000` —
    set → `b10FC = 1`, and when already `2` the scale advance
    `xmm6 += f[copy+0x34] * 2.3f * f[copy+0x38]` fires (`b2150-adv`:
    `2.0*2.3*3.0 = 13.8` lands in the width out); clear → `b10FC = 2`.
  - `b <= 0x0F`: `q[ctx+0x10C8]` is a **match-word cursor** —
    `w[q10C8]` is compared against the current seglist word; match, or
    `cl==0`/`cl==2`, exits via the merge tail. Otherwise
    `002AC5F0` measures the lite node; `eax==0` → break merge
    (`xmm6 += f[0209CC68]`), else the cursor cell advance plus per-node
    `xmm6 += f[0209CC68]`, `xmm7 = max(f[0209CC64], xmm7)`.
- **Exit:** `xmm6 += f[0209CC60]*f[copy+0x40]`; `f[r8] = xmm6` (width),
  `f[r9] = xmm7` (height — `2B24B0` passes `&ctx+0x10E8`, which is why
  that field doubles as the line-height slot it snapshots); **return
  `rbx − r15` = bytes consumed** (`b2150-lite` → 1).

## `002AF340(&state0xD0, cursor, &params, r9gate)`

The multiline/layout walker — same save/restore skeleton plus
`q[copy+0x30]/+0x38` zero-init, `d[rsp+0x20] = (b[r15]!=0)` where
`r15 = q[ctx+0x10C8]` is the source string. Distinct behaviors proven:

- **Heavy arm** (`af340-heavy`): `b1102 = 0`, `f10 += f[0209CC68]`, the
  same decode/flag/`b10FC` chain, `r12d++` → return count.
- **memcmp arm:** `memcmp(r15, rbx, strlen(r15)) == 0` → `r13d = 1` →
  the walk treats it as a matched terminator (`00861ED2` = VCRUNTIME
  `memcmp`, run native).
- **`b==0` or match → final flush + exit** (`0x2AF832`): the same
  flush as tag-3 then `f30 += f[0209CC60]*scale` — **the ret-0
  `2AC5F0` break skips this flush entirely** (`af340-run`: unflushed
  `f30/f34` stay `0`; `bd00-t2` uses `c5f0=(1,1)` so the NUL flush
  lands `17.9/4.2` → `ceilf` → `18/5`).
- **`b==3` — line break** (`0x2AF5B1`): `f24 += f14`;
  `f20 = max(f10)`; `f30 = max(f20)`; `f34 = max(f14+f24)`; reset
  `f14=f10=0`, `d1C = f24 = d2C = 1.0f`; cursor+1.
- **`b==2` — nested inline measure** (`af340-tag2`): `b1102 = 1`,
  `002B2150(&copy, cursor+1, &f34cell, &f38cell)`; nested outs merge
  `f10`/`f14` maxes, `ctx+0x10E8` updated when the nested height beats
  the running max; `f24 += d[0209CC3C]`; cursor+1.
- **`b==0xE` — params adjuster** (`af340-tage`): `002B3E30(params)`
  boundary, `f24 += float(d[0209CC3C])` (`8.0` shipped → `f24=8.0`).
- **Return** `r12d` (heavy-node count) — or `-1` under the `d[rsp+0x3C]`
  gate; the `+0x10FC` flag writes are **not** restored by `2AF340`
  (`af340-heavy` leaves `b10FC=1`) — that's `2B2150`'s restore layer,
  not this one's.

## Harness changes

- `REAL` += `0x2B2150`, `0x2AF340`, `0x2AC1E0` (the `0xD0` init —
  `memset` hook + `0039C4A0` tail already bounded).
- Scripted boundaries added: `s2ac2f0` (`c2f0` codepoint/advance
  sequence), `s2ac5f0` (`c5f0` ret/advance/r8-r9 out sequence),
  `s2b3e30`, `s17f940` (`f940v` getter value), `s17fae0`, `s17f8c0`;
  `_ctxr()` applies `ctxr*` + `af340f` → `f[0209CC68]`/`f[0209CC64]`
  inside the decoder stubs.
- Fixtures: `strb` (walker byte stream at `nstr`), `c60`/`c60d` (the
  `copy+0x60` flag-table object), `eflags` (flag dwords at
  `elemb+d[c60+0xC]+idx*8`), `e598v`, `params`, `ctxe8`.
- `e312q` now resolves string attrs (`"nstr"`/`"c60"`); `c60` is
  allocated **before** `e312q` so the attr resolves.
- `t3s` in `RES1A` is now a terminating lite stream
  (`\x00\x00\x05\x00` — two-byte tag + `0x05` + NUL), and `bd00-t2`
  carries `c5f0=[(1,1),(1,1)]` so both walkers' NUL flushes run.

## Corrections of record

- `rdx=0` in the `b24b0-*` cases was ignored — the key is `edx`;
  `w.sel=2` leaked into `q10C8` → `2B2150` read `w[2]`. Fixed to
  `edx="c60"` (zero-word match buffer = the shipped empty-const
  semantics; NUL matches it naturally).
- The `q[copy+0x60]` flag-table pointer must be a fixture — real
  `2AC1E0` zeroes it (`b2150-heavy`/`adv`, `af340-heavy` carry
  `e312q={0x60:"c60"}`); `0039C4A0`'s return no longer supplies it
  (that path only feeds `q[state+0x60]` from the `2B3050` arm).
- `2AF340`'s `s2ac5f0`-returns-0 break exits **before** the final
  flush — `f30`/`f34` stay `0`; measured dims only materialize on
  NUL/tag-3 flushes. `bd00-t2`'s `c5f0` sequence updated to match.

## Still scripted (disclosed)

`002AC2F0` (control decode), `002AC5F0` (interpret/glyph measure —
the entry to the ~131-body font engine), `002B3E30`, the `17Fxxx` shim
family, `0039BAD0`/`00254A10`/`0039C4A0`, `ceilf` (real math,
fixture-selectable), cookie.

## Validation

`python check.py` — 450/450, three independent runs, `result.json` SHA256
`78ec7301de9ff9e9f484071fa7a195d3d4dd637c1b52c2925b6dd41e172a12c1`
(byte-identical), zero unexpected faults.
