# V121 GN — WEATHER/TERRAIN AUGMENT NAMESPACE CORRECTION — 2026-09-01

**Status:** READ_ONLY_ANALYSIS_ONLY / NOT_APPLIED / NOT_PERSISTENCE_CERTIFIED  
**Project:** For Xeavin — FFXII_TZA GFZ/GZF V121 full-executable reconstruction  
**Secondary use:** XIIOnline Weather/Terrain + CombatFormula + equipment/passive authority research  
**Intended physical parent:** GM160 recovery-transfer GZF contained in the uploaded handoff ZIP  
**Authorized EXE SHA-256:** `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`

## 0. Supersession / accounting

This document supersedes earlier interpretations that treated all bits in the BattleStats `+0x68/+0x78` family as one undifferentiated status-ID namespace.

In particular it supersedes the stale statement in:

`V121_GN_BOW_CROSSBOW_RECIPE_AND_WEATHER_FORMULA_CLOSURE_2026-09-01.md`

that described the `0038B220` Weather/Terrain bypass as involving:
- target status ID 17;
- caster status ID 16.

Fresh exact disassembly proves all three `0038B220` early-out tests are **bit index 16**, and public Xeavin source closes the second semantic namespace carried by that bit.

This is read-only research only.

Official GM160 remains:

- functions: **38,161**
- explicit: **38,001**
- unresolved: **160**
- coverage: **99.58072%**
- overlap: **0**

No GFZ mutation is claimed.

---

# 1. Exact `0038B220` Weather/Terrain early-out

Canonical CombatFormula function:

## `0038B220`

- body: **1,138 bytes**
- exact SHA-256:
  `a0e03037826d41312c3f686a94884a735d59874795a524ffe9a005668800b505`

Exact entry:

```text
0038B220  PUSH RDI
0038B222  SUB  RSP,30
0038B226  TEST byte ptr [RDX+6A],01
0038B22A  MOV  RDI,RDX
0038B22D  JNE  0038B68C

0038B233  TEST byte ptr [RDX+7A],01
0038B237  JNE  0038B68C

0038B23D  TEST byte ptr [R8+1C],01
0038B242  JNE  0038B68C
```

Canonical calculator ABI:

- `RCX` = caster BKBI
- `RDX` = target BKBI
- `R8`  = FormulaEvaluationContext*

Therefore the early-out tests are:

1. target BKBI mutable layer `+0x68`, byte +2, bit 0  
   = bit index **16**;

2. target BKBI derived/auto layer `+0x78`, byte +2, bit 0  
   = bit index **16**;

3. caster merged evaluation bitmap beginning `context+0x1A`, byte +2, bit 0  
   = bit index **16**.

The earlier target-ID-17 interpretation was an off-by-one semantic mistake and is withdrawn.

---

# 2. Exact two-layer mutation architecture

Canonical:

## `0030E130`
`BattleStats_ModifyStatusLayerStateAndProcessSideEffects`

- body: **553 bytes**
- SHA-256:
  `f985df17d3dcbfd7862a9eb6bf4333becc39c9c8861203b582ec6ff5447faf95`

Given numeric bit/effect ID `n`, it addresses:

```text
byteIndex = n >> 3
bit       = 1 << (n & 7)
```

and can mutate either:

### layer at BKBI `+0x68`
ordinary/mutable status-effect layer

or:

### layer at BKBI `+0x78`
derived/automatic effect/augment layer.

The two layers deliberately share the same numeric bit positions but do not necessarily share the same semantic name namespace.

---

# 3. Public Xeavin source closes both namespaces

Xeavin's public:

`The-Insurgents-Workshop/Helpers/EnumHelper.cs`

defines two separate enums.

## 3.1 Augment namespace

Relevant exact values:

```text
AccuracyBoost = 0x0000000000000004
Weatherproof  = 0x0000000000010000
Thievery      = 0x0000000000020000
```

Therefore:

- augment bit/index **2**  = **AccuracyBoost**
- augment bit/index **16** = **Weatherproof**
- augment bit/index **17** = **Thievery**

The independent Forge post identifying Thievery as raw augment ID 17 agrees exactly with this enum ordering.

## 3.2 Status-effect namespace

The same source separately defines:

