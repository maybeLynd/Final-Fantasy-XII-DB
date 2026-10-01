---
system: Bytecode to original native command and resumed request
category: 01-Script-VM-Native-Bridge
status: PARTIAL
owner_layer: PrimaryOwner:Script_VM_Native_Bridge
evidence_tier: 2
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: "SECTION-11 isolated original-instruction execution; static table and range verification"
last_reviewed: 2026-09-30
local_production_status: "Locally validated; independent acceptance pending"
audit:
  passes: 1
  last_pass: 2026-09-30
  last_pass_kind: falsification
  last_pass_state: opus-script-resume-falsification-pass-1
  crossref_clean: false
---

# A script from bytecode through wait and resume

## 1. The mechanism this section connects

The original actor request driver selects a slot. The interpreter executes bytecode using a shared
numeric stack. A CALL enters the native lifecycle. A busy command preserves request phase and
scratch, and the interpreter returns with its program counter at that CALL. A later eligible
invocation polls again without repeating begin. Completion produces a typed/default result,
resets the phase and permits following bytecode to run.

This is now demonstrated with original code on both sides of the former experiment boundary:
`0025DF00 -> 0025E4C0 -> 002621D0 -> real callback -> real result writer -> interpreter`.
EXP-106 had scripted the interpreter; EXP-085 had planted callbacks. Neither historical experiment
is retrospectively relabeled as the new integrated test.

## 2. The state that must survive

| Storage | What the tested code does |
|---|---|
| Evaluation stack02099AC0 | Resets depth on every interpreter entry, including refusal; keeps old array bytes. |
| Actor integer/float registers | Survive a returned invocation and another actor's run in the fixture. |
| Request+00 | Holds the bytecode PC for runnable execution. Other wait kinds overlay it. |
| Request+08 | Holds a native-command target ordinal, not a generation-bearing allocation reference. |
| Request+0C | Holds command result bits and supports selected comparison operations. |
| Request+10 | Holds the interpreter accumulator, including CALLPOPA results. |
| Request+15 | Holds begin/poll/result phase; not the actor-indexed control byte consulted by some polls. |
| Request+18 onward | Command-/kind-specific scratch; original wait stores a signed countdown here. |

A reimplementation that gives the interpreter an unrelated persistent private stack would diverge.
So would one that reconstructs only the PC but discards phase, target and scratch before resuming.
No concurrency or arbitrary reentrancy guarantee follows from these local rules.

## 3. An actual waiting command

The fixture executes this controlled stream (opcodes and operands below are hexadecimal):

```text
4F 02 00       signed literal 2
58 00 00       CALL original wait (family0 command0)
36             consume its implicit int0 into actor I0
4F 63 00       signed literal99
37             write actor I1
19             stop-request marker
```

With the selected raw-count predicates:

| Invocation | Countdown after poll | Request phase | Saved PC | Interpreter return |
|---|---:|---:|---|---:|
| First | 1 | 1 | CALL at stream+3 | 0 |
| Second | 0 | 1 | CALL at stream+3 | 0 |
| Third | -1 | 0 | After the final marker | 1 |

Begin pops the argument only on the first invocation. The third invocation consumes the result,
writes I1=99, and stops. A separate wait0 completes within its first invocation. Another controlled
predicate combination scales3 to6 before the first decrement. These are invocation/countdown
observations, not a claim about exact frames, seconds or shipped compiler output.

## 4. Target identity and result ownership

CALLACT and CALLACTPOPA save the popped target ordinal. The original lifecycle re-resolves that
ordinal through the manager whenever needed. It passes the selected target separately from the
issuer. Original getmyid can therefore return actor1's identity into actor0's selected request.

The result writers compute the issuing request from actor+0xA8 and signed actor+0x11 times0x28.
The fixture checks request indices0 and1, preserving the unselected result slot.

Changing the manager's ordinal mapping between polls changes the target read on the next resume.
That synthetic rebind is NOT a live actor-allocation identity test, and does not prove safe handling
of a stale callback or recycled slot.

