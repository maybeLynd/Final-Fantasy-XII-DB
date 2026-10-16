---
title: "Doors, gates and map changes: the override table the setmapid verbs write, what its floor, wall and mj bits block, the show and hide model masks and when a new map clears them"
kind: "system"
category: "World, areas and travel"
addresses: "0209A3E0, 0026E880, 003792E0, 003795A0, 00379430, 00232020, 00230A40, 0022F8B0, 0026E300, 00379010, 0026E5F0, 0026E960, 003278D0"
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

The collision part of the loaded map is a `68`<sub>h</sub>-byte descriptor at `map + 40h`. `0026E500(0)` returns it
from `[0209A678]` once `0026E960` has bound a map. Its polygons are `20`<sub>h</sub>-byte records at `[part + 10h]`
and its wall records are `90`<sub>h</sub>-byte records at `[part + 18h]`. A polygon id below `4000`<sub>h</sub> names a polygon
and an id from `4000`<sub>h</sub> names a wall record (`0022F8B0`, `0022DE60`). The attribute word sits at `+C`<sub>h</sub> of
a polygon and at `+4` of a wall record. Its fields, with the functions that read each one:

| bits | field | written by a verb | read by |
|---|---|---|---|
| 0-2 | polygon type: 0 floor, 1 wall, 2 and 4 marker polygons, 3 camera region | none | `00230A40`, `0022D4B0`, `0022CC50`, `00231A90`, `002321D0`, `00233230` |
| 3-6 | mj group 0-15; selects override entry `40h + group` | none | `00232020`, `00230A40`, `00232090`, `00231F80`, `002321D0`, `00231A90` |
| 12 | copied into bit 2 of the body's flag word | `setmapidfloor` kind 9 | `003808A0` |
| 13-17 | floor group 0-31; the wall group on type-1 polygons and wall records | none | every override reader below |
| 18-22 | ground field | `setmapidfloorground` | `00231F80` |
| 23-27 | block bits for movement kinds 0, 5, 1, 2, 3 (bits 23, 24, 25, 26, 27) | `setmapidfloor`, `setmapidmj` | `00230A40`, `00232090`, `0022D4B0`, `0022CC50` |
| 26 | on type-1 polygons and wall records: skipped by the sphere sweep | none | `0022D7E0` |
| 30 | wall ignored by kind-4 queries | `setmapidwall` kind 6 | `0022D4B0`, `0022CC50` |
| 31 | wall switched off | `setmapidwall` kind 5 | `0022F8B0`, `0022DE60`, `0022D7E0`, `0022D4B0`, `0022CC50` |

### The override table

`0209A3E0` holds 80 entries of two 32-bit words, `mask` then `value`, 8 bytes each, from `0209A3E0` to
`0209A65F`. A set mask bit means that bit of the attribute word is replaced by the value bit. A clear
mask bit lets the authored bit through. The three banks follow from the writers' offsets (`003795A0`
adds `20`<sub>h</sub> to the entry, `00379430` adds `40`<sub>h</sub>) and from the three zeroing loops of `0026E960`
(`0209A3E0`-`0209A4DF`, `0209A4E0`-`0209A5DF`, `0209A5E0`-`0209A65F`):

| entries | addresses | bank | selected by |
|---|---|---|---|
| `00`<sub>h</sub>-`1F`<sub>h</sub> | 0209A3E0-0209A4DF | floors | attribute bits 13-17 of a floor polygon |
| `20`<sub>h</sub>-`3F`<sub>h</sub> | 0209A4E0-0209A5DF | walls | attribute bits 13-17 of a wall polygon or wall record, plus `20`<sub>h</sub> |
| `40`<sub>h</sub>-`4F`<sub>h</sub> | 0209A5E0-0209A65F | mj groups | attribute bits 3-6, plus `40`<sub>h</sub> |

### How a reader applies the overrides

