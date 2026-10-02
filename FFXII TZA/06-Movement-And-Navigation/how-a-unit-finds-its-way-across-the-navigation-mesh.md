---
system: How a unit finds its way across the navigation mesh - the dataset, the region search, the waypoints, and the script verb that opens and closes its doors
category: 06-Movement-And-Navigation
status: AUDITED
owner_layer: PrimaryOwner:Movement
evidence_tier: 1
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: the navigation module 00382D10..003843E3 and the four bodies outside it that this page names, disassembled
    from the authority image and read whole, 2026-09-19; the dataset layout the code reads then parsed out of slot 4 of
    every map pack in an extracted copy of the game (461 of 461 files, every structural test passing); the script verb's
    use counted in the 1,114 decompiled field scripts
last_reviewed: 2026-09-29
audit:
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-nav-mesh-falsification-pass-1
  crossref_clean: true
  reopened_count: 0
  note: written by FABLE while placing two of FRONTIER's uncited bodies (00382D10, 003842E0), which turned out to have no
    page to go on - the pathfinder had only mechanical rows on the battle-unit field map. Static, plus one data census.
    Not read - the locomotion solver that consumes the waypoint, the direct-route check that shares the portal test, and
    the six other callers of the region lookup; pending first review  promoted: 2026-10-01 DOCUMENTED -> AUDITED by SWE2-AUDIT-SPEC (FRONTIER eligibility census sweep): falsification record opus-nav-mesh-falsification-pass-1; audit_crossrefs at HEAD reports 0 unresolved findings; cross-subsystem neighbours dispositioned in their section; killer observations recorded in the pass; promoter is not the last substantive author (last substantive commit: OPUS)
---

# How a unit finds its way across the navigation mesh

A battle unit that wants to be somewhere else does not steer at its goal. It asks a small pathfinder for **the next
point to walk toward**, walks, and asks again. The pathfinder works on an authored mesh that arrives with the area:
triangles grouped into at most 128 convex-ish **regions**, joined by **portals** - shared edges a mover may cross. It
searches regions, not triangles; it places one waypoint on each portal of the route; and it re-aims the nearest waypoint
every time it is asked, so the path bends as the unit moves. Whether a portal is open depends on **what kind of mover is
asking** - and a field script can open or close it per kind, which is how an event fences enemies into a room or lets
the party through a door.

## 1. The dataset

The mesh is **slot 4 of the area's map pack** ([the map ctrl pack](../03-World-Area-Field/Map-Pack/the-map-ctrl-pack.md)).
The area setup hands the copied section to `00384160` (372 B), which stores its address in `02AEDFB0` and rebases the
offsets inside it in place: the six header offsets at `+0x0C`..`+0x20`, a seventh at `+0x28`, and the grid's own two at
`+8` and `+0xC`. `00383A20` clears the pointer, `00383C80` answers whether it is set, `00383840` returns it. *(qualified 2026-09-28, FABLE, Claude Opus 5.5, on ASTRA's nav root call order; addresses in [`fable-returns-0928k`](../_index/candidates/fable-returns-0928k/README.md)): the clear has two callers, one on the startup chain and the area-unload reset. On the reset's normal entry the pointer is cleared before the grid teardown, with one call between them whose effects are not traced, so whether the pointer stays 0 until the grid is gone is not established.)*

```struct NavDataset base=section
+0x00  u32   1
+0x04  u16   vertexCount      not read by the code; holds on 461 of 461 files
+0x06  u16   triangleCount    loop bound of the whole-mesh containment test
+0x08  u16   portalCount      not read by the code; holds on 461 of 461 files
+0x0A  u16   regionCount      <= 0x80: the search keeps fixed 128-entry arrays
+0x0C  off   vertices         8 B each: f32 x, f32 z
+0x10  off   triangles        8 B each: u16 vertex[3], u16 region
+0x14  off   portals          8 B each: u16 vertexA, u16 vertexB, u8 gated (+4), u8 mapId (+5), u8 classMask (+6)
+0x18  off   regions          0x22 B each: +2 u16 triangleCount, +0x14 u16 triangleIndex[] (at most 7 fit; 6 is the most any file uses)
+0x1C  off   adjacency        regionCount x regionCount u16: the portal from region i to region j, 0 = none
+0x20  off   grid             u8 cellW, u8 cellH, u8 cols, u8 rows, i16 originX, i16 originZ, +8 off cellTable, +0xC off listPool
+0x28  off   trailer table (rebased; readers since read — `00392740` and `00391597` reach it through getter `00383840`, whose return a cell-seeded census does not propagate to callers)
```

The layout above is what the code reads; it was then tested against the data
([`census.py`](../_experiments/evidence/navigation-dataset-layout/census.py) →
[`census.out.txt`](../_experiments/evidence/navigation-dataset-layout/census.out.txt)): in **461 of 461** sections every
triangle's vertex indices are below the vertex count, every triangle's region id is below the region count, **every
triangle a region lists names that region back**, the adjacency matrix has an empty diagonal and portals in both
directions wherever it has one, every portal's vertices exist, and every grid cell's list is a `0xFF`-terminated run of
valid region ids. The largest region count in any file is **exactly 128**, the search's array bound. 31,672 regions and
52,174 portals in all.

**Everything is XZ.** Height plays no part in the mesh; callers pass `(x, z)` pairs and the two entry points that take
world positions (`00383620`, `00384130`) drop `y` on the way in.

## 2. Which region am I in - `00383F10` (542 B)

A point is rejected (`0xFF`, "no region") if either coordinate is NaN or it lies outside the grid's rectangle
(`origin` .. `origin + cell x count`). Otherwise the cell `(z - originZ) / cellH x cols + (x - originX) / cellW` indexes
the u16 cell table; `0xFFFF` is an empty cell, anything else is an offset into the list pool, where a `0xFF`-terminated
list of region ids waits. Each listed region's triangles are tried in turn with `00382D10` (391 B), and **the first
region with a triangle containing the point wins**.

