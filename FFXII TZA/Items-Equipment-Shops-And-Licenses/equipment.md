[Home](../../README.md) / [Items, equipment, shops and licenses](README.md) / Equipment

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Equipment: the five slots, what can be worn where, two-handed weapons, shields and ammunition, Optimise, and what happens when you equip | system | Items, equipment, shops and licenses | Equipment | How equipping works: the five slot words of a member record, the setters and when they move the worn counts and rebuild the stats, the eligibility test and its order (slot, free copy, pairing, license), why taking something off always succeeds, how the off hand and the main hand are reconciled for shields, two-handed weapons and ammunition, the takeaway and giveback verbs and the stashed loadout, the Optimise builder and its rules per slot, and the starting gear. | 0x0031A630, 0x0031A510, 0x0031A410, 0x00317930, 0x00318B40, 0x002F7EC0, 0x002F9F20, 0x002F7A10, 0x002F7C80, 0x0030FBE0, 0x0030FAA0 |

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
row's `+0x07` bits under mask `0xE0` ([Equipment row](equipment-row.md)). An empty main hand is always refilled with Unarmed,
`0x1000`.

### The setters

| Setter | Record | Eligibility free-copy test | Worn counts | Unit refresh | Sites |
|---|---|---|---|---|---|
| `0x0031A630(record, slot, id, update)` | given | when `update` | when `update` | when `update` | `0x0031A630`-`0x0031A6ED` |
| `0x0031A510(mappedId, slot, id, flags)` | by party seat, `[0x02EBF190] + 0x5A7E` | always | always | when `0x0031B860` finds a unit (`0x0031A5F5`-`0x0031A602`) | `0x0031A510`-`0x0031A60C` |
| `0x0031A410(index, slot, id)` | by record index | always | always | when `0x0031B860` finds a unit (`0x0031A4D2`-`0x0031A4DF`) | `0x0031A410`-`0x0031A4DF` |

Each setter, for an id other than `0xFFFF`, first asks the eligibility test, below. It then moves one worn copy
from the old item to the new (`0x0030F9A0`, `0x0030C410`, [Inventory](inventory.md)), stores the id, and reconciles the
hands with `0x00318B40`. When the slot it set has changed, it rebuilds the stats with `0x0030FED0(record, 0x97)` and
refreshes the unit¹. Only that slot is compared².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00324470` |
| ² | `0x0031A6BB`, `0x0031A4B2`, `0x0031A5DA` |

</details>

`0x0031A630` returns -1 for a null record¹ and for an id the eligibility test refuses², and
0 otherwise³. The rebuild runs whatever `update` is⁴; the unit refresh needs `update` and a
unit that `0x0031B860` finds for the record⁵. The test is `0x00317930(record, record + 0x50,
slot, id, update)`⁶.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0031A64E` |
| ² | `0x0031A67E` |
| ³ | `0x0031A6F2` |
| ⁴ | `0x0031A6D4` |
| ⁵ | `0x0031A6D9`-`0x0031A6ED` |
| ⁶ | `0x0031A668`-`0x0031A677` |

</details>

`0x0031A410` and `0x0031A510` return -1 for a record index or seat byte above `0x27` and for an id the eligibility
test refuses, and 0 otherwise¹. `0x0031A510`
also returns -1 for a seat that `0x00322C50(0x17, seat)` refuses, any seat outside 0-8².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0031A427`, `0x0031A476`, `0x0031A4E4`; `0x0031A55F`, `0x0031A5A3`, `0x0031A611` |
| ² | `0x0031A53C`-`0x0031A547` |

</details>

Both test with the free-copy test¹ and give `0x00318B40` an `update` of 1². Their unit refresh, like that of `0x0031A630`, needs a unit that `0x0031B860` finds³. `0x0031A510` calls `0x00324380` with `flags` bit `0x1` clear even when
the slot did not change⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0031A45D`, `0x0031A58A` |
| ² | `0x0031A4A4`, `0x0031A5CC` |
| ³ | `0x0031A4CF`-`0x0031A4DF`, `0x0031A5F2`-`0x0031A602` |
| ⁴ | `0x0031A607`-`0x0031A60C` |

</details>

