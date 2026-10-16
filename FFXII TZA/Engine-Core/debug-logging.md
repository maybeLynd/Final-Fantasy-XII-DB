---
title: "Debug logging: the log call, its sink and the console prints the shipped game still runs"
kind: "system"
category: "Engine core"
summary: "The three ways the executable formats text: the PhyreEngine log call 005CDAA0 that formats every message into a 16 KB stack buffer and hands it with a channel number to a sink whose only action is a debugger break on channel 4, the vsprintf wrapper 0019C5D0, and the plain printf 0017D280 that writes boot and script-debug messages to a standard output no window shows; with the sink's lazy construction, the C runtime options word, and the census of channels the 245 log sites pass."
addresses: "005CDAA0, 005CDB90, 005CDA30, 005CD9C0, 008AADA0, 0019C5D0, 0017D280, 0016D670, 0018A320, 00809C50, 0036FCC0, 0017D9D0"
---

## What the player sees

Nothing. The shipped game still carries its developers' logging: engine code formats messages
such as `[FileCache] …` on every load, and the boot prints the name of each step it runs. None of
it reaches the screen. The only cost a player pays is time: every log call formats its message
into a 16 KB stack buffer before the sink discards it.

## How it works

### The log call

`005CDAA0(channel, format, …)` is the log call of the PhyreEngine layer and the game code built
on it: 135 functions call it at 245 sites. It reserves a `0x4050`-byte frame, fetches the C
runtime options word through `0016D670`, and formats into its 16 KB buffer with
`__stdio_common_vsnprintf_s(options, buffer, 0x4000, -1, format, 0, args)`; the `-1` count is
`_TRUNCATE`, so a longer message is cut, never dropped. It then makes sure the sink exists and
calls the sink's virtual slot 1 with the channel and the buffer. The function has one exit and no
test that could skip the formatting.

The sink is a lazily built singleton. The guard `02CB6158` and the pointer `02CB6150` follow the
compiler's thread-safe static pattern (`_Init_thread_header` / `_Init_thread_footer` around the
first use); the pointer comes from `005CDA30`, itself a lazy static (guard `02CB6148`) that
installs the `Phyre::PTTYCallback` vtable `00D360A0` into the 8-byte object at `02CB6140` and
registers `008AADA0` with `atexit`.

`005CD9C0` returns the pointer's address for other users of the same singleton, and `005CD960` runs the same guarded construction and returns nothing; it is
reached only through the thunk `00866B80`, which no code calls.

### What the sink does

Slot 1 of that vtable is `005CDB90(sink, channel)`: when the channel is 4 and `IsDebuggerPresent`
holds it calls `DebugBreak`; otherwise it returns. The text is never read. So the log call's
whole effect in the shipped game is the formatting. Slot 0, `005CD8F0`, is the deleting
destructor: it resets the vtable, rebuilds the pointer through `005CDA30` when the object being
destroyed is the live singleton, and frees the object when its flag bit 0 is set.

Of the 245 sites, 206 load a literal channel: 0 at 16 sites, 1 at 80, 2 at 84 and 3 at 26. The
other 39 compute theirs from a register. No literal is 4, so no literal site can break into a
debugger. The format strings beside the literals read as informational text on channel 0, engine
and screen messages on 1 and 2, and unexpected-value errors on 3.

### The two other formatters

`0019C5D0(buffer, size, format, …)` is the `vsprintf` wrapper 120 functions use at 268 sites: it
calls
`__stdio_common_vsprintf_s(options, buffer, size, format, 0, args)` and returns the count, with
any negative result clamped to -1.

`0017D280(format, …)` is a plain `printf`: `__stdio_common_vfprintf(options, stdout, format, 0,
args)`. 38 functions call it at 60 sites: the PS2 emulation start-up lines in `0036D990` and
`0022CB90` ([PS2 CPU emulation](ps2-cpu-emulation.md)), the boot step list in `0036FCC0`
(`AtelMapJumpByLoad()`, `YsConfig_Load()` and five more), the loader's `load failed!` in
`0017D9D0`, two lines in the field start `00314020`, and the script verbs of the `0050C670` to
`00510870` family that print their arguments.

The executable is a windowed application (PE subsystem 2), so the stream has no console to appear
in unless one is attached from outside.

### The options word

`0016D670` returns the address of the `printf` options qword `02EBA3D0`, and is its only
reference in the image. The C initializer `00809C50` sets bit 2 in it (`4`) and bit 1 in the
`scanf` options qword behind `0018A320` (`01F7F5B0`) before any game code runs; nothing else
writes either, so every formatter above passes the value 4.

## Layouts

| Address | Type | Name | Meaning |
|---|---|---|---|
| `005CDAA0` | `frame` | 0x4050 bytes: a 0x4000-byte message buffer, the va_list and the cookie |  |
| `02CB6140` | `u64` | the sink object: its vtable pointer, Phyre::PTTYCallback 00D360A0 |  |
| `02CB6148` | `i32` | guard of the sink object (005CDA30) |  |
| `02CB6150` | `void*` | the sink pointer the log call uses |  |
| `02CB6158` | `i32` | guard of the sink pointer (005CDAA0, 005CD9C0, 005CD960, 008AADA0) |  |
| `02EBA3D0` | `u64` | printf options, 4 after 00809C50 |  |
| `01F7F5B0` | `u64` | scanf options, bit 1 set by 00809C50 |  |
| `00D360A0` | `vtable` | slot 0 005CD8F0 (deleting destructor), slot 1 005CDB90(sink, channel, text) |  |

## Shipped data

| Fact | Value |
|---|---|
| log call sites / functions | 245 / 135 |
| literal channels | 0: 16, 1: 80, 2: 84, 3: 26; computed: 39 |
| `vsprintf` wrapper callers / sites | 120 / 268 |
| `printf` callers / sites | 38 / 60 |
| message buffer | 16,384 bytes, truncating |
| sink action | channel 4 with a debugger attached: `DebugBreak`; otherwise none |

## Operations

Every log call: format into the stack buffer, build the sink on the first call, call slot 1.
Every `printf` call: format straight to the C runtime's standard output. At process exit:
`008AADA0` re-establishes the stock object's vtable and, only when the pointer still names that
object, rebuilds the pointer.

## State

The sink object and its two guards, the two options words, and the standard output stream.

## Modding notes

- Replacing slot 1 of `00D360A0`, or the pointer at `02CB6150` after the first log call has built
  it, receives every message with its channel; before the first call the stock sink would be
  built over a replaced pointer, and a pointer replaced after it survives the exit pass.
- Attaching a console (`AllocConsole` or a redirected standard output) shows the `printf` lines,
  including the boot step names, without any other change.
- The 16 KB format on every log call is the cost to remove if a hot path logs.

## Related

- [Startup constants](startup-constants.md): the boot sequence the step names belong to.
- [Lazy statics and the one-time init lock](../Compiler-And-C-Runtime/lazy-statics-and-one-time-init.md): the guard pattern the sink uses.
