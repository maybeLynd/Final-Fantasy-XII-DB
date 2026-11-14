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

Each piece of equipment is one row of numbers in `battle_pack.bin`, and the row points to a separate bonus record with
its extra stats, statuses and elements, so two rows can share one record. The row's class decides whether three of its
numbers mean a weapon's reach, damage formula and Attack, a shield's two evades, or armor's Defense, Magick Resist and
augment.

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
| `+0x07` | `u8` | slotFlags | mask `0xE0` slot, bit `0x10` no license, bit `0x4` hits flying, bit `0x2` cannot sell; table below |
| `+0x08` | `u8` | ordinal | order of the row inside its class (`0x0031C9CB`) |
| `+0x09` | `u8` | class | equipment class 0-26; sets the group and the pairing (`0x0031E9F0`) |
| `+0x0A` | `u32` | pad0A | 0 on every row |
| `+0x0E` | `u16` | helpId | extra text id, through `0x002F9860` (`0x0031C9B0`); 0 on every row |
| `+0x10` | `u8` | chargeWeight | summed over the five equipped items to slow the charge while battle flag `0x022C314C` bit `0x40` is set (`0x002F9C00`) |
| `+0x11` | `i8` | offHandClass | the class an off-hand item must have; -1 for no class (`0x002F7EC0`, `0x00317930`) |
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
| `+0x24` | `u8` | b24 | weapons: 0, 3, 5, 7, 8 or 10; 0 on every other row; read by no instruction, so it has no effect (below) |
| `+0x25` | `u8` | reachKind | weapons: which range pair sets the near and middle distance (`0x00320D70` at `0x00320D93`) |
| `+0x26` | `u8` | motionClass | weapons: attack motion class, through the map at `0x02EBF180`, main-hand rows only (`0x003203B0` at `0x0032041E`) |
| `+0x27` | `u8` | chargeBase | weapons: charge time base for actions with flag `+0x0C` bit `0x8000000` (`0x002F8410` at `0x002F851A`) |
| `+0x28` | `u32` | bonusRecord | offset of the bonus record from section offset `0x7144`, 0-4200; rebased at load (`0x0023823E`) |
| `+0x2C` | `u16` | attackEffect | weapons: low 15 bits = the effect a plain Attack shows (`0x0030AC50` at `0x0030AD56`) |
| `+0x2E` | `u16` | pad2E | 0 on every row |
| `+0x30` | `u32` | modelId | weapons, ammunition and shields: the held model, 0x0077xxxx (`0x0031BF60` at `0x0031BFE0`) |

Byte `+0x24` is read nowhere in the game. Every row is reached from the slot `0x02EBF0F8`, whose only references
are rip-relative; the row pointers those readers compute go only into registers, the stack and the callees
they are passed to, such as `0x0031E9F0` (`+0x09`) and `0x00320D70` (`+0x25`), and none of them reads a byte that
covers `+0x24`. No row pointer is stored in memory outside the stack, and no row is copied whole.

`0x0030AC50(action id, weapon id)` takes both ids as words. The action row is looked up only when
`0x00322C50(0x14, id, 0)` answers non-zero, the weapon row only when `0x00322C50(6, id, 0)` does; a row
whose slot (`0x02EBF138`, `0x02EBF0F8`) or whose `0x0020E600` answer is null counts as missing
(`0x0030AC5F`-`0x0030AD09`). The weapon row index is the id less `0x1000` (`0x0030ACFE`). With no action row
the answer is -1 (`0x0030AD0B`-`0x0030AD0E`, `0x0030AD6E`-`0x0030AD73`).

When the action row's word `+0x24` is not `0xFFFF`, has bit `0x8000` and the row's dword `+0x0C` lacks
bit `0x40000000`, the answer is that word's low 15 bits (`0x0030AD10`-`0x0030AD2F`). When the word is
`0xFFFF`, the weapon row exists and `+0x0C` lacks the bit, the answer is the low 15 bits of the
weapon row's word `+0x2C` (`0x0030AD43`-`0x0030AD5A`). Every other case answers -1, among them a word
`+0x24` without bit `0x8000` (`0x0030AD48`-`0x0030AD4B`, `0x0030AD73`).

The bonus record is 24 bytes:

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
| mask `0xE0` | the slot, `(+0x07 & 0xE0) >> 5`: 0 main hand, 1 off hand (shields and ammunition), 2 head, 3 body, 4 accessory | the slot test `0x00317930` (`0x00317A18`), Optimise `0x002F7A10` (`0x002F7A87`), the shop classifier `0x002FABD0` (`0x002FAC9D`) |
| `0x10` | needs no license | the license test skips the item (`0x00323CDF`) |
| `0x4` | reaches flying targets | `0x00390CF6` for weapon actions, formula slot 12 (`0x0038895B`) |
| `0x2` | cannot be sold | copied to the query record `+0x54` bit `0x1` (`0x0031CA3C`-`0x0031CA47`), which the shop turns into price bit `0x80000000` (`0x0057DED0`) |
| `0x1`, `0x8` | not set on any row | - |

