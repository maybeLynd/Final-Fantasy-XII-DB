---
title: "Action definition row: power, targeting, range, element and flag fields of a battle action"
kind: "format"
category: "Battle actions"
addresses: "0x00237FC0, 0x00236C30, 0x00238850, 0x003845F0, 0x0020E600, 0x00385F60, 0x0031C5D0, 0x0031EB20, 0x00390AB0"
---

## What the player sees

Every command that does something in battle is one row of one table: Attack, each magick and
technick, each item use, each summon, Quickening and Concurrence, each Foecraft move, and the traps.
The row decides what the action costs, how long it charges, how far it reaches, what it can target,
how wide its area is, how strong it is, its element, the statuses it inflicts and where it sits in the
command list. The name and help text are in the text banks, and the row holds their ids.

## Where it comes from

The rows are section 14 of `battle_pack.bin`, the section its directory entry at file offset `+0x3C`
points to. The section is an `st2e` table of 543 rows, 60 bytes each, starting `0x20` bytes into the
section. In the `us` file the section is at `0x13210`. Row *n* is action id *n*: Cure is row 0,
Attack row 150, Steal row 169.

Every reader computes the row itself rather than calling a getter (`0x0038B248`-`0x0038B28E` is one
example). It loads the registry slot `0x02EBF138`, resolves the slot's `+0x0C` through `0x0020E600` to
the first row, and adds the action id times the slot's `u16` stride at `+0x08`. While a recipe runs,
the action id is the formula scratch word `0x02AEDFD4`.

