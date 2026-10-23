---
title: "Bestiary: every enemy definition of every area with its name, level, stats, elements, statuses, loot and rewards"
kind: "reference"
category: "Enemy spawning"
addresses: "0x02EBF120, 0x02EBF150, 0x02EBF148, 0x02EBF140, 0x003EA710, 0x0023A570, 0x0023AC80, 0x002FEF30, 0x0030C470, 0x002398F0, 0x002394C0, 0x002390B0, 0x0023A3B0, 0x002F8BB0, 0x002F90C0, 0x00312280, 0x00317090, 0x00390390, 0x00390680, 0x003180F0, 0x00238BF0, 0x0031C2F0, 0x002ED6F0, 0x002DF9A0, 0x00264ED0"
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

### How it is built

`Database/Tools/catalogues/bestiary.py` reads the files the way the game reads them:

1. The area files. The executable's kind-21 path array `0x01EDC280`, which `0x002DF9A0` installs at `0x0215F0A8` for every
   language but Korean and Chinese, names area *a*'s file at position 2*a* under `plan_master/in`. 215 positions name
   a file and 166 of those ship. Each section is an `st2e` table whose rows start at the section's `+0x0C`.
2. The placements. A map's script is entry 3*n* of the US kind-5 array `0x01EE23A0` (`0x002DF9A0`, language 1), and its
   area is the word `+4` of row *n* of `map_ref.bin`, as `0x00264ED0` reads it. The decoder walks every function of
   those 708 scripts.
3. The names: the definition's name word `+0x08` through the word banks of the `us` `battle_pack.bin`, as `0x0023A570`
   resolves it through `0x02EBF170`.
4. The item names: ids through the [Item list](../Items-Equipment-Shops-And-Licenses/item-list.md),
   [Equipment list](../Items-Equipment-Shops-And-Licenses/equipment-list.md),
   [Loot list](../Items-Equipment-Shops-And-Licenses/loot-list.md) and key-item list, and `0xE000` + *n* as *n* gil
   ([Item and ability ids](../Engine-Core/item-and-ability-ids.md)).
5. The model: the class row's dword `+0x00` is a bound id (letter class in bits 16-23, number in bits 0-15).
   `0x002ED6F0` turns it into a resource kind and file index, and the decoder takes the file name from that kind's path
   array ([Script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md)).

The 31 `bts_` test-battle scripts under `plan_map` hold the other 517 placements of the shipped scripts. The US
kind-5 array names none of them, so no area load runs them, and the decoder leaves them out.

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
clears unit flag bit 26 first (`0x00326AFD`), which the enemy path requires.

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
| `+0x03` | `u8` | flags: bits 0-1 the tracked-HP class (`0x00328FF0`); bit 4 the height and AI tests below; bit 5 the shadow kind | `0x0023A570`, `0x00238BF0`, `0x00236210`, `0x00301AD0` |
| `+0x04` | `u8[4]` | 0 in every row | `0x00313120` (`0x0031337B`) reads `+0x04`-`+0x06` as a party row's Quickening slots for any unit the verb `spattackplay` (`0x003495A0`) names; `+0x07` no instruction (below) |
| `+0x08` | `u16` | name word | `0x0023A570`, `0x0031C5D0` (`0x0031DD5A`), `0x00536310` |
| `+0x0A` | `i16[3]` | model scale in percent, 0 meaning 100 | `0x00238BF0` (`0x00238D1B`-`0x00238D68`), handed to `0x002E5FD0` |
| `+0x10` | `u8` | 0, or 55 on two rows | no instruction (below) |
| `+0x11` | `u8[2]` | the model's variant bytes: `+0x12` first, `+0x11` second | `0x0031C540` (`0x0031C5AB`, `0x0031C5B1`) |
| `+0x13` | `u8` | animation set, `0xFF` for the weapon's | `0x003202F0` ([Action phases](../Battle-Actions/action-phases.md)) |
| `+0x14` | `u8` | 0 in every row | no instruction (below) |
| `+0x15` | `u8` | flags: bit 0 Attack and weapon evade from the rows; bit 1 shield and magick evade from the rows; bit 2 unit flag bit 43; bits 3-4 the target-information query | `0x002FEF30`, `0x0023A570`, `0x0031AA30` |
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

