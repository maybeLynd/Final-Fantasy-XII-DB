# Reconstruction readiness — `FFXII TZA/04-Actor-Entity/`

| | |
|---|---|
| Stream | R (reconstruction readiness), per [`docs/cloud-briefs/re-readiness.md`](../../docs/cloud-briefs/re-readiness.md) |
| Board task | `OPUS-CLOUD-R-READINESS-04-1002` |
| Date | 2026-10-02 |
| Snapshot | this repo's text snapshot only (`df2c9f47`); no executable, Ghidra or live game was used. Several 04 pages are being edited by other lanes; every quotation is the text **as the snapshot has it** |
| Status of this file | **draft / pointer**. Nothing here is evidence. Every item is a quotation or a paraphrase of a page, with its location. |

**Counts:** 18 pages read in full (17 system pages + `README.md`, 16,027 lines); 24 member `.tsv` files checked for layout and row count only · **36 entry-point rows** mapped (10 record construction, 5 manager slot, 5 field pass, 13 battle unit and definition, 3 names) · **28** self-stated open gaps + **20** structural gaps · **contradictions: 52 value-changing** (§3.1: 9 with a favoured side settled by a dated correction — C-V3, C-V14, C-V15, C-V16, C-V32, C-V43, C-V44, C-V45, C-V50 — and 43 with no favoured side; all 52 are "page-text only - needs local check") **+ 20 value-changing counts and census figures** (§3.2) **+ 56 stale / struck-but-repeated** (§3.3) **+ 13 banner** (§3.4) · **Rating: NOT YET** overall (names READY bar one address; BattleUnit pool, field pass, manager slot, kind byte and StatusView MOSTLY; unit construction, the actor record and the contexts NOT YET).

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
| `Actor-Storage-Record/actor-storage-record-accesses.tsv` | 1,130 (271 functions, 111 displacements) | no: `Actor-Storage-Record/the-actor-storage-record-field-map.md:53-55` states 1042 rows / 275 functions / 86 offsets (C-N1) |
| `Actor-Storage-Record/actor-record-offsets-observed.tsv` | 56 (highest offset `0x118`) | no: `Actor-Storage-Record/the-record-behind-every-actor.md:1512` says "all 70 offsets"; `Actor-Storage-Record/the-record-behind-every-actor.md:1540-1541` says the eight beyond `0x118` "are recorded in the TSV" (C-N9) |
| `Actor-Storage-Record/actor-storage-record-flags1c-initial-values.tsv` | 8 sequence rows + 1 comment | yes: matches the presets at `Actor-Storage-Record/the-record-behind-every-actor.md:309-311` and `Actor-Storage-Record/the-actor-storage-record-field-map.md:117` |
| `Actor-Storage-Record/actor-storage-record-flag-bit-writes.tsv` | 121,759 | yes: `Actor-Storage-Record/the-actor-storage-record-field-map.md:208` |
| `Actor-Storage-Record/actor-storage-record-flag-bits.tsv`, `actor-arg-proven-closure.tsv`, `actor-static-proven-bases.tsv`, `actor-resource-entry-accesses.tsv`, `actor-wait-slot-accesses.tsv`, `actor-sequence-descriptor-accesses.tsv`, `actor-definition-payload-accesses.tsv` | 88 / 251 / 48 / 82 / 14 / 3 / 7 | layout only; the wait-slot file has none of `0025DF00`'s `+0x14`/`+0x27` stores that `the-field-runtime-pass.md:741` lists (S-20) |
| `Battle-Unit/battle-unit-accesses.tsv` | 2,205 (345 functions) | no: `Battle-Unit/the-battle-unit-field-map.md:59-61` states 2203 rows / 342 functions; `Battle-Unit/the-battle-unit-field-map.md:643` "the committed 2,207 in 344" (C-N4) |
| `Battle-Unit/battle-target-buffer-accesses.tsv`, `battle-target-result-entry-accesses.tsv`, `navigation-path-state-accesses.tsv` | 68 / 4 / 14 | no count stated on any page |
| `Actor-Manager-Record/actor-manager-record-accesses.tsv` | 204 | no: `Actor-Manager-Record/the-actor-manager-record-field-map.md:409` "holds **194** rows today" (C-N11) |
| `Actor-Manager-Record/actor-manager-record-rip-accesses.tsv`, `actor-manager-slot-accesses.tsv`, `actor-manager-slot-entry-accesses.tsv` | 113 / 330 / 26 | not cited by any page; `Actor-Manager-Record/the-actor-manager-record-field-map.md:55` gives the array route as "51 / 31 / 17" |
| `Actor-Contexts/movement-context-accesses.tsv` | 708 (124 displacements, no `chain:0xB8` rows) | no: `Actor-Contexts/the-movement-and-secondary-context-censuses.md:19-20` "1,028 rows, 122 distinct displacements; chain-only rows carry route `chain:0xB8`" (C-N12) |
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
| `+0x88` / `+0x89` | u8 | wait-slot count / resource-entry count: "`n88` = 8, or 6 when `sub == 1`; `n89` = 10, or 8 when `sub == 1`" | `Actor-Storage-Record/the-record-behind-every-actor.md:1631` |
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
  - `+0x27` set by kinds 3, 6 and 7 and "nothing reads `+0x27` as the settled flag" (`the-field-runtime-pass.md:484-489`, `:348`).
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
7. **Unload.** `002628B0`: semantic release, then the pool release. "when `002628B0` runs in an ordinary session, how often" is not
   established (`Actor-Storage-Record/the-record-behind-every-actor.md:2347-2349`).

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
| S-18 | **StatusView inputs.** What `003879C0`'s class-row `+0x12` bit 7 and `0030C2C0`'s callees (`003278C0`, `002FEAD0`) mean. (The effective action id `00387090` *is* stated, at `README.md:72`.) | named with their bit positions; `002FEAD0` is measured at the bit level only (`Unit-Display-Record/the-record-00329220-builds.md:427-435`) | `Unit-Display-Record/the-record-00329220-builds.md:65`, `:148-149` |
| S-19 | **Order of the initialiser's stores after `002665EB`.** The free-list build, the wait-slot clear and the `+0x1C` blocks are given by address only. | "the index store … is at `002665EB`, after six record stores"; the later calls by address | `Actor-Storage-Record/the-record-behind-every-actor.md:109`, `:1189` |
| S-20 | **Census completeness for the wait slot.** The route-seeded `actor-wait-slot-accesses.tsv` holds 14 rows at displacements `0x0`/`0x8`/`0x10`/`0x14`/`0x16`. It holds none of the resolver's `+0x14`/`+0x27` stores or the `+0x22` cursor that `the-field-runtime-pass.md` lists. A port that trusts the census misses writers. | the page lists the stores itself | `the-field-runtime-pass.md:427`, `:741` |

---

## 3. Contradictions (statements a re-implementer would have to choose between)

Quotes are exact as the snapshot has them; `…` marks an elision only. "Favoured" is named only where a dated correction
on the pages settles the point. Otherwise the item says **no favoured side**, and any supporting evidence the pages
offer is noted without choosing.

The section has four parts:
- **§3.1** — value-changing items that change what a port would compute: offsets, addresses, constants, formulas,
  control flow.
- **§3.2** — value-changing counts and census figures. These do not change a port's arithmetic, but they change what
  a checker would expect.
- **§3.3** — stale "not read / open" claims, and corrected claims still repeated unstruck.
- **§3.4** — status banners against front matter.

### 3.1 Value-changing (offsets, addresses, constants, formulas, control flow) — page-text only - needs local check

Every item in this subsection is **page-text only - needs local check**, including those with a favoured side: the
favoured side is the one the pages' own dated correction picks, not one checked against the executable.

#### The actor record and its pool

**C-V1. What the two fields of `+0x03` are called: "kind" low and "sequence" high, or the reverse.**
- Side A: `Actor-Storage-Record/the-actor-storage-record-field-map.md:279-280`: "`(old & 0xE0) | (kind & 0x1F)`, then `| (sequenceByte << 5)` — the packed kind (low 5
  bits) and sequence (high 3)".
- Side B:
  - `CONTRACT-actor-record-pool-and-region-map.md:168`: "the three high bits are the kind and do not reach the dispatch".
  - `CONTRACT-actor-record-pool-and-region-map.md:184`: "`r9b = i & 0x1F, the GROUP index`".
  - `CONTRACT-actor-record-pool-and-region-map.md:193`: "**`record[+3] = (kind << 5) | (i & 0x1F)`.**"
  - `CONTRACT-actor-storage-record-initialisation.md:155`: "`(kindCode << 5) | (sequence & 0x1F)`".
- Side B also covers the record page's two wordings of the low five bits:
  - `Actor-Storage-Record/the-record-behind-every-actor.md:313-314`: "`+0x03`'s low five bits are **the row index into that table**";
  - `Actor-Storage-Record/the-record-behind-every-actor.md:1446`: "`record[+0x03] = (kindCode << 5) | (sequenceWithinKind & 0x1F)`".

  A row index into the eight-entry table and a "sequence within kind" are different quantities. A per-kind sequence
  restarts at 0 for each kind; a row index runs 0–7 across the table.
- Status: **no favoured side.** The pool contract's table is backed by execution, but no dated correction strikes
  the field map's line.
- Why it matters: every class-3 gate tests `(byte[+3] & 0xE0) == 0x60` (`Actor-Storage-Record/the-actor-storage-record-field-map.md:401-402`), and the region map
  dispatches on `& 0x1F` (`CONTRACT-actor-record-pool-and-region-map.md:168`). Swapping the fields, or numbering the low field per kind, breaks both.

**C-V2. Which `sub` value gives the `0xA0` wait-array step, and the size of a sequence-7 record.**
- Side A, `Actor-Storage-Record/the-record-behind-every-actor.md:1974` (2026-09-16): "`00266B8C` loads **`0xC8`** if it matches and `00266B93` **`0xA0`** if it does
  not … **8 × `0x14` wherever that byte is not 1** - which moves `waitSlotArray` to `+0x578` and makes the whole
  record **`0x6B8`, not `0x6E0`**".
- Side B:
  - `Actor-Storage-Record/the-record-behind-every-actor.md:1612-1613`: "`sub == 1` gives `0xA0`."
  - `Actor-Storage-Record/the-record-behind-every-actor.md:1647`: "| 7 | `0x668` | `0x4D8`, 8 × `0x14` | `0x578`, 6 × `0x28` |".
  - `CONTRACT-actor-record-pool-and-region-map.md:144`: "`+0xA8 = +0xA0 + (subFlag ? 0xA0 : 0xC8)`".
  - The live table, `Actor-Storage-Record/the-record-behind-every-actor.md:2520`: "| record extent | `0x6E0` | `0x668` |".
