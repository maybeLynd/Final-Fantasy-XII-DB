# V121 GN — WEATHER PROBABILITY + NATIVE APPLY CORRECTION — 2026-08-31

**Status:** READ_ONLY_ANALYSIS_ONLY / NOT_APPLIED / NOT_PERSISTENCE_CERTIFIED  
**Project:** For Xeavin — FFXII_TZA GFZ/GZF V121 full-executable reconstruction  
**Secondary use:** XIIOnline weather/environment native-seam research  
**Supersedes specific wording in:** `V121_GN_READ_ONLY_WEATHER_SLOT_TRIGGER_ADDENDUM_2026-08-31.md`  
**Intended physical GFZ parent:** GM160 recovery-transfer GZF contained in the uploaded handoff ZIP  
**Authorized EXE SHA-256:** `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`

## 0. GFZ accounting remains unchanged

This is a semantic/native-seam correction and expansion only.

No GM160 GZF mutation is claimed.

Persistence-certified GM160 remains:

- functions: **38,161**
- explicit: **38,001**
- unresolved: **160**
- explicit coverage: **99.58072%**
- overlap: **0**

Strong unresolved GN proposals remain:

1. `00313A00` — `InputGameplay.FieldBattleCapabilityAndUIRequestInhibitMaskReconciliation`
2. `002F7380` — `Presentation.LegacyPS2GS.TextureMipLocalMemoryBudgetAndReferenceSlotTableRebuild`

---

# 1. Important correction: Weather probability is EBP/script data, not MapRef data

The earlier weather addendum correctly reconstructed the Weather Slot transition mechanics, but conservatively described `002658B0` as reading an authored MapRef threshold/weight.

That source attribution is now superseded.

## `002658B0`

Canonical V120 PrimaryOwner: **WorldAreaField**

Complete body:
- **112 bytes**
- SHA-256:
  `9689942f64e9a4793c82b8b06bbbff16c8e79081cf60f9d1c80e7a641abec8e7`

Exact native behavior:

1. input Weather Slot 1..3 is converted to zero-based index 0..2;
2. native script/EBP resource state is validated;
3. the loaded script header field at **offset `+0x64`** is read;
4. that offset is resolved to the authored variable section;
5. the function returns signed byte:
   `section[1 + weatherSlotIndex]`;
6. if the script resource is unavailable, it returns **33**.

## ff12-script source proof

The bundled ff12-script source defines the exact binary script header:

```cpp
struct tScriptHead {
    ...
    u32 unknown16Arr1Off; // 0x60
    u32 unknownScaleOff;  // 0x64 - u8 count, u8[count] (100,100,100)
    u32 pcDefOff;         // 0x68
    ...
};
```

The decompiler loads that field as:

```cpp
u8 weatherProbabilityCount = *(fileBuffer + header->unknownScaleOff);
const u8* weatherProbabilityData =
    fileBuffer + header->unknownScaleOff + 1;

for (u8 i = 0; i < weatherProbabilityCount; i++)
    weatherProbability.push_back(weatherProbabilityData[i]);
```

The compiler writes:

```cpp
u8 weatherProbabilityCount =
    static_cast<u8>(weatherProbability.size());

outFile.write(&weatherProbabilityCount, 1);

for (const auto weather : weatherProbability)
    outFile.write(&weather, 1);

scriptHead.unknownScaleOff =
    static_cast<u32>(layout.weatherProbabilityStartPos);
```

The high-level language exposes the field literally as:

```text
option weatherProbability = {...};
```

The documentation includes the example:

```text
option weatherProbability = {100, 0, 0};
```

Therefore `002658B0` is mechanically and source-correlated as:

**`WorldField_GetAuthoredWeatherProbabilityForSlot`**

This is stronger than a generic threshold/weight interpretation.

---

# 2. Meaning of `weatherProbability`

The native transition algorithm establishes the operational semantics.

## `0025ACA0`

Canonical V120 PrimaryOwner: **WorldAreaField**

