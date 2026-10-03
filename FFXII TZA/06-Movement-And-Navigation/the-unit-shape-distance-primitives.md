---
system: The unit-shape distance and containment primitives — sphere/cylinder/box
  closest-point solves, point-in-shape tests, and the edge and triangle
  predicates the navigation queries are built from
category: 06-Movement-And-Navigation
status: DOCUMENTED — SD-182 is ANSWERED, every box is closed and the constants and planted siblings are on the page (owner re-status 2026-09-30, OPUS, on SWE2-CONTRACT's DD batch 10) — the adoption this line waited for has landed (SWE2-DATA 2026-09-30, Data structures and formulas;
  the request closed as CON-129), SD-182 answered the transform-pair question, and the constants and the planted
  siblings are supplied (SWE2-CONTRACT DD batch 10) (was — home page filed so the executed contract has somewhere
  to land; the full adoption is in flight via REQ-OPUS-NAV-RESIDUAL-BOUNDARY-FINDINGS)
owner_layer: CodeDomain — shared geometry
evidence_tier: 1
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: every function this page names executed from the shipped bytes under
    EXP-138/EXP-139 (evidence/nav-residual-boundary-exec/,
    evidence/nav-region-query-exec/ — Unicorn world vs Python model,
    466/466 functional cases and 411/411 byte-precise mutants, stable across
    three processes)
last_reviewed: 2026-09-29
audit:
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-falsification-1 - spans, dispatch, tables, imports and the push-out chain survive; the 'zero inbound
    references' audit is refuted (planted callbacks) and the D4B0 planter corrected to 002315E0
  note: skeleton filed by SWE2-ORACLE at OPUS's request
    (OPUS-REQ-ORACLE-RESIDUAL-BOUNDARY-HAS-NO-PAGE-TO-ADOPT-INTO) so the ten
    unowned addresses in the EXP-138 findings scope have a home; the executed
    semantics land via the findings adoption, not here
---

# The unit-shape distance and containment primitives

> One sentence: the small geometry toolbox — "how far is this segment from this
> shape", "is this point inside this shape", "does this edge wind around this
> point" — that the navigation walk, the region query, and the separation pass
> all reach into.

## 1. What the player sees

When a unit walks to a waypoint, pushes past another body, or asks whether a
spell's capsule touches a target, the same handful of questions is being
answered underneath: *does this line cross this face*, *is this point inside
this volume*, *how far is this segment from this shape*. The bodies on this
page are the answers. Nothing on screen names them; when they are wrong the
symptom is a walker that hugs a wall it should clear, a separation push that
fires late, or a region query that reports the wrong exit side.

## 2. Native mechanism

