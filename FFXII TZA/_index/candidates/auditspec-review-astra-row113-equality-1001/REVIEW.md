# Audit-spec review: ASTRA row113 equality

Reviewer: SWE2-AUDIT-SPEC · 2026-10-02 · Task: `ASTRA-REQ-SPEC-ROW113-EQUALITY-1001` · Package: `_experiments/evidence/row113-equality/`

## Verdict: ACCEPT

## What was checked

- `prove.py` re-run fresh in a disposable copy → exit 0; result byte-identical to retained `result-01.json`
  (producer_complete, theorem "equal branch iff row275 under stated premises", row_product_max 4294836225,
  difference interval [-18022125, 4276814100], 39 pins, native_game_runs 0).
- `control.py` re-run → exit 0; all prerequisite cases refused with expected diagnostics
  (missing-parent-proof-status, bad-high-half → "original byte mismatch").
- The modular inequality is sound on its face: u16×u16 < 2^32, so mod-2^32 equality of `B + i*s` and
  `B + 275*s` forces `(i-275)*s ≡ 0` with |difference| < 2^32, hence i = 275 when s ≠ 0; B cancels.

## Notes

- Scope kept: this is a source/invariant proof over retained original bodies — no native or game
  execution, no natural type-admission claim (that stays with FABLE's OV42/OV21 question).

