# Reconstruction readiness — `FFXII TZA/26-PKFL-Package-Container/`

| | |
|---|---|
| Stream | R (reconstruction readiness), per [`docs/cloud-briefs/re-readiness.md`](../../docs/cloud-briefs/re-readiness.md) |
| Board task | `OPUS-CLOUD-R-READINESS-26-1002` |
| Date | 2026-10-02 |
| Snapshot | this repo's text snapshot only (`f26c5667`); no executable, Ghidra, archive or live game was used |
| Status of this file | **draft / pointer**. Nothing here is evidence. Every item is a quotation or a paraphrase of a page, with its location. Pages in this folder are being edited by other lanes; every quotation is of the snapshot text. |

**Counts:** _filled in when the report is complete._

Citation form: `ABBREV:line`, where the abbreviation stands for a page path relative to
`FFXII TZA/26-PKFL-Package-Container/`. Line numbers are those of the snapshot file.

| abbrev. | page | lines |
|---|---|---:|
| `RM` | `README.md` | 178 |
| `PK` | `Container/pkfl-package-container.md` | 504 |

"Not stated" means neither page says it. Where a point is made only on a page outside this folder, it is given
as a path from `FFXII TZA/` and marked as outside the audited set; those pages were not read for this report
(only their existence was checked, so that the links on `RM`/`PK` could be called live or dead).

## Pages read

Both `.md` files in the folder were read in full (682 lines). The folder holds **no member `.tsv`**: the two
data files the pages lean on, `pkfl-container-census.tsv` (`RM:23`, `PK:52`) and `format-magic-census.tsv`
(`RM:178`), are workstation paths (`Tools\work\formats\…`) and are not in this snapshot, so no layout or count
could be confirmed against a `.tsv`. Every count below is page text.

The census script named on `RM:23`, `tools/analysis-kit/gfz-scripts/census_pkfl_container.py`, **is** in the
snapshot (outside the audited set). It was opened only to see which entry width the frozen census used:
`read_dir` returns `"(slotCount, [offsets])"` and unpacks `"<%dI" % n` four-byte words from `+8`
(`census_pkfl_container.py:46-52`), i.e. the **withdrawn** four-byte reading. So the frozen `.tsv` that `PK:52`
and `PK:222` say the sheet "agrees" with was built under the reading `PK:232-237` withdraws (see X-3).

All seven relative links the two pages make into other folders resolve in the snapshot (`18-Audio/the-voice-pack-slots-and-the-voice-verbs.md`,
`18-Audio/Sound-Bank-And-Voice-Formats/sab-sound-bank-container.md`, `02-…/St2e-Carriers/area-nmb-index.md`,
`02-…/St2e-Carriers/README.md`, `02-…/vbf-archive-and-st2e-tables.md`, `_index/ASSET-FORMATS.md`,
`25-EBP-Script-Container/README.md`). The three sub-folders `RM:160-166` lists (`Container/`, `Slots/`,
`Variants/`) — only `Container/` exists.

| page | front matter / status as the page states it | in-body banner or dated text that differs |
|---|---|---|
| `RM` | no front matter; heading `## CENSUSED — 10,314 of 10,314, 2026-09-04` (`RM:21`) | `> ### ⚠ Withdrawn 2026-09-11 — the pairing is the directory's entry width` (`RM:39`) over a section whose earlier box says `⚠ The reading below was WRONG. Corrected 2026-09-04` (`RM:62`); two later sections (`RM:96`, `RM:111`) carry no banner |
| `PK` | `status: AUDITED — the layout, the walker and the corpus read; the four residues of section 7 closed 2026-09-18 …` (`PK:4`); `evidence_tier: 1` (`:6`); `last_reviewed: 2026-09-04` (`:19`); `audit: passes: 1`, `last_pass: 2026-09-05`, `last_pass_state: … §3 loader contract NOT audited`, `crossref_clean: true`, `reopened_count: 0` (`:26-30`); `verified: 9 cited function entries` (`:14`) | "while auditing why this page still reads `PARTIAL`" (2026-09-14, `PK:374`); body corrections dated 2026-09-11 (`PK:81`, `:232`, `:426`) and closures dated 2026-09-18 (`PK:381`, `:403`, `:412`, `:418`); crossings dated 2026-09-18 (`PK:498`) |

