---
system: Indexed source request arming, allocation and terminal queue composition
category: 02-Resource-And-Asset-Pipeline
status: PARTIAL
readiness: BEHAVIORALLY UNDERSTOOD
confidence: HIGH
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: "SECTION-09: selected original bodies and call sites re-derived; original initializers, armer, whole producer, providers, actual allocators and terminal pump executed on synthetic inputs. Service status is supplied by the fixture, not observed live."
last_reviewed: 2026-09-29
audit:
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-indexed-request-falsification-pass-1
  crossref_clean: true
external_production:
  section: SECTION-09
  date: 2026-09-23
  status: "locally validated; formal independent acceptance pending"
  evidence: _experiments/evidence/continuation-section09-owner-producer/REVIEW.md
---

# From an armed source request to a held, submitted, or failed owner

A source owner, its production-mask bit, its tagged allocation and its queue request are distinct
stateful objects. This mechanism connects the original owner producer to the previously established
[owner and borrowed-view lifetime](the-external-source-owner-and-borrowed-view-lifetime.md).
It refutes two plausible shortcuts: a retained pending bit is not an automatic retry, and a recycled
queue slot is not proof that its external owner received a completion.

[Evidence and exact substitutions](../_experiments/evidence/continuation-section09-owner-producer/REVIEW.md)
contain the original disassembly, 190 named assertions and ten rejecting code variants. The tests
use synthetic loaded metadata and service status; no installed-game scheduling is claimed.

## 1. The storage and initialization footprint

Owner `g,i` is at `02B581A0 + (g*16+i)*0x1C`, with the native sweep covering `g=0..4`, `i=0..15`.
The independent pending mask for group `g` is a DWORD at `02B58A60+4*g`.

| Offset | Representation | Established use |
|---|---|---|
| `+0` | DWORD | Backing source handle. Not a unique request token. |
| `+4` | DWORD | Owner state, separate from queue state. |
| `+8` | DWORD | Armer's third argument, retained as annotation; later semantic meaning is unresolved. |
| `+0xC` | BYTE | Initialized group identity. |
| `+0xD` | BYTE | Preferred-allocation route receipt; pending skip/failure can rewrite it. |
| `+0xE` | WORD | Initialized slot identity, distinct from mapped file index. |
| `+0x10` | signed WORD | Request kind. |
| `+0x12` | signed WORD | Mapped file index after WORD narrowing and increment. |
| `+0x14` | signed DWORD | Transfer length. |
| `+0x18` | signed DWORD | File offset supplied to the queue. |

`003DD7E0` initializes all eighty records; `003DD790(g)` initializes one group of sixteen. Both
clear handle/state and route, write group/slot identity, and clear the appropriate mask. They
preserve annotation and the old request argument bytes. Sentinel controls cover every record,
including the last record and an untouched neighboring group.

These are reset functions, not destructors. They do not free arbitrary live source handles before
clearing the fields. Valid initialization timing is a caller obligation, not proved by this fixture.
The producer derives group/slot from loop registers rather than reading the stored identity pair.

## 2. Arming is a state transition, not a queued read

`003DDA20(g,i,annotation)` accepts only owner state0. It stores the annotation, writes state2, sets
`1<<i` in the group mask and returns1. On every tested nonzero state1..5 it returns0 without
replacing the annotation. The argument and shift/index domain must be valid; there is no new
out-of-range safety guarantee.

The whole producer `003DD4C0` requires BOTH the mask bit and state2. A bit on a state0,1,3,4 or5
record does not make that record a valid new production request. At the common pending-record tail,
route+0xD may be overwritten even when the state was not2; it is not an immutable identity field.

A selected script caller `003492A0` is statically followed: it obtains group/index arguments and
passes annotation0. This supports a concrete caller edge, not an exhaustive arming census or a
full script-execution proof.

## 3. File selection and requested slice

The producer uses `0032F240(g)` to obtain the active group selector. The provider reads a BYTE
enable at `022C6D18+g` and a DWORD selector at `022C6D28+4*g`; a negative selector rejects.
`0032F170` maps it into kind/index outputs:

| Group | Kind | Intermediate file index |
|---|---:|---|
| 0 | 5 | `3 * selector` |
| 1,2,3 | 8 | `4 * selector` |
| 4 | 1 | `selector + 0x6B`, but the producer's length provider subsequently rejects group4 |

