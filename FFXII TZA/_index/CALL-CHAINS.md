# Call chain index

Every cross-subsystem transition, documented in both directions, with **owner transitions**
distinguished from **triggers**.

A trigger causes a thing to happen. An owner transition is where authority for the state
actually lives. Confusing the two is how ownership gets wrongly inherited - see
[`EVIDENCE-STANDARD.md`](EVIDENCE-STANDARD.md).

## Documented chains

| Chain | Owners crossed | Document |
|---|---|---|
| Field init -> Weather roll -> apply -> Movement -> LegacyPS2GS rebuild | ActorEntity -> WorldAreaField -> Movement -> Presentation | [`../03-World-Area-Field/Weather/call-chains/field-init-weather-to-legacyps2gs-rebuild.md`](../03-World-Area-Field/Weather/call-chains/field-init-weather-to-legacyps2gs-rebuild.md) |
| Runtime `setweatherslot` -> apply -> Presentation refresh | Script/VM -> WorldAreaField -> Presentation | same document, "The split that matters" |
| Committed action -> presentation-ready ring -> current unit -> capability policy | CombatAction -> InputGameplay/UI | [`../07-Combat-Action/Command-And-Action-Seam/native-command-seam.md`](../07-Combat-Action/Command-And-Action-Seam/native-command-seam.md) |
| Command intent -> issue -> commit -> action advance | CombatAction | same document |
| Pad input -> capability policy -> UI request router -> screen | Input -> UI | [`../16-UI/Request-Router/ui-request-router.md`](../16-UI/Request-Router/ui-request-router.md) |
| ScriptVM fullscreen menu -> selector translate -> request mailbox | Script/VM -> UI | same document |
| Equipment/licence change -> derived augment layer -> merged formula context | Items/Equipment -> Status -> CombatFormula | [`../10-Status-Periodic-Terminal/Status-And-Augment-Layers/two-layer-effect-model.md`](../10-Status-Periodic-Terminal/Status-And-Augment-Layers/two-layer-effect-model.md) |
| Weather Slot -> MWeather -> gameplay class -> element scaling | WorldAreaField -> CombatFormula | [`../08-Combat-Formula/Weather-Terrain-Element-Scaling/weather-terrain-element-scaling.md`](../08-Combat-Formula/Weather-Terrain-Element-Scaling/weather-terrain-element-scaling.md) |
| Weather Slot -> MWeather -> Presentation backend basis | WorldAreaField -> Presentation | [`../03-World-Area-Field/Weather/mweather-resource-format.md`](../03-World-Area-Field/Weather/mweather-resource-format.md) |
| ActionDefinition -> recipe -> calculator lists -> committed result | CombatFormula | [`../08-Combat-Formula/Recipe-System/ranged-weapon-recipes.md`](../08-Combat-Formula/Recipe-System/ranged-weapon-recipes.md) |

| Sound event → variant selection (slot 43) → trigger | Audio | [`../18-Audio/Sound-Selection/sound-variant-selection.md`](../18-Audio/Sound-Selection/sound-variant-selection.md) |
| Trigger → state gate → slot alloc → bind Sequence → parameter ops → dispatch | Audio | [`../18-Audio/Sound-Selection/sound-trigger.md`](../18-Audio/Sound-Selection/sound-trigger.md) |
| Field id → field record bit 15 → action eligibility | WorldAreaField → CombatAction | [`../03-World-Area-Field/Field-Record-Table/field-record-bit15-action-permission.md`](../03-World-Area-Field/Field-Record-Table/field-record-bit15-action-permission.md) |

| Section query → tag/name match → offset → base resolution → pointer | Resource | [`../02-Resource-And-Asset-Pipeline/resource-section-addressing.md`](../02-Resource-And-Asset-Pipeline/resource-section-addressing.md) |
| Script verb id → dispatch table → native handler | Script/VM → engine | [`../01-Script-VM-Native-Bridge/scriptvm-native-dispatch-table.md`](../01-Script-VM-Native-Bridge/scriptvm-native-dispatch-table.md) |

| Heading/speed intent → delta → position integration | Movement | [`../06-Movement-And-Navigation/heading-speed-to-position-delta.md`](../06-Movement-And-Navigation/heading-speed-to-position-delta.md) |

