---
title: "Geometry primitives: the unit sphere, cylinder and box tests behind collision, the collision-mesh ray cast that uses them, and the volume clamps"
kind: "system"
category: "Movement and pathfinding"
addresses: "0x00380FA0, 0x00381AC0, 0x00381630, 0x00381450, 0x00381EB0, 0x00382020, 0x0046BF60, 0x0046BFA0, 0x0022E6D0, 0x0022CF50, 0x0022D4B0, 0x0022F430, 0x002315E0, 0x0022F8B0, 0x00233050, 0x0022D0D0, 0x00202E10, 0x00202B70, 0x00361DE0, 0x003623C0, 0x00363FD0, 0x00362230, 0x003631B0, 0x0025A8E0, 0x0025C830, 0x0046DB50, 0x0036DD80, 0x0036DD90, 0x0036DDA0"
---

## What the player sees

A character stopping at a wall, a thrown line of sight that a pillar blocks, a sound that seems to
come from the edge of a courtyard, a script trigger that fires when the party steps into a marked
rectangle: underneath, a handful of small questions are being answered. Does this segment cross
this shape, is this point inside it, where on this area is the point nearest to me. The bodies on
this page are those answers. Nothing on screen names them; when one is wrong the symptom is a
walker that hugs a wall it should clear or a trigger that fires a step early.

## How it works

### The shape record and the segment test

Collision shapes are unit solids in their own frame: a unit sphere, a unit cylinder of radius 1 and
height 2, or a unit cube of half-extent 1. A shape record holds its type at `+0x00` (0 sphere, 1
cylinder, 2 box), a forward transform at `+0x10` and its inverse at `+0x50`; size, position and
orientation live only in the transform pair. The collision mesh's wall records are such shapes
(0x90 bytes each, [doors and gates](../World-Areas-And-Travel/doors-gates-and-map-changes.md)).

`0x00380FA0(out, shape, A, B)` solves a segment against a shape: `A` and then `B` are mapped into the
shape's frame through the inverse at `+0x50` (`0x00202B70`), the type picks a primitive below, and a
type other than 0, 1 or 2 (tested after both points are mapped), or a primitive that reports no
hit, returns -1.0. A hit is mapped back
through `+0x10` into `out`, and the return value is the three-dimensional distance from `A` to
`out`. Each primitive takes `(out, A, B)` in the unit frame, writes `out` with `B`'s `w`, and
returns 1 for a hit.

### The three unit primitives

The sphere, `0x00381AC0`: with `d = B - A`, `L = |d|` and `u = d / L` (zero when `L < 1e-6`), the
closest point of the line to the origin is `P = A + t u` with `t = -A . u`. A hit needs `|A| < 1`,
or `|B| < 1`, or `|P| <= 1` with `0 <= t / L <= 1`; then `h = sin(acos(|P|))` and the point is
`P - u h`, the segment's entry into the sphere.

The cylinder, `0x00381630`, tests the caps first. With `A.y > 1` it returns 0 outright when `B.y >= 1`;
otherwise `t = -L (A.y - 1) / d.y` (`0x0046BFA0` against the top plane `0x00D11280`), and when
`0 < t < L` and the point `A + d t / L` lies within radius 1 of the axis that point is the hit.
`A.y < -1` mirrors this with the bottom plane `0x00D11290` and `B.y <= -1`. A cap miss falls through
to the side.

The side solve projects everything onto the ground plane: `Axz = (A.x, 0, A.z)`, `dxz = (d.x, 0,
d.z)`, `m = |dxz|`, `u = dxz / m`, `t = -Axz . u`, `P = Axz + t u`. The side counts when
`0x00382020(A)` or `0x00382020(B)` says an endpoint is inside, or `|P| <= 1` with `0 <= t / m <= 1`;
then `s = (t - sin(acos(|P|))) / m` and the point is `A + d s` along the full direction, accepted
only when its `y` lies in `[-1, 1]`.

The box, `0x00381450`, runs the six faces of the unit cube from the table at `0x00D11200` in order, each
a plane `{n, 1}` used as both normal and point. For a face `t = -L ((A - n) . n) / (d . n)`; when
`-0.001 < t` and `t` is below the best so far (initially `L`), the point `A + d t / L` is accepted
when each of its coordinates lies within 1.001 of the face normal's matching component, and it
becomes the new best. The nearest accepted face is the hit.

