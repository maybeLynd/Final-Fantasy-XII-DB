[Home](../../README.md) / [Story, events and hunts](README.md) / Event memory

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Event memory: the event and summon memory heaps a field gets when its actors are bound, and the list of fields that get no event memory | system | Story, events and hunts | Scripts across all areas | What happens to two working heaps when a field's actor manager is bound: both are released, the 1 MiB event memory heap EVTMEM is made again unless the field's id is in eventmemorylist.bin, and the 100 KiB summon memory heap SMNMEM is made again unless the field record's bit `0x8000` is set, with the list's file format, its loader and its eight shipped ids. | 0x0026C8C0, 0x00377440, 0x00377480, 0x0025A990, 0x0025AA30, 0x02ADD0A8 |

## What the player sees

Nothing directly: these are working memory for the actors of events and summons. The two are decided separately:
a field on the event memory list loads its event actors from the general memory, and a field marked as a town
loads its summon actor from there. A field that is both, or neither, follows each rule on its own.

## How it works

### At actor bind

`ActorManager_BindLoadedDefinitionPayload` (`0x0026C8C0`) binds the payload of any of the five actor manager slots.
Only when slot 0, the field, is bound (`0x0026C95D`-`0x0026C95F`) does it handle two heaps whose pointers are
`0x02099DD0` and `0x02099DD8` (`0x0026C9B5`-`0x0026CA39`):

1. It takes the id registered for slot 0, `0x0032F240(0)`, the id the field was loaded by: the slot loader
   `0x0032FCA0` stores it (`0x0032FD09`) and requests the field's own files by it (`0x0032FD3F`) (`0x0026C9B7`).
2. It releases each heap that exists: heap 13 at `0x02099DD0` and heap 14 at `0x02099DD8`, through `0x00369760`,
   `0x0036D160` and `0x003697F0` (`0x0026C9BC`-`0x0026CA17`).
3. When `0x00377440(id)` reports the id absent from the event memory list, `0x0025A990` makes heap 13 again
   (`0x0026CA1E`-`0x0026CA29`).
4. When `0x00377480(id)` returns 0, `0x0025AA30` makes heap 14 again (`0x0026CA2E`-`0x0026CA39`).

### The two heaps

| Heap | Pointer | Size | Name | Made by |
|---|---|---|---|---|
| 13 | `0x02099DD0` | `0x100000`, 1 MiB | `EVTMEM` | `0x0025A990` (`0x0025A9D5`-`0x0025AA21`) |
| 14 | `0x02099DD8` | `0x19000`, 100 KiB | `SMNMEM` | `0x0025AA30` |

Each maker releases an existing heap first, through `0x00369760(heap)`, `0x0036D160(heap)` and `0x003697F0(block)`, and
sets its pointer to 0 (`0x0025A99E`-`0x0025A9BE`, `0x0025AA3E`-`0x0025AA5E`). It then allocates the block from pool 5
(`0x0036C1D0(5, 5)`, `0x0036A190`), stores the result in the pointer even when it is null, and pops the pool selection
(`0x0036C140`). Only a block that is not null is named (`0x0036C660`) and registered under its heap number with
`0x00369D30(heap, block, size, 0)`, a tail jump (`0x0025A9F2`-`0x0025AA21`, `0x0025AA92`-`0x0025AAC1`).

The slot reset `0x002628B0` releases both heaps the same way when slot 0 is reset (`0x00262DC3`-`0x00262DC5`,
`0x00262DD3`-`0x00262E28`).

The slot loaders take the payloads of slots 1 and 2 from heap 13 and the payload of slot 3 from heap 14 when those
heaps exist, and from pool 5 otherwise (`0x0032F8F6`-`0x0032F96B`, `0x0032FE00`-`0x0032FE40`). So a field on the list
loads slots 1 and 2 from the general pool, and a town loads slot 3 from it. A heap is also absent when its block
cannot be had: `0x0036A190` returns 0 when both of its tries fail (`0x0036A1C9`, `0x0036A1F0`, `0x0036A1FB`), and
`0x0025A990` then leaves heap 13 unmade (`0x0025A9F2`-`0x0025A9F5`).

### The two tests

`0x00377440(id)` reads the list at `0x02ADD0A8`: no list, an empty list or an id not in it all count as absent
(`0x00377440`-`0x0037747A`). It compares the id with each `u16` entry from `+0x0A`, up to the `u16` count at `+0x08`,
and returns 1 for absent (`0x00377475`) and 0 when an entry matches (`0x0037747B`).

`0x00377480(id)` returns bit `0x8000` of the id's record in the field record table `0x02ADD100`,
the town bit ([Area flags](../World-Areas-And-Travel/area-flags-navimapdata.md)), and 0 for an id outside the table
(the unsigned compare with the count at `+4`, `0x0037748C`) or while the table is not loaded (`0x0037748A`).
So the summon memory heap is made only for fields that are not towns, and for every field while the table is
not loaded.

### The list file

The list is `common/eventmemorylist.bin`, kind 9 file `0x29`, requested by `0x00378540` under the name `EVTMEM`
(`0x003787E6`-`0x00378841`); its completion `0x00378A50` stores the pointer in `0x02ADD0A8`.

The buffer comes from `0x00267990(size)` (`0x003787FB`), which allocates the file's size in arena 5 (`0x0036C1D0(5)`,
`0x0036A190`) and labels the block with the file name cut from `..\..\katano\ateldecode.c` (`0x0036C750`) and the tag
`0x1698` (`0x0036C660`). `0x00378540` then labels it again with the name `EVTMEM` and tag 0 (`0x00378810`).

## Layouts

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `char[8]` | magic | "EVMEMLST" |
| `+0x08` | `u16` | count | 8 |
| `+0x0A` | `u16[8]` | ids | the field ids that get no event memory |

## Shipped data

The one shipped file is 26 bytes and lists the ids 0, 49, 668, 670, 782, 871, 872 and 912.

## Modding notes

- Adding a field's id to the list frees 1 MiB in that field; an event that needs the event memory heap there will
  have no event memory heap.
- Marking a field as a town also drops its summon memory heap.

## Related

- [Area flags](../World-Areas-And-Travel/area-flags-navimapdata.md) - the field record table and its town bit.
