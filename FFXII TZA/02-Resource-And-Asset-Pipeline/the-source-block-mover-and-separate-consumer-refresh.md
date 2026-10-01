---
system: Original arena source movement and separate consumer refresh
category: 02-Resource-And-Asset-Pipeline
status: DOCUMENTED — every register row is closed (OV-45 and OV-46 answered 2026-09-29; OV-47 SUPERSEDED as a duplicate of OV-2; OV-48 and OV-49 NOT A QUESTION, the acceptance item OV-49 discharged by the non-author review FRONTIER-REVIEW-AUDITSPEC-OV-ACCEPTANCE-0929 that accepted the SECTION-07 content); owner read 2026-09-30 (OPUS)
owner_layer: "Runtime.Memory / EFX source and container consumers"
evidence_tier: "isolated original-instruction execution and selected full-body static analysis"
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: "SECTION-07: actual allocator movement and demand delivery; combined driver tested only through an explicit original-code window"
external_production:
  section: SECTION-07
  date: 2026-09-23
  status: "locally validated; formal independent acceptance pending"
  evidence: _experiments/evidence/continuation-section07-source-movement/REVIEW.md
audit:
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-source-mover-falsification-pass-1
---

# What moves a resource, and when its consumers are repaired

A stable tagged handle can name a different backing address after an allocation call. The arena
mover updates that handle; it does not update every consumer's cached raw pointer. EFX has separate
refresh paths. This page distinguishes the original producers from those consumers and specifies
what the new bounded execution establishes.

[Evidence and reproduction](../_experiments/evidence/continuation-section07-source-movement/REVIEW.md).
This advances [the ownership/disposal mechanism](the-resource-owner-from-copy-or-borrow-to-disposal.md),
[the entry tree](CONTRACT-resource-entry-tree.md), and [the source rebase](CONTRACT-efx-source-rebase.md).
It does not assign unrelated text pointers to this owner or claim a safe complete game schedule.

## 1. Interface and identities

| Operation | Original body | Relevant input/result |
|---|---|---|
| Explicit compaction | `00369C60` | arena ID and repeat flag; returns completed-move count |
| Allocation-pressure retry | `0036BFE0` | current arena/request extent; may move existing allocations before retry |
| Equal-size selector | `0036AAD0` | arena and repeat flag; uses current free head |
| Adjacent/search selector | `0036ABE0` | arena; at most one selected move per invocation |
| Actual mover | `0036A2A0` | arena record, selected free header, selected source header |
| Movement latch read/clear | `00369CF0` / `003697C0` | arena ID; reads/clears arena `+0x62` |
| Deferred child request | `003E6AA0` | render record and index, stored in five bits |
| Bound-container child entry | `003B3C00` | full container ticket and signed index |
| EFX source refresh | `003B3480` | context and optional container |
| Combined container walk | `0024D540` | only original refresh window `0024D565..0024D6A9` executed here |

A movable allocation's header is `payload - 0x40`; its `+0x18` DWORD is the payload allocation
extent. Its encoded `+0x20` backlink identifies a 16-byte handle slot. The tagged value uses the
slot address, while `slot+8` holds the current allocation header. Slot/header generation words are
updated together. The tested handle value stays the same across a move; an old raw pointer does not.

## 2. Selection is not a generic best-fit algorithm

The exact selector starts at the current free-list head, `arena+0x90`, and searches the movable tree
by the signed `header+0x18` extent. An equal-size candidate must lie above the hole by the original
low32 unsigned address comparison and have inhibit mask `0x04` clear. A smaller candidate may be remembered
in a register, but that register is not a fallback argument to the mover. The controlled smaller,
nonadjacent member is not selected.

The adjacent selector walks free holes. It can first move a hole's physical successor when that
block is allocated and `header+0x15 & 6 == 2`: membership present, inhibition absent. Equal size is
not required in this branch. Otherwise it performs the exact-size higher-address search. The
fixture distinguishes a larger adjacent hole from an equally large hole separated by a raw block.

Acquiring through `0036A000` removes membership and excludes the tested block from the selectors.
Releasing through `0036D170` restores eligibility unless inhibited. This is not a nesting retain
count, a scheduler lock, or evidence that all callers obey a universal pin convention.

`00369C60(..., 0)` can make **two** moves: one through the exact pass, then one through the adjacent
pass. A nonzero repeat value repeats the applicable walks. Neither form promises that every
fragmentation arrangement can be compacted or that an allocation always succeeds.

## 3. Actual move order and what the stable handle does not promise