`0x0031A510` also
re-records the fighting units and reloads their models¹ unless `flags` bit `0x1` is set²;
the five-slot callers `0x0031A710` and `0x0031A300` pass bit `0x1`³ and do that once at the end
only when their own `flags` bit `0x1` is clear and at least one slot was set⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00324380` |
| ² | `0x0031A5F5`-`0x0031A610` |
| ³ | `0x0031A740`, `0x0031A34D` |
| ⁴ | `0x0031A772`-`0x0031A780`, `0x0031A382`-`0x0031A3E0` |

</details>

All four of their call sites set that bit¹; the takeaway and giveback
verbs call `0x00324380` themselves after their loops².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003FF848`, `0x003FF87D`, `0x0030FB98`, `0x0030FC1A` |
| ² | `0x0030FC3B`, `0x0030FBAC` |

</details>

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
| `takeoff_equip` `0x55B`: the given id taken off each of the nine party records that wears it and holds a main character (byte `+4` 6 or less, `0x0030FD6E`; byte `+5` 0, `0x0030FD68`), except members with KO, Stone or X-Zone (`0x80000003` of stats `+0x3C` or `+0x64`) outside a town (`0x00377C20`; `0x0030FD40`-`0x0030FD89`) | `0x0031A630(record, slot, 0xFFFF, 1)` | `0x0030FDC8` |
| `resetJobs` `0x5D6` ([Licenses](licenses.md)) | `0x0031A260` → `0x0031A410` | `0x00328C11` |
| the scenario presets and the party record set-up | `0x0031A630(…, 0)` | `0x00239C6F`-`0x00239CBF`, `0x0023AE99`-`0x0023AEE9` |
| the enemy record set-up: slot 0 from the enemy row's `+0x16`, slot 1 from `+0x1C`, slots 2-4 empty | `0x0031A630(…, 0)` | `0x0023ADB5`-`0x0023ADFA` |

The set-up sites of the last two rows are in the record initialiser `0x0023AC80`, apart from `0x00239960`'s own. It first
clears the `0x1C8`-byte record and empties its five slots¹, then takes the kind from bits 8-15
of `edx`², returns 0 while the dword `0x02089300` is 0³, and runs the
party sites for kind 0 and the enemy sites for kind 1, returning 0 for any other kind⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0023ACA4`-`0x0023ACD0` |
| ² | `0x0023ACA1`, `0x0023ACB2` |
| ³ | `0x0023ACE4`-`0x0023ACEE` |
| ⁴ | `0x0023ACF7`-`0x0023ACFA`, `0x0023AD9F`-`0x0023ADA2` |

</details>

`0x0023AC80` is called with kind 0 for each of the 40 records by the battle reset `0x00237DF0`¹ and by the
scenario presets' function `0x00239960` for a valid pending preset, before its own sites², and with kind 1
by the spawn installer `0x0023A570`, for a unit with flag bit `0x4000000` whose row checks pass, once `0x00236100` gives
it a spawn record whose flag bits `0x5` are clear³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00237E26` |
| ² | `0x00239AC4` |
| ³ | `0x0023A641`-`0x0023A79D`, `0x0023A7A9` |

</details>

No battle action calls a setter, and ammunition is never used up: the battle's item reservation takes only item
actions ([Using an item](item-use.md)).

### The equip screen

The equip pane `0x003FF360` shows the member's five slots, the list of pieces for the chosen slot and the stat
rows:

- `0x003FF1F0`, the slot row painter¹, shows the name of the piece in slot i (`[0x0209AC30] + 0xD48 +
  0x20 x i`) with its icon; in the Optimise preview (`+0x178` = `0x402`) a slot whose preview id at
  `0x02B5F210` differs shows that piece in colour 5, and an empty one shows text `0x3EA` in colour 4.
- `0x003FE490`, the stat row painter that `0x003FE5D0` installs², shows row i's name (text `0x4A90` + i),
  the current value `+0xC8` and, when the new value `+0xEC` differs, the new one in colour 5 when it is at
  least the current and 4 when it is lower.
- `0x003FF040(pane, slot)` empties a slot: in mode `0x400` it hands over to `0x003FDA20`; otherwise, when the slot
  holds something other than empty or Unarmed (`0x1000`), it removes the piece (`0x003FFA20(slot, 0xFFFF)`),
  refreshes the list³ and returns 0.
- `0x003FCEE0()` returns the widest description line⁴ over the equipment in inventory
  lists 1 to 4, for sizing the help window.