The wait poll reads a byte selected by target actor+0x15 through
`02099011 + sign_extend(index)*0x288`. Command phase instead lives at request+0x15. Varying these
independently disproves the earlier claim that this is merely the request's own reentrancy guard.
*Answered 2026-09-29 (OV-15; `_index/candidates/ov15-skip-mask-fable/`):* the indexed control is the target manager's skip mask (manager record `+0x201`; the world-tick page names it). A skip begin (script command 1337, or the engine's loop over managers 1-3) sets its bits, and a skip end clears them. The bind writes it 0. The wait poll zeroes its countdown while the mask is non-zero, so a skipped wait ends by its second poll; 72 call sites consult the mask through the same reader.

## 5. Result delivery can be lost without denying completion

Original nowmap returns an integer; original getx returns float bits; getmyid uses the target.
The lifecycle rereads the result phase, appends if depth<63, resets phase0 and reports completion.

At depth63, the callback still writes request+0C but no new stack value is appended. A caller must
not treat completion as proof that a result was delivered. A command with no callbacks supplies
an implicit integer0 when space permits; missing callback is not always an error.

The tests use original family initialization and shipped callback addresses. No successful
callback stand-ins or application replacements are installed.

## 6. Stopping, empty opcodes and the stack-discard boundary

`0025E60A` sets a stop request; `0025E613` advances without newly setting it. At the loop boundary,
a requested stop returns if depth is empty; otherwise it clears depth and continues. This can
poll a busy CALL again during the SAME invocation when another operand was left beneath its
arguments. That is a tested synthetic state, not a compiler-reachability claim.

The length table gives0 to opcodes00..02,1 to03..47, and3 to48..63. With empty depth, opcode01
returns at the same address; opcode00 runs to the65,536-iteration budget without advancing.
Opcode03 sets actor flag40 and cancels its advance. A self-jump likewise needs the budget.
A finite budget is not general validation of malformed code or memory references.

Opcode47 reads PC+2 and PC+1 even though its length is1 and the decoded value is unused. An
isolated guard-page child proves the PC+2 access can fault; opcode19 at the same boundary returns
without that read. Out-of-table opcode lengths and every malformed input are not certified.

## 7. Validated scope

Section11 has146 named assertions, an identical repeat and10 targeted wrong-code variants that
fail their intended checks. It runs the full original0025DF00 entry for selected runnable kind1
and configured idle service branches. It does NOT run the complete outer0025D9E0 frame pipeline.

No application substitution, import bridge, game startup, OS I/O or fresh live session is used.
State is synthetic. Existing EXP-085 records receive14 selected consistency checks and8 corrupted
controls; the historical Unicorn campaigns are not rerun. Only tested/arithmetic/control paths
are established; inclusion in the58-body manifest is not instruction coverage.

## 8. Remaining obligations

- [x] ~~Complete other interpreter opcode families, actor-call/return and request-arming transitions.~~ *ANSWERED 2026-09-29 (SWE2-FRONTIER): BF-1 (71859306c) read all 100 interpreter opcodes; actor-call/return and request-arming are on the actor-request page. Register OV-13.*
- [x] ~~**OV-14.** Establish other wait kinds and nonempty external service behavior at the required grain.~~ *ANSWERED 2026-09-29 (FABLE, applied by SWE2-FRONTIER): wait kinds on the actor-request page §5/§7 with a store census; the unspecified service-behavior half is a class-1 declared limit. Register OV-14; record `_index/candidates/ov14-wait-kinds-fable/`.*
- [x] ~~**OV-15.** Trace the relevant control-byte producers and their actual native meaning.~~ *ANSWERED 2026-09-29 (FABLE): the byte is the target manager's skip mask (manager record `+0x201`); [`_index/candidates/ov15-skip-mask-fable/`](../../_index/candidates/ov15-skip-mask-fable/README.md), `skip_mask.py` A C R W I FAILS 0. Register OV-15.*
- [ ] **OV-16.** Establish live scheduling, synchronization, reentrancy and allocation-identity requirements where needed.
- [x] ~~**OV-17.** Establish bytecode/label/constant resource lifetime and authored input constraints.~~ *ANSWERED 2026-09-29 (FABLE, applied by SWE2-FRONTIER): all operands in range across every shipped script; tables live as long as the bound payload. Register OV-17; record `_index/candidates/ov17-constant-bounds-fable/`.*
- [x] ~~Obtain independent acceptance and propagate accepted claim-specific L2 consequences without self-promotion.~~ *NOT A QUESTION 2026-09-29 (SWE2-FRONTIER) under the class-2 ruling: an independent-acceptance/process item, carried by board task FABLE-CARRIER-SECTION-OVERLAY-ACCEPTANCE-0929. Register OV-18.*

