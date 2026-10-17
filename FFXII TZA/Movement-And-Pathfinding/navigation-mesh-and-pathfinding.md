---
title: "Navigation mesh and pathfinding: the mesh in the map pack, finding a region, the route search and its waypoints, the doors a script opens, and the obstacle grid"
kind: "system"
category: "Movement and pathfinding"
addresses: "00384160, 00391A30, 00391D90, 00391710, 00468A70, 00468580, 00336E40, 00336210, 00336AE0, 00383840, 00383C80, 00383A20, 00383740, 00383F10, 00384130, 00382D10, 00383A30, 00382FF0, 00383620, 00383850, 0026E300, 00382EA0, 003842E0, 003792E0, 003278D0, 003839C0, 003839F0, 00383670, 00383C90, 00325BB0, 0030A130, 00392740, 00392200, 003912E0, 00391410, 00336CE0"
---

## What the player sees

A monster chasing you around a pillar, a party member catching up through a doorway, an enemy
giving up on a target it cannot reach: all of it runs on a flat mesh of regions the area carries,
joined by portals. A unit searches for a route once, keeps it while it still leads to the goal,
remembers the last two goals it could not reach so it does not search for them again, and walks
from portal to portal, aiming each waypoint afresh as it goes and cutting corners it no longer
needs.

Some portals are doors a zone script opens and closes, per kind of mover, so a gate can be closed
to monsters and open to the party. Height plays no part in any of it: the mesh is flat, and a
unit standing on a ledge above its goal is as close as one beside it.

## How it works

### The dataset

The mesh is slot four of the area's map pack ([map pack](../World-Areas-And-Travel/mpk-map-pack.md)).
Area setup hands the copied section to `00384160` (`003781A6`, `003782C9`), which stores its
address at `02AEDFB0` and rebases the offsets in place: the six header offsets `+0x0C` to `+0x20`,
the trailer offset `+0x28`, and the grid's own two at `+8` and `+0xC`. `00383840` returns the
pointer, `00383C80` whether it is set, `00383A20` clears it, and `00383740` returns the grid's
rectangle as four floats.

