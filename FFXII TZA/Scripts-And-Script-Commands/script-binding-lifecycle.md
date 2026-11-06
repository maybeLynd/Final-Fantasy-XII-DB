---
title: "Script binding lifecycle: a model binding from the script that names it to its release and the slot's reuse"
kind: "lifecycle"
category: "Scripts and script commands"
addresses: "0x002EB540, 0x002EAE20, 0x002E25E0, 0x002E6700, 0x002EAD50, 0x002E4D20, 0x002EA6E0, 0x002E28E0, 0x002E3110, 0x002EAEB0, 0x002E65A0, 0x002E9360, 0x002E6D60"
---

## What the player sees

When a scene gives a character a different body or hands an actor a prop, the scene can pause a moment while the
model loads. When nothing uses the model any more it is unloaded, and a later scene that names it loads it again.

## Stages

1. **Find or create.** A bind verb names a bound id. `0x002EB540` or `0x002EAE20` finds its entry on the live or the
   requested list, or pops a free one (`0x002E25E0`) onto the requested list, and sets the caller's holder bit
   ([script name bindings](script-name-bindings.md#find-or-create-holders-and-the-reference-count)).
2. **Load.** The request pump `0x002E6700` sizes the model's file, takes a buffer and files the read (`0x002EAD50`);
   the entry moves to the live list ([script name bindings](script-name-bindings.md#loading-an-entry)).
3. **Ready.** The completion `0x002E4D20` registers the model with the render system, and `0x002EA6E0` loads up to
   three sub-resources; when they are in, the ready bit is set, which every wait tests
   ([script name bindings](script-name-bindings.md#loading-an-entry)).
4. **Held.** The bind `0x002E28E0` and the attach `0x002E3110` each add a reference
   ([script name bindings](script-name-bindings.md#the-bind-what-binding-a-model-to-an-actor-does),
   [script name bindings](script-name-bindings.md#the-attach-slots)).
5. **Let go.** When the holders and references are gone and the entry is not pinned, the re-lister `0x002EAEB0` moves
   it to the retired list, or, while it is still loading, marks the release to happen when the load completes
   ([script name bindings](script-name-bindings.md#find-or-create-holders-and-the-reference-count)).
6. **Freed.** The per-frame binding update `0x002E65A0` releases retired entries from the oldest: `0x002E9360` queues
   the entry's lanes for unload, releases its sub-resources and buffer, and pushes the entry on the free list
   ([script name bindings](script-name-bindings.md#the-per-frame-binding-update)).
7. **Under memory pressure.** When an allocation in arena 6 or 10 fails, `0x002E6D60` unloads one queued lane and
   releases the oldest retired entry before the arena compacts and retries
   ([script name bindings](script-name-bindings.md#the-per-frame-binding-update),
   [resource arena and relocation](../Game-Files-And-Data-Tables/resource-arena-and-relocation.md)).
8. **Reuse.** The stamp rises when the entry is retired and again when it is freed, so a handle given out before
   stops resolving ([script name bindings](script-name-bindings.md#the-handle-one-number-checked-before-use),
   [identifier spaces](../Engine-Core/identifier-spaces.md)).

## Across transitions

- **An area unload** runs the per-frame binding update itself (`0x002628B0` is one of its callers), so retired
  entries are freed as the zone goes ([script name bindings](script-name-bindings.md#the-per-frame-binding-update),
  [changing areas](../World-Areas-And-Travel/changing-areas.md)).
- **A pinned entry** (pin bit `0x1` or `0x2`) is never released: when `--count <= 0` its count is clamped to 0
  instead, `count = 0` while `+0x19 & 3` is non-zero (`0x002EAF75`-`0x002EAF8C`;
  [script name bindings](script-name-bindings.md#find-or-create-holders-and-the-reference-count)).
- **A retired entry whose buffer handle is 0** is not passed to `0x002E9360`. It stays on the retired list while
  newer entries are released ahead of it (`0x002E9419`); the first per-frame update that starts with such an
  entry at the head of the list nulls the head (`0x002E6653`), so it ends on no list and its slot stays
  lost until the binding table is set up again
  ([script name bindings](script-name-bindings.md#the-per-frame-binding-update)).
- **The 129th binding** at once has no free entry, and both finders write through the null pointer
  ([native limits](../Engine-Core/native-limits.md)).

## Related

- [Script name bindings](script-name-bindings.md): the binding table in full.
- [Model asset list](../Graphics/model-asset-list.md): what a bound id names.
- [Character render records](../Graphics/character-render-records.md): where the bound model is drawn from.

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Actor entity: `0x002628B0` calls `0x0025B070`, `0x00263660`, `0x002695A0`, `0x0037B230`, `0x003B6C20`, `0x003DDC20`, `0x003DE920`;
  `0x002628B0` is called by `0x0025BFB0`, `0x0032FCA0`; `0x002E28E0` calls `0x0025AB30`, `0x00263FF0`; `0x002E28E0` is called by
  `0x0037B4D0`; `0x002E3110` is called by `0x0037B4D0`; `0x002E65A0` is called by `0x002628B0`; `0x002EAE20` is called by
  `0x0037B4D0`; `0x002EB540` is called by `0x0037B4D0`.
- Actor entity: those functions are documented on [actor lifecycle](../Characters-And-Objects/actor-lifecycle.md),
  [frame update order](../Engine-Core/frame-update-order.md),
  [startup constants](../Engine-Core/startup-constants.md), [event scenes](event-scenes.md),
  [actor record](../Characters-And-Objects/actor-record.md).
- Actor entity: and on [actor managers](../Characters-And-Objects/actor-managers.md), [native commands](native-commands.md),
  [debug menu](../Engine-Core/debug-menu.md), [script name bindings](script-name-bindings.md),
  [force fight mode](../Engine-Core/force-fight-mode.md).
- Audio: `0x002628B0` calls `0x00360B50`, `0x00360DD0`, `0x003636A0`; `0x002E9360` calls `0x003A0F80`; those functions are
  documented on [music](../Sound-And-Music/music.md), [game over](../World-Areas-And-Travel/game-over.md),
  [script name bindings](script-name-bindings.md).
- Core runtime: `0x002628B0` calls `0x00229EE0`; `0x002E65A0` is called by `0x0022A770`, `0x0022AF50`, `0x0022B000`, `0x0022B6E0`,
  `0x0022B7E0`, `0x0022B8C0`, `0x0022BC20`; those functions are documented on
  [game over](../World-Areas-And-Travel/game-over.md),
  [frame update order](../Engine-Core/frame-update-order.md).
- Input: `0x002628B0` calls `0x0035B5D0`; those functions are documented on [vibration](../Controls-And-Input/vibration.md).
- Movement: `0x002628B0` calls `0x00263560`, `0x0026A1D0`, `0x00379070`, `0x003791C0`, `0x003792D0`, `0x003DAA20`; `0x002E28E0` calls
  `0x00269E60`, `0x00269F90`, `0x0026A370`, `0x0026AF40`, `0x0026B2E0`, `0x002E3500`, `0x002E5C90`, `0x002E5E10`, `0x002E8E20`,
  `0x002EC3F0`; `0x002E3110` calls `0x002EC3F0`.
- Movement: those functions are documented on [frame update order](../Engine-Core/frame-update-order.md),
  [time stop and freeze](../Engine-Core/time-stop-and-freeze.md),
  [doors gates and map changes](../World-Areas-And-Travel/doors-gates-and-map-changes.md),
  [script name bindings](script-name-bindings.md).
- Movement: and on [facing and steering](../Movement-And-Pathfinding/facing-and-steering.md),
  [movement bodies and separation](../Movement-And-Pathfinding/movement-bodies-and-separation.md).
- Party: `0x002628B0` calls `0x00358B40`, `0x00359200`; those functions are documented on
  [player movement](../Movement-And-Pathfinding/player-movement.md),
  [actor managers](../Characters-And-Objects/actor-managers.md).
- Presentation: `0x002628B0` calls `0x002E65A0`, `0x002E8CC0`, `0x003EB500`, `0x003EB5F0`; `0x002E28E0` calls `0x002E8FD0`,
  `0x003E6150`, `0x00426FA0`, `0x00427280`, `0x0042FB80`; `0x002E3110` calls `0x002E8FD0`, `0x002EDF90`, `0x004288B0`, `0x0042F250`,
  `0x0042FB80`; `0x002E65A0` calls `0x003DD4C0`; `0x002E6700` is called by `0x002E65A0`; `0x002E9360` is called by `0x002E65A0`.
- Presentation: those functions are documented on
  [frame update order](../Engine-Core/frame-update-order.md), [verb table](verb-table.md),
  [party during scenes](party-during-scenes.md), [script name bindings](script-name-bindings.md),
  [battle verbs](battle-verbs.md), [party verbs](party-verbs.md).
- Presentation: and on [game application](../Engine-Core/game-application.md),
  [add motion tables](../Graphics/add-motion-tables.md),
  [authored presentation commands](../Graphics/authored-presentation-commands.md),
  [bone trails](../Graphics/bone-trails.md).
- Resource: `0x002628B0` calls `0x0032E520`; `0x002E4D20` calls `0x00409090`; `0x002E6700` calls `0x0032E400`; `0x002EAD50` calls
  `0x0032E400`, `0x0032E620`; those functions are documented on [debug menu](../Engine-Core/debug-menu.md),
  [script name bindings](script-name-bindings.md),
  [startup constants](../Engine-Core/startup-constants.md).
- Save load settings: `0x002628B0` calls `0x002EF2B0`; those functions are documented on
  [script name bindings](script-name-bindings.md).
- World area: `0x002628B0` calls `0x00378230`, `0x003DFA50`, `0x003EAA00`; `0x002E28E0` calls `0x00377C20`; those functions are
  documented on [doors gates and map changes](../World-Areas-And-Travel/doors-gates-and-map-changes.md),
  [ebp navigation icons](../EBP-Script-Files/ebp-navigation-icons.md),
  [ard area battle data](../Game-Files-And-Data-Tables/ard-area-battle-data.md).
- World area: and on [force fight mode](../Engine-Core/force-fight-mode.md).
