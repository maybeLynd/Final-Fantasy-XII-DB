---
title: "Image hardening: the executable's load address, DEP, Control Flow Guard and stack cookies as built"
kind: "system"
category: "Compiler and C runtime"
addresses: "00808EE4, 00809B8C, 00808C40, 00809654, 00809620, 00809728, 0080973C, 01F44830, 01F44838, 008C31C0, 008C31C8, 0016D6A0, 00896270, 00809958, 0059A030, 0059D2D0, 01F2CDA0, 02CA9D91, 0067F700, 00594EB0, 00594350, 02D3E880, 00165F80, 008B1B00"
---

## What the player sees

Nothing in normal play. The game always loads at the same address, so an address found once (in a
cheat table, a trainer or this database) is valid on every machine and every launch. If something
overruns a protected stack buffer, the game closes at once with no error box and no crash dump of its
own.

## How it works

### Load address and relocations

The optional header asks for image base `00120000`<sub>h</sub>. `DllCharacteristics` is `8120`<sub>h</sub>:
`HIGH_ENTROPY_VA` (`0020`<sub>h</sub>), `NX_COMPAT` (`0100`<sub>h</sub>) and `TERMINAL_SERVER_AWARE` (`8000`<sub>h</sub>).
`DYNAMIC_BASE` (`0040`<sub>h</sub>) is clear, so the loader maps the image at its preferred base and
`HIGH_ENTROPY_VA` has no effect. Every address in this database is `00120000`<sub>h</sub> plus the RVA and is the
address in the running game.

The file header's `Characteristics` is `0022`<sub>h</sub>, so `RELOCS_STRIPPED` is clear, and the base-relocation
directory (`39360`<sub>h</sub> bytes) is shipped. The image could be rebased by a tool; the Windows loader has no
reason to rebase it.

### Data execution prevention

`NX_COMPAT` is set, and no section is both writable and executable: `.text` is the only executable
section and is read-only; `.data` and `.tls` are the only writable ones. Code placed in a data page by
a mod needs `VirtualProtect` or an executable `VirtualAlloc` before it can run.

### Control Flow Guard is present but never switched on

The load configuration directory is 148 bytes. It names a check slot `008C31C0` and a dispatch slot
`008C31C8`, gives no guard function table (table and count 0), and its `GuardFlags` is `00000100`<sub>h</sub>
(`CF_INSTRUMENTED` alone, no `CF_FUNCTION_TABLE_PRESENT`). `GUARD_CF` (`4000`<sub>h</sub>) is clear in
`DllCharacteristics`, so the loader never enables the feature and the slots keep their on-disk values:

- the check slot holds `0016D6A0`, whose whole body is `C2 00 00` (`ret 0`);
- the dispatch slot holds `00896270`, which is `FF E0` (`jmp rax`) followed by padding.

One instruction in the image reads the check slot: the thunk `00809958` (`jmp [008C31C0]`). Its eleven
callers are all runtime start-up and lock code between `008087C4` and `00809CD4` (among them
`_Init_thread_wait` `008093C0` and `_Init_thread_notify` `00809364`). No instruction references the
dispatch slot, and no code branches to `00896270`. The game's own indirect calls carry no guard check at
all.

The `.gfids` section holds twelve dwords (`49 48 19 10 13 16 69 113 10 98 55 11`, 48 bytes of a
512-byte raw section). The load configuration does not point at them, and the image's own section
contribution record lists them as a `.gfids$y` input of `30`<sub>h</sub> bytes; none of them is an RVA.

### The shared do-nothing body at 0016D6A0

`0016D6A0` is three bytes of `ret 0`, and the linker has folded many empty functions onto it. Code
reaches it by 2,528 direct calls and 340 direct jumps, plus 22 through the jump `0017E7D0`. These are
calls to functions that do nothing in this build, not guard checks: a direct call never consults the
check slot. A body that "calls `0016D6A0`" does nothing at that point.

### Stack cookies

The cookie is the qword at `01F44830`, named by the load configuration's `SecurityCookie` field. On disk
it holds `00002B992DDFA232`<sub>h</sub>. The entry point `00808EE4` calls `__security_init_cookie` (`00809B8C`)
before anything else, then jumps to the runtime start-up `00808D78`.

1. If the cookie still holds the on-disk value (`00809BAF`), it builds a new one: the system time
   (`GetSystemTimeAsFileTime`) xor the thread id xor the process id xor
   `(counter.high << 32) xor counter` from `QueryPerformanceCounter` xor the address of a stack local,
   masked to 48 bits; a result equal to the on-disk value becomes `00002B992DDFA233`<sub>h</sub>. It is stored at
   `00809C1C`, the cookie's only writer.
2. In both cases the complement of the cookie is stored at `01F44838` (`00809C2B`).

A protected function stores `cookie xor rsp` in its frame and, before returning, passes it back to
`__security_check_cookie` (`00808C40`). The check compares it with the cookie (`00808C40`), then rotates
the value left 16 bits and requires the low 16 bits of the result, the cookie's unused top bits, to be
zero (`00808C4A`). On either failure it jumps to `__report_gsfailure` (`00809654`), restoring the value
first on the second path (`00808C58`).

