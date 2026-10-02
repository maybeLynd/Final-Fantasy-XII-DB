# Interior citations, cloud-drafted: how-a-character-is-lit.md's entry-cited functions (OPUS, 2026-10-02)

The page named 4 F-frontier functions only at their entry. A Claude Code cloud session (https://claude.ai/code/session_01Gc8PZstMPLLqppwXDU6yKq) drafted one sentence and 1-5 interior anchors per function from OPUS's annotated disassembly pack (`cloud-input/f-interior/` in the private snapshot repo). OPUS checked every row mechanically with `interior_ingest.py` and re-read every sentence against the bytes before applying.

**Rows.** 4 applied with 18 anchors. Rejected by the mechanical check: 0. Skipped by the session: 0. Missing: 0.

**OPUS corrections on re-read.**

- `003477E0`: pass-22: callee(s) outside the page's layer renamed by ledger name or role (unowned and ActorEntity callees at 003477E0+0x4, 003477E0+0x15)
- `00347D60`: pass-22: callee(s) outside the page's layer renamed by ledger name or role (unowned and ActorEntity callees at 00347D60+0x4, 00347D60+0x12)
- `003DD6C0`: pass-22: callee(s) outside the page's layer renamed by ledger name or role (ActorEntity and unowned callees at 003DD6C0+0x18, 003DD6C0+0x5C, 003DD6C0+0x35, 003DD6C0+0x55)

**Verification.** [`interior_applier.py`](interior_applier.py) reads [`rows.json`](rows.json) and re-decodes every function first. Every anchor is an instruction boundary inside its extent with the recorded mnemonic ([`.out`](interior_applier.out): FAILS 0; idempotent).

**Effect and gates.** All 4 rowed functions now measure A. On the page: `check_links` 0, `check_self_contradiction --db` 0, `check_consistency` 4 (the pre-existing four), `verify_doc_addresses --all` 0 documents to confirm.

**Limits.** Body statements, not meanings. A cloud draft is a pointer, not evidence: what stands here is OPUS's re-read. The session's agreement with OPUS is not independent review.

## Review (OPUS)

A non-author spot-check goes to SWE2-AUDIT-SPEC: at least 15 rows read against the bytes.
