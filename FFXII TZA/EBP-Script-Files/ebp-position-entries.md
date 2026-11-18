[Home](../../README.md) / [EBP script files](README.md) / Position entries (FF12POS3)

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Position entries (FF12POS3): a zone's authored points, boxes and ellipses, the accessor that copies them and the systems that read them | format | EBP script files | Script sections | Section 16 of a zone .ebp, magic FF12POS3 and named POSENT by the engine: a 16-byte header and 0x30-byte records holding a type (point, box or ellipse), two extents, a position and a heading. The section is bound whole into field root 0 (0x02B59D48) and read through one accessor, 0x003DFD00, by spawn placement, the enemy wander orders, the AI distance condition, two fixed-entry steering routines and the position verbs; also the older-layout reader behind getcrystalid and getanchorid, the 4,653 shipped tables and the editing rules. | 0x003320E0, 0x003DFE60, 0x02B59D48, 0x003DFD00, 0x00320940, 0x003209C0, 0x00236450, 0x00319390, 0x00312DF0, 0x00312730, 0x00301AD0, 0x003394A0, 0x0033DB60, 0x00354FB0, 0x003DFAC0, 0x00264CA0, 0x003DFA50 |

## What the player sees

Where monsters appear and roam in a zone. A monster spawns at an authored point or at a random spot
inside an authored box or ellipse, wanders around a numbered point, and an enemy's gambits can test
its distance from one. Scripts read the same points to place actors. None of it is drawn; the entries
are why monsters gather in particular parts of a field.

## Where it comes from

Slot 16 of the [EBP script container](ebp-script-container.md) directory, in zone scripts only. The
walker `0x003304A0` calls `0x003320E0`¹, which clears the pointer's low four bits and tail
calls `0x003DFE60(0, section)`: the section is stored as field root 0 at `0x02B59D48`². Slot 17
would go to root 1³ in the same way; no shipped container has a slot 17. `0x003DFA50`
releases the roots.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00330615` |
| ² | `0x003DFE6A` |
| ³ | `0x00332110` |

</details>

`0x003DFA50` passes each non-null root, `0x02B59D48` and `0x02B59D50`, to `0x00331880` and nulls it¹, then does the same for the navigation-icon block `0x02B59D58`². The boot clear `0x003DFDA0` zeroes both roots with one 16-byte
store³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003DFA70`-`0x003DFA7D` |
| ² | `0x003DFA8A`-`0x003DFA9B` |
| ³ | `0x003DFDAE` |

</details>

## Layouts

All multi-byte fields are little-endian.

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `char[8]` | magic | "FF12POS3"; only byte 7 is read, as a version |
| `+0x08` | `u32` | size | `0x10` + `0x30` × count |
| `+0x0C` | `u32` | count | records |

```
+0x10  record[count]
+size  u32      0x0000000A
```

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | type | read as a byte: 0 point, 1 box, 2 ellipse |
| `+0x04` | `f32` | extentX | box width or ellipse diameter along the record's local x |
| `+0x08` | `f32` | extentZ | box depth or ellipse diameter along the record's local z |
| `+0x0C` | `f32` |  | 1.0 in all but 18 entries (counts below) |
| `+0x10` | `f32` | x |  |
| `+0x14` | `f32` | y |  |
| `+0x18` | `f32` | z |  |
| `+0x1C` | `f32` | heading | radians, rotates the region |
| `+0x20` | `f32[4]` |  | value 0 |

## Shipped data

<details>
<summary>Show the shipped data</summary>

Measured over all 10,036 EBP2 containers in the nine language trees.

