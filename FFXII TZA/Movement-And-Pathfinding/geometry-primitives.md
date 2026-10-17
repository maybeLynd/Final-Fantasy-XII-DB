---
title: "Geometry primitives: the unit sphere, cylinder and box tests behind collision, the collision-mesh ray cast that uses them, and the volume clamps"
kind: "system"
category: "Movement and pathfinding"
addresses: "00380FA0, 00381AC0, 00381630, 00381450, 00381EB0, 00382020, 0046BF60, 0046BFA0, 0022E6D0, 0022CF50, 0022D4B0, 0022F430, 002315E0, 0022F8B0, 00233050, 0022D0D0, 00202E10, 00202B70, 00361DE0, 003623C0, 00363FD0, 00362230, 003631B0, 0025A8E0, 0025C830, 0046DB50, 0036DD80, 0036DD90, 0036DDA0"
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
height 2, or a unit cube of half-extent 1. A shape record holds its type at `+00`<sub>h</sub> (0 sphere, 1
cylinder, 2 box), a forward transform at `+10`<sub>h</sub> and its inverse at `+50`<sub>h</sub>; size, position and
orientation live only in the transform pair. The collision mesh's wall records are such shapes
(`90`<sub>h</sub> bytes each, [doors and gates](../World-Areas-And-Travel/doors-gates-and-map-changes.md)).

`00380FA0(out, shape, A, B)` solves a segment against a shape: `A` and then `B` are mapped into the
shape's frame through the inverse at `+50`<sub>h</sub> (`00202B70`), the type picks a primitive below, and a
type other than 0, 1 or 2 (tested after both points are mapped), or a primitive that reports no
hit, returns -1.0. A hit is mapped back
through `+10`<sub>h</sub> into `out`, and the return value is the three-dimensional distance from `A` to
`out`. Each primitive takes `(out, A, B)` in the unit frame, writes `out` with `B`'s `w`, and
returns 1 for a hit.

### The three unit primitives

The sphere, `00381AC0`: with `d = B - A`, `L = |d|` and `u = d / L` (zero when `L < 1e-6`), the
closest point of the line to the origin is `P = A + t u` with `t = -A . u`. A hit needs `|A| < 1`,
or `|B| < 1`, or `|P| <= 1` with `0 <= t / L <= 1`; then `h = sin(acos(|P|))` and the point is
`P - u h`, the segment's entry into the sphere.

The cylinder, `00381630`, tests the caps first. With `A.y > 1` it returns 0 outright when `B.y >= 1`;
otherwise `t = -L (A.y - 1) / d.y` (`0046BFA0` against the top plane `00D11280`), and when
`0 < t < L` and the point `A + d t / L` lies within radius 1 of the axis that point is the hit.
`A.y < -1` mirrors this with the bottom plane `00D11290` and `B.y <= -1`. A cap miss falls through
to the side.

The side solve projects everything onto the ground plane: `Axz = (A.x, 0, A.z)`, `dxz = (d.x, 0,
d.z)`, `m = |dxz|`, `u = dxz / m`, `t = -Axz . u`, `P = Axz + t u`. The side counts when
`00382020(A)` or `00382020(B)` says an endpoint is inside, or `|P| <= 1` with `0 <= t / m <= 1`;
then `s = (t - sin(acos(|P|))) / m` and the point is `A + d s` along the full direction, accepted
only when its `y` lies in `[-1, 1]`.

The box, `00381450`, runs the six faces of the unit cube from the table at `00D11200` in order, each
a plane `{n, 1}` used as both normal and point. For a face `t = -L ((A - n) . n) / (d . n)`; when
`-0.001 < t` and `t` is below the best so far (initially `L`), the point `A + d t / L` is accepted
when each of its coordinates lies within 1.001 of the face normal's matching component, and it
becomes the new best. The nearest accepted face is the hit.

