# EXP-203 — `0028FBE0` dispatch consumers `00296E90`/`00297040`, executed

**Status:** complete — **418/418 cases, stable across 3 independent runs,
byte-identical `result.json` (SHA256
`75bcd73a0257e851d37049ef71a45c45b05f2c9721af858239591ca4e62eb661`), zero
unexpected faults.**
**Evidence class:** `NATIVE-REPLAY` (`live_game: false`). Shipped bytes executed
under Unicorn; synthetic fixtures disclosed below; none claim
initialized-gameplay reachability.
**Harness:** `_experiments/evidence/member-block-chain-exec/check.py` (extends
EXP-192..202; 407 inherited + 11 new `e690-*`/`p7040-*` direct-entry cases)
**Result:** `_experiments/evidence/member-block-chain-exec/result.json`
**Image authority:** FFXII TZA shipping EXE, SHA256
`73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`.

## Scope

EXP-202 ended with the `0028FBE0` subtype dispatch *observed firing* into
scripted `00296E90`/`00297040` sinks. Both turn out to be small flag-setters
over a `0x160`-stride slot array inside the dispatch controller's handler
object — this package promotes them to executed bodies and asserts the real
writes, so the whole wrapper → queue → dispatch → consume chain now runs
native end-to-end.

## `00296E90(ctrlsub, id)` — slot flag setter, bit `0x10`

- `rcx == 0` → return (`e690-null`: no resolve call at all).
- `idx = 00273320(id)` (still scripted — `s273320`); `idx < 0` → return
  with no writes (`e690-bad` drives `s273320_ret=-1`; the call carries
  `rcx = id = 7` — `mov ecx, edx`).
- `rdx = idx*0x160`; `w[ctrlsub+rdx+0x318] |= 0x10`;
  `w[ctrlsub+rdx+0x350] = 0` — an OR-accumulate (`e690-or`: `0x40` preset
  → `0x50`) plus a paired zero-word; `idx 2` writes at `+0x5D8` leaving
  slot 0 untouched (`e690-idx2`).

## `00297040(ctrlsub, id, flag)` — flag setter, bit pair

Same resolve; then:

- `flag == 0` (r8d): `w[idx*0x160+0x318] |= 0x20`; `w[+0x354] = 0`
  (`p7040-f0`, `p7040-idx2`).
- `flag != 0`: gated on `b[idx*0x160+0x31E] != 3` — `== 3` → return with
  no writes (`p7040-f1g3`); otherwise `w[+0x318] |= 0x40`;
  `w[+0x356] = 0` (`p7040-f1`).
- `rcx == 0` → return before the resolve (`p7040-null`).

## End-to-end dispatch now native

With the sinks real, the `d3d0-*` cases assert memory rather than stub
records: subtype 2/6 (arms 1/5) → `w[ctrlsub+0x318] == 0x10`; subtype 7
(arm 6) → `0x40` + `w356 == 0`; subtype 1 (arm 0) → `0x20` +
`w354 == 0`; subtype 4 (arm 3) and subtype 8 (`subtype-1 > 6`) leave
`w318` untouched. `rargs` records `rcx == ctrlsub` on every dispatch.

## Corrections of record

- **EXP-202's new-case asserts were unreachable in the committed
  harness**: the EXP-201 assert group's predicate was
  `startswith(("fa3b0-","fmt-","bd00-","d4d0-"))` — `d3d0-*`/`d480-*`
  fell through the elif chain and passed vacuously (the probe output they
  were based on was correct; only the assert wiring was dead). The
  predicate now covers `d3d0-`/`d480-`/`e690-`/`p7040-`, and the `d3d0-*`
  dispatch asserts check real `ctrlsub` flag writes instead of stub call
  records. This is exactly the failure mode the negative-claim discipline
  exists for; it is recorded here rather than silently fixed.
- `ctrlsub` allocation widened `0x40` → `0x4000`: the sinks write at
  `idx*0x160 + up-to 0x358`, so a `s273320_ret` index ≥ 1 previously would
  have scribbled past the fixture block.
- `00273320` remains the sole scripted edge inside both sinks — it is the
  id→slot-index resolver shared with the wider battle-display table
  machinery (scripted since EXP-201 alongside `002B3050`).

## Validation

`python check.py` — 418/418, three independent runs, `result.json` SHA256
`75bcd73a0257e851d37049ef71a45c45b05f2c9721af858239591ca4e62eb661`
identical each time. New fixture: `csb` (byte presets on `ctrlsub` —
flag-word and `b31E` gate presets). No inherited-case regressions.

**Not claimed:** live-game reachability. `00273320` (id resolver),
`0031C5D0` (resource resolver) and `002B3050` (string copy) remain the
scripted boundaries on this path — `00273320` is now the deepest scripted
edge inside the dispatch consumers themselves.
