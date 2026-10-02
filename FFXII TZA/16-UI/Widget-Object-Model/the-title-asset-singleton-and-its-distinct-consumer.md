---
system: The title asset singleton and its distinct consumer
category: 16-UI
status: PARTIAL
owner_layer: UI widget object model
readiness: BEHAVIORALLY UNDERSTOOD
evidence_tier: 1
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: "SECTION-04 original-byte/control-flow review plus bounded native original-code execution with explicit service substitutions; not live FF12"
last_reviewed: 2026-09-29
audit:
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-title-asset-falsification-pass-1
  crossref_clean: true
  reopened_count: 0
local_production: "SECTION-04 complete locally; independent acceptance and full-system L2 remain pending"
---

# The title asset singleton and its distinct consumer

This page corrects a receiver census, not merely two field names. The producer/consumer chain
contains **a 0xD8 asset widget, a different 0x1D0 consumer, and a message record**. Following a
published pointer does not make all the registers in the containing function point to that widget.

The existing [menu atlas](../Menu-Screen-Atlas/members/ui_atlas_all.tsv) associates `00394070`
with title assets. The original request descriptor points to the `title_logo` string. This section
has not reopened an authored archive, rendered the screen, or verified those files during a live
session. The behavioral conclusions below come from the original code and bounded fixtures.

[Production review and reproduction](../../_experiments/evidence/continuation-section04-widget-receiver/REVIEW.md).

## 1. Identity comes from two different construction chains

| Property | Asset widget | Consumer |
|---|---|---|
| Published pointer slot | `02AEE4C0` | `02AEE4C8` |
| Factory | `00394460` | `00394530` |
| Requested object extent | `0xD8` at `0039449F` | `0x1D0` at `0039456C` |
| Selected handler | `00394070` at `00394498` | `003939B0` at `00394571` |
| Publication instruction | `003940F5` | `00393A11` |
| Relevant receiver alias | RBX in own handler; RDI in `00393FF0` | RSI in `003939B0` |

Both factories ultimately use `00244F50` and `002465F0`; sharing those helpers does not make their
subclass storage the same. The small allocation can occupy a `0x120` backing slot, but the
initializer clears only the requested `0xD8`. A backing stride is not the logical type extent.

`00394460` tests the asset publication slot at **`0039448B`**, not at `003944A4`; the latter is
the allocation call. It performs several preliminary calls before the null guard. Thus an
already-published asset suppresses this allocation, not necessarily all side effects of the factory.

The consumer factory first requires a nonnull asset publication, then either allocates the
separate consumer or handles its existing instance. The original allocation/wrapper path is
exercised with synthetic objects; the earlier calls in the asset factory are inspected statically.

## 2. The two invalid supports

At consumer entry:

```asm
003939D1  mov rbx, rdx       ; WidgetMessage*, not the asset widget
003939D6  mov rsi, rcx       ; this 0x1D0 consumer, not the asset widget
003939F7  movzx eax, [rbx+8] ; message payload's low byte
003939FB  xor ebx, ebx       ; clears all of RBX through a 32-bit write
00393A23  lea edx, [rbx+15h] ; computes 21; does not read memory
```

The init arm stores the message byte in the **consumer's** `+0xC0`, zeroes its state at `+0xC4`
and child pointer at `+0xC8`, publishes to `02AEE4C8`, and sets channel 1 bit 21 through
`002E1C20`. A native control gives message+8 and receiver+8 deliberately different bytes; the
original handler uses the message. Another control observes the constant channel/bit arguments.

The former `WidgetSingleton02AEE4C0.byte0008` and `dword0015` supports are withdrawn.
**This does not prove that no legitimate generic Widget field exists at overlapping offsets.**
The local type table no longer invents those two asset fields from these instructions.

The earlier producer's general “sound for presence” claim fails on this counterexample. Its source
is not in the supplied archive. This package supplies a separate bounded intrafunction diagnostic
and targeted tests, not a claim that the upstream scanner was repaired or the entire widget family
recertified. The known coverage/missed-displacement statistics do not rescue a false positive.

## 3. The asset has actual producer and lifecycle fields

| Offset | Original evidence | Bounded meaning |
|---|---|---|
| `+0xC0` DWORD | zero at `003940FC`; OR 1 at `003940E3`; low bit read at `00393A98` | Resource-ready flags for this asset widget; other bits unassigned here. |
| `+0xC8` QWORD | store at `00394033`; read at `00394097` | Resource-entry result passed to `0024A680(ptr, 1)` on message 18. |
| `+0xD0` QWORD | store at `00394050`; read at `00393AA5` and `003940A8`; zero at `003940B9` | Loaded-block result consumed by the other widget and released/cleared on message 18. |

`00393FF0` obtains a request ticket through `00249580`, calls the resource service with
`(ticket, 7, 0x3D, 3, descriptor, 2)`, retains the result at +0xC8 and clears **the returned
record's** DWORD +0x40. It calls the second service with `(ticket, 7, 0x3A)`, retaining its result
at +0xD0, then submits the ticket through `00249410`.