### The class byte and the group

`0x0031E9F0` maps the class `+0x09` through the 27 bytes at `0x0031EA74` and the jump table at `0x0031EA50` to a
category 1-9, or 0 for a class above 26 (`0x0031EA4A`), and `0x0031E9A0` folds the category into the group, 0 for
category 0 (`0x0031E9A0`-`0x0031E9DD`). The group decides what
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
| 7, 8, 9 | 19, 20, 21-22 | `3` | Defense | Magick Resist | augment, `0xFF` for no augment |

Reach is in tenths (`0x00309300` at `0x0030938B`); the recipe is the plain Attack's damage formula (`0x00385F60` at
`0x003861FD`, [Weapon formulas](../Damage-And-Battle-Formulas/weapon-formulas.md)); the augment is the one the item gives
(`0x0030FED0` at `0x003100EF`, [Augments](../Damage-And-Battle-Formulas/augments.md)).

Most combat readers do not test the group: they read the weapon fields of the main-hand item, stats `+0x50`. They
read the element, status chance and statuses from the off-hand item instead when the weapon's `+0x11` is 23 or
above as an unsigned byte (`0x0038BEDE`, `0x0038FA54`, `0x00384D09`). That includes the -1 of two-handed weapons, whose
off hand is empty, so they fall back to the weapon's own fields.

### Pairing

The off-hand item's class must equal the main-hand item's `+0x11` (`0x002F7EC0` at `0x002F7F70`-`0x002F7F76`).
`0x002F7EC0(off, main)` answers 1 at once when either word is empty, `0xFFFF` (`0x002F7ED5`-`0x002F7EED`), and 0 with no
equipment table bound (`0x002F7EEF`-`0x002F7EF9`, `0x002F7F87`). The
shipped rows use 18, a shield, on one-handed weapons, 23-26 on the four ammunition weapons, and -1 elsewhere, so
two-handed weapons take nothing in the off hand.

## Shipped data

| Class | Category | Rows | Off hand | First items |
|---|---|---:|---|---|
| `0` | 1 | 11 | 18 or -1 | Unarmed |
| `1` | 2 | 27 | 18 | Broadsword, Longsword, Iron Sword |
| `2` | 3 | 13 | -1 | Claymore, Defender, Save the Queen |
| `3` | 3 | 10 | -1 | Kotetsu, Osafune, Kogarasumaru |
| `4` | 3 | 8 | -1 | Ashura, Sakura-saezuri, Kagenui |
| `5` | 3 | 15 | -1 | Javelin, Spear, Partisan |
| `6` | 3 | 13 | -1 | Oaken Pole, Cypress Pole, Battle Bamboo |
| `7` | 4 | 16 | 23 | Shortbow, Silver Bow, Aevis Killer |
| `8` | 4 | 9 | 24 | Bowgun, Crossbow, Paramina Crossbow |
| `9` | 4 | 12 | 25 | Altair, Capella, Vega |
| `10` | 2 | 7 | 18 | Handaxe, Broadaxe, Slasher |
| `11` | 2 | 6 | 18 | Iron Hammer, War Hammer, Sledgehammer |
| `12` | 2 | 12 | 18 | Dagger, Mage Masher, Assassin's Dagger |
| `13` | 3 | 8 | -1 | Rod, Serpent Rod, Healing Rod |
| `14` | 3 | 10 | -1 | Oak Staff, Cherry Staff, Wizard's Staff |
| `15` | 2 | 11 | 18 | Mace, Bronze Mace, Bhuj |
| `16` | 2 | 6 | 18 | Gilt Measure, Arc Scale, Multiscale |
| `17` | 4 | 6 | 26 | Hornito, Fumarole, Tumulus |
| `18` | 6 | 20 | -1 | Gendarme, Leather Shield, Buckler |
| `19` | 7 | 60 | -1 | Leather Cap, Headgear, Headguard |
| `20` | 8 | 60 | -1 | Leather Clothing, Chromed Leathers, Leather Breastplate |
| `21` | 9 | 42 | -1 | Opal Ring, Ruby Ring, Tourmaline Ring |
| `22` | 9 | 6 | -1 | Manufacted Nethicite, Cat-ear Hood, Fuzzy Miter |
| `23` | 5 | 8 | -1 | Onion Arrows, Parallel Arrows, Fiery Arrows |
| `24` | 5 | 8 | -1 | Onion Bolts, Long Bolts, Stone Bolts |
| `25` | 5 | 8 | -1 | Onion Shot, Silent Shot, Aqua Shot |
| `26` | 5 | 8 | -1 | Onion Bombs, Poison Bombs, Stun Bombs |

