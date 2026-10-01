# V121 GN — WEATHER RUNTIME VS FIELD-INIT RESOURCE SPLIT — 2026-08-31

**Status:** READ_ONLY_ANALYSIS_ONLY / NOT_APPLIED / NOT_PERSISTENCE_CERTIFIED  
**Project:** For Xeavin — FFXII_TZA GFZ/GZF V121 full-executable reconstruction  
**Secondary use:** XIIOnline weather/environment native-seam research  
**Intended physical parent:** GM160 recovery-transfer GZF contained in the uploaded handoff ZIP  
**Authorized EXE SHA-256:** `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`

## 0. Accounting

No GZF mutation is claimed.

Persistence-certified GM160 remains:

- functions: **38,161**
- explicit: **38,001**
- unresolved: **160**
- coverage: **99.58072%**
- overlap: **0**

This document narrows the upstream context of unresolved:

`002F7380` — `Presentation.LegacyPS2GS.TextureMipLocalMemoryBudgetAndReferenceSlotTableRebuild`

It does not change that proposed CodeDomain name.

---

# 1. Correction to the earlier weather→Movement wording

Earlier GN weather analysis proved that the committed Weather Slot is passed into Movement resource reconfiguration during field initialization.

A complete direct-call census now shows:

## `00379290`

- complete body: **53 bytes**
- SHA-256:
  `3ffc81922688323d8b9ed02b655d844aab271c985fa78c30743128c4dac4eba6`
- canonical V120 PrimaryOwner: **WorldAreaField**

has exactly **one direct caller** in the executable:

`002620E0 -> 00379290`

No authored runtime `setweatherslot` path calls it.

Therefore the correct statement is:

**Weather Slot is a proven selector/input to the Movement/LegacyPS2GS resource-bank configuration during field initialization/reconfiguration.**

It is not proven that every runtime Weather Slot change immediately re-runs that resource-bank transition.

---

# 2. Field-initialization Weather Slot path

## `002620E0`

- complete body: **231 bytes**
- SHA-256:
  `7605a77072bf9d04cf0330b8b662aa627d791dfa16dde5dd68f6d304127f182f`

Exact observed weather sequence:

1. call `0025ACA0`
   - native EBP `weatherProbability` retention/transition roll;
   - chosen slot is applied through `0026D910`;

2. query committed Weather Slot through `00265920`;

3. publish the slot through general resource/notification channel 0;

4. publish the slot through general resource/notification channel `0x1F`;

5. query slot again;

6. call `00379860(weatherSlot)`;

7. call `00379290()`;

8. continue normal field initialization.

Thus field initialization deliberately fans out the committed Weather Slot into multiple downstream systems.

---

# 3. `00379290` is specifically the WorldAreaField→Movement field-resource bridge

Exact body:

```text
if (02ADD090 != null):
    02ADD0E9 = 1
    weatherSlot = 00265920()
    tail 0026E8D0(weatherSlot)
else:
    02ADD0E9 = 0
    tail 00379630()
```

When the relevant area/field resource runtime exists:

**current Weather Slot**
→ `0026E8D0(weatherSlot)`

When it does not exist:

the function enters the alternate field/resource reconstruction path `00379630`.

Canonical V120 evidence independently places:
- `00379290` on the WorldAreaField side;
- `0026E8D0` on the Movement side.

Therefore this is a genuine cross-category transition rather than ownership inheritance.

---

# 4. Alternate field/resource rebuild also uses the current Weather Slot

## `00379630`

The alternate field/resource rebuild path:

1. destroys/releases existing related resource handles;
2. queries current Weather Slot through `00265920`;
3. calls Movement reconfiguration `0026E8D0(weatherSlot)`;
4. rebuilds associated graphics/resource records;
5. materializes additional field-dependent resource objects.

So both branches of the field-resource initialization/rebuild family ultimately feed the committed Weather Slot into Movement resource configuration.

Again, this occurs inside the **field resource lifecycle**, not as an unconditional side effect of every Weather Slot update.

---

# 5. Runtime authored `setweatherslot` path is different

Authored script call:

`0x021A setweatherslot(int)`

maps to ScriptVM handler:

`003565C0`

Exact runtime transaction:

1. pop requested slot;
2. validate current field/map context;
3. clamp to 1..3;
4. call `0026D910(weatherSlot)`;
5. call `0026D8F0()`;
6. return.

