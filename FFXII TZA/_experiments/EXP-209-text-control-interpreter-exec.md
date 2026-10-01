# EXP-209 — `002AC5F0` text-control-code interpreter, executed

**Status:** complete — **455/455 cases, stable across 3 independent runs,
byte-identical `result.json` (SHA256
`4cca9cf5cd73a2282247487108f6cd6ef060430a1fd401f91f38a68a78f323c6`), zero
unexpected faults.**
**Evidence class:** `NATIVE-REPLAY` (`live_game: false`). Shipped bytes executed
under Unicorn; synthetic fixtures disclosed below; none claim
initialized-gameplay reachability.
**Harness:** `_experiments/evidence/member-block-chain-exec/check.py` (extends
EXP-192..208; 450 inherited + 5 new `c5f0-*` direct-entry cases)
**Result:** `_experiments/evidence/member-block-chain-exec/result.json`
**Image authority:** FFXII TZA shipping EXE, SHA256
`73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`.

## Scope

EXP-208 promoted the walkers `002B2150`/`002AF340` and left the
interpreter scripted. This package promotes `002AC5F0` itself — the
15-arm control-code dispatcher below the walkers — plus five small leaf
helpers it calls (`00229E40`, `0024ABA0`, `002B1F20`, `002B2C50`,
`002B2D20`). The deep machinery stays scripted: `002A9F00` (glyph
engine), `002B2DF0`/`002B43C0` (walker wrappers), `002AB820`,
`003FFDF0` (tag-14 param parser), `002B3E30`, and the `0017Fxxx` font
shims (`17F880` height, `17F850`, `17FA10`, `17FB00`, `17F920`,
`17F9C0`, plus the existing `17F940`/`17FAE0`/`17F8C0` boundaries).

## `002AC5F0(state, &cursor_cell, params, &aux_dword)`

`rdx` is a pointer to the cursor cell (`q[rdx]` = char ptr) — unlike
`002B2150`, which takes the char pointer directly. Head:

- `*r9 = 0` on entry.
- `b[cursor] == 0` → return `0`, cursor untouched (`c5f0-nul`).
- `q[state+0x10C8]` nonzero → match-word gate: `w[match] == w[cursor]`
  → return `0` (`c5f0-match`, `w[c60]=w[nstr]=0x41`).
- `b[cursor] ∈ 1..0xF` → jump table at `0x2AE334` (15 entries, read
  from shipped bytes):

  | tag | arm | behavior |
  |-----|-----|----------|
  | 1,4,6,7 | `0x2ACB96` | shared arm |
  | 2 | `0x2AC6D1` | nested `002B2150` |
  | 3 | `0x2AC6AE` | |
  | 5 | `0x2ACCF3` | space/advance (below) |
  | 8 | `0x2AD011` | cursor `+= 3`, ret 1 (`c5f0-tag8`) |
  | 9 | `0x2AD008` | cursor `+= 1`, ret 1 (`c5f0-tag9`) |
  | 10 | `0x2ACE25` | tag-5-family arm + char scan for `02`/`05` |
  | 11,12,13 | `0x2AC6CA` | no-op, ret 0 → walker break (`b2150-brk`) |
  | 14 | `0x2AC825` | parameterized format (below) |
  | 15 | `0x2AD01A` | second dispatch table (`0x2AE370`/`0x2AE3FC`) |

- Shared tail `0x2ACFA4`: `f[0209CC68] = xmm6`, `f[0209CC64] = xmm7`,
  `q[0209E598] = 0`, `17FAE0(0)` font-slot clear, `eax = 1`.

### Tag 5 — space/advance (`0x2ACCF3`)

- `254A10()` gate; if 0 → `229E40()` (global dword read, real). Then
  `24ABA0()` → shipped consts `448/448 = 1.0f`.
- `cvttss2si(1.0 * f[0x916314]=15.0)` → `xmm6 = 15.0` — the space
  advance, shipped-derived, not a fixture.
- Writes `b[q[0209CC40]+0x10FC] = 0` — the mode byte is cleared on the
  **global** ctx, not the passed state.
- `ctx48` (`q[0209CC48]`) == 0 arm: `f[ctx+0x10EC] = max(f10EC,
  f[r12] + 15 + f10F8)`; `b[ctxo+0x1100] = 1` when `b1101 == 0`.
  `ctx48 != 0` arm instead reads `d[state+0xB0] & 0x800000` →
  `f[state+0x80] + 2*d[01E0CDC0]*s34*s38` and clamps `xmm6` to the
  remainder (`xmm1 - f[r12]`).
- `f[0209CC68] = xmm6 + f[state+0x4C]`; `17F880()` → `f[0209CC64]`
  (height; scripted `f880v` default `6.5`).
