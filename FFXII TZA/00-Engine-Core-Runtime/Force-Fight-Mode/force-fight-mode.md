---
system: Force fight mode
category: 00-Engine-Core-Runtime
status: AUDITED
owner_layer: none — one global, set by the script VM, read by five subsystems
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
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-02
audit:
  passes: 1
  last_pass: 2026-09-02
  last_pass_state: falsification-pass
  crossref_clean: true
  reopened_count: 0
---

# Force fight mode

> One global flag, named by the game's own script vocabulary, that a cutscene can raise — and that
> changes what units may do, how they move, and how the party stands.

**DOCUMENTED.** The flag, both its readers, its setter, its feature enable, the script verb that
drives it, and its fifteen consumers are all read. What each consumer *does* with it is documented
elsewhere or open.

## 1. What the player sees

Some fights in FFXII are not optional in the ordinary way. A script raises this flag and the party's
behaviour changes underneath the player — which actions are offered, how units close distance, and
how the party holds its stance.

The engine's own name for it is **`setforcefightmode`**. That is the script verb; it is not a
reconstruction.

**The player also has a button on it, and its off state has a name on screen.** R2
([the R2 toggle](../../15-Input/Modal-Toggles/r2-force-fight-toggle.md)) clears this flag, and while
it is clear the HUD shows **`FLEEING`** ([`EXP-025`](../../_experiments/EXP-025-r2-visual-toggle.md),
2026-09-10: one press → `FLEEING` with the flag `0`, a second press → gone with the flag `1`). So
"force fight mode on" is the ordinary state in which the party fights, and the script verb's job
is to deny the player the fleeing state. What fleeing changes beyond the label — enemy pursuit,
command availability — is the consumer census below, not that observation.

## 2. Native mechanism

### The flag and its predicate

```
01E0C2B8      dword      the force-fight-mode flag

00253B90:     return *(int *)0x01E0C2B8 == 0;      /* 12 bytes, whole body */
```

**Note the polarity: the predicate is TRUE when force fight mode is OFF.** Every consumer below
tests it that way round, so a reading of "this gate fires during forced fights" is exactly backwards.

### It is set by a script verb, and the binding is verified

The flag has **four write sites in two functions**, and the only one that takes an argument is:

```c
int FUN_00254EA0(int enable)          /* 54 bytes, whole body */
{
    if (enable && FUN_003BA2E0()) { *(int *)0x01E0C2B8 = 1; return 1; }
    *(int *)0x01E0C2B8 = 0;  return 0;
}
```

That setter has **exactly one caller**: `FUN_003444D0`, owned by **Script/VM Native Bridge**. In the
dispatch table that function is:

| call id | verb | args | handler |
|---|---|---:|---|
| `0x0334` | **`setforcefightmode`** | 1 | `003444D0` |

**Arity-verified**, as the dispatch-table document requires before a row counts as fact: the handler
is 23 bytes and contains **exactly one** `VMValueStack_PopInt32CoerceFloat32`, matching the catalog's
one argument.

### `FUN_003BA2E0` is a feature enable, not just a setter veto

`FUN_003BA2E0` must return nonzero before the flag goes to 1, so a script asking for force fight mode
can be refused; clearing is unconditional. But it is **not only** a setter guard — see section 8,
which reads it and finds it gates a second reader too.

```c
int FUN_003BA2E0(void)                /* 27 bytes, whole body */
{
    return (*(u8 *)0x02B4053C != 0 && *(u8 *)0x02B4053D != 0) ? 1 : 0;
}
```

**Two adjacent byte globals, both required.** What they are is answered in §5 (**AN-1**, 2026-09-17): the script-side “fight status by event” enable and a boot-set companion, neither cleared in the shipped game.

### Fifteen consumers

`00253B90` has **7 direct call sites**, plus a jump thunk (`thunk_FUN_00253b90`, `0030C0D0`) called
from **8 more** — **15 in total**. Named consumers:

| Consumer | What it gates |
|---|---|
| `BattleAction_CheckActionAvailabilityReason` (`002FFCF0`) | reason **`0x24`** — refuses every action except ids `0x113` and `0x95` |
| `FUN_00313A00` | the **capability policy**'s row-2 bit 1 |
| `BattleLocomotion_ComputeStepDistance` (via the thunk) | selects the movement divisor: `÷1.5` vs `÷3`, `×0.25` vs `÷5` |
| `BattleUnit_ComputePartyBattleStance` | party stance |
| `BattleUnit_UpdateEngagementStateFlag` | engagement state |
| `BattleRuntime_GetModeDependentDistanceThreshold` | a distance threshold |
| `BattleUnit_UpdateCombatFrame`, `FUN_0030C010` | unread *(answered: see AN-4, ANSWERED 2026-09-12 (FABLE); 2026-10-02, OPUS)* |

**Three separately documented systems already branch on this one flag** — action availability, the
capability-inhibition policy, and battle locomotion — which is why it kept reappearing before it was
named.

### The most consequential gate

