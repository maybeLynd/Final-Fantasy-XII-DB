---
title: "Bestiary: every enemy definition of every area with its name, level, stats, elements, statuses, loot and rewards"
kind: "reference"
category: "Enemy spawning"
addresses: "0x02EBF120, 0x02EBF150, 0x02EBF148, 0x02EBF140, 0x003EA710, 0x0023A570, 0x0023AC80, 0x002FEF30, 0x0030C470, 0x002398F0, 0x002394C0, 0x002390B0, 0x0023A3B0, 0x002F8BB0, 0x002F90C0, 0x00312280, 0x00317090, 0x00390390, 0x00390680, 0x003180F0, 0x00238BF0, 0x0031C2F0, 0x002ED6F0, 0x002DF9A0, 0x00264ED0, 0x0031C540, 0x0026D610, 0x002E6090, 0x002E28E0, 0x0042FB80, 0x00420480, 0x0041F340, 0x00504F00, 0x00504840, 0x004772E0, 0x003171C0, 0x00315820, 0x00315420, 0x005760A0, 0x003214B0, 0x002B58B0, 0x01EC73A0, 0x00D23740, 0x0038D400, 0x00315D50, 0x01EED130, 0x00316930, 0x002DFC0A"
---

## What it lists

`bestiary.tsv` holds one line for each of the 1,146 enemy definitions in the 166 shipped area files (`.ard`): the
rows of directory slot 2 that `0x003EA710` binds to registry slot `0x02EBF120` when the area loads
([Area battle data](../Game-Files-And-Data-Tables/ard-area-battle-data.md)).

Four of the 166 files have no slot 2 rows (`asp_a` 94, `mrm_a` 187, `slm_a` 217 and `dor_f` 280), so the lines
come from 162 areas. Each line joins the definition to
its class row (slot 0, `0x02EBF150`), its base stat row (slot 5, `0x02EBF148`) and its growth stat row (slot 6,
`0x02EBF140`), and to the zone-script calls that place it.

- One monster has many definitions: one per area it appears in and one per variant inside an area. The 1,146 lines
  carry 457 distinct names; Imperial Swordsman has 51 definitions, Flan 5 and Wolf 2. Every definition is kept.
- The level, the status immunities, the starting statuses and the augments are not in the area file. Each placement
  sets them through four script verbs (below), so a definition placed several ways lists every combination.
- 1,143 definitions are placed by the us map scripts, 6,229 times in all. Three are placed by none: Dead Bones
  (`bog_a` row 3), Axebeak (`enw_b` row 8) and Omega Mark XII (`gil_i` row 7).

[`enemy-placements.tsv`](enemy-placements.tsv) lists those 6,229 placements one by one: the area, the map script by
its path under `plan_map`, the zone-script function that makes the four calls (its name as the script stores it),
the definition row it places with its id and name, and the level it sets. The same walk builds both files, and the
decoder asserts that each definition's `placements` count is its number of lines there.

The category is the spawn lifecycle's because a definition does nothing until a zone script spawns it: the
installer `0x0023A570` applies it to a unit through the spawn record ([Spawn record fields](spawn-record-fields.md)).

### Where the values come from

Each line is read as the game reads the files:

1. The area files. The executable's kind-21 path array `0x01EDC280`, which `0x002DF9A0` installs at `0x0215F0A8` for every
   language but Korean and Chinese, names area *a*'s file at position 2*a* under `plan_master/in`. 215 positions name
   a file and 166 of those ship. Each section is an `st2e` table whose rows start at the section's `+0x0C`.
2. The placements. A map's script is entry 3*n* of the US kind-5 array `0x01EE23A0` (`0x002DF9A0`, language 1), and its
   area is the word `+4` of row *n* of `map_ref.bin`, as `0x00264ED0` reads it. The placements are the calls in every
   function of those 708 scripts.
3. The names: the definition's name word `+0x08` through the word banks of the `us` `battle_pack.bin`, as `0x0023A570`
   resolves it through `0x02EBF170`.
