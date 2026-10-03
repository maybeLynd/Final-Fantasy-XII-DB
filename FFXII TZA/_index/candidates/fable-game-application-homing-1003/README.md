# Interior citations, cloud-drafted: game-application.md's entry-cited functions (FABLE, 2026-10-03)

The page named 178 F-frontier functions only at their entry. A Claude Code cloud session (https://claude.ai/code/session_01SCNjBjkQLVBQa4akEYXVn4, on FABLE's own cloud credit) drafted one sentence and 1-5 interior anchors per function from FABLE's annotated disassembly pack (`cloud-input/f-interior/` in the private snapshot repo, OPUS's listing code). FABLE checked every row mechanically with `fable_ingest.py` (OPUS's interior_ingest checks) and re-read every sentence against the listing before staging.

**Rows.** 177 staged with 844 anchors. Rejected by the mechanical check: 0. Skipped by the session: 1. Missing: 0.

**FABLE corrections on re-read.**

- `00798EB0`: `01F3DA1C` and `01F3DA20` are mutable .data dwords; 0x780/0x438 are only their static initial values, not fixed constants
- `001D9FD0`: 001DA032 tests only al, and the al==0 path from 001DA034 also reaches 005CD820/00210EB0/zeroing; 'both outcomes' left that path unstated
- `00673030`: 00673092..006730D3 copy only qwords +0,+8,+0x10,+0x18,+0x30,+0x40 and dwords +0x20,+0x38 (56 bytes); dwords +0x24 and +0x3c are not copied, so not the whole 0x48-byte element
- `0017F610`: ret at 0017F64B returns rax = the 001D50D0 result from 0017F631/0017F63B (0 on the null path via 0017F639), not nothing

**Verification.** [`interior_applier.py`](interior_applier.py) reads [`rows.json`](rows.json) and re-decodes every function first: every anchor is an instruction boundary inside its extent with the recorded mnemonic ([`.out`](interior_applier.out): FAILS 0; idempotent). The section is appended at publish time; the publish gates (address, neighbours, correction) run on the result.

**Limits.** Body statements, not meanings. A cloud draft is a pointer, not evidence: what stands here is FABLE's re-read. The session's agreement with FABLE is not independent review; SWE2-AUDIT-SPEC spot-checks.
