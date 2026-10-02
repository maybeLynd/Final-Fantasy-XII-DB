---
system: Indexed external-source owners and borrowed resource views
category: 02-Resource-And-Asset-Pipeline
status: PARTIAL — OV-19 and OV-21 stay open (OV-19's deferred-free ordering against an in-flight read, and OV-21's loaded-state reachability of the synthetic rejection/bank-exhaustion/competing-owner cases; both are runtime remainders) (status line current 2026-10-02, SWE2-CONTRACT DD batch 21)
readiness: BEHAVIORALLY UNDERSTOOD
confidence: HIGH
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: "SECTION-08 owner/view lifetime plus SECTION-09 original initializers, armer, full allocation producer and terminal queue composition. Synthetic service metadata/status; no real IO or whole consumer session. Historical receipts retain their bounded scope."
last_reviewed: 2026-09-23
audit:
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-external-owner-falsification-pass-1
  crossref_clean: true
external_production:
  section: SECTION-09
  date: 2026-09-23
  status: "locally validated; formal independent acceptance pending"
  evidence: _experiments/evidence/continuation-section09-owner-producer/REVIEW.md
---

# Who owns an externally supplied source while requests and consumers use it?

The mode1 resource entry retains a source representation, but does not own the backing allocation.
A concrete owner exists above it: a static table of indexed source requests. That owner can defer
its free until completion, publish a handle despite failed or reused registration, and dispose the
resource's consumers before freeing its backing. Its policy is not the queue's slot lifecycle.

This page specifies that owner and the actual source-view exclusion pair. It extends the
[ownership contract](CONTRACT-resource-input-ownership.md), [queue contract](CONTRACT-resource-request-queue.md),
and [movement mechanism](the-source-block-mover-and-separate-consumer-refresh.md).
[Original bodies, fixtures and limits](../_experiments/evidence/continuation-section08-external-source-owners/REVIEW.md) are reproducible, bounded evidence—not a
live game session, a universal source-owner census, or an accepted L2 verdict.

## 1. Objects that must not be conflated

| Object | Identity, extent and lifetime |
|---|---|
| `IndexedExternalSourceRequest` | Static owner at `02B581A0 + (group*16+index)*0x1C`. The production sweep covers 5 groups of 16; helper callers must supply valid indices. |
| Backing source | Separately allocated tagged source named by owner `+0`. Its numeric handle can survive its deallocation. |
| `ResourceRequestSlot` | Separate 0x80 queue slot at `022C31C0`; stores the owner's address as callback argument, not the owner's state. |
| `RenderResourceEntry` | 0x50 bank element retaining the source representation at `+0x30` and a cache at `+0x38`. Registration can return an earlier entry. |
| EFX context/ticket | A further consumer that borrows source runs while owning tables/instances. Cancellation precedes backing release in the matched owner deletion path. |
| Acquired view | Raw section pointer returned by `00409960`. A successful tagged view removes movement membership; `00409C00(entry)` restores it. Not a counted ownership object. |

## 2. Owner record and initialization footprint

| Offset | Size | Meaning established here |
|---|---:|---|
| `+0x00` | 4 | Tagged source handle; retained after deferred completion frees it. |
| `+0x04` | 4 | Owner state; not queue state and not a bank-success receipt. |
| `+0x08` | 4 | Annotation stored from the armer's third argument. Initializers preserve it; downstream meaning remains open. |
| `+0x0C` | 1 | Initialized group identity,0..4. The producer uses its loop index rather than reading this field. |
| `+0x0D` | 1 | Successful arena11-route receipt; default/fallback/failure writes0. Pending skips can overwrite it. Not a lifetime guarantee. |
| `+0x0E` | 2 | Initialized slot identity,0..15; not the mapped file request index at+12. |
| `+0x10` | 2 | Signed request kind. |
| `+0x12` | 2 | Signed request index. |
| `+0x14` | 4 | Requested byte count. |
| `+0x18` | 4 | File offset supplied to the queue descriptor. |

SECTION-09 executes `003DD7E0` (all80) and `003DD790` (one group): clear handle/state/route and
pending masks; initialize group/index; preserve annotation and old request arguments. These are
reset footprints, not safe destruction of already-live owners.

