# Interior citations, cloud-drafted: CONTRACT-save-container-transform.md's entry-cited functions (OPUS, 2026-10-03)

The page named 5 F-frontier functions only at their entry. A local drafting agent (local-ee-drafter, no cloud credit) drafted one sentence and 1-5 interior anchors per function from OPUS's annotated disassembly pack (`cloud-input/f-interior/` in the private snapshot repo). OPUS checked every row mechanically with `interior_ingest.py` and re-read every sentence against the bytes before applying.

**Rows.** 4 applied with 20 anchors. Rejected by the mechanical check: 0. Skipped by the session: 1. Missing: 0.

**OPUS corrections on re-read.**

- `0087C760`: byte re-read by a non-drafting agent: the level check at 0087C840 is `cmp ebp, 9; ja` (unsigned), so any negative `l` other than the -1 already turned into 6 also gives -2; '`l` <= 9' with the '(unsigned)' attached only to argument 6 reads as a signed bound that would accept negatives

**Verification.** [`interior_applier.py`](interior_applier.py) reads [`rows.json`](rows.json) and re-decodes every function first. Every anchor is an instruction boundary inside its extent with the recorded mnemonic ([`.out`](interior_applier.out): FAILS 0; idempotent).

**Effect and gates.** All 4 rowed functions now measure A. On the page: `check_links` 0, `check_self_contradiction --db` 0, `check_consistency` 0 disagreements naming this page (tree total 3), `verify_doc_addresses --all` 0 REVIEW on this page (tree total 2).

**Limits.** Body statements, not meanings. A cloud draft is a pointer, not evidence: what stands here is OPUS's re-read. The session's agreement with OPUS is not independent review.

## Review (OPUS)

A non-author spot-check goes to SWE2-AUDIT-SPEC: at least 15 rows read against the bytes.
