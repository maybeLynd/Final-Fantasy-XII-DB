---
system: The `sloc` menu-map container — world map images, routes and their world origins
category: 02-Resource-And-Asset-Pipeline
status: AUDITED
owner_layer: CodeDomain:Presentation.Map
evidence_tier: 1
verified_against:
  gzf_sha256: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity across GN160 -> GN161 - this document cites none of the 109 functions batch R109 touched, so every per-function record it rests on is byte-identical in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md (six ledger figures re-derived)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  snapshot_sha256: b57264ba73231665bf226da6d5761feee72df36c5999fc68ae14adfdd18fea34
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  parent_tag: GN160
corpus_validated: "52 of 52 sloc units (436 files across 9 locales), 2026-09-05"
container_format: sloc
last_reviewed: 2026-09-05
archive_formats:
  - "sloc | explained | menumap_sub##.bin and the four unnamed menumap_sub##_e# variants (.bin member, 52 units): layout section 2, consumer 00379870 reads the NPS2 record origin/extent through the 02ADD030 table, section 3"
audit:
  passes: 1
  last_pass: 2026-09-06
  last_pass_state: GN160-corpus-and-code-reparse-repos-1e — all 436 entries re-detected across every extension, 52 units decompressed and re-parsed, FUN_00379870 re-decoded; 14/14 corpus figures exact and the dead-branch correction confirmed from 430/430 NPS2 tags
  crossref_clean: true
  reopened_count: 0
---

# The `sloc` menu-map container

> **The map screen.** Fifty-two files holding every detailed area map the game draws, the walking
> routes marked on them, and — the part that makes the maps usable — the world-space origin that
> says where each picture sits in the world.

**Corpus validation, before anything else.**

| | |
|---|---|
| files examined | **436** — 52 logical units across 9 locale copies |
| units | **52**: `menumap_sub00` … `menumap_sub47`, plus four `_e3` variants (`sub01`, `sub07`, `sub25`, `sub26`) |
| magic `sloc` at `+0x00` | **52 / 52** |
| size | **1,049,520 B – 11,544,192 B** — ~~4.5 GB of `.bin` in total~~ 2.41 GB over the 436 copies *(corrected 2026-10-02, OPUS: the archive index; every `.bin` in the archive totals 2.48 GB)*, the largest thing under `ps2data/image` |
| directory entries | **424** across the 52 units |
| `NPS2` records | **430**, stride 32, in 52 / 52 |

> **48 base sublocations plus 4 alternates.** `menumap_location.bin` (`lmap`) carries **48**
> sublocation records, which is exactly the count of non-`_e3` units here.

---

## 1. What the player sees

**Open the map from the menu and this is the picture.** The drawn plan of the Westersand, the
Sandsea, Giruvegan — the detailed area map with its walkable corridors, its chambers, and the pale
lines showing the routes out to neighbouring areas.

Three separate things have to be right for that screen to work, and all three ship in this one file:

- **the picture** — a `TIM2` image, the PS2 texture format, one per map;
- **the routes** — `LCMPOS1` records, polylines in *world* coordinates tracing the exits;
- **where the picture is** — a 32-byte `NPS2` record per image giving the world-space origin of its
  top-left corner and how much world the image covers.

The third is what turns a picture into a map. Without it the game could draw the plan but could not
put your party marker anywhere on it. **The engine converts at a fixed four image pixels per world
unit**, so a marker at world `(x, z)` lands at `4 * (x - originX)`, `4 * (z - originZ)`.

**A few maps have no route lines** — five of the 424 records are not routes at all (§5), and four
images in the whole corpus have no map record pointing at them.

## 2. The layout

**All offsets are from the start of the file.**

### 2.1 Header — ~~16 bytes~~ 20 bytes (`0x14`), then the directory *(corrected 2026-10-02, OPUS: the struct below and the directory at `+0x14`)*

```struct SlocHeader base=file size=0x14
+0x00  char[4]  magic        'sloc' - bytes 73 6C 6F 63, in 52 of 52
+0x04  u32      version      100 in 52 of 52
+0x08  u16      dirOffset    16 in 52 of 52 - the directory begins at +0x14, see below
+0x0A  u16      recordEnd    end of the record area, relative to +0x20
+0x0C  u32      _reserved0   0 in 52 of 52
+0x10  u32      recordCount  2 .. 17 observed
```