- `+0x03` bit 4: `0x00238BF0` raises the unit byte `+0x58` to 7 ([Battle units](../Characters-And-Objects/battle-units.md));
  `0x00236210` returns the motion height without its random part (`0x002362A4`); the gambit target selector
  `0x00301AD0` tests it (`0x0030268D`).
- `+0x03` bit 5: `0x00238BF0` passes it to `0x002E8A10`, which stores it as the render record's shadow kind, bits 12-13
  of `+0x304` ([Character lighting and shadows](../Graphics/character-lighting-and-shadows.md)).
- `+0x15` bit 3: `0x0031AA30` leaves the target-kind word at 0 for an enemy (`0x0031AACF`); bits 3 or 4: it leaves the
  reach word at -1 instead of `0x01EED2D0[action kind]` (`0x0031AB39`). `0x0031AA30` runs from `0x00321060` and `0x00328530`.

### The class row (slot 0, 84 bytes)

| Offset | Type | Field | Read by |
|---|---|---|---|
| `+0x00` | `u32` | model, a bound id | `0x0031C2F0` |
| `+0x04` | `u8` | type, unit `+0x55` | `0x0023A570` |
| `+0x05` | `u8` | class, unit `+0x56`, the kill chain's class ([Kill chain](../Rewards-EXP-Gil-And-Loot/kill-chain.md)) | `0x0023A570` |
| `+0x06` | `u16` | unit `+0x52`; 0 in every row | `0x0023A570` |
| `+0x10` | `i16` | push weight: a positive value divided by 10 is the weight the separation tick gives the body, as the party table's `+0x7A` ([Party table](../Party/party-table.md)); any other value goes over unchanged, and the -1 of 221 rows makes the body one an overlap never moves (`0x00314E10` gives a negative weight a share of 0) | `0x00238BF0` (`0x00238CEB`) → `0x0026DAC0` ([Movement bodies](../Movement-And-Pathfinding/movement-bodies-and-separation.md)) |
| `+0x12` | `u8` | flags: bits 0-2 the effect column; bit 4 actor `+0x09` bit 6; bit 5 the view query; bit 6 actor `+0x08` bit 3 and `+0x09` bit 6; bit 7 the pair clearance | below |
| `+0x18` | `u8` | bits 1-3 a movement group; bits 4-6 the placement height | `0x00239E10`, `0x003247F0`, the locomotion functions below |
| `+0x20` | `u8` | combo cap: hits at most this value minus 1 | `0x00388660` (`0x00388845`, [Combos](../Battle-Actions/combos.md)) |
| `+0x21` | `u8` | bit 1: an enemy may back off from its target | `0x003341A0` (`0x00334204`, [Action range](../Battle-Actions/action-range.md)) |
| `+0x22` | `u8` | facing in degrees, unit `+0x64` | `0x0023A570` |
| `+0x23` | `u8` | unit `+0x68` | `0x0023A570` |
| `+0x25` | `u8` | sight radius | `0x003247F0` ([Enemy AI](../Enemy-AI-And-Gambits/enemy-ai.md)) |
| `+0x26` | `u8` | radius for units below 40 % HP | `0x003247F0` |
| `+0x27` | `u8` | unit `+0x6C` | `0x0023A570` |
| `+0x28` | `u8` | bit 0 the view query's height; bit 1 the kill chain skips it | `0x0031ADB0` (`0x0031B08D`), `0x00317ED0` (`0x00317F09`) |
| `+0x29` | `u8[5]` | absorb, halve, nullify, weak, potency | `0x002FEF30` ([Elements](../Damage-And-Battle-Formulas/elements.md)) |
| `+0x30` | `u8[16]` | read and written by no instruction (below); taken as eight little-endian pairs, each is `0xFFFF` or `0x0100`-`0x01FF` | none |
| `+0x40` | `u16` | model family, the same-model run | `0x00317ED0` (`0x00317F77`) |
| `+0x52` | `u16` | species, `0xFFFF` none | `0x003171C0`, `0x0031B9A0`, `0x00329220` ([Kill rewards](../Rewards-EXP-Gil-And-Loot/kill-rewards.md)) |

