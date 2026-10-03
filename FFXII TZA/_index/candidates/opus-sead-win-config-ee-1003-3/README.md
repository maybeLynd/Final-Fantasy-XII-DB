# Interior citations, cloud-drafted: sead-win-config.md's entry-cited functions (OPUS, 2026-10-03)

The page named 1 F-frontier functions only at their entry. A local drafting agent (local-ee-drafter, no cloud credit) drafted one sentence and 1-5 interior anchors per function from OPUS's annotated disassembly pack (`cloud-input/f-interior/` in the private snapshot repo). OPUS checked every row mechanically with `interior_ingest.py` and re-read every sentence against the bytes before applying.

**Rows.** 1 applied with 5 anchors. Rejected by the mechanical check: 0. Skipped by the session: 0. Missing: 0.

**OPUS corrections on re-read.**

- `007DD9F0`: byte re-read by a non-drafting agent: Lock, both allocations (007AD460(8,0x50,1) / (8,0x48,1)), the field stores, the slot +8 / +0x20 calls with no null test, the o+8-or-0 store and the error path all check out. Defect: the terminator index is movsxd then 'cmp rcx, 0x100; jae 00809728' - an unsigned 64-bit compare, so a negative index (L <= -2 from 0019C5D0) also reaches 00809728; the row's 'index 0x100 or more' states only the upper bound. Wording fix only; length kept within 1200.

**Verification.** [`interior_applier.py`](interior_applier.py) reads [`rows.json`](rows.json) and re-decodes every function first. Every anchor is an instruction boundary inside its extent with the recorded mnemonic ([`.out`](interior_applier.out): FAILS 0; idempotent).

**Effect and gates.** All 1 rowed functions now measure A. On the page: `check_links` 0, `check_self_contradiction --db` 0, `check_consistency` 0 disagreements naming this page (tree total 3), `verify_doc_addresses --all` 0 REVIEW on this page (tree total 2).

**Limits.** Body statements, not meanings. A cloud draft is a pointer, not evidence: what stands here is OPUS's re-read. The session's agreement with OPUS is not independent review.

## Review (OPUS)

A non-author spot-check goes to SWE2-AUDIT-SPEC: at least 15 rows read against the bytes.
