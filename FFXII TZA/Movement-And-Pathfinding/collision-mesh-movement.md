---
title: "Collision-mesh movement: how a body is swept across the collision polygons, pushed out of walls and kept off closed edges, and the point queries on the same mesh"
kind: "system"
category: "Movement and pathfinding"
addresses: "00380C40, 002327D0, 0022EF20, 00380A70, 0022D7E0, 0022E7D0, 0022E340, 00231E40, 002324F0, 0022F9B0, 0022F250, 00232760, 0022DE60, 0022EAC0, 00381D90, 003810B0, 00380E00, 00380EB0, 00231690, 00230C10, 003D97E0, 00232160, 00231890, 00231820, 00231900, 0026E350, 0026E3C0, 02088FE0, 020891F0, 02089280, 020892C0"
---

## What the player sees

A character who walks into a wall slides along it instead of stopping dead, and one who walks into a
corner is eased back out of it. Ground a gate has closed works the same way: the character slides
along the line where the closed ground starts. A big monster tests a wider patch of the map around
itself than a party member does, so it is held at the mouth of a passage it does not fit. Whatever
stands on the ground stands at the height of the collision polygon under it. The follow camera uses
the same mesh to keep from passing through walls.

## How it works

### The collision part and its cell lists

The collision part is the descriptor `0026E500(0)` returns for the bound map ([doors, gates and map
changes](../World-Areas-And-Travel/doors-gates-and-map-changes.md)); `00322220`, run at the area
initialisation `002342F0` and the map bind `0026E760`, keeps part 0 at `02EC1370` and part 2 (else 1,
else 0) at `02EC1378`. The fields the code on this page reads:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `GridHeader*` | grid | the cell grid's size |
| `+0x08` | `void*` | vertices | `0x10` bytes each |
| `+0x10` | `CollisionPolygon*` | polygons | `0x20` bytes each |
| `+0x18` | `void*` | wallRecords | `0x90`-byte shape records ([geometry primitives](geometry-primitives.md)) |
| `+0x20` | `u16*` | listIndex | four banks of `n + 1` list starts |
| `+0x28` | `u16*` | idPool | below `0x4000` a polygon, `0x4000`-`0x4FFF` a wall record, from `0x5000` a dynamic shape |
| `+0x38` | `i32` | originX | added to x before the column divide |
| `+0x3C` | `i32` | originZ | added to z before the row divide |
| `+0x40` | `i16` | n | the bank stride minus one |

`GridHeader`: `8` `i32` columns, `C` `i32` rows, `10` `i32` cell width, `14` `i32` cell height.
`CollisionPolygon`: `0` `f32[3]` normal, `C` `u32` attribute word, `10` `i16[3]` vertices, `16`
`i16[3]` the neighbour across each edge, `1C` `u32` flags (bit 10 ends contacts past the third edge).

