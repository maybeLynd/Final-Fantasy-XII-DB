# Consumer check: interior rows deleted by a later record, restored (OPUS, 2026-10-03)

**What is corrected:**
- 55 rows of three published OPUS interior records had been deleted from their pages by later OPUS records:
  - 44 on `the-lua-loader-and-what-it-accepts.md`, by 890844135;
  - 8 on `sqex-sd-sound-driver-architecture.md`, by 33eb7192f;
  - 3 on `the-music-control-file-and-the-bgm-stream.md`, by e63502b10.
- The rows are restored unchanged.
- The applier that deleted them now refuses to: it re-renders only a section it owns and never drops a row that is
  not its own. See [README](README.md).

**Consumers searched:**
- engine_explained (`progress.py`) reads the pages; the restored rows count again after the commit.
- `check_record_rows_present.py` now checks every committed record's rows on its page; at HEAD before the fix it
  reported exactly these 55 rows, and nothing else.
- The `*-cloudint-1003` sections on the same pages are unchanged; their appliers print ALREADY with the fixed copy.

Regression: `Database/Tools/analysis-kit/gfz-scripts/test_interior_applier.py`, verified FAILS 0 (T1-T4 pass; control C1:
the pre-fix applier loses the first record's rows).
Regression: `Database/Tools/analysis-kit/gfz-scripts/check_record_rows_present.py`, verified FAILS 0 on the restored
worktree and FAILS 55 at the pre-fix HEAD.
