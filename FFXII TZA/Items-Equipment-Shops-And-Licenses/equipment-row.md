---
title: "Equipment row: every field of a weapon, shield, armor, accessory or ammunition data row and its bonus record"
kind: "format"
category: "Items, equipment, shops and licenses"
addresses: "0x02EBF0F8, 0x00238160, 0x0031E9F0, 0x0031E9A0, 0x0031C5D0, 0x002FEF30, 0x0030FED0, 0x00317930"
---

## What the player sees

- Every weapon, shield, helm, armor piece, accessory and ammunition has its own row of numbers: its price, its
  attack or defense, its element, the statuses it inflicts or protects from, and its bonuses.
- One-handed weapons can be paired with a shield; bows, crossbows, guns and hand-bombs take their own ammunition;
  other weapons use both hands.
- Some unique items cannot be sold.

## Where it comes from

The rows are section 13 of `battle_pack.bin`, the section its directory entry at file offset `+0x38` points to.
The section is an `st2e` table of 557 rows of 52 bytes starting `0x20` bytes in; in the `us` file it is at
`0xB048`. Row *n* is equipment id `0x1000 + n`: Unarmed is row 0, Broadsword row 1. Rows 0-419 are the items the
id space names (ids up to `0x11A3`, [Item and ability ids](../Engine-Core/item-and-ability-ids.md)).

The bonus records follow the rows at section offset `0x7144`, 176 records of 24 bytes. A row's `+0x28` is the
offset of its record from there, and every row points at one; record 0 is the empty one.

Every reader computes the row itself: it loads the registry slot `0x02EBF0F8`, resolves the slot's `+0x0C` through
`0x0020E600` to the first row, and adds `(id - 0x1000)` times the slot's `u16` stride at `+0x08`
(`0x0031C869`-`0x0031C8F3` is one example). The bonus record is `0x0020E600(row +0x28)`.

## Layouts

All multi-byte fields are little-endian.

Offsets in the row table are from the start of the row, and offsets in the bonus record table from the start of
the record. Row *n* starts at the header's `+0x0C` plus *n* times the header's `u16` stride at `+0x08`
(`0x002381CC`-`0x002381DA`). In the `us` file the header holds 557 rows (`+0x04`), stride 52, rows at `0x20` and
bonus records at `0x7144` (`+0x18`).