### 2.2 Directory — `recordCount` u16 offsets at `+0x14`

```struct SlocDirEntry base=record size=0x2
+0x00  u16  recordOffset  record position, relative to +0x20
```

**A record's absolute position is `0x20 + recordOffset`.** Measured over **all 424 entries in all 52
units**: every offset lands inside the file, and within each unit the offsets are **strictly
ascending and distinct — 52 / 52**.

> **The `+0x20` base is not the directory's end.** For a 7-record unit the directory occupies
> `0x14 … 0x22`, which runs *past* `0x20`. So the base is a fixed constant, not "wherever the
> directory happens to stop", and a reader that computes it from the count will be wrong for any
> unit with more than six records.

### 2.3 Record area, then images, then the `NPS2` tail

```
0x20 + recordOffset[i]   ->  record i        (LCMPOS1 | NAVIICN2 | untagged, see §5)
0x20 + recordEnd         ->  end of records; images follow after 16-byte-aligned padding
   ... TIM2 images ...
   NPS2[]                    32 bytes each, one per image, running to EOF
```

- **`0x20 + recordEnd` lands at or before the first `TIM2` in 52 / 52**, with a gap that is always a
  multiple of 16 and never more than 192 bytes — alignment padding.
- **`NPS2` records are stride 32 in 52 / 52**, and **the last one ends exactly at EOF in 52 / 52**.
  The tail runs to the end of the file with nothing after it.

## 3. The loader contract

**`FUN_00379870` at `0x00379870` is the runtime consumer of the `NPS2` record**, and its complete
body is 24 instructions. It is what turns a sublocation id into a world-to-image transform.

```
0x00379877  lea    rcx, [rip + 0x27637b2]      -> 0x02ADD030, the per-sublocation record table
0x00379888  mov    rcx, [rcx + rax*8]          index by the sublocation id in ecx
0x0037988C  test   rcx, rcx / je 0x3798c4      no record -> the null branch
0x00379891  cmp    byte ptr [rcx + 3], 0x31    the TAG'S FOURTH BYTE against '1'
0x0037989F  movss  xmm0, [rcx + 0x10]          originX
0x003798A7  movss  xmm1, [rcx + 0x14]          originZ
0x003798AE  movss  xmm6, [rcx + 0x18]          extent X   (the '1' test FAILED)
0x003798B3  movss  xmm7, [rcx + 0x1c]          extent Z
0x003798D5  call   0x3c6360                    consume origin
0x003798F0  jmp    0x3c6380                    tail-call, consume extent as two ints
```

| Field | Read by | Rejected if | Clamped to | Inert |
|---|---|---|---|---|
| `sloc` magic `+0x00` | — | **never** | — | **yes** — `sloc` occurs **0 times in the image**, as ASCII or as the dword `0x636F6C73` |
| `sloc` `+0x04` version `100` | — | — | — | **no reader found** |
| `NPS2` tag byte `+3` | `0x00379891` | — | — | — |
| `NPS2` `+0x10` originX | `0x0037989F` / `0x003798B8` | — | — | — |
| `NPS2` `+0x14` originZ | `0x003798A7` / `0x003798BD` | — | — | — |
| `NPS2` `+0x18` / `+0x1C` extent | `0x003798AE` / `0x003798B3` | — | — | — |
| the whole record | — | **a null table slot** → origin `(0,0)`, extent `256.0` (`0x003798C4`) | — | — |

### The version test is checked against `'1'`, and no shipped record satisfies it

The compare at `0x00379891` is **`cmp byte ptr [rcx + 3], 0x31`** — ASCII **`'1'`**. `NPS2`'s fourth
byte is `'2'`.

> **So every shipped record fails that test and takes the else-branch.** `NPS2` is the *fallthrough*,
> not the tested-for case. **The `'1'` branch is dead code in this build**: it would read the origin
> from the same place but substitute a **hard-coded extent of `256.0`** (the constant at
> `0x00915A00`) instead of reading `+0x18`/`+0x1C`.

Measured over the whole corpus: **430 `NPS` records, 430 of them `NPS2`, zero tagged `…1`.** The
branch is a legacy `NPS1` path retained in code with no data to reach it.

**This corrects an existing project note.** `agent_flow/tools/lcmpos_decode_progress.md` describes
the check as *"the magic byte +3 is the tag's '2'"*. The instruction tests for `'1'`, and the
difference matters to anyone editing a record: **changing the tag's last byte to `'1'` does not
select a variant — it discards the per-record extent and substitutes 256.0.**

