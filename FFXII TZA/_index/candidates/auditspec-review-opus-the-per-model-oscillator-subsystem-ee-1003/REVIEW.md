# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-the-per-model-oscillator-subsystem-ee-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-THE-PER-MODEL-OSCILLATOR-SUBSYSTEM-EE-B5F98` · Package: `_index/candidates/opus-the-per-model-oscillator-subsystem-ee-1003/` · Page: `17-Presentation-Rendering/Model-And-Motion-Formats/the-per-model-oscillator-subsystem.md` (commit b0c7c5a57)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `ALREADY / FAILS 0` (exit 0).
- `rows.json`: 1 row(s), 5 anchors; rejected 0, missing 0.
- Semantic pass: **every row and every callee whose inputs or result the row names** read against raw capstone output of the certified image (SHA256 73461D08...):
  - `0040ABF0` exact: `and byte [rcx+0x3F], 0xF7` (`0040AC0E`); `dil` to `+0x3E`; byte `[rsp+0x70]` (argument 5 after the 0x48-byte frame) `& 1`, `shl 3`, ORed into `+0x3F` (`0040AC28`); `edx` == 0 -> epilogue (`0040AC30`); 16 bytes `[r8]` -> `+0x40`; stack vector (0.0, 1.0 from `01CEBBA8`, `00D108A0` = 9.9999997e-06) passed as `rcx` and `rdx` with `r8` = `rcx+0x40` to `00202E10` (`0040AC72`, which reads `rdx` and `r8` - a cross product); the three results to `+0x50/+0x54/+0x58`; `00380800(rbx+0x50, rbx+0x50)`; `0020E620(01EFFA30 + 32*(edx-1))` (`0040ACB4`; `0020E620` = `ecx - [01F83530]`) to dword `+0x2C`; `or byte +0x3F, 2`; `si` (= `r9d`) to word `+0x3C`; cookie `01F44830` / `00808C40`.
  - Advisory: the row lists "sets `0x2`" before the `0020E620` store; in the code the `or` follows that call (`0040ACB9`). The callee cannot see the byte, so the effect set is the same.
- Limits hold: body statements only, static evidence; the draft and OPUS's re-read are not independent review, this record is.
