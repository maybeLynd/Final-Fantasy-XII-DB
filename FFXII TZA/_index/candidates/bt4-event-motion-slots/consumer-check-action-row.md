# Affected-consumer check: the action row's +0x30 reader, propagated from BT-4 (FABLE, Claude Opus 5.5, 2026-09-27)

affected: 07-Combat-Action/Action-Definition-Row/the-action-definition-row.md (the +0x30 row of the field map)
run: bt4_event_slots.py at c07423604 (worktree = that HEAD plus the BT-4 package), check P2 measures 0030A457 / 0030A46A as dword reads of [row + 0x30] in BattleAction_SelectPhasePresentationEvent, FAILS 0.

| consumer | what it said | state |
|---|---|---|
| `07-Combat-Action/Action-Definition-Row/the-action-definition-row.md`, field-map row `+0x30` | reader "—"; "an id-shaped word; reader not found" | revised-here: struck, reader named. It was applied only after FABLE's UQ-107 publish, because the page carried that package's staged hunks |
| same page, FABLE's 2026-09-18 narrowing (`+0x30` is a shared performance id on a hundreds grid) | the value names a shared performance | agrees; the reader returns it as the action's phase-9..11 presentation event, and the per-action `.ca` motion packs carry those numbers |
| `_index/OPEN-QUESTIONS.md` AY-2 (ANSWERED 2026-09-26) | "only +0x21 lacked a reader" | agrees in effect: `+0x30` now has one. The row's history had it reader-less as of 2026-09-18; no status change needed |

Regenerated with it: nothing.
