---
title: "Call signatures: the argument registers a function reads, from its own body"
kind: "reference"
category: "Engine core"
summary: "For 562 functions from across the executable, call-signatures.tsv gives the argument count and the integer and float argument registers each body reads before writing them, whether the entry stores an argument in its home slot, and whether the count is only a lower bound because the body tail-jumps on; a second table lists the twelve that also read stack arguments, a third the 40 that sit in a class's virtual table."
addresses: ["0079D730", "00309EC0", "0026D6D0", "0079D620", "00311CD0", "00197710", "008628F0", "0085DDE0", "00325EA0", "0030FE60"]
---

# Call signatures: the argument registers a function reads, from its own body

## What it lists

One row for each of 562 functions drawn from across the executable, from `0015BCF0` to
`008628F0` and from two-instruction stubs to a body of 898 instructions (`007A2440`). The set is
a selection, not every function in the image. For each, the table gives the argument registers
the body itself reads, and from them the argument count.

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
The walk reads the table and follows every arm. `0079D730` reads `edx` at entry
(`dec edx; cmp edx, 0x11; ja`), dispatches through the table at `0079D745`, and reads `rcx` only
inside the arms (`0079D752 movd xmm0, [rcx+0x414]`); it lists as `rcx,rdx`, arity 2.

### Positions, not register counts

The x64 convention gives each argument a position: `rcx` or `xmm0` is the first, `rdx` or `xmm1`
the second, `r8` or `xmm2` the third, `r9` or `xmm3` the fourth. Arity is the highest position read.
A function can leave a lower position unread: `00197710` overwrites `ecx` with `movzx ecx, r8b`
before any read and reads `dl`, `r8b` and `r9b`, so it lists `rdx,r8,r9` at arity 4. 56 rows
have such an unread position below their arity.

### Lower bounds

Only register slots are counted. A body that leaves through a tail jump hands its untouched
argument registers to the target, so its arity is a floor. `0079D620` is `mov ecx, 2` and
`jmp 00796FC0`; `0026D6D0` sets `xmm1`, `xmm0` and `r8d` and jumps to `0026D6F0`. Both list
arity 0 with `lower_bound` 1. An indirect jump that is not a switch also sets the flag:
`00309EC0` loads a handler from `[rdx+0x50]` and leaves through `00309F20 jmp rax`.

### Stack arguments

A fifth or later argument arrives on the stack, above the caller's 32-byte home area, and the
main table does not count it. A second table, `call-signatures-stack-args.tsv`, reads each body for
loads from `[entry rsp + 0x28]` and above. Twelve rows read one. `008628F0` reads
`[rsp+0x28]`, position 5, as its first instruction although its register arity is 2, and
`0085DDE0` reads positions 7, 8 and 9 (`0085DDF8 mov r15, [rsp+0xA0]` under a 0x58-byte frame).

## Columns

`call-signatures.tsv`, one row per function:

| Column | Meaning |
|---|---|
| `addr` | the function's entry address |
| `arity` | the highest argument position read before written, 0 to 4; register slots only |
| `int_regs` | the integer argument registers read before written, `-` for none |
| `flt_regs` | the float argument registers `xmm0` to `xmm3` read before written |
| `home_spill` | integer argument registers the entry block stores, unchanged, into their own home slot (`[entry rsp + 8]` for `rcx` up to `+0x20` for `r9`) |
| `lower_bound` | 1 when the body tail-jumps out with an integer argument register untouched, or leaves through an indirect jump that is not a switch; `arity` is then a floor |
| `unresolved_jump` | 1 when the body has an indirect jump that is not a switch |
| `call_passthrough` | argument registers still neither read nor written at some call, so possibly handed to the callee unchanged |
| `insns` | instructions in the body |

`home_spill` is a store at the entry, before anything changes the register. A store of an
argument register elsewhere does not count: `0030FE60` zeroes `ecx` and writes it to a table
through `rax`, and `00311CD0` stores `r9d` at `[rsp+0x20]` after `sub rsp, 0x38`, which is the
fifth argument of its own call to `00311B20`. Neither is a home spill. Five rows have one,
among them `0018D680`, which then reads its argument's bytes back from the slot.

The table has no return-value column. Whether a body writes `rax` before every `ret` does not
say whether `rax` holds a result: `00325EA0` writes `eax` as scratch (`00325EEF cvttss2si`) and
returns its result through the pointer in `rdx`.

`call-signatures-stack-args.tsv`, one row for each of the same 562 functions:

| Column | Meaning |
|---|---|
| `addr` | the function's entry address |
| `derived_arity` | `arity` from the main table |
| `all_reads_placed` | 0 when some stack read could not be placed because the frame moved by a register amount; the row is then a floor |
| `stack_positions` | the argument positions read from the stack: 5 is `[entry rsp + 0x28]`, eight bytes per position |
| `max_position` | the highest of them |
| `first_read` | one instruction that reads a stack argument, not necessarily the earliest in the body (`0085DDE0` lists `0085DFE9` though `0085DDF8` comes first) |

The frame size is followed through `push`, `sub rsp` and `add rsp` by an immediate, and frame
pointers set from `rsp`. Loads, compares and tests count; stores do not, and the home slots
`+0x08` to `+0x20` belong to the four register arguments.

`call-signatures-this-types.tsv`, one row for each function that sits in a class's virtual table,
so that its first argument is that class's `this`:

| Column | Meaning |
|---|---|
| `addr` | the function's entry address |
| `name` | its working name, `FUN_` and the address when it has none |
| `derived_arity` | `arity` from the main table |
| `int_regs` | `int_regs` from the main table |
| `lower_bound` | `lower_bound` from the main table |
| `classes` | how many classes' virtual tables hold it |
| `class_names` | those classes, separated by `;` |
| `slots` | the slot indices it occupies, separated by `,` |

## Data

| Fact | Value |
|---|---|
| Functions listed | 562 |
| Arity 0 / 1 / 2 / 3 / 4 | 144 / 162 / 156 / 63 / 37 |
| Arity is a lower bound | 34 |
| Leave through an indirect jump that is not a switch | 8 |
| Read a float argument register | 6 |
| Store an argument in its home slot at entry | 5 |
| Leave a position below their arity unread | 56 |
| Read a stack argument | 12 |
| Stack reads not all placed | 29 |
| Sit in a class's virtual table | 40 |

Of the 40 virtual-table rows, `0053DD10` (`mov eax, 1; ret`) is held by 24 classes' tables, and
most of the rest are methods of the Phyre framework's application and input-device classes.

## Related

- [Vtable methods](vtable-methods.md): every virtual slot with its class, the source of `this`
  types.
- [Class hierarchy](class-hierarchy.md): how the classes and their tables are found.
- [Jump thunks](jump-thunks.md): one-instruction forwarders, the extreme case of a lower-bound row.