---

## 1. Interface

The system is a **file format plus a small loader surface**. The pages divide it into: the on-disk layout
(§1.1), how a package is named and located (§1.2), how the engine loads and indexes a package's directory
(§1.3), how a slot's payload is then requested (§1.4), state (§1.5), order (§1.6) and dependencies (§1.7).
Slot *payload* meaning is out of scope by the pages' own rule: "**What a slot's payload *means* belongs to the
owning system** — motion payloads to `17-Presentation-Rendering`, audio payloads to `18-Audio`" (`RM:170-171`;
again `PK:399-400`).

### 1.1 On-disk layout (the current reading, 2026-09-11)

**Header** — a `struct` fence, eight bytes (`PK:72-75`):

```
+0x00  char[4]  magic       'PKFL' -- 10,314 / 10,314
+0x04  u32      slotCount   16 (.mot, .snd) or 64 (.vpc, .vpcjp); no file mixes them
```

**Directory** — "**Corrected 2026-09-11 (§8): the directory is `slotCount` pairs of `{u32 offset, u32 size}`**,
eight bytes per slot, `{0, 0}` meaning the slot is absent; it ends at `8 + 8 × slotCount` — **`0x88`** for a
16-slot package, **`0x208`** for a 64-slot one" (`PK:81-84`), and as prose:
`+0x08  { u32 offset, u32 size }[slotCount]   file-relative; {0, 0} = slot absent` (`PK:86`). It is not fenced
on purpose: "the array length is `slotCount`, a runtime value, and `check_layouts.py` requires a literal"
(`PK:88-89`). The directory is "**indexed, not packed** … a slot's index is its identity and a zero entry means
that index is unused in this package" (`PK:91-93`).

| item | value as stated | where |
|---|---|---|
| file population | 10,314 = `.mot` 4,392 (2,552 MB), `.snd` 2,304 (146 MB), `.vpc` 1,809 (1,240 MB), `.vpcjp` 1,809 (1,298 MB), all under `ps2data/plan_master` | `RM:6-11`, `PK:43-48` |
| `slotCount` by extension | 16 for `.mot`+`.snd` (6,696 files), 64 for `.vpc`+`.vpcjp` (3,618); "**No file mixes them.**" | `RM:29-34`, `PK:74`, `PK:218` |
| entry bounds (pair reading) | "`{offset, size}` pairs with `8 + 8n ≤ offset` and `offset + size ≤ file` — **10,314 / 10,314 packages**" | `PK:242` |
| lone zeros | "pairs with exactly one of offset / size zero — **0**" | `PK:243` |
| slots used | "`.mot` and `.snd` indices 0–15; `.vpc` and `.vpcjp` indices **0–13** of 64" | `PK:244`; ceiling restated `PK:419-420` |
| `.snd` occupancy | "every package fills slots 0–7; slot 9 in 1,809" | `PK:245` |
| `.vpc` / `.vpcjp` occupancy by slot | "identical occupancy by slot (1,782, 945, 702, 441, 279, 180, 126, 36, 27, 27, 18, 9, 9, 9)" | `PK:246` |
| `.mot` occupancy by slot | **not stated** under the pair reading | — |
| first payload | "the first payload at `0x800` (now the first *pair's* offset)" survives | `PK:249-250` |
| empty packages | 27: `spc_z0000.vpc` / `.vpcjp` and `evt_t0005.mot`, nine locale copies each, each "one 2,048-byte file, `PKFL`, count word 64 or 16, and every `{offset, size}` pair zero, so the header and the empty directory alone, padded to the sector" | `PK:247`, `PK:337`, `PK:403-407` |
| worked directory | "`nal_a0100.snd`'s directory reads `{0x800, 0x2300}, {0x3000, 0x40}, {0x3800, 0x40} …` — the `0x40`s are sizes" | `PK:431-432` |
| byte order | **not stated** for the directory words; only implied by the image scan "as ASCII, LE dword, BE dword and reversed" (`PK:338`) and the byte dump `00 40 00 00 40 00 00 00` (`PK:272`) | — |
| write path | "None found. Nothing in the executable emits `PKFL`." | `PK:193` |

### 1.2 Addressing: `(namespace, index)` through the resource path table

