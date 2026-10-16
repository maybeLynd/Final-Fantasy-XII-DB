---
title: "Bullet Physics: the linked rigid-body library, how PhyreEngine bodies become Bullet bodies, and why nothing is simulated"
kind: "system"
category: "Third-party libraries"
addresses: "0069FB10, 006A0310, 006A2320, 006A4A60, 0069F070, 0069EF20, 00698C80, 006883A0, 0069E6F0, 00691240, 0068B9E0, 00832390, 00852DB0, 008542B0, 00854080, 0083A3A0, 0083A030, 00854980, 0085E680, 008365C0, 02E4AFF0, 008531F0, 008324B0, 006A3E20"
---

## What the player sees

Nothing. No object in the game is moved by rigid-body physics: characters, monsters and props are
placed by animation, scripts and the game's own movement code. The Bullet library and the
PhyreEngine code that would feed it are in the executable, but the physics manager they depend on is
never switched on and no shipped asset declares a physics object, so no Bullet world or body is ever
created.

## How it works

### Identity and version

The library identifies itself through its own class names. The constructors write the RTTI-named
vtables `btCompoundShape` (`00832390`), `btRigidBody` (`00852DB0`) and `btDiscreteDynamicsWorld`
(`00854980`), and the text `Overflow in AABB, object removed from simulation` (`01CCE6A0`) is
Bullet's own warning. There is no version string and no `btGetVersion` constant; the version is
bounded by the serializer's chunk names instead:

- `btStridingMeshInterface::serialize` (`008365C0`) names its short-index chunk
  `btShortIntIndexTripletData` (`01CCDD58`, loaded at `00836762`). The older name
  `btShortIntIndexData` occurs nowhere in the image; upstream Bullet renamed it after the 2.76
  release.
- Its index-type switch has two arms, integer (type 2) and short (type 3), at `008366DA` to
  `008366E6`. The name `btCharIndexTripletData`, which belongs to the third (byte) arm that every
  release from 2.78 carries, occurs nowhere in the image.
- No `m_rollingFriction` name and no multibody type name is present.

The only Bullet release between those two upstream changes is 2.77, so the linked library is the
2.77 line. The library's code sits from `00830760` (`btCollisionShape::calculateTemporalAabb`) up to
the import thunks at `00861E90`, plus a second block from `0087F180`, whose first function sorts
contact manifolds by their bodies' island tags (`+EC`<sub>h</sub>).

### The route from a Phyre scene to Bullet

PhyreEngine wraps Bullet in its `PPhysics` classes; the Bullet-backed ones are named in the image as
`PPhysicsRigidBodyBullet`, `PPhysicsShapeBullet`, `PPhysicsBoxBullet`, `PPhysicsSphereBullet`,
`PPhysicsCapsuleBullet`, `PPhysicsCylinderBullet`, `PPhysicsPlaneBullet`, `PPhysicsMeshBullet` and
`PPhysicsCharacterControllerBullet`. The single route into Bullet is a chain of four calls:

1. `006883A0` is slot 14 of both class descriptors of `PPhysicsWorld` (vtables `00D70BC8` and
   `00D70ED0`) and has no direct caller. It passes its second argument, an array of `PPhysicsWorld`
   instances (data `+58`<sub>h</sub>, count `+70`<sub>h</sub>, stride at `+38`<sub>h</sub> of the class record at `+50`<sub>h</sub>), to
   `00698C80`.
2. `00698C80` returns at once unless the first byte of the physics manager is set. Otherwise, for
   each `PPhysicsWorld` instance, it builds the Bullet world (`006A0310`) and walks the world's body
   lists (`0069EF20`).
3. `0069EF20` calls `0069F070` for every rigid body in every list and links each body to its list.
4. `0069F070` removes the body from a Bullet world it is already in (world slot `+A0`<sub>h</sub>), builds the
   Bullet body when it has none (`0069FB10`), builds the world if it is still missing, and puts a
   body that was in a world back into it (`006A65A0`).

`0069FB10` is the only caller of the `btRigidBody` constructor and `006A0310` the only caller of the
`btDiscreteDynamicsWorld` constructor.

### The physics manager, and why the route never runs

The manager is a static object at `02E4AFF0`, created on first use by `0069E6F0`. Its first byte is
the enable flag, and the qwords at `+18`<sub>h</sub>, `+20`<sub>h</sub> and `+28`<sub>h</sub> are the collision configuration,
collision dispatcher and constraint solver a world needs. Its constructor `00691240` clears the enable
byte and sets `+08`<sub>h</sub> to `10`<sub>h</sub>; it does not write the three slots, which keep the static object's
zero fill.

