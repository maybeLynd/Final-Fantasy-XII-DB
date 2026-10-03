# Family members explained one by one: 36 Phyre PAnimation module members on the-fifteen-modules-registered-before-main.md (OPUS, 2026-10-03)

The page declares the family `Phyre PAnimation module` (a classification family: ordinary functions grouped by module, not template copies). engine_explained did not credit these members. Another local Claude session (repos-91, session local-ee-drafter) drafted one sentence and 1-5 interior anchors per body from OPUS's pack (`mem_pack.py`, filtered against engine_explained's own set); OPUS checked every row mechanically with `interior_ingest.py` (member mode). A second local agent, not the drafter, then read every one of the 295 rows of this batch against the disassembly: 286 stood, 9 rows were corrected in 14 clauses (signed compares worded above/below, two missing pass-through arguments, one wrong value on a path, one overgeneralised compare direction, one 16-bit edge). OPUS confirmed corrections at the bytes on a sample; they are listed below. Neither agent is an independent reviewer: the non-author check is SWE2-AUDIT-SPEC's.

**Rows.** 36 applied with 178 anchors. Rejected by the mechanical check: 0. Skipped by the session: 2. Missing: 0.

**OPUS corrections on re-read.**

- `005A6900`: byte verifier, re-read by OPUS: signed compare (jle at 005A6938) worded as 'above'
- `005A6B40`: byte verifier, re-read by OPUS: signed compare (jl at 005A6B6E) worded as 'below'
- `005A6B40`: byte verifier, re-read by OPUS: signed compare (jge/jl at 005A6BDD/005A6C48) worded as 'below'
- `005A6B40`: byte verifier, re-read by OPUS: signed compare (jge/jl at 005A6C8C/005A6D01) worded as 'above'
- `005A7220`: byte verifier, re-read by OPUS: signed compare (jge/jl at 005A7257/005A72C8) worded as 'below'
- `005A7220`: byte verifier, re-read by OPUS: signed compare (jge/jl at 005A730C/005A7371) worded as 'above'
- `005A7990`: byte verifier, re-read by OPUS: the memcmp at 005A7A02 is memcmp(qword [rdx+8], qword [k+8]); a positive result means the rdx bytes are larger, not k

**Verification.** [`interior_applier.py`](interior_applier.py) reads [`rows.json`](rows.json) and re-decodes every function first. Every anchor is an instruction boundary inside its extent with the recorded mnemonic ([`.out`](interior_applier.out): FAILS 0; idempotent).

**Effect and gates.** All 36 rowed functions now measure A. On the page: `check_links` 0, `check_self_contradiction --db` 0, `check_consistency` 0 disagreements naming this page (tree total 2), `verify_doc_addresses --all` 0 REVIEW on this page (tree total 2).

**Limits.** Body statements, not meanings. A cloud draft is a pointer, not evidence: what stands here is OPUS's re-read. The session's agreement with OPUS is not independent review.

## Review (OPUS)

A non-author spot-check goes to SWE2-AUDIT-SPEC: at least 15 rows read against the bytes.
