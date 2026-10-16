---
title: "Equipment row: every field of a weapon, shield, armor, accessory or ammunition data row and its bonus record"
kind: "format"
category: "Items, equipment, shops and licenses"
addresses: "02EBF0F8, 00238160, 0031E9F0, 0031E9A0, 0031C5D0, 002FEF30, 0030FED0, 00317930"
---

## What the player sees

- Every weapon, shield, helm, armor piece, accessory and ammunition has its own row of numbers: its price, its
  attack or defense, its element, the statuses it inflicts or protects from, and its bonuses.
- One-handed weapons can be paired with a shield; bows, crossbows, guns and hand-bombs take their own ammunition;
  other weapons use both hands.
- Some unique items cannot be sold.

## Where it comes from

The rows are section 13 of `battle_pack.bin`, the section its directory entry at file offset `+38`<sub>h</sub> points to.
The section is an `st2e` table of 557 rows of 52 bytes starting `20`<sub>h</sub> bytes in; in the `us` file it is at
`B048`<sub>h</sub>. Row *n* is equipment id `1000h + n`: Unarmed is row 0, Broadsword row 1. Rows 0-419 are the items the
id space names (ids up to `11A3`<sub>h</sub>, [Item and ability ids](../Engine-Core/item-and-ability-ids.md)).

The bonus records follow the rows at section offset `7144`<sub>h</sub>, 176 records of 24 bytes. A row's `+28`<sub>h</sub> is the
offset of its record from there, and every row points at one; record 0 is the empty one.

Every reader computes the row itself: it loads the registry slot `02EBF0F8`, resolves the slot's `+0C`<sub>h</sub> through
`0020E600` to the first row, and adds `(id - 1000h)` times the slot's `u16` stride at `+08`<sub>h</sub>
(`0031C869`-`0031C8F3` is one example). The bonus record is `0020E600(row +28h)`.

