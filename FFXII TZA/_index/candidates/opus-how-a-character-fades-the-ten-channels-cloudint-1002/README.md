# Interior citations, cloud-drafted: how-a-character-fades-the-ten-channels.md's entry-cited functions (OPUS, 2026-10-02)

The page named 19 F-frontier functions only at their entry. A Claude Code cloud session (https://claude.ai/code/session_019LqHiXRaWmgLrNYjxULfMf) drafted one sentence and 1-5 interior anchors per function from OPUS's annotated disassembly pack (`cloud-input/f-interior/` in the private snapshot repo). OPUS checked every row mechanically with `interior_ingest.py` and re-read every sentence against the bytes before applying.

**Rows.** 19 applied with 83 anchors. Rejected by the mechanical check: 0. Skipped by the session: 0. Missing: 0.

**OPUS corrections on re-read.**

- `002915C0`: pass-22: callee(s) outside the page's layer renamed by ledger name or role (unowned, ActorEntity, Resource and UI callees at 002915C0+0x64, 002915C0+0x7D, 002915C0+0x8A, 002915C0+0x9E, 002915C0+0xB4, 002915C0+0xF3, 002915C0+0x132, 002915C0+0x13F, 002915C0+0x15A)
- `002E84B0`: pass-22: callee(s) outside the page's layer renamed by ledger name or role: the jmp at 002E84B0+0x42 reaches an unclassified function
- `002E8500`: pass-22: callee(s) outside the page's layer renamed by ledger name or role: the jmp at 002E8500+0x36 reaches an unclassified function
- `00348700`: pass-22: callee(s) outside the page's layer renamed by ledger name or role (Script_VM and Thunk callees at 00348700+0xC, 00348700+0x25)
- `00348B00`: pass-22: callee(s) outside the page's layer renamed by ledger name or role (Script_VM and Thunk callees at 00348B00+0x11, 00348B00+0x1C, 00348B00+0x21)
- `00348F20`: pass-22: callee(s) outside the page's layer renamed by ledger name or role (Script_VM and Thunk callees at 00348F20+0x16, 00348F20+0x21, 00348F20+0x39)
- `003497D0`: pass-22: callee(s) outside the page's layer renamed by ledger name or role (Script_VM callee at 003497D0+0xC)
- `00373160`: copy direction reversed: `0046D100` (a jmp to a 64-byte copy that loads [rdx] and stores [rcx]) gets rcx = A entry+0xC0 (00373160+0x1AB) and rdx = E entry+0xC0 (00373160+0x19D), and rcx = A+0x150 (00373160+0x1C5) with rdx = E+0x150 (00373160+0x1BE), so E is copied into A; pass-22: callee(s) outside the page's layer renamed by ledger name or role (CoreRuntime and unowned callees at 00373160+0x19, 00373160+0xD8, 00373160+0x105, 00373160+0x11F, 00373160+0x137, 00373160+0x192)
- `0041FBF0`: pass-22: callee(s) outside the page's layer renamed by ledger name or role (CoreRuntime and Resource callees at 0041FBF0+0x1F, 0041FBF0+0x32)
- `0042DE50`: pass-22: callee(s) outside the page's layer renamed by ledger name or role: the call at 0042DE50+0x14 reaches an unclassified function

**Verification.** [`interior_applier.py`](interior_applier.py) reads [`rows.json`](rows.json) and re-decodes every function first. Every anchor is an instruction boundary inside its extent with the recorded mnemonic ([`.out`](interior_applier.out): FAILS 0; idempotent).

**Effect and gates.** All 19 rowed functions now measure A. On the page: `check_links` 0, `check_self_contradiction --db` 0, `check_consistency` 4 (the pre-existing four), `verify_doc_addresses --all` 0 documents to confirm.

**Limits.** Body statements, not meanings. A cloud draft is a pointer, not evidence: what stands here is OPUS's re-read. The session's agreement with OPUS is not independent review.

## Review (OPUS)

A non-author spot-check goes to SWE2-AUDIT-SPEC: at least 15 rows read against the bytes.