4. The item names: ids through the [Item list](../Items-Equipment-Shops-And-Licenses/item-list.md),
   [Equipment list](../Items-Equipment-Shops-And-Licenses/equipment-list.md),
   [Loot list](../Items-Equipment-Shops-And-Licenses/loot-list.md) and key-item list, and `0xE000` + *n* as *n* gil
   ([Item and ability ids](../Engine-Core/item-and-ability-ids.md)).
5. The model: the class row's dword `+0x00` is a bound id (letter class in bits 16-23, number in bits 0-15).
   `0x002ED6F0` turns it into a resource kind and file index, and the file name is that index's entry of the kind's
   path array ([Script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md)).
6. The Clan Primer Bestiary entry: the class row's word `+0x52` (below), and the entry's name from the US Bestiary
   catalog `menuhandbook_monster.bin`, read as the entry page reads it (next section).
7. The race and family: the class row's bytes `+0x04` and `+0x05` through word banks 13 and 14 of the `us`
   `battle_pack.bin`, as battle-text words `0x6800` + `+0x04` and `0x7000` + `+0x05` (Project notes give the
   basis).

### The Clan Primer Bestiary entry

The class row's word `+0x52` is the number of the Clan Primer Bestiary entry whose kill count the enemy's defeats
raise, for every entry but the two of step 2 ([Clan Primer](../Menus-And-HUD/clan-primer.md), [Handbook files](../Game-Files-And-Data-Tables/handbook-files.md)):

1. At a defeat, `0x003171C0` reads `[[enemy + 0xE68] + 0x52]` (`0x00317213`) and, unless it is `0xFFFF` or the actor's
   class nibble is 3, passes it to `0x00315820` through the thunk `0x00253750`
   ([Kill rewards](../Rewards-EXP-Gil-And-Loot/kill-rewards.md)).
2. `0x00315820` keeps the count plus one in the save byte `+0x3404` + that number (`0x0031588E`), for a number below
   `0x200` for which `0x00315D50` returns -1.
   - It returns another value for two numbers of its `menuhandbook.bin` list, which `0x01EED130` pairs with a
     quest: entry 251, Gilgamesh, with 167, and entry 259, Shadowseer, with 170.
   - A defeat leaves those two counts unchanged, so the 11 Gilgamesh and 3 Shadowseer definitions name an entry
     their defeats do not count.
   - The field-frame sweep `0x00316930` sets each of the two counts to 1 once `0x00315DC0` passes for its quest
     ([Achievements](../Steam-And-Achievements/achievements.md)).
3. The entry page's record builder `0x005760A0(record, n)` reads entry *n*'s kill count through `0x00315420(n)`
   (`0x00576227`), which reads the same byte, save `+0x3404` + *n* (`0x0031545C`).
4. The same builder takes the entry's name from the catalog: the `i32` at `+0x00` of the 12-byte record *n*, a
   battle-text word for the Bestiary, resolved by `0x003214B0` (`0x0057617B`) and read as string 0 of its row by
   `0x002B58B0` (`0x00576185`).

The catalog is kind-7 resource `0x354`, the Bestiary family's base id at `0x00D23740` + 2 × 5 (`0x00575C60`). The US
build's kind-7 path array `0x01EC73A0`, which `0x002DF9A0` loads in its US case (`0x002DFC0A`) and stores at `0x0215F038` (`0x002DFF7F`), names
`myoshiok/us/handbook/menuhandbook_monster.bin` for it. Its 384 entry names are all words of bank 8, the monster
names. One entry serves every variant of a monster: Wolf and Alpha Wolf both count for entry 2, Wolf.

The 21 definitions whose name word reads No name in the `us` text are placed by the `PRISON_` functions of `nal_a`
and `nal_b`, the `COCKATRICE_` functions of `sav_b`, the `SND_MAN_` and `SND_WOMAN_` functions of `rbn_a`, and the
`THIRD_` functions of `rui_a` and `srb_b`. Sixteen use a model from the `npc` model folder, the five of `sav_b` one
from the `monster` folder.

