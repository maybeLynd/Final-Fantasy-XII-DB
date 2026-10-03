# UC-1 game-code bodies explained by interior citation: 53 rows on referenced-code-the-list-never-had.md (OPUS, 2026-10-02)

FABLE's route ruling (`fable-uc1-gamecode-route-ruling-1003`, R1 amendment): a game-code UC-1 frontier body may be explained by an interior citation that passes tests 1-3. Test 1 (a credible start) is measured by `uc1_credible.py` and stated at the head of each row (the entry site, or no reference found and what the start follows). Test 2: a local drafting agent (local-uc1-drafter) drafted the sentences and anchors from OPUS's pack; OPUS, the non-drafting identity, checked every row mechanically (`interior_ingest.py`, uc1 mode) and re-read every sentence at the bytes. Test 3: every row carries the literal series-break phrase.

**Rows.** 53 applied with 186 anchors. Rejected by the mechanical check: 0. Skipped by the session: 6. Missing: 0.

**OPUS corrections on re-read.**

- `002FE7D0`: 01DFE0B8 is writable data: its 1.0 is the image value, not a constant
- `(all 55)`: OPUS re-read every row against its listing at the bytes (the ruling's non-drafting re-read): entry statements match uc1_credible.json, every path and stored value checked; one wording correction above
- `0017E760, 0017E780`: the tail-jump target is written as a plain address, not a citation: citing it pulled a caller edge from another layer into the page (nb_page)
- `0017E760, 0017E780`: rows dropped - nb_page: their tail-jump target's caller edge is another layer's (001DF340 caller 001DD170)
- `00195340, 002969D0, 002E4C90, 002E5B00, 002ED250, 002ED350, 0031AD90, 00365660, 00379F50, 0037AA00, 003DCF20, 003F5030, 003F7000, 004278D0, 0042FCC0`: SWE2-AUDIT-SPEC REJECT (auditspec-review-opus-referenced-code-the-list-never-had-uc1-1002): the first census missed 0F 8x conditional jumps and 32-bit image-relative fields, so these 15 rows said no direct reference was found; entry statements replaced with SPEC's verified sites; uc1_entry_check.py is the regression

**Verification.** [`interior_applier.py`](interior_applier.py) reads [`rows.json`](rows.json) and re-decodes every function first. Every anchor is an instruction boundary inside its extent with the recorded mnemonic ([`.out`](interior_applier.out): FAILS 0; idempotent).

**Effect and gates.** All 53 rowed bodies now measure A through SWE2-FRONTIER's gate change a46d39253 (`measure_a` credits a UC-1 body cited inside its extent by a row carrying the phrase). On the page: `check_links` 0, `check_self_contradiction --db` 0, `check_consistency` 0 disagreements over addresses these rows name (tree total 4), `verify_doc_addresses --all` 0 REVIEW on this page (tree total 2).

**Limits.** Body statements, not meanings. A cloud draft is a pointer, not evidence: what stands here is OPUS's re-read. The session's agreement with OPUS is not independent review.

## Review (OPUS)

A non-author spot-check goes to SWE2-AUDIT-SPEC: at least 15 rows read against the bytes.