Complete body:
- **107 bytes**
- SHA-256:
  `1b3c8438f6d17865bce2ef73931846e5e684d188879e680eec1de93f74fdc464`

Exact behavior:

1. query current Weather Slot;
2. read the authored `weatherProbability` for that slot through `002658B0`;
3. probability `0`:
   - current slot cannot be retained;
   - select another eligible slot;
4. probability `>=100`:
   - retain current slot;
5. probability `1..99`:
   - consume native MT19937;
   - scale to uniform 0..99;
   - retain current slot when `roll < probability`;
   - otherwise select another eligible slot;
6. tail-enter `0026D910(finalWeatherSlot)`.

Strong native working name:

**`WorldField_RollAndApplyWeatherSlotTransition`**

The `weatherProbability` value is therefore the **probability that the current Weather Slot survives the native weather-transition roll**.

It is also used by the alternate-slot resolver as a zero/nonzero eligibility indication.

Do not overstate it as a normalized probability distribution across all three slots.

---

# 3. Alternate Weather Slot selection is not probability-weighted

## `0025ABA0`

Canonical V120 PrimaryOwner: **WorldAreaField**

Complete body:
- **253 bytes**
- SHA-256:
  `e667fef7213170669d451dff789f2ff54cb870cbe818765d690b154de72dddd4`

Given current Weather Slot 1..3, it:

1. checks the other slots' `weatherProbability` values through `002658B0`;
2. treats nonzero alternate values as eligible;
3. selects the sole eligible alternative directly when only one remains;
4. uses native MT19937 when two alternatives remain eligible;
5. returns one of the three Weather Slots.

The observed alternate choice does **not** weight the two remaining alternatives according to their numeric `weatherProbability` values.

Conservative strong name:

**`WorldField_SelectAlternateEligibleWeatherSlot`**

Thus native weather behavior is:

**current-slot retention probability**
→ if not retained, choose among eligible alternative slots.

---

# 4. Authored script-call proof: `setweatherslot` and `getweatherslot`

The bundled ff12-script call map and the executable dispatch table align exactly.

## Script call `0x021A`

Authored name:

`setweatherslot(int)`

Dispatch target:

`003565C0`

## Script call `0x040C`

Authored name:

`getweatherslot()`

Dispatch target:

`00356250`

The neighboring `0x0219` / `0x021B` table entries also align with `animepauseclear` and `setnavimapindex`, eliminating an accidental-table-index explanation.

These authored names corroborate the Weather Slot semantics.

However, project policy remains:

**Do not use ScriptVM wrappers as XIIOnline replay seams.**

The wrappers are evidence of intent. The lower native WorldAreaField calls are the implementation seams.

---

# 5. `getweatherslot()` proves native getter `00265920`

## `00356250`

ScriptVM handler for authored `getweatherslot()`.

Its meaningful semantic work is:

1. call `00265920`;
2. return the resulting integer to the VM.

Therefore lower native:

## `00265920`

Complete body:
- **41 bytes**
- SHA-256:
  `e9bd7451c316314862af6ea8e5a7abbfdd6f6d4c8f0eb32e0f6bbd7a3ca66843`

is definitively the native:

**`WorldField_GetCurrentWeatherSlot1To3WithDebugOverride`**

Behavior:
- return positive debug Weather Slot override when active;
- otherwise return `signed(persistentPayload+0x1060) + 1`.

---

# 6. `setweatherslot(int)` proves lower apply path and one-shot preserve latch

## `003565C0`

ScriptVM handler for authored `setweatherslot(int)`.

Complete executable body:
- **99 bytes**
- SHA-256:
  `5819ab38a39de73bbaff074fa212437d73317ef5a5b70a85487b017c7911aa9a`

Mechanically:

1. pop the VM integer argument;
2. require a valid current field runtime;
3. require the field state to permit the operation;
4. require the script/map context to match the active map;
5. clamp requested Weather Slot to 1..3;
6. call lower native `0026D910(weatherSlot)`;
7. call `0026D8F0()`.