`00232020(attr)` is the stand-alone form. `00230A40`, `00232090`, `00231F80`, `002321D0` and
`00231A90` inline the same arithmetic, and the five wall readers apply only the wall entry:

```c
// floors and mj groups: 00232020, 00230A40, 00232090, 00231F80, 002321D0, 00231A90
g   = (attr >> 13) & 0x1F;                              // floor entry
mj  = ((attr >> 3) & 0xF) + 0x40;                       // mj entry
eff = (attr & ~mask[g])  | (value[g]  & mask[g]);
eff = (eff  & ~mask[mj]) | (value[mj] & mask[mj]);      // applied second: the mj entry wins

// walls: 0022F8B0, 0022DE60, 0022D7E0, 0022D4B0, 0022CC50
w   = ((attr >> 13) & 0x1F) + 0x20;
eff = (attr & ~mask[w]) | (value[w] & mask[w]);
```

Because the mj entry is applied after the floor entry, an mj override of a bit beats a floor override of
the same bit on every polygon tagged with that mj group.

### The writers and the path reset

Four functions write the table, and each ends in a call to `003278D0`:

| function | arguments | effect |
|---|---|---|
| `0026E880` | entry, v, bit, width | `mask |= ((1 << width) - 1) << bit`, then those bits of `value` become `v << bit` |
| `0026E850` | entry, bit, width | clears those mask bits, so the authored bits show through again |
| `0026E130` | entry | `mask := 0` for one entry |
| `0026E150` | first, count | `mask := 0` for `count` consecutive entries |

`003278D0` walks the body registry (`00236850` is the count, `00236820(i)` returns the `F50`<sub>h</sub>-byte body
`i` at `[0208E688]`). For every body whose first byte has bit 4 set it calls `003839C0` and `003839F0` on
the body's `+200`<sub>h</sub> block: the two shorts at `+C`<sub>h</sub> and `+E`<sub>h</sub> become `FFFF`<sub>h</sub> and the `80`<sub>h</sub> bytes from
`+10`<sub>h</sub> become `FF`<sub>h</sub>. Nothing else is written, and no map model is touched by any of the four writers.

### The verbs

The script sources call these verbs `setmapidfloor`, `setmapidwall`, `setmapidmj` and so on. The names
and ids are those of the verb table page in Related. Handlers come from the family-0 verb table at
`01EED700`, 32 bytes per verb, where an instantaneous verb's handler is the first slot of the next
record: record `FF`<sub>h</sub> at `01EEF6E0` holds `00343E60`, the handler of verb `FE`<sub>h</sub>.

Operands are popped with `00267E10(ctx)`, which returns an integer operand as it is and truncates a
float operand, and pushed with `00267F90(ctx, n)`. The three-operand verbs push -1 and then pop four
times, dropping the first pop, so the pushed -1 is thrown away and the script's operands reach the
native as (group, kind, v): `00343E60` runs `or edx, -1; call 00267F90`, four `call 00267E10` and
`jmp 003792E0` with the last pop in `ecx`.

