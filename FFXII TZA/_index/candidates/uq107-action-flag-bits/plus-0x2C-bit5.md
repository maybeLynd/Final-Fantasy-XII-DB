# UQ-107: `+0x2C` bit 5 and the "register-mask" sites (FABLE, Claude Opus 5.5, 2026-09-27)

The six `test word [row+0x2C], ax` / `cmp word, cx` sites the 09-17 narrowing credited to "the status-mask family"
test immediates loaded just before them:
- 00323F4D mov eax, 0x2000 / 00323F52 test (BattleStats_HasRequiredLicenseForAction): word bit 13 = +0x2D bit 5
- 003852A6 mov eax, 0x200 / 003852AB (BattleFormula_BuildCandidateStatusMask): bit 9 = +0x2D bit 1
- 0038737D mov eax, 0x200 / 00387382 (BattleAction_ComputeAuthoredStatusMask): bit 9
- 00387675 mov eax, 0x200 / 0038767A (003875D0): bit 9
- 0039110D mov eax, 0x400 / 00391112 (00390F20): bit 10 = +0x2D bit 2 (known)
- 0039118D mov eax, 0x800 / 00391192 (00390F20): bit 11 = +0x2D bit 3
- 0030341C mov ecx, 0x8000 / 00303434 cmp word, cx; setae (AiOrder_EvaluateTargetSelector): bit 15 = +0x2D bit 7
Bare value reads: 002376F0 x4 and 003871CE `& 7` (element); 00322B62 `test cl, 0x40` (bit 6); 00308CF2 `shr 0xc` / `shr 0xf`.
So bit 5 (0x20, 166 rows) is read at none of the 40 verified sites: dead in this build by that census.
Open for UQ-107: what each +0x0C bit gates at its reader (the 23 sites of action-row-0x0C-bit-readers.tsv).

