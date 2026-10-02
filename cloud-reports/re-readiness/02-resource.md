# Reconstruction readiness — `FFXII TZA/02-Resource-And-Asset-Pipeline/`

| | |
|---|---|
| Stream | R (reconstruction readiness), per [`docs/cloud-briefs/re-readiness.md`](../../docs/cloud-briefs/re-readiness.md) |
| Board task | `OPUS-CLOUD-R-READINESS-02-1002` |
| Date | 2026-10-02 |
| Snapshot | this repo's text snapshot at `f26c5667` only; no executable, Ghidra or live game was used |
| Status of this file | **draft / pointer**. Nothing here is evidence. Every item quotes or paraphrases a page and gives `page:line`. Text is quoted as the snapshot has it; several of these pages are being edited by other lanes. |

**Counts:**
- **Pages:** 59 `.md` pages read in full (26,673 lines). 23 `.tsv` + 1 `.json` member files checked for layout and
  counts only. One cited member file is missing (`LBB:36`).
- **Interface:** 81 entry-point rows mapped (§1.1).
- **Gaps:** 31 self-stated gaps (G-S1–G-S31) and 38 structural gaps (G-T1–G-T38).
- **Contradictions:** 179 in total.
  - **123 value-changing** (C-V1–C-V123), all marked "page-text only - needs local check". 29 have a favoured side
    settled by a dated correction on the pages: C-V7, C-V14, C-V15, C-V16, C-V21, C-V25, C-V31, C-V35, C-V36, C-V37,
    C-V38, C-V50, C-V57, C-V70, C-V71, C-V78, C-V84, C-V85, C-V87, C-V88, C-V89, C-V93, C-V103, C-V104, C-V105,
    C-V111, C-V114, C-V115, C-V119. The other 94 have no favoured side.
  - **56 stale / banner** (C-S1–C-S56).
- **Cross-checks:** 34 came out consistent.
- **Rating:** **NOT YET** overall. The core load path (archive → path → FST → queue → arena/codec → section lookup →
  registry) is **MOSTLY**. The EFX relocators, `.ard`/`.nmb`, text banks and four PS2-era format groups are
  **NOT YET** (§4).

Citation form: `ALIAS:line`, where the alias names a page inside `FFXII TZA/02-Resource-And-Asset-Pipeline/` (table
below). "Not stated" means no page in this folder says it. Where only another category's page makes a point, the
pointer is given as the 02 page cites it; that other page was not audited for this report.

## Pages read

All 59 `.md` pages were read in full (26,673 lines). Status is quoted from each page; "README" is the folder
`README.md`, which lists only five pages (`README:13-35`).

| alias | page | lines | status as the page states it |
|---|---|---:|---|
| README | `README.md` | 76 | index; `Functions \| 572` (`README:8`) |
| REG | `authored-data-table-registry.md` | 2279 | `status: DOCUMENTED` (`REG:4`, owner re-status 2026-10-01); body banner `**PARTIAL.**` (`REG:62`); README `**PARTIAL, tier 1.**` (`README:14`) |
| ROW | `CONTRACT-authored-table-row-lookup.md` | 1405 | `readiness: BEHAVIORALLY UNDERSTOOD`, `confidence: PROVEN` (`ROW:6-7`); `last_reviewed: 2026-09-11` (`ROW:17`); `crossref_clean: false` |
| EV | `authored-reference-lifetime-evidence.md` | 1560 | `status: "DOCUMENTED — evidence note …"` (`EV:4`); `last_reviewed: 2026-09-12` (`EV:15`) |
| RSA | `resource-section-addressing.md` | 901 | `status: DOCUMENTED` (`RSA:4`); README `**DOCUMENTED, tier 1.**` (`README:16`) |
| CSA | `CONTRACT-resource-section-addressing.md` | 256 | `readiness: CONTRACT READY`, `confidence: PROVEN` (`CSA:6-7`) |
| TREE | `CONTRACT-resource-entry-tree.md` | 506 | `readiness: BEHAVIORALLY UNDERSTOOD`, `confidence: PROVEN` (`TREE:6-7`); `last_reviewed: 2026-09-13` (`TREE:17`) |
| EFX | `CONTRACT-efx-source-rebase.md` | 954 | `readiness: BEHAVIORALLY UNDERSTOOD`, `confidence: PROVEN` (`EFX:6-7`); `last_reviewed: 2026-09-23` (`EFX:17`) |
| TL | `a-typed-list-measured-once-and-built-in-one-allocation.md` | 747 | `status: DOCUMENTED` (`TL:4`); `readiness: SEMANTICALLY IDENTIFIED` (`TL:8`) |
| RQ | `the-resource-request-queue.md` | 950 | `status: "PARTIAL — …"` (`RQ:4`); README `**PARTIAL, tier 1.**` (`README:21`) |
| RQC | `CONTRACT-resource-request-queue.md` | 385 | `readiness: BEHAVIORALLY UNDERSTOOD`, `confidence: PROVEN` (`RQC:6-7`) |
| ISR | `the-indexed-source-request-from-arm-to-terminal-pump.md` | 277 | `status: PARTIAL` (`ISR:4`) |
| OWNC | `CONTRACT-resource-input-ownership.md` | 490 | `readiness: CONTRACT READY`, `confidence: HIGH` (`OWNC:6-7`) |
| OWN | `the-resource-owner-from-copy-or-borrow-to-disposal.md` | 243 | `status: PARTIAL` (`OWN:4`) |
| EXT | `the-external-source-owner-and-borrowed-view-lifetime.md` | 289 | `status: PARTIAL` (`EXT:4`) |
| MOV | `the-source-block-mover-and-separate-consumer-refresh.md` | 208 | `status: DOCUMENTED …` (`MOV:4`); `external_production status: "locally validated; formal independent acceptance pending"` (`MOV:13`) |
| PRF | `the-nonempty-prf-registration-and-specialized-relocation.md` | 134 | `status: PARTIAL` (`PRF:4`) |
| ARDC | `CONTRACT-ard-area-binder.md` | 254 | `readiness: CONTRACT READY`, `confidence: PROVEN` (`ARDC:6-7`); `crossref_clean: false` (`ARDC:24`) |
| AEC | `Authored-Expressions/CONTRACT-authored-expression-evaluation.md` | 310 | `readiness: BEHAVIORALLY UNDERSTOOD`, `confidence: PROVEN` (`AEC:6-7`) |
| RND | `Authored-Expressions/how-an-authored-number-gets-its-randomness.md` | 851 | `status: AUDITED …` (`RND:4`); `last_reviewed: 2026-09-08` (`RND:17`) |
| VBF | `VBF-Archive-And-Authored-Tables/vbf-archive-and-st2e-tables.md` | 1294 | `status: DOCUMENTED - was REOPENED …` (`VBF:4`); README `**DOCUMENTED, tier 1.**` (`README:25`) |
| PATH | `VBF-Archive-And-Authored-Tables/how-a-path-is-resolved-to-bytes.md` | 369 | `status: DOCUMENTED - every §8 question is answered` (`PATH:4`) |
| BIG | `VBF-Archive-And-Authored-Tables/how-the-bigfile-index-loads-and-is-verified.md` | 477 | `status: DOCUMENTED` (`BIG:4`); body banner `**PARTIAL.**` (`BIG:36`) |
| BKT | `VBF-Archive-And-Authored-Tables/the-dat-and-bin-extension-buckets.md` | 190 | `status: DOCUMENTED` (`BKT:4`) |
| S2R | `VBF-Archive-And-Authored-Tables/St2e-Carriers/README.md` | 220 | no front matter |
| NMB | `…/St2e-Carriers/area-nmb-index.md` | 881 | `status: DOCUMENTED …` (`NMB:4`); `last_reviewed: 2026-09-04` (`NMB:19`) |
| BTB | `…/St2e-Carriers/battle-text-banks.md` | 538 | `status: AUDITED …` (`BTB:4`) |
| LDR | `…/St2e-Carriers/how-the-ard-loader-binds-area-battle-data.md` | 951 | `status: AUDITED` (`LDR:4`); `last_reviewed: 2026-09-04` (`LDR:19`) |
| PJR | `Prefetch-And-Json-Data/README.md` | 57 | no front matter |
| AH | `Prefetch-And-Json-Data/ah-asset-header-manifests.md` | 336 | `status: AUDITED` (`AH:4`) |
| PFM | `Prefetch-And-Json-Data/how-the-prefetch-manifests-are-read.md` | 364 | `status: AUDITED` (`PFM:4`) |
| TA | `Prefetch-And-Json-Data/ta-texture-animation-lists.md` | 690 | `status: AUDITED` (`TA:4`) |
| LFR | `Loose-Files-And-Size-Tables/README.md` | 38 | no front matter |
| FST | `Loose-Files-And-Size-Tables/file-size-tables-fst.md` | 412 | `status: AUDITED …` (`FST:4`) |
| SF | `Standard-Formats/shipped-standard-formats.md` | 375 | `status: AUDITED` (`SF:4`); README `**DOCUMENTED, tier 1.**` (`README:32`) |
| PR | `PS2-Image-Data-Formats/README.md` | 130 | no front matter; gives no per-page status |
| TIM2 | `PS2-…/tim2-images-and-the-seven-slot-registry.md` | 350 | `status: AUDITED` (`TIM2:4`) |
| LBB | `PS2-…/loader-bound-bin-families.md` | 744 | `status: DOCUMENTED` (`LBB:4`) |
| UBF | `PS2-…/unnamed-bin-families.md` | 279 | `status: AUDITED` (`UBF:4`) |
| FIVE | `PS2-…/five-small-bin-tables.md` | 573 | `status: DOCUMENTED — UQ-68 …` (`FIVE:4`) |
| MRP | `PS2-…/mrp-menu-resource-packages.md` | 246 | `status: DOCUMENTED …` (`MRP:4`) |
| AS7 | `PS2-…/as7-menu-graphics-containers.md` | 163 | `status: DOCUMENTED …` (`AS7:4`) |
| BTM | `PS2-…/btm-exfont-bitmaps.md` | 168 | `status: DOCUMENTED …` (`BTM:4`) |
| CL2 | `PS2-…/cl2-menu-colour-tables.md` | 196 | `status: DOCUMENTED …` (`CL2:4`) |
| AMAP | `PS2-…/amap-menumap-area-table.md` | 143 | `status: AUDITED` (`AMAP:4`) |
| BINM | `PS2-…/binmenu-guest-face-and-map-effect-images.md` | 214 | `status: AUDITED` (`BINM:4`) |
| CHSE | `PS2-…/chse-character-se-tables.md` | 377 | `status: DOCUMENTED …` (`CHSE:4`); body `**Status is \`PARTIAL\` for that reason**` (`CHSE:127`) |
| CMAP | `PS2-…/cmap-menumap-common-sublocation-directory.md` | 162 | `status: DOCUMENTED …` (`CMAP:4`) |
| GMAP | `PS2-…/gmap-menumap-guide-texts.md` | 126 | `status: AUDITED` (`GMAP:4`) |
| HCHK | `PS2-…/hchk-hctg-hdat-handbook-indexes.md` | 523 | `status: AUDITED` (`HCHK:4`) |
| HIMG | `PS2-…/himg-handbook-image-bundles.md` | 239 | `status: AUDITED` (`HIMG:4`) |
| LMAP | `PS2-…/lmap-menumap-location-graph.md` | 737 | `status: DOCUMENTED …` (`LMAP:4`) |
| LST | `PS2-…/lst-menuquest-list.md` | 171 | `status: DOCUMENTED …` (`LST:4`) |
| MQ | `PS2-…/menuquest-bin-quest-detail-tables.md` | 124 | `status: AUDITED` (`MQ:4`) |
| MG | `PS2-…/mg-worldmap-mesh.md` | 174 | `status: DOCUMENTED …` (`MG:4`) |
| SLOC | `PS2-…/sloc-menumap-container.md` | 348 | `status: AUDITED` (`SLOC:4`) |
| WMAP | `PS2-…/wmap-menumap-world-map-graph.md` | 219 | `status: DOCUMENTED …` (`WMAP:4`) |

Member files, checked for layout and counts only (no item below rests on a member file alone):

| file | what was checked |
|---|---|
| `VBF-…/members/constant-resource-requests.tsv` | header `api site function name kind id file via_caller_site`; **238 data rows**, 182 distinct sites, 147 with a file, 91 `-`, 66 with `via_caller_site` — agrees with `VBF:1138-1142` |
| `VBF-…/members/switch-family-record-store-5x.tsv` | 10 rows, cases `0x50`–`0x59`; **no page in the folder links it** |
| `authored-table-header-accesses.tsv` | 1,795 rows over 231 functions; seeded from 41 slots `0x02EBF008`–`0x150` minus `0x0D0` (fits `REG:897-898`); **no page links it** |
| `authored-table-registry-slot-accesses.tsv` | 5 rows, route `ARRAY 0x02EBF008 stride=0x8 count=64` — agrees with the 64-slot extent `REG:81` |
| `resource-request-slot-accesses.tsv` | pool route `022C31C0` + 64×`0x80`; seeds `0032E590` as a slot function although it takes an id (`RQ:317`), giving one spurious `disp 0x1` row |
| `indexed-external-source-request-accesses.tsv` | `stride=0x1C count=80` — agrees with `ISR:38-39` |
| `resource-kind-override-table-accesses.tsv` | 9 rows (8 qword stores + loop `lea`) — fits `RQ:73-74` |
| `resource-read-status-accesses.tsv` | 2 rows, `001D6DD4` / `001D6FF4` store `-1` — agrees with `RQ:710-712` |
| `resource-section-name-scratch-accesses.tsv` | 5 rows (4 qword zeroes, `[+0x1f]=0`) — agrees with `RSA:434-440` |
| `render-resource-entry-buffer-accesses.tsv` | 38 rows, all `EMBED RenderResourceEntry +0x10` (the `0x50` entry; see C-V5) |
| `render-stride-0e-lement-accesses.tsv` | 374 rows, all `bank=0xD98` — agrees with `RSA:325` |
| `image-address-arena-record-accesses*.tsv` | 41 rows, `022D7FD0 stride=0xA8 count=15` — agrees with `TREE:298` |
| `members/listtype-census*.tsv`, `members/atlas-name-census.tsv` | combined totals 344 blobs / 7,665 records / 30,546 items agree with `TL:343-344`; the atlas census disagrees with `TL:349-351` and `TL:370` (C-V27, C-V28) |
| `members/image_address_base_writer_bounds.json` | `01F83530` past raw `.data` end; `FFFB` replay — agrees with `TREE:87-98` |
| `Authored-Expressions/*.tsv` | 76 rows / 21 offsets / 5 functions and 25 rows / 6 offsets; **no page links either** |
| `PS2-…/members/bin-assembly-census.tsv` | 123 `[FMT-SITES]`, 2,144 `[BIN-STRINGS]`, header `assembly_fmts=142` — agrees with `UBF:242-250` |
| `PS2-…/members/hb-index-census.tsv` | 54 rows; `tag` = 102 in every row (see C-V40); monster `hdat_files` per locale 4–11 (see C-V39) |
| `PS2-…/members/mmsg-value-receiver-adapters.tsv` | 28 rows — agrees with `BINM:25` |
| `PS2-…/summon-effect-state-02b40508-accesses.tsv` | 3 rows in `003B54C0`; **no page links it** |
| `PS2-…/members/loader-bound-census.tsv` | **does not exist**, though `LBB:36` cites it (G-T36) |

---

## 1. Interface

The folder is the engine's file and data layer. It has six layers, each documented by its own pages:

1. **Archive and path layer** (VBF, PATH, BIG, BKT, FST, PFM): a 31 GB `SRYK` archive indexed by MD5 of the path, a
   RAM file cache keyed by a djb2-style hash, a 41-kind path directory, and per-locale file-size tables.
2. **Request queue** (RQ, RQC, ISR): every kind/id load goes through a 64-slot queue pumped by the frame, in 512 KB
   parts when a gate allows it.
3. **Arena, handle and image-address layer** (TREE, EV, EFX, MOV, OWN, OWNC, EXT, PRF): 15 arenas with `0x40`-byte
   block headers, a red-black tree per arena, tagged handles, and a 32-bit "image address" codec relative to a base at
   `01F83530`.
4. **Section addressing** (RSA, CSA): the tag + 32-byte-name lookup inside a loaded resource.
5. **Authored data tables** (REG, ROW, VBF §2/§7, BTB, ARDC, LDR, NMB): `st2e` tables bound into a 64-slot pointer
   array at `0x02EBF008`, area `.ard` files bound per area change, text banks.
6. **Formats** (TL, AEC/RND, PJR/AH/TA, SF, all PS2 pages): menu typed lists, authored expressions, prefetch/asset
   manifests, texture-animation lists, PS2-era `.bin`/`.dat` formats.

### 1.1 Entry points (functions, with their callers)

#### Archive, path and size

