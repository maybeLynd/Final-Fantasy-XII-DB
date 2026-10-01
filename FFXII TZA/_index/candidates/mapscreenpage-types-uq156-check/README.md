# MapScreenPage type rows from FABLE's UQ-156 proposal, verified and corrected (OPUS, 2026-09-26)

**Evidence class: STATIC** (the shipping image, every instruction decoded at its address), `live_game: false`.

This answers `FABLE-REQ-OPUS-MAPSCREENPAGE-TYPES-FROM-UQ156`, which asked to propagate
[`uq156-arm-readings/types-proposal-mapscreenpage.md`](../uq156-arm-readings/types-proposal-mapscreenpage.md) into `_types`.
Every proposed row was checked against the image before it was written. The key sites were re-read by OPUS; the wider
census was done by a helper pass. Two of the proposal's rows were wrong and are written differently.

**5 / 5 pass; `result.json` is byte-identical over two runs (md5 `a0ba4b7f4910a7a62c2194eea4252dcc`).**

| case | what the image shows |
|---|---|
| `E1` | `00402D20` steps `0x70` per entry (`00402D88`) and links at `+0x60` / `+0x68` (`00402D7C` / `00402D80`); `00402C30` copies a `0x30` record into `+0x00..+0x2F` and clears the links |
| `E2` | the selector-2 scratch is `0x480` = 24 × `0x30` (`002B7490`, selector 2 at `002B74AF`); the builder's cap for `r8d = 2` is `0x18` (`003C1A71`); 24 × `0x70` = `0xBBC0 − 0xB140` |
| `N1` | the `+0x140` nodes come from selector 0 (`00402A93 xor r9d, r9d` → `003BE3A0`) |
| `N2` | node `+0x00` holds float pairs (`004029FE` / `00402A02`, stride 8); `+0x90` is their count, clamped to 3..16 |
| `N3` | the drawer tests `+0xA8` bit 0 before `sinf`, reads `+0x90`, calls `00274CA0`, follows `+0x98` |

## What changed in `_types`

- **`MapScreenMarkerNode0B0` → `MapScreenLinkNode0B0`** (FABLE §1, upheld). The nodes are the page's links between field
  points, not markers.
  - Each undirected connection is kept once.
  - Each is drawn as a sampled curve of 3–16 points; FABLE's "line" is made precise.
  - New rows: `points` (`+0x00`, float[32]; this corrects my own "NOT OBSERVED" row), `linkRecord` (`+0x80`, whose
    ids are **point indices** and which carries a middle point at `+0x88`), `pointCount` (`+0x90`), and `drawFlags`
    (`+0xA8`, bit 0 pulse; no producer in the paths read).
  - `next` and `prev` keep their links.
- **`MapScreenPage +0xB140` is `MapScreenMarkerEntry070[24]`, `0xA80` bytes, not "96 B"** (FABLE §2 contradicted).
  - It supersedes four rows. The former `qwordB1A0` / `qwordB1A8` are entry 0's `+0x60` / `+0x68`.
  - **New type `MapScreenMarkerEntry070`**: record copy `+0x00`, rect `+0x30`, scale `+0x38`, `+0x40`, measured size
    `+0x48` / `+0x4A`, `+0x4E`, links `+0x60` / `+0x68`.
- **`+0xBBC0` `markerListHead`** (typed; FABLE's name). **`+0xBBC8` `currentMarker`** is typed as an entry pointer: the
  list finders return it. The tween's `+0x30` read is in arm 2, not arm 4. **`+0xBBD0` `linkListHead`** (renamed).
- **Named with meanings, readiness unchanged:**
  - `viewBaseX` / `viewBaseY`, `zoomPercent`, `stateFlags00E0` (behaviour only), `mapData`, `mapSlot`, `pageFlags`
    (bits 0–3, bit 1 added), `mode`, `msg37Byte08` / `msg37Byte10` / `msg40Word` / `msg37Tick`.
  - **`mapPictureX` / `mapPictureY`**, not "scroll": the only writer centres the map picture.
  - **`viewSizeX` / `viewSizeY`**, not "layout size copy": the location page stores a different value, and three other
    functions rewrite `+0xBBEE`.

`types_index.py --validate`: no new errors (the store's 40 pre-existing errors are unchanged) and 0 gaps.
`TYPE-COVERAGE.md` is **not** regenerated in this publish. The generator now appends a "Validation errors" section for
those 40 errors, which arrived with other identities' changes after the last regeneration. That section belongs to the
store's owner, so the committed report stays a dated snapshot that still shows the old node name.

## Consumers of the renamed names

| consumer | state |
|---|---|
| `_types/fields.tsv`, `_types/types.tsv` | revised-here |
| `_index/TYPE-COVERAGE.md` | stale (dated snapshot; see above) |
| `_index/candidates/type-debt-by-type.tsv`, `worktree-drift-2026-09-25/`, `Tools/work` snapshots, SWE2-STRUCT's inbox | historical snapshots; left as dated records |
| `16-UI/Map-Screens/the-map-screens-and-their-shared-map-data.md` | agrees (uses neither name) |
| FABLE's proposal | agrees in §1 and in most of §2; this README records the two corrections |

Run: `python check.py` (needs `pefile` and `capstone`, and the shipping EXE at the path in the script).
