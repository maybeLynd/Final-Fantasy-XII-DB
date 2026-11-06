---
title: "Identifier spaces: the kinds of id, handle and index the engine passes between subsystems, with each kind's range, invalid values, maker, resolver and reuse"
kind: "reference"
category: "Engine core"
addresses: "0x003589B0, 0x003588B0, 0x0031B7E0, 0x002E9810, 0x002E97C0, 0x002DF980, 0x002DF960, 0x0036A000, 0x003B38B0, 0x0051CC30, 0x00377190, 0x00377360, 0x0035B2F0, 0x0020E620, 0x0020E600, 0x00309440, 0x003008A0, 0x0030F760, 0x002F9860, 0x002F9920, 0x003214B0, 0x00264D60, 0x0031B9F0, 0x00252E60, 0x00252F40, 0x00247510, 0x00254B50, 0x00280A00, 0x002621D0, 0x003DC240, 0x00197160, 0x003A1180, 0x0021B5B0, 0x0032A8A0, 0x0032A930, 0x00269F40, 0x00263990, 0x00328990, 0x00322C50, 0x00387730, 0x0030E360"
---

## What it lists

[`identifier-spaces.tsv`](identifier-spaces.tsv) holds 146 kinds of identifier, the handles, ids and indexes that cross subsystems. Each row
gives the identifier's form (its bit fields), its range, the values that name nothing, the function that makes it,
the function that turns it back into the thing it names, and what happens to an old value when its slot is used again.

The identifiers fall into six families:

| Family | Rows | Old values after reuse |
|---|---|---|
| Checked handles: a slot plus a stamp, serial or generation that the resolver compares | actor, battle unit, model binding, effect ticket, bone trail, scene element, fade record, presentation command, vibration, arena, sound driver, sound play handle | stop resolving: the resolver sees the changed stamp and returns null or 0 |
| Plain indices and fixed ids | resource kind and id, encoded item id, action id, field id, text id, bank and row word, item picture id, script text id, party seat, member selector, inventory list id, bound id, widget message id, menu request id, script call id, control code, story flag id, name id, license node number, status id, quest id, achievement entry, achievement descriptor, movie id, shop number, fade layer, request slot, action availability index, standard motion id, time-stop request id, license board index, locale id, weather slot, actor group, add-motion table selector, area id, augment id, battle command row, battle message id, bestiary entry, binding button, character light bit, common effect index, debug menu command, effect element type, element, enemy group, equipment class, equipment slot, field effect number, font colour table index, formula recipe, formula slot, gauge colour index, gauge type, ground type, HUD hide bit, keycap index, magick school, menu lock kind, Phyre modifier code, movement kind, movement lock number, music track, render command code, request channel, save slot, scenario number, script opcode, settings slot, shape string number, text control code, title image, tutorial key, vibration pattern, weapon motion class, wind preset, arena number, battle logic word, bone physics deny bit, effect signal number, target class, bone id | name the same thing for the whole run; out-of-range values are refused, clamped or read past, as each row says |
| Encoded pointers | encoded pointer | the low 32 bits of an address; the base at `0x01F83530` is 0 |
| Unchecked addresses and slot numbers | loot pickup, sound id | no check: a reused pickup element or block registry record answers to an old handle or id |
| Handles nothing looks up | movement entry | harmless: no instruction resolves or compares the handle |
| Numbers read against what is bound now: a slot, row or group with no stamp, looked up in the slot, area, map pack or script bound at the time | voice cue word, message window slot, message macro number, script effect slot, puppet slot, map override group, map model group, map animation slot, ACTL record id, manager camera entry, camera shot row, camera shake row, blur sprite, effect anchor index, step point, skip entry, entrance index, destination index, map exit group, script actor ordinal, map sound index, collision group, background NPC id, battle voice group, effect trigger number, enemy definition row, enemy class row, event script number, field sign record, highlight rectangle, LGT2 light id, light group, map effect channel, map sound emitter, navigation icon entry, order set id, party list index, picture slot, roster slot, scene number, script data reference, script manager slot, script motion slot, standard motion lane, system message number, window picture part, event sound entry | name what is bound now: after a rebind the same number names the new holder, as each row says |

