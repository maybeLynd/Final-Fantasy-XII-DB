---
system: Weather and terrain element scaling
category: 08-Combat-Formula
status: AUDITED
owner_layer: PrimaryOwner:CombatFormula
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

# Weather and terrain element scaling

> Why your Fire spells are weak in the rain, why Thunder hits harder in water, and why
> "Heavy Rain" behaves like Rain and Wind at the same time — because that is literally how
> it is built.

## 1. What the player sees

Weather and the ground you are standing on change elemental damage. Rain weakens Fire and
strengthens Lightning. Sandstorms boost Earth. Snow boosts Ice. Standing in water boosts
Lightning and Water but halves Earth. Strong wind boosts Fire and Wind and halves Water.

Crucially, **these stack multiplicatively** — the game has no separate hardcoded rule for
"Heavy Rain". It is Rain × strong wind, and the numbers fall out on their own.

An Agate Ring (Weatherproof / *Ignore Weather & Terrain*) turns the whole stage off.

## 2. Native mechanism

`0038B220` is a **pre-affinity** environmental element-scaling stage: it runs before the
separate resistance/weakness/absorb affinity stage (`0038B6A0`), and both read the same
action element mask at `ActionDefinition+0x13`. It operates on the canonical formula scratch
scale `g_fFormulaScratchScale` at `02AEE054`.

Three ~~independent~~ inputs, applied in sequence ~~and multiplied together~~ — but not as independent factors: Lightning, Ice, Earth and Water each take one ×1.2 when the environment class **or** the terrain class matches, so Lightning in rain on water terrain is ×1.2, not ×1.44; only rules on different elements, or a ×0.5 against a ×1.2, compose *(corrected 2026-10-02, OPUS: checked at `0038B3E1`–`0038B424`, one `mulss` for either test, and the same shape at `0038B46D`, `0038B4F3` and `0038B579`; CONTRACT-environmental-element-scaling.md, the 2026-09-25 rule table)*:

**Global environment class** — `02099DA8`, getter `00263E10`, derived by `0026D910` from
authored field/environment data.

**MWeather gameplay class** — `02099DAC`, getter `00263E20`. Derived by collapsing the
MWeather 3-bit preset: preset `0` → class 0, presets `1..3` → class 1, presets `≥4` → class 2.

**Target-local terrain class** — resolved per target through `003210E0` → `00263DD0`, which
walks from the target's live runtime state into its current field/navigation record, reads the
target-local authored environment index, and resolves it through the field environment table.

### Early-out

The whole stage is skipped when **bit index 16** is present on either combatant:

```
0038B220  TEST byte ptr [RDX+6A],01   ; target BKBI +0x68 layer, bit 16   <- corrected 2026-10-02, OPUS: the TEST is at 0038B226 (0038B220 is push rdi, 0038B222 sub rsp, 0x30)
0038B222  JNE  skip   <- corrected 2026-10-02, OPUS: the JNE is at 0038B22D; the next two tests are 0038B233 and 0038B23D
          TEST byte ptr [RDX+7A],01   ; target BKBI +0x78 layer, bit 16
          JNE  skip
          TEST byte ptr [R8+1C],01    ; caster merged context +0x1A, bit 16
          JNE  skip
```

In the derived augment namespace, bit 16 is **Weatherproof**. See
[`../../10-Status-Periodic-Terminal/Status-And-Augment-Layers/`](../../10-Status-Periodic-Terminal/Status-And-Augment-Layers/)
for why the same bit position also aliases the status *Disease*.

## 3. Key addresses

| Address | Working name | Body | Role |
|---|---|---:|---|
| `0038B220` | `BattleFormula_ApplyWeatherTerrainElementScalingUnlessWeatherproof` | 1,138 B | the stage |
| `0038B6A0` | `BattleFormula_ApplyActionElementAffinity` | 686 B | separate later affinity stage |
| `00263E10` | `WorldField_GetGlobalEnvironmentClass` | 7 B | reads `02099DA8` |
| `00263E20` | `WorldField_GetMWeatherGameplayClass` | 7 B | reads `02099DAC` |
| `00263DD0` | `WorldField_ResolveTargetLocalTerrainClass` | 53 B | per-target terrain |
| `003210E0` | *(thunk)* | — | → `00263DD0` |
| `00321490` / `003214A0` | *(thunks)* | — | → `00263E10` / `00263E20` |

