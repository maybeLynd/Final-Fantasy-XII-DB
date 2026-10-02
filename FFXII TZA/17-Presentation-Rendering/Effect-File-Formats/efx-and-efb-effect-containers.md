---
system: EFX and EFB — the effect containers
category: 17-Presentation-Rendering
status: PARTIAL — the residue this line named is answered in §2b (SWE2-CONTRACT DD batch 10) - all 3,698 files opened (header second half measured, +0x0C read by four callers), the EFB buffer lifetime read (one fixed block, released only by the map teardown after its contexts), both binders read (00333C80 = the 0x600 version normaliser, 004FF270 = the 0x700 offset relocator); §5 version counts and the 2026-09-16 walk corrected 2026-09-29 (FABLE, GI-8); still open: SD-194 (runtime — which path the null-name fields request, and whether any such field is loaded; status line current 2026-10-02, SWE2-CONTRACT DD batch 21) (was — no .efx/.efb file was opened and the EFB buffer lifetime is not read; the chunk handlers 003A7E80/003A79C0 read structurally 2026-09-18 (index-registered records in two tables, their binders 00333C80 and 004FF270 unread))
owner_layer: PrimaryOwner:Presentation
evidence_tier: 1
verified_against:
  gzf_sha256: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: additive-annotation across GN161 -> GN162 - REPLACED 2026-09-21 (OPUS), because the snapshot-identity basis this block carried is FALSE at GN162: this document cites record(s) 0026F470, which batch R30 touched. The weaker basis HOLDS and is measured: the advance changed 30 records in comment and tags ONLY - 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten (check_delta_additivity.py GN161 -> PARENT, control passed) - and check_stranded_absence.py, sweeping the GN160 resolved set which strictly CONTAINS all 30, reports no live absence claim on any line of this document
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md (six ledger figures re-derived)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  snapshot_sha256: b57264ba73231665bf226da6d5761feee72df36c5999fc68ae14adfdd18fea34
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
corpus_validated: "3,288 .efx and 410 .efb — magic read from every file in FFXII_TZA.vbf by the 2026-09-06 audit pass (section 6b); written 2026-09-05 with NO FILE OPENED and section 5 keeps that history. First 8 bytes only — the payload is still unmeasured."
last_reviewed: 2026-09-12
archive_formats:
  - "efx"
  - "efb"
audit:
  passes: 1
  last_pass: 2026-09-06
  last_pass_state: GN160-corpus-supplied-repos-1e — the corpus half this sheet lacked, measured: magic of all 3,698 files read from the VBF, all 5 .rdata constants and the reject path re-decoded; version split closed, payload still unmeasured
  crossref_clean: false
  reopened_count: 0
---

# EFX and EFB — the effect containers

> Every spell animation, every summon, every hit flash. **4.5 GB — the second-largest format family
> in the archive after `.phyre`.** This sheet establishes the **container header and its loader
> contract** for both. It does not decode the payload.

> ## ⚠ READ THIS BEFORE THE REST
>
> ~~**No `.efx` or `.efb` file was opened to write this sheet.**~~ *(answered: see the 2026-09-30 update below - every file has now been opened, §2b; 2026-10-02, OPUS)* Neither is in the local extraction and
> no `.vbf` archive exists on this machine, so the corpus half is limited to the archive index —
> names, sizes and directories. **Everything in §2 and §3 is read from the loaders in the shipped
> executable, at tier 1, and nothing in it is corroborated by a file.**
>
> That is the inverse of this project's usual gap. **The reader's own parse is stronger evidence for
> a layout than a corpus reading is** — it is what the engine actually does — but a corpus would
> catch a field the loader never exercises, and there is none here. §5 says exactly what that costs.
>
> *Update 2026-09-16 (SWE2-DATA): the record-bearing chunk families now have a corpus reading —
> all 3,698 files were walked and every `0xB00` record-store chunk (30,033), `0xA00` element
> definition (31,635) and `0x800` sub-record (32,639) decoded. **Corrected 2026-09-29 (FABLE, GI-8): that walk
> stopped at the first blob header of each of the 410 `.efb` files and did not see the 531 EFX streams embedded in
> `.cm` / `.mpk` files; walking every stream gives 48,868 `0xA00` and 53,351 `0x800` chunks
> ([the dispatch page](effect-element-type-dispatch.md) §2.8, [`type_census.py`](members/type_census.py)). The `0xB00`
> count was not re-walked.** The kind-`0x54` mesh records and
> the type-`0x05` elements are censused in
> [effect-mesh-records-kind-54](effect-mesh-records-kind-54.md); the remaining payload is still
> unmeasured.*
>
> *Update 2026-09-30 (SWE2-CONTRACT, DD batch 10): every `.efx` and `.efb` file has now been opened for this sheet's
> own claims - the header's second half, the chunk grammar, the `0x600` / `0x700` records and the EFB header. §2b has
> the results; the statement above describes how the sheet was written, and stands as history.*

---

## 1. What the player sees

When Firaga blooms, when an Esper lands, when a Quickening chains — the shape, timing and colour of
what happens on screen come out of these files. `.efx` is the bigger family and the one attached to
characters and actions; `.efb` is smaller and sits in its own tree.

**A modder who wants a different Quickening edits one of these**, and the first thing they need to
know is which bytes the engine will refuse — because the engine refuses silently, and a rejected
effect simply does not appear.

## 2. The layout

**Both formats share one container convention.** Offsets are from the start of the file.

```struct EfxHeader base=file size=0x10
+0x00  char[8]  magic     'EFX0010' | 'EFX0009' | 'EFX0008', NUL-terminated, compared as 8 bytes
+0x08  byte[8]  _unread   no reader found in the loader body at 0x003EDAD0   <- corrected 2026-10-02, OPUS - +0x0C is read by the caller 003B0660+0xDF as the stream length (section 2b)
```

```struct EfbHeader base=file size=0x10
+0x00  char[8]  magic     'EFB0001' | 'EFB0002', NUL-terminated, compared as 8 bytes
+0x08  byte[8]  _unread   no reader found in the loader body at 0x0026FB90
```

**In both, the payload begins at `+0x10`** — `0x003EDB7B` `LEA R12,[R9 + 0x10]` for EFX, and the EFB
loader takes `param_1 + 0x10` at the same point in its flow. **The eight bytes at `+0x08` are
skipped by both loaders**, which is a finding rather than an absence: the header is 16 bytes and only
the first half is read.

### The EFX chunk stream

After the header the EFX loader walks a chunk list until it reaches `base + size`:

```struct EfxChunk base=record
+0x00  u32   length    distance to the next chunk; the walk adds it to the cursor
+0x04  u16   flag      gate: the loader's branch requires this to equal 0x100
+0x06  u16   type      0x600 | 0x610 | 0x620 | 0x630 | 0x700 | 0x800 | 0xA00   (0x701 withdrawn 2026-09-12)   <- corrected 2026-10-02, OPUS - the header is 0x0C bytes: an i32 at +0x08 follows, stored to 02EBB738 before each handler (003EDAD0+0x4A6..+0x4AC), and the handler gets chunk + 0xC (003EDAD0+0x4C3); section 2b
```

