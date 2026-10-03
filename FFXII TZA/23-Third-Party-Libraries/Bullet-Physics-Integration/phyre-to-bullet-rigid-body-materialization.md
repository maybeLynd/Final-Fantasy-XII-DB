---
system: Phyre-to-Bullet rigid body materialization
category: 23-Third-Party-Libraries
status: AUDITED — the exact Bullet version (UQ-302) is SUPERSEDED as a duplicate of BN-1, answered 2026-09-26 (the 2.77 line); the field split inside phyreBody[0xC0]/material[0x04] (BN-2) is answered; which objects become rigid bodies (UQ-304) is SUPERSEDED as a duplicate of BN-4, answered 2026-09-27 (none in shipped content); the 102 generically tagged functions (UQ-305) are SUPERSEDED as a duplicate of BN-6. Re-statused 2026-09-29 (OPUS, owner read under FABLE's status-currency ruling, _index/candidates/dd-owner-read-0929)
owner_layer: CodeDomain:Phyre.PPhysics.Bullet + ThirdParty.Physics.Bullet
evidence_tier: 6
verified_against:
  gzf_sha256: 2ed8affb732f0def0a7852e0788298ae36b81206099dd1712f59825fc1c00bb9
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: additive-annotation across GN158 -> GN161 - every step of the certified lineage is additive on the canonical record (internal 38161, owner 9409 and finalNo 585 constant at all five generations; each step's codeDomain and explicit rise equals its unresolved fall). Of the functions classified since GN158 this document cites none of batch R109's 109; the 21 classified before GN160 are named in AUDIT-LOG's batch records and not in a tracked machine-readable list, so identity is not claimed. Voided by any delta that removes or rewrites a comment, tag, name, prototype or body range.; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md, lineage extension (twenty ledger figures across five generations)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  snapshot_sha256: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-02
audit:
  passes: 1
  last_pass: 2026-09-03
  last_pass_state: GN158 checkpoint 2ed8affb… / snapshot 46f02e26…, project GFZ_HD2
  falsification_passes: 1
  last_falsification: 2026-09-03
  last_falsification_by: repos-d2
  falsification_result: 0 overturned, 9 survived, 2 claims strengthened — see section 10
  crossref_clean: true
  reopened_count: 0
  promoted: 2026-10-01 DOCUMENTED -> AUDITED by SWE2-AUDIT-SPEC (FRONTIER eligibility census sweep): falsification record GN158 checkpoint 2ed8affb… / snapshot 46f02e26…, project GFZ_HD2; audit_crossrefs at HEAD reports 0 unresolved findings; cross-subsystem neighbours covered inline (no dedicated section; fresh audit reports 0 unaccounted); killer observations recorded in the pass; promoter is not the last substantive author (last substantive commit: OPUS)
---

# Phyre-to-Bullet rigid body materialization

> The single function where FFXII's own physics description stops and a real Bullet
> `btRigidBody` begins — and the exact defaults the game hands Bullet when it builds one.

## 1. What the player sees

Almost nothing in FFXII is simulated physics. Characters walk on paths, enemies are moved by
their scripts, and the world is fixed. But some things *are* handed to a real physics engine —
and you can tell which, because they behave differently: they fall, they tumble, they come to
rest at an angle, and they settle.

The important thing a player would notice if this broke is not falling objects. It is that
**physics objects go to sleep**. A physics engine that simulated everything all the time would
burn the frame budget on a chest lid that stopped moving ten minutes ago. So when a body is not
dynamic, the game creates it and *immediately* marks it as sleeping — it exists, it collides,
but it costs nothing until something wakes it.

This is also the seam where the game's own idea of a physical object — a shape, a weight, a
centre of balance — is translated into the third-party physics library's idea of one. Everything
before this point is Square Enix's description. Everything after it is Bullet, a widely used
open-source physics library, running exactly as it does in any other game that ships it.

For a modder that boundary is the useful part: **once you are past this function, the public
Bullet documentation applies.**

## 2. Native mechanism

`0069FB10` builds two Bullet objects out of one Phyre rigid-body description, in a fixed order,
and refuses to do it twice.

### Guard

The first thing it does is check whether the body already exists:

```c
if (phyreBody->btRigidBody /* +0x118 */ != 0) return 0;   // already materialized
```

So the function is idempotent by construction. Materialization is a one-time transition.

### Step 1 — the compound shape

FFXII does not hand Bullet a single collision shape. It always builds a **`btCompoundShape`** — a
container that holds child shapes, each with its own transform. Even a body with one child gets a
compound. That uniformity is why the code below has no special case for simple bodies.

If the compound does not exist yet it is allocated at **128 bytes** and constructed by `00832390`.
That constructor writes `btCompoundShape::vftable` — a genuine qualified symbol — and initialises
the object to upstream Bullet's documented starting state: broadphase shape type **31**
(`COMPOUND_SHAPE_PROXYTYPE`), a deliberately inverted local AABB (min `+1e18`, max `-1e18`, so the
first child expands it correctly), and local scaling `(1, 1, 1)`.

Its one parameter is upstream Bullet's `enableDynamicAabbTree`. FFXII passes **0** — no dynamic
AABB tree. When that flag is set Bullet allocates a 64-byte `btDbvt` to accelerate child lookup;
FFXII declines it, which is the right call for compounds with few children and tells you these
bodies are not expected to hold many parts.

### Step 2 — realise each child and accumulate mass

The children live in a count/array pair using the same small-buffer idiom as the rest of Phyre: a
count with **bit 31 used as an ownership flag**, and an array that is stored *inline* when the count
is below 2 and *out of line* otherwise. Every read of it re-derives the base, which is why the
decompiled body repeats the same three-way test many times.

For each child the engine calls the child's own virtual `+0x08` to build itself, bails out on the
first failure, and accumulates the child's mass:

```c
totalChildMass += child->mass;   /* child +0x0C */
```

### Step 3 — place each child in the compound

Each child's local scale is multiplied by the body's scale and pushed into the child's Bullet shape
through its virtual `+0x28` (`setLocalScaling` in upstream Bullet):

```c
scaled.x = child[0x50] * body[0x88];
scaled.y = child[0x54] * body[0x8C];
scaled.z = child[0x58] * body[0x90];
```

Then the child's transform is written into the compound by `00833390`
(`btCompoundShape::updateChildTransform`), with the body's **centre of mass negated** and added to
the translation:

```c
origin += ( -body[0x30], -body[0x2C], -body[0x28] );   /* <- corrected 2026-10-02, OPUS - reversed: x takes -body[0x28], y -body[0x2C], z -body[0x30] (negated at 0069FB10+0x1AD..+0x1E1, added at 0069FB10+0x307 / +0x2FA / +0x2E9 into the origin stored at +0x30C / +0x312 / +0x318) */
```

That negation is the whole reason a physics body rotates about its balance point rather than its
model origin. Bullet always spins a body about the origin of its collision shape, so the engine
shifts the *shape* by minus the centre of mass instead.

`btCompoundShape` children are stored at a stride of **0x60 (96 bytes)**, and
`updateChildTransform` finishes by calling the compound's virtual `+0x78`
(`recalculateLocalAabb`) — which is why moving one child correctly grows the whole compound's
bounds.

### Step 4 — mass and inertia

```c
mass = body[0xE4];
if (body[0xE8] == 1) {                       /* dynamic */
    if (authoredInertia == (0,0,0))
        compound->calculateLocalInertia(mass, &inertia);   /* virtual +0x38 */
    else
        inertia = authoredInertia;           /* body +0x58/+0x5C/+0x60 */
    if (mass == 0.0f) mass = totalChildMass; /* fall back to the sum of the children */
} else {
    mass = 0.0f;                             /* non-dynamic */
}
```

Two behaviours worth knowing. **An authored inertia wins over the computed one** — set it and
Bullet's shape-derived inertia is never consulted. And **a dynamic body with mass 0 does not become
static**; it silently inherits the sum of its children's masses. A body you intended to be massless
will fall.

### Step 5 — construct the `btRigidBody`

A `btRigidBodyConstructionInfo` is built on the stack, the body is allocated at **0x2C0 (704)
bytes, 16-byte aligned**, and `00852DB0` constructs it — writing `btRigidBody::vftable` and
delegating to `008542B0` (`btRigidBody::setupRigidBody`), which is exactly upstream Bullet's
structure.

### Step 6 — sleep and back-reference

```c
if (body[0xE8] != 1)                    /* not dynamic */
    setActivationState(rigidBody, 2);   /* 2 = ISLAND_SLEEPING */
rigidBody[0x108] = phyreBody;           /* back-pointer, Bullet -> Phyre */
```

The back-pointer at `+0x108` is how a collision result gets from Bullet back to the game object it
belongs to. It is the return path for the entire seam.

## 3. Key addresses

| Address | Working name | Body | Role |
|---|---|---:|---|
| `0069FB10` | `PPhysicsRigidBody_MaterializeBulletBody` | 1,899 B | **the seam** — builds the compound shape and the `btRigidBody` from a Phyre body description |
| `006A4A60` | `PPhysicsRigidBody_ResetBulletTransformScaleAndActivation` | 965 B | called at the end of materialization; resets transform, scale and activation |
| `00832390` | `btCompoundShape::btCompoundShape` | 201 B | writes `btCompoundShape::vftable`; shape type 31; inverted AABB; optional `btDbvt` |
| `00832590` | `btCompoundShape::addChildShape` | 635 B | GFZ-named |
| `00833390` | `btCompoundShape::updateChildTransform` | 173 B | writes a 64-byte transform at child stride `0x60`; updates the `btDbvt` if present |
| `00852DB0` | `btRigidBody::btRigidBody` | 95 B | writes `btRigidBody::vftable`; delegates to `setupRigidBody` |
| `008542B0` | `btRigidBody::setupRigidBody` | 678 B | GFZ-named |
| `0083A3A0` | `btCollisionObject::setActivationState` | 21 B | the `(state - 4) > 1u` guard — refuses to overwrite states 4 and 5 |
| `0085E680` | `btAlignedAllocFunc` dispatcher | 13 B | increments the live-allocation counter, tail-jumps through the allocator pointer |
| `00840F90` | `btDbvt::btDbvt` | 36 B | 64-byte dynamic AABB tree, allocated only when `enableDynamicAabbTree` is set — FFXII never sets it at the call site read here |

Addresses are Ghidra image base `0x00120000`. **Every row above is a function**, and body sizes are
exact-current body extents from a `DumpFullCoverageGraph.java` run at the GN checkpoint.

### Data addresses cited by this document

**Data, not functions** — no body extent. Listed separately so a cross-reference audit does not read
them as functions that have gone missing.

| Address | Name | Kind | Contents |
|---|---|---|---|
| `02EAF6C4` | `gNumAlignedAllocs` | `u32` counter | Bullet's live aligned-allocation count, incremented by `0085E680` |
| `01F44CF0` | `btAlignedAllocFunc` | function pointer | the settable allocator hook the dispatcher tail-jumps through |

## 4. Data structures and formulas

### Phyre rigid-body description — fields read by the seam

```
PPhysicsRigidBody (param_1)
  +0x28  f32   centreOfMass.z    negated into every child transform   <- corrected 2026-10-02, OPUS - .x, not .z: 0069FB10+0x307 adds -[+0x28] to the child origin's x, and 006A4A60 multiplies it by the basis column 0
  +0x2C  f32   centreOfMass.y
  +0x30  f32   centreOfMass.x   <- corrected 2026-10-02, OPUS - .z, not .x: 0069FB10+0x2E9 adds -[+0x30] to the child origin's z
  +0x58  f32   localInertia.x    authored; (0,0,0) means "compute it"
  +0x5C  f32   localInertia.y
  +0x60  f32   localInertia.z
  +0x88  f32   scale.x
  +0x8C  f32   scale.y
  +0x90  f32   scale.z
  +0x98  ptr   geometry          when null, the children are searched for one
  +0xB0  u32   childCount        bit 31 is an ownership flag, masked with 0x7FFFFFFF
  +0xB8  ptr   children          INLINE when (count & 0x7FFFFFFF) < 2, else a pointer
  +0xC0  8 B   dampingPair       copied verbatim into the construction info
  +0xE4  f32   mass              0 with dynamic set falls back to the child mass sum
  +0xE8  u8    isDynamic         1 = dynamic; anything else = created sleeping, mass 0
  +0x118 ptr   btRigidBody       OUTPUT; non-null short-circuits the whole function
  +0x120 ptr   btCompoundShape   OUTPUT
```

```
child
  +0x0C  f32   mass
  +0x18  ptr   material          8 bytes read from +0x04 of it into the construction info
  +0x50  f32   localScale.x
  +0x54  f32   localScale.y
  +0x58  f32   localScale.z
```

### The child array base — exact expression

Re-derived on every access, hence its repetition in the body:

```c
n = phyreBody[0xB0] & 0x7FFFFFFF;
base = (n == 0) ? 0
     : (n <  2) ? (phyreBody + 0xB8)          /* the slot IS the array */
                : *(void **)(phyreBody + 0xB8);
child_i = *(void **)(base + i * 8);
```

### Child world placement

```c
scaled     = (child[0x50] * body[0x88], child[0x54] * body[0x8C], child[0x58] * body[0x90]);
childShape->setLocalScaling(&scaled);                      /* virtual +0x28 */
origin.x  += -body[0x30];   /* <- corrected 2026-10-02, OPUS - x takes -body[0x28] (0069FB10+0x307) */
origin.y  += -body[0x2C];
origin.z  += -body[0x28];   /* <- corrected 2026-10-02, OPUS - z takes -body[0x30] (0069FB10+0x2E9) */
btCompoundShape::updateChildTransform(compound, i, &transform);
```

### `btCompoundShape` construction state — exact constants

```c
shape[0x08] = 31;            /* COMPOUND_SHAPE_PROXYTYPE */
localAabbMin = ( 0x5D5E0B6B,  0x5D5E0B6B,  0x5D5E0B6B);   /* +1.0000000150474662e+18 */
localAabbMax = ( 0xDD5E0B6B,  0xDD5E0B6B,  0xDD5E0B6B);   /* -1.0000000150474662e+18 */
localScaling = ( 0x3F800000,  0x3F800000,  0x3F800000);   /*  1.0f, 1.0f, 1.0f       */
if (enableDynamicAabbTree)   /* FFXII passes 0 */
    m_dynamicAabbTree = new (btAlignedAlloc(0x40, 0x10)) btDbvt();
```

`0x5D5E0B6B` is `BT_LARGE_FLOAT` (`1e18`) in single precision — upstream Bullet's own sentinel.

### `btRigidBodyConstructionInfo` as FFXII fills it

Laid out from the struct base, sizes as written:

```
+0x00  f32  m_mass                      = authored mass, or the child mass sum
+0x08  ptr  m_motionState               = 0        <- FFXII uses no motion state
+0x10  64B  m_startWorldTransform       = identity (basis 1,1,1 + origin 0,0,0)
+0x50  ptr  m_collisionShape            = the btCompoundShape
+0x60  16B  m_localInertia              = authored, or calculateLocalInertia()
+0x70   8B  m_linearDamping/m_angularDamping   <- from phyreBody +0xC0
+0x78   8B  m_friction/m_restitution            <- from child->material +0x04
+0x80  f32  m_linearSleepingThreshold    = 0x3F4CCCCD = 0.8f
+0x84  f32  m_angularSleepingThreshold   = 0x3F800000 = 1.0f
+0x88  u8   m_additionalDamping          = 0 (false)
+0x8C  f32  m_additionalDampingFactor    = 0x3BA3D70A = 0.005f
+0x90  f32  m_additionalLinearDampingThresholdSqr  = 0x3C23D70A = 0.01f
+0x94  f32  m_additionalAngularDampingThresholdSqr = 0x3C23D70A = 0.01f
+0x98  f32  m_additionalAngularDampingFactor       = 0x3C23D70A = 0.01f
```

**Those seven trailing values are upstream Bullet's `btRigidBodyConstructionInfo` defaults, in
upstream order, unmodified.** FFXII overrides none of them. That is the tier-6 match that anchors
this whole reading: the probability of seven unrelated constants landing on `0.8, 1.0, false,
0.005, 0.01, 0.01, 0.01` in that sequence by coincidence is nil.

The two fields FFXII *does* supply — damping from the body, friction and restitution from the
child's material — are the only physical tuning the game applies. Everything else is Bullet stock.

### Activation state guard — exact expression

```c
void setActivationState(btCollisionObject *o, int newState) {
    if ((unsigned)(o->m_activationState /* +0xF4 */ - 4) > 1)   /* i.e. != 4 && != 5 */
        o->m_activationState = newState;
}
```

`4` is `DISABLE_DEACTIVATION` and `5` is `DISABLE_SIMULATION`; the unsigned subtract-and-compare is
the standard compilation of upstream Bullet's two-way inequality. FFXII passes `2`
(`ISLAND_SLEEPING`) for every non-dynamic body.

### Return codes

```
0     success (including "already materialized")
9     no collision geometry — neither phyreBody[0x98] nor any child had one
0xE   allocation failed (btRigidBody)
other propagated verbatim from a child's build failure
```

## 5. Call chain

```
Phyre physics scene brings a rigid body online
  -> PPhysicsRigidBody_MaterializeBulletBody          0069FB10   [AUTHORITY 22 -> 23]
     -> btAlignedAllocFunc dispatcher                 0085E680
     -> btCompoundShape::btCompoundShape              00832390
     -> child->build()                                virtual +0x08
     -> childShape->setLocalScaling()                 virtual +0x28
     -> btCompoundShape::updateChildTransform         00833390
        -> compound->recalculateLocalAabb()           virtual +0x78
     -> compound->calculateLocalInertia()             virtual +0x38   (dynamic, no authored inertia)
     -> btRigidBody::btRigidBody                      00852DB0
        -> btRigidBody::setupRigidBody                008542B0
     -> btCollisionObject::setActivationState         0083A3A0        (non-dynamic only)
     -> PPhysicsRigidBody_ResetBulletTransformScaleAndActivation  006A4A60
  -> from here on the object is simulated by stock Bullet
```

**Upstream (who causes this):** Phyre's physics scene. The **owner transition** is `0069FB10`
itself — above it the object is a Phyre description with no Bullet representation; below it, it is a
`btRigidBody` and Bullet owns its motion.

**Downstream (what this causes):** the whole Bullet simulation — `btDbvtBroadphase::collide`,
`btSequentialImpulseConstraintSolver`, `btVoronoiSimplexSolver`. Results return to the game through
the `+0x108` back-pointer.

**Do not confuse with:**

- **`0085E680` is not a general allocator.** It is Bullet's own `btAlignedAllocFunc` indirection:
  it bumps `gNumAlignedAllocs` and tail-jumps through a replaceable pointer. Every Bullet allocation
  in the image goes through it, so it is a natural instrumentation point — and a misleading one to
  attribute to any single caller.
- **A "compound shape" here is not an optimisation.** It is unconditional; even single-child bodies
  get one.
- **This is materialization, not per-frame update.** Nothing in this document runs per frame.

## 6. Modding notes

- **Best intervention point:** `phyreBody[0xE8]` (the dynamic flag) and `phyreBody[0xE4]` (mass),
  set *before* materialization. After the `btRigidBody` exists, changing them does nothing — the
  guard at `+0x118` means the function will not run again.
- **Regenerates itself:** the compound's local AABB (recomputed by `recalculateLocalAabb`) and the
  local inertia when it is left at `(0,0,0)`. Do not write either directly.
- **Breaks if:**
  - You set the dynamic flag with mass `0` expecting a static body. You get a body whose mass is the
    sum of its children — it will fall.
  - You expect a non-dynamic body to be awake. It is created `ISLAND_SLEEPING` and something must
    wake it.
  - You expect activation-state writes to stick on a body already at state 4 or 5. They are ignored
    by design.
  - There is no collision geometry anywhere — the function returns `9` and no body is created at all.
- **Multiplayer / XIIOnline:** a `btRigidBody`'s simulated transform is **locally derived**. Two
  clients running the same Bullet build from the same inputs will still diverge — the solver is
  iterative and order-sensitive. Physics results must not be trusted as shared world state; if a
  physics outcome matters to gameplay, one side has to decide it and send the outcome. The
  authoritative thing here is the *materialization inputs* (shape, mass, dynamic flag), which are
  authored and identical everywhere.
- **Mod compatibility:** damping (`+0xC0`) and the material's friction/restitution (`+0x04`) are the
  two authored tuning knobs this seam reads. They are per-object and safe for a mod to change
  without touching engine code.

## 7. What is not known

- [x] **UQ-302.** The exact Bullet version. The construction-info layout has **no `m_rollingFriction` field**,
      which is consistent with a pre-2.82 Bullet, but no version string has been found in the image
      to pin it the way zlib, libvpx and Lua are pinned.
      ***NARROWED 2026-09-17 (FABLE): the serializer's type-name set bounds the version without pinning it.** The image has no constant-return `btGetVersion` (no function in the list is a bare `mov eax, imm; ret` with a value in 270..300), no `BulletDNA`/`SDNA` blob and no version string. It does carry the twenty struct names the linked `serialize` methods return, at ~~file offsets `0x1BAC800`..`0x1BAE300`~~ `01CCD380` (`btCollisionShapeData`) to `01CCF378` (`btRigidBodyFloatData`), file offsets `0x1BAC180`..`0x1BAE178` *(corrected 2026-10-02, OPUS: each of the twenty names located in the image)*: `btRigidBodyFloatData`, `btCollisionObjectFloatData`, `btCollisionShapeData`, `btCompoundShapeData`/`ChildData`, `btConvexHullShapeData`, `btCylinderShapeData`, `btCapsuleShapeData`, `btStaticPlaneShapeData`, `btTriangleMeshShapeData`, `btStridingMeshInterfaceData`, `btMeshPartData`, `btIntIndexData`, `btShortIntIndexTripletData`, `btQuantizedBvhFloatData`, `btQuantizedBvhNodeData`, `btOptimizedBvhNodeData`, `btBvhSubtreeInfoData`, `btVector3FloatData`, `btVector3DoubleData`. No `m_rollingFriction` name and no multibody struct appear, which keeps the build below 2.82 as the construction-info layout already said; the set is otherwise the collision and rigid-body serialization of the 2.7x..2.81 line, ~~and nothing in it separates those releases. The exact number is not in the image.~~* *(Corrected 2026-09-26 (FABLE, Claude Opus 5.5): one name does separate them; see the answer below.)*
      **ANSWERED 2026-09-26 (FABLE, Claude Opus 5.5) (as `BN-1`): the linked Bullet is the 2.77 line.** Control: [`bn1_bullet_version.py`](../../_index/candidates/bn1-bullet-version/bn1_bullet_version.py) (3 checks,
      FAILS 0). Found by a delegated read-only pass by comparing the image with upstream Bullet source at dated commits.
      The image side is re-checked here and the upstream side re-read from the fetched copies.
      - **Why not 2.76 or earlier.** The image's `btStridingMeshInterface::serialize` names its short-index chunk
        `btShortIntIndexTripletData`. Upstream renamed it to that on 2010-02-27, after the 2.76 release, which still
        says `btShortIntIndexData`. The old name occurs nowhere in the image.
      - **Why not 2.78 or later.** Its index switch has exactly two arms, integer and short. Upstream added a third,
        `PHY_UCHAR` with `btCharIndexTripletData`, on 2011-01-07, and every later release keeps it. That name occurs
        nowhere in the image.
      - **An independent upper bound.** The RTTI still nests the solver's island callback inside `solveConstraints`;
        upstream moved it to file scope on 2011-12-12.
      - **So:** the only release between 2010-02-27 and 2011-01-07 is 2.77. A trunk snapshot from that window also
        fits, and the image cannot separate the two.
      - Evidence class: static, plus comparison with upstream source (the Bullet repository's history).
- [x] **BN-2.** The precise field split inside `phyreBody[0xC0]` and `child->material[0x04]`. Both are copied
      as 8-byte pairs; the mapping to `m_linearDamping`/`m_angularDamping` and
      `m_friction`/`m_restitution` is derived from the surrounding layout fit, not read directly.
      ***ANSWERED 2026-09-18 (FABLE) — read directly from the three bodies, no layout fit needed.** The construction info is built at `rbp − 0x10` in `PPhysicsRigidBody_MaterializeBulletBody`, and the four stores land in upstream order: `phyreBody+0xC0` → `[rbp+0x60]` = `cInfo+0x70` and `phyreBody+0xC4` → `cInfo+0x74` (`006A0187`–`006A019C`); `material+0x04` → `[rbp+0x68]` = `cInfo+0x78` and `material+0x08` → `cInfo+0x7C` (`006A0173`–`006A0182`). `btRigidBody::setupRigidBody` then copies `cInfo+0x78` / `+0x7C` verbatim into the collision object's `+0xFC` / `+0x100` (`0085445B`–`00854467`) and hands `cInfo+0x70` / `+0x74` to `00854080` as `xmm1` / `xmm2` (`0085449B`–`008544A8`), which is `setDamping`: each clamped to `[0, 1]` and stored at body `+0x1E0` / `+0x1E4` (`008540C9`, `008540E8`). The consumer names them: `008531F0`, the only Bullet-band caller of `powf`, computes `pow(1 − [+0x1E0], dt)` and multiplies the linear velocity `+0x150`..`+0x158` by it, then `pow(1 − [+0x1E4], dt)` over the angular velocity `+0x160`..`+0x168` (`00853210`–`00853279`) — upstream's `applyDamping`. So **`phyreBody[0xC0]` is `{m_linearDamping, m_angularDamping}`** and **`material[0x04]` is `{m_friction, m_restitution}`**, and the earlier mapping stands, now as a reading. Static: the three bodies.*
- [x] ~~**UQ-303.** What `006A4A60` (`ResetBulletTransformScaleAndActivation`, 965 B) does in detail — it is named
      from its GFZ tag and its position, not from a full read.~~ **ANSWERED 2026-09-14 (OPUS)** — all 965 bytes
      read from the shipping image; see §*`006A4A60` read end to end* below. The tag is accurate and
      incomplete: it does not say the function removes the body from the world and re-adds it with a
      group/mask pair computed from `byte [self+0xE0]`.
- [x] **UQ-304** *(superseded id — the live row is **`BN-4`**)*. Which FFXII objects actually become Bullet rigid bodies in a shipped map, and how many exist *(closed — the register row is WITHDRAWN.)*
      at once.
      **NARROWED FURTHER 2026-09-22 (FABLE): the Phyre-side population is EMPTY.** Over all 35,984
      shipped clusters, `Physics` — the widest needle — occurs in **0**, against controls of 2,184
      each for `PEffect` and `PContextSwitch`. See the section above.
      **Narrowed 2026-09-18 (FABLE): the static route into the seam is one chain, and it starts at a body nothing calls.* `edges.tsv` gives `PPhysicsRigidBody_MaterializeBulletBody` one caller, `0069F070`, whose one caller is `0069EF20`, whose one caller is `00698C80`, whose one caller is `006883A0` — and `006883A0` has **no listed caller**: it is reached by pointer (a component virtual or a callback), so which Phyre objects reach the seam is decided by whatever installs `006883A0`~~, which no page has read~~ *(answered: see `BN-4` below - no shipped Phyre object carries a physics component, 2026-09-22; 2026-10-02, OPUS)*. How many bodies exist at once is a question of the shipped maps' physics components, not of the code.*
## `BN-4` — the shipped Phyre corpus contains no physics at all (FABLE, 2026-09-22)

The 2026-09-18 narrowing ended by saying *“how many bodies exist at once is a question of the
shipped maps' physics components, not of the code”*. **Those components were then measured, and
there are none.**

| needle, over all **35,984** shipped `.phyre` clusters | clusters |
|---|--:|
| `PPhysicsRigidBody` | **0** |
| `PhysicsRigidBody` — widened | **0** |
| **`Physics`** — the widest possible | **0** |
| `PEffect` *(control)* | 2,184 |
| `PContextSwitch` *(control)* | 2,184 |

**The controls are what make the zero worth writing down.** Two needles known to be present return
2,184 clusters each from the same pass, so the sweep reads the corpus correctly and the zero is a
real zero rather than a broken reader. *And the needle cannot be too narrow:* the registered class
is `PPhysicsRigidBody**Base**`, which the substring `PPhysicsRigidBody` matches — and `Physics`
alone still finds nothing.

> **So the asset side is empty while the code side is fully present.** The image's recovered
> reflection schema registers **sixteen** Phyre physics classes — `PPhysicsRigidBodyBase`,
> `PPhysicsWorldBase`, `PPhysicsShapeBase`, `PPhysicsBoxBase`, `PPhysicsCapsuleBase`,
> `PPhysicsMeshBase`, `PPhysicsModel`, `PPhysicsMaterial`, `PPhysicsCharacterControllerBase` and
> seven more — **and not one of them is declared or instantiated by any shipped cluster.**

**That closes the route this page documents.** §'s chain reaches the seam only through `006883A0`,
which has no listed caller and is entered by pointer; the narrowing left open *which* Phyre objects
install it. **The answer is none, because no shipped Phyre object carries a physics component to
install.** Together with `BN-5` — no static path passes `enableDynamicAabbTree = 1` — the Phyre→
Bullet path has code, registration and reflection, and **no authored input**.

> **What this does NOT say, and the distinction is the whole caveat.** It is a statement about the
> **Phyre cluster corpus**. FFXII ships map and collision data in its own formats outside
> `.phyre`, and the seam is reached by a function pointer, so a native installer could still drive
> it from non-Phyre data. **What is excluded is the Phyre component route — the one this page
> traced — not physics in the game.**

- [x] Whether any FFXII code path ever passes `enableDynamicAabbTree = 1`; only the `0` call site
      has been read. **BN-5.**
      *Answered on the page 2026-09-14 (FABLE), box left for the ledger mirror (BN-5):* **no static path does.**
      - **One caller.** The constructor `00832390` has exactly one call site in the raw call index, which includes unlisted
        code and tail jumps: `0069FBBF`, preceded by `xor edx, edx` (`0069FBBA`).
      - **No indirect route.** No 8-byte pointer to the constructor exists anywhere in the file.
      - **No inlined construction.** `btCompoundShape`'s vtable `01CCD7A8` is loaded by exactly two instructions: the
        constructor (`008323B1`) and the destructor `008324B0` (`008324C7`).

      So every `btCompoundShape` the game builds has no dynamic AABB tree, and `btDbvt::btDbvt` (`00840F90`) is never reached
      from this class.
- [x] **UQ-305.** The 102 Bullet functions still carrying only the generic `ThirdParty.Physics.Bullet` tag. *(closed — the register row is WITHDRAWN.)*
      **Narrowed 2026-09-18 (FABLE): twelve of the 102 named from the classes they instantiate.* Every one of the 102 was decoded and each `lea` of an `.rdata` address whose `[−8]` is a valid RTTI locator was resolved to its class; twelve install vtables, and the nested-class names spell the enclosing method. **`00833440`** (716 B) installs `btConvexHullShape` — its constructor; **`008382D0`** (815 B) installs `btAxisSweep3Internal<unsigned short>` and falls back to a `btNullPairCache` — the `btAxisSweep3` constructor; **`00838650`** (208 B) walks the same vtable down to `btBroadphaseInterface` — its destructor; **`0083AA80`** (211 B) installs `btCollisionWorld` — its constructor; **`0083B780`** (9,779 B) builds a `DebugDrawcallback` — `btCollisionWorld::debugDrawObject`; **`0083E7E0`** (3,822 B) builds `BridgeTriangleConvexcastCallback` and `LocalInfoAdder` of `btCollisionWorld::objectQuerySingle` with a `btGjkEpaPenetrationDepthSolver` — `objectQuerySingle`; **`0083FD10`** (2,868 B) builds `BridgeTriangleRaycastCallback` and `LocalInfoAdder2` of `rayTestSingle` with a `btSphereShape` — `btCollisionWorld::rayTestSingle`; **`00846710`** (1,289 B) builds `NodeTriangleCallback` and `QuantizedNodeTriangleCallback` of `btOptimizedBvh::build` — `build`; **`0084AB40`** (596 B) builds a `btTriangleShape`, a `CastResult` and both penetration-depth solvers — `btTriangleConvexcastCallback::processTriangle`; **`0084BED0`** (2,005 B) builds a `btSphereShape`, a `btPointCollector` and a `btDiscreteCollisionDetectorInterface::Result` — `btConvexConvexAlgorithm::calculateTimeOfImpact`; **`00857970`** (659 B) builds `btClosestNotMeConvexResultCallback` over a `btSphereShape` — the CCD sweep of `btDiscreteDynamicsWorld::integrateTransforms`; **`008585E0`** (697 B) builds `InplaceSolverIslandCallback` of `solveConstraints` and hands it to `btSimulationIslandManager` — `btDiscreteDynamicsWorld::solveConstraints`. The other ninety install no vtable; their callee sets are `sqrtf` / `cosf` / `sinf` / the cookie check or nothing, so they are the leaf math of the collision algorithms and need a structural match against a Bullet release to name. Static: the vtable sweep over all 102 bodies.*

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| `00852DB0` constructs a `btRigidBody` | the body writes the qualified symbol `btRigidBody::vftable` | 3 |
| `00832390` constructs a `btCompoundShape` | the body writes the qualified symbol `btCompoundShape::vftable` | 3 |
| The seven construction-info trailing constants are Bullet stock defaults | exact match to upstream Bullet's `btRigidBodyConstructionInfo` initialiser list — `0.8, 1.0, false, 0.005, 0.01, 0.01, 0.01` in upstream order | 6 |
| `0x5D5E0B6B` / `0xDD5E0B6B` are `±BT_LARGE_FLOAT`, and 31 is `COMPOUND_SHAPE_PROXYTYPE` | upstream Bullet constants, matching the compound constructor's complete body | 6 |
| `0083A3A0` is `btCollisionObject::setActivationState` | complete 21-byte body; `(state - 4) > 1u` is the exact compilation of upstream's `!= DISABLE_DEACTIVATION && != DISABLE_SIMULATION` (4 and 5) | 6 |
| `0085E680` is Bullet's `btAlignedAllocFunc` indirection | complete 2-instruction body: increment a counter, tail-jump through a pointer — upstream `btAlignedAllocInternal` with `gNumAlignedAllocs` | 6 |
| Idempotence, return codes, centre-of-mass negation, mass fallback, child-array idiom | complete exact-current body of `0069FB10` | 1 |
| Child stride `0x60`, `recalculateLocalAabb` at virtual `+0x78` | complete exact-current body of `00833390` | 1 |
| Object sizes 128 B (compound), 704 B (rigid body), 64 B (`btDbvt`) | allocation sizes in the complete bodies of `0069FB10` and `00832390` | 1 |
| Body extents and tags | `DumpFullCoverageGraph.java` regenerated at the GN checkpoint, 38,161 rows, 0 duplicate entry addresses | 1 |

**Method note.** Five of the functions named here (`0085E680`, `00832390`, `00833390`, `00852DB0`,
`0083A3A0`) carried **only generic shape classes** in the ledger — `NativeDispatch.NoCall.ComputedTailTransfer`,
`NativeRoutine.AcyclicDirectCall.Bounded.Conditional`, `NativeDispatch.AcyclicComputedJump.Bounded`,
`NativeRoutine.BoundedDirectCall.Pair.Linear`, `NativeLeaf.InlineStateMutation`. They were accounted
for and not understood. Matching them against upstream Bullet source converted all five into real
mechanism identities. This is open question **B-1** work.

**Superseded readings:** an earlier reading in this session guessed `0083A3A0` was
`setCollisionFlags` and the constant `2` was `CF_KINEMATIC_OBJECT`. Reading the complete body
disproved it: the `(state - 4) > 1u` guard is specific to `setActivationState`, and `2` is
`ISLAND_SLEEPING`. The wrong reading was reachable because both functions take `(object, int)` and
both constants are small — a reminder that argument shape is not identity.

## 10. Falsification pass 1 — 2026-09-03, session `repos-d2`

**Previously unattacked** (`passes: 0`). Program state: parent `2ed8affb…`, snapshot `46f02e26…`,
EXE `73461d08…`, project `proj_hd2` / `GFZ_HD2`, `CHECKPOINT VERIFIED` before any reading.

**Nothing in this document was overturned.** Two claims are strengthened and one address is
identified that closes an open item in another document.

### Strengthened — the dynamic AABB tree is built nowhere, not merely "not here"

§3 says the `btDbvt` is *"allocated only when `enableDynamicAabbTree` is set — FFXII never sets it
at the call site read here."* True, and provably narrower than the evidence allows. A caller census
over all 38,161 bodies:

```
00832390  btCompoundShape::btCompoundShape   1 caller image-wide: 0069FB10
0069FBBA  xor edx, edx                       enableDynamicAabbTree = 0
0069FBBF  call 00832390
00840F90  btDbvt::btDbvt                     1 caller image-wide: 00832390
```

**There is exactly one compound-shape construction site in the entire image, it passes zero, and the
`btDbvt` constructor's only caller is the compound-shape constructor.** So the dynamic AABB tree is
**constructed nowhere in FFXII** — every compound shape in the game uses the linear child scan.

The hedge was appropriate to what had been read; the census closes it. **For a modder this is the
difference between "this call site does not enable it" and "enabling it has no precedent anywhere in
the shipped binary."**

### Strengthened — the allocator hook, and an address identified for another document

`01F44CF0` has **exactly one writer and one reader** across all bodies: `FUN_0085E6C0` stores to it
(the `btAlignedAllocSetCustom*` setter), and `0085E680` tail-jumps through it. **"Settable" is
verified rather than assumed.**

**And the slot is one of four.** Reading the run it belongs to:

```
01F44CE0 -> 0085E730  malloc
01F44CE8 -> 0019C590  free
01F44CF0 -> 0085E630  the aligned-alloc hook this document documents
01F44CF8 -> 0085E6F0  the aligned-free hook
```

**That is Bullet's allocator function-pointer table**, and it identifies one of the six runs
[the unowned-code census](../../99-Unresolved-Residual/Unowned-Code-Census/why-the-unowned-code-has-no-owner.md)
lists as uncharacterised remainder — *"`01F44CF0` | 4 | **`malloc`, `free`**, plus an aligned-free
callback"*. It is not loose pointers; it is this library's allocator hooks, and
`02EAF6C4 gNumAlignedAllocs` is the counter beside them.

### Survived — every measurement and every reading checked

| Claim | Result |
|---|---|
| all nine stated body sizes (1,899 / 965 / 201 / 635 / 173 / 95 / 678 / 21 / 13) | **SURVIVED, all nine exact.** `00840F90`, left blank, is **36 B** and is filled in above |
| `0083A3A0` is the `(state - 4) > 1u` guard refusing to overwrite states 4 and 5 | **SURVIVED, exact**: `mov eax,[rcx+0xF4]; sub eax,4; cmp eax,1; jbe skip; mov [rcx+0xF4],edx` |
| `0085E680` increments the counter and tail-jumps through the pointer | **SURVIVED, exact**: `inc [02EAF6C4]` / `jmp qword [01F44CF0]`, 13 bytes, both data addresses confirmed |
| `00832390` writes shape type **31** | **SURVIVED**: `mov dword ptr [rcx+8], 0x1F` |
| `00832390` writes an **inverted AABB** | **SURVIVED**: `+0x40..+0x48 = 0x5D5E0B6B`, `+0x50..+0x58 = 0xDD5E0B6B` — the same magnitude with the sign bit set |
| `00852DB0` writes the vftable and delegates to `setupRigidBody` | **SURVIVED**: vftable `01CCF348` at `[rdi]`, then `call 008542B0` |
| every row in §3 is a function | **SURVIVED** — all ten resolve, and the two data addresses are correctly listed separately |

**Two of these match upstream Bullet exactly**, which is tier 6 corroboration arrived at
independently: `setActivationState` is `if (m_activationState1 != DISABLE_DEACTIVATION &&
m_activationState1 != DISABLE_SIMULATION)` with those constants being 4 and 5, and the compound
shape's constructor initialises `m_localAabbMin` to `+BT_LARGE_FLOAT` and `m_localAabbMax` to
`-BT_LARGE_FLOAT` — which is precisely the `5D5E0B6B` / `DD5E0B6B` pair.

### What was tried and failed to break anything

- **Tried to break the `enableDynamicAabbTree` absence** by looking for a second construction site.
  There is one caller, and a control confirmed the scan detects the calls that do exist —
  `00832390` is among `0069FB10`'s callees, `00840F90` is not.
- **Tried to make the allocator hook unsettable.** One writer, and it is the setter.
- **Tried to find a size error**, the defect that has cost two other documents rows tonight. All nine
  stated sizes are exact.
- **No banned evidence.** No `.pdata`/`.xdata`/unwind/EH. The Bullet identifications rest on
  instruction-level agreement with upstream semantics, not on name resemblance.

## 9. Related

- [`../third-party-middleware-inventory.md`](../third-party-middleware-inventory.md) — the library census this sits inside; ~~**REOPENED 2026-09-02**~~ reopened 2026-09-02 by a count defect this block found, since resolved *(answered: the inventory's front matter, `status: DOCUMENTED`, 2026-10-01; 2026-10-02, OPUS)*
- [`../../22-Middleware-PhyreEngine/Subsystem-Map/phyre-subsystem-map.md`](../../22-Middleware-PhyreEngine/Subsystem-Map/phyre-subsystem-map.md) — `PPhysics` is 153 of its classes; this is the seam out of them
- [`../../06-Movement-And-Navigation/heading-speed-to-position-delta.md`](../../06-Movement-And-Navigation/heading-speed-to-position-delta.md) — how characters move; **not** this. Character motion is scripted, not simulated.
- [`../../00-Engine-Core-Runtime/Object-Model/vtable-method-index.md`](../../00-Engine-Core-Runtime/Object-Model/vtable-method-index.md) — the class/slot index

## `006A4A60` read end to end — `BN-3` / `UQ-303` (OPUS, 2026-09-14)

Both rows asked the same thing: the function is **named from its GFZ tag and its call position, not
from a full read.** All 965 bytes are read here, from the shipping executable at the authority hash
`73461D08…9721F8`, image base `0x120000`. Every address below is decoded from the bytes.

`006A4A60(rcx = self, dl = alsoRescaleShapes)` → always returns **0** (`006A4E0C xor eax, eax`).

### 1. It does nothing without a body, and `+0xE9` is an in-world latch

`rdx = qword [self + 0x118]` is the Bullet body; **null returns immediately** (`006A4A8F`).
`byte [self + 0xE9]` is read into `r15b` and is a boolean *currently in the world*: if set, the
function walks `qword [self+0xC8] → +0x10 → +0x60`, calls **vtable slot `+0xA0`** on it, and
**clears `[self+0xE9]` to 0** (`006A4AE6`). Each hop is null-checked and skipping any of them skips
the call but still clears the latch.

### 2. Two vec3s are pushed into the body at `+0x150` and `+0x160`

Floats at `self+0x68/0x6C/0x70` and `self+0x78/0x7C/0x80` are assembled with a **zeroed fourth lane**
(`mov dword [rbp-0x5d], 0`) and stored as 16-byte `movdqa` writes to `body+0x150` and `body+0x160`.

### 3. The transform is composed, not copied

`movups xmm0, [self+0x48]` — 16 bytes — into `006A57C0`, whose 4×4 output is then ~~multiplied~~
~~componentwise by the scale at `self+0x28/0x2C/0x30`~~ applied to the centre-of-mass vector at `self+0x28/0x2C/0x30` as a matrix-vector product, not a componentwise scale *(corrected 2026-10-02, OPUS: `006A4A60+0x12A`..`+0x1D6` sum, per row, the three basis entries times `[+0x28]`, `[+0x2C]` and `[+0x30]`; the same vector `0069FB10` negates into every child origin)*, and offset by the translation at
`self+0x38/0x3C/0x40` (held in `xmm6`, `xmm8`, `xmm9` across the call), and the result goes to
`00853FE0`. **So the stored transform is built from four separate fields of `self`, not taken from
one.**

### 4. The second argument gates a per-shape rescale

`test dil, dil` (`006A4C60`). When set, it reads a vec3 at `self+0x88/0x8C/0x90` and iterates
`dword [self+0xB0] & 0x7FFFFFFF` elements of the container at `self+0xB8` — **the inline-or-heap
small-vector shape**: `btr eax, 0x1f` then `cmp eax, 1`, taking `qword [self+0xB8]` as a pointer when
the count exceeds 1 and `lea rax, [self+0xB8]` as inline storage when it does not. For each element it
multiplies the element's `+0x50` vec3 componentwise by the `+0x88` vec3 (via two `shufps` broadcasts)
and calls **vtable slot `+0x28`** on the object at `[element + qword[self+0x120] + 0x28] + 0x40`.
Afterwards it calls **slot `+0x78`** on `qword [self+0x120]` once.

### 5. The re-add computes a collision group and mask from one byte

If the object was in the world and the latch is not already 1:

```
006A4DBE  movzx r8d, byte [rbx + 0xE0]        ; a group INDEX
006A4DC6  mov   eax, 1
006A4DD2  shl   ax, cl                        ; group  = 1 << index   (16-bit)
006A4DD8  movzx r9d, word [r9 + r8*2 + 0x78]  ; mask   = a table indexed by the same byte
006A4DE2  call  qword [r10 + 0x130]           ; (world, body, group, mask)
```

**`byte [self+0xE0]` is a collision-group index**, and the mask is a `u16` table at `+0x78` of the
object reached through `self+0xC8 → +0x10`, indexed by that same byte. Then `0083A030(body, 0)` runs
and the latch is set to 1. **`0083A030(body, 0)` also runs on the path where the latch was already
1** — it is the one thing this function does unconditionally once a body exists.

### What this changes about the name

`ResetBulletTransformScaleAndActivation` is **accurate and incomplete**. Reset, transform, scale and
activation are all there; what the tag does not say is that the function performs a **remove-and-
re-add through the broadphase**, and that the re-add recomputes a group/mask pair from
`byte [self+0xE0]`. A caller that wanted only a transform update would be paying for a world
round-trip.

### Not claimed

The Bullet API names behind vtable slots `+0xA0`, `+0x28`, `+0x78` and `+0x130` are **not read** —
they are inferred from slot position and argument shape, and this section names the slots rather than
the methods. `006A57C0`, `00853FE0` and `0083A030` are called and **not entered**.

*(Read by OPUS 2026-09-14. Closes `BN-3` and `UQ-303`, which are the same question asked twice.)*

`006A0A50` (249 B) is ~~the basis-write~~ an angular-velocity write, not a basis write *(corrected 2026-10-02, OPUS: it adds the matrix product into the angular velocity `+0x160`..`+0x168`, which `008531F0` damps by `+0x1E4`; nothing at `+0x120`..`+0x148` is written)* `006A0A40` runs on a live `[rcx+0x118]` record: the record's 3x3 basis at `+0x120`..`+0x148` multiplies the `rdx` input vector, each axis is scaled by `+0x260`/`+0x264`/`+0x268`, offset by `+0x160`/`+0x164`/`+0x168` and stored back into ~~`+0x160`..`+0x164`~~ `+0x160`..`+0x168` *(corrected 2026-10-02, OPUS: three stores, `006A0A50+0xC3`, `+0xDB` and `+0xD3`)* - then `0083A030` is called on the record, the post-write commit this page's rigid-body path performs.

Interior anchor `006A0B3A` (function `006A0A50`).

`006A3AF0` (11 B, no direct call; `btSphereShape` vtable slot 10) multiplies the float at `+0x30` by the float at `+0x20` and returns it - the implicit-dimension x times the local-scaling x, the shape's radius as Bullet's `btSphereShape` computes it.

Interior anchor `006A3AF5` (function `006A3AF0`).

`006A3D40` (127 B, no direct call; `btBoxShape` vtable slot 19) switches on an index 0-5 through the six-entry RVA table at `006A3DC0` and writes a unit axis into the out vector with `w` = 0: +x, -x, +y, -y, +z, -z in that order (`0x3F800000` / `0xBF800000` in one lane, zeros elsewhere); an index above 5 returns without a write - the box's six preferred penetration directions.

Interior anchor `006A3D59` (function `006A3D40`).

`006A4550` (92 B, no direct call; `btBoxShape` vtable slot 15) returns, through the hidden result pointer, the half-extent vector at `+0x30`/`+0x34`/`+0x38` with each component negated (xor with the sign mask `01CEBDA0`) where the direction's matching component is below zero, `w` = 0 - the box's supporting vertex without margin.

Interior anchor `006A4581` (function `006A4550`).

`006A45B0` (26 B, no direct call; slot 1 of `btCollisionWorld::ConvexResultCallback`, shared by `ClosestConvexResultCallback` and `objectQuerySingle`'s local callback) is the filter test: it returns 1 only when the proxy's 16-bit group (`+8`) meets the callback's mask (`+0xE`) and the proxy's mask (`+0xA`) meets the callback's group (`+0xC`), else 0 - `needsCollision` for convex sweeps.

Interior anchor `006A45BA` (function `006A45B0`).

`006A45D0` (26 B, no direct call; slot 1 of `btCollisionWorld::RayResultCallback`, shared by `ClosestRayResultCallback` and `rayTestSingle`'s local callback) is the same filter test on the ray callback's layout: proxy group `+8` against the callback's mask `+0x1A`, proxy mask `+0xA` against its group `+0x18` - `needsCollision` for ray tests.

Interior anchor `006A45DA` (function `006A45D0`).

`0069EEB0` (109 B, no direct call; `btGhostPairCallback` vtable slot 1) takes the two proxies of a new overlapping pair, and for each whose client object's type word `+0x104` equals 4 (the ghost-object type) calls that object's slot at `+0x30` with the other proxy; it returns 0 - the ghost-pair callback's add-overlap hook that keeps a ghost object's overlap list in step with the broadphase.

Interior anchor `0069EECF` (function `0069EEB0`).

## Interior citations for the entry-cited functions (OPUS, 2026-10-03, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-phyre-to-bullet-rigid-body-materializati-ee-1003/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `00832590` | 635 B | increments dword [rcx+0x68]; loads the 64 bytes at `rdx` once on entry, before any call; with child `c` = `r8`, takes `t` = dword [c+8] and `m` = the float `c`'s vtable slot +0x50 returns, calls `c`'s slot +8 with (`rdx`, &stack `lo`, &stack `hi`) and lowers floats [rcx+0x40] to [rcx+0x48] to `lo` / raises [rcx+0x50] to [rcx+0x58] to `hi` per x/y/z (NaN changes nothing); `p` = `008410B0(qword [rcx+0x60], &copy of lo and hi, dword [rcx+0x1C] sign-extended)` when that qword is non-null, else 0; appends a 0x60-byte child to the array with count dword [rcx+0x1C], capacity +0x20, data qword +0x28 and owner byte +0x30 (when the count equals the capacity and twice the count (1 for 0) is larger (signed), `0085E680(0x60 times that, 0x10)` gets the entries' bytes +0 to +0x57, the old data goes to `0085E710` when non-null and owned, then the data qword becomes the new block, the owner byte 1 and the capacity the new size; a store at a null slot is skipped): the 64 bytes loaded on entry, `c` at +0x40, `t` at +0x48, `m` at +0x4C, `p` at +0x50; increments the count | `008325A0`, `008325FE`, `0083269B`, `008326EA`, `008327CB` |
| `00833440` | 716 B | constructor: calls `00831D30(rcx)`, stores vtable `01CCD938`, sets byte +0x98 = 1, zeroes qword +0x90 and dwords +0x84 / +0x88 and sets dword +8 = 4; with `n` = `r8d` (signed): when `n` is positive takes `0085E680(16n, 0x10)` as the point array (qword +0x90, capacity dword +0x88 = `n`, owner byte +0x98 = 1) and fills its entries with a 16-byte stack value the body has not written (a store at a null address is skipped); sets dword +0x84 = `n`, also when negative; for each i below `n` stores (floats at `rdx` + i times `r9d` (signed) and +4, +8, then 0) into entry i (no null test); calls `00832290(rcx)` and returns `rcx` | `00833478`, `00833485`, `008334D5`, `008335E8`, `008336EB` |
| `008382D0` | 815 B | constructor (stack args 5-8: word `s`, word `m`, qword `c`, byte `f`): vtable `01CCE2A0`, words +8 = `r9w`, +0xA = `s`, qword +0x88 = `c`; zeroes qwords +0x90/+0xA0, byte +0x98, dword +0x9C; null `c` makes qword +0x88 what `00847E60` returns for block `0085E680(0x80, 0x10)` (0 if that is null) and byte +0x98 = 1; when `f` is 0, qword +0xA8 = `q` = `0085E680(0x28, 0x10)` (non-null: vtable `01CCE218`, qwords +8/+0x10/+0x18/+0x20/+0xC = 0, byte +0x20 = 1) and qword +0xA0 = `r` = what `00849B30` returns for (block `0085E680(0xE0, 0x10)`, qword +0xA8) (0 if that is null), then byte [r+0xDD] = 1 untested; copies 16 bytes at `rdx`/`r8` to +0x10/+0x20, +0x30 = (`s` as float / (max - min) per x/y/z, 0); with `n` = `m` + 1 (word, wraps to 0): qword +0x48 = `h` = `0085E680(0x60n, 0x10)` (size -1 on overflow; non-null: qwords +0/+0x10 of `n` entries zeroed), words +0x42 = `n`, +0x40 = 0, +0x50 = 1; word +0x40 of entry k = k+1 (k = 1 to `n`-1), then entry `n`-1's = 0; qwords +0x58+8j, +0x70+8j = `0085E680(8n, 0x10)` (j = 0 to 2); qword [h] = 0; no store via `h` tests it; for j = 0 to 2 words h+0x40+2j = 0, h+0x46+2j = 1, and in array +0x58+8j words +0/+2/+6 = 0, +4 = word +0xA; returns `rcx` | `00838303`, `0083835B`, `008383EF`, `008384B6`, `00838578` |
| `00838650` | 208 B | stores vtable `01CCE2A0`; when qword [rcx+0xA0] is non-zero, calls vtable slot +0 with 0 of the object at qword [rcx+0xA8] (no null test) and `0085E710` on that qword, then the same for qword +0xA0 (re-read); calls `0085E710` on qwords +0x80, +0x78, +0x70 and +0x48 in that order; when byte +0x98 is non-zero calls slot +0 with 0 of the object at qword +0x88 and `0085E710` on it; stores vtable `01CCE1A8` | `00838673`, `0083868C`, `008386C7`, `008386F6`, `0083870D` |
| `0083AA80` | 211 B | stores vtable `01CCE610`; for each i below dword [rcx+0xC] (signed), with `o` = pointer i of the array at qword [rcx+0x18] and `p` = qword [o+0xC8]: when `p` is non-null, calls slot +0x48 of the result of slot +0x48 of the object `w` at qword [rcx+0x78] (no other argument set up) with (`p`, qword [rcx+0x28]), then `w`'s slot +0x10 (re-read) with (`p`, qword [rcx+0x28]), and nulls qword [o+0xC8]; then, when the array qword is non-null, calls `0085E710` on it if byte +0x20 is non-zero and nulls it; sets byte +0x20 = 1 and zeroes qword +0x18 and dwords +0xC and +0x10 | `0083AAAC`, `0083AADB`, `0083AAEC`, `0083AAFF`, `0083AB24` |
| `0084AB40` | 596 B | constructs a stack shape `S` with `00831D90(&S)`, then vtable `01CCECC0` and dword S+8 = 1; on stack blocks `X` and `B` sets X+0x80 to X+0xAF = the 48 bytes at `rdx`, float X+0x70 = float [rcx+0xD4], dword B+0x140 = 0x38D1B717 and clears the low 4 bits of word B+0x160; calls `0084BDF0(&X, qword [rcx+8], &S, &B, &O)` with a stack object `O` of vtable `01CCE0C8`; prepares a stack result `R` (vtable `01CCE688`, qword R+0xB8 = 0, float R+0xC0 = 0, float R+0xB0 = 1.0) and calls `0084BED0(&X, rcx+0x10, rcx+0x50, rcx+0x90, rcx+0x90, &R)`; when that returns a non-zero byte, the squared length of the x/y/z at R+0x90 is above `01CEBB60` (0.0001) and float [rcx+0xD0] is above float R+0xB0 (NaN fails both), scales R+0x90 to R+0x98 by 1/`sqrtf` (`00861F14`) of that length and calls its own vtable slot +0x10 with (&R+0x90, &R+0xA0, float R+0xB0, `r8d`, `r9d`); then stores `01CCE688` in `R` again, calls `0084B280(&X)`, stores `01CCE0B0` in `O` and `00D7A770` in `S` and calls `00830C40(&S)` | `0084AB94`, `0084AC15`, `0084AC71`, `0084ACD3`, `0084AD2A` |

## Interior citations for the entry-cited functions (OPUS, 2026-10-03, cloud-drafted, opus-phyre-to-bullet-rigid-body-materializati-ee-1003-2)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-phyre-to-bullet-rigid-body-materializati-ee-1003-2/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `0083B780` | 9779 B | Scope: all calls (direct, tail, exit jcc, indirect by operand, imports by name) and all non-stack stores with widths; branch conditions, arithmetic and order not stated; scoped row: set-exact. Calls: `00808C40`, `0083E050`, `00841850`, `00841860`, `[r10+0x10]`, `[r10+0x80]`, `[r8+0x68]`, `[rax+0x10]`, `[rax+0x18]`, `[rax+0x28]`, `[rax+0x50]`, `[rax+0x70]`, `[rax+0x8]`, `[rax+0xA0]`, `[rax+0xA8]`, `[rax+0xB0]`, `[rdx+0x20]`, `import:sqrtf`; Stores: none | `0083B80A`, `0083DD5B` |
| `0083E7E0` | 3822 B | Scope: all calls (direct, tail, exit jcc, indirect by operand, imports by name) and all non-stack stores with widths; branch conditions, arithmetic and order not stated; scoped row: set-exact. Calls: `00808C40`, `00836D40`, `0083E610`, `0083E7E0`, `00841860`, `0084A9E0`, `0084B280`, `0084BDF0`, `[rax+0x10]`, `[rax+0x50]`, `[rax+0x70]`, `[rax+0x8]`, `import:sqrtf`; Stores: `q[r9+0xD0]` | `0083E8FC`, `0083F640`, `0083F67E` |
| `0083FD10` | 2868 B | Scope: all calls (direct, tail, exit jcc, indirect by operand, imports by name) and all non-stack stores with widths; branch conditions, arithmetic and order not stated; scoped row: set-exact. Calls: `00808C40`, `00830C40`, `00831990`, `00836DA0`, `0083E610`, `0083FD10`, `00841860`, `0084AA90`, `0084B280`, `0084B2C0`, `0084B320`, `[rax+0x10]`, `[rax+0x70]`, `import:sqrtf`; Stores: `q[rax+0xD0]`, `q[rcx+0xD0]` | `0083FDA4`, `00840731`, `008407F4`, `0084079A` |
| `00846710` | 1289 B | Scope: all calls (direct, tail, exit jcc, indirect by operand, imports by name) and all non-stack stores with widths; branch conditions, arithmetic and order not stated; scoped row: set-exact. Calls: `00841850`, `008424A0`, `00844CA0`, `0085E680`, `0085E710`, `[rax+0x8]`; Stores: `b[rbx+0x68..0xC8/32]`, `b[rbx+0xF0]`, `b[rcx+0x48]`, `d[rbx+0x44,0x74,0x78,0xB4,0xB8,0xDC,0xE0,0xF8]`, `d[rdx+r8*1+0x10]`, `d[rdx+r8*1+0xC]`, `q[rbx+0x54,0x60,0x80,0x94,0xA0,0xC0,0xE8]`, `w[rdx+r8*1+0x2]`, `w[rdx+r8*1+0x4]`, `w[rdx+r8*1+0x6]`, `w[rdx+r8*1+0x8]`, `w[rdx+r8*1+0xA]`, `w[rdx+r8*1]`, `x[rcx+0x10..0x30/16]`, `x[rcx]`, `x[rdx]` | `0084675D`, `00846741`, `00846A1E`, `00846BF0` |
