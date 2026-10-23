---
title: "Call signatures: the argument registers a function reads, from its own body"
kind: "reference"
category: "Engine core"
addresses: "0x0079D730, 0x00311CD0, 0x00197710, 0x0085DDE0, 0x00325EA0, 0x0030FE60, 0x0018D680, 0x0053DD10"
---

## What it lists

One row for each of 499 functions drawn from across the executable, from `0x0015BCF0` to
`0x00862660` and from two-instruction stubs to a body of 898 instructions (`0x007A2440`). The set is
a selection, not every function in the image. For each, the table gives the argument registers
the body itself reads, and from them the argument count: the highest argument position the body reads.

A function is listed only when its body settles every argument read the method can see: it hands no untouched
argument register on through a tail jump, leaves through no indirect jump that is not a switch, and every read of a
stack argument is placed against a frame the walk can follow. A row gives the inputs the body uses, not its
declared prototype: a parameter the body never reads does not show, the tables tell integer from float registers but give no
types, and return values are outside them (see below).

### Method

A register is an argument when some path from the entry reads it before anything writes it. The
body is walked as a control-flow graph, branch by branch, so a register read on one arm only is
still found. Calls are stepped over: a register the callee reads is not thereby an argument of the
caller, and every argument register counts as overwritten after a call returns.

`xor ecx, ecx` and its kin are writes, not reads. A byte or word write covers only that part of
the register, so `mov cl, 1` followed by a read of `rcx` still reads the incoming upper bits; a
32-bit write zero-extends and covers the whole register.

### Switches are followed

An MSVC `switch` ends in `jmp reg` after a bounds check and a load from a table of 32-bit offsets.
The walk reads the table and follows every arm. `0x0079D730` reads `edx` at entry
(`dec edx; cmp edx, 0x11; ja`), dispatches through the table at `0x0079D745`, and reads `rcx` only
inside the arms (`0x0079D752 movd xmm0, [rcx+0x414]`); it lists as `rcx,rdx`, arity 2.

### Positions, not register counts

The x64 convention gives each argument a position: `rcx` or `xmm0` is the first, `rdx` or `xmm1`
the second, `r8` or `xmm2` the third, `r9` or `xmm3` the fourth. Arity is the highest position read.
A function can leave a lower position unread: `0x00197710` overwrites `ecx` with `movzx ecx, r8b`
before any read and reads `dl`, `r8b` and `r9b`, so it lists `rdx,r8,r9` at arity 4. 52 rows
have such an unread position below their arity.

### Stack arguments

A fifth or later argument arrives on the stack, above the caller's 32-byte home area, and the
main table does not count it. A second table, [`call-signatures-stack-args.tsv`](call-signatures-stack-args.tsv), reads each body for
loads from `[entry rsp + 0x28]` and above. Eight rows read one; `0x0085DDE0` reads positions 7, 8 and 9
(`0x0085DDF8 mov r15, [rsp+0xA0]` under a 0x58-byte frame).

## Columns

`call-signatures.tsv`, one row per function:

| Column | Meaning |
|---|---|
| `addr` | the function's entry address |
| `arity` | the highest argument position read before written, 0 to 4; register slots only |
| `int_regs` | the integer argument registers read before written, `-` for none |
| `flt_regs` | the float argument registers `xmm0` to `xmm3` read before written |
| `home_spill` | integer argument registers the entry block stores, unchanged, into their own home slot (`[entry rsp + 8]` for `rcx` up to `+0x20` for `r9`) |
| `call_passthrough` | argument registers neither read nor written before some call, which that callee receives unchanged |
| `insns` | instructions in the body |

`home_spill` is a store at the entry, before anything changes the register. A store of an
argument register elsewhere does not count: `0x0030FE60` zeroes `ecx` and writes it to a table
through `rax`, and `0x00311CD0` stores `r9d` at `[rsp+0x20]` after `sub rsp, 0x38`, which is the
fifth argument of its own call to `0x00311B20`. Neither is a home spill. Three rows have one,
among them `0x0018D680`, which then reads its argument's bytes back from the slot.

The table has no return-value column. Whether a body writes `rax` before every `ret` does not
say whether `rax` holds a result: `0x00325EA0` writes `eax` as scratch (`0x00325EEF cvttss2si`) and
returns its result through the pointer in `rdx`.

[`call-signatures-stack-args.tsv`](call-signatures-stack-args.tsv), one row for each of the same 499 functions:

| Column | Meaning |
|---|---|
| `addr` | the function's entry address |
| `derived_arity` | `arity` from the main table |
| `stack_positions` | the argument positions read from the stack: 5 is `[entry rsp + 0x28]`, eight bytes per position |
| `max_position` | the highest of them |
| `first_read` | one instruction that reads a stack argument, not necessarily the earliest in the body (`0x0085DDE0` lists `0x0085DFE9` though `0x0085DDF8` comes first) |

The frame size is followed through `push`, `sub rsp` and `add rsp` by an immediate, and frame
pointers set from `rsp`. Loads, compares and tests count; stores do not, and the home slots
`+0x08` to `+0x20` belong to the four register arguments.

[`call-signatures-this-types.tsv`](call-signatures-this-types.tsv), one row for each function that sits in a class's virtual table,
so that its first argument is that class's `this`:

| Column | Meaning |
|---|---|
| `addr` | the function's entry address |
| `name` | its working name, `FUN_` and the address when it has none |
| `derived_arity` | `arity` from the main table |
| `int_regs` | `int_regs` from the main table |
| `classes` | how many classes' virtual tables hold it |
| `class_names` | those classes, separated by `;` |
| `slots` | the slot indices it occupies, separated by `,` |

## Data

| Fact | Value |
|---|---|
| Functions listed | 499 |
| Arity 0 / 1 / 2 / 3 / 4 | 133 / 141 / 138 / 55 / 32 |
| Read a float argument register | 6 |
| Store an argument in its home slot at entry | 3 |
| Leave a position below their arity unread | 52 |
| Read a stack argument | 8 |
| Sit in a class's virtual table | 36 |

Of the 36 virtual-table rows, `0x0053DD10` (`mov eax, 1; ret`) is held by 24 classes' tables, and
most of the rest are methods of the Phyre framework's application and input-device classes.

It is also called directly: `0x002DDC50()` answers whether `0x0053DD10()` returns 1, so it always answers 1, and every
test on it in its eleven callers passes. They include the HUD's depth-list draw `0x003F0170`, the overhead status
mark `0x002C7B10`, the text icon parser `0x002AEB20`, the ExFont drawer `0x003649A0`, `0x003656A0`, `0x00366110`,
`0x002847C0`, `0x002856B0`, `0x00505570`, `0x00505E00` and `0x0053E380`.

## Related

- [Vtable methods](vtable-methods.md): every virtual slot with its class, the source of `this`
  types.
- [Class hierarchy](class-hierarchy.md): how the classes and their tables are found.
- [Jump thunks](jump-thunks.md): one-instruction forwarders, whose signature is their target's.
