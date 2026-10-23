---
title: "Bullet Physics: the linked rigid-body library, how PhyreEngine bodies become Bullet bodies, and why nothing is simulated"
kind: "system"
category: "Third-party libraries"
addresses: "0x0069FB10, 0x006A0310, 0x006A2320, 0x006A4A60, 0x0069F070, 0x0069EF20, 0x00698C80, 0x006883A0, 0x0069E6F0, 0x00691240, 0x0068B9E0, 0x00832390, 0x00852DB0, 0x008542B0, 0x00854080, 0x0083A3A0, 0x0083A030, 0x00854980, 0x0085E680, 0x008365C0, 0x02E4AFF0, 0x008531F0, 0x008324B0, 0x006A3E20"
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
vtables `btCompoundShape` (`0x00832390`), `btRigidBody` (`0x00852DB0`) and `btDiscreteDynamicsWorld`
(`0x00854980`), and the text `Overflow in AABB, object removed from simulation` (`0x01CCE6A0`) is
Bullet's own warning. There is no version string and no `btGetVersion` constant; the version is
bounded by the serializer's chunk names instead:

- `btStridingMeshInterface::serialize` (`0x008365C0`) names its short-index chunk
  `btShortIntIndexTripletData` (`0x01CCDD58`, loaded at `0x00836762`). The older name
  `btShortIntIndexData` occurs nowhere in the image; upstream Bullet renamed it after the 2.76
  release.
- Its index-type switch has two arms, integer (type 2) and short (type 3), at `0x008366DA` to
  `0x008366E6`. The name `btCharIndexTripletData`, which belongs to the third (byte) arm that every
  release from 2.78 carries, occurs nowhere in the image.
- No `m_rollingFriction` name and no multibody type name is present.

The only Bullet release between those two upstream changes is 2.77, so the linked library is the
2.77 line. The library's code sits from `0x00830760` (`btCollisionShape::calculateTemporalAabb`) up to
the import thunks at `0x00861E90`, plus a second block from `0x0087F180`, whose first function sorts
contact manifolds by their bodies' island tags (`+0xEC`).

### The route from a Phyre scene to Bullet

PhyreEngine wraps Bullet in its `PPhysics` classes; the Bullet-backed ones are named in the image as
`PPhysicsRigidBodyBullet`, `PPhysicsShapeBullet`, `PPhysicsBoxBullet`, `PPhysicsSphereBullet`,
`PPhysicsCapsuleBullet`, `PPhysicsCylinderBullet`, `PPhysicsPlaneBullet`, `PPhysicsMeshBullet` and
`PPhysicsCharacterControllerBullet`. The single route into Bullet is a chain of four calls:

1. `0x006883A0` is slot 14 of both class descriptors of `PPhysicsWorld` (vtables `0x00D70BC8` and
   `0x00D70ED0`) and has no direct caller. It passes its second argument, an array of `PPhysicsWorld`
   instances (data `+0x58`, count `+0x70`, stride at `+0x38` of the class record at `+0x50`), to
   `0x00698C80`.
2. `0x00698C80` returns at once unless the first byte of the physics manager is set. Otherwise, for
   each `PPhysicsWorld` instance, it builds the Bullet world (`0x006A0310`) and walks the world's body
   lists (`0x0069EF20`).
3. `0x0069EF20` calls `0x0069F070` for every rigid body in every list and links each body to its list.
4. `0x0069F070` removes the body from a Bullet world it is already in (world slot `+0xA0`), builds the
   Bullet body when it has none (`0x0069FB10`), builds the world if it is still missing, and puts a
   body that was in a world back into it (`0x006A65A0`).

`0x0069FB10` is the only caller of the `btRigidBody` constructor and `0x006A0310` the only caller of the
`btDiscreteDynamicsWorld` constructor.

### The physics manager, and why the route never runs

The manager is a static object at `0x02E4AFF0`, created on first use by `0x0069E6F0`. Its first byte is
the enable flag, and the qwords at `+0x18`, `+0x20` and `+0x28` are the collision configuration,
collision dispatcher and constraint solver a world needs. Its constructor `0x00691240` clears the enable
byte and sets `+0x08` to `0x10`; it does not write the three slots, which keep the static object's
zero fill.