"**A package is addressed as `(namespace, index)`** through the resource-kind path table …
`ResourcePath_Get` (`0x002DF980`) returns `g_pathTables[namespace][index]`, 22 bytes, **with no bound on either
argument.**" (`PK:110-114`). Its full definition lives on
`02-Resource-And-Asset-Pipeline/…/St2e-Carriers/area-nmb-index.md` §3 (outside the audited set; linked `PK:112`).

| namespace | table slot | record | maps | region variants | stride | where |
|---:|---|---|---:|---:|---|---|
| 5 | `+0x028` (`0x0215F028`) | `{ebp, mot, fpk}` | 709 | 10 | `i%3 == 0,1,2` | `PK:120`, `PK:201` |
| 8 | `+0x040` (`0x0215F040`) | `{ebp, mot, snd, vpc}` | 329 | 10 | `i%4 == 0,1,2,3` | `PK:121`, `PK:202` |
| 37 | `+0x128` (`0x0215F128`) | `{ebp, mot, snd, vpcjp}` | 329 | 2 | `i%4 == 0,1,2,3` | `PK:122`, `PK:203` |

- **Entry point `ResourcePath_Get`** `0x002DF980`: "`g_pathTables[ns][index]`, no bounds check; table base
  `0x002DF983`, ns fetch `0x002DF98D`, index fetch `0x002DF991`" — "✅ full body" (`PK:199`). Callers named on
  the page: Presentation `001BB2B0` (`PK:499`), Resource `002EEEE0`, `001DA290` (`PK:500`), WorldAreaField
  `00379A10` (`PK:503`); "Consumers reach them through `ResourcePath_Get`" (`PK:158`).
- **Entry point `ResourcePath_Init`** `0x002DF9A0`: "installs ns 5 (`0x002DFC03` and nine more), ns 8
  (`0x002DFBE7` and nine more), ns 37 (`0x002DFB7E`, `0x002DFE74`)" — "◐ the slot-install region" (`PK:200`);
  "ten writes each to `0x0215F028` and `0x0215F040`, two to `0x0215F128`, all inside `0x002DF9A0`" (`PK:157`).
  Caller: "called from the 978-byte core start-up root" (`PK:490`); the root's address is **not stated**.
- **Language selection.** "Namespaces 8 and 37 are the same 329-map set differing only in the fourth field … **one
  authored map list, two namespaces, and the engine selects the namespace.**" (`PK:124-126`; also `PK:65-68`).
  *How* the engine selects (which setting, which function) is **not stated**.
- **Corroboration** by `.rdata` string counts (`PK:130-136`) and strings ÷ stems (`PK:138-142`, `PK:300`, `PK:302`).
- **`.fpk`**: "709 map stems × 10 (namespace 5) + 215 area stems × 2 (namespace 21) = 7,520" and "the 7,520
  `.fpk` paths … ship **zero files**" (`PK:144-154`).

### 1.3 Directory load and slot readers (the "walker", 2026-09-11 / 2026-09-18)