Only three functions obtain the manager (`00698C80`, `006A0310` and the script-callback function
`00698720`, which reads only its `+10`<sub>h</sub>), and none of them writes it. Apart from the getter, its
exit-time destructor `008B3BE0` and its unwind funclet `008A09F0` (`_Init_thread_abort` on the guard
`02E4B090`), no instruction in the image addresses `02E4AFF0` to `02E4B098`. The enable byte therefore
stays 0, so `00698C80` returns before doing anything; and even a direct call to `006A0310` returns
`15`<sub>h</sub> because the three solver slots stay null.

### Building the world

When its inputs exist, `006A0310` builds a `btAxisSweep3` broadphase of 16,384 handles over the
world's box (`00838600` with `4000`<sub>h</sub>), hands a new `btGhostPairCallback` to the broadphase's pair
cache, creates the `btDiscreteDynamicsWorld` from the manager's dispatcher, solver and configuration,
stores `0069E970` in the world's callback slot `+90`<sub>h</sub>, and sets gravity from the `PPhysicsWorld`
(world slot `+80`<sub>h</sub>, `00858560`). When the manager's `+08`<sub>h</sub> is not 0, it copies that value into the
`PPhysicsWorld`'s `+B8`<sub>h</sub> and sizes two tables with it (`006A5450` on `+98`<sub>h</sub>, `006A54E0` on `+A8`<sub>h</sub>).

A failed broadphase allocation (`0085E680`) or ghost-callback allocation (`00210EC0`) returns `E`<sub>h</sub>.
A failed world allocation does not: when `0017D260` returns 0 (`je` at `006A046D`), the function
falls through to `006A04A3`, loads the null world from `+60`<sub>h</sub> and writes `+90`<sub>h</sub> and `+A0`<sub>h</sub> through
it (`006A04AE`).

### Building a rigid body

`0069FB10` turns one `PPhysicsRigidBody` into Bullet objects:

1. It returns 0 at once when the body already has a Bullet body (`+118`<sub>h</sub>).
2. It allocates a 128-byte `btCompoundShape` when there is none (`+120`<sub>h</sub>). The one call to the
   constructor passes 0 for the dynamic AABB tree (`0069FBBA`), so no compound in the game has one.
3. Each child shape builds itself (its vtable slot `+08`<sub>h</sub>); the first failure is returned. The
   children's masses (`+0C`<sub>h</sub>) are summed.
4. Each child's scale (`+50`<sub>h</sub>) is multiplied by the body's scale (`+88`<sub>h</sub>) and set on its Bullet
   shape (slot `+28`<sub>h</sub>). This loop reads `+50`<sub>h</sub>, `+54`<sub>h</sub> and `+58`<sub>h</sub> of every child entry without
   the null check the build loop has, so a null child entry crashes the build. The child's transform is written into the compound (`00833390`) with the
   body's centre of mass subtracted: x takes minus `+28`<sub>h</sub>, y minus `+2C`<sub>h</sub>, z minus `+30`<sub>h</sub>.
5. Mass and inertia are chosen (see the next heading), and a construction info is filled with
   Bullet's stock defaults (see Layouts).
6. Friction and restitution come from a material: the body's `+98`<sub>h</sub>, or else the first child's
   `+18`<sub>h</sub>. With neither, the function returns 9 and builds no body.
7. A 704-byte, 16-aligned `btRigidBody` is allocated through Bullet's allocator hook (`0085E680`) and
   constructed (`00852DB0` → `008542B0`); failure returns `E`<sub>h</sub>.
8. A non-dynamic body is put to sleep (`0083A3A0` with state 2), the Bullet body gets a back-pointer
   to the Phyre body at its `+108`<sub>h</sub>, the motion type is applied (`006A2320`) and the transform and
   velocities are pushed in (`006A4A60`).

### Mass and inertia

The byte `+E8`<sub>h</sub> selects the motion type. Only type 1 (dynamic) gets mass: the authored mass `+E4`<sub>h</sub>,
or the sum of the children's masses when that is 0, and the authored inertia `+58`<sub>h</sub> to `+60`<sub>h</sub>, or
the compound's computed inertia (slot `+38`<sub>h</sub>) when all three are 0. Every other type is built with
mass 0.

