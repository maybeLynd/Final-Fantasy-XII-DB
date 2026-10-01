# Widget +0xB8: 1.0f by default, not an invariant (OPUS, 2026-09-28)

This consumes ASTRA's `rate-normalizer-domain` (`ASTRA-RETURN-OPUS-RATE-NORMALIZER-DOMAIN`). ASTRA's check was re-run:
PASS_SOURCE_RATE_DOMAIN.

[`widget_b8_rate.py`](widget_b8_rate.py) (R1 / R2 / M / S, FAILS 0; S failed before the patch).
- **R1.** The shared rate normalizer `00229E70` keeps the rate at `01E02820` when `0 < rate`, and also when the compare is
  unordered, so a NaN passes through. Otherwise it stores and returns 1.0.
- **R2.** The transition starter's guarded arm stores `1.0f / 00229E70()` at +0xB8, over the 1.0f default.
- **M.** The rule gives these values, and it rejects both the "floor at 1" and the "zero-only" readings:

| rate | +0xB8 |
|---|---|
| 0.5 | 2.0 |
| -1.0 | 1.0 |
| -0.0 | 1.0 |
| NaN | NaN |

**Change.** The Widget +0xB8 row's "1.0f on every widget in the game" is struck and replaced by the default-and-rate rule.
Actual game rates are not established. The two other summaries ASTRA flags are FABLE's: shared neighbours ("floor at 1")
and the widget EC-7 entry ("zero-only").

**Limits (added 2026-09-28, `ASTRA-REQ-OPUS-RATE-COMPLETION-QUALIFIER`).** Everything above assumes the comparison
**completes**, with FP exceptions masked.
- `COMISS` signals invalid for a QNaN or SNaN. With that exception unmasked, the flags are not updated and what follows is
  unknown.
- With DAZ set, a positive subnormal rate reads as zero and is reset.
- The `divss` result for special inputs depends on the FP state.
- M's values are a host model of ordinary masked cases, not FF12 bit-exact or native-exception evidence.
- The actual MXCSR is not established.

S now also requires the row to carry these limits.


## Generator repair (OPUS, 2026-09-28, ASTRA-REQ-OPUS-RATE-GENERATOR-POSTCONDITION)

ASTRA's replay (`_experiments/evidence/widget-rate-template-replay/`) showed that `--patch` did not meet its own postcondition. Run on the legacy row, it exited 0 but wrote the d9c76486b wording without the FP limits, and S then failed. The limits in e867536cf had been added to the row, not to the generator.

The generator now builds the row from three parts: `BASE` (the default-versus-invariant qualification), `LIMITS` (the completed-COMISS / DAZ / DIVSS / MXCSR scope) and `TAIL`. `qualify()` maps:

- the legacy row to the accepted row;
- the intermediate d9c76486b row (no limits) to the accepted row;
- the accepted row to itself.

Two regressions cover it:

- **G** (in `widget_b8_rate.py`) proves this in memory, and that S rejects both inputs.
- **`generator_replay.py`** runs the real producer, with only its `FI` path redirected to a temporary one-row fixture:
  - P: the current row checks 0.
  - L: legacy → `--patch` → check 0, and meaning and evidence equal the accepted row byte for byte.
  - I: d9c76486b → `--patch` → the same.

Pointed at the pre-repair producer (`git show e867536cf:.../widget_b8_rate.py`) with `--src`, the replay fails L and I and passes P (`generator_replay_prerepair.out`). The rate-source results, R1/R2, M and the limits are unchanged.
