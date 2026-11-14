---
title: "Call signatures: the arguments each function reads and passes on"
kind: "reference"
category: "Engine core"
addresses: "0x0079D730, 0x00311CD0, 0x00197710, 0x0085DDE0, 0x00325EA0, 0x0030FE60, 0x0018D680, 0x0053DD10, 0x004B1190, 0x0073F920, 0x001263AD"
---

## What it lists

One row for each of the executable's 39,115 functions, from `0x00121000` to `0x008C15E0` and from one-instruction
stubs (a `ret` or a `jmp`) to a body of 6,492 instructions (`0x004B1190`): the integer and float argument registers each function reads,
its argument count (the highest argument position it reads), the arguments its entry stores in their home slots,
and the stack arguments it reads. A second table lists every call and tail call, including those in `__except` blocks, with its target and the argument
registers that reach it unchanged. Return values are not in these tables.

### What the code shows beyond the arguments

[`call-signatures-contract-evidence.tsv`](call-signatures-contract-evidence.tsv) has one row per function
with what its bytes and its direct callers show about the rest of its contract. Each function is read straight
through in address order, so a value is followed along the layout of the code and each path is not followed on its
own. There is one exception: code laid out after a `ret`, a `jmp` or an `int3` starts from the state at
the first forward jump that names it.

Decoding steps over a jump table inside a function and any bytes that do not decode, and it resumes at
the next address a table or a direct jump names. A jump table of fewer than three entries and the byte
index table beside it are found from the indexed read that names them, and decoding ends before them.
A count is evidence for a contract and is not a prototype.

| Column | Meaning |
|---|---|
| `ret_sites` | the `ret` instructions in the function, with the `repz` and `bnd` forms |
| `return_register_at_ret` | for each `ret`, the last write to `rax` or `xmm0` above it in the layout, at any width: `none`, `after a call` when a call comes first, and `tail` for a jump to another function, which returns that function's value; `-` when the function has neither, 462 rows of which 378 end in a jump through a register or memory |
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
11,488 functions store through an argument, 1,095 keep one in memory, 5,706 write globals and 103 call themselves.
22,203 have no direct `call` site, so their caller columns are 0. A table, a pointer or a tail jump can still reach
them.

The return's width is the width callers read, because `return_register_at_ret` gives only the last write in the
layout: above the `ret` of `0x003AA280` that is `xor eax, eax` (`0x003AA2CD`), and all 40 callers read the full `rax`.
Types,
the meaning of each argument, the thread a function runs on and what must be set up first are on the system pages
and cannot be read from these counts.

`Database/Tools/catalogues/call_contracts.py` writes the table.

### Ownership, threads, failure and re-entry

[`call-signatures-contract-flow.tsv`](call-signatures-contract-flow.tsv) has one row for each of the 39,115
functions, measured along each function's control flow. A value is followed from an argument, a call's result or a
constant to where it is used.

[`call-signatures-contracts.tsv`](call-signatures-contracts.tsv) has 54 functions read by hand, whole: what each
takes, returns and keeps, what it reads and writes, what happens when it fails, its locks and recursion, and where
the evidence for it stops.

Along each function's control flow the flow table counts 1,831,216 instructions; the `instructions` column of the
evidence table sums to 1,831,107 over the same 39,115 functions. The two are measured separately, and in some
functions the flow reaches more than that function's count. 549 indirect jumps end a path, among them tail calls
through a pointer.

A function's code is what control flow reaches from its entry, up to the next function's entry. A jump to an address
below that entry and not itself an entry stays in the function: `0x005CD2FF` in `0x005CD1E0` reaches its own epilogue
at `0x005CD319`. A jump to another entry ends the path as a tail call.

#### Thread starts

The game creates its threads at nine sites: four `_beginthreadex` calls and five `CreateThread` calls.
[`call-signatures-thread-starts.tsv`](call-signatures-thread-starts.tsv) lists the 21 start functions and the
process entry, with the creating call and how the start reaches it.

