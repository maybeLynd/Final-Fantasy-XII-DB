---
title: "Collision-mesh movement: how a body is swept across the collision polygons, pushed out of walls and kept off closed edges, and the point queries on the same mesh"
kind: "system"
category: "Movement and pathfinding"
addresses: "0x00380C40, 0x002327D0, 0x0022EF20, 0x00380A70, 0x0022D7E0, 0x0022E7D0, 0x0022E340, 0x00231E40, 0x002324F0, 0x0022F9B0, 0x0022F250, 0x00232760, 0x0022DE60, 0x0022EAC0, 0x00381D90, 0x003810B0, 0x00380E00, 0x00380EB0, 0x00231690, 0x00230C10, 0x003D97E0, 0x00232160, 0x00231890, 0x00231820, 0x00231900, 0x0026E350, 0x0026E3C0, 0x02088FE0, 0x020891F0, 0x02089280, 0x020892C0"
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

The collision part is the descriptor `0x0026E500(0)` returns for the bound map ([doors, gates and map
changes](../World-Areas-And-Travel/doors-gates-and-map-changes.md)); `0x00322220`, run at the area
initialisation `0x002342F0` and the map bind `0x0026E760`, keeps part 0 at `0x02EC1370` and part 2 (else 1,
else 0) at `0x02EC1378`. The fields the code on this page reads:

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
`i16[3]` the neighbour across each edge, `1C` `u32` flags (bit `0x400` ends contacts past the third edge).

A cell's list in bank `k` is the ids from `index[k (n + 1) + cell]` up to `index[k (n + 1) + cell +
1]`. The cell of a point is the staggered-grid lookup `0x00233050` ([geometry
primitives](geometry-primitives.md)). `0x0022F830(query)` runs the query's callback once per bank whose
bit is set in the query's mask byte `+0x16` (mask `0xF`), each time with the list start at `+0x12` and
its count at `+0x14`. The floor searches (`0x00231900`, `0x00233110`) read bank 0 directly, the marker
search `0x00231A90` reads bank 3, and the sweep's penetration test reads bank 1, plus bank 0 for a
flier.

### The body's footprint frame

The record the sweep moves is the body's placement (the body's `+0x30`, [movement
bodies](movement-bodies-and-separation.md)); its stepped radii `+0x80` and `+0x84` are the
footprint. `0x0022EF20(placement)` builds the footprint frame at `0x02089280`: `0x00380A60` calls
`0x00380A70(placement, out, up)` with up `{0, 1, 0, 1}` from `0x00D22740`, which takes the x axis as
`(-[+0x10], 0, [+0x18])`, the z axis as the normalised cross product of x and up, x again as up
cross z, and the position `+0x00` as the translation.

The y row is `up` with its w cleared (`0x00380AB9`-`0x00380ACA`), and rows 0 to 2 get w 0; the translation row takes
all four floats of the position, w included (`0x00380B51`-`0x00380B6A`). Nothing is tested: a direction pair of `(0,
0)` gives a zero cross product, a length of 0 and a reciprocal of infinity (`0x00380B0A`), so the z and x rows come
out NaN.

`0x0022EF20` then zeroes the translation, keeps the rigid inverse (`0x00217610`) at `0x020892C0`, scales
the frame by the radii (x by `+0x80`, z by `+0x84`, each floored at 0.01) and the inverse by their
reciprocals. A point mapped through `0x020892C0` lands in a space where the footprint is the unit
circle; `0x02089280` maps a vector back.

Before it builds the frame, `0x0022EF20` sets two words below it to 1. After `0x00380A70` has put the placement's position
in the frame's translation row (`0x00380B53`-`0x00380B6A`, the frame's address in `rdx` from `0x0022EF3B`), it zeroes that
row's x, y and z. The rigid inverse `0x00217610` (through `0x0022EF81`) and the scaling `0x00217150` (through `0x0022F00F`) are
the only code that reads the row, since the vector transform `0x00202B90` reads rows 0 to 2 only:

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02089270` | `u32` | 0 (zero-filled tail of `.data`) | set to 1 on every frame build | `0x0022EF20` (`0x0022EF42`) | no other RIP-relative, image-base-relative or address-forming reference names it |
| `0x02089274` | `u32` | 0 (zero-filled tail of `.data`) | set to 1 on every frame build | `0x0022EF20` (`0x0022EF4F`) | as for `0x02089270` |
| `0x020892B0` | `f32[2]` | 0 (zero-filled tail of `.data`) | the frame's translation x and y, `0x02089280 + 0x30`: 0 once the frame is built | `0x00380A70` (`0x00380B53`, `0x00380B59`, through `0x0022EF59`); `0x0022EF20`, 0 with one 8-byte store (`0x0022EF65`); `0x00217150` (`0x002175FB`, the whole row, through `0x0022F00F`) | `0x00217610` (`0x00217633`, the whole row, through `0x0022EF81`); `0x00217150` (`0x0021744C`, `0x00217454`, through `0x0022F00F`) |
| `0x020892B8` | `f32` | 0 (zero-filled tail of `.data`) | the frame's translation z, `0x02089280 + 0x38`: 0 once the frame is built | `0x00380A70` (`0x00380B5F`, through `0x0022EF59`); `0x0022EF20`, 0 (`0x0022EF77`); `0x00217150` (`0x002175FB`, through `0x0022F00F`) | `0x00217610` (`0x00217633`, through `0x0022EF81`); `0x00217150` (`0x00217459`, through `0x0022F00F`) |

