---
title: "Area battle data (.ard and .nmb): the per-area file of enemy definitions, class rows, stat rows, gambit order sets, motion overrides and preloaded models, and its companion"
kind: "format"
category: "Game files and data tables"
addresses: "0x003EA6E0, 0x00264ED0, 0x003EA820, 0x003EA710, 0x0023A160, 0x003845F0, 0x003846F0, 0x02B5E0B8, 0x02B5E0C0, 0x003DCF00, 0x02B58178, 0x003DCA30, 0x02B58188, 0x02B58180, 0x003DCBC0, 0x003EA650, 0x0035A3A0, 0x0035AC60, 0x002628B0, 0x0025AFC0, 0x0037C910, 0x0037C3F0, 0x003DC8D0, 0x02B580B0, 0x0032FC30, 0x02EBF150, 0x02EBF168, 0x02EBF120, 0x02EBF148, 0x02EBF140, 0x003EA6B0"
---

## What the player sees

Which monsters an area can field, how strong each is at each level, what it can steal and drop
from, and which gambits it follows all come from the area's `.ard`. Entering a new area swaps the
whole set; an area without one has no enemy definitions at all.

## Where it comes from

Each area's file is `ps2data/plan_master/<tree>/plan_map/<area>/area/<area>.ard`, resource kind `0x15`
(21), file `area × 2`. The `in` and `ch` trees hold byte-identical copies; the Korean and Chinese
builds name the files through their own kind-21 path array (see
[file size tables](file-size-tables-fst.md)).

Beside it is `<area>.nmb` (kind `0x1A`, 26).

The area number comes from the map-reference row: `0x00264ED0` returns the `u16` at `+4` of row `n` of
the table at `[0x02099D88]`. The rows are 8 bytes each from the offset the table holds at `+0x04`
(`0x00264EE9`-`0x00264EF0`), with no bounds check on `n`. It returns 0 while `[0x02099D88]` or `[0x02099D90]` is
null, or when the row's address comes out 0 (`0x00264ED7`, `0x00264EE4`, `0x00264EF4`, `0x00264EFE`).

## Layouts

All multi-byte fields are little-endian.

FF12AR03 header (`0x30` bytes, offsets from the start of the file):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `char[8]` | 'FF12AR03' | never read |
| `+0x08` | `u32` | dword08 | 0 |
| `+0x0C` | `u32` | trailer offset | 0 = no trailer |
| `+0x10` | `u32[8]` | section directory | slot k at `+0x10` + 4k, 0 = absent |
| `+0x10` | `u32` | slot 0 | st2e, 84-byte class rows -> `0x02EBF150` |
| `+0x14` | `u32` | slot 1 | order-set directory -> `0x02EBF168` |
| `+0x18` | `u32` | slot 2 | st2e, 88-byte enemy definitions -> `0x02EBF120` |
| `+0x1C` | `u32` | slot 3 | never read |
| `+0x20` | `u32` | slot 4 | never read |
| `+0x24` | `u32` | slot 5 | st2e, 56-byte base stat rows -> `0x02EBF148` |
| `+0x28` | `u32` | slot 6 | st2e, 56-byte growth stat rows -> `0x02EBF140` |
| `+0x2C` | `u32` | slot 7 | motion-file overrides -> `0x02B58178` |

Slot 1:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u16` | count |  |
| `+0x02` | `u16` | word02 | 100 (in all 166 area files) |
| `+0x04` | `...` | offsets | count + 1 u32 offsets from the section (the last is the end) |

Slot 7, then count records of `0x10`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | count |  |
| `+0x04` | `u8[12]` | bytes04 | 12 bytes |

Slot 7 record (`0x10`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` |  | bound id |
| `+0x04` | `u16` |  | weapon class |
| `+0x06` | `u16` | motion |  |
| `+0x08` | `u16` |  | file index |

Trailer, then count records:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | count |  |

Trailer record:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` |  | bound id |
| `+0x04` | `u32` |  | lane mask |

.nmb:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u16` | count |  |
| `+0x02` | `u16` | version | 100 |
| `+0x04` | `...` | offsets | u32 offsets[count + 1] from the file start (the last is the file size), then the entries |

