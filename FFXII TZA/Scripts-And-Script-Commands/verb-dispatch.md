---
title: "Verb dispatch: how a script's call id reaches a native handler, how arguments and results cross the value stack, and what the guards refuse"
kind: "system"
category: "Scripts and script commands"
addresses: "0x0025E4C0, 0x002621D0, 0x003DC2D0, 0x003DC270, 0x003DC240, 0x003DC2A0, 0x02B57EF0, 0x01EED700, 0x01F281B0, 0x01F29418, 0x01F29440, 0x01F26720, 0x00267E10, 0x00267DB0, 0x00267F90, 0x00267F60, 0x02099AC0, 0x002650B0, 0x00268100, 0x00261806, 0x0026B4E0, 0x0026B4C0, 0x002651A0, 0x0016D6A0, 0x008620C0, 0x003538F0, 0x00342A80"
---

## What the player sees

Every door that opens, every line of dialogue, every camera move and every wait in a scene is a
zone script calling a native verb: a sixteen-bit number that names one of nearly two thousand
engine functions. The script pushes its arguments, names the verb, and reads back one value. This
page is the plumbing between the two: how the number finds the function, how the arguments
arrive and how the answer comes back. Nothing here is visible on screen, but every scripted
moment passes through it.

## How it works

### The four call opcodes

The interpreter `0x0025E4C0`, which the per-actor driver `0x0025DF00` of the field runtime runs
([script interpreter](script-interpreter.md)), pre-decodes a sixteen-bit operand for every opcode at or above `0x47`,
as `operand = pc[1] | pc[2] << 8` in a sixteen-bit register (`0x0025E5AF`-`0x0025E5BD`), so the id can never exceed `0xFFFF`.
Four three-byte opcodes turn that operand into a verb call:

| Opcode | Mnemonic | Actor | Result |
|---|---|---|---|
| `0x58` | `CALL` | the current actor: wait slot `+8` := the actor's own ordinal | left on the value stack |
| `0x59` | `CALLACT` | pops an actor handle into wait slot `+8`, only while the phase byte `+0x15` is 0 | left on the value stack |
| `0x5D` | `CALLPOPA` | as `CALL` | popped into the `A` register, wait slot `+0x10` |
| `0x5E` | `CALLACTPOPA` | as `CALLACT` | popped into `A` |

