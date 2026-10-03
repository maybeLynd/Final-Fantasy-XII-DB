# Consumer check: the recurrence-prevention guards repaired (OPUS, 2026-10-03)

**What is corrected:**
- `run_correction_regressions.py` counted an exit-0 run as PASS even when its own summary reported failures.
- `checkpoint_consistency.py --rev` stopped before C5-C8.
- C9 ordered the exclusion policy by calendar date.
- `derived_binding.relabel()` kept a stale reason.

See [README](README.md).

**Consumers searched:**
- The correction-regression census, re-run in full with the fixed runner ([`correction_regressions.out`](correction_regressions.out)).
- Every checkpoint receipt.
- The publish gate's relabel path (`publish_paths.sh` imports `derived_binding.gate`).
- The two legacy scripts that relied on printed text (`b20_checks.py`, `awn_b_checks.py`), which now exit 1 on their own fail count.

Regression: `Database/Tools/analysis-kit/gfz-scripts/run_correction_regressions.py --self-test`, verified 0 failures (16 cases, including exit 0 with FAILS 1).
Regression: `Database/Tools/analysis-kit/gfz-scripts/checkpoint_consistency.py --self-test`, verified 0 failures (including the same-day C9 re-score).
Regression: `Database/Tools/analysis-kit/gfz-scripts/derived_binding.py --self-test`, verified 0 failures (22 checks, including reason A plus moved set B giving displayed reason B).
