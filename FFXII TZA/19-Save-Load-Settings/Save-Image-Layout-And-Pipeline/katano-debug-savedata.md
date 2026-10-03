---
system: .sav — sixteen development save images, shipped and not loaded
category: 19-Save-Load-Settings
status: AUDITED
owner_layer: PrimaryOwner:Save_Load_Settings
evidence_tier: 1
verified_against:
  gzf_sha256: fb9b5e7ea002c1626a53d47da0b0b69a2443e246f7ce2b64329be4e034a2d3f7
  snapshot_sha256: a9cead8777597cdca58f2a47f27153f5231d60ad2bc16c3da9df8253820b09bd
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity - every function this document cites has byte-identical per-function records in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: 7 cited function entries, 0 of them among the 128 records that changed across GN158..GN161 (check_delta_additivity.py, check_transfer_eligible.py); re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS-REQ-FABLE-PROVENANCE-TRANSFER-144 (9bedb5e0); re-targeted GN160 -> GN161 under EVIDENCE-STANDARD addendum 2026-09-14bh
    previously: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708 (GN160), superseded 2026-09-14
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
corpus_validated: "16 / 16 .sav in the archive index, all opened, 2026-09-12"
last_reviewed: 2026-09-13
archive_formats:
  - "sav"
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-katano-savedata-pass-1 - all sixteen re-read and every published figure exact; NEW: generation B is generation A's map from +0x08 on (60 Hz clock identity 8/8 with five failing controls), the four header constants are block sizes and version stamps with +0x64 recording the 02EBF190 block at 23,152 against 29,712 shipped, and a third route - console ids 15/16 - names the operation but only prints a number
  crossref_clean: false        # 2026-09-30 (SWE2-DATA): false until the pass-22 UNACCOUNTED NEIGHBOUR findings are accounted (FRONTIER-REQ-SWE2-DATA-PASS22-DEBT; OPUS-REQ-DATA-PASS30-CROSSREF-CLEAN-0930)
  reopened_count: 0
---

# `.sav` — sixteen development save images

> `ps2data/image/ff12/katano/ff12savedata00.sav` … `15.sav`: save images left in a developer's folder,
> in three generations of layout. Four match the shipped runtime save image header exactly except for
> one constant — and that constant is the size of a runtime block that has since grown (§6).
> **Nothing in the executable names them**, and all three routes that could reach them — by path,
> by the sixteen-slot debug loader, and by the developer console command that names the
> operation — are inert.

**Corpus validation.**

| | |
|---|---|
| files examined | **16 of 16** `.sav`, all opened |
| **generation A** — 57,864 B (`0xE208`) | slots 00–03 |
| **generation B** — 49,664 B, tag `FF12` | slots 04, 05, 06, 15 |
| **generation C** — 22,016 B, zero header | slots 07–14 |
| `ff12savedata` or `.sav\0` in the executable | **0 occurrences** |

Census: [`census.py`](../../_experiments/evidence/katano-savedata/census.py) →
[`census.out.txt`](../../_experiments/evidence/katano-savedata/census.out.txt).

---

## 1. What the player sees

**Nothing.** By their folder and contents these are development saves — the four readable ones hold one to five minutes of play and at most 150 gil — made while the
game was being built. The remaster's real saves live outside the archive and use the layout on
[the save image page](save-image-buffers-header-and-payload.md).

## 2. The layout

**Generation A (00–03)** is the runtime save image of [the save image page](save-image-buffers-header-and-payload.md) §4,
truncated at `0xE208`:

| field | 00 | 01 | 02 | 03 | shipped layout |
|---|---:|---:|---:|---:|---|
| `+0x00` checksum | 0 | 0 | 0 | 0 | CRC of `+0x08..+0xE200` in a written save |
| `+0x08` gil | 8 | 9 | 0 | 150 | gil |
| `+0x18..+0x1B` play time | 0:03:59 | 0:05:08 | 0:01:21 | 0:02:40 | h:mm:ss derived from `+0x10` |
| `+0x58` / `+0x5C` / `+0x60` | `20050223` `00001538` `05071901` in all four | | | | same constants |
| `+0x64` | `00005A70` in all four | | | | **`00007410`** |
| `+0x68` / `+0x6C` | `0131F3EA` / `00004818` in all four | | | | the pair `SaveImage_ValidateRuntimeFormatHeader` tests |
| payload `+0x1044` (image `+0x1244`) area id | 109 | 114 | 274 | 1145 | active or pending area id |
| `+0xE200` checksum copy | 0 | 0 | 0 | 0 | the finaliser's CRC copy |