```text
Petrify = 0x00000004
Disease = 0x00010000
Lure    = 0x00020000
```

Therefore:

- status bit/index **2**  = **Petrify**
- status bit/index **16** = **Disease**
- status bit/index **17** = **Lure**

These are separate enum namespaces that happen to occupy matching bit positions.

Do not identify a bit solely from its numeric index without knowing which layer supplied it.

---

# 4. Public Xeavin source proves equipment stores a raw Augment field

Xeavin's public:

`Formats/Battlepack/EquipmentAndAttributes.cs`

parses helm/armor/accessory equipment records and exposes the byte directly as:

```text
[JsonPropertyName("Augment")]
public byte Augment { get; set; }
```

The reader:

```text
data.Augment = br.ReadByte();
```

and writer:

```text
bw.Write(equip.Augment);
```

preserve the raw numeric augment identifier.

This directly corroborates the native `0030FED0` equipment path, which reads the corresponding equipment-definition byte and converts that numeric value into a bit in the derived/automatic layer.

---

# 5. Public Workshop intentionally keeps the Augment definition table numeric

Xeavin's public:

`Formats/Battlepack/Augments.cs`

loads the augment-definition section as entries:

```text
Entries.Add($"Augment {i}", entry);
```

with each entry carrying numeric fields such as:
- Equipment Description
- License Description
- Parameter
- Timer Link

Thus the parser intentionally does not provide a second friendly-name enum inside `Augments.cs`.

The friendly identifier bridge instead exists in `Helpers/EnumHelper.cs` for the common augment bitfield.

For the IDs relevant here, that source is sufficient:
- 2 = AccuracyBoost
- 16 = Weatherproof
- 17 = Thievery.

---

# 6. `0030FED0` reconstructs the derived Augment/auto-effect layer

Canonical:

## `0030FED0`
`BattleStats_RecomputeDerivedStateAndAutoStatuses`

- body: **1,787 bytes / 0x6FB**
- exact SHA-256:
  `01a49b9744154d628b7fc654eddadf42efec96702992fe8fc14cfe8d2ff9e853`

Historical V40 semantics already establish this as the broad rebuild of automatic effects from authored unit/equipment/passive state.

The complete body builds a temporary desired 128-bit bitmap and reconciles it against BKBI `+0x78`.

### Equipment source

For equipped records accepted by the native equipment-class gate:
- resolve equipment definition;
- read one raw augment/effect ID from the equipment definition;
- if it is not the sentinel, set that ID's bit in the desired bitmap.

This is the native equivalent of Workshop's equipment `Augment` byte.

### Passive/license/unit-authored source

A second loop traverses authored/passive records and can import up to eight numeric effect/augment IDs from a qualifying record into the same desired bitmap.

### Reconciliation

The desired bitmap is compared against current BKBI `+0x78`.

Missing bits are added through the layer-3/set operation.
Stale bits are removed through the layer-1/clear operation.

Therefore BKBI `+0x78` is a **derived/automatic effect layer that includes authored augments**, not merely a duplicate ordinary-status bank.

---

# 7. FormulaEvaluationContext deliberately merges mutable statuses and derived augments

Canonical:

## `003847C0`
`BattleFormula_BuildEvaluationContext`

- body: **273 bytes**
- SHA-256:
  `a6b21a9e9ae7293dd1eb24d35da97906c385a5ec066899de3d06e3afaa7bb536`

For every numeric bit ID `0..127`, it tests the same bit in:

- caster BKBI `+0x68`
- caster BKBI `+0x78`

and ORs their presence into the evaluation bitmap beginning at:

`FormulaEvaluationContext+0x1A`.

This is a critical architecture rule:

**FormulaEvaluationContext contains a merged effect bitmap, not a namespace-tagged union.**

Once merged, a calculator testing bit `n` cannot distinguish whether the bit came from:
- an ordinary mutable status at index `n`;
- or a derived augment/automatic effect at index `n`.

This explains several previously puzzling gates.

---

# 8. Exact Weather/Terrain bypass identity: augment 16 = Weatherproof

`0038B220` exits before applying any of its:
- global Weather element factors;
- target-local terrain element factors;
- MWeather strong-wind element factors

when bit 16 is present on either combatant through the tested layers/context.