### Ids readers confuse

- **An actor handle is not a battle unit.** `0x003589B0` makes the handle from the actor record. `0x003588B0` turns it
  back into the actor, and `0x0031B7E0` goes one step further to the actor's unit, and only while `0x02089340` bit `0x10`
  is set.
- **A target class is not an actor group.** The class is the low nibble of actor byte `+0x0E` that
  setfreetargettype writes (`0x00269FE0`), and showtargettype and hidetargettype compare it whole
  (`0x0026DDB4`-`0x0026DDBB`). The group verbs compare the group `0x00263BE0` computes from it: nibbles 1, 2 and 7
  give group 0, nibble 3 gives group 2, and every other nibble gives group 1.
- **A party seat is not a member.** A seat (0 to 8, in one of five slot maps) holds a member selector. The selector
  is the row of the party table and of the forty member records.
- **An encoded item id is not a list position.** The id's nibble picks a class (`0x00309440`: nibble + 5). The menus
  page through the twelve derived inventory lists instead, which `0x00252E60` fills when an owned count goes from 0
  to non-zero.
- **A binding handle is not a bound id.** The bound id (letter class and number) names a model for
  the whole run. The binding handle names one of the 128 binding entries and stops working when that entry is
  retired.
- **A text id has two forms.** `0x002F9860` reads `group × 1000 + row`, while `0x002F9920` searches the rows for a row's
  own id under `group × 10000`. The two agree only where a file numbers its rows from `group × 10000` in order.

## Columns

| Column | Meaning |
|---|---|
| `id_kind` | the row's name |
| `form` | the identifier's bit fields or composition |
| `range` | the values that can name something |
| `invalid` | the values that name nothing, and what the resolver returns for them |
| `made_by` | the function or source that produces the identifier |
| `resolved_by` | the function that turns it into the thing it names |
| `reuse` | what happens to an old value when its slot is used again |
| `page` | the page that explains the identifier, by its path in the database |

## Related

- [Item and ability ids](item-and-ability-ids.md): the encoded id and its classes
- [Battle units](../Characters-And-Objects/battle-units.md): the actor handle
- [Script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md): binding handles and bound ids
- [Party slots](../Party/party-slots.md): seats and selectors
- [Native limits](native-limits.md): the counts behind the ranges

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Actor entity: `0x002621D0` calls `0x00358940`; `0x00263990` is called by `0x0025C230`, `0x0025C830`, `0x00268D10`, `0x00272CB0`,
  `0x00272CE0`; `0x00263BE0` is called by `0x0035A7A0`, `0x0035A990`, `0x0046BAC0`; `0x00269FE0` calls `0x00268EA0`; `0x00269FE0` is
  called by `0x00238BF0`; `0x002DF980` is called by `0x0032FCA0`; `0x002E97C0` is called by `0x0037B4D0`; `0x002E9810` is called
  by `0x0037B4D0`; `0x0030E360` calls `0x00300FC0`.
- Actor entity: `0x0030F760` calls `0x00236820`, `0x00236850`; `0x0031B7E0` calls `0x00263E30`, `0x003588B0`; `0x00322C50` is called
  by `0x002367A0`, `0x0023A570`, `0x0031B810`, `0x003266C0`, `0x00329CC0`; `0x003589B0` is called by `0x00234480`, `0x0025C230`,
  `0x0025C830`, `0x00268650`, `0x00268D10`, `0x0037B4D0`, `0x003B6F80`.
- Actor entity: those functions are documented on [frame update order](frame-update-order.md),
  [time stop and freeze](time-stop-and-freeze.md), [ps2 cpu emulation](ps2-cpu-emulation.md),
  [npc names](../Characters-And-Objects/npc-names.md),
  [battle unit construction](../Characters-And-Objects/battle-unit-construction.md).
- Actor entity: and on [battle verbs](../Scripts-And-Script-Commands/battle-verbs.md),
  [target selection](../Battle-Actions/target-selection.md),
  [script requests](../Scripts-And-Script-Commands/script-requests.md),
  [script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md).
