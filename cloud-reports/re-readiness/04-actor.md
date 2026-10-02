# Reconstruction readiness — `FFXII TZA/04-Actor-Entity/`

| | |
|---|---|
| Stream | R (reconstruction readiness), per [`docs/cloud-briefs/re-readiness.md`](../../docs/cloud-briefs/re-readiness.md) |
| Board task | `OPUS-CLOUD-R-READINESS-04-1002` |
| Date | 2026-10-02 |
| Snapshot | this repo's text snapshot only (`df2c9f47`); no executable, Ghidra or live game was used. Several 04 pages are being edited by other lanes; every quotation is the text **as the snapshot has it** |
| Status of this file | **draft / pointer**. Nothing here is evidence. Every item is a quotation or a paraphrase of a page, with its location. |

**Counts:** *(filled in when the report is complete)*

Citation form: `page:line`, where `page` is the path inside `FFXII TZA/04-Actor-Entity/`. The paths are given in full
every time. "Not stated" means none of the 04 pages says it. Where only another category's page makes a point, the
pointer is given as a path from `FFXII TZA/`, but that page was not audited for this report.

## Pages read

All 18 `.md` pages were read in full (17 system pages plus `README.md`; 16,027 lines). Member `.tsv` files were opened
only for their header and row count.

| page | status as the page states it |
|---|---|
| `README.md` | category index; "Functions \| 235" (`README.md:8`); per-page banners at `README.md:14`, `:21`, `:28`, `:34`, `:39`, `:44`, `:50` (see §3.2, B-1) |
| `Actor-Storage-Record/the-record-behind-every-actor.md` (2,967 lines) | `status: AUDITED` (`Actor-Storage-Record/the-record-behind-every-actor.md:4`); `readiness: SIGNATURE RESOLVED` (`Actor-Storage-Record/the-record-behind-every-actor.md:8`); `confidence: PROVEN` (`Actor-Storage-Record/the-record-behind-every-actor.md:9`); `last_reviewed: 2026-09-08` (`Actor-Storage-Record/the-record-behind-every-actor.md:15`); body verdict "**Not reconstruction-ready**" (`Actor-Storage-Record/the-record-behind-every-actor.md:2218`) |
| `Actor-Storage-Record/the-actor-storage-record-field-map.md` (531) | `status: AUDITED` (`Actor-Storage-Record/the-actor-storage-record-field-map.md:4`); `readiness: BEHAVIORALLY UNDERSTOOD` (`Actor-Storage-Record/the-actor-storage-record-field-map.md:8`); `last_reviewed: 2026-09-10` (`Actor-Storage-Record/the-actor-storage-record-field-map.md:17`) |
| `CONTRACT-actor-storage-record-initialisation.md` (249) | `readiness: CONTRACT READY` (`CONTRACT-actor-storage-record-initialisation.md:6`); `confidence: PROVEN` (`CONTRACT-actor-storage-record-initialisation.md:7`); `last_reviewed: 2026-09-29` (`CONTRACT-actor-storage-record-initialisation.md:18`); no `status:` key |
| `CONTRACT-actor-record-pool-and-region-map.md` (833) | `readiness: BEHAVIORALLY UNDERSTOOD` (`CONTRACT-actor-record-pool-and-region-map.md:6`); `confidence: PROVEN` (`CONTRACT-actor-record-pool-and-region-map.md:7`); `last_reviewed: 2026-09-11` (`CONTRACT-actor-record-pool-and-region-map.md:17`); no `status:` key |
| `the-definition-record-flag-pair.md` (410) | `status: AUDITED — the flag pair, its writers and its 125 guard sites read; …` (`the-definition-record-flag-pair.md:4`); `last_reviewed: 2026-09-06` (`the-definition-record-flag-pair.md:19`) |
| `Battle-Unit/the-battle-unit-field-map.md` (1,917) | `status: AUDITED` (`Battle-Unit/the-battle-unit-field-map.md:4`); `readiness: BEHAVIORALLY UNDERSTOOD` (`Battle-Unit/the-battle-unit-field-map.md:8`); `last_reviewed: 2026-09-12` (`Battle-Unit/the-battle-unit-field-map.md:23`) |
| `battleunit-slot-pool-and-actor-class.md` (831) | `status: AUDITED` (`battleunit-slot-pool-and-actor-class.md:4`); no `readiness:`/`confidence:`; `last_reviewed: 2026-09-02` (`battleunit-slot-pool-and-actor-class.md:18`); `reopened_count: 1` (`battleunit-slot-pool-and-actor-class.md:26`) |
| `Unit-Definition/CONTRACT-battle-unit-construction.md` (443) | `readiness: BEHAVIORALLY UNDERSTOOD` (`Unit-Definition/CONTRACT-battle-unit-construction.md:6`); `confidence: PROVEN` (`Unit-Definition/CONTRACT-battle-unit-construction.md:7`); `review_status: "Production correction; T2 peer review and canonical acceptance remain pending."` (`Unit-Definition/CONTRACT-battle-unit-construction.md:14`) |
| `Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md` (958) | `status: DOCUMENTED` (`Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md:4`); `last_reviewed: 2026-09-22` (`Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md:16`) |
| `Unit-Display-Record/the-record-00329220-builds.md` (533) | `status: AUDITED` (`Unit-Display-Record/the-record-00329220-builds.md:4`); `last_reviewed: 2026-09-10` (`Unit-Display-Record/the-record-00329220-builds.md:15`) |
| `Battle-Record-Kind/actor-type-id-partition-and-the-13-value-band.md` (427) | `status: AUDITED` (`Battle-Record-Kind/actor-type-id-partition-and-the-13-value-band.md:4`); `last_reviewed: 2026-09-03` (`Battle-Record-Kind/actor-type-id-partition-and-the-13-value-band.md:19`) |
| `Battle-Record-Kind/battle-record-kind-byte.md` (965) | `status: DOCUMENTED — what the kind byte means answered 2026-09-10 …` (`Battle-Record-Kind/battle-record-kind-byte.md:4`); body banner "**PARTIAL — deliberately.**" (`Battle-Record-Kind/battle-record-kind-byte.md:32`) |
| `Actor-Names/the-npc-name-dictionary.md` (710) | `status: AUDITED` (`Actor-Names/the-npc-name-dictionary.md:4`); `confidence: PROVEN` (`Actor-Names/the-npc-name-dictionary.md:9`) |
| `Actor-Manager-Record/the-actor-manager-record-field-map.md` (1,046) | `status: AUDITED` (`Actor-Manager-Record/the-actor-manager-record-field-map.md:4`); `readiness: BEHAVIORALLY UNDERSTOOD` (`Actor-Manager-Record/the-actor-manager-record-field-map.md:8`) |
| `CONTRACT-manager-slot-entry-tables.md` (645) | `readiness: BEHAVIORALLY UNDERSTOOD` (`CONTRACT-manager-slot-entry-tables.md:6`); evidence row "any runtime observation \| **none exists** \| none \| UNKNOWN" (`CONTRACT-manager-slot-entry-tables.md:507`) |
| `Actor-Contexts/the-movement-and-secondary-context-censuses.md` (567) | `status: AUDITED — the secondary context's entryId (FS-2 …) and the movement context's +0x10C..+0x21F (UQ-91 …) answered 2026-09-17` (`Actor-Contexts/the-movement-and-secondary-context-censuses.md:4`); `readiness: PARTIALLY UNDERSTOOD` (`Actor-Contexts/the-movement-and-secondary-context-censuses.md:8`) |
| `the-field-runtime-pass.md` (1,028) | `status: DOCUMENTED — the SECTION-12 wait-completion polarity correction …` (`the-field-runtime-pass.md:4`); `last_reviewed: 2026-09-03` (`the-field-runtime-pass.md:19`); `audit.last_pass: 2026-10-01` (`the-field-runtime-pass.md:22`) |
| `CONTRACT-field-runtime-pass.md` (879) | `readiness: CONTRACT READY` (`CONTRACT-field-runtime-pass.md:6`); `confidence: PROVEN` (`CONTRACT-field-runtime-pass.md:7`); closing "No full-system L2 or formal acceptance is awarded here." (`CONTRACT-field-runtime-pass.md:879`) |

`.tsv` files checked (data rows = lines − 1):

