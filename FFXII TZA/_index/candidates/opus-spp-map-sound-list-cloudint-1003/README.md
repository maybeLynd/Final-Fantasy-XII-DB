# Interior citations, cloud-drafted: spp-map-sound-list.md's entry-cited functions (OPUS, 2026-10-03)

OPUS drafted these rows itself from its F-interior pack (`f_pack.py`: each function the page cites only at its entry, with its annotated listing) and checked every row mechanically with `interior_ingest.py` (every anchor an instruction boundary inside the extent with the recorded mnemonic; every address a listing token). No second agent drafted or verified them, so the non-author check is SWE2-AUDIT-SPEC's.

**Rows.** 2 applied with 10 anchors. Rejected by the mechanical check: 0. Skipped by the session: 0. Missing: 0.

**OPUS corrections on re-read.**

- none needed

**Verification.** [`interior_applier.py`](interior_applier.py) reads [`rows.json`](rows.json) and re-decodes every function first. Every anchor is an instruction boundary inside its extent with the recorded mnemonic ([`.out`](interior_applier.out): FAILS 0; idempotent).

**Effect and gates.** All 2 rowed functions now measure A. On the page: `check_links` 0, `check_self_contradiction --db` 0, `check_consistency` 0 disagreements naming this page (tree total 2), `verify_doc_addresses --all` 0 REVIEW on this page (tree total 2).

**Limits.** Body statements, not meanings. A cloud draft is a pointer, not evidence: what stands here is OPUS's re-read. The session's agreement with OPUS is not independent review.

## Review (OPUS)

A non-author spot-check goes to SWE2-AUDIT-SPEC: at least 15 rows read against the bytes.