- Actor entity: and on [party verbs](../Scripts-And-Script-Commands/party-verbs.md),
  [party control modes](party-control-modes.md), [force fight mode](force-fight-mode.md),
  [party data](../Party/party-data.md),
  [party during scenes](../Scripts-And-Script-Commands/party-during-scenes.md).
- Audio: `0x0021B5B0` calls `0x00212950`, `0x00224540`; `0x0021B5B0` is called by `0x00210C00`; `0x003A1180` is called by
  `0x00271500`; those functions are documented on [sound effects](../Sound-And-Music/sound-effects.md),
  [audio manager](../Sound-And-Music/audio-manager.md).
- Combat AI: `0x0030F760` is called by `0x00305AB0`, `0x00305CC0`; `0x0031B7E0` is called by `0x00301AD0`; `0x00322C50` is called
  by `0x00301AD0`, `0x003215C0`, `0x00321630`, `0x00321770`, `0x00321850`, `0x003219D0`, `0x00321B00`, `0x00321E40`, `0x00327A10`,
  `0x00327CB0`.
- Combat AI: those functions are documented on [battle verbs](../Scripts-And-Script-Commands/battle-verbs.md),
  [glossary](glossary.md), [spawn record fields](../Enemy-Spawning/spawn-record-fields.md),
  [battle units](../Characters-And-Objects/battle-units.md), [frame update order](frame-update-order.md).
- Combat AI: and on [enmity](../Enemy-AI-And-Gambits/enmity.md), [gambit screen](../Menus-And-HUD/gambit-screen.md),
  [item and ability ids](item-and-ability-ids.md).
- Combat action: `0x003008A0` is called by `0x00300280`, `0x0030EF20`; `0x0030E360` calls `0x0030B8E0`, `0x0030B9B0`; `0x0030E360`
  is called by `0x002FDDA0`, `0x00304850`, `0x0030EB10`; `0x0030F760` calls `0x0030AB40`, `0x003105D0`; `0x0030F760` is called by
  `0x0030FA00`, `0x00312FA0`.
- Combat action: `0x0031B7E0` is called by `0x002FE660`, `0x002FFB60`, `0x00304850`, `0x00305110`, `0x00305230`, `0x00305430`,
  `0x003082F0`, `0x00309990`, `0x0030A250`, `0x0030C010`, `0x0030C970`, `0x0030CBE0`; `0x0031B7E0` is also called by `0x0030D160`,
  `0x0030DB70`, `0x0030EEA0`, `0x0030F760`, `0x00310780`, `0x00311B20`, `0x00312FA0`, `0x00313120`, `0x00313CD0`, `0x00313DB0`.
- Combat action: `0x00322C50` is called by `0x002FFCF0`, `0x003060E0`, `0x00309300`, `0x003093D0`, `0x0030CBE0`, `0x0030DB70`,
  `0x0031A7B0`; `0x003589B0` is called by `0x00319F50`, `0x00325260`.
- Combat action: those functions are documented on [enemy ai](../Enemy-AI-And-Gambits/enemy-ai.md),
  [action phases](../Battle-Actions/action-phases.md), [hp and ko](../Damage-And-Battle-Formulas/hp-and-ko.md),
  [action results](../Battle-Actions/action-results.md),
  [binmenu images](../Game-Files-And-Data-Tables/binmenu-images.md).
- Combat action: and on [battle units](../Characters-And-Objects/battle-units.md),
  [quickenings and summons](../Battle-Actions/quickenings-and-summons.md),
  [battle verbs](../Scripts-And-Script-Commands/battle-verbs.md), [frame update order](frame-update-order.md),
  [force fight mode](force-fight-mode.md).
- Combat action: and on [menu map files](../Game-Files-And-Data-Tables/menu-map-files.md),
  [command availability](../Battle-Actions/command-availability.md),
  [action definition row](../Battle-Actions/action-definition-row.md), [call signatures](call-signatures.md).
- Combat action: and on [bestiary](../Enemy-Spawning/bestiary.md),
  [zone changes and mapjump](../World-Areas-And-Travel/zone-changes-and-mapjump.md),
  [reward verbs](../Scripts-And-Script-Commands/reward-verbs.md).