**Seven chunk-type constants are compared in the loader body**, and they fall into two families that
are handled by completely separate code paths:

| type | handling |
|---|---|
| `0x700` ~~, `0x701`~~ | run-collected: consecutive `0x700` chunks are measured, one allocation is taken (context `+0x880`), the run is `memcpy`'d, then each is passed to `FUN_003A7E80` (`003EDEE5`–`003EDFBF`) |
| `0x800` | run-collected into context `+0x870`, each chunk to `FUN_003A9730` — **copied into a new allocation, or borrowed in place** (below) (`003EE0EB`–`003EE1DD`) |
| `0xA00` | the same shape into context `+0x878`, each chunk to `FUN_003A9A70` (`003EDFD1`–`003EE0D9`) |
| anything else, or a chunk whose `+0x04` is not `0x100`, or context `+3` bit 0 clear | the single-chunk fallback `003EE2D0(chunk + 4, length − 4)` — not read (`003EE1EC`) |
| `0x600`, `0x610`, `0x620` | run-collected into a **second** buffer with per-type stride arithmetic (below) |
| `0x630` | terminates the `0x600`-family run |

**The `0x600`-family stride arithmetic is authored-data shaped and worth writing out**, because it
is what a modder changing chunk sizes will hit. Measuring the run:

```
0x600 :  total += 0xB0                                  fixed 176-byte slot
0x610 :  n = byte at chunk+0x13 ;  if n == 0 then n = 0x40     (read as [rax + 0x0F] with rax = chunk + 4; corrected 2026-09-12)
         total += n * 4 + 0x30
0x620 :  total += length                                 the chunk's own length
```

and when copying, `0x610` advances the destination by `0x330 - (0xC0 - n) * 4` — so a `0x610` chunk
occupies a **0x330-byte slot minus four bytes for every unused entry below 0xC0**, with `n` defaulting
to `0x40` when the authored byte is zero. `0x600` chunks are zero-filled from their own length out to
the full `0xB0`.

> **`n == 0` meaning `0x40` is a real modding trap**: a chunk that stores zero entries is treated as
> storing sixty-four, in both the sizing pass and the copy.

