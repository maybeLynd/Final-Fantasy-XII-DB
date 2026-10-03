---
contract: Run a script's native command — id split, family table, begin/poll/result in one call
category: 01-Script-VM-Native-Bridge
scope: subsystem
level: L2
readiness: CONTRACT READY
confidence: PROVEN
implements: Native-Command-Lifecycle/native-command-lifecycle.md
entries: ["002621D0", "003DC2D0", "003DC270", "003DC240", "003DC2A0"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-22 (FABLE) on this document's own citations, every
    one resolving into a known section of the authority image; and §4's invariants re-measured from
    the shipping bytes — the five bodies' extents, all three accessors disassembled in full, the
    family-table initialiser read instruction by instruction with its four counts taken from the
    tables' own first dwords, and the last command's result slot resolved in all five tables.
    **This records checks performed on that date, not the method of the original derivation**, which
    is on the lifecycle page; see §15.
last_reviewed: 2026-09-29
audit:
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-native-lifecycle-falsification-pass-1
  crossref_clean: false
  reopened_count: 0
local_production_date: 2026-09-23
local_production_status: "SECTION-11 locally validated; formal independent acceptance pending"  # <- corrected 2026-10-02, OPUS - accepted non-author 2026-09-29 (SWE2-AUDIT-SEM, OV-18), as the lifecycle page records
---

> **Current production correction — SECTION-11, 2026-09-23.** Original interpreter, actual command callbacks, and selected request-driver paths execute together against synthetic state. Historical audit counters remain history, not acceptance of these changes. No new live game session or whole S-07/L2 acceptance is claimed. See [the section review](../_experiments/evidence/continuation-section11-script-resume/REVIEW.md).


# Contract — the native command lifecycle

> **Authored 2026-09-22 by FABLE.** S-07's binding gap is *"two subsystem contracts, but the
> interpreter core and the command lifecycle are uncontracted"*. This contract takes **the command
> lifecycle**; the interpreter core has its own contract and Section11 integrated evidence.
>
> Written against FRONTIER's adequacy test: *a narrower contract is adequate exactly when the
> system's operations have no cross-operation invariant or ordering it leaves unstated.* §4 is seven
> such invariants, and two of them are about a record layout that **interleaves adjacent commands**.

## 1. Purpose

Turn one packed command id from a zone script into a call, or into a wait that resumes on a later eligible invocation,
and hand the answer back to the script.

## 2. Interface

| | body | size |
|---|---|---:|
| execute | `VMNativeCommand_ExecuteLifecycle` (`002621D0`) | 461 B |
| build the family table array | `VMNativeCommandDispatch_InitializeFamilyTables` (`003DC2D0`) | 89 B |
| fetch `begin` | `003DC270` | 39 B |
| fetch `poll` | `003DC240` | 39 B |
| fetch `result` | `003DC2A0` | 41 B |

## 3. Types

```
family table array : 16 qwords at 02B57EF0
command table      : +0x00  int  count
                     row N at tbl + 32*N  —  see N-3, the rows are SHIFTED
```

| family | table | count |
|---:|---|---:|
| 0 | `01EED700` | 1,496 |
| 3 | `01F281B0` | 147 |
| 5 | `01F29418` | 1 |
| 7 | `01F29440` | 104 |
| all twelve others | `01F26720` | 212 |

*Every count above is the table's own first dword, read from the image.*

The execution state is the selected `ActorWaitSlot`: phase+15, payload+0C, saved ordinal+8 and
scratch+18. The append target is a `VmValueStack`, shared at02099AC0 when called by the interpreter.
These two objects must not be confused with the target actor or its indexed runtime control byte.

Begin receives issuer/target/scratch/stack in RCX/RDX/R8/R9 and manager as the fifth argument.
Poll receives issuer/target/scratch; R9 is not explicitly reloaded as a stack argument on that
call path. Result receives issuer/target/scratch/stack. These are callback-specific contracts,
not a universal four-argument signature.

## 4. Preconditions · postconditions · invariants

### The seven cross-operation invariants

**N-1 — The id's field widths decide the number of tables.** `002621D0` splits the id with
`sar 0xC` and `and 0xFFF`: **four bits of family, twelve of command for the interpreter's zero-extended WORD IDs**. Arbitrary direct 32-bit IDs retain the signed-shift precondition. There are sixteen family
slots because four bits admit sixteen, not because sixteen were wanted.

**N-2 — Twelve of the sixteen families alias to one table, so their ids are interchangeable.**
`003DC2D0` `rep stosq`s all sixteen slots with the default `01F26720` and then overwrites exactly
four — index 0, 3, 5 and 7 (`02B57EF0`, `+0x18`, `+0x28`, `+0x38`). **`0x2005` and `0x4005` resolve
to the same command.** *Whether that is deliberate aliasing or a fallback for unimplemented families
is `AO-1` and is not settled here.* *(answered: AO-1, 2026-09-12 — the shared table is family 2's and the other eleven are verb-less fallbacks, native-command-lifecycle.md section 7; 2026-10-02, OPUS)*

**N-3 — The record is SHIFTED: `result(N)` lives in row N+1, so adjacent commands interleave.** The
three accessors compute, all with the same `shl rax, 5`:

| callback | arithmetic | address |
|---|---|---|
| begin | `shl 5` then `[rax + rcx + 8]` | `tbl + 32N + 8` |
| poll | `shl 5` then `[rax + rcx + 0x10]` | `tbl + 32N + 0x10` |
| **result** | **`inc rax`** then `shl 5` then `[rax + rcx]` | **`tbl + 32(N+1)`** |

So one aligned 32-byte row holds `result(N−1)`, `begin(N)`, `poll(N)` and the unused slot — **the
result pointer of a command shares a row with the begin and poll of the next one.** *A reader who
lays out a 32-byte record as `{result, begin, poll, unused}` per command and indexes it by N will be
one row out on every result.*

**N-4 — And the data is authored for the shift: the last command's result slot is in bounds in every
table.** For the nonnegative decoded command IDs, the signed bounds check is `N < count`, which permits `result(count−1)` to read at `tbl + 32*count`
— one row past the counted rows. Resolved in all five tables, that read yields a **real function
pointer** in family 0 (`00342560`) and family 7 (`00510970`), and a valid NULL in the other three.
**Three tables are packed back to back with exactly the eight bytes that slot needs** — family 3's
rows end at `01F29410` and family 5's count begins at `01F29418`; family 5's end at `01F29438` and
family 7's at `01F29440`. *The layout is intentional authoring, not an overrun that happens to be
harmless.*

**N-5 — All three accessors refuse identically.** Null family-table pointer, or signed `N >= count`, yields
**NULL** rather than a fault — `test rcx, rcx` / `je`, then `cmp edx, [rcx]` / `jge`, in each of the
three. For valid decoded nonnegative IDs, missing callbacks are ordinary downstream inputs. This is not a lower-bound guard for arbitrary direct negative accessor arguments.

**N-6 — `begin`, `poll` and `result` are not three visits; they are one call that falls through.**
The executor reads the phase byte at `+0x15` of the command's state block and branches three ways,
but phase `0` runs `begin` and **falls through to `poll`**, and if `poll` reports not-running it
**falls through to `result` in the same call**. **An instantaneous command — one carrying only a
`result` — therefore completes on its very first invocation**, because the absent `poll` yields
"not running" from a zeroed local. *Only a command that polls busy ever leaves phase 1 behind for
the next invocation.* An implementation that visits the three phases on three successive frames would make
every one of the ~~1,155~~ single-callback commands take three frames instead of none *(corrected 2026-10-02, OPUS: family 0 has 1,288 single-callback records (1,189 `result` only, 73 `begin` only, 26 `poll` only), and all five tables 1,571 commands with a real `result` alone; the five command tables read under the accessor frame - begin `tbl + 8 + 0x20n` (`003DC28E`), poll `+ 0x10` (`003DC25E`), result `tbl + 0x20(n + 1)` (`003DC2BA`))*.

**N-7 — The fourth slot is NULL in all 1,960 records.** `tbl + 32N + 0x18` is never used. *This was
once recorded as "unused in every record but one"; the exception was a read past the end of family 0
landing on filler, and the correction is on the owning page.*

**And the answer's route back:** the finished command's return value is appended to a **63-entry**
result list, a structure of arrays with a count, a type tag and two value words per entry. The phase
byte encodes progress **and** return type (`AO-3`).

## 5. State

The initializer writes the sixteen family pointers; authored callback-table contents are inputs.
The issuer's selected ActorWaitSlot stores phase/scratch and results. The target actor may differ
from the issuer. The saved target is an ordinal and is looked up again when the lifecycle runs.
The interpreter supplies its shared image-backed stack; standalone callers supply an explicit stack.
The lifecycle does not allocate either of these objects or reset the stack at entry.

## 6. Relationships

| | |
|---|---|
| **Upstream** | the interpreter core — a separately specified part of S-07 |
| **Sibling** | [`CONTRACT-script-to-native-bridge.md`](CONTRACT-script-to-native-bridge.md) |
| **Downstream** | every native verb implementation reached through a callback |

## 7. State transitions

Phase0 clears result+0C, invokes begin if present, and then polls. Phase1 polls without re-running
begin. Entry phase>=2 proceeds directly to result handling. A poll with low bit1 sets phase1 and
returns1. Completion invokes the result callback if present, rereads phase for typing, conditionally
appends the result, resets phase0 and returns0.

An int writer selects phase2; a float writer selects phase3. These are transient on the tested
normal completion path, not permanent completed states. No result callback still produces an
implicit integer0 if capacity allows. Depth63 suppresses append but not the callback, result-store
write, phase reset or complete return.

The original wait begin/poll and three real result callbacks are integrated with bytecode in
Section11. A continued same-instruction invocation does not imply begin or argument pops run again.

## 8. Script · resource · event interactions

The five command tables are authored data. The authored verb catalog carries **1,954** names against
**1,960** distinct commands across the five tables; the two figures are close and **no claim is made
that they should be equal**.

## 9. Determinism

Deterministic. The dispatch draws no generator; whether an individual callback does is that
callback's business.

## 10. Failure paths and edge conditions

- A null family table or an out-of-range command yields NULL from all three accessors (N-5).
- A command with no `begin` takes an alternative path rather than failing.
- A command with no `poll` is treated as not running, which is what makes N-6's fall-through work.

## 11. Observable behaviour

A command can begin, poll, return a value and allow further bytecode during one interpreter
invocation. A pending command preserves scratch and phase while returning at the same CALL address.
No particular relationship between invocation count and live elapsed frames is established here.

## 12. Reproduction formula

Resolve `result(count−1)` in each of the five tables and assert it is in bounds and equals the value
the image holds at `tbl + 32*count`. Run a command with only a `result` callback from phase 0 and
assert it completes in **one** call. Resolve `0x2005` and `0x4005` and assert they yield the same
three callbacks.

## 13. Runtime validation

The old statement that none of these bodies was executed was stale. [EXP-085](../_experiments/EXP-085-verb-lifecycle-execution.md)
executed the executor and leaves with planted callbacks:35 producer cases including9 mutants.
Section11 independently checks14 selected retained order/return/phase/depth records and rejects8
corrupted-record controls; this is not a rerun of that complete campaign.

[Section11](../_experiments/evidence/continuation-section11-script-resume/REVIEW.md) additionally
executes original family initialization, wait begin/poll, nowmap/getmyid/getx result callbacks,
interpreter and selected full request-driver paths.146 original-instruction assertions and10
rejected private-code variants cover the integrated slice. Zero callbacks/application callees
are substituted. No fresh live session or complete verb population is claimed.

## 14. Unresolved

- Deliberate aliasing versus fallback authoring for the twelve shared table slots; complete catalog reconciliation.
- Other commands' scratch shapes, service effects, polling conditions and resource ownership.
- Actual frame scheduling and allocation identity across target reuse; synchronization/reentrancy.
- Authored reachability of malformed-stack, missing-callback and full-capacity conditions.
- Remaining interpreter opcode/wait families; selected integrated execution is not whole S-07 acceptance.

## 15. Evidence

| claim | evidence | tier |
|---|---|---|
| N-1 | `sar 0xC` and `and 0xFFF` in `002621D0` | 1 |
| N-2 and the four counts | `003DC2D0` read instruction by instruction — the `rep stosq` of 16, the four overwrites at slot 0, 3, 5 and 7 — with each count taken from its table's own first dword | 1 |
| N-3 — the shifted result row | all three accessors disassembled in full; `003DC2BA inc rax` before `shl rax, 5`, then a displacement of **zero** at `003DC2C1` | 1 |
| N-4 — the slot is in bounds in every table | `tbl + 32*count` resolved in all five: real function pointers in families 0 and 7, NULL in the rest; and the 8-byte packing between tables 3→5 and 5→7 | 1 |
| N-5 | the two refusal branches present identically in each accessor | 1 |
| N-6, N-7, the result list, `AO-3` | [the lifecycle page](Native-Command-Lifecycle/native-command-lifecycle.md) §§2, 11, 12, falsified twice 2026-09-02 | 1 |

## 16. Parity plan

L3 is out of scope. A reimplementation is judged on N-1 through N-7. **N-6 is the one to test first**
— three-visit phasing is the natural design and it would make ~~1,155~~ 1,571 *(corrected 2026-10-02, OPUS: the `result`-only commands of all five tables, the five command tables read under the accessor frame - begin `tbl + 8 + 0x20n` (`003DC28E`), poll `+ 0x10` (`003DC25E`), result `tbl + 0x20(n + 1)` (`003DC2BA`))* instantaneous commands take
three frames each. **N-3 is the one to get right in the data layout**, because being one row out on
every result is silent.

## 16a. Crossings into other layers (FABLE, 2026-09-22)

- **Script_VM_Native_Bridge — internal.** All five bodies are this category's own.
- **Every other layer reached is MECHANICAL**, through the executor's own callees and through the
  callbacks it dispatches to, which belong to whichever system implements the verb. *Those addresses
  are deliberately not cited: the callback targets span the whole engine, and naming any of them
  would import its edge set for no statement this contract makes.*

## 17. Related

- [The native command lifecycle](Native-Command-Lifecycle/native-command-lifecycle.md) — the mechanism
- [The ScriptVM native dispatch table](scriptvm-native-dispatch-table.md) — the table census
- [Contract — the script-to-native bridge](CONTRACT-script-to-native-bridge.md)

## Falsification pass 1 — 2026-09-29 (OPUS): every invariant survives

**Attack.** N-1 to N-5 became checks against the bodies and the tables' own bytes. Script:
`Tools/analysis-kit/gfz-scripts/falsify_native_lifecycle.py`, output `falsify_native_lifecycle.out`, image `73461d08…`,
0 BROKEN.

| # | Clause attacked | Result |
|---|---|---|
| L0 | §2 sizes | **survives**: 461 / 89 / 39 / 39 / 41 B |
| L1 | N-1 | **survives**: `sar 0xc` and `and 0xfff` in the executor |
| L2 | N-2 | **survives**: `rep stosq` of `01F26720` over `02B57EF0`, then the four specific tables at `02B57EF0`, `+0x18`, `+0x28` and `+0x38` |
| L3 | §3 counts | **survives**: 1,496 / 147 / 1 / 104 / 212 |
| L4 | N-3 | **survives**: begin `+8`, poll `+0x10`, result `inc rax` before `shl 5` |
| L5 | N-4 | **survives**: the past-the-end result slots are `00342560` (family 0), `00510970` (family 7) and NULL elsewhere; families 3 and 5 end at `01F29410` and `01F29438`, eight bytes before the next count |
| L6 | N-5 | **survives**: each accessor tests a null table and `N >= count` the same way |

No correction.

## Cross-subsystem neighbours — pass 22 (FABLE, 2026-09-29)

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page. Section 16a's heading is numbered, so the crossings gate does not read it; this section names each edge.*

**ActorEntity — SERVICE (1 edge).** The executor `VMNativeCommand_ExecuteLifecycle` (`002621D0`) calls `ActorManager_GetRecordByOrdinal` (`00358940`), a 30-byte bounds-checked read of the manager's record array that returns 0 for a negative or out-of-range ordinal. The executor looks up a manager record by ordinal through the actor layer's accessor; the wait slot and the value stack it drives stay this contract's.

**World — CLIENT (1 edge).** The area initialiser `00266D10` calls `VMNativeCommandDispatch_InitializeFamilyTables` (`003DC2D0`). Area initialisation is where the sixteen family-table pointers at `02B57EF0` are ~~(re)built~~ built, once *(corrected 2026-10-02, OPUS: `003DC2D0` is their only writer and is reached only through `00266D10` ← the boot routine ← the frame dispatcher's start-up step ← the start-up job (chain addresses in FABLE's record readiness-apply-fable-1002b); static)*, so the world layer owns when the dispatch tables are set up and this contract owns what they hold.

## Homed frontier bodies called from this page's functions (FABLE, 2026-10-02, cloud-drafted)

*Functions no page cited until now. Each is entered directly from a function this page already cites (the site is given as caller + offset). Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's homing pack and re-read by FABLE against the certified image; verified by [`homing_applier.py`](../_index/candidates/fable-home-contract-native-command-lifecycle-1002/homing_applier.py): every site transfers to its function, the page cites the caller, and every anchor is an instruction boundary inside its function that decodes to the recorded mnemonic.*

| function | size | entered from | what the body does | interior anchors |
|---|---|---|---|---|
| `0032A7A0` | 65 B | `00342560` + 0x13 | returns 0 when `ecx` is above 5 (unsigned); otherwise forms the record `qword 02EBF190 + 8 + cl * 0x1C8` (or a null base when `cl` is above 0x27) and returns 1 when its byte `+0x1C3` or byte `+0x1C4` is not 0xFF, 0 when both are 0xFF | Interior anchor `0032A7A5`; Interior anchor `0032A7B1`; Interior anchor `0032A7C6`; Interior anchor `0032A7CF`; Interior anchor `0032A7D8` |