| file | rows | agrees with the page? |
|---|---:|---|
| `Actor-Storage-Record/actor-storage-record-accesses.tsv` | 1,130 (271 functions, 111 displacements) | no: `Actor-Storage-Record/the-actor-storage-record-field-map.md:53-55` states 1042 rows / 275 functions / 86 offsets (C-V12) |
| `Actor-Storage-Record/actor-record-offsets-observed.tsv` | 56 (highest offset `0x118`) | no: `Actor-Storage-Record/the-record-behind-every-actor.md:1512` says "all 70 offsets"; `Actor-Storage-Record/the-record-behind-every-actor.md:1540-1541` says the eight beyond `0x118` "are recorded in the TSV" (C-V13) |
| `Actor-Storage-Record/actor-storage-record-flags1c-initial-values.tsv` | 8 sequence rows + 1 comment | yes: matches the presets at `Actor-Storage-Record/the-record-behind-every-actor.md:309-311` and `Actor-Storage-Record/the-actor-storage-record-field-map.md:117` |
| `Actor-Storage-Record/actor-storage-record-flag-bit-writes.tsv` | 121,759 | yes: `Actor-Storage-Record/the-actor-storage-record-field-map.md:208` |
| `Actor-Storage-Record/actor-storage-record-flag-bits.tsv`, `actor-arg-proven-closure.tsv`, `actor-static-proven-bases.tsv`, `actor-resource-entry-accesses.tsv`, `actor-wait-slot-accesses.tsv`, `actor-sequence-descriptor-accesses.tsv`, `actor-definition-payload-accesses.tsv` | 88 / 251 / 48 / 82 / 14 / 3 / 7 | layout only; the wait-slot file has none of `0025DF00`'s `+0x14`/`+0x27` stores that `the-field-runtime-pass.md:741` lists (S-20) |
| `Battle-Unit/battle-unit-accesses.tsv` | 2,205 (345 functions) | no: `Battle-Unit/the-battle-unit-field-map.md:59-61` states 2203 rows / 342 functions; `Battle-Unit/the-battle-unit-field-map.md:643` "the committed 2,207 in 344" (C-V15) |
| `Battle-Unit/battle-target-buffer-accesses.tsv`, `battle-target-result-entry-accesses.tsv`, `navigation-path-state-accesses.tsv` | 68 / 4 / 14 | no count stated on any page |
| `Actor-Manager-Record/actor-manager-record-accesses.tsv` | 204 | no: `Actor-Manager-Record/the-actor-manager-record-field-map.md:409` "holds **194** rows today" (C-V16) |
| `Actor-Manager-Record/actor-manager-record-rip-accesses.tsv`, `actor-manager-slot-accesses.tsv`, `actor-manager-slot-entry-accesses.tsv` | 113 / 330 / 26 | not cited by any page; `Actor-Manager-Record/the-actor-manager-record-field-map.md:55` gives the array route as "51 / 31 / 17" |
| `Actor-Contexts/movement-context-accesses.tsv` | 708 (124 displacements, no `chain:0xB8` rows) | no: `Actor-Contexts/the-movement-and-secondary-context-censuses.md:19-20` "1,028 rows, 122 distinct displacements; chain-only rows carry route `chain:0xB8`" (C-V16) |
| `Actor-Contexts/secondary-context-accesses.tsv` | 309 (91 functions, 43 displacements) | no: `Actor-Contexts/the-movement-and-secondary-context-censuses.md:214` "302 accesses, 89 functions, 40 offsets" |
| `Actor-Contexts/movement-context-proven-bases.tsv`, `secondary-context-element-accesses.tsv` | 68 / 176 | not cited |
| `field-pending-request-cells-022c8030-accesses.tsv` | 8 | layout only; no count stated |

No item below rests on a `.tsv` alone.

---

## 1. Interface

The category holds five objects and one per-frame driver:

- **`ActorStorageRecord`**, the field actor ("the record behind every actor"). It is carved from one pool per manager
  slot and holds the script VM state, the wait slots, the resource-entry lists and two embedded contexts.
- **`ActorManagerSlot`**, five 648-byte slots at `02098E10`. A slot owns a record pool, the bound definition payload,
  the script variable banks and the camera-shot and camera-shake entry tables.
- **`BattleUnit`**, the 3,920-byte combatant, from a fixed pool of 32. It is bound to an actor record and built from a
  definition id.
- **`BattleStatsRecord`** (`0x1C8`). The kind byte at `+5` selects the party or the enemy definition table.
- **`StatusView`** (`0xC0`), a per-call UI snapshot of a party member.
- **The field runtime pass** `0025D9E0`. It drives one manager slot's actors for one frame through the wait resolver
  `0025DF00`.

The NPC name dictionary (`npcdic.bin`) is a side table that the actor's `+0x102` id indexes.

### 1.1 Entry points (functions, with their callers)

#### Record pool and actor record construction

| entry | callers | what it does | cite |
|---|---|---|---|
| `ActorSystem_InitializeManagerRuntime` `0026CE60` | `0025BFB0`, `0032F1B0` | calls the allocator; installs `manager+0x08` (`0026CEB8`) | `Actor-Storage-Record/the-record-behind-every-actor.md:1368`, `:2331` |
| `ActorStorage_AllocateAndInitializeRecords` `002679F0` (436 B) | `0026CE60` | sizes the pool from the per-sequence table `01E0C328`, allocates through `qword [r15+0x88]` (`00267A79`), `memset`s it, writes the count and the pointer table, stamps `+0x03`, prefix-sums the per-kind counters, then calls the initialiser on every record | `Actor-Storage-Record/the-record-behind-every-actor.md:1367-1407`, `:1283-1287`; `CONTRACT-actor-record-pool-and-region-map.md:102-132` |
| `ActorStorage_InitializeRecord` `00266530` (1,439 B) | "exactly one": `002679F0` at `00267B79` | initialises one record: masks, constants, slot index at `002665EB`, calls `00266AD0`, `00266BD0`, `003DB580`, `0020E600` ×7, `003DBB60` ×4; `rep stosw` `0xFFFF` over `+0xC8`–`+0xEB` at `002668B0` | `Actor-Storage-Record/the-record-behind-every-actor.md:92-98`, `:109`, `:162-165`, `:1272`; `CONTRACT-actor-storage-record-initialisation.md:45-48`, `:86`; `CONTRACT-actor-record-pool-and-region-map.md:294-295` |
| region map `00266AD0` (211 B) | `00266530` | switch on `rec[3] & 0x1F` (jump table `00266BA4`); plants `+0xB8`, `+0xC0`, `+0xA0`, `+0xA8` | `CONTRACT-actor-record-pool-and-region-map.md:134-145`; `Actor-Storage-Record/the-record-behind-every-actor.md:1599-1613` |
| per-sequence preset `00266BD0` (96 B) | `00266530` at `002665B1` only | jump table `00266C30` on `byte[+3] & 0x1F`: whole-word `+0x1C` presets; `+0x14` bit 7 for rows 5 and 7 | `Actor-Storage-Record/the-record-behind-every-actor.md:306-311`, `:1189` |
| `003DB580` (183 B) | `00266530` at `002667D7` | writes `+0x88`, `+0x89`, `+0x24`, `+0x60 = 0xFF00`; builds the `+0xA0` free list (stride `0x14`) | `Actor-Storage-Record/the-record-behind-every-actor.md:1617-1628`; `CONTRACT-actor-storage-record-initialisation.md:94-96`; `CONTRACT-actor-record-pool-and-region-map.md:610-612` |
| `00268EA0` (439 B) | nine callers | arms the `+0x118` countdown | `Actor-Storage-Record/the-record-behind-every-actor.md:165`, `:1313-1316` |
| `ImageAddress_ResolveRuntimePointer` `0020E600` (10 B) | the initialiser ×7 | `mov eax, ecx / add rax, [01F83530] / ret`; its encode pair is `0020E620` | `Actor-Storage-Record/the-record-behind-every-actor.md:163`, `:1921-1927` |
| `ActorResource_SubmitRequestDescriptor` `003DBB60` (120 B) | the initialiser ×4 | builds a 9-byte descriptor and submits it to `003DBCF0` | `Actor-Storage-Record/the-record-behind-every-actor.md:164`, `:2961-2966` |
| unload `002628B0` | `0032FCF6`, `0025BFB0` (`0025C036`) | phase 1 `ActorSystem_ReleaseManagerRecords` `0025B070`; phase 2 releases the pool at `00262D9F` via `003697F0` | `Actor-Storage-Record/the-record-behind-every-actor.md:2279-2295`, `:2319-2328`; `Actor-Manager-Record/the-actor-manager-record-field-map.md:345` |

#### Manager slot

