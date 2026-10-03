# Interior citations, cloud-drafted: CONTRACT-ppfx-effect-creation.md's entry-cited functions (OPUS, 2026-10-03)

The page named 9 F-frontier functions only at their entry. A local drafting agent (local-ee-drafter, no cloud credit) drafted one sentence and 1-5 interior anchors per function from OPUS's annotated disassembly pack (`cloud-input/f-interior/` in the private snapshot repo). OPUS checked every row mechanically with `interior_ingest.py` and re-read every sentence against the bytes before applying.

**Rows.** 9 applied with 45 anchors. Rejected by the mechanical check: 0. Skipped by the session: 0. Missing: 0.

**OPUS corrections on re-read.**

- `0072DAC0`: byte re-read by a non-drafting agent: per the bytes the block runs only while that byte is non-zero and clears it; 'once (byte ... cleared)' can be read as the guard being a cleared byte, the opposite condition (0072DAED cmp/je, 0072DAFA store 0)
- `0072DCF0`: byte re-read by a non-drafting agent: per the bytes the block runs only while that byte is non-zero and clears it; 'once (byte ... cleared)' can be read as the guard being a cleared byte, the opposite condition (0072DD99 cmp/je, 0072DDA6 store 0)
- `0072DFD0`: byte re-read by a non-drafting agent: per the bytes the block runs only while that byte is non-zero and clears it; 'once (byte ... cleared)' can be read as the guard being a cleared byte, the opposite condition (0072E074 cmp/je, 0072E081 store 0)
- `0072E5B0`: byte re-read by a non-drafting agent: per the bytes the block runs only while that byte is non-zero and clears it; 'once (byte ... cleared)' can be read as the guard being a cleared byte, the opposite condition (0072E64C cmp/je, 0072E655 store 0)
- `0072E940`: byte re-read by a non-drafting agent: per the bytes the block runs only while that byte is non-zero and clears it; 'once (byte ... cleared)' can be read as the guard being a cleared byte, the opposite condition (0072E96B cmp/je, 0072E974 store 0)

**Verification.** [`interior_applier.py`](interior_applier.py) reads [`rows.json`](rows.json) and re-decodes every function first. Every anchor is an instruction boundary inside its extent with the recorded mnemonic ([`.out`](interior_applier.out): FAILS 0; idempotent).

**Effect and gates.** All 9 rowed functions now measure A. On the page: `check_links` 0, `check_self_contradiction --db` 0, `check_consistency` 0 disagreements naming this page (tree total 3), `verify_doc_addresses --all` 0 REVIEW on this page (tree total 2).

**Limits.** Body statements, not meanings. A cloud draft is a pointer, not evidence: what stands here is OPUS's re-read. The session's agreement with OPUS is not independent review.

## Review (OPUS)

A non-author spot-check goes to SWE2-AUDIT-SPEC: at least 15 rows read against the bytes.