Struct NavDataset base=section:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | 1 |  |
| `+0x04` | `u16` | vertexCount | +`0x06` u16 triangleCount (the whole-mesh test's bound) |
| `+0x08` | `u16` | portalCount | +`0x0A` u16 regionCount, at most 128 (the search's arrays) |
| `+0x0C` | `off` | vertices | 8 B each: f32 x, f32 z |
| `+0x10` | `off` | triangles | 8 B each: u16 vertex[3], u16 region |
| `+0x14` | `off` | portals | 8 B each: u16 vertexA, u16 vertexB, u8 gated (+4), u8 mapId (+5), u8 classMask (+6) |
| `+0x18` | `off` | regions | `0x22` B each: +2 u16 triangleCount, +`0x14` u16 triangleIndex[] |
| `+0x1C` | `off` | adjacency | regionCount x regionCount u16: the portal index from i to j, 0 = none |
| `+0x20` | `off` | grid | u8 cellW, u8 cellH, u8 cols, u8 rows, i16 originX, i16 originZ, |
| `+0x08` | `off` | cellTable | (u16 per cell), +`0xC` off listPool |
| `+0x24` | `u32` | trailer record count (at most 32 used) |  |
| `+0x28` | `off` | trailer records | `0x20` B each: i16 kind, f32 x +4, f32 z +8, f32 radius +`0xC`, f32 radius2 +`0x10`, f32 +`0x14` (kind 1; read by the segment query only) |

Portal index 0 means no portal, so the adjacency entries are 1-based and record 0 is padding.
Across the 461 shipped sections every triangle names a region that lists it back, the adjacency
matrix is symmetric with an empty diagonal, and the largest region count is exactly 128.
Everything is XZ: the two entry points that take world positions (`00383620`, `00384130`) drop y.

### Which region a point is in

`00383F10(xz)` returns `0xFF` when either coordinate is NaN (`_fdclass` on the float) or the point
lies outside the grid's rectangle; both edges of the rectangle are admitted (`<=` on both upper bounds, a `ja` against `origin +
count * size`). The cell `(z - originZ) / cellH * cols + (x - originX) / cellW` (signed truncating
divides) indexes the cell table with no bound check; `0xFFFF` is an empty cell, anything else an
offset into the list pool, where a `0xFF`-terminated list of region ids waits.

Each listed region's
triangles are tried in turn with `00382D10`, and the first region with a containing triangle wins.

`00382D10(triangle, xz)` walks the three edges through the index table `{0, 1, 2, 0}` at
`00D112B0`, takes the cross product of each edge with the vector from the edge's start to the
point, keeps the first non-zero cross as the reference sign, and answers 0 as soon as a later
cross has the opposite sign. A zero cross is tolerated, so a point on a shared edge belongs to
whichever region the cell lists first. `00383A30(xz, region)` asks the narrower question without
the grid: it scans every triangle of the mesh for ones of that region and runs the same test;
region `0xFF` is never inside.

A point exactly on the upper x edge takes column `cols`, which is the next row's first cell, and on
the upper z edge reads past the table; a cell size of 0 divides by zero. Nothing checks either.

### The path record

Each battle unit carries one at `+0x200` (`0x490` bytes):

Struct NavPath base=unit+`0x200`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `i32` | region the mover was last placed in (written by the same-region exit and the full search) |  |
| `+0x04` | `i32` | start region of the route held, 0xFF = none |  |
| `+0x08` | `i32` | goal region of the route held, 0xFF = none |  |
| `+0x0C` | `u8[2]` | the last (start, goal) pair that had no route |  |
| `+0x0E` | `u8[2]` | the one before that |  |
| `+0x10` | `u8[128]` | next[region]: the region to enter after this one; 0xFF ends the chain |  |
| `+0x90` | `f32[128][2]` | waypoint[region]: the x, z to walk to while in this region |  |

`003839F0` fills `next[]` with `0xFF`; `003839C0` fills the two no-route pairs with `0xFFFF`.

### The search

`00382FF0(startXZ, goalXZ, path, moverClass, radius)`, reached only through `00383620`, which
repacks two world positions:

1. both points are located; a start off the mesh returns -2, a goal off the mesh -3;
2. same region: `+0` = start, the region's waypoint is the goal itself, its `next` is `0xFF`; return 0;
3. known dead end: when `(start, goal)` equals either remembered pair, return -1 without searching;
4. route still good: follow `next[]` from the start region, stopping at `0xFF`, a self-loop or an
   id past the region count (a longer cycle is not caught; the search's own writes, a predecessor
   tree, never make one); when the chain reaches the goal region only the goal's waypoint is
   refreshed and `+0` is left alone; return 0;
5. otherwise Dijkstra over regions in the plain quadratic form: integer distances start at
   `0x7FFFFFFF`, the start region at 0 with the start point as its entry point;
6. each round settles the current region, stops if it is the goal, and relaxes every unsettled
   region through the cost function below; a strict improvement records the predecessor, the new
   entry point (the closest point on the portal) and the distance walked to it. The next current
   region is the unsettled one with the least distance, ties to the lowest index; the search ends
   when none is reachable;
7. the waypoints are laid walking back from the last region settled, carrying a target that starts
   as the goal. For each step from `pred` to `cur` with the portal's ends `A` and `B`: `c` is the
   point of `AB` closest to the target at distance `d1` (`00382EA0`), `e` the entry point recorded on
   the portal, reached after `d2`; the waypoint is `c + (e - c) * d1 / (d1 + d2)`, the midpoint when
   both are 0;
8. then the clearance rule: a portal shorter than `2 * radius` gives its midpoint, and a waypoint
   within `radius` of an end is pushed to `radius` from that end toward the other (`003842E0`).
   `waypoint[pred]` = the point, `next[pred]` = `cur`, and the point becomes the next target;
9. `+0` = start and `waypoint[goal]` = the goal. When the last region settled was the goal, `next[goal]` = `0xFF` and
   0 is returned; otherwise the pair is pushed onto the two-deep memory, the held route marked empty,
   and -1 returned.

An unreachable goal costs one full search, then nothing until the pair changes or the memory is
wiped. A unit chasing a target that moves about inside one region never searches twice.

### What a portal costs, and who may cross it

`00383850(from, to, goal, entryPoint, goalPoint, outPoint, moverClass, outDistance)`: an adjacency
entry of 0 costs `0x7FFFFFFF`. Otherwise the portal is tested for the mover class:

- an ungated portal (byte `+4` = `0xFF`), or one whose map id `0026E300` answers 0 for, is open when
  bit `moverClass` of its class mask `+6` is set;
- a gated portal asks `0026E300(mapId, moverClass)` (class in `edx`, as the caller left it): the class indexes the six-entry table at
  `00915760` (`{23, 25, 26, 27, -1, 24}`) for a bit; a negative entry returns -1 (closed); with the
  override table `0209A3E0` (two dwords per map id) holding that bit in its first dword the answer is
  1 (open) or, with the bit also in the second dword, 2 (closed); otherwise 0 falls back to the
  authored mask.

An open portal costs `trunc(100 * (d + g))`, where `d` is the distance from the entry point to the
portal segment (`00382EA0`, which also returns the closest point) and `g` is the distance from that
closest point on to the goal when `to` is the goal region, else 0; `outDistance` receives `d`
alone, before the goal leg is added. Distances are centimetre-grained integers measured portal to
portal; only the last hop sees the goal, and the recorded entry distance never includes it.

In the shipped data 51,248 portals are ungated and 926 gated under 30 map ids; the class masks are
`0x2F` (every class, 32,467 portals), `0x08` (class 3 only, 19,374), `0x00` (324), `0x0C` (8) and
`0x2B` (1): a walkable core and a wider skirt only class-3 movers may enter.

### The two geometry leaves

`00382EA0(A, B, P, out)` is the distance from `P` to the segment `AB` in XZ: the far end when `P`
projects beyond it, the near end when it projects before it, else the foot of the perpendicular,
with the distance `|cross| / |AB|`; `out`, when given, receives the closest point. `003842E0(A, B,
out, r)`: `A` when `A` equals `B`; the midpoint when `AB` is shorter than `2r`; otherwise `A + r *
(sin a, cos a)` with `a = atan2(dx, dz)`, the point `r` from `A` toward `B`. Its only two callers are
the clearance steps of the search and the follower.

### The doors a script opens

The mover class is the unit's byte `+0x1F4` ([battle unit fields](../Characters-And-Objects/battle-unit-fields.md)).

The script verb `setmapidfloor(mapId, kind, on)` ends in `003792E0(mapId, kind, on)` (`0034385C`,
`00343EB7`, `003441F2`), which switches on `kind` through six real arms, 0 → bit 23, 1 → 25, 2 → 26,
3 → 27, 7 → 24, 9 → 12, the same bits as the class table: `on` non-zero stores the override with the
bit clear (open, `0026E880(mapId, on == 0, bit)`), `on` = 0 stores it set (closed), and a negative
`on` removes the override (`0026E850(mapId, bit, 1)`).

The shipped scripts make 106,618 such calls: 84,066 with a literal kind (2: 28,510; 3: 26,951; 0:
8,706; 1: 8,699; 7: 7,223; 9: 2,091; 4: 1,886) and 22,552 with a variable; kind 4 reaches the bare
return and does nothing.

Every override change ends in `003278D0` (seven sites in the setters), which, for each live
battle-unit slot (byte `+0` bit 4; the slot count re-read every iteration), wipes the no-route
memory and the `next[]` chain of the unit's path record. Opening or closing a door invalidates
every unit's cached route and every remembered dead end at once.

### One step of following the route

`00383670(position, _, outPoint, path, radius)` starts from the region the mover was last placed in
and advances along `next[]` while the mover's point is already inside the next region
(`00383A30`), so a corner cut skips the waypoint no longer needed.

`00383C90(path, region, position, radius)` then re-aims the current region's waypoint: on the portal to the next region it
takes the closest point to the mover (`d1`) and the closest point to the following waypoint (`d2`),
divides them as the search does, and applies the same clearance rule. The region is stored back,
and the output is that waypoint with the mover's own y. In the goal region nothing is re-aimed and
the waypoint is the goal.

The caller is the unit's navigation step `00325BB0(unit)` ([battle locomotion](battle-locomotion.md)),
run from four combat sites (`002FDBE9`, `002FDD69`, `00304D5B`, `00308341`):

1. when `00325D90()` is 0 it runs `0033C9B0` on the locomotion block `+0x80` and returns true;
2. it clears unit flag bit 18 and searches, `00383620(unit + 0xD0, unit + 0x100, unit + 0x200,
   class, r)`, from the start point at `+0xD0` to the goal at `+0x100` into the path record at
   `+0x200`, with the class byte `+0x1F4` and `r = 1.414 * 0030A130(unit)`: the larger of the
   actor's two collision radii (`00265090`) times the `f32` at `00D10818`, `0x3FB4FDF4` =
   1.4140000343, a decimal literal 0.015 percent below root two;
3. a non-zero search result checks the handler pointer at `+0x698` against the control-flow guard
   (`0016D6A0`), calls nothing, and returns false;
4. otherwise `00383670(unit + 0xE0, unit + 0x100, unit + 0xF0, unit + 0x200, r)` reads the mover
   position from `+0xE0` and writes the next waypoint to `+0xF0`; the step flag word `+0x1F0`
   takes bit 0 and bit 1 from the order record's (`[+0x708]`) word `+4` (`0x200`, `0x100`), bit 3
   from unit flag bit 23, and bit 4 when the action id `+0x714` is below `0x21F` and not `0x96`;
5. the solver `00336CE0(block, block)` runs; bit 10 of the flag word zeroes `+0x158` and runs
   `00313500`; bit 7 zeroes `+0x158`, clears itself and publishes the facing
   (`003003F0(unit, unit + 0x140, [unit + 0x160], 0, 0)`).

### The obstacle grid

Beside the mesh the area keeps a coarse grid, built once per area (`003924B0`, in one block named
`MapGrid` from `00384580`), with `cols` at
`02AEE060`, `rows` at `02AEE064`, origin floats at `02AEE070`/`02AEE078`, the cell size at
`02AEE090`, a record of `02AEE0B8` = `0x24` bytes per cell at `[02AEE0A0]`, an occupancy byte per
cell at `[02AEE0A8]` and a mask scratch at `[02AEE0B0]`. Each record is a bitset of 288 obstacle
ids.

`00392740` refills it every field frame (`00234849` in `00234590`): it zeroes the count `02AEE0BC`,
every record, every occupancy byte and the 128-slot actor list at `02AEE0C0`, then assigns ids:

| Ids | Obstacles | Position and radius |
|---|---|---|
| 0-127 | the actors of the actor manager's three slot groups (`00263FF0`, `00263C50(g, 3)`, `00263B50(g, 3)`, `00358940`), while the count is below 128; each is stored at `list[id]` | `002646C0` position; the larger of `00265090`'s two radii |
| 128-159 | the dataset's trailer records, kinds 0 and 1 only (other kinds consume an id and mark nothing; the registry base 160 is fixed) | floats `+4`, `+8`; `+0xC`, or the larger of `+0xC` and `+0x10` for kind 1 |
| 160-287 | a registry's active entries (`0032A6B0` count, `0032A6C0` active, `0032A6E0` position and radii), at most 128 | the entry's position; the larger of its two radii |

`00392200(id, x, z, r)` takes the cells under the square `[x - r, x + r] x [z - r, z + r]`, clamped to
the grid, tests each cell's rectangle against the circle (`004690B0`), and for a hit sets bit
`id & 7` of byte `id >> 3` in the cell's record and increments the cell's occupancy byte (a `u8`,
which wraps at 256). The id space is exactly the record: 128 + 32 + 128 = 288 = 0x24 × 8. The
registry count is read twice, and only a count that changed between the reads could reach id 288,
which would land in the next cell's record.

`003912E0(x0, z0, x1, z1)` clears the mask scratch and ORs into it the records of every occupied
cell in the index rectangle, each index clamped piecewise, `i < 0 ? 0 : min(i, count - 1)`.

`00391410(p1, p2, r)`, the segment query, returns 0 at once when no dataset is loaded (`00383840`
null). Otherwise it builds the rectangle from the two points widened by `r`, flattens both points
to y = 0, computes `003A1920(p1, p2)` and discards the result, then walks mask bits 128 to 287
(from byte `+0x10`).

Bits 128-159 test the segment against the trailer record of that index as a box (kind 0,
`00468D50`) or a circle (kind 1, `00468E50`, handed the five dwords `+4` to `+0x14`), bits 160-287 against the registry entry's shape (`00468E50`); the first hit
returns 1, else 0. Actor ids 0-127 are never tested here; `00391710` is the query that walks the
listed actors.

### The actor queries

Three queries list the actors (ids 0-127) whose shapes meet a query shape. Each ORs into the mask
scratch the records of the occupied cells under the query's bounding square (clamped to the grid),
tests every listed actor (count `02AEE0BC`, list `02AEE0C0`) whose bit is set, and copies the
handles that pass to its output, returning their count. Every shape is flat: the queries zero or
ignore y.

| Query | Query shape | Test per actor |
|---|---|---|
| `00391A30(circle, out, ellipse)`, from `00391D10` | centre, radius `+0x10` | without `ellipse`: the actor's circle (`002FB340`: position, larger radius) overlaps, `00468D10`; with it: the actor's ellipse (`002FB500`: position, both radii, facing) against the circle, `00469060` |
| `00391D90(segment, out, ellipse)`, from `003920F0` | ends `+0x00` and `+0x10`, half-width `+0x20` | without `ellipse`: the actor's centre lies between the ends within radius plus half-width of the line, or within that of the far end; with it: `00468F90` |
| `00391710(sector, out)`, from `003919B0` | centre, radius `+0x10`, start angle `+0x20`, sweep `+0x24` | the actor's circle against the sector, `00468A70` |

`00391D10` and `003920F0` pass bit 4 of their flags as `ellipse` and hand the list on to
`003911D0`. The segment test without `ellipse` has no cap at the start: an actor just behind the
first end is listed only when it is also near the far end.

### The shape tests

- `00468D10(a, b)`: two circles overlap when the squared centre distance is strictly below `(ra +
  rb)^2`.
- `00468580(ellipse, p)`: the ellipse's radius toward `p`. The offset is turned into the ellipse's
  frame by its angle `+0x18` (the sine table `01F004E0`, `0x8000` steps a turn) and divided by the semi-axes
  `+0x10` and `+0x14`, giving `(u, v)`; the radius is `|(a u, b v)| / |(u, v)|`, or `a` when `|(u,
  v)|` is at most `1e-6`.
- `00469060(ellipse, circle)`: overlap when the squared distance is at most `(radius toward the
  circle + r)^2`.
- `00468F90(segment, ellipse)`: `004691A0` takes the segment's closest point to the ellipse's centre
  (an end when the projection falls outside); overlap when the distance is below the ellipse's
  radius toward that point plus the half-width.
- `00469410(A, B, w, circle)`: the segment from `A` to `B` widened by `w` meets the circle when the
  closest point (the foot of the perpendicular, `B` past the end, `A` before the start) is closer
  than `w + r`; `00468F70` calls it on a record holding `A`, `B` and `w`.
- `00468A70(sector, circle)`: a circle on the centre passes; one at or beyond `R + r` fails; a sweep
  of a full turn or more passes everything in reach.
- Otherwise `00468A70` takes the angle from the start ray to the circle's centre (the arc-cosine
  table `00D12590`, 16,384 steps, made a full-turn angle by the sign of the cross product); it must
  lie in `(0, sweep]`, or either edge ray, from the centre to `R` along the start or the end angle,
  must meet the circle (`00469410` with width 0).
- A dot product that rounds above 1 has 1 subtracted rather than being clamped, so a circle exactly
  on the start ray reads as ninety degrees off.

### Finding a free spot beside an anchor

`00336E40(request)` picks a standing point for an actor next to another: the party placement after a
zone jump and the revive placement call it ([KO and game over](../Status-Effects-And-KO/ko-and-game-over.md)).
The request holds a mode at `+0x00`, the anchor unit at `+0x08`, the unit to place at `+0x10`, and
receives the point at `+0x20` and a heading at `+0x30`.

The base is the anchor's position dropped onto the floor (`0026E350`), with the anchor's larger
radius and its facing. Without an anchor the base is the recorded anchor `022C7DD0` with radius 0.5
and heading `022C7DE0`, and the party leader (`003272A0`) gets that point and heading outright; with
nothing recorded (`022C7D10` = 0) the unit keeps its own position and facing. `0033CA00` records the
anchor from the controlled character: its position, facing, actor (`022C7D18`) and a copy of its
placement (`022C7D20`, 0xB0 bytes).

The distance and the first heading depend on the mode:

| Mode | Distance | First heading |
|---|---|---|
| 0 | the unit's larger radius + the anchor's radius + 0.5 | the anchor's facing |
| 1 | 3.6 when `0030D9A0()` is 1, else 2.0 (`00309AE0`) | the bearing from the point `+0x90` of camera record 2's view (`00259B10(2)`, `02097320 + 2 * 0x110`) through the base, turned 40 degrees left or right by a C runtime `rand()` bit |
| 2 | as mode 0 | the anchor's facing plus 210 degrees |

Twelve headings are tried in order, the first heading plus 0, -30, +30, -60, +60 and so on to -180
degrees, each at the distance along that heading; a second ring adds 1.0 to the distance and 20
degrees to the first heading. The first point that passes both tests below wins and the call
returns 1; with none the base is used and it returns 0. The point is dropped onto the floor and the
heading is the bearing from the point to the base, so the unit faces the anchor.

`00336210(point, base, unit, kind)` accepts a point when the dynamic obstruction query
(`003357B0`, flags `0x20`, or `0xA0` for mode 2) finds nothing there for the unit's larger radius,
the straight walk from the point to the base is not blocked for class 2 (`0033D3E0`), the segment
query (`00391410`) finds no shaped obstacle at the point, the point is on the mesh (`00384130`), and
`00336390` finds walkable terrain (`0026E100`) at the point and at the four corners `+-r` in x and
z. A unit with no actor is accepted at once.

`00336AE0(anchor, point)` then asks whether the anchor could walk there: it copies the anchor's body
placement (`00265970`, or the recorded copy when there is no anchor), makes it a kind-1 body with
radii 0.5, moves its start 0.6 toward the point and, when the point is within 10, sweeps the rest of
the way over the collision mesh (`00380C40`, the collision-mesh
sweep); it passes when the sweep ends within 0.001 of the point. With
no anchor and nothing recorded, the copy is the stack as it was.

### Placing the party

`00310920(point, angle)` is the body of the zone-jump party placement (`0037D000`). It collects the
party's battle units (`0031B810` for slots 0-3) that have a status record free of `0x80000003`, or
any of them in a town (the town flag `00377C20`), into `022C1788` (four at most):

- with none, the character `00327270()` names is placed at the point and turned to the angle;
- with no leader (`003272A0`), `00310D30` does the same and every collected unit is placed at the
  point itself;
- with a leader, the leader is placed at the point and every other unit at the spot `00336E40`
  finds for it in mode 2 beside the leader.

Each placed unit's actor goes to its point (`0026B0C0`), the unit's `+0xD0` and `+0xE0` both take the
point, `00392170` runs on its actor, unit flag bit 26 is set, `+0x15C` and `+0x160` take the angle,
and the actor's yaw and facing are set to it (`0026A0D0`, `0026B620`). `00313670` re-places every
collected unit other than the leader with `00311F70(0, unit, 0)`.

`0033A380`, from the area initialisation `002342F0`, clears the recorded-anchor flag `022C7D10` and
the 48 bytes at `022C7CE0`, and `004696A0` resets the ten `0x20`-byte slots at `02EBB560`.

## Layouts

Globals:

| Address | Type | Name | Meaning |
|---|---|---|---|
| `02AEDFB0` | `void*` | the navigation dataset (null when none) |  |
| `00915760` | `i32[6]` | class to override bit: {23, 25, 26, 27, -1, 24} |  |
| `0209A3E0` | `u32[32][2]` | map-id overrides: dword 0 = override present, dword 1 = closed |  |
| `00D10818` | `f32` | 1.4140000343, the clearance factor |  |
| `00D112B0` | `i32[4]` | {0, 1, 2, 0}, the edge index table |  |
| `02AEE060` | `.. 02AEE0C0` | the obstacle grid (section above) |  |

Battle unit:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x080` | `locomotion block (the solver's argument)` | +0xD0 | f32[4]  search start point |
| `+0x0E0` | `f32[4]` | mover position read by the follower | +`0xF0`  f32[4]  the waypoint written |
| `+0x100` | `f32[4]` | goal | +`0x158` u32     zeroed on flag bits 7 and 10 |
| `+0x1F0` | `u32` | step flags | +`0x1F4` u8      mover class |
| `+0x200` | `NavPath (0x490 bytes)` | +0x698 ptr | handler checked on a failed search |
| `+0x708` | `void*` | order record (word +4: 0x200, 0x100) | +`0x714` u16     action id |

## Shipped data

| Fact | Value |
|---|---|
| sections with a mesh | 461 of 461 map packs |
| regions, portals | 31,672 and 52,174 |
| largest region count | 128, the array bound |
| portals ungated, gated | 51,248 and 926, under 30 map ids |
| class masks | `0x2F` 32,467; `0x08` 19,374; `0x00` 324; `0x0C` 8; `0x2B` 1 |
| `setmapidfloor` calls | 106,618 in the 1,114 zone scripts; 84,066 with a literal kind (2, 3, 0, 1, 7, 9 and 4, the 1,886 no-ops), 22,552 with a variable |

## Operations

Per step: the combat site asks for a navigation step; the search returns at once when the held
route still reaches the goal, re-searches when it does not, and refuses a remembered dead end; the
follower advances past regions already entered, re-aims the waypoint, and hands it to the
locomotion solver. Per field frame: the obstacle grid is cleared and refilled from every actor,
trailer record and registry entry before the queries that read it.

## State

The dataset pointer and the rebased section; each unit's path record; the override table; the
obstacle grid's records, occupancy bytes, mask scratch, count and actor list.

## Modding notes

- The route cache is keyed on regions alone; it stays valid only because every override change
  wipes every unit's cache. A reimplementation that changes the mask or the overrides by another
  route must wipe them too.
- The clearance factor is the decimal 1.414, not root two, and it is applied by the caller; the
  difference decides waypoints on portals within a fraction of a centimetre of twice the radius.
- Costs are integers of `trunc(100 * distance)`; a port in floating point breaks ties differently.
- A gated portal defers to the script's override when one exists and to its authored mask when
  none does; kind 4 has no bit and its verb calls do nothing.
- The region lookup admits the rectangle's upper edges and does not bound the cell index; keep
  computed columns and rows inside their counts and cell sizes non-zero.
- Shaped obstacles (ids 128 and up) are visible to the segment query and invisible to the actor
  query; actors the other way round.

## Related

- [Battle locomotion](battle-locomotion.md): the solver that consumes the waypoint.
- [Map pack](../World-Areas-And-Travel/mpk-map-pack.md): slot four.
- [Battle unit fields](../Characters-And-Objects/battle-unit-fields.md): the unit's class byte and blocks.
- [Movement bodies and separation](movement-bodies-and-separation.md): the collision radii.
