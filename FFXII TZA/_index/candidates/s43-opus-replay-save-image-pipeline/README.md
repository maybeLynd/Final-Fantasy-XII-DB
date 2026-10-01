# S-43: the save-image pipeline's seven bodies executed as shipped code (OPUS, 2026-09-25, block 335)

**Evidence class: NATIVE-REPLAY (unicorn), `live_game: false`.** S-43's exposure note (block 299) found no application
stub reaching any S-43 invariant. It named one coverage gap: `CONTRACT-save-image-pipeline.md` (SV-1..SV-6), whose §13
says *"No experiment executes these seven bodies"*. This harness executes them.

## What was run

`check.py`, with `world.py` / `world.json` / `printf_bridge.py` / `shipped_pack.py` from block 334. These run as
shipped:
- the bare clear `002EF5F0` and the compound clear `002EF650`;
- the getters `002EF640` / `002EF620` / `002EF630`;
- the backup copy `002EF570`;
- the submission copy `002EF690`, with its selector `00236760`.

There is **no application stub**. The only import reached is `memset`, bridged by name.

**Stop boundaries** (recorded, nothing substituted):

| boundary | what it is |
|---|---|
| `0020E540` | The platform write `002EF690` tail-jumps into; it fetches the platform storage object `001C18E0`. Its arguments are recorded |
| `001DBAC0` | Where the compound clear's reinitialiser `00253A80` applies sound settings through the audio registry (S-41's object) |

**Fixtures:**
- the buffers' contents: SHAKE-256 patterns, and `0xCC` / `0xAB` fills;
- the selector bit `d[q[02EBF190]+4]` bit 12;
- six idle objects, including `[02092758]` and `[020927C0]`, which `00253A80` clears.

**5 / 5 pass, and `result.json` is byte-identical over three runs** (md5 `68b245056304290b580f06ebf6cddf20`).

| case | contract item | observed |
|---|---|---|
| `SV1_getters_and_spacing` | SV-1 | The getters return `02164280` / `021BA940` / `02211000`. With the backup `022676C0` the three gaps are `0x566C0`: `0x30` of padding past each `0x56690` image |
| `SV2_copies_complete_with_tail` | SV-2 | `002EF570` copies all `0x56690` active bytes to the backup, and `002EF690` all capture bytes to the submission buffer, **the last 16 bytes (the tail after the `0xACD`-block loop) included**. The `0x30` padding after each image is not written |
| `SV6_selector_first_then_copy_then_writer` | SV-6 | `00236760` runs **before the first byte of the copy**. The tail jump reaches `0020E540` with `ecx` = that selector (1), `rdx` = the submission buffer and `r8d` = `0x56690` |
| `SV4_backup_unread_by_the_family` | SV-4 | None of the other bodies reads the backup buffer (a memory-read hook over its whole extent). Its image-wide single reference is static |
| `SV5_two_clears` | SV-5 | `002EF5F0` zeroes exactly `0x56690` bytes (the padding keeps its `0xAB`) and tail-jumps to `0016D6A0`. `002EF650` zeroes the same extent, calls `0016D6A0`, and **only then** enters the reinitialiser `00253A80`: the buffer is all zero at its entry |

## What the execution adds

1. **SV-1, SV-2, SV-4, SV-5 and SV-6 are executed.** SV-3 (six sites load `0x56690`) is an image census. S-43's four
   contracts now all have execution.
2. **SV-6's "handle" is a selector bit.** `00236760` returns bit 12 of `d[q[02EBF190]+4]`, and the writer receives it in
   `ecx`. The contract calls it "a handle obtained from `00236760`"; the value is a 0/1 selector. Routed to FABLE.
3. **The compound clear's reinitialiser reaches the sound layer.** `00253A80` clears two boot singletons, then applies
   sound settings through the audio registry, before `002EF2D0` / `00238A80` would run.

## Not covered

- `002EF2D0` and `00238A80` after the compound clear (past the audio boundary);
- the platform write itself;
- a live game.