- `d[r9] = 1` (aux out), `q[rdx] += 1` (cursor).
- `ctx48 == 0` → **nested `002B2150(state, cursor+1, &stack_f, 0)`** —
  inline measure of the remaining run; `f10F4 = max(f10F4, result)`.
  Proven live: `b2150-lite` records 2 `l2b2150` entries, `b24b0-run`
  records 3 (outer + one per walker walk). `r9 = 0` at this call site —
  `002B2150`'s height-out write tolerates the null.

Net effect under `\x05`: width `15.0`, height `6.5` → `2AF340` flush →
`ceilf` → **15×7 px** in `bd00-t2`/`b3120-ok`/`b3050-run` (replacing
EXP-208's stub-driven `18/5`).

### Tag 14 — parameterized format (`0x2AC825`)

- `003FFDF0` (scripted) parses the param block; `d[rsp+0x48] == 0` →
  `b[ctx+0x10FE] = 1` (`sete`), `b[ctx+0x1101] = 1` — both observed on
  `ctxo` in `b24b0-acc`.
- `002B2DF0` wrap call (scripted `f2df0`), float combination /
  metric compares; the param loop touches `002A9F00`/`0039C4A0`/
  `002B43C0` boundaries.
- **Returns `0`** — `002AF340` treats it as a break, sees `b==0xE`,
  fires its own post-break `002B3E30` arm (`af340-tage`, `f24 = 8.0`
  from `d[01E0CDE8]`); `002B2150` takes its break-merge exit.
- The `b10FE` mark feeds `002B24B0`'s accumulate:
  `f10F4 += 2*d[01E0CDC0=16]*s34*s38` → `acc+ec = 32 > measure 0` →
  `f[+0x54] = 32` (`b24b0-acc`, `b3120-tage` → `w1 = 32`).

### Tags 11–13 — ret-0 no-ops

`0x2AC6CA`: return 0 with no cursor advance or state write → the
caller's break path (`b2150-brk` on `\x0B`: `eax = 0` consumed, zero
outs).

## Fixture disclosure

- Strings are synthetic byte streams at `nstr` (`strb`); `ccp` is a
  synthetic cursor cell for direct entry. `e312` is the `0xD0` state
  struct; `ctxo` (`q[0209CC40]`) is the planted global text ctx.
- Scripted-return fixtures: `f880v` (height float, default `6.5`),
  `f2df0`/`f2b43c0` (walker-wrapper floats), `f3ff0` (param-parse
  byte count), `f940v` (font-slot value, `0x1234`), `c2f0` (heavy-byte
  decode queue), `eflags` (element flag bits).
- `448/448`, `15.0f`, `d[01E0CDC0]=16`, `d[01E0CDE8]=8` are
  **shipped** constants — read from the image, not fixtures.

## Corrections of record

- `rdx` in `002AC5F0` is `&cursor` (cell pointer), not the char
  pointer — the case-table key is `edx`; `rdx=` was silently ignored
  and defaulted to `w.sel=2`, faulting on `q[2]` (same trap as
  EXP-208's `b24b0` entries).
- `b10FD` (the `002B3120` return byte) is **read-only** in this whole
  family — no arm writes it; the previous `-1`/`5`/`3`/`2` return
  values were stub artifacts (`ctxrb` fixture). Real behavior: ret
  `eax = 0` from these streams.
- `002AC5F0`'s ctx writes (`b10FC`, `b1100`, `b1101`, `b10FE`,
  `f10EC`/`f10F4`) target the **global** `q[0209CC40]` object; the
  walkers' save/restore covers the passed state struct — so the
  interpreter's marks persist on `ctxo` (asserted), while `002B24B0`'s
  wider field save/restore still round-trips `b10FC` to `0xAB`.
- Tag-5's advance is `int(1.0 × 15.0) = 15` shipped units, and it
  clears the mode byte and fires its own nested measure under
  `ctx48==0` — three `l2b2150` entries per `b24b0` run, not one.
- Tag-14's arm **returns 0** — the `002B3E30` reachability from
  `002AF340` flows through the ret-0 break, not a direct call.

## Boundary status

Native this package: `002AC5F0`, `00229E40`, `0024ABA0`, `002B1F20`,
`002B2C50`, `002B2D20` (plus everything EXP-192..208 promoted).

Scripted boundaries remaining on the text path: `002AC2F0` (heavy-byte
decode), `002A9F00`, `002B2DF0`, `002B43C0`, `002AB820`, `003FFDF0`,
`002B3E30`, `002B1F20`'s siblings, the `0017Fxxx` shim family
(`17F850/880/920/940/9C0/A10/AE0/B00/C0`). The `002AC5F0` shared arms
(`0x2ACB96` for tags 1/4/6/7, tag-3 `0x2AC6AE`, tag-10 `0x2ACE25`,
tag-15 `0x2AD01A` and its second-level table) execute native but
remain fixture-light — deeper exercise needs parameterized fixtures
for `003FFDF0`'s parse block.
