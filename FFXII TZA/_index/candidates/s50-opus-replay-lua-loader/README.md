# S-50: the Lua chunk loader's entry, fork and header check executed as shipped code (OPUS, 2026-09-25, block 322)

**Evidence class: NATIVE-REPLAY (unicorn), `live_game: false`.** S-50's exposure note (block 301) found every
invariant of `CONTRACT-lua-chunk-loader.md` **unexecuted**: EXP-110 scripts `00683C30` at its entry, and nothing
downstream of it runs. This harness runs the loader's bodies themselves.

## What was run

`check.py`, with `world.py` / `world.json` / `printf_bridge.py` from blocks 318 / 319 / 321. The world is built once
through `Session` and is not otherwise used.

**No lua_State exists.** No shipped asset carries a chunk, and no `lua_State` constructor has been located (the Lua
pages' DA-1). So this does **not** load a chunk end to end. Each body runs as shipped code up to its first call into
machinery that needs a live state. That call is a **stop boundary**: the run ends there and its arguments are
recorded. Nothing is substituted.

| stop boundary | reached from |
|---|---|
| `00812F70` `luaL_loadbufferx` | `00683C30` |
| `0082E910` `luaU_undump` | the fork |
| `0082BE30` `luaY_parser` | the fork |
| `0081BFF0` `luaO_pushfstring` | any refusal; the format argument and the `why` string are recorded |

**Everything else runs as shipped:**
- `00683C30`;
- the fork `0081D790` (`f_parser`);
- the header check `0082E490`;
- the ZIO read `0081C6A0`, whose refill is inline: it calls the ZIO reader at `0081C6D5` (`call [rbx+0x10]`) and copies
  through the `memcpy` thunk `00861EBA` (bridged by name).

EXP-110 and `diff_lua_header.py` stubbed the ZIO read `0081C6A0`; it runs as shipped here.

**Fixtures** are planted data only:
- the Phyre buffer;
- the chunk bytes;
- the ZIO `{n, p, reader, data, L}`, the SParser (`z` at `+0`, `mode` at `+0x50`, `name` at `+0x58`) and the
  LoadState `{L, z, b, name}`.

The ZIO reader is the shipped `xor eax, eax; ret` at `00122125`, so a refill sees EOF.

**Imports.** Besides `memcpy`, the only import these bodies reach is `strchr`, the mode guard's call through IAT
`008C2A10` at `0081D7ED`. Both are bridged by name as the C library functions.

**3 / 3 pass, and `result.json` is byte-identical over three runs** (md5 `4ccfbccf7afaad3cb9246a8faad83b92`).

| case | contract item | observed |
|---|---|---|
| `PRE_and_marshalling_00683C30` | §4 PRE, §3.2, §12 | With a buffer whose data qword `+0x18` is NULL, the entry returns **without reaching the load**. With a NULL buffer pointer, the **first fault is the read at `0x48`**: `rdx` is dereferenced before any check. For a buffer with `+0x10 = 0x80001234`, `+0x18 = data` and `+0x48 = 0x21`, the load receives `(L, data, r8 = 0x1234, r9 = 0x20, mode = 0)` |
| `I1_I2_fork_and_mode_guards` | §4 I1, I2; §7 | First byte `0x1B` goes to `luaU_undump`; `return 1` goes to `luaY_parser`. With `mode == NULL` neither guard fires. `"t"` on a binary chunk and `"b"` on a text chunk are **refused through `luaO_pushfstring` before either path**, with `why` = `"t"` / `"b"`. `"bt"` passes a binary chunk |
| `I3_header_18_compared_17_read` | §4 I3, §3.1, §10 | The shipped 5.2 header (`LuaR`, format 0, `01 04 08 04 04 00`, tail `19 93 0D 0A 1A 0A`) is accepted. **A one-bit flip at every one of header bytes 1..17 is refused.** 16 bytes, with the shipped EOF reader behind them, is refused as **`truncated`** by the real `luaZ_read` / `luaZ_fill` |

## What the execution adds

1. **The §3.2 correction is confirmed by execution.** §12's boxed correction (added statically) says `r8` is the
   size and `r9` is the name. The run shows it:
   - the u32 at `+0x10` with bit 31 cleared (`0x80001234` → `0x1234`) arrives in **`r8`, the size**;
   - the qword at `+0x48` less its low bit (`0x21` → `0x20`) arrives in **`r9`, the name**.

   **Still stale in the same page** (routed to FABLE, not edited here):
   - §3.2's table still labels `+0x10` `name` and `+0x48` `length`;
   - §2's row gives `00812F70` as `(L, data, len, u32 name, mode)`;
   - §12's reproduction formula computes `len` from `+0x48` and `name` from `+0x10`;
   - §14 still carries "whether `name` is a pointer or an index, given it is passed as 32 bits".
2. **The refusal messages form a prefix cascade.** Measured per header byte (1-based, after the dispatcher's
   `0x1B`):

   | header bytes | message |
   |---|---|
   | 1–3 (`Lua`) | `not a` |
   | 4–5 (version `0x52`, format `0`) | `version mismatch in` |
   | 6–11 (endianness and the five size bytes) | `incompatible` |
   | 12–17 (the tail) | `corrupted` |

   This is Lua 5.2's `checkHeader` cascade over prefixes of 4, 6 and 12 bytes (counting the planted `0x1B`). §13's
   `diff_lua_header.py` counts outcomes per case; this is the per-byte map, measured with the formatter as the only
   boundary.
3. **The mode guards call `strchr` on the mode string.** A mode that excludes the chunk's kind is refused before the
   fork dispatches; the formatted `why` is the mode string itself.
4. **`truncated` goes through the shipped refill.** A short stream now reaches the message through `0081C6A0`'s own
   refill (`0081C6D5`, the ZIO reader, reached and returning NULL), not through a stubbed read.

## Not covered

- **POST** (`true` only when `luaL_loadbufferx` returned 0, and the stack is restored on failure). It needs
  `00812F70` to return, and that needs a live `lua_State`, so it remains unexecuted.
- `luaU_undump` / `luaY_parser` bodies.
- The message formatting itself (`luaO_pushfstring` is a boundary).
- DA-1: no chunk from a real asset.
- A live game.
