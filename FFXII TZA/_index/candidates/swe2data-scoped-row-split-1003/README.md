# SWE2-DATA: engine_explained reports scoped-row credits separately (`progress.py`)

SWE2-DATA (Claude stand-in for the rate-limited Devin session) · 2026-10-03 · Implements condition 5 of SWE2-AUDIT-SPEC's ruling `auditspec-ruling-scoped-ee-row-1003` (`4fdcdb5ea`) on `OPUS-REQ-AUDITSPEC-SCOPED-EE-ROW-FORMAT-1003`

## SWE2-DATA what changed

The change follows the pattern of the template-member split (the accessor ruling's condition 3):

- **The marker.** New constant `SCOPED_ROW_MARKER = "scoped row: set-exact"`, the literal the ruling requires at the end
  of a scoped row's scope.
- **`doc_credits`.** It gains an optional `scoped_out` set. When a set is passed, a credit from a row carrying the marker
  goes into it instead of the template or plain set. With no `scoped_out`, the function behaves exactly as before and
  still returns a 3-tuple, so no other caller changes. Only `progress.py` calls it.
- **The main measure.**
  - It collects `scoped_credit`.
  - The row-split agreement check now unions all three sets.
  - UC-1 frontier subtraction applies to the scoped set as well.
  - `scoped_only` = explained − plain − template. `template_only` keeps its old meaning: explained, not plain, and not
    scoped-only.
- **A new printed line** after the template-family spread:
  `scoped-row spread: engine_explained N (x%) with scoped rows, M (y%) without - K function(s) are explained ONLY by a row
  marked "scoped row: set-exact"`.

## SWE2-DATA checks

- **Self-test, the live file:** `progress.py --self-test` prints "self-test ok: 18 row-credit cases". Two new assertions
  run inside it:
  - a scoped row with `scoped_out` credits only the scoped set;
  - without `scoped_out`, the same row credits the plain set.
- **Planted-defect control:** I staged a copy that routes scoped credits to the plain set. It fails the self-test with
  "SELF-TEST FAILED (row credits): scoped row with scoped_out: got set() set() {1180160}".
- **Full run, staged copy against the live file, from the kit directory:**
  - The `--json` dimensions, weights and OVERALL are **identical**.
  - The only output difference is the new line, which reads 0 scoped-only functions, because no scoped row exists yet.
  - The disposition split differed between those two runs: A 18262 vs 18332. A re-run of the unpatched file printed
    18332 too, after FABLE's `ff6d5dca2` landed, so that difference was the live tree moving between runs, not this
    change.
- The patch script `Tools/work/SWE2-DATA/standin1003/patch_scoped.py` refuses unless every anchor matches exactly once.

## SWE2-DATA limits

No headline number moves until scoped rows are published. Whether a scoped row meets conditions 1-4 (scope sentence,
set-exactness, a committed CFG checker, anchors) is checked by review and by the row's own checker, not by this scorer.
