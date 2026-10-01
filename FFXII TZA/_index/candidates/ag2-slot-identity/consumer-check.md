# Affected-consumer check: AG-2 answered, and the registry page's `00236C74` citation corrected (FABLE, Claude Opus 5.5, 2026-09-26)

## The correction

Section 2 of `authored-data-table-registry.md` has a note, added 2026-09-22 on
`OPUS-REQ-FABLE-REGISTRY-PAGE-IS-ONE-SLOT-SHORT`, which said that `00236C30`'s first store is
`mov qword ptr [0x02EBF008], rax` at `00236C74`, sourced from `+4`.

The bytes say otherwise. `00236C70 movsxd rax, dword ptr [rcx + 4]` / `00236C74 mov qword ptr [rip + …]` resolves to
`0x02EBF180`, the weapon-class map. `0x02EBF008` is bound from `+0x118` through the registrar: the lea is at `00237010` and
the field read at `00237017`.

The note's conclusion still stands. The origin is `0x02EBF008`, the end is `0x02EBF200`, and there are 64 slots. The
initialiser binds both bounds, but not as its first and last stores.

Regression: `ag2_slot_identity.py` C8 asserts both instructions.

| consumer | what it says | state |
|---|---|---|
| `02-Resource-And-Asset-Pipeline/authored-data-table-registry.md` section 2 note | "first is `[0x02EBF008]` at `00236C74` from `+4`" | revised-here (struck, dated correction beside it) |
| same page, the tail read (2026-09-11) | "`02EBF180` — the weapon-class map (directory `+4`) … stores this directory dword directly (`00236C70`–`00236C74`)" | agrees |
| same page, the evidence table's "Slot bounds" row | upper bound `0x02EBF1F8` | revised-here (dated note: `0x02EBF200` since the 2026-09-22 correction) |
| `02-Resource-And-Asset-Pipeline/CONTRACT-authored-table-row-lookup.md` section 7a | `+0x118` → `02EBF008` | agrees (C2 reproduces all 35 rows) |
| `_index/_inbox/repos-c9.md` (slot table) | slot 47 `02EBF180`, `+4`, direct store, `00236C74` | agrees |
| `00-Engine-Core-Runtime/the-encoded-id-space-and-the-query-record.md` row `02EBF008` | a clock-driven schedule | agrees with the join's `movie` (UQ-80 already read `movie` as the schedule table) |

## The AG-2 answer

| consumer | state |
|---|---|
| the registry page's AG-2 box | revised-here (ticked, answer beside it) |
| the registry page's frontmatter `status:` | revised-here (AG-2 answered; UQ-80 remains open) |
| `_index/OPEN-QUESTIONS.md` AG-2 | revised-here (ANSWERED; the previous status kept as history) |
| `_index/OPEN-QUESTIONS.md` UQ-80 (2026-09-15 narrowing) | agrees. It named pack-backed slots by file using the same join, and every name it gives matches a row of `ag2-slot-identity.tsv`: `chr_data`, `dougu_data`, `maho_data`, `waza_data`, `gambit_data`, the three `daiji` tables, `questreward_data`, `horidashi`, `mgccategory_data`, `license_data`, `ability_data`. |
| the page's 2026-09-07 named-reader census | agrees on the rows checked in C5 (loot = `drop`, MP gain from HP damage = `damagemp_data`, text banks = `word.bin`). Slot 7's label "status auxiliary / timer parameters" differs in wording from `ability_data`; it is recorded as a lead, not a contradiction, because both of its named readers compute charge and cost values. |

Nothing here was executed. The identity is static plus authored data: the image's manifest and the nine packs of the
extract.