That returned record's +0x40 is not the widget's header-flags field at the same offset.
The missing +0xC8 store also refutes the old twelve-byte “unobserved” span starting at +0xC4.
There are four unresolved bytes at +0xC4, followed by a known QWORD pointer.

### Publication is earlier than readiness

Own message 1 publishes the widget, zeroes +0xC0, and starts the two requests. The request-ticket
constructor records the owner. For the newly created ticket's ordinary owner-notification branch,
`00249410` emits message 16 synchronously when its two counters are equal; otherwise it leaves
completion pending. Own message 16 ORs bit 0 without altering other bits.

Native fixtures cover both equal counters and two deliberately pending service results.
The service returns/counts are explicitly scripted. This establishes the original caller's
branch/order under those controls, **not real asset latency or actual IO completion**.
A nonnull publication slot is therefore not by itself a readiness flag.

### Cleanup is asymmetric, and publication is not an ownership token

Own message 18:

1. Passes +0xC8 to `0024A680` with mode 1.
2. If +0xD0 is nonnull, releases it through `003697F0` and clears +0xD0.
3. Clears channel 0 bit 21 and sets `02AEE4C0` to zero.

It does **not** clear the +0xC8 pointer or ready flags. In a synthetic mismatch control, it also
clears the publication even if that slot no longer equals the supplied receiver: there is no
receiver-equality guard in this handler. This is a bounded instruction fact, not evidence that
such a mismatch occurs in an ordinary game session.

Retained +0xC8 bytes are not proof of a live resource. This handler is not asserted idempotent,
and neither these controls nor the presence of a null guard proves safe arbitrary replay of
teardown. Common widget storage-freeing, real cancellation completion and external lifetimes
remain outside this section's certification.

### FABLE 2026-09-30: the ordinary completion sender and the local retirement guards (OV-29)

*Consumed from ASTRA's [`title-member-notification-routing`](../../_experiments/evidence/title-member-notification-routing/README.md)
(SWE2-AUDIT-SPEC `_index/candidates/auditspec-review-astra-title-member-notification-0930/REVIEW.md`, ACCEPT) and
[`title-retirement-local-guards`](../../_experiments/evidence/title-retirement-local-guards/README.md)
(`_index/candidates/auditspec-review-astra-title-retirement-guards-0930/REVIEW.md`, ACCEPT); FABLE record
[`astra-returns-fable-0930`](../../_index/candidates/astra-returns-fable-0930/README.md). Static only.*

**Who sends a pending ticket's message 16.** `00393FF0` prepares its two requests through `002493D0` (call at
`00394029`) and `00249320` (`00394048`). Both call `00249210` (`002493DE`, `00249332`), which installs the queue
completion `002495C0` (`00249274`, the only instruction forming that address) with the member pointer's low 32 bits as
context, submits to the queue requester (`002492F3`) and increments the ticket's requested count `+0x18` (`002492F8`). Each
factory then installs its member callback at member `+0x10` (`002493D0`: `00249670`, with member `+0x18` from `0024A4E0`;
`00249320`: `00249660`). When a completion arrives, `002495C0` sign-extends the context, calls member `+0x10` first if it
is non-null (`002495E8`), increments the done count `+0x1A` (`002495ED`) and, when the ticket is sealed (bit 1), the counts
are equal and ticket `+4` is zero, loads the owner at `0024960B` and sends message 16 to it at **`00249632`**; it then
clears ticket bit 0 (`00249634`) and member bit 0 of `+0x20` (`00249637`). On the custom branch (ticket `+4` non-zero) it
calls ticket `+0x10` and skips the ticket bit-0 clear. The watcher route (factory `002491B0`, handler `00248700` ->
`002494F0`) is separate and does not replace this descriptor. So the synchronous `0024947D` (in `00249410`) and
`0024955D` (in `002494F0`) are not a complete set of senders: `00249632` is the ordinary later one, and a negative
observation needs that site, or an independently proved equivalent observer, with ticket, member and owner identity.
"Callback first" holds for a completion that arrives after the requester returns; one delivered inside the submit is outside
this route. The 32-bit context round trip is a premise, not tested.

**What message 18's `0024A680(+0xC8, 1)` gates on.** `0024A680` (141 B) returns on NULL; otherwise the address must equal
one of 64 fixed resource records `0208F580 + k*0x48` (k 0..63; the pool ends at the counter `02090780`), or it returns
before any effect. For a member it calls a tracking-tree helper first; if `+0x38 & 0x3F00 == 0x1400` and `+0x10` is non-null it
passes `+0x10` to `003697F0`; with a non-zero mode it passes `+0x18` to `003697F0`, which returns on NULL. It then clears
`+0x38` bit `0x20` (`0024A6F8`) and decrements `02090780` (`0024A6FC`). There is no local test of bit `0x20`, no access
to the ticket pool and no clear of `+0x10` or `+0x18`. So the gate is address membership, not "ticket pending" or
"already retired": a recognized record stays eligible after the clear, and a repeated normal call reaches the decrement
again. The completion tickets are a separate pool (`02090790`, 12 x `0x20`, allocator `00249580`). The counter's only
other reference is the record allocator `0024A4E0`'s increment (`0024A58A`).

