---
system: Save image — buffers, header and persistent payload
category: 19-Save-Load-Settings
status: DOCUMENTED — every register row is closed (owner re-status 2026-09-30, OPUS; SD-40 answered 2026-09-30: nothing reads header dwords 0x12/0x13 back as fields); the payload interior (UQ-271, SUPERSEDED as a duplicate of V-1) is mapped by V-1, ANSWERED 2026-09-27; the two stamps (V-2) and the 0x8000 growth (V-12) answered 2026-09-17; residue SD-40
owner_layer: PrimaryOwner:Save_Load_Settings
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
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-30
audit:
  passes: 1
  last_pass: 2026-09-02
  last_pass_state: four-buffer-claim-survived-gap-is-not-padding
  crossref_clean: false
  reopened_count: 3
origin: opened by U-1, raised in the cross-subsystem accessor hub audit
container_format: save-image
---

# Save image — buffers, header and persistent payload

> Your entire save is **353,936 bytes**, and the game keeps **four copies of it in memory at all
> times**, evenly spaced 353,984 bytes apart.

~~**PARTIAL.**~~ **DOCUMENTED.** *(corrected 2026-10-02, OPUS: the front matter says `status: DOCUMENTED`, every register row closed 2026-09-30)* The buffer layout, sizes, header constants and the payload base are read at tier 1
and are exact. ~~The full header field map and the payload's interior are not.~~ *(Corrected 2026-09-30, SWE2-DATA: the header map is
`V-3`, answered on [the version-stamps page](version-stamps-and-what-loading-normalises.md); the payload interior is
`V-1`, ANSWERED 2026-09-27 (OPUS) in the register — `UQ-271` is SUPERSEDED as its duplicate.)*

## 1. What the player sees

The save slot on the load screen shows you where you were, who was leading the party, and lets
you tell one save from another at a glance. All of that is a small header written just before the
file goes out.

The rest — every flag, every item, every step of story progress — is one large block that the
game keeps live in memory the whole time you play. **Saving is not "gathering up your progress";
your progress already lives in save format continuously.** Saving copies it, stamps a header on
it, and writes it out.

That is why the current area is readable from the save data at any moment, and why a crash loses
only what changed since the last write rather than requiring reconstruction.

## 2. Native mechanism

### Four buffers, identically sized and evenly spaced

```c
undefined * SaveImage_GetActiveRuntimeBuffer(void)    { return &DAT_02164280; }
undefined * SaveImage_GetCaptureStagingBuffer(void)   { return &DAT_021ba940; }
undefined * SaveImage_GetWriteSubmissionBuffer(void)  { return &DAT_02211000; }
// and, from SaveImage_BackupActiveRuntimeBuffer:      &DAT_022676c0
```

| Buffer | Address | Role |
|---|---|---|
| Active runtime | `0x02164280` | the live save state, updated as you play |
| Capture staging | `0x021BA940` | snapshot taken when you save |
| Write submission | `0x02211000` | what is handed to the file write |
| Backup | `0x022676C0` | a copy of the active buffer — **read by nothing; written before a LOAD** (request 6 with a non-zero parameter, which opens the controller in load mode) by `SaveImage_BackupActiveRuntimeBuffer` through the thunk `00584490` from the fullscreen procedure `0027F5D0` (V-6, corrected 2026-09-12 and again 2026-09-13; §7) |

**Every gap is exactly `0x566C0` (353,984 bytes):**

```
0x021BA940 - 0x02164280 = 0x566C0
0x02211000 - 0x021BA940 = 0x566C0
0x022676C0 - 0x02211000 = 0x566C0
```

Four evenly-spaced buffers occupying `4 x 0x566C0 = 0x159B00` = **1,415,936 bytes** of `.data`.

### The image is 353,936 bytes — 48 fewer than the spacing

The size is not inferred from the spacing; it appears as a literal in two independent places:

```c
void SaveImage_ClearActiveRuntimeBuffer(void)
{
    memset(&DAT_02164280, 0, 0x56690);        // 353,936
    _guard_check_icall(0);                     // no-op, see image hardening
    return;
}

void SaveImage_CopyCaptureToWriteSubmissionBuffer(void)
{
    ...
    FUN_0020e540(handle, &DAT_02211000, 0x56690);   // same size   <- corrected 2026-10-02, OPUS: 'handle' is a one-bit selector (a static bit getter), and 0020E540 is a stub (one call, then a jump to an empty ret 0; addresses in save-readiness-apply-fable-1002)
}
```

`0x566C0 - 0x56690 = 0x30` — a **48-byte gap** between the end of one image and the start of the
next. The buffers are spaced with padding rather than packed.

### Header 512 bytes, then the payload

```c
void * SaveImage_GetPersistentPayloadBase(void)
{
    return (void *)(SaveImage_GetActiveRuntimeBuffer() + 0x200);
}
```

**The first `0x200` (512) bytes are header; the persistent payload starts at `+0x200`.**

Combined with the hub finding that opened this document:

```
areaId = max(0, payload[0x1044])            = image[0x1244] = 0x02164280 + 0x1244
```

### Four header constants, at fixed offsets

Each is a 6-byte accessor returning a literal:

| Accessor | Header offset | Value | Reading |
|---|---|---|---|
| `SaveImage_GetHeaderDword58Constant` | `0x58` | `0x20050223` | **reads as the date 2005-02-23**; written and never read back |
| `SaveImage_GetHeaderDword5CConstant` | `0x5C` | `0x00001538` | 5,432 — **the size of the region cleared at buffer `+0x200`** (`002EF2DD`) |
| `SaveImage_GetHeaderDword60Constant` | `0x60` | `0x05071901` | **the battle-state block's magic**, stamped at `002370DF` and compared at `00233C4D` (`V-2`) |
| `SaveImage_GetHeaderDword64Constant` | `0x64` | `0x00007410` | 29,712 — **the battle-state block's size** (`002370CD`) |

`0x20050223` decodes cleanly as `YYYYMMDD` for **23 February 2005** — about a year before FFXII's
March 2006 Japanese release, exactly where a save-format freeze would sit. `0x05071901` admits a
similar reading. **The values are tier-1 fact; the date interpretation is a reading**, flagged in
§7 as **V-2** rather than asserted.

**Two of the four are placed, and `+0x64` dates the format.** Each constant occurs in `.text` only in
its getter and — for three of the four — in one `memset` length or one `cmp`
([version stamps](version-stamps-and-what-loading-normalises.md) §2 and its 2026-09-13 addition).
`+0x5C` and `+0x64` are **sizes**, not dates. Nothing compares `+0x64`, but it still records how big
the battle-state block was when the image was written: the sixteen development saves in
[the katano folder](katano-debug-savedata.md) carry `0x5A70` = 23,152 there against this build's
`0x7410` = 29,712, so **the same `+0x68` / `+0x6C` pair that the validator accepts can sit above two
different block layouts.**

### What the header records at save time

`SaveImage_FinalizeHeaderAndChecksum` writes the slot metadata. The visible assignments:

```c
local_78 = header_byte54;
local_74 = header_dword50;

bVar2 = PartyFocus_GetPreferredDefinitionSelector();      // who is leading
...
bVar3 = PersistentFlag_QueryPrimaryOrAuthoredThresholdGate(0x400b);

uVar5  = WorldTransition_GetActiveOrPendingFieldId();     // current area
puVar7[0x13] = uVar5;                                     // -> header dword 0x13

wVar4  = MapRef_GetPersistenceGroupId(uVar5);             // area -> map group
uVar5  = FUN_00254380(wVar4);
puVar7[0x12] = uVar5;                                     // -> header dword 0x12

*(uchar *)(puVar7 + 0x15) = local_78;
puVar7[0x14] = uVar6;
puVar7[0x0F] = uVar5;                                     // 0xFF unless (local_54 & 1)
puVar7[0x11] = 0;
```

So the header carries the **current area id**, a **map persistence group derived from it**, and a
**party-leader definition selector** — which is what a save slot displays — and, read 2026-09-11
for `V-3`, the rest of what a slot shows: **the roster** (`00583DC2`–`00583EB4`: for party pages
0–8 from `00282DF0(slot)`, skipping an empty page (`+0x60` word negative), one 4-byte entry at
`+0x20 + 4 × n` — character id, level, the two job ids as nibbles, and flags for leader / unit flag
`0x400` / the page flagged bit 1, that last page written after the loop with flag bit 2), and
**the play clock** — `00254CC0` adds each frame's 60 Hz ticks (`0035E790`) to the qword at `+0x10`,
caps it at 9999 h 59 m 59 s, and rewrites `+0x18` hours / `+0x1A` minutes / `+0x1B` seconds from it
(`00254CF8`–`00254DBF`), mirroring the tick total into the image-backed block's `+0x47E8`;
`002536B0` and `00254C90` read the three back. **The gil is header `+0x08`** (`GameState_SetGil`
`00254EE0` / `GameState_GetGil` `00253690`) — the first dword the checksum covers.

It also uses the stack cookie:

```c
local_38 = DAT_01f44830 ^ (ulonglong)auStack_98;
```

`DAT_01F44830` is the same `SecurityCookie` value read independently from the PE load config in
the image-hardening document. Two unrelated derivations agreeing.

## 3. Key addresses

