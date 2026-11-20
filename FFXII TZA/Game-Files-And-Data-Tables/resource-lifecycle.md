[Home](../../README.md) / [Game files and data tables](README.md) / Resource lifecycle

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Resource lifecycle: a loaded block from its request to the free, with registration, borrowing, moves and disposal | lifecycle | Game files and data tables | Loaded resources | The stages a loaded resource passes through: the request sized from the file-size table, the arena allocation and its pressure path, the queued read and delivery, registration as a render source, borrowing by effects and views, the move compaction can make and its repair, disposal in its fixed order, and the owner's free; each stage linked to the page that explains it. | 0x0032E620, 0x0032E400, 0x0036A100, 0x0036A190, 0x0036BFE0, 0x0041E490, 0x00409D60, 0x003B37E0, 0x00369860 |

## What the player sees

Models, motions and effects appear once their data has loaded and vanish cleanly when the scene that loaded them
is unloaded. An event script that loads an animation set waits while its read is armed or in flight, plays it, and
frees it. The wait also ends when the read was held back or could not be set up, so its end alone does not mean
the set loaded ([Script motion slots](resource-ownership-and-disposal.md#script-motion-slots)).

## Stages

| Step | What happens | Where in the code |
|---|---|---|
| 1 | **Request.** A requester files a read of a file by kind and id; its size comes from the file-size table, and a file the table marks absent is never read ([file requests and the read queue](file-requests-and-the-read-queue.md), [file size tables](file-size-tables-fst.md)). | `0x0032E400` |
| 2 | **Allocation.** The destination is a block of an arena, carved bottom-up or top-down; when the arena has no room, the pressure path calls the arena's callback, compacts and retries ([resource arena and relocation](resource-arena-and-relocation.md#blocks), [resource arena and relocation](resource-arena-and-relocation.md#compaction)). | `0x0036A100`<br>`0x0036A190`<br>`0x0036BFE0` |
| 3 | **Read and delivery.** The pump issues the read and, on delivery, runs the requester's callback ([file requests and the read queue](file-requests-and-the-read-queue.md)). |   |
| 4 | **Registration.** A loader registers the data as a source in the render resource bank; two sources with the same tag and name share one bank entry, the first registered winning ([resource ownership and disposal](resource-ownership-and-disposal.md#the-four-loaders-that-register-sources), [resource ownership and disposal](resource-ownership-and-disposal.md#the-render-resource-bank)). |   |
| 5 | **Use.** Effect contexts and views borrow the source in place ([resource ownership and disposal](resource-ownership-and-disposal.md#effect-contexts), [resource ownership and disposal](resource-ownership-and-disposal.md#borrowed-views)). |   |
| 6 | **Move.** Compaction can move a movable block. Its handle keeps its value and resolves to the new address, while a raw pointer a consumer kept still points at the old one ([resource arena and relocation](resource-arena-and-relocation.md#the-mover)). |   |

   An effect that borrows the source is repaired against the new address when a cue of one of its instances is next
   started (`0x003B3C00` runs `0x003B3480` before `0x0024FE70`)
   ([resource ownership and disposal](resource-ownership-and-disposal.md#after-a-source-moves)).
| Step | What happens | Where in the code |
|---|---|---|
| 7 | **Disposal.** `0x0041E490` detaches the source in a fixed order: the render records that point at it are cleared, the entry's effect ticket is cancelled with its contexts and instances, and the bank entry is reset and removed ([resource ownership and disposal](resource-ownership-and-disposal.md#disposal-order)). |   |
| 8 | **Free.** The block's owner frees it; a block whose header lacks the magic ends the game with a dump ([resource arena and relocation](resource-arena-and-relocation.md#blocks)). | `0x00369860` |

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

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 81 calls with 16 other topics</summary>

**Characters and objects** (explained on [frame update order](../Engine-Core/frame-update-order.md), [zone changes and mapjump](../World-Areas-And-Travel/zone-changes-and-mapjump.md), [ps2data bin families](ps2data-bin-families.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0032E400`](../Graphics/effect-file-list.md) (on effect file list) | is called by | [`0x0032FCA0`](../EBP-Script-Files/ebp-script-container.md) Actor resource: begin manager resource set load (on ebp script container)<br>[`0x00330310`](../EBP-Script-Files/ebp-script-container.md) Actor resource: begin primary payload load (on ebp script container)<br>[`0x003306E0`](../EBP-Script-Files/atel-debug-companions.md) (on atel debug companions) |
| [`0x0032E620`](../Graphics/effect-file-list.md) (on effect file list) | is called by | [`0x0032FCA0`](../EBP-Script-Files/ebp-script-container.md) Actor resource: begin manager resource set load (on ebp script container)<br>[`0x00330310`](../EBP-Script-Files/ebp-script-container.md) Actor resource: begin primary payload load (on ebp script container) |
| [`0x0036A100`](resource-lifecycle.md) | is called by | [`0x00330310`](../EBP-Script-Files/ebp-script-container.md) Actor resource: begin primary payload load (on ebp script container)<br>[`0x003306E0`](../EBP-Script-Files/atel-debug-companions.md) (on atel debug companions) |

**Controls and input** (explained on [startup constants](../Engine-Core/startup-constants.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0032E620`](../Graphics/effect-file-list.md) (on effect file list) | is called by | [`0x00291C80`](../Graphics/effect-file-list.md) (on effect file list) |

**Graphics** (explained on [standard file formats](standard-file-formats.md), [file requests and the read queue](file-requests-and-the-read-queue.md), [ebp camera tables](../EBP-Script-Files/ebp-camera-tables.md), [character render records](../Graphics/character-render-records.md), [effect files efx efb](../Graphics/effect-files-efx-efb.md), [animation driven movement](../Movement-And-Pathfinding/animation-driven-movement.md), [authored presentation commands](../Graphics/authored-presentation-commands.md), [startup constants](../Engine-Core/startup-constants.md), [effect element types](../Graphics/effect-element-types.md), [effect file list](../Graphics/effect-file-list.md), [effect element runtime](../Graphics/effect-element-runtime.md), [bone trails](../Graphics/bone-trails.md), [character effects](../Graphics/character-effects.md), [effect anchors and targets](../Graphics/effect-anchors-and-targets.md), [resource ownership and disposal](resource-ownership-and-disposal.md), [frame update order](../Engine-Core/frame-update-order.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0032E400`](../Graphics/effect-file-list.md) (on effect file list) | is called by | [`0x003B2310`](../Graphics/effect-file-list.md) (on effect file list)<br>[`0x003B53C0`](small-bin-tables.md) (on small bin tables) |
| [`0x0032E620`](../Graphics/effect-file-list.md) (on effect file list) | is called by | [`0x003B2310`](../Graphics/effect-file-list.md) (on effect file list)<br>[`0x003B53C0`](small-bin-tables.md) (on small bin tables) |
| [`0x0036A100`](resource-lifecycle.md) | is called by | [`0x002561C0`](../EBP-Script-Files/ebp-camera-tables.md) (on ebp camera tables)<br>[`0x003325D0`](../Graphics/character-render-records.md) (on character render records)<br>[`0x003A7BE0`](resource-lifecycle.md)<br>[`0x003A9790`](resource-lifecycle.md)<br>[`0x003A9AD0`](resource-lifecycle.md)<br>[`0x003A9EF0`](../Graphics/effect-files-efx-efb.md) (on effect files efx efb)<br>[`0x003AA470`](../Graphics/effect-files-efx-efb.md) (on effect files efx efb)<br>[`0x003AF2B0`](../Movement-And-Pathfinding/animation-driven-movement.md) (on animation driven movement)<br>[`0x003B6890`](../Graphics/authored-presentation-commands.md) (on authored presentation commands)<br>[`0x003EDAD0`](../Graphics/effect-files-efx-efb.md) (on effect files efx efb)<br>[`0x00436D00`](../Graphics/effect-element-types.md) (on effect element types)<br>[`0x00500C00`](../Graphics/effect-file-list.md) (on effect file list) |
| [`0x0036A100`](resource-lifecycle.md) | is also called by | [`0x00501520`](resource-lifecycle.md)<br>[`0x00501750`](../Graphics/effect-files-efx-efb.md) (on effect files efx efb)<br>[`0x00502CB0`](../Graphics/effect-element-types.md) (on effect element types)<br>[`0x005032D0`](../Graphics/effect-files-efx-efb.md) (on effect files efx efb)<br>[`0x00503880`](../Graphics/effect-element-types.md) (on effect element types)<br>[`0x00503BA0`](resource-lifecycle.md)<br>[`0x00503CD0`](../Graphics/effect-files-efx-efb.md) (on effect files efx efb)<br>[`0x00503E30`](resource-lifecycle.md)<br>[`0x00504060`](../Graphics/effect-file-list.md) (on effect file list)<br>[`0x00504230`](resource-lifecycle.md)<br>[`0x00504350`](resource-lifecycle.md)<br>[`0x005043F0`](resource-lifecycle.md) |
| [`0x0036A100`](resource-lifecycle.md) | is also called by | [`0x0051C270`](../Graphics/bone-trails.md) (on bone trails)<br>[`0x005211F0`](resource-lifecycle.md) |
| [`0x0036A190`](resource-lifecycle.md) | is called by | [`0x003A7460`](../Graphics/effect-element-runtime.md) (on effect element runtime)<br>[`0x003A78A0`](resource-lifecycle.md)<br>[`0x003A8020`](../Graphics/effect-element-runtime.md) (on effect element runtime)<br>[`0x003A9100`](resource-lifecycle.md)<br>[`0x003A9C10`](resource-lifecycle.md)<br>[`0x0044A620`](../Graphics/effect-element-types.md) (on effect element types)<br>[`0x0045FD50`](../Graphics/effect-element-types.md) (on effect element types)<br>[`0x0046F380`](resource-lifecycle.md)<br>[`0x004FF440`](../Graphics/effect-element-runtime.md) (on effect element runtime)<br>[`0x00504350`](resource-lifecycle.md)<br>[`0x00524800`](../Graphics/effect-element-runtime.md) (on effect element runtime)<br>[`0x00525D50`](../Graphics/effect-element-types.md) (on effect element types) |
| [`0x0036A190`](resource-lifecycle.md) | is also called by | [`0x00529200`](../Graphics/effect-element-types.md) (on effect element types)<br>[`0x0052A130`](../Graphics/effect-element-types.md) (on effect element types)<br>[`0x0052ADF0`](resource-lifecycle.md)<br>[`0x0052D3B0`](../Graphics/effect-element-types.md) (on effect element types)<br>[`0x0052E430`](resource-lifecycle.md) |
| [`0x003B37E0`](../Graphics/character-effects.md) (on character effects) | calls | [`0x0024F410`](resource-ownership-and-disposal.md) (on resource ownership and disposal)<br>[`0x0024F4D0`](../Graphics/character-effects.md) (on character effects)<br>[`0x003B39E0`](../Graphics/character-effects.md) (on character effects) |
| [`0x0041E490`](resource-lifecycle.md) | is called by | [`0x002E65A0`](../Scripts-And-Script-Commands/script-binding-lifecycle.md) (on script binding lifecycle) |

**Saving, loading and settings** (explained on [file requests and the read queue](file-requests-and-the-read-queue.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0032E620`](../Graphics/effect-file-list.md) (on effect file list) | is called by | [`0x002EF300`](../Saving-Loading-And-Settings/save-file-format.md) (on save file format) |

**Scripts and script commands** (explained on [file requests and the read queue](file-requests-and-the-read-queue.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0032E400`](../Graphics/effect-file-list.md) (on effect file list) | is called by | [`0x0050DF70`](resource-lifecycle.md) |
| [`0x0032E620`](../Graphics/effect-file-list.md) (on effect file list) | is called by | [`0x0050DFE0`](file-requests-and-the-read-queue.md) (on file requests and the read queue) |
| [`0x0036A100`](resource-lifecycle.md) | is called by | [`0x0050D8F0`](resource-lifecycle.md) |

**World, areas and travel** (explained on [ps2data bin families](ps2data-bin-families.md), [frame update order](../Engine-Core/frame-update-order.md), [resource arena and relocation](resource-arena-and-relocation.md), [standard file formats](standard-file-formats.md), [item and ability ids](../Engine-Core/item-and-ability-ids.md), [async load manager](async-load-manager.md), [graphics settings](../Engine-Core/graphics-settings.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0032E400`](../Graphics/effect-file-list.md) (on effect file list) | is called by | [`0x00378540`](../World-Areas-And-Travel/area-flags-navimapdata.md) (on area flags navimapdata) |
| [`0x0032E620`](../Graphics/effect-file-list.md) (on effect file list) | is called by | [`0x00378540`](../World-Areas-And-Travel/area-flags-navimapdata.md) (on area flags navimapdata) |
| [`0x0036A190`](resource-lifecycle.md) | is called by | [`0x00378540`](../World-Areas-And-Travel/area-flags-navimapdata.md) (on area flags navimapdata) |
| [`0x0032E400`](../Graphics/effect-file-list.md) (on effect file list) | is called by | [`0x00268750`](ps2data-bin-families.md) Map ref: begin load resources (on ps2data bin families)<br>[`0x003319D0`](../World-Areas-And-Travel/zone-changes-and-mapjump.md) (on zone changes and mapjump)<br>[`0x00378030`](../World-Areas-And-Travel/mpk-map-pack.md) (on mpk map pack)<br>[`0x00379A10`](../World-Areas-And-Travel/zone-asset-list.md) (on zone asset list)<br>[`0x003EA820`](ard-area-battle-data.md) Area ard: load or unload field resource (on ard area battle data) |
| [`0x0032E620`](../Graphics/effect-file-list.md) (on effect file list) | is called by | [`0x00268750`](ps2data-bin-families.md) Map ref: begin load resources (on ps2data bin families)<br>[`0x00378030`](../World-Areas-And-Travel/mpk-map-pack.md) (on mpk map pack)<br>[`0x003EA820`](ard-area-battle-data.md) Area ard: load or unload field resource (on ard area battle data) |
| [`0x0036A100`](resource-lifecycle.md) | is called by | [`0x00267930`](../Compiler-And-C-Runtime/memory-and-allocation.md) (on memory and allocation)<br>[`0x003319D0`](../World-Areas-And-Travel/zone-changes-and-mapjump.md) (on zone changes and mapjump)<br>[`0x003EA820`](ard-area-battle-data.md) Area ard: load or unload field resource (on ard area battle data) |
| [`0x0036A190`](resource-lifecycle.md) | is called by | [`0x00268750`](ps2data-bin-families.md) Map ref: begin load resources (on ps2data bin families)<br>[`0x00377DC0`](../Graphics/effect-files-efx-efb.md) (on effect files efx efb)<br>[`0x00378030`](../World-Areas-And-Travel/mpk-map-pack.md) (on mpk map pack)<br>[`0x00378BC0`](../World-Areas-And-Travel/mpk-map-pack.md) (on mpk map pack) |

</details>

---

[← File requests and the read queue](file-requests-and-the-read-queue.md)