## 4. Data structures

```
Action element mask   ActionDefinition +0x13
  0x01 Fire   0x02 Lightning   0x04 Ice   0x08 Earth   0x10 Water   0x20 Wind

Globals
  02099DA8  global environment class   0..3   <- corrected 2026-10-02, OPUS: the domain is 0..4; the stage has arms for 0..3 only and class 4 matches none (0038B2A8, 0038B3F4, 0038B4FE, 0038B478, 0038B584; the OPUS 2026-09-21 section below)
  02099DAC  MWeather gameplay class    0..2
  02AEE054  g_fFormulaScratchScale
```

### Global environment class matrix (`02099DA8`)

| Class | Effect | Familiar name |
|---:|---|---|
| 0 | Fire ×0.5, Lightning ×1.2 | Rain |
| 1 | Earth ×1.2 | Sand base |
| 2 | Ice ×1.2 | Snow/Ice base |
| 3 | Water ×1.2 | Fog |

### MWeather gameplay class (`02099DAC`)

| Class | Effect |
|---:|---|
| 0, 1 | no element modifier at this stage |
| 2 | Fire ×1.2, Water ×0.5, Wind ×1.2 — **strong wind** |

### Target-local terrain class

| Class | Effect | Familiar name |
|---:|---|---|
| 0 | Lightning ×1.2, Water ×1.2, Earth ×0.5 | Water terrain |
| 1 | Earth ×1.2 | Sand terrain |
| 2 | Ice ×1.2 | Snow/Ice terrain |

Note the binary does **not** halve Fire merely because the target stands in water terrain.

### Composition — how named weather emerges

| Condition | Composition | Net |
|---|---|---|
| Rain | class 0 | Fire ×0.5, Lightning ×1.2 |
| Heavy Rain | class 0 × strong wind | Fire ×0.6, Lightning ×1.2, Water ×0.5, Wind ×1.2 |
| Snowstorm | class 2 × strong wind | Fire ×1.2, Ice ×1.2, Water ×0.5, Wind ×1.2 |
| Sandstorm | class 1 × strong wind | Fire ×1.2, Earth ×1.2, Water ×0.5, Wind ×1.2 |
| Fog | class 3 | Water ×1.2 |

Fire ×0.6 in Heavy Rain is `0.5 × 1.2`. **No weather or formula code loads a 0.6 constant** —
see the re-verification section for the scan that establishes this.

## 5. Call chain

```
Weather Slot committed  (0026D910)
  -> MWeather 3-bit preset extracted
     -> collapsed to gameplay class -> 02099DAC
  -> authored field/environment data
     -> global environment class    -> 02099DA8

action resolution
  -> BattleFormula_BuildEvaluationContext (003847C0)   merges status+augment layers
  -> BattleFormula_ResolveTargetResult (00385F60)
     -> recipe calculator list
        -> 0038B220   THIS STAGE (pre-affinity)
           -> 00263E10 / 00263E20 / 003210E0->00263DD0
           -> scales g_fFormulaScratchScale
        -> 0038B6A0   element affinity (separate, later)
```

**Upstream:** the committed Weather Slot and the target's field/navigation record.
**Downstream:** the scratch scale consumed by the rest of the formula chain.
**Do not confuse with:** `0038B6A0` element affinity (target resistance/weakness/absorb) —
a different stage with different inputs.

## 6. Modding notes

- **To change weather combat effects:** the multipliers are ~~literal float constants inside~~
  ~~`0038B220`~~ float constants in `.rdata` that `0038B220` loads — ×0.5 from `01CEBB70` (`0038B299`) and ×1.2 from `008FCC90` (`0038B3E5`) *(corrected 2026-10-02, OPUS: checked at those addresses; CONTRACT-environmental-element-scaling.md, the rule table)*. The *classes* come from authored data — MWeather and the field environment
  table — so changing which weather maps to which class is a data edit, not a code edit.
- **Regenerates itself:** `02099DA8` / `02099DAC` are derived by the weather apply. Do not
  write them directly; apply the Weather Slot and let them fall out.
- **XIIOnline:** do **not** network these multipliers, the scratch scale, or the class
  globals. Network the authoritative Weather Slot and area identity; let each client's native
  code derive the classes. Combat outcomes should be authoritative — a client whose weather
  state is stale will predict different damage.