| Address | Name | Verified |
|---|---|---|
| `002EF640` | `SaveImage_GetActiveRuntimeBuffer` | ✅ read |
| `002EF620` | `SaveImage_GetCaptureStagingBuffer` | ✅ read |
| `002EF630` | `SaveImage_GetWriteSubmissionBuffer` | ✅ read |
| `002EF2B0` | `SaveImage_GetPersistentPayloadBase` | ✅ read |
| `002EF5F0` | `SaveImage_ClearActiveRuntimeBuffer` | ✅ read |
| `002EF690` | `SaveImage_CopyCaptureToWriteSubmissionBuffer` | ✅ read (partial — loop elided) |
| `002EF570` | `SaveImage_BackupActiveRuntimeBuffer` | ✅ read (partial — loop elided) |
| `00583D60` | `SaveImage_FinalizeHeaderAndChecksum` | ⚠ read, many blocks elided; the checksum segment `00583F81`–`00583FA1` and the flag byte `00583F5A`–`00583F70` read from the bytes 2026-09-11 (§4) |
| `00255260` | `SaveImage_ValidateRuntimeFormatHeader` | ✅ read from the bytes 2026-09-11 — the predicate is in §8; the 2026-09-01 decompile stays on record as unusable |
| `003BB220` | `CRC32_Compute` | ✅ read — the reflected CRC-32 the finaliser and `0057E310` call (§4) |
| `0057E310` | `SaveWrite_PrepareAndSubmitFullImage` | ✅ read — staging → submission, CRC / 1 / save counter into the submission header, hand-off to `003BB9B0` (§4, §5) |
| `0057E4D0` | `SaveWrite_OperationStateCallback` | ✅ read — the events that reach the submit and that write `02CA99E8` (§5) |
| `00235E80` / `00235E90` / `002EF290` / `002EF2A0` | header constant accessors | ✅ read |
| `02164280` / `021BA940` / `02211000` / `022676C0` | the four buffers | — |
| `01F44830` | security cookie | ✅ cross-confirmed |
| — | `MapRef_GetPersistenceGroupId` | ~~not read~~ read on [the location-map sheet](../../02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/lmap-menumap-location-graph.md) §10.4 (field → the map-reference table's persistence group) *(Corrected 2026-09-30, SWE2-DATA)* |
| — | `PartyFocus_GetPreferredDefinitionSelector` | ~~not read~~ read on [the battle-state block field map](../../11-Party/Battle-State-Block/the-battle-state-block-field-map.md) (the getter of block `+0x5AA4`, the party leader) *(Corrected 2026-09-30, SWE2-DATA)* |
| — | `PersistentFlag_QueryPrimaryOrAuthoredThresholdGate` | ~~not read~~ read for this call in §8c: `0x400B` sets bit 14, the authored threshold schedule, index 11 (`V-5`) *(Corrected 2026-09-30, SWE2-DATA)* |

## 4. Data structures and formulas

```
Save image                       0x56690 bytes (353,936)
  +0x000 .. +0x1FF   header      512 bytes
  +0x200 .. end      persistent payload

Header (V-3, mapped 2026-09-11 from every read writer; 0x200 bytes)
  +0x00   dword   in the finaliser's buffer: ~CRC32 (00583FA1); in the SUBMITTED image: the plain
                  CRC32 of active +0x08..+0xE200 (0057E3BF) — the write path overwrites it
  +0x04   dword   1 in the submitted image (0057E3C7)
  +0x08   dword   the party's gil — GameState_SetGil 00254EE0 writes it (00254F1F), GameState_GetGil
                  00253690 reads it (00253697); the first byte the checksum covers
  +0x0C   dword   walked-distance total, mirrored from the battle block by 00254E80 (00254E90)
  +0x10   qword   play-clock tick accumulator, 60 Hz: 00254CC0 adds the frame's ticks (0035E790) and
                  caps at 0x80BEFBFF = 9999 h 59 m 59 s (00254CF8-00254D3A)
  +0x18   word    play time, hours (mod 10000)   } derived from +0x10 by 00254CC0 (00254D3E-00254DBF);
  +0x1A   byte    play time, minutes             } 002536B0 rebuilds seconds = h*3600 + m*60 + s;
  +0x1B   byte    play time, seconds             } 00254C90 returns the three; the mode-3 stash saves them
  +0x20   4 B x N the slot preview roster, one entry per living party page (N <= 9, written by the   <- corrected 2026-10-02, OPUS: seven entries, +0x20..+0x3B (00583EBE-00583EEB fill 0xFF up to 7; an eighth or ninth page lands on +0x3C, rewritten at 00583F0D; CONTRACT-save-image-buffers.md)
                  finaliser 00583DC2-00583EB4): +0 character id (page +0x60), +1 level (+0xBA),
                  +2 job nibbles (+0x86 << 4 | +0x87), +3 flags: bit 0 = the leader, bit 1 = unit
                  flag 0x400, bit 2 = the page flagged bit 1 (written last)
  +0x3C   dword   [0x0F]  0xFF unless (flags & 1)
  +0x44   dword   [0x11]  written as 0   <- corrected 2026-10-02, OPUS: zeroed, then, when the story-flag test of 0x400B is non-zero, the clan rank byte is stored here and the counter read of 0x11 at +0x40 (getters named in save-readiness-apply-fable-1002) (00583F03-00583F32)
  +0x48   dword   [0x12]  map persistence group, derived from area id
  +0x4C   dword   [0x13]  active or pending field (area) id
  +0x50   dword   [0x14]  the finaliser's value, then in the submitted image the save counter
                  02CA99B4, saturating at 0xFFFFFFFF (0057E3CE-0057E3DD); the slot UI's own
                  counter 00580CD0 writes it too (00580D8E)
  +0x54   byte    [0x15]  the party-leader definition selector
  +0x58   dword           constant 0x20050223
  +0x5C   dword           constant 0x00001538
  +0x60   dword           constant 0x05071901
  +0x64   dword           constant 0x00007410
  +0x68   dword   magic 0x0131F3EA  } the pair SaveImage_ValidateRuntimeFormatHeader tests
  +0x6C   dword   size  0x00004818  } (written by 00253A80 for the image-backed state block)
  +0x57   byte    flags: bit 0 = stash pending (from block +4 bit 12, 00583F63);
                         bit 2 from block +4 bit 14 (00583F70)   <- corrected 2026-10-02, OPUS: bit 1 is set too, from a second static bit getter (00583F74-00583F7D)
  +0x70   qword   } the mode-3 stash (the normalise page section 4): +0x70..+0x7B = the play clock
  +0x78   word    } (+0x10..+0x1B), +0x7C = the walked-distance total, +0x80..+0x90 = the
  +0x7A/B bytes   } world-transition record payload +0x1044..+0x1054
  +0x7C   dword   }
  +0x80   5 dwords}
  +0xC0..+0x1FF   untouched by any enumerated route (320 B)   <- corrected 2026-10-02, OPUS: zero - both clears memset the whole image (002EF5F6-002EF603, 002EF656-002EF663), the boot frame first

Persistent payload
  +0x1044  i32    active or pending field (area) id   (= image +0x1244)
  +0xE000  dword  CRC32 of image[0x0008, 0xE200)     (= image +0xE200, 00583F99)

Buffers in .data, stride 0x566C0 (353,984), 0x30 padding between images
  0x02164280   active runtime
  0x021BA940   capture staging
  0x02211000   write submission
  0x022676C0   backup
```

**Addressing:**

```
payloadBase = activeRuntimeBuffer + 0x200
areaId      = max(0, payload[0x1044])
buffer[n]   = 0x02164280 + n * 0x566C0        for n in 0..3
```

**The checksum (V-4, answered 2026-09-11).** `CRC32_Compute` (`003BB220`) is the reflected CRC-32:
polynomial `0xEDB88320`, initial state `0xFFFFFFFF`, eight shift-and-xor steps per byte, final
complement (`003BB220`–`003BB2BD`; a signed non-positive length returns 0 without reading). The
finaliser feeds it **the active image from `+0x0008` to `+0xE200`** — length `0xE1F8` = 57,848
bytes, `00583F81`–`00583F92`: `SaveImage_GetActiveRuntimeBuffer` again, whatever destination the
finaliser was told to write — and stores the result at **destination `+0xE200`** and its complement
at **destination `+0x0000`** (`00583F99`–`00583FA1`). So the checksum covers neither the first eight
bytes nor the 296,592 bytes after `+0xE200`; those are outside it, not proven unchecked. ASTRA's
[EXP-057](../../_experiments/EXP-057-save-checksum-controls.md) executed the helper (agreeing with
`zlib.crc32` over 256 single bytes and `123456789` → `CBF43926`) and the finaliser segment in
isolation with distinct active and staging fixtures: flips at bytes 0, 7, `E200` and the image end
leave the CRC unchanged, flips at 8 and `E1FF` change it, and a one-byte-short mutant is rejected.
~~`0057E310` recomputes the same interval from the active buffer into a two-dword record — the
load-side comparison, if that is what it is~~ — **corrected the same day: it is the write side.**
`SaveWrite_PrepareAndSubmitFullImage` (`0057E310`, 436 B) copies the capture staging buffer into
the write-submission buffer (`0xACD` × 128 + 16 = `0x56690` bytes, `0057E337`–`0057E3A6`), then
**overwrites the submission's first dword with the CRC of the *active* image `+0x0008`–`+0xE200`**
— the helper's return, not its complement — **and its second dword with 1** (`0057E3A9`–`0057E3C7`),
stores the save counter `02CA99B4` (incremented first unless already `0xFFFFFFFF`, `0057E3C1`–
`0057E3DB`) at submission `+0x50`, formats the slot asset name (`SavePath_FormatSlotAssetName`
`00584610`, ~~index `0x40`~~ buffer size `0x40` and **slot `r9b = 0`** — corrected 2026-09-13: this writer is the field-transition autosave, and it always writes slot 0; [request router §2](../../16-UI/Request-Router/ui-request-router.md) — `0057E3E0`–`0057E3F2`) into the operation record `+0xD0`, points the
record's `+0xF8` at the submission buffer with `+0x100 = 0x56690`, writes the base path prefix
(`003935C0`) and the file name (`sprintf`, `0057E456`), and hands the record to `003BB9B0`
(`0057E490`) — the write-submission call, ~~whose body is unread~~ *(Corrected 2026-09-30, SWE2-DATA: read under `FV-3`, §7 — it refuses while
the storage machine is busy, clamps the count to 5 and queues the `0x38`-byte descriptors)*. It finishes by setting
`02CA99E8 = 1` (`0057E495`) — the global `SaveWrite_GetBusyFlag` (`00583920`) reads. So the submitted image's
`+0x00` is the plain CRC and `+0xE200` the finaliser's copy of the same value, provided the active
interval did not change between the two; the finaliser's complement at `+0x00` survives only in
the buffer the finaliser wrote, not in the file.

**Nothing recomputes or compares it at load (FV-3, controlled negative, 2026-09-11).** Four
measurements, each with a positive hit that shows the method sees what it looks for:
`CRC32_Compute` has exactly two callers in the call graph — the finaliser and the submit path;
the reflected polynomial `0xEDB88320` occurs as an immediate at eight sites, all inside
`CRC32_Compute` (`003BB243`–`003BB2AC`); the only CRC-32 lookup table in the image (`01CC7E70`:
`00000000, 77073096, EE0E612C, …`) is referenced by one function, zlib's `crc32_little`
(`0080E600`, `0080E602`), reached through `crc32_z` (`0080E910`) from twelve hashing helpers
(`0015CC90`, `0017CDF0`–`0017F8C0`) and from nothing in the save code; and the access census
gives the checksum field (payload `+0xE000`) **one writer and no reader**, with every reader of
header `+0x00` a 16-byte block copy (`00229B40`, `003F4AA0`, `0057E310`, `00580CD0`, `00583C00`,
`00583CB0`). The other polynomial constant in the image, `0x04C11DB7` at `01CB5384`, is used by
an Audio function (`007B9F80`). So whatever acceptance a loaded image gets is the `+0x68` pair
validator (§8), the container layer (§8b), or none — not this checksum. The limits: a CRC
computed with a table outside `.rdata`'s 256-entry form, or by code the function list does not
cover (7.1 % of the span), would escape the sweeps. One more writer of the header's first dwords
~~remains unread~~ *(Corrected 2026-09-30, SWE2-DATA: read under `FV-3`, §7 — `+0xD8` is the finaliser's return, the ~~complemented~~ plain CRC)* *(corrected 2026-10-02, OPUS: `00583F97`–`00583FA1` keep `crc` in `eax`; the complement is only the finaliser's own `+0` store, which state 8 overwrites at `00581FA8`–`00581FBA`)*: `SaveSlotTransaction_StateMachine` (`00581DA0`) stores its record's `+0xD8` at
image `+0x00` and `1` at `+0x04` in one of its states (`00581FA8`–`00581FBA`), the same shape as
the submit path.

```
checksum = CRC32(active[0x0008 .. 0xE200))        // 0xE1F8 bytes, reflected, poly EDB88320
dest[0xE200] = checksum
dest[0x0000] = ~checksum
```

**Note on the header index notation:** `puVar7` is a `uint *`, so `puVar7[0x13]` is byte offset
`0x4C`, not `0x13`. The table above gives byte offsets.

## 5. Call chain

```
while playing
  -> game systems read and write the ACTIVE RUNTIME buffer continuously
     (WorldTransition_GetActiveOrPendingFieldId reads payload +0x1044 from it)

player saves   <- corrected 2026-10-02, OPUS: a manual save writes ACTIVE, not STAGING (00581DCA-00581DCF, 00581F27-00581F2F, kind 8 at 00581F51); staging and submission serve the autosave 0057E310 only
  -> capture into STAGING (0x021BA940) — WorldTransitionSnapshot_CaptureRuntimeState (00229B40,
     read 2026-09-11; its direct caller is WorldTransition_StageFieldTransition, 003147BB):
       -> ACTIVE state block +0x4E68C, 0x6000 bytes  -> ACTIVE +0x2200 (the mirror)   00229B76-00229BE2
       -> ACTIVE state block +0x4E68C, 0x8000 bytes  -> STAGING +0x4E68C (whole block) 00229BE4-00229C41
       -> ACTIVE +0x0000, 0xE240 bytes               -> STAGING +0x0000                00229C43-00229CC2
       -> WorldPersistence_ExportGroupPersistentBank -> STAGING +0xE240 / +0x2E450    00229CCA-00229CE6
       -> SpawnKeep_SerializePersistenceBanks        -> STAGING +0xE440 / +0x2E650    00229CEB-00229CF2
       -> 002EF540(STAGING +0x4E660)                                                    00229CF7-00229CFE
     so the header, payload +0x0..+0xE040 and the battle-state block are COPIED from the active
     image, while the group banks and the SpawnKeep images are EXPORTED from the runtime globals;
     "inside the payload, therefore saved" holds only for the copied regions. ~~Whether the save
     menu (0027F5D0 -> SaveTransition_PrepareRuntimeImageForCapture -> an indirect handler through
     0020E5C0) re-captures without a field transition is not resolved (FZ-13).~~
     **RESOLVED 2026-09-16 (SWE2-STRUCT, offline) — the manual save never touches staging.** The
     manual write is storage-queue **op 8**, and `SaveSlotTransaction_StateMachine` (`00581DA0`)
     state 7 is its only enqueue site in the image (`00581F89`; every other EnqueueOperation caller
     pushes ops {1,2,3,4,6,7,9,0xA,0xB,0xC,0xD} — the earlier "register-held op" guess was wrong;
     it was a literal `mov dword [rsp+0x30], 8` at `00581F51`). The record's 0x38-byte element
     carries `+0x28 = SaveImage_GetActiveRuntimeBuffer()` = **`02164280`, the live image** and
     `+0x30 = 0x56690` (`00581F27`-`00581F84`); the write worker `003BAEB0` dereferences exactly
     those fields into the file write `00862620` (`003BB05A`-`003BB062`). State 7 also runs
     `SaveImage_FinalizeHeaderAndChecksum` (`00581EE7`) and `SaveSlotMetadata_BuildSubmissionDescriptor`
     (`00581ED2`) on the same active buffer before enqueueing; state 8 stores the finaliser's dword
     at active `+0x00` and `1` at `+0x04` (`00581FA8`-`00581FBA`) then probes the written file's
     first 8 bytes back into active+0 (op 7, `00581FD9`). So the file carries whatever is live in   <- corrected 2026-10-02, OPUS: op 7 is a write, not a read-back - kind 7 -> 003BB920 (00582149-00582160) arms 02B40E1C = 2 at 003BB98C, the write command; state 8 writes {checksum, 1} into the file
     the active block at write time — no staging refresh is needed, and whether the menu re-captures
     staging is moot for the file's contents. Staging `021BA940` and submission `02211000` belong to
     the autosave path only (`SaveWrite_PrepareAndSubmitFullImage` `0057E310`, slot 0, calls
     `003BB9B0` directly — no queue). Load is symmetric: op 9 fills the active buffer
     (`SaveLoad_ControllerTransitionStateMachine` `0058111E`). AQ-9 prediction: a changed
     active-block byte persists through a manual save/reload — not by re-capture but because the
     file is the live image.
  -> SaveImage_FinalizeHeaderAndChecksum
       -> PartyFocus_GetPreferredDefinitionSelector      (leader)
       -> WorldTransition_GetActiveOrPendingFieldId      (area)
       -> MapRef_GetPersistenceGroupId(area)             (map group)
       -> PersistentFlag_QueryPrimaryOrAuthoredThresholdGate(0x400B)
  -> SaveImage_CopyCaptureToWriteSubmissionBuffer      (one caller: 001C1910)
       -> copy STAGING -> WRITE SUBMISSION, 0x56690 bytes
       -> FUN_0020e540(handle, 0x02211000, 0x56690)      -> to disk   <- corrected 2026-10-02, OPUS: not to disk; 0020E540 is one call then a jump to an empty ret 0, and 'handle' is a static bit getter's one-bit selector (addresses in save-readiness-apply-fable-1002)

  or, from the operation state machine (read 2026-09-11):
  -> SaveWrite_OperationStateCallback (0057E4D0; reached by pointer, no direct caller)
       event 1  -> record fields, then SaveWrite_PrepareAndSubmitFullImage, 00244960, 00247870(rec, 1)
       event 2  -> 003BB430() == 0 and 003BB420() != 0 -> 02CA99E8 = 1, FUN_00583fd0(1, rec) -> rec +0xC0
                   003BB420() == 0                     -> rec +0xC8 = 1, 02CA99E8 = 0, 0036FD80(0), 00245020(rec)
       event 12 with rec[+8] in 0x8100..0x8102          -> SaveWrite_PrepareAndSubmitFullImage, rec +0xC0 = 0
  -> SaveWrite_PrepareAndSubmitFullImage (0057E310)
       -> copy STAGING -> WRITE SUBMISSION, 0x56690 bytes (inline)
       -> submission +0x00 = CRC32(ACTIVE +0x08..+0xE200), +0x04 = 1, +0x50 = save counter 02CA99B4
       -> slot asset name (index 0x40) -> rec +0xD0; rec +0xF8 = submission, +0x100 = 0x56690   <- corrected 2026-10-02, OPUS: 0x40 is the name buffer's size and the slot is r9b = 0 (the autosave note in section 4)
       -> FUN_003bb9b0(rec, path, 1)                     -> the write submission (read under FV-3, §7)
       -> 02CA99E8 = 1                                    (SaveWrite_GetBusyFlag's global)

separately
  -> SaveImage_BackupActiveRuntimeBuffer : ACTIVE -> BACKUP (0x022676C0)
  -> SaveImage_ClearActiveRuntimeBuffer  : memset ACTIVE, 0x56690
```

**Upstream:** the save UI, and every system that mutates progress.
**Downstream:** the platform file write.

**Do not confuse with:** settings/config storage. This category owns both; this document covers
only the save image.

## 6. Modding notes

- **A save is 353,936 bytes (`0x56690`)** with a **512-byte header**. Payload offsets in an
  external editor need `+0x200` against the file start.
- **The area id is at file offset `0x1244`** (`payload +0x1044`). Editing it relocates the load.
- **Four in-memory copies exist.** `0x02164280` is the live one — that is the address to watch in
  a debugger or cheat table. The other three are staging, submission and backup.
- **The buffers are 48 bytes apart beyond the image size**, so a runaway write past one image
  lands in the gap rather than immediately in the next buffer — **but that gap is not padding after
  the fourth buffer** (corrected 2026-09-02, §8c). A live 7-entry record array begins 16 bytes into
  the final gap, so overrunning the backup buffer corrupts unrelated state.
- **`0x20050223` at header `+0x58` is a stable format stamp.** A tool checking save validity can
  use it, but see V-2 — its meaning is a reading, not proven.
- **Header dwords `0x12` and `0x13` are area/map metadata** (the finaliser writes the current field id to `0x13` and
  its map persistence group to `0x12`, §2), so a save edited to a new area should update both. ~~or the slot display
  and the load may disagree~~ *(Corrected 2026-09-30, SWE2-DATA: who reads the two dwords back is not verified; registered as `SD-40`)*. *(`SD-40` answered 2026-09-30, OPUS, [record](../../_index/candidates/sd40-42-header-readers-0930/README.md): nothing reads them back as fields; outside the writer only whole-block copies touch them, and the save menu's own header reads are other offsets. So editing them alone changes nothing a reader was found for; the load follows payload `+0x1044`, the bullet above. The record's limits are 30 escapes, 18 indirect calls and file buffers before the image copy.)*
- **XIIOnline:** the entire progress state is one 353,936-byte block at a fixed address with ASLR
  off, which makes it directly readable. But it is **per-client local state**: two clients each
  keep their own active buffer, and nothing here reconciles them. Shared progress needs an
  authority above this layer, not a copy of this buffer.

## 7. What is not known

- [x] **UQ-271.** *(SUPERSEDED in the register 2026-09-26, FABLE, Claude Opus 5.5: a duplicate; the open residue is carried by **V-1**)* The payload interior — what lives around `+0x1044` and everywhere else in 353,424 bytes.
      **V-1, the big one.**
- [x] ~~Whether `0x20050223` / `0x05071901` are dates, versions or magics. **V-2.**~~
      ***ANSWERED 2026-09-17 (FABLE): both are format stamps, and only one is ever checked.** `0x05071901` is the battle-state block's stamp: `002370C0` zeroes `0x7410` bytes at `[02EBF190]` and writes it as the block's first dword (`002370DF`), `00233C10` validates a loaded image's block by comparing that dword with the constant (`00233C4D`) and rebuilds the block when it differs, and `SaveImage_GetHeaderDword60Constant` (`00235E90`) returns the same value for the header's `+0x60`. `0x20050223` is the header stamp: `SaveRuntime_InitializeHeaderAndImageBackedState` (`00253A80`) takes it from the getter `002EF2A0` and stores it at the active image's `+0x58` (`00253AB8`), and no instruction in the image compares it, the getter's `mov` being the constant's only occurrence. Read as BCD they are 2005-02-23 and 2005-07-19 revision 1, which is a reading of the digits, not a claim the code makes; what the code makes of them is one validated block magic and one write-only header stamp. Static, immediate census over every function.*
- [x] ~~The full header map; only offsets `0x3C`–`0x64` are partially accounted for.~~ **V-3** —
      ANSWERED 2026-09-11 (§4): every offset a reached writer touches is named — CRC, gil, walked
      total, play clock, roster, slot metadata, save counter, leader, flags, constants, the
      image-backed block's stamp and the mode-3 stash; `+0xC0`–`+0x1FF` is untouched.
- [x] ~~The checksum algorithm — the function is named for it but the computation is elided in the
      decompilation.~~ **V-4** — ANSWERED 2026-09-11 (§4): reflected CRC-32 over the active image
      `+0x0008`–`+0xE200`, stored at `+0xE200` and complemented at `+0x0000`; EXP-057.
- [x] ~~What `0057E310` does with the CRC it recomputes~~ (the write-submission path, §4 / §5);
      ~~where a loaded image's `+0x00` / `+0xE200` is compared~~ (nowhere in the executable, §4 —
      four controls). Left: which of the two submission routes (`002EF690` from `001C1910`;
      `0057E310` from the operation callback) a given save takes, what `003BB9B0` does with the
      record, and what `SaveSlotTransaction_StateMachine` stores at `+0x00` from its `+0xD8`.
      **FV-3**, narrowed twice 2026-09-11.
      ***CLOSED 2026-09-17 (FABLE), the three leftovers read.** *The route:* `0057E310` is the autosave path, slot 0, which submits directly (§5 above); `002EF690` is reached only from the `SaveloadManager` method `001C1910` (`001C1929`), which copies the capture into the submission buffer when the manager's byte `+0x10` is clear and its flag `+0xA70` is set, and then clears that flag (`001C1919`..`001C192E`): ~~the manual save's deferred hand-off~~ a copy that reaches no file, because its tail is a compiled-out stub *(corrected 2026-10-02, OPUS: checked at `002EF72C` and `0020E540`–`0020E576` — `0020E540` is one call then a jump to an empty `ret 0` (both addresses in save-readiness-apply-fable-1002); the manual save writes the active buffer, §5)*, driven from `0017D6E0`. *`003BB9B0(_, records, count)`:* refuses with 0 while the storage machine is busy (`[02B40E10]` non-zero, `003BB9B4`), clamps the count to 5, copies that many `0x38`-byte descriptors from `records` into `02B40EC8` (`003BB9F0`..`003BBA21`), sets `02B40FE0` = count, `02B40E1C` = 2, `02B40E10` = 1 (busy), `02B40EC0`, `02B40E18` and `02B40FE4` = 0 (`003BBA25`..`003BBA48`), runs the storage handler `003BAEB0` and returns 1: it queues up to five descriptors into the storage machine's block and starts it. *The `+0x00` store:* `SaveSlotTransaction_StateMachine` caches the finaliser's return in `+0xD8` (`00581EF8`, right after `SaveImage_FinalizeHeaderAndChecksum`) and state 8 writes it to active `+0x00` with 1 at `+0x04` (`00581FA8`..`00581FBA`); by V-4 that dword is the ~~complemented~~ plain CRC-32 *(corrected 2026-10-02, OPUS: the finaliser stores `~crc` at dest `+0` but returns `crc` in `eax`, `00583F97`–`00583FA1`; `00808C40` preserves `eax` and `00581EF8` caches it; katano-debug-savedata.md, the `+0x00` row)* of `+0x0008`..`+0xE200`, so `+0xD8` is the header's checksum word held across the file operation. Static, bodies read.*
