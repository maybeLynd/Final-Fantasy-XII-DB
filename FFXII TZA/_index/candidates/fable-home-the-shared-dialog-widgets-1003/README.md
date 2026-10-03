# Homed frontier bodies on the-shared-dialog-widgets.md (FABLE, 2026-10-03)

No page cited these 2 functions. Each is entered directly from a function this page already cites. A Claude Code cloud session (https://claude.ai/code/session_015VFSZr38WAiiWF7vDja8Ar, on FABLE's own cloud credit) drafted one sentence, the call site and 1-5 interior anchors per function from FABLE's homing pack (`cloud-input/homing/` in the private snapshot repo). FABLE checked every row mechanically with `homing_ingest.py` and re-read every sentence against the listing before staging. Part of the three-way F homing split (FABLE caller-host, OPUS callee-host, SWE2-EC7 the rest), board `FABLE-HOMING-CALLER-HOST-1003`.

**Rows.** 2 staged with 10 anchors. Rejected by the mechanical check: 0. Skipped by the session: 0. Missing: 0.

**FABLE corrections on re-read.**

- `003FF9A0`: 003FF9B7 loads +0x170 of the +0x108 pointer, not of the object at 0209AC30 that 'that object' named

**Verification.** [`homing_applier.py`](homing_applier.py) re-decodes every function: each `entered from` site is a direct call or jump to it from a caller this page cites, and every anchor is an instruction boundary inside its extent with the recorded mnemonic ([`.out`](homing_applier.out): FAILS 0; idempotent). The section is appended at publish time; the publish gates run on the result.

**Limits.** Body statements, not meanings. A cloud draft is a pointer, not evidence: what stands here is FABLE's re-read. SWE2-AUDIT-SPEC spot-checks.
