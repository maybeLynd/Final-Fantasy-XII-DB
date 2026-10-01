# One bank-generic resolver routes three element types into two index entries (OPUS, 2026-09-27)

**State: REPAIRED 2026-09-27 (SWE2-STRUCT).** The routes are bank-qualified (`bank=0xD98` /
`bank=0xD90`), seeding is gated on the classified bank provenance of each call site, and
`check_route_collisions.py` refuses undiscriminated same-route/different-size FN groups. C3–C5 of
`route_collision.py` now assert the repaired invariants.

## The defect

`_types/types.tsv` gives **RenderStrideC0Element** (0xC0) and **RenderResourceEntry** (0x50) the same route,
`FN 0x002ED570+0x0`. The resolver behind that route is bank-generic:
- **Formula.** It returns `decode(chunk) + (slot & [bank+0x50]) * [bank+0x48]`, taking the stride and mask from the
  bank passed in `rcx` (C1).
- **Three banks share it.** The shared bank constructor `0051F9F0` is called with strides `0x50`, `0xC0` and `0x260`
  (C2). The 0x260 one is the RenderModelInstance size.

So the index attributes every 002ED570 caller's accesses to both declared types, clipped to each type's size. The
effects:
- **The types are merged.** All 58 functions in RenderResourceEntry's index also appear in RenderStrideC0Element's
  (C4). Every index row below `+0x50` is ambiguous between the two.
- **The third bank leaks in.** `005049E0` writes its receiver out to `+0x250`, so it initialises a 0x260 row, yet it
  sits in RenderStrideC0Element's index (C5). The size clip hides the writes that would have exposed it.

Control: `route_collision.py` — C3–C5 originally encoded the defect state and were written to flip to FAIL
on repair; they now assert the repaired invariants (routes discriminated, index split, `005049E0` excluded
from the C0 type) and PASS on the repaired tree.

## What it affects, verified

- **The store rows of both types still stand.** Their evidence cells cite hand-read sites, such as the attach
  bodies, `00372820`, and the constructor. What is unreliable is any count or "no access" statement taken from the
  index for these two types.
- **Contradiction audits are blocked for these types.** OPUS's "unobserved row vs index" audit (106 DISCOVERED rows
  whose "no access" the index contradicts) cannot use these two types' index rows as evidence until the route is
  repaired. The HM-1 package's `+0x20` correction already excludes the foreign sites by reading them.

## Repair (owner's) and the regression it needs

- **Repair.** Key the route by the bank. The three banks are reached through `RenderResourceRoot` (`EMBED
  RenderResourceRoot +0x60` is RenderStrideC0Bank), so the seed should be 002ED570's return **when rcx is that
  bank**, not every return.
- **Regression.** Add a store check that refuses two types of different sizes sharing an identical `FN` route without
  a discriminator. C3 and C4 then flip to FAIL, which is the evidence the repair landed.
- **Also examine** the other shared route, `FN 0x002EF640+0x200` (PersistentFlagPayload / SavePayload). It is
  probably a prefix overlap and was not judged here.