`0046BF60(p, n, q)` is `(p - q) . n`; `0046BFA0(A, d, n, p)` is `-|d| ((A - p) . n) / (d . n)`, the
distance along the segment to the plane through `p` with normal `n`. `00382020(p)` is 1 when
`-1 < p.y < 1` and `sqrt(p.x^2 + p.z^2) < 1`; `0046DB50` reuses it on the records of the list
`003DAE20` returns, the body placements linked each frame by `003DB0D0` (heading at
`+10`<sub>h</sub>/`+18`<sub>h</sub>, the inner shape's radii at `+70`<sub>h</sub>/`+74`<sub>h</sub> and height at `+78`<sub>h</sub>), to find the
highest record top above a point.

### Point in shape

`00381EB0(shape, p)` maps `p` through the inverse and tests membership strictly: type 0 `|local| <
1`; type 1 `-1 < y < 1` and `sqrt(x^2 + z^2) < 1`; type 2 every coordinate in `(-1, 1)`; any other
type is outside. Its one caller is `0022F8B0`, the per-cell wall contact test of the collision
walker: for each id in the cell's list that names a wall record (`4000`<sub>h</sub> to `4FFF`<sub>h</sub>), and, when
the query's `+24`<sub>h</sub> is set, whose effective attribute word has bit 31 clear, it tests the point at
the query's `+18`<sub>h</sub> and raises the query's `+20`<sub>h</sub> on the first hit.

### The polygon predicates

Collision polygons are `20`<sub>h</sub>-byte records at the mesh part's `[+10h]`: a plane normal at `+00`<sub>h</sub>,
the attribute word at `+0C`<sub>h</sub> and three vertex indices at `+10`<sub>h</sub>, `+12`<sub>h</sub>, `+14`<sub>h</sub> into the
`10`<sub>h</sub>-byte vertices at `[+08h]`. `0022E6D0(A, d, {polygon, vertex})` returns `-|d| ((A - vertex) .
n) / (d . n)`, the distance along the segment to the polygon's plane, through the vertex the
caller hands it.

`0022CF50(part, id, p)` is the winding test: for each edge `(v[i], v[next[i]])`
with `next = {1, 2, 0}` at `00908DE8`, `cross(v[next] - v[i], p - v[i]) . n < 0` answers 0; three
edges that are zero or positive answer 1, so a point on an edge counts as inside.

### The collision-mesh ray cast

`0022D4B0(part, q)` is the per-cell callback of the walker below, planted only by `002315E0`. It
takes the ids listed for the cell (`[part + 28h]` from `q.+3Eh`, `q.+40h` of them) and skips an
id at or above `5000`<sub>h</sub>. Each polygon's attribute word (`+0C`<sub>h</sub>) and each wall record's (`+04`<sub>h</sub>)
is first overlaid with the override table: `eff = (word & ~mask) | (value & mask)` from the entry
`0209A3E0 + 8 (32 + group)`, the group being bits 13-17 of the word.

The low three bits of `eff` then decide: 0 is tested; 1 is tested unless bit 31 is set, and with bit 30 set only when the query
kind `q.+46h` is not 4; 4 is tested only for kind 4; 2, 3, 5, 6 and 7 are skipped.

A tested polygon gets `t = 0022E6D0(start, delta, {polygon, v[0]})`; when `0 <= t < best` the point
`start + delta t / length` is put to the winding test. A tested wall record gets `t = 00380FA0(&hit,
record, start, end)` with the same bound. An accepted hit with bit 23 of `eff` clear becomes the
new best: `q.best = t`, the hit point goes to `[q.+20h]`, `q.+42h = id`, `q.state = 2`. With bit
23 set the hit only raises `q.state` from 0 to 1, a marker that something was crossed without
stopping the ray.

Struct MeshQuery  (the walker's record, built on the caller's stack):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `f32[4]` | delta = end - start (w from end) | +`10`<sub>h</sub>  ptr  start point |
| `18`<sub>h</sub> | `void*` | end point | +`20`<sub>h</sub>  ptr  the hit point written |
| `28`<sub>h</sub> | `void*` | per-cell callback | +`30`<sub>h</sub>  f32  best t (starts at the length) |
| `34`<sub>h</sub> | `f32` | segment length | +`38`<sub>h</sub>  i32  stop at the first hit when set |
| `3C`<sub>h</sub> | `i16` | current cell | +`3E`<sub>h</sub>  i16  cell list start |
| `40`<sub>h</sub> | `i16` | cell list count | +`42`<sub>h</sub>  i16  hit id (`FFFF`<sub>h</sub> none) |
| `44`<sub>h</sub> | `i16` | state: 0 none, 1 marker only, 2 hit | +`46`<sub>h</sub>  i16  query kind |

`0022F430(part, q)` walks the segment through the collision grid. The cell of a point is
`00233050`: column `(x + originX) / cellW`, row `(z + originZ) / cellH` after subtracting half a
cell height on odd columns (the grid is staggered), `FFFF`<sub>h</sub> outside. `002330D0(part, point, k)` returns that
cell plus `k × (stride + 1)`, or the negative answer as it is. `002F67C0`, which fades the background NPCs
listed in a point's cell in or out by their distance from the point, uses it with `k` = 1 (`002F67F0`).

From the start cell it loops:
the delta, length and best are reset to the whole remaining segment, the callback runs over the
cell's list and the lists at `cell + k (stride + 1)` for `k = 1, 2` (`00908DF8`, `stride` the
mesh part's short at `+40`<sub>h</sub>), and a hit shortens the segment to the hit point, keeping the earlier
hit when it was nearer and stopping at once when `q.+38h` is set.

When the current cell is the end point's cell the walk stops. Otherwise `0022D0D0` clips the
segment against the cell's rectangle widened by 0.1 on each side (with an exit margin of 1.8 on the
main mesh part `0026E500(0)`, 0.09 on any other), keeping the nearest crossing with `0.0001 < t <
length`, and returns the exit side (0 `+x`, 1 `+z`, 2 `-x`, 3 `-z`) or -1 when the segment ends
inside; the exit point becomes the new start and its cell the next cell. A hit shortens the
segment by writing the hit point into the caller's end vector through `+18`<sub>h</sub>.

