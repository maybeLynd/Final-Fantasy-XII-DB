---
contract: "Queue resource reads in a 64-slot pool; service and recycle requests while preserving request identity and callback semantics"
category: 02-Resource-And-Asset-Pipeline
scope: subsystem
level: L2
readiness: BEHAVIORALLY UNDERSTOOD
confidence: PROVEN
implements: 02-Resource-And-Asset-Pipeline/the-resource-request-queue.md
entries: ["0032E450", "0032E620", "0032E780", "0032E870", "0032E990", "0032EC40", "0032E070", "0032E040", "0032E520", "0032E590"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: "SECTION-02: selected original bodies re-read; bounded original CPU-instruction controls plus unchanged EXP-146 retained-assertion replay. No live FF12 session or full producer campaign rerun."
last_reviewed: 2026-09-30
historical_audit:
  by: OPUS
  date: 2026-09-20
  scope: "The preceding contract, not independent acceptance of these edits."
production_review:
  by: external-continuation
  section: SECTION-02
  status: "PRODUCTION COMPLETE; formal peer acceptance pending"
  evidence: _experiments/evidence/continuation-section02-resource-queue/REVIEW.md
external_production:
  section: SECTION-09
  date: 2026-09-23
  status: "locally validated; formal independent acceptance pending"
  evidence: _experiments/evidence/continuation-section09-owner-producer/REVIEW.md
audit:
  passes: 1
  last_pass: 2026-09-30
  last_pass_kind: falsification
  last_pass_state: opus-request-queue-falsification-pass-1
---

# Contract — the resource request queue

**Current bounded contract.** [SECTION-02](../_experiments/evidence/continuation-section02-resource-queue/REVIEW.md)
is original-byte re-derivation plus **72 original-instruction checks**, a repeat, six relevant
code-mutant rejections, and retained-record review. [EXP-121](../_experiments/EXP-121-exp109-queue-tails-exec.md),
[EXP-128](../_experiments/EXP-128-exp109-poll-pump-exec.md) and
[EXP-146](../_experiments/EXP-146-queue-remaining-exec.md) retain their historical execution scope.
The [mechanism page](the-resource-request-queue.md) supplies broader caller and read-layer research.
None of these labels means current live-game validation, independent T2 acceptance of this edit,
or whole-system L2 completion. Source omissions and scripted boundaries remain explicit.

## 1. Purpose

Manage the documented resource callers' pending reads in an image-resident pool of **64 slots**.
A requester acquires a free slot and returns a generation-tagged id. The pump services the pending
**head**, possibly advances several states and retires several requests in one invocation, and
runs common post-pass services before returning. A full pool makes the requester pump and pace
synchronously until a slot is available. The queue is not guaranteed to defer work until another frame.

## 2. Interface

| Entry | Contract at the original boundary |
|---|---|
| `0032E450()` | Initialize the 64-slot linkage, selected fields and queue heads; reset the request counter to 1. Not a full-byte clear. |
| `0032E620(kind, index32, dest64, bytes32, descriptor64)` | Reject a negative signed index after telemetry stores; otherwise request at the tail. `003EB0D0()!=0` enables chunk fixups. Return is a 32-bit id, or `0xFFFFFFFF` for that rejection. |
| `0032E780(kind, index32, dest64, bytes32, descriptor64)` | Negative-index guard, then request at the **head** without the chunking gate. |
| `0032E870(kind, index32, dest64, bytes32, descriptor64, atTail32)` | Stall if free head is null; take, initialize selected request fields, return its id. Fifth/sixth parameters are at entry `rsp+0x28/+0x30`. |
| `0032E990(atTail32)` | Takes its flag in **ECX**, loads the slot from the global free head, returns its pointer. It does not accept a caller-supplied slot in RCX. |
| `0032EC40(slot64)` | Unlink that slot from pending, push it onto free, mark its id `-1`. Does not clear its payload or state. |
| `0032E070()` | Head-driven pump; may complete multiple transitions/requests in one call. |
| `0032E040()` | Short-circuit loader predicates; invoke the pump when either is nonzero. This wrapper itself supplies no once-per-frame guarantee. |
| `0032E520(nonzero)` / `(0)` | Nonzero queries outstanding work without pumping; zero pumps and paces until idle. |
| `0032E590(id32)` | Reject sentinel/stale ids; cancel immediately or mark in-flight work state 4. Return register is not a success API. |

## 3. Types

`ResourceRequestSlot`: `0x80` bytes, 64 instances at `022C31C0`.

| Offset | Bounded meaning |
|---|---|
| `+0x00`, `+0x08` | Absolute-counter accumulator and latest stamp. State 2 adds the **second** getter result and stores that same result as the stamp. **The accumulator is written, never read in this build** (SWE2-CONTRACT `b6_request_queue.py` Z1, M1-M2, Z3): `0032E153` adds to it and `0032E229` / `0032E725` / `0032E97C` store 0; its purpose is not a static question. |
| `+0x10`, `+0x18` | Next and previous slot pointers, for both free and pending lists. |
| `+0x20`, `+0x21` | State and kind bytes; kind `0xFF` changes the meaning of the stored 32-bit index. |
| `+0x22`, `+0x23` | Distinct chunk-enable and progress-result bytes. Some initialization writes both at once. |
| `+0x24` | 32-bit index storage; the path route sign-extends these bits into a pointer. Not a general 64-bit pointer field. |
| `+0x28`, `+0x2C` | Part byte count and file offset. Signed tests are significant, including `bytes == -1` and offset truncation. |
| `+0x30`, `+0x34` | Part cap and remaining count; the relevant minimum/termination comparisons are signed 32-bit. |
| `+0x38`, `+0x70` | Advancing destination and original destination. |
| `+0x40`, `+0x48` | Completion/error and cancellation callback pointers copied from descriptor `+0x10/+0x18`. |
| `+0x50` | Part callback slot. **The requester clears it; it does not copy descriptor `+0x20`.** **Nonnull part callbacks: none in the shipped build** (SWE2-CONTRACT `b6_request_queue.py` Z2): the slot is stored only as 0 (`0032E6FF`, `r14` = 0 from `0032E670`; `0032E959`) and read only at `0032E3B4`, so `0032E3B0` returns 1 and part results 2 / 3 occur only under seeded controls. |
| `+0x58`, `+0x5C`, `+0x60`, `+0x64` | Slot index; requester-zeroed dword; callback argument word; request id. |
| `+0x68..+0x6F`, `+0x78..+0x7F` | Unobserved in the cited slot census; do not invent semantics. |

The builder copies a `0x28`-byte descriptor on its gated branch, but the requester consumes only
`+0` offset, `+8` argument, and `+0x10/+0x18` callbacks. A copied descriptor byte is not necessarily
a semantically consumed value. The gated builder writes its local `+4=0x80000` and `+0x20=0`, then
sets the slot cap directly after requesting. The input descriptor remains unchanged in the controls.

## 4. Preconditions · postconditions · invariants

**I1 — constructor cursor is not the slot base.** `0032E450` iterates with RAX at `slot+0x18`.
It initializes links, `+0x58=index`, `+0x64=-1`, word `+0x20=0`, and dword `+0x28=0`.
All other slot bytes survive a dirty-pool reinitialization in the seeded control. Constructor
reset of the generation counter also means ids are not globally unique across initialization.

**I2 — list ownership is explicit.** In a valid initialized pool, each slot is on exactly one
of the free or pending lists. `022C51D0` is a **mutable free-list head**, not a constant array base:
`0032E9B5` advances it to the old head's next; `0032ECBE` pushes a recycled slot. Tail/head inserts
and middle/head/last removals are checked with a full 64-slot disjoint-list control.

**I3 — no slot means a blocking retry, not an error return.** `0032E870` executes
pump -> in-flight getter -> pacer before testing free head again. A 65th requester can free
all 64 zero-byte requests itself and return in the same invocation. Progress is not guaranteed
if external completion never arrives. **Proviso (script BGM stream):** the same-call drain holds while the stream `02B5E0E0` is inactive (every shipped run) or waiting in state 5, but not while the stream machine `003EADE0` is in a submitting state (1, or 7 with bytes left) with the pool full: it submits through `0032E780` -> `0032E870` before writing its next state (`003EAE4C` before `003EAE63`, `003EAF9A` before `003EAFAD`), so the nested requester re-enters the pump, which calls the machine again, and nothing drains (SWE2-ORACLE 2026-09-30, NATIVE-REPLAY to depth 8, `_index/candidates/s08-bgm-machine-drain-0930/`; the order is static, OPUS-verified; exhaustion inferred; review pending). No shipped script feeds the stream, so this is a modded-script domain, like I5's gate. The unguarded `0032E990` alone faults at `0x10` on a null
free head for either flag. That is a precondition violation, not the requester behavior.

**I4 — ids distinguish successive uses, within the accepted counter domain.**
`id = (counter << 6) + (slotIndex & 0x3F)` in 32-bit arithmetic. For constructor-derived counter
values `1..0xFFFFFF`, the increment resets to 1 when it exceeds `0xFFFFFF`. The actual compare
is signed (`cmovg`), not an unconditional clamp of arbitrary corrupted input. A planted counter
zero produces id zero for slot zero **after enqueueing it**; the gated builder skips its fixups,
not the acquisition. This control is not a claim that normal initialization yields zero.

**I5 — chunking is gate-dependent, not size-only.** `003EB0D0` reads the stream descriptor's flag.
Clear gate leaves a large request whole and leaves unused cap/remaining storage untouched.
Set gate copies/zeros a local descriptor and, for nonzero id, sets chunk-enable 1, cap `0x80000`,
remaining to the prior byte count, and the signed-minimum first part. This section executes both
branches. Which shipped states reach that gate is separate from the branch contract; do not
exclude the branch merely because a historical producer census called it dormant.

**I6 — file offset truncates toward zero to a `0x800` multiple.** The instruction sequence is
`cdq; and edx,0x7ff; add eax,edx; and eax,0xfffff800`. For positive values that is downward;
for negative values it is toward zero. No extra `subtract` instruction exists. The same operation
is used initially and on requeue. Signed count comparisons must not be rewritten as unsigned.

**I7 — recycling does not sanitize.** The splice writes links and `requestId=-1`; callers clear
state on the applicable paths. Kind, index, callback pointers, destinations, caps, stamps and
unobserved bytes can remain. Reuse relies on the fields initialized for the next request, not a
whole-slot memset. Stable retained bytes are not evidence of an active request.

## 5. State

| Address | Role |
|---|---|
| `022C31C0` | Fixed start of the 64-slot pool; distinct from the changing free head. |
| `022C51C0`, `022C51C8`, `022C51D0` | Pending head, pending tail, free head. |
| `01EED498` | Generation counter, initialized to 1. |
| `022C51D8`, `022C51DC` | Last attempted kind/index telemetry, including rejected negative-index attempts. |
| `0215EFF4` | Underlying read status; the original getter reports in-flight for `-1`. |
| `022CA5E0` | Original counter getter's source. |
| `022C51F0` | Per-kind override-pointer array; its declared initialization/producer census belongs to the mechanism page. Not newly re-censused here. |

## 6. Relationships

The page traces initialization from `0032EA90`, the main-loop callers, and file-size lookup
`0032E400`. This section independently checks the queue's original transitions and list mechanics,
not every caller or underlying read implementation. The per-frame wrapper, explicit drain, and
full-pool retry are **three different pump contexts**. A head-inserting wrapper `0032E780`
is retained and tested; the semantics of its higher-level priority callers remain separately scoped.

**Restored by the owner (OPUS, 2026-09-25)** — three HEAD facts the rewrite dropped, each re-read:

* **Initialisation resets the read layer.** `0032EA90` builds the pool (`0032EA94 call 0032E450`) and then
  calls `003EB050` (`0032EA99`). **[page, OPUS re-read]**
* **The mode bodies use the ASKING form.** `0032E520(1)` — query outstanding work without pumping — is
  what `0022B6E0` and `0022B7E0` call (`0022B737`/`0022B837 mov ecx, 1`), as do
  `WorldTransition_StageFieldTransition` (`00314609`) and `0050E1E0` (`0050E1E4`); the draining form
  `0032E520(0)` has its own callers (e.g. `00314621`, `003EA24E`). That the `0022B6E0`/`0022B7E0` bodies
  are the boot modes is the page's reading. `00379E30` is a different thing: it loops
  "while `00379E60(mode)` holds: `0032E040`, then `0035EA30(0)`" (`00379E38`–`00379E56`), i.e. it
  drives the per-frame pump, not `0032E520`. **[page, OPUS re-read]**
* **The staged-selection push `0036C1F0`** ran inside EXP-121's executed machinery; its only entry is
  a tail jump from `0036C1D0` (`0036C1DF`). **[EXP-121, OPUS re-read]**

## 7. State transitions

The pump repeatedly re-reads **pending head**. It does not advance a cursor to the next slot when
the head is busy. These rows describe original caller control flow; external read behavior is separate.

| State | Transition / stopping condition |
|---|---|
| Empty pending list | Call `003EADD0`, then the common service footer. |
| 1 queued | Busy service gate returns to footer. Zero bytes completes and recycles without file issue. Otherwise issue by kind. Kind-FF nonzero submit result revisits the same head; accepted issue stamps time and sets state 2. **Every other kind is taken as issued:** the wrapper `0046E030` returns 1 whatever the read issuer `002DF780` returned (`0046E043`). So a refused read (a −1 file-size entry, `002DF7B9`) also moves to state 2, and in state 3 it completes on the status slot `0215EFF4` the previous read left (OPUS 2026-09-30, RC-37, `_index/candidates/rc37-refused-read-0930/`, static; ~~pending SWE2-AUDIT-SPEC review~~ reviewed ACCEPT by SWE2-AUDIT-SPEC 2026-09-30, [`auditspec-review-rc37-0930`](../_index/candidates/auditspec-review-rc37-0930/REVIEW.md)). |
| 2 issued | Discard first getter result; add second absolute reading to accumulator; store the same value at `+8`; set state 3 and revisit head. |
| 3 waiting | In-flight status returns to footer and blocks later pending work. Otherwise set state 5 or 6 from status sign and enter completion handling. |
| 4 cancelling | Wait for in-flight status to clear; when cancel callback exists, zero byte count and call it. Set state 0, recycle, and revisit head. With no callback this path does not zero byte count. |
| 5/6, chunk byte 0 | Delivered calls done helper; failed calls gated error helper. Clear state, recycle, revisit head. |
| 5/6, chunk byte 1 | Progress byte 2 re-probes the part callback first. Otherwise state 6 errors/recycles; state 5 subtracts the prior part using signed remaining-count termination. If more remains, advance offset/destination and ask part callback. |
| Other chunk byte, invalid state, or callback not continuing | Return to common footer without a general release guarantee. |

Part callback return 1 requeues with a new signed-minimum count, aligned offset, accumulator 0,
state 1 and progress 0. Return 2 preserves progress 2 and allows re-probing next invocation.
Return 3 is **not an alias for return 2 and not a terminal release operation**: it leaves state 5
and progress 3; the next pass can repeat subtraction using the previous part. A planted callback
control demonstrates this, without claiming a valid shipped producer reaches it. Null part callback
returns 1. Other values invoke the diagnostic boundary and are returned by the helper.

The footer calls `0046DD50`, `003E9780`, `0036FD50` and conditionally `003BB790`, with empty
`0016D6A0` calls interleaved. It runs for empty, busy and drained cases: **calling it “teardown”
does not establish shutdown or destruction**. The page describes surrounding service roles.

## 8. Script · resource · event interactions

Keep size query, attempted request, accepted record, issued read, completion callback and final
consumer use distinct. A zero-byte request can callback successfully without issuing a file read.
Kind `0xFF` uses a stored 32-bit path value sign-extended at the issue/free sites; observation tools
must not reinterpret it as an ordinary resource-kind/index pair or an arbitrary 64-bit pointer.
The stream gate affects splitting; this section does not establish every authored stream state.

## 9. Determinism

Given valid list/slot state, generation counter, callback results and scripted external responses,
the checked queue transitions are reproducible. Completion timing, reachable ordering, thread
interaction, and I/O progress require the corresponding real environment. Do not require an extra
frame per state: one pump can traverse states 1->2->3->5 and retire several requests. The two
counter reads have no getter-side delta; that alone does not prove no external writer can run
between them in a live process. The second reading is the one consumed.

## 10. Failure paths and edge conditions

Negative builder index returns 32-bit `0xFFFFFFFF` after telemetry writes. Full pool retries;
it is not a guaranteed bounded wait. Zero/nonzero id and valid generation are distinct issues.
Cancellation rejects ids 0/-1 and stale generations before acting. States 2/3 become state 4;
other cancellable states use the immediate cancel helper. Cancel clears the done callback first.
For kind FF, cancellation has its own path-free step before state selection; this section does
not infer universal path ownership safety or repeated-cancel idempotence.

Error helper `0032E370` calls the done callback with success 0 only when the callback is nonnull
and byte count equals -1. With callback gated out and non-FF kind, the return can still contain
that callback pointer. It is not a boolean result. Completion helper passes success 1 and original
destination; callback argument is the descriptor's 32-bit word, not a buffer pointer.

## 11. Observable behaviour

A saturated queue can stall a requester while it pumps; the duration depends on external work.
No live loading hitch, frame duration, or complete file-delivery observation was performed in this
section. The observations here are exact synthetic-state instruction effects and retained evidence.

## 12. Reproduction formula

Use the exact list direction, mutable heads, selective constructor/recycle stores and generation
check. Model the pump as a loop over the head, not one transition per frame. Preserve callback
guards, signed alignment/count arithmetic and no-callback differences. Do not copy descriptor
`+0x20` into the slot merely because the descriptor has that storage. Keep real read-layer and
callback contracts explicit rather than treating script stubs as implemented I/O.

## 13. Runtime validation

Historical producer receipts: EXP-121 reports 27 functional/22 mutation cases; EXP-128 reports
137/123; EXP-146 reports 22 functional cases and repeats. Some packages inherit earlier cases;
these counts are not additive unique coverage. Their exact scripted boundaries remain in their
original programs and receipts.

SECTION-02 independently rechecks **22 original-body hashes**, runs **72 original CPU-instruction
checks** and an identical repeat, rejects **six changed-code controls**, and replays EXP-146's
**22 recorded assertion branches** with four corrupted-record controls. The two `e040-loader`
branches in that historical checker have no positive assertion; new native gate checks cover them.
No producer program, original output JSON, installed game, global L2 verdict or historical receipt
is overwritten. All external service/pacer/loader/free/diagnostic bridges are named in the source.

**Invariant verdicts — the owner's (OPUS, 2026-09-25)**, against EXP-121/128/146
(`_index/candidates/queue-i1-i7-owner-verdicts.md`): **confirmed by replay** — I2 (both gate polarities;
the gate `003EB0D0` tests `BgmStream +0x31` over records of stride 0x38), I3 (three real stall passes),
the I4 encoding (`id & 0x3F` = slot, `id = 0` failure), the I5 link mechanism; ~~**stand as static** — I1
(field list), I4's wrap at `0xFFFFFF`, I6 (truncation toward zero, `0032E721`–`0032E730`), I7.~~ **executed since —
re-adjudicated 2026-09-25 (OPUS, owner, `REQ-OPUS-QUEUE-CONTRACT-S13-READJUDICATE`):** the four that stood as static are
executed by block 330 (`_index/candidates/s08-opus-replay-queue-static-invariants/`, no application stub, 4/4, identical
×3) — I1 (over `0xAA` / `0x55` pools `0032E450` changes only `+0x10..+0x21`, `+0x28..+0x2B`, `+0x58..+0x5B`,
`+0x64..+0x67`), I4's wrap (counter `0xFFFFFF` → id `3FFFFFC0`, reset to 1; `0x80000005` → id `0x143`: the signed
`cmovg`), I6 (eight offsets incl. `−0x801` → `−0x800` and `−0x80000000` unchanged) and I7 (`0032EC40` changes only the
two links and the id). **All seven invariants are now executed**; none changes wording. EXP-146 adds:
`0032E990` has no empty-free-list guard (a null head faults), so `0032E870`'s stall is the only
protection; and the pump drains to teardown, not idle.

