[Home](../../README.md) / [Graphics](README.md) / Model lifecycle

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Model lifecycle: a character model from its binding to the render record's clear | lifecycle | Graphics | Character models / Model Files | The stages of a model on screen: the binding that loads its file, the bind that creates its render record, the pending wait and the promotion that binds its resources, its skeleton, attachment to a parent, the per-frame dirty walk and presentation entries, the two-step removal, the record's clear and the release of the binding; each stage linked to the page that explains it. | 0x002E28E0, 0x0042FB80, 0x004279B0, 0x0042ED60, 0x00428710, 0x00429140, 0x00427C90, 0x004200A0, 0x0041F730 |

## What the player sees

A character appears once its model has loaded and the frame it was added in has ended. It moves and plays its
motions with its weapons in hand, and vanishes when it is removed; its model data is unloaded once nothing uses
it.

## Stages

1. **Binding.** A script names the model by its bound id, and the binding entry loads the model's file
   ([script binding lifecycle](../Scripts-And-Script-Commands/script-binding-lifecycle.md),
   [model asset list](model-asset-list.md)).
2. **Bind.** `0x002E28E0` binds the entry to an actor that has a presentation context: it takes a reference on the
   entry and creates the actor's render record through `0x0042FB80`
   ([script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md#the-bind-what-binding-a-model-to-an-actor-does)).
3. **Allocation.** `0x004279B0` clears a free record, puts it on the pending list and initialises it; with all 160
   records in use, or a record with the same key already there, the request is refused
   ([character render records](character-render-records.md#allocation)).
4. **Promotion.** At the end of the field frame (`0x0042ED60`) the promoter `0x00428710` binds the model's resources,
   takes a shadow entry when the shadow code allows one, and moves the record to the active list
   ([character render records](character-render-records.md#promotion-retirement-and-clearing)).
5. **Skeleton.** The record's skeleton entry is acquired from the skeleton bank, and its bones are built from the
   model's `@FTR` node table
   ([skeleton entries and bones](skeleton-entries-and-bones.md), [model files](model-files-cm-ca.md)).
6. **Attachment.** A child record, such as a weapon or a ride, asks for a tie to a parent slot; the next request
   service resolves the slot against the parent's skeleton and ties the child to that bone
   ([character render records](character-render-records.md#attaching-a-record-the-pending-tie-and-the-slot-table)).
7. **Per frame.** The dirty-word walk and the transform commit run each frame, and the record's presentation
   entries run its track states ([character render records](character-render-records.md#the-dirty-words),
   [presentation entries](presentation-entries.md#the-per-entry-update),
   [character render object](character-render-object.md)).
8. **Removal.** `0x00429140` marks a record for removal, or unlinks and clears one still pending at once; the next
   active sweep detaches its children, frees its shadow entries and tears it down (`0x004200A0`)
   ([character render records](character-render-records.md#promotion-retirement-and-clearing)).
9. **Clear.** `0x0041F730` zeroes the record and writes its defaults, ready for the next allocation
   ([character render records](character-render-records.md#promotion-retirement-and-clearing)).
10. **Unload.** When the binding entry has no reference or holder left and is not pinned, it is retired, and the
    per-frame binding update frees it with the model's buffer ([script binding lifecycle](../Scripts-And-Script-Commands/script-binding-lifecycle.md)).

## Across transitions

- **An area unload** runs the binding update itself, so bindings already retired are freed as the zone goes
  ([script binding lifecycle](../Scripts-And-Script-Commands/script-binding-lifecycle.md),
  [changing areas](../World-Areas-And-Travel/changing-areas.md)).
- **A disposed source** first has the render records that point at it cleared
  ([resource lifecycle](../Game-Files-And-Data-Tables/resource-lifecycle.md)).

## Related

- [Character render records](character-render-records.md): the records, their pool and their events.
- [Actor model rebuild](../Characters-And-Objects/actor-model-rebuild.md): rebuilding a model in place.
- [Model files](model-files-cm-ca.md): the file a binding loads.

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Actor entity: `0x002E28E0` calls `0x0025AB30`, `0x00263FF0`; `0x002E28E0` is called by `0x0037B4D0`; those functions are
  documented on [native commands](../Scripts-And-Script-Commands/native-commands.md),
  [debug menu](../Engine-Core/debug-menu.md),
  [script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md).
- Movement: `0x002E28E0` calls `0x00269E60`, `0x00269F90`, `0x0026A370`, `0x0026AF40`, `0x0026B2E0`, `0x002E3500`, `0x002E5C90`,
  `0x002E5E10`, `0x002E8E20`, `0x002EC3F0`; `0x0042FB80` is called by `0x002E28E0`, `0x002E3110`.
- Movement: those functions are documented on
  [script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md),
  [facing and steering](../Movement-And-Pathfinding/facing-and-steering.md),
  [movement bodies and separation](../Movement-And-Pathfinding/movement-bodies-and-separation.md); and on
  [script binding lifecycle](../Scripts-And-Script-Commands/script-binding-lifecycle.md).
- Resource: `0x00429140` calls `0x002ED570`; `0x0042FB80` calls `0x00409090`; those functions are documented on
  [resource sections](../Game-Files-And-Data-Tables/resource-sections.md),
  [script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md).
- Script VM: `0x002E28E0` is called by `0x003409F0`, `0x00342640`, `0x00355210`, `0x0050D810`; those functions are documented on
  [script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md),
  [native commands](../Scripts-And-Script-Commands/native-commands.md).
- World area: `0x002E28E0` calls `0x00377C20`; those functions are documented on
  [force fight mode](../Engine-Core/force-fight-mode.md).

---

[← Model files (.cm, .ca)](model-files-cm-ca.md) | [Animation playback →](animation-playback.md)
