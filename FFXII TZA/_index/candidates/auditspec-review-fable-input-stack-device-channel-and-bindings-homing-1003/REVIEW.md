# SWE2-AUDIT-SPEC review: FABLE interior citations (fable-input-stack-device-channel-and-bindings-homing-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-INPUT-STACK-DEVICE-CHANNEL-AND-BINDING` · Package: `_index/candidates/fable-input-stack-device-channel-and-bindings-homing-1003/` · Page: `15-Input/Input-Stack/input-stack-device-channel-and-bindings.md` (commit b7c6eb07d)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 5 functions, 25 anchors / ALREADY / FAILS 0` (exit 0).
- `rows.json`: 5 row(s), 25 anchors; rejected 0, missing 0.
- Semantic pass: **every row** read clause by clause against `disr.py` output of the certified image (SHA256 73461D08...), call offsets resolved:
  - `00343C60` exact: `00267E10(r9)` at `+0x10`, `00267310(byte rdx+0x15)` at `+0x1B`, `cmovne ebx, ecx` (0 when the second is non-zero) into `00361200(first, 1, 1)`; then `0025D5D0` at `+0x36`, `00267310(byte +0x15)` at `+0x3F` and, when non-zero, `00360960(-1, 0, 0)` at `+0x50`.
  - `005DCD10` exact: bit 31 of dword `[rcx]` clear and qword `+8` non-null -> `00662EA0` per element at stride `0x88` for the count, then `00584730(array)`; both paths store 0 to qword `+8` and dword `[rcx]`.
  - `005DE1D0` exact: `0060B750(qword [O+0x28], rcx+8, O)` when `O` = qword `[rcx]` is non-null; `[rcx]` = 0; tail `jmp 0x16d6a0` with `rcx+8`.
  - `00670790` exact: 7th argument `[rsp+0x38]`; v from its dword `+8`, else the first non-zero dword `+4` over `dword [sixth] & 0x7FFFFFFF` stride-0x88 elements (0 when none); `edx` = dword `+0x18` of the 5th; tail `006224E0` with the 8th moved to the 5th slot (`006707F0`), else `00622350(rdx, edx, 0, v)`.
  - `00670810` exact: the same selection; with the 7th non-null the 8th and 9th move to the 5th and 6th slots (`00670871`-`00670878`, `0067086A`) before `jmp 006226D0`; otherwise the 9th moves to the 5th (`00670884`) before `jmp 00622450`.
- Limits hold: body statements only, static evidence; the draft and FABLE's re-read are not independent review, this record is.