So these images carry the current header constants and format pair but **no checksums** — they were
never passed through the write path — and a different fourth constant at `+0x64`.

**Generation B (04, 05, 06, 15)** begins with the tag `FF12`, `u32 1`, then `u32` values 6,500 / 6,500 / 0 /
500 at `+0x08`. **From `+0x08` on it is generation A's map** — gil at `+0x08`, the 60 Hz clock at
`+0x10` matching the `h:mm:ss` at `+0x18`/`+0x1A`/`+0x1B`, the area id at `+0x1244` — so the two
generations differ in their **first eight bytes ~~only~~** and in `+0x58`–`+0x6C`, which are zero in generation B where generation A carries its six constants *(corrected 2026-10-02, OPUS: read through `vbf_read_entry` from `FFXII_TZA.vbf`)*, tag and version where generation A has the
checksum (§6)~~. What follows the header is still undecoded~~ *(answered: see §7 `SV-1`, narrowed 2026-09-27 — all three generations carry the 40-record party-stats array; 2026-10-02, OPUS)*.

**Generation C (07–14)** has an all-zero header — zero through `+0x6C`, so not even the four
constants — and its first non-zero byte is at `+0x901` (slot 13: `+0x1244`). Seven of the eight are
byte-identical (the published CRC `09ABA8E5` is CRC32 over `[0x08, size)`, as the census computes
it; whole-file CRC32 `A66D9739` for the seven and `179883EE` for slot 13 says the same thing
independently), and `u32 +0x1244` reads 233 in those seven and 54 in slot 13.

## 3. The loader contract

**No loader opens these files.** Two routes were checked:

- **By name.** The executable contains neither `ff12savedata` nor `.sav` terminated by a NUL, in any
  case — the path is not in the image, so no path table can reach it.
- **By the debug slot loader.** The script verb `debug_loadjfdata` (`0x209C`, handler `0050D9A0`) calls
  `002EF300(slot)`, which clamps the slot to `0..15` (`002EF306`–`002EF314`) and loads **resource kind 1,
  index `0x75 + slot`**, `0xE240` bytes, into the active runtime save buffer (`002EF317`–`002EF336`). Sixteen
  slots and a save-sized read make it the loader these files were made for, but in the shipped kind-1
  path arrays indices 117–132 name other files (for example `test_battle\…\listhelp_status.bin` through
  `menu02.bin` in the array at `01E19670`), and no shipped script uses the verb.

| Field | Read by | Rejected if | Clamped to | Inert |
|---|---|---|---|---|
| the whole file | — | — | — | **yes — not named in the image; the one slot loader resolves different paths** |

## 4. Key addresses

| Address | Role | Read? |
|---|---|---|
| `0050D9A0` | `debug_loadjfdata` handler | ✅ entry and the `002EF300` call |
| `002EF300` | kind-1 slot load into the active save buffer | ✅ full body |

### Data addresses

| Address | Name | Kind | Contents |
|---|---|---|---|
| `01E19670` | a kind-1 path array | `.data` | indices 117–132: `listhelp_*.bin`, `menu0*.bin`, … |

## 5. Corpus survey

§2 lists every file. Generation A's four saves differ in gil, play time and area; everything else in
the checked header is identical across them.

## 6. Falsification pass 1 — 2026-09-13 (OPUS)

*(`check_already_answered.py` run first by term and by address, one query at a time and read in
full. Thirteen documents touch `savedata`; no register row answers anything here. The archive was
read, never written; nothing was executed.)*

### Everything §2 measures reproduces

