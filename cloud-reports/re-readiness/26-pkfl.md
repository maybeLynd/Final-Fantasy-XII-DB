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

## 3. Contradictions (statements a re-implementer would have to choose between)

Rules used here. Both sides are quoted exactly as the snapshot has them, with `path:line`. **Value-changing**
items (§3.1) change a count, offset, size, constant, signature or behaviour a port would implement or validate
against; every one is **page-text only - needs local check**, because this session cannot see the executable
or the archive. A favoured side is named only where a dated correction on the pages settles it; otherwise
"no favoured side". §3.2 holds stale "open / not read" claims, corrected claims still repeated unstruck,
banner / front-matter disagreements and attribution conflicts that do not change a value. §3.3 lists what was
cross-checked and found consistent, so the reader can see what was tested.

The root of most items: the **2026-09-11 correction** (`PK:426-437`) changed the directory entry from four
bytes to `{u32 offset, u32 size}`. It was applied by striking (`PK:77-79`, `RM:48`), by banners
(`RM:39-46`, `PK:232-251`) and by in-place notes (`PK:81-84`, `PK:165`, `PK:187-191`) — but several
sections that rest on the four-byte reading carry **no** strike and **no** banner: `PK:43-49` (the lead
table), `PK:95-98` (§2, *after* the correction), `PK:213-230` (§5 invariants and occupancy, which sit
*above* the banner at `PK:232` that only covers "the survey below"), `PK:291-308` (§6), `PK:310-363` (§6b),
`PK:399-402` (§7), and `RM:96-118` (two README sections after the banner'd one).

### 3.1 Value-changing — page-text only - needs local check

#### X-1. Where the directory ends (`0x48` vs `0x88`)

- `PK:81-84`: "**Corrected 2026-09-11 (§8): the directory is `slotCount` pairs of `{u32 offset, u32 size}`**, eight bytes per slot, `{0, 0}` meaning the slot is absent; it ends at `8 + 8 × slotCount` — **`0x88`** for a 16-slot package, **`0x208`** for a 64-slot one"
- `PK:242`: "`{offset, size}` pairs with `8 + 8n ≤ offset` and `offset + size ≤ file` | **10,314 / 10,314 packages**"
- vs `PK:260-261`: "And in **2,268 files the smallest present offset is `0x40`, which is *before* the 16-slot directory ends at `0x48`.**"
- vs `PK:269-270`: "In a 16-slot package the directory runs `+0x08 .. +0x48`, so slot 14's offset word lives at `+0x40` and slot 15's at `+0x44`."
- vs `PK:333` (§6b, no banner): "smallest offset `0x40`, 16-slot files | 2,268 | **2,268**"
- vs `RM:92-94`: "**the first payload is not at the directory end** — in 2,268 files the smallest offset is `0x40`, *before* the 16-slot directory ends at `0x48`."

**Favoured: `0x88` / `0x208`, settled by the dated correction `PK:426-433` (2026-09-11).** Under it, no
offset can be below the directory end (`PK:242`), so "smallest offset `0x40`" cannot be an offset. `PK:261`
sits under the `PK:232` banner but is not struck; `PK:333` and `RM:92-94` are under no strike.

#### X-2. Gap between the directory and the first payload (1,976 / 1,784 bytes)

- `PK:259-260`: "**2. The first payload is never at the directory end.** The gap is 1,976 bytes in 4,356 files and 1,784 in 3,573 — the first payload usually sits at `0x800`."
- `PK:332` (§6b, no banner): "gap to first payload | 1,976 in 4,356; 1,784 in 3,573 | **identical**"
- vs `PK:82-83` (directory ends at `0x88` / `0x208`) and `PK:249-250`: "What survives: … the first payload at `0x800` (now the first *pair's* offset)".

Arithmetic (this report's, not a page's): 1,976 = `0x800 − 0x48` and 1,784 = `0x800 − 0x108`, i.e. the gaps were
measured from the **withdrawn** directory ends; from `0x88` / `0x208` the same `0x800` payload would sit 1,912 /
1,528 bytes past the directory. **Favoured: the 2026-09-11 directory end (`PK:426-433`); the gap figures are
not restated under it** — a writer padding header + directory to `0x800` needs the restated rule (G-2).

#### X-3. Which slot indices are ever used (0–27 dense vs 0–15 / 0–13)

- `PK:49` (lead "Corpus validation" table, no banner): "occupied slot indices | **0–27**, densely — no index in that range is ever unused"
- `PK:224-230` (above the `PK:232` banner): "**Occupancy is dense and perfectly paired:**" … "16/17     54  18/19     54  20/21     36  22..27    18"
- `RM:98-99` (no banner): "**36 of the 64 declared slots are never used in any of the 3,618 64-slot files.** Nothing above index 27 is ever occupied."
- vs `PK:244`: "slots used | `.mot` and `.snd` indices 0–15; `.vpc` and `.vpcjp` indices **0–13** of 64"
- vs `PK:415-416`: "all 10,314 packages … populate no slot from 16 to 27: the 16-slot families reach slot 15 at most and the 64-slot families slot 13."
- vs `PK:419-420`: "Over all 3,618 64-slot packages (`.vpc` and `.vpcjp`) the highest populated slot is 13; no package uses any index above 13, so none above 27."

**Favoured: 0–15 (16-slot) and 0–13 (64-slot), settled by the dated closures `PK:412-416` and `PK:417-422`
(2026-09-18, FABLE).** The README's "36 of the 64" becomes 50 of 64 under that ceiling (this report's
arithmetic, 64 − 14; no page states 50).