| Combat entry → BattleUnit slot allocation → actor bind → encoded handle | ActorEntity | [`../04-Actor-Entity/battleunit-slot-pool-and-actor-class.md`](../04-Actor-Entity/battleunit-slot-pool-and-actor-class.md) |
| Frame mode 2/3/5 → `World_UpdateSimulationTick` → field frame (slot 0 only) → actor drive loop → per-unit lifecycle callback at record `+0x38` → range retire / teardown | CoreRuntimeScheduling → WorldAreaField → ActorEntity → Spawn_Encounter_Lifecycle | [`../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md`](../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md) |
| Result record → `BattleFormula_ApplyTargetResult` → HP write (delta or absolute) → clamp → publishers → KO set / cleared → killer id → spawn death statistics → group ledger → death event | CombatFormula → Status → Spawn_Encounter_Lifecycle → Presentation | [`../08-Combat-Formula/Current-HP/the-hp-write-and-the-lethal-transition.md`](../08-Combat-Formula/Current-HP/the-hp-write-and-the-lethal-transition.md) |
| Status add / remove → mask write → per-status parameter and timer → transition result → the applier → cascade (definition `+0x0C`) → terminal table → defeat cleanup (party-state latches and UI requests) / rewards or recover | Status → CombatFormula → Party / UI → Rewards_Progression_Economy | [`../10-Status-Periodic-Terminal/Status-Write/the-status-write-and-its-side-effects.md`](../10-Status-Periodic-Terminal/Status-Write/the-status-write-and-its-side-effects.md) |
| Definition id → class byte → party table `02EBF130` / enemy table `02EBF120` → stats record (battle-state element / spawn record `+0x80`) → equipment, licences, level, gambits / steal bits, spawn counter | ActorEntity → CombatFormula → Items / CombatAI / Spawn_Encounter_Lifecycle | [`../04-Actor-Entity/Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md`](../04-Actor-Entity/Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md) |
| Definition row → level grower `0030C470` → level 0 → silent growth `0030C650` → experience `002F8F20` → status strip `0030F690` → HP / MP reconcile → starting MP → recompute `0030FED0` | ActorEntity → Rewards_Progression_Economy → Status → CombatFormula | [`../04-Actor-Entity/Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md`](../04-Actor-Entity/Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md) §2.6 |
| Any stats write → recompute `0030FED0` → desired set (party row / foe mask / equipment / licences) → diff against `+0x78` → layer write `0030E130` (modes 3 / 1) → stat rebuild `002FEF30` → foe `+0xE90` immunities (mode 5, into `+0x38`) → affinity handshake → clamps → charge count `0030E060` | CombatFormula → Status → Items | [`../08-Combat-Formula/the-auto-status-rebuild.md`](../08-Combat-Formula/the-auto-status-rebuild.md) |
| AI script `btlAtelSetAbility` `0x3000` / `btlAtelSetStatus` `0x3002` → `00510440` / `005103B0` → `002390B0` / `002394C0` → unit `+0xE80` / `+0xE90` (+ one-shot `BattleStats_AddStatusMode3` on a fresh spawn) → recompute `0030FED0` desired set / mode-5 immunities (`+0x38`) | Script_VM_Native_Bridge → ActorEntity → CombatFormula → Status | [`../08-Combat-Formula/the-auto-status-rebuild.md`](../08-Combat-Formula/the-auto-status-rebuild.md) |
| Script spawn verbs (`0x30xx` `VM_Spawn_*` / `VM_SpawnEntry_*`) → spawn record `+0x00`–`+0x18`, `+0x50`–`+0x7C` → `btlAtelSetUnitFinish` `0x304C` → `0023A410` → HP override / recompute; lethal transition → `+0x08`/`+0x0C`; applier → `+0x14`, `+0x78`–`+0x7B`; bank rotation / continuous-entry restore → whole record | Script_VM_Native_Bridge → Spawn_Encounter_Lifecycle → CombatFormula | [`../05-Spawn-Encounter-Lifecycle/Spawn-Record/the-spawn-keep-entry-field-map.md`](../05-Spawn-Encounter-Lifecycle/Spawn-Record/the-spawn-keep-entry-field-map.md) |
| Unit `+0x698` / party array → stats record → the rebuild `002FEF30` (effective bytes) / status write `0030E360` (words, arrays) / HP write `00300530` / MP writes `00300CE0`, `00300BC0` / recompute `0030FED0` / grower `0030C470` / level-up `0030C650` / direct state order `002FDDA0` / applier `003112F0` | CombatFormula → Status → Rewards_Progression_Economy → CombatAction | [`../08-Combat-Formula/Battle-Stats-Record/the-battle-stats-record-field-map.md`](../08-Combat-Formula/Battle-Stats-Record/the-battle-stats-record-field-map.md) |
| Unit pool `0208E688` / `ActorWork_GetBattleUnit` `0031B760` / `BattleStats_FindOwningBattleUnit` `0031B860` → battle unit → `+0x698` stats record (151 readers) / `+0x6A0` spawn record / `+0x00` flags (38 writers) / `+0xE98` group id | ActorEntity → CombatFormula → Spawn_Encounter_Lifecycle | [`../04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md`](../04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md) |
| Save buffer `+0x200` → payload: transition record `+0x1044` / flag banks `+0x1384` / snapshot mirror `+0x2000` / image-backed block `+0x8000` (`020927C0`) / group banks + SpawnKeep images `+0xE040`, `+0x2E250` / transition metadata `+0x4E460` / inventory descriptors `+0x53C54` | Save_Load_Settings → WorldAreaField → Spawn_Encounter_Lifecycle → Platform_Online_Achievements → Items | [`../19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/the-save-payload-field-map.md`](../19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/the-save-payload-field-map.md) |
| `ActorManager_BindLoadedDefinitionPayload` `0026C8C0` → slot `02098E10 + i × 0x288` → `02099D70` (bound slot) → `+0x28` index / `+0x10` live / `+0x201` opt-in → the world tick's slot loop | ActorEntity → Engine_Core_Runtime | [`../04-Actor-Entity/Actor-Manager-Record/the-actor-manager-record-field-map.md`](../04-Actor-Entity/Actor-Manager-Record/the-actor-manager-record-field-map.md) |
| `ActorManager_GetRecordByOrdinal` `00358940` / `ActorHandle_ResolveRegistryEntryByPackedId` `003588B0` → actor storage record → `+0xB8` `contextPtr` / `+0xC0` (the two most-followed links) / `+0x30` battle unit / `+0x60` resource free list | ActorEntity → Movement → Script_VM_Native_Bridge | [`../04-Actor-Entity/Actor-Storage-Record/the-actor-storage-record-field-map.md`](../04-Actor-Entity/Actor-Storage-Record/the-actor-storage-record-field-map.md) |
| UI / Input / Presentation → `0031FE70` / `00320040` → `BattleSlotMap_ResolveMappedBattleSlot` `0031B9F0` → party stats record → `00329220` (status view: HP / MP / layers / affinity / equipment / experience / action state / spawn counter) | UI → ActorEntity → CombatFormula | [`../04-Actor-Entity/Unit-Display-Record/the-record-00329220-builds.md`](../04-Actor-Entity/Unit-Display-Record/the-record-00329220-builds.md) |
| Calculator table `01EFA5C0[195]` → `00390390` (steal roll) → enemy row `+0x32`–`+0x36` / spawn record `+0x14` bits 0–2 → `RNG_MT19937_NextU32` × 3 / console arm 243 → scratch `02AEE04C`–`02AEE04E`, `02AEDFB8`, `02AEDFBC` / result `+0x2C` bit 23 → `BattleFormula_ResolveTargetResult` copies to result `+0x32`–`+0x34`, kind 6 → the applier's steal step (inventory, spawn record `+0x14` bit cleared) / `BattleFormula_DispatchPostResultEvents` → event `0x33` / `0x34` → `0046AB10` ring `02EBB560` → `005369C0` | Authored data → CombatFormula ← Spawn_Encounter_Lifecycle / Developer console → CombatAction / Presentation | [`../08-Combat-Formula/Steal/the-steal-roll.md`](../08-Combat-Formula/Steal/the-steal-roll.md) |
| Resolved result (`+0x1C == 1`) → `BattleFormula_ApplyResultMetadata` `00385BA0` → `BattleFormula_DispatchPostResultEvents` `00469EC0` (action id `02AEDFD4`, result `+0x140` / `+0x2C` / `+0x58` / kind) → event id → `0046AB10` (ring `02EBB560`, filter `00469570`, rate limit) → `005369C0` (row slots) → `00536410` / `0035B990`; rows = `[02EBF018]` = `battle_message.bin` | CombatAction → CombatFormula → Presentation ← Authored data | [`../07-Combat-Action/Post-Result-Events/the-post-result-events-and-the-battle-message-table.md`](../07-Combat-Action/Post-Result-Events/the-post-result-events-and-the-battle-message-table.md) |
| R2 press → `00253C70` toggle `020927E0` → `00252B60` (policy gates) → `00366870` acquire: counter `022CBE18` → threshold `022CBE08 = 30 × [01DFE0B4]` → engaged bit 2 of `022CBE1A` → `00252C80` → flag `01E0C2B8` (`0` = `FLEEING` on the HUD, EXP-025) | Input → Audio (state word) → CoreRuntime (mode flag) → Presentation | [`../15-Input/Modal-Toggles/r2-force-fight-toggle.md`](../15-Input/Modal-Toggles/r2-force-fight-toggle.md) §2g |
| Script `skipexec` (1337, `0034ECF0`) / engine `00360880` → `00360710` (request entry `022CB730`, pending → active bits `022CB9C0` / `022CB9D8`, eleven notifications) → `0026A5B0` sets bit k of manager `+0x201` → `World_UpdateSimulationTick` `00314020` runs sub-steps 1–15 for that slot → command 1306's poll (`0034DB30`) → `00360A50` clears; **manager 0 refused at `00360728`** | Script/VM → CoreRuntimeScheduling → ActorEntity (managers 1–4 only) | [`../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md`](../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md) §2.2a |
| Save image payload `+0x4E48C` → `02EBF190` block (0x7410) → `+0x5A48` selectors / `+0x5A58` slot map (`BattleGroup_RefreshFourActorDefinitions` `003266C0`) / `+0x5AA4` leader (`PartyFocus_*`) / `+0x5AD0` sequence (`00306760`) / `+0x5B04` mode flags (ladder `0030D9A0`) / `+0x5B00`–`+0x5B0E` echoes (`BattleFormula_ApplyResultMetadata` `00385BA0`) / `+0x5B10` gambit banks (`GambitConfig_*`) → the status view `00329220` bits 10 / 11, the slot-map wrappers, the transition record | Save_Load_Settings → Party / CoreRuntime / CombatFormula / CombatAI → UI | [`../11-Party/Battle-State-Block/the-battle-state-block-field-map.md`](../11-Party/Battle-State-Block/the-battle-state-block-field-map.md) |
| `BattleFormula_InitializeResultRecord` `003848E0` (sentinels) → `BattleFormula_ResolveTargetResult` `00385F60` + calculator slots via context `+0x10` (kind `+4`, flags `+0x18` / `+0x2C` / `+0x140`, numbers, masks `+0x54` / `+0x58`, timers `+0x42`, steal `+0x32`, deltas `+0x11E`, echoes `+0x138` / `+0x13C`) → `BattleFormula_ApplyTargetResult` `003112F0` (20 steps) → `BattleFormula_ApplyResultMetadata` `00385BA0` → `BattleFormula_DispatchPostResultEvents` `00469EC0` | CombatFormula → CombatAction → Party (block) / Presentation | [`../07-Combat-Action/Result-Record/the-result-record-field-map.md`](../07-Combat-Action/Result-Record/the-result-record-field-map.md) |
| `SaveLoad_ControllerLifecycleHandler` `00582860` → `SaveLoad_NormalizeLoadedRuntimeStateAndReseedRNG` `00584210`: mode byte `02AEE4D8` (verb `0x7067` → `00510970` → `00394630`) × header `+0x57` bit 0 → stash (header `+0x70`–`+0x90` ← `+0x10`–`+0x1B`, accumulator `00320D50`, transition record `+0x1044`; field `0x483`) or restore (bank A `00269A20`, metadata `002EF410`, pair selector `0023A390(0)`) → `RNG_MT19937_Seed` `00379CF0` | Save_Load_Settings → WorldAreaField / Party / RNG | [`../19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/version-stamps-and-what-loading-normalises.md`](../19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/version-stamps-and-what-loading-normalises.md) §4 |
| Stats `+0x68` (status layer) \| `+0x78` (augment layer) → `BattleFormula_BuildEvaluationContext` `003847C0` merge → context `+0x1A`–`+0x29` (128 bits) → calculator slots' bit tests (id 2 weather accuracy, id 16 weather scaling, id 17 the steal's three rolls, …) | Status_Periodic_Terminal / Items → CombatFormula | [`../08-Combat-Formula/Evaluation-Context/the-evaluation-context-field-map.md`](../08-Combat-Formula/Evaluation-Context/the-evaluation-context-field-map.md) §2.3 |
| `BattleUnit_CommitAction` `0030F760` → `BattleTargetBuffer_ResetPreservingFlag0` `00316CF0` / `BattleTargetBuffer_TryAppendActorWork` `00316CD0` on unit `+0x778` → `Battle_ProcessActionTargetEntry` `003191B0` finds the entry → `Battle_ProcessActionTarget` `00307300` writes `entry.outcome` from the resolved result (`003075BF`–`003075F9`) → readers: `0030071A` (bit 8 → the HP event variant), `00308790` / `0030C045` (entry 0 bit 10 → combo continuation), `00317783` (the code byte → reaction presentation) | CombatAction | [`../04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md`](../04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md) §2.4 |
| unit `+0x710` (the committed focus handle) → `BattleUnit_ResolveByFocusHandle` `0031B7E0` (`02089340` bit 4) → `ActorHandle_ResolveRegistryEntryByPackedId` `003588B0` (selector bits 16–19 < 5 → manager `00263FF0` = `02098E10 + sel × 0x288`; vector / storage / bounds / enable / count / entry / `+0x16` == bits 20–30) → `00263E30` returns actor `+0x30`, the BattleUnit | ActorEntity / CombatAction | [`../04-Actor-Entity/battleunit-slot-pool-and-actor-class.md`](../04-Actor-Entity/battleunit-slot-pool-and-actor-class.md) §11 |
| `BattleFormula_ResetScratchState` `003849B0` → the calculator slots write the scratch words (`02AEDFB8`–`02AEE05F`) → `BattleFormula_RollAvoidGuardParryOutcome` `003896B0` (bands vs stats `+0x33` / `+0x32` / `+0x31`, then the hit chance `02AEDFE0`) → the preview memoises flag word B bits 1–3 in the source's 64-byte record (`00385AC3`–`00385AF2`) → the resolver replays them (`003860DF`–`00386108`) and copies the number words out (`0038641D`–`00386813`) → `Battle_ProcessActionTarget` → entry outcome bits 8 / 9 / 10 | CombatFormula → CombatAction | [`../08-Combat-Formula/Scratch-Block/the-formula-scratch-block.md`](../08-Combat-Formula/Scratch-Block/the-formula-scratch-block.md) §2.3–2.5 |
| `00322050(unit)` (a definition change on the selected unit) → `003220E0`: old handle, `002659D0` advances actor `+0x16`, new handle → if the leader's unit (`00327150`) held the old handle: `+0x5AA4` = the re-keyed unit's stats `+4` → `PartyFocus_SelectAndRequestDefaultActor` `00326500` (mode → selector → unit with stats / four slot-map entries / actor slot 0) → `PartyFocus_RequestPackedActorHandle` `003594B0` | ActorEntity → Party | [`../11-Party/Battle-State-Block/the-battle-state-block-field-map.md`](../11-Party/Battle-State-Block/the-battle-state-block-field-map.md) §2.7 |
| `PartyFocus_ProcessActorControlPresentationState` `00358F90` → `003A1920` (position vs previous position of the focus actor's movement context) → `00317230` → block `+0x5AC8` / `+0x5ACC` (walked distance) → recipe 60 slot 146 `0038EBE0` (× 10 / 3 / 2 / 1 of the distance since last use) → `02AEE004`; recipe 56 slots 49 / 144 (`00389C60` → result `+0x138` → block `+0x5B0E` → `2 ^ count`); recipes 16 / 17 slots 121 / 122 (`+0x5B0C` bank) | Party → CombatFormula | [`../08-Combat-Formula/Recipe-System/the-count-clock-and-bank-recipes.md`](../08-Combat-Formula/Recipe-System/the-count-clock-and-bank-recipes.md) |
| Spawn candidate → distance validation → placement / retirement | Spawn | [`../05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md`](../05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md) |

| Leader status → control suppression (same predicate as action + reward) | Party ← WorldAreaField | [`../11-Party/party-roster-and-control-suppression.md`](../11-Party/party-roster-and-control-suppression.md) |

## A rule that spans subsystems

One predicate, found independently in three places across fifteen blocks:

```
nonFunctional(unit) =  ((unit.statusLayer0 | unit.statusLayer1) & 0x80000003) != 0
                    && FieldData_GetActiveFieldRecordBit15() == 0
```

| Subsystem | Consequence |
|---|---|
| Combat action eligibility | cannot act |
| Rewards | earns **zero** EXP and LP |
| Party control | player **loses control** |

The field-record override is therefore not a combat detail — it is a general per-area waiver
of the functional rule. Documented in
[field-record bit 15](../03-World-Area-Field/Field-Record-Table/field-record-bit15-action-permission.md),
[EXP/LP award](../13-Rewards-Progression-Economy/experience-and-license-point-award.md) and
[party control](../11-Party/party-roster-and-control-suppression.md).

## Not yet documented

Major chains still owed, roughly by value:

- Main loop -> per-frame subsystem update order (**the spine; everything hangs off it**)
- Zone load -> resource bind -> actor population -> spawn controller activation
- ScriptVM verb -> native handler -> engine state, for the full call catalog
- Enemy AI decision -> target selection -> command issue
- Damage resolution -> HP change -> KO -> death consequence -> reward trigger
- Treasure/interactable activation -> reward -> inventory
- Save write -> persistent payload layout -> load restore
- Audio event -> voice allocation -> stream
- Render frame build -> Phyre pipeline -> present

## Recording rules

1. Show the **complete** order, not just the interesting hop.
2. Mark every owner boundary and say who owns what.
3. State both directions - upstream causes and downstream consequences.
4. Call out mechanisms that look like part of the chain but are not
   (the "Do not confuse with" section exists for this).
5. A cross-boundary chain is documented **where its mechanism is explained** — normally the page
   that owns the mechanism — and **indexed here with every owner it crosses named**. A chain that
   belongs to no single page gets its own document in the *upstream* category's `call-chains/`
   folder.

   *Restated 2026-09-14 to describe the corpus (`OPUS-REQ-CALLCHAINS-RULE5`). This rule used to say
   that every chain crossing an owner boundary lives in an upstream `call-chains/` folder. Of the 35
   chains in the table above that cross an owner boundary, **exactly one did**; 32 point at an
   ordinary subsystem page and 2 are a section of the page above them, and the corpus contains
   **exactly one `call-chains/` folder**. A rule met once in thirty-five is not governing the
   corpus, and leaving it stated that way made this index describe a filing system that does not
   exist.*

   *It also mis-modelled the unit. **These 32 chains are not documents** — they are sections of pages
   that explain the mechanism, so obeying the old wording meant authoring 32 new documents and
   duplicating the explanation, not moving 32 files. Explaining a chain beside the mechanism it runs
   through is the better arrangement, not a lapse from one. The single conforming case earned its
   folder honestly: field init → weather roll → apply → Movement → LegacyPS2GS rebuild crosses four
   owners and belongs to no one page.*

   > **The purpose the old wording reached for was findability from the upstream side, and it is
   > this index that delivers it.** The `Owners crossed` column is the by-owner entry point, which
   > is why naming **every** owner a chain crosses is the binding half of this rule rather than a
   > courtesy. **The residual cost is real and is stated rather than hidden:** a reader sitting on
   > an upstream subsystem page still will not see the chain unless they come here.

6. **Every owner transition carries one of two labels, and both name their owners.** Rule 2 has said
   "mark every owner boundary and say who owns what" since this index was written, and it has never
   said *in what form* — so the corpus marks boundaries ten different ways and nothing can count
   them. This is that form, written 2026-09-18 at `FRONTIER-REQ-OPUS-CHAIN-AUTHORITY-TRIGGER-CONVENTION`
   so final-audit pass 21 has something to measure.

   ```
   [AUTHORITY NN -> NN]    the DECISION crosses
   [TRIGGER   NN -> NN]    only CONTROL crosses
   ```

   `NN` is the two-digit category number (`18` for Audio, `22` for Middleware-PhyreEngine), or
   `EXT` for an owner outside the image entirely — the OS, a driver, hardware.

   **`*` means "more than one owner, selected elsewhere", and it is allowed on either side — but it
   has to be earned.** Both halves of that were found by applying this rule to real transitions
   rather than by designing it.

   *On the source.* The audio entry point's chain begins "UI / event script / battle logic decides a
   sound should happen" — **three owners enter the same hop**, which is the ordinary shape of an
   entry point, and forcing one of them to be picked would have manufactured a fact.

   *On the destination, which the first draft of this rule refused.* `002621D0` is the script VM's
   native-command dispatcher: above it the state belongs to the VM, **below it to whichever
   subsystem the handler edits**, chosen at run time from `familyTables[id>>12]`. A dispatcher
   genuinely does not know where it lands. Writing "a hop always knows where it landed" was a
   guess about the corpus that the corpus refuted within the hour.

   > **What keeps `*` from becoming "I did not look":** it is only admissible when the alternatives
   > are *selected elsewhere* — a table, a slot, a caller set — and **that selector must be named in
   > the surrounding text**. `*` because the set is plural is a fact; `*` because the set is unknown
   > is a gap, and a gap is written as one.

   **"Owner" means three different things in this corpus, and rule 6 labels only one of them.**
   Working the backlog turned up two markers that are not subsystem crossings at all:

   - `r2-force-fight-toggle.md` marks `00252C80 -> 01E0C2B8` *"[OWNER transition: the flag]"*. The
     whole chain is Input's; what crosses is **not a subsystem boundary but a durability boundary** —
     the arbitration's decision stops being a computation and becomes a global that fifteen
     consumers read later, most of them Movement. There is no call into another owner.
   - `cutscene-name-slots-and-the-depth-of-field-sidecar.md` marks `0020A760`, and its own prose
     puts the transition at `001A5760` instead, *"where the slot record takes ownership of the name
     buffer and becomes responsible for releasing it"*. That is **memory ownership** — a lifetime
     question, and the type store's business rather than this index's.

   Both are real and worth recording; neither is `[AUTHORITY]` or `[TRIGGER]`. A row that is one of
   the other two says so — `[DECISION SETTLES, not a subsystem transition]`, `[MEMORY OWNERSHIP, not
   a subsystem transition]` — and the checker counts it as declared rather than as backlog.
   **Forcing them into this rule's two verbs would have produced two labels that were wrong in the
   same way the unlabelled markers were vague.**

   **`TRIGGER` labels the hop, not the caller — and existing pages use the word the other way.**
   `texture-mip-local-memory-budget.md` writes "`002F7380` THIS `[Presentation mechanism, Movement
   trigger]`", meaning *Movement is what causes this to run*. That is a statement about the **source**
   and it is perfectly true; under this rule the same hop is an **AUTHORITY** transition, because the
   mechanism it lands in is Presentation's and Presentation decides the outcome. The two readings do
   not conflict once the subject is fixed: **the label is about what crosses the hop, never about who
   pushed.** Where a page already says "X is the trigger" in the causal sense, leave the sentence and
   label the row.

   **The discriminator is what a reimplementation must own.** If reproducing the outcome means
   reimplementing the destination's *decisions* — state it reads that the source never passed,
   branches the source cannot predict — the transition is **AUTHORITY**. If the outcome is
   determined by the arguments the source chose, it is a **TRIGGER**, and the destination is a
   mechanism the source drives.

   > The two are not a spectrum and the test is not "is the callee complicated". `00249C60` is an
   > AUTHORITY transition into Audio because the gate at `02091098` can refuse the whole request and
   > the caller never learns why; a `memcpy` into a middleware buffer is a TRIGGER no matter how much
   > code is on the far side, because nothing over there decides anything.

   **Why the distinction earns its keep:** a chain that is all TRIGGER hops can be reimplemented from
   its head alone, and one with an AUTHORITY hop cannot — the far side has to be reimplemented too,
   or preserved. That is exactly the question reconstruction readiness asks of every crossing, and
   until now the chains recorded the crossing without recording the answer.

   **The existing markers are legacy and the checker counts them UNLABELLED**, which is the honest
   starting number rather than a grandfather clause: `check_chain_transitions.py` reports labelled,
   unlabelled and malformed separately, and **only the unlabelled count is a backlog**. It cannot
   tell a *mis*labelled transition from a correct one — that judgement needs the definition above and
   a reader — so the check measures form and the convention supplies the meaning.

## Cross-subsystem accessor hubs

Registered from cross-reference audit pass 3, 2026-09-02. Full document:
[`../00-Engine-Core-Runtime/Shared-State-Accessors/cross-subsystem-accessor-hubs.md`](../00-Engine-Core-Runtime/Shared-State-Accessors/cross-subsystem-accessor-hubs.md).

Three small accessors carry most of the traffic between otherwise separated owners:

| Hub | Size | Callers | Subsystems | Largest consumer |
|---|---:|---:|---:|---|
| `Actor_GetWorldPosition` (`00265020`) | 61 B | 79 | 12 | Script VM (23) |
| `WorldTransition_GetActiveOrPendingFieldId` (`003148F0`) | 27 B | 49 | 10 | World/Area/Field (10) |
| `BattleUnit_GetBySlotIndex` (`00236820`) | 37 B | 40 | 9 | **Movement (10)** |

Three edges that no category document had connected:

```
Audio (00362850)            -> Actor_GetWorldPosition          3D positional audio
SpawnKeep_RotateBanks...    -> WorldTransition_Get...FieldId    area change drives bank rotation
Movement (10 call sites)    -> BattleUnit_GetBySlotIndex        pool is not combat-only
```

And one structural fact reached through the second hub:

```
areaId = max(0, SaveImage_GetPersistentPayloadBase()[0x1044])
```

**The current area is save state**, which is why 49 callers across 10 subsystems read it from the
save payload rather than from a runtime global.

## The foe-class gate, three sightings

Registered 2026-09-02. One authored classifier decides which foes matter to three separate systems:

```
isRewardingFoe(unit) = unit.pBkbi.wDefinitionSelector[+1] == 1
```

| Subsystem | Function | Consequence when false |
|---|---|---|
| Rewards | `Reward_ComputeExperienceForRecipient` (`002F8BB0`) | no EXP from this foe |
| Rewards | `Reward_ComputeLicensePointsForRecipient` (`002F90C0`) | no LP from this foe |
| Combat AI | `BattleEnmity_UpdatePeriodicDecay` (`00321530`) | keeps no threat table |
| Combat AI | `BattleEnmity_ApplyActionParameters` (`003216E0`) | tests `== 0`: the caster side |
| Rewards | `EnemyChain_UpdateOnDefeat` (`00317ED0`) | does not build or break a chain |

Each was read independently, in a different block, without searching for the pattern. This is the
second constant to behave this way - see also the `0x80000003` status mask below.

**The class byte, both values.** 2026-09-02: `BattleEnmity_ApplyActionParameters` tests the *same*
byte for `== 0`, which decodes the field completely:

```
wDefinitionSelector  u16
  low  byte   combatant id (indexes the 40-entry enmity table as table[id + 1])
  high byte   class: 0 = party-side, 1 = foe