- `0x003FCDE0(pane)`, run by `0x003FCD20`, hides every member mark and shows those of the nine party records that
  `0x00282FA0` passes, one spacing apart.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003FF648` |
| ² | `0x003FE69C` |
| ³ | `0x003FF920` |
| ⁴ | `0x00292B70`, `0x002B3050` |

</details>

The list marks a piece through `0x0027F030`: bit `0x1` when `0x00317B70` refuses it, and bit `0x4` for an ammunition
mismatch. The helpers:

- `0x002CCA10(class)` answers whether a class is an ammunition weapon, 7, 8, 9 or 17; `0x002CCA00` whether it is
  ammunition, 23 to 26; `0x002CCA30` whether it is a shield, 18.
- `0x002CA430(id)` gives a weapon's ammunition class from its class: 7 gives 23, 8 gives 24, 9 gives 25, 17
  gives 26 and any other 0.
- `0x002CCA40(ammo, current)` answers whether inventory list 4 holds a piece of that ammunition class that is
  the one in the off hand (`current`, slot 1 at `[0x0209AC30] + 0xD68`) or owned in a count above 0.

### Can it be worn

`0x00317930(record, loadout, slot, id, freeCopy)` returns 1 or 0¹, testing in order:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00317930`-`0x00317AE5` |

</details>

| Step | What happens | Where in the code |
|---|---|---|
| 1 | The slot must be 0-4. | `0x0031794A` |
| 2 | The id in the slot's entry of `0x00D107E8`, Unarmed for slot 0 and empty for slots 1-4, is accepted at once; an empty slot 0 is refused. | `0x00317953`-`0x00317960`<br>`0x0031797E`-`0x00317984` |
| 3 | The id must be a valid equipment id. | `0x0031798B`-`0x003179A5` |
| 4 | With `freeCopy`, at least one copy must be owned and not worn. | `0x003179A7`-`0x003179BB` |
| 5 | The row's slot bits must equal the slot. | `0x00317A18`-`0x00317A21` |
| 6 | For the off hand, unless the item is a shield, class 18, or the main hand is empty, the main hand's `+0x11` must equal the item's class. | `0x00317A27`-`0x00317A82` |
| 7 | A null record or an enemy record passes here. | `0x00317A84`-`0x00317A8F` |
| 8 | The party row's dword `+0x00`, a mask of forbidden classes, must not hold the item's class; it is 0 on every shipped row. | `0x00317A91`-`0x00317AD6` |
| 9 | The license test `0x00323C60` decides (`0x00317AD8`-`0x00317AE5`, [Licenses](licenses.md)). |   |

Taking something off always succeeds: every setter skips the test for `0xFFFF`, and the test itself accepts an
empty slot 1-4. The free-copy test runs before the old copy is released¹, so re-equipping the
item already worn needs a spare copy.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0031A677`, `0x0031A69B` |

</details>

Equipping draws on three other parts of the game. The piece's row says which slot it fits and which weapon it pairs
with, the inventory must hold a copy nobody is wearing, and a main character must own a License Board square that
grants it. When the slot changes, the game rebuilds the character's stats.

The slot check `0x0031794A` belongs to the eligibility test, so `0x0031A510` stores `0xFFFF` without it: `0x0031A584`
jumps past `0x00317930` to the read of the slot's old word¹. Every caller that stores `0xFFFF` through
`0x0031A510` gives a slot from 0 to 4:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0031A5A5` |

</details>

- The equip pane taking a piece off: `0x003FF040(pane, slot)` calls `0x003FFA20(slot, 0xFFFF)`¹,
  and `0x003FFA20` hands the slot to `0x0031A510`². The slot is the argument of the command
  `0x8001` the pane receives³: 1 when the pane sends it to itself⁴,
  otherwise the item its grid confirmed.
- The pane's grid `+0x170` sends only an item below its count `+0xE8`⁵, and the pane sets
  that count to 5⁶. The pane decodes record 3 of layout unit 7 as its parent
 ⁷, and that record's one grid node is item 5, this grid.
- That item is never below 0. It is `+0xED` + (`+0xF2` + `+0xF4`) × `+0xEC` + `+0xEE`⁸,
  passed as the command's argument⁹. The grid's build sets all four fields to 0¹⁰.
