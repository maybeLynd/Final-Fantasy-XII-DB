---
title: "Call signatures: the arguments each function reads and passes on"
kind: "reference"
category: "Engine core"
addresses: "0x0079D730, 0x00311CD0, 0x00197710, 0x0085DDE0, 0x00325EA0, 0x0030FE60, 0x0018D680, 0x0053DD10, 0x004B1190, 0x0073F920, 0x001263AD"
---

## What it lists

One row for each of the executable's 39,107 functions, from `0x00121000` to `0x008C15E0` and from one-instruction
stubs (a `ret` or a `jmp`) to a body of 6,492 instructions (`0x004B1190`): the integer and float argument registers each function reads,
its argument count (the highest argument position it reads), the arguments its entry stores in their home slots,
and the stack arguments it reads. A second table lists every call and tail call, including those in `__except` blocks, with its target and the argument
registers that reach it unchanged. Return values are not in these tables.

### What the code shows beyond the arguments

[`call-signatures-contract-evidence.tsv`](call-signatures-contract-evidence.tsv) has one row per function
with what its bytes and its direct callers show about the rest of its contract. Each function is read straight
through in address order, so a value is followed along the layout of the code and each path is not followed on its
own. Decoding steps over a jump table inside a function and any bytes that do not decode, and it resumes at the
next address a table or a direct jump names. A count is evidence for a contract and is not a prototype.

| Column | Meaning |
|---|---|
| `ret_sites` | the `ret` instructions in the function, with the `repz` and `bnd` forms |
| `return_register_at_ret` | for each `ret`, the last write to `rax` or `xmm0` above it in the layout, at any width: `none`, `after a call` when a call comes first, and `tail` for a jump to another function, which returns that function's value; `-` when the function has neither, 463 rows of which 378 end in a jump through a register or memory |
| `callers` | the direct `call` sites of the function |
| `caller_reads_rax` | how many of them read the return register before writing it, by the width first read (`rax`, `eax`, `ax`, `al`) |
| `caller_reads_xmm0` | how many read `xmm0` before writing it |
| `writes_through_arg` | for each argument register, how many different offsets the function stores to through it, directly, through a `lea` of it or after reloading it from its stack home slot: an output or a changed record |
| `arg_kept_in_memory` | an argument's full 64-bit value stored in a global (`global`) or in a record that is not the stack (`record`), so the callee may keep the pointer |
| `direct_recursion` | calls of the function from its own body |
| `global_writes` | instructions that write global memory through `rip`, into a writable section |
| `instructions` | the function's length in instructions, without `int3` padding |

Of the functions with a direct caller, 6,385 have a caller that reads an integer return and 418 one that reads a
float.
10,885 functions store through an argument, 951 keep one in memory, 5,706 write globals and 103 call themselves.
22,195 have no direct `call` site, so their caller columns are 0. A table, a pointer or a tail jump can still reach
them.

The return's width is the width callers read, because `return_register_at_ret` gives only the last write in the
layout: above the `ret` of `0x003AA280` that is `xor eax, eax` (`0x003AA2CD`), and all 40 callers read the full `rax`.
Types,
the meaning of each argument, the thread a function runs on and what must be set up first are on the system pages
and cannot be read from these counts.

`Database/Tools/catalogues/call_contracts.py` writes the table.

### Positions, not register counts

The x64 convention gives each argument a position: `rcx` or `xmm0` is the first, `rdx` or `xmm1`
the second, `r8` or `xmm2` the third, `r9` or `xmm3` the fourth. Arity is the highest position read.
`0x0079D730` reads `edx` at entry (`dec edx; cmp edx, 0x11; ja`) and `rcx` only inside the arms of its switch
(`0x0079D752 movd xmm0, [rcx+0x414]`), so its arguments are `rcx` and `rdx`, arity 2.

A function can leave a lower position unread: `0x00197710` overwrites `ecx` with `movzx ecx, r8b`
before any read and reads `dl`, `r8b` and `r9b`, so it lists `rdx,r8,r9` at arity 4. 7,058 functions
have such an unread position below their arity.

### Stack arguments

A fifth or later argument arrives on the stack, above the caller's 32-byte home area, and the main table's arity
does not count it. The stack arguments are in [`call-signatures-stack-args.tsv`](call-signatures-stack-args.tsv):
1,670 functions read one. `0x0085DDE0` reads positions 7, 8 and 9 (`0x0085DDF8 mov r15, [rsp+0xA0]` under a 0x58-byte
frame); `0x0073F920` reads every position from 5 to 45.

