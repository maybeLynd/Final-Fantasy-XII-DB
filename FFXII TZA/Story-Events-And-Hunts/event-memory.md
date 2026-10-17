---
title: "Event memory: the event and summon memory heaps a field gets when its actors are bound, and the list of fields that get no event memory"
kind: "system"
category: "Story, events and hunts"
addresses: "0026C8C0, 00377440, 00377480, 0025A990, 0025AA30, 02ADD0A8"
---

## What the player sees

Nothing directly: these are working memory for the actors of events and summons. A field on the list, or a field
marked as a town, loads them from the general memory instead.

## How it works

### At actor bind

`ActorManager_BindLoadedDefinitionPayload` (`0026C8C0`) binds the payload of any of the five actor manager slots.
Only when slot 0, the field, is bound (`0026C95D`-`0026C95F`) does it handle two heaps whose pointers are
`02099DD0` and `02099DD8` (`0026C9B5`-`0026CA39`):

1. It takes the id registered for slot 0, `0032F240(0)`, the id the field was loaded by: the slot loader
   `0032FCA0` stores it (`0032FD09`) and requests the field's own files by it (`0032FD3F`) (`0026C9B7`).
2. It releases each heap that exists: heap 13 at `02099DD0` and heap 14 at `02099DD8`, through `00369760`,
   `0036D160` and `003697F0` (`0026C9BC`-`0026CA17`).
3. When `00377440(id)` reports the id absent from the event memory list, `0025A990` makes heap 13 again
   (`0026CA1E`-`0026CA29`).
4. When `00377480(id)` returns 0, `0025AA30` makes heap 14 again (`0026CA2E`-`0026CA39`).

### The two heaps

| Heap | Pointer | Size | Name | Made by |
|---|---|---|---|---|
| 13 | `02099DD0` | `100000`<sub>h</sub>, 1 MiB | `EVTMEM` | `0025A990` (`0025A9D5`-`0025AA21`) |
| 14 | `02099DD8` | `19000`<sub>h</sub>, 100 KiB | `SMNMEM` | `0025AA30` |

Each maker releases an existing heap first, allocates the block from pool 5, names it (`0036C660`) and registers
it under its heap number with `00369D30`. The slot reset `002628B0` releases both heaps the same way when slot 0
is reset (`00262DC3`-`00262DC5`, `00262DD3`-`00262E28`).

The slot loaders take the payloads of slots 1 and 2 from heap 13 and the payload of slot 3 from heap 14 when those
heaps exist, and from pool 5 otherwise (`0032F8F6`-`0032F96B`, `0032FE00`-`0032FE40`). So a field on the list, or
a town, loads those slots' actors from the general pool.

### The two tests

`00377440(id)` reads the list at `02ADD0A8`: no list, an empty list or an id not in it all count as absent
(`00377440`-`0037747A`). `00377480(id)` returns bit 15 of the id's record in the field record table `02ADD100`,
the town bit ([Area flags](../World-Areas-And-Travel/area-flags-navimapdata.md)), and 0 for an id outside the table.
So the summon memory heap is made only for fields that are not towns.

### The list file

The list is `common/eventmemorylist.bin`, kind 9 file `29`<sub>h</sub>, requested by `00378540` under the name `EVTMEM`
(`003787E6`-`00378841`); its completion `00378A50` stores the pointer in `02ADD0A8`.

## Layouts

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `char[8]` | magic | "EVMEMLST" |
| `08`<sub>h</sub> | `u16` | count | 8 |
| `0A`<sub>h</sub> | `u16[8]` | ids | the field ids that get no event memory |

## Shipped data

The one shipped file is 26 bytes and lists the ids 0, 49, 668, 670, 782, 871, 872 and 912.

## Modding notes

- Adding a field's id to the list frees 1 MiB in that field; an event that needs the event memory heap there will
  have none.
- Marking a field as a town also drops its summon memory heap.

## Related

- [Area flags](../World-Areas-And-Travel/area-flags-navimapdata.md) - the field record table and its town bit.
