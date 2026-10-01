# V121 GN — READ-ONLY WEATHER-SLOT TRIGGER ADDENDUM — 2026-08-31

**Status:** READ_ONLY_ANALYSIS_ONLY / NOT_APPLIED / NOT_PERSISTENCE_CERTIFIED  
**Project:** For Xeavin — FFXII_TZA GFZ/GZF V121 full-executable reconstruction  
**Secondary use:** XIIOnline weather/environment native-seam research  
**Intended physical parent:** GM160 recovery-transfer GZF contained in the uploaded handoff ZIP  
**Authorized EXE SHA-256:** `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`

## 0. Hard fence

This addendum refines the upstream trigger context of current GN proposal:

`002F7380` — `Presentation.LegacyPS2GS.TextureMipLocalMemoryBudgetAndReferenceSlotTableRebuild`

It does **not** mutate the GM160 recovery-transfer GZF. The uploaded handoff ZIP is the authoritative transfer package and explicitly contains that GZF. The current execution filesystem adapter has not exposed the archive payload as ordinary `/mnt/data` bytes, so exact-current Ghidra mutation/pack/reopen work is not claimed here.

Official persistence-certified GM160 state remains **38,161 functions / 38,001 explicit / 160 unresolved / 99.58072% / overlap 0**.

## 1. Authored proof: the 1..3 selector is a Weather Slot

### `0017D490`
- body: **20 bytes**
- SHA-256: `3ee8dd6c10995742c607ccab0955095104fb96b93df3ded6aab9593845a604d9`

The function obtains the global debug/config singleton and returns dword `[singleton+0xAAC]`.

The same exact field `+0xAAC` is passed to the authored executable format string:

`%s%s %d %s, Weather Slot:%d (Triangle/Cross to toggle)`

The argument placement puts `[singleton+0xAAC]` in the integer corresponding to `Weather Slot:%d`. Therefore `0017D490` is a **Weather Slot override getter**. This is authored-string evidence, not address-range inference.

## 2. Persistent weather state

`002EF2B0` is the existing `SaveImage_GetPersistentPayloadBase` boundary.

The persistent payload contains:
- `payload+0x1060` — **zero-based current/saved Weather Slot index 0..2**;
- `payload+0x1061` — **weather-slot preserve/init marker**.

When the marker is clear, native weather initialization may publish a new requested slot into `+0x1060`. When set, the current slot is preserved across the corresponding initialization/transition path. Native initialization later clears the marker.

## 3. Weather-slot runtime initializer — `0026D910`

- body: **418 bytes**
- SHA-256: `1703f5dce9c22c84928f9e45874590c6080de584cb58296018a9138c7a13b4d2`

Input is a requested Weather Slot in the **1..3** domain.

The body:
1. queries `0017D490` and uses a positive debug Weather Slot override when present;
2. converts 1..3 to zero-based 0..2 and clamps the three-slot domain;
3. obtains the persistent payload;
4. when `payload+0x1061 == 0`, writes the zero-based slot into `payload+0x1060`;
5. uses `payload+0x1060` to select one of **three authored MapRef subrecords**;
6. derives/publishes current field runtime parameters from that record;
7. clears `payload+0x1061`.

The previous generic “field mode 1..3” interpretation is superseded by the authored-string-backed **Weather Slot 1..3** interpretation.

## 4. Authored per-slot threshold getter — `002658B0`

- body: **112 bytes**
- SHA-256: `9689942f64e9a4793c82b8b06bbbff16c8e79081cf60f9d1c80e7a641abec8e7`
- canonical V120 PrimaryOwner: **WorldAreaField**

Input Weather Slot 1..3 is converted to zero-based 0..2. The function validates the loaded authored field resource, resolves its record, and returns signed byte `record+1+slotIndex`.

If the resource is unavailable it returns **0x21 = 33**.

The return is consumed as:
- zero/nonzero eligibility;
- threshold against a native uniform 0..99 roll;
- `>=100` always-keep behavior.

Conservative mechanism description: **authored per-weather-slot retention/transition threshold or weight**. The exact authored schema field name remains unclaimed.

## 5. Alternate Weather Slot resolver — `0025ABA0`

- body: **253 bytes**
- SHA-256: `e667fef7213170669d451dff789f2ff54cb870cbe818765d690b154de72dddd4`
- canonical V120 PrimaryOwner: **WorldAreaField**

Given current Weather Slot 1..3, it checks the other slots through `002658B0`, selects an eligible alternative, and consumes native MT19937 only when two eligible alternatives require a random choice. It always returns 1..3.