### The sweep

`0x00380C40(placement, move)` is the entry, run by the body solver `0x003DB140` on the body's `+0x30`
and by the straight-walk test `0x00336AE0`. It resets the push vector `+0x40` to `{0, 0, 0, 1}` and
clears flag `+0x60` bit `0x10`, and does nothing more without a collision part or for a move of 0.001
or less.

With a valid polygon at `+0x52` it runs the sweep `0x002327D0(part, placement, position, move,
polygon)`, stores the polygon it returns, stores the ground height (`0x00231890`) at `+0x7C` and into
the position's y unless flag `+0x60` bit `0x1` (a flier), and normalises `+0x40` (`0x00380800`) when bit
`0x10` was raised. `0x003808A0` then refreshes the cell attributes.

The collision part is `0x0026E500(0)` (`0x00380C5C`), and the push reset writes all 16 bytes `{0, 0, 0, 1}`
(`0x00380C64`-`0x00380C71`). The move's length is taken in three dimensions, y included, and a NaN length also ends
the call (`0x00380C81`-`0x00380CB0`). The polygon test is signed: with `+0x52` negative the sweep, the height and the
normalisation are skipped and `0x003808A0` still runs (`0x00380CB9`-`0x00380D0D`).

`0x002327D0` cuts the move into sub-steps. With `rMin` and `rMax` the smaller and larger of the two
radii, a walker uses a sub-step of `0.8 * rMin` and a penetration ellipsoid whose vertical half-axis
is 0.1 and whose centre sits `max(0.1, rMax) / 2` above the position. A flier (flag bit `0x1`) uses `h
= +0x6C / 2` as the half-axis and the centre offset, and `0.8 * min(rMin, h)` as the sub-step. The
horizontal half-axes are the frame's x axis times `+0x80` and its z axis times `+0x84`.

Each sub-step aims the centre at `position + unit(move) * min(step, remaining)` and runs these
stages:

1. Penetration rounds: the penetration query (below) runs on the centre's cell over bank 1, or
   banks 0 and 1 for a flier, with dynamic shapes included and, for a flier, the bit `0x4000000` walls. A body
   with a radius above 2.0 also floods the neighbouring cells (`0x0022E340`).
2. When the deepest penetration is above 0.01, the summed push (its vertical part dropped for a
   walker) is normalised, scaled by that depth and added to the centre and to `+0x40`, and flag bit
   `0x10` is set. Up to four rounds run; a body with a radius above 2.0 runs one.
3. The polygon walk: `0x002324F0` names the edge of the current polygon the centre lies beyond. When
   there is one and its neighbour `+0x16` exists, is open to the body's kind byte `+0x50`
   (`0x00230A40`) and has not been visited in this sub-step (`0x02088FE0`, at most 128), the walk
   moves into it and repeats.