- Status: **no favoured side by dated correction.**
  - Side A is the latest dated text.
  - Side B carries the executed region-map pilot and the EXP-026 live observation (`CONTRACT-actor-record-pool-and-region-map.md:372-374`, `:446-453`).
  - Side A also pairs the `0xA0` step with 8 wait slots. The table pairs it with 6 slots ("**`n88` = 8, or 6 when
    `sub == 1`**", `Actor-Storage-Record/the-record-behind-every-actor.md:1631`), so `0x578 + 6×0x28 = 0x668`.
- A port that follows side A mis-sizes every sequence-2, -4 and -7 record.

**C-V3. Address of the slot-index store.**
- Side A: `Actor-Storage-Record/the-record-behind-every-actor.md:109`: "the index store `mov word ptr [rbx], r10w` is at `002665EB`, after six record stores".
- Side B: `Actor-Storage-Record/the-record-behind-every-actor.md:2853`: "| `+0x00` is the slot index | `0026656B mov word ptr [rbx], r10w` |".
- Status: **favoured: side A.** It is a dated correction ("Corrected 2026-09-29, OPUS, … `CON-168`", `Actor-Storage-Record/the-record-behind-every-actor.md:109`),
  and `CONTRACT-actor-storage-record-initialisation.md:86` agrees. The falsification table at `Actor-Storage-Record/the-record-behind-every-actor.md:2853` is unstruck.

**C-V4. Is `& 0xFFFFDEFF` on `+0x1C` an initialiser instruction?**
- Side A: `Actor-Storage-Record/the-record-behind-every-actor.md:76`: "`002666F1  and dword ptr [rbx + 0x1C], 0xFFFFDEFF  ; clear bits 8 and 13`". The same address
  appears in `Actor-Storage-Record/the-actor-storage-record-field-map.md:80` as one of the initialiser's `+0x1C` stores.
- Side B: `Actor-Storage-Record/the-record-behind-every-actor.md:287-289`: "**So `EH-4`'s `&0xFFFFDEFF` is not an initialiser mask at all** — the route-proven census
  puts it at `00265AC3`, in `ActorSystem_BindBattleUnitsForEligibleRecords`, and the second copy is `0026A003`."
- Status: **no favoured side.** Either there are three sites (with `002666F1`) or the §2 listing is wrong.
- This decides whether a freshly constructed record has `+0x1C` bits 8 and 13 clear before the presets.

**C-V5. Does the initialiser itself write inside `+0x60`–`+0xB8` and `+0xC0`–`+0xEC`?**
- Side A, `CONTRACT-actor-storage-record-initialisation.md:91-92`: "Six spans — including 88 bytes at `+0x60`–`+0xB8` and 44 at `+0xC0`–`+0xEC` — are … **not
  touched by `00266530`'s own stores**". The 2026-09-29 falsification row, `CONTRACT-actor-storage-record-initialisation.md:241`, says it "**survives**: the
  body's own stores end at `0x11C` and touch neither `+0x60`-`+0xB7` nor `+0xC0`-`+0xEB`".
- Side B, `CONTRACT-actor-record-pool-and-region-map.md:294-295`: "`rep stosw` with `ecx = 0x12` writes `0xFFFF` over `+0xC8`–`+0xEB` at `002668B0`".
  `002668B0` lies inside `00266530`'s 1,439 bytes. `Actor-Storage-Record/the-record-behind-every-actor.md:134-135` and `Actor-Storage-Record/the-actor-storage-record-field-map.md:205` also call `+0xC8`–`+0xEB` a
  `u16[18]` override array the constructor fills.
- Status: **no favoured side.** The later contract pass does not address the `rep stosw`.
- The answer decides the initial value of the override array (`0xFFFF` = "not overridden").

**C-V6. The per-sequence table at `0x01E0C328`: what byte `+0x01` is, and how many entries there are.**
- Side A:
  - `CONTRACT-actor-record-pool-and-region-map.md:54`: "| `+0x01` `u8` | the **sub flag**, `0` or `1` — selects `0xC8` or `0xA0` in the region map |".
  - `CONTRACT-actor-record-pool-and-region-map.md:225`: "**So `01E0C328` is eight entries by data, not by construction.**"
  - `Actor-Storage-Record/the-record-behind-every-actor.md:1612-1613` agrees (the "**`sub`** field").
- Side B:
  - `CONTRACT-actor-storage-record-initialisation.md:164`: "4-byte entries `{u8 classByte, u8 pad, u16 stride}`".
  - `CONTRACT-actor-storage-record-initialisation.md:178`: "| 8–11 | `0x14`/`0x02`/`0x14`/`0x1A` | `0x0000` | — | reserved — no records carved |".
- Status: **no favoured side.** A port that treats `+0x01` as padding loses the `0xA0`/`0xC8` choice (C-V2).

**C-V7. Where the region map points `+0xB8`/`+0xC0`, per class.**
- Side A: `Actor-Storage-Record/the-actor-storage-record-field-map.md:195-197`: "points `+0xB8` / `+0xC0` **into the record's own embedded area at `+0x120`** (`+0x120`,
  `+0x120 + 0x80`, `+0x120 + 0x20`, `+0x120 + 0x230` by kind; …) … jump table at `00266AE7`".
- Side B: `CONTRACT-actor-record-pool-and-region-map.md:137-142`, the arm table: `+0xB8` = NULL / `rec+0x120` / `rec+0x120` / `rec+0x120`; `+0xC0` = NULL /
  NULL / NULL / `rec+0x350`. Side B's jump table is `00266BA4` (`Actor-Contexts/the-movement-and-secondary-context-censuses.md:439`).
- Status: **no favoured side by dated correction.** The pool contract's falsification pass says the map "**holds,
  every cell**" (`CONTRACT-actor-record-pool-and-region-map.md:725`), but it does not amend the field map.

**C-V8. The manager's record range: which of `+0x1D6`/`+0x1DE` is the start and which the count.**
- Start `+0x1D6`, count `+0x1DE`:
  - `Actor-Storage-Record/the-record-behind-every-actor.md:211`: "`+0x1D6`…`+0x1D6 + 0x1DE`";
  - `Actor-Manager-Record/the-actor-manager-record-field-map.md:1044`: "iterates slots `[+0x1D6] .. +0x1D6+[+0x1DE]`".
- Start `+0x1DE`, count `+0x1D6`:
  - `Actor-Storage-Record/the-record-behind-every-actor.md:658`: "each ordinal in `[+0x1DE, +0x1DE + +0x1D6)`";
  - `Actor-Manager-Record/the-actor-manager-record-field-map.md:1032`: "`word[+0x1DE]` to `word[+0x1DE] + word[+0x1D6]`".
- A third pair: `Actor-Contexts/the-movement-and-secondary-context-censuses.md:550`: "range `word[rcx+0x1DA]` through `word[rcx+0x1D2] + count`".
- Status: **no favoured side.** `Actor-Storage-Record/the-record-behind-every-actor.md:1392` and `:1402` place per-kind counts at `+0x1D0` and prefix sums at
  `+0x1D8`, which would make `+0x1D6` count[3] and `+0x1DE` start[3]. No page draws that conclusion.

**C-V9. Initial value of `+0x08` after construction.**
- Side A: `Actor-Storage-Record/the-record-behind-every-actor.md:894`: "`+0x08` keeps its prior value with only bit 7 cleared (`002665BA`, `0026667A`)".
- Side B: `Actor-Storage-Record/the-record-behind-every-actor.md:573-575`: "**`00266607 and dl, 0xDF` clears bit 5 between the first store and the second**, so the
  value left at the end of construction has bit 5 clear".
- Status: **no favoured side.** Both are on the record page.

**C-V10. Which `+0x1C` indices the engine reads.**
- Side A: `Actor-Storage-Record/the-record-behind-every-actor.md:1123`: "0, 2, 3, 4, 5, 6, 7, 10, 11, 13, 14, 16, 17". Index 8 is not in the list.
- Side B: `Actor-Storage-Record/the-record-behind-every-actor.md:304`: "`(dword[+0x1C] & 0x2100) != 0` (`003DF73A`)". That is a read of bits 8 and 13.
- Status: **no favoured side.**

**C-V11. Bank element type.**
- Side A: `Actor-Storage-Record/the-record-behind-every-actor.md:2662`: "What the bank's `u16` entries *mean* is still unknown for both".
- Side B: `Actor-Storage-Record/the-record-behind-every-actor.md:2724`: "the banks hold **`int16`**". The same section says the correction was routed
  (`Actor-Storage-Record/the-record-behind-every-actor.md:2758`).
- Status: **no favoured side by dated correction.** §23 and §24 carry the same date (2026-09-11, `Actor-Storage-Record/the-record-behind-every-actor.md:2597`,
  `Actor-Storage-Record/the-record-behind-every-actor.md:2665`).

**C-V12. Function sizes on the record page.**
- Side A:
  - `Actor-Storage-Record/the-record-behind-every-actor.md:166`: "| `00265FF0`, `00268380` | 1,339/420 B |";
  - `Actor-Storage-Record/the-record-behind-every-actor.md:167`: "| `00265B60`, `002681E0` | 1,067/230 B |".
  - `CONTRACT-actor-storage-record-initialisation.md:249` also gives `00265FF0` as "the 1,339-byte Movement body".
- Side B:
  - `Actor-Storage-Record/the-record-behind-every-actor.md:2940`: "`00265FF0` (~97 B)";
  - `Actor-Storage-Record/the-record-behind-every-actor.md:2928`: "`00265B60` (~90 B)".
- Status: **no favoured side.** The movement-context initialiser is either a 1,339-byte body or a ~97-byte frame op.

#### The manager slot and its entry tables

**C-V13. The `ActorManagerSlot` size.**
- Side A, the contract:
  - `CONTRACT-manager-slot-entry-tables.md:267`: "writes at `slot + 0x20C`, outside the `0x200` slot";
  - `CONTRACT-manager-slot-entry-tables.md:346`: "a store at `+0xF4`, inside the `0x200` slot";
  - `CONTRACT-manager-slot-entry-tables.md:495`: "comparing all 0x200 bytes".
- Side B:
  - `Actor-Manager-Record/the-actor-manager-record-field-map.md:29`: "Five 648-byte slots at `02098E10`";
  - `README.md:18`: "stride `0x288`";
  - `the-field-runtime-pass.md:542-543`: "**five** `ActorManagerSlot`s, `0x288` bytes each".
- Status: **no favoured side by dated correction.** Under side B, `slot + 0x20C` is inside the slot, in the
  bind-cleared `+0x204..+0x243` block (`Actor-Manager-Record/the-actor-manager-record-field-map.md:248`). The contract's "out-of-slot write" (`CONTRACT-manager-slot-entry-tables.md:595`) holds only for
  a `0x200` harness.

**C-V14. How side A validates the record index.**
- Side A: `CONTRACT-manager-slot-entry-tables.md:497`: "`003DA42C test edx,edx / js` — a SIGNED test — and `003DA434 cmp r8d, [rcx+4] / jae`".
- Side B: `CONTRACT-manager-slot-entry-tables.md:500`: "**re-read 2026-09-12**: side A uses one unsigned compare, `003DA434 cmp r8d, [rcx+4]` /
  `jae`, which rejects negatives by itself".