`__report_gsfailure` asks `IsProcessorFeaturePresent(23)` and, when fast fail is available, executes
`int 29h` with code 2 (`00809670`): the process ends with no exception raised. Otherwise it builds a
`C0000409`<sub>h</sub> exception record and calls `00809620`, which first calls `SetUnhandledExceptionFilter(NULL)`
(`0080962B`), then `UnhandledExceptionFilter`, then `TerminateProcess(GetCurrentProcess(), C0000409h)`.
Either way the game's own crash filter never runs.

### Range-check failures

`__report_rangecheckfailure` (`00809728`) calls `0080973C` with code 8, which fast-fails the same way
(`int 29h` at `00809758`) or takes the same filter-clearing fallback. The compiler emits a call to it
where an index into a fixed-size array could not be proved in range.

### Teardowns that end in the do-nothing body

185 functions are exactly `lea rcx, [a static]` followed by `jmp 0016D6A0`, 12 bytes each. Every one
is registered with `atexit` (`00808B90`), so each is the teardown of a static whose destructor is
empty; see [static initialisation and teardown](static-initialisation-and-teardown.md). 144 of them
belong to one structure, Phyre serialization's scalar-conversion tree:

- The lookup `0059A030(source, destination)` calls 144 registrars (`005850F0`–`00592770`, 383 bytes
  each) once, guarded by the byte `02CA9D91`, then walks the tree under the sentinel `01F2CDA0` for the
  `(source, destination)` key and returns the node's routine, or 0.
- Each registrar is a thread-safe local static (see [lazy statics](lazy-statics-and-one-time-init.md)):
  it fills one node (layout below), registers its 12-byte teardown, and inserts the node, rebalancing
  through `0067F700`.
- The twelve type descriptors are Phyre's `bool`, `PChar`, `PUInt8`, `PInt16`, `PUInt16`, `PInt32`,
  `PUInt32`, `PInt64`, `PUInt64`, `PUInt128`, `float` and `double`, each returned by its own accessor
  in `0062FF50`–`00630490`. Each of the 144 ordered pairs occurs once.
- `0059D2D0` stores the routine `0059A030` returns, and stores `0016D6A0` itself when there is none
  (`0059D3BD`), so an unsupported pair converts nothing.

The 144 nodes share 68 routines. Every routine takes `(source base, destination base, desc, context)`,
where `desc` holds the element count, the source stride, the destination stride and a byte that swaps
the two field offsets read from the context, and converts `count` elements, four per loop pass. The
pairing follows from the arithmetic:

- every conversion to an 8-bit integer is the one byte copy `00595C00` (20 pairs), to a 16-bit integer
  `00593980` (14), to a 32-bit integer `005939F0` (10);
- `00594EB0` converts `double` to `float` (`cvtpd2ps`) and `00594350` `float` to `double`
  (`cvtps2pd`);
- float to integer routines truncate (`cvttss2si`, `cvttsd2si`, 18 routines); integer to float routines
  use `cvtsi2ss`, `cvtsi2sd`, `cvtdq2ps` or `cvtdq2pd` (18 routines); 30 routines move integers only.

One of the other 41 tears down the event record `02D3E880`. Its initialiser `00165F80` zeroes the record
(`005CC8A0`) and registers `008B1B00`. `00677450` creates it: when `+00`<sub>h</sub> is 0 it calls `005CD0A0`,
which stores a `CreateEventA` handle (auto-reset, initially unsignalled) at `+08`<sub>h</sub> and sets `+10`<sub>h</sub>
and `+00`<sub>h</sub>. `00677520` closes it through `005CD6D0` (`CloseHandle`). The empty teardown never closes
the handle.

### What the image records about its build

The debug directory has four entries: a CodeView `RSDS` record naming the program database
`FF12X64.pdb` (not shipped); a `VC_FEATURE` record counting 1,296 compiled objects, 1,265 of them built
with `/GS`, 89 with `/sdl` and 49 guard-aware; the linker's section-contribution record (`GCTL`); and
an empty fourth entry. The optional header gives linker version 14.0. There is no COFF symbol table
(`PointerToSymbolTable` and `NumberOfSymbols` are 0).

## Layouts

IMAGE_OPTIONAL_HEADER64 (fields used here):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `18`<sub>h</sub> | `u64` | ImageBase | `00120000`<sub>h</sub> |
| `46`<sub>h</sub> | `u16` | DllCharacteristics | `8120`<sub>h</sub> |

IMAGE_LOAD_CONFIG_DIRECTORY64, 148 bytes at `01CEBE40`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `58`<sub>h</sub> | `u64` | SecurityCookie | `01F44830`<sub>h</sub> |
| `70`<sub>h</sub> | `u64` | GuardCFCheckFunctionPointer | `008C31C0`<sub>h</sub> |
| `78`<sub>h</sub> | `u64` | GuardCFDispatchFunctionPointer | `008C31C8`<sub>h</sub> |
| `80`<sub>h</sub> | `u64` | GuardCFFunctionTable | 0 |
| `88`<sub>h</sub> | `u64` | GuardCFFunctionCount | 0 |
| `90`<sub>h</sub> | `u32` | GuardFlags | `00000100`<sub>h</sub> |