This establishes the implementation beneath authored `setweatherslot`.

Again:

**XIIOnline must not invoke this VM wrapper.**

---

# 7. `0026D8F0` is a one-shot preserve-current-weather latch setter

## `0026D8F0`

Complete body:
- **21 bytes**
- exact SHA-256:
  `499500bffe0d777a7af19365b59aa692f72c2587bf4fbe5ca71f59b7ccf7c8ae`

Exact body:

```text
call SaveImage_GetPersistentPayloadBase
payload[0x1061] = 1
return
```

There is only **one direct CALL** to `0026D8F0` in the executable:

the `setweatherslot` ScriptVM handler immediately after `0026D910`.

This gives the latch a much narrower meaning than a generic initialization flag.

## Interaction with `0026D910`

`0026D910` behaves as:

- if `payload+0x1061 == 0`:
  - commit the requested slot to `payload+0x1060`;
- if `payload+0x1061 != 0`:
  - preserve the previously committed `payload+0x1060` slot instead of replacing it;
- after deriving the field state:
  - clear `payload+0x1061` back to zero.

Therefore:

**`payload+0x1061` is a one-shot “preserve current Weather Slot on the next apply” latch.**

Strong working name for `0026D8F0`:

**`WorldField_SetPreserveCurrentWeatherSlotOnNextApply`**

It is transition policy, not the durable Weather Slot itself.

---

# 8. Separate WorldAreaField reset path also sets the same one-shot latch

`00268320`, canonical WorldAreaField, directly writes:

`payload+0x1061 = 1`

during a bounded field/runtime reset path.

That function also clears/reset two 0x200-byte field runtime banks under its own conditions.

This independently confirms that the byte is a **field-transition preservation mechanism**, not a ScriptVM-only marker and not the developer weather-lock option.

A separate later transition path explicitly clears the latch in one runtime state before continuing its field transition.

The authored debug call named `debug_setlockweatherslot` maps to a different native handler/state family, so `+0x1061` must not be mislabeled as the debug Weather Slot lock.

---

# 9. `0026D910` is the shared native Weather Slot apply owner

## `0026D910`

Canonical V120 PrimaryOwner: **WorldAreaField**

Complete body:
- **418 bytes**
- SHA-256:
  `1703f5dce9c22c84928f9e45874590c6080de584cb58296018a9138c7a13b4d2`

Historical V40 name:

`WorldField_InitializeCurrentFieldRuntimeParameters`

Historical evidence already proved:
- one of three authored mode records;
- MapRef-root/auxiliary data;
- persistent payload `+0x1060/+0x1061`;
- materialization of current-field runtime parameters.

The Weather Slot evidence now upgrades the anonymous “mode 1..3” to the authored **Weather Slot 1..3** domain.

## Direct entry-path census

The whole executable has only four direct control-flow entries to `0026D910`:

1. `0025ACA0` tail-jump:
   - normal native weather retention/transition roll;

2. `00266E74`:
   - global field/world bootstrap path;

3. `00266E7B`:
   - sibling bootstrap application;

4. `003565C0`:
   - authored `setweatherslot(int)` ScriptVM handler.

This small, coherent caller set supports `0026D910` as the **shared lower native Weather Slot application owner**.

---

# 10. `0026D910` does more than write the saved Weather Slot

Its exact transaction:

1. honor positive developer Weather Slot override if active;
2. clamp requested slot to 1..3;
3. obtain persistent payload;
4. obey the one-shot preserve latch;
5. commit/read zero-based Weather Slot at `+0x1060`;
6. select the corresponding one-of-three authored MapRef/environment subrecord;
7. derive/publish current WorldAreaField runtime parameters;
8. clear the one-shot preserve latch;
9. enter downstream field→Presentation reconfiguration.

This makes it a native **apply/materialize transaction**, not just a variable setter.

Strong refined working name:

**`WorldField_ApplyWeatherSlotAndDerivedEnvironmentState`**