- **Mod compatibility:** a mod changing MWeather or field environment data changes gameplay,
  not just visuals. Two clients running different weather data can disagree on damage even
  with the same Weather Slot. Version-fence gameplay-affecting weather data if previews must
  match.

## 7. What is not known

- [x] ~~Whether the status/augment bit-16 alias (Disease vs Weatherproof) is intentional
      (open question **E-1**).~~ **Closed 2026-09-12 as intent residue** on [the namespaces README](../Status-And-Augment-Namespaces/README.md): the consequence is proven — a diseased caster's merged bit 16 turns this stage off at its caster test — and a live check is queued.

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| Stage identity and all multipliers | complete body of `0038B220` (1,138 B, `a0e03037…0b505`) | 1 |
| Early-out is bit **16** on all three tests | exact disassembly at `0038B226` / `0038B233` / `0038B23D` — `+0x6A`, `+0x7A`, `+0x1C` are byte +2 of the `+0x68`, `+0x78`, `+0x1A` bitmaps, bit 0 → index 16 | 1 |
| Bit 16 = Weatherproof in the augment namespace | Xeavin public Workshop `Helpers/EnumHelper.cs`: `Weatherproof = 0x0000000000010000` | 6 |
| Pre-affinity ordering | same `ActionDefinition+0x13` element byte consumed independently by `0038B6A0` | 1 |
| MWeather preset → gameplay class collapse | complete body of `0026D910`; store to `02099DAC`; getter `00263E20` (7 B, `fcf60863…994a`) | 1 |
| Familiar weather names | external FFXII mechanics documentation agrees with the already-exact native matrix | 10 |

**Superseded readings:**
- *Old:* early-out involves "target status ID 17 and caster status ID 16."
  *New:* all three tests are bit index **16**; the ID-17 reading was an off-by-one and is
  withdrawn.

## 9. Related

- [`../Recipe-System/ranged-weapon-recipes.md`](../Recipe-System/ranged-weapon-recipes.md) — a *different* weather gate (accuracy, bit 2)
- [`../../10-Status-Periodic-Terminal/Status-And-Augment-Layers/two-layer-effect-model.md`](../../10-Status-Periodic-Terminal/Status-And-Augment-Layers/two-layer-effect-model.md)
- [`../../03-World-Area-Field/Weather/`](../../03-World-Area-Field/Weather/)

## Re-verification 2026-09-02 (AH-8)

Stamped against parent `381d2aea...`; re-checked against the current `2ed8affb...`.

**Addresses:** 15 cited - 11 function entries, 4 interior - 0 unresolved.

### The composition claim, falsification-tested

The document's sharpest assertion is that severe weather **composes** rather than being authored per
combination: Heavy Rain's Fire multiplier of `0.6` is `0.5` (Rain) x `1.2` (strong wind), not a
value anyone wrote down.

That is falsifiable: **if a `0.6f` constant is loaded anywhere in the weather or formula path, the
claim is wrong.** The binary was scanned for the IEEE-754 encodings.

```
0.5f = 00 00 00 3f    6782 occurrences   (ubiquitous, as expected)
1.2f = 9a 99 99 3f       6 occurrences   (rare - a specific scaling constant)
0.6f = 9a 99 19 3f      28 occurrences
```

`0.6f` **does exist in the binary** - so the document's phrasing *"nobody wrote 0.6 anywhere"* was too
strong, and has been corrected above.

But every site that *loads* one was located. There are **eight** `MOVSS` loads of a `0.6f` constant:

| Site | Function | Owner |
|---|---|---|
| `0x001DC4CB` | `FUN_001dc4c0` | - |
| `0x001EDA8B` | `FUN_001ed240` | - |
| `0x00336BDD` | `FUN_00336ae0` | **Movement** |
| `0x003D8DBB` | `FUN_003d8da0` | - |
| `0x00470C1F` | `FUN_00470b70` | **Presentation** |
| `0x006F46DB`, `0x006F705C`, `0x006F74EE` | Phyre-range functions | - |

**Not one is in CombatFormula, and not one is the weather scaler.** The `0.6` values in this binary
belong to movement, presentation and middleware.

**The substance of the claim holds:** no weather or formula code loads a `0.6`, so Heavy Rain's Fire
multiplier cannot be authored - it must be produced by composing `0.5 x 1.2`. The wording was
imprecise; the mechanism was right.