4. Otherwise `0x0022F9B0` keeps the footprint off the polygon's closed edges and `0x0022F250` off the
   vertices it collected, then the walk repeats; it ends when `0x0022F9B0` reports no contact or after
   four rounds of push-out.
5. The commit: when the centre ends inside the final polygon (`0x002324F0` = -1) the position takes
   the centre; otherwise this sub-step is dropped and the position stays.

The sweep returns the final polygon. A blocked sub-step is not retried shorter: the next one starts
from the same position along the same direction.

### Which edge a point is beyond

`0x002324F0(part, polygon, ctx)` takes the point at `ctx + 8` and, for each edge `(v[i], v[next i])`
with `next = {1, 2, 0}` (`0x00908DE8`), flattens the edge `e` and the offset `w = p - v[i]` to the
ground plane. An edge counts when the point is on its outer side (the y of `unit(e) x w` below
-0.0001) and `|e|` exceeds 0.0001. Of the edges that count it returns the one whose crossing
parameter `t = (w . unit(e)) / |e|` is nearest 0.5, the edge crossed nearest its middle, and -1 when
no edge counts: the point is inside, seen from above.

It writes its working values into `ctx`: the two vertex pointers at `+0x10` and `+0x18`, `w` at `+0x20`, `unit(e)`
at `+0x30` with `|e|` at `+0x3C`, and the cross product at `+0x50` (`0x002325AC`-`0x0023268A`), so `ctx` spans at
least `0x60` bytes and holds the last edge's values on return. An edge replaces the one held only when strictly
nearer 0.5, so of two equally near the lower edge index wins (`0x002326A2`-`0x002326F0`).

### Keeping the footprint off closed edges

`0x0022F9B0(part, placement, centre, polygon)` maps the polygon's three vertices through `0x020892C0`
and flattens them. For each edge it reads the neighbour across it, treating a neighbour closed to
the body's kind (`0x00230A40`) as no neighbour, and finds the closest point `c` of the edge to the flattened
centre in footprint space. When the centre is less than 1 from `c`:

- a closed edge whose closest point lies inside the edge pushes the centre directly away from `c`
  until it is a radius away, mapped back through `0x02089280`; the push is added to the centre and
  to `+0x40`, and flag bit `0x10` is set;
- a closed edge whose closest point is an end vertex records the vertex in `0x020891F0` (16 at most);
- an open edge leads into the neighbour, which is visited (`0x02088FE0`) and handled the same way.

It returns 1 when it handled any contact. `0x0022F250(centre)` then takes each recorded vertex, maps
`centre - vertex` through `0x020892C0` (this time with its height) and, when that is shorter than 1,
pushes the centre out to 1 along it, mapped back through `0x02089280`.

`0x0022F250` walks the list while its index is below `0x020891E4` (`0x0022F273`, `0x0022F3DF`) and applies each push to
the centre before it takes the next vertex, so later vertices see the moved centre. The offset gets w 1.0 before
the mapping (`0x0022F2EC`), and the push goes to the centre's x, y and z only (`0x0022F3AB`-`0x0022F3D4`): unlike the
edge push-out it adds nothing to `+0x40` and sets no flag. A centre exactly on a vertex has a mapped length of 0,
whose reciprocal (`0x0022F341`) makes the push NaN.

`0x00232760(part, placement, cell, point)`, run when the placement's radii step in `0x003808A0`, uses the same
pieces on the standing position: `0x00233110` finds the polygon, `0x0022EF20` builds the frame,
`0x0022F9B0` and `0x0022F250` push the position off closed edges and vertices.

It reads only `part` and `placement`. The cell and the point stay in `r8` and `r9` as the caller left them and
reach `0x00233110` that way (`0x00232770`); the caller passes the cell `0x00233050` gave and the placement as the
point (`0x00380A10`-`0x00380A1F`). `0x00233110` stores -1 at `+0x52` first (`0x00233135`), and with `+0x52` still
negative the visited list is left empty (`0x00232790`) and `0x0022F9B0` runs all the same (`0x002327B1`).

It runs one round of each, with no walk and no penetration test: it empties the visited list and seeds it with the
polygon `+0x52` when that is not negative, empties the vertex list (`0x00232782`-`0x002327A2`), calls `0x0022F9B0(part,
placement, placement, polygon)` with the position `+0x00` as the centre and ignores its result
(`0x002327A8`-`0x002327B1`), and tail-jumps to `0x0022F250(placement)` (`0x002327C3`). Its only call site is `0x00380A22` in
`0x003808A0`.

