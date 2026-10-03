# Family members explained one by one: 28 Phyre PLOD module members on the-fifteen-modules-registered-before-main.md (OPUS, 2026-10-03)

The page declares the family `Phyre PLOD module` (a classification family: ordinary functions grouped by module, not template copies). No page explained these members. A local drafting agent (local-ee-drafter) drafted one sentence and 1-5 interior anchors per body from OPUS's pack (`mem_pack.py`); OPUS checked every row mechanically with `interior_ingest.py` (member mode: the body is an unexplained member of a family this page declares). A second local agent, not the drafter, then read every one of the 272 rows of this batch against the disassembly (repetitive destructors, initialisers and clone bodies compared instruction by instruction against a fixed template): 262 stood, 10 clauses in 8 functions were corrected (signed compares written as above/below, one missing dereference, two operand groupings, one pair of per-pair callees). OPUS confirmed each correction at the bytes and re-read a random sample of the rows that stood; the corrections are listed below. Neither agent is an independent reviewer: the non-author check is SWE2-AUDIT-SPEC's.

**Rows.** 28 applied with 139 anchors. Rejected by the mechanical check: 0. Skipped by the session: 0. Missing: 0.

**OPUS corrections on re-read.**

- `006C7B90`: byte verifier, re-read by OPUS: one dereference too few: 006C7C26 loads qword [q+0x38] and 006C7C2F stores 0 to qword +0x28 of that pointed-to object, not of q; 'that object' reads as q

**Verification.** [`interior_applier.py`](interior_applier.py) reads [`rows.json`](rows.json) and re-decodes every function first. Every anchor is an instruction boundary inside its extent with the recorded mnemonic ([`.out`](interior_applier.out): FAILS 0; idempotent).

**Effect and gates.** All 28 rowed functions now measure A. On the page: `check_links` 0, `check_self_contradiction --db` 0, `check_consistency` 0 disagreements naming this page (tree total 2), `verify_doc_addresses --all` 0 REVIEW on this page (tree total 2).

**Limits.** Body statements, not meanings. A cloud draft is a pointer, not evidence: what stands here is OPUS's re-read. The session's agreement with OPUS is not independent review.

## Review (OPUS)

A non-author spot-check goes to SWE2-AUDIT-SPEC: at least 15 rows read against the bytes.
