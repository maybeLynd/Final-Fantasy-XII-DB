[Home](../../README.md) / [Engine core](README.md) / Debug logging

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Debug logging: the log call, its sink and the console prints the shipped game still runs | system | Engine core | Debug tools | The three ways the executable formats text: the PhyreEngine log call 0x005CDAA0 that formats every message into a 16 KB stack buffer and hands it with a channel number to a sink whose only action is a debugger break on channel 4, the vsprintf wrapper 0x0019C5D0, and the plain printf 0x0017D280 that writes boot and script-debug messages to a standard output no window shows; with the sink's lazy construction, the C runtime options word, and the count of channels the 245 log sites pass. | 0x005CDAA0, 0x005CDB90, 0x005CDA30, 0x005CD9C0, 0x008AADA0, 0x0019C5D0, 0x0017D280, 0x0016D670, 0x0018A320, 0x00809C50, 0x0036FCC0, 0x0017D9D0 |

## What the player sees

Nothing. The shipped game still carries its developers' logging: engine code formats messages
such as `[FileCache] …` on every load, and the boot prints the name of each step it runs. None of
it reaches the screen. The only cost a player pays is time: each message is still written out in
full, up to 16 KB, before it is thrown away unread.

## How it works

### The log call

`0x005CDAA0(channel, format, …)` is the log call of the PhyreEngine layer and the game code built
on it: 136 functions reach it at 245 sites (232 calls, 13 tail jumps). It reserves a `0x4050`-byte
frame, fetches the C runtime options word through `0x0016D670`, and formats into its 16 KB buffer with
`__stdio_common_vsnprintf_s(options, buffer, 0x4000, -1, format, 0, args)`; the `-1` count is
`_TRUNCATE`, so a longer message is cut, never dropped.

It then makes sure the sink exists and calls the sink's virtual slot 1 with the channel and the buffer. The function has one exit and no
test that could skip the formatting.

The sink is a lazily built singleton. The guard `0x02CB6158` and the pointer `0x02CB6150` follow the
compiler's thread-safe static pattern (`_Init_thread_header` / `_Init_thread_footer` around the
first use); the pointer comes from `0x005CDA30`, itself a lazy static (guard `0x02CB6148`) that
installs the `Phyre::PTTYCallback` vtable `0x00D360A0` into the 8-byte object at `0x02CB6140` and
registers `0x008AADA0` with `atexit`.

`0x005CD9C0` returns the pointer's address for other users of the same singleton, and `0x005CD960` runs the same
guarded construction and returns nothing; it is reached through the thunk `0x00866B80`, which the thunk
`0x00863100` jumps to, and `0x00863100` is called by `0x002DF9A0` (`0x002E045D`, `0x002E0486`) and `0x0079EDD0`
(`0x0079EDFF`).

### What the sink does

Slot 1 of that vtable is `0x005CDB90(sink, channel, text)`: when the channel is 4 and `IsDebuggerPresent`
holds it calls `DebugBreak`; otherwise it returns. The text is never read. So the log call's
whole effect in the shipped game is the formatting. Slot 0, `0x005CD8F0`, is the deleting
destructor: it resets the vtable, rebuilds the pointer through `0x005CDA30` when the object being
destroyed is the live singleton, and frees the object when its flag bit `0x1` is set.

Of the 245 sites, 206 load a literal channel: 0 at 16 sites, 1 at 80, 2 at 84 and 3 at 26. The
other 39 compute theirs from a register. No literal is 4, so no literal site can break into a
debugger. The format strings beside the literals read as informational text on channel 0, engine
and screen messages on 1 and 2, and unexpected-value errors on 3.

Among its callers in other layers:

- The path resolver `0x0059EE90` logs the name it resolves as `[FFXII_data] %s` or
  `[FFXII_data_notcache] %s` unless the stream's selector byte `+0x18` is 3 to 5, and a failed
  open as `[FFXII_ERROR] Big file open failed %s`
  ([File path resolution](../Game-Files-And-Data-Tables/file-path-resolution.md)).
- The prefetch manager writes the `[FileCache]` lines, `0x001DA090` on each map jump and
  `0x001DA290` on map entry ([Prefetch manifests](../Game-Files-And-Data-Tables/prefetch-manifests.md)).
- The input code logs every recorded action as `INPUT:%d:%s:%s @ frame=%d` and its kin
  (`0x0079A120`) and each controller connection and disconnection (`0x007A2140`)
  ([Vibration](../Controls-And-Input/vibration.md)).
- The renderer logs binding errors such as `Texture2D (%p) missing Shader Resource View%s`
  (`0x0062A0A0`) and shadow-split mismatches (`0x00600F30`)
  (Presentation and rendering).

### The two other formatters

`0x0019C5D0(buffer, size, format, …)` is the `vsprintf` wrapper 120 functions use at 268 sites: it
calls
`__stdio_common_vsprintf_s(options, buffer, size, format, 0, args)` and returns the count, with
any negative result clamped to -1.

