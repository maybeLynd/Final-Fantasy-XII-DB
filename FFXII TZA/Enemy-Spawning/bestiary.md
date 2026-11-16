---
title: "Bestiary: every enemy definition of every area with its name, level, stats, elements, statuses, loot and rewards"
kind: "reference"
category: "Enemy spawning"
addresses: "0x02EBF120, 0x02EBF150, 0x02EBF148, 0x02EBF140, 0x003EA710, 0x0023A570, 0x0023AC80, 0x002FEF30, 0x0030C470, 0x002398F0, 0x002394C0, 0x002390B0, 0x0023A3B0, 0x002F8BB0, 0x002F90C0, 0x00312280, 0x00317090, 0x00390390, 0x00390680, 0x003180F0, 0x00238BF0, 0x0031C2F0, 0x002ED6F0, 0x002DF9A0, 0x00264ED0, 0x0031C540, 0x0026D610, 0x002E6090, 0x002E28E0, 0x0042FB80, 0x00420480, 0x0041F340, 0x00504F00, 0x00504840, 0x004772E0, 0x003171C0, 0x00315820, 0x00315420, 0x005760A0, 0x003214B0, 0x002B58B0, 0x01EC73A0, 0x00D23740, 0x0038D400, 0x00315D50, 0x01EED130, 0x00316930, 0x002DFC0A"
---

## What it lists

[`bestiary.tsv`](bestiary.tsv) holds one line for each of the 1,146 enemy definitions in the 166 shipped area files (`.ard`): the
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
- 1,143 definitions are placed by the us map scripts, 6,229 times in all. Three are placed by no script: Dead Bones
  (`bog_a` row 3), Axebeak (`enw_b` row 8) and Omega Mark XII (`gil_i` row 7).

[`enemy-placements.tsv`](enemy-placements.tsv) lists those 6,229 placements one by one: the area, the map script by
its path under `plan_map`, the actor whose code makes the four calls (`function`, its name as the script stores it),
the actor's function that holds them (`entry`, an `entryNN` function, named in the actor's function table), the
definition row it places with its id and name, and the level it sets. The same walk builds both files, and the
decoder asserts that each definition's `placements` count is its number of lines there.

One actor often places the same definition at the same level from several entry functions, so `entry` is what tells
those lines apart; it is also the `group` of [`enemy-placement-conditions.tsv`](enemy-placement-conditions.tsv).

[`enemy-placements-maps.tsv`](enemy-placements-maps.tsv) gives the same 6,229 placements with the place the player meets
them: the zone the script belongs to, its map name and its region, as the location line shows them
([Zone asset list](../World-Areas-And-Travel/zone-asset-list.md)). They fall in 471 zones of 41 regions.

[`enemy-placement-kinds.tsv`](enemy-placement-kinds.tsv) gives each of the 6,229 placements its kind. The kind comes
from the tables that name the placement or its definition, never from the function's name, and the first test that
holds sets it:

| Kind | Placements | Test |
|---|---|---|
| `Trial Mode` | 550 | the map script is one of the 100 Trial Mode scripts ([Trial Mode scripts](../Story-Events-And-Hunts/trial-mode-scripts.md)) |
| `story boss` | 156 | the function is one of the functions of a fight in [`story-bosses.tsv`](story-bosses.tsv) |
| `hunt mark` | 43 | the definition is the mark of a hunt in the mark column of [Hunts](../Story-Events-And-Hunts/hunts.md), 40 hunts in all |
| `Elite Mark` | 4 | the definition stands in the Clan Primer's Elite Marks section and is no hunt's mark |
| `rare game` | 208 | the definition stands in the Clan Primer's Rare Game section |
| `foe` | 5,268 | none of the above |

The `primer_section`, `hunt`, `story_boss` and `trial_mode` columns give each test on its own, so a placement that
passes two shows both: 15 `story boss` placements are also a hunt's mark, as Ba'Gamnan in Withering Shores is the mark
of "A Dark Rumor".

`group_chosen_by` names how the zone script picks the placement's group, from the `lane` column of the rows of
[`enemy-placement-conditions.tsv`](enemy-placement-conditions.tsv) whose `group` is the placement's `entry`:

- 312 placements are in groups that are always constants;
- the other 5,917 are in at least one group that the automatic selector, a bank-return selector, the selection kept
  for the lane or the script's loop register picks, or that the area start binds (7 placements).

[`rare-game-spawn-tests.tsv`](rare-game-spawn-tests.tsv) reads in words the spawn tests of the `rare game` placements:
the 879 rows [`enemy-placement-conditions.tsv`](enemy-placement-conditions.tsv) gives them, for 91 definitions, 830
of them with a test. Each test is rewritten clause by clause:

- call `0x0029(N)` is a roll of 0 to N - 1 (`0x00354BF0`: a Mersenne Twister draw, `0x00379CD0`, times N, shifted right
  by 32), so "a roll of 0 to 99 is below 20" is a 20 in 100 chance;
- call `0x05A9()` reads the debug-menu switch "100% Spawn Rare Monster" (`0x003504B0`, `0x0017D430`: byte `+0xC70`,
  command 197), whose menu the shipped game never opens ([Debug menu](../Engine-Core/debug-menu.md));
  83 rows test it alone;
