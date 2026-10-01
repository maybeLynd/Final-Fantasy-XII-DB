# Resource and Asset Pipeline

**Engine category.** Resource load/bind/publish, async asset slots, handle tables, and the VBF/EBP container formats.

| | |
|---|---|
| Classification source | PrimaryOwner: Resource |
| Functions | 572 |
| Status | see [`../_index/COVERAGE.md`](../_index/COVERAGE.md) |

## Systems in this category

- [`authored-data-table-registry.md`](authored-data-table-registry.md) -
  **PARTIAL, tier 1.** **Every authored number in FFXII is reached through one 63-slot pointer
  array** at `0x02EBF008`, all sharing a count/stride/RVA header. The index to the game's content.
- [`resource-section-addressing.md`](resource-section-addressing.md) — **DOCUMENTED, tier 1.**
  How the engine locates data inside a loaded resource: a 4-byte tag plus a 32-byte name key,
  with `0` and `@ALL` as tag wildcards and `-1` as the not-found sentinel. Two entry storage
  modes, one of them cached behind a global re-resolve flag.

- [`the-resource-request-queue.md`](the-resource-request-queue.md) — **PARTIAL, tier 1.** The 64-slot
  request queue every file load goes through: the builder that sizes a request from the file-size
  table and stalls when no slot is free, the pump the frame drives through six states, 512 KB
  parts, and the three callbacks a requester hands in.
- [`VBF-Archive-And-Authored-Tables/vbf-archive-and-st2e-tables.md`](VBF-Archive-And-Authored-Tables/vbf-archive-and-st2e-tables.md) —
  **DOCUMENTED, tier 1.** The 31 GB `SRYK` archive (89,414 entries, index-only queries) and the
  **`st2e`** authored table header — magic plus count/recordSize/headerSize, checked by file-length
  arithmetic. **`action_data.bin` is the file behind registry slot `0x02EBF138`**: 543 records of 60
  bytes, its own count field confirming the executable's `0x21E` bound.

- [`Standard-Formats/shipped-standard-formats.md`](Standard-Formats/shipped-standard-formats.md) —
  **DOCUMENTED, tier 1.** Eight extensions the game did not author, named from one extracted file
  each: TGA title screens, CSV / JSON / C-header text, and four PS2 carry-overs — `SYSTEM.CNF` and
  the memory-card icon pair. The `.ico` files are PS2 icon models, not Windows icons; the ledger's
  2026-09-03 row is overturned.

Other priority targets: `0037F1F0` `Runtime.Resource.AsyncAssetSlotPollFinalizeNotifyOrRetry`, `002D81D0` resource handle table, VBF/EBP container layout (use `ff12-vbf.exe` and `ff12-script.exe`).

## Hooking constraint: Resource-owned one-time-init holders (BK-8, OPUS, 2026-09-27)

Of the 707 lazy-static holder functions, **149 of the 150 that carry a subsystem owner are owned by this category** ([lazy statics and the one-time-init lock](../24-Compiler-And-CRT-Runtime/Lazy-Static-Initialization/lazy-statics-and-the-one-time-init-lock.md); [member registration](../22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/member-registration-and-the-recovered-field-schema.md) §6). For a hook placed anywhere in this category this means:

- A Resource-owned function may be inside a one-time-init region.
- A detour there that returns early or throws leaves the guard at `-1` and hangs every later caller.
- Check for `_Init_thread_header` / `_Init_thread_footer` (`008092FC` / `0080929C`) around the site before placing it, and prefer hooking the accessor's caller.

This is where a shared-world mod most wants to hook. The figure is the holder census's, and it is not re-measured here.

## How to add a system here

1. Copy [`../_templates/SYSTEM.md`](../_templates/SYSTEM.md) into a descriptively-named
   subfolder (or as a `.md` file if it is a single mechanism).
2. Fill all eight sections. A missing section means `STUB` or `PARTIAL`, never `DOCUMENTED`.
3. Mirror every "What is not known" entry into
   [`../_index/OPEN-QUESTIONS.md`](../_index/OPEN-QUESTIONS.md).
4. Register any cross-subsystem chain in
   [`../_index/CALL-CHAINS.md`](../_index/CALL-CHAINS.md).
5. Obey [`../_index/EVIDENCE-STANDARD.md`](../_index/EVIDENCE-STANDARD.md).
   No banned evidence class, ever.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. The image-address resolver / encoder fan-out is MECHANICAL.*

**Presentation — CLIENT.** The resource handle table `002D81D0` named above is also called by three Presentation bodies
(175, 319 and 610 bytes).

## The `0037F1F0` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`0037F1F0` (~159 B) — stack-cookie `0x40` frame (`0037F1F6`/`0037F200`).

| member | role | interior |
| --- | --- | --- |
| `0037F7C0` | `movsxd rbx, edx` index body (`0037F7CF`) | [`0037F7CF`](../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none.