All sixteen files were re-read from the archive and every published figure held: 16 of 16 `.sav`;
**57,864 / 49,664 / 22,016** bytes in the stated slot groups; generation A's checksums zero at both
`+0x00` and `+0xE200`; gil **8 / 9 / 0 / 150**; play times **0:03:59 / 0:05:08 / 0:01:21 / 0:02:40**;
`+0x58`/`+0x5C`/`+0x60` = `20050223` / `00001538` / `05071901` and `+0x64` = **`00005A70`** in all four;
`+0x68`/`+0x6C` = `0131F3EA` / `00004818`; area ids **109 / 114 / 274 / 1145**; generation B's tag,
`u32 1` and `6500 / 6500 / 0 / 500`; generation C's seven-plus-one split and `+0x1244` = 233 / 54.

One provenance note rather than a correction: the published `09ABA8E5` is the census's CRC32 over
**`[0x08, size)`**, not over the whole file. Whole-file CRC32 is `A66D9739` for the seven and
`179883EE` for slot 13 — the same seven-and-one split, reached without the census's span.

### ✔ New: generation B is not a foreign layout — it is generation A from `+0x08` on

§2 said generation B "is not the runtime image's and is not decoded here". Test: generation A's
`+0x10` is a **60 Hz frame counter** and `+0x18` (`u16` hours) / `+0x1A` / `+0x1B` is the same clock
written out. If generation B shares the map, the identity must hold there too.

| file | `+0x10` | stated `h:mm:ss` | derived at 60 Hz | gil `+0x08` | area `+0x1244` |
|---|---:|---|---|---:|---:|
| 04 | 1,352 | 0:00:22 | 0:00:22 | 6,500 | 210 |
| 05 | 1,584 | 0:00:26 | 0:00:26 | 6,500 | 152 |
| 06 | 95,308 | 0:26:28 | 0:26:28 | 0 | 152 |
| 15 | 20,462 | 0:05:41 | 0:05:41 | 500 | 275 |

**8 of 8 across generations A and B**, with controls that decide something: divisor 50, 30 and 24
each fail 8 of 8, 59 fails 6 of 8 and 61 fails 7 of 8; reading the counter from gil, from `+0x0C`,
from `+0x14` or from the area id fails 8 of 8; swapping minutes and seconds fails 8 of 8.

So **generations A and B differ in their first eight bytes ~~and nothing else that is decoded~~** and in the header constants `+0x58`–`+0x6C`, all zero in generation B *(corrected 2026-10-02, OPUS: read through `vbf_read_entry`; generation A carries `20050223` / `00001538` / `05071901` / `00005A70` / `0131F3EA` / `00004818`)*: the
tag `FF12` and a `u32 1` stand where generation A has its checksum and the dword at `+0x04`. ~~The~~
~~payload past the header is still undecoded in both, and generation C — zero through `+0x6C`, first~~
~~non-zero byte at `+0x901` — is undecoded entirely.~~ *(answered: see §7 `SV-1` — all three generations carry the 40-record party-stats array, generation C at image `+0x15FC`; 2026-10-02, OPUS)*

### ✔ New: `+0x5C` and `+0x64` are block sizes — and `+0x64` is the one that moved

Two of the four constants were already placed, and the katano page did not carry either.
[`V-2`](../../_index/OPEN-QUESTIONS.md) and
[the version-stamps page](version-stamps-and-what-loading-normalises.md) establish that
**`0x05071901` (`+0x60`) is the battle-state block's magic** — stamped at `002370DF`, compared at
`00233C4D` — and that **`0x20050223` (`+0x58`) occurs exactly once in the executable**, in its own
getter, with no reader anywhere. That is FABLE's, 2026-09-10, not this pass's.

The other two were not placed. Each of the four accessors has exactly one caller,
`SaveRuntime_InitializeHeaderAndImageBackedState` (`00253A80`, `00253AAC`–`00253AE5`), which writes
them into the header; the literals themselves say what they are:

| header | value | the other site in `.text` | what the number is | on record before? |
|---|---|---|---|---|
| `+0x58` | `20050223` | **none** — the getter `002EF2A0` is its only occurrence | unexplained | yes — `V-2` |
| `+0x5C` | `00001538` | `002EF2DD` — `memset(activeBuffer + 0x200, 0, 0x1538)` | the size of the region the save system clears at buffer `+0x200` | **no** |
| `+0x60` | `05071901` | `002370DF` stamps `*[02EBF190]`; `00233C4D` compares | the battle-state block's magic | yes — `V-2` |
| `+0x64` | `00007410` | `002370CD` — `memset([02EBF190], 0, 0x7410)` | **the battle-state block's size**, 29,712 | **no** |
| `+0x68` | `0131F3EA` | `00253AED` writes, `00255271` validates | the image-backed block's magic | yes |
| `+0x6C` | `00004818` | `00253AA1` — `memset([020927C0], 0, 0x4818)` | the image-backed block's size, 18,456 | yes |

`00001538` and `00007410` each occur in `.text` **twice and only twice** — the getter and the
`memset` length — so the identification is the whole immediate census, not a sighting. The block the
`0x7410` sizes is the one
[the battle-state block field map](../../11-Party/Battle-State-Block/the-battle-state-block-field-map.md)
documents field by field.

**So `+0x64` is not a free constant: it records how big the battle-state block was.** The katano
images say **`0x5A70` = 23,152**; the shipped build says **`0x7410` = 29,712** — the block grew by
**6,560 bytes**, and it grew at the end: the field map's last touched fields are block
`+0x5B00`–`+0x5B0E`, which lie **past the katano-era end** (`0x5A70`).

Two consequences worth keeping:

* **Nothing rejects these images over it.** `SaveImage_ValidateRuntimeFormatHeader` (`00255260`)
  tests `+0x68` / `+0x6C` only, and the katano images carry the shipped values for both. The
  `+0x64` literal has no reader beyond the write.
* **The magic did not move when the size did.** These images carry the shipped `05071901` at
  `+0x60` and the smaller size at `+0x64`, so `00233C4D` — the one check on that block — cannot
  tell the two layouts apart.

### ✔ New: a third route, which §3's two-route argument did not consider

The operation **is** named in the executable even though the files are not. The developer console
carries **command id 15, "Load ps2 savedata from slot: "**, and id 16, **"Convert PS2 Savedata"**
([console command names](../../00-Engine-Core-Runtime/Developer-Tuning-Console/console-command-names.md)).
Their labels sit at `008FD750` and `008FD770`, installed at context `+0x1A8` / `+0x1B0` by
`001D05E3` / `001D05F1` — `0x130 + 8 × id`, the console's own label indexing.

The route is inert, for a third reason:

* **id 16 has no body.** Its arm is `001D4BFA`, the shared do-nothing tail.
* **id 15 only edits a number.** Its arm steps `d+0xAA8` by 1 (`+0xC7` for the other direction) and
  reduces it **modulo 200** (`001D17EE`–`001D180D`).
* **Nothing consumes that number.** All 21 `.text` sites carrying the displacement `0xAA8` were
  classified: six are `sub`/`add rsp, 0xaa8` frame arithmetic, five are unrelated qword fields, four
  are the arm itself, one (`001CCBA3`) is the console context's zero-init, one is a mid-instruction
  match — and the single remaining **read** is `001CDB24`, which puts the value in a vararg slot for
  the row format `"%s%s %d"`. **The console prints the slot number and never passes it anywhere.**

So the label outlived its command. That does not weaken §3's conclusion, but it is a route the page
did not check, and it is the reason to believe `002EF300` is the loader these files were made for.

### ✔ New: `katano` is in the executable — as a source directory

Three `.rdata` literals name it: `..\..\katano\ateldecode.c` (`009156EE`),
`..\..\katano\atelload.c` (`00D1095E`), `..\..\katano\atelareaload.c` (`00D117FE`) — `__FILE__`
strings from the ATEL loader and decoder. The folder these saves sit in carries the same name as a
**build-tree directory of the ATEL sources**, so "a developer's folder" (§1) rests on the image and
not only on the archive path.

### Sharpened: the absence is stronger than §3 states, and the array claim is exact