Only three functions obtain the manager (`0x00698C80`, `0x006A0310` and the script-callback function
`0x00698720`, which reads only its `+0x10`), and none of them writes it. Apart from the getter, its
exit-time destructor `0x008B3BE0` and its unwind funclet `0x008A09F0` (`_Init_thread_abort` on the guard
`0x02E4B090`), no instruction in the image addresses `0x02E4AFF0` to `0x02E4B098`. The enable byte therefore
stays 0, so `0x00698C80` returns before doing anything; and even a direct call to `0x006A0310` returns
`0x15` because the three solver slots stay null.

### Building the world

When its inputs exist, `0x006A0310` builds a `btAxisSweep3` broadphase of 16,384 handles over the
world's box (`0x00838600` with `0x4000`), hands a new `btGhostPairCallback` to the broadphase's pair
cache, creates the `btDiscreteDynamicsWorld` from the manager's dispatcher, solver and configuration,
stores `0x0069E970` in the world's callback slot `+0x90`, and sets gravity from the `PPhysicsWorld`
(world slot `+0x80`, `0x00858560`). When the manager's `+0x08` is not 0, it copies that value into the
`PPhysicsWorld`'s `+0xB8` and sizes two tables with it (`0x006A5450` on `+0x98`, `0x006A54E0` on `+0xA8`).

A failed broadphase allocation (`0x0085E680`) or ghost-callback allocation (`0x00210EC0`) returns `0xE`.
A failed world allocation does not: when `0x0017D260` returns 0 (`je` at `0x006A046D`), the function
falls through to `0x006A04A3`, loads the null world from `+0x60` and writes `+0x90` and `+0xA0` through
it (`0x006A04AE`).

### Building a rigid body

`0x0069FB10` turns one `PPhysicsRigidBody` into Bullet objects:

1. It returns 0 at once when the body already has a Bullet body (`+0x118`).
2. It allocates a 128-byte `btCompoundShape` when there is none (`+0x120`). The one call to the
   constructor passes 0 for the dynamic AABB tree (`0x0069FBBA`), so no compound in the game has one.
3. Each child shape builds itself (its vtable slot `+0x08`); the first failure is returned. The
   children's masses (`+0x0C`) are summed.
4. Each child's scale (`+0x50`) is multiplied by the body's scale (`+0x88`) and set on its Bullet
   shape (slot `+0x28`). This loop reads `+0x50`, `+0x54` and `+0x58` of every child entry without
   the null check the build loop has, so a null child entry crashes the build. The child's transform is written into the compound (`0x00833390`) with the
   body's centre of mass subtracted: x takes minus `+0x28`, y minus `+0x2C`, z minus `+0x30`.
5. Mass and inertia are chosen (see the next heading), and a construction info is filled with
   Bullet's stock defaults (see Layouts).
6. Friction and restitution come from a material: the body's `+0x98`, or else the first child's
   `+0x18`. With neither, the function returns 9 and builds no body.
7. A 704-byte, 16-aligned `btRigidBody` is allocated through Bullet's allocator hook (`0x0085E680`) and
   constructed (`0x00852DB0` → `0x008542B0`); failure returns `0xE`.
8. A non-dynamic body is put to sleep (`0x0083A3A0` with state 2), the Bullet body gets a back-pointer
   to the Phyre body at its `+0x108`, the motion type is applied (`0x006A2320`) and the transform and
   velocities are pushed in (`0x006A4A60`).

### Mass and inertia

The byte `+0xE8` selects the motion type. Only type 1 (dynamic) gets mass: the authored mass `+0xE4`,
or the sum of the children's masses when that is 0, and the authored inertia `+0x58` to `+0x60`, or
the compound's computed inertia (slot `+0x38`) when all three are 0. Every other type is built with
mass 0.

