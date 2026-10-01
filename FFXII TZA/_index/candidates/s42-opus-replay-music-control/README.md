# S-42: the music-control file and the BGM stream executed as shipped code over the shipped `musicctrl.bin` (OPUS, 2026-09-25, block 325)

**Evidence class: NATIVE-REPLAY (unicorn), `live_game: false`.** S-42's exposure note (block 301) found MC-1..MC-8 of
`CONTRACT-music-control-file-and-bgm-stream.md` with **no execution at all**; its §13 says "None". It also noted that
EXP-099 plants the table already rebased, i.e. it assumes MC-5's result. This harness runs the MC bodies, and the
field-music reader over the table the shipped rebase produces from the shipped file.

## What was run

`check.py`, with `world.py` / `world.json` / `printf_bridge.py` from block 324. There is no application stub.

**The table is the shipped file.** `ps2data/image/ff12/in/common/musicctrl.bin` (1,615 B, sha256
`771462a2…202dc7`) is copied raw to a block below 2 GB. Its page offsets are still file-relative, the state the
loader's queued read leaves. `[02B5E0D0]` points at it. The rebase is reached the way the queue's completion reaches
it: through the trampoline `0051EDB0`, with the descriptor's `+8` word `0x003EAB90`.

**Other fixtures** (planted data only):
- the progress operand `00265270` returns: the u16 behind `[02098E58]`, enabled by `[02098E20]` bit 0;
- the kind-`0x24` size table behind `[022C51F0 + 0x24*8]`. The shipped build has no kind-`0x24` files, and the size
  tables load from FST files at boot.

**The request queue runs as shipped**, after its own initialiser `0032EA90`, which also runs `003EB050` and sets the
descriptor. That covers `0032E400`, `0032E780` / `0032E870` and `0032E4D0`.

**Stop boundaries** (the run ends there and the arguments are recorded; nothing is substituted): the sound layer
`002DF660`, `002DEE90`, `002DF680`, `002DF630` and `002DF690`.

**9 / 9 pass, and `result.json` is byte-identical over three runs** (md5 `0da240672601cfc739c7bf9b75d3b407`).

| case | contract item | observed |
|---|---|---|
| `MC4_MC5_trampoline_then_rebase` | MC-4, MC-5 | `0051EDB0(0x003EAB90)` enters the rebase. The **11 page words** (max field 1311, `(1311 + 0x7F) >> 7`) become block + offset. The bytes after the header are untouched |
| `reader_over_rebased_shipped_file` | the field-music reader, after MC-5 | `003EAA70` over that table agrees with an independent decode of the **raw** file for **every field 0..1313** at progress 0, 100, 1580, 5000 and `0x8000`. For example, at 1580: 684 fields have a track and 630 have none |
| `MC5_zero_stays_zero_twice_doubles` | MC-5 | A zero page word stays 0, and the reader answers −1 for a field on that page. Running the rebase a second time adds the block address again (32-bit wrap: `EC200034`, …) |
| `MC5_address_limits` | MC-5 | At `0x90000000` the rebase stores `90000034`, and the reader's `movsxd` sign-extends it and **faults**. At `0x200100000` the 32-bit add keeps only `00100034`, and the reader faults there |
| `MC4_sign_extended_target` | MC-4 | `0051EDB0(0x80001000)` jumps to the sign-extended `…FFFF80001000` and faults |
| `MC6_checker_bounded_to_one` | MC-6 | Active at `02B5E0E0+0x31` gives 1. An active byte in a second `0x38` slot is never reached: 0 |
| `MC7_ring_clamped_to_file` | MC-7 | **A `0x12345`-byte file under a `0x30000` ring:** the ring becomes `0x12345` and the first read is the whole file (`bytesRead` `0x12345`, cursor 0, state 2, `requestId` from the real queue). **A `0x45000` file** keeps the `0x30000` ring. **State 2 waits** while `0032E4D0` reports the read in flight |
| `MC7_pieces_and_ring_cursor` | MC-7 | For the `0x45000` file and the `0x30000` ring, state 7 reads the next piece: `0x10000` (the `002DF600` constant), then `0x5000` (the rest of the file). The cursor is `bytesRead mod ring` (`0x10000`, then `0x15000`). With everything read, the machine asks `002DF630` whether the stream is busy |
| `MC8_play_pair` | MC-8 | `bgmstreamplay` (`003EB150`) moves state 5 to 6. The next tick calls **`002DF680(streamId, 0x40, 0x7F)`** from the descriptor's `+0x32` / `+0x33`, which `003EB050` initialised |

## What the execution adds

1. **MC-4 through MC-8 are executed.** MC-5 is executed over the shipped file, and the field-music reader now runs on
   the table the shipped rebase produces. Before this, EXP-099 planted that result and EXP-008 read it live.
2. **The page's size rule is path-dependent.** The music page's §2.1 says
   `size = 0032E400(kind, index); /* the file-size table, rounded up to 64 */`. Measured:
   - `0032E400` returns the table entry **as is** (`0032E428`–`0032E430`);
   - only its fallback path, the call to `0046DE70` when a kind has no table, rounds up to 64 (`0032E43B`–`0032E448`).

   So a `0x12345`-byte stream file clamps the ring to `0x12345`, not `0x12380`. Routed to FABLE.
3. **MC-5's address limits are measured.** Below 2 GB is required by the reader's sign extension, and below 4 GB by
   the rebase's 32-bit add. A block at `0x90000000` or `0x200100000` faults in the reader.
4. **MC-4's sign extension is measured.** A callback word of `0x80000000` or more is not a usable target.

## Not covered

- **MC-1** (one writer) and **MC-2** (the tail jump): static facts. The loader `003EAB60` → `0051ED10` allocates
  from engine heap 5, whose allocator halts unbuilt.
- **MC-3**: the loader's return before the bytes arrive (same allocation).
- The `usebgmstream` buffer rounding: `003EACA0` allocates from heap 2.
- The sound layer's behaviour (it is the boundary).
- A live game.

## MC-3 executed: the loader hands back the block before any byte arrives (OPUS, 2026-09-26)

`mc3.py` runs over this harness (imported unchanged; its cases run first).
- **What this block lacked** was engine heap 5. It is registered by boot's own calls at boot's own sizes, so there is
  no deviation: `00369D30(5, 0036D240(0x1C0100), 0x1C0000, 0x100)`, from `0022A2EC`-`0022A304`.
- **The size.** The kind-9 size-table entry for id `0x20` is planted with the shipped `musicctrl.bin`'s size (1,615 B).
  It is the same kind of fixture as this block's kind-0x24 table.
- **The run.** The boot music loader `003EAB60` then runs as shipped: `0051ED10` → `0032E400` → the heap-5 allocation
  `0036C1D0`/`0036A190`/`0036C140` → `0032E620`.

| case | asserted |
|---|---|
| heap 5 | registered by the shipped arena calls |
| publish | the loader returns; `[02B5E0D0]` (MC-1's one writer, `003EAB78`) holds the returned block, inside arena 5 |
| queue | the read queued through `0032E620` names kind 9, id `0x20`, that block and 1,615 bytes |
| before the bytes | no byte of the block is written during the call; its head is still zero, not the file's `MUS0` header |

**Runs.** 4/4, and two runs give an identical `mc3_result.json`. MC-1 and MC-2 stay static; they are put to AUDIT-SEM as
static-structure invariants.
