---
title: "Lua runtime: the embedded Lua 5.2.1 interpreter, its chunk loader, its standard libraries and why no script runs"
kind: "system"
category: "Third-party libraries"
addresses: "00683C30, 00812F70, 00810180, 0081DF50, 0081D790, 0082BE30, 0082E910, 0082E490, 00684D10, 00686280, 00684F60, 00685AC0, 006844C0, 02E41570, 02E41578, 00685F60, 01CCB3E0, 01CCB470, 00824340, 01CCBA90, 00818AC0, 00825660, 00681840, 008216A0, 008162F0, 00827600"
---

## What the player sees

Nothing. The executable carries a complete Lua 5.2.1 interpreter, wired to PhyreEngine's script
objects, but the shipped game never creates a Lua state and ships no script, so no Lua code runs.
Everything scripted in the game runs on Square Enix's own script machine instead.

## How it works

### Identity and version

The image carries Lua's own banner, `$LuaVersion: Lua 5.2.1  Copyright (C) 1994-2012 Lua.org,
PUC-Rio $` (`01CCA080`), the 5.2-only names `LUA_PATH_5_2` (`01CCCB48`) and `_ENV` (`01CCB6BC`), and
the 5.2-only library `bit32`. The chunk-header check below confirms version byte `52`<sub>h</sub>.

### Numbers are single precision

This build is configured with a 4-byte `lua_Number`, a `float`, where stock Lua 5.2 on x64 uses an
8-byte `double`. The chunk-header check expects number size 4, and the library code works in floats:
`math.sin` (`00818AC0`) reads its argument as a float, calls the C `sin` on it as a double and
pushes the result back as a float. Thirteen `math` functions share that one shape (`sin`, `sinh`,
`cos`, `cosh`, `tan`, `tanh`, `asin`, `acos`, `atan`, `ceil`, `floor`, `sqrt`, `exp`).

### The chunk loader

PhyreEngine loads a chunk through `00683C30(L, script)`:

1. When the script's data pointer `+18`<sub>h</sub> is null it returns false without touching Lua.
2. Otherwise it calls `luaL_loadbufferx` (`00812F70`) with the data, the length `+10`<sub>h</sub> with bit 31
   cleared, the chunk name `+48`<sub>h</sub> with its low bit cleared, and a null mode.
3. On success it returns true. On failure it reads the error message (`00811530` on index -1),
   pops it (`00811130` with -2) and returns false; the message is not reported.

`00812F70` wraps the buffer in a reader (`00812170`) and calls `lua_load` (`00810180`), which runs the
parser through `luaD_protectedparser` (`0081DF50`). That function takes the address of `f_parser`
(`0081D790`, at `0081DF7C`), which nothing calls directly.

### Source text and bytecode

`f_parser` looks at the first byte of the chunk:

- `1B`<sub>h</sub> (the start of `\x1bLua`): the binary loader `luaU_undump` (`0082E910`), which first checks
  the header (`0082E490`).
- anything else: the source parser `luaY_parser` (`0082BE30`).

Each branch refuses its form only when a mode string is given and lacks `b` or `t`
(`attempt to load a %s chunk (mode is '%s')`). `00683C30` passes no mode, so both plain Lua source
and precompiled chunks are accepted.

### Who calls the loader

Three functions load and run a script, each calling `00683C30` and then `lua_pcall`, and printing
`execute: lua_pcall failed - error code: %d` (`00D6FEB0`, `00D6FFD8`) on failure:

| Function | Reached from |
|---|---|
| `00684D10` | slot 1 of the `PCallerScript` vtable `00D6FDB8` |
| `00686280` | slot 2 of the same vtable |
| `00684F60` | `00685140`, `00685560` and `006853C0`, slots 0, 1 and 4 of the `PScheduler` vtable `00D6FD68` |

Each takes the script from a `PScript` object. `00684D10` takes the state from its argument or from
an entry of the buffer pool at `02E41050`; none of the three creates one.

### The buffer pool

When the pool exists, `00684D10` takes its next free entry: entries are `28`<sub>h</sub> bytes from the
pointer at pool `+50`<sub>h</sub>, `+58`<sub>h</sub> counts the entries in use and `+48`<sub>h</sub> (bit 31 cleared) is the
capacity. It copies entry `+10`<sub>h</sub> bytes (bit 31 cleared) from the buffer at entry `+18`<sub>h</sub> to the one
at entry `+08`<sub>h</sub> and runs the script on the state at entry `+20`<sub>h</sub>.

On its way out it gives the entry back by decrementing `+58`<sub>h</sub>, but only when the entry is still the
last one taken. `00681840` is the same release as a separate function; the only callers are two
exception-unwind funclets, `008A0030` and `008A0070`, which pass it the pool and entry they find in
their parent's frame.

### No code creates a Lua state

Creating a state runs `lua_newstate` and its `f_luaopen`, which interns the memory-error message,
initialises the metamethod names and the lexer's reserved words. None of that is in the image:

- the text `not enough memory` occurs nowhere, nor `luaL_newstate`'s `PANIC: unprotected error`;
- the metamethod-name table `01CCBA90` (`__index`, `__newindex`, `__gc` …) is referenced by no
  instruction;
- the reserved-word table `01CCBBE0` is read only by `luaX_token2str` (`00824340`), not by an
  initialiser.

The rest of the core is linked, including the lexer and the protected-call machinery, so the
interpreter can run only on a state built outside the executable and handed to one of the three
functions above.

### Standard libraries

Every standard library of Lua 5.2 is compiled in, each with its registration array:

| Library | Opener | Registered functions |
|---|---|---|
| base | `00814F90` | 22 |
| coroutine | `00815500` | 6 |
| table | `00815E30` | 6 |
| string | `00817550` | 14 |
| bit32 | `00818A40` | 12 |
| math | `00819410` | 27 |
| io | `00826500` | 11, plus 9 file methods |
| os | `00827430` | 11 |
| debug | `00828540` | 16 |
| package | `00828D30` | 2, plus the global `require` |

None is ever opened:

- `luaL_openlibs`' two lists, `loadedlibs` at `01CCB3E0` (`_G`, `table`, `package`, `coroutine`,
  `io`, `os`, `string`, `debug`) and `preloadedlibs` at `01CCB470` (`bit32`, `math`, `string`), are
  referenced by no instruction.
- No opener has a call or jump site.
- `00685AC0`, slot 1 of the `PUtilityScripting` vtable `00D6FD98`, makes five other setup calls
  and then appends four pairs, `math`, `bit32`, `string` and `coroutine` with their openers,
  to a list through `006844C0`. The list's count `02E41570` and buffer `02E41578` are touched only by
  `006844C0` and by `00685F60` (slot 2) and `008B25C0` (exit), which free it. Nothing reads the
  pairs.

The `io`, `os`, `debug` and `package` functions, among them `io.open`
(`00825660`, which checks its mode against `[rwa]%+?b?` and opens a `FILE*`) and `package.loadlib`
(`00828580`), are therefore present and unreachable.

### Interpreter bodies outside the member list

Three of the largest Lua functions are not in `lua-runtime-members.tsv`; each carries Lua's own
messages:

- `008216A0` is `luaV_execute`, the bytecode loop: it raises "'for' initial value must be a
  number", "'for' limit must be a number" and "'for' step must be a number". `luaD_call` (`0081D900`)
  and the coroutine resume `0081E5A0` (with "cannot resume dead coroutine") and `0081E920`, which
  it calls, call it.
- `008162F0` is `string.format`: the string library's registration array pairs the name `format`
  with it (`01CCAD98`), and it raises "invalid option '%%%c' to 'format'".
- `00827600` is `debug.getinfo`: the debug library's array pairs `getinfo` with it (`01CCC6F8`); its
  default option string is "flnStu" and it raises "function or level expected".


The precompiled-chunk header `0082E490` compares, 18 bytes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u8[4]` | signature | 1B 4C 75 61  "\x1bLua" |
| `04`<sub>h</sub> | `u8` | version | 52  (5.2) |
| `05`<sub>h</sub> | `u8` | format | 00 |
| `06`<sub>h</sub> | `u8` | endianness | 01  little-endian |
| `07`<sub>h</sub> | `u8` | sizeofInt | 04 |
| `08`<sub>h</sub> | `u8` | sizeofSizeT | 08 |
| `09`<sub>h</sub> | `u8` | sizeofInstr | 04 |
| `0A`<sub>h</sub> | `u8` | sizeofNumber | 04  float |
| `0B`<sub>h</sub> | `u8` | integralNumbers | 00 |
| `0C`<sub>h</sub> | `u8[6]` | tail | 19 93 0D 0A 1A 0A  (`01CCD300`) |

It reads 17 bytes after the signature byte the parser has already taken (`0082E4CC`) and compares all
18 with the expected header it builds from immediates (`0082E4C7` to `0082E4EA`).

The `PScript` fields `00683C30` reads:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `10`<sub>h</sub> | `u32` | length | bit 31 is a flag and is cleared |
| `18`<sub>h</sub> | `void*` | data | null: nothing is loaded |
| `48`<sub>h</sub> | `void*` | name | low bit is a flag and is cleared |

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
- A compile error is swallowed by `00683C30`; the script silently does not load.
- No standard library is opened, so even `print`, `pairs` and `string` are absent unless the state's
  creator opens them.

## Related

- PhyreEngine: the scripting classes (`PScript`,
  `PScheduler`, `PCallerScript`) and object bindings around this interpreter.
- [Script interpreter](../Scripts-And-Script-Commands/script-interpreter.md): the game's own script
  machine, which runs every shipped script.
- `lua-runtime-members.tsv`: the interpreter's functions, from `0080F2E0` up to `00830760`.
- `lua-runtime-lua-math-unaryfunctionadapter.tsv`: the thirteen one-argument `math` functions.
