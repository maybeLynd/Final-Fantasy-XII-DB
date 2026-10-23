---
title: "Doors, gates and map changes: the override table the setmapid verbs write, what its floor, wall and mj bits block, the show and hide model masks and when a new map clears them"
kind: "system"
category: "World, areas and travel"
addresses: "0x0209A3E0, 0x0026E880, 0x003792E0, 0x003795A0, 0x00379430, 0x00232020, 0x00230A40, 0x0022F8B0, 0x0026E300, 0x00379010, 0x0026E5F0, 0x0026E960, 0x003278D0"
---

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
and an id from 0x4000 names a wall record (`0x0022F8B0`, `0x0022DE60`). The attribute word sits at `+0xC` of
a polygon and at `+4` of a wall record. Its fields, with the functions that read each one:

| bits | field | written by a verb | read by |
|---|---|---|---|
| 0-2 | polygon type: 0 floor, 1 wall, 2 and 4 marker polygons, 3 camera region | none | `0x00230A40`, `0x0022D4B0`, `0x0022CC50`, `0x00231A90`, `0x002321D0`, `0x00233230` |
| 3-6 | mj group 0-15; selects override entry `0x40 + group` | none | `0x00232020`, `0x00230A40`, `0x00232090`, `0x00231F80`, `0x002321D0`, `0x00231A90` |
| 12 | copied into bit 2 of the body's flag word | `setmapidfloor` kind 9 | `0x003808A0` |
| 13-17 | floor group 0-31; the wall group on type-1 polygons and wall records | none | every override reader below |
| 18-22 | ground field | `setmapidfloorground` | `0x00231F80` |
| 23-27 | block bits for movement kinds 0, 5, 1, 2, 3 (bits 23, 24, 25, 26, 27) | `setmapidfloor`, `setmapidmj` | `0x00230A40`, `0x00232090`, `0x0022D4B0`, `0x0022CC50` |
| 26 | on type-1 polygons and wall records: skipped by the sphere sweep | none | `0x0022D7E0` |
| 30 | wall ignored by kind-4 queries | `setmapidwall` kind 6 | `0x0022D4B0`, `0x0022CC50` |
| 31 | wall switched off | `setmapidwall` kind 5 | `0x0022F8B0`, `0x0022DE60`, `0x0022D7E0`, `0x0022D4B0`, `0x0022CC50` |

`0x00230A40` closes a polygon to every movement kind when there is no neighbour across the edge (`0x00230A4F`) or the
polygon type (bits 0-2, after the overrides) is not 0 (`0x00230AB9`). Otherwise kinds 0, 1, 2, 3 and 5 test their block bit;
kind 4 and kinds 6 and above have none and pass every floor polygon (`0x00230B4A`).

### The override table

`0x0209A3E0` holds 80 entries of two 32-bit words, `mask` then `value`, 8 bytes each, from `0x0209A3E0` to
`0x0209A65F`. A set mask bit means that bit of the attribute word is replaced by the value bit. A clear
mask bit lets the authored bit through. The three banks follow from the writers' offsets (`0x003795A0`
adds `0x20` to the entry, `0x00379430` adds `0x40`) and from the three zeroing loops of `0x0026E960`
(`0x0209A3E0`-`0x0209A4DF`, `0x0209A4E0`-`0x0209A5DF`, `0x0209A5E0`-`0x0209A65F`):

| entries | addresses | bank | selected by |
|---|---|---|---|
| 0x00-0x1F | 0x0209A3E0-0x0209A4DF | floors | attribute bits 13-17 of a floor polygon |
| 0x20-0x3F | 0x0209A4E0-0x0209A5DF | walls | attribute bits 13-17 of a wall polygon or wall record, plus 0x20 |
| 0x40-0x4F | 0x0209A5E0-0x0209A65F | mj groups | attribute bits 3-6, plus 0x40 |

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

### The writers and the path reset

Four functions write the table, and each ends in a call to `0x003278D0`:

| function | arguments | effect |
|---|---|---|
| `0x0026E880` | entry, v, bit, width | `mask \|= ((1 << width) - 1) << bit`, then those bits of `value` become `v << bit` |
| `0x0026E850` | entry, bit, width | clears those mask bits, so the authored bits show through again |
| `0x0026E130` | entry | `mask := 0` for one entry |
| `0x0026E150` | first, count | `mask := 0` for `count` consecutive entries |

`0x003278D0` walks the body registry (`0x00236850` is the count, `0x00236820(i)` returns the 0xF50-byte body
`i` at `[0x0208E688]`). For every body whose first byte has bit 4 set it calls `0x003839C0` and `0x003839F0` on
the body's `+0x200` block: the two shorts at `+0xC` and `+0xE` become 0xFFFF and the 0x80 bytes from
`+0x10` become 0xFF. Nothing else is written, and no map model is touched by any of the four writers.

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
| 0xF6 | resetmapidfloorall | `0x003416E0` | `0x003791D0(-1)` | none; -1 is pushed and popped |
| 0xF7 | resetmapidfloor | `0x00341290` | `0x003791D0(g)` | g |
| 0xF8 | resetmapidwallall | `0x00341E30` | `0x00379270(-1)` | none |
| 0xF9 | resetmapidwall | `0x00341A90` | `0x00379270(g)` | g |
| 0xFA | resetmapidmjall | `0x003424D0` | `0x00379220(-1)` | none |
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
is negative. `0x00379270(g)` calls `0x0026E130(g + 0x20)` or `0x0026E150(0x20, 0x20)` (`0x00379274`).
`0x00379220(g)` calls `0x0026E130(g + 0x40)` or `0x0026E150(0x40, 0x10)` (`0x00379224`-`0x00379229`).

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

A body's movement kind is the byte at `+0x50` of its navigation record, the record `0x003808A0`,
`0x002327D0` and `0x00380D30` work on. The readers of the block bits are:

- `0x00230A40(part, polygon, kind)` applies the overrides and returns 0 when `eff & 7` is not 0 (not a
  type-0 floor polygon). Otherwise it returns 1 when the kind's bit is clear: kind 0 tests bit 23, kind
  1 bit 25, kind 2 bit 26, kind 3 bit 27, kind 5 bit 24. Kind 4 and kinds above 5 always get 1.
- `0x00232090(part, polygon)` packs the same five bits into a kind bitfield (bit k set means kind k is
  blocked: bit 0 from 23, bit 1 from 25, bit 2 from 26, bit 3 from 27, bit 5 from 24) and returns 0
  when `eff & 7` is not 0.
- `0x002327D0`, the movement sweep called from `0x00380C40`, asks `0x00230A40` (`0x00232EB9`) about each
  neighbouring polygon the body is about to cross into. A 0 answer makes the sweep treat that edge as a
  wall (`0x0022F9B0`, `0x0022FB2C`), so the body slides along the boundary of a blocked polygon exactly as
  along a wall.
- `0x00233110`, called by `0x00380D30` and `0x00231400`, picks the polygon under a point from the cell's list
  and skips every polygon `0x00230A40` refuses (`0x002331C0`).
- `0x00380D30(record, position)` places a body: after finding its polygon it reads `0x00232090` into
  `+0x5E` and, when the body's own kind bit is set, writes 0xFFFE into the polygon slot `+0x52`. The body
  is then standing on ground that is closed to it.
- `0x00231A90` searches the body's cell for type-2 and type-4 marker polygons (stored at `+0x5C` and
  `+0x54`), using the overridden type bits.

The verb's kind numbers and the reader's kind numbers differ in one place: a script that writes
kind 7 sets bit 24, and bit 24 is what the reader tests for movement kind 5.

### What the wall bits do

Walls are tested by the collision callback `0x0022F8B0` (installed through `0x0022F830` by `0x00232490` and
`0x00231400`), the sphere sweep `0x0022D7E0`, and the ray casts `0x0022DE60`, `0x0022D4B0` and `0x0022CC50`.
Each applies the wall entry to the attribute word and then decides as follows.

