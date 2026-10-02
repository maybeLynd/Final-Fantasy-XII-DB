---
system: Weather apply and environment materialization
category: 03-World-Area-Field
status: DOCUMENTED
owner_layer: PrimaryOwner:WorldAreaField
evidence_tier: 1
verified_against:
  gzf_sha256: 2ed8affb732f0def0a7852e0788298ae36b81206099dd1712f59825fc1c00bb9
  snapshot_sha256: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity across GN160 -> GN161 - this document cites none of the 109 functions batch R109 touched, so every per-function record it rests on is byte-identical in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md (six ledger figures re-derived)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  previous_parent: 381d2aea82b96d7af781844e191d9b92a37e93bd2d4ff276a33ba56e7307461b
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-02
audit:
  passes: 1
  last_pass: 2026-09-02
  last_pass_state: reverification-against-current-parent
  crossref_clean: true
  reopened_count: 1
---

# Weather apply and environment materialization

> `0026D910` is the shared native owner for "make this Weather Slot real". It is not a setter.

## 1. What the player sees

The moment weather actually changes: the sky, lighting and environment update, and the
gameplay weather class the combat formula reads flips over. One transaction.

## 2. Native mechanism

Input is a Weather Slot in the authored `1..3` domain.

1. if a positive developer override is active, use it instead;
2. clamp/convert to the native three-slot domain;
3. obtain the SaveImage persistent payload;
4. inspect `payload+0x1061` `bInitializationRestoreState`:
   - **clear** -> commit the requested zero-based slot to `payload+0x1060`
   - **set** -> *preserve* the already-committed slot instead
5. select the corresponding one-of-three authored MapRef/environment subrecord;
6. derive and publish current WorldAreaField runtime parameters;
7. extract the MWeather 3-bit preset and collapse it to the gameplay class in `02099DAC`;
8. derive the global environment class into `02099DA8`;
9. clear `bInitializationRestoreState`;
10. continue into the downstream field -> Presentation refresh.

Step 7 is the critical one: **the apply publishes gameplay state, not just visuals.**

### Downstream Presentation refresh

The tail reaches `002E3D40` in zero mode, which resolves field context (`003148F0`),
canonical WorldAreaField state (`00264F10`), the committed slot (`00265920`), extracts the
three MWeather fields (`00377850`, `003777A0`, `003777B0`), and tail-enters `0040AAD0` -
the Presentation backend mode/orientation initializer.

### Entry census

Only **four** direct control-flow entries exist in the whole executable:

| From | Context |
|---|---|
| `0025ACA0` (tail jump) | the normal weather transition roll |
| `00266E74` | global field/world bootstrap |
| `00266E7B` | the immediately following second bootstrap apply |
| `003565C0` | authored `setweatherslot(int)` ScriptVM handler |

That small, coherent caller set is what makes `0026D910` the shared apply owner.

### The duplicate bootstrap apply

`00266D10` contains:

```
00266E42  MOV EBP,1
00266E72  MOV ECX,EBP
00266E74  CALL 0026D910
00266E79  MOV ECX,EBP
00266E7B  CALL 0026D910
```

No intervening semantic call. Both are genuine, and `0026D910` is **not** side-effect free.
With restore state set beforehand, the first pass materializes the *previously saved* slot
(publishing its live environment parameter bank through `00180620` -> `001A7E40`) and clears
the flag; the second then commits baseline slot 1. The first pass also advances the shared
Presentation PRNG by 14 steps.

So it is not a dead duplicate - but the designer's *reason* remains unproven.

> **Naming note.** The GFZ calls `0026D910` `WorldField_InitializeCurrentFieldRuntimeParameters`.
> This database uses `WorldField_ApplyWeatherSlotAndDerivedEnvironmentState` for the same 418-byte
> function, for the reasons argued in §2. Both names appear in
> [`weather-probability-and-transition-roll.md`](weather-probability-and-transition-roll.md), which
> now records the equivalence.

## 3. Key addresses

| Address | Working name | Body | Role |
|---|---|---:|---|
| `0026D910` | `WorldField_ApplyWeatherSlotAndDerivedEnvironmentState` | 418 B | the apply owner |
| `002E3D40` | field -> Presentation refresh (zero mode) | - | downstream |
| `0040AAD0` | Presentation backend mode/orientation init | 286 B | consumes MWeather |
| `00180620` -> `001A7E40` | environment parameter publication | - | per-slot live bank |
| `001F08A0` | direction normalise/publish | - | writes `02CB8420/24/28` |
| `00263E10` / `00263E20` | environment / MWeather class getters | 7 B each | gameplay readers |
| `00266D10` | broad bootstrap | - | the double apply |

## 4. Data structures

```
payload +0x1060  s8   committed Weather Slot (0..2)
payload +0x1061  u8   bInitializationRestoreState
02099DA8         u32  global environment class 0..3
02099DAC         u32  MWeather gameplay class 0..2
02CB8420/24/28   f32  normalized environment direction vector — the
                     (x, y, -z) form; `001F08A0` materialises both
                     handednesses into the live object ((-x,-y,z) at
                     +0xDC..+0xE4, (x,y,-z) at +0xFC..+0x104) and the
                     global gets the second — the flip happens at
                     publication, not in the renderer (001F08D1-001F094F)

Live environment runtime object (via 001A7E40) - the shadow parameter set (named 2026-09-26, section D-4 below)
  +0x140, +0x144        per-slot dword lanes: mShadowValueLerpMinForMap / ForChr
  +0x870/874/878        per-slot scalar lanes: mCascadePartition0 / 1 / 2
                        plus a three-float vector from a slot-indexed bank
```

## 5. Call chain

See [`call-chains/field-init-weather-to-legacyps2gs-rebuild.md`](call-chains/field-init-weather-to-legacyps2gs-rebuild.md)
for the full fan-out.

## 6. Modding notes

- **This is the seam.** `0026D910(slot)` is the highest proven non-VM transition that both
  commits the slot and materializes everything downstream.
- Do not call the ScriptVM wrapper `003565C0`; do not write `payload+0x1060`.
- Authored `setweatherslot` performs `0026D910(slot)` **then** `0026D8F0()` (arming restore
  state for the next apply). Reproducing a scripted weather event may need both; ordinary
  synchronisation must not blindly do both.
