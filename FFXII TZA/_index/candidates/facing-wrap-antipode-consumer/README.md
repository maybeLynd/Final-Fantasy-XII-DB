# Consumer check: the facing re-wrap is a two-cycle at ±π (FABLE, Claude Opus 5.5, 2026-09-28)

affected: 06-Movement-And-Navigation/CONTRACT-facing-and-steering.md, ED-3 (register row)

Consumes ASTRA-RETURN-FABLE-FACING-WRAP-ANTIPODE (`_experiments/evidence/facing-wrap-antipode/`) and
OPUS-REQ-FABLE-FACING-WRAP-ANTIPODE. **Verdict: ACCEPT**, re-derived. [`wrap_check.py`](wrap_check.py)
([output](wrap_check.out)) binds `0026C090`'s sign branch, bias loads, divide / truncate / multiply / two subtractions and
the kind-3 store from the listing. It reads the three constants from the image and computes the sequence in binary32:
- **Result:** +π → −π → +π and −π → +π → −π. +0 is fixed.
- **Control:** with the negative bias replaced by +π, −π becomes a fixed point, so the check sees the bias choice.

So "idempotent, so harmless" is false at the exact antipodes. The number of wraps on each path decides the stored sign
there, although the geometric direction is the same. OPUS counts the paths in 3683ff941: kind 1 wraps three times, and
the kind-3 target wraps twice.

| consumer | action | agreement |
|---|---|---|
| CONTRACT-facing-and-steering.md §4 invariant | "idempotent, so harmless … safe to call directly" struck and corrected | revised-here |
| same page, the closing "Answered" line | the idempotence clause struck and replaced | revised-here |
| `_index/OPEN-QUESTIONS.md` ED-3 | "(idempotent, so the double wrap is harmless)" struck and qualified; verdict unchanged | revised-here |
| heading-speed-to-position-delta.md | none: already says the wrap is not idempotent | agrees |
| `_index/candidates/s18-opus-replay-facing-and-steering/` | none: OPUS qualified it in 3683ff941 | agrees |
| `_index/AUDIT-LOG.md` 22213 | none: a historical receipt, kept | history |

Regression: `wrap_check.py` (W1-W3, control C). Run verified at 0754df300: FAILS 0.
