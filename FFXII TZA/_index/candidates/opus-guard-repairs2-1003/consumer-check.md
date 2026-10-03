# Consumer check: recurrence holes in the checkpoint and publication guards closed (OPUS, 2026-10-03)

**What is corrected:** see [README](README.md). It covers five things:
- `--rev` could omit C5;
- C5 passed when goal_gate's count did not parse;
- C9 could be switched off by deleting its marker;
- exact-commit checks borrowed the live `Tools/work` through junctions;
- return packages could not reproduce their own L2 headline.

It also moves the published-row invariant to the shared publication boundary.

**Consumers searched:**
- Every checkpoint receipt: they now carry `required` and `checks_equal_required`, and a full label only for a complete run.
- Every return package: `verify` recounts L2 from the included `L2-VERDICTS.md`.
- Every lane's publish: `publish_paths.sh` runs the row-presence check on the private index.
- 392 committed records across lanes: HEAD and worktree show 0 missing.

Regression: `Database/Tools/analysis-kit/gfz-scripts/checkpoint_consistency.py --self-test`, verified 0 failures. It covers completeness, 12 C5 mutations (each fails closed, with a correct control), C9 lineage (marker removed on a descendant -> FAIL), and copy-not-link isolation.
Regression: `Database/Tools/analysis-kit/gfz-scripts/check_record_rows_present.py --selftest`, verified 0 failures (6 cases plus 6 publication-boundary scenarios through a real private index).
Regression: `Database/Tools/analysis-kit/gfz-scripts/return_package.py --self-test`, verified 0 failures (25 cases, 10 new L2 reproducibility cases).
