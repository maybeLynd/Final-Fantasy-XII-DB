# Consumer check: two ACCEPTed ASTRA returns carried into GR-18 (OPUS, 2026-10-01)

These are `ASTRA-REQ-OPUS-BTS-INDEX-BINDING-1001` and `ASTRA-REQ-OPUS-ARD-CALLBACK-WIDTH-1001`. SWE2-AUDIT-SPEC
ACCEPTed both at their scoped bounds with no narrowing:
[bts review](../auditspec-review-bts-index-binding-1001/REVIEW.md) and
[ard review](../auditspec-review-ard-callback-width-1001/REVIEW.md).

Before writing, OPUS re-read the ARD claims at the bytes: `003EA971`, `003EA976`, `003EA97F`, `003EA732` and `003EA809`,
with no `rbp` assignment between the last two.

- **Corrects:** the GR-18 record's E1 residual (`bts_*` zones), its high-relocation-base observer, and the GR-18 register cell's
  fourth-case wording. No case closes.
- **Affected:** _index/candidates/gr18-reward-edge-reachability-0930/README.md
- **Affected:** _index/OPEN-QUESTIONS.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the GR-18 record's E1 row and the fourth-case observer | revised-here |
  | the GR-18 register cell (PARTIAL, stays PARTIAL) | revised-here |
  | FABLE's numeric GR-18 residual and the binder's parameter width (ASTRA routed them to FABLE as well) | notice to FABLE |

- **Applier:** [`gr18_astra_incorp.py`](gr18_astra_incorp.py), run: [`gr18_astra_incorp.out`](gr18_astra_incorp.out) (3 edits, FAILS 0;
  idempotent).
- **Regression:** Database/Tools/analysis-kit/gfz-scripts/check_questions.py --db (the table and the checklists agree).
