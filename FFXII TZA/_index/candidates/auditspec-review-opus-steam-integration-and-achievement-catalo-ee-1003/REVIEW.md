# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-steam-integration-and-achievement-catalo-ee-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-STEAM-INTEGRATION-AND-ACHIEVEMENT-CAT-315ED` · Package: `_index/candidates/opus-steam-integration-and-achievement-catalo-ee-1003/` · Page: `20-Platform-Online-Achievements/steam-integration-and-achievement-catalogue.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 1 functions, 5 anchors / ALREADY / FAILS 0` (exit 0).
- `rows.json`: 1 row(s), 5 anchors. **Every row** read clause by clause against raw capstone output of the whole body in the certified image (SHA256 73461D08...); every relative call resolved:
  - `007DDC20` exact: imports resolved - `008C2308` AcquireSRWLockExclusive, `008C22F8` ReleaseSRWLockExclusive, `008C2198` SetEvent, `008C20A8` GetLastError; the signed `jl 4` capacity test and 0x80004005; the signed remainder 4 (`and 0x80000003` with the sign fix-up) indexing `+0x74`; `inc +0x84`; the GetLastError HRESULT folding for a positive error.
- Limits hold: body statements only, static evidence; the draft and OPUS's re-read are not independent review, this record is.
