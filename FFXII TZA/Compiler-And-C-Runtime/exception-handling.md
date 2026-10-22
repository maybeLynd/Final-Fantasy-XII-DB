---
title: "Exception handling: x64 unwind data, funclets and the C++ EH tables"
kind: "system"
category: "Compiler and C runtime"
addresses: "0x02F98000, 0x00861EB4, 0x00808BA8, 0x00808F64, 0x00861ED8, 0x00861ECC, 0x00861EAE, 0x0080926C, 0x00715C70, 0x0016D6A0, 0x006DA980, 0x00809054, 0x008090C0, 0x008A5C0A, 0x005CD1E0, 0x007A3770, 0x005CCBF0, 0x00194B00, 0x008F34F0, 0x008968C8, 0x00896BE0, 0x001952E0, 0x01DEAAA0, 0x0019A4F0"
---

## What the player sees

Nothing, in normal play. When a C++ exception passes through a function, small compiler-written
routines destroy that function's half-built objects, and a catch routine decides where the game
carries on. None of them shows a message box.

One case leaves a trace. The routine that writes the key bindings (`0x001993B0`, which writes a
`[Keyboard` section through a wide file stream) has a catch-all handler, `0x00896BE0`. When the write
throws, the handler prints `Catch exception when writing keymap.ini` (`0x008F39A0`) to standard output
and resumes the routine at `0x00199763`. The game keeps running with the bindings it has in memory.

## How it works

### Unwind records

The exception directory points at `.pdata` (`0x02F98000`, `0x68A0C` bytes): 35,713 `RUNTIME_FUNCTION`
records, each giving a code range and the RVA of its `UNWIND_INFO`. Every `UNWIND_INFO` is version 1
and lies in `.xdata` (`0x01D529D0` to `0x01DEAA78`, from the POGO record in the debug directory). 11,353
records carry the chain flag and continue another range's unwind data; 6,594 name a language
handler; the rest only describe the prologue.

### The four handlers

Each handler is named by an RVA after the unwind codes:

| Handler | Address | `.pdata` records | Role |
|---|---|---:|---|
| `__CxxFrameHandler3` | stub `0x00861EB4`, slot `0x008C2A70` (`VCRUNTIME140.dll`) | 4,377 | C++ exception handling |
| `__GSHandlerCheck` | `0x00808BA8` | 2,067 | stack-cookie check only |
| `__GSHandlerCheck_EH` | `0x00808F64` | 141 | cookie check, then `__CxxFrameHandler3` |
| `__C_specific_handler` | stub `0x00861ED8`, slot `0x008C29F0` (`VCRUNTIME140.dll`) | 9 | `__try` / `__except` scopes |

`0x00808F64` calls `__GSHandlerCheckCommon` and then `__CxxFrameHandler3` with the same four arguments,
so its records carry a `FuncInfo` RVA exactly like the 4,377. The stack cookie itself is on
[image-hardening.md](image-hardening.md).

### FuncInfo and its three maps

The language data of a C++ record is one RVA, to a 40-byte `FuncInfo` in `.rdata`. The 4,518 C++
records name 4,446 distinct `FuncInfo` records: one per parent function, plus a second `.pdata`
record for each of the 72 catch funclets, which names its parent's `FuncInfo`. Every record has the
magic `0x19930522`; none has an exception-specification list.

- The unwind map has `maxState` entries. Entry `n` gives the state to fall back to and the cleanup
  funclet to run when leaving state `n`; in all 7,488 entries the fallback state is lower than `n`,
  so the map is a tree that ends at state -1. 561 entries have no action.
- The IP-to-state map gives, per code address, the state in force from there on. All 4,446 maps
  begin with state -1 at the function entry, and the parent's map also covers its catch funclets.
- `dispUnwindHelp` is the frame offset of an 8-byte slot the prologue sets to -2. It is `0x20` in
  3,436 records; `0x00194B00`, for example, stores -2 at `[rsp+0x20]` (`0x00194B11`).
- The try-block map lists `try` ranges as state intervals. The image has 72 try blocks.

### Cleanup funclets

