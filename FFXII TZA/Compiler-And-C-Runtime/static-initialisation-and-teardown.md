---
title: "Static initialisation and teardown: the start-up order, the C and C++ initialiser tables, atexit registration and the quit path"
kind: "system"
category: "Compiler and C runtime"
summary: "How FFXII_TZA.exe builds its global objects before WinMain and registers their teardowns: the entry point and runtime start-up routine, the three-entry C table and the 1,172-entry C++ table with their null bounds, what the C++ initialisers construct (Phyre input semantics, render-pass and format name registries, EASTL allocators, half-float constants), how atexit forwards every registration to the runtime's process table, the shapes of the 2,562 registered teardowns, why a normal quit never runs them, and the TLS directory without callbacks."
addresses: ["00808EE4", "00808D78", "02EAECF8", "008C5680", "008C56A0", "008C31D0", "008C5678", "00808C90", "00808D4C", "00809124", "00808D5C", "00808B90", "00808B40", "00808988", "02EAED08", "02EAED20", "007A3770", "007980A0", "0079887F", "005A0840", "005A08E0", "00879570", "00876C80", "008768A0", "005DC6F0", "005FDCB0", "001EDF00", "006E0220", "00616210", "00662C00", "008C56B0", "02EAED3C"]
---

# Static initialisation and teardown: the start-up order, the C and C++ initialiser tables, atexit registration and the quit path

## What the player sees

Nothing directly: this runs between launching the game and its first window. It decides what exists
when: every global object below exists before the game's own code starts, and none of their teardowns
runs when the player quits from the menu.

## How it works

### Start-up order

The PE entry point is `00808EE4`. Everything before the game's `WinMain` happens in this order:

1. `00808EE4` calls `__security_init_cookie` (`00809B8C`), then jumps to the start-up routine `00808D78`.
2. `00808D78` initialises the runtime (`0080893C`) and takes the start-up lock (`00808900`).
3. It reads the start-up state `02EAECF8`. A value of 1 (start-up already running) fast-fails with code
   7 (`00808DB5`); a value of 0 is set to 1 (`00808DC3`).
4. It runs the C table through `_initterm_e` (`00808DDB`). A non-zero result ends start-up with exit
   code `0xFF` (`00808DE4`).
5. It runs the C++ table through `_initterm` (`00808DFC`), which returns nothing to test, and sets the
   state to 2 (`00808E01`).
6. It releases the lock, checks two dynamic-TLS callback slots (`00809C78`, `00809C80`, both null in
   the image), fetches the command line and calls `007A3770` with the image base `0x00120000`
   (`00808E8A`).

`007A3770` is `WinMain`: it calls `IsDebuggerPresent` and then the game's main routine `007980A0` on
both arms. When `WinMain` returns, the start-up routine calls the runtime's `exit` (`00808E9C`).

### The C table

`_initterm_e` walks `008C5680`–`008C56A0`. The first and last qwords are null; the three entries
between are runtime set-up:

- `00808C90` sets the application type and file modes, initialises the module's exit tables
  (`00808988`), registers `00809CD4` with `atexit`, and prepares the command line and environment.
- `00808D4C` sets `0x4` in the stdio option word returned by `0016D670` and `0x2` in the one returned
  by `0018A320`.
- `00809124` creates the lock and the condition variable or event behind thread-safe local statics,
  and registers `00809244` to delete them; see
  [lazy statics](lazy-statics-and-one-time-init.md).

### The C++ table

`_initterm` walks `008C31D0`–`008C5678`. Both bounds are null qwords; the 1,172 entries run from
`008C31D8` to `008C5670` and every one is non-null and distinct. The linker's own contribution record
names the parts: `.CRT$XCAA` holds `00808D5C` (it installs the runtime's unhandled-exception filter
`00809B54` and sets the new-handler mode), `.CRT$XCL` holds `0016A290` and `0016A29C`, and `.CRT$XCU`
holds the other 1,169. The order is link order, not address order: 593 of the 1,171 steps go upward.
Initialisers from one source file sit together.

The pre-terminator and terminator tables (`.CRT$XP*`, `.CRT$XT*` at `008C56B8`–`008C56E0`) hold only
nulls.

### What the C++ initialisers build

Grouped by the first function each entry calls, from a census of every entry's body:

| Entries | Callee | What is built |
|---:|---|---|
| 143 | `00879570` | a `Phyre::PInputs::PInputChannelSemantic` named `Key_…`, `Button_…` and so on, added to a name registry |
| 97 | `00876C80` | a `PInputKeySemantic`, same registry form |
| 44 | `008768A0` | a `PInputJoypadButtonSemantic` |
| 25 | `008760A0` | a `PInputTypeSemantic` (`Key`, `JoypadButton`, `JoypadAxis`, `MouseButton`, …) |
| 10 | `00876490` | a `PInputAxisSemantic` (`XAxis_0`, `YAxis_0`, …) |
| 60 | `005DC6F0` | a named render-pass record (`VideoScreen`, `MapShadowRender`, `OpaqueDepth`, …), linked through `005FDCB0` |
| 56 | `005FDCB0` | another record added directly to that render-pass list |
| 64 | `001EDF00` | an EASTL allocator (`eastl::allocator_memory_log`) with its name, such as `EASTL basic_string` |
| 69 | `006E0220` | one float constant converted to half precision and stored; no teardown |
| 35 | `00616210` | a named texture-format record (`L8`, `A8`, `LA8`, `RG8`, …) |
| 28 | `00662C00` | a named vertex-format record (`ScreenVertex`, `WorldVertex`, …) |
| 9 | `006D58D0` | a named morph record (`Morph22`, `Morph23`, …) |
| 75 | none | inline stores, then a teardown registration (among them the SQEX sound driver's fixed lists and queues) |
| 31 | none | only `lea rcx, [teardown]; jmp atexit`: a static with no constructor work |
| 7 | none | no calls: four copy 16-byte prototype blocks into live globals with `movaps` (`0015BD30`, `0015BF20` and `0015C0D0` from `01DF0980`–`01DF0A80`, `0015C280` partly from `01F800F0`), `00168C10` zeroes five qwords at `02EA1960`, `0016A270` stores a constant divided by a square root at `02EADEF0`, `001610B0` zeroes eight 16-byte slots |
| 419 | others | 362 further first callees, none used by more than 11 entries |

The registry inserts share one shape: the routine refuses an object whose name pointer is null
(returns `0x11`) or whose name is already present (returns `0x12`), and otherwise pushes the object onto
a singly linked list headed by a global (`00879570` uses `02EB9D80`, `00876C80` `02EB83B8`, `008768A0`
`02EB8348`, and the render-pass insert `005FDCB0` uses `02CBF998`).

1,084 entries register a teardown, each exactly one; 88 register none. None of them takes a
thread-safe local-static guard.

### Teardown registration

Every registration in the image goes through `atexit` (`00808B90`), which calls `_onexit`
(`00808B40`) and turns its result into 0 or -1.

- `00808C90` calls `00808988` with 1 (an executable), which fills the module's two exit tables
  `02EAED08` and `02EAED20` with the encoded value -1 instead of initialising them.
- `_onexit` decodes the first qword of `02EAED08` (`ror64(cookie xor value, cookie & 0x3F)`, cookie
  `01F44830`); it is -1, so it hands the function to the runtime's `_crt_atexit` (`00808B68`), and the
  `_register_onexit_function` path at `00808B79` is never taken.

All teardowns therefore sit in the runtime's own process table, which its `exit` runs last-registered
first.

| Registrations | Where |
|---:|---|
| 1,084 | C++ initialisers |
| 1,541 | functions holding thread-safe local statics, inside the guarded block |
| 2 | `00159340`, one critical-section static at `02EAEA70` built behind bit `0x1` of the plain flag word `02EAEA98`, its accessor inlined twice |
| 1 | `005A08E0`, the engine set-up, registering the engine shutdown `005A0840` |
| 2 | the runtime's own `00808C90` and `00809124` |

That is 2,630 call sites (1,574 calls and 1,056 tail jumps) for about 2,560 distinct teardown functions,
counting the `lea rcx` that sets the argument within the 64 bytes before each site.
Teardowns registered by lazy statics join the table when their static is first built, so their order
depends on what ran first.

### Teardown shapes

- 1,296 are two instructions, `lea rcx, [object]; jmp destructor`; 185 of them jump to the `ret 0` at
  `0016D6A0` and do nothing (see [image hardening](image-hardening.md)).
- 405 more are short tail jumps of up to four instructions.
- 224, nearly all 82 bytes, are list unlinks registered by lazy statics: they splice a node out of an intrusive
  doubly linked list, point the node at itself, and free `+0x18` through `00584730` only when bit 0 of
  `+0x20` is set (`008A8D40`).
- 327 are 95-byte registry unlinks registered by C++ initialisers: they store the base vtable back
  into the object and remove it from a singly linked registry list by its `+0x10` link (`008B76B0`,
  list `02EA06D8`).
- The rest destroy their object inline.

### The normal quit does not run the teardowns

`007980A0` runs the game's message loop until it receives `WM_QUIT` (`0x12`). It then calls `0061C540`,
`005FE190` and the engine shutdown `005A0840`, closes its handles, frees its argument list, optionally
relaunches the executable with `CreateProcessA`, and calls `ExitProcess(0)` at `0079887F`. It does not
return to `WinMain`, so the runtime's `exit` at `00808E9C` and the teardown table are not reached on
that path. `005A0840` is guarded by the byte `02CACCA0`, which `005A08E0` sets when it registers the same
routine with `atexit`, so the shutdown runs once on either path.

### TLS: storage, no callbacks

The TLS directory (`01CEBED8`, 40 bytes) gives raw data `03004000`–`03004008`, the index `02EAED3C` and
the callback array `008C56B0`, whose first qword is null. Nothing runs from TLS callbacks before the
entry point. The TLS block itself is used: the thread-safe local statics keep each thread's epoch at
`+0x04`.

## Layouts

```
initialiser tables (.rdata), qwords
  008C31D0          null              __xc_a
  008C31D8          00808D5C          .CRT$XCAA
  008C31E0..31E8    0016A290 0016A29C .CRT$XCL
  008C31F0..5670    1,169 entries     .CRT$XCU
  008C5678          null              __xc_z
  008C5680          null              __xi_a
  008C5688..5698    00808C90 00808D4C 00809124
  008C56A0          null              __xi_z
  008C56B8..56E0    nulls only        .CRT$XP*, .CRT$XT*

start-up state 02EAECF8 (u32)
  0  not started   1  initialisers running   2  initialisers done

module exit tables (encoded qwords, each set to encode(-1) by 00808988)
  02EAED08  first, last, end    atexit table
  02EAED20  first, last, end    at_quick_exit table

IMAGE_TLS_DIRECTORY64 at 01CEBED8
  +0x00  u64  StartAddressOfRawData   0x03004000
  +0x08  u64  EndAddressOfRawData     0x03004008
  +0x10  u64  AddressOfIndex          0x02EAED3C
  +0x18  u64  AddressOfCallBacks      0x008C56B0   first entry null
  +0x20  u32  SizeOfZeroFill          0
```

## Shipped data

| Fact | Value |
|---|---|
| C table | 3 entries between nulls at `008C5680` and `008C56A0` |
| C++ table | 1,172 entries, `008C31D8`–`008C5670`, between nulls at `008C31D0` and `008C5678` |
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
| `float32-to-float16-static-initialisers` | 69 C++ entries of 29 bytes calling `006E0220` |
| `record-ctor-00616210-initialisers` | 33 C++ entries (texture-format records) |
| `record-ctor-00662c00-initialisers` | 28 C++ entries (vertex-format records) |
| `record-ctor-006d58d0-initialisers` | 9 C++ entries (morph records) |
| `counter-append-initialisers` | 18 C++ entries that append the static to a counted pointer table |
| `zeroinit-record-initialisers`, `zeroinit-3q-initialisers` | 16 and 3 C++ entries that zero a record |
| `alloc-record-0067ffb0-initialisers`, `grow-helper-initialisers` | 8 and 6 C++ entries |
| `ctor-00808fe4-initialisers` | 5 C++ entries that construct an array through `00808FE4` |
| `ctor-0060df70-initialisers` | 2 C++ entries |
| `callback-record-006155b0-registrars` | 6 C++ entries that tail-jump `006155B0` with three code pointers |
| `xc-initializer-leftovers` | 83 C++ entries, each of its own form |
| `empty-dtor-teardown-wrappers` | 145 of the 185 `ret 0` teardowns |
| `static-intrusive-list-teardowns`, `static-intrusive-list-teardown-owners` | the 224 list unlinks, and the class descriptor owning each list |
| `registry-unlink-teardowns` | the 327 registry unlinks |
| `xc-registered-library-teardowns`, `xc-registered-static-teardowns` | 190 and 107 teardowns that C++ entries register |
| `intrusive-list-node-teardowns-115b` | 43 list-clearing loops that release each node through its allocator's slot `+0x18` |
| `scalar-deleting-destructors-free`, `-shared-base`, `-inlined-dtor` | 65, 37 and 24 deleting destructors freeing through `00809950` |
| `two-deallocator-deleting-destructors` | 12 deleting destructors testing bits `0x1` and `0x4` |

The deleting-destructor idiom is on [object construction and destruction](object-construction-and-destruction.md).

## Modding notes

- An injected DLL that attaches after the C++ table has run finds every global above already built.
  The start-up routine `00808D78`, after the cookie is set and before the first initialiser, is the
  earliest point at which none of them exists.
- The prototypes at `01DF0980`–`01DF0A80` lie in the file-backed part of `.data`, so the starting values
  `0015BD30`, `0015BF20` and `0015C0D0` copy can be changed in the file.
- Do not rely on a teardown to see an object die. On a normal quit none runs; on a path through the
  runtime's `exit` they run in reverse registration order after the game has stopped.
- A new global needs both halves: build it in an initialiser and register its teardown, or leave it
  unregistered and accept that it is never torn down.

## Related

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
