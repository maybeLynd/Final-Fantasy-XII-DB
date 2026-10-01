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

## The piecewise clamp, and a check that could not see it (OPUS, 2026-09-28)

Consumed from ASTRA's `nav-mask-zero-count` (`ASTRA-RETURN-OPUS-NAV-MASK-ZERO-COUNT`). Its `check.py` was re-run and
reports PASS_STATIC_PIECEWISE.
- **The rule.** `003912E0` is `i < 0 ? 0 : min_signed(i, count - 1)`, not a plain `[0, count - 1]` clamp. Each
  negative path zeroes its register and jumps past the upper clamp, so the result is in `[0, count - 1]` only for
  positive counts. With a count of 0, a non-negative index becomes -1.
- **The producer defect was mine.** X3 checked the `test` / zeroing / upper `cmovg` but not where each negative path
  goes, so ASTRA's copy with the bypass `jmp` NOPped still passed.
  - **X4** now binds all four paths: `test`, `jns` to the upper clamp, `xor`, and `jmp` to the instruction after that
    path's `cmovg`.
  - It rejects the same mutant, built in memory (the image is untouched).
- **The contract.** §10 item 2 now states the piecewise rule, the positive-count precondition and the count-0 case,
  with the old wording struck. S requires that wording.

Run verified at e4a7aa2dd: `conv_check.py` X1-X4 and S, FAILS 0.

## The builder's provisional counts (OPUS, 2026-09-28)

Consumed from ASTRA's `nav-grid-initial-truncation` (`ASTRA-RETURN-OPUS-NAV-GRID-INITIAL-TRUNCATION`). Its check was
re-run: PASS_ORIGINAL_PREFIX.
- **X5** binds the bytes. `003924B0`'s counts are truncating conversions of `extent / c0`, where
  `c0 = sqrtf(w*h/275)`. Each extent is then divided by its count, with no test or branch before `floorf`.
- **Consequence.** Positive extents do not ensure nonzero counts. A 1 x 400 rectangle gives `nx` = 0 and `+inf` at
  `floorf`.
- **The contract.** §10 gains item 9, which states the domain: each of `w / c0` and `h / c0` must be at least 1.
- **Boundaries.** The `sqrtf` result was a host prediction at ASTRA's supplied boundary. Native library behaviour, the
  rest of the constructor and authored-grid occurrence are not claimed.

Run verified at 6850d35f4: `conv_check.py` X1-X5 and S, FAILS 0.
