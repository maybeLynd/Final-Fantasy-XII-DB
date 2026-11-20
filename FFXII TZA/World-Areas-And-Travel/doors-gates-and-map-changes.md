[Home](../../README.md) / [World, areas and travel](README.md) / Doors, gates and map changes

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Doors, gates and map changes: the override table the setmapid verbs write, what its floor, wall and mj bits block, the show and hide model masks and when a new map clears them | system | World, areas and travel | Changing areas and travel | How a zone script opens a gate or raises a barrier: the 80-entry override table at 0x0209A3E0 that setmapidfloor, setmapidwall and setmapidmj lay over every collision polygon's attribute word, which movement kinds each bit blocks, the ground field, the path reset every write triggers, the route-graph edges that consult the same table, the two 64-bit masks behind showmapmodel and hidemapmodel, and the map bind that clears all of it. | 0x0209A3E0, 0x0026E880, 0x003792E0, 0x003795A0, 0x00379430, 0x00232020, 0x00230A40, 0x0022F8B0, 0x0026E300, 0x00379010, 0x0026E5F0, 0x0026E960, 0x003278D0 |

## What the player sees

A gate swings open and the corridor behind it can be walked. A locked door, a wall of light or a fallen
pillar bars the way until a switch is pulled or the story moves on. A bridge appears, a ladder is lowered,
rubble vanishes. Blocked ground stops the party at an invisible line, and the monsters and townspeople
that walk the same map stop at the same line.

None of this travels with a save. When an area loads, every gate starts in the state the map was built
with, and whatever the area's script changes during its start-up is what the player finds. A change made
in the middle of a visit lasts until the next area load.

## How it works

### Every collision polygon carries a 32-bit attribute word

The collision part of the loaded map is a 0x68-byte descriptor at `map + 0x40`. `0x0026E500(0)` returns it
from `[0x0209A678]` once `0x0026E960` has bound a map. Its polygons are 0x20-byte records at `[part + 0x10]`
and its wall records are 0x90-byte records at `[part + 0x18]`. A polygon id below 0x4000 names a polygon
and an id from 0x4000 names a wall record¹. The attribute word sits at `+0xC` of
a polygon and at `+4` of a wall record. Its fields, with the functions that read each one:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0022F8B0`, `0x0022DE60` |

</details>

| mask | field | written by a verb | read by |
|---|---|---|---|
| `0x7` | polygon type: 0 floor, 1 wall, 2 and 4 marker polygons, 3 camera region | no verb | `0x00230A40`, `0x0022D4B0`, `0x0022CC50`, `0x00231A90`, `0x002321D0`, `0x00233230` |
| `0x78` | mj group 0-15; selects override entry `0x40 + group` | no verb | `0x00232020`, `0x00230A40`, `0x00232090`, `0x00231F80`, `0x002321D0`, `0x00231A90` |
| `0x1000` | copied into bit `0x4` of the body's flag word | `setmapidfloor` kind 9 | `0x003808A0` |
| `0x3E000` | floor group 0-31; the wall group on type-1 polygons and wall records | no verb | every override reader below |
| `0x7C0000` | ground field | `setmapidfloorground` | `0x00231F80` |
| `0xF800000` | block bits for movement kinds 0, 5, 1, 2, 3 (bits `0x800000`, `0x1000000`, `0x2000000`, `0x4000000`, `0x8000000`) | `setmapidfloor`, `setmapidmj` | `0x00230A40`, `0x00232090`, `0x0022D4B0` |
| `0x4000000` | on type-1 polygons and wall records: skipped by the sphere sweep | no verb | `0x0022D7E0` |
| `0x40000000` | wall ignored by kind-4 queries | `setmapidwall` kind 6 | `0x0022D4B0`, `0x0022CC50` |
| `0x80000000` | wall switched off | `setmapidwall` kind 5 | `0x0022F8B0`, `0x0022DE60`, `0x0022D7E0`, `0x0022D4B0`, `0x0022CC50` |

`0x00230A40` closes a polygon to every movement kind when there is no neighbour across the edge¹ or the
polygon type (bits `0x7`, after the overrides) is not 0². Otherwise kinds 0, 1, 2, 3 and 5 test their
block bit; kind 4, kinds 6 and above and negative kinds (the kind is read as a signed 16-bit value, `0x00230AC2`) have
no block bit and pass every floor polygon (`xor r11d, 1`, `0x00230B4A`).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00230A4F` |
| ² | `0x00230AB9` |

</details>

In bytes it returns `(f & 0x7) == 0 && (f & B) == 0`, with `f` the polygon's flags after the overrides¹ and `B` the kind's block bit: `0x800000` for kind 0 (`bt ecx, 0x17`), `0x2000000`,
`0x4000000` and `0x8000000` for kinds 1 to 3, `0x1000000` for kind 5², and 0 for the
others; a negative neighbour index returns 0³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00230A88`-`0x00230AB7` |
| ² | `0x00230AC9`-`0x00230B3D` |
| ³ | `0x00230A4F` |

</details>

### The override table

`0x0209A3E0` holds 80 entries of two 32-bit words, `mask` then `value`, 8 bytes each, from `0x0209A3E0` to
`0x0209A65F`. A set mask bit means that bit of the attribute word is replaced by the value bit. A clear
mask bit lets the authored bit through. The three banks follow from the writers' offsets (`0x003795A0`
adds `0x20` to the entry, `0x00379430` adds `0x40`) and from the three zeroing loops of `0x0026E960`¹:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0209A3E0`-`0x0209A4DF`, `0x0209A4E0`-`0x0209A5DF`, `0x0209A5E0`-`0x0209A65F` |

