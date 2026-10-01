# S-51: the relationships and script/data cells are stale against the store (OPUS, 2026-09-25, block 292)

S-51's non-runtime cells are **my own verdicts from 2026-09-20**. Both reasons they give no longer hold. The re-score is
routed to SWE2-AUDIT-SEM: raising my own verdicts would be self-acceptance.

## script/data: NOT MET, "the file-side layout of the pack that carries these tables is not documented as a format"

It is documented, and it is tested against the whole corpus.
- `06-Movement-And-Navigation/how-a-unit-finds-its-way-across-the-navigation-mesh.md` s1, `struct NavDataset
  base=section`, gives the on-disk layout of map-pack slot 4:
  - the header `u32 1`;
  - the vertex, triangle, portal and region counts;
  - base-relative offsets to vertices (8 B), triangles (8 B), portals (8 B), regions (0x22 B), the region-by-region
    adjacency matrix, the grid, and `+0x28`.
- The map-ctrl pack page's slot table places slot 4 in the pack and gives the rule for the section's position (a running
  sum after a 0x40-byte slot).
- `_experiments/evidence/navigation-dataset-layout/census.py` → `census.out.txt` (`fad7a2fb1`, 2026-09-19) parses slot 4
  of **461 of 461** map packs, and **every structural test passes**:
  - vertex and region bounds;
  - region↔triangle back-references;
  - adjacency symmetry and an empty diagonal;
  - `0xFF`-terminated grid lists;
  - header `+4` = the vertex count and `+8` = the portal count.

  That is 31,672 regions and 52,174 portals.
- The runtime binder `00384160` rebases exactly those offsets in place. So the file layout **is** the runtime layout
  with base-relative offsets: no transform stands between them.

## relationships: PARTIAL, "the mesh dataset has no relationships recorded because it has no type"

It has types, and every one is related to the root:

| type | route |
|---|---|
| `NavRunStateBlock` (the dataset root) | `PTR 0x02AEDFB0` |
| `NavMeshVertex`, `NavMeshTriangle`, `NavPortalRecord`, `NavRegionRecord` | `DYNAMIC 0020E600(NavRunStateBlock +0x0C / +0x10 / +0x14 / +0x18)` |
| `NavRegionAdjacencyEntry` (block 248) | `DYNAMIC 0020E600(NavRunStateBlock +0x1C)`, count = regionCount² |
| `NavTrailerRecord28` (block 248) | `DYNAMIC 0020E600(NavRunStateBlock +0x28)`, count = dword `+0x24` |
| `NavGridParams` (derived, not authored: CON-141) | `STATIC 0x02AEE060` |

The binding-gap text, "the portal table and two of the root's seven references undeclared", is also stale:
- `NavPortalRecord` is declared;
- `+0x1C` and `+0x28` were declared in block 248.

## What is not claimed

The runtime cell stays REPLAY (EXP-131..137) and is not argued here. A* and the step-follower's semantics are in the page
and are unchanged by this note.