| entry | callers | what it does | cite |
|---|---|---|---|
| `ActorManager_BindLoadedDefinitionPayload` `0026C8C0` (1,330 B) | `ActorResource_OnDefinitionPayloadLoaded` (`0032F966`) | `rdi = 02098E10 + slot × 0x288`, stored to `02099D70`; zeroes `+0x244`–`+0x27C`; clears `+0x200` bit 2; writes `+0x28` and `+0x00`; fills `+0x50/+0x58/+0x60/+0x68`, then `+0x70/+0x80/+0x78/+0x98` | `Actor-Manager-Record/the-actor-manager-record-field-map.md:73-79`, `:330-334`; `CONTRACT-actor-record-pool-and-region-map.md:593-605` |
| `ActorManager_GetRecordByOrdinal` `00358940` (30 B) | 75 callers | `pool = [manager+0x08]`; fails closed; returns `qword[pool + 8 + ordinal*8]` | `Actor-Storage-Record/the-record-behind-every-actor.md:257-258`, `:2336-2340`; `the-field-runtime-pass.md:257` |
| `00263FF0(m)` | 93 callers | `02098E10 + m × 0x288` | `CONTRACT-field-runtime-pass.md:455`; `battleunit-slot-pool-and-actor-class.md:517` |
| camera-shot side A: bind `003DA400`, reset `003DA370`, clear `003DA4D0`, republish `003DA570`, rate `003DA2D0`, tick `003DA050` | script verbs `camerastart_7d`/`_7e`, `resumebehindcamera_*`, `camerastop_*`, `camerachange`, `cameraratio*` | the four-entry table at slot `+0x110` | `CONTRACT-manager-slot-entry-tables.md:71-74`, `:396-400`, `:425-436` |
| camera-shake side B: bind `003DD230`, reset `003DCF60`, clear `003DD320`, republish `003DD350`, rate `003DD1F0`, tick `003DCFB0`, sampler `0037D1F0` | `camerashakestart_*`, `camerashakeclear`, `camerashakestop_*`, `camerashakechange`, `camerashakeratio*` | the four-entry table at slot `+0x170`; the sampler draws the gameplay MT | `CONTRACT-manager-slot-entry-tables.md:71-74`, `:401-402`; `Actor-Manager-Record/the-actor-manager-record-field-map.md:866-872`, `:935-936` |

#### Field runtime pass

| entry | callers | what it does | cite |
|---|---|---|---|
| `World_UpdateSimulationTick` `00314020` (845 B) | frame bodies `0022A770`, `0022B8C0`, `0022BC20` | runs the pass for slots 0–4 on the mode-0 path (up to sixteen sub-steps), slots 3 and 4 on the mode-1 path | `the-field-runtime-pass.md:253`, `:537-542`, `:792` |
| `ActorManager_RunFieldRuntimePass` `0025D9E0` (1,297 B, `ret` at `0025DEF0`) | `00314020` only (`0031411D`, `003141DB`) | one slot's pass: save-busy refusal, `+0x10` bit 0 refusal, publishes `02099D70`/`02099D78`, the slot-0 `0xD4` request, then either the designated drive (`+0x12 != 0`) or the music select, init core, roster loop and two folds | `the-field-runtime-pass.md:31`, `:37`, `:56-118`, `:137-141`, `:184-203`; `CONTRACT-field-runtime-pass.md:49-50`, `:144-154` |
| `WorldActor_UpdateRuntimeAndScriptExecutionState` `0025DF00` (1,228 B) | the pass, 5 sites | the wait resolver: 8-way dispatch on wait slot `+0x14` (table `0025E3CC`); the kind 1/2 arm calls the interpreter `0025E4C0` | `the-field-runtime-pass.md:215-217`, `:394`, `:661-667`, `:707-708`; `CONTRACT-field-runtime-pass.md:53` |
| `SaveWrite_GetBusyFlag` `00583920` (7 B) | the pass | `mov eax, [02CA99E8]`; non-zero stops the pass | `the-field-runtime-pass.md:76-82`; `CONTRACT-field-runtime-pass.md:260` |
| `BattleUnit_UpdateLifecycleAndCombatFrame` `00233F70` (467 B) | via record `+0x38` from `0025DF00` | the battle-unit frame, gated by record `+0x14` bit 4 | `the-field-runtime-pass.md:177`, `:843-848` |

#### Battle unit and definition

| entry | callers | what it does | cite |
|---|---|---|---|
| `BattleStorage_InitializeWorkArrays` `002368D0` (353 B) | `0022A0B0` | count cell `0208E6A0 = 0x20`; reallocs `0x20 × 0xF50` "BtlWork" at `[0208E688]`; two `0x9400` banks | `battleunit-slot-pool-and-actor-class.md:354-368`, `:599-632` |
| `ActorSystem_BindBattleUnitsForEligibleRecords` `00265A20` | not stated | walks the manager's records; binds every record with `+0x14 ≥ 0x80`; stops at 32 (`00265A8F`) and clears `+0x14` bit 4 instead | `battleunit-slot-pool-and-actor-class.md:122-139` |
| `BattleUnit_AllocateSlotAndBindActor` `00234480` | `00265A20` only | linear first-free scan on flag bit 0; silent return when full; `memset(slot,0,0xF50)`; slot index `+0xEA9`; `+0x10` actor; `+0x08` encoded handle; `002134A0` writes actor `+0x30` | `battleunit-slot-pool-and-actor-class.md:96-131`, `:445-466` |
| `BattleUnit_GetBySlotIndex` `00236820` | 40 callers | bounds both ends; `IMUL RAX, RAX, 0xF50` | `battleunit-slot-pool-and-actor-class.md:152-160`, `:413` |
| `ActorSystem_ReleaseBattleUnitSlotForActor` `00234200` | not stated | copies `+0xE0`/`+0x160` out to the spawn record, then a bounds-checked `memset(slot,0,0xF50)` at `002342CE` | `battleunit-slot-pool-and-actor-class.md:790-807`; `Battle-Unit/the-battle-unit-field-map.md:1142-1152` |
| `BattleUnit_ApplyUnitDefinition` `0023A570` (1,808 B) | `Spawn_ApplyScriptSelectedUnit` `0023A3B0`, `BattleGroup_RefreshFourActorDefinitions` `003266C0`, `BattleUnit_TeardownAndDespawn` `00300E40` (id `0xFFFF`) | splits the id into class (high byte) and row; resets the unit; party or enemy path; common stores; returns 1 on install | `Unit-Definition/CONTRACT-battle-unit-construction.md:41-45`; `Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md:58-146` |
| `BattleUnit_ResetStateForReuse` `00236A60` (452 B) | `0023A570` at `0023A5B0` | clears `+0x80` for `0x610` bytes; masks flags; nulls `+0x698`/`+0x6A0`/`+0xE60`/`+0xE68` | `Unit-Definition/CONTRACT-battle-unit-construction.md:86-91`; `Battle-Unit/the-battle-unit-field-map.md:366-367`, `:621-622` |
| `BattleStats_InitializeDefinitionRecord` `0023AC80` (717 B) | `0023A570` (`0023A7A9`), `00237DF0`, `00239960` | `memset(page,0,0x1C8)`; sentinels; id at `+4`; level grower `0030C470`; equipment, LP, licences, gambits | `Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md:154-171`; `Battle-Record-Kind/battle-record-kind-byte.md:73-77` |
| `00322050` rekey (44 B) → `003220E0` | `0023A570` | zeroes `+0xEA4`/`+0xEA8`; bumps the generation `+0x16`; re-points the leader selector; stores the new handle at `+8` | `Unit-Definition/CONTRACT-battle-unit-construction.md:98-100`, `:230-238`; `Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md:68-77` |
| `ActorHandle_EncodeRegistryEntry` `003589B0` / `ActorHandle_ResolveRegistryEntryByPackedId` `003588B0` (143 B) | many | encode `(((+0x16 & 0x7FF)<<4 \| (+0x15 & 0xF)) << 16) \| +0x00`; decode with seven guards | `battleunit-slot-pool-and-actor-class.md:474-487`, `:515-524` |
| `00329220` StatusView builder (1,933 B) | `0031FE70` (full=0), `00320040` (full=1), `0031FEC0`, `0031FF70` | builds the `0xC0`-byte view from stats, owning unit and party row | `Unit-Display-Record/the-record-00329220-builds.md:44-53`, `:105-107`, `:191-198` |
| kind classifier `002F8E90` (131 B) | 17 sites in 11 functions | kind 0 → band ? 2 : 1; kind 1 → owner free-target nibble → 4 / 8 / 0x10 | `Battle-Record-Kind/battle-record-kind-byte.md:120-133` |
| reward partition `002F90C0` / `002F8BB0` | `00312280` | LP / EXP eligibility by type-id span and the `0x80000003` rule | `Battle-Record-Kind/actor-type-id-partition-and-the-13-value-band.md:47-61`, `:79-87`, `:110-117` |

#### Names

| entry | callers | what it does | cite |
|---|---|---|---|
| `NpcDictionary_Load` `003EAC40` (36 B) | `00379D20` only | `0051ED10(kind 9, index 0x1F, callback 003EAC70)`; block at `02B5E0D8` | `Actor-Names/the-npc-name-dictionary.md:44-46`, `:115` |
| `Actor_GetDisplayName` `00263990` (74 B) | display | `+0x102 < 0` → the pointer at `+0xF8`; else strip bit 14, query flag `0032A930`, `003EAC10` entry `2×id + (flag != 0)` | `Actor-Names/the-npc-name-dictionary.md:69`, `:75-80` |
| `Actor_SetNameId` `00269F40` (16 B), verbs `setnpcname` `0034B9A0` / `setshopname` `0034C170` | script | store the id at `+0x102` with bit 14 cleared; a negative id only if `003EABE0(id)` is non-null | `Actor-Names/the-npc-name-dictionary.md:85-90` |

