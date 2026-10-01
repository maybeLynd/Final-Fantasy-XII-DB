# Affected-consumer check: BN-4, no Bullet rigid body in shipped content (OPUS, 2026-09-27)

**State: PENDING REVIEW.** Independent review is routed to SWE2-AUDIT-SPEC.

**The ruling** (control: `_index/candidates/bn4-physics-seam-route/bn4_dispatch.py`, D1-D6):
- **Every `btRigidBody` construction is enumerated.** Four functions write its RTTI vtable:
  - `00852DB0`, reached only from the seam builder `0069FB10`;
  - `00852E10`, the solver-internal fixed body, reached only from the solver virtual `0085CED0`;
  - the destructor pair.
- **A dynamics world exists only on the `PPhysicsWorld` path.** `btDiscreteDynamicsWorld`'s constructor is reached
  only from the seam walk `00698C80` and the seam chain `0069F070`.
- **The dispatchers of descriptor hook `+0x70` are enumerated.**
  - `0063B040` dispatches for all cluster objects except three sentinels.
  - `0059E300` dispatches for asset references only.
  - `0063AFF0` forwards to the base class.
  - Together they are 3 of the 22 `[reg+0x70]` sites in the Phyre range.
- **No shipped data names the class.** No shipped `.phyre` holds a physics object. A byte scan of all 89,414 extracted
  files (55 GB) finds `PhysicsWorld` in none.
- **Bounds:**
  - compressed containers are not seen by the byte scan;
  - static enumeration, not a live count.

**No accepted knowledge is replaced.** Part 1 (`01c5d983c`) and FABLE's 2026-09-22 corpus census stand. The row's
caveat, "a native installer could still drive it from non-Phyre data", is closed by D5 and D6.

**Consumers:**

| consumer | action | agreement |
|---|---|---|
| `_index/OPEN-QUESTIONS.md` BN-4 | OPEN → ANSWERED, prior status kept | revised-here |
| `23-Third-Party-Libraries/Bullet-Physics-Integration/phyre-to-bullet-rigid-body-materialization.md` | it describes the mechanism and does not claim a population; no change | agrees |

Run receipt: `bn4_dispatch.py` executed at 6f74a7839 (FAILS 0, 6 PASS lines).
