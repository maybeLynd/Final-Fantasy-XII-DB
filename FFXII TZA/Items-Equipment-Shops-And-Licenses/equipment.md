---
title: "Equipment: the five slots, what can be worn where, two-handed weapons, shields and ammunition, Optimise, and what happens when you equip"
kind: "system"
category: "Items, equipment, shops and licenses"
addresses: "0x0031A630, 0x0031A510, 0x0031A410, 0x00317930, 0x00318B40, 0x002F7EC0, 0x002F9F20, 0x002F7A10, 0x002F7C80, 0x0030FBE0, 0x0030FAA0"
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

A member record holds five `u16` equipment ids at `+0x50`-`+0x59`, slot 0 main hand to slot 4 accessory, `0xFFFF`
for empty ([Unit stats fields](../Damage-And-Battle-Formulas/unit-stats-fields.md)). Which slot an item fits is its
row's `+0x07` bits 7-5 ([Equipment row](equipment-row.md)). An empty main hand is always refilled with Unarmed,
`0x1000`.

### The setters

| Setter | Record | Eligibility free-copy test | Worn counts | Unit refresh | Sites |
|---|---|---|---|---|---|
| `0x0031A630(record, slot, id, update)` | given | when `update` | when `update` | when `update` | `0x0031A630`-`0x0031A6ED` |
| `0x0031A510(mappedId, slot, id, flags)` | by party seat, `[0x02EBF190] + 0x5A7E` | always | always | always | `0x0031A510`-`0x0031A60C` |
| `0x0031A410(index, slot, id)` | by record index | always | always | always | `0x0031A410`-`0x0031A4DF` |

Each setter, for an id other than `0xFFFF`, first asks the eligibility test, below. It then moves one worn copy
from the old item to the new (`0x0030F9A0`, `0x0030C410`, [Inventory](inventory.md)), stores the id, and reconciles the
hands with `0x00318B40`. When the slot it set has changed, it rebuilds the stats with `0x0030FED0(record, 0x97)` and
refreshes the unit (`0x00324470`). Only that slot is compared (`0x0031A6BB`, `0x0031A4B2`, `0x0031A5DA`).

`0x0031A510` also
re-records the fighting units and reloads their models (`0x00324380`) unless `flags` bit `0x1` is set (`0x0031A5F5`-`0x0031A610`);
the five-slot callers `0x0031A710` and `0x0031A300` pass bit `0x1` and do that once at the end.

The worn counts are kept only while the member is in the party: joining adds an owned and a worn copy of every
piece, and leaving removes them ([Party members](../Party/party-members.md)). So the starting gear and the
scenario presets set the slots with `update` 0.

### Who equips

| Feature | Path | Sites |
|---|---|---|
| the equip menu, one slot | `0x003FFA20` → `0x0031A510(member, slot, id, 1)` | `0x003FFA4F` |
| the equip menu, Optimise | `0x002F9F20`, then `0x0031A710(member, out, 1)` | `0x003FF839`, `0x003FF84D` |
| the equip menu's Optimise preview: builds the loadout without equipping it | `0x002F9F20`, then `0x003FEAD0`, stored at `0x02B5F210` | `0x003FE81C`-`0x003FE82E` |
| the equip menu, remove all | `0x0031A300(member, 1)` | `0x003FF87F` |
| equipping a piece just bought in a shop | `0x0031A510` | `0x0057AF18` |
| `takeaway_item_and_equip` `0x388`, `giveback_item_and_equip` `0x387` | `0x0031A300`, `0x0031A710` | `0x0030FC2F`, `0x0030FBA0` |
| `takeoff_equip` `0x55B`: the given id taken off each of the nine party records that wears it and holds a main character (byte `+4` 6 or less, `0x0030FD6E`; byte `+5` 0, `0x0030FD68`), except members who are down outside a town (`0x0030FD40`-`0x0030FD89`) | `0x0031A630(record, slot, 0xFFFF, 1)` | `0x0030FDC8` |
| `resetJobs` `0x5D6` ([Licenses](licenses.md)) | `0x0031A260` → `0x0031A410` | `0x00328C11` |
| the scenario presets and the party record set-up | `0x0031A630(…, 0)` | `0x00239C6F`-`0x00239CBF`, `0x0023AE99`-`0x0023AEE9` |
| the enemy record set-up: slot 0 from the enemy row's `+0x16`, slot 1 from `+0x1C`, slots 2-4 empty | `0x0031A630(…, 0)` | `0x0023ADB5`-`0x0023ADFA` |

