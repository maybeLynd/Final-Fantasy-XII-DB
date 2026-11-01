---
title: "Lua runtime: the embedded Lua 5.2.1 interpreter, its chunk loader, its standard libraries and why no script runs"
kind: "system"
category: "Third-party libraries"
addresses: "0x00683C30, 0x00812F70, 0x00810180, 0x0081DF50, 0x0081D790, 0x0082BE30, 0x0082E910, 0x0082E490, 0x00684D10, 0x00686280, 0x00684F60, 0x00685AC0, 0x006844C0, 0x02E41570, 0x02E41578, 0x00685F60, 0x01CCB3E0, 0x01CCB470, 0x00824340, 0x01CCBA90, 0x00818AC0, 0x00825660, 0x00681840, 0x008216A0, 0x008162F0, 0x00827600"
---

## What the player sees

Nothing. The executable carries a complete Lua 5.2.1 interpreter, wired to PhyreEngine's script
objects, but the shipped game never creates a Lua state and ships no script, so no Lua code runs.
Everything scripted in the game runs on Square Enix's own script machine instead.

## How it works

### Identity and version

The image carries Lua's own banner, `$LuaVersion: Lua 5.2.1  Copyright (C) 1994-2012 Lua.org,
PUC-Rio $` (`0x01CCA080`), the 5.2-only names `LUA_PATH_5_2` (`0x01CCCB48`) and `_ENV` (`0x01CCB6BC`), and
the 5.2-only library `bit32`. The chunk-header check below confirms version byte `0x52`.

### Numbers are single precision

This build is configured with a 4-byte `lua_Number`, a `float`, where stock Lua 5.2 on x64 uses an
8-byte `double`. The chunk-header check expects number size 4, and the library code works in floats:
`math.sin` (`0x00818AC0`) reads its argument as a float, calls the C `sin` on it as a double and
pushes the result back as a float. Thirteen `math` functions share that one shape (`sin`, `sinh`,
`cos`, `cosh`, `tan`, `tanh`, `asin`, `acos`, `atan`, `ceil`, `floor`, `sqrt`, `exp`).

### The chunk loader

PhyreEngine loads a chunk through `0x00683C30(L, script)`:

1. When the script's data pointer `+0x18` is null it returns false without touching Lua.
2. Otherwise it calls `luaL_loadbufferx` (`0x00812F70`) with the data, the length `+0x10` with bit `0x80000000`
   cleared, the chunk name `+0x48` with its low bit cleared, and a null mode.
3. On success it returns true. On failure it reads the error message (`0x00811530` on index -1),
   pops it (`0x00811130` with -2) and returns false; the message is not reported.

`0x00812F70` wraps the buffer in a reader (`0x00812170`) and calls `lua_load` (`0x00810180`), which runs the
parser through `luaD_protectedparser` (`0x0081DF50`). That function takes the address of `f_parser`
(`0x0081D790`, at `0x0081DF7C`), which nothing calls directly.

### Source text and bytecode

`f_parser` looks at the first byte of the chunk:

- `0x1B` (the start of `\x1bLua`): the binary loader `luaU_undump` (`0x0082E910`), which first checks
  the header (`0x0082E490`).
- anything else: the source parser `luaY_parser` (`0x0082BE30`).

Each branch refuses its form only when a mode string is given and lacks `b` or `t`
(`attempt to load a %s chunk (mode is '%s')`). `0x00683C30` passes no mode, so both plain Lua source
and precompiled chunks are accepted.

### Who calls the loader

Three functions load and run a script, each calling `0x00683C30` and then `lua_pcall`, and printing
`execute: lua_pcall failed - error code: %d` (`0x00D6FEB0`, `0x00D6FFD8`) on failure:

| Function | Reached from |
|---|---|
| `0x00684D10` | slot 1 of the `PCallerScript` vtable `0x00D6FDB8` |
| `0x00686280` | slot 2 of the same vtable |
| `0x00684F60` | `0x00685140`, `0x00685560` and `0x006853C0`, slots 0, 1 and 4 of the `PScheduler` vtable `0x00D6FD68` |

Each takes the script from a `PScript` object. `0x00684D10` takes the state from its argument or from
an entry of the buffer pool at `0x02E41050`; none of the three creates one.

### The buffer pool

When the pool exists, `0x00684D10` takes its next free entry: entries are `0x28` bytes from the
pointer at pool `+0x50`, `+0x58` counts the entries in use and `+0x48` (bit `0x80000000` cleared) is the
capacity. It copies entry `+0x10` bytes (bit `0x80000000` cleared) from the buffer at entry `+0x18` to the one
at entry `+0x08` and runs the script on the state at entry `+0x20`.

On its way out it gives the entry back by decrementing `+0x58`, but only when the entry is still the
last one taken. `0x00681840` is the same release as a separate function; the only callers are two
exception-unwind funclets, `0x008A0030` and `0x008A0070`, which pass it the pool and entry they find in
their parent's frame.

### No code creates a Lua state

Creating a state runs `lua_newstate` and its `f_luaopen`, which interns the memory-error message,
initialises the metamethod names and the lexer's reserved words. None of that is in the image:

- the text `not enough memory` occurs nowhere, nor `luaL_newstate`'s `PANIC: unprotected error`;
- the metamethod-name table `0x01CCBA90` (`__index`, `__newindex`, `__gc` …) is referenced by no
  instruction;
- the reserved-word table `0x01CCBBE0` is read only by `luaX_token2str` (`0x00824340`), not by an
  initialiser.

The rest of the core is linked, including the lexer and the protected-call machinery, so the
interpreter can run only on a state built outside the executable and handed to one of the three
functions above.

### Standard libraries

Every standard library of Lua 5.2 is compiled in, each with its registration array:

| Library | Opener | Registered functions |
|---|---|---|
| base | `0x00814F90` | 22 |
| coroutine | `0x00815500` | 6 |
| table | `0x00815E30` | 6 |
| string | `0x00817550` | 14 |
| bit32 | `0x00818A40` | 12 |
| math | `0x00819410` | 27 |
| io | `0x00826500` | 11, plus 9 file methods |
| os | `0x00827430` | 11 |
| debug | `0x00828540` | 16 |
| package | `0x00828D30` | 2, plus the global `require` |

None is ever opened:

- `luaL_openlibs`' two lists, `loadedlibs` at `0x01CCB3E0` (`_G`, `table`, `package`, `coroutine`,
  `io`, `os`, `string`, `debug`) and `preloadedlibs` at `0x01CCB470` (`bit32`, `math`, `string`), are
  referenced by no instruction.
- No opener has a call or jump site.
- `0x00685AC0`, slot 1 of the `PUtilityScripting` vtable `0x00D6FD98`, makes five other setup calls
  and then appends four pairs, `math`, `bit32`, `string` and `coroutine` with their openers,
  to a list through `0x006844C0`. The list's count `0x02E41570` and buffer `0x02E41578` are touched only by
  `0x006844C0` and by `0x00685F60` (slot 2) and `0x008B25C0` (exit), which free it. Nothing reads the
  pairs.

The `io`, `os`, `debug` and `package` functions, among them `io.open`
(`0x00825660`, which checks its mode against `[rwa]%+?b?` and opens a `FILE*`) and `package.loadlib`
(`0x00828580`), are therefore present and unreachable.

### Objects and the collector

Every collectable object is created by `luaC_newobj` (`0x0081A620`). It allocates through `0x00823670` (`0x0081A644`),
writes the type tag at `+0x08` (`0x0081A664`) and the current white, global `+0x54` bits `0x3`, at `+0x09`
(`0x0081A670`). It then links the object at `+0x00` into the list it is given, or into the all-objects list at global
`+0x60` (`0x0081A659`, `0x0081A67A`).

| Object | Constructor | Tag | Size |
|---|---|---|---|
| C closure | `0x0081ECA0` (`0x0081ECC0`), from `lua_pushcclosure` `0x00810470` (`0x008104C5`) | `0x26` | `(nupvalues + 2) << 4` (`0x0081ECA6`, `0x0081ECB4`) |
| Lua closure | `0x0081ECD0` (`0x0081ECF3`), from `0x00823310` (`0x00823345`), `0x0082BE30` (`0x0082BE61`) and `0x0082E910` (`0x0082E96A`, `0x0082E9C8`) | 6 | `nupvalues * 8 + 0x20` (`0x0081ECE6`) |
| long string | `0x0081EFB0` (`0x0081F003`) | `0x14` | `length + 0x21` (`0x0081EFEB`) |
| short string, up to `0x28` bytes | `0x0081F1F0` (`0x0081F258`), from `0x0081EDC0` (`0x0081EE72`), which `0x0081EFB0` jumps to (`0x0081EFD0`) | 4 | `length + 0x21` (`0x0081F234`) |
| userdata | `0x0081F050` (`0x0081F079`), from `0x00810240` (`0x00810269`) | 7 | `length + 0x30` (`0x0081F071`) |
| table | `luaH_new` `0x0081F6B0` (`0x0081F6C6`), from `lua_createtable` `0x0080F740` (`0x0080F76A`), `0x0081CA00`, `0x008216A0`, `0x00829B10` and `0x0082BE30` | 5 | `0x40` (`0x0081F6C2`) |
| function prototype | `luaF_newproto` `0x0081ED30` (`0x0081ED46`), from `0x00829680`, `0x0082BE30`, `0x0082DCE0` and `0x0082E910` | 9 | `0x80` (`0x0081ED42`) |
| upvalue | open: `0x0081EAA0` (`0x0081EAEC`), from `0x00823310` (`0x00823393`), linked into the thread's open list; closed: `0x0081ED90` (`0x0081EDA7`), from `0x0081D790` (`0x0081D863`) | `0xA` | `0x28` (`0x0081EAE8`, `0x0081EDA3`) |
| thread | `lua_newthread` `0x00813F20` (`0x00813F57`), from `coroutine.create` `0x008150F0` and `coroutine.wrap` `0x00815150` | 8 | `0xD0` (`0x00813F47`) |

The collector's sweeps `0x0081B050` (`0x0081B0EC`) and `0x0081B1A0` (`0x0081B24C`) free a dead object through `0x00819C90`.
It picks an arm by tag from the byte table `0x00819D50`:

- a Lua closure (`0x00819CD5`), a C closure (`0x00819CEA`), userdata (`0x00819D09`) and strings (`0x00819D20`) are freed
  at the same size through `0x00823670`; a short string first decrements the string table's count at global
  `+0x38` (`0x00819D12`);
- a table jumps to `0x0081F420` (`0x00819CF4`);
- a thread jumps to `0x00813EB0` (`0x00819CF9`);
- a prototype jumps to `0x0081EB50` (`0x00819CC0`), which frees its vectors and then its `0x80` bytes (`0x0081EBEA`);
- an upvalue jumps to `0x0081EC10` (`0x00819CEF`), which frees `0x28` bytes (`0x0081EC33`, `0x0081EC37`).

No code in the image creates a state (above), so these functions run only on a state built outside the
executable.

Five kinds of record live inside these objects and are never collected on their own:

- a value is `0x10` bytes, the payload at `+0x00` and the tag at `+0x08`: `lua_createtable` pushes a table as
  the pointer (`0x0080F773`), the tag `0x45` (`0x0080F776`) and a step of `0x10` (`0x0080F77D`);
- a call frame is `0x50` bytes: a thread's base frame sits at its `+0x80`, every further frame comes from
  `luaE_extendCI` `0x00813E10` (`0x00813E24`) and is freed by `0x00813D90` (`0x00813DDE`) or `0x00813E50` (`0x00813E8E`);
- the global state shares the `0x2C0` block `close_state` `0x00813D00` frees with the main thread (`0x00813D77`);
- a table's hash nodes are `0x28` bytes, `1 << lsizenode` of them from `setnodevector` `0x00820260`
  (`0x008202DE`-`0x008202EB`), run by `luaH_resize` `0x0081F9B0` (`0x0081F9FB`), which frees the old vector
  (`0x0081FB2B`); a table without a hash part points at the shared node `0x01CCB8C8` (`0x00820283`);
- a prototype's local-variable and upvalue descriptors are `0x10` bytes each, in vectors its loader allocates
  (`0x0082E103` in `0x0082E050`, `0x0082E7D7` in `0x0082E790`).

### Interpreter bodies outside the member list

Three of the largest Lua functions are not in [`lua-runtime-members.tsv`](lua-runtime-members.tsv); each carries Lua's own
messages:

- `0x008216A0` is `luaV_execute`, the bytecode loop: it raises "'for' initial value must be a
  number", "'for' limit must be a number" and "'for' step must be a number". `luaD_call` (`0x0081D900`)
  and the coroutine resume `0x0081E5A0` (with "cannot resume dead coroutine") and `0x0081E920`, which
  it calls, call it.
- `0x008162F0` is `string.format`: the string library's registration array pairs the name `format`
  with it (`0x01CCAD98`), and it raises "invalid option '%%%c' to 'format'".
- `0x00827600` is `debug.getinfo`: the debug library's array pairs `getinfo` with it (`0x01CCC6F8`); its
  default option string is "flnStu" and it raises "function or level expected".


The precompiled-chunk header `0x0082E490` compares, 18 bytes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8[4]` | signature | 1B 4C 75 61  "\x1bLua" |
| `+0x04` | `u8` | version | 52  (5.2) |
| `+0x05` | `u8` | format | 00 |
| `+0x06` | `u8` | endianness | 01  little-endian |
| `+0x07` | `u8` | sizeofInt | 04 |
| `+0x08` | `u8` | sizeofSizeT | 08 |
| `+0x09` | `u8` | sizeofInstr | 04 |
| `+0x0A` | `u8` | sizeofNumber | 04  float |
| `+0x0B` | `u8` | integralNumbers | 00 |
| `+0x0C` | `u8[6]` | tail | 19 93 0D 0A 1A 0A  (`0x01CCD300`) |

