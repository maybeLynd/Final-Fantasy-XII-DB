---
title: "Image hardening: the executable's load address, DEP, Control Flow Guard and stack cookies as built"
kind: "system"
category: "Compiler and C runtime"
addresses: "0x00808EE4, 0x00809B8C, 0x00808C40, 0x00809654, 0x00809620, 0x00809728, 0x0080973C, 0x01F44830, 0x01F44838, 0x008C31C0, 0x008C31C8, 0x0016D6A0, 0x00896270, 0x00809958, 0x0059A030, 0x0059D2D0, 0x01F2CDA0, 0x02CA9D91, 0x0067F700, 0x00594EB0, 0x00594350, 0x02D3E880, 0x00165F80, 0x008B1B00"
---

## What the player sees

Nothing in normal play. The game always loads at the same address, so an address found once (in a
cheat table, a trainer or this database) is valid on every machine and every launch. If something
overruns a protected stack buffer, the game closes at once with no error box and no crash dump of its
own.

## How it works

### Load address and relocations

The optional header asks for image base `0x00120000`. `DllCharacteristics` is `0x8120`:
`HIGH_ENTROPY_VA` (`0x0020`), `NX_COMPAT` (`0x0100`) and `TERMINAL_SERVER_AWARE` (`0x8000`).
`DYNAMIC_BASE` (`0x0040`) is clear, so the loader maps the image at its preferred base and
`HIGH_ENTROPY_VA` has no effect. Every address in this database is `0x00120000` plus the RVA and is the
address in the running game.

The file header's `Characteristics` is `0x0022`, so `RELOCS_STRIPPED` is clear, and the base-relocation
directory (`0x39360` bytes) is shipped. The image could be rebased by a tool; the Windows loader has no
reason to rebase it.

### Data execution prevention

`NX_COMPAT` is set, and no section is both writable and executable: `.text` is the only executable
section and is read-only; `.data` and `.tls` are the only writable ones. Code placed in a data page by
a mod needs `VirtualProtect` or an executable `VirtualAlloc` before it can run.

### Control Flow Guard is present but never switched on

The load configuration directory is 148 bytes. It names a check slot `0x008C31C0` and a dispatch slot
`0x008C31C8`, gives no guard function table (table and count 0), and its `GuardFlags` is `0x00000100`
(`CF_INSTRUMENTED` alone, no `CF_FUNCTION_TABLE_PRESENT`). `GUARD_CF` (`0x4000`) is clear in
`DllCharacteristics`, so the loader never enables the feature and the slots keep their on-disk values:

- the check slot holds `0x0016D6A0`, whose whole body is `C2 00 00` (`ret 0`);
- the dispatch slot holds `0x00896270`, which is `FF E0` (`jmp rax`) followed by padding.

One instruction in the image reads the check slot: the thunk `0x00809958` (`jmp [0x008C31C0]`). Its eleven
callers are all runtime start-up and lock code between `0x008087C4` and `0x00809CD4` (among them
`_Init_thread_wait` `0x008093C0` and `_Init_thread_notify` `0x00809364`). No instruction references the
dispatch slot, and no code branches to `0x00896270`. The game's own indirect calls carry no guard check at
all.

The `.gfids` section holds twelve dwords (`49 48 19 10 13 16 69 113 10 98 55 11`, 48 bytes of a
512-byte raw section). The load configuration does not point at them, and the image's own section
contribution record lists them as a `.gfids$y` input of `0x30` bytes; none of them is an RVA.

### The shared do-nothing body at 0x0016D6A0

`0x0016D6A0` is three bytes of `ret 0`, and the linker has folded many empty functions onto it. Code
reaches it by 2,528 direct calls and 340 direct jumps, plus 22 through the jump `0x0017E7D0`. These are
calls to functions that do nothing in this build, not guard checks: a direct call never consults the
check slot. A body that "calls `0x0016D6A0`" does nothing at that point.

### Stack cookies

The cookie is the qword at `0x01F44830`, named by the load configuration's `SecurityCookie` field. On disk
it holds `0x00002B992DDFA232`. The entry point `0x00808EE4` calls `__security_init_cookie` (`0x00809B8C`)
before anything else, then jumps to the runtime start-up `0x00808D78`.