The original `0036A2A0` performs metadata and tree bookkeeping around this decisive order:

1. Decode/reuse the source's handle slot and write its destination header at `0036A364`.
2. Call the real old-allocation release at `0036A397`.
3. Copy `source_header+0x18` payload bytes through `004746F0` at `0036A3A7`.
4. Claim the chosen destination through original `0036BC60` at `0036A3BB`, restore metadata,
   reinsert membership, and synchronize slot/header generation (store at `0036A461`).

The copy adapter independently observes the republished slot and already-released old allocation
at import entry. This is **not atomic publication**. No thread or callback is shown observing that
interval in FF12, so the result establishes ordering, not a demonstrated game race.

For normal non-overlapping fixture moves, the complete `0x400` allocation survives, the tagged
handle resolves to the destination, the old raw address is no longer an allocated payload, and
usage accounting is preserved. Arena release changes allocation bookkeeping; the synthetic backing
map remains mapped and this is not an OS-unmapping test.

A smaller adjacent-hole control reaches overlapping source/destination ranges at the original
`memcpy` import. That process stops before copying. No host `memmove` is used to silently validate
an overlap, and no eventual payload result or Windows CRT defect is claimed.

## 4. Allocation pressure can be the producer

The pressure fixture consumes an arena, then frees two `0x800` holes separated by a movable `0x400`
block. Neither individual hole can satisfy a new `0xC00` request. The normal original allocation
front reaches `0036BFE0`, which selects and moves the prior source, retries allocation and returns
new storage. No callback or diagnostic manufactures progress; the existing source bytes survive.

Thus a caller cannot assume a raw cached pointer remains current merely because it did not request
an explicit compaction operation. An allocation can be the invalidating operation.

The same producer has statically checked scheduling paths: `002E65A0` invokes compaction for arenas
6 and 10 during maintenance, and script adapter `0050E300` supplies the requested arena/repeat
arguments. Their complete external service/VM executions are not part of this fixture.

## 5. Two dirty notions, not one queue

Successful compaction sets `arena+0x62`. `00369CF0` reads this movement-since-clear latch;
`003697C0` clears it. A successful move followed by release still leaves the latch set until clear.
A zero-move operation does not set it. It does not say that all consumers have been refreshed.

A separate render-record request uses `+0x294` bit27 and `+0x304[31:27]`:

- `003E6AA0` replaces the previous five-bit index and preserves the low 27 bits. It is one coalesced
  request, not a FIFO. The issuer itself does not enforce the later index bound.
- `00427DE0` skips delivery and keeps the bit when `record+0x288 == -1`.
- Otherwise it calls `003B3C00` and clears the bit regardless of success. A stale full ticket,
  invalid index, or failed start is not automatically retried by retaining this bit.
- `003B3C00` rejects negative indices and values at or above `0xB`, validates the full ticket,
  and requires a nonnull container. Index **zero returns 1 without refresh or child start**.
- Indices 1..10 call refresh before child-start logic. A missing group in the fixture returns 0
  after the context/container pointers have already been repaired.

The element-kind `0x28` call at `003B939F` is another static demand site. Its presence does not prove
all moves are followed by that command, nor a universal same-frame or next-frame deadline.

## 6. Real movement followed by original refresh

The fixture uses the actual allocator to move an EFX source with a parsed borrowed lookup. The
handle now resolves to new storage, but the context's `+0x858` base and lookup entry remain old.
Original `003B3480` resolves the handle, computes the new source and repairs the selected lookup.
An unchanged repeat does not apply the delta twice. The old `+0x870` run origin remains unchanged;
borrow-aware teardown does not free that stale origin.

The full dirty-state driver is separately executed with one selected pending request and all
unrelated dirty bits clear. Its positive-index path repairs the context and container despite a
subsequent start returning failure. The index-zero/stale/unbound paths discriminate the opposite
cases. Synthetic empty/default payloads do not certify all specialized repair walkers.

## 7. Combined walk is a separate refresh opportunity

`0024D540` has an additional container-list refresh window. For caller argument zero it follows
`02091108` through container `+0x348`, establishes the current context and repairs borrowed data.
It compares the context's base separately from each container's `+0x390`.

The isolated original window is tested with two containers sharing one context. Both container
bases change correctly; the lookup is not shifted twice. A nonzero caller argument skips that
window; clearing the borrow bit skips the tested repairs. These are caller-selected conditions,
not a claim that an actual render frame ran.