`003DDA20` accepts state0 only, writes annotation/state2 and sets the pending bit. The complete
`003DD4C0` then reads original group providers and actor-slot flags, allocates/pins, populates the
request and either holds state1 or submits state3. Its class1 allocation-header change is not the
pin operation. The new [producer mechanism](the-indexed-source-request-from-arm-to-terminal-pump.md)
records selector formulas, arena preference/fallback, narrowing, failure/rearm and the two gates.
Its synthetic inputs do not establish actual frame frequency or shipped metadata reachability.

## 3. Submission carries an owner address, not an ownership transfer

`003DDA70(owner)` resolves the backing handle and calls the original `0032E620` requester. Its
stack descriptor contains file offset at `+0`, low32(owner address) at `+8`, completion `003DD850`
at `+0x10`, and a null cancellation callback at `+0x18`.

The tested original request stores that callback and argument in its own slot; the source remains
pinned. The owner writes state3 AFTER the call without using its return. A synthetic signed index
of -1 rejects queue acquisition but still leaves state3. This exposes an interface precondition;
it is not proof the normal producer submits that value.

The callback argument is an address of persistent owner-record storage. It is not an encoded
request ID or a generation fence protecting owner reuse. Correct ordering must be supplied by the
producer/caller; this section does not invent a missing record-generation check.

## 4. Deletion and completion have different clearing footprints

| Operation and prior state | Original behavior |
|---|---|
| `003DD420` on state1 | Free tagged backing; clear handle+state together; clear route byte `+0x0D`. |
| `003DD420` on state3 | Change state to5 only. Preserve backing, pin, handle, queued request and callback. |
| `003DD420` on state4 | Dispose matching entry/context, then free backing; clear handle+state and route. |
| Deletion on other tested states | No action by this deletion path; state5 stays pending. |
| `003DD850` with state5 | First unpin, then dispose/free; clear only the state DWORD. Handle and route byte remain. |
| `003DD850` with state other than5 | First unpin, then register source; write state4 without testing the registration return. |
| `003DD740` | Return stored handle only for state4; return zero otherwise. |

`003DD380(group)` applies the deletion policy to exactly sixteen records. The original control
includes a last-slot state4 owner and a next-group survivor; shortening the loop to fifteen fails.
The lookup/deletion helpers do not range-check arbitrary group/index arguments. Their defined
caller domain is not a malformed-input safety guarantee.

A stale numeric handle after state5 completion is not a live allocation. Conversely, state4 is
not proof an entry was registered: a zero-capacity bank returns no entry, yet completion publishes
state4 and lookup returns its handle. Its later owner deletion still frees the source.

## 5. Queue completion is not queue recycling or universal error recovery

The owner-delete control leaves the real submitted queue slot pending. Calling the original
`0032E330` completion helper dispatches the original owner callback and completes the deferred
free. That helper itself does not unlink/recycle the slot; its caller owns that step.

`0032E370` dispatches completion on its error path only for requested length -1. The tested positive
length `0x180` invokes no owner callback and leaves owner state3 and backing intact. SECTION-09
extends this by actually running the terminal pump with fixture-supplied service status: positive
error and cancellation recycle the queue slot while leaving owner state3 and pin intact. A later
owner delete selects5, but the fixture has no remaining completion to deliver. No real service or
outer recovery path is established; this is not a proved shipped leak or permanent stall. The
fixture resets its synthetic queue only after inspecting these outcomes.

Pre-submission failures are different: a bad selector, inactive/nonpositive length or allocation
failure leaves state0 and its pending bit. Another sweep alone does not retry. A new original arm
call restores state2 and allows recovery when the cause is repaired. Clearing the hold gate alone
does not submit state1. After successful completion/free and valid rearm, the original allocator
can reuse the exact numeric handle; it does not identify the owner's new transaction.

## 6. Disposal uses the stored representation, not resolved equivalence

`0041E490(manager, representation)` first acquires, then releases, then tail-calls `00409D60` on
the bank at manager `+0xD90`, passing the ORIGINAL representation. The temporary pin is already
gone before disposal starts. It is not a lock spanning context cancellation and source free.

The mode1 match at `004095D5` compares against entry `+0x30`. Passing a raw resolved payload
pointer does not match an entry retaining its tagged handle, even though both resolve to the same
storage. Passing the handle does match. Entry disposal alone leaves external backing allocated;
the concrete owner calls `00369800` afterward.

