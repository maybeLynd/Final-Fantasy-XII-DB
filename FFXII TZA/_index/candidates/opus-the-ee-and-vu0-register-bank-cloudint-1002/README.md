# Interior citations, cloud-drafted: the-ee-and-vu0-register-bank.md's entry-cited functions (OPUS, 2026-10-02)

The page named 9 F-frontier functions only at their entry. A Claude Code cloud session (https://claude.ai/code/session_019LqHiXRaWmgLrNYjxULfMf) drafted one sentence and 1-5 interior anchors per function from OPUS's annotated disassembly pack (`cloud-input/f-interior/` in the private snapshot repo). OPUS checked every row mechanically with `interior_ingest.py` and re-read every sentence against the bytes before applying.

**Rows.** 9 applied with 40 anchors. Rejected by the mechanical check: 0. Skipped by the session: 0. Missing: 0.

**OPUS corrections on re-read.**

- `002330D0`: pass-22: callee(s) outside the page's layer renamed by ledger name or role: the call at 002330D0+0x10 reaches a Movement-owned function
- `0029BC80`: the 0xA1 call is not under the rcx test: the null branch at 0029BC80+0x177 lands on 0029BC80+0x197, just before the call at 0029BC80+0x19F; pass-22: callee(s) outside the page's layer renamed by ledger name or role (unowned and Boundary callees at 0029BC80+0x3D, 0029BC80+0x85, 0029BC80+0x9C, 0029BC80+0xAB, 0029BC80+0xFE, 0029BC80+0x14A, 0029BC80+0x155, 0029BC80+0x19F)
- `0050C670`: pass-22: callee(s) outside the page's layer renamed by ledger name or role (unowned, Runtime and Script_VM callees at 0050C670+0xD, 0050C670+0x1D, 0050C670+0x31)
- `0050C8D0`: pass-22: callee(s) outside the page's layer renamed by ledger name or role (unowned, Runtime and Script_VM callees at 0050C8D0+0xD, 0050C8D0+0x1D, 0050C8D0+0x31)
- `00510870`: pass-22: callee(s) outside the page's layer renamed by ledger name or role (Script_VM, unowned, Runtime and ActorEntity callees at 00510870+0x26, 00510870+0x48, 00510870+0x5B, 00510870+0x6C, 00510870+0x7A, 00510870+0x87, 00510870+0x93, 00510870+0xA2, 00510870+0xAE, 00510870+0xBC)
- `006BA940`: pass-22: callee(s) outside the page's layer renamed by ledger name or role (Boundary, CRT and Phyre callees at 006BA940+0x1C, 006BA940+0x36, 006BA940+0x50, 006BA940+0x5E)

**Verification.** [`interior_applier.py`](interior_applier.py) reads [`rows.json`](rows.json) and re-decodes every function first. Every anchor is an instruction boundary inside its extent with the recorded mnemonic ([`.out`](interior_applier.out): FAILS 0; idempotent).

**Effect and gates.** All 9 rowed functions now measure A. On the page: `check_links` 0, `check_self_contradiction --db` 0, `check_consistency` 4 (the pre-existing four), `verify_doc_addresses --all` 0 documents to confirm.

**Limits.** Body statements, not meanings. A cloud draft is a pointer, not evidence: what stands here is OPUS's re-read. The session's agreement with OPUS is not independent review.

## Review (OPUS)

A non-author spot-check goes to SWE2-AUDIT-SPEC: at least 15 rows read against the bytes.
