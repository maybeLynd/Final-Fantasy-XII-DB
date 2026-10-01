---
system: Weather Slot state model
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
  previous_parent: 381d2aea82b96d7af781844e191d9b92a37e93bd2d4ff276a33ba56e7307461b
  previous_snapshot: d2445517c66513976c83a446f87537a3c1d8c21f5bef033779affe98d7e61a20
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-02
audit:
  passes: 1
  last_pass: 2026-09-02
  last_pass_state: reverification-against-current-parent
  crossref_clean: true
  reopened_count: 1
---

# Weather Slot state model

> The durable "which weather is this area in right now" value, and the transition-policy
> byte that sits next to it and is repeatedly mistaken for part of it.

## 1. What the player sees

Every field area is in one of **three** weather configurations at a time. Walking into a
zone, saving and reloading, or a script event changing the weather all resolve to that one
value. It persists across save/load, and it is the thing that decides whether it is raining
on you — and, because weather feeds combat, whether your Fire spells are weaker right now.

The developer build exposes it directly with the on-screen debug line
`Weather Slot:%d (Triangle/Cross to toggle)`.

## 2. Native mechanism

There are exactly two persistent bytes, and they mean different things.

**`payload+0x1060` — the durable Weather Slot.** Zero-based `0..2`. Every runtime query
returns it as `1..3`. This is the real world state.

**`payload+0x1061` — `bInitializationRestoreState`.** A world-transition policy flag, *not*
a weather variable. When it is set, the next weather/environment apply **preserves** the
already-committed slot instead of taking the requested one, then clears the flag.

`payload` is the SaveImage persistent payload obtained through the existing
`SaveImage_GetPersistentPayloadBase` boundary (`002EF2B0`).

Reading the current slot (`00265920`):
1. if a positive developer override is active, return it;
2. otherwise return `signed(payload+0x1060) + 1`.

## 3. Key addresses

| Address | Working name | Body | Role |
|---|---|---:|---|
| `00265920` | `WorldField_GetCurrentWeatherSlot1To3WithDebugOverride` | 41 B | canonical getter, honours debug override |
| `0017D490` | `WorldField_GetDebugWeatherSlotOverride` | 20 B | returns `[debugSingleton+0xAAC]` |
| `002EF2B0` | `SaveImage_GetPersistentPayloadBase` | — | persistent payload boundary |
| `0026D8F0` | `WorldPersistence_MarkInitializationRestoreState` | 21 B | writes `payload+0x1061 = 1` |
| `00268320` | `WorldPersistence_ResetBanksAndMarkInitializationState` | 88 B | clears `scratch1` always and `scratch2` when `0209AC10 == 0` and `01E0C3EC != 0`; sets `+0x1061` when `0209AC10 == 0` (F-3) |
| `0026D910` | `WorldField_ApplyWeatherSlotAndDerivedEnvironmentState` | 418 B | the apply owner — consumes and clears `+0x1061` |

## 4. Data structures

```
SaveImage persistent payload
  +0x1060  s8   currentWeatherSlot            zero-based 0..2  (queried as 1..3)
  +0x1061  u8   bInitializationRestoreState   world-transition policy, NOT weather-owned

Debug/config singleton
  +0xAAC   s32  debugWeatherSlotOverride      positive value forces the slot
```

The authored/runtime domain is **1..3**. The persisted domain is **0..2**. Every crossing
between them is an explicit `+1` / `-1` in the native code — do not conflate them.

## 5. Call chain

```
world reset / transition path
  00280140 | 0036FCC0 | 00394130
     -> 00268320  (sets payload+0x1061 when dword 0209AC10 == 0; F-3)

authored runtime script
  0x021A setweatherslot(int)
     -> 003565C0  (ScriptVM handler)
        -> 0026D910(slot)      <- apply
        -> 0026D8F0()          <- arm restore state for the NEXT apply

field-runtime initialization
  0025D9E0 ActorManager_RunFieldRuntimePass
     -> 002620E0  (primary ActorManager only)
        -> 0025ACA0  (roll)
           -> 0026D910(finalSlot)
```

**Upstream (who causes this):** world transition/reset paths arm `+0x1061`; field
initialization and authored script both drive `0026D910`.

**Downstream (what this causes):** environment materialization, Presentation refresh,
CombatFormula environment class, field-resource selection. See
[`weather-apply-and-environment-materialization.md`](weather-apply-and-environment-materialization.md).