### 1.2 Inputs and outputs (data read and written, with record layouts)

#### `ActorStorageRecord` header (`+0x00`–`+0x11F`)

The type is per-sequence: "Records are 720 to 1,760 bytes, by kind" (`Actor-Storage-Record/the-record-behind-every-actor.md:1425`). The header fields, as the pages
state them:

| offset | width | meaning | cite |
|---|---|---|---|
| `+0x00` | u16 | `selfIndex`, the slot index (`002665EB`) | `Actor-Storage-Record/the-record-behind-every-actor.md:109`; `Actor-Storage-Record/the-actor-storage-record-field-map.md:94` |
| `+0x02` | u8 | `actorIndexClass`, "can hold only 1 or 2" (`0026670D`); meaning is OQ FZ-25 | `Actor-Storage-Record/the-actor-storage-record-field-map.md:95`, `:227-233` |
| `+0x03` | u8 | packed class (high 3 bits) and table row (low 5 bits); see C-V1 for the naming conflict | `Actor-Storage-Record/the-record-behind-every-actor.md:313-314`, `:1446`; `CONTRACT-actor-record-pool-and-region-map.md:193` |
| `+0x04` | u16 | `0xFF00` at init | `Actor-Storage-Record/the-record-behind-every-actor.md:86` |
| `+0x06` | u16 | `channelActiveMask`, bit `ch` set while channel `ch`'s list is non-empty | `Actor-Storage-Record/the-record-behind-every-actor.md:1700`, `:1758` |
| `+0x08`, `+0x09`, `+0x0C`, `+0x0D`, `+0x0E`, `+0x13`, `+0x14` | u8 flag bytes | per-bit tables; "fifty bits with a meaning" | `Actor-Storage-Record/the-record-behind-every-actor.md:343-364`, `:1066`, `:1308`; `Actor-Storage-Record/the-actor-storage-record-field-map.md:100-111` |
| `+0x0E` low nibble | 4 bits | free-target type (`00263C20`); 1 hostile, 3 allied/event, 4 interactable, 5 non-combatant, 6 boss scripts | `Battle-Record-Kind/battle-record-kind-byte.md:293`, `:362`; `Battle-Record-Kind/battle-record-kind-byte.md:4` |
| `+0x11` | s8 | `currentWaitSlot`, index into `+0xA8` | `Actor-Storage-Record/the-record-behind-every-actor.md:1663-1666`; `the-field-runtime-pass.md:647` |
| `+0x12` | u8 | `0xFF` at init; party slot 0–3 when active | `Actor-Storage-Record/the-record-behind-every-actor.md:86`, `:2440-2446` |
| `+0x14` | u8 | bit 4 drive the bound battle unit; bit 5 script enable (`00269E00`); bit 6 settled; bit 7 battle-unit eligible; bits 0–3 never written | `the-field-runtime-pass.md:152-180`; `CONTRACT-field-runtime-pass.md:428` |
| `+0x15` / `+0x16` | u8 / u16 | handle selector (`& 0xF`) / generation (`& 0x7FF`) | `battleunit-slot-pool-and-actor-class.md:483-487`; `Actor-Storage-Record/the-record-behind-every-actor.md:248-249` |
| `+0x18` | u32 | `0xFFFF0000` at init | `Actor-Storage-Record/the-record-behind-every-actor.md:86` |
| `+0x1C` | u32 | request bitmap; presets 0 / `0x38` / `0x40` / `0x30004` / `0x34C85` by row | `Actor-Storage-Record/the-record-behind-every-actor.md:309-311`; `Actor-Storage-Record/the-actor-storage-record-field-map.md:117` |
| `+0x30` | ptr | the bound `BattleUnit` | `Actor-Storage-Record/the-record-behind-every-actor.md:206`; `battleunit-slot-pool-and-actor-class.md:463` |
| `+0x38` | ptr | callback; `00233F70` planted at `00265AA8` | `the-field-runtime-pass.md:177` |
| `+0x40`, `+0x48`, `+0x50`, `+0x58` | ptr | authored entry (`0x30` B); script function table; jump table; bytecode base | `Actor-Storage-Record/the-actor-storage-record-field-map.md:124-127` |
| `+0x60`–`+0x63` | u8 ×4 | free-list head, detached-list head, selected entry, list flags | `Actor-Storage-Record/the-actor-storage-record-field-map.md:128-131`; `Actor-Storage-Record/the-record-behind-every-actor.md:1696-1697` |
| `+0x64`–`+0x70` / `+0x74`–`+0x80` | int32 ×4 / float ×4 | script VM registers I0–I3 / F0–F3 | `Actor-Storage-Record/the-actor-storage-record-field-map.md:132-139`; `Actor-Storage-Record/the-record-behind-every-actor.md:192-194` |
| `+0x88` / `+0x89` | u8 | wait-slot count (8, or 6 when sub == 1) / resource-entry count (10, or 8) | `Actor-Storage-Record/the-record-behind-every-actor.md:1631` |
| `+0x8C`, `+0x94` | u8[8] each | channel tails / heads | `Actor-Storage-Record/the-actor-storage-record-field-map.md:142-143` |
| `+0xA0`, `+0xA8`, `+0xB8`, `+0xC0` | ptr | resource entries, wait slots, movement context, secondary context | `CONTRACT-actor-record-pool-and-region-map.md:94-96`; `Actor-Storage-Record/the-record-behind-every-actor.md:1602-1611` |
| `+0xC8`–`+0xEB` | u16[18] | override array, `0xFFFF` at init | `Actor-Storage-Record/the-actor-storage-record-field-map.md:205`; `CONTRACT-actor-record-pool-and-region-map.md:294-295` |
| `+0xF6` | u16 | spawn entry-group word | `Actor-Storage-Record/the-actor-storage-record-field-map.md:165`, `:387`; `battleunit-slot-pool-and-actor-class.md:281` |
| `+0xF8`, `+0x100`, `+0x102` | ptr / u16 / s16 | literal name pointer / not stated / name id | `Actor-Names/the-npc-name-dictionary.md:76-77`, `:154`, `:162` |
| `+0x10C`/`+0x110`/`+0x114` | | stop set 2 live / pending set / pending clear | `Actor-Storage-Record/the-actor-storage-record-field-map.md:171-173` |
| `+0x118` / `+0x11A` | u16 | countdown 0 / reload 60 | `Actor-Storage-Record/the-record-behind-every-actor.md:1309-1321` |

#### Region map and the per-sequence table

- The table at `0x01E0C328` has eight 4-byte entries `{u8 class 0..3, u8 sub 0/1, u16 size}`
  (`CONTRACT-actor-record-pool-and-region-map.md:49-55`, `:59-68`). Sizes 808 / 936 / 816 / 840 / 720 / 1,760 / 1,760 / 1,640 (`Actor-Storage-Record/the-record-behind-every-actor.md:1412-1423`).
- `+0xA8 = +0xA0 + (subFlag ? 0xA0 : 0xC8)` (`CONTRACT-actor-record-pool-and-region-map.md:144`).
- Arms (`CONTRACT-actor-record-pool-and-region-map.md:137-142`):

  | class (sequence) | `+0xB8` | `+0xC0` | `+0xA0` |
  |---|---|---|---|
  | 0 (seq 0) | NULL | NULL | `rec+0x120` |
  | 1 (seq 1, 2) | `rec+0x120` | NULL | `rec+0x1A0` |
  | 2 (seq 3, 4) | `rec+0x120` | NULL | `rec+0x140` |
  | 3 (seq 5, 6, 7) | `rec+0x120` | `rec+0x350` | `rec+0x4D8` |

- The executed live control EXP-026 gives seq 5: extent `0x6E0`, `+0xA8 = 0x5A0`; seq 7: extent `0x668`,
  `+0xA8 = 0x578` (`CONTRACT-actor-record-pool-and-region-map.md:446-453`; `Actor-Storage-Record/the-record-behind-every-actor.md:2520`). See C-V2.

#### Wait slot (`0x28`, at `*(rec+0xA8) + (int8)rec[+0x11] × 0x28`) and resource entry (`0x14`)

- Wait slot fields (`the-field-runtime-pass.md:653-654`; `Actor-Storage-Record/the-record-behind-every-actor.md:1883-1903`):
  - `+0x14` `waitKind`, an enum 0–7 (`cmp 7 / ja`);
  - `+0x15` `commandPhase`;
  - `+0x16` `parked`;
  - `+0x18` `targetRef`, base-relative to `*(01F83530)`;
  - `+0x20` `waitResourceId`;
  - `+0x22` the list cursor for kinds 5 and 7 (`the-field-runtime-pass.md:427`);
  - `+0x24` `targetOrdinal`;
  - `+0x26` `waitChannel`;
  - `+0x27` set by kinds 3, 6 and 7 and "never read as a settled flag" (`the-field-runtime-pass.md:484-489`, `:348`).
