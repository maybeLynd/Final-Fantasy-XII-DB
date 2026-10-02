# Interior citations, cloud-drafted: mh-movie-seek-index.md's entry-cited functions (OPUS, 2026-10-02)

The page named 2 F-frontier functions only at their entry. A Claude Code cloud session (session_01EsnYZKbu767dCnSLHP8iar) drafted one sentence and 1-5 interior anchors per function from OPUS's annotated disassembly pack (`cloud-input/f-interior/` in the private snapshot repo). OPUS checked every row mechanically with `interior_ingest.py` and re-read every sentence against the bytes before applying.

**Rows.** 2 applied with 10 anchors. Rejected by the mechanical check: 0. Skipped by the session: 0. Missing: 0.

**OPUS corrections on re-read.**

- none needed

**Verification.** [`interior_applier.py`](interior_applier.py) reads [`rows.json`](rows.json) and re-decodes every function first. Every anchor is an instruction boundary inside its extent with the recorded mnemonic ([`.out`](interior_applier.out): FAILS 0; idempotent).

**Effect and gates.** All 2 rowed functions now measure A. On the page: `check_links` 0, `check_self_contradiction --db` 0, `check_consistency` 4 (the pre-existing four), `verify_doc_addresses --all` 0 documents to confirm.

**Limits.** Body statements, not meanings. A cloud draft is a pointer, not evidence: what stands here is OPUS's re-read. The session's agreement with OPUS is not independent review.

## Review (OPUS)

A non-author spot-check goes to SWE2-AUDIT-SPEC: at least 15 rows read against the bytes.

**Pass-22 neighbours (2026-10-02, OPUS).** `check_publish_neighbours.py` refused this page's first draft: a row sentence named another layer's function by address, which adds an unaccounted crossing. `005CC930` is now named by role in the row (the QPC time getter); the row's own `001D9F90` stays, so the page gains an OPUS crossing section with the Platform SERVICE edge it calls (`QueryPerformanceCounter`, import slot `008C2188`). The rows were re-verified afterwards (`interior_applier.py`: ALREADY, FAILS 0), and `Tools/work/OPUS/nb_page.py` shows no new hit.