The header's `+0x0C` and `+0x18` are offsets from the start of the section, rebased by `0x003845F0` (`0x0038460E`,
`0x0038462F`). A row's `+0x28` is an offset from the header's `+0x18` (`0x00238225`-`0x0023823E`). The directory entry
`+0x38` is an offset from the start of `battle_pack.bin`, rebased by `0x003846F0` (`0x00384759`-`0x00384780`).

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u16` | pad00 | 0 on every row |
| `+0x02` | `u16` | nameWord | name: bank = word >> 11, entry = word & `0x7FF` (`0x0031C5D0` at `0x0031C911`) |
| `+0x04` | `u8` | subType | kind of item, copied to the query record `+0x2C` (`0x0031C9C4`) |
| `+0x05` | `u8` | pad05 | 0 on every row |
| `+0x06` | `u8` | sortKey | the Optimise tie-break: equal values go to the higher id (`0x002F7C3C`) |
| `+0x07` | `u8` | slotFlags | bits 7-5 slot, bit 4 no license, bit 2 hits flying, bit 1 cannot sell; table below |
| `+0x08` | `u8` | ordinal | order of the row inside its class (`0x0031C9CB`) |
| `+0x09` | `u8` | class | equipment class 0-26; sets the group and the pairing (`0x0031E9F0`) |
| `+0x0A` | `u32` | pad0A | 0 on every row |
| `+0x0E` | `u16` | helpId | extra text id, through `0x002F9860` (`0x0031C9B0`); 0 on every row |
| `+0x10` | `u8` | chargeWeight | summed over the five equipped items to slow the charge while battle flag `0x022C314C` bit 6 is set (`0x002F9C00`) |
| `+0x11` | `i8` | offHandClass | the class an off-hand item must have; -1 for none (`0x002F7EC0`, `0x00317930`) |
| `+0x12` | `u16` | price | buy price in gil (`0x0031C981`) |
| `+0x14` | `u32` | pad14 | 0 on every row |
| `+0x18` | `u8` | value18 | reach, shield evade or Defense, by group; table below |
| `+0x19` | `u8` | value19 | recipe, magick evade or Magick Resist, by group |
| `+0x1A` | `u8` | value1A | Attack Power or augment, by group |
| `+0x1B` | `u8` | knockback | weapons: knockback chance (`0x00388350` at `0x00388409`) |
| `+0x1C` | `u8` | combo | weapons: combo chance, or critical chance for recipes 25-27 (`0x00388550`, `0x00389140`) |
| `+0x1D` | `u8` | weaponEvade | weapons: added to weapon evade (`0x002FF4A0`) |
| `+0x1E` | `u8` | element | weapons and ammunition: attack element, one bit each (`0x0038BE30`) |
| `+0x1F` | `u8` | statusChance | weapons and ammunition: on-hit status chance, percent (`0x0038F9D0` at `0x0038FB44`) |
| `+0x20` | `u32` | statusMask | weapons and ammunition: statuses a plain Attack inflicts (`0x00384C30` at `0x00384DB2`) |
| `+0x24` | `u8` | b24 | weapons: one value per weapon kind; no read in a census of the code that loads `0x02EBF0F8` and its callees |
| `+0x25` | `u8` | reachKind | weapons: which range pair sets the near and middle distance (`0x00320D70` at `0x00320D93`) |
| `+0x26` | `u8` | motionClass | weapons: attack motion class, through the map at `0x02EBF180`, main-hand rows only (`0x003203B0` at `0x0032041E`) |
| `+0x27` | `u8` | chargeBase | weapons: charge time base for actions with flag `+0x0C` bit 27 (`0x002F8410` at `0x002F851A`) |
| `+0x28` | `u32` | bonusRecord | offset of the bonus record from section offset `0x7144`, 0-4200; rebased at load (`0x0023823E`) |
| `+0x2C` | `u16` | attackEffect | weapons: low 15 bits = the effect a plain Attack shows (`0x0030AC50` at `0x0030AD56`) |
| `+0x2E` | `u16` | pad2E | 0 on every row |
| `+0x30` | `u32` | modelId | weapons, ammunition and shields: the held model, 0x0077xxxx (`0x0031BF60` at `0x0031BFE0`) |

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u16` | maxHp | added to max HP (`0x002FF4AF`) |
| `+0x02` | `u16` | maxMp | added to max MP (`0x002FF4BF`) |
| `+0x04` | `u8` | strength | added to Strength (`0x002FF4CF`) |
| `+0x05` | `u8` | magickPower | added to Magick Power (`0x002FF4DE`) |
| `+0x06` | `u8` | vitality | added to Vitality (`0x002FF4ED`) |
| `+0x07` | `u8` | speed | added to Speed (`0x002FF4FD`) |
| `+0x08` | `u32` | statusesHeld | statuses the wearer has while it is equipped, into stats `+0x3C` (`0x002FF51B`) |
| `+0x0C` | `u32` | statusImmune | statuses the wearer cannot get, into stats `+0x38` (`0x002FF50D`) |
| `+0x10` | `u8` | absorb | elements absorbed, into stats `+0x41` (`0x002FF538`) |
| `+0x11` | `u8` | immune | elements nullified, into stats `+0x43` (`0x002FF556`) |
| `+0x12` | `u8` | halved | elements halved, into stats `+0x42` (`0x002FF547`) |
| `+0x13` | `u8` | weak | elements the wearer is weak to, into stats `+0x40` (`0x002FF529`) |
| `+0x14` | `u8` | potency | elements boosted, into stats `+0x44` (`0x002FF56D`) |
| `+0x15` | `u8[3]` | pad15 | 0 in every record |