| Fact | Value |
|---|---|
| containers with section 16 | 4,653: 517 per language, all zone scripts |
| languages | the 517 tables are byte-identical in all nine trees |
| magic | `FF12POS3` in all |
| `size` | `0x10 + 0x30 × count` in all, followed by the dword `0x0000000A` in all |
| `count` | 3 to 191, median 42; 231,183 records (25,687 per language) |
| tables reaching entry 8 / entry 32 (`us`) | 516 / 484 of 517 |
| `type` | 0 (187,803), 1 (43,209), 2 (171); upper three bytes 0 in all |
| `+0x0C` | 1.0 in 231,165; -1.0 in 9; 0.0 in 9 |
| `+0x20` to `+0x2C` | zero in every record |
| box extents, smaller side | 6.0 (11,394), 12.0 (11,367), 4.0 (4,770), 8.0 (4,374), 10.0 (3,168), 7.0 (1,440) |
| heading | non-zero in 18,621 records, 18,153 of them a whole number of degrees; -2.861 to 5.760 rad |
| section slack after `size` | 96 to 176 bytes; zero except in the nine copies of `slm_a01.ebp`, whose 176 bytes hold the dwords `0x730` and 1 at `size + 0x34` and `size + 0x38` (`0x730` is the section offset of `size + 0x60`) and the four floats 135.0104522705078, -0.20425499975681305, 138.69577026367188 and 0.5508739948272705 at `size + 0x60` |

[`ebp-position-entries-records.tsv`](ebp-position-entries-records.tsv) lists every record of the 517 tables, 25,687
rows, read from the `us` tree; every figure above reproduces from the same read over all nine trees.

| Column | Holds |
|---|---|
| `script` | the zone script, its path under the language folder of `ps2data/plan_master` |
| `languages` | the language trees whose section 16 is byte-identical to the `us` one (all nine in every row) |
| `record`, `record_offset` | the entry number from 0 and its offset from the section start, `0x10 + 0x30 × record` |
| `type`, `type_name` | the byte at `+0x00` and its meaning: 0 point, 1 box, 2 ellipse |
| `extent_x`, `extent_z` | the floats at `+0x04` and `+0x08` |
| `w0C` | the float at `+0x0C` |
| `x`, `y`, `z` | the position, `+0x10` to `+0x18` |
| `heading` | `+0x1C`, in radians |

</details>

## Loader behaviour

### Binding

The bind stores the pointer and nothing else: no field is checked, copied or rewritten, and the
records are read from the loaded file whenever they are needed.

### The accessor

`0x003DFD00(class, index, out)` zeroes a 0x30-byte output (`0x003DFD10` to `0x003DFD23`) and returns 0 when
the root is null. Then:

- when byte 7 of the magic is `'3'` or above¹, it returns 0 for an index at or past
  `count`² and otherwise copies record `index` whole (`0x003DFD48` to `0x003DFD63`);
- below `'3'` it reads 16-byte records at `+0x10 + index × 0x10` into output `+0x10` to `+0x1C` with
  the type byte 0 (`0x003DFD69` to `0x003DFD9A`).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003DFD2C` |
| ² | `0x003DFD33` |

</details>

Both branches test the index against `count` `+0x0C` with a signed compare¹,
so a negative index is not refused, and both return 1 after the copy². The class
indexes `0x02B59D48` without a bound check³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003DFD33`, `0x003DFD69` |
| ² | `0x003DFD40`, `0x003DFD9A` |
| ³ | `0x003DFD0A` |

</details>

Nothing reads `size`, the first seven magic bytes or the trailing zero dwords.

### Readers

| Reader | What it takes |
|---|---|
| `0x00320940(index, out)` | x, y and z of class-0 record `index`, from the record's `+0x10` (`0x00320980`-`0x0032099D`), returning 0; -1 when absent, that is when `0x003DFD00(0, index, rec)` returns 0 (`0x00320961`-`0x0032096A`) |
| `0x003209C0(index, out)` | the whole record; spawn candidates (`0x00234AF0`) and region placement |
| `0x00236450` | spawn placement: type 0 the point; type 1 a random offset within half of each extent; type 2 a random x, then z bounded by the ellipse; `0x00319390` rotates the offset by the heading and adds it to x and z, leaving y 0 for types 1 and 2 because `out` is zeroed first and `0x00319390` writes only x and z (`0x00236475`-`0x00236479`, `0x00236634`); a failed record fetch, or a type byte other than 0, 1 and 2, returns 0 (`0x00236486`, `0x002364DB`) |
| `0x00312DF0` via `0x00312730` | orders `0x4000` to `0x401F` wander within a radius of entry `order - 0x3FFF` |
| `0x00301AD0` (`0x00302C93`) | the AI distance condition, entry operand + 1 |
| `0x002350C0` | range retirement mode 2: entry `+0x51` of the spawn record |
| `0x003394A0` (`0x003394DB`) | the class steering solver tests the distance from entry 8 |
| `0x0033DB60` (`0x0033DB90`) | steers relative to a point 11.0 units from entry 32 |
| `setentrypos` (`0x00354FB0`) | pushes the entry's x, y, z and heading and runs `0x00350510` |
| `btlAtelGetPositionDataX`, `Y`, `Z` (`0x0050F960`, `0x0050F9B0`, `0x0050FA00`) | one coordinate to a script |
| `debug_positioninfo` (`0x0050EBA0`) | the accessor with a class from its argument |