</details>

| entries | addresses | bank | selected by |
|---|---|---|---|
| 0x00-0x1F | 0x0209A3E0-0x0209A4DF | floors | attribute bits under mask `0x3E000` of a floor polygon |
| 0x20-0x3F | 0x0209A4E0-0x0209A5DF | walls | attribute bits under mask `0x3E000` of a wall polygon or wall record, plus 0x20 |
| 0x40-0x4F | 0x0209A5E0-0x0209A65F | mj groups | attribute bits under mask `0x78`, plus 0x40 |

### How a reader applies the overrides

`0x00232020(attr)` is the stand-alone form. `0x00230A40`, `0x00232090`, `0x00231F80`, `0x002321D0` and
`0x00231A90` inline the same arithmetic, and the five wall readers apply only the wall entry:

```c
// floors and mj groups: 0x00232020, 0x00230A40, 0x00232090, 0x00231F80, 0x002321D0, 0x00231A90
g   = (attr >> 13) & 0x1F;                              // floor entry
mj  = ((attr >> 3) & 0xF) + 0x40;                       // mj entry
eff = (attr & ~mask[g])  | (value[g]  & mask[g]);
eff = (eff  & ~mask[mj]) | (value[mj] & mask[mj]);      // applied second: the mj entry wins

// walls: 0x0022F8B0, 0x0022DE60, 0x0022D7E0, 0x0022D4B0, 0x0022CC50
w   = ((attr >> 13) & 0x1F) + 0x20;
eff = (attr & ~mask[w]) | (value[w] & mask[w]);
```

Because the mj entry is applied after the floor entry, an mj override of a bit beats a floor override of
the same bit on every polygon tagged with that mj group.

An mj override closes a walking exit only through walking. The exit test `0x0025B600` ([script
requests](../Scripts-And-Script-Commands/script-requests.md)) takes the mj group from the word `+0x88` of the focus
actor's movement body¹ and the group's owner actor from the table `0x0209A210`²; it reads no entry of the override table.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0025B688`-`0x0025B698` |
| ² | `0x0025B6AD`-`0x0025B6B4` |

</details>

A movement kind whose bit the mj entry sets cannot enter the group's polygons¹, so the body's `+0x88` does
not take the group. `0x003808A0` records the group of the polygon the body stands on after every move or placement ([the
ground field](#the-ground-field-and-bit-0x1000)), so a body that already stands on one of the group's polygons when
the entry is set keeps the group, and `0x0025B600` can still file the exit's request.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00230A40` |

</details>

