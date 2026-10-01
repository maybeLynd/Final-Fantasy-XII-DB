# Affected-consumer check: UQ-107's 2026-09-18 `+0x0C` census corrected (FABLE, Claude Opus 5.5, 2026-09-27)

affected: 07-Combat-Action/Action-Definition-Row/the-action-definition-row.md (the UQ-107 box's 2026-09-18 narrowing)

also annotated: `07-Combat-Action/Action-Definition-Row/members/action-row-0x0C-bit-readers.tsv` (a header line
marks it as 23 of the 60 reads; its rows stay as published)

run: uq107_flag_bits.py at bbd3af82a (worktree = that HEAD plus this package), 3 checks, FAILS 0. F1 and F3 measure the
correction.

**The change.** My 2026-09-18 narrowing, and the table it published, had four defects.
- It called its 23 sites "every provenance-verified read"; the follower finds 60.
- It said the immediates `0x1`..`0x8`, `0x60`, `0x200000`, `0x3000000`, `0x10000000` and `0x20000000` "are not the
  action row's". The 2026-09-19 correction re-examined three of them and left "the others … not re-examined". All
  are the action row's: `0031EB20` (`BattleMenu_BuildCommandEntryList`), `003230E0` and `00327A10` test them on
  verified row pointers.
- It said bits 12 and 24 "together" set shape 3 in `0031A990`. Bit 24 alone sets 3; bit 12 gives 0, or 5.
- It called `0x8000221B` a "reason" (it is the status mask passed to `0030E9C0`), and cited the `and` instructions
  `002F868F` / `002F849A` as the `shr`s (`002F868C` / `002F8497`).

The clauses are struck with a dated note, and the box is ticked with the answer at publish time.

| consumer | what it says | state |
|---|---|---|
| the action-row page, UQ-107 box narrowing of 2026-09-18 / 2026-09-19 | the clauses above | revised-here |
| `members/action-row-0x0C-bit-readers.tsv` | "every provenance-verified read", 23 rows | revised-here (a header line; the rows stay as the 09-18 record) |
| the action-row page `+0x0C` field row | bit 11 clears the result; readers `00386079`, `00320E10`, `00390AB0` | agrees |
| `07-Combat-Action/how-an-action-gathers-its-targets.md` | bits 1, 21, 24, 25 in the target gather | agrees |
| `07-Combat-Action/how-close-a-unit-must-stand-to-act.md` | bit 26 = the weapon's reach | agrees |
| `04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md`, the `00312170` paragraph (SWE2-EC7-95) | "bit 8 set unless `& 0x2000`, bit 9 unless `& 0x4000`" | routed-to-FRONTIER: the `cmove` pair at `0031221E`–`00312232` sets them iff bits 13 / 14 are set (`FABLE-REQ-FRONTIER-UQ107-EC7-AND-RESULT-KINDS`) |
| `07-Combat-Action/Result-Record/the-result-record-field-map.md` | the `+0x04` kinds; no `+0x10` row | routed-to-FRONTIER in the same request: kinds 7 and 8 are written (`00390EF2`, `003910A5`, `00390E35`), and `00390E42` writes `+0x10` |

Grep of `0x8000221B`, `002F868F`, `002F849A`, `00312170`, "not the action row's" and the members table name across the
database, 2026-09-27.