The `fr` `battle_pack.bin` keeps a label at each of those words: `prison_human`, `prison_bangaa`, `prison_seeq`,
`siiku_cocka`, `2kyu_simin_men`, `2kyu_simin_women`, `seeq_event` and `viera_event`. Each line's explanation gives
the word, its `fr` text, its model's folder and the zone-script functions that place it.

The 31 `bts_` test-battle scripts under `plan_map` hold the other 517 placements of the shipped scripts. The US
kind-5 array names none of them, so no area load runs them, and they are left out.

### The placement verbs

Every placement in the shipped scripts is one script function calling these four verbs, each with immediate
arguments (`PUSHII`, a pooled int or a pooled float):

| Verb | Handler | What it sets |
|---|---|---|
| `btlAtelSetUnit(row)` | `0x00510160` → `0x0023A3B0` | installs definition `0x100` + *row* with `0x0023A570` |
| `btlAtelSetLevel(base, range)` | `0x0050F910` → `0x002398F0` | level `base + rand % (range + 1)` and reference level `+0x88` = `base`, through `0x0030C470` |
| `btlAtelSetStatus(table)` | `0x005103B0` → `0x002394C0` | 32 two-bit codes: 3 immune, 2 added at a fresh spawn, 1 added when an LCG draw is odd ([Augments](../Damage-And-Battle-Formulas/augments.md)) |
| `btlAtelSetAbility(a, b)` | `0x00510440` → `0x002390B0` | the enemy augment mask `+0xE80`: bit *j* of `a` sets augment 31 - *j*, bit *j* of `b` sets augment 63 - *j* |

The status table argument is an msp reference (tag 3, resolved by `0x002650B0`): 8 bytes at the script image's
`[+0x40]` plus the offset. `0x0023A570` has two other callers: `0x00300E40` passes `0xFFFF` (`0x00300F6D`), and `0x003266C0`
clears unit flag bit `0x4000000` first (`0x00326AFD`), which the enemy path requires.

Because the reference level is the placement's own base level, every stat and reward is the base row's value at
that level and grows by the growth row's value for each level above it ([Stats](../Damage-And-Battle-Formulas/stats.md)):

```python
stat = growth[field] * (level - base) + base[field] + order adjustment  # 0x002FEF30
reward = per-level[field] * (level - base) + base[field]  # 0x002F8BB0, 0x002F90C0, 0x00312280, 0x00317090
```

So a Wolf placed at levels 2-3 and one placed at levels 6-7 both have 94 HP at their lowest level.

### The enemy definition (slot 2, 88 bytes)