- A set bit 31 removes the wall. `0x0022F8B0` calls the contact test `0x00381EB0` only while `eff` is below
  `0x80000000` (and only when its record's `+0x24` is non-zero; with it zero every wall is tested).
  `0x0022DE60` and `0x0022D7E0` skip type-1 polygons and wall records whose bit 31 is set.
- A set bit 30 makes a type-1 polygon or wall record invisible to kind-4 queries only. `0x0022D4B0` and
  `0x0022CC50` read the query kind from `+0x46` of the query, keep the wall for every other kind and skip
  it for kind 4. Type-4 polygons are the mirror image: they are hit only by kind-4 queries.
- The movement sweep sets `+0x46` to 2, or to 3 when flag bit 0 of the record is set (`0x002327D0`), so
  a `setmapidwall(g, 6, v)` never changes where a walking body stops. None of the five wall readers
  above issues a kind-4 query itself; the kind-4 caller lies outside them.
- Bit 26 on a type-1 polygon or wall record makes `0x0022D7E0` skip it unless the query's `+0x3C` is
  non-zero. No verb reaches bit 26 of a wall entry, so this is authored data only.

### The ground field and bit 12

`0x003808A0(record, part)` runs after a body moved (`0x00380C40`) or was placed (`0x00380D30`). From the
effective attribute of the body's polygon it stores the floor group into `+0x56`, the mj group into
`+0x58`, bit 12 into flag bit 2 of `+0x60`, and the five-bit ground field (`0x00231F80`, bits 18-22 after
overrides) into `+0x5A`. `0x00231F80` has that one caller (`0x0038090E`).

The record is the placement at `+0x30` of an actor's movement body (`[actor + 0xC0] + 0x138`), so the
body holds the floor group at `+0x86` and the ground field at `+0x8A`. The script reads and writes
them through three helpers that return -1 when the actor has no body:

| Verb | Handler | Helper | Effect |
|---|---|---|---|
| `0x2EA` `getmapid()` | `0x00348100` | `0x002E9890` | pushes the floor group of the running actor, negatives as 0 |
| `0x48B` `getmapid_48b(actor)` | `0x00347240` | `0x002E9890` | the same for the actor `0x00263770` finds |
| `0x2FF` `getmapgroundtype()` | `0x0034E0E0` | `0x002E9830` | pushes the ground field, negatives as 0 |
| `0x48C` `getmapgroundtype_48c(actor)` | `0x003476B0` | `0x002E9830` | the same for a given actor |
| `0x4E2` `setmapgroundtype(v)` | `0x0034E510` | `0x002EBC70` | writes `v` to the running actor's `+0x8A` |
| `0x4E3` `setmapgroundtype_4e3(actor, v)` | `0x00347D20` | `0x002EBC70` | the same for a given actor |

The ground field also picks an effect: the presentation command `0x18` (`0x00520C80`) calls
`0x003B0C50`, which plays effect 100 for ground 0 to 3, 7, 9, 13 and 14, 101 for 4, 102 for 5,
103 for 11, 12 and 15, 148 for 16 and 18, and nothing for the others (`0x003B02A0`). A
`setmapgroundtype` write lasts until the body's next move or placement rewrites `+0x8A`.

Two of those effects carry a float, stored at the new effect's `+0x36C` with bit `0x800` set in its word
`+0x368`: 148 takes the actor's `+0x144`, and 103 takes the float `+0xC0` of the record at qword `+0x138`
of the actor's `+0xC0` record (`0x002E98C0`) when bit 3 of that record's dword `+0x90` is set (`0x002E9860`).

### Asking whether a bit is overridden

`0x0026E300(entry, kind)`, reached through the thunk `0x0032A780`, maps the kind through the table
`0x00915760` = {23, 25, 26, 27, -1, 24} and returns -1 for kind 4, 0 when the mask bit is clear
(authored data applies), 1 when the bit is overridden to 0 and 2 when it is overridden to 1.

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
`0x0209A6C8`, at bit `id & 0x3F`:

| mode | 0x0209A6C0 | 0x0209A6C8 | verb and handler |
|---|---|---|---|
| 1 | set | clear | `showmapmodel` 0x10C `0x00347FD0`; `showmapmodel_113` 0x113 `0x00347C90` takes the mode as its second operand |
| 0 | clear | set | `hidemapmodel` 0x10D `0x003482F0` |
| 2 | clear | clear | `defaultmapmodel` 0x270 `0x00348680` |

Two readers turn the masks into the hidden set of the frame:

- `0x0026E5D0()` returns `0x0209A6C8 & ~0x0209A6C0`: only what a script forced off.
- `0x0026E5F0()` returns `~0x0209A6C0 & (0x0209A6C8 | base)`, where `base` is `0x0209A690` when `0x0209A6FC`
  is 0 and `(0x0209A690 | 0x0209A6A0) & ~0x0209A698` otherwise. `0x0209A690` is the collision part's own
  hidden set `[[part] + 0x30]`, copied once at bind (`0x0026E9DC`). `0x0209A6A0` and `0x0209A698` are copied
  every frame by `0x003820C0` (`0x00382810`, `0x00382817`) from `[part + 0x50]` and `[part + 0x48]`.

`0x0209A6FC` is set to 1 by `0x0026E1D0`, by `0x0026E960` and by the zone's manager-0 start-up `0x002628B0`
(`0x00262B53`); the verb `setmapmodelstatus` (0x3EE, `0x003526D0`) writes its operand into it through
`0x00379070`. A model with its bit in the hidden set is not drawn, while its collision polygons are
untouched: hiding a gate model and opening its floor group are two separate writes.

Four consumers read the hidden set:

- the draw-list build `0x002F5550` (`0x002F5611`, `0x002F562F`) tests a model's 64-bit group mask at `+0x20`
  of its 0x30-byte record against it;
- the draw pass `0x002F4520` (`0x002F4B99`) consults it for models with a group byte at `+0x1C`;
- the background-animation update `0x004668C0` (`0x004668E4`) skips entries whose group bit is hidden;
- `0x003ECCA0` (`0x003ECD84`) does the same for its entries.

### Camera regions

The part's shown and hidden sets of the frame come from type-3 polygons around the camera. Each frame
the camera update `0x003820C0` calls `0x00233230(part, 0x02AEDEE0)` (`0x003827FB`) with the collision part
(`0x0026E500(0)`) and the camera position, the fourth row of the camera matrix copy at `0x02AEDEB0`:

1. `0x00382080` zeroes the 64 fade weights at `0x02EBF278`, and the part's sets `+0x48`, `+0x50`,
   `+0x58` and `+0x60` are zeroed;
2. `0x00233050` finds the camera's cell in the part's grid, and the polygons listed for the cell are
   walked;
3. a type-3 polygon for which `0x002324F0` returns a negative value at the camera position applies its
   attribute word: with bit 3 set, the value `v` in bits 16-23 sets bit `v` of `+0x48` (shown models)
   when below 64, else bit `v - 64` of `+0x58`; with bit 4 set, the value in bits 24-31 does the same
   with `+0x50` (hidden models) and `+0x60`.

For a model value below 64 `0x0022FF10(part, polygon, camera, v)` also writes the fade weight
`0x02EBF278[v]`: the camera's barycentric weights in the polygon (`0x0022F050`) applied to the byte `+0x0F`
of its three vertices, divided by 255. `0x003820C0` then copies `+0x48`, `+0x50`, `+0x58` and `+0x60` to
`0x0209A698`, `0x0209A6A0`, `0x0209A6B0` and `0x0209A6B8` (`0x00382810` to `0x00382825`).

The draw pass multiplies the alpha of a model whose group byte `+0x1C` is 1 to 254 and whose bit is
not in the hidden set by `0x02EBF278[group]` (`0x002F4FDF`), so a region painted with vertex alpha fades
its models in across the polygon. `0x003ECCA0` and `0x002F1F40` read the weights too.

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
set `[[part] + 0x38]` copied at bind (`0x0026E9EA`), or 0 while no map is bound. For each of the 64
channels whose bit differs from the previous frame's set `0x0209A6E0` it stops the channel
(`0x0026FE50`) when the bit is set and starts it for the current weather slot `0x0209A6E8`
(`0x0026FEB0`, which runs `0x0026FAD0(channel, slot, 0)`) when it is clear.

### A new map clears everything

The field tick's request handler `0x003775D0` calls `0x00378120` (`0x003776DD`) when bit 3 of `0x02ADD0F0` is
set, and `0x00378120` calls `0x0026E760` (`0x00378193`) with the new map data:

1. `0x0026E640` zeroes `0x0209A6C0`, `0x0209A6C8`, `0x0209A690` to `0x0209A6B8` and the rest of the model block,
   and sets the 32 shorts at `0x0209A71C` to 0xFFFF.
2. `0x0026E960(map)` stores the map in `0x0209A670`, the two part descriptors `map + 0x40` and
   `map + 0xA8` in `0x0209A678` and `0x0209A680`, copies `[[part] + 0x30]` into `0x0209A690`, sets `0x0209A6FC`
   to 1 and zeroes all 80 masks, calling `0x003278D0` after each one.

`0x0209A3E0` and `0x0209A3E4` are referenced by the four writers, by `0x0026E960` and by the twelve readers
named on this page and by nothing else (38 and 23 references). `0x0209A6C0` and `0x0209A6C8` are referenced
only by `0x00379010`, `0x0026E640`, `0x0026E5D0` and `0x0026E5F0`. No save-image copy exists among those
references: the table and the masks are state of the loaded map only.

## Layouts

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
| `+0x10` | `i16[3]` | vertex | indices into the `0x10`-byte vertex array at [part + 8]; `0x00231A90` reads the vertex colour at +`0xC` |
| `+0x16` | `i16[3]` | neighbour | polygon id across each edge, -1 for none (`0x0022F9B0`) |
| `+0x1C` | `u8[4]` | tail | read and written by no function: the polygon array [part + `0x10`] is reached from the map `0x0209A678` by `0x0026E100`, `0x0026E350`, `0x0026E530`, `0x0026E640`, `0x0026E960`, `0x00377560` and `0x00377AB0`, and the polygon readers `0x00230A40`, `0x0022CC50`, `0x0022D4B0`, `0x0022D7E0`, `0x0022DE60`, `0x0022F9B0`, `0x00231A90`, `0x00232090`, `0x002321D0`, `0x00233110` (and its callers `0x00380D30`, `0x00231400`) and `0x00233230` read and write nothing from +`0x1C` to +`0x1F`; nothing fixes its width |

`RouteEdge` (`0x8` bytes, offsets from the start of the edge):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u16` | nodeA | node index; node positions are 8-byte pairs at [graph + `0xC`] (`0x00383850`) |
| `+0x02` | `u16` | nodeB | node index |
| `+0x04` | `i8` | hasEntry | -1 when the edge has no override entry (`0x00383850`) |
| `+0x05` | `u8` | entry | override table entry passed to `0x0026E300` (`0x00383850`, `0x0033D3E0`) |
| `+0x06` | `u8` | kinds | authored kind bitmask, bit k means kind k may use the edge |
| `+0x07` | `u8` | pad | read by no function: the edge table [graph + `0x14`] is reached by `0x00383850` (+`0x04` to +`0x06`), `0x0033D3E0` (+`0x05`, +`0x06`), `0x00382FF0` and `0x00383C90` (+`0x00`, +`0x02`) and the relocation `0x00384160`, and none of the ten byte reads at +7 of an 8-byte-stride record in the image belongs to a function that reaches the graph; nothing fixes its width |

The edge table is `[graph + 0x14]` and the node-pair adjacency table `[graph + 0x1C]`, both resolved
through `0x0020E600`; `graph + 0xA` is the node count.

## Operations

A script opens a gate for walking bodies and shows the open model:

1. `setmapidfloor(g, 0, 1)`: `0x00343E60` pops the operands and calls `0x003792E0(g, 0, 1)`.
2. `0x003792E0` calls `0x0026E880(g, 0, 23, 1)`: mask bit 23 of entry `g` is set and value bit 23 is 0.
3. `0x0026E880` calls `0x003278D0`, which clears the cached navigation block of every registered body
   with bit 4 of its first byte set.
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
5. `0x003808A0` then records the floor group, mj group, ground field and bit 12 of the polygon the body
   stays on.

## State

| address | contents | written by | cleared by |
|---|---|---|---|
| `0x0209A3E0` | 80 override entries, 640 bytes | `0x0026E880`, `0x0026E850`, `0x0026E130`, `0x0026E150` | `0x0026E960` at map bind |
| `0x0209A6C0` | forced-on model mask | `0x00379010` | `0x0026E640` |
| `0x0209A6C8` | forced-off model mask | `0x00379010` | `0x0026E640` |
| `0x0209A690` | the part's hidden model set | `0x0026E960` | `0x0026E640` |
| `0x0209A698`, `0x0209A6A0` | the part's shown and hidden sets of the frame | `0x003820C0` | `0x0026E640` |
| `0x0209A6FC` | 1: the part's sets take part in `0x0026E5F0` | `0x0026E1D0`, `0x0026E960`, `0x002628B0`, `0x00379070` | never cleared by the functions here |
| `0x0209A670` | the bound map; 0 before a map is bound | `0x0026E960` | `0x0026E1D0` |
| `0x0209A678`, `0x0209A680` | the two part descriptors | `0x0026E960` | `0x0026E640` |
| `0x0209A6D0`, `0x0209A6D8` | forced-on and forced-off map effect masks | `0x00378FB0` | `0x0026E640` |
| `0x0209A6A8` | the part's hidden effect set | `0x0026E960` | `0x0026E640` |
| `0x0209A6B0`, `0x0209A6B8` | the camera regions' shown and hidden effect sets | `0x003820C0` | `0x0026E640` |
| `0x0209A6E0` | the hidden effect set of the last step | `0x0026EB30` | replaced by `0x0026EB30` every step |
| `0x02EBF278` | 64 `f32` fade weights of the camera regions | `0x0022FF10` | `0x00382080`, every frame |

The two resets also write three words beside the model block, each 0 at load (the zero-filled tail of `.data`); no
instruction reads them at these addresses:

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x0209A700` | `u32` | 0 | cleared together with `0x0209A704` (below) by one qword store of 0 | `0x0026E1D0` (`0x0026E21A`, 8 bytes, covering `0x0209A700`-`0x0209A707`) | no instruction at this address |
| `0x0209A704` | `u32` | 0 | the word after `0x0209A700`: the map set-up clears it, the map teardown clears it, `0x00379930(x)` stores its argument, and the draw-list build reads it | `0x0026E1D0` (`0x0026E21A`, in the same qword store); `0x00378120`, 0 (`0x0037814C`); `0x00378230`, 0 (`0x00378253`); `0x00379930` (`0x00379930`, its first argument) | `0x002F5550` (`0x002F5585`) |
| `0x0209A70C` | `u64` | 0 | all bits set: `0xFFFFFFFFFFFFFFFF`, stored as one qword | `0x0026E640` (`0x0026E6CA`) | no instruction at this address |
| `0x0209A714` | `u64` | 0 | all bits set, stored as one qword; it ends at `0x0209A71B`, just before the 32 anchor words at `0x0209A71C` that the same reset fills with `0xFFFF` (`0x0026E6EE`) | `0x0026E640` (`0x0026E6D5`) | no instruction at this address |

The anchor-word reader `0x003A6FC0(n)` sign-extends `n` and does not bound it (`0x003A6FD0`-`0x003A6FDA`), so an `n` from -8
to -1 would read these two qwords; the draw-list build `0x002F5550` writes an anchor word only for an index from 0 to 31
(`0x002F653F`-`0x002F654B`).

None of these addresses is read or written by the save image functions referenced from them; the state
is rebuilt from the map and its script on every load.

## Modding notes

- A floor group number in a script is the polygon's bits 13-17; a wall group is the same field on a
  type-1 polygon or wall record; an mj group is bits 3-6. The `+0x20` and `+0x40` banks are offsets the
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