*Qualified (2026-09-27, FABLE, Claude Opus 5.5, bytes re-read, on OPUS-NOTICE-FABLE-NAV-PAGE-UPPER-EDGE and ASTRA's
[nav-upper-bound-admission](../_experiments/evidence/nav-upper-bound-admission/README.md)):* **both edges of the rectangle are
admitted.** The lower checks reject only `origin > x` (`00383F77`, `00383F93`), and the upper checks are `ja` against
`origin + count x size` (`00383FAF`, `00383FCD`), so a point exactly on the upper edge passes. The cell index is then
loaded at `0038402C` with no bound check. A point with `x` exactly on the upper edge takes column `cols`, which is the
next row's first cell; with `z` exactly on the upper edge it reads past the cell table. The only test after the load
is the `0xFFFF` sentinel. A strictly smaller world `x` is not always safe, because the distance is rounded in `f32`:
origin -32768, cell 255 and 255 columns take `x = 32256.998046875` to a distance of `65025.0`, which is column 255.
The evidence is an isolated original-code fixture (ASTRA, B-tier), not a normal-game occurrence.

`00382D10` is a point-in-**triangle** test, whatever its analysis name says about polygons. It walks the three edges
through the index table `{0, 1, 2, 0}` at `00D112B0`, takes the cross product of each edge with the vector from the
edge's start to the point, keeps the first non-zero cross as the reference sign, and answers 0 as soon as a later cross
has the opposite sign. A zero cross - the point on an edge's line - is tolerated, so a point on a shared edge belongs to
whichever region the cell lists first.

`00383A30` (591 B) asks the narrower question "is this point inside region *r*?" without the grid: it scans **every
triangle of the mesh**, skips those whose region word differs, and runs the same three-cross test inline. Region `0xFF`
is never inside. `00383740` (252 B) returns the grid's rectangle as four floats.

## 3. The path record

Each battle unit carries one, at `unit + 0x200` (`0x490` bytes; the navigation step addresses it as its locomotion block
`+0x180`):

```struct NavPath base=unit+0x200
+0x00   i32      region the mover was last placed in
+0x04   i32      start region of the route held, 0xFF = none
+0x08   i32      goal region of the route held, 0xFF = none
+0x0C   u8[2]    the last (start, goal) pair that had NO route
+0x0E   u8[2]    the one before that
+0x10   u8[128]  next[region] - the region to enter after this one; 0xFF ends the chain
+0x90   xz[128]  waypoint[region] - the point to walk to while in this region (f32 x, f32 z)
```

`003839F0` fills `next[]` with `0xFF`; `003839C0` fills the two no-route pairs with `0xFFFF`.

## 4. The search - `00382FF0` (1,575 B)

`(start xz, goal xz, path, moverClass, radius)`, reached through `00383620`, which only repacks two world positions.

1. Both points are located (section 2). A start off the mesh returns **-2**, a goal off the mesh **-3**.
2. **Same region:** the waypoint of that region is the goal itself, its `next` is `0xFF`; return 0.
3. **Known dead end:** if `(start, goal)` equals either remembered no-route pair, return -1 without searching.
4. **Route still good:** follow `next[]` from the start region (stopping at `0xFF`, a self-loop or an id past the region
   count). If the chain reaches the goal region, only the goal's own waypoint is refreshed; return 0. A unit chasing a
   target that moves about inside one region therefore never searches twice.
5. **Otherwise, Dijkstra over regions**, the plain O(n^2) form: integer distances start at `0x7FFFFFFF`, the start region
   at 0 with the start point as its *entry point*. Each round settles the current region, stops if it is the goal, and
   relaxes **every** unsettled region `j` through the cost function of section 5; an improvement records the
   predecessor, the new entry point (the closest point of the portal) and the distance walked to it. The next current
   region is the unsettled one with the least distance; the search ends when none is reachable.
6. **The waypoints are laid walking back from the last region settled** toward the start, carrying a *target* that begins
   as the goal. For each step `pred → cur`, with the portal's ends `A`, `B`:
   - `c` = the point of `AB` closest to the target (`00382EA0`), at distance `d1`; `e` = the entry point the search
     recorded on the same portal, reached after walking `d2`;
   - the waypoint is `c + (e - c) x d1 / (d1 + d2)` (the midpoint of the two when both distances are zero) - the two
     feet divided in proportion to the two distances, which is where a straight line from the previous point to the
     target would cross the portal;
   - **clearance:** if the portal is shorter than `2 x radius` the waypoint becomes its midpoint; otherwise, if it lies
     within `radius` of `A` it is pushed to `radius` from `A` toward `B`, and likewise from `B` (`003842E0`, section 6);
   - `waypoint[pred]` = that point, `next[pred]` = `cur`, and the point becomes the next target.
7. `waypoint[goal]` = the goal. If the last region settled **was** the goal: `next[goal] = 0xFF`, return 0. If not, the
   pair is pushed onto the two-deep no-route memory, the held route is marked empty, and the search returns **-1** - so
   an unreachable goal costs one full search, then nothing until the pair changes or the memory is wiped (section 7).

## 5. What a portal costs, and who may cross it - `00383850` (368 B)

`(from, to, goalRegion, entryPoint, goalPoint, outPoint, moverClass, outDistance)`. `adjacency[from x n + to]` of 0 is
"not neighbours": cost `0x7FFFFFFF`. Otherwise the portal is tested for **this mover class**:

- **an ungated portal** (byte `+4` = `0xFF`) is open when bit `moverClass` of its class mask `+6` is set;
- **a gated portal** first asks `0026E300` (73 B, through a five-byte thunk) about its map id `+5`. That body looks the
  class up in a six-entry table at `00915760` - `{23, 25, 26, 27, -1, 24}` - to get an attribute bit, then reads the
  script's **map-id override table** `0209A3E0`
  ([the movement body pool](the-movement-body-pool-and-the-separation-pass.md), section 2.4): no override for that bit →
  0, **fall back to the authored class mask**; override present with the bit clear → 1, **open whatever the mask says**;
  override present with the bit set → 2, **closed**; a class with no bit (`-1`) → closed.

