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
8. **Release.** On every bound slot but 4 the manager's teardown `0x002628B0` runs `0x0025B070`, which ends the movement
   job of each class-1 or class-3 record in the slot's two record ranges, runs the per-record teardown and
   releases the battle units. On every slot it then frees the record block (`0x00262D96`-`0x00262DA4`); every record
   address is valid only until then ([actor record](actor-record.md#release)).
9. **The slot's other state.** The same teardown resets the state other systems keep per slot: skips, voices, the
   summon group, event sounds and script effect slots ([actor record](actor-record.md#what-else-the-teardown-resets)).
10. **New handle.** `0x002659D0` advances a record's discriminator, so a handle taken before stops resolving. It runs
    for the verb `changeentryid` and through `0x003220E0` (`0x00322050`, `0x00322080`, the latter for `incentryid`). A
    rebuilt pool restarts every discriminator at 1 ([battle units](battle-units.md#the-handle)).

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

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Audio: `0x002628B0` calls `0x00360B50`, `0x00360DD0`, `0x003636A0`; those functions are documented on
  [music](../Sound-And-Music/music.md), [game over](../World-Areas-And-Travel/game-over.md).
- Combat action: `0x003589B0` is called by `0x00319F50`, `0x00325260`; those functions are documented on
  [zone changes and mapjump](../World-Areas-And-Travel/zone-changes-and-mapjump.md),
  [reward verbs](../Scripts-And-Script-Commands/reward-verbs.md).
- Core runtime: `0x002628B0` calls `0x00229EE0`; those functions are documented on
  [game over](../World-Areas-And-Travel/game-over.md).
- Gameplay: `0x003589B0` is called by `0x0031ADB0`; those functions are documented on
  [bestiary](../Enemy-Spawning/bestiary.md).
- Input: `0x002628B0` calls `0x0035B5D0`; those functions are documented on [vibration](../Controls-And-Input/vibration.md).
- Movement: `0x0025B070` calls `0x002E3D00`; `0x002628B0` calls `0x00263560`, `0x0026A1D0`, `0x00379070`, `0x003791C0`, `0x003792D0`,
  `0x003DAA20`; `0x00266530` calls `0x00265FF0`, `0x00268380`; `0x0026C8C0` calls `0x0026D6F0`; `0x003589B0` is called by
  `0x002E5610`, `0x002EBFA0`.
- Movement: those functions are documented on [actor record](actor-record.md),
  [frame update order](../Engine-Core/frame-update-order.md),
  [time stop and freeze](../Engine-Core/time-stop-and-freeze.md),
  [doors gates and map changes](../World-Areas-And-Travel/doors-gates-and-map-changes.md).
- Movement: and on [actor record fields](actor-record-fields.md),
  [heading speed to position delta](../Movement-And-Pathfinding/heading-speed-to-position-delta.md),
  [world lock](../Scripts-And-Script-Commands/world-lock.md).
- Party: `0x002628B0` calls `0x00358B40`, `0x00359200`; `0x0026C8C0` calls `0x003590D0`, `0x00359200`; `0x003589B0` is called by
  `0x00269C70`, `0x00326500`, `0x00353530`, `0x0050C610`, `0x0050D2F0`.
- Party: those functions are documented on [player movement](../Movement-And-Pathfinding/player-movement.md),
  [actor managers](actor-managers.md), [frame update order](../Engine-Core/frame-update-order.md),
  [party verbs](../Scripts-And-Script-Commands/party-verbs.md); and on
  [party control modes](../Engine-Core/party-control-modes.md).
- Presentation: `0x002628B0` calls `0x002E65A0`, `0x002E8CC0`, `0x003EB500`, `0x003EB5F0`; `0x0026C8C0` calls `0x002E83A0`,
  `0x002EBC30`, `0x002EDA30`, `0x002EDA40`, `0x002EDA50`, `0x002EDA60`, `0x002EDA70`, `0x002EDA80`; `0x003589B0` is called by
  `0x003A4290`, `0x003A56F0`, `0x00465120`, `0x00465690`, `0x00506700`.
- Presentation: those functions are documented on
  [frame update order](../Engine-Core/frame-update-order.md),
  [verb table](../Scripts-And-Script-Commands/verb-table.md), [actor managers](actor-managers.md),
  [authored expressions](../Game-Files-And-Data-Tables/authored-expressions.md).
- Presentation: and on [effect element runtime](../Graphics/effect-element-runtime.md),
  [effect element types](../Graphics/effect-element-types.md),
  [battle numbers](../Menus-And-HUD/battle-numbers.md).
- Resource: `0x002628B0` calls `0x0032E520`; those functions are documented on
  [debug menu](../Engine-Core/debug-menu.md).
- Save load settings: `0x002628B0` calls `0x002EF2B0`; `0x0026C8C0` calls `0x002EF2B0`; those functions are documented on
  [script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md).
- Script VM: `0x003589B0` is called by `0x00342150`, `0x00342D40`, `0x003438F0`, `0x00349C90`, `0x0034B5D0`, `0x0034BB80`,
  `0x00352270`, `0x00352940`, `0x00354F20`, `0x003555F0`, `0x00357620`, `0x0050C7A0`.
- Script VM: those functions are documented on
  [effect anchors and targets](../Graphics/effect-anchors-and-targets.md),
  [ebp text sections](../EBP-Script-Files/ebp-text-sections.md), [actor record](actor-record.md).
- Story event quest hunt: `0x0026C8C0` calls `0x00377440`; those functions are documented on
  [actor managers](actor-managers.md).
- World area: `0x002628B0` calls `0x00378230`, `0x003DFA50`, `0x003EAA00`; `0x0026C8C0` calls `0x0026DB30`; those functions are
  documented on [doors gates and map changes](../World-Areas-And-Travel/doors-gates-and-map-changes.md),
  [ebp navigation icons](../EBP-Script-Files/ebp-navigation-icons.md),
  [ard area battle data](../Game-Files-And-Data-Tables/ard-area-battle-data.md).
- World area: and on [party verbs](../Scripts-And-Script-Commands/party-verbs.md).