The producer stores low16(kind), and stores `low16(intermediateIndex)+1` with WORD wrapping.
`003DDA70` later sign-extends these WORDs to call the queue requester. The difference matters:
a synthetic group1 selector0x2000 yields request index0x8001, rejected as a negative index by the
requester, yet the owner still becomes state3 and consumes its production bit.

`0032F290(g,i)` gets length from the metadata pointer at `022C6E70+8*g`, tests its first byte for
activity and reads DWORD `metadata+0xC+8*i`. `0032F260` gets offset at `metadata+8+8*i`.
The length must be positive. The active-byte check is NOT a NULL-pointer guard; readable metadata
and bounded indices are preconditions. The provider refuses group4 with -1, so this producer cannot
allocate that fifth group's requests through this reviewed length path. This does not establish
that every other fifth-group operation or its authored data is dead.

Annotation+8 and initialized identity fields do not substitute for these provider inputs. The
fixture uses distinct sentinels and offsets/counts to detect wrong-source interpretations.

### FABLE 2026-09-30: the FST extent does not bound the narrowed owner index (OV-42)

*Consumed from ASTRA's [`ov42-selector-fst-bound`](../_experiments/evidence/ov42-selector-fst-bound/README.md) packet after
SWE2-AUDIT-SPEC's review `_index/candidates/auditspec-review-astra-ov42-fst-bounds-0930/REVIEW.md` (ACCEPT-WITH-NARROWING); FABLE record
[`astra-returns-fable-0930`](../_index/candidates/astra-returns-fable-0930/README.md). Static only.*

The WORD narrowing above happens in `003DD4C0`: `003DD610` loads the low WORD of the mapped index, `003DD618` adds 1,
`003DD61D` stores it at `[rbx+0x12]`, and `003DDAA8` sign-extends it for `0032E620`, which rejects a negative value at
`0032E64A`/`0032E64E`. The FST size lookup does not see that WORD. `0032FCA0` (which also stores the group selector that
`0032F240` reads, at `0032FD09`) sizes the **full** index `base+1` at `0032FD94`/`0032FD99` through `0032E400`. For a full
index of `0x400` or more the per-kind override arm (`0032E41F`) is not taken, and the fallback `0032E431` -> `0046DE70` ->
`002DF960` computes `kind*5000 + signed32(index)` and loads a DWORD from the raw 820,000-byte FST table `02EC3EE0` with no
bound check. `003DD4C0` itself sizes from `0032F290`'s directory entry and never calls the size helper; nor does `0032E620`.

Over the declared selector domain 0..32767 (a hypothesis, not a proved caller domain) the twelve language FSTs give:

| group mapping | selectors whose WORD is negative | positive FST sizes at the full index, per language | first alias common to all 12 |
|---|---:|---:|---|
| group 0, kind 5, `3k+1` | 10,922 (from 10,923) | 385 or 386 | k = 11,667: full 35,002, WORD -30,534, flat 60,002 = kind 12 / id 2, size 24,832 |
| groups 1-3, kind 8, `4k+1` | 16,384 (8,192..16,383 and 24,576..32,767) | 961 | k = 8,751: full 35,005, WORD -30,531, flat 75,005 = kind 15 / id 5, size 163,840 |

So "a large mapped index always fails the size check" is false as an argument from table extent, and no single monotonic
threshold exists either. Group-0 selectors 0..10,922 and group-1-3 selectors 0..8,191 cannot give a negative WORD. Group 4
is excluded in code: `003DD4C0`'s length provider refuses it, and `0032FCA0` sets its size to -1 at `0032FDAA`.

A negative size takes `0032FED2 jl 0032FF25`, which loads the group's directory pointer (the `022C6E70 + 8g` table that
`0032F290`/`0032F260` read) and clears its first byte at `0032FF2D`; for group > 3 that is always the path. An old non-zero
directory header therefore does not survive that branch's store.

**Limits kept.** The result covers only `003DD4C0`'s `+1` WORD: the sibling narrowings `003DF4F3 add ax,2` in `003DF440`
and `003EA076 add ax,3` in `003E9F80`, and `0032FCA0`'s sizing of `base+2`, `base+3` and kind `0x25` `base+3`, are not
analysed. No counterexample selector, loaded owner, path-table access, successful companion load, natural selector producer
or interpreter reachability was observed or proved; these are lookup counterexamples to a proposed bound, not rejection or
leak witnesses. The header clear says nothing about intervening caller effects, async write order, the positive-size
branch, aliases or thread interleaving. The precondition stated above (readable metadata and bounded indices) stands, and
the FST extent does not discharge it. OV-42's natural rejection and OV-21 stay OPEN; the next discriminator is every
non-debug selector producer's range into `0032FCA0` and the deferred request that tails into it.