- `getplaymin()` is the minutes of the play clock and `getplaytime()` the play time in seconds (`0x00349700`,
  `0x00348970`, both from the save header's hours, minutes and seconds at `+0x18` to `+0x1B` through `0x00254C90`);
  `0x00254C90(&a, &b, &c)` stores the word `+0x18` and the bytes `+0x1A` and `+0x1B` of the object at `[0x02092758]`, each
  widened to a dword, through its three pointers in that order (`0x00254C90`-`0x00254CAA`);
- `btlAtelIsPcOnPoint(-1, N)` holds while the party leader (`0x003272A0`) stands inside region record N of the map
  (`0x0050FFF0`, `0x002374E0`), and call `0x0290(-1, x, z)` is the leader's ground distance to the point x, z
  (`0x003448F0`, `0x004686D0`);
- each `g_btl_hunt_` word the tests read is set to 1 in `fon_b01` by Atak, Blok and Stok of the Hunt Club, except
  `g_btl_hunt_fon_アダマンタイマイ`, which the Huntmaster (`バンガ16`) sets, and to 2 by the `hunt_kansi.main` of
  its own zones;
- each script word (`file +0x..`, `scratch2 +0x..`) is given once per row by its writers in
  [`enemy-spawn-variables.tsv`](enemy-spawn-variables.tsv): a constant by its value, a call result by what the call
  returns, any other word by its writers. A script's file words are one area that all its actors share, so the
  stores of every actor of the script are named.

[`rare-game-catalogue.tsv`](rare-game-catalogue.tsv) has one row for each of the 80 rare game names of those 208
placements: its maps, levels, Clan Primer entry, trophy and the number of its spawn rules. 31 of them carry a Trophy
key item, which are all 31 Trophy key items (`0x80B8` to `0x80D6`); no other key item names a rare game.

[`rare-game-spawn-rules.tsv`](rare-game-spawn-rules.tsv) lists the rules, 574 rows: for each placement, each distinct
pair of how the zone script enters it and what it tests there, with the tests in the words of
[`enemy-placement-conditions-terms.tsv`](enemy-placement-conditions-terms.tsv).

A rule entered "when a bank-return selector returns it" has no roll or count test. The selector `0x002354F0` returns
the first lane of the unit whose kept record has bit `0x4` set (`0x0023555C`) and sets bit `0x4000000` of the unit
(`0x0023557E`), or returns -1; the script then enters that lane's group.

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
5. The model: the class row's dword `+0x00` is a bound id (letter class in the bits under mask `0xFF0000`, number in the bits under mask `0xFFFF`).
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
   - The count stops at 254: `0x00315820` adds one to it, holds the sum at `0xFE` (`cmova` at `0x00315884`) and stores
     the sum plus one (`0x0031588E`), so a defeat past 254 leaves the count at 254.
   - It returns another value for two numbers of its `menuhandbook.bin` list, which `0x01EED130` pairs with a
     quest: entry 251, Gilgamesh, with 167, and entry 259, Shadowseer, with 170.
   - A defeat leaves those two counts unchanged, so the 11 Gilgamesh and 3 Shadowseer definitions name an entry
     their defeats do not count.
   - The field-frame sweep `0x00316930` sets each of the two counts to 1 once `0x00315DC0` passes for its quest
     ([Achievements](../Steam-And-Achievements/achievements.md)), while the count is at most 0 (save
     byte 0 or 1, `0x003169E0`-`0x003169FA`; the byte becomes 2, `0x00316A0C`).
3. The entry page's record builder `0x005760A0(record, n)` reads entry *n*'s kill count through `0x00315420(n)`
   (`0x00576227`), which reads the same byte, save `+0x3404` + *n* (`0x0031545C`), minus 1; a number at or above
   `0x200` gives -1 (`0x00315424`-`0x0031542C`).
4. The same builder takes the entry's name from the catalog: the `i32` at `+0x00` of the 12-byte record *n*, a
   battle-text word for the Bestiary, resolved by `0x003214B0` (`0x0057617B`) and read as string 0 of its row by
   `0x002B58B0` (`0x00576185`).

The catalog is kind-7 resource `0x354`, the Bestiary family's base id at `0x00D23740` + 2 × 5 (`0x00575C60`). The US
build's kind-7 path array `0x01EC73A0`, which `0x002DF9A0` loads in its US case (`0x002DFC0A`) and stores at `0x0215F038` (`0x002DFF7F`), names
`myoshiok/us/handbook/menuhandbook_monster.bin` for it. Its 384 entry names are all words of bank 8, the monster
names. One entry serves every variant of a monster: Wolf and Alpha Wolf both count for entry 2, Wolf.

202 of the 1,143 placed definitions, in 445 placements, have `0xFFFF` at class row `+0x52` (an empty
`primer_entry`), which step 1 skips, so their defeats raise no entry's kill count. 73 of them, in 195 placements,
stand in the monsters list of an entry of [`clan-primer-entries.tsv`](../Menus-And-HUD/clan-primer-entries.tsv) through
that entry's gallery model (entries 33, 35, 278 and 377 to 383). No entry's monsters list names the other 129, in
250 placements; [`bestiary-no-primer-entry.tsv`](bestiary-no-primer-entry.tsv) lists them. By family:

- Imperial Army 49: Imperial Hoplite 15, Imperial Magus 10, Imperial Gunner 7, Imperial Swordsman 5, Imperial
  Marksman 4, Imperial Pilot 4, Vayne 2, Imperial Beastmaster 1, Larsa 1;
- Titantoise 16, all No name; Dalmascan Army 12: Dalmascan Soldier 7, Basch 3, Amalia 1, Vossler 1;
- Bangaa 12: Bangaa, Bwagi, Gijuk and Rinok 3 each; Seeq 8: Seeq 5, No name 3; Rook 8: Rook, Helm-Rook,
  Spinner-Rook and Sphere-Rook 2 each;
- ??? 8: Sephira 5, Vayne Novus 2, The Undying 1; Viera 5: Krjn 3, No name 1, Viera Huntress 1; Wolf 5, all Mastiff;
- Pirate 3: Pirate, Elza and Rikken; Judge 2: Judge Zargabaath and Judge Drace; Guardian 1: Omega Mark XII.

Nine of them share a name with an entry whose list names other definitions: the 3 Bangaa and 5 Seeq of `rbn_a`
(entries 376 and 372) and the Omega Mark XII of `gil_i` row 9 (entry 291, which names `gil_i` rows 7 and 8 and `tri_t` row 4).

The 21 definitions whose name word reads No name in the `us` text are placed by the `PRISON_` functions of `nal_a`
and `nal_b`, the `COCKATRICE_` functions of `sav_b`, the `SND_MAN_` and `SND_WOMAN_` functions of `rbn_a`, and the
`THIRD_` functions of `rui_a` and `srb_b`. Sixteen use a model from the `npc` model folder, the five of `sav_b` one
from the `monster` folder.

The `fr` `battle_pack.bin` keeps a label at each of those words: `prison_human`, `prison_bangaa`, `prison_seeq`,
`siiku_cocka`, `2kyu_simin_men`, `2kyu_simin_women`, `seeq_event` and `viera_event`. Each line's explanation gives
the word, its `fr` text, its model's folder and the zone-script functions that place it.

The 31 `bts_` test-battle scripts under `plan_map` hold the other 517 placements of the shipped scripts. The US
kind-5 array names none of them, so no area load runs them, and they are left out.

### Columns of bestiary-no-primer-entry.tsv

| Column | Holds |
|---|---|
| `same_name_entry` | for a definition whose name is also the name of a Bestiary entry, that entry and the note that its monsters list names other definitions: entry 376 for the three Bangaa of `rbn_a`, entry 372 for its five Seeq, entry 291 for the Omega Mark XII of `gil_i` row 9; `-` on the other 120 rows |

### The Clan Hall reward for a boss

Montblanc's talk in the Clan Hall (`rbn_a14`) calls `funcActor.getClearBoss`, which walks 19 bosses in a fixed
order. It takes the first boss whose defeat variable is 2 and whose bit in `g_iw_報酬あげたボスフラグ` is clear, sets
that bit and returns the boss's place k in the order. The talk then gives package `0x903B` + k with two lines that
name the fight.

- First the talk gives a clan-rank package for each rank reached since the last reward: `0x902F` to `0x903A` for
  ranks 1 to 12. It raises the rewarded rank by 1 per package and loops until it reaches the current rank.
- Then it calls the walk again after each boss package, until the walk returns -1. So one talk gives
  every boss defeated since the last visit, in the walk's order.

[`clan-hall-boss-rewards.tsv`](clan-hall-boss-rewards.tsv) lists the 19 bosses in walk order with:
- the defeat variable;
- Montblanc's lines;
- the package and what it gives;
- the bit;
- the story script steps that write the defeat, with their map and region;
- the developer and preset scripts that also write it.

### Columns of clan-hall-boss-rewards.tsv

| Column | Holds |
|---|---|
| `montblanc_lines` | the two texts the talk shows for the boss, separated by ` / `: Montblanc's line naming the fight, then the dedication of the reward in double quotes; the two Society of Antiquaries rows hold the dedication alone |
| `given_bit` | the boss's bit in `g_iw_報酬あげたボスフラグ`, the word that records a given reward: byte `order / 8`, bit value `1 << (order mod 8)`, from `byte 0 bit 0x1` for order 0 to `byte 2 bit 0x4` for order 18 |
| `defeat_set_at` | the story steps that set the defeat variable to 2, as script, actor, function and step, with the map name and region in brackets |
| `developer_or_preset_setters` | the developer test scripts (`evt_t0081` to `evt_t0505`) and the new-game set `pre_z0000` that also store the variable, as script, function and step; `-` on 10 bosses |
| `cite` | the steps behind the row: the boss's step of `funcActor.getClearBoss` in `rbn_a14` and the case of Montblanc's talk that gives the package |

### The boss fights

A boss fight is a defeat variable `g_btl_<name>` in the script that places its monsters. The variable is 1 while
the fight waits and 2 once it is won. The new-game set-up `pre_z0000` sets most of them to 1, and the fight's
`setup.battle` binds the battle to its variable.

[`story-bosses.tsv`](story-bosses.tsv) lists the 62 fights of the 156 functions that place a boss. Each row gives:
- the monsters, map and region;
- the scene that starts the fight;
- the story-counter tests that hold where it is placed;
- the first counter value stored after the battle (the store after the boss gauge opens on the same path, which
  can come before the step that writes the defeat);
- whether the boss is an Esper (13 of the fights, one per Esper);
- the Clan Hall reward;
- the steps that show each cell.

The `story_counter_link` column says how the fight touches the story counter:

| link | fights |
|---|---:|
| both (written after the battle and tested where placed) | 22 |
| written after the battle | 12 |
| tested where placed | 1 |
| not in the fight's steps | 27 |

Where a story-counter value's developer name names the battle, `link_reason` gives the value and its number of
story writes. Eight fights store a value other than the one named for them, because the counter skips the named
value; `link_reason` gives both.

### Columns of story-bosses.tsv

| Column | Holds |
|---|---|
| `story_point_before` | the story-counter (`シナリオフラグ`) tests that hold where the fight is placed, each with its steps and the developer name of the value it tests (for example `645: After the secret of the mines`); for a fight whose steps test no story-counter value, that the defeat variable is 1 there and, where `pre_z0000` sets it, the new-game step that sets it to 1 |
| `other_writers_of_1` | the stores of the defeat variable besides the new-game set in `pre_z0000`: `only the new-game set (pre_z0000)` on 39 fights; otherwise each `set to 1 by` (and `set to 0 by`) step with its condition, or, on 6 fights, the steps that set it to 2 outside the fight |
| `story_point_after` | the first story-counter value stored after the battle, in decimal and hex with its developer name, the step that stores it and the step that sets the defeat variable to 2 (34 fights); on the other 28, that the fight's function stores no story-counter value after the battle, with the defeat step |
| `cite` | the steps behind the row: the store of 2 in the defeat variable, the tests of the variable for 1, and the step that opens the boss gauge |

### The placement verbs

Every placement in the shipped scripts is one script function calling these four verbs, each with immediate
arguments (`PUSHII`, a pooled int or a pooled float):

| Verb | Handler | What it sets |
|---|---|---|
| `btlAtelSetUnit(row)` | `0x00510160` → `0x0023A3B0` | installs definition *row* OR `0x100` (`bts` at `0x0023A3E1`; `0x100` + *row* for a row below `0x100`), or `0xFFFF` for row `0xFF` (`0x0023A3D9`-`0x0023A3E7`), with `0x0023A570`, after `0x002355A0` (`0x0023A3D4`); an actor without a battle unit gets nothing (`0x0031B760`, `0x0023A3C4`-`0x0023A3CF`) |
| `btlAtelSetLevel(base, range)` | `0x0050F910` → `0x002398F0` | level `base + rand % (range + 1)` and reference level `+0x88` = `base`, through `0x0030C470`, returning 0 (`0x00239939`); the draw is the LCG `0x00328370`; refused with −1 when the actor has no unit (`0x0023990F`) or byte `[[unit + 0x6A0]]` has bit `0x1` or `0x4` set (`0x00239918`); the spawn record `+0x6A0` is read with no null test (`0x00239911`), so a unit without one faults there; `range` = −1 divides by zero at `0x00239926` and faults |
| `btlAtelSetStatus(table)` | `0x005103B0` → `0x002394C0` | 32 two-bit codes: 3 immune, 2 added at a fresh spawn, 1 added when an LCG draw is odd ([Augments](../Damage-And-Battle-Formulas/augments.md)); `+0xE90` is zeroed first (`0x002394FC`), and an actor without a battle unit gets nothing (`0x002394D9`) |
| `btlAtelSetAbility(a, b)` | `0x00510440` → `0x002390B0` | the enemy augment mask `+0xE80`: bit *j* of `a` sets augment 31 - *j*, bit *j* of `b` sets augment 63 - *j*; an actor without a battle unit gets nothing (`0x002390CA`) |

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
| `+0x02` | `u8` | spawn counter slot, `0xFF` no slot | `0x0023A570` |
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
| `+0x18` | `u32` | starting HP, 0 for no starting HP | `0x0023A410` ([Enemy spawning](enemy-spawning.md)) |
| `+0x1C` | `u16` | off-hand equipment id | `0x0023AC80` (slot 1) |
| `+0x22` | `u16` | base stat row | `0x0023A570`, `0x002FEF30` |
| `+0x24` | `u16` | growth stat row | `0x0023A570`, `0x002FEF30` |
| `+0x26` | `i16` | voice bank, negative for the model's | `0x003212E0` ([Character sound tables](../Game-Files-And-Data-Tables/character-se-tables-chse.md)) |
| `+0x28` | `u16[5]` | drop slots 1-5 | `0x003180F0` ([Loot drops](../Rewards-EXP-Gil-And-Loot/loot-drops.md)) |
| `+0x32` | `u16[3]` | steal: common, uncommon, rare | `0x00390390`, `0x0023A570` ([Steal](../Damage-And-Battle-Formulas/steal.md)) |
| `+0x38` | `u32[2]` | the ids of the model's part 8 entries 0 and 1, 0 for no entry; 0 in every row | `0x0031C000` through `0x0031BEC0` ([Actor model rebuild](../Characters-And-Objects/actor-model-rebuild.md), states 13-15) |
| `+0x40` | `u8[2]` | those entries' attach links, through the table at `0x00D107F8`; 0 in every row | `0x0031BE30` |
| `+0x42` | `u8[2]` | Monograph drop chances | `0x003180F0` |
| `+0x44` | `u16[2]` | poach: common (95 %), rare (5 %) | `0x00390680` ([Formula slots](../Damage-And-Battle-Formulas/formula-slots.md)): the common word when `0x00379CD0() % 100` is below 95, else the rare one (`0x00390690`-`0x003906AD`), for an enemy target (byte `+0x05` = 1) with a unit, kept at `[0x02EBF188]`; while the dword `+0xE60` of the console settings object `0x001D50D0()` is 0 the common word is taken and while it is 1 the rare one (`0x0017D410`, `0x0039071D`-`0x00390795`), and its constructor sets it to -1, which keeps the roll (`0x001CCE1F`); a word of `0xFFFF`, or a target that is not an enemy, leaves item 0 in `0x02AEE050` (`0x00390713`, `0x003907A3`-`0x003907AB`); the slot also sets the target's HP outright to 0 (`0x02AEE02C`, `0x003907BE`) and bit `0x80000` of the result's `+0x2C` (`0x003907C8`) |
| `+0x48` | `u16[4]` | Monograph pairs: key item, item | `0x003180F0` |
| `+0x50` | `u16[4]` | order sets for orders 0-3 | `0x0023A570` (set 0), `0x00239040`, `0x002FDDA0` ([Battle orders](../Battle-Actions/battle-orders.md)) |

The `+0x03` and `+0x15` bits, by their readers:

- `+0x03` bit `0x10`: `0x00238BF0` raises the unit byte `+0x58` to 7 ([Battle units](../Characters-And-Objects/battle-units.md));
  `0x00236210` returns the motion height without its random part (`0x002362A4`); the gambit target selector
  `0x00301AD0` tests it (`0x0030268D`).
- `+0x03` bit `0x20`: `0x00238BF0` passes it to `0x002E8A10`, which stores it as the render record's shadow kind, mask `0x3000`
  of `+0x304` ([Character lighting and shadows](../Graphics/character-lighting-and-shadows.md)).
- `0x002E8A10(actor, v)` stores `v & 3` in that mask and also sets bit `0x400000` of the render record's `+0x290`. It
  does nothing for a null actor, a null context `+0xC0`, a context whose dword `+0x00` is -1 or whose low word is
  `0xFFFF`, a record address of 0, or a record whose dword `+0x284` is 0 (`0x002E8A10`-`0x002E8A62`).
- `+0x15` bit `0x8`: `0x0031AA30` leaves the target-kind word at 0 for an enemy (`0x0031AACF`); bits `0x8` or `0x10`: it leaves the
  reach word at -1 instead of `0x01EED2D0[action kind]` (`0x0031AB39`). `0x0031AA30` runs from `0x00321060` and
  `0x00328530`, and `0x0031AB80` tail-jumps to it (`0x0031ABC5`).

`0x0031AA30(unit, _, id, out)` first stores -1 in the dword `out + 4` and 0 in the dword `out + 0`
(`0x0031AA48`-`0x0031AA58`), and answers -1 when `0x00322C50(0x14, id, 0)` refuses the id (`0x0031AA60`-`0x0031AA6F`); otherwise
it answers 0 (`0x0031AB5D`).

For the action row it calls `0x0020E600(table dword +0x0C)` on the table `[0x02EBF138]` twice, for the null test
(`0x0031AA83`) and for the value (`0x0031AA97`): the row is that section at `id * stride`, the stride being the table's
word `+0x08`, or address 0 when the table or the section is null (`0x0031AA74`-`0x0031AAAE`). A row address of 0 is not
handled: no test stands before the row reads at `0x0031AB02`, `0x0031AB10` and `0x0031AB3F`.

The target-kind dword `out + 0` becomes 3, or 4 when the action row's dword `+0x0C` has bit `0x800`, for a party
member (stats kind 0) and, unless it is the kind-1 unit named below, for a unit whose class nibble `0x00263C20(actor)`
gives is 3. It becomes 1, or 2 with that bit, for a kind-1 unit of another nibble. It keeps 0 for a kind-1 unit whose
enemy row byte `+0x15` has bit `0x8`, tested before the nibble (`0x0031AAC2`-`0x0031AAD3`), and for a unit of another
nibble with no stats record or of a kind above 1 (`0x0031AAB1`-`0x0031AB1D`).

The reach dword `out + 4` becomes `0x01EED2D0[row byte +0x1E]`, except for a kind-1 unit whose enemy row byte `+0x15`
has a bit of `0x18` (`0x0031AB20`-`0x0031AB4D`), and `0x0031A990(row, out + 8)` fills the rest (`0x0031AB51`-`0x0031AB58`). A
null unit is not handled once the id is accepted: its test leads to the read of the actor pointer `+0x10`
(`0x0031AAB1`-`0x0031AAB4`, `0x0031AAE2`).

### Colour and model variants

Two bytes of each enemy definition choose how its model looks: the variant picks one of the model's `@FOR` records,
which also sets its scale and pose entry, and the colour picks that record's option number. So every chocobo uses the
one model `m1066`, and only the colour number tells a Red Chocobo (1) from a Brown one (5).

`0x0031C540(actorId, &colour, &variant)` resolves the id to its actor (`0x003588B0`) and the actor's unit (`0x00263E30`,
`+0x30`), and reads the two bytes from the unit's definition (`[unit + 0xE60]`, `+0x12` and `+0x11`) when the
unit's row `+0x698` byte `+5` is 1. Otherwise it fails with both 0 and a non-zero return.