**Copy or borrow — the `0x800` / `0xA00` runs (2026-09-12, FABLE, from ASTRA's arena-7 package).** The loader's
context is `*(02F97340)`. For both run types it measures the run, then tests **context `+2` mask `4`** — bit 2,
not bit 4 as first written (`003EE018`, `003EE117`: `test byte ptr [rax + 2], 4`): clear → allocate under the arena selection `(8, 10)` and `memcpy` the run into the
new block, storing that block at `+0x878` / `+0x870`; **set → store the source pointer itself** there
(`003EE078`, `003EE171`) and hand the chunks to their handlers in place. `0x700` and the `0x600` family are always
copied. So with the bit set, the engine keeps pointers into the caller's EFX buffer. ~~for the kind-10 file that
is arena 7's raw backing … Which value the bit has at that load, who sets it … are not established.~~
**Who sets it — the writer census is now closed (2026-09-13, SWE2-STRUCT, OPUS-REQ-SWE2-STRUCT-EFXFLAG-WRITERS):**
a context is always a heap copy of a caller's `0x890`-byte template made by
`0024B3A0` (allocated, linked into the per-kind list `020910A0[template byte 0]`, its four run pointers
`+0x870`–`+0x888` cleared, installed at `02F97340`). The complete writer set for context `+2`, enumerated by body
decode: every constructor memsets the template (byte = 0); `0026FB90` (`0026FC60`) and `003B38B0` (`003B3984`)
alone `or 0x0C`; `0024B3A0` propagates the byte into the heap copy; and post-copy exactly two bodies write it —
the identical nibble merges `0026FD26` (type-2 context) and `003B22A0` (type-7 context), each computing
`(old & 0x0F) | (entry+0x16 & 0xF0)`, so **the low nibble can never change after construction**. ~~the only store to
`+2` is the EFB loader's post-parse nibble merge~~ — the earlier rip-relative census missed `003B22A0`; it was a
sample, not a census. Consequence: `or 0x0C` is **not universal** — it is exactly the type-2 and type-3
constructors — so the teardown release at `003A9625` (mirror `003A9975`) is **reachable**, taken by every
type-1/4/5/7 context that latched `+3` bit 0 with a non-null run pointer — the designed path for the
run-collected types 4 and 5. *Six functions build a context and parse, each
from its own template — the table below; the two bullets that follow are two of them.*

| template byte `+0` | constructor → parse | `+2` | `+3` bit 0 (run-collected chunks) | `0x800` / `0xA00` runs |
|---:|---|---|---|---|
| 1 | `002FC4A0` (`002FC541`, `002FC54B` → `002FC5D2`) | 0 | **no** | not run-collected: every chunk goes to `003EE2D0` |
| 2 | the EFB loader `0026FB90` | `0xC` | yes | **borrowed** from the EFB buffer |
| 3 | `003B38B0` (`003B3977`–`003B39B3`; one caller, `00409FE0`) | `0xC` | yes | **borrowed** from `resolve(source) + offset`, with the source reference, offset and resolved base recorded at context `+0x860` / `+0x864` / `+0x858` |
| 4 | `003B29B0` (`003B2A60` → `003B2A75`) | 0 | yes | copied |
| 5 | `003B0660` (kind 10) | 0 | yes | copied |
| 7 | `003B2220` (`003B2250` → `003B226D`), source from its record's `+0x28` — the field `003B2310` fills with arena 7's backing for kind 12 | 0 | **no** | not run-collected |

So **borrowing is not EFB-only**: the type-3 effect instance (`003B38B0` takes a node from the pool `02EBDB88`)
borrows too, and it is the kind that carries relocation fields. And for types 1 and 7 the copy / borrow bit is moot —
their contexts never take the run-collected path (the `0x37D` mask below).
- **the EFB loader** `0026FB90` zero-fills its template, sets byte `+0` = 2 and **ORs `0xC` into `+2`
  unconditionally** (`0026FC4E`–`0026FC6C`) — so every EFX blob embedded in an EFB file has its `0x800` / `0xA00`
  runs **borrowed from the EFB file buffer**;
- **the effect-file loader** `003B0660` zero-fills its template and sets only byte `+0` = 5 (`003B0719`–`003B0735`)
  — so its file's `0x800` / `0xA00` runs are **copied**. That file is resource kind 10, id 0 — kind 10 holds
  `effect_finish\*\c_all.efx` and `menu\m_all.efx` ([the size tables](../../02-Resource-And-Asset-Pipeline/Loose-Files-And-Size-Tables/file-size-tables-fst.md)) — loaded into arena 7's raw
  backing, so for this load no borrowed pointer into arena 7 is kept by this function. ~~The chunk handlers'
  own retention, and the lifetime of the EFB buffers the borrowed pointers name, are not read.~~ *Corrected 2026-09-30
  (SWE2-CONTRACT, DD batch 10): both are read in §2b. The handlers keep their records in the context's own tables
  (`+0x38` for `0x600`, `+0x840` for `0x700`), which the context teardown `0024F410` releases. The EFB buffer is one
  fixed block that only the map teardown `00378230` frees, and it does so after it has disposed of every type-2
  context.*

**Borrowed bytes are written to and published, and a borrowed context can be relocated** (ASTRA's primary package,
[the lifetime evidence](../../02-Resource-And-Asset-Pipeline/authored-reference-lifetime-evidence.md) §14–§16; FABLE re-read the cited instructions 2026-09-12):
- **Not a read-only view.** The `0x800` handler `003A9730` stores the chunk's id and subtype into the payload
  (`0x280` / `0x282` past it, `003A974F`–`003A9755`) and publishes the **full payload pointer** into the table at
  `*(02EBEF90)` indexed by the id (`003A9767`), then passes `low32(payload) + dword[02EBB738]` on (`003A976B`–`003A9771`);
  `003A9A70` does the same for `0xA00` through `02EBEF78`. Neither checks the id against the table size.
- **Teardown** `003A9600` / `003A9950`: with `+3` bit 0 set it releases the run block `+0x870` / `+0x878` **unless
  `+2` mask 4 is set** (a borrowed run is never freed) and clears the pointer; with it clear it releases every
  table entry from index 1; either way it finally releases the table itself (`003A9600`–`003A9697`).
- **Relocation.** For a mask-4 context, `003B3480` (called from `003B3C00`) re-resolves `+0x860` through `003AB7F0`,
  adds `+0x864`, and when the result differs from `+0x858` calls `0024D970`, which rebases the context's lists and
  both tables by `low32(new) − low32(old)` sign-extended, skipping table index 0, and stores the new base last
  (`0024D984`–`0024D9A7`). `003AB7F0` sends a tagged value (low two bits) through the arena-handle resolver
  `0036B130` — the same handle form as [the memory page](../../24-Compiler-And-CRT-Runtime/Memory-And-Allocation/where-the-games-memory-comes-from.md) — and treats a result whose sign-extended
  low 32 bits are ≤ `0x40` as null. **So a borrowed effect can follow data held in a handle-addressed arena block
  that moves**; no instance of such a move is observed, the repair covers a signed 32-bit displacement only, and
  the list handlers and native subtype effects are not executed.
- **Where the type-3 source comes from, and when relocation can matter** (§17–§18 of the lifetime evidence, re-read
  2026-09-12). The type-3 constructor's caller `00409FE0` passes a resource entry's storage source, entry `+0x18`
  (storage record at `+0x10`). The storage allocator `003AB8B0` makes **kind 0 a raw block and kind 1 a handle**.
  The initialized mode-0 entry uses kind 0 — an untagged pointer, which `003AB7F0` returns unchanged, so for that
  path the rebase compare cannot change and no relocation happens; only a **kind-1 (handle) source** can move under a
  borrowed effect. For mode 0 the final `003AB940` returns without releasing the source.
- **Teardown order.** Both entry-removal paths `00409CA0` / `00409D60` dispose the effect first — `003B37E0(entry +0x44)`,
  which requires the full stored management id, calls `0024F4D0` and `0024F410` on the context and recycles the
  management record — then `00409730` releases the entry, reaching `0051EE80` → `003AB7C0` on the source last
  (`00409CFD`–`00409D18`). So a borrowed effect context is disposed before the bytes it borrows are released. Before
  that, `00409730` calls `00427B00(entry +0x30)`, which **frees nothing**: it walks the active character render records
  and clears references at `+0x68` / `+0xD8` / `+0xF0` that decode to the argument (lifetime evidence §19; its only calls
  are the reference encoder and decoder). A mode-1 entry's source is therefore not reclaimed by that call.
Also gated before any chunk work: context `+3` bit 0 is set only when context byte `+0` is 0, 2, 3, 4, 5, 6, 8 or 9
(mask `0x37D`, `003EDBA2`–`003EDBB3`), and it is cleared at entry.

## 2b. The files opened, the two binders, and the EFB buffer's life — 2026-09-30 (SWE2-CONTRACT for OPUS)

*For the player:* an effect file's older layouts are converted in memory as they load. Each effect's internal
offsets are fixed up once, at load. The map's `.efb` weather effects stay in memory for as long as the map is loaded,
and they are released only after every effect built from them has been torn down. The checks are in
[`b10_checks.py`](../../_index/candidates/swe2contract-ddres-b10-0930/b10_checks.py) (E1–E12). The corpus is the full
extract, and control X1 re-decodes sample files from `FFXII_TZA.vbf` byte for byte.

**The files, opened (E1–E4).** Every `.efx` begins with its 8-byte magic: `EFX0010` × 3,284, `EFX0008` × 4. **`+0x08`
is the float `1.0` and `+0x0C` is the file's own size, in all 3,288 files.** The chunk walk from `+0x10` ends exactly
at `+0x0C` in every file, and all 157,819 chunks carry `0x100` in their `+4` word. The chunk header is
`{u32 length, u16 0x100, u16 type, i32 +0x08}`. The loader stores the `+0x08` dword at `02EBB738` before each
handler (`003EDF76`–`003EDF7C`), passes the handler `chunk + 0xC`, and the record starts at `chunk + 0x10`.

The loader body does not read `+0x0C`, but four of its six callers do: `003B0660`, `003B2220`, `003B29B0` and
`003B38B0` each pass `dword [efx + 0xC]` as the size argument (`003B073F`, `003B226A`, `003B2A6F`, `003B39B0`). The
EFB loader passes its blob header's size instead (`0026FCE2`). In all 410 `.efb` files, every blob's size word equals
the embedded EFX's own `+0x0C`. So §2's `_unread` holds for the loader's body only: `+0x0C` is the stream length the
callers hand in, and `+0x08` is a constant that nothing on these paths reads. Every `.efb` is `EFB0002`, with the
blob count at `+0x08` and the row count at `+0x0A` (§3), and its `u32 +0x0C` is 0 in all 410 files.

**`004FF270`, the `0x700` binder, relocates offsets (E5–E7).** `003A7E80` copies the chunk's byte `+2` to record
`+0xC2` and calls `004FF270(record, low32(record) + [02EBB738])`. `004FF270` switches on `+0xC2`:

| `+0xC2` | body | fixed record | chunks |
|---:|---|---:|---:|
| 0 | `00537C80` | `0x160` | 8,029 |
| 1 | `00537FA0` | `0x200` | 472 |
| 2 | `00538350` | `0x280` | 60 |
| 3 | `005387B0` | `0x300` | 64 |
| other | returns the record unchanged | — | 0 |

Each body runs `004FF230` (three `0x40`-byte blocks at `+0x00`, `+0x40` and `+0x80`), then a fixed list of
sub-blocks, and returns the record's end. Every step is the same operation on a pair of dwords (`00430AF0`,
`004304F0`): decode through `0020E600`, add the delta, re-encode through `0020E620`. Each listed dword therefore
becomes `stored + low32(record) + bias` (mod 2^32).