§3 says the image contains neither `ff12savedata` nor `.sav` NUL-terminated. Measured over the whole
file, case-folded: **`.sav` occurs 0 times as a substring at all**, and `ff12savedata` 0 times —
against the controls `.bin\0` **2,144**, `.ebp\0` **10,380**, `npcdic` **10**, `musicctrl` **2**. So
no path *assembled at runtime* can end in `.sav` either, which the NUL-terminated form left open.

The kind-1 array claim reproduces exactly: at `01E19670`, indices **117–132** are
`listhelp_status.bin`, `listhelp_ability.bin`, `listhelp_eventitem.bin`, `listhelp_gambit.bin`,
`listhelp_targetchip.bin`, `listhelp_license.bin`, `menu_command_template.bin`, `menu_expansion.bin`,
`horidashi.bin`, `ability_data.bin`, `savemember_data.bin`, `saveparty_data.bin`, `word.bin`,
`menu00.bin`, `menu01.bin`, `menu02.bin`. The array has **one** rip-relative reference in the whole
image, `002DFC2B`, inside the case-dispatched installer that stores it into the global `0215F008`.

`002EF300` was re-read whole: the clamp is `cmovns` / `cmovg` against 15, the destination is
`002EF640()` — `lea rax, [02164280]`, the active buffer that `002EF650` zeroes for `0x56690` — and
the read length is the **immediate `0xE240`**. Generation A files are `0xE208`: **56 bytes shorter
than the fixed read**, and generations B and C are shorter still (`0xC200`, `0x5600`).

### A near-miss, recorded

My first offset control shifted **both** sides — clock at `+0x14`, time bytes at `+0x1C` — and
reported *0 of 8 disagree*, which reads as a pass. Both fields are zero there, so the control
decided nothing. The controls above each keep one side real; the `+0x14` control survives only
because the **stated** time is non-zero in all eight.

**Not claimed.** What generation B and C hold past the header. What the payload difference between a
23,152-byte and a 29,712-byte state block is, field by field — the sizes are read, the added fields
are not. Whether an image with the old size would be *accepted in practice*: the header check passes
and the version gate cannot distinguish them, but no load was executed and none can be here.
Whether `20050223` means anything beyond its value. Whether the console command ever had a body.

## 7. What this document does not claim

- [x] **SV-1.** The layouts of generation B (`FF12`-tagged) and generation C (zero header) **past the
      header**. `SV-1`, narrowed 2026-09-13: generation B's header ~~*is* generation A's from~~
      ~~`+0x08` on (§6)~~ follows generation A's map from `+0x08` on (§6) but carries none of its constants at `+0x58`–`+0x6C` *(corrected 2026-10-02, OPUS: zero in the shipped generation-B images, read through `vbf_read_entry`)*, and `+0x64` is the size of the block behind `02EBF190` — 23,152 in these
      images against 29,712 shipped, a real revision that nothing in the shipped build checks.
      **NARROWED FURTHER 2026-09-27 (OPUS): all three generations carry the party-stats array. The discriminator is the shipped record's own byte +4 (the definition row index), which runs 0..39 across consecutive records: generation A at image +0x2208 with stride 0x1C4, generation B at the same place (block +8 of the copy at payload +0x2000) with stride 0x190, generation C at image +0x15FC with stride 0x140 - 40 records in every image (the shipped array is BattleStatsRecord[40] at stride 0x1C8, which finds no run in generation A). Generation B's record ends at +0x190, where the shipped licencePoints field begins. CORRECTED the same day: the first narrowing below put 160 of the 6,560 extra bytes in a shipped tail +0x5A70..+0x5B10. In fact generation A's post-array fields (the slot maps, the source byte) sit 0xA0 = 40 x 4 lower than shipped, so the 160 B are the record growth (0x1C4 to 0x1C8) and the tail existed in development at +0x59D0..+0x5A70; 6,560 = 160 + 6,400 gambit bytes. Still open: which four bytes each record gained, the B and C records past the head, generation C's block framing, and what B and C hold after the array. Control _index/candidates/sv1-party-array/sv1_party_array.py (3 checks, FAILS 0; P3 rejects the tail reading).**
      **NARROWED 2026-09-27 (OPUS): the battle-state block's extra 6,560 bytes are located. In the shipped layout (the type store's BattleSystemState rows) ~~the bytes past the development size +0x5A70 are the slot-map / sequence / transition / result-echo tail (+0x5A70..+0x5B10, 160 B) and~~ *(CORRECTED 2026-09-27, OPUS: those 160 B are the stats-record growth, 40 x 4; see the narrowing above)* the bytes past it include the gambit configuration: gambitBanks GambitConfig[120] at +0x5B10 (6,240 B) and gambitSelectedBank int32[40] at +0x7370 (160 B). So 6,400 of the 6,560 are gambit data. In all four generation-A images the battle-state mirror (payload +0x2000) is zero from block +0x5A05 on, consistent with a 0x5A70-byte block. Their CRC slots +0x0 / +0xE200 are zero, so they were never checksummed. Not claimed: whether the development build kept gambits elsewhere or not at all. Still open: generations B and C past the header. Control _index/candidates/sv1-battle-block-tail/sv1_battle_block_tail.py (4 checks, FAILS 0).**
      *SUPERSEDED 2026-09-27 (FABLE, Claude Opus 5.5) in the register (OPUS, cd73ae1d5) under FRONTIER's scope ruling (Extension 2026-09-27c): everything the row asked about the shipped record is answered; the residue lies in development images no shipped loader opens and is carried by the sv1 instruments. Ticked on OPUS-NOTICE-FABLE-TICK-FIVE-SUPERSEDED-BOXES.*