- Combat formula: `0x003008A0` is called by `0x003112F0`; `0x0030E360` calls `0x003112F0`, `0x0031B860`, `0x00386A50`, `0x00386A70`;
  `0x0030E360` is called by `0x00300530`, `0x003112F0`; `0x0031B9F0` is called by `0x00320AB0`; `0x00322C50` is called by
  `0x002FEF30`; `0x00387730` is called by `0x00387BB0`, `0x0038FCE0`; `0x003A1180` is called by `0x003112F0`.
- Combat formula: those functions are documented on [traps](../World-Areas-And-Travel/traps.md),
  [save and teleport crystals](../World-Areas-And-Travel/save-and-teleport-crystals.md),
  [action results](../Battle-Actions/action-results.md), [subsystem update flags](subsystem-update-flags.md),
  [force fight mode](force-fight-mode.md); and on [loot drops](../Rewards-EXP-Gil-And-Loot/loot-drops.md).
- Gameplay: `0x00309440` is called by `0x0031C5D0`, `0x00322C50`; `0x0030E360` calls `0x00307D10`, `0x003299B0`; `0x0030F760` calls
  `0x00316CD0`, `0x00316CF0`; `0x0031B7E0` is called by `0x0030BB30`, `0x00312B40`, `0x0031ADB0`, `0x00339630`; `0x0031B9F0` calls
  `0x00322C50`; `0x00322C50` is called by `0x0031B9F0`, `0x0031C5D0`; `0x00328990` calls `0x0031C5D0`; `0x003589B0` is called by
  `0x0031ADB0`.
- Gameplay: those functions are documented on [item and ability ids](item-and-ability-ids.md),
  [force fight mode](force-fight-mode.md), [enemy spawning](../Enemy-Spawning/enemy-spawning.md),
  [native limits](native-limits.md), [battle verbs](../Scripts-And-Script-Commands/battle-verbs.md).
- Gameplay: and on [action definition row](../Battle-Actions/action-definition-row.md),
  [spawn record fields](../Enemy-Spawning/spawn-record-fields.md),
  [bestiary](../Enemy-Spawning/bestiary.md),
  [battle locomotion](../Movement-And-Pathfinding/battle-locomotion.md); and on
  [party member status record](../Characters-And-Objects/party-member-status-record.md).
- Input: `0x00197160` calls `0x00196480`, `0x0079D1D0`, `0x0079E650`, `0x0079E6A0`, `0x0079E6D0`; `0x00197160` is called by
  `0x00196FF0`; `0x00254B50` is called by `0x00253C70`, `0x002E09A0`; `0x00263BE0` is called by `0x00226BE0`; `0x0032A8A0` is called
  by `0x00253C70`; `0x0035B2F0` is called by `0x0035B650`.
- Input: those functions are documented on [controls](../Controls-And-Input/controls.md),
  [frame update order](frame-update-order.md), [force fight mode](force-fight-mode.md),
  [time stop and freeze](time-stop-and-freeze.md), [jump thunks](jump-thunks.md).
- Items equipment shops license: `0x00252E60` is called by `0x00325F40`; `0x003008A0` calls `0x00309F30`; `0x003008A0` is called
  by `0x002FD530`, `0x002FD640`, `0x002FD780`, `0x002FEEB0`, `0x00300B80`, `0x00300BA0`, `0x0030B180`, `0x0030C410`, `0x0030F9A0`,
  `0x0030FAA0`, `0x0030FBE0`, `0x00310870`.
- Items equipment shops license: `0x00322C50` is called by `0x003096F0`, `0x0030B180`, `0x0030B4B0`, `0x0030B510`, `0x0030B570`,
  `0x0030B630`, `0x00317930`, `0x0031A510`, `0x00323910`, `0x00323C60`, `0x00323D10`, `0x00323EC0`; `0x00322C50` is also called by
  `0x00325F40`.