1. If the cookie still holds the on-disk value (`0x00809BAF`), it builds a new one: the system time
   (`GetSystemTimeAsFileTime`) xor the thread id xor the process id xor
   `(counter.high << 32) xor counter` from `QueryPerformanceCounter` xor the address of a stack local,
   masked to 48 bits; a result equal to the on-disk value becomes `0x00002B992DDFA233`. It is stored at
   `0x00809C1C`, the cookie's only writer.
2. In both cases the complement of the cookie is stored at `0x01F44838` (`0x00809C2B`).

A protected function stores `cookie xor rsp` in its frame and, before returning, passes it back to
`__security_check_cookie` (`0x00808C40`). The check compares it with the cookie (`0x00808C40`), then rotates
the value left 16 bits and requires the low 16 bits of the result, the cookie's unused top bits, to be
zero (`0x00808C4A`). On either failure it jumps to `__report_gsfailure` (`0x00809654`), restoring the value
first on the second path (`0x00808C58`).

`__report_gsfailure` asks `IsProcessorFeaturePresent(23)` and, when fast fail is available, executes
`int 0x29` with code 2 (`0x00809670`): the process ends with no exception raised. Otherwise it builds a
`0xC0000409` exception record and calls `0x00809620`, which first calls `SetUnhandledExceptionFilter(NULL)`
(`0x0080962B`), then `UnhandledExceptionFilter`, then `TerminateProcess(GetCurrentProcess(), 0xC0000409)`.
Either way the game's own crash filter never runs.

### Range-check failures

`__report_rangecheckfailure` (`0x00809728`) calls `0x0080973C` with code 8, which fast-fails the same way
(`int 0x29` at `0x00809758`) or takes the same filter-clearing fallback. The compiler emits a call to it
where an index into a fixed-size array could not be proved in range.

### Teardowns that end in the do-nothing body

185 functions are exactly `lea rcx, [a static]` followed by `jmp 0x0016D6A0`, 12 bytes each. Every one
is registered with `atexit` (`0x00808B90`), so each is the teardown of a static whose destructor is
empty; see [static initialisation and teardown](static-initialisation-and-teardown.md). 144 of them
belong to one structure, Phyre serialization's scalar-conversion tree:

- The lookup `0x0059A030(source, destination)` calls 144 registrars (`0x005850F0`–`0x00592770`, 383 bytes
  each) once, guarded by the byte `0x02CA9D91`, then walks the tree under the sentinel `0x01F2CDA0` for the
  `(source, destination)` key and returns the node's routine, or 0.
- Each registrar is a thread-safe local static (see [lazy statics](lazy-statics-and-one-time-init.md)):
  it fills one node (layout below), registers its 12-byte teardown, and inserts the node, rebalancing
  through `0x0067F700`.
- The twelve type descriptors are Phyre's `bool`, `PChar`, `PUInt8`, `PInt16`, `PUInt16`, `PInt32`,
  `PUInt32`, `PInt64`, `PUInt64`, `PUInt128`, `float` and `double`, each returned by its own accessor
  in `0x0062FF50`–`0x00630490`. Each of the 144 ordered pairs occurs once.
- `0x0059D2D0` stores the routine `0x0059A030` returns, and stores `0x0016D6A0` itself when there is none
  (`0x0059D3BD`), so an unsupported pair converts nothing.

The 144 nodes share 68 routines. Every routine takes `(source base, destination base, desc, context)`,
where `desc` holds the element count, the source stride, the destination stride and a byte that swaps
the two field offsets read from the context, and converts `count` elements, four per loop pass. The
pairing follows from the arithmetic:

- every conversion to an 8-bit integer is the one byte copy `0x00595C00` (20 pairs), to a 16-bit integer
  `0x00593980` (14), to a 32-bit integer `0x005939F0` (10);
- `0x00594EB0` converts `double` to `float` (`cvtpd2ps`) and `0x00594350` `float` to `double`
  (`cvtps2pd`);