No battle action calls a setter, and ammunition is never used up: the battle's item reservation takes only item
actions ([Using an item](item-use.md)).

### The equip screen

The equip pane `0x003FF360` shows the member's five slots, the list of pieces for the chosen slot and the stat
rows:

- `0x003FF1F0`, the slot row painter (`0x003FF648`), shows the name of the piece in slot i (`[0x0209AC30] + 0xD48 +
  0x20 x i`) with its icon; in the Optimise preview (`+0x178` = `0x402`) a slot whose preview id at
  `0x02B5F210` differs shows that piece in colour 5, and an empty one shows text `0x3EA` in colour 4.
- `0x003FE490`, the stat row painter that `0x003FE5D0` installs (`0x003FE69C`), shows row i's name (text `0x4A90` + i),
  the current value `+0xC8` and, when the new value `+0xEC` differs, the new one in colour 5 when it is at
  least the current and 4 when it is lower.
- `0x003FF040(pane, slot)` empties a slot: in mode `0x400` it hands over to `0x003FDA20`; otherwise, when the slot
  holds something other than empty or Unarmed (`0x1000`), it removes the piece (`0x003FFA20(slot, 0xFFFF)`),
  refreshes the list (`0x003FF920`) and returns 0.
- `0x003FCEE0()` returns the widest description line (`0x00292B70`, `0x002B3050`) over the equipment in inventory
  lists 1 to 4, for sizing the help window.
- `0x003FCDE0(pane)`, run by `0x003FCD20`, hides every member mark and shows those of the nine party records that
  `0x00282FA0` passes, one spacing apart.

The list marks a piece through `0x0027F030`: bit `0x1` when `0x00317B70` refuses it, and bit `0x4` for an ammunition
mismatch. The helpers:

- `0x002CCA10(class)` answers whether a class is an ammunition weapon, 7, 8, 9 or 17; `0x002CCA00` whether it is
  ammunition, 23 to 26; `0x002CCA30` whether it is a shield, 18.
- `0x002CA430(id)` gives a weapon's ammunition class from its class: 7 gives 23, 8 gives 24, 9 gives 25, 17
  gives 26 and any other 0.
- `0x002CCA40(ammo, current)` answers whether inventory list 4 holds a piece of that ammunition class that is
  the one in the off hand (`current`, slot 1 at `[0x0209AC30] + 0xD68`) or owned in a count above 0.

### Can it be worn

`0x00317930(record, loadout, slot, id, freeCopy)` returns 1 or 0 (`0x00317930`-`0x00317AE5`), testing in order:

1. The slot must be 0-4 (`0x0031794A`).
2. The id in the slot's entry of `0x00D107E8`, Unarmed for slot 0 and empty for slots 1-4, is accepted at once
   (`0x00317953`-`0x00317960`); an empty slot 0 is refused (`0x0031797E`-`0x00317984`).
3. The id must be a valid equipment id (`0x0031798B`-`0x003179A5`).
4. With `freeCopy`, at least one copy must be owned and not worn (`0x003179A7`-`0x003179BB`).
5. The row's slot bits must equal the slot (`0x00317A18`-`0x00317A21`).
6. For the off hand, unless the item is a shield, class 18, or the main hand is empty, the main hand's `+0x11` must
   equal the item's class (`0x00317A27`-`0x00317A82`).
7. A null record or an enemy record passes here (`0x00317A84`-`0x00317A8F`).
8. The party row's dword `+0x00`, a mask of forbidden classes, must not hold the item's class; it is 0 on every
   shipped row (`0x00317A91`-`0x00317AD6`).
9. The license test `0x00323C60` decides (`0x00317AD8`-`0x00317AE5`, [Licenses](licenses.md)).

Taking something off always succeeds: every setter skips the test for `0xFFFF`, and the test itself accepts an
empty slot 1-4. The free-copy test runs before the old copy is released (`0x0031A677`, `0x0031A69B`), so re-equipping the
item already worn needs a spare copy.

### The two hands

`0x00318B40(slots, slotJustSet, update)` runs after every store (`0x00318B40`-`0x00318C79`):

1. An empty main hand becomes Unarmed (`0x00318B73`-`0x00318B8E`).
2. It compares the main hand's `+0x11` with the off hand's class, `0xFF` for an empty off hand; on a match it is
   done (`0x00318BE0`-`0x00318C31`). A two-handed weapon, `+0x11` of -1, with an empty off hand matches.
