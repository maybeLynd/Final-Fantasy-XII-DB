---
title: "Area battle data (.ard and .nmb): the per-area file of enemy definitions, class rows, stat rows, gambit order sets, motion overrides and preloaded models, and its companion"
kind: "format"
category: "Game files and data tables"
addresses: "003EA6E0, 00264ED0, 003EA820, 003EA710, 0023A160, 003845F0, 003846F0, 02B5E0B8, 02B5E0C0, 003DCF00, 02B58178, 003DCA30, 02B58188, 02B58180, 003DCBC0, 003EA650, 0035A3A0, 0035AC60, 002628B0, 0025AFC0, 0037C910, 0037C3F0, 003DC8D0, 02B580B0, 0032FC30, 02EBF150, 02EBF168, 02EBF120, 02EBF148, 02EBF140, 003EA6B0"
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

The area number comes from the map-reference row: `00264ED0` returns the `u16` at `+4` of row `n` of
the table at `[02099D88]`.

## Layouts

```python
FF12AR03 header (0x30 bytes, offsets from the start of the file)
+0x00  char[8]  'FF12AR03'       never read
+0x08  u32      0
+0x0C  u32      trailer offset   0 = no trailer
+0x10  u32[8]   section directory, slot k at +0x10 + 4k, 0 = absent
               slot 0 st2e, 84-byte class rows          -> 02EBF150
               slot 1 order-set directory               -> 02EBF168
               slot 2 st2e, 88-byte enemy definitions   -> 02EBF120
               slot 3, slot 4 never read
               slot 5 st2e, 56-byte base stat rows      -> 02EBF148
               slot 6 st2e, 56-byte growth stat rows    -> 02EBF140
               slot 7 motion-file overrides             -> 02B58178

slot 1         +0x00 u16 count, +0x04 count + 1 u32 offsets from the section (the last is the end)
slot 7         +0x00 u32 count, +0x04 12 bytes, then count records of 0x10:
               +0x00 u32 bound model id, +0x04 u16 weapon class, +0x06 u16 motion, +0x08 u16 file index
trailer        +0x00 u32 count, then count records {u32 bound model id, u32 lane mask}

.nmb           +0x00 u16 count, +0x02 u16 100, +0x04 u32 offsets[count + 1] from the file start
               (the last is the file size), then the entries
```

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
| trailers | 140 files, 998 records; the other 26 have offset 0 |
| trailer model letters | `w` 564, `m` 278, `n` 140, `s` 13, `c` 3 |
| section 19 (`us` scripts) | 271 carry an `FF12AR03` block, `+0x2C` = `0x30` in all, 2,116 slot-7 records in all; 266 with a trailer |
| `.nmb` files | 166 per tree, byte-identical, version 100, `8 + 7 × count` bytes |
| `.nmb` counts | 0 to 22; equal to the `.ard`'s slot 2 row count in all 166 |
| `.nmb` entries | 1,146: `12 BA 00` 1,120 and `12 BB 00` 26, each a one-glyph two-byte string |

## Loader behaviour

### When an area loads

`0032FC30(slot, n)`, for area slot 0, calls `003EA6E0(n, force)`, which reads the area number with
`00264ED0` and returns at once when it equals the loaded one (`02B5E0B8`) and `force` is 0. The force
byte is never set, so re-entering the same area keeps the file.

Otherwise `003EA820(area)`:

1. pre-reads the first `0x800` bytes of kind `0x15` file `area × 2 + 1`, the path
   `<area>\area\<area>.fpk`, through `0032EB40` (which reads only a file larger than `0x800`; no such
   file ships);
2. sizes the `.ard` with `0032E400(0x15, area × 2)`;
3. if a file is loaded, frees it, sets `02B5E0B8` to −1, clears the motion overrides
   (`003DCF00(0)`) and unbinds the five tables (`0023A160(category, 0)`);
4. with a size of 1 or more, unbinds them again, allocates the size, tags the block
   `..\..\katano\atelareaload.c` and files the read with completion `003EA710`, recording the area in
   `02B5E0B8`.

A file that is missing or empty leaves every table null.

At start-up `0032F430` runs `003EA6B0` (`0032F697`): the loaded area `02B5E0B8` becomes -1, the two
roots `02B5E0C0` and `02B5E0C8` 0, and both motion-override tables are cleared (`003DCF00(0)`,
`003DCF10(0)`).

### Binding the sections

`003EA710(file)` binds each section as the file's base plus its directory offset, with no bounds
check and no magic check:

| Directory slot | Category | Binder | Null when the offset is 0 |
|---|---|---|---|
| 0 | 0 → `02EBF150` | `003845F0` | no |
| 1 | 1 → `02EBF168` | `003846F0`, depth 0 | no |
| 2 | 2 → `02EBF120` | `003845F0` | no |
| 7 | `003DCF00` → `02B58178` | stored as is | yes |
| 5 | 3 → `02EBF148` | `003845F0` | yes |
| 6 | 4 → `02EBF140` | `003845F0` | yes |

It then makes the file root 0 (`02B5E0C0`). The binders add the section's address to the offsets
inside it, so the loaded block is no longer a copy of the file.

### The second area root (EBP section 19)

A script container (`.ebp`) can carry a second `FF12AR03` block in directory slot 19
([script container](../EBP-Script-Files/ebp-script-container.md)). When the container arrives,
`003304A0` passes it to `003320D0` (`00330666`), which drops the area slot and jumps to `003EAA00`:

1. a block already held is unbound (`003DCF10(0)`) and released (`00331880`);
2. the new block becomes root 1 (`02B5E0C8`);
3. its directory slot 7 (`+0x2C`) becomes the third motion-override table `02B58180` (`003DCF10`), or 0
   when `+0x2C` is 0.

Only `+0x2C` and the trailer offset `+0x0C` of this block are read; its `st2e` slots are never bound.

### Motion-file overrides

`003DCA30(model, motion, class, &kind, &file)` picks the file of an action motion, always of kind
`0x1E`. It looks for the model and motion in three tables, in order:

1. the global table `02B58188` (model and motion only), loaded at start-up by `003DCBC0` from kind 9,
   file 5 (tagged `PCSkill`);
2. the area's slot 7 (`02B58178`), matching model, motion and weapon class;
3. the table `02B58180` installed with the second area root (`003DCF10`).

The first match gives the file index; none gives −1.

### Preloading the trailer's models

`003EA650(n)` returns root `n`'s trailer (`n` 0 or 1, the `.ard` and the second area root). The task
`0037C3F0`, which `0037C910` installs (called from `00261F90`, `003473A0` and `00359800`), walks three
lists in turn: root 0's trailer, root 1's, and, when it was started with argument 1, an `{id, mask}`
table at `+0x80` of area slot 0's loaded data. For each record it:

1. finds or creates the model's name binding (`002EAE20`) and marks it (`002EBD40`);
2. waits until the model is loaded (`002E4C20`);
3. requests each lane whose bit is set in the mask (`002EB5D0`, `002ECA30`) and waits until it is
   loaded (`002E4C30`).

When the lists end it calls `003601C0(10)` and removes itself.

### Models kept through an area change

When an area slot is unloaded (slots 1–3 in `002628B0`, slot 0 in `0025AFC0`, which `0032F850` and
`0032FB70` call), the game:

1. runs `0035A3A0`, which, for each trailer record of both roots whose model is already loaded
   (`002E4C20`), sets the binding's keep bit (`+0x19` bit 0) and the hold bits of lane 0 and of
   every lane in the mask (`002ECAB0(id, lane, 1)`);
2. releases the area's models (`002E4000`, `002E3E20`), which the keep bit and hold bits survive;
3. runs `0035AC60`, which clears the keep bits and hold bits again.

So a model the trailer names stays loaded across the change instead of being unloaded and read
again.

### The .nmb request

Of the 51 read requests in the executable, the one that passes kind `0x1A` as a constant is in
`00324510`, which would build a buffer from 301 files (`0032E620(0x1A, i, …)` for `i` below `0x12D`)
but never starts: nothing stores the state that begins the build
([authored data tables](authored-data-tables.md)).

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
- Give a model, motion and weapon class the same motion file size in every area: `003DC8D0` keeps the
  sizes of up to sixteen recent motion lookups at `02B580B0`, keyed by those three and never cleared
  after start-up, and a later request reuses the cached size.

## Related

- [Authored data tables](authored-data-tables.md): the registry slots, the table header and the binders.
- [Battle unit construction](../Characters-And-Objects/battle-unit-construction.md): how an enemy definition becomes a unit.
- [Stats](../Damage-And-Battle-Formulas/stats.md): the base and growth rows.
- [Enemy AI](../Enemy-AI-And-Gambits/enemy-ai.md): the order sets of slot 1.
- [Script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md): the bindings, keep bits and lane holds the trailer sets.