#### X-4. The frozen census `.tsv` the sheet "agrees" with

- `PK:51-54`: "The occupancy in this sheet was parsed here from the archive and then compared against the frozen `pkfl-container-census.tsv`: **10,314 common paths, 10,314 agree, 0 differ.**"
- `PK:222`: "occupancy agrees with the independent frozen census | **10,314 / 10,314, zero differences**"
- vs `PK:234-237`: "Every figure in this section was measured with a 4-byte directory entry. … everything built on them (the even/odd pairing, the aliasing at `0x40`, the shared offsets, the 74,340 "present offsets", the 0 B medians) is an artefact of that reading."

A port that validates against `pkfl-container-census.tsv` would validate against the four-byte slot numbering.
Outside the audited set, the census script in this snapshot reads four-byte words
(`tools/analysis-kit/gfz-scripts/census_pkfl_container.py:46-52`). **No favoured side on the pages** — the
correction does not mention the `.tsv`, and the `.tsv` is not in the snapshot.

#### X-5. What the repeated `0x40` value is: an in-directory alias, or a size

- `RM:73-75`: "In `alc_a0100.snd`, slots 1, 5, 7, 9, 11, 13 and 15 all carry offset `0x40` — which is slot 14's *own directory entry*. The bytes there are the pair of directory words read as data. It is a canonical **"this half is empty"** marker, cheaper than a null."
- `PK:298` (§6, no banner): "the shared value `0x40` is independently explained: it is the byte offset of slot 14's own directory entry in a 16-slot package, and the bytes there are the slot-14/15 offset words."
- `PK:305-308` (§6, no banner): "That predicts distinct offsets for the two halves. **It fails in 2,349 files**, where the odd halves alias one location — so the pairing is a directory-level invariant and not a content-level one."
- `PK:330-331`, `PK:334-335` (§6b, no banner): "files with ≥2 slots aliasing | 2,349 | **2,349**"; "`alc_a0100.snd` slots at `0x40` | 1, 5, 7, 9, 11, 13, 15 | **identical**"
- vs `PK:245`: "the "offset `0x40`" of the old reading was **14,337 sizes of `0x40` bytes**"
- vs `PK:431-432`: "`nal_a0100.snd`'s directory reads `{0x800, 0x2300}, {0x3000, 0x40}, {0x3800, 0x40} …` — the `0x40`s are sizes."