"The engine never walks the directory: it loads the directory's bytes as a block (`0x88` / `0x208`) and indexes
it by slot … a slot's length is **stored**, not computed. `slotCount` is not read; the slot index comes from the
script (`voiceread`'s argument) and is bounded only by the table it indexes." (`PK:187-190`.)

| function | role as stated | read? | where |
|---|---|---|---|
| `0032F430` | "allocates the four per-manager directory tables at boot"; "gives each manager slot a `0x208` buffer and zeroes its first byte" | read in full (`PK:398`) | `PK:207-208`, `PK:385-386`; caller World `00266D10` (`PK:502`) |
| `0032FCA0` `ActorResource_BeginManagerResourceSetLoad` | "requests exactly `0x88` bytes of a manager's `.snd` and `.mot` and `0x208` of its `.vpc` and `.vpcjp` into four per-manager tables (`022C6E98`, `022C6E70`, `022C6EE8`, `022C6EC0`; `0032FE60`–`0032FFE2`)"; "writes a zero into byte 0 when it does not request a package (`0032FEC7`, `0032FF2D`, `0032FF98`, `00330004`)" | read in full (`PK:398`) | `PK:165`, `PK:206`, `PK:381-386`, `PK:394-395`; callers: ActorEntity layer (`PK:494`), WorldAreaField (`PK:503`) — the calling function is **not named** |
| table → field map | `022C6E70` "record field +1, `0x88`, completion `003302B0`"; `022C6E98` "field +2, `0x88`, completion `00331760`"; `022C6EE8` "field +3 of namespace 8, `0x208`, completion `00331820`"; `022C6EC0` "field +3 of namespace 37, `0x208`, completion `003317C0`" | — | `PK:382-385` |
| `0032F260` / `0032F290` | "field +1 offset and size" | read in full | `PK:388`; caller Presentation `003DD4C0` for `0032F260` (`PK:499`) |
| `0032F2C0` / `0032F2F0` / `0032F3A0` | "field +2 offset, size, and slot `k+8`'s size at `+0x4C`" | read in full | `PK:388-389` |
| `0032F320` / `0032F360` | "`0032F320` returns slot `k`'s **offset** (`[table + 8k + 8]`) and `0032F360` its **size** (`[table + 8k + 0xC]`)"; "the two 64-slot tables, selected by `r8d`" | read in full | `PK:165`, `PK:389-390` |
| reader guard | "every one of them reads slot `k` at `+8 + 8k` / `+0xC + 8k` after one test only: `cmp byte ptr [buf], 0` and return -1 if zero" | — | `PK:390-391` |
| completions | "the two completions clear a pending bit in the manager's state word (`022C6E48`, bits 14 and 15) and never touch the buffer" | read in full | `PK:392-393` |
| `0032ED80` `ActorResource_ResetManagerLoadState` | "(clears them)" | **not stated** | `PK:208-209`; caller ActorEntity (`PK:494`) |

Field table (`PK:161-165`): `+0x00` magic — "Inert … **yes**"; `+0x04` slotCount — "not read by any function
read here"; `+0x08` pairs — read as above, "Rejected if: not bounded (`k` comes from the script)", "Inert: the pair
`{0, 0}` — a zero size loads nothing (`003EA011`–`003EA013`)". Closure of the magic question: "Nothing compares
`+0x00` or `+0x04` against any value … a loaded directory is recognised by that byte being non-zero, which is the
`P`. Corrupting the magic to any non-zero first byte changes nothing; zeroing byte 0 makes every slot read of
that package return -1." (`PK:391-397`.)

### 1.4 Sub-file request

- **Voice loader `003E9EF0`**: "issues `0032E620(kind, packId, dest, size)` with that offset as the request's file
  offset" (`PK:165`); "`003E9EF0` (the sub-file request)" (`PK:207`). The voice chain is on
  `18-Audio/the-voice-pack-slots-and-the-voice-verbs.md` §2.5 (`PK:191`; outside the audited set).
- **`0032E620`** — the generic resource request. Example caller shape from a crossing: "`0032E620(7, 0x98 + n,
  buffer, result, &record)`, where the stack record carries the callback `00291C60`" (`PK:173-174`); "51 raw call
  sites" (`PK:167`). It is called by Resource `0032EB40`, `00384420` (`PK:500`), Script VM `0050DFE0`
  (`PK:501`), World `00378540` (`PK:502`), WorldAreaField `MapRef_BeginLoadResources` (`00268750`), `00378030`,
  `AreaArd_LoadOrUnloadFieldResource` (`003EA820`) (`PK:503`), Presentation `003B53C0`, `003B2310` (`PK:499`),
  Save/Load `FUN_002ef300` (`PK:496`). Its body is **not described** on either page.
- Which `kind` value(s) a PKFL sub-file request uses: **not stated**.

### 1.5 State and lifetime

| state | what the page says | lifetime | where |
|---|---|---|---|
| `g_pathTables` (`0x0215F000` + 8·ns, per the three slot addresses) | `[5]`, `[8]`, `[37]` hold the record arrays; "written only by `ResourcePath_Init` and read by nobody by name" | written at start-up (`PK:490`); never freed: **not stated** | `PK:156-159`, `PK:201-203` |
| four per-manager directory tables `022C6E70`, `022C6E98`, `022C6EE8`, `022C6EC0` | one `0x208` buffer per manager slot, byte 0 zeroed at allocation; loaded with `0x88` or `0x208` bytes | allocated "at boot" by `0032F430` (`PK:207`); cleared by `0032ED80` (`PK:208-209`); number of managers, buffer stride, and when the reset runs: **not stated** | `PK:165`, `PK:382-386` |
| byte 0 of a table buffer | "load-bearing": non-zero = loaded (the `P`); zero = not requested / not loaded → readers return -1 | written by `0032F430` (zero) and `0032FCA0` (zero when not requesting; the loaded `P` otherwise) | `PK:386`, `PK:393-397` |
| manager state word `022C6E48` | "bits 14 and 15" are pending bits cleared by completions | which code sets them, and the meaning of the other bits: **not stated** | `PK:392-393` |
| manager record array `02098E10` | "the **`0x288` stride** - the same records the manager indexer walks" (from the ActorEntity crossing) | **not stated** | `PK:494` |

### 1.6 Order

- Start-up: `ResourcePath_Init` "is called from the 978-byte core start-up root" (`PK:490`); `0032F430` allocates
  the tables "at boot" (`PK:207`). Their relative order: **not stated**.
- Per manager resource-set load: `0032FCA0` requests the directories (`PK:165`, `PK:206`); completions clear
  pending bits 14/15 (`PK:392-393`); readers then index the loaded buffer (`PK:387-391`); the voice loader issues
  the sub-file request (`PK:165`). What triggers `0032FCA0` (map load? actor spawn?) and in which frame phase:
  **not stated** (the crossings name only layers, `PK:494`, `PK:503`).
- Slot index source: "the slot index comes from the script (`voiceread`'s argument)" (`PK:189-190`); for the
  `.mot` / `.snd` readers the index source is **not stated**.
- Reset: `0032ED80` "(clears them)" (`PK:208-209`); when: **not stated**.

### 1.7 Dependencies

| on | for | where |
|---|---|---|
| `02-Resource-And-Asset-Pipeline` (`area-nmb-index.md` §3; VBF archive page) | `ResourcePath_Get`, the path-table element format, archive lookup, the `kind 7, id 0x98` example | `PK:110-114`, `PK:177-178`, `PK:479-480` |
| `18-Audio` | voice chain (`voiceread`, `003E9EF0`), `.snd` / `.vpc` payloads; `.sab` as the "magic *is* checked" contrast | `PK:105`, `PK:191`, `PK:399-400`, `PK:481-482`, `RM:171` |
| `17-Presentation-Rendering` | `.mot` payload meaning | `RM:171`, `PK:400` |
| `25-EBP-Script-Container` | the indexed-directory idiom; `.ebp` is field 0 of every namespace record | `RM:177`, `PK:91-93`, `PK:120-122`, `PK:483-484` |
| `04-Actor-Entity` / ActorEntity layer | the manager records (`02098E10`, `0x288` stride) and the `ActorResource_*` load functions | `PK:494`, `PK:206-209` |
| `00-Engine-Core-Runtime` (CoreRuntimeScheduling) | start-up root calling `ResourcePath_Init` | `PK:490` |
| `01-Script-VM` | script argument supplies the slot index (`voiceread`); `0050DFE0` calls `0032E620` | `PK:189-190`, `PK:501` |
| `03-World-Area-Field`, `16-UI`, `19-Save-Load-Settings` | callers only (CLIENT crossings) | `PK:496-503` |

## 2. Gaps

### 2.1 Gaps the pages state themselves (still open, or never closed)

| # | gap | where |
|---|---|---|
| S-1 | **Slot meaning.** "**Nothing is claimed about what any slot holds.**" Payload meaning is delegated to `17-…` and `18-Audio`; "no reading of 'even = data, odd = descriptor' is asserted" (that last clause is itself stale, see X-6). | `PK:399-402`, `RM:132`, `RM:170-172` |
| S-2 | **No slot denominator.** "**So the 14-pair denominator is NOT established, and no sheet should be scored against it yet.**" Steps 2-3 of the plan (`check_pkfl.py`, one sheet per unit) have no stated outcome; `Slots/` and `Variants/` do not exist in the snapshot. | `RM:86-90`, `RM:150-158`, `RM:160-166` |
| S-3 | **Write path.** "None found. Nothing in the executable emits `PKFL`." A port's tooling would have to infer a writer from the layout. | `PK:193` |
| S-4 | **Code half of the audit.** "**The corpus half of this sheet is now independently confirmed; the code half is not.**" The 2026-09-18 body reads (`PK:381-398`) are author reads, not an audit pass; front matter still `last_pass_state: … §3 loader contract NOT audited`. | `PK:360-363`, `PK:28` |
| S-5 | **`ResourcePath_Init` is half-read.** "◐ the slot-install region". | `PK:200` |
| S-6 | **Crossings are tier 2.** "tier 2: ledger names, sizes and `edges.tsv`; no body read for this note"; ActorEntity: "**4 of the 15 bodies on that layer are read, the rest are counted**". | `PK:488`, `PK:494` |
| S-7 | **`evt_t0005.mot` source.** "`evt_t0005.ebp` does load and play motion … while its own `.mot` is empty, so what it plays is served from another package" — which package is not stated. | `PK:410-411` |
| S-8 | **Ordering under the pair reading.** "'Offsets are not ascending in slot order' was not re-measured and is not asserted." | `PK:250-251` |

### 2.2 Structural gaps (a port needs these and no page in the folder states them)

| # | missing | why a port needs it | evidence of the gap |
|---|---|---|---|
| G-1 | **Byte order of the header and directory words.** | Reading `{offset, size}` at all. | Only implicit: `PK:272` dump, `PK:338` "LE dword"; `PK:72-86` give `u32` with no endianness. |
| G-2 | **Payload alignment / padding rule under the pair reading.** The `0x10`-alignment invariant (`PK:220`, `PK:327`) was measured over the four-byte reading and is in neither the "artefact" list nor the "survives" list (`PK:236-237`, `PK:249-251`); "padded to the sector" (`PK:407`) gives no sector size; "the first payload usually sits at `0x800`" (`PK:260`) says "usually". | A writer, and any validator. | `PK:220`, `PK:249-251`, `PK:260`, `PK:407` |
| G-3 | **Whether `size` is the stored (compressed) or the decoded length**, and whether a slot payload is itself compressed. Only the outer VBF block compression is mentioned ("decompressing only block 0 of each", `PK:238`, `PK:313`). | The sub-file request passes `size` straight through (`PK:165`). | not stated |
| G-4 | **Path-table element format and index formula.** `ResourcePath_Get` "returns `g_pathTables[namespace][index]`, 22 bytes" (`PK:113`) — whether "22 bytes" is the function size or the element; the element type (string pointer?) and the map → index formula (`index = 3·map + field`? from "`i%3 == 0,1,2`", `PK:120`) are not written out. Delegated to `area-nmb-index.md` §3 (outside). | Building `(ns, index)` for a map. | `PK:113`, `PK:118-122` |
| G-5 | **Region-variant selection.** Ten arrays for ns 5 and ns 8, two for ns 37 (`PK:120-122`, `PK:301`); which array the engine uses, and what selects it, is not stated. | Picking the path. | `PK:138-142`, `PK:300-301` |
| G-6 | **Language (namespace 8 vs 37) selection mechanism.** "the engine selects the namespace" (`PK:126`). | Loading `.vpc` vs `.vpcjp`. | `PK:65-68`, `PK:124-126` |
| G-7 | **Path → shipped file resolution, and the 9 vs 10 mismatch.** Files ship under nine locale roots (`PK:404-405`) while paths come in ten region variants (`PK:120-121`); 1,809 `.vpc` files against 3,290 `.vpc` strings (`PK:133`), 2,304 `.snd` files against 3,290 strings (`PK:132`). How a path string maps to an archive entry, and why the file counts are what they are, is not stated (the `.fpk` "path with no file" case is explained, `PK:150-154`; the PKFL cases are not). | Every load. | `PK:43-48`, `PK:130-136`, `PK:404-405` |
| G-8 | **When the walker "does not request a package".** "the walker writes a zero into byte 0 when it does not request a package (`0032FEC7`, `0032FF2D`, `0032FF98`, `00330004`)" — the condition is not given (missing path? field absent in ns 5 records, which have no `snd`/`vpc`?). | Reproducing which tables are live per manager. | `PK:394-395` |
| G-9 | **Which records `0032FCA0` reads for fields +1 / +2.** Fields +3 are tied to "namespace 8" and "namespace 37" (`PK:384-385`); fields +1 (`mot`) and +2 (`snd`) are not tied to a namespace, and ns 5 records have `fpk`, not `snd`, at +2 (`PK:120`). | Map vs. non-map managers. | `PK:382-385` |
| G-10 | **Manager count, per-manager buffer stride, and the readers' argument list.** "gives each manager slot a `0x208` buffer" (`PK:386`); how a reader selects the manager, what `r8d` values pick which 64-slot table (`PK:390`), and the full argument list of the seven readers are not stated. | Calling the readers. | `PK:386-391` |
| G-11 | **Out-of-range `k`.** `k` is "not bounded" (`PK:165`), `slotCount` is not read (`PK:189`), and a 16-slot package is loaded as `0x88` bytes into a `0x208` buffer (`PK:165`, `PK:386`). What a read at `k ≥ 16` of a 16-slot table returns (stale bytes of an earlier load?) is not stated. | Faithful edge behaviour. | `PK:165`, `PK:189-190`, `PK:386` |
| G-12 | **Caller handling of `-1`.** Readers "return -1 if zero" (`PK:391`); what `003E9EF0` and the `.mot`/`.snd` consumers do with `-1` is not stated (only "a zero size loads nothing", `PK:165`). | Error path. | `PK:165`, `PK:391` |
| G-13 | **Manager state word `022C6E48`.** Who sets bits 14/15, which completion clears which bit, and the other bits. | Load sequencing. | `PK:392-393` |
| G-14 | **Trigger and frame position of `0032FCA0`, `0032ED80`, `0032F430`.** Only layers are named (`PK:494`, `PK:502-503`); the calling functions and when they run are not. | Order (§1.6). | `PK:206-209`, `PK:494`, `PK:502-503` |
| G-15 | **`0032E620` contract.** Argument list (four vs five arguments, X-12), `kind` values for PKFL requests, the callback record, completion semantics. Only called-by lists are given. | The sub-file request itself. | `PK:165`, `PK:167-179`, `PK:494-504` |
| G-16 | **`0024AB90` and `00249810`** appear only in the `00291C80` crossing ("queries `0024AB90(7, 0x98 + n)`", "allocates `00249810(2, result)`", `PK:171-172`) and as "the allocation arm `00249810` … this page's container init describes" (`PK:498`); no page section describes a "container init". | If the PKFL loads use the same query/allocate shape (not stated). | `PK:171-172`, `PK:498`, `PK:500` |
| G-17 | **`PKFL_Bind`.** Named once — "`PKFL_Bind` and the slot-consumer functions were not read" (`PK:360`) — and nowhere else in the database snapshot (searched all of `FFXII TZA/`). No address, no role. | Unknown whether it is one of the named functions under another name. | `PK:360` |
| G-18 | **`.mot` occupancy by slot under the pair reading**, and a per-extension present-pair total. The only total, "74,340 present offsets" (`PK:213`, `PK:326`), is listed as an artefact (`PK:237`); no replacement is given. | Corpus validation of a port. | `PK:213`, `PK:237`, `PK:244-246` |

### 2.3 Fields or figures given without meaning

| # | item | where |
|---|---|---|
| U-1 | `+0x04 slotCount` — written in every file (16 / 64) and "not read by any function read here"; whether any engine path reads it is bounded only by the six/seven readers' sweep (`PK:387-391`). A writer must still emit it. | `PK:74`, `PK:164`, `PK:189` |
| U-2 | `0032F3A0` reads "slot `k+8`'s size at `+0x4C`" for field +2 (`.snd`) — why a `.snd` consumer needs slot `k+8`'s size is not stated (cf. `.snd` "slot 9 in 1,809", `PK:245`). | `PK:389` |
| U-3 | The figure **321** in "709, 329, 321 and the ten/two array counts are unaffected" — 321 appears nowhere else on either page. | `PK:469` |
| U-4 | `.fpk` field of ns 5 and ns 21 (215 area stems × 2) — named for the string reconciliation only; ns 21 is not otherwise described. | `PK:144-149` |
| U-5 | The `0x288`-stride manager records at `02098E10` — named in a crossing; their relation to the per-manager directory tables is not stated. | `PK:494` |

