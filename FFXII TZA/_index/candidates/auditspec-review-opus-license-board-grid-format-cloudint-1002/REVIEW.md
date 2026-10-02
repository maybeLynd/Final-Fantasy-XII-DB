# Audit-spec review: OPUS cloudint interior citations (opus-license-board-grid-format-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC · 2026-10-02 · Task: `OPUS-REQ-AUDITSPEC-OPUS-LICENSE-BOARD-GRID-FORMAT-CLOUDINT-1002` · Package: `_index/candidates/opus-license-board-grid-format-cloudint-1002/`

## Verdict: ACCEPT

## What was checked

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY`/`FAILS 0` (idempotent).
- `rows.json` reconciles with the README: 2 rows applied, 9 anchors, rejected/skipped/missing 0.
- Semantic pass: both rows exact vs the certified image: 003FDAD0 verified in full (002D45C0(+0xD8,1), bit27 of +0xE0 = (qword+0xE0 non-null), 002445C0, 002C1A80(m,word 02F9736A,0,word 02F97368,word 02F9736C) veto path clearing bit27 and returning 0, signed 5-bit A@16-20/B@21-25 of dword+0x180, 0x400|0x80->00563EC0 gated on B>0 or 0x480, 0x800|0x20->00564300 gated on B<A-1 or 0x820, slot at rcx+0xF0+oldB*8 three-word fill (first via 32-byte table at qword+0xE0 else 0xFFFF), 002527B0(8,slot byte+7+0x20,slot word+0), 005655F0(rcx,newslot,0), 005674B0(qword+0xC8,newslot), bit27 refresh + 002445C0 + 00249C60(10) + ret 1, else 002D3900(+0xD8)+ret 0) and 00511F50 (00280120 passthrough non-zero -> return result; else two 00267E10(r9) pops -> 00560070(second,first)).
- Limits hold: body statements only.
