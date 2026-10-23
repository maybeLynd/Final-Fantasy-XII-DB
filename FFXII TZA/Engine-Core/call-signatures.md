---
title: "Call signatures: the arguments each function reads and passes on"
kind: "reference"
category: "Engine core"
addresses: "0x0079D730, 0x00311CD0, 0x00197710, 0x0085DDE0, 0x00325EA0, 0x0030FE60, 0x0018D680, 0x0053DD10, 0x004B1190, 0x0073F920, 0x001263AD"
---

## What it lists

One row for each of the executable's 38,161 functions, from `0x00121000` to `0x008C15E0` and from one-instruction
stubs (a `ret` or a `jmp`) to a body of 6,492 instructions (`0x004B1190`): the integer and float argument registers each function reads,
its argument count (the highest argument position it reads), the arguments its entry stores in their home slots,
and the stack arguments it reads. A second table lists every call and tail call with its target and the argument
registers that reach it unchanged. Return values are not in these tables.

### Positions, not register counts

The x64 convention gives each argument a position: `rcx` or `xmm0` is the first, `rdx` or `xmm1`
the second, `r8` or `xmm2` the third, `r9` or `xmm3` the fourth. Arity is the highest position read.
`0x0079D730` reads `edx` at entry (`dec edx; cmp edx, 0x11; ja`) and `rcx` only inside the arms of its switch
(`0x0079D752 movd xmm0, [rcx+0x414]`), so its arguments are `rcx` and `rdx`, arity 2.

A function can leave a lower position unread: `0x00197710` overwrites `ecx` with `movzx ecx, r8b`
before any read and reads `dl`, `r8b` and `r9b`, so it lists `rdx,r8,r9` at arity 4. 7,025 functions
have such an unread position below their arity.

### Stack arguments

A fifth or later argument arrives on the stack, above the caller's 32-byte home area, and the main table's arity
does not count it. The stack arguments are in [`call-signatures-stack-args.tsv`](call-signatures-stack-args.tsv):
1,523 functions read one. `0x0085DDE0` reads positions 7, 8 and 9 (`0x0085DDF8 mov r15, [rsp+0xA0]` under a 0x58-byte
frame); `0x0073F920` reads every position from 5 to 45.

Fifty-nine functions also read their own stack through a pointer that a loop advances: `0x001263AD` walks `rsp`
itself up its local array, 16 bytes a pass, until an index reaches a count it is given. Those reads are in the
`loop_reads` column, each with the pointer's offset on the first pass and its change per pass; how far they reach
is set by the loop's exit test.

### What a call receives

[`call-signatures-forwards.tsv`](call-signatures-forwards.tsv) has one row for each of the 137,224 call and tail-call
sites: 122,330 calls and 14,894 tail calls. 126,149 name a function, 3,799 an import, 440 a function pointer kept in
a global, and 6,836 a register or memory operand. At 35,359 sites at least one argument register still holds the
function's incoming value on every path to the site, so the callee receives that argument unchanged.

## Columns

`call-signatures.tsv`, one row per function:

| Column | Meaning |
|---|---|
| `addr` | the function's entry address |
| `arity` | the highest argument position read before written, 0 to 4; register slots only |
| `int_regs` | the integer argument registers read before written, `-` for none |
| `flt_regs` | the float argument registers `xmm0` to `xmm3` read before written |
| `home_spill` | integer argument registers stored unchanged into their own home slot (`[entry rsp + 8]` for `rcx` up to `+0x20` for `r9`) |
| `call_passthrough` | argument registers the body neither reads nor writes before some call or tail call, which that callee receives unchanged |
| `insns` | instructions in the body |

`home_spill` is a store of the incoming register into its own slot. A store of an argument register elsewhere does
not count: `0x0030FE60` zeroes `ecx` and writes it to a table through `rax`, and `0x00311CD0` stores `r9d` at
`[rsp+0x20]` after `sub rsp, 0x38`, which is the fifth argument of its own call to `0x00311B20`. Neither is a home
spill. 1,277 functions have one, among them `0x0018D680`, which then reads its arguments' bytes back from the slots.

[`call-signatures-stack-args.tsv`](call-signatures-stack-args.tsv), one row per function:

| Column | Meaning |
|---|---|
| `addr` | the function's entry address |
| `derived_arity` | `arity` from the main table |
| `stack_positions` | the argument positions read from the stack: 5 is `[entry rsp + 0x28]`, eight bytes per position |
| `max_position` | the highest of them |
| `first_read` | the first instruction, in address order, that reads the highest position |
| `loop_reads` | reads of the function's own stack through a pointer a loop advances: the site, the pointer and displacement, its offset from the entry `rsp` on the first pass and its change per pass; `after the loop at L` for a read through the pointer a loop has left behind |

[`call-signatures-forwards.tsv`](call-signatures-forwards.tsv), one row per call or tail-call site:

| Column | Meaning |
|---|---|
| `caller` | the function containing the site |
| `site` | the instruction's address |
| `kind` | `call`, or `tail` for a jump that leaves the function |
| `target` | the function called, the import (`DLL!name`), a global holding the target (`[address]`), or the register or memory operand |
| `held_on_every_path` | argument registers no path from the entry writes before the site |
| `held_on_some_paths` | argument registers some path, not every one, leaves unwritten before the site |

[`call-signatures-this-types.tsv`](call-signatures-this-types.tsv), one row for each function that sits in a class's virtual table,
so that its first argument is that class's `this`:

| Column | Meaning |
|---|---|
| `addr` | the function's entry address |
| `name` | its working name, `FUN_` and the address when it has none |
| `derived_arity` | `arity` from the main table |
| `int_regs` | `int_regs` from the main table |
| `classes` | how many virtual tables hold it |
| `class_names` | those tables' classes, separated by `;` |
| `slots` | the slot indices it occupies, separated by `,` |

## Data

| Fact | Value |
|---|---|
| Functions | 38,161 |
| Arity 0 / 1 / 2 / 3 / 4 | 10,303 / 8,013 / 11,022 / 4,714 / 4,109 |
| Read a float argument register | 1,240 |
| Store an argument in its home slot | 1,277 |
| Leave a position below their arity unread | 7,025 |
| Read a stack argument | 1,523 |
| Read their own stack through a loop-advanced pointer | 59 |
| Call and tail-call sites | 137,224 |
| Sit in a class's virtual table | 6,883 |

`0x0053DD10` (`mov eax, 1; ret`) is held by 24 virtual tables. It is also called directly: `0x002DDC50()` answers
whether `0x0053DD10()` returns 1, so it always answers 1, and every test on it in its eleven callers passes. They
include the HUD's depth-list draw `0x003F0170`, the overhead status mark `0x002C7B10`, the text icon parser `0x002AEB20`,
the ExFont drawer `0x003649A0`, `0x003656A0`, `0x00366110`, `0x002847C0`, `0x002856B0`, `0x00505570`, `0x00505E00` and
`0x0053E380`.

## Related

- [Vtable methods](vtable-methods.md): every virtual slot with its class, the source of `this`
  types.
- [Class hierarchy](class-hierarchy.md): how the classes and their tables are found.
- [Jump thunks](jump-thunks.md): one-instruction forwarders, whose signature is their target's.