An open portal costs `trunc(100 x d)`, where `d` is the distance from the entry point to the portal segment - plus, when
`to` is the goal region, the distance from that closest point on to the goal. The closest point and `d` go back to the
search. So distances are **centimetre-grained integers measured portal to portal**, not region centres, and only the last
hop sees the goal.

In the shipped data 51,248 portals are ungated and 926 gated, under 30 distinct map ids, none above 31. The class masks
are `0x2F` (every class; 32,467 portals), **`0x08` (class 3 only; 19,374)**, `0x00` (324), `0x0C` (8) and `0x2B` (1): the
mesh is two meshes in one - a walkable core, and a wider skirt only class-3 movers may enter.

## 6. The two geometry leaves

`00382EA0` (332 B) is distance from a point to a segment in XZ, optionally returning the closest point: the far end when
the point projects beyond it, the near end when it projects before it, else the foot of the perpendicular, with the
distance taken as `|cross| / |AB|`.

`003842E0` (260 B), `(A, B, out, r)`: if `A` equals `B`, `out = A`; if `AB` is shorter than `2r`, `out` is the midpoint;
otherwise `out = A + r x (sin a, cos a)` with `a = atan2(dx, dz)` - **the point `r` from `A` toward `B`**, the engine's
heading convention ([heading and speed to a position delta](heading-speed-to-position-delta.md)). Its only two callers
are the clearance steps of sections 4 and 8.

## 7. The script's hand on the doors

The mover class is the battle unit's byte `+0x1F4`, the field the unit field map calls `placementMode`
([the battle unit field map](../04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md)): **1 by default, 2 for an
enemy record, 3 for an enemy whose probe gate has bit 3.** Those are exactly the *kind* numbers of the script verb
**`setmapidfloor(mapId, kind, on)`** (`0x00FE`): its tail `003792E0` (245 B) switches on `kind` through a ten-entry
jump table of which six arms are real - **0 → bit 23, 1 → bit 25, 2 → bit 26, 3 → bit 27, 7 → bit 24, 9 → bit 12** - the
same bit numbers, under the same small indices, as the pathfinder's class table. `on` non-zero stores the override with
the bit **clear** (open), `on` = 0 stores it **set** (closed), a negative `on` removes the override. The 1,114 decompiled
field scripts make 84,066 such calls, all with literal kinds: 0, 1, 2, 3, 7 and 9 - the six real arms - and **4, whose
1,886 calls reach the bare return and do nothing in this build** (class 4 is also the one class the pathfinder's table
gives no bit). Kinds 2 and 3, the enemy classes, account for 55,461 of the calls.

Every change to the override table ends in `003278D0` (84 B): for each live battle unit it wipes the no-route memory
(`003839C0`) and the `next[]` chain (`003839F0`) of the unit's path record. **Opening or closing a door invalidates every
unit's cached route and every remembered dead end at once**, which is why the two caches of section 4 are safe.

## 8. One step of following the route - `00383670` (204 B)

`(position, -, outPoint, path, radius)`. Starting from the region the mover was last placed in, it advances along
`next[]` **while the mover's point is already inside the next region** (`00383A30`), so a mover that cut a corner skips
the waypoint it no longer needs. Then `00383C90` (632 B) re-aims the current region's waypoint from where the mover is
now: on the portal to the next region it takes the closest point to the mover (`d1`) and the closest point to the
*following* waypoint (`d2`), divides them as in section 4, and applies the same clearance rule. The mover's region is
stored back, and the output is that waypoint with **the mover's own `y`**. In the goal region `next` is `0xFF`, nothing
is re-aimed, and the waypoint is the goal.

The caller is the battle unit's navigation step `00325BB0` (465 B,
[battle locomotion](Battle-Locomotion/battle-locomotion-steering-and-recovery.md)): it builds or reuses the route from
the locomotion block's current position to its destination, abandons the step when the search does not return 0, and
otherwise takes the next waypoint and hands it to the locomotion solver. The radius it passes both times is
**1.414 x the larger of the actor's two collision radii** (`0030A130`, 40 B) - the half-diagonal of the square the
actor's footprint fits in.
**REFINED 2026-09-22 (FABLE): the factor is the decimal literal, not root two, and it is applied by the CALLER.**
`0030A130` returns only `maxss` of the two radii and multiplies by nothing; the navigation step multiplies at both of
its call sites (`00325BFA`, `00325C49`) by the `f32` at `00D10818`, whose stored value is
**`0x3FB4FDF4` = `1.4140000343`**. The nearest `f32` to `sqrt(2)` is `0x3FB504F3` = `1.4142135624`, so the shipped
factor is **0.015 % below** the half-diagonal this sentence describes. The intent is the half-diagonal; the constant is
a rounded decimal, and **a reimplementation computing `sqrtf(2.0f)` differs on portals within a fraction of a
centimetre of twice the mover's radius** - which is exactly where section 4's clearance rule changes its answer. See
[the search-and-follow contract](CONTRACT-navigation-search-and-follow.md) NV-5.

## 9. What a reimplementation must keep

- The region lookup's tie-break: first region in the cell's list with a containing triangle; edge points count as inside.
- The search is over **at most 128 regions**, exhaustive, with integer costs of `trunc(100 x distance)` measured from
  entry point to portal, the goal's leg added only on the last hop.
- Two caches: a held route is reused while its `next[]` chain still leads from the start region to the goal region, and
  the last two failed `(start, goal)` pairs fail at once. Both are wiped for every unit whenever a script changes a
  map-id override.
- Waypoints sit on portals, divided between two closest points in proportion to the two distances, then kept `radius`
  from either end - or on the midpoint of a portal narrower than the mover.
- A portal's openness is per mover class; a gated portal defers to `setmapidfloor`'s override when one exists and to its
  authored mask when none does.
- Return codes: 0 route, -1 none, -2 start off the mesh, -3 goal off the mesh.

