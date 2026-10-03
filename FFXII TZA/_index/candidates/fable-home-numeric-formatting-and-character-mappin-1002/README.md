# Homed frontier bodies on numeric-formatting-and-character-mapping.md (FABLE, 2026-10-02)

No page cited these 8 functions. Each is entered directly from a function this page already cites. A Claude Code cloud session (https://claude.ai/code/session_01G1D6BV8reSc8hRtefJLZec, on FABLE's own cloud credit) drafted one sentence, the call site and 1-5 interior anchors per function from FABLE's homing pack (`cloud-input/homing/` in the private snapshot repo). FABLE checked every row mechanically with `homing_ingest.py` and re-read every sentence against the listing before staging. Part of the three-way F homing split (FABLE caller-host, OPUS callee-host, SWE2-EC7 the rest), board `FABLE-HOMING-CALLER-HOST-1003`.

**Rows.** 8 staged with 32 anchors. Rejected by the mechanical check: 0. Skipped by the session: 0. Missing: 0.

**FABLE corrections on re-read.**

- `002A4030`: the body null-tests rcx, a and b but substitutes 0 and carries on instead of returning; those paths were not stated
- `0028F750`: o is re-read from the global after the call, not kept across it

**Verification.** [`homing_applier.py`](homing_applier.py) re-decodes every function: each `entered from` site is a direct call or jump to it from a caller this page cites, and every anchor is an instruction boundary inside its extent with the recorded mnemonic ([`.out`](homing_applier.out): FAILS 0; idempotent). The section is appended at publish time; the publish gates run on the result.

**Limits.** Body statements, not meanings. A cloud draft is a pointer, not evidence: what stands here is FABLE's re-read. SWE2-AUDIT-SPEC spot-checks.