`002315E0(part, &start, &end)` is the ray cast as a function: it builds the query with this
callback, kind `FFFF`<sub>h</sub> and the stop flag clear, runs the walker and returns the state (0 clear, 1
marker only, 2 blocked); it answers `FFFF`<sub>h</sub> without a mesh part, and it copies its end argument
to a local first, so only direct walker callers see the end vector overwritten. Its callers are
`0032A4D0` and `00318CA0`. The walker's three other call sites, in `00230B60` (`00230BD8`) and
`00230C10` (`00230E1D`, `00231123`), plant the sphere sweep and the other ray casts of the doors
page.

### The volume clamps

The sound-emitter section of the map pack ([map pack](../World-Areas-And-Travel/mpk-map-pack.md))
carries volume records, reached as offsets from `[022CBAF0]`, and the emitter walk `003631B0`
dispatches on each record's kind byte `+09h & 7Fh`: 0 the ellipse clamp, 1 the rectangle clamp,
2 the segment chain, anything else leaves the point unchanged. All three take `(point, out,
record)` and write a four-float `out` with `w = 1.0`.

Struct EmitterVolume  base=[`022CBAF0`] + offset:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `09`<sub>h</sub> | `u8` | kind (& `7F`<sub>h</sub>): 0 ellipse, 1 rectangle, 2 segment chain |  |
| `14`<sub>h</sub> | `u32` | segment count (kind 2) |  |
| `20`<sub>h</sub> | `f32[4]` | centre |  |
| `30`<sub>h</sub> | `f32` | extent a | +`34`<sub>h</sub>  f32  extent b |
| `40`<sub>h</sub> | `f32[8]` | segments (kind 2): start f32[4], direction f32[4], `20`<sub>h</sub> bytes each |  |
| `50`<sub>h</sub> | `f32` | rotation angle |  |

