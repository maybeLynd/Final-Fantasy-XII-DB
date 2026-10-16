---
title: "Equipment: the five slots, what can be worn where, two-handed weapons, shields and ammunition, Optimise, and what happens when you equip"
kind: "system"
category: "Items, equipment, shops and licenses"
addresses: "0031A630, 0031A510, 0031A410, 00317930, 00318B40, 002F7EC0, 002F9F20, 002F7A10, 002F7C80, 0030FBE0, 0030FAA0"
---

## What the player sees

- Each character has five slots: weapon, off hand, head, body and accessory.
- A piece can be equipped only when a spare copy is owned and its license has been bought.
- Equipping a two-handed weapon drops the shield; equipping a shield under a two-handed weapon or a bow leaves the
  character unarmed.
- A bow, crossbow, gun or hand-bomb needs its own ammunition; removing the ammunition also removes the weapon.
- Optimise picks the strongest weapon, off hand, helm and armor; it never changes the accessory.

## How it works

### The slot words

A member record holds five `u16` equipment ids at `+50`<sub>h</sub>-`+59`<sub>h</sub>, slot 0 main hand to slot 4 accessory, `FFFF`<sub>h</sub>
for empty ([Unit stats fields](../Damage-And-Battle-Formulas/unit-stats-fields.md)). Which slot an item fits is its
row's `+07`<sub>h</sub> bits 7-5 ([Equipment row](equipment-row.md)). An empty main hand is always refilled with Unarmed,
`1000`<sub>h</sub>.

### The setters

| Setter | Record | Eligibility free-copy test | Worn counts | Unit refresh | Sites |
|---|---|---|---|---|---|
| `0031A630(record, slot, id, update)` | given | when `update` | when `update` | when `update` | `0031A630`-`0031A6ED` |
| `0031A510(mappedId, slot, id, flags)` | by party seat, `[02EBF190] + 5A7Eh` | always | always | always | `0031A510`-`0031A60C` |
| `0031A410(index, slot, id)` | by record index | always | always | always | `0031A410`-`0031A4DF` |

Each setter, for an id other than `FFFF`<sub>h</sub>, first asks the eligibility test, below. It then moves one worn copy
from the old item to the new (`0030F9A0`, `0030C410`, [Inventory](inventory.md)), stores the id, and reconciles the
hands with `00318B40`. When the slot it set has changed, it rebuilds the stats with `0030FED0(record, 97h)` and
refreshes the unit (`00324470`). Only that slot is compared (`0031A6BB`, `0031A4B2`, `0031A5DA`).

`0031A510` also
re-records the fighting units and reloads their models (`00324380`) unless `flags` bit 0 is set (`0031A5F8`-`0031A606`);
the five-slot callers `0031A710` and `0031A300` pass bit 0 and do that once at the end.

The worn counts are kept only while the member is in the party: joining adds an owned and a worn copy of every
piece, and leaving removes them ([Party members](../Party/party-members.md)). So the starting gear and the
scenario presets set the slots with `update` 0.

### Who equips

| Feature | Path | Sites |
|---|---|---|
| the equip menu, one slot | `003FFA20` → `0031A510(member, slot, id, 1)` | `003FFA4F` |
| the equip menu, Optimise | `002F9F20`, then `0031A710(member, out, 1)` | `003FF839`, `003FF84D` |
| the equip menu's Optimise preview: builds the loadout without equipping it | `002F9F20`, then `003FEAD0`, stored at `02B5F210` | `003FE81C`-`003FE82E` |
| the equip menu, remove all | `0031A300(member, 1)` | `003FF87F` |
| equipping a piece just bought in a shop | `0031A510` | `0057AF18` |
| `takeaway_item_and_equip` `388`<sub>h</sub>, `giveback_item_and_equip` `387`<sub>h</sub> | `0031A300`, `0031A710` | `0030FC2F`, `0030FBA0` |
| `takeoff_equip` `55B`<sub>h</sub>: the given id taken off party rows 0-6 that wear it, except members who are down outside a town (`0030FD40`-`0030FD89`) | `0031A630(record, slot, FFFFh, 1)` | `0030FDC8` |
| `resetJobs` `5D6`<sub>h</sub> ([Licenses](licenses.md)) | `0031A260` → `0031A410` | `00328C11` |
| the scenario presets and the party record set-up | `0031A630(…, 0)` | `00239C6F`-`00239CBF`, `0023AE99`-`0023AEE9` |
| the enemy record set-up: slot 0 from the enemy row's `+16`<sub>h</sub>, slot 1 from `+1C`<sub>h</sub>, slots 2-4 empty | `0031A630(…, 0)` | `0023ADB5`-`0023ADFA` |

