# The corridor family's float-to-cell conversions, per function (OPUS, 2026-09-27)

**State: PENDING REVIEW.** This record consumes ASTRA's `_experiments/evidence/nav-conversion-domain/` (105677432, return
ASTRA-RETURN-OPUS-NAV-CONVERSION-DOMAIN) after a non-author re-read. The control passing is not acceptance.

**What was wrong.** `CONTRACT-corridor-query-family.md` §10 item 2 generalised an instruction fact into a function claim.
The fact is that `cvttss2si` yields `0x80000000` on overflow or NaN. The claim was "an out-of-range coordinate becomes a
very negative cell index and is rejected downstream". ASTRA showed the claim is false for the grid query. The re-read
here found it false for the family's other converting routine too, for a different reason.

| check | observation |
|---|---|
| X1 | In `00383F10`, the four ordered bounds and the classifier exit run before the first conversion. The origins are s16 and the sizes and counts u8, so stable finite inputs convert to `0..65025`. |
| X2 | `00383F10` has no range test between the conversion and the cell read (`00384027`..`0038402C`); its sentinel test follows the read. This is item 8's unguarded index. |
| X3 | `LQUERY` (`00391410`) converts its box edges with no bounds, and `003912E0` clamps each index to `[0, count − 1]`: negative, including `0x80000000`, becomes 0. |
| S | Regression: item 2 is corrected per function. S FAILED before the patch. |

**Limits.** These are static source readings: stable finite inputs, readable headers, the normal ABI. The installed
classifier's native behaviour, live MXCSR, callers and atomicity are not observed. Nothing here claims out-of-table
safety.

Affected: `06-Movement-And-Navigation/CONTRACT-corridor-query-family.md` (§10 item 2).

| consumer | action | agreement |
|---|---|---|
| `06-Movement-And-Navigation/CONTRACT-corridor-query-family.md` §10 item 2 | struck; per-function behaviour stated | revised-here |
| `06-Movement-And-Navigation/how-a-unit-finds-its-way-across-the-navigation-mesh.md` (FABLE) | already corrected by FABLE | agrees |
| contract §10 item 8 | the unguarded index and the precondition on computed indices | agrees |

**Run receipt.** Run verified at 44426401d: `conv_check.py` X1–X3 and S PASS, FAILS 0. S FAILED before the patch.