`0x00312DF0(point, index, radius, ctx, out)` takes the point from entry `index` through `0x00320940` when
`point` is null, and returns -1 when that fails¹. It copies the point's y to
`out + 4`, then tries up to nine spots. Each sets x = `point.x + (rand % (2r + 1)) - r` and
z = `point.z + (rand % (2r + 1)) - r`, with `rand` from `0x00328370`. It returns 0 at the first spot that
`0x00317DE0(ctx, out, r != 0)` accepts², and -2 after the ninth³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00312EA3`-`0x00312EB7` |
| ² | `0x00312E40`-`0x00312E9F` |
| ³ | `0x00312EBC` |

</details>

### The older-layout reader

`getcrystalid`¹ and `getanchorid`² call `0x00264CA0`, which for a kind of 6 or
9 calls `0x003DFAC0(kind, index)`. That routine reads root 0 as an earlier layout:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00352C80` |
| ² | `0x003532D0` |

</details>

- it needs byte 7 at least `'2'`¹ and decodes `+0x08` as an offset (`0x0020E600`, base 0)
  to a table: `u32 n` at `+0`, then for each kind a `s32` offset at `+8 + kind × 16` and a `s32`
  count at `+0x10 + kind × 16`;
- for `kind < n` and `index < count` it returns `root + offset + 32 × index`, else 0.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003DFAE1` |

</details>

On an `FF12POS3` table `+0x08` is `size`, so `n` is the trailing `0x0000000A` and the count is read
past the records. In the 517 `us` tables that count lies inside the section, and is 0, for kind 6 in
289 tables and kind 9 in 1; otherwise it lies in section 19 or past the end of the file.

## Modding notes

- Keep `size = 0x10 + 0x30 × count` and the `0x0000000A` after the records, and leave byte 7 of the
  magic `'3'`: a lower digit switches the accessor to 16-byte records.
- Fixed indices carry meaning: wander orders and AI conditions use entry `n + 1`, the class steering
  solver entry 8 and the routine at `0x0033DB60` entry 32. Append new entries rather than reorder.
- An index at or past `count` yields an all-zero record (the accessor) or -1¹, not a
  crash.
- The extents of a box are full sizes; placement uses half of each on either side of the point, in
  the frame the heading rotates. Type 0 ignores both.
- `getcrystalid` and `getanchorid` with kind 6 or 9 do not read `FF12POS3` records; use other kinds.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00320940` |

</details>

## Related

- [EBP script container](ebp-script-container.md): the directory and the walker.
- [Enemy spawning](../Enemy-Spawning/enemy-spawning.md): candidate positions, region placement and range retirement.
- [Battle locomotion](../Movement-And-Pathfinding/battle-locomotion.md): the order goal decoder and the class steering solver.
- [Gambit conditions](../Enemy-AI-And-Gambits/gambit-conditions.md): the condition evaluator.
- [Random number generators](../Random-Numbers/random-number-generators.md): the generator behind region placement and wandering.

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 1 call with 1 other topic</summary>

**World, areas and travel** (explained on [force fight mode](../Engine-Core/force-fight-mode.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x003DFDA0`](ebp-position-entries.md) | is called by | [`0x00266D10`](../Engine-Core/frame-update-order.md) (on frame update order) |

</details>
