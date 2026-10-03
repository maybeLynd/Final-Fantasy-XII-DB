# Homed frontier bodies on the-element-types-80-97.md (FABLE, 2026-10-03)

No page cited these 6 functions. Each is entered directly from a function this page already cites. A Claude Code cloud session (https://claude.ai/code/session_015VFSZr38WAiiWF7vDja8Ar, on FABLE's own cloud credit) drafted one sentence, the call site and 1-5 interior anchors per function from FABLE's homing pack (`cloud-input/homing/` in the private snapshot repo). FABLE checked every row mechanically with `homing_ingest.py` and re-read every sentence against the listing before staging. Part of the three-way F homing split (FABLE caller-host, OPUS callee-host, SWE2-EC7 the rest), board `FABLE-HOMING-CALLER-HOST-1003`.

**Rows.** 6 staged with 30 anchors. Rejected by the mechanical check: 0. Skipped by the session: 0. Missing: 0.

**FABLE corrections on re-read.**

- `0047BFB0`: 0047BFB6/0047C01D/0047C04E read the .data floats 01E02838/01E02834/01E02830 (written by 004BF500) before the reset call at 0047C089, so 02064CC8/CC0/CC4 hold those sums and the later tests and y/z values use the stored c0/c8, not the bare constants
- `00487D60`: 00487E09/00487F25 add the .data floats 01E02830/01E02834 (written by 004BF500) before the truncation and the 02064CB4 store; and the both-W path falls through from 00487E3D into the C test at 00487E4C rather than ending after the call
- `0048D240`: 0048D314/0048D436 add the .data floats 01E02830/01E02834 (written by 004BF500) before the truncation and the 02064CB4 store; and the both-W path falls through from 0048D348 into the C test at 0048D35E rather than ending after the call
- `0048F790`: 0048F7ED compares x with the .data float 01E02830 (written by 004BF500); no reset call precedes it in this body, so it is not a constant 0

**Verification.** [`homing_applier.py`](homing_applier.py) re-decodes every function: each `entered from` site is a direct call or jump to it from a caller this page cites, and every anchor is an instruction boundary inside its extent with the recorded mnemonic ([`.out`](homing_applier.out): FAILS 0; idempotent). The section is appended at publish time; the publish gates run on the result.

**Limits.** Body statements, not meanings. A cloud draft is a pointer, not evidence: what stands here is FABLE's re-read. SWE2-AUDIT-SPEC spot-checks.