**Favoured: sizes, settled by `PK:426-433` (2026-09-11).** `RM:73-75` is under the `RM:39` "Withdrawn
2026-09-11" banner ("the aliasing story below", `RM:43`) but is itself framed as a correction (`RM:62`
"Corrected 2026-09-04"), so the README carries two stacked "corrections" of which the inner one is wrong.

#### X-6. Whether the second word of a pair is a "descriptor"

- `PK:401-402` (§7, unstruck): "The even/odd pairing is described structurally and **no reading of "even = data, odd = descriptor" is asserted**, though the aliasing evidence is consistent with it."
- vs `PK:81`, `PK:86`: "`{u32 offset, u32 size}`"; `PK:165`: "`0032F360` its **size** (`[table + 8k + 0xC]`)".

**Favoured: the second word is the slot's size, settled by `PK:426-433` (2026-09-11).** The §7 bullet
outlived the correction (as `PK:371` says another §7 bullet did).

#### X-7. How a slot's length is obtained

- `PK:97-98` (§2, *after* the correction, unstruck): "a slot's length is **not** reliably the distance to the next slot's offset, because slots may share one."
- `PK:256-257`: "Anything that computes a slot's length by walking slot indices in order is wrong in more than half the corpus; lengths must be derived after sorting by offset."
- `RM:77-79`: "**Computing a slot's length as the distance to the next present offset gives an aliased slot a length of 0.**"
- vs `PK:189`: "a slot's length is **stored**, not computed."; `PK:165` (`0032F360` returns the size).

**Favoured: stored, settled by `PK:187-191` / `PK:426-433` (2026-09-11).**

#### X-8. Whether offsets ascend in slot order

- `PK:96` (§2, after the correction): "offsets are **not** ascending in slot order"
- `PK:255`: "**1. Offsets are not ascending in slot order — only 4,833 of 10,314.**"; `PK:336` (§6b): "offsets ascending in slot order | 4,833 / 10,314 | **4,833**"; `PK:357-358` "**no reading makes the directory ordered**"
- `RM:92-93`: "**offsets are not ascending in slot order** (unlike EBP)"
- vs `PK:250-251`: ""Offsets are not ascending in slot order" was not re-measured and is not asserted."

**Favoured: "not asserted", settled by the 2026-09-11 banner `PK:232-251`** — so the database currently
states **nothing** about order under the pair reading (S-8). A writer cannot learn from the pages whether to
emit payloads in slot order.

#### X-9. Is any header byte read: "never validated / inert" vs "byte 0 is load-bearing"

- `PK:102`: "**The magic is never validated.**"
- `PK:107-108`: "Corrupting the first four bytes of a package is expected to change nothing — see §6 for the limit on that expectation."
- `PK:163`: "`+0x00` magic | — | — | — | **yes — `PKFL` occurs 0 times in the whole image, so no memory-operand comparison is possible either**" (columns: Read by, Rejected if, Clamped to, Inert)
- vs `PK:391`: "after one test only: `cmp byte ptr [buf], 0` and return -1 if zero."
- vs `PK:393-397`: "So the magic is never validated, but its first byte is load-bearing in one way … Corrupting the magic to any non-zero first byte changes nothing; zeroing byte 0 makes every slot read of that package return -1."

**Favoured: byte 0 is read (non-zero = loaded), settled by `PK:381` (2026-09-18, FABLE).** The field table
`PK:163` still lists `+0x00` as read by nobody and inert, and `PK:107-108` still says all four bytes can be
corrupted with no effect.

#### X-10. How many slot readers there are, and what `0032F320` / `0032F360` cover

