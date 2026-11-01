---
title: "Global state accessors: every one-instruction getter of a global, with its global, width and callers"
kind: "reference"
category: "Engine core"
addresses: "0x0020E600, 0x0020E620, 0x00189120, 0x002640C0, 0x006372A0, 0x003590D0, 0x001B1C00, 0x00796E20, 0x001A9930, 0x0018CA40, 0x00198790, 0x002EF640, 0x00236850, 0x001EDE70, 0x001EDDA0, 0x001EDEC0, 0x00229E70, 0x00229EA0"
---

## What it lists

One row per function whose body is a single load or `lea` of one global through a rip-relative
operand and a `ret`, with at most one instruction between them that uses only the loaded register: a step
such as `and eax, 1` or `or rax, 1`, or one load through it. Of the executable's 39,108 functions, 454 are
such accessors, 313 reads and 141 address takes:

- 257 return the global's value, 48 a field of the object the global points to, and 8 the value after one
  step on the register (`and eax, 1` in five of them).
- 118 return the global's address, and 23 the address with bit `0x1` set (`or rax, 1`).

Five functions of the same shape write through the global's pointer instead of reading, and are not
listed: `0x00255040`, `0x00290610`, `0x00290C50`, `0x002B4700` and `0x002CA5C0`. Each row gives the functions
that call the accessor or tail-jump to it, directly or through a jump thunk, and the places that hold its
address instead of calling it.

The engine reaches most of its singletons this way. The heaviest getters, with the names the
other pages establish for their globals:

| Accessor | Global | Callers | What the global is |
|---|---|---|---|
| `0x006372A0` | `0x02CF8270` (address) | 248 | the root of the PhyreEngine class-descriptor registry (also reached through the thunk `0x006C4460`, slot 9 of the `PClassDataMemberPhyreArray<PBase *>` virtual table) |
| `0x002640C0` | `0x02099D70` | 138 | the pointer the binder publishes to actor manager 0 ([frame update order](frame-update-order.md)) |
| `0x00189120` | `0x01F7F598` | 117 | the render manager object ([game application](game-application.md)) |
| `0x003590D0` | `0x022C7FE0` (u32) | 80 | the party-focus actor's packed handle |
| `0x001B1C00` | `0x01F811E8` | 56 | the immediate-mode batcher singleton |
| `0x00796E20` | `0x02EA5368` | 55 | the PhyreEngine application object |
| `0x001A9930` | `0x01F81168` | 47 | the map-art context, whose keys and setters [graphics settings](graphics-settings.md) describes |
| `0x0018CA40` | `0x01F7F5E8` | 46 | the render command vector |
| `0x00198790` | `0x01F7FFE0` | 46 | the input manager singleton pointer |
| `0x002EF640` | `0x02164280` (address) | 28 | the save runtime buffer ([saving and loading](../Saving-Loading-And-Settings/saving-and-loading.md)) |
| `0x00236850` | `0x0208E6A0` (u32) | 27 | the battle unit slot count ([battle units](../Characters-And-Objects/battle-units.md)) |
| `0x001DDAB0` | `0x01F82D18` | 26 | the display settings object ([debug menu](debug-menu.md)) |
| `0x0016D670` | `0x02EBA3D0` (address) | 23 | the C runtime `printf` options ([debug logging](debug-logging.md)) |
| `0x00229EA0` | `0x02064AD3` (s8) | 22 | the frame-mode byte ([startup constants](startup-constants.md)) |
| `0x001EDE70` | `0x01F82E38` (u32) | 22 | the 60 fps gate that `0x001EDDC0` sets from FrameLimit ([game settings](../Saving-Loading-And-Settings/game-settings.md)) |

Two helpers that are three instructions rather than one carry more traffic than any getter.
`0x0020E600(u)` returns `u + [0x01F83530]` with `u` zero-extended from 32 bits, and `0x0020E620(p)`
returns the low 32 bits of `p - [0x01F83530]`: a pointer is stored as a 32-bit offset from the base
and recovered by adding it back. `0x0020E600` has 815 callers and `0x0020E620` 279; the base
`0x01F83530` is zero in the image and has no writer, so in this build the offset is the pointer's
low 32 bits.

Three accessors beside them are two-global predicates rather than loads: `0x001EDDA0` returns 0
only when `0x01DFE0C0` is 0 and `0x01F82E38` is not; `0x001EDEC0(x)` returns 1 when `0x01F82E38` is 0 or
`0x01DFE0C0` is set and `~x & 1` otherwise; `0x00229E70` returns the step accumulator `0x01E02820` as it stood at the top of the pass ([frame update order](frame-update-order.md)),
first storing 1.0 into it when it is 0 or below.

## Columns

| Column | Meaning |
|---|---|
| `accessor` | the function's entry address |
| `global` | the address the instruction loads from or takes |
| `width` | bytes read: 1, 2, 4 or 8; 0 for an address take (`lea`) |
| `kind` | `read` or `address` |
| `instruction` | the first instruction as disassembled |
| `follow_up` | the one instruction between the load and the `ret`, if any: a step on the loaded register, or a load through it |
| `callers` | distinct functions that call the accessor or tail-jump to it, directly or through a jump thunk (a function whose whole body is one jump to it; the thunk's callers count) |
| `address_refs` | places that hold the accessor's address instead of calling it: instructions that form it (`lea` from `rip`, a 64-bit immediate) and eight-byte data cells in the image |

## Related

- [Game application](game-application.md): the singletons the application sets up at boot.
- [Jump thunks](jump-thunks.md): the other one-instruction function family.
- [Debug logging](debug-logging.md): the options word accessor and the log sink.