The `st2e` tables use the shared table header ([authored data tables](authored-data-tables.md)).
The fields of the enemy definitions and class rows are on
[battle unit construction](../Characters-And-Objects/battle-unit-construction.md), and those of the base and
growth rows on [stats](../Damage-And-Battle-Formulas/stats.md) and
[EXP, LP and level-ups](../Rewards-EXP-Gil-And-Loot/exp-lp-and-level-ups.md).

## Shipped data

| Fact | Value |
|---|---|
| files | 166 per tree, 224 to 35,632 bytes, all `FF12AR03` |
| areas the executable names | 215 per tree; 49 ship no file, and every shipped file is named |
| directory | slots 0, 1, 2, 5, 6 and 7 present in all 166; slots 3 and 4 absent in all |
| slot 0 rows | 954 in all, 84 bytes |
| slot 2 rows | 1,146 in all, 88 bytes |
| slot 5 rows | 1,119 in all, 56 bytes |
| slot 6 rows | 619 in all, 56 bytes |
| slot 1 counts | 0 to 24 order sets per area |
| slot 7 records | 1,773 in all |
| `pc_skillmotion.bin` | 544 bytes, `in` and `ch` identical: count 33, then 33 slot-7 records; its twelve bytes after the count and each record's `+0x0A`-`+0x0F` are 0 |
| its records | 11 character models with three motions each, 3000 to 3017, weapon class 1 in all; 3009-3011 on five models and 3012-3014 on two; 33 different files, 18 of them in the archive |
| trailers | 140 files, 998 records; the other 26 have offset 0 |
| trailer model letters | `w` 564, `m` 278, `n` 140, `s` 13, `c` 3 |
| section 19 (`us` scripts) | 271 carry an `FF12AR03` block, `+0x2C` = `0x30` in all, 2,116 slot-7 records in all; 266 with a trailer |
| `.nmb` files | 166 per tree, byte-identical, version 100, `8 + 7 × count` bytes |
| `.nmb` counts | 0 to 22; equal to the `.ard`'s slot 2 row count in all 166 |
| `.nmb` entries | 1,146: `12 BA 00` 1,120 and `12 BB 00` 26, each a one-glyph two-byte string. Read as text (`0x002AC2F0`; the lead-byte tables `0x00916570` and `0x009165B0` both hold `0x2A0` for lead `0x12`), they are glyphs 826 and 827, which the Japanese font `jp/font00` draws as the digits `0` and `1`: one digit per enemy definition. The 26 ones are `bds_e` 1-4, `bhm_c` 5-9, `bhm_d` 0, `dor_b` 1-2, `mrm_e` 1, `rui_c` 1, `tri_d` 1, `tri_f` 10-11, `tri_q` 7-10 and `tri_t` 5-9 |

Every row of the area files is in six tables, and `pc_skillmotion.bin`'s in a seventh. The `ch` and `in` copies are
byte-identical. The 1,146 enemy
definitions are the [bestiary](../Enemy-Spawning/bestiary.md)'s rows, and the 1,422 order sets are on
[enemy order sets](../Enemy-AI-And-Gambits/enemy-order-sets.md).

| Table | Rows | One row per |
|---|---:|---|
| [`ard-area-battle-data-files.tsv`](ard-area-battle-data-files.tsv) | 166 | area file: size, SHA-256, trailer offset, the rows of each section, and its `.nmb`'s size, count and SHA-256 |
| [`ard-area-battle-data-class-rows.tsv`](ard-area-battle-data-class-rows.tsv) | 954 | slot 0 class row |
| [`ard-area-battle-data-stat-rows.tsv`](ard-area-battle-data-stat-rows.tsv) | 1,738 | slot 5 base row (1,119) or slot 6 growth row (619) |
| [`ard-area-battle-data-motion-overrides.tsv`](ard-area-battle-data-motion-overrides.tsv) | 1,773 | slot 7 record |
| [`ard-area-battle-data-pcskill-records.tsv`](ard-area-battle-data-pcskill-records.tsv) | 33 | record of `pc_skillmotion.bin`: the model's name, and the kind `0x1E` file its index names, with whether the archive carries it |
| [`ard-area-battle-data-trailer-records.tsv`](ard-area-battle-data-trailer-records.tsv) | 998 | trailer record: bound id and lane mask |
| [`ard-area-battle-data-nmb-entries.tsv`](ard-area-battle-data-nmb-entries.tsv) | 1,146 | `.nmb` entry: its offset and bytes |

