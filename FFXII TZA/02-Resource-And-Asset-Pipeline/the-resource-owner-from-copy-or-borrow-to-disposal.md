---
system: Resource ownership from copied or borrowed input through refresh and disposal
category: 02-Resource-And-Asset-Pipeline
status: PARTIAL
readiness: BEHAVIORALLY UNDERSTOOD
confidence: HIGH
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: "SECTION-06 isolated original-instruction controls plus selected full-body static reads; simulated relocation, not live movement"
last_reviewed: 2026-09-23
audit:
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-resource-owner-falsification-pass-1
  crossref_clean: true

external_production:
  section: SECTION-10
  date: 2026-09-23
  status: "locally validated; formal independent acceptance pending"
  evidence: _experiments/evidence/continuation-section10-nonempty-registration/REVIEW.md
---

# Who owns a resource, and what can invalidate its pointers?

The relevant layers do **not** use one ownership flag or one lifetime. An outer entry can own a
copy while an effect context borrows that same allocation. Lookup tables belong to the context.
An arena tree records membership, a ticket identifies an effect context, and a render record may
hold one of several different representations of the source. These distinctions determine what
must be invalidated before memory can be reused.

The [ownership contract](CONTRACT-resource-input-ownership.md) states the interfaces. This page
connects them. [Evidence and reproduction](../_experiments/evidence/continuation-section06-resource-lifetime/REVIEW.md)
are bounded original-code execution, not a live FF12 observation or accepted whole-system L2 pass.

The [SECTION-08 owner/view specification](the-external-source-owner-and-borrowed-view-lifetime.md)
now adds a concrete indexed external owner, queue-client completion/deletion and consumer pinning.
Earlier section receipts below retain their original evidence scope.

The primary static and isolated-execution evidence under this page is its evidence note,
[authored reference lifetime and resource allocation evidence](authored-reference-lifetime-evidence.md): the
allocator, handle, relocation and teardown reads that sections 1–8 compose. *(Link added 2026-09-30 by SWE2-CONTRACT,
DD batch 7.)*

## 1. Entry-owned copy versus externally owned backing

`00409A60(entry, source, mode)` resolves a source and normalizes its name in the original input.
For the tested plain header this happens BEFORE copying, so even copy-mode setup is not read-only
on the input. Mode0 constructs/reserves the embedded buffer at entry+10 and copies the source.
Mode1 saves the source representation at +30 instead. The source header+8 supplies size+40.

That mode is independent of the later effect context's borrow bit. `003B38B0` creates a type3
context with flags0x0C and stores source32/offset32 at +860/+864. The context therefore borrows
runs from an entry-owned copy in mode0, or from external storage in mode1. The caller's stack
0x890 template and its separately allocated runtime clone are not the same owned object.

**Implemented setup order matters:** `00409FE0` searches tag/name before it acquires and initializes
a new entry. On a matching existing entry, it returns that slot without replacing the old source
with the new request's contents. The original-path control uses equal names/tags but different
sizes and payload bytes. The old bytes remain. This is cache reuse, not evidence that reload
repairs every reference. SECTION-06 did not execute the new-entry path. SECTION-08 now executes plain TEST-header
new-entry registration. SECTION-10 now adds nonempty PRF0/1 and A00 subtype0 registration,
original nested-pointer repair after compaction and disposal. Other specialized children, optional
configuration and actual game scheduling remain separate.

### Nonempty admission is not a complete initialization verdict

[SECTION-10](../_experiments/evidence/continuation-section10-nonempty-registration/REVIEW.md) discriminates the named `@FEF` admission result from the separate metadata
footer offset actually passed to the parser. The bank can admit an entry with no ticket after a
missing named section, or ticket0 after ticket exhaustion; bad signature can retain a ticket/context
without a parsed payload. Caller-safe inputs and error handling are not implied by the bank index.

A00 subtype0 changes eight nonzero encoded fields in the borrowed selected backing. After genuine
source movement, original specialized refresh repairs these as well as the lookup pointer. Setup
is not idempotent on a disposed and then re-registered already-relocated external buffer: the tested
sequence adds the base again. Copy mode instead repairs its owned copy, not those original payload
fields. Source-name normalization still writes original input in both modes.

## 2. The parser borrows mutable runs, not its lookup allocations

`003EDAD0` checks context byte2 mask4 for families800/A00. Clear selects arena8 allocation and a
signed32 rounded-down copy; set stores the input run cursor. Both then register individual payloads.
Original `003A9730` and `003A9A70` write index/subtype metadata INTO the selected payload and
store pointers into the context's lookup table. Borrowed bytes are writable and must remain alive.