What each record field does to a unit is on [Stats](../Damage-And-Battle-Formulas/stats.md) and
[Elements](../Damage-And-Battle-Formulas/elements.md).

### The slot and flag byte

| Bits of `+0x07` | Meaning | Readers |
|---|---|---|
| 7-5 | the slot: 0 main hand, 1 off hand (shields and ammunition), 2 head, 3 body, 4 accessory | the slot test `0x00317930` (`0x00317A18`), Optimise `0x002F7A10` (`0x002F7A87`), the shop classifier `0x002FABD0` (`0x002FAC9D`) |
| 4 | needs no license | the license test skips the item (`0x00323CDF`) |
| 2 | reaches flying targets | `0x00390CF6` for weapon actions, formula slot 12 (`0x0038895B`) |
| 1 | cannot be sold | copied to the query record `+0x54` bit 0 (`0x0031CA3C`-`0x0031CA47`), which the shop turns into price bit 31 (`0x0057DED0`) |
| 0, 3 | not set on any row | - |

### The class byte and the group

`0x0031E9F0` maps the class `+0x09` through the 27 bytes at `0x0031EA74` and the jump table at `0x0031EA50` to a
category 1-9, and `0x0031E9A0` folds the category into the group (`0x0031E9A0`-`0x0031E9DD`). The group decides what
`+0x18`, `+0x19` and `+0x1A` mean in the stats rebuild `0x002FEF30` (`0x002FF451`), the augment rebuild `0x0030FED0`
(`0x003100E5`) and the query filler `0x0031C5D0` (`0x0031CA54`):

| Category | Classes | Group | `+0x18` | `+0x19` | `+0x1A` |
|---|---|---|---|---|---|
| 1 | 0 | `1` | reach | recipe | Attack Power |
| 2 | 1, 10, 11, 12, 15, 16 | `1` | reach | recipe | Attack Power |
| 3 | 2-6, 13, 14 | `1` | reach | recipe | Attack Power |
| 4 | 7, 8, 9, 17 | `1` | reach | recipe | Attack Power |
| 5 | 23-26 | `1` | 0 | 0 | Attack Power |
| 6 | 18 | `2` | shield evade | magick evade | 0 |
| 7, 8, 9 | 19, 20, 21-22 | `3` | Defense | Magick Resist | augment, `0xFF` for none |

Reach is in tenths (`0x00309300` at `0x0030938B`); the recipe is the plain Attack's damage formula (`0x00385F60` at
`0x003861FD`, [Weapon formulas](../Damage-And-Battle-Formulas/weapon-formulas.md)); the augment is the one the item gives
(`0x0030FED0` at `0x003100EF`, [Augments](../Damage-And-Battle-Formulas/augments.md)).

Most combat readers do not test the group: they read the weapon fields of the main-hand item, stats `+0x50`. They
read the element, status chance and statuses from the off-hand item instead when the weapon's `+0x11` is 23 or
above as an unsigned byte (`0x0038BEDE`, `0x0038FA54`, `0x00384D09`). That includes the -1 of two-handed weapons, whose
off hand is empty, so they fall back to the weapon's own fields.

### Pairing

The off-hand item's class must equal the main-hand item's `+0x11` (`0x002F7EC0` at `0x002F7F70`-`0x002F7F76`). The
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

The rows count ids `0x1000`-`0x11A3`, and the names are each row's own name word. Rows 420-556 are unused
placeholder rows named "NOT USED" and "Reserve".