- Items equipment shops license: those functions are documented on [item and ability ids](item-and-ability-ids.md),
  [bazaar](../Items-Equipment-Shops-And-Licenses/bazaar.md),
  [party verbs](../Scripts-And-Script-Commands/party-verbs.md),
  [reward verbs](../Scripts-And-Script-Commands/reward-verbs.md), [stats](../Damage-And-Battle-Formulas/stats.md).
- Items equipment shops license: and on [party data](../Party/party-data.md),
  [party table](../Party/party-table.md), [battle verbs](../Scripts-And-Script-Commands/battle-verbs.md),
  [quickening and esper list](../Battle-Actions/quickening-and-esper-list.md),
  [command availability](../Battle-Actions/command-availability.md).
- Movement: `0x0031B7E0` is called by `0x00312730`, `0x00336710`, `0x00337A50`, `0x00338140`; `0x00322C50` is called by
  `0x0031BAC0`, `0x00326BB0`; `0x003589B0` is called by `0x002E5610`, `0x002EBFA0`.
- Movement: those functions are documented on
  [spawn record fields](../Enemy-Spawning/spawn-record-fields.md),
  [force fight mode](force-fight-mode.md), [battle locomotion](../Movement-And-Pathfinding/battle-locomotion.md),
  [game over](../World-Areas-And-Travel/game-over.md), [party data](../Party/party-data.md).
- Movement: and on
  [heading speed to position delta](../Movement-And-Pathfinding/heading-speed-to-position-delta.md),
  [world lock](../Scripts-And-Script-Commands/world-lock.md).
- Party: `0x0030F760` calls `0x0031B7E0`; `0x00322C50` is called by `0x003170E0`, `0x0031AC00`, `0x0031B510`, `0x00320800`,
  `0x00321100`, `0x00326500`, `0x003287A0`, `0x00328DB0`, `0x00329080`; `0x00328990` is called by `0x00328BD0`; `0x003589B0` is called
  by `0x00269C70`, `0x00326500`, `0x00353530`, `0x0050C610`, `0x0050D2F0`.
- Party: those functions are documented on [battle verbs](../Scripts-And-Script-Commands/battle-verbs.md),
  [party verbs](../Scripts-And-Script-Commands/party-verbs.md), [party data](../Party/party-data.md),
  [party control modes](party-control-modes.md), [player movement](../Movement-And-Pathfinding/player-movement.md).
- Presentation: `0x00247510` is called by `0x002D2DB0`, `0x00579420`; `0x00263990` is called by `0x002B0280`; `0x002DF980` is
  called by `0x001BB2B0`; `0x002F9920` is called by `0x0037E5B0`, `0x0037E8D0`; `0x0030F760` calls `0x00313B30`; `0x003589B0` is
  called by `0x003A4290`, `0x003A56F0`, `0x00465120`, `0x00465690`, `0x00506700`; `0x0036A000` is called by `0x003DD4C0`.
- Presentation: `0x00377190` is called by `0x00463FF0`, `0x00464B30`, `0x00464F20`, `0x0047BE20`; `0x00377360` is called by
  `0x00464050`, `0x00464B80`, `0x00465120`, `0x0047BF70`; `0x003A1180` is called by `0x0046CC70`; `0x003B38B0` calls `0x003EDAD0`;
  `0x0051CC30` is called by `0x003E6770`.
- Presentation: those functions are documented on [menu lists](../Menus-And-HUD/menu-lists.md),
  [quest menu files](../Game-Files-And-Data-Tables/quest-menu-files.md),
  [handbook files](../Game-Files-And-Data-Tables/handbook-files.md),
  [file size tables fst](../Game-Files-And-Data-Tables/file-size-tables-fst.md).
- Presentation: and on [battle verbs](../Scripts-And-Script-Commands/battle-verbs.md),
  [authored expressions](../Game-Files-And-Data-Tables/authored-expressions.md),
  [effect element runtime](../Graphics/effect-element-runtime.md).
- Presentation: and on [effect element types](../Graphics/effect-element-types.md),
  [battle numbers](../Menus-And-HUD/battle-numbers.md),
  [script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md),
  [character se tables chse](../Game-Files-And-Data-Tables/character-se-tables-chse.md).
