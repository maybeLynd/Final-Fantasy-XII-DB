[Home](../../README.md) / [Damage and battle formulas](README.md) / Augment list

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Augment list: every augment with its name, text, value, the code that reads the value, and its timer | reference | Damage and battle formulas | Stats, HP and augments | All 129 rows of the shipped augment table (ability_data) in battle_pack.bin, decoded field by field: the augment id, its shipped name and extra text, the value at +0x04 with the function that reads it and what it does with it (stat bonuses, MP-cost and charge-time percentages, shield block, the Potion, Ether and Phoenix Down lores), the timer slot of the three timed effects, and a one-line explanation. | 0x02EBF040, 0x0031C5D0, 0x002FEF30, 0x002F95D0, 0x002F8410, 0x00387FD0, 0x0038DD20, 0x0038DF00, 0x0038E2D0, 0x0030EA40 |

## What it lists

[`augment-list.tsv`](augment-list.tsv) holds one line for each of the 129 rows of the augment table that registry slot `0x02EBF040`
reaches (`battle_pack.bin` directory entry `+0xEC`). Row *n* is augment id *n*, the id whose bit
[Augments](augments.md) sets in a unit's two augment layers.

- 89 rows carry a shipped name and 40 are named `NOT USED`. 19 of those 40 have no other text: 17 have an empty
  text and rows 33 and 34 the text `NOT USED`. Three of the 19 are the timed effects 55-57.
- 77 rows have a non-zero value at `+0x04`. 63 are read by a function that picks the row by number, 3 are the
  default timers of the three timed effects, and 11 (the ten gambit-slot rows 104-113 and row 128) are read by no
  instruction (below).

### The name of each augment

The `term` column is the name every catalogue in the database uses for an augment (the party table, the
bestiary, the enemy orders):

- **88 augments are granted by a license**, and the license's name is the game's name for them: Brawler (9),
  Martyr (21), Battle Lore, Magick Lore, Potion Lore and the rest. Each is granted by exactly one license.
- **Which licenses grant augments.** License data (entry `+0x34`) grants augment rows through its node types 15 to
  18 (byte `+0x05`: types 15-17 are group `0x1B` and 18 group `0x1C` in `0x003241D0`'s table `0x00324260`, both class
  2 in `0x00323890`). Type 30, the Second Board node 360, names augment 128, Second Board: it is group `0x1E`, class 3, so the
  rebuild never applies it as an augment.
- **The other 41 have no license.** They are the augments only equipment, a party table row or a foe's script
  gives, such as the Steel Poleyns' (37) or the Esper rows' (18, 31).
- **Lobbying (12)**, the Cat-ear Hood's, is the one of the 41 with an English name word, "Converts license points
  to gil.". The other 40 have no English name: the
  English, French, German, Italian and Spanish `battle_pack.bin` name them `NOT USED`, `Unused`, `dummy` or
  `DUMMY`, and the menus show only their help text.
- **The names the 41 go by.** They take the names the modding community uses for them, such as Tread Lightly (37),
  Safety (1) and Combo Boost (13). Rows 38 and 115, which have no community name, are Cartridge (the Japanese
  カートリッジ) and Reserve.
- **The Japanese build (`in`) names every row**, and `name_jp` keeps those names: 37 is トラップ回避, 1 セーフティ,
  13 殺陣.

