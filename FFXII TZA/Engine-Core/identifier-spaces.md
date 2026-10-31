---
title: "Identifier spaces: the kinds of id, handle and index the engine passes between subsystems, with each kind's range, invalid values, maker, resolver and reuse"
kind: "reference"
category: "Engine core"
addresses: "0x003589B0, 0x003588B0, 0x0031B7E0, 0x002E9810, 0x002E97C0, 0x002DF980, 0x002DF960, 0x0036A000, 0x003B38B0, 0x0051CC30, 0x00377190, 0x00377360, 0x0035B2F0, 0x0020E620, 0x0020E600, 0x00309440, 0x003008A0, 0x0030F760, 0x002F9860, 0x002F9920, 0x003214B0, 0x00264D60, 0x0031B9F0, 0x00252E60, 0x00252F40, 0x00247510, 0x00254B50, 0x00280A00, 0x002621D0, 0x003DC240, 0x00197160, 0x003A1180, 0x0021B5B0, 0x0032A8A0, 0x0032A930, 0x00269F40, 0x00263990, 0x00328990, 0x00322C50, 0x00387730, 0x0030E360"
---

## What it lists

`identifier-spaces.tsv` holds 146 kinds of identifier, the handles, ids and indexes that cross subsystems. Each row
gives the identifier's form (its bit fields), its range, the values that name nothing, the function that makes it,
the function that turns it back into the thing it names, and what happens to an old value when its slot is used again.

The identifiers fall into six families:

| Family | Rows | Old values after reuse |
|---|---|---|
| Checked handles: a slot plus a stamp, serial or generation that the resolver compares | actor, model binding, effect ticket, bone trail, scene element, fade record, presentation command, vibration, arena, sound driver, sound play handle | stop resolving: the resolver sees the changed stamp and returns null or 0 |
| Plain indices and fixed ids | resource kind and id, encoded item id, action id, field id, text id, bank and row word, item picture id, script text id, party seat, member selector, inventory list id, bound model id, widget message id, menu request id, script call id, control code, persistent flag id, name id, license node number, status id, quest id, achievement entry, achievement descriptor, movie id, shop number, fade layer, request slot, action availability index, standard motion id, time-stop request id, license board index, locale id, weather slot, actor group, add-motion table selector, area id, augment id, battle command row, battle message id, bestiary entry, binding button, character light bit, common effect index, debug menu command, effect element type, element, enemy group, equipment class, equipment slot, field effect number, font colour table index, formula recipe, formula slot, gauge colour index, gauge type, ground type, HUD hide bit, keycap index, magick school, menu lock kind, Phyre modifier code, movement kind, movement lock number, music track, render command code, request channel, save slot, scenario number, script opcode, settings slot, shape string number, text control code, title image, tutorial key, vibration pattern, weapon motion class, wind preset, arena number, battle logic word, bone physics deny bit, effect signal number, target class, bone id | name the same thing for the whole run; out-of-range values are refused, clamped or read past, as each row says |
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
- **A model-binding handle is not a bound model id.** The bound id (letter class and number) names a model for
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
