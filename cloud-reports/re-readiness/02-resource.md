# Reconstruction readiness — `FFXII TZA/02-Resource-And-Asset-Pipeline/`

| | |
|---|---|
| Stream | R (reconstruction readiness), per [`docs/cloud-briefs/re-readiness.md`](../../docs/cloud-briefs/re-readiness.md) |
| Board task | `OPUS-CLOUD-R-READINESS-02-1002` |
| Date | 2026-10-02 |
| Snapshot | this repo's text snapshot at `f26c5667` only; no executable, Ghidra or live game was used |
| Status of this file | **draft / pointer**. Nothing here is evidence. Every item quotes or paraphrases a page and gives `page:line`. Text is quoted as the snapshot has it; several of these pages are being edited by other lanes. |

COUNTS-PLACEHOLDER

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
