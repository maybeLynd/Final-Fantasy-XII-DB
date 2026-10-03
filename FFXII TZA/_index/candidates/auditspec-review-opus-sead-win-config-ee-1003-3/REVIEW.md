# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-sead-win-config-ee-1003-3)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-SEAD-WIN-CONFIG-EE-1003-3-A0E1B` · Package: `_index/candidates/opus-sead-win-config-ee-1003-3/` · Page: `18-Audio/Sound-Bank-And-Voice-Formats/sead-win-config.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 1 functions, 5 anchors / ALREADY / FAILS 0` (exit 0).
- `rows.json`: 1 row(s), 5 anchors. **Every row** read clause by clause against raw capstone output of the whole body in the certified image (SHA256 73461D08...); every relative call resolved:
  - `007DD9F0` exact: imports resolved from the PE import table - `008C2308` AcquireSRWLockExclusive, `008C22F8` ReleaseSRWLockExclusive, `008C2120` OutputDebugStringA; the old object's slot +0 with 1; `007AD460(8, 0x50, 1)`, `memset` 0x50, vtables `01CB7B80`/`01CB7BD8`/`01CB7C20`, the zeroed qwords and dword +0x48; slot +8 with (a, o+0x10) unchecked; the fallback `007AD460(8, 0x48, 1)` with `01CB80F8` and the three -1 qwords, its slot +8 to E on negative; `o+8` or 0 (`cmove`) to `[[o+0x30]+8]`; slot +0x20 with `[o+0x40]`; the negative arm's release, `0019C5D0(s, 0x100, 01CB8218, r)`, the `jl 0xff` / -2 adjustment, the newline, the `jae 0x100` terminator check to `00809728` (`007DDC0F`), OutputDebugStringA and `007A5570(2, s)`; the release on every other path; `r` returned.
- Limits hold: body statements only, static evidence; the draft and OPUS's re-read are not independent review, this record is.