It reads 17 bytes after the signature byte the parser has already taken (`0x0082E4CC`) and compares all
18 with the expected header it builds from immediates (`0x0082E4C7` to `0x0082E4EA`).

The `PScript` fields `0x00683C30` reads:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x10` | `u32` | length | bit `0x80000000` is a flag and is cleared |
| `+0x18` | `void*` | data | null: nothing is loaded |
| `+0x48` | `void*` | name | low bit is a flag and is cleared |

## Shipped data

| Fact | Value |
|---|---|
| archive files searched | 89,414 (58,894,815,547 bytes) |
| files with a `.lua` name | 0 |
| files containing a Lua 5.2 header start `1B 4C 75 61 52 00` | 0 |
| bare `1B 4C 75 61` matches | 2, inside `anx.webm` and `vnp.webm` video data, followed by `08` and `17`, not `52` |
| files containing `PScript`, `PScheduler`, `PCallerScript`, `PUtilityScripting` or a Lua 5.2 chunk header | 0 of 89,414, among them 0 of the 35,984 `.phyre` files |

## Modding notes

- The game never builds a Lua state. Running Lua needs a state created outside the executable and a
  `PScript` object supplied to `PCallerScript` or `PScheduler`, which no shipped asset declares.
- Plain Lua source is accepted; nothing needs compiling.
- Precompiled chunks must come from a Lua 5.2 compiler built with a 4-byte float number type. A stock
  x64 `luac` writes number size 8 and the header check rejects it.
- Numbers are single precision: integers are exact only up to 16,777,216.
- A compile error is swallowed by `0x00683C30`; the script silently does not load.
- No standard library is opened, so even `print`, `pairs` and `string` are absent unless the state's
  creator opens them.

## Related

- PhyreEngine: the scripting classes (`PScript`,
  `PScheduler`, `PCallerScript`) and object bindings around this interpreter.
- [Script interpreter](../Scripts-And-Script-Commands/script-interpreter.md): the game's own script
  machine, which runs every shipped script.
- [The member table](lua-runtime-members.tsv): the interpreter's functions, from `0x0080F2E0` up to `0x00830760`,
  213 of the 600 with their Lua 5.2.1 name: 130 from the libraries' `luaL_Reg` tables (`print`, `string.format`,
  `file:read`, the `luaopen_` openers) and 83 from a message only that function uses or from its code
  (`lua_pcallk` `0x00810340`, `index2addr` `0x0080F300`); the evidence is in each row.
- [The one-argument math functions](lua-runtime-lua-math-unaryfunctionadapter.tsv): the thirteen `math` functions
  that take one argument.