Both outputs are zeroed first (`0x0031C56F`, `0x0031C575`), and the id is resolved only while battle flag
`0x02089340` bit `0x10` is set (`0x0031C54A`): the answer is −1 without the flag, the actor, the unit or its row
(`0x0031C5C2`), −2 for a row whose byte `+5` is not 1 (`0x0031C592`), and 0 after a read (`0x0031C5A9`).

The model rebuild hands them on as
`0x0026D610(actor, variant, colour)` (`0x0037B77C`-`0x0037B7A5`), or as variant 1 and colour 0 when the read fails
([actor model rebuild](../Characters-And-Objects/actor-model-rebuild.md)). From there:

1. `0x0026D610` stores variant and colour at the actor's secondary `+0x14C` and `+0x14D` (`0x002E6090`).
2. The presentation set-up `0x002E28E0` passes both to `0x0042FB80` (`0x002E2986`-`0x002E2998`), whose initialiser
   `0x00420480` keeps the variant at render record `+0x5C`, 1 when it is 0 (`0x00420557`-`0x00420568`), and the colour at
   `+0x5D` (`0x0042056C`-`0x00420576`).
3. The bind `0x0041F340` hands both to the model row (`0x0041F641`-`0x0041F69E`, `0x004780C0`). `0x00504F00` matches the
   variant against the model's `@FOR` record keys (`+0xB8`; the first record's key when no key matches, 0 with no
   record or a first key of `0xFF`, `0x005050A2`-`0x005050C8`)
   ([model files](../Graphics/model-files-cm-ca.md)).