## 4. Allocation, membership and preparation

The selected ActorManagerSlot is `02098E10+g*0x288` via `00263FF0`.
`0037B330` reads the mode at `02ADD930`, except that nonzero `02ADD931` makes it return4.

Only mode2 with ActorManagerSlot+0x17 mask0x40 tries arena11 first. The selection call requests
allocation class5. If that tagged allocation fails, the original code restores the selection and
tries arena6; all other cases go straight to arena6. A successful arena11 allocation records
route1; fallback/default records0. Original stack push/pop behavior and final selected arena are
checked independently.

On success, `0036A000` acquires/pins the tagged source. The separate `0036C620(raw,1)` changes
allocation classification/counters to class1; it is NOT the pin. The producer writes handle,
length, offset and kind/index into the owner.

`00267310(g)` reads ActorManagerSlot+0x201. Nonzero selects state1, a prepared and pinned source
with no queued read. Zero calls `003DDA70`, which submits and writes state3 without testing the
requester's return. Both successful preparation paths consume the production-mask bit.

Clearing the hold byte later and running the same producer does not submit a state1 owner. Its
bit has been consumed and its state is not2. A separate dispatcher or transition must be proved;
none is invented here. Deleting prepared state1 does free its backing. Deleting state2 through
the existing deletion helper does nothing, so an armed request can still be processed afterward.

## 5. Failure and rearming are different operations

| Event | Owner state | Pending production bit | What another producer call does |
|---|---:|---|---|
| Selector disabled/negative | 0 | Retained | No new attempt without arming. |
| Inactive metadata or nonpositive length | 0 | Retained | No new attempt without arming. |
| Both available allocation routes fail | 0 | Retained | No new attempt without arming. |
| Prepared with hold gate | 1 | Cleared | Does not submit merely because hold later clears. |
| Requester rejects a narrowed negative index | 3 | Cleared | Does not recreate the missing queue request. |
| Successful queued submission | 3 | Cleared | Waits for other owner/queue transitions. |

The first three cases are recoverable in the fixture by repairing the cause and calling the
ORIGINAL armer again: state0 is eligible, becomes2 and a later producer call succeeds. Merely
freeing space or fixing the selector, without rearming, does not do that.

Failure here is not a universal promise that the allocator always returns. The fixture configures
active arenas and finite failure; other original allocator states can wait on progress outside
this owner function. Actual game-level retry/scheduling policy remains a separate question.

## 6. Slot capacity and byte capacity are independent

The full-sweep controls arm eighty records with valid metadata for the first four groups, and
request 0x80 bytes per source. With 32 fixture handle slots the original producer queues32 and
then encounters handle exhaustion despite byte storage. With128 handle slots, the same producer
queues all64 eligible requests in one invocation. The fifth group rejects before allocation.
The produced FIFO order is group then slot; only successful handles retain payload usage.

These are actual native allocation/handle failure paths, not a scripted success counter. They
are fixture capacities, not a new assertion that the game's arena always has32 or128 handles.
One call can perform many requests; its occurrence or budget per live frame is not established.

## 7. Terminal queue behavior does not imply owner completion

The producer first queues a real request. The fixture then supplies the service boundary by
setting that slot to request state3 and writing `0215EFF4`. Original status readers, the whole
`0032E070` pump, callbacks, cancellation and recycling execute. The pre-read/OS issuance path is
not run. The pump's common services take configured idle/empty branches.

| Supplied service / action | Original queue result | Original owner result |
|---|---|---|
| Pending -1 | Retains the queued request | State3, not published. |
| Success0 | Calls completion, then recycles slot | Unpins/registers plain source and becomes4. |
| Error-2, positive count | Calls error handling and recycles slot, without owner completion | State3 and source pin persist; no entry registered. |
| Original queue cancel from state3 | Stages cancellation, then retires with null cancel callback | State3 and source pin persist. |

Deleting the owner after either non-notifying terminal path sets state5; no completion remains in
this fixture to finish that deferred free. The public armer refuses5. This is a protocol boundary
requiring a higher-level recovery explanation, NOT a proved permanent game leak or hang. The
fixture's later queue reset/manual source cleanup is not treated as normal engine recovery.