The inertia call (`006A0032`) passes the authored mass `+E4`<sub>h</sub> (`xmm8`, loaded at `0069FFEA`), not
the summed mass. A dynamic body with mass 0 and zero inertia therefore gets the children's summed mass
but an inertia computed for mass 0, which is zero.

### Motion types and collision groups

`006A2320(body, type)` sets the Bullet collision flags and activation state:

| Type | Collision flags (`+E8`<sub>h</sub> of the Bullet body) | Activation state |
|---|---|---|
| 0, static | static set, kinematic cleared | 2, sleeping |
| 1, dynamic | both cleared | 1, active |
| 2, kinematic | kinematic set, static cleared | 4, never deactivates |
| other | unchanged | unchanged; returns 9 |

The activation write goes through `0083A3A0`, which refuses to overwrite states 4 and 5. When the
body's group byte `+E0`<sub>h</sub> is 15, it becomes 1 for types 0 and 2 and 0 for type 1.

`006A4A60` re-inserts a body. When the body's `+E9`<sub>h</sub> is set, it removes it from the Bullet world
of its list (`+C8`<sub>h</sub> → `+10`<sub>h</sub> → `+60`<sub>h</sub>, world slot `+A0`<sub>h</sub>). It copies the linear velocity `+68`<sub>h</sub>
and angular velocity `+78`<sub>h</sub> into the Bullet body, builds its world transform from the orientation
quaternion `+48`<sub>h</sub> (`006A57C0`), the position `+38`<sub>h</sub> and the centre of mass, and, when asked,
re-applies child scales.

Only when `+E9`<sub>h</sub> was set does it re-add the body (slot `+130`<sub>h</sub>) with group `1 << +E0h` and the mask
the world keeps for that group (a 16-bit table at its `+78`<sub>h</sub>), and wake it (`0083A030`). A new body from `0069FB10` has `+E9`<sub>h</sub> clear, so `006A4A60` gives it only its velocities and
transform.

### Bullet bodies outside the member list

Three Bullet functions are not in `bullet-physics-members.tsv`:

- `008531F0` is `btRigidBody::applyDamping`, called from `00857E70`. It multiplies the linear
  velocity `+150`<sub>h</sub> by `(1 - linearDamping)` to the power of the time step (damping at `+1E0`<sub>h</sub>, via
  `powf`) and the angular velocity `+160`<sub>h</sub> the same way with `+1E4`<sub>h</sub>.
- When the additional-damping byte `+1E8`<sub>h</sub> is set, `008531F0` goes on to scale both velocities by
  `+1EC`<sub>h</sub> when their squared lengths are below `+1F4`<sub>h</sub> (angular) and `+1F0`<sub>h</sub> (linear). It then
  pulls each velocity shorter than its damping value toward zero by 0.005, or zeroes it when it is
  no longer than 0.005.
- `008324B0` is the `btCompoundShape` destructor body that the deleting destructor `00832530` calls.
  It frees the dynamic AABB tree at `+60`<sub>h</sub> (`00840FC0`, then the aligned free `0085E710`), frees the
  child array at `+28`<sub>h</sub> when the byte `+30`<sub>h</sub> says the shape owns it, and leaves the
  `btCollisionShape` vtable in place.
- `006A3E20` converts a 3x3 rotation, rows 16 bytes apart, to a quaternion `x, y, z, w`: from the
  trace when it is positive, otherwise from the largest diagonal element. The linker placed it at
  `006A3E20`, outside both Bullet ranges; its only callers are Bullet's `0083B050` (`0083B3DC`),
  `0083B580` (`0083B6A8`) and `0084C6B0` (`0084C855`).

## Layouts

`PPhysicsRigidBody`, the fields the Bullet route reads and writes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `028`<sub>h</sub> | `f32[3]` | centreOfMass | subtracted from every child's position in the compound |
| `038`<sub>h</sub> | `f32[3]` | position |  |
| `048`<sub>h</sub> | `f32[4]` | orientation | quaternion x, y, z, w |
| `058`<sub>h</sub> | `f32[3]` | inertia | all zero: computed from the compound shape |
| `068`<sub>h</sub> | `f32[3]` | linearVelocity |  |
| `078`<sub>h</sub> | `f32[3]` | angularVelocity |  |
| `088`<sub>h</sub> | `f32[3]` | scale | multiplies every child's scale |
| `098`<sub>h</sub> | `void*` | material | friction at +`04`<sub>h</sub>, restitution at +`08`<sub>h</sub> |
| `0B0`<sub>h</sub> | `u32` | childCount | bit 31 is a flag; one child is stored inline at +`B8`<sub>h</sub> |
| `0B8`<sub>h</sub> | `void*` | children | the child array, or the single child itself |
| `0C0`<sub>h</sub> | `f32[2]` | damping | linear, angular |
| `0E0`<sub>h</sub> | `u8` | collisionGroup | index into the world's mask table |
| `0E4`<sub>h</sub> | `f32` | mass | 0: the children's summed mass |
| `0E8`<sub>h</sub> | `u8` | motionType | 0 static, 1 dynamic, 2 kinematic |
| `0E9`<sub>h</sub> | `u8` | inWorld | set when the Bullet body is in a world |
| `118`<sub>h</sub> | `void*` | bulletBody | btRigidBody, set once |
| `120`<sub>h</sub> | `void*` | compoundShape | btCompoundShape |

