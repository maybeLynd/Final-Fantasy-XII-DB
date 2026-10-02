# Audit-spec review: FABLE cloudint interior citations (fable-contract-phyre-cluster-header-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC · 2026-10-02 · Task: `FABLE-REQ-AUDITSPEC-FABLE-CONTRACT-PHYRE-CLUSTER-HEADER-CLOUDINT` · Package: `_index/candidates/fable-contract-phyre-cluster-header-cloudint-1002/`

## Verdict: ACCEPT

## What was checked

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY`/`FAILS 0` (idempotent).
- `rows.json` reconciles with the README: 4 rows applied, 19 anchors, rejected/skipped/missing 0.
- Semantic pass: every one of the 4 rows checked sentence-by-sentence against the shipping body in the certified image (SHA256 73461D08...) — all 4 rows exact: 00584E10 (00599770 result -> 0x54-byte copy via five movups blocks + dword+0x50, returns that dword), 0062F080 (two-qword unlink then self-link at rdx+8), 0067ADD0 (dword+0x10 copy, btr 31 arg, conditional 00861EBA, returns rcx), 006CC920 (byte+0x48 gate -> 005CD840/005CD5E0(rcx+0x28), returns 1).
- Limits hold: body statements only; static/native verification, no engine-in-loop or replay claims.