- [x] ~~What `PersistentFlag_QueryPrimaryOrAuthoredThresholdGate(0x400B)` gates.~~ **V-5 CLOSED
      in section 8c** - bit 14 set selects the authored threshold schedule; index 11.
- [x] ~~Why a fourth backup buffer exists and who reads it.~~ **V-6** — ANSWERED 2026-09-11 as a
      controlled negative: ~~**nothing reads it and nothing reaches its writer.**~~ *(the second half is refuted — see the
      corrections below; struck 2026-09-13 after AUDITSPEC-ABS63-2EF570-ROUTE)* `022676C0` is
      referenced by exactly one instruction in the image — the `lea` that makes it the destination
      of `SaveImage_BackupActiveRuntimeBuffer` (`002EF570`, `0x56690` bytes from the active buffer,
      `002EF570`–`002EF5E9`) — and that function has ~~**no caller in the call graph and no
      reference to its address anywhere**~~ (no `lea` / `mov` of `002EF570`, no 4- or 8-byte data
      occurrence — but the thunk `00584490` encodes it in a `jmp`); no getter returns the buffer, no data pointer holds it, and the stride
      immediates a computed `buffer[3]` would need (`0x566C0`, `0xACD80`, `0x103440`) occur
      nowhere. **Controls:** the same sweeps find the other three buffers' getters and copy sites
      (`02164280`: `002EF640`, `002EF5F6`, `002EF57C`; `021BA940`: `002EF620`, `002EF6A4`;
      `02211000`: `002EF630`, `002EF69D`, `002EF71E`). Limits: a function-pointer table built at
      run time from arithmetic, or code in the function list's 7.1 % gap, would escape the
      sweeps. ~~In the shipped build the fourth buffer is dead space: 353,936 bytes allocated for a
      backup path the PC port no longer enters.~~
      **CORRECTED 2026-09-12 (FABLE):** the writer **is** called. A function-list-independent index of every `E8` / `E9` rel32 in `.text` finds the 5-byte thunk `00584490` (`jmp 002EF570`) and its one call at `0027F974`, inside the save controller's state handler `0027F5D0` (a callback with no static caller of its own; 21-state jump table at `0027F8C6`): on the arm where the controller id `[ctx+0xD4]` is non-zero (`0027F8DB` / `0027F8ED`) the active runtime buffer is backed up and then `SaveLoad_OpenController(ctx+0xD4, 1)` opens the controller ~~in save mode~~ (`0027F984`). The "read by nothing" half stands (the rip sweep of `022676C0` is instrument-independent); the "no caller" half was a caller-graph negative that never asked about thunks. So the backup is taken ~~**before every save write**~~ and never read back in the shipped build — dead storage still, but written on a live path. **V-6.**
      **CORRECTED AGAIN 2026-09-13 (FABLE, AUDITSPEC-ABS63-2EF570-ROUTE): the mode was misread.** A non-zero parameter
      `[ctx+0xD4]` opens the controller in **load** mode. `SaveLoad_OpenController` stores `parameter != 0` (`00583950`–`00583955`),
      which becomes the controller's `+0xC1` and the slot selector's `+0xEA`. The selector starts its list at slot 1 only when
      `+0xEA` is 0 (`0057FF56`–`0057FF66`), since slot 0 is the autosave and cannot be saved to. The title text is `0xC82`
      when `+0xEA` is 0 and `0xC84` / `0xC86` otherwise (`0058030F`–`00580330`). The save crystal's script passes 0
      (`openfullscreenmenu(0x8005, 0)`), which takes the capture arm (`0027F8F6`–`0027F972`: `005844A0`, then
      `0020E5C0`, a no-op). **So the backup is written before a load, not before a save.** The route
      ([request router](../../16-UI/Request-Router/ui-request-router.md), request 6) is: `0027F540` builds the `0xF0`-byte
      fullscreen widget with procedure `0027F5D0` through the widget factory `00244F50`. Its table arm `0027F8DB` branches on
      `jne 0027F974` (`0027F8E2` / `0027F8F4`) to `call 00584490` → `jmp 002EF570`. It is reachable whenever a load is
      opened through request 6 with a non-zero parameter. Whether that path runs in an ordinary session is a runtime
      property. It does not change the static route, and a completed load would be the observation.