## 9. Evidence and related contracts

[Section review](../../_experiments/evidence/continuation-section11-script-resume/REVIEW.md) ·
[Native assertions](../../_experiments/evidence/continuation-section11-script-resume/results/native_baseline.json) ·
[Scope](../../_experiments/evidence/continuation-section11-script-resume/scope.json) ·
[Interpreter contract](../CONTRACT-interpreter-core.md) ·
[Command lifecycle](../CONTRACT-native-command-lifecycle.md) ·
[Bridge](../CONTRACT-script-to-native-bridge.md).


## Follow-on evidence: actor requests and non-kind-1 waits (SECTION-12, 2026-09-24)

[The new request specification](the-actor-request-from-arming-through-start-and-return.md)
connects original bytecode submission to start/end notifications and same-call continuation.
It adds ordered list waits and notification exhaustion without rerunning this section's completed
countdown campaign. The earlier lack of non-kind-1 coverage is this section's historical boundary,
not a claim that the follow-on evidence is absent. Whole-frame timing, actor allocation reuse and
remaining opcode/service semantics are still separate obligations.

## Falsification pass 1 — 2026-09-30 (OPUS): every static fact under the executions survives

**Attack.** The page's claims rest on SECTION-11's isolated executions. This pass attacks the static facts those
executions depend on, at the interpreter's own instructions and tables; the executions are carried, not re-run. Script:
`Tools/analysis-kit/gfz-scripts/falsify_script_resume.py`, output `falsify_script_resume.out`, image `73461d08…`,
0 BROKEN, exit 0.

| # | Clause attacked | Result |
|---|---|---|
| R1 | §2 the stack depth at `02099AC0` is reset on every interpreter entry | **survives**. The interpreter's first reference to it is the store `0025E4D8 mov [02099AC0], r11d`, and `r11d` is zeroed before it |
| R2 | §6 the budget is 65,536 | **survives**: `0025E4FA mov ecx, 0x10000` |
| R3 | §6 100 opcodes through one table, a default above | **survives**. `0025E5D1 cmp eax, 0x63` / `ja 0025E60A`. The image-relative table at `00261DF8` has 100 targets, all inside the interpreter |
| R4 | §6 lengths 0 for 00..02, 1 for 03..47, 3 for 48..63 | **survives**. The advance is the signed word at `01EFEA60 + op·24`, read at `0025E5FE` and `0025E631`, and all 100 match |
| R5 | §6 opcode 03 sets actor flag 0x40 and cancels its advance | **survives**. Arm `0025E5EA`: `or byte [r15 + 0x14], 0x40`, reloads the advance word, `sub r14, rax` |
| R6 | §6 `0025E60A` sets a stop request, `0025E613` advances without setting it; opcode 19 is the marker | **survives**. `0025E60A mov [rsp + 0xc0], ebp` with `ebp = 1` set before; `0025E613` begins the advance path. `0025E60A` is also the out-of-range default, and opcode 19's table entry |
| R7 | §5 a result is appended only while depth < 63 | **survives**. `002621D0` receives the stack by pointer: all three of the interpreter's calls pass `r8` = `02099AC0` (value flow, through `r10`). It reads depth as `movsxd rax, dword [rbx]` (`00262280`), and three `cmp eax, 0x3f` / `jge` bounds skip the append (`00262289`, `0026231B`, `0026233F`) |
| R8 | §4 the issuing request is `actor+0xA8 + sx(actor+0x11)·0x28` | **survives**. 12 sites in 7 functions load `sx(byte [r + 0x11])` with a `0x28` stride beside `[r + 0xA8]`, among them the driver `0025DF00` and the interpreter |
| R9 | §4 the wait poll reads `02099011 + sx(index)·0x288` | **survives**. One reference to `02099011`; the functions pairing it with the `0x288` stride are `00264830` and `00267310` |
| R10 | §6 opcode 47 reads PC+2 and PC+1 although its length is 1 | **survives**, and the pass shows why. The operand decode before dispatch runs for every opcode ≥ `0x47` (`0025E5A9 cmp r12b, 0x47` / `jb`, then `movzx ebx, [r14 + 2]`, `movzx eax, [r14 + 1]`). The length table starts its 3-byte range at `0x48` (R4). Opcode 47's own table entry is the default arm `0025E60A`, so the value it decodes is unused |