In the availability cascade the flag participates in a very sharp rule:

```c
if (raw[5] == 0
    && ((raw[0x64] | raw[0x3C]) & 0x08000020) == 0
    && force_fight_is_OFF()
    && actionId != 0x113 && actionId != 0x95)      return 0x24;
```

So for one class of unit, with those status bits clear, **outside force fight mode only two action
ids are permitted at all**. Whatever `0x113` and `0x95` are, they are the exceptions the engine keeps
available when everything else is shut down.

## 3. Key addresses

| Address | Role |
|---|---|
| `0x01E0C2B8` | the flag |
| `00253B90` | `flag == 0` predicate — 12 B, 15 consumers |
| `00253BA0` | **effective-value reader** — `enable ? flag : 0`; 27 B, **2 UI callers** |
| `00254EA0` | the setter, with veto — 54 B |
| `003BA2E0` | **feature enable** — two adjacent bytes `0x02B4053C` / `0x02B4053D` both non-zero; 27 B, 3 callers |
| `003444D0` | `setforcefightmode` handler, script call id `0x0334` |
| `00252C80` | the second writer — 134 B, unread *(answered: see AN-2, answered 2026-09-11; 2026-10-02, OPUS)* |
| `0030C0D0` | `thunk_FUN_00253b90` — the jump thunk, 8 callers |

## 4. Modding notes

- **The verb is `setforcefightmode(1|0)`**, call id `0x0334`. It is ordinary script vocabulary; any
  zone script can raise or clear it.
- **Raising it can fail.** `FUN_003BA2E0` must agree; clearing always succeeds. That same
  function is a **feature enable**, not just a setter guard — it also gates the UI-side
  reader, while the 15 gameplay consumers read the flag raw (section 8).
- **Mind the polarity.** `00253B90` returns true when the mode is **off**. Reading it backwards
  inverts every gate above.
- **It is global, not per-unit.** One flag governs the whole battle.
- **XIIOnline:** it is set by script and read by action availability, movement and stance. Two clients
  whose scripts diverge will disagree about what actions are legal *and* how fast units close. It is
  a one-dword authoritative state — cheap and important to synchronise.

## 5. What is not known

- [x] ~~What `FUN_003BA2E0` tests.~~ **PARTLY ANSWERED 2026-09-02** — it requires **two adjacent byte
      globals**, `0x02B4053C` and `0x02B4053D`, to both be non-zero. ~~What those two bytes are is
      open.~~ It has 3 callers image-wide. **AN-1.**
      ***ANSWERED 2026-09-17 (FABLE): the two bytes are the script-side “fight status by event” enable and its boot-set companion, and in the shipped game neither is ever cleared.** `02B4053C` has three writers, all through the seven-byte setter `003BA300(cl)`: the boot initialiser `00266D10` stores 1 (`00266E42`..`00266E49`), the manager-slot unload `002628B0` stores 1 again on every area unload (`esi` = 1 from `002628E4`, the call at `00262C29`), and the script verb `debug_setfightstatusbyevent` (id `0x206B`, adapter `0050C910`) stores the one int it pops. `02B4053D` has one writer, the sister setter `003BA310(cl)`, called once, from the same boot sequence with 1 (`00266E4E`..`00266E50`); nothing clears it. So the pair reads as a script-controlled event veto of force fight (the verb's own name) over a boot-time enable, both defaulting on, with the veto reset to on whenever an area unloads. The verb is unused: all 1,115 `us` event containers were decompiled with ff12-script (1,114 succeeded) and none names `debug_setfightstatusbyevent`, while the controls `setnpcname` (549 files) and the other `debug_` verbs (109 files) appear as expected. In the shipped game, then, `003BA2E0` is true from boot onward and the enable is a debug hook. Static reading plus a corpus census; nothing executed.*
- [x] ~~Whether the flag can be `1` while `FUN_003BA2E0` is false — a state in which gameplay would act
      on force fight mode while the UI reported it off. The setter cannot produce it; the unread
      second writer `FUN_00252C80` might.~~ **AN-5** — answered by
      [the R2 toggle](../../15-Input/Modal-Toggles/r2-force-fight-toggle.md) §2f (propagated
      2026-09-11): the second writer's final store is `enable ? 1 : 0` too; the only `1`-with-enable-false
      window is inside its own call to `003BA2E0`, unobservable on this thread.
- [x] ~~What `FUN_00252C80` (134 B) does with the flag — the second writer, which also reads the prior
      value and stores a computed one.~~ **AN-2** — answered by the same page's §2e (propagated
      2026-09-11): `state == 0` sets the flag to the enable, `state != 0` clears it, and an unchanged
      value is not rewritten unless forced; the state it receives is the R2 toggle's engaged bit.
- [x] ~~What action ids `0x113` and `0x95` are — the two the availability cascade exempts.
      (Also **AI-2**.)~~ **AN-3 ANSWERED 2026-09-11:** Dismiss and Dismount ([the battle text banks](../../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/battle-text-banks.md), bank 0).