- [x] ~~What the `iVar14 < 9` and `lVar15 < 7` loops in the finalizer iterate. **V-7.**~~ **V-7
      ANSWERED 2026-09-12 (FABLE), mostly by the V-3 reading above:** the `< 9` loop is the roster
      walk over party pages 0–8 (`00583DC2`–`00583E3A`, `00282DF0(slot)`, the empty page skipped, the
      page with byte `+0` bit 1 deferred and appended after the loop with flag bit 2); the `< 7` loop is
      **the padding** — entries from the count written up to the seventh are filled with `0xFF` in
      their first byte (`00583EBE`–`00583EEB`), so the header's roster is a fixed seven-entry field
      `+0x20`–`+0x3B` and `N ≤ 9` above is the walk's bound, not the field's: at most seven entries
      are ever stored (the eighth and ninth living pages would overrun `+0x3C`, which the finaliser
      writes next — a shipped roster never has more than seven living pages).
- [x] ~~Whether the on-disk file is the write-submission buffer verbatim.~~ **V-8 ANSWERED in
      section 8b** — no: a `SAFH` container with a declared uncompressed size and a high-entropy body.
- [x] ~~Whether the `SAFH` body is a non-zlib codec, encrypted, or compressed-then-encrypted.~~
      **V-9 ANSWERED 2026-09-13 (FABLE):** zlib level 9, then RC4-128 with an MD5-derived key (§8b, *The body decoded*),
      verified by decoding nine shipped saves.
- [x] ~~What the u32 at `SAFH +0x08` is (varies 0–26 across saves).~~ **V-10 ANSWERED 2026-09-13 (FABLE):** the rotation
      of the 32-character passphrase before hashing, `abs(rand()) mod 32` per save (`008663C5`–`008663ED`).