| Offset | Type | Field | Read by |
|---|---|---|---|
| `+0x00` | `u16` | class row | `0x0023A570`, `0x002FEF30`; `0x0031C2F0` reads its low byte for the model ([Battle unit construction](../Characters-And-Objects/battle-unit-construction.md)) |
| `+0x02` | `u8` | spawn counter slot, `0xFF` none | `0x0023A570` |
| `+0x03` | `u8` | flags: bits `0x3` the tracked-HP class (`0x00328FF0`); bit `0x10` the height and AI tests below; bit `0x20` the shadow kind | `0x0023A570`, `0x00238BF0`, `0x00236210`, `0x00301AD0` |
| `+0x04` | `u8[4]` | 0 in every row | `0x00313120` (`0x0031337B`) reads `+0x04`-`+0x06` as a party row's Quickening slots for any unit the verb `spattackplay` (`0x003495A0`) names; `+0x07` no instruction (below) |
| `+0x08` | `u16` | name word | `0x0023A570`, `0x0031C5D0` (`0x0031DD5A`), `0x00536310` |
| `+0x0A` | `i16[3]` | model scale in percent, 0 meaning 100 | `0x00238BF0` (`0x00238D1B`-`0x00238D68`), handed to `0x002E5FD0` |
| `+0x10` | `u8` | 0, or 55 on two rows | no instruction (below) |
| `+0x11` | `u8` | the model variant: the `@FOR` record key the render record asks for (below) | `0x0031C540` (`0x0031C5B1`) |
| `+0x12` | `u8` | the colour: the model row's option number (below) | `0x0031C540` (`0x0031C5AB`) |
| `+0x13` | `u8` | animation set, `0xFF` for the weapon's | `0x003202F0` ([Action phases](../Battle-Actions/action-phases.md)) |
| `+0x14` | `u8` | 0 in every row | no instruction (below) |
| `+0x15` | `u8` | flags: bit `0x1` Attack and weapon evade from the rows; bit `0x2` shield and magick evade from the rows; bit `0x4` unit flag bit `0x80000000000`; bits `0x18` the target-information query | `0x002FEF30`, `0x0023A570`, `0x0031AA30` |
| `+0x16` | `u16` | main-hand equipment id | `0x0023AC80` (slot 0) |
| `+0x18` | `u32` | starting HP, 0 for none | `0x0023A410` ([Enemy spawning](enemy-spawning.md)) |
| `+0x1C` | `u16` | off-hand equipment id | `0x0023AC80` (slot 1) |
| `+0x22` | `u16` | base stat row | `0x0023A570`, `0x002FEF30` |
| `+0x24` | `u16` | growth stat row | `0x0023A570`, `0x002FEF30` |
| `+0x26` | `i16` | voice bank, negative for the model's | `0x003212E0` ([Character sound tables](../Game-Files-And-Data-Tables/character-se-tables-chse.md)) |
| `+0x28` | `u16[5]` | drop slots 1-5 | `0x003180F0` ([Loot drops](../Rewards-EXP-Gil-And-Loot/loot-drops.md)) |
| `+0x32` | `u16[3]` | steal: common, uncommon, rare | `0x00390390`, `0x0023A570` ([Steal](../Damage-And-Battle-Formulas/steal.md)) |
| `+0x38` | `u32[2]` | the ids of the model's part 8 entries 0 and 1, 0 for none; 0 in every row | `0x0031C000` through `0x0031BEC0` ([Actor model rebuild](../Characters-And-Objects/actor-model-rebuild.md), states 13-15) |
| `+0x40` | `u8[2]` | those entries' attach links, through the table at `0x00D107F8`; 0 in every row | `0x0031BE30` |
| `+0x42` | `u8[2]` | Monograph drop chances | `0x003180F0` |
| `+0x44` | `u16[2]` | poach: common (95 %), rare (5 %) | `0x00390680` ([Formula slots](../Damage-And-Battle-Formulas/formula-slots.md)) |
| `+0x48` | `u16[4]` | Monograph pairs: key item, item | `0x003180F0` |
| `+0x50` | `u16[4]` | order sets for orders 0-3 | `0x0023A570` (set 0), `0x00239040`, `0x002FDDA0` ([Battle orders](../Battle-Actions/battle-orders.md)) |

The `+0x03` and `+0x15` bits, by their readers:

- `+0x03` bit `0x10`: `0x00238BF0` raises the unit byte `+0x58` to 7 ([Battle units](../Characters-And-Objects/battle-units.md));
  `0x00236210` returns the motion height without its random part (`0x002362A4`); the gambit target selector
  `0x00301AD0` tests it (`0x0030268D`).
- `+0x03` bit `0x20`: `0x00238BF0` passes it to `0x002E8A10`, which stores it as the render record's shadow kind, bits 12-13
  of `+0x304` ([Character lighting and shadows](../Graphics/character-lighting-and-shadows.md)).
- `+0x15` bit `0x8`: `0x0031AA30` leaves the target-kind word at 0 for an enemy (`0x0031AACF`); bits `0x8` or `0x10`: it leaves the
  reach word at -1 instead of `0x01EED2D0[action kind]` (`0x0031AB39`). `0x0031AA30` runs from `0x00321060` and `0x00328530`.