**Do not confuse with:** `debug_setlockweatherslot` (`0x209F`) maps to a *different* native
handler and state family. `+0x1061` is not the debug weather lock.

## 6. Modding notes

- **Best intervention point:** `0026D910(slot)` — the shared native apply owner for both the
  RNG transition path and authored `setweatherslot`. It commits the slot, materializes the
  authored environment record, and refreshes Presentation in one transaction.
- **Do not** write `payload+0x1060` directly. You will get the value without the
  environment materialization or the Presentation refresh.
- **Do not** invoke the ScriptVM wrapper `003565C0` as an API. VM wrappers are authored-intent
  evidence, not seams.
- **Regenerates itself:** everything downstream of the apply — environment parameters,
  Presentation backend state, Movement resource banks.
- **XIIOnline:** `payload+0x1060` is authoritative shared world state and belongs in world
  snapshots and late-join. `payload+0x1061` is transient local transition policy and must
  **not** be promoted to a durable networked weather field merely because Weather reads it.
  Reproducing an authored `setweatherslot` *event* may legitimately need both calls; ordinary
  weather synchronisation must not blindly send both.

## 7. What is not known

- [x] ~~Exact conditions under which `00268320` arms the restore state (open question **F-3**).~~ **F-3 ANSWERED
      2026-09-13 (FABLE, from ASTRA's spawn page §16 and a writer census):** `00268320` sets `+0x1061 = 1` exactly when a fresh read of dword `0209AC10` is zero (`0026835E`–`0026836C`) and never clears it; it clears `scratch2` (`02099FF0`) only when `0209AC10 == 0` **and** `01E0C3EC != 0` (`00268324`–`00268345`) and `scratch1` (`02099DF0`) always. Every RIP writer of the two globals: `0209AC10` — `1` in `SaveLoad_ControllerLifecycleHandler` (`00582E98`, just before `WorldTransitionSnapshot_RestorePersistencePairForActiveSlot`), `0` from `WorldTransition_StageFieldTransition` when the staged request is field `0xC` (`00314752`–`00314754` via the setter `00287D00`), and `0` from script verb `0x05BF`, whose handler `00355E80` tail-calls the same setter with `ecx = 0`; its only other reader is the `0x05BE` getter (`00286000` ← `00355940`). `01E0C3EC` — `1` in the image, `1` on the same field-`0xC` branch (`00314759`), `0` in `SaveLoad_NormalizeLoadedRuntimeStateAndReseedRNG` (`00584386`, `esi` = 0), which the controller reaches at `00582EBA`. So after the controller's restore path the next `00268320` keeps `scratch2` and leaves `+0x1061` alone, and after staging field `0xC` it wipes `scratch2` and arms `+0x1061`. Residue: whether the controller path and the reset run in that order in a real load, and what `0x05BE`/`0x05BF` do in authored scripts (ASTRA-REQ-FABLE-RESTORE-REQUEST).
- [x] ~~Whether a higher non-VM apply seam exists above `0026D910` (open question **D-3**).~~ **D-3 ANSWERED 2026-09-12 (FABLE): no runtime seam above it — only boot.** `WorldField_InitializeCurrentFieldRuntimeParameters` (`0026D910`) has exactly three call sites: the script verb **`setweatherslot`** (`0x021A`, thunk `003565C0`, [the verb table](../../01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-verb-table.tsv)) and two back-to-back native calls with argument 1 at `00266E74` / `00266E7B` inside `00266D10`, a 1,185-byte subsystem initialiser that the boot function `0022A0B0` ([what the engine fixes at boot](../../00-Engine-Core-Runtime/what-the-engine-fixes-at-boot.md)) runs once at `0022A3F7`. So at runtime every weather apply comes through the VM verb; the only higher non-VM seam is the boot pass, which primes the seam twice and never returns to it.
- [x] Thread/game-frame requirements for calling `0026D910` safely (open question **F-1**).
      *SUPERSEDED 2026-09-26 (FABLE, Claude Opus 5.5) under the runtime rule, because the static half is settled. Every in-image path to
      `0026D910` starts at one of three application entries on the main-loop thread: GameApplication's setup, its update
      slot (through `MainLoop_UpdateAndRenderFrame`), and the `setweatherslot` script verb. No thread procedure the image
      starts reaches any of them, and the path takes no lock. Control: `_index/candidates/f1-weather-apply-thread/f1_thread_reach.py` (3 checks). The blind spot is the
      handshake page's: indirect thread starts. The receiver-safe live call the row asks for is not queued.*

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| `+0xAAC` is the Weather Slot debug override | authored format string `%s%s %d %s, Weather Slot:%d (Triangle/Cross to toggle)` with `[singleton+0xAAC]` in the matching integer position | 2 |
| `+0x1060` is the durable zero-based slot | complete body of `00265920` (41 B, `e9bd7451…6843`) and `0026D910` (418 B, `1703f5dc…b4d2`) | 1 |
| `+0x1061` is `bInitializationRestoreState`, not weather-owned | complete body of `00268320` (88 B, `b209df73…0bef`) plus its three non-Weather callers `00280140`, `0036FCC0`, `00394130` | 1 |
| Slot domain is 1..3 authored / 0..2 persisted | explicit conversions in `00265920` and `0026D910` | 1 |
| `setweatherslot` maps to `003565C0` | ff12-script catalog `{ 0x021a, setweatherslot, 1 arg, PRM_TYPE_INT }` + executable dispatch table | 9 |

**Superseded readings:**
- *Old:* `+0x1061` is a narrowly Weather-owned "preserve weather on next apply" latch, and
  `0026D8F0` is `WorldField_SetPreserveCurrentWeatherSlotOnNextApply`.
  *New:* it is broader world-transition initialization/restore state that Weather merely
  consumes. Corrected by canonical V31/V40 evidence for `00268320`. The *effect* inside
  `0026D910` is still one-shot slot preservation — but the flag is not Weather's.

## 9. Related

- [`weather-probability-and-transition-roll.md`](weather-probability-and-transition-roll.md) — how the slot is chosen
- [`weather-apply-and-environment-materialization.md`](weather-apply-and-environment-materialization.md) — what the apply does
- [`mweather-resource-format.md`](mweather-resource-format.md) — the authored record the slot indexes
- [`../../08-Combat-Formula/Weather-Terrain-Element-Scaling/`](../../08-Combat-Formula/Weather-Terrain-Element-Scaling/) — gameplay consequence

## Re-verification 2026-09-02 (AH-4)

Stamped against parent `381d2aea...`; re-checked against the current `2ed8affb...`.

**Addresses:** 13 cited, **13 resolve as function entries**, 0 unresolved.

**Central claim re-derived.** The headline is *"the durable 'which weather is this area in right now'
value, and the transition-policy byte that sits next to it and is repeatedly mistaken for part of
it."*

`WorldField_InitializeCurrentFieldRuntimeParameters` (`0026D910`) shows exactly that relationship:

```c
if (*(char *)(payload + 0x1061) == '\0') {       // the policy byte GATES the write
    *(char *)(payload + 0x1060) = (char)value;   // the durable slot value
    ...
}
...
*(undefined1 *)(payload + 0x1061) = 0;           // policy cleared afterwards
```

Two adjacent bytes with different lifetimes: `+0x1060` is the durable value, `+0x1061` is a
transition-policy flag that gates the write and is then cleared. That is the document's claim,
confirmed - and it also explains why the two are easily conflated.

Both offsets are independently present in the save payload map, derived from a census of
`SaveImage_GetPersistentPayloadBase` callers.

**Stamp advanced because the bodies were re-read**, per the evidence standard.

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

`00280140` carries no `PrimaryOwner`; the audit labels it from its `CodeDomain`, whose family head
is **`SaveLoad`** — a different taxonomy from the owner vocabulary (`Save_Load_Settings`) used
everywhere else. Both name the same subsystem.
- **CombatAI - SERVICE (1 edge).** `00233C10` reaches bodies filed to combat AI: `00327F80` - shared machinery across the layer boundary, no shared ownership.
- **CombatFormula - SERVICE (1 edge).** `00237DF0` reaches bodies filed to combat formula: `0023AC80` - shared machinery across the layer boundary, no shared ownership.
- **Gameplay - CLIENT and SERVICE (4 edges).** `002FA230`, `002FA260` are also called by bodies filed to Gameplay: `00237DF0` (Combat); `00233C10`, `0025D9E0` reach bodies filed to Gameplay: `00237DF0` (Combat), `00234150` (CombatAction) - shared machinery across the layer boundary, no shared ownership.
- **Items_Equipment_Shops_License - SERVICE (2 edges).** `00233C10`, `00237DF0` reach bodies filed to items/equipment: `0030B6A0`, `0023AF50` - shared machinery across the layer boundary, no shared ownership.
- **Movement - SERVICE (7 edges).** `0025D9E0`, `00266D10` reach bodies filed to movement: `0025DF00`, `00263560`, `002EBE40` - shared machinery across the layer boundary, no shared ownership.
- **Presentation - SERVICE (8 edges).** `0022A0B0`, `002620E0`, `00266D10` reach bodies filed to presentation: `0036FFF0`, `0037CCC0`, `00259B30` (CameraSystem) - shared machinery across the layer boundary, no shared ownership.
- **Resource - CLIENT (10 edges).** `0017D280` is also called by bodies filed to resource: `0017D9D0`, `001B14E0`, `001F4340` - shared machinery across the layer boundary, no shared ownership.
- **Script_VM_Native_Bridge - CLIENT (38 edges).** `0017D280` is also called by bodies filed to script VM / native bridge: `0050C670`, `0050C8D0`, `0050C990` - shared machinery across the layer boundary, no shared ownership.
- **Story_Event_Quest_Hunt - CLIENT (12 edges).** `002EF2B0` is also called by bodies filed to story/event: `0032A8A0`, `0032A930`, `0032A9A0` - shared machinery across the layer boundary, no shared ownership.
- **UI - CLIENT and SERVICE (7 edges).** `003148F0` is also called by bodies filed to UI: `0029C530`, `003C5F00`; `00237DF0`, `002678C0` reach bodies filed to UI: `00313840`, `002509A0` - shared machinery across the layer boundary, no shared ownership.

## 10. The transition contract — `0026D910` read end to end (2026-09-10)

§3 names `WorldField_ApplyWeatherSlotAndDerivedEnvironmentState` the apply owner and §6 calls it the
best intervention point, but its own ordering was never written down. Here it is, as the contract a
reimplementation has to satisfy.

```c
void WorldField_ApplyWeatherSlotAndDerivedEnvironmentState(int slot)   /* 0026D910, 418 B */
{
    if (WorldField_GetDebugWeatherSlotOverride() > 0)          /* 0026D921 */
        slot = WorldField_GetDebugWeatherSlotOverride();       /* 0026D92A - called AGAIN */

    slot -= 1;                                                 /* 0026D933: 1-based in */
    slot  = (slot < 0) ? 0 : (slot > 2 ? 2 : slot);            /* saturating, never fails */

    *(int*)0x02099DBC = 0;                                     /* 0026D946, before anything else */

    if (payload[0x1061] == 0)                                  /* 0026D951 - the policy gate */
        payload[0x1060] = (int8)slot;                          /* 0026D95E - COMMIT */
    /* else: the requested slot is DISCARDED and the committed one kept */

    ... derive from (int8)payload[0x1060], re-read at 0026D96F and 0026D9BB ...

    payload[0x1061] = 0;                                       /* 0026DA92 - every path */
    return 002E3D40(0, 0, 0, 0);                               /* 0026DAAD - a TAIL JUMP */
}
```

**Five things that only fall out of reading it.**

**The argument is one-based and the clamp saturates.** `setweatherslot(0)` and `setweatherslot(1)`
both select slot 0; anything of 4 or more selects slot 2. **An out-of-range request never fails and
never reports** — it silently becomes the nearest valid slot. A mod passing a bad value gets weather,
not an error.

**The debug override is read twice, not cached.** `0017D490` is called at `0026D921` to test and
again at `0026D92A` to take the value. It is a 20-byte accessor over a single field, so the two
reads agree in practice — but the *shape* is a double read, and a reimplementation that caches it
has changed the call pattern even where the result is identical.

**The policy gate discards, it does not defer.** When `+0x1061` is set the requested slot is thrown
away — there is no queue and no retry. The caller cannot tell: the function returns the same way
either way.

**The derive re-reads the payload rather than using the local.** `0026D96F` and `0026D9BB` both load
`payload[0x1060]` again instead of reusing the clamped argument, which is exactly what makes the
gated path correct — when the commit was skipped, the environment is derived from the **kept** slot,
not the requested one. A reimplementation that passed its local `slot` through would materialise the
wrong environment on every restore.

**`+0x1061` is cleared unconditionally, on every path.** `0026DA92` sits on the common tail that the
resource-lookup bail-outs at `0026DA83` also reach. So the flag is consumed exactly once per apply
whether or not anything was found — §3's *"consumes and clears"* is confirmed and is stronger than
it sounds.

### What it does not touch

`+0x1062` and `+0x1063` — the save-override cluster four bytes away — are **not** read or written
here. The two clusters are adjacent in the payload and independent in behaviour.

### Limits

- **The derive half is cited, not decoded.** `00180620`, `003148F0` and the `*(02099D88)` resource
  walk belong to [the mweather format](mweather-resource-format.md) and
  [the apply page](weather-apply-and-environment-materialization.md); this contract stops at "it
  re-reads the committed slot and hands off".
- **The tail jump to `002E3D40` means this function has no return value of its own** — whatever the
  materialiser returns is what the caller sees. Nothing here establishes what that is.
- `02099DBC` is cleared first and nothing here reads it back; what it means is not established.
- Static only. §"Re-verification 2026-09-02" covers the live side of the slot state, not this
  ordering.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited.*

**Input — CLIENT of the initialisers, not a weather dependency.**

- The boot initialiser `0022A0B0` calls a 119-byte Input-filed initialiser. It stores into `02EC0B81`
  ([what the engine fixes at boot](../../00-Engine-Core-Runtime/what-the-engine-fixes-at-boot.md)).
- The area initialiser `00266D10` calls a 1,936-byte Input-filed body. That body reaches the actor manager, the party
  focus handle and the registry resolver, and it is unread
  ([the shared neighbours page](../../00-Engine-Core-Runtime/Shared-State-Accessors/the-shared-neighbours-pass-22-keeps-finding.md)).

Neither reads the weather slots.


## SWE2-EC7-66 update (2026-09-19) - `0036FCC0`

`0036FCC0` (130 B) is a weather-slot row body - `0016D6A0`/`0017D280`/`00233C10`/`002678C0`/`00267C90`/`00268320` plus `00D10FD0`-`00D11040`. Interior anchor `0036FCCB` (a `0017D280` call).


**CombatAI and Items_Equipment_Shops_License — CLIENT (SWE2-EC7 2026-09-19, 2 edges).** `00233C10`, a
callee this page's `0036FCC0` section cites, is also called by the CombatAI-filed `00327F80` and the
Items-filed `0030B6A0`. Both callers are mechanical users of the same shared helper.

## SWE2-EC7-96 update (2026-09-20) - `002FA260` measured

`002FA260` (44 B) is the six-field clear `00233C10` and
`00237DF0` run: five qwords plus a trailing dword at
`02BE3E60`..`02BE3E8C` are zeroed outright - the fixed-shape
reset the slot model applies on reinit.
Interior anchor `002FA269` (the second qword clear).

## SWE2-EC7-97 update (2026-09-20) - `002FA230` measured

`002FA230` (44 B) is the second six-field clear `00233C10` and
`00237DF0` run alongside `002FA260`: five qwords plus a trailing
dword at `02EC3EA0`..`02EC3EC8` are zeroed outright - the twin
reset to `002FA260`'s `02BE3E60` block, same shape, different
slot array.
Interior anchor `002FA239` (the second qword clear).

## §10's "the derive re-reads the payload" holds for three published values and not for the fourth (OPUS, 2026-09-21)

Found while assembling [`CONTRACT-weather.md`](../CONTRACT-weather.md); the divergence is registered
as `GB-1` and the contract's invariant I-7.

§10 argues, correctly, that `0026D96F` and `0026D9BB` re-read `payload[0x1060]` instead of reusing
the clamped argument, "which is exactly what makes the gated path correct", and warns that "a
reimplementation that passed its local `slot` through would materialise the wrong environment on
every restore."

**One published value does pass the local through, and it is the gameplay one.** At `0026DA2C`–
`0026DA31` the MWeather preset that becomes `02099DAC` is taken with `edx = edi + 1`, and `edi` is
the clamped **requested** slot, unmodified since `0026D943`. Every other published value —
`00180620`'s environment bank, `02099DA8`, `02099DB0`, `02099DBC` — is derived from the re-read
committed slot, and the presentation path reached by the tail jump uses `00265920()`, also the
committed slot.

So on the restore path the function materialises the **kept** slot's environment and the
**requested** slot's combat weather, in the same call. §10's warning stands for the derive half it
was written about; the qualification is that the function itself already does the thing §10 warns
against, in exactly one place.
