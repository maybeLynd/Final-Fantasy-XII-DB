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