The fixture reproduces the original register/stack entry at `0024D565` and returns at a barrier at
`0024D6AA`. Five earlier service calls and later rendering are not executed. Synthetic container
nodes are detached before destruction because their allocation/destruction is outside this test.

## 8. What an implementation must preserve

Preserve the allocation/header distinction, slot publication/generation updates, membership and
inhibition conditions, capacity copy length, selection order and movement count. Do not silently
turn the allocator's operation into an all-consumer rebase or convert the one-entry pending command
into a successful-operation queue. Zero-return and zero-index semantics require separate handling.

A derived pointer can be current only with respect to the source binding actually used when it
was acquired or repaired. The tests establish specific transitions, not a universal lifetime rule
for arbitrary pointers returned elsewhere in the game.

## 9. Remaining obligations

- [x] ~~**OV-45.** Establish external owner replacement/reload and all actual pin/unpin caller obligations.~~ *ANSWERED 2026-09-29 (FABLE, Claude Opus 5.5) for replacement/reload: a manager reload runs the group deleter at unload and the group initialiser at bind; only the BGM stream head-inserts, so every older owner read completes, and frees its state-5 owner, before the new payload binds. The all-callers part is superseded under OV-2's limit (register row); [`ov45-owner-reload-fable/`](../_index/candidates/ov45-owner-reload-fable/README.md). Register OV-45.*
- [x] ~~**OV-46.** Verify overlapping-copy results against the exact deployed Windows CRT dependency, not a host approximation.~~ *ANSWERED 2026-09-29 (FABLE, Claude Opus 5.5): measured on the exact dependency the game loads (System32 `vcruntime140.dll` 14.51.36247.0, sha256 `d1f4225d...`; the install ships none): its `memcpy` is overlap-safe in all 31,784 overlapping cases, both directions, so the overlapping move above produces the `memmove` result; another machine's redistributable is another dependency; [`ov46-overlap-copy-fable/`](../_index/candidates/ov46-overlap-copy-fable/README.md). Register OV-46.*
- [x] ~~Establish full consumer ordering/reentrancy across maintenance, rendering and possible callbacks/threads.~~ *SUPERSEDED 2026-09-29 (SWE2-FRONTIER): duplicate of OV-2 - the same ask in substance; OV-2 carries it. Register OV-47.*
- [x] ~~Extend nonempty specialized payload/instance repairs where they are required by concrete consumers.~~ *NOT A QUESTION 2026-09-29 (SWE2-FRONTIER): a method constraint phrased as work, ruled a declared limit of the claim - the page already follows it; nothing remains to answer. Register OV-48.*
- [x] ~~Obtain formal independent acceptance of this production; no TEAM, L2 or terminal verdict is self-awarded.~~ *NOT A QUESTION 2026-09-29 (SWE2-FRONTIER) under the class-2 ruling: an independent-acceptance/process item, carried by board task FABLE-CARRIER-SECTION-OVERLAY-ACCEPTANCE-0929. Register OV-49.*

## Falsification pass 1 — 2026-09-30 (OPUS): every section tested survives

**Attack.** The static clauses under sections 2–5 and 7 were turned into checks at their instructions. SECTION-07's
executions are carried, not re-run. Script: `Tools/analysis-kit/gfz-scripts/falsify_source_mover.py`, output
`falsify_source_mover.out`, image `73461d08…`, 0 BROKEN, exit 0.

| # | Clause attacked | Result |
|---|---|---|
| S1 | §3: the move order | **survives**. The slot's `+8` takes the destination header (`0036A364`). The old allocation is released (`0036A397`). The payload is copied from old `+0x40` to new `+0x40` (`0036A3A7`), the destination is claimed (`0036A3BB`), and the generation word is stored (`0036A461`). That is the stated non-atomic order |
| S2 | §2: the two selectors | **survives**. The exact selector starts at the free head (`arena + 0x90`), reads the `+0x18` extent and tests inhibit bit 4 of `+0x15`. The adjacent selector requires `(+0x15 & 6) == 2` |
| S3 | §2: "can make **two** moves" | **survives**. The exact pass runs once. The adjacent pass repeats only while it moves and the repeat flag is set. A nonzero count sets `+2` and the `+0x62` latch; zero leaves both |
| S4 | §5: latch and request | **survives**. `+0x62` is read and cleared at arena stride `0xA8`. The request sets bit 27 of `+0x294` and replaces `+0x304[31:27]`, keeping the low 27 bits |
| S5 | §5: delivery and the child entry | **survives**. Delivery happens only with bit 27 set and `+0x288 ≠ −1`, and the bit is cleared whatever `003B3C00` returns. `003B3C00` refuses an index below 0 or at or above `0xB`, checks the ticket generation in `02EBD480` and needs a container. Index 0 returns 1 with no refresh; any other index refreshes (`003B3480`) before the child start (`0024FE70`) |
| S6 | §4: the scheduled producers | **survives**. Maintenance compacts arenas 6 and 10 with repeat 1 (twice each). The script adapter passes its two operands straight to `00369C60` |
| S7 | §7: the combined walk | **survives**. There are five earlier service calls. The window is skipped for a nonzero argument. The walk goes `02091108 → +0x348` and repairs the context against `+0x858` (through `003A9BA0` among others) and each container against `+0x390`, separately |

