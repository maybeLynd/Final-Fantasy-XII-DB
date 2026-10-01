# GR-10 answered: camera record 2 is the ordinary field camera; the intervention target is on screen while `setinterventioncamera` holds context 1 and no event camera is active (OPUS, 2026-09-30)

Register row GR-10 asks when camera record 2 is the view on screen. The script verb `setinterventioncamera` reaches
`PartyFocus_SetSecondaryPackedActorHandle` (`00359410`), which points record 2 (of the stack at `02097300`, stride
`0x110`) at camera context 1. The row could not say who sets record 2's kind (`+0xF0`) or bit 2 of the active mask
`02098DEC`. The page is [active party and the leader change](../../../11-Party/active-party-reserve-and-the-moment-the-leader-changes.md) §8b.

Static, the certified image. The checker is `gr10_camera_check.py` (output `gr10_camera_check.out`, **`FAILS 0`**). It
uses the kit's `retool.py` and `regval.py`; `structflow.py` (stride `0x110`, `seed_leas` on the stack's nine users)
found the field writers, and its one extra hit (`003CBCA0`, a 4×4 identity-matrix fill at record `+0x20`) is a
loop-join over-approximation, not a `+0xF0` store.

## The answer (OPUS)

**Record 2 is the ordinary field camera.**

- **Which record is on screen (C1).** The view selector `00259820` shows the record of the **highest** set bit of the
  active mask `02098DEC` (bits 7 down to 0). A kind-1 record follows the camera context in its `+0xF4` (`00259990`).
- **Record 2's state is refreshed every tick (C3, C4).** At its fixed tail, the world tick calls `00358EE0`
  (`00314278`). That calls `PartyFocus_ProcessActorControlPresentationState` `00358F90` whenever one of these holds:
  - there is no event focus and the leader handle `022C7FE0` is set;
  - the intervention handle `022C7FE8` is set;
  - an event focus is set while an event manager is live.

  Every call of `00358F90` sets mask bit 2 and gives record 2 kind 1 (`0035906B`–`0035908F`, reached on every path).
  In mode 0 the tick clears bit 2 first (`00358C60`). The area init zeroes the mask and every kind.
- **Only event cameras outrank it (C2).** The other mask writers are:
  - bit 5 (`002555D0`, on and off);
  - bits 4 and 6 off (`00258B90`);
  - a computed bit of 4 or above (`003D9150`);
  - bit 1 on (`0050E480`, below record 2).

  So record 2 is the view whenever no record 3–7 is active.
- **What record 2 follows (C5).** Its context `+0xF4` is written only by `0025A280(record, context)`:
  - **1** by `setinterventioncamera` (`00359424`);
  - **0** on that verb's clear (`00359499`) and on the manager-0 unload (`00262B5D`).

  The area init leaves it 0 (the leader's context).

**So the intervention target is what the player sees from `setinterventioncamera(1, n)` until the verb's clear or a
manager-0 unload, during every tick in which no event camera (records 4–7) is active.**

**In player terms:** the normal exploration camera simply switches to following the scripted "intervention" actor. A
cutscene camera, when one is running, takes over from it.

## Limits

- **Which contexts exist.** What camera contexts 0 and 1 resolve to (the `0x860`-stride context array) is the camera
  pages' matter.
- **The event cameras.** When the event cameras on bits 4–6 run is not enumerated.
- **Mode 0 only.** "Every tick" is about mode 0, where `00358C60` clears bit 2. In other modes bit 2 stays as the last
  set left it.

## Consumers (routed, not edited here)

- The active-party page §8b (FABLE's), and register row **GR-10**, via a DATA restatement request.
