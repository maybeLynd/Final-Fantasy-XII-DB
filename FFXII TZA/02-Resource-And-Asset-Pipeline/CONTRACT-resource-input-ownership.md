---
contract: "Resource-entry ownership, borrowed payloads, and indexed external-source lifetime"
category: 02-Resource-And-Asset-Pipeline
scope: subsystem
level: L2
readiness: CONTRACT READY
confidence: HIGH
implements: 02-Resource-And-Asset-Pipeline/authored-reference-lifetime-evidence.md
entries: ["003EDAD0", "0026FB90", "0024B3A0", "003B38B0", "003B37E0", "0024F410", "00409A60", "00409D60", "00409730", "003B3480"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-22 (FABLE) on this document's own citations, every
    one resolving into a known section of the authority image; and §4's invariants measured from the
    shipping bytes — both ownership branches disassembled in full and compared instruction by
    instruction, the copy length's rounding idiom decoded, the flag's construction sites read, the
    post-parse merge reduced algebraically from its four instructions, and the context slot censused
    image-wide by two instruments. **The censusing instrument was itself corrected during this work
    — see §15** — and the numbers below are the corrected ones. **This records checks performed on
    that date, not the method of the original derivation**, which is on the lifetime page; see §15.
last_reviewed: 2026-09-30
audit:
  passes: 1
  last_pass: 2026-09-30
  last_pass_kind: falsification
  last_pass_state: opus-resource-ownership-falsification-pass-1
  crossref_clean: false
  reopened_count: 0

external_production:
  section: SECTION-10
  date: 2026-09-23
  status: "locally validated; formal independent acceptance pending"
  evidence: _experiments/evidence/continuation-section10-nonempty-registration/REVIEW.md
---

# Contract — resource input ownership, retention and release

> **SECTION-06, 2026-09-22:** current contract reconciled with the original parser, allocator,
> context/ticket teardown, resource-entry disposal and bounded source-refresh path. Earlier static
> evidence remains in [the lifetime page](authored-reference-lifetime-evidence.md), especially
> sections 13–19. This is local production, not new peer acceptance or a whole-system L2 verdict.
> [Review, exact substitutions and reproduction](../_experiments/evidence/continuation-section06-resource-lifetime/REVIEW.md).

> **SECTION-08, 2026-09-23:** a concrete five-by-sixteen external-owner table is now traced
> through original queue submission, completion, deferred deletion, bank registration/disposal,
> and consumer view pin/unpin. In that section the preparation sweep and full consumer use were static-only;
> no live IO or general safe-reload guarantee is asserted. [Current mechanism](the-external-source-owner-and-borrowed-view-lifetime.md) and
> [review and exact fixture boundaries](../_experiments/evidence/continuation-section08-external-source-owners/REVIEW.md). Prior section receipts remain history.

> **SECTION-09, 2026-09-23:** the original initializers, armer and complete producer now execute
> with synthetic service metadata, arenas and actor-slot flags. The actual queued request is then
> driven through the original pump's terminal branches using fixture-supplied status, not actual IO.
> Pending failure is NOT automatic retry; positive-length error/cancel retirement is NOT owner completion.
> [Producer mechanism](the-indexed-source-request-from-arm-to-terminal-pump.md) and
> [evidence, controls and limits](../_experiments/evidence/continuation-section09-owner-producer/REVIEW.md).

## 1. Purpose

Specify which layer owns resource bytes and which layer only retains pointers into them.
The outer entry can own a copy while its inner EFX context BORROWS that copy. A request slot,
an effect ticket, an arena tree member, an entry, a context and the backing allocation are not
one object and do not share one lifetime. No universal reference-count policy is assumed.

## 2. Interface

| Original body | Interface role and boundary |
|---|---|
| `00409A60(entry, source, mode)` | Setup on the reached entry path: mode0 makes an embedded-buffer copy; mode1 retains the source representation. Not a general replacement transaction. |
| `003B38B0(source32, offset32)` | Takes a free generation-bearing ticket, creates a type3 context with flags0x0C, records source/offset and parses. |
| `0024B3A0(template)` | Allocates/copies 0x890, links the context, allocates its lookup tables and publishes selectors. |
| `003EDAD0(input, length32)` | Parses using the current context; copies or borrows the 800/A00 runs. |
| `003B3480(context, optionalInstance)` | Conditional source refresh; uses current source resolution and signed delta repair, not a retain operation. |
| `003B37E0(ticket32)` | Checks the full ticket ID, destroys matching context/instances, sweeps secondary tickets and recycles the ticket. |
| `0024F410(context)` | Unlinks context; releases owned payloads and lookup tables; destroys associated instances and the context allocation. |
| `00409D60(bank, candidate)` | Finds matching entries; clears selected render references, cancels the ticket, resets the entry and removes its bank slot. |
| `00409730(entry)` | Per-row resource teardown; clearing a reference is distinct from freeing the embedded buffer. |
| `003DD7E0()` / `003DD790(group)` | Reset all eighty / one group's sixteen owner records and masks. Preserve annotation and old request arguments; not destructors. |
| `003DDA20(group,index,annotation)` | Accept only state0; write annotation+8, state2 and the group's pending bit. Does not allocate or submit. |
| `003DD4C0()` | Sweep five groups/sixteen slots; require pending bit AND state2; choose metadata, allocate/pin, then defer state1 or submit state3. |
| `003DDA70(owner)` | Resolves source; submits the original resource request with owner-address callback; writes state3 even if requester returns failure. |
| `003DD850(ownerAddress32)` | Completion first unpins the source. State5 takes disposal/free and state0; other states take registration and state4 regardless of registration's return. |
| `003DD420(group,index)` / `003DD380(group)` | Single/all-sixteen owner deletion: state1 free, state3 deferred state5, state4 dispose/free; do not cancel queue submission. |
| `003DD740(group,index)` | Exposes the stored handle only when owner state is4; does not prove bank membership or allocation liveness. |
| `00409960(entry,tag,name)` / `00409C00(entry)` | Find/pin/resolve a selected view and release that entry's view. The tagged mode uses nonnested membership, not a reference count. |
| `0041E490(manager,sourceRepresentation)` | Acquire then release representation, then tail-call disposal on manager+0xD90 with the ORIGINAL representation. No pin spans that disposal. |

## 3. Types

`EfxCallerTemplate` names the caller's stack layout. `0024B3A0` copies that layout into a
separately allocated runtime context; the stack template does not acquire a heap destructor.
The following fields describe the runtime stage where applicable:

| Context offset | Established obligation |
|---|---|
| `+2`, mask4 | Borrow the 800/A00 input runs when set; copy when clear. Also gates source refresh. |
| `+3`, mask1 | Bulk-run versus individual-entry cleanup layout; independent of the borrow bit. |
| `+8/+10` | Per-kind context next/previous links. |
| `+840/+848/+850` | Separately allocated 0x400/0xA00/0x1800-byte lookup buffers; NOT borrowed run storage. |
| `+858` | Full resolved source base last published by creation/refresh. |
| `+860/+864` | Independent source32 and signed offset32; not one qword pointer. |
| `+870/+878` | 800/A00 run origins; can remain stale after source refresh; zeroed by bulk teardown. |

`RenderResourceEntry` is a 0x50 bank element. Mode+4 selects embedded owned source versus
reference+30; cache+38 is not a lifetime proof; source size+40 is taken from header+8; ticket+44
names the effect ticket. Its embedded `RenderResourceEntryBuffer` begins at +10 and has a
**0x20 transferred storage extent**: `0051EEB0` copies two 16-byte lanes, not only the formerly
claimed 0x1C span. Opaque copied bytes at buffer+4/+1C are not assigned invented meanings.

`IndexedExternalSourceRequest` is a0x1C static owner/request record at
`02B581A0 + (group*16+index)*0x1C`. The observed production sweep covers five groups of sixteen;
the public lookup/deletion helpers do not themselves validate these indices. It stores source
handle+0, state+4, arm annotation DWORD+8, initialized group BYTE+0C, allocation-route receipt+0D,
initialized slot WORD+0E, signed request kind/index+10/+12, requested bytes+14 and file offset+18.
The annotation's downstream purpose remains unresolved: observing its writer is not full meaning.
The producer derives group/index from its loops, not from those initialized identity fields. The
record is not heap allocated; its source handle names a separately owned allocation. Queue-slot
memory, owner-record memory and the bank element remain different objects.

## 4. Preconditions · postconditions · invariants

### The cross-operation invariants

**RL-1 — ownership is layer-relative.** The parser tests mask4 at `003EE018`/`003EE117`.
Copy mode allocates run storage through arena8 and copies into it; borrow mode stores the input
cursor. `003B38B0` supplies a type3 template with flags0x0C, so that context borrows even when
its caller's resource entry owns the encompassing allocation. EFB is another borrowing caller;
it is not the only one. The context constructor itself always allocates the lookup tables.

**RL-2 — borrowed input is mutable.** Original `003A9730` and `003A9A70` write the index/subtype
into payload storage and publish pointers into the selected run. Borrow is not a read-only view.
The fixture's default subtype avoids asserting that every format-specific rebaser is complete.

**RL-3 — allocation, copying and parser bounds are different.** A positive run length is
allocated, but copy length is its signed-32 truncation toward zero to a multiple of16.
An unaligned 0x2B3 fixture leaves the final three copy bytes at their allocation-fill value;
the borrow source still includes them. This is NOT a malformed-input safety proof. Lengths,
lookahead reads, table indices, destination field writes and allocation success need valid bounds.
The original lookahead can read next-chunk metadata before comparing the cursor with the end.

**RL-4 — cleanup layout is not the ownership bit.** When context+3 mask1 is set, 800/A00 teardown
releases +870/+878 only if mask4 is clear, but clears the run pointer in either case.
It ALWAYS releases the corresponding lookup table. When mask1 is clear, individual nonzero
entries are released even with mask4 set: 800 indices1..319 and A00 indices1..767 are walked.
Do not generalize the borrow exception to this separate cleanup layout or to every subobject.

**RL-5 — selectors and cache fields are not ownership handles.** `02F97340` and companion globals
are rebound by construction, parsing/refresh and destruction. Destruction can leave them pointing
into the freed context. Source refresh updates selected lookup pointers and +858 but does not
update +870/+878 in the reviewed context walk. `00409730` clears reference+30 but leaves cache+38.
A surviving numeric pointer is not proof that the referenced allocation is still valid.
The EFB nibble merge preserves its target's low nibble; that algebra does not prove global
selector stability across arbitrary nested calls or concurrency.

**RL-6 — matched disposal orders consumers before owned backing.** `00409D60` first clears its
selected render references, then calls ticket cancellation at `00409EC0`, entry reset at
`00409EC8`, and bank-slot removal at `00409ED3`. Cancellation destroys the context/instances;
entry reset subsequently frees the owned buffer. Mode1 leaves the external backing allocated.
A stale ticket fails the exact ID comparison. Recycled ticket memory is not freed heap storage.
These are the reached API paths, not permission to free an arbitrary borrowed source early.

**RL-7 — state-based source ownership is distinct from queue cancellation and registration.**
Submission stores state3. Deletion of state3 writes5 but leaves the source allocated and the
pending request/callback intact. Completion then disposes any matching entry, frees the source
and clears only state+4: stale handle+0 and route+0D survive. State4 deletion, in contrast, clears
handle+state and route+0D after disposal/free. Lookup exposes only state4. Completion's ordinary
branch ignores registration failure, so state4 is not proof an entry exists. Positive-length
queue-error dispatch does not call this completion; full failure recovery remains unproved.

**RL-8 — the view pair is bounded exclusion, not nested retention.** A successful tagged-mode
view pins through003AB880;00409C00 unpins through003AB940. Two acquisitions followed by one release
restore movement eligibility. Mode0 setup likewise brackets its source copy with one acquire and
one release, which also releases a pre-existing pin. Mode1 setup retains the representation
without acquiring that pin. After actual movement, source-cache refresh is conditional on
02B62E10; a nonzero stale cache is not permission for a consumer to dereference it.

**RL-9 — reuse does not transfer the new owner's allocation.** A same-tag/name registration
returns the existing entry without replacing its backing. Two distinct owner records can therefore
reach state4 while the bank still holds only the first source. Deleting the second owner frees its
own allocation without disposing the first source's entry. This is tested synthetic alias policy,
not proof that every shipped reload path admits competing owners.

## 5. State and ownership

| Owner | Owns / does not own |
|---|---|
| Mode0 resource entry | Embedded-buffer backing allocated/copied by setup; teardown releases it. |
| Mode1 resource entry | Holds reference/cache; this row teardown does not free that external source. |
| EFX runtime context | Its 0x890 object and allocated lookup tables; copy-mode runs, not borrowed runs. |
| Effect ticket table | Fixed slot memory; valid generation references a context. Recycling clears selected fields, not the table allocation. |
| Arena membership pair | Adds/removes a tree member. Two acquires followed by one release reinsert it; this pair is not a nesting reference counter. |
| `IndexedExternalSourceRequest` | Owns its separately allocated tagged source; retains it during deferred state5 until completion. State4 publication does not guarantee registration. Other owner families remain separate. |

## 6. Relationships

[Resource queue](CONTRACT-resource-request-queue.md) scheduling is distinct from the effect ticket
pool at `02EBCD80`/`02EBDB80..B0`. [Arena tree membership](CONTRACT-resource-entry-tree.md) is
not actual deallocation: `003AB880`/`003AB940` remove/add tagged membership, whereas `003AB7C0`
dispatches actual raw/tagged release. [Source rebase](CONTRACT-efx-source-rebase.md) repairs
selected pointers after a detected move. SECTION-06 simulated relocation; SECTION-07 and the
SECTION-08 view control execute actual original compaction. Neither establishes a live schedule.
[Widget lifecycle](../16-UI/Widget-Object-Model/the-title-asset-singleton-and-its-distinct-consumer.md)
remains a separate consumer path. The encoded query's borrowed text pointers are NOT automatically
proved to share this exact owner or refresh protocol.

## 7. State transitions

Entry setup -> source copy or external reference -> ticket/context creation -> context's run
copy/borrow -> lookup publication -> optional detected source move/refresh -> matching consumer
cleanup -> context/ticket recycling -> owned source release -> bank-slot retirement.

The concrete indexed owner has the following bounded transitions:

| Input state/event | Effect |
|---|---|
| State0, arm | Set state2, store annotation and pending bit; return1. Other states refuse and return0. |
| State2 plus pending, failed provider/allocation | Set state0, leave pending bit. A later producer sweep does not rearm it. |
| State2 plus pending, allocation succeeds and hold gate set | Pin source, populate arguments, set state1; consume pending bit without queuing. |
| State2 plus pending, allocation succeeds and hold gate clear | Submit; write state3 and consume pending even if the requester rejects. |
| State1, hold gate later clears, producer sweep | No submission by this sweep; another actual submission route/trigger must be established. |
| Prepared owner, explicit submit | Queue submit then state3, even on a negative-index rejection fixture. |
| State1, delete | Tagged free; clear handle+state and route+0D. |
| State3, delete | Set state5; do not free or cancel the queue request. |
| State4, delete | Matched bank/context disposal first; tagged free; clear handle+state and route. |
| State5, completion | Unpin; dispose/free; clear only state to0, retaining old numeric handle and route. |
| Not state5, completion | Unpin; register plain source; state4 regardless of registration's return. |
| Other deletion states | No action in the tested deletion footprint. |

The producer now has bounded execution evidence in SECTION-09. It prefers arena11 only when
`0037B330()==2` and the selected ActorManagerSlot+17 has mask40; arena6 is the fallback/default.
A successful pin is separate from reclassification to allocation class1. Route+0D records successful
arena11 selection, but it is also overwritten on pending failure/skip; it is not a lifetime token.
File metadata comes from the group providers, not annotation+8. Word narrowing and +1 occur before
signed requester interpretation. Valid metadata pointers and caller indices are preconditions.

The callback identity remains a low32 owner address, not a queue ID or generation-fenced owner
transaction. The tested free/rearm path can reuse the SAME numeric backing handle. Do not infer
request identity from that equality or invent a duplicate-callback exclusion guarantee.

For a positive-length request, the original terminal pump can recycle a service-error or cancelled
queue slot while leaving this owner state3 and its source pinned. Its pending production bit has
already been consumed. Owner deletion then selects state5 without an outstanding callback in this
fixture. This local composition does not establish the game's complete higher-level recovery policy.

A new context does not itself invalidate an older context's borrowed source. Re-parsing the same
copy-mode context overwrites the run pointer without releasing the previous copy in the tested
path; that is a synthetic API-use boundary, not a demonstrated normal-game leak.

## 8. Script · resource · event interactions

800/A00 family metadata are authored input; ownership is caller policy. Source refresh acts only
when mask4 is set. Type3 creation stores a source32 plus signed offset, resolves their source,
and later re-resolves through `003B3480`. In the fixture a simulated tagged-slot relocation lets
the ORIGINAL driver repair the lookup table while retaining the old run-origin field.
No authored asset corpus or scheduling frequency is newly certified. SECTION-08 additionally
executes plain TEST-header new-entry registration and a real context attached for deletion; it
does not execute the nonempty PRF/@FEF branch or certify specialized payload ownership.

## 9. Determinism

No RNG is used in the tested ownership paths. Results depend on current arena state, generation,
mode/flags, source contents, table entries, current globals and the source resolver. Uninitialized
copied padding and stale caches must not be treated as deterministic semantic outputs.

## 10. Failure paths and edge conditions

- Empty effect-ticket free list returns zero before allocating a context.
- Wrong full ticket ID does not cancel an occupied slot. Reusing a retired old ID is a no-op.
- Null source passed to `00409A60` leaves the entry unchanged; its allocator-failure paths are not
  proven transactional. Constructor failure is not a general supported rollback interface here.
- `00409D60` does not sweep render references at all when no entry matches. Exact raw/reference
  comparison and decoded-source comparison must not be conflated for tagged mode1 references.
- `00427B00` clears different sides of the paired render references than `00409D60` compares;
  neither proves a census of every consumer in the executable.
- Direct buffer resize copies min(old capacity,new capacity), not only used bytes, releases old
  source and preserves used. It does not update outside borrower pointers. A higher-level caller
  must order refresh/disposal correctly; live reachability of unsafe interleavings is unproved.
- Original source movement is now tested in SECTION-07 and the SECTION-08 view control. Arbitrary
  malformed inputs, whole live scheduling, thread safety and nonempty specialized children remain
  outside the fixture. Selected synthetic nesting/rejection/exhaustion controls do not prove ordinary
  initialized-game reachability.
- The owner stores state3 after submission without inspecting the requester's return, and state4
  after registration without inspecting its return. The negative-index and zero-bank-capacity
  controls discriminate these facts; they are not claimed to be ordinary gameplay failures.
- Calling0041E490 with a resolved raw pointer does not match a mode1 entry retaining a tagged
  representation. Its pin/unpin pair has finished before disposal. Caller order, not that pair
  alone, must protect a borrowed view.

- Failed metadata selection or allocation leaves state0 plus a pending bit; recovery requires an
  actual state0 arming call, not just another sweep. The active-byte check is not a NULL-pointer guard.
- The fifth group's length accessor returns -1 in the reviewed provider, despite the five-group sweep.
  This is a producer/provider domain difference, not a claim that all fifth-group authored data are dead.
- Slot-handle capacity and arena byte capacity are distinct. The controlled 32-handle arena fails
  further source allocations even with byte storage available; a 128-handle fixture permits64 queued
  requests in one producer call. These are fixture capacities, not newly asserted game-wide limits.

## 10a. Nonempty registration and relocation — SECTION-10

The original `00409FE0` path now runs with nonempty version0/1 PRF records and A00 subtype0
payloads whose encoded fields are nonzero. It first reuses any matching tag/name bank entry. New
entries normalize source names and select owning-copy versus retained-tagged backing. A missing
named `@FEF` leaves an admitted bank entry without an effect ticket. A found section admits the
specialized path but its offset is NOT the parser offset: metadata providers produce a size,
rounded to64 bytes, and a DWORD at source+roundedSize-4 supplies the actual effect offset.

The last five source-name bytes also select an external configuration-string pointer. These
fixtures provide bounded names, valid pointers and the original no-configuration-result branch;
optional `.cm` lookup/priority parsing and their producers are not executed.

Type3 ticket creation and parsing borrow the selected entry backing. Original A00 registration
writes lookup index/subtype and runs subtype0's four pair-relocation helpers on nonzero fields.
For mode0, relocation changes the COPY while normalization has already changed input padding.
For mode1, specialized fixups mutate externally owned source bytes. Same-key reuse does not parse
again. After disposal, explicitly registering that same already-repaired external input again adds
the base again in this synthetic sequence. No restored-relative-data or idempotence guard was found
on the executed path; actual caller refresh/reload discipline remains required.

Bank admission, valid ticket, and successfully parsed payload are separate observations. Exhausted
ticket storage leaves an admitted entry with ticket0. An invalid effect signature can leave a valid
ticket/context with no parsed record. These are discriminating fixtures, not observed game faults.

After an ORIGINAL compactor move, the context/table and embedded encoded words are initially stale.
Original `003B3480` -> `0024D970` -> `003A9BA0` repairs the nonempty record and its eight selected
encoded values. Unchanged re-refresh does not add the delta twice. The borrowed run origin remains
stale, and original disposal releases context/tables before the external owner releases its backing.
[159 assertions, repeat,8 affected variants, and limits](../_experiments/evidence/continuation-section10-nonempty-registration/REVIEW.md).

## 11. Observable behaviour

The observable API differences include pointer identity, input mutation, retained lookup entries,
selective render-reference clearing, per-arena live usage, generation fencing, and actual backing
reclamation. This section does not claim rendered effects, live IO timing, audio output or an
observed game crash. Readiness, publication, allocation membership and pointer bytes are distinct.

## 12. Reproduction formula

Run the original bodies over the fixture's two native arenas, copied/borrowed runs, indexed resource
bank, generation-bearing tickets, matching/unmatched instances and tagged slots. Compare old/new
pointers, sentinel bytes, lists, active/free state and actual allocator usage. Move a source only
through an explicitly simulated slot update, then run the ORIGINAL refresh driver. Inspect the
nine claim groups in the named native assertions rather than treating their count as
whole-game coverage. This describes the SECTION-06 fixture; SECTION-07 supplies actual movement,
and SECTION-08 supplies original indexed-owner/view/queue-client controls. See the delivered [driver](../_experiments/evidence/continuation-section06-resource-lifetime/run_review.py).

## 13. Runtime validation

**SECTION-06:** 171 passing bounded original-instruction assertions; identical repeat; ten targeted
private-image variants rejected by the required assertion. 85 selected original body records match
the authorized EXE. The application diagnostic formatter is substituted, and imported memset,
memcpy and strncpy are bridged. All reached allocation/free, parser, ticket, entry and context
logic otherwise uses the original instructions. Fixtures synthesize arenas, lists, bank pages,
source data and relocation. No fresh live session or full historical Unicorn campaign is claimed.

*Extended 2026-09-26 (FABLE, Claude Opus 5.5), on `OPUS-NOTE-FABLE-S47-OVERLAP-COPY-EXECUTED`:*
the overlapping movement is executed through the bound CRT, not only bridged. The image imports
memcpy from VCRUNTIME140 (IAT `008C2A68`, re-read from the import directory; no app-local copy),
and in VCRUNTIME140 14.51.36247.0 memcpy is `jmp memmove`, so overlap is handled.
`candidates/s47-opus-crt-memcpy-overlap/` executes it on every dispatch path (39,215 copies,
0 failures; `check.py` 8/8), and M07-7s move completes past the import with exact_move's whole
post-state (`overlap_complete.py` 5/5). Scope: the memmove equivalence is a property of the
installed runtime — OPUS found it in all 41 x64 vcruntime140 builds on the host (14.00–14.51) —
not of the game image.

The prior contract's “none executed” paragraph is superseded at this bounded scope. EXP-079 still
does not establish the missing flag from its capture, and this does not retroactively change it.

**SECTION-08:**116/116 original-instruction assertions, identical repeat, nine rejected affected
code variants.120 selected bodies are pinned; this is not instruction coverage. Original requester,
completion/error helpers, owner deletion/completion, plain-header bank registration, views and
allocator/context teardown execute with synthetic state. No queue pump/OS completion, live FF12,
full allocation producer or full consumer body executes. [Reproduction and limits](../_experiments/evidence/continuation-section08-external-source-owners/REVIEW.md).

**SECTION-09:**190 passing original-instruction assertions, identical repeat and ten rejected
impacted variants.138 selected bodies are pinned. Actual allocation failures, metadata providers,
initialization, arming and whole producer execute. Terminal pump tests first queue through that
producer, then supply request-state3/status metadata: pending -1, success0, error-2; cancellation
also uses the original cancellation helper. Original status readers, pump, callbacks and recycling
execute; IO issuance, OS completion and nonempty footer services do not. One diagnostic substitution
and three CRT bridges remain explicit. [Reproduction](../_experiments/evidence/continuation-section09-owner-producer/REVIEW.md).

**SECTION-10:**159 passing original-instruction assertions, identical repeat,8 rejected variants.
114 selected bodies and3 dispatch/signature data spans are pinned. Original nonempty PRF bank
registration, lookup, subtype0 setup/fixup, allocator, movement, refresh and disposal run with
synthetic metadata and payloads. One diagnostic substitution and3 memory/string import bridges;
no live IO, rendering, optional config parsing or full subtype population. [Review](../_experiments/evidence/continuation-section10-nonempty-registration/REVIEW.md).

## 14. Unresolved

1. Shipped asset alignment/size/index guarantees and complete format-specific pointer meanings.
2. Whole-schedule and reentrancy safety, other external-owner families, and matching view lifetimes
   across callbacks. A specific indexed-owner and view policy is now established, not a universal one.
3. Other specialized PRF/EFX subtypes, optional `.cm` priority/configuration producers, and complete
   child creation/rendering ownership. SECTION-10 executes nonempty PRF0/1 and A00 subtype0 setup,
   relocation, actual movement/repair and teardown, not all authored variants or scheduling.
4. The actual service's issuance/completion and higher-level recovery after an owner remains3/5;
   the eventual submission policy for held state1; callback single-delivery/reuse preconditions;
   metadata creation/lifetime, caller bounds and loaded-data reachability of synthetic failure states.
   The original producer's local selection/allocation/rearm and terminal pump composition are now
   executed in SECTION-09; do not schedule another identical sweep as if these were still unexecuted.
5. Whether a particular query/text or widget consumer uses this exact owner chain.
6. Independent peer acceptance of these updated claims and any resulting L2 adjudication.

## 15. Evidence

[Original disassembly](../_experiments/evidence/continuation-section06-resource-lifetime/original_disassembly.txt),
[body manifest](../_experiments/evidence/continuation-section06-resource-lifetime/original_body_manifest.json),
[claim map](../_experiments/evidence/continuation-section06-resource-lifetime/claim_matrix.tsv),
[native controls](../_experiments/evidence/continuation-section06-resource-lifetime/native_controls.c),
[results](../_experiments/evidence/continuation-section06-resource-lifetime/results/summary.json).
Historical static sections and original producer scripts/captures remain unchanged.
[SECTION-08 original caller analysis, controls and claim map](../_experiments/evidence/continuation-section08-external-source-owners/REVIEW.md)
extend this contract without retroactively accepting historical or local claims.

[SECTION-09 producer-to-terminal-pump mechanism and original-instruction controls](../_experiments/evidence/continuation-section09-owner-producer/REVIEW.md)
add evidence at that scope; they do not establish general live IO recovery or independent acceptance.

### 15a. Static anchors retained from the pre-overlay contract (FABLE, Claude Opus 5.5, 2026-09-25)

These are the owner's restoration of the 28 static anchors under RL-1…RL-5 that the rewrite dropped, per
`fable-overlay-dispositions-2026-09-25.md` §3. Each was re-read against the image today. **The rewritten
§4 governs**: these lines are the instruction-level evidence under it, and they re-assert no conclusion
the rewrite corrected.

- **The two mask-4 arms of the parser are one sequence twice.** The A00 arm tests at `003EE018` and the
  800 arm at `003EE117`. On a clear bit each arm runs the same code (`003EE01E`–`003EE06F` and
  `003EE11D`–`003EE168`): `0036C1D0(8, 0xA)`, `0036A100(len)`, `0036C140()`, then `memcpy`. They differ in
  the field they publish (A00 `+0x878`, 800 `+0x870`), and the A00 arm also loads `r11d = 0xA00`. On a set
  bit each arm stores the caller's cursor `r12` in place of an allocation (`003EE078`, `003EE171`). Both
  arms rejoin at `003EE07F` and `003EE178` respectively.
- **Two lengths (RL-3).** The run length is `ebx = cursor − r12 − 4` (`003EE012` / `003EE015`), and
  `003EE02D` allocates with it. The `memcpy` length is `ebx` truncated toward zero to a multiple of 16:
  `cdq` / `and edx, 0xf` / `add` / `and eax, 0xfffffff0` / `movsxd` (`003EE04C`–`003EE061`).
- **The template bit.** `0026FB90` memsets its `0x890`-byte template (`0026FC5B`) and then runs
  `0026FC60 or byte ptr [rsp + 0x22], 0xc`.
- **The nibble merge.** `0026FD1A`–`0026FD26` computes `ctx[+2] = ((entry[+0x16] ^ ctx[+2]) & 0xF) ^ entry[+0x16]`,
  which equals `(ctx[+2] & 0x0F) | (entry[+0x16] & 0xF0)`. The rewrite's RL-5 bounds what that algebra
  proves.
- **The published slot.** `0024B3A0` zeroes `+0x870` / `+0x878` / `+0x880` / `+0x888` (`edx` cleared at
  `0024B430`; stores `0024B45B`–`0024B470`) and publishes the context into `02F97340` (`0024B477`).
- **The container-name lookup `0024F790`** (interior anchor `0024F7DA`), which `0026FB90` calls. `00180370`
  returns the resource name, and a null name exits. The name is copied to a stack buffer. The IAT `strstr`
  (`008C2A08`, `VCRUNTIME140.dll`) is called with the needle at `008FB2B0`. **Correction to HEAD:** that
  string is `"\"`, a single backslash, not a `.jso` suffix (`.jso` is the next string, at `008FB2B4`).
  So `r11` is the character after the name's first path separator, and it is compared against each of the
  `[02092718]` records at `02F93340` (stride `0x10`).

## 16. Parity plan

A later independent implementation should compare ownership transitions, operation ordering,
selective clearing, callback/ticket identities, source representation and pointer validity under
the stated preconditions. Numeric equality of stale pointers must not stand in for ownership.
L3 implementation is not performed here and is not a new database-completion prerequisite.

## Cross-subsystem neighbours — pass 22 (FABLE, 2026-09-29)

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page. `0036A100`, cited in §15a as the allocation between the arena select and restore, is a generic arena allocator: it asks the current arena (`022D89BC`) for the length, falls back to a second allocator, and tags the block header; most edges below are other layers allocating through it.*

**ActorEntity — CLIENT and SERVICE (6 edges).** `ActorResource_BeginPrimaryPayloadLoad` `00330310` and `003306E0` (3,882 bytes) call `0036A100`; `002628B0` calls the all-sixteen owner deletion `003DD380`; `ActorManager_BindLoadedDefinitionPayload` `0026C8C0` calls the group reset `003DD790`; the owner sweep `003DD4C0` calls `00263FF0` (the address of actor-manager slot *n*, stride `0x288` from `02098E10`) and `0032F240` (a flag-gated table lookup by actor index). The actor layer allocates its payloads through the arena allocator and resets or deletes its own owner groups through this contract's API, and the sweep reads the actor slot's flags to choose the arena (§7: arena 11 only when `0037B330` answers 2 and the selected actor-manager slot's `+17` has mask `0x40`).

**CombatAction — CLIENT (1 edge).** `002FC3C0` (183 bytes) calls the context release `0024F410`. An action-layer body releases an effect context through the contract's release call, after the keyed-slot calls it makes first; the ownership rules of §4 apply to that caller as to any other.

**Presentation — CLIENT, SERVICE and DEPENDENCY (61 edges).** Twenty-six Presentation bodies allocate through `0036A100`, among them `CharacterRenderSystem_AllocateAndInitialize` `003325D0`, the parser `003EDAD0` itself, `00436D00`, `00500C00` and `005032D0`; the context API's own bodies are Presentation-filed and call one another — `003B2220` and `003B38B0` call `0024B3A0` and the parser `003EDAD0`, which the template builder `0026FB90` also calls and which calls its per-record handlers `003A77F0`, `003A79C0`, `003A7B50`, `003A7E80`, `003EE2D0` and the two index/subtype writers `003A9730` and `003A9A70`; the refresh `003B3480` (called by `003B3C00`) and `003B3550` call `0024D970`, which calls `003A9860`, `003A9BA0` and `003AA3D0`; `0024F410` calls `0024F4D0`, and the ticket destroy `003B37E0` calls `0024F410`, `0024F4D0` and `003B39E0`; the owner sweep `003DD4C0` is called by `002E65A0` and calls `0037B330` and the submit `003DDA70`; `002E65A0` also calls `0041E490`; `0041E860` calls `003AB7C0`, `00427320` calls `003DD740`, `0041FCF0` calls `00409960` and `00409C00`, `00409730` calls `00427B00`, and `00409FE0` calls `003B38B0`. The ownership API this contract specifies lives in the presentation layer's effect and model code, so these edges are that API's internal calls plus its presentation-side clients; the contract's retention and release rules are claims about exactly these bodies.

**Script_VM_Native_Bridge — CLIENT (3 edges).** The verb bodies `0050D8F0` (176 bytes) calls `0036A100`, `0034A6A0` (36 bytes) calls the single-owner deletion `003DD420`, and `003492A0` (62 bytes) calls the request annotation `003DDA20`. Script verbs allocate, request and delete owner records through the same API; the annotation rule (state 0 only, no allocation, no submit) is what those verbs get.

**World and WorldAreaField — CLIENT (4 edges).** `00266D10` (1,185 bytes, World) calls the full reset `003DD7E0`; `AreaArd_LoadOrUnloadFieldResource` `003EA820`, `00267930` and `003319D0` call `0036A100`. A world body resets all eighty owner records (which §2 says is not a destructor), and the field resource loader and two field bodies allocate through the arena allocator.

## Falsification pass 1 — 2026-09-30 (OPUS): every clause tested survives

**Attack.** The contract's addressed clauses were turned into checks at their instructions: RL-1's mask tests and
template, RL-3's copy length, RL-4's cleanup layout, RL-6's disposal order, RL-7's submission state, RL-8's pin pair,
and §2 / §3's disposal tail, owner records, lane copy, resets and lookup. SECTION-06/08/09/10's executions are carried,
not re-run. Script: `Tools/analysis-kit/gfz-scripts/falsify_resource_ownership.py`, output
`falsify_resource_ownership.out`, image `73461d08…`, 0 BROKEN, exit 0.

| # | Clause attacked | Result |
|---|---|---|
| O1 | RL-1 the parser tests mask 4 at `003EE018` / `003EE117` | **survives**. Both are `test byte [rax + 2], 4` |
| O2 | RL-1 `003B38B0` supplies a type-3 template with flags `0x0C` | **survives**. `mov byte [rsp + 0x20], 3`, `or byte [rsp + 0x22], 0xc` |
| O3 | RL-3 the copy length is truncated toward zero to a multiple of 16 | **survives**. `cdq` / `and edx, 0xf` / `add eax, edx` / `and eax, 0xfffffff0`, interleaved with argument set-up, at four sites in `003EDAD0` |
| O4 | RL-4 cleanup layout versus ownership | **survives**. In `003A9600` (the 800 runs) and `003A9950` (A00), when context+3 mask 1 is set, `+0x870` / `+0x878` is freed only when mask 4 is clear, and is always cleared. When mask 1 is clear, the 8-byte entries are walked to `0xA00` / `0x1800` (indices 1..319 / 1..767) with no mask-4 test. Both end by releasing the lookup table (`jmp 003697F0`). `0024F410` calls both |
| O5 | RL-6 the disposal order | **survives**. `00409EC0 call 003B37E0` (ticket), `00409EC8 call 00409730` (entry reset), `00409ED3 call 0051FCF0` (bank slot) |
| O6 | §2 `0041E490`'s disposal with the original representation | **survives**. It acquires (`003AB880`) and releases (`003AB940`), then `mov rcx, [rdi + 0xd90]`, `mov rdx, rbx`, `jmp 00409D60` |
| O7 | §3 the 0x1C owner records at `02B581A0` | **survives**. The lookup, arm and delete helpers all address `02B581A0` with the record stride |
| O8 | §3 `0051EEB0` copies two 16-byte lanes | **survives**. Two `movaps` loads and two stores to `[rdi]` / `[rdi + 0x10]` |
| O9 | RL-8 the pin pair | **survives**. `00409960` reaches `003AB880`, and `00409C00` reaches `003AB940` |
| O10 | §2 the resets: eighty records and one group's sixteen | **survives** |
| O11 | RL-7 submission writes state 3 regardless | **survives**. `003DDABE mov dword [rbx + 4], 3` follows the last call, with no result test between |
| O12 | §2 the lookup exposes only state 4 | **survives**. `cmp dword [rax + rcx + 4], 4` |

**Verdict.** The contract's addressed clauses hold. Tier 1 (static).
