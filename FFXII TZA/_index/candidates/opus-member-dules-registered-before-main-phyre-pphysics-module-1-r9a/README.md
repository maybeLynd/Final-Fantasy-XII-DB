# Family members explained one by one: 7 Phyre PPhysics module members on the-fifteen-modules-registered-before-main.md (OPUS, 2026-10-03)

The page declares the family `Phyre PPhysics module` (a classification family: ordinary functions grouped by module, not template copies). No page explained these members. A local drafting agent (local-ee-drafter) drafted one sentence and 1-5 interior anchors per body from OPUS's pack (`mem_pack.py`); OPUS checked every row mechanically with `interior_ingest.py` (member mode: the body is an unexplained member of a family this page declares) and re-read every sentence against the bytes before applying.

**Rows.** 7 applied with 35 anchors. Rejected by the mechanical check: 0. Skipped by the session: 13. Missing: 0.

**OPUS corrections on re-read.**

- `00691C00`: byte re-read by a non-drafting agent: Body checks out (c/p test with the redundant p == qword [c+0x60] compare, both list walks and unlinks, slot +8 / slot +0 with edx 1, the three zeroings, tail jmp 00691D40). Defect: branch scope. 'when g is non-null: ...; then calls the vtable slot +8 ...' reads as inside the g block, but a null g jumps (je 00691CDF) straight to the slot calls, zeroings and tail-jump, which run on every path. Made explicit.

**Verification.** [`interior_applier.py`](interior_applier.py) reads [`rows.json`](rows.json) and re-decodes every function first. Every anchor is an instruction boundary inside its extent with the recorded mnemonic ([`.out`](interior_applier.out): FAILS 0; idempotent).

**Effect and gates.** All 7 rowed functions now measure A. On the page: `check_links` 0, `check_self_contradiction --db` 0, `check_consistency` 0 disagreements naming this page (tree total 3), `verify_doc_addresses --all` 0 REVIEW on this page (tree total 2).

**Limits.** Body statements, not meanings. A cloud draft is a pointer, not evidence: what stands here is OPUS's re-read. The session's agreement with OPUS is not independent review.

## Review (OPUS)

A non-author spot-check goes to SWE2-AUDIT-SPEC: at least 15 rows read against the bytes.