Fifty-nine functions also read their own stack through a pointer that a loop advances: `0x001263AD` walks `rsp` itself
up its local array, 16 bytes a pass. It copies nine 16-byte rows into the array, reads the first at `0x00126499`, and
loops until its output pointer `rdi` (the fifth argument), advanced each pass by the stride in its sixth argument
(`0x0012652C`), reaches the end `rdi + 8 * stride` set at `0x00126488` (`0x0012652F cmp rdi, rcx`): eight passes for a
non-zero stride, after which `0x00126534 pop rsp` loads the stack pointer saved just above the array.

Those reads are in the `loop_reads` column, each with the pointer's offset when the loop is entered and its change
per pass; how far they reach is set by the loop's exit test.

### What a call receives

[`call-signatures-forwards.tsv`](call-signatures-forwards.tsv) has one row for each of the 137,603 call and tail-call
sites: 122,336 calls and 15,267 tail calls. 126,523 name a function, 3,802 an import, 441 a function pointer kept in
a global, and 6,837 a register or memory operand. At 35,829 sites at least one argument register still holds the
function's incoming value on every path to the site, so the callee receives that argument unchanged.

## Columns

[`call-signatures.tsv`](call-signatures.tsv), one row per function:

| Column | Meaning |
|---|---|
| `addr` | the function's entry address |
| `arity` | the highest argument position read before written, 0 to 4; register slots only |
| `int_regs` | the integer argument registers read before written, `-` when the body reads no integer argument register |
| `flt_regs` | the float argument registers `xmm0` to `xmm3` read before written |
| `home_spill` | integer argument registers stored unchanged into their own home slot (`[entry rsp + 8]` for `rcx` up to `+0x20` for `r9`) |
| `call_passthrough` | argument registers some path leaves unwritten up to a call or tail call (the site's `held_on_every_path` or `held_on_some_paths` in the forwarding table), less those in `int_regs` and `flt_regs`; on that path the callee receives them unchanged |
| `insns` | instructions reached from the entry and from the body's `__except` blocks; bytes of the extent that no path reaches, such as a switch table or padding, are not counted |

`home_spill` is a store of the incoming register into its own slot. A store of an argument register elsewhere does not
count: `0x0030FE60` zeroes `ecx` and writes it through `rax` as a dword every 8 bytes over three 0x200-byte tables (from
`0x022BE984`, `0x022BEB94` and `0x022BEDA4`) and as a word 4 bytes before each table (`0x0030FE7B`, `0x0030FE9B`, `0x0030FEBB`),
and `0x00311CD0` stores `r9d` at `[rsp+0x20]` after `sub rsp, 0x38`, which is the fifth argument of its own call to
`0x00311B20`.

Neither is a home spill. 1,334 functions have one, among them `0x0018D680`, which then reads its arguments' bytes back
from the slots.

[`call-signatures-stack-args.tsv`](call-signatures-stack-args.tsv), one row per function:

| Column | Meaning |
|---|---|
| `addr` | the function's entry address |
| `derived_arity` | `arity` from the main table |
| `stack_positions` | the argument positions read from the stack: 5 is `[entry rsp + 0x28]`, eight bytes per position |
| `max_position` | the highest of them |
| `first_read` | the first instruction, in address order, that reads the highest position |
| `loop_reads` | reads of the function's own stack through a pointer a loop advances: the site, the pointer and displacement, the pointer's offset from the entry `rsp` when the loop is entered and its change per pass (a site after the pass has advanced the pointer reads one step higher on the first pass); `after the loop at L` for a read through the pointer a loop has left behind |

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
| `name` | its working name, `FUN_` and the address when it has no name |
| `derived_arity` | `arity` from the main table |
| `int_regs` | `int_regs` from the main table |
| `classes` | how many virtual tables hold it |
| `class_names` | those tables' classes, separated by `;` |
| `slots` | the slot indices it occupies, separated by `,` |

## Data

| Fact | Value |
|---|---|
| Functions | 39,107 |
| Arity 0 / 1 / 2 / 3 / 4 | 10,661 / 8,214 / 11,172 / 4,772 / 4,288 |
| Read a float argument register | 1,314 |
| Store an argument in its home slot | 1,334 |
| Leave a position below their arity unread | 7,058 |
| Read a stack argument | 1,670 |
| Read their own stack through a loop-advanced pointer | 59 |
| Call and tail-call sites | 137,603 |
| Sit in a class's virtual table | 6,882 |

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

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Audio: `0x00121000` calls `0x00121DB0`, `0x00124350`; `0x00121000` is called by `0x007AC4F0`; those functions are documented
  on [media decoder libraries](../Third-Party-Libraries/media-decoder-libraries.md),
  [audio effects](../Sound-And-Music/audio-effects.md).