### The transform, and where it comes from

`px = 4 * (worldX - originX)` and `py = 4 * (worldZ - originZ)`, at exactly **four image pixels per
world unit**. **This is inherited, not derived here** — it comes from the prior work cited in §8,
which established it from `FUN_003C6420` and **confirmed it at runtime** via a live DLL harvest.
This sheet re-derives the *record* side (the table at `0x02ADD030`, the field offsets, the version
test) at tier 1, and cites the pixel ratio as tier 10 from that work.

**The write path: there is none.** Nothing writes a `sloc` file; these are authored offline.

## 4. Key addresses

| Address | Role | Read? |
|---|---|---|
| `0x00379870` | the `NPS2` consumer — sublocation id to world-to-image transform | ✅ complete body, 24 instructions |
| `0x00379877` | `lea rcx, [rip + 0x27637b2]` → the record table at `0x02ADD030` | ✅ |
| `0x00379888` | `mov rcx, [rcx + rax*8]` — index by sublocation id | ✅ |
| `0x00379891` | `cmp byte ptr [rcx+3], 0x31` — the version test, against `'1'` | ✅ |
| `0x003798AE` / `0x003798B3` | the per-record extent reads, the branch every shipped record takes | ✅ |
| `0x003798C4` | the null branch — extent `256.0` | ✅ |
| `0x00915A00` | the `256.0` default extent constant | data |
| `0x02ADD030` | per-sublocation `NPS2` record pointer table | data |
| `0x003C6360` / `0x003C6380` | the origin and extent consumers | ❌ not read here |

## 5. Corpus survey

**Invariants — measured over all 52 units.**

| | |
|---|---|
| `sloc` magic, `version` 100, `+0x08` = 16, `+0x0C` = 0 | **52 / 52** each |
| directory offsets ascending, distinct, in range | **52 / 52 units, 424 / 424 entries** |
| `0x20 + recordEnd` at or before the first `TIM2` | **52 / 52** |
| `NPS2` stride 32 | **52 / 52** |
| last `NPS2` ends exactly at EOF | **52 / 52** |

### Not every record is a route

Of the **424** directory entries:

| record | count |
|---|---:|
| `LCMPOS1` | **419** |
| `NAVIICN2` | **4** — `sub29` entry 13, `sub39` entries 1 and 6, `sub44` entry 0 |
| untagged | **1** — `sub10` entry 3, beginning `04 00 24 00 40 00 00 00` |

**Prior work recorded that "five extracted maps have no usable LCMPOS path" and left it there. These
are those five, and they are not empty** — four carry a `NAVIICN2` record instead and one carries an
untagged record. **The directory does not promise a route; it promises a record.**

### Four images have no record

`recordCount` is less than the `TIM2` count in exactly three units: **`sub02` (17 vs 18), `sub07`
(15 vs 17), `sub31` (12 vs 13)** — four orphan images in total.

> **This reproduces a prior finding by a different instrument.** The prior work found the same
> orphans by pairing record→TIM2→NPS2 and reported that `0x13E`/`0x141`/`0x3D` had previously been
> given the *wrong* map. This sheet counted magics and compared against the header's own count, and
> lands on the same three units. **Two methods, one answer.**

### The `_e3` variants

Four units ship a second copy: `sub01_e3`, `sub07_e3`, `sub25_e3`, `sub26_e3`. Each is within 100
bytes of its base unit's size and carries the same record count. **What `_e3` selects is not
established** — `0xE3` is an area id in the prior work's worked example, which is suggestive and not
deciding. **PROPOSED-repos-c7-15.**

## 6. Falsification pass — 2026-09-05