## Layouts

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u16` | pad00 | 0 on every row |
| `02`<sub>h</sub> | `u16` | nameWord | name: bank = word >> 11, entry = word & `7FF`<sub>h</sub> (`0031C5D0` at `0031C911`) |
| `04`<sub>h</sub> | `u8` | subType | kind of item, copied to the query record `+2C`<sub>h</sub> (`0031C9C4`) |
| `05`<sub>h</sub> | `u8` | pad05 | 0 on every row |
| `06`<sub>h</sub> | `u8` | sortKey | the Optimise tie-break: equal values go to the higher id (`002F7C3C`) |
| `07`<sub>h</sub> | `u8` | slotFlags | bits 7-5 slot, bit 4 no license, bit 2 hits flying, bit 1 cannot sell; table below |
| `08`<sub>h</sub> | `u8` | ordinal | order of the row inside its class (`0031C9CB`) |
| `09`<sub>h</sub> | `u8` | class | equipment class 0-26; sets the group and the pairing (`0031E9F0`) |
| `0A`<sub>h</sub> | `u32` | pad0A | 0 on every row |
| `0E`<sub>h</sub> | `u16` | helpId | extra text id, through `002F9860` (`0031C9B0`); 0 on every row |
| `10`<sub>h</sub> | `u8` | chargeWeight | summed over the five equipped items to slow the charge while battle flag `022C314C` bit 6 is set (`002F9C00`) |
| `11`<sub>h</sub> | `i8` | offHandClass | the class an off-hand item must have; -1 for none (`002F7EC0`, `00317930`) |
| `12`<sub>h</sub> | `u16` | price | buy price in gil (`0031C981`) |
| `14`<sub>h</sub> | `u32` | pad14 | 0 on every row |
| `18`<sub>h</sub> | `u8` | value18 | reach, shield evade or Defense, by group; table below |
| `19`<sub>h</sub> | `u8` | value19 | recipe, magick evade or Magick Resist, by group |
| `1A`<sub>h</sub> | `u8` | value1A | Attack Power or augment, by group |
| `1B`<sub>h</sub> | `u8` | knockback | weapons: knockback chance (`00388350` at `00388409`) |
| `1C`<sub>h</sub> | `u8` | combo | weapons: combo chance, or critical chance for recipes 25-27 (`00388550`, `00389140`) |
| `1D`<sub>h</sub> | `u8` | weaponEvade | weapons: added to weapon evade (`002FF4A0`) |
| `1E`<sub>h</sub> | `u8` | element | weapons and ammunition: attack element, one bit each (`0038BE30`) |
| `1F`<sub>h</sub> | `u8` | statusChance | weapons and ammunition: on-hit status chance, percent (`0038F9D0` at `0038FB44`) |
| `20`<sub>h</sub> | `u32` | statusMask | weapons and ammunition: statuses a plain Attack inflicts (`00384C30` at `00384DB2`) |
| `24`<sub>h</sub> | `u8` | b24 | weapons: one value per weapon kind; no read in a census of the code that loads `02EBF0F8` and its callees |
| `25`<sub>h</sub> | `u8` | reachKind | weapons: which range pair sets the near and middle distance (`00320D70` at `00320D93`) |
| `26`<sub>h</sub> | `u8` | motionClass | weapons: attack motion class, through the map at `02EBF180`, main-hand rows only (`003203B0` at `0032041E`) |
| `27`<sub>h</sub> | `u8` | chargeBase | weapons: charge time base for actions with flag `+0C`<sub>h</sub> bit 27 (`002F8410` at `002F851A`) |
| `28`<sub>h</sub> | `u32` | bonusRecord | offset of the bonus record from section offset `7144`<sub>h</sub>, 0-4200; rebased at load (`0023823E`) |
| `2C`<sub>h</sub> | `u16` | attackEffect | weapons: low 15 bits = the effect a plain Attack shows (`0030AC50` at `0030AD56`) |
| `2E`<sub>h</sub> | `u16` | pad2E | 0 on every row |
| `30`<sub>h</sub> | `u32` | modelId | weapons, ammunition and shields: the held model, `0077xxxx`<sub>h</sub> (`0031BF60` at `0031BFE0`) |

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u16` | maxHp | added to max HP (`002FF4AF`) |
| `02`<sub>h</sub> | `u16` | maxMp | added to max MP (`002FF4BF`) |
| `04`<sub>h</sub> | `u8` | strength | added to Strength (`002FF4CF`) |
| `05`<sub>h</sub> | `u8` | magickPower | added to Magick Power (`002FF4DE`) |
| `06`<sub>h</sub> | `u8` | vitality | added to Vitality (`002FF4ED`) |
| `07`<sub>h</sub> | `u8` | speed | added to Speed (`002FF4FD`) |
| `08`<sub>h</sub> | `u32` | statusesHeld | statuses the wearer has while it is equipped, into stats `+3C`<sub>h</sub> (`002FF51B`) |
| `0C`<sub>h</sub> | `u32` | statusImmune | statuses the wearer cannot get, into stats `+38`<sub>h</sub> (`002FF50D`) |
| `10`<sub>h</sub> | `u8` | absorb | elements absorbed, into stats `+41`<sub>h</sub> (`002FF538`) |
| `11`<sub>h</sub> | `u8` | immune | elements nullified, into stats `+43`<sub>h</sub> (`002FF556`) |
| `12`<sub>h</sub> | `u8` | halved | elements halved, into stats `+42`<sub>h</sub> (`002FF547`) |
| `13`<sub>h</sub> | `u8` | weak | elements the wearer is weak to, into stats `+40`<sub>h</sub> (`002FF529`) |
| `14`<sub>h</sub> | `u8` | potency | elements boosted, into stats `+44`<sub>h</sub> (`002FF56D`) |
| `15`<sub>h</sub> | `u8[3]` | pad15 | 0 in every record |

What each record field does to a unit is on [Stats](../Damage-And-Battle-Formulas/stats.md) and
[Elements](../Damage-And-Battle-Formulas/elements.md).

### The slot and flag byte

| Bits of `+07`<sub>h</sub> | Meaning | Readers |
|---|---|---|
| 7-5 | the slot: 0 main hand, 1 off hand (shields and ammunition), 2 head, 3 body, 4 accessory | the slot test `00317930` (`00317A18`), Optimise `002F7A10` (`002F7A87`), the shop classifier `002FABD0` (`002FAC9D`) |
| 4 | needs no license | the license test skips the item (`00323CDF`) |
| 2 | reaches flying targets | `00390CF6` for weapon actions, formula slot 12 (`0038895B`) |
| 1 | cannot be sold | copied to the query record `+54`<sub>h</sub> bit 0 (`0031CA3C`-`0031CA47`), which the shop turns into price bit 31 (`0057DED0`) |
| 0, 3 | not set on any row | - |

### The class byte and the group