### The penetration test

The query is built on the caller's stack:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | callback | `0x0022D7E0`, or `0x0022DE60` for the camera |
| `+0x08` | `void*` | part | the collision part |
| `+0x10` | `i16` | cell | the cell being tested |
| `+0x12` | `i16` | listStart | written by `0x0022F830` |
| `+0x14` | `i16` | listCount | written by `0x0022F830` |
| `+0x16` | `u8` | bankMask | the bits under mask `0xF` select the banks |
| `+0x18` | `f32*` | axes | three `f32[4]` rows, the ellipsoid's half-axis vectors |
| `+0x20` | `f32*` | centre | the ellipsoid's centre |
| `+0x28` | `f32*` | push | the summed push, `f32[4]` |
| `+0x30` | `f32` | deepest | deepest penetration, -1.0 at start |
| `+0x34` | `i16` | deepestId | its id, `FFFF` when nothing was hit |
| `+0x36` | `i16` | kind | a word `0x00231690` stores from one of its stack arguments (`0x002316F0`, `0x00231708`); neither callback reads it |
| `+0x38` | `i32` | dynamic | test ids from `0x5000` |
| `+0x3C` | `i32` | bit26Walls | test walls with attribute bit `0x4000000` |

For a direction `n`, the ellipsoid reaches `r(n) = sqrt((n . a0)^2 + (n . a1)^2 + (n . a2)^2)` from
its centre, with `a0`-`a2` the three rows. `0x0022D7E0(query)` walks the list:

- A polygon of any type other than 1 is tested; a type-1 polygon only when its wall-overridden
  attribute word is below `0x80000000` and its bit `0x4000000` is clear or `+0x3C` is set. The test takes the
  distance `d = (centre - v[0]) . n` to the polygon's plane and needs `0 < d < r(n)`.
- `0x0022E7D0` then gives the vector from the polygon to the centre: zero when the centre projects
  inside the face, else from the closest point of the first edge the centre lies outside. When that
  vector is longer than 0.001 and than `d`, its direction replaces `n` and its length `d`. With `d <
  r(n)`, `n * (r(n) - d)` is added to the push.
- A wall record (`0x4000`-`0x4FFF`) is tested when its wall-overridden word is below `0x80000000`
  and its bit `0x4000000` is clear or `+0x3C` is set: `0x00381D90` gives the contact normal and `0x003810B0` the
  distance, and a distance below `r(normal)` adds `normal * (r - distance)`.
- An id from `0x5000`, only with `+0x38` set, names entry `id - 0x5000` of the bound map's
  dynamic shapes (`[0x0209A670] + 0x1A0`, 0x10 bytes each), tested when its dword at `[map + 0x1D8] +
  0xC * index` is non-zero. `0x00230790` builds it as a cylinder shape record with attribute word 1,
  from sizes stored as 4.12 fixed point and a matrix from the map's table at `+0x188`, and it is then
  tested as a wall record.

Every hit whose depth is strictly greater than `+0x30` becomes the deepest, with its id at `+0x34`.
`0x0022E7D0` answers 0, skipping the polygon, when the centre lies outside the third edge (`v[2]` to
`v[0]`) and the polygon's flag word `+0x1C` has bit `0x400`.

### Big bodies and the neighbouring cells

`0x0022E340(query, point, extent)` floods the cells a big body's box overlaps. The sweep hands it the
centre and, as the box's half-extents, the larger `|x|` and the larger `|z|` of the two horizontal
half-axes. For each of six neighbour points (the point moved by a full cell height in z, or by a
cell width in x and half a cell height in z, matching the staggered columns) it takes the cell, and
skips it when it is outside the grid, already in the visited list `0x02088FE0` or the list is full at
128.

Otherwise it records the cell, builds the cell's rectangle widened by 0.1 on each side
(`0x00231E40`), and, when the box reaches past that rectangle's near edges in z and x, runs the query
on the cell (`0x0022F830`) and floods on from the neighbour point.