- Wait-kind arms (`the-field-runtime-pass.md:413-421`, `:707-708`):

  | kind | arm | behaviour |
  |---|---|---|
  | 0 | `0025E127` | blocked |
  | 1, 2 | `0025E0BE` | the interpreter |
  | 3 | `003DBF60` | holds while the entry exists |
  | 4 | `003DC050` | holds until the notification arrives; `003DB2A0` removes the entry |
  | 5 | `002674B0` | |
  | 6 | `003DB640` | |
  | 7 | `00267420` | |

- Resource entry (`0x14`), as stated (`CONTRACT-actor-record-pool-and-region-map.md:560-584`; `Actor-Storage-Record/the-record-behind-every-actor.md:1623-1628`):
  - `+0x00` next, `+0x01` prev;
  - `+0x03` requester wait slot;
  - `+0x04` dword `0x80000000`;
  - `+0x06` actor ordinal (`0x8000` = none);
  - `+0x08` requester manager index;
  - `+0x0C` requester return PC;
  - `+0x10` a byte compared to 3.

#### `ActorManagerSlot` (`0x288`, five at `02098E10`, ends `02099AB8`)

| offset | meaning | cite |
|---|---|---|
| `+0x000` | bound definition payload; payload `+0x50` word = designated actor ordinal | `Actor-Manager-Record/the-actor-manager-record-field-map.md:90`; `the-field-runtime-pass.md:137-139` |
| `+0x008` | `recordPool` (count dword, table at pool+8) | `the-field-runtime-pass.md:589-593` |
| `+0x010` | status byte: bit 0 live (set `0026D305`, cleared `00262DA8`); bit 1, bit 3 (`0xD4` latch), bit 4, bit 5, bit 7 (republished into `+0x11` bit 0) | `CONTRACT-field-runtime-pass.md:60`, `:444-452`; `the-field-runtime-pass.md:91-97`, `:324-327` |
| `+0x011` | bit 0 copy of `+0x10` bit 7; bit 3 payload load in flight | `CONTRACT-field-runtime-pass.md:61`, `:521-525` |
| `+0x012` | "Drive the named actor": the bind sets it, exit A clears it | `CONTRACT-field-runtime-pass.md:62` |
| `+0x018`/`+0x01A`, `+0x01C`/`+0x01E` | side-A reverse lookup words; side-B shake channel owners | `CONTRACT-manager-slot-entry-tables.md:70`; `Actor-Manager-Record/the-actor-manager-record-field-map.md:99-100` |
| `+0x020` | actor count (bound of both fold loops) | `CONTRACT-field-runtime-pass.md:65` |
| `+0x024`, `+0x038` | per-pass frame counters | `CONTRACT-field-runtime-pass.md:66` |
| `+0x028` | manager index; also indexes the shake table | `Actor-Manager-Record/the-actor-manager-record-field-map.md:102`, `:861-876` |
| `+0x048`, `+0x058`, `+0x060` | `table256` (save payload) / `bank64` `02099DF0` / `bank32` `02099FF0` | `the-field-runtime-pass.md:556-576`; `Actor-Manager-Record/the-actor-manager-record-field-map.md:104-106` |
| `+0x050`, `+0x068`, `+0x070`, `+0x078`, `+0x080`, `+0x098` | local base, int pool, float pool, variable descriptors, tag table, resolver `00264E30` | `Actor-Manager-Record/the-actor-manager-record-field-map.md:323-334` |
| `+0x0A0`–`+0x100` | section pointers 2, 3, 6, 8, 9, 10, 11, 12 | `Actor-Manager-Record/the-actor-manager-record-field-map.md:316` |
| `+0x110`, `+0x170` | four `0x18` entries each: camera shot (A) / camera shake (B) | `Actor-Manager-Record/the-actor-manager-record-field-map.md:148-170`; `CONTRACT-manager-slot-entry-tables.md:69` |
| `+0x1D0`/`+0x1D8` | per-kind record counts / prefix sums (u16) | `Actor-Storage-Record/the-record-behind-every-actor.md:1392`, `:1402` |
| `+0x1D6`/`+0x1DE` | record range of one kind (start/count disputed, C-V5) | `Actor-Manager-Record/the-actor-manager-record-field-map.md:246-247` |
| `+0x200`, `+0x201` | bit 2 cleared at bind; sub-step opt-in | `Actor-Manager-Record/the-actor-manager-record-field-map.md:146`, `:292` |
| `+0x204`–`+0x243`, `+0x244`–`+0x27C` | bind-zeroed blocks | `Actor-Manager-Record/the-actor-manager-record-field-map.md:248`, `:76` |

Slot entry (`0x18`) for both sides (`CONTRACT-manager-slot-entry-tables.md:117-124`):

| offset | field |
|---|---|
| `+0x00` | `definitionValue` |
| `+0x04` | `lookupIndex` |
| `+0x08` | state |
| `+0x0A` | `recordIndex` |
| `+0x0C` | `clock` |
| `+0x10` | `rate` |
| `+0x14` | `clockRunning` (A only) |
| `+0x15` | 3 unknown bytes |

#### Contexts

- **Movement context** (`0x230` at record `+0x120`, through `+0xB8`). Named fields include:
  - position `+0x00..+0x08`;
  - radius pair `+0x50/+0x54` and mean radius `+0xFC` (floor 0.01);
  - requested speed `+0xD0`;
  - sub-record index `+0xDC`;
  - active `SteeringRecord` pointer `+0xF0`;
  - two `0x80` `SteeringRecord`s at `+0x120`/`+0x1A0`.

  Cites: `Actor-Contexts/the-movement-and-secondary-context-censuses.md:100-188`, `:375`. The lede says the page "names nothing — the store owns the layouts" (`Actor-Contexts/the-movement-and-secondary-context-censuses.md:38-39`).
- **Secondary context** (`0x188` at `+0x350`, through `+0xC0`):
  - `4 × 0x30` elements in the first 192 bytes: `+0` render index, `+4` resource id, `+8` bound record, `+0x10` flags,
    `+0x2A` motion preset;
  - `+0x138` the movement body pointer;
  - `+0x14C`–`+0x14F` model, CLUT, init byte, attach bits;
  - stop-set triplets at `+0x158`–`+0x178`.

  Cites: `Actor-Contexts/the-movement-and-secondary-context-censuses.md:204-279`, `:310-344`.

#### `BattleUnit` (`0xF50` = 3,920 B, pool `*(0208E688)`, 32 slots)

| offset | meaning | cite |
|---|---|---|
| `+0x000` | u64 flags; bit 0 slot in use; bit table §2.5 (36 immediate rows, 7 register-mask rows) | `Battle-Unit/the-battle-unit-field-map.md:84`, `:313-362` |
| `+0x008` | encoded actor handle | `Battle-Unit/the-battle-unit-field-map.md:86`; `battleunit-slot-pool-and-actor-class.md:445` |
| `+0x010` | the bound `ActorStorageRecord` | `Battle-Unit/the-battle-unit-field-map.md:87`; `battleunit-slot-pool-and-actor-class.md:446` |
| `+0x048` | s32 HP floor, zeroed on every apply | `Battle-Unit/the-battle-unit-field-map.md:95`; `Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md:140-141` |
| `+0x052`–`+0x058` | definition word, team `0xFF`, type, kind, lane byte, runtime category mode | `Battle-Unit/the-battle-unit-field-map.md:99-104` |
| `+0x080` | `BattleLocomotionState` (`0x180`) | `Battle-Unit/the-battle-unit-field-map.md:412-440` |
| `+0x0E0` | world position (copied to the spawn record at release) | `Battle-Unit/the-battle-unit-field-map.md:116-118` |
| `+0x200`–`+0x68F` | navigation path state; waypoint table `{f32 x, f32 z}[128]` at `+0x290` | `Battle-Unit/the-battle-unit-field-map.md:444-452`, `:616-623` |
| `+0x698` / `+0x6A0` | stats record / spawn record (NULL for party) | `Battle-Unit/the-battle-unit-field-map.md:173-174`; `Battle-Record-Kind/battle-record-kind-byte.md:66-72` |
| `+0x6B0`–`+0xB9F` | action-state block (`0x4F0`); `+0x6B4` 13-phase machine; `+0x6E0`–`+0x6F8` order sets; `+0x708`/`+0x710`/`+0x714` committed order, target, action id; target buffer `+0x778` (`0x208`) | `Battle-Unit/the-battle-unit-field-map.md:175-222`, `:454-488` |
| `+0xBC0` | perception candidates (`0x208`, max 32) | `Battle-Unit/the-battle-unit-field-map.md:495` |
| `+0xE60`/`+0xE68`/`+0xE70`/`+0xE78` | definition row / `.ard` class row / reward rows | `Battle-Unit/the-battle-unit-field-map.md:235-238`; `Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md:112-115` |
| `+0xEA9` | slot index | `Battle-Unit/the-battle-unit-field-map.md:249`; `battleunit-slot-pool-and-actor-class.md:447` |
| `+0xEB4`–`+0xF4F` | 156-byte unreached tail | `Battle-Unit/the-battle-unit-field-map.md:259` |