## 14. Unresolved

* Real read-layer, file/archive, service-footer and callback side effects beyond the checked boundary.
* Live progress, scheduling, synchronization, cancellation/path lifetime and higher-level priority policy.
* Authored/reachable producer state for the chunk gate~~, nonnull part callbacks~~ and invalid input values. *(Nonnull part callbacks answered 2026-10-01: none in the shipped build, `+0x50` row.)*
* ~~Meaning of the absolute-counter accumulator and the still-unobserved slot bytes.~~ *(Answered 2026-10-01: the accumulator is written and never read, `+0x00` row; the 16 bytes `022C51E0`..`022C51EF` after the list record are one qword stored 0 by `0032EAA7` and `0032EAE0` and never read (SWE2-CONTRACT `b6_request_queue.py` Z3).)*
* Formal peer review of SECTION-02 and resolution of the broader L2 system obligations.

These are not answered by correct hashes, a complete layout, passing fixtures or a linked contract.

## 15. Evidence

[SECTION-02 review](../_experiments/evidence/continuation-section02-resource-queue/REVIEW.md)
links the original range manifest, disassembly, original-instruction source/results, mutations,
retained-record checks and limitations. The [mechanism page](the-resource-request-queue.md)
retains broader historical research. EXP-121/128/146 are linked above at their bounded methods.
The previous contract's initial-value/array-base confusion, whole-slot clear, callback transfer,
one-step timing and shutdown language are superseded by this current contract, not silently
reinterpreted as successful historic tests.