The other bytes (`08`-`0F`, `13`-`17`, `19`-`1F`, `24`, `2E`-`2F`, `42`-`51`) are 0 in every row.

The `+0x12` and `+0x18` bits, by their readers:

- `+0x12` bits 0-2: `0x00329F80` picks the action effect from the table at `0x00D10720`, five values per effect class,
  and starts none for a value above 4 (`0x00329FB3`).
- `+0x12` bits 4 and 6: `0x00238BF0` hands bit 4 to `0x0026A3A0` (actor `+0x09` bit 6) and bit 6 to `0x0026A430`
  (actor `+0x08` bit 3 and `+0x09` bit 6), the bits `partyusecharhit` sets ([Party verbs](../Scripts-And-Script-Commands/party-verbs.md)).
- `+0x12` bit 5: the view builder `0x0031ADB0` reports kind 1 instead of 2 for a target with it (`0x0031B394`).
- `+0x12` bit 7: `0x003879C0`, `0x00390AB0` (`0x00390B93`, `0x00390C16`) and the pair clearance `0x0033D660` (`0x0033D794`)
  ([Battle locomotion](../Movement-And-Pathfinding/battle-locomotion.md)).
- `+0x18` bits 1-3, the value 4: the target list notices every unit (`0x003248F8`), actor `+0x13` bit 7 is set
  (`0x00238E23`), and `0x00233EA0`, `0x00233F70`, `0x0031E880` and `0x00325260` test it too.
- `+0x18` bits 1-3, other values: the locomotion functions `0x003357B0`, `0x00336710`, `0x00336CE0`, `0x00337470`,
  `0x003377C0`, `0x00337C10`, `0x00337D90`, `0x00338490`, `0x0033A240`, `0x0033C310` and `0x0033E1F0` compare the group with 0, 1,
  2, 4 and 5.
- `+0x18` bits 4-6: the placement height byte `+0x1F6` (`0x00239E10`, [Enemy spawning](enemy-spawning.md)).

### The base and growth stat rows (slots 5 and 6, 56 bytes)

| Offset | Type | Field | Read by |
|---|---|---|---|
| `+0x00` | `u16` | clan points, statistics counter 17 | `0x00317090` ([Kill rewards](../Rewards-EXP-Gil-And-Loot/kill-rewards.md)) |
| `+0x02` | `u8` | shield evade, with `+0x15` bit 1 | `0x002FEF30` |
| `+0x03` | `u8` | magick evade, with `+0x15` bit 1 | `0x002FEF30` |
| `+0x20` | `u32` | max HP | `0x002FEF30` |
| `+0x24` | `i16` | max MP | `0x002FEF30` |
| `+0x26` | `u8[4]` | Strength, Magick Power, Vitality, Speed | `0x002FEF30` |
| `+0x2A` | `u8` | innate evade | `0x002FEF30` |
| `+0x2B` | `u8` | Defense | `0x002FEF30` |
| `+0x2C` | `u8` | Magick Resist | `0x002FEF30` |
| `+0x2D` | `u8` | Attack, with `+0x15` bit 0 | `0x002FEF30` |
| `+0x2E` | `u8` | weapon evade, with `+0x15` bit 0 | `0x002FEF30` |
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

### Checks

- The 166 files' own slot 2 headers give 1,146 rows in all, and the TSV has 1,146 data lines; the slot 0, 5 and 6
  headers give 954, 1,119 and 619 rows, the counts on the area file page.
- Two runs over the same files give byte-identical output.
- The 708 us map scripts hold 6,229 `btlAtelSetUnit` calls, each followed in the same function by one
  `btlAtelSetLevel`, one `btlAtelSetStatus` and one `btlAtelSetAbility` with immediate arguments, and each naming a
  row below its area's slot 2 count; the decoder asserts all three. With the 517 of the `bts_` scripts they are the
  6,746 calls of each verb in the us scripts.
