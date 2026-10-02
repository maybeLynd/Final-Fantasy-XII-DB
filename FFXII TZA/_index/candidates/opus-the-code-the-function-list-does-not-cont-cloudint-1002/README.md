# Interior citations, cloud-drafted: the-code-the-function-list-does-not-contain.md's entry-cited functions (OPUS, 2026-10-02)

The page named 4 F-frontier functions only at their entry. A Claude Code cloud session (session_01XRXP3rS6fx4VxurArNZ8tP) drafted one sentence and 1-5 interior anchors per function from OPUS's annotated disassembly pack (`cloud-input/f-interior/` in the private snapshot repo). OPUS checked every row mechanically with `interior_ingest.py` and re-read every sentence against the bytes before applying.

**Rows.** 4 applied with 18 anchors. Rejected by the mechanical check: 0. Skipped by the session: 0. Missing: 0.

**OPUS corrections on re-read.**

- none needed

**Verification.** [`interior_applier.py`](interior_applier.py) reads [`rows.json`](rows.json) and re-decodes every function first. Every anchor is an instruction boundary inside its extent with the recorded mnemonic ([`.out`](interior_applier.out): FAILS 0; idempotent).

**Effect and gates.** All 4 rowed functions now measure A. On the page: `check_links` 0, `check_self_contradiction --db` 0, `check_consistency` 4 (the pre-existing four), `verify_doc_addresses --all` 0 documents to confirm.

**Limits.** Body statements, not meanings. A cloud draft is a pointer, not evidence: what stands here is OPUS's re-read. The session's agreement with OPUS is not independent review.

## Review (OPUS)

A non-author spot-check goes to SWE2-AUDIT-SPEC: at least 15 rows read against the bytes.

**Pass-22 neighbours (2026-10-02, OPUS).** `check_publish_neighbours.py` refused this page's first draft: a row sentence named another layer's function by address, which adds an unaccounted crossing. The row's own `0026A420` stays, so OPUS's crossing section gains a Script/VM CLIENT bullet for its two script-verb callers `00349E40` and `0034ACE0` (both bodies read). The rows were re-verified afterwards (`interior_applier.py`: ALREADY, FAILS 0), and `Tools/work/OPUS/nb_page.py` shows no new hit.
