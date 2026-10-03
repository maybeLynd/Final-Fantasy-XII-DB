# Interior citations, cloud-drafted: the-message-window-layout-readers.md's entry-cited functions (OPUS, 2026-10-03)

The page named 1 F-frontier functions only at their entry. A local drafting agent (local-ee-drafter, no cloud credit) drafted one sentence and 1-5 interior anchors per function from OPUS's annotated disassembly pack (`cloud-input/f-interior/` in the private snapshot repo). OPUS checked every row mechanically with `interior_ingest.py` and re-read every sentence against the bytes before applying.

**Rows.** 1 applied with 5 anchors. Rejected by the mechanical check: 0. Skipped by the session: 0. Missing: 0.

**OPUS corrections on re-read.**

- `002A36A0`: byte re-read by a non-drafting agent: Gates, the rcx-advanced-from-its-post-call-value detail, 002A5BC0(w), AND 0xE3 and the unconditional OR 0x80 all check out. Defect: 'calls 002A7D30 n times' states a fixed count, but the loop bound is the word [w+0x3F0] re-read (movsx) after every call (002A36F5), so the call count follows the re-read value (first call always made, since n > 0 is tested first); rewritten to state the loop as coded.

**Verification.** [`interior_applier.py`](interior_applier.py) reads [`rows.json`](rows.json) and re-decodes every function first. Every anchor is an instruction boundary inside its extent with the recorded mnemonic ([`.out`](interior_applier.out): FAILS 0; idempotent).

**Effect and gates.** All 1 rowed functions now measure A. On the page: `check_links` 0, `check_self_contradiction --db` 0, `check_consistency` 0 disagreements naming this page (tree total 3), `verify_doc_addresses --all` 0 REVIEW on this page (tree total 2).

**Limits.** Body statements, not meanings. A cloud draft is a pointer, not evidence: what stands here is OPUS's re-read. The session's agreement with OPUS is not independent review.

## Review (OPUS)

A non-author spot-check goes to SWE2-AUDIT-SPEC: at least 15 rows read against the bytes.
