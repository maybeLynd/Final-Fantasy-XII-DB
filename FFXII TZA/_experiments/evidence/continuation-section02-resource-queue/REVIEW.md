# SECTION-02 — Resource-request queue production closure

**Production date:** 2026-09-22. **DB_GOAL=NOT_MET.** This completes a bounded local production
section, not the entire resource subsystem, independent T2 acceptance, or the full L1+L2 database.

**Base:** `FFXII TZA(20260922-211246).zip`, SHA-256
`fc02c2fcc0fd305c53e0c8c2949b7b4dad6225921db1328cbfd8cfffea34aeaf`, with
**Update 01** (`482105c6ba0862dac9eeb0c45d0194d53e40205e2c1ee738b916aa3e4b3d7017`) applied.
The original archive and all original experiment programs/results remain untouched.

## What this section does

Re-derive the resource queue's original core control flow, consume EXP-146 at its supported
scope, and reconcile the contract, mechanism page, two experiment narratives and exact type/field
records. The prior work linked the remaining executed entries but left current invariant verdicts
and several conflicting descriptions behind. This section performs that production work rather
than adding another dashboard or repeating Section 1's result-applier checks.

The delivered overlay changes seven existing files (including the continuation handoff); the
complete `types.tsv` and `fields.tsv` are included because those are the files being edited, but
only one type row and thirteen field rows change. All unrelated TSV lines are preserved byte-for-byte.
No names, confidence levels, readiness labels, or offsets of unrelated records are touched.

## Reproducible results and their limits

| Check | Result | Scope |
|---|---:|---|
| Original body-byte checks | 22/22 | Supplied historical Ghidra extents re-read against the authorized EXE; not a fresh GN162 import. |
| Original CPU-instruction checks | 72/72 | Synthetic queue state on Linux x86-64 with Microsoft x64 ABI and explicit service bridges. |
| Repeated native baseline | Identical | Actual callback pointer equality is checked; that host-ASLR pointer is normalized in the displayed return field only. Not 144 unique checks. |
| Changed-code controls | 6/6 rejected | Each fails its intended assertion, not just a crash/timeout. |
| EXP-146 retained assertion branches replayed | 22/22 return pass | Two positive loader branches are vacuous; their native behavior is independently tested here. Not a full producer rerun. |
| Corrupted retained-record controls | 4/4 rejected | Free-head, generation-id, recycle-id and stall-order corruptions. |

See [summary](results/summary.json), [native results](results/baseline.json),
[repeat](results/repeat.json), [mutation outcomes](results/mutation_results.json), and
[retained review](results/retained_review.json). Every check has a name and the retained native
observations include queue state, counters and relevant service/callback order.

These do not claim new installed-game observations, full disk/archive behavior, the producer's
complete Unicorn campaigns, current Ghidra annotation certification, official score generation,
peer acceptance, or reconstruction parity. Original `check.py` comments and JSON remain historical
artifacts; corrected interpretations are in their linked narratives and canonical pages.

## Original-code findings

### Q1. The queue record's “slotArrayBase” is the moving free head

`022C51D0` equals the array start immediately after `0032E450` initializes it. That initial equality
does not define its lifetime meaning. `0032E990` loads the free slot from that global; `0032E9B5`
advances it to the old head's `+0x10`; `0032ECBE` pushes a recycled slot onto it. At `0032E88D`,
RBX is **zero** from `0032E888`, so the comparison is an empty-free-list test, not a bounds test.

`ResourceRequestQueue +0x10` is renamed **freeHead**, with existing pointer width/layout retained.
Pending tail at `+8` is confirmed by original insert/removal instructions and full-graph controls,
not merely adjacency. The pending-head null branch runs a service gate and footer, not an immediate
function return. The type's original 0x28 view still denotes the declared referenced extent; this
work does not manufacture proof of allocation size or a new ownership object.

### Q2. Correct list direction and selective initialization/recycling

Both free and pending lists use **+0x10 next, +0x18 previous**. A stale summary reversed these and
claimed a different pair of free-list links. The constructor's RAX cursor is slot+0x18; its raw
displacements must be translated before describing fields.

With every slot prefilled with A5, the constructor writes only the listed link/index/id/state-kind/
count fields. Its unlisted bytes survive. The free-list splice `0032EC40` writes links and id only;
state clearing is performed by its callers. It does not sanitize callbacks, destinations, kind,
index, counters, caps or unobserved tail storage.

