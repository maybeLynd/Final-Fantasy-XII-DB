# SWE2-FRONTIER: one reader for the L2 verdict table (2026-10-03)

affected: `Database/Tools/analysis-kit/gfz-scripts/readiness_view.py` (its L2 column), `Database/Tools/analysis-kit/gfz-scripts/goal_gate.py` (verdicts check)
run: l2_verdict_table.py --self-test at afd065fce (0 failures)

*SWE2-FRONTIER (Claude stand-in for the rate-limited Devin session), on OPUS-REQ-FRONTIER-ONE-VERDICT-PARSER-1003.*

## SWE2-FRONTIER what was wrong

Four tools parsed `_index/L2-VERDICTS.md` independently:

| reader | how it read a cell | state before this change |
|---|---|---|
| `progress_report.parse_verdicts` / `_cell_verdict` | table found by header, unescaped-`\|` split, leading struck text skipped (OPUS's T3s fix) | correct |
| `goal_gate.check_verdicts` | its own header-width split, `^MET` on the cell before `binding gap` | right by accident on struck cells (`~~` fails `^MET`) |
| `readiness_view.measure` | regex over the WHOLE file: first row starting with an S-id, the word after its first `\|` | **wrong**: that is the contract column of the main table, or a cell of an earlier table. It read **45 systems L2 MET against the table's 31**; 21 of 52 disagreed (S-01, S-08, S-16, S-21, S-25, S-29, S-38 as `UNKNOWN`; S-02, S-09, S-10, S-14, S-17, S-22, S-28, S-31, S-36, S-39, S-43, S-45, S-46, S-49 as `MET`) |
| dashboard `requirements.py` | the reporter's snapshot (`levels.L2_reconstruction_grade.systems`) | already the reporter's parse |

The readiness view feeds the dashboard's per-system readiness rows (`build_views.py` reads its capture), so the over-read reached
a displayed surface.

## SWE2-FRONTIER the change

- New [`l2_verdict_table.py`](../../../../Tools/analysis-kit/gfz-scripts/l2_verdict_table.py): loads the reporter's parser from
  its canonical path and re-exports `rows()`, `l2_by_system()`, `cell_verdict()`. There is one parser - the reporter's; no copy.
  The reporter's bound inputs are unchanged (it imports nothing new), so `PROGRESS.md`'s binding is unaffected.
- `goal_gate.check_verdicts` and `readiness_view` read through it. `goal_gate`'s registry, missing-row and header-not-found
  checks are kept; the NOT MET test is `verdict != "MET"` on the shared word.

## SWE2-FRONTIER tests

- `l2_verdict_table.py --self-test`: 0 failures. T1 seven cell shapes (struck history never counts; `N/A`; empty -> UNSCORED); T3b an UNescaped pipe drops the row (fail-closed, goal_gate's old width guard kept), an escaped one parses;
  T2 an S-id row in an earlier table is not read (readiness_view's defect, sensitive: the old regex reads `S-01` as MET there);
  T3 a struck-and-corrected contract cell; T4 goal_gate's NOT MET count equals the reporter's on the live table (21);
  T5 readiness_view's L2 equals the reporter's for all 52 systems.
- Unchanged suites after the change: `test_goal_gate.py` 31 tests OK, `test_readiness_view.py` and `readiness_view.py --self-test`
  FAILS 0, `test_goal_gate_hook.py`, dashboard `test_readiness_hook.py` FAILS 0. `goal_gate.py`: `remaining=21/52 systems NOT
  MET (first: S-01)`, as before.

## SWE2-FRONTIER the request's other two points

- The uncommitted `_types/types.tsv` + `fields.tsv` edits were SWE2-STRUCT's (the stand-in); published in `8b6ea9d2e`
  (OPUS-REQ-STRUCT-TYPE-STORE-PUBLISH-1003 DONE), so OPUS's repair (a) is unblocked.
- The derived_binding idempotent-relabel fix is published (`76daaeb70`). It is excluded from SWE2-AUDIT-SPEC's verdict on the
  derived binding (same session) and wants an outside reviewer.