- The `in` and `ch` area files are byte-identical (166 of 166), and the 708 us map scripts place every enemy exactly
  as the `fr` and `in` copies do. Only the names differ by language: 986 of the 1,146 differ in the `de`
  `battle_pack.bin`. The TSV keeps the `us` names.
- No text field keeps an undecoded `{hh}` byte.

Five definitions compared with the code that reads them:

| Definition | Field | Shipped bytes | Reader and result |
|---|---|---|---|
| Wolf, `dst_a` row 2 | HP, base row 2 and growth row 1 | `+0x20` = `0x5E`, `0x14` | `0x002FEF30`: 94 + 20 per level above the placement's base |
| Wolf | level, script `dst_a01` | `btlAtelSetLevel(2, 1)` | `0x002398F0`: level 2 or 3, reference level 2 |
| Wolf | steal | `+0x32` = `0x2021`, `0x2069`, `0x10F3` | `0x00390390`: Wind Stone, Wolf Pelt, Pointy Hat |
| Flan, `mic_a` row 4 | EXP, LP | base `+0x34` = 200, `+0x2F` = 1; growth 7, 0 | `0x002F8BB0`, `0x002F90C0`: 200 EXP + 7 per level, 1 LP |
| Flan | weak | class row 4 `+0x2C` = `0x01` | `0x002FEF30` copies it to stats `+0x40`: fire |
| Malboro, `lus_d` row 3 | poach | `+0x44` = `0x207E`, `+0x46` = `0x207F` | `0x00390680`: Malboro Fruit at 95 %, Malboro Flower at 5 % |
| Malboro | clan points | base `+0x00` = 330, growth 85 | `0x00317090`: 330 + 85 per level |
| Basch, `naf_a` row 2 | evades | `+0x15` = `0x03`, base `+0x02` = 25, `+0x03` = 10 | `0x002FEF30`: shield evade 25 and magick evade 10 from the row, not the Buckler |
| Omega Mark XII, `gil_i` row 7 | absorb | class row 6 `+0x29` = `0xFF` | `0x002FEF30`: absorbs all eight elements |

## Columns

| Column | Meaning |
|---|---|
| `area`, `area_id`, `row`, `id` | the area file, its area number, the definition's row and its id `0x100` + row |
| `name` | the shipped name |
| `placements`, `level` | how many placements the us map scripts make, and the level ranges `base`-`base + range` they set |
| `class_row`, `model`, `model_id` | the class row, its model's file name and bound id |
| `type`, `class`, `species`, `model_family` | class row `+0x04`, `+0x05`, `+0x52` (empty for none), `+0x40` |
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
| `start_hp` ... `class_bytes30` | the remaining fields as the layout tables above name them, raw; `push_weight` is class row `+0x10` divided by 10, and `class_bytes30` the sixteen bytes of `+0x30` |
| `explanation` | a one-line summary of the placements, HP, elements, rewards and steals |

A value that differs between placements of one definition is listed once per variant, separated by ` / `.

## Related

- [Area battle data (.ard and .nmb): the per-area file of enemy definitions, class rows, stat rows, gambit order sets, motion overrides and preloaded models, and its companion](../Game-Files-And-Data-Tables/ard-area-battle-data.md)
- [Battle unit construction: the party and enemy definition tables, the stats record a unit gets, the kind byte and the type partition](../Characters-And-Objects/battle-unit-construction.md)
- [Stats: how max HP, MP, Strength, Magick Power, Vitality, Speed, Attack Power, Defense, Magick Resist and evade are built, and their caps](../Damage-And-Battle-Formulas/stats.md)
- [Augments: how a unit's augments, auto-statuses and status immunities are rebuilt from its character, gear, licenses and an enemy's script](../Damage-And-Battle-Formulas/augments.md)
- [Loot drops: drop roll, item slots, quantities, drop tables and the chain bonus](../Rewards-EXP-Gil-And-Loot/loot-drops.md)