The derived-augment interpretation is now exact:

**augment bit 16 = Weatherproof.**

External FFXII mechanics independently describe this ability as:

**Ignore Weather & Terrain**

and identify it on:
- Entites;
- most frogs;
- Crystal Bugs;
- most Espers;
- player equipment via Agate Ring.

Therefore the strong native semantic is:

**Weatherproof / Ignore Weather & Terrain bypasses `0038B220` environmental element scaling.**

A conservative working calculator description is:

`BattleFormula_ApplyWeatherTerrainElementScalingUnlessWeatherproof`

without changing canonical GFZ metadata outside the normal audit/replay process.

---

# 9. Disease is a same-bit mutable-status alias, not the intended augment identity

Because ordinary status index 16 is:

**Disease**

and `0038B220` directly checks target mutable layer `+0x68` bit 16, the machine code has an observable alias:

**Disease present in the mutable layer also satisfies the same early-out condition.**

Likewise, caster Disease is merged by `BattleFormula_BuildEvaluationContext` into context bit 16 and therefore also satisfies the caster early-out.

This follows directly from the shared-bit merge architecture.

Do not reinterpret the Weatherproof augment as Disease.
Do not reinterpret Disease as an augment.

The correct description is:

- intended derived augment namespace: **Weatherproof**
- same-index mutable status alias: **Disease**
- calculator sees only the merged bit after context construction.

Whether the Disease alias is an intentional design shortcut or an incidental namespace collision is **not proven**.

---

# 10. Severe-weather ranged accuracy uses a different augment: AccuracyBoost

Bow recipe 25 preview calculator:

## `003895D0`

- severe-wind hit-rate scale: **×0.8**
- skips the reduction when merged context bit **2** is set.

Crossbow recipe 26 preview calculator:

## `00389610`

- severe-wind hit-rate scale: **×0.5**
- skips the reduction when merged context bit **2** is set.

Public Xeavin augment enum closes:

**augment bit 2 = AccuracyBoost.**

Xeavin's Forge post independently identifies:

**Accuracy Boost = Cameo Belt augment.**

External FFXII mechanics report:
- Bow accuracy is reduced by 20% in severe weather;
- Crossbow accuracy is reduced by 50%;
- Cameo Belt prevents the weather-caused misses;
- Agate Ring / Weatherproof does **not** remove this ranged-accuracy penalty.

This matches the binary separation exactly:

### Elemental Weather/Terrain effects
bypass augment:
**Weatherproof / bit 16 / Agate Ring**

### Bow/Crossbow severe-weather accuracy
bypass augment:
**AccuracyBoost / bit 2 / Cameo Belt**

This is a clean native separation, not one universal Weather immunity flag.

---

# 11. Petrify is the same-bit mutable-status alias for AccuracyBoost

Public Xeavin status enum closes:

**status index 2 = Petrify.**

Because FormulaEvaluationContext merges:
- caster status layer;
- caster derived augment layer;

context bit 2 can be set by either:
- mutable **Petrify**
- derived **AccuracyBoost**.

Therefore the exact Bow/Crossbow calculator gate is:

**skip severe-weather accuracy reduction when merged effect bit 2 is active.**

The intended augment interpretation is AccuracyBoost/Cameo Belt.

But native Petrify presence shares the same formula bit and therefore also satisfies the condition.

Again:
- do not rename AccuracyBoost as Petrify;
- do not claim the alias is intentional;
- preserve the observable merge behavior.

---

# 12. Corrected native model

The relevant two-layer formula model is:

```text
ordinary mutable status bits       BKBI +0x68
                \
                 OR -> FormulaEvaluationContext merged bitmap
                /
derived augment/auto-effect bits   BKBI +0x78
```

Key overlapping indices:

| Bit | Mutable status namespace | Derived augment namespace | Relevant formula role |
|---:|---|---|---|
| 2 | Petrify | AccuracyBoost | Bow/Crossbow severe-weather accuracy bypass |
| 16 | Disease | Weatherproof | Weather/Terrain elemental-scaling bypass |
| 17 | Lure | Thievery | no weather role established here |

This table is a namespace map, not a claim that the paired names are semantically related.

---

# 13. XIIOnline consequence

This is important for multiplayer state design.

