---
title: "Actor lifecycle: an actor record from its manager's bind to the release, and when its handle stops working"
kind: "lifecycle"
category: "Characters and objects"
addresses: "0x0026C8C0, 0x002679F0, 0x00266530, 0x003589B0, 0x003588B0, 0x002628B0, 0x0025B070, 0x002659D0"
---

## What the player sees

When an area or a scene loads, its characters and objects appear, run their scripts and react; in battle they
fight. When the party leaves the area or the scene ends, they all disappear together.

## Stages

1. **Bind.** When a manager slot's definition payload has loaded, `0x0026C8C0` binds it to the slot; slot 0, the
   zone's, also resets the field state that belongs to it ([actor managers](actor-managers.md#the-bind)).
2. **Pool.** `0x002679F0` builds the slot's record pool from the payload's sequences, one block holding the pointer
   table and every record ([actor record](actor-record.md#the-pool)).
3. **Initialise.** `0x00266530` fills each record and binds its script entry
   ([actor record](actor-record.md#the-initialiser)).
4. **Handle.** `0x003589B0` names a record by its index, its manager slot and its discriminator, and `0x003588B0`
   resolves the handle back ([battle units](battle-units.md#the-handle),
   [identifier spaces](../Engine-Core/identifier-spaces.md)).
5. **Run.** Each frame the records' scripts run in the frame's update order
   ([script interpreter](../Scripts-And-Script-Commands/script-interpreter.md),
   [frame update order](../Engine-Core/frame-update-order.md)).
6. **Battle unit.** A record that fights gets a battle unit from its definition
   ([battle unit construction](battle-unit-construction.md), [battle units](battle-units.md)).
7. **Hold.** A time stop or the world lock holds the record's script while the request is active
   ([time stop and freeze](../Engine-Core/time-stop-and-freeze.md),
   [world lock](../Scripts-And-Script-Commands/world-lock.md)).
8. **Release.** On every slot but 4 the manager's teardown `0x002628B0` runs `0x0025B070`, which ends the movement
   job of each class-1 or class-3 record in the slot's two record ranges, runs the per-record teardown and
   releases the battle units. On every slot it then frees the record block (`0x00262D96`-`0x00262DA4`); every record
   address is valid only until then ([actor record](actor-record.md#release)).
9. **The slot's other state.** The same teardown resets the state other systems keep per slot: skips, voices, the
   summon group, event sounds and script effect slots ([actor record](actor-record.md#what-else-the-teardown-resets)).
10. **Reuse.** `0x002659D0` advances a record's discriminator, so a handle taken before stops resolving
    ([battle units](battle-units.md#the-handle)).

## Across transitions

- **An area change** requests managers 0 to 3 for reinitialisation, and the next tick tears them down before any
  actor runs ([changing areas](../World-Areas-And-Travel/changing-areas.md)).
- **A scene** loads into manager 1, 2 or 3 through the same loader and is torn down when it is disposed
  ([event scenes](../Scripts-And-Script-Commands/event-scenes.md)).
- **Party members captured by a scene** are bound to a scene record until the scene releases them
  ([party during scenes](../Scripts-And-Script-Commands/party-during-scenes.md)).

## Related

- [Actor managers](actor-managers.md): the slots and the bind.
- [Actor record](actor-record.md): the record, its pool and its release.
- [Battle units](battle-units.md): the battle side of a record.