EXP-146's own retained lifecycle has **kind 3 and index 256** after retirement, contrary to its
old prose claiming both cleared and calling the whole record cleared. Native sentinel controls
make this nonzero-versus-zero distinction deliberate instead of relying on initially zero BSS.
A deliberately wrong recycle write and a redirected constructor store are rejected.

### Q3. The pump is head-driven, not one-state-per-frame

After many transitions or releases the original code jumps back to `0032E090` and reloads pending
head. It can process states 1 -> 2 -> 3 -> 5 and retire multiple slots in one call. A waiting head
returns to the footer and prevents a later zero-byte request from being processed during that call.

One new control drains all **64 zero-byte requests in one pump invocation**. Another queues a
65th request against a full pool: that requester pumps the existing 64, paces once, then consumes
the returned slot. This is no queue-full error, but also not a guarantee that real I/O will finish.
The frame wrapper only tests two loader predicates; no frame scheduler resides inside it. The
explicit query form does not pump; the drain form pumps before testing whether work remains.

Thus “next frame at the earliest” and a mandatory frame per state are not valid queue contracts.
Live elapsed time and actual scheduler/concurrency behavior remain unresolved by these fixtures.

### Q4. The common footer is not evidence of shutdown

Empty, waiting and drained pump calls all reach `0046DD50`, `003E9780`, `0036FD50` and, conditionally,
`003BB790`. Empty pending also calls `003EADD0`. The original narrative confused that `xadd0`
trace tag with a different scripted tick-source boundary (`00862090`).

The queue core proves these calls occur, not that they destroy or shut down anything. Existing
mechanism research identifies surrounding read/voice/save services; this section does not newly
execute those implementations. “Common service footer” replaces the unsupported “teardown” claim.

### Q5. A descriptor containing a callback does not mean the requester consumes it

`0032E870` copies descriptor +0 offset, +8 argument and +0x10/+0x18 callbacks. It **unconditionally
clears slot +0x50 at 0032E959**. It does not read descriptor +0x20 for that slot. The gated builder
copies the 0x28-byte descriptor but zeros its local +0x20 and clears slot +0x50 again.

The previously stated transfer `descriptor+0x20 -> slot+0x50` is therefore false for these entries.
A nonnull seeded descriptor pointer makes the control discriminate copying from clearing. The
original descriptor remains unchanged after the gated local copy. Descriptor +4 is not consumed
by the requester; the gated builder writes the actual slot cap separately.

This does not establish that no other code ever installs a part callback. That producer/reachability
question remains separate. No speculative new writer or purpose is inserted into the database.

### Q6. Callback results and absence guards have distinct effects

A null part callback returns 1. Return 1 requeues; return 2 retains progress byte2 and selects the
re-probe branch on a later invocation. Return3 also returns with a pending record but does **not**
select the same branch: a later state5 pass can subtract the previous part again. A synthetic
nonnull callback distinguishes these paths. This is a contract observation, not a claim that the
shipped producer reaches a buggy callback state.

Cancellation clears count only when its callback exists; without one, the old count survives.
Failure invokes the done/error callback only when count is exactly -1. A gated-out error helper
can return its callback pointer instead of zero, so the return is not a boolean success contract.

For path-kind requests, issue and free sign-extend the stored 32-bit value. It is not an arbitrary
full-width char pointer field. Path ownership, repeated cancellation safety and real allocator effects
are not established by the no-free boundary bridge used here.

### Q7. Generation, signed arithmetic and partial rejection stay precise

The original id uses `(counter << 6) + (slotIndex & 0x3F)` in 32-bit arithmetic. The low components
are disjoint under the original shift/mask, so prior OR notation is equivalent in that domain.
Constructor counter 1..0xFFFFFF increments and resets to1; the underlying comparison is signed,
which matters for arbitrary planted values outside that domain. The constructor resets generation,
so this is not a persistent globally unique identity across initialization.

A planted zero counter and slot zero produce **id0 after enqueue**. The gated builder skips its
post-fixups, not the acquisition. Negative builder indices, by contrast, store attempted-request
telemetry and return 32-bit FFFFFFFF without taking a slot. A generation-mismatched cancellation
must not affect a reused slot; suppressing the generation comparison is detected by a mutant.

Offsets truncate toward zero to 0x800; they do not round positive inputs up. Part minima and
remaining termination use signed comparisons. Ten offset controls cover positive/negative aligned
and unaligned values, zero and signed endpoints. A deliberate positive-bias mutation is rejected.
No claim is made that every negative count or invalid counter fixture is normal game state.

### Q8. One counter value is consumed, not a computed duration