The files agree. In all 8,625 `0x700` chunks the chunk's `+0x08` dword equals its subtype's fixed size exactly, and the
chunk is long enough to hold that record. Every one of the 212,896 relocated dwords, plus that bias, lands inside its
own chunk. **So the stored values are offsets into the variable data that follows the fixed record, and the binder
fixes them up once, at load.** The result is in the arena-offset form that the engine decodes with `0020E600`. It
names `record + bias + stored` only when `[01F83530]`'s low 32 bits are zero, which this batch does not establish. The
`0x700` run is always copied (above), so the result points into the copy.

**`00333C80`, the `0x600` binder, normalises old versions (E8–E9).** `003A79C0` stores the chunk's index byte at
record `+0`, resets the 29 dwords `+0x2C`–`+0x9F` to the encoded null, registers the record and calls `00333C80`.

- **With the version global `01EFF3B0` at 9 or 8**, it copies the `0xA0`-byte record to the stack and rewrites the
  first `0x2C` bytes in the `EFX0010` layout:
  - the lane bytes move from `+0x06` to `+0x0A`. There are eleven in `EFX0009`; `EFX0008` has ten, so the eleventh
    (`+0x14`) is cleared;
  - the following flag and word fields move up. In `EFX0009` the words at `+0x14` / `+0x16` land at `+0x18` /
    `+0x1A`, and those at `+0x1A`–`+0x1E` land at `+0x26`–`+0x2A`. `EFX0008`'s come from `+0x10` / `+0x12` and
    `+0x16`–`+0x1A`;
  - `+0x03`–`+0x07` and `+0x1C`–`+0x25` are zeroed.
- **In every version**, it clears `+0x16` bit 1 when the old high nibble is `0xF`. It then sets the high nibble to
  the index of the last non-zero byte among the eleven at `+0x0A`–`+0x14`, or 0 when all are zero
  (`00333FB0`–`00333FD9`), and returns `record + 0xA0`.

Those eleven bytes are the lane map that [op `0x28`](../Model-And-Motion-Formats/fef-and-motion-entries.md) indexes
(`byte[def + 0xA + lane]`), and the 29 dwords are its request slots (`dword[def + 0x2C + 4·map]`). The nibble is the
last lane in use. In the files, every `0x600` chunk's `+0x08` dword is `0xA0` (5,363 chunks). The authored nibble
matches the recomputed one in only 3,209 of 5,359 `EFX0010` records, so the value the engine uses comes from the
loader, not from the file.

**Where the records are kept (E12).** `003A79C0` registers each `0x600` record in the table at `[02EBEFA8]`. For the
EFB loader's context that table is the context's `+0x38` (`0026FCAD`). `003A7E80` registers each `0x700` record in
the context's `+0x840` table (`0026FCB8`). The context teardown `0024F410` points the same two globals at those
tables and calls their teardowns `003A75B0` / `003A7D30` (`0024F46A`–`0024F488`).

**The EFB buffer's life (E10–E11).** `00377DC0` is the map load's `.efb` request (from `00378A60`). It allocates one
fixed block of `0x43D170` bytes (4,444,528, exactly the size of the largest shipped `.efb`) and reads
`PS2Data\efb\<map>.efb` into it.

- **Mode 1:** the completion `003788F0` parses the block through `0026FF90` → `0026FB90`, so the type-2 context's
  `0x800` / `0xA00` runs borrow from this block. It then publishes the block at `02ADD088`. On a failed read it
  releases the block and clears `02ADD050`.
- **Mode 0:** the completion `003789A0` hands the block to `0053DD10`, which is `mov eax, 1` / `ret`, so nothing is
  parsed. It publishes the block at `02ADD088` too.

**The block is freed in one place: the map teardown `00378230`** (callers `002628B0`, `00378A60` twice, `0050D5D0`).
When `02ADD088` is set, the teardown runs three steps in this order:
1. `0026FF50`: when an EFB was parsed, `0024C550(2)` walks the type-2 context list `020910A0[2]` and disposes of every
   context through `0024F410`. That runs the `0x800` / `0xA00` run teardowns `003A9600` / `003A9950` (which never
   free a borrowed run) and then frees the context itself.
2. `0026F420`: `0024C460(2)`, the kind's second list.
3. Only then does it release the block and clear `02ADD088`.

`0026FB90` also disposes of the previous EFB's contexts before it parses (`0026FBAE`–`0026FBCE`). **So on these paths no
type-2 context outlives the bytes it borrows.** ~~Not read: what mode 0 is for, and whether a mode-0 and a mode-1
request can both be pending for one map (each publishes at `02ADD088`).~~ *Corrected 2026-09-30 (SWE2-CONTRACT for OPUS, DD batch 14)*: both are answered in §2c
below. Mode 0 asks for the `.efb` of the field block's shared map_ctrl pack, and no such file ships. Both requests can
be pending, and the mode-0 read always fails and frees its own block first.

| claim | evidence | tier |
|---|---|---|
| header `+0x08` = 1.0 and `+0x0C` = size, chunk grammar, EFB header, blob sizes | E1–E4, all 3,698 files, control X1 | 1 |
| `+0x0C` read by four of the six loader callers | E3 | 1 |
| `004FF270`: subtype dispatch, fixed sizes, the relocation arithmetic | E5–E6 | 1 |
| every `0x700` chunk's bias = fixed size; every relocated offset inside its chunk | E7 | 1 |
| `00333C80`: version rewrite, lane-count nibble; authored vs. computed nibble | E8–E9 | 1 |
| the handlers' tables and their teardown | E12 | 1 |
| the EFB buffer: one fixed block, freed only by `00378230` after its contexts | E10–E11 | 1 |

## 2c. The mode-0 `.efb` request, and why it never collides with mode 1 — 2026-09-30 (SWE2-CONTRACT for OPUS)

*For the player:* nothing is visible. When the field loader loads a field, it also asks for a second map-effect file,
named after the area's shared map pack. No such file ships, so the request fails quietly and returns its buffer before
the field's own `.efb` is read. *For a modder:* a file supplied under that name would be read and never parsed. When
the field's own `.efb` also loads, the 4.4 MB buffer holding it is never freed.

The checks are in [`b14_checks.py`](../../_index/candidates/swe2contract-ddres-b14-0930/b14_checks.py) (Q1–Q13).
They are static, plus the installed archive.