or, if retaining historical terminology:

**`WorldField_InitializeCurrentFieldRuntimeParametersForWeatherSlot`**

Do not rename canonical V120 metadata in-place without its normal audit/replay process; these are semantic refinements for future reconstruction/native-seam use.

---

# 11. Immediate downstream Presentation refresh

The tail path from `0026D910` reaches `002E3D40` with zero-valued explicit inputs.

That zero-mode path:

1. obtains current field/context state through `003148F0`;
2. resolves canonical WorldAreaField state through `00264F10`;
3. queries the committed Weather Slot through `00265920`;
4. derives three weather/field-dependent parameters through:
   - `00377850`
   - `003777A0`
   - `003777B0`
5. tail-enters canonical Presentation owner:
   `0040AAD0`.

## `0040AAD0`

Canonical V120 Presentation owner:

**Embedded Presentation backend mode/orientation initializer**

Exact identity:
- **286 bytes**
- SHA-256:
  `ace98b940185f121d2eb0819301478dfa1f81c1493d7310a31ca89114039dd9b`

It:
- publishes Presentation backend selector globals;
- resets backend preset state;
- derives orientation transform;
- rebuilds normalized runtime basis.

Therefore `0026D910` automatically gives the chosen Weather Slot **immediate downstream Presentation coherence** through native WorldAreaField-derived parameters.

This is another reason to prefer it over direct writes to `payload+0x1060`.

---

# 12. Two authored layers of FFXII weather are now separated

The native architecture is:

## Layer A — EBP/script weather decision

Authored EBP/script header:

`weatherProbability`

Native readers/logic:

`002658B0`
→ `0025ABA0`
→ `0025ACA0`

Purpose:

**decide whether the current Weather Slot is retained and, if not, select an eligible alternate.**

## Layer B — MapRef/environment realization

Committed Weather Slot:

`0026D910`

Purpose:

**materialize the chosen slot into authored current-field environment/runtime parameters and refresh dependent Presentation state.**

Additional normal field-load paths then publish the committed slot into other resource/environment systems, including Movement resource configuration.

This corrects the earlier wording that treated the probability source and realized weather parameters as one authored MapRef family.

They are distinct layers.

---

# 13. Complete high-level native weather transaction

For an ordinary native field weather transition:

**EBP/script `weatherProbability`**
→ `002658B0` current-slot probability
→ `0025ACA0` retention RNG
→ if necessary `0025ABA0` alternate-slot selection
→ `0026D910` commit/apply selected Weather Slot
→ MapRef/environment parameter materialization
→ Presentation backend refresh
→ higher field initialization publishes committed slot
→ environment/resource notification channels
→ WorldAreaField→Movement bridge
→ Movement resource dirty transition
→ `0026E290`
→ unresolved `002F7380`
→ LegacyPS2GS texture-mip local-memory table rebuild.

This explains why Weather Slot changes eventually reach `002F7380` without making that function a Weather owner.

---

# 14. XIIOnline native-seam consequence

## Authority generation

On the authoritative world instance:

**allow native `0025ACA0` to make the weather transition decision.**

This preserves:
- authored EBP `weatherProbability`;
- native MT19937 behavior;
- eligibility rules;
- mods that legitimately alter EBP weather data.

Observe/network the **committed resulting Weather Slot**, not the local RNG draw.

## Receiver application

Strongest currently proven lower native apply candidate:

**`0026D910(chosenWeatherSlot)`**

Why:
- it is the common native apply target for both normal RNG weather transitions and authored `setweatherslot`;
- it commits/preserves persistent Weather Slot correctly;
- it materializes authored environment state;
- it performs immediate downstream Presentation refresh.

Do **not** invoke the VM wrapper `003565C0`.

Do **not** direct-write `payload+0x1060`.

Do **not** independently rerun `0025ACA0` on each receiver.

## Scripted `setweatherslot` fidelity

The authored command performs:

`0026D910(slot)`
→ `0026D8F0()`

So the exact native scripted semantic includes both:
1. apply requested slot now;
2. arm one-shot preservation for the next Weather Slot application.

For multiplayer reproduction of an authored scripted `setweatherslot` event, the one-shot preservation semantic may need to be reproduced as part of the event.

However, production use should still choose the **highest non-VM native transition** whose preconditions and downstream effects are verified.

Do not blindly call both functions in every weather synchronization case.

---

# 15. Durable world state vs transient local policy

Current static evidence supports:

## Durable logical weather state

**Weather Slot 1..3**  
persisted zero-based at `payload+0x1060`.

No separate adjacent persistent weather timer/phase was found in the exhaustive native read/write audit of this state family.

## Transient transition policy

`payload+0x1061`

one-shot preserve-current-slot-on-next-apply latch.

This is not durable weather identity.

For ordinary server world snapshots / late join:

synchronize/persist the committed Weather Slot.

For an in-flight scripted transition that requires exact next-apply preservation:

the transition event may also require preserve-latch semantics.

That is an event/lifecycle detail, not a reason to treat the latch as the server's durable Weather value.

---

# 16. Mod-compatibility consequence

The native weather pipeline now exposes two mod-compatible inputs:

1. **EBP/script `weatherProbability`**
   - controls weather retention/eligibility behavior;

2. **MapRef/environment Weather Slot records**
   - control how each committed slot is materialized.

A native-coherent XIIOnline implementation can preserve both:

authority uses the game's/mod's authored EBP probability logic  
→ server synchronizes resulting Weather Slot  
→ each receiver applies that slot through native WorldAreaField realization  
→ local authored MapRef/Presentation/Movement derived state rebuilds naturally.

This is preferable to:
- replacing weather RNG;
- forcing weather visual globals;
- replicating Movement dirty/cache state;
- replicating LegacyPS2GS allocations.

---

# 17. Spawn/rare-enemy ordering implication

Weather is a known input to FFXII conditional spawn eligibility.

Therefore the multiplayer ordering contract should be:

**authoritative Weather Slot settles**
→ receiver/world weather revision is known
→ weather-dependent native spawn eligibility/controller logic runs
→ resulting enemy realization is synchronized through the existing persistent-world model.

Do not permit a client to evaluate weather-dependent rare/conditional spawn state against a stale Weather Slot while the authoritative world has already advanced.

This preserves the project's rule:

**native eligibility remains native; synchronize authoritative world inputs/outcomes rather than replacing the inner eligibility engine.**

---

# 18. Remaining weather proof debt

Before production XIIOnline integration:

1. live-test `0026D910(slot)` in a receiver-safe controlled context;
2. verify exact thread/game-frame requirements;
3. verify whether a higher non-VM WorldAreaField transaction provides even better downstream coherence;
4. determine which runtime weather changes automatically reach Movement reconfiguration outside field-load initialization;
5. determine whether a scripted `setweatherslot` replication event must reproduce `0026D8F0` on receivers;
6. characterize the exact conditions under which `00268320` arms the same preserve latch;
7. retain notification channels 0 / 31 unnamed until stronger authored evidence appears;
8. verify multi-client late join/reconnect weather realization;
9. test weather-dependent Rare Game/native spawn eligibility ordering;
10. perform real linked certification.

Static GFZ proof is architecture/reverse-engineering evidence, not live multiplayer certification.

---

# 19. Supersession note

In `V121_GN_READ_ONLY_WEATHER_SLOT_TRIGGER_ADDENDUM_2026-08-31.md`, replace:

**“authored MapRef per-slot threshold/weight”**

for `002658B0`

with:

**“authored EBP/script-header `weatherProbability` value for the requested Weather Slot”**

The rest of the MapRef-derived `0026D910` realization analysis remains valid.

The corrected architecture is:

**EBP/script probability decision**
→ **Weather Slot**
→ **MapRef/environment realization**
→ **Presentation/Movement/local derived state**.

