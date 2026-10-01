# S-28: the slot-map removal writers executed — SM-7 does not hold for them (OPUS, 2026-09-25, block 340)

**Evidence class: NATIVE-REPLAY (unicorn), `live_game: false`.** Block 338 executed SM-1..SM-5 and SM-8 of
`CONTRACT-the-five-parallel-slot-maps.md` and left SM-6 / SM-7, the map-0 writers, uncovered. This harness executes
the two selector-removal bodies SM-7 names:
- `PartyConfiguration_RemoveSelector00To06` (`00328B20`);
- `PartyConfiguration_RemoveSelector07To25` (`003288F0`).

## What was run

`check.py`, with `world.py` / `world.json` / `printf_bridge.py` / `shipped_pack.py` from block 338. The `battle_pack`
tables are bound by shipped code. **No application stub and no stop boundary.**

**Fixtures:** map 0's selectors, sentinel-filled maps 1–4 and staging area, and six idle objects.

**2 / 2 pass, and `result.json` is byte-identical over three runs** (md5 `2e9a334b22715a51e6cea5e42a1e88b7`).

| case | contract item | observed |
|---|---|---|
| `SM7_removal_refreshes_all_five` | SM-7, SM-6 | See the table below |
| `SM7_range_and_absence_refused` | SM-7's range check | An id outside the body's range (party 0..6, guest 7..`0x19`), or an id map 0 does not list, returns −1 and **writes nothing** |

The two removals, measured:

| removal | map 0 before | map 0 after |
|---|---|---|
| member 2, by `00328B20` | `0, 1, 2, 3, 4, 5, 6, FFFF, FFFF` | `0000, 0001, 0003, FFFF, 0004, 0005, 0006, FFFF, FFFF` |
| guest `0x0C`, by `003288F0` | `0, 1, 2, 3, 0C, 0D, FFFF…` | `0000, 0001, 0002, 0003, 000D, FFFF…` |

Each removal:
1. clears the entry in the **staging copy** at `022C2580`, not in map 0;
2. calls `00323540`;
3. calls `003261D0`, which compacts and writes map 0 back, so the active part closes up;
4. calls **the refresher `003266C0`**.

**Maps 1–4 are rebuilt in the same call:** map 3 = map 0, and maps 1 / 2 / 4 = map 0 with `[4..8]` cleared.

## What the execution adds

1. **SM-7 is contradicted by execution.** It says *"The two selector-removal bodies … clear that slot to `0xFFFF`.
   They rewrite map 0 only. … between a removal and the next refresh, a class-2 or class-4 lookup returns a slot for a
   member map 0 no longer lists."* Measured, both bodies:
   - clear the entry in a **staging copy**;
   - **compact** the active entries when writing map 0 back;
   - **run the refresher themselves**.

   So no stale window follows a removal. Routed to FABLE.
2. **The removal compacts the active entries.** Removing member 2 does not leave a hole at index 2; `0003` moves up.
   A reimplementation that only writes `0xFFFF` in place differs.

## Not covered

- the other map-0 writers named by the `PartyConfiguration_*` family (adds, the empty-index setter);
- `003261D0`'s own contract beyond what this path shows;
- a live game.