The inertia call (`0x006A0032`) passes the authored mass `+0xE4` (`xmm8`, loaded at `0x0069FFEA`), not
the summed mass. A dynamic body with mass 0 and zero inertia therefore gets the children's summed mass
but an inertia computed for mass 0, which is zero.

### Motion types and collision groups

`0x006A2320(body, type)` sets the Bullet collision flags and activation state:

| Type | Collision flags (`+0xE8` of the Bullet body) | Activation state |
|---|---|---|
| 0, static | static set, kinematic cleared | 2, sleeping |
| 1, dynamic | both cleared | 1, active |
| 2, kinematic | kinematic set, static cleared | 4, never deactivates |
| other | unchanged | unchanged; returns 9 |

The activation write goes through `0x0083A3A0`, which refuses to overwrite states 4 and 5. When the
body's group byte `+0xE0` is 15, it becomes 1 for types 0 and 2 and 0 for type 1.

`0x006A4A60` re-inserts a body. When the body's `+0xE9` is set, it removes it from the Bullet world
of its list (`+0xC8` → `+0x10` → `+0x60`, world slot `+0xA0`). It copies the linear velocity `+0x68`
and angular velocity `+0x78` into the Bullet body, builds its world transform from the orientation
quaternion `+0x48` (`0x006A57C0`), the position `+0x38` and the centre of mass, and, when asked,
re-applies child scales.

Only when `+0xE9` was set does it re-add the body (slot `+0x130`) with group `1 << +0xE0` and the mask
the world keeps for that group (a 16-bit table at its `+0x78`), and wake it (`0x0083A030`). A new body from `0x0069FB10` has `+0xE9` clear, so `0x006A4A60` gives it only its velocities and
transform.

### Bullet bodies outside the member list

Three Bullet functions are not in [`bullet-physics-members.tsv`](bullet-physics-members.tsv):

- `0x008531F0` is `btRigidBody::applyDamping`, called from `0x00857E70`. It multiplies the linear
  velocity `+0x150` by `(1 - linearDamping)` to the power of the time step (damping at `+0x1E0`, via
  `powf`) and the angular velocity `+0x160` the same way with `+0x1E4`.
- When the additional-damping byte `+0x1E8` is set, `0x008531F0` goes on to scale both velocities by
  `+0x1EC` when their squared lengths are below `+0x1F4` (angular) and `+0x1F0` (linear). It then
  pulls each velocity shorter than its damping value toward zero by 0.005, or zeroes it when it is
  no longer than 0.005.
- `0x008324B0` is the `btCompoundShape` destructor body that the deleting destructor `0x00832530` calls.
  It frees the dynamic AABB tree at `+0x60` (`0x00840FC0`, then the aligned free `0x0085E710`), frees the
  child array at `+0x28` when the byte `+0x30` says the shape owns it, and leaves the
  `btCollisionShape` vtable in place.
- `0x006A3E20` converts a 3x3 rotation, rows 16 bytes apart, to a quaternion `x, y, z, w`: from the
  trace when it is positive, otherwise from the largest diagonal element. The linker placed it at
  `0x006A3E20`, outside both Bullet ranges; its only callers are Bullet's `0x0083B050` (`0x0083B3DC`),
  `0x0083B580` (`0x0083B6A8`) and `0x0084C6B0` (`0x0084C855`).

## Layouts

