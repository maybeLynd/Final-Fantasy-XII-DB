---
experiment: EXP-022
title: Current question status and advisory text boundaries
status: VALIDATED — instrument controls; semantic follow-ups routed
contract: none - answered-advisory boundary inspection in the ledger; a Method A tooling record that executes no shipping game code. Checked BOTH directions 2026-09-13: it names no contract and no contract names it
date_designed: 2026-09-10
method: A - offline instrument preparation
live_game: false
---

# EXP-022 — distinguish checker mistakes from stale semantic prose

The final FABLE-REQ-ASTRA-TOOLING item named three pre-existing answered/unknown
reports. The current instrument reports nine physical lines. Each was inspected
against its local context and current ledger entry before changing the instrument.
No original-game semantic claim is promoted by the checker repair.

The old parser searched for an ANSWERED-like word anywhere in a row, including its
historical account. It therefore classified the reopened DG-1 row and the currently
non-answered ER-1/AY-10 rows as closed. The revision obtains statuses from the existing
check_questions.read_table parser. It does not introduce another status vocabulary.
The canonical parser labels DG-1 UNKNOWN, ER-1 OPEN and AY-10 BLOCKED in this snapshot;
those classifications do not prove the underlying mixed prose is consistent.

The old scanner used a physical-line neighborhood to associate a negative phrase
with an ID. This borrowed EN-1 from an adjacent completed bullet and DD-1 from the
next heading. The revision associates text within a paragraph, list item or table
row, preserves hard wraps, and removes balanced struck-through historical spans
while retaining physical line numbers. It still requires exactly one candidate ID,
including any open IDs in the same block. This is a bounded advisory heuristic,
not a semantic parser: unrelated propositions can share one paragraph.

Eight controls pass, including true negatives, adjacent-bullet/heading boundaries,
multiline strike history, retained live negatives, ambiguous IDs, current versus
historical statuses, and duplicate/empty ledger rejection. The original positive
self-test also passes. The canonical parser emits a pre-existing ResourceWarning
from its unclosed-file expression during unit tests; it is retained in test output
and was not silently represented as a new clean-file-handle control.

## Candidate-by-candidate disposition

The [same-input comparison](evidence/EXP-022-advisories/comparison.json) retains full
source snapshots, local context, question rows and instrument hashes. The old set
has nine lines, the revised set four. Neither set is a defect count.

| ID / source | Disposition |
|---|---|
| EN-1, workbench page line 262 | False association: the unknown purpose is a separate unchecked bullet; EN-1 answers the numeric combination in a preceding bullet. Removed by block boundaries. |
| I-6, verb-population page line 144 | Stale discontinuity claim, inconsistent with the closed mapping result and dispatch page sections 15–16. Remains reported; semantic propagation assigned to FABLE. |
| I-6, dispatch-table page line 162 | Same stale discontinuity reading, also present in earlier summary/formula prose. Remains reported; FABLE must propagate the established correction, not merely silence this line. |
| AY-10, VBF/table page line 557 | Stale authoring-key lead immediately follows a runtime correction disproving it. Its ledger also mixes answered text with a final STILL OPEN cell. Canonical status removes it from this answered-only scan; FABLE receives the unresolved document/status inconsistency separately. |
| EE-3, group contract line 298 | Negative is struck-through history followed by its correction. Removed by strike handling; deferred-arm reachability remains a distinct open question. |
| DD-1, input page line 869 | Stale converter-unknown text contradicts the same page's later writer correction and binding contract sections 7a/14a. Remains reported; OPUS receives this and the stale conclusion around line 934. |
| DD-1, input page line 915 | Unknown axis usage is a separate paragraph; the next heading supplied DD-1 to the old scanner. Removed by block boundaries. |
| ER-1, EXP-007 line 144 | Free-list direction/allocator endpoint is an explicitly separate residual, EW-3. This does not contradict the established table-population observation. Current canonical status is also OPEN. |
| DG-1, EXP-009 line 104 | Producer/progress semantics remain open after the oracle-scope correction. Historical ANSWERED text must not close the reopened row. |
| Z-11, boot page line 208 (new candidate) | Same paragraph mentions known time-base mode at 01DFE0B4 and an unknown consumer of a different global, 02064ACC. This is a residual, not a contradiction. Retain it as a manually reviewed advisory instead of adding a question-specific suppression. |

The revised CLI therefore still returns its advisory exit code 1 on the corpus.
That is an expected retained candidate set, not a failed preservation test and not
a clean semantic validation. The I-6/DD-1 prose and AY-10 mixed record require owner
correction; this package does not edit their meaning or close their follow-ups.
Negative phrases split across physical lines, unmarked historical prose, complex
Markdown nesting and multiple propositions in one block remain limitations.

## Publication control

The first validation invocation incorrectly proceeded after its publication claim
failed during a competing publication. It changed only ASTRA's claimed RULES output;
no staging occurred. Its receipt is retained as initial-unreserved-validation.json.
ASTRA then acquired publication at board revision 453 and repeated the controls,
generation, idempotence and input-stability checks before staging. The sealing script
now requires that active reservation. Source snapshots and the initial comparison
remain unchanged; the final checker replays their four candidates exactly after an
explanatory docstring edit.