`0031E9F0` maps the class `+09`<sub>h</sub> through the 27 bytes at `0031EA74` and the jump table at `0031EA50` to a
category 1-9, and `0031E9A0` folds the category into the group (`0031E9A0`-`0031E9DD`). The group decides what
`+18`<sub>h</sub>, `+19`<sub>h</sub> and `+1A`<sub>h</sub> mean in the stats rebuild `002FEF30` (`002FF451`), the augment rebuild `0030FED0`
(`003100E5`) and the query filler `0031C5D0` (`0031CA54`):

| Category | Classes | Group | `+18`<sub>h</sub> | `+19`<sub>h</sub> | `+1A`<sub>h</sub> |
|---|---|---|---|---|---|
| 1 | 0 | `1` | reach | recipe | Attack Power |
| 2 | 1, 10, 11, 12, 15, 16 | `1` | reach | recipe | Attack Power |
| 3 | 2-6, 13, 14 | `1` | reach | recipe | Attack Power |
| 4 | 7, 8, 9, 17 | `1` | reach | recipe | Attack Power |
| 5 | 23-26 | `1` | 0 | 0 | Attack Power |
| 6 | 18 | `2` | shield evade | magick evade | 0 |
| 7, 8, 9 | 19, 20, 21-22 | `3` | Defense | Magick Resist | augment, `FF`<sub>h</sub> for none |

Reach is in tenths (`00309300` at `0030938B`); the recipe is the plain Attack's damage formula (`00385F60` at
`003861FD`, [Weapon formulas](../Damage-And-Battle-Formulas/weapon-formulas.md)); the augment is the one the item gives
(`0030FED0` at `003100EF`, [Augments](../Damage-And-Battle-Formulas/augments.md)).

Most combat readers do not test the group: they read the weapon fields of the main-hand item, stats `+50`<sub>h</sub>. They
read the element, status chance and statuses from the off-hand item instead when the weapon's `+11`<sub>h</sub> is 23 or
above as an unsigned byte (`0038BEDE`, `0038FA54`, `00384D09`). That includes the -1 of two-handed weapons, whose
off hand is empty, so they fall back to the weapon's own fields.

### Pairing

The off-hand item's class must equal the main-hand item's `+11`<sub>h</sub> (`002F7EC0` at `002F7F70`-`002F7F76`). The
shipped rows use 18, a shield, on one-handed weapons, 23-26 on the four ammunition weapons, and -1 elsewhere, so
two-handed weapons take nothing in the off hand.

## Shipped data

| Class | Category | Rows | Off hand | First items |
|---|---|---:|---|---|
| `0` | 1 | 11 | 18 or none | Unarmed |
| `1` | 2 | 27 | 18 | Broadsword, Longsword, Iron Sword |
| `2` | 3 | 13 | none | Claymore, Defender, Save the Queen |
| `3` | 3 | 10 | none | Kotetsu, Osafune, Kogarasumaru |
| `4` | 3 | 8 | none | Ashura, Sakura-saezuri, Kagenui |
| `5` | 3 | 15 | none | Javelin, Spear, Partisan |
| `6` | 3 | 13 | none | Oaken Pole, Cypress Pole, Battle Bamboo |
| `7` | 4 | 16 | 23 | Shortbow, Silver Bow, Aevis Killer |
| `8` | 4 | 9 | 24 | Bowgun, Crossbow, Paramina Crossbow |
| `9` | 4 | 12 | 25 | Altair, Capella, Vega |
| `10` | 2 | 7 | 18 | Handaxe, Broadaxe, Slasher |
| `11` | 2 | 6 | 18 | Iron Hammer, War Hammer, Sledgehammer |
| `12` | 2 | 12 | 18 | Dagger, Mage Masher, Assassin's Dagger |
| `13` | 3 | 8 | none | Rod, Serpent Rod, Healing Rod |
| `14` | 3 | 10 | none | Oak Staff, Cherry Staff, Wizard's Staff |
| `15` | 2 | 11 | 18 | Mace, Bronze Mace, Bhuj |
| `16` | 2 | 6 | 18 | Gilt Measure, Arc Scale, Multiscale |
| `17` | 4 | 6 | 26 | Hornito, Fumarole, Tumulus |
| `18` | 6 | 20 | none | Gendarme, Leather Shield, Buckler |
| `19` | 7 | 60 | none | Leather Cap, Headgear, Headguard |
| `20` | 8 | 60 | none | Leather Clothing, Chromed Leathers, Leather Breastplate |
| `21` | 9 | 42 | none | Opal Ring, Ruby Ring, Tourmaline Ring |
| `22` | 9 | 6 | none | Manufacted Nethicite, Cat-ear Hood, Fuzzy Miter |
| `23` | 5 | 8 | none | Onion Arrows, Parallel Arrows, Fiery Arrows |
| `24` | 5 | 8 | none | Onion Bolts, Long Bolts, Stone Bolts |
| `25` | 5 | 8 | none | Onion Shot, Silent Shot, Aqua Shot |
| `26` | 5 | 8 | none | Onion Bombs, Poison Bombs, Stun Bombs |