```

| Value | Meaning | Consequences |
|---|---|---|
| `1` | foe | awards EXP, awards LP, maintains a threat table, receives enmity propagation |
| `0` | party-side | **generates** enmity as an action's caster |

## The `0x80000003` functional predicate, four sightings

```
nonFunctional(unit) =  ((unit.statusLayer0 | unit.statusLayer1) & 0x80000003) != 0
                    && FieldData_GetActiveFieldRecordBit15() == 0
```

| Subsystem | Function | Consequence |
|---|---|---|
| Combat action | action eligibility gate | the unit cannot act |
| Rewards | `Reward_ComputeExperienceForRecipient` / `...LicensePoints...` | earns nothing |
| Party | `PartyControl_RecomputeSuppressionFromLeaderBattleState` (`0023B040`) | player loses control |
| Combat AI | `BattleEnmity_WriteAllCombatantIds` (`00321D30`) | threat cannot be written |
| Combat AI | `AiOrder_EvaluateAndResolveActionTarget` (`003014C0`) | no gambit is evaluated at all |
| Combat Action | `BattleAction_CheckActionAvailabilityReason` (`002FFCF0`) | action unavailable (returns 2) |

All six read independently, in six separate blocks.

## `DAT_02089340` - a shared global runtime flags word

Registered 2026-09-02. Two subsystems test different bits of the same global:

| Bit | Subsystem | Effect |
|---|---|---|
| `0x20` | Combat AI - `AiOrder_EvaluateAndResolveActionTarget` | suppresses AI action selection |
| `0x40` | Party - `PartyControl_RecomputeSuppressionFromLeaderBattleState` | seeds control suppression |

Neither document had this cross-link; both were read independently.

## The two gameplay RNG streams

Registered 2026-09-02 from a full reverse-edge census. Full document:
[`../21-RNG-And-Determinism/rng-streams.md`](../21-RNG-And-Determinism/rng-streams.md).

```
LCG  (00328370, state 0x022C256C)   15 callers   -> DECISIONS
       spawn placement, AI target choice, weighted action pick, stance timers
       seeded by g_uAreaInitLcgSeedSequence++ at BattleSystem_InitializeAreaState

