# Affected-consumer check: HM-1 narrowed; the secondary-context census's "no located writer" corrected (FABLE, Claude Opus 5.5, 2026-09-26)

**Control:** `hm1_model_selectors.py` beside this file (5 checks, FAILS 0).

The census said the secondary-context bytes `+0x14C`/`+0x14D`/`+0x14E` had "no located writer". Each has one:
- `+0x14C`/`+0x14D`: the setter `002E6090`. Its only call, in the secondary-context initialiser, passes (1, 0).
- `+0x14E`: the actor-record initialiser, which sets it to 1.

The census's own reader columns stand. The high-model key getters `002657E0`/`00263FC0` read the same two bytes and
were not in them.

| consumer | what it said | state |
|---|---|---|
| `04-Actor-Entity/Actor-Contexts/the-movement-and-secondary-context-censuses.md`, the named-fields note | "`+0x14C`/`+0x14D`/`+0x14E` stay UNRESOLVED … with no located writer" | revised-here (struck; the writers and the two names beside it) |
| same page, census rows `+0x14C`, `+0x14D`, `+0x14E` | writes `0` | revised-here (dated cell notes; the measured counts are kept as the census printed them) |
| `17-Presentation-Rendering/Model-And-Motion-Formats/add-motion-skeleton-and-high-model-tables.md` §7 | `HM-1` open: `b`/`c` undecoded, the 39 values unread, `0022A0B0` unread | revised-here (dated narrowing: `b`/`c`, their one writer, the values, the boot page) |
| same page, `SWE2-EC7-76` update (`002657E0` + `00263FC0` gated byte readers) | the two getters' reads and defaults | agrees (H1 re-reads them) |
| `00-Engine-Core-Runtime/what-the-engine-fixes-at-boot.md` | `0022A0B0` is the boot routine | agrees (cited as HM-1's fourth item) |
| `01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-verb-table.tsv` rows `208B`/`208C` | the two debug verbs' names and handlers | agrees (H2 reads them) |
| `_index/OPEN-QUESTIONS.md` HM-1 | OPEN | revised-here (NARROWED; the previous status kept as history) |