`0x00231E40(part, out, cell)` writes the rectangle as two points: column `cell % columns` and row `cell / columns`
(signed, `0x00231E4D`) give the corner `x = column * width - originX`, `z = row * height - originZ`, with half a
cell height (`height / 2`, rounded toward 0) added to z in an odd column (`0x00231E91`-`0x00231EAA`). `out` gets `{x -
0.1, 0, z - 0.1, 1}` and `out + 0x10` gets `{x + width + 0.1, 0, z + height + 0.1, 1}` (`0x00231EB0`-`0x00231F10`).

### The camera's variant

`0x0022DE60(query)` is the same test as `0x0022D7E0` with three differences: the plane distance may be
as low as -0.001, ids from `0x5000` and the bit `0x4000000` rule are not tested, and its edge contact
`0x0022EAC0` points along the sum of the polygon's normal and, when the edge has a neighbour (the `i16` at
polygon `+0x16` is not negative), the normal of the polygon across that edge, rescaled to the contact's
length. A sphere therefore slides over a crease instead of catching on it; across an open edge the
push follows the polygon's own normal.

`0x00230C10(part, out, start, end, kind, radius)` is the camera's sphere sweep: a ray cast from start
to end (the walker `0x0022F430` with `0x0022CC50`) shortened to its hit, the `0x0022DE60` test with a
sphere of the radius at the end over banks 0-2 (kind `0x13`), two more ray casts offset by the
radius at -30 and +30 degrees about the line when the sphere touches, and a final push back toward
the start by the deepest penetration. `0x00230C00` forwards to it.

`0x00231690(part, push, id, axes, centre, kind, dynamic, placement)` runs `0x0022D7E0` once on the
centre's cell and returns the deepest penetration, with the push and the id written out; kind bit `0x1`
selects banks 0-2, or banks 0-1 with the bit `0x4000000` walls when `dynamic` is set; a placement with a
radius above 2.0 adds the flood. `0x003D97E0` ray casts (`0x00230B60`), and on a hit takes the hit's
normal (`0x00232160`) and moves the hit point 0.1 along it; on a miss the normal is zero.

Without kind bit `0x1` the query takes bank 1 alone (mask 2, `0x002316F8`); `dynamic` goes to the query's `+0x38`
whatever the kind, so ids from `0x5000` are tested whenever it is non-zero (`0x0023170C`). The push is reset to `{0,
0, 0, 1}` before the query (`0x00231730`-`0x00231737`); with nothing hit the deepest is -1.0 and the id `0xFFFF`
(`0x002316D7`-`0x002316F3`, `0x002317F1`-`0x002317FA`).

The flood test reads the placement's radii `+0x80` and `+0x84` with no null test (`0x00231743`-`0x00231767`). The
flood's half-extents are the larger `|x|` and the larger `|z|` of axis rows 0 and 2 (`0x0023176D`-`0x002317C8`); the
visited list is emptied and seeded with the centre's cell when that is not negative (`0x0023177D`-`0x002317D7`).

`0x003D97E0(part, hit, normal, aux, start, end, kind)` calls `0x00230B60(part, hit, start, end, kind, 0)`
(`0x003D97F8`-`0x003D9829`) and returns the id it gives. The normal is taken at `start`, not at the hit point
(`0x003D983A`), which is where a wall record's contact normal is measured; an id from `0x5000` leaves the normal as
the caller had it. The move is the normal times `0.1 / |normal|` (`0x003D9861`-`0x003D98E6`).

On a miss (a negative id) the normal is `{0, 0, 0, 1}` and the 16 bytes at `aux` are zeroed
(`0x003D98F4`-`0x003D9905`); a hit leaves `aux` alone. The follow camera's `0x0032CF50` passes kind 4 (`0x0032CF9B`).

The follow camera (`0x0032AEC0`, reached from the mode-1 camera view `0x00259990`, [scripted
camera](../Graphics/scripted-camera.md)) is the caller of all three: `0x0032BCC0`,
`0x0032BEB0` and `0x0032CA70` use `0x00230C00`, `0x0032BCC0` and `0x0032CA70` use `0x00231690`, and `0x0032CF50`
uses `0x003D97E0`. `0x0032BCC0` counts a depth
between 0 and 0.27 as touching.

