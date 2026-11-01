---
title: "Glossary: the database's words for engine objects, records, ids, handles, pools and files, each with the page that explains it"
kind: "reference"
category: "Engine core"
addresses: ""
---

## What it lists

`glossary.tsv` holds 150 terms: engine objects, records, ids, handles, pools, file kinds and recurring words that
several pages use. Each row says what the thing is, the other names the pages use for it, and the
page and section that explain it in full. Player-facing names (items, magicks, statuses) are in the reference tables
of their own pages, not here.

Community reverse-engineering notes and modding tools use other names for some of these. The first eight below are
also in the `also_called` column of the row they name, so that a search for one finds the page:

| Community name | Row |
|---|---|
| BUW, BattleUnitWork | battle unit |
| BUK, BattleUnitKeep | stats record |
| BUKPlus, BattleUnitKeepPlus | spawn record |
| BAW | actor record |
| ardUnit | enemy definition |
| ardClass | class row |
| section13 | equipment row |
| section 14 of the battle pack, `g_SecActions` | action row |
| the order flag names of The Insurgent's Toolkit (`noTimeout` and the others) | order set; the table of aliases is on [enemy order sets](../Enemy-AI-And-Gambits/enemy-order-sets.md) |

`btlKeepCharWork1` and `btlKeepCharWork2` are the executable's own labels for the two keep banks
([battle units](../Characters-And-Objects/battle-units.md)).

### Words that name more than one thing

Some words are used for different things on different pages. Where a word below has a row of its own, the row
gives the meaning on the page it links:

| Word | What it names, by page |
|---|---|
| arena | one of the fifteen numbered memory arenas ([resource arena and relocation](../Game-Files-And-Data-Tables/resource-arena-and-relocation.md)); the Gi command allocator at `[0x01F7F4C0]` ([Gi render commands](../Graphics/gi-render-commands.md#the-command-arena)); the GS-record arena at `[0x01FD4A78]` ([render command list](../Graphics/render-command-list.md)) |
| block | a piece of an arena, with its `0x40`-byte header ([resource arena and relocation](../Game-Files-And-Data-Tables/resource-arena-and-relocation.md)); a heap buffer that start-up turns into an arena ([startup constants](startup-constants.md)) |
| binding entry | one of the 128 model-binding entries ([script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md)); an actor's tag-table entry that `PUSHACT` reads ([verb dispatch](../Scripts-And-Script-Commands/verb-dispatch.md)) |
| draw list | the sorted effect records at `[0x02F8F2F8]` ([effect drawing](../Graphics/effect-drawing.md#the-draw-list)); a location-map page's icon records ([menu map files](../Game-Files-And-Data-Tables/menu-map-files.md#readers-of-sloc)); the list a character render object's slot 16 builds ([character render object](../Graphics/character-render-object.md#the-draw)) |
| text id | a menu or help string number ([battle text tables](../Game-Files-And-Data-Tables/battle-text-tables.md)); an entry of a script's text section, the script text id ([EBP text sections](../EBP-Script-Files/ebp-text-sections.md)) |
| resource entry | a `0x14`-byte entry of an actor's pool at `+0xA0` ([actor record](../Characters-And-Objects/actor-record.md)); a row in a bank of a table descriptor ([resource sections](../Game-Files-And-Data-Tables/resource-sections.md)); a `0x50`-byte entry of the render resource root ([character render records](../Graphics/character-render-records.md)) |
| kind byte | the stats record's byte `+0x05`, 0 party and 1 enemy ([battle unit construction](../Characters-And-Objects/battle-unit-construction.md#the-kind-byte-and-the-type-partition)); the action row's byte `+0x1E` ([action definition row](../Battle-Actions/action-definition-row.md#the-kind-byte)); the steering byte `+0x2A` ([facing and steering](../Movement-And-Pathfinding/facing-and-steering.md)) |
| target list | the action's target list, the units an action affects, at unit `+0x778` ([area of effect](../Battle-Actions/area-of-effect.md)); the menu's target list, the battle menu's choosable targets ([target selection](../Battle-Actions/target-selection.md)); the field target cycle list, handles at `0x022C83F0` ([controls](../Controls-And-Input/controls.md)) |
| ordinal | a record's position in its manager's pool ([actor record](../Characters-And-Objects/actor-record.md)); the number that adds a letter to an enemy's name ([battle unit construction](../Characters-And-Objects/battle-unit-construction.md)) |
| control code | an input code of 1 to 152 ([controls](../Controls-And-Input/controls.md)); a code inside a string is a text code, a control byte or an escape ([text codes](../Menus-And-HUD/text-codes.md)) |
| emitter | the middle level of a running effect ([effect element runtime](../Graphics/effect-element-runtime.md)); the point, line and polygon submit functions ([effect element types](../Graphics/effect-element-types.md)); a character's sound emitter ([animation sounds](../Sound-And-Music/animation-sounds.md)); a map sound emitter ([map sounds](../Sound-And-Music/map-sounds.md)) |
| actor class | bits 5 to 7 of the actor's byte `+0x03` ([actor record](../Characters-And-Objects/actor-record.md#the-class-byte)); the nibble of byte `+0x0E` that `0x00263C20` returns ([HP and KO](../Damage-And-Battle-Formulas/hp-and-ko.md)) |
| keep | the keep banks of spawn records and a keep entry, one record in them ([spawn record fields](../Enemy-Spawning/spawn-record-fields.md)); the order flag `0x8000` ([enemy order sets](../Enemy-AI-And-Gambits/enemy-order-sets.md)); in community notes, the stats record ([unit stats fields](../Damage-And-Battle-Formulas/unit-stats-fields.md)) |

## Columns

| Column | Meaning |
|---|---|
| `term` | the term as the pages use it |
| `meaning` | what the thing is |
| `also_called` | other names the pages use for the same thing, and the names community notes and tools give it |
| `page` | the page that explains it in full, by its path in the database |
| `section` | the section of that page, as a link anchor, or empty for the whole page |

## Related

- [Identifier spaces](identifier-spaces.md): every kind of id and handle, with its range and resolver.
- [Native limits](native-limits.md): the engine's fixed limits.