Ten starts go through `0x005CD1E0`, which runs them from the trampoline `0x005CCBA0`. Four go through `0x008636E0`, whose
object's slot 1, `0x00863410`, calls the descriptor's function. Three share the trampoline `0x007A5550`.

`thread_starts` lists the starts that reach a function by direct and tail calls. 1,953 functions have one. Code
entered through a pointer is not followed, so `-` says only that no start reaches the function by those calls.

#### Locks

[`call-signatures-locks.tsv`](call-signatures-locks.tsv) has the 372 calls that take a lock, in 201 functions: 286
`EnterCriticalSection`, 9 `TryEnterCriticalSection`, 15 slim reader/writer locks, 61 of the PhyreEngine lock
`0x005CD4F0` and one of its re-entrant form `0x005CD370`. 309 name a lock the trace could follow.

The PhyreEngine lock `0x005CD4F0` keeps no owner: its state goes from 0 to 1, so a thread that already holds it waits
with no time-out (`0x005CD473`, `0x005CD482`). `0x005CD370` stores the owner's thread id and only raises the hold count
for that thread (`0x005CD3BE`, `0x005CD435`).

#### Call groups

`call_group` numbers the 33 groups of two or more functions that can reach each other by direct and tail calls,
conditional tail jumps included, and gives the group's size. They hold 443 functions; the largest has 160. Over calls
alone there are 29 groups holding 257 functions, the largest 77, and the other 186 are in a group only through a tail
jump. A function calling itself directly is counted in `direct_recursion` above.

#### Columns of call-signatures-contract-flow.tsv

| Column | Holds |
|---|---|
| `addr` | the function |
| `rcx_use`, `rdx_use`, `r8_use`, `r9_use` | the range of offsets read and written through the argument, counted when a path into the instruction holds it, with a pointer stepped around a loop counted at its first-pass offset and a path left out when a 64-bit `cmp` of the value with that same offset of the argument sends it away; other tests, such as a flag or a null check, do not narrow the count, so a counted access can sit on a path such a test excludes; `indexed at` the same for a base with an index register or a `lea` with one, at the fixed part of the offset; whether it is used as an array index; its width when below 8 bytes; and the constants it is compared with or tested against |
| `return_values` | what `rax` holds at each `ret`: a number, an argument, a global, a load, or the result of a named call; `?` where the trace stops |
| `zero_guards` | an argument tested against zero, with what is returned on that path when no call comes first |
| `callers_use_return` | across call sites, how many test the result against zero, use it as an address, store it or otherwise compare it |
| `releases` | the arguments, or fields of arguments, passed to a release on at least one path, including through other functions |
| `returns_new_from` | the allocator a returned block came from |
| `fatal_calls` | the fatal exits the function calls or tail-jumps to, by import name: `exit` (also `_exit` and `ExitProcess`), `TerminateProcess`, `abort`, `terminate` (also `__std_terminate`), `pure call`, `invalid parameter`, `bad alloc`, `length error`, `out of range`, `regex error`, `invalid argument`, `throw` |
| `locks` | the locks it takes directly |
| `thread_starts` | the starts that reach it by direct and tail calls |
| `call_group` | its call group and that group's size |

The releases are `free`, `_aligned_free` and `0x00369860`. The allocators are `malloc`, `calloc`, `_aligned_malloc`,
`realloc`, `0x0036A100`, `0x0036A190` and `0x0036B160`. Both sets are followed through the functions that forward to them.

A `-` or a `?` in these columns says where the trace stops. It does not say the function has no such use.
`Database/Tools/catalogues/call_flow.py`, `call_flow_tables.py` and `call_contracts_read.py` write these tables.

### Positions, not register counts

