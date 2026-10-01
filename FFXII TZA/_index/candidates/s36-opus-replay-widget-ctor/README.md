# S-36: the widget constructor `002465F0` executed as shipped code, and the row's per-invariant stub exposure (OPUS, 2026-09-25, block 298)

**Evidence class: NATIVE-REPLAY (unicorn), `live_game: false`.** This is a narrow OPUS harness, not an ORACLE EXP.

## Why

S-36's runtime cell (MIXED, "no per-invariant stub-exposure analysis yet") names EXP-069 and EXP-091. Neither of them
executes the subject of `16-UI/Widget-Object-Model/CONTRACT-widget-object.md`:
- **EXP-069** runs the request router, generic handler and setter. Its own `contract_coverage` says: *"factory is a
  recording stub, so allocation, copying, ownership and widget procedures are untested"* (`00244F50`, `0028E860`,
  `00808C40` and others are recording `ret` stubs). EXP-068 is the same.
- **EXP-091** is `CONTRACT-commit-action.md` evidence, a different system.
- The `spawn-widget-*` evidence directories are **static** ("this is not execution").

So the contract's constructor postconditions and invariants had **no execution record**.

## What was run

`check.py`:

| status | functions |
|---|---|
| real | `002465F0`, the default handler `005C5230`, `001EDDA0`, `00314960` and the CRT cookie check `00808C40` |
| import bridge | `00861EC0` = `jmp [008C2A60]` = **`VCRUNTIME140!memset`**: `memset(rcx, dl, r8)` |
| planted | a recording handler, passed as the constructor's handler argument, which by the contract's interface is the caller's input |

- The whole SHA-asserted image is mapped.
- Entering any other function fails a case.
- **5 / 5 cases pass, identical over three runs.**

| case | contract item | observed |
|---|---|---|
| `null-handler-default` | a null handler becomes the default; `self[0] != NULL` | `self[0] = 005C5230`. The default handler **runs**, called with message 1 (`005C5230` entered) |
| (all cases) | every widget starts with `1.0f` at `+0xB8` and `100` at `+0x44` | both hold. Also `+0xA0 = 0x80`, `+0xA1 = 0xFF80`, `+0x9C = 0x800080`, `+0x98 = 0`, `+0x48 = &00915198` |
| `null-handler-default` | precondition: `memset`s all `size` bytes | one `memset(self, 0, 0xD8)`; every byte the constructor does not write is 0 afterwards |
| `handler-message-1-payload` | postcondition: the handler is called **once** with `{1, locals->a, locals->b}` | one call, `rcx = self`, message id 1, `a` / `b` copied from `locals+8` / `+0x10` |
| `handler-null-locals-zero-payload` | "both left zero when the argument is NULL" | the message is `{1, 0, 0}` |
| `flag-bit14` | the stack flag's bit 0 → `+0x40` bit 14 | `+0x40 = 0x480A` with the flag set, `0x080A` without |
| `small-size-measurement` | (measurement) | with `size = 0x40`, `memset` clears 0x40 bytes but the constructor **still writes `+0x40`..`+0xBB`**. The storage must cover the fixed header (`0xBC`) whatever `size` says, which the contract's precondition ("requires `size` bytes") does not state |

`00314960` was not reached: `001EDDA0` returned 1 on the image value `[01DFE0C0] = 1`, so the `+0xB4` arm is
unexercised.

## Per-invariant stub exposure for the row

| contract item | executed by | can a substitution reach it? |
|---|---|---|
| constructor postconditions and header invariants | **this harness** | only the `memset` import (bridged with its library semantics) |
| "an unhandled message id tail-jumps to `005C5230`" | not executed (the contract itself says it is observed per handler, not proven for all 267) | coverage |
| the request router / generic handler (the router page) | EXP-069, EXP-068 | the factory `00244F50` is stubbed there. It is exactly what this harness runs from its body inward (`002465F0` is `00244F50`'s constructor call) |

**Stale text.** The binding gap claims a large types gap. That belongs to the types column (MET), not to runtime.
