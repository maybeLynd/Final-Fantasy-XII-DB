---
title: "Vtable methods: every virtual slot in the executable with its class and the function it names"
kind: "reference"
category: "Engine core"
addresses: "0x008C5760, 0x00D86960, 0x009007E8, 0x00D360A0, 0x005C5230, 0x0016D6A0, 0x0016D680"
---

## What it lists

One row per vtable slot: the function the slot holds, the class whose vtable it is, the vtable's
address and the slot index. The vtables are the 2,286 found through their complete object
locators ([class hierarchy](class-hierarchy.md)); a slot is each consecutive qword after the locator pointer
that holds a function entry, and the table ends at the first qword that does not.

Four vtables are followed at once by a short string whose first 8 bytes read as a `.text` address inside a
function, so they are not slots: `LOD` after `Phyre::PLOD::PUtilityLOD` (`0x00D85180`, read as `0x00444F4C`),
`Box` after `btBoxShape` (`0x00D7A918`, read as `0x00786F42`), `m_u` after a `PClassDataMemberArrayDynamic`
(`0x00D337A0`, read as `0x00755F6D`) and `Cel` after a `PClassDescriptorForType` (`0x00D5A248`, read as `0x006C6543`).

The code uses each as a string: `0x006A3B10` returns `0x00D7A918`, `0x00164BE7` passes `0x00D5A248` to `0x005DC6F0`, ten
`lea` instructions load `0x00D337A0`, and the qword at `0x01F2EE90` holds `0x00D85180`.

The function that holds `0x00164BE7` is `0x00164BE0`. It calls `0x005DC6F0(0x02D36E20, 0x00D5A248, 0)` and then
jumps to `0x00808B90` with the address `0x008B03B0` (`0x00164BE4`-`0x00164C05`).

Of the 6,882 functions the slots hold, 5,318 begin a `.pdata` entry, 1,303 are frameless leaves that no
`.pdata` entry covers, and 261 are a single `jmp`; `target_kind` and `target_basis` give each slot's case.

The `classes_sharing` column counts the distinct classes whose vtables hold the same function:
4,271 functions have 1 and are that class's methods; 2,611 appear in two or more, through
inheritance or linker folding, and the extreme cases are stubs (`0x005C5230`, `return 0`, in 2,514
slots; `0x0016D6A0`, `ret`, in 1,386; `0x0016D680`, `return this`, in 1,349).

Class names are given twice: `decorated` is the MSVC name as the image spells it
(`.?AVGiVmax@@`, `.?AVPTTYCallback@Phyre@@`), and `class` is the readable form
(`GiVmax`, `Phyre::PTTYCallback`) for names without template arguments; the 21,859 rows of the 1,660
template classes keep only the decorated form, because the image spells their arguments only in that form,
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
| `target_kind` | `function` when the target begins a `.pdata` entry, `leaf function` when no `.pdata` entry covers it, `jump thunk` when its first instruction is a `jmp` |
| `target_basis` | the `.pdata` entry (`.pdata entry 0x005A0CB0-0x005A0D14`), or `no .pdata entry`; for a thunk also the `jmp` target |

## Related

- [Class hierarchy](class-hierarchy.md): how the vtables and names are recovered, and what the classes are.
- [Game application](game-application.md): `GameApplication`'s vtable `0x008C5760`.
- [Debug logging](debug-logging.md): `Phyre::PTTYCallback`'s two slots at `0x00D360A0`.
