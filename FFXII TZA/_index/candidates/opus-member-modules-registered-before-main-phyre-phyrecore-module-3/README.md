# Family members explained one by one: 27 Phyre PhyreCore module members on the-fifteen-modules-registered-before-main.md (OPUS, 2026-10-03)

The page declares the family `Phyre PhyreCore module` (a classification family: ordinary functions grouped by module, not template copies). engine_explained did not credit these members. Another local Claude session (repos-91, session local-ee-drafter) drafted one sentence and 1-5 interior anchors per body from OPUS's pack (`mem_pack.py`, filtered against engine_explained's own set); OPUS checked every row mechanically with `interior_ingest.py` (member mode). A second local agent, not the drafter, then read every one of the 294 rows of this batch against the disassembly: 260 stood, 34 rows were corrected in 40 clauses (18 inline sub-objects written as the qword they hold, 6 signed compares written as above/below, 6 wrong arguments or offsets, 2 missed paths). OPUS confirmed corrections at the bytes on a sample; they are listed below. Neither agent is an independent reviewer: the non-author check is SWE2-AUDIT-SPEC's.

**Rows.** 27 applied with 129 anchors. Rejected by the mechanical check: 13. Skipped by the session: 0. Missing: 0.

**OPUS corrections on re-read.**

- `001F41A0`: byte verifier, re-read by OPUS: `00809054` gets `rcx` = qword `[rcx+0xA8]` itself (001F41F2), i.e. `b`+8, not `b`; only `00809950` gets `b` (001F4225)
- `001F5B80`: byte verifier, re-read by OPUS: the `this` passed is the inline allocator object `rcx+0x50` itself and its vtable is qword `[rcx+0x50]`; 'slot of qword `[rcx+0x50]`' names one dereference too many (rows 7.23-7.26 use the same phrase for the object held in the qword)
- `001F8B30`: byte verifier, re-read by OPUS: the `this` passed is the inline allocator object `rcx+0x88` itself and its vtable is qword `[rcx+0x88]`; 'slot of qword `[rcx+0x88]`' names one dereference too many (rows 7.23-7.26 use the same phrase for the object held in the qword)

**Verification.** [`interior_applier.py`](interior_applier.py) reads [`rows.json`](rows.json) and re-decodes every function first. Every anchor is an instruction boundary inside its extent with the recorded mnemonic ([`.out`](interior_applier.out): FAILS 0; idempotent).

**Effect and gates.** All 27 rowed functions now measure A. On the page: `check_links` 0, `check_self_contradiction --db` 0, `check_consistency` 0 disagreements naming this page (tree total 2), `verify_doc_addresses --all` 0 REVIEW on this page (tree total 2).

**Limits.** Body statements, not meanings. A cloud draft is a pointer, not evidence: what stands here is OPUS's re-read. The session's agreement with OPUS is not independent review.

## Review (OPUS)

A non-author spot-check goes to SWE2-AUDIT-SPEC: at least 15 rows read against the bytes.
