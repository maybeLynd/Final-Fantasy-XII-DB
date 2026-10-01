# SD-3: what capability-policy bit 21 changes (OPUS, 2026-09-30)

Register row SD-3 was registered by SWE2-DATA (`f7a3292bd`, capability-inhibition-policy.md §7). Bit 21 of the aggregate
policy is set and cleared ~~only~~ by the Save/Load controller's handlers *(corrected 2026-09-30, OPUS: not only them; the movie player, `0023FBE0`, `002CEB40` and `003939B0` also write row 1, and `00394070` row 0 — [`sd3-bit21-pause-0930`](../sd3-bit21-pause-0930/README.md) W1)*, on row 1 (the page's four encodings, `005823F8` /
`0058252C` / `005828B4` / `00582F1B`). It is consumed by `00229AF0` (Audio) and `00228380` (input), "whose bodies decide
the effect". This record reads those bodies. It is static. The checker is `sd3_bit21.py` (output `sd3_bit21.out`,
`FAILS 0`). **Status proposed: NARROWED.**

## What the bit changes (OPUS)

**1. The full-screen audio hold is skipped (A1, A2).**
- **Where it runs:** `00229AF0` runs from the full-screen state's event handler. That is
  `Phyre::VTS::ScreenStateFullScreen` slot 5 (`007A3B20`, vtable `01CB3FA8`). On event 4 with `[rdx + 4]` = 0, it sets
  state 3 and, unless `00228480()` refuses, tail-jumps through `0017D4B0` to `00229AF0`.
- **Bit clear:** `00229AF0` calls `Audio_SetGroupMask(0x3F, 1, 1)`, holding audio groups 0–5 (the mask mirrors the
  driver's group-hold mask, per what-the-engine-calls-to-make-a-sound.md, answered 2026-09-17). It skips this only if
  `00226BD0(0xF)` is non-zero.
- **Bit set:** it returns the row-1 policy word (`002E1020(1)`) instead, and no hold is applied.
- **So:** while the Save/Load controller holds bit 21, a full-screen state change does not hold the game's audio.

**2. The input arbiter's modal changes (I1, I2).** `00228380`'s only caller is `00253C70`, on the input arbiter's
path. It normally carries a flag of 1 into `002282F0`. With bit 21 in the aggregate it reads row 1:
- **Row 1 lacks bit 21:** it returns 0 at once, and no modal is opened.
- **Row 1 has bit 21 (the Save/Load writers' row):** the flag becomes 0.
- **The modal:** `002282F0(flag)` creates, once, the widget with handler `00229590` (`0xD0` bytes, factory
  `00244F50`), puts the flag at payload `+8`, and keeps it at `[01FD4940]`.
- **So:** during a Save/Load operation, the arbiter's modal is opened in its flag-0 variant.

## Limits (OPUS)

- **Still open:** what the modal `00229590` does with flag 0 against flag 1, and what event 4 of
  `ScreenStateFullScreen` is (a focus or mode change is the likely reading, but it is not read here). These two decide
  the player-visible meaning.
- **Static only.** When the Save/Load handlers set and clear the bit, relative to a save's progress, is on the page's
  side.

**Review:** routed to SWE2-AUDIT-SPEC (OPUS production → FABLE-side review). The register row belongs to SWE2-DATA's page.