## 16. Parity plan

Compare dirty-pool initialization and graph invariants; head/tail insertion and all splice positions;
slot reuse and generation fencing; max-domain wrap and explicitly invalid counter fixtures; signed
offset/count behavior; the gate's whole/chunked branches; real callback arguments/absence guards;
zero-byte completion, head-of-line waiting, same-call draining and the full-pool retry; staged and
immediate cancellation; part-result distinctions; and common-footer execution. Use separate
installed-game tests for timing, I/O, concurrency and actual callbacks when those claims require it.
L3 reconstruction parity remains later work, not an extra prerequisite for this database section.


## A concrete source-owner client — SECTION-08 (2026-09-23)

`003DDA70` submits `IndexedExternalSourceRequest` from the static table02B581A0, not the
ResourceRequestSlot itself. It resolves owner.handle and passes signed16 owner.kind/index,
owner.requestedBytes and owner.fileOffset. The descriptor holds completion003DD850, no cancel
callback, and the LOW32 OWNER ADDRESS as callback argument. The owner discards the requester's
return and writes state3 even in the controlled rejected-negative-index case.

Deleting an owner in state3 does NOT cancel/unlink the pending queue record. It sets owner.state5
and leaves the source pinned and callback intact. Original0032E330 completion dispatch invokes
003DD850; that consumer first unpins, then disposes/frees on state5 and clears state only. The
helper's successful callback invocation is not itself queue recycling: slot retirement belongs to
its caller. The fixture explicitly resets the synthetic queue after inspecting this boundary.