The construction info `0069FB10` fills, as `008542B0` reads it:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `f32` | mass |  |
| `08`<sub>h</sub> | `void*` | motionState | 0 |
| `10`<sub>h</sub> | `f32[16] startWorldTransform` | identity |  |
| `50`<sub>h</sub> | `void*` | collisionShape | the compound |
| `60`<sub>h</sub> | `f32[4]` | localInertia |  |
| `70`<sub>h</sub> | `f32[2]` | linearDamping, angularDamping | from +`C0`<sub>h</sub>, clamped to 0..1 by `00854080` |
| `78`<sub>h</sub> | `f32[2]` | friction, restitution | from the material |
| `80`<sub>h</sub> | `f32` | linearSleepingThreshold | 0.8 |
| `84`<sub>h</sub> | `f32` | angularSleepingThreshold | 1.0 |
| `88`<sub>h</sub> | `u8` | additionalDamping | 0 |
| `8C`<sub>h</sub> | `f32` | additionalDampingFactor | 0.005 |
| `90`<sub>h</sub> | `f32` | additionalLinearDampingThresholdSqr 0.01 |  |
| `94`<sub>h</sub> | `f32` | additionalAngularDampingThresholdSqr 0.01 |  |
| `98`<sub>h</sub> | `f32` | additionalAngularDampingFactor | 0.01 |

`PPhysicsWorld`'s default instance (`0068B9E0`): gravity (0, -9.8, 0) at `+00`<sub>h</sub>, 1.0 at `+10`<sub>h</sub>, and
the broadphase box from (-5000, -5000, -5000) at `+14`<sub>h</sub> to (5000, 5000, 5000) at `+24`<sub>h</sub>.

## Shipped data

| Fact | Value |
|---|---|
| `.phyre` files in the archive | 35,984 (27,154,292,432 bytes) |
| files containing the text `Physics` | 0 |
| files containing `PPhysicsWorld` or `PPhysicsRigidBody` | 0 |
| control: files containing `PEffect` | 2,184 |
| control: files containing `PContextSwitch` | 2,184 |

No shipped cluster declares or instantiates a `PPhysics` class, so even with the manager enabled the
class-descriptor callback would have no instances to visit.

## Modding notes

- The whole route is dormant. Adding `PPhysicsWorld` and `PPhysicsRigidBody` objects to a cluster is
  not enough: the manager at `02E4AFF0` also needs its enable byte and its dispatcher, solver and
  collision configuration, which no code in the game creates.
- Set the motion type, mass and inertia before the Bullet body is built; `0069FB10` runs once per
  body.
- A dynamic body with mass 0 is not static: it takes its children's summed mass. With zero inertia
  as well, its inertia is computed for mass 0 and is zero, so Bullet never rotates it; author the
  mass or the inertia.
- A body without a material on itself or on any child is never built (return 9).
- Damping outside 0..1 is clamped by `00854080`.
- Bullet's allocator hooks are four pointers from `01F44CE0` (allocate, free, aligned allocate at
  `01F44CF0`, aligned free); `0085E680` counts live aligned allocations at `02EAF6C4` and calls the
  hook.

## Related

- PhyreEngine: the engine whose `PPhysics` classes wrap
  Bullet.
- [Movement bodies and separation](../Movement-And-Pathfinding/movement-bodies-and-separation.md):
  the collision bodies the game actually uses for actors.
- [Heading and speed to position](../Movement-And-Pathfinding/heading-speed-to-position-delta.md):
  how actors move without physics.
- `bullet-physics-members.tsv`: the library's functions in its two link ranges.
- The `bullet-physics-pphysics-*-accesses.tsv` files beside this page: the field accesses of the
  `PPhysics` classes' class descriptors and vtables.