- [x] **UQ-269.** What the extra 6,560 bytes of the runtime state block are. The two sizes are read; the
      fields between them are not.
      *SUPERSEDED 2026-09-26 (FABLE, Claude Opus 5.5), as FRONTIER ruled (FABLE-REQ-FRONTIER-SCOPE-OR-PROCESS-DISPOSITION-RULES):
      the row is replaced by the writer census it named. That census is [the battle-state block field map](../../11-Party/Battle-State-Block/the-battle-state-block-field-map.md)
      over all 0x7410 bytes, with its accesses table. Which of those bytes are the extra ones cannot be labelled from
      this image, because nothing in it knows the older layout.*
- [x] **UQ-270.** Whether the console's “Convert PS2 Savedata” command ever had a body. Its arm is the *(NO ADMISSIBLE SOURCE, reviewed and signed 2026-09-26 by OPUS; see the register row UQ-270.)*
      shared do-nothing tail in this build; nothing here says what it was.
      *Narrowed 2026-09-22 (FABLE) — **the historical half stays unanswerable from this image, but there IS a
      candidate elsewhere, and its independence is the point.*** Re-read: id 16's arm `001D4BFA` is the dispatcher's
      **own epilogue**, which [the arm catalogue](../../00-Engine-Core-Runtime/Developer-Tuning-Console/arm-catalogue-slice-A-ids-12-43.md)
      already records as *“both the unimplemented-id target and the common tail most real arms jump to”*; its
      sibling id 15 has a real body that only steps a counter modulo 200. **Neither command loads or converts
      anything.** Separately, a **real PS2-oldsave reading path does exist in the image**: the branch in `00408C30`
      that formats `PS2Data//oldsave//` + `%snew%03d` and opens the result
      ([the config page](../Game-Settings-Config/ff12config-and-debglobal.md)). **It is dead for an entirely
      unrelated reason** — `01E02810` is statically `-1`, so the `js` at `00408DD5` skips the whole branch — and
      **it is not reachable from the console at all**: `00408C30` has exactly one caller, `003692D0`, and the
      console dispatcher `001D1660` contains **zero** references to it.
      **What this does and does not license.** It gives *“nothing here says what it was”* a bounded candidate for
      what a PS2-savedata operation looked like in this codebase, and it shows the two dead mechanisms are
      independent rather than two views of one. **It is not evidence that id 16 ever drove that path, or that it
      ever had a body** — the surviving branch reads old saves, which fits id 15's *“Load ps2 savedata from
      slot:”* better than id 16's *“Convert”*, and no call edge connects either command to it. The box stays
      open.*

