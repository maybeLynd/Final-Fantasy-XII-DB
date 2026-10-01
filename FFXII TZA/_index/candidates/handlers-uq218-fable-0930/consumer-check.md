# Consumer-check record - UQ-218 pass 18 applied to the authored-command handler page (FABLE, Claude Opus 5.5, 2026-09-30)

affected: `Database/FFXII TZA/17-Presentation-Rendering/Authored-Commands/the-authored-presentation-command-handlers.md`

## What changed

Answers `DATA-REQ-FABLE-HANDLERS-UQ218-P18`. The selectors paragraph said two things that SWE2-DATA's pass 18 has since
settled. Both are now struck, with the answer beside them:
- "the band names themselves are inference ... still not a code-proven band→name binding". It is a code path: op `0x0B`
  (`00417110`) plays `@FMC` record `list[result & 0xFFFF] + (result >> 16)` (`00417367`), and that record's op `0x09`
  names the `@FMN`.
- "Still open: which yaw sign is the character's left". A positive yaw delta is the left.

Neither struck sentence asserted anything false. They called the binding unproven and the sign open, and both now have
answers. Register row UQ-218 is already ANSWERED (SWE2-DATA, `29436f1ad`).

## Consumers

- `fef-and-motion-entries.md` carries the 2026-09-29 positional match the struck text cited. SWE2-DATA's pass 18 updated
  that page in `29436f1ad`, so it is not touched here.
- register row UQ-218: ANSWERED at `29436f1ad`; unchanged.

## Regression

`band_names.py` (SWE2-DATA, `_index/candidates/uq218-pass18-0930/`): S0/S1 (bands 3/4 bind `walk_l`/`walk_r` only),
T/T7 (turn bands by sign), R (kind `0xA` run pair), C (control: 33,753 op-0x09 indices all land on an `@FMN`) and P (the
code path, 10 sites).

run: band_names.py at 4e32dd8df (HEAD when FABLE re-ran it), FAILS 0
