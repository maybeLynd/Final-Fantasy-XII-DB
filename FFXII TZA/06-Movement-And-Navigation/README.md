# Movement and Navigation

**Engine category.** Locomotion, pathing, navmesh, facing, and the weather-indexed field-resource banks.

| | |
|---|---|
| Classification source | PrimaryOwner: Movement |
| Functions | 485 |
| Status | see [`../_index/COVERAGE.md`](../_index/COVERAGE.md) |

## Systems in this category

- [`heading-speed-to-position-delta.md`](heading-speed-to-position-delta.md) —
  ~~**DOCUMENTED, tier 1.**~~ **AUDITED, tier 1.** *(corrected 2026-10-02, OPUS: the page's front matter says `status: AUDITED`)* How heading and speed become a per-frame step:
  ~~`x = sin(heading)*speed`, `z = cos(heading)*speed`, plus a separate vertical term.~~ `x = sin(yaw)*cos(pitch)*speed`, `y = sin(pitch)*speed`, `z = cos(yaw)*cos(pitch)*speed`, the pitch terms dropping out on the flat path *(corrected 2026-10-02, OPUS: `002E454C`–`002E459C`, IAT `008C2BB0` sinf / `008C2BA8` cosf; the page's 2026-09-02 correction)*. Includes
  the actor-class gate `(flags & 0xE0) == 0x60` that silently refuses movement, and the
  verbatim override path.

- [`how-an-animation-moves-and-turns-a-character-toward-its-target.md`](how-an-animation-moves-and-turns-a-character-toward-its-target.md) —
  ~~**DOCUMENTED, tier 1.**~~ **AUDITED, tier 1.** *(corrected 2026-10-02, OPUS: the page's front matter says `status: AUDITED`)* The attack step-in and the turn to face: authored command `0x1A`, a 128-entry request
  pool, and per-frame speed and turn curves stored in the animation container's `@FRM` entry.
- [`how-a-unit-finds-its-way-across-the-navigation-mesh.md`](how-a-unit-finds-its-way-across-the-navigation-mesh.md) —
  ~~**DOCUMENTED, tier 1.**~~ **AUDITED, tier 1.** *(corrected 2026-10-02, OPUS: the page's front matter says `status: AUDITED`)* The battle pathfinder: the navigation dataset (slot 4 of the map pack, layout
  tested on 461 of 461 files), the grid region lookup, the Dijkstra search over at most 128 regions, the
  waypoints laid on portals, the per-step re-aim - and the per-mover-class portal test that the script verb
  `setmapidfloor` opens and closes.

- [`the-unit-shape-distance-primitives.md`](the-unit-shape-distance-primitives.md) —
  ~~**PARTIAL, tier 1.**~~ **DOCUMENTED, tier 1.** *(corrected 2026-10-02, OPUS: the page's front matter says `status: DOCUMENTED`)* The shared geometry toolbox the navigation queries reach into: the
  unit-shape distance dispatch and its sphere/cylinder/box primitives, the point-in-shape
  test, the edge/triangle predicates, and the nav-grid edge-range scan that drives them.

- [`the-movement-body-pool-and-the-separation-pass.md`](the-movement-body-pool-and-the-separation-pass.md) —
  ~~**PARTIAL, tier 1.**~~ **AUDITED, tier 1.** *(corrected 2026-10-02, OPUS: the page's front matter says `status: AUDITED`)* The 128-entry movement-body pool behind the ~~movement~~ secondary context's `+0x138` (actor `+0xC0`) *(corrected 2026-10-02, OPUS: `002E353D` loads `[actor+0xC0]` and `002E3546` stores the body at its `+0x138`; the pool page's 2026-09-18 context correction)*:
  the placement record (position, cell, ground height), the collision ellipse from the character
  parameter block, the per-frame cell registration, and the world-tick separation pass that
  pushes overlapping bodies apart by weight and feeds the push into the next candidate position.

86 of 485 Movement functions carry GFZ names; the two central ones above are verified, the
rest are unverified claims. Other known anchors: `0026E8D0` resource reconfiguration (takes the Weather Slot), `0026E290` dirty observation, `00379290` the WorldAreaField to Movement bridge, `00379630` the alternate rebuild path.

**Boundary note:** Movement owns the resource/dirty transaction but *not* the Presentation table that transaction triggers - see [`../17-Presentation-Rendering/Legacy-PS2-GS/`](../17-Presentation-Rendering/Legacy-PS2-GS/).

## How to add a system here

1. Copy [`../_templates/SYSTEM.md`](../_templates/SYSTEM.md) into a descriptively-named
   subfolder (or as a `.md` file if it is a single mechanism).
2. Fill all eight sections. A missing section means `STUB` or `PARTIAL`, never `DOCUMENTED`.
3. Mirror every "What is not known" entry into
   [`../_index/OPEN-QUESTIONS.md`](../_index/OPEN-QUESTIONS.md).
4. Register any cross-subsystem chain in
   [`../_index/CALL-CHAINS.md`](../_index/CALL-CHAINS.md).
5. Obey [`../_index/EVIDENCE-STANDARD.md`](../_index/EVIDENCE-STANDARD.md).
   No banned evidence class, ever.

## Cross-subsystem neighbours — SWE2-EC7 (pass-22 dispositions)

- **Presentation - SERVICE (1 edge).** `0026E290` reaches bodies filed to presentation: `002F7380` (LegacyPS2GS) - shared machinery across the layer boundary, no shared ownership.
- **WorldAreaField - CLIENT (2 edges).** `0026E8D0`, `00379630` are also called by bodies filed to WorldAreaField (world area): `00379290` - shared machinery across the layer boundary, no shared ownership.