4. `0x00504F00` keeps the colour as the option number `+0xB9`
   while it is below the `@FOR` option count `+0x33` and not negative, else 0 (`0x005050DB`-`0x0050510B`).
5. The variant also picks the `@FOR` scale (`0x00504840`, record `+0x26C`) and the pose sequencer entry
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
| `+0x04` | `u8` | type, unit `+0x55`, named by word bank 13 (word `0x6800` + type: 0 Hume, 1 Humanoid, 2 Giant, 3 Dragon, 4 Beast, 5 Insect, 6 Plant, 7 Avion, 8 Amorph, 9 Fiend, 10 Elemental, 11 Warmech, 12 ???, 13 Undead, 14 Construct, 15 Ichthian); when the source unit's is 13, the Drain slot `0x0038D400` exchanges the target's HP loss and gain with the source's (`0x0038D4D9`-`0x0038D50B`), and its final block then rewrites part of them; when the target's is 13 (the slot context `+0x18`) the slot gives the amount to the target and takes it from the source (`0x0038D481`-`0x0038D4BF`, `0x0038D561`-`0x0038D5B8`); the other slots that test the target's 13 are listed below the class row ([Formula slots](../Damage-And-Battle-Formulas/formula-slots.md)) | `0x0023A570` |
| `+0x05` | `u8` | class, unit `+0x56`, the kill chain's class ([Kill chain](../Rewards-EXP-Gil-And-Loot/kill-chain.md)), named by word bank 14 (word `0x7000` + class, 64 names; class 34 is Skeleton) | `0x0023A570` |
| `+0x06` | `u16` | unit `+0x52`; 0 in every row | `0x0023A570` |
| `+0x10` | `i16` | push weight: a positive value divided by 10 is the weight the separation tick gives the body, as the party table's `+0x7A` ([Party table](../Party/party-table.md)); any other value goes over unchanged, and the -1 of 188 class rows (221 definitions use them) makes the body one an overlap never moves (`0x00314E10` gives a negative weight a share of 0) | `0x00238BF0` (`0x00238CEB`) → `0x0026DAC0` ([Movement bodies](../Movement-And-Pathfinding/movement-bodies-and-separation.md)) |
| `+0x12` | `u8` | flags: mask `0x7` the effect column; bit `0x10` actor `+0x09` bit `0x40`; bit `0x20` the view query; bit `0x40` actor `+0x08` bit `0x8` and `+0x09` bit `0x40`; bit `0x80` the pair clearance | below |
| `+0x18` | `u8` | bits `0xE` a movement group; mask `0x70` the placement height | `0x00239E10`, `0x003247F0`, the locomotion functions below |
| `+0x20` | `u8` | combo cap: hits at most this value minus 1 | `0x00388660` (`0x00388845`, [Combos](../Battle-Actions/combos.md)) |
| `+0x21` | `u8` | bit `0x2`: an enemy may back off from its target | `0x003341A0` (`0x00334204`, [Action range](../Battle-Actions/action-range.md)) |
| `+0x22` | `u8` | facing in degrees, unit `+0x64` | `0x0023A570` |
| `+0x23` | `u8` | unit `+0x68` | `0x0023A570` |
| `+0x25` | `u8` | sight radius | `0x003247F0` ([Enemy AI](../Enemy-AI-And-Gambits/enemy-ai.md)) |
| `+0x26` | `u8` | radius for units below 40 % HP | `0x003247F0` |
| `+0x27` | `u8` | unit `+0x6C` | `0x0023A570` |
| `+0x28` | `u8` | bit `0x1` the view query's height; bit `0x2` the kill chain skips it | `0x0031ADB0` (`0x0031B08D`), `0x00317ED0` (`0x00317F09`) |
| `+0x29` | `u8[5]` | absorb, halve, nullify, weak, potency | `0x002FEF30` ([Elements](../Damage-And-Battle-Formulas/elements.md)) |
| `+0x30` | `u8[16]` | read and written by no instruction (below); taken as eight little-endian pairs, each is `0xFFFF` or `0x0100`-`0x01FF` | no instruction |
| `+0x40` | `u16` | model family: the loot quantity group the kill chain's run compares, not the model (Coeurl and Grimalkin are both `m1014`, with `0x0226` and `0x139A`) | `0x00317ED0` (`0x00317F77`) |
| `+0x52` | `u16` | Clan Primer Bestiary entry, `0xFFFF` no entry (above) | `0x003171C0`, `0x0031B9A0`, `0x00329220` ([Kill rewards](../Rewards-EXP-Gil-And-Loot/kill-rewards.md)) |

