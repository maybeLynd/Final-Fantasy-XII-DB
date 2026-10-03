# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-the-ordered-container-runtime-ee-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-THE-ORDERED-CONTAINER-RUNTIME-EE-1003-B9FBA` · Package: `_index/candidates/opus-the-ordered-container-runtime-ee-1003/` · Page: `24-Compiler-And-CRT-Runtime/Cxx-Runtime-Families/the-ordered-container-runtime.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 1 functions, 5 anchors / ALREADY / FAILS 0` (exit 0).
- `rows.json`: 1 row(s), 5 anchors. **Every row** read clause by clause against raw capstone output of the whole body in the certified image (SHA256 73461D08...); every relative call resolved:
  - `001BD040` exact on both insert paths: the unsigned descent from `[m+0x18]` with `setb`; p and the `[m+0x10]` / `0016D720(p)` predecessor step; slot +0x10 of `m+0x30` with (0x40, 0); `001BC950(b+0x20, r)` behind its null test; `0016D840(b, p, h, s)` with p the ORIGINAL last node (`r14`) on the second path; `inc [m+0x28]`; the 0/1 flag at `o+8`; o returned.
- Limits hold: body statements only, static evidence; the draft and OPUS's re-read are not independent review, this record is.
