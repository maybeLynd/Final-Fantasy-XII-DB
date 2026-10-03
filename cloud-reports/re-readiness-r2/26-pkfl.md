# Reconstruction readiness, pass 2: `FFXII TZA/26-PKFL-Package-Container/`

| | |
|---|---|
| Stream | R2 (reconstruction readiness, pass 2), per [`docs/cloud-briefs/re-readiness-r2.md`](../../docs/cloud-briefs/re-readiness-r2.md), part A |
| Lane | FABLE, session r2-27 |
| Date | 2026-10-03 |
| Snapshot | this repo at `b23bdddd` (text synced from XIIOnline `f9d9053b9`); no executable, archive, Ghidra or live game was used |
| Pass 1 | [`cloud-reports/re-readiness/26-pkfl.md`](../re-readiness/26-pkfl.md) (2026-10-02, snapshot `f26c5667`) |
| Status of this file | **draft / pointer**. Nothing here is evidence. Every verdict quotes a page with its location. |

Citation form: `ABBREV:line`. Line numbers are those of this snapshot. Pass 1 read only the two pages in the
folder; this pass also reads the pages and register rows that now answer pass-1 gaps, and cites them.

| abbrev. | page (relative to `FFXII TZA/`) |
|---|---|
| `PK` | `26-PKFL-Package-Container/Container/pkfl-package-container.md` (520 lines; 504 in pass 1) |
| `RM` | `26-PKFL-Package-Container/README.md` (178 lines, unchanged length) |
| `OQ` | `_index/OPEN-QUESTIONS.md` (the register) |
| `VP` | `18-Audio/the-voice-pack-slots-and-the-voice-verbs.md` |
| `QP` | `02-Resource-And-Asset-Pipeline/the-resource-request-queue.md` |
| `IS` | `02-Resource-And-Asset-Pipeline/the-indexed-source-request-from-arm-to-terminal-pump.md` |
| `AN` | `02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/area-nmb-index.md` |
| `AL` | `02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/how-the-ard-loader-binds-area-battle-data.md` |
| `WT` | `00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md` |
| `SP` | `18-Audio/Sound-Bank-And-Voice-Formats/spp-map-sound-list.md` |
| `SV` | `01-Script-VM-Native-Bridge/Interpreter-Core/script-variables-and-their-storage-classes.md` |
| `SW` | `05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md` |
| `GA` | `00-Engine-Core-Runtime/Application-Root/game-application.md` |
| `EB` | `25-EBP-Script-Container/README.md` |

## 1. Summary

**What changed since pass 1.** On 2026-10-02 OPUS put in-place corrections ("*corrected 2026-10-02, OPUS: …
re-parsed under the `{offset, size}` reading from `FFXII_TZA.vbf`, all 10,314 packages*") through `PK` §§2, 3, 5,
6, 6b and 7 and `RM`. These corrections settle most of pass 1's four-byte-era contradictions and restate the
corpus invariants under the pair reading. `PK` also gained two new sections, an interior-citation table (`PK:506-512`)
and a homed-body table (`PK:514-520`). Several structural gaps pass 1 listed as missing from the folder are answered
on neighbouring pages (`VP` §2.1-§2.5, `QP` §2.2, `AN` §3, `IS` §3) and in register rows (`FZ-12`, `FZ-19`, `FZ-20`,
`GA-5`, `CC-9`, `FRP-2`, `OV-35`). Most of those answers are older than pass 1, which read only the folder.

**Pass-1 items judged: 66.** These are pass 1's §2 gaps (S-1…S-8, G-1…G-18, U-1…U-5) and its §3 contradictions
(X-1…X-15, B-1…B-20). The contradictions are included because the brief counts "two pages that disagree" as a gap.

| verdict | S (self-stated) | G (structural) | U (unexplained) | X (value-changing) | B (stale / banner) | **total** |
|---|---:|---:|---:|---:|---:|---:|
| CLOSED | 1 | 5 | 1 | 9 | 7 | **23** |
| NARROWED | 2 | 10 | 3 | 6 | 1 | **22** |
| OPEN | 5 | 0 | 0 | 0 | 12 | **17** |
| WRONG-IN-PASS-1 | 0 | 3 | 1 | 0 | 0 | **4** |
| **total** | 8 | 18 | 5 | 15 | 20 | **66** |

Classes of the 39 still-open pass-1 items (NARROWED + OPEN): **DOC 23 · STATIC 10 · DATA 6 · RUNTIME 0**. No pass-1 item and no new gap needs
the live game. 14 of the 23 DOC items are stale text or front matter on `PK` / `RM` themselves.

**New gaps: 8.** DOC 6 · STATIC 1 · DATA 1 · RUNTIME 0 (§3).

**Rating: MOSTLY, unchanged from pass 1** (pass 1: MOSTLY overall, with three parts NOT YET). The three parts pass 1
rated NOT YET (writing a package, `(ns, index)` addressing, the sub-file request) are now **MOSTLY**: what they
lack is pointers and two narrow static reads, not structure (§4).

## 2. Pass-1 gaps

One row per pass-1 item, in pass 1's order. "Class" is given for every NARROWED or OPEN row: STATIC (a desk read
of the executable or data), RUNTIME (live observation), DATA (a census of shipped data), DOC (the answer exists on
another page, or the fix is an edit to stale text on this one).