~~**Pending adoption** — the verified executed contract for every body below~~
~~lives in [`_experiments/EXP-138-nav-residual-boundary-exec.md`](../_experiments/EXP-138-nav-residual-boundary-exec.md)~~
~~("Verified behavior contract") and lands here via~~
~~`REQ-OPUS-NAV-RESIDUAL-BOUNDARY-FINDINGS`.~~ *(Corrected 2026-09-30, SWE2-DATA: that request is closed; its result
was the ledger row CON-129 and it adopted nothing here. The contract of
[EXP-138](../_experiments/EXP-138-nav-residual-boundary-exec.md) is adopted below, in "Data structures and
formulas".)* This section owns the census so the
addresses have one home and no second page invents a parallel description.

### The shape record

The primitives operate on a shared **shape record**: a type dword at `+0x00`
(`0` sphere, `1` cylinder, `2` box — all in *unit* space), a forward transform
at `+0x10`, and its inverse at `+0x50`. Callers transform the query into the
shape's local frame, run the unit-space test, and map the answer back.

### The toolbox, by owner

| VA | role | span |
|---|---|---|
| `0022D4B0` | D4B0 — the nav-grid edge-range scan (F430's planted callback `q[ctx+0x28]`): subrecords route to FA0, plain edges route to E6D0 + CF50 | 815 B |
| `0022E6D0` | E6D0 — signed projected distance `−L·num/den` against an edge's plane | 249 B |
| `0022CF50` | CF50 — triangle winding test, three XPROD edge checks over the `0x908DE8` index table | 381 B |
| `00380FA0` | FA0 — segment-vs-shape distance: both endpoints to local frame, type dispatch to a primitive, result mapped back, `−1.0` on no-hit | 263 B |
| `00381AC0` | sphere primitive — unit-sphere surface solve via `acosf`/`sinf` | 708 B |
| `00381630` | cylinder primitive — top/bottom cap-plane tests plus the XZ-radial side solve | 1,168 B |
| `00381450` | box primitive — six-face unit-cube test over the `0xD11200` face table, margin `1.001` | 477 B |
| `00381EB0` | EB0 — point-in-unit-shape test: local transform, then per-type membership | 365 B |
| `0046BF60` | BF60 — point-plane dot distance | 54 B |
| `0046BFA0` | BFA0 — signed projected distance `−|d|·dot/den` (same form as E6D0, different arg roles) | 294 B |

### Who reaches it

- `0022F430` F430 (the waypoint walker) ~~plants D4B0 as its per-cell edge
  callback~~ *invokes D4B0 as its per-cell edge callback; CORRECTED 2026-09-29 (OPUS, falsification pass 1): the planter is
  F430's caller `002315E0`, which takes D4B0's address (`lea` at `0023160E`) into its stack context and then calls F430* — the executed wiring is in
  [how a unit finds its way across the navigation mesh](how-a-unit-finds-its-way-across-the-navigation-mesh.md)
  and the EXP-138 record.
- `0022F8B0` N2F8B0 (the sub-record point-test loop) calls EB0.
- `003DA5A0` D5A0 (capsule distance) is the sibling whose anisotropic-metric
  helpers DA730/A1D30 already have owners ~~in 04-Actor-Entity and here~~. *(Corrected 2026-09-30, SWE2-DATA: the
  owner is [the movement body pool and the separation pass](the-movement-body-pool-and-the-separation-pass.md), which
  reads D5A0 as the signed separation of two ellipses and DA730 as one ellipse's extent, and runs the DA730 + A1D30
  pairs; the 04-Actor-Entity context census lists DA730 only as a field reader.)*

## Data structures and formulas (SWE2-DATA, 2026-09-30)

Adopted from the executed contract of [EXP-138](../_experiments/EXP-138-nav-residual-boundary-exec.md) ("Verified
behavior contract"). Fixture parity is MODEL-PROVEN; the static reads behind it are the falsification pass below.

```
shape record          +0x00 type (0 sphere, 1 cylinder, 2 box; unit space)
                      +0x10 forward transform, +0x50 its inverse
nav edge (32 B)       q[tab+0x10] + si*32, for si < 0x4000; d[edge+0xC] selects the CLST pair
nav subrecord (144 B) q[tab+0x18] + (si-0x4000)*144, for 0x4000 <= si < 0x5000; si >= 0x5000 is skipped

E6D0(A, ctx, {edge, vtx})  L = |ctx|; returns -L * ((A - vtx) . n) / (ctx . n)  (negative or NaN: rejected)
CF50(tab, si, pt)          1 when cross(vb - va, pt - va) . f[rec..] > 0 for all three edges ({1,2,0} at 0x908DE8)
FA0(out, shape, A, B)      A, B to local frame through the inverse at +0x50; type dispatch to the unit primitive;
                           the closest point mapped back through +0x10; returns the 3-D distance, or -1.0 on no hit
sphere                     projects A onto the segment direction and solves the unit-sphere surface (acosf / sinf)
cylinder                   top and bottom cap planes (BF60 / BFA0) plus the XZ radial side solve; D2020 tests inside
box                        the six-face table at 0xD11200, margin 1.001, epsilon -0.001
D2020(pt)                  1 when -1 < y < 1 and sqrt(x^2 + z^2) < 1
EB0(sub, pt)               local = inverse(+0x50) * pt; type 0 |local| < 1, type 1 as D2020, type 2 |x|,|y|,|z| < 1
D5A0(out, capA, posB, capB, posA)
                           ellA = A1D30(DA730(capA, posB, posA)), ellB symmetric; out = {posA - posB, 1.0};   <- corrected 2026-10-02, OPUS - out.w is the horizontal distance sqrt(dz^2 + dx^2), not 1.0: 003DA663 overwrites the 1.0 stored at 003DA62D-003DA63E
                           returns dist - (ellA + capA.w + ellB + capB.w)
```

## Call chain (SWE2-DATA, 2026-09-30)

Upstream, as "Who reaches it" above: the planter `002315E0` hands D4B0 to the waypoint walker F430; the sub-record
point-test loop `0022F8B0` calls EB0; the region-scan callbacks `0022D7E0` / `0022DE60` are planted the same way
(falsification U5). Downstream:

```
D4B0 (per-cell edge callback)
  +-- subrecord (0x4000 <= si < 0x5000) --> FA0 --> sphere 00381AC0 / cylinder 00381630 / box 00381450
  +-- plain edge (si < 0x4000)          --> E6D0 (signed distance) --> CF50 (winding test)
EB0 (point in shape) <-- 0022F8B0
cylinder primitive --> BF60 / BFA0 (plane distances)
```

## Modding notes (SWE2-DATA, 2026-09-30)

- A shape is a unit sphere, cylinder or cube in its own frame; its size, position and orientation live only in the
  transform pair. Scaling a collision shape means editing the transforms, not a radius field.
- The box test's `1.001` margin means a point up to a thousandth of the half-extent outside a face still counts as on
  it.
- Edge indices at or above `0x5000` are skipped by the edge scan, so that range cannot carry live geometry.

## Evidence table (SWE2-DATA, 2026-09-30)

| claim | evidence | tier |
|---|---|---|
| the ten bodies, their spans and their tables | falsification pass 1, U0–U3 (`falsify_unit_shape.py`) | 1 |
| the contract formulas above | EXP-138 executed parity (`_experiments/evidence/nav-residual-boundary-exec/`) | MODEL-PROVEN |
| D4B0 is planted by `002315E0`, not F430 | falsification pass 1, U4 | 1 |
| the region-scan siblings are planted callbacks, not dead | falsification pass 1, U5 | 1 |
| the push-out chain | falsification pass 1, U6 | 1 |

## 3. What is not known

- ~~Whether the shape record's `+0x10`/`+0x50` pair is authored data or filled
  per-query — the transform pair builder `00230790` and the region-scan
  siblings `0x22D7E0..`/`0x22DE60` that build it are decoded but not yet
  executed.~~ *Corrected 2026-09-30 (SWE2-CONTRACT, DD batch 10): answered by the SD-182 box below. The pair is
  authored in the map pack's nav chunk, and `00230790` builds a different object, the transform workbench. The
  siblings are listed with their plants and callees in "Constants and the planted siblings" below; they are still not
  executed.* ~~The EXP-139 post-scope audit (whole-image scan, NATIVE/STATIC)
  found **zero inbound references** to `0x22D7E0`/`0x22DE60`/`0x230790`/
  `0x22E7D0`/`0x3810B0` — dead code or runtime-dispatched in this build.~~
  **CORRECTED 2026-09-29 (OPUS, falsification pass 1): the five are reached, as planted callbacks.** `0022D7E0`'s address is
  taken by `lea` in `00231690` (reached from `0032BCC0`, `0032CA70`) and `002327D0` (from `00380C40`); `0022DE60`'s in
  `00230C10` (from `00230C00`, which also calls F430) - the same plant-and-invoke shape as D4B0. `00230790` and `0022E7D0`
  are called by `0022D7E0`, and `003810B0` by both. So they are runtime-dispatched, not dead. The audit's "no `lea`" missed
  the three `lea`s. The
  sibling `0x381D90` (push-out direction) is live through `0x232160` ←
  `0x3D97E0` ← a `0x32xxxx` chain; the generic math leaves (`0x217150`
  matmul, `0x217610` rigid-inverse, `0x202C70`, `0x380800`) have 15–86
  ~~callers~~ call sites each *(86, 16, 81, 15 counting anonymous-thunk callers; as calling functions 43, 11, 52, 10)* and land with whichever subsystem scope claims them.
- The `0x1CEBDA0` sign-mask constant and `0xD11200` face table are read, not
  owned — ~~their full contents are cited from the authority image, not
  reproduced here.~~ *Corrected 2026-09-30 (SWE2-CONTRACT, DD batch 10): their contents are now reproduced, in
  "Constants and the planted siblings" below.*
- [x] **Whether the shape record's `+0x10`/`+0x50` transform pair is authored or built per query.** The nav
  subrecords that carry shapes sit in the loaded nav table (`q[tab+0x18]`, 144-byte stride), which points to
  authored data; the pair builder `00230790` writes the shared transform workbench (matrix 0's first row), which
  points to per-query frames. Neither write into a shape record's `+0x10`/`+0x50` is traced. **SD-182**
  (SWE2-DATA, 2026-09-30). *(Answered 2026-09-30 (SWE2-ORACLE `8acf79ac7`); register row SD-182, record [`sd182-nav-transform-pair-0930`](../_index/candidates/sd182-nav-transform-pair-0930/README.md): authored. The map pack's nav chunk carries both matrices, `+0x50` is the inverse of `+0x10` in the file bytes (all 89,330 shipped subrecords, to float32 rounding), and the engine points at those bytes and never writes them; `00230790`'s workbench is a different object.)*

## Constants and the planted siblings (SWE2-CONTRACT for OPUS)

*For the player:* nothing changes. A box collision shape is a unit cube with six faces, and a point up to one
thousandth outside a face still counts as inside. The checks are in
[`b10_checks.py`](../_index/candidates/swe2contract-ddres-b10-0930/b10_checks.py) (S1–S3), static, on the shipping
image. DD batch 10, 2026-09-30.

**The face table `00D11200` (S1).** Six `vec4` planes `{nx, ny, nz, d}`, each with `d = 1.0`, give the six faces of
the unit cube:

| face | `+x` | `-x` | `+y` | `-y` | `+z` | `-z` |
|---|---|---|---|---|---|---|
| address | `00D11200` | `00D11210` | `00D11220` | `00D11230` | `00D11240` | `00D11250` |
| normal | `(1, 0, 0)` | `(-1, 0, 0)` | `(0, 1, 0)` | `(0, -1, 0)` | `(0, 0, 1)` | `(0, 0, -1)` |

The box primitive takes the table (`003814FF`) and its `+4` column (`003814F0`), and loads the margin `1.001` from
`00D112A4` (`003814F7`).

**The sign mask `01CEBDA0` (S2).** Four `0x80000000` dwords: an `xorps` mask that negates four floats. Its neighbour
`01CEBD80` is a different constant: two `0x7FFFFFFFFFFFFFFF` qwords, the `f64` absolute-value mask that A1D30 applies
(`003A1D37`). That is the control.

**The sibling bodies (S3).** These are read at call level only and have not been executed. Sizes are the v4
extents. The callee lists leave out the stack-cookie check `00808C40` and `sqrtf` `00861F14`.

| VA | size | reached by | callees |
|---|---:|---|---|
| `0022D7E0` | 1,659 B | planted by `lea` at `002316B7` (`00231690`) and `00232B22` (`002327D0`) | `00230790`, `00381D90`, `003810B0`, `0022E7D0` |
| `0022DE60` | 1,240 B | planted by `lea` at `00230EB1` **and `0023126A`**, both in `00230C10` | `0022EAC0`, `003810B0`, `00381D90` |
| `00230790` | 688 B | `0022D7E0` | `00202C70`, `00202D50`, `00202D70`, `00203170` |
| `0022E7D0` | 740 B | `0022D7E0` | `00202E10` |
| `003810B0` | 923 B | `0022D7E0`, `0022DE60` | `00202B70`, the box primitive `00381450` |
| `00381D90` | 288 B | `0022D7E0`, `0022DE60`, `00232160` | `00202B70`, `00380800`, `00380E00`, `00380EB0` |
| `00382020` | 94 B | the cylinder primitive (twice), `0046DB50` | none (D2020, the point-in-unit-cylinder test of the formulas) |

The second plant of `0022DE60` (`0023126A`) is new; EXP-139 names only `00230EB1`. `003810B0`
reaches only the box primitive, not the sphere or cylinder ones. D5A0, DA730 and A1D30 (`003DA5A0`, `003DA730`,
`003A1D30`) have their owner on the separation-pass page, as "Who reaches it" says.

| claim | evidence | tier |
|---|---|---|
| the face table and the margin | S1 | 1 |
| the sign mask, with its abs-mask neighbour as control | S2 | 1 |
| the siblings' sizes, plants and callees | S3 | 1 |

## 4. Evidence

Executed parity evidence: `Database/FFXII TZA/_experiments/evidence/
nav-residual-boundary-exec/` and `nav-region-query-exec/` — `check.py`,
`bodies.json` (per-body sha256 over the shipped bytes), `result.json`.
Fixture-backed parity is MODEL-PROVEN, not game-level or replay authority.

## Falsification pass 1 — 2026-09-29 (OPUS): the toolbox holds; the "dead" siblings are planted callbacks

Every static claim was re-derived from the shipping image by
[`falsify_unit_shape.py`](../../Tools/analysis-kit/gfz-scripts/falsify_unit_shape.py), whose output is in
[`falsify_unit_shape.out`](../../Tools/analysis-kit/gfz-scripts/falsify_unit_shape.out). Killers first.

| check | killer searched for | result |
|---|---|---|
| U0 | a different span | survives: all ten |
| U1 | a primitive FA0 does not reach | survives: the sphere, cylinder and box primitives |
| U2 | another table or margin | survives: the box reads `00D11200` and the constant 1.001; CF50 reads `00908DE8` |
| U3 | a sphere solve without `acosf` / `sinf` | survives: `acosf`, `sinf` (and `sqrtf`, `0046BF60`) |
| U4 | F430 taking D4B0's address | **corrected**: only F430's caller `002315E0` takes it, then calls F430 |
| U5 | any inbound reference to the five "dead" bodies | **refuted**: `0022D7E0` and `0022DE60` are planted by `lea` in `00231690`, `002327D0` and `00230C10`, and they call the other three |
| U6 | a broken push-out chain | survives: `00381D90` ← `00232160` ← `003D97E0` |
| U7 | a leaf outside 15–86 | survives **as call sites** (86, 16, 81, 15); as calling functions the range is 10–52 |

**Why it was missed.** A census of `call` / `jmp` targets sees a function reached only through an address it hands to
someone else as unreferenced. The `lea` plants are exactly the mechanism this page already names for D4B0. The same "no
`lea`" statement is in [EXP-139](../_experiments/EXP-139-nav-region-query-exec.md), which is its author's record, so the
correction is routed. The consumer record is
[`unit-shape-falsification-pass-1-0929`](../_index/candidates/unit-shape-falsification-pass-1-0929/README.md).

## Cross-subsystem neighbours — SWE2-EC7 (pass-22 dispositions)

- **ActorEntity - CLIENT (3 edges).** `003DA5A0` is also called by bodies filed to ActorEntity: `0025BAD0`, `0025C230`, `0025C830` - shared machinery across the layer boundary, no shared ownership.
- **CombatAI - CLIENT (1 edge).** `002315E0` is also called by bodies filed to combat AI: `0032A4D0` - shared machinery across the layer boundary, no shared ownership.
- **Presentation - CLIENT (7 edges).** `00230C00`, `00231690` are also called by bodies filed to presentation: `0032BCC0`, `0032BEB0`, `0032CA70` - shared machinery across the layer boundary, no shared ownership.

## Homed bodies: functions reached only indirectly whose callees this page cites (OPUS, 2026-10-02, F homing)

*No page cited these functions and none of their callers is documented: they are reached by table or pointer dispatch or through undocumented callers. Each one calls something this page documents, which the sentence names. Each sentence states what the body does (access and representation, not purpose); the anchors are instructions inside it that do it. Drafted locally and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../_index/candidates/opus-the-unit-shape-distance-primitives-homing-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `0022CC50` | 765 B | scans the word `+0x40` ids listed from word `+0x3E` in the index array at qword `+0x28` of `rcx`, skipping ids from 0x5000 up; an id from 0x4000 is a 0x90-byte record of qword `+0x18`, a lower id a 32-byte record of qword `+0x10`, and either record's flags dword (`+4` / `+0xC`) is overridden per group (bits 13-17 plus 0x20) by the mask / value pairs at `0209A2D0` + 0x110; type 1 is skipped when the top bit is set or bit `0x40000000` is set with word `+0x46` of `rdx` equal to 4, and a low record of type 4 is kept only when that word is 4 (for low records every other non-zero type is skipped); a distance from `00380FA0` (high ids) or `0022E6D0` (low ids, whose hit point at the query origin plus the direction times distance / float `+0x34` must also pass `0022CF50(rcx, id, &point)`) that is non-negative and below float `+0x30` of `rdx` is stored there with its 16-byte point at qword `+0x20` and the id at word `+0x42`; the scan stops at the first hit when dword `+0x38` is non-zero | `0022CCD1`, `0022CCDA`, `0022CD59`, `0022CE60`, `0022CECE` |
