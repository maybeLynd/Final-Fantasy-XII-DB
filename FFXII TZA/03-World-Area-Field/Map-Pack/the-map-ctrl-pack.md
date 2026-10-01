---
system: .mpk — the map_ctrl pack, 32 size-prefixed slots per map
category: 03-World-Area-Field
status: AUDITED
owner_layer: PrimaryOwner:WorldAreaField
evidence_tier: 1
verified_against:
  gzf_sha256: fb9b5e7ea002c1626a53d47da0b0b69a2443e246f7ce2b64329be4e034a2d3f7
  snapshot_sha256: a9cead8777597cdca58f2a47f27153f5231d60ad2bc16c3da9df8253820b09bd
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: additive-annotation across GN161 -> GN162 - REPLACED 2026-09-21 (OPUS), because the snapshot-identity basis this block carried is FALSE at GN162: this document cites record(s) 0026F470, which batch R30 touched. The weaker basis HOLDS and is measured: the advance changed 30 records in comment and tags ONLY - 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten (check_delta_additivity.py GN161 -> PARENT, control passed) - and check_stranded_absence.py, sweeping the GN160 resolved set which strictly CONTAINS all 30, reports no live absence claim on any line of this document
    verified: 86 cited function entries, 0 of them among the 128 records that changed across GN158..GN161 (check_delta_additivity.py, check_transfer_eligible.py); re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS-REQ-FABLE-PROVENANCE-TRANSFER-144 (9bedb5e0); re-targeted GN160 -> GN161 under EVIDENCE-STANDARD addendum 2026-09-14bh
    previously: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708 (GN160), superseded 2026-09-14
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
corpus_validated: "550 / 550 .mpk in the archive index, all split, 2026-09-12"
last_reviewed: 2026-09-12
archive_formats:
  - "mpk"
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-map-ctrl-pack-pass-1
  crossref_clean: true
  reopened_count: 0
---

# `.mpk` — the map_ctrl pack

> One pack per PS2 map (`ps2data/plan_master/map_ctrl/<area>/<map>/bin/<map>.mpk`): a count of 32,
> 32 section sizes, and the sections back to back. When a field loads, the engine requests two of
> them, splits each in place into 32 arena blocks, and hands the sound, world (`YM00`), navigation,
> `ACTL`, light and minimap sections to their systems — discarding the sections this remaster
> replaced.

**Corpus validation.**

