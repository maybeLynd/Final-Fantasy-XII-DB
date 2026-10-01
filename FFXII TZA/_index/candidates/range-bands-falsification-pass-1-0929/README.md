# Consumer check: falsification pass 1 on how-close-a-unit-must-stand-to-act (OPUS, 2026-09-29)

corrects: 07-Combat-Action/how-close-a-unit-must-stand-to-act.md (section 1 step 5 and section 7: CON-187)

## What was corrected

- **Both components, not either.** The band builder `002FEB80` authors the bands (near `a`, middle `a + b`, reach
  `a + b + R`) only when both inner components are non-zero. `002FECAA` skips the test of `b` when `a` is 0.
- **Additions, not corrections:**
  - the builder's weapon bound is one-sided (id < count + `0x1000`), and the empty `0xFFFF` fails it;
  - a null equipment row is kind 0 in `00320D70`;
  - two early exits in `00338140`, and its avoidance attempt before the stand tail;
  - `00337A50`'s speed gate `+0xB0`, and its stand window `30 x [01DFE0B4]` (the frame limit).

## Current consumers

- consumer: `17-Presentation-Rendering/Model-And-Motion-Formats/fcp-character-parameter-block.md` section 6.1 describes
  `00320D70` only ("no equipment -> 0" agrees with the addition) and defers the combination to this page; it agrees.
- consumer: `07-Combat-Action/README.md` names "the `0.6` / `0.8` fallback" without its condition; it agrees.
- consumer: `04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md` places the storage (`+0x6D4`..`+0x6DC`) only; it
  agrees.
- consumer: `_index/CONTRADICTIONS.tsv`: revised-here (`CON-187`).

## Regression

regression: `Database/Tools/analysis-kit/gfz-scripts/falsify_action_range_bands.py` B4. It fails unless `002FECAA` is
`je 002FECB8` (a zero `a` skips the test of `b`) and `002FECB3` is the only store of 1 into `ebx`.

run: verified at c9e6a606b (BROKEN 0, exit 0), against the certified image `73461d08…`.