## Cross-subsystem neighbours — FINAL-AUDIT pass 22, FRONTIER's debt (SWE2-FRONTIER, 2026-09-30)

*Added 2026-09-30 (SWE2-FRONTIER, `SWE2-FRONTIER-PASS22-DEBT-OWN`, batch 4): layers pass 22 still reported for this page. Every edge was listed in full and the call sites below were read.*

**CoreRuntimeScheduling — CLIENT and SERVICE (10 edges).** The frame and loading loops drive this page's scheduling paths. `MainLoop_UpdateAndRenderFrame` (`0022B8C0`) and `0022BC20` call the combined container walk `0024D540`. The compaction scheduler `002E65A0` is called by those two and by `0022A770`, `0022AF50`, `0022B000`, `0022B6E0` and `0022B7E0`. At the end of its refresh window `0024D540` reads the 8-byte mode getter `00229EA0` (a signed byte from a global) and tests `mode - 2` against `~4` (`0024D6AA`–`0024D6B2`). The scheduling layer decides when compaction and the walk run; what they do stays on this page.

**Audio — SERVICE and CLIENT (4 edges).** The walk's first calls include the Audio body `003B3D20` (`0024D551`), which starts by testing an enable byte. The three 83-byte sound-bank loaders `003A12D0`, `003A1330` and `003A1390` first release their arena through `0036D170` (`003A12D8`, `003A1338`, `003A1398`). `003A12D0` then calls `003A1650` with the same id and, when the returned handle matches the slot-table entry it indexes, sets that entry's byte `+0xD`; the two siblings have the same size and open the same way. So audio is a client of the release that restores a block's eligibility to move.

**ActorEntity — CLIENT (1 edge).** The slot unload `002628B0` calls `002E65A0` twice, around its other teardown calls (`00262AFC`, `00262B12`). Unloading a slot is one of the points where compaction is invoked.

**Script_VM_Native_Bridge — CLIENT (5 edges).** Three script adapters expose the arena controls. `0050E300` pops two ints through `VMValueStack_PopInt32CoerceFloat32` (`00267E10`) and calls the explicit compaction `00369C60` (`0050E318`–`0050E32B`). `0050DEB0` pops an arena id, acquires through `0036A000` and returns the result through `VMResult_WriteInt32` (`0026B4E0`). `0050DF30` pops an id and tail-jumps to the release `0036D170`. Scripts can therefore pin, unpin and compact arenas; the rules stay this page's.

**Presentation — SERVICE and CLIENT (81 edges, batch 7).** The draw loop and the render records are both sides of the separate consumer refresh this page reads. `MainLoop_Draw` (`0022B0B0`) calls the container walk `0024D540`, which calls ten render bodies in its walk (`003A3740`, `003A3A00` and peers). On the consumer side, `RenderRecords_ProcessDirtyState` (`00427DE0`) is cited here for its skip rule (`record+0x288 == -1`). It calls 52 render bodies and the bound-container child entry `003B3C00`, and is called by `RenderSystem_UpdateCharacterRecords` (`00426090`) and `0042ED60`. `003B3C00` refreshes through the EFX source refresh `003B3480`. The child start `0024FE70` calls `003A7460` / `003A74F0` and is called by `003B1260`, `003B2830` and `003B3C00`. The deferred child request `003E6AA0` is called by `003B4B60`, `003B4E50`, `003B54C0` and `003B8260`. `0042ED60` also clears the movement latch through `003697C0`. The last three edges belong to the compaction scheduler `002E65A0` and the producer `003DD4C0`, which the audit files to Presentation by their tags. The scheduler calls the explicit compaction `00369C60` and the producer, and the producer acquires through `0036A000`. Presentation owns the records and the draw; the mover's rules stay here.