### Colour and model variants

`0x0031C540(actorId, &colour, &variant)` resolves the id to its actor (`0x003588B0`) and the actor's unit (`0x00263E30`,
`+0x30`), and reads the two bytes from the unit's definition (`[unit + 0xE60]`, `+0x12` and `+0x11`) when the
unit's row `+0x698` byte `+5` is 1. Otherwise it fails with both 0 and a non-zero return. The model rebuild hands them on as
`0x0026D610(actor, variant, colour)` (`0x0037B77C`-`0x0037B7A5`), or as variant 1 and colour 0 when the read fails
([actor model rebuild](../Characters-And-Objects/actor-model-rebuild.md)). From there:

1. `0x0026D610` stores variant and colour at the actor's secondary `+0x14C` and `+0x14D` (`0x002E6090`).
2. The presentation set-up `0x002E28E0` passes both to `0x0042FB80` (`0x002E2986`-`0x002E2998`), whose initialiser
   `0x00420480` keeps the variant at render record `+0x5C`, 1 when it is 0 (`0x00420557`-`0x00420568`), and the colour at
   `+0x5D` (`0x0042056C`-`0x00420576`).
3. The bind `0x0041F340` hands both to the model row (`0x0041F641`-`0x0041F69E`, `0x004780C0`). `0x00504F00` matches the
   variant against the model's `@FOR` record keys (`+0xB8`; the first record's key when none matches, 0 with no
   record) and keeps the colour as the option number `+0xB9`
   while it is below the `@FOR` option count `+0x33`, else 0
   ([model files](../Graphics/model-files-cm-ca.md)).
4. The variant also picks the `@FOR` scale (`0x00504840`, record `+0x26C`) and the pose sequencer entry
   (`0x004772E0`, record `+0x450`).

Over the 1,146 definitions, `+0x12` is 0 on 1,065, 1 on 46, 2 on 20, 3 on 8, 4 on 3 and 5 on 4; `+0x11` is 0 on
1,046, 1 on 27, 2 on 22, 3 on 21, 4 on 21, 5 on 3, 6 on 4, and 7 and 8 on one each. 1,018 rows have both 0.

The chocobos are one model, `m1066` (`0x006D002A`), with one `@FOR` record (key 1) and six option numbers. Every
chocobo definition has variant 0 and one of these colours:

| Colour (`+0x12`) | Definitions |
|---|---|
| 1 | Red Chocobo (3), Lv. 99 Red Chocobo (2) |
| 2 | Black Chocobo (5), Bull Chocobo (1) |
| 3 | White Chocobo (1) |
| 4 | Green Chocobo (2) |
| 5 | Brown Chocobo (4) |

### The class row (slot 0, 84 bytes)

