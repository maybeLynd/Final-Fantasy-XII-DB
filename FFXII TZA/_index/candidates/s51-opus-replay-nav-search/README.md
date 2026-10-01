# S-51: the navigation contract's NV-1, NV-2 and NV-3 executed over a shipped mesh (OPUS, 2026-09-26)

**Evidence class: NATIVE-REPLAY (unicorn), `live_game: false`.**

**The gap.** S-51's runtime cell stays REPLAY because its executions (EXP-131–137, and the closers so far) cover consumer
anchors with `contract: none`, not `CONTRACT-navigation-search-and-follow`'s own invariants. This harness runs the contract's
entries on real data.

## What was run

`check.py` runs over block 345's world (`../s25-opus-replay-enmity/check.py`, whose cases run first; `result.json` keeps md5
`49662471…`). Battle units are installed there by the shipped installer.

- **The mesh.** It is slot 4 of the shipped map pack `ps2data/plan_master/map_ctrl/frs01/frs0101/bin/frs0101.mpk`, cut
  exactly as the [navigation census](../../../_experiments/evidence/navigation-dataset-layout/census.py) cuts it: 22 regions in
  two connected components.
  - It is copied to memory and **bound by `00384160`**, which stores `[02AEDFB0]` and rebases the header offsets in place.
- **The points.** Starts and goals are region centroids computed from the mesh's own triangles. Each one resolves back to
  its region through `00383F10` (checked, R0).
- **The `NavPath`** is initialised by the game's own wipers `003839F0` / `003839C0`.
- **Import bridges by name, with library semantics:** `_fdclass` (the float class of `xmm0`) and `_hypotf`.
  *Qualified 2026-09-28 (OPUS), on ASTRA-RETURN-OPUS-CRT-FDCLASS-DEPENDENCY.* The bridge's class codes are NaN 2,
  infinity 1, zero 0, subnormal −2 and normal −1, read from the low 32 bits of `xmm0`. They agree code for code with
  ASTRA's static reading of the installed `ucrtbase.dll` `_fdclass`: 65 bytes, no memory operand, no MXCSR access,
  sign ignored. The game tests only AX. ASTRA's reading binds that host DLL, not the game's actual IAT resolution,
  so the bridge is consistent with one real implementation, not proven to be the one the game loads. No bridge
  defect.
- **No application stub.**
- **The instrument.** A hook at `0038319D`, the Dijkstra array set-up past every early exit, counts the searches that ran
  Dijkstra.

**9 / 9 pass; `result.json` is byte-identical over two runs (md5 `e0c4bd61…`).**

| case | contract item | observed |
|---|---|---|
| `R0_mesh_bound_by_00384160_and_regions_resolve` | — | the root is the section, the header offsets are rebased, and all 22 centroids resolve to their own regions |
| `N1_same_region_returns_0_no_dijkstra` | NV-3, outcome 1 | start and goal in one region: returns 0, **no Dijkstra** |
| `N2_connected_pair_dijkstra_once_route_chains` | — | region 0 → 21: Dijkstra runs **once**, it returns 0, and `next[]` chains **0 → 1 → 2 → 3 → 4 → 19 → 20 → 21** |
| `N3_held_route_no_dijkstra_only_goal_waypoint_refreshed` | NV-3, outcome 3 | the goal moved inside region 21: returns 0 with **no Dijkstra**, and **only waypoint[21]** changes |
| `N4_unreachable_dijkstra_minus1_dead_end_recorded` | — | region 0 → 10 (the other component): Dijkstra runs, it returns **-1**, start/goal become `0xFF`, and `(0, 0x0A)` is written into the dead-end memory at `+0x0C` |
| `N5_dead_end_refused_without_dijkstra` | NV-3, outcome 2 | the same pair again: **-1 with no Dijkstra** |
| `N6_NV1_locomotion_reset_wipes_route_keeps_dead_ends` | NV-1 | on a real unit, `BattleLocomotion_ResetPathAndSetTargets` `003291B0` (on unit `+0x80`, whose `+0x180` is the `NavPath` at unit `+0x200`) sets `next[]` to all `0xFF` and **keeps the dead-end pair**. Afterwards the connected pair runs Dijkstra again, and the unreachable pair is **still refused without Dijkstra** |
| `N7_NV2_flagged_units_both_wiped_unflagged_untouched` | NV-2 | `003278D0` wipes **both** caches on every unit whose byte 0 bit 4 is set. A unit without that bit is untouched |
| `N8_NV2_count_reread_each_iteration_perturbation_covers_the_extra_slot` | NV-2 | with the count cell lowered by one, the last slot is **not** visited (control). With the same lowering, plus a disclosed perturbation that raises the count back during the walk, the last slot **is** wiped. The bound is re-read at `00327910`, not hoisted |

**One precision the run adds.** The two wipers write exactly `next[0..127] = 0xFF` (`003839F0`) and the two dead-end pairs at
`+0x0C` = `0xFFFF` (`003839C0`). **Neither touches the start and goal words at `+4` / `+8`.** After a locomotion reset, those
words keep their last values, and the held-route test finds `next[start] = 0xFF` and searches again.

## Not covered

- NV-4 (the shared clearance rule): static, from the caller census.
- NV-5 (the `1.414` factor at the step's call sites): static bytes. `0030A130` is not executed here.
- NV-6 (per-class portal openness): carried by the contract from the page. `setmapidfloor` and the class masks are not
  driven here.
- The follower `00383670` and the re-aim `00383C90`.
- A live game.