A cleanup funclet is called by the unwinder with the parent's establisher frame in `rdx` and indexes
the parent's locals off it. The image has 3,820 distinct cleanup funclets. All but one lie in
`.text$x` (`0x00896280` to `0x008A6970`); the exception, `0x00861EAE`, is the `__std_terminate` import stub
itself, named directly as an action.

| Body | Funclets |
|---|---:|
| `lea rcx,[rip+global] ; jmp destructor` | 1,620 |
| `lea rcx,[rdx+disp] ; jmp destructor` | 899 |
| `mov rcx,[rdx+disp] ; jmp destructor` | 487 |
| `mov rcx,[rdx+disp] ; add rcx,imm ; jmp destructor` | 288 |
| `push rbp`, a frame from `rdx` (`mov rbp,rdx`), then calls, tests or loops | 346 |
| `jmp 0x00861EAE` | 86 |
| other short forms: 53 offset a global (`lea rcx,[rip+g] ; add rcx,imm`), 32 end in `jmp [import slot]` | 94 |

[The cleanup funclet table](exception-handling-cleanup-funclets.tsv) lists all 3,820, read from every
`FuncInfo` unwind map, with the form, the object each points `rcx` at (a local `rdx+N` of the parent's
frame, or a global) and the code it jumps to.

3,092 of the 3,819 bodies in `.text$x` are 12 bytes or shorter, and the longest, `0x00896D60`, is 62
bytes. The common tail-jump targets:

- `0x0080926C`, `_Init_thread_abort`, from 1,545 funclets: each releases the guard of a function-local
  static whose constructor threw. The guards are on
  [lazy-statics-and-one-time-init.md](lazy-statics-and-one-time-init.md).
- `0x00715C70`, from 352: frees the buffer at `+8` of a post-effect library string unless it is the
  shared empty value `0x02EA1720`.
- `0x00861EAE`, from the 86 single-`jmp` pads `0x008A26E4` to `0x008A5B1F`: the `__std_terminate` stub
  (`jmp [0x008C2A78]`). An exception that reaches one of these ends the process.
- `0x001A2830`, from 74: frees an EASTL buffer (begin `+0`, capacity end `+0x10`) through slot 3 of
  the allocator at `+0x18`.

`0x0019A4F0` is the clean-up target of three funclets (`0x00896D00`, `0x008A5930`, `0x008A593C`): it frees the
`BSTR` its argument points to (`SysFreeString`, `jmp [0x008C27C8]`).

### Funclets that do nothing

`0x0016D6A0` is three bytes, `ret 0`. 66 funclets tail-jump to it, 106 call it, and 3 pass it as the
element destructor of an array, as `0x0089DD0E` does with the vector destructor iterator `0x00809054`.
That iterator checks the pointer through `0x00809958` (`jmp [0x008C31C0]`, a slot that holds `0x0016D6A0`)
and then calls it once per element, so these funclets destroy nothing.

`0x006DA980` is also `ret 0`. 99 funclets call it with a source path and line number, the remains of
a release report from the post-effect library: 18 distinct paths, among them
`..\src\GPU\GPUPostEffect.cpp` (17 funclets) and `..\src\ppfx.cpp` (4; `0x008A2050` also passes
`IPfxContext::Instantiate()`).

### Catch funclets

All 72 try blocks have exactly one handler, and every handler has type 0 with adjectives `0x40`: the
image contains only `catch (...)`. A catch funclet sets up a frame from `rdx` like a cleanup funclet
and returns the address the parent resumes at.

- 63 rethrow: they end in `call 0x00861ECC` (`_CxxThrowException`) with two null arguments.
- 8 return a resume address. `0x008968C8` calls `basic_ios::setstate` (slot `0x008C26A0`) on the
  stream and returns `0x00194C5E`, inside its parent `0x00194B00`.
- `0x00896993` frees a `std::string` buffer before rethrowing; see
  [msvc-containers.md](msvc-containers.md).
- Of the 63 in the first group, 22 first free a half-built block through `0x00210EB0`, and 16 release
  one through a sized standard-library release that checks the 32-byte rule: `0x00790840` (8-byte
  elements, 8 funclets), `0x00209AD0` (4-byte, 4) or `0x00209B50` (16-byte, 4). 7 rethrow at once and 18
  clean up another way first; `0x00899670`, for one, calls slot 0 of the object at frame `+0x60` with
  `edx` 1 when it is non-null.