- Status: **favoured: side B**, by the dated re-read. Side A's row is still unstruck in the same evidence table.

**C-V15. Does one bind serve both sides?**
- Side A: `CONTRACT-manager-slot-entry-tables.md:212`: the generic `bind(…, SIDE)` formula with "`call 00257230(slot->0x28)`" for both sides.
- Side B:
  - `CONTRACT-manager-slot-entry-tables.md:49`: "after the field writes **the two call different functions** — A `00257230`, B `0037DCF0`."
  - `CONTRACT-manager-slot-entry-tables.md:591`: "**Do not write one bind with a side parameter.**"
- Status: **favoured: side B.** It sits under the dated banner "CHECKED 2026-09-11" (`CONTRACT-manager-slot-entry-tables.md:32`), and the page's own
  instruction to implementers repeats it.

**C-V16. What a negative fifth argument produces on the two sides.**
- Side A: `CONTRACT-manager-slot-entry-tables.md:501`: "**executed** with the same negative value on both sides — the entry's `+0x04` and the call
  trace both differ".
- Side B: `CONTRACT-manager-slot-entry-tables.md:48`: "*Corrected 2026-09-26 …* side B always gets 0, the zero side A substitutes. The slots end up
  identical".
- Status: **favoured: side B** (dated correction).

