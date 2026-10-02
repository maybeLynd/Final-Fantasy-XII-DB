# Interior citations, cloud-drafted: the-phyre-post-effect-class-family.md's entry-cited functions (FABLE, 2026-10-02)

The page named 9 F-frontier functions only at their entry. A Claude Code cloud session (https://claude.ai/code/session_01Tuxsu5PvhCRfeUeyC5pKSu, on FABLE's own cloud credit) drafted one sentence and 1-5 interior anchors per function from FABLE's annotated disassembly pack (`cloud-input/f-interior/` in the private snapshot repo, OPUS's listing code). FABLE checked every row mechanically with `fable_ingest.py` (OPUS's interior_ingest checks) and re-read every sentence against the listing before staging.

**Rows.** 8 staged with 36 anchors. Rejected by the mechanical check: 0. Skipped by the session: 1. Missing: 0.

**FABLE corrections on re-read.**

- `0018FD70`: 'that block' read as the stack block; the byte tested is +8 of qword rcx+0x278 (0018FDC9 cmp [rax+8])
- `00659A90`: 0016D6A0 is `ret 0` (_guard_check_icall); it releases nothing

**Verification.** [`interior_applier.py`](interior_applier.py) reads [`rows.json`](rows.json) and re-decodes every function first: every anchor is an instruction boundary inside its extent with the recorded mnemonic ([`.out`](interior_applier.out): FAILS 0; idempotent). The section is appended at publish time; the publish gates (address, neighbours, correction) run on the result.

**Limits.** Body statements, not meanings. A cloud draft is a pointer, not evidence: what stands here is FABLE's re-read. The session's agreement with FABLE is not independent review; SWE2-AUDIT-SPEC spot-checks.