`0x0046BF60(p, n, q)` is `(p - q) . n`; `0x0046BFA0(A, d, n, p)` is `-|d| ((A - p) . n) / (d . n)`, the
distance along the segment to the plane through `p` with normal `n`. `0x00382020(p)` is 1 when
`-1 < p.y < 1` and `sqrt(p.x^2 + p.z^2) < 1`; `0x0046DB50` reuses it on the records of the list
`0x003DAE20` returns, the body placements linked each frame by `0x003DB0D0` (heading at
`+0x10`/`+0x18`, the inner shape's radii at `+0x70`/`+0x74` and height at `+0x78`), to find the
highest record top above a point.

### Point in shape

`0x00381EB0(shape, p)` maps `p` through the inverse and tests membership strictly: type 0 `|local| <
1`; type 1 `-1 < y < 1` and `sqrt(x^2 + z^2) < 1`; type 2 every coordinate in `(-1, 1)`; any other
type is outside. Its one caller is `0x0022F8B0`, the per-cell wall contact test of the collision
walker: for each id in the cell's list that names a wall record (`0x4000` to `0x4FFF`), and, when
the query's `+0x24` is set, whose effective attribute word has bit `0x80000000` clear, it tests the point at
the query's `+0x18` and raises the query's `+0x20` on the first hit.

### The polygon predicates

Collision polygons are 0x20-byte records at the mesh part's `[+0x10]`: a plane normal at `+0x00`,
the attribute word at `+0x0C` and three vertex indices at `+0x10`, `+0x12`, `+0x14` into the
0x10-byte vertices at `[+0x08]`. `0x0022E6D0(A, d, {polygon, vertex})` returns `-|d| ((A - vertex) .
n) / (d . n)`, the distance along the segment to the polygon's plane, through the vertex the
caller hands it.

`0x0022CF50(part, id, p)` is the winding test: for each edge `(v[i], v[next[i]])`
with `next = {1, 2, 0}` at `0x00908DE8`, `cross(v[next] - v[i], p - v[i]) . n < 0` answers 0; three
edges that are zero or positive answer 1, so a point on an edge counts as inside.

### The collision-mesh ray cast

`0x0022D4B0(part, q)` is the per-cell callback of the walker below, planted only by `0x002315E0`. It
takes the ids listed for the cell (`[part + 0x28]` from `q.+0x3E`, `q.+0x40` of them) and skips an
id at or above `0x5000`. Each polygon's attribute word (`+0x0C`) and each wall record's (`+0x04`)
is first overlaid with the override table: `eff = (word & ~mask) | (value & mask)` from the entry
`0x0209A3E0 + 8 (32 + group)`, the group being bits `0x3E000` of the word.

The low three bits of `eff` then decide: 0 is tested; 1 is tested unless bit `0x80000000` is set, and with bit `0x40000000` set only when the query
kind `q.+0x46` is not 4; 4 is tested only for kind 4; 2, 3, 5, 6 and 7 are skipped.

A tested polygon gets `t = 0x0022E6D0(start, delta, {polygon, v[0]})`; when `0 <= t < best` the point
`start + delta t / length` is put to the winding test. A tested wall record gets `t = 0x00380FA0(&hit,
record, start, end)` with the same bound. An accepted hit with bit `0x800000` of `eff` clear becomes the
new best: `q.best = t`, the hit point goes to `[q.+0x20]`, `q.+0x42 = id`, `q.state = 2`. With bit
`0x800000` set the hit only raises `q.state` from 0 to 1, a marker that something was crossed without
stopping the ray.

Struct MeshQuery  (the walker's record, built on the caller's stack):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `f32[4]` | delta = end - start (w from end) |  |
| `+0x10` | `void*` | start point |  |
| `+0x18` | `void*` | end point |  |
| `+0x20` | `void*` | the hit point written |  |
| `+0x28` | `void*` | per-cell callback |  |
| `+0x30` | `f32` | best t (starts at the length) |  |
| `+0x34` | `f32` | segment length |  |
| `+0x38` | `i32` | stop at the first hit when set |  |
| `+0x3C` | `i16` | current cell |  |
| `+0x3E` | `i16` | cell list start |  |
| `+0x40` | `i16` | cell list count |  |
| `+0x42` | `i16` | hit id (0xFFFF none) |  |
| `+0x44` | `i16` | state: 0 none, 1 marker only, 2 hit |  |
| `+0x46` | `i16` | query kind |  |

`0x0022F430(part, q)` walks the segment through the collision grid. The cell of a point is
`0x00233050`: column `(x + originX) / cellW`, row `(z + originZ) / cellH` after subtracting half a
cell height on odd columns (the grid is staggered), `0xFFFF` outside. `0x002330D0(part, point, k)` returns that
cell plus `k × (stride + 1)`, or the negative answer as it is. `0x002F67C0`, which fades the background NPCs
listed in a point's cell in or out by their distance from the point, uses it with `k` = 1 (`0x002F67F0`).

From the start cell it loops:
the delta, length and best are reset to the whole remaining segment, the callback runs over the
cell's list and the lists at `cell + k (stride + 1)` for `k = 1, 2` (`0x00908DF8`, `stride` the
mesh part's short at `+0x40`), and a hit shortens the segment to the hit point, keeping the earlier
hit when it was nearer and stopping at once when `q.+0x38` is set.

When the current cell is the end point's cell the walk stops. Otherwise `0x0022D0D0` clips the
segment against the cell's rectangle widened by 0.1 on each side (with an exit margin of 1.8 on the
main mesh part `0x0026E500(0)`, 0.09 on any other), keeping the nearest crossing with `0.0001 < t <
length`, and returns the exit side (0 `+x`, 1 `+z`, 2 `-x`, 3 `-z`) or -1 when the segment ends
inside; the exit point becomes the new start and its cell the next cell. A hit shortens the
segment by writing the hit point into the caller's end vector through `+0x18`.