- The class row columns are the fields of the class row on
  [battle unit construction](../Characters-And-Objects/battle-unit-construction.md), in offset order: `model` `+0x00`
  to `species` `+0x52`, with `absorb`, `halve`, `nullify`, `weak` and `potency` the five affinity bytes `+0x29`.
- The stat row columns: `score` `+0x00` ([kill rewards](../Rewards-EXP-Gil-And-Loot/kill-rewards.md)),
  `shield_evade` `+0x02`, `magick_evade` `+0x03`, `hp` `+0x20`, `mp` `+0x24`, `strength` to `magick_resist`
  `+0x26` to `+0x2C`, `attack` `+0x2D`, `weapon_evade` `+0x2E`, `lp` `+0x2F`, `gil` `+0x30` and `exp` `+0x34`
  ([stats](../Damage-And-Battle-Formulas/stats.md), [EXP, LP and level-ups](../Rewards-EXP-Gil-And-Loot/exp-lp-and-level-ups.md)).
- The bytes no field covers are 0 in every row: class row `+0x08`-`+0x0F`, `+0x13`-`+0x17`, `+0x19`-`+0x1F`,
  `+0x24`, `+0x2E`-`+0x2F` and `+0x42`-`+0x51`; stat row `+0x04`-`+0x1F`; slot 7's twelve bytes after the count and
  each record's `+0x0A`-`+0x0F`.

## Loader behaviour

### When an area loads

`0x0032FC30(slot, n)`, for manager slot 0, calls `0x003EA6E0(n, force)`, which reads the area number with
`0x00264ED0` and returns at once when it equals the loaded one (`0x02B5E0B8`) and `force` is 0. The force
byte is never set, so re-entering the same area keeps the file.

Otherwise `0x003EA820(area)`:

1. pre-reads the first `0x800` bytes of kind `0x15` file `area × 2 + 1`, the path
   `<area>\area\<area>.fpk`, through `0x0032EB40` (which reads only a file larger than `0x800`; no such
   file ships);
2. sizes the `.ard` with `0x0032E400(0x15, area × 2)`;
3. if a file is loaded (root `0x02B5E0C0` non-null, `0x003EA883`, `0x003EA98D`), frees it (`0x003697F0`), sets the root to
   0 and `0x02B5E0B8` to −1, clears the motion overrides (`0x003DCF00(0)`) and unbinds the five tables
   (`0x0023A160(category, 0)`);
4. with a size of 1 or more, clears the motion overrides and unbinds them again (`0x003EA8DA`-`0x003EA90D`), allocates
   the size (`0x0036A100`), tags the block `..\..\katano\atelareaload.c` and files the read with completion
   `0x003EA710`, recording the area in `0x02B5E0B8` (`0x003EA984`);
5. with a null block from `0x0036A100` instead, files no read and leaves `0x02B5E0B8` as step 3 left it (`0x003EA941`).

A file that is missing or empty leaves every table null. The call runs in arena 4: it pushes it first
(`0x0036C1D0(4, 5)`, `0x003EA83B`) and pops it with its closing jump to `0x0036C140` (`0x003EA9F7`).

At start-up `0x0032F430` runs `0x003EA6B0` (`0x0032F697`): the loaded area `0x02B5E0B8` becomes -1, the two
roots `0x02B5E0C0` and `0x02B5E0C8` 0, and both motion-override tables are cleared (`0x003DCF00(0)`,
`0x003DCF10(0)`).

### Binding the sections