- `PK:387-390`: "finds exactly six slot readers, `0032F260` / `0032F290` (field +1 offset and size), `0032F2C0` / `0032F2F0` / `0032F3A0` (field +2 offset, size, and slot `k+8`'s size at `+0x4C`) and `0032F320` / `0032F360` (the two 64-slot tables, selected by `r8d`)" — the list names **seven** addresses.
- `PK:187-189`: "it loads the directory's bytes as a block (`0x88` / `0x208`) and indexes it by slot — `0032F320` for the offset, `0032F360` for the size"
- `RM:43-44`: "The engine loads `0x88` / `0x208` bytes as the directory and indexes pairs by slot (`0032F320` / `0032F360`)"
- `PK:206-207`: "`0032F320` / `0032F360` (offset / size of slot `k`)"

**Scope: favoured "64-slot tables only", settled by the later dated read `PK:381` (2026-09-18) over the
2026-09-11 text.** **Count (six vs seven): no favoured side.** `RM:43-44`, `PK:187-189` and `PK:206-207`
still present `0032F320` / `0032F360` as the only indexers; `PK:204-209` (§4, Key addresses) does not list
the five `.mot` / `.snd` readers at all.

#### X-11. How many directory-load completions there are

- `PK:382-385`: four tables, each with its own completion: "completion `003302B0`", "completion `00331760`", "completion `00331820`", "completion `003317C0`"
- vs `PK:392-393`: "the two completions clear a pending bit in the manager's state word (`022C6E48`, bits 14 and 15) and never touch the buffer"
- vs `PK:398`: "the walker, the allocator, the six readers and the two completions read in full."

**No favoured side.** Which completion clears which bit, and whether two of the four were read, is not stated (G-13).

#### X-12. Argument list of the resource request `0032E620`

- `PK:165`: "the voice loader `003E9EF0` issues `0032E620(kind, packId, dest, size)` with that offset as the request's file offset" (four arguments; the file offset is not among them)
- vs `PK:173-174`: "requests the file with `0032E620(7, 0x98 + n, buffer, result, &record)`, where the stack record carries the callback `00291C60`" (five arguments)

**No favoured side.** Where the PKFL slot's file offset travels (a fifth argument, the record, or elsewhere)
is not stated.

#### X-13. The "74,340 present offsets" and the `0x10` alignment invariant

- `PK:213`: "**Invariants — every one measured over all 10,314 packages and all 74,340 present offsets.**"
- `PK:219-220`: "every present offset lies inside the file | **10,314 / 10,314**"; "every present offset is **`0x10`-aligned** | **74,340 / 74,340**"
- `PK:326-328` (§6b): "present offsets | 74,340 | **74,340**"; "every offset `0x10`-aligned | 74,340 / 74,340 | **74,340, 0 unaligned**"
- vs `PK:236-237`: "everything built on them (… the 74,340 "present offsets", …) is an artefact of that reading."
- vs `PK:249-251` (the "What survives" list), which does **not** include the alignment invariant.

**Favoured for the 74,340 figure: artefact, settled by the 2026-09-11 banner.** **For `0x10` alignment: no
favoured side** — under the pair reading the 74,340 words are offsets *and* sizes, so the measurement says
both are `0x10`-multiples, but the pages neither restate nor withdraw it.

#### X-14. README counts built on the four-byte reading, in sections with no banner

- `RM:113-115`: "**2,952 files do not fill their pairs contiguously from 0.** … **So a pair index is a typed slot, not a sequence number** — which is what makes 14 a population rather than a maximum."
- `RM:117`: "Pairs per file range 0–14; 4,212 files carry exactly one pair, 2,331 carry eight"
- vs `PK:244`: "`.mot` and `.snd` indices 0–15; `.vpc` and `.vpcjp` indices **0–13** of 64"; `PK:245`: "`.snd` | every package fills slots 0–7; slot 9 in 1,809"

**Population: favoured 16 (`.mot`/`.snd`) and 14 (`.vpc`/`.vpcjp`), settled by `PK:412-422` (2026-09-18).
The per-file counts (2,952 / 4,212 / 2,331): no favoured side** — they were not re-measured under the pair
reading. (This report's arithmetic suggests the old 16-slot read reached only new slots 0–7 of a `.mot` /
`.snd`, so slots 8–15 of those files were invisible to it; no page says so.)

#### X-15. EBP's file population (out of this system, but stated in it)