The context's lookup allocations are independent: 0x400 bytes at +840, 0xA00 at +848, and 0x1800
at +850. Their ownership does not transfer to the caller just because the payload is borrowed.
The default-subtype controls exercise original dispatch default returns, not every specialized
format's relocation. Lookahead and index validity remain parser preconditions.

## 3. Teardown is selected by TWO flags

When context byte3 mask1 selects bulk layout, the 800/A00 destructors release their run origins
only when byte2 mask4 is clear, then clear the origins either way. They always release their own
lookup allocation. In nonbulk layout, individual nonnull entries are released regardless of the
borrow bit. Do not apply the bulk exception to that different representation.

`0024F410` unlinks the runtime context and rebinds the working globals before subobject cleanup.
It later frees the context itself. The global `02F97340` may still contain its address after free.
Its value is a selector left by the last operation, not a reference count or liveness certificate.
A separate new context does not itself free or replace an older context's borrowed source.

## 4. The effect ticket pool is not the resource request queue

Type3 creation uses the 64 slots at `02EBCD80`, each0x38 bytes, with active/free links at
`02EBDB80/88/90`. It preserves low6 slot bits and high tag bits while changing generation bits.
This is distinct from the request queue already studied in Update02.

`003B37E0` compares the WHOLE ID before mutation. On a match it destroys associated instances,
then the context, sweeps matching secondary tickets, unlinks the active slot and returns it to
free state. The secondary pool has32 slots; recycling it is not heap deallocation.
The explicit double instance walk does not double-free the tested instances: the first walk unlinks
them. Matching instances are removed, an interleaved other-owner instance survives, and the two
nonempty deferred payloads are queued once. The queue-full and complex-child paths are not tested.

## 5. Actual entry disposal orders consumers before its copied backing

`00409D60` repeatedly finds a matching entry. Only when a match exists does it sweep selected
render records. Then it cancels ticket+44 through `003B37E0`, runs row teardown `00409730`, and
removes the bank slot. The recorded call sites establish this ordering; the integrated execution
checks actual native allocator state and consumer/list outcomes.

Mode0 context/tables and the entry's copied source are released. Mode1 context/tables are released,
but external source backing remains live until its owner releases it separately. `00409730` clears
mode/reference/size and invalidates index/ticket, but leaves cache+38. This disproves the old claim
that a bank row has no per-row teardown merely because it is not individually allocated.

The render clearing is selective. `00409D60` compares source values at +68, +E0, +F8, +42C, +430
and +390, clearing associated fields. `00427B00` instead compares +68, +D8 and +F0. A paired
reference and resolved value are not interchangeable. No matching entry means no `409D60` sweep.
No claim is made that these walks enumerate every reference anywhere in the game.

## 6. Membership, retaining and destruction are different operations

`003AB880` removes a tagged node from its arena tree and returns payload. `003AB940` adds it back.
Both leave the payload allocated. The tested repeated acquire does not add a nesting count: one
release reinserts after two acquires. Generation mismatch protects the membership pair.

Actual `003AB7C0` dispatches raw release to `003697F0`, or tagged release to `00369800`.
The tagged path removes the slot ownership/tree relation and releases the owner allocation through
`00369860`. The fixture proves this with a real allocated node and synthetic matching slot.
It does not prove all slot-reuse ABA cases or the scheduler that moves tree members.

## 7. Movement needs a separate refresh operation

Direct `0051EEB0` reserve allocates replacement, copies min(old capacity,new capacity), releases
old source, and transfers its descriptor. It does NOT repair other objects holding old pointers.
Used bytes are not the copy bound, and the used count survives even a caller-requested shrink.

The separate `003B3480` driver, gated by context mask4, resolves source32 plus signed offset and
compares it with +858. If changed it invokes `0024D970`. The new control simulates a tagged-slot
move, then executes the ORIGINAL driver and lookup-repair walkers. The lookup element moves and
+858 is updated; a repeat does not apply the delta twice. **Run origin+870 is not updated.**
Because borrowed bulk teardown skips freeing that run origin, the stale field does not by itself
force a double free. It still must not be read as the currently valid payload. SECTION-07 now executes actual source movement and selected original refresh paths.
Correct scheduling relative to every consumer remains open; its separate mechanism specifies the
proved call order without converting it into a whole-game timing guarantee.

## 8. A producer closes the buffer-extent ambiguity

`0051EEB0` performs two MOVAPS stores at `0051EF73/0051EF76`, covering descriptor+0..1F. This is
positive write evidence for a0x20 transferred extent, not an alignment guess or a census negative.
The former parent+2C gap is its last four bytes. The temporary does not initialize that padding,
so the store records it as opaque copied bytes without invented semantic meaning. The corrected
layout does not imply all earlier field interpretations or unknown payloads are understood.

