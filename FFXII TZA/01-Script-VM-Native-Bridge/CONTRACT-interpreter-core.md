---
contract: Interpret zone-script bytecode — one body, 100 opcodes, a stack of int32 and float32
category: 01-Script-VM-Native-Bridge
scope: subsystem
level: L2
readiness: CONTRACT READY
confidence: PROVEN
implements: Interpreter-Core/worldactor-scriptvm-interpreter.md
entries: ["0025E4C0"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-22 (FABLE) on this document's own citations, every
    one resolving into a known section of the authority image; and §4's invariants re-measured from
    the shipping bytes — the body's extent, all 100 dispatch entries decoded from the RVA table and
    rebased, the distinct-target count, every shared group enumerated, containment of all 100 targets
    tested against the body's own extent, and the two range compares read at their addresses.
    **This records checks performed on that date, not the method of the original derivation**, which
    is on the interpreter page; see §15.
last_reviewed: 2026-09-30
audit:
  passes: 1
  last_pass: 2026-09-30
  last_pass_kind: falsification
  last_pass_state: opus-interpreter-core-falsification-pass-1
  crossref_clean: false
  reopened_count: 0
local_production_date: 2026-09-23
local_production_status: "SECTION-11 locally validated; formal independent acceptance pending"  # <- corrected 2026-10-02, OPUS - accepted non-author 2026-09-29 (SWE2-AUDIT-SEM, OV-18), as the interpreter page records
---

> **Current production correction — SECTION-11, 2026-09-23.** Original interpreter, actual command callbacks, and selected request-driver paths execute together against synthetic state. Historical audit counters remain history, not acceptance of these changes. No new live game session or whole S-07/L2 acceptance is claimed. See [the section review](../_experiments/evidence/continuation-section11-script-resume/REVIEW.md).


# Contract — the interpreter core

> **Authored 2026-09-22 by FABLE.** S-07's binding gap named two uncontracted things — *the
> interpreter core and the command lifecycle*. The lifecycle is covered by
> [`CONTRACT-native-command-lifecycle.md`](CONTRACT-native-command-lifecycle.md) (commit
> `fb3117aea`); **this added the other contract**, not complete execution or semantic acceptance.
> Section11 below supplies a new bounded integrated execution slice.
>
> Written against FRONTIER's adequacy test: *a narrower contract is adequate exactly when the
> system's operations have no cross-operation invariant or ordering it leaves unstated.* §4 is six
> such invariants, and the sharpest is a disagreement between two ranges in the same dispatch
> prologue.

## 1. Purpose

Execute zone-script bytecode with typed numeric operations and native-command calls. Specify the
state that survives a returned invocation, including an in-flight command, without treating the
shared evaluation stack as persistent caller-frame storage. This contract covers a bounded
execution slice; the complete opcode and native-verb populations remain larger.

## 2. Interface

| Interface | Original location and actual role |
|---|---|
| Interpreter | `0025E4C0`, 14,646 bytes; RCX manager, RDX issuing actor, R8 its selected `ActorWaitSlot` |
| Script driver | `0025DF00`; selects actor `+0xA8 + sign_extend(actor[+0x11])*0x28` before the runnable branch |
| Native lifecycle | `002621D0(manager, issuer, stack, packed_id, request)` |
| Dispatch | `00261DF8`, 100 DWORD RVAs relative to `00120000` |
| Lengths | Signed WORD at `01EFEA60 + opcode*24` |
| Evaluation stack | Static image storage `02099AC0`, extent `0x284`, not the interpreter's stack frame |
| Tested returns | A busy native call yields interpreter return 0; stopping/budget/gate exits tested here return 1. This is not a complete error/success taxonomy. |

The bytecode base, selected request and request-result writers must agree with the actor's active
request index. The fixture tests both index 0 and index 1; arbitrary negative indices are not made
safe by their signed representation.

## 3. Types

`VmValueStack` has depth, tag, source-kind, reserved-word and numeric-value arrays. In the interpreter
it is the shared object at `02099AC0`. Every interpreter entry sets **depth** to zero; it does not
clear the arrays or restore the previous actor's stack.

`ActorStorageRecord` holds persistent integer registers `+0x64..+0x70`, float registers
`+0x74..+0x80`, bytecode and label bindings. `ActorWaitSlot`, stride `0x28`, holds the kind-selected
head: for execution, QWORD PC at `+0`, saved native target ordinal at `+8`, result/comparison value
at `+0x0C`, accumulator at `+0x10`, kind at `+0x14`, phase at `+0x15`, and command scratch beginning
`+0x18`. Other wait kinds overlay this same storage; do not impose one interpretation on all kinds.

Integer arithmetic is not universally float arithmetic. Tested int addition wraps at 32 bits;
mixed numeric addition uses float32, and float-to-int pops truncate. Helper call counts do not
establish the arithmetic type of every opcode.

## 4. Preconditions · postconditions · invariants

**I1 — Preserve the correct state, not the whole evaluation stack.** Entry `0025E4D8` resets shared
depth even when the actor gate then refuses execution. Actor registers and selected request fields
survive. Popped argument values needed after a yield must be saved by the command/operation.

**I2 — A busy CALL retains both its instruction and its phase/scratch.** It returns with the PC at
the CALL, not at the literal arguments preceding it. Phase 1 resumes polling without rerunning begin.
The original `wait` begin/poll demonstrates this through repeated interpreter invocations.

**I3 — Re-fetch is not reinitialization.** Re-reading CALL on resume must not repeat phase-zero
argument pops, target selection or side effects. `CALLACT` saves an ordinal and the lifecycle resolves
that ordinal again; it does not guarantee stable allocation identity for the original target.

**I4 — There are distinct epilogue entries.** `0025E60A` requests a stop; `0025E613` performs the
common length advance without setting that request. The loop at `0025E570` stops on a requested
stop with empty depth, but discards nonempty depth and continues. An extra value below a busy
command's argument can therefore cause another poll in the SAME invocation (synthetic control).

**I5 — Neither a table target nor return 1 guarantees forward PC progress.** Lengths are 0 for
opcodes 00..02, 1 for 03..47, and 3 for 48..63. Opcode00 at zero depth runs to the 65,536-iteration
budget without advancing; 01 stops at the same address; 03 sets actor flag40 and cancels its own
advance. A self-jump also exhausts the budget. Budget exhaustion publishes the current PC.

**I6 — Predecode is a real memory access.** Opcodes >=47 read two following bytes before dispatch;
47 itself is length1. An isolated guard-page control faults at `0025E5AF` reading PC+2, whereas
19 at the same page edge stops safely. An unused operand is not a harmless inaccessible read.
Opcodes >63 still reach an opcode-indexed length lookup outside the documented 100 rows; this
contract does not promise their progress, memory safety or equivalence to a valid marker.

**I7 — Completion and result delivery differ.** A finished command resets phase0. It may append an
int/float or an implicit zero. Depth63 suppresses append even though result storage is written and
completion succeeds. Callback target identity is distinct from the issuing result-record owner.

**I8 — Valid memory and proper scheduling remain preconditions.** Fixture branches exercise selected
original code; they do not supply synchronization for a global stack, bound every authored table,
or prove script reachability, arbitrary reentrancy or real frame timing.

## 5. State

| Storage | Lifetime and footprint established here |
|---|---|
| Shared `02099AC0` | Image-backed storage. Depth reset per entry, arrays retained until overwritten. No per-call allocation/free. |
| Issuer registers | Persist across returns and another actor's invocation in the fixture. |
| Request PC/phase/scratch | Survive native wait; PC advances past CALL only after completion. |
| Request accumulator | Written/read by bytecodes and the POPA call forms; survives the next interpreter entry. |
| Command target | Saved ordinal at request+8; manager lookup is repeated by lifecycle. |
| Bytecode/labels/pools | Caller-bound synthetic inputs in these tests. Full resource lifetime not established *(answered: OV-17 — every shipped operand in range, tables live as long as the bound payload; 2026-10-02, OPUS)*. |

The full original `0025DF00` was executed for selected runnable requests and idle service branches;
it clears its active-actor global afterward. This is not the entire outer field-frame driver.

## 6. Relationships

`0025DF00` selects a runnable request -> `0025E4C0` executes bytecode -> `002621D0` runs native
begin/poll/result -> an original result writer uses the issuing actor's selected request -> the
interpreter consumes the result and continues or returns.

See [command lifecycle](CONTRACT-native-command-lifecycle.md),
[the bridge](CONTRACT-script-to-native-bridge.md), and
[the connected mechanism](Interpreter-Core/the-script-from-bytecode-through-wait-and-resume.md).
An actor's indexed control byte consulted by some polls is NOT the request's command phase.

## 7. State transitions

For original `wait(2)` under the tested raw-count predicates: first begin consumes2 and poll leaves1,
phase1/PC-at-CALL; second invocation polls to0, still busy; third polls to-1, completes, supplies
implicit integer0 and executes following bytecode. Phase resets0. This is a sequence of poll
invocations, not an assertion about elapsed game frames or seconds.

Wait0 can complete in the first interpreter invocation. Timing predicates can scale an authored
count; a separate original-code control makes3 become6 before the first decrement.

A blocked actor gate discards previous evaluation depth while preserving the request PC and actor
registers. Marker stops, busy returns, actor-halt, and instruction-budget exhaustion are different
transitions and must not be implemented as one generic successful instruction.

### Cross-actor request scheduling — SECTION-12 (2026-09-24)

Original `REQSW` (24) and `REQEW` (27) each arm kind4 at their continuation PC. Mode2 generates
its requester notification when the target entry starts. Mode3 does so when the target entry is removed: on RET,
or when a mode-4 `freqcancel` recycle (`003DB420`) removes the target as its channel head without running it
(FABLE 2026-10-02, [review](../_index/candidates/fable-review-astra-request-cancel-notification-1002/REVIEW.md)).
The former permits caller continuation before target bytecode runs; the latter waits for removal, which is
normally, but not necessarily, the target's return.
The requested target is separate from the issuer whose class/counter selects immediate versus
filed-only insertion. Notifications use the requester's ordinary entry capacity and can fail
without undoing target progress. A mode-3 end notification is attempted before the removed entry is relinked onto
the free list, so a self-requested notification on an already-full pool is refused even though the removal then
frees a slot. The removal's return is the entry's `+0x12` bit 0, not a delivery result
([the actor request](Interpreter-Core/the-actor-request-from-arming-through-start-and-return.md) section 3; a
conditional static reading, premises there; FABLE 2026-10-02). Their match key is channel plus low32 continuation offset, not
a new generation-bearing identity.

Opcode32 uses original entry lookup/encoding to arm kind3 only while a matching entry exists.
Original driver kinds3/5/6/7 hold on an active dependency; kind4 holds on a MISSING notification.
A satisfied wait can switch to kind1 and execute subsequent bytecode in the same driver call.
Kinds5/7 keep a forward cursor and do not rescan previously passed actors. These claims are
isolated original-instruction evidence, not live-frame counts or proof of arbitrary input safety.

[The request mechanism](Interpreter-Core/the-actor-request-from-arming-through-start-and-return.md)
and [production evidence](../_experiments/evidence/continuation-section12-actor-request-waits/REVIEW.md)
preserve exact claims and remaining capacity, caller, lifetime and scheduling boundaries.

## 8. Script · resource · event interactions

Original callback tables are initialized by `003DC2D0`; selected real commands are wait0000,
getmyid0072, getx006D and nowmap0090. The fixtures use controlled bytecode, labels, constants,
actor tables and save-state fields. No callbacks are planted. No authored script corpus, resource
load transition, fresh actor allocation or whole event sequence is certified.

## 9. Determinism

For pinned code and identical fixture state the repeated execution matches. Script results depend
on current globals, callback behavior and preserved actor/request state, not bytecode alone.
A shared evaluation stack and reused actor pointers do not establish thread safety or generation
fencing. The existing ASTRA live register-reuse task remains separate.

## 10. Failure paths and edge conditions

Entry resets depth before refusal; zero-length opcodes can retain the PC; the instruction budget
bounds this tested loop but does not make all malformed bytecode safe. Inaccessible predecode
bytes can fault. The original diagnostic forwarding leaf ultimately reaches the shipped return
stub on reached paths; no host substitute is installed for it.

Unknown/empty callback entries can complete with implicit0. A full evaluation stack silently loses
the result append. Manager ordinal lookup, signed request indices and bytecode/label/data pointers
retain their actual native preconditions, not added reconstruction guards.

## 11. Observable behaviour

The fixture distinguishes persistent registers and scratch from a discarded shared stack, and
shows continued bytecode after a command completes. These are isolated original-code observations,
not screen output or a running-game timing measurement.

## 12. Reproduction formula

Run the Section11 driver against the pinned EXE and historical database inputs. Compare PC, actor
registers, request phase/scratch/accumulator, stack depth/tags, and selected peer state. Use two actors
and conflicting target/control values so an accidental receiver substitution cannot look correct.
The baseline includes full selected-driver entries, not a stubbed interpreter. Guard-page and
wrong-code controls explicitly discriminate the corrected claims.

## 13. Runtime validation

**Current: isolated original-instruction execution.** Section11 supplies146 named assertions,
an identical repeat and10 rejected private-code variants. The interpreter, family initializer,
selected real callbacks and full selected-kind request driver run with **zero application
substitutions and zero import bridges**. Synthetic input/state are not live observations.

Earlier EXP-106 ran surrounding driver machinery with the interpreter scripted. EXP-085 ran the
lifecycle with fixture callbacks. Those results are preserved; their bounded scopes are now
connected by new evidence rather than relabeled as prior integrated execution.

No fresh FF12 session, full Unicorn campaign or complete 100-opcode coverage is claimed.

## 14. Unresolved

- Remaining opcode semantics, variable/reference forms, actor-call/return stacks and other wait kinds *(answered in part: opcode semantics and actor-call/return BF-1 / OV-13, other wait kinds OV-14 — the-script-from-bytecode-through-wait-and-resume.md section 8; 2026-10-02, OPUS)*.
- Live allocation identity and register reuse; scheduling, reentrancy and synchronization obligations.
- Full top-level field-frame composition, nonempty service branches and all native-command callbacks.
- Authored operand/index bounds and resource lifetime for bytecode, label tables and constant pools *(answered: OV-17, same section 8; 2026-10-02, OPUS)*.
- Meaning/producer scope of the actor-indexed control byte; it is not commandPhase by displacement *(answered: the target manager's skip mask `+0x201`, OV-15; `00267310` reads `02099011 + sx(idx)*0x288`; 2026-10-02, OPUS)*.
- Family-alias authoring rationale and unobserved class-specific behavior. These are not waived by
  the selected passing slice.

The old no-execution statement and claims of an always-progressing epilogue or no resume state are
superseded, not silently treated as previously proved.

## 15. Evidence

[Section11 review](../_experiments/evidence/continuation-section11-script-resume/REVIEW.md),
[original disassembly](../_experiments/evidence/continuation-section11-script-resume/original_disassembly.txt),
[dispatch/length rows](../_experiments/evidence/continuation-section11-script-resume/opcode_dispatch_lengths.tsv),
[146 assertions](../_experiments/evidence/continuation-section11-script-resume/results/native_baseline.json),
[scope](../_experiments/evidence/continuation-section11-script-resume/scope.json).

Historical audit receipts remain attached to their prior text. Local production is not independent
acceptance, a new numbered EXP, or an automatic S-07 gate promotion.

## 16. Parity plan

L3 implementation remains later. Tests of database sufficiency should preserve actual PC/phase/
scratch transitions, stack disposal, result typing and target ownership. Do not introduce a fresh
per-call stack lifetime, three-frame command phasing, universal PC advancement or guaranteed result
append. Extend the original-code slice into remaining opcode/wait mechanisms with explicit inputs
and discriminating controls; do not rerun settled cases merely to inflate counts.

## 16a. Crossings into other layers (FABLE, 2026-09-22)

- **Script_VM_Native_Bridge — internal.** The body is this category's own.
- **Movement — MECHANICAL.** The interpreter is *called from* that layer's per-unit pump, which is
  how a script gets ticked at all. That is an upstream caller, not a shared responsibility: nothing
  in §4 is a statement about movement.
- **Every other layer reached is MECHANICAL**, through the interpreter's own callees — the value
  stack, the actor manager, the actor-resource accessors and the pointer helpers. *Their addresses
  are deliberately not cited beyond the value-model names in §3: each is a hub, and naming one
  imports its whole edge set for a statement this contract does not make.*

## Cross-subsystem neighbours — pass 22 (FABLE, 2026-09-29)

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page. Section 16a's heading is numbered, so the crossings gate does not read it; this section names each edge.*

**ActorEntity — SERVICE and CLIENT (18 edges).** The script driver `0025DF00` calls `00359B80`, `ActorResource_RemoveActiveEntry` `003DB2A0`, `ActorResource_GetEntryByOrdinal` `003DB550`, `ActorResource_IsChannelBitActive` `003DB640`, `ActorResource_FindActiveEntryByIdOrClass` `003DBF60` and `ActorResource_FindScriptRequestEntry` `003DC050`, and is called by `ActorManager_RunFieldRuntimePass` `0025D9E0`; the interpreter `0025E4C0` calls `00268EA0`, `003587C0`, `ActorManager_GetRecordByOrdinal` `00358940`, `003DB2A0`, `ActorResource_RecycleEntryRange` `003DB420`, `003DB550`, `003DB640`, `ActorResource_SelectPendingEntryForExecution` `003DB6E0`, `ActorResource_StartEntryScriptExecution` `003DBDC0` and `003DBF60`; and the native lifecycle `002621D0` calls `00358940`. The request entries the driver selects and the interpreter runs, retires and recycles are the actor layer's `ActorResource` records, and the actor manager's field runtime pass is what runs the driver for each actor.

**Movement — CLIENT and SERVICE (6 edges).** The driver `WorldActor_UpdateRuntimeAndScriptExecutionState` `0025DF00` is itself filed to Movement in the census, and it calls the interpreter `0025E4C0`; it also calls `Movement_SetRequestedSpeed` `0026D6F0`, `002E4A10`, `Movement_UpdateActorFrame` `002E5030`, `002E5750` and the record-kind gate `002E6310`. The same per-actor update that selects and runs a script request also copies the movement context's position (`002E4A10`) and runs the steering dispatch, so script execution and locomotion share one driver; this contract claims only the request selection and the interpreter call.

**Presentation — SERVICE (3 edges).** `0025DF00` calls `003E68B0`, `003E6A70` and `003E6EF0`. Each is a wrapper that resolves the actor's `+0x550` character-render sub-record through a shared gate and forwards to one render-record query, and their results feed the driver's steering dispatch; they are not part of the interpreter.

**World — CLIENT (1 edge).** The area initialiser `00266D10` calls `VMNativeCommandDispatch_InitializeFamilyTables` `003DC2D0`. The native-command callback tables of section 8 are installed during area initialisation.

## 17. Related

- [The WorldActor ScriptVM interpreter](Interpreter-Core/worldactor-scriptvm-interpreter.md) — the mechanism
- [Contract — the native command lifecycle](CONTRACT-native-command-lifecycle.md) — S-07's other half
- [The ScriptVM native dispatch table](scriptvm-native-dispatch-table.md)

## Falsification pass 1 — 2026-09-30 (OPUS): every clause tested survives

**Attack.** The contract's static clauses were turned into checks at the interpreter's own instructions and tables.
The ten facts it shares with the script-resume page run first (R1–R10, `falsify_script_resume.py`), then six of its
own (K1–K6). SECTION-11/12's executions are carried, not re-run. Script:
`Tools/analysis-kit/gfz-scripts/falsify_interpreter_core.py`, output `falsify_interpreter_core.out`, image
`73461d08…`, 0 BROKEN, exit 0.

| # | Clause attacked | Result |
|---|---|---|
| R1–R10 | I1, I4, I5, I6, I7 and §2's driver, table and lengths (the facts shared with the script-resume page) | **all survive**. Depth reset at `0025E4D8`; budget `0x10000`; 100 targets at `00261DF8`; advance words 0/1/3 at `01EFEA60 + op·24`; opcode 03's flag `0x40`; stop at `0025E60A`, advance at `0025E613`; the depth < 63 append in `002621D0`, stack passed by pointer; the `+0xA8 + sx(+0x11)·0x28` request address; the `02099011 + sx·0x288` poll byte; the pre-dispatch decode for opcodes ≥ `0x47` |
| K1 | §2 the interpreter is 14,646 bytes | **survives** |
| K2 | §2 the stack's extent is `0x284` | **survives**. `002621D0` writes four indexed arrays at `+0x04` (byte), `+0x44` (byte), `+0x84` (dword) and `+0x184` (dword), so 64 entries end at `+0x284` |
| K3 | I5 opcode 00 does not advance, and 01 stops at the same address | **survives**. Opcode 00's table entry is the plain advance `0025E613`, with length 0. Opcode 01's is the stop entry `0025E60A`, which falls into that advance |
| K4 | I6 opcodes above `0x63` still reach the length lookup | **survives**. The advance reloads the saved opcode byte (`movzx edx, [rsp + 0xb8]`) and indexes `01EFEA60` with it, with no bound |
| K5 | §3 integer registers `+0x64..+0x70`, float registers `+0x74..+0x80` | **survives**. The interpreter addresses all eight through `r15`, the actor record |
| K6 | §7 REQSW (`0x24`) and REQEW (`0x27`) arm kind 4 | **survives**. Both arms' control flow reaches one shared store, `002602EE mov byte [rsi + 0x14], 4` |

**Verdict.** The contract's static facts hold. Tier 1 (static).
