# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-cross-subsystem-accessor-hubs-ee-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-CROSS-SUBSYSTEM-ACCESSOR-HUBS-EE-1003-A8F85` · Package: `_index/candidates/opus-cross-subsystem-accessor-hubs-ee-1003/` · Page: `00-Engine-Core-Runtime/Shared-State-Accessors/cross-subsystem-accessor-hubs.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 1 functions, 5 anchors / ALREADY / FAILS 0` (exit 0).
- `rows.json`: 1 row(s), 5 anchors. **Every row** read clause by clause against raw capstone output of the whole body in the certified image (SHA256 73461D08...); every relative call resolved:
  - `003B50E0` exact: `movsxd rbx, ecx` and `movsx rcx, bx` (the low word sign-extended), `t` = `002EA030(edx)`; -1 word -> 0; `R` = `[022C6F28]` + 0x740 w, `cmove` 0 when dword `R+0x284` is 0; `003E56C0(R)` null -> 0; `002EA030(0)` match -> byte `+0xCD`, `002EA030(1)` match -> byte `+0xCE`, else 0.
- Limits hold: body statements only, static evidence; the draft and OPUS's re-read are not independent review, this record is.