### Contact with a wall record

`0x00381D90(record, out, p)` maps `p` into the record's unit frame (`+0x50`) and takes the excess
over the unit shape with a 0.999 margin: a sphere's excess is the local point itself when it is
more than 0.999 from the centre, else zero; a cylinder's (`0x00380EB0`) is the radial part beyond
0.999 and the vertical part beyond `+-0.999`; a box's (`0x00380E00`) is each coordinate's part beyond
`+-0.999`. The excess is mapped back as a direction through `+0x10` and normalised (`0x00380800`), so a
point inside the shape gets a zero normal and no push.

The shape is the record's dword `+0x00`: 0 sphere, 1 cylinder, 2 box (`0x00381DBB`-`0x00381DEB`). Any other value
takes no excess and leaves `out` as the caller passed it, and that is then mapped and normalised like an excess
(`0x00381DCB`). The map into the frame uses all four floats of `p`, w included (`0x00381DB6`); before the map back the
excess's w is set to 0 (`0x00381E82`), and `0x00380800` gives a zero vector for a length below `1e-6`
(`0x0038083F`-`0x0038084C`).

`0x003810B0(record, p)` returns the distance from the shape in world units: the local point scaled by
`(|l| - 1) / |l|` for a sphere outside it, the radial and vertical parts beyond 1 for a cylinder,
and, for a box, the offset from the face the box segment test `0x00381450` finds along the excess
direction. The offset is mapped through `+0x10` as a direction and its length returned.

### Point queries