`0x003EA710(file)` first labels the block `AREA` with the loaded area `[0x02B5E0B8]` (`0x0036C660`,
`0x003EA724`-`0x003EA736`). It binds each section as the file's base plus its directory offset, with no bounds
check and no magic check:

| Directory slot | Category | Binder | Null when the offset is 0 |
|---|---|---|---|
| 0 | 0 → `0x02EBF150` | `0x003845F0` | no |
| 1 | 1 → `0x02EBF168` | `0x003846F0`, depth 0 | no |
| 2 | 2 → `0x02EBF120` | `0x003845F0` | no |
| 7 | `0x003DCF00` → `0x02B58178` | stored as is | yes |
| 5 | 3 → `0x02EBF148` | `0x003845F0` | yes |
| 6 | 4 → `0x02EBF140` | `0x003845F0` | yes |

It then records the block as the file root (`0x02B5E0C0` = the file, `0x003EA809`). The binders add the section's
address to the offsets inside it, so the loaded block is no longer a copy of the file.

### The second area root (EBP section 19)

A script container (`.ebp`) can carry a second `FF12AR03` block in directory slot 19
([script container](../EBP-Script-Files/ebp-script-container.md)). When the container arrives,
`0x003304A0` passes it to `0x003320D0` (`0x00330666`), which drops the manager slot and jumps to `0x003EAA00`:

1. a block already held is unbound (`0x003DCF10(0)`) and released (`0x00331880`);
2. the new block becomes root 1 (`0x02B5E0C8`);
3. its directory slot 7 (`+0x2C`) becomes the third motion-override table `0x02B58180` (`0x003DCF10`), or 0
   when `+0x2C` is 0.

Only `+0x2C` and the trailer offset `+0x0C` of this block are read; its `st2e` slots are never bound.

### Motion-file overrides

`0x003DCA30(model, motion, class, &kind, &file)` picks the file of an action motion, always of kind
`0x1E`. It looks for the model and motion in three tables, in order:

1. the global table `0x02B58188` (model and motion only), loaded at start-up by `0x003DCBC0` from kind 9,
   file 5 (tagged `PCSkill`, `pc_skillmotion.bin`), laid out like slot 7;
2. the area's slot 7 (`0x02B58178`), matching model, motion and weapon class;
3. the table `0x02B58180` installed with the second area root (`0x003DCF10`), matching model, motion and weapon
   class (`0x003DCB16`-`0x003DCB29`).

The first match gives the file index; no match gives −1. `0x003DCA30` writes the kind `0x1E` first (`0x003DCA49`)
and returns 1 when the global table answers (`0x003DCA9C`) and 0 otherwise (`0x003DCB3B`, `0x003DCB58`, `0x003DCB83`).
A null table or a count of 0 is passed over (`0x003DCA5A`, `0x003DCA68`, `0x003DCABB`, `0x003DCAC9`, `0x003DCB03`,
`0x003DCB11`).

Besides requesting the file, `0x003DCBC0` zeroes each of the sixteen skill-motion entries at `0x02B57F70` except its id
`+0x08`, set to `i | 0x10`, and its index `+0x13`, set to `i` (`0x003DCBE0`-`0x003DCC0F`). It sets the class byte
`+0x0A` of the sixteen size-cache entries at `0x02B580B0` to `0xFF` (`0x003DCC20`), zeroes `0x02B58174`, sets `0x02B58170`
to 1 and nulls `0x02B58180`, `0x02B58178` and `0x02B58188` (`0x003DCC31`-`0x003DCC52`).

With a size above 0 it allocates the buffer in arena 4 with tag 3 (`0x0036C1D0(4, 5)`, `0x0036C1A0(3)`,
`0x0036A190`), labels it and files the read with completion `0x003DC330`, which stores the buffer in `0x02B58188`.

### Preloading the trailer's models

`0x003EA650(n)` returns root `n`'s trailer (`n` 0 or 1, the `.ard` and the second area root): the root plus its
offset `+0x0C` (`0x003EA67E`-`0x003EA688`). It returns 0 for an `n` above 1 as unsigned (`0x003EA657`), a null root
(`0x003EA66C`) or an offset of 0 (`0x003EA679`).

