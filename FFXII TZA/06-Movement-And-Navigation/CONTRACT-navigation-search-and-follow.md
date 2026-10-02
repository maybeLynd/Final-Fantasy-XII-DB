---
contract: Find a route across the navigation mesh and walk it — two caches, one shared clearance rule, and a factor that is not root two
category: 06-Movement-And-Navigation
scope: subsystem
level: L2
readiness: CONTRACT READY
confidence: PROVEN
implements: 06-Movement-And-Navigation/how-a-unit-finds-its-way-across-the-navigation-mesh.md
entries: ["00382FF0", "00383670", "00383C90", "003842E0", "003278D0", "0030A130"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-22 (FABLE) on this document's own citations, every
    one resolving into a known section of the authority image; and §4's invariants measured from the
    shipping bytes — the invalidator disassembled in full, the callers of **both** cache wipers and
    of both geometry leaves censused image-wide and compared as sets, the clearance helper's caller
    count taken as the control on the shared-rule claim, and the clearance constant resolved from
    the image to its exact `f32` value and compared against `sqrt(2)`. **This records checks
    performed on that date, not the method of the original derivation**, which is on the navigation
    page; see §15.
last_reviewed: 2026-09-29
audit:
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-nav-search-falsification-pass-1
  crossref_clean: false
  reopened_count: 0
---

# Contract — navigation search and follow

> **Authored 2026-09-22 by FABLE.** S-51's binding gap ends *"A\* and the step-follower are
> untouched"* — its one contract,
> [`CONTRACT-corridor-query-family.md`](CONTRACT-corridor-query-family.md), covers the corridor
> query. **This takes the search and the follower.** The portal table and the root's two
> undeclared references are type work and are not claimed here.
>
> Written against FRONTIER's adequacy test: *a narrower contract is adequate exactly when the
> system's operations have no cross-operation invariant or ordering it leaves unstated.* §4 is six
> such invariants — and **NV-1 and NV-2 are about when one operation's cached answer stops being
> valid for the other**, which neither body states.

## 1. Purpose

Decide which way a unit should walk, remember it, and hand out one waypoint at a time.

## 2. Interface

| | body | size |
|---|---|---:|
| the search | `Navigation_FindPathAndBuildPortalWaypoints` (`00382FF0`) | 1,575 B |
| one step of the follow | `00383670` | 204 B |
| re-aim the current waypoint | `Navigation_AdjustPortalWaypointForClearance` (`00383C90`) | 632 B |
| the clearance rule | `Navigation_OffsetPointAlongSegmentForClearance` (`003842E0`) | **2 callers, and they are the two above** |
| wipe the route | `Navigation_ResetPathPredecessors` (`003839F0`) | **3 callers** |
| wipe the dead ends | `003839C0` | **2 callers** |
| invalidate everything | `003278D0` | 84 B |
| the clearance radius | `BattleUnit_GetNavigationClearanceRadius` (`0030A130`) | 40 B |

## 3. Types

```
NavPath   at unit + 0x200, 0x490 bytes
  +0x00  i32      the region the mover was last placed in
  +0x04  i32      start region of the held route, 0xFF = none
  +0x08  i32      goal region of the held route
  +0x0C  u8[2]    the last (start, goal) pair with NO route   \  the dead-end memory,
  +0x0E  u8[2]    the pair before that                        /  two deep (NV-1)
  +0x10  u8[128]  next[region]; 0xFF ends the chain              the held route (NV-1)
  +0x90  xz[128]  waypoint[region]
```

## 4. Preconditions · postconditions · invariants

### The six cross-operation invariants

**NV-1 — The two caches have DIFFERENT invalidation sets, and the difference is observable.**
Censused image-wide: **`003839F0` (the route) has three callers; `003839C0` (the dead ends) has
two.** Both are called by the unit reset and by the override invalidator — but
**`BattleLocomotion_ResetPathAndSetTargets` (`003291B0`, at `003291CF`) calls only `003839F0`.**
*So a locomotion reset throws away the route a unit had and keeps both remembered failures: the unit
will search again for a goal it could reach, and will still refuse instantly a `(start, goal)` pair
it failed before. The page states the two caches as a pair; they are not wiped as a pair.*

**NV-2 — One script action invalidates both caches for every live unit, and it re-reads the unit
count on every iteration.** `003278D0` walks slots, requires `test byte ptr [rax], 0x10`
(`003278F2`), and calls **both** wipers on `unit + 0x200` (`00327901`, `00327909`). The bound is
`BattleUnit_GetSlotCount` called **inside** the loop at `00327910`, not hoisted. *This is what makes
the caches safe: opening or closing a door with `setmapidfloor` cannot leave a stale route anywhere,
and a unit that appears during the walk is still covered by the re-read bound.*

**NV-3 — Three of the search's four successful outcomes never run Dijkstra.** Same region; a
`(start, goal)` pair in the dead-end memory (returns `-1` without searching); and a held route whose
`next[]` chain still runs from the start region to the goal, where **only the goal's own waypoint is
refreshed**. *A unit chasing a target that moves about inside one region never searches twice — the
cost of pursuit is the cache, not the search.*

**NV-4 — The search and the follower apply the SAME clearance rule, and that is provable from the
caller set rather than by reading both.** `003842E0` has **exactly two call sites in two functions**
— `00382FF0` at `0038351C` and `00383C90` at `00383EB1`. `00382EA0`, the point-to-segment leaf, has
four sites in three functions, **two of them inside `00383C90`** — the two distances the re-aim
divides. *So the waypoint a route is built with and the waypoint it is re-aimed to during the walk
are produced by one rule, and a port that re-derives the follower's geometry independently will
drift from the search's.*

**NV-5 — The clearance factor is the decimal literal `1.414`, NOT root two — and it is applied by
the caller, not by the function usually credited with it.** `0030A130` is 40 bytes and returns
`maxss` of the actor's two collision radii — **no multiplication at all**. The navigation step
multiplies at **both** of its call sites (`00325BFA`, `00325C49`) by the `f32` at `00D10818`:

```
stored           0x3FB4FDF4 = 1.4140000343
sqrt(2)                     = 1.4142135624
nearest f32 to sqrt(2)      = 0x3FB504F3
```

*The stored value is **0.015 % below** root two.* Since the radius decides whether a portal counts
as narrower than the mover and how far a waypoint is pushed from a portal's end, **a port writing
`sqrtf(2.0f)` produces a different waypoint on portals near the threshold.** The navigation page
writes the factor as "1.414 ×" and attributes it to `0030A130`; the value is right and the home is
not.

**NV-6 — A portal's openness is per mover class, and the class number is the script verb's `kind`.**
Carried from [the page](how-a-unit-finds-its-way-across-the-navigation-mesh.md) §§5 and 7 and **not
re-derived here**: the mover class is the unit's `+0x1F4`; `setmapidfloor`'s `kind` uses the same
small indices; class 4 has no bit and its 1,886 scripted calls reach a bare return. Costs are
`trunc(100 × d)` integers measured entry-point to portal, with the goal's leg added only on the last
hop. *The relevance here is that NV-3's route cache is keyed on regions alone, so a route cached
before an override change would be valid for the wrong class — which is exactly what NV-2 prevents.*

## 5. State

**Owned:** the unit's `NavPath`. **Read, never written:** the mesh, the portal table, the override
table. **Written elsewhere:** nothing.

## 6. Relationships

| | |
|---|---|
| **Sibling** | [`CONTRACT-corridor-query-family.md`](CONTRACT-corridor-query-family.md) — S-51's contracted half |
| **Invalidated by** | `setmapidfloor`, through `003278D0` (NV-2) |
| **Consumed by** | the battle unit's navigation step, which abandons its step on any return but `0` |
| **Uncontracted** | the portal table and the root's two undeclared references — type work, not claimed here |

## 7. State transitions

Per request: *locate both points → same region? → dead end remembered? → held route still good? →
else Dijkstra over at most 128 regions → lay waypoints backward from the last settled region.* Per
step: *advance `next[]` while already inside the next region → re-aim this region's waypoint → store
the region back.* The dead-end memory transitions only by being pushed onto, or wiped (NV-1).

## 8. Script · resource · event interactions

The mesh, the portals, their class masks and their map ids are authored. ~~**`setmapidfloor` is the~~
~~only script verb that reaches this subsystem**~~ **Every verb of the map-id override family `00F6`–`0103` and `0107`–`010B` reaches this subsystem** — floor, wall and mj alike *(corrected 2026-10-02, OPUS: `003278D0` is called by the setters `0026E130`, `0026E150`, `0026E850`, `0026E880` (and by `0026E960` at area start), whose callers are the tails of those nineteen verbs (FABLE's record readiness-apply-fable-1002))*, and it reaches it by invalidation rather than by
parameter (NV-2).

## 9. Determinism

Deterministic. No generator is drawn. *But not memoryless*: the same request can return `-1` without
searching because of NV-3's dead-end memory, so a reimplementation without the two-deep memory
answers the same question differently.

## 10. Failure paths and edge conditions

- Return codes partition the outcomes: `0` route, `-1` none, `-2` start off the mesh, `-3` goal off
  the mesh; the caller abandons its step on anything but `0`.
- An unreachable goal costs **one** full search and then nothing until the pair changes or a wipe
  (NV-3).
- A locomotion reset leaves the dead ends in place (NV-1).

## 11. Observable behaviour

A creature that cannot reach you stops trying almost immediately and starts again the moment a door
opens somewhere in the area.

## 12. Reproduction formula

Census the callers of both wipers and assert **3 and 2**, with `003291B0` in the first set only
(NV-1). Reset locomotion after a failed search and assert the next identical request still returns
`-1` without searching. Census `003842E0` and assert **exactly two callers**, the search and the
re-aim (NV-4). Read `00D10818` and assert `0x3FB4FDF4`, not `0x3FB504F3` (NV-5).

## 13. Runtime validation

**The query tree below this subsystem is executed** — [`EXP-131`](../_experiments/EXP-131-navgrid-query-exec.md),
adopted 2026-09-20 — and six families are recorded as executed on the page. **Neither the search nor
the follower is among them**, and this contract claims no runtime evidence of its own. S-51's
runtime cell is not addressed here. *Stated rather than left blank so a CONTRACT READY header is not
read as evidence of execution.*

## 14. Unresolved

- Why a locomotion reset keeps the dead ends (NV-1) — deliberate, or an omission.
- What class 3's probe-gate bit means for the creature that has it, and what kinds `0`, `7` and `9`
  of the verb gate — [the page](how-a-unit-finds-its-way-across-the-navigation-mesh.md)'s own open
  items, not re-opened here.
- ~~The locomotion solver that consumes the waypoint.~~ *(answered: see [battle locomotion](Battle-Locomotion/battle-locomotion-steering-and-recovery.md), the solver read; 2026-10-02, OPUS)*

## 15. Evidence

| claim | evidence | tier |
|---|---|---|
| NV-1 — 3 callers against 2 | both wipers censused image-wide and the two caller sets compared; `003291B0` present in one and absent from the other | 1 |
| NV-2 — the invalidator | `003278D0` disassembled in full: the `0x10` gate at `003278F2`, both wipe calls, and the bound re-read at `00327910` | 1 |
| NV-4 — one clearance rule | `003842E0` censused — **exactly 2 call sites in 2 functions**, which is the control: a third caller would defeat the claim | 1 |
| NV-5 — the constant and its home | `0030A130` disassembled in full (no multiply); both `mulss` sites read; `00D10818` resolved from the image and compared with the nearest `f32` to `sqrt(2)` | 1 |
| NV-3, NV-6 — the caches, the cost model and the class gate | [the navigation page](how-a-unit-finds-its-way-across-the-navigation-mesh.md) §§4–7 | 1 |

## 16. Parity plan

L3 is out of scope. A reimplementation is judged on NV-1 through NV-5. **NV-5 is the cheapest to get
wrong and the hardest to notice**: `1.414f` and `sqrtf(2.0f)` differ in the fourth decimal, and the
difference only shows on portals within a fraction of a centimetre of twice the mover's radius.
**NV-1 is the one most likely to be "tidied"**: wiping both caches together is the obvious design and
is not what the engine does.

## 16a. Crossings into other layers (FABLE, 2026-09-22)

- **MovementAndNavigation — internal.** The search, the follower, the clearance rule and both wipers
  are this category's own.
- **ActorEntity — SERVICE, and NV-2 rests on it.** The invalidator reaches every unit through the
  battle-unit slot pool, and the clearance radius comes from the actor's collision pair; this
  contract asserts the walk and the `maxss`, **not the pool's own behaviour or the radii's origin**.
- **CombatAction — MECHANICAL.** The navigation step that applies NV-5's factor and abandons on a
  non-zero return belongs to that layer; NV-5 cites its two `mulss` sites and nothing else about it.
- **Script_VM_Native_Bridge — SERVICE, and NV-2 and NV-6 are the statement.** ~~`setmapidfloor` is the~~
  ~~only verb that reaches this subsystem.~~ Every override verb `00F6`–`0103`, `0107`–`010B` reaches it through `003278D0` *(corrected 2026-10-02, OPUS: the callers of `003278D0` and of its setters, §8)*. *Its tail and jump table are on the page and are not
  re-derived here.*
- **Presentation — SERVICE, and it owns a leaf this contract leans on.** The point-to-segment
  routine `00382EA0` that NV-4 counts carries that layer's ownership, not this one's, although both
  of its navigation callers are here. **NV-4's claim is about the caller SET of that leaf and of the
  clearance helper — how many there are and which — and asserts nothing about the leaf's own
  arithmetic**, which the page records and this contract does not re-derive.
- **CombatAI — MECHANICAL.** Two further callers of the clearance-radius helper `0030A130` belong to
  that layer. **NV-5 is a statement about what that helper does NOT do — it applies no factor — and
  about the two `mulss` sites in the navigation step; other callers of it are outside the claim**,
  and whether they apply a factor of their own is not established here.
- **Every other layer reached is MECHANICAL**, through these bodies' own callees. *Their addresses
  are deliberately not cited: each is a hub, and naming one imports its whole edge set.*

> **Dispositioned by name on purpose.** The crossings pre-check credits a layer for its alias
> appearing as a whole word anywhere in a document, so words like *movement*, *actor* and *script*
> in ordinary prose can clear a layer that nothing here dispositions — the defect measured in
> `_index/candidates/fable-crossings-prose-false-clears.tsv`. The paragraphs above, not those words,
> are what discharge these.

## 17. Related

- [How a unit finds its way across the navigation mesh](how-a-unit-finds-its-way-across-the-navigation-mesh.md) — the mechanism
- [Contract — the corridor query family](CONTRACT-corridor-query-family.md) — S-51's contracted half
- [Battle locomotion steering and recovery](Battle-Locomotion/battle-locomotion-steering-and-recovery.md) — NV-1's third caller and NV-5's applier

## Cross-subsystem neighbours — SWE2-EC7 (pass-22 dispositions)

- **ActorEntity - CLIENT and SERVICE (5 edges).** `003839C0` is also called by bodies filed to ActorEntity: `00236A60`; `0030A130`, `003278D0` reach bodies filed to ActorEntity: `00265090`, `00236820`, `00236850` - shared machinery across the layer boundary, no shared ownership.
- **CombatAI - CLIENT (2 edges).** `0030A130` is also called by bodies filed to combat AI: `0031E6F0`, `0031E760` - shared machinery across the layer boundary, no shared ownership.
- **CombatAction - CLIENT (6 edges).** `0030A130`, `003291B0` are also called by bodies filed to combat action: `00320E10`, `002FDA60`, `002FDC30` - shared machinery across the layer boundary, no shared ownership.
- **Presentation - SERVICE (2 edges).** `00382FF0`, `00383C90` reach bodies filed to presentation: `00382EA0` - shared machinery across the layer boundary, no shared ownership.

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page.*

**Status_Periodic_Terminal — SERVICE (1 edge).** The unit reset `BattleUnit_ResetStateForReuse` (`00236A60`), cited here as a caller of the route wipe, also calls `BattleUnit_TakeAndClearPrimaryResourceRecoveryAccumulator` (`00320450`), an 87-byte body that zeroes the unit's float at `+0x70` and returns its old value only when the unit is live and its status words pass the field bit15 test. A unit being reset for reuse drops its pending periodic resource-recovery credit along with its route; that belongs to the periodic layer, not to navigation.

## Falsification pass 1 — 2026-09-29 (OPUS): every invariant survives

**Attack.** The structural clauses of §2 and NV-1 to NV-5 became checks that fail if the shipping image says otherwise. The
checks decode every listed body in `.text`, so the caller counts are whole-image. Script:
`Tools/analysis-kit/gfz-scripts/falsify_nav_search.py`, output `falsify_nav_search.out`, image `73461d08…`, 0 BROKEN.
NV-6 is carried from the page, as its own text says, and is not attacked here.

| # | Clause attacked | Result |
|---|---|---|
| N0 | §2 sizes | **survives**: 1,575 / 204 / 632 / 40 / 84 B |
| N1 | NV-1 the two wipers' caller sets | **survives**: the route wipe is called by the unit reset `00236A60`, the invalidator `003278D0` and the locomotion reset `003291B0` (`003291CF`); the dead-end wipe by the first two only |
| N2 | NV-2 the invalidator | **survives**: it tests `byte [unit], 0x10`, calls both wipers on `unit + 0x200`, and re-reads the slot count at `00327910` before the back-edge `jl 003278E6` |
| N3 | NV-4 one clearance rule | **survives**: `003842E0` has exactly two call sites (`0038351C`, `00383EB1`); `00382EA0` has four sites in three functions, two in `00383C90` |
| N4 | NV-5 the factor and its home | **survives**: `0030A130` is `maxss` of two radii with no multiply; its callers multiply by `[00D10818]` = `0x3FB4FDF4` (1.414) at `00325BFA` and `00325C49` |

No correction.