The other bytes (`08`-`0F`, `13`-`17`, `19`-`1F`, `24`, `2E`-`2F`, `42`-`51`) are 0 in every row.

`0x0031B9A0(unit)` returns the class row's Bestiary entry word `+0x52` (`0x0031B9CE`-`0x0031B9D5`) only for a unit whose
stats record is of kind 1 and whose class nibble `0x00263C20(actor)` gives is not 3; for a null unit, a unit with no
stats record and every other unit it returns `0xFFFF` (`0x0031B9A9`-`0x0031B9E4`).

The `+0x12` and `+0x18` bits, by their readers:

- `+0x12` bits `0x7`: `0x00329F80(unit, action)` picks the action effect by the action's class byte `+0x21`, 0 to 8, and
  starts no effect for a class above 8 or while the unit's dword `+0x774` is not -1 (`0x00329F86`-`0x00329F93`,
  `0x00329FE7`-`0x00329FEF`).
- For a unit whose stats record `+0x698` is of kind 1, its byte `+0x05`, the value is entry
  `5 × class + (+0x12 bits 0x7)` of the table at `0x00D10720`, and a value of those bits above 4 starts no effect
  (`0x00329F99`-`0x00329FBD`, `0x0032A016`-`0x0032A026`).
- A party member, kind 0, reads the table at `0x00D106B0`, two values per class, the second for a stats record whose
  byte `+0x04` is `0x1B` to `0x27` (`0x00329FC5`-`0x00329FDE`, `0x00329FF1`-`0x0032A00C`); any other unit reads column 0 of
  `0x00D10720`.
