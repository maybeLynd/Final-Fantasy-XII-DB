# SWE2-AUDIT-SPEC review: FABLE cloud-drafted interior citations (fable-field-record-table-navimapdata-homing-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for Devin; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-FIELD-RECORD-TABLE-NAVIMAPDATA-HOMING` · Package: `_index/candidates/fable-field-record-table-navimapdata-homing-1003/` · Page: `03-World-Area-Field/Field-Record-Table/field-record-table-navimapdata.md` (commit eea05327e; reviewed at HEAD f8b2904c0, package and page unchanged since and unmodified in the working tree)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` was re-run fresh without `--apply`. It printed `VERIFY 1 functions, 5 anchors`, `ALREADY` and `FAILS 0`. The committed `.out` is the pre-apply `DRY` run with the same counts.
- `rows.json`: 1 row and 5 anchors, `mode: homing`. Rejected 0, skipped 0, missing 0, corrections 0. The row is on the page at line 1242 (heading at line 1236), byte for byte.
- Semantic pass: **every row** was read clause by clause against `disw.py` output of the certified image (SHA256 73461D08...).
  - **`0031BD80`: exact.**
    - Three exits go to `0031BDB3 mov eax, 0xffff`: a null `rcx` (`0031BD8B`), a null `00263E30(rcx)` at +0xD (`0031BD95`), and a null qword `+0x698` (`0031BDA1`).
    - Otherwise `rcx = qword + 0x50`, `edx` restored from `ebx`, and the tail jump to `0031BDC0` (`0031BDAE`).
- Limits hold: body statements only, static evidence. The cloud draft and FABLE's re-read are not independent review; this record is.