## 9. Exact remaining obligations

- [x] ~~Establish whole-schedule/reentrant safety for required consumers, including nonempty specialized
  child/subtype walks. SECTION-07 establishes the original mover and selected refresh paths;
  SECTION-08 adds bounded real view exclusion, not universal safe pinning.~~ *SUPERSEDED 2026-09-29 (SWE2-FRONTIER): whole-schedule/reentrant safety for all consumers including unbounded specialized walks ruled a declared limit under the batch-K class-1 pattern - an exhaustive/universal enumeration beyond the bounds the page proves; coverage is judged in the scope dimension, members unenumerated. Ruling: _index/candidates/register-triage/batch-K-scope-rulings.md, Extension 2026-09-29; register OV-24.*
- [x] ~~**OV-25.** Complete the indexed owner's producer/error-recovery and nonempty registration policy, and
  identify OTHER external-owner families. SECTION-08 establishes this owner's deferred deletion,
  tagged-reference matching and same-key reuse; those are no longer unspecified for this family.~~ *ANSWERED 2026-09-29 (FABLE, Claude Opus 5.5): registration of a loaded source has one door (`00409FE0` <- only the thunk `0041E580` <- four completion callbacks), so there are exactly four owner families: this indexed owner, the motion cache `02B57F70` (refcounted; its sweeps release only loaded slots), the script name-binding record, and the per-lane sub-record `02161DA0` (a lane is freed only when requested and loaded). Error recovery: the OV-42 record; nonempty registration: OV-39/40/41. Still open, kept here: the name-binding record's deletion policy and a stale-node lane requested in flight; [`ov25-queue-clients-fable/`](../_index/candidates/ov25-queue-clients-fable/README.md). Register OV-25.*
- [x] ~~**OV-26.** Establish authored format bounds, shipped alignment/index guarantees, and allocation-failure behavior.~~ *ANSWERED 2026-09-29 (FABLE): authored bounds — all 14,139 shipped `@FRP` containers keep offsets in bounds, every entry 16-byte aligned, the count reproduces the independent tag census; allocation failure — a failed copy allocation leaves the buffer NULL with non-zero size, the copy skipped, setup returning normally without reporting it; [`ov26-frp-bounds-fable/`](../_index/candidates/ov26-frp-bounds-fable/README.md) (`frp_bounds.py` V O M; `alloc.md`, `alloc.py` A T C S). Still open, kept here: what a later parse does with a NULL buffer (static, unread). Register OV-26.*
- [x] ~~Connect other text/widget/audio consumers to this exact owner only where original calls/state prove it.~~ *NOT A QUESTION 2026-09-29 (SWE2-FRONTIER): a method constraint phrased as work, ruled a declared limit of the claim - the page already follows it; nothing remains to answer. Register OV-27.*
- [x] ~~Obtain formal independent acceptance and reconcile only the affected L1/L2 obligations afterward.~~ *NOT A QUESTION 2026-09-29 (SWE2-FRONTIER) under the class-2 ruling: an independent-acceptance/process item, carried by board task FABLE-CARRIER-SECTION-OVERLAY-ACCEPTANCE-0929. Register OV-28.*

## Actual mover follow-up — SECTION-07 (2026-09-23)

[The original source-block mover and separate refresh paths](the-source-block-mover-and-separate-consumer-refresh.md)
now covers tagged-slot movement through `0036A2A0`, its exact/adjacent selectors, real allocation
pressure, dirty child-request delivery and a bounded original combined-walk window. It replaces no
SECTION-06 raw evidence and does not identify unrelated borrowed text pointers as this owner.
The earlier simulated relocation is retained as that packet's explicit scope.


## Concrete external ownership and borrowed views — SECTION-08 (2026-09-23)

There is now a specific owner above mode1 entries: the0x1C table at02B581A0, indexed in five
groups of sixteen. It stores its own source handle and submits an original queue request with
its address as completion argument. Prepared deletion frees immediately; in-flight deletion sets
state5 without cancelling the pending request; completion then cancels matching resource consumers
and frees the external source. Direct state4 deletion clears handle and route; deferred completion
clears only state and leaves the stale numeric handle.003DD740 exposes only state4, not stale state0.

State4 is not proof of bank registration. Completion ignores a failed registration, and a same-name
registration can reuse the FIRST source while a second owner becomes state4. Deleting that second
owner releases only its own source and does not transfer or replace the first source's ownership.
These are bounded native controls; ordinary authored reachability of duplicate/failure states is
not established.