No battle action calls a setter, and ammunition is never used up: the battle's item reservation takes only item
actions ([Using an item](item-use.md)).

### Can it be worn

`00317930(record, loadout, slot, id, freeCopy)` returns 1 or 0 (`00317930`-`00317AE5`), testing in order:

1. The slot must be 0-4 (`0031794A`).
2. The id in the slot's entry of `00D107E8`, Unarmed for slot 0 and empty for slots 1-4, is accepted at once
   (`00317953`-`00317960`); an empty slot 0 is refused (`0031797E`-`00317984`).
3. The id must be a valid equipment id (`0031798B`-`003179A5`).
4. With `freeCopy`, at least one copy must be owned and not worn (`003179A7`-`003179BB`).
5. The row's slot bits must equal the slot (`00317A18`-`00317A21`).
6. For the off hand, unless the item is a shield, class 18, or the main hand is empty, the main hand's `+11`<sub>h</sub> must
   equal the item's class (`00317A27`-`00317A82`).
7. A null record or an enemy record passes here (`00317A84`-`00317A8F`).
8. The party row's dword `+00`<sub>h</sub>, a mask of forbidden classes, must not hold the item's class; it is 0 on every
   shipped row (`00317A91`-`00317AD6`).
9. The license test `00323C60` decides (`00317AD8`-`00317AE5`, [Licenses](licenses.md)).

Taking something off always succeeds: every setter skips the test for `FFFF`<sub>h</sub>, and the test itself accepts an
empty slot 1-4. The free-copy test runs before the old copy is released (`0031A677`, `0031A69B`), so re-equipping the
item already worn needs a spare copy.

### The two hands

`00318B40(slots, slotJustSet, update)` runs after every store (`00318B40`-`00318C79`):

1. An empty main hand becomes Unarmed (`00318B73`-`00318B8E`).
2. It compares the main hand's `+11`<sub>h</sub> with the off hand's class, `FF`<sub>h</sub> for an empty off hand; on a match it is
   done (`00318BE0`-`00318C31`). A two-handed weapon, `+11`<sub>h</sub> of -1, with an empty off hand matches.
3. On a mismatch after setting the off hand: a shield turns the main hand into Unarmed, and so does an emptied off
   hand under a weapon that does not take a shield, a bow, crossbow, gun or hand-bomb (`00318C33`-`00318C5E`).
4. On any other mismatch the off hand is emptied (`00318C64`-`00318C79`).

| Action | Result |
|---|---|
| a two-handed weapon equipped while a shield is worn | the shield is dropped |
| a bow equipped over a shield or the wrong ammunition | the off hand is emptied; no ammunition is put in |
| a shield equipped under a two-handed or ammunition weapon | allowed; the weapon becomes Unarmed |
| ammunition equipped under the wrong weapon | refused by the eligibility test |
| ammunition removed from under its weapon | the weapon becomes Unarmed |

Every pairing test reads the main hand's `+11`<sub>h</sub> and the off hand's `+09`<sub>h</sub>; the off hand's own `+11`<sub>h</sub> is never
read (`002F7F70`-`002F7F76`, `00317A7B`-`00317A7F`, `00318BE0`).

### Takeaway and giveback

`takeaway_item_and_equip` `388`<sub>h</sub>, through `0030FBE0`, works on every record of party seats 0-8 except guests,
party rows 7-25 (`0030FBF3`-`0030FC14`):