90 of the 120 are the sound engine's (`0x007A4D50` to
`0x007F3950`), which formats its `[sead]` messages with it before `OutputDebugStringA`, and its
sink `0x007A5570` fetches the options word through `0x0016D670` ([Sound engine](../Sound-And-Music/sound-engine.md));
the sprite batcher `0x001B0A20` builds `%s_clut_%d` texture names with it
([Sprite batcher](../Graphics/sprite-batcher.md)).

`0x0017D280(format, …)` is a plain `printf`: `__stdio_common_vfprintf(options, stdout, format, 0,
args)`. 40 functions reach it at 62 sites (49 calls, 13 tail jumps): the PS2 emulation start-up lines in
`0x0036D990` and `0x0022CB90` ([PS2 CPU emulation](ps2-cpu-emulation.md)), the boot step list in `0x0036FCC0`
(`AtelMapJumpByLoad()`, `YsConfig_Load()` and five more), the loader's `load failed!` in
`0x0017D9D0`, two lines in the field start `0x00314020`, and the script verbs of the `0x0050C670` to
`0x00510870` family that print their arguments.

`0x0017D9D0` prints `load failed!` when the resource loader's open `0x001D6F20` returns null, and
the archive open `0x001F4340` prints `BigFile head wrong!`
([Bigfile archive](../Game-Files-And-Data-Tables/bigfile-archive.md)).

The settings parser reports bad lines of the
config file through it: `[ConfigFile] invalid line at [%s]` and `invalid key` (`0x001DE5D0`), and
`[ConfigFile] %s value invalid [%s]` and `invalid Resolution` (`0x001DF350`)
([Game settings](../Saving-Loading-And-Settings/game-settings.md)).

The executable is a windowed application (PE subsystem 2), so the stream has no console to appear
in unless one is attached from outside.

### The options word

`0x0016D670` returns the address of the `printf` options qword `0x02EBA3D0`, and is its only
reference in the image. The C initializer `0x00809C50` sets bit `0x4` in it (`4`) and bit `0x2` in the
`scanf` options qword behind `0x0018A320` (`0x01F7F5B0`) before any game code runs; nothing else
writes either, so every formatter above passes the value 4.

## Layouts

| Address | Type | Name | Meaning |
|---|---|---|---|
| `0x005CDAA0` | `frame` |  | `0x4050` bytes: a `0x4000`-byte message buffer, the va_list and the cookie |
| `0x02CB6140` | `u64` |  | the sink object: its vtable pointer, Phyre::PTTYCallback `0x00D360A0` |
| `0x02CB6148` | `i32` |  | guard of the sink object (`0x005CDA30`) |
| `0x02CB6150` | `void*` |  | the sink pointer the log call uses |
| `0x02CB6158` | `i32` |  | guard of the sink pointer (`0x005CDAA0`, `0x005CD9C0`, `0x005CD960`, `0x008AADA0`) |
| `0x02EBA3D0` | `u64` |  | printf options, 4 after `0x00809C50` |
| `0x01F7F5B0` | `u64` |  | scanf options, bit `0x2` set by `0x00809C50` |
| `0x00D360A0` | `vtable` |  | slot 0 `0x005CD8F0` (deleting destructor), slot 1 `0x005CDB90`(sink, channel, text) |

## Shipped data

| Fact | Value |
|---|---|
| log call sites / functions | 245 / 136 |
| literal channels | 0: 16, 1: 80, 2: 84, 3: 26; computed: 39 |
| `vsprintf` wrapper callers / sites | 120 / 268 |
| `printf` callers / sites | 40 / 62 |
| message buffer | 16,384 bytes, truncating |
| sink action | channel 4 with a debugger attached: `DebugBreak`; otherwise nothing |

## Operations

Every log call: format into the stack buffer, build the sink on the first call, call slot 1.
Every `printf` call: format straight to the C runtime's standard output. At process exit:
`0x008AADA0` re-establishes the stock object's vtable (`0x008AADB3`), runs the pointer's guarded
construction under the guard `0x02CB6158` (`0x008AADD5`, again at `0x008AADE9` on the rebuild path), so
a pointer not yet built is built there through `0x005CDA30` (`0x008AAE16`), and, only when the pointer
still names that object (`0x008AADE0`), rebuilds the pointer from `0x005CDA30` (`0x008AADF2`).

## State

The sink object and its two guards, the two options words, and the standard output stream.

## Modding notes

- Replacing slot 1 of `0x00D360A0`, or the pointer at `0x02CB6150` after the first log call has built
  it, receives every message with its channel; before the first call the stock sink would be
  built over a replaced pointer, and a pointer replaced after it survives the exit pass.
- Attaching a console (`AllocConsole` or a redirected standard output) shows the `printf` lines,
  including the boot step names, without any other change.
- The 16 KB format on every log call is the cost to remove if a hot path logs.

## Related

- [Startup constants](startup-constants.md): the boot sequence the step names belong to.
- [Lazy statics and the one-time init lock](../Compiler-And-C-Runtime/lazy-statics-and-one-time-init.md): the guard pattern the sink uses.
