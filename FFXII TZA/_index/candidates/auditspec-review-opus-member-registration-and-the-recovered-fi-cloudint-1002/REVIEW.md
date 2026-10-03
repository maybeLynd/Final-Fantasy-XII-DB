# SWE2-AUDIT-SPEC review: OPUS cloud-drafted interior citations (opus-member-registration-and-the-recovered-fi-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting cloud session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-MEMBER-REGISTRATION-AND-THE-RECOVERED-FI-CL` · Package: `_index/candidates/opus-member-registration-and-the-recovered-fi-cloudint-1002/` · Page: `22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/member-registration-and-the-recovered-field-schema.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY / FAILS 0`.
- `rows.json`: 9 rows, 39 anchors; rejected 0, missing 0.
- Semantic pass: **all 9 rows** (the request asks for at least 15) read clause by clause against the resolved disassembly of the certified image (SHA256 73461D08..., rip targets resolved by `disr.py`). All 9 exact, including the bit-31-clear free gate (`shr 31; not al; test al,1`) in `0062A870`/`00672F30`/`006C7A40` and the unsigned `cmovb` minimum. Note only: `00672F30` copies `+0x20`/`+0x38` as dwords, so the "0x48 bytes" are copied field by field without their padding, which the row's own wording covers.
- Limits hold: body statements only, static evidence; a cloud draft plus OPUS's re-read is not independent review, this record is.
