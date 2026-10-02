# Audit-spec review: OPUS cloudint interior citations (opus-derived-call-signatures-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC · 2026-10-02 · Task: `OPUS-REQ-AUDITSPEC-OPUS-DERIVED-CALL-SIGNATURES-CLOUDINT-1002` · Package: `_index/candidates/opus-derived-call-signatures-cloudint-1002/`

## Verdict: ACCEPT

## What was checked

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY`/`FAILS 0` (idempotent).
- `rows.json` reconciles with the README: 11 rows applied, 40 anchors, rejected/skipped/missing 0.
- Semantic pass: all 11 rows exact vs the certified image: 00197980 (edx->ecx, tail 00197990), 00197990 (state validate + 0079E650/0079E6A0/0079E6D0 dispatch else 0), 00197A20 (byte+0x3A bit tests), 00197A50 (init + indirect callbacks), 002681C0 (movsx byte+0x12, tail 00269C70), 002D6640 (state store 02F973A0..AA + zero/zero tail), 002D6680/002D66A0/002D66C0 (accessors), 0032AB50/0032AB60 (byte-array index/mask bit set/clear at +0x14F4), 0057EBB0, 00792870 (list-head + vtable + alloc + zero loops), 0079D620 (ecx=2 tail 00796FC0), 007A08A0 (byte+0x69->9 else vtable+0x48 / +0x64 inc + tail 0079BDF0).
- Limits hold: body statements only.