| id | name | handler | native call | script operands |
|---|---|---|---|---|
| `F6`<sub>h</sub> | resetmapidfloorall | `003416E0` | `003791D0(-1)` | none; -1 is pushed and popped |
| `F7`<sub>h</sub> | resetmapidfloor | `00341290` | `003791D0(g)` | g |
| `F8`<sub>h</sub> | resetmapidwallall | `00341E30` | `00379270(-1)` | none |
| `F9`<sub>h</sub> | resetmapidwall | `00341A90` | `00379270(g)` | g |
| `FA`<sub>h</sub> | resetmapidmjall | `003424D0` | `00379220(-1)` | none |
| `FB`<sub>h</sub> | resetmapidmj | `003421B0` | `00379220(g)` | g |
| `FC`<sub>h</sub> | setmapidfloorground | `003429B0` | `003791F0(g, v)` | g, v |
| `FD`<sub>h</sub> | setmapidmjground | `00343140` | `00379240(g, v)` | g, v |
| `FE`<sub>h</sub> | setmapidfloor | `00343E60` | `003792E0(g, kind, v)` | g, kind, v |
| `FF`<sub>h</sub> | setmapidwall | `00344A20` | `003795A0(g, kind, v)` | g, kind, v |
| `100`<sub>h</sub> | setmapidmj | `003458D0` | `00379430(g, kind, v)` | g, kind, v |
| `101`<sub>h</sub> | setmapidfloor_101 | `00343810` | `003792E0(g, kind, v)` | g, kind, v, x; x is popped and dropped |
| `102`<sub>h</sub> | setmapidwall_102 | `003444F0` | `003795A0(g, kind, v)` | g, kind, v, x |
| `103`<sub>h</sub> | setmapidmj_103 | `00345370` | `00379430(g, kind, v)` | g, kind, v, x |
| `107`<sub>h</sub> | resetmapidfloorground | `00342E00` | `003791F0(g, -1)` | g |
| `108`<sub>h</sub> | resetmapidmjground | `003434B0` | `00379240(g, -1)` | g |
| `109`<sub>h</sub> | resetmapidfloor_109 | `00344190` | `003792E0(g, kind, -1)` | g, kind; -1 is pushed twice |
| `10A`<sub>h</sub> | resetmapidwall_10a | `00344E30` | `003795A0(g, kind, -1)` | g, kind |
| `10B`<sub>h</sub> | resetmapidmj_10b | `00345EF0` | `00379430(g, kind, -1)` | g, kind |

The reset natives clear masks only. `003791D0(g)` calls `0026E130(g)`, or `0026E150(0, 20h)` when `g`
is negative. `00379270(g)` calls `0026E130(g + 20h)` or `0026E150(20h, 20h)` (`00379274`).
`00379220(g)` calls `0026E130(g + 40h)` or `0026E150(40h, 10h)` (`00379224`-`00379229`).

Verbs `104`<sub>h</sub> to `106`<sub>h</sub> (`setmapambient`, `setmapambient_105`, `resetmapambient`; handlers
`00346380`, `00346880`, `00346D20`) sit between these ids but write the four floats at `0209A390`
through `00379080`; they change lighting, not the map, and are outside this page.

### Which bit each kind writes

`003792E0(g, kind, v)` and `00379430(g, kind, v)` share one kind-to-bit map; `003795A0` has its own.
The value bit is the inverse of `v` for floors and mj groups (`sete` at `003792ED`) and equal to `v`
for walls (`setnz r10b` at `003795AB`):

| native | kind to bit | value bit when v is 0 or more | v below 0 |
|---|---|---|---|
| `003792E0` (floors), `00379430` (mj, entry + `40`<sub>h</sub>) | 0 to 23, 1 to 25, 2 to 26, 3 to 27, 7 to 24, 9 to 12; any other kind writes nothing | `v == 0`, so a set bit blocks | `0026E850(entry, bit, 1)`: the bit's mask is cleared |
| `003795A0` (walls, entry + `20`<sub>h</sub>) | 5 to 31, 6 to 30; any other kind writes nothing | `v != 0`, so a set bit switches the wall off | `0026E850(entry, bit, 1)` |

Read with the consumers below, `v = 1` opens in both banks: it clears a floor's block bit and sets a
wall's off bit. `v = 0` closes, and a negative `v` hands the bit back to the authored data.

`003791F0(g, v)` writes the ground field: `0026E880(g, v, 18, 5)` when `v` is 0 or more and
`0026E850(g, 18, 5)` when it is negative. `00379240` does the same on entry `g + 40h`.

### What the floor bits block

A body's movement kind is the byte at `+50`<sub>h</sub> of its navigation record, the record `003808A0`,
`002327D0` and `00380D30` work on. The readers of the block bits are:

- `00230A40(part, polygon, kind)` applies the overrides and returns 0 when `eff & 7` is not 0 (not a
  type-0 floor polygon). Otherwise it returns 1 when the kind's bit is clear: kind 0 tests bit 23, kind
  1 bit 25, kind 2 bit 26, kind 3 bit 27, kind 5 bit 24. Kind 4 and kinds above 5 always get 1.
- `00232090(part, polygon)` packs the same five bits into a kind bitfield (bit k set means kind k is
  blocked: bit 0 from 23, bit 1 from 25, bit 2 from 26, bit 3 from 27, bit 5 from 24) and returns 0
  when `eff & 7` is not 0.
- `002327D0`, the movement sweep called from `00380C40`, asks `00230A40` (`00232EB9`) about each
  neighbouring polygon the body is about to cross into. A 0 answer makes the sweep treat that edge as a
  wall (`0022F9B0`, `0022FB2C`), so the body slides along the boundary of a blocked polygon exactly as
  along a wall.
- `00233110`, called by `00380D30` and `00231400`, picks the polygon under a point from the cell's list
  and skips every polygon `00230A40` refuses (`002331C0`).
- `00380D30(record, position)` places a body: after finding its polygon it reads `00232090` into
  `+5E`<sub>h</sub> and, when the body's own kind bit is set, writes `FFFE`<sub>h</sub> into the polygon slot `+52`<sub>h</sub>. The body
  is then standing on ground that is closed to it.
- `00231A90` searches the body's cell for type-2 and type-4 marker polygons (stored at `+5C`<sub>h</sub> and
  `+54`<sub>h</sub>), using the overridden type bits.

The verb's kind numbers and the reader's kind numbers differ in one place: a script that writes
kind 7 sets bit 24, and bit 24 is what the reader tests for movement kind 5.

### What the wall bits do

Walls are tested by the collision callback `0022F8B0` (installed through `0022F830` by `00232490` and
`00231400`), the sphere sweep `0022D7E0`, and the ray casts `0022DE60`, `0022D4B0` and `0022CC50`.
Each applies the wall entry to the attribute word and then decides as follows.