The rows count ids `1000`<sub>h</sub>-`11A3`<sub>h</sub>, and the names are each row's own name word. Rows 420-556 are unused
placeholder rows named "NOT USED" and "Reserve".

| Field | Values in rows 0-419 |
|---|---|
| `+12`<sub>h</sub> price | 0 to 56,000; Unarmed 0, Broadsword 390, Flametongue 4,000; Excalibur, Gendarme and the Genji Shield 1; Ribbon 10 |
| `+07`<sub>h</sub> bit 1 | set on Hero's Blade, Treaty-Blade, Sword of Kings, Joyeuse, Chirijiraden, Manufacted Nethicite, Goddess's Magicite and Dawn Shard, among others |
| `+10`<sub>h</sub> | 0 on 260 rows, 1 on 72, 2 on 84, 3 on 1, 5 on 3 |
| `+18`<sub>h</sub> on weapons | 10 on 144, 100 on 42, 20 on 10, 30 on 3, 200 on 1 |
| `+19`<sub>h</sub> on weapons | 20-29, and 104 on maces |
| `+1A`<sub>h</sub> on weapons and ammunition | 1 to 224 |
| `+27`<sub>h</sub> on weapons | 10 to 99 |

Flametongue, row 8: class 1, off hand 18, price 4,000, reach 10, recipe 20, Attack Power 45, knockback 10,
combo 5, weapon evade 5, element fire (`01`<sub>h</sub>), charge base 32, bonus record 0, effect `8003`<sub>h</sub>, model
`770020`<sub>h</sub>. Ribbon, row 385: class 22, slot 4, price 10, Defense 1, Magick Resist 1, no augment, bonus record
4200, which holds Regen and Libra and protects from Petrify, Stop, Sleep, Confuse, Doom, Blind, Poison, Silence,
Sap, Oil, Disable, Immobilize, Slow and Disease.

## Loader behaviour

1. `00236C30` passes the directory entry `+38`<sub>h</sub> to `00238160` (`00236D73`).
2. `00238160` binds `02EBF0F8` to the section through `003845F0`, which rebases the header's rows offset `+0C`<sub>h</sub>
   and bonus offset `+18`<sub>h</sub> by the section address (`0038460E`, `0038462F`).
3. It then rewrites every row's `+28`<sub>h</sub> to the encoded address of its bonus record, header `+18`<sub>h</sub> plus the stored
   offset (`00238225`-`0023823E`). Nothing else writes a row.

## Modding notes

- Price is `+12`<sub>h</sub>; making an item unsellable is `+07`<sub>h</sub> bit 1.
- A weapon's damage formula is `+19`<sub>h</sub>; its element `+1E`<sub>h</sub>; its on-hit statuses `+1F`<sub>h</sub> and `+20`<sub>h</sub>.
- The class `+09`<sub>h</sub> decides how the game reads `+18`<sub>h</sub>-`+1A`<sub>h</sub>: a row moved to another group changes meaning.
- To let a two-handed weapon take a shield, set its `+11`<sub>h</sub> to 18. A value of 23 or above, or -1, makes combat read
  the element and statuses from whatever is in the off hand.
- Bonuses that every item can carry, stats, held statuses, immunities and elements, live in the bonus record, so
  two rows can share one record.

## Related

- [Stats](../Damage-And-Battle-Formulas/stats.md) - what the groups and the bonus record add.
- [Augments](../Damage-And-Battle-Formulas/augments.md) - the augment byte of armor and accessories.
- [Elements](../Damage-And-Battle-Formulas/elements.md) - the element bytes.
- [Weapon formulas](../Damage-And-Battle-Formulas/weapon-formulas.md) - recipe, knockback, combo and statuses.