`name` stays the English name word: for the licensed augments it is a sentence ("Increases attack power when
fighting empty-handed.").

### Where the values come from

Each line is read from the shipped files in these steps:

1. the `st2e` table at entry `+0xEC`: 129 rows of 8 bytes from the section's `+0x20`;
2. the name word `+0x02` through the word banks at entry `+0xF8`, and the text id `+0x00` through the text groups,
   both as `0x0031C5D0`'s class-29 arm reads them (`0x0031E494`-`0x0031E559`);
3. the reader of `+0x04` for each row, from the functions that load `0x02EBF040` (below);
4. every one-byte text code through the glyph table of the shipped `us` font `font00.dat`
   ([Fonts](../Menus-And-HUD/fonts.md));
5. the license that grants each augment, from the license table ([License list](../Items-Equipment-Shops-And-Licenses/license-list.md));
6. the Japanese name: the same name word in the `in` `battle_pack.bin`, decoded with the `jp` `font00.dat` as
   `0x002AC2F0` reads a code: a byte from `0x20` is glyph byte − `0x20`, and a lead byte `0x10`-`0x1F` with the next
   byte is glyph `[0x00916570 + 4 × (lead & 0xF)]` + next − `0x20` ([Fonts](../Menus-And-HUD/fonts.md)).

| Offset | Type | Field | Meaning |
|---|---|---|---|
| `+0x00` | `u16` | textId | an extra text, through `0x002F9860`; 0 for no text |
| `+0x02` | `u16` | nameWord | the name: bank 10, row = the augment id, on every row |
| `+0x04` | `u16` | value | the augment's number; its reader decides what it means (table below) |
| `+0x06` | `u8` | timerSlot | 3, 4 and 5 on ids 55-57, `0xFF` (no timer) on the others ([Battle buffs](../Status-Effects-And-KO/battle-buffs.md), `0x0030EA40`) |
| `+0x07` | `u8` | | 0 on every row |

The readers of `+0x04`:

| Rows | Reader | What the value does |
|---|---|---|
| 35, 42-47, 60-68 | `0x002FEF30` | added to Strength, [Stats](stats.md) (`0x002FF581`-`0x002FF77A`) |
| 19, 22, 24, 26, 69-73, 87, 97-102 | `0x002FEF30` | added to Magick Power, [Stats](stats.md) |
| 74-85 | `0x002FEF30` | added to max HP, [Stats](stats.md) |
| 91-93 | `0x002F95D0` | percent taken off an action's MP cost when the user has no augment 32 (`0x002F9674`-`0x002F9682`), for every action but the Quickenings and Esper summons of a record that is not an enemy (`0x002F9646`-`0x002F9667`): `cost = (int)(c - c / 100.0 * p)`, with `c` the action's byte `+0x0A` and `p` the sum of word `+0x04` of the rows 91-93 whose bits `0x8`, `0x10` and `0x20` of the user's bitset byte `+0x73` or `+0x83` are set (`0x002F96E5`-`0x002F97C1`) ([MP](../Status-Effects-And-KO/mp.md)) |
| 94-96 | `0x002F8410` | percent taken off the charge time ([Action phases](../Battle-Actions/action-phases.md)) |
| 3, 88-90 | `0x00387FD0`, `0x00389370` | added to the shield-block chance ([Damage formula](damage-formula.md)) |
| 119-121 | `0x0038DD20` | added to 100 percent of the heal it computes (`0x02AEE054` × `0x02AEE058`), for each of the user's bits 119-121 set in the bitset at its third argument's `+0x1A` (`0x0038DD3A`-`0x0038DE0B`). The heal is an HP gain, `0x02AEE008` (`0x0038DE95`); it is an HP loss, `0x02AEE004`, instead when one or all three of these hold: the context's target type `+0x18` is `0x0D` (Undead), the target has Reverse (context `+0x08` bit `0x1000`), the user has augment 15 (Medicine Reverse, `+0x1B` bit `0x80`) (`0x0038DE21`-`0x0038DECB`). A loss also sets the HP gain `0x02AEE008` to -1 (`0x0038DE82`, `0x0038DEA3`), except a loss from the target type alone, which leaves `0x02AEE008` as it was (`0x0038DE5E`-`0x0038DE64`, `0x0038DEAD`-`0x0038DEB1`); a gain with two of the three sets `0x02AEE004` to -1 (`0x0038DE70`, `0x0038DEB9`), and a gain with none of them leaves `0x02AEE004` as it was (`0x0038DE95`, `0x0038DEC5`-`0x0038DECB`). A loss, or with none of the three a loss an earlier slot left in `0x02AEE004`, marks the target in the user's hit mask through `0x00387B00` unless that value is -1 (`0x0038DED1`-`0x0038DEDC`) |
| 122-124 | `0x0038DF00` | the same, for bits 122-124, into `0x02AEE010` (`0x0038DF1A`-`0x0038DFEB`). It tests neither Reverse nor the target's type: with the user's augment 15 (Medicine Reverse, `+0x1B` bit `0x80`) it calls `0x00387B00`, which marks the target in the user's hit mask, and moves the value to the MP loss `0x02AEE00C`, setting `0x02AEE010` to -1 (`0x0038E001`, `0x0038E03A`-`0x0038E053`) |
| 125-127 | `0x0038E2D0` | added to the action's power `+0x10` for bits 125-127 (`0x0038E335`-`0x0038E3F6`), the percent of the target's max HP it restores; the sum is doubled when the user also has augment 14, Item Boost (`+0x1B` bit `0x40` of the bitset at its third argument's `+0x1A`, `0x0038E40C`-`0x0038E412`), then capped at 100 (`0x0038E414`-`0x0038E421`). The HP gain `0x02AEE008` is that percent of the target's max HP `+0x24`, doubled under Bubble (status 28), or under Disease (status 16) of its current HP `+0x48` (at least 1), divided by 100 and raised to 1 when it comes to 0 (`0x0038E424`-`0x0038E46E`) |
| 55-57 | `0x00387020` | the default timer, value × 30 × the frame base `0x01DFE0B4`, which `0x0030EA40` and `0x0038FF20` store in the slot `+0x06` names |

### The functions that read the table

Fifteen functions load `0x02EBF040`, at 111 instructions: `0x002FEF30`, `0x002F95D0`, `0x002F8410`, `0x00387FD0`,
`0x00389370`, `0x0038DD20`, `0x0038DF00`, `0x0038E2D0`, `0x0030EA40`, `0x00387020`, `0x00385570`, `0x0038FF20`, the query filler
`0x0031C5D0`, the validator `0x00322C50` and the loader `0x00236C30`.

- The first eight pick their rows by number and name only the rows in the table above.
- `0x0030EA40`, `0x00385570` and `0x0038FF20` take any id. `0x0030EA40` reads `+0x04` through `0x00387020` and `0x0038FF20`
  computes the same product inline (`0x0039005D`-`0x00390088`), both only for a slot `+0x06` below 8; `0x00385570` reads
  `+0x06` only. `0x0030EA40` calls `0x00387020` only when the timer it is given is negative
  (`0x0030EAA3`-`0x0030EAB3`).
- `0x00387020` does not read its first argument. For an id of `0xFF` it answers 0 (`0x00387028`-`0x00387030`).
  For any other id the row address is `(u32)(base + stride × id)`, where base is the answer of
  `0x0020E600` for the dword `+0x0C` of `[0x02EBF040]` and stride is the word `+0x08` of `[0x02EBF040]`
  (`0x00387051`-`0x0038706E`). The answer is `word +0x04 × [0x01DFE0B4] × 30` as 32-bit integers
  (`0x00387074`-`0x0038707F`).

  With `[0x02EBF040]` null, or a null answer of the first `0x0020E600` call, the row address is 0 and the
  word at address 4 is read (`0x00387038`-`0x0038704F`, `0x00387072`-`0x00387074`).
- `0x0031C5D0` reads `+0x00` and `+0x02`.

No other instruction reaches the table, and no instruction writes it after `battle_pack.bin` is loaded. Every read of
`+0x04` is one of the 28 in these functions: 23 take a fixed row, three in `0x002FEF30` take the 44 ids of its
lists (the rows in the table above), and the two that take any id (`0x00387074` from `0x0030EA40`, `0x00390071` in
`0x0038FF20`) read only a row whose slot `+0x06` is at most 7
(`0x0030EA9D`, `0x0039001D`-`0x00390024`), which is true only of rows 55-57. So the values of rows 104-113 (1 each) and
128 (20) are read by no instruction.

### Augment 114, Essentials

Augment 114's name word is "Attack Items", and the Essentials license (node 31, 1 LP) grants it. All seven main
characters start with that square ([License list](../Items-Equipment-Shops-And-Licenses/license-list.md)), so it stands
for the Attack and Items commands every character has from the start. The game needs neither the square nor the
augment to allow them:

- Attack (action row 150) and all 51 named item rows carry bit `0x2000` of the action row's `+0x2C`, which the license
  check `0x00323EC0` passes before any board lookup (`0x00323F4D`-`0x00323F58`;
  [Licenses](../Items-Equipment-Shops-And-Licenses/licenses.md)).
- No instruction tests augment 114 directly: bit `0x4` of the layer bytes `+0x76` or `+0x86`, or of the merged copy at
  context `+0x28`.
- The four functions that test an augment by a computed id do not ask for 114: the stats rebuild takes its ids from
  its three lists (`0x002FF5CA`-`0x002FF70F`), the enemy-order selector from the order (`0x00302494`), and the context
  merge (`0x00384827`) and the timer pass `0x00385570` (`0x003855CD`) walk every id.
- No instruction reads the Essentials license bit, owned-square byte `+0x197`, by itself.

So the commands are innate to every character. The row's help text, "Slightly raises max HP." (text id 13062),
names an effect the code never applies: the max-HP list of the stats rebuild is rows 74-85 (`0x00D102B0`), its other
two lists (`0x00D10290`, `0x00D102A0`) hold no 114 either, and no instruction tests augment 114 (above, and Project
notes).

### Properties of the shipped rows

- The table's header gives 129 rows of 8 bytes, one TSV line each.
- On every row byte `+0x07` is 0 and the name word is bank 10, row *n*; only ids 55-57 have a timer slot.
- Example rows: row 74 "Increases max HP by 30." has value 30, the bonus [Stats](stats.md)
  lists for it; rows 94-96 have value 12, the percentage `0x002F8410` sums for "Reduces action time by 10%";
  rows 55-57 have slots 3, 4 and 5 and value 120, the two minutes [Battle buffs](../Status-Effects-And-KO/battle-buffs.md)
  states.

## Columns

| Column | Meaning |
|---|---|
| `id`, `term` | the augment id (the row) and its name in the database: its license's name, or the modding community's name (above) |
| `name`, `name_jp` | the English name word `+0x02`, and the same word in the Japanese build |
| `license` | the license that grants the augment, empty when no license grants it |
| `text_id`, `text` | `+0x00` and its shipped text; empty for 0 |
| `value` | `+0x04` |
| `value_reader`, `value_use` | the function that reads this row's value and what it does with it; empty when no instruction reads it |
| `timer_slot` | `+0x06`; empty for `0xFF` |
| `explanation` | a one-line summary: the name (or the extra text when the name is `NOT USED`), the value and its use |

## Related

- [Augments: how a unit's augments, auto-statuses and status immunities are rebuilt from its character, gear, licenses and an enemy's script](augments.md)
- [Stats: how max HP, MP, Strength, Magick Power, Vitality, Speed, Attack Power, Defense, Magick Resist and evade are built, and their caps](stats.md)
- [Battle buffs: what Battle Cry, Enrage, Magick Barrier, Perfect Defense and the other enemy abilities switch on, and how long they last](../Status-Effects-And-KO/battle-buffs.md)

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Presentation: `0x002AC2F0` is called by `0x002AAE40`; those functions are documented on
  [message windows](../Menus-And-HUD/message-windows.md).
