# RC-2: the extra bytes past each boot arena are one byte per handle slot, outside the arena (OPUS, 2026-09-30)

Input for `RC-2` ([what the engine fixes at boot](../../../00-Engine-Core-Runtime/what-the-engine-fixes-at-boot.md), the
memory budget). SWE2-CONTRACT registered the row, so it applies this. Static evidence only (shipping image `73461d08…`).
EXP-142's executed observation, that the tail keeps the fixture fill, is the isolated-execution side and is carried.

## The sizes: allocation = registered size + slot count

`0022A0B0` allocates each block with `0036D240(size)`, then registers it with `00369D30(id, block, size, slots)`:

| allocation (`0022A1DC`..`0022A262`) | registration (`0022A290`..`0022A394`) | extra |
|---|---|---:|
| `0x1DC0010` | size `0x1DC0000`, slots `0x10` | `0x10` |
| `0xD20100` | `0xD20000`, `0x100` | `0x100` |
| `0x100010` | `0x100000`, `0x10` | `0x10` |
| `0x1C0100` | `0x1C0000`, `0x100` | `0x100` |
| `0x6C00400` | `0x6C00000`, `0x400` | `0x400` |
| `0x3000100` | `0x3000000`, `0x100` | `0x100` |
| `0x2000100` | `0x2000000`, `0x100` | `0x100` |
| `0x1200010` | `0x1200000`, `0x10` | `0x10` |
| `0x400100` | `0x400000`, `0x100` | `0x100` |

In every case the extra is exactly the arena's handle-slot count: one byte per slot. The two unregistered blocks
(`0x80000`, `0x100000`) have none; they are RC-3.

## The registrar builds everything inside the registered size

`00369D30(id, base, size, slots)` lays out the arena from the block's **start**:

1. It zeroes a 64-byte header at `base` (`00369E4C`–`00369E67`).
2. It places two bitmaps at `align64(base + 0x7F)` (`+0x20`) and after it (`+0x28`). Their sizes come from the page
   count `ceil(size / 0x10000)`, rounded up to 32 (`00369DDF`–`00369E23`).
3. It places the handle-slot table at `+0x30`/`+0x40`: **`slots × 16` bytes** (`00369EB7 shl rax, 4`). Each 16-byte
   slot is initialised as a linked record: next and previous words, the arena id at `+4`, 0 at `+5`, and 0 at `+8`
   (`00369EE5`–`00369F33`).
4. It puts the heap start at the 64-aligned end of that table (`+0x10`, `+0x90`, `+0x98`). The heap size at `+0x5C` is
   `align64down(low32(base) + size − heapStart)` (`00369F5D`–`00369F88`). **Only `size`** bounds it, not the allocation.

No field the registrar writes addresses anything past `base + size`. The `slots` bytes the boot code adds therefore lie
beyond the heap end, outside every structure the arena defines. The handle slots themselves are 16 bytes each and sit at
the front, inside the registered size.

So what the extra bytes are for: nothing the arena uses. They are slack, one byte per handle slot, past the arena's
end. That agrees with EXP-142, where no boot step writes them.

## Not claimed

- Why the sizing adds `slots` bytes. One reading is a one-byte-per-slot table that was later moved into the 16-byte
  slots at the front; another is a mis-scaled `slots × 16`. Both are readings, not findings.
- That no allocator path outside `00369D30` ever reads past `base + size`. The arena record's bounds all derive from
  `size`, and a census of the allocator's reads is the next step if anyone needs the stronger form.