**Still OV-29.** A ticket still pending at teardown, if observed, shows overlap; it does not by itself show cancellation
or draining. Nothing here asserts safe repeated teardown, idempotence, double-free or the absence of transitive effects.
That helper's tracking-tree effects (its chain is in the ASTRA packet), `003697F0`'s free effects, overall counter integrity, natural
pending teardown, post-teardown delivery, cancellation or drain, watchers made by services not read here, pointer reuse
and real IO outcomes all remain open. *(Narrowed 2026-10-02, FABLE: the tracking-tree branch is now read as far as a deferred queue and the queued callback - next subsection. Its native effects stay open.)*

### FABLE 2026-10-02: the tracking-tree branch of message 18 queues its release (OV-29)

*Consumed from seven ASTRA packets, each ACCEPTed by SWE2-AUDIT-SPEC with no narrowing that touches the facts used here: [`title-tracker-callback-boundary`](../../_experiments/evidence/title-tracker-callback-boundary/README.md) ([review](../../_index/candidates/auditspec-review-astra-title-tracker-callback-0930/REVIEW.md)) and its producer repair [`title-tracker-qualification`](../../_experiments/evidence/title-tracker-qualification/README.md) ([review](../../_index/candidates/auditspec-review-title-tracker-qualification-0930/REVIEW.md)), [`title-queue-consumption`](../../_experiments/evidence/title-queue-consumption/README.md) ([review](../../_index/candidates/auditspec-review-astra-title-queue-consumption-1001/REVIEW.md)), [`title-queue-pump-boundary`](../../_experiments/evidence/title-queue-pump-boundary/README.md) ([review](../../_index/candidates/auditspec-review-astra-title-queue-pump-boundary-1001/REVIEW.md)), [`title-cleanup-import-boundary`](../../_experiments/evidence/title-cleanup-import-boundary/README.md) ([review](../../_index/candidates/auditspec-review-astra-title-cleanup-import-1001/REVIEW.md)), [`title-cleanup-guard-and-annotation-prerequisite`](../../_experiments/evidence/title-cleanup-guard-and-annotation-prerequisite/README.md) ([review](../../_index/candidates/auditspec-review-astra-title-cleanup-guard-qualification-1001/REVIEW.md)) and [`title-cleanup-count-selector`](../../_experiments/evidence/title-cleanup-count-selector/README.md) ([review](../../_index/candidates/auditspec-review-astra-title-cleanup-count-selector-1001/REVIEW.md)). FABLE record [`astra-returns-title-fable-1002`](../../_index/candidates/astra-returns-title-fable-1002/README.md); its check re-reads every instruction below from the image (FAILS 0). Static only. Every statement assumes normal returns from the callees named and the state premises stated; none is an observed run.*

**From message 18 to the tracker.** For a recognized record, `0024A680` first calls `00181610`, which takes the tracking manager from `001B1C00` and tail-jumps to `001B1960` with the record. When the lookup in the manager's tree at `+0x2208` finds a node for the record's key, `001B1960` passes that node's `+0x28` value to `001FB660`; when it does not, it returns without that call. *(This link is FABLE's own read of the image, checked in the record. The packets retain these bodies; nobody has certified the key or the tree.)* `001FB660` (188 B: one root and two chained fragments) hands `value+0`, then `+0x28` of each node on its circular list, to `00183720`. It clears each field only after that call returns. It also hands a second list to `001AF2B0` and to an indirect `[+0x18]` call with size `0x30`, and finally resets `+0x20`, `+0x28` (byte), `+0x30` and its list sentinel. Its own instructions free nothing; what `0016D6D0`, `001AF2B0` and the indirect call do is not read here. *(FABLE, 2026-10-02, on ASTRA's `title-tracker-callback-boundary`, SPEC ACCEPT)*

**`00183720` queues; it does not release.** `00189120` takes no argument: it returns the shared global `01F7F598`. `00183720` returns at once for a NULL argument. Otherwise it reads that global twice, tests only the first read for NULL, and passes the second to `00185A90` with the callback `0017ECC0` and the original argument as data. `00185A90` appends the 16-byte pair {`0017ECC0`, argument} to the queue at `ctx+0xC38+32*ctx[+0xCB8]`. The index is sign-extended and not bounds-checked. On the fast arm it stores the advanced write cursor before it copies the pair, and calls nothing. When the cursor is at or past the end (unsigned) it hands off to `001858A0`. That helper grows the buffer (capacity 1 from a count of 0, otherwise doubled) through two allocator slots, `+0x10` and `+0x18`, and never calls the pair. So the tracker's local pointer clears happen while the release work is still waiting in the queue. *(FABLE, 2026-10-02, on ASTRA's `title-tracker-callback-boundary`, SPEC ACCEPT)*; growth *(FABLE, 2026-10-02, on ASTRA's `title-queue-consumption`, SPEC ACCEPT)*

**Who runs the queue.** `00186230` (125 B) first advances `ctx[+0xCB8]` to (old + 1) & 3. It then calls each pair in that bank, from its begin up to a snapshot of its write cursor, with the function at pair `+0` and RCX = the data at pair `+8`. Afterwards it re-reads the index and resets that bank's write cursor to its begin. The buffer is neither freed nor cleared. Two conditional cases follow from the code, not from any observed callback. An append to the same bank during the loop that does not grow the buffer can land past the snapshot, and the reset then drops it. A callback that changes the index moves the reset to another bank. *(FABLE, 2026-10-02, on ASTRA's `title-queue-consumption`, SPEC ACCEPT)*