Working mechanism: **three-slot eligible Weather Slot alternate resolver**.

## 6. Weather retention roll and apply — `0025ACA0`

- body: **107 bytes**
- SHA-256: `1b3c8438f6d17865bce2ef73931846e5e684d188879e680eec1de93f74fdc464`
- canonical V120 PrimaryOwner: **WorldAreaField**

Exact algorithm:
1. current slot = positive debug override, otherwise `payload+0x1060 + 1`;
2. threshold = `002658B0(currentSlot)`;
3. threshold `0` → choose alternate through `0025ABA0`;
4. threshold `>=100` → keep current slot;
5. threshold `1..99` → call native `RNG_MT19937_NextU32_Thunk`, scale to **0..99** through high-half multiply-by-100, keep current if `roll < threshold`, otherwise choose alternate;
6. tail-enter `0026D910(finalSlot)`.

Strong working name: **`WorldField_RollAndApplyWeatherSlotTransition`**.

## 7. Current Weather Slot getter — `00265920`

- body: **41 bytes**
- SHA-256: `e9bd7451c316314862af6ea8e5a7abbfdd6f6d4c8f0eb32e0f6bbd7a3ca66843`

Behavior:
1. return positive Weather Slot debug override when present;
2. otherwise return `signed(payload+0x1060) + 1`.

Strong working name: **`WorldField_GetCurrentWeatherSlot1To3WithDebugOverride`**.

It does not roll weather; it queries the committed slot.

## 8. Higher field initialization transaction — `002620E0`

- body: **231 bytes**
- SHA-256: `7605a77072bf9d04cf0330b8b662aa627d791dfa16dde5dd68f6d304127f182f`

Observed path:
1. performs existing field/resource setup;
2. calls `0025ACA0`, causing native Weather Slot roll + apply;
3. re-reads the committed Weather Slot;
4. calls shared resource/notification dispatcher `0026FAD0` twice with category/index `0` and `0x1F`, both carrying the committed Weather Slot;
5. re-reads the slot;
6. calls `00379860(weatherSlot)`;
7. calls `00379290()`;
8. continues normal field initialization.

This proves the committed Weather Slot is **published into multiple downstream native systems** after the WorldAreaField decision.

The exact authored meanings of `0026FAD0` categories `0` and `0x1F` remain unnamed.

## 9. Direct zero-based weather publication — `00379860 / 00379F50`

`00379860` is a tiny gate: when the relevant field/environment runtime object is active it tail-forwards the 1..3 Weather Slot to `00379F50`; otherwise it returns.

`00379F50` subtracts one, accepts only 0..2, and publishes the zero-based slot into runtime global `02EBF408`.

Thus another local field/environment runtime receives the committed Weather Slot in zero-based form. Its exact object type is intentionally not overtyped here.

## 10. Weather Slot → Movement resource reconfiguration — `00379290`

- body: **53 bytes**
- SHA-256: `3ffc81922688323d8b9ed02b655d844aab271c985fa78c30743128c4dac4eba6`
- canonical V120 PrimaryOwner: **WorldAreaField**

When the relevant field runtime object exists, this function:
1. marks WorldAreaField lifecycle state;
2. gets the current Weather Slot from `00265920`;
3. tail-calls `0026E8D0(weatherSlot)`.

This is the direct native bridge:

**committed Weather Slot → Movement resource configuration**.

## 11. Movement dirty transition — `0026E8D0`

- body: **134 bytes**
- SHA-256: `68aea8568f166938bb4fcafe30d29ce45f7997b71402fb3ac2ba35d224f95ebc`
- canonical V120 PrimaryOwner: **Movement**

It publishes the incoming slot/resource selector into Movement state, sets dirty flag `0209A708=1`, rebuilds the associated Movement resource descriptor family, and finalizes the local resource configuration.

Weather remains upstream WorldAreaField state. This is receiver-local derived resource state.

## 12. Movement dispatcher → `002F7380`

### `0026E290`
- body: **97 bytes**
- SHA-256: `aac93b37c874c23a7b634ae96bab718d3d89d826cc60c4c76bb258b66b023793`
- canonical V120 PrimaryOwner: **Movement**

When the current resource is active and dirty:
1. obtain the Presentation-side dataset;
2. call `002F7380`;
3. clear `0209A708`;
4. continue normal resource callback processing.

Complete proven chain:

**WorldAreaField weather roll**
→ committed Weather Slot 1..3
→ persistent zero-based slot `+0x1060`
→ authored MapRef weather parameters
→ field/resource notifications
→ `00379290`
→ `0026E8D0` Movement resource reconfiguration
→ dirty state
→ `0026E290`
→ `002F7380`
→ LegacyPS2GS texture-mip local-memory budget/slot-table rebuild.

## 13. Effect on GN semantic proposal `002F7380`

The strong GN proposal remains:

`Presentation.LegacyPS2GS.TextureMipLocalMemoryBudgetAndReferenceSlotTableRebuild`

Do **not** rename it as a Weather function. It does not choose weather, consume the weather RNG, own persistent weather state, or read `+0x1060` directly. Weather Slot is now a **proven upstream trigger/context**.

## 14. XIIOnline weather/environment architecture consequence

The multiplayer roadmap already places weather/environment in shared world-state work. The native reconstruction gives a concrete implementation model.

### Authority / generation
On the authoritative native FFXII instance:
- allow `0025ACA0` to perform the real native Weather Slot transition;
- preserve authored MapRef thresholds/eligibility;
- preserve native MT19937 behavior;
- observe the **committed resulting Weather Slot**.

The server should not replace the native authored weather RNG/eligibility logic.

### Network truth
Synchronize the **committed Weather Slot outcome**, fenced by stable world/map/revision identity.

Do not network:
- local Movement dirty bits;
- `0209A6xx` cache/resource details;
- LegacyPS2GS table entries/allocations;
- `002F7380` derived state.

### Receiver realization
Apply the authoritative resulting slot through the highest proven safe native WorldAreaField weather-application transition, then let native downstream field notifications, Movement reconfiguration and Presentation/GS rebuild happen locally.

Do **not** independently rerun `0025ACA0` on every receiver. Independent MT19937 draws can select different weather.

### Late join / reconnect
Persist the committed Weather Slot as authoritative world state. A late joiner realizes the existing slot rather than rolling a new one simply because it loaded the field later.

### Mod compatibility
Because the authority still consumes the game's authored MapRef weather data and native RNG path, legitimate weather-data mods remain inputs to the authoritative native outcome. XIIOnline synchronizes the result rather than replacing the decision engine.

## 15. Best-native-seam roles

- `0025ACA0` — **OBSERVE ON AUTHORITY / WEATHER GENERATION**
- `0026D910` — **RECEIVER-APPLICATION CANDIDATE / WORLD-FIELD WEATHER APPLY**; exact production-safe preconditions still require challenge
- `00265920` — **QUERY CURRENT WEATHER SLOT**
- `00379290` — **DOWNSTREAM WORLD→MOVEMENT BRIDGE**
- `0026E8D0` — **DERIVED LOCAL MOVEMENT RECONFIGURATION**
- `0026E290` — **DERIVED LOCAL DIRTY DISPATCH**
- `002F7380` — **DERIVED LOCAL PRESENTATION / LEGACY GS REBUILD**

Known addresses are starting points, not immutable choices. If a higher WorldAreaField transition is proven to apply a committed slot with more complete downstream coherence, prefer it.

## 16. Remaining proof debt

Before production XIIOnline integration, verify:
1. exact ABI/preconditions for applying an externally chosen Weather Slot through the highest safe WorldAreaField transition;
2. whether `0026D910` alone is correct for every receiver state or a higher transition should be invoked;
3. exact semantic meaning of `0026FAD0` categories `0` and `0x1F`;
4. whether scripted weather changes carry additional state beyond the 1..3 slot;
5. whether weather timing/counters require shared persistence in addition to the committed slot;
6. ordering relative to rare-enemy/native spawn eligibility — weather must settle before weather-dependent eligibility is treated as authoritative;
7. real linked multiplayer certification.

Static GFZ proof does not substitute for live multiplayer proof.

## 17. Current GFZ accounting

This weather discovery refines context/mechanism only.

Applied GN rows: **0**

Persistence-certified GM160 remains:
- **38,001 explicit**
- **160 unresolved**
- **99.58072%**
- **overlap 0**

Strong unresolved GN proposals remain:
1. `00313A00` — `InputGameplay.FieldBattleCapabilityAndUIRequestInhibitMaskReconciliation`
2. `002F7380` — `Presentation.LegacyPS2GS.TextureMipLocalMemoryBudgetAndReferenceSlotTableRebuild`

Prospective arithmetic if both later pass exact-current mutation/persistence certification:
- **38,003 explicit**
- **158 unresolved**
- **99.58596%**

That prospective state is **not** a checkpoint.
