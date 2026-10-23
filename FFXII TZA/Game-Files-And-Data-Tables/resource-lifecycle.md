---
title: "Resource lifecycle: a loaded block from its request to the free, with registration, borrowing, moves and disposal"
kind: "lifecycle"
category: "Game files and data tables"
addresses: "0x0032E620, 0x0032E400, 0x0036A100, 0x0036A190, 0x0036BFE0, 0x0041E490, 0x00409D60, 0x003B37E0, 0x00369860"
---

## What the player sees

Models, motions and effects appear once their data has loaded and vanish cleanly when the scene that loaded them
is unloaded. An event script that loads an animation set waits until it is in memory, plays it, and frees it.

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
   raw pointer a consumer kept still points at the old one; an effect that borrows the source is repaired against
   the new address when it is next advanced
   ([resource arena and relocation](resource-arena-and-relocation.md#the-mover),
   [resource ownership and disposal](resource-ownership-and-disposal.md#after-a-source-moves)).
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
