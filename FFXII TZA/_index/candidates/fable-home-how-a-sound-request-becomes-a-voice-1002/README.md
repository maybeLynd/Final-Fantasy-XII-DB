# Homed frontier bodies on how-a-sound-request-becomes-a-voice.md (FABLE, 2026-10-02)

No page cited these 11 functions. Each is entered directly from a function this page already cites. A Claude Code cloud session (https://claude.ai/code/session_01Dq1LGzf21EuvVAMphWnGMn, on FABLE's own cloud credit) drafted one sentence, the call site and 1-5 interior anchors per function from FABLE's homing pack (`cloud-input/homing/` in the private snapshot repo). FABLE checked every row mechanically with `homing_ingest.py` and re-read every sentence against the listing before staging. Part of the three-way F homing split (FABLE caller-host, OPUS callee-host, SWE2-EC7 the rest), board `FABLE-HOMING-CALLER-HOST-1003`.

**Rows.** 7 staged with 31 anchors. Rejected by the mechanical check: 4. Skipped by the session: 0. Missing: 0.

**FABLE corrections on re-read.**

- `00207F50`: `test r8b, 8` / `test r8b, 0x10` test bits 3 and 4 (masks 8 and 0x10), not 'bit 8' / 'bit 0x10'; the end check is `cmp rdx, rax; je` (inequality), not 'lies before'; `008C2430` is an import slot called indirectly
- `002081A0`: `test dl, 8` / `test dl, 0x10` test bits 3 and 4 (masks 8 and 0x10), not 'bit 8' / 'bit 0x10'; the end check is an inequality, not 'lies before'; both returns set only `al` (`xor al, al` / `mov al, 1`)

**Verification.** [`homing_applier.py`](homing_applier.py) re-decodes every function: each `entered from` site is a direct call or jump to it from a caller this page cites, and every anchor is an instruction boundary inside its extent with the recorded mnemonic ([`.out`](homing_applier.out): FAILS 0; idempotent). The section is appended at publish time; the publish gates run on the result.

**Limits.** Body statements, not meanings. A cloud draft is a pointer, not evidence: what stands here is FABLE's re-read. SWE2-AUDIT-SPEC spot-checks.