**Not read:** ~~the locomotion solver that consumes the waypoint;~~ *(answered for the solver: see [battle locomotion](Battle-Locomotion/battle-locomotion-steering-and-recovery.md), whose turn limiter and step distance are read in full; 2026-10-02, OPUS)* the direct-route check that applies the same portal test
while walking a straight line across regions ([the world tick](../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md)
has a peer's note on it); the six other callers of the region lookup; what class 3's "probe gate bit 3" means for the
creature that has it; what kinds 0, 7 and 9 of the verb gate (class 0 and class 5 have no unit that was seen to use them).

## 10. What occupies the grid each frame — the obstacle bitsets (FABLE, Claude Opus 5.5, 2026-09-28)

Sections 1 to 8 are about the mesh: regions, portals, the route. Beside it the area keeps a coarse obstacle grid, and this is
what fills it. Every address is re-derived from the certified image in [the record](../_index/candidates/nav-obstacle-grid/README.md), which also holds the
addresses of the actor, registry and bounds routines named here only by role.

**The grid.** It is built once per area (the grid-rebuild row on the unit-definition page; its lifetime is in the world-tick
page's area-teardown row). Each of its cells owns an `n`-byte record, with `n = 0x24`, and one occupancy byte. The record is a
**bitset of 288 obstacle ids**: bit `id` set means obstacle `id` overlaps this cell.

**Refilled every frame.** The obstacle builder (its address is in the record) runs at step 21 of the world tick. It sets the listed-actor count
`02AEE0BC` to 0, clears every cell record, every occupancy byte and the 128-slot actor list at `02AEE0C0`, then assigns ids
in three ranges:

| ids | obstacles | position and radius |
|---|---|---|
| 0–127 | actors from the actor manager's three slot groups, while the count is below 128; each is also stored at `list[id]` | the actor's position; the larger of its two radii |
| 128–159 | the navigation dataset's trailer records (at most 32, 0x20 bytes each), kinds 0 and 1 only; other kinds are skipped but still use an id | record floats `+4` / `+8`; the radius `+0xC`, or the larger of `+0xC` and `+0x10` for kind 1 |
| 160–287 | a map-pack registry's active entries, at most 128 | the entry's position; the larger of its two radii |

**How an obstacle lands in cells.** `00392200(id, x, z, r)` takes the cells under the square `[x − r, x + r] × [z − r, z + r]`,
clamped to the grid, and tests each against the circle. *(The test, exact: a cell counts when the circle's centre lies in the cell widened by `r` along one axis at a time, edges included, or when one of the cell's corners lies strictly inside the circle, `r² > d²` in float32. Contact along an edge counts; tangency exactly at a corner does not. ASTRA ran the original test in isolation, and FABLE's float32 model of its instruction order agrees, including the one-ulp radius neighbours of a tangency. The game's MXCSR and malformed inputs stay open; see the record.)* On a hit it sets bit `id` in that cell's record and increments its
occupancy byte.

**How a query reads it.**
- `003912E0` ORs the records of the occupied cells in a rectangle into the mask scratch at the block's tail.
- `00391710` builds its own mask the same way. It then walks bits 0 to count − 1 only, the listed actors, and returns each
  actor whose bounds meet the query shape.
- So that query sees actors and never the ids from 128 up. Which consumer reads those ids from the mask is not read here.

**Limits a port must keep:**
- **The id space is exactly the record.** 128 + 32 + 128 = 288 = 0x24 × 8.
- **The registry count is read twice.** When the first read is below 128, a second read is used unchecked. Only a count that
  changed between the two reads could reach id 288. That id would set bit 0 of the *next* cell's record, or of the first
  occupancy byte after the last cell. Nothing here shows the count changing. *(Executed 2026-09-28 by ASTRA: the original 88-byte marking fragment was run in isolation, outside the game, and id 288 spills exactly this way. FABLE's static model of the same instructions agrees with every executed case. The builder never passes a negative id; the harness's −1 and −8 cases are not reached from it. See the record.)*
- **The occupancy byte is a `u8` increment.** 256 overlaps would read as an empty cell, which the query skips. *(Executed by ASTRA: the byte wraps 255 → 0, and it does not saturate.)* Whether a
  cell can gather that many is not shown.

## Evidence

Every body below was read whole. Interior anchors for those of 128 bytes or more:

| body | interior anchors |
|---|---|
| `00384160` bind and rebase (372 B) | `0038416D`, `0038417C`, `00384196`, `003841B6`, `003841D6`, `003841F6`, `00384216`, `00384236`, `00384267`, `003842A0`, `003842CC` |
| `00383F10` region of a point (542 B) | `00383F3E`, `00383F64`, `00383F99`, `00383FD3`, `0038402C`, `00384031`, `0038404F`, `0038407C`, `003840A9`, `003840C4`, `003840FE`, `0038411B` |
| `00382D10` point in triangle (391 B) | `00382D31`, `00382D6E`, `00382DAC`, `00382E10`, `00382E44`, `00382E56`, `00382E5D` |
| `00383A30` point in region (591 B) | `00383A41`, `00383AAD`, `00383AC8`, `00383AEA`, `00383B13`, `00383BB7`, `00383BE5`, `00383C03`, `00383C0A` |
| `00382FF0` the search (1,575 B) | `0038302F`, `0038303F`, `00383051`, `00383066`, `00383077`, `0038308D`, `003830B0`, `003830E3`, `00383104`, `00383140`, `0038315A`, `003831A3`, `003831CC`, `00383247`, `00383253`, `00383279`, `00383285`, `003832B8`, `00383363`, `00383392`, `00383403`, `0038341B`, `00383425`, `0038349B`, `003834DB`, `00383503`, `0038351C`, `0038352A`, `00383532`, `003835B8`, `003835CB`, `003835E1` |
| `00383850` portal cost (368 B) | `00383892`, `0038389A`, `003838C4`, `003838CC`, `003838D8`, `003838E6`, `003838F0`, `0038395C`, `00383975`, `0038399B`, `003839A3` |
| `00382EA0` point to segment (332 B) | `00382F02`, `00382F0D`, `00382F44`, `00382F4F`, `00382F7A`, `00382FB9`, `00382FCA` |
| `003842E0` point `r` along a segment (260 B) | `00384324`, `0038432C`, `00384359`, `00384366`, `0038438D`, `00384395`, `003843AA` |
| `00383C90` re-aim a waypoint (632 B) | `00383CD3`, `00383D1D`, `00383D7B`, `00383D9B`, `00383DBA`, `00383DCA`, `00383E2E`, `00383E75`, `00383E9B`, `00383EB1`, `00383ED6` |
| `00383670` one step (204 B) | `00383699`, `003836B0`, `003836B8`, `003836D0`, `003836ED`, `00383700`, `0038371D` |
| `00383740` grid rectangle (252 B) | `0038377E`, `0038379C`, `003837D7`, `0038380E` |
| `003792E0` the verb's tail (245 B) | `003792E3`, `003792ED`, `00379300`, `0037930D`, `0037931C`, `0037932B`, `0037933A`, `00379349`, `00379358`, `00379373`, `00379380` |
| `00325BB0` the unit's navigation step (465 B) | `00325BD0`, `00325BFA`, `00325C06`, `00325C22`, `00325C27`, `00325C6D`, `00325D0A` |

Data: `00D112B0` = `{0, 1, 2, 0}`; `00915760` = `{23, 25, 26, 27, -1, 24}`; the verb tail's jump table at `003793D8`
sends kinds 4, 5, 6 and 8 to a bare return. Script use: `setmapidfloor` is called in 423 of the 1,114 decompiled scripts.

## Cross-subsystem neighbours

**Presentation - SERVICE.** `00382EA0`, the point-to-segment distance, is filed under the Presentation layer by the
classification; its three callers are all on this page (the search, the cost function, the re-aim). It is this module's
geometry leaf and nothing about drawing crosses.

**CombatAction - CLIENT.** `00325BB0`, the unit's navigation step, is called from the action layer's unit state
machines (four call sites in the call graph), and `0030A130`, the clearance radius, from one action-layer body. They
drive this module each frame a unit has somewhere to go; nothing of the pathfinder is owned there, and those callers
were not read for this page.

**CombatAI - CLIENT.** `0030A130` is also called from two combat-AI bodies, which want the same footprint radius for
their own distance tests. The crossing is that getter; those callers were not read.

**ActorEntity - SERVICE.** The obstacle builder (§10) takes obstacle ids 0–127 from the actor layer: the actor manager's slot-range accessors, its slot fetch, and the actor's position and radius getters (named by role; their addresses are in the [obstacle-grid record](../_index/candidates/nav-obstacle-grid/README.md)). What crosses is each actor's pointer, position and two radii. Nothing of the actor record is owned here, and those accessors' other callers were not read.

**Script VM native bridge, World/Area/Field - by role only.** The verb's handler and the area setup that binds the
dataset are described by role and not cited; the verb's tail `003792E0` carries no owner in the classification.
- **Audio - CLIENT (1 edge).** `003148F0` is also called by bodies filed to audio: `00261F90` - shared machinery across the layer boundary, no shared ownership.
- **CombatFormula - CLIENT (1 edge).** `00377C20` is also called by bodies filed to combat formula: `00300530` - shared machinery across the layer boundary, no shared ownership.
- **Core - CLIENT (1 edge).** `00383A20` is also called by bodies filed to Core: `002341C0` (CrossSubsystemResetOrchestration) - shared machinery across the layer boundary, no shared ownership.
- **Gameplay - CLIENT (5 edges).** `0033CB70`, `00377C20` are also called by bodies filed to Gameplay: `00339630` (Combat), `00307D10` (Combat), `0030A8A0` (Combat) - shared machinery across the layer boundary, no shared ownership.
- **Input - CLIENT (3 edges).** `00263FF0`, `00377C20` are also called by bodies filed to input: `00226BE0` (ActorControlMaskPropagationRuntime), `002E09A0` (CommandGateBoundarySupport), `00253C70` - shared machinery across the layer boundary, no shared ownership.
- **InputGameplay - CLIENT (1 edge).** `00377C20` is also called by bodies filed to InputGameplay: `00313A00` (FieldBattleCapabilityAndUIRequestInhibitMaskReconciliation) - shared machinery across the layer boundary, no shared ownership.
- **Items_Equipment_Shops_License - CLIENT (2 edges).** `00377C20` is also called by bodies filed to items/equipment: `00309FB0`, `0030FD10` - shared machinery across the layer boundary, no shared ownership.
- **Party - CLIENT (1 edge).** `00377C20` is also called by bodies filed to party: `00304180` - shared machinery across the layer boundary, no shared ownership.
- **PlatformOnlineAchievements - CLIENT (1 edge).** `003148F0` is also called by bodies filed to PlatformOnlineAchievements: `003160C0` - shared machinery across the layer boundary, no shared ownership.
- **Rewards_Progression_Economy - CLIENT (1 edge).** `00377C20` is also called by bodies filed to rewards/progression: `00312280` - shared machinery across the layer boundary, no shared ownership.
- **Save_Load_Settings - CLIENT and SERVICE (2 edges).** `003148F0` is also called by bodies filed to save/load/settings: `00583D60`; `003148F0` reaches bodies filed to save/load/settings: `002EF2B0` - shared machinery across the layer boundary, no shared ownership.
- **Spawn_Encounter_Lifecycle - CLIENT (1 edge).** `003148F0` is also called by bodies filed to spawn/encounter lifecycle: `00233780` - shared machinery across the layer boundary, no shared ownership.
- **Status_Periodic_Terminal - CLIENT (3 edges).** `00377C20` is also called by bodies filed to status/periodic terminal: `0030E360`, `0030F690`, `00310DB0` - shared machinery across the layer boundary, no shared ownership.
- **UI - CLIENT (5 edges).** `003148F0` is also called by bodies filed to UI: `0029C530`, `003C5F00`, `003C80C0` - shared machinery across the layer boundary, no shared ownership.

## What executing the query tree added — [`EXP-131`](../_experiments/EXP-131-navgrid-query-exec.md), adopted 2026-09-20 (OPUS)

This page describes what the navigation query **means**; EXP-131 ran it — 54/54 functional
cases, 61/61 mutants, stable across three processes — and what follows is only the
**representation and reimplementation** side of that, not a second account of the mechanism.
Five of these are things a reimplementation gets wrong silently.

### The record shapes, measured (OPUS)

| thing | shape |
|---|---|
| adjacency matrix entry | **2 bytes**, at `m[cur*deg + slot]`, with `deg = w[root+0xA]` — ~~the triangle count~~ the region count, §1's `regionCount` *(corrected 2026-10-02, OPUS: `00383883` `movzx r10d, word [r11+0xA]` / `00383888` `imul r10d, ebx` make it the row stride of the region-by-region adjacency)* |
| adjacency entry value | a **1-BASED** edge-record index; **`0` means no edge** |
| edge record | stride **8** — ~~`{w va, w vb, b +4, b class@+5, b flag@+6}`~~ `{w va, w vb, b gated@+4, b mapId@+5, b classMask@+6}` *(corrected 2026-10-02, OPUS: `003838C4` `test byte [rec+6], r8b` with `r8b = 1 << class`; `003838CC` `cmp byte [rec+4], 0xFF`; `003838D3` `movzx ecx, byte [rec+5]` → `0032A780`)*, at `BASE(edgeId*8)` |
| grid candidate record | stride **0x22**, triangle selector at **`+0x14`** |
| cell list | a byte list of record indices, **`0xFF`-terminated** |
| walk budget | `r13d == 0x80` → return `0` |

**Record 0 of the edge pool is unused padding**, which is what makes the index 1-based. An
implementation that treats the adjacency entry as a 0-based index reads the padding record
for every first edge and is wrong without faulting.

### Four arithmetic behaviours a port will not reproduce by accident (OPUS)

1. **The cell division is a signed `idiv` and truncates TOWARD ZERO.** Python's `//` floors,
   so `-7 // 2` disagrees with the shipped body on every negative numerator. ~~This bites only~~
   ~~outside the grid origin, which is exactly where a test corpus tends not to go.~~ *In `00383F10` it does not bite for a
   stable finite point: a point below the origin is rejected by the `ja` checks before any conversion, so every
   numerator is in `[0, 65025]` (qualified 2026-09-27, FABLE, Claude Opus 5.5, on ASTRA-RETURN-FABLE-NAV-CONVERSION-DOMAIN).*
2. **`cvttss2si` on overflow or NaN yields `0x80000000`** — the integer indefinite — rather
   than raising. ~~The out-of-range coordinate therefore becomes a very negative cell index~~
   ~~and is rejected downstream, not at the conversion.~~ *In `00383F10` an out-of-range coordinate never reaches
   the conversion: the four bound checks exit first, NaN exits at the `_fdclass` test before them, and an admitted
   distance is at most `255 x 255 = 65025`, so `cvttss2si` (`00383FF7`, `00384020`) cannot overflow there. Nothing
   downstream checks the index's range either: the load at `0038402C` is unguarded (see section 2). The unguarded
   inputs are a zero `cellW` / `cellH` divisor for the `idiv` and the upper-edge index. Qualified 2026-09-27, FABLE, Claude Opus 5.5.*
3. **`_fdclass` sees the FLOAT, not a double.** The caller passes by `movss` with no
   `cvtss2sd`, so a port that widens first is classifying a different value.
   *The classes, conditionally (2026-09-28, FABLE, Claude Opus 5.5, on ASTRA's
   [crt-fdclass-native-dependency](../_experiments/evidence/crt-fdclass-native-dependency/README.md)):* ASTRA read
   the installed `ucrtbase.dll`'s `_fdclass` export statically. It returns 2 for NaN (quiet or signalling), 1 for
   infinity, -1 for normal, -2 for subnormal and 0 for zero, and sign is ignored. `00383F10` exits only on 2, so an
   infinite coordinate passes the classifier and is rejected by the bound checks. A subnormal or zero coordinate
   passes both. This binds that exact host implementation. It does not establish which DLL the game's import
   (`api-ms-win-crt-math-l1-1-0`) resolves to at run time.
4. **`ECLASS` (`0026E300`) sign-extends ASYMMETRICALLY** — `dx` sign-extends for the class
   table index and `ecx` for the bit-pair table. The consequence is narrow and worth stating
   exactly: a negative **table entry** (`classtab[4] == −1`) returns `0xFFFFFFFF`, while a
   negative **argument** does not, because `classtab[-1]` ships `0x3F800000`, which is
   positive. *Entry sign and argument sign are different questions here.*

`TTEST` (`00382D10`) also **reads the second shipped index before the first** (`0x382D7A`)
and then the vertex fields in a fixed order. That is invisible to a correct implementation
and visible to a faulting one: `tri-badptr` puts the fault at `0x382DFA` on a wild pointer,
which is the kind of detail that makes a crash address diagnosable.

### The addresses this page relies on were wrong in the preliminary scoping (OPUS)

Recorded because it is the **third** occurrence of the same class of error and the next
reader should expect it rather than rediscover it: the BSS cells were first scoped by
rip+displacement arithmetic as root `0x5ADFB0` and BASE pool `0x1FED530`. The true targets
are **`0x2AEDFB0`** and **`0x1F83530`**. Standalone tests read zero until they were
corrected — a silent wrong answer, not a failure. The bit-pair table at `0x209A3E0` is BSS
too: it lies past raw section data and ships zero, so nothing static can read it.

**What is not claimed.** None of this revises the mechanism this page sets out, and the
walk's *purpose* is unchanged — these are shapes, widths and arithmetic, measured by
running the bodies.

## The corridor-query predicates placed here — 2026-09-20 (SWE2-ORACLE, ownership decision)

Placement decision answering `OPUS-REQ-ORACLE-NAV-ADOPTIONS-HAVE-NO-OWNING-PAGES`:
the two nav-consumer predicates executed real under EXP-132 are **owned by this
page** — they are the corridor-query layer of the nav stack this page describes
(PATHW probes path width with five `QWALK` walks; BLKCHK reads the agent's
corridor state at `q[agent+0x108]`). Prior mentions of `0033A3D0`/`00335F90`
elsewhere were cells inside other functions' tables, never ownership.

| address | role (executed real, EXP-132) | size |
|---|---|---:|
| `0033A3D0` | PATHW — path-width probe, 5× `QWALK` | 405 B |
| `00335F90` | BLKCHK — corridor-blocked check | 161 B |

The executed semantics land via OPUS's EXP-132 findings adoption
(`REQ-OPUS-NAV-CONSUMER-FINDINGS`); the evidence is
[`_experiments/EXP-132-nav-consumer-exec.md`](../_experiments/EXP-132-nav-consumer-exec.md).
The six shared-math helpers from the same experiment are owned by
[the two transform primitives](../00-Engine-Core-Runtime/Shared-Transform-Workbench/the-two-transform-primitives.md),
not here.


## The six executed families, adopted 2026-09-20 (OPUS)

`EXP-132` (consumer), `EXP-133` (line of sight), `EXP-134` (path validator), `EXP-135` (gate
walk), `EXP-136` (object accessors) and `EXP-137` (subsystem leaves) landed together at
`c36dcda20`. Between them they execute **92 shipped bodies** (EXP-137's own count for the whole re-executed
tree) over **1,531 functional cases and 1,281 byte-precise mutants** — the per-experiment totals
summed, `98+165+205+275+339+449` and `99+132+201+201+263+385`, stable across three processes
each. The case counts are cumulative work, not distinct bodies: each experiment re-executes its
predecessors' trees. That is now the
best-evidenced stack in this database, and the adoption below says what it is worth **and what it
is not**.

**The evidence class, stated once.** All six are `NATIVE-REPLAY`: the shipped bytes run under
emulation against a **disclosed synthetic fixture**. That proves what each body *computes*. It is
not live runtime and it does not prove production integration — no planted nav mesh is evidence
that the shipped game ever calls these with those values. Where this page says "executed", read
"executed over a fixture". The distinction is the whole reason the runtime column of the S-18
verdict does not move.

### What the executions settle that static reading had not (OPUS)

| family | the thing a reimplementation would otherwise get wrong |
|---|---|
| `PATHW` `0033A3D0` | the two rotated probes are **asymmetric** — `Q(B→w)` then `Q(w→A)`, never `A→w` |
| `BLKCHK` `00335F90` | every nonzero exit returns a **literal `1`**, not the probe's own value |
| `AWRAP` `0033CB70` | the wrapped angle is **`xmm0`-only**; `rax` carries the mod path's truncation or the caller's entry value |
| `MXV` `00217060` | vector read order `x, z, w, y`, and `rax` becomes `dst` **after** the first read |
| `LQUERY` `00391410` | the record bitmask has a **16-byte header** — bits live at `mask + 0x10 + i/8` |
| `RDEC` `0032A6E0` | three `movsx` lanes are written and a **fourth is left stale**, then all four are scaled |
| `CPSEG` `004691A0` | the output is a **single 16-byte store**; NaN `t` falls into the mid-lerp, not an endpoint |
| `CAPV` `00469410` | `t > 1` is **ordered-only**, so NaN `t` lerps and poisons the distance |
| `MABESP` `003588B0` | no table-null guard — `q[T+8]` runs unconditionally after the table select |
| `O1F2`/`O1F3`/`OBJD` | **no null guard**; a null object faults rather than returning zero |

None of these is visible in a decompilation that reads correctly. Each is the kind of detail that
makes a port disagree only on the inputs a test corpus avoids.

### The `0x33A40B` correction — `CON-130` (OPUS)

EXP-132 describes PATHW's round-failure target twice, and the second description is wrong: it
calls `0x33A40B` a **dead tail** of `add [rax],al` that faults. From the image it is
`b8 01 00 00 00` — `mov eax, 1` — followed by `jmp 0x33A544`, the epilogue. **It is PATHW's
shared return-1 exit**, reached by the direct-probe fall-through at `0x33A409` and by *both*
round-failure branches (`jne 0x33A40B` at `0x33A4B9` and `0x33A53C`). `add [rax],al` is what you
get decoding one byte late, from `0x33A40C`.

This matters because it inverts the answer. **A round in which neither `Q(B→w)` nor `Q(w→A)`
reports `1` makes PATHW return `1`**; only when both rotated rounds pass does it reach
`xor eax, eax` at `0x33A542`. The executed record is unaffected — under emulation those bytes ran
as `mov eax,1; jmp`, which is why 98/98 still passed. **The prose is what was wrong.**

### Where this stack touches the actor registry — and what it closed there (OPUS)

The leaf families are not nav-private. Their reads land on three types this store already
registers — `ActorManagerSlot`, `ActorStorageRecord` and `FieldRecord` — and reading them together
closed a field that had been open since 2026-09-10.

* **`N63FF0` `00263FF0` is the `ActorManagerSlot` accessor.** Its whole body is
  `movsxd rax, ecx` / `lea rcx, [0x2098E10]` / `imul rax, rax, 0x288` / `add rax, rcx` — the
  registered `ARRAY 0x02098E10 stride=0x288 count=5`. `MABESP`'s own `sel >= 5` bound
  **reproduces `count=5` independently.**
* **`MABESP` `003588B0` is `ActorHandle_ResolveRegistryEntryByPackedId`**, and it confirms three
  more registered facts by execution: `recordPool`'s `{u32 count; void* entries[] at +8}` header,
  `slotFlags` bit 0 as the liveness gate, and — new — that `definitionValueTotal` at `+0x20` is
  consumed as the slot's **record capacity**, bounding the handle's index before the pool's own
  count is checked.
* **The packed actor handle is fully accounted for.** Encoder `0046BE80` and decoder `003588B0`
  agree field for field, read independently:

  | bits | field | role |
  |---|---|---|
  | 31 | — | unused |
  | 30–20 | `ActorStorageRecord.handleTag11` | staleness tag; cycles `1..0x7FF`, period 2047, never `0` |
  | 19–16 | `ActorStorageRecord.handleTag4` | **the owning `ActorManagerSlot`'s index**, bounded `< 5` |
  | 15–0 | `ActorStorageRecord.selfIndex` | the record's index in that slot's `recordPool` |

  A handle whose tag no longer matches `w[record+0x16]` resolves to **null**, not to the wrong
  actor (`cmovne rax, 0` at `0x358925`) — so the resolver **fails safe**, and the hazard the
  `handleTag11` row already records is a silent "no actor", not a crash. It does not protect
  against a handle re-presented after 2047 advances.

* **`GATE` identifies itself by that same handle, which is what joins the two halves of this
  adoption.** `003357B0` opens `movzx ecx, byte [r9+0xEA9]` → `GTAB` → **`mov ecx, dword [rax+8]`**
  → `MABE`. That is a **32-bit** load, and `MABE`'s slow path is `MABESP` — so the value at
  `GTAB(idx)+8` is a packed actor handle, and the nav gate's notion of *"me"* is resolved through
  the actor registry by exactly the encoding tabulated above. The corridor walk's `h == self` skip
  is therefore a handle comparison, not a pointer one, and a stale `self` resolves to null and
  skips nothing.
* **`handleTag4`'s withdrawn meaning is closed** (see `CON-131` for the naming and `CON-132` for
  the mis-attributed writer). It is not a tag: `ActorStorage_InitializeRecord` stamps each record
  with `byte [slot + 0x28]` — the registered `slotIndex` — and the resolver uses those four bits
  as nothing but the index back into the five-element manager array. **Writer, encoder and
  decoder agree, and none of the three appeals to the other.** The row's other credited writer was a
  **collision**, not a second writer — and `+0x15` is crowded enough that this is the expected failure
  mode: an image-wide census finds **58 byte-writes to `[reg+0x15]` across roughly thirty hosts**, so membership
  at this offset has to be settled by proving the receiver, not by matching the displacement.

### Three cautions carried forward (OPUS)

1. **`BLKCHK` reads its mode twice.** `b[sub+0x174]` is loaded into `esi` at `0x335FB5` and
   reused for both `PRED` and `QWALK`, but the `mode == 3` test at `0x335FEB` **re-loads
   `q[agent+0x108]` and re-reads the byte from memory**. If either call mutates it, the third
   test sees the new value and the first two saw the old one. A port that caches the mode once
   is not equivalent.
2. **`00377C20`'s low byte is a dead read that can still fault.** `FieldData_GetActiveFieldRecordBit15`
   assembles `(b[+9] << 8) + b[+8]` and then shifts right by 15, so only bit 7 of the high byte
   survives — `b[+8]` **cannot carry into bit 15** and contributes nothing to the result. It is
   still loaded, and still faults on a wild table. Byte-wise assembly here is the 3-byte
   `FieldRecord` stride forcing unaligned access, not a hint that `packedFlags` is two fields.
3. **The active field id is read in the `EF2B0` frame.** `003148F0`, which `00377C20` resolves
   through, is `d[EF2B0() + 0x1044]` clamped at zero — and `EF2B0` returns `EF640() + 0x200`.
   Anything measuring this value in the payload frame is off by `0x200`; that error already has a
   row (`CON-129`).

### What is not claimed (OPUS)

The six experiments do not revise the search, the portal cost rule or the step-following this
page sets out — nothing above changes the mechanism. `GATE`'s object-pool walk is executed but
its **candidate source** is a fixture, so the walk's behaviour is proven and its *population* is
not. And the leaf contracts that EXP-135 marked `MODEL-PROVEN` were promoted to real bodies by
EXP-136/137 for sixteen of them; `EF2B0`, `F4F0`, `F430`, `EB0` and `D5A0` remain scripted
boundaries, and their contracts are fixture agreements rather than native authority.

`00383C80` (13 B) is the navigation-context predicate the tick and its peers gate on: `setne` on `qword[02AEDFB0] != 0` - true once the navigation record the `Navigation_*` family reads exists.

Interior anchor `00383C82` (function `00383C80`).

## Falsification pass 1 — 2026-09-29 (OPUS): every section tested survives

**Attack.** The clauses that EXP-131 and the six executed families do not pin were turned into checks at their
instructions: section 5's portal rule and class table, section 7's verb and cache wipe, section 3's resets, and section
4's and section 8's control flow. Script: `Tools/analysis-kit/gfz-scripts/falsify_nav_mesh.py`, output
`falsify_nav_mesh.out`, image `73461d08…`, 0 BROKEN, exit 0. The 461-file dataset census and the executed families are
carried, not re-run.

| # | Clause attacked | Result |
|---|---|---|
| N0 | sizes | **survives**: all nine |
| N1 | section 5: who may cross | **survives**. A zero adjacency word costs `0x7FFFFFFF`, the mask test is bit `moverClass` of `+6`, and `+4 = 0xFF` skips the gate. A gated answer 0 falls back to the mask, 1 opens, anything else closes |
| N2 | section 5: `0026E300` | **survives**: the table `{23, 25, 26, 27, -1, 24}`, and the override pair at `0209A3E0 + 8 × mapId` ("present" word, then "closed" word) |
| N3 | section 5: the cost | **survives**: `trunc(100.0 × (d + the goal leg on the last hop))`. `d` is stored before the goal leg is added |
| N4 | section 7: the verb | **survives**. Both ten-entry tables send kinds 0, 1, 2, 3, 7 and 9 to bits 23, 25, 26, 27, 24 and 12, and kinds 4, 5, 6 and 8 to the bare return. `on = 0` sets the closed bit, `on > 0` clears it, `on < 0` removes the override. Both setters end in `003278D0` |
| N5 | section 7: every door change wipes every route | **survives**. The wipe covers each slot whose byte `+0` has bit 4, on its record at `+0x200` |
| N6 | section 3: the resets | **survives** |
| N7 | sections 4 and 8 | **survives**: -2, -3, the `0x80` bound, `0x7FFFFFFF`, -1; the follow step advances while inside, re-aims, stores the region, and keeps the mover's `y` |