| attack | result |
|---|---|
| Is `+0x14` a directory, or a coincidence of ascending numbers? | **`0x20 + offset` lands on a recognised record magic in 419 of 424 entries**, and the other 5 land on two other record types. A wrong base or stride would land in the middle of image data, not on tags. |
| Is the record base the directory's end? | **No, and assuming so breaks at 7+ records.** For `sub00` the directory runs to `0x22` and the base is `0x20`. Tested by prediction against actual magic positions, not by inspection. |
| Does the version test select `NPS2`? | **No — it tests for `'1'` and every shipped record is `'2'`.** 430 of 430. The prior note's description is corrected in §3. |
| Is the `'1'` branch reachable? | **Not by any shipped record.** Stated as *"no shipped record reaches it"*, not *"it is unreachable"* — a modder could tag one `NPS1` and would then get the 256.0 default. |
| Is the transform ratio re-derived here? | **No, and §3 says so.** It is inherited at tier 10 from runtime-confirmed prior work. Only the record side is tier 1 here. |
| Did the prior work's findings get assumed or checked? | **Checked, by a different method.** The orphan images and the five non-route records were both re-derived from magic counts against header counts, independently of their record-pairing route. |
| Could the decompiler have invented the `lea` target? | Every address in §3 and §4 is from **disassembly**; `0x00379877 + 7 + 0x27637b2 = 0x02ADD030` resolves by hand. |

**The killer observation.** The central claim is *"`+0x14` is a `u16` directory of record offsets
based at `+0x20`."* It dies if any offset lands outside the file, if any unit's offsets are not
ascending, or if the predicted positions miss the record tags. All three were tested on all 424
entries; 419 land on `LCMPOS1` and the remaining 5 on two other tags, none on nothing.

## 6b. Independent audit pass — 2026-09-06, `repos-1e`

**Method.** Every archive entry's first four bytes tested for the `sloc` magic — **all extensions,
not just `.bin`** — then all 52 units decompressed in full and re-parsed with a fresh reader.
`FUN_00379870` re-decoded with capstone. Program state: GN160 (`gzf fa0db293…`).

**Every corpus figure reproduces exactly.**

| claim | sheet | re-parse |
|---|---|---|
| files carrying the magic | 436 | **436**, and all 436 are `.bin` |
| logical units | 52 | **52 distinct basenames**, all under `worldmap` |
| `+0x04` version | 100 in 52 / 52 | **100 in 52 / 52** |
| `+0x08` `dirOffset` | 16 in 52 / 52 | **16 in 52 / 52** |
| `+0x0C` `_reserved0` | 0 in 52 / 52 | **0 in 52 / 52** |
| `+0x10` `recordCount` | 2 … 17 | **2 … 17** |
| directory entries | **424** across 52 units | **424** |
| offsets strictly ascending and distinct | 52 / 52 | **52 / 52** |
| `0x20 + recordOffset` inside the file | 52 / 52 | **52 / 52** |
| `0x20 + recordEnd` at or before the first `TIM2` | 52 / 52 | **52 / 52** |
| `NPS2` records | **430** | **430** |
| `NPS2` stride 32 | 52 / 52 | **52 / 52** |
| last `NPS2` ends exactly at EOF | 52 / 52 | **52 / 52** |
| size range | 1,049,520 – 11,544,192 | **identical** |

**The consumer reproduces instruction for instruction.** `0x00379877 lea rcx,[rip+0x27637b2]`
resolves to `0x02ADD030`; the null branch, the tag test, and all four `movss` field reads are at the
cited addresses with the cited displacements.