With a real default-payload context attached, the original owner deletion cancels that context,
releases its tables, retires the entry and frees its backing. The outer and inner render-reference
sweeps compare different sides of the paired fields. A pair not cleared by the first sweep can
still be cleared by the later context-cancellation sweep. Whole-chain reasoning must not stop at
a single negative result. Complex nonempty specialized children remain untested.

## 7. Equal-key registration is reuse, not replacement or transfer

The ordinary completion path reaches original `0041E580 -> 00409FE0`. Plain TEST-header fixtures
exercise both new-entry registration and the same tag/name reuse path. Distinct sources with the
same name and different marker bytes produce one bank row retaining the first handle and cache.
Both owner records nevertheless become state4.

Deleting the second owner frees its own source and preserves the first bank entry/source. Deleting
the first then removes that entry and frees the original backing. No ownership transfer or
reference count protects hypothetical additional users in this test. The full PRF/@FEF branch,
authored name conventions and real reload request scheduling remain separate.

## 8. Acquired views have a local exclusion interval, not a nested lock

`00409960(entry, tag, name)` performs selection first. A missing section returns NULL without
acquiring. The successful mode1 branch pins through `003AB880` and returns the resolved source
plus its selected section offset. `00409C00(entry)` ends the view through `003AB940`.

A native arena fixture verifies no tested compaction move while the pin is held. After TWO view
acquisitions, ONE end restores movement eligibility, and the original compactor moves the source.
The entry cache still contains the old address until another guarded lookup refreshes it under
`02B62E10`. The next view then returns the new base. The tested section offset is zero; general
interior arithmetic is separately visible in the original body.

Mode0 `00409A60` copy setup also brackets the source with one acquire/release. The actual copy
import observes the source removed from the tree; afterward it is a member again—even if a caller
had pinned it before setup. Mode1 setup merely retains the representation and does not pin.
This pair cannot be treated as independently nestable retain/release calls.

The complete static body `0041FCF0` calls the view at `0041FFA0`, uses the returned value while
performing its consumer work, and ends that entry's view at `0041FFF8`. The consumer itself and
its callbacks are not executed here, so no assertion is made that all descendants avoid retaining
raw pointers or that arbitrary reentry is safe. A separate buffer-view consumer `005371C0` is also
read statically, not substituted for a live rendering proof.

## 9. Reconstruction obligations and remaining boundaries

A compatible implementation needs separate owner, queue, bank and view states; matching source
representations; selective clearing; and the original operation order. It must not turn every
failure into rollback, every completion into registration success, every pin into a reference
count, or every stale pointer into a live reference.

- [x] Execute original initialization/arming/full producer with controlled metadata and allocator state; establish local failure/rearm and original terminal-pump callback/recycle behavior (SECTION-09).
- [ ] **OV-19.** Establish actual IO issuance/completion, outer recovery after owner state3/5 outlives a queue entry, held-state1 submission, and callback single-delivery/reuse preconditions.
- [x] ~~Establish nonempty PRF/@FEF registration, specialized consumers and their ownership/replacement rules.~~ *ANSWERED 2026-09-29 (SWE2-FRONTIER): nonempty PRF/@FEF registration and the specialized consumers are on the-nonempty-prf-registration-and-specialized-relocation.md (published in the same commit); `uq218-residue-fable` (a20f0a985) carries the E/C ticket consumers. Register OV-20.*
- [ ] **OV-21.** Determine the relevant loaded-state reachability of synthetic rejection, bank exhaustion and competing-owner cases.
- [x] ~~Establish full consumer scheduling/reentrancy where required; the local pin pair is not a threading proof.~~ *SUPERSEDED 2026-09-29 (SWE2-FRONTIER): duplicate of OV-2 - the same ask in substance; OV-2 carries it. Register OV-22.*
- [x] ~~Complete independent peer review and incorporate accepted claims at their earned evidence level. No L2 or final-audit acceptance is self-awarded.~~ *NOT A QUESTION 2026-09-29 (SWE2-FRONTIER) under the class-2 ruling: an independent-acceptance/process item, carried by board task FABLE-CARRIER-SECTION-OVERLAY-ACCEPTANCE-0929. Register OV-23.*

The deployed Windows copy-overlap dependency from SECTION-07 is still unresolved. SECTION-08's
copy bridge rejects overlapping inputs rather than silently changing them to memmove.


## 10. SECTION-09 evidence boundary