The distinction also explains why the owner state cannot be reconstructed from whether a queue
slot exists. State3 can describe an accepted submission, a rejected submission, or an already
retired request whose owner was never notified.

## 8. Identity after completion/free/rearm

The callback argument is the low32 address of static owner storage. A deferred completion clears
state but can leave the old numeric handle. Valid rearming after completion can obtain the SAME
numeric source handle from the original allocator. Both calls still carry the same owner address.

Thus neither source-handle inequality nor the callback address is an independent per-request
sequence number. This does not prove duplicate completions happen or every stale callback is
admitted in normal gameplay. Delivery uniqueness and record-reuse ordering need their own evidence.

## 9. Remaining reconstruction obligations

- [ ] **OV-33.** Actual service issuance/status production, loading state and outer error-recovery policy.
- [x] ~~**OV-34.** The eventual dispatcher/transition for a prepared state1 owner, if used by shipped callers.~~ *ANSWERED 2026-09-29 (FABLE, applied by SWE2-FRONTIER): none exists - state1 arises under the skip mask, state 4 only via the completion callback, deleters take it to 0. Register OV-34; record `_index/candidates/ov34-state1-owner-fable/`.*
- [x] ~~**OV-35.** Authored selector/metadata creation and lifetime, permitted caller indices and mode meanings.~~ *ANSWERED 2026-09-29 (FABLE, applied by SWE2-FRONTIER): the .mot PKFL directory at 022C6E70, selector = resource-set index, mode->namespace map and g/i bounds enumerated. Register OV-35; record `_index/candidates/ov35-source-metadata-fable/`.*
- [x] ~~**OV-36.** Complete callback single-delivery/reuse and relevant scheduling/reentrancy obligations.~~ *ANSWERED 2026-09-29 (FABLE, applied by SWE2-FRONTIER): at-most-once delivery - every site resets/recycles before the next dispatch; reentrancy universality superseded under OV-2. Register OV-36; record `_index/candidates/ov36-callback-delivery-fable/`.*
- [x] ~~Nonempty authored PRF/@FEF registration and specialized consumer ownership/refresh.~~ *ANSWERED 2026-09-29 (SWE2-FRONTIER): answered by the-nonempty-prf-registration-and-specialized-relocation.md, published in the same commit. Register OV-37.*
- [x] ~~Formal independent acceptance; no L2 or terminal score is awarded by local fixture success.~~ *NOT A QUESTION 2026-09-29 (SWE2-FRONTIER) under the class-2 ruling: an independent-acceptance/process item, carried by board task FABLE-CARRIER-SECTION-OVERLAY-ACCEPTANCE-0929. Register OV-38.*

The Windows overlap-copy question from SECTION-07 remains separate. The native adapter rejects
overlap rather than silently treating Windows memcpy as memmove. Original historical captures and
all preceding section evidence remain unchanged.

## Falsification pass 1 — 2026-09-30 (OPUS): every section tested survives

**Attack.** The static clauses of sections 1–5 were turned into checks at their instructions: the armer, the three
providers, the slot/mode/hold readers, the whole producer loop and the submit. SECTION-09's executions are carried, not
re-run. Script: `Tools/analysis-kit/gfz-scripts/falsify_indexed_source_request.py`, output
`falsify_indexed_source_request.out`, image `73461d08…`, 0 BROKEN, exit 0.

| # | Clause attacked | Result |
|---|---|---|
| I1 | §1–2: storage and arming | **survives**. Owners sit at `02B581A0 + (16g + i)·0x1C`. The armer accepts only state 0, stores the annotation at `+8`, writes state 2, ORs `1 << i` into `02B58A60 + 4g` and returns 1; otherwise it returns 0 |
| I2 | §3: selection, length, offset | **survives**. The enable byte is `022C6D18 + g` and the selector `022C6D28 + 4g` (−1 when disabled). Kinds map 5/`3·sel`, 8/`4·sel` and 1/`sel + 0x6B`. The length and offset providers refuse `g > 3`, test the metadata's first byte, and read `+0xC + 8i` and `+8 + 8i` |
| I3 | §4: the slot, mode and hold readers | **survives**. The slot is `02098E10 + 0x288·g`. The mode is `02ADD930`, and 4 when `02ADD931` is set. The hold byte is `slot + 0x201` |
| I4 | §2, §4, §5: the producer | **survives**. A record needs its mask bit **and** state 2. Every failure writes state 0 and keeps the bit. Arena 11 is tried first only in mode 2 with `+0x17 & 0x40` (route 1 on success); otherwise, or on failure, arena 6, both at class 5. Success pins, reclassifies with 1, and stores `low16(kind)` and `low16(index) + 1`. It then goes to state 1 under hold or submits, and both clear the bit. The route byte `+0xD` is written at the common tail whether the state was 2 or not |
| I5 | §4: the submit | **survives**. The kind and index words are sign-extended, submitted through `0032E620`, and state 3 is written without testing the result |

