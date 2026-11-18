[Home](../../README.md) / [Engine core](README.md) / Jump thunks

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Jump thunks: every one-instruction forwarder, its target, and who reaches which of the two | reference | Engine core | Function and class indexes | The 763 functions in the executable whose whole body is one jump to another function, and the 86 terminate landing pads that share one import stub; jump-thunks.tsv lists 568 of the forwarders and 85 of the pads with the target, the direct callers of the thunk and of the target, and whether the thunk's address is held in a data table; with how each forwarder is reached, the ten two-step chains in the table, the one forwarder that presets an argument before jumping, and the shared ret stub 0x0016D6A0 that both the Control Flow Guard slot and 2,528 call sites name. | 0x0016D6A0, 0x0017E7D0, 0x00379F20, 0x0035B450, 0x0035B650, 0x00861EAE, 0x008A26E4, 0x00866B80, 0x005CD960 |

## What it lists

A forwarder is a body that is exactly one `jmp rel32` into `.text`, followed by `int3` padding or by
another start. It sits at a `.pdata` begin, or right after an `int3`, a `ret` or another `jmp rel32`.
It is itself a start: a `.pdata` begin, the target of a `call` or `jmp rel32`, a qword in `.rdata`
or `.data`, the target of a rip-relative `lea`, or an `E9` right after `int3` padding. The terminate
pads, which jump to `0x00861EAE`, are counted apart. By this rule the executable has 763 forwarders
and 86 terminate pads.

The table has one row for 653 of them: 568 forwarders and 85 terminate pads. A thunk and its target are two addresses for one body, and the two are reached by
different roads, so the table records for each the number of functions that `call` the thunk
directly, the number that `call` the target directly, and whether the thunk's or the target's
address appears as an aligned qword in `.rdata` or `.data` (a vtable, a dispatch table or a
stored callback).

The caller counts take only `call` instructions in ordinary function bodies:
a tail jump (`0x0037D110` is reached only by the jump at `0x00351E62`) and a call from an
exception-cleanup funclet (`0x0083AB80` from three unwind funclets) both leave a count at 0.

The 86 terminate pads jump to the import stub `0x00861EAE`, which is `jmp [0x008C2A78]`, the
`__std_terminate` import from `VCRUNTIME140.dll`. 85 lie in one run from `0x008A26E4` to
`0x008A508D`, with other code between 33 of them. The 86th, `0x008A5B1F`, stands alone after the `ret` of a funclet that ends at
`0x008A5B1E`. No pad is called and no pad is held in a table; they are the landing pads the exception
records name for functions that must not throw.

The 763 forwarders jump to 763 distinct targets, one each, and 33 of the targets are themselves
forwarders. Each forwarder is counted once, in the first row that fits:

| Reached by | Forwarders |
|---|---|
| a direct `call` | 234 |
| its address held as a qword or taken by `lea`, and no call | 404 |
| only a `jmp` from another function | 113 |
| nothing | 12 |

384 forwarders are held as a qword at all, 26 are taken by `lea`, and 158 are jumped to at all. The
twelve that nothing reaches are `0x006DAA00`, `0x006DAA10`, `0x006DAA20`, `0x006DAA30`, `0x006DAA40`,
`0x006DF270`, `0x006DF280`, `0x007122F0`, `0x00719360`, `0x00719370`, `0x00809930` and `0x00809940`.

So 751 forwarders are reached by something. `0x0017CDE0` is one of them: it is the qword at `0x008C5788`,
slot 5 of the `GameApplication` vtable `0x008C5760` ([game application](game-application.md)), and the `lea` at
`0x00298290` takes it.

For 384 forwarders a stored pointer names the thunk rather than the body: a hook on the body misses
every dispatch through such a pointer. Among the table's rows, for 132 bodies the thunk is the only
named entry any `call` uses. The reverse holds for the 8 targets a table names directly (`0x005C5230`, `0x007A0B40`,
`0x0016D6A0`, `0x0019C590`, `0x00784DF0`, `0x001243B0`, `0x00844090` and `0x0083AE00`): a hook on the thunk misses the
dispatch through the table.

