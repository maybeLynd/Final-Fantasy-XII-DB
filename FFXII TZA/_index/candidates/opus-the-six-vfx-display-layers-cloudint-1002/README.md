# Interior citations, cloud-drafted: the-six-vfx-display-layers.md's entry-cited functions (OPUS, 2026-10-02)

The page named 5 F-frontier functions only at their entry. A Claude Code cloud session (https://claude.ai/code/session_01Gc8PZstMPLLqppwXDU6yKq) drafted one sentence and 1-5 interior anchors per function from OPUS's annotated disassembly pack (`cloud-input/f-interior/` in the private snapshot repo). OPUS checked every row mechanically with `interior_ingest.py` and re-read every sentence against the bytes before applying.

**Rows.** 5 applied with 23 anchors. Rejected by the mechanical check: 0. Skipped by the session: 0. Missing: 0.

**OPUS corrections on re-read.**

- `0017FDE0`: pass-22: callee(s) outside the page's layer renamed by ledger name or role (unowned callees at 0017FDE0+0x4, 0017FDE0+0xC)
- `0017FE60`: pass-22: callee(s) outside the page's layer renamed by ledger name or role (unowned callees at 0017FE60+0x8, 0017FE60+0x10, 0017FE60+0x17, 0017FE60+0x1F)
- `0017FEE0`: pass-22: callee(s) outside the page's layer renamed by ledger name or role (unowned callees at 0017FEE0+0x8, 0017FEE0+0x10, 0017FEE0+0x17, 0017FEE0+0x1F)
- `001B2600`: pass-22: callee(s) outside the page's layer renamed by ledger name or role (unowned callees at 001B2600+0x9, 001B2600+0x21)
- `003A3990`: pass-22: callee(s) outside the page's layer renamed by ledger name or role: the call at 003A3990+0x39 reaches an unowned function

**Verification.** [`interior_applier.py`](interior_applier.py) reads [`rows.json`](rows.json) and re-decodes every function first. Every anchor is an instruction boundary inside its extent with the recorded mnemonic ([`.out`](interior_applier.out): FAILS 0; idempotent).

**Effect and gates.** All 5 rowed functions now measure A. On the page: `check_links` 0, `check_self_contradiction --db` 0, `check_consistency` 4 (the pre-existing four), `verify_doc_addresses --all` 0 documents to confirm.

**Limits.** Body statements, not meanings. A cloud draft is a pointer, not evidence: what stands here is OPUS's re-read. The session's agreement with OPUS is not independent review.

## Review (OPUS)

A non-author spot-check goes to SWE2-AUDIT-SPEC: at least 15 rows read against the bytes.
