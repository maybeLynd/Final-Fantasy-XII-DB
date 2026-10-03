# SWE2-AUDIT-SPEC review: OPUS cloud-drafted interior citations (opus-generated-float-table-builders-ee-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-GENERATED-FLOAT-TABLE-BUILDERS-EE-1003` · Package: `_index/candidates/opus-generated-float-table-builders-ee-1003/` · Page: `00-Engine-Core-Runtime/Startup-Data-Construction/generated-float-table-builders.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh, verify mode (no `--apply`) -> `VERIFY 2 functions, 10 anchors`, `ALREADY`, `FAILS 0`.
- `rows.json`: 2 rows, 10 anchors; 7 rejected by the mechanical check (not applied, not reviewed here), 0 skipped, 0 missing.
- Semantic pass: **both rows** (the request asks for at least 15; the package has 2) read clause by clause against `disr.py` output of the certified image. Both exact.
  - `004C2040`: `memset(rcx, 0, 0xc20)` at `004C2051`; every listed immediate matches its store at `004C2056`..`004C2148`, including the dword/qword widths (qwords `+0xbb8`, `+0xc14`, `+0xbf8`, `+0xc08`; `+0xc00` and dword `+0xc1c` from `eax` = 0 set at `004C205D`); `eax` is never changed after, so the return is 0.
  - `004DF360`: the cell index words `[02064DD0]`/`[02064DB0]` are read with `movsx` and scaled by 16 into `02064E30`; `[c]` gets `movzx` of the 16-bit sum word `02064DB8` + `0x8000` (`004DF3A7`..`004DF3B6`); bytes `+4..+0xf` are written from the just-stored copy at `02064C64` (8 bytes) plus `psrldq 0xc` dword at `+0xc`; `02064DB4` is first `w+0x352` and replaced by `w+0x2bc` unless `w` equals the *pre-store* word `02064DB0` minus `0x2bc` (`je` at `004DF3FC`, equality, polarity correct); `call r11` with `rcx` = `c`, `rdx` = incoming `rdx`, `r8` = 0; the final two stores re-read `02064B0C`/`02064DB4` after the call, as stated.
- Limits hold: body statements only, static evidence; a cloud draft plus OPUS's re-read is not independent review, this record is.