The rows count ids `0x1000`-`0x11A3`, and the names are each row's own name word. Rows 420-556, named "NOT USED"
and "Reserve", lie past the inventory's counts, so the party cannot hold them, but 124 of them are equipped.

- Enemies: 958 of the 1,146 enemy definitions put one of 97 rows in the main hand `+0x16`, and 36 put one of 12
  other rows in the off hand `+0x1C`; `0x0023AC80` installs both (`0x0023ADA8`, `0x0023ADBA`).
- Guests: Lamont, Larsa and Reddas carry rows 468, 469, 484 and 485 from the party table (`+0x0A`-`+0x13`,
  `0x0023AE8C`-`0x0023AEDA`) and the scenario presets (`+0x04`-`+0x0D`, `0x00239C62`-`0x00239CBF`).
- Espers: the 13 "Reserve" rows 179-191 are the main hands of the 13 Espers and rows 544-556 their body pieces, one
  each, and Shemhazai holds row 459 in the off hand.
- Reserve: rows 440, 444-449, 462-464, 486, 490 and 491 have no reference in the area files, `battle_pack.bin` (party
  table, scenario presets, shops, bazaar, reward packages and selectors, licenses, starting inventory), the
  chests and other records of the shipped scripts, or an immediate of the executable.

| Field | Values in rows 0-419 |
|---|---|
| `+0x12` price | 0 to 56,000; Unarmed 0, Broadsword 390, Flametongue 4,000; 1 on 34 of the rows below 420, among them Excalibur, Gendarme, the Genji Shield and the 13 Reserve rows, and on every `NOT USED` row from 420 on; Ribbon 10 |
| `+0x07` bit `0x2` | set on 21 rows: Hero's Blade, Treaty-Blade, Sword of Kings, Joyeuse, Chirijiraden, both Nightmare rows, Flimsy Blade, Manufacted Nethicite, Goddess's Magicite, Dawn Shard and ten Reserve rows (the `cannot_sell` column of [`equipment-list.tsv`](equipment-list.tsv)) |
| `+0x10` | 0 on 260 rows, 1 on 72, 2 on 84, 3 on 1, 5 on 3 |
| `+0x18` on weapons | 10 on 144, 100 on 42, 20 on 10, 30 on 3, 200 on 1 |
| `+0x19` on weapons | 20-29, and 104 on ten of the eleven maces and on Joyeuse below row 420, and on the `NOT USED` rows 463-466 (class 15); the mace Bonebreaker has 27 |
| `+0x1A` on weapons and ammunition | 1 to 224 |
| `+0x27` on weapons | 10 to 99 |

Flametongue, row 8: class 1, off hand 18, price 4,000, reach 10, recipe 20, Attack Power 45, knockback 10,
combo 5, weapon evade 5, element fire (`0x01`), charge base 32, bonus record 0, effect `0x8003`, model
`0x770020`. Ribbon, row 385: class 22, slot 4, price 10, Defense 1, Magick Resist 1, no augment, bonus record
offset 4200 (record 175), which holds Regen and Libra and protects from Petrify, Stop, Sleep, Confuse, Doom, Blind, Poison, Silence,
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
[Authored data tables](../Game-Files-And-Data-Tables/authored-data-tables.md), no read is at `+0x00`. All 562 reads
of `+0x08` are `movzx` loads that feed the row formula or its inverse (21 divide an offset by the stride), and no read
is compared.

## Modding notes

- Price is `+0x12`; making an item unsellable is `+0x07` bit `0x2`.
- Changing `+0x24` changes nothing: no code reads it.
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

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Actor entity: `0x0032E400` is called by `0x0032FCA0`, `0x00330310`, `0x003306E0`; those functions are documented on
  [frame update order](../Engine-Core/frame-update-order.md),
  [zone changes and mapjump](../World-Areas-And-Travel/zone-changes-and-mapjump.md),
  [ps2data bin families](../Game-Files-And-Data-Tables/ps2data-bin-families.md).
- Save load settings: `0x00235E90` is called by `0x00253A80`; those functions are documented on
  [frame update order](../Engine-Core/frame-update-order.md).
- Script VM: `0x0032E400` is called by `0x0050DF70`.