- The cursor code `0x002D0A20`, `0x002D1DB0`, `0x002D4B70` and `0x002D4D60` keeps those fields at 0 or above on this
  one-column grid of 5 items, sized by its layout item¹¹. `0x002D1B10` runs only for flag
  `0x800000` of `+0xE0`¹², which no writer sets on this grid.
- The equipment list `0x003FDFE0` emptying a slot: it calls `0x003FFA20` with its byte `+0x17E` and the chosen row's id,
  with no check `0x003FCA70` when that id is `0xFFFF`¹³. `0x003FD368` is the one write of
  `+0x17E` to the list; it stores the list's build argument¹⁴, which `0x003FDA20` takes from
  `0x003FF040`'s slot¹⁵.
- The shop's member picker: `0x0057AF18` gives the picker's byte `+0xC6`, byte `+0x4C` of `0x0035D380(6, item)`
 ¹⁶, whose one write is `0x0057ACD7`. For `0xFFFF` the class-6 test `0x00322C50` refuses the id,
  the 557 equipment ids being `0x1000`-`0x122C`, so `0x0035D380` clears the record and the slot is 0
 ¹⁷.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003FF0F8`-`0x003FF0FC` |
| ² | `0x003FFA49`-`0x003FFA4F` |
| ³ | `0x003FF6EA`-`0x003FF765` |
| ⁴ | `0x003FF7C3`-`0x003FF7E1` |
| ⁵ | `0x002D40B8`-`0x002D40FF` |
| ⁶ | `0x003FF628`-`0x003FF63C` |
| ⁷ | `0x003FF5AB`-`0x003FF5D5` |
| ⁸ | `0x002D40B8`-`0x002D40E9` |
| ⁹ | `0x002D40FF` |
| ¹⁰ | `0x002D1667`-`0x002D166E` |
| ¹¹ | `0x0029FA05`-`0x0029FA0C` |
| ¹² | `0x002D3CB5`, `0x002D3D66` |
| ¹³ | `0x003FE1A2`-`0x003FE1CB` |
| ¹⁴ | `0x003FE30B`-`0x003FE324` |
| ¹⁵ | `0x003FDA35`, `0x003FDA4B`, `0x003FF099`-`0x003FF0A2` |
| ¹⁶ | `0x0057ACCE`-`0x0057ACD7` |
| ¹⁷ | `0x0031C853`-`0x0031C863`, `0x0035D3A6`-`0x0035D3BB` |

</details>

### The two hands

`0x00318B40(slots, slotJustSet, update)` runs after every store¹:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00318B40`-`0x00318C79` |

</details>

| Step | What happens | Where in the code |
|---|---|---|
| 1 | An empty main hand becomes Unarmed. | `0x00318B73`-`0x00318B8E` |
| 2 | It compares the main hand's `+0x11` with the off hand's class, `0xFF` for an empty off hand; on a match it is done. A two-handed weapon, `+0x11` of -1, with an empty off hand matches. | `0x00318BE0`-`0x00318C31` |
| 3 | On a mismatch after setting the off hand: a shield turns the main hand into Unarmed, and so does an emptied off hand under a weapon that does not take a shield, a bow, crossbow, gun or hand-bomb. | `0x00318C33`-`0x00318C5E` |
| 4 | On any other mismatch the off hand is emptied. | `0x00318C64`-`0x00318C79` |

With `update` non-zero each replacement also moves a worn copy: `0x0030F9A0` for the piece taken off and `0x0030C410`
for the one put on¹. With `update` 0 only the
words are written.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00318B79`-`0x00318B89`, `0x00318C4A`-`0x00318C59`, `0x00318C64`-`0x00318C74` |

</details>

| Action | Result |
|---|---|
| a two-handed weapon equipped while a shield is worn | the shield is dropped |
| a bow equipped over a shield or the wrong ammunition | the off hand is emptied; no ammunition is put in |
| a shield equipped under a two-handed or ammunition weapon | allowed; the weapon becomes Unarmed |
| ammunition equipped under the wrong weapon | refused by the eligibility test |
| ammunition removed from under its weapon | the weapon becomes Unarmed |

Every pairing test reads the main hand's `+0x11` and the off hand's `+0x09`; the off hand's own `+0x11` is never
read¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002F7F70`-`0x002F7F76`, `0x00317A7B`-`0x00317A7F`, `0x00318BE0` |

</details>

### Takeaway and giveback