**The dead-branch correction is confirmed independently.** `0x00379891` compares the tag's **fourth
byte** against `0x31` (`'1'`), and reading the tag of every one of the **430** tail records gives
**430 `NPS2`, zero `…1`** — so the compare fails for every shipped record and
`0x00379897 … 0x003798AC` is unreachable on shipped data. **§3 already states this measurement and
this conclusion**; a second reader with a different parser now gets the same 430/430, which is what
the row was worth checking for. *(I first drafted this as "now has a measured denominator rather
than an inference" — it already had one. **Second time this pass that I nearly claimed as a
contribution something the sheet already said**, after the `0x01EFF3B0` global in the `efx` sheet.
An auditor's addition has to be grepped against the document before it is written down.)*

### The auditor's parse was wrong twice before it was right

My first re-parse reported **381 files, 45 units, 178,928 directory entries and 336 `NPS2`** — four
figures, all wrong, and wrong in a way that looked like a format sheet failing badly.

- **381 / 45:** I filtered to `.bin` *and* tested the magic against a truncated block-0 read, missing
  55 files.
- **178,928 / 336:** I put `recordCount` at `+0x0A` and read the directory as `u32`. §2.1 says
  `recordCount` is the **`u32` at `+0x10`** and the entries are **`u16` at `+0x14`, relative to
  `+0x20`** — all three stated in the fence and the sentence under it.

> **This is the fourth time in this session's audits that a disagreement was the auditor's
> instrument**, after a vacuously-sorted empty list, an unscoped count, and reading a `u32` offset
> table as `u16`. **The rule that keeps earning itself: a re-parse that disagrees is evidence about
> the parser until the layout has been read, not skimmed** — and the more dramatic the disagreement,
> the more likely it is the reader. A sheet does not usually miss its own record count by a factor of
> 400.

**What was attacked and held.** (a) That `+0x20` might really be the directory's end for small units
— it is not; units with more than six records have a directory that runs past `0x20`, and the base
is still `0x20`. (b) That the `NPS2` tail might contain a second tag family — it does not, 430 of 430.
(c) That some `sloc` unit might ship under a non-`.bin` extension — none does, tested across every
entry in the archive.

**Not audited:** the `TIM2` image payloads and the `LCMPOS1`/`NAVIICN2` record bodies, which §7
already scopes out.

## 7. What this document does not claim

- **The `LCMPOS1` record layout.** Prior work gives it as aligned `{float x, float y, float z, u32
  pad}` polylines; this sheet does not re-derive it and does not restate it as established here.
- **What `NAVIICN2` is.** Four records, tag suggests navigation icons, and a tag is a weak
  instrument — this README's own category has two recorded misses from name-driven guesses.
- **What the untagged `sub10` record is.**
- **What `_e3` means.**
- **What `version = 100` gates.** Constant in 52/52 and no reader found, so nothing is known about
  what a different value would do.
- **What `recordEnd` is used for.** It is consistent with the image area's start in 52/52, but no
  code was found reading `+0x0A`.
- **The image side.** `TIM2` is the PS2 texture format and is documented as a candidate `standard`
  row in [`README.md`](README.md); this sheet documents the wrapper, not the images.

## 8. Related

- [`README.md`](README.md) — the `ps2data/image` long tail, which records that **`.bin` is the weak
  census row** and that `sloc` is one of the seven signatures found in it. *(corrected 2026-10-02, OPUS: the full census of 2026-09-19 in that README counts 26 magics over 178 of the 236 units, `st2e` the largest at 73 and `sloc` second at 52; the 28 below includes leading dwords that are not magics, such as `CCdd`)* **The `.bin` signature
  census has since measured 28 signatures over 236 logical units**
  (`Tools/work/formats/bin-signature-census.tsv`), and `sloc` is ~~the largest of them~~ the second largest, after `st2e`'s 73, at 52 units.
- `agent_flow/tools/lcmpos_decode_progress.md` — **the prior work this sheet builds on and partly
  corrects.** It establishes the `LCMPOS1` polyline layout, the 4 px/world-unit ratio and the `NPS2`
  field offsets, **confirmed at runtime** through a live DLL MapCalib harvest, and it records that
  an earlier heuristic origin solver was wrong (only 62 of 375 origins within 8 units of truth).
  **It is a tool progress note, not a database document** — treated here as a strong prior reading
  whose record-side claims were re-derived at tier 1 and one of whose statements is corrected in §3.
- `../../16-UI/` — the map screen that consumes the transform.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings become reportable once citations written 0x... or FUN_... count (R5); tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Presentation — CLIENT.** Cited container accessors (17, 31 and 1,864 bytes) are called by Presentation bodies of 133, 346 and 1,587 bytes.
- **WorldAreaField — CLIENT (2 edges).** 2 inbound (WorldAreaField bodies `00378120`, `00377400` call page-cited `00379870`). Substantive edges include `00379870` is called by `00378120`; `00379870` is called by `00377400`.

## Interior citations for the entry-cited functions (OPUS, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-sloc-menumap-container-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `00377400` | 54 B | returns without work unless `ecx` is 0 to 3 (unsigned compare); otherwise stores its low byte at `02ADD0E8`, calls `003C63A0` with the qword at `02ADD010 + ecx*8` and tail-jumps `00379870(ecx)` | `0037740C`, `00377415`, `0037741B`, `0037741F`, `0037742B` |

## Cross-subsystem neighbours of the interior rows (OPUS, 2026-10-02)

- **Script/VM native bridge — CLIENT (1 edge).** The 23-byte script verb `00356BF0` pops one operand through `00267E10` and tail-jumps into the row's `00377400` with it, so a script selects which of the four `02ADD010` entries is opened. Edge from `edges.tsv`; both bodies read.