- float to integer routines truncate (`cvttss2si`, `cvttsd2si`, 18 routines); integer to float routines
  use `cvtsi2ss`, `cvtsi2sd`, `cvtdq2ps` or `cvtdq2pd` (18 routines); 30 routines move integers only.

One of the other 41 tears down the event record `0x02D3E880`. Its initialiser `0x00165F80` zeroes the record
(`0x005CC8A0`) and registers `0x008B1B00`. `0x00677450` creates it: when `+0x00` is 0 it calls `0x005CD0A0`,
which stores a `CreateEventA` handle (auto-reset, initially unsignalled) at `+0x08` and sets `+0x10`
and `+0x00`. `0x00677520` closes it through `0x005CD6D0` (`CloseHandle`). The empty teardown never closes
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
| `+0x18` | `u64` | ImageBase | `0x00120000` |
| `+0x46` | `u16` | DllCharacteristics | `0x8120` |

IMAGE_LOAD_CONFIG_DIRECTORY64, 148 bytes at `0x01CEBE40`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x58` | `u64` | SecurityCookie | `0x01F44830` |
| `+0x70` | `u64` | GuardCFCheckFunctionPointer | `0x008C31C0` |
| `+0x78` | `u64` | GuardCFDispatchFunctionPointer | `0x008C31C8` |
| `+0x80` | `u64` | GuardCFFunctionTable | 0 |
| `+0x88` | `u64` | GuardCFFunctionCount | 0 |
| `+0x90` | `u32` | GuardFlags | `0x00000100` |

| Section | Address | Virtual size | Raw size | Access |
|---|---|---|---|---|
| `.text` | `0x00121000` | `0x07A0635` | `0x07A0800` | R-X |
| `.rdata` | `0x008C2000` | `0x152D7FC` | `0x152D800` | R-- |
| `.data` | `0x01DF0000` | `0x11A7530` | `0x018E400` | RW- |
| `.pdata` | `0x02F98000` | `0x0068A0C` | `0x0068C00` | R-- |
| `.rodata` | `0x03001000` | `0x00011C0` | `0x0001200` | R-- |
| `.gfids` | `0x03003000` | `0x0000030` | `0x0000200` | R-- |
| `.tls` | `0x03004000` | `0x0000009` | `0x0000200` | RW- |
| `_RDATA` | `0x03005000` | `0x000A250` | `0x000A400` | R-- |
| `.rsrc` | `0x03010000` | `0x004B830` | `0x004BA00` | R-- |
| `.reloc` | `0x0305C000` | `0x0039360` | `0x0039400` | R-- |

Scalar-conversion tree node, `0x30` bytes, guard dword at `+0x30` (`0x02CAAD10`..0x02CACC58):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u64` | link0 | self-linked until inserted |
| `+0x08` | `u64` | link1 |  |
| `+0x10` | `u64` | parent | low bit is the node colour |
| `+0x18` | `u64` | source | type descriptor (lookup key, first) |
| `+0x20` | `u64` | destination | type descriptor (lookup key, second) |
| `+0x28` | `u64` | routine | conversion routine |