### 2.1 Self-stated gaps (pass 1 §2.1)

| id | gap | verdict | evidence (quote + `page:line`) | still missing | class |
|---|---|---|---|---|---|
| S-1 | slot meaning | NARROWED | `.vpc` slots are now described on `OQ:2420` (GA-3, ANSWERED): "every populated slot of every `us` `.vpc` is one [`VSP1` sub-file] (510 sub-files over 201 packs), with a `u32` count at `+0x04` and *count* 16-byte records". `PK:399-400` still says "**Nothing is claimed about what any slot holds.**" and delegates the question by rule (`RM:170-172`). | What `.mot` slots 0-15 and `.snd` slots 0-15 hold is not stated on any page read. `PK` has no pointer to GA-3 for `.vpc`. | DATA |
| S-2 | no slot denominator; `Slots/`, `Variants/` | OPEN | `RM:86` unchanged: "**So the 14-pair denominator is NOT established, and no sheet should be scored against it yet.**". The populations are now stated, at 16 slots for `.mot` / `.snd` and 14 for `.vpc` / `.vpcjp` (`PK:49`, `PK:244`), but no page turns them into a denominator, and steps 2-3 of `RM:150-155` (`check_pkfl.py`, one sheet per unit) have no recorded outcome. | A stated denominator (or a statement that none is needed now that the slot ceilings are known); the fate of `Slots/`. | DOC |
| S-3 | no write path | OPEN | `PK:193` unchanged: "**The write path.** None found. Nothing in the executable emits `PKFL`." This is a stated limit. The layout rules a writer needs are now largely restated (G-2). | Nothing more can be found in the executable. A port's writer must be specified from the layout. | STATIC (stated limit) |
| S-4 | code half of the audit | OPEN | `PK:362-363`: "**The corpus half of this sheet is now independently confirmed; the code half is not.**"; the 2026-10-02 note at `PK:362` adds "the loader contract itself is still unaudited"; `PK:28` "§3 loader contract NOT audited". | An independent audit pass of §3 and the 2026-09-18 body reads (`PK:381-398`). | STATIC |
| S-5 | `ResourcePath_Init` half-read | NARROWED | `PK:200` still "◐ the slot-install region" (also `AN:552`). The locale switch is now mapped on `AL:596-605`: "The jump table (`002DFBBE`, eleven dwords at `002E04B0`) sends locale ids 1–8 and 11 to nine bodies, ids 9 and 10 and every out-of-range id to a tenth"; "The bodies re-install between four and nine pointers each — the per-locale text and menu tables at `0215F008`, `0215F010`, `0215F028`, `0215F040` …" (register `CC-9`, `OQ:1644`, ANSWERED). | Which array each locale id installs at `0215F028` / `0215F040` / `0215F128` is not tabulated (G-5). `ResourcePath_Init`'s other arguments and its `fopen` tail are unread. | STATIC |
| S-6 | crossings are tier 2 | OPEN | `PK:488` unchanged: "tier 2: ledger names, sizes and `edges.tsv`; no body read for this note"; `PK:494` "**4 of the 15 bodies on that layer are read, the rest are counted**". | Body reads behind the crossing notes. They do not block a port of the container. | STATIC |
| S-7 | where `evt_t0005`'s motion comes from | OPEN | `PK:410-411` unchanged: "while its own `.mot` is empty, so what it plays is served from another package, not from this one". No other page names that package (searched for `evt_t0005`). | Which package's `.mot` serves `evt_t0005.ebp`'s `motionread` calls. | DATA |
| S-8 | ordering under the pair reading | CLOSED | `PK:251`: "re-measured 2026-10-02 - offsets ascend in slot order in all 10,287 non-empty packages, the first at `0x800` in every one and each later payload at the next `0x800` boundary after the one before; 2026-10-02, OPUS". The same fact is restated at `PK:98`, `PK:297`, `PK:336` and `RM:94`. | — | — |