| function | role and callers as stated | cite |
|---|---|---|
| `001F4340` | BigFile opener, 991 B: reads the `SRYK` header and index, MD5-verifies the index; only caller `0019B070` | `BIG:59`, `BIG:214` |
| `0019B070` | allocates the `0xB0` archive object, calls the opener, frees it on `false`; one call site `0017CEF6` mounts `../FFXII_TZA.vbf` | `BIG:262`, `PATH:239` |
| `0019AEE0` / `001F47D0` | MD5 of the caller's path, then digest-tree lookup per mounted archive (compares `+0x18` then `+0x20`) | `BIG:243-245`, `PATH:193` |
| `00214FC0` / `00215290` / `00215110` | reader handle: construct (64 KiB cache) / `fopen` / read clamped to size; 15 pooled handles + one spare | `BIG:248-251`, `BIG:267` |
| `0019A770` / `0019A860` / `0019AA20` | read planner; blocks via CRT `fread` (`0019A8D1`), zlib 1.2.11 `uncompress` `0080C5A0` from `0019AAAE` | `BIG:171-172`, `BIG:268-270` |
| `00597970` | `PStreamReaderFile` constructor; vtable `00D26C90` (7 slots: dtor, Close, IsOpen, Rebind, Close-then-rebind, Read, Seek) | `PATH:45`, `PATH:63-69` |
| `0059EE90` | path resolver: route 1 (RAM cache) then route 2 (archive); 6 callers (5 Resource + Audio `00225BA0`) | `PATH:143-158`, `PATH:350` |
| `0020C440` / `00674A00` | route-1 key builder (uppercase, `\`, collapse) and hash (`0x1505`, ×`0x21`, `btr 0x1F`) | `PATH:169-176`, `PATH:352` |
| `002DF9A0` | `ResourcePath_Init`, 2,831 B: fills the 41-slot path directory `0215F000` per language; called once from `0022A0B0` | `VBF:310-311`, `FST:71` |
| `002DF980` | `ResourcePath_Get`, 22 B: `pathTables[kind][index]`, no bounds check | `NMB:114-123` |
| `002DF880` | `ResourcePath_Copy`: −1 on NULL | `NMB:139-142` |
| `002DF960` | FST size reader `(kind,id)`, 28 B | `FST:72`, `FST:106` |
| `0032E400` | size lookup: override `022C51F0[kind]` first, else `002DF960` via `0046DE70`; positive sizes rounded up to 64 | `FST:73`, `RQ:229-234` |
| `001DA0F0` / `001DA610` / `001DA290` / `001D9A40` | prefetch parser / `common.txt` init / per-map entry / `eventList.csv` | `PFM:77`, `PFM:119-121` |
| `001A7D50` / `001A8BA0` / `001A9770` | `.ta` discovery request / parser / chaining callback | `TA:85-108` |
| `00473E80` / `001D8D60` / `001EE820` | TGA loader (verb `0x5A2`) / decode / BGR→RGBA row copy | `SF:59-79` |

#### Request queue

| function | role | cite |
|---|---|---|
| `0032EA90` → `0032E450` | resource-system initialiser → pool build (64-slot links, counter = 1), then `003EB050`, then clear 256 overrides | `RQ:72-74`, `RQC:58`, `RQC:157-158` |
| `0032E620(kind, index, dest, bytes, &desc)` | builder, 340 B; rejects a negative index with `0xFFFFFFFF`; gate `003EB0D0()!=0` enables chunking | `RQ:86`, `RQC:59`, `RQ:249-251` |
| `0032E780` | head-insert wrapper, only caller `003EADE0` (BGM stream) | `RQ:485-487` |
| `0032E7B0` / `0032E7C0` | raw-path (kind `0xFF`) requester; 16 call sites (`003306E0`×10, `003319D0`×4, `00377DC0`×2) | `RQ:570-571`, `RQ:675-676` |
| `0032E870` | slot take, with the stall loop `0032E88D`–`0032E8C3` | `RQ:102-104`, `RQ:337` |
| `0032E990` / `0032EC40` | pop free head (no null guard) / release (sets `+0x64=-1`) | `RQC:62-63` |
| `0032E070` | pump, 605 B, six-entry jump table `0032E2D0` | `RQ:140-141`, `RQ:339` |
| `0032E040` | 38 B guarded kick: tail-jumps to the pump when `001EDE80()` or `0017D930()` is non-zero | `RQ:945-949`, `RQC:65` |
| `0032E520(arg)` | 0 = drain, non-zero = ask | `RQ:126-140` |
| `0032E4D0(id)` / `0032E590(id)` | in-flight query / cancel | `RQ:316-322` |
| `0032E330` / `0032E370` / `0032E3B0` / `0032E2F0` | delivery / error / part / cancel callback sites | `RQ:341` |
| `0046E030` → `002DF780`; `002DF6C0` | read issue (kind ≠ FF) / kind FF | `RQ:343-344`, `RQ:145` |
| `003DDA20` / `003DD4C0` / `003DD850` / `003DD420` | indexed external source: arm / produce / complete / delete | `ISR:65-70`, `EXT:93-98` |

#### Arena, handles, image address

| function | role | cite |
|---|---|---|
| `00369D30(id, backing, size, count)` | arena init (ids ≤ 14), header via `0036A490`; boot table of 9 arenas from `0022A0B0` | `EV:351-361`, `EV:392-400` |
| `0036BC60` | allocator, 887 B; 64-byte rounding; header `0x40`; returns `block+0x40` | `EV:229-244` |
| `0036A100` / `0036A190` | allocate with selected arena (direction 0 / 1); retry via `0036BFE0` | `EV:224-227` |
| `0036C660` | prefix tagger (7-byte name, tag at header `+0x1E`) | `EV:179-197`, `EV:1494-1508` |
| `00369860` / `003697F0` / `00369800` | free (1,009 B) / raw release / tagged release | `EV:1202-1222`, `OWN:140-142` |
| `0036AF20` / `0036B130` | issue handle `slot|3` / resolve `[slot+8]+0x40` (41 B) | `EV:561-569`, `EFX:80-87` |
| `0036D170` → `0036B410` → `0036B4E0` | tree add (membership bit set) / insert / walk | `TREE:112`, `TREE:139-143` |
| `003AB880` → `0036A000` → `0036C790` | tree remove (pin) / generation check + remove / rebalance (359 B) | `TREE:176-193`, `TREE:222-223` |
| `003AB940` | tree add (unpin) | `TREE:9`, `OWNC:169-170` |
| `0020E600` / `0020E620` | image-address decode `uint64(base + uint32(ref))` / encode `low32(p) − low32(base)`; base qword `01F83530` | `ROW:52`, `ROW:76-78`, `EV:264-266` |
| `003AB7F0` | handle resolver used by every mode-1 consumer | `EFX:89-95`, `RSA:198-201` |
| `00369C60` / `0036A2A0` / `003B3C00` | compaction / mover / deferred child entry (bounds `0..0xA`) | `MOV:36-47`, `EFX:282-284` |
| `003B3480` → `0024D970` → `003AA3D0`, `003A9BA0`, `003A9860`; `0024D940` → `003A8FF0` | EFX source rebase (delta = `sext32(low32(new) − low32(old))`) | `EFX:46-55`, `EFX:143-146`, `EFX:458-461` |
| `0024D540` | combined walk, called from main-loop frame functions (see C-V18) | `EFX:476-481`, `EV:1455-1456` |
| `003EDAD0(input, len32)` | copy (mask 4 clear) or borrow (mask 4 set) of an EFX input | `OWNC:423-431` |
| `00409780` | `@FRP` (`0x50524640`) child/name lookup: index and offset outputs, both −1 initially | `PRF:34-37`, `CSA:121-126` |

#### Section addressing

| function | name | size | cite |
|---|---|---|---|
| `00409C30` | `ResourceSectionHeader_MatchesTagAndName32` | 101 B | `CSA:52` |
| `00409660` | `ResourceEntry_FindSectionPointerByTagAndName` | 89 B | `CSA:53` |
| `004096C0` | `ResourceEntry_ResolveSectionOffset`; 17 call sites in 11 functions | 41 B | `CSA:54`, `RSA:555` |
| `00409600` | `ResourceEntry_GetResolvedBasePointer`; 4 callers | 86 B | `CSA:55`, `RSA:620` |
| `00409210` | name normaliser into scratch `02B62E20` (31-char limit) | — | `RSA:434-440` |
| `00409A60` | setup (mode 0 copy / mode 1 keep) | — | `OWN:48-51`, `RSA:139` |
| `0041E500` | sole writer of the re-resolve flag `02B62E10` | — | `RSA:589-593` |
| `0051F9F0` | descriptor geometry writer (`bankShift` 5 everywhere) | — | `RSA:672-684` |

#### Authored tables, area data, text

| function | role | cite |
|---|---|---|
| `002368D0` `BattleStorage_InitializeWorkArrays` | registers loader `0x13` `"STATIC"` with delivery stub `00238850`; clears and requests the 12 boards | `ROW:841-844`, `REG:2003-2009` |
| `00238850` → `00236C30(1)` | STATIC delivery: binds `0208E680`, then 33×`003845F0` + 2×`003846F0` + five member binders + two raw stores | `ROW:308-309`, `ROW:1120-1128`, `REG:465-468` |
| `003845F0` `AreaData_BindAndRebaseSectionDescriptor` | 252 B: `*slot = desc`; rebases `+0x0C/+0x10/+0x18/+0x1C`; `+0x14` sub-directory | `REG:968-983`, `ROW:237-241` |
| `003846F0` | two-level / variant binder (text banks, `.ard` cat 1, ref-array bands) | `BTB:62-71`, `LDR:376-380` |
| `00237FC0`, `00238160`, `00238880`, `00238660`, `003847B0` | bespoke binders for `02EBF138`, `02EBF0F8`, `02EBF0D8`, `02EBF158`, `02EBF118` | `ROW:1124-1139` |
| `0023A160` `BattleData_SetAreaArdSectionCategory` | `.ard` category → registry slot | `REG:208-223`, `LDR:323-330` |
| `0032FC30` → `003EA6E0` → `003EA820` / `003EA710` | area-change refresh → `.ard` reader → read-completion binder | `ARDC:48-51`, `ARDC:254` |
| `00264ED0` | `MapRef_GetAreaArdFieldResourceIndex`, 49 B | `ARDC:48`, `LDR:141` |
| `002F9860` / `002F9920` | text id resolvers (÷1000 positional / ÷10000 associative), 28 groups each | `VBF:776-802` |
| `00324510` | dormant `.nmb` assembler publishing `02EBF178` | `NMB:306-323`, `REG:1991-1999` |
| `004314E0` | authored expression `eval(record, context)`, 147 B, 99 non-EH callers; tail-calls combiner `00431350` | `RND:102-113`, `RND:390` |
| `003A6E60` | draw `f(bound)`, 345 B leaf | `AEC:47`, `RND:177-178` |
| `00259180` | RNG seeder, once at boot from `0022A0B0` | `RND:398`, `RND:415-419` |
| `002432B0` | typed-list decoder, 609 B, 108 functions / 113 sites | `TL:42-49` |

#### PS2-era formats (loaders)

| function | file / family | cite |
|---|---|---|
| `0039BEC0` | TIM2 validator/registrar: slot 1–7 on success, 0 on failure | `TIM2:86-101` |
| `002467A0`, `00280750`, `002808D0`, `00280AD0`, `003658F0`, `0039C3F0` | texpack, tex2pack, mrppack, clutpack, fontpack_fs, fontpack_it loaders | `LBB:84-164` |
| `003BC2D0` | world-map widget loader: kind 7 `0xA2`/`0xA3`/`0xA4` → widget `+0xD8`/`+0xE0`/`+0xE8` | `LMAP:467-473`, `WMAP:134-135` |
| `00253780` | `amap` (kind 7 `0xA5`) → `020927D0` | `AMAP:67-68` |
| `003C1DF0` | `gmap` (kind 7 `0x496 + byte+4`) → widget `+0xF8` | `GMAP:67-72` |
| `00576F50` / `00577100` | handbook bind / once-register | `HCHK:386-388`, `HCHK:412` |
| `0037F4D0`, `003800D0` | `menuquest` list / detail tables | `LST:91-92`, `MQ:71-75` |
| `002EA530` / `002ED950` | CHSE loader (kind 9 `0x0B+i`) / row reader | `CHSE:350-364` |
| `00365810` | `.btm` loader, 12-id table `00D10C98` | `BTM:74-77` |
| `003C1F00` / `003C26C0` | `.cl2` requester / reader | `CL2:100-111` |
| `00291C80` / `00248500` / `0024AA00` | AS7 request loop / LZ decoder / offsets walker | `AS7:125-141` |
| `00249320`/`00249350` → `00249210` → `0032E400` + `0032E620`; callback `00249660` | MRP request chain | `MRP:139-143` |
| `00562F90`, `00561390` | `mg` world-map mesh requesters | `MG:86`, `MG:105-106` |
| `00379870` | `sloc` consumer via table `0x02ADD030` | `SLOC:123-144` |

### 1.2 Inputs and outputs (data read and written, with record layouts)

#### Archive `FFXII_TZA.vbf`

- File: 31,196,932,183 bytes, 89,414 entries (`VBF:59-61`, `BIG:347`).
- Index header: `+0x00 'SRYK' 0x4B595253`, `+0x04 indexSize`, `+0x08 count`, `+0x0C _high` (never read) (`BIG:118-123`).
- Index body (`BIG:108-116`): keys `count × 16` (MD5 of each name), then records `count × 32`, then a name table (a u32
  length that counts itself), then a u16-per-64 KiB-block size table to `indexSize`.
- Record, `0x20` bytes: `+0x00 u32 firstBlock`, `+0x04 u32 copy`, `+0x08 u64 size`, `+0x10 u64 offset`,
  `+0x18 u64 nameOffset`, rebased in place (`BIG:125-131`, `BIG:159`).
- Block value: 0 = raw 64 KiB; `size mod 65536` in the last block = raw tail; any other value = zlib stream length
  (`BIG:166-168`).
- Integrity: MD5 (`0x8003`) over the index only; the 16-byte digest sits 16 bytes before EOF. "**It covers the index and
  nothing else.**" (`BIG:178`, `BIG:373-387`).

#### Path directory and file-size tables

- `g_pathTables` `0x0215F000`: 41 slots (kinds), filled by `002DF9A0` per language (`VBF:310-311`, `VBF:711-724`,
  `VBF:730-736`).
- FST file: `sprintf("%sFileSizeTables/FileSizeTable_%s.fst", "../", name)` (`FST:77`).
  - Layout: `u32[205000]` = `size[kind*5000 + id]`; `0xFFFFFFFF` = no file (`FST:56-61`).
  - Read by one `fread` of `0xC8320` bytes into `02EC3EE0`; a short read deliberately writes to address 0 (`FST:71`,
    `FST:81`).
- Kind-2 manifest `0x01E4D830`: 82 used slots, NULLs at 40/83/84 (`VBF:966-967`, `VBF:1267`).
- Size override `022C51F0`: 256 per-kind pointers, never filled; that path is dormant (`FST:111`, `FST:177`).

#### Request slot `ResourceRequestSlot` (64 × `0x80` at `022C31C0`, `RQC:71`, `RQ:425-436`)

| off | field | cite |
|---|---|---|
| `+0x00` u64 | counter accumulator, written never read | `RQC:75` |
| `+0x08` u64 | stamp (second `0035E810` reading) | `RQ:166-170` |
| `+0x10` / `+0x18` | next / prev | `RQC:76` |
| `+0x20` u8 | state 1..6 | `RQ:428` |
| `+0x21` u8 | kind; `0xFF` = raw path | `RQ:429` |
| `+0x22` u8 | chunk enable | `RQ:430` |
| `+0x23` u8 | part verdict | `RQC:78` |
| `+0x24` i32 | index, or path pointer truncated through `movsxd` | `RQC:79`, `RQ:548` |
| `+0x28` / `+0x2C` | bytes this part / file offset, truncated toward zero to `0x800` | `RQ:432` |
| `+0x30` / `+0x34` | part cap `0x80000` / remaining | `RQ:433` |
| `+0x38` / `+0x70` | dest / dest0 | `RQ:434` |
| `+0x40` / `+0x48` / `+0x50` | onDone / onCancel / onPart (always 0 in the shipped build) | `RQ:286-287`, `RQC:84` |
| `+0x60` / `+0x64` | arg / request id | `RQC:85` |
| `+0x68..+0x6F`, `+0x78..+0x7F` | "Unobserved ... do not invent semantics" | `RQC:86` |

- Request descriptor (`0x28` B, caller's): `+0` offset, `+8` arg, `+0x10` onDone, `+0x18` onCancel, `+0x20` not
  consumed (`RQ:437-439`, `RQC:88-91`).
- Request id: `id = (counter << 6) + (slot & 0x3F)`; counter `01EED498` starts at 1 and resets above `0xFFFFFF`
  (`RQC:112-114`).
- File offset: `cdq; and edx,0x7ff; add eax,edx; and eax,0xfffff800` (`RQC:126`, `RQ:211-221`).

#### Indexed external-source request (80 × `0x1C` at `02B581A0`, `ISR:38-52`)

- Fields: `+0` handle, `+4` state, `+8` annotation, `+0xC` u8 group, `+0xD` u8 route, `+0xE` u16 slot, `+0x10` s16
  kind, `+0x12` s16 index, `+0x14` s32 length, `+0x18` s32 offset.
- Pending mask: dwords at `02B58A60 + 4g`.
- Selector map `0032F170` (`ISR:84-88`): g0 → kind 5, index `3·sel`; g1–3 → kind 8, index `4·sel`; g4 → kind 1,
  index `sel+0x6B`.

#### Arena block header (`0x40` below the payload; assembled from EV)

| off | field | cite |
|---|---|---|
| `+0x00` | u16 magic `0xFF12` | `EV:191`, `EFX:370` |
| `+0x02` | byte, `FF` on free | `EV:1220` |
| `+0x04` / `+0x08` | free-list links | `EV:443` |
| `+0x0C` / `+0x10` | neighbour links | `EV:590-592` |
| `+0x14` | bit 0 = allocated | `EV:244` |
| `+0x15` | bit 1 = tree member; `& 6 == 2` and mask `0x04` gate movement | `TREE:130-132`, `TREE:436` |
| `+0x16` / `+0x17` | arena / category counter index | `EV:1221` |
| `+0x18` | dword payload extent = tree key (signed compare) | `TREE:194-197`, `EV:1127-1130` |
| `+0x1C` | u16 sequence / generation | `EV:1469-1473`, `TREE:217` |
| `+0x1E` | u16 debug tag | `EV:1496` |
| `+0x20` | encoded handle-slot backlink | `EV:561-565`, `MOV:49-51` |
| `+0x24` / `+0x28` / `+0x2C` | tree left / right / parent (arena offsets) | `TREE:42-50` |
| `+0x34..+0x3B` | 7-byte name + NUL | `EV:192-193` |
| `+0x3E` | must-be-zero guard; cleared on insert | `TREE:50`, `EV:1215` |

- Arena record: `022D7FD0 + id·0xA8`, 15 records. Fields: `+0x08` backing, `+0x50` tree root, `+0x62` compaction
  latch, `+0x90`/`+0x98` free ends, `+0xA0` callback (`EV:394-396`, `EV:1120`, `TREE:445`).
- Boot arenas (malloc / init / slots, `EV:351-361`): 2 `1DC0010/1DC0000/10`, 3 `D20100/D20000/100`,
  4 `100010/100000/10`, 5 `1C0100/1C0000/100`, 6 `6C00400/6C00000/400`, 7 `3000100/3000000/100`,
  8 `2000100/2000000/100`, 9 `1200010/1200000/10`, 11 `400100/400000/100`.

#### Resource entry and section addressing

- Section header: `+0x00` tag, `+0x10..+0x2F` 32-byte name (`CSA:60-62`).
- Match rule: `tag==0 || tag==0x4C4C4140 ("@ALL") || header.tag==tag`, and `name==NULL || all 32 bytes equal`
  (`RSA:224-227`).
- Pointer: `ptr = (offset==-1 || entry==NULL) ? NULL : sign32(low32(base(entry)) + u32(offset))` (`RSA:231-233`).
- Base: `mode==0 ? 0051EE00(entry+0x10) : mode==1 ? (DAT_02b62e10 ? refresh : cachedBase) : NULL` (`RSA:250-254`).
- Entry fields: `+0x04` mode, `+0x10` buffer descriptor (mode 0; handle at `+0x18`), `+0x30` handle, `+0x38` cache,
  `+0x40` size (`CSA:64-68`, `OWNC:103-105`). The entry size is contested (C-V5).
- Table descriptor: `+0x10` bankDir base, `+0x38` slot table, `+0x48` rowStride, `+0x4C` bankShift, `+0x50` rowMask;
  `row(i) = bank + sign32(u32((i & rowMask)*rowStride))` (`RSA:204-219`).

#### Authored data

- `st2e` header (32 B as corrected 2026-10-01, `VBF:89-101`, `VBF:1251-1257`):
  - `+0x00` magic `"st2e"`, `+0x04` count, `+0x08` recordSize, `+0x0C` headerSize (32 or 0).
  - `+0x10` 0 in all 407 files; `+0x14` heapOffset.
  - `+0x18` = `0x7144` in `eitm_data`, else 0; `+0x1C` = `0x98` in `tutorial_data`, else 0.
- String heap: `{u32 one=1; u32 base=12; u32 heapSize_minus_1; u32 count; u32 offsets[count+1]; char text[]}`
  (`VBF:591-598`).
- `us` charset: `0x20..0x39 A..Z`, `0x3A..0x53 a..z`, `0x04` space, `0x02` line break, `0x00` end; `{0F}xx` is an
  inline escape (`VBF:609-613`).
- Registry: `0x02EBF008 .. 0x02EBF200`, 64 slots, 8-byte stride (`REG:81`).
- Row formula: `row(t, n) = 0020E600(t[+0x0C]) + n * t[+0x08]`, `+0x04` = count (`REG:370-382`). The canonical shape
  computes the row address in 32 bits and does not bounds-check (`ROW:515`, `ROW:700-704`).
- `battle_pack.bin` directory: entry *i* at `+4+4i`. `action_data` `+0x3C`, `commandpack` `+0x2C`, `word.bin`
  `+0xF8`, `status_data` `+0x40`, `attribute_data` `+0xA8`, `license_board` `+0x11C` (`VBF:342-347`). The entry count
  and width are contested (C-V20).
- `commandpack`: `{u32 count; u32 offsets[count+1]; payload}`, records `{u16 actionId, u8 weight, u8 0}`.
  Reader: `r = rand % 100`, running sum (`VBF:404-418`).
- Text banks: `TextBankTable {u16 bankCount=15; u16 _pad; u32[16] bankOffset}` and
  `TextBank {u16 blockCount; u16 _pad; u32 blockOffset[count+1]}`. Word = `bank<<11 | block` (`BTB:75-76`,
  `BTB:114-124`).
- `.ard` header `Ff12Ar03Header`, `0x30` (`LDR:106-118`, `ARDC:56-60`):
  - `+0x00` magic (never read), `+0x0C` trailer offset.
  - Slots: `+0x10` (always `0x30`) → cat 0, `+0x14` → cat 1, `+0x18` → cat 2, `+0x24` → cat 3, `+0x28` → cat 4,
    `+0x2C` → `003DCF00`.
  - Category → slot: 0 → `0x02EBF150`, 1 → `0x02EBF168` (via `003846F0`), 2 → `0x02EBF120`, 3 → `0x02EBF148`,
    4 → `0x02EBF140`. Record widths 84/88/56/56 (`LDR:323-360`).
- `.ard` slots 5/6: `value = slot6[f] × (level − byte[stats+0x88]) + slot5[f]` (`LDR:936-946`).
- `.nmb`: `{u16 count 0..22; u16 0x0064}`, `u32 offset[count+1]`, entries `{u8 0x12; u8 0xBA|0xBB; u8 0}`; size
  `8 + 7·count` (`NMB:71-100`).

#### Authored expression (16-byte record, `RND:82-96`, `AEC:53-64`)

- Fields: `+0x00` payload A, `+0x04` payload B, `+0x08`/`+0x0A` u16 period A/B (`RND:96` only), `+0x0C` kind A,
  `+0x0D` kind B, `+0x0E` u16 flags. Operator = bits 4–7 of `+0x0E`; curve selector = bits 0–1 (A) / 2–3 (B).
- Operand kinds: 0 absent, 1 = resolve the payload and read `+0x04` of the target, ≥ 2 = curve with *kind* points.
- Operators (`AEC:68-76`, `RND:123-131`):

  | op | result |
  |---|---|
  | 0 | `a` |
  | 1 | `a + f(b)` |
  | 2 | `a − f(b)` |
  | 3 | `a − b + f(2b)` |
  | 4 | `a × (f(b)+1)` |
  | 5 | `b == a ? a : a + f(b − a)` |
  | > 5 | `a` |

  With `b == 0`, only op 5 draws (`AEC:80-82`).
- `f(bound)` (`AEC:157-166`, `RND:191-199`): `advance(5)`; `v=as_float(state)` in [1,2); `P=v·B`; `D=P−B·1.0f`;
  `advance(2)`; return `(int)D`. Fixture: seed `458DC800` → 445,312,896 for bound 1e9 (`AEC:88-89`).

#### Menu and PS2-era formats (the parts a port needs to load files)

| format | layout | cite |
|---|---|---|
| typed list | outer record 20 B (count bits 0–9, item offset self-relative); items `{len, type 1..9, …}`; sizes 1 `0x20` 2 `0x40` 3 `0` 4 `0x20` 5 `0x30` 6 `0` 7 `0xA0` 8 `0x20` 9 `0x40`; one allocation `count*8 + Σsize` | `TL:57-107`, `TL:530-537` |
| TIM2 | `+0x00 'TIM2'`, `+0x40` low nibble must be 1; rest per Sony spec | `TIM2:64-72` |
| pack dir | `u32[dir_size/4]` self-relative offsets, `0xFFFFFFFF` fill, 16 or 32 slots | `LBB:60-65` |
| MRP | `MrpHeader` 0x30; table A 0x14; tail 0x10 atlas names; table B 0x0C | `MRP:60-117` |
| AS7 | big-endian `'A7'`, `u16be count`, `u32be tailOff`, `u32be offsets[]`; LZ pages | `AS7:52-57`, `AS7:134-137` |
| BTM | raw 4 bpp texels; glyph `{u16 code, u8 w, u8 h, u8 ?, u32 pixelOffset}` | `BTM:53-62`, `BTM:140` |
| CL2 | `Clt2Header` 0x40, palette `count*4` RGBA; alpha `min(255, trunc(a·255/128))` | `CL2:50-72` |
| FST | above | `FST:56-61` |
| amap | 396 B; P/Q/R/S tables, `S[i] = 60099+i` | `AMAP:49-63` |
| wmap | 2,040 B; header 0x14; regions 12, areas 39×28 B, routes 60×8 B, Strahl 18×4 B | `WMAP:53-127` |
| lmap | 23,852 B; 48 records `counts(4) | A 24·n | B 24·n | C 20·n | block(8) | D 4·n` | `LMAP:72-117` |
| cmap | 1,760 B; directory 48×8, sec2 369 u16, sec3 77×8 | `CMAP:51-100` |
| gmap | header 0x10, entries `{gate, key, textRel, 0}` | `GMAP:49-63` |
| hctg/hchk/hdat/himg | base table `00D23740` u16[6]; record 12 B; himg 8 bpp TIM2 pages | `HCHK:53-351`, `HIMG:53-78` |
| qstl (`.lst`) | header, 8-byte directory `{u16 questId, u16 dataRel, u32 kind}` | `LST:53-65`, `LST:155` |
| menuquest | `u16 off[6], 0xFFFF, u16 N`; record 20 B | `MQ:51-60` |
| CHSE | `CHSE`, `u16 1`, `u16 letter`, `u32 count`, `u32 0`; record 16 B | `CHSE:69-88` |
| sloc | header 0x14, u16 directory, records, TIM2s, `NPS2[]` 32 B | `SLOC:78-111` |
| `.ta` | CRLF text, frame 0 = name without `_pic_` | `TA:67-81` |
| `.ah` | `"%s"` tokens, no `##` filter | `AH:60-110` |
| prefetch `.txt` | `"%s"` tokens; `##` lines dropped; entries resolve-and-mark only, "**never read**" | `PFM:83-132` |
| TGA | uses only width/height at `+0x0C/+0x0E`, `w×h×3` BGR | `SF:73-79` |

### 1.3 State (globals and objects, with lifetime)

| state | contents / initial value / lifetime | cite |
|---|---|---|
| archive object (`0xB0`) | index at `+0x00`, block-size table `+0x68`, compressed flags `+0x70`, path `+0x78`; lives from mount at boot | `BIG:66-89`, `BIG:116`, `BIG:170` |
| `01F83440` / `01F83448` | RAM-cache enable byte / budget = physical memory / 3, clamped 32 MB–4 GB | `PATH:244` |
| `01F83441` | low-memory byte (< 1 GiB or budget clamped) | `PATH:268-272` |
| `0215F000` | 41 path-array pointers, set once by `002DF9A0` | `VBF:310-311` |
| `02EC3EE0` | FST, 820,000 B, read once at boot | `FST:81` |
| `022C31C0` / `022C51C0..D0` | request pool / pending head, tail, free head; free head = pool start initially | `RQC:139-140`, `RQ:760` |
| `01EED498` | request counter, initial 1 | `RQC:141` |
| `0215EFF4` | read status: −1 in flight, ≥ 0 bytes delivered, −2 rejected | `RQ:333`, `RQ:715` |
| `022C51F0` | 256 override pointers, zeroed at init, never filled | `RQ:73-74`, `FST:111` |
| `02B581A0` / `02B58A60` | 80 external-source owners / 5 pending masks; reset by `003DD7E0` | `ISR:38-54` |
| `022D7FD0` | 15 arena records (`0xA8`); 9 set at boot by `0022A0B0` | `EV:351-361` |
| `022D89A8` / `022D89BC` | logical-source → arena map / selected arena; identity map in every state | `EV:381-384`, `EV:1406-1410` |
| `01F83530` | image-address base qword; **zero at image load** (past raw `.data`); one in-image store route (`00210570`, texture id `0xFFFB`), "undriven" | `TREE:87-98`, `ROW:441`, `EV:287` |
| `02B62E10` | re-resolve flag byte, set/cleared only by `0041E500` around a refresh | `RSA:589-593` |
| `02B62E20` | 32-byte name scratch (not re-entrant) | `RSA:455-456` |
| `02EBCD80` | EFX ticket pool, 64 × `0x38`; links `02EBDB80/88/90` | `OWN:106-112` |
| `02EBEF70` / `02EBEF78` / `02EBEF90` | EFX relocation chain / `0x1800` table / `0xA00` table | `EFX:912-920` |
| `02F97340` | EFX context (`0x890`) published by `0024B3A0` | `OWNC:70` |
| `0x02EBF008..0x02EBF200` | registry: STATIC slots bound once at boot, never rebound; five `.ard` slots rebound on every outer-area change, null when the area has no `.ard`; 12 board pointers | `REG:915-923`, `REG:2016-2024` |
| `0208E680` | STATIC blob | `ROW:843-844` |
| `02B5E0C0` / `02B5E0B8` | loaded `.ard` base (two entries) / loaded field index (−1 = none) | `LDR:283-284`, `LDR:625-626`, `ARDC:254` |
| `0x02EBF190` | `BattleSystemState` pointer, always `021B290C`; 40 × `0x1C8` stats records from `+8` | `REG:440-448`, `REG:1355-1367` |
| `02EC3D80` / `02F973C0` | text-group presence / data tables, null in the file, filled at load | `VBF:776-802`, `VBF:863-864` |
| `01EF93E8` / `022D9138` | RNG state (seeded `0x458DC800` at boot) / enable word (BSS; writers `00259180`, `0044BAC0`) | `RND:250-251`, `RND:398` |
| `01EF93FC` | vf00.w, the `1.0f` operand of `f` | `AEC:303-304` |
| `0208F580` | atlas registry, 64 × `0x48`, BSS | `TL:226-232` |
| `02AEE810` | TIM2 / font-variant registry, 8 pointers | `TIM2:154`, `LBB:157-163` |
| `02B457E0` | world-map widget singleton (`0x278`) | `LMAP:465-466` |
| `02CA9738` | handbook root singleton | `HCHK:376-384` |

### 1.4 Order (what runs when, and what triggers it)

**Boot.** The order below is stated in pieces. No page gives one boot sequence for the folder.

1. Archive mount: `0017CEF6` → `0019B070` → `001F4340` (`PATH:239`, `BIG:214`).
2. `0022A0B0` runs:
   - `ResourcePath_Init` `002DF9A0`, with the FST read (`FST:71`);
   - the nine arena inits (`EV:351-361`);
   - the RNG seeder `00259180`, after twenty presentation initialisers (`RND:398`).
3. Resource system init `0032EA90` (`RQ:72-74`).
4. `002368D0` registers STATIC and the 12 board requests. Delivery `00238850` → `00236C30(1)` (`ROW:841-844`,
   `REG:2003-2009`).
5. Prefetch `common.txt` is resolved and marked, not read (`PFM:119-132`).

**Per frame.**

- `0032E040` kicks the pump `0032E070` when `001EDE80()` or `0017D930()` is non-zero. Its callers are the frame-mode
  bodies, the boot initialiser and two others (`RQ:119-126`). The contract states no once-per-frame guarantee (C-S6).
- **Pump states** (`RQ:143-153`, `RQC:174-194`):
  - Empty list → `003EADD0`.
  - State 1 (if the BGM machine is idle) → issue through `0046E030`/`002DF780`, or `002DF6C0` for kind FF → state 2.
  - State 2 → state 3.
  - State 3 → state `5 + (0046E0E0()<0)` once `0046DFE0` reports done.
  - State 4 → cancel callback.
  - States 5/6 → done or error, or the chunk logic.
  - Footer: `0046DD50`, `003E9780`, then `003BB790`.
- **Stall.** `0032E870` with no free slot loops: pump → `0046DFE0` → `0035EA30(0)` (`RQ:102-104`).
- **EFX rebase.** `0024D540` runs from the main-loop frame functions (callers contested, C-V18). On a source move:
  `003B3480` compares the new base to `+0x858` → `0024D970` → three table rebases (`EFX:46-55`).
- **Re-resolve.** `0041E500`: set flag → `00409F70([+0xD90])` → clear flag → `0046E3E0([+0xD98])` →
  `0051B9F0([+0xDA8])` → `00478030([+0xDA0])`. Triggered from `0042ED60` and `00332590` (`RSA:308-310`,
  `RSA:589-593`).
- **Arena maintenance.** `002E65A0` compacts arenas 6 and 10 (`MOV:108-109`).

**On area change.**

- `0032FC30` → `003EA6E0` (skip if already loaded and not forced) → `003EA820` (`ARDC:48-51`, `ARDC:254`).
- `003EA820` unbinds: 15 `(N,0)` category clears in three groups of five (`ARDC:118-125`).
- It then requests `(21, 2·areaIndex)` plus the `.fpk` sibling (`ARDC:70-71`, `ARDC:90`).
- On delivery `003EA710` binds categories 0–2, then 3–4 only if their resolve is non-zero, then slot 7 → `003DCF00`
  (`ARDC:118-125`).
- `002342F0` scrubs the 40 stats records (`REG:657-658`).

**Teardown.** EFX disposal order is render sweep → `003B37E0` (`00409EC0`) → `00409730` (`00409EC8`) → `0051FCF0`
(`00409ED3`) (`OWNC:154-157`). The world-map widget frees its three buffers through `003697F0` (`LMAP:475`).

### 1.5 Dependencies (on other systems)

| on | what | cite |
|---|---|---|
| 18-Audio | BGM stream machine `003EADD0`/`003EADE0` served before the queue in state 1; `0032E780` head-insert; Audio caller of the resolver `00225BA0` | `RQ:345`, `RQ:485-487`, `PATH:350` |
| 15-Input | caller `0079FB10` of the stream reader | `PATH:230-231` |
| 19-Save-Load | `003BB790` save-storage machine in the pump footer; locale selector arms of `002DF9A0` | `RQ:657-671`, `PATH:239` |
| 22-Phyre | `PStreamReaderFile`, `.phyre` loads named by `.ah` | `PATH:45`, `AH:235-236` |
| 17-Render / Presentation | `RenderResourceEntry` banks at `+0xD90/+0xD98/+0xDA0/+0xDA8`; atlas registry; TIM2 upload `0017F3B0` | `RSA:589-593`, `TL:226-232`, `CL2:72` |
| 16-UI | typed-list widgets, menu screens, map screens `002B7B80`/`002BAF80` | `TL:144-146`, `LMAP:316` |
| 07-Combat / 05-Spawn | `BattleUnit_ApplyUnitDefinition` `0023A570`; action-row page; `.ard` slots 5/6 growth | `REG:1446`, `LDR:936-946` |
| 24-CRT | zlib `0080C5A0`, `_Init_thread_header/_footer` `008092FC`/`0080929C` for the 149 one-time-init holders | `BIG:171-172`, `README:42-50` |
| 00-Engine | main-loop frame functions `0022B0B0`/`0022B8C0`/`0022BC20`; boot `0022A0B0` ← `0017D4C0` | `EV:1455-1456`, `ROW:874` |

---

## 2. Gaps

### 2.1 Gaps the pages state themselves (still open as written)

Items a page marks answered elsewhere are not repeated here. They appear under §3.2 when their "open" text is
still unstruck.

| id | gap, as the page states it | cite |
|---|---|---|
| G-S1 | Queue side effects: "Real read-layer, file/archive, service-footer and callback side effects beyond the checked boundary"; "Live progress, scheduling, synchronization, cancellation/path lifetime and higher-level priority policy"; "Authored/reachable producer state for the chunk gate" | `RQC:271-273` |
| G-S2 | "*Nothing live has run.* Whether the allocator supplies a high half at all ... it is open" (raw-path pointer truncated to 32 bits in `+0x24`) | `RQ:540-541` |
| G-S3 | "36 of `0032E620`'s callers compute their kind ... not modelled here"; "The other 36 sites compute their kind. They are not resolved here" | `RQ:680-681`, `NMB:227-228` |
| G-S4 | The owner record's `+8` annotation: "later semantic meaning is unresolved"; "The annotation's downstream purpose remains unresolved" | `ISR:45`, `OWNC:114` |
| G-S5 | "what a byte-count -1 failure callback registers ..., and the five other `003EDAD0` drivers"; "the 20 array-bearing setup routines' loops and what the linked `*02EBEF70` nodes are"; OV-42 "Still OPEN" | `PRF:103-105` |
| G-S6 | Decoder base `01F83530` over the process: "**"zero for the life of the process" is supported, not proven**"; "**"The base is zero for the whole process" is well supported and not proven.**"; Limits 3 "parks it as live-only" | `TREE:101`, `ROW:472`, `EV:1400-1405` |
| G-S7 | "**Threading** — not established; no lock appears in the read bodies"; "no arbitrary reentrant/thread-safe lookup is established" | `TREE:257`, `RSA:141`, `EFX:393-394` |
| G-S8 | "whether any arena exceeds 4 GiB in practice"; "Whether any arena backing ever sits more than 4 GiB from the decoder base" | `EFX:554-555`, `ROW:823-828` |
| G-S9 | "Whether any caller distinguishes "not found" from a genuine offset of `-1` (RA-6)" | `CSA:194` |
| G-S10 | Authored expression: "What the record is part of, and who authors it"; "The **bit-2-clear** branch of `0042FDB0` is not characterised here ... Mode-byte values 1 and 2 ... are unread"; `00430B90` "**not read**" | `AEC:219`, `RND:379-384`, `RND:403` |
| G-S11 | `0x02EBF178`: "What sets state 1 and fills the 301 ids, and who reads the blob, is **FZ-8**." | `REG:1999-2000` |
| G-S12 | Registry residue "**60 bytes in 8 tables**"; 30 tables with no type rows ("the generic accessor that resolves a descriptor to a record" is wanted); class-13 table order not stated | `REG:1229`, `REG:2234-2243`, `REG:1263-1265` |
| G-S13 | `.ard`: "**What is still missing is the record level:** the four `st2e` tables' fields and what a row means"; "What each *individual* bit switches remains open"; "what writes `stats + 0x88`" | `LDR:657-661`, `LDR:646-654`, `LDR:950` |
| G-S14 | `.nmb`: "**What an entry means is not established.**"; "`0x12BA` vs `0x12BB` is undecided." | `NMB:763-768` |
| G-S15 | `.ard` reader: "at `003EA8A4` and `003EA9AE` no instruction sets `rcx` after the preceding free call"; "Which caller sets the force flag the refresh's skip depends on" | `ARDC:188-189` |
| G-S16 | Text: "The CJK tables index a different glyph set and were not tested"; "What the data puts in each array is still a runtime fact"; low-pool group 20 "not yet bound to a file" | `VBF:617-618`, `VBF:846`, `BTB:234` |
| G-S17 | BigFile: whether a `false` from `0019B070` refuses to start the game ("followed one level") | `BIG:439-445` |
| G-S18 | FST: "**Why ten kinds are unsized**"; the byte-identical pairs; kind 5 unnamed | `FST:186-188`, `FST:293-296` |
| G-S19 | Prefetch: whether manifests are complete or advisory; the `events/` loader; nothing measured from a file | `PFM:247-254` |
| G-S20 | `.ah`: the consumer of the list; `_srm` meaning; the kind-4 dispatch "not read" | `AH:235-239` |
| G-S21 | `.ta`: the script verbs for rate/loop and the `0x130` record; which dispatcher twin serves `.ta` | `TA:228-229`, `TA:316-318` |
| G-S22 | TIM2: "What the decoder does with the other fields"; "**Whether the seven-slot ceiling is ever reached in play.**"; what `eXt` means | `TIM2:197-198`, `TIM2:297-299` |
| G-S23 | behindcamera: "**Still open:** which drive parameter `x` is and what `y` answers"; "the function that samples `obj+0x10..+0x63` per frame was **not** located" | `LBB:354-356`, `LBB:261` |
| G-S24 | MRP `+0x2C` "not established"; "The spare `{count,offset}` pairs' table strides" | `MRP:73`, `MRP:227` |
| G-S25 | Field-level residue on the menu formats: hctg `+0x08` high bits, monster tail `v1`–`v3`, hchk `+0x0A`/`+0x03`, hdat `arg`; `QHD0`/`QHT0` fields, `rel[5]`, header `+0x0C`; cmap `auxId` and sec2 semantics; wmap `+8` aux and `B2`; sloc LCMPOS1, NAVIICN2, `_e3`, `version`, `recordEnd` | `HCHK:392-410`, `MQ:94-97`, `CMAP:141`, `WMAP:198-199`, `SLOC:314-327` |
| G-S26 | binmenu: "**Open (static limit):** **palette ownership**"; "the exact guest-slot → `face_guestNN` selection table" | `BINM:152-166` |
| G-S27 | CHSE: which actors reach state 4 with no battle-record key; what the letters are; why three tables ship empty | `CHSE:212-226` |
| G-S28 | gmap: a latent over-read for five Latin `guide00` copies "(inferred, not run)"; `0x18xx` text codes; no writer of byte `+4` searched | `GMAP:91-99` |
| G-S29 | Unnamed `.bin`: ashd "`field04`'s role is open", "Its bytecode is not disassembled"; the st2e surplus bytes "the content is not read" | `UBF:160`, `UBF:168`, `UBF:230-231` |
| G-S30 | Five small tables: sign scene-record `a`/`b` and text rows; hchk header fields; qstd bits 18/30 "No reader"; QST1 field 718 and bit 26 | `FIVE:206`, `FIVE:349-350`, `FIVE:360`, `FIVE:396-398` |
| G-S31 | Every system page states it has no live-game observation (for example "No observation of the running game"; "Nothing was executed"; "no experiment executes these five bodies") | `AEC:224`, `BTB:348-350`, `ARDC:178-180`, `FST:298-301` |

### 2.2 Structural gaps found while mapping (a port needs these and no 02 page states them)

| id | gap | where it shows |
|---|---|---|
| G-T1 | **Queue pacing and clocks.** The pacer `0035EA30` (called with 0 and 2), the counter `022CA5E0` (writer, unit, initial value) and the return values of `003EADD0` and `0046DFE0` are not stated. Only "returns 2 while the word is −1" is given for `0046DFE0`. | `RQ:103`, `RQ:173`, `RQ:145`, `RQ:713` |
| G-T2 | **Two pump branches appear only in the contract.** The kind-FF retry ("Kind-FF nonzero submit result revisits the same head") and the refused-read path ("a refused read (a −1 file-size entry, `002DF7B9`) also moves to state 2 ...") are in `RQC:177`. The state table in RQ does not carry them, and the `002DF6C0` return contract is not given. | `RQC:177` vs `RQ:145-147` |
| G-T3 | **`0032EB40`, the "staged (2 KB-chunk) request path".** It is named on FST but absent from the queue pages, and ARDC calls it a read request (C-V45). | `FST:74`, `FST:108` |
| G-T4 | **EFX ticket id.** "preserves low6 slot bits and high tag bits while changing generation bits": no bit widths and no initial stamp. | `OWN:107` |
| G-T5 | **External-source metadata directory `022C6E70+8g`.** Only the first byte, `+8+8i` and `+0xC+8i` are given. | `ISR:95-96` |
| G-T6 | **`.cm` configuration table `02B64380` and the `metadataSize` provider chain.** Named, with no parse or format. | `PRF:47`, `PRF:51-53`, `PRF:123` |
| G-T7 | **EFX per-element relocation bodies.** `005004C0` dispatches to 38 bodies and only subtype 0 (`00500470`) is described. The 'R' repair `00501420` and the notify `00442460` are named only. | `PRF:58`, `PRF:134`, `EFX:912` |
| G-T8 | **Tree add path.** It never says which arena tree it inserts into; only remove gives `tree = (byte[node+3] < 0xF) ? 022D7FD0 + byte[node+3]*0xA8 : 0`. The splice helpers `0036B490`/`0036B5A0` and the third argument (`0x4AA`, `0x4BF`, `0x4DF`, `0x4E3`) are undefined. | `TREE:292` vs `TREE:298`; `TREE:178-185` |
| G-T9 | **Handle-slot table.** Slot `+5` active, `+6` generation, `+8` header are given, but the table base, size and allocation are not stated. | `TREE:217`, `EV:561-569`, `EFX:120` |
| G-T10 | **Arena record and header initial contents.** `0036A490` writes the header ("the 0x40-byte record initializer") but no field-by-field initial values are given. The arena record layout is "a map, a qword array and optional 16-byte bookkeeping records", with offsets deferred. | `EV:394-397`, `EV:1470`, `ROW:1318` |
| G-T11 | **Section-addressing bodies and descriptor fields.** `00409930` (`ResourceEntry_FindSectionIndexByTagAndName`) has no body description. Descriptor `+0x28` (bank blob) and `+0x54` (capacity) are used but absent from the §4 layout. The six `0041E500` callback bodies are named only. `RSA:712` cites `rowstride-census.tsv` "the durable artifact", which exists nowhere in the repo. | `RSA:168`, `RSA:204-212` vs `RSA:679`/`RSA:701-702`, `RSA:603-610`, `RSA:712` |
| G-T12 | **Typed list type 4.** The constructor sets `node[+0x18]=0` and "builds nothing", yet the drawer arm `0029ED30` is "a `jmp` through node `+0x18`". Whether that jump is guarded is not stated. The allocator `002497B0` and release `002482E0` are named only. | `TL:128`, `TL:466`, `TL:590` |
| G-T13 | **RNG recurrence `advance()`.** "The recurrence itself is specified on the RNG page" — not on any 02 page. Only `as_float(state)` is given for how state becomes `v ∈ [1,2)`. | `AEC:120-121`, `AEC:160`, `RND:186` |
| G-T14 | **Curve evaluator edge cases.** Missing: a value below the first x, negative values against the period, period 0, how the three control points are chosen, which root `0039B6E0` takes, and what sentinel `2.0` triggers. The period fields `+0x08`/`+0x0A` are absent from both record-layout tables. | `RND:82-96`, `AEC:53-57` |
| G-T15 | **Expression context and variants.** The `context` argument of `eval` is never described. The second writer of the enable word, `0044BAC0`, is named only. The float twin `004309C0` and its tail `00430540` have no formulas. | `AEC:45`, `RND:251`, `RND:277`, `RND:402` |
| G-T16 | **`003846F0` body.** It binds text banks, `.ard` category 1 and every `+0x14` sub-directory entry, but is described only as "a different binder, with a third argument zeroed", "the two-level rebase", and in two conflicting sketches (C-V47). | `REG:220`, `REG:979`, `ROW:847`, `BTB:66-69`, `LDR:378-380` |
| G-T17 | **Bespoke binders.** What `00237FC0`'s "re-registered" rows do, what `00238160` rewrites per row, and the three nesting levels of `00238660` are not enumerated. | `ROW:1135-1138`, `REG:1950` |
| G-T18 | **`0x02EBF188`.** Written 93 times by 40 functions, read by none found. Only "formula gates / result metadata" (UNPROVEN) is given. | `REG:891-892`, `REG:1900` |
| G-T19 | **`BattleSystemState` and the 456-byte stats record.** `0x7410` B with magic `0x05071901`; only scattered offsets are known, and "58 offsets is a floor". There is no layout or initial values. | `REG:2053`, `REG:1492-1521` |
| G-T20 | **Row-address width.** ROW proves 32-bit truncating arithmetic for one instance. REG's formula gives no width, and whether every inlined consumer truncates is not stated. | `ROW:700-704`, `REG:379` |
| G-T21 | **Field id → `.ard` area index.** `00264ED0` is named (49 B) with no mapping, and "the same area has different indices" in `.nmb`. | `ARDC:48`, `LDR:141`, `NMB:684` |
| G-T22 | **`.ard` base table entry 1.** The binder writes entry 0 of `02B5E0C0` and `003EA650` accepts 0..1, but no writer of entry 1 is stated. The slot-7 table's count/terminator for `003DCA30` is not given. | `LDR:625`, `LDR:641`, `LDR:676-681` |
| G-T23 | **Text decoding.** The packed-string indexer `002B58B0` is "by reference". The `{0F}xx` / `0x0F` inline escape codes are not decoded. The CJK encodings ("multi-byte sequences of their own") are not given. PS2 pages defer their text encoding to "the text-data sheets". | `BTB:98`, `BTB:108`, `VBF:198`, `VBF:613`, `HCHK:351`, `LST:84-85` |
| G-T24 | **Text-group tables `02EC3D80` / `02F973C0`.** "null in the file and populated at load": the populating function and its source are not named. | `VBF:863-864`, `VBF:1113-1114` |
| G-T25 | **Route-1 (RAM cache) behaviour.** The extension test is "nine single-character tests" with no boolean combination. The cache node layout, insertion by `0059A9B0`, and eviction against `01F83448` are not described. | `PATH:178-182`, `PATH:292-293` |
| G-T26 | **Archive object and mounts.** The `0xB0` object is given only at `+0x00/+0x20/+0x68/+0x70/+0x78`. Route 2 has "five package slots", with no search order. The name-table terminator is not stated. | `BIG:262`, `PATH:239`, `BIG:115` |
| G-T27 | **`.ah` entry and request record.** The struct is fenced as `size=0x03`, yet it has a `+0x88` back-pointer and ordinals divide by 8. The request-record kind 4 arm of `001A0BB0` is "not read", though `.ta` depends on it. | `AH:68-80`, `AH:96`, `AH:238-239`, `TA:88` |
| G-T28 | **`.ta` / phyremaps.** The phyremaps parser `00677340`, the loaded-asset table `0019CA80` and the frame-set element layout are named only. | `TA:94`, `TA:120`, `TA:668` |
| G-T29 | **TIM2 decode route.** "Which loader the 446 `.tm2` files actually go through" is unknown; decoding is left to the Sony spec, and `+0x40` "is **not a uniform `formatId`**". | `TIM2:81-82`, `TIM2:259-264` |
| G-T30 | **AS7 LZ codec `00248500`.** The tail block `{mode, k, be16 outLen, dictionary}` is given but not the token format. | `AS7:134-137` |
| G-T31 | **`mg` mesh layout.** The only struct on the page is the superseded one; "§2's slot struct is 4 bytes out of phase", and the replacement lives only in an `_index/candidates` record. | `MG:4`, `MG:48-69`, `MG:95`, `MG:147`, `MG:156` |
| G-T32 | **`sloc` records.** The LCMPOS1, NAVIICN2 and untagged-record layouts are not given. The filler of `0x02ADD030` and the consumers `003C6360`/`003C6380` are "not read here". | `SLOC:124`, `SLOC:186`, `SLOC:316-320` |
| G-T33 | **`loc_MAX 59` has no owner.** wmap: "(in `lmap`, not here)"; lmap: "Those belong to `menumap_world.bin` and are not tested here". | `WMAP:155`, `LMAP:621-623` |
| G-T34 | **binmenu texture format.** "The per-kind descriptor table ... is **runtime-populated**"; a port must pick L8 or CLUT. | `BINM:125-126`, `BINM:154-156` |
| G-T35 | **Handbook root handle layout.** The `+0xC8…+0xF0` stride is internally inconsistent (C-V95), so the exact buffer slots are ambiguous. | `HCHK:380`, `HCHK:387` |
| G-T36 | **Loader-bound families: ids and census.** The page cites "`members/loader-bound-census.tsv` … 87 files, all rows", which does not exist; only the generator is present. The kind-9 ids of `behindcamera`/`pc_skillmotion` and the kind-7 ids of `tex2pack` (`0xD7`) and `fontpack_fs` (`0xD2`) are not on the page; they appear only in the generator. | `LBB:36`, `LBB:179-180`, `PS2-…/members/gen_loader_bound_census.py:34-46` |
| G-T37 | **Movie / TGA helpers.** The TGA probe `002DF8E0` and texture loader `00183180` are named only, and the "0x1C-stride movie table" has no layout (see C-V67). | `SF:65-66`, `SF:148` |
| G-T38 | **One boot order.** The boot steps in §1.4 are stated piecemeal across eight pages. No page gives their relative order inside `0022A0B0` (FST read vs arena init vs seeder vs `002368D0`). | `FST:71`, `EV:344-361`, `RND:398`, `ROW:874` |

---

## 3. Contradictions (statements a re-implementer would have to choose between)

Each item quotes both sides exactly as the snapshot has them, with `page:line`.

- **§3.1** lists items that change a value: a count, offset, address, constant, size, formula, layout or role. Every one
  is marked **page-text only - needs local check**, because this session cannot see the executable.
- **"Favoured"** names a side only when a dated correction, answer or superseding note on the pages settles it.
  Otherwise it says **none**.
- **§3.2** lists stale "not read / open" claims that another page or a later dated section answers, banners that
  disagree with front matter, and similar items whose fix changes no value.
- **§3.3** lists the cross-checks that came out consistent.

The ids are stable labels. Items are grouped by layer, not listed in numeric order.

### 3.1 Value-changing — page-text only - needs local check

#### File-size table, request queue, read path

**C-V1 — what slot `+0x48` holds.**
- `FST:97`: "the completion callback at slot `+0x48`".
- `RQ:287`: "`+0x48` | `+0x18` | on cancel completion (state 4) and by `0032E590` for a request not yet issued". The
  done callback is `+0x40` (`RQ:286`).
- Favoured: none. *page-text only - needs local check.*

**C-V2 — 4th argument of `0032E620`.**
- `FST:85`: "`0032E620(kind, index, dest, id, …)`".
- `RQ:86`: "`0032E620(kind, index, dest, bytes, &descriptor)`".
- Favoured: none. *page-text only - needs local check.*

**C-V3 — `0046DD50` live or dormant, and its rounding.**
- `FST:378`: "`0046DD50` (251 B) is the `02CA6068` state stepper the pump `0032E070` runs: … state 1 sizes the next
  stag[e] … (each `(x + (x>>31 & 0x7FF))` rounded down by `>> 0xB`)".
- `RQ:717`: "**`0046DD50` is dormant.** Its state word `02CA6068` has no writer but itself (whole-image scan)". `RQ:717-721`
  adds that states 1–4 are unreachable and "state 2 rounds two sizes up to `0x800`".
- The two sides differ on live vs dormant, on which state rounds, and on rounding direction.
- Favoured: none. *page-text only - needs local check.*

**C-V4 — callers of the cancel `0032E590`.**
- `RQ:321-322`: "Callers: `00280140`, `00291D90`, `002CEB40`, `002E60F0`, `002FC3C0`, `002FCF00` and the
  `003B1310`–`003B21E0` family".
- `RQ:648`: "Its direct callers are `002FC3C0`, `003B1310`, `003B1710` and `003B18E0`"; `RQ:678`: "The cancel's four
  callers …". The four-caller list equals the `0032E520` ask-callers (`RQ:133-140`).
- The P9 double-free conclusion (`RQ:675-679`) rests on the four.
- Favoured: none. *page-text only - needs local check.*

**C-V64 — size of `003EADE0`.**
- `RQ:345`: "`003EADD0` → `003EADE0` | — | 12 / 522 B".
- `RQ:891`: "`003EADE0` (512 B) — the request state machine".
- Favoured: none. *page-text only - needs local check.*

**C-V65 — how many callers `0032E040` has.**
- `RQ:119-126` lists the seven frame-mode bodies, boot `0022A0B0`, `0036EEB0` and `00379E30`.
- `RQ:945`: "`0032E040` — 38 B, 8 A-measured callers"; `RQ:828-829` names eight.
- Favoured: none. *page-text only - needs local check.*

**C-V73 — which requests `002DF6C0` serves.**
- `FST:390`: "`002DF6C0` … `0032E070` runs per request" (as the general read gate).
- `RQ:145`: kind `0xFF` → `002DF6C0`; other kinds → `0046E030` → `002DF780`.
- Favoured: none. *page-text only - needs local check.*

**C-V108 — does the builder write the caller's descriptor?**
- `RQ:438`: "`+0x04 i32 (set to 0x80000 by the builder)`", in the caller's `RequestDescriptor`.
- `RQC:90-91`: "The gated builder writes its local `+4=0x80000` ... The input descriptor remains unchanged in the
  controls."
- Favoured: none (RQC is the later contract, but it does not mark RQ as corrected). *page-text only - needs local check.*

#### Arena, tree, handles, image address

**C-V6 — address of the re-resolve flag.**
- `TREE:386`: "the `027A2E10` flag is armed, resolves `+0x30` through `003AB7F0`".
- `CSA:71`: "Global: `02B62E10`, the engine-wide re-resolve flag (RA-5)"; also `RSA:590` and `OWNC:174`. `027A2E10`
  occurs nowhere else in the folder.
- Favoured: none. *page-text only - needs local check.*

**C-V7 — the `003AB7F0` ≤ `0x40` guard.**
- `RSA:200`: "`else -> r = 0036B130(h); r <= 0x40 ? 0 : r`" (a full-pointer compare).
- `EFX:98`: "**The full 64-bit result survives unless `unsigned(sext(low32(result))) <= 0x40`**".
- `EFX:536` (EXP-084): rejected is "`low32(slot+8) ∈ {0} ∪ [0xFFFFFFC0, 0xFFFFFFFF]`".
- `EV:845-850`: "compares **the unsigned 64-bit value of the sign-extended low 32 bits** with `40` … Returned
  `100000040` is suppressed, while `100000041` survives".
- Favoured: the EFX/EV side, by the dated executed record "**Consumed 2026-09-16 (OPUS) from [`EXP-084`]**"
  (`EFX:511`). RSA is not marked. *page-text only - needs local check.*

**C-V8 — what `003AB7F0` returns for an untagged handle.**
- `EFX:421-422` (reproduction formula): "`resolve (0036B130, called via 003AB7F0): if handle == 0 or (handle & 3) == 0:
  return 0  # tag required`".
- `EFX:90`: "untagged -> return the input unchanged (`003AB846`)"; `RSA:199`: "`(h & 3) == 0 -> h (a raw pointer)`".
- Favoured: none. *page-text only - needs local check.*

**C-V13 — how many entries the rebase loops repoint.**
- `EFX:916`: `003A9BA0` "for each `rbx` step of 8 through `0x1800` … - 768 entries repointed"; `EFX:920`: "320 entries
  repointed".
- `RSA:895`: "`rbx` strides 8 from 8 to 0x1800" (767). `EFX:261-262`: teardown "(319 walked)" / "(767 walked)".
  `EV:868-874`: the helpers skip index 0.
- Favoured: none. *page-text only - needs local check.*

**C-V14 — what a below-base offset does.**
- `EFX:205-207`: "Past that the stored offset wraps and later resolves to the wrong address *inside* the arena".
- `TREE:80-81` (⚠ CORRECTED 2026-09-15, accepting EXP-083): "So the failure is not a wrap *inside* the arena as this
  page previously said — it is a fault outside it."
- Favoured: TREE (dated correction 2026-09-15). EFX §4 is unstruck. *page-text only - needs local check.*

**C-V15 — does an offset before the arena base fail to round-trip?**
- `EFX:408-409`: "**Offset before the arena base** — cannot round-trip at all". Also `EFX:551-552` and `EFX:607-608`:
  "must fail to round-trip".
- `EFX:521-524`: "executed as `off-delta-underflow`, and **it does not fail. It wraps.** `0x100 − 0x200` stores
  `0xFFFFFF00`".
- Favoured: `EFX:521-524` (EXP-084, consumed 2026-09-16, `EFX:511`). *page-text only - needs local check.*

**C-V16 — the delta bound.**
- `EFX:406`: "**`|delta| >= 2 GiB`** — pointers shift by `delta - 2^32`".
- `EFX:491`: "**`|newBase − oldBase| < 2 GiB` is off by one value.**". `EFX:168`: "−2^31 <= newBase − oldBase <=
  2^31−1".
- Favoured: the exact range (falsification pass 1, 2026-09-13, `EFX:491-494`; EXP-084 `EFX:531`).
  *page-text only - needs local check.*

**C-V17 — role of `003AB880` / `0036A000`.**
- `EXT:246`: "`003AB880` (42 B) is the alignment guard … anything misaligned tail-jumps `0036A000` (the subsystem's
  invalid-parameter handler) … the 'aligned or die' check".