Ten rows of the table jump to another row: `0x00235DC0` to `0x003844F0` to `0x003697F0`, `0x002E08B0` to
`0x00268620` to `0x00317E60`, `0x002E23B0` to `0x00253720` to `0x00315420`, `0x002E23C0` to `0x00253730` to
`0x00316670`, `0x002E24A0` to `0x003EC7D0` to `0x00404F20`, `0x003CA2E0` to `0x0037C860` to `0x00303EC0`,
`0x0046D340` to `0x00202D50` to `0x00217610`, `0x0046D350` to `0x00202D70` to `0x00217150`, `0x00809950` to
`0x00210EB0` to `0x0019C590` and `0x00863100` to `0x00866B80` to `0x005CD960`.

One forwarder is not a bare jump and so is not in the table: `0x00379F20` is `mov dl, 2` then
`jmp 0x0035B450`, and `0x0035B450` is itself a thunk to `0x0035B650`; calling `0x00379F20` is calling
`0x0035B650` with its second argument preset to 2, which is why the two are not interchangeable.

The other direction also occurs: one address with several identities. `0x0016D6A0` is a three-byte
`ret 0`. 2,528 `call` instructions name it, among them every deleting destructor's array-delete
arm, which passes an object and a size that the stub discards.

The load configuration's Control
Flow Guard check pointer, the slot `0x008C31C0`, also holds `0x0016D6A0`, and `0x0017E7D0` is a thunk to
it; the guard function table is empty (count 0, flags `0x100`) and the optional header's
`DllCharacteristics` is `0x8120`, with the guard bit `0x4000` clear, so the loader never replaces
the slot and the check stays a no-op; the linker folded the two empty functions into one body.

## Columns

| Column | Meaning |
|---|---|
| `thunk` | the one-instruction function's entry address |
| `target` | the address the jump lands on |
| `thunk_callers` | distinct functions with a direct `call` to the thunk |
| `target_callers` | distinct functions with a direct `call` to the target |
| `thunk_pointer_referenced` | 1 when the thunk's address is an aligned qword in `.rdata` or `.data` |
| `target_pointer_referenced` | 1 when the target's address is |

## Related

- [Global state accessors](global-state-accessors.md): the other one-instruction family.
- [Debug logging](debug-logging.md): `0x005CD960`, the end of one chain, is the log sink's
  construction entry.

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 56 calls with 5 other topics</summary>

**Sound and music**

| Function | | Functions |
|---|---|---|
| `0x001243B0` | is called by | `0x00121030`, `0x00121E20`, `0x00210ED0`, `0x00210F60`, `0x002112D0`, `0x00211340`, `0x002254D0`, `0x00225610`, `0x007A48C0`, `0x007A4A10`, `0x007A4AC0`, `0x007A4B30` |
| `0x001243B0` | is also called by | `0x007A4BB0`, `0x007A4C70`, `0x007A4CA0`, `0x007A4D50`, `0x007A5A00`, `0x007A5B20`, `0x007A87C0`, `0x007AC4F0`, `0x007ACD30`, `0x007AD240`, `0x007B0F90`, `0x007B31A0` |

**Sound and music**

| Function | | Functions |
|---|---|---|
| `0x001243B0` | is also called by | `0x007BBAB0`, `0x007BDFA0`, `0x007BE0B0`, `0x007BEAF0`, `0x007BED30`, `0x007BEF30`, `0x007C8890`, `0x007CA650`, `0x007CA9F0`, `0x007EEA00`, `0x007EFA30`, `0x007EFA70` |
| `0x001243B0` | is also called by | `0x007EFB60`, `0x007EFC40`, `0x007EFCB0`, `0x007EFD20`, `0x007EFD90`, `0x007EFE00`, `0x007EFE70`, `0x007EFFE0`, `0x007F0060`, `0x007F0120`, `0x007F0190`, `0x007F0210` |

**Sound and music**

| Function | | Functions |
|---|---|---|
| `0x001243B0` | is also called by | `0x007F0320`, `0x007F0580`, `0x007F0660`, `0x007F0700`, `0x007F0790`, `0x007F0820`, `0x007F1340`, `0x007F1A50` |

**Sound and music** (explained on [sound engine](../Sound-And-Music/sound-engine.md), [sound effects](../Sound-And-Music/sound-effects.md), [audio manager](../Sound-And-Music/audio-manager.md), [sound driver objects](../Sound-And-Music/sound-driver-objects.md), [debug logging](debug-logging.md), [spatial sound](../Sound-And-Music/spatial-sound.md))

**Sound and music** (explained on [audio effects](../Sound-And-Music/audio-effects.md), [sound engine config](../Sound-And-Music/sound-engine-config.md), [maths library](../Compiler-And-C-Runtime/maths-library.md))

</details>