- A value of -1 starts nothing; any other goes to `0x002EACD0(unit dword +0x08, 1, unit + 8, value)`, whose answer is
  kept at `+0x774` (`0x0032A02E`-`0x0032A045`). Row 0 of both tables holds -1 only, so class 0 starts no effect on any
  path.
- `+0x12` bits `0x10` and `0x40`: `0x00238BF0` hands bit `0x10` to `0x0026A3A0` (actor `+0x09` bit `0x40`) and bit `0x40` to `0x0026A430`
  (actor `+0x08` bit `0x8` and `+0x09` bit `0x40`), the bits `partyusecharhit` sets ([Party verbs](../Scripts-And-Script-Commands/party-verbs.md)).
- `+0x12` bit `0x20`: the view builder `0x0031ADB0` reports kind 1 instead of 2 for a target with it,
  except a target whose `+0x698` record has byte `+5` = 0, which gets kind 2 without the test
  (`0x0031B379`-`0x0031B3A1`).
- `+0x12` bit `0x80`: `0x003879C0`, `0x00390AB0` (`0x00390B93`, `0x00390C16`) and the pair clearance `0x0033D660` (`0x0033D794`)
  ([Battle locomotion](../Movement-And-Pathfinding/battle-locomotion.md)).
- `+0x18` bits `0xE`, the value 4: the target list notices every unit (`0x003248F8`), actor `+0x13` bit `0x80` is set
  (`0x00238E23`), and `0x00233EA0`, `0x00233F70`, `0x0031E880` and `0x00325260` test it too.
- `+0x18` bits `0xE`, other values: the locomotion functions `0x003357B0`, `0x00336710`, `0x00336CE0`, `0x00337470`,
  `0x003377C0`, `0x00337C10`, `0x00337D90`, `0x00338490`, `0x0033A240`, `0x0033C310` and `0x0033E1F0` compare the group with 0, 1,
  2, 4 and 5.
- `+0x18` bits under mask `0x70`: the placement height byte `+0x1F6` (`0x00239E10`, [Enemy spawning](enemy-spawning.md)).

The type `+0x04`, by its readers:

- The slot context `+0x18` holds the target unit's `+0x55` (`0x003847C0`, `0x0038487C`-`0x00384885`;
  [Damage formula](../Damage-And-Battle-Formulas/damage-formula.md#the-context)), and the formula slots test `+0x18 == 13`
  as a word (`cmp word ptr [r8 + 0x18], 0xd`, with `rbx` for `r8` at `0x0038D561` and `0x0038DE21`) at `0x00387F76`,
  `0x0038825F`, `0x003889FF`, `0x0038D10D`, `0x0038D180`, `0x0038D481`, `0x0038D561`, `0x0038D680`, `0x0038DE21`, `0x0038E09E` and
  `0x0038E7E3`.
- At `0x0038D680` a context word `+0x18` of 13 stores 1 in the dwords `0x02AEDFBC` and `0x02AEDFB8`; any other stores twice
  the target's dword `+0x48` in the dword `0x02AEE02C` (`0x0038D680`-`0x0038D6A2`).
- The drain slot `0x0038D400(source, target, context)` writes the scratch words of
  [Damage formula](../Damage-And-Battle-Formulas/damage-formula.md#the-scratch-block). A source that is its own target sets
  `0x02AEDFB8` and `0x02AEDFBC` to 1 (`0x0038D418`-`0x0038D427`); attack `0x02AEE058` below defence `0x02AEE05C` sets
  `0x02AEDFB8` to 1 and the target's HP loss `0x02AEE004` and the user's HP gain `0x02AEE018` to 0 (`0x0038D441`-`0x0038D46B`).
- Otherwise the amount is `trunc((attack - defence) * scale)`, the scale `0x02AEE054` (`0x0038D487`-`0x0038D48F`). It
  goes to the target's loss and the user's gain; against a target of type 13 (`0x0038D481`) it goes to the target's
  gain `0x02AEE008` and the user's loss `0x02AEE014` instead, while the target's loss takes the old user's loss and the
  user's gain the old target's gain (`0x0038D4A1`-`0x0038D4BF`).
- A source whose unit `+0x55` is 13 then swaps the target's loss and gain with the user's (`0x0038D4C5`-`0x0038D50B`,
  the unit kept at `[0x02EBF188]`). Reverse on the target (context `+0x08` bit `0x1000`) swaps the target's loss and
  gain, and Reverse on the source (context `+0x04` bit `0x1000`) the user's (`0x0038D52C`-`0x0038D55B`).
- A final block recomputes the amount and rewrites (`0x0038D561`-`0x0038D5F8`). Against a type-13 target the target's
  gain and the user's loss are the amount, or with Reverse on the target the target's loss is the amount and its
  gain and the user's loss -1. Against any other target the target's loss and the user's gain are the amount, or
  with Reverse on the target the target's gain is the amount and its loss and the user's gain -1.
- With Reverse on the source the user's word just written moves to the other user's word, and the first becomes
  -1: against a type-13 target the user's gain takes it and the slot returns (`0x0038D5A8`-`0x0038D5C7`); otherwise
  the user's loss takes it. The slot then calls `0x00387B00(source, target)` when the user's loss `0x02AEE014` is not
  -1 (`0x0038D602`-`0x0038D60D`).

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
| `placed_in` | the maps, as map name (region), whose us scripts place this row: the rows of [`enemy-placements-maps.tsv`](enemy-placements-maps.tsv) whose script lies in this row's area folder, with the same row; `-` when no script places it |
| `class_row`, `model`, `model_id` | the class row, its model's file name and bound id |
| `type`, `race` | class row `+0x04`, and its name in the `us` text: battle-text word `0x6800` + type, word bank 13 |
| `class`, `family` | class row `+0x05`, and its name in the `us` text: battle-text word `0x7000` + class, word bank 14. The `us` text of class 46 carries the prefix "NOT USED" ("NOT USED Wings"; the `de` text is Flugwesen), and the column keeps it as shipped |
| `primer_entry`, `primer_name` | class row `+0x52`, the Clan Primer Bestiary entry (empty for no entry), and that entry's name in the US Bestiary catalog |
| `model_family` | class row `+0x40` |
| `base_row`, `growth_row` | definition `+0x22`, `+0x24` |
| `hp` ... `magick_evade` | the stats `0x002FEF30` builds at a placement's base level without order adjustments: the base row plus the gear's bonus records, Attack and evades from the gear unless `+0x15` says otherwise, capped as on [Stats](../Damage-And-Battle-Formulas/stats.md) |
| `*_per_level` | the growth row's value added per level above the base |
| `hp_per_level` | growth row `+0x20` (`u32`), the max HP added per level: 0 to 20,000, 0 on 309 rows |
| `mp_per_level` | growth row `+0x24` (`i16`), the max MP per level: 0 to 150 |
| `strength_per_level`, `magick_power_per_level`, `vitality_per_level`, `speed_per_level` | growth row `+0x26` to `+0x29`, one byte each: Strength 0 to 4, Magick Power 0 to 3, Vitality 0 to 7, Speed 0 to 3 per level |
| `attack_per_level` | growth row `+0x2D` when definition `+0x15` has bit `0x1`, so Attack comes from the rows; 0 otherwise, since Attack then comes from the gear (0 to 4) |
| `defense_per_level`, `magick_resist_per_level`, `evade_per_level` | growth row `+0x2B`, `+0x2C` and `+0x2A`: 0 to 4, 0 to 4 and 0 to 3 per level |
| `exp`, `lp`, `gil`, `clan_points` and their `_per_level` | the base and growth rows' rewards |
| `exp_per_level`, `lp_per_level`, `gil_per_level`, `clan_points_per_level` | growth row `+0x34` (EXP, 0 to 666), `+0x2F` (LP, 0 on all 1,146 rows), `+0x30` (gil, 0 to 10) and `+0x00` (clan points, 0 to 520) per level |
| `weak`, `absorb`, `halve`, `nullify`, `potency` | the class row's affinity bytes ORed with the gear's attribute records |
| `immune`, `auto_status`, `auto_status_half` | the status codes 3, 2 and 1 of the placements' `btlAtelSetStatus` tables |
| `augments` | the augments `btlAtelSetAbility` sets, each by its term on [Augment list](../Damage-And-Battle-Formulas/augment-list.md) with its id |
| `steal_*`, `drop_1`-`drop_5`, `poach_*` | the items by name |
| `steal_common`, `steal_uncommon`, `steal_rare` | definition `+0x32`, `+0x34` and `+0x36` by name; an id whose top four bits are `0xE` is gil and reads `N gil`, where N is the low twelve bits; empty for `0xFFFF` (215, 181 and 122 rows) |
| `drop_2`, `drop_3`, `drop_4` | definition `+0x2A`, `+0x2C` and `+0x2E`, drop slots 2 to 4, by name; empty for `0xFFFF` (526, 488 and 554 rows) |
| `poach_common`, `poach_rare` | definition `+0x44` (the 95 % item) and `+0x46` (the 5 % item) by name; empty on 530 rows each |
| `monograph_1`, `monograph_2` | item, chance and the key item that must be held |
| `weapon`, `weapon_element`, `weapon_status`, `off_hand` | the two equipment ids by name; the main-hand row's element and on-hit status |
| `variant` | definition `+0x12` (the colour) then `+0x11` (the model variant), as "colour, variant" |
| `start_hp` ... `class_bytes30` | the remaining fields as the layout tables above name them, raw; `push_weight` is class row `+0x10` divided by 10, `+0x10 / 10`, and `class_bytes30` the sixteen bytes of `+0x30` |
| `flags03` | definition `+0x03` in hex, the bits of the layout above: `0x3` the tracked-HP class, `0x10` the height and AI tests, `0x20` the shadow kind |
| `flags15` | definition `+0x15` in hex: bit `0x1` Attack and weapon evade from the rows, `0x2` shield and magick evade from the rows, `0x4` the unit flag, `0x18` the target-information query |
| `scale_x`, `scale_y`, `scale_z` | definition `+0x0A`, `+0x0C` and `+0x0E` (`i16`), the model scale in percent: 55 to 300, 100 on 942 rows; the three are equal on 1,145 of the 1,146 rows |
| `anim_set` | definition `+0x13`, the animation set: 16 on 18 rows and 19 on 3; empty for `0xFF`, the weapon's set, on 1,125 |
| `class_flags12` | class row `+0x12` in hex: mask `0x7` the effect column, bits `0x10`, `0x20`, `0x40` and `0x80` as the class row table says |
| `class_kind18` | class row `+0x18` in hex: bits `0xE` the movement group, mask `0x70` the placement height |
| `class_flags21` | class row `+0x21` in hex, `0x00` to `0x03`; bit `0x2` lets an enemy back off from its target |
| `scale2` | class row `+0x27`, which `0x0023A570` copies to unit `+0x6C`: 20 to 45 |
| `low_hp_radius` | class row `+0x26`, the radius `0x003247F0` uses for units below 40 % HP: 0 to 35 |
| `class_flags28` | class row `+0x28` in hex, `0x00`, `0x02` or `0x03`: bit `0x1` the view query's height, bit `0x2` the kill chain skips the unit |
| `explanation` | a one-line summary of the placements, HP, elements, rewards and steals; for a No name line also its name word, that word's `fr` text, its model's folder, the functions that place it and its Clan Primer entry |

A value that differs between placements of one definition is listed once per variant, separated by ` / `.

### Columns of rare-game-catalogue.tsv

| Column | Meaning |
|---|---|
| `name` | the rare game's name |
| `placements` | its placements of kind `rare game` |
| `areas` | the area files that place it |
| `maps` | each map of its placements with region and zone |
| `levels` | the level ranges of its bestiary rows |
| `clan_primer_entry` | the Clan Primer entry number and name of its bestiary rows |
| `trophy` | the Trophy key item whose `sources` cell in key-item-list.tsv names it, id and name; `-` when no key item names it |
| `trophy_use` | the trophy's `used_for` cell; `-` with no trophy |
| `spawn_rules` | the number of distinct spawn rules over its placements, a rule counted once for each script that holds it |
| `spawn_rule_rows` | where the rules are: the rows of rare-game-spawn-rules.tsv with this name |

### Columns of rare-game-spawn-rules.tsv

| Column | Meaning |
|---|---|
| `name` | the rare game |
| `script`, `function`, `group`, `row` | the placement: the zone script, the placing actor, its `entryNN` function and the definition's row |
| `map_name`, `region`, `zone` | where the placement is |
| `rule` | the rule's number within the placement, from 1 |
| `decided_by` | the `spawnNN` and `respawnNN` functions with a path that reads as this rule |
| `entered_as` | how those paths enter the placement: the source of the group and of the lane, from the `lane` column of enemy-placement-conditions.tsv |
| `spawn_rule` | what those paths test: the story, weather, count, random and other texts of enemy-placement-conditions-terms.tsv, joined by `;`; `no test` when they test nothing |

## Related

- [Area battle data (.ard and .nmb): the per-area file of enemy definitions, class rows, stat rows, gambit order sets, motion overrides and preloaded models, and its companion](../Game-Files-And-Data-Tables/ard-area-battle-data.md)
- [Battle unit construction: the party and enemy definition tables, the stats record a unit gets, the kind byte and the type partition](../Characters-And-Objects/battle-unit-construction.md)
- [Stats: how max HP, MP, Strength, Magick Power, Vitality, Speed, Attack Power, Defense, Magick Resist and evade are built, and their caps](../Damage-And-Battle-Formulas/stats.md)
- [Augments: how a unit's augments, auto-statuses and status immunities are rebuilt from its character, gear, licenses and an enemy's script](../Damage-And-Battle-Formulas/augments.md)
- [Loot drops: drop roll, item slots, quantities, drop tables and the chain bonus](../Rewards-EXP-Gil-And-Loot/loot-drops.md)

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Actor entity: `0x002E6090` is called by `0x00265B60`; those functions are documented on
  [actor record](../Characters-And-Objects/actor-record.md).
- Combat: `0x00263E30` is called by `0x003206E0`; those functions are documented on
  [battle units](../Characters-And-Objects/battle-units.md).
- Input: `0x001D50D0` is called by `0x00197160`, `0x00197790`, `0x00197800`; those functions are documented on
  [debug menu](../Engine-Core/debug-menu.md).
- Items equipment shops license: `0x00236C30` calls `0x00238660`; those functions are documented on
  [authored data tables](../Game-Files-And-Data-Tables/authored-data-tables.md).
- Save load settings: `0x00865AE0` is called by `0x00866200`; those functions are documented on
  [save file format](../Saving-Loading-And-Settings/save-file-format.md).
- World area: `0x00236C30` calls `0x003847B0`; those functions are documented on
  [authored data tables](../Game-Files-And-Data-Tables/authored-data-tables.md).