`CALLACT` pops its actor only on the first visit, so a durative verb that runs for many frames
keeps the target it started with. `CALLACTPOPA` has no dispatcher call of its own: it jumps into
`CALLPOPA`'s body past the current-actor load. All four call the lifecycle `0x002621D0(manager,
actor, stack, id, waitSlot)`; a non-zero return means the verb is still running, and the handler
rewinds the program counter so the same instruction runs again next frame.

### From id to handler

`0x002621D0` splits the id with an arithmetic shift by 12 and a mask of `0xFFF`: four bits of
family, twelve of command. The family selects a table pointer from the sixteen-entry array at
`0x02B57EF0`, which `0x003DC2D0` fills at start-up (from the actor-system reset `0x00266D10`,
[startup constants](../Engine-Core/startup-constants.md)): every entry gets the default table `0x01F26720`,
then families 0, 3, 5 and 7 get their own.

| Family | Id range | Table | Commands |
|---|---|---|---|
| 0 | `0x0000` to `0x05D7` | `0x01EED700` | 1,496 |
| 3 | `0x3000` to `0x3092` | `0x01F281B0` | 147 |
| 5 | `0x5000` | `0x01F29418` | 1 |
| 7 | `0x7000` to `0x7067` | `0x01F29440` | 104 |
| 1, 2, 4, 6, 8 to 15 | `0xN000` to `0xN0D3` | `0x01F26720`, shared | 212 |

So `0x2005` and `0x4005` name the same command; the shared table is family 2's debug verbs, and
the other eleven families alias it. A table is a signed count at `+0`, four bytes of zero, then
one 32-byte record per command from `+8`: begin at `+0`, poll at `+8`, an always-null pointer at
`+0x10`, result at `+0x18`.

The three accessors `0x003DC270` (begin), `0x003DC240` (poll) and `0x003DC2A0` (result) index the
family array with no bound, return null for a null table, and compare the command against the
count as a signed integer. A command at or above the count is refused; a negative command would
read before the table, and a family outside 0 to 15 would read beside the array. Neither is
reachable from bytecode, because the decoder leaves the id in 0 to `0xFFFF`.

The pointer
`0x0016D6A0`, a bare `ret`, stands in for an absent callback in 9 begin and 25 result slots, so a
non-null pointer is not proof of a handler.

### The callback signatures

All three callbacks use the Microsoft x64 convention with the same first three registers:

| Register | begin | poll | result |
|---|---|---|---|
| `rcx` | the issuing actor record | same | same |
| `rdx` | the target actor: the issuer, or the actor wait slot `+8` names, resolved by ordinal through `0x00358940` | same | same |
| `r8` | the wait slot's `+0x18`, sixteen bytes of scratch private to the command | same | same |
| `r9` | the value stack | not passed | the value stack |
| `[rsp + 0x20]` | the manager slot | not passed | not passed |

`poll` cannot read arguments, which is why a durative verb's `begin` must copy what it needs into
the scratch block. A poll that reads the manager index `+0x15` through `rdx`, as `wait`'s and
`camerasync`'s do, reads the target's, which is the issuer's only because those verbs are issued
with `CALL`. Nearly every handler opens with `mov rcx, r9` and a call to a pop helper: that
pair is "read an argument".

### The value stack

The stack is one static object at `0x02099AC0`, `0x284` bytes, whose depth the interpreter zeroes
on every entry: `+0` the depth, `+4` a tag byte per slot (1 int, 2 float), `+0x44` a source byte
per slot (6 for a literal or computed value, the width nibble for a reference), `+0x84` a dword
per slot every push writes as 0, `+0x184` the value. Sixty-four slots exist and 63 are usable:
both pushes return without writing at depth 63.

The two pops mirror each other. `0x00267E10` pops as an int, truncating a float with `cvttss2si`;
on an empty stack it returns 0 without a call, and on a tag that is neither 1 nor 2 it calls
`0x008620C0` and returns 0. `0x00267DB0` pops as a float, widening an int with `cvtdq2ps`; on an empty
stack it calls `0x008620C0` and returns 0.0, and on a bad tag returns 0.0 silently. `0x008620C0`
formats "FFXII tried to call exit(), this might be a serious error!" and returns, so every failure
is silent in play: a script that supplies too few arguments runs on zeros.

### Argument order

Handlers pop in stack order, so the first value popped is the last the script pushed, and the
decompiler's parameter list is the pop order. `getmapjumpposbyindex` (`0x0211`, `0x003538F0`)
pops four references, resolving each through `0x002650B0`, then pops the index, calls
`0x00377AB0(index, out)` and stores `out[0]` through the last reference popped, `out[3]` through
the first.

### References and actor handles

`PUSHP` (`0x00268100`) pushes the packed reference
`((ref & 0xFFFFFF) + index × size) | (ref & 0x7000000) | 0x70000000` (`0x00268155`-`0x0026816C`) for the
decoded reference `ref` and element `index`, `size` being 2 for the width nibble `ref >> 28` of 2 or
3, 4 for 4 or 5 and 1 otherwise (`0x00268124`-`0x00268146`), with tag 1 and the real width in the source byte. `0x002650B0(slot, offset)` turns it back into an address
through the six class bases ([script variables](script-variables.md)); classes 6 and 7 fall to
base 0. 57 handlers call it; a store through it is a raw dword whatever the declared width.

`PUSHACT` (`0x00261806`) packs an actor as `(word + 0xE of the actor's tag-table entry) << 16 |
index | 0x4000`, or `0x8000` when the index is past the count of the script image's `+0x80` table,
the [per-actor tag tables](script-interpreter.md#registers) (`0x0026181B`). The request
opcodes and `0x0025AF60` decode the same encoding: bit `0x4000` marks a live handle, bit `0x8000` refuses.

### Results

A verb returns a value by writing the issuer's current wait slot: `0x0026B4E0` stores the int at
`+0xC` and sets the phase byte `+0x15` to 2; `0x0026B4C0` stores the float and sets 3; `0x002651A0`
sets 2 and returns what `+0xC` already holds, used by `charcommoneffectplay` (`0x0465`,
`0x00342A80`) after a nested handler wrote it. The slot index at the record's `+0x11` is read with
`movsx` in every writer and reader, so the field is a signed byte with no bound.

After the result callback the lifecycle pushes exactly one value: the int at `+0xC` for phase 2,
the float for 3 or more, an int 0 for 0 or 1 or when the result slot is null; a stack already at
depth 63 gets nothing. The phase byte then returns to 0. The int writer is reached from 28 calls
and 321 tail jumps, the float writer from 22 and 31, so a handler that returns ends in a jump to
its writer and one that does not ends in a jump to the native function it wraps.

## Layouts

```python
call instruction   opcode (0x58 / 0x59 / 0x5D / 0x5E), u16 id = family << 12 | command
family array       0x02B57EF0: 16 × u64 table pointer
command table      +0 s32 count, +4 zero, then records from +8: +0 begin, +8 poll, +0x10 null, +0x18 result (32 bytes)
value stack        0x02099AC0: +0 s32 depth, +0x04 u8 tag[64], +0x44 u8 source[64], +0x84 u32 zero[64], +0x184 u32 value[64]
reference          (offset + index × width) | class << 24 | 0x70000000; tag 1; source byte = width
actor handle       word +0xE of the +0x80 tag-table entry << 16 | index | 0x4000; 0x8000 no actor
wait slot          +8 target ordinal, +0xC result, +0x10 A, +0x14 wait kind, +0x15 phase, +0x18 scratch[16]
```

## Shipped data

| Fact | Value |
|---|---|
| command slots | 1,960 in five tables (1,496 / 147 / 1 / 104 / 212) |
| absent-callback stub `0x0016D6A0` | 9 begin slots, 25 result slots, 0 poll slots |
| the `+0x10` slot | null in all 1,960 records |
| census method | `E8` calls and `E9` jumps to each helper over `.text` of the shipping executable, including code outside any listed function |
| int pop `0x00267E10` | 1,559 calls and 2 tail jumps |
| float pop `0x00267DB0` | 436 calls and 4 tail jumps |
| pushes `0x00267F90` / `0x00267F60` | 244 / 58 calls |
| reference resolver `0x002650B0` | 57 calls |
| result writers | int 28 calls + 321 jumps, float 22 + 31, claim-and-read 1 |
| lifecycle `0x002621D0` call sites | 3 (`CALL`, `CALLACT`, `CALLPOPA`; `CALLACTPOPA` shares the third) |

## Operations

Per call instruction: decode the id, resolve the target, run the lifecycle, push one value, pop it
into `A` for the `…POPA` forms. Per handler: pop the arguments, do the work, optionally write the
result slot.

## State

The value stack `0x02099AC0`, the family array `0x02B57EF0`, and the issuer's wait slot (`+8`, `+0xC`,
`+0x15`, `+0x18`).

## Modding notes

- A verb id is `family << 12 | command`; families 1, 2, 4, 6 and 8 to 15 all read the 212-entry
  debug table, so `0x2xxx` and `0x4xxx` are the same verbs.
- Arguments are popped last-pushed first; a handler's decompiled parameter order is the pop order.
- Too few arguments give zeros, too many leave values on the stack, and the 64th push is lost:
  none of it is reported.
- A reference argument must come from `PUSHP`; the handler writes a raw dword to the resolved
  address whatever the variable's declared width.
- Every call pushes one value, so a verb used as a statement needs the `CALLPOPA` form.

## Related

- [Script interpreter](script-interpreter.md): the opcodes around the call.
- [Native commands](native-commands.md): the lifecycle, the tables and the durative verbs.
- [Script verb table](verb-table.md): every id, name and handler.
- [Script variables](script-variables.md): the storage classes a reference names.