| Offset | Type | Field | Read by |
|---|---|---|---|
| `+0x00` | `u32` | model, a bound id | `0x0031C2F0` |
| `+0x04` | `u8` | type, unit `+0x55`, named by word bank 13 (word `0x6800` + type: 0 Hume, 1 Humanoid, 2 Giant, 3 Dragon, 4 Beast, 5 Insect, 6 Plant, 7 Avion, 8 Amorph, 9 Fiend, 10 Elemental, 11 Warmech, 12 ???, 13 Undead, 14 Construct, 15 Ichthian); when the source unit's is 13, the Drain slot `0x0038D400` exchanges the target's HP loss and gain with the source's (`0x0038D4D9`-`0x0038D50B`), and its final block then rewrites part of them ([Formula slots](../Damage-And-Battle-Formulas/formula-slots.md)) | `0x0023A570` |
| `+0x05` | `u8` | class, unit `+0x56`, the kill chain's class ([Kill chain](../Rewards-EXP-Gil-And-Loot/kill-chain.md)), named by word bank 14 (word `0x7000` + class, 64 names; class 34 is Skeleton) | `0x0023A570` |
| `+0x06` | `u16` | unit `+0x52`; 0 in every row | `0x0023A570` |
| `+0x10` | `i16` | push weight: a positive value divided by 10 is the weight the separation tick gives the body, as the party table's `+0x7A` ([Party table](../Party/party-table.md)); any other value goes over unchanged, and the -1 of 221 rows makes the body one an overlap never moves (`0x00314E10` gives a negative weight a share of 0) | `0x00238BF0` (`0x00238CEB`) → `0x0026DAC0` ([Movement bodies](../Movement-And-Pathfinding/movement-bodies-and-separation.md)) |
| `+0x12` | `u8` | flags: bits 0-2 the effect column; bit `0x10` actor `+0x09` bit `0x40`; bit `0x20` the view query; bit `0x40` actor `+0x08` bit `0x8` and `+0x09` bit `0x40`; bit `0x80` the pair clearance | below |
| `+0x18` | `u8` | bits `0xE` a movement group; bits 4-6 the placement height | `0x00239E10`, `0x003247F0`, the locomotion functions below |
| `+0x20` | `u8` | combo cap: hits at most this value minus 1 | `0x00388660` (`0x00388845`, [Combos](../Battle-Actions/combos.md)) |
| `+0x21` | `u8` | bit `0x2`: an enemy may back off from its target | `0x003341A0` (`0x00334204`, [Action range](../Battle-Actions/action-range.md)) |
| `+0x22` | `u8` | facing in degrees, unit `+0x64` | `0x0023A570` |
| `+0x23` | `u8` | unit `+0x68` | `0x0023A570` |
| `+0x25` | `u8` | sight radius | `0x003247F0` ([Enemy AI](../Enemy-AI-And-Gambits/enemy-ai.md)) |
| `+0x26` | `u8` | radius for units below 40 % HP | `0x003247F0` |
| `+0x27` | `u8` | unit `+0x6C` | `0x0023A570` |
| `+0x28` | `u8` | bit `0x1` the view query's height; bit `0x2` the kill chain skips it | `0x0031ADB0` (`0x0031B08D`), `0x00317ED0` (`0x00317F09`) |
| `+0x29` | `u8[5]` | absorb, halve, nullify, weak, potency | `0x002FEF30` ([Elements](../Damage-And-Battle-Formulas/elements.md)) |
| `+0x30` | `u8[16]` | read and written by no instruction (below); taken as eight little-endian pairs, each is `0xFFFF` or `0x0100`-`0x01FF` | none |
| `+0x40` | `u16` | model family, the same-model run | `0x00317ED0` (`0x00317F77`) |
| `+0x52` | `u16` | Clan Primer Bestiary entry, `0xFFFF` none (above) | `0x003171C0`, `0x0031B9A0`, `0x00329220` ([Kill rewards](../Rewards-EXP-Gil-And-Loot/kill-rewards.md)) |

The other bytes (`08`-`0F`, `13`-`17`, `19`-`1F`, `24`, `2E`-`2F`, `42`-`51`) are 0 in every row.

The `+0x12` and `+0x18` bits, by their readers:

- `+0x12` bits `0x7`: `0x00329F80` picks the action effect from the table at `0x00D10720`, five values per effect class,
  and starts none for a value above 4 (`0x00329FB3`).
- `+0x12` bits `0x10` and `0x40`: `0x00238BF0` hands bit `0x10` to `0x0026A3A0` (actor `+0x09` bit `0x40`) and bit `0x40` to `0x0026A430`
  (actor `+0x08` bit `0x8` and `+0x09` bit `0x40`), the bits `partyusecharhit` sets ([Party verbs](../Scripts-And-Script-Commands/party-verbs.md)).
- `+0x12` bit `0x20`: the view builder `0x0031ADB0` reports kind 1 instead of 2 for a target with it (`0x0031B394`).
- `+0x12` bit `0x80`: `0x003879C0`, `0x00390AB0` (`0x00390B93`, `0x00390C16`) and the pair clearance `0x0033D660` (`0x0033D794`)
  ([Battle locomotion](../Movement-And-Pathfinding/battle-locomotion.md)).
