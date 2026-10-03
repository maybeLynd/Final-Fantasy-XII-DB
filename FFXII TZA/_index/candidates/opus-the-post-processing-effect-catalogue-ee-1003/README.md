# Interior citations, cloud-drafted: the-post-processing-effect-catalogue.md's entry-cited functions (OPUS, 2026-10-03)

The page named 3 F-frontier functions only at their entry. A local drafting agent (local-ee-drafter, no cloud credit) drafted one sentence and 1-5 interior anchors per function from OPUS's annotated disassembly pack (`cloud-input/f-interior/` in the private snapshot repo). OPUS checked every row mechanically with `interior_ingest.py` and re-read every sentence against the bytes before applying.

**Rows.** 3 applied with 15 anchors. Rejected by the mechanical check: 0. Skipped by the session: 0. Missing: 0.

**OPUS corrections on re-read.**

- `0070BA00`: byte re-read by a non-drafting agent: Argument position: the float 00902EF8 is loaded into xmm3, the 4th argument slot, and the stack holds dword 0 at [rsp+0x20] (5th) and -1 at [rsp+0x28] (6th); r9 is not set up. The draft's list (rcx, 0, 0, r9, float, 0, -1) has seven entries and makes the float the 5th argument, which contradicts the 0070B780 row (5th dword to +0x5A0, 6th = n, so -1 skips the 00722900 path). Rest verified: byte [rcx] and byte +0x147 / qword +0x60 gates, jb 1 log gates, 0070B990(rcx, edx, 0) with cmovs returning it only when negative.

**Verification.** [`interior_applier.py`](interior_applier.py) reads [`rows.json`](rows.json) and re-decodes every function first. Every anchor is an instruction boundary inside its extent with the recorded mnemonic ([`.out`](interior_applier.out): FAILS 0; idempotent).

**Effect and gates.** All 3 rowed functions now measure A. On the page: `check_links` 0, `check_self_contradiction --db` 0, `check_consistency` 0 disagreements naming this page (tree total 3), `verify_doc_addresses --all` 0 REVIEW on this page (tree total 2).

**Limits.** Body statements, not meanings. A cloud draft is a pointer, not evidence: what stands here is OPUS's re-read. The session's agreement with OPUS is not independent review.

## Review (OPUS)

A non-author spot-check goes to SWE2-AUDIT-SPEC: at least 15 rows read against the bytes.
