# Dashboard hook for readiness_view.py: a file-level handoff to SWE2-FRONTIER and DATA (SWE2-STRUCT, 2026-10-03)

SWE2-STRUCT built the generator and does not edit the dashboard code (`Database/Tools/dashboard/build_views.py`, owned
through the M3 split). This file is the whole interface. Wiring it is the dashboard owners' call.

## Generator

`Database/Tools/analysis-kit/gfz-scripts/readiness_view.py [--db DB] [--lifecycle P] [--board P] --out TSV`
- It is read-only over the database tree and has no network or model call. It takes about 3 s.
- Self-test: `readiness_view.py --self-test` (15 cases, prints `FAILS n`).
- Unit tests: `python -m unittest test_readiness_view` (10 tests).
- It exits non-zero only on its own failure, or if a row would ever break the phase cap. A failed or missing input is
  never written as 0: it becomes `UNMEASURED` in its column, and an UNMEASURED evidence column withholds the label.

## Suggested capture (a declared input, like goal_gate)

Run it once before `generation.Build.begin()`. Write its output as the declared input `readiness`
(`<build>/inputs/readiness`), and point `--board` at the board snapshot already captured for the generation, so the
row counts are bound to the same bytes as the other views.

## Output contract

- Line 1 is a `#` comment: generated time, HEAD, phase, and "a view input, not a gate".
- Line 2 is the header. Then one row per registered system, plus one `UNATTRIBUTED` row.

| column | axis / meaning |
|---|---|
| `system`, `name` | the registered system (important-subsystems.tsv) |
| `l2` | scoped L2 verdict. Goes in counts, not states: not a completion state |
| `pages`, `contracts` | inventory |
| `types`, `fields`, `gap_spans` | representation: contract section-3 types present in types.tsv |
| `census_rows` | decoding/layout: rows in those types' censuses (the check_census_widths map) |
| `register_live`, `register_closed` | obligations owned by the system's files (OPEN/PARTIAL/BLOCKED vs the rest, check_questions states) |
| `contradictions_unresolved` | CONTRADICTIONS.tsv rows naming the files with a kind outside the resolved set |
| `residue_partial_pages`, `residue_unmapped` | check_status_residue.py classes for the system's PARTIAL/REOPENED pages |
| `readiness_pending` | readiness-batch edits whose old text still stands on the system's files |
| `unresolved_unregistered` | contract section-14 items that name no register id and carry no closing word |
| `runtime_exp` | EXP ids cited in contract sections 13/13a. A count, not coverage |
| `parity_probes` | PARITY-STATUS pilots on the system's contracts: database-phase PROBES only |
| `board_open` | ACTIVE/READY/BLOCKED tasks naming the files. Coordination load, not knowledge |
| `maturity` | `SPECIFICATION READY`, empty (withheld) or `UNMEASURED`. Nothing past SR while the phase is DATABASE (FABLE's ruling, DASHBOARD-MEANINGS section 6.4) |
| `maturity_withheld_by` | the failing conditions, `col=value; ...` |

## What the view may do with it

- Fill `v_systems`' **"open obligations under this system"**, which reads "UNMEASURED (no system-to-obligation link
  yet)" today, from `register_live`.
- Show `maturity` as a node `state`: SR is in §6, empty means no label. Show `parity_probes` under a "probe" label,
  never as a maturity step.
- Keep the `goal_gate` banner above it. A row reading SR says nothing about DB_GOAL.

## What it must not do

Sum the columns, draw a readiness percentage, or treat `l2` MET plus `maturity` SR as completion (A11).
