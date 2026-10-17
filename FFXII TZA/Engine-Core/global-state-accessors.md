---
title: "Global state accessors: every one-instruction getter of a global, with its global, width and callers"
kind: "reference"
category: "Engine core"
addresses: "0020E600, 0020E620, 00189120, 002640C0, 006372A0, 003590D0, 001B1C00, 00796E20, 001A9930, 0018CA40, 00198790, 002EF640, 00236850, 001EDE70, 001EDDA0, 001EDEC0, 00229E70, 00229EA0"
---

## What it lists

One row per function whose body is a single load or `lea` of one global through a rip-relative
operand and a `ret`, with at most a register-only follow-up such as `and eax, 1`. The census walks
every function entry in the executable; 401 qualify, 283 returning the global's value and 118 its
address. The caller count is the number of distinct functions containing a direct `call` to the
accessor; calls through stored pointers, tail jumps and thunks are not counted.

The engine reaches most of its singletons this way. The heaviest getters, with the names the
other pages establish for their globals:

| Accessor | Global | Callers | What the global is |
|---|---|---|---|
| `006372A0` | `02CF8270` (address) | 248 | the root of the PhyreEngine class-descriptor registry (also reached through the thunk `006C4460`, which the count excludes) |
| `002640C0` | `02099D70` | 138 | the pointer the binder publishes to actor manager 0 ([frame update order](frame-update-order.md)) |
| `00189120` | `01F7F598` | 117 | the render manager object ([game application](game-application.md)) |
| `003590D0` | `022C7FE0` (u32) | 78 | the party-focus actor's packed handle |
| `001B1C00` | `01F811E8` | 56 | the immediate-mode batcher singleton |
| `00796E20` | `02EA5368` | 55 | the PhyreEngine application object |
| `001A9930` | `01F81168` | 47 | the map-art context, whose keys and setters [graphics settings](graphics-settings.md) describes |
| `0018CA40` | `01F7F5E8` | 46 | the render command vector |
| `00198790` | `01F7FFE0` | 46 | the input manager singleton pointer |
| `002EF640` | `02164280` (address) | 28 | the save runtime buffer ([saving and loading](../Saving-Loading-And-Settings/saving-and-loading.md)) |
| `00236850` | `0208E6A0` (u32) | 27 | the battle unit slot count ([battle units](../Characters-And-Objects/battle-units.md)) |
| `001DDAB0` | `01F82D18` | 26 | the display settings object ([debug menu](debug-menu.md)) |
| `0016D670` | `02EBA3D0` (address) | 23 | the C runtime `printf` options ([debug logging](debug-logging.md)) |
| `00229EA0` | `02064AD3` (s8) | 22 | the frame-mode byte ([startup constants](startup-constants.md)) |
| `001EDE70` | `01F82E38` (u32) | 22 | the mode flag `00184960` tests against the suppressor `01DFE0C0` ([startup constants](startup-constants.md)) |

Two helpers that are three instructions rather than one carry more traffic than any getter.
`0020E600(u)` returns `u + [01F83530]` with `u` zero-extended from 32 bits, and `0020E620(p)`
returns the low 32 bits of `p - [01F83530]`: a pointer is stored as a 32-bit offset from the base
and recovered by adding it back. `0020E600` has 815 direct callers and `0020E620` 279; the base
`01F83530` is zero in the image and has no writer, so in this build the offset is the pointer's
low 32 bits.

Three accessors beside them are two-global predicates rather than loads: `001EDDA0` returns 0
only when `01DFE0C0` is 0 and `01F82E38` is not; `001EDEC0(x)` returns 1 when `01F82E38` is 0 or
`01DFE0C0` is set and `~x & 1` otherwise; `00229E70` returns the frame-rate float `01E02820`,
first storing 1.0 into it when it is 0 or below.

## Columns

| Column | Meaning |
|---|---|
| `accessor` | the function's entry address |
| `global` | the address the instruction loads from or takes |
| `width` | bytes read: 1, 2, 4 or 8; 0 for an address take (`lea`) |
| `kind` | `read` or `address` |
| `instruction` | the first instruction as disassembled |
| `follow_up` | the register-only instructions between the load and the `ret`, if any |
| `callers` | distinct functions with a direct `call` to the accessor |

## Related

- [Game application](game-application.md): the singletons the application sets up at boot.
- [Jump thunks](jump-thunks.md): the other one-instruction function family.
- [Debug logging](debug-logging.md): the options word accessor and the log sink.