That `1.2f` appears only **6 times** in the whole executable is corroborating: it is a rare, specific
constant, exactly as a single strong-wind multiplier should be.

**Stamp advanced because the claim was re-derived**, per the evidence standard.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Save_Load_Settings — SERVICE.** `0026D910` on this page calls `SaveImage_GetPersistentPayloadBase`, owned by that layer. What it reaches is a 20-byte accessor returning `002EF640() + 0x200` - **the base the persistent flag banks are indexed off**, so those banks live inside the save payload; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page.*

**CombatAction — CLIENT (3 edges).** `Battle_ProcessActionTarget` `00307300`, `BattleAction_ResolveSpecialSequenceTargets` `0030EC00` and `BattleUnit_HandleActorTimelineEvent` `00319F50` call the interpreter `BattleFormula_ResolveTargetResult` `00385F60`. Every action target's result is resolved through the interpreter that runs this page's scaling step, so the action layer is how the weather and terrain multipliers reach a hit.

**Movement — OUT-OF-SCOPE (2 edges).** `00336AE0` calls `00380C40` and is called by `00336E40`. This page cites `00336AE0` only as one of the eight `0.6f` load sites in the falsification table; its movement edges have nothing to do with element scaling.

**Presentation — OUT-OF-SCOPE (4 edges).** `001DC4C0` is called by `00193AD0`; `001ED240` calls `001EC560` and is called by `00418880`; `00470B70` calls `00428CD0`. These three are cited only as `0.6f` load sites that prove the constant is not in the weather or formula path; their presentation edges are outside this page's claim.

**Script_VM_Native_Bridge — CLIENT (1 edge).** The `setweatherslot` verb body `003565C0` calls `WorldField_InitializeCurrentFieldRuntimeParameters` `0026D910`. A script that sets the weather slot re-runs the field-parameter initialisation that publishes the environment class this scaler reads.

**Status_Periodic_Terminal — CLIENT (1 edge).** The periodic tick `BattleUnit_RunPeriodicCombatMaintenance` `00310DB0` calls `00385F60`. A periodic result is resolved through the same interpreter as an action's, which is how a tick's result can meet the scaling step.

## The `003210E0`/`00321490`/`003214A0` exclusive-subtree triple — all 3 roots bound (SWE2-FRONTIER, followup queue)

`003210E0` (9 B) — `rcx = qword[rcx+0x10]` then `jmp 00263DD0`
(`003210E0`/`003210E4`).

| member | role | interior |
| --- | --- | --- |
| `00263DD0` | null-gated `qword[+0xC0]` deref walk (`00263DD2`/`00263DD7`) | [`00263DD2`](../../_index/ADDRESS-INDEX.md) |

`00321490`/`003214A0` (5 B each) — plain `jmp` thunks.

| root | member (target) | interior |
| --- | --- | --- |
| `00321490` | `00263E10` — `dword[02099DA8]` getter | [`00263E10`](../../_index/ADDRESS-INDEX.md) |
| `003214A0` | `00263E20` — `dword[02099DAC]` getter | [`00263E20`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none.

## The environment-class domain is 0..4, and this page's matrix lists the arms, not the domain (OPUS, 2026-09-21)

Filed as `CON-146` while assembling [`CONTRACT-weather.md`](../../03-World-Area-Field/CONTRACT-weather.md).

This page's layout block types `02099DA8` as `0..3` and its matrix has four rows. **The stage's arms
are four; the authored domain is five.** `0038B220` tests the getter's result only for equality —
`test eax, eax` at `0038B2A8` and `0038B3F4`, `cmp eax, 2` at `0038B478`, `cmp eax, 1` at
`0038B4FE`, `cmp eax, 3` at `0038B584` — with **no default arm**, and the authored table this global
is published from (`map_ref.bin` header `+0x10`, 16 entries `{4,4,4,0,0,1,2,2,3,0,…}`) supplies the
value **4** for **246 of the 279 shipped weather lanes**. So the matrix is correct about what each
of its four classes does and incomplete as a statement of the domain: **the common case is `4`,
which matches no arm and therefore applies no environmental element scaling at all.**

Nothing about the four listed matrices changes. What changes is that a reimplementation typing this
global `0..3` has no representation for the state most of the game is in, and would have to fold it
onto class 0 — turning "no weather effect" into `Fire x0.5, Lightning x1.2` across most areas.