- `OWN:136`: "`003AB880` removes a tagged node from its arena tree and returns payload."
- `EFX:120`: `0036A000` does the "**generation check**, then **removes the entry from the arena tree**".
- `TREE:347`: "`0036A000` requires it set, removes, clears it".
- Favoured: none (no dated correction on EXT). *page-text only - needs local check.*

**C-V18 — callers of `0024D540`.**
- `EV:1455-1456`: "called only by the three main-loop frame functions `0022B0B0`, `0022B8C0` and `0022BC20`".
- `EV:1322`: "`0024D540` is run by `MainLoop_UpdateAndRenderFrame`" (one caller).
- `EFX:620`: "run by `MainLoop_UpdateAndRenderFrame` and a 463-byte core body".
- `RSA:583` groups `0022BC20`, `0022B8C0` and `0022B6E0` as callers of {`00332590`, `00332660`, `0024D540`}.
- Favoured: none. *page-text only - needs local check.*

**C-V19 — what `0024D970`'s delta drives.**
- `EXT:224`: "the three callees consuming the queue backlog the delta represents".
- `OWNC:322`, `EFX:143-146`, `MOV:136-138`: a relocation delta applied to the lookup tables and encoded pointers.
- Favoured: none. *page-text only - needs local check.*

**C-V60 — size of `00442460`.**
- `EV:753`: "`00442460` (82 B)".
- `EXT:258`: "`00442460` (121 B)".
- Favoured: none. *page-text only - needs local check.*

