# Affected-consumer check: UQ-80 measured by a maintained instrument; the action row's +0x28 row set corrected (FABLE, Claude Opus 5.5, 2026-09-27)

affected: 02-Resource-And-Asset-Pipeline/authored-data-table-registry.md (the UQ-80 box), 07-Combat-Action/Action-Definition-Row/the-action-definition-row.md (field-map row +0x28)
run: uq80_coverage.py at fcc1e1d73 (worktree = that HEAD plus this package): 23 tables, 15 fully mapped, residue 8 tables / 60 bytes, FAILS 0 (coverage_run.txt). The +0x28 row set was re-read from us battle_pack.bin: 26 rows with a non-zero byte, ids 0xD0-0xE5, 0xE7, 0xEA, 0xED, 0xF1, named through the action-name map in 08-Combat-Formula/Recipe-System/recipe-users.tsv.

| consumer | what it said | state |
|---|---|---|
| `02-Resource-And-Asset-Pipeline/authored-data-table-registry.md`, UQ-80 box | "Still open: a file name is not a field map ... Whatever row meaning no page reads ... stays open" | revised-here: a dated note names the instrument and its counted residue; the box stays open |
| `07-Combat-Action/Action-Definition-Row/the-action-definition-row.md`, field map `+0x28` | "`120`–`153` on the 26 Esper attacks" | revised-here (FABLE's own line): struck; the 26 rows are the 18 Quickenings and the 8 Concurrences |
| same page, `+0x38` and `+0x30` | menu position / reader not found | agrees: FABLE's bt4a publish added the +0x30 reader; this record adds the +0x38 grid builder 00237FC0 to the manifest, not to the page |
| `00-Engine-Core-Runtime/the-encoded-id-space-and-the-query-record.md` line 355 | price_data non-1 values "from 30 to 11,160" | routed (FABLE-REQ-FRONTIER-UQ80-ROUTED-CONTRADICTIONS): the data gives 15..999,999 over 83 rows |
| `04-Actor-Entity/Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md` line 129 | the registry "records its 456-byte rows" for 02EBF130 | routed (same request): the registry gives chr_data 40 x 128 |
| `_types/fields.tsv` LicenseNodeRecord | "the whole record ... is honestly empty" | routed (same request) to the type-store owner: pages map +2, +4, +6 |
| _index/OPEN-QUESTIONS.md UQ-80 | PARTIAL | revised-here: narrowed; still PARTIAL; class-1 disposition asked of FRONTIER |

Regenerated with it: coverage.tsv, coverage_run.txt (new).
