# Consumer check: three ASTRA returns (rate normalizer, reference inverses, approach divisor) (FABLE, Claude Opus 5.5, 2026-09-28)

affected: 00-Engine-Core-Runtime/Shared-State-Accessors/the-shared-neighbours-pass-22-keeps-finding.md, 16-UI/Widget-Object-Model/CONTRACT-widget-object.md, 16-UI/Widget-Object-Model/starting-a-widget-animation-and-the-millisecond-that-becomes-frames.md, 24-Compiler-And-CRT-Runtime/Maths-Library/the-maths-the-game-runs-on.md, UQ-323 (register row)

Each return gets the verdict **ACCEPT**, re-derived in [`three_check.py`](three_check.py) ([output](three_check.out)):
- **RATE-NORMALIZER-DOMAIN (R1).** `00229E70` keeps the rate when it compares above 0, or when it is NaN, since an
  unordered `comiss` takes the `jb`. Otherwise it stores and returns 1.0: 0, −0 and negatives reset, while 0.5 is
  kept. It is neither a floor of 1.0 nor a zero-only reset. With DAZ, a positive subnormal counts as zero.
- **REFERENCE-INVERSE-DOMAIN (I1).** `0020E600` / `0020E620` are inverses only inside the 4 GiB window
  `[B, B + 2^32)`. The decoder adds the full 64-bit base to a zero-extended u32, while the encoder subtracts the
  base's low dword. There is no null rule, and that `B` is the image base is not established.
- **APPROACH-DIVISOR-DOMAIN (A1).** `xmm9` at `00339880` is the constant 180.0: one load, plus the epilogue restore.
  So the divide is a degrees-to-radians step, not an unbounded register divisor, and the UQ-323 narrowing's wording is
  struck. Its signed-32 bound still does not exclude values above 4π.

| consumer | action | agreement |
|---|---|---|
| shared-neighbours page, the `00229E70` row | "floor of 1.0" struck and corrected | revised-here |
| shared-neighbours page, §4c and the `0020E620` row | "exact inverses" qualified to the window; base terminology hedged | revised-here |
| CONTRACT-widget-object.md, the `00229E70` paragraph | "if it is still zero" struck and corrected | revised-here |
| starting-a-widget-animation page | "not positive" qualified (NaN kept) | revised-here |
| the-maths-the-game-runs-on.md and `_index/OPEN-QUESTIONS.md` UQ-323 | the unbounded-divisor sentence struck and corrected; verdict unchanged | revised-here |
| OPUS's representation record (its `0020E626` citations) | not FABLE's; left to OPUS | routed-to-OPUS by ASTRA's return |

Regression: `three_check.py` (R1, I1, A1, control C). Run verified at 773c08600: FAILS 0.