## Layouts

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u16` | helpId | help text id; 4000 = none (`0x0031C5D0` at `0x0031DBB1`, through `0x002F9860`) |
| `+0x02` | `u8` | rangeNear | near range band, tenths; used when `+0x0C` bit 26 is clear (`0x00320D70`) |
| `+0x03` | `u8` | rangeMiddle | middle range band, tenths (`0x00320D70`) |
| `+0x04` | `u8` | knockback | knockback chance base (`0x00388B50` at `0x00388BE6`) |
| `+0x05` | `u8` | reach | reach in tenths; bounds the Reflect retarget (`0x00309300`, `0x00384F40`) |
| `+0x06` | `u8` | areaRadius | area radius; 0 = the target alone (`0x0030D160`, `0x0031A990`) |
| `+0x07` | `u8` | areaAngle | cone half-angle in degrees, or line half-width (`0x0030D160`, `0x0031A990`) |
| `+0x08` | `u8` | recipe | damage recipe; 0 = the weapon's (`0x00385F60` at `0x0038617E`) |
| `+0x09` | `u8` | chargeBase | charge time base (`0x002F8410` at `0x002F8586`) |
| `+0x0A` | `u8` | cost | MP cost, or Mist charges for kinds 5 and 6 (`0x002F95D0`, `0x00308FF0`, `0x00309110`) |
| `+0x0B` | `u8` | b0B | 1-3 on rows 182-207 only |
| `+0x0C` | `u32` | flags | action flags; table below |
| `+0x10` | `u8` | power | action power (31 formula slots) |
| `+0x11` | `u8` | power2 | second power byte (`0x00388C10`, `0x0038A9D0`, `0x0038EB30`) |
| `+0x12` | `u8` | hit | hit threshold into `0x02AEDFE0` (`0x00389040` at `0x00389089`) |
| `+0x13` | `u8` | element | one bit per element (`0x0038B220`, `0x0038B6A0`) |
| `+0x14` | `u8` | statusChance | on-hit status chance, percent (`0x0038F970` at `0x0038F9B0`) |
| `+0x15` | `u8` | boostPercent | percent added to the working magnitude `0x02AEE004` (`0x0038F8E0` at `0x0038F93B`) |
| `+0x16` | `u8[2]` | pad16 | 0 on every row |
| `+0x18` | `u32` | statusMask | statuses the action applies or removes, one bit each (`0x003872D0`, `0x003851F0`) |
| `+0x1C` | `u8` | category | action category 0-9; picks the presentation event (`0x0030A370` at `0x0030A37F`) |
| `+0x1D` | `u8` | enmityDirect | enmity toward the user (`0x003216E0` at `0x00321716`) |
| `+0x1E` | `u8` | kind | action kind; picks what `+0x22` holds (`0x003093D0`, `0x00469EC0`) |
| `+0x1F` | `u8` | enmitySpread | enmity passed to foes already hostile (`0x00321733`) |
| `+0x20` | `u8` | enmityOthers | enmity taken from the others, negated (`0x00321744`) |
| `+0x21` | `u8` | effectClass | 0-8, picks an effect started while the action runs (`0x00329F80` at `0x00329FE7`) |
| `+0x22` | `u16` | linkedId | the magick, technick, item or ability id of the row (`0x003093D0`, `0x003060E0`) |
| `+0x24` | `u16` | effectId | the action's own effect id; bit 15 a flag (`0x0030AC50`, `0x0030A190`, `0x00310DB0`) |
| `+0x26` | `u8` | esper | the Esper's row in the party table, on the 13 summon rows (`0x00306760`) |
| `+0x27` | `u8` | pad27 | 0 on every row |
| `+0x28` | `u16` | cinematicId | Quickening and Concurrence cinematic (`0x0030A190` at `0x0030A209`) |
| `+0x2A` | `u16` | pad2A | 0 on every row |
| `+0x2C` | `u16` | flags2 | second flag word; table below |
| `+0x2E` | `u16` | descId | description text id (`0x0031C5D0` at `0x0031DBBE`) |
| `+0x30` | `u32` | event | presentation event of phases 9-11 (`0x0030A370` at `0x0030A457`) |
| `+0x34` | `u16` | nameWord | name: bank = word >> 11, entry = word & `0x7FF` (`0x00305F10`, `0x00536410`) |
| `+0x36` | `u16` | targetFlags | third flag word; table below |
| `+0x38` | `u8` | menuPage | command list page (`0x00237FC0` at `0x00238033`) |
| `+0x39` | `u8` | menuRow | row on that page (`0x00237FC0` at `0x00238043`) |
| `+0x3A` | `u8` | aiReaction | bit number set in the AI operand mask of kind 10 (`0x00312170` at `0x003121F5`) |
| `+0x3B` | `u8` | pad3B | 0 on every row |

### The kind byte

Byte `+0x1E` is the action's kind ([Command availability](command-availability.md) has the
ownership rule for each):

| Kind | Rows | Examples |
|---:|---:|---|
| `0` | 1 | Attack |
| `1` | 81 | magicks: Cure, Blindna |
| `2` | 24 | technicks: First Aid, Charge |
| `3` | 51 | items: Potion, Ether |
| `5` | 13 | summons: Belias, Mateus |
| `6` | 18 | Quickenings: Red Spiral, White Whorl |
| `7` | 235 | Foecraft: Fear, Aerora |
| `8` | 16 | traps: explosion, choking gas |
| `9` | 26 | Esper attacks: Painflare, Hellfire |
| `10` | 16 | Concurrences: Inferno, Torrent |
| `13`, `14`, `16`, `17` | 3, 1, 1, 1 | the Reserve rows 155-157, `actstop`, `escape`, `escapestop` |
| `255` | 56 | 47 `NOT USED` and Reserve rows; nine named rows with no linked id: `Do nothing.`, Mount, Dismount, `sousachange`, Mist Charge (3), Chain Bonus, Dismiss |

### The element byte

Bit *n* of `+0x13` is one element; no shipped row sets more than one:

| Bit | Rows | Examples |
|---:|---:|---|
| `0` | 19 | Fire, Fira, Firaga |
| `1` | 11 | Thunder, Thundara |
| `2` | 10 | Blizzard, Blizzara |
| `3` | 8 | Quakeja, Tremor |
| `4` | 13 | Aqua, Aquara |
| `5` | 13 | Aero, Aeroga |
| `6` | 9 | Holy, Holyja |
| `7` | 13 | Dark, Darkra |

### The flag word at +0x0C

| Bit | Rows | Effect (reader) |
|---:|---:|---|
| `0`, `2`, `3` | 71, 341, 416 | the user, allies and foes can be targeted ([Target selection](target-selection.md); `0x003230E0`, `0x0031EB20`) |
| `1` | 13 | the area is the whole party ([Area of effect](area-of-effect.md); `0x0030D461`) |
| `4` | 32 | sets bit 10 of the command entry (`0x0031F0A4`-`0x0031F0AF`) |
| `5`, `6` | 22, 103 | how the target list is built ([Target selection](target-selection.md); `0x00322BD5`-`0x00322BED`) |
| `8`, `9` | 186, 378 | copied to the query record's `+0x20` (`0x0031DB9E`-`0x0031DBA7`) |
| `11` | 57 | clears bit 5 of the result's byte `+0` (`0x00386079`); also read by `0x0031AA30` (`0x0031AB02`) |
| `12` | 18 | the shape reader reports the whole party or no area, whatever the radius (`0x0031A990`) |
| `13` | 162 | magick class: a target with augment 56 (Magick-Immunity) voids it as result kind 7 (`0x00390EE5`, `0x003910C3`); no charge time under augment 54 (Swiftcast) (`0x002F8689`) |
| `14` | 207 | physical class: augment 55 (Physical-Immunity) voids it as result kind 7 (`0x00390E9A`, `0x00391076`) |
| `16` | 78 | Reflect (status 23) bounces it: result kind 8 and a new target from `0x00384F40` (`0x00390D7F`, `0x00390DF1`-`0x00390E42`) |
| `17` | 28 | runs the special-guard roll (`0x00388058`) |
| `19` | 97 | Silence blocks it (`0x002FFE56`, [Command availability](command-availability.md)) |
| `21` | 26 | the area is centred on the user ([Area of effect](area-of-effect.md); `0x0030D271`) |
| `24`, `25` | 49, 5 | the area is a cone or a line ([Area of effect](area-of-effect.md); `0x0030D2C0`) |
| `26` | 35 | the weapon's reach and range bands replace the row's ([Action range](action-range.md); `0x00309377`, `0x00320D74`, `0x00390C7F`) |
| `27` | 1 | the charge base comes from the weapon row's `+0x27` (`0x002F8494`, [Action phases](action-phases.md)) |
| `28` | 36 | changes the command entry (`0x0031F0EF`, `0x0031F157`) |
| `29` | 112 | the command entry carries a cost (`0x0031F000`) |
| `30` | 87 | runs a scene: summon, Quickening, Concurrence ([Quickenings and summons](quickenings-and-summons.md); 17 sites, `0x00304D3F` among them) |
| `31` | 64 | consumes an item: the command entry carries the item count (`0x0031F077`) |

Bits 13 and 14 are also copied into the kind-10 AI operand mask as its bits 8 and 9 (`0x00312213`-`0x00312232`).
Bits 7, 10, 15, 18 and 20 are set on 324, 292, 24, 1 (Attack) and 81 rows and are read by no instruction. The 60
instructions that read the word test other bits; those that take it whole keep bit 13 (`0x0030770D`, masked by a
0-or-1 register; `0x002F8689`), bits 13 and 14 (`0x00312213`), bits 24 and 25 (`0x0030D3AE`), bits 12, 21, 24 and 25
(`0x0031A99A`), bit 27 (`0x002F8494`), bits 8 and 9 (`0x0031DB9E`), bits 5 and 6 (`0x00322BD5`) or bit 31 (`0x0031F077`).
No shipped row sets bits 22 or 23.

### The flag word at +0x2C

| Bit | Rows | Effect (reader) |
|---:|---:|---|
| `0`-`2` | 70 | a value 0-5; for kind-1 rows, values 0-4 pick which of five magick lists the row joins (`0x002376F0` at `0x002377FF`, `0x00237881`); 5 is only on row 81, `NOT USED` |
| `3` | 21 | the user gains MP from the damage when it has augment 86 (Inquisitor) (`0x002F92C1`, `0x002F9323`) |
| `4` | 40 | the user gains MP from the damage when it has augment 20 (Warmage) (`0x002F9330`-`0x002F937B`) |
| `6`, `7` | 10, 2 | the action may target a KO or a Stone unit ([Target selection](target-selection.md); `0x002FFAF5`, `0x002FFB30`) |
| `8` | 61 | the effect test of `0x0030CA80` is skipped (`0x0030CB71`) |
| `10`, `11` | 195, 65 | the target wakes from Sleep and loses Confuse, or loses Invisible (`0x00390F20` at `0x00391112`, `0x00391192`) |
| `13` | 98 | no License needed ([Command availability](command-availability.md); `0x00323F52`) |
| `14` | 93 | returned by `0x0030BB30` for categories 1-8 (`0x0030BC0C`) |

Bits 9, 12 and 15 (3, 20 and 10 rows) are read through the whole word by the AI order selectors
(`0x00303434`, `0x00303492`, `0x00308CF2`) and by `0x003851F0` and `0x003872D0` (`0x003852AB`, `0x00387382`).

Bit 5 is set on 227 rows and is read by no instruction. The 44 instructions that read the byte `+0x2C` or the
word test or keep other bits: bits 0-2 (`0x002377FF`, `0x00237885`, `0x00300B3F`, `0x00317CFF`, `0x0031CDC2`, `0x0031EF87`,
`0x0032A46F` among them), bits 3 and 4 (`0x002F9323`, `0x002F9377`), bits 6 and 7 (`0x002FFAF5`, `0x002FFB30`, `0x00322B67`,
`0x00322B78` among them) and bits 8-15 (the word tests above, `0x0030847E`, `0x003084B8`, `0x00308CFB`, `0x00308D02`,
`0x0030BC10`).

### The flag word at +0x36

| Bit | Rows | Effect (reader) |
|---:|---:|---|
| `0` | 51 | the action adds statuses: `0x003875D0` returns the mask `+0x18` only with it set and bit 9 of `+0x2C` clear (`0x00387629`); the gambit target picker passes over a unit that already has them all ([Gambit conditions](../Enemy-AI-And-Gambits/gambit-conditions.md); `0x0030856F`) |
| `1` | 26 | the action removes statuses: tested by `0x003872D0` (`0x00387331`); the gambit target picker passes over a unit that has none of them (`0x003084EF`) |
| `2` | 2 | the area takes the side opposite the target (Self-Sacrifice, Self-Destruct; `0x0030D36C`) |
| `3` | 1 | the area takes everyone (Mass-Destruct; `0x0030D36C`) |
| `4` | 227 | when clear, one branch of the pre-resolution gates fails the result (`0x00390D55`-`0x00390D63`) |
| `5` | 14 | the gambit target picker keeps a candidate whose byte `+0x55` is `0x0D` without testing what the action would change (`0x0030844B`-`0x00308457`) |

## Shipped data

| Field offset | Values in the 543 rows |
|---|---|
| `+0x02`, `+0x03` | 0 on 537 rows; `+0x02` is 1 on five rows and 20 on one, `+0x03` 20 on four and 15 on two |
| `+0x05` | 100 × 212, 0 × 130, 30 × 56, 20 × 50, 255 × 39 |
| `+0x06` | 0 × 296, 10 × 98, 8 × 63, 6 × 46, 100 × 13 |
| `+0x07` | 0 × 490, 180 × 33, 60 × 7, 75 × 3 |
| `+0x09` | 0 × 212, 3 × 149, 23 × 81, 1 × 32, 2 × 24; at most 60 |
| `+0x0A` | 0 × 397, 2 × 23, 3 × 14, 8 × 12; at most 72; Cure 8 |
| `+0x10` | 0 × 242, 100 × 36, 90 × 15; at most 253; Cure 20, Fira 67 |
| `+0x12` | 100 × 312, 0 × 157 |
| `+0x14` | 0 × 494; 100 on Bio, 35 on Firaja, 50 on Darkja |
| `+0x15`, `+0x16`, `+0x17`, `+0x27`, `+0x2A`, `+0x3B` | 0 on every row |
| `+0x18` | 0 × 387; Blindna `0x80`, Poisona `0x100`, Raise `0x1` |
| `+0x22` | `0xFFFF` × 343; 200 distinct ids |
| `+0x26` | 27-39 on the summons Belias to Zodiark, 0 elsewhere |
| `+0x28` | 120-153 on the 26 Quickening and Concurrence rows (Red Spiral 120) |
| `+0x34` | the row's own number, except rows 128-142, which hold 136, 137, 128, 129, 130, 138, 139, 140, 141, 135, 142, 131, 132, 133, 134 |
| `+0x38`, `+0x39` | `0xFF` on 386 rows; Attack 0 / 0, Cure 1 / 0, Cura 1 / 1, Fira 2 / 9 |
| `+0x3A` | 255 × 475; 15 × 49, 16 on Cure to Curaja and the Potions |

Cure's row, as stored:

```
a1 0f 00 00 00 64 00 00 04 17 08 00 4c 2d 19 30 14 00 00 00 00 00 00 00 00 00 00 00 01 0c 01 02
04 01 00 30 b3 00 00 00 00 00 00 00 30 10 10 27 00 00 00 00 00 00 30 00 01 00 10 00
```

## Loader behaviour

The table arrives with the battle data resource:

1. `BattleStorage_InitializeWorkArrays` registers `0x00238850` as the handler for resource `0x13`,
   named `STATIC` (`0x002369BB`-`0x002369CE`).
2. On delivery `0x00238850` stores the blob pointer in `0x0208E680` and jumps to `0x00236C30(1)`
   (`0x0023885A`-`0x0023886F`).
3. `0x00236C30` binds the battle tables from the blob's directory and calls `0x00237FC0` with entry
   `+0x3C` (`0x00236D7B`-`0x00236D85`).
4. `0x00237FC0` binds `0x02EBF138` to that section through `0x003845F0` (`0x00237FD5`-`0x00237FDE`), which
   stores the section pointer and rebases the header's offsets at `+0x0C`, `+0x10`, `+0x18` and
   `+0x1C` by the section address (`0x003845F4`-`0x00384640`).
5. It then walks every row once and files each row with both `+0x38` and `+0x39` set into the
   command grid at `0x0208D308` (`0x00238033`-`0x00238132`).

## Modding notes

- Power is `+0x10`, hit rate `+0x12`, status chance `+0x14`, statuses `+0x18` and element `+0x13`.
- `+0x08` re-routes the whole damage formula; 0 hands it to the equipped weapon.
- The MP cost is the byte `+0x0A`, before the augment adjustments of `0x002F95D0`.
- The name is not in the row: `+0x34` points into the text bank, so two rows can share a name.
- `+0x15` is a working percent boost that no shipped row uses.

## Related

- [Action range](action-range.md) - `+0x02`, `+0x03`, `+0x05` and flag bit 26.
- [Area of effect](area-of-effect.md) - `+0x06`, `+0x07` and the area flags.
- [Target selection](target-selection.md) - the target flags of `+0x0C` and `+0x2C`.
- [Command availability](command-availability.md) - kinds, costs, Silence and the License bit.
- [Action phases](action-phases.md) - the charge base and the scene flag.
- [Quickenings and summons](quickenings-and-summons.md) - `+0x26` and the scene rows.
- [Steal](../Damage-And-Battle-Formulas/steal.md) - one recipe from `+0x08` end to end.