The task `0x0037C3F0`, which `0x0037C910` installs (called from `0x00261F90`, `0x003473A0` and `0x00359800`), walks three
lists in turn: root 0's trailer, root 1's, and, when it was started with argument 1, the `{id, mask}` table at the
offset that `+0x80` of manager slot 0's loaded data holds (`0x0037C461`-`0x0037C481`). For each record it:

1. sets bit `0x400` of the busy mask `0x022CB720` (`0x003601B0(10)`, `0x0037C4CB`);
2. finds or creates the model's name binding (`0x002EAE20`) and marks it (`0x002EBD40`); a list 2 id first goes
   through `0x002E9A60` with manager 0 bound (`0x0037C4E9`-`0x0037C515`);
3. waits until the model is loaded (`0x002E4C20`), then passes on to the next record when the mask is 0
   (`0x0037C566`-`0x0037C594`);
4. requests each lane whose bit is set in the mask (`0x002EB5D0`, `0x002ECA30`) and waits until it is
   loaded (`0x002E4C30`). The lanes go 0 to 31; a lane for which `0x002EB5D0` answers 0 gets no request and no
   wait (`0x0037C5F7`-`0x0037C5FE`).

When the lists end it calls `0x003601C0(10)` and removes itself: the state is the task's counter `+0x00`, and
state 10 equals the length 10 that `0x0037C910` stores, so the runner ends the task after that step (`0x002F1826`).

`0x0037C910(argument)` clears the task's words and stores the argument (`0x0037C918`-`0x0037C932`). It takes a task
(`0x002F16B0`) into `0x02ADD968` and runs `0x002E63D0` and `0x002E6570`, which clear bit `0x10` of `+0x19` in the
binding entries and zero the lane records' `+0x40`. With a task it sets the counter `+0x00` to 0, the length
`+0x04` to 10, the end routine to 0, the step routine to `0x0037C3F0` and the step `+0x1C` to 0
(`0x0037C95A`-`0x0037C972`); with all 32 tasks taken it installs nothing (`0x0037C958`).

The field set-up `0x00261F90` passes 1 (`0x00261FC1`), and `0x003473A0` and the entry-read step `0x00359800` give it 0.

The task runs as eleven states (jump table `0x0037C6F8`), and one call steps through them until it has to wait or
the walk ends:

- before each state a null trailer, or for list 2 a null slot 0 data pointer, an offset of 0 or a count of 0, sends
  it to state 9 (`0x0037C430`-`0x0037C4A5`); a trailer's count is first compared in state 8, so a trailer with count 0
  still has its first record read;
- a model or lane that is not loaded yet returns to the runner in state 2 or 6 (`0x0037C55E`, `0x0037C63F`), and a
  state above 10 returns at once (`0x0037C4B6`);
- state 8 adds 1 to the record index `0x02ADD950` and goes back to state 0 while it is below the list's count
  (`0x0037C661`-`0x0037C6B5`);
- its state 9 moves to the next list: it zeroes the record index `0x02ADD950` and adds 1 to the list
  index. The walk ends after list 1, or after list 2 when the argument was 1;