1. It copies the five slot words to the record's `+5A`<sub>h</sub>-`+63`<sub>h</sub> (`0030FC1F`-`0030FC29`).
2. It removes all gear with `0031A300(seat, 1)` (`0030FC2F`).
3. It backs up the counts of items `0000`<sub>h</sub>-`003F`<sub>h</sub> and equipment `1000`<sub>h</sub>-`11A3`<sub>h</sub> and sets them to 0
   ([Inventory](inventory.md); `0030FC47`-`0030FCEF`); the placeholder rows above `11A3`<sub>h</sub> are left alone.

`giveback_item_and_equip` `387`<sub>h</sub>, through `0030FAA0`, adds the counts back, re-equips the five stashed words
through `0031A710`, which tests each again, and clears the count backup (`0030FAAD`-`0030FBC7`). It does not clear
`+5A`<sub>h</sub>-`+63`<sub>h</sub>.

### Optimise

`002F9F20(seat, out)` builds the loadout (`002F9F20`-`002FA092`):

1. It starts from the five worn words (`002F9F8D`-`002F9FB4`).
2. For slots 0-3 it walks a range of ids, `1000`<sub>h</sub>-`10C7`<sub>h</sub> for slot 0, `10C8`<sub>h</sub>-`11A3`<sub>h</sub> for slot 1,
   `10DC`<sub>h</sub>-`1117`<sub>h</sub> for slot 2 and `1118`<sub>h</sub>-`1153`<sub>h</sub> for slot 3 (tables `00D0F9C0`, `00D0F9D0`). The accessory,
   slot 4, is never walked.
3. A candidate must pass the eligibility test with the free-copy test (`00317B20`), and for the off hand
   `002F7EC0` against the chosen main hand (`002F9FF1`-`002FA01A`).
4. `002F7A10` keeps the better of the current choice and the candidate (`002FA01C`-`002FA03C`).
5. After slot 0, an empty main hand becomes Unarmed and an off hand that no longer pairs is emptied
   (`002FA056`-`002FA077`).

`002F7A10` ranks by slot:

| Slot | First | Then |
|---|---|---|
| weapon, and ammunition | `002F7C80`: Attack Power `+1A`<sub>h</sub>; for a bow, crossbow, gun or hand-bomb, plus the best usable ammunition's `+1A`<sub>h</sub>, or -1 when there is none | the live weapon, then the live weapon's class, then the lower class |
| shield | evade `+18`<sub>h</sub> | magick evade `+19`<sub>h</sub> |
| helm | Magick Resist `+19`<sub>h</sub> | Defense `+18`<sub>h</sub> |
| armor | Defense `+18`<sub>h</sub> | Magick Resist `+19`<sub>h</sub> |

A final tie goes to the larger `+06`<sub>h</sub>, then the higher id (`002F7C3C`-`002F7C56`). A worn piece stays unless an
eligible one beats it.

## Shipped data

The starting gear of party rows 0-6, set by the record set-up from the party row's words `+0A`<sub>h</sub>-`+12`<sub>h</sub>:

| Row | Gear |
|---|---|
| 0 Vaan | Dagger, Leather Cap, Leather Clothing |
| 1 Ashe | Longsword, Buckler, Bronze Helm, Bronze Armor, Bangle |
| 2 Fran | Shortbow, Onion Arrows, Headgear, Chromed Leathers |
| 3 Balthier | Altair, Onion Shot, Headgear, Chromed Leathers |
| 4 Basch | Mythril Blade, Bronze Helm, Bronze Armor |
| 5 Penelo | Dagger, Cotton Cap, Cotton Shirt |
| 6 Reks | Mythril Sword, Buckler, Leather Cap, Leather Clothing |

## Modding notes

- Optimise never touches the accessory, and ranks weapons by Attack Power alone.
- A bow left without ammunition loses to Unarmed in Optimise, because its score is -1.
- To let a class wear a piece, the party row's class mask must leave its bit clear; every shipped mask is 0.

## Related

- [Equipment row](equipment-row.md) - the slot bits, the class and `+11`<sub>h</sub>.
- [Inventory](inventory.md) - the worn counts.
- [Licenses](licenses.md) - the equipment license test.
- [Stats](../Damage-And-Battle-Formulas/stats.md) - what the rebuild adds.
- [Party members](../Party/party-members.md) - gear counted on joining and leaving.