MT19937 (00379CD0)                  66 callers   -> OUTCOMES
       damage, guard/parry, knockback, combo count, status duration
       53 of the 66 callers are BattleFormula_*
```

**Corrected 2026-09-02.** A write scan found **seven further LCG consumers the call census missed**,
all inlined, all in Rewards: `EnemyChain_UpdateOnDefeat`, `EnemyChain_TryAdvanceRank`,
`Loot_RollAdditionalItemChance`, `Loot_RollNormalSlotChance`, `Loot_RollNormalSlotQuantityBucket`,
`Loot_SelectChanceProfileByWeight`, `FUN_00319530`.

**So loot rolls are on the LCG**, and the "decisions vs outcomes" split is wrong. The accurate
statement:

> **MT19937 is the combat-formula stream** (53 of 66 callers are `BattleFormula_*`).
> **The LCG carries spawn placement, AI choice, stance timers, loot and enemy chain.**

The LCG needs one `u32` plus a draw count to reproduce; MT19937 needs 624 words. **A call-edge
census cannot find inlined consumers of a small function - scan writes to the state instead.**

## Field action -> RNG -> permanent save bit

Registered 2026-09-02 from crossref audit pass 5. `BattleUnit_TryTriggerNearbyAuthoredFieldAction`
(`002F8060`) spans four owners in one body:

```
WorldTransition_GetActiveOrPendingFieldId    World/Area  - which area
proximity gate on a nearby authored record   CombatAction
RNG_MT19937_NextU32_Thunk                    RNG         - roll % 100 < 75  (75/25)
PersistentFlag_SetBank512Low(record[2], 1)   Story       - PERMANENT save bit
```

**A save-persistent flag is set from an MT19937 draw.** Unlike the LCG cases, the consequence is not
a transient outcome but a bit written into the save image at payload `+0x14B4`. Two clients that
disagree on this roll disagree permanently.

**The surface is exactly two functions** (AF-4, 2026-09-02). Intersecting 17 persistent-flag setters
against 91 RNG consumers over the whole call graph yields **2**, and both write `Bank512Low` from
MT19937:

| Function | Flag id | Split |
|---|---|---|
| `002F8060` `BattleUnit_TryTriggerNearbyAuthoredFieldAction` | `record[2]` | hardcoded 75/25 |
| `002FAFD0` *(unowned)* | `record[9]` | authored threshold, then 50/45/5 |

Reconciling those two call sites covers the **entire** path by which a random draw becomes
irreversible save state.

## The shared authored-table header

Registered 2026-09-02. Four subsystems reach authored data through the same shape:

```
<table global>
  +0x04   i32   entry count          (seen in loot; equipment not yet checked at +4)
  +0x08   u16   row stride
  +0x0C   u32   RVA  ->  ImageAddress_ResolveRuntimePointer  ->  row array