Both clamps collapse to the centre when either extent is at or below 0: `out = centre`. Otherwise
`d = point - centre` is rotated into the volume's frame, `u = d.x cos(a) - d.z sin(a)` and `v =
d.x sin(a) + d.z cos(a)` with `a = +50h`; the vertical component takes no part in either test.

The ellipse, `00361DE0`: `S = u^2 + v^2`, `R = sqrt(|S / (u^2 / a^2 + v^2 / b^2)|)` is the ellipse's
radius in the point's direction (0 when `S` is 0) and `D = sqrt(|S|)` the point's distance. When
`R <= D` the point is outside or on the boundary and `out = centre + d (R / D)` in the original
frame; otherwise `out = point`. The status-bit helpers run on `1 / b^2` and on `D` (a zero sets
bit 6, a negative bit 7), not on the quotient, so a point exactly at the centre passes both,
makes `R / D` a 0 by 0 division and returns NaN.

The rectangle, `003623C0`: `lx = u / a` and `lz = v / b`. The CLIP word `022D9130` is shifted left
6 and takes bit 0 for `lx > 1`, bit 1 for `lx < -1`, bit 4 for `lz > 1`, bit 5 for `lz < -1`,
then is masked to 24 bits (four generations) and copied to `022D9478`. With none of the four bits
set `out = point`; otherwise `lx` and `lz` are clamped to `[-1, 1]`, `X = lx a`, `Z = lz b`, and
`out = (centre.x + X cos(-a) - Z sin(-a), point.y, centre.z + X sin(-a) + Z cos(-a))`.

The segment chain, `00362230`, calls `00363FD0(point, start, dir)` for each segment: `t = -((start
- point) . dir) / |dir|^2` clamped to `[0, 1]`, 0 when `|dir|^2` is not positive, with the squared
distance `|start - point + t dir|^2` left at `022D92D4` (and `022D92E4`). The segment with the
smallest squared distance wins (the first always, a later one only when strictly nearer) and `out =
start + t dir`; with no segments `out = point`. It returns the record's `+30`<sub>h</sub>.

The emitter walk is one reader. The other is the actor-record proximity test `0025C830` (run per
record by `0025C170` from the field tick, [field runtime](../Characters-And-Objects/field-runtime.md)):
it measures each of the four party-slot actors (`0209A1F0`) against two rectangles authored in the
record's movement context (centres `+00`<sub>h</sub> and `+10`<sub>h</sub>, extents `+30`<sub>h</sub>/`+34`<sub>h</sub> and `+40`<sub>h</sub>/
`+44`<sub>h</sub>, angles `+38`<sub>h</sub> and `+48`<sub>h</sub>).

It calls `0025A8E0` twice per rectangle, once with the x
extent and one with the z extent as the test radius, and recovers the x bits from the older CLIP
generation (`>> 6`) and the z bits from the newer.

With record byte `+0D`<sub>h</sub> bit 3 the same test uses the capsule separation `003DA5A0` ([movement
bodies](movement-bodies-and-separation.md)) instead of the rectangles.

`0025A8E0(p, rec)`, its only caller that test, is the outcode without the clamp: the CLIP word is
shifted left 6 and takes bits 0/1 for `p.x` above `e` or below `-e`, bits 2/3 for `p.y`, bits 4/5
for `p.z`, with `e = |rec.+0Ch|`, and the word is copied to `022D9478`. The history is what lets
one function clamp a point and the next read the outcome of the clamp before it.

### The workbench

None of the clamps computes on the stack. They write intermediates to the emulated VU0 register
file: `022D9198` (Q), `022D91A0` (ACC), the vector registers from `022D92A0` to `022D935F`, the
CLIP word `022D9130` with its copy at `022D9478`, and the status word `022D9470`, where `0036DDA0`
sets bit 6 on a zero divisor and `0036DD90` bit 7 on a negative one.

`0036DD80` rewrites the
`vf00` image at `01EF93F0` to `{0, 0, 0, 1}` before each use, so the "constants" 0.0 and 1.0 the
clamps load from `01EF93F0` and `01EF93FC` are a live register image. The block is shared by
every caller and is not reentrant.

## Layouts

```
shape record (a collision wall record is one)
+0x00  i32     type: 0 sphere, 1 cylinder, 2 box
+0x04  u32     attribute word (collision mesh; the primitives do not read it)
+0x10  f32[16] forward transform (unit frame to world)
+0x50  f32[16] inverse transform (world to unit frame)

