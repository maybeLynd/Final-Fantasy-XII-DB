---
title: "Static initialisation and teardown: the start-up order, the C and C++ initialiser tables, atexit registration and the quit path"
kind: "system"
category: "Compiler and C runtime"
addresses: "0x00808EE4, 0x00808D78, 0x02EAECF8, 0x008C5680, 0x008C56A0, 0x008C31D0, 0x008C5678, 0x00808C90, 0x00808D4C, 0x00809124, 0x00808D5C, 0x00808B90, 0x00808B40, 0x00808988, 0x02EAED08, 0x02EAED20, 0x007A3770, 0x007980A0, 0x0079887F, 0x005A0840, 0x005A08E0, 0x00879570, 0x00876C80, 0x008768A0, 0x005DC6F0, 0x005FDCB0, 0x001EDF00, 0x006E0220, 0x00616210, 0x00662C00, 0x008C56B0, 0x02EAED3C"
---

## What the player sees

Nothing directly: this runs between launching the game and its first window. It decides what exists
when: every global object below exists before the game's own code starts, and none of their teardowns
runs when the player quits from the menu.

## How it works

### Start-up order

The PE entry point is `0x00808EE4`. Everything before the game's `WinMain` happens in this order:

1. `0x00808EE4` calls `__security_init_cookie` (`0x00809B8C`), then jumps to the start-up routine `0x00808D78`.
2. `0x00808D78` initialises the runtime (`0x0080893C`) and takes the start-up lock (`0x00808900`).
3. It reads the start-up state `0x02EAECF8`. A value of 1 (start-up already running) fast-fails with code
   7 (`0x00808DB5`); a value of 0 is set to 1 (`0x00808DC3`).
4. It runs the C table through `_initterm_e` (`0x00808DDB`). A non-zero result ends start-up with exit
   code `0xFF` (`0x00808DE4`).
5. It runs the C++ table through `_initterm` (`0x00808DFC`), which returns nothing to test, and sets the
   state to 2 (`0x00808E01`).
6. It releases the lock, checks two dynamic-TLS callback slots (`0x00809C78`, `0x00809C80`, both null in
   the image), fetches the command line and calls `0x007A3770` with the image base `0x00120000`
   (`0x00808E8A`).

`0x007A3770` is `WinMain`: it calls `IsDebuggerPresent` and then the game's main routine `0x007980A0` on
both arms. When `WinMain` returns, the start-up routine calls the runtime's `exit` (`0x00808E9C`).

### The C table

`_initterm_e` walks `0x008C5680`–`0x008C56A0`. The first and last qwords are null; the three entries
between are runtime set-up:

- `0x00808C90` sets the application type and file modes, initialises the module's exit tables
  (`0x00808988`), registers `0x00809CD4` with `atexit`, and prepares the command line and environment.
- `0x00808D4C` sets `0x4` in the stdio option word returned by `0x0016D670` and `0x2` in the one returned
  by `0x0018A320`.
- `0x00809124` creates the lock and the condition variable or event behind thread-safe local statics,
  and registers `0x00809244` to delete them; see
  [lazy statics](lazy-statics-and-one-time-init.md).

### The C++ table

`_initterm` walks `0x008C31D0`–`0x008C5678`. Both bounds are null qwords; the 1,172 entries run from
`0x008C31D8` to `0x008C5670` and every one is non-null and distinct. The linker's own contribution record
names the parts: `.CRT$XCAA` holds `0x00808D5C` (it installs the runtime's unhandled-exception filter
`0x00809B54` and sets the new-handler mode), `.CRT$XCL` holds `0x0016A290` and `0x0016A29C`, and `.CRT$XCU`
holds the other 1,169. The order is link order, not address order: 593 of the 1,171 steps go upward.
Initialisers from one source file sit together.

The pre-terminator and terminator tables (`.CRT$XP*`, `.CRT$XT*` at `0x008C56B8`–`0x008C56E0`) hold only
nulls.

### What the C++ initialisers build

Every entry, grouped by the first function it calls:

| Entries | Callee | What is built |
|---:|---|---|
| 143 | `0x00879570` | a `Phyre::PInputs::PInputChannelSemantic` named `Key_…`, `Button_…` and so on, added to a name registry |
| 97 | `0x00876C80` | a `PInputKeySemantic`, same registry form |
| 44 | `0x008768A0` | a `PInputJoypadButtonSemantic` ([Phyre input semantics](../Controls-And-Input/phyre-input-semantics.md)) |
| 25 | `0x008760A0` | a `PInputTypeSemantic` (`Key`, `JoypadButton`, `JoypadAxis`, `MouseButton`, …; [Phyre input semantics](../Controls-And-Input/phyre-input-semantics.md)) |
| 10 | `0x00876490` | a `PInputAxisSemantic` (`XAxis_0`, `YAxis_0`, …; [Phyre input semantics](../Controls-And-Input/phyre-input-semantics.md)) |
| 60 | `0x005DC6F0` | a named render-pass record (`VideoScreen`, `MapShadowRender`, `OpaqueDepth`, …), linked through `0x005FDCB0` |
| 56 | `0x005FDCB0` | another record added directly to that render-pass list |
| 64 | `0x001EDF00` | an EASTL allocator (`eastl::allocator_memory_log`) with its name, such as `EASTL basic_string` |
| 69 | `0x006E0220` | one float constant converted to half precision and stored; no teardown |
| 35 | `0x00616210` | a named texture-format record (`L8`, `A8`, `LA8`, `RG8`, …) |
| 28 | `0x00662C00` | a named vertex-format record (`ScreenVertex`, `WorldVertex`, …) |
| 9 | `0x006D58D0` | a named morph record (`Morph22`, `Morph23`, …) |
| 75 | none | inline stores, then a teardown registration (among them the SQEX sound driver's fixed lists and queues) |
| 31 | none | only `lea rcx, [teardown]; jmp atexit`: a static with no constructor work |
| 7 | none | no calls: four copy 16-byte prototype blocks into live globals with `movaps` (`0x0015BD30`, `0x0015BF20` and `0x0015C0D0` from `0x01DF0980`–`0x01DF0A80`, `0x0015C280` partly from `0x01F800F0`), `0x00168C10` zeroes five qwords at `0x02EA1960`, `0x0016A270` stores `0.9 / sqrt(16.0)` = 0.225 at `0x02EADEF0` (`sqrtss`, `divss`, `0x0016A270`-`0x0016A284`), `0x001610B0` zeroes eight 16-byte slots |
| 419 | others | 362 further first callees, none used by more than 11 entries |

The registry inserts share one shape: the routine refuses an object whose name pointer is null
(returns `0x11`) or whose name is already present (returns `0x12`), and otherwise pushes the object onto
a singly linked list headed by a global (`0x00879570` uses `0x02EB9D80`, `0x00876C80` `0x02EB83B8`, `0x008768A0`
`0x02EB8348`, and the render-pass insert `0x005FDCB0` uses `0x02CBF998`).

1,084 entries register a teardown, each exactly one; 88 register none. None of them takes a
thread-safe local-static guard.

### Teardown registration

Every registration in the image goes through `atexit` (`0x00808B90`), which calls `_onexit`
(`0x00808B40`) and turns its result into 0 or -1.

- `0x00808C90` calls `0x00808988` with 1 (an executable), which fills the module's two exit tables
  `0x02EAED08` and `0x02EAED20` with the encoded value -1 instead of initialising them.
- `_onexit` decodes the first qword of `0x02EAED08` (`ror64(cookie xor value, cookie & 0x3F)`, cookie
  `0x01F44830`); it is -1, so it hands the function to the runtime's `_crt_atexit` (`0x00808B68`), and the
  `_register_onexit_function` path at `0x00808B79` is never taken.

All teardowns therefore sit in the runtime's own process table, which its `exit` runs last-registered
first.

| Registrations | Where |
|---:|---|
| 1,084 | C++ initialisers |
| 1,541 | functions holding thread-safe local statics, inside the guarded block |
| 2 | `0x00159340`, one critical-section static at `0x02EAEA70` built behind bit `0x1` of the plain flag word `0x02EAEA98`, its accessor inlined twice; both register the teardown `0x008B9040` (`0x00159384`, `0x001593F1`), which stores `0x01CC6B60` at `0x02EAEA68` and hands `0x02EAEA70` to the import at `0x008C20D0` |
| 1 | `0x005A08E0`, the engine set-up, registering the engine shutdown `0x005A0840` |
| 2 | the runtime's own `0x00808C90` and `0x00809124` |

Library initialisers register theirs the same way: the Bullet initialiser `0x00859D20` builds the static at `0x02EAF400`
(`0x00852E10`) and registers `0x008B90A0` (`0x00859D95`), which puts back the vtable `0x01CCF348`, releases the buffer
`[0x02EAF620]` through `0x0085E710` when it is set and `0x02EAF628` is set, clears both fields and runs `0x00839FD0` on the
object.

That is 2,630 call sites (1,574 calls and 1,056 tail jumps) for about 2,560 distinct teardown functions,
counting the `lea rcx` that sets the argument within the 64 bytes before each site.
Teardowns registered by lazy statics join the table when their static is first built, so their order
depends on what ran first.

### Teardown shapes

- 1,296 are two instructions, `lea rcx, [object]; jmp destructor`; 185 of them jump to the `ret 0` at
  `0x0016D6A0` and do nothing (see [image hardening](image-hardening.md)).
- 405 more are short tail jumps of up to four instructions.
- 224, nearly all 82 bytes, are list unlinks registered by lazy statics: they splice a node out of an intrusive
  doubly linked list, point the node at itself, and free `+0x18` through `0x00584730` only when bit 0 of
  `+0x20` is set (`0x008A8D40`).
- 327 are 95-byte registry unlinks registered by C++ initialisers: they store the base vtable back
  into the object and remove it from a singly linked registry list by its `+0x10` link (`0x008B76B0`,
  list `0x02EA06D8`).
- The rest destroy their object inline.

### The normal quit does not run the teardowns

`0x007980A0` runs the game's message loop until it receives `WM_QUIT` (`0x12`). It then calls `0x0061C540`,
`0x005FE190` and the engine shutdown `0x005A0840`, closes its handles, frees its argument list, optionally
relaunches the executable with `CreateProcessA`, and calls `ExitProcess(0)` at `0x0079887F`. It does not
return to `WinMain`, so the runtime's `exit` at `0x00808E9C` and the teardown table are not reached on
that path. `0x005A0840` is guarded by the byte `0x02CACCA0`, which `0x005A08E0` sets when it registers the same
routine with `atexit`, so the shutdown runs once on either path.

### TLS: storage, no callbacks

The TLS directory (`0x01CEBED8`, 40 bytes) gives raw data `0x03004000`–`0x03004008`, the index `0x02EAED3C` and
the callback array `0x008C56B0`, whose first qword is null. Nothing runs from TLS callbacks before the
entry point. The TLS block itself is used: the thread-safe local statics keep each thread's epoch at
`+0x04`.

## Layouts

```
initialiser tables (.rdata), qwords
  0x008C31D0          null              __xc_a
  0x008C31D8          0x00808D5C          .CRT$XCAA
  0x008C31E0..31E8    0x0016A290 0x0016A29C .CRT$XCL
  0x008C31F0..5670    1,169 entries     .CRT$XCU
  0x008C5678          null              __xc_z
  0x008C5680          null              __xi_a
  0x008C5688..5698    0x00808C90 0x00808D4C 0x00809124
  0x008C56A0          null              __xi_z
  0x008C56B8..56E0    nulls only        .CRT$XP*, .CRT$XT*

start-up state 0x02EAECF8 (u32)
  0  not started   1  initialisers running   2  initialisers done

module exit tables (encoded qwords, each set to encode(-1) by 0x00808988)
  0x02EAED08  first, last, end    atexit table
  0x02EAED20  first, last, end    at_quick_exit table

IMAGE_TLS_DIRECTORY64 at 0x01CEBED8
  +0x00  u64  StartAddressOfRawData   0x03004000
  +0x08  u64  EndAddressOfRawData     0x03004008
  +0x10  u64  AddressOfIndex          0x02EAED3C
  +0x18  u64  AddressOfCallBacks      0x008C56B0   first entry null
  +0x20  u32  SizeOfZeroFill          0
```

## Shipped data

| Fact | Value |
|---|---|
| C table | 3 entries between nulls at `0x008C5680` and `0x008C56A0` |
| C++ table | 1,172 entries, `0x008C31D8`–`0x008C5670`, between nulls at `0x008C31D0` and `0x008C5678` |
| table order | 593 of 1,171 steps ascending |
| C++ entries registering a teardown | 1,084 |
| `atexit` sites | 2,630: 1,574 calls, 1,056 tail jumps |
| distinct teardowns | about 2,560, by the `lea rcx` within the 64 bytes before each site |
| TLS callbacks | none |

Counts come from disassembling every C++ entry and every `atexit` site; a site's teardown is the
`lea rcx` within the 64 bytes before it (about 35 sites set `rcx` some other way and are counted as sites only).

The member lists beside this page, each named `static-initialisation-and-teardown-<list>.tsv` with a
function address in its first column:

| List | Members |
|---|---|
| `msvc-dynamic-initialiser-stubs` | 43 C++ entries of 32 bytes: call a constructor, then tail-jump `atexit` |
| `atexit-teardown-registration-stubs` | 30 C++ entries of 12 bytes that only register a teardown |
| `float32-to-float16-static-initialisers` | 69 C++ entries of 29 bytes calling `0x006E0220` |
| `record-ctor-0x00616210-initialisers` | 33 C++ entries (texture-format records) |
| `record-ctor-0x00662c00-initialisers` | 28 C++ entries (vertex-format records) |
| `record-ctor-0x006d58d0-initialisers` | 9 C++ entries (morph records) |
| `counter-append-initialisers` | 19 C++ entries, `0x00160BF0` to `0x00161070` at a 0x40 stride, that append the static to a counted pointer table |
| `zeroinit-record-initialisers`, `zeroinit-3q-initialisers` | 16 and 3 C++ entries that zero a record |
| `alloc-record-0x0067ffb0-initialisers`, `grow-helper-initialisers` | 8 and 6 C++ entries |
| `ctor-0x00808fe4-initialisers` | 5 C++ entries that construct an array through `0x00808FE4`; `0x00162B30` passes the element constructor `0x005DC890`, which stores `0x34460000` and zeroes two qwords, for 23 elements of `0x18` bytes at `0x02CB7DA0` |
| `ctor-0x0060df70-initialisers` | 2 C++ entries |
| `callback-record-0x006155b0-registrars` | 6 C++ entries that tail-jump `0x006155B0` with three code pointers |
| `xc-initializer-leftovers` | 83 C++ entries, each of its own form |
| `empty-dtor-teardown-wrappers` | 145 of the 185 `ret 0` teardowns |
| `static-intrusive-list-teardowns`, `static-intrusive-list-teardown-owners` | the 224 list unlinks, and the class descriptor owning each list |
| `registry-unlink-teardowns` | the 327 registry unlinks |
| `xc-registered-library-teardowns`, `xc-registered-static-teardowns` | 190 and 107 teardowns that C++ entries register |
| `intrusive-list-node-teardowns-115b` | 43 list-clearing loops that release each node through its allocator's slot `+0x18` |
| `scalar-deleting-destructors-free`, `-shared-base`, `-inlined-dtor` | 65, 37 and 24 deleting destructors freeing through `0x00809950` |
| `two-deallocator-deleting-destructors` | 12 deleting destructors testing bits `0x1` and `0x4` |

The deleting-destructor idiom is on [object construction and destruction](object-construction-and-destruction.md).

## State

### The runtime's DLL flag

`0x0080893C`, the runtime set-up that the start-up routine calls first, takes the runtime's module type in `ecx`. It
sets the byte `0x02EAED38` to 1 only when that type is 0, the type of a DLL, and otherwise writes back the value it
read. The start-up routine passes 1 (`0x00808D82`), so the byte stays 0. The runtime clean-up `0x00808B14`, which the
start-up routine calls at `0x00808EAF` with `dl` 0, runs both of its clean-up steps when the byte is 0 or its second
argument is 0. Both steps are `0x0061ECF0`, which only returns 1.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02EAED38` | `u8` | 0 (zero-filled tail of `.data`) | 1 when the runtime was set up for a DLL; 0 in this executable | `0x0080893C` (`0x00808953`), its own value back | `0x0080893C` (`0x00808942`), `0x00808B14` (`0x00808B1A`) |

### The exit tables' end words

`0x00808988` fills each of the two exit tables with the encoded value -1. It stores first and last in one 16-byte
store, and the end word in its own 8-byte store. No instruction reads either end word.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02EAED18` | `u64` | 0 (zero-filled tail of `.data`) | end of the `atexit` table `0x02EAED08`, encoded -1 | `0x00808988` (`0x00808A1F`) | - |
| `0x02EAED30` | `u64` | 0 (zero-filled tail of `.data`) | end of the second exit table `0x02EAED20`, encoded -1 | `0x00808988` (`0x00808A33`) | - |

### Semantic registry heads

Two more registries have the insert shape described above: `0x00876490` for the 10 `PInputAxisSemantic` objects
and `0x00877060` for the 4 `PInputMouseButtonSemantic` objects. Each initialiser passes one static object, and the
insert puts it at the front, so after the C++ table has run each list starts with the object of the last
initialiser in table order.

The deleting destructor of each class and the teardown of each object unlink the object again. They walk the
list with a pointer that starts at the head, so their store writes the head when the object is first in the list.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02EB82D8` | `void*` | 0 (zero-filled tail of `.data`) | head of the `PInputAxisSemantic` registry, linked through `+0x10` and keyed by the name at `+0x08`; after the C++ table it is `Gyro` (`0x01F45008`), then `ZAxis_2`, `YAxis_2`, `XAxis_2`, `ZAxis_1`, `YAxis_1`, `XAxis_1`, `ZAxis_0`, `YAxis_0`, `XAxis_0` (`0x01F45128`) | `0x00876490` (`0x008764FA`), the inserted object; through the unlink pointer: `0x00876410` (`0x00876468`), `0x008BA2C0` (`0x008BA317`), `0x008BA320` (`0x008BA377`), `0x008BA380` (`0x008BA3D7`), `0x008BA3E0` (`0x008BA437`), `0x008BA440` (`0x008BA497`), `0x008BA4A0` (`0x008BA4F7`), `0x008BA500` (`0x008BA557`), `0x008BA560` (`0x008BA5B7`), `0x008BA5C0` (`0x008BA617`), `0x008BA620` (`0x008BA677`) | `0x00876410` (`0x0087642A`), `0x00876490` (`0x008764AD`), `0x00876520` (`0x00876532`), `0x00876590` (`0x0087659F`, `0x00876630`), `0x00876670` (`0x0087667B`), `0x008BA2C0` (`0x008BA2D5`), `0x008BA320` (`0x008BA335`), `0x008BA380` (`0x008BA395`), `0x008BA3E0` (`0x008BA3F5`), `0x008BA440` (`0x008BA455`), `0x008BA4A0` (`0x008BA4B5`), `0x008BA500` (`0x008BA515`), `0x008BA560` (`0x008BA575`), `0x008BA5C0` (`0x008BA5D5`), `0x008BA620` (`0x008BA635`) |
| `0x02EB8428` | `void*` | 0 (zero-filled tail of `.data`) | head of the `PInputMouseButtonSemantic` registry, same links; after the C++ table it is `Button_LeftMB` (`0x01F46328`), then `Button_MiddleMB` (`0x01F46308`), `Button_RightMB` (`0x01F46348`) and `Empty` (`0x01F462E8`) | `0x00877060` (`0x008770CA`), the inserted object; through the unlink pointer: `0x00876FE0` (`0x00877038`), `0x008BDB90` (`0x008BDBE7`), `0x008BDBF0` (`0x008BDC47`), `0x008BDC50` (`0x008BDCA7`), `0x008BDCB0` (`0x008BDD07`) | `0x00876FE0` (`0x00876FFA`), `0x00877060` (`0x0087707D`), `0x008770F0` (`0x00877102`), `0x00877160` (`0x0087716F`, `0x00877200`), `0x00877240` (`0x0087724B`), `0x008BDB90` (`0x008BDBA5`), `0x008BDBF0` (`0x008BDC05`), `0x008BDC50` (`0x008BDC65`), `0x008BDCB0` (`0x008BDCC5`) |

The other readers come in pairs with the same code, one per registry:

- `0x00876520` and `0x008770F0` store the object whose name matches their second argument through their first
  argument and return `0x13` when no object has the name;
- `0x00876590` and `0x00877160` count the list and copy the object pointers into the array they are passed. When the
  array's count already matches they reuse its buffer (`0x008765C5`); otherwise they give it a new buffer of that
  many pointers, freeing the old one when bit 31 of its count word is clear. They return 0, or `0xD` when the
  allocation fails;
- `0x00876670` and `0x00877240` return the object whose name matches, or 0.

### Half-precision constants

69 C++ initialisers each convert one float from `.rdata` with `0x006E0220` and store the 16-bit result in its own
global. They come in 23 sets of the same three values:

| Bits | Value | Source float | Meaning |
|---|---|---|---|
| `0x7BFF` | 65504 | `0x00D8F9CC` (`0x477FE000`) | the largest finite half |
| `0x1400` | 2^-10 = 0.0009765625 | `0x00D8F9C0` (`0x3A7FFFD5`) | the half epsilon, the gap between 1 and the next half |
| `0x0001` | 2^-24 | `0x00D5003C` (`0x33800000`) | the smallest positive half, a subnormal |

`0x3A7FFFD5` is just below 2^-10; `0x006E0220` adds `0x1000` to the mantissa before it shifts it right by 13, so the
result rounds up to `0x1400`. No instruction reads any of the 69 globals: no RIP-relative, image-base-relative or
disp32 reference other than its initialiser's store, and the loop-bound `lea` at `0x0072F206` for `0x02EA1A40`, names
one.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| each row of [static-initialisation-and-teardown-state.tsv](static-initialisation-and-teardown-state.tsv): `0x02EA0B50`-`0x02EA40D4` | `u16` | 0 (zero-filled tail of `.data`) | one of the three constants above (`value_bits`, `value`), with its source float, its initialiser and the table slot that holds it | the initialiser, once, before `WinMain` (`set_by`) | none (`read_by` `-`) |

### Statics only their teardown names

Two C++ initialisers do nothing but register a teardown: `0x00167310` (slot `0x008C43E0`) registers `0x008B5C40`, and
`0x00167320` (slot `0x008C4428`) registers `0x008B5CA0`. Each teardown destroys one static array of two words. It frees
the buffer through `0x00584730` only when bit 31 of the count word is clear and the buffer is set, then zeroes both
words. No other instruction names either array, so both stay 0 and the teardown frees nothing.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02E523F0` | `u32` | 0 (zero-filled tail of `.data`) | count word of the array that `0x008B5C40` destroys; stays 0 | `0x008B5C40` (`0x008B5C76`), 0 | `0x008B5C40` (`0x008B5C4D`) |
| `0x02E523F8` | `void*` | 0 (zero-filled tail of `.data`) | buffer of that array; stays 0 | `0x008B5C40` (`0x008B5C6F`), 0 | `0x008B5C40` (`0x008B5C5C`) |
| `0x02E56560` | `u32` | 0 (zero-filled tail of `.data`) | count word of the array that `0x008B5CA0` destroys; stays 0 | `0x008B5CA0` (`0x008B5CD6`), 0 | `0x008B5CA0` (`0x008B5CAD`) |
| `0x02E56568` | `void*` | 0 (zero-filled tail of `.data`) | buffer of that array; stays 0 | `0x008B5CA0` (`0x008B5CCF`), 0 | `0x008B5CA0` (`0x008B5CBC`) |

## Modding notes

- An injected DLL that attaches after the C++ table has run finds every global above already built.
  The start-up routine `0x00808D78`, after the cookie is set and before the first initialiser, is the
  earliest point at which none of them exists.
- The prototypes at `0x01DF0980`–`0x01DF0A80` lie in the file-backed part of `.data`, so the starting values
  `0x0015BD30`, `0x0015BF20` and `0x0015C0D0` copy can be changed in the file.
- Do not rely on a teardown to see an object die. On a normal quit none runs; on a path through the
  runtime's `exit` they run in reverse registration order after the game has stopped.
- A new global needs both halves: build it in an initialiser and register its teardown, or leave it
  unregistered and accept that it is never torn down.

## Related

- [Phyre input semantics](../Controls-And-Input/phyre-input-semantics.md): the semantic objects the input registrars
  `0x008760A0`, `0x00876490` and `0x008768A0` build.
- [Image hardening](image-hardening.md): the cookie set up before the tables run, and the `ret 0`
  teardowns.
- [Lazy statics and one-time initialisation](lazy-statics-and-one-time-init.md): the statics built on
  first use, which register 1,541 of the teardowns.
- [Object construction and destruction](object-construction-and-destruction.md): constructors,
  destructors and vtable installs.
- `runtime-services.md`: the runtime and Windows imports used here.
- [Startup constants](../Engine-Core/startup-constants.md): what the game's own start-up
  fixes after `WinMain` begins.
- [Controls](../Controls-And-Input/controls.md): the input manager that reads the semantics registered here.