- [x] ~~What `BattleUnit_UpdateCombatFrame` and `FUN_0030C010` do with it.~~ **AN-4 ANSWERED
      2026-09-12 (FABLE): both gate the combo continuation on the mode.** In
      `BattleUnit_UpdateCombatFrame` (`00308768`–`003087A6`), after the action-state advance, a unit
      whose merged status has neither **Confuse** (5) nor **Berserk** (27) consults `00253B90` and,
      with force fight **off**, skips; with force fight on — or under either status — it requires the
      target buffer non-empty with entry 0's outcome bit 10 (*the combo continues*, `+0x788`) and
      calls `BattleAction_TryContinueComboSequence` (`0030FA00`). That function's first call is
      `FUN_0030C010(unit)` (`0030FA20`; its other caller is `0031ADB0`), which repeats the
      status-or-force-fight gate (`0030C020`–`0030C035`) and then answers *may the combo continue*:
      entry 0's bit 10 (`0030C045`), unit flag bit 22 clear (`0030C053`), the focus target `+0x710`
      resolves with a stats record whose status has none of `0x80000003` unless the field's bit 15
      permits (`0030C05A`–`0030C08A`), when the battle-state word `02089340` has bit 0 the unit's `+8`
      handle must equal the global at `0208E6A4` (`0030C08C`–`0030C09F`), and the special-sequence
      state `022C2160` must be 0 or 7 (`0030C0A1`–`0030C0AE`). So outside force-fight mode a party
      unit chains combo hits only while Confused or Berserk; the mode lifts that restriction.
      *Not read:* the identity of the `0208E6A4` handle and what `0031ADB0` does with the answer.
      **AN-4.**

## 6. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| The predicate is `*(int *)0x01E0C2B8 == 0` | complete 12-byte body of `00253B90`, RIP target machine-resolved | 1 |
| Four writes in two functions | full-image scan for RIP references to the global | 1 |
| The setter vetoes on `FUN_003BA2E0` | complete 54-byte body of `00254EA0` | 1 |
| The setter's only caller is `FUN_003444D0` | caller census over `edges.tsv` | 1 |
| `FUN_003444D0` is `setforcefightmode`, id `0x0334`, 1 arg | `scriptvm_dispatch.tsv` | 2 |
| …and the binding is **arity-verified** | the 23-byte handler contains exactly one `VMValueStack_PopInt32CoerceFloat32`, matching the catalog's 1 argument | 1 |
| 15 consumers | `.text` byte scan: 7 `E8` sites on `00253B90`, plus 8 on its `E9` thunk | 1 |

**Scope honesty:** this document establishes what the flag **is** and **who reads it**. What most
consumers do with it is either documented in their own systems or listed as unknown above.

## 7. Related

- [`../../15-Input/Gameplay-Capability-Policy/capability-inhibition-policy.md`](../../15-Input/Gameplay-Capability-Policy/capability-inhibition-policy.md) — closes its open question **C-5**, the meaning of `01E0C2B8`
- [`../../07-Combat-Action/Action-Availability/battle-command-availability-and-reason-codes.md`](../../07-Combat-Action/Action-Availability/battle-command-availability-and-reason-codes.md) — the `0x24` refusal this flag gates
- [`../../06-Movement-And-Navigation/Battle-Locomotion/battle-locomotion-steering-and-recovery.md`](../../06-Movement-And-Navigation/Battle-Locomotion/battle-locomotion-steering-and-recovery.md) — the movement divisor it selects
- [`../../01-Script-VM-Native-Bridge/scriptvm-native-dispatch-table.md`](../../01-Script-VM-Native-Bridge/scriptvm-native-dispatch-table.md) — the table the verb binding comes from, and the arity rule applied here
- [`../Battle-Runtime-Mode/battle-runtime-mode-ladder.md`](../Battle-Runtime-Mode/battle-runtime-mode-ladder.md) — another runtime state set by script verbs, found the same way

## 8. Falsification pass 2026-09-02

**Attack chosen.** The document was written in the previous tick and rests on three countable
claims — a 15-consumer census, a polarity, and a script-verb binding — plus one structural claim
about `FUN_003BA2E0`. All four were re-tested. Three survive; the fourth was incomplete.

### SURVIVED: the census, recounted independently

```
00253B90        7 direct E8 sites,  1 E9 thunk
thunk 0030C0D0  8 direct E8 sites
                                    total 15
```

Exactly as published. **And the thunk's callers are informative**: seven of the eight are
**Movement** (`BattleLocomotion_ComputeStepDistance` alone accounts for three), the eighth is
`BattleSystem_RunFieldFrameOrchestrator` (WorldAreaField). The thunk is effectively **Movement's
access path to the flag** — which is why an edge-list census of `00253B90` never showed the movement
consumers.

### SURVIVED: polarity and the verb binding

`xor eax, eax ; cmp [01E0C2B8], eax ; sete al` — the predicate is `flag == 0`, true when the mode is
**off**. The `setforcefightmode` binding and its one-pop arity check reproduce unchanged.