- `+0x18` bits `0xE`, the value 4: the target list notices every unit (`0x003248F8`), actor `+0x13` bit `0x80` is set
  (`0x00238E23`), and `0x00233EA0`, `0x00233F70`, `0x0031E880` and `0x00325260` test it too.
- `+0x18` bits `0xE`, other values: the locomotion functions `0x003357B0`, `0x00336710`, `0x00336CE0`, `0x00337470`,
  `0x003377C0`, `0x00337C10`, `0x00337D90`, `0x00338490`, `0x0033A240`, `0x0033C310` and `0x0033E1F0` compare the group with 0, 1,
  2, 4 and 5.
- `+0x18` bits 4-6: the placement height byte `+0x1F6` (`0x00239E10`, [Enemy spawning](enemy-spawning.md)).

### The base and growth stat rows (slots 5 and 6, 56 bytes)

| Offset | Type | Field | Read by |
|---|---|---|---|
| `+0x00` | `u16` | clan points, statistics counter 17 | `0x00317090` ([Kill rewards](../Rewards-EXP-Gil-And-Loot/kill-rewards.md)) |
| `+0x02` | `u8` | shield evade, with `+0x15` bit `0x2` | `0x002FEF30` |
| `+0x03` | `u8` | magick evade, with `+0x15` bit `0x2` | `0x002FEF30` |
| `+0x20` | `u32` | max HP | `0x002FEF30` |
| `+0x24` | `i16` | max MP | `0x002FEF30` |
| `+0x26` | `u8[4]` | Strength, Magick Power, Vitality, Speed | `0x002FEF30` |
| `+0x2A` | `u8` | innate evade | `0x002FEF30` |
| `+0x2B` | `u8` | Defense | `0x002FEF30` |
| `+0x2C` | `u8` | Magick Resist | `0x002FEF30` |
| `+0x2D` | `u8` | Attack, with `+0x15` bit `0x1` | `0x002FEF30` |
| `+0x2E` | `u8` | weapon evade, with `+0x15` bit `0x1` | `0x002FEF30` |
| `+0x2F` | `u8` | LP | `0x002F90C0` ([EXP, LP and level-ups](../Rewards-EXP-Gil-And-Loot/exp-lp-and-level-ups.md)) |
| `+0x30` | `u32` | gil | `0x00312280` ([Gil](../Rewards-EXP-Gil-And-Loot/gil.md)) |
| `+0x34` | `i32` | EXP | `0x002F8BB0` |

Bytes `04`-`1F`, `32`-`33` and `36`-`37` are 0 in every row of both slots.

### Bytes no instruction reads

Definition `+0x07`, `+0x10` and `+0x14` and class row `+0x30`-`+0x3F` arrive whole with the area file,
which `0x003EA710` binds, and no instruction reads or writes them afterwards. Every way to a row was followed:

- The four slot pointers are loaded by seven functions and no others: `0x02EBF120` by `0x0023A570`, `0x0023AC80`,
  `0x002FEF30`, `0x0031C2F0`, `0x0031C5D0` and `0x00322C50`; `0x02EBF150` by `0x0023A570`, `0x002FEF30`, `0x0031C2F0` and `0x00322C50`;
  `0x02EBF148` and `0x02EBF140` by `0x0023A570` and `0x002FEF30`; `0x0023A160` clears all four. No instruction forms the four
  addresses from the image base.
- The definition pointer unit `+0xE60` is loaded or stored at 32 sites in 25 functions and the class row pointer
  `+0xE68` at 52 sites in 33 functions, and the pointers were followed into the callees that receive them.
  `0x00313120` reads `+0x04`-`+0x06` of the row at `+0xE60` of the unit `0x0031B7E0` resolves from the actor handle the verb
  `spattackplay` pops (`0x0031337B`), and `0x00317400` reads `+0x7A`: both treat the row as a party row.
