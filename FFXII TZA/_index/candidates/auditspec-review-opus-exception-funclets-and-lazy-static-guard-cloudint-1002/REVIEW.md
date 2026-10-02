# Audit-spec review: OPUS cloudint interior citations (opus-exception-funclets-and-lazy-static-guard-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC · 2026-10-02 · Task: `OPUS-REQ-AUDITSPEC-OPUS-EXCEPTION-FUNCLETS-AND-LAZY-STATIC-GUARD-CL`
Package: `_index/candidates/opus-exception-funclets-and-lazy-static-guard-cloudint-1002/`

## Verdict: ACCEPT

## What was checked

- `interior_applier.py` re-run fresh → exit 0, `FAILS 0` (idempotent).
- `rows.json` reconciles with the README: 4 rows applied, 15 anchors, rejected/skipped/missing 0.
- Semantic sample: all 4 rows read against the certified image —
  - `001DAAC0` exact: `005CC8C0(&record, 001DADB0)`, +0x18=3, +0x20="FileCachePrefetchManager"
    (009005E8), +0x2C=0xFFFFFFFE, +0x8=0xF000, `0016D6A0(&record, 0x7C)`, then rcx at record+0x10,
    dword 1 at rcx+0x20, `005CD1E0(rcx, &record)`, byte 1 at rcx+0x18.
  - `0089BEF0` exact: rbp=rdx in a 0x40 frame, returns 0xFFFFFFFF (or eax,-1).
  - `008A5B7C` exact: returns 1 iff dword [[rcx]] == 0xC0000005.
  - `008A5C0A` exact: rcx stored at rbp+0x40/+0x30, [rcx] at rbp+0x38; on dword == 0xE06D7363 calls
    `00862052()` and returns its eax, else stores 0 at rbp+0x20 and returns 0.
- Limits hold: body statements only.