- [x] ~~Why the image grew by exactly `0x8000` between the 2018 and current builds. **V-12.**~~
      ***ANSWERED 2026-09-17 (FABLE): the growth is the battle-state block, appended at the old image's end.** The block pointer `02EBF190` is set to `active image + 0x4E68C` (`00233C25`..`00233C33`), four bytes before the old image's length `0x4E690`, and `002370C0` initialises `0x7410` bytes there under the stamp `0x05071901`: the forty `0x1C8`-byte [stats records](../../04-Actor-Entity/Battle-Record-Kind/battle-record-kind-byte.md) from `+8`, the fields at `+0x5B12` and `+0x5B42` the import compares, and the rest of the block. `0x4E68C + 0x8004 = 0x56690`, the current image size, so the image grew by one `0x8000` reserve overlapping the old final dword. Older images carry that state inside the payload instead, at whole-image `[0x2200, 0x8200)`, and the loader's prelude `00235AF0` compares the block's `+0`, `+4`, `+0x5B42` and `+0x5B12` with that region's and, on any difference, has `002EF4A0` copy the region's `0x6000` bytes into the block's head and rebuilds the records; [the spawn page](../../05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md)'s §27 reads that import in full. The `0xBF4` bytes between the initialised `0x7410` and the reserve's end are written by nothing read here. Static, bodies read.*

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| Four buffer addresses | complete bodies of three accessors + the destination in `SaveImage_BackupActiveRuntimeBuffer` | 1 |
| Stride is `0x566C0`, uniform across all three gaps | arithmetic on the four literal addresses | 1 |
| Image size is `0x56690` | `memset(..., 0x56690)` and the copy length, two independent sites | 1 |
| Header is `0x200` bytes | `SaveImage_GetPersistentPayloadBase` returns `active + 0x200` | 1 |
| Area id at payload `+0x1044` | complete body of `WorldTransition_GetActiveOrPendingFieldId` | 1 |
| Four header constants and their values | complete bodies of four 6-byte accessors | 1 |
| Header records area, map group and leader | assignments in `SaveImage_FinalizeHeaderAndChecksum` | 1 |
| `DAT_01F44830` is the security cookie | matches `SecurityCookie` from the PE load config, derived independently | 1 |
| The backup buffer has no reader; its writer **is** called, through a thunk, on the **load**-mode arm (V-6, **CORRECTED 2026-09-12**: raw `E8`/`E9` index — thunk `00584490` called at `0027F974` in `0027F5D0`; mode corrected 2026-09-13: `0057FF56`–`0057FF66`) | rip-relative sweep of `022676C0` (one hit, the writer's `lea`); call graph and address / data sweeps of `002EF570` (zero); stride-immediate sweep (zero); the three live buffers as positive controls | 1 (controlled negative) |
| The header map (§4): gil at `+0x08`, the play clock at `+0x10`–`+0x1B`, the roster at `+0x20`, the rest | `00254EE0` / `00253690`, `00254CC0`, `002536B0`, `00254C90`, `00583DC2`–`00583EB4` read; the payload map's header census for the writer set | 1 | PROVEN |
| The checksum recurrence, interval and two stores | `003BB220`–`003BB2BD` read; `00583F81`–`00583FA1` read; EXP-057 (helper + finaliser segment in isolation, distinct active / staging fixtures, boundary flips, one-byte-short mutant rejected) | 1 + isolated original code |
| The validator's predicate and its argument | `00255260`–`0025528C` read; call sites `00280372` / `003941DC` pass image `+0x68`; EXP-058 (ten cases, no stubs, any-size mutant rejected) | 1 + isolated original code |

### A decompilation I refused to use

`SaveImage_ValidateRuntimeFormatHeader` (`00255260`, 45 bytes) decompiles to:

```c
bool SaveImage_ValidateRuntimeFormatHeader(int *param_1)
{
    if ((param_1 != (int *)0x0) && ((*param_1 != 0 || (param_1[1] != 0)))) {
    }
    return true;
}
```

Read literally this says "the validator always returns true", which would be a striking claim —
that FFXII does not validate save headers at all.

**It is an artifact.** The `if` body is empty because Ghidra dropped it, exactly as in the Phyre
reflection family. A 45-byte function with a two-clause guard does not have an empty consequent.
The honest reading is that the function tests a non-null pointer and a non-zero first 8 bytes,
and the outcome of that test is not visible in this decompilation.

Recorded as **unusable** in §3 rather than summarised. The tempting claim here was a headline;
the empty-block rule already on file is what stopped it, and the same rule marks
`SaveImage_FinalizeHeaderAndChecksum` as partially elided.

**Resolved from the bytes 2026-09-11.** The 45 bytes are a predicate over two dwords:

```
if (p == NULL)                       return true;    // 00255260-00255263, 00255287
if (p[0] == 0 && p[1] == 0)          return true;    // 00255265-0025526E
if (p[0] != 0x0131F3EA)              return false;   // 00255270-00255279
return p[1] == 0x00004818;                           // 0025527A-00255286
```

A non-zero first dword that is not the magic rejects after one read; the second dword is read
only for a zero first dword or the magic. Nothing is written and nothing is called. Both callers
pass **image `+0x68`** — the magic / size pair `00253A80` writes for the image-backed state block
(`00280372`, `003941DC`) — so this validates that block's stamp, not the header constants of §2
and not the checksum. ASTRA's [EXP-058](../../_experiments/EXP-058-save-validator-controls.md)
executed the body over ten pairs (null, zero / zero, the pair, and seven rejections including
`4817` / `4819` and `20050223` / `1538`) with exact read tracking and no stubs; a mutant that
accepts any size is rejected. ~~What a caller does with `false` is not read.~~ *(Corrected 2026-09-30, SWE2-DATA, callers read: on `false`
both call sites (the area controller and the title-side body) call the save-image reset — the init that clears the
payload and applies the authored flag lists — so a failed stamp starts from a fresh image; the title-side body is orphaned per
[the battle-runtime-mode contract](../../00-Engine-Core-Runtime/Battle-Runtime-Mode/CONTRACT-battle-runtime-mode.md).)*

### Numbers stated only where they are literals

`0x56690` and `0x566C0` are different numbers and both matter. The size comes from two literal
call arguments; the stride comes from address arithmetic. The 48-byte difference is stated as
what it is — a gap between images — and not explained, because nothing read so far says what
occupies it.

## 8b. Reopened 2026-09-02 — the on-disk format, and an exact cross-check

**V-8 is answered: the file on disk is not the write-submission buffer verbatim.**

Nine retail save files were read from
`Documents\My Games\FINAL FANTASY XII THE ZODIAC AGE\<steamid>\FFXII_00N`.

### The container

```
FFXII_000  first 32 bytes:
53 41 46 48  90 66 05 00  00 00 00 00  e8 d3 57 46  e0 f9 0a a1 ...
"SAFH"       0x00056690   0x00000000   high-entropy body
```

| Offset | Size | Content |
|---|---|---|
| `+0x00` | 4 | magic `"SAFH"` — Save File Header |
| `+0x04` | u32 | **uncompressed image size** |
| `+0x08` | u32 | ~~small value, varies 0-26 across saves~~ **key rotation 0–31** (`abs(rand()) mod 32` at write; must be ≤ 31 at read) — `V-10` |
| `+0x0C` | - | body, entropy 7.93-7.98 bits/byte |

### The cross-check that matters

`+0x04` reads **`0x00056690` = 353,936** - **exactly the size derived in section 2 from the
`memset` literal in `SaveImage_ClearActiveRuntimeBuffer`.**

Two completely independent routes agree to the byte: a decompiled instruction operand, and a file
written by the retail game on this machine. That is the strongest confirmation available for the
image size, and it was not available when section 2 was written.

### The image grew by exactly 32 KB between builds

The five saves dated February 2018 declare a different size:

| Saves | Declared size | |
|---|---:|---|
| 2025 (`FFXII_000`-`003`) | 353,936 | `0x56690` - matches the current EXE |
| 2018 (`FFXII_004`-`008`) | 321,168 | `0x4E690` |

```
353,936 - 321,168 = 32,768 = 0x8000 exactly
```

**The save image grew by precisely 32 KB in a patch.** So `0x56690` is not a property of "FFXII" -
it is a property of *this build*. Any tool must read the declared size from `+0x04` rather than
assume a constant, and the database's figure is scoped to the authorized EXE.

### The body is not plain zlib - and what that does and does not prove

- Every offset in the file was tested for a DEFLATE stream, raw (`wbits=-15`) and zlib-wrapped
  (`wbits=15`): **0 hits across 5,253 offsets**.
- No zlib magic byte (`0x78 01/5E/9C/DA`) anywhere.
- Entropy 7.93-7.98 bits/byte, essentially maximal.
- No repeated 16-byte blocks - no ECB electronic-codebook tell.

Compression ratios are 38:1 to 118:1, unremarkable for a mostly-zero 354 KB buffer, so **something
is compressing.** But the binary links zlib 1.2.11 and no plain zlib stream is present, so the body
is either compressed with a non-zlib codec, encrypted, or compressed and then encrypted.

**Maximal entropy cannot distinguish compressed from encrypted** - compressed data also looks
random. The claim proven here is the negative one: *not a plain DEFLATE stream*. Which of the three
it actually is stays open as **V-9**. *(Answered in the next section, 2026-09-13.)*

### The body decoded — compressed, then encrypted (2026-09-13, FABLE; answers `V-9` and `V-10`)

*Read from the image and checked by decoding shipped save files offline; the file opener, its decoder and the writer were
located by ASTRA's [spawn page §25](../../05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md).*

**Reading** — `008666B0` (mode 1): after the `SAFH` magic, `+0x08` must be ≤ 31 (`00866805`) and is kept in `02EB3868`;
`+0x04` must be ≤ `0x100000` (`00866817`); the body from `+0x0C` goes to `00865D90`, which runs two stages and requires the
result's length to equal `+0x04` (`00866866`–`0086686D`):

1. **RC4 decryption through Windows CryptoAPI** (`00865840`): `CryptAcquireContextW` with container `RSA_SQEX_FFXII_TZA`
   and provider *Microsoft Enhanced Cryptographic Provider v1.0*, type 1 (retried with `CRYPT_NEWKEYSET`,
   `008658AF`–`008658D6`); `CryptCreateHash(CALG_MD5 = 0x8003)`; the 32-byte ASCII constant at `01CCFCF8` —
   `FINAL FANTASY XII THE ZODIAC AGE` — **rotated left by `+0x08` characters** (`strncpy` and two `memcpy`s,
   `0086592C`–`0086595C`), **with its 32nd byte then overwritten by NUL** (`00865961`), so only **31 characters** are
   hashed (`CryptHashData`, `00865985`); `CryptDeriveKey(CALG_RC4 = 0x6801, flags 0x00800000 — a 128-bit key)`
   (`008659AF`); and `CryptDecrypt` over the body in 1,000-byte chunks, the last one marked final (`008659C2`–`00865A31`).
2. **zlib `uncompress`** (`0080C5A0`, zlib 1.2.11).

**Writing** — `00866200` (mode 0) builds `{ "SAFH", u32 length, u32 r }` with **`r = abs(rand()) mod 32`**
(`008663C5`–`008663ED`), compresses the image with `compress2` at **level 9** (`0087AF40`, `deflateInit_` with version
`1.2.11`, `00866464`–`0086646C`) and encrypts the result with the twin `00865AE0` (the same key derivation, `CryptEncrypt`).

**So `V-9`: compressed with zlib, then encrypted with RC4-128; and `V-10`: `+0x08` is the passphrase rotation, a fresh
random 0–31 per save.** The entropy test above could not tell, and the zero-DEFLATE-hit result is explained: the zlib
stream exists only after decryption.

**Checked on real files (offline decode, not the game):** `tools/safh_decode.py` (FABLE scratch) applies exactly that
recipe to nine shipped saves from ASTRA's `EXP015` backup: all nine decrypt to a zlib stream with header `78 DA` (level 9),
all inflate to exactly their declared `+0x04` length, and every decoded image carries the stamp `0x05071901` at `+0x60`.
Control: hashing all 32 characters instead makes the first file fail (`incorrect header check`), so the 31-byte quirk is
real. Rotations seen: 0, 1, 2, 7, 14, 15, 23, 25, 26.

**And two image sizes ship in one save folder:** four of the nine declare **`0x56690`** and five declare **`0x4E690`** —
exactly `0x8000` smaller, the older build's size ([§8b above](#the-image-grew-by-exactly-32-kb-between-builds) and `V-12`).
The reader copies with a fixed request of `0x56690` (`SaveLoad_ControllerTransitionStateMachine`, packet 9, `0058111E`), so, by
the read sequence ASTRA's §25 traces, loading an older-size save would take the short-read path the [request router §2](../../16-UI/Request-Router/ui-request-router.md)
describes: `0x4E690` bytes copied, result 0 reported, and the load continuing as a success. ~~What the last `0x8000` bytes hold
after such a load, and whether a later step migrates them, is not established here (`V-12`).~~ *(Corrected 2026-09-30, SWE2-DATA: `V-12` is
ANSWERED 2026-09-17, §7 — the loader's prelude `00235AF0` compares the battle-state block with buffer `+0x2200` and, on any
difference, copies the older image's `0x6000` bytes from there back into the block.)*

> **A same-process older-save load has now been observed end to end — and it does not answer the question above.**
> 2026-09-21, ASTRA's `old-save-start-p` run (`FABLE-REQ-ASTRA-OLD-SAVE-LOAD`), consumed by FABLE. Modern field →
> returned title → old load-complete → settled old field, in one process, eight accepted samples:
>
> | stage | first six levels | prefix `[0,0x5B10)` equals the saved old file | bank 0 records matching the old save |
> |---|---|---|---|
> | modern field | `1,1,1,1,2,1` | no | 22/40 |
> | returned title | `1,1,1,1,2,1` | no | 34/40 |
> | old load complete | `21,21,21,21,21,21` | **yes** | 40/40 |
> | settled old field | `21,…` | yes | 40/40 |
>
> **So the older file's compatibility records replace the modern battle prefix and bank 0** — `H1` — and the
> reading in which prior modern state simply survives and is used instead, `H2`, is **refuted for this file**.
> *The partial bank matches at the first two stages are the trap*: common and default records agree across saves,
> so 22/40 and 34/40 are not partial imports; the discriminator is the full prefix plus the differing party
> records. The title transition also changed state — 220 battle bytes differ between modern field and returned
> title — so a field-to-old difference cannot be charged wholly to the old loader (`H3`), **but the title
> transition did not itself produce the older party records**: those appear only at load-complete, where 1,572
> bytes differ, and the two old-stage blocks are byte-identical.
>
> ***What this does NOT establish, including the question this section asks.*** It says nothing about the last
> `0x8000` bytes of an older-size image or whether anything migrates them — `V-12` stands exactly as written above.
> *(2026-09-30, SWE2-DATA: `V-12` is answered statically in §7; this observation neither adds to nor contradicts it.)*
> It does not identify the writer instruction, does not generalise to other files or builds, and does not reach
> enemy death, respawn consequences or native callback ordering. **And the keep banks are recorded but not
> explained:** keep 1 holds 328 nonzero bytes at modern field and zero at returned title; keep 2 holds 346 at
> returned title, is byte-identical at load-complete, and is zero at settled old field — *and modern keep 1 is
> **not** byte-identical to returned-title keep 2*, so this is not a proven bank copy, swap or wipe, and not an
> uninterrupted lifetime. Only the sampled values and the stage-bounded changes are established. ~~*Narrowed the same day:* the decoded 2018 images end exactly where the current battle-state block would begin — the block sits at buffer `+0x4E68C` (payload `+0x4E48C`), 4 bytes before the old image's end — and **they carry no copy of it anywhere**: across the five, the block's magic `0x05071901` occurs only at header `+0x60` and in the `0x80`-byte transition mirror at buffer `+0x2200`, the mirror's leading 16 bytes occur nowhere else, and nothing past `0x4E000` is non-zero except 6 bytes; the four current images hold the block (magic at `+0x4E68C`, about 7,500 non-zero bytes in `0x4E000`–`0x56000`). Nothing in the current load path converts one layout to the other: `00584210` moves only the Trial Mode stash fields, `00233C10` checks only the stamp at `+0x4E68C`, and the reader requests `0x56690`. So a 2018 save loaded by this build would supply the first `0x4E690` bytes and leave the battle-state block as the session had it. Where the 2018 build kept that state is a property of that build, which this database does not have.~~ **Corrected 2026-09-13 (FABLE, on `ASTRA-CONTRA-FABLE-OLD-SAVE-CONVERSION` and `ASTRA-REQ-FABLE-MIRROR-COPY-EXTENT`, re-read):** the older images **do** carry the battle-state state — **at buffer `+0x2200`**, the region the payload map had called a `0x80`-byte mirror. Both capture paths copy **`0xC0 × 0x80 = 0x6000` bytes** from the block (`+0x4E68C`) to `+0x2200` (`SaveTransition_PrepareRuntimeImageForCapture` `00584515`–`00584572`, `WorldTransitionSnapshot_CaptureRuntimeState` `00229B81`–`00229BE2`), and in the decoded images that region is a full block: in `FFXII_004` (2018) the party records at `+0x2200 + 8 + k × 0x1C8` hold level 21 and HP 742, 674, 668…, where the current `FFXII_000` holds level 1 in both copies. And the load path **converts**: the battle-state guard `00233C10` first calls `00235AF0` (`00233C14`), which compares the block with `buffer + 0x2200` at `+0`, `+4`, `+0x5B42` and `+0x5B12` (`00235B19`–`00235B48`) and, on any difference, has `002EF4A0` copy those `0x6000` bytes back into the block (`02166480` → `021B290C`) and rebuilds the forty gambit-bank groups at `+0x5B10` — ASTRA's [spawn page §27](../../05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md) — before the stamp test. So an older save's block is imported from `+0x2200`, not left as the session had it; my search had looked for the region's first 16 bytes *elsewhere* and not recognised the region itself. What the rebuild supplies for the rest of the block and whether the result plays correctly are initialized-state questions. *Observed 2026-09-13 ([EXP-080](../../_experiments/EXP-080-older-save-live-load.md), re-derived from the raw spans): after an ordinary load of the 2018-size save `004` the live block's first `0x5B10` bytes equal its `+0x2200` copy and bank 0 of all forty members equals the copied records' `+0x88` — members 8–39 included, which only the conversion loop writes; the fresh-title control matches 0 of 40 ([battle-state block §2.9](../../11-Party/Battle-State-Block/the-battle-state-block-field-map.md)).*

**Practical consequence** *(written before the decode; kept for history):* external save editing is **not** straightforward. A tool cannot seek to
file offset `0x1244` for the area id - that offset is valid inside the *decoded* image, not inside
the file.

## 8c. Reopened 2026-09-02 - payload interior, first mapped region

The Story category's persistent flag banks were read, and every one of them addresses **this
payload**. That maps the first real region of the interior and closes **V-5**.

| Payload offset | Size | Content |
|---|---:|---|
| `+0x1044` | 4 | active or pending field (area) id |
| `+0x1384` | 8 | persistent flag `Bank64A` |
| `+0x13B4` | 256 | persistent flag `Bank2048` |
| `+0x14B4` | 64 | persistent flag `Bank512` (Low + High) |
| `+0x14F4` | 64 | persistent flag `Primary` |

The flag region is **exactly contiguous** - `0x13B4 + 256 = 0x14B4` and `0x14B4 + 64 = 0x14F4` -
which independently corroborates both the offsets and the capacities their names imply.

**V-5 closed.** `PersistentFlag_QueryPrimaryOrAuthoredThresholdGate(0x400B)` in
`SaveImage_FinalizeHeaderAndChecksum` is not a flag read: bit 14 of the encoded id selects the
**authored threshold schedule**, and the low 14 bits give index **11**.

**V-1 advanced, not closed.** 336 bytes of the interior are now identified out of 353,424. The
overwhelming majority is still unmapped. *(Dated 2026-09-02. `V-1` is ANSWERED 2026-09-27 (OPUS): the type store tiles
all 353,424 payload bytes and the unknown bytes are reached by no entry route — the register row.)*

## 8d. Reopened 2026-09-02 - the payload map, systematically

Rather than hunting one field at a time, **all 70 callers of `SaveImage_GetPersistentPayloadBase`
were decompiled** (11,093 bytes total) and every offset applied to the returned base was extracted.
That yields the first real map of the payload interior.

### The world-transition record - a named 36-byte structure at `+0x1040`

| Offset | Size | Field | Named accessors |
|---|---|---|---|
| `+0x1044` | i32 | active or pending field id | `Get`/`SetActiveOrPendingFieldId` |
| `+0x1048` | i32 | destination parameter | `Get`/`SetDestinationParameter` |
| `+0x104C` | i32 | previous field id | `GetPreviousFieldId` |
| `+0x1050` | i32 | previous destination parameter | `GetPreviousDestinationParameter` |
| `+0x1054` | i32 | options | `Get`/`SetOptions` |
| `+0x1058` | ? | *unnamed* | only `StageFieldTransition` |
| `+0x105C` | i32 | transition field id | `GetTransitionFieldId` |
| `+0x1060` | u8 | field runtime parameter | `WorldField_InitializeCurrentFieldRuntimeParameters` |
| `+0x1061` | u8 | initialization state | `WorldPersistence_ResetBanksAndMarkInitializationState` |
| `+0x1062` | u8 | flags | `WorldTransition_ClearFlag1062_Bit04`, + 19 consumers |
| `+0x1063` | u8 | *unnamed* | `ActorManager_RunFieldRuntimePass`, 10 consumers |

**`WorldTransition_ResetState` writes `+0x1044`, `+0x1048`, `+0x104C`, `+0x1050` and `+0x1054`
together**, which is direct evidence that those five are one logical record rather than five
unrelated fields.

The structure is exactly what a transition needs: **where you are, where you are going, where you
came from, and how.** The previous-field pair is why the game can put you back at the right door
when you re-enter an area.

`+0x1062` is the single most-consulted byte in the payload - **19 functions** - and one of its bits
has an authored name (`ClearFlag1062_Bit04`), so it is a per-transition flag word.

### The consolidated map

| Payload range | Bytes | Content |
|---|---:|---|
| `+0x0010`, `+0x0014` | 8 | read by `ActorManager_RunFieldRuntimePass` |
| `+0x1000`, `+0x1020`, `+0x1040` | - | transition-adjacent, unnamed |
| `+0x1044` .. `+0x1063` | 32 | **world-transition record** (above) |
| `+0x1364` | - | unnamed, just before the flag banks |
| `+0x1384` .. `+0x1393` | 16 | `Bank64A`, `Bank64B` |
| `+0x1394` .. `+0x13B3` | 32 | **gap, unexplained** (AA-5) |
| `+0x13B4` .. `+0x14B3` | 256 | `Bank2048` |
| `+0x14B4` .. `+0x14F3` | 64 | `Bank512` |
| `+0x14F4` .. `+0x1533` | 64 | `Primary` flags |
| `+0x1534` | 4+ | read by `ActorManager_RunFieldRuntimePass` - continues immediately after `Primary` |

That is **roughly 470 identified bytes** of 353,424 - up from 336. Still a fraction of one percent,
but it is now a *structure* rather than a scatter of addresses, and `+0x1534` shows the mapped
region continues rather than ending.

### What this census cannot see - and why AB-5 stayed open

This enumerates **direct callers of the base accessor only**. Any code that obtains the base once,
caches it, and passes the pointer onward is invisible to it.

**The achievement counters were not found.** `ACH_COUNT_STEP`, `ACH_COUNT_KILL` and the other nine
counters must be stored somewhere, and the natural guess is this payload - but no offset in this
census corresponds to them, and 31 of the 70 callers are unowned and unnamed.

The honest conclusion is that **the method did not reach them**, not that they are absent.
**AB-5 stays OPEN**, now with a recorded reason: a pointer-propagation-aware analysis is required,
not another census of direct callers. *(Dated 2026-09-02; `AB-5` is ANSWERED since 2026-09-10, §8e below.)*

## 8e. Propagated 2026-09-10 — the analysis §8d asked for

The pointer-propagation-aware analysis this page recorded as the requirement for `AB-5` was run
with the kit's typed field scanner and is published as
[`the-save-payload-field-map.md`](the-save-payload-field-map.md): **the achievement block is inside
the image at payload `+0x8000`** (`00253970` points `020927C0` at buffer `+0x8200`), and the two
SpawnKeep images, the group banks, the transition snapshot and its mirror, the transition metadata
and the inventory descriptors are placed. **`AB-5` is ANSWERED**; the residue is `FG-1`–`FG-4` on
that page.

## 9. Related

- [`../../00-Engine-Core-Runtime/Shared-State-Accessors/cross-subsystem-accessor-hubs.md`](../../00-Engine-Core-Runtime/Shared-State-Accessors/cross-subsystem-accessor-hubs.md) — U-1 was raised there; the area-id hub reads this payload
- [`../../24-Compiler-And-CRT-Runtime/Binary-Hardening-And-Hooking/image-hardening-cfg-aslr-dep-and-stack-cookies.md`](../../24-Compiler-And-CRT-Runtime/Binary-Hardening-And-Hooking/image-hardening-cfg-aslr-dep-and-stack-cookies.md) — the security cookie cross-confirmed here, and the no-op `_guard_check_icall`
- [`../../03-World-Area-Field/`](../../03-World-Area-Field/) — the area id this header records
- [`../../11-Party/party-roster-and-control-suppression.md`](../../11-Party/party-roster-and-control-suppression.md) — PartyFocus, whose selector goes into the header

## 8c. Falsification pass 2026-09-02

**Attack chosen.** The headline asserts a **count**: *"the game keeps **four** copies of it in
memory at all times, evenly spaced."* A count is falsified by finding one more. The killer looked
for was a **fifth buffer** at the next stride in either direction — the same bounds test that
overturned the slot count in
[`../../02-Resource-And-Asset-Pipeline/authored-data-table-registry.md`](../../02-Resource-And-Asset-Pipeline/authored-data-table-registry.md).

**Result: SURVIVED, and each buffer gained a confirmed role.** A reference census over all four
buffers plus the stride slot above and below shows every buffer is reached by named accessors that
identify what it is for:

| Buffer | Referenced by | Role |
|---|---|---|
| `02164280` | `GetActiveRuntimeBuffer`, `ClearActiveRuntimeBuffer`, `ResetActiveImageAndRebindState`, and **read** by `BackupActiveRuntimeBuffer` | **ACTIVE** |
| `021BA940` | `GetCaptureStagingBuffer`, and **read** by `CopyCaptureToWriteSubmissionBuffer` | **CAPTURE STAGING** |
| `02211000` | `GetWriteSubmissionBuffer`, and **written** by `CopyCaptureToWriteSubmissionBuffer` | **WRITE SUBMISSION** |
| `022676C0` | **written** by `BackupActiveRuntimeBuffer` | **BACKUP** |

The read/write direction alone distinguishes the pairs: staging is read and submission written by the
same copy; active is read and backup written by the same backup. **Four buffers, four roles, no
ambiguity.**

**Bounds.** The stride slot **below** (`0210DBC0`) has **zero references of any kind** — there is no
buffer 0. The slot **above** (`022BDD80`) has exactly one reference, and it is **not** a buffer
access: no `LEA` of the address, just an indirect `MOV qword ptr [R14 + 0x20], RAX`. There is no
fifth buffer. The headline count is correct.

### OVERTURNED: the 48-byte gap is not padding

Chasing that single reference found something the document had assumed away. `FUN_002EFA70` clamps
its first argument to `0..6` and walks a **48-byte-stride array**:

```c
iVar9 = param_1 < 0 ? 0 : (6 < param_1 ? 6 : param_1);   // 7 entries, 0..6
lVar11 = iVar9 * 0x30;                                   // 48-byte stride
uVar1 = (&DAT_022bdd89)[lVar11];
*(undefined8 *)(&DAT_022bdd68 + lVar11) = 0;
(&DAT_022bdd70)[lVar10 * 6] = 0;                         // *6 on an 8-byte type = 48
...
```

Fields run `+0x64`, `+0x68`, `+0x69`, `+0x6B`, `+0x70`, `+0x78`, `+0x80`, `+0x88`..`+0x8B` from
`0x022BDD00`, so the array is based at **`0x022BDD60`**, seven records of 48 bytes.

Placing that against this document's own geometry:

```
buffer 4 (BACKUP)   0x022676C0 .. 0x022BDD50     (0x56690 bytes)
the "48-byte gap"   0x022BDD50 .. 0x022BDD80
record array        0x022BDD60 .. 0x022BDEB0     <- begins 16 bytes INTO the gap
```

**Three gaps are padding. The fourth is not.** Rather than assume, all four gaps were probed at
8-byte intervals across their full 48 bytes:

| Gap | Range | References |
|---|---|---:|
| after buffer 1 | `021BA910`–`021BA940` | **0** |
| after buffer 2 | `02210FD0`–`02211000` | **0** |
| after buffer 3 | `02267690`–`022676C0` | **0** |
| **after buffer 4** | `022BDD50`–`022BDD80` | **29** |

Section 6 told a modder that a runaway write *"lands in padding, not immediately in the next
buffer."* For gaps 1–3 that is **exactly right** — they are untouched by any instruction in the
image. For gap 4 it is **wrong**, and the space is not lightly used:

```
022BDD50   double     read by FUN_001C2F50 (SUBSD), written by FUN_002EFA70 (MOVSD)
022BDD58   byte       written by FUN_002EFE10, read by FUN_002EFA70
022BDD60   array base indexed at *8 and at *0x30 by a family of seven functions
                      spanning 002EF840 .. 002EFE10
```

An overrun of as little as **17 bytes** past the backup buffer lands on a live `double`. That is the
case a save-editor or memory-patch author is most likely to hit, because the backup buffer is the
last of the four — there is no fifth image to absorb the damage.

**Not established:** what the seven records are. The array is indexed `0..6` by `FUN_002EFA70` and
shared by six sibling functions, all sitting immediately after the save accessors in address order,
which is suggestive of save-slot metadata — but adjacency is banned as proof here and no field has
been read for meaning. The `*8` and `*0x30` stride views are also unreconciled. Registered as
**V-11**.

> **V-11 answered 2026-09-12 (FABLE): not save metadata — the seven records are the field-transition
> overlay (fade) request slots.** `002EFA70(slot, duration, mode, white)` read whole: the slot is clamped
> to 0–6 (`002EFA90`–`002EFA9D`), any live effect in the record is released (`0024CFF0`, `002EFB55` /
> `002EFBBB`) and the record refilled — `+0x28`–`+0x2B` four colour bytes taken from a pending static
> override, from the record's own bytes when `mode` and `+4` allow, or the constants **`0x80000000`
> / `0x80FFFFFF`** (half-alpha black / white, chosen by the fourth argument, `002EFC58`–`002EFC67`);
> `+0x2C = 2 × duration`; `+5 = mode`; `+8 = +0xA = 1`; flag nibbles at `+9` and `+0x24`; then the
> overlay object is allocated from the 0x1C0-byte pool (`00375900`, handle at `+0`) and started
> (`003B0F80(handle, 1)`, `+4 = 1` on success), and three statics are latched (`3`, `0`, `6`,
> `002EFCF4`–`002EFD05`). Its eight callers are the transition requesters —
> `WorldTransition_RequestFieldTransition` (slot from the request's byte `+2`, `003144E5`),
> `WorldTransition_RequeueCurrentFieldForRestore`, `ActorManager_RunFieldRuntimePass`, `00228C70`
> (twice), `0027EFA0`, `00280140`, `002CC960`. The array sits after the save buffers by allocation
> order only; nothing in it is saved.

### Arithmetic re-verified

Every number in the headline was recomputed from the addresses rather than carried forward:

```
spacings          0x21BA940-0x2164280 = 0x566C0
                  0x2211000-0x21BA940 = 0x566C0
                  0x22676C0-0x2211000 = 0x566C0     all equal
image             0x56690 = 353,936
spacing           0x566C0 = 353,984
gap               0x566C0 - 0x56690 = 0x30 = 48
four buffers      4 x 0x566C0 = 0x159B00 = 1,415,936 bytes
```

All consistent with the document as written.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. The image-address resolver fan-out is MECHANICAL.*

- **Items_Equipment_Shops_License — CLIENT and SERVICE.**
  - `GameState_GetGil` / `GameState_SetGil` are called by the gil-class inventory appliers and both shop commits.
  - The header-copy site `003F4AA0` reads and writes gil and grants items twice (`Inventory_GrantEncodedLootItem`).
- **Presentation — CLIENT.** The cited helpers are also read by rendering-side code:
  - `0017F8C0` (28 B) by four bodies, including the 6,441-byte and 2,440-byte render bodies;
  - `00247870` by a 1,307-byte body;
  - `0024CFF0` by `CharacterRenderRecord_UpdateRootAnimationPre…` and `CharacterRenderRecord_TeardownAndReset`;
  - `002CC960` by the 4,810-byte body;
  - the 0x1C0-byte pool allocator `00375900` by five bodies of 578–2,736 bytes.
- **Input — SERVICE.**
  - `0017CDF0` calls a 69-byte Input-filed helper.
  - `00228C70` calls two helpers, of 50 and 80 bytes.
  - The save-buffer binder `00253970` calls two helpers, of 24 and 26 bytes.
  - `0027F5D0` calls one helper, of 30 bytes.

## Crossings into other layers — addendum, FINAL-AUDIT pass 22 (OPUS, 2026-09-18)

Two crossings the 2026-09-14 pass above did not reach. Both are the **restore** side consulting
another layer, and this page owns nothing in either. Call sites read from the shipping image.

- **Gameplay — CLIENT, two edges.**
  - `00233C10` calls **`BattleSystem_ResetRuntimeState`** (`00237DF0`) at **three** sites —
    `00233C3F`, `00233C48`, `00233C59`. That body is the restore entry: it runs the bank reader
    `00235AF0` (`00233C14`), resolves the payload base through `002EF640` and `add rax, 0x4E68C`
    (`00233C25`–`00233C2A`), caches it in a global (`00233C33`), calls `0030B6A0`, and only then
    resets the battle runtime. **Restoring a save is what makes it reset battle state**, which is
    why the edge exists and why it belongs to this page's subject rather than to Gameplay.
  - `00235AF0` calls **`BattleEncodedId_IsValidForClass`** (`00322C50`) at **`00235C59`** — the bank
    reader validating an encoded id as it copies back. The same shared validator is already named
    from the other end on
    [the party-read page](../../01-Script-VM-Native-Bridge/Party-Presentation-Verbs/the-party-read-in-state-machine.md).
- **Developer — CLIENT, one edge.** `0017D6E0` calls `001C2F50` at **`0017D831`**, in a fixed
  sequence: `001C2F40` first (`0017D81E`), then a test of `byte [rax+0x463C]` gating a call to
  `0022FFE0` (`0017D823`–`0017D82C`), then `001C2F50` **unconditionally**, then `001E05E0`
  (`0017D836`). This page already cites `001C2F50` — but only in the globals table, as a reader of
  the double at `022BDD50`, which names the endpoint and not the edge. **Naming the endpoint
  somewhere on the page is not accounting for the edge**, and §4.2 is explicit about that; the call
  site above is.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**CombatFormula — CLIENT.** `BattleFormula_ApplyTargetResult`, owned by that layer, calls `00253690` on this page. That caller is the target-result application: it resolves the owning unit for both the source and the target stats records, keeps bit 9 of its flags argument as a switch, and **unless bit 0 is set** runs an eligibility test between the two units that abandons the whole call when it fails; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Rewards_Progression_Economy — CLIENT.** `BattleUnit_ProcessDefeatRewardsAndLoot`, owned by that layer, calls `00254EE0` on this page. That caller is defeat-and-loot processing, which reads the defeated unit's `+0x698` block, needs `byte[+5] == 1`, and is suppressed entirely by bit 3 of `byte[+0xE9A]`; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**CombatAction — SERVICE (7 edges, two subjects and two callers read).** The combat-action layer's
**execution-resource lifecycle** reads and writes Gil through the two accessors cited here, and it is
a complete four-phase cycle rather than seven separate relationships:
`BattleAction_CheckExecutionResourceAvailability`, `BattleAction_PrepareExecutionResources`,
`BattleAction_ConsumeExecutionResources` and `BattleAction_RefundReservedExecutionResources` all call
`GameState_GetGil` `00253690`, and the last three of them also call `GameState_SetGil` `00254EE0`.
Check reads; prepare, consume and refund read and write.

Both accessors work the same object. `00253690` is three instructions —
`mov rax, [02092758] / mov eax, [rax+8] / ret` — so **Gil is the `dword` at `+8` of the game-state
object at `[02092758]`**. `00254EE0` does not simply store: it computes `new − current` first and
**branches on the sign**, taking `cl = 6` when the delta is positive and a different path when it is
not, so the setter knows a gain from a loss and says which. `00303BD0` returns 0 for a null unit and
takes its second argument as a `word`; `00300280` requires the unit's `[+0x698]` block and then
`byte[+5]` before it refunds anything.

The crossing is that the action layer spends and refunds through this page's accessors. This page
owns the field; it owns none of the lifecycle. Read from the shipping bytes 2026-09-14 (OPUS).
- **ActorEntity - CLIENT (6 edges).** `002EF2B0`, `0024CFF0`, `002EFA70` are also called by bodies filed to actor entity: `0025D9E0`, `0025B070`, `002628B0` (+1 more) - shared machinery across the layer boundary, no shared ownership.
- **Audio - CLIENT and SERVICE (6 edges).** `002EF2B0`, `007B9F80` are also called by bodies filed to audio: `00261F90`, `007BA7E0`; `00228C70` reaches bodies filed to audio: `00249CA0`, `002DEE70`, `00360D70` (+1 more) - shared machinery across the layer boundary, no shared ownership.
- **CombatAI - SERVICE (1 edge).** `00233C10` reaches bodies filed to combat AI: `00327F80` - shared machinery across the layer boundary, no shared ownership.
- **CoreRuntimeScheduling - CLIENT and SERVICE (15 edges).** `0017D6E0`, `001C1910`, `001C2F50` are also called by bodies filed to core runtime scheduling: `0017D6E0`, `0017CCD0`, `0022A0B0`; `0017D6E0`, `00228C70`, `00233C10` reach bodies filed to core runtime scheduling: `001A1460`, `001DB600`, `001E0550` (+8 more) - shared machinery across the layer boundary, no shared ownership.
- **PlatformOnlineAchievements - CLIENT and SERVICE (5 edges).** `00254E80` is also called by bodies filed to platform/online achievements: `003162E0`, `00316760`; `00583D60`, `00254EE0` reach bodies filed to platform/online achievements: `00316A50`, `00315390`, `003166F0` - shared machinery across the layer boundary, no shared ownership.
- **Script_VM_Native_Bridge - CLIENT (22 edges).** `002EFA70`, `003BB420`, `00254C90` are also called by bodies filed to script VM / native bridge: `00342A80`, `003433A0`, `00348970` (+19 more) - shared machinery across the layer boundary, no shared ownership.
- **Story_Event_Quest_Hunt - CLIENT and SERVICE (13 edges).** `002EF2B0` is also called by bodies filed to story/event/quest: `0032A8A0`, `0032A930`, `0032A9A0` (+9 more); `00583D60` reaches bodies filed to story/event/quest: `0032A8A0` - shared machinery across the layer boundary, no shared ownership.
- **UI - CLIENT and SERVICE (119 edges).** `00244960`, `00245020`, `00282DF0` are also called by bodies filed to UI: `00252030`, `00279E20`, `005528C0` (+88 more); `00253970`, `0027EFA0`, `00228C70` reach bodies filed to UI: `0029DBE0`, `00247AE0`, `0035C560` (+3 more) - shared machinery across the layer boundary, no shared ownership.
## The `00581DA0` exclusive subtree — all 4 members bound (SWE2-FRONTIER, followup queue)

*Pointer and two corrections (2026-09-19, FABLE).* What these states do - which file, which operation, in which
order - is on [how a manual save is committed](../how-a-manual-save-is-committed.md). Against the note below: the
numbers each arm adds to `+0xDC` are **progress weights** for the save gauge, not result codes; and the
"read-buffer enqueue" of state 1 selects the storage machine's **write** command.

`SaveSlotTransaction_StateMachine` (`00581DA0`, 640 B) drives the save-slot
transaction on record `rbx`: `rdi` is the result struct from `002EF640`, `dl`
the requested state. If `byte[+0xCC]` already equals it the call is a no-op
(`00581DD2`); otherwise `state−1` dispatches through the jump table at
`00582020` over eight cases. Every arm does its work then adds a result code
to the accumulator `dword[+0xDC]` (`00581FE3`) and reports it through
`00581860` before `byte[+0xCC]` commits the new state (`00581FF4`). The arms:

- state 1 — clears the result struct, `005837F0(1, +0xCD)` path →
  `00582730(path, rdi, 8)` (corrected 2026-09-29, OPUS, CON-192: path first, then the buffer and the size) enqueue; code
  `((+0xC8 & 1) << 6) | 0x10` (`00581E32`).
- state 2 — `005837F0(0, +0xCD)` → `005826D0` type-0xB enqueue; code
  `((+0xC8 & 1) | 4) << 2` (`00581E62`).
- states 3/4 — the same with `005837F0(1, +0xCD)`; state 4 uses
  `+0xCE + 2` as the path index (`00581E9E`); code `0x10`.
- state ~~5~~ **7** (CON-192: the table at `00582020` sends states 4, 5 and 6 to one arm and 7 here) — the submission arm: `005832B0` builds the descriptor into
  `+0xE8` from the result's `+0x18`/`+0x1A`/`+0x1B` fields with
  `+0xCD + 1`, `00583D60` returns into `+0xD8`, the `005837F0` path is copied
  and handed to `00583700`, and a UI request follows via `00582540` when
  `[02CA99C0]` is up; code `0x168` or `0xE6` by `+0xC8 & 1` (`00581F8E`).
- state ~~7~~ **8** (CON-192) — the result arm: `[rdi] = +0xD8`, `[rdi+4] = 1`, another
  `005837F0`/`00582730` enqueue; code `0x32` (`00581FA8`).

| member | role | interior |
| --- | --- | --- |
| `005826D0` (83 B) | `SaveStorageQueue_EnqueuePathOperationType11` — copies the path into a stack request with type `0xB` and posts it to the `[02CA99C0]` queue via `00582540` (`00582700` copy loop, `00582716` post) | [`005826E8`](../../_index/ADDRESS-INDEX.md) |
| `00582730` (94 B) | `SaveStorageQueue_EnqueueReadBuffer` — same queue post but type `7`, stashing the buffer pointer `rdx` and size `r8d` into the request (`0058276F`/`0058277C`) | [`00582748`](../../_index/ADDRESS-INDEX.md) |
| `005832B0` (1,091 B) | `SaveSlotMetadata_BuildSubmissionDescriptor` — validates `slot < 0xC8` and the `0x3C`-bounded time fields, takes the clock via `00254A10`, and formats the descriptor into `[01F2CCC0]` with the `00D23F18`/`00D23F38`/`00D23F4C` templates through `0017D2E0` | [`00583341`](../../_index/ADDRESS-INDEX.md) |
| `00583700` (230 B) | `SavePath_BuildSlotDirectoryName` — gated on `[02CA99B8]`, expands via `003935C0`, then formats `"%s%03d"` (`009153E4`) with the slot byte — the `slot%03d` directory name | [`0058374D`](../../_index/ADDRESS-INDEX.md) |

Shared callees deliberately outside the census: `002EF640`, `005837F0`,
`00582540`, `00581860`, `00583D60`, `003935C0`, `00254A10`, `0017D2E0`,
`00861EC0`, `00808C40`.
