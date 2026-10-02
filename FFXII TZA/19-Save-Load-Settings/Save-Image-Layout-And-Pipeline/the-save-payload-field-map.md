---
system: The save-image payload — a field map from every reached accessor (AB-5's stated blocker, run)
category: 19-Save-Load-Settings
status: AUDITED
owner_layer: PrimaryOwner:Save_Load_Settings — the regions belong to the pages that read their writers
evidence_tier: 1
level: L1
readiness: BEHAVIORALLY UNDERSTOOD
confidence: PROVEN
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: a typed field scan over every function in functions.tsv, seeded by the payload base getter
    002EF2B0, the three buffer getters (002EF640 / 002EF620 / 002EF630, at -0x200) and the three global
    pointers into the image (020927C0 at +0x8000, 02092758 at -0x200, 02EBF190 at +0x4E48C), propagated through call
    arguments and record-returning callees for three hops; control WorldTransition_GetActiveOrPendingFieldId's
    read of +0x1044 (found); every access row is published beside this page
last_reviewed: 2026-09-10
audit:
  passes: 1
  last_pass: 2026-09-12
  last_pass_state: opus-the-save-payload-field-map-pass-1
  last_pass_kind: authored
  crossref_clean: false        # 2026-09-30 (SWE2-DATA): false until the pass-22 UNACCOUNTED NEIGHBOUR findings are accounted (FRONTIER-REQ-SWE2-DATA-PASS22-DEBT; OPUS-REQ-DATA-PASS30-CROSSREF-CLEAN-0930)
  reopened_count: 0
---

# The save-image payload — a field map from every reached accessor

> ### ⚠ Every offset on this page is a PAYLOAD offset. The instructions are not.
>
> The buffer getters (`002EF640` active, `002EF620` staging, `002EF630` submission) return the
> **buffer base, header included**, and the payload starts **`0x200`** further on. So an instruction's
> literal and this page's row differ by `0x200`, always, in that direction:
>
> **`buffer + X` is `payload + (X − 0x200)`.**
>
> **This has now misled three separate readings in one day** (2026-09-13) — the
> `+0x4E68C` / `+0x4E48C` pair below, and twice over what the `0xE240` recovery copy covers, where
> buffer `+0xE240` is payload `+0xE040`, **group persistent bank A**, and *not* payload `+0xE240`,
> SpawnKeep image A. Each time the wrong reading looked plausible because `0x200` is also a real
> field size in this map. **Subtract before comparing an instruction to a row.**


> [The save-image page](save-image-buffers-header-and-payload.md) mapped roughly 470 bytes of the 353,424-byte payload from the 70
> direct callers of the base getter and recorded why it stopped: *a pointer-propagation-aware
> analysis is required*. This page is that analysis. It reaches ~~368 functions and~~
> ~~309 offsets~~ 350 functions and 301 offsets in the published `save-payload-accesses.tsv` *(corrected 2026-10-02, OPUS: counted in the TSV, 1,725 rows)*, places the SpawnKeep images, the group persistence banks, the transition
> snapshot, the inventory descriptors and — answering `AB-5` — **the achievement block, which is
> inside the image at `+0x8000`**.

## 1. What the player sees

A save slot. Everything the slot restores — where you are and where you came from, the story
flags, the monsters a zone remembers, the achievement counters, the inventory's runtime
descriptors — is the payload this page maps, and the header the slot list shows is the 512 bytes
before it.

## 2. Native mechanism

### 2.1 How the accessors were found

Seven seeds: the payload base getter `SaveImage_GetPersistentPayloadBase` (`002EF2B0`), the three
buffer getters (`002EF640` active, `002EF620` staging, `002EF630` write submission — offset `−0x200`
so their accesses land in payload coordinates), and three global pointers the engine keeps into the
image: **`020927C0`**, which `00253970` sets to `SaveImage_GetActiveRuntimeBuffer() + 0x8200`
(`00253985`–`00253990`) — payload `+0x8000`; **`02092758`**, set to the buffer itself
(`00253979`–`0025397E`); and **`02EBF190`**, the battle-state block, which
`SaveRuntime_RebindImageBackedGameplayState` (`00238A80`, `00238A89`–`00238A92`) and `00233C10`
(`00233C2A`–`00233C33`) set to the buffer `+0x4E68C` — payload `+0x4E48C`.
> **Re-verified 2026-09-13 (`ASTRA-REQ-OPUS-LOAD-CLOSE`), and it is the third reading this convention
> has caught out.** `00233C10`'s null path is `call 0x2EF640` then `add rax, 0x4E68C` then a store
> into `[rip+0x2C8B570]`, which resolves to `02EBF190` — so the version-stamp page's *allocation*
> and this map's *rebind* are **the same instruction pair seen in the two coordinate systems**, not a
> contradiction between two pages. See the banner at the top.
>
> **And one asymmetry worth recording while the body was open:** on that null/bind path `00237DF0`
> runs **twice** — `00233C3F call 0x237DF0`, then `00233C48 jmp 0x237DF0` after the epilogue —
> while the already-bound and magic-mismatch paths tail-jump to it **once** (`00233C55`/`00233C59`).
> Recorded as observed; whether the double invocation is a two-phase design or a duplicated call is
> **not established**.

From each, the scanner tracks the register through `mov` / `lea` / `add`,
reports every `[reg + disp]`, propagates the pointer into callees through argument registers and
back to callers through `rax`; three hops.

| | count |
|---|---|
| payload access rows | ~~1829 (976 at a seed, 853 through propagation)~~ 1,725 in the published TSV *(corrected 2026-10-02, OPUS: counted in `save-payload-accesses.tsv`; the reserved-span check below cites the same 1,725)* |
| payload functions / offsets | ~~368 / 309~~ 350 / 301 *(corrected 2026-10-02, OPUS: distinct functions and displacements in `save-payload-accesses.tsv`)* |
| header access rows / functions / offsets | ~~204 / 26 / 40~~ 199 / 25 / 40 *(corrected 2026-10-02, OPUS: counted in `save-header-accesses.tsv`)* |
| control | `WorldTransition_GetActiveOrPendingFieldId` (`003148F0`) reads `+0x1044` — found |

**What the enumeration cannot see:** indexed entries (an access to `entry[i]` is reported at the
table's base, so a 0x180-entry table shows one entry), pointers stored into objects the scan has no
seed for, and anything below the third hop. The large untouched ranges in §2.4 are stated with
that limit.

> **What a census like this cannot see (2026-09-11, OPUS-NOTICE-CENSUSWRITES).** Seeds: the payload base getter and the buffer getters; a writer that reaches the buffer through a copy of its address kept elsewhere is outside unless propagation happens to carry it.
> A second limit is on the store side (AL-8): a block store marks one displacement while covering
> sixteen offsets, so *no store row at `+0xNN`* never proves *never written*. **20 of this census's
> 66 no-write displacements sit inside a wider store's range** — most of them in
> `WorldTransitionSnapshot_CaptureRuntimeState`'s 16-byte runs around `+0x4E48C..+0x4E508`
> (`work/STRUCT/blockwrite_overlap.tsv`).
> A scan seeded on *accessors* reaches *consumers*: a constructor that builds the record before
> any accessor can return it is reached only if it is seeded on its own. So the **reads** below are
> the well-covered side and the **writes** are under-covered wherever a constructor or an
> index-derived writer sits outside the seeds — do not rest an absence-of-writer claim on this
> TSV alone; pair it with a displacement scan of the candidate writers.

### 2.2 The payload, region by region

> **Coordinates.** Every offset on this page is **payload-relative**: payload = save buffer
> `+0x200`, so a staging-buffer address `buffer + X` appears here as `+(X − 0x200)`. The capture
> `00229B40` works on the buffer (`002EF620()` at `00229B4C`), which is why its `lea rcx, [rdi +
> 0xE240]` (`00229CDF`) is this page's `+0xE040`. Stated 2026-09-11 after OPUS-CONTRA-GROUPBANK
> read the same call in buffer coordinates.
>
> **CORRECTED 2026-09-11 (OPUS-CONTRA-GROUPBANK).** The two group persistent banks are **0x200
> bytes each, not 0x80**: `WorldPersistence_ExportGroupPersistentBank` (`0025D8E0`) copies
> `02099FF0` in a **four-iteration** loop of eight 16-byte moves (`0025D8E7` `mov edx, 4`,
> `0025D8F0`–`0025D941`), and the import (`00269A20`) mirrors it (`00269A27`, `00269A30`–`00269A81`).
> Bank A therefore spans `+0xE040`–`+0xE23F` and abuts SpawnKeep image A at `+0xE240`; bank B
> spans `+0x2E250`–`+0x2E44F` and abuts image B at `+0x2E450` — the image offsets were right, the
> bank sizes were the first loop iteration only. The derived 16-byte rows in §2.3 for `+0xE050`…
> `+0xE0B0` and `+0x2E260`…`+0x2E2C0` are that first iteration; the `+0xE0C0` / `+0x2E2D0` rows are
> the loop's pointer advance, not a field. `memset(02099FF0, 0, 0x200)` at `0026DC04`, `00268338`
> and `00267181` sizes the bank independently (OPUS).

| payload range | bytes | content | who |
|---|---:|---|---|
| `+0x0000`–`+0x01FF` | 512 | **the kind-3 authored-operand bank, `i16[256]`** (added 2026-09-11, OPUS-REQ-FABLE-PAYLOAD0): `ActorManager_BindLoadedDefinitionPayload` installs `SaveImage_GetPersistentPayloadBase()` (`002EF2B0` = buffer `+0x200` = payload `+0`) at slot 0's `+0x48` — the global `02098E58` — at `0026CAF8`–`0026CAFD`; reached only through that pointer by three accessors bounded at `0x100` with a 2-byte stride and gated by `02098E20` bit 0: `00264640` (get, `movzx`), `0026ABA0` (set), `0026B730` (element 0); the reader `AiTargetSelector_ResolveOperandValue` (`00321190`) sign-extends the element (`003211EC`). What the 256 entries mean is not established (OPUS: a stride-4 scan of the region finds nothing else referencing it). **Scripts write it (2026-09-12, FABLE-FZ22):** the same 512 bytes are the `global` class's offset `0` — 513 shipped scripts declare a `short` there (the decompiler's tool name `シナリオフラグ`, *scenario flag*) and 193 declare it as `global_flag[256]`, a `short[256]` array — so the operand bank the AI target selector sign-extends is script-authored state | script operands (scripts write, the selector reads) |
| `+0x0200`–`+0x0CF4` | 2805 | **the script-global variable space** (added 2026-09-12, FABLE-FZ22): every `global`-class script variable is a byte range here, addressed through the manager slot's `+0x48` by `ScriptVariable_Resolve` ([the storage-class page](../../01-Script-VM-Native-Bridge/Interpreter-Core/script-variables-and-their-storage-classes.md)); 9,448 scalar declarations at 587 offsets and 34 `global`-element arrays in 1,114 shipped scripts, none declared at two widths — the tables [`script-global-variables-by-offset.tsv`](../../01-Script-VM-Native-Bridge/Interpreter-Core/script-global-variables-by-offset.tsv), [`script-global-variables-by-script.tsv`](../../01-Script-VM-Native-Bridge/Interpreter-Core/script-global-variables-by-script.tsv) and [`script-global-arrays-by-offset.tsv`](../../01-Script-VM-Native-Bridge/Interpreter-Core/script-global-arrays-by-offset.tsv). The engine reads the region natively at one place found: `SaveloadManager_ShouldAutosaveForTransition` tests `+0xA00 + i == 1` (`002EF390`). See the box below §2.2 | the scripts, through the resolver |
| `+0x1044`–`+0x1063` | 32 | the world-transition record ([the save page](save-image-buffers-header-and-payload.md) §8d) | `WorldTransition_*` |
| `+0x1384`–`+0x1533` | 432 | the persistent flag banks (`Bank64A/B`, `Bank2048`, `Bank512`, `Primary`) | the flag accessors |
| `+0x2000`–`+0x7FFF` | ~~128~~ **24,576** | ~~**a mirror of the battle-state block's first 0x80 bytes**~~ **a copy of the battle-state block's first `0x6000` bytes — its older-build location** (corrected 2026-09-13 on `ASTRA-REQ-FABLE-MIRROR-COPY-EXTENT`: both copies run `0xC0` iterations of `0x80` bytes, `00229B81`–`00229BE2` and `00584515`–`00584572`; the earlier row counted one iteration. **`+0x4E48C` here is a PAYLOAD offset and is correct: the instructions read `+0x4E68C` (`00584504`, `00229B81`) because they are in BUFFER coordinates, and the payload begins `0x200` into the buffer — see §the buffer getters, “buffer `+0x4E68C` — payload `+0x4E48C`”. OPUS checked the two against the image on 2026-09-13, briefly “corrected” this to `+0x4E68C`, and reverted it: a coordinate system is not a typo, and the `0x200` that makes them differ is the header, not an error**), copied from `+0x4E48C` by `WorldTransitionSnapshot_CaptureRuntimeState` (`00229B40`) and `SaveTransition_PrepareRuntimeImageForCapture` (`005844A0`); the load guard's prelude `00235AF0` compares its `+0`, `+4`, `+0x5B42`, `+0x5B12` with the live block and on a difference copies it back (`002EF4A0`) and rebuilds the gambit banks; 2018-size saves carry their only copy of the block here | transition / load compatibility |
| `+0x8000`–`+0xC817` | 18,456 | **the image-backed state block** `*(020927C0)`: `+0x30` (0x1F4 B zeroed at init), **`+0x224` the 0x180 × 0x20 entry table the achievement page reads** (payload `+0x8224`; written by `003C5E50` / `003C60F0` / `003C8670`, read by `002551B0`), `+0x3244` / `+0x3245` flags, `+0x32C4` a bitmap ~~of 0x80 bytes~~ **whose accessors reach five bytes** (`00254DD0` tests, `00254E00` sets/clears; corrected 2026-09-18, OPUS — the third `0x80` on this page to be struck, after both group persistent banks), **`+0x3844` the "already fired" achievement bitmap** (payload `+0xB844`, 5 readers / 3 writers), `+0x47E8` (zeroed by `00255040`); its size `0x4818` and magic `0x0131F3EA` are written into the header at `+0x6C` / `+0x68` by `SaveRuntime_InitializeHeaderAndImageBackedState` (`00253A80`, `00253AED`–`00253AFB`) | achievements, inventory index |
| `+0xE000` | 4 | a u32 the finalizer writes (`00583F99`) | save |
| `+0xE040`–`+0xE23F` | 512 | **group persistent bank A** (~~128~~ **0x200 B**, corrected 2026-09-11) — `WorldPersistence_ExportGroupPersistentBank` (`0025D8E0`) writes it from `02099FF0`, `WorldPersistence_ImportGroupPersistentBank` (`00269A20`) reads it back | world persistence |
| `+0xE240`–`+0x2E24F` | 131,088 | **SpawnKeep image A**: `+0xE240` previous field id, `+0xE242` most-recent, bank 2 at `+0xE250`, bank 1 at `+0x1E250` — `SpawnKeep_SerializePersistenceBanks` (`00233440`) writes it from `00229B40` (`00229CF2`), `SpawnKeep_RestorePersistenceBank` (`00233550`) reads it from `005843E0` (`0058443B`) — the layout [the placement page](../../05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md) derived from the copy loops, now placed in the image. **THE PAIR IS ASYMMETRIC (OPUS, 2026-09-13, `ASTRA-CONTRA-OPUS-SPAWN-LIFECYCLE`):** the serializer `00233440` is 260 bytes and runs **two** `movups` bank loops plus the two field-id stores at `00233530`/`0023353A`; the restore `00233550` is 127 bytes and runs **one**, sourced from `lea rdx,[rcx+0x10]` — **bank 2 only** — followed by the two field-id stores at `002335BC`/`002335C7`. **Bank 1 at `+0x1E250` is written on save and is not read back by this helper.** Whether some other path restores it is **not established**; what is established is that this one does not, and a reader who sees two banks in the image and a serializer that writes both will assume otherwise | spawn keep |
| `+0x2E250`–`+0x2E44F` | 512 | **group persistent bank B** (~~128~~ **0x200 B**, corrected 2026-09-11) | world persistence |
| `+0x2E450`–`+0x4E45F` | 131,088 | **SpawnKeep image B**, read by `00233550` from `005843E0` (`0058445E`) — **the "persistence pair for the active slot"** that `WorldTransitionSnapshot_RestorePersistencePairForActiveSlot` restores is these two images, each with its group bank before it (stride `0x20210`) | spawn keep |
| `+0x4E460`–`+0x4E48B` | 44 | the save-transition metadata record (`SaveTransitionMetadata_CaptureToRecord` `002EF3C0`, `SaveTransitionMetadata_RestoreFromRecord` `002EF410`, `002EF540`, `WorldTransition_StageFieldTransition` `003145E0` at `+0x4E464`) | transition |
| `+0x4E48C`–`+0x5589B` | ~~23,312~~ **29,712** (`0x7410`, corrected 2026-09-11: the reset `002370C0` clears exactly that many bytes at `002370CD`; the inventory descriptors below and the gambit banks are *inside* the block — [the block page](../../11-Party/Battle-State-Block/the-battle-state-block-field-map.md)) | **the battle-state block `*(02EBF190)`** — `SaveRuntime_RebindImageBackedGameplayState` (`00238A80`, `00238A89`–`00238A92`) and `00233C10` (`00233C2A`–`00233C33`) point the global at `SaveImage_GetActiveRuntimeBuffer() + 0x4E68C`; the block opens with the magic **`0x05071901`** (`00233C4D`, the constant the header carries at `+0x60`), a flag dword at `+4`, and **the 40 party `BattleStatsRecord`s from `+8`** (`0x4E494`; every offset of the stats map applies at `+0x4E494 + d`); the fields at block `+0x5B00`–`+0x5B0E` (`00233C83`–`00233C9E`) are the last touched. Its first ~~0x80~~ `0x6000` bytes *(corrected 2026-10-02, OPUS: the capture copies `0x6000`, `00229B76`–`00229BE2`; this map's `+0x2000` row)* are what the capture functions mirror to `+0x2000` | battle state, party |
| `+0x53C54`–`+0x53C9B`, `+0x53E54` | 72 + 2 | (block `+0x57C8`) inventory class descriptors rebased on load by `InventoryRuntime_RebaseClassDescriptorsAndClearDerivedState` (`0030B6A0`) — **pointers stored in the image and fixed up after load** | inventory |

> **The script-global region, 2026-09-12 (FABLE-FZ22).** The census behind this page follows the
> buffer getters and reaches one row between `+0x200` and `+0xD00` (`+0xA00`), because scripts reach
> the region through a pointer the census does not seed: `ActorManager_BindLoadedDefinitionPayload`
> installs `SaveImage_GetPersistentPayloadBase()` at each manager slot's `+0x48`, and the variable
> resolver adds a 24-bit offset from the script's descriptor table to it ([the storage-class page](../../01-Script-VM-Native-Bridge/Interpreter-Core/script-variables-and-their-storage-classes.md) §2.3).
> Decoding every shipped script's descriptor table gives the region's owners:
>
> | what | count | where |
> |---|---:|---|
> | scalar `global` declarations | 9,448 in 738 scripts | 587 offsets, `+0x0` and `+0x200`–`+0xCF4`; 646 bytes covered; no offset declared at two widths |
> | `global`-element arrays | 34 distinct (base, width, dims) in 639 scripts | `+0x0` (`short[256]`), `+0x31F`–`+0xCEE`; 608 bytes covered |
> | most-shared | `+0x940` `char` in 575 scripts (tool name `mp_last_weather`); `+0x900`/`+0x904`/`+0x908`/`+0x90C` `float` in 418–419 (`mp_map_set_angle` / `_x` / `_y` / `_z` — a map's saved player pose, written from `getangle` before `rlookat` in `alc_a01`); `+0x910` `int` in 407 (`mp_map_flg`); `+0xB14` `u_char[94]` in 121 (`quest_global_flag`); `+0xC7C` `float[3]` in 97 (`g_com_navi_footcalc`) | |
> | names | 288 of the 587 scalar offsets and 24 array-only offsets carry a name from **ff12-script 3.0's built-in `globalMap`** (`CScriptContainerInitializers.cpp`, 1,022 entries), a tool-side table whose own provenance is not established; one conflict (`+0x0`, `シナリオフラグ` vs `global_flag[256]`); the tool's `global_var_N` fallbacks are per-script indices and are not names | the `tool_name` column of the by-offset table |
> | native readers inside the region | one: `002EF390` (`buffer + 0xC00 + i == 1`, i.e. payload `+0xA00 + i`), called by `SaveloadManager_ShouldAutosaveForTransition` (`001C1720`, `001C17C3`) with `i` taken from the matching entry of its 16-byte transition table — a **per-index autosave enable byte** that scripts set (`+0xA00`–`+0xA1D` declared `u_char` by 2–34 scripts each) and the transition gate reads | `+0xA00`–`+0xA71` |
>
> So the region is script-owned state with one engine consumer; the 2,805 bytes are saved and loaded
> verbatim with the rest of the payload, and their meanings are the scripts' (FZ-27 for the shared
> ones). Coverage is by declaration, not by use: a byte no shipped script declares may still be
> reserved by the authoring tool's table.

### 2.3 The payload, offset by offset

| offset | width | name | w / r | writers | readers |
|---|---|---|---|---|---|
| `+0x0000` | 0 |  | 0 / 1 |  | `002EF2D0` (`002EF2E1`) |
| `+0x0A00` | 1 |  | 0 / 1 |  | `002EF390` (`002EF3A0`) — indexed: `+0xA00 + i`, the autosave enable bytes scripts set (the §2.2 box) |
| `+0x1000` | 1 |  | 1 / 3 | `0046B3F0` (`0046B43B` +1) | `0046B0F0` (`0046B105`); `0046B240` (`0046B274`); +1 more |
| `+0x1020` | 1 |  | 1 / 2 | `0046B290` (`0046B2E8` +1) | `0046B020` (`0046B035`); `0046B1A0` (`0046B1D4`) |
| `+0x1040` | 4 |  | 1 / 2 | `0046B290` (`0046B2DA`) | `0046B0B0` (`0046B0B9`); `0046B290` (`0046B2C9`) |
| `+0x1044` | 4 | active or pending field id (world-transition record) | 4 / 4 | `WorldTransition_StageFieldTransition` `003145E0` (`00314685`); `WorldTransition_ResetState` `00314970` (`0031498D`); `WorldTransition_SetActiveOrPendingFieldId` `00314DC0` (`00314DCD`); +1 more | `WorldTransition_RequeueCurrentFieldForRestore` `00314530` (`0031456F`); `WorldTransition_StageFieldTransition` `003145E0` (`0031466E`); +2 more |
| `+0x1048` | 4 | destination parameter | 4 / 3 | `WorldTransition_StageFieldTransition` `003145E0` (`003146A9`); `WorldTransition_ResetState` `00314970` (`0031499C`); `WorldTransition_SetDestinationParameter` `00314D80` (`00314D8D`); +1 more | `WorldTransition_StageFieldTransition` `003145E0` (`00314698`); `WorldTransition_GetDestinationParameter` `003148B0` (`003148B9`); +1 more |
| `+0x104C` | 4 | previous field id | 3 / 2 | `WorldTransition_StageFieldTransition` `003145E0` (`00314674`); `WorldTransition_ResetState` `00314970` (`003149AB`); `SaveLoad_NormalizeLoadedRuntimeStateAndReseedRNG` `00584210` (`0058434A`) | `WorldTransition_GetPreviousFieldId` `00314870` (`00314879`); `SaveLoad_NormalizeLoadedRuntimeStateAndReseedRNG` `00584210` (`00584293`) |
| `+0x1050` | 4 | previous destination parameter | 3 / 2 | `WorldTransition_StageFieldTransition` `003145E0` (`0031469E`); `WorldTransition_ResetState` `00314970` (`003149BA`); `SaveLoad_NormalizeLoadedRuntimeStateAndReseedRNG` `00584210` (`00584356`) | `WorldTransition_GetPreviousDestinationParameter` `00314850` (`00314859`); `SaveLoad_NormalizeLoadedRuntimeStateAndReseedRNG` `00584210` (`0058429F`) |
| `+0x1054` | 4 | options | 4 / 2 | `WorldTransition_StageFieldTransition` `003145E0` (`003146B6`); `WorldTransition_ResetState` `00314970` (`003149C9`); `WorldTransition_SetOptions` `00314DA0` (`00314DAD`); +1 more | `WorldTransition_GetOptions` `003148D0` (`003148D9`); `SaveLoad_NormalizeLoadedRuntimeStateAndReseedRNG` `00584210` (`005842AB`) |
| `+0x1058` | 4 | (transition record, unnamed) | 1 / 0 | `WorldTransition_StageFieldTransition` `003145E0` (`003146C8`) |  |
| `+0x105C` | 4 | transition field id | 2 / 1 | `WorldTransition_RequeueCurrentFieldForRestore` `00314530` (`00314586`); `WorldTransition_StageFieldTransition` `003145E0` (`003146D3`) | `WorldTransition_GetTransitionFieldId` `00314910` (`00314919`) |
| `+0x1060` | 1 | field runtime parameter | 1 / 4 | `WorldField_InitializeCurrentFieldRuntimeParameters` `0026D910` (`0026D95E`) | `0025ACA0` (`0025ACC1`); `002620E0` (`00262123` +2); +2 more |
| `+0x1061` | 1 | initialization state | 4 / 1 | `WorldPersistence_ResetBanksAndMarkInitializationState` `00268320` (`0026836C`); `0026D8F0` (`0026D8F9`); `WorldField_InitializeCurrentFieldRuntimeParameters` `0026D910` (`0026DA92`); +1 more | `WorldField_InitializeCurrentFieldRuntimeParameters` `0026D910` (`0026D951`) |
| `+0x1062` | 1 | per-transition flag byte | 11 / 8 | `WorldTransition_RequeueCurrentFieldForRestore` `00314530` (`00314563`); `WorldTransition_StageFieldTransition` `003145E0` (`003146DE`); `WorldTransition_ClearFlag1062_Bit04` `003149E0` (`003149E9`); +8 more | `WorldPersistence_ResetBanksForFieldTransition` `0026DB30` (`0026DBF4`); `00314A60` (`00314A69`); +6 more |
| `+0x1063` | 1 | (transition record, unnamed) | 5 / 5 | `002628B0` (`00262A6A`); `0026A720` (`0026A731` +1); `00314A00` (`00314A39` +2); +2 more | `ActorManager_RunFieldRuntimePass` `0025D9E0` (`0025DBA8`); `00261F90` (`0026201B`); +3 more |
| `+0x1064` | 1 |  | 1 / 1 | `0046B490` (`0046B4A4`) | `0046B180` (`0046B18E`) |
| `+0x1164` | 2 |  | 2 / 1 | `0046B350` (`0046B364`); `0046B3F0` (`0046B44E`) | `0046B0D0` (`0046B0DE`) |
| `+0x1364` | 1 |  | 1 / 1 | `0046B380` (`0046B3B5` +1) | `0046B1F0` (`0046B224`) |
| `+0x1384` | 1 | `Bank64A` | 1 / 1 | `PersistentFlag_SetBank64A` `0032AC70` (`0032ACB3` +1) | `PersistentFlag_QueryBank64A` `0032A9A0` (`0032A9E4`) |
| `+0x138C` | 1 | `Bank64B` | 1 / 1 | `PersistentFlag_SetBank64B` `0032ACF0` (`0032AD33` +1) | `PersistentFlag_QueryBank64B` `0032AA00` (`0032AA44`) |
| `+0x13B4` | 1 | `Bank2048` | 1 / 1 | `PersistentFlag_SetBank2048` `0032ABF0` (`0032AC36` +1) | `PersistentFlag_QueryBank2048` `0032A930` (`0032A97B`) |
| `+0x14B4` | 1 | `Bank512` | 2 / 2 | `PersistentFlag_SetBank512Low` `0032AD70` (`0032ADB6` +1); `PersistentFlag_SetBank512High` `0032ADF0` (`0032AE3A` +1) | `PersistentFlag_QueryBank512Low` `0032AA60` (`0032AAAB`); `PersistentFlag_QueryBank512High` `0032AAD0` (`0032AB1F`) |
| `+0x14F4` | 1 | `Primary` flags | 1 / 1 | `PersistentFlag_SetPrimary` `0032AB60` (`0032ABA8` +1) | `PersistentFlag_QueryPrimaryOrAuthoredThresholdGate` `0032A8A0` (`0032A900`) |
| `+0x1534` | 1 |  | 2 / 3 | `002628B0` (`00262A76`); `0026A720` (`0026A73D` +1) | `ActorManager_RunFieldRuntimePass` `0025D9E0` (`0025DBB6`); `00261F90` (`00262029`); +1 more |
| `+0x1535` | 1 |  | 1 / 0 | `002EF370` (`002EF37D`) |  |
| `+0x2000` | 16 | start of the `0x6000`-byte copy of the battle-state block (copied from `+0x4E48C`; ~~first 0x80 bytes~~ corrected 2026-09-13) | 2 / 2 | `WorldTransitionSnapshot_CaptureRuntimeState` `00229B40` (`00229BA2`); `SaveTransition_PrepareRuntimeImageForCapture` `005844A0` (`00584532`) | `00235AF0` (`00235B00` +1); `SaveTransition_PrepareRuntimeImageForCapture` `005844A0` (`00584515`) |
| `+0x2004` | 4 |  | 0 / 1 |  | `00235AF0` (`00235B24`) |
| `+0x2010` | 16 | (the mirror) | 2 / 0 | `WorldTransitionSnapshot_CaptureRuntimeState` `00229B40` (`00229BAA`); `SaveTransition_PrepareRuntimeImageForCapture` `005844A0` (`0058453A`) |  |
| `+0x2020` | 16 |  | 2 / 0 | `WorldTransitionSnapshot_CaptureRuntimeState` `00229B40` (`00229BB2`); `SaveTransition_PrepareRuntimeImageForCapture` `005844A0` (`00584542`) |  |
| `+0x2030` | 16 |  | 2 / 0 | `WorldTransitionSnapshot_CaptureRuntimeState` `00229B40` (`00229BBA`); `SaveTransition_PrepareRuntimeImageForCapture` `005844A0` (`0058454A`) |  |
| `+0x2040` | 16 |  | 2 / 0 | `WorldTransitionSnapshot_CaptureRuntimeState` `00229B40` (`00229BC2`); `SaveTransition_PrepareRuntimeImageForCapture` `005844A0` (`00584552`) |  |
| `+0x2050` | 16 |  | 2 / 0 | `WorldTransitionSnapshot_CaptureRuntimeState` `00229B40` (`00229BCA`); `SaveTransition_PrepareRuntimeImageForCapture` `005844A0` (`0058455A`) |  |
| `+0x2060` | 16 |  | 2 / 0 | `WorldTransitionSnapshot_CaptureRuntimeState` `00229B40` (`00229BD2`); `SaveTransition_PrepareRuntimeImageForCapture` `005844A0` (`00584562`) |  |
| `+0x2070` | 16 |  | 2 / 0 | `WorldTransitionSnapshot_CaptureRuntimeState` `00229B40` (`00229BDA`); `SaveTransition_PrepareRuntimeImageForCapture` `005844A0` (`0058456A`) |  |
| `+0x2080` | 0 | ~~(end of the mirror)~~ the copy loop's per-iteration pointer step (`lea rax, [rax + 0x80]`), not an end — the copy runs `0xC0` iterations to `+0x7FFF` (corrected 2026-09-13) | 0 / 2 |  | `WorldTransitionSnapshot_CaptureRuntimeState` `00229B40` (`00229B91`); `SaveTransition_PrepareRuntimeImageForCapture` `005844A0` (`00584521`) |
| `+0x7B12` | 2 | the copy's block `+0x5B12`: member 0, bank 0, slot 0's action word — one of the importer's four probe fields ([battle-state block §2.9](../../11-Party/Battle-State-Block/the-battle-state-block-field-map.md)) | 0 / 1 |  | `00235AF0` (`00235B41`) |
| `+0x7B42` | 1 | the copy's block `+0x5B42`: member 0, bank 0's count byte `+0x32` — a probe field (§2.9 of the battle-state block page) | 0 / 1 |  | `00235AF0` (`00235B31`) |
| `+0x8000` | 0 | **image-backed state block** (`*(020927C0)` = buffer + 0x8200), 0x4818 B — begins | 0 / 7 |  | `InventoryDerivedIndex_AddPresentItem` `00252E60` (`00252EB5`); `00252F70` (`00252F8F`); +5 more |
| `+0x8008` | 16 |  | 1 / 1 | `00394130` (`0039423B`) | `00394130` (`003942CA`) |
| `+0x8018` | 16 |  | 1 / 1 | `00394130` (`00394246`) | `00394130` (`003942D5`) |
| `+0x8028` | 8 |  | 1 / 1 | `00394130` (`00394252`) | `00394130` (`003942E0`) |
| `+0x8030` | 2 | image-backed block `+0x30` | 2 / 2 | `00252610` (`002526AA`); `002527B0` (`00252819` +1) | `002526F0` (`00252793`); `SaveRuntime_InitializeHeaderAndImageBackedState` `00253A80` (`00253B3E`) |
| `+0x8090` | 4 |  | 2 / 1 | `00252610` (`0025265B` +1); `002527B0` (`002527CF` +1) | `002526F0` (`0025273B` +1) |
| `+0x8224` | 16 | ~~**achievement / counter entry table**~~ **the navigation-map revealed-tile table** (block `+0x224`, 0x180 × 0x20 B, one 256-bit tile bitmap per navimap id — FG-1, 2026-09-12) — entry 0 | 3 / 1 | `003C5E50` (`003C5E8D`); `003C60F0` (`003C611D`); `003C8670` (`003C869C`) | `002551B0` (`002551E3`) |
| `+0x8234` | 16 | (entry 0, second half) | 3 / 1 | `003C5E50` (`003C5E97`); `003C60F0` (`003C6127`); `003C8670` (`003C86A6`) | `002551B0` (`002551E9`) |
| `+0xB244` | 1 | block `+0x3244` **the inventory category flags** — bit *n* set by `002CD650` when category *n*'s derived list is non-empty (1 weapons, 2 armour, 3 ammunition, 4 items, 5 magicks / technicks, 6 loot, 7 key items other than maps, 8 accessories; [the encoded-id space page](../../00-Engine-Core-Runtime/the-encoded-id-space-and-the-query-record.md) §2.9); ~~bit 0 kept, bit 1 cleared at init~~ zero after init *(corrected 2026-10-02, OPUS: `00253B1C` keeps bit 0, but `00253B47`–`00253B56` then zero `+0x3244` for `0x80` bytes; katano-debug-savedata.md)* | 3 / 2 | `00252D40` (`00252D67` +1); `00253480` (`002534AA`); `SaveRuntime_InitializeHeaderAndImageBackedState` `00253A80` | `00252D10` (`00252D2E`); the menu code |
| `+0xB245` | 1 | block `+0x3245` | 2 / 0 | `00253480` (`002534B1`); `SaveRuntime_InitializeHeaderAndImageBackedState` `00253A80` (`00253B23`) |  |
| `+0xB2C4` | 1 | block `+0x32C4` bitmap, ~~0x80 B~~ **five bytes reached, upper bound not established** (`00254E00` / `00254DD0`) — corrected 2026-09-18, OPUS: every call site hands a compile-time constant and the largest is `0x23`, so byte `4` is the highest the accessors touch | 2 / 1 | `SaveRuntime_InitializeHeaderAndImageBackedState` `00253A80` (`00253B5D`); `00254E00` (`00254E27` +1) | `00254E00` (`00254E2E`) |
| `+0xB2CC` | 1 |  | 1 / 2 | `00315910` (`00315975` +1) | `003154B0` (`003154FD`); `00315910` (`00315965` +1) |
| `+0xB30C` | 1 |  | 1 / 2 | `00315B50` (`00315BB8` +1) | `003156E0` (`00315737`); `00315B50` (`00315BA4`) |
| `+0xB34C` | 1 |  | 1 / 2 | `00315A20` (`00315A70`) | `00315620` (`00315647`); `00315A20` (`00315A4B` +1) |
| `+0xB36C` | 1 |  | 1 / 2 | `00315CD0` (`00315D29`) | `00315470` (`00315493`); `00315CD0` (`00315D00`) |
| `+0xB3F4` | 1 |  | 1 / 2 | `00315B50` (`00315C06` +1) | `003156E0` (`0031577E`); `00315B50` (`00315BF2`) |
| `+0xB404` | 1 |  | 3 / 4 | `00315820` (`0031588E`); `00315A90` (`00315AB7`); `00316930` (`00316A0C`) | `00315420` (`00315440` +1); `00315820` (`0031583E` +2); +2 more |
| `+0xB604` | 1 |  | 2 / 4 | `00315AD0` (`00315B2D`); `00315B50` (`00315C65`) | `00315670` (`00315697`); `003156E0` (`003157B7`); +2 more |
| `+0xB844` | 1 | block `+0x3844` — the "already fired" achievement bitmap | 3 / 5 | `00315910` (`003159FE`); `00315E90` (`00316069`); `00316A50` (`00316ADB` +1) | `003154B0` (`00315612`); `00315910` (`003159D9` +1); +3 more |
| `+0xB845` | 1 |  | 0 / 1 |  | `00316440` (`00316449`) |
| `+0xB848` | 1 |  | 1 / 2 | `00315B50` (`00315CA7`) | `003156E0` (`00315805`); `00315B50` (`00315C8E`) |
| `+0xB84C` | 0 |  | 3 / 5 | `00316810` (`0031689D` +3); `00316BF0` (`00316C30` +1); `00316C60` (`00316CA3` +1) | `003162E0` (`0031631C` +2); `003166F0` (`00316705` +2); +3 more |
| `+0xB868` | 4 |  | 0 / 1 |  | `00315390` (`003153A4`) |
| `+0xC7B8` | 4 |  | 0 / 2 |  | `00250270` (`002502D9` +1); `00252FA0` (`00252FD7`) |
| `+0xC7E8` | 8 | block `+0x47E8` (zeroed by `00255040`) | 2 / 2 | `00254CC0` (`00254D06` +1); `00255040` (`00255047`) | `002542B0` (`002542D1`); `00254CC0` (`00254D0F`) |
| `+0xE000` | 4 | u32 written by the finalizer | 1 / 0 | `SaveImage_FinalizeHeaderAndChecksum` `00583D60` (`00583F99`) |  |
| `+0xE040` | 0 | group persistent bank A, ~~0x80 B~~ **0x200 B** (`0025D8E0` / `00269A20`; the rows to `+0xE0B0` are the export loop's first iteration) | 1 / 6 | `WorldPersistence_ExportGroupPersistentBank` `0025D8E0` (`0025D901`) | `WorldTransitionSnapshot_CaptureRuntimeState` `00229B40` (`00229CDF`); `SaveLoad_NormalizeLoadedRuntimeStateAndReseedRNG` `00584210` (`0058432B`); +4 more |
| `+0xE050` | 16 |  | 1 / 1 | `WorldPersistence_ExportGroupPersistentBank` `0025D8E0` (`0025D909`) | `WorldPersistence_ImportGroupPersistentBank` `00269A20` (`00269A45`) |
| `+0xE060` | 16 |  | 1 / 1 | `WorldPersistence_ExportGroupPersistentBank` `0025D8E0` (`0025D911`) | `WorldPersistence_ImportGroupPersistentBank` `00269A20` (`00269A4D`) |
| `+0xE070` | 16 |  | 1 / 1 | `WorldPersistence_ExportGroupPersistentBank` `0025D8E0` (`0025D919`) | `WorldPersistence_ImportGroupPersistentBank` `00269A20` (`00269A55`) |
| `+0xE080` | 16 |  | 1 / 1 | `WorldPersistence_ExportGroupPersistentBank` `0025D8E0` (`0025D921`) | `WorldPersistence_ImportGroupPersistentBank` `00269A20` (`00269A5D`) |
| `+0xE090` | 16 |  | 1 / 1 | `WorldPersistence_ExportGroupPersistentBank` `0025D8E0` (`0025D929`) | `WorldPersistence_ImportGroupPersistentBank` `00269A20` (`00269A65`) |
| `+0xE0A0` | 16 |  | 1 / 1 | `WorldPersistence_ExportGroupPersistentBank` `0025D8E0` (`0025D931`) | `WorldPersistence_ImportGroupPersistentBank` `00269A20` (`00269A6D`) |
| `+0xE0B0` | 16 |  | 1 / 1 | `WorldPersistence_ExportGroupPersistentBank` `0025D8E0` (`0025D939`) | `WorldPersistence_ImportGroupPersistentBank` `00269A20` (`00269A75`) |
| `+0xE0C0` | 0 |  | 0 / 2 |  | `WorldPersistence_ExportGroupPersistentBank` `0025D8E0` (`0025D8F0`); `WorldPersistence_ImportGroupPersistentBank` `00269A20` (`00269A3A`) |
| `+0xE240` | 0 | **SpawnKeep image A**: previous field id | 1 / 4 | `SpawnKeep_SerializePersistenceBanks` `00233440` (`00233530`) | `WorldTransitionSnapshot_CaptureRuntimeState` `00229B40` (`00229CEB`); `WorldTransitionSnapshot_RestorePersistencePairForActiveSlot` `005843E0` (`00584434`); +2 more |
| `+0xE242` | 2 | most-recent field id | 1 / 1 | `SpawnKeep_SerializePersistenceBanks` `00233440` (`0023353A`) | `SpawnKeep_RestorePersistenceBank` `00233550` (`002335C3`) |
| `+0xE250` | 0 | bank 2 of image A (~~0x10000~~ a `0x10000` slot holding `0x9400` copied bytes and a `0x6C00` zero tail *(corrected 2026-10-02, OPUS: `00233448`, `0023345D`, `00233560` — `0x128` passes of `0x80`)*) | 1 / 2 | `SpawnKeep_SerializePersistenceBanks` `00233440` (`00233481`) | `SpawnKeep_SerializePersistenceBanks` `00233440` (`00233468`); `SpawnKeep_RestorePersistenceBank` `00233550` (`0023355C` +1) |
| `+0xE260` | 16 |  | 1 / 1 | `SpawnKeep_SerializePersistenceBanks` `00233440` (`00233489`) | `SpawnKeep_RestorePersistenceBank` `00233550` (`0023357B`) |
| `+0xE270` | 16 |  | 1 / 1 | `SpawnKeep_SerializePersistenceBanks` `00233440` (`00233491`) | `SpawnKeep_RestorePersistenceBank` `00233550` (`00233583`) |
| `+0xE280` | 16 |  | 1 / 1 | `SpawnKeep_SerializePersistenceBanks` `00233440` (`00233499`) | `SpawnKeep_RestorePersistenceBank` `00233550` (`0023358B`) |
| `+0xE290` | 16 |  | 1 / 1 | `SpawnKeep_SerializePersistenceBanks` `00233440` (`002334A1`) | `SpawnKeep_RestorePersistenceBank` `00233550` (`00233593`) |
| `+0xE2A0` | 16 |  | 1 / 1 | `SpawnKeep_SerializePersistenceBanks` `00233440` (`002334A9`) | `SpawnKeep_RestorePersistenceBank` `00233550` (`0023359B`) |
| `+0xE2B0` | 16 |  | 1 / 1 | `SpawnKeep_SerializePersistenceBanks` `00233440` (`002334B1`) | `SpawnKeep_RestorePersistenceBank` `00233550` (`002335A3`) |
| `+0xE2C0` | 16 |  | 1 / 1 | `SpawnKeep_SerializePersistenceBanks` `00233440` (`002334B9`) | `SpawnKeep_RestorePersistenceBank` `00233550` (`002335AB`) |
| `+0xE2D0` | 0 |  | 0 / 2 |  | `SpawnKeep_SerializePersistenceBanks` `00233440` (`00233470`); `SpawnKeep_RestorePersistenceBank` `00233550` (`00233570`) |
| `+0x1E250` | 0 | bank 1 of image A (~~0x10000~~ a `0x10000` slot holding `0x9400` copied bytes and a `0x6C00` zero tail *(corrected 2026-10-02, OPUS: `00233448`, `0023345D` — `0x128` passes of `0x80`)*) | 1 / 1 | `SpawnKeep_SerializePersistenceBanks` `00233440` (`002334E7`) | `SpawnKeep_SerializePersistenceBanks` `00233440` (`002334CF`) |
| `+0x1E260` | 16 |  | 1 / 0 | `SpawnKeep_SerializePersistenceBanks` `00233440` (`002334EF`) |  |
| `+0x1E270` | 16 |  | 1 / 0 | `SpawnKeep_SerializePersistenceBanks` `00233440` (`002334F7`) |  |
| `+0x1E280` | 16 |  | 1 / 0 | `SpawnKeep_SerializePersistenceBanks` `00233440` (`002334FF`) |  |
| `+0x1E290` | 16 |  | 1 / 0 | `SpawnKeep_SerializePersistenceBanks` `00233440` (`00233507`) |  |
| `+0x1E2A0` | 16 |  | 1 / 0 | `SpawnKeep_SerializePersistenceBanks` `00233440` (`0023350F`) |  |
| `+0x1E2B0` | 16 |  | 1 / 0 | `SpawnKeep_SerializePersistenceBanks` `00233440` (`00233517`) |  |
| `+0x1E2C0` | 16 |  | 1 / 0 | `SpawnKeep_SerializePersistenceBanks` `00233440` (`0023351F`) |  |
| `+0x1E2D0` | 0 |  | 0 / 1 |  | `SpawnKeep_SerializePersistenceBanks` `00233440` (`002334D6`) |
| `+0x2E250` | 0 | group persistent bank B, ~~0x80 B~~ **0x200 B** | 1 / 3 | `WorldPersistence_ExportGroupPersistentBank` `0025D8E0` (`0025D901`) | `WorldTransitionSnapshot_CaptureRuntimeState` `00229B40` (`00229CCA`); `WorldTransitionSnapshot_RestorePersistencePairForActiveSlot` `005843E0` (`0058444B`); +1 more |
| `+0x2E260` | 16 |  | 1 / 1 | `WorldPersistence_ExportGroupPersistentBank` `0025D8E0` (`0025D909`) | `WorldPersistence_ImportGroupPersistentBank` `00269A20` (`00269A45`) |
| `+0x2E270` | 16 |  | 1 / 1 | `WorldPersistence_ExportGroupPersistentBank` `0025D8E0` (`0025D911`) | `WorldPersistence_ImportGroupPersistentBank` `00269A20` (`00269A4D`) |
| `+0x2E280` | 16 |  | 1 / 1 | `WorldPersistence_ExportGroupPersistentBank` `0025D8E0` (`0025D919`) | `WorldPersistence_ImportGroupPersistentBank` `00269A20` (`00269A55`) |
| `+0x2E290` | 16 |  | 1 / 1 | `WorldPersistence_ExportGroupPersistentBank` `0025D8E0` (`0025D921`) | `WorldPersistence_ImportGroupPersistentBank` `00269A20` (`00269A5D`) |
| `+0x2E2A0` | 16 |  | 1 / 1 | `WorldPersistence_ExportGroupPersistentBank` `0025D8E0` (`0025D929`) | `WorldPersistence_ImportGroupPersistentBank` `00269A20` (`00269A65`) |
| `+0x2E2B0` | 16 |  | 1 / 1 | `WorldPersistence_ExportGroupPersistentBank` `0025D8E0` (`0025D931`) | `WorldPersistence_ImportGroupPersistentBank` `00269A20` (`00269A6D`) |
| `+0x2E2C0` | 16 |  | 1 / 1 | `WorldPersistence_ExportGroupPersistentBank` `0025D8E0` (`0025D939`) | `WorldPersistence_ImportGroupPersistentBank` `00269A20` (`00269A75`) |
| `+0x2E2D0` | 0 |  | 0 / 2 |  | `WorldPersistence_ExportGroupPersistentBank` `0025D8E0` (`0025D8F0`); `WorldPersistence_ImportGroupPersistentBank` `00269A20` (`00269A3A`) |
| `+0x2E450` | 0 | **SpawnKeep image B**: previous field id | 0 / 3 |  | `WorldTransitionSnapshot_CaptureRuntimeState` `00229B40` (`00229CD6`); `WorldTransitionSnapshot_RestorePersistencePairForActiveSlot` `005843E0` (`00584457`); +1 more |
| `+0x2E452` | 2 | most-recent field id | 0 / 1 |  | `SpawnKeep_RestorePersistenceBank` `00233550` (`002335C3`) |
| `+0x2E460` | 0 | bank 2 of image B | 0 / 1 |  | `SpawnKeep_RestorePersistenceBank` `00233550` (`0023355C` +1) |
| `+0x2E470` | 16 |  | 0 / 1 |  | `SpawnKeep_RestorePersistenceBank` `00233550` (`0023357B`) |
| `+0x2E480` | 16 |  | 0 / 1 |  | `SpawnKeep_RestorePersistenceBank` `00233550` (`00233583`) |
| `+0x2E490` | 16 |  | 0 / 1 |  | `SpawnKeep_RestorePersistenceBank` `00233550` (`0023358B`) |
| `+0x2E4A0` | 16 |  | 0 / 1 |  | `SpawnKeep_RestorePersistenceBank` `00233550` (`00233593`) |
| `+0x2E4B0` | 16 |  | 0 / 1 |  | `SpawnKeep_RestorePersistenceBank` `00233550` (`0023359B`) |
| `+0x2E4C0` | 16 |  | 0 / 1 |  | `SpawnKeep_RestorePersistenceBank` `00233550` (`002335A3`) |
| `+0x2E4D0` | 16 |  | 0 / 1 |  | `SpawnKeep_RestorePersistenceBank` `00233550` (`002335AB`) |
| `+0x2E4E0` | 0 |  | 0 / 1 |  | `SpawnKeep_RestorePersistenceBank` `00233550` (`00233570`) |
| `+0x4E460` | 0 | save-transition metadata record (`002EF3C0` / `002EF410`) | 2 / 4 | `WorldTransitionSnapshot_CapturePersistencePairForActiveSlot` `00584580` (`005845C2`); `002EF540` (`002EF547`) | `WorldTransitionSnapshot_CaptureRuntimeState` `00229B40` (`00229CF7`); `SaveLoad_NormalizeLoadedRuntimeStateAndReseedRNG` `00584210` (`00584371`); +2 more |
| `+0x4E464` | 4 |  | 2 / 0 | `WorldTransition_StageFieldTransition` `003145E0` (`00314731`); `SaveTransitionMetadata_CaptureToRecord` `002EF3C0` (`002EF3C9`) |  |
| `+0x4E468` | 16 |  | 1 / 1 | `SaveTransitionMetadata_CaptureToRecord` `002EF3C0` (`002EF3DA`) | `SaveTransitionMetadata_RestoreFromRecord` `002EF410` (`002EF420` +1) |
| `+0x4E46C` | 4 |  | 0 / 1 |  | `SaveTransitionMetadata_RestoreFromRecord` `002EF410` (`002EF463`) |
| `+0x4E470` | 16 |  | 1 / 1 | `002EF540` (`002EF551`) | `SaveTransitionMetadata_RestoreFromRecord` `002EF410` (`002EF46D`) |
| `+0x4E478` | 16 |  | 1 / 1 | `SaveTransitionMetadata_CaptureToRecord` `002EF3C0` (`002EF3EC`) | `SaveTransitionMetadata_RestoreFromRecord` `002EF410` (`002EF43B` +1) |
| `+0x4E480` | 8 |  | 1 / 1 | `002EF540` (`002EF55D`) | `SaveTransitionMetadata_RestoreFromRecord` `002EF410` (`002EF453`) |
| `+0x4E488` | 4 |  | 2 / 1 | `002EF540` (`002EF568`); `SaveTransitionMetadata_CaptureToRecord` `002EF3C0` (`002EF3FD`) | `SaveTransitionMetadata_RestoreFromRecord` `002EF410` (`002EF432`) |
| `+0x4E48C` | 0 | **the battle-state block** `*(02EBF190)` begins: its magic `0x05071901` (checked at `00233C4D`) | 4 / 9 | `WorldTransitionSnapshot_CaptureRuntimeState` `00229B40` (`00229C01`); `002370C0` (`002370DF`); `DefinitionRuntime_DeactivateAndRemoveConfiguredItems` `00323540` (`003235A3`); +1 more | `WorldTransitionSnapshot_CaptureRuntimeState` `00229B40` (`00229B81` +3); `00235AF0` (`00235B19`); +7 more |
| `+0x4E490` | 4 | battle-state block `+4` flags (bit `0x1000` set/cleared by `00233C10`) | 6 / 14 | `00233C10` (`00233CA6`); `00239960` (`002399FB` +7); `0023A2C0` (`0023A2CB` +1); +3 more | `00235AF0` (`00235B20`); `00236740` (`00236747` +4); +12 more |
| `+0x4E491` | 1 |  | 0 / 7 |  | `003202F0` (`00320319`); `DefinitionRuntime_DeactivateAndRemoveConfiguredItems` `00323540` (`0032354A`); +5 more |
| `+0x4E492` | 2 |  | 1 / 2 | `BattleStats_RecomputeDerivedStateAndAutoStatuses` `0030FED0` (`00310594`) | `BattleStats_ReconcileResourcesToEffectiveCapacity` `0030F5A0` (`0030F602` +1); `BattleStats_RecomputeDerivedStateAndAutoStatuses` `0030FED0` (`00310566`) |
| `+0x4E494` | 0 | **party stats record 0** (block `+8`; 40 × `0x1C8` follow) — offsets `+0x4E494 + d` are `BattleStatsRecord +d` ([the stats map](../../08-Combat-Formula/Battle-Stats-Record/the-battle-stats-record-field-map.md)) *(9 census row(s) removed 2026-09-13 as route-contaminated (§8); counts not regenerated)* | 9 / 34 | `00239960` (`00239D89` +1); ~~`Battle_ProcessActionTarget` `00307300` (`003079FC` +1)~~; `00311AF0` (`00311B06` +1); +6 more | ~~`Battle_ProcessActionTarget` `00307300` (`00307460`)~~; `00309B40` (`00309B53`); +32 more |
| `+0x4E498` | 1 | record 0 `+4` (definition id) *(1 census row(s) removed 2026-09-13 as route-contaminated (§8); counts not regenerated)* | 3 / 35 | `BattleStats_InitializeDefinitionRecord` `0023AC80` (`0023AD8E`); `0030C470` (`0030C507`); `BattleStats_AdvanceLevelToTargetAndRecomputeGrowth` `0030C650` (`0030C753`) | `002371B0` (`0023721F`); `002372E0` (`0023735F`); +33 more |
| `+0x4E499` | 1 | record 0 `+5` (kind byte) | 0 / 34 |  | `002371B0` (`00237214`); `002372E0` (`00237354`); +32 more |
| `+0x4E49A` | 2 |  | 2 / 6 | `BattleStats_RecomputeDerivedStateAndAutoStatuses` `0030FED0` (`00310594`); `BattleStats_ModifySecondaryResource` `00300BC0` (`00300C6A`) | `BattleStats_ReconcileResourcesToEffectiveCapacity` `0030F5A0` (`0030F602` +1); `BattleStats_RecomputeDerivedStateAndAutoStatuses` `0030FED0` (`00310566`); +4 more |
| `+0x4E49C` | 4 | *(5 census row(s) removed 2026-09-13 as route-contaminated (§8); counts not regenerated)* | 4 / 8 | `WorldTransitionSnapshot_CaptureRuntimeState` `00229B40` (`00229C09`); `0030C470` (`0030C500` +1); `BattleFormula_ApplyTargetResult` `003112F0` (`003118BB`); +1 more | `WorldTransitionSnapshot_CaptureRuntimeState` `00229B40` (`00229BA6` +1); ~~`Battle_ProcessActionTarget` `00307300` (`00307642` +2)~~; +6 more |
| `+0x4E49E` | 2 |  | 1 / 1 | `BattleFormula_ApplyTargetResult` `003112F0` (`003118D9`) | `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` (`002FF265`) |
| `+0x4E4A0` | 2 |  | 2 / 2 | `0030C470` (`0030C507` +1); `BattleStats_AdvanceLevelToTargetAndRecomputeGrowth` `0030C650` (`0030C753` +1) | `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` (`002FF084` +1); `BattleStats_AdvanceLevelToTargetAndRecomputeGrowth` `0030C650` (`0030C735` +1) |
| `+0x4E4A2` | 2 |  | 0 / 1 |  | `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` (`002FF293`) |
| `+0x4E4A4` | 8 | *(17 census row(s) removed 2026-09-13 as route-contaminated (§8); counts not regenerated)* | 2 / 8 | `0030C470` (`0030C516` +1); `BattleStats_AdvanceLevelToTargetAndRecomputeGrowth` `0030C650` (`0030C760` +1) | ~~`Battle_ProcessActionTarget` `00307300` (`00307876` +6)~~; ~~`BattleUnit_SubmitResultReactionMode` `00328480` (`0032848F` +1)~~; +6 more |
| `+0x4E4A6` | 2 |  | 1 / 1 | `BattleFormula_ApplyTargetResult` `003112F0` (`003118F7`) | `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` (`002FF2C1`) |
| `+0x4E4A8` | 4 |  | 3 / 2 | `0030C470` (`0030C526` +1); `BattleFormula_ApplyTargetResult` `003112F0` (`00311915`); `BattleStats_AdvanceLevelToTargetAndRecomputeGrowth` `0030C650` (`0030C776` +1) | `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` (`002FF0CD` +1); `BattleStats_AdvanceLevelToTargetAndRecomputeGrowth` `0030C650` (`0030C76C` +1) |
| `+0x4E4AA` | 2 |  | 0 / 1 |  | `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` (`002FF2AA`) |
| `+0x4E4AC` | 16 |  | 3 / 5 | `WorldTransitionSnapshot_CaptureRuntimeState` `00229B40` (`00229C11`); `0030C470` (`0030C536` +2); `BattleStats_AdvanceLevelToTargetAndRecomputeGrowth` `0030C650` (`0030C78C`) | `WorldTransitionSnapshot_CaptureRuntimeState` `00229B40` (`00229BAE` +1); `GambitConfig_CopySelectedBankForStatsIndex` `00327C40` (`00327C91`); +3 more |
| `+0x4E4AE` | 2 |  | 0 / 1 |  | `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` (`002FF20F`) |
| `+0x4E4B0` | 4 |  | 2 / 4 | `0030C470` (`0030C546`); `BattleStats_AdvanceLevelToTargetAndRecomputeGrowth` `0030C650` (`0030C7A2`) | `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` (`002FF0B7` +1); `BattleStats_AdvanceLevelToTargetAndRecomputeGrowth` `0030C650` (`0030C798`); +2 more |
| `+0x4E4B2` | 2 |  | 0 / 1 |  | `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` (`002FF2D6`) |
| `+0x4E4B4` | 2 |  | 4 / 5 | `00239960` (`00239BF6`); `00328BD0` (`00328D4A`); `0030C470` (`0030C54F` +1); +1 more | `BattleStats_SetLicenseNodeStateAndApplySideEffects` `00323910` (`00323B64`); `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` (`002FF0AA` +1); +3 more |
| `+0x4E4B8` | 4 |  | 1 / 6 | `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` (`002FEFB9` +2) | `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` (`002FEFAB`); `BattleStats_ReconcileCurrentHpToEffectiveMaximum` `0030F340` (`0030F375` +1); +4 more |
| `+0x4E4BC` | 2 | *(1 census row(s) removed 2026-09-13 as route-contaminated (§8); counts not regenerated)* | 3 / 14 | `WorldTransitionSnapshot_CaptureRuntimeState` `00229B40` (`00229C19`); ~~`Battle_ProcessActionTarget` `00307300` (`00307798`)~~; `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` (`002FF824`) | `WorldTransitionSnapshot_CaptureRuntimeState` `00229B40` (`00229BB6` +1); `00239960` (`00239CD8`); +12 more |
| `+0x4E4BE` | 1 |  | 1 / 1 | `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` (`002FF840`) | `BattleFormula_ApplyTargetResult` `003112F0` (`003118AE`) |
| `+0x4E4BF` | 1 |  | 1 / 1 | `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` (`002FF85A`) | `BattleFormula_ApplyTargetResult` `003112F0` (`003118CC`) |
| `+0x4E4C0` | 0 | *(2 census row(s) removed 2026-09-13 as route-contaminated (§8); counts not regenerated)* | 2 / 3 | ~~`BattleUnit_DispatchActorPresentationEvent` `003299B0` (`003299C2` +1)~~; `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` (`002FEFBC` +1) | `003064F0` (`00306511`); `BattleAction_CheckUnitActionAvailability` `00306480` (`00306495`); +1 more |
| `+0x4E4C1` | 1 |  | 1 / 0 | `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` (`002FF88E`) |  |
| `+0x4E4C2` | 1 |  | 1 / 0 | `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` (`002FF8F2`) |  |
| `+0x4E4C3` | 1 |  | 1 / 3 | `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` (`002FF90C`) | `BattleFormula_ApplyTargetResult` `003112F0` (`003118EA`); `BattleStats_ReconcileResourcesToEffectiveCapacity` `0030F5A0` (`0030F62F` +1); +1 more |
| `+0x4E4C4` | 1 |  | 1 / 1 | `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` (`002FF921`) | `BattleFormula_ApplyTargetResult` `003112F0` (`00311908`) |
| `+0x4E4C5` | 1 |  | 1 / 0 | `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` (`002FF936`) |  |
| `+0x4E4C6` | 1 |  | 1 / 0 | `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` (`002FF949`) |  |
| `+0x4E4C7` | 1 |  | 1 / 0 | `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` (`002FF95B`) |  |
| `+0x4E4C8` | 4 |  | 1 / 3 | `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` (`002FEFC0` +1) | `DefinitionRuntime_ActivateAndApplyConfiguredSideEffects` `00316DF0` (`0031704B`); `BattleStats_ReconcileCurrentHpToEffectiveMaximum` `0030F340` (`0030F34E` +1); +1 more |
| `+0x4E4C9` | 1 |  | 1 / 0 | `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` (`002FF8B6`) |  |
| `+0x4E4CA` | 1 |  | 1 / 0 | `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` (`002FF8D2`) |  |
| `+0x4E4CB` | 1 |  | 2 / 5 | `00328BD0` (`00328D44`); `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` (`002FF89F`) | `BattleStats_ReconcileResourcesToEffectiveCapacity` `0030F5A0` (`0030F62F` +1); `BattleStats_RecomputeDerivedStateAndAutoStatuses` `0030FED0` (`0031054F` +1); +3 more |
| `+0x4E4CC` | 4 |  | 4 / 4 | `WorldTransitionSnapshot_CaptureRuntimeState` `00229B40` (`00229C21`); `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` (`002FF0D3` +1); `BattleStats_ChangeStatusAndProcessSideEffects` `0030E360` (`0030E564`); +1 more | `WorldTransitionSnapshot_CaptureRuntimeState` `00229B40` (`00229BBE` +1); `SaveTransition_PrepareRuntimeImageForCapture` `005844A0` (`0058454E`); +2 more |
| `+0x4E4CD` | 1 |  | 1 / 1 | `BattleStats_RecomputeDerivedStateAndAutoStatuses` `0030FED0` (`00310451`) | `BattleStats_RecomputeDerivedStateAndAutoStatuses` `0030FED0` (`0031048E`) |
| `+0x4E4CE` | 1 |  | 1 / 1 | `BattleStats_RecomputeDerivedStateAndAutoStatuses` `0030FED0` (`0031045F`) | `BattleStats_RecomputeDerivedStateAndAutoStatuses` `0030FED0` (`0031049C`) |
| `+0x4E4CF` | 1 |  | 1 / 1 | `BattleStats_RecomputeDerivedStateAndAutoStatuses` `0030FED0` (`0031046D`) | `BattleStats_RecomputeDerivedStateAndAutoStatuses` `0030FED0` (`003104AA`) |
| `+0x4E4D0` | 4 | record 0 `+0x3C` (status word) | 3 / 27 | `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` (`002FEFC4` +2); `BattleStats_ChangeStatusAndProcessSideEffects` `0030E360` (`0030E50E` +1); `BattleStats_RecomputeDerivedStateAndAutoStatuses` `0030FED0` (`0031047B`) | `002371B0` (`00237228`); `002372E0` (`00237368`); +25 more |
| `+0x4E4D4` | 4 |  | 3 / 4 | `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` (`002FF2FE` +1); `BattleStats_RecomputeDerivedStateAndAutoStatuses` `0030FED0` (`00310443` +1); `DefinitionRuntime_ActivateAndApplyConfiguredSideEffects` `00316DF0` (`00317066`) | `BattleStats_RecomputeDerivedStateAndAutoStatuses` `0030FED0` (`00310480` +2); `00329220` (`003294B5`); +2 more |
| `+0x4E4D5` | 1 |  | 2 / 2 | `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` (`002FF306` +1); `BattleStats_RecomputeDerivedStateAndAutoStatuses` `0030FED0` (`00310451`) | `BattleStats_RecomputeDerivedStateAndAutoStatuses` `0030FED0` (`0031048E`); `00329220` (`003294C7`) |
| `+0x4E4D6` | 1 |  | 2 / 2 | `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` (`002FF30E` +1); `BattleStats_RecomputeDerivedStateAndAutoStatuses` `0030FED0` (`0031045F`) | `BattleStats_RecomputeDerivedStateAndAutoStatuses` `0030FED0` (`0031049C`); `00329220` (`003294D2`) |
| `+0x4E4D7` | 1 |  | 2 / 2 | `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` (`002FF316` +1); `BattleStats_RecomputeDerivedStateAndAutoStatuses` `0030FED0` (`0031046D`) | `BattleStats_RecomputeDerivedStateAndAutoStatuses` `0030FED0` (`003104AA`); `00329220` (`003294DD`) |
| `+0x4E4D8` | 1 |  | 3 / 3 | `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` (`002FEFC8` +2); `BattleStats_RecomputeDerivedStateAndAutoStatuses` `0030FED0` (`0031047B` +1); `0030C470` (`0030C5CB` +1) | `BattleStats_RecomputeDerivedStateAndAutoStatuses` `0030FED0` (`003104B8` +1); `00329220` (`003294E8`); +1 more |
| `+0x4E4DC` | 4 |  | 4 / 12 | `WorldTransitionSnapshot_CaptureRuntimeState` `00229B40` (`00229C29`); `BattleStats_RecomputeDerivedStateAndAutoStatuses` `0030FED0` (`00310508`); `DefinitionRuntime_ActivateAndApplyConfiguredSideEffects` `00316DF0` (`00317066`); +1 more | `WorldTransitionSnapshot_CaptureRuntimeState` `00229B40` (`00229BC6` +1); `0050FD50` (`0050FD80`); +10 more |
| `+0x4E4DE` | 0 |  | 0 / 3 |  | `003202F0` (`0032035E`); `DefinitionRuntime_DeactivateAndRemoveConfiguredItems` `00323540` (`00323599`); +1 more |
| `+0x4E4E0` | 2 |  | 4 / 6 | `00239960` (`00239D7F`); `0030C470` (`0030C5CB` +1); `BattleStats_RecomputeDerivedStateAndAutoStatuses` `0030FED0` (`0031053D`); +1 more | `0050FE80` (`0050FEA4`); `BattleStats_ReconcileResourcesToEffectiveCapacity` `0030F5A0` (`0030F5CE`); +4 more |
| `+0x4E4E2` | 1 |  | 2 / 2 | `00328BD0` (`00328D47`); `0030E060` (`0030E111`) | `00329220` (`00329441`); `0030E060` (`0030E0A3`) |
| `+0x4E4E4` | 2 |  | 2 / 17 | `BattleStats_InitializeDefinitionRecord` `0023AC80` (`0023ACC2`); `Equipment_ReconcilePrimarySecondarySlotCompatibility` `00318B40` (`00318B8E` +1) | `Equipment_BuildRecommendedLoadoutForMappedStats` `002F9F20` (`002F9F8D`); `Equipment_EvaluateCandidateLoadoutAndBuildDerivedStats` `0030A4E0` (`0030A565` +2); +15 more |
| `+0x4E4E6` | 2 |  | 1 / 7 | `Equipment_ReconcilePrimarySecondarySlotCompatibility` `00318B40` (`00318C79`) | `Equipment_BuildRecommendedLoadoutForMappedStats` `002F9F20` (`002F9F94`); `Equipment_EvaluateCandidateLoadoutAndBuildDerivedStats` `0030A4E0` (`0030A585` +1); +5 more |
| `+0x4E4E8` | 2 |  | 0 / 3 |  | `Equipment_BuildRecommendedLoadoutForMappedStats` `002F9F20` (`002F9F9D`); `Equipment_EvaluateCandidateLoadoutAndBuildDerivedStats` `0030A4E0` (`0030A59A`); +1 more |
| `+0x4E4EA` | 2 |  | 0 / 3 |  | `Equipment_BuildRecommendedLoadoutForMappedStats` `002F9F20` (`002F9FA6`); `Equipment_EvaluateCandidateLoadoutAndBuildDerivedStats` `0030A4E0` (`0030A5A8`); +1 more |
| `+0x4E4EC` | 2 |  | 2 / 6 | `WorldTransitionSnapshot_CaptureRuntimeState` `00229B40` (`00229C31`); `BattleStats_InitializeDefinitionRecord` `0023AC80` (`0023ACD0`) | `WorldTransitionSnapshot_CaptureRuntimeState` `00229B40` (`00229BCE` +1); `Equipment_BuildRecommendedLoadoutForMappedStats` `002F9F20` (`002F9FAF`); +4 more |
| `+0x4E4EE` | 2 |  | 1 / 2 | `InventoryEquipment_SnapshotAndClearTemporaryState` `0030FBE0` (`0030FC24`) | `BattleStats_SetEquipmentSlotsByMappedId` `0031A710` (`0031A750`); `00329220` (`00329738`) |
| `+0x4E4F0` | 4 | *(1 census row(s) removed 2026-09-13 as route-contaminated (§8); counts not regenerated)* | 1 / 4 | ~~`BattleUnit_DispatchActorPresentationEvent` `003299B0` (`003299EE`)~~ | `BattleStats_SetEquipmentSlotsByMappedId` `0031A710` (`0031A763`); `DefinitionRuntime_ActivateAndApplyConfiguredSideEffects` `00316DF0` (`00317048`); +2 more |
| `+0x4E4F5` | 1 |  | 0 / 1 |  | `003202F0` (`00320364`) |
| `+0x4E4F6` | 2 |  | 1 / 0 | `InventoryEquipment_SnapshotAndClearTemporaryState` `0030FBE0` (`0030FC29`) |  |
| `+0x4E4F8` | 4 | record 0 `+0x64` (status word) | 1 / 28 | `BattleStats_ChangeStatusAndProcessSideEffects` `0030E360` (`0030E4F8` +1) | `002371B0` (`00237225`); `002372E0` (`00237365`); +26 more |
| `+0x4E4FC` | 1 |  | 3 / 4 | `WorldTransitionSnapshot_CaptureRuntimeState` `00229B40` (`00229C39`); `00328BD0` (`00328D30`); `BattleStats_ModifyStatusLayerStateAndProcessSideEffects` `0030E130` (`0030E24E`) | `WorldTransitionSnapshot_CaptureRuntimeState` `00229B40` (`00229BD6` +1); `SaveTransition_PrepareRuntimeImageForCapture` `005844A0` (`00584566`); +2 more |
| `+0x4E4FD` | 1 |  | 0 / 1 |  | `00329220` (`0032948E`) |
| `+0x4E4FE` | 1 |  | 0 / 1 |  | `00329220` (`00329499`) |
| `+0x4E4FF` | 1 |  | 0 / 1 |  | `00329220` (`003294A4`) |
| `+0x4E500` | 1 |  | 0 / 9 |  | `00239960` (`00239CC4`); `0050FE20` (`0050FE44`); +7 more |
| `+0x4E504` | 1 |  | 0 / 1 |  | `BattleStats_RecomputeDerivedStateAndAutoStatuses` `0030FED0` (`00310303` +2) |
| `+0x4E505` | 1 |  | 0 / 2 |  | `003202F0` (`0032036A`); `BattleStats_RecomputeDerivedStateAndAutoStatuses` `0030FED0` (`00310319`) |
| `+0x4E508` | 1 |  | 0 / 3 |  | `0030C470` (`0030C5C1` +1); `BattleStats_ReconcileResourcesToEffectiveCapacity` `0030F5A0` (`0030F5C0` +3); +1 more |
| `+0x4E50C` | 1 |  | 2 / 6 | `00328BD0` (`00328D34`); `BattleStats_ModifyStatusLayerStateAndProcessSideEffects` `0030E130` (`0030E212` +1) | `WorldTransitionSnapshot_CaptureRuntimeState` `00229B40` (`00229B9B` +2); `00328BD0` (`00328D23` +1); +4 more |
| `+0x4E50D` | 0 |  | 0 / 3 |  | `00328BD0` (`00328D37`); `BattleStats_RecomputeDerivedStateAndAutoStatuses` `0030FED0` (`00310319`); +1 more |
| `+0x4E50E` | 1 |  | 0 / 1 |  | `00329220` (`00329495`) |
| `+0x4E50F` | 1 |  | 0 / 1 |  | `00329220` (`003294A0`) |
| `+0x4E510` | 1 |  | 0 / 9 |  | `00239960` (`00239CCE`); `0050FE20` (`0050FE4A`); +7 more |
| `+0x4E514` | 0 |  | 1 / 1 | `0030C470` (`0030C4B1`) | `DefinitionRuntime_ActivateAndApplyConfiguredSideEffects` `00316DF0` (`00316EC3` +1) |
| `+0x4E516` | 2 |  | 0 / 1 |  | `DefinitionRuntime_ActivateAndApplyConfiguredSideEffects` `00316DF0` (`00316F4A`) |
| `+0x4E51C` | 16 |  | 2 / 4 | `0030C470` (`0030C4B1`); `GambitConfig_LoadAuthoredPresetAndRebuildRuntimeOrders` `00327CB0` (`00327D57`) | `GambitConfig_CopyBasePairSetForStatsIndex` `00327BE0` (`00327BFF`); `GambitConfig_InitializeThreeBanksFromBasePairs` `00326030` (`00326057` +2); +2 more |
| `+0x4E51E` | 2 |  | 1 / 1 | `GambitConfig_LoadAuthoredPresetAndRebuildRuntimeOrders` `00327CB0` (`00327D64`) | `DefinitionRuntime_ActivateAndApplyConfiguredSideEffects` `00316DF0` (`00316F4A`) |
| `+0x4E52C` | 16 |  | 0 / 2 |  | `GambitConfig_CopyBasePairSetForStatsIndex` `00327BE0` (`00327C0A`); `GambitConfig_InitializeThreeBanksFromBasePairs` `00326030` (`00326070` +2) |
| `+0x4E53C` | 16 |  | 0 / 2 |  | `GambitConfig_CopyBasePairSetForStatsIndex` `00327BE0` (`00327C16`); `GambitConfig_InitializeThreeBanksFromBasePairs` `00326030` (`0032607F` +2) |
| `+0x4E544` | 0 |  | 0 / 1 |  | `DefinitionRuntime_ActivateAndApplyConfiguredSideEffects` `00316DF0` (`00316EE9` +1) |
| `+0x4E546` | 1 |  | 0 / 1 |  | `DefinitionRuntime_ActivateAndApplyConfiguredSideEffects` `00316DF0` (`00316ECF` +2) |
| `+0x4E54C` | 2 |  | 1 / 4 | `GambitConfig_LoadAuthoredPresetAndRebuildRuntimeOrders` `00327CB0` (`00327D78` +1) | `GambitConfig_CopyBasePairSetForStatsIndex` `00327BE0` (`00327C22`); `GambitConfig_LoadAuthoredPresetAndRebuildRuntimeOrders` `00327CB0` (`00327D6C` +1); +2 more |
| `+0x4E54E` | 1 |  | 2 / 2 | `00328BD0` (`00328CF5`); `GambitConfig_LoadAuthoredPresetAndRebuildRuntimeOrders` `00327CB0` (`00327D84`) | `00328BD0` (`00328CE2`); `DefinitionRuntime_ActivateAndApplyConfiguredSideEffects` `00316DF0` (`00316ECF` +2) |
| `+0x4E550` | 4 |  | 1 / 1 | `BattleStats_ChangeStatusAndProcessSideEffects` `0030E360` (`0030E594`) | `00329220` (`00329524`) |
| `+0x4E564` | 16 | *(2 census row(s) removed 2026-09-13 as route-contaminated (§8); counts not regenerated; **no census access remains at this offset**)* | 2 / 0 | ~~`Battle_ProcessActionTarget` `00307300` (`003079C3`)~~; ~~`00311F70` (`00312062`)~~ |  |
| `+0x4E574` | 16 | *(4 census row(s) removed 2026-09-13 as route-contaminated (§8); counts not regenerated; **no census access remains at this offset**)* | 2 / 1 | ~~`Battle_ProcessActionTarget` `00307300` (`003079CA`)~~; ~~`00311F70` (`00312069`)~~ | ~~`BattleAction_ApplyKnockbackImpulse` `00323350` (`003233D5` +1)~~ |
| `+0x4E57C` | 4 | *(2 census row(s) removed 2026-09-13 as route-contaminated (§8); counts not regenerated; **no census access remains at this offset**)* | 0 / 1 |  | ~~`BattleAction_ApplyKnockbackImpulse` `00323350` (`003233EA` +1)~~ |
| `+0x4E5D0` | 2 |  | 1 / 0 | `BattleStats_ChangeStatusAndProcessSideEffects` `0030E360` (`0030E5AF`) |  |
| `+0x4E5F0` | 4 | *(2 census row(s) removed 2026-09-13 as route-contaminated (§8); counts not regenerated; **no census access remains at this offset**)* | 2 / 0 | ~~`Battle_ProcessActionTarget` `00307300` (`00307A03`)~~; ~~`00311F70` (`003120A7`)~~ |  |
| `+0x4E5F4` | 4 | *(4 census row(s) removed 2026-09-13 as route-contaminated (§8); counts not regenerated; **no census access remains at this offset**)* | 2 / 1 | ~~`Battle_ProcessActionTarget` `00307300` (`00307A0B`)~~; ~~`00311F70` (`003120AF`)~~ | ~~`BattleAction_ApplyKnockbackImpulse` `00323350` (`0032346F` +1)~~ |
| `+0x4E610` | 2 |  | 2 / 0 | `BattleFormula_ApplyTargetResult` `003112F0` (`00311824`); `BattleStats_UpdateStatusAuxiliaryValue` `0030EA40` (`0030EAB9`) |  |
| `+0x4E612` | 2 |  | 1 / 0 | `BattleFormula_ApplyTargetResult` `003112F0` (`00311834`) |  |
| `+0x4E614` | 2 |  | 1 / 0 | `BattleFormula_ApplyTargetResult` `003112F0` (`00311844`) |  |
| `+0x4E616` | 2 |  | 1 / 0 | `BattleFormula_ApplyTargetResult` `003112F0` (`00311854`) |  |
| `+0x4E618` | 2 |  | 2 / 0 | `BattleFormula_ApplyTargetResult` `003112F0` (`00311864`); `0030C470` (`0030C586`) |  |
| `+0x4E61A` | 2 |  | 1 / 0 | `BattleFormula_ApplyTargetResult` `003112F0` (`00311874`) |  |
| `+0x4E61C` | 2 |  | 1 / 0 | `BattleFormula_ApplyTargetResult` `003112F0` (`00311884`) |  |
| `+0x4E61E` | 2 |  | 1 / 0 | `BattleFormula_ApplyTargetResult` `003112F0` (`00311894`) |  |
| `+0x4E620` | 4 |  | 1 / 1 | `0030C470` (`0030C586`) | `00329220` (`003296B9`) |
| `+0x4E624` | 4 |  | 4 / 5 | `00239960` (`00239C05`); `00323790` (`0032379C` +1); `BattleStats_SetLicenseNodeStateAndApplySideEffects` `00323910` (`003239E1`); +1 more | `00323790` (`00323790`); `BattleStats_SetLicenseNodeStateAndApplySideEffects` `00323910` (`003239C7`); +3 more |
| `+0x4E628` | 8 |  | 1 / 0 | `00239960` (`00239C0D`) |  |
| `+0x4E630` | 8 |  | 1 / 0 | `00239960` (`00239C17`) |  |
| `+0x4E638` | 8 |  | 1 / 0 | `00239960` (`00239C1E`) |  |
| `+0x4E640` | 8 |  | 1 / 0 | `00239960` (`00239C25`) |  |
| `+0x4E648` | 8 |  | 1 / 0 | `00239960` (`00239C2C`) |  |
| `+0x4E64E` | 1 |  | 2 / 1 | `0030C470` (`0030C496`); `BattleStats_AdvanceLevelToTargetAndRecomputeGrowth` `0030C650` (`0030C7BB`) | `BattleStats_AdvanceLevelToTargetAndRecomputeGrowth` `0030C650` (`0030C66F` +5) |
| `+0x4E650` | 4 |  | 1 / 0 | `00239960` (`00239C33`) |  |
| `+0x4E654` | 2 |  | 1 / 0 | `00239960` (`00239C39`) |  |
| `+0x4E656` | 1 |  | 2 / 6 | `0030C470` (`0030C496`); `BattleStats_AdvanceLevelToTargetAndRecomputeGrowth` `0030C650` (`0030C7BB`) | `0030C620` (`0030C63F`); `00317480` (`00317580` +2); +4 more |
| `+0x4E657` | 1 |  | 3 / 9 | `BattleStats_SetLicenseBoardSelectorAAndActive` `00323740` (`00323772`); `00328BD0` (`00328D52`); `BattleStats_InitializeDefinitionRecord` `0023AC80` (`0023ACD5`) | `00293310` (`0029379D`); `00293FE0` (`002943D6`); +7 more |
| `+0x4E658` | 1 |  | 1 / 9 | `BattleStats_SetLicenseBoardSelectorBAndActive` `003236F0` (`00323722`) | `00293310` (`002937B0`); `00293FE0` (`002943EA`); +7 more |
| `+0x4E659` | 1 |  | 5 / 2 | `BattleStats_SetLicenseBoardSelectorBAndActive` `003236F0` (`00323729`); `BattleStats_SetLicenseBoardSelectorAAndActive` `00323740` (`00323779`); `BattleStats_ReconcileActiveLicenseBoardSelector` `003242F0` (`00324341` +1); +2 more | `BattleStats_GetActiveLicenseBoardSelector` `003236B0` (`003236DB`); `BattleStats_ReconcileActiveLicenseBoardSelector` `003242F0` (`00324336`) |
| `+0x4EB2C` | 8 | *(31 census row(s) removed 2026-09-13 as route-contaminated (§8); counts not regenerated; **no census access remains at this offset**)* | 0 / 11 |  | ~~`Battle_ProcessActionTarget` `00307300` (`00307568` +10)~~; ~~`00311F70` (`00312079` +1)~~; +9 more |
| `+0x4EB34` | 8 | *(10 census row(s) removed 2026-09-13 as route-contaminated (§8); counts not regenerated; **no census access remains at this offset**)* | 0 / 5 |  | ~~`Battle_ProcessActionTarget` `00307300` (`003079E8` +2)~~; ~~`00311F70` (`0031208B` +1)~~; +3 more |
| `+0x4F334` | 4 | *(1 census row(s) removed 2026-09-13 as route-contaminated (§8); counts not regenerated; **no census access remains at this offset**)* | 1 / 0 | ~~`Battle_ProcessActionTarget` `00307300` (`00307511`)~~ |  |
| `+0x512E9` | 1 |  | 0 / 1 |  | `003202F0` (`00320319`) |
| `+0x51334` | 2 |  | 0 / 1 |  | `003202F0` (`0032034B`) |
| `+0x51336` | 2 |  | 0 / 1 |  | `003202F0` (`0032035E`) |
| `+0x5134D` | 1 |  | 0 / 1 |  | `003202F0` (`00320364`) |
| `+0x5135D` | 1 |  | 0 / 1 |  | `003202F0` (`0032036A`) |
| `+0x52BD4` | 2 |  | 0 / 1 |  | `InventoryEquipment_SnapshotAndClearTemporaryState` `0030FBE0` (`0030FC67`) |
| `+0x52C54` | 2 |  | 0 / 1 |  | `InventoryEquipment_SnapshotAndClearTemporaryState` `0030FBE0` (`0030FCC7`) |
| `+0x53410` | 2 |  | 1 / 1 | `InventoryEquipment_SnapshotAndClearTemporaryState` `0030FBE0` (`0030FC6F`) | `InventoryEquipment_RestoreTemporarySnapshotAndClearBackup` `0030FAA0` (`0030FAE7`) |
| `+0x53490` | 2 |  | 1 / 1 | `InventoryEquipment_SnapshotAndClearTemporaryState` `0030FBE0` (`0030FCCF`) | `InventoryEquipment_RestoreTemporarySnapshotAndClearBackup` `0030FAA0` (`0030FB37`) |
| `+0x53C54` | 0 | inventory class descriptors, rebased on load (`0030B6A0`) | 1 / 1 | `InventoryRuntime_RebaseClassDescriptorsAndClearDerivedState` `0030B6A0` (`0030B710`) | `InventoryRuntime_RebaseClassDescriptorsAndClearDerivedState` `0030B6A0` (`0030B702`) |
| `+0x53C5C` | 8 |  | 1 / 0 | `InventoryRuntime_RebaseClassDescriptorsAndClearDerivedState` `0030B6A0` (`0030B713`) |  |
| `+0x53C64` | 8 |  | 1 / 0 | `InventoryRuntime_RebaseClassDescriptorsAndClearDerivedState` `0030B6A0` (`0030B717`) |  |
| `+0x53C6C` | 8 |  | 1 / 0 | `InventoryRuntime_RebaseClassDescriptorsAndClearDerivedState` `0030B6A0` (`0030B71F`) |  |
| `+0x53C74` | 8 |  | 1 / 0 | `InventoryRuntime_RebaseClassDescriptorsAndClearDerivedState` `0030B6A0` (`0030B723`) |  |
| `+0x53C7C` | 8 |  | 1 / 0 | `InventoryRuntime_RebaseClassDescriptorsAndClearDerivedState` `0030B6A0` (`0030B727`) |  |
| `+0x53C84` | 8 |  | 1 / 0 | `InventoryRuntime_RebaseClassDescriptorsAndClearDerivedState` `0030B6A0` (`0030B72B`) |  |
| `+0x53C8C` | 8 |  | 1 / 0 | `InventoryRuntime_RebaseClassDescriptorsAndClearDerivedState` `0030B6A0` (`0030B72F`) |  |
| `+0x53C94` | 0 |  | 0 / 1 |  | `InventoryRuntime_RebaseClassDescriptorsAndClearDerivedState` `0030B6A0` (`0030B71B`) |
| `+0x53E54` | 1 | the bazaar goods' flag bytes (block `+0x59C8`, 128 B: unlocked once / available now; [the bazaar page](../../12-Items-Equipment-Shops-License/the-bazaar-recipe-unlock-and-purchase.md) §2.2, §7 on the rebind mask) | 3 / 3 | `BattleIdClassD_ResetPurchasedEntryAndNestedPrerequisiteState` `0030B180` (`0030B203`); `BattleIdClassD_RefreshPrerequisiteRuntimeFlags` `0030B270` (`0030B461`); `InventoryRuntime_RebaseClassDescriptorsAndClearDerivedState` `0030B6A0` (`0030B750`) | `BattleIdClassD_RefreshPrerequisiteRuntimeFlags` `0030B270` (`0030B345` +1); `0031C5D0` (`0031DA69` +2); +1 more |
| `+0x53E55` | 0 |  | 0 / 1 |  | `InventoryRuntime_RebaseClassDescriptorsAndClearDerivedState` `0030B6A0` (`0030B753`) |
| `+0x53ED4` | 1 |  | 1 / 18 | `PartyConfiguration_SetDefinitionSelectorForIndex` `00329080` (`00329122` +1) | `0030A970` (`0030A994`); `PartyConfiguration_AddSelector07To25ToAvailablePrimaryIndex` `003170E0` (`00317100`); +16 more |
| `+0x53ED6` | 2 |  | 0 / 1 |  | `0030A970` (`0030A9A7`) |
| `+0x53ED8` | 2 |  | 0 / 1 |  | `0030A970` (`0030A9B8`) |
| `+0x53EDA` | 2 |  | 0 / 1 |  | `0030A970` (`0030A9C7`) |
| `+0x53EE4` | 2 |  | 0 / 9 |  | `PartyConfiguration_AddSelector00To06ToAvailableIndex4To8` `003172E0` (`00317352`); `PartyConfiguration_SetEmptyIndexSelector` `00326110` (`00326138`); +7 more |
| `+0x53EE6` | 1 |  | 2 / 8 | `BattleGroup_RefreshFourActorDefinitions` `003266C0` (`00326717` +5); `BattleSlotMap_InitializeMappingClasses` `00329CC0` (`00329DF6`) | `BattleUnit_FindMappedDefinitionSelectorByIndex` `0031B810` (`0031B841`); `BattleSlotMap_ResolveMappedBattleSlot` `0031B9F0` (`0031BA8B`); +6 more |
| `+0x53EE8` | 2 |  | 1 / 0 | `BattleGroup_RefreshFourActorDefinitions` `003266C0` (`003268BD`) |  |
| `+0x53EEC` | 2 |  | 1 / 0 | `BattleGroup_RefreshFourActorDefinitions` `003266C0` (`003269A7` +1) |  |
| `+0x53EEE` | 8 |  | 1 / 0 | `BattleGroup_RefreshFourActorDefinitions` `003266C0` (`00326728`) |  |
| `+0x53EF6` | 2 |  | 2 / 1 | `BattleGroup_RefreshFourActorDefinitions` `003266C0` (`0032671B` +1); `BattleSlotMap_InitializeMappingClasses` `00329CC0` (`00329DFD`) | `BattleGroup_RefreshFourActorDefinitions` `003266C0` (`00326739`) |
| `+0x53EF8` | 2 |  | 2 / 2 | `BattleGroup_RefreshFourActorDefinitions` `003266C0` (`0032673E` +5); `BattleSlotMap_InitializeMappingClasses` `00329CC0` (`00329E04`) | `BattleSlotMap_ResolveMappedBattleSlot` `0031B9F0` (`0031BA71`); `BattleGroup_RefreshFourActorDefinitions` `003266C0` (`00326705`) |
| `+0x53EFA` | 2 |  | 1 / 0 | `BattleGroup_RefreshFourActorDefinitions` `003266C0` (`003268CD`) |  |
| `+0x53EFE` | 2 |  | 1 / 0 | `BattleGroup_RefreshFourActorDefinitions` `003266C0` (`003269AB` +1) |  |
| `+0x53F08` | 2 |  | 2 / 0 | `BattleGroup_RefreshFourActorDefinitions` `003266C0` (`00326742`); `BattleSlotMap_InitializeMappingClasses` `00329CC0` (`00329E0B`) |  |
| `+0x53F0A` | 1 |  | 2 / 4 | `BattleGroup_RefreshFourActorDefinitions` `003266C0` (`00326720`); `BattleSlotMap_InitializeMappingClasses` `00329CC0` (`00329E12`) | `BattleStats_SetEquipmentSlotByMappedId` `0031A510` (`0031A554`); `BattleSlotMap_ResolveMappedBattleSlot` `0031B9F0` (`0031BA57`); +2 more |
| `+0x53F1A` | 2 |  | 2 / 0 | `BattleGroup_RefreshFourActorDefinitions` `003266C0` (`00326724`); `BattleSlotMap_InitializeMappingClasses` `00329CC0` (`00329E19`) |  |
| `+0x53F1C` | 1 |  | 2 / 7 | `BattleGroup_RefreshFourActorDefinitions` `003266C0` (`00326747` +4); `BattleSlotMap_InitializeMappingClasses` `00329CC0` (`00329E20`) | `0031B950` (`0031B981`); `BattleSlotMap_ResolveMappedBattleSlot` `0031B9F0` (`0031BA3D`); +5 more |
| `+0x53F1E` | 2 |  | 1 / 0 | `BattleGroup_RefreshFourActorDefinitions` `003266C0` (`003268DC`) |  |
| `+0x53F22` | 2 |  | 1 / 0 | `BattleGroup_RefreshFourActorDefinitions` `003266C0` (`003269B0` +1) |  |
| `+0x53F2C` | 2 |  | 2 / 1 | `BattleGroup_RefreshFourActorDefinitions` `003266C0` (`0032674B` +2); `BattleSlotMap_InitializeMappingClasses` `00329CC0` (`00329E27`) | `BattleGroup_RefreshFourActorDefinitions` `003266C0` (`00326700`) |
| `+0x53F30` | 1 |  | 6 / 10 | `003220E0` (`00322173`); `00326620` (`003266A3`); `00327810` (`00327836` +1); +3 more | `PartyConfiguration_ReconcileRosterFromCurrentSelectors` `003261D0` (`0032620A`); `PartyFocus_SelectAndRequestDefaultActor` `00326500` (`00326542` +1); +8 more |
| `+0x53F54` | 4 |  | 4 / 2 | `002370C0` (`0023712E`); `00317230` (`0031726B` +2); `00322200` (`00322216`); +1 more | `00317230` (`00317243` +1); `00320D50` (`00320D57`) |
| `+0x53F58` | 4 |  | 4 / 2 | `002370C0` (`00237121`); `00317230` (`0031727C` +1); `00322200` (`00322209`); +1 more | `00317230` (`0031724F` +1); `00320D50` (`00320D5F`) |
| `+0x53F5C` | 2 |  | 7 / 6 | `SaveTransitionMetadata_RestoreFromRecord` `002EF410` (`002EF44C` +1); `BattleUnit_IssueCommand` `00311CF0` (`00311D5E`); `00313600` (`00313638`); +4 more | `SaveTransitionMetadata_CaptureToRecord` `002EF3C0` (`002EF3E5` +1); `SaveTransitionMetadata_RefreshSubsetToRecord` `002EF510` (`002EF517`); +4 more |
| `+0x53F60` | 1 |  | 3 / 2 | `BattleAction_UpdateSpecialPresentationSequence` `00306760` (`0030697F`); `00313840` (`0031387D`); `003139C0` (`003139C7`) | `BattleAction_UpdateSpecialPresentationSequence` `00306760` (`003067EC` +1); `003137E0` (`003137E7`) |
| `+0x53F61` | 1 |  | 2 / 7 | `BattleAction_UpdateSpecialPresentationSequence` `00306760` (`00306966`); `00313840` (`0031386A`) | `00300FC0` (`0030110B`); `0030A970` (`0030A9D7`); +5 more |
| `+0x53F64` | 4 |  | 3 / 3 | `BattleAction_UpdateSpecialPresentationSequence` `00306760` (`003069A8`); `00313760` (`0031378A` +1); `00313840` (`003138AE`) | `AiOrder_EvaluateTargetSelector` `00301AD0` (`00303543`); `00313600` (`00313616`); +1 more |
| `+0x53F68` | 4 |  | 2 / 2 | `BattleAction_UpdateSpecialPresentationSequence` `00306760` (`003069B7`); `00313840` (`003138BB`) | `00313760` (`00313784`); `00313830` (`00313837`) |
| `+0x53F6C` | 4 |  | 9 / 11 | `SaveTransitionMetadata_RestoreFromRecord` `002EF410` (`002EF424` +1); `00303D90` (`00303DC6` +1); `00303F00` (`00303FDD` +2); +6 more | `SaveTransitionMetadata_CaptureToRecord` `002EF3C0` (`002EF3D3` +1); `00303D90` (`00303E03` +2); +9 more |
| `+0x53F70` | 4 |  | 4 / 2 | `00303D90` (`00303DD4`); `00304440` (`00304468` +1); `00304680` (`00304734`); +1 more | `00304060` (`003040CE`); `00304660` (`00304667`) |
| `+0x53F74` | 4 |  | 3 / 2 | `00303F00` (`00303FB6`); `00304440` (`0030449E`); `00304680` (`00304741`) | `00304060` (`003040F3`); `00304670` (`00304677`) |
| `+0x53F78` | 4 |  | 4 / 0 | `00303D90` (`00303E37`); `00303F00` (`00303F59`); `00304440` (`00304546`); +1 more |  |
| `+0x53F8C` | 4 | battle-state block `+0x5B00` (`00233C9E`) | 2 / 1 | `00233C10` (`00233C9E`); `BattleFormula_ApplyResultMetadata` `00385BA0` (`00385BEA` +1) | `0038EBE0` (`0038EC70`) |
| `+0x53F90` | 4 |  | 10 / 14 | `SaveTransitionMetadata_RestoreFromRecord` `002EF410` (`002EF435` +5); `00303D90` (`00303DB8` +1); `BattleAction_UpdateSpecialPresentationSequence` `00306760` (`00306949` +2); +7 more | `SaveTransitionMetadata_CaptureToRecord` `002EF3C0` (`002EF3F7` +1); `00303D90` (`00303D9B`); +12 more |
| `+0x53F94` | 4 |  | 2 / 1 | `0030D8B0` (`0030D97C`); `0030DA10` (`0030DA26`) | `0030D8B0` (`0030D8DB`) |
| `+0x53F98` | 2 | block `+0x5B0C` | 4 / 2 | `00233C10` (`00233C83`); `002FA210` (`002FA219`); `0038D970` (`0038D9F2`); +1 more | `0038D970` (`0038D9DE`); `0038DA00` (`0038DA56`) |
| `+0x53F9A` | 1 | block `+0x5B0E` | 3 / 2 | `00233C10` (`00233C91`); `002FA210` (`002FA227`); `BattleFormula_ApplyResultMetadata` `00385BA0` (`00385BD1` +1) | `00389C60` (`00389CC4`); `0038EAF0` (`0038EB03`) |
| `+0x53F9C` | 2 |  | 3 / 5 | `00235AF0` (`00235BCC` +1); `GambitConfig_CommitBankAndRebuildRuntimeOrders` `003282D0` (`0032832E`); `GambitConfig_InitializeThreeBanksFromBasePairs` `00326030` (`00326069`) | `00235AF0` (`00235D17`); `GambitRuntime_RebuildOrderSetForStatsRecord` `00327DE0` (`00327E2F` +3); +3 more |
| `+0x53F9E` | 2 |  | 1 / 4 | `00235AF0` (`00235CEC`) | `00235AF0` (`00235B39`); `GambitRuntime_RebuildOrderSetForStatsRecord` `00327DE0` (`00327E6E` +1); +2 more |
| `+0x53FAC` | 16 |  | 3 / 0 | `00235AF0` (`00235BDB`); `GambitConfig_CommitBankAndRebuildRuntimeOrders` `003282D0` (`00328336`); `GambitConfig_InitializeThreeBanksFromBasePairs` `00326030` (`00326078`) |  |
| `+0x53FBC` | 16 |  | 3 / 0 | `00235AF0` (`00235BEA`); `GambitConfig_CommitBankAndRebuildRuntimeOrders` `003282D0` (`0032833F`); `GambitConfig_InitializeThreeBanksFromBasePairs` `00326030` (`00326087`) |  |
| `+0x53FCC` | 2 |  | 3 / 4 | `00235AF0` (`00235BF8` +2); `GambitConfig_CommitBankAndRebuildRuntimeOrders` `003282D0` (`00328347`); `GambitConfig_InitializeThreeBanksFromBasePairs` `00326030` (`00326095`) | `00235AF0` (`00235CF5` +1); `GambitRuntime_RebuildOrderSetForStatsRecord` `00327DE0` (`00327E51` +5); +2 more |
| `+0x53FCE` | 1 |  | 2 / 2 | `00235AF0` (`00235D0F`); `GambitConfig_AdjustAvailableEntryCountByStatsRecord` `003279B0` (`00327A01` +1) | `00235AF0` (`00235B29`); `GambitConfig_AdjustAvailableEntryCountByStatsRecord` `003279B0` (`003279E7` +1) |
| `+0x53FD0` | 16 |  | 1 / 0 | `GambitConfig_InitializeThreeBanksFromBasePairs` `00326030` (`003260A3`) |  |
| `+0x53FE0` | 16 |  | 1 / 0 | `GambitConfig_InitializeThreeBanksFromBasePairs` `00326030` (`003260B2`) |  |
| `+0x53FF0` | 16 |  | 1 / 0 | `GambitConfig_InitializeThreeBanksFromBasePairs` `00326030` (`003260C1`) |  |
| `+0x54000` | 4 |  | 1 / 0 | `GambitConfig_InitializeThreeBanksFromBasePairs` `00326030` (`003260CF`) |  |
| `+0x54004` | 16 |  | 1 / 0 | `GambitConfig_InitializeThreeBanksFromBasePairs` `00326030` (`003260DD`) |  |
| `+0x54014` | 16 |  | 1 / 0 | `GambitConfig_InitializeThreeBanksFromBasePairs` `00326030` (`003260EC`) |  |
| `+0x54024` | 16 |  | 1 / 0 | `GambitConfig_InitializeThreeBanksFromBasePairs` `00326030` (`003260FB`) |  |
| `+0x54034` | 4 |  | 1 / 0 | `GambitConfig_InitializeThreeBanksFromBasePairs` `00326030` (`00326109`) |  |
| `+0x557FC` | 4 |  | 1 / 16 | `GambitConfig_InitializeThreeBanksFromBasePairs` `00326030` (`00326039`) | `GambitConfig_CopySelectedBankForStatsIndex` `00327C40` (`00327C63`); `GambitRuntime_RebuildOrderSetForStatsRecord` `00327DE0` (`00327E27` +1); +14 more |

### 2.4 What nobody reaches

43 ranges totalling 54,569 bytes have no access on any enumerated route once the named
regions (the two SpawnKeep images, the two group banks, the entry table, the snapshot and its mirror,
the flag banks) are counted as covered. The ones of 4 KB or more: `+0x2081`–`+0x7B11` (23,185 B) *(2026-09-26: covered by the battle-state copy, §2.2; `FG-2`)*; `+0xC7F0`–`+0xDFFF` (6,160 B); `+0x54038`–`+0x557FB` (6,084 B). Under the scan's
limits these are where indexed tables and unseeded objects live, not evidence of unused space.

### 2.5 The header, offset by offset

512 bytes before the payload. The 16-byte rows are block copies (`WorldTransitionSnapshot_CaptureRuntimeState`,
`SaveWrite_PrepareAndSubmitFullImage`, `SaveUI_RestoreActiveHeaderFromControllerBackup`); the
finalizer `SaveImage_FinalizeHeaderAndChecksum` (`00583D60`) writes `+0x21`–`+0x23`, `+0x3C`–`+0x4C`,
`+0x54`, `+0x57`; `SaveLoad_NormalizeLoadedRuntimeStateAndReseedRNG` (`00584210`) rewrites
`+0x0C`, `+0x18`–`+0x1B`, `+0x78`–`+0x8C` on load; `SaveRuntime_InitializeHeaderAndImageBackedState`
(`00253A80`) writes `+0x58`–`+0x6C` at init.

| offset | width | name | w / r | writers | readers |
|---|---|---|---|---|---|
| `+0x0000` | 16 | (16-byte block copies begin) | 5 / 7 | `WorldTransitionSnapshot_CaptureRuntimeState` `00229B40` (`00229C61`); `SaveWrite_PrepareAndSubmitFullImage` `0057E310` (`0057E361` +1); `SaveSlotTransaction_StateMachine` `00581DA0` (`00581E0E` +1); +2 more | `WorldTransitionSnapshot_CaptureRuntimeState` `00229B40` (`00229C4B` +1); `003F4AA0` (`003F4AD9`); +5 more |
| `+0x0004` | 4 |  | 2 / 0 | `SaveWrite_PrepareAndSubmitFullImage` `0057E310` (`0057E3C7`); `SaveSlotTransaction_StateMachine` `00581DA0` (`00581FBA`) |  |
| `+0x0008` | 4 |  | 1 / 5 | `GameState_SetGil` `00254EE0` (`00254F1F`) | `GameState_GetGil` `00253690` (`00253697`); `GameState_SetGil` `00254EE0` (`00254EF1`); +3 more |
| `+0x0009` | 0 |  | 0 / 1 |  | `CRC32_Compute` `003BB220` (`003BB234`) |
| `+0x000C` | 4 |  | 2 / 2 | `00254E80` (`00254E90`); `SaveLoad_NormalizeLoadedRuntimeStateAndReseedRNG` `00584210` (`005842DC` +1) | `002536D0` (`002536DC`); `002CF940` (`002CFA9B`) |
| `+0x0010` | 16 |  | 6 / 6 | `WorldTransitionSnapshot_CaptureRuntimeState` `00229B40` (`00229C69`); `00254CC0` (`00254CF8` +1); `00394130` (`003942B9`); +3 more | `WorldTransitionSnapshot_CaptureRuntimeState` `00229B40` (`00229C65`); `00254CC0` (`00254D27`); +4 more |
| `+0x0018` | 2 |  | 3 / 5 | `00254CC0` (`00254DBF`); `00394130` (`003942BD`); `SaveLoad_NormalizeLoadedRuntimeStateAndReseedRNG` `00584210` (`005842CF` +1) | `002536B0` (`002536B7`); `00254C90` (`00254C97`); +3 more |
| `+0x001A` | 1 |  | 2 / 5 | `00254CC0` (`00254D9E`); `SaveLoad_NormalizeLoadedRuntimeStateAndReseedRNG` `00584210` (`0058430D`) | `002536B0` (`002536BE`); `00254C90` (`00254C9E`); +3 more |
| `+0x001B` | 1 |  | 2 / 5 | `00254CC0` (`00254D63`); `SaveLoad_NormalizeLoadedRuntimeStateAndReseedRNG` `00584210` (`00584314`) | `002536B0` (`002536C7`); `00254C90` (`00254CA5`); +3 more |
| `+0x0020` | 16 |  | 4 / 4 | `WorldTransitionSnapshot_CaptureRuntimeState` `00229B40` (`00229C71`); `SaveWrite_PrepareAndSubmitFullImage` `0057E310` (`0057E371`); `SaveUI_RestoreActiveHeaderFromControllerBackup` `00583C00` (`00583C51`); +1 more | `WorldTransitionSnapshot_CaptureRuntimeState` `00229B40` (`00229C6D`); `SaveWrite_PrepareAndSubmitFullImage` `0057E310` (`0057E36D`); +2 more |
| `+0x0021` | 1 |  | 1 / 0 | `SaveImage_FinalizeHeaderAndChecksum` `00583D60` (`00583DEE` +1) |  |
| `+0x0022` | 1 |  | 1 / 0 | `SaveImage_FinalizeHeaderAndChecksum` `00583D60` (`00583E01` +1) |  |
| `+0x0023` | 1 |  | 1 / 1 | `SaveImage_FinalizeHeaderAndChecksum` `00583D60` (`00583E04` +6) | `SaveImage_FinalizeHeaderAndChecksum` `00583D60` (`00583DBA` +2) |
| `+0x0030` | 16 |  | 3 / 4 | `WorldTransitionSnapshot_CaptureRuntimeState` `00229B40` (`00229C79`); `SaveWrite_PrepareAndSubmitFullImage` `0057E310` (`0057E379`); `SaveUI_RestoreActiveHeaderFromControllerBackup` `00583C00` (`00583C59`) | `WorldTransitionSnapshot_CaptureRuntimeState` `00229B40` (`00229C75`); `SaveWrite_PrepareAndSubmitFullImage` `0057E310` (`0057E375`); +2 more |
| `+0x003C` | 4 | header dword written by the finalizer | 1 / 0 | `SaveImage_FinalizeHeaderAndChecksum` `00583D60` (`00583F0D`) |  |
| `+0x0040` | 16 |  | 4 / 4 | `WorldTransitionSnapshot_CaptureRuntimeState` `00229B40` (`00229C81`); `SaveWrite_PrepareAndSubmitFullImage` `0057E310` (`0057E381`); `SaveUI_RestoreActiveHeaderFromControllerBackup` `00583C00` (`00583C61`); +1 more | `WorldTransitionSnapshot_CaptureRuntimeState` `00229B40` (`00229C7D`); `SaveWrite_PrepareAndSubmitFullImage` `0057E310` (`0057E37D`); +2 more |
| `+0x0044` | 4 |  | 1 / 0 | `SaveImage_FinalizeHeaderAndChecksum` `00583D60` (`00583F10` +1) |  |
| `+0x0048` | 4 |  | 1 / 0 | `SaveImage_FinalizeHeaderAndChecksum` `00583D60` (`00583F4B`) |  |
| `+0x004C` | 4 |  | 1 / 0 | `SaveImage_FinalizeHeaderAndChecksum` `00583D60` (`00583F3C`) |  |
| `+0x0050` | 16 |  | 6 / 6 | `WorldTransitionSnapshot_CaptureRuntimeState` `00229B40` (`00229C89`); `SaveWrite_PrepareAndSubmitFullImage` `0057E310` (`0057E389` +1); `00580CD0` (`00580D8E`); +3 more | `WorldTransitionSnapshot_CaptureRuntimeState` `00229B40` (`00229C85`); `SaveWrite_PrepareAndSubmitFullImage` `0057E310` (`0057E385`); +4 more |
| `+0x0054` | 1 |  | 1 / 0 | `SaveImage_FinalizeHeaderAndChecksum` `00583D60` (`00583F53`) |  |
| `+0x0057` | 1 | byte the finalizer and the loader both write | 2 / 2 | `SaveImage_FinalizeHeaderAndChecksum` `00583D60` (`00583F63` +2); `SaveLoad_NormalizeLoadedRuntimeStateAndReseedRNG` `00584210` (`0058436D`) | `SaveLoad_NormalizeLoadedRuntimeStateAndReseedRNG` `00584210` (`0058423A`); `WorldTransitionSnapshot_RestorePersistencePairForActiveSlot` `005843E0` (`00584404`) |
| `+0x0058` | 4 | `002EF2A0()` at init | 1 / 0 | `SaveRuntime_InitializeHeaderAndImageBackedState` `00253A80` (`00253AB8`) |  |
| `+0x005C` | 4 | `002EF290()` at init | 1 / 0 | `SaveRuntime_InitializeHeaderAndImageBackedState` `00253A80` (`00253AC7`) |  |
| `+0x0060` | 16 | `00235E90()` at init | 4 / 4 | `WorldTransitionSnapshot_CaptureRuntimeState` `00229B40` (`00229C91`); `SaveRuntime_InitializeHeaderAndImageBackedState` `00253A80` (`00253AD6`); `SaveWrite_PrepareAndSubmitFullImage` `0057E310` (`0057E391`); +1 more | `WorldTransitionSnapshot_CaptureRuntimeState` `00229B40` (`00229C8D`); `SaveWrite_PrepareAndSubmitFullImage` `0057E310` (`0057E38D`); +2 more |
| `+0x0064` | 4 | `00235E80()` at init | 1 / 0 | `SaveRuntime_InitializeHeaderAndImageBackedState` `00253A80` (`00253AE5`) |  |
| `+0x0068` | 4 | magic `0x0131F3EA` | 1 / 3 | `SaveRuntime_InitializeHeaderAndImageBackedState` `00253A80` (`00253AED`) | `00280140` (`0028036E`); `00394130` (`003941D8`); +1 more |
| `+0x006C` | 4 | `0x4818` — the image-backed block's size | 1 / 1 | `SaveRuntime_InitializeHeaderAndImageBackedState` `00253A80` (`00253AFB`) | `SaveImage_ValidateRuntimeFormatHeader` `00255260` (`0025526B` +1) |
| `+0x0070` | 16 |  | 4 / 5 | `WorldTransitionSnapshot_CaptureRuntimeState` `00229B40` (`00229C99`); `SaveWrite_PrepareAndSubmitFullImage` `0057E310` (`0057E399`); `SaveUI_RestoreActiveHeaderFromControllerBackup` `00583C00` (`00583C79`); +1 more | `WorldTransitionSnapshot_CaptureRuntimeState` `00229B40` (`00229C95`); `SaveWrite_PrepareAndSubmitFullImage` `0057E310` (`0057E395`); +3 more |
| `+0x0078` | 2 |  | 1 / 1 | `SaveLoad_NormalizeLoadedRuntimeStateAndReseedRNG` `00584210` (`00584261`) | `SaveLoad_NormalizeLoadedRuntimeStateAndReseedRNG` `00584210` (`00584301`) |
| `+0x007A` | 1 |  | 1 / 1 | `SaveLoad_NormalizeLoadedRuntimeStateAndReseedRNG` `00584210` (`00584269`) | `SaveLoad_NormalizeLoadedRuntimeStateAndReseedRNG` `00584210` (`00584309`) |
| `+0x007B` | 1 |  | 1 / 1 | `SaveLoad_NormalizeLoadedRuntimeStateAndReseedRNG` `00584210` (`00584270`) | `SaveLoad_NormalizeLoadedRuntimeStateAndReseedRNG` `00584210` (`00584310`) |
| `+0x007C` | 4 |  | 1 / 1 | `SaveLoad_NormalizeLoadedRuntimeStateAndReseedRNG` `00584210` (`00584278`) | `SaveLoad_NormalizeLoadedRuntimeStateAndReseedRNG` `00584210` (`00584317` +1) |
| `+0x0080` | 16 |  | 4 / 6 | `WorldTransitionSnapshot_CaptureRuntimeState` `00229B40` (`00229CA6`); `SaveWrite_PrepareAndSubmitFullImage` `0057E310` (`0057E3A6`); `SaveUI_RestoreActiveHeaderFromControllerBackup` `00583C00` (`00583C86`); +1 more | `WorldTransitionSnapshot_CaptureRuntimeState` `00229B40` (`00229C50` +2); `SaveWrite_PrepareAndSubmitFullImage` `0057E310` (`0057E350` +2); +4 more |
| `+0x0084` | 4 |  | 1 / 1 | `SaveLoad_NormalizeLoadedRuntimeStateAndReseedRNG` `00584210` (`0058428D`) | `SaveLoad_NormalizeLoadedRuntimeStateAndReseedRNG` `00584210` (`00584338`) |
| `+0x0088` | 4 |  | 1 / 1 | `SaveLoad_NormalizeLoadedRuntimeStateAndReseedRNG` `00584210` (`00584299`) | `SaveLoad_NormalizeLoadedRuntimeStateAndReseedRNG` `00584210` (`00584344`) |
| `+0x008C` | 4 |  | 1 / 1 | `SaveLoad_NormalizeLoadedRuntimeStateAndReseedRNG` `00584210` (`005842A5`) | `SaveLoad_NormalizeLoadedRuntimeStateAndReseedRNG` `00584210` (`00584350`) |
| `+0x0090` | 16 |  | 3 / 4 | `WorldTransitionSnapshot_CaptureRuntimeState` `00229B40` (`00229CAD`); `SaveUI_RestoreActiveHeaderFromControllerBackup` `00583C00` (`00583C8D`); `SaveLoad_NormalizeLoadedRuntimeStateAndReseedRNG` `00584210` (`005842B1`) | `WorldTransitionSnapshot_CaptureRuntimeState` `00229B40` (`00229CA9`); `00580CD0` (`00580E0F`); +2 more |
| `+0x00A0` | 16 |  | 2 / 2 | `WorldTransitionSnapshot_CaptureRuntimeState` `00229B40` (`00229CB5`); `SaveUI_RestoreActiveHeaderFromControllerBackup` `00583C00` (`00583C95`) | `WorldTransitionSnapshot_CaptureRuntimeState` `00229B40` (`00229CB1`); `SaveUI_BackupActiveHeaderToControllerCache` `00583CB0` (`00583D41`) |
| `+0x00B0` | 16 |  | 2 / 2 | `WorldTransitionSnapshot_CaptureRuntimeState` `00229B40` (`00229CC2`); `SaveUI_RestoreActiveHeaderFromControllerBackup` `00583C00` (`00583C9D`) | `WorldTransitionSnapshot_CaptureRuntimeState` `00229B40` (`00229CB9`); `SaveUI_BackupActiveHeaderToControllerCache` `00583CB0` (`00583D49`) |

Untouched: `+0xC0`–`+0x1FF` (320 B).

## 3. Key addresses

| address | what |
|---|---|
| `002EF2B0`, `002EF640`, `002EF620`, `002EF630` | the payload base and the three buffer getters (seeds) |
| `020927C0` | global pointer to the image-backed block = buffer `+0x8200`; set by `00253970` |
| `02092758` | global pointer to the buffer; set by `00253970` |
| `00253970` | assigns both pointers, then runs the init chain |
| `02EBF190` | global pointer to the battle-state block = buffer `+0x4E68C`; set by `SaveRuntime_RebindImageBackedGameplayState` (`00238A80`) and `00233C10` |
| `00233C10` | rebinds the block if unset, checks its magic `0x05071901`, and sets or clears flag `0x1000` at its `+4` from `02089344` bit 0 |
| `00253A80` | `SaveRuntime_InitializeHeaderAndImageBackedState` — zeroes the block (`0x4818`), writes header `+0x58`–`+0x6C` |
| `00229B40` | `WorldTransitionSnapshot_CaptureRuntimeState` — the capture that fills the snapshot mirror, the group bank and SpawnKeep image A |
| `005843E0`, `00584580` | restore / capture of the persistence pair for the active slot |
| `00233440` | `SpawnKeep_SerializePersistenceBanks` |
| `00233550` | `SpawnKeep_RestorePersistenceBank` |
| `0025D8E0` | `WorldPersistence_ExportGroupPersistentBank` |
| `00269A20` | `WorldPersistence_ImportGroupPersistentBank` |
| `0030B6A0` | inventory class descriptor rebase on load |

## 4. Data structures and formulas

```
save image buffer (0x56690)
  +0x0000  header (0x200)
  +0x0200  payload (0x56490)
     +0x0000 kind-3 operand bank i16[256] (0x200, via slot 0 +0x48 = 02098E58)
     +0x1044 world-transition record (32 B)      +0x1384 flag banks (432 B)
     +0x2000 block copy (0x6000; was 'mirror 0x80') +0x8000 image-backed block (0x4818): +0x224 entry table, +0x3244 flags,
                                                          +0x32C4 bitmap, +0x3844 fired bitmap, +0x47E8
     +0xE040 group bank A (0x200)                +0xE240 SpawnKeep image A (0x20010)
     +0x2E250 group bank B (0x200)               +0x2E450 SpawnKeep image B (0x20010)
     +0x4E460 transition metadata (0x2C)         +0x4E48C battle-state block *(02EBF190), 0x7410 B: magic 0x05071901, +4 flags,
                                                          +8 party BattleStatsRecord[40] (0x1C8 each), ... +0x5B00..+0x5B0E
     +0x53C54 inventory descriptors
```

## 5. Call chain

Capture: `00229B40` → snapshot mirror, group bank A (`0025D8E0`), SpawnKeep image A (`00233440`);
`00584580` → the persistence pair. Restore: `005843E0` → `00233550` on both images; `00584210`
normalises the header and reseeds; `0030B6A0` rebases the inventory descriptors. Achievements:
`00253970` → `020927C0`; the accessors in [the achievement page](../../20-Platform-Online-Achievements/steam-integration-and-achievement-catalogue.md).

## 6. Modding notes

- **The achievement state is in the save file** at payload `+0x8000`–`+0xC817`; the "already fired"
  bitmap at `+0xB844` is what a mod that unlocks or resets achievements would touch.
- **A zone's remembered monsters are two 131 KB images in the save**, each preceded by a ~~128-byte~~ 512-byte *(corrected 2026-10-02, OPUS: `0x200` B, this page's bank rows, corrected 2026-09-11)*
  group bank; editing one entry means editing a `0x250` record inside `+0xE250` or `+0x1E250`
  ([the spawn-keep entry](../../05-Spawn-Encounter-Lifecycle/Spawn-Record/the-spawn-keep-entry-field-map.md)).
- **Inventory descriptors are stored as pointers and rebased on load** — a save edited by hand must
  leave `+0x53C54`–`+0x53C9B` to the loader.

## 7. What is not known

- [x] **FG-1.** ~~**What the 0x180 × 0x20 entry table at `+0x8224` holds per entry** beyond the achievement
  page's reading of its accessors~~, and what `+0x8030` / `+0x8090` / `+0xB2CC`–`+0xB868` (the
  `00315xxx` family) are. **FG-1.** *Table half answered 2026-09-12 (FABLE):* **each 32-byte entry
  is a navigation map's revealed-tile bitmap** — the "explored" fog the in-game map lifts as you
  walk. The accessor `002551B0(out, fieldId)` indexes the table by **`003779F0(fieldId)`**, the
  12-bit navimap entry id in bits 0–11 of the field record (`[02ADD100]` bytes `+8`/`+9`; `0xFFF`
  → no entry, so `≤ 0x180` entries — 384 slots for 370 shipped ids), and copies the entry to `out`
  or returns its address (`002551C0`–`002551ED`). The live copy is the 32-byte block `02B45978`
  (pointer `02B45A50`): `003C5410(fieldId)` sizes it from the navimap's cell dimensions
  (`02B457F8` / `02B457FC`, `0x100` × `0x100` default → 16 × 16 tiles of 16 × 16 cells = 256 bits,
  `003C543D`–`003C54A2`) and loads the saved entry into it, filling `0xFF` (all revealed) when
  there is none (`003C54B6`–`003C54C2`); `003C5500` marks it every frame the focus actor's position
  changes (`02B45A64`–`02B45A6C`), transforming a ±24-unit neighbourhood in 8-unit steps into map
  cells and setting bit `(x >> 4) & 7` of byte `(y >> 4) × rowBytes + (x >> 4 >> 3)` (`003C566D`–
  `003C56BC`); and the three writers copy the live block back into the entry — `003C8670` from
  `WorldTransition_StageFieldTransition` (the field being left), `003C60F0` from `0027F5D0` for
  the active-or-pending field, `003C5E50` from `00252DE0` when `02B45A00` bit 0 says the block is
  live. The UI readers (`00403970`, `00403F90`, `00404730`, `003C4070`, `003C4B20` — interior read 2026-09-17, SWE2-FRONTIER: 1,282 B, `0035D460` ×3 + `003C72F0`/`002DD350`/`00248EB0`, first call at [`003C4B3F`](../../_index/ADDRESS-INDEX.md); `003C72F0` itself reads the same day: 1,111 B — `00202B70` ×2 + `00203080`/`00202CA0`, first call [`003C74FE`](../../_index/ADDRESS-INDEX.md)) draw the map
  from the copied entry. So the table is per-navimap exploration state, not achievement counters;
  the `+0x8030` / `+0x8090` words and the `00315xxx` family's bytes remain.
  *Narrowed 2026-09-15 (FABLE), still open.* The region was re-read as a unit, as image-block offsets (payload − `0x8000`).
  - **`+0xB2CC`–`+0xB86B` is the Clan Primer's per-entry state.** A static table ties it to the Handbook screen:
    - `00D23750` maps the screen's eight tabs to categories `[0,1,2,3,4,6,5,7]`.
    - `00D23758` gives each tab's entry count: 160 / 96 / 64 / 120 / 56 / 512 / 48 / 30.
    - The Handbook code (`00576550`, `00576920`) passes that category to the flag functions.
    - The string `handbook_monster%03d.txt` follows the tables.
  - **Two parallel flag families**, one bit or byte per entry:

    | tab (category) | family A — tested `003154B0`, set/cleared `00315910` | family B — set/cleared `00315B50` |
    |---|---|---|
    | 0–4 (0–4) | one 496-bit set at block `+0x32CC`, category bases 0 / 160 / 256 / 320 / 440 (`00D10630` / `00D10640`) | the parallel 496-bit set at `+0x330C`, same bases |
    | 5 (6), 512 | not a bit: set when the entry's defeat count (`00315420`, the bestiary byte at `+0x3404` minus 1) is above 0; an entry listed in the keyed record table `[022C2550]` is tested by its record instead (type 0: a field variable ≥ the record's value; type 1: another entry's defeat count above 0) | ~~one whole byte per entry at `+0x3604`~~ **eight bits per entry at `+0x3604`** — `00315AD0` sets or clears one bit, `00315B50` all eight (corrected 2026-09-15) |
    | 6 (5), 48 | not stored in this family | a 48-bit set at `+0x33F4` |
    | 7 (7), 30 | a 30-bit set at `+0x3844` — the achievement page's "already fired" bitmap | the parallel 30-bit set at `+0x3848` |

    Tab 5 is therefore the bestiary: its index space is the 512-byte defeat block `+0x3404` that
    [event memory at actor bind](../../14-Story-Event-Quest-Hunt/event-memory-at-actor-bind.md) already reads.
  - **Two more id-indexed arrays** in the region, each bounded `id < 0x100`: a 256-bit set at `+0x334C` (`00315A20`) and
    256 four-bit values at `+0x336C`, stored as nibbles (`00315CD0`, value `< 0x10`).
  - **`+0x3868` is a `u32` that `00315390` turns into a rank 1–12.** It walks a 12-row table ending at `00D10628`
    (8-byte rows `{u32 threshold, u8, u8, u16}`) from the top. A row is taken when the word, `00316480()` and
    `00316670()` all meet its threshold and its two byte minimums.
  - **`+0x8030` / `+0x8090` ~~are the heads of two arrays~~ head two of the three arrays of one typed store** —
    ~~block `+0x30` is a `u16[48]` and `+0x90` a `u32[101]`~~ *(corrected 2026-09-26, FABLE, Claude Opus 5.5)*: block
    `+0x30`–`+0x223` holds a `u16[32]` at `+0x30`, a `u8[32]` at `+0x70` and a `u32[101]` at `+0x90`, each selected by a
    class code (6, 7, 8). The payload therefore also carries `+0x8070`, which the census table above has no row for. The
    header initialiser clears ~~both~~ all three with one 500-byte `memset` from `+0x30` (`00253B36`–`00253B42`); the
    three arrays tile that span exactly (64 + 32 + 404 bytes). `00252610` /
    `002527B0` write them and `002526F0` reads them, indexed, ~~in two modes selected by `ecx == 1`~~ by the class in
    `ecx` (the `cmp ecx, 1` follows `sub ecx, 6` / `sub ecx, 1`, so it selects class 8). Indices are clamped to 31, 31
    and 100, and a negative index becomes 0. The read returns 0 unless its third argument is set or bit 15 of
    `[[0215E6E0]]` is. Control: `_index/candidates/fg1-typed-store/typed_store.py`, 9 checks. Its planted negative
    requires that no accessor reaches the `u16` class past `+0x6F`.
  - **Who writes family B (added 2026-09-15): the Handbook's viewers, as they display an entry**, always with `set = 1`:
    - the page view `00572600` on tab 7 (`0057284C`–`0057285D`);
    - `005789D0` on tab 6 (`00578AEB`–`00578AF9`);
    - `00574900` through `00577A20`. For a bestiary entry (tab 5) it sets bit *page* of the entry's `+0x3604` byte when
      `00576F30(5, entry, page)` returns 0; for the other tabs it sets the entry's flag when the page shown is the last one
      (`00574914`–`0057497C`).
    So B records what the screen has displayed, per page for the bestiary. A is what the listing tests
    (`00576550`, `00576920`). Calling them "read" and "unlocked" is the natural reading of their writers and readers,
    not a traced player-visible effect.
  - **Not read:** ~~which of A and B means "unlocked" and which "viewed";~~ ~~what tabs 0–4 and 6 are called;~~ what the
    `+0x334C` / `+0x336C` ids and the `+0x30` / `+0x90` arrays count; ~~what the rank table's two minimum counts are~~.
    *(Read 2026-09-26 (FABLE, Claude Opus 5.5), `FG-1`; control [`fg1_clan_primer.py`](../../_index/candidates/fg1-clan-primer/fg1_clan_primer.py), 3 checks, FAILS 0.)*
    - **Tabs 0–4** are the handbook's story, world, person, knowledge and tutorial files. The tab table's six family
      bases are the `menuhandbook_<family>` resources the [handbook-index page](../../02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/hchk-hctg-hdat-handbook-indexes.md)
      names. These are file stems, not on-screen captions.
    - **Tab 6 is the hunt list.** Its viewer bit is the row's ordinal within its row kind in the hunt table
      (`menuquest`), with capacity 48.
    - **The rank table's minima.** The `+5` byte is compared with the count of set bits in the 30-bit set at
      `+0x3844`, and only rank 12 requires it: all 30. The `+4` byte is the other count's minimum, rising from 2 at
      rank 2 to 44 at rank 12. What that count counts is not read.
  **ANSWERED 2026-09-27 (OPUS), FG-1:** the three remaining sub-questions are settled from bytes and shipped data. (1) The rank table's +4 count is 00316480's: it walks the menuhandbook.bin hcom node bound at [022C2550] (p = blob+8, two u16 self-relative hops, count at +2, 2-byte entries {questId, minimum} from +4). It counts an entry when the quest registry's clear bit +0x1020 (0046B1A0, isquestclear) or order bit +0x1000 (0046B240, isquestorder) is set and the quest scenario flag +0x1064[id] (0046B180, getquestscenarioflag) is at least the minimum. The shipped node is identical in all nine locales: 45 entries, quest ids 128-172 once each, minima 30/50/70/90/100. So the count is the listed quests whose scenario flag has reached the listed stage; rank 12 needs 44 of the 45. (2) +0x334C (256 bits) and +0x336C (256 nibbles, 128 B) are the handbook's gate-input banks. Image-wide they have one writer each (00315A20, 00315CD0), called only by the hdat entry op executor 00577A40. They have one reader each (00315620, 00315470), called by the hchk gate 00575E80 and by 00577A40. The shipped data exercises neither side: all 2,844 non-monster hchk gates hold the 0xFF sentinel in both slots, and all 12,168 hdat op programs are empty. So both banks stay zero in every save this executable writes, and no id carries a meaning in this title. (3) The +0x30 u16[32] / +0x70 u8[32] / +0x90 u32[101] store (classes 6/7/8) is the remembered menu cursor positions (Cursor Position = Last Selection). The option's setter 002DE1E0 writes option bit 15 and tail-jumps 002526D0, which clears the 0x1F4-byte table, and the reader 002526F0 first calls the bit-15 getter 002DDD50. Not claimed: which menu owns each slot (54 call sites), the 45 quests' names, and the authored intent of the unused banks. Store rows renamed from achievementState*/imageState*Array, carried from the refuted achievement reading. Control _index/candidates/fg1-residue/fg1_residue.py (15 checks with 2 mutants, FAILS 0).
- [x] **FG-2.** **The 23,185 bytes at `+0x2081`–`+0x7B11`** — no enumerated route. (The second large range
  the first run left, `+0x4E50D`–`+0x53C53`, is the battle-state block: `02EBF190` is a pointer into
  the image, §2.2.) **FG-2.**
  **ANSWERED 2026-09-26 (FABLE, Claude Opus 5.5) by reference: the range lies inside the `0x6000`-byte copy of the battle-state block
  at `+0x2000`, which §2.2 and the type-store section already describe.** Control: [`fg2_battle_state_mirror.py`](../../_index/candidates/fg2-battle-state-mirror/fg2_battle_state_mirror.py) (3 checks, FAILS 0).
  - The capture copies the block to payload `+0x2000` in `0xC0 × 0x80` strides, and the restore copies it back.
  - So payload `+X` here is block `+(X − 0x2000)`, and this range is block `+0x81`–`+0x5B11`, whose fields are the
    [battle-state block page](../../11-Party/Battle-State-Block/the-battle-state-block-field-map.md)'s.
  - It ends just before `+0x7B12`, the importer's probe word (`FG-3`), which is why the census's boundaries fall
    there.
- [x] **What `+0x7B12` / `+0x7B42` and `+0x1164` / `+0x1364` / `+0x1534` are.** **FG-3.** *Narrowed 2026-09-13 (FABLE):* `+0x7B12` / `+0x7B42` are inside the `0x6000`-byte battle-state copy at `+0x2000` — block `+0x5B12` (member 0, bank 0, slot 0's action word) and `+0x5B42` (that bank's count byte), two of the four fields `00235AF0` compares before importing ([battle-state block §2.9](../../11-Party/Battle-State-Block/the-battle-state-block-field-map.md)). `+0x1164` / `+0x1364` / `+0x1534` stay open.
  **Answered 2026-09-14 (FABLE).** A static read of every displacement access to the three offsets
  (`dispscan`), all through `SaveImage_GetPersistentPayloadBase`. The verb names are the external catalog's
  ([provenance](../../01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-dispatch.tsv)): leads, not engine names.
  - **`+0x1164` is `u16[256]`** (it ends at `+0x1364`), one word per index of a 256-entry registry.
    - **Writers:** `0046B350(i, w)` stores the word (`0046B364`), reached from verb `0x2B5` (`setquestcontract`,
      index clamped to 0–255, `00351581`–`0035159F`). `0046B3F0(i, set)` sets bit `i` of the bitset at
      `+0x1000` and, **only when that bit was clear**, stamps the current field id (`003148F0`) into word `i`
      (`0046B42D`–`0046B44E`); clearing leaves the word alone (`0046B466`–`0046B470`). `0046B3F0` is reached
      from verb `0x1D1` (`setquestorder`, `0033FF80`) and from arm 4 of `00329E60`'s jump table (`00329EC9`).
    - **Readers:** `0046B0D0(i)` (`0046B0DE`), reached from verb `0x2B6` (`getquestcontract`, `00351C65`) and from
      `AiTargetSelector_ResolveOperandValue` (`00321232`).
    - So the word is a per-entry field id by default, which a script can overwrite. The neighbours complete
      the registry: bitset `+0x1000` (`getquestorder` `0x1D3` reads it), bitset `+0x1020` (`getquestclear`
      `0x1D4`) and the count `+0x1040` (`getquestcleartotal` `0x1D5`).
  - **`+0x1364` is a 256-bit set** (32 bytes, ending where `Bank64A` starts at `+0x1384`).
    - `0046B380(i, on)` sets or clears bit `i` (`0046B3B5` / `0046B3D1`), from verb `0x2BC` (`setquestok`).
    - `0046B1F0(i)` tests it (`0046B224`), from verb `0x2BD` (`isquestok`).
    - Both verbs clamp the index to 0–255.
    - The only other `+0x1364` displacement in the executable, `001E72E6`, is a `dword` store on an `r14`
      object in `001E71B0`. It is not this payload.
  - **`+0x1534` is the saved music override**, as [the area-music page](../../18-Audio/how-the-music-changes-when-you-change-area.md)
    reads it. All six accesses:
    - **Setter `0026A720`** (verb `0x471`, `setnowmapmusicno`, `00345E82`). A negative track clears `+0x1063` bit 6
      and zeroes the byte (`0026A72C`–`0026A73D`); otherwise it sets bit 6 and stores the track (`0026A74A`–`0026A75B`).
    - **Reset `002628B0`** clears bit 6 and stores `bpl` (`00262A65`–`00262A76`).
    - **Three readers** take the byte instead of `003EAA70(field)` while bit 6 is set: `0025DBB6`, `00262029`
      and `0026DE41`.
  - **Not claimed:**
    - Nothing was executed.
    - What the registry's entries are is not established from the image; "quest" is the catalog's word.
    - What `00329E60`'s other arms and the AI operand use the word for is not read.
- [x] ~~**Why the group bank and SpawnKeep image are paired twice** (`+0xE040` / `+0x2E250`) — which
  transition writes B and when the pair rotates.~~ **FG-4** — ANSWERED 2026-09-10: **the battle-state
  block's flag bit 12 selects the pair.** `00236760` returns `(*(02EBF190) + 4) >> 12 & 1`
  (`00236760`–`00236770`); `WorldTransitionSnapshot_CapturePersistencePairForActiveSlot` (`00584580`)
  writes pair A (`0025D8E0` at `+0xE040`, `00233440` at `+0xE240`) when it is 0 and pair B (`+0x2E250`,
  `+0x2E450`) when it is 1 (`00584593`–`005845E1`), then captures the transition metadata at
  `+0x4E460` and stores the byte `0208D455` into its first dword (`005845BB`–`005845C2`);
  `WorldTransitionSnapshot_RestorePersistencePairForActiveSlot` (`005843E0`) restores A when the
  bit is 0, B when `00394450()` returns 3 and header `+0x57` bit 0 is set (`00584404`–`0058445E`),
  clears bit 1 of block `+0x5B04` after B (`0058446A`), and reads the byte back from `+0x4E460`
  (`00584471`–`00584482`). The bit is set or cleared by `00233C10` from `02089344` bit 0
  (`00233C6E`, `00233CA6`); what that global bit means is the residue.

- [x] ~~**What the shared script globals mean** — `+0x900`–`+0x910` (a saved pose and a map flag by
  their tool names), `+0x940`–`+0x943`, `+0xB14` (`quest_global_flag[94]`), `+0xC7C`, `+0xC88`–`+0xCF4`
  — and where ff12-script's `globalMap` names come from.~~ **FZ-27 ANSWERED 2026-09-12 (FABLE) from
  the shipped scripts** — every use of the six names over the 1,114 decompiled `us` scripts
  (`ff12-script -dc`, the BQ-10 corpus), assignments and consumers counted:
  - **`+0x900`–`+0x90C` `mp_map_set_angle / _x / _y / _z`** are a **scratch look-at target, not a
    saved pose**: `_x`/`_y`/`_z` are set from literals (568 / 534 / 569), from file variables (72)
    or from an object's `getx()`/`gety()`/`getz()` (`warp_up.getx()` 55, `warp.getx()` 26 …),
    `_angle` is `getangle(mp_map_set_x, mp_map_set_z)` (698) or a literal (`π` 311, 0 296, `5π/3`
    236, `2π/3` 236), and the only consumers are **`turn_62(mp_map_set_angle)`** (3,521) and
    **`rlookat(mp_map_set_angle)`** (3,132). The cell in §2.2 reading "a map's saved player pose" is
    corrected by this: the four floats are the argument staging area of the turn/look verbs.
  - **`+0x910` `mp_map_flg`** is a **scratch handle**, not a flag: it takes the handle returned by
    `mapsoundplay` (279) or `sebsoundplay` (216) and is awaited with `eventsoundplaysync(mp_map_flg)`
    (583), or a field-effect id `1 … 6` (111 each) passed to `set_field_effect` (111) /
    `clear_field_effect` (210); `= 0` (588) resets it.
  - **`+0x940` `mp_last_weather`**: the script's cached weather slot — `= getweatherslot()` (2,806),
    overridden by literals `1` / `3` / `2` / `−1` (531 / 427 / 411 / 224), read by `switch` (127) and
    `if` (53) to branch weather-dependent behaviour.
  - **`+0xB14` `quest_global_flag[94]`**: per-quest progress bytes — counters (`[6]++` 50, `[8]++` 34,
    `[7]++` 7, `[7] = 10`), bit flags (`[4] |= 1`, `[4] |= 2` with the matching `& 1` / `& 2` tests, 13
    each) and resets (`[0]`–`[3] = 0`, 11 each) across 103 scripts.
  - **`+0xC7C` `g_com_navi_footcalc[3]`**: the party leader's last sampled position —
    `[0] = getx_12b(-1)`, `[1] = gety_12c(-1)`, `[2] = getz_12d(-1)` (234 each) — tested with
    `distance_290(-1, [0], [2]) >= 0.8` (246): a "has the leader moved" check in 96 scripts.
  - **`+0xC88` / `+0xC8C` / `+0xCF0` `g_com_set_get_label` / `_2` / `_3`**: item-acquisition message
    ids — assigned per script (`= 139` 38, `= 0x80B5` 16 …; 398 / 235 / 195 assignments) and consumed
    by `additemmes(label, 1)` (1,353 / 193 / 193) and `setmeswinmesid(0, label)` (386 / 580 / 193).
  None of the six is the region's one native reader (`002EF390`, `+0xA00 + i`), so all six are
  script-only state that the save carries verbatim. **Where the `globalMap` names come from is not
  in the game**: the usage matches every name (`getweatherslot` ↔ `mp_last_weather`, `additemmes` ↔
  `set_get_label`), which supports the table reproducing authored symbol names, but the table's
  source is the tool's and stays unproved here.

## 8. Evidence

| claim | evidence | tier | confidence |
|---|---|---|---|
| Every row of both tables | `save-payload-accesses.tsv`, `save-header-accesses.tsv`; `hop_scan.py --retseed 002EF2B0,002EF640:-0x200,002EF620:-0x200,002EF630:-0x200 --gptr 020927C0:0x8000,02092758:-0x200,02EBF190:0x4E48C --size 0x56490 --depth 3`, control `003148F0:0x1044` found; **92 rows removed 2026-09-13** (below) | 1 | PROVEN |
| `020927C0` = buffer `+0x8200`; the block's size and magic in the header | `00253979`–`00253990`; `00253AED`–`00253AFB` | 1 | PROVEN |
| `02EBF190` = buffer `+0x4E68C`; its magic `0x05071901` | `00238A89`–`00238A92`, `00233C2A`–`00233C33`; `00233C4D` | 1 | PROVEN |
| The region names | the linked pages and the writers named in §2.2 | 1 | PROVEN (by reference) |
| The untouched ranges | absence on every enumerated route with a passing control | 1 | PROVEN (for those routes) |
| The script-global region `+0x200`–`+0xCF4` | 1,114 descriptor tables decoded; the resolver `00262440` and the binder `0026CAF8`–`0026CAFD` read; `002EF390` / `001C1720` read | 1 | PROVEN (ownership); names tier 2 (tool table) |
| What the untouched ranges hold | **not established** | — | UNKNOWN |

> **92 census rows removed, 2026-09-13 (FABLE; the sibling of OPUS-REQ-FABLE-STATEBLOCK-ROUTE-CONTAMINATION).**
> The seed `02EBF190:0x4E48C` inherits the battle-state block census's defect. In `Battle_ProcessActionTarget` `00307300`,
> `rbx` is a stats record only inside the loop `003073F0`–`00307452`. The label `00307457` is reached from `003073E0`
> with `rbx` = the target unit, but the address-order walk carried the stats record across it. The unit path's reads
> and writes, and its callees' ones, were filed at `+0x4E494 + disp`. Re-running the command above with
> `--cut 00307300:00307457` (added to `hop_scan.py` for this) removes 97 rows of the current scanner generation and
> adds none. **92** of the 97 are rows of the committed TSV, and they are listed in
> [`route-contamination-removed.tsv`](route-contamination-removed.tsv). In §2.3, 15 offset rows carry the note and 24
> citations are struck. At 8 offsets no access remains: `+0x4E564`, `+0x4E574`, `+0x4E57C`, `+0x4E5F0`, `+0x4E5F4`,
> `+0x4EB2C`, `+0x4EB34` and `+0x4F334`. Those were a unit's `+0xD0`, `+0xE0`, `+0xE8`, `+0x15C`, `+0x160`, `+0x698`,
> `+0x6A0` and `+0xEA0`, never a stats record's. The block census loses the same sites except `00321786`, which only this census's
> depth-3 route reached; see [the battle-state block map](../../11-Party/Battle-State-Block/the-battle-state-block-field-map.md) §8.

## 9. Related

- [`save-image-buffers-header-and-payload.md`](save-image-buffers-header-and-payload.md) — the buffers, the header, the first map.
- [`../../20-Platform-Online-Achievements/steam-integration-and-achievement-catalogue.md`](../../20-Platform-Online-Achievements/steam-integration-and-achievement-catalogue.md) — the achievement accessors whose block this page places.
- [`../../05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md`](../../05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md) — the SpawnKeep images' internal layout.
- [`../../05-Spawn-Encounter-Lifecycle/Spawn-Record/the-spawn-keep-entry-field-map.md`](../../05-Spawn-Encounter-Lifecycle/Spawn-Record/the-spawn-keep-entry-field-map.md) — the record inside the images.

## Falsification pass 1 — 2026-09-12 (OPUS)

**passes: 1 · last_pass: 2026-09-12**

Every cited access site in this map was disassembled and its displacement compared with the offset of
the row citing it, by
[`check_field_citations.py`](../../../Tools/analysis-kit/gfz-scripts/check_field_citations.py):
**879 sites across 350 rows**.

| outcome | sites |
|---|---:|
| displacement **is** the row's offset | 138 |
| resolved through an embedded sub-object base | 645 |
| indexed form, indeterminate by displacement alone | 70 |
| cites the source object of a cross-object copy | 24 |
| cites a datum rather than an instruction | 2 |

**Nothing failed to decode, and no site contradicts its row.**

**The sub-object bases, counted for the first time** (44 distinct): `+0x4E494` x187, `+0x4E48C` x160, `+0x80` x46, `+0x4E4B8` x23, `+0x8000` x21, `+0x4E50C` x21, `+0x2080` x16, `+0xE0C0` x15.

**Two bases carry 347 of the 879 sites between them** - `+0x4E48C` and `+0x4E494`, sixteen bytes apart. A map of this size is really a map of one dominant sub-block and a long tail; that was not visible from the rows themselves.

**Not claimed:** this checks what the map *says* — that each citation touches the offset it is filed
under. It says nothing about fields the census never reached, and the document's own coverage limits
stand unchanged.

## Residual placements — 2026-09-14 (SWE2-FRONTIER, residual-placement package)

| function | size | role (call-signature read) |
|---|---:|---|
| `00564780` | 729 | save-pane body (callers `00564010`/`0056DD50`): `[rbx+0x180]`/`+0x17C`/`+0x17F`, `[rcx+0x17E]`/`+0x17F`; `00252D10`, `0057D610`, `00252D40`, `002526F0`, `0057D5E0` x2 |

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. The image-address resolver fan-out is MECHANICAL.*

**Input — CLIENT and SERVICE.** `InputGameplay_ArbitrateDigitalInputAndModalS…` reads three accessors this field map
cites:

- the flag getter `00236760`;
- `00264640`;
- `PersistentFlag_QueryPrimaryOrAuthoredThresholdGate` (`0032A8A0`).

**Input arbitration consults a `Primary` persistent flag.** In the other direction, the save-buffer binder `00253970`
(24 B and 26 B), the area unload `002628B0` (126 B), `0027F5D0` (~~30 B~~ **1,280 B — corrected
2026-09-14 (OPUS): the function list gives `0027F5D0` 1,280 bytes, and `how-a-sound-request-becomes-a-voice.md`
quotes the same figure; 30 B disagreed with both and `check_consistency` caught the pair**) and
`WorldTransition_RequeueCurrentFieldForRestore` (21 B) each call Input-filed helpers.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **CombatFormula — SERVICE and CLIENT, 86 edges.** The payload stores the battle stats record, and the functions that read and write that record are formula-layer ones:
  - the slot accessors `BattleStats_GetByBattleSlotIndex` and `BattleStats_GetByMappedBattleSlot`, called by 18 of the page's bodies;
  - `BattleStats_InitializeDefinitionRecord`, the record's initialiser;
  - `BattleStats_FindOwningBattleUnit`, the owner lookup;
  - `BattleFormula_ApplyTargetResult`, which calls the resource and HP mutators and the level advance, and calls `GameState_GetGil` / `GameState_SetGil`.
  The page maps where those fields live in the image, while the formula layer owns what they mean in play.
- **CoreRuntimeScheduling — SERVICE and CLIENT.**
  - Three cited bodies read small core getters (7, 9 and 11 bytes), and one calls a 40-byte core helper.
  - The save-buffer binder is called from the start-up subtree's root.
  - Two cited bodies are called by the 2,001-byte core frame body.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Gameplay — CLIENT (63 edges through 44 of this page's functions).** The Gameplay layer reaches this page at `00301AD0`, `0031C5D0`, `00329CC0`, `0031B810` and 40 more. `FUN_00234150` is the worked example, read in full - it is a 104-byte registration helper that takes the `.text` address `002FED60` as a callback and gates on `byte[+0] & 0x10` of what `0031B810` returns; **11 of the 18 bodies on that layer are read, the rest are counted**. The crossing is that those functions are consulted by that layer, not a shared responsibility. Edge count and subject list from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).

**Presentation — CLIENT (35 edges through 17 of this page's functions).** The Presentation layer reaches this page at `003C4070`, `002628B0`, `00403970`, `00404730` and 13 more. `FUN_00259b30` is the worked example, read in full - it is a 699-byte reset of two `0x860`-byte presentation slots based at `02098378`: each slot's `0x630`-byte body and its three `0xB0`-byte sub-blocks are zeroed and re-seeded from one transform, with the `+0x1F8` scale set to 1.0; **2 of the 30 bodies on that layer are read, the rest are counted**. The crossing is that those functions are consulted by that layer, not a shared responsibility. Edge count and subject list from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).

**RNG_Random_Selection — SERVICE.** `0025ACA0` on this page calls `RNG_MT19937_NextU32_Thunk`, owned by that layer. What it reaches is a five-byte thunk - `jmp 00863BF0` - onto the CRT's Mersenne Twister next-u32; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Rewards_Progression_Economy — SERVICE.** `0030E360` on this page calls `BattleUnit_ProcessDefeatRewardsAndLoot`, owned by that layer. What it reaches is defeat-and-loot processing, which reads the defeated unit's `+0x698` block, needs `byte[+5] == 1`, and is suppressed entirely by bit 3 of `byte[+0xE9A]`; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).


**ActorEntity — CLIENT (SWE2-EC7-156, 105 edges).** `003F1E90` calls `00202C70`/`00203170`, `00300E40` calls `00236760`, `002371B0` calls `0031B8xx` — the actor layer consults this page's helpers, shared fan-in.
**CombatAI — CLIENT and SERVICE (SWE2-EC7-156, 42 edges).** `00233C10` calls `00327F80`, `00239960`/`0023AC80` call `00327CB0`/`00326030` of that layer — the payload helpers and the combat layer exchange calls, no second owner.
**Items_Equipment_Shops_License — CLIENT and SERVICE (SWE2-EC7-156, 87 edges).** `00233C10` calls `0030B6A0`, `0023AF50` reaches `002370C0`/`00237DF0`/`00238xxx` — shared-helper exchange, not a shared responsibility.
**Movement — CLIENT (SWE2-EC7-156, 134 edges).** `00334220`/`003347C0`/`00334E00`/`00335B60` call `00202B10` — the movement layer consults this page's shared helper, fan-in.
**Party — CLIENT and SERVICE (SWE2-EC7-156, 77 edges).** `00239960` calls `00329080`, `003590D0` reaches `0025D9E0`, `00358B40`/`00359200` reach `002628B0` — shared-helper exchange, not a second owner.
**Status_Periodic_Terminal — CLIENT (SWE2-EC7-156, 45 edges).** `0030FED0` calls `002FEF30`, `0030E360` calls `00300FC0`, `0030F690` reaches `0030C470` — the status layer consults this page's helpers, shared fan-in.
**UI — CLIENT (SWE2-EC7-156, 340 edges).** `002A0440` calls `00181330`/`00181560`/`001816B0`/`00181870`; batch-121's `003096F0` helpers `00322C50`/`0020E600` share the fan-in — the interface layer consults this page's functions, not a shared responsibility.

**Script_VM_Native_Bridge — CLIENT (SWE2-EC7-157, 113 edges).** Batch-122's `0037E8D0` names `00473B90`/`002F9920`/`0037EF70`/`0037EFC0`, and the map's helpers (`00236740`/`00236760`/`00203170`) are reached by `0050F3F0`/`0050F540`/`00356160` on that layer — shared fan-in, no second owner.
- **PlatformOnlineAchievements - CLIENT and SERVICE (58 edges).** `00315420`, `003166F0`, `002536D0` are also called by bodies filed to platform/online achievements: `00316760`, `003160C0`, `00316A50` (+8 more); `00315E90`, `00316A50`, `003162E0` reach bodies filed to platform/online achievements: `008632B0`, `00315420`, `003165C0` (+16 more) - shared machinery across the layer boundary, no shared ownership.
- **Spawn_Encounter_Lifecycle - CLIENT and SERVICE (14 edges).** `00265020`, `0031B810`, `00265200` are also called by bodies filed to spawn/encounter: `00234AF0`, `00234DA0`, `002350C0` (+4 more); `00229B40`, `005843E0`, `00584580` reach bodies filed to spawn/encounter: `00233440`, `00233550` - shared machinery across the layer boundary, no shared ownership.
- **StoryEvent - CLIENT (2 edges).** `00265270`, `00314910` are also called by bodies filed to story event: `001ED240` - shared machinery across the layer boundary, no shared ownership.
- **Story_Event_Quest_Hunt - CLIENT and SERVICE (18 edges).** `002EF2B0`, `00265270`, `0032AB60` are also called by bodies filed to story/event/quest: `00377970`, `0032A8A0`, `0032A930` (+11 more); `00264920`, `002EF2D0`, `0032A8A0` reach bodies filed to story/event/quest: `0032A8A0`, `00379160`, `00377970` - shared machinery across the layer boundary, no shared ownership.
## The `003C5E50` exclusive subtree — all 4 members bound (SWE2-FRONTIER, followup queue)

`003C5E50` (~171 B) is the third revealed-tile writer the table above names —
the one that runs when `02B45A00` bit 0 says the live block is dirty. The full
body: `0028F970`, then the bit-0 gate at `003C5E59`; when set, `ebx =
[02B476B8]` (the navimap id), `003779F0(ebx)` exists-check, `002551B0(0, ebx)`
fetches the entry, and `02B45978`/`02B45988` are copied 0x20 B into it
(`003C5E86`–`003C5E97`); then `02B45A00` bit 0 cleared (`003C5EA0`),
`0035BB70`, memset `02B46280` (0x1430), `0028FA70`, memset `02B45850` (0x120),
memset `02B46280` again, `0028FF20`, `002908C0`, and a tail call into
`00290BE0` (`003C5EFB`).

The sibling at `003C5F00` is the **mark-dirty twin**: `02B45A00 |= 1`, memsets
the same `02B46280`/`02B45850` blocks, writes 19 dword flags at `02B45A04`
(`eax - 0xE` vs 4 → 1 when the index lies outside `[0xE, 0x12]`,
`003C5F30`–`003C5F48`), stores `003148F0()` into `02B476B8`, `003148F0`→
`003C5410`, clears `02B45970`, then `0028FAF0`/`0028FF00`/`00290960(1)`.

| member | role | interior |
| --- | --- | --- |
| `0028FA70` (115 B) | four-call `0209BE80`-manager battery — `003F8EA0`, `003F8A90`, `004FE3C0`, tail `0028A080` | [`0028FA87`](../../_index/ADDRESS-INDEX.md) |
| `002908C0` (117 B) | mode-3 conditional — `0209BE80` manager, `003F6FD0` fires only when `[rbx+0x2F0] == 3` (`00290909`) | [`00290909`](../../_index/ADDRESS-INDEX.md) |
| `00290BE0` (29 B) | conditional inner refresh — `0209BE80` nonnull and `[+0x10F10]` nonnull → `003F5030` (`00290BF6`) | [`00290BEC`](../../_index/ADDRESS-INDEX.md) |
| `003F8EA0` (31 B) | block-zero wrapper — `[rcx+0x52A0] = 0`, then `00861EC0(rcx+0x4020, 0, 0x1280)` | [`003F8EA0`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `0028F970`, `003779F0`, `002551B0`,
`0035BB70`, `00861EC0` (memset), `0028FF20`, `0028A080`, `003F8A90`,
`004FE3C0`, `003F6FD0`, `003F5030`, `003148F0`, `003C5410`, `0028FAF0`,
`0028FF00`, `00290960`.

## The `003C5500` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`003C5500` (~15 B) — thin forward.

| member | role | interior |
| --- | --- | --- |
| `0035D630` | `dword[022C83E8] >> 7`, `not`, `& 1` — inverted bit-7 getter (`0035D630`/`0035D63B`) | [`0035D630`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none.


### Interior citation — frontier hub `00282EA0` (2026-09-18, SWE2-EC7)

`00282EA0` — 53 B, 15 callers (the `0029xxxx` save-field readers above).
`rdx = [global + rcx*8 + 0xAC8]` selects a per-slot record, then a 9-iteration
scan compares `edx` against `ecx` walking `rcx + 0x408` at 0xC0 stride
([`00282EC0`](../../_index/ADDRESS-INDEX.md)) — returns the first matching slot
index, 0 when the record misses all nine. A fixed-window membership probe.

## The type store never received this page's 2026-09-13 correction (2026-09-19, OPUS)

*§2's row for `+0x2000`–`+0x7FFF` strikes through "a mirror of the battle-state block's first `0x80`
bytes" and replaces it with the `0x6000` copy. **`_types/fields.tsv` still carries the struck-through
reading**, and carries it across the largest `TYPE RESOLVED` span in the entire type store.*

The store's row is `SavePayload +0x2008`, **23,306 bytes**, `replicatedVec4RecordSpan2008`,
`TYPE RESOLVED / HIGH`, **evidence column empty**, reading:

> *replicated record region, stride `0x80`: the transition-capture paths (`00229B40`/`005844A0`) lea
> each record base `+0x80` apart and movups-write seven vec4s at `record+0x10..+0x70` (alternating
> xmm1/xmm0)*

Every element of that is the copy this page already corrected.

### The two functions run the same copy, and it is a `memcpy`

Measured in both bodies the row names, and they are the same instruction sequence:

| function | loop | count | source → destination |
|---|---|---|---|
| `00229B40` | [`00229B7B`](../../_index/ADDRESS-INDEX.md)–`00229BE2` | `mov r8d, 0xC0` | buffer `+0x4E68C` → `+0x2200` |
| `005844A0` | [`0058451C`](../../_index/ADDRESS-INDEX.md)–`00584572` | `mov ecx, 0xC0` | buffer `+0x4E68C` → `+0x2200` |

Each iteration is `lea dst,[dst+0x80]` / `lea src,[src+0x80]` and **eight src→dst `movups` pairs**.
`0xC0 × 0x80` = **`0x6000` = 24,576 bytes**, and buffer-relative `+0x4E68C → +0x2200` is
payload-relative **`+0x4E48C → +0x2000`** — §2's figures exactly, re-derived from the instructions.

So: **"stride `0x80`" is the copy's per-iteration advance**, and it is the `0x80` that survived from
the struck-through reading. **The "seven vec4s at `record+0x10..+0x70`" are eight steps of that
`memcpy`** — and *"alternating xmm1/xmm0"*, cited in the row as evidence of structure, is the
compiler's two-register pipelining, which is the **signature of an unrolled copy**. The row quoted
the thing that refutes it as its support.

*(`00229B40` also contains a `0x1C4`-iteration copy at `00229C50` and a `0x100` one at `00229BF0`.
Neither touches this region — worth stating because a census that grabbed the function's largest run
would attribute the wrong one, and `00229C75` inside the `0x1C4` loop is already the citation that
withdrew `SaveImageHeader.vec4StoreHead30`.)*

### Nothing reads the span's interior

From `save-payload-accesses.tsv`, the whole of `+0x2000`–`+0x7FFF` carries **24 accesses**: 19 are the
two copies and their pointer walks, and the other **5 are `00235AF0`, which only *compares*** —
`cmp dword [rdx]` (`+0x2000`), `cmp dword [rdx+4]` (`+0x2004`), `cmp word [rdx+0x5B12]` (`+0x7B12`),
`cmp byte [rdx+0x5B42]` (`+0x7B42`). Those four offsets are **exactly** the four scalar rows the store
already carries around this span (`mirrorBattle`, `payloadDword2004`, `payloadWord7B12`,
`payloadByte7B42`), which is why the tiling looks right even though the big row does not.

**Not one access anywhere in the 23,306 bytes is anything but a copy step.** The "vec4 records" have
no independent writer and no reader at all.

### What the span is instead, and it is better than unknown

A byte-for-byte copy makes the mapping exact: **mirror`+X` is battleState`+(X−0x2000)`**. The store's
own neighbours corroborate the alignment — `+0x2000` is the magic `0x05071901` and `+0x2004` the flag
dword, matching §4's `+0x4E48C` layout. So this row **begins at battleState`+0x8`, the start of the
party `BattleStatsRecord[40]` array** (`0x1C8` each = 18,240 bytes). 18,240 of its 23,306 bytes are a
type this database already documents, reached by copy rather than by a second declaration.

**NOT CLAIMED:** the 5,066 bytes past that array, and whether anything writes the mirror other than
the two capture copies — 24 accesses is what the table holds, not a proof of absence.

*Narrowed 2026-09-27 (OPUS): the mirror's last 0x4F0 bytes are gambit banks.* By the same identity, mirror `+0x7B10`–`+0x7FFF` is battleState `+0x5B10`–`+0x5FFF`, the start of `gambitBanks` (`GambitConfig[120]`, `0x34` per bank): banks 0–23 whole and bank 24's first `0x10` bytes. So `00235AF0`'s two interior compares read **bank 0's slot-0 action word** (`+0x7B12` = block `+0x5B12`) and **bank 0's `filledCount`** (`+0x7B42` = block `+0x5B42`). The store's four rows there now say so (control [`mirror_gambits.py`](../../_index/candidates/savepayload-mirror-gambits/mirror_gambits.py)). The bytes between the stats array and the banks (block `+0x4748`–`+0x5B0F`) map onto the BattleSystemState rows the same way; this note names them only by reference. Why `00235AF0` tests those two bank-0 values is not claimed.

### The propagation failure is the finding

The page was corrected on 2026-09-13. The store was not, and nothing caught it for six days:
`check_copy_displacements.py` tests whether a **cited address decodes to a copy step**, and this row
cites `00229B40` and `005844A0` — **function entries, not instructions** — so it never reached the
test. The largest overclaim in the store was invisible to the instrument written to find exactly that
overclaim. The check now carries a second pass for entry-only citations whose bodies are dominated by
a copy and write the object nowhere else; across all 2,938 rows it flags **this row and nothing else**.

## The three "unobserved" payload spans are zeroed wholesale, by two functions whose names say so (2026-09-19, OPUS)

*`unobservedSpan1538` (2,760 B), `unobservedSpanC818` (6,120 B) and `unobservedTail5589C` (3,060 B)
carry **no access at all** in `save-payload-accesses.tsv` — 11,940 bytes with no reader and no
individual writer. That is a statement about **reads**, and it was the only kind of statement anyone
had made about them. A bulk-write sweep finds the other half in two 35- and 50-byte functions.*

```
002EF5F0  SaveImage_ClearActiveRuntimeBuffer
    002EF5F6  lea  rcx, [rip + 0x1E74C83]   -> 02164280
    002EF5FD  mov  r8d, 0x56690
    002EF603  call 00861EC0                 ; memset(02164280, 0, 0x56690)

002EF650  SaveRuntime_ResetActiveImageAndRebindState
    002EF656  lea  rcx, [rip + 0x1E74C23]   -> 02164280
    002EF65D  mov  r8d, 0x56690
    002EF663  call 00861EC0                 ; the same clear, then 00253A80 / 002EF2D0 and a tail
                                            ; jmp to 00238A80 to rebind
```

**`02164280` is the static save-image buffer** — the one `U-5` identifies as
`SaveImage_GetActiveRuntimeBuffer()`'s return — and **`0x56690` is the whole image**: `0x200` header
plus `0x56490` payload, which is the buffer size this page states in §4. So the clear covers **every
byte of the header and the payload**, and all three spans fall inside it:

| span | payload | buffer-relative | inside `0x56690` |
|---|---|---|---|
| `unobservedSpan1538` | `+0x1538`–`+0x2000` | `+0x1738`–`+0x2200` | yes |
| `unobservedSpanC818` | `+0xC818`–`+0xE000` | `+0xCA18`–`+0xE200` | yes |
| `unobservedTail5589C` | `+0x5589C`–`+0x56490` | `+0x55A9C`–`+0x56690` | yes |

### What changes and what does not

**Unchanged:** nothing reads these bytes, and nothing writes them *individually*. The census stands.

**Added:** they have a **defined value and a lifetime**. Each clear sets the whole image to zero, so
the spans hold zero from that point until something writes them — and nothing observed does. A
reconstruction that allocated this buffer without zeroing it would differ from the engine in 12,
bytes that no test would catch, because nothing reads them *yet*.

**This is the third time today that `unreached` has turned out not to mean `untouched`**, after
`BattleUnit +0x298` (1,016 B inside a `0x610` `memset`) and the `ManagerSingleton` hole (23,224 B
inside a `0x10FD0` one). The pattern is now explicit enough to state as a rule: **a span with no
accessor should be swept for bulk writes before it is described, because the two questions have
different instruments and only one of them had been run.**

**NOT CLAIMED:** what the spans are *for*. Zero-initialisation is a lifetime fact, not a semantic
one, and these bytes remain unread on every route this database has. **Also not claimed:** that these two are the only
writers — the sweep covers `memset`/`memcpy` with a **literal** size, so a copy whose length is
computed at runtime is invisible to it.

> *The one loose end that raised is now resolved rather than left open.* `0063C910` holds the sweep's
> only two size-unresolved `memcpy` calls, and neither bears on this page: `0063C96D` takes its length
> from **`dword [r13 + 0x38]`** and `0063CACC` from **`rbp`** — both runtime values — and both write to a
> **register destination** (`rcx = rbx`), not to `savebuffer + disp`. Their source is an object field
> `[obj + 0xC0]`. They entered the sweep only by call-reachability from the save entry points, and
> **nothing ties either to the save image buffer at all.**

## V-1: the payload's residue by every entry route (2026-09-27, OPUS)

*The register still described this payload as ~470 bytes mapped. The type store has since tiled all 353,424
bytes, and the three spans above were tested from one route only (`census_savepayload.py`, the active getter).*

**The tiling, measured from `_types/fields.tsv`.** It closes at exactly `0x56490` with no gap, walked through
the embedded types and their arrays.

| confidence | bytes |
|---|--:|
| PROVEN | 335,460 |
| HIGH | 3,095 |
| PROBABLE | 916 |
| UNKNOWN | 13,953 |

**The top-level residue is reached by no route.** The census is seeded at every entry this page records:
- the getters `002EF640` / `002EF620` / `002EF630` (buffer base) and `002EF2B0` (payload base);
- the slots `02092758` (−0x200), `020927C0` (+0x8000) and `02EBF190` (+0x4E48C);
- rip-relative operands and `lea`s into all four image buffers.

Offsets are carried six hops into callees. The census touches none of the eight top-level UNKNOWN spans
(12,018 B): `+0x1538`, `+0xC818`, `+0xE004`, the four transition-record holes and `+0x5589C`.

Three more checks agree:
- The published access census (`save-payload-accesses.tsv`, 1,725 sites) has no row in them.
- No listed body carries a displacement in the tail's payload- or buffer-relative range, with any base.
- No census-reached body carries one in `+0xC818`'s range.

**Controls:**
- every documented region is reached;
- the `+0x1044` read is found;
- the whole-image clears `002EF5F0` / `002EF650` are found by their `lea 02164280`;
- a planted access at `+0xC900` is flagged;
- the raw sweep sees the known `lea rdx, [rax+0x4E68C]` at `00229B81`.

**Reading.** These bytes are reserved space in the sense `AA-5` accepted: zeroed by the whole-image clears,
carried with the image, and read by nothing in this executable. Their purpose is not derivable here.

**Still open: 1,935 B inside five embedded types.**
- `PersistentFlagPayload`, 814 B: the 778-byte script-global tail, AA-5's bank and AA-8's tail bytes.
- `BattleStatsRecord`, 15 B × 40 = 600 B.
- `ImageBackedStateBlock`, 274 B.
- `GambitConfig`, 160 B.
- `BattleSystemState`, 63 B.
- `SpawnKeepImage`, 12 B × 2.

**Not tracked:** indirect calls and index-register offsets. Control: `_index/candidates/v1-payload-residue/v1_residue_census.py`.

## SWE2-EC7-38 update (2026-09-19) - `00564010`

`00564010` (479 B) is a save-payload body - `0209AC30`/`01F44830`/`00567200`, `002432B0`/`00254A10`/`0029FB50`/`00564780`/`00244F50`/`00244960`. Interior anchor `00564049` (a `002432B0` call).

## SWE2-EC7-39 update (2026-09-19) - `00404730`

`00404730` (418 B) is the UI reader the page names - `01F44830`, `002551B0`/`003C4AE0`/`00861EC0`/`003C46B0`/`00808C40`. Interior anchor `00404809` (a `002551B0` call).

## SWE2-EC7-41 update (2026-09-19) - `00576550`

`00576550` (345 B) is a save-payload body - `02CA9738`, `003154B0`/`0037E780`/`0037F060`. Interior anchor `005765BF` (a `003154B0` call).

## SWE2-EC7-43 update (2026-09-19) - `00576920`

`00576920` (289 B) is a save-payload body - `02CA9738`, `003154B0`/`00315670`/`003156E0`/`0037F060`/`00576E30`. Interior anchor `0057697E` (a `003154B0` call).

## SWE2-EC7-45 update (2026-09-19) - `00576E30`

`00576E30` (243 B) is an event-memory callee - `00265270`/`00315420`/`00576860`. Interior anchor `00576E63` (a `00265270` call).

## SWE2-EC7-49 update (2026-09-19) - `00403F90`

`00403F90` (193 B) is a save-payload UI reader - `002551B0`/`003C4AE0`/`00861EC0`. Interior anchor `00403FB8` (a `002551B0` call).

## SWE2-EC7-50 update (2026-09-19) - `0035BB70`

`0035BB70` (181 B) is a save-payload memset-battery body - `002419B0`/`00244F00`/`002A27F0`/`00861EC0`. Interior anchor `0035BB85` (a `002419B0` call).

## SWE2-EC7-54 update (2026-09-19) - `003C46B0`

`003C46B0` (346 B) is a save-payload field body - `00203170`/`003977B0`/`003985B0`/`00398C50`/`003C6420`/`00808C40` plus `00915FE4`/`01CEBB70`/`01CEBDA0` rdata. Interior anchor `003C46E2` (a `00203170` call).

## SWE2-EC7-55 update (2026-09-19) - `003C6420`

`003C6420` (1864 B) is a save-payload field marshal - `01F44830` cookie, `00202C70`/`00397910` plus the `00180E50`-`00181910` accessor family, `0024AD00`/`00255150`. Interior anchor `003C64FB` (a `00202C70` call).


## SWE2-EC7-55 update (2026-09-19) - `0037E780`

`0037E780` (274 B) is a save-payload body - `0046B1A0`/`0046B240`. Interior anchor `0037E82F` (a `0046B1A0` call).

## SWE2-EC7-56 update (2026-09-19) - `0037F060`

`0037F060` (200 B) is a save-payload body - `0046B1A0`/`0046B240`. Interior anchor `0037F0D9` (a `0046B1A0` call).

## SWE2-EC7-58 update (2026-09-19) - `003F8A90`

`003F8A90` (169 B) is an indirect-only linked-node teardown - `call rax` deleter on `[rbx+0x38]` then `+0x28`/`+0x30` sibling relink and null. Interior anchor `003F8AC7` (the `call rax` deleter).

## SWE2-EC7-62 update (2026-09-19) - `002419B0`

`002419B0` (146 B) is a save-payload body - `00244DD0`/`00245020`/`002CCC30` plus `00915058`/`0208EA68` and one vcall. Interior anchor `002419D4` (a `002CCC30` call).


## SWE2-EC7-86 update (2026-09-20) - `003C4AE0` defaulting index lookup measured

`003C4AE0` (50 B) is the count-then-lookup the save-layout callers
run: `00264790` returns a count; `<= 0` yields the global default
`[02B45A50]`; otherwise `002551B0(0, count)` resolves the record and
`cmove` folds a null result back to the same default - a get-or-
default over the `02B45A50` table.
Interior anchor `003C4AF9` (the `002551B0` resolve arm).

## SWE2-EC7-102 update (2026-09-20) - `00293CE0` measured

`00293CE0` (295 B) is the bitmask-driven table fill
`00293310`, `00293FE0` and `00294B50` call: `dl == 0`
early-outs with `[r9]` written back and the stack
argument returned. Otherwise slot `rdi = movsxd
dword[r9]` takes `002F9860(0x2328)` when the
`00254A10`/`00264150` quiet pair passes and the
`rbp` stack flag is set (`rbx` otherwise); an
8-iteration `rol ebx` loop then fills
`[r15 + edi*8]` with `002F9860(esi + 0x4B27)` for
each bit set in `r14b`; the quiet pair is re-checked
and a trailing slot takes `rsp+0x60`, or
`002AC290()` when `rsp+0x78 == 0`; `[r13]` gets the
final `edi` count and the return is `rbp + 1` - the
bit-selected row-list composer the save-payload
walks run.
Interior anchor `00293D65` (the `0x4B27`-relative
`002F9860` call).

`0057D5E0` (31 B) is the byte-table read `00564780`'s save-pane body calls twice: returns `byte[0xD23D60 + edx]` — the `test ecx,ecx` tests the just-loaded `0x120000` image-base constant rather than the first argument, so the `+0xC03D6C` arm is unreachable folded code and the function is an unconditional table index.

Interior anchor `0057D5ED` (function `0057D5E0`).

`00578F50` (373 B) is the `005789D0`-family field pack into `[02CA9748]`: returns 0 when `0037ED80()` reports 2; else copies `[src+0xC0]` -> `+0x130`, zeroes `+0x134`, stores `[src+0xC4]` at `+0x138` and repacks the `+0x138` dword (btr 8; `(src+0xC4==0)` << 8; masks `0xFFFFF9FF`/`0xFFF807FF`; `[src+0xC8]` << 0xB); three identical margin computes `(f4+f2)*ec + ee + ed` off `[src+0x190]`/`[+0x188]`/`[+0x118]`'s `+0xD8` records land at `+0x13C`/`+0x13D`/`+0x13F`, `+0x13E` takes `[+0x128]`'s `+0xC1` (or `0xFF` when absent), and bit 3 of the global's `+0xD0` is set — returns 1.

Interior anchor `00578FA3` (function `00578F50`).

`00578920` (163 B) is the `005789D0` lazy-install `00579420`/`00579AF0` run: only when `[02CA9748]+0x120` is null it `00244F50(0x1A8, 005789D0, &ctx)`s with the four argument bytes packed into the context, and the created object is stored into `+0x120` — a once-only registration of the tab-6 handler.

Interior anchor `0057899E` (function `00578920`).

`00578860` (189 B) is the two-slot select inside the `005789D0` pane: `002470C0` runs on `[[this + [this+0xC8]*8 + 0x188]]` first, then both `+0x188` entries are looped — `00247870(entry, i == edx)` arms the chosen one, which alone also gets `002470D0(entry)`; when `+0xC4` mode is not 1, `00394850(this, 0, 1, {0, edx+1})` notifies and `[this+0xC8] = dl` is stored — pick-one-of-two with a mode-gated announce.

Interior anchor `005788B3` (function `00578860`).

`005780D0` (80 B) is the `[02CA9748]+0x128` setter `00579420`/`00579AF0` share: writes `cl` into the object's `+0xC1` byte, then `00577C30(byte[+0xC0], obj+0x50, cl, 00D23888, [obj+0xC8])` fires the change notify — silent when the `+0x128` object is absent.

Interior anchor `00578116` (function `005780D0`).

`00577A40` (399 B) is the `02CA9738` `+0x110` nibble-bank adjust `00574900` runs: requires the record's `+0xC9` byte == 1 and its `+0xF0` table live; word `+0xCE` is bounds-checked against `[tbl+8]`/`[tbl+0xA]` and resolves entry `tbl + u16[tbl+idx*2+0x12]`; arg `ecx` must be under the entry's `[+0]` count, then `rdx + dword[ent+ecx*4+4]` gives the op list; for each of its `[+2]` stride-4 rows the op byte dispatches — 0: clamp arg1 to `[0,0xF]`; 1: `00315A20(arg0, arg1==1)`; 2: `00315470(arg0)` then `arg0+arg1` capped at `0xF`; 3: `00315470(arg0)` then `arg0-arg1` floored at 0 — the last three through `00315CD0`; returns 1 on a resolved list, 0 on any failed gate.

Interior anchor `00577B2F` (function `00577A40`).

`00577C30` (475 B) is the five-widget refresh `005780D0` fires when the `+0x128` object changes: `ecx` maps 0/1/2 -> 0/1/2 else `0xFF`, then `0037EAA0(r8d, mapped)` -> `0037E5B0(result, &rec)` resolves the record. The `rec[+0x3F] == 1` path derives the flag from `0037EE10(rec[+0x38]) >= rec[+0x3E]`; otherwise `0046B1A0(rec[+0x38]) != 0`. Widget `[r9+0]` gets `[+0x18]` = `args[min(rec[+0x3A]/3 + flag, 5)]` (the `0xAAAAAAAB` divide) and `[+0xA]` = `rec[+0x3A]`'s mod-3 remainder; `rec[+0x40]` formats `"q_img_c%03d"` through `0017D2E0`. The `[r9+8]` widget takes the record pointer at `[+0x18]` with `0020E620` -> `[+0x20]`; the `[r9+0xC]` widget takes `0037EB70`/`0020E620` the same way; `[r9+0x10]`'s `+8` bit 0 mirrors `0046B1A0(rec[+0x38])`; and when `ecx == 1` the `[r9+0x14]` widget's `+8` bit 0 is `00576D20(6, rec[+0x3C])`.

Interior anchor `00577CD2` (function `00577C30`).

`003C37B0` (2011 B) is the two-arm emitter `003C4070` runs: `0035D320` fetches the object twice, `esi = [[rax+0x18]+8]` and `r14d = [02B45970]` pick the arm - nonzero `r14d` runs `00248EB0`/`00398C50`/`00248F40`/`002DD350` then the `00181560`/`001816B0`/`00181910`/`00181870`/`00181930`/`001817A0` battery and `003C81B0` under `0x10000000`/`0x6C108000`/`0x1000000000000011` tags, else nonzero `esi` runs the `00248EB0`/`003588B0`/`00265020`/`00202B70`/`00203170` x4 arm - the paired save/map draw.

Interior anchor `003C37DA` (function `003C37B0`).

`003C81B0` (1212 B) is the mode-switched emit helper `003C37B0` runs: `ecx` selects the arm, `00203170`/`00398C50` pairs run per arm, then `00202D70`, `00203080`, `00248F40`, `00202FE0`, `00202B10` with `00202B70` x6, `00202CA0` x6, `00202C90` x2 and `00181460`/`00181330` - the tagged stream's per-mode emit.

Interior anchor `003C825D` (function `003C81B0`).

`003C29A0` (1208 B) is the fetch-and-format helper `003C4070` runs: `[rdx]` nonzero gates, `0035D320` x3 fetches, `003588B0` x2, `00272DE0`, `0035D3D0`, `00265020` x2, `00202B70` x2, `00862930`, `00265200` x2, `002D8D10` x2 and `00861F0E` - the save/map draw's preparation body.

Interior anchor `003C29D7` (function `003C29A0`).

`00403640` (809 B) is the map reader `00403970` calls: `00808F10`, `00404230`, `00861F0E` x2, `004048E0`, `00202C70` x2, `003C3F90`, `00203170`, `003977B0`, `003C4980` and `003C4970` run the draw under the cookie check - the save-screen map's inner pass.

Interior anchor `0040365A` (function `00403640`).

`003C34E0` (709 B) is the map reader `003C4070` calls: `00264AC0`, `00202D70`, `003C6140`, `002649B0` x2, `002648F0` x2, `003C7B30` x2, `003C2870` x2, `003C6270` and `00181330` run the slot's emit under the cookie check - the save-map's paired-helper stage.

Interior anchor `003C350B` (function `003C34E0`).

`00264AC0` (26 B) is the slot-count reader `003C34E0` calls (the settings-command and per-frame gate paths share it): `00264AE0` returns the table, `dword[rax]` is the count - the `00264xxx` family's one-call accessor.

Interior anchor `00264AC4` (function `00264AC0`).

`002649B0` (130 B) is the record accessor `003C34E0` and `003C7B30` call (the settings/gate paths share it): `00264AE0` table, `edx < dword[rax]` bounds, stride 0x20, `ecx <= 1` gates on a `byte[+0x2C]` bit-test through `00377860` - the gated element pointer.

Interior anchor `002649C4` (function `002649B0`).

`002648F0` (42 B) is the record initializer `003C34E0` and `003C7B30` call (the settings/gate paths share it): writes `word[+1]` = 0x0101, `byte[0]` = 1, `byte[+3]` = 1, `word[+4]` = 0xFFFF into `rdx`, then `byte[rcx+0x1D]` feeds the `00264920` tail - the 6-byte seed-and-continue.

Interior anchor `00264912` (function `002648F0`).

`003C7B30` (877 B) is the channel-lerp stage `003C34E0` calls: `word[rcx+0x5A]`/`+0x58` scale each byte of the colour record `>>7`, half-way deltas go through `cvtdq2ps`/`mulss`/`cvttss2si` into stack pairs, then `002649B0`/`002648F0` seed the slot and `00202B70`/`00202CF0`/`00181350` finish under the cookie check - the save-map's colour interpolate.

Interior anchor `003C7CF4` (function `003C7B30`).

`00264AE0` (106 B) is the counted-slot getter `002649B0` and `00264AC0` call (the settings arm `003F9720` shares the family): `02098E20` bit 0 gates, `02098E10`'s table + `dword[+0x70]` resolves through `0020E600`, `dword[rcx]` bounds `edi`, and `dword[rcx + rdi*4 + 4]` + `rbx` is the element pointer - the `00264xxx` family's index root.

Interior anchor `00264B06` (function `00264AE0`).

`00264920` (137 B) is the record packer `002648F0`'s tail calls (the settings arm `003F9720` reaches it too): `00264870` looks the record up, `0037C860`/`0037C8F0` pick `word[+8]`/`+6`/`+4`, then five `0032A8A0` byte-stores fill `rdi` (`+2`, `+0`, `+1`, `+3`) and `word[+0xA]` lands at `word[+4]` - the 6-byte payload assembler.

Interior anchor `0026495C` (function `00264920`).

`00309480` (615 B) is the candidate-kind evaluator `0030A4E0` calls: four `movzx` words (`r8w`, `r9w`, `[rsp+0x70]`, `[rsp+0x78]`) each go through `0031EA90`, `[rsp+0x50]`/`esi`/`edi` dispatch the returned kinds to `003096F0(r14w, r15w)` or `0020E600` - the loadout's class-pair resolver.

Interior anchor `00309527` (function `00309480`).

`0024AD00` (577 B) is the call-free accumulate `003C6420` (and `00249080`/`00249110`) call: `rdx`'s 64-byte block publishes to `022D92E0`..`022D9310`, `rcx`/`r8`/`rax` land in `022D8F90`/`022D8FA0`/`022D8FB0`, then the `r9d`-counted loop runs `shufps`/`mulps`/`mulss` over `r8`'s 0x10-stride rows - the payload's matrix fold.

Interior anchor `0024AD7F` (function `0024AD00`).

`003096F0` (475 B) is the range resolver `00309480` calls: `00322C50(ecx=6)` gates, then `02EBF0F8`'s record resolves twice through `0020E600` and `(cx - 0x1000) * word[+8] + eax` forms the offset - the payload map's indexed-range computation.

Interior anchor `00309706` (function `003096F0`).

`0037E8D0` (451 B) is the record matcher `005789D0` calls: `02AED490`'s `+0xC8` table, `word[+0xE8] < word[r9+0xA]` bounds, `byte[+0xEE]` counts a `0x18`-stride scan of `+0xF0` records matching `byte[+1] == 2 && byte[+2] == r8b`, then `00473B90`/`002F9920`/`0037EF70`/`0037EFC0` act on the hit - the payload map's keyed record find.

Interior anchor `0037E9B7` (function `0037E8D0`).

`0037EE10` (338 B) is the id lookup `00577C30` calls: `[02AED490 + 0xC8]` table, `word[r10 + 0xA]` entries at `+0x10` stride 8, `(dword >> 8) & 0x3FF == edi` is the match, `0046B180` finishes - the payload's 10-bit key scan.

Interior anchor `0037EF14` (function `0037EE10`).

`003C4810` (337 B) is the bit writer `003C6420` calls: `ecx` splits `cdq`/`& 0x3F` into slot and bit, `r13`/`r14` are the two out pointers zeroed first, `00255150` resolves the field - the payload's bitfield store.

Interior anchor `003C48AD` (function `003C4810`).

`003C2870` (301 B) is the tagged-record emit `003C34E0` calls on `[rcx+0x10]`'s write cursor: five 16-byte stores - `0x10000000`/`0x6C038100`, `0x3040C00000000001`/`0x1EE`, `[rbx+0x80]`/`0x47`, `[rbx+0x78]`/`0x42`, then the `r9+0x10` block takes `0x10000000`, `(r8-4-words)<<0x10 | 0x6C008000`, `edx` and `4` with `xmm2` at `+0x24` - the payload's fixed-tag section writer.

Interior anchor `003C294A` (function `003C2870`).

`001817A0` (37 B) is the xmm forwarding thunk `003C2870` calls: `xmm0` saves into `xmm6`, `001B1C00` runs, its return becomes `rcx`, `xmm1` restores from `xmm6`, and the tail jumps into `001B1FE0` - the two-call float hand-off the tagged-section writer borrows.

Interior anchor `001817C0` (function `001817A0`).

`002AB870` (115 B) is the packed field writer the save-payload builders call: `ecx < 8` returns 0, else `word[rdx] = 0x290F` tags the slot and `r8d`'s bits spread into bytes 2..7 - byte 6 gets `(r8d >> 0x18) | 0x80`, byte 5 `(r8d >> 0x10) | 0x80`, byte 4 `(r8d >> 8) | 0x80`, byte 3 `r8b | 0x80`, and byte 2 assembles the four stray flag bits (`r8d >> 0x1F`, `>> 0x17`, `>> 0xF`, `>> 7`, each `& 1`) shifted into `| 0x84`; byte 7 zeroes and 8 returns - the 8-byte tagged record encoder.

Interior anchor `002AB878` (function `002AB870`).

`00253240` (522 B) is the slot-descriptor table fill: `ecx` bounds to `<= 0xB` (out-of-range runs `0016D6A0(0x200)` and re-reads as `edi`), `rbx = 02092760 + idx*8` gets `dword[+4]` = `0020E620(adjusted base)` and `word[+2]` = the case tag via the `002532BF` jump table (0x40/0xC8/0x8C/0x30/0x20/0x28/0x100/0x18/0x51/0x200 variants, each adding 0x80..0xAEA to the `020927C0`-rooted `+0x38CC` base), and with `edx` set the `020927C0`-indexed row `r14` gets `dword[+0x47B8] = 0` and its `0020E600(dword[+4])`-resolved word buffer 0xFFFF-filled to `word[+2]` entries.

Interior anchor `002532CA` (function `00253240`).

`00295FE0` (200 B) is the save-table row search: the `02EBF038` descriptor supplies `+4` count, `+8` row stride and `+0xC` base through `0020E600`; each row's `0035D330(0x19, i)` record is skipped when `byte[+0x23]` is set, otherwise the row's eight-word array at `+8` scans for `esi` and a hit returns `002B58B0(qword[row+0x18])` - the occupied-flag-gated lookup the two save-payload builders share.

Interior anchor `00296061` (function `00295FE0`).

`002CD650` (345 B) is the config-slot reconciliation pass: for each slot in the fixed order 1,3,2,8,5,4,7,6 the body asks `00252D10(slot)` whether it is already set; when clear, a paired count probe over a neighbouring slot (`00252FA0` for most pairs, `00252FF0(0xA)` for slot 7) decides whether `00252D40(slot, 1)` fires - the post-load latch fix-up the save-payload and layout callers run.

Interior anchor `002CD6D2` (function `002CD650`).


`005781A0` (360 B) is the chain-counter `005789D0` runs before laying out a field group: arg3 selects the head - `1` walks `[r9+0x18]` but only after `0046B1A0` accepts `[r9]`'s type word, `0` walks `[r9+0x28]` directly - and each hop chases the link with `002B39A0` at kind 2, re-probing at kind 3 when the result equals its input (an end-of-line marker convention), counting live nodes; it then reserves `count*8 + 0x100` bytes through `00244F50` with the local helper `00578450` and delivers the block through the caller's out-pointer.

Interior anchor `00578262` (function `005781A0`).

`00252FF0` (240 B) is the kind-scoped entry count `002CD650` runs: kind above `0xB` hits `0016D6A0(0x200)` and returns 0; it reads the count at `020927C0[kind*4]+0x47B8` (0 returns 0); and for kind `0xA` resolves `02092764[kind*8]` through `0020E600` and counts u16 entries whose `+0x8000`-biased value wraps to `<=0x3F` - a range filter over the row's id list

Interior anchor `00253084` (function `00252FF0`).

`003C6270` (232 B) is the packed-quad emitter `003C34E0` runs: it expands the record's `+0x5A`/`+0x58` i16 pair into fixed-point channels (`a*0xFF >> 7`, `a >> 2`, `0`, `b` for row one; `a*0xFF >> 7`, `a*3 >> 1`, `a >> 1`, `b` for row two, all `>>7`-scaled), calls `00248EB0`, then advances `[rbp+0x10]` by `0x30`, writes the first u32x4 row, advances `0x10`, and writes the second - two u32x4 colour rows into the output stream

Interior anchor `003C6300` (function `003C6270`).

`003DF5B0` (187 B) is the lane reset `002628B0` runs before marshalling: it sets `02B59D10 = 1`, clears `02B59D18`, and zeroes all 24 lane pointers `02B59C48`..`02B59CF8` at 8-byte stride - the empty state the save-image field lanes start from before any field is staged

Interior anchor `003DF5B2` (function `003DF5B0`).