There is no direct call from this handler to:
- `00379290`;
- `00379630`;
- `0026E8D0`;
- `0026E290`;
- `002F7380`.

Therefore a scripted runtime Weather Slot change does **not** directly force the Movement/LegacyPS2GS resource-bank rebuild.

---

# 6. What runtime `setweatherslot` does update immediately

Lower native apply owner:

## `0026D910`

- WorldAreaField owner;
- commits/preserves Weather Slot;
- selects one of three authored MapRef/environment records;
- republishes field runtime parameters;
- clears the one-shot preserve latch;
- reaches `002E3D40`;
- zero-mode `002E3D40` queries current Weather Slot and derives WorldAreaField parameters;
- tail-enters canonical Presentation owner `0040AAD0`.

Thus runtime `setweatherslot` provides immediate:

**WorldAreaField state**
→ **authored MapRef/environment parameter refresh**
→ **Presentation backend refresh**

without immediately rebuilding the separate Movement weather-indexed resource family.

That split is native behavior and should be preserved rather than “fixed” by multiplayer code.

---

# 7. Implication for `002F7380`

The correct context is now:

## Field initialization / field-resource rebuild

committed Weather Slot  
→ WorldAreaField field-resource initialization  
→ Movement weather/resource bank selection  
→ Movement dirty state  
→ `0026E290`  
→ `002F7380`  
→ LegacyPS2GS texture-mip local-memory slot-table rebuild.

## Runtime scripted Weather Slot update

`setweatherslot` authored intent  
→ lower native `0026D910`  
→ WorldAreaField/MapRef environment materialization  
→ Presentation backend refresh  
→ arm one-shot weather-preserve latch  
→ return.

No immediate `002F7380` transition is proven on this path.

Therefore:

**Weather Slot is one proven field-resource selection input to `002F7380`'s upstream resource family, not `002F7380`'s general runtime trigger.**

This further protects the unresolved GN row from being overnamed as Weather-specific.

---

# 8. XIIOnline consequence

This changes the receiver strategy in an important way.

## For an authoritative runtime Weather Slot change

Receiver should first reproduce the native WorldAreaField weather apply semantics through the best proven non-VM apply transition.

Do **not** automatically append:
- Movement resource reconfiguration;
- Movement dirty dispatch;
- `002F7380`.

Why:

the original game does not perform those calls directly in authored runtime `setweatherslot`.

Forcing them would make XIIOnline less native-coherent than single-player FFXII.

## For field load / re-entry / late join

The receiver's normal field initialization should use the authoritative committed Weather Slot before the field-resource initialization transaction reaches its weather-dependent branches.

Then native field initialization can naturally publish:

Weather Slot
→ field/environment systems
→ Movement weather-indexed resource bank
→ Presentation/LegacyPS2GS derived tables.

This is the preferred late-join architecture.

---

# 9. Persistent-world ordering

For a late join or field re-entry:

1. authoritative map/area identity known;
2. authoritative committed Weather Slot known;
3. local persistent/current Weather Slot is reconciled through native WorldAreaField application;
4. local field-resource initialization runs;
5. native Movement resource family binds the current Weather Slot;
6. native Presentation/LegacyPS2GS tables rebuild locally;
7. only then treat weather-dependent spawn eligibility as settled.

For an already-loaded client receiving a runtime weather change:

1. authoritative Weather Slot revision arrives;
2. apply native runtime Weather Slot state;
3. allow native WorldAreaField/Presentation consequences;
4. do not manufacture a field-resource rebuild unless the engine itself transitions into one.

---

# 10. Why this matters for mod compatibility

A mod may distinguish:

- runtime environmental changes that reuse already-loaded field resources;
- resource-bank changes that happen only when entering/rebuilding a field.

Blindly forcing the Movement/GS resource-bank transition after every networked weather change could violate that design.

Preserving the native split gives better compatibility:

**runtime weather semantics remain runtime weather semantics; field initialization remains field-resource initialization.**

---

# 11. Current GN result remains unchanged

Strong unresolved GN proposals:

1. `00313A00`  
   `InputGameplay.FieldBattleCapabilityAndUIRequestInhibitMaskReconciliation`

2. `002F7380`  
   `Presentation.LegacyPS2GS.TextureMipLocalMemoryBudgetAndReferenceSlotTableRebuild`

Applied rows: **0**

Certified GM160 ledger remains:

- **38,001 explicit**
- **160 unresolved**
- **99.58072%**
- **overlap 0**