```

| Table | Global | Document |
|---|---|---|
| Loot profiles | `DAT_02EBF0C0` | Rewards - loot drops |
| Equipment definitions | `DAT_02EBF0F8` | Items - id encoding |
| Weighted action ids | `DAT_02EBF160` | Combat AI - gambits |
| Resource sections | - | Resource pipeline |

The three `DAT_02EBFxxx` globals sit within `0xA0` bytes of one another, so this is a **table of
tables** rather than four unrelated globals. `ImageAddress_ResolveRuntimePointer` is the general
authored-data access path, not a per-system detail.

**Corrected 2026-09-02:** the full array runs `0x02EBF008`-`0x02EBF1F8` (63 slots, 8-byte stride),
but **not every slot is an authored table**. `0x02EBF190` is a mutable battle-system runtime state
block of >= 23 KB whose `+0x04` is a bitfield, not a count. Membership in the array does **not**
imply the count/stride/RVA header. Identified so far:

| Slot | Contents |
|---|---|
| `0x02EBF0C0` | loot chance/quantity profiles (authored table) |
| `0x02EBF0F8` | equipment definitions (authored table) |
| `0x02EBF138` | **action definitions**, ids `0`..`0x21E` = 543 (authored table) |
| `0x02EBF160` | weighted action ids (authored table) |
| `0x02EBF190` | **battle-system runtime state block** (NOT a table) |

## Area data (`.ard`) binding

Registered 2026-09-02. The authored-data registry is populated per load, not statically:

```
<map>.ard loaded from the VBF archive
  -> AreaData_BindAndRebaseSectionDescriptor (003845F0)
     -> generated per-slot setter (002383C0 .. 002385A0, 0x30 apart)
        -> registry slot at 0x02EBF008 + i*8
  -> rows reached via RVA + ImageAddress_ResolveRuntimePointer  (survives rebasing)