`takeaway_item_and_equip` `0x388`, through `0x0030FBE0`, works on every record of party seats 0-8 except guests,
party rows 7-25¹:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0030FBF3`-`0x0030FC14` |

</details>

| Step | What happens | Where in the code |
|---|---|---|
| 1 | It copies the five slot words to the record's `+0x5A`-`+0x63`. | `0x0030FC1F`-`0x0030FC29` |
| 2 | It removes all gear with `0x0031A300(seat, 1)`. A seat with no record is skipped. After the nine seats it calls `0x00324380` once. | `0x0030FC2F`<br>`0x0030FC02`<br>`0x0030FC3B` |
| 3 | It backs up the counts of items `0x0000`-`0x003F` and equipment `0x1000`-`0x11A3` and sets them to 0 ([Inventory](inventory.md); `0x0030FC47`-`0x0030FCEF`); the placeholder rows above `0x11A3` are left alone. The call for `0x1000`, which `0x003008A0` refuses, copies that count but leaves it in place. It returns 1. | `0x003008DD`<br>`0x0030FCE2`<br>`0x0030FCFB` |

`giveback_item_and_equip` `0x387`, through `0x0030FAA0`, adds the counts back, re-equips the five stashed words
through `0x0031A710`, which tests each again, and clears the count backup¹. It does not clear
`+0x5A`-`+0x63`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0030FAAD`-`0x0030FBC7` |

</details>

The giveback's add for `0x1000` is refused as well¹. It re-equips the records of the seats that pass
the takeaway's test², calls `0x00324380` once before clearing the backup³ and
returns 1⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0030FB48` |
| ² | `0x0030FB70`-`0x0030FBA0` |
| ³ | `0x0030FBAC` |
| ⁴ | `0x0030FBCC` |

</details>

### Optimise

`0x002F9F20(seat, out)` builds the loadout¹:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002F9F20`-`0x002FA092` |

</details>

| Step | What happens | Where in the code |
|---|---|---|
| 1 | It starts from the five worn words. | `0x002F9F8D`-`0x002F9FB4` |
| 2 | For slots 0-3 it walks a range of ids, `0x1000`-`0x10C7` for slot 0, `0x10C8`-`0x11A3` for slot 1, `0x10DC`-`0x1117` for slot 2 and `0x1118`-`0x1153` for slot 3 (tables `0x00D0F9C0`, `0x00D0F9D0`). The accessory, slot 4, is never walked. |   |
| 3 | A candidate must pass the eligibility test with the free-copy test, and for the off hand `0x002F7EC0` against the chosen main hand. | `0x00317B20`<br>`0x002F9FF1`-`0x002FA01A` |
| 4 | `0x002F7A10` keeps the better of the current choice and the candidate. | `0x002FA01C`-`0x002FA03C` |
| 5 | After slot 0, an empty main hand becomes Unarmed and an off hand that no longer pairs is emptied. | `0x002FA056`-`0x002FA077` |

The record is `0x00320AB0(seat, 3)`; for a seat with no record `0x002F9F20` writes nothing and returns 0, otherwise it
returns 1¹. The candidate is tested on the loadout being built, `out`². Ammunition, ids `0x1184`-`0x11A3` of the slot-1 walk, is ranked by `0x002F7A10` with the
weapon's rules, slot 0³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002F9F5B`-`0x002F9F66`, `0x002FA09D` |
| ² | `0x002F9FF1`-`0x002F9FFF` |
| ³ | `0x002FA021`-`0x002FA033` |

</details>

`0x002F7A10(current, candidate, slot, record)` returns the id it keeps. It keeps `current` when the candidate has no
row or its row's slot bits are 4 or 5, and takes the candidate when `current` is empty or has no row¹. For a slot above 3 it goes straight to the final tie².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002F7A3B`-`0x002F7AFC` |
| ² | `0x002F7B0C`-`0x002F7B0F` |

</details>

`0x002F7A10` ranks by slot:

| Slot | First | Then |
|---|---|---|
| weapon, and ammunition | `0x002F7C80(id, record)`: 0 for Unarmed or an empty id (`0x002F7CB4`-`0x002F7CC5`); Attack Power `+0x1A`; for a bow, crossbow, gun or hand-bomb, a weapon whose `+0x11` is 23-26 (`0x002F7D1E`-`0x002F7D26`), plus the best usable ammunition's `+0x1A`, or -1 when there is no usable ammunition. The search starts from the ammunition in the record's off hand `+0x52` when its class is the weapon's `+0x11`, and ranks with `0x002F7A10` slot 0 each id `0x1184`-`0x11A3` of that class that passes the eligibility test for slot 1 with the free-copy test on an empty loadout (`0x002F7D31`-`0x002F7EA9`) | the larger value (`0x002F7BE4`-`0x002F7BE8`), then the live weapon, the record's `+0x50`, then the live weapon's class, then the lower class (`0x002F7B78`-`0x002F7C37`) |
| shield | evade `+0x18` | magick evade `+0x19` |
| helm | Magick Resist `+0x19` | Defense `+0x18` |
| armor | Defense `+0x18` | Magick Resist `+0x19` |

A final tie goes to the larger `+0x06`, then the higher id¹. A worn piece stays unless an
eligible one beats it.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002F7C3C`-`0x002F7C56` |

</details>

## Shipped data

<details>
<summary>Show the shipped data</summary>

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

</details>

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

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 38 calls with 12 other topics</summary>

**Enemy AI and gambits** (explained on [glossary](../Engine-Core/glossary.md), [spawn record fields](../Enemy-Spawning/spawn-record-fields.md), [battle units](../Characters-And-Objects/battle-units.md), [frame update order](../Engine-Core/frame-update-order.md), [enmity](../Enemy-AI-And-Gambits/enmity.md), [gambit screen](../Menus-And-HUD/gambit-screen.md), [item and ability ids](../Engine-Core/item-and-ability-ids.md), [battle verbs](../Scripts-And-Script-Commands/battle-verbs.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00322C50`](../Engine-Core/item-and-ability-ids.md) Battle encoded id: is valid for class (on item and ability ids) | is called by | [`0x00301AD0`](../Enemy-AI-And-Gambits/enemy-order-sets.md) Ai order: evaluate target selector (on enemy order sets)<br>[`0x003215C0`](../Enemy-AI-And-Gambits/enmity.md) Battle enmity: read for combatant id (on enmity)<br>[`0x00321630`](../Enemy-AI-And-Gambits/enmity.md) Battle enmity: get highest relevant (on enmity)<br>[`0x00321770`](../Enemy-AI-And-Gambits/enmity.md) Battle enmity: any above threshold (on enmity)<br>[`0x00321850`](../Enemy-AI-And-Gambits/enmity.md) Battle enmity: write for combatant id (on enmity)<br>[`0x003219D0`](../Enemy-AI-And-Gambits/enmity.md) Battle enmity: propagate to perceiving foes (on enmity)<br>[`0x00321B00`](../Enemy-AI-And-Gambits/enmity.md) Battle enmity: adjust other relevant combatants (on enmity)<br>[`0x00321E40`](../Battle-Actions/weapon-motion-list.md) Battle enmity: clamp and store (on weapon motion list)<br>[`0x00327A10`](../Menus-And-HUD/widgets.md) Gambit config: classify action target pair compatibility (on widgets)<br>[`0x00327CB0`](../Enemy-AI-And-Gambits/gambits.md) Gambit config: load authored preset and rebuild runtime orders (on gambits) |
| [`0x00377C20`](../Scripts-And-Script-Commands/party-during-scenes.md) (on party during scenes) | is called by | [`0x003014C0`](../Enemy-AI-And-Gambits/gambits.md) Ai order: evaluate and resolve action target (on gambits)<br>[`0x00301AD0`](../Enemy-AI-And-Gambits/enemy-order-sets.md) Ai order: evaluate target selector (on enemy order sets)<br>[`0x00305AB0`](../Enemy-AI-And-Gambits/gambits.md) Battle unit: select and commit next action (on gambits) |