- Presentation: and on [startup constants](startup-constants.md),
  [bone trails](../Graphics/bone-trails.md).
- Resource: `0x002DF960` is called by `0x00409FE0`; `0x002DF980` is called by `0x001DA290`, `0x002EEEE0`; `0x003B38B0` is called
  by `0x00409FE0`; those functions are documented on
  [resource ownership and disposal](../Game-Files-And-Data-Tables/resource-ownership-and-disposal.md),
  [debug logging](debug-logging.md), [debug menu](debug-menu.md).
- Rewards progression economy: `0x0030E360` calls `0x00312280`; `0x003A1180` is called by `0x0030C650`; those functions are
  documented on [area flags navimapdata](../World-Areas-And-Travel/area-flags-navimapdata.md),
  [battle verbs](../Scripts-And-Script-Commands/battle-verbs.md).
- Save load settings: `0x00247510` is called by `0x0057E950`, `0x0057EBB0`, `0x00580840`, `0x005819F0`, `0x00581B70`, `0x00582860`;
  `0x0032A8A0` calls `0x002EF2B0`; `0x0032A8A0` is called by `0x00583D60`; `0x0032A930` calls `0x002EF2B0`.
- Save load settings: those functions are documented on
  [saving and loading](../Saving-Loading-And-Settings/saving-and-loading.md), [game application](game-application.md),
  [script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md),
  [strong and weak mode](../Rewards-EXP-Gil-And-Loot/strong-and-weak-mode.md).
- Script VM: `0x002621D0` calls `0x003DC240`, `0x003DC270`, `0x003DC2A0`; `0x002621D0` is called by `0x0025E4C0`; `0x00264D60` is
  called by `0x00348DF0`, `0x0034ADA0`, `0x00352A50`, `0x00352EC0`, `0x003534F0`, `0x003545B0`, `0x00354F20`, `0x003555F0`,
  `0x00356B70`, `0x0050EAB0`; `0x00269F40` is called by `0x0034B9A0`, `0x0034C170`; `0x00269FE0` is called by `0x003528C0`.
- Script VM: `0x002E97C0` is called by `0x003409F0`, `0x00341840`, `0x003418B0`, `0x00342640`, `0x00344200`, `0x00344550`,
  `0x00345A60`, `0x003463F0`, `0x00354A40`, `0x00355210`; `0x002E9810` is called by `0x0033F330`, `0x003409F0`, `0x003414A0`,
  `0x003418B0`, `0x00343A30`, `0x00343B00`, `0x00344200`, `0x00344F00`, `0x00354400`, `0x00354A40`; `0x0032A8A0` is called by
  `0x0034E0B0`; `0x0032A930` is called by `0x0034E980`.
- Script VM: `0x003589B0` is called by `0x00342150`, `0x00342D40`, `0x003438F0`, `0x00349C90`, `0x0034B5D0`, `0x0034BB80`,
  `0x00352270`, `0x00352940`, `0x00354F20`, `0x003555F0`, `0x00357620`, `0x0050C7A0`; `0x0036A000` is called by `0x0050DEB0`;
  `0x003A1180` is called by `0x00357040`; `0x003DC240` is called by `0x002621D0`.
- Script VM: those functions are documented on [native commands](../Scripts-And-Script-Commands/native-commands.md),
  [script interpreter](../Scripts-And-Script-Commands/script-interpreter.md),
  [archades scenes](../Story-Events-And-Hunts/archades-scenes.md),
  [archades scripts](../Story-Events-And-Hunts/archades-scripts.md).
- Script VM: and on [ebp text sections](../EBP-Script-Files/ebp-text-sections.md),
  [npc names](../Characters-And-Objects/npc-names.md), [battle units](../Characters-And-Objects/battle-units.md),
  [script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md).
- Script VM: and on [reward verbs](../Scripts-And-Script-Commands/reward-verbs.md),
  [effect anchors and targets](../Graphics/effect-anchors-and-targets.md),
  [actor record](../Characters-And-Objects/actor-record.md), [sound effects](../Sound-And-Music/sound-effects.md).
