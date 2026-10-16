---
title: "Jump thunks: every one-instruction forwarder, its target, and who reaches which of the two"
kind: "reference"
category: "Engine core"
summary: "The 653 functions in the executable whose whole body is one jump to another function, listed with the target, the direct callers of the thunk and of the target, and whether the thunk's address is held in a data table, in jump-thunks.tsv; with the 85 terminate landing pads that share one import stub, the ten two-step chains, the one forwarder that presets an argument before jumping, and the shared ret stub 0016D6A0 that both the Control Flow Guard slot and 2,528 call sites name."
addresses: ["0016D6A0", "0017E7D0", "00379F20", "0035B450", "0035B650", "00861EAE", "008A26E4", "00866B80", "005CD960"]
---

# Jump thunks: every one-instruction forwarder, its target, and who reaches which of the two

## What it lists

One row per function entry whose body is a single five-byte `jmp` to another function entry: 653
of them. A thunk and its target are two addresses for one body, and the two are reached by
different roads, so the table records for each the number of functions that `call` the thunk
directly, the number that `call` the target directly, and whether the thunk's or the target's
address appears as an aligned qword in `.rdata` or `.data` (a vtable, a dispatch table or a
stored callback).

The caller counts take only `call` instructions in ordinary function bodies:
a tail jump (`0037D110` is reached only by the jump at `00351E62`) and a call from an
exception-cleanup funclet (`0083AB80` from three unwind funclets) both leave a count at 0.

85 of the thunks, `008A26E4` to `008A508D`, jump to the import stub `00861EAE`, which is
`jmp [008C2A78]`, the `__std_terminate` import from `VCRUNTIME140.dll`. None is called and none
is held in a table; they are the landing pads the exception records name for functions that must
not throw. The other 568 thunks forward to 568 distinct targets, one each:

| Population | Thunks |
|---|---|
| called directly by some function | 234 |
| held as a qword in `.rdata` or `.data` | 244 |
| neither called nor held | 94 |
| targets with no direct caller of their own | 195: 132 whose thunk is called, 14 whose thunk is only held, 49 neither |

So for 132 bodies the thunk is the only named entry any `call` uses, and for 244 a stored pointer
names the thunk rather than the body: a hook on the body misses every dispatch through such a
pointer. The reverse holds for the 8 targets a table names directly (`0080A270`, `001FC320`,
`0020B0F0`, `001D6B70`, `006AB7E0` and `005EA310` among them): a hook on the thunk misses the
dispatch through the table.

Ten thunks jump to another thunk: `00235DC0` to `003844F0` to `003697F0`, `002E08B0` to
`00268620` to `00317E60`, `002E23B0` to `00253720` to `00315420`, `002E23C0` to `00253730` to
`00316670`, `002E24A0` to `003EC7D0` to `00404F20`, `003CA2E0` to `0037C860` to `00303EC0`,
`0046D340` to `00202D50` to `00217610`, `0046D350` to `00202D70` to `00217150`, `00809950` to
`00210EB0` to `0019C590` and `00863100` to `00866B80` to `005CD960`.

One forwarder is not a bare jump and so is not in the table: `00379F20` is `mov dl, 2` then
`jmp 0035B450`, and `0035B450` is itself a thunk to `0035B650`; calling `00379F20` is calling
`0035B650` with its second argument preset to 2, which is why the two are not interchangeable.

The other direction also occurs: one address with several identities. `0016D6A0` is a three-byte
`ret 0`. 2,528 `call` instructions name it, among them every deleting destructor's array-delete
arm, which passes an object and a size that the stub discards.

The load configuration's Control
Flow Guard check pointer, the slot `008C31C0`, also holds `0016D6A0`, and `0017E7D0` is a thunk to
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
- [Debug logging](debug-logging.md): `005CD960`, the end of one chain, is the log sink's
  construction entry.