Do **not** network the raw merged formula bitmap as authoritative game state.

Do **not** separately forward:
- BKBI `+0x68`;
- BKBI `+0x78`;
- formula context bits 2/16

as ad-hoc Weather flags.

Instead preserve the native state owners:

## Mutable statuses
Synchronize/realize authoritative status consequences through the native status transaction.

## Equipment/passive augments
Synchronize authoritative:
- equipment;
- character/passive/license state;
- unit authored identity/state

through their proper native owners.

Then allow:

`BattleStats_RecomputeDerivedStateAndAutoStatuses`

to reconstruct the receiver-local derived augment layer naturally.

## Combat
Authority runs the native CombatFormula against coherent:
- Weather Slot/environment state;
- terrain;
- mutable statuses;
- equipment/passive augments.

XIIOnline replicates the authoritative resolved combat outcome rather than each internal formula bit.

This avoids stale/contradictory derived effect layers.

---

# 14. Mod compatibility consequence

This native architecture is unusually friendly to the project's mod-compatibility rule.

A mod can change:
- equipment's raw Augment field;
- passive/unit authored augment sources;
- augment behavior/formula logic;
- Weather/Terrain authored data

and the native derived-state rebuild will still feed CombatFormula coherently.

XIIOnline should therefore prefer:
- shared authoritative logical state/outcomes;
- native local derived-state reconstruction;

over hardcoding vanilla augment assumptions into networking.

For compatibility-sensitive multiplayer sessions, gameplay-affecting equipment/augment/formula data may need version/equivalence fencing so local previews do not silently disagree with authority.

---

# 15. Corrections to prior evidence

## Superseded Bow/Crossbow artifact section 10

Replace the old statement:

> `0038B220` has early bypass conditions involving target status ID 17 and caster status ID 16.

with:

> `0038B220` early-outs on merged/native bit index 16 for both target and caster. In the derived augment namespace, bit 16 is Weatherproof; in the ordinary status namespace the same bit position is Disease.

## Refined Bow/Crossbow weather gate

Earlier statement:

> context bit 2 means native status ID 2.

is incomplete.

Replace with:

> context bit 2 is a merged formula-effect bit. Derived augment bit 2 is AccuracyBoost; mutable status bit 2 is Petrify. The severe-weather ranged-accuracy calculators cannot distinguish the source after context merging.

---

# 16. Evidence hierarchy

## Exact FFXII executable — primary

Proves:
- `0038B220` bit-16 early-outs;
- `003847C0` merged context construction;
- `0030FED0` derived/automatic effect rebuild;
- `0030E130` two-layer mutation mechanics;
- Bow/Crossbow severe-weather bit-2 gates;
- actual Weather/Terrain formula consequences.

## Xeavin public Workshop source — independent structure/name bridge

`Helpers/EnumHelper.cs` proves:
- augment bit 2 = AccuracyBoost
- augment bit 16 = Weatherproof
- augment bit 17 = Thievery
- status bit 2 = Petrify
- status bit 16 = Disease
- status bit 17 = Lure

`EquipmentAndAttributes.cs` proves:
- supported equipment records contain a raw `Augment` field.

`Augments.cs` proves:
- augment-definition records are indexed numerically as `Augment {i}`.

## External FFXII mechanics — semantic corroboration

Independently corroborates:
- Ignore Weather & Terrain behavior;
- Agate Ring provides that elemental Weather/Terrain immunity;
- Cameo Belt/AccuracyBoost protects ranged accuracy;
- Agate Ring does not remove Bow/Crossbow severe-weather accuracy loss.

External mechanics do not override the executable.

---

# 17. GFZ accounting remains unchanged

This closes surrounding semantics and corrects stale evidence.

It does **not** apply a new GM160 unresolved row.

Applied GN rows: **0**

Certified GM160 remains:

- **38,001 explicit**
- **160 unresolved**
- **99.58072%**
- **overlap 0**

Strong current unresolved GN proposals remain:

1. `00313A00`
   `InputGameplay.FieldBattleCapabilityAndUIRequestInhibitMaskReconciliation`

2. `002F7380`
   `Presentation.LegacyPS2GS.TextureMipLocalMemoryBudgetAndReferenceSlotTableRebuild`

