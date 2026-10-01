# S-41: the spatial source objects executed for the first time — five classes, slot 34 and slot 39, stub-free (OPUS, 2026-09-26)

**Evidence class: NATIVE-REPLAY (unicorn), `live_game: false`.**

**The gap.** `CONTRACT-spatial-source-objects` (SA-1..SA-7) had **no execution record**. The exposure note records this as
coverage, not exposure.

## What was run

`check.py` runs over block 355's world (`../s29-opus-replay-inventory-rebase/world.py`, whose real initialisers build it),
plus **three real initialiser steps**:
1. **`00210AF0`**, the audio object's own lazy initialiser.
2. **`007AD620(00210EC0, 00210EB0)`**, the audio library's allocation-callback installer, called with **exactly the two
   functions the library init passes**: `00210760` loads them with `lea 00210EC0` at `0021082A` and `lea 00210EB0` at
   `00210841`, and passes them through `007A4D50` to `007AD620`. The rest of that init sits under `001DBA40`, which needs
   `CreateThread`, and is not run.
3. **`007BB620`**, the listener's own initialiser: 0xA0 bytes via `007AD460` → `[02EAD0B0]`, constructor `007EF100`,
   cell `02EADE08`.

**The source objects are planted data.** Each is a 0x1000-byte block with:
- its class vtable at `+0`: Dynamic `01CB99F0`, Point `01CB9B40`, Ambient `01CB9C88`, Direction `01CB9DD0`, Polygon
  `01CB9F18`;
- the radius at `+0xE4`, and a vector (1, 2, 3, 7) at `+0x100`;
- for Polygon, three vertices counted at `+0x108`, inline from `+0x110`, with mode byte `+0x104`.

Slot 34 and slot 39 are **read from each vtable and called**. No application stub. Every write into each object is
recorded.

**12 / 12 pass, and `result.json` is byte-identical over two runs** (md5 `e9ae3596228dab44d248672f73e9f4ed`).

| case | item | observed |
|---|---|---|
| `real_initialisers_audio_callbacks_listener` | — | all three return; the listener object is built |
| `slot34_targets_are_the_five_contract_bodies` | SA-1 | the five vtables' slot 34 are `007F1340`, `007F1A50`, `007F1D10`, `007F1F80` and `007F25E0` |
| `SA1_all_five_write_D0_DF_and_E0` | SA-1 | every class writes the position `+0xD0..+0xDF` and the byte `+0xE0` |
| `SA1_nothing_outside_D0_E0_written_by_two_classes` | SA-1 | **no class writes anything outside `+0xD0..+0xE0`** in these runs |
| `SA2_ambient_w_1_direction_copies_vector_and_forces_w` | SA-2 | Ambient: `(0, 0, 0, 1.0)`. Direction: `(1, 2, 3, 1.0)`, so the stored `w` 7.0 never reaches the output |
| `SA3_ambient_direction_E0_always_1` | SA-3 | `+0xE0 = 1` at radius 10, 2 and 0 alike |
| `SA3_point_dynamic_polygon_E0_is_distance_below_radius` | SA-3 | `+0xE0 = (distance(+0xD0, listener) < +0xE4)`, taking the listener position from the real listener object: Point at 3.74 → 1 at radius 10, 0 at radius 2; Polygon the same (nearest vertex). With radius 0, all three write 0 |
| `SA4_the_other_four_classes_never_write_the_radius` | SA-4 | Point, Ambient, Direction and Polygon never write `+0xE4`, in any run |
| `SA4_dynamic_mode0_path_leaves_the_radius_unwritten_…` | SA-4 | Dynamic's store `007F13EC` is gated on `+0x140 == 1` (`007F1379`) **and** a live audio-library handle at `+0x38` (`007A8C30` → registry `007B24F0` / `007B2470`, under a lock). In mode 0 it does not write `+0xE4`, as the gate predicts |
| `SA5_base_vtable_slot34_is_zero` | SA-5 | `SoundObject`'s vtable `01CBAB68` slot 34 reads 0. This is a static read |
| `SA6_slot39_true_for_point_dynamic_polygon_false_…` | SA-6 | slot 39 returns 1 for Point, Dynamic and Polygon, and 0 for Ambient and Direction |
| `no_fence_no_fault` | — | every call returns |

## Observations (not contract items)

- **Point's slot 34 passes the stored `w` through:** `+0xD0` = (1, 2, 3, **7**). SA-2 claims forcing only for Ambient
  and Direction, so this is consistent. It is recorded because a port that forced `w` everywhere would differ here.
- **Polygon mode 1** (`+0x104 ≠ 0`) computes a point on the polygon, (−1.958, 1.414, 1.414), rather than the nearest
  vertex.

## Not covered

- **Dynamic's handle path**, and so its own radius write (SA-4's positive half). It needs an emitter registered in the
  audio library, and that registry is built by the thread-starting audio init;
- **SA-7**, an image-wide census: static structure, not executable;
- a live game.