#### `BattleStatsRecord` (`0x1C8`)

- Fields (`Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md:159-194`; `Unit-Display-Record/the-record-00329220-builds.md:66-78`; `the-definition-record-flag-pair.md:61-63`, `:93-96`):

  | offset | meaning |
  |---|---|
  | `+0x04` | id (u16) |
  | `+0x05` | kind byte |
  | `+0x24` | max HP |
  | `+0x28` | MP capacity |
  | `+0x38` | immunities |
  | `+0x3C` / `+0x64` | status words |
  | `+0x48` | HP |
  | `+0x4C` | MP |
  | `+0x50`–`+0x58` | equipment |
  | `+0x18C` | experience |
  | `+0x190` | LP, clamped to 99,999 |
  | `+0x194` | licences |
  | `+0x1C2` | level |

- Kind 0 lives at `*(02EBF190) + 8 + slot × 0x1C8`. Kind 1 is embedded in the `0x250` spawn record at `+0x80`
  (`Battle-Record-Kind/battle-record-kind-byte.md:64`).
- The kind domain is `{0, 1}` (`Battle-Record-Kind/battle-record-kind-byte.md:314-315`).

#### Definition rows

- Enemy table `02EBF120` (`Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md:96-121`, `:348`; `Battle-Record-Kind/battle-record-kind-byte.md:473`):
  - row `+0x00` indexes the `.ard` class table `02EBF150`;
  - `+0x02` spawn-counter lane;
  - `+0x03 & 3` tracked-HP code;
  - `+0x08` name;
  - `+0x22`/`+0x24` reward rows;
  - `+0x32`–`+0x36` steal slots;
  - `+0x50` order-set index.
- Party table `02EBF130`: 128 rows of the descriptor's word `+8` bytes (`Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md:349`); field list at `Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md:167-193`.

#### `StatusView` (`0xC0`), output of `00329220`

- Eighteen flag bits in `+0x00`.
- HP block `+0x20`–`+0x28`; MP block `+0x2C`–`+0x38`.
- Countdowns `+0x66`–`+0x85`.
- Experience and to-next `+0x90`/`+0x94`; equipment `+0x98`–`+0xA8`.
- Level and licence count `+0xBA`/`+0xBB`.

Cites: `Unit-Display-Record/the-record-00329220-builds.md:57-91`.

#### `npcdic.bin`

- Layout `{NPC0, u32 relocated, u32 count, i32 offsets[count], strings}`.
- 2,282 entries = 1,141 pairs. Entry `2×id` is the first name and `2×id+1` the second.
- Strings use `0x20–0x39 = A–Z, 0x3A–0x53 = a–z, 0x04 = space` (`Actor-Names/the-npc-name-dictionary.md:52-63`).

### 1.3 State (globals and objects, with lifetime)

| object | where / size | lifetime | cite |
|---|---|---|---|
| actor record pool (one per manager) | `ActorManagerSlot +0x08`; header `(count*8 + 0x17) & ~15` doubled, then 16-aligned records | allocated by `ctx->vtbl_88` in `002679F0` and zeroed; released at `00262D9F` in `002628B0`, owner nulled at `00262DA4` | `Actor-Storage-Record/the-record-behind-every-actor.md:1378-1387`, `:2279-2291` |
| `ActorManagerSlot` ×5 | `02098E10`, image-resident | static; "**no destructor can exist**" for the entry tables | `CONTRACT-manager-slot-entry-tables.md:151-152`; `the-field-runtime-pass.md:542-546` |
| bound slot | `02099D70` | scoped "current manager"; twelve functions save, bind and restore; the unload binds without restoring | `Actor-Manager-Record/the-actor-manager-record-field-map.md:340-357` |
| script banks | `02099DF0` (64 int16, wiped every field transition), `02099FF0` (32 int16, saved), save payload base `0x02164480` (256 int16) | as stated | `Actor-Storage-Record/the-record-behind-every-actor.md:2406-2431`, `:2788-2791` |
| party roster | `0209A1F0`, 4 qwords | reset `0026DB52`/`0026DB5A`; cleared by `002695A0` | `Actor-Storage-Record/the-record-behind-every-actor.md:2433-2456` |
| save busy flag | `02CA99E8` | set 1 at `0057E495`, `0057E559`; cleared at `0057E58B` | `the-field-runtime-pass.md:82-86` |
| BattleUnit pool | `[0208E688]`, `0x20 × 0xF50`; count `0208E6A0` | allocated by `002368D0`; each slot `memset` at allocation (`002344D2`) and release (`002342CE`) | `battleunit-slot-pool-and-actor-class.md:354-368`, `:788-807` |
| battle-state block | `*(02EBF190)`; `+8` 40 × `0x1C8` | points into the save buffer at `+0x4E68C` (`00238A80`); a loaded save re-runs the reset | `Battle-Record-Kind/battle-record-kind-byte.md:949-952`; `Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md:356` |
| spawn records | `*(0208E690) + id × 0x250` | `.data`, filled at runtime | `Battle-Record-Kind/battle-record-kind-byte.md:511`, `:519-521` |
| spawn-history counters | `0208D354`, two banks of 64 u16; bank selector `0208D454` | flipped per area by `00233780`; filled with 1 | `Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md:244-251` |
| NPC dictionary | `02B5E0D8` | loaded at boot by `00379D20`; relocated in place | `Actor-Names/the-npc-name-dictionary.md:44-46`, `:60-62` |
| request mask | `02099ABC` | ORed by `0026A5F0`; "drained by the world tick's every-mode prologue `0025BFB0`" is stated as a FABLE proposal | `CONTRACT-field-runtime-pass.md:263`, `:473` |
| dispose mark | `022C6D20[m]` | set by `00332190`; cleared by `0032ED80` and `0032F430` | `CONTRACT-field-runtime-pass.md:534-548` |

### 1.4 Order (what runs when in a frame, and what triggers it)

1. **Boot / area load.** `World_UpdateSimulationTick` → `0025BFB0` → `0026CE60` → `002679F0`. That is, size, allocate,
   zero, count, carve and stamp `+0x03`, prefix-sum, then initialise every record (`Actor-Storage-Record/the-record-behind-every-actor.md:1368`, `:1377-1406`,
   `Actor-Storage-Record/the-record-behind-every-actor.md:2924`).
2. **Bind.** `0026C8C0` writes the slot. It sets `+0x12` from the payload's `+0x50` word (`CONTRACT-field-runtime-pass.md:62`;
   `Actor-Manager-Record/the-actor-manager-record-field-map.md:73-79`).
3. **Frame.** The frame bodies call `00314020` (`the-field-runtime-pass.md:792`). It runs slots 0–4 in mode 0, up to sixteen sub-steps,
   and slots 3–4 in mode 1 (`the-field-runtime-pass.md:537-542`). Per slot, the pass (`CONTRACT-field-runtime-pass.md:216-240`; `the-field-runtime-pass.md:56-203`) runs in this
   order:
   1. busy refusal;
   2. republish `+0x10` bit 7 → `+0x11` bit 0;
   3. dispose-request gate;
   4. `+0x10` bit 0 refusal;
   5. publish `02099D70`/`02099D78`;
   6. the slot-0 `0xD4` request;
   7. then one of two branches:
      - **designated drive** (`+0x12 != 0`), ending at exit A or exit B;
      - otherwise, in order:
        - `00261F90` music;
        - `002620E0`;
        - roster loop;
        - fold 1;
        - fold 2;
   8. common tail: `0025B600` when `r14d` is zero; `+0x24`/`+0x38` incremented.
4. **Per actor**, `0025DF00` (`the-field-runtime-pass.md:499-512`, `:830-835`):
   1. class-3 movement path;
   2. loop head with the half-rate gates;
   3. index the wait slot;
   4. dispatch, at most two per call;
   5. settle block.
5. **Battle side.**
   - `00265A20` binds eligible records (`battleunit-slot-pool-and-actor-class.md:122-139`).
   - The unit frame runs through record `+0x38` while `+0x14` bit 4 is set (`the-field-runtime-pass.md:177`).
   - Defeat → `00312280` (`Battle-Unit/the-battle-unit-field-map.md:863-909`).
   - Release → `00234200` (`battleunit-slot-pool-and-actor-class.md:790-807`).
6. **Definition install** is triggered three ways (`Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md:404`, `:425`, `:732`; `Unit-Definition/CONTRACT-battle-unit-construction.md:55-57`):
   - script verb `VM_Spawn_ApplySelectedUnit` → `0023A3B0`;
   - teardown (`0xFFFF`);
   - area transition (`002342F0`) and save rebind (`00238A80` → `00237DF0`).
7. **Unload.** `002628B0`: semantic release, then the pool release. "When `002628B0` runs in a session" is
   **not established** (`Actor-Storage-Record/the-record-behind-every-actor.md:2347-2349`).

### 1.5 Dependencies (on other systems)

