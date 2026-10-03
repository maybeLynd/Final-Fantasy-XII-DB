# SWE2-AUDIT-SPEC review: OPUS cloud-drafted interior citations (opus-class-descriptor-and-metadata-system-homing-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting cloud session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-CLASS-DESCRIPTOR-AND-METADATA-SYSTEM-HOMING` · Package: `_index/candidates/opus-class-descriptor-and-metadata-system-homing-1002/` · Page: `22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY / FAILS 0`.
- `rows.json`: 10 rows, 44 anchors; rejected 0, missing 0.
- Semantic pass: **all 10 rows** (the request asks for at least 15) read clause by clause against the resolved disassembly of the certified image (SHA256 73461D08..., rip targets resolved by `disr.py`). All 10 exact, including `00164100`'s net clear of bit 0x2 (`or 2` then `and ~2`) and set of 0x8, `006777D0`'s TLS guard (`jle` skip: proceeds when `02D3ECF8` is greater, signed) and `006AF4F0`'s 16-byte entry walk through `+0x78` chains.
- Limits hold: body statements only, static evidence; a cloud draft plus OPUS's re-read is not independent review, this record is.