- `0x008A5C4B`, the handler of `0x008098D4`, returns `0x008098E9`, where that routine clears `eax`:
  `0x008098D4` allocates through `0x00210EC0` and returns null instead of passing an exception on.
- `0x00896960`, a handler of the string grow `0x00195670`, allocates again through `0x001DF990` for the
  size held at frame `+0x68` plus one byte and resumes at `0x0019573B`.

[The catch funclet table](exception-handling-catch-funclets.tsv) lists all 72 with their parents, `FuncInfo` records, sizes,
the calls they make and where they end.

### What the image throws

`_CxxThrowException` is reached through stub `0x00861ECC` from 69 call sites: 64 in catch funclets
and 5 in ordinary code. Four of the five (`0x0019501D`, `0x0019B3BD`, `0x001AA78D`, `0x00203F29`) pass the
only `ThrowInfo` record in the image, `0x01DEAAA0`, whose catchable types are `std::bad_cast` and
`std::exception`. The fifth, `0x005CCBD2`, passes nulls and rethrows. Every other exception is raised
inside a library the game imports, such as the `MSVCP140` length and allocation checks.

### Structured exception handling

Nine functions register `__C_specific_handler`, one `__try` scope each:

| Parent | Guarded range | Handler | Kind |
|---|---|---|---|
| `0x005CCBA0` | `0x005CCBC3`..`0x005CCBCC` | filter `0x008A5AD0` | `__except`, resumes `0x005CCBCE` |
| `0x005CD1E0` | `0x005CD2C8`..`0x005CD2E0` | filter `0x0089BEF0` | `__except`, resumes `0x005CD2E0` |
| `0x007A3770` | `0x007A378D`..`0x007A3798` | filter `0x008A5AD0` | `__except`, resumes `0x007A3798` |
| `0x00808A54` | `0x00808A5B`..`0x00808AE6` | filter `0x008A5B7C` | `__except`, resumes `0x00808AE6` |
| `0x00808D78` | `0x00808DA3`..`0x00808EB8` | filter `0x008A5B94` | `__except`, resumes `0x00808EB8` |
| `0x00808FE4` | `0x00809015`..`0x0080903E` | `0x008A5BB2` | `__finally` |
| `0x00809054` | `0x00809087`..`0x008090B3` | `0x008A5BDE` | `__finally` |
| `0x008090C0` | `0x008090E4`..`0x0080910C` | filter `0x008A5C0A` | `__except`, resumes `0x0080910C` |
| `0x00863430` | `0x008634CC`..`0x008634E4` | constant 1 | `__except`, resumes `0x008634E4` |

- `0x007A3770` calls `0x007980A0` directly when `IsDebuggerPresent` returns non-zero, and inside the
  scope otherwise. Its filter `0x008A5AD0` calls `0x005CCBF0`, which builds
  `<exe path>.YYYYMMDD_HHMMSS.dmp` (`%s.%04u%02u%02u_%02u%02u%02u.dmp`) and writes it through
  `0x005CCD00`. `0x005CCBA0` calls the routine pointer at `+8` of its argument the same way.
- `0x005CD1E0` and `0x00863430` create a thread and raise `0x406D1388` with `RaiseException` inside the
  scope; the filters swallow it (`0x0089BEF0` returns -1, `0x00863430` uses the constant 1).
- `0x008A5C0A`, the filter of `__ArrayUnwind` (`0x008090C0`), calls `terminate` when the exception code is
  `0xE06D7363` and otherwise returns 0. `0x008A5B7C` accepts only `0xC0000005`.
- The two `__finally` handlers run `__ArrayUnwind` when the array constructor or destructor iterator
  did not finish.

### Stream sentry destructor clones

`0x001952E0`, `0x00195310`, `0x001AAF20` and `0x001AAF50` are four byte-identical 45-byte bodies. Each loads
the stream from `[rcx]`, finds the virtual base through the displacement at `+4` of its first
pointer, reads the stream buffer at base `+0x48`, and calls slot 2 (`+0x10`) of its vtable when it is
non-null.

