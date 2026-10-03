# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-binding-profiles-remapping-and-control--1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-BINDING-PROFILES-REMAPPING-AND-CO` · Package: `_index/candidates/fable-home-binding-profiles-remapping-and-control--1002/` · Page: `15-Input/Binding-Profiles/binding-profiles-remapping-and-control-state.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `homing_applier.py` was re-run fresh from the package directory with the analysis venv python. It exited 0 and printed `VERIFY 2 functions, 5 anchors` / `ALREADY` / `FAILS 0`. Without `--apply` it only verifies; `ALREADY` means the section is already on the page. It wrote nothing.
- `rows.json`: 2 rows, 5 anchors; mechanically rejected 3, skipped 0, missing 0.
- Semantic pass: **all 2 rows** read clause by clause against the full `disr.py` disassembly of the certified image (rip targets resolved; image-base-relative forms rebased on `00120000`). Every call offset, stack-argument slot, compare signedness and branch polarity was checked. Each entered_from site was disassembled and confirmed as a direct call or jump to the body. Host fit was checked against every citation of the caller on the page outside the homed section.
- `001E0980`: two `InputManager_GetSingleton` calls; the second result goes into the `00196710` tail-jump. `002498A0`: `[02F97364] & 0x800`.
- Host: `002284F0` (the `0xD0`-byte widget proc) and `001EC060` (the profile record builder) are read on the page.
- Limits: body statements only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is.
