---
contract: allocate, promote, retire and release the 160 character render records through one image-lifetime pool
category: 17-Presentation-Rendering
scope: family
readiness: BEHAVIORALLY UNDERSTOOD
confidence: PROVEN
implements: 17-Presentation-Rendering/Character-Render-Records/the-character-render-record-array.md
entries: ["004269A0", "004278E0", "004279B0", "00428710", "00427C90", "00429140"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-14 (OPUS) - 142 addresses cited - 3 data, 40 entry, 99 interior, every one resolving
    into a known section of the authority image. **This records a check performed on
    that date, NOT the method of the original derivation**, which this block never
    carried; see this document's own Evidence section and `audit.last_pass_state`
    for that.
last_reviewed: 2026-09-11
audit:
  passes: 1                    # falsification passes survived. 0 = NOT yet fact.
  last_pass: 2026-09-12        # YYYY-MM-DD
  last_pass_state: opus-render-pool-pass-1   # snapshot SHA the pass ran against
  crossref_clean: true         # audit_crossrefs.py reports nothing for this document
  reopened_count: 0
---

# Contract — the character render record pool lifecycle

One allocation of `0x48930` bytes made at `003325E7` holds 160 `CharacterRenderRecord`s of `0x740`
bytes followed by a `0x130`-byte control block, `CharacterRenderSystemTail`. The pointer lives at
`0x022C6F28`; every operation below begins by loading it. Nothing is ever freed, so this contract is
about **slot state, not memory**: a record is allocated by being taken off a free cursor and released
by being unlinked and marked free in place.

Five operations share the block, and none of them is a method on a record — they are free functions
that reach the pool through the global. That is the reason a contract is the right shape for this:
the invariants live between the functions, not inside any of them.

## 1. Purpose

To give a caller a record addressed by a **name**, to make that record visible to the render walk
only after a promotion step, and to reclaim it when it is flagged — while keeping four indices
(`headActive`, `tailActive`, `headPending`, `tailPending`), a free cursor and a live count mutually
consistent across five functions that never call one another.

## 2. Interface

| operation | entry | parameters | returns |
|---|---|---|---|
| construct | `004269A0` | none | none |
| look up by name | `004278E0` | `rcx` = NUL-terminated name | `ax` = record index, or `-1` |
| allocate | `004279B0` | `rcx` = name, `rdx`/`r8` = two 32-byte buffers, `r9d` + stack = flags | `rax` = record pointer, or `0` |
| promote pending → active | `00428710` | none used from the pool | none |
| retire flagged actives | `00427C90` | none | none |
| release a record | `00429140` | `rcx` = record pointer | `eax` = 0 on a null argument, **1 on every other input**, which is not a free-slot certificate: a 1 can mean a deferred mark, a no-op or a direct unlink and clear *(qualified 2026-10-02, OPUS: render-removal-phase-contracts, accepted)* |

Microsoft x64 throughout. The two failure returns of `allocate` are both `xor eax, eax` and are
**indistinguishable to the caller** — see §10.

## 3. Types

`CharacterRenderSystemTail` at `*(char**)0x022C6F28 + 0x48800`, and the 160 `CharacterRenderRecord`s
that precede it at stride `0x740`.

**The two link widths differ, and every crossing between them is deliberate.** The pool's four
indices are 32-bit and hold `-1` for *none*:

| field | offset in tail | width |
|---|---|---|
| `headActiveIndex` | `+0x00` | 4 |
| `tailActiveIndex` | `+0x04` | 4 |
| `nextFreeIndex` | `+0x08` | 4 |
| `liveCount` | `+0x0C` | 4 |
| `headPendingIndex` | `+0x10` | 4 |
| `tailPendingIndex` | `+0x14` | 4 |

The record's own links are 16-bit and hold `-1` for *none*: `id` at `+0x00`, `prevIndex` at `+0x02`,
`nextActiveIndex` at `+0x04`. So a head is written from a link with `movsx` (`0042880B`, `00428820`,
`00427D29`, `00427D3E`, `0042925E`, `00429273`) and a link is written from a head with `movzx`
(`00427A3C`→`00427A43`, `00428853`→`0042885A`).

**The `movzx` direction truncates `0xFFFFFFFF` to `0xFFFF`, and that is correct rather than lucky.**
A 32-bit `-1` narrowed to 16 bits is the 16-bit `-1`, which is exactly the sentinel the link field
uses; a reconstruction that widened the record links to 32 bits without widening the sentinel
comparisons, or that made either side unsigned, would break this. The widths are part of the
contract, not an implementation detail.

There is a **third index of a different width again**: `+0x2C` is 16-bit with an `0xFFFF` sentinel,
scaled by `0x740` and added to the pool base at `0042E954`–`0042E973`. It is not one of the six
above ~~and no lifecycle operation here touches it~~; construct stores `0xFFFF` in it (section 7) and no other lifecycle operation here touches it *(corrected 2026-10-02, OPUS: `004269A0`+0x66 `mov word ptr [rsi + 0x4882c], ax` with `eax` = -1)*.

## 4. Preconditions · postconditions · invariants

**Preconditions.** The pool pointer at `0x022C6F28` is non-null and the constructor has run. No
operation validates this; `004269A0` is the only writer of the initial state.

**Invariants**, each maintained by more than one function and therefore genuinely shared:

1. `headActiveIndex == -1` if and only if the active list is empty, and likewise for pending. Both
   emptiness tests are written as `cmp dword ptr [...], -1` (`00427A18`, `0042882A`).
2. `0 <= liveCount <= 160`. The ceiling is enforced only at `004279E9`, **before** the increment, so
   the pool holds exactly 160 records and the 161st allocation is refused *(qualified 2026-10-02, OPUS: the signed gate bounds the count and nothing else - the starting cursor is read signed at `004279B0`+0x4A with no range check before the clear it addresses, and neither remover tests the count before its decrement, so the lower bound is not enforced: a count of 0 would become -1, an arithmetic case and not an observed one; render-slot-identity-publication and render-removal-phase-contracts, accepted)*.
3. `liveCount == 0` implies `nextFreeIndex == 0`. This is enforced identically and independently in
   the two release paths — `00427D48`/`00427D50` and `0042927D`/`00429288` — and in the constructor.
   It is the only invariant in this contract that is asserted in two places at once, which is what
   makes it a real invariant rather than an incidental assignment.
4. `liveCount` counts records on **either** list. Promotion moves a record between lists and does not
   touch it (`00428710` has no access at `+0x0C`).
5. A record whose state word `+0x284` is `0` is free. The free-cursor advance scans for exactly that
   (`00427AD2`) and the record initializer sets it non-zero (`0042049A`) *(qualified 2026-10-02, OPUS: "free" is the scan's predicate, not an ownership certificate - a count below 160 does not by itself imply that any row has a zero `+0x284`, and nothing checks the count against the 160 flags; render-slot-identity-publication, accepted)*.

**And the advance has NO ITERATION BOUND**, which makes the three facts above load-bearing together
rather than separately. `00427AB0`–`00427ADA` increments the cursor, wraps it at 160 and re-tests
`+0x284`, with nothing counting the trips. It terminates because **invariant 2 guarantees a free slot
exists** — the ceiling refuses the 161st allocation *before* the increment at `00427A7F` — and
because **every release really does clear `+0x284`**: `0041F730` opens with `memset(record, 0, 0x740)`
at `0041F754`, the whole record *(qualified 2026-10-02, OPUS: both legs are conditional. The cap yields a zero `+0x284` only while the count agrees with the flags - the accepted countermodel, count 0 with every flag non-zero, passes the cap and the scan then never meets a zero, a mathematical case and not an observed hang - and the scan stops within 160 visits only under stable readable flags with at least one zero. Nor is the memset the clear's last write: 125 direct writes and six calls into four helpers follow it, their composed footprints stay inside the record and miss `+0x0` and `+0x284`, and so the clear returns with id -1 and `+0x284` 0 under its premises - a valid writable record, a private frame, readable constant inputs, normal returns, a fill confined to its span, ABI preservation and no interference; render-slot-identity-publication and render-clear-callee-footprints, accepted)*.

> **Both release paths reach that memset, but only one of them directly.** `00429140` calls
> `0041F730` at `00429291`. `00427C90` does **not call it at all** — it calls
> `004200A0 CharacterRenderRecord_TeardownAndReset` at `00427DAE`, which calls `0041F730` in turn *(qualified 2026-10-02, OPUS: as a tail jump at `004200A0`+0x146, after `004200A0`'s fifteen calls; `00429140`'s direct arm makes no `004200A0` call, so that cleanup does not run on it - render-removal-phase-contracts, accepted)*.
> §7's wording reads as though the release path calls the reset itself; for that path it is one
> level deeper. *(Added 2026-09-12 by the falsification pass below, which went looking for a release
> that decremented `liveCount` without resetting the record — the one thing that would make this
> loop spin forever — and did not find one.)*

**Postconditions** are listed per operation in §7.

## 5. State

All state is in the tail block. `+0x18` is a 32-bit flag word; bit 5 is set by promotion
(`00428863`) **and by retirement (`00427DB3`)**, and bit 0 is cleared and then restored around one
promotion callee (`00428790`-`004287B7`), so a caller's bit 0 survives a promotion whatever that
callee does to it. What the bits mean is not established here.

**Corrected 2026-09-12 by execution.** This section said no lifecycle operation reads or writes the
tuning fields at `+0x1C`, `+0x20`, `+0x24`, `+0x28`, `+0x40` and `+0x4C..+0x70`. **`+0x28` is read by
promotion** at `0042876A` and copied into every promoted record's `+0x414` at `00428773`. The rest of
that list stands~~: written only by the constructor and by the reset helper `0042ED30`.~~: written by the constructor and by the reset helper `0042ED30`, and `+0x1C` also by the keyed setter `002EBC30` *(corrected 2026-10-02, OPUS: `002EBC30`+0x7 `movss dword ptr [rax + 0x4881c], xmm0`, reached from `0026C8C0`+0x4F9)*.

## 6. Relationships

- **Consumer:** ~~`CONTRACT-character-transform-publish` operates on records reached by walking the~~
  ~~active list from `+0x00`. It sees a record only after `00428710` has promoted it, which is the~~
  ~~ordering guarantee this contract exists to state.~~ not `CONTRACT-character-transform-publish`, which reads no record of this pool *(corrected 2026-10-02, OPUS: `001FB120`+0x2A `imul rdi, rax, 0x318` and `001FB120`+0x3C `add rdi, qword ptr [rcx + 0x58]` index the render object's own `0x318`-stride array; `001FB120` never reads `022C6F28`)*.
- **Consumer:** `CONTRACT-coast-down-latch` addresses a record by id and tests `record[+0x06] == -1`.
  It does not consult the pool.
- **Producer:** `00420480`, the record initializer called by `allocate` with the record and the two
  caller buffers, fills the record and marks it in use.

## 7. State transitions

**Construct — `004269A0`.** Calls the per-record clear `0041F730` on all 160 records, then writes,
in this order: `headActive = -1`, `tailActive = -1`, one 8-byte store putting `0` into both
`nextFreeIndex` and `liveCount`, `headPending = -1`, `tailPending = -1`, flag word `= 0` *(corrected 2026-10-02, OPUS: not its final value - `004269A0`+0x2B9 `or dword ptr [rax + 0x48818], 5` runs at the end of the constructor, so a constructed pool's flag word is 5)*, `+0x2C`
`= 0xFFFF`. The tuning block follows. **The 8-byte store at `004269ED` covers two 4-byte fields and
is not evidence that they are one field** — they are read separately at 4 bytes everywhere else *(qualified 2026-10-02, OPUS: each per-record clear is a memset followed by the clear's own sentinel and default stores, so a constructed row is not all-zero - `+0x0` ends at -1, and no direct store or helper footprint after the memset touches `+0x284`; render-slot-identity-publication with FABLE's narrowing and render-clear-callee-footprints, accepted)*.

**Look up — `004278E0`.** Walks the active list from `headActive`, skipping any record whose
`+0x290` has bit 1 set, and byte-compares the caller's name against the record's name at `+0x1C`
until a NUL. On no match it walks the pending list — **and the pending walk has no such skip.**

**Corrected 2026-09-12 by execution.** This paragraph said the pending list is walked "the same
way". The loop at `00427952` tests nothing at `+0x290`: a record marked for retirement is invisible
to the active walk and **visible** to the pending one. The asymmetry is not decorative — it decides
whether a name can be re-allocated while its old record is waiting to be retired, and the answer is
different depending on which list that record is on. A reconstruction that hoisted the test out of
the first loop to cover both, which is the obvious tidy, changes 370 of this suite's 492 lines *(scope named 2026-10-02, OPUS: the suite's first generation; the current 525-command suite compares 581 lines - re-run 2026-10-02, 0 mismatches - and the same control changes 460 of 583, §13)*.

A hit returns `movzx eax, r10w` — the index zero-extended from 16 bits — and a miss `or eax, -1`.
The one caller compares `ax` alone (`004279DC`), so only 16 bits of the answer are ever read.

**Allocate — `004279B0`.**

1. `call 004278E0(name)`; if it returns anything but `-1`, **return 0**. Allocation is keyed by
   name and a duplicate is refused rather than replaced.
2. If `liveCount >= 160`, **return 0**.
3. `index = nextFreeIndex`; `record = pool + index * 0x740`; `call 0041F730(record)` clears it *(qualified 2026-10-02, OPUS: the cursor is read signed at `004279B0`+0x4A and nothing compares it before this clear, so the step is in range only under the precondition 0 <= nextFreeIndex <= 159, which the count gate in step 2 does not supply; render-slot-identity-publication, accepted)*.
4. Link at the **tail of the pending list**: if `headPending == -1` then `headPending = index`,
   else the old tail's `nextActiveIndex` takes `index` and this record's `prevIndex` takes the old
   tail. Then `tailPending = index` and `record.id = index` *(qualified 2026-10-02, OPUS: in that order - the list writes precede the self-index WORD store at `004279B0`+0x9D, so the id is not the slot's first publication; the id store does precede `00420480`'s first OR of `0x2010F9` into `+0x284` (`00420480`+0x1A, step 5) and the count increment (step 6). These are separate stores, not one atomic publication; render-slot-identity-publication with FABLE's narrowing, accepted)*.
5. `call 0020E600(encodedRootPointer)` with the tail's `+0x30` in `ecx`, and pass its result as
   the fifth argument of `call 00420480(record, buf1, buf2, ...)`.
6. **Set bit 0 of the record's own `+0x290`** (`00427A76`), which promotion later clears — see
   below. Then `liveCount++` (`00427A7F`).
7. Advance the free cursor: if `liveCount >= 160` set `nextFreeIndex = 0` and stop; otherwise
   increment `nextFreeIndex`, wrapping to `0` at 160, until the record it names has `+0x284 == 0` *(qualified 2026-10-02, OPUS: from a start in 0..159 every visited index stays in 0..159 and one full cycle is 160 visits; the loop stops within 160 only if the flags are stable and readable and at least one is zero, which the count does not prove; render-slot-identity-publication, accepted)*.
8. Return the record.

**The record is on the PENDING list when allocate returns.** Nothing that walks the active list can
see it yet.

**Allocate writes two links, not four.** It never stores `-1` into this record's `nextActiveIndex`,
and in the empty-list case it never stores one into `prevIndex` either: both arrive as `-1` from the
reset at step 3, which writes six 16-bit links at `0041F771`-`0041F795`. The sentinel on a fresh
record is therefore the RESET's postcondition, not allocate's, and a reconstruction whose reset does
not write them builds a list that walks into record 0.

**Promote — `00428710`.** For each record on the pending list, in list order — and the successor is
read into `r15d` at `00428760`, **before** any of this, so the walk survives the re-linking:

1. `call 0041FCF0(record)`.
2. Copy the tail's `+0x28` into the record's `+0x414` (`0042876A`-`00428773`).
3. `call 003E68E0(record)`; **if it answers non-zero**, `record[+0x114] = 003B56D0(record.id)`.
   The record's id is passed sign-extended from 16 bits (`00428782`).
4. Clear bit 0 of the tail's flag word, `call 0042C410(record, pool)` (interior read 2026-09-17, SWE2-FRONTIER: `003E7D10` first at [`0042C46A`](../_index/ADDRESS-INDEX.md), `003B0C30` next), then put bit 0 back to what
   it was — as an xor of the difference (`004287AC`-`004287B7`), not a plain restore, so whatever
   the callee did to that bit is undone and any other bit it touched is kept.
5. Clear **bit 0** of the record's `+0x290` (`004287BD`) — the bit allocate set. After a promotion
   that bit means "allocated and never promoted", which is exactly the state release's second path
   acts on.
6. Unlink from pending (fixing `headPending`/`tailPending` when the record was at either end), append
   to the active list (`headActive = index` when the active list is empty, otherwise the old active
   tail's `nextActiveIndex` takes the index and this record's `prevIndex` takes the old tail), set
   this record's `nextActiveIndex = -1`, **set bit 5 of the flag word**, and `tailActive = index`.

After the last record, `tailPending` and `headPending` are both set to `-1` (`0042888C`, `00428893`)
— and those two stores run **even when the pending list was empty**, because the emptiness test at
`0042872A` jumps straight to them. `liveCount` is not touched.

**Corrected 2026-09-12 by execution.** This paragraph described steps 6 and nothing else, and said
the pending list is emptied wholesale "not by the per-record unlinks". Both happen: each record is
properly unlinked and the ends are then cleared anyway. The four callees, the two stamps and the
flag-bit bracket were all missing.

**Retire — `00427C90`.** Walks the active list from `headActive` with a constant `0` in `ebp`, the
successor again read before anything else (`00427CD4`). For each record whose `+0x290` has bit 1 set:

1. Patch the neighbours' links.
2. `liveCount--` (`00427D18`) — **before** the two end fixups, not after them *(qualified 2026-10-02, OPUS: and before every call of steps 5-7, with no positive-count test and no read of the id at `+0x0` before it - the only selection test is `+0x290` mask 02 at `00427C90`+0x3D, and the signed next link is cached at +0x44 before the branch. A count of 0 would decrement to -1 and skip step 4's reset, arithmetic only; render-removal-phase-contracts, accepted)*.
3. `headActive` from the record's `next` and `tailActive` from its `prev`, each guarded by comparing
   the ends against the **record's own id at `+0x00`**, not against the index the walk is holding.
   The two are the same until something plants a record whose id disagrees with its position, and
   then the ends are left alone and the list is broken rather than repaired.
4. If `liveCount == 0`, `nextFreeIndex = 0`.
5. `call 0042F4C0(record)`.
6. **Drain the child list at `+0x08`**: while it is not `-1`, `call 00426EC0(pool + child * 0x740)`.
   The parent's `+0x08` is re-read every iteration and retire never writes it, so this loop
   terminates only if the callee unlinks the child it was handed. **The terminator is the callee's
   postcondition, not retire's** — which is also why no fixture here can drive the loop.
7. `call 003B6000(record[+0x114])` if that handle is non-zero, then `call 003AFBE0(record[+0x118])`
   if that one is, then `call 004200A0(record)`, then **set bit 5 of the flag word**.

   **The two handles are the record's SHADOW OBJECTS, and the two calls are their frees** — folded
   from FABLE's BT-1 note by OPUS 2026-09-13, with all four addresses re-verified at the image:

   | handle | pool | allocator | free |
   |---|---|---|---|
   | `record + 0x114` | 160 slots of `0xE0`, reached through the POINTER at `[02B40528]` | `003B56D0` (`003B56DF mov rbx, qword ptr [rip+..]`) | `003B6000` (`003B600A add rax, qword ptr [rip+..]`) |
   | `record + 0x118` | 32 slots of `0x70`, the table AT `02B3F570` | `003AF340` (`003AF35B lea rbx, [rip+..]`) | `003AFBE0` (`003AFBE7 lea rdx, [rip+..]`) |

   > **The two pools are reached differently and a reimplementation must not unify them.** The
   > `0xE0` pool is behind a POINTER — both its allocator and its free DEREFERENCE `02B40528` —
   > while the `0x70` table IS `02B3F570`, taken by `lea` in both. So one is relocatable and the
   > other is fixed in the image, which is invisible if the two are read as "two pools".

   The per-frame walker's callee `00426340` gates both on the record's state; see the record
   page §13. **Nothing in the note contradicted this contract** — it names what step 7 was already
   calling, which is why this fold adds and corrects nothing.
   > *Identified 2026-09-12 (FABLE, BT-1). **FOLDED INTO STEP 7 BY OPUS 2026-09-13**, all four addresses re-verified; kept here as the derivation.* The two
   > handles are the record's **shadow objects**: `+0x114` an entry of the 160-slot `0xE0` pool at
   > `[02B40528]`, `+0x118` an entry of the 32-slot `0x70` table at `02B3F570`; `003B6000` /
   > `003AFBE0` are their frees, `003B56D0` / `003AF340` their allocators, and the per-frame walker's
   > callee `00426340` gates them on the record's state — see the record page §13.

**Corrected 2026-09-12 by execution.** Steps 2, 3, 6 and 7 were missing or in the wrong order.

**Release — `00429140`.** Given a record pointer. A null answers `0` and does nothing. Otherwise the
record's own state selects **one of two entirely different paths**, and the answer is `1` either way
— and `1` as well when neither applies *(qualified 2026-10-02, OPUS: so a 1 reports "not null", not completion - it covers path one's deferred mark, the no-op when neither applies (`00429140`+0xC4 jumping to +0x156, no call and no non-stack write) and path two's direct unlink and clear, and only path two leaves the row cleared on return; render-removal-phase-contracts, accepted)*.

**Path one, when `+0x284` has bit 2 set (a live record).** Nothing is unlinked and no count moves:

1. Set **bit 1** of `+0x290` — the same bit retire selects on — so the next retire pass is what
   removes this record. Set bit 0 of `+0x2AE`.
2. Zero `+0x108` (8 bytes) and `+0x110`.
3. `+0x284 = (+0x284 & ~4) | (1 << 30)`: the live bit off, bit 30 on.
4. `call 00422D50()`; if it answers a pointer, clear bit 1 of that object's `+0x0C`.
5. If `+0x18` is not `-1`: resolve `+0x10` through `0020E600`, read the owner at `+0xD98` of the
   result, `call 002ED570(owner, +0x18)`, and if that answers a pointer, clear bit 2 of its first
   dword and store `0020E620(0)` — minus the resolver's base — into its `+0xA0`. The test of `+0x18`
   is made twice (`004291B0`, `004291C1`) with nothing in between that could change it.

**Path two, when bit 2 is clear and `+0x290` has bit 0 set (allocated, never promoted).** The unlink
shape against `headPending`/`tailPending`, `liveCount--`, `liveCount == 0 → nextFreeIndex = 0`, and
then `call 0041F730(record)` — the full reset, which is what returns the record to the free cursor *(qualified 2026-10-02, OPUS: the count drops at `00429140`+0x10D, after the neighbour links and before the end fixups, the new-count-0 cursor reset (+0x148) and the clear (+0x151), with no positive-count test; this arm makes no `004200A0` call, so none of retirement's step-7 cleanup runs. "Returns to the free cursor" means the clear leaves `+0x284` at 0 for the scan to find, under the clear's premises; render-removal-phase-contracts and render-clear-callee-footprints, accepted)*.

**Corrected 2026-09-12 by execution. This is the largest correction in the contract.** The section
said the unlink happens *when bit 2 is set*. It happens when bit 2 is **clear**; a live record is
only marked. That inverts the lifetime: release is not how a record leaves the pool, it is how a
record is *asked* to leave, and `00427C90` is the only function that removes a promoted record and
the only one that drops the count for it. Two other contracts read this one for lifetime.

## 8. Script · resource · event interactions

None of these functions reads authored data or a script value. The name that keys allocation arrives
as a caller argument; where it comes from is outside this contract.

## 9. Determinism

Fully deterministic given the call order. The free cursor makes allocation **order-dependent in the
index it hands out**: the same sequence of allocations and releases always produces the same indices,
but interleaving them differently produces different indices for the same names. A reconstruction
that allocated the lowest free index instead of scanning forward from the cursor would be
observationally different the moment a record is released and another allocated, because record
indices are written into other structures (`+0x2C` here, and the transform publish path).

## 10. Failure paths and edge conditions

- **Duplicate name** and **pool full** both return `0` from `allocate` with no distinguishing
  output. A caller cannot tell them apart, and neither logs.
- `00429140` returns `0` when handed a null record and does nothing. **Every other input answers
  `1`**, including a record that matches neither path — so the answer reports "not null" and not
  "something happened", and no caller can tell the two paths apart from the return value.
- **The free-cursor scan at step 7 has no iteration bound of its own.** It terminates because the
  `liveCount >= 160` test at step 7 precedes it, so at least one record is free. If `liveCount` ever
  disagreed with the records' `+0x284` state words, the scan would not terminate. Nothing in the
  binary checks that agreement; it is an unstated invariant between two representations of the same
  fact, and it is the sharpest fragility in this family *(qualified 2026-10-02, OPUS: the accepted slot packet states the same condition as a premise - stable readable flags with at least one zero - and names a second unchecked input: a starting cursor outside 0..159 addresses a row outside the pool at the first clear, before the scan begins. Both are conditional countermodels, not observed faults or hangs; render-slot-identity-publication, accepted)*.
- Retire and release both call a per-record teardown *after* the unlink and the decrement, so a
  teardown that re-entered the pool would see consistent indices but a decremented count *(qualified 2026-10-02, OPUS: retirement's teardown is `004200A0`, release's is the bare clear `0041F730` with no `004200A0`; in both the decrement and the new-count-0 cursor reset precede the call, and retirement then sets bit 5 of the flag word after `004200A0` returns (`00427C90`+0x123); render-removal-phase-contracts with FABLE's narrowing, accepted)*.

## 11. Observable behaviour

Not established. Everything above is static. What would be observable, if anyone captured it:

- allocating the same name twice returns a record the first time and nothing the second;
- a record is absent from whatever the active walk drives for at least one promotion boundary after
  it is allocated;
- with 160 records live, the next allocation fails and no record is displaced.

## 12. Reproduction formula

```c
/* tail = *(char**)0x022C6F28 + 0x48800 */
int16_t pool_lookup(const char *name);              /* 004278E0 */

void *pool_allocate(const char *name, const void *a32, const void *b32, ...)
{
    if (pool_lookup(name) != -1)      return 0;     /* 004279D7 */
    if (tail->liveCount >= 160)       return 0;     /* 004279E9 */

    int32_t  i   = tail->nextFreeIndex;             /* 004279FA */
    record_t *r  = pool + i;
    record_clear(r);                                /* 0041F730 */

    if (tail->headPendingIndex == -1) tail->headPendingIndex = i;
    else {
        pool[tail->tailPendingIndex].nextActiveIndex = (int16_t)i;
        r->prevIndex = (int16_t)tail->tailPendingIndex;   /* movzx: 0xFFFF == -1 */
    }
    tail->tailPendingIndex = i;
    r->id = (int16_t)i;

    record_init(r, a32, b32, ...);                  /* 00420480 */
    tail->liveCount++;                              /* 00427A7F */

    if (tail->liveCount >= 160) tail->nextFreeIndex = 0;
    else {
        int32_t c = tail->nextFreeIndex;
        do { if (++c >= 160) c = 0; tail->nextFreeIndex = c; }
        while (pool[c].stateWord284 != 0);           /* 00427AD2 */
    }
    return r;
}
```

The `do/while` shape is the one the binary has: `nextFreeIndex` is **stored on every iteration**
(`00427AB2`), not only at the end, so an interrupted scan leaves the cursor part-way.

## 13. Runtime validation

**Executed 2026-09-12 as the twenty-seventh differential pilot (`OPUS-RENDERPOOL-ISOLATED`).
Evidence class: isolated original-code. Not observed in a running game, and nothing below claims
otherwise.**

`Reconstruction/Tests/Differential/diff_render_pool.py` runs all five entry points as **shipped bytes
under Unicorn at their real virtual addresses** — `004278E0`, `004279B0`, `00428710`, `00427C90` and
`00429140` — against `Reconstruction/Game/Render/render_pool.c`, built by MSVC at `/W4 /O2`. The
look-up is **not** stubbed inside allocate: allocate really calls it. Neither are `0020E600` and
`0020E620`, three instructions each, which the reconstruction reproduces rather than scripts. ~~Eleven~~ Thirteen *(corrected 2026-10-02, OPUS: `diff_render_pool.py` scripts 13 - `RESET`, `INIT`, `PREP`, `ASK`, `STAMP`, `FINISH`, `HANDOFF`, `CHILD`, `FREEA`, `FREEB`, `DESTROY`, `ASKREL`, `FIND` - the 13 the §15 row lists)*
other callees are oracles at their own real addresses, and every one of their calls is compared as a
trace line, so an argument that changed would fail even where no state does.

    diff_render_pool : 525 commands, 581 compared lines, 0 mismatches,
                       68 allocations accepted and 4 refused, 322 oracle calls traced
    negative controls: the pending walk given the active walk's retirement test - 460 of 583 lines;
                       release unlinking a live record - 21; promotion clearing the record's bit 1
                       instead of bit 0 - 25; the free cursor reading +0x284 as a byte - 4; the end
                       fixups comparing the walk's index instead of the record's id - 1
    mutation campaign: 95 mutants, 90 KILLED, 1 SURVIVED, 4 TIMEOUT,
                       inputs stable and hashes re-checked

**Two campaigns, and what the first one bought was a list of things the fixture could not tell
apart.** Sixteen mutants survived it, and every one named a real gap rather than a weak mutant: both
retirement-bit tests had only ever been driven at `+0x290 = 3`, so a mask widened by bit 0 behaved
identically; the free cursor's wrap had only been driven where record 0 was free, so wrapping to 1
reached the same answer; the promotion bracket had only been driven at bit 0; and the release path's
three zeroing writes and its two side-object masks were all aimed at fields that were already what
the write makes them. A hundred commands of fixture closed fifteen of the sixteen.

**The one survivor and the four timeouts are both predictions of this contract, not weaknesses of
the suite.** The survivor moves `RP_REC_CHILD` from `+0x08` to `+0x09` and nothing notices, because
retirement's child loop is entered zero times — see below. All four timeouts are mutants of the free
cursor's scan or of the `-1` sentinel it stops on: each makes an unbounded loop fail to terminate.
**§10 already names that scan as the sharpest fragility in this family**, and the campaign found it
again from the other side. A timeout is not scored as a kill here and is not claimed as one.

**The reconstruction was written from §7 first, deliberately.** Every other pilot this week was
written from the disassembly and still had things backwards that only execution found; this one
tested the cheaper path — implement what the contract says and let the run adjudicate. The result is
the answer to that question. §7 as written produced a reconstruction that was wrong about which
function unlinks a record, which bit promotion clears, what the pending walk tests, what promotion
does besides re-linking, what retirement does after the hand-off, and what release answers. Five of
those are corrections now carried in §5, §7, §10 and §15; the others were omissions.

**The fifth control is the argument for the fixture.** Changing the end fixups to compare the walk's
index instead of the record's own id fails on exactly **one** line of 581 — the case built for it, a
record whose planted id disagrees with its position. Every other case in the suite has the two equal,
so without that one case the suite would have proved a claim it never tested.

**What this run does not establish.**

- **Nothing here has been observed in a running game.** The three §13 requests below stand.
- The **constructor `004269A0`** is out of scope; both sides plant the state it would leave.
- **Retirement's child loop is entered zero times.** It re-reads the parent's `+0x08` after every
  call to `00426EC0` and retire never writes it, so the loop terminates only if that callee unlinks
  the child it was handed. A scripted oracle cannot supply that without inventing the effect, so the
  loop is undriven and its termination is **the callee's postcondition, not retire's**.
- The promotion **flag-bit-0 bracket** is driven with the bit set and clear, but the oracle never
  changes it, so the restore is shown preserving a bit and never undoing a callee's write to it.
- What the **~~eleven~~ thirteen scripted callees** *(corrected 2026-10-02, OPUS: the 13 oracles of `diff_render_pool.py`)* do to a record beyond the fields this pool reads is not
  established. Only the reset's link writes are modelled, from its own bytes at `0041F771`-`0041F795`,
  and only because the list logic reads them. **A stubbed effect is not a proved one.** *(qualified 2026-10-02, OPUS: for the reset's own helper calls this is now bounded statically - their composed write footprints lie inside the record and miss `+0x0` and `+0x284` (see §4) - which bounds the effect without executing it; the other scripted callees remain oracles; render-clear-callee-footprints, accepted)*

**Still wanted from a running game**, unchanged by this run and in the order they would pay:

1. **Invariant 3** (`liveCount == 0 → nextFreeIndex == 0`) is asserted in two independent places.
   Both are now executed in isolation; a breakpoint on `00427D50` and `00429288` would show whether
   both fire in a normal session.
2. **The free-cursor termination argument** in §10 rests on `liveCount` agreeing with 160 state
   words. One read of `liveCount` alongside a count of records with `+0x284 != 0` settles it.
3. **The promotion boundary** in §6 — that a record is invisible to the active walk until `00428710`
   runs. This run shows the two lists behaving that way in isolation; it cannot show when a real walk
   happens, which is the part downstream contracts depend on.

Requested from ASTRA; not claimed by me.

## 13a. Falsification pass 1 — 2026-09-12 (OPUS), SURVIVED

Run under `EVIDENCE-STANDARD`'s procedure against the current program state. **Every claim below was
attacked by naming what would make it false and then looking for that**, not by re-reading the
document.

| # | invariant | the killer | what the binary says |
|--:|---|---|---|
| 1 | a head is `-1` iff its list is empty | the two cited tests read the same field, or a field that is not a head | **holds.** `00427A18` tests `+0x48810` = `headPending` (tail-relative `+0x10`); `0042882A` tests `+0x48800` = `headActive` (`+0x00`). Two different lists, as claimed — the offsets are tail-relative and §3 says so |
| 2 | `0 <= liveCount <= 160`, ceiling **before** the increment | the compare is `>`, or against another constant, or after the increment | **holds exactly.** `004279E9 cmp dword [rbx+0x4880C], 0xA0` / `jge` returning 0, and the `inc` is at `00427A7F` — after |
| 3 | `liveCount == 0 → nextFreeIndex = 0`, in both release paths **identically** | one path stores something other than zero | **holds.** `00429140` is literal (`0042927D cmp …, 0` / `xor eax,eax` / `00429288`). `00427C90` stores a **register** — `ebp` — and `00427CBA xor ebp, ebp` is the only write to it before the use, so it is zero |
| 4 | `liveCount` is untouched by promotion | `00428710` accesses `+0x4880C` | **holds.** No access to that offset anywhere in the function |
| 5 | `+0x284 == 0` means free | the scan tests another offset or another value, or a release leaves it non-zero | **holds.** `00427AD2` compares `[record + 0x284]` against `eax`, and `eax` is zero from `00427A7D`. `0042049A` sets it to `0x2010F9`. Both release paths reach `0041F730`'s whole-record `memset` *(qualified 2026-10-02, OPUS: reaching the memset is not the postcondition by itself - 125 direct writes and six calls into four helpers follow it, and `+0x284` is 0 and `+0x0` is -1 on return under the clear's premises; render-clear-callee-footprints, accepted)* |

**What was tried and did not break it.** The pool arithmetic was recomputed rather than accepted:
`160 × 0x740 = 0x48800`, `+ 0x130 = 0x48930`, the stated allocation. Every stated body size was
re-checked against the current census — **no drift**. A banned-evidence sweep for `.pdata`, `.xdata`,
unwind, EH-map and IP-to-state terms found **nothing**. `audit_crossrefs.py` reports **no findings**
for this document, so `crossref_clean` is now true rather than assumed. The hardest attack —
**looking for a release that decrements `liveCount` without resetting the record**, which would make
the unbounded free-cursor scan spin forever — failed: the path that does not call `0041F730` calls
`004200A0`, which does.

**What the pass added rather than corrected:** the termination argument in §4, which the document had
in pieces and never joined, and the fact that one release path reaches the reset indirectly.

> **One pass is one pass.** `AUDITED` means *survived a deliberate attack against a named program
> state*, not *true*. ~~The five operations are still **unexecuted** — §13's pilot does not exist —~~ *(answered: see §13 - `diff_render_pool.py` runs all five as shipped bytes, re-run 2026-10-02: 581 lines, 0 mismatches; and the correction below; 2026-10-02, OPUS)* so
> everything above rests on reading the instructions, and reading is what this session has twice seen
> a pilot refute within the hour.

### 13a. The seven experiments that name this contract — one cited, six declined (FABLE, 2026-09-22)

Seven experiments carry `contract: ../17-Presentation-Rendering/CONTRACT-render-record-pool-lifecycle.md`
in their front matter and none was cited back. Under the cite-or-decline ruling
(`FABLE-NOTICE-EXECUTION-EVIDENCE-IS-NOT-REACHING-THE-PAGES-MEASURED`, routed via
`FRONTIER-REQ-FABLE-EXPERIMENT-BACKREFS`) each must be cited or declined **with a reason**.

**The test, stated before the answer:** this contract's scope is its six entries plus their 26 direct
callees — 31 addresses, `004278E0` appearing in both sets, which is the control. An experiment earns
a citation here by executing something in that set that this section currently runs as an oracle.

| experiment | its subject | addresses in this contract's scope | disposition |
|---|---|---|---|
| [`EXP-120`](../_experiments/EXP-120-exp108-tail-resolvers-exec.md) | EXP-108's ramp-channel consumer tails | `0020E600`, ~~**`002ED570`**~~ **`003E56A0`** | **CITED** |
| [`EXP-121`](../_experiments/EXP-121-exp109-queue-tails-exec.md) | the staged lane queue and table tails | **none** | declined |
| [`EXP-122`](../_experiments/EXP-122-alloc-dispatch-exec.md) | allocator dispatch, the staged-kind front door | `0020E600`, `0020E620` only | declined |
| [`EXP-123`](../_experiments/EXP-123-alloc-core-exec.md) | the 887 B intrusive free-list allocator | `0020E600`, `0020E620` only | declined |
| [`EXP-125`](../_experiments/EXP-125-pool-adoption-exec.md) | the compacting-allocator move scan | `0020E600`, `0020E620` only | declined |
| [`EXP-126`](../_experiments/EXP-126-alloc-free-path-exec.md) | the allocator free/release path | `0020E600`, `0020E620` only | declined |
| [`EXP-128`](../_experiments/EXP-128-exp109-poll-pump-exec.md) | the `E070` six-arm task state machine | **none** | declined |

~~**`EXP-120` is cited because it executes `002ED570` — `ResourceTable_ResolveEntryByIndex`, a direct
callee of these entries, and one of the eleven this section runs as an **oracle***.~~ *(Corrected 2026-09-25, FABLE, Claude Opus 5.5, on OPUS block 301 and the s38 exposure study; EXP-120 re-read.)* **The citation stands
and its reason was wrong.** EXP-120's executed set is `003E56A0` / `00370F60` / `0020E600`; its own text says
`002ED570` was closed by EXP-117. `003E56A0`, the tail EXP-109 had scripted, is in this contract's scope, and that
is what earns the citation. *The table records the front-matter keys as of 2026-09-22. Since then EXP-121 and
EXP-128 name the resource request queue, and EXP-122/123/125/126 name no contract.* Executing it as
shipped bytes (14/14 functional cases, 14/14 mutants, stable) converts one of those eleven from a
traced oracle into original code that ran. **It does not execute any of the five operations**, so
~~§13's headline is unchanged and the sentence above it still stands: the five are unexecuted.~~ **That sentence was
already false when written.** §13's `diff_render_pool.py` (2026-09-12) runs all five entry points as shipped
bytes, and §20's EXP-109 (2026-09-19) executes all six lifecycle operations. The five **are** executed: by the
differential and by EXP-109, not by EXP-120 *(Corrected 2026-09-25, FABLE, Claude Opus 5.5, on OPUS block 301 and the s38 exposure study; EXP-120 re-read.)*.

**The six are declined on measurement, not on judgement.** `EXP-121` and `EXP-128` touch **nothing**
in the 31. The four allocator experiments touch only `0020E600` and `0020E620` — the two
three-instruction image-address helpers this very section says the reconstruction *"reproduces rather
than scripts"*. They are in every pilot in the database; sharing them is not a relationship between
subjects. The real subjects are the general allocator (`00369860`–`0036C900`) and the queue/task
machinery (`0032E…`, `0035E…`), neither of which this contract covers.

> **So the `contract:` key on those six is mis-targeted, and that is the finding rather than the
> declines.** Six executed experiments — 333 functional cases and 305 mutants between them — are
> pointed at a contract that does not describe them, which means the allocator and the queue pump
> have real execution evidence filed under a page that cannot use it, **and whatever contract does
> cover them reads as static.** Reported back rather than repaired here: the `contract:` keys are the
> experiments' own front matter, not mine to rewrite. *`EXP-120`'s key is arguably mis-targeted too —
> its subject is EXP-108's tree — but it is cited anyway, because the callee it executes is genuinely
> this contract's.*

## 14. Unresolved

- The bit meanings of the flag word at `+0x18`. Bit 5 is set by promotion ~~;~~ and by retirement *(corrected 2026-10-02, OPUS: `00427C90`+0x123 `or dword ptr [rdi + 0x48818], 0x20`, §5)*; bits 0, 2 and 4 are
  touched by callers outside this family. FABLE.
- `+0x40` and `+0x4C..+0x70`: written once by the constructor, no reader observed in a depth-2 route
  census. Absence of a reader in that census is not absence of a reader.
- `+0x64` is an 8-byte span with one 8-byte store and no other access; whether it is one field or
  two is **not** decided by that store.
- The relationship, if any, between the 16-bit index at `+0x2C` and either list.
- Which caller supplies the names that key allocation.

## 15. Evidence

Static, from the shipping image (`73461D08…`), instruction by instruction. The access census
`17-Presentation-Rendering/Character-Render-Records/character-render-system-tail-accesses.tsv`
(153 accesses in 54 functions) was built by seeding the pool pointer with a negative base offset so
that only accesses at or above `+0x48800` land in range, with the allocator's own capacity test as
the control. Its limits are the tool's: depth-2 argument propagation, no branch structure.
**Named-gap audit 2026-09-16** (OPUS-REQ-STRUCT-WIDEN-FOUR-CENSUS-SEED-LISTS): the five
`CharacterRenderSystem_*` functions absent from this census were each read and dispositioned — three
are `jmp` trampolines whose targets (`002EBC30`, `002EBBB0`, `00425FB0`) are already census seeds
carrying the same public names, and two (`003325D0` the pool allocator, `00428980` the command-packet
emitter) touch no tail field. No seed change was justified; the census is unchanged.

Three findings here came from reading the disassembly after the census disagreed with expectation,
not from the census itself: the free-cursor wrap (the census shows four writes to `+0x08` and says
nothing about their order), the name-keyed refusal (the census does not see `004278E0`'s return
value), and the `movzx`/`movsx` width crossing.

An image-wide displacement sweep for `+0x4880C` was run as a negative check — the census reports
`liveCount` reads only, which would have meant the ceiling at 160 could never be reached. The sweep
found `inc` at `00427A7F` and `dec` at `00427D18` and `0042924D`, with a positive control on
`+0x48808` that recovered its six known writers. **The negative was refuted**; the census had
recorded the read-modify-writes correctly and the apparent absence was a reporting error on my side.

**Claim table added 2026-09-12 (`OPUS-S15-CLAIM-TABLES-SIX`).** The prose above states the method
and is kept; this enumerates the claims so a pilot's `CONTRACT_MAP` can be derived from them.
**Rows re-tiered 2026-09-12 (`OPUS-RENDERPOOL-ISOLATED`).** The lifecycle has now been executed in
isolation — see §13 — and the rows that the run drove say so. Rows still marked `static` were not
driven: the constructor, the `+0x2C` index and the census-derived statements about who else touches
the tail. **No row claims live evidence**; nothing here has been observed in a running game.

| claim | evidence | tier | confidence |
|---|---|---|---|
| the pool is 160 records of stride 0x740 ahead of the tail block | `*(char**)0x022C6F28 + 0x48800`, with the ceiling `160` read from the compare at `004279E9` | 1 (static) | PROVEN |
| the pool's six indices are 32-bit and the record's three links are 16-bit, both using -1 | every head write from a link uses `movsx` (`0042880B`, `00428820`, `00427D29`, `00427D3E`, `0042925E`, `00429273`) and every link write from a head uses `movzx` (`00427A3C`→`00427A43`, `00428853`→`0042885A`) | 1 (static) | PROVEN |
| the narrowing is correct rather than lucky | a 32-bit `-1` truncated to 16 bits is the 16-bit sentinel the link field uses — the truncation sites are the link stores `00427A3C`→`00427A43` and `00428853`→`0042885A` on the row above; widening the links without widening the comparisons, or making either side unsigned, breaks it | 1 (static) | PROVEN |
| the 8-byte store in the constructor is not evidence that two fields are one | `004269ED` covers `nextFreeIndex` and `liveCount`, which are read separately at 4 bytes everywhere else | 1 (static) | PROVEN |
| allocation is keyed by name and refuses a duplicate rather than replacing it | step 1 of `004279B0` returns 0 when `004278E0` finds the name | 1 (static) | PROVEN |
| allocate's two failure returns are indistinguishable to the caller | ~~both are `xor eax, eax` — `004279E2` (duplicate refused) and `00427A7D` (pool full)~~ both leave through the one `xor eax, eax` at `004279B0`+0x32: a duplicate falls into it and the pool-full test `004279B0`+0x39 (`cmp ..., 0xa0` then `jge`) jumps back to it *(corrected 2026-10-02, OPUS: the other cited site is `004279B0`+0xCD, on the success path, the zero the free-cursor wrap uses)*; a refused duplicate and a full pool look the same | 1 (static) | PROVEN |
| a newly allocated record is on the PENDING list, invisible to any active walk | step 4 links at the tail of pending; nothing sets an active link until `00428710` | 1 (static) | PROVEN |
| the free cursor advances to the next record whose state word +0x284 is 0, wrapping at 160 | step 7, against the initializer that sets it non-zero at `0042049A` and the scan at `00427AD2`; it stops within 160 visits only under stable flags with at least one zero *(qualified 2026-10-02, OPUS: render-slot-identity-publication, accepted)* | 1 (static) | PROVEN |
| liveCount == 0 implies nextFreeIndex == 0 | enforced identically and independently in both release paths — `00427D48`/`00427D50` and `0042927D`/`00429288` — and in the constructor. The only invariant here asserted in two places at once | 1 (static) | PROVEN |
| liveCount counts records on EITHER list, and promotion does not change it | `00428710` has no access at `+0x0C` | 1 (static) | PROVEN |
| promotion unlinks each record AND clears both pending ends afterwards | `004287C4`-`00428824` is a full unlink per record; `0042888C`/`00428893` then set both ends to `-1` anyway, and run even when the list was empty. **This row said the ends are cleared "not by the per-record unlinks"**; both happen. Corrected 2026-09-12 | 1 (isolated original-code) | PROVEN |
| promotion sets bit 5 of the tail's flag word | `00428863`; ~~the other bits of `+0x18` are set by unrelated callers~~ retire sets it too (`00427C90`+0x123), the constructor sets bits 0 and 2 (`004269A0`+0x2B9 `or ..., 5`) and promotion brackets bit 0 (`00428710`+0x80..+0xA7); the other writers, `002E8700`, `002E8CC0`, `002EBBB0` and `002EBBF0`, are outside the family *(corrected 2026-10-02, OPUS: every `+0x48818` access in the image, retool grep)*; their meanings are not established here | 1 (static) | PROVEN |
| retire acts only on actives whose +0x290 has bit 1 set | `00427CCD test byte [rbx+0x290], 2` | 1 (isolated original-code) | PROVEN |
| the lifecycle never reads or writes the tuning fields EXCEPT +0x28 | `+0x1C`, `+0x20`, `+0x24`, `+0x40` and `+0x4C..+0x70` are written ~~only~~ by the constructor and by `0042ED30`, and `+0x1C` also by the keyed setter `002EBC30` *(corrected 2026-10-02, OPUS: `002EBC30`+0x7, reached from `0026C8C0`+0x4F9)*; **`+0x28` is read by promotion** at `0042876A` and stamped into each promoted record's `+0x414`. Corrected 2026-09-12 | 1 (isolated original-code) | PROVEN |
| the +0x2C index is a third width again and ~~no lifecycle operation touches it~~ only construct touches it, storing `0xFFFF` *(corrected 2026-10-02, OPUS: `004269A0`+0x66 `mov word ptr [rsi + 0x4882c], ax`)* | 16-bit with an `0xFFFF` sentinel, scaled by `0x740` at `0042E954`–`0042E973` | 1 (static) | PROVEN |
| the pending walk has no retirement test, and the active walk does | `0042790A` tests `+0x290` bit 1 in the first loop; the second loop at `00427952` has no such test. Executed: a marked record is invisible to a look-up when active and answers one when pending, and hoisting the test to cover both changes 370 of 492 lines *(the first suite; 460 of 583 in the current one, §13 - scope named 2026-10-02, OPUS)* | 1 (isolated original-code) | PROVEN |
| allocate sets bit 0 of the record's +0x290 and promotion clears it | `00427A76 or dword [rdi+0x290], 1` and `004287BD and dword [rsi+0x290], 0xFE`. The bit therefore means "allocated and never promoted", which is the state release's second path acts on. Executed on both sides of a promotion | 1 (isolated original-code) | PROVEN |
| a fresh record's links are the RESET's postcondition, not allocate's | allocate writes `prevIndex` only in the non-empty case and never writes `nextActiveIndex`; `0041F771`-`0041F795` writes six 16-bit links at `-1`. Executed with the reset's link effect modelled from those bytes: without it the first promotion walks into record 0 | 1 (isolated original-code) | PROVEN |
| the free cursor reads +0x284 as a DWORD, starts at the record just taken, wraps at 160 and parks at 0 when the pool fills | `00427AD2 cmp dword [r8+rbx+0x284], eax` with `eax` zero; `00427AB0`-`00427AC2`. Executed against a byte-wide read, which differs on a state word of `0x100` | 1 (isolated original-code) | PROVEN |
| promotion stamps the tail's +0x28 into the record's +0x414 and conditionally takes a handle into +0x114 | `0042876A`-`00428773`, then `003E68E0` gating `003B56D0(record.id)` at `00428779`-`0042878A`. Executed at both answers of the question | 1 (isolated original-code) | PROVEN |
| promotion clears flag bit 0 for one callee and restores it whatever the callee did | `00428790`-`004287B7`: `and eax, ~1`, the call, then an xor of the difference masked to bit 1. Executed with the bit set and clear | 1 (isolated original-code) | PROVEN |
| retirement decrements the count BEFORE the two end fixups, and the fixups compare the record's own id | `00427D18` precedes `00427D1E`-`00427D42`, which compare `movsx eax, word [rbx]` against each end. Executed with a planted id that disagrees with the walk: the ends are left alone and the list is broken rather than repaired | 1 (isolated original-code) | PROVEN |
| retirement frees two handles and drains a child list at +0x08 | `003B6000(+0x114)` and `003AFBE0(+0x118)`, each guarded by a non-zero test, then `004200A0(record)` and flag bit 5 at `00427DB3`. The child loop at `00427D5E`-`00427D8B` re-reads the parent's `+0x08` and retire never writes it, so **its terminator is `00426EC0`'s postcondition**; the handle frees are executed, the child loop is not and cannot be from a scripted oracle | 1 (isolated original-code) | PROVEN |
| release does not unlink a live record: it marks it for retirement | `0042916F or dword [rcx+0x290], 2` on the bit-2 path, with no list write anywhere on it. Executed: the ends, both lists and the count are unchanged, and a following retire is what removes the record | 1 (isolated original-code) | PROVEN |
| release's unlink path is the one for a record that was never promoted | `00429204` tests `+0x290` bit 0 after the bit-2 path is not taken, and only that branch unlinks, decrements and resets. **This section's §7 said the unlink happens when bit 2 is SET.** Corrected 2026-09-12 | 1 (isolated original-code) | PROVEN |
| release answers 1 for every non-null record, including one that matches neither path | ~~every path but the null converges on `00429296 mov eax, 1`.~~ Every non-null path answers 1, through two returns: the mark arm's full path loads 1 at `00429140`+0xB9 and returns at +0xC3, and every other non-null path converges on +0x156 *(corrected 2026-10-02, OPUS: three returns - +0x1C with 0, +0xC3 and +0x165 with 1; render-removal-phase-contracts and FABLE's review, accepted)*. Executed at all three | 1 (isolated original-code) | PROVEN |
| release's live path drops two side objects through the resolver pair | `00422D50` then `+0x0C &= ~2`; `0020E600(+0x10)`, the owner at `+0xD98`, `002ED570(owner, +0x18)`, then `first &= ~4` and `+0xA0 = 0020E620(0)`. Executed at each combination of the two answers and both values of `+0x18` | 1 (isolated original-code) | PROVEN |
| what the ~~eleven~~ thirteen scripted callees do to a record beyond these fields is NOT established *(corrected 2026-10-02, OPUS: this row lists thirteen)* | `0041F730`, `00420480`, `0041FCF0`, `003E68E0`, `003B56D0`, `0042C410`, `0042F4C0`, `00426EC0`, `003B6000`, `003AFBE0`, `004200A0`, `00422D50` and `002ED570` ran as oracles. Only the reset's link writes are modelled, and only because the list logic reads them; for `0041F730` alone its helper write footprints are now bounded statically, inside the record and clear of `+0x0` and `+0x284`, which narrows this row for that callee without executing it *(qualified 2026-10-02, OPUS: render-clear-callee-footprints, accepted)* | none | UNKNOWN |
| `0051BA80` admits through `0051F080` with `refresh = 0` when the caller's slot is `-1` | `r9d` zeroed at `0051BAE9`, call at `0051BAF5`; the `0x3B0` record is then copied in (`0051BB20`–`0051BB7D`) and `0041CA70` finalizes | 1 (static) | PROVEN |
| `0051F620` resolves its base by the signed low-2-bit mode of `[rcx+4]` and rebases every linked node's `+0x18` | `shl/sar 0x1E` mode select at `0051F63A`; walk headed `[rbx+0x1C]`, `0x30` stride, `[node+0x18] = 003AB7F0([node+0x10]) + [node+0x20]` | 1 (static) | PROVEN |
| the rebase walk reads each node's `+0x0C` link AFTER the `003AB7F0` call, with no snapshot | `call` at `0051F682`, next-index read at `0051F690` | 1 (static) | PROVEN |
| the slot handle is `(gen << 8) \| slot` and the generation CLAMPS rather than wraps | `003B56D0` executed real: scans `q[02B40528]` for `b[slot+0x40] & 1 == 0` to a `0xA0` cap, then `d[02B40520]`+1 with `cmova` forcing `> 0xFFFFFF` to **1**. `alloc-gen-wrap` (`gen=0xFFFFFF`) yields `(1<<8)\|slot`; `alloc-gen-edge` (`0xFFFFFE`) yields `0xFFFFFF` unclamped. EXP-117 | 2 (isolated original-code) | PROVEN |
| a full pool returns handle `0`, and the allocator stamps the slot BEFORE it resolves the parent | early-out arm at `003B5707`; `d[+0x10] = handle` precedes the two parent resolves, so a failed resolve leaves an occupied slot. EXP-117 | 1 (isolated original-code) | PROVEN |
| **CORRECTS the static reading**: RES routes EVERY nonzero mode to `0036B130`, and the mode-1 arm is dead code | `003AB7F0` executed real: the `setne`/`cmp ecx,1` pair can only yield 0 or 1, so modes 1, 2 and 3 all take the resolver call and the `xor eax` arm at `003AB81E` is unreachable by construction. The earlier static claim that modes 2/3 return `0` does not hold. Mutant `cmp ecx,1`→`2` kills. EXP-117 | 1 (isolated original-code) | PROVEN |
| RES bounds the resolver's result: a low dword unsigned-`<= 0x40` is returned as `0` | `movsxd rcx,eax; cmp rcx,0x40; cmovbe rax,0` after the `0036B130` call. `res-hres-low` plants `0x30` and gets `0`; `res-hres-neg` plants `0x80000000`, sign-extended, and gets it back verbatim. EXP-117 | 2 (isolated original-code) | PROVEN |
| the allocator requires a LIVE parent record - `arg = -1`, or a zero `+0x284` gate, faults | both parent resolves substitute `rcx = 0` and `003E5AD0` then dereferences `rcx+0x400` unconditionally. `alloc-neg1` and `alloc-gate0` fault at `0x400` with the slot already stamped. EXP-117 | 2 (isolated original-code) | PROVEN |
| `002ED570`'s two handle deposits are CONDITIONAL, not cleared | a null `[ctx+0x30]` or `[ctx+8]` skips its `003AB7F0` call entirely, leaving whatever `[ctx+0x38]` / `[ctx+0x10]` already held. A reimplementation that zeroes them diverges. EXP-117 | 1 (isolated original-code) | PROVEN |
| `002ED570`'s index product is SIGNED | `cdqe` sign-extends the 32-bit `(d[ctx+0x50] & idx) * d[ctx+0x48]` before the base add - `mids-negprod` (`0xFFFF x 0x10000`) returns `base - 0x10000`. EXP-117 | 1 (isolated original-code) | PROVEN |
| row 550 NARROWS and does not close: two of its thirteen named callees have now executed real | `003B56D0` and `002ED570` ran as real bodies in EXP-117 with the semantics in the rows above; the other eleven still ran as oracles. The pool CONTENTS remain planted fixture, so what is established is the algebra these two compute, not the record layout they read. Adopted 2026-09-19 (OPUS) answering REQ-OPUS-SLOT-HANDLE-ALGEBRA-FINDINGS | 2 of 13 | PARTIAL |
| `002ED570`'s context IS the slot-bank container shape, independently | it reads `[ctx+0x30]` as a handle and deposits the resolved value at `[ctx+0x38]`, shifts the index by `[ctx+0x4C]`, multiplies by `[ctx+0x48]` and masks with `[ctx+0x50]` - which is `RenderModelInstanceContainer`'s declared `slotTableHandle` / `slotTable` / `bankShift` / `rowStride` / `indexMask`, derived statically the same day from `0051FF30` and `0051F9F0`'s three strides. Execution and static reading agree field for field. EXP-117 + `_types` | 2 (isolated original-code, static) | PROVEN |

## 16. Parity plan

A reconstruction must reproduce: the name-keyed refusal, the pre-increment capacity test, the
pending-then-promote ordering, the forward-scanning wrap-around cursor, and the two link widths with
their sentinels. Of these the cursor is the one most likely to be "improved" into a free-list and the
one whose observable consequence — which index a name gets — reaches other structures.

## 17. Related

- `CONTRACT-character-transform-publish` — the consumer of the active list.
- `CONTRACT-coast-down-latch` — addresses records by id without consulting the pool.
- `17-Presentation-Rendering/Character-Render-Records/the-character-render-record-array.md`

## 18. The presentation-entry ID carries no generation — 2026-09-13 (OPUS)

`ASTRA-REQ-OPUS-PRESENTATION-ENTRY-LIFETIME`. Confirmed, and the central claim can be put **more
strongly than it was asked**.

### The table

`0041E3FD lea rax, [rsi + 0x160]` / `0041E404 mov [rsi+0xDA8], rax` — the root publishes its
container at `+0x160`. The slots are `0x30` bytes each, computed in the allocator itself:

```asm
0051F0E5  movzx edx, si           ; the slot index = the LOW 16 BITS of esi
0051F0E8  lea   rbx, [rdx+rdx*2]  ; slot * 3
0051F0EC  shl   rbx, 4            ;      * 16  ->  slot * 0x30
0051F0F0  add   rbx, rax          ; the node
0051F0F3  or    dword ptr [rbx], 1
0051F0FF  bts   esi, 0x10         ; ID = slot | 0x10000
0051F10A  mov   dword ptr [rbx+4], esi
```

**64 slots × `0x30` = `0xC00`, and `0x190 + 0xC00 = 0xD90`** — the span closes exactly on the next
field, which is the arithmetic that makes "64" a measurement rather than a guess.

### Why "not a generation" is the strong form

> **The ID is a pure function of the slot index.** `esi`'s low 16 bits *are* the slot, `bts` sets bit
> 16, and nothing else is mixed in — no counter, no allocation sequence, no reuse stamp. **So it is
> not that the code forgets to bump a generation; a generation cannot be encoded here at all.** The
> same slot necessarily yields the same ID for every occupant it ever has.
>
> **A stale presentation-entry ID is therefore indistinguishable from a live one**, and that is why
> *"lookup and release require external lifetime protection"* is a **requirement of the design**,
> not a caution about current callers.

### The engine has two ID schemes, and only one of them is self-checking

| scheme | staleness detection |
|---|---|
| the **handle** table (`0036A000`, `0036D170`, `0036B130`) | a **generation**: `word [slot+6]` is compared against `word [obj+0x1C]` before the pointer is trusted — see [`CONTRACT-efx-source-rebase.md` §2](../02-Resource-And-Asset-Pipeline/CONTRACT-efx-source-rebase.md) |
| the **presentation entry** (`0051F080`) | **none** — the ID is the slot index with bit 16 set |

**A reimplementation must not carry an assumption across these two.** They look alike — a small
integer key into a fixed table — and they differ in exactly the property that decides whether holding
a key across a frame is safe.

### Method note: an artifact I nearly published

While checking `0041E3FD` I decoded from a nearby address rather than from the function entry, and
the disassembler resynchronised into `lea eax, [rsi+0x160]` — a **32-bit** `lea` that would truncate
the container pointer and would have been a serious width defect, in a cluster where width defects
are the running theme. Decoding `0041E3A0` from its entry gives the true bytes
`48 8d 86 60 01 00 00` = **`lea rax`**. There is no defect. **A decode that does not start at a known
instruction boundary is not evidence**, and the danger is sharpest when the artifact happens to
confirm what one is already finding everywhere.

`0051BA80`'s `refresh=0` admissions, `0051F620`'s refresh of all linked nodes, and the
iterator's next-read-after-callback were re-derived from the shipped bodies 2026-09-15
(SWE2-CONTRACT); ASTRA's readings hold in every particular, sharpened:

- **`0051BA80` (344 B)** — when the caller's slot is `-1` it first runs `0051F150(rcx)`
  (bailing on a negative), builds a `0x3B0` local record through `0041CB90` /
  `0041D220`, then admits through `0051F080(rdi, src, ebp, **refresh = 0**)` at
  `0051BAF5` — `r9d` is zeroed at `0051BAE9`. On success `0051F240` resolves the new
  slot, the `0x3B0` record is copied in (`7 × 0x80 + 0x30` `movups` at
  `0051BB20`–`0051BB7D`), `0041CA70` finalizes, and the slot is written to `[rdi]`.
  The `refresh = 0` entry therefore exists with unresolved `+0x18`s until a rebase
  pass runs — it is exactly the admission shape `0051F620` exists to finish.
- **`0051F620` (`PresentationEntryReferenceContainer_RebaseResolvedPointers`, 131 B)**
  resolves the base by the signed low-**2**-bit mode of `[rcx+4]` (`shl 0x1E` / `sar
  0x1E` sign-extends bits 0–1): mode 0 → `rdi = 003AB7F0([rcx+8])`, mode 1 →
  `rdi = [rcx+8]` direct, `-1`/`-2` → null; `[rcx+0x10] == 0` also selects null. It then walks the linked list headed at
  `[rbx+0x1C]`, `0x30`-stride nodes, `-1` terminated via `[node+0x0C]`, rebasing each
  node's `+0x18` to `003AB7F0([node+0x10]) + [node+0x20]`.
- **The next-read-after-callback is real and located in that loop:** `[node+0x0C]` is
  read at `0051F690` **after** `003AB7F0` returns at `0051F682` — the walk does not
  snapshot the link before calling the resolver. Whether `003AB7F0` can unlink a
  node is not established here; if it cannot, the order is inert.

**Left open:** `0041D220` / `0041CB90` resource admission and defaults, the native cleanup helpers,
and external ID invalidation.

## 19. `0041FCA0` selects `+0xCE` — and the reason is a call-site mode/id confusion — 2026-09-13 (OPUS)

`ASTRA-REQ-OPUS-RENDER-EVENT-SELECTION`. **The conclusion is right. The reason is sharper than
"cannot reach", and it comes with a precondition that should be tested rather than assumed.**

### The getter

```asm
0041FCA6  cmp   dword ptr [rcx+0xC8], -1
0041FCB0  je    0x41FCD7                    ; -1 -> return word[+0xCC]
0041FCB2  movsx r8d, word ptr [rcx+0xCC]    ; <-- the SELECTOR argument
0041FCBA  movsx edx, word ptr [rcx+0xCE]    ; the candidate
0041FCC1  call  0x4235C0
0041FCC8  je    0x41FCD7                    ; false -> return word[+0xCC]
0041FCCA  movsx eax, word ptr [rbx+0xCE]    ; true  -> return word[+0xCE]
```

### `004235C0` has exactly one `ret`, and the third argument decides whether it can be false

The whole 459-byte body has **one `ret`, at `004236E5`, preceded by `mov eax, 1`**; every other exit
`jmp`s into that epilogue. The two paths that reach it with `eax = 0` are both inside a switch on
`ebx`, and `ebx` is the incoming selector — `004235D6 mov ebx, r8d`, **with no write to `ebx` between
there and the switch** (the only one is `004236D1`, inside the epilogue):

```asm
00423735  test ebx, ebx  / je 0x423760   ; selector 0 -> CAN return 0 (via 00424230)
00423739  sub  ebx, 1    / je 0x4236CC   ; selector 1 -> return 1
0042373E  cmp  ebx, 1    / jne 0x4236CC  ; anything else -> return 1
00423743  ...            setle dil       ; selector 2 -> CAN return 0 (rank-table compare)
```

> **So the false paths exist and live in arms 0 and 2 only.** A selector outside `{0,1,2}` falls
> through `jne 0x4236CC` to the unconditional `return 1`, and the getter then selects `+0xCE`
> whenever `+0xC8 != -1` — **which is exactly ASTRA's conclusion**.

### What the other callers pass, and why that reframes the claim

| caller | third argument |
|---|---|
| `00424550` | `xor r8d, r8d` — **mode 0** |
| `00424D80` | `mov r8d, 2` — **mode 2**, and a variable at its other site |
| **`0041FCA0`** | **`movsx r8d, word ptr [rcx+0xCC]` — a 16-bit ID FIELD** |

**The other two callers use the small mode enum the switch is written for, and they use precisely the
two values that can return false.** `0041FCA0` puts an id where a mode belongs. `004235C0` even
**re-reads `+0xCC` itself** at `00423605` for the comparison it actually performs, so the argument is
redundant as an id and meaningful only as a mode.

> **The getter's unconditional behaviour is therefore a consequence of a type confusion at one call
> site, not an intended selection rule.** That is worth recording as the mechanism, because it also
> gives the claim its precondition:
>
> ~~**`0041FCA0` selects `+0xCE` whenever `+0xC8 != -1` *if and only if* `+0xCC` is never 0, 1 or 2.**~~
> `+0xCC` is loaded `movsx` — a signed word — and holds ids elsewhere in this body (`0x2035`,
> `0x2036`, `0x3D`). **If it can ever hold 0 or 2, the getter's behaviour changes discontinuously**:
> it would begin consulting the rank table at `0x1ADCCC4` or calling `00424230`. That value range is
> not established here and is not assumed.
>
> **AMENDED 2026-09-27 (OPUS, owner), consuming FABLE-REQ-OPUS-POOL-CONTRACT-S19-SELECTOR-PRECONDITION: the precondition is not needed; the selection is unconditional.**
> - **The kind test comes first.** Before its selector switch (`00423735`), `004235C0` returns 1 unless BOTH normalised event kinds, `(v >> 12) & 0xF`, are 1 or 2.
>   - The candidate is tested at `004236B0`–`004236E9`, and the current event (`+0xCC`, re-read at `00423605`) at `0042370D`–`00423727`.
>   - A `+0xCC` of 0, 1 or 2 has kind 0, so it returns 1 there and never consults the selector.
>   - A negative id has kind 0xF and returns 1 the same way.
> - **So the false arms can never run from `0041FCA0`.** The selector values that could return false (0 and 2) are exactly the values the kind test has already sent to `return 1`. The earlier empty-lookup exit (`00423613`) returns 1 too.
> - **Nothing changes the record in between.** Per FABLE's control, the callee closure's only store is `0051F2B7`, and all readers and writers run on the main thread.
> - **Result:** `0041FCA0` selects `+0xCE` whenever `+0xC8 != -1`, with no condition on `+0xCC`'s range. The call-site mode/id confusion above is still how the code reads, but it has no behavioural consequence.
> - **Evidence:** `_index/candidates/uq194-event-entry/uq194_event_entry.py` U3 and U10 (FABLE; re-run by OPUS, FAILS 0). OPUS re-read `004235C0`'s bytes `00423605`–`00423760`.

**Propagated, not re-derived:** `0051B9E0` / `0051F240` cache writes, widths and preconditions are
ASTRA's; container capacity, source/ID/refresh lifetime and native initialisation stay open.


## 20. What execution measured — [`EXP-109`](../_experiments/EXP-109-render-pool-lifecycle-exec.md), folded in 2026-09-19 (OPUS)

`EXP-109` executed all six ~~lifecycle operations plus the constructor~~ entry points - the constructor and the five operations *(corrected 2026-10-02, OPUS: §2's interface lists six entries, `004269A0` the constructor among them, and EXP-109's title names the same six)* - and the default writers from
shipped bytes. **§15's "static, from the shipping image, instruction by instruction" is no longer
the only evidence class here**, and the two must not be summed: execution shows what these bodies
compute for planted inputs, and says nothing about which inputs the game supplies.

### Confirmed, changing nothing

- **The lookup gate is a skip.** §7 already reads `+0x290` bit 1 as making a record *"invisible"*
  to lookup while still linked. Execution agrees, and the unification is worth stating plainly:
  **bit 1 has one meaning with two consequences** — hidden from lookup, and selected by the next
  retire pass.
- **The promotion bit-0 pin.** §5 already records `00428790`–`004287B7`.

> **And §5's wording is the more accurate of the two.** `EXP-109` states the pin as
> `d[+0x48818] = (post_PHOOK & ~1) | (pre_PHOOK & 1)`. That formula gives the right **output** and
> the wrong **input**: the bytes clear bit 0 *before* the call —
>
> ```
> 00428790  mov ebx, [rdi+0x48818]        ; PRE
> 0042879E  and eax, 0xfffffffe
> 004287A1  mov [rdi+0x48818], eax        ; bit 0 CLEARED, then the hook runs
> 004287A7  call 0042C410                 ; PHOOK sees bit 0 == 0
> 004287AC  mov eax, [rdi+0x48818]        ; POST
> 004287B2  xor eax, ebx
> 004287B4  and eax, 1
> 004287B7  xor [rdi+0x48818], eax        ; bit 0 restored to PRE
> ```
>
> **A reconstruction built from the formula would call the hook with bit 0 still set** and then
> patch the result — identical output, different argument, and any hook that reads bit 0 diverges.
> §5's *"cleared and then restored around"* is kept.

### Two cells that execution named wrongly, and the names are load-bearing

**`+0x48830` is a rebased POINTER, not a resolver index.** It has **exactly one writer in the
image** — the 30-byte setter `00426480`:

```
00426484  mov  rcx, rdx                 ; the caller's POINTER
00426487  call 0020E620                 ; BAS2:  ecx - d[01F83530]   pointer -> offset
0042648C  mov  rcx, [022C6F28]          ; the pool singleton
00426493  mov  dword ptr [rcx+0x48830], eax
```

and **16 readers**. `BAS2` (`0020E620`) and `BASE` (`0020E600`, `ecx + q[01F83530]`) are inverses,
which is exactly why allocation passes the cell back through `BASE` before handing it to the record
initialiser. **So the round trip is a pointer stored in image-relative form so it survives a base
change** — not an index being resolved. Calling it an index invites a reconstruction to store a
small integer, and the `BASE`/`BAS2` pair then has no reason to exist.

**`+0x48828` is not an epoch.** It has two writers — the constructor (`00426C75`) and the reset
helper `0042ED30` (`0042ED53`) — and **both store the same immediate `0x3E2AAAAB`, which is
`0.16666667f` = 1/6**. It is read once, by promotion at `0042876A`, and copied into every promoted
record's `+0x414` (already in §5 as the tail block's `+0x28`). **It is a float tuning constant, and
"epoch" implies a generation counter — a lifetime mechanism this pool does not have here.**

### Added to the contract

- **The constructor's `+0x4881C` is `34.0f`** (`0x42080000`, `00426C60`), and **the store is a
  `qword`**: one instruction writes `34.0f` at `+0x4881C` **and zeroes `+0x48820`**. A
  reconstruction that stores only the float leaves `+0x48820` uninitialised. `+0x48824` is `4.0f`.
- **Release rewrites state rather than moving a record between lists.** `00429192`–`00429199` is
  `d[+0x284] = (d & ~4) | (1<<30)` — the retired bit cleared, bit 30 set — after `0042916F` sets
  `+0x290` bit 1, the same bit retire selects on.
- **Retire saves the successor before unlinking** (`00427CD4` re-read), so a corrupted `+4` cannot
  redirect the walk; an empty live list forces `nextFree = 0`, matching release's pending path.
- **Drain writes `w[c+6] = w[c+0xA] = -1` on every exit except the `parent == -1` fast path**,
  including the parent-free terminate and the `d284`-gated mid-chain exits.
- **The two handle clears are indexed, not scanned** — `HC1` computes `u8(ecx)*0xE0 + q[02B40528]`
  and `HC2` computes `u8(ecx)*0x70 + 02B3F570`, each verifying the id at a fixed offset before
  clearing. **The slot table is the same one `EXP-108` reads.**
- **`CLR` is a 1,208-byte default writer, not a memset** — a `0x740` clear followed by ~100 stores:
  `-1` sentinels, `1.0f` fields, `0x1000` array values, `0x2A0 = 0xF`, `0x2F4 = 0x03050303`,
  `b[0x4B7] = 0x20`, `b[0x66D] = 2`, and a `0x40`-byte constant struct copied from `01F204E0`.
  **A reconstruction that zero-fills a record produces a different record.** *(qualified 2026-10-02, OPUS: exactly 125 direct non-stack writes plus 47 composed helper writes; the `0x40`-byte block is copied twice, to `+0x180` and `+0x1C0`, a copy and not a zero fill, whose values hold only while that writable constant is unchanged; the vec4 helper writes four 4-byte scalars per call, 16 bytes per call, at `+0x210` and `+0x220`; the channel helper writes ten 8-byte entries `+0x4C0`..`+0x510` (loop bound 10); and a named fill zeroes `+0x580`..`+0x5D0`; render-clear-callee-footprints with FABLE's narrowing, accepted)*

### Unreachable is not dead

**Promotion's `prev.next` splice never fires during a clean drain** — each record's `+2` is already
`-1` when its unlink runs, because the previous iteration cleared it. `EXP-109` reaches it only by
planting a stale link. **So it is live error-handling for corrupt lists, not dead code**, and it
must be reimplemented even though no clean sequence executes it. The same distinction applies to
the boundary calls `EXP-112` found unreachable from its own entry point.

### Still open — routed, not answered

- **What the pointer in `+0x48830` points AT.** Its producer and its algebra are settled above; its
  *callers* are not — 16 readers use it and none of them was executed here. **This is the follow-up
  the request asked for, and it is now a narrower question than when it was asked.**
- **Whether any `PHOOK` implementation reads `+0x48818` bit 0.** The pin exists to protect a
  caller's bit across a callee that might change it; whether any shipped callee does is unmeasured.
  Semantics — **FABLE**.
- §14's open items are untouched by this pass.

*(OPUS 2026-09-19, on `REQ-OPUS-POOL-LIFECYCLE-FINDINGS` from SWE2-ORACLE. Each finding re-read from
the bytes; two cell names corrected and one formula's argument corrected.)*


## 21. The three-arm vector writer — [`EXP-118`](../_experiments/EXP-118-transform-vec-writer-exec.md), folded in 2026-09-19 (OPUS)

`003E5B30` (338 B) fills a `vec4` from a record and a field id. It has three arms, and **`EXP-118`
executed all of them**. Two of its findings are ABI hazards that a reconstruction will not
reproduce by accident.

### Arm 3's table pointer is a 32-BIT sum, sign-extended

```
003E5C0E  mov    rcx, qword ptr [rcx + 0x400]   ; the field table
003E5C15  test   rcx, rcx / je                  ; null      -> -1
003E5C1A  movzx  eax, word ptr [rcx + 0xc]      ; an offset word
003E5C1E  test   ax, ax / je                    ; zero      -> -1
003E5C23  movzx  eax, ax
003E5C26  add    eax, ecx                       ; 32-BIT ADD - the high half is discarded
003E5C28  movsxd rdx, eax                       ; ... then SIGN-EXTENDED back to 64
003E5C2B  je     0x3e5c65                       ; sum == 0  -> -1   (flags from the add)
```

**The table address is computed in 32 bits and sign-extended.** For any table whose low dword has
bit 31 set, `rdx` becomes a negative 64-bit value and the read goes nowhere near the table. This is
invisible in a 64-bit reimplementation that simply adds pointers — **it must be reproduced as a
32-bit truncating add if the addresses are ever to match**, and it is a standing constraint on
where this table may live.

The third `je` is easy to miss: it tests the flags of `add eax, ecx`, so **`table_low32 + off == 0`
is a third null arm**, distinct from the two explicit null tests above it.

### The field index is signed and unbounded

```
003E5C2D  mov  rcx, r8            ; r8 = the field id
003E5C30  add  rcx, rcx           ; *2
003E5C33  mov  eax, [rdx + rcx*8 + 4]     ; => rdx + field*16 + 4
```

`rcx*8` on a doubled field is **`field × 16`, with no bound check of any kind**. `EXP-118` drives
`field = -1` and reads `rdx − 16` — *before* the table. **The arithmetic is an index computation,
not a validated lookup**, and the only thing keeping it in range is the caller.

### Four outcomes in one return word

| return | meaning |
|---|---|
| `w[base+0x30]` | arm 1 — a real material tag |
| `0` | arm 2, whether or not it resolved |
| `w[rdx + field*16]` | arm 3 — a real row tag |
| `0xFFFFFFFF` (`003E5C71`, `or eax, -1`) | arm 3 found no table, no offset, or a zero sum |

So a caller **can** distinguish "no field table" (`-1`) from "went through the fallback" (`0`) from
a genuine tag — but only if it treats `0` as a value rather than as failure.

### Field `0xb` is its own path, and its fallback is graceful

`cmp r8d, 0xb` (`003E5B43`) splits the material arm off. It resolves four deep — record → gate,
codec and `T51` → object → selector byte and keyed scan → entry → `+0x70` → payload → `&3` → base
— **and every null along that chain hops to the `003E6DA0` fallback rather than failing.** All six
of `EXP-118`'s zero/negative cases produce the fallback's output. `d[ptr+4] & 3` selects the `+0x30`
or `+0x60` embedded vec block, and **modes 2 and 3 fall back too** — the mask is exactly `&3`,
which the `&7` mutant dies on. **Any field other than `0xb` never reaches that fallback at all.**

`G42` (`00422D50`) contributes one more: **its gate dword is both sentinel and argument** —
`d[+0xC4] == -1` short-circuits to `0`, and any other value is passed to `T51` verbatim as `edx`.

### The output's `w` lane is forced to `1.0f`

Every successful exit writes `mov dword ptr [rbx + 0xc], 0x3F800000` (`003E5BA8`, `003E5BE1`,
`003E5BFC`, `003E5C4F`, `003E5C67`). **This writer produces positions, never directions** — the
same invariant, and the same reason, as
[`CONTRACT-transform-primitives`](../00-Engine-Core-Runtime/CONTRACT-transform-primitives.md) §15b,
where the point transform ignores an incoming `w`. Here the `1.0f` genuinely *is* an immediate,
which is worth saying beside that section: **the two are not the same mechanism** even though they
produce the same value.

*(OPUS 2026-09-19, on `REQ-OPUS-TRANSFORM-VEC-WRITER-FINDINGS` from SWE2-ORACLE. The 32-bit sum,
the unbounded signed index and the `1.0f` stores re-read from the image.)*


## 22. The tails that were not deep — [`EXP-119`](../_experiments/EXP-119-t51-tail-resolvers-exec.md), folded in 2026-09-19 (OPUS)

§21's tree left two scripted boundaries, each carrying a ~85-instruction estimate since `EXP-109`.
**Both are trivial, and the residual they represented was an overestimate rather than an
undocumented subsystem:**

```
0051B9E0  jmp 0051F240                       ; 5 bytes. T51 is a THUNK.
00370E20  mov ecx, dword ptr [rcx + 0x94]    ; 11 bytes. E20 is a TRAMPOLINE.
00370E26  jmp 0020E600
```

`0051B9E0` is already named — `PresentationEntryReferenceContainer_ResolveEntryById` — and the real
body is `0051F240` (138 B). **So the `003E5B30` tree of §21 is now proven-real end to end**, with
no scripted boundary left in it.

**E20's offset is unsigned.** `mov ecx, [rcx+0x94]` is a 32-bit move and therefore zero-extends, so
E20 computes `BASE + u32(d[+0x94])` — *not* a signed add. One instruction, and it decides whether a
high offset wraps or reaches.

### What the real resolver does, and what it does not check

| | |
|---|---|
| **the mode is a SIGNED 2-bit field** | `shl r8d, 0x1e` then `sar r8d, 0x1e` (`0051F251`) — so `d[ctx+4] & 3 == 2` becomes `−2` and `3` becomes `−1`, and **both return 0**. Shifting by 31 instead would truncate mode 2 to `0` and let the body proceed, which is how the mutant dies |
| **the index is masked to 16 bits** | `movzx ecx, di` (`0051F266`, `0051F283`) — `idx = 0x10001` reads element 1 |
| **the null guard is on the ELEMENT, not the table** | a table resolving to `0` short-circuits **only when `idx == 0`**; any nonzero index still dereferences `idx * 48` and faults at `0x30`. **The resolver does not validate its inputs** |
| **the lazy write-back is sign-extended** | the `RES(hdl) + addend` sum is computed in `eax` and `movsxd`-ed to `rcx` (`0051F2B4`) before the store to `q[elem+0x18]`, so a negative addend stores `hres − n` as a signed qword |
| **the `RES` bound does not suppress the addend** | when the bound zeroes a handle, `0 + addend` still writes `addend`. **The bound zeroes the handle, not the sum** — so a clamped resolve produces a small non-zero pointer rather than a null one |

That last row is the one to carry into a reimplementation: **clamping a handle and clamping the
value written are different things here**, and the code does only the first.

*(OPUS 2026-09-19, on `REQ-OPUS-T51-TAIL-RESOLVERS-FINDINGS` from SWE2-ORACLE. Both thunk sizes,
the zero-extending `mov`, the `shl`/`sar` pair, the 16-bit mask and the `movsxd` re-read from the
image.)*

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Movement — CLIENT.** `Movement_ModifyHeadingSpeedForObjectState`, owned by that layer, calls `0051B9E0` on this page. That caller is a 427-byte per-object step over the **`0x740`-byte records at `[022C6F28]`**: a `-1` in `word[+0]` skips the record, and when bit 0 of `word[+0x62C]` is set it decays `float[+0x624]` by about `0.83` per step and clears that bit once the value falls below roughly `0.0625`; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**UI — CLIENT and SERVICE (SWE2-EC7 2026-09-18, 2 edges).** `0018EEE0`, a UI-filed
body, calls `0018F8F0` — one of the `0060E7A0` link-setter callers named below — and
is in turn called by `001F3300`, one of the `00609710` profile-guard callers; the
crossing is that the UI layer sits on both sides of the render-node helpers this
page's pool feeds — it consults them, it does not share ownership of them.
- **Input - CLIENT and SERVICE (17 edges).** `005CD4F0`, `005CD820` are called by bodies filed to Input: `0079C140`, `007A0340`; `001EC060`, MainLoop_UpdateAndRenderFrame (`0022B8C0`) reach bodies filed to Input: `0017DE60`, `00182D40`, `00249860`, `00249880` (+9 more) - shared machinery across the layer boundary, no shared ownership.
- **Party - CLIENT and SERVICE (4 edges).** PartyFocus_CommitPendingPackedActorHandle_Thunk (`00358BB0`) is called by bodies filed to Party: PartyRoster_AssignActorAndCommitFocusWhenEligible (`0050C610`); MainLoop_UpdateAndRenderFrame (`0022B8C0`), ActorManager_BindLoadedDefinitionPayload (`0026C8C0`) reach bodies filed to Party: PartyFocus_CommitPendingPackedActorHandle_Thunk (`00358BB0`), PartyFocus_GetCurrentPackedActorHandle (`003590D0`), PartyControl_SetMovementSuppressionBit (`00359200`) - shared machinery across the layer boundary, no shared ownership.
- **WorldAreaField - CLIENT and SERVICE (5 edges).** `0036A100` is called by bodies filed to WorldAreaField: `00267930`, `003319D0`, AreaArd_LoadOrUnloadFieldResource (`003EA820`); MainLoop_UpdateAndRenderFrame (`0022B8C0`), ActorManager_BindLoadedDefinitionPayload (`0026C8C0`) reach bodies filed to WorldAreaField: WorldPersistence_ResetBanksForFieldTransition (`0026DB30`), World_UpdateSimulationTick (`00314020`) - shared machinery across the layer boundary, no shared ownership.
- **CombatAction - MECHANICAL (2 edges).** both edges are combat-action bodies calling `PartyFocus_GetCurrentPackedActorHandle` (`003590D0`) - accessor fan-in.
- **Gameplay - MECHANICAL (1 edge).** the single edge is `0031ADB0` calling `PartyFocus_GetCurrentPackedActorHandle` (`003590D0`) - accessor fan-in.
- **Save_Load_Settings - CLIENT and SERVICE (3 edges).** `SaveLoad_ControllerLifecycleHandler` (`00582860`) calls `00182D40`, while `ActorManager_BindLoadedDefinitionPayload` (`0026C8C0`) and `WorldPersistence_ResetBanksForFieldTransition` (`0026DB30`) reach `SaveImage_GetPersistentPayloadBase` (`002EF2B0`).
- **Story_Event_Quest_Hunt - MECHANICAL and SERVICE (13 edges).** thirteen persistent-flag bodies (`PersistentFlag_Query*`/`PersistentFlag_Set*`, `0032A8A0`-`0032AD60` block) call `SaveImage_GetPersistentPayloadBase` (`002EF2B0`) - fan-in on the payload-base accessor; `ActorManager_BindLoadedDefinitionPayload` (`0026C8C0`) also reaches `EventMemory_QueryDefinitionIdAbsent` (`00377440`).

## The `00424D80` exclusive subtree — all 2 members bound (SWE2-FRONTIER, followup queue)

`00424D80` (1,607 B) — a render-record submit/validate body. `003AB7F0(r8)`
resolves the target, `-1` on null (`00424DB0`/`00424DBD`); `00420EA0(rbx,0)`
opens the record (`00424DCA`); `003E7D10` gates on `dword[rbx+0x6A4]` with
mode 3 (`00424DCF`/`00424DDA`). `004235C0` is called twice — once with
**mode 2** (the caller noted in the `+0xCE`/`+0xC8` selector discussion
above, `00424E0C`) — `esi` is compared against the `0x3009` and `0x203D`
command-type constants (`00424E15`/`00424F5B`), `word[+0xCC]`,
`dword[+0xC8]`/`+0xC4` `-1` sentinels, `byte[+0x5E]` bit 0, and
`movsx byte[+0x413]` vs `word[rdi+0x31A]` all feed the verdict
(`00424E22`–`00424F32`); failures clear bit 6 of `byte[+0x4B7]`
(`00424F63`/`00424FB2`).

| member | role | interior |
| --- | --- | --- |
| `00372510` (131 B) | scratch-row accessor — `0020E600(dword[rcx+0x84])` then indexes by `movsx word[+0x88] * 0x292` (`0037251D`/`00372536`) and a second `0020E600(dword[rdi+0x18])` (`00372540`) | [`00372536`](../_index/ADDRESS-INDEX.md) |
| `00409FD0` (15 B) | callback thunk — binds `rdx = &0040A200`, tail `jmp 0051FE30` (`00409FD3`/`00409FDA`) | [`00409FDA`](../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `003AB7F0`, `00420EA0`, `003E7D10`,
`004235C0`, `00422D10`, `00409090`, `00409210`, `0020E600`, `0051B9E0`,
`0041C760`, `0051FE30`.

## The `00424550` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`00424550` (~135 B) — five-register render-pool body
(`00424550`/`00424555`).

| member | role | interior |
| --- | --- | --- |
| `0041D4D0` | `edx == 0` gate, `or dword[+0xC], 0x1000` flag set (`0041D4D5`/`0041D4D9`) | [`0041D4D5`](../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none.

## Crossings into other layers — FINAL-AUDIT pass 22

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`.*

- **ActorEntity — CLIENT.** `002EBC30` on this page — the keyed setter that writes `xmm0` to
  `[022C6F28]+0x4881C` (`002EBC30`–`002EBC3F`) — is called by the ActorEntity body `0026C8C0`:
  the actor layer publishes a float into the render-record pool. (edge: `edges.tsv`)

**Resource — SERVICE.** The free chain `0041E500`/`0046E3E0`/`00478030`/`0042DA30` all reach `0051FF30`, and `0042DA30` also calls `00409660`/`00409F50`, on the resource layer — record teardown delegates storage back to it.

**Script VM — CLIENT.** `0050DDA0` on the script bridge calls `00369800`.
## Interior citation — frontier hub `00422D50` (2026-09-18, SWE2-EC7)

`00422D50` — 57 B, 22 callers (5 A-measured);
`CharacterRenderRecord_ResolveActive…`-shaped — the handle-to-record leg of this contract.
Interior verified: `[rcx+0xC4] == -1` is the empty check returning 0 (`00422D56`–`00422D64`);
else `[rcx+0x10]` is the image handle resolved by `0020E600`
([`00422D6D`](../_index/ADDRESS-INDEX.md)), the resolved object's `[+0xDA8]` member is the live
pool, and `0051B9E0(pool, [+0xC4])` runs the indexed fetch at `00422D84`. Sentinel `-1` means
"no active record", not "record zero".


### Interior citation — frontier hub `003E7D10` (2026-09-18, SWE2-EC7)

`003E7D10` — 53 B, 9 callers: the `02B59D80` record-field getter the pool
readers call. `byte 02B59D71` gates the read; `ecx == -1` or a zero
`word[row]` return 0; the record sits at `ecx * 0x150` off the base
([`003E7D24`](../_index/ADDRESS-INDEX.md)) and the answer is
`dword[row + edx*4 + 0xC0]` — an indexed array-of-fields read inside each
record.
## SWE2-EC7-20 update (2026-09-18) — render-zone fragment set: `0060E7A0`, `0060CE50`, `00609710`, `0051FF30`, `0051F9F0`

`0060E7A0` (98 B) is a bounded block append: `r8 == 0` returns 1 (`0060E7AD`);
else `r8w = word[rdx+0x12] & 0x1FFF` is the source length and `dx =
word[rdx+0x10]` the running offset — `r8w + dx > dword[rcx]` or `dx < 4`
returns 3 (`0060E7BC`..`0060E7E7`); on pass `00861EBA` copies `r8w` bytes from
`r9` to `rcx + dx` (`0060E7E9`..`0060E7F6`) and returns 0. The capacity-checked
record append the pool's writers share. Callers `0018F8F0`/`001F5D70`/`001F8D10`/
`00604750`/`006515C0`/`00659EC0`/`0065CD60` — the Phyre render-node zone this
contract's pool feeds.

`0060CE50` (827 B) is a render-record transform commit: it stores `rdx` into
`[rcx+0xA8]` (`0060CE6C`), then stages a sixteen-float block — when
`[rdx+0xB0]` is non-null its 0x2C-byte record copies verbatim into the rbp
frame with three dword zeroes and 1.0f at `+0x47` (`0060CE7C`..`0060CF12`);
otherwise `rdx`'s inline block copies first, `00185AF0` runs over the frame
(`0060CFBF`), and its 0x40-byte result is shuffled back lane-wise
(`movups`/`shufps 0x55`/`0xAA`/`0xFF`, `0060CFC4`..`0060D06A`). The staged
block is then copied dword-wise into `[rbx+0xB0]` (`0060D06F` onward). The
matrix/parameter publish the record pool's descriptors carry. Callers
`00187950`/`001B76E0`/`001E2AF0`/`001F06D0`/`001F3930`.

`00609710` (7 B) is the low-bit flag getter the render calls gate on
(`FUN_00609710(ctx) != 0` → profile slot arm): its whole body is
`eax = dword[rcx+8] & 1; ret` (`00609710`..`00609716`). Seventeen callers —
`00186130`/`00186410`/`00187950`/`00191560`/`001F28B0`/`001F2A20`/`001F2B70`/
`001F2C50`/`001F2D40`/`001F2E40`/`001F3090`/`001F3210`/`001F3260`/`001F3300`/
`001F3440`/`001F3740`/`00212F70`.

`0051FF30` (217 B) is a callback-driven index-list walker: `edi = dword[rcx+0x40]`
is the head index, `-1` exits (`0051FF39`..`0051FF45`); per step it resolves
`r14/rbp = [rbx+0x38] + edi*16` through the `003AB7F0` lazy-pointer fix-up on
`+0x30` (`0051FF60`..`0051FF99`), computes `esi = edi >> [rbx+0x4C]`, resolves
`rax = [rbx+0x10] + esi*32` and `0020E600([rax+0x10])` for the segment base
(`0051FF9E`..`0051FFC5`), and builds `rcx = ([rbp]==-1) ? 0 : rdx +
(edi & [rbx+0x50]) * [rbx+0x48]` — the per-element address — before `call r15`
(`0051FFC5`..`0051FFE1`). `edi = [r14+8]` advances (`0051FFE4`). The for-each
the pool's refresh pass drives. Callers `00409F70`/`0046E3E0`/`00478030` — the
descriptor-container owners.

`0051F9F0` (380 B) is the pool-descriptor initializer: it clears the 0x5C-byte
header — `-1` qwords at `+0x18`/`+0x40`, `+0x48 = edx`, `+0x4C = r8d` (the
shift), `+0x50 = (1<<r8)−1`, `+0x54 = (1<<r8)*r14d` (`0051FA11`..`0051FAA6`) —
then fills the caller's `[rsp+0x50]` table with `r14d` `{-1,-1,0}` 0x20-byte
rows (`0051FA55`..`0051FA7A`) and the `[rsp+0x58]` table with `+0x54`
`{-1,-1,0020E600(0)}` 0x10-byte rows (`0051FAB5`..`0051FAE1`). `0036C1D0(6)` +
`0036A100((1<<r8)*edx)` + `0036C140()` size and allocate the element store into
`+0x28` (`0051FAE3`..`0051FB0C`), a third loop back-fills each `+0x10`-table
entry's base via `0020E620(rbp + stride*i)` (`0051FB20`..`0051FB44`), and
`0051F6B0` post-init runs before `[rbx] |= 1` marks it live
(`0051FB46`/`0051FB4E`). Callers `00409F10`/`0046E250`/`00477EE0`.

## SWE2-EC7-21 update (2026-09-18) — `001823B0` mod-4 index arm + `0041C760` fragment

`001823B0` (46 B) is a retry-once resolve-and-forward: `0018CA40()` runs first
(`001823B4`); a null result exits (`001823B9`..`001823DD`), else
`dword[01F7F538] = 0` clears the error slot (`001823BE`), `0018CA40()` runs a
second time (`001823C8`), and the fresh pointer forwards into `0018BE70`
(`001823CD`..`001823D4`). The double-probe re-acquire the render-command
builders run before submit. Callers `001EC060`/`001FBE50`/`0022B0B0`/`0022B8C0`
— the render-command builders this contract's pool feeds.

`0041C760` (14 B) is a single-field bit read: `eax = dword[rcx+0x2C8]`, shifted
right 12 and masked to bit 0 (`0041C760`..`0041C76C`) — returns bit 20 of the
record's `+0x2C8` flags. Callers `00422A30`/`004232D0`/`00424230`/`00424D80` —
including this contract's `00424D80` submit/validate body.

**Party — SERVICE (SWE2-EC7 2026-09-18, 1 edge).** `0022B8C0` — one of the
`001823B0` index-math callers this section names — calls `00358BB0`, a
Party-filed body. The pool's command-index path reaches into the party layer;
the crossing is that this contract's caller consults that layer, not that the
pool shares ownership of it.

## SWE2-EC7-22 update (2026-09-18) — `00409090` global-chain key lookup

`00409090` (53 B) is the chain-walk lookup over the `[01EFF940]` global list:
`rax = [01EFF940]`, `rdx` walks `+8` links, `[rcx]` key compared against each
node's `[rax]` head — the bucket-chain find the pool's render-record
registrations run. Interior anchor `004090A3` (the key load). Three callers —
`00409660`-zone registration arms.

## SWE2-EC7-33 update (2026-09-19) - `00604750`

`00604750` (7,713 B) is the render-node zone's frame builder: stack-cookie prologue, `005DC580`/`005DC430` frame ctors, a nine-float parameter block at `rbp+0x7AC` (1.0, -0.91, 0.5, 0.5, 11.0, 7.0), then a `005CD4F0`-locked `005EB670` slot walk with `0062C300`/`0060E7A0` mid-pass and a `005CD820` release. Interior anchor `00604C06` (a `005EB670` slot call).

## SWE2-EC7-37 update (2026-09-19) - `0042F4C0`

`0042F4C0` (509 B) is one of the eleven scripted record callees the contract names - `022C6F28`, `00426EC0` pair plus `003E5CF0`/`0042F310`/`003326C0`/`004288B0`/`00421B00`/`003E55B0`. Interior anchor `0042F506` (an `003E5CF0` call).

## SWE2-EC7-41 update (2026-09-19) - `004200A0`

`004200A0` (331 B) is a render-pool body - `0046C240`/`0041E860`/`003AEF30`/`003E69A0`/`00512C80`/`0024CFF0`/`0017F100`/`0019C570`. Interior anchor `004200B4` (a `0046C240` call).

## SWE2-EC7-42 update (2026-09-19) - `00185AF0`

`00185AF0` (297 B) is a render-record body - `001871B0` single call. Interior anchor `00185B80` (the `001871B0` call).

## SWE2-EC7-43 update (2026-09-19) - `003AF340`

`003AF340` (276 B) is a render-record-pool body - `022C6F28`/`02B3F550`/`02B3F570`, `003E6E40` single call. Interior anchor `003AF3B0` (the `003E6E40` call).

## SWE2-EC7-44 update (2026-09-19) - `0041CB90`

`0041CB90` (269 B) is a call-free defaults writer - `+0x324`/`+0`/`+4`/`+8`/`+0x318`/`+0x2D8`/`+0x338`/`+0x35C`/`+0x360` = -1, `+0x340` = `[01DFE0BC]` x 30.0f (`008F8D80`), `+0x344`/`+0x348`/`+0x34C` = -1.0f, `+0x358` = 0x10. Interior anchor `0041CC36` (the `01DFE0BC` float load).

## SWE2-EC7-45 update (2026-09-19) - `0051FE30`

`0051FE30` (242 B) is the record-pool callback body - `0020E600`/`003AB7F0` plus a `call r12` register call. Interior anchor `0051FE6C` (a `0020E600` call).

## SWE2-EC7-45 update (2026-09-19) - `0051F6B0`

`0051F6B0` (236 B) is a body - `003AB7F0` single call. Interior anchor `0051F6FD` (the `003AB7F0` call).

## SWE2-EC7-47 update (2026-09-19) - `00426340`

`00426340` (211 B) is the per-frame walker's state-gated callee - `003AFD00`/`003B5980`/`003B6900`/`003B6B80`. Interior anchor `00426358` (an `003AFD00` call).

## SWE2-EC7-47 update (2026-09-19) - `00425FB0`

`00425FB0` (219 B) is a body - `0042EF90` plus `call r14`/`call rbp` register calls. Interior anchor `0042600C` (the `0042EF90` call).

## SWE2-EC7-47 update (2026-09-19) - `00426EC0`

`00426EC0` (216 B) is a call-free `0x740`-stride animation-object link fixer - `word[rdx+6]` index, `+0x284`-nonzero `cmove` gate, `word[rcx+8]` vs `word[rdx]` compare, `-1` relink writes. Interior anchor `00426ED1` (the `022C6F28` table load).

## SWE2-EC7-48 update (2026-09-19) - `0051F080`

`0051F080` (198 B) is a record-pool sibling - `003AB7F0`/`0051F380`/`0051F410`. Interior anchor `0051F09F` (a `003AB7F0` call).

## SWE2-EC7-52 update (2026-09-19) - `001871B0`

`001871B0` (673 B) is a call-free 3x3 cofactor expander - `mulss`/`subss` pairs across `[rdx]`/`[+0x10]`/`[+0x20]` rows write a four-row `movups` result to `[rcx]`. Interior anchor `0018722F` (the first cofactor difference).

## SWE2-EC7-53 update (2026-09-19) - `00421B00`

`00421B00` (450 B) is a render-record-pool body - `0020E600`/`002ED570`/`003B30A0`/`003E5CF0`/`004209A0`/`0046E300`/`0046E370` plus `022C6F28`. Interior anchor `00421B15` (a `0020E600` call).

## SWE2-EC7-54 update (2026-09-19) - `005EB670`

`005EB670` (321 B) is a call-free 4x4 matrix transpose - `[rdx]`/`+0x10`/`+0x20`/`+0x30` rows published column-wise into `[rcx]`. Interior anchor `005EB6CE` (the `+0xC` store).

## SWE2-EC7-55 update (2026-09-19) - `0041E860`

`0041E860` (252 B) is a render-pool body - `0020E600`/`003B3300`/`00422C20`/`0042F190`/`0046E2B0`/`00477640`/`00478070`/`0051BC10`. Interior anchor `0041E881` (a `0042F190` call).

## SWE2-EC7-57 update (2026-09-19) - `0051F410`

`0051F410` (176 B) is the admission-accounting body the render-pool contract names - `003AB7F0` single call. Interior anchor `0051F47B` (a `003AB7F0` call).

## SWE2-EC7-58 update (2026-09-19) - `004232D0`

`004232D0` (170 B) is a render-record probe the pool contract names - `0020E600`/`0041C760`/`0051B9E0`. Interior anchor `004232F2` (a `0020E600` call).

## SWE2-EC7-61 update (2026-09-19) - `003B3300`

`003B3300` (151 B) is a render-pool body - `0024EE60` single call plus `02EBD480`/`02EBDB98`/`02EBDBA0`/`02EBDBA8`. Interior anchor `003B3326` (a `0024EE60` call).



## SWE2-EC7-64 update (2026-09-19) - `0051F380`

`0051F380` (141 B) is a record-pool sibling - `003AB7F0` single call. Interior anchor `0051F3BB` (a `003AB7F0` call).


## SWE2-EC7-70 update (2026-09-19) - `004780B0` sign-extend trampoline measured

`004780B0` (8 B) is the widen trampoline the `003E55B0` resolve chain tails
through: `movsx edx, dx` sign-extends the slot selector, then `jmp
002ED570` - the `[+0xDA0]`-table indexer `003E6DA0` also calls.
Interior anchor `004780B3` (the `jmp 002ED570`).

## SWE2-EC7-70 update (2026-09-19) - `003E6DA0` fallback chain measured

`003E6DA0` (67 B) measured - the CONTRACT's "null along the chain hops to
the `003E6DA0` fallback" is exact: `dword[+0x18] == -1` returns NULL;
otherwise it resolves `+0x10` through `0020E600`, indexes `[rax+0xDA0]` by
the `+0x18` selector through `002ED570`, and when that lands non-NULL tails
`00370E20` on the record. Any miss returns NULL.
Interior anchor `003E6DBB` (the `[rax+0xDA0]` table load).

## SWE2-EC7-71 update (2026-09-19) - `003E55B0` `CharacterRenderRecord_ResolveModelInstance` measured

Measured on `the-character-render-record-array.md` (PARTIAL -
non-bearing); mirrored here on the lifecycle CONTRACT.

`003E55B0` (53 B) is the resolver the array page names, read from the
image: `word[rcx+0x64]` is the model-instance selector - `-1` returns
NULL with no work; otherwise `0020E600(dword[rcx+0x10])` resolves the
record's context object and `qword[rax+0xDA0]` is its instance table,
handed with the selector word to `004780B0` by tail jump.
Interior anchor `003E55CB` (the `0020E600` context resolve).

## SWE2-EC7-72 update (2026-09-19) - `0051BA40` pop-with-value measured

`0051BA40` (55 B) is the pop the record-pool bodies call:
`0051F240(rcx)` resolves the top entry; when present it saves
`ebx = [entry]`, runs `0041CF00(entry)` (the release), and returns the
saved dword through `0051F190(rcx, ebx)` - the take-and-free pair.
Interior anchor `0051BA5D` (the `0041CF00` release call).

## SWE2-EC7-73 update (2026-09-19) - `003E5AD0` word-field getter measured

`003E5AD0` (88 B) is the word getter the pool bodies call: `r8 =
[+0x400]` must be non-NULL; `edx < 0x20` returns
`word[(r8 + word[r8+2]) + edx*2 + 0x14C]`; `edx` `0x104`/`0x105`/`0x106`
returns `word[r8+0x3A]`/`[+0x3C]`/`[+0x3E]`; anything else `0xFFFF` -
the record's dual-range field read.
Interior anchor `003E5AEF` (the `+0x14C` indexed read).

## SWE2-EC7-82 update (2026-09-20) - `0051F190` pool-element release measured

`0051F190` (163 B) is the element free the pool callers run:
`[rcx+4]` folded `<< 30 >> 30` picks the base - arm 1 uses `[rdi+8]`
directly, arm 0 resolves `[rcx+8]` through `003AB7F0`, other values
skip the fetch - `dx` selects a 48-stride element, `0051F4C0(rdi, dx)`
runs, then the 0x28-byte record is cleared (0 / -1 fills) and
`[rdi+0x14]` decrements, clearing `[rdi+0x18]` when it empties.
Interior anchor `0051F1DB` (the `003AB7F0` resolve).

## SWE2-EC7-84 update (2026-09-20) - `00409210` + `00421FF0` measured

`00409210` (46 B) is the 0x20-block record init the pool callers run:
`[rcx]`/`+8`/`+0x10`/`+0x18` zero, the handler pointer at `008BCF70`
runs (`r8d = 0x20`), and `byte[rcx+0x1F]` goes 0 - a fixed-layout
constructor with the register callback folded in.
Interior anchor `0040922E` (the indirect handler call).

`00421FF0` (85 B) is the `[rax+0xD98]`-path record fetch the pool
callers share with `00422170`: `[rcx+0x18]` != -1 gates
`0020E600([rcx+0x10])`, `[rax+0xD98]` + `002ED570(edx)` resolve the
record, and a live one tails into `00370F60(rec, edx)` - 0 on every
dead path.
Interior anchor `00422033` (the `00370F60` tail).

## SWE2-EC7-85 update (2026-09-20) - `0041CF00` + `0041CEC0` measured

`0041CF00` (192 B) is the element-table init the pool callers run:
`word[rbx+0x28]` entries at 0xA0 stride from `+0x30` each take
`-1`/`cx`/zeroed qwords/`0x1E0000`/`30.0f`/`0xFF7F`-masked flags;
then `+0xC` bit `0x1000` runs `002ED570([+0x338] via +0x330)` ->
`00372280` and clears, before tail `0041CB90`.
Interior anchor `0041CFBB` (the `0041CB90` tail).

`0041CEC0` (63 B) is the callback-plus-flag the same callers run:
when the global handler pointer is live it runs
`handler([rcx+0x2C0], rcx+0x31C)`, and `+0xC` gains `0x200` either
way.
Interior anchor `0041CEE3` (the indirect `call rax`).

## SWE2-EC7-86 update (2026-09-20) - `00372280` indexed record reset measured

`00372280` (194 B) is the per-index element reset the pool callers
run: `0020E600([rbx+0x84])` twice yields the record base and the
s16 index list at `word[rbx+0x88]*0x290`; for each of
`word[rbx+0x8a]` entries the indexed 0x290-stride record takes
`word[+0x280] &= ~0x10`, `+0x1A0`/`+0x1A4` zeroed with `+0x1AC` =
1.0f, and `+0x1C0`/`+0x1C4` zeroed with `+0x1CC` = 1.0f - two
vec4-style slots re-armed per element.
Interior anchor `003722F4` (the `+0x280` flag clear).

## SWE2-EC7-87 update (2026-09-20) - `003E18D0` mode-select forward measured

`003E18D0` (119 B) is the mode-select the pool callers run: a
`0020E600([rdi])` resolve must be live; when `[02B59D64]` is set
the mode is forced to 4, otherwise an `edx == 4` request is
re-decoded through the record's `byte[+0x1A]` (== 4 yields 2);
`0040B5D0(record, mode)` then runs and a nonzero return writes
`word[rdi+0x60] = 0x1E`.
Interior anchor `003E192A` (the `0040B5D0` call).

## SWE2-EC7-97 update (2026-09-20) - `002EF250` + `002EF030` measured

`002EF250` (64 B) is the two-resolve bit writer `001EBC70` and
`001EC060` call: `003EC580(movsx cx)` then `00422D50` must both
return non-null, then `edx` sets or clears `0x800000` at
`[rax+0xC]` - the record flag the pool lifecycle toggles.
Interior anchor `002EF268` (the `00422D50` call).

`002EF030` (32 B) is the two-global mode check `001EC060` and
`0022BEB0` call: `dword[01EEBAA8] == 8` and `dword[01EEBAAC] ==
dword[02164204]` together yield 1, anything else 0 - the paired
counter comparison the lifecycle consults.
Interior anchor `002EF03F` (the second compare).

## SWE2-EC7-110 update (2026-09-20) - `001AC6F0` measured

`001AC6F0` (45 B) is the
indexed float read `001E2AF0`
and `001E6480` run: negative
`edx` answers 0.0, else
`qword[rcx + 0xE8]` is the
vector head and `(end -
begin) / 8` bounds the index;
`qword[begin + edx * 8]` is
the record pointer and `movss`
returns its `+0x2C` float.
Out-of-range answers
`xorps` 0.0 rather than
trapping.
Interior anchor `001AC70F`
(the indexed record fetch).

## SWE2-EC7-111 update (2026-09-20) - `001868F0` measured

`001868F0` (20 B) is the
two-slot select `0018EEE0`
and `001F2A20` run: `dl`
nonzero answers
`qword[+0xB28]`, zero
answers `qword[+0xB30]` -
the adjacent-pair pick the
pool record uses for its two
roles.
Interior anchor `001868F4`
(the `+0xB28` read).

`00185A80` (7 B) is the
accumulator `001E2AF0` and
`001F5D70` run:
`dword[rcx + 0xDBC] += edx` -
the running total the pool
keeps on the record.
Interior anchor `00185A86`
(the tail after the `+0xDBC`
accumulate).

`002ED570` (146 B) is the indexed record resolver the pool's callers share: lazily resolves `obj+0x30` to `+0x38` and `obj+8` to `+0x10` via `003AB7F0`; `edx` splits `idx*16` into the `+0x38` table and `idx >> [+0x4C]` selects the `*32` row in `+0x10` whose `dword[+0x10]` resolves through `0020E600`; a `dword[idx*16 record]` of `-1` yields `0`, else `(+0x50 & idx) * +0x48 + resolved` - the pool's two-table locator with the sentinel-null arm.

Interior anchor `002ED5CE` (function `002ED570`).

`00409F50` (17 B) is the sign-extending entry into `002ED570`: `dx == -1` returns `0`, else `movsx edx, dx` and tail-jump - the u16-index guard the effect callers take.

Interior anchor `00409F5C` (function `00409F50`).

`00409FA0` (35 B) is the pool-enumerate caller the render family enters through `0051FE30`: packs `edx`/`r8` into the `rsp+0x20` arg block and supplies `rdx = 0040A1E0` as the per-record callback - the bounded apply-over-records entry beside `00409F50`.

Interior anchor `00409FB9` (function `00409FA0`).

`00332660` (91 B) is the second six-slot stage binder beside `00332590`: `022C6F20` gets `&022C6F30`, `00369CF0(6)` enters the stage and a nonzero answer runs `0041E500(&022C6F30)` / `00426950()` / `003697C0(6)`; the tail then calls `004262E0(qword[022C6F28])` and falls through `jmp 0042ED60` - the paired binder on the same six-slot lifecycle.

Interior anchor `0033268D` (function `00332660`).

`00409A30` (33 B) is the out-param shim into the `00409780` pool query: forwards `(rcx, rdx, r8, r9)` with `r9 = &rsp+0x30` and a fifth stack slot `&rsp+0x68`, then returns `dword[rsp+0x68]` - the pool lookup's last-field read the adm/animation callers wrap.

Interior anchor `00409A43` (function `00409A30`).

`0041CA70` (283 B) is the render-record rebind a caller runs after a swap: when `byte[+0xC] & 0x20` is clear and `word[+0x318] != -1`, `qword[+0x310]` resolves through `00409F50`, `004096C0(row, dword[+0x320])` and `004090D0(row, sx word[+0x31A], word[+0x31C] & 0xFFF)` rebuild the row into `qword[+0x368]`/`+0x370`; then `qword[+0x18] = this+0x30 + dword[+0x20]*0xA0` computes the row-array end and `esi < word[+0x28]` walks 0xA0-stride rows from `+0x80`, re-resolving `qword[row-8]` through `00409F50`/`004096C0`/`00408F80` into `row+0x20`/`row+0x28` whenever `word[row-0x46] == 1` and `word[row] != -1` - the pool's rebind-all pass.

Interior anchor `0041CB10` (function `0041CA70`).

`003AB7C0` (36 B) is the alignment dispatch: a null `rcx` returns, `cl & 3` nonzero tail-jumps `00369800`, and aligned pointers tail-jump `003697F0` - the free-path split by pointer alignment the render-pool and resource-owner callers share.

Interior anchor `003AB7D9` (function `003AB7C0`).

`0041E500` (76 B) is the guarded record teardown: `byte[02B62E10]` sets as the re-entry flag, `00409F70` runs on `qword[+0xD90]`, the flag clears, then `0046E3E0` on `+0xD98`, `0051B9F0` on `+0xDA8` and a `00478030` tail on `+0xDA0` - the four-link free chain the frame and render-pool callers share.

Interior anchor `0041E517` (function `0041E500`).

`00426950` (78 B) is the `022C6F28` chain drain: `dword[+0x48800]` heads the id chain, each id indexes a `0x740`-stride record that gets `0042DA30`, and `movsx word[+4]` links to the next until -1 - the teardown walk the frame and render-pool callers share.

Interior anchor `0042697E` (function `00426950`).

`0042DA30` (466 B) is the deferred field populate `00426950` calls once the pool slot's `[rcx+0x284]` bit 4 is set: the `+0x408` word selects a `00409F50` section of the `[rcx+0x10]` object's `+0xD90` table, `00409660` finds its `'@FCP'` (`0x50434640`) block and `+0x400` caches the element at `index+0x30`; through `00422D50` the three offset fields `+0x68`, `+0xD8` and `+0xF0` are resolved by `0020E600`/`003AB7F0` pairs into `+0x69C`/`+0xE0`/`+0xF8` with the `+0xE8`/`+0x100` biases published at `+0x558`/`+0x560`, the no-object arm zeroes the whole set (`+0x69C` via `0020E620(0)`), and `+0x42C`/`+0x430` get the same resolve-or-zero pass - the fixup the pool lifecycle expects before the record goes live.

Interior anchor `0042DB2E` (function `0042DA30`).

`003E47C0` (200 B) is the two-record blend `0042C410` runs: `00421E20` fetches kind-6 into `rsp+0x20` and kind-7 into `rsp+0x60`, `0046D340` lays `[rbx+0x180]` into `rsp+0xA0`, two `0046D350` combines fold the rows together, and bit 0 of `[rbx+0x418]` becomes whether the kind-6 lane's `+0x38` float exceeds the kind-7 lane's

Interior anchor `003E4835` (function `003E47C0`).

`0051F4C0` (180 B) is the slot splice `0051F190` runs when freeing an index: `[rcx+0x10]` unset yields a null base, else the low two bits of `[rcx+4]` select the `0x30`-stride table - `1` uses `[rbx+8]` directly, `0` goes through `003AB7F0`; entry `r8 = base + di*0x30` is unlinked by stitching its `+8`/`+0xC` index neighbours (each `0x30`-scaled, `-1`-terminated), `[rbx+0x1C]`/`[rbx+0x20]` head fields pointing at `di` are re-pointed at the entry's own links, and the entry's link qword is cleared to `-1`

Interior anchor `0051F528` (function `0051F4C0`).

`0042ED60` (162 B) is the pool teardown `00332660` runs: `022C6F28` mirrors into `02EBB740` with `02EBB748` zeroed, `+0x48818` bit `0x20` clears around `00427C90`/`00428710`; when the bit was set it resolves `0020E600([+0x48830])` for `0041E500` and walks the `+0x48800`-seeded chain of `0x740` rows (`+4` word `-1` ends) through `0042DA30`, then `003697C0(6)`, `00427DE0(1)` and tail `00427BD0`

Interior anchor `0042EDCE` (function `0042ED60`).

`00427BD0` (185 B) is the `022C6F28` row sweep `0042ED60` runs: it follows the `[+0x48800]`-indexed `0x740`-row chain (`[rbx+4]` links), and for each `[rbx+6] == -1` row with `[+0x294]` bit `0x19` set it clears the bit, `00420A40`s the row, resolves `[rbx+0x18]` through `0020E600`/`[+0xD98]`/`002ED570` for a `00373030` call on `[rbx+0x180]`, then `00428E70`s the row

Interior anchor `00427C22` (function `00427BD0`).

`00428E70` (152 B) is the two-link row walk `00427BD0` and `00427DE0` run on the `022C6F28` table: `word[rcx]` resolves to its `0x740`-stride row through `0042E550`, the row's `word[+8]` link gets the same resolve-and-apply, and the row's `+8`/`+0xA` chains are then iterated by `0042EF90` with `0042E550` as the per-node proc - a nested two-deep visit over the pool's linked rows.

Interior anchor `00428E9F` (function `00428E70`).

`003E73B0` (155 B) is the two-bit mode setter `00427DE0` runs on a pool record: `byte[+0xC0]` bits 3-4 compared against `edx`, and on a change `00422D50(rcx)` resolves the peer object; mode `0` releases a live `[+0x118]` through `003AFBE0`, mode `1` lazily allocates it through `003AF340(movsx word[rbx])`, the cached value is mirrored into `[rsi+0x360]`, then the mode bits are rewritten - alloc-on-promote, free-on-clear.

Interior anchor `003E73D5` (function `003E73B0`).

`003AFBE0` (35 B) is the `02B3F570` slot release `003E73B0` (mode-0 arm) and `00427C90` call, matching this page's existing note: `slot = 02B3F570 + cl*0x70`, and only when `dword[slot+4] == ecx` is the tag word cleared to `0` (`cmovne` nulls the pointer otherwise) - a tag-checked dealloc on the 32-slot `0x70` table.

Interior anchor `003AFBFF` (function `003AFBE0`).

`0042E550` (192 B) is the pair-resolve `00428E70` runs per visited row: `dword[rcx+0x18]` (or the `-1` sentinel) resolves through `0020E600([rcx+0x10])` then `002ED570([rax+0xD98], id)` into `rdi`; `word[rcx+6]` picks a second `022C6F28` `0x740`-row (live-gated on `dword[+0x284]`), resolved the same way into `rbx`; when `rdi` is non-null `00373F40(rdi, rbx)` applies the pair and `004242B0(rsi)` closes out - the two-hop lookup the row walk delegates to.

Interior anchor `0042E5F3` (function `0042E550`).

## Interior citations for the entry-cited functions (OPUS, 2026-10-03, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../_index/candidates/opus-contract-render-record-pool-lifecycle-ee-1003/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `0018BE70` | 144 B | allocates 0x18 bytes with `0085E730(0x18, 0, -1)` and, when that is non-null, constructs `o` = `001F19E0(it)` (else `o` = 0); appends `o` to the pointer vector `v` = `rcx`: when end qword `[v+8]` is below capacity qword `[v+0x10]` it advances the end by 8 and stores `o` at the old end (unless that end is null), otherwise calls `001AB570(v, end, &o)` and re-reads `o`; then tail-jumps to `0018AFF0(0018B4E0(), o)` | `0018BE90`, `0018BEA7`, `0018BEC6`, `0018BEDC`, `0018BEFB` |
| `0065CD60` | 1181 B | copies values of `o` = `rcx` into the buffer `B` = qword `[qword [o+0x58]+8]` (re-read per item) through descriptor qwords `+0x210`..`+0x278`, skipping null ones; a copy goes to `B` + word `[d+0x10]`, (word `[d+0x12]` AND 0x1FFF) bytes by `memcpy` `00861EBA`, and returns 3 when offset + length exceeds dword `[B]` (unsigned) or the offset is below 4; with `f` = float `[o+0x84]` and `a` = (1.0 - float `+0x88`) * `f`, the sources are: `+0x210` `a`, `+0x218` `a`*`a`, `+0x220` `f`, `+0x228` `f`*`f`, `+0x230`/`+0x238`/`+0x240`/`+0x248`/`+0x250` the bytes at `o`+0x8C/+0x90/+0xA0/+0xB0/+0xC0 (1 returned if that address is null), and `+0x270` the four floats (`[o+0xDC]`, `[o+0xE0]`, `[o+0xE0]` - `[o+0xDC]`, 1.0 / that difference); for `+0x258`, `+0x260`, `+0x268` and `+0x278` it returns `0060E7A0(B, d, o+0xC4 / +0xC8 / +0xCC / +0xE4)` when non-zero; returns 0 after the last | `0065CDD6`, `0065CDF8`, `0065CF1E`, `0065D0DC`, `0065D180` |

## Homed frontier bodies called from this page's functions (FABLE, 2026-10-03, cloud-drafted)

*Functions no page cited until now. Each is entered directly from a function this page already cites (the site is given as caller + offset). Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's homing pack and re-read by FABLE against the certified image; verified by [`homing_applier.py`](../_index/candidates/fable-home-contract-render-record-pool-lifecycle-1003/homing_applier.py): every site transfers to its function, the page cites the caller, and every anchor is an instruction boundary inside its function that decodes to the recorded mnemonic.*

| function | size | entered from | what the body does | interior anchors |
|---|---|---|---|---|
| `00370890` | 777 B | `0046E300` + 0x39 | when `rdx` is non-null and dword `rdx+0x10` equals dword `rcx+4`, sets it to -1 and, for each of the signed word `rdx+0x8a` word indices `j` at `B` + signed word `rdx+0x88`*0x290, `B` = `0020E600(dword rdx+0x84)`, when `0020E600` of dword `+0x278` of record `B` + `j`*0x290 is non-null stores `00370890` + 0x9F(0) there and -1 at word `+0x27c`; then stores -1 at dword `rcx+8` and word `+0x14`, calls `00370890` + 0xE5(`P`+0x1f0), `P` = `0020E600(dword rcx+0x84)`, and returns if `C` = `0020E600(dword rcx+0xa0)` is null; else for each index read likewise from `rcx`, clears bits `0x2` and `0x8` of word `+0x280` of record `R` = `P` + index*0x290 and, when that call is again non-null, with `E` = `C` + 0x30 + signed word `R+0x27e`*0x4c, copies word `E+0x20` to `R+0x270`, -1 to word `+0x276`, calls `00370890` + 0x1A4(`R`+0x1f0) and, in three walks each begun with bit `0x2` of word `R+0x280` clear, writes along the chain `R`, `0020E600(dword +0x278)`, ... floats `E+0x34..+0x3c` to `+0x190..+0x198`, `E+0x28..+0x30` to `+0x1b0..+0x1b8` and `E+0x40` to `+0x1d0`, with 1.0 at `+0x19c`, `+0x1bc` and `+0x1d4..+0x1dc`; then, if still non-null, calls `00370890` + 0x2CA, + 0x2DE and + 0x2E6 with `rcx` | Interior anchor `003708D4`; Interior anchor `00370934`; Interior anchor `003709EE`; Interior anchor `00370A55`; Interior anchor `00370B5A` |
| `00370BA0` | 14 B | `0046E370` + 0x39 | tail-jumps to `00370BA0` + 0x7 with `rcx` unchanged when dword `rcx+0x9c` is 2, and returns without other work otherwise | Interior anchor `00370BA7`; Interior anchor `00370BAD` |