- Runtime weather changes do **not** force the Movement/LegacyPS2GS resource rebuild. Only
  field initialization does. Preserve that split.

## 7. What is not known

- [x] ~~Designer reason for the duplicate bootstrap apply (open question **D-2**).~~ **Closed
      2026-09-12 (FABLE): the mechanism is the whole of what the image holds.** `0026D910(slot)`
      writes the requested slot into the field state's `+0x1060` only when the restore byte
      `+0x1061` is clear (`0026D951`–`0026D95E`), materializes whatever `+0x1060` then holds, and
      clears `+0x1061` at `0026DA92`; `+0x1061` is set by `0026D8F0` (the authored
      `setweatherslot`'s arming call) and by `WorldPersistence_ResetBanksAndMarkInitializationState`
      (`0026836C`, when `0209AC10` is zero — F-3). *Corrected 2026-09-13:* this row said `00280140` also sets it;
      on its restore route (message 18, request bit 9) `00280140` calls `00268320` and then, when `0020E5A0()` returns 5,
      **clears** it — `00280213` stores `dil`, and `edi` was zeroed at `002801A0` ([spawn page §17](../../05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md)). So the bootstrap's pair is **"honour a pending restore, then
      commit the baseline"**: when a restore is armed, pass 1 materializes the saved slot and disarms
      it, pass 2 commits slot 1; when none is armed, pass 1 already commits slot 1 and pass 2 repeats
      it, costing the 14 PRNG steps §2 measured. Whether the designers wrote two calls for that
      reason or by accident is not a fact the binary carries; the row is retired as an intent residue.
- [x] ~~Whether a higher non-VM apply seam exists (open question **D-3**).~~ **D-3 ANSWERED 2026-09-12 (FABLE): no runtime seam above it — only boot.** `WorldField_InitializeCurrentFieldRuntimeParameters` (`0026D910`) has exactly three call sites: the script verb **`setweatherslot`** (`0x021A`, thunk `003565C0`, [the verb table](../../01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-verb-table.tsv)) and two back-to-back native calls with argument 1 at `00266E74` / `00266E7B` inside `00266D10`, a 1,185-byte subsystem initialiser that the boot function `0022A0B0` ([what the engine fixes at boot](../../00-Engine-Core-Runtime/what-the-engine-fixes-at-boot.md)) runs once at `0022A3F7`. So at runtime every weather apply comes through the VM verb; the only higher non-VM seam is the boot pass, which primes the seam twice and never returns to it.
- [x] Physical rendering role of the published direction vector (open question **D-4**).
      **Narrowed 2026-09-17 (OPUS's finding, verified instruction-exact by SWE2-FRONTIER):**
      the sole writer `001F08A0` and sole reader `006084B0` are both fully read. The reader
      is a **verbatim passthrough** — `0060899E`–`006089DA` copies `02CB8420/24/28` unchanged
      into the descriptor at `+0x560/+0x564/+0x568` and continues with `02CB8430` — so whatever
      the vector means, the renderer treats it as a shader-constant slot, not a transformed
      direction. The naming question that remains — direction-of-travel vs direction-to-source —
      differs by exactly the sign `001F08A0` materialises both of; the deciding evidence is the
      descriptor's shader-constant binding at `+0x560`, which nothing read so far touches.
      **Narrowed again 2026-09-26 (FABLE, Claude Opus 5.5): the three callers are read. The vector is a direction
      field of one per-scene object, authored per map (default: straight up), and it is published beside the SSS
      switches.** Static.
      - **The object.** `001F08A0`'s receiver is the `0xB08`-byte object that `001F0850` returns, through the static
        pointer `01F82EA8`; the vector-pointer setter allocates it on first use. The vector is its `+0xFC`/`+0x100`/`+0x104`.
      - **Source 1: the map pack.** The tag-25 field environment handler and the tag-9 handler of
        [the map ctrl pack](../Map-Pack/the-map-ctrl-pack.md) (§3.5's tag table names both) pass it through the setter
        that takes a vector pointer. The value is either the chunk's vector at `+0x10`, or a default of
        **(0.0001, 1.0, 0.0)**, almost straight up, which both handlers store before their calls. The 0.0001 keeps the
        vector off the exact vertical, the usual guard for building a basis from it; that purpose is an inference.
      - **Source 2: a per-index preset.** `001A7E40(table, i)` copies entry `i` of a table into the singleton: two
        dwords to `+0x140`/`+0x144`, the direction (when byte `+0x398` is set), and a float triple to
        `+0x870`/`+0x874`/`+0x878` (`001A7E5F`–`001A7EF9`).
      - **Source 3: two angles.** `001C7850(a, b)` rotates a base vector by two angles given in degrees (`001C4F50`: `π/180`
        scaling, two axis rotations) before storing. Its only caller is `001C3D50`, the same body that
        writes the `02CB80xx` render globals.
      - **The neighbours.** `006084B0` copies this vector in the same pass as `02CB8430`–`02CB8440`. OPUS declared that
        block as the SSS lighting parameters (console ids 167/168, SSS enable and width, at `02CB8434`/`02CB8438`). So
        the direction reaches the renderer beside the subsurface-scattering switches.
      - *Still open:* the shader binding of the descriptor's `+0x560`. The sources fit a scene light direction —
        authored per map, default up, set beside ~~a colour-like triple~~ the shadow cascade partitions *(corrected
        2026-09-26, below)* — but that name is an inference until the binding is read.
      **ANSWERED 2026-09-26 (FABLE, Claude Opus 5.5): it is the scene's light direction. The data names it: almost every map's
      JSON (439 of 459) authors it as two angles, `lightOrientation` and `lightHeight`, in degrees.** Static plus the shipped data.
      - **The data.** `jsondata/maps/*.json` carries `lightOrientation` / `lightHeight` in 439 of 459 files, with
        `lightOrientation2`/`3` and `lightHeight2`/`3` beside them. `jsondata/cutscenes/*.json` carries them in 283 of
        337. Heights cluster at 60–80 (70 in 51 map files); orientations are spread round the compass.
      - **The map path.** The map-JSON loader reads each pair and hands it to `001C78D0(i, orientation, height)`, which
        builds the vector with the two-angle routine `001C4F50` (degrees to radians, two axis rotations). It stores the
        vector as entry `i` of the per-index table through `001A9B30`, which also sets the table's byte `+0x398`, the
        flag `001A7E40` tests. It then calls `001AA3B0`, which selects an entry through `001A7E40` and so publishes it
        (Source 2 above).
      - **The cutscene path.** The cutscene-JSON loader reads the pair only when the file sets `enableLightInfo`, which
        exactly one of the 337 cutscene files does. It then passes the pair to `001C7850` (Source 3 above).
      - **So the role is the key light's direction.** An orientation angle and a height angle are a light's azimuth
        and elevation; with neither authored, the map pack's default points it straight up. Its neighbours in the
        published record are the SSS switches. Which shader constant reads the descriptor's `+0x560`, and whether the
        stored sense points at the light or away from it, stay as stated above.
      - **Sharpened and corrected 2026-09-26 (FABLE, Claude Opus 5.5): the object is the shadow system's parameter set,
        so the direction is the shadow-casting light's.** The cutscene-JSON loader writes this object through its cached
        pointer `01F812C8`, which `0015CC00` sets to `001F0850()`. The key strings name its fields:
        - `+0x140` / `+0x144`: `mShadowValueLerpMinForMap` / `ForChr`;
        - `+0x870` / `+0x874` / `+0x878`: `mCascadePartition0` / `1` / `2`, the cascade split distances;
        - `+0x890` / `+0x894`: `m_iPCFBlurSize` / `ForMap`;
        - `+0x898`: `ShadowBias`;
        - `+0x8A0` / `+0x8A4`: `m_iBlurBetweenCascades` / `m_fBlurBetweenCascadesAmount`.

        So the per-index entry `001A7E40` copies is a shadow set: the two lerp minimums, the direction and the three
        cascade partitions. The earlier "colour-like triple" was wrong. The near-vertical default (0.0001, 1.0, 0.0)
        fits the guard a shadow-map view basis needs. The published `02CB8420` copy is therefore the shadow light's
        direction; its shader binding at the descriptor's `+0x560` is still unread.
- [x] Thread/frame requirements for calling it safely (open question **F-1**).
      *SUPERSEDED 2026-09-26 (FABLE, Claude Opus 5.5) under the runtime rule, because the static half is settled. Every in-image path to
      `0026D910` starts at one of three application entries on the main-loop thread: GameApplication's setup, its update
      slot (through `MainLoop_UpdateAndRenderFrame`), and the `setweatherslot` script verb. No thread procedure the image
      starts reaches any of them, and the path takes no lock. Control: `_index/candidates/f1-weather-apply-thread/f1_thread_reach.py` (3 checks). The blind spot is the
      handshake page's: indirect thread starts. The receiver-safe live call the row asks for is not queued.*

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| Full apply transaction | complete body of `0026D910` (418 B, `1703f5dc...b4d2`) | 1 |
| Exactly four direct entries | complete direct control-flow census over authorized `.text` | 1 |
| Duplicate bootstrap is genuine | exact disassembly `00266E42..00266E7B` | 1 |
| First pass publishes real environment state | complete bodies of `00180620` and `001A7E40` | 1 |
| Direction vector has exactly one downstream reader | complete data-reference audit -> `006084B0` only | 1 |
| Reader is a verbatim passthrough into descriptor `+0x560` | exact disassembly `0060899E`–`006089DA`; writer publishes both handednesses `001F08D1`–`001F094F` | 1 |

**Superseded readings:** the first bootstrap pass is **not** proven to be teardown,
interpolation seeding, fade-source setup, backend swap prep, or cleanup. Do not claim any of
those.

## 9. Related

- [`weather-slot-state-model.md`](weather-slot-state-model.md)
- [`mweather-resource-format.md`](mweather-resource-format.md)
- [`../../21-RNG-And-Determinism/rng-streams.md`](../../21-RNG-And-Determinism/rng-streams.md)

## Re-verification 2026-09-02 (AH-2)

Stamped against parent `381d2aea...`; re-checked against the current `2ed8affb...`.

**Addresses:** 24 cited - **19 function entries, 5 interior** (instruction addresses inside
`FUN_00266D10`, cited in this document's own disassembly listing), 0 unresolved.

**Central claim re-derived.** The headline is *"`0026D910` is the shared native owner for 'make this
Weather Slot real'. It is not a setter."*

`0026D910` decompiles in the current parent as `WorldField_InitializeCurrentFieldRuntimeParameters`,
**418 bytes**, and within it: reads and writes save payload `+0x1060` and `+0x1061`, consults
`g_pMapRefResourceRoot`, and calls out to further subsystems. A 418-byte function touching MapRef,
the save payload and Presentation is not a setter. The claim holds.

**Stamp advanced because the bodies were re-read**, per the evidence standard.

## Cross-subsystem neighbours — the Weather field-frame census (audit pass, repos-2d, 2026-09-03)

`audit_crossrefs.py` against `Tools/work/graph_gn` (38,161 functions, 90,525 edges) reported **21
UNACCOUNTED NEIGHBOUR** findings across the six Weather documents and the category README. **They
are almost entirely the same neighbourhood seen from six angles**, because the Weather system is
documented in parts and every part cites the same field-frame routines.

**This section is the census for all of them.** The other Weather documents disposition by
reference to it rather than repeating it — duplicating a census in six files is how one rots.


**ActorEntity — SERVICE (SWE2-EC7-156, 43 edges).** This page's `0022A0B0` calls `002368D0` and `0025D9E0` calls `0025B250`/`0025B600`/`0025B82x` of that layer — the weather frame consumes actor helpers, not a shared responsibility.
**CoreRuntimeScheduling — CLIENT and SERVICE (SWE2-EC7-156, 11 edges).** `0022A0B0` calls `0022BDF0` and is called by `0017D4C0`; `00233780` calls `0032A150` — a two-way runtime-helper exchange, not a second owner.
**Input — SERVICE (SWE2-EC7-156, 7 edges).** `0022A0B0` calls `0035B270`, `00266D10` calls `00226BE0`, `002B7B80`/`002BAF80` call `00250200`/`00250130` of that layer — the weather pass consumes input-side helpers.
**Presentation — CLIENT (SWE2-EC7-156, 76 edges).** `002B7B80`/`002BAF80`/`002BC3E0`/`002D2Dxx` of that layer call `001EDEC0`; batch-121's `003D99B0` helper `0032B600` shares the same fan-in — the render layer reaches weather's helpers, not a shared responsibility.
**Resource — SERVICE (SWE2-EC7-156, 40 edges).** `0022A0B0` calls `00259DF0`/`002DF9A0`/`0032EAE0`/`00379D20` of that layer — the weather frame consumes resource helpers, not a shared responsibility.
**UI — CLIENT (SWE2-EC7-156, 25 edges).** `00252030`/`00276D30`/`0027C870`/`00299090` call `001EDEC0` — the interface layer consults this page's helper, shared fan-in.
- **Audio - CLIENT (161 edges).** `001243B0` is also called by bodies filed to audio: `00121030`, `00121E20`, `00210ED0` - shared machinery across the layer boundary, no shared ownership.
- **CombatAction - CLIENT (6 edges).** `003148F0`, `003590D0` are also called by bodies filed to combat action: `002F8060`, `002FA740`, `00317E60` - shared machinery across the layer boundary, no shared ownership.
- **CombatFormula - CLIENT (54 edges).** `00379CD0` is also called by bodies filed to combat formula: `003851F0`, `00387130`, `00387FD0` - shared machinery across the layer boundary, no shared ownership.
- **Gameplay - SERVICE (6 edges).** `0025D9E0`, `00329CC0` reach bodies filed to Gameplay: `00234150` (CombatAction), `00316DF0` (DefinitionRuntime), `00322C50` (Combat) - shared machinery across the layer boundary, no shared ownership.
- **Movement - SERVICE (29 edges).** `00259B30`, `0025D9E0`, `00266D10` reach bodies filed to movement: `00380D30`, `0025DF00`, `00263560` - shared machinery across the layer boundary, no shared ownership.
- **Party - CLIENT and SERVICE (8 edges).** `003590D0` is also called by bodies filed to party: `00263770`, `00269C70`; `0025D9E0`, `00329CC0` reach bodies filed to party: `003590D0`, `00326500` - shared machinery across the layer boundary, no shared ownership.
- **PlatformOnlineAchievements - CLIENT (2 edges).** `003148F0`, `003160C0` are also called by bodies filed to PlatformOnlineAchievements: `003160C0`, `00315E90` - shared machinery across the layer boundary, no shared ownership.
- **RNG_Random_Selection - SERVICE (5 edges).** `0022A0B0`, `0025ABA0`, `0025ACA0` reach bodies filed to random selection: `00379CF0`, `00379CD0` - shared machinery across the layer boundary, no shared ownership.
- **Rewards_Progression_Economy - CLIENT (2 edges).** `00379CD0` is also called by bodies filed to rewards/progression: `002F9A60`, `002F9B20` - shared machinery across the layer boundary, no shared ownership.
- **SaveLoad - CLIENT (3 edges).** `0020E5A0`, `00268320`, `002EF2B0` are also called by bodies filed to SaveLoad (save/load settings): `00280140` (RuntimeLifecycleSupport) - shared machinery across the layer boundary, no shared ownership.
- **Save_Load_Settings - CLIENT and SERVICE (24 edges).** `001EDEC0` is also called by bodies filed to save/load/settings: `00582860`; `0020E5A0`, `0025ACA0`, `0025D9E0` reach bodies filed to save/load/settings: `001C18E0`, `002EF2B0` - shared machinery across the layer boundary, no shared ownership.
- **Script_VM_Native_Bridge - CLIENT and SERVICE (36 edges).** `00264F10`, `00265920` are also called by bodies filed to script VM / native bridge: `0050CDE0`, `00356250`, `0050D360`; `00266D10` reaches bodies filed to script VM / native bridge: `003DC2D0` - shared machinery across the layer boundary, no shared ownership.
- **Spawn_Encounter_Lifecycle - CLIENT (1 edge).** `003148F0` is also called by bodies filed to spawn/encounter lifecycle: `00233780` - shared machinery across the layer boundary, no shared ownership.
- **Status_Periodic_Terminal - CLIENT (2 edges).** `002F8060`, `00379CD0` are also called by bodies filed to status/periodic terminal: `00310DB0`, `00386C70` - shared machinery across the layer boundary, no shared ownership.
- **Story_Event_Quest_Hunt - CLIENT (14 edges).** `002EF2B0` is also called by bodies filed to story/event: `0032A8A0`, `0032A930`, `0032A9A0` - shared machinery across the layer boundary, no shared ownership.

### Runtime infrastructure: `ImageAddress_ResolveRuntimePointer`

Four of the five `CoreRuntimeScheduling` findings across the category are one 10-byte function,
`0020E600` `ImageAddress_ResolveRuntimePointer`, cited by `002658B0`, `0038B220` (Combat Formula)
and `0040FF30` (Presentation). Its census:

**815 callers across 18 owner subsystems** — Presentation 279, unowned 299, Combat Formula 73,
Combat Action 50, Items 28, Actor/Entity 18, Movement 15, Status 10, Rewards 10, Combat AI 9,
World/Area/Field 6, UI 5, Script VM 3, Resource 3, Audio 3, Input 2, Save/Load 1, RNG 1.

It converts a stored 32-bit image address into a runtime pointer — the convention every authored
table in this engine is addressed through, including
[the field record table](../Field-Record-Table/field-record-table-navimapdata.md) and the status
definition table. **It is runtime infrastructure, not a Weather relationship**, and it is in the
same class as `_guard_check_icall` and `memset`: uninformative as a neighbour *and* as a subject.
The remaining two — `001EDEC0` from `00394130`, and `0022A0B0` calling `00266D10` — are host-frame
scheduling around the same routines.

*Disposition: runtime infrastructure. Census stated here because no document enumerates it —
`cross-subsystem-accessor-hubs.md` ranks it but does not list its callers, so pointing there would
be a deferral rather than a disposition.*

### The RNG the Weather roll uses — documented all along, under its real name

`0025ABA0` and `0025ACA0` call `00379CD0` `RNG_MT19937_NextU32_Thunk`, owner **`RNG_Random_Selection`**.
That is not an unaccounted relationship: it is the Weather transition roll itself, described at
length in [weather-probability-and-transition-roll.md](weather-probability-and-transition-roll.md),
which names **MT19937** thirteen times.

The audit could not see it because **these documents never write the word "random"** — they use the
engine's own algorithm name. The alias list for that owner is `random` / `selection`, and the one
Weather document containing the word "selection" (`weather-slot-state-model.md`, once, in an
unrelated sentence) is the one Weather document with **no** RNG finding. That is a natural
experiment, not a theory.

*Disposition: explained, and it is the subject of a sibling document. The checker's vocabulary gap
is reported to the coordinator rather than papered over — `MT19937` and `RNG` belong in that
owner's aliases.*

### The field-frame routines and their Audio, Party and Actor/Entity callees

The Audio findings (5-6 edges in four documents) and the Party findings are all callees of two
large field-frame routines these documents cite for their Weather role:

| Cited here for | Flagged callees | What they are |
|---|---|---|
| `0025D9E0` `ActorManager_RunFieldRuntimePass` (1,297 B) | `00261F90` (Audio, 335 B), `003590D0` `PartyFocus_GetCurrentPackedActorHandle` (Party, 7 B) | a per-frame field pass: it drives audio and asks who the party focus is |
| `00266D10` field/area initialisation (1,185 B) | `00362F70` (Audio, 516 B), `003B6ED0` (Actor/Entity, 93 B) | area setup: it starts audio and initialises actor state |
| `002620E0` (231 B), `00265920` (41 B) | `00363B40`, `00361810`, `002DE800` (Audio) | small field routines with Audio callers |

A field frame pass that touches audio and the party focus is doing its own job, not a Weather one.
**Weather is one of several things these routines carry**, which is exactly why the documents cite
them — and citing them imports everything else they carry.

*Disposition: field-frame and area-initialisation work belonging to those routines' own systems.*

### `WorldTransition_GetActiveOrPendingFieldId` — disposition by reference

The `ActorEntity` (`00329CC0` `BattleSlotMap_InitializeMappingClasses`, `0025D9E0`),
`CombatAction` (`002FA740`, `002F8060` `BattleUnit_TryTriggerNearbyAuthoredFieldAction`),
`Spawn_Encounter_Lifecycle` (`00233780` `SpawnKeep_RotatePersistenceBanksForAreaTransition`) and
`PlatformOnlineAchievements` (`003160C0`) findings are all **callers of `003148F0`**, the
49-caller field-id accessor.

Its complete caller census — 49 callers across 11 subsystems, verified row by row — is enumerated
in [`../../00-Engine-Core-Runtime/Shared-State-Accessors/cross-subsystem-accessor-hubs.md`](../../00-Engine-Core-Runtime/Shared-State-Accessors/cross-subsystem-accessor-hubs.md)
§2 (hub 2). *Valid deferral: that document contains the census.* Everything in the world asks which
field is active; none of it is a Weather relationship.

### Save/Load

`weather-slot-state-model.md` cites `002EF2B0` `SaveImage_GetPersistentPayloadBase` (**70 distinct
calling functions across 5 owners** — World/Area/Field 23, unowned 31, Story/Event/Quest/Hunt 12,
Actor/Entity 3, Audio 1; those 70 functions contain **121 call sites**, which is the number the
actor-record page quotes) and `00268320` `WorldPersistence_ResetBanksAndMarkInitializationState`, both reached from
`00280140` (924 B). The Weather Slot is **persisted state** — that document's own subject is where
it lives in the save payload — so a Save/Load edge is the relationship, not an unaccounted one.

*Disposition: explained; it is the persistence path the document exists to describe.*

`00280140` carries no `PrimaryOwner`; the audit labels it from its `CodeDomain`, whose family head
is **`SaveLoad`** — a different taxonomy from the owner vocabulary (`Save_Load_Settings`) used
everywhere else. Both name the same subsystem.



## The `00266D10` exclusive subtree — the bootstrap's 32 helpers (SWE2-FRONTIER, exclusive-subtrees package)

The exclusive-callee census assigns 32 frontier functions to `00266D10` — what the broad
bootstrap actually runs. All signature-swept 2026-09-15 (`bshape.py`):

| cluster | members | role |
|---|---|---|
| request/mailbox arms | `002E1450` (`00404DC0` + `0215F200`/`0215F540`), `002EA320` (507 B — `0041D6C0` ×5 + `0036C5A0` ×2 over `0215FD46`–`02164080` cells), `002EA530` (deque ops `0032E400`/`0036C1D0`/`0036A190`/`0036C140`/`0032E620`/`0036C660` + `00D0F8B0`/`021641A0`) | the boot-time request-ring fills — `0215Fxxx`/`02161Dxx` are the router cells the field frame drains |
| `02B5xxxx` list accessors | `003DAE30` (`02B4E4C0` + `02B57CE0`), `003DCBC0` (300 B — deque family + `02B57F70`/`02B580BA`/`02B5817A` + `00D11790` table), `003DD7E0` (`02B581AD`), `003DDD10` (`02B58A80`), `003DE710` (`02B58C72`/`02B59372`), `003DF030` (`02B59360`), `003E7DF0` (`02B5C780`–`02B5D040`, twelve cells), `003EB750` (`00265F90` ×3 over `02B5E160`–`02B5EBB0`), `003EBAB0`, `003EBE40`, `003EC620` | the initialiser's world-state lists — spawn/area record banks zeroed and primed at boot |
| cell writers | `002556F0` (`02092810`/`02096280`/`02096520`/`02096730` quad), `00259E90` (`02097304`/`02097B80`/`B4`/`02097C50` + `003CBFF0` ×3/`00259B30`), `001DC000` (`00210B30`), `00210F60` (`007A5B00`/`007A58D0`/`001243B0`), `002DF2C0` (`02AED560` + `003603C0`/`003CBFA0`/`001DC000`) | named-cell initialisation across `02092xxx`/`02097xxx` |
| listener block | `00360C70` (190 B — deque family + `022CB9F0`), `00362F70` (516 B — `002DEBA0`/`002DF2C0`, `022CBA8C`/`022CBB00`), `0036C5A0` (`022D7FD0`) | the `022CB9xx`/`022CBAxx` audio-listener block priming |
| leaves | `002EFA20`, `002F1A00`, `00314940`, `0035B790`, `0037CB00`, `0037CB10`, `003B6ED0` (`02EBCBE0`), `003BA310`, `003E82B0`, `003E90E0` | ten 7–199 B bodies, mostly single-cell or tail thunks |

The shape fits §2's "broad bootstrap": no single dominant body — instead 32 small writes spread
across the request ring, the `02B5xxxx` spawn/area lists, the `02092xxx` cells and the listener
block. The double `0026D910` apply is the only heavy call inside `00266D10` itself, which is why
none of these members is individually large.

## The `00394130` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`00394130` (530 B) — a real body dispatching on `dword[rdx]`, reaching `0023A110` by a `call` at `003942F9`, not a thunk (no `jmp`-route to `0023A110` exists in the image; corrected 2026-09-27 AUDIT-SEM re-attack).

| member | role | interior |
| --- | --- | --- |
| `0023A110` | `byte[0208D455] = cl` — weather-mode byte setter (`0023A110`) | [`0023A110`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none.

## Interior citation — frontier hub `001EDEC0` (2026-09-17, SWE2-EC7)

`001EDEC0` — 40 B, 29 frontier callers at census; the "host-frame helper" this page lists from
`00394130`. Interior verified: it is a two-global predicate. `dword [01F82E38] == 0` -> return 1;
else `dword [01DFE0C0] != 0` -> return 1; else return `!(arg & 1)` — the `not ecx`/`and ecx,1` at
[`001EDEDA`](../../_index/ADDRESS-INDEX.md) complements the caller's flag bit when the first
global is set but the second is not. An enable/disable mask pair plus a caller-override fallback,
not a computation.

NOT claimed: what `01F82E38`/`01DFE0C0` name semantically.


## Interior citation — frontier hub `00265920` (2026-09-18, SWE2-EC7)

`00265920` — 41 B, 20 callers (5 A-measured); the state getter the weather materialisation
polls. Interior verified: `0017D490()` answers the pending-state count
([`00265924`](../../_index/ADDRESS-INDEX.md)); a positive result re-enters it tail-first
(`00265931`), while zero falls through to `002EF2B0()` and returns
`sign-extended byte [rax+0x1060] + 1` ([`0026593B`](../../_index/ADDRESS-INDEX.md)) — the
stored mode plus one, the "next state" convention this page's transition roll consumes.

## SWE2-EC7-34 update (2026-09-19) - `002DE800`

`002DE800` (830 B) is a vec3 weather/console apply - loads `[rcx]`/`[+4]`/`[+8]` floats, `00265920` gate, `0215E738`/`0215E710` records, `002DE420`/`002DEB1E`/`002DEB14`/`002DEB0A`. Interior anchor `002DE831` (the `00265920` call).

## SWE2-EC7-35 update (2026-09-19) - `00259B30`

`00259B30` (699 B) is a weather apply body - `02098DE9`/`02098DEA`/`02098DEB`/`02098378` flags, `00861EC0`/`00380D30`/`00380B80` quadruples plus `00861F0E`/`00861F08`/`003DA2C0`. Interior anchor `00259B69` (an `00861EC0` call).

## SWE2-EC7-40 update (2026-09-19) - `002E1450`

`002E1450` (374 B) is the request/mailbox arm the page names - the `0215F1A3`..`0215F1D0` requester bytes, a single `00404DC0` tail. Interior anchor `002E15A3` (the `00404DC0` call).

## SWE2-EC7-44 update (2026-09-19) - `00259E90`

`00259E90` (271 B) is a scripted-camera-adjacent cell writer - `00259B30`/`003CBFF0`/`00861EC0`. Interior anchor `00259EA4` (a `00259B30` call).

## SWE2-EC7-44 update (2026-09-19) - `003EB750`

`003EB750` (271 B) is an effect-file body - `00265F90` single call. Interior anchor `003EB788` (the `00265F90` call).

## SWE2-EC7-45 update (2026-09-19) - `003DDD10`

`003DDD10` (240 B) is a body - `00861EC0` single call. Interior anchor `003DDD5F` (the `00861EC0` call).

## SWE2-EC7-48 update (2026-09-19) - `001A7E40`

`001A7E40` (202 B) is a body - `001F0850`/`001F08A0` pair. Interior anchor `001A7E5A` (an `001F0850` call).

## SWE2-EC7-48 update (2026-09-19) - `003DE710`

`003DE710` (201 B) is a body - `00861EC0` single call. Interior anchor `003DE755` (the `00861EC0` call).

## SWE2-EC7-48 update (2026-09-19) - `003E7DF0`

`003E7DF0` (199 B) is a call-free `02B5C7AC`-region pool init - 32x`0x48` records zeroed with `+0x44` = index+`0x20`, then a `02B5C860` 28-entry pointer-link loop and `02B5C810`/`02B5C780`/`02B5D040` publishes. Interior anchor `003E7E00` (the record loop head).

## SWE2-EC7-50 update (2026-09-19) - `002EA530`

`002EA530` (183 B) is a body - `0032E400`/`0032E620`/`0036A190`/`0036C140`/`0036C1D0`/`0036C660`. Interior anchor `002EA56B` (a `0032E400` call).

## SWE2-EC7-50 update (2026-09-19) - `003EBAB0`

`003EBAB0` (183 B) is a call-free `02B5EBC0`-region reset - eight `0x14`-stride (ptr,count) zero pairs plus eight `word 0x100` markers `02B5EBD0`..`02B5EC5C`. Interior anchor `003EBAB2` (the first zero store).

## SWE2-EC7-52 update (2026-09-19) - `002DE420`

`002DE420` (967 B) is a weather/console apply helper - `00861F68`/`00861F62`/`00808C40` plus `0215EF40` record writes. Interior anchor `002DE6B9` (a `00861F68` call).

## SWE2-EC7-56 update (2026-09-19) - `00380B80`

`00380B80` (190 B) is a call-free record defaults initializer - `+0x50`-`+0x5A` zero words, `+0x64`-`+0x98` floats (`0.5`/`2.0`/`18.0`), `+0x0C`-`+0x3C` = `1.0f` run. Interior anchor `00380BB1` (the `+0x64` float write).

## SWE2-EC7-62 update (2026-09-19) - `002DF2C0`

`002DF2C0` (148 B) is a weather cell writer - `001DC000`/`003603C0`/`003CBFA0`/`00808C40` plus `01CEBBA8`/`01F44830`/`02AED560`. Interior anchor `002DF2E0` (a `003603C0` call).



## SWE2-EC7-64 update (2026-09-19) - `00210F60`

`00210F60` (142 B) is a cell-writer body - `001243B0`/`007A58D0`/`007A5B00` plus `01CEBBA8`. Interior anchor `00210F7F` (a `007A5B00` call).


## SWE2-EC7-79 update (2026-09-20) - `00678B50` float fraction split measured

`00678B50` (82 B) is the two-arm divider the weather callers run:
when `float[+0x3C]` is nonzero it writes `+0x28 = xmm2/(xmm1-xmm2)`
and `+0x38 = xmm1*xmm2/(xmm1-xmm2)`; when `+0x3C` is zero it writes
`+0x28 = 1/(xmm1-xmm2)` and `+0x38 = xmm1/(xmm1-xmm2)` - the
scaled-vs-raw fraction split.
Interior anchor `00678B74` (the `divss xmm4, xmm3`).

## SWE2-EC7-92 update (2026-09-20) - `00377A90` resolve-and-forward measured

`00377A90` (29 B) is the forwarder the weather-apply caller
`00259B30` uses: `003148B0(rcx)` resolves the record, then the body
tails `00377AB0` with that result in `ecx` and the original argument
in `rdx`.
Interior anchor `00377A99` (the `003148B0` call).

## The published environment class is not 0..3, and the apply is not slot-atomic (OPUS, 2026-09-21)

Both found while assembling [`CONTRACT-weather.md`](../CONTRACT-weather.md) from the shipping bytes
and the shipped archive. Filed as `CON-146`; the second is registered as `GB-1`.

**§4 types `02099DA8` as a "global environment class `0..3`". The authored domain is `0..4`.**
`0026DA10`–`0026DA26` publishes `dword[A + 4 + envIdx*4]`, where `A` is `mapRefRoot +
header[+0x10]`. That table was decoded from `map_ref.bin`, extracted from the shipped
`FFXII_TZA.vbf` — the `in` and `ch` copies are byte-identical, sha256 `7c63552f…` — and it holds 16
entries with values `{4,4,4,0,0,1,2,2,3,0,0,0,0,0,0,0}`. The index is lane byte 0 of the 16-byte
block, whose histogram over all 279 shipped weather lanes is `0`×163, `1`×64, `2`×19, `3`×7, `4`×4,
`5`×1, `6`×2, `7`×2, `8`×16, `9`×1. **So `02099DA8` = 4 for 246 of 279 lanes** — more than every
other value put together — and the combat stage `0038B220` tests it only for equality with `0`
(`0038B2A8`, `0038B3F4`), `2` (`0038B478`), `1` (`0038B4FE`) and `3` (`0038B584`), with no default
arm. **4 means no environmental element scaling**, which is the state most of the game is in and the
one a `0..3` type has no room for.

**§2 step 7 and the slot-state page's §10 both say the derive re-reads the committed slot. One
published value does not.** The gameplay class at `0026DA2C`–`0026DA31` calls
`00377850(ebp = selector, edx = edi + 1)`, and `edi` is the **clamped requested** slot — untouched
between `0026D943` and `0026DA2E`. The presentation path reached by the tail jump calls the same
extractor with `00265920()`, the **committed** slot (`002E3D6E`–`002E3D79`). They differ exactly
when the `+0x1061` gate at `0026D951` discards the request, so after a scripted `setweatherslot`
arms the flag, the next field-entry roll landing elsewhere publishes **one slot's combat weather
under another slot's sky**. On the ungated path the commit makes them equal, which is why the
divergence is invisible in ordinary play and was not noticed.

**Also carved out of this function's derive half**, and previously undocumented here: the four
16-byte-block lanes are now declared types (`MapRefImageHeader`, `MapRefFieldRow`,
`MapRefWeatherBlock`, `MapRefWeatherLane` in `_types`), `02099DB0` is written by this function and
read by nothing — and is `0` in all 279 shipped lanes — and `02099DBC` has a second writer,
`0026AB40`, whose whole body is `[02099DBC] = (ecx != 0)`, corroborating the boolean domain the
authored table at header `+0x18` supplies.

`003D99B0` (456 B) is the defaults initializer `00259B30` calls: `0032B600` runs on `rdi+0x2B0`, `dword[+0x190] |= 0x200002` sets the flags, then constants flood in - `+0x64` = `0x3FA66666`, `+0x68` = `0x40000000`, `+0x218` = `0x3F99999A`, `+0x10..+0x2C` from the `01EFE998` float table - the weather record's parameter reset.

Interior anchor `003D99C9` (function `003D99B0`).

`0032B790` (227 B) is the call-free defaults block `0032B600`/`003D99B0`/`003D9B80` run: `+0xC0` = 0x20000000, `+0x100`/`+0x120`/`+0x2EC`/`+0x2FC`/`+0x30C`/`+0x31C`/`+0x33C`/`+0x34C`/`+0x35C` = 1.0f, `+0x11C` = 1.3f, `+0x374` = 1, the rest zeroed - the weather record's field reset.

Interior anchor `0032B79C` (function `0032B790`).

`00379F70` (438 B) is the globals-record initializer `00266D10`/`00379D00` call: `1.0f` defaults flood `02EBF460`..`02EBF50C` while `movdqu` zero/alternating fills cover `02EBF420`..`02EBF4B0`, `byte` flags clear, and `00861EC0` zeroes the `02ADD8E0` block - the bootstrap's shared-state reset.

Interior anchor `0037A0EA` (function `00379F70`).

`0032B600` (388 B) is the element reset `003D99B0` runs on `rdi + 0x2B0`: `[rcx + 0x20]`/`[+0x28]` zero, `+0x2C` = 1.0f, `+0x3C` = 0x3EF74BC7, `00861F02` computes a value negated into `+0x34`, `00861F14` square-roots for the next field, `0032CE40`/`0032B790`/`00861F02` finish - the weather record's per-element initializer (pre-named by the batch-121 crossing row).

Interior anchor `0032B63F` (function `0032B600`).

`003DC8D0` (303 B) is the keyed insert `003DC5B0`/`003DCD00` call on `02B580B0` (0xC stride to `02B58170`): the `(ecx, dx, r8b)` triple scans for a live slot; a miss claims `02B58174`'s index, stores the key + `-1` + `003DCA30`'s byte, and a non-negative `rsp+0x70` index runs `0032E400` into `dword[+4]` - the world-state bank's memo slot the initialiser primes.

Interior anchor `003DC95F` (function `003DC8D0`).

`003DCBC0` (300 B) is the `02B57F70` bank init `00266D10` calls: sixteen 0x14-stride records take `(i&0xF)` slot tags with `dword[+8] = i|0x10`, zeroed links and `byte[+0x13]=i`; `02B580BA`..`02B5817A` at 0xC stride fill `0xFF`, `02B58174`=0 / `02B58170`=1 / `02B58178`/`+0x80`/`+0x88` clear, then `0032E400(9,5)` drives the issue loop - the deque-family list build the accessor table names.

Interior anchor `003DCC59` (function `003DCBC0`).

## Interior citations for the entry-cited functions (FABLE, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's disassembly pack and re-read by FABLE against the certified image; verified by [`interior_applier.py`](../../_index/candidates/fable-weather-apply-and-environment-materializ-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `001AA3B0` | 30 B | calls `00265920` with the incoming registers and tail-jumps to `001A7E40(rcx, result - 1)`, with the incoming `rcx` kept across the call | `001AA3B9`, `001AA3C1`, `001AA3C9` |
| `001DC000` | 61 B | calls `00210B30` with the incoming registers and tail-jumps to `00210F60` with its result in `rcx`, the incoming `rcx` in `rdx`, the incoming `rdx` in `r8` and the incoming `xmm2` in `xmm3` | `001DC018`, `001DC020`, `001DC023`, `001DC026`, `001DC038` |
| `00210ED0` | 135 B | calls `0016D6A0` with `ecx` = 1 when `xmm1` lies between 0 and 1.0 (`01CEBBA8`) inclusive (0 otherwise, including NaN) and the incoming `rdx` untouched; then builds a local object at `rsp + 0x78` with `007A4380`, calls `007A4C70(obj, r8d)` and `007A45C0(obj, xmm1, 0.0, 0)`, and finishes with `001243B0(obj)`; the incoming `rcx` is not used | `00210F02`, `00210F0D`, `00210F24`, `00210F37`, `00210F42` |
| `002EFA20` | 80 B | stores 3 to byte `022BDD5D` and 0 to byte `022BDD5C`, zeroes the dwords `022BDD60`, `022BDD90`, `022BDDC0`, `022BDDF0`, `022BDE20`, `022BDE50`, `022BDE80` (stride 0x30), `022BDEB0` and `022BDEB8`, and stores 6 to dword `022BDEB4` | `002EFA22`, `002EFA29`, `002EFA53`, `002EFA5F`, `002EFA65` |
| `002F1A00` | 23 B | zeroes dword `022BE7C0` and qwords `022BE7C8` and `022BE7D0` | `002F1A02`, `002F1A08`, `002F1A0F` |
| `0036C5A0` | 41 B | when `ecx` is at most 14 (unsigned), stores `rdx` to the qword at `+0xA0` of entry `ecx` of the 0xA8-byte-stride table at `022D7FD0`; otherwise stores `rdx` to the qword at address `0xA0` (a null base) | `0036C5A3`, `0036C5A8`, `0036C5B6`, `0036C5C1` |
| `003777A0` | 15 B | tail-jumps to `003777C0` with `r8d` = 3 and `r9d` = 4, passing `rcx` and `rdx` through | `003777A6`, `003777AA` |
| `003777B0` | 15 B | tail-jumps to `003777C0` with `r8d` = 7 and `r9d` = 2, passing `rcx` and `rdx` through | `003777B6`, `003777BA` |
| `003DA2C0` | 16 B | zeroes `xmm3`, `xmm2`, `edx` and `xmm0` and tail-jumps to `002564D0`, passing `rcx` through | `003DA2C3`, `003DA2C6`, `003DA2C8`, `003DA2CB` |
| `003DD7E0` | 97 B | zeroes qwords `02B58A60` and `02B58A68` and dword `02B58A70`, then walks 5 x 16 records of 0x1C bytes addressed from `02B581AD`, storing for each the inner index (0 to 15) to word `+1`, 0 to qword `-0xD` and to byte `+0`, and the outer index (0 to 4) to byte `-1` (offsets relative to that pointer) | `003DD7ED`, `003DD820`, `003DD826`, `003DD82D`, `003DD83B` |
| `003DF030` | 98 B | walks 5 x 8 records of 0x38 bytes from `02B59360` (record 8 x outer + inner), storing the inner index (0 to 7) to byte `+0x12` and the outer index (0 to 4) to byte `+0x11` and zeroing dword `+0`, qwords `+8`, `+0x18` and `+0x20`, byte `+0x10` and word `+0x28`; its fallback to a null record for an inner index above 7 cannot be reached within the loop bound | `003DF04F`, `003DF05B`, `003DF076`, `003DF07F`, `003DF08B` |
| `003EBE40` | 45 B | zeroes the six qwords `02B5EC60`, `02B5EC68`, `02B5EC70`, `02B5EC78`, `02B5EC80` and `02B5EC88` | `003EBE42`, `003EBE49`, `003EBE50`, `003EBE5E`, `003EBE65` |
| `0050CDE0` | 91 B | calls `00267E10(r9)` twice, keeping the first result as `a` and the second as `b`, then calls `0016D6A0(b, 00264F10(a))` and `0016D6A0(b, 00264F40(a))` and tail-jumps to `0016D6A0(b, 00264F90(a))` | `0050CDF0`, `0050CDFA`, `0050CE0C`, `0050CE1C`, `0050CE36` |