- `0x00231890(part, p, polygon)` is the height of the polygon's plane under `p`: `v[0].y + ((v[0].x -
  p.x) n.x + (v[0].z - p.z) n.z) / n.y`; with no polygon, or `n.y` at or below 0.001 or NaN, it is `p.y`
  (`0x00231899`, `0x002318C0`).
  `0x00231820` is the same, written into `p.y`.
- `0x00231900(part, p, typeMask)` is the highest polygon under `p`: of the bank-0 ids of `p`'s cell,
  the polygons with `n.y` above 0.001, a type (attribute bits `0x7`) whose bit value `1 << type` is set in
  `typeMask` (`bt`, `0x002319EB`), and `p` inside them seen from above (`0x002324F0` = -1), the one with the
  highest plane height wins; -1 without a part, a cell or a candidate.
- Without a part means a null grid pointer `[part]` (`0x00231926`); an empty list also gives -1 (`0x00231978`). The
  first candidate is taken whatever its height and a later one only when strictly higher, so of equal heights the
  first in the list wins (`0x00231A14`-`0x00231A1E`).
- The id test against `0x4000` is signed (`0x002319C9`): an id of `0x8000` or more is read as a polygon at a
  negative index. The id comes back zero-extended, -1 as `0xFFFF` (`0x00231A36`).
- `0x0026E350(p)` drops `p` onto the highest type-0 polygon of the bound map (`0x00231900(..., 1)`, then
  `0x00231820`) and returns 0, or -1 when there is no such polygon.
- `0x0026E350` also returns -1, leaving `p` as it was, when no map is bound (`[0x0209A670]` null, `0x0026E361`) or the
  map has no collision part (`[0x0209A678]` null, `0x0026E372`); the part it searches is `[0x0209A678]`.
- `0x0026E3C0(part, p)`, reached from the terrain probe `0x003208C0`, drops `p` the same way and then raises a
  probe point from the floor by 1.0 at a time, up to 30 times, until the wall contact test
  `0x00232490` reports no contact; from there a ray cast (`0x00230B60`) down to the floor point replaces
  the height with the first hit.
- `0x0026E3C0` searches the part it is given and tests no bound map. It returns the polygon id that `0x00231900`
  found, zero-extended, not 0, and `0xFFFF` with `p` left as it was when no polygon qualifies (`0x0026E3EB`,
  `0x0026E490`, `0x0026E4F4`).
- The first test is at the floor plus 1.0, `probe.y = h + 1.0` with `h` the floor height `0x00231890` returns,
  which `0x0026E3C0` stores in `p.y` (`0x0026E40E`-`0x0026E41E`), through `0x00232490(part, probe, 1)`
  (`0x0026E460`-`0x0026E478`). Each later test raises it again, `probe.y += 1.0` (`addss xmm2, xmm6`, `0x0026E460`).
- When all 30 raised points report contact (`cmp ebx, 0x1e`, `0x0026E483`), `0x0026E3C0` returns with `p.y` at the floor
  height and casts no ray. The ray is `0x00230B60(part, hit, probe, floor point, 0xFFFF, 0)`; with `r >= 0` for its
  result `r` it sets `p.y` to the hit's y (`0x0026E4B8`-`0x0026E4DA`, `0x0026E4DF`-`0x0026E4ED`), so a miss,
  `r < 0`, also keeps the floor height.
- `0x00232160(part, out, id, p)` is the normal of a hit: a polygon's 16 bytes (normal and attribute
  word), a wall record's contact normal at `p` (`0x00381D90`); an id from `0x5000` leaves `out`
  alone. `0x00231F20` copies a polygon's 16 bytes the same way; `0x002FB560` uses it to tilt a model to
  the floor.
- The id tests in `0x00232160` are signed 16-bit (`0x0023216B`, `0x00232176`): `0x4000`-`0x4FFF` tail-jumps to
  `0x00381D90(wallRecords + (id - 0x4000) * 0x90, out, p)` (`0x0023217C`-`0x00232193`), and an id below `0x4000`,
  `0x8000`-`0xFFFF` included as negative values, copies the 16 bytes of polygon `id` (`0x00232198`-`0x002321BE`).
- `0x0022F050(part, polygon, p, out)` gives `p`'s barycentric weights in the polygon, seen from above:
  the areas of the three sub-triangles `p` forms with each edge, over their sum. The marker search
  `0x00231A90` uses them to blend the vertex colour bytes (times 1/128) of the type-2 polygon under a
  body into the placement's `+0x30`-`+0x3C`, or copies `0x0209A3A0` there when there is no such polygon.

## Layouts

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `f32[4]` | position | committed by the sweep |
| `+0x10` | `f32` | dirX | the footprint x axis is `(-dirX, 0, dirZ)` |
| `+0x18` | `f32` | dirZ | the pair's second part |
| `+0x40` | `f32[4]` | push | push of this move, normalised by `0x00380C40` |
| `+0x50` | `u16` | kind | the kind `0x00230A40` tests, read as a zero-extended word (`0x0022FB1F`, `0x00232EAE`, `0x002331B5`); `0xFFFF` at set-up (`0x00380B97`) |
| `+0x52` | `i16` | polygon | polygon under the body |
| `+0x60` | `u32` | flags | bit `0x1` flier, bit `0x10` pushed this move |
| `+0x6C` | `f32` | height | a flier's ellipsoid |
| `+0x7C` | `f32` | groundHeight | plane height under the body |
| `+0x80` | `f32` | radiusA | stepped radius, the footprint's x |
| `+0x84` | `f32` | radiusB | stepped radius, the footprint's z |

| Address | Type | Name | Meaning |
|---|---|---|---|
| `0x02088FE0` | `i32[128]` | visited | cells (flood) or polygons (walk) already seen |
| `0x020891E0` | `i32` | visitedCount | entries in `visited` |
| `0x020891F0` | `void*[16]` | contactVertices | vertices met by the edge push-out |
| `0x020891E4` | `i32` | contactCount | entries in `contactVertices` |
| `0x02089280` | `f32[16]` | footprintFrame | the frame scaled by the radii |
| `0x020892C0` | `f32[16]` | footprintInverse | its inverse |
| `0x00908DE8` | `i32[3]` | nextVertex | `{1, 2, 0}` |
| `0x00D22740` | `f32[4]` | up | `{0, 1, 0, 1}`, w cleared on use |

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
  attribute word, the override table, the kind test `0x00230A40` and the cell attributes.
- [Geometry primitives](geometry-primitives.md): the shape record, the unit primitives and the
  ray cast.
- [Movement bodies and separation](movement-bodies-and-separation.md): the body, its placement and
  the radius stepping.
- [Movement step](heading-speed-to-position-delta.md): the solver that hands the move in.
- [Scripted camera](../Graphics/scripted-camera.md): the camera records and the
  mode-1 view.