**Controls and input** (explained on [force fight mode](../Engine-Core/force-fight-mode.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00377C20`](../Scripts-And-Script-Commands/party-during-scenes.md) (on party during scenes) | is called by | [`0x00253C70`](../Controls-And-Input/controls.md) (on controls) |

**Input gameplay** (explained on [force fight mode](../Engine-Core/force-fight-mode.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00377C20`](../Scripts-And-Script-Commands/party-during-scenes.md) (on party during scenes) | is called by | [`0x00313A00`](../Battle-Actions/action-phases.md) (on action phases) |

**Movement and pathfinding** (explained on [status timers](../Status-Effects-And-KO/status-timers.md), [battle locomotion](../Movement-And-Pathfinding/battle-locomotion.md), [game over](../World-Areas-And-Travel/game-over.md), [party data](../Party/party-data.md), [script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md), [time stop and freeze](../Engine-Core/time-stop-and-freeze.md), [script binding lifecycle](../Scripts-And-Script-Commands/script-binding-lifecycle.md), [navigation mesh and pathfinding](../Movement-And-Pathfinding/navigation-mesh-and-pathfinding.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0031B860`](../Battle-Actions/battle-log.md) Battle stats: find owning battle unit (on battle log) | is called by | [`0x0033CB10`](../Status-Effects-And-KO/status-timers.md) (on status timers)<br>[`0x0033D890`](../Movement-And-Pathfinding/battle-locomotion.md) (on battle locomotion) |
| [`0x00322C50`](../Engine-Core/item-and-ability-ids.md) Battle encoded id: is valid for class (on item and ability ids) | is called by | [`0x0031BAC0`](../Party/party-slots.md) (on party slots)<br>[`0x00326BB0`](../Party/party-data.md) (on party data) |
| [`0x00377C20`](../Scripts-And-Script-Commands/party-during-scenes.md) (on party during scenes) | is called by | [`0x0025B470`](../Movement-And-Pathfinding/movement-bodies-and-separation.md) (on movement bodies and separation)<br>[`0x0026C3E0`](../Engine-Core/time-stop-and-freeze.md) (on time stop and freeze)<br>[`0x002E28E0`](../Movement-And-Pathfinding/movement-bodies-and-separation.md) (on movement bodies and separation)<br>[`0x00310920`](../Party/party-slots.md) (on party slots)<br>[`0x00313670`](../Party/party-slots.md) (on party slots) |

**Scripts and script commands** (explained on [battle unit construction](../Characters-And-Objects/battle-unit-construction.md), [battle verbs](../Scripts-And-Script-Commands/battle-verbs.md), [party during scenes](../Scripts-And-Script-Commands/party-during-scenes.md), [script censuses](../Story-Events-And-Hunts/script-censuses.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00320AB0`](../Engine-Core/subsystem-update-flags.md) (on subsystem update flags) | is called by | [`0x0050FD00`](../Damage-And-Battle-Formulas/stats.md) (on stats)<br>[`0x0050FD50`](../Damage-And-Battle-Formulas/stats.md) (on stats)<br>[`0x0050FDD0`](../Damage-And-Battle-Formulas/stats.md) (on stats)<br>[`0x0050FE20`](../Damage-And-Battle-Formulas/stats.md) (on stats)<br>[`0x0050FE80`](../Damage-And-Battle-Formulas/stats.md) (on stats)<br>[`0x0050FED0`](../Damage-And-Battle-Formulas/stats.md) (on stats)<br>[`0x0050FF20`](../Characters-And-Objects/battle-unit-construction.md) (on battle unit construction) |
| [`0x00377C20`](../Scripts-And-Script-Commands/party-during-scenes.md) (on party during scenes) | is called by | [`0x00344740`](../Scripts-And-Script-Commands/battle-verbs.md) (on battle verbs)<br>[`0x00352FA0`](../Scripts-And-Script-Commands/party-during-scenes.md) (on party during scenes)<br>[`0x003537D0`](../Battle-Actions/weapon-motion-list.md) (on weapon motion list)<br>[`0x00355680`](../Story-Events-And-Hunts/script-censuses.md) (on script censuses) |

**Engine core** (explained on [frame update order](../Engine-Core/frame-update-order.md), [enemy respawning](../Enemy-Spawning/enemy-respawning.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00237DF0`](../Enemy-Spawning/enemy-respawning.md) (on enemy respawning) | calls | [`0x00229ED0`](../Saving-Loading-And-Settings/game-settings.md) (on game settings)<br>[`0x0032A160`](../Enemy-Spawning/enemy-respawning.md) (on enemy respawning) |

**Saving, loading and settings** (explained on [item and ability ids](../Engine-Core/item-and-ability-ids.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00237DF0`](../Enemy-Spawning/enemy-respawning.md) (on enemy respawning) | is called by | [`0x00238A80`](bazaar.md) (on bazaar) |

</details>

---

[Equipping an item →](equipping-an-item.md)
