# `Phyre::PUtility`, the module registry node (OPUS, 2026-09-28)

**Question.** The page on [the fifteen modules registered before `main`](../../../22-Middleware-PhyreEngine/Subsystem-Map/the-fifteen-modules-registered-before-main.md)
holds FABLE's answers of 2026-09-14 about the module objects on the chain at `02CACC90`. The type store had no row for
their shared base. What is its extent and layout?

**Answer.** [`putility.py`](putility.py) ([output](putility.out)), static on the certified image: FAILS 0. W failed
before the patch. Every fact is re-read from the bytes; none is taken from the page.

- **I: the image.** All fourteen `.data` module objects begin `{vtable 00D26BC0, next 0, a pointer to the module's name
  string, dword 0xFF, dword 0}`. The fourteen names read correctly, `Serialization` through `DeveloperExtensions`.
- **Z: the size is 0x20.**
  - Slot 0 of the base vtable is `005A0CB0`, the scalar deleting destructor. It re-stamps `00D26BC0`, unlinks `this`
    from `02CACC90`, and for flags bit 0 frees with an explicit size of **0x20** (`005A0D01`, `005A0D06`).
  - Two pairs of module objects sit exactly 0x20 apart (`01F2EE60`/`01F2EE80` and `01F47550`/`01F47570`).
- **C: construction and teardown.**
  - Each of the fourteen registrars links its object into the chain, installs the derived vtable, and tail-jumps
    `atexit` with its paired teardown in `rcx`.
  - Each teardown re-stamps `00D26BC0` and unlinks the object.
  - PText's object at `02E5BE88` (`.bss`) is built by `006CCC10`, called from `00167B90`. That constructor stores key
    0xFF (`006CCC17`) and the name `"Text"`, and `008B6F00` is its teardown.

**The type:**

| offset | field | ctype | |
|---|---|---|---|
| +0x00 | `vtable` | `void*` | `00D26BC0` in the image and after teardown; the derived vtable is installed by the static constructor. Slot 0 is the deleting destructor, slot +0x08 init, slot +0x10 shutdown |
| +0x08 | `next` | `PUtility*` | the chain link from `02CACC90` |
| +0x10 | `moduleName` | `char*` | the module's name string; no reader is established here |
| +0x18 | `orderKey` | `uint32` | 0xFF in every module, so every module splices at the head |
| +0x1C | `unobservedSpan1C` | `u8[4]` | zero in the images; DISCOVERED |

**Not claimed:** what a key below 0xFF would mean; the derived classes' sizes (only two are bounded at 0x20); what reads
`+0x10`.

| consumer | action | agreement |
|---|---|---|
| `_types/types.tsv` / `fields.tsv` | `PUtility` added (1 + 5 rows) with its fifteen static instances | revised-here |
| the fifteen-modules page (§2, §5: node layout, `005A0CB0`, the teardown column, PText) | the same facts, read from the bytes | agrees (no edit needed) |

This is OPUS's own check; independent acceptance is requested separately.