Event record `0x02D3E880`, `0x28` bytes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` | created |  |
| `+0x08` | `u64` | handle | CreateEventA result |
| `+0x10` | `u8` | flag | set by `0x005CD0A0`, cleared by `0x005CD6D0` |
| `+0x18` | `u32` |  | (zeroed by `0x005CC8A0`) |
| `+0x20` | `u32` |  | (zeroed by `0x005CC8A0`) |
| `+0x24` | `u32` |  | (zeroed by `0x005CC8A0`) |

## Shipped data

| Fact | Value |
|---|---|
| image base | `0x00120000`; entry point RVA `0x6E8EE4` (`0x00808EE4`) |
| `DllCharacteristics` | `0x8120`: `HIGH_ENTROPY_VA`, `NX_COMPAT`, `TERMINAL_SERVER_AWARE` |
| file `Characteristics` | `0x0022`; relocations shipped, `0x39360` bytes |
| `GuardFlags` | `0x00000100`; guard function table 0, count 0 |
| cookie on disk | `0x00002B992DDFA232` at `0x01F44830` |
| cookie checks | 2,390 call sites of `0x00808C40` in 2,209 functions |
| cookie reads | 2,216, one per function: 2,208 prologue loads in functions that call the check, plus runtime code |
| range-check calls | 237 call sites of `0x00809728` in 114 functions |
| calls to `0x0016D6A0` | 2,528 calls and 340 jumps direct, 22 more through `0x0017E7D0` |
| `ret 0` teardowns | 185, all `atexit`-registered; 144 scalar-conversion nodes, 41 others |
| `.gfids` | 12 dwords, 48 bytes, referenced by nothing |
| `VC_FEATURE` | 1,296 objects; 1,265 `/GS`, 89 `/sdl`, 49 guard-aware |

Function counts follow the image's `.pdata` entries, each chained entry folded into its primary.

The member lists beside this page:

- [`image-hardening-guard-adapter-registrars.tsv`](image-hardening-guard-adapter-registrars.tsv): the 145 empty teardowns registered by the
  scalar-conversion registrars and by `0x00165F80`, with the static each tears down, its registrar and the
  registrar's descriptor pair and routine.
- [`image-hardening-scalar-conversion-registrars.tsv`](image-hardening-scalar-conversion-registrars.tsv): the scalar-conversion registrars.
- [`image-hardening-guard-cf-dispatch-target.tsv`](image-hardening-guard-cf-dispatch-target.tsv): the dispatch target `0x00896270`.

## State

### The scalar-conversion tree

The 144 nodes lie at `0x02CAAD10`-`0x02CACC58`, `0x38` bytes apart: the `0x30`-byte node, then its registrar's
guard. The tree's header is the sentinel `0x01F2CDA0`. Its `+0x18`, `0x01F2CDB8`, holds the root and is the root's
parent. The header's six qwords hold `0x01F2CDA0` on disk, so the tree starts empty.

`0x0059A030` calls the registrars in the order of their nodes' addresses, and the `(source, destination)` keys rise
in that order. Each registrar does the following (sites of `0x005850F0`; every registrar has them at the same
offsets):

1. Inside its guarded block it stores the node's address in `+0x00`, `+0x08` and `+0x10` (`0x0058515C`-`0x0058516A`),
   the source and destination descriptors with one 16-byte store (`0x00585176`) and the routine (`0x00585184`).
2. On every call it sets bit `0x1` of `+0x10` (`0x005851BC`) and points `+0x00` and `+0x08` at the sentinel
   (`0x005851CA`, `0x005851D1`).
3. It walks down from the root comparing the source, then the destination, as unsigned values: a smaller key
   follows `+0x00`, a larger one `+0x08` (`0x00585203`-`0x0058522F`). An equal key ends the call (`0x0058523A`).
4. Otherwise it stores the last node it visited, with bit `0x1` set, in its own `+0x10` (`0x0058524B`), stores itself in
   that node's `+0x00` or `+0x08`, or in `0x01F2CDB8` when the tree is empty (`0x00585255`), and calls
   `0x0067F700(0x01F2CDA0, node)` (`0x0058525F`).

`0x0067F700` rebalances while the parent's bit `0x1` is set (`0x0067F718`, `0x0067F9A4`) and clears the root's bit `0x1` before
it returns (`0x0067F9C2`). Bit `0x1` set marks a red node and clear a black one: the tree is a red-black tree. Because
the keys arrive in rising order, every insert walks through `+0x08` only, and step 4 stores into a `+0x08`;
during the build a node's `+0x00` changes after step 2 only in `0x0067F700`'s rotations (`0x0067F984`).

After all 144 inserts the root is `0x02CAB3D8` (`PUInt8` to `PUInt64`, routine `0x00592E30`). 8 nodes are red and 136
black, 72 have no child, and every path from the root to the sentinel passes 6 black nodes.

`0x0059FE20`, the `PSerialization` module's shutdown (slot 2 of the vtable `0x00D26C40`, which `0x00160320` installs in `0x01F2CD80`
at `0x0016036A`; before that, and again after `0x008A8CE0`, `0x01F2CD80` holds the base vtable `0x00D26BC0`, whose slot 2 is
the stub `0x005C5230`), calls
`0x0067F580(0x01F2CDA0)` (`0x0059FF08`). It removes every node, rebalancing through `0x0067F9D0`, and leaves each one
pointing at itself in `+0x00`, `+0x08` and `+0x10` (`0x0067F69D`-`0x0067F6A4`, `0x0067F6BB`-`0x0067F6C2`). It then clears
the byte `0x02CA9D91` (`0x0059FF0D`), so the next call of `0x0059A030` runs the 144 registrars again.

On that second run every guard is already set, so each registrar runs steps 2 to 4 only, and the tree is rebuilt
with the same shape. The exit teardown `0x008A81D0`, which `0x00160310` registers with `atexit`, calls
`0x0067F580(0x01F2CDA0)` twice (`0x008A81E4`, `0x008A81F1`).

`0x0059A030` reads `+0x18` (`0x0059A340`), `+0x20` (`0x0059A34E`) and `+0x00` or `+0x08` (`0x0059A36C`) of each node on its
search path, and `+0x28` of the node it finds (`0x0059A388`). No other function reads or writes a node.

Besides the 144
empty teardown adapters `0x008A83E0` + k x `0x10`, each a `lea` of its node and a `jmp` to the `ret` at `0x0016D6A0`, only the
registrars name a node by a RIP-relative reference; no image-base-relative or disp32 reference and no data qword
names one. Only the registrars, `0x0059A030`, `0x0059FE20` and `0x008A81D0` name the header, and `0x0067F700`, `0x0067F580`
and `0x0067F9D0` reach the nodes from it.

The table gives the six fields of every node. Each row of
[image-hardening-state.tsv](image-hardening-state.tsv) is one field of one node, with its registrar and
conversion pair, its value once the 144 inserts are done, and its own writers and readers by instruction.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `+0x00` of each node (144 rows of the table) | `void*` | 0 (zero-filled tail of `.data`) | link0: the child whose key is smaller, `0x01F2CDA0` when there is none; the node's own address from step 1 until step 2, and again after `0x0067F580` removes it | the node's registrar (steps 1 and 2); `0x0067F700` (`0x0067F984`); `0x0067F580` and `0x0067F9D0`, from `0x0059FE20` and `0x008A81D0` | `0x0059A030` (`0x0059A36C`); `0x0067F580`, `0x0067F700` and `0x0067F9D0` |
| `+0x08` of each node (144 rows) | `void*` | 0 (zero-filled tail of `.data`) | link1: the child whose key is larger, `0x01F2CDA0` when there is none; the node's own address from step 1 until step 2, and again after `0x0067F580` removes it | the node's registrar (steps 1 and 2); the registrar of the node inserted beneath it (step 4, 143 nodes); `0x0067F700` (`0x0067F950`, `0x0067F980`); `0x0067F580` and `0x0067F9D0` | the walks of the registrars that run after it (step 3, 143 nodes); `0x0059A030` (`0x0059A36C`); `0x0067F580`, `0x0067F700` and `0x0067F9D0` |
| `+0x10` of each node (144 rows) | `void*` | 0 (zero-filled tail of `.data`) | parent, low bit the node colour (set red, clear black); `0x01F2CDB8` for the root; the node's own address before step 2 and after `0x0067F580` removes it | the node's registrar (steps 1, 2 and 4); `0x0067F700`, `0x0067F580` and `0x0067F9D0` | the node's registrar (step 2); `0x0067F580`, `0x0067F700` and `0x0067F9D0` |
| `+0x18` of each node (144 rows) | `void*` | 0 (zero-filled tail of `.data`) | source: type descriptor (lookup key, first), one of the twelve | the node's registrar (step 1, the 16-byte store) | the node's registrar (step 3, except the first, `0x00592770`, which finds the tree empty); the walks of the registrars that run after it; `0x0059A030` (`0x0059A340`) |
| `+0x20` of each node (144 rows) | `void*` | 0 (zero-filled tail of `.data`) | destination: type descriptor (lookup key, second), one of the twelve | the node's registrar (step 1, the 16-byte store) | the node's registrar (step 3, except `0x00592770`); the walks of the registrars that run after it when the sources are equal; `0x0059A030` (`0x0059A34E`) |
| `+0x28` of each node (144 rows) | `void*` | 0 (zero-filled tail of `.data`) | routine: the conversion routine, one of the 68 | the node's registrar (step 1) | `0x0059A030` (`0x0059A388`) only |

### The failure record

When `IsProcessorFeaturePresent(23)` reports no fast fail, `__report_gsfailure` (`0x00809654`) and `0x0080973C` fill an
exception record at `0x02EAED90` and a context record at `0x02EAEE30` (`0x4D0` bytes, up to `0x02EAF300`). They pass
`0x01CC72D0`, the read-only pair `0x02EAED90`, `0x02EAEE30`, to `0x00809620` (`0x0080971B`, `0x008097CD`), which passes it to
`UnhandledExceptionFilter` (`0x00809634`).

1. The context is captured with `RtlCaptureContext` and unwound with `RtlVirtualUnwind`: up to two frames by `0x00809848`
   for `0x00809654` (`0x00809679`), one by `0x008097D8` for `0x0080973C` (`0x00809761`). Each reads `Rip` (`+0xF8`) to find
   the frame's unwind entry (`0x00809859`, `0x008097EB`).
2. Each reporter then stores its return address in `Rip` (`0x00809683`, `0x0080976B`) and the address just above it in
   `Rsp` (`0x00809693`, `0x0080977B`). `0x00809654` is reached by the jump at `0x00808C5C`, so its return address is the
   one the failing function's call to `0x00808C40` pushed; `0x0080973C`'s is always `0x00809736`.
3. `0x00809654` also stores the value it was passed, the failed `cookie xor rsp`, in `Rcx` (`+0x80`, `0x008096AD`).
4. Each copies `Rip` into `ExceptionAddress` (`0x0080969A`, `0x00809782`) and stores the code `0xC0000409`, flags 1 and
   one parameter: 2 from `0x00809654` (`0x008096E2`), the argument from `0x0080973C` (`0x008097C2`), which is 8 from its only
   caller `0x00809728`.

No instruction in the image reads any other field of either record. No RIP-relative, image-base-relative or
disp32 reference names an address in `0x02EAED90`-`0x02EAF2FF` outside `0x00809654` and `0x0080973C`, and the only data
qwords that point into it are the pair at `0x01CC72D0`.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02EAED90` | `u32` | 0 (zero-filled tail of `.data`) | exception record `+0x00`, the code: `0xC0000409` | `0x00809654` (`0x008096B4`), `0x0080973C` (`0x00809790`) | `UnhandledExceptionFilter` through `0x01CC72D0`; no instruction in the image |
| `0x02EAED94` | `u32` | 0 (zero-filled tail of `.data`) | exception record `+0x04`, the flags: 1 | `0x00809654` (`0x008096BE`), `0x0080973C` (`0x0080979A`) | `UnhandledExceptionFilter` through `0x01CC72D0`; no instruction in the image |
| `0x02EAEDA0` | `void*` | 0 (zero-filled tail of `.data`) | exception record `+0x10`, the exception address: the reporter's return address, copied from `0x02EAEF28` | `0x00809654` (`0x008096A1`), `0x0080973C` (`0x00809789`) | `UnhandledExceptionFilter` through `0x01CC72D0`; no instruction in the image |
| `0x02EAEDA8` | `u32` | 0 (zero-filled tail of `.data`) | exception record `+0x18`, the parameter count: 1 | `0x00809654` (`0x008096C8`), `0x0080973C` (`0x008097A4`) | `UnhandledExceptionFilter` through `0x01CC72D0`; no instruction in the image |
| `0x02EAEDB0` | `u64` | 0 (zero-filled tail of `.data`) | exception record `+0x20`, the first parameter: the fast-fail code, 2 for a cookie failure, 8 for a range-check failure | `0x00809654` (`0x008096E2`), `0x0080973C` (`0x008097C2`) | `UnhandledExceptionFilter` through `0x01CC72D0`; no instruction in the image |
| `0x02EAEEB0` | `u64` | 0 (zero-filled tail of `.data`) | context record `+0x80`, `Rcx`: for a cookie failure the failed `cookie xor rsp`; for a range-check failure the captured value | `RtlCaptureContext` and `RtlVirtualUnwind` (step 1); `0x00809654` (`0x008096AD`) | `UnhandledExceptionFilter` through `0x01CC72D0`; no instruction in the image |
| `0x02EAEEC8` | `void*` | 0 (zero-filled tail of `.data`) | context record `+0x98`, `Rsp`: the address just above the reporter's return address | `RtlCaptureContext` and `RtlVirtualUnwind` (step 1); `0x00809654` (`0x00809693`), `0x0080973C` (`0x0080977B`) | `UnhandledExceptionFilter` through `0x01CC72D0`; no instruction in the image |
| `0x02EAEF28` | `void*` | 0 (zero-filled tail of `.data`) | context record `+0xF8`, `Rip`: the reporter's return address | `RtlCaptureContext` and `RtlVirtualUnwind` (step 1); `0x00809654` (`0x00809683`), `0x0080973C` (`0x0080976B`) | `0x00809848` (`0x00809859`), `0x008097D8` (`0x008097EB`), `0x00809654` (`0x0080969A`), `0x0080973C` (`0x00809782`); `UnhandledExceptionFilter` through `0x01CC72D0` |