State2 calls the getter twice, discards the first result, adds the second to the accumulator and
stores that **same second return** as the stamp. There is no third getter call and no subtraction.
The getter has no own write effect, but that does not prove an external writer cannot change it
between two reads in a live process. The purpose of the accumulated absolute readings remains open.

### Q9. Historical green cases are not uniformly assertive

The EXP-146 checker returns pass for `e040-loader1` and `e040-loader2` without checking that the
pump was entered. Emptying their retained trace still returns pass. This limitation is recorded,
not treated as a new rejection or silently counted as substantive verification.

New native checks prove the idle branch skips the pump, the first predicate short-circuits the
second, and the second can invoke the pump. The underlying predicates remain scripted external
boundaries. The historical 22 cases and full producer source/results are not rewritten.

## Execution boundary and mutation inventory

Original queue bodies run in a private PE image at their expected addresses. The code does not
patch the EXE on disk, attach to FF12, access saves, or publish to the PC repository.

Original subjects executed include constructor, requester, both request wrappers, list take/recycle,
pump, frame/query/drain/cancel paths, local callback helpers, stream flag getter, in-flight/status
getters, counter getter, empty return leaf and free-if-nonnull thunk. The manifest additionally
pins the size resolver and id-query bodies read statically; a hash check is not called execution.

**Scripted boundaries:** `003EADD0` service gate; `0046E030`/`002DF6C0` read issuers;
`0046DD50`/`003E9780`/`0036FD50`/`003BB790` footer services; `0035EA30` pacer;
`001EDE80`/`0017D930` loader predicates; `00369860` free implementation;
`008620C0` diagnostic. Callback pointers installed by fixtures lead to argument-recording host
functions. These boundaries are explicit in [native_controls.c](native_controls.c).

The pacer has one optional controlled read-completion action; it is not a real I/O completion.
The 65-request test uses the original queue to recycle actual fixture slots, not a pacer-injected
replacement slot. The empty-free direct-call negative controls use child processes and verify
SIGSEGV address 0x10. No host/game null-page write is attempted.

The six code mutants alter only private mappings: omit free-head advance, omit generation
increment, redirect one constructor store, clear the wrong recycle field, bias positive offsets,
and suppress stale-generation rejection. Each fails a named assertion; a timeout/crash is not
substituted for mutant detection. Only impacted cases are run, not a full project mutation campaign.

## Canonical files changed

- [Resource queue contract](../../../02-Resource-And-Asset-Pipeline/CONTRACT-resource-request-queue.md).
- [Mechanism page](../../../02-Resource-And-Asset-Pipeline/the-resource-request-queue.md).
- [`_types/types.tsv`](../../../_types/types.tsv): one queue-row constructor/evidence correction.
- [`_types/fields.tsv`](../../../_types/fields.tsv): thirteen scoped queue/slot rows.
- [EXP-128 narrative](../../EXP-128-exp109-poll-pump-exec.md).
- [EXP-146 narrative](../../EXP-146-queue-remaining-exec.md).
- [External handoff](../../../_index/_inbox/EXTERNAL-CONTINUATION.md).

[Exact row changes](canonical_row_changes.json) preserve before/after records.
The earlier contract audit and annotation-transfer metadata remain historical, not acceptance of
this edit. No TEAM task, model identity, active claim, overall score, L2 verdict or reconstruction
source is changed. New code/evidence is attributed to external continuation, not an existing agent.

## Remaining work

Peer review the corrected contract/type facts and map accepted conclusions to S-08's actual
obligations; do not automatically mark L2 MET. Keep the original experiment harness repairs in a
new version/receipt if pursued, preserving historical output. Investigate required real service,
callback-producer and path-lifetime behavior only to the scope needed for the database.

For independent next production work, the retained reward-bindings package remains eligible after
checking the latest uploaded handoff for newer consumption. Section1's producer-intercept and
installer-fixture repairs also remain precisely recorded. A completed section is not database
completion and does not imply that any worker is running between chat turns.

## Reproduction

Merge this overlay into the matching full database after Update01. With Python3.10+, Linux x86-64
and GCC, run:

```sh
python run_review.py --exe /path/to/FFXII_TZA.exe --output /path/to/new/section02-results
```

The runner locates the merged database from its nested directory; `--database` can override it.
It refuses a nonempty output folder, checks the authorized original EXE and pinned producer inputs,
compiles a temporary PIE host with warnings-as-errors, runs and repeats the native baseline, checks
six mutants, replays retained assertions with controls, and rechecks input hashes. No third-party
Python package is required. The compiler and original EXE are not distributed in the overlay.
