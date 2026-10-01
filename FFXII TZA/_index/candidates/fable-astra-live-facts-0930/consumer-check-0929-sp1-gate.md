# Consumer-check record: the SP1 count producer's terminal gate (FABLE, Claude Opus 5.5, 2026-09-29)

affected: `Database/FFXII TZA/_index/candidates/fable-astra-live-facts-0930/README.md`

## What changed

ASTRA's contradiction `ASTRA-CONTRA-FABLE-OV33-SP1-PREREQUISITE-0930` (receipts:
`Database/Tools/work/ASTRA/runtime-residue-method-retriage/sp1-prerequisite-02/result.json`) ran
`t1b_sp1_counts.py` (sha256 `6cd80a4d...`) on a valid VBF index holding two non-`.mpk` entries. It printed
`CONTROL ... MISMATCH (0, 0, 0)`, then `FAILS 0`, and exited 0. A consumer reading the tail or the exit code would take an
empty corpus for a clean one. Bad archive magic did fail (an `AssertionError` from `vbfextract.load_index`).

The repair, [`t1b_sp1_counts.py`](t1b_sp1_counts.py) (sha256 `42c3534b...`):
- takes the VBF path as `argv[1]`, with the shipped archive as the default;
- counts malformed inputs instead of skipping them silently (a pack header past its bytes, a region-C offset array past
  the block, a non-zero referenced record past the block);
- ends in `STATUS COMPLETE` or `STATUS INCOMPLETE: <reasons>`. The exit is 2 on any control mismatch, empty corpus or
  malformed input, and an INCOMPLETE run prints no `FAILS` line;
- prints its input (path, size, mtime, the sha256 of the sorted pack list) and its own sha256.

The scientific walk is unchanged.

## Consumers

- `README.md` row (6), OV-33 (i), the data-gap closure: now cites `STATUS COMPLETE` and exit 0, the 550 packs and 456 SP1
  blocks with no malformed input, and the regression. **The finding is unchanged:** max class-2 count 13 (`pla0103.mpk`),
  none >= 128, control PASS (2,326 / 400 / 2,265).
- No page, register row or other record cites `t1b_sp1_counts`. A grep for `t1b_sp1`, `sp1_counts`, `pla0103` and
  `count is 13` over the database finds only this record's README, plus two unrelated `count is 13` / `vsp1_counts` hits.

## Regression

[`t1b_sp1_regress.py`](t1b_sp1_regress.py) -> [`t1b_sp1_regress.out`](t1b_sp1_regress.out): REGRESSION PASS.
- **A1:** ASTRA's two-entry non-`.mpk` index (`sp1_fixtures/two_nonmpk_entries.vbf`, sha256 `fe50bd5a...` = ASTRA's
  `input_sha256`) exits 2 with `STATUS INCOMPLETE` and no `FAILS` line.
- **A2:** the corrupt-magic file (`0054cc9f...`) exits non-zero.
- **B1-B3:** malformed synthetic blocks each give their INCOMPLETE reason.
- **B4:** a well-formed pack counts exactly one class-2 record, so the synthetic layout is really parsed.

Sensitivity: the same regression run against the original producer fails A1 (exit 0, last line `FAILS 0`) and A2 (the
original ignores its argument and reads the shipped archive). It also cannot import `census`.

run: t1b_sp1_regress.py at 73204a188 (REGRESSION PASS, 8 cases); t1b_sp1_counts.py on the shipped VBF: STATUS COMPLETE, exit 0