### CORRECTED: `FUN_003BA2E0` is a feature enable, not a setter veto

The document called it "the veto gate" and described it only as guarding the setter. It also guards a
**second reader**:

```c
int FUN_00253BA0(void)                /* 27 bytes, whole body */
{
    return FUN_003BA2E0() ? *(int *)0x01E0C2B8 : 0;
}
```

So there are **two readers with different semantics**:

| reader | returns | consumers |
|---|---|---|
| `00253B90` | the **raw** flag, as `flag == 0` | **15**, all gameplay — combat, movement, capability |
| `00253BA0` | the **effective** flag, `enable ? flag : 0` | **2**, both **UI** (`00276650`, `00276D30`) |

**Gameplay reads the raw flag; UI and the setter respect the enable.** That asymmetry is worth
stating plainly: if `FUN_003BA2E0` is false while the flag is somehow already 1, gameplay would still
behave as though force fight mode were on while the UI would report it off. Whether that state is
reachable is not established — the setter cannot produce it, but `FUN_00252C80` (the second writer,
still unread) is not so constrained. **AN-5.** *(Answered since — `AN-5`: the state is not reachable through
`00252C80` either; §5's struck item and [the R2 toggle page](../../15-Input/Modal-Toggles/r2-force-fight-toggle.md) §2f.)*

### AN-1 partly answered

*Answered 2026-09-17 (FABLE): see §5's closed box; the two bytes are the `debug_setfightstatusbyevent` enable (`02B4053C`, reset to 1 at boot and at every area unload) and its boot-set companion (`02B4053D`), and the verb occurs in none of the 1,115 `us` event containers.*

`FUN_003BA2E0` is 27 bytes and reads two **adjacent byte globals**, `0x02B4053C` and `0x02B4053D`,
requiring **both** non-zero. What they are remains open *(answered: see AN-1, ANSWERED 2026-09-17 (FABLE); 2026-10-02, OPUS)*, but the shape — two adjacent bytes acting as
one enable — is now known, and it has only **3 callers** image-wide.

### Not changed

The flag, the setter, the verb binding, the arity verification, the 15-consumer figure and the
`0x24` availability gate all stand as written.

## Interior citations — entry-only-large pass (2026-09-14, SWE2-FRONTIER)

This page named `00276D30` only at its entry. The interior addresses below were read in the
shipping image.

| body | interior cite | what is there |
|---|---|---|
| `00276D30` | `0027768A` | `mov dword ptr [rip+…], eax` — writes `0208F570`, the shared mode-state field this page's §5 documents |
| `00276D30` | `00276DE6` | `call 00245000` then `00244960` — the accessor pair that opens the body's work phase after `00247570` |

*(Pass 22 adjacency, 2026-09-14: force-fight state is read from outside the mode's own layer —
`00244960`, the accessor half of the open-work pair, is called by four **save** writers
`0057E4D0`/`005819F0`/`00582860`/`005823B0` (the mode persists into save payloads);
presentation `00308130` calls `00253B90`; and `0031ADB0` calls **actor** bodies `00263E30`/
`003588B0`/`003589B0`/`00265020` — 9 edges. A mode that must be serialised, displayed and
applied to actors has callers in all three layers.)*

*(Pass 22 live-graph completion, 2026-09-15: `00265020`'s reader population continues into
`Spawn_Encounter_Lifecycle` (`00234AF0`, `002350C0`, `00234DA0`, 3), `Rewards_Progression_
Economy` (`002FB150`, `00312280`, 2) and `Audio` (`00362850`, 1). ~~The force-fight getter is~~
~~read wherever the mode matters — spawn, rewards, audio — which is what a mode flag is for.~~ These readers fetch an actor's position, not the mode *(corrected 2026-10-02, OPUS: `00265020` is the actor world-position getter: it copies three dwords from `[actor+0xB8]` to its three out pointers, `00265020+0x1A`–`+0x2E`; the force-fight flag reader is `00253B90`, `[01E0C2B8] == 0`).)*

*(Pass 22 live-graph sweep 2, 2026-09-15: two more of the getter population's own neighbours
— `00312280` calls `Platform_Online_Achievements` `00316A50`, and `00234AF0` calls
`RNG_Random_Selection` `00328370` (2 edges). The rewards and spawn callers carry their own
callees with them.)*

## Crossings into other layers — FINAL-AUDIT pass 22 (OPUS, 2026-09-18)

**Resource — this page is the CALLER.** `002628B0` calls `0032E520` at **three** sites —
`00262AF2`, `00262B0D`, `00262B1E`. The callee is 107 bytes and refuses a zero argument before
doing anything (`0032E524`–`0032E526`), so each of the three is a guarded request. **This page
consults the resource layer and owns nothing in it.**

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**CombatAI — CLIENT.** `AiOrder_CheckActionPreconditions`, owned by that layer, calls `00308130` on this page. That caller is the precondition check: a `0x650`-byte frame with a stack cookie into which it copies **twelve `0x80`-byte blocks** from the unit's `+0x80` before testing the order's `word[+0]` and signed `word[+2]`; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**CombatFormula — CLIENT.** `BattleStats_ResolveByActorHandle`, owned by that layer, calls `00263E30` on this page. That caller is a 55-byte resolver behind the same `byte[02089340] & 0x10` gate as the focus-handle pair: it takes the handle through `003588B0` and `00263E30` and returns the resulting unit's `+0x698` **stats record** rather than the unit itself; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).
- **Audio — CLIENT and SERVICE (13 edges).** 2 inbound (Audio bodies `00362850`, `00363560` call page-cited `Actor_GetWorldPosition` (00265020), `00362850`); 11 outbound (page-cited `00362850`, `002628B0`, `00266D10` call Audio bodies `00360B50`, `003636A0`, `00360DD0`). Substantive edges include `002628B0` calls `00360B50`; `002628B0` calls `003636A0`; `002628B0` calls `00360DD0`; `00266D10` calls `00362F70`; the remaining edges run through shared helpers the page cites.
- **Combat — MECHANICAL (1 edge).** 1 Combat-side calls into shared helper(s) the page cites (`ActorWork_GetBattleUnitRaw` (00263E30)) - the helpers' general call surface, not a Combat relationship of this page's subjects.
- **CombatAction — CLIENT and SERVICE (26 edges).** 19 inbound (CombatAction bodies `BattleAction_CheckActionAvailabilityReason` (002FFCF0), `BattleUnit_HandleActionTimelineEvent` (00325260), `BattleUnit_HandleActorTimelineEvent` (00319F50) call page-cited `ActorWork_GetBattleUnitRaw` (00263E30), `BattleAction_CheckActionAvailabilityReason` (002FFCF0), `Actor_GetWorldPosition` (00265020)); 7 outbound (page-cited `BattleAction_CheckActionAvailabilityReason` (002FFCF0), `BattleAction_TryContinueComboSequence` (0030FA00), `0031ADB0` call CombatAction bodies `0030C010`, `BattleAction_CheckExecutionResourceAvailability` (00303BD0), `BattleAction_CheckUnitActionAvailability` (00306480)). Substantive edges include `00253B90` is called by `0030C010`; `0030C010` is called by `BattleAction_TryContinueComboSequence` (0030FA00); `BattleAction_TryContinueComboSequence` (0030FA00) calls `0030C010`; `BattleAction_TryContinueComboSequence` (0030FA00) calls `BattleUnit_CommitAction` (0030F760); the remaining edges run through shared helpers the page cites.
- **Gameplay — CLIENT and SERVICE (16 edges).** 12 inbound (Gameplay bodies `0031ADB0`, `BattleUnit_HasNonPartyEngagementEvidence` (00308040), `BattleUnit_UpdateEngagementStateFlag` (00307D10) call page-cited `ActorWork_GetBattleUnitRaw` (00263E30), `00253B90`, `Actor_GetWorldPosition` (00265020)); 4 outbound (page-cited `BattleAction_CheckActionAvailabilityReason` (002FFCF0), `BattleUnit_ComputePartyBattleStance` (00308130), `BattleAction_CheckGlobalCategoryDisableReason` (0031A7B0) call Gameplay bodies `BattleEncodedId_IsValidForClass` (00322C50), `BattleRuntime_GetMode0To5FromFlagsAndFieldBit15` (0030D9A0), `BattleUnit_UpdateEngagementStateFlag` (00307D10)). Substantive edges include `Spawn_ValidateCandidateDistanceToPlayers` (00234DA0) is called by `BattleUnit_HasNonPartyEngagementEvidence` (00308040); `00253B90` is called by `BattleRuntime_GetModeDependentDistanceThreshold` (00309A90); `0030C010` is called by `0031ADB0`; `RNG_SharedGameplayLCG_NextU32` (00328370) is called by `00312B40`; the remaining edges run through shared helpers the page cites.
- **Input — SERVICE (3 edges).** 3 outbound (page-cited `002628B0`, `00266D10`, `SaveLoad_ControllerLifecycleHandler` (00582860) call Input bodies `0035B5D0`, `00226BE0`, `00182D40`). Substantive edges include `002628B0` calls `0035B5D0`; `00266D10` calls `00226BE0`; `SaveLoad_ControllerLifecycleHandler` (00582860) calls `00182D40`.
- **InputGameplay — CLIENT (1 edge).** 1 inbound (InputGameplay bodies `00313A00` call page-cited `00253B90`). Substantive edges include `00253B90` is called by `00313A00`.
- **Movement — CLIENT and SERVICE (41 edges).** 30 inbound (Movement bodies `00326BB0`, `002EBFA0`, `003911D0` call page-cited `Actor_GetWorldPosition` (00265020), `ActorWork_GetBattleUnitRaw` (00263E30), `RNG_SharedGameplayLCG_NextU32` (00328370)); 11 outbound (page-cited `002628B0`, `00266D10`, `Spawn_TrySelectCandidatePosition` (00234AF0) call Movement bodies `00263560`, `00265200`, `003DAA20`). Substantive edges include `002628B0` calls `003DAA20`; `002628B0` calls `00263560`; `002628B0` calls `00379070`; `002628B0` calls `003792D0`; the remaining edges run through shared helpers the page cites.
- **Party — CLIENT and SERVICE (25 edges).** 14 inbound (Party bodies `PartyConfiguration_ReconcileRosterFromCurrentSelectors` (003261D0), `BattleUnit_GetPartyLeader` (003272A0), `PartyConfiguration_SetSelectorsAndReconcileRoster` (003273D0) call page-cited `ActorHandle_EncodeRegistryEntry` (003589B0), `ActorWork_GetBattleUnitRaw` (00263E30), `Actor_GetWorldPosition` (00265020)); 11 outbound (page-cited `SpawnLifecycle_CheckAndRetireByNativeRange` (002350C0), `002628B0`, `0031ADB0` call Party bodies `BattleUnit_GetPartyLeader` (003272A0), `PartyFocus_IsCurrentPackedActorHandle` (003273B0), `BattleUnit_ResolveByFocusHandle` (0031B7E0)). Substantive edges include `Spawn_ValidateCandidateDistanceToPlayers` (00234DA0) calls `PartyFocus_IsCurrentPackedActorHandle` (003273B0); `SpawnLifecycle_CheckAndRetireByNativeRange` (002350C0) calls `PartyFocus_IsCurrentPackedActorHandle` (003273B0); `002628B0` calls `PartyFocus_ClearCurrentActorIfEligible` (00358B40); `002628B0` calls `PartyControl_SetMovementSuppressionBit` (00359200); the remaining edges run through shared helpers the page cites.
- **Rewards_Progression_Economy — CLIENT and SERVICE (13 edges).** 4 inbound (Rewards_Progression_Economy bodies `BattleUnit_ProcessDefeatRewardsAndLoot` (00312280), `Loot_FindOverlappingPickupIndex` (002FB150), `GameState_SetGil` (00254EE0) call page-cited `Actor_GetWorldPosition` (00265020), `00316A50`); 9 outbound (page-cited `BattleUnit_ProcessDefeatRewardsAndLoot` (00312280) call Rewards_Progression_Economy bodies `Reward_ComputeExperienceForRecipient` (002F8BB0), `Reward_ComputeLicensePointsForRecipient` (002F90C0), `GameState_GetGil` (00253690)). Substantive edges include `00316A50` is called by `GameState_SetGil` (00254EE0); the remaining edges run through shared helpers the page cites.
- **SaveLoad — CLIENT and SERVICE (3 edges).** 2 inbound (SaveLoad bodies `00280140` call page-cited `00254CB0`, `SaveImage_GetActiveRuntimeBuffer` (002EF640)); 1 outbound (page-cited `SaveLoad_ControllerLifecycleHandler` (00582860) call SaveLoad bodies `00582790`). Substantive edges include `SaveLoad_ControllerLifecycleHandler` (00582860) calls `00582790`; the remaining edges run through shared helpers the page cites.
- **Script_VM_Native_Bridge — CLIENT and SERVICE (45 edges).** 42 inbound (Script_VM_Native_Bridge bodies `0050F0A0`, `0050EEA0`, `0050D9A0` call page-cited `Actor_GetWorldPosition` (00265020), `ActorHandle_EncodeRegistryEntry` (003589B0), `00254CB0`); 3 outbound (page-cited `00266D10`, `003444D0`, `0050C910` call Script_VM_Native_Bridge bodies `VMValueStack_PopInt32CoerceFloat32` (00267E10), `VMNativeCommandDispatch_InitializeFamilyTables` (003DC2D0)). Substantive edges include `00254EA0` is called by `003444D0`; `00266D10` calls `VMNativeCommandDispatch_InitializeFamilyTables` (003DC2D0); `003BA300` is called by `0050C910`; the remaining edges run through shared helpers the page cites.
- **Spawn_Encounter_Lifecycle — CLIENT and SERVICE (12 edges).** 10 inbound (Spawn_Encounter_Lifecycle bodies `Spawn_TrySelectCandidatePosition` (00234AF0), `Spawn_SelectAndPrepareAutomaticEntry` (00235720), `SpawnLifecycle_CheckAndRetireByNativeRange` (002350C0) call page-cited `RNG_SharedGameplayLCG_NextU32` (00328370), `Actor_GetWorldPosition` (00265020), `Spawn_TrySelectCandidatePosition` (00234AF0)); 2 outbound (page-cited `Spawn_TrySelectCandidatePosition` (00234AF0), `SpawnLifecycle_CheckAndRetireByNativeRange` (002350C0) call Spawn_Encounter_Lifecycle bodies `Spawn_ValidateCandidateDistanceToPlayers` (00234DA0), `SpawnGroup_UpdateExpectedMemberLaneMask` (00306E60)). Substantive edges include `Spawn_TrySelectCandidatePosition` (00234AF0) is called by `Spawn_SelectAndPrepareAutomaticEntry` (00235720); `Spawn_TrySelectCandidatePosition` (00234AF0) calls `Spawn_ValidateCandidateDistanceToPlayers` (00234DA0); `Spawn_ValidateCandidateDistanceToPlayers` (00234DA0) is called by `Spawn_TrySelectCandidatePosition` (00234AF0); `SpawnLifecycle_CheckAndRetireByNativeRange` (002350C0) calls `SpawnGroup_UpdateExpectedMemberLaneMask` (00306E60); the remaining edges run through shared helpers the page cites.
- **Status_Periodic_Terminal — CLIENT (3 edges).** 3 inbound (Status_Periodic_Terminal bodies `BattleFormula_BuildRuntimeCounterPeriodicHpCredit` (00386860), `BattleUnit_RunPeriodicCombatMaintenance` (00310DB0), `BattleStats_ChangeStatusAndProcessSideEffects` (0030E360) call page-cited `ActorWork_GetBattleUnitRaw` (00263E30), `Loot_FindOverlappingPickupIndex` (002FB150), `BattleUnit_ProcessDefeatRewardsAndLoot` (00312280)). Substantive edges include `Loot_FindOverlappingPickupIndex` (002FB150) is called by `BattleUnit_RunPeriodicCombatMaintenance` (00310DB0); the remaining edges run through shared helpers the page cites.
- **UI — CLIENT and SERVICE (93 edges).** 78 inbound (UI bodies `00276D30`, `00279E20`, `0029C770` call page-cited `00244960`, `00245000`, `00247870`); 15 outbound (page-cited `00276D30`, `00276650`, `SaveLoad_ControllerLifecycleHandler` (00582860) call UI bodies `002734B0`, `0035BB50`, `002969E0`). Substantive edges include `00245000` is called by `0029C9D0`; `00245000` is called by `0029C770`; `00245000` is called by `002BF4F0`; `00245000` is called by `002BE450`; the remaining edges run through shared helpers the page cites.
- **World — CLIENT (3 edges).** 3 inbound (World bodies `00266D10` call page-cited `003BA300`, `003BA310`, `003DF900`). Substantive edges include `003BA300` is called by `00266D10`; `003BA310` is called by `00266D10`; the remaining edges run through shared helpers the page cites.
- **WorldAreaField — CLIENT and SERVICE (25 edges).** 5 inbound (WorldAreaField bodies `WorldTransition_StageFieldTransition` (003145E0), `WorldTransitionSnapshot_CaptureRuntimeState` (00229B40), `WorldTransitionSnapshot_RestorePersistencePairForActiveSlot` (005843E0) call page-cited `SaveImage_GetActiveRuntimeBuffer` (002EF640), `00313A00`, `00362850`); 20 outbound (page-cited `00266D10`, `002628B0`, `Spawn_TrySelectCandidatePosition` (00234AF0) call WorldAreaField bodies `FieldData_GetActiveFieldRecordBit15` (00377C20), `FieldData_GetActiveFieldRecordBit15` (00313F60), `FieldRegion_ContainsWorldPosition` (002374E0)). Substantive edges include `Spawn_TrySelectCandidatePosition` (00234AF0) calls `FieldRegion_ContainsWorldPosition` (002374E0); `Spawn_TrySelectCandidatePosition` (00234AF0) calls `003209C0`; `SpawnLifecycle_CheckAndRetireByNativeRange` (002350C0) calls `FieldData_GetFormat0RecordVectorByIndex` (00320940); `002628B0` calls `003DFA50`; the remaining edges run through shared helpers the page cites.
- **Script_VM_Native_Bridge — CLIENT and SERVICE (45 edges).** 42 inbound (Script_VM_Native_Bridge bodies `0050F0A0`, `0050EEA0`, `0050D9A0` call page-cited `Actor_GetWorldPosition` (00265020), `ActorHandle_EncodeRegistryEntry` (003589B0), `00254CB0`); 3 outbound (page-cited `00266D10`, `003444D0`, `0050C910` call Script_VM_Native_Bridge bodies `VMValueStack_PopInt32CoerceFloat32` (00267E10), `VMNativeCommandDispatch_InitializeFamilyTables` (003DC2D0)). Substantive edges include `00254EA0` is called by `003444D0`; `00266D10` calls `VMNativeCommandDispatch_InitializeFamilyTables` (003DC2D0); `003BA300` is called by `0050C910`; the remaining edges run through shared helpers the page cites.
## The `002FFCF0` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`002FFCF0` (`BattleAction_CheckActionAvailabilityReason`, ~264 B) —
`byte[rdx] & 0x10` test, `qword[+0x698]` into `rdi` (`002FFCFF`/`002FFD05`).

| member | role | interior |
| --- | --- | --- |
| `0031A7B0` | `r8d = 1`, `movzx edi, dx` forward (`0031A7BA`/`0031A7C0`) | [`0031A7BA`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none.

## Interior citation — frontier hub `00244960` (2026-09-17, SWE2-EC7)

`00244960` — 12 B, 61 frontier callers at census; the pass-22 note above already calls it "the
accessor half of the open-work pair". Interior verified:
[`00244965`](../../_index/ADDRESS-INDEX.md) is `je 00248220` — the whole body is
`cmp qword ptr [rdx + 0x10], 0; je 00248220; ret`: a **predicate-guarded dispatch** — if the
record's `+0x10` pointer is absent, fall through to `00248220` (a bounded-loop routine per the
census tags); present → return. The save writers calling it are probing whether the mode record's
optional sub-object exists before serialising.

NOT claimed: what `00248220` does for the absent case (it is the null path, not verified here) or
the record type at `rdx` — only the guard shape is measured.


## Interior citation — frontier hub `00253B90` (2026-09-18, SWE2-EC7)

`00253B90` — 12 B, 7 callers; the `[01E0C2B8] == 0` gate. Interior verified:
`cmp dword [01E0C2B8], 0; sete al` at [`00253B92`](../../_index/ADDRESS-INDEX.md) —
the global's zero state is the whole answer; no flags, no second source.

## SWE2-EC7-40 update (2026-09-19) - `005819F0`

`005819F0` (372 B) is a force-fight body - `02CA99B0`/`02CA99C0` fields, `00254CB0` pair plus `00247510`/`002EF640`/`00244960`/`00247870`/`00247930`. Interior anchor `00581A30` (a `00254CB0` call).

## SWE2-EC7-87 update (2026-09-20) - `003DF900` shared-state block reset measured

`003DF900` (79 B) is the global-state init the force-fight,
font and registry callers run: `02B59D20` takes `byte = 2` and
bit-0 cleared, the `+0x4`/`+0x10`/`+0x14`/`+0x18`/`+0x1C` fields
are zeroed, `+0x1C` receives `0x80808080` and `+0x20` receives
`0x80000000` - a ~0x24-byte block returned to defaults.
Interior anchor `003DF92C` (the xmmword clear).

## SWE2-EC7-106 update (2026-09-20) - `00253BA0` measured

`00253BA0` (27 B) is the gated
flag read `00276650` and `00276D30`
call: `003BA2E0()` runs first, and
only when it reports nonzero does the
answer come back as `dword[01E0C2B8]`
- a zero `003BA2E0` result forces 0 -
the single predicate in front of the
force-fight state word.
Interior anchor `00253BAD` (the
`cmovne` on `01E0C2B8`).

## SWE2-EC7-107 update (2026-09-20) - `003BA2E0` measured

`003BA2E0` (27 B) is the two-flag
conjunction `00252C80`, `00253BA0`
and `00254EA0` call: answers 1 only
when both `byte[02B4053D]` and
`byte[02B4053C]` are nonzero - the
paired ready check in front of the
force-fight state word.
Interior anchor `003BA2E9` (the
second flag test).

`00582FC0` (114 B) is the mode-record teardown `00582860` runs on shutdown: `00393900(rcx+0x100, 1)` and `003938B0(rcx+0x108, 1)` release the paired sync objects, then when flag `[rbx+0xC1]` is clear it `003697F0`-frees the `+0x110` and `+0x118` pointers and nulls both — conditional cleanup, so a live flag leaves the buffers owned elsewhere.

Interior anchor `00582FCE` (function `00582FC0`).

`005819A0` (80 B) is the `02CA99C8`-record flag latch `00582860` calls: when the global exists and `+0xCC` bit 0 is still clear, it stores `00249C60(0x42)` into `+0xE8` unless the mode byte is `1`, then sets `+0xCC |= 1`; the mode byte is always written to `+0xD0` — a once-only initialization latch keyed on the `+0xCC` flag.

Interior anchor `005819D7` (function `005819A0`).

## Interior citations for the entry-cited functions (OPUS, 2026-10-03, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-force-fight-mode-cloudint-1003/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `002734B0` | 60 B | for `i` from 0 while `i` is below `0035BB60()` (re-read each step, signed), tail-jumps to `0035BB20(i)` for the first `i` whose `0035BB20(i)` record has bit `0x4` of its first byte set; returns 0 when none has (or the count is not above 0) | `002734BF`, `002734C3`, `002734C8`, `002734D6`, `002734E7` |
| `0050EEA0` | 61 B | with `n` = `003BB420` of the incoming `rcx`, calls `00254CB0(0)` and `0017D280(00D22AD8, n)`, then tail-jumps to `0026B4E0(rcx, n)` | `0050EEAD`, `0050EEB6`, `0050EEC4`, `0050EED8` |
| `0050F0A0` | 61 B | with `n` = `003BB420` of the incoming `rcx`, calls `0017D280(00D22860, n)` and `0026B4E0(rcx, n)`, then tail-jumps to `00254CB0(0)` | `0050F0AD`, `0050F0BD`, `0050F0C7`, `0050F0D8` |