## 8. Related

- [The save image: buffers, header and payload](save-image-buffers-header-and-payload.md) — the layout generation A matches.
- [Console command names](../../00-Engine-Core-Runtime/Developer-Tuning-Console/console-command-names.md) — ids 15 and 16 name this operation.
- [The battle runtime-mode ladder](../../00-Engine-Core-Runtime/Battle-Runtime-Mode/battle-runtime-mode-ladder.md) — the `02EBF190` block whose size `+0x64` records.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. The image-address resolver fan-out is MECHANICAL.*

**ActorEntity — SERVICE.** The `debug_loadjfdata` handler `0050D9A0` calls a 96-byte actor helper after popping its
argument. Which actor state it touches is not read here.

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **CoreRuntimeScheduling — CLIENT.** `SaveRuntime_ResetActiveImageAndRebindState` is called by a 255-byte boot-mode body, so the active save image is reset as part of core boot.

### One edge added 2026-09-22 (FABLE), dispositioned rather than left to the count

`UQ-270`'s narrowing above cites `00408C30`, and that citation brings **one new edge** into a layer this
page already leaves unaccounted: `00408C30 callee 00862A20`, owned by **PlatformOnlineAchievements**.
**Nothing about that layer is claimed here.** The citation exists to say where a dead PS2-oldsave reading
path lives and that the console cannot reach it; the callee is one of that body's own, and neither it nor
its layer bears on the claim. *Recorded because the pre-check counts layers, not edges, and an edge that slips in under an
unchanged count is exactly what a diff of counts would miss — this one was caught by diffing the edges.*

*Measured, and stated no more strongly than that: the unaccounted set after this edit is a **strict subset**
of the set before it, so this edit introduces **no new unaccounted layer**. The set also got smaller, from five
to three, for a reason this pass did **not** establish — `audit_crossrefs.doc_accounts_for` returns `False` for
both departed layers on **both** versions of this page, so the paragraph above is not what discharged them and
no credit for it is claimed here.*

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Audio — SERVICE.** `002DDE60` on this page calls a **34-byte** Audio-owned body. What it reaches is
a clamp-and-forward: it forces a negative argument to `0`, caps it at `2`, loads a handle from
`0215EF44` and tail-jumps onward with the clamped index. **The crossing is that one call, not a
shared responsibility**, and its own callee is not named, per the 2026-09-16 refinement of the
crossing rule.

**Input — SERVICE.** `002DDE60` also calls **two 46-byte Input-owned bodies that are twins**: each
takes a byte argument, resolves a handle through the same accessor, returns early when it is null,
and otherwise tail-jumps onward with the byte. **They differ only in their final target**, which is
why both edges exist rather than one. Neither is read further, and neither of their callees is named.

*Read from the shipping bytes 2026-09-16 (FABLE), closing two of the five pass-22 findings `OPUS`
measured RED at `HEAD`. `002DDE60` is cited on this page for the `+0x3244` / `+0x3245` clearing
sequence; these three edges are its business rather than this document's, and the pass-22 rule is
that naming the caller obliges the sentence.*

**Presentation — SERVICE (SWE2-EC7-159, 6 edges).** Batch-124's `001EA1E0` names its caller
`001D0390`, which itself calls `001CD0E0` and is called by `001CCB20`; `001D1660` calls
`001C7360`/`001C752x` — Presentation-tagged helpers the debug-save enumerator neighbours. Shared
helper exchange, not a save-layout responsibility.

**Resource — SERVICE.** `001C26B0`/`001C19A0`/`001C2720`, the record-convert and base helpers this page's `001EA6C0` entry names, are also invoked from the resource layer (`00597970`/`00597A70`/`0059ED70`/`0059EE10` and siblings) - a shared-helper crossing the save-image page borrows; it owns no resource-table state.
- **PlatformOnlineAchievements - SERVICE (2 edges).** `00408C30`, `00862A20` reach bodies filed to platform/online achievements: `00862A20`, `00862A40` - shared machinery across the layer boundary, no shared ownership.
- **Script_VM_Native_Bridge - CLIENT and SERVICE (2 edges).** `002EF300` is also called by bodies filed to script VM / native bridge: `0050D9A0`; `0050D9A0` reaches bodies filed to script VM / native bridge: `00267E10` - shared machinery across the layer boundary, no shared ownership.
- **WorldAreaField - CLIENT (3 edges).** `002EF640` is also called by bodies filed to world area: `00229B40`, `003145E0`, `005843E0` - shared machinery across the layer boundary, no shared ownership.
## The `00253A80` exclusive subtree — all 4 members bound (SWE2-FRONTIER, followup queue)

