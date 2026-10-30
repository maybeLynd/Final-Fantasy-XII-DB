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

The table holds 878 types in 25 categories. The largest is `SaveImage` (0x56690 bytes).

| Category | Types |
|---|---|
| Battle actions | 10 |
| Characters and objects | 27 |
| Compiler and C runtime | 5 |
| Controls and input | 12 |
| Damage and battle formulas | 6 |
| Enemy AI and gambits | 4 |
| Enemy spawning | 11 |
| Engine core | 74 |
| Game files and data tables | 25 |
| Graphics | 90 |
| Items, equipment, shops and licenses | 4 |
| Menus and HUD | 111 |
| Movement and pathfinding | 20 |
| Party | 9 |
| PhyreEngine | 352 |
| Random numbers | 6 |
| Rewards: EXP, LP, gil and loot | 9 |
| Saving, loading and settings | 12 |
| Scripts and script commands | 12 |
| Sound and music | 17 |
| Status effects and KO | 1 |
| Steam and achievements | 8 |
| Story, events and hunts | 2 |
| Third-party libraries | 27 |
| World, areas and travel | 24 |

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
