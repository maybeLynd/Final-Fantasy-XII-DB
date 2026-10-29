---
title: "Engine types: every identified engine type with its purpose, its owner page and its lifetime"
kind: "reference"
category: "Engine core"
addresses: ""
---

## What it lists

One row per engine type whose purpose is established: the records, objects, tables and statics the
executable builds and reads. Each row gives what the type is for, the page that documents it (its owner
page) and its lifetime: where its storage lives, which code creates or fills it, and what releases it.
Addresses in a row are the instructions and functions that do so.

The table holds 449 types in 24 categories. The largest is `SaveImage` (0x56690 bytes).

| Category | Types |
|---|---|
| Battle actions | 7 |
| Characters and objects | 23 |
| Controls and input | 12 |
| Damage and battle formulas | 5 |
| Enemy AI and gambits | 3 |
| Enemy spawning | 11 |
| Engine core | 63 |
| Game files and data tables | 19 |
| Graphics | 66 |
| Items, equipment, shops and licenses | 2 |
| Menus and HUD | 96 |
| Movement and pathfinding | 14 |
| Party | 9 |
| PhyreEngine | 34 |
| Random numbers | 5 |
| Rewards: EXP, LP, gil and loot | 9 |
| Saving, loading and settings | 7 |
| Scripts and script commands | 10 |
| Sound and music | 12 |
| Status effects and KO | 1 |
| Steam and achievements | 6 |
| Story, events and hunts | 1 |
| Third-party libraries | 16 |
| World, areas and travel | 18 |

## Columns

| Column | Meaning |
|---|---|
| `type` | the type's name in this database; a name ending in an address is a static at that address |
| `size` | the type's size in bytes, or how it varies for a type whose size depends on its contents |
| `category` | the engine area the type belongs to; its owner page can sit in another one |
| `purpose` | what the type is for, with the code that uses it |
| `owner_page` | the page that documents the type |
| `lifetime` | where the type's storage lives, what creates or fills it and what releases it |

## Data

[engine-types.tsv](engine-types.tsv)

## Related

- [Class hierarchy](class-hierarchy.md): the RTTI-named classes and their vtables.
- [Vtable methods](vtable-methods.md): every virtual slot with its class.