`0x002315E0(part, &start, &end)` is the ray cast as a function: it builds the query with this
callback, kind `0xFFFF` and the stop flag clear, runs the walker and returns the state (0 clear, 1
marker only, 2 blocked); it answers `0xFFFF` without a mesh part, and it copies its end argument
to a local first, so only direct walker callers see the end vector overwritten. Its callers are
`0x0032A4D0` and `0x00318CA0`. The walker's three other call sites, in `0x00230B60` (`0x00230BD8`) and
`0x00230C10` (`0x00230E1D`, `0x00231123`), plant the sphere sweep and the other ray casts of the doors
page.

### The volume clamps

The sound-emitter section of the map pack ([map pack](../World-Areas-And-Travel/mpk-map-pack.md))
carries volume records, reached as offsets from `[0x022CBAF0]`, and the emitter walk `0x003631B0`
dispatches on each record's kind byte `+0x09 & 0x7F`: 0 the ellipse clamp, 1 the rectangle clamp,
2 the segment chain, anything else leaves the point unchanged. All three take `(point, out,
record)` and write a four-float `out` with `w = 1.0`.

Struct EmitterVolume  base=[`0x022CBAF0`] + offset:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x09` | `u8` | kind (& 0x7F): 0 ellipse, 1 rectangle, 2 segment chain |  |
| `+0x14` | `u32` | segment count (kind 2) |  |
| `+0x20` | `f32[4]` | centre |  |
| `+0x30` | `f32` | extent a |  |
| `+0x34` | `f32` | extent b |  |
| `+0x40` | `f32[8]` | segments (kind 2): start f32[4], direction f32[4], 0x20 bytes each |  |
| `+0x50` | `f32` | rotation angle |  |

Both clamps collapse to the centre when either extent is at or below 0: `out = centre`. Otherwise
`d = point - centre` is rotated into the volume's frame, `u = d.x cos(a) - d.z sin(a)` and `v =
d.x sin(a) + d.z cos(a)` with `a = +0x50`; the vertical component takes no part in either test.

The ellipse, `0x00361DE0`: `S = u^2 + v^2`, `R = sqrt(|S / (u^2 / a^2 + v^2 / b^2)|)` is the ellipse's
radius in the point's direction (0 when `S` is 0) and `D = sqrt(|S|)` the point's distance. When
`R <= D` the point is outside or on the boundary and `out = centre + d (R / D)` in the original
frame; otherwise `out = point`. The status-bit helpers run on `1 / b^2` and on `D` (a zero sets
bit `0x40`, a negative bit `0x80`), not on the quotient, so a point exactly at the centre passes both,
makes `R / D` a 0 by 0 division and returns NaN.

The rectangle, `0x003623C0`: `lx = u / a` and `lz = v / b`. The CLIP word `0x022D9130` is shifted left
6 and takes bit `0x1` for `lx > 1`, bit `0x2` for `lx < -1`, bit `0x10` for `lz > 1`, bit `0x20` for `lz < -1`,
then is masked to 24 bits (four generations) and copied to `0x022D9478`. With none of the four bits
set `out = point`; otherwise `lx` and `lz` are clamped to `[-1, 1]`, `X = lx a`, `Z = lz b`, and
`out = (centre.x + X cos(-a) - Z sin(-a), point.y, centre.z + X sin(-a) + Z cos(-a))`.

The segment chain, `0x00362230`, calls `0x00363FD0(point, start, dir)` for each segment: `t = -((start
- point) . dir) / |dir|^2` clamped to `[0, 1]`, 0 when `|dir|^2` is not positive, with the squared
distance `|start - point + t dir|^2` left at `0x022D92D4` (and `0x022D92E4`). The segment with the
smallest squared distance wins (the first always, a later one only when strictly nearer) and `out =
start + t dir`; with no segments `out = point`. It returns the record's `+0x30`.

The emitter walk is one reader. The other is the actor-record proximity test `0x0025C830` (run per
record by `0x0025C170` from the field tick, [field runtime](../Characters-And-Objects/field-runtime.md)):
it measures each of the four party-slot actors (`0x0209A1F0`) against two rectangles authored in the
record's movement context (centres `+0x00` and `+0x10`, extents `+0x30`/`+0x34` and `+0x40`/
`+0x44`, angles `+0x38` and `+0x48`).

It calls `0x0025A8E0` twice per rectangle, once with the x
extent and one with the z extent as the test radius, and recovers the x bits from the older CLIP
generation (`>> 6`) and the z bits from the newer.

With record byte `+0x0D` bit `0x8` the same test uses the capsule separation `0x003DA5A0` ([movement
bodies](movement-bodies-and-separation.md)) instead of the rectangles.

`0x0025A8E0(p, rec)`, its only caller that test, is the outcode without the clamp: the CLIP word is
shifted left 6 and takes bits `0x1`/1 for `p.x` above `e` or below `-e`, bits `0x4`/3 for `p.y`, bits `0x10`/5
for `p.z`, with `e = |rec.+0x0C|`, and the word is copied to `0x022D9478`. The history is what lets
one function clamp a point and the next read the outcome of the clamp before it.

### The workbench

None of the clamps computes on the stack. They write intermediates to the emulated VU0 register
file: `0x022D9198` (Q), `0x022D91A0` (ACC), the vector registers from `0x022D92A0` to `0x022D935F`, the
CLIP word `0x022D9130` with its copy at `0x022D9478`, and the status word `0x022D9470`, where `0x0036DDA0`
sets bit `0x40` on a zero divisor and `0x0036DD90` bit `0x80` on a negative one.

`0x0036DD80` rewrites the
`vf00` image at `0x01EF93F0` to `{0, 0, 0, 1}` before each use, so the "constants" 0.0 and 1.0 the
clamps load from `0x01EF93F0` and `0x01EF93FC` are a live register image. The block is shared by
every caller and is not reentrant.

## Layouts

Shape record (a collision wall record is one):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `i32` | type: 0 sphere, 1 cylinder, 2 box |  |
| `+0x04` | `u32` | attribute word (collision mesh; the primitives do not read it) |  |
| `+0x10` | `f32[16]` | forward transform (unit frame to world) |  |
| `+0x50` | `f32[16]` | inverse transform (world to unit frame) |  |

Collision polygon (`0x20` bytes at [part + `0x10`]):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `f32[3]` | plane normal |  |
| `+0x0C` | `u32` | attribute word |  |
| `+0x10` | `u16[3]` | vertex indices into the 0x10-byte vertices at [part + 0x08] |  |

Globals:

| Address | Type | Name | Meaning |
|---|---|---|---|
| `0x00D11200` | `f32[6][4]` | unit-cube faces {n, 1}: +x, -x, +y, -y, +z, -z |  |
| `0x00D11260` | `f32[4]` | {0, 0, 0, 1}, the sphere's centre |  |
| `0x00D11270` | `f32[4]` | {0, 0, 0, 1}, the cylinder's axis point |  |
| `0x00D11280` | `f32[4]` | {0, 1, 0, 1}, the top cap plane |  |
| `0x00D11290` | `f32[4]` | {0, -1, 0, 1}, the bottom cap plane |  |
| `0x00D112A0` | `f32[4]` | {0.999, 1.001, -0.999, 0}; 0x00D112A4 is the box margin |  |
| `0x00908DE8` | `i32[3]` | {1, 2, 0}, the next-vertex table |  |
| `0x00908DF8` | `i32[4]` | {0, 1, 2, -1}, the cell-list offsets |  |
| `0x0209A3E0` | `...` | override entries, 8 bytes each; walls and polygons use entries 32-63 |  |
| `0x022CBAF0` | `void*` | base of the emitter volume records |  |
| `0x022D9130` | `...` | the CLIP word |  |
| `0x022D9478` | `...` | the CLIP word's copy |  |
| `0x022D9198` | `f32` | the VU0 register image: Q |  |
| `0x022D91A0` | `f32[4]` | the VU0 register image: ACC |  |
| `0x022D92A0` | `...` | the VU0 register image: vector registers 0x022D92A0 to 0x022D935F |  |
| `0x022D9470` | `u8` | the VU0 register image: flag byte |  |
| `0x01EF93F0` | `f32[4]` | the vf00 image {0, 0, 0, 1} |  |

## Shipped data

| Fact | Value |
|---|---|
| unit-cube faces at `0x00D11200` | `(1,0,0,1)`, `(-1,0,0,1)`, `(0,1,0,1)`, `(0,-1,0,1)`, `(0,0,1,1)`, `(0,0,-1,1)` |
| box face margin `0x00D112A4` | 1.001 (`0x3F8020C5`); `0x00D112A0` 0.999, `0x00D112A8` -0.999 |
| sphere and cylinder tolerance | `1e-6` on the direction length before the divide |
| ray-cast cell margin | 0.1 on each side; exit margin 1.8 on the main part, 0.09 elsewhere |
| `vf00` image `0x01EF93F0` | `{0, 0, 0, 1}` in the image and after every `0x0036DD80` |

## Operations

Per ray cast: the walker steps cell by cell from the start to the end, and in each cell the
callback tests every listed polygon and wall record the override table leaves active, keeping the
nearest hit. Per point test: the inverse transform and one membership test. Per emitter
evaluation: one clamp per volume record in the listener's list, each through the workbench.

## State

The override table at `0x0209A3E0`; the CLIP word and its four-generation history; the VU0 register
image and the status word; the emitter record base `0x022CBAF0`.

## Modding notes

- A shape's size and orientation are its transform pair only. Scaling a wall means rewriting both
  matrices; the inverse is not recomputed by the engine.
- The box test accepts points up to 1.001 of a half-extent outside a face, and the ray cast's
  `-0.001` lower bound accepts a face the segment starts a hair behind.
- The ray cast stops at the first hit only when the query's `+0x38` is set; `0x002315E0` leaves it
  clear and reports the nearest hit's state, not its position.
- Bit `0x800000` of a polygon's attribute word turns it into a marker: the ray reports it crossed (state 1)
  but is not stopped by it.
- The clamps and the proximity test share one register image. Running either from a second thread,
  or from a hook that re-enters it, corrupts the other's intermediates.
- The ellipse clamp returns NaN for a point exactly on the centre; a port should return the centre.

## Related

- [Doors, gates and map changes](../World-Areas-And-Travel/doors-gates-and-map-changes.md): the
  attribute word, the override table and the other mesh queries.
- [Movement bodies and separation](movement-bodies-and-separation.md): the capsule separation
  `0x003DA5A0` and the body list `0x0046DB50` walks.
- [Navigation mesh and pathfinding](navigation-mesh-and-pathfinding.md): the portal mesh, a
  different structure from the collision mesh.
- [MPK map pack](../World-Areas-And-Travel/mpk-map-pack.md): the emitter section and the walk
  `0x003631B0`.