| system | dependency | cite |
|---|---|---|
| 00 Engine core | the world tick and field frame call the pass; the time-stop registry sets `BattleUnit +0x004` bit 5 and `+0x000` bit 36 | `the-field-runtime-pass.md:537-542`; `Battle-Unit/the-battle-unit-field-map.md:84-85` |
| 01 Script VM | the interpreter `0025E4C0` runs on the record in `r15`; verbs set names, requests, flags, camera entries | `CONTRACT-actor-record-pool-and-region-map.md:477-480`; `CONTRACT-manager-slot-entry-tables.md:71-74`; `Actor-Names/the-npc-name-dictionary.md:85-90` |
| 02 Resource | `0032FC30`/namespace-5 paths; ARD registry slots `02EBF120`–`02EBF168` | `the-field-runtime-pass.md:317-341`; `Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md:104-105` |
| 05 Spawn | spawn records `0x250`; `00236100`; the counters | `Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md:106`, `:244-251`; `Battle-Record-Kind/battle-record-kind-byte.md:502-512` |
| 06 Movement | `00265FF0`/`00268380` initialise the movement context; steering mode gates on class 3 | `CONTRACT-actor-storage-record-initialisation.md:249`; `Actor-Storage-Record/the-actor-storage-record-field-map.md:401-403`; `Actor-Contexts/the-movement-and-secondary-context-censuses.md:375` |
| 07/08/09 Combat | stats rebuild, status words, gambit sets at `+0x6E0`–`+0x6F8`, AI operand reader `00321190` | `the-definition-record-flag-pair.md:114-131`; `Battle-Unit/the-battle-unit-field-map.md:472-475`; `Actor-Storage-Record/the-record-behind-every-actor.md:2672-2703` |
| 11 Party | roster `0209A1F0`, focus `003590D0`, leader selector `+0x5AA4` | `the-field-runtime-pass.md:197-198`; `Unit-Definition/CONTRACT-battle-unit-construction.md:232-238` |
| 14/Save | `SaveImage_GetPersistentPayloadBase` = `002EF640() + 0x200`; busy flag `02CA99E8`; battle-state block in the save buffer | `README.md:78`; `the-field-runtime-pass.md:82-86`; `Battle-Record-Kind/battle-record-kind-byte.md:949-952` |
| 16 UI | `StatusView` consumers; `0209AC30` keeps nine copies | `Unit-Display-Record/the-record-00329220-builds.md:202-216` |
| 18 Audio | `00261F90` area music | `the-field-runtime-pass.md:262`, `:786` |
| 21 RNG | shake sampler draws the gameplay MT; LCG on the build path | `Actor-Manager-Record/the-actor-manager-record-field-map.md:935-938`; `Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md:726` |

---

## 2. Gaps

### 2.1 Gaps the pages state themselves (still open on the snapshot)

Only statements that no later section or dated note on any 04 page answers are listed here. Those that *are*
answered elsewhere are stale, and they are in §3.2.

| # | gap, quoted | cite |
|---|---|---|
| G-1 | "`EH-3` is **narrowed, not closed**" — undeclared header spans remain | `Actor-Storage-Record/the-record-behind-every-actor.md:1679-1680` |
| G-2 | "**No runtime observation confirms a live list.**" (the resource-entry channel lists) | `Actor-Storage-Record/the-record-behind-every-actor.md:1783` |
| G-3 | "What remains unobserved is everything that happens *over time*: the half-rate phase behaviour, the wait-slot drive loop and the free-list discipline are still static readings of code nobody has watched run." | `Actor-Storage-Record/the-record-behind-every-actor.md:2223-2225` |
| G-4 | Unload timing: "when `002628B0` runs in an ordinary session, how often, or whether any holder actually retains an interior pointer across it" is not established | `Actor-Storage-Record/the-record-behind-every-actor.md:2347-2349` |
| G-5 | Script banks: "What the bank's `u16` entries *mean* is still unknown for both"; "**What the bank entries mean individually is still unknown**, except index 3 of kind 1"; "**What the 256 entries mean is unknown.**" | `Actor-Storage-Record/the-record-behind-every-actor.md:2662`, `:2768`, `:2832` |
| G-6 | "**Kinds 4–8 and 10 are named and not decoded.**" (the AI operand kinds that read actor banks) | `Actor-Storage-Record/the-record-behind-every-actor.md:2764` |
| G-7 | "`+0x08` bit 5 is read twice and, on everything I can find, never set" | `Actor-Storage-Record/the-record-behind-every-actor.md:560` |
| G-8 | Resource entry: "**The entry's `+0x06` is still unnamed.**"; "only `3` and `4` are distinguished here" (state); "`+0x024` and `+0x026` are recorded with **`UNRESOLVED` meaning**" | `Actor-Storage-Record/the-record-behind-every-actor.md:1774-1777` |
| G-9 | Wait arming: "The kind 3, 4 and 5 arms were located but their argument setup was not read."; "**What the opcodes mean is not claimed here.**"; the 64-entry wait list's "element layout is **not** recovered" | `Actor-Storage-Record/the-record-behind-every-actor.md:1942-1949` |
| G-10 | "`movementContext` and `secondaryContext` have their extents but no internal layout at all" (record page); the census "names nothing — the store owns the layouts" | `Actor-Storage-Record/the-record-behind-every-actor.md:2006-2007`; `Actor-Contexts/the-movement-and-secondary-context-censuses.md:38-39` |
| G-11 | Record field `+0x02`: "What the two classes *select* is OQ FZ-25." | `Actor-Storage-Record/the-actor-storage-record-field-map.md:233` |
| G-12 | Pool: "What distinguishes sequences 5 and 6, whose descriptors are identical."; "What the **second** table holds is still open"; "Why layout class 0 leaves both `+0xB8` and `+0xC0` NULL." | `CONTRACT-actor-record-pool-and-region-map.md:461`, `:463-464`, `:468` |
| G-13 | "**Whether any shipped descriptor does this is not established here**" (a descriptor declaring more groups than the table carves) | `CONTRACT-actor-record-pool-and-region-map.md:227-228` |
| G-14 | Slot-entry tables: "**Evidence class: isolated original-code. Live capture: still absent.**"; still to execute: "**The reset's ten-word pattern**" | `CONTRACT-manager-slot-entry-tables.md:226`, `:377-378` |
| G-15 | Manager slot fields still unnamed (FH-1 narrowing, 2026-09-27): the `+0x12`/`+0x13`/`+0x17` bytes, the counters, `+0xB8`, `+0xC8`/`+0xD0`, `+0x108`, `+0x1E8`/`+0x1F8`/`+0x1FC`/`+0x284`, the `+0x204`/`+0x244` blocks | `Actor-Manager-Record/the-actor-manager-record-field-map.md:316` |
| G-16 | "That a summon or event read lands on a live slot is the one runtime condition not shown here." | `Actor-Manager-Record/the-actor-manager-record-field-map.md:372` |
| G-17 | Camera shake: "**The `0x10` remainder of each `0x3D0` record, and `0xC8` of each `0xF0` driver block, are unread.** … **the block they point into is not explained.**" | `Actor-Manager-Record/the-actor-manager-record-field-map.md:880-883` |
| G-18 | Contexts: sequence 0's `+0xA0` region, "What lives there is not established here."; "Whether elements 1-5 carry the same vector is unproven" | `Actor-Contexts/the-movement-and-secondary-context-censuses.md:472`, `:342-343` |
| G-19 | Battle unit: `+0x052` "Which definition field feeds the stack slot is not traced."; `+0x056` "The category values are not decoded."; `+0x110` "Which of the two is "goal" and which "look-at" is open."; flag bits "What each bit *means* is still open per bit" | `Battle-Unit/the-battle-unit-field-map.md:399`, `:402`, `:421`, `:598-599` |
| G-20 | Construction: "Required live installation evidence and initialized-state reachability; unexecuted"; "peer review and repair/rerun of the producer harness's wrong table observation and nondiscriminating bit check" | `Unit-Definition/CONTRACT-battle-unit-construction.md:328`, `:341-343` |
| G-21 | Definition data: the area-state party row, "What else that row holds is not read here."; "`00427280` and `003AEEF0` are unread." | `Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md:207-208`, `:547` |
| G-22 | StatusView: "`00329220`'s 1,933 bytes were **not** re-read … Nothing was executed or observed live."; bits 16/17: "What the two designations and the two bits *mean* stays open with them." | `Unit-Display-Record/the-record-00329220-builds.md:287-290`, `:148-149` |
| G-23 | Type id: "the consumer of codes 42–80 is not read"; "`FUN_0050FF20` has zero callers … presumably reached through a dispatch table that was not traced." | `Battle-Record-Kind/actor-type-id-partition-and-the-13-value-band.md:238-239`, `:242-243` |
| G-24 | Kind byte: "Whether that matches hostility in every battle is not claimed here."; the band "whether the band is an inclusion or an exclusion — **the sense differs by call site.**"; "**44 of the 49 remain uncovered by it**" (spawn-entry writers) | `Battle-Record-Kind/battle-record-kind-byte.md:264-265`, `:895-896`, `:750-751` |
| G-25 | Names: "Which of the 247 (or 275) pairs a shipped flag actually sets: **not traced**" | `Actor-Names/the-npc-name-dictionary.md:272-273` |
| G-26 | Field pass: "This is a tested missing-notification boundary, not proof of a deadlock in ordinary gameplay."; "Current notification-capacity/recovery, arbitrary reentrancy, request-identity reuse and authored input bounds remain open." | `the-field-runtime-pass.md:433-434`; `CONTRACT-field-runtime-pass.md:875-879` |
| G-27 | Dispose mark: "nothing here shows the mark being **consumed** by the pass, only reset by teardown and init, and the exact ordinary-reload timing remains unobserved" | `CONTRACT-field-runtime-pass.md:609-611` |
| G-28 | Handles: "nothing here says which unit the game resolves for a real `+0x710`" | `battleunit-slot-pool-and-actor-class.md:531-532` |

