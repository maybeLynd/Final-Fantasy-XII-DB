# Consumer check: falsification pass 1 on how-an-animation-makes-a-sound (OPUS, 2026-09-29)

corrects: 18-Audio/how-an-animation-makes-a-sound.md (sections 2 and 6: CON-190)

## What was corrected

- **CON-190.** The sound picker `0046C250` draws only through `003A6E60`, the presentation bit-feedback PRNG on
  `01EF93E8`. It does not draw from a gameplay generator, so swings and voices never move a combat roll.
- **Added:** types 4 and 5 are silent when `003326C0` finds nothing for emitter word `+8`.

## Current consumers

- consumer: `18-Audio/which-variation-of-a-sound-you-hear.md`, the 2026-09-20 scoping note ("with the gameplay generator");
  revised-here.
- consumer: `18-Audio/README.md` ("a picker that rolls the gameplay generator"); revised-here.
- consumer: `21-RNG-And-Determinism/CONTRACT-which-generator-serves-which-roll.md` row 4 ("procedural rendering"); it
  agrees, since it names no gameplay consumer of `01EF93E8`.
- consumer: `02-Resource-And-Asset-Pipeline/Authored-Expressions/how-an-authored-number-gets-its-randomness.md` already
  places `003A6E60` on `01EF93E8`; it agrees.
- consumer: `_index/CONTRADICTIONS.tsv`: revised-here (`CON-190`).

## Regression

regression: `Database/Tools/analysis-kit/gfz-scripts/falsify_animation_sound.py` S2. It fails unless the picker's only
draw callee is `003A6E60`, its call set is exactly four named callees, and `003A6E60` stores to `01EF93E8`.

run: verified at ed127d443 (BROKEN 0, exit 0), against the certified image `73461d08…`.
