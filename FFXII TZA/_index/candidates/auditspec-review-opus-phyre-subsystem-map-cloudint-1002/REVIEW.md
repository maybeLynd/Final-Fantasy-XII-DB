# Audit-spec review: OPUS cloudint interior citations (opus-phyre-subsystem-map-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC · 2026-10-02 · Task: `OPUS-REQ-AUDITSPEC-OPUS-PHYRE-SUBSYSTEM-MAP-CLOUDINT-1002` · Package: `_index/candidates/opus-phyre-subsystem-map-cloudint-1002/`

## Verdict: ACCEPT

## What was checked

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY`/`FAILS 0` (idempotent).
- `rows.json` reconciles with the README: 6 rows applied, 24 anchors, rejected/skipped/missing 0.
- Semantic pass: every one of the 6 rows checked sentence-by-sentence against the shipping body in the certified image (SHA256 73461D08...) — all 6 rows exact: 005AA2C0 ([rcx]=00D31298 + 10-byte helper on +8 non-null), 00646AB0 ([rcx]=00D61E50; bit31-clear AND >1 AND non-null +0x38 -> helper; then zero +0x38/+0x30), 00691DB0 ([rcx]=00D79830; vtable slot0 edx=1 on +0x78; zero +0x78/+0x68; [rcx]=00D79790), 007933C0 ([rcx]=01CB24A8; helper on +0x28; zero +0x28/+0x30/+0x40; tail 00793410), 00793570 ([rcx]=01CB24C8; eh iter (rcx+0xB0,0x48,4,icall); [rcx]=01CB23C0), 00793750 ([rcx]=01CB2468; helpers on +0x20/+0x48).
- Limits hold: body statements only; static/native verification, no engine-in-loop or replay claims.
