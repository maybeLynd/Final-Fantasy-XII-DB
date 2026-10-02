---
system: Actor script requests from arming through start and return notification
category: 01-Script-VM-Native-Bridge
status: PARTIAL — OV-10 stays open (the remaining reachability observation is runtime, carried by FABLE-REQ-ASTRA-RT-REMAINDERS-0929; the authored bounds and recovery policy are answered at ov10-request-bounds-fable) (status line current 2026-10-02, SWE2-CONTRACT DD batch 21)
owner_layer: Actor request scheduling and ScriptVM execution
evidence_tier: 1
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: "SECTION-12 isolated original-instruction controls; synthetic actors, scripts and request lists"
last_reviewed: 2026-09-29
audit:
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-actor-request-falsification-pass-1
---

# Actor requests: arming, selection, start, return and resumption

**A submitted function request, a running entry, a wait-slot kind and a completion notification
are different states.** The original code can start a target without executing its bytecode,
complete a target without allocating its caller's notification, or complete a dependency and run
the caller's following instructions during the SAME driver invocation.

## Evidence scope

[Production review](../../_experiments/evidence/continuation-section12-actor-request-waits/REVIEW.md)
executes original `00268850`, entry initialization/allocation/insertion, scheduling/start,
`0025E4C0` request opcodes/RET, removal/notification helpers and `0025DF00` with original wait
predicates. There are139 bounded assertions and eight rejecting private-image variants, using
synthetic two-actor state. Zero application substitutions, zero import bridges, zero planted callbacks; no game process.
It is not exhaustive opcode coverage, caller reachability, OS scheduling or independent acceptance.

## 1. The request has two participants

`00268850(manager, issuer, valueStack, issuerRequest, pc, kind, mode)` pops function ID, target and
channel from the stack. The descriptor stores the issuer's manager/ordinal, selected request slot
and low32 continuation offset. The direct native fixture passes explicit values; bytecode fixtures
use original `REQSW`24 and `REQEW`27 handlers to create the descriptor.

The state1-vs-state2 insertion gate reads **issuer+02 and issuer+10** at002689F0/002689F7. It does
not read those fields from the resolved target. Different values in the two actors discriminate
that ownership. Immediate insertion reselects/promotes only when target != issuer. An early
reserved-bit rejection and a later capacity refusal also have different side effects: the latter
already stores the continuation and can decrement target+10.

## 2. Storage and scheduling

The original initializer003DB580 links a finite entry free list at actor+60, initializes detached
head+61 toFF and clears configured channel heads/tails and active bits. Entries are0x14 bytes;
wait slots are0x28. These are synthetic backed arrays, not a claim about real allocation reuse.

`003DBCF0` checks function count, requires a free entry and calls003DB7A0. Admission kind0 requires
an empty channel, kind2 can append despite an existing matching ID, and kind4 rejects a matching ID
already on that channel. A rejected insert returns its candidate to the free list.

003DB6E0 scans highest channel first, then its list from the head. State1 entries are skipped;
state2 is started and becomes3; existing started state resumes. A skipped high-channel state1
entry does not prevent a lower runnable channel from selection. High incoming channels are clamped
for entry placement, but the submitter's separate+26 bitset uses the unclamped channel. Authored
bounds are therefore a genuine precondition, not repaired by every downstream use.

003DBDC0 selects the actor wait slot, runs0025D460, and sets PC to actor bytecode base plus the
function-table offset. The reset covers+00..16 only. Scratch+18..27 and peer slots are not wiped.

## 3. Start-wait and end-wait use detached notifications

| Descriptor mode / entry+10 | Notification point |
|---|---|
| 1 | No start/end notification in these paths |
| 2 | At003DBDC0 selection/start, BEFORE target bytecode executes |
| 3 | At `003DB2A0` removal through `003DC0D0`: on RET, and also when a mode-4 `freqcancel` recycle (`003DB420`) removes the entry as its channel head |
| 4 | The notification itself, filed on the requester detached list |

OriginalREQSW arms kind4 then can resume its caller before the target's first bytecode instruction.
OriginalREQEW remains blocked until the target entry is removed and the removal posts the notification. RET is the
usual removal, but not the only one.