**C-V17. Who writes slot `+0x000`.**
- Side A: `Actor-Manager-Record/the-actor-manager-record-field-map.md:90` lists the `+0x000` writers as "`003DD1F0` (`003DD1FB`); `003DA2D0` (`003DA2DB`)".
- Side B: `CONTRACT-manager-slot-entry-tables.md:433-436`: those are the rate setters, which store "`movss [slot + (ch+0xC)*24], xmm2`" and
  "`(ch+0x10)*24`", that is entry `+0x10` of the two tables. `CONTRACT-manager-slot-entry-tables.md:439` explains the census folding ("displacement
  `0`").
- Status: **no favoured side by dated correction.** The field-map row is a census artefact the field map does not
  flag.

**C-V18. Shake-table base.**
- Side A: `Actor-Manager-Record/the-actor-manager-record-field-map.md:871`: "`0037D212  lea    rax, [rip + 0x2760777]  ; 02ADD990  <- THE BASE`".
- Side B: `Actor-Manager-Record/the-actor-manager-record-field-map.md:630`: "`0037DCF0` | `ecx x 0x3D0` into `02ADD980`".
- Status: **no favoured side.** The two bases differ by `0x10` with the same stride.

**C-V19. The foreign `0x860` presentation array: base and extent.**
- Side A: `Actor-Manager-Record/the-actor-manager-record-field-map.md:245`: "the `lea` at `00259652` → `020994E8` is the loop bound of a foreign `0x860`-stride array at `02098428`".
- Side B: `README.md:74`: "two `0x860`-byte presentation slots based at `02098378`".
- Status: **no favoured side.** As stated, either extent reaches past `02098E10`, the start of the five-slot array.
  `02098428 + 2×0x860 = 020994E8`, and `02098378 + 0x10C0 = 02099438`. Neither page notes the overlap.

**C-V20. Which `+0xC0` the "no record" link reads.**
- Side A: `Actor-Manager-Record/the-actor-manager-record-field-map.md:645-647`: "The `0xC0` link is the secondary context record this map's own `+0xC0` entries
  describe".
- Side B:
  - the slot map's own `+0x0C0` is a 4-byte field written by `003E92F0` (`Actor-Manager-Record/the-actor-manager-record-field-map.md:112`);
  - the secondary-context pointer is the **actor record's** `+0xC0`: "`+0xC0  ptr -> +0x350   SecondaryContext
    (0x188)`" (`Actor-Contexts/the-movement-and-secondary-context-censuses.md:307`).
- Status: **no favoured side.** It is an object-identity conflict, of the kind the field map's own modding note warns
  about.

**C-V21. Slot widths: `+0x010` and `+0x1E0`.**
- Side A, `Actor-Manager-Record/the-actor-manager-record-field-map.md:92`: "| `+0x010` | 1 | u32 |". `Actor-Manager-Record/the-actor-manager-record-field-map.md:145`: "| `+0x1E0` | 4 | u64 |", and `Actor-Manager-Record/the-actor-manager-record-field-map.md:292`: "+0x1E0 u64
  zeroed at bind".
- Side B, the accesses: `+0x010` is tested as a byte (`Actor-Manager-Record/the-actor-manager-record-field-map.md:582`). FH-1 lists "the counters +0x24 / +0x38 / +0x1E0 /
  +0x1E4" as separate fields (`Actor-Manager-Record/the-actor-manager-record-field-map.md:316`), which a u64 at `+0x1E0` would overlap.
- Status: **no favoured side.**

**C-V22. Is `+0x68`–`+0x97` reached?**
- Side A: `Actor-Manager-Record/the-actor-manager-record-field-map.md:199-200`: "The ones of 32 bytes or more: `+0x68`–`+0x97` (48 B), `+0x244`–`+0x287` (68 B)." This
  is after saying "the eight bind-zeroed qwords counted as covered", and those qwords are `+0x244`–`+0x27C`.
- Side B:
  - `Actor-Manager-Record/the-actor-manager-record-field-map.md:78`: the bind "fills the pointer block `+0x50` / `+0x58` / `+0x60` / `+0x68`";
  - `Actor-Manager-Record/the-actor-manager-record-field-map.md:331-333`: `+0x70`, `+0x80` and `+0x78` are written from the image.
- Status: **no favoured side**, but side A is unstruck against the page's own §2.2 and FH-2.

#### The battle unit and its pool

**C-V23. The channel table address.**
- Side A: `battleunit-slot-pool-and-actor-class.md:422`: "`&DAT_02EBF1A0` is cleared as **12 quadwords (96 bytes)**". The front matter's
  `registry_slots` is `"0x02EBF1A0"` (`battleunit-slot-pool-and-actor-class.md:19-20`).
- Side B: `battleunit-slot-pool-and-actor-class.md:630`: "12-qword channel table at `02EFF1A0` (`rep stosq`, 0xC qwords)".
- Status: **no favoured side.** The two addresses differ in one hex digit.

**C-V24. `0208E6A0` and the `0xEA7900` multiplier.**
- Side A: `Battle-Unit/the-battle-unit-field-map.md:531`: "`0208E6A0` the slot count factor (`0xEA7900` per bank)".
- Side B:
  - `battleunit-slot-pool-and-actor-class.md:354`: "`g_nBattleUnitSlotCount` lives at **`0x0208E6A0`**";
  - `battleunit-slot-pool-and-actor-class.md:365`: "`g_nBattleUnitSlotCount = 0x20;`".
  - The release bounds check, `battleunit-slot-pool-and-actor-class.md:796`: "`imul    rcx, rax, 0xEA7900       ; the pool extent`". `battleunit-slot-pool-and-actor-class.md:805` reads it
    as "the slot must lie between the base and `base + count × 0xEA7900`".
- Status: **no favoured side.** `0xEA7900` is `0xF50 × 0xF50` (arithmetic only). The pages' stride is `0xF50` and the
  pool is `0x1EA00` bytes (`battleunit-slot-pool-and-actor-class.md:376`), so a bound of `count × 0xEA7900` is not the pool extent as stated.
- A port must decide what the release check rejects.

**C-V25. Does the binder write the actor's `+0x30` back-pointer?**
- Side A, `battleunit-slot-pool-and-actor-class.md:130-131`: "the allocator plants the unit back-pointer at the actor's `+0x30` (`002134A0`, on the
  success path only, `002344E7`)". `battleunit-slot-pool-and-actor-class.md:463` gives "the bind writes **`ActorStorageRecord +0x30 = BattleUnit*`**".
- Side B: `battleunit-slot-pool-and-actor-class.md:736-737`: "all six pool-base readers store nothing and touch no offset in the span; **the binder
  writes no back-pointer**, which closes the `actorWork` route as well."
- Status: **no favoured side.** Side B is probably scoped to "a back-pointer into the actor record" inside the unit
  span (`battleunit-slot-pool-and-actor-class.md:734-735`), but as written it contradicts §11.

**C-V26. Battle-unit flag bit 21: cleared or set at bind.**
- Side A: `Battle-Unit/the-battle-unit-field-map.md:84`: "bit 21 cleared at bind".
- Side B: `Battle-Unit/the-battle-unit-field-map.md:334`, the bit table: "| 21 | `0x200000` | `SpawnUnit_BindEntryAndMarkCapTracked` `00239840`
  (`002398D1`) |  |". The bind is in the setter column and no clearer is listed.
- Status: **no favoured side.**

**C-V27. Which bit `00233AD0` sets.**
- Side A: `Battle-Unit/the-battle-unit-field-map.md:1241-1243`: "`+0x48`/flag-word writes set `ACTIVATION_COMMITTED` (bit 1) as documented in the flag
  table above."
- Side B: the flag table:
  - `Battle-Unit/the-battle-unit-field-map.md:316`: bit 1's only setter is "`BattleUnit_TeardownAndDespawn` `00300E40` (`00300F2A`)";
  - `Battle-Unit/the-battle-unit-field-map.md:318`: bit 3's setter is "`BattleUnit_ActivateAppliedDefinitionRuntime` `00233AD0` (`00233B4B`)".
- Status: **no favoured side.**

#### Unit construction and the stats record

**C-V28. What the installer stores at unit `+0x52`.**
- Side A: `Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md:119`: "*The class row's word `+0x52` (2026-09-12, FABLE):* the installer copies it to unit `+0x52`".
- Side B: `Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md:143`: "`+0x52 = word +6 (or −1)`".
- Also relevant: `Battle-Unit/the-battle-unit-field-map.md:399` says unit `+0x052` comes from "its stack slot `+0x80` … Which definition field feeds the
  stack slot is not traced", and the display builder reads class-row `+0x52` directly from `[unit+0xE68]`
  (`Unit-Display-Record/the-record-00329220-builds.md:80`).
- Status: **no favoured side.** Side A is dated, but it does not strike side B.

**C-V29. Is unit flag bit 43 ever read?**
- Side A: `Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md:305-307`: "the installer's register-path write is the only known access and the bit is, as far as
  the image shows, unread". `Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md:505` repeats this ("bit 43 has no immediate accessor anywhere in the image").
- Side B: `Unit-Display-Record/the-record-00329220-builds.md:63`: "`0031FDA0(unit)` (106 B): **"unavailable"** — 1 when the unit is null, its flag bit 4 is clear
  or bit 43 set (`0031FDA8`–`0031FDBA`)".
- Status: **no favoured side.** These cannot both hold.

**C-V30. Readers of the spawn record's `+0x12`.**
- Side A: `Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md:496`: "the `+0x12` copy is read once, by `BattleUnit_RefreshActorRuntimeFromDefinition`".
- Side B: `Unit-Display-Record/the-record-00329220-builds.md:80` builds view `+0x88` from "spawn record `+0x12`", which is a second reader (`00329220`).
- Status: **no favoured side.**

**C-V31. The spawn counter at its cap.**
- Side A: `Unit-Definition/CONTRACT-battle-unit-construction.md:119-120`: "the word count increments or wraps to 1 at the cap; retained fixtures exercise
  `0x10->0x11` and" … "`0x34->1`".
- Side B: `Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md:374`: "`if (c < threshold) counters[k] = c + 1`", with no else branch. `Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md:109` is the same.
- Status: **no favoured side by dated correction.** Side A cites executed fixtures.

**C-V32. Party definition table row size.**
- Side A: `Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md:129`: "the party table (the registry page records its 456-byte rows and declines to name it)".
- Side B: `Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md:349`: "~~456-byte rows~~ rows of the descriptor's word `+8` bytes, 128 in the shipped
  `battle_pack.bin` *(corrected 2026-10-02, OPUS …)*".
- Two more figures:
  - `Battle-Record-Kind/actor-type-id-partition-and-the-13-value-band.md:248` and `Battle-Record-Kind/battle-record-kind-byte.md:284` give "40 rows × 128 bytes" for the same table.
  - `Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md:349` says 128 *rows*.
- Status: **favoured: side B** for the row size, by the dated correction. The row *count* (40 against 128) is not
  reconciled.

**C-V33. The tracked-HP table at `02EC1380`.**
- Side A: `Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md:259-260`: "two 24-byte entries `{+0 slotIndex, +4 code, +8 HP, +0xC maxHP, +0x10 MP, +0x14 stats
  +0x28}`". `Unit-Definition/CONTRACT-battle-unit-construction.md:135` gives "stride 24".
- Side B: `Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md:666`: "`02EC1380`–`02EC13A8`: head/tail pointers + two `-1` id dwords" with "`mov dword [02EC1398],
  -1`".
- Status: **no favoured side.** `0x28` bytes is less than 2 × 24. Under stride 24, `02EC1398` is entry 1's `+0`.

**C-V34. When the installer reads the old id.**
- Side A: `Unit-Definition/CONTRACT-battle-unit-construction.md:93`: "The old word at stats `+4` is read before reset when unit bit2 is set."
- Side B: `Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md:60-61`: "remembers the unit's previous id (`+0x698` word `+4`, `0023A5A1`–`0023A5A8`, `0xFFFF` when
  the unit has no record)".
- Status: **no favoured side.**

**C-V35. How the rekey re-points the leader selector.**
- Side A: `Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md:74-76`: "if the party-focus record's `+0x08` held the old one (`00327150`, …), re-points the leader
  selector at `02EBF190 + 0x5AA4` to the re-keyed unit's type byte".
- Side B: `Unit-Definition/CONTRACT-battle-unit-construction.md:236-238`: "match on the occupant's `d[+8]` == old id always stores `d[glob+0x5AA4]` (DWORD — clobbers
  +0x5AA5..7)", executed as EXP-151.
- Status: **no favoured side by dated correction.** The two differ on the store width (byte or dword), the match
  object, and whether `02EBF190` is dereferenced.

**C-V36. Is an enemy (kind-1) stats record grown by the level grower?**
- Side A: `Unit-Definition/CONTRACT-battle-unit-construction.md:298-299`: "`b[rec+5]` suppresses growth+tail, `r8&2` suppresses the tail only".
- Side B: `Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md:184`: "kind 1 … **`+0x88 = kind` (u8)** … then straight to the growth".
- Status: **no favoured side.** Stats `+5` is the kind byte (1 for enemies), so side A suppresses enemy growth and
  side B performs it.

**C-V37. Which callers pass which id.**
- Side A: `Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md:96-98`: the enemy row index is "the definition id the callers pass (`Spawn_ApplyScriptSelectedUnit`
  … with the script-selected id, `BattleGroup_RefreshFourActorDefinitions` with 0)".
- Side B: `Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md:84-85`: "high byte 0  -> the PARTY path". An id of 0 cannot select an enemy row.
- Status: **no favoured side.**

**C-V38. `00329210` against `00329220`, and what `00861EC0` is.**
- Side A: `Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md:776`: "| `00329210` | recompute battery — `lea 0208D328` (`00329213`), `00861EC0` free, …
  `003588B0`/`00263E30`/`003135E0`/`00313800` chain (`003292BF`–`003292EA`)".
- Side B:
  - `Unit-Display-Record/the-record-00329220-builds.md:60-62` places those same sites inside `00329220` (1,933 B).
  - `Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md:610` calls `00861EC0` the memset ("`0023ACA4 mov r8d, 0x1c8` feeding `call 00861EC0`").
- Status: **no favoured side.**

#### Kind byte, type id and names

**C-V39. The valid spawn-definition id range.**
- Side A: `Battle-Record-Kind/battle-record-kind-byte.md:521`: "| definition id | a **single byte**, `0x00`–`0xFE`; `0xFF` means empty |".
- Side B: the same page's code, `Battle-Record-Kind/battle-record-kind-byte.md:510`: "`if (id == 0xFF || (int8)id < 0)     return NULL;`". This also rejects
  `0x80`–`0xFE`.
- Status: **no favoured side.**

**C-V40. Which function seeds the free-target nibble.**
- Side A: `Battle-Record-Kind/battle-record-kind-byte.md:304-306`: "records initialise to **4** (kind 1, `002663A3`) or **5** (kind 3,
  `002660D3`–`002660DE`) in `00265FF0`".
- Side B: `Battle-Record-Kind/battle-record-kind-byte.md:362` (GR-2, 2026-09-30/10-01): "the record initialiser `002666F8` (0, then 4 for kind 1 or 5 for kind
  3)". `Actor-Names/the-npc-name-dictionary.md:162` places a neighbouring initialiser store "`002666C1`, in `00266530`".
- Status: **no favoured side.** GR-2 is later, but it answers a different question and does not strike AL-3's
  addresses.

**C-V41. Reks: main roster or guest.**
- Side A: `Battle-Record-Kind/actor-type-id-partition-and-the-13-value-band.md:257`: "| main roster (`0x00`–`0x06`) | 0–6 | Vaan, Ashe, Fran, Balthier, Basch, Penelo — and **row
  6, Reks**: the prologue's playable is counted with the roster and earns LP |".
- Side B: `Battle-Record-Kind/battle-record-kind-byte.md:286-287`: "rows 0–5 Vaan, Ashe, Fran, Balthier, Basch, Penelo; 6–16 the guests (Reks, …".
- Status: **no favoured side.** The span test `<= 6` (`Battle-Record-Kind/actor-type-id-partition-and-the-13-value-band.md:47-61`) includes row 6, so the row's LP behaviour follows
  side A whatever it is called.

**C-V42. What global "the dictionary" is.**
- Side A: `Actor-Names/the-npc-name-dictionary.md:45`: the block is stored "at the global **`02B5E0D8`**".
- Side B: `Actor-Names/the-npc-name-dictionary.md:371-374`: `00282DF0` "loads the dictionary base `qword[0209AC30]` … and returns `base[idx*8 +
  0xAC8]`".
- Also relevant: `Unit-Display-Record/the-record-00329220-builds.md:209` says `00283270` "**keeps nine copies** at `[0209AC30] + 0x408 + i × 0xC0` (to `+0xAC8`"
  of the StatusView. So `[0209AC30]` is a UI object, and `+0xAC8` is the end of the StatusView copies.
- Status: **no favoured side.** The appendices from `Actor-Names/the-npc-name-dictionary.md:356` on describe world-map label code under the dictionary
  page.

#### The field runtime pass

**C-V43. Where the designated actor's ordinal comes from.**
- Side A: `CONTRACT-field-runtime-pass.md:229`: "`rec = ActorManager_GetRecordByOrdinal(b, *(uint16_t *)(actor + 0x50));`".
- Side B: `the-field-runtime-pass.md:137-139`: "*Corrected 2026-09-30 (FABLE): the first line read `ActorManager_GetRecordByOrdinal(actor,
  word [actor + 0x50])`. Both arguments come from the slot. … the ordinal is the word at `+0x50` of the slot's bound
  definition payload `[slot + 0x00]`".
- Status: **favoured: side B** (dated correction). The contract's reproduction formula is unamended.

**C-V44. What exit A writes to slot `+0x12`.**
- Side A: `CONTRACT-field-runtime-pass.md:232`: "`b[0x12] = (uint8_t)conj;`".
- Side B: `CONTRACT-field-runtime-pass.md:62` and `:127` (corrected 2026-09-26): "in the drive loop `r12d` was just set from `edi` = 0 at
  `0025DB2E`, so this CLEARS `+0x12`, ending the drive request the bind raised".
- Status: **favoured: side B** (dated correction on the same page). The formula is unamended.

**C-V45. Do the roster loop and the folds run after the designated drive?**
- Side A:
  - the formula at `CONTRACT-field-runtime-pass.md:231-235` closes exit A and then runs "the roster loop and the two folds" for both exits;
  - `CONTRACT-field-runtime-pass.md:188`: "the roster loop precedes the two folds, and the folds read a byte the drive loop may have
    changed".
- Side B:
  - `the-field-runtime-pass.md:141`: exit A "runs `002620E0` and jumps to the pass's tail (`0025DB82`)";
  - `CONTRACT-field-runtime-pass.md:145`: with `+0x12 == 0` the pass "skips the loop, and takes neither exit", which makes the designated
    drive and the roster/folds alternatives.
  - `CONTRACT-field-runtime-pass.md:127` says exit A "falls into the common tail".
- Status: **favoured: side B.** It is part of the 2026-09-30 corrected block at `the-field-runtime-pass.md:137-141`.

**C-V46. The slot argument of the deferred `0xD4` request.**
- Side A: `CONTRACT-field-runtime-pass.md:414`: "the deferred arm runs `dreq(1,0xD4)`".
- Side B: `CONTRACT-field-runtime-pass.md:182`: "slot 0 issues `WorldSimulation_ProcessDeferredModeRequest(0, 0xD4)` **once**". `the-field-runtime-pass.md:325`
  says the same ("once for slot 0 with index `0xD4`").
- Status: **no favoured side.**

**C-V47. Address of the dead-path call.**
- Side A: `CONTRACT-field-runtime-pass.md:120`: "`0025DB5A  call 003DB280`".
- Side B: `the-field-runtime-pass.md:130`: "`0025DB5D  call  0x3db280`".
- Status: **no favoured side.** `the-field-runtime-pass.md:161` begins the dead range at `0025DB5A`.

**C-V48. How many wait kinds the resolver arms.**
- Side A: `CONTRACT-field-runtime-pass.md:416`: "kind dispatch is `cmp eax, 7 / ja`, with kinds 0–8 all armed".
- Side B: `the-field-runtime-pass.md:659`: "it is an eight-case enum". `Actor-Storage-Record/the-record-behind-every-actor.md:1800` gives the 8-arm table `0025E3CC`.
- Status: **no favoured side.** "0–8" may count the `ja` default as kind 8, but a port reading side A would arm a
  ninth kind.

**C-V49. Address of the pool-full `+0x14` store.**
- Side A: `the-field-runtime-pass.md:156`: "`ActorSystem_BindBattleUnitsForEligibleRecords` (`00265B13`: `& 0xEF`)".
- Side B: `the-field-runtime-pass.md:177`: "when the battle-unit pool is full (`00265B11`, count ≥ 32)".
- Status: **no favoured side.** They may be a branch and a store, but both are given as the clearing site.

#### Contexts and the definition flag pair

**C-V50. Floor of the movement context's mean radius `+0xFC`.**
- Side A: `Actor-Contexts/the-movement-and-secondary-context-censuses.md:169`: "the turn/blend scalar `max(0.05, (x·scaleX + y·scaleZ)·0.5)` → `+0xFC`".
- Side B: `Actor-Contexts/the-movement-and-secondary-context-censuses.md:177`: "*Falsified in part 2026-09-18 (FABLE)* … whose floor is `0.01` (`008F30E4`, `0026B357`), not
  0.05".
- Status: **favoured: side B** (dated falsification). Side A is unstruck.

**C-V51. How many secondary-context elements there are.**
- Side A: `Actor-Contexts/the-movement-and-secondary-context-censuses.md:310`: "SecondaryContext's first 192 bytes are a **4 × 0x30 element array**".
- Side B: `Actor-Contexts/the-movement-and-secondary-context-censuses.md:342-343`: "Whether elements 1-5 carry the same vector is unproven". That implies six elements.
  `Actor-Contexts/the-movement-and-secondary-context-censuses.md:380` maps "`+0x90` for `k = 4`".
- Status: **no favoured side.**

**C-V52. Width of the `.text` scan and the tested-bit space (definition flag pair).**
- Side A:
  - `the-definition-record-flag-pair.md:18` and `:39`: "**8,001,280 bytes**";
  - `the-definition-record-flag-pair.md:231`: "**Twenty-two bits of the 64 available are never tested**".
- Side B:
  - `the-definition-record-flag-pair.md:278-281`: "virtualSize **7,996,981** … rawSize **7,997,440** … the sheet's figure 8,001,280 …
    difference from rawSize **3,840**";
  - the page's two status words share one 32-bit vocabulary with ten positions tested, so 22 is out of 32.
- Status: **no favoured side.** The audit left it "for the author to correct" (`the-definition-record-flag-pair.md:285-286`).

### 3.2 Value-changing counts and census figures

These are counts that disagree. None changes a port's arithmetic, but each changes what a checker or a re-derivation
would expect. All are page-text only, and the `.tsv` figures are this session's measurement.

| # | side A | side B | favoured |
|---|---|---|---|
| C-N1 | `Actor-Storage-Record/the-actor-storage-record-field-map.md:31`: "81 of them, from 272 functions"; `README.md:39-41`: "81 touched offsets from 272 functions … the 31 untouched bytes" | `Actor-Storage-Record/the-actor-storage-record-field-map.md:53-55`: "1042 … 275 … 86 — 40 with a store row, 46 without"; `Actor-Storage-Record/the-actor-storage-record-field-map.md:183`: "11 ranges totalling 37 bytes"; the `.tsv`: 1,130 rows, 271 functions, 111 displacements | none |
| C-N2 | `Actor-Storage-Record/the-actor-storage-record-field-map.md:203`: "**41 touched offsets have no store row**"; `Actor-Storage-Record/the-actor-storage-record-field-map.md:55`: "46 without" | `Actor-Storage-Record/the-actor-storage-record-field-map.md:204`: "*Re-measured 2026-09-27 …* the table now flags 34" | side B (dated) |
| C-N3 | `Actor-Storage-Record/the-actor-storage-record-field-map.md:56`, `:146`: `+0xB8` "2 / 67"; `Actor-Storage-Record/the-actor-storage-record-field-map.md:96`: `+0x03` "0 / 80" | `Actor-Storage-Record/the-actor-storage-record-field-map.md:192`: "`+0xB8` (`contextPtr`) by 66"; `Actor-Storage-Record/the-actor-storage-record-field-map.md:199`: "`+0x03` … has 78 readers" | none |
| C-N4 | `Battle-Unit/the-battle-unit-field-map.md:37-38`: "163 of them, from 328 functions … the 3206 bytes on 41 ranges"; `README.md:29-31`: "144 offsets across 310 functions … the 45 ranges" | `Battle-Unit/the-battle-unit-field-map.md:59-61`: 2203 rows, 342 functions, 168 offsets; `Battle-Unit/the-battle-unit-field-map.md:255`: "35 ranges totalling 3174 bytes … (re-counted 2026-09-11"; `Battle-Unit/the-battle-unit-field-map.md:643`: "the committed 2,207 in 344"; the `.tsv`: 2,205 rows, 345 functions | side B for the byte total (dated recount); none for the rest |
| C-N5 | `Battle-Unit/the-battle-unit-field-map.md:275`: "**`+0x00` has 38 writers and 81 readers**"; `Battle-Unit/the-battle-unit-field-map.md:277`: "`+0x698` is read by 151 functions and written by one" | `Battle-Unit/the-battle-unit-field-map.md:84` "56 / 99"; `Battle-Unit/the-battle-unit-field-map.md:173` "2 / 175" with writers `00236A60` and `0023A570` | none (`Battle-Unit/the-battle-unit-field-map.md:705-706` says every `N / N` cell was re-counted, so the §2.4 prose is older) |
| C-N6 | `Battle-Unit/the-battle-unit-field-map.md:597`: "§2.5 lists 33 bits … plus five register-mask bits"; `Battle-Unit/the-battle-unit-field-map.md:427`: "**the twelve authored tunables**" | the table holds 36 immediate rows and 7 register-mask rows (`Battle-Unit/the-battle-unit-field-map.md:315-362`); `Battle-Unit/the-battle-unit-field-map.md:427` lists ten offsets | none |
| C-N7 | `Battle-Unit/the-battle-unit-field-map.md:684-686`: the `.tsv` "holds two rows for it (displacements `0x0` and `0x698`)" | `Battle-Unit/the-battle-unit-field-map.md:729`: "carries thirty `0023A570` rows"; the `.tsv` has 32 | side B (`Battle-Unit/the-battle-unit-field-map.md:698-706`, FZ-16 answered) |
| C-N8 | `Actor-Storage-Record/the-record-behind-every-actor.md:28`, `:121`: "41 fields" | `Actor-Storage-Record/the-record-behind-every-actor.md:2871-2873`: "**39 distinct offsets** and **40 `(offset, width)` pairs** … Neither count is 41." | none |
| C-N9 | `Actor-Storage-Record/the-record-behind-every-actor.md:1512`: "all 70 offsets"; `Actor-Storage-Record/the-record-behind-every-actor.md:1540-1542`: the eight beyond `0x118` "are recorded in the TSV" | `actor-record-offsets-observed.tsv`: 56 rows, highest `0x118` | none |
| C-N10 | `Actor-Manager-Record/the-actor-manager-record-field-map.md:47-48`: "written by the bind at `0026C911` and by fifteen other functions" | `Actor-Manager-Record/the-actor-manager-record-field-map.md:340`: "33 stores in 17 functions" | none |
| C-N11 | `Actor-Manager-Record/the-actor-manager-record-field-map.md:409`: "holds **194** rows today"; `Actor-Manager-Record/the-actor-manager-record-field-map.md:55`: array route "51 / 31 / 17" | `actor-manager-record-accesses.tsv`: 204 rows; `actor-manager-record-rip-accesses.tsv`: 113 rows, 33 functions, 10 displacements | none |
| C-N12 | `Actor-Contexts/the-movement-and-secondary-context-censuses.md:19-20`: "1,028 rows, 122 distinct displacements; chain-only rows carry route `chain:0xB8`"; `Actor-Contexts/the-movement-and-secondary-context-censuses.md:38` and `README.md:52`: "313 accesses at 58 offsets … 302 at 40" | `movement-context-accesses.tsv`: 708 rows, 124 displacements, no `chain:0xB8`; `secondary-context-accesses.tsv`: 309 rows, 43 displacements | none |
| C-N13 | `Actor-Contexts/the-movement-and-secondary-context-censuses.md:238`: `+0x138` "2 / 20" | `Actor-Contexts/the-movement-and-secondary-context-censuses.md:200`: "**That also makes the `2 / 20` count short by one.**" | side B |
| C-N14 | `CONTRACT-manager-slot-entry-tables.md:343`: "`getcamerasubframe()` in 37 calls" | `CONTRACT-manager-slot-entry-tables.md:452`: "`getcamerasubframe` results in 38 of 39" | none |
| C-N15 | `CONTRACT-field-runtime-pass.md:448`: "58 operand-verified `02098E10` base-takers" | `CONTRACT-field-runtime-pass.md:514`: "Of the 59 functions that take the block base `02098E10`" | none |
| C-N16 | `CONTRACT-field-runtime-pass.md:276-277`: "One call on slot 0 produces **fourteen** trace entries" | `CONTRACT-field-runtime-pass.md:799-800`: "The four trace entries per slot-0 request the contract cites" | none |
| C-N17 | `Battle-Record-Kind/actor-type-id-partition-and-the-13-value-band.md:91-92`: "**28 sites using `0x1B`**"; `Battle-Record-Kind/actor-type-id-partition-and-the-13-value-band.md:100-101`: seven subsystems | `Battle-Record-Kind/actor-type-id-partition-and-the-13-value-band.md:99-100`: "27 sites … in 24 functions" (re-censused 2026-09-13); `Battle-Record-Kind/battle-record-kind-byte.md:871-872`: "26" / "22"; `Battle-Record-Kind/battle-record-kind-byte.md:890`: "**Eight subsystems**" | 27 over 28 within `Battle-Record-Kind/actor-type-id-partition-and-the-13-value-band.md` (dated re-census); none between the pages |
| C-N18 | `Battle-Record-Kind/battle-record-kind-byte.md:29-30`: "**104 sites across 82 functions**" | `Battle-Record-Kind/battle-record-kind-byte.md:109-110`: the owner spread "27 unowned, Movement 15, … Party 1" sums to 104 | none |
| C-N19 | `battleunit-slot-pool-and-actor-class.md:672`: "**67** proved bodies" | `battleunit-slot-pool-and-actor-class.md:772`: "Across the 63 proved member bodies" | none |
| C-N20 | `Actor-Contexts/the-movement-and-secondary-context-censuses.md:375`: "finds 45 functions" | the list in the same paragraph names 44, and it later says "the 44 readers" | none |

### 3.3 Stale "not read / open" claims, and corrected claims still repeated unstruck

Each row quotes the stale side first and then the text that answers or corrects it.

| # | stale side | answer / correction |
|---|---|---|
| C-S1 | `Actor-Storage-Record/the-record-behind-every-actor.md:140-141`: "**`0x11C` is a lower bound, not the size.** … No allocation site was read"; `Actor-Storage-Record/the-record-behind-every-actor.md:1351`: "The record's true size \| **not established**"; `Actor-Storage-Record/the-record-behind-every-actor.md:2881` (2026-09-12): "the record's true size stays `UNKNOWN` (`0x11C` remains a lower bound)"; `CONTRACT-actor-storage-record-initialisation.md:89-90`: "**no allocation site was read**" | `Actor-Storage-Record/the-record-behind-every-actor.md:1425`: "**Records are 720 to 1,760 bytes, by kind**"; `CONTRACT-actor-storage-record-initialisation.md:161-163`: "**CLOSED 2026-09-23**" |
| C-S2 | `Actor-Storage-Record/the-record-behind-every-actor.md:1350`: "Same type as the movement actor \| … \| 3 \| **PROBABLE**"; `CONTRACT-actor-storage-record-initialisation.md:209-210`: "**This contract does not claim the two types are one**" | `Actor-Storage-Record/the-record-behind-every-actor.md:1452-1454` (EH-1 to PROVEN); `CONTRACT-actor-storage-record-initialisation.md:152`: "**CLOSED 2026-09-23 (SWE2-CONTRACT) — the page resolved it PROVEN**" |
| C-S3 | `Actor-Storage-Record/the-record-behind-every-actor.md:165`: "`00266AD0`, `00266BD0`, `00268EA0`, `003DB580` … — **not read**" | read at `Actor-Storage-Record/the-record-behind-every-actor.md:306-311`, `:1599-1613`, `:1617-1628`, `:1313-1316` |
| C-S4 | `Actor-Storage-Record/the-record-behind-every-actor.md:179-180`: "**`+0xB8` is not initialised here.** … a record fresh from this routine still points at the previous occupant's context" | `Actor-Storage-Record/the-record-behind-every-actor.md:1967`: "`00266B54` plants the pointer"; `Actor-Storage-Record/the-record-behind-every-actor.md:50-54` (memset, no prior occupant) |
| C-S5 | `Actor-Storage-Record/the-record-behind-every-actor.md:2202`: "**no destructor identified.** … **NOT answered**"; `Actor-Storage-Record/the-record-behind-every-actor.md:2386-2391`: "**a controlled absence claim**" | `Actor-Storage-Record/the-record-behind-every-actor.md:2271`: "RETRACTED 2026-09-21 (OPUS): the pool IS released" |
| C-S6 | `Actor-Storage-Record/the-record-behind-every-actor.md:418-419`: "`+0x14` bit 5 (`FRP-1` owns it as not established)"; `Actor-Storage-Record/the-actor-storage-record-field-map.md:111`: "bit 5 set at init (meaning open)"; `CONTRACT-field-runtime-pass.md:73-75`: "bit 5 is read by seven sites and unexplained" | `Actor-Storage-Record/the-record-behind-every-actor.md:362` and `CONTRACT-field-runtime-pass.md:428`: "**the script *enable* flag** — `FRP-1`, answered 2026-09-18" |
| C-S7 | `Actor-Storage-Record/the-record-behind-every-actor.md:1251-1252`: "the `+0x1C` indices to `SWE2-DATA` as an argument census" | `Actor-Storage-Record/the-record-behind-every-actor.md:1189`: "*Corrected 2026-09-27 …* the engine does set all eight" |
| C-S8 | `Actor-Storage-Record/the-record-behind-every-actor.md:1020-1021`: "read by a shared predicate `talktreasure`, `reqdisable` and **`fieldsign`** all consult" | `Actor-Storage-Record/the-record-behind-every-actor.md:643-644`: "~~a shared predicate that~~ **the request-bit clearer** … *Corrected 2026-09-16*" |
| C-S9 | `Actor-Storage-Record/the-record-behind-every-actor.md:2168-2169`: "now 36 bytes at `+0x64`–`+0x88`" | `Actor-Storage-Record/the-record-behind-every-actor.md:192-194`: "**CLOSED 2026-09-12** … four `int32` at `+0x64`–`+0x70` and four `float` at `+0x74`–`+0x80`" |
| C-S10 | `Actor-Storage-Record/the-actor-storage-record-field-map.md:80`: the constructor's stores "are not in the TSV"; `Actor-Storage-Record/the-actor-storage-record-field-map.md:236-237`: "`0026670D mov byte ptr [rbx + 2], al` … is **not in `actor-storage-record-accesses.tsv`**" | the `.tsv` on disk has 96 `ctor` rows for `00266530`, `0026670D` among them (measured) |
| C-S11 | `CONTRACT-actor-record-pool-and-region-map.md:665-666`: "**Nothing here has been executed** (§13)"; `CONTRACT-actor-record-pool-and-region-map.md:423`: "**Nothing here has been observed in a running game.**" | `CONTRACT-actor-record-pool-and-region-map.md:372-374`: "It was executed 2026-09-12 … and it was then **observed live**" |
| C-S12 | `CONTRACT-actor-record-pool-and-region-map.md:9`: `entries: ["00267A20", …]`; `CONTRACT-actor-record-pool-and-region-map.md:424`: "**The pool allocation `00267A20`**" | `CONTRACT-actor-record-pool-and-region-map.md:102`: "**`00267A20`, which this section used to name here, is an interior address of that body, not a function**" |
| C-S13 | `CONTRACT-actor-record-pool-and-region-map.md:525-528`: "the five copies are **dead stores** that the register file overwrites" | `CONTRACT-actor-record-pool-and-region-map.md:552-556`: "**CORRECTED 2026-09-20 (SWE2-CONTRACT): the overlap described above never happens.**" |
| C-S14 | `the-definition-record-flag-pair.md:138-140`: "this sheet does not choose between them" (authored record or per-unit copy); `the-definition-record-flag-pair.md:28`/`:30`: "enemy definition record" | `the-definition-record-flag-pair.md:332`: "**CB-7 answered 2026-09-12 (FABLE): a per-unit copy.**" |
| C-S15 | `the-definition-record-flag-pair.md:340-342`: "It does not say bit 5 is Stop or bit 31 is KO." | `the-definition-record-flag-pair.md:199-200` names bit 16 "**Disease**" and bit 28 "Bubble" |
| C-S16 | `Battle-Unit/the-battle-unit-field-map.md:508-509`: `+0xB90` among the "**Six** rows … write or a reset and nothing else" | `Battle-Unit/the-battle-unit-field-map.md:488`: "*(Corrected 2026-09-30 …)* **operand-store kind 10, the unit's what-was-used-on-me mask.**" |
| C-S17 | `Battle-Unit/the-battle-unit-field-map.md:525-526`: "for the twelve tunables, the FCP property catalogue (FW-1)"; `Battle-Unit/the-battle-unit-field-map.md:635-636`: "the twelve tunables' properties (**FW-1**)" | `Battle-Unit/the-battle-unit-field-map.md:427`: FW-1 "answered by consumer" (2026-09-26) |
| C-S18 | `Battle-Unit/the-battle-unit-field-map.md:646`: "What the untouched ranges and the unnamed fields are \| **not established** \| — \| UNKNOWN"; `Battle-Unit/the-battle-unit-field-map.md:603-604`: "`+0x200`–`+0x297` the navigation path state" | `Battle-Unit/the-battle-unit-field-map.md:616`: "**ANSWERED 2026-09-26 …: `+0x298`–`+0x68F` is entries 1–127 of the navigation path record's waypoint table.**"; `Battle-Unit/the-battle-unit-field-map.md:623` |
| C-S19 | `battleunit-slot-pool-and-actor-class.md:658-659`: "the span stays `DISCOVERED` / `UNKNOWN`"; `battleunit-slot-pool-and-actor-class.md:744-745`: "`+0x298` is written by the acquire-side clear and read by nothing in the shipped image that static analysis can reach." | `Battle-Unit/the-battle-unit-field-map.md:616` (2026-09-26, later than `battleunit-slot-pool-and-actor-class.md`'s 2026-09-18/19 sections) |
| C-S20 | `Battle-Unit/the-battle-unit-field-map.md:1196`: "`Navigation_SelectNextWaypointXZ` (1,223 B)" | `Battle-Unit/the-battle-unit-field-map.md:1210`: "*Correction and pointer (2026-09-19, FABLE).* `00383670` is **204 B**, not 1,223" |
| C-S21 | `battleunit-slot-pool-and-actor-class.md:171`: "\| `00234200` \| `ActorSystem_ReleaseBattleUnitSlotForActor` \| not read \|"; `battleunit-slot-pool-and-actor-class.md:788-789`: "There is a second full-slot clear on the other side of the lifetime, and no page records it." | `battleunit-slot-pool-and-actor-class.md:791-807` (the body read); `Battle-Unit/the-battle-unit-field-map.md:1150-1151`: "frees the slot through `00861EC0` with stride `0xF50` (`002342CE`)" |
| C-S22 | `battleunit-slot-pool-and-actor-class.md:272`: "what classes 0 and 1 hold is the residue (§2)" | `battleunit-slot-pool-and-actor-class.md:87-88`: "*Resolved 2026-09-12 (BV-4):* … class 0 is the script-only controller …" |
| C-S23 | `Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md:110`: "an unread resolver (`FB-1`)" | `Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md:488`: FB-1 answered |
| C-S24 | `Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md:200`: `003243F0` "Its meaning beyond the call list is not read." | `Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md:541`: "`003243F0` (95 B) is the **unit retire helper**" |
| C-S25 | `Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md:226-227`: "Which reader consumes unit `+0x18` … is `FB-6`." | `Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md:537-538`: "**FB-6 closed 2026-09-12 (FABLE):** unit `+0x18` was answered 2026-09-10" |
| C-S26 | `Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md:254`: "the reader of the spawn record's `+0x12` copy is still open (`FB-3`)"; `Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md:437-438`: "What reads that copy is `FB-3`." | `Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md:494-495`: "**FB-3 ANSWERED 2026-09-12 (FABLE)**" (its own answer is disputed, C-V30) |
| C-S27 | `Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md:572`: "What the remaining unread callees and unnamed row fields are \| **not established** \| — \| UNKNOWN" | `Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md:503-506`: FB-4 read 2026-09-11; "**ANSWERED 2026-09-12 (FABLE)**" |
| C-S28 | `Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md:109`: "a per-area (the byte at `0208D454`) … counter" | `Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md:244`: "**The spawn counter, corrected.** The byte at `0208D454` is not an area id: it is a **bank selector**" |
| C-S29 | `Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md:519-521`: "the type, kind, facing and perception the installer uses come from the *page*, not the row" | `Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md:111`: "~~from the **page** (`r15 = [rsp+0x90]`)~~ **corrected 2026-09-12 (FABLE): from the `.ard` slot-0 class row**" |
| C-S30 | `Unit-Definition/CONTRACT-battle-unit-construction.md:61`: "the delegate's effects remain static."; `Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md:80-81`: "the delegate's effects are the static reading above." | `Unit-Definition/CONTRACT-battle-unit-construction.md:230-231`: "EXP-151 … executed the rekey inner `003220E0` through `00322050` end-to-end" |
| C-S31 | `Unit-Display-Record/the-record-00329220-builds.md:107`: "\| `0031FEC0`, `0031FF70` \| 167 / 199 B \| two more callers, unread \|" | `Unit-Display-Record/the-record-00329220-builds.md:191`: "*Half answered 2026-09-12 (FABLE):* both are **actor-to-slot wrappers**" |
| C-S32 | `Unit-Display-Record/the-record-00329220-builds.md:226`: "What the predicates and the three party-row words are \| **not established** \| — \| UNKNOWN" | `Unit-Display-Record/the-record-00329220-builds.md:145` (FJ-1 answered), `Unit-Display-Record/the-record-00329220-builds.md:157` ("**ANSWERED 2026-09-26**") |
| C-S33 | `Unit-Display-Record/the-record-00329220-builds.md:94`: "+0x64 u16 page+0x52 (kind 1)" (also `Unit-Display-Record/the-record-00329220-builds.md:80`, `:132`) | `Unit-Display-Record/the-record-00329220-builds.md:65`: "`+0xE68` is the class row, not a stats page" (corrected 2026-09-13); `Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md:112` |
| C-S34 | `Battle-Record-Kind/actor-type-id-partition-and-the-13-value-band.md:241`: "**Whether kind values other than 0 and 1 exist** — still the parent document's open item." | `Battle-Record-Kind/battle-record-kind-byte.md:314-315`: "**AL-4 ANSWERED 2026-09-12 (FABLE): `{0, 1}`, from the writer.**" |
| C-S35 | `Battle-Record-Kind/actor-type-id-partition-and-the-13-value-band.md:394` (2026-09-13): "What the thirteen types *are*, and what a presentation code selects, are untouched." | `Battle-Record-Kind/actor-type-id-partition-and-the-13-value-band.md:260` (§12, 2026-09-11): "**the thirteen Espers**: Belias, …" |
| C-S36 | `Battle-Record-Kind/battle-record-kind-byte.md:324-327`: "the byte is **authored definition data**, set once." (unstruck) | `Battle-Record-Kind/battle-record-kind-byte.md:589`: "### CORRECTED: this is not a shared authored definition"; `Battle-Record-Kind/battle-record-kind-byte.md:602-603`: "only the word "authored" was too strong" |
| C-S37 | `Battle-Record-Kind/battle-record-kind-byte.md:311`: AL-3 "Open: joining the other values, including 6 …" | `Battle-Record-Kind/battle-record-kind-byte.md:362`: "**`GR-2`** … *(Answered 2026-09-30, FABLE …)*" |
| C-S38 | `Battle-Record-Kind/battle-record-kind-byte.md:338`: "What most individual fields *mean* is still open." | `Battle-Record-Kind/battle-record-kind-byte.md:343-345`: "All 72 observed offsets have a row, and 69 have a name or meaning … *(`FE-1` was ANSWERED 2026-09-26.)*" |
| C-S39 | `Battle-Record-Kind/battle-record-kind-byte.md:820-821`: "the consumers are named, the individual bits are not." | `Battle-Record-Kind/battle-record-kind-byte.md:831`: "**That condition was met on the spawn side (2026-09-12, FABLE, AL-10).**" |
| C-S40 | `Battle-Record-Kind/battle-record-kind-byte.md:892-893`: "it strengthens **AL-2** and **N-4** without answering either" | `Battle-Record-Kind/battle-record-kind-byte.md:900-901`: "*Corrected 2026-09-30 (FABLE): `AL-2` and `N-4` were both answered on 2026-09-11.*" |
| C-S41 | `Actor-Names/the-npc-name-dictionary.md:89-90`: "a guard whose index arithmetic on a negative id is the page's open item." | `Actor-Names/the-npc-name-dictionary.md:151-152`: "**FN-2** … **ANSWERED 2026-09-14 (FABLE)**" |
| C-S42 | `Actor-Names/the-npc-name-dictionary.md:219`: "\| Kind 9 = the language `bin` block \| index match and layout match only \| 2 \| PLAUSIBLE \|" | `Actor-Names/the-npc-name-dictionary.md:205`: "**Answered 2026-09-14 (FABLE), from the loader:** the inference holds" |
| C-S43 | `Actor-Manager-Record/the-actor-manager-record-field-map.md:195`: "The names of the members remain open"; `Actor-Manager-Record/the-actor-manager-record-field-map.md:97`: `+0x018` "*not named by any page*" | `CONTRACT-manager-slot-entry-tables.md:117-124` names `definitionValue`, `lookupIndex`, `recordIndex`, `clock`, `rate`, `clockRunning`; `Actor-Manager-Record/the-actor-manager-record-field-map.md:316`: "+0xD8, +0x18 and the +0x11x-+0x1Cx band were named by the store before today" |
| C-S44 | `Actor-Manager-Record/the-actor-manager-record-field-map.md:311`: "**FH-1.** … *(closed — the register row is WITHDRAWN.)*"; `Actor-Manager-Record/the-actor-manager-record-field-map.md:337`: "**FH-3.** … *(closed — the register row is WITHDRAWN.)*" | `Actor-Manager-Record/the-actor-manager-record-field-map.md:316`: "Still unnamed: …"; `Actor-Manager-Record/the-actor-manager-record-field-map.md:339`: "the register row is PARTIAL (FH-3)" |
| C-S45 | `CONTRACT-manager-slot-entry-tables.md:281`: "**45 mutants: 34 KILLED · 4 EQUIVALENT · 4 SURVIVED · 3 NO_BUILD**"; `CONTRACT-manager-slot-entry-tables.md:584`: "45 mutants, 34 killed, 4 proven byte-identical" | `CONTRACT-manager-slot-entry-tables.md:386`: "**49 generated points: 38 KILLED · 4 SURVIVED · 4 EQUIVALENT · 3 NO_BUILD …**"; `CONTRACT-manager-slot-entry-tables.md:389`: "**The 45-mutant line above is superseded.**" |
| C-S46 | `CONTRACT-manager-slot-entry-tables.md:466-468`: "which, and the runtime range of `getcamerasubframe`, is the residue" | `CONTRACT-manager-slot-entry-tables.md:454-456`: "the reset vs. stray-write question below is answered"; `CONTRACT-manager-slot-entry-tables.md:343`: "a shared `mov eax, 1` / `ret` stub, so 1" |
| C-S47 | `Actor-Contexts/the-movement-and-secondary-context-censuses.md:366-367`: "The planter has a second branch that points them elsewhere" | `Actor-Contexts/the-movement-and-secondary-context-censuses.md:62-63`: "**CORRECTED 2026-09-11.** The first publication called the arm at `00266B36`–`00266B52` "another branch …". It does not" |
| C-S48 | `Actor-Contexts/the-movement-and-secondary-context-censuses.md:218`: "The write that assigns a real index is not in this census (`FS-2`)" | `Actor-Contexts/the-movement-and-secondary-context-censuses.md:380`: "***ANSWERED 2026-09-17 (FABLE): the writer that assigns a real index is the element binder `002E3110`***" |
| C-S49 | `Actor-Contexts/the-movement-and-secondary-context-censuses.md:241-243`: `+0x14C`/`+0x14D`/`+0x14E` rows "0 / 1" | `Actor-Contexts/the-movement-and-secondary-context-censuses.md:271`: "*(Corrected 2026-09-26 …: all three have a writer, and two are named.*" (the rows carry italic notes but keep the zero) |
| C-S50 | `Actor-Contexts/the-movement-and-secondary-context-censuses.md:161`: untouched list includes "+0xDC..+0xDC (1 B)" and "+0x10C..+0x21F (276 B)" | `Actor-Contexts/the-movement-and-secondary-context-censuses.md:375`: `00265FF0` "zeroes the index byte `+0xDC`"; UQ-91 answered 2026-09-17 (`Actor-Contexts/the-movement-and-secondary-context-censuses.md:4`) |
| C-S51 | `the-field-runtime-pass.md:143-146`: "**One actor is driven repeatedly inside one frame until it settles.** … **There is no iteration cap.**" (unstruck blockquote); `CONTRACT-field-runtime-pass.md:42-43`: "the actor is driven, asked whether it settled, and driven again." | `the-field-runtime-pass.md:152`: "**Corrected 2026-09-12 (FABLE): nothing ever sets the low nibble, so the inner loop is dead code.**"; `the-field-runtime-pass.md:161-162`: "**each actor is driven once per loop that names it.**" |
| C-S52 | `CONTRACT-field-runtime-pass.md:245-246`: "There is no live evidence and the pass itself is still unexecuted."; `CONTRACT-field-runtime-pass.md:717`: the same | `CONTRACT-field-runtime-pass.md:384-386`: "### 13a. The pass body, the wait resolver and the init core, executed — 2026-09-18 … **Fifty-two bodies from shipped bytes**" |
| C-S53 | `CONTRACT-field-runtime-pass.md:530-532`: "`022C6D20[m]` reads as a **sticky "this manager has been asked to dispose" mark**"; `CONTRACT-field-runtime-pass.md:624-626`: "The one consequence that is not closed" | `CONTRACT-field-runtime-pass.md:534`: "### CORRECTION 2026-09-21 (OPUS) …: The mark IS cleared, in two places"; `CONTRACT-field-runtime-pass.md:661`: "**DISSOLVED rather than answered, 2026-09-21**" |
| C-S54 | `the-field-runtime-pass.md:604-605`: "Six fields are declared; `0x000`–`0x007`, `0x012`–`0x047`, `0x050`–`0x057` and `0x068`–`0x287` are undeclared, which is 614 of 648 bytes." | `CONTRACT-field-runtime-pass.md:62-67` declares `+0x12`, `+0x13`, `+0x17`, `+0x20`, `+0x24`, `+0x38`, `+0x200`; `Actor-Manager-Record/the-actor-manager-record-field-map.md:88-146` maps 57 offsets |
| C-S55 | `the-field-runtime-pass.md:701-704`: "Whether a wider store reaches an actor record's `+0x14` is **not** settled by this pass either" | `the-field-runtime-pass.md:706`: "*Reconciled 2026-09-30 (FABLE):* both items this pass left open are now closed on the page." |
| C-S56 | `the-field-runtime-pass.md:78-80`: "the save meaning comes from … whoever writes `02CA99E8`, which this document has not read." | `the-field-runtime-pass.md:82`: "**Read 2026-09-11:** three writers, all in the save-write operation." (`the-field-runtime-pass.md:80` adds a pointer to it) |

### 3.4 Status banners against front matter

| # | one side | the other side | favoured |
|---|---|---|---|
| B-1 | `README.md` banners: `battleunit-slot-pool-and-actor-class.md` "**DOCUMENTED, tier 1.**" (`README.md:14`); `Battle-Unit/the-battle-unit-field-map.md` DOCUMENTED (`:28`); `Actor-Manager-Record/the-actor-manager-record-field-map.md` DOCUMENTED (`:34`); `Actor-Storage-Record/the-actor-storage-record-field-map.md` DOCUMENTED (`:39`); `Unit-Display-Record/the-record-00329220-builds.md` DOCUMENTED (`:44`); `Actor-Contexts/the-movement-and-secondary-context-censuses.md` "**PARTIAL, tier 1.**" (`:50`) | the pages' front matter: `status: AUDITED` (`battleunit-slot-pool-and-actor-class.md:4`, `Battle-Unit/the-battle-unit-field-map.md:4`, `Actor-Manager-Record/the-actor-manager-record-field-map.md:4`, `Actor-Storage-Record/the-actor-storage-record-field-map.md:4`, `Unit-Display-Record/the-record-00329220-builds.md:4`); `Actor-Contexts/the-movement-and-secondary-context-censuses.md:4` "AUDITED — … answered 2026-09-17" | none (README says status is at `../_index/COVERAGE.md`, `README.md:9`) |
| B-2 | `Battle-Record-Kind/battle-record-kind-byte.md:32`: "**PARTIAL — deliberately.**" (unstruck banner) | `Battle-Record-Kind/battle-record-kind-byte.md:4`: `status: DOCUMENTED …`; `Battle-Record-Kind/battle-record-kind-byte.md:38`: "GR-2 is answered (§7) and the page is DOCUMENTED (2026-10-01, OPUS)" | DOCUMENTED (dated) |
| B-3 | `Actor-Storage-Record/the-record-behind-every-actor.md:9` `confidence: PROVEN`; `Actor-Storage-Record/the-record-behind-every-actor.md:21-22` `reopened_count: 0` | `Actor-Storage-Record/the-record-behind-every-actor.md:1350-1352` PROBABLE/UNKNOWN evidence rows; `Actor-Storage-Record/the-record-behind-every-actor.md:2218` "**Not reconstruction-ready**"; `Actor-Storage-Record/the-record-behind-every-actor.md:2271` "RETRACTED 2026-09-21" | none |
| B-4 | `CONTRACT-field-runtime-pass.md:5-7` `level: L2`, `readiness: CONTRACT READY`, `confidence: PROVEN` | `CONTRACT-field-runtime-pass.md:879`: "No full-system L2 or formal acceptance is awarded here." | none |
| B-5 | `Unit-Definition/CONTRACT-battle-unit-construction.md:7` `confidence: PROVEN` | `Unit-Definition/CONTRACT-battle-unit-construction.md:14`: "T2 peer review and canonical acceptance remain pending." | none |
| B-6 | `Actor-Names/the-npc-name-dictionary.md:9` `confidence: PROVEN` | `Actor-Names/the-npc-name-dictionary.md:219` evidence row "PLAUSIBLE" (stale, C-S42) | none |
| B-7 | `CONTRACT-manager-slot-entry-tables.md:7` `confidence: PROVEN` | `CONTRACT-manager-slot-entry-tables.md:507`: "any runtime observation \| **none exists** \| none \| UNKNOWN" | none |
| B-8 | `Actor-Contexts/the-movement-and-secondary-context-censuses.md:4` status says both open items were answered 2026-09-17 | `Actor-Contexts/the-movement-and-secondary-context-censuses.md:8` `readiness: PARTIALLY UNDERSTOOD` | none |
| B-9 | `last_pass_kind: authored`: `Actor-Storage-Record/the-record-behind-every-actor.md:20`, `Actor-Storage-Record/the-actor-storage-record-field-map.md:22`, `Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md:23` | body sections titled "Falsification pass 1": `Actor-Storage-Record/the-record-behind-every-actor.md:2841`, `Actor-Storage-Record/the-actor-storage-record-field-map.md:312`, `Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md:600` | none |
| B-10 | `Battle-Record-Kind/battle-record-kind-byte.md:21` `last_pass: 2026-09-02` | `Battle-Record-Kind/battle-record-kind-byte.md:642`: "## 12a. Falsification pass 2026-09-17 (OPUS)" | none |
| B-11 | `last_reviewed` dates older than the pages' own dated edits: `Actor-Storage-Record/the-record-behind-every-actor.md:15` (2026-09-08), `Actor-Storage-Record/the-actor-storage-record-field-map.md:17` (09-10), `CONTRACT-actor-record-pool-and-region-map.md:17` (09-11), `the-definition-record-flag-pair.md:19` (09-06), `Battle-Unit/the-battle-unit-field-map.md:23` (09-12), `battleunit-slot-pool-and-actor-class.md:18` (09-02), `Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md:16` (09-22), `Unit-Display-Record/the-record-00329220-builds.md:15` (09-10), `Battle-Record-Kind/actor-type-id-partition-and-the-13-value-band.md:19` (09-03), `Actor-Manager-Record/the-actor-manager-record-field-map.md:17` (09-10), `CONTRACT-manager-slot-entry-tables.md:17` (09-11), `Actor-Contexts/the-movement-and-secondary-context-censuses.md:22` (09-12), `the-field-runtime-pass.md:19` (09-03), `CONTRACT-field-runtime-pass.md:17` (09-12) | dated edits reach 2026-09-30 to 2026-10-02 on these pages (for example `Actor-Storage-Record/the-record-behind-every-actor.md:109`, `Battle-Unit/the-battle-unit-field-map.md:488`, `Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md:349`, `the-field-runtime-pass.md:137`) | none |
| B-12 | section dates "2026-05-15": `the-field-runtime-pass.md:904`, `CONTRACT-field-runtime-pass.md:821` | the program and the pages' other dated sections run from 2026-09 | none (a date anomaly only) |
| B-13 | duplicate section numbers: `Battle-Record-Kind/actor-type-id-partition-and-the-13-value-band.md:227`/`:312` (two §9), `Battle-Record-Kind/battle-record-kind-byte.md:483`/`:861` (two §11), `Actor-Names/the-npc-name-dictionary.md:221`/`:227` (two §9), `battleunit-slot-pool-and-actor-class.md:339`/`:346` (two §9) | cross-references such as "§11" and "§9" are ambiguous on those pages | none |

---

## 4. Rating

**Overall: NOT YET.** The category holds the core layouts every other system rests on: the actor record, the
manager slot and the battle unit. The record's own layout still has structural gaps. Value conflicts sit at its root
(C-V1, C-V2, C-V5, C-V6), and the two embedded contexts have no declared layout on these pages. The parts are
uneven:

| part | rating | why |
|---|---|---|
| NPC name dictionary (`npcdic.bin`, `+0x102`, display lookup) | **READY** apart from S-17 | The file format, the relocation, the pair rule and the lookup are all stated (`Actor-Names/the-npc-name-dictionary.md:52-90`). The missing piece is the flag setter's address. The page's "dictionary" label is also applied to an unrelated UI global (C-V42), and a port must not follow it there. |
| BattleUnit pool, allocation, handle and release | **MOSTLY** | Size, count, first-free scan, silent failure, handle encoding and both full-slot clears are stated (`battleunit-slot-pool-and-actor-class.md:96-160`, `:354-376`, `:474-524`, `:790-807`). Open: the release bounds-check multiplier (C-V24), the channel table address (C-V23) and the back-pointer statement (C-V25). |
| Field runtime pass and wait resolver | **MOSTLY** | The pass's order, refusals, branches and wait-kind arms are stated and executed (`CONTRACT-field-runtime-pass.md:384-386`). Most of its value conflicts carry a dated correction (C-V43, C-V44, C-V45), but the contract's reproduction formula still carries the stale side. Open: the callees `002620E0`/`0025B600`/`00269860`, the fold region, the slot fields `+0x13`/`+0x17` (S-8), wait-kind 3–5 arming (S-7), and C-V46–C-V48. |
| Manager slot and camera entry tables | **MOSTLY** | The bind, the 57-offset field map, the banks and the eight entry operations are stated, and seven of the eight are executed (`CONTRACT-manager-slot-entry-tables.md:228`). Open: the slot size the contract uses (C-V13), the camera player and shake sampler effects (S-12), the unnamed slot fields (G-15), and the `+0x1D6`/`+0x1DE` order (C-V8). |
| Kind byte and type-id partition | **MOSTLY** | The kind domain `{0, 1}` and the table it selects are settled (`Battle-Record-Kind/battle-record-kind-byte.md:314-315`). So are the type-id spans and the reward rule (`Battle-Record-Kind/actor-type-id-partition-and-the-13-value-band.md:47-87`, `:218-224`). Open: the per-site band polarity (S-15), the valid id range (C-V39) and Reks's classification (C-V41). |
| StatusView (`00329220`) | **MOSTLY** | Every field of the `0xC0` record has a stated source (`Unit-Display-Record/the-record-00329220-builds.md:57-91`). Open: bits 16/17's meaning (G-22, S-18). Its bit-4 predicate depends on bit 43, which the definition page calls unread (C-V29). |
| Unit construction and the stats record | **NOT YET** | The installer is mapped site by site and executed against shipped data (`Unit-Definition/CONTRACT-battle-unit-construction.md:217-314`). But **value conflicts sit inside the install itself**: unit `+0x52` (C-V28), the old-id condition (C-V34), the leader-selector store width (C-V35), enemy growth (C-V36), the spawn counter at its cap (C-V31) and the tracked-HP table layout (C-V33). It also lacks the reset's full field list (S-9), the table strides (S-10) and the growth formula (S-11). |
| Actor record: pool, region map, initialiser | **NOT YET** | **Structural gaps.** The allocator is unidentified (S-1). The constructor's output is not stated field by field (S-2). The movement-context initialisers are unread (S-3). The definition payload format is not recovered (S-4). Four value conflicts sit at the root of the layout: the `+0x03` field names (C-V1), the sequence-7 record size (C-V2), whether the initialiser fills the override array (C-V5), and what the table's byte `+0x01` is (C-V6). |
| Movement and secondary contexts | **NOT YET** | The census locates offsets and "names nothing — the store owns the layouts" (`Actor-Contexts/the-movement-and-secondary-context-censuses.md:38-39`). Most fields a mover or renderer needs have no declared meaning on these pages (S-5, G-10), and the census files no longer match the counts the page states (C-N12). |

**To reach MOSTLY overall**, the database would need:
- a local check of C-V1, C-V2, C-V5 and C-V6 against the image (the record layout);
- the record-pool allocator (S-1), and the constructor's full store list with values (S-2), on a page in this
  folder rather than only in `_types/fields.tsv`;
- declared layouts for the movement and secondary contexts (S-5), and the bodies of `00265FF0` and `00268380` (S-3);
- a local check of the install conflicts C-V28, C-V31, C-V33, C-V34, C-V35 and C-V36, and the reset's field list
  (S-9);
- the stale side of each settled item struck in place. That covers the contract formula at `CONTRACT-field-runtime-pass.md:229-235`, the 56
  rows in §3.3, and the banners in §3.4. A re-implementer reading top to bottom meets the stale text first.