[The producer-to-terminal-pump specification](the-indexed-source-request-from-arm-to-terminal-pump.md)
and [review](../_experiments/evidence/continuation-section09-owner-producer/REVIEW.md) distinguish
190 assertions from distinct states and138 selected body identities from instruction coverage.
Original status readers and pump execute after fixture service-state preparation; no new live
session is claimed. Existing SECTION-08 evidence is unchanged. Acceptance remains pending.

`0041F340` (1006 B) is the per-element external-section attach: it resolves the record's `+0x10`-keyed manager tables (`+0xD90`/`+0xD98`/`+0xDA0` via `0020E600`), locates or registers the `0x52544640`-tagged section through `00409660`/`00409FA0`, measures it with `003712E0` into the `+0x480`/`+0x484`/`+0x488`/`+0x48C` extent fields (0x3A0-rounded, `+0x284 |= 0x10000` when the tail lane exists), allocates and copies the payload through `003AB8B0`/`003AB7F0`/`00861EC0`, binds the element record via `0046E4D0` (index resolved by `002ED570` when the id is not -1), stamps `+0x18`/`+0xA8`, and finishes with `00372350`/`00373100`/`00421CD0`/`004780C0` plus the optional `003B3550` back-reference into `+0x288`.

Interior anchor `0041F565` (function `0041F340`).

## Cross-subsystem neighbours — batch-145 addition (SWE2-EC7)

**Presentation — member body hosted here.** `0041F340` is a Presentation-owned section-attach pass documented on this page; its callee set (`002ED570`, `003712E0`, `00372350`, `00373100`, `003AB8B0`, `003AB7F0`, `00861EC0`, `0046E4D0`, `00421CD0`, `004780C0`, `003B3550`, `00409660`, `00409FA0`, resolver `0020E600`) carries heavy traffic to and from Presentation callers. The crossing is a Presentation body whose borrowed-view mechanics live on this page, not a resource-pipeline dependency on that layer.

`003AB8B0` (87 B) is the mode-selected record acquisition the section-attach path calls for its payload: inside a `0036C1D0(6)`/`0036C140` bracket it dispatches on `ebx` - mode 0 resolves through `0036A100`, mode 1 through `0036B160`, other modes fall through returning null - handing the acquired record to the copy and bind steps `0041F340` performs next.

Interior anchor `003AB8DC` (function `003AB8B0`).

`003B3550` (642 B) is the presentation-slot registration `0041F340` invokes for its optional back-reference: bracketed by `0036C1D0(8)`/`0036C140`, it looks the category record up through `0024F610` (a type-3 request keyed on `si`), takes the target object from `003B3400`, and when the record's `+2` flag byte carries bit 4 publishes it into the `02F97340`/`02EBEF70`-family globals (subfields `+0x18`, `+0x848`, `+0x38`, `+0x850`, `+0x840`); it verifies `003AB7F0(+0x860)` plus `+0x864` against extent `+0x858` (`0024D970` on mismatch), clears a `0x3B0`-byte template (`00861EC0`, tag word `0x103`), instantiates it through `0024B270`, and initialises the new record - flag words `+0x368`/`+0x36A`/`+0x378` rebuilt from the `[rbx+0x48]` source's `+0x17` bit and the `0xBFFF`/`0xFFF7`/`0x800`/`0x100` masks, `+0x320..+0x328` = 1.0f, `+0x330`/`+0x334`/`+0x398` = `0x80808080`, `+0x340` back-linked to the source, `+0x370` = `0x102`, marker bytes `+0x2D0`/`+0x2E0`/`+0x2F0` = 0xFF.

Interior anchor `003B36A2` (function `003B3550`).

`0024D970` (73 B) is the extent-delta drain the registration paths `003B3480`/`003B3550` run when a record's span moves: `arg2 - [rcx+0x858]` becomes a signed count fed in order to `003AA3D0`, `003A9BA0` and `003A9860`, and the new extent is then stored back into `+0x858` - the three callees consuming the queue backlog the delta represents before the record is marked current.

Interior anchor `0024D994` (function `0024D970`).

`004780C0` (215 B) is the slot-fill `0041F340` runs on the owner record: `0051FBB0(rcx)` resolves the slot (-1 returns 0), `0016D6A0` fixes up the record pointer before and after, `002ED570(rcx, slot)` resolves the target, and `00504F00` writes it with `u16 slot` stored at `[rbx]` - the queued fill step between `002ED570` lookup and `00504F00` commit