**A cancellation can attempt the end notification without RET** *(2026-10-02, FABLE, from ASTRA's
[`request-cancel-notification`](../../_experiments/evidence/request-cancel-notification/README.md) (`011e013c7`),
FABLE independent review ACCEPT-WITH-NARROWING,
[`fable-review-astra-request-cancel-notification-1002`](../../_index/candidates/fable-review-astra-request-cancel-notification-1002/REVIEW.md)).*

- **What the cancel verbs pass.** `freqcancel` (`00352980`) passes its popped channel and mode 4 to
  `ActorResource_RecycleEntryRange` (`003DB420`). The two-argument form (`00353660`) passes its first pop + 1 and
  resolves the second pop to another actor.
- **What the recycler selects.** Mode 4 clears the state filter. The recycler walks channels from
  `byte actor+0x88` - 1 down to max(0, signed bound), keeping only those set in its entry snapshot of
  `word actor+6`. For each such channel it hands the first entry with a nonzero `+0x11` to `003DB2A0`: at most one
  entry per channel per call.
- **When the notification is attempted.** The entry must be its channel's head, with mode `+0x10` = 3 and a
  requester ordinal other than `0x8000`. `003DB2A0` then unhooks it (clearing `+0x11`) and calls `003DC0D0`
  whatever the run state was. The interpreter is not called in front of that attempt.
- **A non-head entry is not removed.** The removal's search passes the removed index itself to its index leaf on
  every pass instead of walking the list, so a cancel does not remove an entry that sits behind a zero-state head.
- **What an end notification means.** It is evidence that the target entry was removed, not that the target's
  bytecode executed RET. Admission, delivery and consumption of the notification are separate stages (below).
- **The recycler's return value** is 1 on every normal path, including a NULL actor, an empty range and no
  selection, so it says nothing about removal or notification.
- **The NULL-actor hazard.** After a NULL actor both verbs still tail-jump to the request scheduler `003DB6E0`, which
  reads `[rcx + 0x63]` without testing rcx.
- **Premises:** valid, stable and disjoint actor and entry storage; normal ABI and returns. The removal past the
  attempt is opaque for entry flags 2 and above (a flags helper whose effects are not read; its address is on the binding-and-channels page).
- **Still open:** whether an authored scene cancels a mode-3 entry; natural interleaving; same-key re-entry; the
  scheduler's own effects.

The notification is not a separate guaranteed-delivery primitive. It allocates from the requester's
ordinary finite entry pool. Both notification producers ignore the allocation return. Controls
with caller capacity exhausted leave target progress intact and caller kind4 still waiting.
No shipped deadlock, automatic retry or higher recovery is inferred.

**The end notification is attempted before the finishing entry's own slot is free** *(2026-10-02, FABLE, from
ASTRA's [`notification-retirement-order`](../../_experiments/evidence/notification-retirement-order/README.md)
(`e46090c35`), FABLE independent review ACCEPT-WITH-NARROWING,
[`fable-review-astra-notification-retirement-order-1002`](../../_index/candidates/fable-review-astra-notification-retirement-order-1002/REVIEW.md)).*
In a head-entry removal, `003DB2A0` first calls the unhook `003DC1B0`, which relinks the neighbours, clears entry
`+0x11` and writes nothing on the actor. Next comes the mode-3 attempt through `003DC0D0`. Only after that does
the removal relink the index onto the free list and publish it as the free head `+0x60`; every path from the
attempt's return passes both steps.

The attempt is made only when the entry is the list head, its mode `+0x10` is 3, its signed channel byte `+0x02` is
not negative, its requester word `+0x06` is not `0x8000`, and the requester resolves to a non-null actor.

- **Two refusals come first.** The posted descriptor selects function 0. `003DBCF0` checks that id against the
  requester's function count before anything else, as an unsigned compare: a zero count returns 3. Only then does
  it test the requester's free head: `0xFF` returns 2. Neither refusal calls anything or writes outside its own
  stack.
- **So a self-requested notification on a full pool is lost.** When the requester is the removing actor itself and
  its free list is already empty, the notification is refused with 2 before the retiring slot becomes
  allocatable. Conditions: a valid head mode-3 entry; a positive function count; entry flags `+0x12` 0 or 1 (2
  and above also cross a flags helper whose effects are not established); stable, disjoint actor, pool and frame
  storage; normal returns under the ABI; no concurrent writer. This is a conditional reading of the original code,
  not an observed full pool. "Same actor" is a premise on the resolved requester pointer; the code compares nothing.