A cell's list in bank `k` is the ids from `index[k (n + 1) + cell]` up to `index[k (n + 1) + cell +
1]`. The cell of a point is the staggered-grid lookup `00233050` ([geometry
primitives](geometry-primitives.md)). `0022F830(query)` runs the query's callback once per bank whose
bit is set in the query's mask byte `+0x16` (bits 0-3), each time with the list start at `+0x12` and
its count at `+0x14`. The floor searches (`00231900`, `00233110`) read bank 0 directly, the marker
search `00231A90` reads bank 3, and the sweep's penetration test reads bank 1, plus bank 0 for a
flier.

### The body's footprint frame

The record the sweep moves is the body's placement (the body's `+0x30`, [movement
bodies](movement-bodies-and-separation.md)); its stepped radii `+0x80` and `+0x84` are the
footprint. `0022EF20(placement)` builds the footprint frame at `02089280`: `00380A60` calls
`00380A70(placement, out, up)` with up `{0, 1, 0, 0}` from `00D22740`, which takes the x axis as
`(-[+0x10], 0, [+0x18])`, the z axis as the normalised cross product of x and up, x again as up
cross z, and the position `+0x00` as the translation.

`0022EF20` then zeroes the translation, keeps the rigid inverse (`00217610`) at `020892C0`, scales
the frame by the radii (x by `+0x80`, z by `+0x84`, each floored at 0.01) and the inverse by their
reciprocals. A point mapped through `020892C0` lands in a space where the footprint is the unit
circle; `02089280` maps a vector back.

### The sweep

`00380C40(placement, move)` is the entry, run by the body solver `003DB140` on the body's `+0x30`
and by the straight-walk test `00336AE0`. It resets the push vector `+0x40` to `{0, 0, 0, 1}` and
clears flag `+0x60` bit 4, and does nothing more without a collision part or for a move of 0.001
or less.

With a valid polygon at `+0x52` it runs the sweep `002327D0(part, placement, position, move,
polygon)`, stores the polygon it returns, stores the ground height (`00231890`) at `+0x7C` and into
the position's y unless flag `+0x60` bit 0 (a flier), and normalises `+0x40` (`00380800`) when bit
4 was raised. `003808A0` then refreshes the cell attributes.

`002327D0` cuts the move into sub-steps. With `rMin` and `rMax` the smaller and larger of the two
radii, a walker uses a sub-step of `0.8 * rMin` and a penetration ellipsoid whose vertical half-axis
is 0.1 and whose centre sits `max(0.1, rMax) / 2` above the position. A flier (flag bit 0) uses `h
= +0x6C / 2` as the half-axis and the centre offset, and `0.8 * min(rMin, h)` as the sub-step. The
horizontal half-axes are the frame's x axis times `+0x80` and its z axis times `+0x84`.

Each sub-step aims the centre at `position + unit(move) * min(step, remaining)` and runs these
stages:

1. Penetration rounds: the penetration query (below) runs on the centre's cell over bank 1, or
   banks 0 and 1 for a flier, with dynamic shapes included and, for a flier, the bit-26 walls. A body
   with a radius above 2.0 also floods the neighbouring cells (`0022E340`).
2. When the deepest penetration is above 0.01, the summed push (its vertical part dropped for a
   walker) is normalised, scaled by that depth and added to the centre and to `+0x40`, and flag bit
   4 is set. Up to four rounds run; a body with a radius above 2.0 runs one.
3. The polygon walk: `002324F0` names the edge of the current polygon the centre lies beyond. When
   there is one and its neighbour `+0x16` exists, is open to the body's kind byte `+0x50`
   (`00230A40`) and has not been visited in this sub-step (`02088FE0`, at most 128), the walk
   moves into it and repeats.
4. Otherwise `0022F9B0` keeps the footprint off the polygon's closed edges and `0022F250` off the
   vertices it collected, then the walk repeats; it ends when `0022F9B0` reports no contact or after
   four rounds of push-out.
5. The commit: when the centre ends inside the final polygon (`002324F0` = -1) the position takes
   the centre; otherwise this sub-step is dropped and the position stays.

The sweep returns the final polygon. A blocked sub-step is not retried shorter: the next one starts
from the same position along the same direction.

### Which edge a point is beyond

`002324F0(part, polygon, ctx)` takes the point at `ctx + 8` and, for each edge `(v[i], v[next i])`
with `next = {1, 2, 0}` (`00908DE8`), flattens the edge `e` and the offset `w = p - v[i]` to the
ground plane. An edge counts when the point is on its outer side (the y of `unit(e) x w` below
-0.0001) and `|e|` exceeds 0.0001. Of the edges that count it returns the one whose crossing
parameter `t = (w . unit(e)) / |e|` is nearest 0.5, the edge crossed nearest its middle, and -1 when
none counts: the point is inside, seen from above.

### Keeping the footprint off closed edges

`0022F9B0(part, placement, centre, polygon)` maps the polygon's three vertices through `020892C0`
and flattens them. For each edge it reads the neighbour across it, treating a neighbour closed to
the body's kind (`00230A40`) as none, and finds the closest point `c` of the edge to the flattened
centre in footprint space. When the centre is less than 1 from `c`:

- a closed edge whose closest point lies inside the edge pushes the centre directly away from `c`
  until it is a radius away, mapped back through `02089280`; the push is added to the centre and
  to `+0x40`, and flag bit 4 is set;
- a closed edge whose closest point is an end vertex records the vertex in `020891F0` (16 at most);
- an open edge leads into the neighbour, which is visited (`02088FE0`) and handled the same way.

It returns 1 when it handled any contact. `0022F250(centre)` then takes each recorded vertex, maps
`centre - vertex` through `020892C0` (this time with its height) and, when that is shorter than 1,
pushes the centre out to 1 along it, mapped back through `02089280`.

`00232760(part, placement)`, run when the placement's radii step in `003808A0`, uses the same
pieces on the standing position: `00233110` finds the polygon, `0022EF20` builds the frame,
`0022F9B0` and `0022F250` push the position off closed edges and vertices.

### The penetration test

The query is built on the caller's stack:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | callback | `0022D7E0`, or `0022DE60` for the camera |
| `+0x08` | `void*` | part | the collision part |
| `+0x10` | `i16` | cell | the cell being tested |
| `+0x12` | `i16` | listStart | written by `0022F830` |
| `+0x14` | `i16` | listCount | written by `0022F830` |
| `+0x16` | `u8` | bankMask | bits 0-3 select the banks |
| `+0x18` | `f32*` | axes | three `f32[4]` rows, the ellipsoid's half-axis vectors |
| `+0x20` | `f32*` | centre | the ellipsoid's centre |
| `+0x28` | `f32*` | push | the summed push, `f32[4]` |
| `+0x30` | `f32` | deepest | deepest penetration, -1.0 at start |
| `+0x34` | `i16` | deepestId | its id, `FFFF` none |
| `+0x36` | `i16` | kind | 2 or 3 from the sweep; neither callback reads it |
| `+0x38` | `i32` | dynamic | test ids from `0x5000` |
| `+0x3C` | `i32` | bit26Walls | test walls with attribute bit 26 |

For a direction `n`, the ellipsoid reaches `r(n) = sqrt((n . a0)^2 + (n . a1)^2 + (n . a2)^2)` from
its centre, with `a0`-`a2` the three rows. `0022D7E0(query)` walks the list:

- A polygon of any type other than 1 is tested; a type-1 polygon only when its wall-overridden
  attribute word is below `0x80000000` and its bit 26 is clear or `+0x3C` is set. The test takes the
  distance `d = (centre - v[0]) . n` to the polygon's plane and needs `0 < d < r(n)`.
- `0022E7D0` then gives the vector from the polygon to the centre: zero when the centre projects
  inside the face, else from the closest point of the first edge the centre lies outside. When that
  vector is longer than 0.001 and than `d`, its direction replaces `n` and its length `d`. With `d <
  r(n)`, `n * (r(n) - d)` is added to the push.
- A wall record (`0x4000`-`0x4FFF`) is tested when its wall-overridden word is below `0x80000000`
  and its bit 26 is clear or `+0x3C` is set: `00381D90` gives the contact normal and `003810B0` the
  distance, and a distance below `r(normal)` adds `normal * (r - distance)`.
- An id from `0x5000`, only with `+0x38` set, names entry `id - 0x5000` of the bound map's
  dynamic shapes (`[0209A670] + 0x1A0`, 0x10 bytes each), tested when its dword at `[map + 0x1D8] +
  0xC * index` is non-zero. `00230790` builds it as a cylinder shape record with attribute word 1,
  from sizes stored as 4.12 fixed point and a matrix from the map's table at `+0x188`, and it is then
  tested as a wall record.

Every hit whose depth is strictly greater than `+0x30` becomes the deepest, with its id at `+0x34`.
`0022E7D0` answers 0, skipping the polygon, when the centre lies outside the third edge (`v[2]` to
`v[0]`) and the polygon's flag word `+0x1C` has bit 10.

### Big bodies and the neighbouring cells

`0022E340(query, point, extent)` floods the cells a big body's box overlaps. The sweep hands it the
centre and, as the box's half-extents, the larger `|x|` and the larger `|z|` of the two horizontal
half-axes. For each of six neighbour points (the point moved by a full cell height in z, or by a
cell width in x and half a cell height in z, matching the staggered columns) it takes the cell, and
skips it when it is outside the grid, already in the visited list `02088FE0` or the list is full at
128.

Otherwise it records the cell, builds the cell's rectangle widened by 0.1 on each side
(`00231E40`), and, when the box reaches past that rectangle's near edges in z and x, runs the query
on the cell (`0022F830`) and floods on from the neighbour point.

### The camera's variant

`0022DE60(query)` is the same test as `0022D7E0` with three differences: the plane distance may be
as low as -0.001, ids from `0x5000` and the bit-26 rule are not tested, and its edge contact
`0022EAC0` points along the sum of the polygon's normal and, when the edge has a neighbour (the `i16` at
polygon `+0x16` is not negative), the normal of the polygon across that edge, rescaled to the contact's
length. A sphere therefore slides over a crease instead of catching on it; across an open edge the
push follows the polygon's own normal.

`00230C10(part, out, start, end, kind, radius)` is the camera's sphere sweep: a ray cast from start
to end (the walker `0022F430` with `0022CC50`) shortened to its hit, the `0022DE60` test with a
sphere of the radius at the end over banks 0-2 (kind `0x13`), two more ray casts offset by the
radius at -30 and +30 degrees about the line when the sphere touches, and a final push back toward
the start by the deepest penetration. `00230C00` forwards to it.

`00231690(part, push, id, axes, centre, kind, dynamic, placement)` runs `0022D7E0` once on the
centre's cell and returns the deepest penetration, with the push and the id written out; kind bit 0
selects banks 0-2, or banks 0-1 with the bit-26 walls when `dynamic` is set; a placement with a
radius above 2.0 adds the flood. `003D97E0` ray casts (`00230B60`), and on a hit takes the hit's
normal (`00232160`) and moves the hit point 0.1 along it; on a miss the normal is zero.

The follow camera (`0032AEC0`, reached from the mode-1 camera view `00259990`, [scripted
camera](../Graphics/scripted-camera.md)) is the caller of all three: `0032BCC0`,
`0032BEB0` and `0032CA70` use `00230C00`, `0032BCC0` and `0032CA70` use `00231690`, and `0032CF50`
uses `003D97E0`. `0032BCC0` counts a depth
between 0 and 0.27 as touching.

### Contact with a wall record

`00381D90(record, out, p)` maps `p` into the record's unit frame (`+0x50`) and takes the excess
over the unit shape with a 0.999 margin: a sphere's excess is the local point itself when it is
more than 0.999 from the centre, else zero; a cylinder's (`00380EB0`) is the radial part beyond
0.999 and the vertical part beyond `+-0.999`; a box's (`00380E00`) is each coordinate's part beyond
`+-0.999`. The excess is mapped back as a direction through `+0x10` and normalised (`00380800`), so a
point inside the shape gets a zero normal and no push.

`003810B0(record, p)` returns the distance from the shape in world units: the local point scaled by
`(|l| - 1) / |l|` for a sphere outside it, the radial and vertical parts beyond 1 for a cylinder,
and, for a box, the offset from the face the box segment test `00381450` finds along the excess
direction. The offset is mapped through `+0x10` as a direction and its length returned.

### Point queries

- `00231890(part, p, polygon)` is the height of the polygon's plane under `p`: `v[0].y + ((v[0].x -
  p.x) n.x + (v[0].z - p.z) n.z) / n.y`; with no polygon, or `n.y` at or below 0.001, it is `p.y`.
  `00231820` is the same, written into `p.y`.
- `00231900(part, p, typeMask)` is the highest polygon under `p`: of the bank-0 ids of `p`'s cell,
  the polygons with `n.y` above 0.001, a type (attribute bits 0-2) whose bit is set in `typeMask`,
  and `p` inside them seen from above (`002324F0` = -1), the one with the highest plane height wins;
  -1 without a part, a cell or a candidate.
- `0026E350(p)` drops `p` onto the highest type-0 polygon of the bound map (`00231900(..., 1)`, then
  `00231820`) and returns 0, or -1 when there is none.
- `0026E3C0(part, p)`, reached from the terrain probe `003208C0`, does the same and then raises a
  probe point from the floor by 1.0 at a time, up to 30 times, until the wall contact test
  `00232490` reports no contact; from there a ray cast (`00230B60`) down to the floor point replaces
  the height with the first hit.
- `00232160(part, out, id, p)` is the normal of a hit: a polygon's 16 bytes (normal and attribute
  word), a wall record's contact normal at `p` (`00381D90`); an id from `0x5000` leaves `out`
  alone. `00231F20` copies a polygon's 16 bytes the same way; `002FB560` uses it to tilt a model to
  the floor.
- `0022F050(part, polygon, p, out)` gives `p`'s barycentric weights in the polygon, seen from above:
  the areas of the three sub-triangles `p` forms with each edge, over their sum. The marker search
  `00231A90` uses them to blend the vertex colour bytes (times 1/128) of the type-2 polygon under a
  body into the placement's `+0x30`-`+0x3C`, or copies `0209A3A0` there when there is none.

## Layouts

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `f32[4]` | position | committed by the sweep |
| `+0x10` | `f32` | dirX | the footprint x axis is `(-dirX, 0, dirZ)` |
| `+0x18` | `f32` | dirZ | the pair's second part |
| `+0x40` | `f32[4]` | push | push of this move, normalised by `00380C40` |
| `+0x50` | `u8` | kind | the kind `00230A40` tests |
| `+0x52` | `i16` | polygon | polygon under the body |
| `+0x60` | `u32` | flags | bit 0 flier, bit 4 pushed this move |
| `+0x6C` | `f32` | height | a flier's ellipsoid |
| `+0x7C` | `f32` | groundHeight | plane height under the body |
| `+0x80` | `f32` | radiusA | stepped radius, the footprint's x |
| `+0x84` | `f32` | radiusB | stepped radius, the footprint's z |

| Address | Type | Name | Meaning |
|---|---|---|---|
| `02088FE0` | `i32[128]` | visited | cells (flood) or polygons (walk) already seen |
| `020891E0` | `i32` | visitedCount | entries in `visited` |
| `020891F0` | `void*[16]` | contactVertices | vertices met by the edge push-out |
| `020891E4` | `i32` | contactCount | entries in `contactVertices` |
| `02089280` | `f32[16]` | footprintFrame | the frame scaled by the radii |
| `020892C0` | `f32[16]` | footprintInverse | its inverse |
| `00908DE8` | `i32[3]` | nextVertex | `{1, 2, 0}` |
| `00D22740` | `f32[4]` | up | `{0, 1, 0, 1}`, w cleared on use |

## Operations

Per move of a body: the frame is built, the move is cut into sub-steps of 0.8 of the smaller
radius, and each sub-step is pushed out of walls, walked across the polygons it enters, kept off
closed edges and vertices, and committed only when its centre ends on a polygon. Then the ground
height is applied and the cell attributes refreshed. Per camera update: a sphere sweep, a
penetration query and a nudged ray cast on the same mesh.

## State

The body's placement (position, polygon, push vector and flags); the shared scratch of the sweep:
the visited list, the vertex list and the two footprint matrices, rebuilt on every call and shared
by every body.

## Modding notes

- A sub-step is either committed whole or dropped; a body pressed into a corner keeps its last
  committed position rather than creeping in by a fraction.
- The sub-step is 0.8 of the smaller radius, so a body with a tiny radius takes many sub-steps per
  move; a radius below 0.01 is treated as 0.01 by the frame.
- Bodies with a radius above 2.0 take one penetration round per sub-step instead of four but test
  every cell their box overlaps, up to 128 cells.
- A wall's push only acts on a point outside the shape: a body whose centre is already inside a
  wall record gets a zero normal and is not pushed out.
- The visited and vertex lists and the two matrices are globals; running the sweep for two bodies at
  once, or from a hook inside it, corrupts both.

## Related

- [Doors, gates and map changes](../World-Areas-And-Travel/doors-gates-and-map-changes.md): the
  attribute word, the override table, the kind test `00230A40` and the cell attributes.
- [Geometry primitives](geometry-primitives.md): the shape record, the unit primitives and the
  ray cast.
- [Movement bodies and separation](movement-bodies-and-separation.md): the body, its placement and
  the radius stepping.
- [Movement step](heading-speed-to-position-delta.md): the solver that hands the move in.
- [Scripted camera](../Graphics/scripted-camera.md): the camera records and the
  mode-1 view.