collision polygon (0x20 bytes at [part + 0x10])
+0x00  f32[3]  plane normal    +0x0C  u32  attribute word
+0x10  u16[3]  vertex indices into the 0x10-byte vertices at [part + 0x08]

globals
00D11200  f32[6][4]  unit-cube faces {n, 1}: +x, -x, +y, -y, +z, -z
00D11260  f32[4]     {0, 0, 0, 1}, the sphere's centre
00D11270  f32[4]     {0, 0, 0, 1}, the cylinder's axis point
00D11280  f32[4]     {0, 1, 0, 1}, the top cap plane
00D11290  f32[4]     {0, -1, 0, 1}, the bottom cap plane
00D112A0  f32[4]     {0.999, 1.001, -0.999, 0}; 00D112A4 is the box margin
00908DE8  i32[3]     {1, 2, 0}, the next-vertex table
00908DF8  i32[4]     {0, 1, 2, -1}, the cell-list offsets
0209A3E0  override entries, 8 bytes each; walls and polygons use entries 32-63
022CBAF0  ptr        base of the emitter volume records
022D9130 / 022D9478  the CLIP word and its copy
022D9198, 022D91A0, 022D92A0-022D935F, 022D9470  the VU0 register image
01EF93F0  f32[4]     the vf00 image {0, 0, 0, 1}
```

## Shipped data

| Fact | Value |
|---|---|
| unit-cube faces at `00D11200` | `(1,0,0,1)`, `(-1,0,0,1)`, `(0,1,0,1)`, `(0,-1,0,1)`, `(0,0,1,1)`, `(0,0,-1,1)` |
| box face margin `00D112A4` | 1.001 (`3F8020C5`<sub>h</sub>); `00D112A0` 0.999, `00D112A8` -0.999 |
| sphere and cylinder tolerance | `1e-6` on the direction length before the divide |
| ray-cast cell margin | 0.1 on each side; exit margin 1.8 on the main part, 0.09 elsewhere |
| `vf00` image `01EF93F0` | `{0, 0, 0, 1}` in the image and after every `0036DD80` |

## Operations

Per ray cast: the walker steps cell by cell from the start to the end, and in each cell the
callback tests every listed polygon and wall record the override table leaves active, keeping the
nearest hit. Per point test: the inverse transform and one membership test. Per emitter
evaluation: one clamp per volume record in the listener's list, each through the workbench.

## State

The override table at `0209A3E0`; the CLIP word and its four-generation history; the VU0 register
image and the status word; the emitter record base `022CBAF0`.

## Modding notes

- A shape's size and orientation are its transform pair only. Scaling a wall means rewriting both
  matrices; the inverse is not recomputed by the engine.
- The box test accepts points up to 1.001 of a half-extent outside a face, and the ray cast's
  `-0.001` lower bound accepts a face the segment starts a hair behind.
- The ray cast stops at the first hit only when the query's `+38`<sub>h</sub> is set; `002315E0` leaves it
  clear and reports the nearest hit's state, not its position.
- Bit 23 of a polygon's attribute word turns it into a marker: the ray reports it crossed (state 1)
  but is not stopped by it.
- The clamps and the proximity test share one register image. Running either from a second thread,
  or from a hook that re-enters it, corrupts the other's intermediates.
- The ellipse clamp returns NaN for a point exactly on the centre; a port should return the centre.

## Related

- [Doors, gates and map changes](../World-Areas-And-Travel/doors-gates-and-map-changes.md): the
  attribute word, the override table and the other mesh queries.
- [Movement bodies and separation](movement-bodies-and-separation.md): the capsule separation
  `003DA5A0` and the body list `0046DB50` walks.
- [Navigation mesh and pathfinding](navigation-mesh-and-pathfinding.md): the portal mesh, a
  different structure from the collision mesh.
- [MPK map pack](../World-Areas-And-Travel/mpk-map-pack.md): the emitter section and the walk
  `003631B0`.
