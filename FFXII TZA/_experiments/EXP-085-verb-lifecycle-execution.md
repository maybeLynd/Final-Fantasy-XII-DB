---
experiment: EXP-085
title: VMNativeCommand_ExecuteLifecycle under isolated original execution
contract: ../01-Script-VM-Native-Bridge/Verb-Dispatch/CONTRACT-verb-dispatch-abi.md
method: B
live_game: false
tool: evidence/verb-lifecycle-execution/check.py
# status and dates are deliberately absent: the gate does not require them and neither is
# sourced by this record. Adding them would be OPUS authoring SWE2-ORACLE's metadata.
---
# EXP-085 — `VMNativeCommand_ExecuteLifecycle` (`002621D0`) isolated original-code execution

**Evidence class: isolated original-code execution.** Not live-game evidence: fixture globals and
planted callback stubs, executed under Unicorn at canonical virtual addresses against the shipping
EXE (SHA-256 `73461D08…721F8`). A scripted callback is not a proved one — what is established here
is the executor's ordering, argument surface, phase machine and push rule, not what any verb does.

**Target contract:** `01-Script-VM-Native-Bridge/Verb-Dispatch/CONTRACT-verb-dispatch-abi.md`
(§13: "the LIFECYCLE half is still unexecuted"; §16 names STATE-TRANSITION as the last
offline-constructible parity dimension).

**Harness:** `_experiments/evidence/verb-lifecycle-execution/check.py`
**Result:** `result.json` — **35/35 cases pass, 9/9 byte-level mutants detected.**
**Bodies:** `bodies.json` — five bodies, SHA-256'd, all at canonical VAs, **zero stubs of shipped
code** (the only planted code is the three fixture callbacks, which are data by design).

## Call surface (verified against shipped bytes)

`002621D0` is 461 bytes (`0x2621D0..0x26239C`). Its complete call surface:

| site | target | what runs |
|---|---|---|
| `00262220` | `003DC240` GetPollCallback | real leaf (poll resolved unconditionally, saved) |
| `0026223B` | `00358940` rebind | real leaf — see correction below |
| `0026225D` | `003DC2A0` GetResultCallback | real leaf |
| `00262278` | `call rax` | **result** — planted stub |
| `002622BA` | `003DC270` GetBeginCallback | real leaf |
| `002622DB` | `call rax` | **begin** — planted stub |
| `002622F8` | `call rax` | **poll** — planted stub |

Nothing else is called. The 14-call reading produced by a linear sweep past `ret` is wrong — the
`0x2E5180`/`0x8620C0`/`call [rdi+0x98]` sites belong to the next function.

## Signature, executed

`rcx` = arg0 = **the actor manager** · `rdx` = arg1 = the issuing context · `r8` = arg2 = the
value stack · `r9d` = arg3 = the verb id · `[rsp+0x28]` = arg4 = cmdState
(`+8` dword rebind index · `+0xC` return slot · `+0x15` phase byte · `+0x18` 16-byte scratch).

## Executed facts

**The phase machine is §7's, plus one arm §7 doesn't draw.** `phase = [cmdState+0x15]`:

- **phase 0** → clear `cmdState+0xC`, resolve+run `begin` (if present), then `poll`.
- **phase 1** → `poll` only — `begin` is **not** re-run (trace `P`, not `BP`).
- **phase ≥ 2** → neither begin nor poll — `result` runs **directly**. The phase byte is
  **re-read after `result` returns** and selects the push flavor:
  - still `< 2` → push int `0` (the value slot is *not* consulted — `p0-result-p1` plants a
    non-zero `+0xC` and the pushed value is still `0`);
  - `== 2` → push int `dword[cmdState+0xC]` (type byte `1`, tag `6`);
  - `> 2` → push **float** `dword[cmdState+0xC]` (type byte `2`, tag `6`).
- So a `result` callback reports its pushed value through **two** cmdState fields: the value in
  `+0xC`, the flavor in `+0x15` — and `+0x15` is cleared to `0` after the push.
- **`+0xC` is cleared only by the phase-0 arm.** A phase-2 entry (`p2-entry`) pushes whatever was
  left there — the return slot persists across the whole command lifetime.
- **`test al,1` is the whole running check**: poll returning `3` → running; returning `0x100`
  → done (the high bits never reach the test).
- **`begin`'s return value is discarded** — `begin` returning `0x77` leaves the flow exactly
  where a `0` would.
- **A missing `poll` is not-running** (`p0-nopoll`: trace `B,R`); a missing `result` still pushes
  int `0` through the `0x262360` arm; a missing `begin` just skips it.