**Verdict.** Every static fact the executions rely on holds in the shipping image. The pass adds one reason to R10: the
decode threshold (`0x47`) and the length table's (`0x48`) differ by one. Tier 1 (static).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (SWE2-CONTRACT)

- **ActorEntity — CLIENT and SERVICE (18 edges).** 1 inbound (ActorEntity bodies `ActorManager_RunFieldRuntimePass` (0025D9E0) call page-cited `WorldActor_UpdateRuntimeAndScriptExecutionState` (0025DF00)); 17 outbound (page-cited `WorldActorScriptVM_InterpretBytecode` (0025E4C0), `WorldActor_UpdateRuntimeAndScriptExecutionState` (0025DF00), `VMNativeCommand_ExecuteLifecycle` (002621D0) call ActorEntity bodies `ActorResource_RemoveActiveEntry` (003DB2A0), `ActorResource_FindActiveEntryByIdOrClass` (003DBF60), `ActorResource_GetEntryByOrdinal` (003DB550)). Substantive edges include `WorldActor_UpdateRuntimeAndScriptExecutionState` (0025DF00) is called by `ActorManager_RunFieldRuntimePass` (0025D9E0); `WorldActor_UpdateRuntimeAndScriptExecutionState` (0025DF00) calls `ActorResource_RemoveActiveEntry` (003DB2A0); `WorldActor_UpdateRuntimeAndScriptExecutionState` (0025DF00) calls `ActorResource_FindActiveEntryByIdOrClass` (003DBF60); `WorldActor_UpdateRuntimeAndScriptExecutionState` (0025DF00) calls `ActorResource_GetEntryByOrdinal` (003DB550); the remaining edges run through shared helpers the page cites.
- **Movement — CLIENT and SERVICE (8 edges).** 3 inbound (Movement bodies `WorldActor_UpdateRuntimeAndScriptExecutionState` (0025DF00), `Movement_UpdateSteeringTowardTarget` (002E45E0), `002E5750` call page-cited `00267310`, `WorldActorScriptVM_InterpretBytecode` (0025E4C0)); 5 outbound (page-cited `WorldActor_UpdateRuntimeAndScriptExecutionState` (0025DF00) call Movement bodies `002E6310`, `Movement_UpdateActorFrame` (002E5030), `002E4A10`). Substantive edges include `WorldActor_UpdateRuntimeAndScriptExecutionState` (0025DF00) calls `002E6310`; `WorldActor_UpdateRuntimeAndScriptExecutionState` (0025DF00) calls `Movement_UpdateActorFrame` (002E5030); `WorldActor_UpdateRuntimeAndScriptExecutionState` (0025DF00) calls `002E4A10`; `WorldActor_UpdateRuntimeAndScriptExecutionState` (0025DF00) calls `002E5750`.
- **Presentation — CLIENT and SERVICE (4 edges).** 1 inbound (Presentation bodies `003DD4C0` call page-cited `00267310`); 3 outbound (page-cited `WorldActor_UpdateRuntimeAndScriptExecutionState` (0025DF00) call Presentation bodies `003E68B0`, `003E6EF0`, `003E6A70`). Substantive edges include `WorldActor_UpdateRuntimeAndScriptExecutionState` (0025DF00) calls `003E68B0`; `WorldActor_UpdateRuntimeAndScriptExecutionState` (0025DF00) calls `003E6EF0`; `WorldActor_UpdateRuntimeAndScriptExecutionState` (0025DF00) calls `003E6A70`; `00267310` is called by `003DD4C0`.
- **Input — MECHANICAL (1 edge).** 1 inbound (Input bodies `002E09A0` call page-cited `00267310`) - shared-helper call surface, not a Input relationship of this page's subjects.
- **WorldAreaField — MECHANICAL (1 edge).** 1 inbound (WorldAreaField bodies `World_UpdateSimulationTick` (00314020) call page-cited `00267310`) - shared-helper call surface, not a WorldAreaField relationship of this page's subjects.
