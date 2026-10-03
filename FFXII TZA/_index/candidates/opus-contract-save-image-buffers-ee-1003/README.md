# Interior citations, cloud-drafted: CONTRACT-save-image-buffers.md's entry-cited functions (OPUS, 2026-10-03)

The page named 3 F-frontier functions only at their entry. A local drafting agent (local-ee-drafter, no cloud credit) drafted one sentence and 1-5 interior anchors per function from OPUS's annotated disassembly pack (`cloud-input/f-interior/` in the private snapshot repo). OPUS checked every row mechanically with `interior_ingest.py` and re-read every sentence against the bytes before applying.

**Rows.** 3 applied with 15 anchors. Rejected by the mechanical check: 0. Skipped by the session: 0. Missing: 0.

**OPUS corrections on re-read.**

- `005FCF20`: byte re-read by a non-drafting agent: the guard test is signed (`cmp [02CC0400], eax` then `jle` skips at 005FCF50); 'above' is the unsigned term and should be 'greater than (signed)'
- `007A05D0`: byte re-read by a non-drafting agent: 'it rescales `[t+0x24]`, `[t+0x2C]` ... and `[t+0x28]`, `[t+0x30]`' reads as stores into `t`; the products are only computed in registers and passed to `007A10A0`, nothing is written back to `t`; with a masked count of 0 the loop is skipped (`test`/`jbe` at 007A06CB) and it goes straight to `001825A0()` and returns 0; 'after the last item' should cover that path

**Verification.** [`interior_applier.py`](interior_applier.py) reads [`rows.json`](rows.json) and re-decodes every function first. Every anchor is an instruction boundary inside its extent with the recorded mnemonic ([`.out`](interior_applier.out): FAILS 0; idempotent).

**Effect and gates.** All 3 rowed functions now measure A. On the page: `check_links` 0, `check_self_contradiction --db` 0, `check_consistency` 0 disagreements naming this page (tree total 3), `verify_doc_addresses --all` 0 REVIEW on this page (tree total 2).

**Limits.** Body statements, not meanings. A cloud draft is a pointer, not evidence: what stands here is OPUS's re-read. The session's agreement with OPUS is not independent review.

## Review (OPUS)

A non-author spot-check goes to SWE2-AUDIT-SPEC: at least 15 rows read against the bytes.