- **The removal's return is not a delivery result.** It is bit 0 of the entry's `+0x12`, read before the attempt;
  the attempt's own result is overwritten unread. With flags 1 the removal returns 1 even when the notification was
  refused. Index `0xFF` returns a constant 1 without reading an entry.
- **An observer has to read the attempt itself:** the requester, its free head and the call origin at
  `003DBCF0` + 0x36 with return origin `003DC0D0` + 0x57. Spare capacity seen after the removal does not show that
  capacity existed when the notification was allocated.
- **Still open:** whether shipped play reaches a full self-pool; actor lifetime and reuse; concurrent mutation;
  cancel and re-entry scheduling; the insertion helpers' success and effects on a non-`0xFF` free head.

## 4. Notification identity

003DC050 scans the caller's detached list for **channel + low32(savedPC - bytecodeBase)**. Wrong
channel or wrong offset does not resume. A matching entry is removed in0025DF00, which sets kind1
and retries. Neither a generation token nor unique allocation identity is part of that tested key.
Reuse, duplicate delivery and absent actor lifetime protections cannot be inferred from equality.

## 5. Wait-kind semantics

| Kind | Input / predicate | Resume condition |
|---|---|---|
| 0 / >=8 | No runnable dispatch arm | No interpreter in the tested visit |
| 1 / 2 | Original interpreter | Opcode/command semantics |
| 3 | encoded target+18, entry ID+20 | Matching target entry is absent |
| 4 | caller channel and continuation PC | Matching detached notification is present and removed |
| 5 | encoded list+1C, cursor+22 | Actor/ID list cursor reaches end |
| 6 | encoded target+18, channel+26 | Selected channel bit is clear |
| 7 | encoded list+1C, cursor+22, channel+26 | Actor/channel list cursor reaches end |

0025E127 is the blocked/no-interpreter exit.0025E0BE is the interpreter arm. Completion writes
kind1 and returns to the dispatch head; following bytecode can execute immediately under the same
configured service gates. No mandatory extra frame is introduced by notification consumption.

Kinds3/6/7 set+27 to1 on completion. Kinds4/5 do not. The serviced marker+16 has a conditional
skip/clear gate; it is not a universal elapsed-frame counter.

## 6. Ordered list waits are not simultaneous barriers

Original00267420 and002674B0 read a DWORD count and four-byte list elements. A WORD cursor at
request+22 advances past satisfied elements and stops at the first active one. Later calls begin
at that cursor. A previously passed actor can reactivate without being checked again. The channel
variant ignores the second WORD of each element; the resource variant matches it as an entry ID.

A null resolved list completes in the selected helper; invalid actor indices and malformed list
memory are outside the demonstrated preconditions. This is not a blanket memory-safety claim.

## 7. Remaining obligations

- [x] ~~Original producers and ownership of all list-wait payloads, including resource replacement.~~ **Producers and
  ownership answered 2026-09-26 (FABLE, Claude Opus 5.5); resource replacement split out below.**
  - **Three opcodes produce every list wait, and nothing else does.** `0x5F REQALL` and `0x63 REQIALL` arm kind 7
    through one shared store, `mov word [slot+0x14], 0x107` at `00261B97`. `0x61 REQWAITALL` arms kind 5 at
    `00261D24`. Each first writes the encoded list to `+0x1C` and zeroes the cursor `+0x22`, then tests the list at once.
    It parks only if a listed entry is still active; otherwise execution continues.
  - **The census.** An image-wide scan looked for a store of any width to `[reg+0x14]` whose low byte is 5 or 7,
    preceded within 40 instructions by a store to the same base's `+0x1C`. It finds exactly those two immediate
    stores. The 71 register-sourced stores it also lists are dword, qword or float stores on other structures, and
    none lies in the ScriptVM band (`0025xxxx`-`0026xxxx`) or the wait services (`003DBxxx`). Its control is that
    both known stores are listed: `25-EBP-Script-Container/Bytecode-And-Opcodes/members/listwait_producers.py`.
  - **Ownership.** The list is authored data in the bound definition payload (manager slot `+0x000`). It is reached
    through the table offset at payload `+0x30` and indexed by the opcode's 16-bit operand. The wait keeps a 32-bit
    image-address encoding of the list, so it borrows the payload and is valid only while that payload stays bound and
    unmoved. [The bytecode page](../../25-EBP-Script-Container/Bytecode-And-Opcodes/section-000-bytecode.md), in its
    `REQALL` / `REQIALL` / `REQWAITALL` section (2026-09-24), carries the list format and the shipped-script census:
    no out-of-range index, and empty lists authored as no-ops.