**C-V61 — how many applies `00442380` makes.**
- `EV:755-757`: "7×`004304F0` … 7×`00430AF0` … 1×`0042FCF0` (4G) at `+0x230`" (15).
- `EXT:283`: "the fourteen-slot field apply".
- Favoured: none. *page-text only - needs local check.*

**C-V62 — size of `0036BC60`.**
- `EV:229`: "The full 887-byte `0036BC60` body".
- `ROW:1146`: "`0036BC60` (~179 B)".
- Favoured: none. *page-text only - needs local check.*

**C-V63 — EFX ticket pool size, and the overlap at `02EBD480`.**
- `OWN:106` / `OWN:239`: "64 slots of `0x38` at `02EBCD80`" (ends `02EBDB80`).
- `EV:1172-1173`: "`003B39E0` separately recycles matching entries in its 32-record management pool".
- `EFX:269`: "`02EBD480 + (id & 0x3F) * 0x38 + 0x10` — the character-bound container handle table". `02EBD480` is
  `02EBCD80 + 0x700`, inside the 64-slot range.
- Favoured: none. *page-text only - needs local check.*

**C-V66 — `+0x40` of the resolved record.**
- `EXT:240`: "`+0x40` adds a base offset".
- `OWNC:104`: "source size+40 is taken from header+8"; `OWN:51`: "The source header+8 supplies size+40."
- Favoured: none. *page-text only - needs local check.*

