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

The table holds 889 types in 25 categories. The largest is `SaveImage` (0x56690 bytes).

| Category | Types |
|---|---|
| Battle actions | 10 |
| Characters and objects | 28 |
| Compiler and C runtime | 6 |
| Controls and input | 12 |
| Damage and battle formulas | 6 |
| Enemy AI and gambits | 4 |
| Enemy spawning | 11 |
| Engine core | 77 |
| Game files and data tables | 25 |
| Graphics | 91 |
| Items, equipment, shops and licenses | 4 |
| Menus and HUD | 111 |
| Movement and pathfinding | 20 |
| Party | 9 |
| PhyreEngine | 352 |
| Random numbers | 7 |
| Rewards: EXP, LP, gil and loot | 10 |
| Saving, loading and settings | 12 |
| Scripts and script commands | 12 |
| Sound and music | 17 |
| Status effects and KO | 1 |
| Steam and achievements | 8 |
| Story, events and hunts | 2 |
| Third-party libraries | 27 |
| World, areas and travel | 27 |

## Columns

| Column | Meaning |
|---|---|
| `type` | the type's name in this database; a name ending in an address is a static at that address |
| `size` | the type's size in bytes, or how it varies for a type whose size depends on its contents |
| `category` | the engine area the type belongs to; its owner page can sit in another one |
| `purpose` | what the type is for, with the code that uses it |
| `owner_page` | the page that documents the type |
| `lifetime` | where the type's storage lives, what creates or fills it and what releases it |

[engine-types-fields.tsv](engine-types-fields.tsv) gives the fields of 883 of the 889 types, 9,472 rows, one per
field. A type is listed there with every one of its fields; the other 6 types are in [`engine-types.tsv`](engine-types.tsv) only.

| Column | Meaning |
|---|---|
| `type` | the type, as named in [`engine-types.tsv`](engine-types.tsv) |
| `offset` | the field's byte offset in the type |
| `size` | the field's size in bytes |
| `name` | the field's name in this database |
| `ctype` | the field's C type |
| `meaning` | what the field holds, with the code that writes or reads it |

## Data

[engine-types.tsv](engine-types.tsv)

[engine-types-fields.tsv](engine-types-fields.tsv)

## Related

- [Class hierarchy](class-hierarchy.md): the RTTI-named classes and their vtables.
- [Vtable methods](vtable-methods.md): every virtual slot with its class.