- [x] What happens to a parked list wait when its actor's definition payload is rebound or replaced: whether any path
  clears or re-bases slot `+0x1C` before the next poll dereferences it.
  *Narrowed 2026-09-26 (FABLE, Claude Opus 5.5): on the load path the wait is disarmed; only a rebind of a LIVE slot
  is open.* Functions are named by role here; the addresses are in the actor-manager and actor-storage pages.
  - **The bind itself does not touch the waits.** The payload-loaded callback's bind writes the payload to manager slot
    `+0x00` and clears only slot `+0x244`-`+0x283`. The wait slots are on the actor records, not the manager slot.
  - **The records are rebuilt after the bind, conditionally.** The same callback then finalises the manager runtime,
    which allocates and initialises the actor records only when the slot's live bit `+0x10` bit 0 is clear and
    `+0x13` is non-zero.
  - **Initialisation disarms every wait.** The record initialiser walks the record's wait slots (count byte `+0x88`,
    array `[record+0xA8]`, stride `0x28`) and zeroes `+0x00`-`+0x16` of each, the kind byte `+0x14` included. The
    list pointer `+0x1C` and cursor `+0x22` are left as they were. A kind-0 slot never polls them, and every list-wait
    arm rewrites `+0x1C` before arming, so the stale value is never dereferenced.
  - *Open:* a bind on a slot whose live bit is SET keeps the old records, and with them any parked wait's pointer into
    the old payload. Whether any caller binds a live slot is not established.
  - **Answered the same day (FABLE, Claude Opus 5.5): no route binds a slot that still holds its old records.**
    - **Two routes, one entry.** The bind has two entries: the ATEL sibling loader's callback and the primary-payload
      handler. Both are reached only from the manager's resource-set load (raw call and `lea` census over `.text`).
    - **That load unloads first, unconditionally.** It calls the slot unload before it starts the new load.
    - **Every path through the unload ends in the same tail.** The tail releases the old record block, stores 0 to
      slot `+0x08`, clears live bit `+0x10` bit 0 and zeroes `+0x13`. This includes the early branch taken when the slot
      is not live.
    - **So a parked list wait never outlives its payload.** It sits on a record that is released and detached before any
      new payload is bound, and the field pass reaches records only through slot `+0x08`. Addresses are on the
      actor-manager pages; this page names the functions by role.
- [ ] **OV-10.** Real authored input bounds and higher recovery/delivery policy for exhausted notification capacity.
  - *Qualified 2026-10-02 (FABLE, review of ASTRA `notification-retirement-order`):* the end notification is
    attempted before the removed slot is relinked and published, so the capacity that matters is the requester's
    free head at the attempt (section 3). A runtime observation for the residue counts only when it is taken at the
    attempt, with the requester and the call origin; capacity seen after the removal does not count.
- [x] ~~**OV-11.** Outer-frame ordering, reentrancy, live actor allocation/reuse, and remaining native wait services.~~ *ANSWERED 2026-09-29 (FABLE, Claude Opus 5.5): the native wait services are a closed set - `0025DF00`'s bounded eight-entry kind table, one predicate per service arm; actor reuse is this section's own 2026-09-26 answer; in-frame order is the field-pass page sections 4-5; reentrancy stays superseded under OV-2; [`ov11-wait-services-fable/`](../../_index/candidates/ov11-wait-services-fable/README.md). Register OV-11.*
- [x] ~~Required independent review and claim-level incorporation into the major-system L2 assessment.~~ *NOT A QUESTION 2026-09-29 (SWE2-FRONTIER) under the class-2 ruling: an independent-acceptance/process item, carried by board task FABLE-CARRIER-SECTION-OVERLAY-ACCEPTANCE-0929. Register OV-12.*

[Binding and channels](how-a-script-binds-to-an-actor-and-how-requests-are-scheduled.md),
[interpreter contract](../CONTRACT-interpreter-core.md),
[field driver](../../04-Actor-Entity/the-field-runtime-pass.md),
and [earlier command resumption](the-script-from-bytecode-through-wait-and-resume.md)
remain separate, connected parts of the specification.

