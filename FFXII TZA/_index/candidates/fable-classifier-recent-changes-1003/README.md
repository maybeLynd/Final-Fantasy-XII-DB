# Recent Meaningful Changes: knowledge progress versus workflow activity (FABLE, 2026-10-03)

*`FABLE-CLASSIFIER-RECENT-CHANGES-1003`. This is the user's improvement addendum, sections 2 and 10. FABLE built it on
the user's instruction while SWE2-DATA was occupied. The design is SWE2-DATA's plan,
[`swe2data-program-state-present-tense-1003`](../swe2data-program-state-present-tense-1003/README.md) part (3).
SWE2-DATA reviews it. The output contract (JSON v1) was agreed with SWE2-FRONTIER, whose dashboard adapter reads it.*

## The tool

`Database/Tools/analysis-kit/gfz-scripts/recent_changes.py` takes every commit in a 7-day window, with a 24-hour
subset. It derives **canonical events** from what changed:
- a register row's state;
- a correction record that strikes a claim;
- an accepted review of an evidence record;
- a package or type promotion;
- a newly satisfied L2 cell;
- a parity row;
- otherwise, the commit's path class.

Each event maps to one class through one table, `EVENT_CLASS`. Commit size and line counts are never read. Anything no
rule decides is printed UNCLASSIFIED, never guessed. Knowledge and activity are separate axes, and activity is labelled
"throughput only; never a knowledge or completion measure".

How to run it:
- `--json OUT` writes FRONTIER's contract. The write is atomic, so a failed run leaves no file.
- `--self-test` runs 33 fixtures, the shape check, and a sensitivity sweep.

The rules and FABLE's departures from DATA's table are listed at the top of the tool. These departures are for DATA to
rule on:
- a correction counts only when the commit also strikes text on a page;
- rule (f), a page section published with a new candidate record, counts as knowledge;
- `_index/workflow/` documents count as workflow.

## Checks

- **Self-test: FAILS 0** ([`recent_changes.selftest.out`](recent_changes.selftest.out)). All 33 fixtures pass, and so
  does the shape check. The sensitivity sweep catches all 204 swaps of two differently-classed `EVENT_CLASS` entries.
- **Real run at `050fd9350`** ([`real_run_summary.txt`](real_run_summary.txt); the full output is not committed,
  because it is about 3.9 MB):

  | window | commits | knowledge events | activity events | UNCLASSIFIED |
  |---|--:|--:|--:|--:|
  | 24 h | 325 | 330 | 370 | 72 |
  | 7 d | 2,832 | 1,408 | 1,915 | 2,354 |

- **Cross-check.** The per-commit register moves sum to a net +357 ANSWERED. That equals the register's own change
  across the window.
- **Hand-checked commits, all correct:**
  - `67f9e40e1`: register row moved to answered;
  - `ac1406035`: correction;
  - `96820750d`: evidence accepted;
  - `9b346c923`: rule (f);
  - `12e20b066`: package accepted;
  - `3c8bcc7af`: L2 newly MET;
  - `2069927c2`: workflow;
  - `11ff52fc5`: UNCLASSIFIED.

## Known limits

- Reviews kept only on the board are invisible, because TEAM.json is not committed. That leaves 166 evidence records
  in the 7-day window UNCLASSIFIED.
- The register diff runs per commit from git, because `history.jsonl` holds counters only.
- `_types` headers are read at HEAD unless the commit changes line 1.
- CONTRADICTIONS.tsv rows have no rule yet. DATA decides.
- A full run takes about 2.5 minutes.
- The large UNCLASSIFIED share is the honest output. A page-only edit with no canonical event is not counted as
  knowledge.

## Narrowing applied (FABLE, 2026-10-03, on SWE2-DATA's ACCEPT-WITH-NARROWING, 33b51c821)

- **N1.** Rule (f) counts as knowledge only when the record cites an independently accepted result: a review record
  whose verdict is ACCEPT (it may be relative-linked as `../<review>/REVIEW.md`), or an evidence record with an
  accepting review at or before the commit. Otherwise the event is `page-section-unreviewed` and reads UNCLASSIFIED.
  A review that first ACCEPTs a candidate package emits `section-accepted` (knowledge) at that review, the way
  `evidence-accepted` already worked.
- **N2.** At most one rule-(f) event per commit. Self-test: three records and their sections in one commit give one
  event. Reviews still count one per accepting review, since each review is an independent acceptance of one package.
- **N3.** New fixtures kill M5 (rule (f) ignoring the commit's strikes) and M7 (rule (f) firing with no page section).
- **CONTRADICTIONS.tsv:** DATA's ruling (a newly resolved row is a correction) is noted. No rule is built for it yet,
  so those rows stay UNCLASSIFIED, which is the honest default.

**Checks.**
- The self-test gives FAILS 0: every fixture, the JSON contract, the N2 count, and 239 of 239 class swaps caught.
- DATA's `mutate_rules.py`: M0 passes, and M1 to M6 are caught. M7's text anchor moved with the edit; the same
  mutation, re-anchored, makes the self-test fail (3 FAILs).
- A real 24-hour run gives 250 knowledge events. 240 of them are independent AUDIT-SPEC acceptances of OPUS and FABLE
  packages, and 10 are publishes that cite an accepted result. Before the narrowing, 253 of 255 knowledge events were
  author publishes.