Shipping code reaches it from the pump `0017D6E0`. When the DWORD at `01FD4A68` is zero, the pump calls `00189120` and passes the result to `00185C20`, a 5-byte jump to `00186230`. A non-zero value skips the flush. The pump's repeat edge (`0017D853` back to `0017D723`) re-enters after the flush site, so one pump invocation reaches the flush at most once. That count excludes nested reentry through the pump's callees. Four flushes are four pump entries with the gate at zero, not four frames. *(FABLE, 2026-10-02, on ASTRA's `title-queue-pump-boundary`, SPEC ACCEPT)*

**What the queued callback does with the data.** `0017ECC0` calls `005DE250` with the data pointer, then tail-jumps with the same pointer to `0019C590`. That is a 7-byte jump through the IAT slot `008C2B48`, which the PE import data binds to `free` in `api-ms-win-crt-heap-l1-1-0.dll`. The import name is not loaded-module identity. `005DE250` calls `0062BCB0` only when `00625F00` finds the DWORD at `+0xBC` non-zero, then tail-jumps to `00616C60`. `00616C60` calls `0062B100` and then `0062BCB0` with no `+0xBC` test. So on normal returns `0062BCB0` runs once when `+0xBC` is zero and twice when it is not. `0062BCB0` clears `+0xBC` after its first delegate. When `0062B870` returns non-zero it skips its record loop and returns that value, and neither caller tests it. `00616C60` calls `00584730` only when bit 31 of `+0x30` is clear, the low 31 bits exceed 1 and `+0x38` is non-NULL. On every normal branch it then zeroes `+0x38` and `+0x30` and tail-jumps to `005DE290`. *(FABLE, 2026-10-02, on ASTRA's `title-cleanup-import-boundary`, SPEC ACCEPT)*; guard scope *(FABLE, 2026-10-02, on ASTRA's `title-cleanup-guard-and-annotation-prerequisite`, SPEC ACCEPT)*

**A count precondition.** Let n be the low 31 bits of `+0x30`. `0062B100` walks the indices 0 .. max(1, n) - 1 and reads a DWORD at the address `00623DF0` returns: base + 0x58 * index + 0x38. The base is 0 for n = 0, the object's own `+0x38` for n = 1, and the pointer stored at `+0x38` for n > 1, so the selector returns a record's `+0x38` field, not a record base. While that DWORD is positive it calls `005CCB80` with ECX = 1 and reads it again; the service gets no record pointer. With n = 0 the first read is at the absolute address 0x38, and nothing normalizes or skips that state first. That is a precondition on valid state, not an observed crash. No constructor or count writer has been read to show that n >= 1 holds when cleanup gets here. *(FABLE, 2026-10-02, on ASTRA's `title-cleanup-count-selector`, SPEC ACCEPT)*

**The evidence readers were qualified, not the facts.** The tracker packet's first checker accepted a self-consistent fake call on the fast arm. ASTRA's repaired `-02` checker derives the CFG itself and refuses it. The guard packet adds an annotation-agreement prerequisite, which found no disagreement in the inputs of the tracker, queue, pump and import packets. Neither repair changes a fact above. *(FABLE, 2026-10-02, on ASTRA's `title-tracker-qualification`, SPEC ACCEPT)*; *(FABLE, 2026-10-02, on ASTRA's `title-cleanup-guard-and-annotation-prerequisite`, SPEC ACCEPT)*

**Still OV-29.** Message 18's tracking-tree branch is now known to defer its release to this queue. What is not known: when the flush runs relative to title teardown, the value of `01FD4A68` in a real session, and whether the shared context, its index and the queue storage stay valid in between. Also still open: thread and frame placement, cancellation of queued pairs, idempotence, heap validity, and whole-object lifetime. The effects of `001858A0`'s allocator slots, `005CCB80`, `0062B870`, `00584730`, `005DE290`, `001AF2B0`, `0016D6D0` and the indirect calls are also unread. The next static step is a constructor or count writer that proves n >= 1 at `0062B100`, or a valid zero-count skip.

## 4. The consumer reads the dependency, then passes a value onward

The consumer's message-2 arm first checks its own build-state bit. If initialization is still
needed, it loads the asset pointer from `02AEE4C0` into RDX and rejects null or clear low readiness
bit. Only then does `00393AA5` load **asset+0xD0**. It passes that loaded value, the consumer
receiver, and selector 5 into `003946B0`.

The fixed-offset diagnostic and native controls deliberately disagree between the consumer's
own +0xC0 and the asset's +0xC0. The original gate uses the latter. A status value 0x100 does not
satisfy the low-bit test merely by being nonzero.

The positive native case stops exactly at the layout call and checks the three passed arguments.
It does **not** run the subsequent child-tree construction, rendering, or full message-2 body.

## 5. Raw initialization is not a pointer-returning API

`002465F0` mutates its receiver but does not restore RAX to it. The final scheduler predicates leave
0 or 1 in the tested paths. The in-place wrapper `00245000` and allocating wrapper `00244F50`
separately restore the receiver in RAX. The raw function therefore cannot be given the same
object-pointer return guarantee as those wrappers.

Bulk zeroing also precedes header writes and the message-1 handler. Calling it “zero at
construction” must not imply that every byte still equals zero when construction completes.
In this object, message 1 writes resource pointers and may receive immediate readiness notification.

## 6. Validation and scope

The delivered fixture contains 65 original-instruction assertions, a repeat run and six private-image
code mutants. It retains original constructor, allocator, handler, ticket, readiness, bitset,
selected resource-release, default and stack-cookie instructions. Seven application service
boundaries and the imported memset target are explicitly substituted. Results do not certify
those substituted services, real IO, the manager tree, heap/free behavior, or a live game session.

The bounded receiver diagnostic separately checks five complete contiguous bodies with verified
boundaries and an explicit verified jump table. Sixteen synthetic regression cases and five
analyzer mutants cover flag-only operations, 32-bit/partial writes, ABI clobbers, conflicting
joins, pointee separation and LEA classification. These are instrument checks, not more game
experiments or whole-game proof of absence.

## 7. Open questions

- [ ] **OV-29.** Validate actual asset IO/callback timing and cancellation/lifetime behavior in the installed game; equal-counter fixtures are not that observation. *Narrowed 2026-09-30 (FABLE, [record](../../_index/candidates/astra-returns-fable-0930/README.md)): the ordinary later message-16 sender is `00249632`, and message 18's `0024A680` gates on record address membership only (section 3, FABLE 2026-09-30 subsection). Still OPEN.* *Narrowed 2026-10-02 (FABLE, [record](../../_index/candidates/astra-returns-title-fable-1002/README.md), SPEC ACCEPT on seven ASTRA packets): message 18's tracking-tree branch (`0024A680` -> `00181610` -> `001B1960` -> `001FB660`) queues `0017ECC0` callbacks through `00183720` instead of releasing them at once. The shipping flush is `00186230`, reached from `0017D6E0` when `01FD4A68` is zero, and the callback ends in the CRT `free` import (section 3, FABLE 2026-10-02 subsection). When the flush runs relative to teardown is not observed. Still OPEN.*
- [x] ~~Repair and independently test the missing upstream receiver-census producer, then revalidate other affected declarations before claiming family-wide soundness.~~ *NOT A QUESTION 2026-09-29 (SWE2-FRONTIER) under the class-2 ruling: an independent-acceptance/process item, carried by board task FABLE-CARRIER-TOOLING-AND-CHECKER-PROPOSALS-0926. Register OV-30.*
- [x] ~~Complete remaining concrete field/representation obligations and common-header integration for this type without conflating physical evidence with meaning.~~ *ANSWERED 2026-09-29 (SWE2-STRUCT), section 8: every field's receiver, width, both ends, allocation class and the common release chain are recorded in `_types`; named residue: +0xC4 unread (bounded, positive control passes), parent-root release and deferral applicability, real IO timing (OV-29). Earlier: NOT A QUESTION 2026-09-29 (SWE2-FRONTIER) under the class-2 ruling, carried by board task FRONTIER-REQ-SWE2-STRUCT-OV31-TYPE-STORE. Register OV-31.*
- [x] ~~Independently review this section and decide the appropriate type/system readiness; local production does not self-award L2 or terminal acceptance.~~ *NOT A QUESTION 2026-09-29 (SWE2-FRONTIER) under the class-2 ruling: an independent-acceptance/process item, carried by board task FABLE-CARRIER-SECTION-OVERLAY-ACCEPTANCE-0929. Register OV-32.*

*Restored by the owner (OPUS, 2026-09-25) - EXP-189's paragraph, dropped by the SECTION-04 overlay; re-read.*

`00249320` (43 B) is the class-3 node factory ~~the title-asset consumer calls~~ **the title asset's own request body `00393FF0` calls (`00394048`, the `+0xD0` request), reached only from the asset's handler; the `0x1D0` consumer `003939B0` does not call it (`CON-202`, 2026-09-29, OPUS)**: `00249210(rcx, rdx, r8, 3, 0)` builds the node, `00249660` installs at `qword[+0x10]` as its dispatch slot, and `qword[+8]` returns - the fixed-vtable-3 create.

Interior anchor `00249337` (function `00249320`).

## 8. Type-store integration, OV-31 (SWE2-STRUCT, 2026-09-29)

This section records the type-store work for the 0xD8 asset (`WidgetSingleton02AEE4C0` in `_types`).
Each representation fact below comes from an instruction. Meaning is stated separately and only where
a consumer establishes it. Checks: [`ov31_title_asset.py`](../../_index/candidates/ov31-title-asset-type-store-0929/ov31_title_asset.py)
(`S` exact instructions, `P` .pdata chain roots, `J` jump-table arm, `X` cell references, `C`/`O`
receiver census, `K` positive control); record [`README.md`](../../_index/candidates/ov31-title-asset-type-store-0929/README.md).

**Receiver and extent.** The receiver is direct: the object pointer is held in the cell `02AEE4C0`
and passed in RCX to its own handler. The extent is fixed at `0xD8`, set by `0039449F`. `+0x00`..`+0xBF` is the
embedded common widget header (OPUS, 2026-09-27). From this type's side, every access below `+0xC0`
reached from the cell or the own handler is in common widget code: the `00244F00` destroy chain, and the
attach entry `00244960`. The type area `+0xC0`..`+0xD7` is fully declared. A census widened to
`0x1000` finds no type-specific access at or beyond `+0xD8`.

| Offset | Width proof | Writers | Readers | Meaning evidence |
|---|---|---|---|---|
| `+0xC0` u32 | `003940FC` mov dword, `003940E3` or dword; reads `00393A98` byte test, `0039450D` dword | memset, `003940FC` (0), `003940E3` (bit 0) | `00393A98` (consumer gate), `0039450D` (`00394500`) | script verb `fsttl_initialize` polls `00394500` through `00511EC0` and holds until bit 0 is set. Bit 0 means the resources are ready. No enumerated path writes or reads bits 1-31. |
| `+0xC4` u8[4] | none | memset only | none on any enumerated path | none. It sits in the alignment position before a pointer, which is a reading, not proof. |
| `+0xC8` ptr | `00394033`, `00394097` QWORD | `00394033` | `00394097` only | resource-entry result, passed to `0024A680(ptr, 1)` on message 18 |
| `+0xD0` ptr | `00394050`, `003940A8`, `003940B9`, `00393AA5` QWORD | `00394050`, `003940B9` (clear) | `003940A8`, `00393AA5` | loaded block that the consumer passes to `003946B0` |

**Enumerated receiver paths.** The zeros above apply only to these paths:

- all nine references to `02AEE4C0`, found by an image-base-aware scan whose control `02AEE4D0` passes;
- the cell-seeded fixpoint, which reaches 13 functions and converges;
- the own-handler seed `00394070`, run with argument registers, which reaches 4 functions and converges;
- the load batch's three owner-notify sites. The batch records `self` at `+8` (`002495B7`), and the
  notify sites read only the handler slot at `+0x00`.

The `+0xC4` zero has a positive control: the same tool on the sibling cell `02AEE4C8` does see
`+0xC4` accesses.

**Allocation is pool-or-heap, not heap.** `0xD8` is at most `0x120`, so `00244F50` takes the first
free slot of the 112-slot pool. It falls back to `002497B0` only when every slot is busy
(`00244FB2`). The store's class is now `MIXED`.

**Release is external and common.** The asset never destroys itself. Two sites pass it to the widget
destroy `00244F00`:

- `00394400` is called only from the message-18 arm of the `0x5A0` widget handler `00582860`
  (`00582EB5`, behind the nonnull predicate `00394520` and the `+0xC4` bit-`0x10` gate
  `00582E81` / `je 00582EBF` on that widget's byte);
- the `0xF0` sibling's handler `00394130` does so in its own message-18 arm (`00394161`).

The common chain then delivers message 18 to this type's cleanup arm at `0024505A`. After that,
`002482E0` returns the slot to the pool or frees it. A release site is not an ownership proof.

**The script-facing consumer.** Script verb 7055 `fsttl_initialize` has two handlers. Its begin
`00511EA0` runs the creator. Its poll `00511EC0` returns the running flag while `00394500` is zero.
So a script waits for bit 0 of `+0xC0`. That bit has one writer, the own handler's
message-16 arm (`003940E3`). On the enumerated paths, message 16 comes from the load batch's
owner-notify sites (`00249456`, `0024953B`, `0024960B`). A message-16 sender reaching the
asset through the UI-root child link is not excluded (the bound of residue 1).

**Residue, named rather than smoothed:**

1. `+0xC4` has no reader on any enumerated path. An access through the UI-root child link that
   `00248220` makes at attach time is not excluded, because those generic walkers were not read one by one.
2. Release through a teardown of the parent root `*(0208EA28)` is not established.
3. Whether the asset ever takes `00244F00`'s deferred branch, or `00245020`'s `+0x40` bit `0x20`
   deferral, is not established. `00248271` copies that bit from the parent at attach time. *(Narrowed 2026-10-01, OPUS, on ASTRA's title-root-retirement, ACCEPTed: the `00245020` deferral applies after a successful, valid, unchanged root initialization, because the root handler `002445D0` sets the bit and attachment copies it - see the OPUS 2026-10-01 subsection below. `00244F00`'s deferred branch is not settled by it.)*
4. Real IO timing and lifetime remain OV-29.
5. Type readiness is left for independent acceptance (OV-32).

### OPUS 2026-10-01: root retention applies to the title asset, and the owner window has no revocation (OV-29)

*Consumed from ASTRA's [`title-root-retirement`](../../_experiments/evidence/title-root-retirement/README.md) (SWE2-AUDIT-SPEC [review](../../_index/candidates/auditspec-review-title-root-retirement-1001/REVIEW.md), ACCEPT, no narrowing); OPUS re-read `002445D8`, `0024826B`-`00248271` and `00245072`-`0024509B` at the bytes. Static only, and every claim below is conditional on the premises named.*

**The title asset inherits root retention.** The title initializer `00393FF0` starts its two requests, then loads the root `*(0208EA28)` (`00394117`) and attaches the asset under it (`00244960` -> `00248220`). The roots `0208EA20` / `0208EA28` / `0208EA30` are made by `00247AE0`, and their message-1 handler `002445D0` sets `0x23` in `+0x40` (`002445D8`). Attachment copies the parent's bit `0x20` into the child (`0024826B` tests it, `00248271` sets it). So after a successful, valid, unchanged root initialization the asset carries bit `0x20`. Teardown `00245020` broadcasts message 18 and then re-reads that bit (`00245072`). Set: it calls `002473F0(self, 0)`, clears bit 1 and sets bit `0x10`, and keeps the storage. Clear: it tail-calls the physical release `002482E0`. Message and helper side effects are premises, and root membership at attach is not lifetime for good.

**No local revocation in the owner window.** After its ordinary gates (sealed, counts equal, ticket `+4` zero), `002495C0` reads the raw owner at ticket `+8` and that owner's current handler at owner `+0`, rejects NULL for each, and sends message 16. It reads no owner flags `+0x40`, no generation and no publication `02AEE4C0`. The title's message-16 handler `00394070` simply sets ready bit 0 at `+0xC0`. So a completion that arrives after a retained teardown, with the handler unchanged and the gates satisfied, writes the ready bit despite bit `0x10` and the cleared publication. That is a source witness under those conditions, not an observed late delivery.

**Physical release.** `002482E0` nulls the handler before it disposes the storage, so a still-backed, unreused pool slot suppresses the notification. NULL is not a lasting identity token: a released slot can be selected by `00244F50` and reinitialized by `002465F0` with a new handler. Whether a ticket survives into reuse (ABA), external cancellation or drain, heap validity and natural pending teardown all stay open (OV-29).

## Cross-subsystem neighbours — SWE2-EC7 (pass-22 dispositions)

- **Audio - SERVICE (3 edges).** `003939B0` reaches bodies filed to audio: `00229AB0`, `002DEC00`, `002DEE50` - shared machinery across the layer boundary, no shared ownership.
- **CoreRuntimeScheduling - SERVICE (2 edges).** `002465F0`, `003939B0` reach bodies filed to core runtime: `001EDDA0`, `001EDE70` - shared machinery across the layer boundary, no shared ownership.
- **Gameplay - SERVICE (1 edge).** `00394460` reaches bodies filed to Gameplay: `00237DF0` (Combat) - shared machinery across the layer boundary, no shared ownership.
- **Input - CLIENT and SERVICE (4 edges).** `0024A680` is also called by bodies filed to input: `00291D90` (UI); `003939B0`, `00394460` reach bodies filed to input: `001E0C10`, `001E0FB0`, `002501E0` - shared machinery across the layer boundary, no shared ownership.
- **Presentation - CLIENT (4 edges).** `00249410`, `00249580` are also called by bodies filed to presentation: `002B7B80` (UI), `002BAF80` (UI) - shared machinery across the layer boundary, no shared ownership.
- **SaveLoad - CLIENT (3 edges).** `00249210`, `00249410`, `00249580` are also called by bodies filed to SaveLoad (save/load settings): `00582790` (AssetMaterializationSupport) - shared machinery across the layer boundary, no shared ownership.
- **Save_Load_Settings - CLIENT (1 edge).** `003946B0` is also called by bodies filed to save/load/settings: `00582860` - shared machinery across the layer boundary, no shared ownership.
- **Script_VM_Native_Bridge - CLIENT (2 edges).** `00394460`, `00394530` are also called by bodies filed to script VM / native bridge: `00511EA0`, `00511F90` - shared machinery across the layer boundary, no shared ownership.
- **World - CLIENT (1 edge).** `0024A680` is also called by bodies filed to World: `003C63A0` (Navigation) - shared machinery across the layer boundary, no shared ownership.
- **Developer - SERVICE (1 edge).** The pump `0017D6E0`, cited by FABLE's 2026-10-02 subsection for the queue flush, also calls `001C2F50`, filed to the developer map-index auto-test runtime - another duty of the same pump, shared machinery across the layer boundary, no shared ownership with the title asset. *(FABLE, 2026-10-02)*
- **Platform - CLIENT and SERVICE (4 edges).** `001B1960`, the tree-node dispatch through which message 18 reaches the tracker (FABLE's 2026-10-02 subsection), is filed to Windows native support. It is reached from `00181610`, and it calls `0016D6D0` and `001FB660`; `0016D6D0` is also called by `0019CC50` (Windows native support) - shared machinery across the layer boundary, no shared ownership. *(FABLE, 2026-10-02)*

## Falsification pass 1 — 2026-09-29 (OPUS): the chain survives; one caller was misnamed

**Attack.** Every section's checkable clause was turned into a check at its instructions: §1's two factories, §2's
consumer arm, §3's asset handler, request body and ticket, §4's gate and §5's return registers. The consumer's messages
are read through its own jump table (`00393E48`, rebased on the image base), not assumed. Callers come from a raw
`E8`/`E9` index over the whole of `.text`. Script: `Tools/analysis-kit/gfz-scripts/falsify_title_asset.py`, output
`falsify_title_asset.out`, image `73461d08…`, 0 BROKEN, exit 0. The script asserts the corrected statement. §8
(SWE2-STRUCT's OV-31 checks) and the native fixtures are carried, not re-run.

| # | Clause attacked | Result |
|---|---|---|
| A0 | sizes | **survives**: all nine bodies |
| A1 | §1: the two factories | **survives**. The asset factory makes five calls and one byte store before its guard at `0039448B`, as §1 warns. It then allocates `0xD8` with handler `00394070` through `00244F50`. The consumer factory exits unless `02AEE4C0` is non-null, handles an existing `02AEE4C8`, and otherwise allocates `0x1D0` with `003939B0` |
| A2 | §2: the consumer's message-1 arm | **survives**. Jump-table entry 1 is `003939F7`: the message byte goes to the consumer's `+0xC0`, `+0xC4`/`+0xC8` are zeroed, `02AEE4C8` is published, and `002E1C20(1, 21)` runs |
| A3 | §3: the asset's own handler | **survives**. Message 1 publishes, zeroes `+0xC0`, requests and sets channel 0 bit 21. Message 16 ORs bit 0. Message 18 releases in the stated order, with no compare against the slot and no write to `+0xC8` or `+0xC0` |
| A4 | §3: the two requests | **survives**: `(ticket, 7, 0x3D, 3, descriptor, 2)` to `+0xC8` (the returned record's `+0x40` is zeroed), `(ticket, 7, 0x3A)` to `+0xD0`, then the submit |
| A5 | §3: publication before readiness | **survives**. The submit notifies only when words `+0x18` and `+0x1A` are equal and `+4` is 0; it sends message `0x10` to the owner the ticket recorded at `+8` |
| A6 | §4: the consumer's gate | **survives**. Entry 2 is `00393A7A`. It tests the consumer's own `+0xC4` bit 0, then bit 0 of the asset's `+0xC0`, and passes the asset's `+0xD0` to `003946B0` with 5 |
| A7 | §5: the return registers | **survives**. Both wrappers put the receiver back in `rax`. `002465F0` keeps it in `rdi` and returns its predicate |
| A8 | §7's restored note: "`00249320` … the title-asset **consumer** calls" | **broken** (`CON-202`). The node factory reads as stated. But the title asset's call is `00394048`, in the asset's own request body `00393FF0`, which is reached only from the asset's handler (`00394106`). The `0x1D0` consumer `003939B0` makes no direct call to it. `00249320`'s four callers are `003933F0`, `00393FF0`, `003F4840` and `00404060` |

**What the player sees.** Nothing changes on screen. The note named the wrong one of the page's two widgets as the one
that loads the title's menu package (`title.mrp`, per the VBF page). On a page whose whole point is keeping those two
widgets apart, that matters.

*Not claimed:* anything about `00249580` when all twelve of its ticket slots are busy (it then returns 0, and
`00393FF0` does not test for that). It is outside every clause above and is recorded here as an observation only.
