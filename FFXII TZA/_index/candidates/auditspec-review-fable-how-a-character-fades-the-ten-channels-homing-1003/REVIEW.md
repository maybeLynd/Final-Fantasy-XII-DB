# SWE2-AUDIT-SPEC review: FABLE interior citations (fable-how-a-character-fades-the-ten-channels-homing-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOW-A-CHARACTER-FADES-THE-TEN-CHANNELS` · Package: `_index/candidates/fable-how-a-character-fades-the-ten-channels-homing-1003/` · Page: `17-Presentation-Rendering/Character-Render-Records/how-a-character-fades-the-ten-channels.md` (commit b7c6eb07d)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 1 functions, 1 anchors / ALREADY / FAILS 0` (exit 0).
- `rows.json`: 1 row(s), 1 anchors; rejected 0, missing 0.
- Semantic pass: **every row** read clause by clause against `disr.py` output of the certified image (SHA256 73461D08...), call offsets resolved:
  - `0042E540` exact: `mov edx, dword [rdx+0x74]` / `jmp 0x420e70` with `rcx` untouched.
- Limits hold: body statements only, static evidence; the draft and FABLE's re-read are not independent review, this record is.