The x64 convention gives each argument a position: `rcx` or `xmm0` is the first, `rdx` or `xmm1`
the second, `r8` or `xmm2` the third, `r9` or `xmm3` the fourth. Arity is the highest position read.
`0x0079D730` reads `edx` at entry (`dec edx; cmp edx, 0x11; ja`) and `rcx` only inside the arms of its switch
(`0x0079D752 movd xmm0, [rcx+0x414]`), so its arguments are `rcx` and `rdx`, arity 2.

A function can leave a lower position unread: `0x00197710` overwrites `ecx` with `movzx ecx, r8b`
before any read and reads `dl`, `r8b` and `r9b`, so it lists `rdx,r8,r9` at arity 4. 7,059 functions
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

[`call-signatures-forwards.tsv`](call-signatures-forwards.tsv) has one row for each of the 137,609 call and tail-call
sites: 122,336 calls and 15,273 tail calls. 126,527 name a function, 2 the instruction after the call (`call next`),
3,802 an import, 441 a function pointer kept in
a global, and 6,837 a register or memory operand. At 35,835 sites at least one argument register still holds the
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
| Functions | 39,115 |
| Arity 0 / 1 / 2 / 3 / 4 | 10,661 / 8,220 / 11,172 / 4,774 / 4,288 |
| Read a float argument register | 1,316 |
| Store an argument in its home slot | 1,334 |
| Leave a position below their arity unread | 7,059 |
| Read a stack argument | 1,670 |
| Read their own stack through a loop-advanced pointer | 59 |
| Call and tail-call sites | 137,609 |
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
- Platform: `0x005CD4F0` is called by `0x0019CC50`; those functions are documented on [debug menu](debug-menu.md).
- Resource: `0x0036A100` is called by `0x00249210`, `0x0024EF90`, `0x0024F240`; `0x0036A190` is called by `0x00249210`,
  `0x0024A1D0`, `0x00259DF0`, `0x0032E7C0`, `0x00379E90`, `0x00384420`, `0x0051ED10`; `0x005CD1E0` is called by `0x001DAAC0`;
  `0x005CD4F0` is called by `0x001A0A90`, `0x001A0BB0`, `0x001A0C50`, `0x001A1240`, `0x001D9DA0`, `0x001D9FD0`, `0x001DA220`,
  `0x001DA970`, `0x001DADC0`, `0x0020B680`, `0x0020B9A0`, `0x0020BE50`.
- Resource: `0x005CD4F0` is also called by `0x0020BFA0`, `0x0020C1B0`, `0x002121C0`, `0x00212600`, `0x00675460`, `0x00676450`,
  `0x00676A70`, `0x00676BD0`, `0x00677BA0`.
- Resource: those functions are documented on
  [battle text tables](../Game-Files-And-Data-Tables/battle-text-tables.md),
  [standard file formats](../Game-Files-And-Data-Tables/standard-file-formats.md),
  [as7 menu graphics](../Game-Files-And-Data-Tables/as7-menu-graphics.md),
  [startup constants](startup-constants.md).
- Resource: and on
  [file requests and the read queue](../Game-Files-And-Data-Tables/file-requests-and-the-read-queue.md),
  [authored data tables](../Game-Files-And-Data-Tables/authored-data-tables.md),
  [prefetch manifests](../Game-Files-And-Data-Tables/prefetch-manifests.md).
- Resource: and on [async load manager](../Game-Files-And-Data-Tables/async-load-manager.md),
  [file path resolution](../Game-Files-And-Data-Tables/file-path-resolution.md),
  [audio manager](../Sound-And-Music/audio-manager.md),
  [memory and allocation](../Compiler-And-C-Runtime/memory-and-allocation.md).
- Resource: and on [phyre asset files](../PhyreEngine/phyre-asset-files.md),
  [phyre reflection](../PhyreEngine/phyre-reflection.md).
- World area: `0x0036A190` is called by `0x00378540`; those functions are documented on
  [ps2data bin families](../Game-Files-And-Data-Tables/ps2data-bin-families.md).
