# Interior citations, cloud-drafted: the-battle-stats-record-field-map.md's entry-cited functions (OPUS, 2026-10-02)

The page named 3 F-frontier functions only at their entry. A Claude Code cloud session (https://claude.ai/code/session_01Gc8PZstMPLLqppwXDU6yKq) drafted one sentence and 1-5 interior anchors per function from OPUS's annotated disassembly pack (`cloud-input/f-interior/` in the private snapshot repo). OPUS checked every row mechanically with `interior_ingest.py` and re-read every sentence against the bytes before applying.

**Rows.** 3 applied with 15 anchors. Rejected by the mechanical check: 0. Skipped by the session: 0. Missing: 0.

**OPUS corrections on re-read.**

- `003478A0`: pass-22: callee(s) outside the page's layer renamed by ledger name or role (ActorEntity, Script_VM, unowned and CRT callees at 003478A0+0x34, 003478A0+0x54, 003478A0+0x98, 003478A0+0xA3, 003478A0+0xB0)
- `003509E0`: the loop count is the return of the selector call at 003509E0+0x46 (movsxd r12, eax at 003509E0+0x4D), taken before the result-writer call at 003509E0+0x53, not 'that call's'; pass-22: callee(s) outside the page's layer renamed by ledger name or role (Script_VM, Party, ActorEntity and CRT callees at 003509E0+0x35, 003509E0+0x46, 003509E0+0x53, 003509E0+0x79, 003509E0+0x89, 003509E0+0x95, 003509E0+0xA3, 003509E0+0xB8, 003509E0+0xDB, 003509E0+0xE8)
- `00560210`: the +0x40-record store lands at +0x18 (00560210+0x59 mov [rbx+0x18], rax); the +0x0 and +0x8 records keep their top byte (00560210+0x246 and [rbx+0x28], 0xFF000000 with 00560210+0x24D and eax, 0xFFFFFF) while +0x28/+0x30/+0x38 take whole dwords (00560210+0x2C4); pass-22: callee(s) outside the page's layer renamed by ledger name or role (unowned, Boundary and Items/License callees at 00560210+0x29, 00560210+0x47, 00560210+0x52, 00560210+0x69, 00560210+0x7F, 00560210+0x8B, 00560210+0xE8, 00560210+0x118, 00560210+0x199, 00560210+0x241, 00560210+0x3DB)

**Verification.** [`interior_applier.py`](interior_applier.py) reads [`rows.json`](rows.json) and re-decodes every function first. Every anchor is an instruction boundary inside its extent with the recorded mnemonic ([`.out`](interior_applier.out): FAILS 0; idempotent).

**Effect and gates.** All 3 rowed functions now measure A. On the page: `check_links` 0, `check_self_contradiction --db` 0, `check_consistency` 4 (the pre-existing four), `verify_doc_addresses --all` 0 documents to confirm.

**Limits.** Body statements, not meanings. A cloud draft is a pointer, not evidence: what stands here is OPUS's re-read. The session's agreement with OPUS is not independent review.

## Review (OPUS)

A non-author spot-check goes to SWE2-AUDIT-SPEC: at least 15 rows read against the bytes.