3. On a mismatch after setting the off hand: a shield turns the main hand into Unarmed, and so does an emptied off
   hand under a weapon that does not take a shield, a bow, crossbow, gun or hand-bomb (`0x00318C33`-`0x00318C5E`).
4. On any other mismatch the off hand is emptied (`0x00318C64`-`0x00318C79`).

| Action | Result |
|---|---|
| a two-handed weapon equipped while a shield is worn | the shield is dropped |
| a bow equipped over a shield or the wrong ammunition | the off hand is emptied; no ammunition is put in |
| a shield equipped under a two-handed or ammunition weapon | allowed; the weapon becomes Unarmed |
| ammunition equipped under the wrong weapon | refused by the eligibility test |
| ammunition removed from under its weapon | the weapon becomes Unarmed |

Every pairing test reads the main hand's `+0x11` and the off hand's `+0x09`; the off hand's own `+0x11` is never
read (`0x002F7F70`-`0x002F7F76`, `0x00317A7B`-`0x00317A7F`, `0x00318BE0`).

### Takeaway and giveback

`takeaway_item_and_equip` `0x388`, through `0x0030FBE0`, works on every record of party seats 0-8 except guests,
party rows 7-25 (`0x0030FBF3`-`0x0030FC14`):

1. It copies the five slot words to the record's `+0x5A`-`+0x63` (`0x0030FC1F`-`0x0030FC29`).
2. It removes all gear with `0x0031A300(seat, 1)` (`0x0030FC2F`).
3. It backs up the counts of items `0x0000`-`0x003F` and equipment `0x1000`-`0x11A3` and sets them to 0
   ([Inventory](inventory.md); `0x0030FC47`-`0x0030FCEF`); the placeholder rows above `0x11A3` are left alone.

`giveback_item_and_equip` `0x387`, through `0x0030FAA0`, adds the counts back, re-equips the five stashed words
through `0x0031A710`, which tests each again, and clears the count backup (`0x0030FAAD`-`0x0030FBC7`). It does not clear
`+0x5A`-`+0x63`.

### Optimise

`0x002F9F20(seat, out)` builds the loadout (`0x002F9F20`-`0x002FA092`):

1. It starts from the five worn words (`0x002F9F8D`-`0x002F9FB4`).
2. For slots 0-3 it walks a range of ids, `0x1000`-`0x10C7` for slot 0, `0x10C8`-`0x11A3` for slot 1,
   `0x10DC`-`0x1117` for slot 2 and `0x1118`-`0x1153` for slot 3 (tables `0x00D0F9C0`, `0x00D0F9D0`). The accessory,
   slot 4, is never walked.
3. A candidate must pass the eligibility test with the free-copy test (`0x00317B20`), and for the off hand
   `0x002F7EC0` against the chosen main hand (`0x002F9FF1`-`0x002FA01A`).
4. `0x002F7A10` keeps the better of the current choice and the candidate (`0x002FA01C`-`0x002FA03C`).
5. After slot 0, an empty main hand becomes Unarmed and an off hand that no longer pairs is emptied
   (`0x002FA056`-`0x002FA077`).

`0x002F7A10` ranks by slot:

| Slot | First | Then |
|---|---|---|
| weapon, and ammunition | `0x002F7C80`: Attack Power `+0x1A`; for a bow, crossbow, gun or hand-bomb, plus the best usable ammunition's `+0x1A`, or -1 when there is none | the live weapon, then the live weapon's class, then the lower class |
| shield | evade `+0x18` | magick evade `+0x19` |
| helm | Magick Resist `+0x19` | Defense `+0x18` |
| armor | Defense `+0x18` | Magick Resist `+0x19` |

A final tie goes to the larger `+0x06`, then the higher id (`0x002F7C3C`-`0x002F7C56`). A worn piece stays unless an
eligible one beats it.

## Shipped data

The starting gear of party rows 0-6, set by the record set-up from the party row's words `+0x0A`-`+0x12`:

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

- [Equipment row](equipment-row.md) - the slot bits, the class and `+0x11`.
- [Inventory](inventory.md) - the worn counts.
- [Licenses](licenses.md) - the equipment license test.
- [Stats](../Damage-And-Battle-Formulas/stats.md) - what the rebuild adds.
- [Party members](../Party/party-members.md) - gear counted on joining and leaving.