Interior anchor `00478105` (function `004780C0`).

`00504F00` (582 B) is the commit `004780C0` tail-calls after `002ED570` resolves the target: it copies the caller's 32-byte record to `+0xC..+0x2B`, stores `+0x30`/`+0x38`/`+0x40`, `00409F50`-resolves `r8`, binds two `00504E70` tag sections (`0x50524640`, `0x46454640`) at `+0x1F0`/`+0x228`, then `00409A30`-looks up seven `0x4x46xxxx` tags into `+0x208..+0x220`, runs `00504940`, and scans the resolved record's `0xE0`-stride `+0x30`-counted byte table for the `+0xB8`/`+0xB9` sentinel fills

Interior anchor `00504F94` (function `00504F00`).

`005049E0` (470 B) is the record default-constructor the commit path uses: `0xFFFF`/`0xFF`/`0xFFFFFFFF` sentinels across `+0`/`+0xE0`/`+0x140..+0x178`/`+0x208..+0x220`, `006C0520` writes three vec4 defaults (1.0f at `+0x90`/`+0xA0`, `448.0/255.0` at `+0xD0`), `0046D110` inits `+0x50`, `+0x244` clears `0x1B` and sets bit 2, `+0x248 = 1.0f`, `+0x250` = `0.0299f`, then a 20-iteration loop fills the `+0x180` byte/`+0x194` dword pair-table - the pristine-owner baseline

Interior anchor `00504A7F` (function `005049E0`).

`00409960` (208 B) is the kind-dispatched record resolver `0041FCF0` runs: `00409780` yields the index (-1 returns 0); `+4 == 0` resolves the inline `+0x10` array through `0051EE30`/`006B5C70`, `+4 == 1` resolves the `+0x30` external row through `003AB880`, and `+0x40` adds a base offset - the borrow-vs-inline split made concrete at each access

Interior anchor `004099A7` (function `00409960`).

**Movement, ActorEntity and Script VM — CLIENT (shared-callee edges, SWE2-EC7-189).** The `006C0520` vec4-fill helper my `005049E0` entry names is also consulted by the movement layer (`00268380`), and that caller is itself reached by actor-entity callers `00266530`/`00269E20`/`00269E40` (with `0032E620`/`0032FCA0` on the same side); `00269E20`, `0032E620`, `00369800` and `003DD420` in turn carry script-VM callers (`003419A0`/`0050DFE0`/`0050DDA0`). The crossing is those layers calling shared primitives this page names, not shared responsibility. Edge list from `edges.tsv`.