- Status periodic terminal: `0x0030E360` calls `0x00300140`, `0x00301140`, `0x0030E360`, `0x0030FED0`, `0x003876D0`, `0x00387730`;
  `0x0030E360` is called by `0x0030E360`, `0x0030E990`, `0x0030EAE0`, `0x0030F690`, `0x0030FED0`; `0x00322C50` is called by
  `0x0030E130`, `0x0030FED0`, `0x00310DB0`; `0x00387730` is called by `0x0030E360`.
- Status periodic terminal: those functions are documented on [frame update order](frame-update-order.md),
  [battle verbs](../Scripts-And-Script-Commands/battle-verbs.md), [force fight mode](force-fight-mode.md),
  [item and ability ids](item-and-ability-ids.md), [status changes](../Status-Effects-And-KO/status-changes.md).
- Status periodic terminal: and on [battle units](../Characters-And-Objects/battle-units.md),
  [save and teleport crystals](../World-Areas-And-Travel/save-and-teleport-crystals.md).
- Story event quest hunt: `0x00263990` calls `0x0032A930`; `0x0032A8A0` calls `0x00377970`; those functions are documented on
  [npc names](../Characters-And-Objects/npc-names.md), [menu map files](../Game-Files-And-Data-Tables/menu-map-files.md).
- UI: `0x00247510` is called by `0x00252030`, `0x002C59D0`, `0x003EEEC0`, `0x00557B90`, `0x00561390`, `0x0056B4D0`, `0x0056E140`,
  `0x0056F810`; `0x00252F40` is called by `0x0057CF20`, `0x0057D620`; `0x00254B50` calls `0x00280A00`, `0x0028F970`, `0x0035D080`,
  `0x0035D660`, `0x0035D980`, `0x003C87B0`, `0x003C8990`; `0x00254B50` is called by `0x00254B40`; `0x00263990` is called by
  `0x002AC5F0`; `0x00280A00` calls `0x0028E860`.
- UI: `0x00280A00` is called by `0x00254B50`; `0x002F9920` is called by `0x003BE950`; `0x0031B7E0` is called by `0x0031EB20`;
  `0x00322C50` is called by `0x0031EB20`; `0x0032A8A0` is called by `0x00281AE0`, `0x0029C530`.
- UI: those functions are documented on [battle text tables](../Game-Files-And-Data-Tables/battle-text-tables.md),
  [controls](../Controls-And-Input/controls.md), [game over](../World-Areas-And-Travel/game-over.md),
  [license board screen](../Menus-And-HUD/license-board-screen.md).
- UI: and on [ps2data bin families](../Game-Files-And-Data-Tables/ps2data-bin-families.md),
  [gambit screen](../Menus-And-HUD/gambit-screen.md), [inventory screen](../Menus-And-HUD/inventory-screen.md),
  [text handbook unrequested](../Menus-And-HUD/text-handbook-unrequested.md),
  [item and ability ids](item-and-ability-ids.md).
- UI: and on [menu screens](../Menus-And-HUD/menu-screens.md), [battle menu](../Menus-And-HUD/battle-menu.md),
  [action availability](../Controls-And-Input/action-availability.md), [augments](../Damage-And-Battle-Formulas/augments.md),
  [menu map files](../Game-Files-And-Data-Tables/menu-map-files.md).
- UI: and on [action definition row](../Battle-Actions/action-definition-row.md),
  [binmenu images](../Game-Files-And-Data-Tables/binmenu-images.md),
  [zone asset list](../World-Areas-And-Travel/zone-asset-list.md).
- World area: `0x002DF980` is called by `0x00379A10`; `0x002F9920` is called by `0x003C0450`, `0x00576A50`; `0x0030E360` calls
  `0x00377C20`; `0x0030F760` calls `0x00377C20`.
- World area: those functions are documented on
  [standard file formats](../Game-Files-And-Data-Tables/standard-file-formats.md),
  [menu map files](../Game-Files-And-Data-Tables/menu-map-files.md),
  [handbook files](../Game-Files-And-Data-Tables/handbook-files.md), [force fight mode](force-fight-mode.md).
