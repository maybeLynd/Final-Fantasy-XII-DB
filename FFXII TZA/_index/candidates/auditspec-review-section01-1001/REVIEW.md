# Audit-spec section acceptance: SECTION-01 (Update01)

Reviewer: SWE2-AUDIT-SPEC · 2026-10-01 · Task `OPUS-REQ-AUDITSPEC-SECTION01-ACCEPT-1001`
Subject: merge tail `a3707ab82`; owner review `section01-owner-review.md` (conditional:
accept corrections, restore dropped evidence before publication).

## Verdict: ACCEPT

## Condition check — every demanded restoration present at HEAD

`CONTRACT-apply-result-to-target.md`: ORACLE's EXP-148/149 specifics all present
(`002F9A60`/`002F9B20`/`002F9BD0` 3/3/2, `0030FED0` 12, `00316A50`+`00D10460`,
the lethal chain `00377C20`/`0030E360`/`00312280`/`0032A150`/`00306F00`/`003299B0`,
§2 interface row `00311608`–`00311777`). `CONTRACT-battle-unit-construction.md`:
`0023A580`–`0023A594`, `00300F6D`, `0023A5B0`, `0023AAB1`, EXP-047 — all present.

**I11 note:** the literal token is gone; it was an orphan reference in the pre-merge page
(§12 named "the observable I11" but the list ended at I8). The substance — numeric/steal/item/
timer/gil branches do not raise the flag, and no stat-panel refresh follows plain damage —
survives renumbered as merged I4 and §11's FED0 note. The demand's intent is met; the name is not.
Recorded rather than silently ruled.

## Byte-verified anchors (certified image)

- `0023A633` `and qword ptr [rdi], 0xFFFFFFFFFBFFFFFF` — bit 26 clear (U2) ✓
- `002FEAB0` = `xor eax,eax / mov qword [rcx+0xEAC], rax / ret`, 10 B (U4) ✓
- `0023AB5F movzx r12d, byte [rsi+0x2B]` feeding the `cvtdq2ps`/`mulss` ×1.5 (U6) — spot-consistent ✓

## Scope note

Owner review's "not re-derived" list stands: R1, R4, R5, R6's full flag map, R7, U1, U5 are
accepted at the section's stated fixture scope — NATIVE/STATIC plus fixture receipts, no live-game
claim. The page holds as a section for the canonical consumers.
