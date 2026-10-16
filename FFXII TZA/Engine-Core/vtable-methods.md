---
title: "Vtable methods: every virtual slot in the executable with its class and the function it names"
kind: "reference"
category: "Engine core"
addresses: "008C5760, 00D86960, 009007E8, 00D360A0, 005C5230, 0016D6A0, 0016D680"
---

## What it lists

One row per vtable slot: the function the slot holds, the class whose vtable it is, the vtable's
address and the slot index. The vtables are the 2,286 found through their complete object
locators ([class hierarchy](class-hierarchy.md)); a slot is each consecutive `.text` address after
the locator pointer.

The `classes_sharing` column counts the distinct classes whose vtables hold the same function:
4,275 functions have 1 and are that class's methods; 2,611 appear in two or more, through
inheritance or linker folding, and the extreme cases are stubs (`005C5230`, `return 0`, in 2,514
slots; `0016D6A0`, `ret`, in 1,386; `0016D680`, `return this`, in 1,349).

Class names are given twice: `decorated` is the MSVC name as the image spells it
(`.?AVGiVmax@@`, `.?AVPTTYCallback@Phyre@@`), and `class` is the readable form
(`GiVmax`, `Phyre::PTTYCallback`) for names without template arguments; the 1,660 template-class
rows keep only the decorated form, because the image spells their arguments only in that form,
so a grouping by class must use the `decorated` column. A function-local class is written with
its function (`btBvhTriangleMeshShape::performRaycast::MyNodeOverlapCallback`).

## Columns

| Column | Meaning |
|---|---|
| `method` | the function address the slot holds |
| `decorated` | the class's decorated RTTI name |
| `class` | the readable class name, empty for template classes |
| `vtable` | the vtable's address (slot 0) |
| `slot` | the slot index, 0-based; the call is `[[object] + slot × 8]` |
| `classes_sharing` | distinct classes whose vtables hold this function |

## Related

- [Class hierarchy](class-hierarchy.md): how the vtables and names are recovered, and what the classes are.
- [Game application](game-application.md): `GameApplication`'s vtable `008C5760`.
- [Debug logging](debug-logging.md): `Phyre::PTTYCallback`'s two slots at `00D360A0`.