### 2.2 Structural gaps (pass 1 §2.2)

| id | gap | verdict | evidence (quote + `page:line`) | still missing | class |
|---|---|---|---|---|---|
| G-1 | byte order of header / directory words | NARROWED | The engine reads each word as a plain dword: `PK:512` (`0032F320`) "returns the dword at that pointer + `edx`*8 + 8"; `VP:86` "`0032F360(manager, slot, table)` reads `[directory + slot × 8 + 0xC]`". `PK:103` names "a little-endian dword" only for the magic scan. | No page says in words that the header and directory are little-endian. This is a one-line statement for `PK` §2. | DOC |
| G-2 | alignment / padding rule under the pair reading | NARROWED | `PK:220`: "**40,203 / 40,203** pairs, offset and size alike [`0x10`-aligned]"; `PK:251`: "the first at `0x800` in every one and each later payload at the next `0x800` boundary after the one before"; `PK:260`: "1,912 bytes in every non-empty 16-slot package and 1,528 in every non-empty 64-slot one, the first payload sitting at `0x800` in all 10,287"; `PK:406-407`: empties are "one 2,048-byte file … padded to the sector". | The value of the fill bytes between the directory and `0x800`, and between payloads. Whether a non-empty file's length is padded to `0x800` after its last payload. | DATA |
| G-3 | whether `size` is stored or decoded length; payload compression | NARROWED | For `.vpc`: `VP:86-97` sizes a block from the directory's size word and reads "**sub-file `slot` of the `.vpc` / `.vpcjp`** into the block"; `OQ:2420` (GA-3) parses those bytes directly as `VSP1` ("Those pairs **tile each sub-file exactly**: 2,554 records, 0 gaps, 0 overlaps"). So a `.vpc` payload is stored raw at its stated size. For `.mot`: `IS:95-96` "`0032F290(g,i)` gets length from the metadata pointer … and reads DWORD `metadata+0xC+8*i`", which the producer `003DD4C0` sizes from (`IS:117`). | Whether `.mot` and `.snd` payloads are compressed inside the package is not stated. | DATA |
| G-4 | path-table element format and index formula | WRONG-IN-PASS-1 | Already on `AN:114-123` (pass 1 pointed at it but listed it as a gap): "**`ResourcePath_Get` — `0x002DF980`, 22 bytes, the entire function:**" … "`mov rax, [rax + rcx*8]` … `ret -> char*`". So 22 bytes is the function's size and an element is a `char*`. The index formula is on `AN:558`: "the manager decoder: `≤0` → kind 5 `id*3`, `1..3` → kind 8 `id*4`, `4` → kind 1 `id+0x6B`", and on `VP:80-85`. | `PK:113` still reads "returns `g_pathTables[namespace][index]`, 22 bytes" with no type. A pointer to `AN:114-123` and `AN:558` would close it. | — (DOC pointer) |
| G-5 | region-variant selection | NARROWED | `OQ:2640` (FRP-2, ANSWERED 2026-09-22): "`002DF9A0` installs **ten** arrays at namespace 5 (`0215F028`), one per language - `us`, `fr`, `de`, `it`, `es`, `uk`, `kr`, `cn`, `ch`, `in`". The selection is by locale id in `ResourcePath_Init`'s switch (`AL:596-605`, S-5). | The locale-id → array map for `0215F040` (ns 8) and `0215F128` (ns 37). Where the locale id passed to `ResourcePath_Init(region, flag)` (`AN:552`) comes from. | STATIC |
| G-6 | language (ns 8 vs ns 37) selection | WRONG-IN-PASS-1 | Answered 2026-09-11, before pass 1: `OQ:2403` (FZ-19) "the table that plays is bit 10 of `[020BE6E0] + 4` (the voice-language setting)"; `VP:67-69`: "Every entry point calls `002DEBB0`, which is `bit 10 of [020BE6E0] + 4 == 0` … bit set → table 0, the `in` `.vpcjp`; clear → table 1, the language `.vpc`." Both directories are loaded for managers 1-3 (`VP:111-113`). | `PK:65-68` and `PK:124-126` still say only "the engine selects the namespace", with no pointer (see N-7). | — (DOC pointer) |
| G-7 | path → shipped file; 9 roots vs 10 variants | NARROWED | Path resolution is on `AN:231-234`: "`002DF780` refuses the request when `size[kind][index]` in the `.fst` is `-1` (`002DF7B0`). Otherwise it fetches `g_pathTables[kind][index]`". FRP-2 names the ten variants (G-5). `PK:404-405` still names nine locale roots. | Why ten path variants ship as nine locale roots of files (which two variants share a root, or which variant has no files), and the 1,809-file vs 3,290-string gap for `.vpc` (`PK:133`). | DATA |
| G-8 | when the walker "does not request a package" | NARROWED | `IS:128-131`: "A negative size takes `0032FED2 jl 0032FF25`, which loads the group's directory pointer (the `022C6E70 + 8g` table that `0032F290`/`0032F260` read) and clears its first byte at `0032FF2D`; for group > 3 that is always the path." `VP:111-113`: the `.vpc` / `.vpcjp` directories are requested only "for managers 1–3". | `IS:134-136` ("Limits kept") names its own limit: "`0032FCA0`'s sizing of `base+2`, `base+3` and kind `0x25` `base+3`, are not analysed". So the conditions behind `0032FEC7`, `0032FF98` and `00330004` (`PK:395`) are not stated. | STATIC |
| G-9 | which records feed fields +1 / +2 | NARROWED | `VP:108-113`: `0032FCA0` "maps the index to a namespace and base id exactly as §2.2 does" (manager 0 → kind 5 `index × 3`, managers 1-3 → kind 8 `index × 4`, `VP:81-83`), then requests "`.snd` (`base + 2`, `0x88` bytes → `022C6E98`), `.mot` (`base + 1`, `0x88` → `022C6E70`)". `OQ:3447` (OV-35): "the mode maps group to package namespace (1-3 to ns 8, 4 to ns 1, else ns 5)". | For manager 0 the record is ns 5 `{ebp, mot, fpk}` (`PK:120`), so `base + 2` names an `.fpk`, and `.fpk` paths "ship **zero files**" (`PK:150`). No page says what the `.snd` table holds for manager 0: whether the request is refused, sized −1 and byte 0 cleared, or something else. | STATIC |
| G-10 | manager count, buffer stride, reader arguments | CLOSED | Managers: `VP:52` "the actor-manager slot (0..4)"; `SV:301` "**The tables hold five entries, not three.**" (the `022C6D18` / `022C6D28` pair). The directory tables are per-manager pointer arrays: `IS:95` "the metadata pointer at `022C6E70+8*g`"; `PK:512` "takes the pointer at `022C6EC0` + `ecx`*8 when `r8d` is 0, or at `022C6EE8` + `ecx`*8 when it is non-zero", with `ecx` bounded ("returns -1 when `ecx` is above 3 (signed)"). Arguments: `0032F320(manager, slot, table)` / `0032F360(manager, slot, table)` (`VP:86`, `VP:94`); `0032F290(g,i)` / `0032F260` (`IS:95-96`); `0032F2F0(a, c)` / `0032F2C0(a, c)` (`IS:285`); `0032F3A0(signed byte, word mod 10)` (`PK:520`). | — (the readers' ranges for `k` are G-11) | — |
| G-11 | out-of-range `k` on a 16-slot table | NARROWED | `IS:97-98`: "The active-byte check is NOT a NULL-pointer guard; readable metadata and bounded indices are preconditions." `OQ:3447` (OV-35) gives the permitted `.mot` indices as "i 0-15". `PK:386` "the allocator `0032F430` gives each manager slot a `0x208` buffer and zeroes its first byte". | What a read at `k ≥ 16` of a `0x88`-byte load returns is still not stated. The bytes `0x88`-`0x207` of the buffer have no stated initial value or reset (see N-8). | STATIC |
| G-12 | caller handling of `-1` | CLOSED | Voice: `VP:88-89` "a size ≤ 0 loads nothing". `.mot` producer: `IS:97` "The length must be positive", and `IS:98` "The provider refuses group4 with -1". `.snd` consumer `003DF440`: `IS:285` "for `n` <= 0 (signed) it tail-jumps to `0036C140`". | — | — |
| G-13 | manager state word `022C6E48` | CLOSED | `PK:393`: "the four completions each clear one pending bit of the manager's state word `022C6E48` - `003302B0` bit 13 (`.mot`), `00331760` bit 12 (`.snd`), `00331820` bit 15 (`.vpc`), `003317C0` bit 14 (`.vpcjp`) … the walker sets the same bits, `0032FCA0+0x20A`, `+0x277`, `+0x2E2`, `+0x34E`". `VP:115-116` adds that when none remain the completion clears "bit 3 of the manager record's `+0x11` (`00263FF0`)". The other bits are on `SW:3602-3604` ("the root sets bit 1 on entry and bit 9 when the `> 0xC` section exists"), with bits 4, 5 and 6 at `SW:3610-3612`. | `PK` has no pointer to `SW` for the other bits. | — |
| G-14 | trigger and frame position of `0032FCA0`, `0032ED80`, `0032F430` | NARROWED | `OQ:2422` (GA-5, ANSWERED 2026-09-13): `0032FCA0` is "called only from `WorldSimulation_ProcessDeferredModeRequest` `0032FC30`. Its eight call sites pass manager **0** (the world tick, `003140B8`), **1** (the field pass, pack `0xD4`, `0025DAE1`), **3** (`BattleAction_InitializeGlobalSpecialSequenceMode` …), **`clamp(n + 1, 1, 3)`** (`003522C0`, `00353080` — the event-load verbs)". `WT:1263-1267` gives `0032FC30`'s early-outs and its tail call `0032FCA0`. `VP:106-107`: `0032FCA0` begins by "resetting the manager (`002628B0`, `ActorResource_ResetManagerLoadState` `0032ED80`)". `0032F430` is called at boot by World `00266D10` (`PK:502`). | The boot order of `ResourcePath_Init` (`PK:490`) and `0032F430` relative to each other is not stated. `PK` has no pointer to GA-5. | STATIC |
| G-15 | `0032E620` contract | WRONG-IN-PASS-1 | The contract was on its own page from 2026-09-11 (`OQ:2396`, FZ-12 ANSWERED): `QP:86` "### 2.2 The builder — `0032E620(kind, index, dest, bytes, &descriptor)`", with the descriptor at `QP:437-440` ("`+0x00 i32 fileOffset` … `+0x08 i32 arg` … `+0x10 ptr onDone`") and the callbacks at `QP:282-289`. The PKFL kinds are on `VP:56-58` (kind 8 for `.vpc`, kind `0x25` for `.vpcjp`) and `IS:85-88` (kind 5 for group 0, kind 8 for groups 1-3). `PK:165` now carries the five-argument form (X-12). | `PK` has no pointer to `QP`. | — (DOC pointer) |
| G-16 | `0024AB90` and `00249810` | NARROWED | `GA:1029`: "`00249810` (42 B) is the three-call allocation wrapper the pkfl page shows as `00249810(2, result)`: … `0036C1D0` runs with `edx=0xC` …, `0036A190` runs on the saved `ecx` … `0036C140` finishes". `0024AB90` appears on the request path for kind 7 (`02-…/PS2-Image-Data-Formats/loader-bound-bin-families.md:43`, "`00249180`/`0024AB90`, `0032E620` with a callback"). | No body description of `0024AB90` was found. `PK:498`'s "this page's container init" is still a dangling pointer (B-17). | DOC |
| G-17 | `PKFL_Bind` | CLOSED | The only sentence naming it is now struck: `PK:360-362` "~~`PKFL_Bind` and the slot-consumer functions were not read …~~ *(answered: the magic row rests on a body read since 2026-09-18 …)*". | — | — |
| G-18 | `.mot` occupancy under the pair reading; present-pair total | CLOSED | `PK:224`: "under the pair reading `.mot` slots 0-15 hold 1,539, 3,186, 1,737, 1,134, 774, 540, 378, 270, 108, 54, 54, 36, 36, 27, 18, 18 packages and `.snd` slots 0-15 hold 2,304 for 0-7, then 9, 1,809, 324, 225, 153, 99, 45, 18"; `PK:213`: "under the pair reading 40,203 pairs are present". Cross-check (this report's arithmetic): `.mot` 9,909 + `.snd` 21,114 + `.vpc`/`.vpcjp` 2 × 4,590 = 40,203. The `.mot` total, 9,909, also matches `OQ:2420` ("`.mot` totals 9,909 containers"). | — | — |

### 2.3 Fields or figures given without meaning (pass 1 §2.3)

| id | item | verdict | evidence (quote + `page:line`) | still missing | class |
|---|---|---|---|---|---|
| U-1 | `+0x04 slotCount` | CLOSED | `OQ:2420` (GA-3): "**`+0x04` is the directory capacity in slots, varying by family** - 16 for `.mot`/`.snd`, 64 for `.vpc`/`.vpcjp`. Verified as a prediction over all 8,505 files of the three large families: 0 slots past EOF and no file populates a slot at or beyond its own `+0x04`". `PK:391`: "Nothing compares `+0x00` or `+0x04` against any value". | `PK:164` still reads only "not read by any function read here". | — |
| U-2 | `0032F3A0` reads slot `k+8`'s size | NARROWED | The caller is now named, `PK:520` (`003DF2C0`): "calls `0032F3A0(signed byte rbx+0x11, signed word +0x12 of that qword modulo 10 (signed remainder))`"; the same body is on `SP:436`. So `k` = a word modulo 10, and the read covers `.snd` slots 8-17. | Why a `.snd` consumer wants the size of slot `k+8`, and what the record's word `+0x12` is. | STATIC |
| U-3 | the figure 321 at `PK:469` | NARROWED | The only 321 on the related pages is kind 26's array length: `AN:394` "**Both arrays are 321 entries of pure `.nmb` paths**", from the same 2026-09-04 `repos-4b` correction (`AN:819-820` "kind 26 grew from 321 to 359"). | `PK:469` does not say that this is the 321 it means. | DOC |
| U-4 | `.fpk` / namespace 21 | WRONG-IN-PASS-1 | Already described before pass 1, on `AL:596-605` and `OQ:1644` (CC-9, ANSWERED 2026-09-12): "the prologue installs the `in` tree array (`01EDC280`, 430 of 642 `.ard` / `.fpk` paths) into `0215F0A8`", with `AL` line 586 recording "215 `.ard` at even indices and 215 `.fpk` at odd". ns 5's `.fpk` triple is on `OQ:2640` (FRP-2: "rows 0/1/2 read `tst_a01.ebp`, `tst_a01.mot`, `tst_a01.fpk`"). | `PK:144-149` has no pointer to `AL`. | — (DOC pointer) |
| U-5 | `0x288`-stride records at `02098E10` | NARROWED | `VP:115-116`: each directory completion, "when none remain, [clears] bit 3 of the manager record's `+0x11` (`00263FF0`)". `WT:1271`: `0025D4D0` "`imul rcx, movsxd(ecx), 0x288` index into the `02098E10` array"; `WT:1275-1276` "The `02098E10` cell is the shared stop-registry context". | Whether the manager index used by the directory tables (0..4) is the same as the `02098E10` record index is not stated. | DOC |

### 2.4 Value-changing contradictions (pass 1 §3.1)

| id | contradiction | verdict | evidence (quote + `page:line`) | still missing | class |
|---|---|---|---|---|---|
| X-1 | directory end `0x48` vs `0x88` | CLOSED | `PK:260-261` is struck ("~~And in **2,268 files the smallest present offset is `0x40`**…~~"); `PK:270` now reads "`+0x08 .. +0x88`, and `+0x40` / `+0x44` are slot 7's offset and size"; `PK:333` "~~2,268~~ 0 … the smallest offset is `0x800` in all 10,287 non-empty packages"; `RM:93-94` is struck. | — | — |
| X-2 | gap to first payload 1,976 / 1,784 | NARROWED | `PK:260` now reads "1,912 bytes in every non-empty 16-slot package and 1,528 in every non-empty 64-slot one … the old gaps were measured from `0x48` / `0x108`". | `PK:332` (§6b) still reads "gap to first payload \| 1,976 in 4,356; 1,784 in 3,573 \| **identical**", unstruck. Only the blanket note at `PK:318` ("under the same withdrawn four-byte entry") covers it. | DOC |
| X-3 | slots used: 0–27 vs 0–15 / 0–13 | CLOSED | `PK:49` corrected ("~~**0–27**, densely~~ **0–15** in `.mot` / `.snd` and **0–13** in `.vpc` / `.vpcjp`"); `PK:224` relabels the old table "**The four-byte reading's word occupancy, withdrawn below:**"; `RM:98-99` reads "~~36~~ 50 of the 64 … Nothing above index ~~27~~ 13". | — | — |
| X-4 | the frozen census `.tsv` | NARROWED | `PK:53`: "10,314 common paths, which agree only because both parses used the withdrawn four-byte entry *(… 27 of its 10,314 rows agree - the empty packages; a re-freeze is SWE2-DATA's)*"; also `PK:222`, `PK:295`. | The `.tsv` is still the four-byte census; the re-freeze is assigned but not done. | DATA |
| X-5 | `0x40` as an in-directory alias, or a size | NARROWED | `PK:298` corrected: "the repeated `0x40` is a size - 14,337 `.snd` pairs have size `0x40` - and `+0x40` of a 16-slot package is slot 7's offset word"; `PK:308` corrected; `PK:253` heads §5's three items "*as first read; see the correction above*". | Unstruck aliasing text remains in the body: `PK:265-267` ("**2,349 of 10,314 files have two or more slots pointing at the same offset**"), `PK:271-273` ("they point at slot 14's own directory entry"), the box `PK:275-280`, `PK:282-286`, and §6b rows `PK:330-331`, `PK:334-335`. See N-2. | DOC |
| X-6 | second word as "descriptor" | CLOSED | `PK:401-402`: "~~no reading of "even = data, odd = descriptor" is asserted~~ The second word of each pair is the slot's size, not a descriptor *(corrected 2026-10-02, OPUS: `0032F360+0x2E` reads `[table + 8k + 0xC]` as the size …)*". | — | — |
| X-7 | slot length: computed vs stored | CLOSED | `PK:97-98` struck, with the correction "a slot's length is its stored size, which `0032F360` reads at `+0xC + 8k`"; `PK:256-257` struck. `RM:77-79` sits under the `RM:39` "Withdrawn 2026-09-11" banner. | — | — |
| X-8 | offsets ascending in slot order | CLOSED | `PK:251` (see S-8); `PK:255`, `PK:297`, `PK:336`, `PK:357-358` corrected; `RM:92-93` struck. | — | — |
| X-9 | header inert vs byte 0 load-bearing | CLOSED | `PK:108`: "Corrupting bytes 1-3 changes nothing, and so does any non-zero byte 0; a zero byte 0 makes every slot read of the package return -1"; `PK:163`: "**bytes 1-3 yes, byte 0 no**". | — | — |
| X-10 | six vs seven readers; scope of `0032F320` / `0032F360` | NARROWED | Count settled: `PK:387` "exactly ~~six~~ seven slot readers *(corrected 2026-10-02, OPUS: … a grep of every reference to the four tables finds these seven, the allocator `0032F430` and the walker `0032FCA0`)*"; `PK:398` "the ~~six~~ seven readers". Scope settled at `PK:189`, `PK:207` and `RM:44`: "`0032F320` / `0032F360` read only the two 64-slot tables, picked by `r8d`". | The §4 key-address table (`PK:197-203`) still lists none of the seven readers, and `PK:205-209` names `0032F2C0` / `0032F2F0` / `0032F3A0` but not `0032F260` / `0032F290` ("two readers read the `.mot` table"). | DOC |
| X-11 | two vs four completions | CLOSED | `PK:393` (G-13) and `PK:398`: "the ~~two~~ four completions read in full". | — | — |
| X-12 | `0032E620` argument list | CLOSED | `PK:165`: "~~`0032E620(kind, packId, dest, size)` with that offset as the request's file offset~~ `0032E620(kind, packId, dest, size, &record)` with that offset as the record's first dword *(corrected 2026-10-02, OPUS: `003E9EF0+0x36` stores the `0032F320` result at `[rsp + 0x30]`, `003E9EF0+0x64` passes `rsp + 0x30` as the fifth argument …)*". This agrees with `QP:86`, `QP:437-438` and `VP:95-97`. | — | — |
| X-13 | 74,340 present offsets; `0x10` alignment | CLOSED | `PK:213`: "~~74,340 present offsets~~ 74,340 non-zero words of the four-byte reading … under the pair reading 40,203 pairs are present"; `PK:220`: "**40,203 / 40,203** pairs, offset and size alike". §6b rows `PK:326-328` are unstruck but sit under the `PK:318` note. | — | — |
| X-14 | README counts from the four-byte reading | NARROWED | `RM:113`: "**~~2,952~~ 4,761 files do not fill their pairs contiguously from 0.**"; `RM:117`: "Pairs per file range ~~0–14~~ 0–15; 4,212 files carry exactly one pair, ~~2,331~~ 558 carry eight". | The surrounding sentences were not updated (N-3), and "4,212 files carry exactly one pair" carries no re-measured mark (N-4). | DOC |
| X-15 | EBP's 10,045 vs 1,115 | NARROWED | `EB:4-5`: "**1,115 scripts per language, nine languages, 10,045 files in the archive.**" So 1,115 is one language's count, not a second total. | This report's arithmetic: 1,115 × 9 = 10,035, ten short of 10,045. Neither `EB` nor `RM:3` explains the ten. Out of this system's scope. | DOC |

### 2.5 Stale claims and banner disagreements (pass 1 §3.2)

| id | item | verdict | evidence (quote + `page:line`) | still missing | class |
|---|---|---|---|---|---|
| B-1 | `status: AUDITED` vs "§3 loader contract NOT audited" | OPEN | `PK:4` and `PK:28` unchanged; `PK:362-363` "the code half is not". | Front matter that agrees with §6b. | DOC |
| B-2 | `last_reviewed: 2026-09-04` | OPEN | `PK:19` unchanged, while the body carries 2026-10-02 corrections throughout (e.g. `PK:49`, `PK:98`, `PK:393`). | A current date. | DOC |
| B-3 | `passes: 1`, `last_pass: 2026-09-05`, `reopened_count: 0` | OPEN | `PK:26-30` unchanged, after the 2026-09-11 withdrawal (`PK:426-437`) and the 2026-10-02 re-parse. | Front matter that records the reopen. | DOC |
| B-4 | `crossref_clean: true` | OPEN | `PK:29` unchanged; N-2, X-2 and X-5 are still internal disagreements on `PK`. | — | DOC |
| B-5 | `corpus_validated` cites the 2026-09-04 parse | CLOSED | `PK:18`: "# <- corrected 2026-10-02, OPUS - that parse read the withdrawn four-byte entry; re-parsed under the pair reading 2026-09-11 (section 5) and 2026-10-02". | — | — |
| B-6 | `verified: 9 cited function entries` | OPEN | `PK:14` unchanged. The page now also cites the seven readers, four completions, `0032F320`'s interior (`PK:512`) and `003DF2C0` (`PK:520`). | A provenance count that covers the functions cited since 2026-09-11. | DOC |
| B-7 | "It is still weaker than a body read" | CLOSED | `PK:296`: struck, "*(answered: §7 closed it 2026-09-18 by a body read of every directory reader; 2026-10-02, OPUS)*". | — | — |
| B-8 | "`PKFL_Bind` … were not read" | CLOSED | `PK:360-362` struck and answered (G-17). | — | — |
| B-9 | "The engine never walks the directory" vs "The walker exists" | OPEN | `PK:187` and `PK:371-372` unchanged. Wording only; no value differs. | One term for `0032FCA0`. | DOC |
| B-10 | "every occupied slot has its even/odd partner" kept as a qualified truth | OPEN | `RM:82-84` ("**What survives.** … is **true, 10,314 / 10,314** — but it is **partly an artefact of that aliasing**") and `PK:275-280` are unchanged and unstruck. `RM:82-84` sits inside the section the `RM:39` banner withdraws. | Strikes, or a banner on `PK:263-286` (N-2). | DOC |
| B-11 | "the 14-pair denominator is NOT established" | OPEN | `RM:86-90` unchanged (S-2). | — | DOC |
| B-12 | `RM:128-133` "Not measured, and required before any sheet is written" | CLOSED | Unchanged, but under the heading "## What the sample said before the census (superseded)" (`RM:120`); answered by `RM:21-34` and `PK:381-397`. | — | — |
| B-13 | `RM:136-138` "PKFL indices 0–27 are all occupied" | CLOSED | Under the same "superseded" heading (`RM:120`); `RM:98-99` now reads 0-13. | — | — |
| B-14 | `RM:157-158` "Until step 1 lands … a sample estimate" | CLOSED | Settled by `RM:21-24` "CENSUSED — 10,314 of 10,314". | — | — |
| B-15 | `Slots/` and `Variants/` planned | OPEN | `RM:165-166` unchanged; neither folder exists in the snapshot. `Variants/`'s question is answered (`RM:34`). | Remove or re-scope the two rows. | DOC |
| B-16 | attribution of `0032E620` | OPEN | `PK:494`, `PK:496` and `PK:499` still call `0032E620` "page-cited" / "on this page", while `PK:500` lists it as a Resource body. Its own page is `QP` (FZ-12). | — | DOC |
| B-17 | "this page's container init" | OPEN | `PK:498` unchanged. No section of `PK` is a container init. `00249810` is described on `GA:1029` (G-16). | — | DOC |
| B-18 | duplicate Script_VM bullet | OPEN | `PK:501` and `PK:504` are still identical. | — | DOC |
| B-19 | the 1,809 / 1,809 explanation | NARROWED | `OQ:2640` (FRP-2) now names ns 5's ten arrays as ten languages, and `VP:111-113` shows both `.vpc` and `.vpcjp` loaded per pack. `PK:68` and `PK:124-126` are unchanged. | Why the `.vpc` and `.vpcjp` *file* counts are equal (1,809 each) when the string counts are 3,290 and 658 (`PK:133-134`) is still not stated (see G-7). | DOC |
| B-20 | `RM:50-60` median table | CLOSED | Unstruck but under the `RM:39-46` banner ("this section's headline, its medians and the aliasing story below all read sizes as offsets … Kept as history."). | — | — |