**C-V109 — rounding of the EFX copy length.**
- `OWN:83`: "a signed32 rounded-down copy".
- `OWNC:134`: "copy length is its signed-32 truncation toward zero to a multiple of16".
- The two differ for negative values. Favoured: none. *page-text only - needs local check.*

**C-V110 — role of `0036C660`.**
- `EV:71-73` and `EV:177-220`: a prefix tagger that "neither allocates nor calls a deallocator".
- `ROW:1359`: "the row fetch `0036A190` and the rebase `0036C660`".
- Favoured: none. *page-text only - needs local check.*

#### Section addressing

**C-V5 — size of the resource entry: `0xC0` or `0x50`.**
- `RSA:326-329` (J-4, "Corrected 2026-09-26"): "So these rows are **`0xC0` bytes** … `RenderStrideC0Element`"; restated
  at `RSA:773-774`.
- `RSA:743-744` names the `0x50` family `RenderResourceEntry`. `RSA:318-319` says "each row *is* a mode-1 entry" of the
  `[+0xD90]` bank.
- `OWNC:103-105`: "`RenderResourceEntry` … `0x50`". `render-resource-entry-buffer-accesses.tsv` routes every
  `00409600`/`00409780`/`00409A60` access as `EMBED RenderResourceEntry +0x10`.
- J-4 derives `0xC0` from the `+0xD98` bank (`RSA:324-326`), not the `+0xD90` bank the entry functions use.
- Favoured: none. The dated J-4 text is the one in question. *page-text only - needs local check.*

**C-V9 — size of `00409780`.**
- `CSA:231`: "`00409780` (429 B)".
- `RSA:749`: "`00409780` (`ResourceEntry_FindSectionIndexAndOffset`, ~101 B)". 101 B is `00409C30` (`CSA:52`).
- Favoured: none. *page-text only - needs local check.*

**C-V10 — outputs of `00409780`.**
- `CSA:231`: "the first hit writes its index to `*rsi` and its count to `*r9`".
- `CSA:124`: "A matching PRF root returns offset0 but leaves index=-1"; `PRF:34`: "initializes both index and offset to
  -1". These make the second output the offset.
- Favoured: none. *page-text only - needs local check.*

**C-V11 — name of `00409A30`.**
- `RSA:169`: "`ResourceEntry_FindSectionOffsetByTagAndName`".
- `RSA:797`: "`00409A30` — 33 B, 10 callers, `ResourceEntry_FindSectionOffsetByType`".
- Favoured: none. *page-text only - needs local check.*

**C-V12 — how sections are walked.**
- `RSA:398-404` (falsification 2026-09-02): "so the iteration stride **is** `0x30`"; `RSA:422-423`: "Real sections begin
  at `+0x30` (variant 0) or `+0x40` (variant 1)".
- `RSA:133-134` (SECTION-10): "These are fixed table-relative DWORD offsets, not slot-relative ones". `CSA:121-122`:
  "Version0 walks DWORD offsets at+30; version1 walks at+40 … Offsets are relative to the TABLE BASE".
- Favoured: none (the later text does not strike the earlier). *page-text only - needs local check.*

#### Authored data registry and row lookup

**C-V23 — reference count of slot `0x02EBF138`.**
- `VBF:147`: "with 720 references"; `REG:1048` and `REG:1064`: 720.
- `REG:1881`: "| 38 | `02EBF138` | **723** |".
- Favoured: none. *page-text only - needs local check.*

**C-V24 — row size of the action table.**
- `REG:433`: "at **720-byte rows**".
- `VBF:120`: "`action_data.bin` | 32,612 | **543** | **60**"; `README:28-29`: "543 records of 60".
- Favoured: none (720 is the reference count, `REG:1048`). *page-text only - needs local check.*

**C-V25 — what `00236C30` registers.**
- `REG:854`: "contains **34 `lea <slot>` / `movsxd rdx, [rax + <field>]` / `call 0x003845F0` triples".
- `ROW:251`: "**35 pairs**"; `ROW:308`: "`FUN_00236C30` makes **33** calls to `003845F0`" and 2 to `003846F0`.
- `REG:465`: "Decoding `00236C30` gives **42** field-to-slot pairs, not 34, by three routes".
- `REG:2098-2099`: "not among the 38 slot addresses the STATIC registrar `00236C30` takes individually".
- Favoured: `REG:465` over "34", inside the 2026-09-26 AG-2 answer (`REG:458`). `REG:854` and `REG:2098` are not struck,
  and the 33+2 split is not reconciled with `REG:854`. *page-text only - needs local check.*

**C-V26 — image-wide count of `003845F0` calls.**
- `ROW:343-344`: "A sweep of every `call 003845F0` in the image reports 36 registrations"; `ROW:904`: "36 `003845F0` +
  5 `003846F0` sites".