### The runtime's own fast fail

`0x0080996C(code)` is the C runtime start-up's fast fail. It is called with 5 from `0x00808988` (`0x00808A4B`) and with 7
from `0x00808C90` (`0x00808D3A`, `0x00808D45`), `0x00808D78` (`0x00808D95`, `0x00808DBA`) and `0x00809124` (`0x00809231`,
`0x0080923C`).

1. When `IsProcessorFeaturePresent(23)` reports fast fail it executes `int 0x29` with the code (`0x00809993`).
2. Otherwise it clears the dword `0x02EAF300` (`0x00809995`), captures and unwinds a context on its stack and builds an
   exception record with code `0x40000015` and flags 1 there (`0x00809A50`, `0x00809A58`).
3. It calls `IsDebuggerPresent` (`0x00809A60`), `SetUnhandledExceptionFilter(NULL)` (`0x00809A81`) and
   `UnhandledExceptionFilter` (`0x00809A8C`).
4. When that returns 0 it ands `0x02EAF300` with 0, or with -1 when `IsDebuggerPresent` returned 1 (`0x00809A9A`). It
   then returns (`0x00809AB0`).

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02EAF300` | `u32` | 0 (zero-filled tail of `.data`) | a dword that holds 0 at every point: `0x0080996C` clears it and its one other access ands it with 0 or -1 | `0x0080996C` (`0x00809995`, `0x00809A9A`) | `0x0080996C` (`0x00809A9A`, the read of the `and`) only |

## Modding notes

- Addresses are fixed: no rebasing layer is needed, and the live cookie can be read at `0x01F44830`.
- Indirect calls are not validated. A vtable slot or callback pointer can be redirected, and a corrupt
  one is followed without any check.
- DEP is requested: allocate executable memory or change page protection before running injected code.
- A hook that grows or moves a protected frame must keep its cookie slot intact, and nothing may write
  `0x01F44830` after start-up; every protected function live at that moment would fail its check on
  return. The failure cannot be caught by a structured or vectored exception handler.
- Setting `GUARD_CF` or wiring `.gfids` would switch Control Flow Guard on with no valid-target table,
  and every indirect call would fail.

## Related

- [Static initialisation and teardown](static-initialisation-and-teardown.md): the `atexit` registrations
  the empty teardowns belong to.
- [Lazy statics and one-time initialisation](lazy-statics-and-one-time-init.md): the guard the
  scalar-conversion registrars use.
- [Object construction and destruction](object-construction-and-destruction.md): the deleting
  destructors whose sized-delete branch ends in `0x0016D6A0`.
- [`runtime-services.md`](runtime-services.md): the imported Windows and runtime functions.
- [Class hierarchy](../Engine-Core/class-hierarchy.md): the RTTI that names the classes.
