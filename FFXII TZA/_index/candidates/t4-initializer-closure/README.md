# T-4: cross-translation-unit initialization order, followed through callees

OPUS, 2026-09-27. Static, image sha 73461d08…

**Question.** Does any of the 1,172 C++ initializers rely on another compiland's initializer having run first?
FABLE's bound (2026-09-22) read each initializer's own body and found no such reliance. It stated that absence was not
proven, because a helper reached through a call was invisible to it.

**Discriminator.** Follow every direct call and tail jump from each initializer. Collect each closure's reads, writes
and address formations of writable globals. For every global that one initializer writes and a later one uses, ask what
kind of flow it is.

**Result.** The closure is followed to depth 4, and the set of shared globals is the same at depth 2 and 4: 72 globals.
Every one falls into an order-safe class:

| class | globals | why order does not matter |
|---|---|---|
| CRT thread-static epoch | `01F44850` | `_Init_thread_footer` `0080929C`, the CRT's own mechanism |
| function-local static | `01F2E330`, `01F2E340`, `01F2E358` | built behind `_Init_thread_header`/`_footer` (guard `02CF94EC`) by whichever initializer calls first |
| accumulator inside ONE compiland | 14 (registration lists, the context-switch budget, the animation-channel-type index `02CACF18`, …) | one contiguous slot run and a `.text` run with no other function inside, so declaration order |
| accumulator ACROSS compilands | `02CBF998` (named list, 005FDCB0) | first registrant of a name wins, but all 116 init-time names are distinct, so the rejection path is never taken; only list order varies |
| | `02CF8260` (class-id counter) | ids depend on order; no instruction compares a dword at `+0xE8` to a literal except `0057F360`, which is not a descriptor; consumers index by id (Q-2) |
| single-writer, used later | the other 52 | 87 uses are the sixth argument of `00632D80`, stored at `+0x78` (parent) and never dereferenced; 79 go through the root getter `006372A0`; 8 are FABLE's published intra-compiland pairs |

The indirect calls the closure does not follow:
- The allocator vtable `00902720` accounts for 58 sites and is resolved. Its allocate function `001EDF80` builds its heap
  state `1F82E48` on the first call.
- 23 sites in 9 bodies remain unresolved. One of them, `0062CD40`, is a switch jump. They are printed by the control and
  are the residue.

**Not claimed** *(superseded by the second pass below)*:
- code outside the listed bodies;
- ~~the 23 residual indirect sites~~ resolved, see below;
- whether anything consumes the enumeration order of `02CBF998` - sharpened below;
- class ids that leave the process.

**Control.** `t4_closure_check.py`:
- C1: the table.
- C2: the 72 shared globals, stable across depth.
- C3: the classes.
- C4: one-compiland accumulators.
- C5: the two cross-compiland accumulators.
- C6: every later single-writer use.
- R1: `00632D80` never dereferences the parent. With C6, this rejects "an initializer reads another compiland's
  constructed object".
- P1: FABLE's published chain is found.
- L: the residue.

Expected `FAILS 0`, in about 10 minutes.

## Second pass (OPUS, 2026-09-27): the 23 sites resolved

The reviewer (OPUS-REQ-AUDITSPEC-REVIEW-T4-CLOSURE, ACCEPT) judged the first pass as bounded: "no order dependence over
resolvable edges, residue enumerated". This pass resolves the residue, each site by its own receiver:

| sites | resolution |
|---|---|
| 9 calls `[[X]+8]` in `0015BC40` (slot 3) / `00792350` on file-backed PUtility statics | All are behind `byte [01F2CDF0] == 0`. That byte is 1 in the file, and its only image-wide references are 16 byte compares (no store, no `lea`), so the calls are skipped. Were one taken at slot 3, it would reach the file's vtable `00D26BC0` slot 1 = `005C5230` `xor eax, eax; ret`: the derived vtables are installed only by slots 105–1171 and by exit handlers |
| `0062CD40` `jmp rdx` | a 51-arm switch landing inside itself; the function reads no global |
| `0020D2F0` `call r9`, `[rdi+0x40]`, `[rdi+0x48]` | the AMD ADL loader: GetProcAddress results from `atiadlxx.dll` / `atiadlxy.dll`. The one in-image pointer it hands out, `0020D7B0`, is `movsxd; jmp [malloc]` |
| allocator calls in `00199DB0`, `001E2250`, `001F57E0` | the words `001EDF00` installed: vtable `00902720`, slots 2 / 3 = `001EDF80` / `001EDFE0` |
| element destructors in `001E2250`, `001E3D80`, `001F57E0` | slot 0 of the only vtables the reallocators install (`009010B8` → `009010D8` / `00903940`) |
| `006DA8A0` `jmp [rax+0x10]` | dead at init. Its only caller, `00715360` (slot 656), calls it behind `[02EA0B58 + 8] != 0`, a `.bss` word no initializer before slot 656 writes or takes the address of |

**Re-run with the resolved edges.** The only new shared global is the allocator heap state `01F82E48`. `001EDF80` and
`001EDFE0` build it on first use (compare to zero, store on the zero path only), so it is order-safe. The set is the same
at depth 6 (73 = 72 + 1). That `01F82E48` appears at all is the positive control that the edges were applied.

**What remains, sharpened.** One order-visible numbering.
- `005FDCB0` inserts at the head of `02CBF998`, so the list runs in reverse registration order.
- `005FD560` numbers the nodes by list position (`+0x18` = 0, 1, 2, …), so the numbers depend on cross-compiland init
  order.
- The one consumer read here, `005F0720`, uses a number only as a slot index into a per-object table sized by the count
  (`02CB635C`). That is self-consistent within the process.
- The other readers of node `+0x18` are not enumerated.

**T-4 therefore stays NARROWED, not answered.** To answer it, show that every reader of node `+0x18` is index-only, as
Q-2 did for class ids.

**Control additions:** L2a–L2g in `t4_closure_check.py`. Expected `FAILS 0`, in about 15 minutes.

| consumer | action | agreement |
|---|---|---|
| `_index/OPEN-QUESTIONS.md` T-4 status cell | second-pass narrowing appended; stays NARROWED | revised-here |
| `24-Compiler-And-CRT-Runtime/Static-Initialization-And-Lifetime/static-initialization-order-and-injection-timing.md` T-4 box | unchanged: the row is not closed, so the box stays open | agrees |

Affected: T-4 in `_index/OPEN-QUESTIONS.md`. Regression: `t4_closure_check.py` L2a-L2g (run verified at b4b5f347b: 16 PASS, FAILS 0).
