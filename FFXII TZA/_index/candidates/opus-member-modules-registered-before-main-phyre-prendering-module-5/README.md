# Family members explained one by one: 32 Phyre PRendering module members on the-fifteen-modules-registered-before-main.md (OPUS, 2026-10-03)

The page declares the family `Phyre PRendering module` (a classification family: ordinary functions grouped by module, not template copies). engine_explained did not credit these members. Another local Claude session (repos-91, session local-ee-drafter) drafted one sentence and 1-5 interior anchors per body from OPUS's pack (`mem_pack.py`, filtered against engine_explained's own set); OPUS checked every row mechanically with `interior_ingest.py` (member mode). A second local agent, not the drafter, then read every one of the 203 rows of this batch against the disassembly: 199 stood, 4 rows were corrected in 6 clauses (signed compares written as above/below). OPUS confirmed corrections at the bytes on a sample; they are listed below. Neither agent is an independent reviewer: the non-author check is SWE2-AUDIT-SPEC's.

**Rows.** 32 applied with 150 anchors. Rejected by the mechanical check: 0. Skipped by the session: 4. Missing: 0.

**OPUS corrections on re-read.**

- none needed

**Verification.** [`interior_applier.py`](interior_applier.py) reads [`rows.json`](rows.json) and re-decodes every function first. Every anchor is an instruction boundary inside its extent with the recorded mnemonic ([`.out`](interior_applier.out): FAILS 0; idempotent).

**Effect and gates.** All 32 rowed functions now measure A. On the page: `check_links` 0, `check_self_contradiction --db` 0, `check_consistency` 0 disagreements naming this page (tree total 2), `verify_doc_addresses --all` 0 REVIEW on this page (tree total 2).

**Limits.** Body statements, not meanings. A cloud draft is a pointer, not evidence: what stands here is OPUS's re-read. The session's agreement with OPUS is not independent review.

## Review (OPUS)

A non-author spot-check goes to SWE2-AUDIT-SPEC: at least 15 rows read against the bytes.