- `REG:541`: "all 42 calls of `003845F0` are handed one slot's own address".
- Favoured: none (the `REG:538` correction of 2026-09-30 is about slot 50, not ROW's census). *page-text only - needs local check.*

**C-V29 — the STATIC delivery callback.**
- `ROW:870`: "`00236C30` is not called by anyone: it is the **delivery** callback"; `REG:533`; `REG:853`.
- `ROW:841-844`: "registers the delivery stub `00238850` for loader `0x13` … On delivery `00238850` … tail-jumps to
  `00236C30(1)`"; also `ROW:1121-1122` and `REG:2277`.
- Favoured: none (no correction marker on `ROW:870`). *page-text only - needs local check.*

**C-V30 — slots with "no binder provenance".**
- `ROW:855-857`: "`02EBF000`, `02EBF0D0`, `02EBF118`, `02EBF120`, `02EBF140`, `02EBF148`, `02EBF150`, `02EBF168` — have
  **no binder-family provenance**".
- `ROW:334`, `ROW:1125`: `02EBF118` ← `003847B0` (→ `jmp 0x3845F0`). `REG:219-223`: the four `.ard` slots are bound by
  `003845F0`/`003846F0`.
- Favoured: none. *page-text only - needs local check.*

**C-V31 — array extent: 63 slots ending `0x1F8`, or 64 ending `0x200`.**
- `README:14`: "one 63-slot pointer array". `REG:370-371`: "`Registry 0x02EBF008 .. 0x02EBF1F8`" / "`i = 0 .. 62`".
  Also `REG:337-338`, `REG:1840-1844`, `REG:1927`, `REG:782`, `REG:865`.
- `REG:84`: "**Corrected 2026-09-22 (FABLE)** … This page read the array as **63 slots ending at `0x02EBF1F8`**. It ends
  at **`0x02EBF200`**"; `REG:81`.
- Favoured: 64 (`REG:84`, 2026-09-22). *page-text only - needs local check.*

**C-V32 — ROW's slot band against REG's array.**
- `ROW:198`: "The registry is a band of qword slots at `02EBEF70..02EBF3FC`" (146 slots). `ROW:349`: "47 slots"
  image-wide, counting `02EBF000` (`ROW:855`).
- `REG:497-501`: "`0x02EBF000` … **float** … The array starts cold at `0x02EBF008`".
- Favoured: none. *page-text only - needs local check.*

**C-V33 — what an out-of-range or missing table does.**
- `REG:413`: "**Bounds are fail-closed.** An out-of-range index returns a miss, not garbage". `REG:381-382`: "else fail
  closed".
- `ROW:511`: "**So a missing table faults rather than degrades**"; `ROW:515`: "**The index is not bounds-checked in
  the canonical shape**". Only nine consumers check, per `ROW:517-519` and `ROW:766-771`.
- Favoured: none (ROW's `RESOLVED 2026-09-20`, `ROW:736`, does not strike REG). *page-text only - needs local check.*

**C-V34 — the encode/decode round-trip condition.**
- `ROW:892`: "**the exact round-trip condition is `((p - base) mod 2^64) < 2^32`** … This row first read `0 <= p - base
  < 2^32` and called a 32-bit base necessary"; `ROW:98-104` says a base of `0x100000000` round-trips.
- `ROW:891`: "Executed in both directions at a base of `0x100000000`, where the round trip does not return the
  reference". `ROW:1235`: "the pair round-trips only while the base's high half is zero and the delta fits 32 bits".
- Favoured: none (the corrected row and the 2026-09-20 ruling disagree). *page-text only - needs local check.*

**C-V35 — what the twelve board slots hold.**
- `RQ:308-309`: "store **3** into registry slots `02EBF1A0`–`02EBF1F8` … the slots are completion markers". Also
  `REG:1028` and the `REG:2002` heading.
- `REG:2016`: "*Corrected 2026-09-30 (SWE2-STRUCT for OPUS, DD batch 12 …)*: the word is the buffer's address, so the
  twelve are pointers to the loaded boards".
- Favoured: pointers (2026-09-30). *page-text only - needs local check.*

**C-V36 — initial value of slot `0x02EBF198`.**
- `REG:2092`: "**Initialised in the image.** The `.data` bytes hold `0x009224A8`"; also `REG:548-552`, `REG:2080`,
  `REG:2117`.
- `REG:505`: "The slot itself is BSS"; `REG:2108-2109`: "corrects the 'initialised in the image' bullet above: the slot
  is BSS".
- Favoured: BSS (2026-09-18 / 2026-09-30). The neighbour value claimed at `REG:2093-2094` is not re-addressed.
  *page-text only - needs local check.*

**C-V37 — class 13: three slots or four.**
- `REG:1122`: "13 | `02EBF090` **+ `02EBF088` + `02EBF080`**"; `REG:1134-1135`: "it reads three slots".
- `REG:309-316` / `REG:1239-1251`: "computes class 13's upper bound by **adding four row counts**", including
  `02EBF078`. `REG:1205` still lists `02EBF078` as "Registered with no class".
- Favoured: four (`REG:1230-1236`, 2026-09-12/13). *page-text only - needs local check.*

**C-V38 — eleven or twelve generated setters.**
- `REG:363`, `REG:686`, `REG:821-822`, `REG:919`, `REG:2034`: eleven, `0x02EBF1A8`–`0x02EBF1F8`. The front-matter list
  `REG:37-47` has 11.
- `REG:877-880`: "**That walks `0x02EBF1A0`–`0x02EBF1F8` = 12 slots.**". `REG:2064`: "**Twelve setters, not eleven.**
  The generated family runs `00238390`–`002385A0`".
- Favoured: twelve. *page-text only - needs local check.*

**C-V41 — where the `0x02EBF020` (tutorial) count lives.**
- `REG:259`: "`/* 0032A26D: the count is at +0x00 */`".
- `VBF:289-292`: "**`+0x1C` is a group-end list.** … `{u32 count = 5; u32 end[5] …}`". The st2e header `+0x00` is the
  magic (`VBF:90`).
- Favoured: none. *page-text only - needs local check.*

**C-V42 — what `Row(i)` of `0x02EBF0A8` returns.**
- `REG:282`: "returns `rows + *(uint16_t *)(hdr + 8) * i`".
- `REG:295`: "returns **the row's leading dword** … a dereference, not the pointer".
- Favoured: none. *page-text only - needs local check.*

**C-V43 — the `0037C2E0` state machine.**
- `REG:293`: "state 3 loops to 1, state 4 writes `4` to `02EBF3DC` and returns 0".
- `REG:2258`: "state `3` exits".
- Favoured: none. *page-text only - needs local check.*

**C-V111 — number of `.ard` categories.**
- `REG:955`: "**Four `.ard` section categories** (`0`, `1`, `2`, `3`)".
- `REG:231`: "**The caution names four slots; there are five.**" (audit 2026-09-06); `REG:1820-1821`.
- Favoured: five. *page-text only - needs local check.*

**C-V112 — slots `00236C30` fills without `003845F0`.**
- `REG:1954-1956`: `02EBF180` is "the only slot it fills without `AreaData_BindAndRebaseSectionDescriptor`".
- `REG:468`: "two stored directly: `+4` into `0x02EBF180` and `+0x11C` into `0x02EBF200`", plus two via `003846F0`
  (`ROW:847-848`).
- Favoured: none. *page-text only - needs local check.*

**C-V113 — number of inner binders.**
- `ROW:850-853` and `ROW:904`: four (`00237FC0`, `00238160`, `00238880`, `00238660`).
- `ROW:1124-1125`: five member calls, adding `+0x40` → `003847B0`; `REG:467`: "five through the bespoke binders".
- Favoured: none. *page-text only - needs local check.*

**C-V114 — writers in the band `02EBF000`–`02EBF178`.**
- `ROW:865-867`: "has **no rip-relative writer in the image**".
- `REG:509`: "`0x02EBF178` | **2** | both **stores**, `00324558` and `0032469A`". `REG:885`: "**Eighteen slots are
  DIRECTLY written, which narrows J-B**".
- Favoured: REG (2026-09-22 narrowing). *page-text only - needs local check.*

**C-V121 — label of `0x02EBF040`.**
- `REG:1782` / `REG:1867`: "status auxiliary / timer parameters".
- `REG:1195`: "`02EBF040` | 29 | `+0xEC` | `ability_data` (augments) | 129 × 8".
- `REG:491-493` leaves it "as a lead". Favoured: none. *page-text only - needs local check.*

#### Archive, st2e, battle_pack, text

**C-V20 — the `battle_pack.bin` directory.**
- `VBF:24`: "`{u32 count 71, u32 sectionOffset[72], the last an end sentinel …}` … directory entry i at +4+4i".
- `VBF:342`: "`battle_pack.bin` opens with `{u32 count = 71; u32 offset[71]}`".
- `VBF:879`: "the offset table ends at 292 while the first offset is 296".
- `S2R:178`: "**A 71-entry offset table**, ascending, table ending `0x120`"; `S2R:182-183`: "packed, with 8-byte
  entries".
- The table end (`0x120` vs 292) and the entry width (4 vs 8) both differ.
- Favoured: none. *page-text only - needs local check.*

**C-V21 — the `word.bin` header.**
- `VBF:626`: "`{u32 count = 15; u32 headerSize = 68; u32 blockOffsets[15]}`".
- `VBF:377-381`: "**AY-4 ANSWERED 2026-09-15 (OPUS)** … `{ u32 count; u32 offsets[count+1]; payload }`, the offsets
  **absolute from the start of the file**". `BTB:23`: "`u32 offsets[16]` (first 68, last the end)".
- Favoured: AY-4 (2026-09-15). *page-text only - needs local check.*

**C-V22 — numbering of the `word.bin` command block.**
- `VBF:632`: "**Block 3, 63 entries — the player's battle command list**".
- `VBF:388` order `545 · 544 · 1 · 362 · 63 · …` puts 63 at index 4. `BTB:134-135`: bank `4` = 63 entries "the same 63
  entries as `word.bin` block 3".
- Favoured: none. *page-text only - needs local check.*

**C-V115 — the §7 heap struct after the 2026-10-01 header correction.**
- `VBF:595`: "`u32  headerSize; /* 32 */`"; `VBF:587`: heap "`== headerSize + count*recordSize`".
- `VBF:93`: "`headerSize; /* ~~32~~ 32 in 393 of 407; 0 in 14 (no record array) */`"; `VBF:1253-1255`: heap `0x20` in
  the two `mons_act` files.
- Favoured: the corrected §2 (2026-10-01). *page-text only - needs local check.*

**C-V116 — `001F4720` role and digest-tree node layout.**
- `BIG:264`: "`001F4720` / `001F3FD0` | digest-tree insert: node `{links, key +0x18/+0x20, record +0x28}`".
- `BIG:460`: "`001F4720` (176 B) | index-record accessor — `rbx = [rcx+0x30]`, `edx = dword[rcx+0x4C]`". `BIG:459`:
  `001F3FD0` "parent walk `[rdx+0x18]`" (the key offset in `BIG:135`).
- Favoured: none. *page-text only - needs local check.*

**C-V117 — frame of the stream-object offsets.**
- `PATH:72`: IsOpen tests object `+0x28`/`+0x30`/`+0x40`; `PATH:85`: path at `+0x10`; `PATH:250`: "the selector byte
  `+0x18`".
- `PATH:239`: "The resolver stores a source in only `+0x20` (route 1) and `+0x10` (route 2)". It is unstated whether
  §8's offsets are relative to `this+0x20`, the base the locale page uses for `0059EE90(this+0x20, …)`.
- Favoured: none. *page-text only - needs local check.*

**C-V118 — normalisation of the route-2 MD5 key.**
- `PATH:186-187`: skip `.`,`/`,`\`; `\`→`/`; lowercase, then MD5.
- `PATH:287`: "The MD5 key is built afresh from the caller's original path. So the first normalized copy (backslashes,
  lowercase) and its UTF-16 widening are computed and dropped".
- Favoured: none. *page-text only - needs local check.*

**C-V120 — help-action ids below 543.**
- `VBF:658`: "only 82 of 322 fall below 543".
- The table at `VBF:663-667` sums to 81.
- Favoured: none. *page-text only - needs local check.*

#### `.ard`, `.nmb`, text banks

**C-V44 — which function resolves the `.ard` path.**
- `ARDC:52` and `LDR:151-161`: the resolver is `002DF980`.
- `NMB:212`: "`ResourcePath_Get`'s eleven sites resolve to kinds 1, 4, 5, 8, 11, 13–16, 18–20, 22–25, 28, 34 and 37"
  (no 21). `NMB:216-223`: requests via `0032E620` resolve through `002DF780`. `ISR:277`: `003EA820` files its
  resources "through `0032E620`".
- Favoured: none. *page-text only - needs local check.*

**C-V45 — what `0032EB40` is.**
- `ARDC:250`: "calls the read request `0032EB40` - the same request the reader `003EA820` submits"; also `ARDC:239`
  and `ARDC:254`.
- `FST:74`: "`0032EB40` — the same lookup and rounding for the staged (2 KB-chunk) request path"; `FST:108` calls it
  the staged path's size reader.
- Favoured: none. *page-text only - needs local check.*

**C-V46 — the sibling `.fpk` request.**
- `ARDC:90`: "`003EA852 lea r8d, [rsi + 1]`", with namespace in `ecx` at `003EA840` (`ARDC:70`).
- `LDR:176`: "`field_index * 2 + 1` (`003EA83E`, via `FUN_0032eb40(0, 0x15, field_index*2+1)`)"; `LDR:585`.
- The address and the argument position both differ.
- Favoured: none (ARDC's 2026-09-29 re-measurement does not mark LDR). *page-text only - needs local check.*

**C-V47 — `003846F0` recursion and the `00384704` instruction.**
- `BTB:66-69`: "with depth left it **recurses** into each entry (`0038476B`), otherwise it **adds the section base to
  the offset in place** (`00384780`)"; "stores the image-relative encoding of the section (`0020E620`,
  `00384704`–`00384709`)".
- `LDR:376-380`: "`slot = resolve(desc)` (`00384704`–`00384709`)"; "the first `count` through a recursive call with the
  depth argument decremented …, the last in place".
- `REG:220`: `.ard` category 1 passes "a third argument zeroed".
- Favoured: none. *page-text only - needs local check.*

**C-V48 — fields rebased by `003845F0`.**
- `LDR:297-305`: `+0x0C`, `+0x10`, `+0x18`, `+0x1C`, with `+0x14` re-encoded.
- `LDR:715-716`: "descriptor fields (`+0x00`, `+0x10`, `+0x14`, `+0x18`, `+0x1C`) are recorded as rebased".
- Favoured: none. *page-text only - needs local check.*

**C-V49 — is `.ard` slot 7 zero?**
- `LDR:687-688`: "The `.ard` slot is 0 in all 166 `in` files".
- `LDR:453`: "`+0x2C` `slot7` | 0 | 166 | 0 | 151"; `LDR:457-458`: "`slot5`, `slot6` and `slot7` … are **non-zero in
  all 166 files**"; `S2R:87`.
- Favoured: none. *page-text only - needs local check.*

**C-V50 — the `.ard` trailer record.**
- `LDR:469-470`: "`{u16 id, u16 kind, u32 param}`".
- `LDR:631-633`: "8-byte `{selector, mask}` records … the selector (0–13)".
- `LDR:481`: "*(Corrected (FABLE, Claude Opus 5.5, 2026-09-26 …): the trailer is read. The same eight bytes are a
  `u32` key*"; `ARDC:185`: "`{u32 count; {u32 key; u32 mask}[count]}`".
- Favoured: key/mask (2026-09-26). `LDR:631-633` is unstruck. *page-text only - needs local check.*

**C-V51 — which locales get the `ch` tree.**
- `LDR:602-605` (CC-9, 2026-09-12): "**exactly one body touches the `.ard` slot: locale 7**".
- `NMB:779-781` (corrected 2026-09-30, for `.nmb`): "regions 7, 8 and 11 … reach the `ch` install at `002DFE58`". The
  `.ard` store `002DFE66` is 14 bytes away.
- Favoured: none for `.ard`. *page-text only - needs local check.*

**C-V52 — length of the `ch` `.nmb` run.**
- `NMB:494-495`: "contiguous stride-8 runs of 321 (`in`) and 313 + 7 (`ch`)" = 320.
- `NMB:383`: "**Both arrays are 321 entries**"; also `NMB:545` and `NMB:686`.
- Favoured: none. *page-text only - needs local check.*

**C-V53 — number of path-table bases.**
- `LDR:200-201`: "over all **83** path-table bases".
- `NMB:453-454`: "`repos-1e`'s implementation … recovered 83 array bases where `repos-3f` got 94"; `NMB:688`: "all 94
  array bases".
- Favoured: none. *page-text only - needs local check.*

**C-V54 — offset of the augment name word.**
- `BTB:166-168`: "`{u16 nameId, u16 0x5000 + row, u16 parameter, u16 0xFF}`".
- `BTB:181`: the filler reads "augments `+0x02`" as the name word; `BTB:141`: "row `+2`".
- Favoured: none. *page-text only - needs local check.*

**C-V55 — word `+2` range for rows 116–127.**
- `BTB:233-234` and `BTB:245`: "`0x5070`–`0x507F`" (16 values for 12 rows).
- `BTB:167`: "`0x5000 + row`" (gives `0x5074`–`0x507F`).
- Favoured: none. *page-text only - needs local check.*

**C-V106 — the `.nmb` assembler table.**
- `REG:1995`: `{i32 id, i32 size}` pairs.
- `NMB:314`: `{u32 size, u32 requestId}`.
- `NMB:296` "`0032E620(0x1a, i, cursor, id)`" against `NMB:315` "`0032E620(0x1A, i, cursor, size, &desc)`".
- Favoured: none. *page-text only - needs local check.*

**C-V122 — motion-index lookup `003DCA30`.**
- `LDR:677`: "`003DCA30(modelKey, groupId, class, &primary, &secondary)` sets `primary = 0x1E`".
- `REG:1977-1978`: "`003DCA30(model, motion, class, &kind, &index)` — **kind `0x1E` = 30**".
- `ARDC:188`: the rows are "`{u32 model, u16 class, u16 motion, u16 index}`", citing "`02EBF178` neighbourhood" for
  `02B58178`.
- Favoured: none. *page-text only - needs local check.*

**C-V123 — row 103 against 64 help ids.**
- `BTB:169-172`: "`listhelp_ability.bin` (64 ids, `130000`–`130063`) … row 103 → 'Increases magick power when HP is
  full.'". With `n = row` that id cannot exist.
- Favoured: none. *page-text only - needs local check.*

#### Authored expressions

**C-V56 — `0039B630`.**
- `RND:96` and `AEC:120`: the quadratic B-spline "`0.5(1-t)² p0 + ((1-t)t + 0.5) p1 + 0.5t² p2` (`0039B630`)".
- `RND:699`: "`0039B630` (170 B) is a call-free 3x3 matrix-vector transform".
- Favoured: none. *page-text only - needs local check.*

**C-V57 — the `1.0f` in `f`.**
- `RND:401`: "`01CEBBA8` | `1.0f` | 4 B | `.rdata`".
- `AEC:303-304` (falsification pass 1, 2026-09-29, `AEC:268`): "the `1.0f` in `P − B · 1.0f` is **vf00.w**
  (`01EF93FC`)", a writable cell whose writers store the `.rdata` 1.0.
- Favoured: vf00.w (2026-09-29). *page-text only - needs local check.*

**C-V58 — the colour combiner `00431430` against `00431350`.**
- `RND:118-131` / `AEC:68-76` (`00431350`): op 4 = `a × (f(b) + 1)`, op 5 = `b == a ? a : a + f(b − a)`.
- `RND:849` (`00431430`, used by `0042FDB0`): "`rbx + r9`, `rbx - r9`, `2*r9 - r8 + rbx`, `(r9+1) * rbx`, or (modes 4/5
  with `r8 != rbx`) `003A6E60(r8 - rbx)` + `rbx`". Here both 4 and 5 draw f(b−a)+a and arms 1–3 call no `f`.
- Favoured: none. *page-text only - needs local check.*

**C-V59 — "kinds 2 and 3 return 0".**
- `AEC:146`: "**Kinds 2 and 3 of the curve evaluator return 0**".
- `RND:96`: the kind byte ≥ 2 is the point count, and the flag-bit curve-selector values 2 and 3 return 0 (`00431113`).
- Favoured: none. *page-text only - needs local check.*

#### Typed list, prefetch, `.ah`, `.ta`, standard formats

**C-V27 — type-7 second-atlas distribution.**
- `TL:349-351`: "pack unit 01's 258 type-7s author `+0x40 = 0x0001` (`battle_4_c`, same as the required id)".
- The page's own `members/atlas-name-census.tsv` spreads the 258 over 8 units (unit 01 has 150), with second-atlas ids
  0/1/2/`0xFFFF` and `partytop_4_c` required in units 14–15.
- Favoured: none. *page-text only - needs local check.*

**C-V28 — distinct atlas names.**
- `TL:370`: "the arrays declare 48 distinct names but items reference only 28 — 20 names are authored yet never
  indexed".
- `members/atlas-name-census.tsv` distinct-name section: 49 rows, 28 `yes`, 21 `no`.
- Favoured: none. *page-text only - needs local check.*

**C-V119 — is the typed list's table B empty everywhere?**
- `TL:363`, `TL:406`, `TL:451-452`: "authored-empty in every shipped unit".
- `MRP:113-116` ("*Refined since (pointer 2026-09-30, SWE2-CONTRACT)*"): a populated table B ships in
  `rwg0201`/`rwg0202`.
- Favoured: MRP (2026-09-30), outside TL's 344 blobs. *page-text only - needs local check.*

**C-V67 — `002DF980` as a "0x1C-stride movie table".**
- `SF:148`: "from a 0x1C-stride movie table (`002DF980`)"; also `SF:302` and `SF:340`; `LDR:781`: "The movie table
  `002DF980`".
- `SF:341-342`: "`[0215F000][ecx*8]` gives the row head …, `[row][edx*8]` the element"; `NMB:114`: "**`ResourcePath_Get`
  — `0x002DF980`, 22 bytes**". `0x1C` = 28 = the movie kind (`FST:142`).
- Favoured: none. *page-text only - needs local check.*

**C-V68 — callers of `002DF980`.**
- `SF:340`: "22 B, 34 callers".
- `NMB:154` / `NMB:212`: "all eleven `ResourcePath_Get` call sites".
- Favoured: none. *page-text only - needs local check.*

**C-V69 — prefetch file count.**
- `PJR:5`: "| `txt` | 10,253 | `prefetchdata/<lang>`"; also `PJR:13`.
- `PJR:26`, `PFM:41`, `VBF:69`: prefetchdata 9,351. 10,253 is the archive-wide `.txt` count (`VBF:75`).
- Favoured: none. *page-text only - needs local check.*

**C-V70 — `.ah` corpus bytes.**
- `AH:33`, `AH:40`, `AH:222`: 11.7 MB.
- `AH:44`: "~~none~~ **all 2,564, 2026-09-13 (§7)** — **142,481** tokens, **12.2 MB**"; `AH:267`.
- Favoured: 12.2 MB (pass 2, 2026-09-13). *page-text only - needs local check.*

**C-V71 — the `.ta` frame clock.**
- `TA:328` / `TA:332`: "`001E5790` is the clock source (`01CEBDA0` …)". `TA:402` instead calls `001E5790` "a call-free
  mode-switch record writer".
- `TA:204`: "**`TA-1` ANSWERED 2026-09-25 (OPUS)** … its clock is that slot's time".
- Favoured: slot time (2026-09-25). *page-text only - needs local check.*

**C-V72 — identity of the memory-card icon pair.**
- `SF:189-190`: "resource-pool entries 494 and 495".
- `SF:205` (answered 2026-09-26): "kind 7, ids `0x2C` and `0x2D`".
- Favoured: none (possibly two numberings; not reconciled). *page-text only - needs local check.*

**C-V74 — `.ah` request `+0x120`.**
- `AH:103`: the buffer pointer is at `+0x120`.
- `AH:331`: "`+0x120` self-links".
- Favoured: none. *page-text only - needs local check.*

**C-V107 — number of FST files.**
- `AMAP:39`: "in all nine `FileSizeTable_*.fst`".
- `FST:41`: "**12 of 12**".
- Favoured: none. *page-text only - needs local check.*

#### PS2-era formats

**C-V75 — `.bin` file count.**
- `PR:10`: "| `bin` | 1,437 | 2,366 MB |".
- `PR:41`: "| archive entries | 1,439 |"; `UBF:21`; `FST:229`.
- Favoured: none. *page-text only - needs local check.*

**C-V76 — thirteen or fourteen loader-bound families.**
- `LBB:2`: "Thirteen .bin families"; `LBB:31`; `PR:130`.
- The page enumerates 14: 6 packs (`LBB:70-77`), 3 kind-9 (`LBB:177-181`), 5 kind-7 singletons (`LBB:270-276`). The
  87-file total (`LBB:37`) needs all 14.
- Favoured: none. *page-text only - needs local check.*

**C-V77 — clutpack slots.**
- `LBB:75` / `LBB:107`: four slots `+0x390/+0x398/+0x3A0/+0x3A8`.
- `LBB:586`: "`+0x390`/`+0x398`/`+0x3A0` populated".
- Favoured: none (pass B4 `LBB:387` "survives … `+0x390..+0x3A8`" does not strike `LBB:586`). *page-text only - needs local check.*

**C-V78 — the tex2pack slot walk.**
- `LBB:94`: "walks slots `+0x338..+0x388` in step-8 lockstep".
- `LBB:387` (falsification pass 1, 2026-09-29, `LBB:374`): "`+0x338..+0x380` step 8 … dir 10 raw at `+0x388`".
- Favoured: `LBB:387` (2026-09-29). *page-text only - needs local check.*

**C-V79 — where `00366080` writes.**
- `LBB:133`: "element *i* → `obj+0x10+i*8`".
- `LBB:742`: "resolves every entry's offset+dword into the `+0x18` pointer array".
- Favoured: none. *page-text only - needs local check.*

**C-V80 — `.btm` buffer slot base.**
- `BTM:76`: "`[022CBE00 + 0x110 + slot*8]`".
- `LBB:142`: "`+0x110+(slotIdx-1)*8` and registers face `slotIdx+0xA`".
- Favoured: none. *page-text only - needs local check.*

**C-V81 — the `.btm` ready bit.**
- `BTM:77`: "`[022CBE00 + 0x240]`".
- `BTM:152` (RC-37): "`[[022CBE00] + 0x240]`".
- Favoured: none. *page-text only - needs local check.*

**C-V82 — what `002C8EE0` loads.**
- `AS7:92`: "`002C8EE0` | `char_silhouette` load path"; also `AS7:71` and `AS7:139`.
- `LBB:276` / `LBB:287`: `monotone_chr` `7/0x74`, and "`0x75` (**no file ships — the slot stays null**)". The
  constant-request census row for `002C8EE0` names `monotone_chr.bin`.
- Favoured: none. *page-text only - needs local check.*

**C-V83 — the `02AEE810` registry.**
- `TIM2:252`: "**`FUN_0039BEC0` is the `.nfs` gate, not the TIM2 gate.**"
- `LBB:157` / `LBB:163`: `02AEE810` is "`fontVariant[0]` of an 8-pointer array", filled `[1..7]` by `0039BB60`.
  `HIMG:138` and `GMAP:82` route embedded TIM2s through `0039BEC0`.
- Favoured: none. *page-text only - needs local check.*

**C-V84 — `.cl2` id → name.**
- `CL2:90`: "`0xE2`–`0xE4` per the path arrays (`Loca_bhm`/`Loca_gil`/`Loca_rbl`)".
- `CL2:110`: "`0xE2` `Loca_gil`) and 46 (byte 2, `0xE3` `Loca_bhm`)", in the RC-30 answer of 2026-09-30 (`CL2:105`).
- Favoured: `CL2:110` (2026-09-30). *page-text only - needs local check.*

**C-V85 — `008FCE00`: menu manifest or console page table.**
- `CL2:89`: "the `.cl2` ids ride the **menu resource manifest**: `008FCE00`–`008FD2D0` … 14 `u32-2`-tagged id lists".
  `MRP:148-151`: "also manifest list …"; `MRP:154-159`: "**The manifest is a second path.**"
- `MRP:226`: "**ANSWERED 2026-09-30 with the premise refuted** … `008FCE00` is the developer console's page lay[out
  table]". `MRP:229`: "*Superseded reading, 2026-09-30*". `CL2:172` gives the extent `008FCE00`–`008FD328` (15 × 22
  u32).
- Favoured: console page table (2026-09-30). The old range and "14 lists" remain at `MRP:154-155`, `MRP:223`,
  `CL2:89` and `CL2:168`. *page-text only - needs local check.*

**C-V86 — who reads the MRP/CL2 data.**
- `MRP:246`: "The row renderer `001CD0E0`, the label filler `001D0390` and the page-header refresh `001D5260` **read the
  packages**"; `CL2:192`: "… **read the tables**".
- `MRP:226` / `CL2:172` (RC-29): those functions read the developer-console page table.
- Favoured: none (both texts dated 2026-09-30). *page-text only - needs local check.*

**C-V87 — offsets in the `_name` tables.**
- `UBF:131-132`: "a `u32` count, then that many ascending offsets".
- `UBF:26`: "`{u32 count, u32 offsets[count+1] (the last = file size)}`" (narrowed 2026-09-30).
- Favoured: `count+1` (2026-09-30). *page-text only - needs local check.*

**C-V88 — `sign` sections 1 and 2.**
- `FIVE:159`: "| 1 | `0x0EC` | 24 | `{u16, u16}` | **`0x150`** |", with section 2 also `{u16, u16}` (`FIVE:160`).
- `FIVE:206`: "***ANSWERED 2026-09-18 (FABLE)*** … Section 1 … `{u24 labelTextId, u8 buttonIndex}` … Section 2 … a
  `u16[19]` offset table … over 8-byte scene records".
- Favoured: `FIVE:206` (2026-09-18). *page-text only - needs local check.*

**C-V89 — `summoneffectdata` byte split.**
- `FIVE:408-409`: "`+0x04 … 668 B packed parameter bytes`" / "`tail 8 B zero pad`" (680 ≠ 672).
- `FIVE:412`: "*Superseded 2026-09-29 … the 668 bytes are 64 ten-byte records and a 32-byte tail.*" (that is 672).
  `FIVE:465`: "`64·10 + 4·4 + 2·4 + 8 = 672`".
- Favoured: `FIVE:465` layout (2026-09-29). The superseding sentence's "668" is itself 4 short. *page-text only - needs local check.*

**C-V90 — the map-menu loader's request API.**
- `WMAP:134-135`: "**kind-7 resource id `0xA2`** via the shared request queue (`0032E620`) in `003BC2D0`".
- `LMAP:467`: "Its loader `003BC2D0` makes three resource requests `00249210(pool, 7, id, 2)`".
- Favoured: none. *page-text only - needs local check.*

**C-V91 — the `menuhandbook.bin` id space.**
- `HCHK:69-70`: "The sibling `menuhandbook.bin`/`order.bin` pair uses a different id space (kind-6 base `0x80`)".
- `HIMG:214`: "`menuhandbook_order.bin`/`menuhandbook.bin` (ids `0xC9`/`0xC8`)" (kind 7).
- Favoured: none. *page-text only - needs local check.*

**C-V92 — the per-kind descriptor table.**
- `BINM:120`: "`00238640` | indexes the per-kind record table `0x050E53C0 + kind*8`"; `BINM:125-126`.
- `BINM:25`: "the record table 02F973C0"; `REG:542`: "`00238640`, indexes `0x02F973C0`".
- Favoured: none. *page-text only - needs local check.*

**C-V93 — `003845F0` and `+0x14`.**
- `BINM:121`: "`dword` offset fields at `rec+0xC/0x10/0x14/0x18/0x1C` relocated to absolute".
- `BINM:212` (section "*Added 2026-09-30*", `BINM:210`): "re-encodes only its `+0x14` pointer through the
  image-address codec (`0020E620`)"; also `REG:968-983`.
- Favoured: `BINM:212` (2026-09-30). *page-text only - needs local check.*

**C-V94 — CHSE `002E60F0`.**
- `CHSE:321`: "A 491-byte body this page cites calls a 256-byte Audio-filed helper"; `CHSE:322` names the helper
  `003A1650`.
- `CHSE:337`: "`002E60F0` (~62 B)", with subtree member `003A1290` (`CHSE:341`).
- Favoured: none. *page-text only - needs local check.*

**C-V95 — stride of the handbook root's handles.**
- `HCHK:380`: "`+0xC8` … `+0xF0` | six family `hchk` buffers (48-byte stride, …)".
- `HCHK:387`: "stores the six handles at `+0xC8…+0xF0`" (an 8-byte stride).
- Favoured: none. *page-text only - needs local check.*

**C-V96 — `himg` widget fields.**
- `HIMG:96`: "`+0xC9  u8 load phase (0 idle, 2 loading, 3 releasing)`"; `HIMG:99`: "`+0xD2  u8 page mode`".
- `HCHK:424-440`: "must have `+0xC9` == 1"; `HIMG:113`: "`byte[+0xD2]=type`"; `HCHK:202`: "the bound object's
  **family ordinal** byte".
- Favoured: none. *page-text only - needs local check.*

**C-V97 — ownership of `00575710` / `00576F50` / `005771F0`.**
- `LST:94`: "the pane builder `00575710` resolves rows from the loaded quest data"; `LST:113-114`: "quest-data loader /
  quest-list parent widget".
- `HIMG:137-138`: "**State 1** (`00575710` …) … registers `buf + off` as a TIM2" (handbook). `HCHK:386-388` and
  `HCHK:412`: `00576F50` / `005771F0` are the handbook bind and state object.
- Favoured: none. *page-text only - needs local check.*

**C-V98 — the `gmap` corpus.**
- `GMAP:12`: "(5 units x 7 locales)".
- `GMAP:124`: "There are 35 copies (guide00–04: 9, 8, 6, 6, 6)".
- Favoured: none. *page-text only - needs local check.*

**C-V99 — number of named regions.**
- `LMAP:621-622`: "`menumap_world.h` also defines 38 areas, 8 named regions, …".
- `WMAP:149`: "| `region_MAX 11` | 11 named region ids + 1 sentinel | match |"; `WMAP:73`.
- Favoured: none. *page-text only - needs local check.*

**C-V100 — `menumap_sub` file sizes.**
- `LMAP:624-625`: "the TZA `menumap_sub00`–`47.bin` files are 4–11 MB".
- The page's own table lists `1,051,056` (`LMAP:639`); `SLOC:45` gives "**1,049,520 B – 11,544,192 B**".
- Favoured: none. *page-text only - needs local check.*

**C-V101 — `sloc` header size and `dirOffset`.**
- `SLOC:78`: "### 2.1 Header — 16 bytes, then the directory"; `SLOC:83`: "`dirOffset    16 in 52 of 52 - the
  directory begins at +0x14`".
- `SLOC:80`: "`struct SlocHeader base=file size=0x14`"; `SLOC:89`: the directory is at `+0x14`.
- Favoured: none. *page-text only - needs local check.*

**C-V102 — `sloc` `.bin` total.**
- `SLOC:45`: "4.5 GB of `.bin` in total".
- `PR:10`: "| `bin` | 1,437 | 2,366 MB |".
- Favoured: none. *page-text only - needs local check.*

**C-V103 — `.bin` signature count.**
- `SLOC:332-333`: "**The `.bin` signature census has since measured 28 signatures over 236 logical units**".
- `PR:43`: "distinct magics | **26**, over 178 units", in "## The full census — 2026-09-19 (OPUS)" (`PR:30`).
- Favoured: `PR:43` (2026-09-19). *page-text only - needs local check.*

**C-V104 — `himg` share of `.dat`.**
- `HIMG:27-28`: "`himg` is 90% of the `.dat` extension by logical unit (309 of 343)".
- `PR:99`: "**302–309 of 343 units, 88.0%–90.1%**, depending on how the seven are assigned" (2026-09-19 census).
- Favoured: `PR:99` (2026-09-19). *page-text only - needs local check.*

**C-V105 — `lmap` array C cross-references.**
- `LMAP:305-306`: "it is `+12` **and** `+14`, each an A id from the same record in **501 of 545** entries".
- `LMAP:372`: "*(2026-09-13, FABLE, §10.3: … At native offsets it is C `+0` / `+2`, in **545 of [545]**"; `LMAP:502`.
- Favoured: `LMAP:372` (2026-09-13). *page-text only - needs local check.*

#### Handbook census against its page

**C-V39 — monster `hdat` file count (the `himg` delta base).**
- `HCHK:67-69`: "`hctg +0x14` therefore = **the family's `hdat` file count** (1 for story/world/person/tutorial, 2 for
  knowledge, 4 for monster — matching the shipped file names exactly, corpus-verified)"; `HIMG:131-132` repeats it.
- `PR:94-96`: "**7 of `.dat`'s 343 units carry different magics across locales** — `menuhandbook_monster004.dat`
  through `010`, `hdat` in some locales and `himg` in others". `members/hb-index-census.tsv` monster `hdat_files`:
  `ch 5, cn 5, de 4, es 5, fr 5, in 11, it 4, kr 4, us 4`.
- Favoured: none. A port using `2 + hdatCount` mis-numbers `himg` files in five locales unless `+0x14` varies per
  locale. *page-text only - needs local check.*

**C-V40 — `hctg +0x04`.**
- `HCHK:77`: "`+0x04  u32      familyTag  {6400, 6401, 3954, 6403, 6404, 3877} — per-family constant`".
- `members/hb-index-census.tsv` column `tag` (the u32 at hctg `+4`, per its generator) is `102` in all 54 rows.
  `HCHK:83-84` gives the same per-family numbers (`0x1900`…) as "the high 12 bits" of `+0x08`, which cannot hold them.
- Favoured: none. *page-text only - needs local check.*

### 3.2 Stale "open / not read" claims, corrected claims repeated unstruck, and banner disagreements

None of these changes a value a port would compute. Each still has to be resolved before the page can be relied on
as written. The "settled by" side is quoted when a dated text exists.

#### README and banners

**C-S1 — README: the file behind slot `0x02EBF138`.**
- Stale: `README:28-29`, "**`action_data.bin` is the file behind registry slot `0x02EBF138`**".
- Settled by `VBF:44`: "*Corrected 2026-10-01 (SWE2-STRUCT for OPUS):* the action definition table is [bound from
  `battle_pack.bin`'s directory entry `+0x3C`]", and by `VBF:910` (§12, 2026-09-12).
- Also stale: `BTB:47`, `BTB:131` "`action_data.bin` rows" (corrected inline at `BTB:86`); `VBF:490-492` "**Downgraded:**
  … a **strongly supported lead** … **AY-6.**"

**C-S2 — README entry for REG.**
- Stale: `README:13-15`, "**PARTIAL, tier 1.** **Every authored number in FFXII is reached through one 63-slot
  pointer array**".
- Against: `REG:4` (`status: DOCUMENTED`, 2026-10-01); `REG:57-60` "**Corrected 2026-09-02** … The original line said
  *"every authored number"*"; `REG:84` (64 slots).

**C-S3 — REG body banner.**
- Stale: `REG:62`, "**PARTIAL.** … five slots are identified. Most are known only by their principal consumer, three
  are unreferenced".
- Against: `REG:4`; `REG:458` "every one of the 64 slots has an identity" (2026-09-26); `REG:1000-1009` "**Result:
  OVERTURNED on two of the three.**"
- Also stale: `REG:578`, `REG:580`, `REG:593-594` (the superseded load scan), and `REG:1036-1038` "*~46 pointers*".

**C-S4 — BigFile body banner.**
- `BIG:36`: "**PARTIAL.** The container header, the load sequence and the integrity check are read at tier 1." Unstruck.
- Against: `BIG:4` `status: DOCUMENTED … (owner re-status 2026-09-30, OPUS)`.

**C-S5 — CHSE banner and "no reader".**
- Stale: `CHSE:127` "**Status is `PARTIAL` for that reason**"; `CHSE:27` "filed as a candidate for SB-2, not closed";
  `CHSE:321` "What that helper does is not read here."
- Against: `CHSE:4` (DOCUMENTED 2026-09-30); `CHSE:346` "## The reader, traced — SB-2 answered (… 2026-09-25)";
  `CHSE:322`.
- `CHSE:293` and `CHSE:308-309` are settled in place by `CHSE:313-315`.

**C-S38 — README status of Standard-Formats.**
- `README:32`: "**DOCUMENTED, tier 1.**"
- `SF:4`: `status: AUDITED`.

**C-S14 — acceptance banners.**
- `MOV:4`: "OV-49 discharged by the non-author review FRONTIER-REVIEW-AUDITSPEC-OV-ACCEPTANCE-0929"; `MOV:13`:
  "locally validated; formal independent acceptance pending". `MOV:178` names a different board task.
- `RSA:150-155`: "The front matter's "formal independent acceptance pending" is superseded by this". The same SECTION-10
  front matter still says "pending" at `CSA:30` and `EFX:28`, and `EFX:892` says "Formal independent acceptance is
  pending".

**C-S53 — EXP-079.**
- `ROW:550`: "Arena placement **observed live**: [`EXP-079`] (ASTRA, `method: C`, `live_game: true`)".
- `ROW:728-730`: "`EXP-079` — **method -**, no declared method … **None of these is a live run**".

**C-S55 — status against front-matter details.**
- `HCHK:4` `status: AUDITED` with `HCHK:17` "`hdat | mostly-explained | … record interiors only partially field-bound`".
- `BINM:4` and `HIMG:4` are AUDITED with `crossref_clean: false` (`BINM:22`, `HIMG:21`).
- The DOCUMENTED pages CMAP and WMAP say "nothing … carried as open" yet list "declared limits" (`CMAP:145`,
  `WMAP:203`).
- `MRP:4` says every row is closed, yet `MRP:219-222` names eight unrequested files of which RC-29 explains four
  (`MRP:226`).

**C-S51 — `last_reviewed` older than the page's own dated edits.**
- Queue and arena pages: `RQ:18` (2026-09-22), `OWN:10`, `EXT:10` (09-23), `ISR:10`, `PRF:10` (09-29; body to
  2026-10-02), `TREE:17` (09-13), `EFX:17` (09-23).
- Registry and expression pages: `REG:18` (09-11; body to 10-01), `ROW:17` (09-11; body to 10-02), `EV:15` (09-12),
  `RND:17` (09-08).
- VBF folder: `VBF:21` (09-12; last pass 10-01), `BIG:19` (09-03), `BKT:14`, `LDR:19`, `NMB:19` (09-04; re-status
  09-30), `BTB:19`.
- Prefetch, FST and standard formats: `AH:19`, `PFM:19`, `FST:19`, `SF:16`, `TA:20`.
- PS2 pages: `TIM2:19`, `UBF:23`, `FIVE:11`, `CMAP:16`, `WMAP:16`, `BINM:17`, `HIMG:16`.

#### Request queue and ownership

**C-S6 — "once per frame".**
- `RQ:119` "Called once per frame by `0032E040`"; also `RQ:340` and `RQ:452`.
- `RQC:65`: "This wrapper itself supplies no once-per-frame guarantee."

**C-S7 — "loose file" read issue.**
- Stale: `RQ:343` "issue a read (loose file first, then the archive)"; `RQ:355`; `RQ:449`; `RQ:710`; `FST:75`;
  `FST:51-52`; `LFR:13-15`.
- Settled by `RQ:839`: "The ~~loose-file~~ open `001D6F20` *(corrected 2026-09-27 … never a loose file …)*"; also
  `FST:309` and `PATH:239`.

**C-S8 — Windows `memcpy` overlap still open.**
- Stale: `EXT:196` "The deployed Windows copy-overlap dependency from SECTION-07 is still unresolved"; `ISR:240`.
- Settled by `MOV:175` (OV-46 "*ANSWERED 2026-09-29* … overlap-safe in all 31,784 overlapping cases"), `PRF:106`
  (OV-43) and `OWNC:353-356` (2026-09-26).

**C-S9 — held state-1 submission and single delivery still open.**
- Stale: `EXT:190` (OV-19 unchecked); `OWNC:219`; `OWNC:394-396`; `ISR:162-163`; `ISR:229`; `RQC:343`.
- Settled by `ISR:234-236` (OV-34/35/36 "ANSWERED 2026-09-29"), `PRF:105` and `RQ:627`.

**C-S10 — other owner families still open.**
- Stale: `OWN:212-214`.
- Settled by `OWN:175` ("*ANSWERED 2026-09-29 …: there are exactly four owner families*") and `EXT:191` (OV-20).

**C-S11 — OV-42 is both ticked and open.**
- `PRF:105` "- [x] ~~**OV-42.** …~~ *ANSWERED 2026-09-29*", followed by "*Narrowed 2026-10-02 … Still OPEN.*"
- `ISR:140`: "OV-42's natural rejection and OV-21 stay OPEN".

**C-S12 — OV-39's lead clause outlives its correction.**
- `PRF:102`: "the two `@FEF`-specific inputs have no shipped producer - ~~the configuration table `02B64380` is never
  populated~~ **(`CON-195` …: it is seeded at start-up …)**".

**C-S13 — README summary of the builder.**
- Stale: `README:21-23`, "the builder that sizes a request from the file-size table and stalls when no slot is free, …
  512 KB parts".
- Against: `RQ:99-100` "The bytes come from the caller"; `RQ:39-40` "Splitting is gate-dependent"; the stall is in
  `0032E870` (`RQ:102`).

**C-S54 — README priority target.**
- `README:37`: "VBF/EBP container layout (use `ff12-vbf.exe` and `ff12-script.exe`)".
- The VBF layout is read in `BIG` §3a (`BIG:4`, `BIG:108-131`).

#### Arena, tree, section addressing, expressions

**C-S15 — EFX "No harness exists".**
- `EFX:604`; also "What would move this" at `EFX:547-552`.
- Against `EFX:510-512`: "**Consumed 2026-09-16 (OPUS) from [`EXP-084`]** … **52 / 52 cases**".

**C-S16 — "4 GiB wrap" wording survives.**
- `TREE:371`: "the 4 GiB wrap is a fixture-only hazard".
- Against `TREE:267`: "*corrected 2026-09-15 from "4 GiB wrap", which described the wrong failure.*"

**C-S17 — `0036C790` rebalancing "not re-derived".**
- `TREE:168-169` and `TREE:222-223`.
- Against `TREE:175-177`: "**Re-derived 2026-09-18 — … the detail is now byte-proven.**"

**C-S18 — the `+0x18` key "not established".**
- `TREE:357` "**what the `+0x18` key measures** | **not established**"; also `TREE:249-250` and `TREE:429`.
- Against `TREE:194-197`: "**`+0x18` is the allocated payload-byte extent used by the mover (SECTION-07).**"; also
  `TREE:326-328`.

**C-S19 — RSA residue.**
- `RSA:540-541` "the nine functions that call `004096C0`": settled by `RSA:555` "**There are 17 call sites in 11
  functions, not nine.**"
- `RSA:389` "and the fail-closed default": settled by `RSA:391-394` (2026-09-30).
- `RSA:642-645` "**The extent is authored data.**": settled by `RSA:660-663` "is **falsified by the writer**"
  (2026-09-16).
- `RSA:99-100` and `CSA:114-115` say the find-by-name path returns `-1`. Narrowed by `CSA:254` (2026-09-29): "`-1` is
  the offset output of `00409780` …; the pointer finder `00409660` turns it into NULL".
- `RSA:638-639` "It is never a heap object": narrowed by `RSA:701-702`, "The bank blob itself is heap-allocated by
  `0051F9F0`".

**C-S20 — expression pages.**
- `RND:288-290` "**whatever seeds these at runtime, which is not established**": settled by `RND:398` ("Read
  2026-09-11").
- `RND:443-444` "depends on `00431080`, which is unread": settled by `RND:96` / `RND:393` ("read 2026-09-18").
- `AEC:218` and `RND:410` "**The other eleven bits of `+0x0E`**": against `RND:96`, where bits 0–3 select the curve.
- `RND:437` "the zero-bound path keeps only ops 4 and 5": against `RND:161` "**Only operator 5 survives it.**" and
  `AEC:286-294` (2026-09-29).
- `RND:408-409`: an unclosed strike leaves "takes a *context* argument this page passes through without inspecting"
  rendered as live text.

**C-S21 — "no in-image code can obtain a pointer to `01F83530`".**
- Stale: `EV:1341`; `ROW:716` "no instruction in the image writes it".
- Settled by `EV:287` (scope corrected 2026-09-25): "one in-image store route can. The texture-id table writer
  `00210570` … id `0xFFFB`"; also `ROW:441`, `ROW:464-465`.

**C-S22 — "do not assume the identity map".**
- `EV:664-665` and `EV:1050-1051`.
- Against `EV:1406-1410` (Limits 4, 2026-09-30): "**Answered.** … a logical source *n* selects arena *n* in every
  state".

**C-S56 — B10, OV-28 status.**
- `EV:4`: "OV-27 and OV-28 NOT A QUESTION".
- `EV:1395-1396`: "accepted OV-28 for the parent as SECTION-10"; `RSA:153`: "It covers OV-28 and OV-44".

#### Archive, st2e, carriers

**C-S23 — VBF residue.**
- `VBF:1042-1043` "those twelve bytes are an unread header": settled by `VBF:370-375` ("**Answered 2026-09-14**").
- `VBF:620-621` "`?` is an unmapped byte … **AY-8**": settled by `VBF:198` / `VBF:612` ("the character is `&`").
- `VBF:703` "`battle_pack.bin` … is the obvious unopened candidate. **AY-9.**": settled by `VBF:695-702` and §9/§12.
- `VBF:314`: a 2026-09-17 narrowing filed under UQ-72, superseded by `VBF:216` ("**ANSWERED 2026-09-26**").
- `VBF:1062-1063` vs `VBF:1293`: they disagree on which sections pass 7 attacked.

**C-S24 — BIG residue.**
- `BIG:441-442` "Which of the two `CreateFileA` sites opens what": settled by `BIG:256` ("**ANSWERED 2026-09-27 …:
  minidump files.**").
- `BIG:218-219` "per asset: -> FUN_0059F4A0 ReadFile leaf": against `BIG:270` ("blocks arrive through CRT `fread`") and
  `BIG:248-251` (15 pooled handles, 2026-09-30).

**C-S25 — "six token families unmentioned".**
- `BKT:80` and `BKT:148-150`.
- Settled by `BKT:111` ("*all six bound 2026-09-29*") and `BKT:123`.

**C-S26 — St2e-Carriers README.**
- `S2R:95` "a **lead, not a reading**: no loader has been consulted"; `S2R:45-48` "**Neither is explained**". Both are
  answered on LDR (`LDR:78`, `LDR:95`).
- `S2R:213-214` asks a question that `S2R:180-184` already answers ("**It does not.**").
- `S2R:110` / `S2R:125` "fpkPath ... USUALLY NULL": against `LDR:190` / `ARDC:98` ("215 `.ard` at even indices and 215
  `.fpk` at odd").

**C-S27 — `.ard` trailer "read by nothing".**
- `LDR:130-131` "**nothing reads it**"; `LDR:487-489`; `LDR:712-714`.
- Settled by `LDR:109` (CC-8, 2026-09-12), `LDR:463-464` and `LDR:515-516` ("the trailer is read", 2026-09-26).

**C-S28 — `.ard` / `.nmb` locale and table residue.**
- `LDR:523-525` "*why those two trees* remains open": settled by `LDR:593-605` (CC-9, 2026-09-12).
- `NMB:372-374` "exactly one region reaches `ch\...`": against `NMB:779-781` (2026-09-30).
- `NMB:684` "`.ard` in a separate 16-byte record array": against `ARDC:90-93` ("a flat `char*[]` at 8-byte stride").
- `NMB:785-786` "**The three 2000-entry arrays … are lower bounds**": against `NMB:395-396` ("The `entries` column is
  therefore **withdrawn**").

**C-S29 — the binder contract's §12 count.**
- `ARDC:173-174`: "assert five and ten (AB-7)".
- Against `ARDC:120` ("It makes **15** calls, in **three groups of five**", CORRECTED 2026-09-25, `ARDC:116`) and
  `ARDC:242`.

**C-S30 — LDR registry-slot ownership.**
- The front matter `LDR:27-30` lists three slots. `LDR:43` / `LDR:348` / `LDR:662` say "Four".
- `LDR:366-371`: "**`0x02EBF168` is deliberately left undeclared.**" Against `LDR:762-763`, where another page "owns
  `0x02EBF168`", and `LDR:760-761`, where another page owns `0x02EBF120` / `0x02EBF150`.

**C-S31 — text-bank residue.**
- `BTB:174-175` "How the engine composes `13000 + n` into `130000 + n` is not read": settled by `BTB:218-224` and
  `BTB:245` (2026-09-18).
- `BTB:374` "call the input helpers `001E0B90` and `0017DE60`": settled by `BTB:461-468` (2026-09-19, "the page's 'input
  helper' label is wrong").
- `LDR:362-363` / `LDR:434-437`, "which … is 'status' versus 'attributes'": partly superseded by CC-7 (`LDR:932-948`,
  2026-09-26).

#### Prefetch, `.ah`, `.ta`, FST, standard formats

**C-S32 — Prefetch README.**
- `PJR:34-36` (budget read?): answered by `PFM:102-105`.
- `PJR:47-48` (eventlist "unexamined"): answered by `PFM:142-144`.
- `PJR:13-15` and `PFM:32-33` ("pulled into memory"): against `PFM:131-132` ("**CORRECTED 2026-09-21** … **never
  read**").
- `PFM:18`, `PFM:45`, `PFM:169` and `PFM:254` say "no file opened", while `PJR:29-37` quotes file contents.

**C-S33 — PFM entry-only and open rows.**
- `PFM:159` / `AH:153` `0018A330` "❌ entry only": against `AH:315-317` ("now read", 2026-09-18).
- `PFM:164` `00597970` "the file-cache request": against `PATH:25-28` (stream-reader constructor) and `SF:69-71`.
- `PFM:150-151` / `PFM:245-246` case-insensitive lookup "not established": against `PATH:213-215`.
- `PFM:243` selector 5 "unestablished": against `PATH:136-138` / `PATH:249-250` (answered 2026-09-30).

**C-S34 — `.ah` residue.**
- `AH:18`, `AH:157`, `AH:159`, `AH:242` "No file was opened": against `AH:44` ("all 2,564, 2026-09-13").
- `AH:241` "one npc": against `AH:170-171` ("~~one npc~~ *two*", 2026-09-13).
- `AH:151` / `AH:183` builders "not read in full": against `AH:137-139` and `AH:334-336`.

**C-S35 — `.ta` residue.**
- `TA:188-190` "Not yet run": against `TA:245` (falsification pass 1, 2026-09-13).
- `TA:146` "✗ `TA-1`": against `TA:196` / `TA:204` (answered 2026-09-25).
- `TA:123-126` (TA-2 route): against `TA:280-282` and `TA:232` (answered 2026-09-26).

**C-S36 — Standard-Formats residue.**
- `SF:190` and `SF:200-201` FR-2 "is not read": against `SF:203` ("**ANSWERED 2026-09-26 … there is no such
  routine.**").
- `SF:161` "Key addresses: None" and `SF:175` "Not applicable": against the addresses in the body (`SF:59-79`,
  `SF:147-153`).
- `SF:12` / `SF:15` "one file of each extension was extracted": against `SF:146` (webm "not re-derived here").

**C-S37 — FST residue.**
- `FST:96-98` / `FST:184-185` "FZ-12" (queue unread): answered by RQ (`RQ:117`, `RQ:425-439`).
- `FST:325` "alloc/enqueue triple": against `FST:382` ("*Corrected 2026-09-30* … it does not queue it").
- `FST:237` "**Open:** none of the eight has a loader sheet": against `FST:240` and `FST:4` (2026-09-18).
- `FST:229` lists `'CCdd'` as a `.bin` signature: against `PR:59-64` ("`CCdd` was never a magic", 2026-09-19).
- `FST:25` `crossref_clean: true` despite C-V1, C-V2, C-V3 and this item.

#### PS2-era formats

**C-S39 — PS2 README residue.**
- `PR:11` "`tm2` | 447 | **likely TIM2** … candidate `standard`": against `TIM2:227` ("magic `TIM2` | … **456 / 456**",
  2026-09-13).
- `PR:130` lists `summoneffectdata` among "the kind-9 named objects", and `LBB:173` says "Kind 9 files arrive as **named
  resource objects**". Against `LBB:174-175` / `LBB:181` and `FIVE:424` ("*Corrected 2026-09-29: not a named
  object …*").

**C-S40 — TIM2 residue.**
- `TIM2:142-143`, `TIM2:155`, `TIM2:299` say `0039BF50` is unread: against `TIM2:340-349` ("SWE2-EC7-91 update
  (2026-09-20)").
- `TIM2:145`, `TIM2:156`, `TIM2:263-264`, `TIM2:296` "the four callers are still unread": against `HIMG:137-138`
  (`00575710` read) and `GMAP:82` (`003BC4E0`).
- `TIM2:160`, `TIM2:184`, `TIM2:188`, `TIM2:200` "**No file was opened**": against `TIM2:44` / `TIM2:220` ("All 456
  files were opened", §8, 2026-09-13).

**C-S41 — AS7 residue.**
- `AS7:65`, `AS7:118-121`, `AS7:129-130` ("the walker of `offsets[]` is still not isolated"): against `AS7:141`
  ("**ANSWERED** … `0024AA00`") and `AS7:148` (superseded readings, 2026-09-30).
- `AS7:4` "no registered residue left": against `AS7:146` "Review pending: `ORACLE-REQ-AUDITSPEC-RC4-5-25-30-0930`".

**C-S42 — BTM residue.**
- `BTM:121-125` (bit depth, owner, coverage "not established"): against `BTM:140` (RC-26), `BTM:143` (RC-27) and
  `BTM:154`.
- `BTM:4` / `BTM:133` "no reader" for the glyph's unknown byte: against `BTM:133-134` (UQ-364 reads `+0x04` as the
  advance width).

**C-S43 — CL2 "no traced request route".**
- `CL2:180` and `CL2:162-165`.
- Against `CL2:178` ("*Round 3 (records) RC-30:* **ANSWERED 2026-09-30** … `003C1F00` … The reader is `003C26C0`") and
  `CL2:105-116`.

**C-S44 — MRP: "four unrequested".**
- `MRP:4`: "four unrequested .mrp files come through .rdata id lists".
- `MRP:219-222` lists eight without constant requests.

**C-S45 — unnamed `.bin` residue.**
- `UBF:137` `filelistlocalin.bin` "stay open": against `UBF:138` / `UBF:141` ("Narrowed 2026-09-27").
- `UBF:135-136`, `UBF:149-152`, `UBF:229-230` say records not decoded: against `UBF:145-147` / `UBF:153-155`
  (2026-09-27).
- `UBF:13` "The document cites one address", `UBF:112` "Key addresses: None", `UBF:238` / `UBF:255` "no crossing
  section": against `UBF:238` (five addresses) and `UBF:277-279` (crossing section present).

**C-S46 — five small tables residue.**
- `FIVE:40` "the scope is seven formats"; `FIVE:46` / `FIVE:213` "In all five cases"; `FIVE:185-186` "**No reader has
  been located for any of the five files**".
- Against: §13–§14 add QST1 and `dP<d`, and readers are found at `FIVE:194-206`.
- `FIVE:140` (bwin "**Not claimed:**"): against `FIVE:201-202` (2026-09-18 / 2026-09-27).

**C-S47 — `himg` residue.**
- `HIMG:211-212` "which index table authors it is not yet traced": against `HCHK:151-152` / `HCHK:212-214` (`00575D10`
  fills `sel = word[rec+0x06]`).
- `HIMG:227` "NOT claimed: what the two completion callbacks … deliver": against `HIMG:233` ("Added 2026-09-30").

**C-S48 — `cmap` sec3 "pad".**
- `CMAP:98`: "`u16  pad;    /* +4 = 0 in all 77 */`".
- `GMAP:69`: "requests kind 7 with **id `0x496` + the record's byte `+4`**".

**C-S49 — `lst` residue.**
- `LST:137-140`: the field-level reader "is not isolated"; `+0x04 = 100` "unconfirmed".
- Against `LST:153`: "**ANSWERED 2026-09-30 … the readers are `0037EFC0` and `0037E5B0`**"; and `LST:155`.

**C-S50 — `lmap` residue.**
- `LMAP:302-303` "Left: the 8-byte block (RC-35) and array B's `+0xC` (RC-36)": against `LMAP:314-317` and
  `LMAP:559-561` (answered same day).
- `LMAP:590-591` "*"What each does is not read"* above is unchanged and still true": against `LMAP:600` ("superseded by
  that reading").
- `LMAP:322-325` "this sheet does not adopt it": against `LMAP:4` and `LMAP:565-566` ("a zone route is a map-jump
  link").
- `LMAP:451-454` "**Not claimed.**": against §10 (`LMAP:456` onward, 2026-09-13 / 2026-09-16).

**C-S52 — broken cross-references.**
- `WMAP:30-31` / `WMAP:38` cite §5/§6/§7 for content at §4/§5/§6.
- `LMAP:694` points to "wmap … §6" for the join (it is §5).
- `CHSE:125-126` and `LMAP:200-201` cite "[`sloc`] §3" for the `002DF9A0` path-table wall; SLOC §3 (`SLOC:118-172`) does
  not mention it.
- `ROW:873` cites "§M-7"; REG has no such heading.
- `FIVE:478-479` cites "§181 and §185" (line numbers, not sections).
- `RSA:712` cites a member file that does not exist (G-T11).
- `LBB:36` cites a member file that does not exist (G-T36).

### 3.3 Checked and found consistent (not contradictions)

**Archive and path**
- Entry count 89,414 appears at `VBF:61`, `README:26` and `BIG:121`.
- The bucket sum 39,653 + 39,578 + 9,351 + 832 = 89,414 (`VBF:69`, `VBF:1005`).
- `indexSize` 11,995,716 = `0x00B70A44` (`BIG:120`, `BIG:342`, `BIG:348`).
- The route-1 hash (`0x1505`, ×`0x21`, `btr 0x1F`) agrees at `PATH:176`, `PATH:352` and `TA:373-376`.
- The selector census 5 + 13 + 1 + 1 = 20 agrees at `PATH:99-107` and `PFM:134-138`.

**FST and request queue**
- `820,000` B, `0x39` = 57, `kind*5000` and `02EC3EE0` agree at `LFR:9`, `FST:42-43`, `FST:57` and `ISR:116`.
- The `+0x28` bytes and `+0x2C` offset truncated to `0x800` agree at `FST:89-94` and `RQ:105-107` / `RQ:432`.
- The request pool `022C31C0 + 64×0x80 = 022C51C0` (pending head) agrees at `RQ:766` and `RQC:139-140`.
- The owner table `02B581A0 + 80×0x1C = 02B58A60` (mask base) agrees at `ISR:38-39`.

**Arena and EFX**
- The arena record `022D7FD0 + id·0xA8`, 15 records, agrees at `TREE:298`, `RSA:831-832`, `RQ:587` and `EV:231`.
- The block header `0xFF12` / `+0x14` bit 0 agrees at `EFX:370-372` and `EV:191`.
- `0036B130` is 41 B with a `0x100000` floor (`EFX:80-83`, `RSA:201`, `EV:1280`).
- The tree generation check `word[slot+6]` vs `word[obj+0x1C]` agrees at `TREE:217` and `EFX:120`.
- `0036C790` is 359 B, and its relink agrees at `TREE:176-185` and `TREE:393-406`.
- The `00409EC0` → `00409EC8` → `00409ED3` disposal order agrees at `OWNC:155-156`, `OWNC:481` and `OWN:240`.
- The lookup buffers `0x400` / `0xA00` / `0x1800` and the 319/767 bounds agree at `OWNC:98`, `OWNC:143`, `EFX:259-262`
  and `EV:730-733`.
- The descriptor census `02B62E40+0x140 = 02B62F80`, `02CA61B0+0xA0 = 02CA6250` and `02CA74A0+0xA0 = 02CA7540` checks out
  (`RSA:695-697`).

**Authored data**
- The 18 pack offsets of `REG:1176-1195` match `ROW:257-291`.
- `0x21E` / 543 agrees at `REG:624-628`, `REG:1053-1056` and `VBF:156-159`.
- The `.ard` five-slot map agrees at `REG:219-223`, `LDR:323-329` and `LDR:612`. The row sizes 84/88/56/56 agree at
  `REG:1604` and `LDR:356-360`.
- `0x00320A59 + 0x2B9E737 = 0x02EBF190` (`REG:1361`); `0x0020E609 + 0x1D74F27 = 0x01F83530` (`REG:1414`).
- The texture-id route `0x01F83580 − 5·16 = 0x01F83530` (`ROW:434-459`).
- The `.ard` header reads (nine) agree with the binder's nine resolves (`LDR:611`, `ARDC:111`, `ARDC:241`).
- The 1,146 unit rows of slot 2 equal the 1,146 `.nmb` entries (`LDR:404`, `NMB:44`).
- The text-bank counts agree at `BTB:46`, `BTB:197` and `BTB:317`. The `0xA0` `&` / `0xAA` `:` charset agrees at
  `BTB:97` and `VBF:612`.

**Typed list**
- The combined census (344 blobs, 7,665 records, 30,546 items) agrees with `TL:343-344` and `TL:640`.
- The 20,459 atlas references = 20,181 + 278 (`TL:348`).

**PS2-era formats**
- `wmap` closes at 2,040 B (`WMAP:56-60`, `WMAP:99`); `cmap` closes at 1,760 B (`CMAP:28`, `CMAP:39`).
- The `lmap` totals A 384 / B 111 / C 545 / D 97 match the `lmap-native` output (`LMAP:256`); the size equation =
  23,852 (`LMAP:362`).
- The kind-7 ids `0xA2`/`0xA3`/`0xA4` → `+0xD8`/`+0xE0`/`+0xE8` agree at `LMAP:469-473`, `WMAP:140-142`,
  `CMAP:116-117` and `VBF:1182`.
- The handbook census totals 69/74/57/100/16/384 = 6,300 and `f16` {17,12,21,12,1,192} agree with `HCHK:45-99`.
- The `himg` file and page totals agree (2,721 files; 6,693 pages) (`HIMG:13`, `HIMG:57-85`).
- `summoneffectdata` `(9, 0x2A)` → `02AD9B60` agrees at `FIVE:439-441` and `LBB:181`. The `.btm` id table `00D10C98`
  agrees at `BTM:74` and `FIVE:198`.
- The checks named in the brief's launch notes: "Eight extensions" (`README:32`, `SF:37`, `SF:281`); the `.ico`
  overturn (`README:34-35`, `SF:24`, `SF:139-142`).

---

## 4. Rating

**Overall: NOT YET.** The core load path is documented well enough to write from the pages, once the listed
value conflicts are settled at the bytes:

> archive → path resolver → file-size table → request queue → arena / handle / image-address codec → section lookup →
> registry binding

The folder still has structural gaps that a port cannot work around:
- text decoding (G-T23, G-T24);
- the EFX specialised relocators (G-T6, G-T7);
- the two-level binder `003846F0` (G-T16);
- the field-to-area map for `.ard` (G-T21);
- several file formats whose layout is not on the page (`mg` G-T31, `sloc` G-T32, AS7 codec G-T30, TIM2 decode route
  G-T29, binmenu texture format G-T34).

On top of these, 123 value conflicts (§3.1) leave a re-implementer choosing between stated values. 94 of them have no
dated correction to settle them.

| layer | pages | rating | what blocks READY |
|---|---|---|---|
| Archive container, index, integrity | BIG, VBF §1 | **MOSTLY** | object fields and mount order (G-T26); node layout (C-V116) |
| Path resolution (RAM cache + archive) | PATH | **MOSTLY** | route-1 extension test and cache policy (G-T25); offset frame and key normalisation (C-V117, C-V118) |
| File-size tables | FST | **MOSTLY** | four disagreements with the queue page (C-V1, C-V2, C-V3, C-V73); `0032EB40` (G-T3) |
| Request queue and external-source owners | RQ, RQC, ISR | **MOSTLY** | pacer/clock/return values (G-T1); two pump branches only in the contract (G-T2); caller lists (C-V4, C-V65); size (C-V64) |
| Arena allocator, tree, handles, image-address codec | TREE, EV, MOV | **MOSTLY** | add-path tree selection and splice helpers (G-T8); handle table (G-T9); header initial values (G-T10); the guard formula (C-V7); flag address (C-V6); base lifetime is live-only (G-S6) |
| EFX source rebase and input ownership | EFX, OWN, OWNC, EXT, PRF | **NOT YET** | 38 per-element relocators, 'R' repair, `.cm` table (G-T6, G-T7); ticket id (G-T4); role conflicts (C-V17, C-V19, C-V63) |
| Section addressing | RSA, CSA | **MOSTLY** | entry size `0xC0` vs `0x50` (C-V5); section walk (C-V12); `00409780` outputs (C-V10); `00409930` body (G-T11) |
| Authored registry and row lookup | REG, ROW, VBF §2/§7 | **MOSTLY** | `003846F0` and bespoke binders (G-T16, G-T17); bounds behaviour (C-V33); registrar counts (C-V25, C-V26); row-address width (G-T20) |
| `battle_pack`, `word.bin`, text banks, text ids | VBF, BTB | **NOT YET** | directory shape (C-V20); escape codes, CJK, `002B58B0`, group-table filler (G-T23, G-T24) |
| `.ard` binder and `.nmb` | ARDC, LDR, NMB, S2R | **NOT YET** | field→area index (G-T21); resolver identity (C-V44); `0032EB40` (C-V45); `003846F0` depth (C-V47); slot 7 (C-V49); record level (G-S13); `.nmb` meaning (G-S14) |
| Authored expressions | AEC, RND | **MOSTLY** | `advance()` lives on another category's page (G-T13); curve edge cases (G-T14); colour combiner (C-V58); `1.0f` operand (C-V57) |
| Typed list (menu widgets) | TL | **MOSTLY** | type-4 drawer jump (G-T12); census conflicts (C-V27, C-V28, C-V119) |
| Prefetch, `.ah`, `.ta` | PJR, PFM, AH, TA | **MOSTLY** | `.ah` entry layout and kind-4 dispatch (G-T27); phyremaps (G-T28). Prefetch itself is resolve-and-mark only (`PFM:131-132`) |
| Standard formats (TGA, ico, `system.cnf`, csv/json, webm) | SF | **MOSTLY** | "movie table" misreading (C-V67); webm decoding is libvpx (`SF:147-153`) |
| Menu-map family (`amap`, `wmap`, `lmap`, `cmap`, `gmap`) | AMAP, WMAP, LMAP, CMAP, GMAP | **MOSTLY** | loader API (C-V90); region count (C-V99); `loc_MAX` owner (G-T33) |
| Handbook family (`hctg`, `hchk`, `hdat`, `himg`) | HCHK, HIMG | **MOSTLY** | `himg` numbering base (C-V39); `hctg +0x04` (C-V40); root stride (C-V95); widget fields (C-V96) |
| Quest, CHSE, `.btm`, `.cl2`, MRP, five small tables | LST, MQ, CHSE, BTM, CL2, MRP, FIVE | **MOSTLY** | manifest premise residue (C-V85, C-V86); `.btm` slot base and ready bit (C-V80, C-V81) |
| TIM2, AS7, `mg`, `sloc`, binmenu, unnamed `.bin` | TIM2, AS7, MG, SLOC, BINM, UBF, LBB | **NOT YET** | TIM2 route (G-T29); AS7 codec (G-T30); `mg` layout only off-page (G-T31); `sloc` records (G-T32); binmenu texture format (G-T34); registry identity (C-V83); loader census missing (G-T36) |

What would move the folder to MOSTLY overall:
1. A local byte check of the 94 unsettled §3.1 items, starting with these, which change a port's behaviour on every
   load:
   - C-V5 (entry size);
   - C-V7 (resolver guard);
   - C-V20 (`battle_pack` directory);
   - C-V33 (row bounds);
   - C-V44 / C-V45 (`.ard` request route);
   - C-V3 (`0046DD50`);
   - C-V90 (map loader API).
2. Pages for `003846F0`, the `005004C0` relocator family, `002B58B0` with the text escape and CJK encodings, the
   `00264ED0` field→area mapping, and the `mg` / `sloc` record layouts.
3. Striking the 56 §3.2 items, so that the pages say one thing each.