**Callback argument surface, measured per callback** (stubs log every register):

| | begin | poll | result |
|---|---|---|---|
| rcx | issuing context | same | same |
| rdx | resolved target | same | same |
| r8 | `cmdState+0x18` | same | same |
| r9 | **value stack** | **residual — never set** | value stack |
| stack | manager at `[rsp+0x28]` | — | — |

- `poll-r9-residual`: `begin` clobbers `r9` to `0xDEAD5EED`; poll logs `r9 = 0xDEAD5EED` — the
  executor never writes `r9` before poll. The three-argument claim is executed, not inferred.
- `begin`'s fifth argument is the manager — logged at `[rsp+0x28]` from the callee side
  (the contract's `[rsp+0x20]` is the caller-side view of the same slot).

**CORRECTION — the rebind resolves through the manager, not the context.** `00262238 mov rcx,rbp`
hands `arg0` (the manager) to `00358940`; the actor table is read at `[manager+8]` and indexed by
`dword[cmdState+8]`. The *trigger* is `word[ctx] != dword[cmdState+8]`; the *table* is the
manager's. A reconstruction reading "rebind the context" would resolve through the wrong object.
Measured: rebind → `rdx` = `table[8+idx*8]`; equal keys → `rdx` = issuing context; null table,
out-of-range or negative index → `rdx` = `0` (`00358940`'s `xor eax,eax` tail).

**The stack bound is `0x3F`, and index 63 is unreachable.** Depth `62` pushes at index 62; depth
`63` still runs `result` but **refuses the push** — depth stays 63, phase clears, return 0. A
reconstruction using 64 slots overflows the record by one entry.

**Negative depth passes the bound** (`movsxd`; signed compare). Depth `-1` writes the type byte at
`rbx+3` — **inside the depth dword itself** — making it `0x01FFFFFF`, then `inc` yields
`0x02000000`. A negative depth is self-repairing into garbage, not a fault.

**The id split is `sar` + `and 0xFFF`.** `id=0xFFFFFFFF` → family `-1` resolves `array[-1]` — the
executor's own arithmetic shift keeps the negative family (the pre-decode's `movzx` is what makes
`0..15` a *reachable* invariant, not the executor).

## Mutants — 9/9 detected

| mutant | patch | how it diverges |
|---|---|---|
| `sar`→`shr` family split | `0x262205` | id `0xFFFFFFFF` → family `0xFFFFF` → unmapped array read (fault) |
| `and 0xFFF`→`0x1FFF` | `0x26220C` | id `0x1FFF` → command `0x1FFF` reads the zeroed record — nothing runs |
| phase byte `+0x15`→`+0x16` | `0x262213` | phase-1 entry takes the phase-0 arm — `begin` runs |
| phase==1 `je`→`jne` | `0x26224F` | phase 1 goes straight to `result` |
| `test al,1` `je`→`jne` | `0x262305` | a running poll is treated as done — `result` runs, phase clears |
| `cmp al,2` `jae`→`jb` | `0x262283` | phase<2 takes the `==2` arm's `jne` — float push of `+0xC` |
| phase==2 `jne`→`je` | `0x262316` | `==2` takes the float arm |
| depth bound `0x3F`→`0x40` | `0x262289` | index 63 becomes writable |
| `+0xC` clear → `nop` | `0x2622B7` | `begin` observes the stale return slot |

## Limitations

- Callbacks are fixture-planted stubs; what real verbs do on the other side is out of scope by
  design (§16: scripting them tests the executor, not the interface).
- The `id`-decode case `0xFFFFFFFF` exercises the executor's own `sar`; the claim that shipped
  bytecode can only produce `0..15` families remains a *pre-decode* property, not re-proved here.
- `003DC2D0` (the table initialiser) is not driven — it was already executed by the 40th pilot.
- No live runtime, no real VM context; the live half (breakpoint on `002621D0` in a running game)
  remains ASTRA's queue item.


## SECTION-11 evidence consumption — 2026-09-23

The historical campaign remains exactly as recorded: fixture callbacks establish the executor,
not real verb semantics. Section11 independently checks14 retained order/phase/depth/return
observations and supplies8 corrupted-record controls, without rerunning the historical Unicorn
campaign. New146 original-instruction assertions connect real bytecode, family initialization,
wait/getmyid/getx/nowmap callbacks and selected request-driver paths. No planted callbacks or
application substitutions occur in that new fixture. Whole S-07 and live-game acceptance remain open.

[Review](evidence/continuation-section11-script-resume/REVIEW.md). Local production is validated;
formal independent acceptance remains pending. Historical source, raw records and audit status
are preserved.