```

Original authoring paths survive in the shipping build:

```
PS2Data\plan_master\in\plan_map\<map>\area\<map>.ard
```

Sibling mechanisms under their own names: `Navigation_BindAndRebaseDataset` (Movement),
`InventoryRuntime_RebaseClassDescriptorsAndClearDerivedState` (Items).

---

## Verb-to-verb: a script verb calling another verb's native handler

**Added 2026-09-02. This is a transition class the database did not previously have**, and it is not
a wrapper, a thunk or a shared helper: the callee is a **full verb in the same dispatch table**, and
the **operand stack is the calling convention**.

```
script issues setentrypos (0x0405)
  -> 00354FB0  pops one index, looks the entry up
     -> PUSHES four floats onto the operand stack
     -> calls 00350510  == the result callback of 0x0019 setpos_19 (declared 4 arguments)
        -> setpos_19 reads those four floats as its own arguments
```

```
script issues ucsetpos (0x0168)
  -> TAIL JUMPS into 0034EBC0 == the handler of 0x0001 setpos (3 arguments)
     -> or drains three floats when its target does not resolve
```

Seven rows use this. The values travel over exactly the stack a script would have used, so from the
callee's side there is nothing to distinguish a verb-issued call from a script-issued one — which is
why it is invisible to a call-graph reading that only classifies edges by owner.

**Consequence for anyone tracing gameplay:** a verb's observable effect may be another verb's
handler, and the argument count at the *call site* is not the argument count of the *effect*. The
seven `*sync` verbs are the degenerate case — producer and consumer inlined into one function with a
compile-time-constant argument, which is why they measure net zero and are genuinely zero-argument.

Owner document:
[`../01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-verb-dispatch-and-parameter-encoding.md`](../01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-verb-dispatch-and-parameter-encoding.md)

## Chains established 2026-09-03

**Three of these cross more owners than any chain previously in this index, and one crosses two file
formats.** Each names what it does **not** establish, because a chain index is where a shared-consumer
argument gets read as a traced dataflow.

| Chain | Owners crossed | Document |
|---|---|---|
| Cutscene asset name -> slot classification -> DoF sidecar JSON -> shader uniform | Resource -> Presentation -> GPU | [`../99-Unresolved-Residual/Cutscene-Asset-Slots/cutscene-name-slots-and-the-depth-of-field-sidecar.md`](../99-Unresolved-Residual/Cutscene-Asset-Slots/cutscene-name-slots-and-the-depth-of-field-sidecar.md) + [`../17-Presentation-Rendering/Post-Processing/the-post-processing-effect-catalogue.md`](../17-Presentation-Rendering/Post-Processing/the-post-processing-effect-catalogue.md) |
| Cutscene asset name -> two flags -> script stand-down gate -> per-frame script pacing | Resource -> Script/VM -> ActorEntity | [`../99-Unresolved-Residual/Cutscene-Asset-Slots/cutscene-name-slots-and-the-depth-of-field-sidecar.md`](../99-Unresolved-Residual/Cutscene-Asset-Slots/cutscene-name-slots-and-the-depth-of-field-sidecar.md) |
| ScriptVM wait command -> in-progress flag -> stand-down veto -> re-poll next frame | Script/VM -> ActorEntity | same document |
| Actor-manager flag byte -> escape hatch -> terminates every scripted wait for that manager | ActorEntity -> Script/VM | same document |
| Console command id -> dispatch table -> arm -> render settings block -> 25 consumers | Developer console -> Presentation | [`../00-Engine-Core-Runtime/Developer-Tuning-Console/what-the-console-tunes.md`](../00-Engine-Core-Runtime/Developer-Tuning-Console/what-the-console-tunes.md) |
| Console command 103 -> off edge -> re-seed ids 104-106 from live engine object | Developer console -> engine object | [`../00-Engine-Core-Runtime/Developer-Tuning-Console/ARM-CATALOGUE-WORK-DIVISION.md`](../00-Engine-Core-Runtime/Developer-Tuning-Console/ARM-CATALOGUE-WORK-DIVISION.md) |
| R2 -> input arbitration -> capability mask -> force fight mode flag | Input -> CombatAction | [`../15-Input/Modal-Toggles/r2-force-fight-toggle.md`](../15-Input/Modal-Toggles/r2-force-fight-toggle.md) |
| Field record bit 15 -> forces the R2 toggle off -> a town pins the mode | WorldAreaField -> Input -> CombatAction | same document |
| `setmapwind` / `defaultmapwind` -> two-source multiplexer -> Presentation backend init | Script/VM -> WorldAreaField -> Presentation | [`../03-World-Area-Field/Weather/mweather-resource-format.md`](../03-World-Area-Field/Weather/mweather-resource-format.md) |

### What these chains do NOT establish

**The depth-of-field chain crosses a file-format boundary and the crossing is a name correspondence,
not a traced dataflow.** `mDofFocusDistance` is read from `JsonData/CutScenes/<name>.json`;
`fParam_FocusDistance` is a shader uniform. **No code path between them has been followed.** The
argument that they are the same value is that **the two functions naming the render settings are the
same two that read the JSON keys** — a shared-consumer argument, which is strong evidence and not a
trace.

> **A chain index is exactly where that distinction gets lost.** A row reading *"JSON key -> shader
> uniform"* invites a reader to assume somebody followed it. **Nobody has.**

**And the console-to-settings chain rests on five of ~~25~~ 28 functions**, the five carrying strings.
*(Corrected 2026-09-30, OPUS: 28 functions reference the render-settings block and 24 access it; `block_refs_count.py`.)*
**Naming the block is not naming its fields** — there is no verified name-to-offset binding, so no row
here says which console command tunes which named setting.