`PPhysicsRigidBody`, the fields the Bullet route reads and writes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x028` | `f32[3]` | centreOfMass | subtracted from every child's position in the compound |
| `+0x038` | `f32[3]` | position |  |
| `+0x048` | `f32[4]` | orientation | quaternion x, y, z, w |
| `+0x058` | `f32[3]` | inertia | all zero: computed from the compound shape |
| `+0x068` | `f32[3]` | linearVelocity |  |
| `+0x078` | `f32[3]` | angularVelocity |  |
| `+0x088` | `f32[3]` | scale | multiplies every child's scale |
| `+0x098` | `void*` | material | friction at +`0x04`, restitution at +`0x08` |
| `+0x0B0` | `u32` | childCount | bit 31 is a flag; one child is stored inline at +`0xB8` |
| `+0x0B8` | `void*` | children | the child array, or the single child itself |
| `+0x0C0` | `f32[2]` | damping | linear, angular |
| `+0x0E0` | `u8` | collisionGroup | index into the world's mask table |
| `+0x0E4` | `f32` | mass | 0: the children's summed mass |
| `+0x0E8` | `u8` | motionType | 0 static, 1 dynamic, 2 kinematic |
| `+0x0E9` | `u8` | inWorld | set when the Bullet body is in a world |
| `+0x118` | `void*` | bulletBody | btRigidBody, set once |
| `+0x120` | `void*` | compoundShape | btCompoundShape |

The construction info `0x0069FB10` fills, as `0x008542B0` reads it:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `f32` | mass |  |
| `+0x08` | `void*` | motionState | 0 |
| `+0x10` | `f32[16] startWorldTransform` | identity |  |
| `+0x50` | `void*` | collisionShape | the compound |
| `+0x60` | `f32[4]` | localInertia |  |
| `+0x70` | `f32[2]` | linearDamping, angularDamping | from +`0xC0`, clamped to 0..1 by `0x00854080` |
| `+0x78` | `f32[2]` | friction, restitution | from the material |
| `+0x80` | `f32` | linearSleepingThreshold | 0.8 |
| `+0x84` | `f32` | angularSleepingThreshold | 1.0 |
| `+0x88` | `u8` | additionalDamping | 0 |
| `+0x8C` | `f32` | additionalDampingFactor | 0.005 |
| `+0x90` | `f32` | additionalLinearDampingThresholdSqr 0.01 |  |
| `+0x94` | `f32` | additionalAngularDampingThresholdSqr 0.01 |  |
| `+0x98` | `f32` | additionalAngularDampingFactor | 0.01 |

`PPhysicsWorld`'s default instance (`0x0068B9E0`): gravity (0, -9.8, 0) at `+0x00`, 1.0 at `+0x10`, and
the broadphase box from (-5000, -5000, -5000) at `+0x14` to (5000, 5000, 5000) at `+0x24`.

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

## State

Six statistics globals of the library, all 0 in the zero-filled tail of `.data`. Like the rest of the library they
run only inside a world, which the game never builds (above).

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02EAF390` | `i32` | 0 | the count of pair removals: the hashed pair cache's remove `0x00848960` adds 1 on entry, before it orders the two proxies by their id `+0x18` and looks the pair up | `0x00848960` (`0x00848971`, `inc`) | only that increment |
| `0x02EAF394` | `i32` | 0 | the count of pair-add requests: `0x00848170` adds 1 before the filter test (the callback at the cache's `+0x28`, or the two proxies' group and mask words `+0x08`/`+0x0A`) and the jump to the insert `0x008485E0` | `0x00848170` (`0x0084817F`, `inc`) | only that increment |
| `0x02EAF398` | `i32` | 0 | the count of pair lookups: `0x00848270` adds 1 on entry | `0x00848270` (`0x00848275`, `inc`) | only that increment |
| `0x02EAF39C` | `i32` | 0 | the count of overlapping pairs, which the game only lowers: by 1 for each pair `0x00848880` removes after the callback's test (`0x008488C0`, removal through `+0x10`), and for each pair the sweep-and-prune pass `0x00838D80` finds no longer overlapping on the three 16-bit axes (`0x00838F60`-`0x00838F89`) | `0x00848880` (`0x008488DA`, `dec`); `0x00838D80` (`0x00838FAE`, `dec`) | only those decrements |
| `0x02EAF3C0` | `u8` | 0 | the no-deactivation switch: the world step `0x008588A0` sets it, when the world has a debug drawer (`0x00858938`), to bit 4 (`0x10`) of the drawer's debug mode (`0x0085894F`-`0x00858955`); while it is non-zero `0x00858C80` puts no body to sleep | `0x008588A0` (`0x00858957`) | `0x00858C80` (`0x00858DA7`) |
| `0x02EAF3CC` | `i32` | 0 | the count of split-impulse recoveries: each of the two contact passes `0x0085A900` and `0x0085AC50` adds 1 for a contact row whose penetration term `+0xA8` is not 0 | `0x0085A900` (`0x0085A91F`, `inc`); `0x0085AC50` (`0x0085AC6B`, `inc`) | only those increments |