`003AB880` (42 B) is the alignment guard `00409960` and `0041E490` both run on a resolved record pointer: a null input returns 0, a pointer with `ptr & 3 == 0` returns itself, and anything misaligned tail-jumps `0036A000` (the subsystem's invalid-parameter handler) with `ecx = ptr` - the 'aligned or die' check both record-resolver families share

Interior anchor `003AB88B` (function `003AB880`).

`0051D220` (200 B) is the lazy pool init `0041F340` runs: under the `02CA842C` once-guard it derives two sizes by `1 <<` the bytes at `01F2B34C`/`01F2B34B`, `00184140`- and `001837A0`-allocates into `02CA8430`/`02CA8438` seeded from the `01F2B340` word table, then clears `02CA8428`; on re-entry it only clears `[rcx+6]` and `02CA8428`

Interior anchor `0051D284` (function `0051D220`).

`00504940` (152 B) is the two-id resolve-and-cache `00504F00` runs: `00409F50([rcx+0x30], word[+0x1F0])` then `004096C0(row, dword[+0x200])` caches `+0x1F8`; when the resolved row's lead word differs from `[rbx+0x228]` it re-resolves through `00409F50` for that id, then `004096C0(row, dword[+0x238])` caches `+0x230` and a non-null result feeds `0016D6A0([rdi+0x44], rax+0x30)`; `[rbx+0x48]` mirrors `+0x1F8` - the borrowed-view pointer refresh.

Interior anchor `00504958` (function `00504940`).

`00442460` (121 B) is the `+0x282` subtype dispatcher `003A9860`'s rebase sweep runs over every live `02EBEF90` slot: `byte[rcx+0x282]` indexes the nine-entry RVA table at `004424B4` whose cases tail to `00442380`, `005322F0`, `00532310`, `00532380`, `005323F0`, `00532440` (twice), `005324C0` and `00532520`; a subtype past 8 falls through and returns the payload itself - the per-record front dispatch on the lifetime table.

Interior anchor `0044248B` (function `00442460`).
- **Audio — CLIENT (4 edges).** 4 inbound (Audio bodies `003A1650`, `003A12D0`, `003A1330` call page-cited `0036D170`, `00369800`). Substantive edges include `00369800` is called by `003A1650`; the remaining edges run through shared helpers the page cites.
- **Save_Load_Settings — CLIENT (1 edge).** 1 inbound (Save_Load_Settings bodies `002EF300` call page-cited `0032E620`). Substantive edges include `0032E620` is called by `002EF300`.
- **World — CLIENT (2 edges).** 2 inbound (World bodies `00378540`, `00266D10` call page-cited `0032E620`, `003DD7E0`). Substantive edges include `0032E620` is called by `00378540`; `003DD7E0` is called by `00266D10`.
- **WorldAreaField — CLIENT (3 edges).** 3 inbound (WorldAreaField bodies `MapRef_BeginLoadResources` (00268750), `00378030`, `AreaArd_LoadOrUnloadFieldResource` (003EA820) call page-cited `0032E620`). Substantive edges include `0032E620` is called by `MapRef_BeginLoadResources` (00268750); `0032E620` is called by `00378030`; `0032E620` is called by `AreaArd_LoadOrUnloadFieldResource` (003EA820).
## Falsification pass 1 — 2026-09-29 (OPUS): every structural clause survives

**Attack.** §1-§5's structural clauses became checks that fail if the shipping image says otherwise. Script:
`Tools/analysis-kit/gfz-scripts/falsify_external_owner.py`, output `falsify_external_owner.out`, image `73461d08…`, 0 BROKEN.
The behavioural results are SECTION-08 and SECTION-09's executed controls and are not re-run.

| # | Clause attacked | Result |
|---|---|---|
| E0 | §1-§2 the table and the one-group reset | **survives**: owners at `02B581A0 + (g·16 + i)·0x1C`. `003DD790` clears handle and state (one qword), sets the route byte `+0x0D`, group `+0x0C` and index `+0x0E`, and clears the mask at `02B58A60 + g·4`. It never touches `+0x08` or `+0x10`..`+0x1B` |
| E1 | §2 the armer | **survives**: `003DDA20` takes state 0 only, writes `+0x08` and state 2, and ORs the pending bit |
| E2 | §3 the submit descriptor | **survives**: file offset at `+0`, low32(owner) at `+8`, `003DD850` at `+0x10`, null at `+0x18`. State 3 is written right after `0032E620`, whose return is not read |
| E3 | §4 the sixteen-record deletion | **survives**: state 1 frees and clears; state 3 becomes 5 only; state 4 disposes (`0041E490`) before it frees (`00369800`) |
| E4 | §4 completion | **survives**: `003DD850` receives the owner as `mov edi, ecx`, low 32 bits, and unpins (`0036D170`) first. State 5 then disposes, frees and clears only the state dword; any other state registers (`0041E580`) and writes 4 without testing the result |
| E5 | §4 lookup | **survives**: `003DD740` returns the handle for state 4 only |
| E6 | §5 the error-path dispatch | **survives**: `0032E370` calls the completion only when its callback is set and the requested length is `-1` |

No correction, so no consumer record.

`00442380` (213 B) is the fourteen-slot field apply that `00442460`'s case table and its seven direct callers share: `004304F0` runs over the seven `0x10`-stride subfields `+0x00`..`+0x60`, then `00430AF0` over the seven `0x40`-stride subfields `+0x70`..`+0x1F0` - the common sweep every subtype apply begins with before its own tail.

Interior anchor `004423DC` (function `00442380`).

`00532520` (174 B) is the extended apply `00442460` dispatches for its deepest subtype: the shared `00442380` sweep runs first, `00430AF0`/`004304F0` extend it over `+0x2DC`..`+0x35C`, then a 32-iteration loop reads the byte row at `+0x36C`, resolves each nonzero byte through `003AA280(0, 0x54, b)` and `0020E620`, and writes the resulting dwords at `+0x39C` - the largest of the table's case bodies.

Interior anchor `00532580` (function `00532520`).
