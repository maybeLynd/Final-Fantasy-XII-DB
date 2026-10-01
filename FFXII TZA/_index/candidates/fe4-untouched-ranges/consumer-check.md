# Affected-consumer check: the stale stats-record `+0x05C` row (FABLE, Claude Opus 5.5, 2026-09-27)

affected: 08-Combat-Formula/Battle-Stats-Record/the-battle-stats-record-field-map.md (the field table's +0x05C row; the FE-4 / UQ-119 box)

run: fe4_ranges.py at 63e642d15 (worktree = that HEAD plus this record), 5 checks, FAILS 0. R2 is the check that
measures the correction.

**The change.** The field table's `+0x05C` row still says *"written and read only by
`BattleFormula_AdvanceStatusTimersAndBuildResult`"*. FE-3 (2026-09-13, FABLE, on OPUS's type correction) established
that its three accesses address the result record at `+0x5C + 4i`, not the stats record. The row is struck, with a
dated note pointing to FE-3.

| consumer | what it says | state |
|---|---|---|
| the field table's `+0x05C` row | "written and read only by `00386C70`" | revised-here (struck; dated note) |
| FE-3's box on the same page | no stats-record `+0x5C` access | agrees (it is the source) |
| the register's FE-3 row | the same | agrees |
| `_types/fields.tsv` `BattleStatsRecord 0x05C slotCounter5C` | a stats-record field compared against 1 | routed-to-OPUS (the type store's owner): `FABLE-REQ-OPUS-STATS-5C-TYPE-ROW-AND-S23B-GAP` |
| §2.3b's "every one of them sitting exactly where a compiler pads" (OPUS's section) | all five residual gaps are padding | routed-to-OPUS in the same request: `+0x60`–`+0x63` is not padding (see the FE-4 record) |
| `battle-stats-record-accesses.tsv` rows at disp `0x5C` | the census rows, marked `idx` | agrees as raw census output (they record the instruction, and the `idx` tag already flags the indexed form); not edited |
| `10-Status-Periodic-Terminal/CONTRACT-periodic-tick.md` | cites stats `+0xBC` and `+0x13C`, not `+0x5C` | agrees |