| | |
|---|---|
| files examined | **550 of 550** `.mpk` entries, all split |
| size | 192 B – 8,054,336 B, 1,660 MB in all |
| count field | **32 in 550 / 550** |
| sizes add up to the file (the loader's own acceptance test) | **550 / 550** |
| the 0x40 slot before every section | **all zero, 4,568 / 4,568** |
| slots ever used | 0, 1, 4, 8, 9, 10, 13, 15, 16, 17, 24–31 — **the other 14 are empty in every file** |

Census: [`census.py`](../../_experiments/evidence/mpk-map-pack-slots/census.py) →
[`census.out.txt`](../../_experiments/evidence/mpk-map-pack-slots/census.out.txt).

---

## 1. What the player sees

**Much of what a place is, beyond its script.** Walking into a new area loads this pack: the
area's sound-effect bank and positional sound map, its world data, its navigation data, its lights,
and the picture and coordinates the minimap uses to show where you are. The dispatcher tests every
slot for null before handing it on, so a pack without a section simply supplies nothing for it.

## 2. The layout

```struct MpkHeader base=file
+0x00  u32       count      32 in 550 of 550
+0x04  u32[32]   size       section sizes in slot order; 0 = slot absent
```

The header is padded to a multiple of `0x40` (`((count + 1) * 4 + 0x3F) & ~0x3F` = `0xC0`). Then, for
each slot whose size is nonzero, in slot order: **a 0x40-byte slot** (zero in the file) and **`size`
bytes of section payload**. There are no offsets; a section's position is the running sum.

| slot | files | first bytes | size (median) | content | consumer (§3) |
|---:|---:|---|---:|---|---|
| 0 | 545 | `SeSe` | 2,816 | the `SeSep` sound-effect bank container | mode 0 → `02ADD080` → `003635E0` |
| 1 | 46 | `WD` + u16 | 32,256 | wave bank ([decoded, §2.4](#24-the-wd-section-slot-1--container-decoded-dead-authored-data-2026-09-20-swe2-data)) — **dead data**, no consumer exists | freed unread in both modes |
| 4 | 461 | u32 `1` | 18,112 | the navigation dataset ([decoded 2026-09-19](../../06-Movement-And-Navigation/how-a-unit-finds-its-way-across-the-navigation-mesh.md)) | mode 1 → copied to `02ADCFE8` → `Navigation_BindAndRebaseDataset` |
| 8 | 461 | `YM00` | 2,920,000 | world data — the tagged-chunk container is [decoded, §2.2](#22-the-ym00-section-slot-8--container-decoded-2026-09-20-swe2-data); per-tag contents open | mode 1 → `02ADCFE0`, mode 0 → `02ADCFF0` → `0026E760` / `0026E7D0` |
| 9 | 270 | `ACTL` | 128 | actor-control table ([decoded, §2.1](#21-the-actl-block-slot-9--decoded-2026-09-20-swe2-data)) | `02ADD0B8` → `003E8940` |
| 10 | 545 | `SPP1` | 128 | the map sound list — SE ids indexed by `mapsoundplay`, the `SP1` emitters and the weather ambience ([decoded 2026-09-13](../../18-Audio/Sound-Bank-And-Voice-Formats/spp-map-sound-list.md)) | mode 0 → `02ADD068` → `003635E0` |
| 13 | 387 | `EFB0` | 70,912 | the PS2 map effect bank | **freed in both modes**; the loose `ps2data/efb/<map>.efb` is loaded instead |
| 15 | 2 | `MRP\0` | 168,640 | map-gauge `MRP` package — the documented `MRP` container, byte-identical in both packs ([decoded, §2.5](#25-the-mrp-section-slot-15--container-decoded-dead-authored-data-2026-09-21-swe2-data)) — **dead data**, pointer forwarded but never dereferenced | `02ADD058` → `initgauge` (verb `0x01AB`) → dead create-param `+0x10` |
| 16 | 456 | `SP1\0` | 1,536 | sound-emitter block ([decoded, §2.3](#23-the-sp1-section-slot-16--container--emitter-record-decoded-2026-09-20-swe2-data)) | `02ADD060` → `003635C0` |
| 17 | 212 | `LGT2` | 1,984 | the light set — member records are the `02EBF420` group's `0x70`-stride objects the ACTL `+0x08` targets drive ([§2.1](#21-the-actl-block-slot-9--decoded-2026-09-20-swe2-data)) | `02ADD090` → `0037AA90(block, 0)` |
| 24–27 | 421 / 136 / 32 / 17 | `TIM2` | 525,376 | map pictures, one per sub-location; picture 0 is uploaded by `00378120` | `02ADD010`+ → `003C63A0` |
| 28–31 | 396 / 133 / 31 / 17 | `NPS2` | 64 | each picture's world placement | `02ADD030`+ → `00379870` |

**Slot 15 is carried, not read (corrected 2026-09-13; closed 2026-09-21 — §2.5).** This table said `initgauge` reads the `MRP` block. The
pointer `02ADD058` has exactly four rip-relative references — the dispatcher's store (`00378F04`), the teardown
load/clear (`003782EB`/`003782FC`) and the getter `00377B90`, whose only caller is `initgauge` (`0034DC70`).
`initgauge` passes it to `003E9020`, which tail-calls `00408300(kind, mrp)`; that sign-extends the pointer's
**low 32 bits** (`00408323 movsxd rax, edx`) into the create parameters of the gauge task `00406E80`, and
`002465F0` copies them into the create message at `+0x08` / `+0x10`. The handler was read in full — all three
message branches — and `+0x10` is never read anywhere, so no instruction reads the block's bytes: the slot-15
`MRP` is **dead authored data** (§2.5), not merely unproven.

Slots 24–27 and 28–31 pair up: a pack with `k` pictures has `k` placement records (the census counts
match slot for slot). The picture and placement formats are the ones the
[menu-map container](../../02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/sloc-menumap-container.md)
documents; `LGT2` is [`section_014`'s format](../../25-EBP-Script-Container/Sections/section-014.md);
`EFB0` is the [EFX/EFB container](../../17-Presentation-Rendering/Effect-File-Formats/efx-and-efb-effect-containers.md);
`SeSep` is walked by `002DF070` ([the sound request page](../../18-Audio/Audio-Boundary/how-a-sound-request-becomes-a-voice.md)).

### 2.1 The `ACTL` block (slot 9) — DECODED 2026-09-20 (SWE2-DATA)

`ACTL` is a **two-level, id-indexed record list** — the map's actor-control table. The block is
variable-size (64–1,792 B corpus-wide, 270/270 packs; the §2 table's "128" was the median). The
layout below is proved three ways at once: the header constants match the install gate, the index
arithmetic reproduces `003E8230`'s lookup exactly, and every one of the 270 shipped blocks parses
with **zero remainder** (`members/actl-census.tsv`, `gen_actl_census.py`).

```struct ActlHeader base=block
+0x00  char[4] magic          'ACTL'
+0x04  u16     version = 1           the 003E8940 install gate: word[+4] != 1 -> pointer cleared to 0
+0x06  u16     recordStride = 0x16   the three walkers advance rbx by +0x16
+0x08  u16     idBound               003E8230: id >= idBound -> miss
+0x0A  u16     reserved = 0
+0x0C  u16     idIndexOffset = 0x10  003E8230: table = actl + word[+0xC]
+0x0E  u16     auxTableOffset        003E7EC0 / 003E8D50: aux = actl + word[+0xE], passed to the handler
```

At `+0x10` sits the **id index**: `u16 bucketCount` then `bucketCount` × `{u16 bound, u16
recordByteOffset}`. Lookup of `id` (`003E8230`, 104 B, decoded in full): `bucket = id/100`
(unsigned magic divide, `0x51EB851F`), `slot = id%100`; miss when `id >= idBound`,
`bucket >= bucketCount` or `slot >= bound[bucket]`; hit returns
`actl + recordByteOffset[bucket] + slot*0x16`. Each bucket's records are **contiguous** —
`bound` records of `0x16` bytes packed back to back — and the census confirms `max(base +
bound*0x16) == auxTableOffset` in all 270 packs (records end exactly where the aux table
begins; the index ends exactly where the first record region begins). So `idBound` is *not* the
record count: it is the script-facing id space — e.g. `lus0115` has `idBound=0x65` (valid ids
0–100) but only **one** record, reached by `id==100` because bucket 0 is empty (`bound=0`) and
bucket 1's entry is `{bound=1, base=0x1A}`.

```struct ActlRecord base=record size=0x16   (1,822 records: 1,721 live + 101 all-0xFF tombstones)
+0x00  u16   state     0x0000 live / 0xFFFF tombstone; bit0 = processed (003E8020 sets),
                     bit1 = the alternator (003E85B0 sets / 003E8690 clears),
                     bits 2-3 = a two-bit override folded into the re-activation
                     predicate (003E8020: ecx = (w0&0xC)!=0 ? !bit1 : bit1; bit3 is
                     verb-driven: animepause 0x218 sets it via 00357100->003E8890,
                     animepauseclear 0x219 clears it via 00357490->003E8860),
                     bit4 = "was active" (003E8350 reads).
                     A tombstone makes every i16 field negative, so every `js` guard skips
                     the record naturally
+0x02  i16   slotId    timer-slot id (dense 0..0x4D, never -1 in live records) -> the
                     0x50-stride f32-slot family at 02EBB6E0/02ECB6E0:
                     activate writes f32 0.0 at slot+0x38 (004735D0 -> 00467700);
                     003E8440 inits the slot with f32 148542.5 (00473500) + raw 0x000140C1
                     (004735D0); 00466AD0 = "slot live" predicate (004735E0 wrapper)
+0x04  u16   pad04     0xFFFF in all 1,822 records — CLOSED dead authored (2026-09-22):
                     every `+0x04`/`+0x06`/`+0x0A`/`+0x0C` access in the
                     `003E7Exx`–`003E8Exx` family resolves to the block header
                     (`+0x04` version gate, `+0x06` stride) or the bucket index
                     (`entry+0x04` = recOff); no record pointer is ever read
                     there — all six `003E8230` callers are in-family
+0x06  u16   pad06     0xFFFF in all 1,822 — dead authored (same closure)
+0x08  i16   target    member-target spec: bit14 = 0 -> the word IS a member id driven
                     directly (003E8C50: 0037B0F0+0037A310 then 0037A130); bit14 = 1 ->
                     low 14 bits index an aux-table row {u16 count; u16 memberIds[]}
                     (btr ecx,0xE in 003E8190) and the same three ops are broadcast to
                     every member via the 003E8A70/003E8A10/003E8A40 stubs (arm/disarm
                     pairs 0037B0F0/0037B190, 0037A310/0037A3B0, 0037A130/0037A1D0 on
                     arg 0/1). 0x64..0x6B in 48 records else -1;
                     bit14 is never set in the corpus — the row-list path is format-only
+0x0A  u16   pad0A     0xFFFF in all 1,822 — dead authored (same closure)
+0x0C  u16   pad0C     0xFFFF in all 1,822 — dead authored (same closure)
+0x0E  i16   flagIdx   index into the 64-slot flag channel state (corrected 2026-09-22:
                     the byte array is `u8[64]` at **02F8F23C** — the earlier
                     "02D8F23C" figure was a transcription slip; the flag block reads
                     `{qword queue@02F8F228; u8 gate@02F8F238; u16 channel@02F8F23A;
                     u8 flags[64]@02F8F23C}`; 1..0x39 in 151 records else -1; all
                     < 0x40, matching the cmp ecx,0x40 guards). Per-flag byte bits:
                     bit1 = the flag's binary value (`00270130` writes it);
                     bit0 = in-progress (`002700F0(idx,0)` clears it, and copies
                     bit3 into bit2); bit2 = notify; bit3 = posted/dirty.
                     `0026FAD0(idx, value, mode)` — gated on `byte[02F8F238]` —
                     probes `0024F680` and, finding nothing pending, posts a type-2
                     message `{u16 idx; u16 mode}` through `0026F470` (queue
                     `qword[02F8F228]`, channel `word[02F8F23A]`) bracketed by
                     `0036C1D0`/`0036C140`, then marks `flags[idx] |= 8` and `|= 4`
                     when bit0 clear. `0026FDB0(idx)` re-queries the queue for the
                     slot's state (the `== 2` the `003E8350` query tests as mask bit
                     0x04). activate -> `002700F0` (clear bit0, set bit2 if bit3) +
                     `00270130` (set bit1) + `0026FE50` (notify — `02F8F238`-gated
                     record push clearing `flags[]` bits 0x0C, already named in the
                     world-tick doc); the alternator ops call `0026FAD0` with
                     `mode = s8[+0x15]` when non-negative else 0.
+0x10  i16   objectId  id < 0x3E8 -> 00362DC0 resolver -> a runtime object whose status
                     byte is `obj+0x08`: bit0 = active (the query's `00362E30` test ->
                     result bit 0x10); bit2 = activated mark and bit4 = cleared — set
                     by `00363A90` (sole caller `003E8C50`): `obj+0x08 = (old & 0xE9) |
                     (+0x14-hi!=1)<<1 | 1<<2`; bit4 = the alternator-phase mirror —
                     `00363AD0(id,1)` in `003E85B0` sets it, `00363AD0(id,0)` in
                     `003E8690` clears it. 0x64..0x84 in 809 records, one 0x07D5,
                     one 0x0000, else -1 — all < 0x3E8, matching the cmp ebp,0x3E7 gate
+0x12  u8    phaseKind high nibble = lifecycle phase (authored 0 -> stamped 3 by
                     first-touch, read as +0x12>>4: phase 0 -> init, phase 1 -> query);
                     low nibble = kind, authored 0-3 (2 x1192, 3 x386, 1 x78, 0 x64) —
                     DEAD at runtime: all 17 refs to the container base 02B5D080
                     enumerate to the 003E7Exx-003E8Exx family, every record access is
                     enumerated, and the only +0x12 reader is 003E8020's sar-4 phase
                     extract; activation 003E8C50 copies +0x02/+0x08/+0x0E/+0x10 but
                     not +0x12. Authoring-time classification, preserved through
                     retagging (003E88C0/003E8900 mask it back in with &0xF)
+0x13  u8    pair13    nibble-pair 0x01 x1340 / 0x00 x381 — nibbles swapped by first-touch; the
                     post-swap high nibble gates the processed-path phase dispatch
+0x14  u8    pair14    nibble-pair 0x00 x1492 / 0x01 x229 — nibbles swapped by first-touch; the
                     post-swap high nibble is the authored arg for the +0x10 object op:
                     `00363A90` writes it as `obj+0x08` bit1 (`hi == 1 -> bit1 clear`,
                     else set) alongside the always-set bit2 activated mark
+0x15  i8    mode      signed mode byte, -1 (0xFF) in all 1,822; 003E8AA0's filter:
                     processed only when +0x15 == mode arg or mode < 0.
                     Runtime writers: `003E88C0(value,id)` — retag + `w0 &=~8 |0x10`
                     + phase nibble reset (`+0x12 &= 0xF`); `003E8900(value,id)` —
                     retag + same `w0` edit + phase nibble set to 1 (`|= 0x10`).
                     Tail-called from the verb wrappers `00354710`/`00354AD0`
                     (**animeplay** 0x213 / **animeplaytiming** 0x280), which take
                     the new tag from `byte[rdx+0x15]` where rdx is the verb's
                     second arg = the **command-owner record** — resolved in
                     `VMNativeCommand_ExecuteLifecycle` (`002621D0`) as
                     `owner = qword[qword[b+8] + cmdState[8]*8 + 8]` via
                     `00358940` (or `b` itself when `cmdState+8 == word[b]`).
                     So **+0x15 is the invoking command owner's group byte
                     copied in** — retagging reparents the record to the
                     invoker's group; the owner byte's own writers live in the
                     script-VM spawn family (`0x26xxxx` inits), a VM-lane
                     question
```

The aux table at `actl + word[+0x0E]` is a second index — `{i16 bound; i16 rowOffset[bound]}`
— where each offset is **relative to the ACTL block base** and points at a
`{u16 count; u16 memberIds[]}` row (`003E8190` resolves `rowOffset[id & 0x3FFF] +
qword[02B5D080]` — the same global). Member ids resolve through the **group table at
`02EBF420`** (corrected 2026-09-21: the earlier `02E2F420` figure has zero references;
all eight member ops `lea` `02EBF420` — mechanical RIP resolution): **5 groups ×
`0x50`** (`0037A450` walks `02EBF420`..`02EBF5B0`; `0037B230` initializer caps idx ≤ 4),
group `+0x28` = `{u32 ?; u32 count; {u16 objSlot,
u16 memberId}[count]}` searched for the member id → objSlot, group `+0x20` =
`{u32 ?; u32 bound; u16 objIndex[bound]}` maps objSlot → objIndex, and the resolved
object at `qword[group+0x00] + objIndex*0x70` gets flag writes at `obj+0x13`.
`0037B230` inits a group: `+0x00`..`+0x3F` zeroed (clears the `+0x18` sub-struct ptr
too — `0037B290` reads `word[struct+0x10]` behind it), `f32[+0x40]`/`+0x44`/`+0x48`
= 1.0, `byte[+0x4C]` = 0.

**The group table is the `LGT2` runtime** (decoded 2026-09-21, SWE2-DATA):
`0037AA90(block, group)` is the slot-17 `LGT2` installer — it gates on
`dword[block]==0x3254474C`, resets the group via `0037B230`, and stores the block
itself at `group+0x00`. Two callers: the slot-17 binder installs into group 0
(`02ADD090 → 0037AA90(block, 0)`, with `003DE920` alongside) and `0032F1B0(idx)`
installs `qword[022C6E20 + idx*8]` into group `idx` (groups 1–4 — a second
LGT2-block source table). `0037AA50(idx)` clears `group+0x00..+0x18`/`+0x4C`;
`0037ACA0`/`0037ACD0` are the group-0 gate ops called from `003DE920`.

The `0x70`-stride "member objects" are **authored LGT2 records inside the block**:
`member[i] = block + i*0x70` for `i < u16[block+0x0A]` — member[0]'s first 0x10
bytes carry the file header itself (`'LGT2'` at +0x00, `u16 subChainOff` at +0x04,
`u16 memberCount` at +0x0A). `subChainOff = 0x10 + count*0x70` in all 212 packs —
a 0x10 zero pad follows the member array, then a `{u16 size, u16 tag}` sub-record
chain terminated by `size==0`. The installer walks the chain through an 8-way jump
table (`0x37AC7C`): tag0→`group+0x08`, tag1→`+0x10`, tag2→`+0x18` (plus
`byte[elem+0x12]` cleared on its 8-stride elements when `dword[01EF94E0]≠0`, then
`0037A9B0(group,0)`), tag3→`+0x20` (the objIndex table), tag4→ignored,
tag5→`+0x38` (**the curve table**: `{u32 ?; u32 count; u32[count] offsets;
stride-walked records}` — the offsets are rewritten by `0020E620` to point at
each variable record, and each record is a `003CC5F0` piecewise-cubic channel
curve; kind-2 members index them three-at-a-time via `+0x14`/`+0x16`/`+0x18`),
tag6→`+0x28` (the memberId→objIndex search table), tag7→`+0x30`. Post-install
fixups: `member[i]+0x31` is remapped through a table at `01EF94E4` when `<6`, and
group-0 members get `member+0x37 |= 0x20`. Corpus tags seen: {3:212, 5:212,
6:211, 0:198, 2:123, 7:20} — 1 and 4 never appear.

**Sub-record interiors** (decoded 2026-09-22, census over all 212 LGT2 packs —
the stored pointers aim at the `{u16 size,u16 tag}` record headers, so consumer
offsets sit 4 bytes inside the bodies below):

- **tag 6** (`group+0x28`) = `{u32 count; count×{u16 memberObjIdx; u16 subId}}`
  — the first hop of member resolution: the member-op functions linear-search
  `word[entry+2]` for the authored sub-id and take `word[entry+0]`
  (`0x37A15D`–`0x37A18D`). Sub-ids are small group tags (0,1,5…).
- **tag 3** (`group+0x20`) = `{u32 count; u16 memberArrayIdx[count]}` (mod-4
  padded) — the second hop: `dword[+4]` bounds-checks the tag-6 result and
  `word[+8+i*2]` yields the index into the `0x70` member array
  (`qword[group+0x00]`). The resolved member then gets the flag op
  (e.g. `and byte[member+0x13], 0xFD` — clears charging-enable bit1).
  `0037B030` uses the same two-hop for its pending-test; a tag-6 **miss**
  falls back to index 0 — `tag3[0]` is the default member tested when the
  authored id has no explicit pair.
- **tag 0** (`group+0x08`) = `{u32 count=1; u16 0; u16 idx}` in all 180 packs —
  **dead-authored**: installed but never read by any consumer in the LGT2
  family (zero `group+0x08` loads).
- **tag 7** (`group+0x30`) = `u16[12]` sparse table, `0xFFFF` sentinels with
  entries at slots 4 and 8 in all 18 packs — **dead-authored** the same way
  (installed at `0x37ABE0`, reset at `0x37B263`, no reader).
- **tag 2** (`group+0x18`) = `{u32 pad; u32 count;
  count×{u16 id; u8 kind; u8 pad; u16 base; u16 bound}}` — count is 0 in all
  123 records, so the `0037AF4D` kind-gated element walk is dead on shipped
  data (the `+0x12` byte it reads is the ENTRY kind, unrelated to member
  `+0x12`).

**Consumers** (all read the installed pointer at `02B5D080`, stored by `003E8940`, reset by
`003E8D50(-1)` inside it):

| function | shape |
|---|---|
| `003E8230` | `id` → record lookup (the index decode above) |
| `003E7EC0` | iterates every bucket's every record; per record calls `003E8020` (first-touch) |
| `003E8D50` | same bucket/record iteration; per record tails into `003E8C50` — called by the `003E8940` installer: **activates every record's channels on map load** |
| `003E8AA0(mode)` | per record where `mode < 0` or `movsx rec[+0x15] == mode`: `0037A500(0, word[+0x08])` — the snapshot op |
| `003E82F0(id)` | lookup → `003E8350` — **query-by-id** (result mask) |
| `003E8BF0(id)` | lookup → `003E8C50` — **activate-by-id** |
| `003E88C0(value,id)` | retag `+0x15`, clear `w0` bit3, set bit4, phase→0 — tail of `00354710` |
| `003E8900(value,id)` | retag `+0x15`, same `w0` edit, phase→1 — tail of `00354AD0` |
| `003E8890(id)` / `003E8860(id)` | set / clear `w0` bit3 — tails of `00357100`/`00357490` |
| `003E8190(idx, aux, cb, arg)` | aux-row member driver: `ecx = idx & ~0x4000` selects `{u16 count; u16 memberIds[]}` row `word[aux+2+ecx*2]` (offset rel. base); calls `cb(memberId, arg)` per member, early-exit on first nonzero — `003E8350` uses it as a list-any charge test with `cb = 003E82A0` |
| `003E82A0` | two-instruction trampoline `0037B030(0, id)` — the per-member charge-test callback `003E8190` invokes |
| `003E8A70` / `003E8A10` / `003E8A40` | broadcast stubs for `003E8190`: `arg ? disarm : arm` — `0037B0F0`/`0037B190`, `0037A310`/`0037A3B0`, `0037A130`/`0037A1D0` |
| `003E7F20`-family | ranged first-touch: buckets `lo..hi`, `003E8020` per record |
| `003E8DB0`-family | ranged activate: buckets `lo..hi`, `003E8C50` per record |
| `003E82B0` | teardown: `qword[02B5D080] = 0; byte[02B5D088] = 1` (the state-machine gate flag) |

The handlers are a per-record **state-cycling machine**, driven by `003E8020`. On
first-touch (`w0` bit0 clear): `+0x12` is restamped `{phase=3 | kind}`, `w0` bit1 is
cleared, `+0x13`/`+0x14` get their nibbles swapped, `003E8990` clears `w0` bits 3–4 and
primes the channels (`+0x02` slot ← 148542.5 then 0.0; `+0x10` object ← `00363A90` with
the `+0x14` arg nibble), `w0` bit0 is set, and `003E8C50` runs. On later passes (bit0
set, gate flag `byte[02B5D088]` clear): if the `+0x13` post-swap high nibble is 0 —
authored low nibble was 0, the 381-record minority — the phase nibble runs `003E8440`
(phase 0, init) or `003E8350` (phase 1, query; result 0 sets `w0` bit4 "query-clean").
Then `w0` bit1 alternates two writes: bit1 set → `003E8690` (clears it), bit1 clear →
`003E85B0` (sets it); and bit4-set + bit1-clear records get `003E8C50` re-activation.

| handler | effect on the `+0x08` targets' `obj+0x13` | other channels |
|---|---|---|
| `003E8C50` activate | `{b0=1, b1=0, b2=0}` (arg-0 arms `0037B0F0`/`0037A130`/`0037A310`) | `+0x02` ← 0.0; `+0x0E` bits (`002700F0`/`00270130`/`0026FE50`); `+0x10` obj+0x08 bit4 (`00363AD0`) |
| `003E85B0` | `{b0=—, b1=0, b2=0}` (only `0037A310`/`0037A130`) | `+0x02` ← 0.0; `+0x0E` (`0026FAD0` + `002700F0`); `+0x10` bit4 (`00363AD0`) |
| `003E8690` | `{b0=0, b1=1, b2=0}` (arg-1 arms `0037B190`/`0037A1D0` + `0037A310`; also `0037A270`) | `+0x02` ← init value when its r9 arg ≠ 0 |
| `003E8440` init | `0037B030` predicate per target (early-exit on first active kind-2); also `0037A270`/`0037A1D0` arms | `+0x02` ← 148542.5 + raw `0x000140C1`; `+0x0E` (`0026FAD0`/`0026FDB0`/`002700F0`); `+0x10` (`00362E30`/`00363180`) |
| `003E8350` query | none — `0037B030` per target (direct or via traversal) | `+0x0E` `0026FDB0` state==2; `+0x10` `00362E30` obj+0x08 bit0. Returns mask: bit0/1 = pre-state (`w0` bit4, `+0x02` slot-live), `0x08` = active kind-2 target, `0x04` = flag-slot state 2, `0x10` = obj bit0 |
| `0037A500` snapshot | kind-2 objects: `dword[obj+0x28]` → `dword[obj+0x2C]` | — |

The `0x70`-stride member objects behind the group table carry a small state machine
of their own, and the ops above decompose cleanly onto it:

| obj field | semantics |
|---|---|
| `+0x12` | u8 kind — `== 2` is the chargeable kind (`0037A450`, `0037A270`, `0037A500`, `0037B030` gate on it); `0037A5B0` dispatches on it too (kind-1 → lerp arm, kind-2 → curve arm, kind-0 → no arm) |
| `+0x13` b0 | **suspend** — set `0037B0F0` / clear `0037B190`; while set the object is skipped by `0037A450` charging, `0037B030` pending-test, `0037A500` snapshot and the `0037AExx` traversal |
| `+0x13` b1 | **charging enabled** — clear `0037A130` / set `0037A1D0`; `0037A450` requires it; `0037A5B0` early-outs without it for every kind |
| `+0x13` b2 | **re-arm on overflow** — clear `0037A310` / set `0037A3B0`; when the accumulator crosses the limit, b2 resets it to 0, otherwise it clamps at the limit |
| `+0x14`/`+0x16`/`+0x18` | per-kind union: kind-1 = **s16 lerp start triple**; kind-2 = **three consecutive i16 indices into the tag-5 curve-offset table** (`group+0x38`) — all 50 kind-2 records carry (i, i+1, i+2), groups spaced 4 apart; kind-0 = packed authored payload, not channel data |
| `+0x1C`..`+0x1F` | packed authored payload (populated on kind-0; the kind-2 curve parameter is `member+0x2C`, read as `[member+0x10 + 0x1C]` inside `0037A5B0`) |
| `+0x28` | per-kind union: kind-2 = f32 charge limit (corpus: 100.0×32, 10.0×16, 240.0×1, 30.0×1); kind-1 = s16 lerp **end** channel 0 (`+0x28`,`+0x2A`,`+0x2C` = the end triple); kind-0 = packed authored payload |
| `+0x2C` | per-kind union: kind-2 = f32 accumulator (authored 0) — `0037A450` adds **+1.0**/tick to kind-2, b1-set, b0-clear objects; `0037A500` writes `+0x28` into it; `0037A270` zeroes it; `0037B030` returns `+0x28 > +0x2C` = "still pending"; kind-1 = s16 lerp end channel 2 |
| `+0x30`/`+0x34`/`+0x38` | the output channel triple — `0037AExx`/`0037AF4D` collect `member+0x30` pointers into the `02EBF5C0` gather array for the renderer. kind-0 = static authored f32s; kind-1/2 = runtime-written each pass by `0037A5B0` |

**`0037A5B0(member+0x10, group)` is the channel evaluator** (decoded 2026-09-21):
gated on `member+0x13` bit1, it switches on `member+0x12`:

- **kind 0** (5,157 members): no arm — `+0x30`/`+0x34`/`+0x38` stay at their
  authored f32 values. Static light.
- **kind 1** (653): linear-interpolation triple —
  `out[k] = ( s16[+0x28+2k] − s16[+0x14+2k] )·t + s16[+0x14+2k]`, then ×**1/128**
  (`0x08C5B34`), written to `+0x30`/`+0x34`/`+0x38`. `t = 00466BF0()` = the active
  `02EBB6E0` tag-23 slot's `f32[obj+0xA8] × 0.01` — the same slot family ACTL
  `+0x02` ids index, so kind-1 lights fade on the tag-23 timeline.
- **kind 2** (50): each `+0x14`/`+0x16`/`+0x18` i16 indexes a u32 in the tag-5
  offset table (`group+0x38`), `0020E600`-decoded to a **`003CC5F0` piecewise-cubic
  curve** evaluated at `f32[member+0x2C]` (the charge accumulator), clamped
  [−1,1] → `+0x30`/`+0x34`/`+0x38`. `003CC5F0` =
  `{u32 @0; u32 keyFlag@4; f32 tFirst@8; f32 vFirst@0xC; f32 tEnd@0x10;
  f32 vEnd@0x14; keys @+0x38 stride 0x24: {f32 span@0; …; f32 c3@+0x28;
  f32 c2@+0x2C; f32 c1@+0x30; f32 c0@+0x34}}` — before `tFirst` → `vFirst`,
  past `tEnd` → `vEnd`, else `t/tEnd` walks key spans and evaluates
  `c0 + f·c1 + f²·c2 + f³·c3` inside the hit key.

So the `+0x08` member ops are a per-object charge timer on **kind-2 LGT2 members**
(the authored light set): `003E8C50` activate writes
`{b0=1,b1=0,b2=0}` (suspended, discharged, clamp-mode), `003E8690` writes
`{b0=0,b1=1,b2=0}` (charging), and the query's `0x08` result bit is "member still
charging". The `+0x28` "writer" question closes: **no runtime writer exists — the
limit is authored in LGT2**, delivered by `0037AA90` (and the `+0x2C` accumulator is
authored 0). Member `+0x12` kinds are authored {0: 5,157, 1: 653, 2: 50} across
5,860 members in 212 packs — and the kind byte is **the channel-mode dispatch**:
static / tag-23-timed lerp / charge-driven cubic curves.

**The charge consumer is the `animesync` script verb** (closed 2026-09-21): the
verb-dispatch table (`scriptvm-verb-table.tsv`) binds the whole family —
`0x213 animeplay` → `00354710` → `003E88C0` (retag `+0x15`, phase→0);
`0x214 animesync` → begin `003567F0` (resolves the target id into the verb arg via
`00267E10`) + poll `00355300`; `0x218 animepause` → `00357100` → `003E8890` (set
`w0` bit3); `0x219 animepauseclear` → `00357490` → `003E8860` (clear bit3);
`0x280 animeplaytiming` → `00354AD0` → `003E8900` (retag, phase→1). `00355300`
optionally refreshes that group's snapshots (`00267310` gate → `00473680` +
`003E8AA0(mode)` + `00466DD0`), then returns `003E82F0(id) != 0` — the record's
`003E8350` mask, whose `0x08` bit is exactly "a kind-2 member still charging". So
the zone script's `animeplay`/`animesync` pair arms an LGT2 member's charge timer
and blocks the script until `+0x2C` reaches the authored `+0x28` — a
wait-for-light-animation mechanism.

External drivers: `00314020` → `003E7EC0` (first-touch pass); `00355300` → `003E82F0` +
`003E8AA0` (query one id, then refresh snapshots — mode = `byte[ctx+0x15]` of its own
context object); `0034ECF0` → `00360710` (same `+0x15`-byte mode source); `00228130` →
`00360880` (~~bit-scans `dword[02CB9C4]`, dispatches `00360710(member=bitIdx, group=arg)`~~ for managers 1 to 3, finds the lowest set bit of `dword[022CB9C4 + 4*(m-1)]` and calls `00360710(member=bit, group=m)` once per manager - *corrected 2026-10-01, OPUS, on ORACLE's RC-17 correction, read at `003608A0`-`003608B0`*);
`002628B0` → `003603F0` (loops members 0–7 through `00360A50(member=i, group=arg)`);
`0034DB30` → `00360A20` → `00360A50` (forwarder). The `00360710`/`00360A50` family walks
the `022CB730` group table (0x80-stride groups, 8 × 0x10 slots) and passes the **group
index as `mode`** — so `+0x15` is a signed group tag: authored −1 in all 1,822 records
means the snapshot walk fires only on a negative mode or on records a runtime path has
re-tagged to a non-negative group.

Named residue after this pass: what the
`+0x04`/`+0x06`/`+0x0A`/`+0x0C` fields were for (unused-by-corpus).
(Closed since this list was written: LGT2 member kinds 0/1/2 semantics, the sub-record tag
interiors, the `003E8350` `0x08`-bit provenance — live-composed by `0037B030`'s
`member+0x28 > +0x2C` charge test, no stored upstream — `00363A90`'s `obj+0x08` write
(bits 1–2 = authored mode + activated mark, bit4 cleared; bit4 itself is the
`003E85B0`/`003E8690` alternator mirror), and the `0026FAD0` flag-channel op on the
`u8[64]` array at `02F8F23C` (gate `02F8F238`, channel `word[02F8F23A]`, queue
`qword[02F8F228]`) — the earlier `02D8F23C` figure was a transcription slip.)

### 2.2 The `YM00` section (slot 8) — container DECODED 2026-09-20 (SWE2-DATA)

`YM00` is the map's world-data container — the largest section (median 2.9 MB, 461/461 packs).
Its outer layout is proved two ways at once: `002F6AB0`'s index walk supplies the arithmetic
(`mov ecx,[r15-4]`/`mov edx,[r15]` adjacent-entry reads, `and …,0xffffff` offset mask,
`shl r14,4` 16-byte unit scale, `add r14,r11` base add, `shr ecx,0x18` tag extract,
`cmp eax,0x21` tag bound, `mov ecx,[r13+rax*4+0x1d72f8]` jump-table fetch with `r13` = image
base via `lea r13,[rip-0x1d6c88]` at `002F6C81`), and **all 461 shipped sections parse with
zero structural remainder** (`members/ym00-census.tsv`, `gen_ym00_census.py`).

```struct Ym00Header base=block
+0x00  char[4] magic          'YM00'
+0x04  u32     scalar        per-map 32-bit value: 459/461 hold an f32-shaped value
                             21.9–400; rbn0104 (0x56612CE3) and byu0101 (0x57048FB5)
                             hold Unix-timestamp-shaped values (2015-11 / 2016-03, the remaster
                             dev window — probably re-export stamps). **Never read by the
                             loader** — 002F6AB0 sets rbx = file+0x10 and only touches the
                             region at +0x10 onward, so +0x04 is authored export metadata,
                             not a runtime input
+0x08  char[8] authorTag     a level-designer surname, NOT the pack stem — 16 distinct values
                             corpus-wide (t-hiros x174, naomif x125, mtanaka x119, kazuk x19,
                             ndaichi/yoshida x4, rfukuza/hmorita x3, tkawamo/sanda x2,
                             katano/yamazak/okahisa/shenyic/takinok/yoshika x1). **Never read
                             by the loader** either — the whole 0x10 header except the count/
                             index base is export metadata (author + stamp)
+0x10  u32     indexCount    = 17 in all 461; rbx in 002F6AB0 points here, so this dword is
                             both the count and the index base
+0x14  u32[18] index         indexCount+1 entries {u24 offset | u8 tag}; offsets are 16-byte
                             units relative to file+0x10, strictly non-descending; the +1
                             entry is the end sentinel {tag=0xFF, off=end}
```

`chunk(tag_i)` = `file[0x10 + off_i·16, 0x10 + off_{i+1}·16)`; equal adjacent offsets mark an
empty chunk. After the last chunk the file is padded with 0/16/32/48 bytes — pure 16-byte-unit
alignment to EOF, no footer.

**The index is a fixed 17-slot schema — identical order in all 461 packs:**
`11, 25, 24, 0, 29, 33, 1, 30, 28, 22, 26, 32, 31, 17, 27, 23, 12` (ascending by offset).
That makes each tag a fixed-position member, not a record type in a stream:

| tag | chunk bytes (min–max) | empty in | §3.5 arm role (condensed) |
|---:|---:|---:|---|
| 11 | **128 always** | never | environment/ambient record → `0209A660` (`0026E8C0`); decoded below |
| 25 | **1152 always** | never | field-aware environment setup (`003ED190`, special-cases field `0x11A`) |
| 24 | 48–1,104 | never | `{u32 count; 0xC pad; count×0x10 sources}` exact in all 461 → derived `count·0xE0` alloc `[+0x1D0]` |
| 0 | 80–262,672 | never | `{u32 count; 0xC pad; count×0x40 rows}` — size exact in all 461; row = **a 4×4 row-major placement transform** — rows 0–2 = the node's scaled basis axes (w=0): 233,546/390,136 rows orthonormal (pure rotation, incl. 84,456 identity), 101,170 orthogonal × uniform scale, 54,699 orthogonal × anisotropic scale, only 721 sheared — row 3 `+0x30` = origin (w=1.0); `[+0x188]` base. Consumers split on how much of the frame they use: `002F5550` composes the **whole matrix** into the tag-30 world transform (`word[rec+0x02]`·0x40 selects the row — unparented path at `002F6013` computes `RotY(timelineAngle)·tag0` where `00202F00`/`00217880` builds the in-place Y-rotation and `00202D70`(`00217150`) multiplies `out = r8·rdx`; the parented path at `002F5EF8` conjugates — `tag0⁻¹·parent·tag0` via `00202D60` inverse — i.e. the row is the **joint frame** re-expressing the parent transform in the node's local basis), while `002F70CB` (init) and `002F67C0` (distance fade) read only the `+0x30`–`+0x3C` origin |
| 29 | 16–65,664 | never | `0x10`-stride records → `[+0x1B0]`; `word[rec+2]` = tag-33 selector — read under tag-30 b30 in `002F4520`/`002F5550` |
| 33 | 16–1,536 | never | `{u32 count; count×0x10 sources}` — count>0 in only 43 packs → `002F6740` builds `count·12` `{1,1.0f}` alloc `[+0x1D8]`; source record `{u16 ?; u16 tag0RowIdx(+0x02); …; s16 extA(+0x08); s16 extB(+0x0A); s16 extC(+0x0C)}` — the extents ×`1/4096` (`00908E30`) form a scaled vec3 radius; runtime record = `{u32 enable(+0x00); i32 state(+0x04); f32 accum(+0x08)}` — a distance-gated fade integrator (`002F67C0`) |
| 1 | 16–8,320 | never | `{u32 count; count×0x30 sources}` → `[+0x170]` count — count>0 in only 11 packs; `count·4` alloc `[+0x1C8]` |
| 30 | 64–343,600 | never | `{u32 count; 0xC pad; count×0x30 u16-field records}` exact in all 461 (764,018 censused) → `[+0x174]` count, `[+0x178]` record base (`001806F0` publishes); record fields below |
| 28 | **16 always** | never | chunk ptr only → `[+0x1A8]` |
| 22 | 224–2,804,400 | never | chunk ptr only → `[+0x180]` — per-instance oscillation specs; only 8 bytes/record (`+0x30`/`+0x34`) are live, the rest is a dead PS2-packet blob (§2.2) |
| 26 | 0–3,010,576 | 2 packs | bank-locked copy (`00467D00`/`00467D20`/`00467BF0`) + "resource present" flag `[+0x230]` |
| 32 | **0 always** | all 461 | `[+0x1B8]` = chunk ptr — a permanently empty anchor slot |
| 31 | 0–312,416 | 1 pack | `00232380` nested six-tag parse → first `0x68` sub-record |
| 17 | 0–119,120 | 29 packs | `00232380` nested six-tag parse → second `0x68` sub-record |
| 27 | 0–95,776 | 358 packs | `003ED840` — "current/next" cursor pair at `02B5F1A0`/`02B5F1B0` |
| 23 | 32–257,488 | never | `00466E70` (1453 B handler, unread) |
| 12 | 16–336 | never | `00468160` — binds against the tag-14 buffer and tag-32 payload |

**Positive control.** The independently re-derived jump table at `002F72F8` (34 image-relative
offsets, `r13 = 0x120000`) reproduces §3.5's arm addresses exactly — every handler above lands
inside `002F6AB0` (`002F6Cxx`–`002F6F19`), and the 15 tags absent from every shipped file
(2–8, 10, 13, 15, 16, 18–21) all share the default arm `002F6F19` (loop tail = skip). The
authored corpus and the dead tag space partition the switch cleanly.

**Tag 11 — the 128-byte environment record** (decoded 2026-09-20): the loader arm
`002F6DE9` publishes the chunk at `0209A660` and immediately unpacks the first 0x10
bytes; the rest is read lazily by the `0209A660` consumers. Live region is the first
**0x20 bytes** — `+0x20`..`+0x7F` are zero in all 461 packs:

| off | type | census | consumer |
|---:|---|---|---|
| `+0x00` | u32 | packed RGBA — top byte always `0x80` (`0x80000000` ×185 = black @ alpha 0x80, else `0x80xxxxxx`) — "bit31 set" is the alpha byte's bit 7, matching `+0x04`'s 0x80-alpha dominance | `==0xFFFFFFFF` keeps the previous `022D8ED8` (edi sentinel = −1, set at `002F6C4A` before the arm dispatch); else stored. `0036D400` unpacks the four bytes → floats ÷ `255.0` (`008C5B40`) → `00182280` apply on the command-record path (emits `0x45`/`0x47` records); `003ECE60` passes it through when its own dword `!= −1` |
| `+0x04` | u32 RGBA | `7f7f7f80` ×86, `80808080` ×60, alpha byte `0x80` dominant | `00466140` byte-quad → f32 RGB × `1/128` + `w=1.0` → `0209A3A0`–`0209A3AC` |
| `+0x08` | f32 | `0.1` ×448, `0.3` ×12, `0.2` ×1 | → `0209A6EC` |
| `+0x0C` | f32 | `1000.0` ×252, `100.0` ×32, `80.0` ×15, `20000.0` ×15 — distance-like | → `0209A6F0` |
| `+0x10` | f32[4] | populated in ~100 packs, zero elsewhere | `003781D2` `movups` gated by `dword[+0x1C]≠0`; `003ED217`/`003ED4E6` test `+0x10/+0x14/+0x18` all-zero → hardcoded default when field id `==0x11A` or vector empty |
| `+0x1C` | f32/u32 | sparse | the `003781D2` gate |

`0209A660` readers: the store `0026E8C0`, the `0026EA43` reset family, and consumers
`003781D2`, `003ECE74` (scales a byte of the vector by two f32 globals — colour grading),
`003ED1B4`/`003ED46E` (the `0x11A`-vs-vector branches above).

**Tag 30 — the `0x30` instance-source records** (census pass 2026-09-20): 764,018 records
across 461 packs. A u16-field row, not a float row:

| off | type | census |
|---:|---|---|
| `+0x00` | u16 | **tag-22 record index** — deduplicated, `< n22` in all 764,018 records (only 9 packs are sequential); `002F4520` resolves `index[v]` (the `+1` in the load skips the index's own count dword) → `rec+0x30` |
| `+0x02` | u16 | tag-0 row index — varied (`0x0114`–`0x0581` in samples) |
| `+0x04` | u16 | tag-26 entry index (`0x06`, `0x45`, `0x74`); `0xFFFF` sentinel ×10,346 |
| `+0x06` | u16 | `0xFFFF` sentinel |
| `+0x08` | u16 | seq id — sequential-ish (`0x4B`,`0x4C`,`0x3C`,`0x3D`,`0x18D`,`0x192`); `00466CB0` arg |
| `+0x0A` | u16 | zero |
| `+0x0C`–`+0x0F` | u32 | flag dword — low word `0x0031`/`0x1031` (b13 colour, b14 bucket, b30 tag-24 link); high byte = bank mask (`0x97`/`0x87`/`0x80`) |
| `+0x10` | u32 | zero in all |
| `+0x14` | u16 | tag-24 `0xE0`-table index when b30 (0/1) |
| `+0x16` | u8 | small varied byte (census: 0x14 ×725K, 0x28, 0x0F, 0x0A, 0x3C, 0x64, 0x10, 0x1E — not the `0x6014` constant the u16 reading implied) — **unread by every tag-30 consumer** (`002F4520`, `002F5550`, `002F67C0`, the `002F6AB0` load tail, `002F7380`): dead-authored |
| `+0x17` | u8 | flag byte → `[rsp+0x40]` seed in `002F4520` (mostly `0x60`, also `0x80`/`0x02`/`0x01`/`0x64`/`0x3F`) |
| `+0x18`–`+0x1B` | u32 | packed RGBA colour multiplier (`0x80442F2C`-class) or 0 |
| `+0x1C` | u8 | **mask-bit index** into the `0026E5F0` 64-bit fold — `002F4B8F`: `dec al; cmp 0xFD; ja` rejects {0,0xFF}, else `bt rax, +0x1C`; corpus 0xFF ×762,837 (99.8%), else small indices |
| `+0x1D` | u8 | variant byte (dedupe key — `002F7380`) |
| `+0x1E`/`+0x1F` | u8,u8 | a byte pair — `002F4520` multiplies them (`byte[+0x1E]·byte[+0x1F]`), negates, `cvtdq2ps` → `00180890` arg (float extent/divisor) |
| `+0x20` | u64 | per-slot bitmask (≤16 effective bits; `00466CB0` arg) |
| `+0x22`–`+0x2F` | — | zero in all 764,018 — dead-authored tail pad (`+0x28`/`+0x2C` explicitly verified 0, no reader in any consumer) |

**Tag-30 runtime expansion — decoded 2026-09-20** (`002F6AB0` post-index tail,
`002F6F2A`–`002F727E`): after the index walk the loader expands the `0x30` records
into a `0x70`-stride runtime array at `ctx+0x1C0` (`003EC8D0(6, count·0x70)`).
Per record (`rdi` walks `rec+0xC`, `rbx` walks `runtime+0x48`):

- `dword[rec+0x0C]` is a **32-bit flag word** (low word = the `0x0031`/`0x1031`
  census value, high word = `0x9700`/`0x8700`/`0x8000`): bit 13 = colour arm, bit 14
  = bucket counter (`inc dword[ctx + bit14·8 + 0x1F4]` — two counters at
  `+0x1F4`/`+0x1FC`), bit 30 = has tag-24 link.
- Bit 30 set → `u16[rec+0x14]` (`selector`, 0/1 in census) indexes the tag-24
  `0xE0`-stride table at `ctx+0x1D0` (tag-24 arm `002F6D33`: count → `+0x220`,
  `0x10`-stride sources → `+0x198`, `count×0xE0` alloc → `+0x1D0`) and writes `-1`
  to `entry+0xC0` — a deferred-alloc marker; a later pass (`002F71F0`) allocates
  `dword[ctx+0x22C]` bytes per marked entry. `+0x22C` is written by `002F6740`,
  the tag-33 arm's callee (`002F6D63` → `002F6740(ctx, chunk)`, which also stores
  a built array at `ctx+0x1D8`).
- Bit 13 set → `dword[rec+0x18]` (the `0x2F2C`/`0x8044` pair as one dword, e.g.
  `0x80442F2C`) is a **packed RGBA colour** decoded by `00466140`, scaled by `xmm6`,
  stored as the runtime `+0x40` vec4 (default `1.0×4`).
- Colour dword zero + `qword[ctx+0x40]` matrix present → `u16[rec+0x02]` indexes the
  **tag-0** `0x40`-stride table (`ctx+0x188`), fetches its `+0x30` position vec4,
  transforms it through the `ctx+0x40` matrix (`00231A90`) into runtime `+0x40`.
  So `+0x02` is a **tag-0 row index** — the census `0x0114`–`0x0581` range is within
  tag-0 row counts.
- Runtime record init: `+0x40` vec4 = `1.0`, ~~`+0x48`/`+0x58` = 0, `+0x50` = `-1`~~ **`+0x50` = 0, `+0x58` = `0xFFFFFFFF` (-1), `+0x60` = 0** - the stores are `[rbx+8]` / `[rbx+0x10]` / `[rbx+0x18]` with `rbx` = entry `+0x48` (`002F6FE4`-`002F6FEC`), matching the `+0x58` = -1 stated below (corrected 2026-09-25 (OPUS, TA-1 replay); `+0x50` is later filled by `002F5550` with the tag-23 slot record, [TA-1](../../_index/candidates/ta1-opus-replay-texture-anim-clock/)).

Then a **cross-link pass** (`002F7128`): outer loop `r13d` = `dword[02EBB6E0]` ×
each tag-30 record calls `00466CB0(slotIdx, tag0idx=u16[rec+0x02],
seq=u16[rec+0x08], mask=qword[rec+0x20])`. The slot family it walks —
`{bound dword[02EBB6E0], cursor dword[02EBB6E4]=-1, table qword[02EBB6F0],
chunk qword[02EBB6F8]}`, `0x50`-stride — is **built by the tag-23 arm's callee
`00466E70`** (`002F6DDC`; count = `dword[chunk+0x10]`, alloc `count×0x50`). This
is the *same* `02EBB6E0` family `ACTL`'s `+0x02` timer-slot ids index (§2.1) —
the direct ACTL↔YM00 coupling. `00466CB0` indexes `qword[02EBB6F0] +
slotIdx·0x50`, takes `qword[slot+8]`, and tests bit `u16[sub+0x2A]` against
`rec+0x20` — **`+0x20` is a per-slot bitmask** (census: small u16, `+0x22`+ zero →
≤16 effective bits authored). Runtime `+0x58` starts as `-1`: the first matching
slot's result fills it, a *second* match resets it to 0 — a uniqueness check —
and pass `002F71A1` then rewrites any leftover `-1` to 0 (unresolved). So
`+0x58` = the uniquely-matching slot object or 0.

Final tail (`002F722A`, two iterations): for counts `dword[ctx+0x1F4]` and
`dword[ctx+0x20C]` allocate a `count×2` u16 array (`+0x1E0`/`+0x1F8`) plus a
`2·ceil(count/8)` bitmap (`+0x1E8`/`+0x200`). `+0x20C`'s writer is outside
`002F6AB0` (residue).

So the `+0x30` record reads as: `{u16 tag22Idx, u16 tag0RowIdx/tag29Idx, u16 tag26Idx|0xFFFF,
u16 0xFFFF, u16 seq, u16 0, u32 flags{b13 colour|b14 bucket|b30 link|b24-31 bankMask},
u16 tag24Idx, u8 ?, u8 flagSeed, u32 packedRGBA, u8 maskBit|0xFF, u8 variant, u8 extA,
u8 extB, u64 slotMask, pad}`.
`+0x16`, `+0x28`, `+0x2C` are all unconsumed by
every pass — dead-authored (closed 2026-09-22).

**The per-bank consumer — `002F7380`** (invoked on the ctx from `0026E290` when
flag `0209A708` is set — a bank-change refresh): walks the tag-30 source records
(`+0x178`, count `+0x174`) and re-reads three fields:

- `u16[rec+0x04]` = an index into the `0x60`-stride entry table hanging off the
  tag-26 buffer at `qword[qword[ctx+0x150]+8]` (`+0x150` is written by the shared
  tag-14/26 alloc-copy tail at `002F6EB9`; tag 14 is never authored, so the live
  buffer is always tag-26's; the table count is `dword[buf]` → `ctx+0x224`,
  which `00467D20` builds — it is **Σ picture counts**, not the chunk's record
  count (a record holds a multi-picture TIM2)).
  Guard `≤ 0x3FFF`; `+0x04 == 0xFFFF` is an authored sentinel — 10,346 records
  corpus-wide — skipped by the bound check.
- `dword[rec+0x0C] & (1 << (dword[0209A6E8] + 0x17))` — **the flag dword's bits
  24–31 (the byte at `+0x0F`) are a per-bank presence mask** (`0209A6E8` = the
  active bank, so bank *n* = bit *n*+0x17; the census `+0x0E` values `0x8000`/
  `0x8700`/`0x9700` decode as banks {14} / {7,8,9,14} / {7,8,9,11,14}).
- `u8[rec+0x1D]` = a variant byte, deduped against the previous record's
  (`+0x1C` ≈ `0x00FF` in the census = low byte `+0x1C` ≈ `0xFF` constant-ish, high
  byte `+0x1D` the variant).

For each bank-member record the pass bumps `u16[tag26entry+0xE]` (a refcount,
walking the `word[entry+0xC]` successor chain too), then keeps entries with
refcount >1 under a budget — `00467AA0` = `0x1007FF − 3·(G1·G2) − dword[02CA6008]
− dword[02CA6004]`, `& 0xFFFFF800` — counting a per-entry cost from
`00466190` (`byte[+5]` clamp 7, `word[+6]`, `word[+8]`) and a type filter
`00466220` (`byte[entry]` ∈ `{0x14,0x1C}`). The survivors (`ctx+0x228` count)
get a `count×0x28` zeroed table at `ctx+0x218` — **the active-bank working set**.
So tag-30 records are the authored *instances*, tag-26 the *variant entries* they
select among per bank, and `002F7380` is the bank-change reselection.

**The tag-26 expansion — `00467D20`** (the copy callback of the shared tag-14/26
arm): the chunk is a `{u32 count; (count+1)×{u24 off16 | u8 0xFF}}` index over
named `TIM2` records — `{char[0x28] name (e.g. BGnpc_n1039, shops_…);
u32 picCount; u32 0; TIM2 image}` at `off_i·0x10`, `+0x28` mirroring the TIM2's
own `u16[+6]` picture count exactly (all 20,809 records, 459 packs —
`members/ym00-tag2226-census.tsv`). `00467D20` first sums the picture counts into
`dword[buf]`, allocs `Σ·0x60` at `qword[buf+8]` (the table `002F7380` reads), and
walks each picture via `00536080` — which treats the TIM2 header itself as the
list header: `byte[+0x05]` picks a `+0x10`/`+0x80` first-picture offset (0 in all
20,809), `u16[+0x06]` the picture count, pictures u32-length-prefixed. Per picture
the 0x60 entry is filled from the TIM2 picture header: `byte[pic+0x13]−1` (the
TIM2 imageType — 4/5 only corpus-wide) → class byte `+0x00` via the stride-4 table
at `00D12520`, `word[pic+0x14]`
→ `word[+0x06]` (width) feeding `003A1FE0` → `byte[+0x02]` and two bit-scans →
`byte[+0x03]`/`+0x04`, `word[pic+0x16]` → `word[+0x08]` (height), `byte[pic+0x11]`
→ `byte[+0x05]`, `word[pic+0x0C]`-relative link → `0020E620`-encoded index at
`dword[+0x14]`, sub-index `j` → `word[+0x0C]`, `+0x20`..`+0x5F` = 16 encoded-null
dwords (`0020E620(0)`); gate `byte[pic+0x12] ≠ 0x10` (always 3 → always taken) adds
`dword[pic+8]`-based link → `dword[+0x18]`, flag `0x10` → `byte[+0x01]`, and
`word[pic+0x0E]` → `word[+0x0A]`.

**The tag-22 consumer — `002F4520`** (the method callback installed at `ctx+0x130`
by `002F6AB0`): the sole reader of `ctx+0x180` (`002F4765`); the two other
`+0x180` `.text` hits are `002F6B9D` (ctx init) and `002F6D91` (the store), and
the `xmmword [rbp+0x180]` sites in `002F5xxx` are stack-local matrix copies, not
the ctx. The function walks a u16 candidate-id list (`qword[ctx + sel·8]`,
`sel` = argument — list heads at `+0x00`/`+0x08` with counts at `+0x10`/`+0x18`),
range-checks each id
against the bound globals, then resolves the tag-30 source record
(`ctx+0x178 + id·0x30`) and its `0x70` runtime entry (`ctx+0x1C0 + id·0x70`).
Gated on `dword[rec+0x0C]` flags it resolves the tag-22 record:

```text
tag22rec = tag22chunk + (dword[tag22index + (word[tag30rec+0x00] + 1)·4] & 0xFFFFFF)·0x10 + 0x30
```

i.e. tag-30 `+0x00` (movsx'd) +1 skips the index's count dword, and the resolved
offset +0x30 skips the record's own header. The authored record (348,239 across
461 packs — `members/ym00-tag2226-census.tsv`) is:

```text
+0x00  vec4  AABB min   (w = 1.0, 348,210/348,210 verified)
+0x10  vec4  AABB max   (w = 1.0)
+0x20  vec4  (128,128,128,128)  — uniform constant, all records
+0x30  u32   axis mask: 0 = static (338,279 / 97.2%), 1 = lane 2 only (704),
             2 = lanes 1+3 (7,594), 3 = all three (1,633) — callee stores
             lane1→runtime+0x1FC, lane2→+0x200 (lane3 computed, unstored)
+0x34  u32   period ∈ {2,3,4,6,8} — nonzero iff mode ≠ 0
+0x38  …     tail blob, 0x78–0x7E340 bytes (record lengths 0xB0–0x7E380;
             5,714 zero-length index aliases) — dead authored data, below
```

When `dword[rec+0x30] ≠ 0` the function takes a scaled timer float
(`qword[[rsp+0x78]+0xA8]`, ×`xmm9`; 0 when absent), clamps
`trunc(phase)` into `[0, period)` and subtracts it — leaving the **fractional
remainder** — then injects it into the vec3 lanes by axis mask
(1 → lane 2 only, 2 → lanes 1+3, 3 → all three) and calls
`00180720` — a tail-jump to `001E5540`, which stores lane 1 → the runtime
entry's `+0x1FC` and lane 2 → `+0x200`, then walks the entry's linked list
(`[+0x18..+0x20)`) calling `0060EC30(node, frameIndex)` — propagating the
clamped frame to each linked sub-record. A separate apply, `00180730` (the
`001A9930`-singleton → `001A9B70` family), runs earlier with a mode
`edi ∈ {0..4}` derived from the record's `+0x30` nonzero
test plus flag bits (flag b7 → `[rsp+0x74]`, b15 pick, b16-17 → `[rbp-0x70]`,
variant byte `+0x17`) — `edi ∈ {1,4}` also runs `00202D70` (matrix op on
`rbp+0x20`/`rbp+0x140`) first. So tag-22 records are the **per-instance
oscillation/mover spec deduplicated across tag-30 instances**: an exported
AABB triplet (not read by this consumer) plus `{axis mask, period}` driving a
sawtooth `phase mod period` offset into runtime fields `+0x1FC`/`+0x200`
(their semantic names unproven).

**The consumed surface is exactly 8 bytes per record** — `002F4520` aims the
record pointer at `rec+0x30` (`(off16+3)·16` = `off16·16 + 0x30`; the `inc`
on `word[tag30rec+0x00]` skips the index's u32 count dword, so `index[k]`
selects record `k` directly — verified against the AABB invariant on all
764,018 tag-30 references) and dereferences only `[r15]` and `[r15+4]`.
`ctx+0x180` has no other reader (the arm `002F6D91` is a bare store; `002F5550`
never touches `+0x180`). So the AABB/scale header `+0x00`–`+0x2F` **and** the
`+0x38` tail are dead authored data in TZA.

The tail itself is a **retired PS2 VIF/GIF packet stream** (HIGH confidence
as dead data; the format attribution is a byte-pattern HYPOTHESIS, matching
the WD slot-1/MRP slot-15 precedent of retired PS2-era payloads). At `+0x38`:
`u32` ∈ {23 in 96.4% of 342,525 records; else 5/7/15/17/19/21/31 — always odd
and <32, GIFtag-NLOOP-shaped}, `u32` 0, then a fixed 6-byte prefix
`04 04 00 01 01 80` + `u8 count` + `6c` (VIFcode `UNPACK`), followed by
repeating `… 0e/1e 30 12 04 …` sub-packets and `0a c0 NN 6e`-headed runs of
packed `XX·4` quads (`7f7f7f80`, `3f3f3f80` — V4-8-style normals/colours)
interleaved with f32s. The blob is a per-instance mesh/vertex stream the
PS2 original would have fed the VU1 pipeline; TZA's renderer never reads it —
the only fields that survived the port are the `+0x30` axis mask and `+0x34`
period.

The same pass reads five more tag-30 fields (all `002F4520`, verified):

- `word[rec+0x14]` → the tag-24 `0xE0` runtime entry (`imul r12, rax, 0xE0;
  add ctx+0x1D0`) — matrices at `entry+0x40`/`+0x80` are composed through
  `00202C70`/`00202D70` into the apply.
- `byte[rec+0x1C]` — **a bit index into the `0026E5F0` 64-bit fold**
  (`dec al; cmp 0xFD; ja` rejects `0`/`0xFF`, else `bt rax, bit`; the fold
  runs per record). Corpus: `0xFF` = disabled in 762,837/764,018 (99.8%);
  the rest are small bit indices — this corrects the earlier
  "`+0x1C` ≈ `0xFF` constant" note.
- `byte[rec+0x1E]`·`byte[rec+0x1F]` — a u8 pair, multiplied, negated and
  `cvtdq2ps`'d into an `00180890` arg (a float extent/divisor).
- `byte[rec+0x17]` — seeds a flag byte (`[rsp+0x40]`) the threshold path
  may set to 1.
- Flag dword **b30** (`+0x0C` bit 30) also routes `word[rec+0x02]`
  (movsx'd) into **tag-29** — `word[ctx+0x1B0 + idx·0x10 + 2]` selects a
  u16 that indexes the tag-33 `0xC`-stride array (`ctx+0x1D8`) for the f32
  at `+8`, compared against `xmm12` (a gating threshold; negative index →
  default). So `+0x02` is dual-role: tag-0 row index on the colour path
  (load time) and tag-29 index at update time under b30.
- The context object `[rsp+0x78]` carries a feature-mask dword at `+0x40`:
  bit 10 sources a float from `obj+0x98`, bit 11 from `obj+0xA0`
  (sign-flipped), bits 13–17 (`0x2F000`) override a mode; `obj+0x90` is a
  frame float → `cvttss2si` — the counter driving tag-26 entry reselection
  (`+edi`, clamped into `dword[buf]`, successor-check `word[entry+0xC]` →
  `001807F0`).

**The presentation pass `002F5550` re-runs the same chain per tag-30
record** (`r14` = record `+0x20` cursor, `rsi` = ctx — verified
2026-09-21):

- `qword[rec+0x20]` (the u64 slot mask) gated against per-pass masks at
  `[rsp+0x40]`/`[rsp+0x48]` — a skip gate.
- `dword[rec+0x0C]` bit 28 (`not eax; bt eax,0x1C`) is an inverted
  enable; `word[rec+0x0A]` would discriminate `{1..4}` but is **0 in all
  764,018 records** — the branch is authored but dead.
- `word[rec+0x14]` selects the tag-24 `0xE0` entry (`rbx`); its `+0xBC` /
  `+0xC8` floats are per-entry cull thresholds, and `qword[entry+0xC0]`
  is a **byte-bitmap pointer** (the `-1` expansion write is its unset
  sentinel): under flag b30 the tag-29→tag-33 selector writes
  `byte[bitmap+sel]` = 1/2 (inside/outside the `xmm10` threshold), and
  state 2 skips the record.
- `word[rec+0x04]` → `001807A0`; `word[rec+0x02]` → **tag-0 row pointer**
  (`·0x40 + ctx+0x188`) stored into the output record (`qword[rdi]`) and
  composed by `00202D60`/`00202D70` matrix ops — the tag-0 matrix
  handoff.

`002F5550` also calls **`002F67C0`** (at `002F5877`) — the
**distance-gated fade**: walks a u16 selector list (`word[r14 + cursor]`,
low 12 bits = tag-33 index), requires `dword[tag33rt+0x00]` enabled, then
reads the **tag-33 authored record** (`ctx+0x1A0`, `0x10`-stride):
`word[+0x02]` → tag-0 matrix row, and `s16[+0x08]`/`[+0x0A]`/`[+0x0C]` ×
`1/4096` (`00908E30` = `{1/4096}×4`, so extents are 12-bit fixed-point)
form a scaled bound vec3. It measures horizontal distance
`sqrt(dx²+dz²+ε)` (`00861F14` thunk) plus a `dy` check between the
reference point (`r12`) and the row's `+0x30` translation, derives an
inside/outside flag, edge-writes it to `dword[tag33rt+0x04]`, and
integrates `f32[tag33rt+0x08]` up/down by `xmm8` toward the bounds —
the runtime record is `{u32 enable; i32 state; f32 accumulator}`, a
hysteresis fade timer.

The `+0x174`/`+0x178` records and the `0x70` runtime array (`+0x1C0`) sit on the
0x240-byte load context that `0026E760` (mode-1) / `0026E7D0` (mode-0 →
`0209A668`) allocate via `003EC8D0`; `002F7380` reads the source records.

**The four method slots** `002F6AB0` installs at `ctx+0x128`–`+0x140` are the
consumers (field-access census over each body, `.text`):

| slot | fn | role |
|---|---|---|
| `+0x128` | `002F5450` | **destructor** — `003EC8A0` ×8 frees the runtime tables (`+0x150` region, `+0x1C0` array, `+0x1C8`, `+0x1D0`, `+0x1D8`, `+0x1E0`, `+0x210`, `+0x218`, `+0x220`), `00466B10`, tail `004680D0` |
| `+0x130` | `002F4520` | **per-instance update** — the tag-22 oscillation consumer above; also reads `+0x218`/`+0x228` (the active-bank set `002F7380` built), `+0x1B0` (tag-29 chunk), `+0x198`/`+0x1D0` (tag-24), `+0x1D8` (tag-33 array) |
| `+0x138` | `002F5550` | **per-frame presentation pass** — walks tag-30 records + the `0x70` runtime array, the tag-24 `0xE0` entries (`+0x220` count), `+0x22C` (tag-33 size → `00861EC0`), runs the `0026E5F0` five-mask fold and the `00202D70`/`00202D80` matrix ops; the `xmmword [rbp+0x180]` locals live here |
| `+0x140` | `002F5540` | **getter** — `return qword[ctx+0x160]` (the container `base+0x14` the ctor stored) |

So `ctx+0x1C0`'s readers are the update (`002F4520`), presentation
(`002F5550`) and teardown (`002F5450`) callbacks — the whole runtime-array
lifecycle lives in the method family. `+0x218`/`+0x228` are read by
`002F4520` and freed by `002F5450`.

`ctx+0x20C` is now **closed — it was never a standalone field**. It is the
high dword of `qword[ctx+0x208]`, and that qword is the unowned third member
of a `{ptr, ptr, qword}` block at `ctx+0x1F8` — `002F5450` runs
`003EC8A0` (free-and-null) on `+0x1F8` and `+0x200`, the same
`{+0x00,+0x08} owned-pointer` shape as the sibling block at `ctx+0x1E0`
(`+0x1E0`/`+0x1E8` freed, `+0x1F0` the third qword). The only touch anywhere
in the family is the init's `qword[rsi+0x208] = 0` (`002F6C22`); nothing
reads it and nothing populates either block — the other `+0x208`/`+0x20C`
`.text` hits (`002F239E`, `002F319C`, the `00454xxx`/`006FFxxx` clusters,
…) are unrelated structures, and the ctx-receiving callees (`002F6740`,
`0026E960`, `001806F0`, the destructor's `00466B10`/`004680D0`) never touch
it either. Dead/reserved tail space of an embedded member pair this
resource type leaves empty — there is no indirect writer to find.

**Named residue** (the MP-2 continuation): tag-22's
`+0x38` tail is now **closed as dead authored data** — `ctx+0x180` has exactly
one reader (`002F4520`) which reads only `+0x30`/`+0x34`; the blob is a retired
PS2 VIF/GIF packet stream (§2.2). `ctx+0x20C` is closed too — it is the high
dword of `qword[ctx+0x208]`, the unowned third member of the never-populated
`{ptr,ptr,qword}` block at `ctx+0x1F8` (above). Tag-30's `+0x16`/`+0x28`/`+0x2C`
are closed the same way — `+0x28`/`+0x2C` are 0 in all 764,018 records and
`+0x16` has no reader in any tag-30 consumer (`002F4520`, `002F5550`,
`002F67C0`, `002F6AB0`'s tail, `002F7380`): all dead-authored. `+0x04` is the
tag-26 entry index on both passes; `+0x0A` is authored-but-dead (0 in all
764,018). The container contract itself is closed.

### 2.3 The `SP1` section (slot 16) — container + emitter record DECODED 2026-09-20 (SWE2-DATA)

`SP1` is the map's **sound-emitter block** (456/461 packs; 704–9,792 B, always a multiple of
64). The layout below is proved by the four consumer bodies against all 456 shipped blocks
(`members/sp1-census.tsv`, `gen_sp1_census.py`).

```struct Sp1Header base=block
+0x00  char[4] magic          'SP1\0'
+0x04  u32     listBase = 0x20    byte offset of the weather-variant index list; the
                                 fallback reads it through the 0020E600 decode (identity)
+0x08  u32     offAreas           -> the listener grid (one 0x220 record, below)
+0x0C  u32     offEmitterIndex    -> {u16 bound; u16 recordOff[]} the emitter index
+0x10  u32     offEmitters        -> bit15-terminated u16 prefix list, then variable-size
                                    emitter records
+0x14  u32     reserved14        0
+0x18  u16     reserved18        0
+0x1A  u16     reserved1A        0 — dead in all 456 packs (see the weather path below)
+0x1C  u32     reserved1C        0
+0x20  ...     index-list region  {u32 count; i32 SPP1-index[]} lists; the active one is
                                 selected at runtime (00363B40 fallback)
```

The three region offsets tile `offAreas < offEmitters < offEmitterIndex` in every pack, and the
index's `recordOff` entries point into the emitter arena (2,326 records over 454 indexed
packs; 2 packs carry `offC = 0` and no emitters).

```struct Sp1Emitter base=record variable size -- dominant 0x60, min 0x40, larger for multi-point shapes
+0x00  i32   spp1Index   index into the SPP1 (slot 10) u32[+0x20] SE-id table;
                        negative = disabled (457 of 2,326 records ship disabled)
+0x04  u32   handle      runtime voice handle (0 in the file): released via
                        002DEE80/002DF150 on generation mismatch, written with the
                        002DEFA0 start result
+0x08  u8    flags       runtime flags (003638B0: bit6 cleared per call then set when
                        the arg2 gate <= 0; bits4-5 skip the voice start entirely;
                        bit3 blocks when bit2 set; bit0 = voice started this pass)
+0x09  u8    shape       &0x7F position class: 0 x1364 (point -> 00361DE0),
                        1 x108 (003623C0), 2 x400 (multi-point -> 00362230),
                        3 x454 (constant arm — no transform call)
+0x0A  u8    volMax      127 x1835, else 40-100 — volume at zero distance
+0x0B  u8    volMin      attenuation floor: vol = (volMax-volMin)*(range-dist)/range
                        + volMin, then * per-variant pct / 100, clamp 0..127
+0x0C  u8[3] variantPct  per-weather-slot volume percent (100,100,100 in 2,315 of
                        2,326); indexed by WorldField_GetCurrentWeatherSlot1To3WithDebug-
                        Override()-1 (`00265920` = debugWeatherSlotOverride [settings
                        singleton 01F81428 +0xAAC] when positive, else saveImage
                        currentWeatherSlot [002EF2B0()+0x1060] +1 — named on
                        [weather-slot-state-model.md](../Weather/weather-slot-state-model.md));
                        0 = silent slot
+0x10  f32   range       attenuation distance cap in 00361810's volume math
+0x14  u32   count       class-2 point count (1 x2265; singles carry 1)
+0x18  u8    rtArg       runtime: 003638B0's r8 arg echoed
+0x19  u8    rtGen       runtime: generation byte vs the global counter — mismatch
                        releases the handle (002DF150) before restart
+0x1A  i8    rtOverride  runtime: >=0 returns it directly from 003638B0 (forced result)
+0x1C  f32   deadScalar  1.0 x2104, else 0.03-0.9 — DEAD authored data: zero +0x1C
                        accesses in the whole consumer family (0x362A..0x3642 +
                        00361810/00361DE0/00362230/003623C0/00363F30/00363FD0/
                        003638B0); shape and range fit a retired pitch/rate
                        multiplier
+0x20  f32   posX        world-space position (page's "record +0x20")
+0x24  f32   posY
+0x28  f32   posZ
+0x30  f32   dirX        direction vec2 — comiss-gated in the class-0/1 transforms
+0x34  f32   dirY        (00361DE0/003623C0) and read by 00362230's head
+0x38  f32   attenScalar attenuation arg to 00361810 (all classes)
+0x40  ...   points      class-2 only: count x {vec4 pos; vec4 aux} at 0x20 stride;
                        00363FD0 scores each, the winner's index goes to dword
                        [02D8F20] (mirrored to 02D9390) and its vec4 pair to
                        02D92A0/02D92B0
+0x54  f32   extentA     class-0/1 only
+0x58  f32   extentB     class-0/1 only
```

**Consumers.** `003635C0` is a bare installer: stores the block at `022CBAF0` and clears two
flags. `003631B0` is the per-frame walker: it iterates a u16 index list (**bit15 = end
marker**), each entry `&0x7FFF` selects `word[table + idx*2 + 2]` of the
`{u16 bound; u16 recordOff[]}` index, and computes `record = SP1 + off` (base read from
`022CBAF0`). Per record it applies the shape-class position transform, then calls
`003638B0(record, ...)`. `003638B0` bound-checks `dword[rec]` against **SPP1's** `+0x04`
count, fetches `u32[SPP1 + idx*4 + 0x20]` (the SE id), and starts the voice.

**The weather path corrects the page's earlier note.** `00363B40` reads the *SPP1* block
(`022CBAF8`), not SP1: SPP1's `word[+0x1A]` would name a `{u16 count; i16 idx[]}` override
list, but that word is **0 in every checked SPP1 list** (all 456 SP1-bearing maps), so the
function always falls through to
its second half — which reads a `{u32 count; i32 SPP1-index[]}` list at
`SP1 + [SP1+0x04]` (`= SP1 + 0x20`, the index-list region). The read is spelled
`rbx = movsxd(eax) + qword[022CBAF0]` where `eax = 0020E600(dword[SP1+0x04])` — i.e.
`low32(listBase + qword[01F83530])` added to the SP1 pointer. `01F83530` is the
**engine-wide offset-decode base** behind `0020E600`/`0020E620` (`arg ± base`,
~815/~279 callers — the universal authored-offset ↔ runtime-pointer pair, see
[the shared-neighbours pass](../../00-Engine-Core-Runtime/Shared-State-Accessors/the-shared-neighbours-pass-22-keeps-finding.md)
§4c and OPEN-QUESTIONS CD-2/UQ-83): it is zero-initialised `.data` that no instruction in
the image writes — the static route to a writer is exhausted (no rip-relative store, no
`lea`, no stored pointer, no absolute-addressing form), so the decode is zero-extension
for the process life and the `+0x04` field is an ordinary u32 byte offset. It is **not**
a per-list runtime cursor: the actual variant selection is
`ebp = 00265920() - 1` — the named `WorldField_GetCurrentWeatherSlot1To3WithDebugOverride`
(weather-slot-state-model.md §table: debug override at settings-singleton `+0xAAC` wins
when positive, else save-image `currentWeatherSlot` +1) — applied afterwards as an
index into the deduplicated SE-id gather
array at `022CBB58` (count at `022CBB70`). Each list entry is looked up in SPP1's
`u32[+0x20]` SE-id table. So the
"weather-index table at +0x04" belongs to SPP1's contract, and SP1's `+0x04`/`+0x20` region
is the single weather-variant index list the SP1-side fallback walks. `00363750`
(release path called before re-installs) iterates the same SPP1 `u32[+0x20]` table and
releases entries in the SE-id band `[1000, 2000)`.

**The `+0x08` record is a 16×16 listener grid** (closed 2026-09-21): `00362E50`
bounds-checks the listener position — `x ∈ [+0x08, +0x08 + u32[+0x10]·f32[+0x00])`,
`z ∈ [+0x0C, +0x0C + u32[+0x14]·f32[+0x04])` — then computes the cell indices by
divide-and-clamp and returns `SP1 + u16[+0x20 + 2·(idxX + idxZ·u32[+0x14])]`, or 0
when outside/empty. All 456 packs carry **exactly one** 0x220 record —
`{f32 cellW, cellH; f32 minX, minZ; u32 16, u32 16; u16 grid[256]}` — and every
cell's u16 is an SP1-relative offset into the `+0x20` region naming a
**bit15-terminated u16 emitter-index list** (0 bad offsets, 0 out-of-range entries
corpus-wide; 39,080/116,736 cells are 0 = empty; list lengths 1–17, one entry
dominant). So the `+0x20` region mixes two list types: the weather-variant
`{u32 count; i32 idx[]}` lists at its head, and one per-cell emitter list per
grid cell. The per-frame driver (`0x362ACE` body): mark every indexed emitter
(flag bit6), evaluate the grid, run `003631B0` over the cell's list (then over the
arena-head default list — which is a lone `{0x8000}`, selecting emitter 0),
dispatch the result via `002DF410(1, 0xB4, idx)` into `022CBA80`, clear flag bit3
on all. The "prefix list" question resolves: **the u16 lists ARE the emitter-set
encoding** — entries `&0x7FFF` index `word[emitIndex+2+i*2]` record offsets;
the arena-head list is just the whole-map default.

**Named residue**: none on the SP1 surface — `+0x1C` is dead authored data (zero
consumers), and the variant selector `00265920` is the already-named
`WorldField_GetCurrentWeatherSlot1To3WithDebugOverride` (weather-slot-state-model.md).

### 2.4 The `WD` section (slot 1) — container DECODED, dead authored data (2026-09-20, SWE2-DATA)

`WD` is a wave bank: a 0x20 header, an offset table, a 0x20-stride record table, and a
16-byte-block ADPCM stream. All 46 sections parse cleanly (`members/wd-census.tsv`,
`gen_wd_census.py` reproduces it from the VBF) — but **no consumer exists in TZA**: the
dispatcher frees slot 1 unread in both modes (below), no `.text` compare tests the `WD`
magic, and no loose `WD`-format file exists in the VBF or on disk. All 46 sections live
in the mode-0 `{0, 1, 10}` block packs (UQ-87) — the block's wave bank, authored on a
PS2-era layout and discarded by the PC runtime.

```struct WdHeader base=file
+0x00  char[2] magic        'WD' (u16 0x4457)
+0x02  u16    bankId      46 distinct values 0x1FA..0x251, one per pack — id/serial-like
+0x04  u32    dataSize    trailing blob = file[len-dataSize .. len); its start is 0x40-aligned
+0x08  u32    count       == +0x0C (duplicated in all 46)
+0x0C  u32    count2      duplicate of +0x08 in all 46
+0x10  u32    reserved10  0
+0x14  u32    flags       0 (29 packs), 0x8000 (11), 0x10000 (6)
+0x18  u32    reserved18  0
+0x1C  u32    reserved1C  0
```

The offset table (`count` u32s at `+0x20`) lists absolute record positions; the first is
`align16(0x20 + 4·count)` and the stride is 0x20 in all 46. Each record is two 0x10 halves
at `off_i` / `off_i+0x10`:

```struct WdRecord base=off_i
+0x00  u32   reserved00  0
+0x04  u32   X       blob-relative stream start — non-decreasing across a file's records (46/46)
+0x08  u32   Y       blob-relative loop point: `Y >= X` → loop start inside `[X, nextX)` (203/225 — 177 at `Y == X` = loop the whole stream, 26 strictly inside); `Y < X` → non-looping one-shot (22/225, Y is a stale small value)
+0x0C  u32   const0C   0x5FE800FF — constant in all 225
+0x10  u32   hash    per-entry id — shared by some records (e.g. both dst0100 head records)
+0x14  u32   const14   0x407F7F3C — constant in all 225
+0x18  u32   reserved18  0
+0x1C  u32   reserved1C  0
```

Every X and Y is `< dataSize` (225/225) — both are positions inside the trailing blob,
which is a PS2-style 16-byte-block ADPCM stream (per-block `{predictor/shift, flag}`
headers; flag byte `0x02` dominant, `0x00`/`0x04` seen). **X/Y roles resolved
2026-09-22 by corpus geometry** (the record table is dead — no consumer — so this is
a distributional reading, not a body read): every `Y ≥ X` lands strictly inside its
own stream `[X, nextX)` (0 violations in 225), which is exactly a PS2 VAG-style
loop-point contract — 177 loop from the stream start (ambient beds), 26 loop from an
interior point (intro + loop tail), and the 22 `Y < X` records are non-looping
one-shots whose Y is stale authoring residue. Nine packs share
identical leading stream content (`alc2000`/`asp0100`/`byu1000`/`byu2000`/`nac2000`/
`rbn2000`/`slm0100`/`var1000`/`var2000` all begin with the same block) — the blob is a
shared bank referenced per-map.

In 27/46 packs `dataStart` (`fileSize − dataSize`) lands inside the record table — the
last record pair(s) physically occupy bytes the size field counts. The record table is
located purely by the absolute offsets, and the stream follows the last record half; the
table and the blob were laid down independently, so the overlap is real authored layout,
not corruption.

**Why it is dead data.** `00378BC0` frees `slot[1]` in both modes with a bare arena free —
mode 1: `call 003697F0` on `[rsp+0x28]` at `00378DBB`; mode 0: stores the pointer to
`02ADD070` (`00378DFB`) then frees it (`00378E07`) — and `02ADD070` has zero readers (two
rip-relative stores, no loads; `003697F0` is the shared arena free — 254 call sites).
A `.text` scan finds no `0x4457` magic compare, the VBF
contains no non-`.mpk` file starting `WD`, and no `.wd` file exists on disk. Unlike
`EFB0` (slot 13, discarded for a loose `.efb`), `WD` has no replacement at all: the
embedded wave bank is simply never played in TZA.

### 2.5 The `MRP` section (slot 15) — container DECODED, dead authored data (2026-09-21, SWE2-DATA)

Slot 15 exists in exactly **2 packs** — `rwg0201` and `rwg0202` — and the two payloads are
**byte-identical** (168,640 B each): one shared block, not per-map data. It is an instance of
the documented [`MRP` relocated-pointer
container](../../02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/mrp-menu-resource-packages.md)
(the `mrp_menu/*.mrp` family — `+0x03` is the relocation flag, not a terminator), parsed as:

```struct MrpHeader_rwg0201 base=file   instance parse; conforms to the canonical MrpHeader directory layout in mrp-menu-resource-packages.md
+0x00  char[3]  magic         'MRP'
+0x03  u8       relocated     = 0 on disk (the '\0' of the shipped magic; set to 1 by 002A00F0)
+0x04  u32      tailCount     = 2
+0x08  u32      tailOff       = 0x470
+0x0C  u32      spareCount0   = 0
+0x10  u32      spareOff0     = 0x490
+0x14  u32      spareCount1   = 0
+0x18  u32      spareOff1     = 0x490   (empty tables park at 0x490, not EOF)
+0x1C  u32      descCount     = 5
+0x20  u32      descOff       = 0x30
+0x24  u32      tableBCount   = 2
+0x28  u32      tableBOff     = 0x490   (POPULATED — 0 in all 116 menu files)
+0x2C  u32      unk2C         = 0
```

- **5 descriptors** (`0x14` stride) at `+0x30`, conforming to the documented
  `{u8 index; u8 sub; u8 0; u8 tag; u16 u,v,w,h; u32 aux; u32 ref}` shape — `ref` is
  row-relative into the tagged item payloads that occupy `0x94..0x470` (the `0x80`-fill
  `{index<<16 | code}` records; the same typed-list encoding the menu files carry).
- **Tail table** at `0x470`: 2 × `char[16]` names — `"template"`, `"temlate02"`.
- **Table B** at `0x490`: 2 × `{u32 flag=1; u32 length; u32 relOff}` — `+8` is relative to the
  table-B base, per the relocator's `002A0147 ADD`. The two entries cover the file contiguously:
  `[0] → 0x4B0, len 0x8430` = `{char[16] "template"; TIM2 image}`; `[1] → 0x88E0, len 0x209B0` =
  `{char[16] "temlate02"; TIM2 image}` — `0x88E0 + 0x209B0 == 0x292C0 == fileSize` exactly. Both
  are named `TIM2` textures: the map-gauge's map images. This is the **only populated table B in
  the MRP corpus** — all 116 menu files ship it empty.
- The payload is a map-gauge/minimap package: two textures plus the rect list that tiles them.

**Why it is dead data.** The pointer lifecycle is fully closed — `02ADD058` has exactly four
rip-relative references, none of which dereferences the buffer:

| site | access | role |
|---|---|---|
| `00378F04` | store | dispatcher keeps the slot pointer; also sets flag bit `0x12` at `02ADD0F0` |
| `00377B90` | load | the getter — only caller is `initgauge` (`0034DC70`, verb `0x01AB`) |
| `003782EB` / `003782FC` | load / clear | teardown — frees via `003697F0`, zeroes the cell |

`initgauge` → `003E9020` → `00408300(kind, mrp)`; `00408300`'s full body (`00408300`–`0040835C`)
`movsxd`s both args into the create message at `+0x08`/`+0x10` — **the pointer is truncated to its
low 32 bits and never dereferenced**. The gauge task `00406E80` was then read in full: message
kinds 1 (create), 2, `0x11` (teardown). The create branch reads `msg+0x08` (the gauge kind) and
builds the task context from a `0051EDC0` variant object (`rbx+0xD0`), an SP1 emitter cursor
(`0020E600`), a `+0xD8` pointer array (`byte[src+0x24]` entries, `0024A440` refcounted), a
`00244F50` window (`rbx+0xC0`) and a `00244960` registration — **`msg+0x10` is never read in any
branch**. The relocator `002A00F0` never runs on this buffer (nothing requests it through
`00249320`; the dispatcher stores the raw pointer), so even the `MRP`+flag byte's meaning is
latent here. A `.text` scan finds **zero** `4D 52 50` bytes — consistent with the family rule
that `+3` is a flag, but here also proving no alternate consumer probes the magic. No map-side
loose `.mrp` exists (all 116 are `mrp_menu/` UI files; none on disk). The gauge's live content
comes from the TIM2 map pictures (slots 24–27) and the `0051EDC0` window variants — the embedded
gauge package, like `WD`, is a PS2-era layout retained but unplayed.

**Residue:** none slot-15-specific. The typed-list item-type vocabulary that these payloads use is
now closed corpus-wide under UQ-76 (type 6 = a blanked text slot, type 3 never authored — see the
typed-list doc's census note).

## 3. The loader contract

### 3.1 Two requests per field

`00331990(field)` requests two packs through `00378A60`:

```c
00378A60(field, MapRef_GetAuxValue0(field), /*mode*/0);    // 003319A4: the row's block word +0
00378A60(field, MapRef_GetPrimaryFieldValue(field), 1);    // 003319BF: the row's own word +0
```

Both indices are namespace-4 (`map_ctrl`) resource indices. `00378030` (from `00378B41`) sizes the
file with `0032E400(4, index)`, allocates an arena block tagged `MapN` (`00D11120`), and submits a load
whose completion is **`00378BC0`** (`003780B1`) with the argument `block | mode` — the mode in the low
two bits. It also stores `MapRef_GetAuxValue1(field) + 500` at `02ADD078` (`003780EB`–`003780FA`).
Before the pack, `00377DC0` requests the loose `PS2Data\efb\<map>.efb` built from the same path
(`00377E8A`–`00377EEE`), with completion `003788F0` → `02ADD050` in mode 1 and `003789A0` → `02ADD098`
in mode 0. The debug verb `mapload` (`0x2001`, `0050D4D0`) requests a single pack in mode 1.

Only the mode-1 request names the scene: `00378A60` calls `00379A10(4, index)` — the map-name setter —
only when the mode is nonzero (`00378B46`–`00378B51`).

### 3.2 The split — `0036B980`

The completion calls `0036B970(block, slots, 32)` → `0036B980`, which carves the one loaded block into
32 arena blocks in place:

| Field | Read by | Rejected if | Clamped to | Inert |
|---|---|---|---|---|
| `+0x00` count | `0036B99E` | **count > 32 → returns 0, nothing split** (`0036B9BB`) | — | — |
| `+0x04` sizes | `0036BA30`–`0036BA45` | **`roundup((count+1)·4, 0x40) + Σ(size ? size + 0x40 : 0)` ≠ the arena block's size → returns 0**; also 0 when the arena has fewer free handle slots than extra sections (`0036BA78`–`0036BAA2`) | — | — |
| the 0x40 slots | `0036BB35`–`0036BBDC` | — | — | **yes — overwritten with a copied arena block header** (owner bytes `+2/+3/+0x14–0x17/+0x1E`, size `+0x18`, encoded tag `+0x30`) |
| payloads | the consumers below | — | — | — |

The header's own block keeps the header; each payload becomes an independently freeable block, so
the dispatcher can free a slot it does not want without touching the others. **A zero size yields a
null slot**, which the dispatcher tests before storing or marking it.

### 3.3 The dispatch — `00378BC0`

```c
if (!split(block, slot, 32)) return;                             // 00378BF3
for (i = 0; i < 4; i++) {                                        // 00378C40..00378CA2
    pictures[i]   = slot[24 + i];   if (slot[24+i]) mark(bit 9 + i);    // 02ADD010 + 8i
    placements[i] = slot[28 + i];   if (slot[28+i]) mark(bit 13 + i);   // 02ADD030 + 8i
}
if (mode != 0) {                                                 // 00378CA4
    nav        = copy(slot[4]) tagged "IdMa", free(slot[4]);     // 02ADCFE8, 00378CCD..00378D4C
    world1 = slot[8];      if (slot[8]) mark(bit 3);             // 02ADCFE0
    free(slot[10]); free(slot[0]); free(slot[1]);                // 00378D74..00378DBA
} else {
    world0 = slot[8];      if (slot[8]) mark(bit 3);             // 02ADCFF0
    free(slot[1]);                                               // 00378DF6..00378E19
    sppMap = slot[10]; seBank = slot[0]; if (slot[10]) mark(bit 0);   // 02ADD068, 02ADD080
}
free(slot[13]); free(slot[12]);                                  // 00378E57..00378E83
spBlock = slot[16]; if (...) mark(bit 7);                        // 02ADD060
lights  = slot[17]; if (...) mark(bit 8);                        // 02ADD090
actors  = slot[9];  if (...) mark(bit 4);                        // 02ADD0B8
gauge   = slot[15]; if (...) mark(bit 18);                       // 02ADD058
clear pending bits 0..18; if nothing else is pending: 003775D0(); // 00378F20..00378F39
```

`mark(bit)` sets the bit in both `02ADD0EC` (pending) and `02ADD0F0` (to bind). **Slot 4 is neither
stored nor freed in mode 0**, and slots 2, 3, 5–7, 11, 14 and 18–23 are never read — a section placed
there would stay allocated with no owner. No shipped pack uses any of them (census).

**Slot 13 is discarded.** All 387 embedded `EFB0` sections differ from the loose `.efb` of the same
name (same `EFB0002` signature; the loose file is larger in 174 and not larger in 213), and the loose
file is what `00377DC0` loads.

### 3.4 Binding — `003775D0` and `00378120`

`003775D0` consumes the bind bits: bit 7 → `003635C0(spBlock)` stores it for the sound system at
`022CBAF0`; bit 0 → `003635E0(sppMap, seBank, [02ADD078])` walks the `SeSep` bank (`002DF070`), frees
it, and keeps the `SPP1` map at `022CBAF8`; bit 4 → `003E8940(actors)` publishes the list at `02B5D080`
when its `u16 +4` is 1; bit 8 → `0037AA90(lights, 0)` and `003DE920`; bit 3 → `00378120`, which makes
the mode-1 `YM00` current (`02ADCFF8`), hands the mode-0 one to `0026E7D0` (which stores its object at
`0209A668`) and the mode-1 one to `0026E760` (both through `003EC9A0`, `003EC8D0` and `002F6AB0`; a
non-null `0209A670` is what the camera hit check's `0026E500` tests before probing), binds the navigation copy
(`02ADD008` → `Navigation_BindAndRebaseDataset`, `003781A6`), uploads picture 0 (`003C63A0`) and
applies placement 0 (`00379870`). Teardown is `00378230` (all slots) and `003784A0` (sound and the
second `YM00`).

**The write path.** None; authored offline.

### 3.5 `002F6AB0` — the `YM00` object's chunk-tag dispatch (SWE2-FRONTIER, switch-families package)

`002F6AB0` (2118 B) is the constructor `0026E760`/`0026E7D0` call after allocating the 0x240-byte
`YM00` presentation object. Its head writes an identity matrix (`00203170`), zeroes
`+0x150`–`+0x230`, installs four method callbacks `002F5450` / `002F4520` / `002F5550` /
`002F5540` at `+0x128`–`+0x140`, stores the caller's section index at `+0x168`, and obtains the
chunk container through `003EC970` — a kind-indexed (≤7) table of 0x38-byte records at
`02EBB820` (`+0x158` = base, `+0x160` = `base+0x14`).

The container is a **tagged-chunk index**: `[rbx]` = entry count, then `count+1` dwords at
`rbx+4`; each dword is `tag:8 | offset:24` with the payload at `rbx + offset·0x10` and the next
entry's offset as the end (`002F6C90`–`002F6CD7`). The tag byte dispatches a 34-case RVA jump
table at `002F72F8` (site `002F6CCC`, bound `0x21`):

| tag | arm | role (all verified against the body) |
|---|---|---|
| 0 | `002F6CD9` | `[+0x16C]` = payload dword; `[+0x188]` = `payload+0x10` ptr (`r14+0x10`) — the `0x40`-stride vector table read at `002F70CB` |
| 1 | `002F6CFE` | `[+0x170]` = count; `[+0x190]` = payload; if nonzero, `[+0x1C8]` = `003EC8D0`-alloc `count·4` |
| 9 | `002F6D9D` | `003ED3F0(r14)` — resets three `0x180`-stride records at `02B5ED94`–`02B5F214` (quad heads `1.0f`), then works from the chunk pointer `0209A660` |
| 11 | `002F6DE9` | `0026E8C0` stores the chunk to `0209A660`; `[r14]` is a **packed RGBA dword** stored to `022D8ED8` (`0xFFFFFFFF` keeps the previous value; `0036D400` unpacks it ÷`255.0` → `00182280` on the command-record path); `[r14+4]` unpacks as RGBA via `00466140` × `1/128` (`008C5B34` = `0x3C000000`, `mulss xmm6` at `002F6E34`/`002F6E38`/`002F6E4F`) into float globals `0209A3A0`/`0209A3A4`/`0209A3A8` (`0209A3AC` forced `1.0f`); `[r14+8]`/`[r14+0xC]` stored to `0209A6EC`/`0209A6F0` — the environment/ambient-light chunk |
| 12 | `002F6E7C` | `00468160(r14, [+0x150], [+0x1B8])` — binds this chunk against the tag-14 buffer and the tag-32 payload (`not read`) |
| 14 | `002F6E97` | `003EC910(6, 0x20, init=00467D00)` → bank-locked `0x20` alloc + init callback; `00467D20` copies the chunk in; `[+0x150]` = buffer; `00467BF0(buf, 0)` registers it under `02EBB6A0` via `005360C0` |
| 17 | `002F6DC8` | `00232380(+0xA8, r14)` — nested chunk parse into the second `0x68` sub-record |
| 22 | `002F6D91` | `[+0x180]` = chunk ptr — the chunk is a `{u32 count; (count+1)×{u24 off16 \| u8 tag=0}}` index (sentinel `0xFF`, `sentinelOff·16 == size`, 461/461; 5,714 zero-length entry aliases) over `{vec4 AABBmin, vec4 AABBmax, vec4(128×4), u32 axisMode, u32 period, tail}` records — **the per-instance oscillation spec**; only `+0x30`/`+0x34` are consumed (`002F4520` via tag-30 `+0x00`, §2.2), the AABB header and `+0x38` tail are a dead PS2 VIF/GIF packet blob |
| 23 | `002F6DDC` | `00466E70(r14)` — builds the `02EBB6E0` `0x50`-stride slot family: `[02EBB6E0]` = `dword[chunk+0x10]` bound, `[02EBB6E4]` = `-1` cursor, `[02EBB6F0]` = `003EC8D0`-alloc `count·0x50` table, `[02EBB6F8]` = chunk stash — the same family `ACTL`'s `+0x02` timer-slot ids index and the tag-30 cross-link pass walks via `00466CB0` |
| 24 | `002F6D33` | `[+0x220]` = count; `[+0x198]` = payload; `[+0x1D0]` = alloc `count·0xE0` — **the per-instance presentation-entry array** (the periodic tick's post-recovery mark writes `+0xC0` of entry `[+8]`) |
| 25 | `002F6DAA` | `003ED190(r14)` — field-aware environment setup: reads field id `003148F0`, special-cases `0x11A`, stores the chunk to `02EBB6xx` globals and sets a flag |
| 26 | `002F6ED1` | same alloc+init+copy as tag 14 (`00467D00`, `00467D20`, `00467BF0`) plus `[+0x230]` = 1 — the "resource present" flag; the chunk is a **named-TIM2 bank** — `{u32 count; (count+1)×{u24 off16 \| u8 0xFF}}` index (sentinel = EOF exactly, 459/459 packs) over `{char[0x28] name; u32 picCount; u32 0; TIM2}` records (20,809 censused — `members/ym00-tag2226-census.tsv`); `00467D20` sums each TIM2's `u16[+6]` picCount, allocs `Σ × 0x60` at `qword[buf+8]`, and expands each picture (`00536080` walks the TIM2's own header — `+0x05` flag picks `+0x10`/`+0x80` start, `u16[+6]` the count, pictures u32-length-prefixed) |
| 27 | `002F6EFF` | `003ED840(r14)` — publishes the chunk to `02B5F1A0` and the *next* chunk to `02B5F1B0` (a "current/next" cursor pair) |
| 28 | `002F6F09` | `[+0x1A8]` = chunk ptr |
| 29 | `002F6CF2` | `[+0x1B0]` = chunk ptr — `0x10`-stride records; `002F4520` (b30 records) reads `word[rec+idx·0x10 + 2]` as a selector into the tag-33 `0xC` array |
| 30 | `002F6D73` | `[+0x174]` = count; `001806F0(count)` writes it to the singleton `[001A9930()+0x20]`; `[+0x178]` = payload — the `0x30`-stride instance source records |
| 31 | `002F6DB7` | `00232380(+0x40, r14)` — nested chunk parse into the first `0x68` sub-record |
| 32 | `002F6F12` | `[+0x1B8]` = chunk ptr |
| 33 | `002F6D63` | `002F6740(rsi, r14)` — `[+0x22C]` = count, `[+0x1A0]` = payload, `[+0x1D8]` = alloc `count·12` default-initialized `{1, 1.0f}`; `002F4520` reads `entry·0xC+8` as an f32 threshold (selected via tag-29 under b30) |
| 2–8, 10, 13, 15, 16, 18–21 | `002F6F19` | skipped (loop tail) — the tags exist in the index but this parser does not consume them |

`00232380` (240 B) is itself a six-tag chunk parser over the same `{tag:8|offset:24}` index
(inner table `00232470`): tag 0 → `[+0x00]` + rectangle math into `+0x30`–`+0x40`; tags 1–5 →
ptr fields `+0x20`/`+0x28`/`+0x10`/`+0x18`(+count `+0x44`)/`+0x08`; tail zeroes `+0x48`–`+0x60`.
The two `0x68` sub-records are nested containers inside the `YM00` chunk stream.

After the chunk walk (`002F6F2A`+): if `[+0x158]` is live and `[+0x174]` > 0 the body allocs
`count·0x70` (`003EC8D0`) into `[+0x1C0]`, walks the tag-30 records (`rdi`, `0x30` stride) —
filling each `0x70` entry with four `1.0f` quads, bucket-counting flag bit 14 into
`+0x1F4`/`+0x1FC`/`+0x204`, honoring the bit-30 post-recovery mark by writing `-1` into the
unit's `0xE0` presentation entry `+0xC0` (`002F701D`–`002F7037` — the periodic-tick contract),
and sourcing the color either from the record's own RGBA `[+0xC]` (`00466140` × `1/128`, the
same `xmm6` = `008C5B34` scale at `002F7076`/`002F707A`/`002F709C`/`002F70A0`) or,
when zero, from the tag-0 table entry `[rdi-0xA]·0x40` transformed through the `+0x40`
sub-record's matrix (`00231A90`).

### 3.6 The `002F6AB0` exclusive subtree — the 23 bodies the constructor calls (SWE2-FRONTIER, exclusive-subtrees package)

The exclusive-callee census assigns 23 frontier functions to `002F6AB0` — exactly the helpers
§3.5's tag arms invoke. All signature-swept 2026-09-15 (`bshape.py`):

| cluster | members | role |
|---|---|---|
| the §3.5 tag handlers | `003ED190` (597 B — tag 25, `003148F0` field id + `00D11C10`/`0209A660`), `003ED3F0` (952 B — tag 9, `02B5ED94` reset + `00D11C10`), `003ED840` (45 B — tag 27 cursor publish), `00232380` (240 B — tags 17/31, the `0x68` sub-record parser), `002F6740` (124 B — tag 33, `003EC8D0`), `003EC910` (95 B — tag 14/26's bank-locked alloc, `00D11BF0`), `003EC970` (36 B — the `02EBB820` kind table), `0026E8C0` (8 B — tag 11's chunk store) | already read in §3.5 — the census confirms they have no other caller |
| the `02EBB6xx` object family | `00466E70` (1,453 B — tag 23, `003EC8D0` ×3 + `004677A0`/`00467420`/`004668C0`, `00D12510` + `02EBB6E0`/`E4`/`F0`; interior verified 2026-09-17, SWE2-FRONTIER — the three `003EC8D0` calls sit at [`00466ECA`](../../_index/ADDRESS-INDEX.md)/`00466FF8`/`00467013`, the leaf calls after), `00467420` (503 B — `00203170` identity + `02EBB6E0`/`F0`), `004677A0` (317 B — `00466420` ×2), `00467BF0` (181 B — `005360C0` + `02EBB6A0` register), `00467D20` (817 B — `0020E620` ×6 + `003EC8A0`/`003EC8D0`/`00536080`/`003A1FE0`, `00D12520`), `00468160` (945 B — tag 12's bind: `003EC8D0` ×2 + `0020E600` ×2 + `003CCB60` ×2 + `0020E620`/`00536080`/`00536060`/`003CCC20`/`001801A0`, `02CA6010`/`18`/`20`/`24`) | the tag-12/14/23/26 payload objects — `02EBB6A0`–`02EBB6F0` is their register block |
| resource helpers | `001801A0` (168 B — `001A9930` ×2 + `001A4DB0`), `001806F0` (tag 30's count write), `001837C0` (573 B — `0017E8E0`, `008C5B34`/`008C5B40` consts), `001A40B0` (408 B — `[r9+0x18]`/`[rax+0x10]` callback pair), `001A4DB0` (545 B — `0017FEA0` ×2 + `001A37C0`/`001837C0`/`00183EE0`/`00184140`/`001A40B0`) | the resource-manager resolve chain feeding the chunk arms |
| leaves | `00231F50`, `00466420`, `00536060`, `005360C0` (`003EC8D0`/`00861EBA`) | small bodies |

Every tag arm §3.5 lists resolves to a member of this tree — the constructor's world is fully
inside the census. Not established: which `00D12510`/`00D12520` table row each `0046xxxx`
object registers under.

**Census edge cases (AUDITSEM-CONTRA-FRONTIER-2F6AB0):** the census drops callees whose only
callers are themselves members. `001F1590` (99 B, no ownership tag at all) is called only by
`003ED190` ×2 and `003ED3F0` — exclusive but unlisted above. `00536080` (`FinalNoPrimaryOwner`,
called only by `00467D20`/`00468160`) is the borderline case: ownerless but not frontier, so the
census's frontier-only rule excludes it; `004668C0` is Presentation-owned and stays out
legitimately.

## 4. Key addresses

| Address | Role | Read? |
|---|---|---|
| `00331990` | field load: the two pack requests | ✅ full body |
| `00378A60` | per-mode request, teardown and the mode-1 map-name call | ✅ full body |
| `00378030` | sizes, allocates `MapN`, submits with completion `00378BC0` | ✅ full body |
| `00377DC0` | requests the loose `.efb` for the same map | ◐ path build and both arms |
| `0036B980` | splits one arena block into `count` blocks | ✅ full body |
| `00378BC0` | the slot dispatch | ✅ full body |
| `003775D0` | binds sound, `ACTL`, lights and `YM00` | ✅ full body |
| `00378120` | `YM00`, navigation, picture 0, placement 0 | ✅ full body |
| `003635E0` | `SeSep` bank walk and `SPP1` store | ✅ full body |
| `003635C0` | `SP1` store | ✅ full body |
| `003E8940` | `ACTL` publish | ✅ full body |
| `0026E760`, `0026E7D0` | `YM00` object builders | ◐ calls only |
| `00377B90` | `MRP` getter used by `initgauge` (`0034DC70`) | ✅ full body |
| `00408300` / `00406E80` | the gauge task's creation and handler — the `MRP` pointer's only destination | ◐ creation, and the handler's create branch |
| `00378230`, `003784A0` | teardown | ◐ |

### Data addresses

| Address | Name | Kind | Contents |
|---|---|---|---|
| `02ADD010` | map pictures | `.data`, 4 × ptr | slots 24–27 |
| `02ADD030` | picture placements | `.data`, 4 × ptr | slots 28–31, read by `00379870` |
| `02ADCFE0` / `02ADCFF0` | `YM00` (mode 1 / mode 0) | `.data` ptr | slot 8 |
| `02ADCFE8` | navigation copy | `.data` ptr | slot 4, mode 1 |
| `02ADD058` | gauge resource | `.data` ptr | slot 15 |
| `02ADD060` | `SP1` block | `.data` ptr | slot 16 |
| `02ADD068` / `02ADD080` | `SPP1` map / `SeSep` bank | `.data` ptr | slots 10 / 0, mode 0 |
| `02ADD078` | sound map number | `.data` u32 | `MapRef_GetAuxValue1 + 500` |
| `02ADD090` | light set | `.data` ptr | slot 17 |
| `02ADD0B8` | actor list | `.data` ptr | slot 9 |
| `02ADD0EC` / `02ADD0F0` | pending / to-bind bits | `.data` u32 | bit per slot family |
| `00D11120` | `"MapN"` | `.rdata` | the pack's arena tag |

## 5. Corpus survey

The commonest slot sets are `{0, 4, 8, 10, 13, 16, 24, 28}` (113 packs), then the same plus `9`, plus
`9, 17`, plus `9, 17, 25, 29`; **46 packs carry only `{0, 1, 10}`** — sound, wave data and the
positional map, with no world data, navigation or pictures — and 41 carry only `{0, 10}`. Slot 15
(`MRP`) appears in two packs. Every one of the 46 `WD` sections is in a `{0, 1, 10}` pack.

## 6. Falsification pass

Not yet run.

## 7. What this document does not claim

- [x] ~~**UQ-86.** Which packs the engine requests in mode 0 and which in mode 1 for each field — the map-reference
      table that supplies both indices was not decoded here. `MP-1`.~~
      ***ANSWERED 2026-09-17 (FABLE): the map-reference table is `map_ref.bin`, and it names both packs for every field.** `MapRef_BeginLoadResource` `00268750` requests kind 9 id 4 (`0026875A`..`00268762`, the `MRF` file [the five-small-bin page](../../02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/five-small-bin-tables.md) lists) and keeps it at `02099D88`. Its header's words `+4` and `+8` are the offsets of two arrays: 1,315 field rows of 8 bytes `{u16 own pack index, i16 block index, i16, i16}` and 93 block records of 16 bytes `{i16 mode-0 pack index, i16 aux1, ...}`; `MapRef_GetPrimaryFieldValue` `00264F10` returns the row's first word and `MapRef_GetAuxValue0` `00264F40` the first word of the row's block record (`00264F69`..`00264F79`), so the mode-1 request loads the field's own pack and the mode-0 request loads its block's pack. Joining the namespace-4 indices to the archive's 550 `.mpk` entries through `FileSizeTable_US.fst` row 4 (516 of 550 sizes are unique) resolves 457 own packs and 89 block packs; the two index sets never overlap, no row's own pack is its block's, and together they use every kind-4 index. The per-field listing, both packs with their slot sets, is [`members/map-ref-field-packs.tsv`](members/map-ref-field-packs.tsv). DATA from the archive; the reader chain static.*
- [x] ~~**MP-2.** The inner layouts of `YM00`, `ACTL`, `SP1`, `WD` and `MRP`, and
      what the navigation section at slot 4 holds beyond its binder. `MP-2`.~~
      ***ANSWERED 2026-09-22 (SWE2-DATA): all five sections decoded end-to-end
      (§2.1–§2.5); slot 4 is covered by the navigation decode.** `WD`'s X/Y
      blob positions are an explicit unresolvable exception — the section is
      proven dead (freed unread in both modes), so no consumer exists to give
      the pair a role. History:* *Narrowed 2026-09-13:* `SPP1` is
      decoded in [the map sound list](../../18-Audio/Sound-Bank-And-Voice-Formats/spp-map-sound-list.md); `SP1` is
      known there to carry the emitter records (`003631B0` → `003638B0`, position at record `+0x20`) and a
      weather-index table at `+0x04`. *Narrowed 2026-09-20 (SWE2-DATA):* **`ACTL` is decoded — §2.1**;
      the container contract is proven end-to-end (270/270 packs, zero remainder). *Narrowed 2026-09-20
      (SWE2-DATA):* **`YM00`'s container is decoded — §2.2**: a fixed 17-slot tagged-chunk schema
      identical in all 461 packs, the `{u24 off | u8 tag}` index in 16-byte units from `+0x10`,
      the `0xFF` end sentinel, and the full tag→handler-arm map. *Narrowed 2026-09-20
      (SWE2-DATA):* **`SP1` is decoded — §2.3**: header + three region offsets, the
      `{u16 bound; u16 recordOff[]}` emitter index, the variable-size emitter record
      (2,326 censused), and the corrected SP1↔SPP1 global split. *Narrowed 2026-09-20
      (SWE2-DATA):* **`ACTL`'s record semantics are decoded — §2.1**: `+0x02` timer-slot id,
      `+0x08` target spec (member id / aux-row), `+0x0E` 64-slot flag index, `+0x10`
      object id, `+0x12` `{phase|kind}`, the `+0x13`/`+0x14` arg nibbles, the aux table's
      `{u16 count; u16 memberIds[]}` rows, the `02EBF420` group-table member resolution,
      and the `003E8020` state machine over the activate/clear/alternate/init/query/
      snapshot handlers. *Narrowed 2026-09-20 (SWE2-DATA):* **`YM00` per-chunk semantics
      started — §2.2**: tag 11's environment record (0x20 live bytes, `+0x10` vector via
      `0209A660` lazy readers), tag 0's `{count; count×0x40}` vec-table row (three
      vec3+0 + position vec4), exact strides for tags 24/30/33/1, every arm's store
      target, and `003E8AA0`'s mode = the `+0x15` group tag. Tag 30's record shape is
      also censused — a u16-field row (764,018 records; `+0x00` tag-22 index, `+0x02` id,
      `+0x06` `0xFFFF`, `+0x0C`/`+0x0E` flag words, `+0x14` selector, `+0x16` `0x6014`,
      `+0x1C` `0x00FF`, `+0x20` index; `+0x10`/`+0x1E`/`+0x22`+ dead) — its consumers
      remain. *Narrowed 2026-09-20 (SWE2-DATA):* **`WD` is decoded — §2.4**: the wave-bank
      container (header, offset table, A/B record pairs, blob-relative X/Y positions,
      16-byte-block ADPCM) is proven over all 46 sections, and the section is shown to be
      dead authored data — freed unread in both modes, no magic check, no loose
      replacement. *Narrowed 2026-09-21 (SWE2-DATA):* **`MRP` is decoded — §2.5**:
      the slot is a standard `MRP` container (the `mrp_menu` family's layout —
      5 rect descriptors, a 2-name tail, and the corpus-unique populated table B
      holding two `{name; TIM2}` gauge textures), byte-identical across its 2 packs
      (`rwg0201`/`rwg0202`), and dead — `02ADD058` has exactly four rip refs (store,
      teardown load/clear, getter), `00408300` truncates the pointer to 32 bits into
      a create param `00406E80` never reads in any branch, and no `.text` compare or
      loose replacement exists. *Narrowed 2026-09-21 (SWE2-DATA):* **tags 22/26
      layouts decoded — §3.5**: both are nested `{u32 count; (count+1)×{u24 off16 |
      u8 tag}}` indexes; tag 26's records are `{char[0x28] name; u32 picCount;
      u32 0; TIM2}` (20,809 censused, sentinel = EOF exactly) and `00467D20`
      expands each picture into the `0x60`-stride runtime entries `002F7380`
      reads — the authored texture bank the tag-30 instances select from.
      *Narrowed 2026-09-21 (SWE2-DATA):* **tag-22's consumer and record
      semantics decoded — §2.2**: method callback `002F4520` (`ctx+0x130`) is
      the sole `ctx+0x180` reader; tag-30 `+0x00` is a deduplicated tag-22
      index (correcting the "sequential ordinal" note — `< n22` in all
      764,018 records), resolving `{AABBmin, AABBmax, 128×4, axisMask,
      period, tail}` records (348,239; mode 0 = static 97.2%) — a
      per-instance oscillation/mover spec applying `phase mod period` to
      runtime `+0x1FC`/`+0x200` via `001E5540`. *Narrowed further (SWE2-DATA):*
      **tag-22's `+0x38` tail is closed as dead authored data** — the sole
      `ctx+0x180` reader dereferences only `+0x30`/`+0x34`, and the tail
      (0x78–0x7E340 B; `u32 ∈ odd<32` + `04 04 00 01 01 80 NN 6c` prefix +
      `0a c0 NN 6e` UNPACK runs of packed `7f7f7f80`-style quads) is a retired
      PS2 VIF/GIF vertex-packet stream — same residue class as WD slot 1 and
      MRP slot 15. *Narrowed further (SWE2-DATA):* **tag-0's row semantics are
      closed** — §1's tag table: the three vec3s are the node's scaled basis
      axes (60% orthonormal, 26% uniform-scale, 14% anisotropic-scale, 0.2%
      sheared of 390,136 rows) and `+0x30` the origin; `002F5550` composes the
      full matrix (`RotY(θ)·tag0` unparented, `tag0⁻¹·parent·tag0` parented —
      the row is the joint frame), `002F70CB`/`002F67C0` read only the origin.
      *Narrowed further (SWE2-DATA):* **ACTL `+0x04`/`+0x06`/`+0x0A`/`+0x0C`
      closed dead-authored** (all `0xFFFF` ×1,822 and every same-offset access
      in the `003E7Exx`–`003E8Exx` family is a header or bucket-index read;
      all six `003E8230` callers are in-family), **`+0x15`'s writer provenance
      named** (the verbs copy `byte[owner+0x15]` where `owner` resolves via
      `002621D0`/`00358940` from the command state — the owner byte's writers
      are the VM spawn family, a script-VM question), the **`obj+0x13`
      taxonomy verified complete** (bit0 suspend `|1`/`&0xFE`, bit1 charging
      `|2`/`&0xFD`, bit2 re-arm `|4`/`&0xFB` — the three `0037xxxx` pairs, no
      other `+0x13` access exists), and tag-11 `+0x00` confirmed closed (the
      RGBA override quad is the whole field). The residue
      is `WD`'s X/Y pair roles
      (unresolvable — no consumer). The navigation dataset (slot 4) is covered by
      [its own decode](../../06-Movement-And-Navigation/how-a-unit-finds-its-way-across-the-navigation-mesh.md).
- [x] ~~**UQ-87.** Why packs with only sound sections exist (46 `{0, 1, 10}`, 41 `{0, 10}`) and whether they are the
      mode-0 packs. `MP-1`.~~
      ***ANSWERED 2026-09-17 (FABLE): they are the mode-0 packs, one per block.** Of the 93 block records in `map_ref.bin` (UQ-86), 89 resolve to a pack by size and all 89 are the sound-only packs: 46 with slots `{0, 1, 10}`, 41 with `{0, 10}` and 2 with no slots at all; the 4 unresolved share their size with another pack. No field's own pack is sound-only (457 resolved, every one a full pack). So a block, the area a set of fields shares, carries its sound bank, wave data and map sound list in a pack of its own, requested once in mode 0 when the area is entered, while each field's pack carries the world data, navigation and pictures. That is why the mode-0 completion keeps only slots 0, 1 and 10 and frees the rest. DATA, from the join above.*

## 8. Related

- [The menu-map container](../../02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/sloc-menumap-container.md) — `TIM2` + `NPS2`, the same records as slots 24–31.
- [`section_014` — `LGT2`](../../25-EBP-Script-Container/Sections/section-014.md) — the light-set format slot 17 carries.
- [The authored data table registry](../../02-Resource-And-Asset-Pipeline/authored-data-table-registry.md) — the map-reference row (`AG-10`).

## 9. Falsification pass 1 — 2026-09-13 (OPUS)

*(`check_already_answered.py` run first, per
[`EVIDENCE-STANDARD.md`](../../_index/EVIDENCE-STANDARD.md)'s 2026-09-13 amendment.)*

**The 550 `.mpk` files are not in this working tree** — they live in the VBF, and `census.py` reads
them from there. So this pass could not re-extract the corpus. What it *could* do is check the two
things that make the census trustworthy: **the instrument, and the arithmetic between its own
numbers.** Both hold.

### The corpus table matches the recorded census, line for line

| §"Corpus validation" | `census.out.txt` |
|---|---|
| 550 of 550 entries | `control: .mpk entries in the archive index: 550 (published 550)` — **its own denominator control** |
| count field **32** in 550/550 | `count field: {32: 550}` |
| sizes add up to the file, 550/550 | `layout ends exactly at the file size: 550 []` — empty failure list |
| the `0x40` slot all zero, **4,568/4,568** | `{True: 4568}`, no `False` key |
| fourteen slots never used | `slots never present: [2, 3, 5, 6, 7, 11, 12, 14, 18, 19, 20, 21, 22, 23]` — **14** |

### An internal check neither artifact makes

The eighteen per-slot presence counts — `545, 46, 461, 461, 270, 545, 387, 2, 456, 212, 421, 136,
32, 17, 396, 133, 31, 17` — sum to **exactly 4,568**, the same number as the zero-slot checks.

> The two figures are produced by different lines of the script over different loop variables, and
> they agree to the unit. **That makes each a check on the other**: a miscount in either would have
> to be matched by an equal miscount in the other to stay consistent.

### The census's layout is the loader's own arithmetic

`census.py` says it assumed the layout from `0036B980`. That function is **727 B** and both cited
ranges lie inside it. The size check reads:

```asm
0036BA0A  movsxd rdx, dword ptr [rdx]      ; the count
0036BA10  lea    eax, [rdx + 1]
0036BA16  lea    rcx, [rcx*4 + 0x3f]       ; (count + 1) * 4 ...
0036BA1E  and    ecx, 0xffffffc0           ; ... rounded up to 0x40
0036BA30  mov    eax, dword ptr [rdx]      ; each size
0036BA34  je     0x36ba39                  ; zero sizes contribute nothing
0036BA36  add    eax, 0x40                 ; a 0x40 slot before each payload
0036BA39  add    ecx, eax
```

**That is the assumption, instruction for instruction** — count word plus size table padded to
`0x40`, then a `0x40` slot before each non-zero payload — and the accumulation into `ecx` **is** the
"sizes add up to the file" test §"Corpus validation" calls *the loader's own acceptance test*. The
census did not assume a layout and check the files against it; it took the layout from the code that
enforces it.

**Not claimed:** the raw `.mpk` bytes were **not** re-read, so every per-slot size, median and magic
in the census output stands on the original run. The section-to-system routing, the discarded
sections and the `EFB0`-versus-loose-`.efb` comparison were not re-derived. Nothing was executed or
observed live.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited.*

- **CoreRuntimeScheduling — MECHANICAL, and one CLIENT.**
  - Five cited functions reach their tables through `ImageAddress_ResolveRuntimePointer` / `RuntimePointer_EncodeImageAddress`:
    `0036B980`, `0037AA90`, `00406E80`, `00467D20` and `00468160`.
  - `002465F0` asks the half-rate-mode test (27 B).
  - `003638B0` asks the frame-mode getter (8 B, over `02064AD3`).
  - `001A9930`, the console-block accessor, is called by the per-frame adapter of slot 4. That is the per-frame pump named
    in [the Phyre application page](../../22-Middleware-PhyreEngine/Application-Framework-Boundary/the-game-is-a-phyre-application.md) §7a.
- **CombatAction — CLIENT.** `BattleUnit_TryTriggerNearbyAuthoredFieldAction` and a 477-byte sibling read the field id
  `003148F0`.
- **Spawn_Encounter_Lifecycle — CLIENT.** `SpawnKeep_RotatePersistenceBanksForAreaTransition` reads the field id.
- **PlatformOnlineAchievements — CLIENT.** The 212-byte achievement-side caller reads the field id.
- **Gameplay — CLIENT.** The 44-byte vector helper `00203170` is also used by
  `BattleAction_FindApproachGeometryAroundTarget`. It is a workbench primitive with no map-pack meaning.

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Audio — SERVICE and CLIENT, not read, 17 edges.** Cited map-pack functions call Audio-filed bodies (43 to 1,122 bytes), and are called by four Audio bodies (188 to 1,036 bytes). What sound the map control pack drives is not read here.
- **Input — CLIENT.** The 0x60-byte Input-filed body `00291D90` calls `0024A680`, the free/release
  `003C63A0` runs against the old `[02B457F0]` pack object on the rebuild path this page now cites.
  Crossing-accounted.


- **Movement — CONSULTED BOTH DIRECTIONS (SWE2-EC7, batch 169).** `001F1590`, `00202C70` and the `02ADD0xx`-teardown helpers the batch-169 `003784A0` battery calls (`0026EAF0`, `0026FF50`, `00363750`) are consulted by that layer's bodies (`003ED190`, `003ED3F0`, `00230790`, `00338490` among them) while map-pack bodies ride its helpers in return - shared-helper fan-in around the pack lifecycle, not a movement responsibility of this page.
- **Presentation — CONSULTED BOTH DIRECTIONS (SWE2-EC7, batch 170, 318 edges).** The shared resolver `0016D6D0` this page's drain/teardown bodies reach is also called by Presentation-filed bodies (`001ACF80`, `001B5B60`, `001BC190` and their siblings), and the pack's `02CA6010`/`02CA6018` tables feed that layer's consumers in return - shared-helper fan-in around the pack tables, not a rendering responsibility of this page.
- **Actor - CLIENT and SERVICE (4 edges).** `0037A9B0`, `0037B230` are also called by bodies filed to Actor: `0037AA90` (ResourceAuxiliaryTable); `0032F1B0`, `003775D0` reach bodies filed to Actor: `0037AA90` (ResourceAuxiliaryTable) - shared machinery across the layer boundary, no shared ownership.
- **ActorEntity - CLIENT and SERVICE (99 edges).** `00202C70`, `00203170` are also called by bodies filed to ActorEntity: `003F1E90` (StateInterpolation); `002621D0`, `002628B0` reach bodies filed to ActorEntity: `00358940`, `0025B070` - shared machinery across the layer boundary, no shared ownership.
- **Party - SERVICE (4 edges).** `002628B0`, `00314020` reach bodies filed to party: `00358B40`, `00359200`, `00358C60` - shared machinery across the layer boundary, no shared ownership.
- **Resource - CLIENT (45 edges).** `0016D6D0`, `0016D720` are also called by bodies filed to resource: `0020B840`, `0020BFA0`, `006761F0` - shared machinery across the layer boundary, no shared ownership.
- **SaveLoad - CLIENT (2 edges).** `00245020`, `002EF2B0` are also called by bodies filed to SaveLoad (save/load settings): `00280140` (RuntimeLifecycleSupport) - shared machinery across the layer boundary, no shared ownership.
- **Save_Load_Settings - CLIENT (10 edges).** `00244960` is also called by bodies filed to save/load/settings: `0057E4D0`, `005819F0`, `005823B0` - shared machinery across the layer boundary, no shared ownership.
- **Script_VM_Native_Bridge - CLIENT and SERVICE (141 edges).** `00202E90`, `00202F00`, `00203170` are also called by bodies filed to script VM / native bridge: `00356160`; `002621D0` reaches bodies filed to script VM / native bridge: `003DC240` - shared machinery across the layer boundary, no shared ownership.
- **Story_Event_Quest_Hunt - CLIENT (12 edges).** `002EF2B0` is also called by bodies filed to story/event: `0032A8A0`, `0032A930`, `0032A9A0` - shared machinery across the layer boundary, no shared ownership.
- **UI - CLIENT (80 edges).** `00181DD0`, `00202C70` are also called by bodies filed to UI: `0024B9B0` (Transform), `002AF960` (Text), `002D2600` (Transform) - shared machinery across the layer boundary, no shared ownership.

## The `00378120` exclusive subtree — all 4 members bound (SWE2-FRONTIER, followup queue)

`00378120` (266 B) is the `YM00`/picture-0 map setup §3.4 describes. The full
order is: `[02ADD010]` → `003C63A0` and `[02ADCFE0]` republished to `02ADCFF8`
(`00378124`–`00378139`); `00379870(0)`; then — only when `[02ADCFF0]` is live —
`0026E7D0` on it, republish to `02ADD000`, copy `02ADD0E4` → `02ADD0E0`, and
null `02ADCFF0` (`00378145`–`00378181`). `0026E760([02ADCFF8])` follows, then
`[02ADCFE8]` → `02ADD008` through `00384160`, the three `02EBB7F8`/`FC`/`804`
dwords copy to `02ADD10C`/`110`/`114` with `02ADD108 = 0xA`, and `003AFD40`
applies either `[[0209A660]+0x10]`'s float4 (when `+0x1C` is set) or the
`{0, 100.0, 180.0, 0}` default placement (`003781CF`–`0037821A`), tailing into
`00332130(0)`.

| member | role | interior |
| --- | --- | --- |
| `0026E7D0` (126 B) | the request twin — the `0026EDB0`/`0209A670`/`0209A668` context prologue, `003EC9A0` object resolve, `003EC8D0(6, 0x240)` request build, `002F6AB0` enqueue with `r8d = 0`, handle stored to `[0209A668]` | [`0026E7F6`](../../_index/ADDRESS-INDEX.md) |
| `0026E760` (109 B) | the post twin — identical prologue and request build but `002F6AB0` with `r8d = 1`, then `0026E960` on the request, tailing into `00322220` | [`0026E7B9`](../../_index/ADDRESS-INDEX.md) |
| `0026E960` (342 B) | the picture-0 registration — stores the object to `[0209A670]`, defaults `float[0209A6F4] = -100.0`, sets `0209A6FC`/`0209A708` to 1, stashes handles at `0209A690`/`0209A6A8`, then `003278D0` ×3 plus `003ED0B0`→`0209A2D0`, `003ED020`, `003ECFD0`, `003ED140`, `003B6BA0` | [`0026E966`](../../_index/ADDRESS-INDEX.md) |
| `003ED870` (39 B) | the active-pointer publish — `[rcx+0x1A8]` replaces `[02B5F1A8]` only when the object's count dword is positive (`cmovg`) | [`003ED881`](../../_index/ADDRESS-INDEX.md) |

Shared callees deliberately outside the census: `003C63A0`, `00379870`,
`00384160`, `003AFD40`, `00332130`, `003EC860`/`003EC9A0`/`003EC8D0`/`003ECF70`,
`002F6AB0`, `0026E640`, `00322220`, `003278D0`, `003ED0B0`, `003ED020`,
`003ECFD0`, `003ED140`, `003B6BA0`.

## The `00378230` exclusive subtree — all 2 members bound (SWE2-FRONTIER, followup queue)

`00378230` (114 B) — a map-pack load step: `003697F0` (`00378269`),
`001808A0` (`00378275`), member `0026EAC0` (`00378283`), then
`003697F0` again (`00378293`).

| member | role | interior |
| --- | --- | --- |
| `0026EAC0` (37 B) | callback registration — `rdx = 0026EDB0` handler, `rcx = 0209A670` registry, `003EC860` + `003ECF70` (`0026EAD2`/`0026EAD7`), tail `0026E640` (`0026EAE0`) | [`0026EAD2`](../../_index/ADDRESS-INDEX.md) |
| `0026F420` (77 B) | bounded scan — `0024C460` (`ecx = 2`, `0026F429`), `movdqa` mask `00915520` (`0026F42E`), `rcx = 02F8F24C`, `cmp rax, 0x40` (`0026F462`) | [`0026F462`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `003697F0`, `001808A0`, `003EC860`,
`003ECF70`, `0024C460`, `0026E640`. The `0209A670` cell is the shared
registry; `02F8F24C` the scanned table.

## The `00379870` exclusive subtree — all 2 members bound (SWE2-FRONTIER, followup queue)

`00379870` (144 B) — publishes a `{x, y, w, h}` rect for registry slot
`ecx` into `02B45800`–`02B4580F`. Loads `rcx = qword[02ADD030 + ecx*8]`
(`00379877`/`00379888`); when the slot's `byte[+3] == 0x31` the extent is
fixed `256.0f`/`256.0f` (`00379897`/`003798A4`), otherwise `w = +0x18`,
`h = +0x1C` (`003798AE`/`003798B3`), and a null slot yields `x = y = 0`
with `w = 256.0f` (`003798C4`/`003798CC`). `x = +0x10`, `y = +0x14` are
published through `003C6360` (`003798D5`); `w`/`h` are truncated to int
(`cvttss2si`, `003798DA`/`003798DE`) and tail-published through
`003C6380` (`003798F0`).

| member | role | interior |
| --- | --- | --- |
| `003C6360` (17 B) | x/y setter — `float[02B45800] = xmm0`, `float[02B45804] = xmm1` (`003C6360`/`003C6368`) | [`003C6360`](../../_index/ADDRESS-INDEX.md) |
| `003C6380` (31 B) | w/h setter — int args `ecx`/`edx` → `cvtdq2ps` → `float[02B45808]`/`02B4580C` (`003C6388`/`003C638E`) | [`003C638E`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none. `02ADD030` is the indexed slot
registry (8-B entries); `byte[+3] == 0x31` selects the fixed 256×256
extent over the slot's own `+0x18`/`+0x1C`.

## The `003775D0`/`00377DC0`/`00378030`/`00378BC0` exclusive-subtree quadruple — all 4 roots bound (SWE2-FRONTIER, followup queue)

`003775D0` (~22 B) — `bt`/`btr` bit `0x12` test-and-clear on
`02ADD0F0` (`003775DA`/`003775E4`).

| member | role | interior |
| --- | --- | --- |
| `003635C0` | `022CBA90`/`022CBA9A` byte clears + `022CBAF0 = rcx` publish (`003635C0`/`003635CE`) | [`003635C0`](../../_index/ADDRESS-INDEX.md) |

`00377DC0` (~89 B) — `r11 = rsp`, `rbp = rsp - 0x1A8`, `0x290` frame
(`00377DC0`/`00377DCF`).

| member | role | interior |
| --- | --- | --- |
| `002DF880` | `movsxd ecx`/`movsxd edx` dual index into `0215F000` (`002DF880`/`002DF893`) | [`002DF880`](../../_index/ADDRESS-INDEX.md) |

`00378030` (~67 B) — `r14d = edx` under a five-slot spill
(`00378045`).

| member | role | interior |
| --- | --- | --- |
| `00264FD0` | `02099D88`/`02099D90` double non-null gate + `movsxd` index (`00264FD0`/`00264FE6`) | [`00264FD0`](../../_index/ADDRESS-INDEX.md) |

`00378BC0` (~8 B into a `0x130` stack-cookie frame — `00378BC2`/`00378BD3`).

| member | role | interior |
| --- | --- | --- |
| `00214B70` | `byte[01FD3AE2] = 1` setter (`00214B70`) | [`00214B70`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none.

## Interior citation — frontier hub `0024C460` (2026-09-18, SWE2-EC7)

`0024C460` — 235 B, 13 callers; the per-bucket chain teardown over the `020910A0`
type-bucketed record table. Interior verified: `movsxd rax, ecx` + `lea r14, [020910A0]`
(`0024C470`–`0024C47A`), head pointer from `[r14+rax*8+0x50]`, then a `do`/`while` walk
following each node's `[+0x348]` link ([`0024C4A0`](../../_index/ADDRESS-INDEX.md)). Per node
it publishes three globals — `[+0x120]` to `02EBEF98`, the node itself to `02F97348`,
`[+0x130]` to `02EBEFB0` — through `003A81E0`/`003A72E0`/`003A8D70`, and when `[+0x380]` is
non-null it slots the node into the `0209Axx` word-indexed table under a `<0x100` count gate
(`word [0209216A]` count, `inc word [0209216A]` at `0024C511`), else it calls `00182CA0`.
Every node is freed through `003697F0` (`0024C51B`) and the bucket head is nulled at
`0024C531`. The un-request side of this page's §3.5 `003EC8D0`-built payload chains.

## Interior citation — frontier hub `003EC8D0` (2026-09-18, SWE2-EC7)

`003EC8D0` — 59 B, 10 callers; this page already calls it "the `003EC8D0` alloc" — the body
confirms it: `0036C1D0(rcx, 0xB)` acquires the kind-0xB pool context ([`003EC8DD`](../../_index/ADDRESS-INDEX.md)),
`0036A190(ecx)` performs the sized allocation (`003EC8E4`), `0036C140` releases, and on a
null result it reports through `00862690` with the literal at `00D11BF0` (`003EC8FD`) before
returning the pointer. The `count·4`/`count·0x70` payload blocks in the §3.5 tag handlers
come from exactly this pool call.


### Interior citation — frontier hub `0026E500` (2026-09-18, SWE2-EC7)

`0026E500` — 40 B, 10 callers: the context slot-pair getter the camera hit
check leads with. `0209A670` null-gates the whole body; `ecx` then selects
between the `+0x3A8` and `+0x3B0` qwords of the `0209A2D0` record —
`cmovne eax, edx` at [`0026E51D`](../../_index/ADDRESS-INDEX.md) — returning
the selected pointer, or 0 when the pack is absent.
## SWE2-EC7-23 update (2026-09-18) — `003C63A0` global singleton re-init

`003C63A0` (122 B) is the `[02B457F0]` singleton (re)initializer the map-pack
load path drives: existing pointer freed via `0024A680` and the global nulled,
`0035D530` descriptor fetch, then `0024A480` alloc (`rdx = [01E0C248]` class
block, `r8d = 2`, `0x200` size) stored back to `[02B457F0]` with
`word[[rax+0x20]+0x14]` mirrored into `[02B457F8]` — the pack object's
rebuild-on-load arm. Interior anchor `003C63B7` (the free call).

## SWE2-EC7-30 update (2026-09-18) — `0026E5F0` five-mask fold (via `002F4520`/`002F5550`/`004668C0`)

`0026E5F0` (73 B) — reached through `002F4520`, `002F5550` and
`004668C0` — is the active-mask combiner of the `0209A6xx` state
block: while `0209A670` is live it folds
`([0209A6C8] | base) & ~[0209A6C0]`, where `base = [0209A690]` plus —
only when `dword[0209A6FC]` is set — `| [0209A6A0]` and
`& ~[0209A698]`; a dead manager returns 0. Interior anchor
`0026E62C` (the final `or`/`not`/`and` fold).
## SWE2-EC7-31 update (2026-09-18) — `0024A680` registered-object release

`0024A680` (141 B) is the member-release the pack's teardowns call:
the `0208F580` registry (0x48-stride, up to 0x40 slots) is scanned
for `rcx`; on a hit `00181610(obj)` runs, `dword[obj+0x38] & 0x3F00
== 0x1400` sends `qword[obj+0x10]` through `003697F0`, a non-zero
`edx` sends `qword[obj+0x18]` the same way, `+0x38` bit `0x20` is
cleared (`& 0xFFFFFFDF`), and `dword[02090780]` decrements. A
miss is a silent no-op. Interior anchor `0024A6F8` (the `0xFFFFFFDF`
mask store).

## SWE2-EC7-34 update (2026-09-19) - `00231A90`

`00231A90` (936 B) is a map-cell resolver - the `00233050` grid linearizer first (sign-checked `test ax,ax; js`), `[rsi+0x40]` word, `0209A2D0` base, `002324F0`/`00231E15`/`00231C1B`/`0022F050`. Interior anchor `00231ABB` (the `00233050` call).

## SWE2-EC7-34 update (2026-09-19) - `003ED3F0`

`003ED3F0` (952 B) is a map-record table walker - `[rbx-0xF4]` entries from `02B5ED94` against `02B5F214`, `00861EC0`/`001F1590`/`003ED74D`/`003148F0`/`00203170`. Interior anchor `003ED43F` (an `00861EC0` call).

## SWE2-EC7-34 update (2026-09-19) - `00468160`

`00468160` (945 B) is a map-pack record resolver - null guard, `movsxd` row index, `003EC8D0`/`003CCB60`/`0020E600` plus `00536080`/`00536060`/`003CCC20`. Interior anchor `00468217` (an `003EC8D0` call).

## SWE2-EC7-35 update (2026-09-19) - `00467D20`

`00467D20` (817 B) is a map-pack record fill - the `00D12520` constant pair `{2,1}` stored three times, six `0020E620` image-address encodes plus `003EC8D0`/`003EC8A0`/`003A1FE0`/`00536080`. Interior anchor `00467DC6` (a call site).

## SWE2-EC7-35 update (2026-09-19) - `003CCC20`

`003CCC20` (761 B) is a map-pack data accessor - `02B47798`/`02B47774`/`022D9138` state reads, a single `00181DD0` call. Interior anchor `003CCE6B` (the `00181DD0` call).

## SWE2-EC7-37 update (2026-09-19) - `003ED190`

`003ED190` (597 B) is a map-pack resolve body - `01F44830`/`02EBB7F0`/`01CEBB60`/`01CEBBA8`, `00366690` triple plus `001F1590` pair and `003148F0`/`00203170`/`00202E90`/`00202F00`/`00202F70`. Interior anchor `003ED1C9` (a `003148F0` call).

## SWE2-EC7-37 update (2026-09-19) - `00183EE0`

`00183EE0` (588 B) is a resource-chain sibling - `01F44830`/`02CF72C0`/`02CF7A30`/`01F7F5A0`, `00861EC0` pair plus `0085E730`/`006160B0`/`0060DD70`/`00610990`/`00625F00`/`0061E200`. Interior anchor `00183F2D` (an `0085E730` call).

## SWE2-EC7-37 update (2026-09-19) - `001837C0`

`001837C0` (573 B) is the tag-resolve helper the page names - `01F44830`, `008C5B34`/`008C5B40` consts, `00861EBA`/`0017E8E0`/`00808C40`. Interior anchor `00183830` (an `00861EBA` call).

## SWE2-EC7-37 update (2026-09-19) - `001A4DB0`

`001A4DB0` (545 B) is the resource-manager resolve chain the page names - `0017FEA0` pair plus `001A37C0`/`001837C0`/`00183EE0`/`00184140`/`001A40B0`. Interior anchor `001A4EA0` (an `001A37C0` call).

## SWE2-EC7-37 update (2026-09-19) - `004668C0`

`004668C0` (516 B) is a map-pack record op - `02EBB6E0`/`02EBB6F8`/`01CEBD80`/`008C5B2C`, `0026E5F0`/`00466240`/`00466550`. Interior anchor `004668E4` (a `0026E5F0` call).

## SWE2-EC7-37 update (2026-09-19) - `00467420`

`00467420` (503 B) is a map-pack field sweep - `02EBB6E0` quintuple plus `02EBB6F0` triple, a single `00203170` call. Interior anchor `004675C7` (the `00203170` call).

## SWE2-EC7-39 update (2026-09-19) - `001A40B0`

`001A40B0` (408 B) is a map-ctrl-pack body - two vcalls only, no direct calls. Interior anchor `001A4177` (the first vcall).

## SWE2-EC7-40 update (2026-09-19) - `001A37C0`

`001A37C0` (358 B) is a map-ctrl-pack body - `0016D840`/`0016D6D0`/`001A4440`/`001A3650` plus two vcalls. Interior anchor `001A37F9` (a `0016D6D0` call).

## SWE2-EC7-40 update (2026-09-19) - `00384160`

`00384160` (372 B) is a map-pack sibling - `02AEDFB0`, `0020E600` 13-times/`0020E620` 9-times record fill. Interior anchor `0038417C` (an `0020E600` call).

## SWE2-EC7-42 update (2026-09-19) - `004677A0`

`004677A0` (317 B) is a map-ctrl body - `02EBB6E0`/`02EBB6F0`, `00466420` pair. Interior anchor `00467838` (a `00466420` call).

## SWE2-EC7-45 update (2026-09-19) - `00232380`

`00232380` (240 B) is a call-free jump-table dispatcher - `[rdx]`-count u32 records, `(w & 0xFFFFFF)<<4` entry offset, `sar eax,0x18` case 0-5 via an `rsi`-relative table; each arm stores the entry ptr + `imul`/`sar`-halved fields into the `r9` output record. Interior anchor `002323CF` (the table index load).

## SWE2-EC7-46 update (2026-09-19) - `002F5450`

`002F5450` (229 B) is a body - `003EC8A0`/`003ECA70`/`00466B10`/`00468060`. Interior anchor `002F5468` (an `003EC8A0` call).

## SWE2-EC7-48 update (2026-09-19) - `00466420`

`00466420` (206 B) is a call-free jump-table slot writer - `cmp edx,0x14` case dispatch, each arm stores `r8` into a distinct `rcx+0x90`..`+0x110` field. Interior anchor `00466433` (the table index load).

## SWE2-EC7-48 update (2026-09-19) - `003EC9A0`

`003EC9A0` (199 B) is a call-free ring-slot allocator - `02EBB9E0` mod-8 cursor (`& 0x80000007` wrap), `0x38`-stride `02EBB820` slots, first-free `+8` = -1, `0x2F`/`0x5C` name split, `"unknown"` default `00D11C00`. Interior anchor `003EC9B3` (the cursor advance).

## SWE2-EC7-49 update (2026-09-19) - `003CCB60`

`003CCB60` (191 B) is a call-free 32-entry `02B47790` slot allocator - `+4`-nonzero scan, `02B47774` counter `<< 8 | slot` id, `word[+2] = r8w`, `word[] = 0x8000`, `+0x28`/`+0x30` links. Interior anchor `003CCB74` (the slot scan).

## SWE2-EC7-50 update (2026-09-19) - `003E9020`

`003E9020` (186 B) is a body - `00408200` single call. Interior anchor `003E9038` (the `00408200` call).

## SWE2-EC7-50 update (2026-09-19) - `00467BF0`

`00467BF0` (181 B) is a body - `005360C0`/`00808C40` plus a `008C2F70` import call. Interior anchor `00467C7C` (a `005360C0` call).

## SWE2-EC7-52 update (2026-09-19) - `00466550`

`00466550` (867 B) is a map-pack record op helper - `00202E90`/`00202F00`/`00202F70`/`00202D70`/`00202FE0` plus `0209A370`. Interior anchor `004667DC` (a `00202E90` call).

## SWE2-EC7-53 update (2026-09-19) - `0022F050`

`0022F050` (505 B) is a map-ctrl-pack body - `00202E10`/`00808C40`/`00861F14` plus `00908DEC` rdata. Interior anchor `0022F1B1` (a `00202E10` call).


## SWE2-EC7-53 update (2026-09-19) - `00466240`

`00466240` (475 B) is a call-free record evaluator - `[rdx]`-tabled min/max over `[rcx+0x3C]`/`[rcx+0x40]`/`[rcx+0x48]`, `[rcx+0x4C]`-bit-1 threshold arm. Interior anchor `00466288` (the `minss`).


## SWE2-EC7-53 update (2026-09-19) - `001A3650`

`001A3650` (366 B) is a map-ctrl-pack body - `0016D720`/`0016D840` plus two vcalls. Interior anchor `001A36C3` (a `0016D720` call).

## SWE2-EC7-58 update (2026-09-19) - `001801A0`

`001801A0` (168 B) is a map-ctrl-pack body - `001A4DB0`/`001A9930`. Interior anchor `001801BF` (a `001A9930` call).


## SWE2-EC7-58 update (2026-09-19) - `001A4440`

`001A4440` (165 B) is a map-ctrl-pack body - `0016D840` single call plus one vcall. Interior anchor `001A44BE` (a `0016D840` call).

## SWE2-EC7-59 update (2026-09-19) - `003788F0`

`003788F0` (161 B) is the mode-1 `02ADD050` completion the map-ctrl page names - `0026FF90`/`003697F0`/`0036C110`/`0036C140`/`0036C1A0`/`0036C1D0` plus `02ADD050`/`02ADD088`/`02ADD0EC`/`02ADD0F0`. Interior anchor `00378928` (a `0036C1D0` call).


## SWE2-EC7-59 update (2026-09-19) - `003789A0`

`003789A0` (161 B) is the `02ADD09x` completion sibling - `003697F0`/`0036C110`/`0036C140`/`0036C1A0`/`0036C1D0`/`0053DD10` plus `02ADD088`/`02ADD098`/`02ADD0EC`/`02ADD0F0`. Interior anchor `003789D8` (a `0036C1D0` call).



## SWE2-EC7-63 update (2026-09-19) - `003ED020`

`003ED020` (143 B) is a call-free record-field reader - `(r9*3)<<7 + r11` base + `rcx<<5`, reads `+0x90`/`+0x94` pair into `[rbx]`. Interior anchor `003ED054` (the `+0x90` field read).


## SWE2-EC7-81 update (2026-09-20) - `00536080` variable-record walk measured

`00536080` (60 B) is the nth-element walk the pack callers use:
`edx >= word[+6]` returns 0; else `rax` starts at
`rcx + (byte[+5] ? 0x80 : 0x10)` and follows `dword[rax]` stride
links `edx` times - the variable-length record indexer.
Interior anchor `005360B0` (the stride read).

## SWE2-EC7-83 update (2026-09-20) - `00466CB0` multi-key element find measured

`00466CB0` (288 B) is the indexed find the pack callers run: `ecx`
selects the x80 record in `01EAB6E0` (`dword[01EAB6E8]` gate), and on
a live `[+8]` object `word[+0x2A] <= 0xFF` with `r9 & (1<<cl)` returns
`[+0x28]` immediately; else the `word[+0x28]`-count loop matches `dx`
- `word[+0x2C] == 0` against `[+0x28]+i*0x130+0x46`, nonzero against
`word[[+0x10]+i*0x10]` returning the `word[+6]`-indexed record - and
finally the `bx` pass matches `+0x44` over `word[+0x32]` entries when
`word[+0x2C] == 0`. Miss returns 0.
Interior anchor `00466D90` (the `+0x44` match loop head).

## SWE2-EC7-85 update (2026-09-20) - `00408200` global-object teardown measured

`00408200` (71 B) is the pack teardown the callers run: when the
global object lives and its `[+0xC0]` sub-object has a null
`[+0x10]`, `00245020` runs on the sub-object first; `00245020` then
runs on the object itself and the global zeroes.
Interior anchor `00408226` (the first `00245020` call).

## SWE2-EC7-86 update (2026-09-20) - `003E8940` validated global install measured

`003E8940` (53 B) is the global-pointer install the map callers
run: `003E8D50(-1)` resets the slot, `[02B5D080]` takes `rcx`,
and when the record is live but `word[+4] != 1` the pointer is
cleared back to 0 - a type-tag gate on the installed object.
Interior anchor `003E8968` (the `cmovne` re-store).

## SWE2-EC7-87 update (2026-09-20) - `003CBB30` normalized-cursor record build measured

`003CBB30` (168 B) is the cursor-record build the map callers
run: `00229D60(rcx, xmm2)` returns the cursor scale, the record
at `rdx` is laid out with `scale*[rbx+0x10]` at `+0x14`,
`scale/span` at `+0`, `-([rbx]+[rbx+4])/span` at `+0x28`,
`[rbx]*[rbx+4]*-2/span` at `+0x38`, `dword = [rbx]*[rbx+4]` at
`+0x3C`, `-1.0f` at `+0x2C` and the rest zeroed - a
span-normalized progress record where `span = [rbx+4]-[rbx]`.
Interior anchor `003CBB7A` (the `divss` normalization).

`0024FF60` (151 B) is the sampled-pair publish `002F5550` (this page's tag-30 presentation pass) calls: `00182450` and `00182470` are each converted `cvtss2sd` -> `003B40F0`, offset by `+3.0` / `-3.0` (`00915510`), and compared - when the first sum exceeds the second, `(s1+s2)/2` (`01CEBBD8` = `0.5`) is written to both `02AEEBA0` and `02AEEBA4`; otherwise each sum lands in its own slot - a paired float latch feeding the pass's timeline.

Interior anchor `0024FFBB` (function `0024FF60`).

`003784A0` (143 B) is the teardown battery `00378A60` runs over the `02ADD0xx` statics: `02ADD000` and `02ADD0A0` each get their paired flush (`0026EAF0`/`0026FF50`) then `003697F0` on the stored pointer and a clear, `02ADD0E0` takes `0xFFFFFFFF`, `00363750` flushes once more, and `02ADD068`/`02ADD080` release through `003697F0` - the pack's whole-static shutdown sweep.

Interior anchor `003784E1` (function `003784A0`).

`004680D0` (139 B) is the table drain `002F5450` calls on this page's `02CA6010` array: each of the `02CA6020`-counted `0x40` rows releases `+0x14` through `003CD5D0` when `+0x04` is clear and `+0x30` the same way when `+0x10` reads 4, then `003EC8A0` frees both `02CA6010` and `02CA6018` and the tail jumps `00180280` - the full-table teardown the map pack runs on unload.

Interior anchor `0046810E` (function `004680D0`).

## Interior citations for the entry-cited functions (OPUS, 2026-10-01)

*The functions this page named only at their entry. Each was read from the certified image; the sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Verified by [`mapctrl_interior.py`](../../_index/candidates/opus-mapctrl-interior-1001/mapctrl_interior.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `001806F0` | 32 B | when `001A9930()` returns an object, stores `ecx` in its dword `+0x20` | `00180700`, `00180702`, `00180707` |
| `00180730` | 112 B | calls `001A9B70` with the `001A9930()` object as the first argument, followed by this function's own four register arguments and three stack arguments | `0018074F`, `00180754`, `00180786` |
| `001807A0` | 79 B | when `001A9930()` returns an object, calls `001A9BF0(object, byte +0x1C of 00189120() is non-zero, ecx, edx)` | `001807C4`, `001807C7`, `001807DA` |
| `00182280` | 137 B | when `00189120()` returns an object, calls `00185CD0` on it with this function's four float arguments and its two byte stack arguments | `001822B3`, `001822C0`, `001822E6` |
| `001A9B70` | 121 B | passes `r8d` on as 1, 2, 3 or 4 when it is 1 to 4 and as 0 otherwise, calling `001E5790(rdx, that value, r9, ...)` with its four stack arguments passed on (the first in `r9`) | `001A9B7A`, `001A9B96`, `001A9BDF` |
| `001ACF80` | 306 B | when `001A9930()` returns an object, walks the list at `+0x10` (`0016D6D0` steps it) for the node whose payload `+0x40` has a non-null `+0x100` and whose string `+0x20` equals the string at that object's `+0x241`; on a match it decrements `+0x30`, unlinks the node (`0016DA60`), frees the node's string and the 0x48-byte node through the allocators at node `+0x38` and this `+0x38`, calls `001AC4B0(this, payload +0x100, payload +0x108)`, sets byte `+0x130`, frees payload `+0x100` (`00210EB0`) and the 0x118-byte payload (`00809950`) | `001ACFE0`, `001AD014`, `001AD078`, `001AD09D` |
| `001E5540` | 123 B | stores the floats `xmm1` at `+0x1FC` and `xmm2` at `+0x200`, then calls `0060EC30(element, r9d)` for each qword of the array [`+0x18`, `+0x20`) | `001E5564`, `001E5570`, `001E5595` |
| `00231F50` | 38 B | zeroes the nine qwords `+0x00` to `+0x40` | `00231F52`, `00231F6D`, `00231F71` |
| `0026E290` | 97 B | on the object `*(0209A670)` with dword `+0x120` non-zero: when dword `0209A708` is set, calls `002F7380(object, *0209A668)` and clears `0209A708`; then calls the object's function pointer `+0x130` with (object, `ecx`) when it is set | `0026E2A8`, `0026E2C4`, `0026E2C9`, `0026E2E4` |
| `0026EDB0` | 65 B | calls the function pointer at `+0x128` when it is set, then `0016D6A0` on `+0x40` and on `+0xA8` | `0026EDC9`, `0026EDD7`, `0026EDDC` |
| `002F6740` | 124 B | stores the count `[rdx]` at `+0x22C`; when it is positive, stores `rdx + 0x10` at `+0x1A0`, allocates count * 12 bytes through `003EC8D0(6, ...)` into `+0x1D8`, and fills each 12-byte entry with the qword 1 and the float 1.0 at `+8` | `002F674B`, `002F676B`, `002F679D`, `002F67A6` |
| `0034DC70` | 36 B | tail-calls `003E9020(00267E10(argument 4), 00377B90())` | `0034DC79`, `0034DC80`, `0034DC8F` |
| `00355300` | 79 B | when `00267310(byte +0x15 of argument 2)` is non-zero, calls `00473680`, `003E8AA0` (with that byte) and `00466DD0`; then returns 1 when `003E82F0(dword [argument 3])` is non-zero, else 0 | `00355314`, `0035532A`, `00355336`, `00355344` |
| `0037A9B0` | 78 B | in record `ecx` (0x50 bytes) of the table at `02EBF420`, scans the 8-byte entries from `+0x10` of the list at `+0x18` (count `+4`) for the word equal to `edx` and sets that entry's byte `+2` to 1 | `0037A9BD`, `0037A9E3`, `0037A9F7` |
| `0037ACA0` | 45 B | for `ecx` up to 4, clears byte `+0x4C` of record `ecx` of `02EBF420` (address `02EBF46C`); for `ecx` 0 with the qword `02EBF420` null, tail-jumps to `003774C0` | `0037ACAF`, `0037ACB6`, `0037ACC6` |
| `0037ACD0` | 53 B | for `ecx` up to 4, sets byte `+0x4C` of record `ecx` of `02EBF420` to 1 when its qword `+0` is non-null; for `ecx` 0 with the qword `02EBF420` null, tail-jumps to `00379290` | `0037ACE6`, `0037ACED`, `0037ACFE` |
| `0037B290` | 42 B | returns word `+0x10` of the list at `+0x18` of record `ecx` of `02EBF420` when the list exists with a non-zero count `+4`, else -1 | `0037B2A1`, `0037B2B1`, `0037B2B6` |
| `003B40F0` | 79 B | with v = its double argument xored with the 16 bytes at `01CEBD90`, returns (float `02B404A8` + float `02B40498` * v) / (float `02B404AC` + float `02B4049C` * v), computed in doubles and rounded through a float | `003B40F7`, `003B4118`, `003B4133`, `003B4137` |
| `003CD5D0` | 125 B | for slot `cl` of the 0x40-byte records at `*(02B47790)`: when its dword `+4` equals `ecx`, decrements byte `02B47770`, clears `+4`, clears dword `+0x30` of each node on its `+0x28` chain (linked through `+0x38`), unlinks the record from the list linked through `+0x18` / `+0x20` (ends `02B47778` / `02B47780`) and returns 1; otherwise 0 | `003CD5DE`, `003CD5E3`, `003CD600`, `003CD61F` |
| `003E8230` | 104 B | resolves id `ecx` in the table at `*(02B5D080)`: below word `+8`, splits it into id / 100 and id % 100; the group directory at word `+0xC` holds the group count, and each 4-byte group entry a member count (word `+2`) and an offset (word `+4`); returns table + offset + (id % 100) * word `+6`, or 0 when out of range | `003E8244`, `003E8252`, `003E826B`, `003E8289` |
| `003E82A0` | 9 B | tail-calls `0037B030(0, ecx)` | `003E82A2`, `003E82A4` |
| `003E82F0` | 85 B | resolves `ecx` through `003E8230`; when found, tail-calls `003E8350(record, table + word +0xE, 00265920())`, else returns 0 | `003E8306`, `003E830B`, `003E831B`, `003E8333` |
| `003E8860` | 37 B | clears bit 3 of word `+0` of the record `003E8230(ecx)` resolves | `003E886E`, `003E887D` |
| `003E8890` | 33 B | sets bit 3 of word `+0` of the record `003E8230(ecx)` resolves | `003E889E`, `003E88A8` |
| `003E88C0` | 60 B | on the record `003E8230(edx)` resolves: clears bit 3 and sets bit 4 of word `+0`, stores `cl` in byte `+0x15` and keeps only the low four bits of byte `+0x12` | `003E88D3`, `003E88E8`, `003E88EC`, `003E88F0` |
| `003E8900` | 64 B | as `003E88C0`, and also sets bit 4 of byte `+0x12` | `003E8913`, `003E8930`, `003E8934` |
| `003EC910` | 95 B | between `0036C1D0(..., 0xB)` and `0036C140`, allocates `edx` bytes through `0036A190`; on null calls `00862690(00D11BF0)` and returns null; otherwise calls `r8` on the block when it is set and returns the block | `003EC924`, `003EC92B`, `003EC944`, `003EC95F` |
| `003EC970` | 36 B | for `ecx` up to 7, returns the 0x38-byte record `ecx` at `02EBB820` when its qword `+0` is non-null, else 0 | `003EC97A`, `003EC981`, `003EC98B` |
| `003ECA70` | 68 B | for `ecx` >= 0, on record `ecx` (0x38 bytes) at `02EBB820`: calls `003EC8A0` when dword `+8` is positive, clears qword `+0` and dword `+8`, and decrements dword `02EBB9E4` | `003ECA97`, `003ECA9E`, `003ECAA4` |
| `003ED840` | 45 B | stores `rcx` at `02B5F1A0`; with n = dword `[rcx + ([rcx] + 1) * 4]` AND `0xFFFFFF`, stores `rcx + n * 16` at `02B5F1B0` when `edx` is greater than n (signed) | `003ED844`, `003ED84F`, `003ED865` |
| `00466B10` | 111 B | for each of the dword `02EBB6E0` 0x50-byte records at `*(02EBB6F0)`, passes `+0x20` and `+0x28` to `003EC8A0`; then passes `02EBB6F0` itself, and clears qword `02EBB6F8` and the count | `00466B3B`, `00466B44`, `00466B5F`, `00466B6F` |
| `00467D00` | 17 B | zeroes qword `+0x10`, dword `+0`, qword `+8` and qword `+0x18` | `00467D02`, `00467D08`, `00467D0C` |
| `0051EDC0` | 49 B | returns the qword `+0x70`, `+0x78` or `+0x80` of `*(0209AC30)` for `ecx` 1, 2 or 3, and `+0x68` otherwise | `0051EDDA`, `0051EDE2`, `0051EDE7`, `0051EDEC` |
| `00536060` | 27 B | returns 0 when word `+0xE` is 0, else `rcx` + word `+0xC` + dword `+8` | `0053606A`, `0053606D`, `00536077` |
| `005360C0` | 84 B | allocates dword `+0x10` + 0x10 bytes through `003EC8D0(6, ...)`, stores `rcx` at the block's `+0`, links the block through `+8` (the block takes `[rcx+8]`'s old value, that node points at it, `[rcx+8]` becomes it), copies dword `+0x10` bytes from `rdx` to the block's `+0x10` through `00861EBA`, and increments dword `+0x14` | `005360DB`, `005360E3`, `005360F9`, `00536101`, `00536106` |
| `00291D90` | 625 B | dispatches on the message `[rdx]`: 1 stores itself at `*(0209AC30) + 0x300`, resets `+0x168` with 1 in its bits 16-19, clears the ten 16-byte slots at `+0xC8` and calls `00247950`; `0x12` clears `*(0209AC30) + 0x300`; 2 steps a state machine kept in bits 16-19 of `+0x168` whose steps copy the ten slots from `0209BEA0`, request `0024A440(qword +0xD0, *01E0C210, 2)` into `+0xC0`, test each slot with `0032E4D0`, release `+0xC0` through `0024A680`, and in one state call `00244F00` on itself; any other message goes to `005C5230`, whose result it returns; messages 1, 2 and `0x12` return 0 | `00291DB7`, `00291F96`, `00291F2D`, `00291E4A` |