Actual views are bracketed by00409960 and00409C00. This removes/restores tagged-tree membership,
so the acquired view resists the tested move. It is not nested: one release after two acquisitions
allows movement. The copy path likewise releases one acquired pin without preserving an outer
pin. The cache can then become stale and is repaired on lookup only under its02B62E10 guard.
Caller0041FCF0's bracket is read statically; arbitrary consumer callbacks or a whole frame are not
validated. The source-deletion wrapper also releases its pin BEFORE disposal, not after it.

[Full current owner state machine and reconstruction obligations](the-external-source-owner-and-borrowed-view-lifetime.md)
replace the old unrestricted question of whether ANY external owner is known. Other owner families,
real producer/retry schedules, nonempty specialized registration and whole concurrent/reentrant
consumer lifetimes remain open. [SECTION-08 review](../_experiments/evidence/continuation-section08-external-source-owners/REVIEW.md).

`003EE2D0` (219 B) is the four-way record dispatch `003EDAD0` runs on `[rcx] - 0x100`: every arm first publishes `+4` (s32) to `02EBB738`; kind `3` clears `02096B40`/`02096BA4` and tails `0016D680(rcx+8)` when `+2 == 0x4000`; kind `2` `0024ED80`-inits `02096C70`, clears `02096B40`, tails `003EE260(rcx, edx)`; kind `1` does the same on `02096B98`/`02096BA4` tailing `003EE3B0`; kind `0` clears both globals and runs `003ED8A0(rcx)` - the owner-record teardown/transfer selector

Interior anchor `003EE313` (function `003EE2D0`).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (SWE2-EC7)

**Presentation — SHARED HELPERS (53 edges).** `0016D680` — the teardown `003EE2D0` tail-jumps to on the `0x4000` arm — is also called by render-layer bodies `00183A00`, `00183C60`, `00183EE0` and `001946E0`; `0024ED80` (the list initializer `003EE2D0` runs on `02096C70`/`02096B98`) is likewise called by `003B27A0`/`003B3480`, and `003ED8A0` itself calls `003A7730`. Shared teardown/init plumbing, not a resource dependency on the renderer. Edge count from `edges.tsv`. (SWE2-EC7 batch 152, shipping bytes.)

**UI — CLIENT (1 edge).** UI's `0024B9B0` calls `0024ED80`, the initializer `003EE2D0` runs on its two list heads — one shared helper, no ownership crossing.
- **Audio — CLIENT (1 edge).** 1 inbound (Audio bodies `003A1650` call page-cited `00369800`). Substantive edges include `00369800` is called by `003A1650`.
- **CombatAction — CLIENT (1 edge).** 1 inbound (CombatAction bodies `002FC3C0` call page-cited `0024F410`). Substantive edges include `0024F410` is called by `002FC3C0`.
- **Script_VM_Native_Bridge — CLIENT (1 edge).** 1 inbound (Script_VM_Native_Bridge bodies `0050DDA0` call page-cited `00369800`). Substantive edges include `00369800` is called by `0050DDA0`.
- **Script_VM_Native_Bridge — CLIENT (1 edge).** 1 inbound (Script_VM_Native_Bridge bodies `0050DDA0` call page-cited `00369800`). Substantive edges include `00369800` is called by `0050DDA0`.
## Falsification pass 1 — 2026-09-29 (OPUS): every structural clause survives

**Attack.** The structural clauses of §1-§5 became checks that fail if the shipping image says otherwise. Script:
`Tools/analysis-kit/gfz-scripts/falsify_resource_owner.py`, output `falsify_resource_owner.out`, image `73461d08…`, 0 BROKEN.
The behavioural results are SECTION-06 and SECTION-10's executed controls and are not re-run.

| # | Clause attacked | Result |
|---|---|---|
| O0 | §1 the type-3 context template | **survives**: `003B38B0` sets type byte 3 at `rsp+0x20`, ORs `0x0C` into byte 2, and stores source32 and offset32 at template `+0x860`/`+0x864` |
| O1 | §2 the borrow bit | **survives**: `003EDAD0` tests byte 2 mask 4 at two sites |
| O2 | §4 the ticket pool | **survives**: 64 slots of `0x38` at `02EBCD80`, ending at the link cells `02EBDB80`/`88`/`90`; `003B37E0` compares the whole ID before its first write |
| O3 | §5 disposal order | **survives**: `00409D60` finds (`0051FE30`), sweeps render records, cancels the ticket (`003B37E0`), tears the row down (`00409730`), removes the slot (`0051FCF0`), and looks for the next match |
| O4 | §5 "leaves cache +38" | **survives**: `00409730` stores `+0`, `+4`, `+0x30`, `+0x40` and `+0x44`, never `+0x38` |

No correction, so no consumer record.
