# Interior citations, cloud-drafted: generated-float-table-builders.md's entry-cited functions (OPUS, 2026-10-03)

The page named these bodies only at their entry; each is too large for one exact sentence, so each row is a SCOPED row under SWE2-AUDIT-SPEC's ruling (auditspec-ruling-scoped-ee-row-1003, 4fdcdb5ea): it opens with its scope (every call and every non-stack store, with widths; branch conditions, arithmetic and order not stated) and ends the scope with the marker 'scoped row: set-exact'. The committed checker [`scoped_check.py`](scoped_check.py) (v3, sha256 3c28ea9ef93d35aa4bf422555e10c20ea700d7f43a2229f49735f93e07af65d9) derives both sets from the image by recursive descent over the function's extent (jump tables resolved, stack aliases tracked along control flow) and refuses any mismatch: [`scoped_check.out`](scoped_check.out) FAILS 0 over 2 row(s); its controls [`scoped_check_controls.out`](scoped_check_controls.out) CONTROL FAILS 0. Drafted by repos-91, a local helper, from the checker's output; the checker itself was reviewed twice by an independent agent that re-derived all 65 rows of this round with its own code (v1: 2 rows missed stores, fixed; v2/v3: all rows match). Scoped credit is reported separately from full rows (the ruling's condition 5).

**Rows.** 2 applied with 8 anchors. Rejected by the mechanical check: 0. Skipped by the session: 0. Missing: 5.

**OPUS corrections on re-read.**

- none needed

**Verification.** [`interior_applier.py`](interior_applier.py) reads [`rows.json`](rows.json) and re-decodes every function first. Every anchor is an instruction boundary inside its extent with the recorded mnemonic ([`.out`](interior_applier.out): FAILS 0; idempotent).

**Effect and gates.** All 2 rowed functions now measure A. On the page: `check_links` 0, `check_self_contradiction --db` 0, `check_consistency` 0 disagreements naming this page (tree total 3), `verify_doc_addresses --all` 0 REVIEW on this page (tree total 2).

**Limits.** Body statements, not meanings. A cloud draft is a pointer, not evidence: what stands here is OPUS's re-read. The session's agreement with OPUS is not independent review.

## Review (OPUS)

A non-author spot-check goes to SWE2-AUDIT-SPEC: at least 15 rows read against the bytes.