- `+0xE70` and `+0xE78` (the stat rows) are stored by `0x0023A570` and loaded only by `0x002F8BB0`, `0x002F90C0`, `0x00312280`
  and `0x00317090`.

No instruction in that set touches the bytes above, so the TSV gives them raw.

## Columns

| Column | Meaning |
|---|---|
| `area`, `area_id`, `row`, `id` | the area file, its area number, the definition's row and its id `0x100` + row |
| `name` | the shipped name |
| `placements`, `level` | how many placements the us map scripts make, and the level ranges `base`-`base + range` they set |
| `class_row`, `model`, `model_id` | the class row, its model's file name and bound id |
| `type`, `race` | class row `+0x04`, and its name in the `us` text: battle-text word `0x6800` + type, word bank 13 |
| `class`, `family` | class row `+0x05`, and its name in the `us` text: battle-text word `0x7000` + class, word bank 14. The `us` text of class 46 carries the prefix "NOT USED" ("NOT USED Wings"; the `de` text is Flugwesen), and the column keeps it as shipped |
| `primer_entry`, `primer_name` | class row `+0x52`, the Clan Primer Bestiary entry (empty for none), and that entry's name in the US Bestiary catalog |
| `model_family` | class row `+0x40` |
| `base_row`, `growth_row` | definition `+0x22`, `+0x24` |
| `hp` ... `magick_evade` | the stats `0x002FEF30` builds at a placement's base level without order adjustments: the base row plus the gear's bonus records, Attack and evades from the gear unless `+0x15` says otherwise, capped as on [Stats](../Damage-And-Battle-Formulas/stats.md) |
| `*_per_level` | the growth row's value added per level above the base |
| `exp`, `lp`, `gil`, `clan_points` and their `_per_level` | the base and growth rows' rewards |
| `weak`, `absorb`, `halve`, `nullify`, `potency` | the class row's affinity bytes ORed with the gear's attribute records |
| `immune`, `auto_status`, `auto_status_half` | the status codes 3, 2 and 1 of the placements' `btlAtelSetStatus` tables |
| `augments` | the augments `btlAtelSetAbility` sets, each by its term on [Augment list](../Damage-And-Battle-Formulas/augment-list.md) with its id |
| `steal_*`, `drop_1`-`drop_5`, `poach_*` | the items by name |
| `monograph_1`, `monograph_2` | item, chance and the key item that must be held |
| `weapon`, `weapon_element`, `weapon_status`, `off_hand` | the two equipment ids by name; the main-hand row's element and on-hit status |
| `variant` | definition `+0x12` (the colour) then `+0x11` (the model variant), as "colour, variant" |
| `start_hp` ... `class_bytes30` | the remaining fields as the layout tables above name them, raw; `push_weight` is class row `+0x10` divided by 10, and `class_bytes30` the sixteen bytes of `+0x30` |
| `explanation` | a one-line summary of the placements, HP, elements, rewards and steals; for a No name line also its name word, that word's `fr` text, its model's folder, the functions that place it and its Clan Primer entry |

A value that differs between placements of one definition is listed once per variant, separated by ` / `.

## Related

- [Area battle data (.ard and .nmb): the per-area file of enemy definitions, class rows, stat rows, gambit order sets, motion overrides and preloaded models, and its companion](../Game-Files-And-Data-Tables/ard-area-battle-data.md)
- [Battle unit construction: the party and enemy definition tables, the stats record a unit gets, the kind byte and the type partition](../Characters-And-Objects/battle-unit-construction.md)
- [Stats: how max HP, MP, Strength, Magick Power, Vitality, Speed, Attack Power, Defense, Magick Resist and evade are built, and their caps](../Damage-And-Battle-Formulas/stats.md)
- [Augments: how a unit's augments, auto-statuses and status immunities are rebuilt from its character, gear, licenses and an enemy's script](../Damage-And-Battle-Formulas/augments.md)
- [Loot drops: drop roll, item slots, quantities, drop tables and the chain bonus](../Rewards-EXP-Gil-And-Loot/loot-drops.md)
