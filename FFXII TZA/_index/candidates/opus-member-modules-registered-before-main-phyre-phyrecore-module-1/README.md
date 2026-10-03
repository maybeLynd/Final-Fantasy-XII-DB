# Family members explained one by one: 26 Phyre PhyreCore module members on the-fifteen-modules-registered-before-main.md (OPUS, 2026-10-03)

The page declares the family `Phyre PhyreCore module` (a classification family: ordinary functions grouped by module, not template copies). engine_explained did not credit these members. Another local Claude session (repos-91, session local-ee-drafter) drafted one sentence and 1-5 interior anchors per body from OPUS's pack (`mem_pack.py`, filtered against engine_explained's own set); OPUS checked every row mechanically with `interior_ingest.py` (member mode). A second local agent, not the drafter, then read every one of the 294 rows of this batch against the disassembly: 260 stood, 34 rows were corrected in 40 clauses (18 inline sub-objects written as the qword they hold, 6 signed compares written as above/below, 6 wrong arguments or offsets, 2 missed paths). OPUS confirmed corrections at the bytes on a sample; they are listed below. Neither agent is an independent reviewer: the non-author check is SWE2-AUDIT-SPEC's.

**Rows.** 26 applied with 116 anchors. Rejected by the mechanical check: 14. Skipped by the session: 0. Missing: 0.

**OPUS corrections on re-read.**

- `00186670`: byte verifier, re-read by OPUS: `jl` at 0018669E is a signed compare; 'below' is unsigned wording
- `00194A30`: byte verifier, re-read by OPUS: `jle` at 00194A41 is a signed compare; 'above' is unsigned wording
- `001967D0`: byte verifier, re-read by OPUS: outer loop bound is `jl` at 0019693E (signed); 'below' is unsigned wording
- `001967D0`: byte verifier, re-read by OPUS: the byte copy into `u` runs only when `v` is outside 1..3 (`ja` at 0019686C); when `v` is 1..3 and `p` is null the iteration does nothing (`je` 00196884 -> 001968BA)

**Verification.** [`interior_applier.py`](interior_applier.py) reads [`rows.json`](rows.json) and re-decodes every function first. Every anchor is an instruction boundary inside its extent with the recorded mnemonic ([`.out`](interior_applier.out): FAILS 0; idempotent).

**Effect and gates.** All 26 rowed functions now measure A. On the page: `check_links` 0, `check_self_contradiction --db` 0, `check_consistency` 0 disagreements naming this page (tree total 2), `verify_doc_addresses --all` 0 REVIEW on this page (tree total 2).

**Limits.** Body statements, not meanings. A cloud draft is a pointer, not evidence: what stands here is OPUS's re-read. The session's agreement with OPUS is not independent review.

## Review (OPUS)

A non-author spot-check goes to SWE2-AUDIT-SPEC: at least 15 rows read against the bytes.