- A set bit 31 removes the wall. `0022F8B0` calls the contact test `00381EB0` only while `eff` is below
  `80000000`<sub>h</sub> (and only when its record's `+24`<sub>h</sub> is non-zero; with it zero every wall is tested).
  `0022DE60` and `0022D7E0` skip type-1 polygons and wall records whose bit 31 is set.
- A set bit 30 makes a type-1 polygon or wall record invisible to kind-4 queries only. `0022D4B0` and
  `0022CC50` read the query kind from `+46`<sub>h</sub> of the query, keep the wall for every other kind and skip
  it for kind 4. Type-4 polygons are the mirror image: they are hit only by kind-4 queries.
- The movement sweep sets `+46`<sub>h</sub> to 2, or to 3 when flag bit 0 of the record is set (`002327D0`), so
  a `setmapidwall(g, 6, v)` never changes where a walking body stops. None of the five wall readers
  above issues a kind-4 query itself; the kind-4 caller lies outside them.
- Bit 26 on a type-1 polygon or wall record makes `0022D7E0` skip it unless the query's `+3C`<sub>h</sub> is
  non-zero. No verb reaches bit 26 of a wall entry, so this is authored data only.

### The ground field and bit 12

`003808A0(record, part)` runs after a body moved (`00380C40`) or was placed (`00380D30`). From the
effective attribute of the body's polygon it stores the floor group into `+56`<sub>h</sub>, the mj group into
`+58`<sub>h</sub>, bit 12 into flag bit 2 of `+60`<sub>h</sub>, and the five-bit ground field (`00231F80`, bits 18-22 after
overrides) into `+5A`<sub>h</sub>. `00231F80` has that one caller (`0038090E`).

The record is the placement at `+30`<sub>h</sub> of an actor's movement body (`[actor + C0h] + 138h`), so the
body holds the floor group at `+86`<sub>h</sub> and the ground field at `+8A`<sub>h</sub>. The script reads and writes
them through three helpers that return -1 when the actor has no body:

| Verb | Handler | Helper | Effect |
|---|---|---|---|
| `2EA`<sub>h</sub> `getmapid()` | `00348100` | `002E9890` | pushes the floor group of the running actor, negatives as 0 |
| `48B`<sub>h</sub> `getmapid_48b(actor)` | `00347240` | `002E9890` | the same for the actor `00263770` finds |
| `2FF`<sub>h</sub> `getmapgroundtype()` | `0034E0E0` | `002E9830` | pushes the ground field, negatives as 0 |
| `48C`<sub>h</sub> `getmapgroundtype_48c(actor)` | `003476B0` | `002E9830` | the same for a given actor |
| `4E2`<sub>h</sub> `setmapgroundtype(v)` | `0034E510` | `002EBC70` | writes `v` to the running actor's `+8A`<sub>h</sub> |
| `4E3`<sub>h</sub> `setmapgroundtype_4e3(actor, v)` | `00347D20` | `002EBC70` | the same for a given actor |

The ground field also picks an effect: the presentation command `18`<sub>h</sub> (`00520C80`) calls
`003B0C50`, which plays effect 100 for ground 0 to 3, 7, 9, 13 and 14, 101 for 4, 102 for 5,
103 for 11, 12 and 15, 148 for 16 and 18, and nothing for the others (`003B02A0`). A
`setmapgroundtype` write lasts until the body's next move or placement rewrites `+8A`<sub>h</sub>.

### Asking whether a bit is overridden

`0026E300(entry, kind)`, reached through the thunk `0032A780`, maps the kind through the table
`00915760` = {23, 25, 26, 27, -1, 24} and returns -1 for kind 4, 0 when the mask bit is clear
(authored data applies), 1 when the bit is overridden to 0 and 2 when it is overridden to 1.

Its two callers belong to the long-range route graph at `[02AEDFB0]`: the edge-cost function `00383850`
and the graph walk `0033D3E0`. Both read 8-byte edge records whose `+4` is -1 when the edge has no
override entry, whose `+5` is an override entry and whose `+6` is the authored kind bitmask. The edge is:

- usable when the answer is 1 (the gate was opened with `v = 1`, even where the authored mask forbade
  the kind);
- unusable when the answer is 2 (`00383850` returns the cost `7FFFFFFF`<sub>h</sub>);
- decided by the authored kind bitmask when the answer is 0 or the edge has no entry.

So a `setmapidfloor(g, kind, 0)` closes both the polygons of group `g` and every route-graph edge
tagged with entry `g` for that kind.

### Showing and hiding map models

`00379010(id, mode)` edits two 64-bit masks, the forced-on set `0209A6C0` and the forced-off set
`0209A6C8`, at bit `id & 3Fh`:

| mode | 0209A6C0 | 0209A6C8 | verb and handler |
|---|---|---|---|
| 1 | set | clear | `showmapmodel` `10C`<sub>h</sub> `00347FD0`; `showmapmodel_113` `113`<sub>h</sub> `00347C90` takes the mode as its second operand |
| 0 | clear | set | `hidemapmodel` `10D`<sub>h</sub> `003482F0` |
| 2 | clear | clear | `defaultmapmodel` `270`<sub>h</sub> `00348680` |

Two readers turn the masks into the hidden set of the frame:

- `0026E5D0()` returns `0209A6C8 & ~0209A6C0`: only what a script forced off.
- `0026E5F0()` returns `~0209A6C0 & (0209A6C8 | base)`, where `base` is `0209A690` when `0209A6FC`
  is 0 and `(0209A690 | 0209A6A0) & ~0209A698` otherwise. `0209A690` is the collision part's own
  hidden set `[[part] + 30h]`, copied once at bind (`0026E9DC`). `0209A6A0` and `0209A698` are copied
  every frame by `003820C0` (`00382810`, `00382817`) from `[part + 50h]` and `[part + 48h]`.

`0209A6FC` is set to 1 by `0026E1D0`, by `0026E960` and by the zone's manager-0 start-up `002628B0`
(`00262B53`); the verb `setmapmodelstatus` (`3EE`<sub>h</sub>, `003526D0`) writes its operand into it through
`00379070`. A model with its bit in the hidden set is not drawn, while its collision polygons are
untouched: hiding a gate model and opening its floor group are two separate writes.

Four consumers read the hidden set:

- the draw-list build `002F5550` (`002F5611`, `002F562F`) tests a model's 64-bit group mask at `+20`<sub>h</sub>
  of its `30`<sub>h</sub>-byte record against it;
- the draw pass `002F4520` (`002F4B99`) consults it for models with a group byte at `+1C`<sub>h</sub>;
- the background-animation update `004668C0` (`004668E4`) skips entries whose group bit is hidden;
- `003ECCA0` (`003ECD84`) does the same for its entries.

### Camera regions

The part's shown and hidden sets of the frame come from type-3 polygons around the camera. Each frame
the camera update `003820C0` calls `00233230(part, 02AEDEE0)` (`003827FB`) with the collision part
(`0026E500(0)`) and the camera position, the fourth row of the camera matrix copy at `02AEDEB0`:

1. `00382080` zeroes the 64 fade weights at `02EBF278`, and the part's sets `+48`<sub>h</sub>, `+50`<sub>h</sub>,
   `+58`<sub>h</sub> and `+60`<sub>h</sub> are zeroed;
2. `00233050` finds the camera's cell in the part's grid, and the polygons listed for the cell are
   walked;
3. a type-3 polygon for which `002324F0` returns a negative value at the camera position applies its
   attribute word: with bit 3 set, the value `v` in bits 16-23 sets bit `v` of `+48`<sub>h</sub> (shown models)
   when below 64, else bit `v - 64` of `+58`<sub>h</sub>; with bit 4 set, the value in bits 24-31 does the same
   with `+50`<sub>h</sub> (hidden models) and `+60`<sub>h</sub>.

For a model value below 64 `0022FF10(part, polygon, camera, v)` also writes the fade weight
`02EBF278[v]`: the camera's barycentric weights in the polygon (`0022F050`) applied to the byte `+0F`<sub>h</sub>
of its three vertices, divided by 255. `003820C0` then copies `+48`<sub>h</sub>, `+50`<sub>h</sub>, `+58`<sub>h</sub> and `+60`<sub>h</sub> to
`0209A698`, `0209A6A0`, `0209A6B0` and `0209A6B8` (`00382810` to `00382825`).

The draw pass multiplies the alpha of a model whose group byte `+1C`<sub>h</sub> is 1 to 254 and whose bit is
not in the hidden set by `02EBF278[group]` (`002F4FDF`), so a region painted with vertex alpha fades
its models in across the polygon. `003ECCA0` and `002F1F40` read the weights too.

### Map effects

The values 64 and above of a camera region name map effect channels, and the effect channels have
script masks of their own. `00378FB0(channel, mode)` edits the forced-on set `0209A6D0` and the
forced-off set `0209A6D8` at bit `channel & 3Fh`, with the same modes as `00379010`:

| mode | 0209A6D0 | 0209A6D8 | verb and handler |
|---|---|---|---|
| 1 | set | clear | `showmapeffect` `4F8`<sub>h</sub> `00345AC0`; `showmapeffect_4fa` `4FA`<sub>h</sub> `003455B0` takes the mode as its second operand |
| 0 | clear | set | `hidemapeffect` `4F9`<sub>h</sub> `003460A0` |
| 2 | clear | clear | `defaultmapeffect` `4FB`<sub>h</sub> `00346600` |

Each world step `0026EB30` (from `0036F510`) computes the hidden effect set
`((0209A6A8 | 0209A6B8) & ~0209A6B0 | 0209A6D8) & ~0209A6D0`, where `0209A6A8` is the part's own
set `[[part] + 38h]` copied at bind (`0026E9EA`), or 0 while no map is bound. For each of the 64
channels whose bit differs from the previous frame's set `0209A6E0` it stops the channel
(`0026FE50`) when the bit is set and starts it for the current weather slot `0209A6E8`
(`0026FEB0`, which runs `0026FAD0(channel, slot, 0)`) when it is clear.

### A new map clears everything

The field tick's request handler `003775D0` calls `00378120` (`003776DD`) when bit 3 of `02ADD0F0` is
set, and `00378120` calls `0026E760` (`00378193`) with the new map data:

1. `0026E640` zeroes `0209A6C0`, `0209A6C8`, `0209A690` to `0209A6B8` and the rest of the model block,
   and sets the 32 shorts at `0209A71C` to `FFFF`<sub>h</sub>.
2. `0026E960(map)` stores the map in `0209A670`, the two part descriptors `map + 40h` and
   `map + A8h` in `0209A678` and `0209A680`, copies `[[part] + 30h]` into `0209A690`, sets `0209A6FC`
   to 1 and zeroes all 80 masks, calling `003278D0` after each one.

`0209A3E0` and `0209A3E4` are referenced by the four writers, by `0026E960` and by the twelve readers
named on this page and by nothing else (38 and 23 references). `0209A6C0` and `0209A6C8` are referenced
only by `00379010`, `0026E640`, `0026E5D0` and `0026E5F0`. No save-image copy exists among those
references: the table and the masks are state of the loaded map only.

## Layouts

`MapIdOverride` (`8`<sub>h</sub> bytes, offsets from the start of the 0209A3E0):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u32` | mask | bits replaced; set by `0026E880`, cleared by `0026E850`, `0026E130`, `0026E150` and `0026E960` |
| `04`<sub>h</sub> | `u32` | value | replacement bits; written by `0026E880` only |

Eighty entries: floors `00`<sub>h</sub>-`1F`<sub>h</sub>, walls `20`<sub>h</sub>-`3F`<sub>h</sub>, mj groups `40`<sub>h</sub>-`4F`<sub>h</sub>.

`CollisionPolygon` (`20`<sub>h</sub> bytes, offsets from the start of the polygon):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `f32[3]` | normal | plane normal, dotted with a vertex in `0022DE60` and `0022D7E0` |
| `0C`<sub>h</sub> | `u32` | attr | the attribute word (field table in How it works) |
| `10`<sub>h</sub> | `i16[3]` | vertex | indices into the `10`<sub>h</sub>-byte vertex array at [part + 8]; `00231A90` reads the vertex colour at +`C`<sub>h</sub> |
| `16`<sub>h</sub> | `i16[3]` | neighbour | polygon id across each edge, -1 for none (`0022F9B0`) |
| `1C`<sub>h</sub> | `u32` | tail | not read by the functions on this page |

`RouteEdge` (`8`<sub>h</sub> bytes, offsets from the start of the edge):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u16` | nodeA | node index; node positions are 8-byte pairs at [graph + `C`<sub>h</sub>] (`00383850`) |
| `02`<sub>h</sub> | `u16` | nodeB | node index |
| `04`<sub>h</sub> | `i8` | hasEntry | -1 when the edge has no override entry (`00383850`) |
| `05`<sub>h</sub> | `u8` | entry | override table entry passed to `0026E300` (`00383850`, `0033D3E0`) |
| `06`<sub>h</sub> | `u8` | kinds | authored kind bitmask, bit k means kind k may use the edge |
| `07`<sub>h</sub> | `u8` | pad | not read by `00383850` or `0033D3E0` |

The edge table is `[graph + 14h]` and the node-pair adjacency table `[graph + 1Ch]`, both resolved
through `0020E600`; `graph + Ah` is the node count.

## Operations

A script opens a gate for walking bodies and shows the open model:

1. `setmapidfloor(g, 0, 1)`: `00343E60` pops the operands and calls `003792E0(g, 0, 1)`.
2. `003792E0` calls `0026E880(g, 0, 23, 1)`: mask bit 23 of entry `g` is set and value bit 23 is 0.
3. `0026E880` calls `003278D0`, which clears the cached navigation block of every registered body
   with bit 4 of its first byte set.
4. `showmapmodel(id)`: `00347FD0` calls `00379010(id, 1)`, setting the forced-on bit and clearing the
   forced-off bit.
5. On the next frame `0026E5F0()` no longer contains the model's bit and `002F5550` draws it; a kind-0
   body that crosses into a polygon of group `g` gets 1 from `00230A40` and walks through.

A body steps towards a blocked polygon:

1. `00380C40` calls `002327D0` with the record, its polygon and the move vector.
2. For each edge crossed, `002327D0` reads the neighbour polygon and calls `00230A40(part, polygon,
   kind)`.
3. `00230A40` builds `eff` from the floor and mj entries, finds `eff & 7 == 0` and returns 0 because the
   kind's bit is set.
4. `002327D0` treats the edge as a wall and `0022F9B0` slides the body along it.
5. `003808A0` then records the floor group, mj group, ground field and bit 12 of the polygon the body
   stays on.

## State

| address | contents | written by | cleared by |
|---|---|---|---|
| `0209A3E0` | 80 override entries, 640 bytes | `0026E880`, `0026E850`, `0026E130`, `0026E150` | `0026E960` at map bind |
| `0209A6C0` | forced-on model mask | `00379010` | `0026E640` |
| `0209A6C8` | forced-off model mask | `00379010` | `0026E640` |
| `0209A690` | the part's hidden model set | `0026E960` | `0026E640` |
| `0209A698`, `0209A6A0` | the part's shown and hidden sets of the frame | `003820C0` | `0026E640` |
| `0209A6FC` | 1: the part's sets take part in `0026E5F0` | `0026E1D0`, `0026E960`, `002628B0`, `00379070` | never cleared by the functions here |
| `0209A670` | the bound map; 0 before a map is bound | `0026E960` | `0026E1D0` |
| `0209A678`, `0209A680` | the two part descriptors | `0026E960` | `0026E640` |
| `0209A6D0`, `0209A6D8` | forced-on and forced-off map effect masks | `00378FB0` | `0026E640` |
| `0209A6A8` | the part's hidden effect set | `0026E960` | `0026E640` |
| `0209A6B0`, `0209A6B8` | the camera regions' shown and hidden effect sets | `003820C0` | `0026E640` |
| `0209A6E0` | the hidden effect set of the last step | `0026EB30` | replaced by `0026EB30` every step |
| `02EBF278` | 64 `f32` fade weights of the camera regions | `0022FF10` | `00382080`, every frame |

None of these addresses is read or written by the save image functions referenced from them; the state
is rebuilt from the map and its script on every load.

## Modding notes

- A floor group number in a script is the polygon's bits 13-17; a wall group is the same field on a
  type-1 polygon or wall record; an mj group is bits 3-6. The `+20`<sub>h</sub> and `+40`<sub>h</sub> banks are offsets the
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
- Everything here is cleared when `0026E760` binds a new map. A persistent gate must be re-applied by
  the area script from its own saved variables.

## Related

- [Script verb dispatch and parameter encoding](../Scripts-And-Script-Commands/verb-dispatch.md)
- [Zone changes: mapjump and the other jump verbs, the loading flags, the moment the new zone is ready and what names a map](zone-changes-and-mapjump.md)
- [Area flags: the navimapdata.bin record for every area, the town flag, the KO, Stone and X-Zone override and the other bits](area-flags-navimapdata.md)
- [How a unit finds its way across the navigation mesh](../Movement-And-Pathfinding/navigation-mesh-and-pathfinding.md)
- [The map ctrl pack](mpk-map-pack.md)
