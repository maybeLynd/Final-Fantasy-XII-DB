# V121 corrected post-CS audit GD recovery replay persistence seal — 2026-08-31

**Verdict: PERSISTENCE_CERTIFIED_RECOVERY_REPLAY**

This artifact deterministically reconstructs the previously proven but ephemeral GD working mutation on top of the persistence-certified GC recovery parent. The original GD working project had already passed a full 38,161-function mutation diff before its runtime disappeared, but it had not yet been packed. This replay does **not** claim byte-identity with that lost working project's comment text; the three semantic decisions are replayed with explicit recovery provenance and independently re-audited.

## Durable continuation artifact

`FFXII_TZA_XIIOnline_Gfz9_V121_FULL_EXECUTABLE_COVERAGE_CORRECTED_POST_CS_AUDIT_GD_RECOVERY_REPLAY_99P53_2026-08-31.gzf`

- Size: **82,101,207 bytes**
- SHA-256: `b3d08100e36b8c467da827da825d56dda0a9ee4c26b525ae81cadcde345dc407`
- Internal functions: **38,161**
- PrimaryOwner: **9,409**
- FinalNoPrimaryOwner: **585**
- CodeDomain: **27,987**
- Explicitly accounted: **37,981 / 38,161 = 99.52831%**
- Unresolved: **180**
- Cross-layer overlap: **0**
- Deterministic post-GD snapshot SHA-256: `0e017e31f74b6d1d729d3ac33d3d47395f8d49018450c0cd27f204eb5d097555`
- Fresh-reopen snapshot SHA-256: `0e017e31f74b6d1d729d3ac33d3d47395f8d49018450c0cd27f204eb5d097555` — **byte-identical**
- Authorized executable SHA-256 reported by fresh reopen: `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`

## GD semantic closure

1. `0069FB10` — `Phyre.PPhysics.Bullet.RigidBodyCompoundShapeAndBtRigidBodyMaterialization`
   - Complete body allocates a real Bullet `btCompoundShape`, materializes child collision-shape transforms, computes local inertia when required, constructs the live `btRigidBody`, and stores the Bullet runtime pointer back into the Phyre rigid-body state.
   - Real Phyre/Bullet physics class context corroborates the implementation. PE unwind/EH metadata is excluded.
   - Exact current body: **1,899 bytes**, SHA-256 `cf6912e54b0a4e374a3457be06371915bd01ef0f9eb78fa5ddd0fe8425adab94`.

2. `006A4A60` — `Phyre.PPhysics.PPhysicsRigidBody.ResetBulletTransformScaleAndActivation`
   - Reflected native metadata identifies wrapper `006A4A40` as `Phyre::PPhysics::PPhysicsRigidBody::reset`; that wrapper computes the world transform and invokes this implementation stage.
   - The body synchronizes the Bullet rigid-body transform, child collision-shape scaling, derived transform state, refresh/update behavior, and activation.
   - Exact current body: **965 bytes**, SHA-256 `9ed4a7d76a3c80c30556ba2d608302fa7aa5846219bddd20633e1a4a093625f0`.

3. `006CB2A0` — `Phyre.PRendering.D3D11.PrimitiveRenderer.DirtyStateDetectionAndCachedStateCommit`
   - Installed in the real `PrimitiveRendererD3D11` virtual path.
   - Compares live primitive-render state against the cached state used by the already-certified indexed primitive append/batching paths, commits/rebuilds that cache when dirty, and preserves the state consumed by subsequent indexed draws.
   - Exact current body: **656 bytes**, SHA-256 `b70734603b8e2935ee44999df0316c81e0558e818571a638c5d21dbe09c96101`.

## Exact mutation fence

GC-recovery baseline deterministic snapshot:
`558cb87246d6394cf90bf90182f00b8fd47ecc45bcdb62e964e16728d5e140fe`

Post-GD recovery snapshot:
`0e017e31f74b6d1d729d3ac33d3d47395f8d49018450c0cd27f204eb5d097555`

Full-function comparison:

- changed functions: **3**, exactly `0069FB10`, `006A4A60`, `006CB2A0`
- changed fields: **comment + CodeDomain tag only**
- function additions/removals: **0 / 0**
- tag removals: **0**
- body/range/name/prototype/thunk drift: **0**
- immutable drift: **0**

## Packing proof

The target DomainFile was packed in a separate headless invocation while closed:

- `open=false`
- `busy=false`
- `changed=false`
- `canSave=false`
- explicit `PACK_PASS`
- packed size: **82,101,207 bytes**

## Fresh-reopen proof

The resulting GZF was imported into a completely new Ghidra project with auto-analysis disabled. Fresh reopen reproduced:

- **38,161 functions**
- **37,981 explicit**
- **180 unresolved**
- **99.52831% coverage**
- **overlap 0**
- deterministic snapshot SHA-256 `0e017e31f74b6d1d729d3ac33d3d47395f8d49018450c0cd27f204eb5d097555`, byte-identical to post-GD
- executable SHA-256 `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`

## Continuation rule

Continue only from the fresh-reopened GD recovery artifact and regenerate evidence from its exact 180-function residual before any new mutation. `002F7380` and `00313A00` remain protected unresolved bridges unless stronger independent complete-body evidence resolves their native mechanics.