## Cross-subsystem neighbours — FINAL-AUDIT pass 22, FRONTIER's debt (SWE2-FRONTIER, 2026-09-30)

*Added 2026-09-30 (SWE2-FRONTIER, `SWE2-FRONTIER-PASS22-DEBT-OWN`, batch 5). These are the layers pass 22 still reported for this page. Every edge was listed in full. The subjects are the helpers the sections above read. The far ends are named from the call graph, and the call sites quoted were read.*

**ActorEntity — SERVICE and CLIENT (35 edges).** The manager-slot address `00263FF0` and the group selector `0032F240` are ActorEntity's. The producer `003DD4C0` calls both, and so does `ActorManager_BindLoadedDefinitionPayload` (`0026C8C0`), which also initialises one group of sixteen owner records through `003DD790`. Twenty-nine actor bodies (`0032F1B0` to `003302B0` and peers) take manager slots through `00263FF0`, and `0032FCA0` / `00330310` file requests through the requester `0032E620`. The slot table is the actor layer's. This page reads it, and the actor layer requests sources through the same queue.

**Input — CLIENT and SERVICE (7 edges).** `00226BE0` and `002E09A0` take manager slots through `00263FF0`. `002E09A0` also reads the skip mask through `00267310` and the mode through `0037B330`. `00291C80` files a request through `0032E620`. In the other direction the pump `0032E070` calls the 8-byte getter `0035E810` (`qword [022CA5E0]`) several times, for example at `0032E0F6`, and it steps the four-state pipeline `0046DD50` that the FST page describes. These are shared accessors and a shared pipeline. No input state decides a request.

**Movement — CLIENT (4 edges).** `002E28E0` and `00392740` take manager slots through `00263FF0`. `002E45E0` and `002E5750` read the per-manager skip mask through `00267310`. That is the same read the producer makes to pick state 1; movement uses it for its own skip handling.

**Presentation — CLIENT and SERVICE (18 edges).** The audit files the producer `003DD4C0` itself to Presentation (resolved from its tags). Ten of the eighteen edges are therefore the producer's own calls into the helpers this page reads: `00263FF0`, `00267310`, `0032F170`, `0032F240`, `0032F260`, `0032F290`, the acquire `0036A000`, `0036C620`, the mode read `0037B330` and `003DDA70`. One more is its caller, the compaction scheduler `002E65A0`, which the audit also files to Presentation. The rest are render bodies: `003B2310` and `003B53C0` file requests through `0032E620`; `003A4290`, `003A56F0`, `00465120` and `00465690` take manager slots; and the pump calls `003E9780`. The producer is this page's subject whatever layer the tags give it.

**Save_Load_Settings — CLIENT (1 edge).** `002EF300` clamps a slot number to 0..15 and files a kind-1 request for index `slot + 0x75` into the active runtime save buffer, `0xE240` bytes (`002EF328`–`002EF336`). The save layer loads a save slot through this page's requester.

**Script_VM_Native_Bridge — CLIENT (84 edges).** Fifty-six script bodies read the skip mask through `00267310`, and twenty take manager slots through `00263FF0`: command handlers passing their actor's manager index. `00267E60`, `00344660`, `0034C9A0` and `00357230` read the group selector `0032F240`. `0050DFE0` files a request through `0032E620`. `0050DEB0` acquires through `0036A000`. The verb `003492A0` pops an int through `00267E10` and calls the annotation `003DDA20`. Scripts use the queue's public entry points and the shared actor accessors; the queue's state rules stay this page's.

**World — CLIENT (2 edges).** `00378540` files a request through `0032E620`, and the world body `00266D10` calls the full owner-record reset `003DD7E0`. It is a client of the requester and the reset.

**WorldAreaField — CLIENT (4 edges).** `World_UpdateSimulationTick` (`00314020`) reads the skip mask through `00267310`. `MapRef_BeginLoadResources` (`00268750`), `00378030` and `AreaArd_LoadOrUnloadFieldResource` (`003EA820`) file their field resources through `0032E620`. These are field loads going through this page's requester.