- `RM:3`: "10,314 shipped files against EBP's 10,045"
- vs `RM:144-145`: "`census_ebp_container.py` derived occupancy from the container's own directory across 1,115 files"

**No favoured side.** Neither line says whether one figure is a subset (e.g. unique stems) of the other.

### 3.2 Stale "open / not read" claims, corrected claims repeated unstruck, and banner disagreements

| # | side A (stale or banner) | side B | settled by a dated line? |
|---|---|---|---|
| B-1 | `PK:4` "status: AUDITED — the layout, the walker and the corpus read; the four residues of section 7 closed 2026-09-18" | `PK:28` "§3 loader contract NOT audited"; `PK:362-363` "**The corpus half of this sheet is now independently confirmed; the code half is not.**"; `PK:374` "while auditing why this page still reads `PARTIAL`" (2026-09-14) | no — banner vs front matter |
| B-2 | `PK:19` "last_reviewed: 2026-09-04" | body dated 2026-09-11 (`PK:81`, `:426`), 2026-09-14 (`PK:167`, `:374`), 2026-09-18 (`PK:381`, `:403`, `:412`, `:418`, `:498`) | no — front matter |
| B-3 | `PK:26-27` "passes: 1", "last_pass: 2026-09-05"; `PK:30` "reopened_count: 0" | `PK:426-437` (2026-09-11) withdrew the directory layout: "§2, §3 and §5 carry the correction in place; the README's headline finding is withdrawn there" (`PK:433-435`) | no — front matter |
| B-4 | `PK:29` "crossref_clean: true" | X-1…X-14 above, all inside `PK`; the duplicated bullet B-18 | no — front matter |
| B-5 | `PK:18` "corpus_validated: "10,314 / 10,314 shipped packages, every header and directory re-parsed from FFXII_TZA.vbf 2026-09-04"" | `PK:234` "Every figure in this section was measured with a 4-byte directory entry."; re-parse under the pair reading `PK:237-238`, `PK:433` (2026-09-11) | yes — 2026-09-11 (the front matter still cites the 2026-09-04 parse) |
| B-6 | `PK:14` "verified: 9 cited function entries" | §3, §4 and §7 alone cite 22 distinct function addresses (`002DF980`, `002DF9A0`, `0032FCA0`, `0032F320`, `0032F360`, `003E9EF0`, `0032E620`, `0032F430`, `0032ED80`, `0032F260`, `0032F290`, `0032F2C0`, `0032F2F0`, `0032F3A0`, `003302B0`, `00331760`, `00331820`, `003317C0`, `00291C80`, `0024AB90`, `00249810`, `00291C60`; `PK:165-209`, `PK:381-398`) | no — provenance count predates the 2026-09-11 / 09-18 additions |
| B-7 | `PK:296` "**It is still weaker than a body read**, which is why §7 keeps it open." | `PK:381` "**Closed 2026-09-18 (FABLE) by a body read of every reader of the directory.**" | yes — 2026-09-18 |
| B-8 | `PK:360-362` "**Not audited here:** §3's loader contract. `PKFL_Bind` and the slot-consumer functions were not read, so the *"magic never validated"* row still rests on the whole-image scan the sheet itself flags as the weaker instrument in §7." | `PK:381-398` (2026-09-18 body reads) | yes — 2026-09-18 (for the magic row; the *audit* gap S-4 remains) |
| B-9 | `PK:187` "The engine never walks the directory" | `PK:371-372` "The walker exists and is named there"; `PK:381` "The walker `0032FCA0`"; `PK:401`-adjacent §4 "Listed 2026-09-11" (`PK:205`) | wording only; both dated 2026-09-11 / 09-18 — no value differs |
| B-10 | `RM:82-84` "*"Every occupied slot has its even/odd partner"* is **true, 10,314 / 10,314** — but it is **partly an artefact of that aliasing**"; `PK:275-280` "This qualifies the category README's headline finding rather than contradicting it." | `RM:39-46` "⚠ Withdrawn 2026-09-11 — the pairing is the directory's entry width"; `PK:434-435` "the README's headline finding is withdrawn there" | yes — 2026-09-11 |
| B-11 | `RM:86-89` "**So the 14-pair denominator is NOT established** … until the container sheet's open questions are settled." | `PK:4` "the four residues of section 7 closed 2026-09-18"; `PK:412-422` (16 / 14 slot ceilings) — but no page then states a denominator (S-2) | partly — the open questions are closed 2026-09-18; the denominator is still unstated |
| B-12 | `RM:128-133` "**Not measured, and required before any sheet is written:** … the full slot census … whether the 16-slot and 64-slot forms are versions … the header beyond the count, and whether a magic/version field is validated" (under the heading "superseded", `RM:120`) | `RM:21` census 2026-09-04; `RM:34` "The 16/64 question is answered"; `PK:381-397` (2026-09-18) magic / header | yes — 2026-09-04 and 2026-09-18 (the slot-meaning item, `RM:132`, is still open: S-1) |
| B-13 | `RM:136-138` "PKFL indices 0–27 are all occupied, so **absence carries no information here**" (under "superseded") | `RM:96-109` "The directory IS sparse"; `PK:244` | yes — `RM:21` (2026-09-04) and `PK:412-422` (2026-09-18) |
| B-14 | `RM:157-158` "**Until step 1 lands, the unit count in this README is a sample estimate and must be quoted as one.**" | `RM:21-24` "CENSUSED — 10,314 of 10,314, 2026-09-04 … **Every shipped file parsed; zero failures.**" | yes — 2026-09-04 |
| B-15 | `RM:165-166` "`Slots/` \| one sheet per slot index, once the census fixes the population"; "`Variants/` \| the 16-slot versus 64-slot question, and any version field" | neither folder exists in the snapshot; `RM:34` "The 16/64 question is answered"; `PK:391` nothing compares `+0x04` | yes for `Variants/` — 2026-09-04 (`RM:21`, `RM:34`); `Slots/` remains planned (S-2) |
| B-16 | `PK:494` "reaches this page at `0032ED80`, `0032FCA0`, `0032E620`, `002DF980`"; `PK:496` "calls `0032E620` on this page"; `PK:499` "page-cited `0032E620`" | `PK:500` "page-cited `0032F430`, `ActorResource_BeginManagerResourceSetLoad` (0032FCA0), `0024AB90` call Resource bodies `0032E620`, `0032E400`, `0032E870`" | no — attribution of `0032E620` (this page's, or a Resource body) |
| B-17 | `PK:498` "a UI-side caller consults it for the (kind=2, out-result) marshalling this page's container init describes" | no section of `PK` describes a "container init"; `00249810` appears only in the `00291C80` crossing (`PK:172`) | no — dangling pointer (G-16) |
| B-18 | `PK:501` "**Script_VM_Native_Bridge — CLIENT (1 edge).** 1 inbound (Script_VM_Native_Bridge bodies `0050DFE0` call page-cited `0032E620`)…" | `PK:504` — the same bullet repeated verbatim | n/a — duplicate, not a disagreement |
| B-19 | `PK:124-126` "That is the whole explanation for the strict 1,809 / 1,809 pair: **one authored map list, two namespaces, and the engine selects the namespace.**"; `PK:68` "That is why the two counts are identical at 1,809 each." | `PK:133-134` ns 8 `.vpc` "329 x 10 … 3,290" vs ns 37 `.vpcjp` "329 x  2 … 658": the namespaces differ in variant multiplier, so the namespaces alone do not give equal file counts; the files ship per locale root (nine, `PK:404-405`) — see G-7 | no — the explanation is incomplete, no value is in dispute |
| B-20 | `RM:50-60` the even/odd-median table ("8/9 · 10/11 · 12/13 \| … \| **0 B**") and `RM:48`'s struck headline | `RM:39-46` banner: "this section's headline, its medians and the aliasing story below all read sizes as offsets … Kept as history." | yes — 2026-09-11 (table is unstruck but under the banner) |

### 3.3 Checked and found consistent (not contradictions)

- **Table → record field → extension.** `PK:165` lists `.snd`, `.mot`, `.vpc`, `.vpcjp` → `022C6E98`,
  `022C6E70`, `022C6EE8`, `022C6EC0`; `PK:382-385` gives `022C6E70` = field +1 (`mot`), `022C6E98` = field +2
  (`snd`), `022C6EE8` = field +3 of ns 8 (`vpc`), `022C6EC0` = field +3 of ns 37 (`vpcjp`); the records are
  `{ebp, mot, snd, vpc|vpcjp}` (`PK:121-122`). Consistent.
- **Directory read widths.** `0x88` / `0x208` agree at `RM:43-44`, `PK:83`, `PK:165`, `PK:188`, `PK:372`,
  `PK:383-385`, `PK:429-430`; `8 + 8 × 16 = 0x88`, `8 + 8 × 64 = 0x208`.
- **Reader displacements.** `+8 + 8k` (offset) and `+0xC + 8k` (size) agree at `PK:165`, `PK:373`, `PK:390`,
  `PK:431`; `0032F3A0`'s "slot `k+8`'s size at `+0x4C`" (`PK:389`) equals `0xC + 8(k+8) = 0x4C + 8k`.
- **Path-table slots.** `+0x028`, `+0x040`, `+0x128` (`PK:120-122`) = 8 × 5, 8 × 8, 8 × 37, matching
  `0x0215F028` / `0x0215F040` / `0x0215F128` (`PK:157`, `PK:201-203`).
- **String arithmetic.** `PK:131-135`: 7,090 + 3,290 = 10,380; 3,290 + 658 = 3,948; 709 × 10 + 215 × 2 = 7,520
  with 709 + 215 = 924 (`PK:147-148`); 1,038 = 709 + 329 (`PK:142`).
- **The 8-vs-10 region-variant report** (`PK:300` "`repos-1e`'s initialiser extraction found 8 arrays for
  namespace 8, not 10") is resolved on the same row: "an extraction returning 8 arrays for namespace 8 is
  incomplete rather than contradictory" (2026-09-04).
- **The withdrawn "different bounds" control** (`PK:439-473`) changes no figure: "**No figure changes.** 709,
  329, 321 and the ten/two array counts are unaffected" (`PK:469-470`).
- **The four-byte occupancy for slots 16–27 vs the pair occupancy for 64-slot slots 8–13.** Old pairs 16/17,
  18/19, 20/21, 22–27 = 54, 54, 36, 18 (`PK:229`, `RM:57-60`); new `.vpc` + `.vpcjp` slots 8–13 = 27 + 27, 27 +
  27, 18 + 18, 9 + 9 (`PK:246`). Equal, as `PK:413-414` says ("The 18–54 counts were the size words of slots 8–13").
- **Pairing invariant ↔ no lone zero.** "every occupied slot has its even/odd partner occupied | 10,314 /
  10,314" (`PK:221`) and "pairs with exactly one of offset / size zero | **0**" (`PK:243`) are the same fact
  under the two readings (the interpretation of it is stale: B-10).
- **The 27 empty packages** agree everywhere: `RM:117-118`, `PK:247`, `PK:288-289`, `PK:337` (all 2,048 B,
  9 locale copies each), `PK:403-407`.
- **Population and sizes.** `RM:6-11` = `PK:45-48`; 4,392 + 2,304 = 6,696 and 1,809 + 1,809 = 3,618
  (`RM:31-32`); 2,552 + 146 + 1,240 + 1,298 = 5,236 MB ≈ "5.2 GB" (`PK:36`).
- **Struck text is handled correctly** at `PK:77-79`, `PK:181-185`, `PK:205`, `PK:367-370`, `PK:378-380`,
  `PK:403`, `PK:412`, `PK:417-418`, `RM:48` — each struck claim is followed by its dated replacement.