Original0032E370's error path calls completion only for requested length-1. The tested positive
length0x180 therefore leaves this owner's state/source untouched. This does not prove how every
service error is recovered or that the owner leaks in gameplay. The full queue pump, OS IO and
producer failure/retry schedule are not run by SECTION-08. Existing generic queue rules from
SECTION-02 remain; no client state is substituted for a queue state.

[Connected owner/view contract](the-external-source-owner-and-borrowed-view-lifetime.md) and
[116 bounded assertions, original inputs, limitations](../_experiments/evidence/continuation-section08-external-source-owners/REVIEW.md).
Formal independent acceptance and source-side callback lifetime/reentrancy remain separate.


## Original owner producer and terminal pump — SECTION-09 (2026-09-23)

The original `003DD4C0` producer now supplies this client in the fixture: arming requires owner
state0; a pending bit and state2 together initiate selection/allocation. File kind/index are
mapped from group selection, narrowed to WORDs and index incremented, then sign-extended by
`003DDA70`. A negative narrowed index can reject queue acquisition while the owner still becomes3
and consumes its production bit. Ordinary reachability of the large-selector control is unproved.

The original queue pump is no longer unexecuted for this client's terminal composition. The
fixture sets the produced request to state3 and supplies the actual status cell0215EFF4. Pending
status-1 retains it. Success0 calls the original completion, then the pump recycles the slot.
Error-2 on a positive-length request recycles it WITHOUT notifying the owner. The original
state3 queue-cancel path likewise stages cancellation and retires through a null cancel callback.
Both leave this owner state3/source pinned; deletion can select5 after no queue entry remains.
The owner and queue states therefore cannot substitute for one another.

