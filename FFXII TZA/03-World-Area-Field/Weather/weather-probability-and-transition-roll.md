---
system: Weather probability and transition roll
category: 03-World-Area-Field
status: DOCUMENTED
owner_layer: PrimaryOwner:WorldAreaField
evidence_tier: 1
verified_against:
  gzf_sha256: 2ed8affb732f0def0a7852e0788298ae36b81206099dd1712f59825fc1c00bb9
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: additive-annotation across GN158 -> GN161 - every step of the certified lineage is additive on the canonical record (internal 38161, owner 9409 and finalNo 585 constant at all five generations; each step's codeDomain and explicit rise equals its unresolved fall). Of the functions classified since GN158 this document cites none of batch R109's 109; the 21 classified before GN160 are named in AUDIT-LOG's batch records and not in a tracked machine-readable list, so identity is not claimed. Voided by any delta that removes or rewrites a comment, tag, name, prototype or body range.; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md, lineage extension (twenty ledger figures across five generations)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  snapshot_sha256: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  previous_parent: 381d2aea82b96d7af781844e191d9b92a37e93bd2d4ff276a33ba56e7307461b
last_reviewed: 2026-09-02
audit:
  passes: 1
  last_pass: 2026-09-02
  last_pass_state: reverification-against-current-parent
  crossref_clean: true
  reopened_count: 1
---

# Weather probability and transition roll

> How FFXII decides whether the weather changes when you enter an area — and why it is not
> a timer.

## 1. What the player sees

Weather does not drift while you stand still. It is decided **once**, when a field area's
runtime initializes. Re-entering a zone can change it; standing in it will not. Some areas
never change weather (probability 100), ~~some always re-roll (probability 0)~~ some leave the current slot whenever another slot is eligible (probability 0), an area whose three probabilities are all 0 never changes *(corrected 2026-10-02, OPUS: every arm of `0025ABA0` falls back to the current slot — `0025ABF0`, `0025AC1D`, `0025AC47`, `0025AC88`; the 2026-09-21 correction below)*, most sit
somewhere in between — and it is the *zone's own script data* that says which.

## 2. Native mechanism

The decision is a single retention roll on the **current** slot, not a distribution over all
three.

`0025ACA0` — the transition owner:
1. query the current Weather Slot (`00265920`);
2. read that slot's authored `weatherProbability` (`002658B0`);
3. probability **0** → ~~current slot cannot be retained →~~ pick an alternate with non-zero probability, or keep the current slot when neither has one *(corrected 2026-10-02, OPUS: `0025ABA0` reads only the alternates' probabilities, `002658B0(slot) > 0`, and every arm falls back to the current slot — `0025ABF0`, `0025AC1D`, `0025AC47`, `0025AC88`)*;
4. probability **≥ 100** → retain current slot;
5. probability **1..99** → draw native MT19937, scale to a uniform `0..99`, retain if
   `roll < probability`, else pick an alternate;
6. tail-enter `0026D910(finalSlot)` to apply.

`002658B0` — the probability reader:
1. convert slot `1..3` → index `0..2`;
2. validate the loaded script/EBP resource;
3. read script header field at offset **`+0x64`**, resolve to the authored variable section;
4. return signed byte `section[1 + slotIndex]`;
5. if the script resource is unavailable, return **33**.

`0025ABA0` — the alternate resolver: checks the *other* two slots' probabilities, treats
nonzero as eligible, picks the single eligible one directly, ~~and draws MT19937 only when two~~
~~remain.~~ and draws MT19937 once, before any probability is read, only when the current slot is 2; from slots 1 and 3 the order is fixed, slot 2 first *(corrected 2026-10-02, OPUS: `0025ABAA sub ecx, 1` / `0025ABAD je`, `0025ABB3 cmp ecx, 2` / `0025ABB6 je`; the only call to `00379CD0` is `0025ABB8`; CON-147 below)*. **It does not weight the alternatives by their probability values.**

### Timing

`002620E0` runs the roll, and it is gated:
- requires `managerRecord+0x28 == 0` — the **primary ActorManager, index 0**;
- tests initialization bit `managerRecord+0x10 & 0x04`;
- if already set, the ~~whole~~ weather/resource initialization core is skipped, but the two event posts still run *(corrected 2026-10-02, OPUS: `002620F7 jne 002621A8`; `002621A8 mov ecx, 0xB` / `002621AD call 003601C0`, `002621BC jmp 003601C0`)*;
- otherwise: roll, publish, initialize field resources, then set the bit.

So the roll is a **one-shot per qualifying manager-record lifecycle**. Not per actor, not per
ActorManager, not per frame, and not from a free-running weather timer — no such timer has
been found in this state family.

## 3. Key addresses

| Address | Working name | Body | Role |
|---|---|---:|---|
| `0025ACA0` | `WorldField_RollAndApplyWeatherSlotTransition` | 107 B | the decision |
| `002658B0` | `WorldField_GetAuthoredWeatherProbabilityForSlot` | 112 B | reads EBP header `+0x64` |
| `0025ABA0` | `WorldField_SelectAlternateEligibleWeatherSlot` | 253 B | eligible-alternate picker |
| `002620E0` | *(field-runtime init core)* | 231 B | one-shot gate, primary ActorManager only |
| `0025D9E0` | `ActorManager_RunFieldRuntimePass` | — | caller |
| `00265920` | `WorldField_GetCurrentWeatherSlot1To3WithDebugOverride` | 41 B | current slot |
| `0026D910` | `WorldField_ApplyWeatherSlotAndDerivedEnvironmentState` | 418 B | apply target |

## 4. Data structures

Script (`.ebp`) header — from the ff12-script source, `CScriptContainer.h`:

```
tScriptHead
  +0x60  u32  unknown16Arr1Off
  +0x64  u32  unknownScaleOff      -> u8 count, then u8[count]   == weatherProbability
  +0x68  u32  pcDefOff
```

Authored form in the high-level script language:

```
option weatherProbability = {100, 0, 0};
```

Semantics: **the probability that the current Weather Slot survives the roll.** Also used as
a zero/nonzero eligibility flag by the alternate resolver.

```
ActorManager record   (stride 0x288)
  +0x10   u32  statusBits        bit 0x04 = field-runtime init already done
  +0x28   u32  managerIndex      0 = primary; weather rolls only here
```

## 5. Call chain

```
field/runtime activation
  -> 0025D9E0  ActorManager_RunFieldRuntimePass
     -> 002620E0                       [gate: index 0, init bit clear]
        -> 0025ACA0                    roll
           -> 002658B0                 authored weatherProbability
           -> MT19937 (gameplay RNG)
           -> 0025ABA0                 alternate if not retained
           -> 0026D910(finalSlot)      APPLY  (tail jump)
        -> 00265920                    re-read committed slot
        -> 0026FAD0(0,    slot + 1, managerIndex)   EFB binding channel 0    (the ambient layer)
        -> 0026FAD0(0x1F, slot + 1, managerIndex)   EFB binding channel 0x1F (the weather layer)
        -> 00379860(weatherSlot)
        -> 00379290()                  -> WorldAreaField -> Movement bridge
        -> set init bit 0x04
```

**Upstream:** ActorManager field-runtime pass.
**Downstream:** apply, then environment/Presentation/Movement fan-out.
**Do not confuse with:** the Presentation procedural PRNG — see
[`../../21-RNG-And-Determinism/`](../../21-RNG-And-Determinism/). This roll uses gameplay
MT19937.

## 6. Modding notes

- **Best intervention point for changing weather behaviour:** the authored
  `weatherProbability` in the zone's `.ebp`. Decompile with `ff12-script.exe`, edit, recompile.
  That is the designer-intended knob and it stays mod-compatible.
- **Do not** replace the roll. Other mods legitimately alter EBP weather data; replacing
  `0025ACA0` discards their intent.
- **XIIOnline:** let the **authority** run the native roll, then replicate the *committed
  Weather Slot outcome*. Do not re-roll independently on each client — MT19937 draws will
  diverge. Do not network the RNG draw itself.
- **Ordering matters for late join:** weather feeds conditional spawn eligibility. The
  authoritative slot must settle *before* a joining client evaluates weather-dependent spawn
  or combat prediction.

## 7. What is not known

- [x] ~~Meaning of notification channels **0** and **0x1F** (open question **D-8**).~~ **Read 2026-09-12
      (FABLE): they are EFB binding channels, not notification channels.** `0026FAD0(channel, value,
      manager)` is the effect registry's instantiate call: when the field's EFB is loaded (`02F8F238`,
      set by the EFB loader `0026FB90`) it looks up the kind-2 record `{2, channel, manager}`
      (`0024F680`), allocates one if absent, and runs `0026F470` over the EFB's **binding table** —
      the `0xA0`-byte rows that follow the embedded EFX blobs ([the EFX / EFB page](../../17-Presentation-Rendering/Effect-File-Formats/efx-and-efb-effect-containers.md) §3) — instantiating every
      row whose channel byte `+4` equals `channel` (`0026F534`–`0026F53B`; `−1` is a wildcard) and whose
      enable byte at **`+7 + value`** is set (`0026F522`–`0026F528`). The roll passes `value =
      committed slot + 1` (`0026212A`, `00262155`), so the four bytes `+8`–`+0xB` are the row's
      per-weather-slot enables. Over all **410** shipped `.efb` (2,615 rows, channels 0–63):
      **channel 0** rows (203, in 78 maps) are enabled for every slot in 201 of 203 — the field's
      always-on ambient layer — and **channel 0x1F** rows (613, in 276 maps; the most used channel)
      are weather-selective (`01 00 00 00` × 149, `00 00 01 01` × 88, `00 00 01 00` × 74 …) — the layer
      that changes with the weather. Which effect a row instantiates (its `+5` definition id through
      `0024F610`) and the rest of `0026F470` are the residue. Tally in
      `Tools/work/FABLE/bf3-scratch/efb_channels-2026-09-12.json`.
- [x] ~~Whether any path outside field-init re-runs the roll (open question **F-2**).~~
      **ANSWERED 2026-09-16 (FABLE): no path does.** **The latch, read from the body.** `002620E0` returns immediately unless `dword [rcx + 0x28] == 0` (`002620E6`–`002620ED`), ~~skips its whole body~~ skips the roll and the resource posts, but not the two `003601C0` event posts at `002621A8` *(corrected 2026-10-02, OPUS: `002620F7 jne 002621A8`; `002621A8 mov ecx, 0xB` / `002621AD call 003601C0`, `002621BC jmp 003601C0`)*, if `byte [rcx + 0x10] & 4` (`002620F3`–`002620F7`), and **sets that bit itself at `002621A4`** on the way out. It is a once-per-field-setup body, not a per-frame one. **The roll cannot be re-run.** `0025ACA0` has **exactly one direct caller**, `002620E0`, and **zero** functions reach it by any route that does not pass that latch. **Movement reconfiguration cannot be reached either.** `0026E8D0` has two direct callers, `00379290` and `00379630`; the only thing that reaches *those* is the same latch. Its entire reverse cone within 8 hops is **12 functions** and contains **one** route. **But APPLY is different, and this is what the question was circling.** `0026D910` has **three** direct callers: the roll `0025ACA0`, one CoreRuntimeScheduling path, and **`003565C0` - the `Script_VM_Native_Bridge` handler for the verb `setweatherslot`, call id `021A`, arity 1.** *(The CoreRuntimeScheduling pair is named on the `F-2` register row rather than here: naming it on this page would pull in two Input edges this document has no crossing section for, and I am not classifying a crossing I have not read.)* So **a script can change the weather slot at runtime, in one hop, bypassing both the roll and the latch entirely.** **Of the five weather verbs in the table, only that one gets anywhere near this machinery:** `021A setweatherslot` reaches APPLY at depth 1, while `2024 debug_setweather`, `209F debug_setlockweatherslot`, `03DD changeenvsoundweather` and `040C getweatherslot` reach **none** of the roll, the apply or the reconfiguration within six hops. **THE ASYMMETRY IS THE ANSWER.** A runtime weather change commits a new slot **without re-rolling and without rebuilding Movement's resource banks** - those keep whatever the field-setup pass built. That is a real behavioural statement about the shipped build, and it is why *which runtime weather changes reach Movement reconfiguration* has the answer **none**. *The limit, and it is the one that matters.* `edges.tsv` carries **direct calls**. An indirect or virtual call into `0026D910`, `00379290` or `0026E8D0` would be **invisible to this method**, and this image has 477 `call reg` sites (`AR-5`). **So this is a statement about every route the direct-call graph contains, not a proof that no route exists.** I also read the latch and the dispatcher bodies but not `00379630`'s.

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| `002658B0` reads script header `+0x64` | complete body (112 B, `9689942f…c8e7`) | 1 |
| That field is `weatherProbability` | ff12-script `CScriptContainer.h` (`unknownScaleOff //64 - u8 count, u8[count] (100,100,100)`), `CScriptDecompileAsmLoad.cpp:142`, `CScriptCompileAsmWrite.cpp:938`, `docs/language.md` | 9 |
| Retention semantics 0 / 1-99 / ≥100 | complete body of `0025ACA0` (107 B, `1b3c8438…fdc464`) | 1 |
| Alternates are not probability-weighted | complete body of `0025ABA0` (253 B, `e667fef7…ddd4`) | 1 |
| Roll is one-shot at primary ActorManager init | complete body of `002620E0` (231 B, `7605a770…182f`); `+0x28` proven to be the manager index by the bootstrap loop writing `edi` into it at stride `0x288` | 1 |
| `setweatherslot`/`getweatherslot` IDs | ff12-script catalog `0x021A` / `0x040C`, verified against the executable dispatch table; neighbours `0x0219`/`0x021B` also align, ruling out a table-index accident | 9 |

**Superseded readings:**
- *Old:* `002658B0` returns "an authored MapRef per-slot threshold/weight."
  *New:* it is specifically the EBP/script-header `weatherProbability`. The probability layer
  (script) and the realization layer (MapRef/environment) are **different authored layers**.
- *Old:* weather rerolls periodically on a timer.
  *New:* one-shot at primary ActorManager field-runtime initialization.

## 8b. Re-verified 2026-09-02 against the current parent (AH-3)

This document was stamped against parent `381d2aea...`. The database's certified parent is now
`2ed8affb...`, so its binary-side claims were **re-read** rather than re-stamped.

### What was checked

All four load-bearing addresses were decompiled fresh against the current parent:

| Address | Current-parent name | Claim | Result |
|---|---|---|---|
| `0025ABA0` | `FUN_0025aba0` | draws from the gameplay RNG | ✅ calls `RNG_MT19937_NextU32_Thunk` |
| `0025ACA0` | `FUN_0025aca0` | scales a draw to `0..99` | ✅ calls `RNG_MT19937_NextU32_Thunk` |
| `002658B0` | `FUN_002658b0` | in the weather chain | ✅ resolves |
| `0026D910` | `WorldField_InitializeCurrentFieldRuntimeParameters` (**the GFZ name**; this database calls the same 418-byte function `WorldField_ApplyWeatherSlotAndDerivedEnvironmentState` — see below) | field-init entry | ✅ resolves, name unchanged |

**No claim was contradicted.** The MT19937 attribution holds, which matters because the RNG document
was separately corrected on 2026-09-02 to note that MT19937 is *an* authoritative gameplay stream
rather than *the* one - weather is genuinely on MT19937, not on the shared LCG.

### One function, two names — resolved 2026-09-02

`0026D910` appears in this document under **both** names, which is confusing without a note:

| Name | Source |
|---|---|
| `WorldField_InitializeCurrentFieldRuntimeParameters` | **the GFZ's own working name**, in `functions.tsv` |
| `WorldField_ApplyWeatherSlotAndDerivedEnvironmentState` | **this database's working name**, adopted in [`weather-apply-and-environment-materialization.md`](weather-apply-and-environment-materialization.md) |

They are the **same 418-byte function**. The database renamed it deliberately: that document argues
from the body that `0026D910` is a multi-subsystem *apply* owner — it reads and writes save payload
`+0x1060`/`+0x1061`, consults `g_pMapRefResourceRoot` and calls into Presentation — and therefore
*"is not a setter"* and not merely field-parameter initialisation. The GFZ name describes where it
sits in the field-init path; the database name describes what it does.

**Both names are kept**, because dropping the GFZ name would break tracing back to the annotation
set, and dropping the database name would discard a justified reading. What was missing was this
note saying they denote one function. Found by `check_consistency.py`, which flags any address given
two incompatible names across the database.

### A cross-link the original document could not have had

`0025ACA0` reads:

```c
iVar1 = *(char *)((longlong)pvVar4 + 0x1060) + 1;
```

and `WorldField_InitializeCurrentFieldRuntimeParameters` both reads and writes `+0x1060` and
`+0x1061`, clearing the latter at the end.

**Those are save persistent-payload offsets**, mapped independently in the save document on the same
day by decompiling all 70 callers of `SaveImage_GetPersistentPayloadBase`:

```
+0x1060   u8   field runtime parameter        WorldField_InitializeCurrentFieldRuntimeParameters   <- corrected 2026-10-02, OPUS: s8 - six of its seven readers sign-extend (movsx at 0025ACC1, 00262123, 0026214E, 0026217C, 0026593B, 0026D96F); only 0026D9BB zero-extends
+0x1061   u8   initialization state           WorldPersistence_ResetBanksAndMarkInitializationState
```

So **the weather roll reads a byte of the save image**, and the field-init path writes it. Weather
state is not purely runtime - it is anchored to the persistent payload, alongside the current area
id at `+0x1044`.

The two documents reached the same bytes from opposite directions - one from the weather chain, one
from a census of payload consumers - and agree.

> **Corrected 2026-09-02, same day.** This paragraph originally added *"and neither was written
> knowing about the other."* **That was wrong.** The sibling call-chain document
> `call-chains/field-init-weather-to-legacyps2gs-rebuild.md` already recorded
> `payload+0x1060 commit (or preserve, per +0x1061)` before the compaction. The corroboration between
> the payload census and the weather chain is real; the claim of *independence* was not, and was made
> without checking the neighbouring document that had the answer.

### Stamp advanced, honestly

The `verified_against` block now names the current parent, and `previous_parent` records what it was
stamped to before. **The stamp moved because the bodies were re-read**, per the rule in the evidence
standard - not to make `check_provenance.py` go green.

Claims sourced from the `ff12-script` decompiler (the `tScriptHead` offsets and the
`weatherProbability` semantics in section 4) are unaffected by the parent and were not re-checked.

## 9. Related

- [`weather-slot-state-model.md`](weather-slot-state-model.md)
- [`weather-apply-and-environment-materialization.md`](weather-apply-and-environment-materialization.md)
- [`call-chains/field-init-weather-to-legacyps2gs-rebuild.md`](call-chains/field-init-weather-to-legacyps2gs-rebuild.md)

## Cross-subsystem neighbours — disposition (audit pass, repos-2d, 2026-09-03)

The neighbours `audit_crossrefs.py` reports for this document are the Weather system's shared
field-frame neighbourhood, seen from this document's angle. **The census is stated once**, in
[weather-apply-and-environment-materialization.md](weather-apply-and-environment-materialization.md)
§ *Cross-subsystem neighbours*, rather than repeated in each of the six Weather documents:

- **Core runtime scheduling** — `ImageAddress_ResolveRuntimePointer` (815 callers, 18 owners), the
  convention every authored table in this engine is addressed through. Runtime infrastructure.
- **Audio** and **Party** — callees of the field-frame routines `ActorManager_RunFieldRuntimePass`,
  the area initialiser, and two small field routines, cited here for their Weather role. A frame
  pass that drives audio and asks who the party focus is, is doing its own job.
- **RNG/random selection** — `RNG_MT19937_NextU32_Thunk`. Not unaccounted: it is the Weather
  transition roll, documented under the engine's own algorithm name, **MT19937**.
- **Actor/Entity**, **Combat Action**, **Spawn/Encounter/Lifecycle**, **Platform/Online/Achievements**
  — callers of the field-id accessor `003148F0`, whose 49-caller census is enumerated in
  [`../../00-Engine-Core-Runtime/Shared-State-Accessors/cross-subsystem-accessor-hubs.md`](../../00-Engine-Core-Runtime/Shared-State-Accessors/cross-subsystem-accessor-hubs.md) §2.
- **Save/Load** — the Weather Slot is persisted state; the persistence path is the relationship.
- **CombatFormula - CLIENT (54 edges).** `00265020`, `00379CD0` are also called by bodies filed to combat formula: `00384F40`, `003851F0`, `00387130` - shared machinery across the layer boundary, no shared ownership.
- **Gameplay - CLIENT and SERVICE (4 edges).** `00203170`, `00265020` are also called by bodies filed to Gameplay: `00339630` (Combat), `0031ADB0` (CombatAction); `0025D9E0` reaches bodies filed to Gameplay: `00234150` (CombatAction) - shared machinery across the layer boundary, no shared ownership.
- **Movement - CLIENT (61 edges).** `00203170` is also called by bodies filed to movement: `0022EF20`, `00230790`, `0026EB30` - shared machinery across the layer boundary, no shared ownership.
- **Rewards_Progression_Economy - CLIENT (4 edges).** `00265020`, `00379CD0` are also called by bodies filed to rewards/progression: `002FB150`, `00312280`, `002F9A60` - shared machinery across the layer boundary, no shared ownership.
- **Script_VM_Native_Bridge - CLIENT (47 edges).** `00203170`, `00265020` are also called by bodies filed to script VM / native bridge: `00356160`, `0033FD60`, `00344AF0` - shared machinery across the layer boundary, no shared ownership.
- **Status_Periodic_Terminal - CLIENT (1 edge).** `00379CD0` is also called by bodies filed to status/periodic terminal: `00386C70` - shared machinery across the layer boundary, no shared ownership.
- **Story_Event_Quest_Hunt - CLIENT (12 edges).** `002EF2B0` is also called by bodies filed to story/event: `0032A8A0`, `0032A930`, `0032A9A0` - shared machinery across the layer boundary, no shared ownership.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**UI — CLIENT (5 edges, one fan-in).** All 5 edges are UI bodies reaching `003148F0` on this page. `FUN_003c80c0` is the worked example - it is a 230-byte lazy creator: when `[02B476B0]` is empty it makes a **`0xC8`-byte** object around the `.text` callback `003C5910` and caches it there. `003C5910` interior read 2026-09-17 (SWE2-FRONTIER): 1,159 B — `002432B0` first at [`003C5959`](../../_index/ADDRESS-INDEX.md), `003C5720`/`002DD7E0`/`0029F5D0` ×2. The crossing is **one shared subject with 5 callers on that layer**, not 5 separate relationships. Edge count from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).

**Presentation — CLIENT (81 edges, one fan-in).** `00203170`, the field-side helper this page cites, is called across the presentation layer — `00245E60`, `00258350`, `002B7B80`, `002DB0xx` and the rest of the fan-in. One shared subject with many callers on that layer, not 81 separate relationships.

## The `002620E0` exclusive subtree — all 5 members bound (SWE2-FRONTIER, followup queue)

`002620E0` — the one-shot field-runtime init core §5 sketches — owns **5 frontier
functions**. Every member was disassembled from the shipping image; interior cites sit
inside each extent. The gate confirmed: `[manager+0x28]==0` (primary index) and
`[+0x10] & 4` clear, setting the bit only at `002621A4` after the whole chain runs. The
three `0026FAD0` posts each take `0017D490()` when positive else
`byte[002EF2B0()+0x1060]+1` — the debug-override-then-committed-slot pattern — against
channels `0`, `0x1F`, and the arg to `00379860`. Tail: `003601C0(0xB)` + `003601C0(0xC)`
event notifications.

| member | role | interior |
|---|---|---|
| `00379290` (53 B) | the env-object gate: when `[02ADD090]` is non-null, sets `byte[02ADD0E9]=1` and tails `0026E8D0(00265920())` — posting the current slot; when null, clears the flag and falls into `00379630` (the rebuild) | [`0037929E`](../../_index/ADDRESS-INDEX.md) |
| `00379630` (291 B) | the preset-handle rebuild: releases each nonzero handle in the `02ADD125` dword run (+ `02ADD11D`) via `003ABCA0`, posts `0026E8D0(00265920())`, then for `clamp([021A2CD0], 0, 3)` entries builds a 0x50-byte param record (`+0=0x1002001`, flag `&3|0x20`, 16-B vector from `021A2CE0[i]+0x20`, 16-B from `+0x00`) and registers each via `003AB960` into `02ADD125[i]`; tails `00379760` | [`003796EA`](../../_index/ADDRESS-INDEX.md) |
| `00379760` (249 B) | rebuilds handle `02ADD11C` from preset slot 0 (`0037AD10(0)`): scales the preset's `+0`/`+4`/`+8` floats by three rodata constants (or the `021A2D70` default when no preset), fills a 0x50 record (`+0=0x1042006`), registers via `003AB960`, releasing the prior handle | [`003797AE`](../../_index/ADDRESS-INDEX.md) |
| `00379860` (33 B) | one-line guard — runs the `00379F50` path only while `[02ADD090]` is non-null | [`00379868`](../../_index/ADDRESS-INDEX.md) |
| `0037AD10` (38 B) | the preset getter: `*out = 02C1F460 + idx×0x50` for `idx<5`, else NULL — a 5-entry `0x50`-stride weather-preset record table | [`0037AD18`](../../_index/ADDRESS-INDEX.md) |

`00259B30`, `003E8980`, `0025ACA0`, `0017D490`, `002EF2B0`, `0026FAD0`, `003DE920`,
`00363B40`, `003601C0`, `00265920`, `0026E8D0`, `003ABCA0`, `003AB960`, `00861EC0`,
`00379F50` and `00808C40` are shared callees with other callers — deliberately not census
members.

## SWE2-EC7-23 update (2026-09-18) — `003AB960` generation-handle slot claim

`003AB960` (506 B) is the registrar this page already names in the preset
rebuilds: scans `[02B3F528]` `0x70`-stride slots (up to `0x80`) for a free
`[rdx] == 0` entry, `inc byte[02B3F500]` claim count, `eax = [02B3F504]+1`
wrapped at `0xFFFFFF` (`cmova` to 1), stores `eax << 8 | slot` into the entry —
the generation-tagged handle format `00379630`/`00379760` register their
0x50-byte param records under. Interior anchor `003AB970` (the free-slot
scan).
## SWE2-EC7-31 update (2026-09-18) — `0024F610` bucketed record lookup

`0024F610` (50 B) is the lookup the weather tables feed: null `rcx`
returns 0; `byte[rcx]` indexes the `020910A0` bucket table, and the
`+8`-linked chain is walked for a node whose `word[+4]` equals
`word[rcx+4]` — the matching node or 0. A kind-indexed
chained-hash resolve on 8-byte nodes. Interior anchor `0024F630`
(the `word[+4]` compare).

## SWE2-EC7-40 update (2026-09-19) - `003C5720`

`003C5720` (391 B) is a weather body - `01CEBBA8`/`01F44830`, `00203170`/`00398C50`/`00202B70`/`00808C40`. Interior anchor `003C5803` (a `00203170` call).

## SWE2-EC7-50 update (2026-09-19) - `0026FAD0`

`0026FAD0` (182 B) is the EFB binding-channel post - `0024F680`/`0026F470`/`0036C140`/`0036C1D0`/`00808C40`. Interior anchor `0026FB12` (a `0024F680` call).

## SWE2-EC7-86 update (2026-09-20) - `003ED0B0` last-row field read measured

`003ED0B0` (40 B) is the terminal-row probe the weather and
mip-budget callers run: when `[02EBB7F0]` is live it reads
`dword[table + ([0209A6E8]-1)*0x180 + 4]` - the +4 field of the
count-minus-one row of the 0x180-stride table; a null table
returns -1.
Interior anchor `003ED0CF` (the `+4` field read).

## Two corrections from the S-12 contract (OPUS, 2026-09-21)

Both found by disassembling the bodies this page already names, while assembling
[`CONTRACT-weather.md`](../CONTRACT-weather.md). Filed as `CON-147` and `CON-148`.

**§2's account of the alternate resolver is wrong about when it draws (`CON-147`).** The page says
`0025ABA0` "draws MT19937 only when two remain". The **only** call to `00379CD0` in the 253-byte body
is at `0025ABB8`, inside the arm taken when the current slot is **2** — and it is taken *before* any
probability is read. `0025ABAA` subtracts one and dispatches three ways: current 1 to `0025AC5C`,
current 3 to `0025AC2B`, current 2 falling through. From slot 1 the order is `prob(2)` then
`prob(3)`; from slot 3 it is `prob(2)` then `prob(1)`. **Both are deterministic, and slot 2 always
wins when eligible** — including the "two remain" case this page says is randomised.

**And every arm falls back to the current slot.** `0025ABF0` and ~~`0025AC24`~~ `0025AC1D` *(corrected 2026-09-29, OPUS:
`0025AC24` is inside `0025AC20`'s instruction; the fallback is `setle cl` then `lea eax, [rcx+1]`)* yield 2, `0025AC88`
leaves `ebx` at 1, `0025AC47` leaves `edi` at 3. So `weatherProbability = {0, 0, 0}` **pins the
weather permanently** — the opposite of what "probability 0 → current slot cannot be retained"
implies.

**§2 and the F-2 answer overstate what the latch skips (`CON-148`).** `002620E0`'s init-bit test at
`002620F3` jumps to `002621A8`, **not** to the return. `002621A8` runs `003601C0(0x0B)` and
tail-jumps `003601C0(0x0C)` at `002621BC` — the same two event posts the full path reaches after
setting the bit at `002621A4`. Only the manager-index guard at `002620E6` reaches the bare return at
`002621C1`. The page's central claim is untouched — **the roll is one-shot and cannot be re-run** —
but a reimplementation reading "skips its whole body" would drop two event posts the shipped build
makes on every field-runtime pass.

`003C5130` (641 B) is the gather-emit pass `003C5120` and the lazy creator `003C5910` call: `02B45A70` zeroed, `0035D510` counts and `0035D500` returns the `02B45A80`-family table, then per row `dword[r13+i*4]` -> `0035D4F0`, `0031FE10` gates, `00265020` triple-outputs, the `02064AB0` vector stores into `rdi`, and `00263AA0`/`00263AB0`/`00263AC0`/`00263C20`/`00265200`/`00320C60`/`0037C860`/`003FFFF0`/`004000E0`/`00400550`/`00808C40` run the emit - the index table's per-row collect, whose far-end callers are CombatFormula- and Rewards-side crossings (named at subsystem level, not by address).

Interior anchor `003C515F` (function `003C5130`).

`004000E0` (165 B) is the mark-process-sweep `003C5130` runs: every `[rcx]`-rooted `+0x28` chain node gets `[+0x20] |= 2`, then `[rdx]` iterations of `00400AC0(rdi, rsi+0x10 + i*0x20, i)` process the table, a second pass clears bit 0 on nodes whose `(flags & 6) == 2`, and `[rdi+0x1410] |= 1` commits

Interior anchor `00400134` (function `004000E0`).

`00400AC0` (559 B) is the per-slot processor `004000E0` calls for each `0x20`-stride row: `[rcx]` bit `0x40000` bypasses the `003588B0`/`00234D40` count query (`r9d` stays 1), the `*rdi` `+0x28`-chain is scanned for `dword[+4] == [rbp+4]`, a hit clears flag bit 2 (re-arming bit `0x4` when `r9d == 2`) or splices the node beside the `esi`-indexed cursor with `00400650` unlink/relink; a miss runs the `+0x1411` modulo-0x40 round-robin to pick a free `+0x10`-block slot (`+0x20` bit 0 clear), `00275550` reclaims it, the node links at `[rdi+8]` tail with `+0x1412` bump and `+0x22 = 0x80`, `[rbp]`/`[rbp+0x10]` copy in as the payload, and `+0x24` gets `1.0f` when `+0x1410` bit 0 is clear

Interior anchor `00400C6B` (function `00400AC0`).

## Interior citations for the entry-cited functions (FABLE, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's disassembly pack and re-read by FABLE against the certified image; verified by [`interior_applier.py`](../../_index/candidates/fable-weather-probability-and-transition-roll-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `00234D40` | 91 B | makes the call at `00234D40` + 0x4 with the incoming `rcx`; returns 0 when that result is null or bit 0x10 of its first byte is clear; otherwise returns 2 when its qword `+0x698` is null, and when it is non-null returns 1 if (dword `+0x64` OR dword `+0x3C`) AND 0x80000003 is 0, else the call at `00234D40` + 0x33 on that qword decides: 1 when non-zero, 2 when zero | `00234D44`, `00234D55`, `00234D6C`, `00234D73`, `00234D93` |
| `00263AA0` | 14 B | returns the sign-extended byte `+0x21` of `rcx` when bit 0x40 of byte `+0xF` is set, else 0 | `00263AA4`, `00263AA6`, `00263AAB` |
| `00263AB0` | 14 B | returns the sign-extended byte `+0x22` of `rcx` when bit 0x40 of byte `+0xF` is set, else 0 | `00263AB4`, `00263AB6`, `00263ABB` |
| `00263AC0` | 118 B | returns 0 when `rcx` is null and byte `+0xF` of `rcx` when that byte is not 2; when it is 2, saves qword `02099D70`, stores the address `02098E10` in it, takes `003588B0` of the no-argument call at `00263AC0` + 0x36 (0 when that call returns 0), restores `02099D70`, and returns 1 when that result equals `rcx`, else 2 | `00263AD7`, `00263AEF`, `00263B01`, `00263B0D`, `00263B1E` |
| `00400550` | 132 B | returns without work when `edx` is non-zero; otherwise chains four calls `00400CF0(rcx, a, b, 0, previous result, 0)` with (a, b) = (5, 5), (8, 5), (3, 6), (4, 7), the first taking 0 as its previous result, and returns the last result | `00400552`, `00400576`, `00400590`, `004005AA`, `004005C4` |
| `00400650` | 69 B | unlinks node `rdx` from a doubly linked list with links at qwords `+0x28` and `+0x30`: when qword `+0x30` is non-null stores `rdx`'s `+0x28` into its `+0x28`, when qword `+0x28` is non-null stores `rdx`'s `+0x30` into its `+0x30`; then clears bit 0 of word `+0x20`, zeroes both links and returns `rcx`, or `rdx`'s old `+0x28` when `rcx` equals `rdx` | `00400653`, `00400669`, `0040067A`, `00400683`, `0040068D` |

## Homed bodies: functions reached only indirectly whose callees this page cites (FABLE, 2026-10-03, F homing)

*No page cited these functions and none of their callers is documented: they are reached by table or pointer dispatch or through undocumented callers. Each one calls something this page documents, which the sentence names. Each sentence states what the body does (access and representation, not purpose); the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's F homing pack and re-read by FABLE against the certified image; verified by [`interior_applier.py`](../../_index/candidates/fable-weather-probability-and-transition-roll-homing-1003/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `003597B0` | 31 B | calls `00234D40` with the incoming registers unchanged and returns 1 when it returns 2, otherwise 0 (including when it returns 1) | Interior anchor `003597B4`; Interior anchor `003597B9`; Interior anchor `003597BC`; Interior anchor `003597C1`; Interior anchor `003597C8` |
| `003597D0` | 46 B | calls `00234D40` with the incoming registers unchanged and returns 1 when it returns 1, 2 when it returns 2, otherwise 0 | Interior anchor `003597D4`; Interior anchor `003597DC`; Interior anchor `003597E1`; Interior anchor `003597EA`; Interior anchor `003597F4` |