`SaveRuntime_InitializeHeaderAndImageBackedState` (`00253A80`, 265 B) is the
initializer whose header writes §6 already tabulates. The full body adds the
state-block side of the same reset: `memset([02092758], 0, 0x58)` and
`memset([020927C0], 0, 0x4818)` open it — the `020927C0` block is the
image-backed runtime state whose size the header's `+0x6C` records — and after the
`002EF640`-based header stores (`+0x58`–`+0x6C`) it runs `00253240(i, 1)` for
`i` = 0–0xB (twelve per-slot inits), keeps bit 0 of `020927C0 + 0x3244` while
clearing the rest and clears bit 0 of `+0x3245`, calls `002DDE60`, zeroes
`+0x30` for `0x1F4`, `+0x3244` for `0x80`, and `+0x32C4` for a qword on the same
block, asserts through `0016D6A0`, and tails into a `0x3020`-byte memset at
`020927C0 + 0x224`.

| member | role | interior |
| --- | --- | --- |
| `002EF2A0` (6 B) | `SaveImage_GetHeaderDword58Constant` — returns `0x20050223`, the write-once version dword | — |
| `002EF290` (6 B) | `SaveImage_GetHeaderDword5CConstant` — returns `0x1538`, the `+0x200` region size §6 identifies | — |
| `00235E90` (6 B) | `SaveImage_GetHeaderDword60Constant` — returns `0x5071901`, the battle-state block's magic | — |
| `00235E80` (6 B) | `SaveImage_GetHeaderDword64Constant` — returns `0x7410`, the battle-state block's shipped size (29,712) | — |

All four are single-`mov` constant getters whose only caller is this root —
exactly the census §6's table predicts. Shared callees outside the census:
`00861EC0` (memset), `002EF640` (active-buffer base `02164280`), `00253240`
(per-slot init), `002DDE60`, `0016D6A0` (assert). The `+0x3244`/`+0x3245`
bit-pair and the `00253240` slot loop's target are left as recorded unknowns.

`001EA1E0` (408 B) is the counted table walk `001D0390`/`001EA380` call: `dword[rcx+0x28] & 0x7FFFFFFF` counts `[rcx+0x30]` elements, `01CEB638` supplies the stride base, `0017D260` resolves each entry, `00861EBA` copies, `00584730` stores, `001EA6C0` finishes - the debug save's element enumerator.

Interior anchor `001EA295` (function `001EA1E0`).

`001EA6C0` (174 B) is the bucketed push `001EA1E0` runs per savedata entry: `esi = [rcx] & ~0x80000000` is the count and `rdx = [rcx+8]` the base array; `001C19A0(rbx)` resolves the row, `rbx + esi*8` addresses the free slot, `001C26B0` converts the `[r15]` value (low-bit-adjusted) into the stored pointer, a moved base with the sign bit set runs `001C2720`, and the commit writes `[rdi+8] = rbx`, `[rdi] = esi+1` - `0` on success, `0xD` when `rdx` is null

Interior anchor `001EA708` (function `001EA6C0`).

## Interior citations for the entry-cited functions (OPUS, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-katano-debug-savedata-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `001EA380` | 64 B | when `edx` is below (unsigned) dword `+0x28` of `rcx` with bit 31 cleared, calls `001EAD40(qword +0x30 + edx*8, r8)` (`edx` zero-extended) and sets byte `+0xE8` to 1; otherwise it tail-jumps to `001EA1E0(rcx, r8)` | `001EA38C`, `001EA392`, `001EA3A1`, `001EA3A6`, `001EA3BB` |
