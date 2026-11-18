[Home](../../README.md) / [Engine core](README.md) / Glossary

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Glossary: the database's words for engine objects, records, ids, handles, pools and files, each with the page that explains it | reference | Engine core | Glossary, ids and limits | 153 terms the pages use across subsystems: what the thing is in a sentence or two, the other names the pages give it, and the page and section that explain it in full; with the words that name more than one thing told apart. |  |

## What it lists

[`glossary.tsv`](glossary.tsv) holds 153 terms: engine objects, records, ids, handles, pools, file kinds and recurring words that
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
| actor class | mask `0xE0` of the actor's byte `+0x03` ([actor record](../Characters-And-Objects/actor-record.md#the-class-byte)); the low nibble of byte `+0x0E`, which `0x00263C20` returns, is a separate value, the actor class nibble ([actor record](../Characters-And-Objects/actor-record.md#the-class-byte), [HP and KO](../Damage-And-Battle-Formulas/hp-and-ko.md)) |
| keep | the keep banks of spawn records and a keep entry, one record in them ([spawn record fields](../Enemy-Spawning/spawn-record-fields.md)); the order flag `0x8000` ([enemy order sets](../Enemy-AI-And-Gambits/enemy-order-sets.md)); in community notes, the stats record ([unit stats fields](../Damage-And-Battle-Formulas/unit-stats-fields.md)) |
| selector | the member selector, a seat's low byte and the member's row of the party table ([party slots](../Party/party-slots.md#the-nine-seats)); the byte a file stream is opened with, which picks its log tag and its RAM cache stamp ([file path resolution](../Game-Files-And-Data-Tables/file-path-resolution.md), [prefetch manifests](../Game-Files-And-Data-Tables/prefetch-manifests.md)); the MWeather selector, the word of a field that picks its weather entries ([weather](../World-Areas-And-Travel/weather.md)); a sprite's palette selector ([UI typed lists](../Game-Files-And-Data-Tables/ui-typed-lists.md)); the steering slot selector byte `+0xDC` ([facing and steering](../Movement-And-Pathfinding/facing-and-steering.md)); a reward package selector, id `0xA000` + n ([reward selector list](../Rewards-EXP-Gil-And-Loot/reward-selector-list.md)); the gambit test function `0x00301AD0` ([gambits](../Enemy-AI-And-Gambits/gambits.md)); the byte after a `0x0F` escape in a string ([text codes](../Menus-And-HUD/text-codes.md)); the screen number a script posts with `openfullscreenmenu_48d` ([menus](../Menus-And-HUD/menus.md)); the selector argument of an event start, which picks its priority rule ([character render records](../Graphics/character-render-records.md)); the choice selectors ([presentation entries](../Graphics/presentation-entries.md#the-choice-selectors)) |
| registry slot | one of the 64 qword slots `0x02EBF008` to `0x02EBF200` that reach the authored data tables ([authored data tables](../Game-Files-And-Data-Tables/authored-data-tables.md)); the block registry slot of a sound block, which a sound id is built from ([sound banks](../Sound-And-Music/sound-banks.md#the-block-registry)); one of the 64 atlas registry slots at `0x0208F580` ([UI typed lists](../Game-Files-And-Data-Tables/ui-typed-lists.md)) |
| class byte | mask `0xE0` of an actor record's byte `+0x03`, the actor class ([actor record](../Characters-And-Objects/actor-record.md#the-class-byte)); the defeated battle unit's byte `+0x56`, the class row's type byte that the kill chain compares ([kill chain](../Rewards-EXP-Gil-And-Loot/kill-chain.md)); the equipment row's byte `+0x09`, which sets the item's group ([equipment row](../Items-Equipment-Shops-And-Licenses/equipment-row.md)); a sound record's byte `+4`, which picks a plain, random, ordered, cycling or switched sound ([sound variations](../Sound-And-Music/sound-variations.md)); a screen fade record's byte `+2`, which indexes the class enables at `0x02EC07E0` ([screen fades](../Graphics/screen-fades.md)) |
| member record | a member stats record, one of the forty in the party block ([unit stats fields](../Damage-And-Battle-Formulas/unit-stats-fields.md)); a Phyre reflection member record, one per data member of a class ([Phyre reflection](../PhyreEngine/phyre-reflection.md)); on the party list page, the `0xC0`-byte records at `0x022C8080` ([party list](../Menus-And-HUD/party-list.md)) |
| party record | a member stats record, a stats record of kind 0 in the party block ([unit stats fields](../Damage-And-Battle-Formulas/unit-stats-fields.md)); one of the nine `0xC0`-byte party member status records the menus build at `[0x0209AC30] + 0x408` ([party member status record](../Characters-And-Objects/party-member-status-record.md), [menu screens](../Menus-And-HUD/menu-screens.md)) |
| battle mode | the Battle Mode setting, Active or Wait ([game settings](../Saving-Loading-And-Settings/game-settings.md)); the battle mode register `0x022C83EC`, which can replace the Escape Mode toggle ([Escape Mode](../Controls-And-Input/escape.md)); the summon, chocobo, town and event-party level that `0x0030D9A0` returns is the party control mode ([party control modes](party-control-modes.md)) |

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

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Actor entity: `0x00263C20` is called by `0x00273750`, `0x00273A00`, `0x0046BAC0`; `0x00301AD0` calls `0x002367A0`, `0x00236820`,
  `0x00236850`, `0x0031B760`, `0x0031B770`, `0x0031B810`.
- Actor entity: those functions are documented on [battle units](../Characters-And-Objects/battle-units.md),
  [target selection](../Battle-Actions/target-selection.md),
  [party verbs](../Scripts-And-Script-Commands/party-verbs.md), [frame update order](frame-update-order.md),
  [force fight mode](force-fight-mode.md).
- Combat AI: `0x00301AD0` calls `0x00308C20`, `0x0030BD00`, `0x0031E6F0`, `0x0031E760`, `0x00321190`, `0x003215C0`, `0x00321630`;
  `0x00301AD0` is called by `0x003014C0`.
- Combat AI: those functions are documented on [gambit conditions](../Enemy-AI-And-Gambits/gambit-conditions.md),
  [enemy order sets](../Enemy-AI-And-Gambits/enemy-order-sets.md),
  [spawn record fields](../Enemy-Spawning/spawn-record-fields.md),
  [frame update order](frame-update-order.md).
- Combat action: `0x00263C20` is called by `0x0030AB40`; `0x00301AD0` calls `0x003093D0`, `0x0030AB40`, `0x0030B9B0`, `0x0031C500`.
- Combat action: those functions are documented on [battle verbs](../Scripts-And-Script-Commands/battle-verbs.md),
  [action definition row](../Battle-Actions/action-definition-row.md),
  [action results](../Battle-Actions/action-results.md),
  [target selection](../Battle-Actions/target-selection.md).
- Gameplay: `0x00301AD0` calls `0x00309EC0`, `0x00316CF0`, `0x0031EA90`, `0x00321320`, `0x00322C50`.
- Gameplay: those functions are documented on [item and ability ids](item-and-ability-ids.md),
  [battle verbs](../Scripts-And-Script-Commands/battle-verbs.md),
  [battle locomotion](../Movement-And-Pathfinding/battle-locomotion.md),
  [enemy order sets](../Enemy-AI-And-Gambits/enemy-order-sets.md), [identifier spaces](identifier-spaces.md).
- Movement: `0x00263C20` is called by `0x00335760`, `0x00338490`; those functions are documented on
  [battle locomotion](../Movement-And-Pathfinding/battle-locomotion.md),
  [bestiary](../Enemy-Spawning/bestiary.md).
- Party: `0x00301AD0` calls `0x0031B7E0`, `0x003272A0`, `0x003273B0`; those functions are documented on
  [identifier spaces](identifier-spaces.md), [reward verbs](../Scripts-And-Script-Commands/reward-verbs.md),
  [enemy spawning](../Enemy-Spawning/enemy-spawning.md).
- Presentation: `0x00301AD0` calls `0x00322360`; those functions are documented on
  [battle locomotion](../Movement-And-Pathfinding/battle-locomotion.md).
- UI: `0x00263C20` is called by `0x002734F0`, `0x0027D330`, `0x002BF0E0`, `0x002C7660`, `0x00322A80`, `0x003C5130`, `0x003C8B70`;
  those functions are documented on [widgets](../Menus-And-HUD/widgets.md), [hud](../Menus-And-HUD/hud.md),
  [battle units](../Characters-And-Objects/battle-units.md), [target selection](../Battle-Actions/target-selection.md),
  [action availability](../Controls-And-Input/action-availability.md).
- World area: `0x00301AD0` calls `0x00320940`, `0x00377C20`; those functions are documented on
  [enemy spawning](../Enemy-Spawning/enemy-spawning.md), [force fight mode](force-fight-mode.md).
