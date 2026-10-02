# Audit-spec review: FABLE cloudint interior citations (fable-the-npc-name-dictionary-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC · 2026-10-02 · Task: `FABLE-REQ-AUDITSPEC-FABLE-THE-NPC-NAME-DICTIONARY-CLOUDINT-1002` · Package: `_index/candidates/fable-the-npc-name-dictionary-cloudint-1002/`

## Verdict: ACCEPT

## What was checked

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY`/`FAILS 0` (idempotent).
- `rows.json` reconciles with the README: 4 rows applied, 20 anchors, rejected/skipped/missing 0.
- Semantic pass: every one of the 4 rows checked sentence-by-sentence against the shipping body in the certified image (SHA256 73461D08...) — all 4 rows exact: 001DA220/001DA970 (triple gate -> word+0xE8 store + 005CD4F0/001D9930/005CD820/001D9EC0 call order), 00275F10 (dispatch: id1 payload dwords +0xC8/+0xCC and qword +0xC0; id 0x10 sign-extended +0xCC compare -> 00244F00; id 0x12 vtable-slot call with stack record dword+0xC8 + 16 zero bytes at +8; else 005C5230), 00521290 (0x100 entries stride 0x30 from 02CA8450, skip word 0xFFFF, dword+4 match -> entry address via index*0x30).
- Limits hold: body statements only; static/native verification, no engine-in-loop or replay claims.