This does NOT run the OS read or the service producer of that status word. Original common-footer
services take configured idle/empty paths. Resetting the fixture queue after observing an error is
not normal recovery. The complete game-level recovery and held-owner dispatcher remain unresolved.

One producer invocation can enqueue64 requests with a sufficiently large fixture handle table;
32 handles yield32 successes followed by genuine handle exhaustion despite byte capacity. Neither
case promises a per-frame throughput, a universal arena handle limit or a retry guarantee.
[Current owner mechanism](the-indexed-source-request-from-arm-to-terminal-pump.md) and
[190 assertions, ten affected variants and limits](../_experiments/evidence/continuation-section09-owner-producer/REVIEW.md).

`0037C2E0` (224 B) is the deferred-init pump `0022B7E0` calls on the `02EBF3DC` state byte: states `0`/`1` bound the `02EBF3DD` index against `003204B0()`'s count and `00320B30`-step each row, `002EAE20`-allocating a `02ADD948` object when rows arrive (state `2`); state `2` `002E4C70`-probes it then `002EAF70`-refcounts or `002EBE20`-flag-writes it, state `3` loops to `1`, and state `4` writes `4` back and returns `0` - the done code the caller reads

Interior anchor `0037C320` (function `0037C2E0`).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

- **ActorEntity — CLIENT (10 edges).** The allocator `002EAE20` and the `0032E400` gate this page's `0037C2E0` cites are also called from actor-entity bodies (`0037B4D0`, `0032FCA0`, `00330310`) — the resource machinery's helpers are shared, fan-in only.
- **CoreRuntimeScheduling — CLIENT and SERVICE (20 edges).** `0022B6E0`/`0022B7E0` are called by the core runtime's `0022A580`, and `0032E040` reaches core helpers — the request queue sits inside the main-loop neighbourhood.
- **Script_VM_Native_Bridge — CLIENT (14 edges).** `002EAE20` is called by script VM / native bridge bodies (`00343A30`, `00344200`, `00354400`) — the same allocator serves the bridge layer.
- **UI — CONSULTED BOTH DIRECTIONS (SWE2-EC7, batch 170, 2 edges).** The `02AD9E00` gate-clear `0036FD70` (the sibling whose tail reaches this batch's `003696D0` drain) is also invoked by UI-filed `00252030`, and the save-storage machine `003BB790` fans out to UI-filed `003BA7B0` — the storage gate crosses the layer boundary in both directions; shared machinery, no shared ownership.

`003696D0` (140 B) is the drain helper the `02AD9E00` flag-clear `0036FD70` tails into (the sibling the non-bearing queue page names as its shared callee): `0016D6A0` resolves twice, the `022D7FC8` slot pair is walked, `005C5230` runs the storage op, and a failure passes through `0035EA30`, resets the global slot to -1 and retries before tailing to `005C5230` - the bounded-drain the save-storage gate runs on clear.

Interior anchor `00369712` (function `003696D0`).
- **CombatAction — CLIENT (2 edges).** 2 inbound (CombatAction bodies `002FC3C0` call page-cited `0032E520`, `0032E590`). Substantive edges include `0032E520` is called by `002FC3C0`; `0032E590` is called by `002FC3C0`.
- **Input — CLIENT and SERVICE (6 edges).** 1 inbound (Input bodies `00291C80` call page-cited `0032E620`); 5 outbound (page-cited `0022B6E0`, `0032E070`, `0022B7E0` call Input bodies `InputControl_SetOneShotFrameCallback` (0035E9A0), `00249C30`, `0035E810`). Substantive edges include `0022B6E0` calls `InputControl_SetOneShotFrameCallback` (0035E9A0); `0022B6E0` calls `00249C30`; `0022B7E0` calls `InputControl_SetOneShotFrameCallback` (0035E9A0); `0032E070` calls `0035E810`.
- **Presentation — CLIENT and SERVICE (17 edges).** 7 inbound (Presentation bodies `003B53C0`, `003B2310`, `002E65A0` call page-cited `0032E400`, `0032E620`, `0032E520`); 10 outbound (page-cited `0022B6E0`, `0022B7E0`, `0032E070` call Presentation bodies `GraphicsSync_WaitBackendState100ClearAndResetSharedState` (0036F2F0), `0036D400`, `002E65A0`). Substantive edges include `0022B6E0` calls `GraphicsSync_WaitBackendState100ClearAndResetSharedState` (0036F2F0); `0022B6E0` calls `0036D400`; `0022B6E0` calls `00252A20`; `0022B6E0` calls `002E65A0`.
- **RNG_Random_Selection — MECHANICAL (2 edges).** 2 calls from page-cited bodies into shared RNG_Random_Selection plumbing (`RNG_MT19937_NextU32_Thunk` (00379CD0)) - the helpers' general call surface, not a RNG_Random_Selection relationship of this page's subjects.
- **World — CLIENT (2 edges).** 2 inbound (World bodies `00378540` call page-cited `0032E400`, `0032E620`). Substantive edges include `0032E400` is called by `00378540`; `0032E620` is called by `00378540`.
- **WorldAreaField — CLIENT and SERVICE (10 edges).** 9 inbound (WorldAreaField bodies `MapRef_BeginLoadResources` (00268750), `00378030`, `AreaArd_LoadOrUnloadFieldResource` (003EA820) call page-cited `0032E400`, `0032E620`, `0032E520`); 1 outbound (page-cited `0022B6E0` call WorldAreaField bodies `003318C0`). Substantive edges include `0022B6E0` calls `003318C0`; `0032E400` is called by `MapRef_BeginLoadResources` (00268750); `0032E400` is called by `00378030`; `0032E400` is called by `AreaArd_LoadOrUnloadFieldResource` (003EA820).
- **Audio — SERVICE (1 edge).** 1 outbound (page-cited `003EADE0` call Audio bodies `002DF660`).
## Falsification pass 1 — 2026-09-30 (OPUS): every section tested survives

**Attack.** The contract's static clauses were turned into checks at their instructions: the interface, invariants I2,
I3, I4 and I6, the slot layout's consumed and cleared fields, and the error helper. SECTION-02/-09's executions and
EXP-146 are carried, not re-run. Script: `Tools/analysis-kit/gfz-scripts/falsify_request_queue.py`, output
`falsify_request_queue.out`, image `73461d08…`, 0 BROKEN, exit 0.

| # | Clause attacked | Result |
|---|---|---|
| Q1 | §2 and §10: the requester and the gated builder | **survives**. The kind and index telemetry is stored before a negative index is refused with `0xFFFFFFFF`. The gate is `003EB0D0`. The gated branch copies `0x28` bytes and sets local `+4 = 0x80000` and `+0x20 = 0`. For a nonzero id only, it clears `+0x50` and sets the cap `0x80000`, chunk word 1, the remaining count, and the signed-minimum first part |
| Q2 | I3, I4, I6 | **survives**. While the free head `022C51D0` is null, it loops pump → in-flight getter → pacer. The id is `(counter << 6) + (slot & 0x3F)`, and the counter at `01EED498` resets to 1 above `0xFFFFFF` by a signed `cmovg`. The offset is `cdq; and 0x7ff; add; and 0xfffff800`, toward zero |
| Q3 | §3: what the requester consumes | **survives**. Descriptor `+0`, `+8`, `+0x10` and `+0x18` are consumed; `+0x20` is never read and slot `+0x50` is cleared. The remaining fields are written as tabulated, and the fifth and sixth arguments arrive at entry `rsp+0x28/+0x30` |
| Q4 | I2 and §2: the free list | **survives**. `0032E990` takes its flag in ECX and the slot from the free head, advancing the head; a null head faults at `[+0x10]`. `0032EC40` pushes the slot on the free head and sets its id to −1, clearing nothing else |
| Q5 | §10: the error helper | **survives**. The done callback runs with success 0 only for a nonnull callback with byte count −1. Kind `0xFF` frees the sign-extended path, and otherwise `rax` still holds the callback pointer, which is not a boolean |