Unwind-map entries reach them through 12-byte funclets of the form `lea rcx,[rdx+0x28] ; jmp body`:
`0x008968B0` for `0x001952E0`, `0x00896900` for `0x00195310`, `0x008982F0` for `0x001AAF20` and `0x008982FC` for
`0x001AAF50`. Their parents are character stream routines. `0x00194B00` calls `sputc`, `sputn`, `_Osfx`
and `uncaught_exception` from `MSVCP140`, and `0x001DDC40` calls `_Ipfx`, `sgetc` and `snextc`.

So the bodies are the destructor of the stream sentry these routines construct at frame `+0x28`.
They are listed in [the sentry destructor clones table](exception-handling-bk6-sentry-base-destructor-clones.tsv).

`0x001953F0` is the fuller form for a wide-character output stream: unless `uncaught_exception`
returns true it calls `basic_ostream<wchar_t>::_Osfx`, then makes the same slot-2 call. The funclet
`0x0089690C` (`lea rcx,[rdx+0x28] ; jmp 0x001953F0`) reaches it from `0x00194CD0`.

## Layouts

`RuntimeFunction` (`0xC` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | begin | RVA of the first byte of the range |
| `+0x04` | `u32` | end | RVA one past the last byte |
| `+0x08` | `u32` | unwindInfo | RVA of the UNWIND_INFO in .xdata |

`UnwindInfoHead` (`0x4` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` | versionFlags | version in bits 0-2 (always 1); flags in bits 3-7: 1 exception handler, 2 termination handler, 4 chained |
| `+0x01` | `u8` | prologSize | bytes of prologue |
| `+0x02` | `u8` | codeCount | 2-byte unwind codes that follow, padded to an even count; then the handler RVA and its data, or the chained RuntimeFunction |
| `+0x03` | `u8` | frame | frame register in bits 0-3, scaled offset in bits 4-7 |

`FuncInfo` (`0x28` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | magic | `0x19930522` in all 4,446 records |
| `+0x04` | `i32` | maxState | unwind-map entries |
| `+0x08` | `u32` | unwindMap | RVA of UnwindMapEntry[maxState] |
| `+0x0C` | `u32` | tryBlockCount | try blocks |
| `+0x10` | `u32` | tryBlockMap | RVA of TryBlockMapEntry[tryBlockCount] |
| `+0x14` | `u32` | ipMapCount | IP-to-state entries |
| `+0x18` | `u32` | ipToStateMap | RVA of IpToStateEntry[ipMapCount] |
| `+0x1C` | `i32` | dispUnwindHelp | frame offset of the slot the prologue sets to -2 |
| `+0x20` | `u32` | esTypeList | 0 in every record |
| `+0x24` | `u32` | flags | 1 in 2,443 records, 5 in 2,003 |

`UnwindMapEntry` (`0x8` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `i32` | toState | state to continue with; always lower than this entry's index |
| `+0x04` | `u32` | action | RVA of the cleanup funclet, 0 for none |

`IpToStateEntry` (`0x8` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | ip | RVA from which the state applies |
| `+0x04` | `i32` | state | -1 outside any object's lifetime |

`TryBlockMapEntry` (`0x14` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `i32` | tryLow | first state of the try range |
| `+0x04` | `i32` | tryHigh | last state of the try range |
| `+0x08` | `i32` | catchHigh | highest state inside the handlers |
| `+0x0C` | `i32` | catchCount | handlers; 1 in every block |
| `+0x10` | `u32` | handlerArray | RVA of HandlerType[catchCount] |

`HandlerType` (`0x14` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | adjectives | `0x40` in every handler |
| `+0x04` | `u32` | typeDesc | 0 in every handler: catch (...) |
| `+0x08` | `i32` | catchObj | frame offset of the caught object, 0 |
| `+0x0C` | `u32` | handler | RVA of the catch funclet |
| `+0x10` | `u32` | frameOffset | `0x38`, `0x48` or `0x58` |

`ScopeEntry` (`0x10` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | begin | RVA of the guarded range |
| `+0x04` | `u32` | end | RVA one past it |
| `+0x08` | `u32` | handler | filter RVA, the constant 1, or the __finally RVA |
| `+0x0C` | `u32` | target | RVA of the __except body inside the parent; 0 for __finally |

A `__C_specific_handler` record's data is a `u32` scope count followed by that many `ScopeEntry`.

`0x008F34F0`, the `FuncInfo` of the stream inserter `0x00194B00`, shows the pieces together:

```
maxState 6   unwind map 0x01D55F44   try blocks 1 (0x01D55F74)   IP map 11 entries (0x01D55FA0)
unwind[0]  -> -1   0x008968B0   lea rcx,[rdx+0x28] ; jmp 0x001952E0   (sentry)
unwind[1]  -> -1   0x008968BC   lea rcx,[rdx+0x28] ; jmp 0x001953A0
unwind[2]  ->  1   none
unwind[3]  ->  1   none
unwind[4]  -> -1   0x00861EAE   __std_terminate stub
unwind[5]  ->  4   0x00861EAE
try states 2..2, catch high 3, one catch (...) -> 0x008968C8, resumes at 0x00194C5E
IP map: 0x00194B00 -1, 0x00194B7F 0, 0x00194BB5 1, 0x00194BC3 2, 0x00194C5C 1, 0x00194C82 4,
        0x00194C96 5, 0x00194CAF -1, 0x008968C8 0, 0x008968D5 3, 0x008968F2 0
```

## Shipped data

| Fact | Value |
|---|---|
| `.pdata` records | 35,713 at `0x02F98000`; 11,353 chained; 6,594 with a handler |
| handler records | `__CxxFrameHandler3` 4,377; `__GSHandlerCheck` 2,067; `__GSHandlerCheck_EH` 141; `__C_specific_handler` 9 |
| `FuncInfo` records | 4,446, all magic `0x19930522`, flags 1 in 2,443 and 5 in 2,003 |
| unwind-map entries | 7,488, of which 561 have no action |
| IP-to-state entries | 17,990 |
| try blocks | 72, one `catch (...)` each |
| cleanup funclets | 3,820 distinct (3,819 in `.text$x`) |
| catch funclets | 72, all in `.text$x`; 63 rethrow, 8 resume, 1 frees a string and rethrows |
| `.text$x` | `0x00896280` to `0x008A6970`, `0x106F0` bytes |
| `ThrowInfo` records | 1, `0x01DEAAA0`, `std::bad_cast` |

## Modding notes

- A funclet has no callers. It is reached only through an unwind-map or handler entry, so to change
  what happens when something fails, hook the parent, not the cleanup.
- Moving or resizing a parent function needs new `.pdata`, IP-to-state and unwind-map entries. Stale
  entries fail only when an exception is thrown, which normal play rarely does.
- A detour placed inside a parent runs under the parent's state numbering. Do not throw through it
  and do not leave the parent's frame by any path the unwinder does not know.
- The image never catches a specific type. A mod that throws its own exception type through game
  code is caught by the nearest `catch (...)` and, in 63 of the 72 handlers, thrown again.
- The handlers at `0x007A3770` and `0x005CCBA0` write a crash dump beside the executable. Running under a
  debugger skips them.

## Related

- [Lazy statics and one-time initialisation](lazy-statics-and-one-time-init.md): the guards that the
  1,545 `_Init_thread_abort` funclets release.
- [Image hardening](image-hardening.md): the stack cookie behind `__GSHandlerCheck` and the
  `0x0016D6A0` check pointer.
- [Thunks and import stubs](thunks-and-import-stubs.md): the handler and terminate stubs.
- [MSVC containers](msvc-containers.md): the stream and string code these tables protect.
- [Static initialisation and teardown](static-initialisation-and-teardown.md): the `.text$yd`
  destructors that share the funclets' `lea rcx ; jmp` shape and are registered with `atexit`.
- [Runtime services](runtime-services.md): the crash-dump writer.
- [Jump thunks](../Engine-Core/jump-thunks.md): `0x0016D6A0` as the shared `ret` stub.
- [YEBIS and PPFX](../Third-Party-Libraries/yebis-ppfx-post-effects.md): the library whose
  release reports survive in 99 funclets.
- [EASTL strings and containers](../Third-Party-Libraries/eastl-strings-and-containers.md): the
  buffers `0x001A2830` frees.
