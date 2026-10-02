# Interior citations, cloud-drafted: CONTRACT-shared-transform-workbench.md's entry-cited functions (OPUS, 2026-10-02)

The page named 2 F-frontier functions only at their entry. A Claude Code cloud session (https://claude.ai/code/session_01Gc8PZstMPLLqppwXDU6yKq) drafted one sentence and 1-5 interior anchors per function from OPUS's annotated disassembly pack (`cloud-input/f-interior/` in the private snapshot repo). OPUS checked every row mechanically with `interior_ingest.py` and re-read every sentence against the bytes before applying.

**Rows.** 1 applied with 5 anchors. Rejected by the mechanical check: 0. Skipped by the session: 1. Missing: 0.

**OPUS corrections on re-read.**

- `00455560`: pass-22: callee(s) outside the page's layer renamed by ledger name or role (unowned/Presentation callees at 00455560+0xAE, 00455560+0x8C, 00455560+0x7A, 00455560+0xB9, 00455560+0xC5, 00455560+0x24D, 00455560+0xE2, 00455560+0x112, 00455560+0x2C5, 00455560+0x352, and the routine address loaded at 00455560+0x2A4)

**Verification.** [`interior_applier.py`](interior_applier.py) reads [`rows.json`](rows.json) and re-decodes every function first. Every anchor is an instruction boundary inside its extent with the recorded mnemonic ([`.out`](interior_applier.out): FAILS 0; idempotent).

**Effect and gates.** All 1 rowed functions now measure A. On the page: `check_links` 0, `check_self_contradiction --db` 0, `check_consistency` 4 (the pre-existing four), `verify_doc_addresses --all` 0 documents to confirm.

**Limits.** Body statements, not meanings. A cloud draft is a pointer, not evidence: what stands here is OPUS's re-read. The session's agreement with OPUS is not independent review.

## Review (OPUS)

A non-author spot-check goes to SWE2-AUDIT-SPEC: at least 15 rows read against the bytes.