## Falsification pass 1 — 2026-09-29 (OPUS): every structural clause survives; the notification walk has a cap

**Attack.** §1-§7's structural clauses became checks that fail if the shipping image says otherwise. Script:
`Tools/analysis-kit/gfz-scripts/falsify_actor_request.py`, output `falsify_actor_request.out`, image `73461d08…`, 0 BROKEN.
The behavioural results are SECTION-12's executed controls and are not re-run.

| # | Clause attacked | Result |
|---|---|---|
| A0 | §1 the gate reads the ISSUER's +02 and +10 | **survives**: `r15` is `rdx`, the issuer argument (`00268883`). `002689F0`/`002689F7` test its `+02 == 1` and `+10 == 0`, not the target in `rbx`, and a pass inserts the target through `003DB790` |
| A1 | §2 start selection | **survives**: the slot is `[actor+0xA8] + ~~byte[entry+0x11]~~ sx(byte[actor+0x11])·0x28` *(corrected 2026-10-02, OPUS: `003DBDD4 movsx rax, byte ptr [rcx + 0x11]` with `rcx` the actor (`003DBDE7 mov rax, [rcx + 0xa8]`); the entry is `rsi`, whose `+0x11` is the run state written 3 at `003DBE68`)*; `0025D460` resets it; PC = `[actor+0x58]` + `00358A00`'s offset |
| A2 | §2 "the reset covers +00..16 only" | **survives**: `0025D460` stores a qword, a qword, a dword, a word and a byte (`+0x00`..`+0x16`) and nothing else |
| A3 | §4 the notification key | **survives, made exact**: `003DC050` walks the detached list from byte `[actor+0x61]` over `0x14`-byte entries at `[actor+0xA0]`, and matches dword `[entry+0xC]` and sbyte `[entry+2]`. No generation token is involved. The walk is **also bounded by byte `[actor+0x89]`**, which §4 did not state. Its counter is compared before it is incremented, so at most `byte[actor+0x89] + 2` entries are examined before it reports "not found" (`0xFF`) |
| A4 | §7 the list-wait producers | **survives**: kind 7 through `mov word ptr [rsi+0x14], 0x107` at `00261B97`; kind 5 at `00261D24` after `002674B0` |
| A5 | §6 the two list helpers | **survives**: `00267420` (132 B), `002674B0` (166 B) |

No correction, so no consumer record.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (SWE2-CONTRACT)

- **Movement — CLIENT and SERVICE (9 edges).** 4 inbound (Movement bodies `WorldActor_UpdateRuntimeAndScriptExecutionState` (0025DF00) call page-cited `WorldActorScriptVM_InterpretBytecode` (0025E4C0), `ScriptVM_WaitList_HasAnyActorChannelActive` (00267420), `ScriptVM_WaitList_HasAnyActorResourceEntryActive` (002674B0)); 5 outbound (page-cited `WorldActor_UpdateRuntimeAndScriptExecutionState` (0025DF00) call Movement bodies `002E6310`, `Movement_UpdateActorFrame` (002E5030), `002E4A10`). Substantive edges include `WorldActor_UpdateRuntimeAndScriptExecutionState` (0025DF00) calls `002E6310`; `WorldActor_UpdateRuntimeAndScriptExecutionState` (0025DF00) calls `Movement_UpdateActorFrame` (002E5030); `WorldActor_UpdateRuntimeAndScriptExecutionState` (0025DF00) calls `002E4A10`; `WorldActor_UpdateRuntimeAndScriptExecutionState` (0025DF00) calls `002E5750`.
- **Presentation — SERVICE (3 edges).** 3 outbound (page-cited `WorldActor_UpdateRuntimeAndScriptExecutionState` (0025DF00) call Presentation bodies `003E68B0`, `003E6EF0`, `003E6A70`). Substantive edges include `WorldActor_UpdateRuntimeAndScriptExecutionState` (0025DF00) calls `003E68B0`; `WorldActor_UpdateRuntimeAndScriptExecutionState` (0025DF00) calls `003E6EF0`; `WorldActor_UpdateRuntimeAndScriptExecutionState` (0025DF00) calls `003E6A70`.
