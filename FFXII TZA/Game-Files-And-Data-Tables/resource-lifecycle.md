---
title: "Resource lifecycle: a loaded block from its request to the free, with registration, borrowing, moves and disposal"
kind: "lifecycle"
category: "Game files and data tables"
addresses: "0x0032E620, 0x0032E400, 0x0036A100, 0x0036A190, 0x0036BFE0, 0x0041E490, 0x00409D60, 0x003B37E0, 0x00369860"
---

## What the player sees

Models, motions and effects appear once their data has loaded and vanish cleanly when the scene that loaded them
is unloaded. An event script that loads an animation set waits while its read is armed or in flight, plays it, and
frees it. The wait also ends when the read was held back or could not be set up, so its end alone does not mean
the set loaded ([Script motion slots](resource-ownership-and-disposal.md#script-motion-slots)).

## Stages

1. **Request.** A requester files a read of a file by kind and id; its size comes from the file-size table
   (`0x0032E400`), and a file the table marks absent is never read
   ([file requests and the read queue](file-requests-and-the-read-queue.md),
   [file size tables](file-size-tables-fst.md)).
2. **Allocation.** The destination is a block of an arena, carved bottom-up (`0x0036A100`) or top-down (`0x0036A190`);
   when the arena has no room, the pressure path calls the arena's callback, compacts and retries (`0x0036BFE0`)
   ([resource arena and relocation](resource-arena-and-relocation.md#blocks),
   [resource arena and relocation](resource-arena-and-relocation.md#compaction)).
3. **Read and delivery.** The pump issues the read and, on delivery, runs the requester's callback
   ([file requests and the read queue](file-requests-and-the-read-queue.md)).
4. **Registration.** A loader registers the data as a source in the render resource bank; two sources with the same
   tag and name share one bank entry, the first registered winning
   ([resource ownership and disposal](resource-ownership-and-disposal.md#the-four-loaders-that-register-sources),
   [resource ownership and disposal](resource-ownership-and-disposal.md#the-render-resource-bank)).
5. **Use.** Effect contexts and views borrow the source in place
   ([resource ownership and disposal](resource-ownership-and-disposal.md#effect-contexts),
   [resource ownership and disposal](resource-ownership-and-disposal.md#borrowed-views)).
6. **Move.** Compaction can move a movable block. Its handle keeps its value and resolves to the new address, while a
   raw pointer a consumer kept still points at the old one
   ([resource arena and relocation](resource-arena-and-relocation.md#the-mover)).

   An effect that borrows the source is repaired against the new address when a cue of one of its instances is next
   started (`0x003B3C00` runs `0x003B3480` before `0x0024FE70`)
   ([resource ownership and disposal](resource-ownership-and-disposal.md#after-a-source-moves)).
7. **Disposal.** `0x0041E490` detaches the source in a fixed order: the render records that point at it are cleared,
   the entry's effect ticket is cancelled with its contexts and instances, and the bank entry is reset and removed
   ([resource ownership and disposal](resource-ownership-and-disposal.md#disposal-order)).
8. **Free.** The block's owner frees it (`0x00369860`); a block whose header lacks the magic ends the game with a
   dump ([resource arena and relocation](resource-arena-and-relocation.md#blocks)).

## Across transitions

- **A script motion set** is loaded, waited on and disposed by its own verbs, and the area unload releases the slots
  by their state; an armed slot survives it, and the next sweep reads the motion from the next area's `.mot`
  ([resource ownership and disposal](resource-ownership-and-disposal.md#script-motion-slots)).
- **An area change** unloads the old zone's managers before the new zone's loads are filed
  ([changing areas](../World-Areas-And-Travel/changing-areas.md)).
- **A model binding** keeps its own buffer and releases it when the binding is freed
  ([script binding lifecycle](../Scripts-And-Script-Commands/script-binding-lifecycle.md)).

## Related

- [Resource ownership and disposal](resource-ownership-and-disposal.md): owners, sources and their disposal.
- [Resource arena and relocation](resource-arena-and-relocation.md): arenas, blocks, handles and compaction.
- [Effect lifecycle](../Graphics/effect-lifecycle.md): the effect instances a source's disposal ends.

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Actor entity: `0x0032E400` is called by `0x0032FCA0`, `0x00330310`, `0x003306E0`; `0x0032E620` is called by `0x0032FCA0`,
  `0x00330310`; `0x0036A100` is called by `0x00330310`, `0x003306E0`.
- Actor entity: those functions are documented on
  [frame update order](../Engine-Core/frame-update-order.md),
  [zone changes and mapjump](../World-Areas-And-Travel/zone-changes-and-mapjump.md),
  [ps2data bin families](ps2data-bin-families.md).
- Input: `0x0032E620` is called by `0x00291C80`; those functions are documented on
  [startup constants](../Engine-Core/startup-constants.md).
- Presentation: `0x0032E400` is called by `0x003B2310`, `0x003B53C0`; `0x0032E620` is called by `0x003B2310`, `0x003B53C0`;
  `0x0036A100` is called by `0x002561C0`, `0x003325D0`, `0x003A7BE0`, `0x003A9790`, `0x003A9AD0`, `0x003A9EF0`, `0x003AA470`,
  `0x003AF2B0`, `0x003B6890`, `0x003EDAD0`, `0x00436D00`, `0x00500C00`.
- Presentation: `0x0036A100` is also called by `0x00501520`, `0x00501750`, `0x00502CB0`, `0x005032D0`, `0x00503880`, `0x00503BA0`,
  `0x00503CD0`, `0x00503E30`, `0x00504060`, `0x00504230`, `0x00504350`, `0x005043F0`; `0x0036A100` is also called by `0x0051C270`,
  `0x005211F0`.
- Presentation: `0x0036A190` is called by `0x003A7460`, `0x003A78A0`, `0x003A8020`, `0x003A9100`, `0x003A9C10`, `0x0044A620`,
  `0x0045FD50`, `0x0046F380`, `0x004FF440`, `0x00504350`, `0x00524800`, `0x00525D50`; `0x0036A190` is also called by `0x00529200`,
  `0x0052A130`, `0x0052ADF0`, `0x0052D3B0`, `0x0052E430`; `0x003B37E0` calls `0x0024F410`, `0x0024F4D0`, `0x003B39E0`; `0x0041E490` is
  called by `0x002E65A0`.
- Presentation: those functions are documented on [standard file formats](standard-file-formats.md),
  [file requests and the read queue](file-requests-and-the-read-queue.md),
  [ebp camera tables](../EBP-Script-Files/ebp-camera-tables.md),
  [character render records](../Graphics/character-render-records.md).
- Presentation: and on [effect files efx efb](../Graphics/effect-files-efx-efb.md),
  [animation driven movement](../Movement-And-Pathfinding/animation-driven-movement.md),
  [authored presentation commands](../Graphics/authored-presentation-commands.md).
- Presentation: and on [startup constants](../Engine-Core/startup-constants.md),
  [effect element types](../Graphics/effect-element-types.md),
  [effect file list](../Graphics/effect-file-list.md),
  [effect element runtime](../Graphics/effect-element-runtime.md).
- Presentation: and on [bone trails](../Graphics/bone-trails.md),
  [character effects](../Graphics/character-effects.md),
  [effect anchors and targets](../Graphics/effect-anchors-and-targets.md),
  [resource ownership and disposal](resource-ownership-and-disposal.md); and on
  [frame update order](../Engine-Core/frame-update-order.md).
- Save load settings: `0x0032E620` is called by `0x002EF300`; those functions are documented on
  [file requests and the read queue](file-requests-and-the-read-queue.md).
- Script VM: `0x0032E400` is called by `0x0050DF70`; `0x0032E620` is called by `0x0050DFE0`; `0x0036A100` is called by
  `0x0050D8F0`; those functions are documented on
  [file requests and the read queue](file-requests-and-the-read-queue.md).
- World area: `0x0032E400` is called by `0x00378540`; `0x0032E620` is called by `0x00378540`; `0x0036A190` is called by
  `0x00378540`; those functions are documented on [ps2data bin families](ps2data-bin-families.md).
- World area: `0x0032E400` is called by `0x00268750`, `0x003319D0`, `0x00378030`, `0x00379A10`, `0x003EA820`; `0x0032E620` is called
  by `0x00268750`, `0x00378030`, `0x003EA820`; `0x0036A100` is called by `0x00267930`, `0x003319D0`, `0x003EA820`; `0x0036A190` is
  called by `0x00268750`, `0x00377DC0`, `0x00378030`, `0x00378BC0`.
- World area: those functions are documented on [ps2data bin families](ps2data-bin-families.md),
  [frame update order](../Engine-Core/frame-update-order.md),
  [resource arena and relocation](resource-arena-and-relocation.md),
  [standard file formats](standard-file-formats.md).
- World area: and on [item and ability ids](../Engine-Core/item-and-ability-ids.md),
  [async load manager](async-load-manager.md), [graphics settings](../Engine-Core/graphics-settings.md).