- State 10 then clears `0x02ADD968` and the argument (`0x0037C6C3`-`0x0037C6D4`).

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02ADD955` | `i8` | 0 (zero-filled tail of `.data`) | the list being walked: 0 root 0's trailer, 1 root 1's, 2 the `{id, mask}` table at the offset that `+0x80` of manager slot 0's data holds | `0x0037C910`, 0 (`0x0037C932`); the task `0x0037C3F0`, 1 more (`0x0037C6A8`) | the task `0x0037C3F0`: `0x0037C430`, `0x0037C4E0`, `0x0037C566`, `0x0037C5AD` and `0x0037C661`, which compare it with 2; `0x0037C493`, as the root number passed to `0x003EA650` (sign-extended); `0x0037C689`, to step it |
| `0x02ADD958` | `void*` | 0 (zero-filled tail of `.data`) | the current record's name binding, the answer of `0x002EAE20` | the task `0x0037C3F0` (`0x0037C536`); `0x0037C910`, 0 (`0x0037C924`) | the task: `0x002E4C20` (`0x0037C550`), `0x002EB5D0` (`0x0037C5D9`), `0x002ECA30` (`0x0037C60B`) and `0x002E4C30` (`0x0037C631`) |
| `0x02ADD960` | `void*` | 0 (zero-filled tail of `.data`) | the answer of `0x002EB5D0(binding, lane)` for the lane being tried; a non-zero answer sends the lane to `0x002ECA30` | the task (`0x0037C5ED`); `0x0037C910`, 0 (`0x0037C92B`) | the task, from the register it stores (`0x0037C5F4`) |
| `0x02ADD970` | `u32` | 0 (zero-filled tail of `.data`) | the task's argument: 1 adds the third list | `0x0037C910`, the argument (`0x0037C918`); the task, 0 at its end (`0x0037C6D4`) | the task (`0x0037C695`), which makes the list limit 3 when it is 1 and 2 otherwise |

When a manager slot is unloaded (slots 1–3 in `0x002628B0`, slot 0 in `0x0025AFC0`, which `0x0032F850` and
`0x0032FB70` call), the game:

1. runs `0x0035A3A0`, which, for each trailer record of both roots whose model is already loaded
   (`0x002E4C20`), sets the binding's keep bit (`+0x19` bit `0x1`) and the hold bits of lane 0 and of
   every lane in the mask (`0x002ECAB0(id, lane, 1)`);
2. releases the area's models (`0x002E4000`, `0x002E3E20`), which the keep bit and hold bits survive; `0x0025AFC0`
   makes this step only while the byte `0x02099DA0` is 0 (`0x0025AFFB`-`0x0025B017`);
3. runs `0x0035AC60`, which clears the keep bits and hold bits again.

So a model the trailer names stays loaded across the change instead of being unloaded and read
again.

In `0x0035A3A0` a record with id 0, or whose binding `0x002E99C0` does not find, is passed over (`0x0035A3EA`,
`0x0035A3FF`). The holds need a positive id: each set mask bit `i`, 0 to 31, holds lane `i` and then lane 0
(`0x0035A422`-`0x0035A445`), so a mask of 0 holds no lane. `0x0035AC60` also passes over id 0 (`0x0035ACA7`), clears
the keep bit of every other record whose binding is found, loaded or not (`0x0035ACB9`-`0x0035ACBE`), and for each
set mask bit of a positive id releases lane `i` and then lane 0 (`0x002ECAB0(id, i, 0)`, `0x002ECAB0(id, 0, 0)`,
`0x0035ACE3`, `0x0035ACEF`).

`0x0025AFC0(slot)` points the current manager `0x02099D70` at `0x02098E10 + slot × 0x288` (`0x0025AFE1`) and puts the old
value back before it returns (`0x0025B055`); for a slot other than 0 it does nothing more (`0x0025AFEA`). For slot 0
it runs `0x0035A270(0)` and `0x0035A490` before step 1, which set further keep bits and lane holds, and runs
`0x0035AD40` before step 3.

After step 3 it runs `0x0035AB50(0)`; `0x0035AD40` and `0x0035AB50` clear keep bits and lane holds. It then zeroes
`0x02099DA0` and `0x02099DA6` (`0x0025B02F`, `0x0025B036`) and ends with `0x002EA870(0)`, `0x002EA690`, `0x002ECBE0(0)` and
`0x002EBDE0(0)`.

### The .nmb request

Of the 51 read requests in the executable, the one that passes kind `0x1A` as a constant is in
`0x00324510`, which would build a buffer from 301 files (`0x0032E620(0x1A, i, …)` for `i` below `0x12D`)
but never starts: nothing stores the state that begins the build
([authored data tables](authored-data-tables.md)).

`0x003DC8D0(model, motion, class, &fromGlobal, &failed)` returns a motion file's size. It sets `failed` to 0
(`0x003DC8FE`) and looks for the three keys among the sixteen entries at `0x02B580B0` (`0x003DC904`-`0x003DC926`). On a
hit it writes the entry's byte `+0x0B` to `fromGlobal`, sets `failed` to 1 when the cached size `+0x04` is
negative, and returns that size (`0x003DC9B8`-`0x003DC9CA`).

On a miss it fills entry `[0x02B58174]` with the keys and size −1 and asks `0x003DCA30`, keeping its answer (1 when
the global table matched) in `+0x0B` (`0x003DC95F`-`0x003DC969`):

- no file: the entry's class byte becomes `0xFF`, `fromGlobal` gets the answer, `failed` becomes 1, the index
  stays, and it returns −1 (`0x003DC9DD`-`0x003DC9F1`);
- a file: `0x0032E400(0x1E, file)` gives the size, stored at `+0x04` (`0x003DC977`-`0x003DC97C`). A negative size sets
  `failed` to 1 and is returned with `fromGlobal` unwritten and the index unchanged (`0x003DC9E6`); the entry keeps
  its keys, so a later hit returns that size until a miss refills the entry;
- a size of 0 or more goes back with `fromGlobal` set from `+0x0B` (`0x003DC983`-`0x003DC987`) and the index advanced.

The cache's next-entry index:

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02B58174` | `i32` | 0 (zero-filled tail of `.data`) | the next of the sixteen 12-byte motion-size cache entries at `0x02B580B0`. On a miss `0x003DC8D0` fills entry `[0x02B58174]` (`0x003DC928`-`0x003DC953`) and, once the file and its size are found, advances the index to `(index + 1) mod 16` (`0x003DC989`-`0x003DC99F`, a signed remainder of a value that stays 0 to 15) | `0x003DCBC0`, 0 (`0x003DCC31`); `0x003DC8D0` (`0x003DC99F`) | `0x003DC8D0` (`0x003DC928`, `0x003DC989`) |

