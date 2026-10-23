---
title: "Position entries (FF12POS3): a zone's authored points, boxes and ellipses, the accessor that copies them and the systems that read them"
kind: "format"
category: "EBP script files"
addresses: "0x003320E0, 0x003DFE60, 0x02B59D48, 0x003DFD00, 0x00320940, 0x003209C0, 0x00236450, 0x00319390, 0x00312DF0, 0x00312730, 0x00301AD0, 0x003394A0, 0x0033DB60, 0x00354FB0, 0x003DFAC0, 0x00264CA0, 0x003DFA50"
---

## What the player sees

Where monsters appear and roam in a zone. A monster spawns at an authored point or at a random spot
inside an authored box or ellipse, wanders around a numbered point, and an enemy's gambits can test
its distance from one. Scripts read the same points to place actors. None of it is drawn; the entries
are why monsters gather in particular parts of a field.

## Where it comes from

Slot 16 of the [EBP script container](ebp-script-container.md) directory, in zone scripts only. The
walker `0x003304A0` calls `0x003320E0` (`0x00330615`), which clears the pointer's low four bits and tail
calls `0x003DFE60(0, section)`: the section is stored as field root 0 at `0x02B59D48` (`0x003DFE6A`). Slot 17
would go to root 1 (`0x00332110`) in the same way; no shipped container has a slot 17. `0x003DFA50`
releases the roots.

## Layouts

All multi-byte fields are little-endian.

```
+0x00  char[8]  magic   "FF12POS3"; only byte 7 is read, as a version
+0x08  u32      size    0x10 + 0x30 × count
+0x0C  u32      count   records
+0x10  record[count]
+size  u32      0x0000000A
```

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | type | read as a byte: 0 point, 1 box, 2 ellipse |
| `+0x04` | `f32` | extentX | box width or ellipse diameter along the record's local x |
| `+0x08` | `f32` | extentZ | box depth or ellipse diameter along the record's local z |
| `+0x0C` | `f32` | 1.0 in all but 18 entries (census below) |  |
| `+0x10` | `f32` | x |  |
| `+0x14` | `f32` | y |  |
| `+0x18` | `f32` | z |  |
| `+0x1C` | `f32` | heading | radians, rotates the region |
| `+0x20` | `f32[4]` | 0 |  |

## Shipped data

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
| section slack after `size` | 96 to 176 bytes; zero except in the nine copies of `slm_a01.ebp` |

## Loader behaviour

### Binding

The bind stores the pointer and nothing else: no field is checked, copied or rewritten, and the
records are read from the loaded file whenever they are needed.

### The accessor

`0x003DFD00(class, index, out)` zeroes a 0x30-byte output (`0x003DFD10` to `0x003DFD23`) and returns 0 when
the root is null. Then:

- when byte 7 of the magic is `'3'` or above (`0x003DFD2C`), it returns 0 for an index at or past
  `count` (`0x003DFD33`) and otherwise copies record `index` whole (`0x003DFD48` to `0x003DFD63`);
- below `'3'` it reads 16-byte records at `+0x10 + index × 0x10` into output `+0x10` to `+0x1C` with
  the type byte 0 (`0x003DFD69` to `0x003DFD9A`).

Nothing reads `size`, the first seven magic bytes or the trailing zero dwords.

### Readers

| Reader | What it takes |
|---|---|
| `0x00320940(index, out)` | x, y and z of class-0 record `index`; -1 when absent |
| `0x003209C0(index, out)` | the whole record; spawn candidates (`0x00234AF0`) and region placement |
| `0x00236450` | spawn placement: type 0 the point; type 1 a random offset within half of each extent; type 2 a random x, then z bounded by the ellipse; `0x00319390` rotates the offset by the heading and adds it to x and z |
| `0x00312DF0` via `0x00312730` | orders `0x4000` to `0x401F` wander within a radius of entry `order - 0x3FFF` |
| `0x00301AD0` (`0x00302C93`) | the AI distance condition, entry operand + 1 |
| `0x002350C0` | range retirement mode 2: entry `+0x51` of the spawn record |
| `0x003394A0` (`0x003394DB`) | the class steering solver tests the distance from entry 8 |
| `0x0033DB60` (`0x0033DB90`) | steers relative to a point 11.0 units from entry 32 |
| `setentrypos` (`0x00354FB0`) | pushes the entry's x, y, z and heading and runs `0x00350510` |
| `btlAtelGetPositionDataX`, `Y`, `Z` (`0x0050F960`, `0x0050F9B0`, `0x0050FA00`) | one coordinate to a script |
| `debug_positioninfo` (`0x0050EBA0`) | the accessor with a class from its argument |

### The older-layout reader

`getcrystalid` (`0x00352C80`) and `getanchorid` (`0x003532D0`) call `0x00264CA0`, which for a kind of 6 or
9 calls `0x003DFAC0(kind, index)`. That routine reads root 0 as an earlier layout:

- it needs byte 7 at least `'2'` (`0x003DFAE1`) and decodes `+0x08` as an offset (`0x0020E600`, base 0)
  to a table: `u32 n` at `+0`, then for each kind a `s32` offset at `+8 + kind × 16` and a `s32`
  count at `+0x10 + kind × 16`;
- for `kind < n` and `index < count` it returns `root + offset + 32 × index`, else 0.

On an `FF12POS3` table `+0x08` is `size`, so `n` is the trailing `0x0000000A` and the count is read
past the records. In the 517 `us` tables that count lies inside the section, and is 0, for kind 6 in
289 tables and kind 9 in 1; otherwise it lies in section 19 or past the end of the file.

## Modding notes

- Keep `size = 0x10 + 0x30 × count` and the `0x0000000A` after the records, and leave byte 7 of the
  magic `'3'`: a lower digit switches the accessor to 16-byte records.
- Fixed indices carry meaning: wander orders and AI conditions use entry `n + 1`, the class steering
  solver entry 8 and the routine at `0x0033DB60` entry 32. Append new entries rather than reorder.
- An index at or past `count` yields an all-zero record (the accessor) or -1 (`0x00320940`), not a
  crash.
- The extents of a box are full sizes; placement uses half of each on either side of the point, in
  the frame the heading rotates. Type 0 ignores both.
- `getcrystalid` and `getanchorid` with kind 6 or 9 do not read `FF12POS3` records; use other kinds.

## Related

- [EBP script container](ebp-script-container.md): the directory and the walker.
- [Enemy spawning](../Enemy-Spawning/enemy-spawning.md): candidate positions, region placement and range retirement.
- [Battle locomotion](../Movement-And-Pathfinding/battle-locomotion.md): the order goal decoder and the class steering solver.
- [Gambit conditions](../Enemy-AI-And-Gambits/gambit-conditions.md): the condition evaluator.
- [Random number generators](../Random-Numbers/random-number-generators.md): the generator behind region placement and wandering.