| Field | Values in rows 0-419 |
|---|---|
| `+0x12` price | 0 to 56,000; Unarmed 0, Broadsword 390, Flametongue 4,000; Excalibur, Gendarme and the Genji Shield 1; Ribbon 10 |
| `+0x07` bit 1 | set on 21 rows: Hero's Blade, Treaty-Blade, Sword of Kings, Joyeuse, Chirijiraden, both Nightmare rows, Flimsy Blade, Manufacted Nethicite, Goddess's Magicite, Dawn Shard and ten Reserve rows (the `cannot_sell` column of [`equipment-list.tsv`](equipment-list.tsv)) |
| `+0x10` | 0 on 260 rows, 1 on 72, 2 on 84, 3 on 1, 5 on 3 |
| `+0x18` on weapons | 10 on 144, 100 on 42, 20 on 10, 30 on 3, 200 on 1 |
| `+0x19` on weapons | 20-29, and 104 on maces |
| `+0x1A` on weapons and ammunition | 1 to 224 |
| `+0x27` on weapons | 10 to 99 |

Flametongue, row 8: class 1, off hand 18, price 4,000, reach 10, recipe 20, Attack Power 45, knockback 10,
combo 5, weapon evade 5, element fire (`0x01`), charge base 32, bonus record 0, effect `0x8003`, model
`0x770020`. Ribbon, row 385: class 22, slot 4, price 10, Defense 1, Magick Resist 1, no augment, bonus record
4200, which holds Regen and Libra and protects from Petrify, Stop, Sleep, Confuse, Doom, Blind, Poison, Silence,
Sap, Oil, Disable, Immobilize, Slow and Disease.

## Loader behaviour

1. `0x00236C30` passes the directory entry `+0x38` to `0x00238160` (`0x00236D73`).
2. `0x00238160` binds `0x02EBF0F8` to the section through `0x003845F0`, which rebases the header's rows offset `+0x0C`
   and bonus offset `+0x18` by the section address (`0x0038460E`, `0x0038462F`).
3. It then rewrites every row's `+0x28` to the encoded address of its bonus record, header `+0x18` plus the stored
   offset (`0x00238225`-`0x0023823E`). Nothing else writes a row.

### What the load checks

The load makes three tests, none of them on the file's contents:

- `0x00384420` files no request when `0x0032E400` gives the file a negative size (`0x00384453`-`0x00384459`); the size
  read comes from that size table, not from the file.
- `0x003845F0` leaves the slot null when the section entry is null (`0x003845F7`-`0x003845FA`), and rebases a header
  offset only when it is not 0 (`0x0038460A`, `0x0038461A`, `0x0038462B`, `0x0038463C`).
- `0x00238160` rewrites rows up to the header's row count `+0x04` (`0x00238190`-`0x0023819E`).

The load never checks the `st2e` magic, the stride, the row count against the section's size, or that a row's
`+0x28` lands inside the bonus records. `0x00238850`, `0x003846F0`, `0x00236C30`, `0x003845F0` and `0x00238160` read no row
field other than `+0x28`. The four bytes `st2e` occur nowhere in the image.

Of the header reads made through the registry slots, listed one by one on
[Authored data tables](../Game-Files-And-Data-Tables/authored-data-tables.md), none is at `+0x00`. All 562 reads
of `+0x08` are `movzx` loads that feed the row formula or its inverse (21 divide an offset by the stride), and none
is compared.

## Modding notes

- Price is `+0x12`; making an item unsellable is `+0x07` bit 1.
- A weapon's damage formula is `+0x19`; its element `+0x1E`; its on-hit statuses `+0x1F` and `+0x20`.
- The class `+0x09` decides how the game reads `+0x18`-`+0x1A`: a row moved to another group changes meaning.
- To let a two-handed weapon take a shield, set its `+0x11` to 18. A value of 23 or above, or -1, makes combat read
  the element and statuses from whatever is in the off hand.
- Bonuses that every item can carry, stats, held statuses, immunities and elements, live in the bonus record, so
  two rows can share one record.

## Related

- [Stats](../Damage-And-Battle-Formulas/stats.md) - what the groups and the bonus record add.
- [Augments](../Damage-And-Battle-Formulas/augments.md) - the augment byte of armor and accessories.
- [Elements](../Damage-And-Battle-Formulas/elements.md) - the element bytes.
- [Weapon formulas](../Damage-And-Battle-Formulas/weapon-formulas.md) - recipe, knockback, combo and statuses.
