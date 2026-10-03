# SWE2-AUDIT-SPEC review: OPUS cloud-drafted interior citations (opus-choosing-the-render-target-for-a-text-ru-cloudint-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting cloud session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-CHOOSING-THE-RENDER-TARGET-FOR-A-TEXT-451CB` · Package: `_index/candidates/opus-choosing-the-render-target-for-a-text-ru-cloudint-1003/` · Page: `99-Unresolved-Residual/Glyph-Run-Rendering/choosing-the-render-target-for-a-text-run.md` (commit 890844135)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 1 functions, 5 anchors`, `ALREADY`, `FAILS 0`.
- `rows.json`: 1 row, 5 anchors; rejected 0, missing 0.
- Semantic pass: **every row** read clause by clause against `disr.py` output of the certified image (SHA256 73461D08...):
  - `003655F0` exact: `t` = `[[022CBE00] + rcx*8 + 0x10]` (`movsxd rdx, ecx`, signed slot); count dword `t+4` tested `jle` (signed); 0xC-byte stride from `t+0x10` comparing word `+0` with 0x30 (`00365613`); no match returns 0 (`00365623`); on the match `0017FD00(ecx+0xb)` (`0036562B add ecx, 0xb` / `0036562E`), `f` = `0017F8C0(word [entry])` (`00365636`), non-null `f` returns `0017F9C0(dword f+0x1c)` through `cvttss2si` (`00365648`, truncation), null `f` returns `movzx` byte `+4` (`00365652`).
- Limits hold: body statements only, static evidence; the cloud draft and OPUS's re-read are not independent review, this record is.
