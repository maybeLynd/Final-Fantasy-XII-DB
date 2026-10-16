---
title: "Jump thunks: every one-instruction forwarder, its target, and who reaches which of the two"
kind: "reference"
category: "Engine core"
addresses: "0016D6A0, 0017E7D0, 00379F20, 0035B450, 0035B650, 00861EAE, 008A26E4, 00866B80, 005CD960"
---

## What it lists

A forwarder is a body that is exactly one `jmp rel32` into `.text`, followed by `int3` padding or by
another start. It sits at a `.pdata` begin, or right after an `int3`, a `ret` or another `jmp rel32`.
It is itself a start: a `.pdata` begin, the target of a `call` or `jmp rel32`, a qword in `.rdata`
or `.data`, the target of a rip-relative `lea`, or an `E9` right after `int3` padding. The terminate
pads, which jump to `00861EAE`, are counted apart. By this rule the executable has 763 forwarders
and 86 terminate pads.

The table has one row for 653 of them: 568 forwarders and 85 terminate pads. A thunk and its target are two addresses for one body, and the two are reached by
different roads, so the table records for each the number of functions that `call` the thunk
directly, the number that `call` the target directly, and whether the thunk's or the target's
address appears as an aligned qword in `.rdata` or `.data` (a vtable, a dispatch table or a
stored callback).

The caller counts take only `call` instructions in ordinary function bodies:
a tail jump (`0037D110` is reached only by the jump at `00351E62`) and a call from an
exception-cleanup funclet (`0083AB80` from three unwind funclets) both leave a count at 0.

The 86 terminate pads jump to the import stub `00861EAE`, which is `jmp [008C2A78]`, the
`__std_terminate` import from `VCRUNTIME140.dll`. 85 are packed back to back from `008A26E4` to
`008A508D`. The 86th, `008A5B1F`, stands alone after the `ret` of a funclet that ends at
`008A5B1E`. None is called and none is held in a table; they are the landing pads the exception
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
twelve that nothing reaches are `006DAA00`, `006DAA10`, `006DAA20`, `006DAA30`, `006DAA40`,
`006DF270`, `006DF280`, `007122F0`, `00719360`, `00719370`, `00809930` and `00809940`.

So 751 forwarders are reached by something. `0017CDE0` is one of them: it is the qword at `008C5788`,
slot 5 of the `GameApplication` vtable `008C5760`, and the `lea` at `00298290` takes it.

For 384 forwarders a stored pointer names the thunk rather than the body: a hook on the body misses
every dispatch through such a pointer. Among the table's rows, for 132 bodies the thunk is the only
named entry any `call` uses. The reverse holds for the 8 targets a table names directly (`0080A270`, `001FC320`,
`0020B0F0`, `001D6B70`, `006AB7E0` and `005EA310` among them): a hook on the thunk misses the
dispatch through the table.

Ten rows of the table jump to another row: `00235DC0` to `003844F0` to `003697F0`, `002E08B0` to
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
