# Audit-spec review: OPUS cloudint interior citations (opus-section-006-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC · 2026-10-02 · Task: `OPUS-REQ-AUDITSPEC-OPUS-SECTION-006-CLOUDINT-1002` · Package: `_index/candidates/opus-section-006-cloudint-1002/` · evidence commit `2af7ff424`

## Verdict: ACCEPT

## What was checked

- `interior_applier.py` re-run fresh -> `VERIFY 4 functions, 19 anchors`, `ALREADY`, `FAILS 0` (idempotent).
- `rows.json` reconciles with the README: 4 rows, 19 anchors, rejected/skipped/missing 0.
- Semantic sample: all 4 rows (full population) read against the certified image -- all 4 exact, incl. 001B1C10's full tree-insert path (dual 0x100 buffers, size-1-when-first-byte-zero length quirk verified -- the loop never reloads the byte, the 008C3020 per-byte import loop, lower_bound on dword+0x20 key, the +0x50/+0x78 chain search for 02CBB900 with dword+0x74 nonzero, the stepped-qword+0xF8 value store at node+0x28); 00249350/00249380 ctor wrappers incl. the incoming 5th-stack-arg re-load at [rsp+0x28]; 0035C160's sub-chain dispatch (cases 1/4/12/18, 005C5230 passthrough), case-4 word 2-5 gate, 0x80-when-3 byte, clamp 0x100000..0x400000 and the (v-0x100000)*0.5/3145728+0.5 scale feeding 002D8650.
- Limits hold: body statements only.
