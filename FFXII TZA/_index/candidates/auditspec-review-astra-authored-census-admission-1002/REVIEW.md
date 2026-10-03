# SWE2-AUDIT-SPEC review: ASTRA authored-census admission control

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session) · 2026-10-03 ·
Task: `ASTRA-REQ-SPEC-AUTHORED-CENSUS-ADMISSION-1002` · Package: `_experiments/evidence/authored-census-admission/`
(publisher commit `55466577d`).

## SWE2-AUDIT-SPEC verdict: ACCEPT

The package's own finding stands: **REJECT standalone corpus-completeness / absence inference from a non-zero
global CALL count of the committed collector.** This is a research-tool control, not FF12 execution.

## SWE2-AUDIT-SPEC independent reproduction

- **Collector identity.** The retained `script_verb_census.py` hashes to `ad23888c…` and equals the blob at
  `4a818c6d3`. The swallow is at lines 34–37: `read_entry` inside `try / except Exception: continue`. The only
  guard is the global zero-CALL refusal at line 95.
- **Fresh fixture runs.** I ran the package's `fixture_entry.py` against fresh disposable copies, once with the
  committed collector and once with today's checkout:

  | case | committed collector (`ad23888c`) | current collector (`861ce826`, OPUS `f83823625`) |
  |---|---|---|
  | all readable | exit 0, rows 029A, 029B | exit 0, rows 029A, 029B |
  | second extraction raises | **exit 0, stderr empty, only 029A** | **exit 1, `REFUSE: INCOMPLETE - 1 relevant input(s) not read or parsed`** |
  | both raise | exit 1, zero-CALL refusal, no table | exit 1, zero-CALL refusal plus per-input accounting |

  So the defect reproduces exactly on the committed collector, and the repaired collector now refuses the
  partial case. That is the expected regression control for OPUS's repair.
- **Reducer.** `reduce.py` re-run gives an output **byte-identical** to `result-01.json`
  (`REJECT_STANDALONE_CORPUS_COMPLETENESS_INFERENCE`). It treats the all-failed case as an expected refusal, not
  a zero-case semantic PASS.

## SWE2-AUDIT-SPEC scope notes

- The archive, extractor, decoder and names are synthetic. Nothing here shows a historical real extraction
  failure, and earlier positive captures are not invalidated.
- Consumers of authored-flow absence claims made with the pre-`f83823625` collector need explicit
  attempted/read/decoded accounting.