The focus actor does not always move as kind 0. When it is not riding (kind 5), it moves as kind 1 while `0x002672B0()`
is 0, and while its `+0x0C` bit `0x10` is set and `0x00265680()` is non-zero ([player
movement](../Movement-And-Pathfinding/player-movement.md#the-animation-mode-word)); `0x0025B600` itself runs only
while `0x00265680()` is non-zero¹. So an mj entry has to close kind 1 as well as kinds 0 and 5 to keep the
exit shut in every state of the focus actor.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0025B66B` |

</details>

### The writers and the path reset

Apart from the map bind `0x0026E960`, which clears the table, four functions write it, and each calls `0x003278D0`:
`0x0026E880`, `0x0026E850` and `0x0026E130` end in a tail jump to it¹, and `0x0026E150`
calls it after every entry it clears², so `count` times; with a count of 0 or less `0x0026E150` returns at
once without a write or the call³:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0026E8B0`, `0x0026E873`, `0x0026E141` |
| ² | `0x0026E178` |
| ³ | `0x0026E150`-`0x0026E152`, `0x0026E196` |

</details>

| function | arguments | effect |
|---|---|---|
| `0x0026E880` | entry, v, bit, width | `mask \|= ((1 << width) - 1) << bit`, then those bits of `value` become `v << bit`; `v` is not cut to the width, so a set bit of `v << bit` above the field is also set in `value` (`0x0026E89D`, `0x0026E8A4`-`0x0026E8AC`); it ends with a tail jump to `0x003278D0` (`0x0026E8B0`) |
| `0x0026E850` | entry, bit, width | clears those mask bits, so the authored bits show through again |
| `0x0026E130` | entry | `mask := 0` for one entry |
| `0x0026E150` | first, count | `mask := 0` for `count` consecutive entries |

`0x003278D0` walks the body registry (`0x00236850` is the count, `0x00236820(i)` returns the 0xF50-byte body
`i` at `[0x0208E688]`). For every body whose first byte has bit `0x10` set it calls `0x003839C0` and `0x003839F0` on
the body's `+0x200` block: the two shorts at `+0xC` and `+0xE` become 0xFFFF and the 0x80 bytes from
`+0x10` become 0xFF. Nothing else is written, and no map model is touched by any of the four writers.
A null body is skipped¹, and the count is read again after every body²; with a count
of 0 or less nothing is walked³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003278F0` |
| ² | `0x00327910` |
| ³ | `0x003278DF` |

</details>

### The verbs

The script sources call these verbs `setmapidfloor`, `setmapidwall`, `setmapidmj` and so on. The names
and ids are those of the verb table page in Related. Handlers come from the family-0 verb table at
`0x01EED700`, 32 bytes per verb, where an instantaneous verb's handler is the first slot of the next
record: record `0xFF` at `0x01EEF6E0` holds `0x00343E60`, the handler of verb `0xFE`.

Operands are popped with `0x00267E10(ctx)`, which returns an integer operand as it is and truncates a
float operand, and pushed with `0x00267F90(ctx, n)`. The three-operand verbs push -1 and then pop four
times, dropping the first pop, so the pushed -1 is thrown away and the script's operands reach the
native as (group, kind, v): `0x00343E60` runs `or edx, -1; call 0x00267F90`, four `call 0x00267E10` and
`jmp 0x003792E0` with the last pop in `ecx`.

| id | name | handler | native call | script operands |
|---|---|---|---|---|
| 0xF6 | resetmapidfloorall | `0x003416E0` | `0x003791D0(-1)` | no operand; -1 is pushed and popped |
| 0xF7 | resetmapidfloor | `0x00341290` | `0x003791D0(g)` | g |
| 0xF8 | resetmapidwallall | `0x00341E30` | `0x00379270(-1)` | no operand |
| 0xF9 | resetmapidwall | `0x00341A90` | `0x00379270(g)` | g |
| 0xFA | resetmapidmjall | `0x003424D0` | `0x00379220(-1)` | no operand |
| 0xFB | resetmapidmj | `0x003421B0` | `0x00379220(g)` | g |
| 0xFC | setmapidfloorground | `0x003429B0` | `0x003791F0(g, v)` | g, v |
| 0xFD | setmapidmjground | `0x00343140` | `0x00379240(g, v)` | g, v |
| 0xFE | setmapidfloor | `0x00343E60` | `0x003792E0(g, kind, v)` | g, kind, v |
| 0xFF | setmapidwall | `0x00344A20` | `0x003795A0(g, kind, v)` | g, kind, v |
| 0x100 | setmapidmj | `0x003458D0` | `0x00379430(g, kind, v)` | g, kind, v |
| 0x101 | setmapidfloor_101 | `0x00343810` | `0x003792E0(g, kind, v)` | g, kind, v, x; x is popped and dropped |
| 0x102 | setmapidwall_102 | `0x003444F0` | `0x003795A0(g, kind, v)` | g, kind, v, x |
| 0x103 | setmapidmj_103 | `0x00345370` | `0x00379430(g, kind, v)` | g, kind, v, x |
| 0x107 | resetmapidfloorground | `0x00342E00` | `0x003791F0(g, -1)` | g |
| 0x108 | resetmapidmjground | `0x003434B0` | `0x00379240(g, -1)` | g |
| 0x109 | resetmapidfloor_109 | `0x00344190` | `0x003792E0(g, kind, -1)` | g, kind; -1 is pushed twice |
| 0x10A | resetmapidwall_10a | `0x00344E30` | `0x003795A0(g, kind, -1)` | g, kind |
| 0x10B | resetmapidmj_10b | `0x00345EF0` | `0x00379430(g, kind, -1)` | g, kind |

The reset natives clear masks only. `0x003791D0(g)` calls `0x0026E130(g)`, or `0x0026E150(0, 0x20)` when `g`
is negative. `0x00379270(g)` calls `0x0026E130(g + 0x20)` or `0x0026E150(0x20, 0x20)`¹.
`0x00379220(g)` calls `0x0026E130(g + 0x40)` or `0x0026E150(0x40, 0x10)`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00379274` |
| ² | `0x00379224`-`0x00379229` |

</details>

Verbs `0x104` to `0x106` (`setmapambient`, `setmapambient_105`, `resetmapambient`; handlers
`0x00346380`, `0x00346880`, `0x00346D20`) sit between these ids but write the four floats at `0x0209A390`
through `0x00379080`; they change lighting, not the map, and are outside this page.

### Which bit each kind writes

`0x003792E0(g, kind, v)` and `0x00379430(g, kind, v)` share one kind-to-bit map; `0x003795A0` has its own.
The value bit is the inverse of `v` for floors and mj groups (`sete` at `0x003792ED`) and equal to `v`
for walls (`setnz r10b` at `0x003795AB`):

| native | kind to bit | value bit when v is 0 or more | v below 0 |
|---|---|---|---|
| `0x003792E0` (floors), `0x00379430` (mj, entry + 0x40) | 0 to 23, 1 to 25, 2 to 26, 3 to 27, 7 to 24, 9 to 12; any other kind writes nothing | `v == 0`, so a set bit blocks | `0x0026E850(entry, bit, 1)`: the bit's mask is cleared |
| `0x003795A0` (walls, entry + 0x20) | 5 to 31, 6 to 30; any other kind writes nothing | `v != 0`, so a set bit switches the wall off | `0x0026E850(entry, bit, 1)` |

Read with the consumers below, `v = 1` opens in both banks: it clears a floor's block bit and sets a
wall's off bit. `v = 0` closes, and a negative `v` hands the bit back to the authored data.

`0x003791F0(g, v)` writes the ground field: `0x0026E880(g, v, 18, 5)` when `v` is 0 or more and
`0x0026E850(g, 18, 5)` when it is negative. `0x00379240` does the same on entry `g + 0x40`.

### What the floor bits block

A body's movement kind is the word at `+0x50` of its navigation record (`0x00380D30` reads only its low byte), the record `0x003808A0`,
`0x002327D0` and `0x00380D30` work on. The readers of the block bits are:

- `0x00230A40(part, polygon, kind)` returns 0 for a negative polygon¹. It applies the overrides to the
  attribute word `+0xC` of polygon record `polygon` of `[part + 0x10]`².
- It then returns 0 when `eff & 7` is not 0 (not a
  type-0 floor polygon). Otherwise it returns 1 when the kind's bit is clear: kind 0 tests bit `0x800000`, kind
  1 bit `0x2000000`, kind 2 bit `0x4000000`, kind 3 bit `0x8000000`, kind 5 bit `0x1000000`. Kind 4, kinds above 5
  and negative kinds always get 1.
- `0x00232090(part, polygon)` packs the same five bits into a kind bitfield (bit k set means kind k is
  blocked: bit `0x1` from 23, bit `0x2` from 25, bit `0x4` from 26, bit `0x8` from 27, bit `0x20` from 24) and returns 0
  when `eff & 7` is not 0.
- `0x002327D0`, the movement sweep called from `0x00380C40`, asks `0x00230A40`³ about each
  neighbouring polygon the body is about to cross into. A 0 answer makes the sweep treat that edge as a
  wall⁴, so the body slides along the boundary of a blocked polygon exactly as
  along a wall.
- `0x00233110`, called by `0x00380D30`, `0x00231400` and `0x00232760` (from `0x003808A0`, `0x00380A22`), picks the polygon under a
  point from the cell's list and skips every polygon `0x00230A40` refuses⁵.
- `0x00380D30(record, position)` places a body: after finding its polygon it reads `0x00232090` into
  `+0x5E` and, when the body's own kind bit is set, writes 0xFFFE into the polygon slot `+0x52`. The position is then
  not copied: the body keeps its old position with no polygon⁶, and for the negative slot `0x003808A0` only
  sets `+0x54` to -1 and returns⁷.
- `0x00231A90` searches the body's cell for type-2 and type-4 marker polygons (stored at `+0x5C` and
  `+0x54`), using the overridden type bits.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00230A4F` |
| ² | `0x00230A55`-`0x00230A61` |
| ³ | `0x00232EB9` |
| ⁴ | `0x0022F9B0`, `0x0022FB2C` |
| ⁵ | `0x002331C0` |
| ⁶ | `0x00380D94` |
| ⁷ | `0x003808B7`, `0x00380A2C`-`0x00380A2F` |

</details>

The verb's kind numbers and the reader's kind numbers differ in one place: a script that writes
kind 7 sets bit `0x1000000`, and bit `0x1000000` is what the reader tests for movement kind 5.

### What the wall bits do

Walls are tested by the collision callback `0x0022F8B0` (installed through `0x0022F830` by `0x00232490` and
`0x00231400`), the sphere sweep `0x0022D7E0`, and the ray casts `0x0022DE60`, `0x0022D4B0` and `0x0022CC50`.
Each applies the wall entry to the attribute word and then decides as follows.

- A set bit `0x80000000` removes the wall. `0x0022F8B0` calls the contact test `0x00381EB0` only while `eff` is below
  `0x80000000` (and only when its record's `+0x24` is non-zero; with it zero every wall is tested).
  `0x0022DE60` and `0x0022D7E0` skip type-1 polygons and wall records whose bit `0x80000000` is set.
- `0x0022F8B0(record)` returns at once when the record's `+0x20` is already non-zero¹. Otherwise it
  walks `+0x14` ids of the part's u16 id list `[part + 0x28]`, from index `+0x12` (part `[record + 8]`,
  `0x0022F8C8`-`0x0022F90D`).
- It skips every id outside `0x4000`-`0x4FFF`², so polygons are never tested. Wall record
  `id - 0x4000` of `[part + 0x18]` is tested as `0x00381EB0(wall record, [record + 0x18])`³.
  The first hit sets `+0x20` to 1 and ends the walk⁴.
- A set bit `0x40000000` makes a type-1 polygon or wall record invisible to kind-4 queries only. `0x0022D4B0` and
  `0x0022CC50` read the query kind from `+0x46` of the query, keep the wall for every other kind and skip
  it for kind 4. Type-4 polygons are the mirror image: they are hit only by kind-4 queries.
- The movement sweep sets `+0x46` to 2, or to 3 when flag bit `0x1` of the record is set⁵, so
  a `setmapidwall(g, 6, v)` never changes where a walking body stops. None of the five wall readers
  above issues a kind-4 query itself; the kind-4 caller lies outside them.
- Bit `0x4000000` on a type-1 polygon or wall record makes `0x0022D7E0` skip it unless the query's `+0x3C` is
  non-zero. No verb reaches bit `0x4000000` of a wall entry, so this is authored data only.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0022F8BD` |
| ² | `0x0022F914`-`0x0022F91B` |
| ³ | `0x0022F961`-`0x0022F968` |
| ⁴ | `0x0022F97D` |
| ⁵ | `0x002327D0` |

</details>

### The ground field and bit `0x1000`

`0x003808A0(record, part)` runs after a body moved¹ or was placed². From the
effective attribute of the body's polygon it stores the floor group into `+0x56`, the mj group into
`+0x58`, bit `0x1000` into flag bit `0x4` of `+0x60`, and the five-bit ground field (`0x00231F80`, bits `0x7C0000` after
overrides) into `+0x5A`. `0x00231F80` has that one caller³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00380C40` |
| ² | `0x00380D30` |
| ³ | `0x0038090E` |

</details>

The record is the placement at `+0x30` of an actor's movement body (the qword at `[actor + 0xC0] + 0x138`), so the
body holds the floor group at `+0x86` and the ground field at `+0x8A`. The script reads them through two helpers that
return -1 when the actor has no body, and writes the ground field through a third that then writes nothing:

| Verb | Handler | Helper | Effect |
|---|---|---|---|
| `0x2EA` `getmapid()` | `0x00348100` | `0x002E9890` | pushes the floor group of the running actor, negatives as 0 |
| `0x48B` `getmapid_48b(actor)` | `0x00347240` | `0x002E9890` | the same for the actor `0x00263770` finds |
| `0x2FF` `getmapgroundtype()` | `0x0034E0E0` | `0x002E9830` | pushes the ground field, negatives as 0 |
| `0x48C` `getmapgroundtype_48c(actor)` | `0x003476B0` | `0x002E9830` | the same for a given actor |
| `0x4E2` `setmapgroundtype(v)` | `0x0034E510` | `0x002EBC70` | writes `v` to the running actor's `+0x8A` |
| `0x4E3` `setmapgroundtype_4e3(actor, v)` | `0x00347D20` | `0x002EBC70` | the same for a given actor |

The ground field also picks an effect: the presentation command `0x18`¹ calls
`0x003B0C50`, which plays effect 100 for ground 0 to 3, 7, 9, 13 and 14, 101 for 4, 102 for 5,
103 for 11, 12 and 15, 148 for 16 and 18, and nothing for the others². A
`setmapgroundtype` write lasts until the body's next move or placement rewrites `+0x8A`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00520C80` |
| ² | `0x003B02A0` |

</details>

Two of those effects carry a float, stored at the new effect's `+0x36C` with bit `0x800` set in its word `+0x368`: 148
takes `+0x144` of the actor's render record (`[0x022C6F28] + 0x740 × id`, `0x003B0D3E`), whose `+0x108` is the actor, and
103 takes the float `+0xC0` of the record at qword `+0x138` of the actor's `+0xC0` record¹ when bit `0x8`
of that record's dword `+0x90` is set².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002E98C0` |
| ² | `0x002E9860` |

</details>

### Asking whether a bit is overridden

`0x0026E300(entry, kind)`, reached through the thunk `0x0032A780`, maps the kind through the table
`0x00915760` = {23, 25, 26, 27, -1, 24} and returns -1 for kind 4, 0 when the mask bit is clear
(authored data applies), 1 when the bit is overridden to 0 and 2 when it is overridden to 1.
The kind is not range-checked¹: the dword after the table is `0xC2C80000`, the float -100.0, so kind 6
also returns -1², and kind 7 reads 0 and tests bit `0x1` of the entry.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0026E30E` |
| ² | `0x0026E317` |

</details>

Its two callers belong to the long-range route graph at `[0x02AEDFB0]`: the edge-cost function `0x00383850`
and the graph walk `0x0033D3E0`. Both read 8-byte edge records whose `+4` is -1 when the edge has no
override entry, whose `+5` is an override entry and whose `+6` is the authored kind bitmask. The edge is:

- usable when the answer is 1 (the gate was opened with `v = 1`, even where the authored mask forbade
  the kind);
- unusable when the answer is 2 (`0x00383850` returns the cost `0x7FFFFFFF`);
- decided by the authored kind bitmask when the answer is 0 or the edge has no entry.

So a `setmapidfloor(g, kind, 0)` closes both the polygons of group `g` and every route-graph edge
tagged with entry `g` for that kind.

### Showing and hiding map models

`0x00379010(id, mode)` edits two 64-bit masks, the forced-on set `0x0209A6C0` and the forced-off set
`0x0209A6C8`, at bit `id & 0x3F`; any mode other than 0, 1 and 2 writes neither mask¹:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0037901C` |

</details>

| mode | 0x0209A6C0 | 0x0209A6C8 | verb and handler |
|---|---|---|---|
| 1 | set | clear | `showmapmodel` 0x10C `0x00347FD0`; `showmapmodel_113` 0x113 `0x00347C90` takes the mode as its second operand |
| 0 | clear | set | `hidemapmodel` 0x10D `0x003482F0` |
| 2 | clear | clear | `defaultmapmodel` 0x270 `0x00348680` |

Two readers turn the masks into the hidden set of the frame:

- `0x0026E5D0()` returns `0x0209A6C8 & ~0x0209A6C0`: only what a script forced off.
- `0x0026E5F0()` returns `~0x0209A6C0 & (0x0209A6C8 | base)`, where `base` is `0x0209A690` when `0x0209A6FC`
  is 0 and `(0x0209A690 | 0x0209A6A0) & ~0x0209A698` otherwise. `0x0209A690` is the collision part's own
  hidden set `[[part] + 0x30]`, copied once at bind¹. `0x0209A6A0` and `0x0209A698` are copied
  every frame by `0x003820C0`² from `[part + 0x50]` and `[part + 0x48]`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0026E9DC` |
| ² | `0x00382810`, `0x00382817` |

</details>

While no map is bound (`0x0209A670` is 0) `0x0026E5F0` returns 0¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0026E5F0`-`0x0026E5F8` |

</details>

`0x0209A6FC` is set to 1 by `0x0026E1D0`, by `0x0026E960` and by the zone's manager-0 start-up `0x002628B0`¹; the verb `setmapmodelstatus` (0x3EE, `0x003526D0`) writes its operand into it through
`0x00379070`. A model with its bit in the hidden set is not drawn, while its collision polygons are
untouched: hiding a gate model and opening its floor group are two separate writes.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00262B53` |

</details>

Four consumers read the hidden set:

- the draw-list build `0x002F5550`¹ tests a model's 64-bit group mask at `+0x20`
  of its 0x30-byte record against it;
- the draw pass `0x002F4520`² consults it for models with a group byte at `+0x1C`;
- the background-animation update `0x004668C0`³ skips entries whose group bit is hidden;
- `0x003ECCA0`⁴ does the same for its entries.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002F5611`, `0x002F562F` |
| ² | `0x002F4B99` |
| ³ | `0x004668E4` |
| ⁴ | `0x003ECD84` |

</details>

### Camera regions

The part's shown and hidden sets of the frame come from type-3 polygons around the camera. Each frame
the camera update `0x003820C0` calls `0x00233230(part, 0x02AEDEE0)`¹ with the collision part
(`0x0026E500(0)`) and the camera position, the fourth row of the camera matrix copy at `0x02AEDEB0`:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003827FB` |

</details>

1. `0x00382080` zeroes the 64 fade weights at `0x02EBF278`, and the part's sets `+0x48`, `+0x50`,
   `+0x58` and `+0x60` are zeroed;
2. `0x00233050` finds the camera's cell in the part's grid, and the polygons listed for the cell are
   walked;
3. a type-3 polygon for which `0x002324F0` returns a negative value at the camera position applies its
   attribute word: with bit `0x8` set, the value `v` in the bits under mask `0xFF0000` sets bit `v` of `+0x48` (shown models)
   when below 64, else bit `v - 64` of `+0x58`; with bit `0x10` set, the value in the bits under mask `0xFF000000` does the same
   with `+0x50` (hidden models) and `+0x60`.

For a model value below 64 `0x0022FF10(part, polygon, camera, v)` also writes the fade weight
`0x02EBF278[v]`: the camera's barycentric weights in the polygon¹ applied to the byte `+0x0F`
of its three vertices, divided by 255. `0x003820C0` then copies `+0x48`, `+0x50`, `+0x58` and `+0x60` to
`0x0209A698`, `0x0209A6A0`, `0x0209A6B0` and `0x0209A6B8` (`0x00382810` to `0x00382825`).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0022F050` |

</details>

The draw pass multiplies the alpha of a model whose group byte `+0x1C` is 1 to 254 and whose bit is
not in the hidden set by `0x02EBF278[group]`¹, so a region painted with vertex alpha fades
its models in across the polygon. `0x003ECCA0` and `0x002F1F40` read the weights too.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002F4FDF` |

</details>

### Map effects

The values 64 and above of a camera region name map effect channels, and the effect channels have
script masks of their own. `0x00378FB0(channel, mode)` edits the forced-on set `0x0209A6D0` and the
forced-off set `0x0209A6D8` at bit `channel & 0x3F`, with the same modes as `0x00379010`:

| mode | 0x0209A6D0 | 0x0209A6D8 | verb and handler |
|---|---|---|---|
| 1 | set | clear | `showmapeffect` 0x4F8 `0x00345AC0`; `showmapeffect_4fa` 0x4FA `0x003455B0` takes the mode as its second operand |
| 0 | clear | set | `hidemapeffect` 0x4F9 `0x003460A0` |
| 2 | clear | clear | `defaultmapeffect` 0x4FB `0x00346600` |

Each world step `0x0026EB30` (from `0x0036F510`) computes the hidden effect set
`((0x0209A6A8 | 0x0209A6B8) & ~0x0209A6B0 | 0x0209A6D8) & ~0x0209A6D0`, where `0x0209A6A8` is the part's own
set `[[part] + 0x38]` copied at bind¹, or 0 while no map is bound. For each of the 64
channels whose bit differs from the previous frame's set `0x0209A6E0` it stops the channel² when the bit is set and starts it for the current weather slot `0x0209A6E8`
(`0x0026FEB0`, which runs `0x0026FAD0(channel, slot, 0)`) when it is clear.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0026E9EA` |
| ² | `0x0026FE50` |

</details>

### A new map clears everything

The field tick's request handler `0x003775D0` calls `0x00378120`¹ when bit `0x8` of `0x02ADD0F0` is
set, and `0x00378120` calls `0x0026E760`² with the new map data:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003776DD` |
| ² | `0x00378193` |

</details>

| Step | What happens | Where in the code |
|---|---|---|
| 1 | `0x0026E640` zeroes `0x0209A6C0`, `0x0209A6C8`, `0x0209A690` to `0x0209A6B8` and the rest of the model block, and sets the 32 shorts at `0x0209A71C` to 0xFFFF. |   |
| 2 | `0x0026E960(map)` binds the map:<br>• it stores the map in `0x0209A670` before it tests it; a null map goes straight to the tail jump to `0x003ED870(map)`;<br>• it stores -100.0 at `0x0209A6F4` and 1 at `0x0209A6FC` and at `0x0209A708`;<br>• each part descriptor `map + 0x40` and `map + 0xA8` whose first qword is non-zero is stored in `0x0209A678` or `0x0209A680`; from the first it copies `[[part] + 0x30]` into `0x0209A690` and `[[part] + 0x38]` into `0x0209A6A8`;<br>• it zeroes all 80 masks, calling `0x003278D0` after each one; the value words keep what they held;<br>• it stores `0x003ED0B0()` in `0x0209A2D0`, calls `0x003ED020(i, 0x0209A2F0 + 0x30 × i, 0x0209A300 + 0x30 × i)` for i = 0 to 2, then `0x003ECFD0(0x0209A370)`, `0x003ED140()` and `0x003B6BA0()`, and ends with the tail jump to `0x003ED870(map)`. | `0x0026E966`<br>`0x0026EAB1`<br>`0x0026E999`-`0x0026E9B0`<br>`0x0026E9CE`, `0x0026E9F1`<br>`0x0026E9D8`-`0x0026E9EA`<br>`0x0026EA13`-`0x0026EA55`<br>`0x0026EA57`-`0x0026EA9A` |

`0x0209A3E0` and `0x0209A3E4` are referenced by the four writers, by `0x0026E960` and by the twelve readers
named on this page and by nothing else (38 and 23 references). `0x0209A6C0` and `0x0209A6C8` are referenced
only by `0x00379010`, `0x0026E640`, `0x0026E5D0` and `0x0026E5F0`. No save-image copy exists among those
references: the table and the masks are state of the loaded map only.

## Layouts

<details>
<summary>Show the memory layouts</summary>

`MapIdOverride` (`0x8` bytes, offsets from the start of the 0x0209A3E0):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | mask | bits replaced; set by `0x0026E880`, cleared by `0x0026E850`, `0x0026E130`, `0x0026E150` and `0x0026E960` |
| `+0x04` | `u32` | value | replacement bits; written by `0x0026E880` only |

Eighty entries: floors 0x00-0x1F, walls 0x20-0x3F, mj groups 0x40-0x4F.

`CollisionPolygon` (`0x20` bytes, offsets from the start of the polygon):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `f32[3]` | normal | plane normal, dotted with a vertex in `0x0022DE60` and `0x0022D7E0` |
| `+0x0C` | `u32` | attr | the attribute word (field table in How it works) |
| `+0x10` | `i16[3]` | vertex | indices into the `0x10`-byte vertex array at [part + 8]; `0x00231A90` reads the vertex colour at `+0xC` |
| `+0x16` | `i16[3]` | neighbour | polygon id across each edge, -1 for no neighbour (`0x0022F9B0`) |
| `+0x1C` | `u32` | flags | bit `0x400` is tested by `0x0022E7D0` (`0x0022E93B`), from `0x0022D7E0`, and by `0x0022EAC0` (`0x0022ECA2`), from `0x0022DE60`: no contact past the third edge; the polygon readers `0x00230A40`, `0x0022CC50`, `0x0022D4B0`, `0x0022D7E0`, `0x0022DE60`, `0x0022F9B0`, `0x00231A90`, `0x00232090`, `0x002321D0`, `0x00233110` and `0x00233230` read nothing from `+0x1C` to `+0x1F` themselves |

`RouteEdge` (`0x8` bytes, offsets from the start of the edge):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u16` | nodeA | node index; node positions are 8-byte pairs at [graph + `0xC`] (`0x00383850`) |
| `+0x02` | `u16` | nodeB | node index |
| `+0x04` | `i8` | hasEntry | -1 when the edge has no override entry (`0x00383850`) |
| `+0x05` | `u8` | entry | override table entry passed to `0x0026E300` (`0x00383850`, `0x0033D3E0`) |
| `+0x06` | `u8` | kinds | authored kind bitmask, bit k means kind k may use the edge |
| `+0x07` | `u8` | pad | read by no function: the edge table [graph + `0x14`] is reached by `0x00383850` (`+0x04` to `+0x06`), `0x0033D3E0` (`+0x05`, `+0x06`), `0x00382FF0` and `0x00383C90` (`+0x00`, `+0x02`) and the relocation `0x00384160`, and none of the ten byte reads at +7 of an 8-byte-stride record in the image belongs to a function that reaches the graph; nothing fixes its width |

The edge table is `[graph + 0x14]` and the node-pair adjacency table `[graph + 0x1C]`, both resolved
through `0x0020E600`; `graph + 0xA` is the node count.

</details>

## Operations

A script opens a gate for walking bodies and shows the open model:

1. `setmapidfloor(g, 0, 1)`: `0x00343E60` pops the operands and calls `0x003792E0(g, 0, 1)`.
2. `0x003792E0` calls `0x0026E880(g, 0, 23, 1)`: mask bit `0x800000` of entry `g` is set and value bit `0x800000` is 0.
3. `0x0026E880` calls `0x003278D0`, which clears the cached navigation block of every registered body
   with bit `0x10` of its first byte set.
4. `showmapmodel(id)`: `0x00347FD0` calls `0x00379010(id, 1)`, setting the forced-on bit and clearing the
   forced-off bit.
5. On the next frame `0x0026E5F0()` no longer contains the model's bit and `0x002F5550` draws it; a kind-0
   body that crosses into a polygon of group `g` gets 1 from `0x00230A40` and walks through.

A body steps towards a blocked polygon:

1. `0x00380C40` calls `0x002327D0` with the record, its polygon and the move vector.
2. For each edge crossed, `0x002327D0` reads the neighbour polygon and calls `0x00230A40(part, polygon,
   kind)`.
3. `0x00230A40` builds `eff` from the floor and mj entries, finds `eff & 7 == 0` and returns 0 because the
   kind's bit is set.
4. `0x002327D0` treats the edge as a wall and `0x0022F9B0` slides the body along it.
5. `0x003808A0` then records the floor group, mj group, ground field and bit `0x1000` of the polygon the body
   stays on.

## State

<details>
<summary>Show the state it keeps</summary>

| address | contents | written by | cleared by |
|---|---|---|---|
| `0x0209A3E0` | 80 override entries, 640 bytes | `0x0026E880`, `0x0026E850`, `0x0026E130`, `0x0026E150` | `0x0026E960` at map bind |
| `0x0209A6C0` | forced-on model mask | `0x00379010` | `0x0026E640` |
| `0x0209A6C8` | forced-off model mask | `0x00379010` | `0x0026E640` |
| `0x0209A690` | the part's hidden model set | `0x0026E960` | `0x0026E640` |
| `0x0209A698`, `0x0209A6A0` | the part's shown and hidden sets of the frame | `0x003820C0` | `0x0026E640` |
| `0x0209A6FC` | 1: the part's sets take part in `0x0026E5F0` | `0x0026E1D0`, `0x0026E960`, `0x002628B0`, `0x00379070` | never cleared by the functions here |
| `0x0209A670` | the bound map; 0 before a map is bound | `0x0026E960` | `0x0026E1D0` (`0x0026E20C`); `0x003EC860` (`0x003EC885`, after it releases the map), from the map teardowns `0x0026E760`, `0x0026E7D0`, `0x0026EAC0` and `0x0026EAF0` |
| `0x0209A678`, `0x0209A680` | the two part descriptors | `0x0026E960` | `0x0026E640` |
| `0x0209A6D0`, `0x0209A6D8` | forced-on and forced-off map effect masks | `0x00378FB0` | `0x0026E640` |
| `0x0209A6A8` | the part's hidden effect set | `0x0026E960` | `0x0026E640` |
| `0x0209A6B0`, `0x0209A6B8` | the camera regions' shown and hidden effect sets | `0x003820C0` | `0x0026E640` |
| `0x0209A6E0` | the hidden effect set of the last step | `0x0026EB30` | replaced by `0x0026EB30` every step (`0x0026ED3C`); zeroed by `0x0026E640` (`0x0026E697`), from `0x0026E1D0` and the map teardowns `0x0026E760`, `0x0026E7D0`, `0x0026EAC0` and `0x0026EAF0` |
| `0x02EBF278` | 64 `f32` fade weights of the camera regions | `0x0022FF10` | `0x00382080`, every frame |

The resets also write four words beside the model block, each 0 at load (the zero-filled tail of `.data`). No
instruction reads `0x0209A700`, `0x0209A70C` or `0x0209A714` at these addresses. `0x0209A704` is read: it is the
`setskyonly` flag, and while it is set the draw-list build `0x002F5550` skips every instance without the sky bit
`0x10000000` (`0x002F5E03`-`0x002F5E10`, [weather](weather.md)):

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x0209A700` | `u32` | 0 | cleared together with `0x0209A704` (below) by one qword store of 0 | `0x0026E1D0` (`0x0026E21A`, 8 bytes, covering `0x0209A700`-`0x0209A707`) | no instruction at this address |
| `0x0209A704` | `u32` | 0 | the `setskyonly` flag, the word after `0x0209A700`: the map set-up clears it, the map teardown clears it, `0x00379930(x)` stores its argument, and the draw-list build reads it | `0x0026E1D0` (`0x0026E21A`, in the same qword store); `0x00378120`, 0 (`0x0037814C`); `0x00378230`, 0 (`0x00378253`); `0x00379930` (`0x00379930`, its first argument) | `0x002F5550` (`0x002F5585`) |
| `0x0209A70C` | `u64` | 0 | all bits set: `0xFFFFFFFFFFFFFFFF`, stored as one qword | `0x0026E640` (`0x0026E6CA`) | no instruction at this address |
| `0x0209A714` | `u64` | 0 | all bits set, stored as one qword; it ends at `0x0209A71B`, just before the 32 anchor words at `0x0209A71C` that the same reset fills with `0xFFFF` (`0x0026E6EE`) | `0x0026E640` (`0x0026E6D5`) | no instruction at this address |

The anchor-word reader `0x003A6FC0(n)` sign-extends `n` and does not bound it¹, so an `n` from -8
to -1 would read these two qwords; the draw-list build `0x002F5550` writes an anchor word only for an index from 0 to 31².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003A6FD0`-`0x003A6FDA` |
| ² | `0x002F653F`-`0x002F654B` |

</details>

None of these addresses is read or written by the save image functions referenced from them; the state
is rebuilt from the map and its script on every load.

</details>

## Modding notes

- A floor group number in a script is the polygon's bits under mask `0x3E000`; a wall group is the same field on a
  type-1 polygon or wall record; an mj group is the bits under mask `0x78`. The `+0x20` and `+0x40` banks are offsets the
  natives add, not separate ids a script would write.
- `v = 1` opens and `v = 0` closes in every bank, even though the stored bit is inverted between floors
  and walls. A negative `v` restores the authored bit; the `resetmapid*` verbs restore whole entries.
- Kind numbers differ between writer and reader: writing kind 7 affects reader kind 5. Kind 4 bodies
  ignore floor overrides entirely, and kind-6 wall writes affect only kind-4 queries, never walking.
- An mj override is applied after the floor override, so it can reopen a bit a floor override closed on
  the polygons that carry its group.
- Collision and models are independent. A gate that should look closed needs both `setmapidfloor` or
  `setmapidwall` and `hidemapmodel` or `showmapmodel`; a route-graph edge closes with the floor bit
  only if the edge record carries that entry.
- Everything here is cleared when `0x0026E760` binds a new map. A persistent gate must be re-applied by
  the area script from its own saved variables.

## Related

- [Script verb dispatch and parameter encoding](../Scripts-And-Script-Commands/verb-dispatch.md)
- [Zone changes: mapjump and the other jump verbs, the loading flags, the moment the new zone is ready and what names a map](zone-changes-and-mapjump.md)
- [Area flags: the navimapdata.bin record for every area, the town flag, the KO, Stone and X-Zone override and the other bits](area-flags-navimapdata.md)
- [How a unit finds its way across the navigation mesh](../Movement-And-Pathfinding/navigation-mesh-and-pathfinding.md)
- [The map ctrl pack](mpk-map-pack.md)

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 1 call with 1 other topic</summary>

**Status effects and KO** (explained on [frame update order](../Engine-Core/frame-update-order.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00265680`](../Story-Events-And-Hunts/script-censuses.md) (on script censuses) | is called by | [`0x00310DB0`](../Battle-Actions/action-results.md) Battle unit: run periodic combat maintenance (on action results) |

</details>

---

[← Zone changes](zone-changes-and-mapjump.md)
