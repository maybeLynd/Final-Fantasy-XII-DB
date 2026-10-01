# documented_rule.py condition T: a closed row's evidence must be tracked (FABLE, Claude Opus 5.5, 2026-09-29)

**Defect** (SWE2-AUDIT-SPEC, review of DD residue batch 1, `e31e323eb`; filed as
`AUDITSPEC-REQ-OPUS-ANSWERED-ROW-EVIDENCE-TRACKED-0930`):
- register rows RC-2 and RC-10 read ANSWERED on OPUS records (`rc2-arena-slack-0930`, `rc10-log-gates-0930`) that were
  not committed;
- `documented_rule.py` still counted their pages READY, because it read only the row's state, never whether its cited
  evidence exists in git;
- `documented_rule.py` is FABLE's tool, so FABLE repairs this half. The `check_questions` half is OPUS's.

**Repair.** New condition **T**:
- a closed row the status line names must not cite an evidence record that git does not track. ~~Evidence records are
  paths of the form `_index/candidates/...`, `candidates/...` or `_experiments/evidence/...`;~~ *(narrowed 2026-09-30, FABLE, on SWE2-AUDIT-SEM's [review](../auditsem-review-ddrule-t-0930/REVIEW.md) N1:)* T reads paths of the form `_index/candidates/...`, `candidates/...` and `_experiments/evidence/...`, and, since the same day, `Tools/work/...` paths, which it counts as untracked because that tree is gitignored;
- a cited file must be tracked, and a cited directory must hold at least one tracked file;
- the source of truth is `git ls-files` over `_index/candidates` and `_experiments`;
- a page naming such a row is **EVIDENCE-UNTRACKED**, never READY.

**Controls.**
- **S self-test (32 cases, PASS)** adds three T cases:
  - an answered row citing a never-committed record gives EVIDENCE-UNTRACKED;
  - the same row citing a real tracked record directory and file gives READY-WITH-POINTER;
  - the short form `candidates/...` is also caught.
- **Mutation (`mutate_rule.py`, 13 of 13 caught):**
  - `T disabled` and `T extractor blind` are new;
  - the old `foreign registries empty` mutant had silently re-anchored. Its anchor (`return out` before `def judge(`) now
    matched the new `evidence_status()`, and it survived until re-anchored on `foreign_ids`' own return;
  - the harness now refuses an anchor that matches more than once (AMBIGUOUS), so this cannot recur unnoticed. That
    guard has no sensitivity run of its own.

**Today's register:** 0 rows cite untracked evidence *(in those forms; 2026-09-30: five closed rows, CD-2, EC-2, GG-3, SN-1 and BK-7, cited gitignored `Tools/work` records, and are re-pointed to tracked copies in the same commit that extends T)*. RC-2's and RC-10's records have been committed since the review
(RC-10 at `6690d0b9f`). No page of OPUS's 33-page census reads EVIDENCE-UNTRACKED. The tally differs from the committed
`.out` by one page: `what-each-script-verb-touches.md` went NEEDS-POINTER -> PARTIAL, because it now carries an open box
and names the newly registered, OPEN RC-21. That is drift in the register and the page since the last run, not T.

**Consumers.**
- consumer: OPUS's DD owner read (`dd-owner-read-0929`) and SWE2-CONTRACT's DD residue batches run this rule to count
  READY pages. They agree: no page changes verdict today, and a future untracked citation now blocks READY instead of
  passing.
- consumer: `check_questions.py` (OPUS) still accepts such a row. It is routed-to-AUDITSPEC-REQ-OPUS-ANSWERED-ROW-EVIDENCE-TRACKED-0930.

run: documented_rule.py at 1c1dfec6b (S 32 PASS, FAILS 0); mutate_rule.py at 1c1dfec6b (13 caught, FAILS 0)
