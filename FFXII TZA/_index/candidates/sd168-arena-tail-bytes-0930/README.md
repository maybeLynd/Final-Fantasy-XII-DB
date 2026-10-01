# SD-168: the extra `count` bytes are allocation slack the arena never addresses (OPUS, 2026-09-30)

Register row SD-168 was registered by SWE2-DATA ([where-the-games-memory-comes-from.md](../../../24-Compiler-And-CRT-Runtime/Memory-And-Allocation/where-the-games-memory-comes-from.md)
section 2). It asks what the extra `count` bytes of each arena's boot allocation (`size + count`, tails `0x10` /
`0x100` / `0x400`) serve.

This record is static. The checker is `sd168_tail.py` (output `sd168_tail.out`, `FAILS 0`).

## The answer (OPUS)

- **T1: the allocation.** The boot routine `0022A0B0` allocates each arena's backing through `0036D240` (a thin wrapper
  that jumps to `0085E730`) with exactly **size + count** bytes, the count being the arena's handle count. All nine
  boot arenas match their initializer arguments:

  | size | count | backing |
  |---|---|---|
  | `0x1DC0000` | `0x10` | `0x1DC0010` |
  | `0xD20000` | `0x100` | `0xD20100` |
  | `0x100000` | `0x10` | `0x100010` |
  | `0x1C0000` | `0x100` | `0x1C0100` |
  | `0x6C00000` | `0x400` | `0x6C00400` |
  | `0x3000000` | `0x100` | `0x3000100` |
  | `0x2000000` | `0x100` | `0x2000100` |
  | `0x1200000` | `0x10` | `0x1200010` |
  | `0x400000` | `0x100` | `0x400100` |

- **T2: the initializer carves everything from inside `size`.** `00369D30(arena, backing, size, count)` lays out, from
  the backing's start:
  - a 0x40 header;
  - the bitmap (`+0x20`) and the table (`+0x28`);
  - **the handle slots, `count` × 16 bytes** (`+0x30` / `+0x40` … `+0x38`);
  - the data region (`+0x10`), whose usable length is `size − (data start − base)`, rounded down to 64 (`+0x5C`).

  So no arena structure reaches past `base + size`. The trailing `count` bytes are **not** the handle table: that
  table is 16 × `count` bytes and sits inside `size`.

**Reading:** the `+ count` tail is slack, one byte per handle slot, which the arena itself never addresses. A formula
carried from a layout where the handle table was `count` bytes would explain it. That explanation is an inference and
not claimed.

## Limits (OPUS)

- **Outside the arena.** Only the arena's own code is shown not to address the tail. A foreign pointer into
  `base + size` … `+ count` is not excluded by a census.
- **The system allocator** (`0085E730`) and its page rounding are not read. The tail may be absorbed by page
  granularity in any case.
- **Static only.**

**Review:** routed to SWE2-AUDIT-SPEC (OPUS production → FABLE-side review). The register row belongs to SWE2-DATA's page.
