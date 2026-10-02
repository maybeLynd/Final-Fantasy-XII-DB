---
system: Legacy PS2 GS texture-mip local-memory budget
category: 17-Presentation-Rendering
status: AUDITED
owner_layer: CodeDomain:Presentation.LegacyPS2GS (proposed) - Movement owns the trigger, not this
evidence_tier: 1
verified_against:
  gzf_sha256: 2ed8affb732f0def0a7852e0788298ae36b81206099dd1712f59825fc1c00bb9
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: additive-annotation across GN158 -> GN161 - every step of the certified lineage is additive on the canonical record (internal 38161, owner 9409 and finalNo 585 constant at all five generations; each step's codeDomain and explicit rise equals its unresolved fall). Of the functions classified since GN158 this document cites none of batch R109's 109; the 21 classified before GN160 are named in AUDIT-LOG's batch records and not in a tracked machine-readable list, so identity is not claimed. Voided by any delta that removes or rewrites a comment, tag, name, prototype or body range.; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md, lineage extension (twenty ledger figures across five generations)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  snapshot_sha256: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  previous_parent: 381d2aea82b96d7af781844e191d9b92a37e93bd2d4ff276a33ba56e7307461b
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-02
audit:
  passes: 1
  last_pass: 2026-09-02
  last_pass_state: reverification-against-current-parent
  crossref_clean: true
  reopened_count: 1
---

# Legacy PS2 GS texture-mip local-memory budget

> The PC port still budgets textures against a **4 MiB PlayStation 2 Graphics Synthesizer
> local memory model**, with 8 KiB pages and GS pixel-storage formats. This is a genuine
> console fossil, live in the shipping executable.

## 1. What the player sees

Nothing directly - and that is the point. This is a derived table that decides which textures
get a compact slot in a retained GS-style memory model when a field area's resources are
rebuilt. A modder adding high-resolution textures to a zone is competing for a **fixed 4 MiB
budget**, and textures referenced only once are never admitted at all.

## 2. Native mechanism

`002F7380` tears down and rebuilds a derived table at object `+0x218` / `+0x228`:

1. walk the 0x60-byte source texture record bank;
2. for each, compute the **complete mip-chain footprint** via `00466190`, which reads a
   format code, a mip count capped at 7, and two dimensions, then calls `003A1E50(w, h, fmt)`
   per level, halving both dimensions each time;
3. compute the maximum ~~single-image~~ single-record mip-chain footprint *(corrected 2026-10-02, OPUS: `002F7380`+0xB1 `call 00466190` (the chain sum), +0xB6 `cmp esi, eax`, +0xBB `cmovl esi, eax`)* and a weighted aggregate; publish both through
   `00467B10` / `00467B00`;
4. clear every record's derived reference/slot field;
5. obtain the remaining budget from `00467AA0`;
6. walk the 0x30-byte reference descriptors selected by the current dynamic mask, counting
   references per texture (including linked/continuation records);
7. **reference count <= 1 -> slot `-1`** (ignored entirely);
8. for multiply-referenced textures, admit the full mip chain only while
   `running + current < budget` (**strictly** less);
9. admitted textures get consecutive compact slot indices; rejected get `-1`;
10. if any were admitted, write the count to `+0x228`, allocate exactly `count * 40` bytes to
    `+0x218`, and zero **33 of each record's 40 bytes** — four qwords and one byte;
    `+0x21`..`+0x27` are never written.

### Why this is specifically PS2 GS

The evidence is internal, not architectural analogy:

- `00466220` accepts **exactly** formats `0x14`, `0x24`, `0x2C` - the GS 4-bit indexed
  family (PSMT4 / PSMT4HL / PSMT4HH). Its whole body is
  `tmp = fmt - 0x14; if (tmp & 0xE7) return 0; return fmt != 0x1C;`
- `003A1E50` reproduces **GS page geometry** through a 4-target jump table and a 43-byte PSM
  dispatch table, and every class yields a minimum allocation of `0x800` 32-bit words:

| Class | Alignment | Divisor | Minimum |
|---|---|---:|---:|
| A | 32 x 64 | 1 | 2048 words |
| B | 64 x 64 | 2 | 2048 words |
| C | 64 x 128 | 4 | 2048 words |
| D | 128 x 128 | 8 | 2048 words |

- `00467AA0` derives the budget as
  `threshold = (0x1007FF - used) & 0xFFFFF800`, where
  `used = 3*(globalW*globalH) + runtimeTotalA + runtimeTotalB`.

In 32-bit-word units: `0x100000` words = **4 MiB** arena, `0x800` words = **8 KiB** page.
Those are exactly the GS local memory size and page size.

- Sibling Presentation code emits literal GS transfer register IDs `0x50` `0x51` `0x52` `0x53`
  (BITBLTBUF / TRXPOS / TRXREG / TRXDIR).

### Ownership boundary

`002F7380` is called from a **Movement**-owned navigation/resource dirty dispatcher. Movement
owns the upstream resource/dirty transaction. The callee's mechanism - GS storage geometry,
Presentation budget helpers, Presentation transfer siblings - is Presentation.
**Caller ownership is not inherited.** This is the canonical worked example of the
PrimaryOwner / CodeDomain split.

## 3. Key addresses

| Address | Working name | Body | Role |
|---|---|---:|---|
| `002F7380` | `Presentation.LegacyPS2GS.TextureMipLocalMemoryBudgetAndReferenceSlotTableRebuild` | 723 B | the rebuild — **classified 2026-09-02, GN checkpoint** |
| `00466190` | mip-chain footprint | - | loops `003A1E50`, halving dimensions |
| `003A1E50` | GS format/page size | 144 B | jump table @ `003A1EE0`, PSM table @ `003A1EF0` |
| `00466220` | GS 4-bit PSM classifier | 25 B | accepts `0x14`, `0x24`, `0x2C` only |
| `00467AA0` | remaining aligned budget | 41 B | `(0x1007FF - used) & 0xFFFFF800` |
| `00467AD0` | arena policy seed + reserved-block publish | 42 B | writes `0x4000`, and `(w*h*3) >> 6` = the reservation **in 256-byte GS blocks** |
| `00467B00` / `00467B10` | publish aggregate / maximum | 7 B each | |
| `00244200` | GS transfer emit | 455 B | registers `0x50`->`0x51`->`0x52`->`0x53` |
| `0039D200` | GS extent encode | 484 B | 14-bit graphics addresses, `ceil(w/64)` |
| `0026E8D0` | Movement resource reconfiguration | - | upstream owner transition |
| `0026E290` | Movement dirty observation | - | the actual caller — **verified sole caller** |
| `003EC8A0` | allocation adapter | 35 B | 10 callers; support for the 40-byte slot records |
| `003EC8D0` | allocation/zero routine | 59 B | 10 callers; reaches a CRT routine |

## 4. Data structures

```
Source texture record          0x60 bytes      (stride proven twice: 00466190's
                                                lea rax+rax*2 / shl 5, and 002F75B8)
  +0x00  u8    formatCode       GS PSM; classified by 00466220, and sorted into four
                                page-geometry classes by the table at 003A1EF0
  +0x05  u8    mipCount         clamped to 7 (cmp eax,7 / cmova at 004661C5)
  +0x06  u16   width            passed to 003A1E50, halved per level
  +0x08  u16   height           passed to 003A1E50, halved per level
  +0x0C  u16   continuationFlag non-zero = continues the previous record, so a
                                reference counts against a whole RUN (002F7526)
  +0x0E  int16 refCount THEN derivedSlot   -1 (0xFFFF) = rejected/ignored

Reference descriptor           0x30 bytes
Derived slot record            0x28 (40) bytes; 33 INITIALISED, +0x21..+0x27 NEVER WRITTEN
  +0x00/+0x08/+0x10/+0x18  u64  zeroed at allocation; only +0x00 is re-cleared per frame
  +0x20                    u8   zeroed at allocation, set to 0xFF per frame
  +0x21..+0x27             ---  uninitialised allocator memory for the table's life

Owning object
  +0x218  ptr  derived slot table
  +0x228  u32  admitted slot count

GS model  (every quantity is a hardcoded constant - nothing scales with PC resolution)
  arena      0x100000 words = 4 MiB          GS local memory
  page       0x800    words = 8 KiB          GS page    (budget alignment)
  block      0x40     words = 256 B          GS block   (reservation unit)
  modelW     0x022D8EAC = 0x200 = 512        single writer, constant
  modelH     0x022D8EB4 = 0x1C0 = 448        single writer, constant  -> PS2 NTSC 512x448

  reserved   w*h*3 words = 2.625 MiB         three 512x448 x 4B surfaces, 0.875 MiB each
  published  0x02CA5FF4 = (w*h*3) >> 6 = 10752 blocks
  budget     1.375 MiB = 176 pages, minus two runtime totals

  reserved + budget = 2.625 + 1.375 = 4.000 MiB exactly
```

**`+0x0E` is 16-bit, and it means two different things.** *(Corrected 2026-09-15 (OPUS),
`OPUS-ABI-DERIVEDSLOT-IS-16-BIT`.)* This block previously declared the field `s32 derivedSlot` with no
offset. **Every access to it is a WORD access and there is no 32-bit access to `+0x0E` anywhere in the
723-byte body** — `002F7445` clears it, `002F7500` and `002F752F` increment it in pass 2, `002F758E`
tests it against 1 and `002F75B0` writes the result in pass 3. The `-1` is `0xFFFF` from
`002F7587 or ebp, 0xffffffff` stored as a word: right in value, wrong in width. **A consumer sizing the
field at 4 bytes reads `+0x0E..+0x11` and takes two bytes belonging to the next field.**

And the name was only half of it. **`+0x0E` is a reference COUNT while pass 2 runs and is then
OVERWRITTEN with the slot index during pass 3**, which
[field-init-weather-to-legacyps2gs-rebuild.md](../../03-World-Area-Field/Weather/call-chains/field-init-weather-to-legacyps2gs-rebuild.md)
already records and this block did not: it named only the pass-3 meaning. The four offsets above were
absent too, and all four are read directly from the bodies.

**The derived slot record is NOT zero-initialised, and the shortfall is seven bytes per element.**
*(Corrected 2026-09-15 (OPUS), `OPUS-ABI-SLOTRECORD-NOT-ZERO-INITIALISED`.)* The post-allocation loop is
`002F7600`–`002F7628` and its body is exactly five stores per element — `002F760B`, `002F7610`,
`002F7615`, `002F761A` as qwords and `002F761F` as a byte, with `r9` zeroed at `002F75F0`. Since
`002F7607 lea rcx, [rcx+0x28]` advances from zero, those resolve at `+0x00`, `+0x08`, `+0x10`, `+0x18`
and `+0x20`: **33 of the 40 bytes.** The per-frame reset in the consumer writes even less — only
`+0x00` and `+0x20`. **No other writer of the table was found**, so `+0x21`..`+0x27` are uninitialised
allocator memory for the life of the table, and the table is reallocated on every zone rebuild.

This is the same class of fact the registry already records for `PresentationEntryReferenceNode`, whose
row notes that `+0x28`..`+0x2F` are untouched by reset and release. *"Zero-initialised" is exactly the
kind of promise a consumer relies on*, which is why it is corrected here rather than left as a rounding
of the truth.

PSM dispatch is indexed by `format - 2`:

| Format | Geometry | Identity |
|---|---|---|
| `0x02` | 64x64 / 2 | GS 16-bit |
| `0x0A` | 64x64 / 2 | GS 16S |
| `0x13` | 64x128 / 4 | GS 8-bit indexed |
| `0x14` | 128x128 / 8 | GS 4-bit indexed |
| `0x1B` | 64x128 / 4 | GS 8H |
| `0x24` | 128x128 / 8 | GS 4HL |
| `0x2C` | 128x128 / 8 | GS 4HH |
| others | 32x64 / 1 | default |

## 5. Call chain

```
committed Weather Slot / field resource selection
  -> 00379290   WorldAreaField -> Movement bridge   (or 00379630 alternate rebuild)
     -> 0026E8D0   Movement resource-bank reconfiguration   [AUTHORITY 03 -> 06]
        -> dirty state set
  -> 0026E290   Movement observes dirty
     -> 002F7380  THIS   [Presentation mechanism, Movement trigger]
        -> 00466190 -> 003A1E50   per-texture mip footprint
        -> 00467AA0               remaining budget
        -> allocate count*40 slot table
```

**Upstream:** Movement resource reconfiguration, itself driven by field-resource
initialization - which is driven by the committed Weather Slot.
**Downstream:** the derived slot table consumed by the legacy GS presentation path.

**Do not confuse with:** modern D3D11 GPU residency. This is not a PC texture-memory manager.

## 6. Modding notes

- **Best intervention point:** the upstream Movement reconfiguration `0026E8D0`. Set the
  resource configuration and let the dirty path regenerate this table naturally.
- **Never call `002F7380` directly** to "refresh" textures. It is derived state.
- **Budget reality for texture mods: a fixed 1.375 MiB / 176 GS pages**, minus two runtime
  totals. This is not an approximation and it does not scale with your display resolution:
  both dimensions feeding the reservation are hardcoded constants (512 x 448), so the 4 MiB
  arena less the 2.625 MiB surface reservation is the same on every machine. Admission stops
  at the first texture that would cross the threshold - so ordering matters, and singly-
  referenced textures never get a slot regardless of budget.
  *(Precision, 2026-09-14 (FABLE): the two runtime totals are the rebuild's own two totals, published just before the call: `00467B10` stores the **largest single-record mip-chain footprint** (`00466190`, the running maximum in `esi`, `002F7436`–`002F743B`) at `02CA6004`, and `00467B00` stores **the sum of 1 per 4-bit-indexed record and 4 per other record** (`00466220` selects `edx` = 1 or 4, `002F744A`–`002F7455`) at `02CA6008`. Because the budget is rounded up to whole pages, it stays at 176 pages only while the two totals together are under `0x800` words. "Fixed" therefore means machine-independent, not independent of the area's texture bank.)*
- **XIIOnline:** never replicate this table, Movement dirty/cache state, or GS allocations.
  It is local derived state. A runtime weather change does **not** trigger this path; only
  field initialization/rebuild does. Forcing it would make the mod *less* native-coherent
  than single-player.

## 7. What is not known

- [x] Identity of the three reserved surfaces (**D-5**) - **advanced 2026-09-02**. Their
      geometry is now fact: **three 512 x 448 surfaces at 4 bytes/pixel**, 0.875 MiB each.
      ~~Only the role labels (front / back / Z is the obvious reading) remain inference.~~
      **ANSWERED 2026-09-26 (FABLE, Claude Opus 5.5): the GS state builder names two of them, and the third is never
      selected.** Static.
      - The seed `0036D280` sets width `0x200`, height `0x1C0` and a frame index of 0. `0036D2F0` computes pages
        per surface as (height × width) >> 11: 112 GS pages of 2048 words.
      - `0036D400` composes the GS registers:
        - `FRAME_1` = index × 112 as the frame base, width ÷ 64 as the buffer width, and PSM 0 (32-bit colour).
          With index 0 that is the **first** surface: the draw target.
        - `ZBUF_1` = 224 as the Z base, PSM 1 (24-bit Z), not scaled by the index. That is the **third** surface:
          the Z buffer.
        It emits both as register records (`0x4C`, `0x4E`), and the renderer copies them into its own packets.
      - The **second** surface would be selected only by a frame index of 1. The index has one rip-relative write
        in the image, the seed's 0, so this build never draws to it. That it was the PS2 double buffer's other half
        is the reading of the reservation, not something the code shows.
      - Control: `_index/candidates/d5-reserved-surfaces/surfaces.py`, 6 checks, FAILS 0. Its planted negative
        requires that the Z base is not scaled by the index.
- [x] Purpose of the 1-vs-4 accounting factor for the 4-bit PSM family (open question **D-6**). *(NO ADMISSIBLE SOURCE, reviewed and signed 2026-09-26 by OPUS; see the register row D-6.)*
- [x] **UQ-212.** Designer-facing names for the texture records and slot records. *(OUT OF EVIDENCE BOUNDARY
  2026-09-28, applied by FABLE (Claude Opus 5.5) on OPUS's non-author signature: the names exist only in the
  unshipped source and `FF12X64.pdb`. Both records are PODs that no RTTI descriptor or loaded container names.
  Closed for the gate, unanswered in fact. See the register row UQ-212 and
  [the signature](../../_index/candidates/uq212-oeb-signature-opus/README.md).)*

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| Full rebuild algorithm | complete body of `002F7380` (723 B, plain-body `15594f61...ac8583`) | 1 |
| GS 4-bit PSM classifier accepts exactly 3 values | complete body of `00466220` (25 B, `98e5090e...5b864`) | 1 |
| GS page geometry, 8 KiB minimum in all 4 classes | complete control flow of `003A1E50` (144 B, `b5ee1026...cf8a1`) + jump table `003A1EE0` (16 B, `a5e5bb0a...c2fde`) + PSM table `003A1EF0` (43 B, `5c3b1961...ee6f8c`) | 1 |
| 4 MiB arena / 8 KiB quantum | complete body of `00467AA0` (41 B, `d77d4623...b96df`) in 32-bit-word units | 1 |
| GS transfer register family | `00244200` (455 B) emits `0x50`->`0x53`; canonical V120 sibling `003A22A0` owns the same sequence | 1 |
| Register identities | PS2 SDK / PCSX2 `GSRegs.h`: BITBLTBUF/TRXPOS/TRXREG/TRXDIR; GS local memory 4 MiB, page 8 KiB | 10 |
| Presentation not Movement | sealed V120 Movement exit-gate evidence explicitly assigns the dataset side to Presentation | 1 |

**Superseded readings:** earlier conservative names
`Presentation.Rendering.ImageMipStorageBudgetAndReferenceSlotTableRebuild` and
`Presentation.LegacyPS2GS.ImageMipLocalMemoryBudgetAndReferenceSlotTableRebuild` are
superseded; `TextureMip` is justified by the exact PSM classification plus per-record
mip-chain traversal.

**Status:** **APPLIED AND PERSISTENCE-CERTIFIED**, GN checkpoint 2026-09-02. Fenced against the
live parent (body 723 B, gate hash `ed6a32eb…0140ab5`), applied with exact expected count,
diff clean with immutable drift 0, packed with `PACK_PASS`, fresh-imported and reproduced.

**Correction found during the apply challenge.** Re-deriving the call chain from the live
graph showed two callees the document did not list: `003EC8A0` (35 B) and `003EC8D0` (59 B),
each with 10 callers, the latter reaching a CRT routine. They are the allocate/zero support
behind step 10 — the document described that behaviour but never named the helpers. Added to
§3. This did not change the classification: it is an omission, not a falsification.

## 9. Related

- [`../../06-Movement-And-Navigation/`](../../06-Movement-And-Navigation/) - owns the trigger
- [`../../03-World-Area-Field/Weather/call-chains/field-init-weather-to-legacyps2gs-rebuild.md`](../../03-World-Area-Field/Weather/call-chains/field-init-weather-to-legacyps2gs-rebuild.md)

## Re-verification 2026-09-02 (AH-12)

Stamped against parent `381d2aea...`; re-checked against the current `2ed8affb...`.

**Addresses:** 17 cited plus the two `.text` tables `003A1EE0` / `003A1EF0` - all confirmed
legitimate in iteration 61. **Three bodies re-read** in the current parent.

### The three checkable claims, all confirmed

| Claim | Read in the current parent | Verdict |
|---|---|---|
| `00467AA0` = `(0x1007FF - used) & 0xFFFFF800` | `((h*w*-3 + 0x1007ff) - _DAT_02ca6008) - _DAT_02ca6004 & 0xfffff800` | exact, **including** the composition of `used` |
| `00467AD0` seeds `0x4000` | `_DAT_02ca5ff0 = 0x4000;` | exact |
| `00466220` accepts `0x14`, `0x24`, `0x2C` only | `(*p - 0x14U & 0xe7) == 0 && *p != 0x1c` | exact |

The classifier was checked **exhaustively rather than by reading**: enumerating all 256 byte
values through `(v - 0x14) & 0xE7 == 0 && v != 0x1C` yields `{0x14, 0x24, 0x2C}` and nothing
else. That is stronger than a body read, because it cannot be fooled by misreading a mask.

### An attempted falsification that failed - and paid for itself

The document says the reservation is `3 * width * height`. If those were the **PC render
dimensions**, then at 1920x1080 the reservation would be 6.2 M words against a 1.0 M-word
arena: the subtraction would underflow, the unsigned budget would wrap to an enormous value,
`running + current < budget` would always pass, and **the entire budget would be a no-op** -
falsifying section 6's "budget reality for texture mods".

So the two globals were traced. Each has **exactly one writer**, both in `FUN_0036D280`:

```
0036d286   MOV dword ptr [0x022d8eac], 0x200    ; 512
0036d2ad   MOV dword ptr [0x022d8eb4], 0x1c0    ; 448
```

**512 x 448 is the PlayStation 2 NTSC framebuffer resolution.** They are compile-time
constants, never written again, and read by 26 sites across Presentation - including the GS
transfer emitter `00244200` and the GS extent encoder `0039D200`.

The hypothesis is **refuted and the document vindicated** - but the scan paid for itself,
because the model now closes numerically:

| Quantity | Words | Bytes | |
|---|---:|---:|---|
| arena `0x100000` | 1048576 | 4.000 MiB | GS local memory |
| reserved `w*h*3` | 688128 | 2.625 MiB | three 512x448 x 4B surfaces |
| budget `(0x1007FF-r) & ~0x7FF` | 360448 | 1.375 MiB | **exactly 176 GS pages** |
| **sum** | **1048576** | **4.000 MiB** | closes to the byte |

Two further facts fell out, neither previously recorded:

- **`00467AD0` publishes the reservation as GS blocks.** `DAT_02CA5FF4 = (w*h*3) >> 6`, and
  `>> 6` is division by 64 words = **256 bytes = one GS block** (32 blocks per 8 KiB page).
  10752 blocks x 256 B = 2.625 MiB - the same reservation, in the GS's own second unit. Arena,
  page and now block all quantise correctly, which is a **third independent confirmation**
  that the units are 32-bit words and not bytes.
- **The `0x7FF` bias rounds the budget up.** `(0x1007FF - used) & 0xFFFFF800` is
  `ceil((0x100000 - used) / 0x800) * 0x800`, so a non-page-aligned reservation is forgiven up
  to one page rather than truncated.

**Consequence for section 6:** the texture budget is not "~4 MiB minus some things", it is a
**~~fixed 1.375 MiB / 176 pages~~** at most 1.375 MiB / 176 pages on every machine, less the two runtime totals rounded to whole pages, so 175 pages or fewer once any texture record with a level is present *(corrected 2026-10-02, OPUS: `00467AA0`+0x17 and +0x1D subtract `[02CA6008]` and `[02CA6004]` before the `and eax, 0xfffff800` at +0x23; every class's minimum footprint is `0x800` words, section 6's precision)*. Section 6 now says so.

**Consequence for D-5:** the three reserved surfaces are now known to be **512 x 448 at 4
bytes/pixel, 0.875 MiB each**. Their count, geometry and depth are fact; only the role labels
remain inference. D-5 is advanced, not closed.

**Stamp advanced: three bodies re-read, one exhaustive enumeration, one refuted falsification
attempt.** A new reusable tool - `DumpDataXrefs.java` - was written for the writer scan, since
the call-graph edge dump records function-to-function edges only and cannot answer "who writes
this global".

## SWE2-EC7-38 update (2026-09-19) - `0039D200`

`0039D200` (484 B) is a call-free GS local-memory address packer - `and 0x3f`/`sar`/`shl` bit math with `0xfffffffe641fffff`/`0x664100000`/`0xfffff003ffffffff` masks over `02AEECF0`. Interior anchor `0039D275` (the `r9d` mask step).

## SWE2-EC7-38 update (2026-09-19) - `00244200`

`00244200` (455 B) is a mip-budget sibling - `022D8EAC`/`022D8EB4`/`022D8EA8`, `0039D0C0`/`00248EB0`/`00248E10`. Interior anchor `0024427B` (a `0039D0C0` call).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**UI — MECHANICAL (SWE2-EC7-38, 1 edge).** `00248EB0` — the shared helper this page cites inside `00244200` — is called by a body on the UI layer. Shared-helper fan-in; no UI relationship to the mip budget.

**CoreRuntimeScheduling — MECHANICAL (SWE2-EC7-55, 4 edges).** `001FBD80`/`001FBE50` — shared helpers this page cites inside `0039D0C0` — also edge to CoreRuntimeScheduling bodies (`001A1470`, `0022B8C0`). Shared-helper fan-in/fan-out; no scheduling relationship to the mip budget.
- **Movement - CLIENT and SERVICE (12 edges).** `002F7380`, `003EC8D0` are called by bodies filed to Movement: `0026E290`, `0026E760`, `0026E7D0`; MainLoop_UpdateAndRenderFrame (`0022B8C0`), `0026E8D0`, `00379290`, `00379630` reach bodies filed to Movement: `00263560`, `0026E8D0`, `0037CF00`, `003ECFD0` (+4 more) - shared machinery across the layer boundary, no shared ownership.
- **WorldAreaField - CLIENT and SERVICE (3 edges).** `0026E8D0`, `00379630` are called by bodies filed to WorldAreaField: `00379290`; MainLoop_UpdateAndRenderFrame (`0022B8C0`) reaches bodies filed to WorldAreaField: World_UpdateSimulationTick (`00314020`) - shared machinery across the layer boundary, no shared ownership.
- **ActorEntity - CLIENT and SERVICE (9 edges).** actor bodies `002628B0`/`0037B4D0` call `00263560`, while `00263560`/`00314020`/`0037CF00` reach `ActorManager_RunFieldRuntimePass` (`0025D9E0`), `00238B40`, `00312130`, `0025BFB0` and more - the world-tick path runs both ways across the boundary.
- **Audio - SERVICE (2 edges).** `00314020` reaches audio bodies `002DEBA0` and `00362850`.
- **Input - SERVICE (11 edges).** `MainLoop_UpdateAndRenderFrame` (`0022B8C0`) reaches input bodies `0017DE60`, `00182D40`, `InputGameplay_RebuildFrameSnapshotFromChannelHistory` (`002498B0`), `0035AE30` and seven more - the frame loop drives the input snapshot.
- **Party - SERVICE (4 edges).** `0022B8C0`/`00314020`/`0037CF00` reach `PartyFocus_CommitPendingPackedActorHandle_Thunk` (`00358BB0`), `PartyControl_UpdateControlledActorLocomotion` (`00358C60`), `PartyFocus_UpdatePrimarySecondaryActorProcessing` (`00358EE0`) and `PartyRoster_GetActorBySlot` (`00263750`).
- **Gameplay - SERVICE (3 edges).** `ActorManager_RunFieldRuntimePass` (`0025D9E0`) reaches `00234150`, and `0037B4D0` reaches `WorldActor_GetDefinitionByte12OrMinus1` (`002E9C00`) and `ActorHandle_GetPrimaryFormulaResourceByte` (`00321380`).
- **Resource - SERVICE (2 edges).** `MainLoop_UpdateAndRenderFrame` (`0022B8C0`) reaches `00324510` and `002628B0` reaches `0032E520` - resource-layer calls on the tick path.
- **Save_Load_Settings - CLIENT and SERVICE (4 edges).** `SaveLoad_ControllerLifecycleHandler` (`00582860`) calls `00182D40`; `0025D9E0`/`002628B0` reach `SaveImage_GetPersistentPayloadBase` (`002EF2B0`) and `SaveWrite_GetBusyFlag` (`00583920`).
- **Script_VM_Native_Bridge - MECHANICAL (20 edges).** all 20 edges are script-VM bodies (`003415D0`, `00341CB0`, `00342250`, `00342910`, `00342EC0` and fifteen more) calling `PartyRoster_GetActorBySlot` (`00263750`) - fan-in on one roster accessor.
- **CombatAI - CLIENT (1 edge).** `AiOrder_EvaluateAndResolveActionTarget` (`003014C0`) calls `WorldActor_GetDefinitionByte12OrMinus1` (`002E9C00`) - the AI target resolver consumes the definition-byte query.
- **CombatAction - CLIENT and SERVICE (3 edges).** `002FC3C0` calls `0032E520`, while `00234150` reaches `BattleUnit_SetupEngagedActionState` (`002FED60`) and `BattleUnit_ShouldEnterEngagedActionState` (`00308010`).
- **Story_Event_Quest_Hunt - MECHANICAL (12 edges).** all 12 edges are persistent-flag bodies (`PersistentFlag_Query*`/`PersistentFlag_Set*`, the `0032A8A0`-`0032AD60` block) calling `SaveImage_GetPersistentPayloadBase` (`002EF2B0`) - fan-in on the payload-base accessor.
- **RNG_Random_Selection - SERVICE (2 edges).** `AiOrder_EvaluateAndResolveActionTarget` (`003014C0`) reaches `BattleData_ResolveWeightedId` (`00308EC0`) and `RNG_SharedGameplayLCG_NextU32` (`00328370`) - the AI order path consumes the shared LCG.
- **Spawn_Encounter_Lifecycle - CLIENT (2 edges).** `0023A410` calls `BattleUnit_SetupEngagedActionState` (`002FED60`) and `BattleUnit_ShouldEnterEngagedActionState` (`00308010`) - one spawn-lifecycle body consulting the engaged-action state pair.
- **CombatFormula - SERVICE (2 edges).** `0023A410` reaches `00300520` and `00386C10` - formula-layer calls on the spawn-body path.
- **Status_Periodic_Terminal - SERVICE (1 edge).** `0023A410` reaches `0030FED0` - a single status-layer call.
- **Items_Equipment_Shops_License - MECHANICAL (4 edges).** All 4 edges are equipment/license setters (`BattleStats_SetEquipmentSlotByStatsIndex` `0031A410`, `BattleStats_SetLicenseNodeStateAndApplySideEffects` `00323910`, `BattleStats_SetEquipmentSlotDirect` `0031A630`, `BattleStats_SetEquipmentSlotByMappedId` `0031A510`) calling `0030FED0` - fan-in on one status-layer body, not a per-caller relationship.
- **Rewards_Progression_Economy - MECHANICAL (2 edges).** `BattleStats_AdvanceLevelToTargetAndRecomputeGrowth` (`0030C650`) and `0030C470` call `0030FED0` - the same shared callee as the Items pair.

## SWE2-EC7-39 update (2026-09-19) - `003A22A0`

`003A22A0` (413 B) is the canonical V120 sibling the page names - `003A2090`/`0024B150` pairs plus `003A1FE0`/`003A1F20`/`003A21A0`. Interior anchor `003A22CF` (a `003A1FE0` call).

## SWE2-EC7-55 update (2026-09-19) - `0039D0C0`

`0039D0C0` (264 B) is a mip-budget sibling - `00182A60`/`00182B40`/`001FBD80`/`001FBE20`/`001FBE30`/`001FBE50`/`002D7D90`/`002D7FA0` plus `008C5B30`/`008C5B44`. Interior anchor `0039D0FD` (a `002D7FA0` call).


## SWE2-EC7-113 update (2026-09-21) - `00862690` measured

`00862690` (39 B) is the
varargs spill `003EC8D0`
and `003EC910` run: all
four argument registers home
to the caller's stack, then
`008620B0` runs with `rdx`
pointing at the spilled tail
(`rsp + 0x38`) - the fixed-
prologue shape every
variadic forwarding thunk
in this family shares.
Interior anchor `008626AD`
(the `008620B0` call).

## SWE2-EC7-114 update (2026-09-21) - `008620B0` measured

`008620B0` (16 B) is the
varargs trampoline
`00862690`'s spill forwards
to: `rdx`, `r8` and `r9`
home to the caller's stack
and it returns - the fixed
tail every forwarding thunk
in this family lands on
after homing its registers.
Interior anchor `008620BA`
(the `r9` home store).