### 2.2 Structural gaps (a port needs these and no 04 page states them)

| # | missing piece | what the pages give instead | cite |
|---|---|---|---|
| S-1 | **The record-pool allocator.** The pool comes from `qword [r15+0x88]` / `ctx->vtbl_88`, and that object is not identified. Pool exhaustion behaviour is not read. | "The pool comes from a *virtual* call, so its allocator is not identified"; "pool exhaustion behaviour is not read"; the contract executed it only against "a stub returning a fixture pool" | `Actor-Storage-Record/the-record-behind-every-actor.md:2378-2379`, `:2211`; `CONTRACT-actor-record-pool-and-region-map.md:155` |
| S-2 | **Initial value of every record field.** A port must reproduce the constructor's output byte for byte. | "Only these are given definite values: `+0x04 = 0xFF00`, `+0x12 = 0xFF`, `+0x18 = 0xFFFF0000`, `+0xF5 = 0xFF`, `+0x118 = 0x003C0000`, and a set of zeroed pointers and counters." The masks are listed, but the full store list sits in `_types/fields.tsv`, outside the folder. | `Actor-Storage-Record/the-record-behind-every-actor.md:86-87`; `Actor-Storage-Record/the-actor-storage-record-field-map.md:281-286` |
| S-3 | **Movement-context initialiser bodies.** `00265FF0` (1,339 B) and `00268380` (420 B) are called by the record initialiser. `002681E0` is also called. | named as callees, "**not read**"; `CONTRACT-actor-storage-record-initialisation.md` names `00265FF0` as "the 1,339-byte Movement body that initialises the movement context" | `Actor-Storage-Record/the-record-behind-every-actor.md:166-167`; `CONTRACT-actor-storage-record-initialisation.md:249` |
| S-4 | **The definition payload format.** This covers the authored entry at `[record+0x40]` past `+0x00`/`+0x06`/`+0x16`, the per-area group counts and the payload sections. | "the payload's own format is not recovered"; "**what is inside those sections is unknown**" | `Actor-Storage-Record/the-record-behind-every-actor.md:1044-1054`, `:2203`, `:2208`; `CONTRACT-actor-record-pool-and-region-map.md:466-467` |
| S-5 | **Context internals.** Most movement-context fields and every secondary-context field are needed for any actor that moves or renders. | per-offset census rows and a few names; layouts are "the store's to declare" | `Actor-Contexts/the-movement-and-secondary-context-censuses.md:38-39`; `README.md:53-54` |
| S-6 | **The resource-entry field offsets.** The search uses `resourceId`, `classAndFlag`, state and channel, and their offsets are not stated. | pseudocode only: `e->resourceId`, `e->classAndFlag>>1` | `Actor-Storage-Record/the-record-behind-every-actor.md:1720-1721`, `:1740-1748` |
| S-7 | **Wait-kind arming.** For kinds 3–5: how the interpreter sets the wait slot's `+0x18`–`+0x26` before the resolver reads them. | "their argument setup was not read" | `Actor-Storage-Record/the-record-behind-every-actor.md:1942-1944` |
| S-8 | **The field pass's own callees and slot fields.** These are the init core `002620E0`, the tail call `0025B600`, the roster arm `00269860` and the dead-path `003DB280`. Also missing: what the region between the two folds does to `+0x10` bit 7, and the slot fields `+0x13`, `+0x17` and `+0x200`. | `002620E0` only as "re-arms only when `b10 & 4` is clear, with the `ice` return compared **signed**"; `0025B600` only as "if `r14d` is zero, call `0025B600`"; `00269860(record, 1)` named | `CONTRACT-field-runtime-pass.md:154`, `:418`, `:450-452`, `:63-67`; `the-field-runtime-pass.md:202` |
| S-9 | **The unit reset `00236A60`'s full field list.** Every install starts with it. | "among much else nulls `+0x698`, `+0x6A0`, `+0xE60` and `+0xE68`"; one measured all-ones result `0xFFEF7FB9FFE7B0E1` | `Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md:61-62`; `Unit-Definition/CONTRACT-battle-unit-construction.md:90` |
| S-10 | **Definition table strides.** The enemy row stride for `02EBF120` and the strides of `02EBF150`, `02EBF148`, `02EBF140` and `02EBF168` are missing. | "`row = 02EBF120.base + r12 × stride`" with no stride value; party rows are "the descriptor's word `+8`" | `Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md:104`, `:349` |
| S-11 | **Level growth.** The per-level stat growth that `0030C650` applies is missing. | "growing `+0x08`–`+0x1C` per level as the level-up page §4 reads" (another category) | `Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md:188` |
| S-12 | **The camera player and shake sampler effects.** `00257230` (side A post-bind), `0037DCF0` (side B post-bind) and `00257830` (A reset tail) are not described. Also missing: the `0037D1F0` formula, the `const(01DFE0BC)` value, and the role of `003DA000`. `003DA000` writes the side-A table (`Actor-Manager-Record/the-actor-manager-record-field-map.md:97-98`, `:122`, `:126-131`) and is not among the contract's eight entries (`CONTRACT-manager-slot-entry-tables.md:9`). | strides only: "`ecx x 0xBB0` record base + `r8d` sign gate"; "`ecx x 0x3D0` into `02ADD980`" | `Actor-Manager-Record/the-actor-manager-record-field-map.md:614`, `:624`, `:630`; `CONTRACT-manager-slot-entry-tables.md:427` |
| S-13 | **Per-actor frame ordering on the battle side.** It is not stated where `00265A20` (bind), the unit frame callback and the definition install sit relative to the field pass within one frame. | the install's triggers only (script verb, teardown, area transition, save rebind) | `Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md:404`, `:425`, `:732` |
| S-14 | **Flag-bit semantics for the battle unit.** Most of the 43 bit rows in `Battle-Unit/the-battle-unit-field-map.md` §2.5 carry only setter, clearer and tester sites. | "What each bit *means* is still open per bit" | `Battle-Unit/the-battle-unit-field-map.md:313-362`, `:598-599` |
| S-15 | **The `0x1A`/band gate polarity per call site.** A port must know which of the 27 band sites include and which exclude. | "**the sense differs by call site**"; only five functions named in §3 | `Battle-Record-Kind/battle-record-kind-byte.md:895-896`; `Battle-Record-Kind/actor-type-id-partition-and-the-13-value-band.md:101-104`, `:149-150` |
| S-16 | **The per-character block `02089378 + index × 0x170`** (party `+0x6E0`) and **the constant `01E09350`** (party `+0x6F0`). | addresses only | `Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md:132-133` |
| S-17 | **The NPC name flag setter.** `PersistentFlag_SetBank2048`'s address and the `0051ED10` loader contract. | the call shape only | `Actor-Names/the-npc-name-dictionary.md:44-46`, `:83` |
| S-18 | **StatusView inputs.** What `003879C0`'s class-row `+0x12` bit 7 and `0030C2C0`'s callees (`003278C0`, `002FEAD0`) mean. (The effective action id `00387090` *is* stated, at `README.md:72`.) | named with their bit positions only | `Unit-Display-Record/the-record-00329220-builds.md:65`, `:148-149` |
| S-19 | **Order of the initialiser's stores after `002665EB`.** The free-list build, the wait-slot clear and the `+0x1C` blocks are given by address only. | "the index store … is at `002665EB`, after six record stores"; the later calls by address | `Actor-Storage-Record/the-record-behind-every-actor.md:109`, `:1189` |
| S-20 | **Census completeness for the wait slot.** The route-seeded `actor-wait-slot-accesses.tsv` holds 14 rows at displacements `0x0`/`0x8`/`0x10`/`0x14`/`0x16`. It holds none of the resolver's `+0x14`/`+0x27` stores or the `+0x22` cursor that `the-field-runtime-pass.md` lists. A port that trusts the census misses writers. | the page lists the stores itself | `the-field-runtime-pass.md:427`, `:741` |