No other instruction reaches these six globals.

## Modding notes

- The whole route is dormant. Adding `PPhysicsWorld` and `PPhysicsRigidBody` objects to a cluster is
  not enough: the manager at `0x02E4AFF0` also needs its enable byte and its dispatcher, solver and
  collision configuration, which no code in the game creates.
- Set the motion type, mass and inertia before the Bullet body is built; `0x0069FB10` runs once per
  body.
- A dynamic body with mass 0 is not static: it takes its children's summed mass. With zero inertia
  as well, its inertia is computed for mass 0 and is zero, so Bullet never rotates it; author the
  mass or the inertia.
- A body without a material on itself or on any child is never built (return 9).
- Damping outside 0..1 is clamped by `0x00854080`.
- Bullet's allocator hooks are four pointers from `0x01F44CE0` (allocate, free, aligned allocate at
  `0x01F44CF0`, aligned free); `0x0085E680` counts live aligned allocations at `0x02EAF6C4` and calls the
  hook.

## Related

- PhyreEngine: the engine whose `PPhysics` classes wrap
  Bullet.
- [Movement bodies and separation](../Movement-And-Pathfinding/movement-bodies-and-separation.md):
  the collision bodies the game actually uses for actors.
- [Heading and speed to position](../Movement-And-Pathfinding/heading-speed-to-position-delta.md):
  how actors move without physics.
- `bullet-physics-members.tsv`: the library's functions in its two link ranges.
- The field accesses of the `PPhysics` classes' class descriptors and vtables, one table per class:
  - [`bullet-physics-pphysics-capsule-base-accesses.tsv`](bullet-physics-pphysics-capsule-base-accesses.tsv);
  - [`bullet-physics-pphysics-character-camera-accesses.tsv`](bullet-physics-pphysics-character-camera-accesses.tsv);
  - [`bullet-physics-pphysics-character-controller-base-accesses.tsv`](bullet-physics-pphysics-character-controller-base-accesses.tsv);
  - [`bullet-physics-pphysics-character-controller-bullet-accesses.tsv`](bullet-physics-pphysics-character-controller-bullet-accesses.tsv);
  - [`bullet-physics-pphysics-cylinder-base-accesses.tsv`](bullet-physics-pphysics-cylinder-base-accesses.tsv);
  - [`bullet-physics-pphysics-interface-base-accesses.tsv`](bullet-physics-pphysics-interface-base-accesses.tsv);
  - [`bullet-physics-pphysics-interface-bullet-accesses.tsv`](bullet-physics-pphysics-interface-bullet-accesses.tsv);
  - [`bullet-physics-pphysics-rigid-body-base-accesses.tsv`](bullet-physics-pphysics-rigid-body-base-accesses.tsv);
  - [`bullet-physics-pphysics-shape-base-accesses.tsv`](bullet-physics-pphysics-shape-base-accesses.tsv);
  - [`bullet-physics-pphysics-shape-bullet-accesses.tsv`](bullet-physics-pphysics-shape-bullet-accesses.tsv);
  - [`bullet-physics-pphysics-sphere-base-accesses.tsv`](bullet-physics-pphysics-sphere-base-accesses.tsv);
  - [`bullet-physics-pphysics-tapered-capsule-accesses.tsv`](bullet-physics-pphysics-tapered-capsule-accesses.tsv);
  - [`bullet-physics-pphysics-tapered-cylinder-accesses.tsv`](bullet-physics-pphysics-tapered-cylinder-accesses.tsv);
  - [`bullet-physics-pphysics-world-base-accesses.tsv`](bullet-physics-pphysics-world-base-accesses.tsv);
  - [`bullet-physics-pphysics-world-bullet-accesses.tsv`](bullet-physics-pphysics-world-bullet-accesses.tsv).