**What mode 0 asks for (Q1–Q4).**
- The field loader `00331990(field)` calls `00378A60` twice. The first call is mode 0 with the field block's aux
  value 0 (`MapRef_GetAuxValue0`, `00264F40`). The second is mode 1 with the row's own word `+0` (`00264F10`). The
  script verb `mapload` (`0050D4D0`) asks for mode 1 only. These are `00378A60`'s only three call sites.
- Each call loads a map_ctrl pack through `00378030` and asks `00377DC0` for the `.efb` named after it. The name is
  namespace 4's entry for the index (`002DF880`), cut to the stem after the last `\` or `/` and its four-character
  extension: `PS2Data\efb\<stem>.efb` *(qualified 2026-10-02, OPUS: that name is built on one branch only - when the copied name has a `\` or `/` with more than four bytes after the last one; with no separator, or exactly four bytes after it, the request names an empty string, and with 0-3 bytes after it the copied name is kept whole - the 'Not settled here' paragraph below, from ASTRA's SPEC-accepted [`sd194-stale-name-slice`](../../_experiments/evidence/sd194-stale-name-slice/README.md), method A)*.
- So mode 0 is the request for the `.efb` of the block's shared pack. Its completion `003789A0` hands a delivered block
  to the stub `0053DD10` (`mov eax, 1` / `ret`) and publishes it at `02ADD088`. Only the teardown `00378230` reads
  that global (Q9). Nothing parses the block.

**What ships (Q11–Q13).** Over map_ref.bin's 1,315 rows (their indices equal
[`map-ref-field-packs.tsv`](../../03-World-Area-Field/Map-Pack/members/map-ref-field-packs.tsv) in all 1,315):
- no mode-0 name ships. The 1,281 fields that have one name 89 distinct block packs, and none has an `.efb` in the
  archive;
- mode 1's `.efb` ships for 945 fields, 249 name one the archive lacks, and 121 name no package;
- the two names never coincide;
- the install holds no loose `PS2Data` tree beside the archive.

**What a missing file does in the queue (Q5–Q10).**
- Both requests go through `0032E7B0` → `0032E870` as kind `0xFF` with size −1, appended at the tail. The pump
  `0032E070` serves only the head, one request at a time.
- `002DF6C0` takes its first branch only when the file-system flag `+0x88` (`0017D930`) and two worker flags
  (`001D6EF0`) are set and the path's key is in the file cache (`001D6B40`). Otherwise `001D6D90` sets the status word
  `0215EFF4` to −1 and posts a type-2 job.
- The job (`001A0CF0`) stores `0xFFFFFFFE` when the open fails, and its callback `001D6D70` writes that to the
  status word. The pump waits while the word is −1, then takes state 6 on a negative value. `0032E370` then calls
  the completion with ok = 0.
- `003789A0`'s ok = 0 arm frees its own block and clears `02ADD098` and pending bit `0x40`.
- The first branch could leave a stale status word: a cached path whose open then fails. A path is in the cache only
  if its 31-bit key matches a file the game has opened and read (`0020BE50` compares the key alone). No mode-0 path's key
  matches the key of any of the archive's 89,414 names (Q12).

**So both requests can be pending, and on shipped data they never collide.** After `00331990` both are queued, mode 0
first. The mode-0 read finishes, and fails, before the mode-1 read starts. Then mode 1 parses and publishes. Nothing
is left behind. If a mode-0 file existed, mode 0 would publish first, and a successful mode-1 completion would
overwrite `02ADD088` without freeing it. The teardown frees only `02ADD088`, so that block would leak. That is a modding hazard,
not a shipped path.

**Not settled here (runtime).** For 34 fields the block's index names no package, and for 121 the row's own index
names none. `002DF880` then returns −1 without writing the buffer, and `00377DC0` does not check. *Narrowed
2026-10-02 (SWE2-DATA) on ASTRA's SPEC-reviewed slice [`sd194-stale-name-slice`](../../_experiments/evidence/sd194-stale-name-slice/README.md),
method A over bodies `377DC0..37802A`:* the buffer is not simply forwarded. The caller copies through the first NUL
(`n`, 0≤n≤259), scans the copy backwards for a `5C`/`2F` separator (`j`, or −1), and then: **no separator** (or empty
text) clears `output[0]`; **basename 0–3 bytes** (`k = n−j−5 < 0`) writes a terminator at the signed index −4..−1 —
before the copied output but inside the stack frame — and keeps the copied string; **basename 4 bytes** clears
`output[0]`; **longer** reaches the declared `memcpy` boundary `RCX=output+12, RDX=input+j+1, R8=k+12` (the copy count
includes 12 bytes past `k`; nine long-string/early-separator length classes overlap the intervals, so the memcpy
contract is exceeded for those inputs — a contract limit, not an observed fault). So "whatever the stack held" is
conditional on the inherited bytes, not a raw stale name. Still live: the buffer's actual contents on the null-name
path and which fields a session loads — runtime only. A row is proposed
in [the batch record](../../_index/candidates/swe2contract-ddres-b14-0930/README.md).

| claim | evidence | tier |
|---|---|---|
| mode 0 = the block pack's `.efb`; its only consumer is the stub, and the global is read only by the teardown | Q1–Q4, Q9 | 1 |
| no mode-0 `.efb` ships; the mode-1 split 945 / 249 / 121 | Q11 (archive, TSV control), Q13 | 1 |
| a missing file fails through the queue and frees its block | Q5–Q10 | 1 |
| no mode-0 path's cache key collides with an archive name's | Q12 (unicorn control) | 1 |
| the null-name fields' path | — | runtime (**SD-194**, registered 2026-10-01) *(qualified 2026-10-02, OPUS: the static branch footprint on that path is settled under stated premises by ASTRA's SPEC-accepted sd194-stale-name-slice; the inherited bytes and which fields load stay runtime)* |

## 3. The loader contract

**The magic is a version selector with a hard reject, and it is compared one byte at a time** —
which is why no `EFX0` or `EFB0` byte sequence appears anywhere in `.text` (§6).

### EFX — `FUN_003EDAD0(data, size)`

| Field | Read by | Rejected if | Clamped to | Inert |
|---|---|---|---|---|
| `size` argument | `0x003EDAD0` `TEST EDX,EDX` | `size == 0` → `JZ 0x003EE25D`, immediate `RET` | — | — |
| `+0x00` magic, 8 bytes | three byte-loops at `0x003EDAF0`, `0x003EDB20`, `0x003EDB50` | matches none of the three → `0x003EDB5D` `JNZ 0x003EE24D` | — | — |
| `+0x08 .. +0x0F` | — | — | — | **yes — no reader in the function body** |
| chunk `+0x00` length | the walk cursor | — | — | — |
| chunk `+0x04` | branch gate, must equal `0x100` | ~~—~~ otherwise the chunk goes to the fallback `003EE2D0` | — | — |
| chunk `+0x06` type | the dispatcher | ~~unrecognised type exits the run loop~~ an unrecognised type goes to the fallback `003EE2D0` and the walk continues (corrected 2026-09-12) | — | — |

The version ladder, read from the instruction listing:

```
003edae4  LEA  RCX,[0x00D11C70]        ; "EFX0010"
003edaf0  ...  byte-compare loop, 003edaff CMP R8,0x8
003edb05  MOV  dword ptr [0x01EFF3B0], 0xA        ; version := 10
003edb13  LEA  R8,[0x00D11C78]         ; "EFX0009"
003edb35  MOV  dword ptr [0x01EFF3B0], 0x9        ; version := 9
003edb43  LEA  R8,[0x00D11C80]         ; "EFX0008"
003edb5d  JNZ  003ee24d                           ; no match -> reject
003edb69  MOV  dword ptr [0x01EFF3B0], ECX        ; version := 8  (ECX is the loop counter, == 8)
```

**The reject path is not a fallback.** It was worth checking, because the decompiler renders it as a
fall-through assignment that reads like *"default to 10 and carry on parsing"*:

```
003ee24d  MOV  dword ptr [0x01EFF3B0], 0xA
003ee257  ADD  RSP,0x60
003ee25b  POP  R15
003ee25d  RET
```

> **An unrecognised magic sets the version global to 10 and returns without parsing a single chunk.**
> The file is rejected, silently, with no diagnostic — and the effect simply never appears. **The
> side effect survives the rejection: `0x01EFF3B0` is left at 10.**
>
> **A modder must take from this that `EFX0008`, `EFX0009` and `EFX0010` are the only three accepted
> magics, and that a typo in the eighth byte costs the whole file with no error.**

`0x003EDB69` storing `ECX` rather than a literal `8` is the same trick in reverse: the byte-compare
loop exits with its counter at 8, and the version happens to equal it.

### EFB — `FUN_0026FB90(data)`

Same construction, two versions, and **a real failure return** rather than a void exit:

```
0026fbdd  LEA  RDX,[0x00915780]        ; "EFB0001"
0026fc00  ...  byte-compare loop, 0026fc0d CMP RCX,0x8
0026fc13  MOV  byte ptr [0x02F8F29D], 1
0026fc1f  LEA  RDX,[0x00915788]        ; "EFB0002"
0026fc3b  JNZ  0026fd75                            ; no match -> reject
0026fc47  MOV  byte ptr [0x02F8F29D], 2
...
0026fd75  CALL 0x0036C140                          ; release, paired with the 0036C1D0 at 0026fba6
0026fd7a  XOR  EAX,EAX                             ; return 0
```

**EFB rejects by returning 0**, and ~~releases the lock it took at entry~~ pops the arena selection it pushed at entry (`0x0026FBA6`; `0036C1D0` pushes a selection record tagged with its caller, `0036C140` pops it — a selector stack, not a mutex, and a pop below depth 0 spins forever at `0036C150`) before doing
so — so a rejected EFB is a clean failure a caller can see, where a rejected EFX is not.

**What loading normalises:** nothing in the header. ~~The `0x600` chunk zero-fill (§2) is the only~~
~~normalisation found, and it is per-chunk rather than per-file.~~ Per chunk, the `0x600` zero-fill and the binder `00333C80`, which rewrites an `EFX0009` / `EFX0008` record into the `EFX0010` layout *(corrected 2026-10-02, OPUS: `00333C80`+0x21 `mov ecx, dword ptr [01EFF3B0]`, +0x27 `cmp ecx, 9`; section 2b)*.

**The write path is not documented here.** No writer was found; the search that failed is named in §7.

**The binding table after the blobs (2026-09-12, FABLE, from D-8).** The loader's `+0x08` word is
the number of embedded EFX blobs, each `{u32 size; 12 bytes; EFX[size]}` (`0026FCE2`–`0026FD2D`,
the EFX handed to `003EDAD0`), and after the last blob it publishes the pointer `02F8F228` and the
header word `+0x0A` as a row count `02F8F23A` (`0026FD44`–`0026FD4F`). `0026F470` walks those rows:
byte `+0` = row type (`3` → a `0xA0`-byte row, `1` → `0x60` skipped, `0` ends), byte `+1` must be
`1`, byte `+4` = the **binding channel** (0–63 in the shipped files), `+5` a definition id looked up
through `0024F610`, and `+8`–`+0xB` four **per-weather-slot enable bytes** indexed by `slot + 1`.
The weather roll instantiates channel 0 (ambient, enabled for every slot) and channel `0x1F`
(weather-selective) — see [the weather roll](../../03-World-Area-Field/Weather/weather-probability-and-transition-roll.md)
§7. All 410 `.efb` decode with this grammar (2,615 rows, 0 malformed).

## 4. Key addresses

| Address | Role | Read? |
|---|---|---|
| `0x003EDAD0` | `FUN_003edad0` — the EFX loader; size gate at `0x003EDAD2` | ✅ |
| `0x003EDAE4` / `0x003EDB13` / `0x003EDB43` | the three `LEA`s that select `EFX0010` / `0009` / `0008` | ✅ |
| `0x003EDB7B` | `LEA R12,[R9 + 0x10]` — the EFX payload origin | ✅ |
| `0x003EE24D` | the EFX reject path — sets version 10, returns | ✅ |
| `0x01EFF3B0` | the EFX version global | ✅ |
| `0x0026FB90` | `FUN_0026fb90` — the EFB loader | ✅ |
| `0x0026FBDD` / `0x0026FC1F` | the two `LEA`s that select `EFB0001` / `EFB0002` | ✅ |
| `0x0026FD75` | the EFB reject path — releases and returns 0 | ✅ |
| `0x02F8F29D` | the EFB version global | ✅ |
| `0x00D11C70` `0x00D11C78` `0x00D11C80` | `.rdata` — `EFX0010`, `EFX0009`, `EFX0008` | ✅ |
| `0x00915780` `0x00915788` | `.rdata` — `EFB0001`, `EFB0002` | ✅ |
| `0x003A7E80`, `0x003A79C0` | per-chunk handlers for the `0x700` and `0x600` families | **read 2026-09-18 (FABLE), structurally.** `003A79C0(chunk)` takes the `0x600` chunk's index byte `+1`, stores it at `+4`, resets the 29 dwords from `+0x30` to the encoded null (`RuntimePointer_EncodeImageAddress(0)`, `003A79F0`..`003A7A01`), registers the record `chunk+4` in the table `[02EBEFA8] + 8 + index × 8` and bumps that table's count (`003A7A03`..`003A7A1F`), calls `00333C80(record)` and returns `record + 0xA0`, the next chunk. `003A7E80(chunk, len)` takes the `0x700` chunk's index byte `+0`, writes it as a word at `record+0xC0` and byte `+2` at `+0xC2` (`record = chunk+4`), registers the record in `[[02EBEFA0]] + index × 8`, calls `004FF270(record, [02EBB738] + record)` and returns `chunk + 4 + len`. ~~What `00333C80` (889 B) and `004FF270` (55 B) do to the records is not read.~~ *Corrected 2026-09-30 (SWE2-CONTRACT, DD batch 10): both are read in §2b. `00333C80` rewrites an `EFX0009` / `EFX0008` record into the `EFX0010` layout and recomputes the lane-count nibble at `+0x16`. `004FF270` relocates the `0x700` record's stored offsets by subtype.* |
| `0x00333C80` | the `0x600` version normaliser and lane-count nibble (§2b, SWE2-CONTRACT DD batch 10) | ✅ |
| `0x004FF270` | the `0x700` relocator: four subtypes, fixed sizes `0x160`–`0x300` (§2b) | ✅ |
| `0x00377DC0` / `0x003788F0` / `0x00378230` | the map's `.efb` request (a fixed `0x43D170`-byte block), its parse completion, and the teardown that frees it after its contexts (§2b) | ✅ |

## 5. Corpus survey — and what NOT opening a file costs

**From the archive index, which is the whole of the corpus evidence available here:**

| | `.efx` | `.efb` |
|---|---:|---:|
| files | **3,288** | **410** |
| bytes | 4,579,689,088 | 226,292,720 |
| smallest | 1,840 | 7,584 |
| largest | 25,310,800 | 4,444,528 |
| tree | `ps2data/effect_finish` | `ps2data/efb` |

**What was missing, stated plainly when this sheet was written:** no per-file magic distribution, so
the split between `EFX0008` / `0009` / `0010` across the 3,288 files was unmeasured, and likewise
`EFB0001` / `EFB0002` across 410. **That gap is now closed by the audit pass in §6b, and the answer
is worth more than the arithmetic.**

| accepted by the loader | files that use it |
|---|---:|
| `EFX0010` | **3,284** |
| `EFX0008` | **4** |
| `EFX0009` | **0** *(as a file; **1** embedded stream, `alc1007.mpk` - 2026-09-29)* |
| `EFB0002` | **410** |
| `EFB0001` | **0** |

> ~~**Two of the five accepted versions ship in no file at all**, and a third ships in four.~~ **Corrected 2026-09-29 (FABLE,
> GI-8):** only `EFB0001` ships nowhere. Counting the EFX streams *inside* files too, `EFX0009` ships once (embedded in
> the map-control plan `plan_master/map_ctrl/alc10/alc1007/bin/alc1007.mpk`) and `EFX0008` seven times (the four
> `l0000.efx`, two blobs in `alc0201.efb` / `alc0202.efb`, one stream in `rui0105.mpk`). The
> loader's version space is **capacity the shipped game does not use** — the same shape as EBP's
> `section_017` (a live handler with zero users). A modder reading §3's "these are the only accepted
> versions" now also knows which are *exercised*: ~~writing `EFX0009` is accepted by code that no
> shipped file has ever taken through.~~ *(see the correction above)*.
>
> **And the four `EFX0008` files are one logical file.** They are `l0000.efx` under `ch`, `cn`, `jp`
> and `kr` — 180,448 bytes each, the same event effect in four locale trees, and **absent from every
> other locale**. So the true statement is *one surviving `EFX0008` asset*, not four.

**The `README`'s open question is settled, and the answer is neither of the two on offer.** It asked
whether `.efx` and `.efb` are a container and its payload, noting the different directories as weak
evidence against. **They are not container and payload — they are two formats sharing one container
convention**, each with its own loader, its own magic family, its own version space and its own
version global. The shared convention is specific: an 8-byte NUL-terminated ASCII magic ending in a
version number, compared byte-by-byte, a 16-byte header ~~whose second half nothing reads~~ whose `+0x0C` is the stream length four of the loader's callers pass *(corrected 2026-10-02, OPUS: `003B0660`+0xDF `mov edx, dword ptr [rbx + 0xc]` before the loader call; section 2b)*, and a
payload at `+0x10`.

## 6. Falsification pass — 2026-09-05

| attack | result |
|---|---|
| Is the magic checked at all? | **Yes, and the search that would have missed it is named.** `EFX0`, `EFB0`, `EFX` and `EFB` occur **0 times in `.text`** — the byte-at-a-time comparison against a `.rdata` string leaves no immediate. The same scan finds `cmp dword ptr [rcx],'CAM7'` at `0x002561CA` and `SRYK` at `0x001F43DA`, so the instrument detects the construct when it is there. |
| Could the decompiler have invented the control flow? | **It did, on the one branch that mattered.** Its rendering of the EFX reject reads as *"set version 10 and continue"*; the listing shows `JNZ 0x003EE24D` → set 10 → `RET`. §3 follows the listing, and the difference is parse-anyway versus reject-silently — opposite advice to a modder. |
| Are these really versions, not filenames? | Three consecutive `EFX00nn` strings referenced from **one function** at three `LEA`s `0x2F` apart, each followed by an 8-byte compare and a distinct constant store into **one global**. A filename table would not be consumed that way. |
| Does the claim rest on a file? | **No file was opened**, and that is stated at the top rather than buried. Everything is the loader's own parse. |
| Is `+0x08..+0x0F` really unread? | **No reader in these two function bodies.** That is not the same as inert across the engine — another function handed the same buffer could read it, ~~and that search was not run~~ *(answered: see §2b - `003B0660`+0xDF reads `+0x0C` before calling the loader; 2026-10-02, OPUS)*. §7. |
| Is `EFB4305` a third EFB version? | **No.** It matches the `EFB\d{4}` pattern but is not referenced by the loader, which compares against exactly two strings. Recorded because the regex found it and a reader will find it too. |

**The killer observation for the central claim** — *"three accepted EFX magics, everything else
rejected"* — would be a fourth accepted magic reached by another path, or a caller that parses an
EFX buffer without going through `0x003EDAD0`. Neither was searched for; see §7.

## 6b. Independent audit pass — 2026-09-06, `repos-1e`

**This pass exists to supply the half the sheet says it lacks.** The author flagged, at the top and
in §5, that **no file had been opened**. I have the archive mounted, so the corpus was measured
rather than only checked. Program state: GN160 (`gzf fa0db293…`), `FFXII_TZA.vbf` as shipped.

**The corpus, now measured.** Every `.efx` and `.efb` entry's first 8 bytes read from the archive:

| | sheet (index only) | measured |
|---|---|---|
| `.efx` files | 3,288 | **3,288** |
| `.efb` files | 410 | **410** |
| `.efx` magic split | *unmeasured* | **`EFX0010` × 3,284, `EFX0008` × 4, `EFX0009` × 0** |
| `.efb` magic split | *unmeasured* | **`EFB0002` × 410, `EFB0001` × 0** |
| files whose magic is outside the accepted set | — | **0** |

**Every `.rdata` constant the sheet cites holds the string it claims** — `0x00D11C70` `EFX0010`,
`0x00D11C78` `EFX0009`, `0x00D11C80` `EFX0008`, `0x00915780` `EFB0001`, `0x00915788` `EFB0002` —
read from the image, not from the listing.

**The cited instructions reproduce.** `0x003EDAD0 test edx,edx` / `0x003EDAD2 je 0x3ee25d` is the
`size == 0` gate; `0x003EDAE4 lea rcx,[rip+0x924185]` resolves to `0x00D11C70`; `0x0026FBDD` and
`0x0026FC1F` resolve to the two EFB tags; `0x003EDB5D jne 0x3ee24d` is the EFX reject.

**§6's correction of the decompiler is confirmed, and it is the sheet's most important sentence.**
The reject path is four instructions and it does not parse anything:

```asm
003EE24D  mov  dword ptr [rip + 0x1b11159], 0xa   ; version global <- 10
003EE257  add  rsp, 0x60
003EE25B  pop  r15
003EE25D  ret
```

**It returns immediately.** "Reject silently" is right and "default to 10 and carry on" is wrong —
opposite advice to a modder, exactly as §3 and §6 say. The global it writes is `0x01EFF3B0`, which
§3 already names and already flags as surviving the rejection; I record only that both check out
against the bytes. *(I drafted this row as a contribution before noticing the sheet had it four
times over. Recording the near-miss rather than the claim: **an auditor adding a "detail the sheet
lacks" should grep the sheet for it first**, which is the same mistake as reading a mention for a
declaration, one rung down.)*

**§3's byte-at-a-time claim is confirmed by the section split.** `EFX0` occurs **3 times in the whole
image and all three are in `.rdata`**; `EFB0` occurs **2 times, both `.rdata`**. Zero in `.text` —
so the sheet's explanation for why a `.text` scan finds nothing is right, and it is a *third* distinct
mechanism for that outcome alongside `.sab`'s `.rdata` memory-operand compare and the containers whose
magic is never read at all. **Three formats, three reasons a `.text` scan comes back empty**, which is
why the magic-scan rule needs all of them.

**What was attacked and held.** (a) That the magic compare might be a prefix match rather than eight
bytes — the constants are NUL-terminated 8-byte strings and the corpus contains no near-miss magic
to exploit either way. (b) That the "no file opened" caveat might be hiding a wrong layout — the
measured magic distribution is consistent with §2 in every one of 3,698 files. (c) That `EFX0009`
might simply be rare rather than absent — it is absent, 0 of 3,288.

**What this pass did not do.** It read **the first eight bytes of each file only**. §2's `+0x08`
second header half and the payload at `+0x10` ~~remain unmeasured, so §7's caveats about them stand~~ *(answered: see §2b, measured 2026-09-30; 2026-10-02, OPUS)*
unchanged. **The version question is closed; the body of the format is not.**

## 7. What this document does not claim

- **Any chunk's meaning.** Seven type constants are named and their *sizing* arithmetic is given;
  what a `0x600` or a `0x710` chunk *is* is not established. ~~`FUN_003A7E80` and `FUN_003A79C0` are
  the handlers and neither was read.~~ *Corrected 2026-09-30 (SWE2-CONTRACT, DD batch 10): both handlers were read
  2026-09-18 (§4), and their binders are read in §2b. The `0x600` record is an effect definition with an eleven-lane
  map and 29 request slots, and the `0x700` record is a fixed block of four sizes with relocated offsets into its tail.*
- ~~**The version split across the shipped corpus** — see §5. This is the gap a single census closes.~~ *Corrected
  2026-09-30 (SWE2-CONTRACT, DD batch 10): closed by §5 / §6b and GI-8.*
- ~~**That `+0x08..+0x0F` is engine-wide inert.** No reader in the two loader bodies; **no search was
  run across other functions that receive the buffer**, so the `Inert` column in §3 is scoped to
  those functions and says so.~~ *Corrected 2026-09-30 (SWE2-CONTRACT, DD batch 10): it is not inert. `+0x0C` is the
  stream length, which four of the loader's six callers read and pass in (§2b, E3). `+0x08` is `1.0` in every shipped
  file, and no reader of it was found on those paths. The §3 `Inert` column stays true for the loader body.*
- ~~**That `0x003EDAD0` and `0x0026FB90` are the only entry points.** Their callers were not read.~~ *Corrected
  2026-09-30 (SWE2-CONTRACT, DD batch 10): `003EDAD0` has six direct callers, the six constructors of §2's table, and
  no rip reference. `0026FB90` has one, the thunk `0026FF90` called from the map's `.efb` completion `003788F0`. A
  caller reaching either one through a stored pointer is outside this call census.*
- **The write path.** No writer found; the failed search was a scan for the magic strings and for
  references to the two version globals.
- ~~**Anything about `.efb`'s internal structure beyond its header.** The EFB loader's body past
  `0x0026FC4E` was not read in this block.~~ *Corrected 2026-09-30 (SWE2-CONTRACT, DD batch 10): the body past
  `0026FC4E` is read in §3's binding-table paragraph (FABLE, D-8): the blobs and the row table. §2b adds the header
  word `+0x0C` (0 in all 410 files) and the blob sizes.*

## 8. Related

- [`README.md`](README.md) — the family, and the container/payload question this sheet settles
- [`../../_index/ASSET-FORMATS.md`](../../_index/ASSET-FORMATS.md) §5 — the 48-extension census and dispositions
- [`../../25-EBP-Script-Container/Sections/section-016.md`](../../25-EBP-Script-Container/Sections/section-016.md)
  — the other versioned-magic contract in this database: `FF12POS3`, where the check is a single
  byte and the version selects a record layout rather than a parser

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Audio — CLIENT.** `FUN_003a1650`, owned by that layer, calls `0036B130` on this page. That caller is an audio lookup that resolves an object through `0036B130` and, when it exists, hands it to `002DEC10`; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**CombatAction — CLIENT.** `FUN_002fc3c0`, owned by that layer, calls `0024F410` on this page. That caller is a 183-byte dispatcher: `byte[rec+0x23] & 0xF`, bounded to 7, into an eight-entry jump table; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).
- **Resource - CLIENT and SERVICE (48 edges).** `0024F410`, `0024F4D0`, `003AB7F0`, `003AB940` (+5 more) are called by bodies filed to Resource: ResourceTable_ResolveEntryByIndex (`002ED570`), `003B37E0`, ResourceEntry_GetResolvedBasePointer (`00409600`), `00409730` (+11 more); `002FC3C0`, `002FC4A0`, `003B0660`, `003B2310` (+3 more) reach bodies filed to Resource: `001D6EC0`, `002DF960`, `002DF980`, ResourceTable_ResolveEntryByIndex (`002ED570`) (+13 more) - shared machinery across the layer boundary, no shared ownership.
- **Script_VM_Native_Bridge - CLIENT (1 edge).** `0036B130` is called by bodies filed to Script_VM_Native_Bridge: `0050D5E0` - shared machinery across the layer boundary, no shared ownership.
- **UI - CLIENT (2 edges).** `003B29B0` is called by bodies filed to UI: `00558FB0`, `00561390` - shared machinery across the layer boundary, no shared ownership.