## Modding notes

- Keep slots 0, 1 and 2: they are bound even when their offset is 0, which binds the header itself
  as a table and corrupts it.
- Slots 5, 6 and 7 may be 0; the tables are then null, and any enemy definition that needs them
  reads address 0.
- Every offset inside a section is relative to that section; nothing checks it against the file size.
- The game does not reload the `.ard` when the party re-enters the area it is already in.
- An override in slot 7 applies only where the global table has no entry for the model and motion.
- List a model in the trailer to have it loaded with the area and kept into the next one; the lane
  mask picks which of its parts.
- Give a model, motion and weapon class the same motion file size in every area: `0x003DC8D0` keeps the
  sizes of up to sixteen recent motion lookups at `0x02B580B0`, keyed by those three and never cleared
  after start-up, and a later request reuses the cached size.
- `pc_skillmotion.bin` is read once at start-up (`0x003DCBC0`) into a buffer of its kind 9 size from the language's
  size table (`0x003DCC59`), so a grown file needs its new size in every `.fst`. A size of 0 or less leaves the
  global table empty, and every lookup goes to the area's tables (`0x003DCC62`, `0x003DCA5D`).
- The global lookup takes the count at `+0x00` and the records from `+0x10` without checking either against the
  buffer (`0x003DCA5F`-`0x003DCA88`). The first record whose [bound id](../Scripts-And-Script-Commands/script-name-bindings.md#the-bound-id-what-a-script-names) and motion match gives the file
  (`0x003DCA8C`), whatever its weapon class, so an entry there wins over every area's slot 7 and the second root's
  table for that model and motion.

## Related

- [Authored data tables](authored-data-tables.md): the registry slots, the table header and the binders.
- [Battle unit construction](../Characters-And-Objects/battle-unit-construction.md): how an enemy definition becomes a unit.
- [Stats](../Damage-And-Battle-Formulas/stats.md): the base and growth rows.
- [Enemy AI](../Enemy-AI-And-Gambits/enemy-ai.md): the order sets of slot 1.
- [Script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md): the bindings, keep bits and lane holds the trailer sets.