```
section   address    virtual size   raw size    access
.text     00121000   0x07A0635      0x07A0800   R-X
.rdata    008C2000   0x152D7FC      0x152D800   R--
.data     01DF0000   0x11A7530      0x018E400   RW-
.pdata    02F98000   0x0068A0C      0x0068C00   R--
.rodata   03001000   0x00011C0      0x0001200   R--
.gfids    03003000   0x0000030      0x0000200   R--
.tls      03004000   0x0000009      0x0000200   RW-
_RDATA    03005000   0x000A250      0x000A400   R--
.rsrc     03010000   0x004B830      0x004BA00   R--
.reloc    0305C000   0x0039360      0x0039400   R--
```

Scalar-conversion tree node, `30`<sub>h</sub> bytes, guard dword at +`30`<sub>h</sub> (`02CAAD10`..02CACC58):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u64` | link0 | self-linked until inserted |
| `08`<sub>h</sub> | `u64` | link1 |  |
| `10`<sub>h</sub> | `u64` | parent | low bit is the node colour |
| `18`<sub>h</sub> | `u64` | source | type descriptor (lookup key, first) |
| `20`<sub>h</sub> | `u64` | destination | type descriptor (lookup key, second) |
| `28`<sub>h</sub> | `u64` | routine | conversion routine |

Event record `02D3E880`, `28`<sub>h</sub> bytes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u8` | created |  |
| `08`<sub>h</sub> | `u64` | handle | CreateEventA result |
| `10`<sub>h</sub> | `u8` | flag | set by `005CD0A0`, cleared by `005CD6D0` |
| `18`<sub>h</sub> | `u32` | (zeroed by 005CC8A0) |  |
| `20`<sub>h</sub> | `u32` | (zeroed by 005CC8A0) |  |
| `24`<sub>h</sub> | `u32` | (zeroed by 005CC8A0) |  |

## Shipped data

| Fact | Value |
|---|---|
| image base | `00120000`<sub>h</sub>; entry point RVA `6E8EE4`<sub>h</sub> (`00808EE4`) |
| `DllCharacteristics` | `8120`<sub>h</sub>: `HIGH_ENTROPY_VA`, `NX_COMPAT`, `TERMINAL_SERVER_AWARE` |
| file `Characteristics` | `0022`<sub>h</sub>; relocations shipped, `39360`<sub>h</sub> bytes |
| `GuardFlags` | `00000100`<sub>h</sub>; guard function table 0, count 0 |
| cookie on disk | `00002B992DDFA232`<sub>h</sub> at `01F44830` |
| cookie checks | 2,390 call sites of `00808C40` in 2,209 functions |
| cookie reads | 2,216, one per function: 2,208 prologue loads in functions that call the check, plus runtime code |
| range-check calls | 237 call sites of `00809728` in 114 functions |
| calls to `0016D6A0` | 2,528 calls and 340 jumps direct, 22 more through `0017E7D0` |
| `ret 0` teardowns | 185, all `atexit`-registered; 144 scalar-conversion nodes, 41 others |
| `.gfids` | 12 dwords, 48 bytes, referenced by nothing |
| `VC_FEATURE` | 1,296 objects; 1,265 `/GS`, 89 `/sdl`, 49 guard-aware |

Function counts follow the image's `.pdata` entries, each chained entry folded into its primary.

The member lists beside this page:

- `image-hardening-guard-adapter-registrars.tsv`: the 145 empty teardowns registered by the
  scalar-conversion registrars and by `00165F80`, with the static each tears down, its registrar and the
  registrar's descriptor pair and routine.
- `image-hardening-scalar-conversion-registrars.tsv`: the scalar-conversion registrars.
- `image-hardening-guard-cf-dispatch-target.tsv`: the dispatch target `00896270`.

## Modding notes

- Addresses are fixed: no rebasing layer is needed, and the live cookie can be read at `01F44830`.
- Indirect calls are not validated. A vtable slot or callback pointer can be redirected, and a corrupt
  one is followed without any check.
- DEP is requested: allocate executable memory or change page protection before running injected code.
- A hook that grows or moves a protected frame must keep its cookie slot intact, and nothing may write
  `01F44830` after start-up; every protected function live at that moment would fail its check on
  return. The failure cannot be caught by a structured or vectored exception handler.
- Setting `GUARD_CF` or wiring `.gfids` would switch Control Flow Guard on with no valid-target table,
  and every indirect call would fail.

## Related

- [Static initialisation and teardown](static-initialisation-and-teardown.md): the `atexit` registrations
  the empty teardowns belong to.
- [Lazy statics and one-time initialisation](lazy-statics-and-one-time-init.md): the guard the
  scalar-conversion registrars use.
- [Object construction and destruction](object-construction-and-destruction.md): the deleting
  destructors whose sized-delete branch ends in `0016D6A0`.
- `runtime-services.md`: the imported Windows and runtime functions.
- [Class hierarchy](../Engine-Core/class-hierarchy.md): the RTTI that names the classes.
