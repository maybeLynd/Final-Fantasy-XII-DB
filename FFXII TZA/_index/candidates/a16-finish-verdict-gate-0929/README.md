# A16: a review finishes only with one structured verdict (OPUS, 2026-09-29)

**Request.** `ASTRA-REQ-OPUS-A16-REVIEW-VERDICT-ADMISSION`, with ASTRA's isolated reproduction `7068c250a`
(`_experiments/evidence/a16-review-finish-admission/`). A real non-author review finished DONE with a scoped ACCEPT in its
checkpoint prose but no `verdict:` result ref. `transitions.plan` reported VERDICT-MISSING, and nothing moved to
incorporation.

## The defect is systemic, not one row (OPUS, 2026-09-29)

At board revision 40467, **55 of the 72** DONE, non-retired tasks that carry a `reviews` field hold no single
whole-string policy verdict. The per-row list is [`legacy-verdictless-reviews.tsv`](legacy-verdictless-reviews.tsv).

| reviewer | rows |
|---|---|
| SWE2-AUDIT-SPEC | 35 |
| SWE2-AUDIT-SEM | 19 |
| ASTRA | 1 (`verdict:PARTIAL`, which is not a REVIEW-POLICY verdict) |

Almost all of them finish with a record path alone. A review whose verdict exists only in prose or in a record file can
never drive `transitions.py`, and a verdict is never read out of prose (the transitions convention).

## The repair: the supported finish path (OPUS, 2026-09-29)

- **`team.py`.**
  - `REVIEW_VERDICTS` holds the six REVIEW-POLICY verdicts: ACCEPT, ACCEPT-WITH-NARROWING, REJECT, ESCALATE-FABLE,
    ESCALATE-OPUS and ESCALATE-ASTRA.
  - `review_verdicts()` reads them from whole-string `verdict:<V>` refs, matched with fullmatch and never normalized.
  - A `finish` of a task carrying a `reviews` field is refused unless its result refs hold **exactly one** such verdict.
    The refusal text says how: an inconclusive review is checkpointed, blocked or released, not finished.
  - Tasks without `reviews` are unaffected.
  - The existing DONE history is not validated against the new rule and is not rewritten; `validate` passes on the live
    board.
- **`transitions.py`.**
  - It uses the same vocabulary. Only ACCEPT and REJECT drive a transition.
  - The other four are reported as **VERDICT-MANUAL** with the verdict named. Before this change,
    `verdict:ACCEPT-WITH-NARROWING` read as VERDICT-MISSING, which misstates a real verdict as absent.

## Controls (OPUS, 2026-09-29)

- `test_team.py` `test_k`, through the real `team.apply`.
  - **Refused:** no verdict; `verdict:ACCEPT` + LF; two different verdicts; `verdict:PARTIAL`; `verdict:accept`. Each
    refused review stays ACTIVE and can still be released.
  - **Admitted:** ACCEPT, ACCEPT-WITH-NARROWING, REJECT, ESCALATE-OPUS.
  - **Unaffected:** a plain research finish with no `reviews` field.
- **Mutants.**
  - Gate disabled: `test_k` fails.
  - `== 1` weakened to `>= 1`: `test_k` fails.
  - One mutant run first appeared to fail on the restored source. The cause was a stale `__pycache__` .pyc: the mutant
    has the same byte size and was written within the same second. The cache was cleared and the result re-run.
- **`test_transitions.py`.**
  - X6, X8 and X16 now build their verdict-less, conflicting and LF rows as **legacy DONE rows** directly on the
    disposable board. The writer now refuses them, but 55 such rows exist live.
  - X21: ACCEPT-WITH-NARROWING yields VERDICT-MANUAL and creates nothing.
- **Results.** `python -m unittest test_team`: OK. `test_transitions.py`: FAILS 0. `team.validate` on the live board:
  passes.

**Self-falsification.**
- A reviewer path that finishes reviews by some other writer would bypass the gate. Checked: `team.py apply` (CLI)
  and `transaction` both run `apply()`, and `transitions.py` writes only through the CLI.
- An AUTO-REPAIR / AUTO-INCORP child carrying `reviews` would be forced to carry a verdict it cannot have. Checked:
  `_op` gives children `transition_of`, not `reviews`.

## Limits and what stays open (OPUS, 2026-09-29)

- This repairs admission going forward. The 55 legacy rows stay as they are.
- Making them machine-readable needs an **additive ratification by each reviewing identity**: a new task carrying the
  same `reviews` field plus `"ratifies": <original id>`, finished with the verdict the reviewer's own record states.
  That is routed to SWE2-AUDIT-SPEC, SWE2-AUDIT-SEM and ASTRA. OPUS does not transcribe other reviewers' verdicts.
  - The SWE2-AUDIT-SEM rows were written by the Devin lane, and most of them review OPUS packages. They are left for a
    non-OPUS operator, because OPUS currently runs that identity through Claude subagents.
- A16 itself (one real package through review, repair or incorporation, and next task, with no relayed message) is
  **not** claimed here. It needs this gate independently reviewed first.
