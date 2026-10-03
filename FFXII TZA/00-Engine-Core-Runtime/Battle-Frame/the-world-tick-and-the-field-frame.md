---
system: The world tick and the field frame — what runs on the battle layer each frame, in what order, behind which gates
category: 00-Engine-Core-Runtime
status: AUDITED
owner_layer: PrimaryOwner:WorldAreaField (the tick and the field frame) — the per-unit frame is ActorEntity, its callees are owned elsewhere
evidence_tier: 1
readiness: BEHAVIORALLY UNDERSTOOD
confidence: PROVEN
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: World_UpdateSimulationTick (845 B), BattleSystem_RunFieldFrameOrchestrator (752 B),
    BattleUnit_UpdateLifecycleAndCombatFrame (467 B), the three frame-mode call sites, and fifteen
    gate/helper bodies disassembled from the shipping EXE with every RIP target computed by a tool;
    the callback route for the per-unit frame proven by a boundary-free sweep of .text with controls
last_reviewed: 2026-09-10
audit:
  passes: 1
  last_pass: 2026-09-12
  last_pass_state: opus-the-world-tick-and-the-field-frame-pass-1
  last_pass_kind: authored
  crossref_clean: false
  reopened_count: 0
---

# The world tick and the field frame

> Every frame that shows the field, one function ticks the simulation for five actor-manager slots,
> one function runs the battle layer's fixed per-frame list for slot 0, and one callback — installed
> when a battle unit is bound — runs the lifecycle of each unit. This page is the order and the
> gates; the callees it names are owned by their own pages.

## 1. What the player sees

Nothing directly. This is the spine that decides, sixty (or thirty) times a second, whether enemies
retire for distance, whether a wiped group posts its completion, whether the party's controls are
suppressed, whether the "game over" and "party incapacitated" requests go up, and whether an
enemy far from the party is even simulated. When the full menu is open, most of it does not run
at all — only two of the five actor slots are ticked — which is why the world stands still behind a
menu without anything being paused explicitly. **Queued area work is the exception:** the tick's prologue
runs in every mode, and it drains the actor-manager request mask — initializing and unloading managers and
clearing the party roster — whether or not a menu is open (§2.2, corrected 2026-09-13).

## 2. Native mechanism

### 2.1 Three frame modes tick the world, and they do not ask for the same thing

`World_UpdateSimulationTick` (`00314020`, 845 B) has three callers, one per interactive frame mode
of [the frame dispatcher](../../22-Middleware-PhyreEngine/The-Frame/what-happens-between-two-frames.md)
§2.2, and **the first argument is the mode of the tick**:

| frame mode | caller | site | `ecx` | `edx` |
|---|---|---|---|---|
| 2, the field frame | `0022A770` | `0022ABD6`–`0022ABD8` | **0** | `edi` (the field frame's own flag) |
| 3, the full-menu frame | `MainLoop_UpdateAndRenderFrame` `0022B8C0` | `0022BA1C`–`0022BA23`, under the `ATEL CONTROL` label | **1** | 1 |
| 5, the capture-backed frame | `0022BC20` | `0022BCC8`–`0022BCCF`, same label | **1** | 1 |

The field frame reaches its call only when `001800E0()` is zero and `001800C0()` is zero or
`001EC560()` is zero (`0022ABB9`–`0022ABD2`) — three unread gates *(answered: see EX-6, ANSWERED 2026-09-12 (FABLE), which reads all three; 2026-10-02, OPUS)* that skip the tick entirely.

### 2.2 `World_UpdateSimulationTick` — five slots, up to sixteen sub-steps, one fixed tail

The tick works on the **actor-manager slot array at `02098E10`, stride `0x288`**, whose field map
[the cutscene-slots page](../../99-Unresolved-Residual/Cutscene-Asset-Slots/cutscene-name-slots-and-the-depth-of-field-sidecar.md)
§"The table" recovered and [the field runtime pass](../../04-Actor-Entity/the-field-runtime-pass.md)
§2 reads per slot. **Five slots, `0`–`4`**: every loop below is bounded by `cmp ebx, 5` /
`cmp ebp, 5` (`00314132`, `003141E9`, `00314218`, `0031425D`, `00314270`).

**Prologue, every mode.** `[022C2548] = 1` (`00314047`) — the *tick in progress* word, read back by
`00314960` and cleared to `0` at `0031435D` on every exit; then `003EB9A0`, `003DAA20`, `003DA2F0(1.0f)`,
`003DD210(1.0f)`, `0025BFB0` (`00314056`–`00314078`). Then the **deferred mode request**:
the dword at `01EED060` is cleared to `-1` if it was non-negative (`0031407D`–`00314092`), and if
`01EED064` is non-negative the two console markers at `00D103E0` / `00D10420` are printed
(`0031409A`–`003140AD`) and `WorldSimulation_ProcessDeferredModeRequest(0, request)` runs
(`003140BA`), after which `01EED064 = -1` (`003140BF`). Then `003DAA40` (the movement-body pool's tick reset — the 32 cell masks and every body's active flag, [the movement body page](../../06-Movement-And-Navigation/the-movement-body-pool-and-the-separation-pass.md) §2.6), `0046AFA0`, and — **mode 0
only** — `PartyControl_UpdateControlledActorLocomotion` (`003140D4`); `00268650`, `0025D650`,
`00255810`, `0037D890`, `0025D640` (`003140E6`–`003140FA`). `0025D650` resets the five-field block
at `0209A2B0`–`0209A2C4` every tick (`0025D658`–`0025D67B`) — the byte `0209A2C4[2]` that the
group-completion event lock writes is zeroed here first.

> **`0025BFB0` — the manager request queue, drained in every mode (read 2026-09-13; ASTRA's
> [§14](../../05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md) independently confirmed against the
> 179-byte body).** It reads the mask `02099ABC`; zero returns (`0025BFBC`). If **bit 0 is set in that first
> read**, it calls `ActorSystem_InitializeManagerRuntime` (`0026CE60`) for each set bit **4, 3, 2, 1, 0**,
> re-reading the mask after every call (`0025BFF0`–`0025C005`), then zeroes the four party-roster pointers
> `0209A1F0`–`0209A20F` (`0025C017` / `0025C01F`) — even if a callback has cleared bit 0 meanwhile. Then, with or
> without that sweep, it calls the unload `002628B0` for each set bit **4 down to 0**, clearing each bit only after
> its call returns (`0025C030`–`0025C052`). Bits 5 and above are never visited. Because the mask is re-read, a
> request added during the pass for a lower index runs in the same pass, one for an index already passed waits
> for the next tick, and a manager that re-requests itself during its own unload is cleared by the caller.
> **This call sits before the mode test (`0031410C`), so a menu does not stop queued area preparation, the roster
> clear or the deferred mode request below** — only the slot loops depend on the mode. The one producer read so
> far is `0026A5F0` (requesting manager 0 also requests 1–3); whether ordinary callbacks change the mask during a
> pass is not established (`EX-9`) *(answered: see EX-9, ANSWERED 2026-09-18 (FABLE); 2026-10-02, OPUS)*.

**The slot loops — the shape depends on the mode** (`00314103`–`0031420F`):

```
mode 0 (field):
  003DF760(0, n, 0, 0, 0)  for n = 1, 2, 3, 4, 5                          0031415F-003141B5, unread
  for step = 0 .. 15:                                                     esi, cmp 0x10 at 0031421F
      for slot = 0 .. 4:
          if step != 0 and slot.flags201 == 0: continue                   003141C3-003141D0 via 00267310
          BattleSystem_RunFieldFrameOrchestrator(slot)                    003141D4   (a no-op for slot != 0, section 2.3)
          ActorManager_RunFieldRuntimePass(slot)                          003141DB   the actor drive loop
          00234520(slot)                                                  003141E2   (a no-op for slot != 0, below)
      if step == 0: 002E0D90(); 00268D00()                                003141F2-003141F7  (thunks to 00253C50 / 00268D10)
      for slot = 0 .. 4:
          if step != 0 and slot.flags201 == 0: continue                   00314200-0031420D
          003DB1F0(slot)                                                  00314211   the per-record post-pass, below

mode 1 (menu / capture):
  for slot = 3 .. 4:                                                      ebp = 3 at 003140FF
      BattleSystem_RunFieldFrameOrchestrator(slot)  -> no-op             00314116
      ActorManager_RunFieldRuntimePass(slot)                              0031411D
      003DB1F0(slot)                                                      00314124
      00234520(slot)                                -> no-op             0031412B
  002E0D90()                                                              00314137

any other mode: no slot work at all                                       0031410C jne -> 00314231
```

> **The sixteen sub-steps are real, and a slot opts into them by one byte.** Sub-step 0 runs for
> every slot unconditionally. Sub-steps 1–15 run only for slots whose byte at `+0x201`
> (`02099011 + slot*0x288`, read by `00267310` at `00267321`) is non-zero. That byte is the
> per-manager bitmask the cutscene-slots page traced to two ScriptVM commands (1337, 1306) and two
> engine paths — **so a script can ask for a slot to be simulated up to sixteen times per frame**,
> which is what a fast-forward or a catch-up looks like from inside the tick. What each of the
> fifteen extra passes is *for* is not established here (`EX-1`). *(Answered since — `EX-1`, 2026-09-11,
> in §2.2a below.)*
>
> **Behind the full menu only slots 3 and 4 tick, once.** Slot 0 — where the field frame lives —
> is not touched, so the battle layer does not advance at all in modes 3 and 5. The frame page's
> §6 warning (*"the menu is open is not by itself a reason to expect the simulation to be stopped"*)
> is right about slots 3–4 and wrong about the battle layer: the field frame is the one thing the
> menu modes never reach.

**The per-record post-pass `003DB1F0(slot)`** (132 B): if the slot is live (`+0x10` bit 0,
`003DB1FE`), for each record `ActorManager_GetRecordByOrdinal(slot, i)` (`003DB21A`) whose byte
`+0x63` is non-zero: walk `[record+0xA0]` for `record[+0x89]` entries of stride `0x14` turning a
`1` at entry `+0x11` into `2` (`003DB240`–`003DB250`), then `003DB6E0(record)` (`003DB255`), then
**`record[+0x63] >>= 1`** (`003DB25A`). A per-record countdown that shifts right once per pass.

**The tail, every mode** (`00314231` onward): two counters increment (`022C252C`, `022C2530`;
their resetters are `00314010` / `00314000`), `003DAC70(00314F30)` walks the `0x130`-stride list at
`02B4E4C0` from the head index at `02B57CC0` calling `003DAAB0` and `003DAB50` per node with the
callback (`003DAC76`–`003DACE1`) — **the movement-body separation pass**, each active body against the bodies sharing its cells and every remembered pair, overlapping pairs pushed apart by weight ([the movement body page](../../06-Movement-And-Navigation/the-movement-body-pool-and-the-separation-pass.md) §2.6–2.8; EX-4 answered 2026-09-11) — then **`002623A0(slot)` for the same slots the mode ticked**
(`00314254`–`00314273`). `002623A0` publishes the slot block pointer to `02099D70` and the party
focus record to `02099D78` (`002623C5`–`002623EB`) and, for a live slot, runs `002E5180` over the
records `[+0x1DE, +0x1DE + +0x1D6)` (`002623F4`–`00262426`). Then the fixed list, cited by
address because most are unread: `PartyFocus_UpdatePrimarySecondaryActorProcessing(mode)`
(`00314278`), `002E09A0`, `00359800`, `003DE640`, `002E0940`, `0037C1A0`, `003E7EC0`, `00228480`
→ if zero `0036FD90(0)` (`0031429B`–`003142B6`), `002F1770(mode, edx)`, `002EF910`, `0036E1E0`,
`003DEB30`, `003DF670`, `003606E0`, `00362850` [Audio], `00362DA0` → if zero the time-scale block
(`003142F7`–`0031433C`: `00362DB0()` plus the float at `022C2544`, compared against `002DEBA0()`
[Audio], the smaller clamped to `1.0f`, handed to `00361700(x, 0)`), `003E7650` [Presentation],
`0025D950`, `00263660` [ActorEntity], `002EEEB0`. **Return `eax = (mode == 0)`** (`0031435A`,
`r15` from `003140E2`).

### 2.2a The fifteen extra sub-steps are uniform repeats, and slot 0 never gets them

**Answered 2026-09-11 (`EX-1`).** Two readings settle the question the previous section left open.

**The step number goes nowhere.** `esi` — the sub-step counter — is used for exactly three things
in `00314020`: the two opt-in gates (`test esi, esi` at `003141C3` and `00314200`, which let step 0
through unconditionally), and the step-0-only pair `002E0D90` / `00268D00` (`003141EE`–`003141F7`).
Every callee in the loop receives **the slot index alone** (`mov ecx, ebx` at `003141C7`,
`003141D2`, `003141D9`, `003141E0`, `0031420F`); nothing in the loop or its callees is handed the
step. So sub-steps 1–15 are **the same three calls and the same post-pass, run again** — a slot
whose `+0x201` byte is non-zero is simulated up to sixteen times in one frame. The passes are not
"for" anything individually; the count is the whole mechanism: a fast-forward.

**Slot 0's byte is never set.** The byte has one bit-level writer and one direct writer, both read:

| writer | site | what it can do to slot 0 |
|---|---|---|
| `0026A5B0(manager, on, bit)` (53 B) | `bts` / `btr` on `02098E10 + manager × 0x288 + 0x201` (`0026A5CF`, `0026A5DA`) | whatever its two callers ask |
| ↳ `00360710(request, manager)` — **skip begin** | called by ScriptVM command 1337 `skipexec`'s begin handler `0034ECF0` with the script actor's manager byte `+0x15` (`0034ED01`) and a request index popped by `00267E10`; and by the engine path `00360880`, which loops **managers 1–3** over the pending bits at `022CB9C0` (`0036088A`–`003608BE`) | **returns 0 at once when the manager is 0** (`00360728`–`0036073E`); the engine loop starts at 1 |
| ↳ `00360A50(request, manager)` — **skip end** | called by command 1306's poll handler `0034DB30` (`0034DB59`, `0034DBE8`) and by the engine path `003603F0`, which loops requests 0–7 | **only ever clears** (`0026A5B0(m, 0, k)` at `00360AFA`) |
| `ActorManager_BindLoadedDefinitionPayload` (`0026C8C0`) | `mov [rdi + 0x201], bl` at `0026CC38`, `rbx` being the zero the whole record is filled with | writes **0** |

So the field manager's byte is 0 from its bind onward and no path can raise a bit in it: **the
field frame never fast-forwards; sub-steps 1–15 exist for the cutscene managers (slots 1–4) during
a script skip.** The script situation that opts a slot in is `skipexec` issued by a script whose
actor belongs to that manager — and there is no script situation for slot 0.

**What a skip is, from the two setters.** A skip request is one of eight per manager, a 16-byte
entry at `022CB730 + (manager × 8 + k) × 16` (`b_00` = the bit it owns in `+0x201`, `b_01` = its
row in the pending / active dword arrays `022CB9C0` / `022CB9D8`, `b_02` = state, `dw_08` = begun,
`dw_0C` = armed); `00360980` registers one (it sets the pending bit, `003609F3`). `00360710`
requires the manager live and not held (`00267330`: `+0x10` bit 0 set, bit 7 clear) and the entry
armed (`dw_0C`, `00360768`), then stops the audio side (`002DEBE0` / `002DEDD0`, the three words
`022CB9B0`–`022CB9B8`), calls `002DE7F0(0x7F)` and `002273E0`, marks the entry begun and in state 2,
moves the bit from pending to active (`003607CD`–`003607D9`), notifies eleven subsystems
(`003601B0`, `003600D0`, `00466DD0`, `003E8AA0(m)`, `003DE0A0`, `003E9970(m)`, `0036DE70(m)`,
`00473680(m)`, `0024D9C0`, `003B08F0`, `003DEE10(m)` — unread, `EX-8`), and, if the manager's byte
was still 0, issues `002EFE40(6)`, `002EFE50(0xFF)`, `002EFA70(4, 0, 0, 0)` (`00360822`–`0036084F`)
before setting the bit. `00360A50` undoes it for an entry in state 2 — eight of the same
notifications, the entry and both bit arrays cleared, the bit cleared, then `002E1CA0(0, 0xD)` and
`002E1CA0(0, 0x13)`. Command 1306's poll handler is the wait around it: state 0 holds until
`0025C070(manager)` finds no live record of that manager with `+0x14` bit 6 set (`0025C0A1`–`0025C0C3`),
states 1–3 pass `003608D0` [Audio], `00360D60`, `002F1A30(1)` and `0032E520(1)` [Resource], then
the end is issued and state 4 waits for `00229EB0()` to change (`0034DBED`–`0034DBF7`,
`0034DB8A`–`0034DB92`).

### 2.3 `BattleSystem_RunFieldFrameOrchestrator` — slot 0 only, in this order

`00234590(slot)` returns at once for any slot but `0` (`002345B1 test ecx, ecx` / `jne 0x234866`),
so **everything below happens once per tick, for slot 0, and never behind the menu.**

| # | site | step | what it does or gates |
|---|---|---|---|
| 1 | `002345B9` | `02089340 &= ~0x2000` | bit 13 of the battle-state word cleared at the top of every field frame |
| 2 | `002345C3`–`002345E9` | clock advance | `GameClock_GetRawTickCounter` before and after `0032A100`; **bit 2 of `02089340` = the counter did not move**. `0032A100` bumps `0208D45C` only when the timer value from `003EBA90(0)` differs from the one stored at `022C317C` (`0032A12A`–`0032A13B`) |
| 3 | `002345EF`–`0023461F` | UI requests `0x0B` / `0x18` | skipped when `0035C700()` (`022C83E8 & 0x100`, or `02092730 ∈ {0x0B, 0x18}`, or `002E12D0()`) or `00306BB0()` (`022C2160 ∈ {5, 6}`). Otherwise `002371B0()` → request `0x0B`; else `00237140()` → request `0x18`; through `0035C7A0(id)` = `0035C7B0(id, 1)` |
| 4 | `00234624` | `00313A00` | the capability row-2 reconciliation, [the capability policy](../../15-Input/Gameplay-Capability-Policy/capability-inhibition-policy.md) |
| 5 | `00234629` | `0030C0D0` → `00253B90` | the null predicate the same page names |
| 6 | `0023462E`–`002346C9` | the unit reset loop | runs when `00253B90()`'s result differs from `~bit 3` of `02089340` (`00234639`–`00234645`); `BuildFilteredFourSlotUnitBuffer(&buf, 1)` (`00234651`), then for each unit not carrying flag bit 24 (`0023467B`): `BattleUnit_ResetActionControlForStatusTransition(unit, flag)` (`002346BE`) with `flag = 0` when `+0x714 ≤ 0x21E` and `+0x6B4 ≥ 9`, or `+0x714 == 0x113`, or the record's `(+0x64 \| +0x3C) & 0x8000020` (`00234682`–`002346B9`). Afterwards **bit 3 flips** (`002346CB`–`002346DA`) — so with a steady predicate the loop runs every second field frame |
| 7 | `002346DC`–`002346DF` | `02089340 &= ~2` | bit 1 cleared every field frame; the unit frame re-sets it (section 2.4) |
| 8 | `002346E5` | `PartyControl_RecomputeSuppressionFromLeaderBattleState` | [party roster and control suppression](../../11-Party/party-roster-and-control-suppression.md) |
| 9 | `002346EA` | `BattlePerception_ResetSpatialVisibilityCacheFrameState` | |
| 10 | `002346EF` | `003226C0` | `[022C2570] = 0` (`003226C2`) |
| 11 | `002346F4`–`002346F9` | `0030CBE0`, `003065D0` | CombatAction, unread |
| 12 | `002346FE` | `BattlePerception_AdvanceCandidateCacheGeneration` | |
| 13 | `00234703` | `PartyCombat_UpdateStanceState` | |
| 14 | `00234708` | `Loot_UpdateWorldPickupLifetimeAndDespawn` | |
| 15 | `0023470D` | `00313760` | registry-slot `02EBF190` record `+0x5AD0` bit 1 gates a timer copy (`0031376B`–`003137C9`) |
| 16 | `00234712` | `00304440` | unread |
| 17 | `00234717` | `SpawnGroup_DispatchPendingCompletionSignals` | [group completion](../../05-Spawn-Encounter-Lifecycle/Group-Completion-And-Respawn/when-a-group-is-wiped-and-when-it-comes-back.md) §5 — the once-per-frame consumer of the ledger flag |
| 18 | `0023471C`–`0023476A` | UI request `0x18` latch | `00237260()` non-zero → set bit 9 and raise `0x18` if bit 9 was clear (`0035C8A0`); zero → `0035C8E0(0x18)` — which **ignores `0x18`** (`0035C8E0` only acts on `0x17`, `0035C8E5`–`0035C8F8`) — and clear bit 9 |
| 19 | `00234770`–`002347E8` | UI request `0x17` latch | the party leader (`BattleUnit_GetPartyLeader`) with a record whose `(+0x64 \| +0x3C) & 0x80000003` is clear or `FieldData_GetActiveFieldRecordBit15()` set → clear bit 8 and `0035C8E0(0x17)`; otherwise set bit 8 and raise `0x17` |
| 20 | `002347EE`–`00234849` | bit 11 | `003137F0` (registry-slot `02EBF190` record byte `+0x5AD5`) → `BattleUnit_FindByCombatantId` → if `003135C0()` (`0030D9A0() == 1`) and that unit's record flags pass the same `0x80000003` / Bit15 test: **`02089340 \|= 0x800`**, else `&= ~0x800` |
| 21 | `00234849`–`0023484E` | `00392740`, `PartyFollow_SolveFormationWrapper` | Movement |
| 22 | `00234853`–`0023485C` | `PartyFollow_ApplyGoal` | only if `Navigation_HasDataset()` |
| 23 | `00234861` | `002F82F0` | unread |

The three UI-request helpers write the flag word `022C83E8`: `0035C8A0(0x0B)` sets bit 1 and calls
`00254850(1)`; `(0x17)` sets bit 4 and calls `002548F0(1)`; `(0x18)` sets bit 0 and calls
`00254940(1)` (`0035C8AF`–`0035C8D7`). `0035C8E0` clears only bit 4 (`0x17`, `0035C8EA`–`0035C8F3`).
What the three requests *are* is not established here *(answered since — `EX-2`, 2026-09-12, in §7's struck
checkbox)*; the ladder page already asks what `0x0B`
and `0x18` mean at `02092730` (`EX-2`). Narrowed 2026-09-11: `02092730` is the id of the last UI
request any route posted (`00252B40`, [the router](../../16-UI/Request-Router/ui-request-router.md)
§2), so `0x0B` / `0x18` there are request ids 11 and 24 — the same ids this frame raises; what
each opens on screen is still the router page's open item.

**What the two request predicates test.** `002371B0` returns `1` unless some party slot `0`–`3`
(`BattleUnit_FindMappedDefinitionSelectorByIndex`) holds a unit whose record has kind byte `+5 == 0`,
type byte `+4 ≤ 6` and unit flag bit 1 clear (`002371CC`–`002371EE`), or some `00320AB0(i, 3)` for
`i < 9` has kind `0`, type `≤ 6` and passes the `0x80000003` / Bit15 test (`00237200`–`00237239`).
`00237140` is the same over the party slots with type in `7..0x19` (`00237175`–`0023717F`). So
request `0x0B` goes up when **no low-type kind-0 unit is alive in the party or the nine reserve
entries**, and `0x18` when **no kind-0 unit of type `7..0x19` is**. The type ranges are read, not
named.

**`00234520(slot)`** (109 B) is also slot-0-only (`0023452F`): `PartyControl_RecomputeSuppressionFromLeaderBattleState`,
`00313DB0`, `00319090`, then **the one-shot callback at `0208E6A8`** — called and nulled
(`0023455A`–`00234568`) when `(02089340 & 5) == 1` and bit 1 is clear; otherwise
`00313CD0` if `Navigation_HasDataset()`. The pointer is set by `00238A60` and `0023B020`
(CombatAction) and consumed here exactly once.

### 2.4 The per-unit frame — installed as a callback, run from the actor drive loop

`BattleUnit_UpdateLifecycleAndCombatFrame` (`00233F70`, 467 B) has no caller and no stored pointer.
Its address exists in exactly one place: **`00265A4F lea r13, [00233F70]`** in
`ActorSystem_BindBattleUnitsForEligibleRecords` (`00265A20`), which for every record with byte
`+0x14 ≥ 0x80` (`00265A83`–`00265A89`), up to 32 of them (`00265A8F`), allocates a unit
(`BattleUnit_AllocateSlotAndBindActor`, `00265A9F`) and **stores the callback at record `+0x38`**
(`00265AA8`). The consumer is `WorldActor_UpdateRuntimeAndScriptExecutionState` (`0025DF00`),
called per actor inside [the actor drive loop](../../04-Actor-Entity/the-field-runtime-pass.md)
§4, which calls the callback at `0025E222` — `call rax` after `0025E20E mov rax, [rdi+0x38]` —
with `rcx = slot[+0x28]` and `rdx = record`, only when the record's `+0x09` bit 5 is clear,
`+0x14` bit 4 is set, `+0x18 == 0` and `+0x13` bit 1 / `+0x09` bit 6 are clear
(`0025E1E2`–`0025E215`), setting `+0x0D` bit 6 first (`0025E217`).

**So the ordering is: field frame (slot 0) → actor drive loop → per unit, the lifecycle frame.**
Inside `00233F70`:

```
gates (any fails -> return):                                      00233F80-00233FBD
   ActorWork_GetBattleUnit(record) non-null
   ActorSystem_IsPrimaryBattleSimulationReady()
   Navigation_HasDataset()
   unit flags bit 3 set, bit 16 clear

bit 4 set  (ACTIVE):                                              00233FC3
   kind gate: record +0x698 null, or (+0x64|+0x3C) & 0x80000003 clear, or Bit15   00233FCC-00233FEC
   -> 00307C70 ; BattleUnit_SnapshotWorldActorRuntimeState ; BattleUnit_RunPeriodicCombatMaintenance ;
      BattleUnit_RebuildPerceptionCandidateCache ; BattleUnit_UpdateCombatFrame ;
      BattleUnit_ApplyMovementIntentToWorldActor ; SpawnLifecycle_CheckAndRetireByNativeRange ;
      tail 00312700                                               00233FEE-00234034
   kind gate fails -> the inactive branch below                   00233FD6 / 00233FEC

bit 4 clear:
   bit 1 set -> 00312700 only                                     00234039
   spawn-backed (record +5 == 1) and [+0xE68]+0x18 & 0xE == 4     00234042-00234065
      -> Snapshot ; 0033A240(unit+0x80) ; ApplyMovementIntent ; 00312700
   otherwise (IDLE):                                              00234095
      if !SpawnGroup_HasPendingCompletionSignal(): 02089340 |= 2  0023409E
      Actor_SetMovementSpeed(work, 0.0f) ; 003057D0 ; 0030CA50 -> 00322310 / 003228E0
      if unit bit 33 and byte +4 bit 2 and the result: BattleUnit_TeardownAndDespawn(unit, 0)   002340E2-00234100
      00312700
   ACTIVATION: bit 4 clear and bit 1 clear, 00267240(work) and record +0x698 non-null
      -> unit flags |= 0x10                                       00234117-0023412D
```

**Bit 4 of the unit's first qword is therefore "simulated this frame"**, set by the activation arm
and tested at `00233FC3`; **bit 1 turns the frame into a no-op**; bit 3 must be set and bit 16
clear for any of it to run. The retire check is the last step of the active path, the teardown of a
unit that was told to die (bit 33) is the last step of the idle path.

### 2.5 The battle-state word `02089340`, bit by bit (2026-09-11, OPUS-REQ-FABLE-STATEWORD-BITS)

OPUS swept every instruction that manipulates the word with an immediate and found thirteen bits;
this section reproduces that census (a whole-image rip-relative scan, 2026-09-11: 126 accesses, the
same thirteen bits with the same site counts — bit 4 fifty tests and one clear, bit 5 seven tests,
and no `bt` family instruction on the word), then reads every setter, clearer and tester, and adds
the bits the immediate sweep cannot see: **7, 12 and 13** are set and cleared by four boolean
helpers that `btr` / `and` a *register* copy (`00238AE0`, `00238B00`, `00238B20`, `00238B70`);
**23, 26 and 29** by Script-VM verbs that `bts` / `btr` a register (`0050F2E0`, `0050F170`,
`0050F380`, with getters `0050F2B0`, `0050F140`, `0050F340`); **2 and 3** by the orchestrator's
read-modify-write (§2.3 steps 2 and 6); and **6, 7, 12, 13** are also tested after a whole-word load
(`0023B056` `and al, 0x40`; `0030B78C` and `0046AB10` `test …, 0x3080`).
`BattleSystem_InitializeAreaState` writes the whole word once: `(w & 0xFFFFC01E) | 0x10`
(`00234325`–`00234343`) — bits 1–4 and 14–31 survive an area initialisation, bits 0 and 5–13 do not,
and bit 4 is set.

| bit | set | cleared | tested (sites) | what it means |
|---:|---|---|---|---|
| 0 | `0023B020` — arms the one-shot at `0208E6A8` with a handle at `0208E6A4`; its caller `00306B10` (← `0030CBE0`, step 11) registers `00306560` for a unit's handle | `00238A60` — nulls the one-shot (← `00306570` from `InitializeAreaState`, `002341C0`, `0030C970`; ← `003065D0` from step 11); the init mask | `00234520` runs the one-shot when `(w & 5) == 1` and bit 1 is clear; `0030C010` / `0030DA30` test it before `00237670(handle)` (4) | **a one-shot combat callback is armed** |
| 1 | an idle unit frame (§2.4, `0023409E`; `00308666`, `003086F2`) | step 7 every field frame | §2.4 | the frame is a no-op (§2.4) |
| 2 | step 2 (register) | step 2 | step 2, `00234520` | the clock did not advance this frame |
| 3 | step 6 toggles it (register) | step 6 | step 6 | reset-loop parity |
| 4 | `InitializeAreaState` `00234339` | `002341C0` `002341E4` (← `002695A0` ← `002628B0`, the area unload path) | **50 sites**, all in the party / menu resolvers `00317…`–`00329…`: `BattleUnit_GetPartyLeader` (`003272A9`, returns null without it), `BattleStats_ResolveByActorHandle`, `BattleUnit_ResolveByFocusHandle`, `BattleMenu_BuildCommandEntryList` ×2, `ActorHandle_GetPrimaryFormulaResourceByte26`, `BattleUnit_RebuildPerceptionCandidateCache`, `00329220`, `0031ADB0` ×4 … | **the area's battle state is live** — every resolver answers "nothing" until the area is initialised and after it is torn down |
| 5 | `00238B70(1)`, which then posts `0x30B` to every active unit (EE-7): `SpawnGroup_RecordMemberDeathAndHandleCompletion` on a group's completion (`00306FA4`), `00359A30` (← `00359800`), `0035AB20` (← `00356970`, a thunk) | `00238B70(0)` from `0035A6F0` (← `002628B0`, `003574B0`, a thunk) | `AiOrder_EvaluateAndResolveActionTarget` (`00301511`, returns 0 — no gambit evaluation), `BattleAction_CheckCurrentActionInterruptReason`, `BattleUnit_UpdatePartyCombatStanceState`, `BattleUnit_UpdateCombatFrame`, `BattleUnit_ProcessPendingActionSelectionQueue`, `PartyFollow_ApplyGoal`, `0033D890` (7) | **combat AI suspended** — gambits, stance, pending selections and party follow all stop; always set and cleared together with bit 7 |
| 6 | `0032A200` `0032A217`, the *begin* of the durative script verb **`btlAtelOpenTreasureStart`** (verb `3051`, thunk `0050FBE0`; [the verb table](../../01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-verb-table.tsv)) | `0032A170` `0032A1E3` — the verb's end, reached through the durative dispatcher's pointer | `00313A00` (`00313A40`); `PartyControl_RecomputeSuppressionFromLeaderBattleState` after a load (`0023B056`) | **a treasure is being opened** — the two functions also reset the opening unit's `+0x2C` / `+0x5C` to `0x2001` |
| 7 | `00238AE0(1)` — the same three callers as bit 5, in the same breath | `00238AE0(0)` from `0035A6F0` | in the `0x3080` mask: `BattleTarget_ComputeGlobalEligibilityMask` (`0030B78C`, forces the mask's word to 1) and the message poster `0046AB10` | **presentation veto during the bit-5 pause**: with 12 and 13, no target eligibility and no battle line |
| 8 | `00300FC0` `003010E2` — the unit-teardown path (← `BattleUnit_TeardownAndDespawn`, `BattleStats_ChangeStatusAndProcessSideEffects`) when the removed unit is the focus actor (`PartyFocus_GetCurrentPackedActorHandle`); request `0x17` | the init mask | `00233D20` (`0xF00`) | **the focus actor went down** — request latch `0x17` |
| 9 | `00300FC0` `0030109D` when `00237260()`: every *active* member of kind 0 outside the guest range 7–25 is incapacitated (`0023728D`–`002372B2`); request `0x18` | the init mask | `BattleAction_CheckPresentationSlotReady`; with 10 (`0x600`): `BattleUnit_ApplyMovementIntentToWorldActor`, `PartyControl_Recompute…`, `0031ADB0`, `BattleAction_ApplyKnockbackImpulse`; `00237F40` (`bt 9`) | **the active party is down** (guests excepted) — request latch `0x18` |
| 10 | `00300FC0` `0030106C` when `002372E0()`: every roster member, active slots 0–3 *and* reserve 0–8, is incapacitated (`002372F0`–`00237380`); request `0x0B` | the init mask | `0030A250`, `BattleAction_CheckPresentationSlotReady`, the `0x600` four, `00237F40` (`bt 10`) | **the whole roster is down** — request latch `0x0B` |
| 11 | `00300FC0` `003010CE` when `002373C0()`: the leader (`003137F0` → `BattleUnit_FindByCombatantId`) is incapacitated while `003135C0()`; step 20 sets and clears it every frame by the same test | step 20; the init mask | `00233D20` (`0xF00`) | **the leader is down** (§2.3 step 20) |
| 12 | `00238B00(1)` from `002678C0` (← `0025B600`, `0036FCC0`) | `00238B00(0)` from `ActorManager_BindLoadedDefinitionPayload` (`0026C965`, when its argument is 0), `0025D580`, `002628B0` | the `0x3080` mask | **a definition payload load is in flight** — presentation veto |
| 13 | `00238B20(1)` from `0025B740` (← `ActorManager_RunFieldRuntimePass`): the **focus actor** (`PartyFocus_GetCurrentPackedActorHandle` → `ActorHandle_ResolveRegistryEntryByPackedId`) while `003B7730` (two globals non-zero) and `00265680` hold, its byte `+9` bit 0 and `+8` bit 1 set, its movement context's `+0x14F` bit 0 clear and its `+0x138` attachment present with a non-zero word `+0x88` (`0025B746`–`0025B7C8`) | step 1, at the top of every field frame (`002345B9`) | the `0x3080` mask | **the focus actor stands on a navimap cell whose attribute nibble (bits 3–6) is non-zero** — presentation veto; the word `+0x88` of its movement body is that nibble, written at every placement by `003808A0` ([the movement body page](../../06-Movement-And-Navigation/the-movement-body-pool-and-the-separation-pass.md) §2.4, §2.9; FZ-2 and FZ-10 answered 2026-09-11) — what the nibble means is FZ-11 |
| 23 | `0050F2E0` — **`btlAtelSetDebugRotControlMode`** (verb `3022`, a popped bool) | the same verb | `0050F2B0` — `btlAtelGetDebugRotControlMode` (`3021`) | **the script's debug rotation-control mode**; no native reader |
| 26 | `0050F170` — **`btlSetViewCheckMode`** (verb `3014`, a popped bool) | the same verb | `0050F140` — `btlGetViewCheckMode` (`3013`) | **the script's view-check mode**; no native reader |
| 29 | `0050F380` — **`btlAtelSetRealBattleMode`** (verb `3024`, a popped int; when set also calls `00308DE0`) | the same verb | `0050F340` — `btlAtelGetRealBattleMode` (`3023`) | **the script's "real battle" mode**; no native reader beyond the getter |

Bits 14–22, 24, 25, 27, 28, 30 and 31 have no manipulator or tester in the image, by either
instrument.

**Adjacent layers the frame drives, accounted.** Fourteen edges cross into
**rewards**/progression — `002341C0` calls `00319B10`, `00234590` calls `00319600`,
`00310DB0` calls `00319A00`, and `00265090` is called by `002FB150` — rewards/progression bodies
run inside the field frame's call neighbourhood (what they compute per frame is not read here);
and three reach **platform**/achievements (`0022A770` → `00316930`, `003160C0` → `003148F0`,
`00796E20` → `008655A0`) — the frame also feeds the overlay/achievement plumbing each tick.

## 3. Key addresses

| address | size | what |
|---|---:|---|
| `00314020` | 845 B | `World_UpdateSimulationTick(mode, flag)` — five slots, sixteen sub-steps in mode 0, fixed tail |
| `00234590` | 752 B | `BattleSystem_RunFieldFrameOrchestrator(slot)` — slot 0 only, 23 ordered steps |
| `00233F70` | 467 B | `BattleUnit_UpdateLifecycleAndCombatFrame(slotField, record)` — the per-unit callback |
| `00265A20` | 320 B | `ActorSystem_BindBattleUnitsForEligibleRecords` — installs the callback at record `+0x38` |
| `0025DF00` | 1,228 B | `WorldActor_UpdateRuntimeAndScriptExecutionState` — calls the callback at `0025E222` |
| `0025D9E0` | 1,297 B | `ActorManager_RunFieldRuntimePass(slot)` — [the field runtime pass](../../04-Actor-Entity/the-field-runtime-pass.md) |
| `003DB1F0` | 132 B | per-record post-pass: `+0x63` countdown, `+0xA0` state walk, `003DB6E0` |
| `00234520` | 109 B | slot-0 post-step; the one-shot callback at `0208E6A8` |
| `002623A0` | 152 B | per-slot end of tick; publishes `02099D70` / `02099D78`; `002E5180` over a record range |
| `00267310` | 22 B | slot `+0x201` byte — the sub-step opt-in |
| `0032A100` | 72 B | clock advance: `0208D45C++` when `003EBA90(0)` changed |
| `0035C700` | 61 B | "a UI request is up" predicate over `022C83E8`, `02092730`, `002E12D0` |
| `00306BB0` | 20 B | `022C2160 ∈ {5, 6}` — the special-sequence cinematic is on screen or ending ([the mode ladder](../Battle-Runtime-Mode/battle-runtime-mode-ladder.md) §2d) |
| `002371B0`, `00237140`, `00237260` | 172 / 103 / 126 B | the three party-state predicates behind requests `0x0B`, `0x18`, and the `0x18` latch |
| `0035C7A0`, `0035C8A0`, `0035C8E0` | 10 / 61 / 25 B | raise, set-with-flag, clear a UI request |
| `003135C0`, `003137F0`, `00313760` | 24 / 15 / 115 B | bit-11 helpers and the registry-slot timer step |
| `0022A770`, `0022B8C0`, `0022BC20` | | the three frame modes that call the tick |

### Named callees and their entries

Every function this page names by its ledger name, with the entry the name stands for — so a
reader can go from the step lists above to the function without the index. None of these bodies
was read here beyond what the text says; their pages own them.

| name | entry |
|---|---|
| `ActorManager_GetRecordByOrdinal` | `00358940` |
| `ActorSystem_IsPrimaryBattleSimulationReady` | `002671C0` |
| `ActorWork_GetBattleUnit` | `0031B760` |
| `Actor_SetMovementSpeed` | `0026A330` |
| `BattlePerception_AdvanceCandidateCacheGeneration` | `00325060` |
| `BattlePerception_ResetSpatialVisibilityCacheFrameState` | `0032A650` |
| `BattleUnit_AllocateSlotAndBindActor` | `00234480` |
| `BattleUnit_ApplyMovementIntentToWorldActor` | `0023A070` |
| `BattleUnit_FindByCombatantId` | `0031B770` |
| `BattleUnit_FindMappedDefinitionSelectorByIndex` | `0031B810` |
| `BattleUnit_GetPartyLeader` | `003272A0` |
| `BattleUnit_RebuildPerceptionCandidateCache` | `003247F0` |
| `BattleUnit_ResetActionControlForStatusTransition` | `00300140` |
| `BattleUnit_RunPeriodicCombatMaintenance` | `00310DB0` |
| `BattleUnit_SnapshotWorldActorRuntimeState` | `00236300` |
| `BattleUnit_TeardownAndDespawn` | `00300E40` |
| `BattleUnit_UpdateCombatFrame` | `00308610` |
| `FieldData_GetActiveFieldRecordBit15` | `00313F60` (thunk to `00377C20`) |
| `GameClock_GetRawTickCounter` | `0032A150` |
| `Loot_UpdateWorldPickupLifetimeAndDespawn` | `00319600` |
| `Navigation_HasDataset` | `00383C80` |
| `PartyCombat_UpdateStanceState` | `00307E70` |
| `PartyControl_RecomputeSuppressionFromLeaderBattleState` | `0023B040` |
| `PartyControl_UpdateControlledActorLocomotion` | `00358C60` |
| `PartyFocus_UpdatePrimarySecondaryActorProcessing` | `00358EE0` |
| `PartyFollow_ApplyGoal` | `003246C0` |
| `PartyFollow_SolveFormationWrapper` | `0033B6D0` — a 28-byte wrapper over `PartyFollow_SolveFormation` `00338490` |
| `SpawnGroup_DispatchPendingCompletionSignals` | `00307030` |
| `SpawnGroup_HasPendingCompletionSignal` | `003070E0` |
| `SpawnLifecycle_CheckAndRetireByNativeRange` | `002350C0` |
| `WorldSimulation_ProcessDeferredModeRequest` | `0032FC30` |
| `BuildFilteredFourSlotUnitBuffer` (`BattleUnit_`) | `0030A880` |

### Data

| address | what |
|---|---|
| `02098E10` | actor-manager slot array, stride `0x288`, five slots ticked; `+0x10` bit 0 live, `+0x201` sub-step opt-in, `+0x28` passed to the unit callback |
| `022C2548` | tick in progress: `1` at `00314047`, `0` at `0031435D`; read by `00314960` |
| `022C252C`, `022C2530` | tick counters, `++` at `00314231` / `0031423E`; reset by `00314010` / `00314000` |
| `022C2544` | float added in the time-scale block; written `1.0f` by `00314940` |
| `01EED060`, `01EED064` | deferred request words; the second drives `WorldSimulation_ProcessDeferredModeRequest` |
| `02089340` | battle-state word — **§2.5 reads every bit**: 0 one-shot armed, 1 idle frame, 2 clock did not advance, 3 reset parity, 4 area battle state live, 5 combat AI suspended, 6 script-driven, 7 / 12 / 13 presentation veto, 8 focus actor down, 9 active party down, 10 roster down, 11 leader down, 23 / 26 / 29 script-owned |
| `022C83E8` | UI-request flag word: bits 0, 1, 4 set for requests `0x18`, `0x0B`, `0x17` |
| `0208E6A8` | one-shot callback consumed by `00234520` |
| `0209A2B0`–`0209A2C4` | the block `0025D650` resets every tick |
| `02099D70`, `02099D78` | current slot block and party-focus record, published per slot by `002623A0` |
| `0208D45C` | the raw tick counter, advanced by `0032A100` |
| `02B59D80` | the record table `003E7650` iterates for the presentation-parameter push: live word `+0`, character-render word `+4` |

### The `003E7650` exclusive subtree — the presentation-parameter arm table

`003E7650` owns 51 frontier functions exclusively (FABLE's `exclusive_subtrees.tsv`). §7's
EX-answer names the family at band level; the member-level read (each body disassembled
2026-09-14) splits it into one dispatcher arm, a six-body record-init cluster, and 44 slot
arms in nine recurring shapes. Every arm operates on the same presentation-parameter record in `rcx`;
the cleared dwords are per-parameter "dirty/applied" flags, and the `+0x20` / `+0x70`
sub-records are the two parameter blocks each arm forwards to a shared worker. *(2026-09-19, FABLE: **the index of an
arm is the status bit** - cleared bits are dispatched from `+0x144` and set bits from `+0x140`, and ten statuses have
empty arms; the bit-to-arm table, and the arms that switch rig controllers, are on
[the rig page](../../17-Presentation-Rendering/Character-Render-Records/the-rig-of-seventeen-controllers.md) section 4.)*

**Worker vocabulary** (the shared tails every arm forwards into): `00470050` and `0046FFA0`
consume the `+0x20` block with the **per-arm parameter index** in `edx` (observed
0,1,2,3,4,5,6,7,9,0xD — not a constant); `0051DDC0` and `0051DBF0` consume the `+0x70` block;
`003E1350` / `003E1610` / `003E1310` are the resolve-by-id pair (`0020E600`); `00428F10`
is the commit/notify tail; ~~`0016D6A0` is the string-member release.~~ the call to `0016D6A0` does nothing *(corrected 2026-10-02, OPUS: `0016D6A0` is `ret 0`, three bytes)*.

| arm | shape |
|---|---|
| `0051E3A0` | the dispatcher arm (362 B): two `call rax` indirect sites, `003E7450` + `00428940` + `003B6B10`/`003B6B30` |
| `0051E580`, `0051E6C0`, `0051E7C0`, `0051E880`, `0051E8C0`, `0051E900`, `0051E940`, `0051E980`, `0051EA60`, `0051EC90`, `0051ECD0` | reset field then `rcx += 0x20; jmp 00470050`: cleared fields `+0xDC`, `+0xF4`, `+0x134`, `+0x100`, `+0xEC`, `+0xE0`, `+0xC8`, `+0xE4`, `+0xE8`, `+0xD8`, `+0x12C` |
| `0051E5A0`, `0051E6E0`, `0051E7E0`, `0051E8A0`, `0051E8E0`, `0051E920`, `0051E960`, `0051E9A0`, `0051EA80`, `0051ECB0`, `0051ECF0` | **set** flag dword `=1` then `rcx += 0x20; jmp 0046FFA0` — the set-twin shape (11 arms); the reset/set rows are clear/set pairs |
| `0051E5E0`, `0051EAA0` | reset `+0x120` / `+0xFC` then `rcx += 0x70; jmp 0051DDC0` |
| `0051E600`, `0051EAC0` | **set** `+0x120` / `+0xFC` `=1` then `rcx += 0x70; jmp 0051DBF0` — set twin |
| `0051E5C0`, `0051E5D0`, `0051E780`, `0051E790`, `0051E7A0`, `0051E7B0` | bare field reset and return (11 B): `+0x130`, byte-flag reset, `+0xC0`, byte-flag reset, `+0x13C`, byte-flag reset |
| `0051E620`, `0051E670`, `0051E9C0`, `0051EA10` | reset `+0xD4`/`+0xD0` (or none) then resolve-pair `003E1350`/`003E1610` + `0020E600` ×2 |
| `0051E700`, `0051E740` | reset/set `+0xF8`, run `0051DDC0`/`0051DBF0` on `+0x70`, then `003E1350`/`003E1610` on `[rbx+0x10]` |
| `0051E800`, `0051E840` | ~~set `+0x128` `=1`~~ *(corrected 2026-10-01, OPUS, on reading the bodies: `0051E800` stores 0 at `+0x128` (`0051E809`), `0051E840` stores 1 (`0051E849`))*, then `003E1350`/`003E1610` on `[rbx+0x10]` and `jmp 0016D6A0` on `[rbx+0x10]` — **no `+0x70` work**; the released string member belongs to the resolved member, not the `+0x70` block |
| `0051EAE0`, `0051EB40` | run `00470050`/`0046FFA0` on `+0x20` (call, not tail), then `jmp 00428F10` commit |
| `0051EBA0`, `0051EC10` | `call 00428F10` first, then `0051DDC0`/`0051DBF0` on `+0x70`, tail `jmp 003E1310` |

**The `0047xxxx` record-init cluster** (six bodies, all exclusive to this push): `0046FD00`
(615 B) is the parent init — `003ABCA0` ×6 + `00428CD0` ×4 + `memset`, `003AB960`, and calls
into the four siblings `004703F0` / `004704C0` / `00470590` / `00470660` (195–280 B each, the
same `003ABCA0` + `memset` + `003AB960` + `00428CD0` shape, differing in tail work); `0046FD00`
additionally `lea`-installs `0047xxxx` callbacks into `[rbx+0x18]` — the `call rax` at
`0046FD64` invokes `[rcx+0x18]`; `00D225B0` is a float pool it reads by `movaps`, not a code
table. `00320BB0` (162 B) is the
per-record field accessor `003E7650` calls as `(i, &out, &rec+0x84)` per §7.

### The `0022A770` exclusive subtree — the field frame's helper set

`0022A770` owns 60 frontier functions exclusively. Every member disassembled 2026-09-14;
they fall into ten clusters, several of which §2/§7 already describe at family level — the
table names the members.

| cluster | members | role |
|---|---|---|
| entry gates | `001800E0` (map-art-context byte `+0x41A` — corrected 2026-09-22, see §13 EX-6 note), `001800C0` (ring non-empty), `001BD620` (the ring predicate, 16 B), `001EC760` (2,232 B — the cutscene gate's outer body; **interior read 2026-09-17**: entry `001EC560`→`00265270`, flag `01F832C4` at `001EC7B2`, then six `strstr(sceneName, literal)` tests — `001C50C0` snapshots the scene name from `01F832C8/30`, literals `spc_z0000`, `sum_m0001`, `sum_l0001`, `sum_h0001`, `hne_e0100`, `wdl_b0101` at `.rdata 009025E0`–`00902638`, each match calling the held object's `vtable+0x18` (`001EC800`, `001ECBC3`, …); first literal load at [`001EC7C3`](../../_index/ADDRESS-INDEX.md)), `001EDAD0` (214 B sibling, `001EC560` + `01DFE40C`/`01F832B0` globals), `001EC690` (7 B ~~`01F832C4` flag read~~ *(corrected 2026-10-01, OPUS, on reading the bodies: it increments dword `01F832C4` (`inc` at the entry) and returns)*) | the mode-2 skip conditions §7 EX-6 decodes |
| request predicates | `002335D0` (`0036FFD0`/`0036FF70` ×4), `00233640`, `00233700`, `00239790`, `002370A0`, `00184740` (103 B — `0024DE30` gate), `00263E80` (`002E97B0`) | the `00229ED0`/`002DE250`/`002DDDA0`/`00182FB0`/`00229E20` predicate family §8's evidence row cites |
| one-shot and flag accessors | `002361A0` (`0208E6B4`), `0023B200` (`0208E6B8` + `0036FFE0` ×2), `00250180` (`020927DC`), `0024FCE0` (`02F97348`), `00259970` (`02097B80`), `0025E3F0`, `0026F9D0`, `00466170` | single-global read/write stubs |
| `022C7F92` flag-word accessors | `00358280`, `00358290`, `00358370`, `003583A0`, `00358410`, `00358550`, `003586A0` | 8–31 B getters/setters over flag word bytes `022C7F92`–`022C7F9A` (e.g. `00358370` = `word & 1`) |
| scene/camera state writers | `00255CF0` (389 B), `00255FF0` (422 B), `002563F0` (`020964F0`–`02096500` byte band), `00256F60` (714 B) | the `00263EB0`/`00358320`/`002EA6A0`/`00263C30`/`003587C0`/`0026A3B0` cluster writing into `022C6F28` (the character-render record array) and `02AEDDB0`/`02AEDEF0` (camera matrix) |
| mode-transition arms | `0027EFA0` (143 B: conditional `002EFD20(3)` → `002EFA70`, `0035C7B0(0xB)`, `00252B40(0xB,1)`, `[+0xC8]=2`, `+0xDEE` byte clear), `002805D0` (`0035C740` + `02092730`/`0209AC30` globals) | field-frame mode/arm transitions; `0209AC30` is the fade-request flag's block |
| vtable-dispatch bodies | `002FBA60` (618 B — a `TsElementType` string mapper: `00D0F9F0` is a string constant; its dispatch tables are `002FBCCC`/`002FBDEC` — AUDIT-SEM rev 8681), `002FC4A0` (898 B — 15 rip-indirect vtable calls + `memset` ×4 + `0019C5D0` ×4), `002FCF00`, `003B2220`, `003B25D0` | heavy dispatch/init bodies the frame's sub-steps invoke |
| tick arm | `003143D0` (59 B), `0017DEA0` (276 B) | one sub-step arm: `003DAA20` + `003DA2F0` + `003DD210` + `00255810` + `0037D890` + `0025E3F0`; `0017DEA0` runs the `00198790`/`00197710`/`0079E6A0`/`00239790` ×3 quad-block step |
| actor-manager slot accessors | `00264610` (`02098E10` — the slot array above), `0026B730` (`02098E58`), `0026E260` (`0209A670`), `002506D0` (`0208EA48` + seven-helper chain), `00254E50` (`002805D0` tail) | per-slot state reads the frame consults |
| state-byte and float evaluators | `00258B90` (`02092628`–`02092632` byte block), `00258D70` (`0024B9B0` ×7 + alloc pair `0036C1D0`/`0036C140`), `003D83A0` (2,190 B: `0020E600` ×3 + `sqrtf` ×2 + `00430B90`/`004309C0`/`0036DD80`), `003D9150` (float step: `00861F1A` + `0025A520`/`0025A500`/`0025A2C0`), `0036F460`, `0036F530`, `0037A450`, `0037D4C0`, `0037D970`, `003ECAC0`, `003ECCA0`, `004678E0`, `00468520`, `003CD820` | the frame's parameter evaluators and camera-bank (`02AED5F0`–`02AED604`, `02AEDF10`–`18`, `02CA6010`/`20`) writers; `003ECCA0`→`003ECAC0` ×2 is a paired camera-step |

### The `00314020` exclusive subtree — the simulation tick's helper set

`World_UpdateSimulationTick` owns 38 frontier functions exclusively. All disassembled
2026-09-14; the dominant cluster is the party-focus block at `022C7FE0`–`022C8028` and the
`003Exxxx` perception-update family.

| cluster | members | role |
|---|---|---|
| party-focus / actor processing | `00358EE0` (`PartyFocus_UpdatePrimarySecondaryActorProcessing` — `002671F0` ×4 + `0025A620` ×3 over `022C7FE0`/`E8`/`EC`), `00358A20` (actor resolve `003588B0` + `002E7E50`/`00235EA0`), `00358C60`, `00358CB0` (545 B — the capability/unit gather: `00265680`/`00264DF0`/`0026D810`/`00268620`/`00265830` + `00861F02`), `003594E0` (`sqrtf` ×2 + `001E0C10`/`0017DFC0`), `00359800`, `00359880`, `00359A30` | the focus-actor and party-state chain that writes `022C7FE0`–`022C8028` |
| `003Exxxx` perception update | `003E7EC0` (`02B5D080` gate), `003E8020`, `003E8440`, `003E85B0`, `003E8690`, `003E8990`, `003EB9A0` | `003E8190` ×N + `004735D0`/`00473500` + `0037A2xx`/`0037Bxxx` + `0026FAxx`/`002700F0` shape; `003E8A10`/`40`/`70` are 38-byte two-arm conditional forwarders (`test edx,edx; je` → call A else call B, `ecx=0`) — `003E8A10` selects between the `0037A3B0` pair, `003E8A40` between `0037A1D0`/`0037A130`, `003E8A70` between `0037B190`/`0037B0F0`; a binary select, not an RVA-table dispatch |
| request mailbox | `002E0940` (`00254440` + `0215F1AC`/`0215F1B0` — the three mailbox cells §7 names), `002E15F0` (`0215F1B2`), `002E8700` (`022C6F28` read), `0025D950` (calls `00226B10`/`002E15F0`, reads `02099DA3`/`02099DA5` deferred-request bytes) | the router-facing request cells |
| audio listener | `00361700` (the `(x, 0)` step the listener update calls), `00362DA0` (`022CBA9B`), `00362DB0` (`022CBB28`), `00363A90` (`00362DC0`), `003606E0` (`022CB9DC`/`E4`) | listener-block byte accessors around `022CBA80`–`022CBB0C` |
| flag stubs | `00259AF0` (`02098DEC`), `0025D640`, `002673F0` (`02098E23`), `0025A620` (`02097D20` + consts `008F3108`/`009156E0`) | single-global reads |
| evaluators | `0037C1A0` (resolve `0020E600` ×2 + `00263750`/`0020E620`/`002DEBD0`/`002DEB90` + ~~`0016D6A0` free~~ `0016D6A0`, a `ret 0` stub *(corrected 2026-10-02, OPUS: `0016D6A0` is `ret 0`, three bytes)* + `002EA6A0`/`0037B4D0`), `003DE640` (`003ABD00` ×2 over `02B58C58`/`02B59358`), `003DF670` (`003590D0`/`003588B0`/`002EA6A0`/`0029CAB0`), `004742A0` (777 B — `sqrtf`/`00861F02` ×2 each + `002DDCF0`/`00380800`), `0046AFA0` (`02CA6040`–`4C` const bank) | mixed per-tick evaluators |
| list/table readers | `003DAA40` (`02B4E4C0` — the `0x130`-stride separation-pass list of EX-4 — plus `02B57CE0`), `0036E1E0` (`0024DE70` + `022D94B0`), `0036FD90` (`00809728` tail), `00268650` (`003587C0`/`003589B0` + `0209A2B4`/`B8`), `0017DFC0` (the `00198790`/`00197710`/`0079E6A0` quad + `00796E20`) | table reads feeding the sub-steps |

### The `00234590` exclusive subtree — the orchestrator's 31 helpers

`BattleSystem_RunFieldFrameOrchestrator` owns 31 frontier functions exclusively. All swept
2026-09-15 (`bshape.py`); the tree is dominated by one populate monster and a `022C2xxx`/
`02EBF138` step family:

| cluster | members | role |
|---|---|---|
| scene populate | `00338490` (4,101 B — `00265090` ×4, `00309AE0` ×4, `00203080`/`003135C0` ×3, `003272A0`/`002646C0`/`004687F0`/`00202B10`/`00263C20` ×2, plus `00383C80`/`0033CB70`/`0033D3E0`/`00391410`/`00384130`/`00336390`/`004692F0` and consts `008F3138`/`008F8180`/`00915620`), `00339A60` (390 B — `002646C0`/`00265090` ×2, `003272A0`, `022C7E00`/`30`/`80`), `0033A3D0` (405 B — `0033D3E0` ×5 + the `0020xxxx` resolve set, `00D10B18`), `0033B6D0` (→ `00338490`) | the orchestrator's one heavy populate — instantiates the field's scene state |
| `022C2160` step family | `00306B10` (`0032F6C0` + `0023B020`), `00306BD0` (284 B — `0032F6E0`/`00309230`/`0032FC30`/`0032ED70`/`0020E600`, `02EBF138`), `0030CE10` (`0020E600` ×5 + `00306BD0`), `0030CBE0` (556 B — `0020E600` ×2 + `0031B7E0`/`00322C50`/`0030C890`/`0030A190`/`00328360`/`003226D0`/`003098D0`/`00325B40`/`00325B30`/`0030CE10`/`00306B10`, `022BE978`), `0030C890` (`003098D0`/`00325A20`/`0030A190`/`0031A230`), `00309230` (`00D103B0`/`C0`/`D0` table + `02EBF138`) | the per-step bodies the orchestrator's 23 steps call — `022C2160`/`022C2168` is their shared state pair, `02EBF138` their context |
| record accessors | `002F82F0` (`0030C300` ×2 + `003148F0`/`003EC700`, `022BE944`/`48` + `02EC3EA0`/`C8`), `002FCAC0` (`02EC19C0`/`02EC3D60`), `0031A230` (→ `002FCAC0`), `00325A20`/`00325AD0` (`003202F0` + `02EBF180`), `00325B40` (`00313F60`/`00325AD0`), `003226D0` (`0024DE70`), `003246C0` (`0030A880`/`00339A60`) | record fetch/step ops over `02EBFxxx`/`02EC3xxx`/`022BExxx` |
| cell accessors | `0032A650` (`022C2564`/`68` + `022C26A0`), `0032A690` (`02AEDEF0`), `0032A6B0`/`0032A6C0` (`0209A670`), `00263B50`/`00263C50` (`02098E10` — the actor-manager slot array), `00325060` (`022C2578`), `00392740` (702 B — `00392200` ×3 + `0032A6B0` ×2 + `0032A6C0`/`0032A6E0`, `02AEE060`–`B8`), `0023B020`, `00328360`, `003DC410`, `0042FCE0` (`02CA4ED4`) | slot/cell reads — `00392740` is the cluster's one real body (the `02AEE0xx` bank) |

Not established: which of the 23 steps `0030CBE0`/`0030CE10` implement, and the `00D103B0`
table's case↔step mapping.

### The `002628B0` exclusive subtree — the manager unload's 26 helpers

The manager-slot unload `002628B0` (EX-9's drain-side function) owns 26 frontier functions
exclusively. All swept 2026-09-15 (`bshape.py`):

| cluster | members | role |
|---|---|---|
| `02B5xxxx` record banks | `003DC710` (`02B57F70`), `003DD380` (`0020E600` + `0041E490`/`00369800`, `022C6F28` + `02B581A4`), `003E75A0` (`0024CFF0`/`00470000`/`0051DC60`, `022C6F28` + `02B59EA8`), `003EB500`/`003EB5F0` (239/201 B twins — `002ED470`/`002EB870`/`00265F90`, `02B5EA20`/`02B5EB20`/`70`), `003EC5F0` (`00377C20`/`003EB6C0`), `003EC690` (`002EBD60`/`002E3DC0`, `02B5EC94`) | the manager's own record banks, torn down per slot |
| listener/scene cells | `0035B5D0` (`0035B1A0` ×2, `022C8030`/`02EC0B82`/`02EC0F82`), `00360DD0` (`002DEC00`/`002DEDE0`/`002DEC20`, `022CB9F1`/`022CBA51`), `003605A0` (`022CB732`), `0036E080` (`022D97B0`/`98B0`/`99B0` triple), `00366A00` (`00245020`, `022CBE20`) | the unload's cell clears across `022CB7xx`–`022D99xx` |
| request/mailbox | `002E06F0` (`002A2720`/`002F1C50`, `0215F1B6`/`0215F200`), `002EECC0` (`003E5E20`/`0042FAE0`, `01EEBAB0` + `022C6F28`), `002E8CC0` (`022C6F28` read), `00252DE0` (`002B6260`/`003C5E50`/`003BBCF0`/`00366A00`) | the unload's pending-request flush |
| leaves | `002E0670`, `002E63B0`, `00360100`, `003603F0` (`003601C0` ×2 + `00360A50`/`003600D0`/`002EFA70`/`002260E0`), `00362830`/`00362840`, `003B6C20` (`02EBCBE0`), `003BBCF0`, `003DA180`, `003E9100` (`00408200`) | small clears and forwarders |

### The `00362850` exclusive subtree — the audio listener's 10 helpers

The audio listener update (`00362850`, §7 EX-3) owns 10 frontier functions exclusively: the
vector-transform wrappers that feed it positions, plus its own `02FD4xxx` listener-state
machinery. Interior cites are one instruction inside each declared extent (`interior_cite.py`;
no boundary crossings).

| cluster | members | role | interior |
|---|---|---|---|
| transform wrappers | `001DC090` (42 B), `002DF410` (10 B), `001DC390` (61 B), `002DF560` (148 B) | `001DC090` — `00210B30` resolve then tail `00211140`; `002DF410` — arg shuffle tail into `001DC090`; `001DC390` — `00210B30` resolve then tail `00211340` (xmm2→xmm3); `002DF560` — `003603C0` gate, `003CBFA0` reads the `02E0D5xx` vec3, builds `{x,y,z,1.0}` and calls `001DC390` | `001DC0B5` / `002DF415` / `001DC3C8` / `002DF5D7` |
| vector math | `00211140` (114 B), `00211340` (142 B) | `00211140` — builds the `007A4380` stack object (`007A4C40`/`007A47A0`/`007A46F0`), `cvtdq2ps`/`divss` normalizes two int args, edx `7` op; `00211340` — `007A5B00` construct, `007A5670` over the two arg vec3s, `001243B0` teardown | `0021118C` / `002113B3` |
| listener state | `00362C60` (181 B), `00362D20` (127 B), `00362E50` (261 B) | `00362C60` — the `02FD4xxx` state driver: `002DEE80` ×2, `003636A0`, `002DF150`, stamps `0x7F` defaults, byte counter + flag byte; `00362D20` — blend accumulator: `acc += rate`, clamps at `1.0`, lerp `b·(1−t)+a·t` → int cell; `00362E50` — `0020E600` row over the `02FD4xxx` bank, `comiss` against the arg float on `[rec+8]`/`[+0xC]` | `00362CFE` / `00362D42` / `00362E92` |
| entry sweep | `00363F30` (149 B) | walks `rbp` word entries at `[rcx]+2`; each resolves into `022CBAF0`; when `byte[+8]&0x70==0` and the `022CBB2E` flag is set (and the arg permits) → `002DF0F0` release + clear `+8` bits 0/6 and `+4` | `00363F8F` |

`00210B30`, `0020E600`, `007A4380`/`007A4C40`/`007A47A0`/`007A46F0`/`007A5B00`/`007A5670` and
`002DF0F0`/`002DF150`/`002DEE80` are shared callees — deliberately not census members.

## 4. Data structures and formulas

**The three mode arguments and what they select** (section 2.2): `0` → sixteen sub-steps over
five slots and the full tail; `1` → slots 3–4 once and the tail; anything else → the tail only.
The return is `mode == 0`.

**The sub-step opt-in**: `run(step, slot) = (step == 0) || (*(u8*)(0x02098E10 + slot*0x288 + 0x201) != 0)`.
**Passes per frame**: `1 + 15 × [byte(slot) != 0]`, the same work each pass (section 2.2a);
`byte(0) == 0` always — its only setter refuses manager 0 and its loader writes 0.

**The reset-loop parity**: the loop runs iff `00253B90() != ((02089340 >> 3) & 1) ^ 1`, and running
it toggles bit 3 — a two-frame cadence under a steady predicate.

**Unit flags this page fixes**: bit 1 (frame is a no-op), bit 3 (required), bit 4 (simulated —
the activation arm sets it), bit 16 (must be clear), bit 24 (excluded from the reset loop), bit 33
(teardown on the idle path). Bits 33 and 47 are also set by [group completion](../../05-Spawn-Encounter-Lifecycle/Group-Completion-And-Respawn/when-a-group-is-wiped-and-when-it-comes-back.md)
§5's reaction case, which as of that page's amendment has no static caller.

## 5. Call chain

```
frame dispatcher 0022A580 (mode byte 02064AD3)
  mode 2  0022A770 ---- World_UpdateSimulationTick(0, edi)     0022ABD8
  mode 3  0022B8C0 ---- World_UpdateSimulationTick(1, 1)       0022BA23   "ATEL CONTROL"
  mode 5  0022BC20 ---- World_UpdateSimulationTick(1, 1)       0022BCCF   "ATEL CONTROL"

World_UpdateSimulationTick
  -> WorldSimulation_ProcessDeferredModeRequest(0, 01EED064)   when pending
  -> per slot / sub-step:
       BattleSystem_RunFieldFrameOrchestrator(slot)            slot 0 only: the 23 steps of section 2.3
         -> SpawnGroup_DispatchPendingCompletionSignals         step 17
         -> BattleUnit_ResetActionControlForStatusTransition   step 6, per unit, every second frame
       ActorManager_RunFieldRuntimePass(slot)                  the actor drive loop
         -> WorldActor_UpdateRuntimeAndScriptExecutionState(record)
              -> [record+0x38] == BattleUnit_UpdateLifecycleAndCombatFrame   0025E222
                   -> SpawnLifecycle_CheckAndRetireByNativeRange   active path, last
                   -> BattleUnit_TeardownAndDespawn(unit, 0)       idle path, bit 33
       00234520(slot)                                          slot 0 only; the 0208E6A8 one-shot
       003DB1F0(slot)                                          the +0x63 countdown
  -> 002623A0(slot)  per ticked slot
  -> the fixed tail (section 2.2), ending 002EEEB0 ; 022C2548 = 0

ActorSystem_BindBattleUnitsForEligibleRecords
  -> BattleUnit_AllocateSlotAndBindActor ; record+0x38 = 00233F70   00265A9F, 00265AA8
```


### The `0022B8C0` exclusive subtree — the full-menu frame's 8 helpers

`MainLoop_UpdateAndRenderFrame` (`0022B8C0`, the mode-3 frame above) owns 8 frontier functions
exclusively — the small state readers/writers and one-off passes scattered through its ~90-call
body. Every member was disassembled from the shipping image; interior cites are one instruction
inside each declared extent.

| member | role | interior |
| --- | --- | --- |
| `00181B20` (102 B) | a widget refresh on the `001EBA40` `0x2E0` object: `[rax+0x278]` handle, `00189120` getter ×2, `00186910`, byte `[rax+8]` selects the arg, `0018CA40` then `0018B8B0(...,4)` | [`00181B32`](../../_index/ADDRESS-INDEX.md) |
| `00181DB0` (31 B) | `setne` over `001EB990(001EBA40())` — returns whether the object's flag pair is raised | [`00181DBC`](../../_index/ADDRESS-INDEX.md) |
| `001EB990` (24 B) | `al = ([rcx+0x26E] != 0) || ([rcx+0x26D] != 0)` — reads the flag pair `001EBC70` writes | [`001EB990`](../../_index/ADDRESS-INDEX.md) |
| `00258E40` (106 B) | the mode-3 arm's UI/VFX sequence: `0036C1D0(8,0xA)`, `2/[01DFE0B4]` division, `003CCF20`/`003B4840`/`003D7DC0`, `02F8F320=1`, `0024B9B0(0,3)`, `0036C140`, `02096885`/`0209688C` gate → `003D8190` | [`00258E74`](../../_index/ADDRESS-INDEX.md) |
| `00258EB0` (38 B) | the `02064AA0`-arm's shorter variant: `0036C1D0(2,0xA)`, `0024B9B0(0,4)`, `0036C140` | [`00258EB4`](../../_index/ADDRESS-INDEX.md) |
| `002D0570` (8 B) | publishes `rcx` into `0209E630` — the root registers `0022BEB0` here | [`002D0570`](../../_index/ADDRESS-INDEX.md) |
| `002E1BA0` (15 B) | raises the two flag bytes `0215F1AE`/`0215F1AF` — run near the frame's tail | [`002E1BA0`](../../_index/ADDRESS-INDEX.md) |
| `0037CF00` (67 B) | 4-iteration clear pass: `00263750(i)` for i in 0..3, non-null entries get `002E49B0(obj,0)` + `002E4A40(obj)` | [`0037CF12`](../../_index/ADDRESS-INDEX.md) |

`001EBA40` (the `0x2E0` lazy singleton) and the `0024B9B0`/`0036C1D0`/`0036C140` helpers are shared
callees with other callers — deliberately not census members.


### The `0026CE60` exclusive subtree — the manager-runtime init's 8 helpers

`ActorSystem_InitializeManagerRuntime` (`0026CE60`, the per-set-bit call of §"slots") owns 8
frontier functions exclusively — the reset battery and the leaf initializers that fill the
`0209BE80` manager object's flag word and the `02B44xxx` state banks. Every member was
disassembled from the shipping image; interior cites are one instruction inside each extent.

| member | role | interior |
| --- | --- | --- |
| `00253A30` (67 B) | the reset battery: eight calls in fixed order (`00365980`, `003BBCD0`, `0035BB70`, `003C5F00`, `003CB410`/`003CB440`, `00366940`, `00366740`), zeroes `020927C8`/`020927CC`, tails `0028F2A0`. OPUS's field-map worked example reads it as a *teardown*; the body only proves an ordered reset — teardown vs re-init is not named by the bytes | [`00253A43`](../../_index/ADDRESS-INDEX.md) |
| `003BBCD0` (27 B) | `memset(02B443D0, 0, 0x1400)` and publishes the base at `02B457D0` — the state-bank clear | [`003BBCD9`](../../_index/ADDRESS-INDEX.md) |
| `003C5F00` (170 B) | the bank init: `or [02B45A00],1`, `memset(02B46280,0,0x1430)` ×2, a 19-entry `seta` flag fill at `02B45A04` (entries `0xE`–`0x11` get 1), `memset(02B45850,0,0x120)`, `003148F0` ×2 + `003C5410`, `02B45970=0`, then `0028FAF0`/`0028FF00`/`00290960(1)` | [`003C5F41`](../../_index/ADDRESS-INDEX.md) |
| `0028FAF0` (75 B) | on the `[0209BE80]` manager object: `or [rax+0x10F68],0x100`, `003F8EC0(rax+0xA0)`, `004FE3C0(rax+0x80)` — flag raise + two sub-object inits | [`0028FB00`](../../_index/ADDRESS-INDEX.md) |
| `0028FF00` (29 B) | if `[0209BE80]` and its `[+0x10F80]` pointer are both non-null → `002C63D0` — a conditional dispatch on the manager | [`0028FF0C`](../../_index/ADDRESS-INDEX.md) |
| `00290960` (34 B) | toggles bit `0x800` of `[0209BE80]+0x10F68` to the `ecx` argument — the flag setter `003C5F00` calls last | [`0029097B`](../../_index/ADDRESS-INDEX.md) |
| `002EA650` (59 B) | clears `0215FD44`/`0215FD45`, runs `003E7C70()`, tails `003E7CC0(1|0)` on `0215FD44` — a flag-reset + conditional notify | [`002EA656`](../../_index/ADDRESS-INDEX.md) |
| `00366740` (107 B) | lazy singleton `022CBE20`: `00244F50(0xE0, &00366B80, &out, &022CBE18)` factory + `00246AC0`, under a stack-cookie guard | [`00366785`](../../_index/ADDRESS-INDEX.md) |

`0035BB70`/`003CB410`/`003CB440`/`00366940`/`0028F2A0`/`002C63D0` and the `003148F0`/`003C5410`/
`003F8EC0`/`004FE3C0` helpers are shared callees with other callers — deliberately not census
members.


### The `002EEEB0` exclusive subtree — the fixed tail's 8 members

`002EEEB0` is the fixed tail §5's chain ends on (18 B): `002EE430()` then tail `002EF050` —
the scheduled-record driver plus the phase-wrap pass. The exclusive census assigns it **8
frontier functions**. Every member was disassembled from the shipping image; interior cites
are one instruction inside each extent.

| member | role | interior |
| --- | --- | --- |
| `002EE430` (1390 B) | the scheduled-event driver: stamps iteration ids into `01EEBAA8`, rolls the `021642xx` pending-id ring, and dispatches each entry through `002E99C0`/`002EAE20`/`003EC580`/`0042FB80` and the member set (`002EE1D0`, `002EE290`, `002EDC90`, `002ECA30`, `002E9C30`), ending each pass with `002EED80` | [`002EE8B8`](../../_index/ADDRESS-INDEX.md) |
| `002EED80` (290 B) | the ring roll: when `0216420C` is 1, shifts the `02164238`–`0216426C` seven-dword history window forward, clears `01EEBAA8`, runs `002EEB20` ×2 | [`002EED9E`](../../_index/ADDRESS-INDEX.md) |
| `002EE290` (323 B) | a normalize pass: bumps `[rdx+0x1C]`, clears `[rdx+0x18]` bit 2, `0042FB80` queue op, resolves the `0x740` record; when `+0x160`/`+0x164`/`+0x168` are not all 1.0 it writes four 1.0s at `+0x330`–`+0x33C` and calls `00420D50` | [`002EE36F`](../../_index/ADDRESS-INDEX.md) |
| `002EE1D0` (189 B) | a validated write: `02161DA0` (`NameBindingSubRecord`) lookup (`word[+0x1E]` ×`0x120`, `[+0x5C]` stamp check), `registeredMask`-gated `valueIds[r8]` read at `[rbx+rax*4+0x60]`, then two `0x740` resolves storing `0020E620` image pointers at `+0x42C`/`+0x430` | [`002EE241`](../../_index/ADDRESS-INDEX.md) |
| `002ECA30` (124 B) | a flag-set on the `02161DA0` records: `1<<r10` set/clear in `liveMaskByEntry` (`[r9+0x40]`) per `r8d`, gated on the `+0x24|+0x28|+0x34` permitted union, with a bit-0 normalize (`+0x40` collapses to 0/1 when bit 0 is a permitted bit) | [`002ECA7F`](../../_index/ADDRESS-INDEX.md) |
| `002E9C30` (43 B) | the validated `02161DA0` lookup itself: `word[rcx+0x1E]` ×`0x120`, returns the record iff `ownerGenerationStamp` `[+0x5C]` matches `[rcx+0x24]` | [`002E9C50`](../../_index/ADDRESS-INDEX.md) |
| `002EDC90` (40 B) | the `0x740` resolve + `+0x284` gate → `00427280` (`cx == -1` skips) | [`002EDCAA`](../../_index/ADDRESS-INDEX.md) |
| `002EF050` (165 B) | the phase-wrap pass: 10 ids at `01EEBAB0`, each `003EC580`-resolved record with `[+0x6E0]==0` gets `+0x124 += [0215FD40]`, wrapped below 2π (`01CEBC78`) by `x − 2·floor(x/2π)·π` (`01CEBC50`) | [`002EF0A5`](../../_index/ADDRESS-INDEX.md) |

`002E99C0`/`002EAE20`/`002EB5E0`/`002EEB20`/`002EDAA0`/`002EDD20`/`002EDE20`/`002E4C30`,
`003203B0`, `003EC580`, `0042FB80`, `00426C90`, `00426E20`, `00427280`, `00420D50`,
`004288B0` and `0020E620` are shared callees with other callers — deliberately not census
members.

### The `002E09A0` exclusive subtree — the mailbox drain's 6 helpers

`002E09A0` is the router input-mailbox drain in the fixed tail (1,002 B, EX-3 above). The
exclusive census assigns it **6 frontier functions**. Every member was disassembled from the
shipping image; interior cites are one instruction inside each extent. The slot array it
walks is the eight `0x68`-stride records at `0215F200` (`lea r15` at `002E09E4`).

| member | role | interior |
| --- | --- | --- |
| `00267360` (50 B) | the slot-0 probe called after the walk: indexes the `0x288`-stride table at ~~`0209BE10`~~ `02098E10` *(corrected 2026-10-02, OPUS: `00267360+0xA` `lea rax, [02098E10]`)*, and when `+0x10` bit 0 is set returns `([+0x11] & 1) \| ([+0x10] >> 7)` — its result decides whether the pending byte `0215F1A0` survives (`002E0B8B`–`002E0C65`) | [`0026737B`](../../_index/ADDRESS-INDEX.md) |
| `002A28B0` (46 B) | the state-6 completion probe: sign-extends `byte[rec+0x3B8]` into the eight-qword registration table `0209C4D0`, and returns `([rec+0x40] >> 9) & 1` only when the table slot still points back at the record | [`002A28C6`](../../_index/ADDRESS-INDEX.md) |
| `002A2A60` (75 B) | the per-record status query: dispatches on `byte[rec+0x180]` (0–7) through the RVA table at `02A2AAC` (image-base relative) and returns code 1–5, which the root maps to slot states 1/3/4/5/8 (`002E0AB7`–`002E0AD7`) | [`002A2A7C`](../../_index/ADDRESS-INDEX.md) |
| `002A38C0` (158 B) | the mailbox-mode setter: stores its arg at `0209C62C`, runs `003EC830`/`003EC810` for mode 1/0, then sweeps the same `0209C4D0`–`0209C510` pointer table — mode 1 calls `002A3730(obj, 1)` per entry; mode 0 clears `+0x3C5` when `[+0x44] & 0x180000 == 0x180000` and `+0x3F3` bit 7 when `== 0x100000` | [`002A38F5`](../../_index/ADDRESS-INDEX.md) |
| `003591F0` (8 B) | a request-word store — `word[024C7FFC] = cx`; the root calls it with 0 (`002E0CF5`) to clear the word on the post path | [`003591F0`](../../_index/ADDRESS-INDEX.md) |
| `00404D70` (66 B) | the deferred-enable arm: sets `+0xC8` bit 3 on `02B62D80` unless bit 1 is set, and `+0xC8` bit 7 on `02B62D88` unless bit 5 is set; `00265680()` selects it over `00404DC0` at the tail (`002E0D45`–`002E0D6E`) | [`00404D9C`](../../_index/ADDRESS-INDEX.md) |

`00267310`, `002A2830`, `002A3730`, `00248F00`, `00263FF0`, `00265680`, `00360360`,
`0036D830`, `0037B330`, `003EC810`/`003EC830`, `0053DD10`, `00229F00`, `00253BC0`,
`00254B50` and `00404DC0` are shared callees with other callers — deliberately not census
members.

### The `002341C0` exclusive subtree — the area-teardown reset's 5 helpers

`002341C0` is the 62-byte reset battery the unload path (`← 002695A0 ← 002628B0`) runs —
the same body whose `002341E4` `and` clears bit 4 of `02089340`, the "area battle state
live" bit the resolvers gate on. Its calls, in order: `0030FE60`, `00383A20`,
`00306570(0)` (the one-shot nul), `00392710`, `002FAEC0`, `0031BD60`, the flag clear,
`00325080`, `00319B10`, and tail `002FA470`. The exclusive census assigns it **5 frontier
functions**; every member was disassembled from the shipping image.

| member | role | interior |
| --- | --- | --- |
| `00392710` (45 B) | ~~releases `[02AE82A0]` through `003844F0` when set, then tail-memsets `00861EC0(02AE8060, 0, 0x460)` — the 0x460-byte block contains the pointer cell~~ *(corrected 2026-09-28, FABLE, Claude Opus 5.5, on ASTRA's nav-grid teardown: the two cells were mis-copied; re-derived in [`fable-returns-0928j`](../../_index/candidates/fable-returns-0928j/README.md))* **The nav grid's teardown.** It releases the grid block `[02AEE0A0]` through `003844F0` when the pointer is set, then tail-memsets `00861EC0(02AEE060, 0, 0x460)`: the 0x60-byte `NavGridParams` block, pointer cell included, and the 0x400 bytes after it. The root below that range is not cleared. The block is built only by `BattleSystem_InitializeAreaState` `002342F0`, whose rebuild is the pointer's one store and releases no earlier block. So a grid lives from area initialisation to this reset on area unload. Not established: whether initialisation can run twice without an unload between (the first block would then be lost), and whether the 0x400 bytes are one 128-entry table | [`0039271B`](../../_index/ADDRESS-INDEX.md) |
| `002FAEC0` (12 B) | clears the tag cell — `qword[022BE948] = 0` | [`002FAEC5`](../../_index/ADDRESS-INDEX.md) |
| `00325080` (11 B) | `BattlePerception_ResetCandidateCacheGeneration` — `dword[022C2578] = 7` | [`00325085`](../../_index/ADDRESS-INDEX.md) |
| `002FA470` (175 B) | the tail: appends tag `[022BE940]` into the 3-deep dedup ring at `02EC3E60` (3 × 0xC-byte records `{tag, 0, 0xFF}`) when absent — head `02EC3E84` advances mod 3, count `02EC3E88` clamps at 3 — then falls into `002F7FA0` | [`002FA4A6`](../../_index/ADDRESS-INDEX.md) |
| `002F7FA0` (158 B) | a mod-3 cyclic rotation over the ring's 0xC-stride records: for each entry whose `+0` equals the tag, up to three swaps rotate it through the ring bounded by `[+0x24]`/`[+0x28]` (the 0x55555556 magic-div does the mod-3) | [`002F7FF3`](../../_index/ADDRESS-INDEX.md) |

`0030FE60`, `00383A20`, `00306570`, `003844F0`, `00861EC0`, `0031BD60` and `00319B10`
are shared callees with other callers — deliberately not census members.

### The `0025D9E0` exclusive subtree — the field-runtime pass's 5 helpers

`ActorManager_RunFieldRuntimePass` (`0025D9E0`, 1,297 B) is the per-slot drive the
actor loop calls — it operates on the script-record at `02098E10 + slot × 0x288`
(the same table the `0025E4C0` trace marker indexes) and walks the record's flag
bytes: `+0x10` low bits = run enables, bit 7 → `+0x11` bit 0, `+0x11` bits 2/3
gates, `+0x12` = pending-wake list nonempty (drained through `0025DF00` +
`003DB280` until bit 6 shows), `+0x17` bits 4/7 = suspend/active. The
`[rbx + 0x200] & 2` body iterates a 4-entry pointer table at `020AA1F0`-side
`r13` chain raising `+8` bit `0x40`. The exclusive census assigns it **5 frontier
functions**; every member was disassembled from the shipping image.

| member | role | interior |
| --- | --- | --- |
| `00234150` (104 B) | four-slot conditional cleanup — `0031B810(i)` for i = 0–3, and when `[obj] & 0x10` is set calls `00308010(obj, 1)` then dispatches `obj, 1` through `00300D60` on success else `00300DC0` | [`00234184`](../../_index/ADDRESS-INDEX.md) |
| `00254A90` (46 B) | deferred-flush service — `0035C620()`, and when `dword[02092744] == 0` runs `00251F40(dword[020927E8])` and ORs `0xC` into `word[020CC2AC]`; tails into `001D6C20` | [`00254AA2`](../../_index/ADDRESS-INDEX.md) |
| `00259FB0` (34 B) | two-rate tick — `00259620(float[02098DFC])` then tail `0025A0C0(float[02098E00])` | — |
| `002677B0` (40 B) | flag predicate — returns 1 iff `003148D0()` has bit 3 set and bit 4 clear | — |
| `00363A80` (7 B) | one-byte setter — `byte[022CBA91] = cl` | — |

Shared callees deliberately outside the census: `00583920`, `0032F6E0`,
`0026A5F0`, `003603C0`, `0025E400`, `003590D0`, `003588B0`, `00377DB0`,
`0032FC30`/`0032F6C0`, `0025DF00`, `003DB280`,
`002620E0`, `003148F0`, `002EF2B0`, `003EAA70`, `00361010`, `0037C8F0`,
`0037C860`, `00360D60`, `0037CB40`, `00269860`, `00261F90`, `0031B810`,
`00308010`, `00251F40`, `001D6C20`, `00259620`, `0025A0C0`, `003148D0`.

## 6. Modding notes

- **To run something once per field frame, after the battle layer**, the cheapest native seam is the
  one-shot at `0208E6A8`: store a function pointer and `00234520` calls it exactly once, then nulls
  it, provided `(02089340 & 5) == 1` and bit 1 is clear. The engine's own two writers are
  `00238A60` and `0023B020`.
- **To simulate a slot faster than real time**, set its `+0x201` byte (the script commands 1337 /
  1306 do) — the tick then runs up to sixteen sub-steps for that slot. Slot 0's sub-steps also
  re-run the whole field frame, including the UI-request latches and the group-completion
  dispatch, so a mod doing this must expect those to fire per sub-step.
- **The field frame does not run while the full menu is open** — but the tick's prologue does: queued
  manager initialization and unload (`0025BFB0`), the party-roster clear that comes with a manager-0 request,
  and the deferred mode request all run in every mode. A mod that needs a value updated per frame regardless
  of menus must hook the tick's tail or a slot 3–4 pass, not the field frame; a mod that assumes the roster
  cannot change behind a menu is wrong whenever an area request is queued.
- **A unit is simulated only with flags bit 3 set, bit 16 clear, bit 4 set**, and only once its
  record has been bound by `00265A20` (`+0x14 ≥ 0x80`, at most 32 units). Forcing a unit "active"
  is a write of bit 4; the engine's own activation arm additionally requires bit 1 clear and
  `00267240(work)`.
- **The tick-in-progress word `022C2548`** tells a hook whether it is inside the world tick; the
  widget constructor reads it for exactly that reason.

## 7. What is not known

- [x] ~~**What each of the fifteen extra sub-steps is for**, and which script situations set the
  `+0x201` byte on slot 0 rather than on a cutscene slot.~~ `EX-1` — answered 2026-09-11, section
  2.2a: the passes are uniform repeats (the step number reaches no callee), and no situation sets
  slot 0's byte — the skip-begin setter refuses manager 0, the skip-end setter only clears, the
  loader writes 0.
- [x] ~~Bits 6, 23, 26 and 29 of `02089340` are set by script verbs (§2.5) and their meanings are not
  read.~~ **FZ-1 ANSWERED 2026-09-11:** the verb table names them — treasure opening in progress,
  debug rotation-control mode, view-check mode, "real battle" mode (§2.5).
- [x] ~~Bit 13's condition is read in full (§2.5, the focus actor's movement-context `+0x138`
  attachment); what that attachment is — created outside the census, released through `003DAD00` —
  is not named.~~ **FZ-2 ANSWERED 2026-09-11:** the attachment is the actor's movement body,
  created by `002E3500` after the presentation set-up ([the movement body page](../../06-Movement-And-Navigation/the-movement-body-pool-and-the-separation-pass.md));
  what writes the word `+0x88` the bit tests is **FZ-10**.
- [x] ~~**What the eleven skip-begin notifications and the three pre-skip calls do**~~ (`003601B0`,
  `003600D0`, `00466DD0`, `003E8AA0`, `003DE0A0`, `003E9970`, `0036DE70`, `00473680`, `0024D9C0`,
  `003B08F0`, `003DEE10`; ~~`002EFE40` / `002EFE50` / `002EFA70`~~), and what `00360980` arms a skip
  request from. `EX-8`. *Narrowed 2026-09-12 (FABLE):* the three pre-skip calls are the
  **screen-fade layers** — kind 6, wait `0xFF`, and layer 4 to black in zero frames, the instant
  cut a skipped scene shows ([the screen-fade layers](../../17-Presentation-Rendering/Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md) §2.5). **EX-8 ANSWERED 2026-09-12 (FABLE), at the mechanism level — the eleven, in call
  order (`003607E1`–`0036081D`; `m` is the skip's manager argument):**
  1. `003601B0(0xF)` sets bit 15 of the word `022CB720` (the skip flag bit).
  2. `003600D0` frees all seven fade layers (`002EF840(0..6)`, [the screen-fade layers](../../17-Presentation-Rendering/Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md)), then `002F1A70`,
     `003DE210` and `003DE0A0`.
  3. `00466DD0` finishes every active timed record of the `0x50`-stride pool at `02EBB6F0`
     (flags `+0x4C` bit 0 set, bit 1 clear, float `+0x38` non-zero → `00467730(i, +0x40)`, bit 2 set).
  4. `003E8AA0(m)` walks the loaded voice bank's entry table (`[02B5D080]`: count at `+8`,
     offsets at `+0xC`) and runs `0037A500` on the entries that belong to `m`.
  5. `003DE0A0` releases the four `0x68`-stride handle records at `02B58A80` through the typed
     handle release `0024CFF0` and zeroes them.
  6. `003E9970(m)` frees every voice-pack slot of manager `m` ([the voice-pack slots](../../18-Audio/the-voice-pack-slots-and-the-voice-verbs.md)).
  7. `0036DE70(m)` cancels the manager's pending loads: over the 32 `0x18`-stride requests at
     `022D94B0` whose byte `+8` is `m` and whose word `+4` has a bit other than 2, it sets `+4 = 4`
     and calls `003B24C0(id)`, then `003B1700(id)` (= `003B18E0`, [the request queue](../../02-Resource-And-Asset-Pipeline/the-resource-request-queue.md) §2.3) when that
     returns 0.
  8. `00473680(m)` → `0026FA80`: when the byte `02F8F238` is set, posts a `{kind 2, m}` message
     through `0024E7D0`.
  9. `0024D9C0` is the presentation reset: `0209A6F8` and `022D8EDC` set to 1, `003B81A0(0)`,
     `003ACA90(2)`, four flag bits cleared, `003B5310(0)`, `003AF330(0)`, `003AFD30(1)`, `003B6930(4)`.
  10. `003B08F0` purges the 36-record `0x18`-stride pool at `02EBEC00`: every live record whose
      byte `+0x13` lacks bit 0 and whose byte `+0x10` is not `0x63` goes to `003B0770`.
  11. `003DEE10(m)` drains and frees the manager's eight `0x38`-stride streaming slots at
      ~~`02B58960 + m × 8 × 0x38`~~ `02B59360 + m × 8 × 0x38` *(corrected 2026-10-02, OPUS: `003DEE10+0x37` `lea rcx, [02B59360]`, `+0x59` `imul rbx, rax, 0x38`)*, by state (`+0x10` 1–4: drain the request queue with `0032E520(0)`
      and `0035EA30`, `003DEB30`, `002DEE90(−1)`, `003697F0` frees).
  Then `00267310(m)` decides the instant cut. What arms a skip is already above (`00360980`
  registers the request and sets its pending bit). **Residual:** the identity of the pools at
  `02EBB6F0`, `02EBEC00` and `02B58960`, and of message kind 2.

  > ### `02EBEC00`'s record is now laid out, from the functions that use it (FABLE, 2026-09-22)
  >
  > This is `BI-11`'s handle class 5/6/9 seen from the pool end. **The 24-byte record is
  > `{key, object, flags}`:**
  >
  > | offset | what | read from |
  > |---|---|---|
  > | `+0x00` | **`u32` key, and `0` means the slot is FREE** | `003AFFB0` counts slots with `[rec] == 0` at `0x18` stride, unrolled six at a time (`003AFFD0`–`003AFFF9`, `add rax, 0x90`); `003B0770` finds a record by `[rcx] == esi` |
  > | `+0x08` | **a pointer to a class-chained registry object** | `003B009C mov rcx, [rcx+8]` then `003B00A0 call 0024EE60` |
  > | `+0x13` | **a flag byte**; bits 1–2 decide survival | `003B0060`–`003B006B`: `and al, 6` / `sub al, 2` / `test al, 0xFD` skips the record when `(flags & 6) == 2` |
  >
  > **`003AFFB0` is a compacting purge, not merely a scan.** For every live record that the `+0x13`
  > test does not spare it releases the object at `+0x08` through `0024EE60` and then closes the
  > gap — `003B00A5 cmp rbx, 0x23` bounds the index at 35, the last of the 36 slots, and
  > `003B00AB lea rax, [rbx + rbx*2]` / `lea rdi, [rsi + rax*8]` is the `× 0x18` move of the tail
  > down one slot.
  >
  > **And `0024EE60` ties the pool to the registry this page's residual is really about.** It takes
  > the object's **first byte as its class** (`0024EE68 movzx eax, byte ptr [rcx]`), indexes the
  > head table at `020910F0` (`0024EE72 lea r8, [rcx + rax*8]`) and walks the `+0x348` chain to
  > unlink it (`0024EE85 mov rcx, [rcx + 0x348]`). *That is exactly the `020910F0[class]` /`+0x348`
  > structure `BI-11` already records* — so **the pool is a keyed side-table over the registry's
  > class-chained objects**, not a store of its own.
  >
  > **What this does NOT do is name the subsystem.** `BI-11` asks what the family *holds*; this
  > gives the record's shape and the pool's role, and leaves the identity where OPUS's reference
  > census left it — every reference in one contiguous `Presentation` band. **Static, bodies read.**
- [x] ~~**What UI requests `0x0B`, `0x17` and `0x18` are.**~~ **EX-2 ANSWERED 2026-09-12 (FABLE),
  at the mechanism level** — the three predicates re-read, with what each request arms:
  **`0x0B` (11) is the game-over request.** `002371B0` returns 1 only when *no* living kind-0 unit
  of type `≤ 6` — the playable characters' types — stands in party slots 0–3 or in the nine reserve
  entries (`002371CC`–`00237239`): nobody is left to swap in. Its route (`0035C7B0(11, 1)`,
  `0035C806`–`0035C81E`) sets `022C83E8` bit 8, runs `00227370` — transition request `0x16`
  through `00226BE0(0x16, 0, 0, −1, −1)` and `00226280` unless the global `01FD46D4` carries bit 22
  — and posts request 11 into the mailbox; `00254850(1)` then sets [the capability policy](../../15-Input/Gameplay-Capability-Policy/capability-inhibition-policy.md) **row 8** bits
  0, 1, 2, 4, 5, 6, 7, 9, 11 and 20. The generic route's second widget classes 11 with 16
  (`00280140`, `002803F7`–`00280403`: `+0xC8 = 2`).
  **`0x18` (24) is the party-incapacitated request.** `00237140` (`00237150`–`00237199`) skips
  guest-typed units (kind 0, type `7..0x19`) and returns 1 only when every other occupied party slot
  holds a torn-down unit — reached only after the game-over test failed, so playables still exist
  in the reserves; stage 18's `00237260` is the same walk with **KO / Stone / X-Zone**
  (`0x80000003`, [the thirty-two statuses](../../10-Status-Periodic-Terminal/the-thirty-two-statuses.md)) in place of "torn down", exempted by [field bit 15](../../03-World-Area-Field/Field-Record-Table/field-record-bit15-action-permission.md) (`00313F60`).
  The router sends 24 to `0035D080`, whose `0xC8`-byte widget (`0035D6B0`) builds **the battle-menu
  selection state** (`0035BC50`) — the reserve-swap prompt, by mechanism; `00254940(1)` sets row 8
  bit 11 and `002547D0(1)` bits 1, 2, 4, 5, 6, 7 and 9.
  **`0x17` (23) is the leader-incapacitated latch.** Stage 19 raises it while the party leader's
  status layers carry `0x80000003` without the bit-15 exemption and clears it otherwise;
  `002548F0(on)` sets or clears row 8 bits 6, 8, 9 and 11. It takes the generic route with no
  special class. **The on-screen wording of the three screens is not read** — it lives in the UI
  layout resources or a live observation, not in these bodies.
- [x] ~~**What the tail's unread callees do**, in particular `002E09A0` (1,002 B), `003E7650`
  (1,566 B, Presentation) and `00362850` (1,036 B, Audio); and the five `003DF760(0, n, …)` calls
  that open mode 0.~~ **EX-3 ANSWERED 2026-09-12 (FABLE), at the mechanism level.**
  **`002E09A0` drains the router's input mailbox.** It walks the eight `0x68`-stride records at
  `0215F200` by their state word `+8` (state 6 → `002A28B0`, else `002A2A60`; 7 = empty,
  `002E0A1D`–`002E0AB1`), then — when the last posted request `02092730` is 0 or 5, no record is
  active, the mailbox's pending byte `0215F1A0` is set, the device is present
  (`InputDevice_QueryAvailabilityState_Always1`) and, unless the pending id is one of ~~12 / 15 / 16
  / 17 / 19~~ **12 / 15 / 17 / 18 / 19** (`bt 0xE9000`), no transition is running (`0036D830` → `00226BA0`) — it posts
  `00254B50([0215F1A4], [0215F1A8], 0)` and clears the pending byte (`002E0CAD`–`002E0D10`). The
  mailbox `002E1B10` writes exactly those three cells (`002E1B35`–`002E1B47`), so this is the
  consumer [the router page](../../16-UI/Request-Router/ui-request-router.md) §2 leaves implicit:
  ~~**input-raised requests reach the router one field frame later, from here.**~~

  > **BOTH HALVES OF THAT SENTENCE CORRECTED 2026-09-21 (FABLE), against my own 2026-09-12 answer,
  > while reading the same bodies for [the input subsystem contract](../../15-Input/CONTRACT-input-subsystem.md).**
  >
  > **The exempt set is `12, 15, 17, 18, 19`.** The instruction is `mov ecx, 0xE9000` / `bt ecx, eax`
  > at `002E0CDE`, and `0xE9000 = 2^12 + 2^15 + 2^17 + 2^18 + 2^19` — **id 16 is not exempt and id 18
  > is**. Computed from the constant rather than read off the prose. (`002E0CD9 cmp eax, 0x13 / ja`
  > sends every id above 19 to the transition check first, which is why the `bt` is safe.)
  >
  > **And the latency is the guard's, not a frame's.** `002E09A0` is called at `0031427D`, in the
  > **fixed tail of `00314020`** — the same body whose battle arm calls the arbiter at `00314137`
  > (then `0031413C jmp 0x314231`, which falls through to the tail) and whose field arm calls it at
  > `003141F2`. So a request the arbiter posts at `00253D78`, `00253EE6`, `00253F44` or `00253F53`
  > **is visible to the drain in the same tick**, and the call order alone permits same-tick delivery.
  > What actually holds a request back is this paragraph's own guard — `02092730` must be `0` or `5`,
  > no slot of the eight `0x68` records may carry `+0x38` or `+0x3E` ~~bit 7~~ **bit 0**, ~~and for a non-exempt id no
  > transition may be running~~. *(Corrected 2026-09-26, FABLE, Claude Opus 5.5, on OPUS's executed replay.
  > The test is `shl al, 7` / `sar al, 7`, which keeps bit 0. The transition clause never holds a request on this
  > build, because its device term `0053DD10` returns a constant 1. A not-ready manager slot 0 discards the request
  > rather than deferring it; see [the router contract](../../16-UI/CONTRACT-ui-request-router.md) R-5.)* That is a **conditional** deferral with a testable condition, and it is
  > a different claim from a fixed one-frame latency. Nothing else in the EX-3 answer changes. **`00362850` is the audio listener update:** it resolves the party
  focus actor (`PartyFocus_GetCurrentPackedActorHandle` → `ActorHandle_ResolveRegistryEntryByPackedId`
  → `Actor_GetWorldPosition`), reads the camera matrix at `02AEDEF0` through `00202C70`, forms
  the offset and its `atan2f` heading, and writes the listener block `022CBA80`–`022CBB0C`
  (`003628B7`–`003629DF`). **`003E7650` pushes the presentation parameters:** for every record of
  the table at `02B59D80` whose word `+0` is live and whose word `+4` names a character render
  record (`× 0x740` into `[022C6F28]`, [the character render record array](../../17-Presentation-Rendering/Character-Render-Records/the-character-render-record-array.md)), it runs `00320BB0(i, &out, &rec+0x84)` and
  the 47-accessor family `0051E3A0`–`0051ECF0` plus `0046FD00` (`003E7673`–`003E7C53`). **The five
  `003DF760(0, n, 0, 0, 0)` calls** write entry `n` of four parallel eight-entry tables — pointers
  `02B59C40[n]` and `02B59C80[n]`, dwords `02B59CC0[n]` and `02B59CE0[n]` — so mode 0 clears
  the registrations of slots 1–5 (two pointers, two words each) before its sub-steps. Residual:
  the identities of the record tables `0215F200` and `02B59D80`.
- [x] ~~**What the `0x130`-stride list at `02B4E4C0` holds** that `003DAC70` walks every tick with
  the `00314F30` callback.~~ **EX-4 ANSWERED 2026-09-11:** the 128 movement bodies; the walk is
  the separation pass — each body against the bodies sharing its spatial cells, overlapping pairs
  pushed apart by weight, the push consumed by the next candidate position
  ([the movement body page](../../06-Movement-And-Navigation/the-movement-body-pool-and-the-separation-pass.md) §2.6–2.8).
- [x] ~~**What `003DB1F0`'s `+0x63` countdown and `+0xA0` state walk drive.**~~ **EX-5 ANSWERED
  2026-09-12 (FABLE):** `+0x63` (`entryListFlags`, [the actor storage record map](../../04-Actor-Entity/Actor-Storage-Record/the-actor-storage-record-field-map.md)) is a **two-pass "list changed"
  window** — `ActorResource_InsertEntryFromDescriptor` (`003DBA83`) and `ActorResource_RemoveActiveEntry`
  (`003DB3F5`) set it to `2`, and every shift-right site (this post-pass `003DB25A`, `003DB28E`,
  `003DBCC1`) halves it, so it is non-zero for the two passes after an insert or a removal. While
  it is, the walk over `[record+0xA0]` — the actor's `ActorResourceEntry` array, `+0x89` entries of
  `0x14` bytes — promotes every entry in run-state 1 (queued) to state 2 (ready to run,
  [the binding page](../../01-Script-VM-Native-Bridge/Interpreter-Core/how-a-script-binds-to-an-actor-and-how-requests-are-scheduled.md) §2.4–2.5), and `ActorResource_SelectPendingEntryForExecution` then picks the
  highest channel's ready entry. The same promotion is what `003DBAE0` does on a state-2 insert.
- [x] ~~**What the field frame's three entry gates `001800E0`, `001800C0`, `001EC560` test**, i.e.
  when frame mode 2 skips the tick.~~ **EX-6 ANSWERED 2026-09-12 (FABLE), at the mechanism level:**
  `001800E0` is *the map-art context's byte `+0x41A` is non-zero* (`001A9930` is the 8-byte
  getter `mov rax, [rip+0x1DD7831]` returning `*(01F81168)` — the `0x520`-byte map-art context
  built by `001A98B0`, per [the game application](../Application-Root/game-application.md); the
  object does carry console state, which is where the original "console singleton" gloss came
  from — corrected 2026-09-22 on FABLE's own contra: `01F68168`, the address the gloss implied,
  has zero image references; which command sets the byte is not matched); `001800C0` is
  *the ring behind `001BDAB0()` is not empty* (`001BD620`: head `+0xFC` equals tail `+0x100`,
  inverted); `001EC560` is *the current cutscene slot `01DFE40C` is 0–4, its per-slot flag at
  `01F832B0` is set, and ~~`00265680()` holds~~ `00265680()` answers zero* *(corrected 2026-10-02, OPUS: `001EC560+0x20` `call 00265680`, `+0x25` `test eax, eax`, `+0x27` `lea eax, [rbx+1]`, `+0x2A` `je` — 1 only when it returned 0)* — the same marker and flag array [the cutscene name-slot page](../../99-Unresolved-Residual/Cutscene-Asset-Slots/cutscene-name-slots-and-the-depth-of-field-sidecar.md) §2
  decodes. `00265680` requires manager slot 0 live with `+0x10` bit 7 / `+0x11` bit 0 clear, every
  live slot's `+0x17` bits 0–1 set (`002656C0`–`002656DF`, [the actor-manager record map](../../04-Actor-Entity/Actor-Manager-Record/the-actor-manager-record-field-map.md)), no entry of the eight
  `0x68`-byte records at `0215F200` flagged at `+0x38` / `+0x3E` ~~bit 7~~ **bit 0** (`002E0540`'s `shl 7` / `sar 7`
  keeps bit 0; corrected 2026-09-26), and then
  `00265720()`. So the field frame skips the tick while the console holds that byte, or while a
  queued ring is non-empty during a cutscene whose slot holds a releasable entry.
- [x] ~~**The meaning of unit flag bits ~~1, 3,~~ 16 ~~and 24~~** beyond their effect here.~~ **Narrowed
  2026-09-12 from [the battle-unit field map](../../04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md)'s flag table:** bit 1 is set only by `BattleUnit_TeardownAndDespawn`
  (`00300F2A`) — *torn down*, which is why it makes the frame a no-op; bit 3 is set by
  `BattleUnit_ActivateAppliedDefinitionRuntime` (`00233B4B`) and cleared by `BattleUnit_ResetStateForReuse`
  — *definition runtime activated*; bit 24 is set by `BattleUnit_RecoverFromTerminalStatusSetIfClear`
  (`003012A1`) and `00313500`, cleared by `BattleUnit_HandleReactionAnimationEvent` (`0032517C`) and
  `003083A0` — *a reaction animation is pending*. **Bit 16 answered 2026-09-12 (FABLE):** a whole-`.text` scan for `0x10000` writers finds its one
  clearer-and-setter, **`BattleUnit_UpdateEngagementStateFlag` (`00307D10`, `00307DD8`–`00307DE2`)**,
  called by `BattleStats_RebuildEffectiveStatsAndAffinityState`, `00308130` and
  `BattleStats_ChangeStatusAndProcessSideEffects`: the bit is recomputed as 1 for a party unit of
  type `0x1A` (the chocobo), for a unit whose status layers carry bits 5 or 27, for a unit with
  flag bit 9 unless `0030B050` clears its bit 10, or with bit 10 set, and for one where `00307CE0`
  passes but `0030BF20` on its action context fails; 0 when the null predicate `00253B90` holds
  (which also zeroes `+0xDCC`, the qword `022C1F40` and bits 1–2 of the byte `022C1F48`) or otherwise. **Bit 16 had no OR / AND site in the unit census**
  (only the high dword's bit 48 uses `0x10000`) because its writer masks with `0xFFFEFFFF` and ORs a
  shifted register (`00307DD8` `and [rdi+4], 0xFFFEFFFF`, `00307DDF` `shl ebx, 0x10`, `00307DE2`
  `or [rdi+4], ebx`) — re-verified 2026-09-12; all four bits are now placed. `EX-7` closes.
- [x] **EX-9.** **Which writers set the manager request mask `02099ABC`, and whether ordinary initialize / unload callbacks
  change it during `0025BFB0`'s pass.** One producer is read (`0026A5F0`); ASTRA's isolated execution shows how the
  wrapper treats mid-pass changes, not that the game makes them; the native effects of `0026CE60` and `002628B0`
  on a live area change are not observed. `EX-9`. *Narrowed 2026-09-13 (FABLE):* **writers, enumerated** (every RIP reference to `02099ABC`): the drain `0025BFB0` (clears bits), the area initialiser `00266D10` (stores 0 at `0026713B`, after `BattleSystem_InitializeAreaState`), and the one producer `0026A5F0`, which ORs `1 << m` (manager 0 first requests 1, 2, 3) and then resets the router latch (`002E15D0` clears `0215F1A0`–`0215F1A8`, `002E1690` sets `0215F1A1`). **Its callers:** `WorldTransition_StageFieldTransition` (1, 2, 3 at `00314648`–`0031465C`); the requeue `00314530` (1, 2, 3, 0); `WorldTransition_RequestFieldTransition` (0, `003144A1`); `00314410` (manager 4, only while no deferred mode request is pending, which it then records in `01EED060`); the field runtime pass (`0025DA3A`) for a slot whose deferred-unload byte `022C6D20[m]` is set, when no save is being written and the slot is live or `+0x13` is set and `+0x11` bit 3 is clear; `00332190(m)`, which sets `022C6D20[m] = 1` for a slot that is live, has `+0x13` set or has `+0x11` bit 3, and requests at once only when the slot is live; and the script side — `eventdispose_f2` (`0x00F2`, `00356D40`, managers `clamp(n + 1, 1, 3)`: 185 × `(0)`, 76 × `(1)` in 212 `us` scripts), `debug_eventload`'s poll (`0050D0C0`) and `debug_eventdispose` (`0050D240`), the last two with no `us` script use. **Mid-pass changes:** in the direct and tail call graph, neither `ActorSystem_InitializeManagerRuntime` nor the unload `002628B0` reaches the producer except through `00306570` (from `BattleSystem_InitializeAreaState` and `002341C0`), and that route cannot fire — it calls `00332190(3)` only when slot 3 is not live (`002671F0`), and `00332190` requests only when it is, with nothing in between (`00238A60`) touching the slot. Indirect calls — the manager's `+0x108` callback (`00262F1E`) and scripts run inside initialisation, which can call `eventdispose_f2` — are outside the call graph and stay open.
  ***ANSWERED 2026-09-18 (FABLE): no ordinary initialise or unload callback changes the mask during the pass, and the two indirect routes the narrowing left open are closed.** *Reachability, unbounded.* Walking every direct and tail call from the drain `0025BFB0` reaches 3,108 functions; of the producer `0026A5F0`'s eight callers (`0025D9E0`, `00314410`, `00314440`, `00314530`, `003145E0`, `00332190`, `0050D0C0`, `0050D240`) only `00332190` is among them, by the single route `0026CE60` → `BattleSystem_InitializeAreaState` `002342F0` (`00234397`, argument 0) → `00306570` → `00332190(3)`, which is the gated-impossible route above: `00306570` goes on only while slot 3's live bit `+0x10` bit 0 (`002671F0`, `02098E20 + 3 × 0x288`) is clear and `00332190` requests only while it is set. *The `+0x108` hook is never installed.* Every qword store into a `+0x108` field in `.text` was listed (128); the three on a manager slot are the unload's own read-call-clear (`00262F0F`..`00262F20`, storing `rbp` zeroed at `0026292A`), the reset `00265FF0` (`00266352`, storing `r15` zeroed at `00266005`) and the bind `ActorManager_BindLoadedDefinition` `0026C8C0` (`0026CC65`, storing `rbx` zeroed at `0026C905`, in the same block that zeroes `+0xA0`..`+0xB8`); the slot array `02098E10` is zero-initialised `.data`, so the hook `002628B0` calls at `00262F1E` is null in every shipped path. *Scripts do not run inside the pass.* Neither `0026CE60` (2,577 reachable functions) nor `002628B0` (2,013) reaches the command dispatcher `002621D0` or `eventdispose_f2` `00356D40`, and every one of the 261 `eventdispose_f2` calls in the `us` scripts sits in a script-thread function (`main` 257, `map_dwbtl_start_id_check` 2, `start_battle` 1, `CUT_FINISH` 1) that only the VM step runs. What remains unobserved (the native effects of the two callbacks on a live area change) is a description of the callbacks, not a route to the mask. Static sweep over the direct call graph and the image; virtual dispatch other than the `+0x108` hook is not represented in that graph, and the manager callbacks are the two direct calls the drain makes.*

## 8. Evidence

| claim | evidence | tier | confidence |
|---|---|---|---|
| Three callers, and the mode argument each passes | `0022ABD6`–`0022ABD8`, `0022BA1C`–`0022BA23`, `0022BCC8`–`0022BCCF`; `check_caller_claims --addr 0x00314020` = 3 | 1 | PROVEN |
| Five slots, sixteen sub-steps in mode 0, slots 3–4 in mode 1 | the `cmp ebx, 5` / `cmp esi, 0x10` bounds and `lea ebp, [r13+3]` cited in section 2.2 | 1 | PROVEN |
| The sub-step opt-in is the slot `+0x201` byte | `003141C9 call 0x267310` guarded by `test esi, esi`; `00267321` | 1 | PROVEN |
| The field frame is slot-0-only | `002345B1`–`002345B3`; likewise `0023452F`–`00234531` | 1 | PROVEN |
| The 23 steps and their order | one pass over `002345B9`–`00234861`, every step cited | 1 | PROVEN |
| Bit 2 = clock did not advance; `0032A100` advances `0208D45C` on a changed timer | `002345C3`–`002345E9`; `0032A12A`–`0032A13B` | 1 | PROVEN |
| The reset loop's parity and the bit-3 flip | `00234639`–`00234645`, `002346CB`–`002346DA` | 1 | PROVEN |
| The request predicates' filters | `002371CC`–`00237239`, `00237175`–`0023717F`, `0023728D`–`002372BB` | 1 | PROVEN |
| `0035C8E0` ignores `0x18` | `0035C8E0`–`0035C8F8`: only `id - 0x0B == 0x0C` acts | 1 | PROVEN |
| The unit frame's address is taken once and stored at record `+0x38` | boundary-free `.text` sweep for `E8`/`E9`/both `LEA` encodings, control positive: one hit, `00265A4F`; `00265AA8` | 1 | PROVEN |
| The callback is called at `0025E222` under four record-bit gates | `0025E1E2`–`0025E222` | 1 | PROVEN |
| The unit frame's gates and three paths | `00233F80`–`0023412D`, every branch cited | 1 | PROVEN |
| The one-shot at `0208E6A8` | `0023455A`–`00234568`; writers `00238A60`, `0023B020` from the global index | 1 | PROVEN |
| `+0x63` is set to 2 by insert / remove and halved by every post-pass; the walk promotes state 1 to 2 | the storage census rows for `0x63` (two `\|= 2`, three `shr 1`, three reads); `003DB222`–`003DB25A` | 1 | PROVEN |
| The three entry gates | `001800E0`, `001800C0`, `001BD620`, `001EC560`, `00265680`, `002E0540` read whole; globals resolved from the instructions (`01DFE40C`, `01F832B0`, `02098E20`, `0215F200`) | 1 | PROVEN (mechanism) |
| Bits 1 / 3 / 24 setters and clearers; bit 16 has none | the battle-unit flag table (census) | 1 | PROVEN / narrowed |
| What the unread callees do | **not established** *(answered: see EX-3, ANSWERED 2026-09-12 (FABLE); 2026-10-02, OPUS)* | — | UNKNOWN |

## 9. Related

- [The time-stop registry](../System-Stop-Registry/the-time-stop-and-system-stop-registry.md) — the 28 stop requests (menus, event scripts, time-stop magick, masks, skips) and the seven per-actor stop sets that decide which actors this frame actually advances

- [`../Per-Frame-Update-Gate/one-word-decides-which-fifteen-subsystems-tick.md`](../Per-Frame-Update-Gate/one-word-decides-which-fifteen-subsystems-tick.md)
  — the enable word above the frame dispatcher.
- [`../../22-Middleware-PhyreEngine/The-Frame/what-happens-between-two-frames.md`](../../22-Middleware-PhyreEngine/The-Frame/what-happens-between-two-frames.md)
  — the seven frame modes; this page is what three of them do to the world.
- [`../../04-Actor-Entity/the-field-runtime-pass.md`](../../04-Actor-Entity/the-field-runtime-pass.md)
  — the actor drive loop between the tick and the per-unit frame.
- [`../../05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md`](../../05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md)
  — range retirement, the active path's last step.
- [`../../05-Spawn-Encounter-Lifecycle/Group-Completion-And-Respawn/when-a-group-is-wiped-and-when-it-comes-back.md`](../../05-Spawn-Encounter-Lifecycle/Group-Completion-And-Respawn/when-a-group-is-wiped-and-when-it-comes-back.md)
  — step 17 and the idle path's bit-1 write.
- [`../Battle-Runtime-Mode/battle-runtime-mode-ladder.md`](../Battle-Runtime-Mode/battle-runtime-mode-ladder.md)
  — `02092730`, `022C83E8` and `022C2160`, the words behind the request gates.
- [`../../10-Status-Periodic-Terminal/Periodic-Tick/what-the-periodic-tick-does.md`](../../10-Status-Periodic-Terminal/Periodic-Tick/what-the-periodic-tick-does.md)
  — `00300140`, the per-unit reset step 6 calls.
- [`../../99-Unresolved-Residual/Cutscene-Asset-Slots/cutscene-name-slots-and-the-depth-of-field-sidecar.md`](../../99-Unresolved-Residual/Cutscene-Asset-Slots/cutscene-name-slots-and-the-depth-of-field-sidecar.md)
  — the slot record's field map and the `+0x201` byte's writers.

## Falsification pass 1 — 2026-09-12 (OPUS)

**passes: 1 · last_pass: 2026-09-12**

| claim | measured |
|---|---|
| **the 23 steps and their order**, over `002345B9`–`00234861` | **23** numbered rows, `1`…`23`, the first at **`002345B9`** and the last at **`00234861`** — the cited range's exact endpoints |
| five slots, sixteen sub-steps, slots 3–4 in mode 1 | `00314132 cmp ebx, 5` (and five more), `0031421F cmp esi, 0x10`, `003140FF lea ebp, [r13 + 3]` |
| `0035C8E0` ignores `0x18` | `sub ecx, 0xb` / `je` / `cmp ecx, 0xc` / `jne` — **only `id − 0x0B == 0x0C` acts**, so `0x18` falls through to `ret` |
| the callback at `0025E222` under **four** record-bit gates | `+0x9` bit 6 ∨ `+0x13` bit 1 (composite), `+0x14` bit 4, the `+0x18` byte compare, `+0x9` bit 5 — **four**, with `test rax, rax` on `+0x38` being the callback-pointer null check rather than a fifth gate |

### The "23 steps" is a step count, not a call count

The cited range contains **39 calls to 35 distinct targets**. Counting calls and concluding the 23
is wrong would be the sixth such mistake in this sweep: a *step* in §2.3 is a numbered row that may
issue several calls. **Counted as steps, it is exactly 23 and it spans exactly the cited range** —
both endpoints land on a numbered row.

This is the sixth count in this sweep that reproduced only once its unit was identified, and it is
now [a standing rule](../../_index/EVIDENCE-STANDARD.md) rather than six separate observations.

**Not claimed:** nothing here was executed or observed live; §7's open items are untouched.

## Interior citations — entry-only-large pass (2026-09-14, SWE2-FRONTIER)

This page named `PartyFollow_SolveFormation` only at its entry. The interior addresses below were
read in the shipping image.

| body | interior cite | what is there |
|---|---|---|
| `00338490` | `00338590` | `mov byte ptr [rip+…], 1` — sets `022C7E00`, first of four slot flags at 0x60 stride (`022C7E60`/`022C7EC0`/`022C7F20`) cleared/set per formation slot, after `Navigation_HasDataset` gates the solve |
| `00338490` | `003385C2` | `call BattleUnit_FindMappedDefinitionSelectorByIndex` — resolves each follower's slot inside the `BattleUnit_GetPartyLeader`-anchored walk |

*(Second interior pass, 2026-09-16, SWE2-FRONTIER.)* The evaluator pair the §3 row
already lists by callee — `003D83A0` (2,190 B) and its row-builder `00430B90` (1,199 B) —
were opened end to end in the shipping image. `003D83A0` is the frame's **mode-driven
transform evaluator**: it walks a linked list of parameter records rooted at
`[02B4D7A8]`, resolves each node through the `0020E600` service (`+0x40` current,
`+0x0C` next — the `003D8B50` back-edge is the list walk), and composes scaled vector
rows into the shared transform workbench's row array (`022D91B0`–`022D939F`, see
[the shared transform workbench](../Shared-Transform-Workbench/the-shared-transform-workbench.md)).

| body | interior cite | what is there |
|---|---|---|
| `003D83A0` | `003D83B2`–`003D83F5` | prologue: squared 3-D distance of `rdx[0..2]`−`rdx[4..7]` → `00861F14` (the CRT import thunk §3 calls `sqrtf`) → `÷ 10.0f` — the evaluator's distance term |
| `003D83A0` | `003D859C`/`003D865A` | mode-1 arm of both scalar switches: `angle = record[+0x20 or +0x24]`, `index = cvttss2si(angle ÷ 6.2831855f × 32768.0f) & 0x7FFF`, `scalar = float[01F004E0][index]` — **`01F004E0` is a 32,768-entry sine table** (verified: `table[i] == sin(2πi/32768)` for i=0..7, `=1.0` at 8,192, `≈0` at 16,384) |
| `003D83A0` | `003D84FF`–`003D85D7` | first scalar switch on `descriptor[+0xA0] & 0xF`: mode 2 = `record[+0x48]−1.0`, mode 3 = ±1.0 by `record[+0x20]` vs π, mode 4 = ±1.0 or half-scale by `descriptor[+0xA1] & 3`; second switch on `+0xA0 >> 4` picks the other scalar the same way |
| `003D83A0` | `003D8699`/`003D86AE` | `call 00430B90` ×2 — builds two three-float rows, from `descriptor+0x00` and `descriptor+0x40`, keyed by the `cvttss2si(record[0])` quantized value in `r14` |
| `003D83A0` | `003D86DE`/`003D88AE` | writes into the workbench rows: `022D9250` (a whole row) then `022D9240`–`022D925C` per-element scaled by the two mode scalars; temporaries at `022D91B0`–`022D91F0`, plus `022D9198` (Q) and `022D92E0` |
| `003D83A0` | `003D8B3C`/`003D8B50` | the list walk's tail: `0020E600(record[+0x0C])` resolves the next node; `jne 0x3D84C6` loops until the resolver returns null |
| `003D83A0` | `003D8BC3`–`003D8C1C` | exit: scales all eight output floats by `[02B4D7B8]` — a global scale applied uniformly to the composed result |
| `00430B90` | `00430BA5`–`00430BDA` | the row evaluator's outer dispatch on `byte[descriptor+0x30] >> 2 & 3`: mode 0 writes a zero row, mode 1 writes `1.0f ×3` — the two constant-row modes |
| `00430B90` | `00430BF6`–`00430C1A` | sub-mode `descriptor[+0x30] & 3 == 0`: three `call 004309C0` — one scalar channel evaluation per element, reading `descriptor+0x00`/`+0x10`/`+0x20` |
| `00430B90` | `00430C41`/`00430C62` | sub-mode `& 3 == 3` with `descriptor[+0x31]`/`+0x32` both zero: `00430540` evaluated twice (r8d = 0 then 1) and combined through `004307C0` — a two-operand channel fold |

`004309C0`, the per-channel scalar evaluator both rows bottom out in, itself dispatches
on `byte[channel+0x0C]`: `0` returns `0.0f`, `1` resolves `*[rcx]` through `0020E600`
and reads `[rax+4]`, otherwise it delegates to `00430540`. `003D83A0`'s only caller is `0037D970`
— the sibling evaluator in the same §3 row — so the pair is one Presentation-owned
evaluation family, entered once per frame step.

*(Third interior pass, 2026-09-16, SWE2-FRONTIER.)* `003D9150` (356 B, same §3 row,
sole caller `00258B90`) is the frame's **per-channel camera view-state commit**. It
takes a context whose `+0x330` dword is the channel index, early-outs on the
per-channel enable dword `context[+0x334 + idx*4]`, then on two shared gates
(`001EDDA0` — the 27 B `[01DFE0C0] != 0 || [01F82E38] == 0` predicate — and
`001EDAD0` consulted with the sub-object's `+0x3AC`/`+0x3AE`/`+0x3A2` fields and
`context[+0x40]`), then on the master byte `context[+0x00]`.

| body | interior cite | what is there |
|---|---|---|
| `003D9150` | `003D91D2`–`003D921F` | double-buffered row select: `rsi = context[+0x20]`; `byte[rsi+0x240]` picks which of `context+0x230`/`context+0x240` is dst vs src, then both are offset by `channel×0x20`; `byte[rsi+0x241] & 1` picks the writer — `003CC970` when set, `003CC080` otherwise — called with staging block `02096ED0` and per-channel float `context[+0x320 + idx*4]` |
| `003D9150` | `003D9224`–`003D9267` | the half-angle term: `context[+0x328 + idx*4]` → `02096ED8`, `× 0.5f` → `00861F1A` (**`tanf`** per external-import-stubs-map) → reciprocal guarded: `02096EE0 = 0.0f` when `tanf` returns 0, else `1.0f / tanf(x·0.5)` — i.e. `cot(x/2)`, the standard projection-scale term |
| `003D9150` | `003D926F`–`003D929F` | commit trio on record index `((byte[rsi+0x241] & 4) \| 8) >> 1` → **6 when bit 2 set, else 4**: `CameraSystem_SetCameraActive` (`0025A520`, arg2=1), `CameraRecord_SetMode` (`0025A500`, mode 3), `CameraRecord_CopyViewState` (`0025A2C0`, source=`02096ED0`) — the staged block, incl. the cot half-angle at `+0x10`, becomes the record's view state |

So `00258B90` (the `02092628`–`02092632` byte-block evaluator) drives this commit per
channel: compute the view state into `02096ED0`, activate camera record 4 or 6 in mode
3, copy the staged state in.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Developer — CLIENT, not read.** A cited function is also called by a 1,046-byte Developer-labelled body.
- **Gameplay — SERVICE and CLIENT, 56 edges.** The Gameplay-labelled neighbours are battle runtime bodies:
  - the engagement test `BattleUnit_UpdateEngagementStateFlag` and its evidence helpers;
  - the approach search `BattleAction_FindApproachGeometryAroundTarget`, which calls two cited geometry helpers;
  - `BattleRuntime_GetMode0To5FromFlagsAndFieldBit15`, called by cited battle bodies;
  - `BattleRuntime_GetModeDependentDistanceThreshold`.

## Interior citations for the entry-cited functions (OPUS, 2026-10-01)

*Every function below is cited on this page by its entry only. Each row was read from the certified image (`73461D08...`, image base `00120000`) and states what the body does - access and representation, not meaning - anchored on instructions strictly inside the body. The applier re-decodes every anchor and refuses on any mismatch ([record](../../_index/candidates/opus-worldtick-interior-1001/README.md)). Where a row differs from an earlier line of this page, the row is what the bytes show; the record lists those cases.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `0017DFC0` | 67 B | reads qword `+0xDF8` of `00796E20()`'s result, asks `00197710(00198790(), 0, 2, 3)` and returns 1 when `0079E6A0(that object, the answer, 0)` is non-zero | `0017DFCB` mov, `0017DFE2` call, `0017DFF8` setne |
| `001800C0` | 31 B | returns 1 when the ring predicate `001BD620(001BDAB0())` is false | `001800CC` call, `001800D5` sete |
| `00184740` | 103 B | fills three zeroed locals through `0024DE30`; when they read 1 and `0x17A` and dword `01F7F540` is 0 it sets `01F7F540` and `01F7F500` to 1, and when they do not match it clears `01F7F500` | `0018476F` cmp, `00184781` mov, `0018479B` mov |
| `00197800` | 100 B | returns the dword at index `edx` (0 to `0x6A`, else -1) of table `01DF1030` when `001D50D0()` returns an object whose byte `+0xC3D` is set, else of table `01DF0E80` | `00197818` cmp, `00197831` mov, `0019784E` mov, `0019785B` or |
| `001BD620` | 16 B | returns whether the object's dword `+0xFC` equals its dword `+0x100` | `001BD626` cmp, `001BD62C` sete |
| `001EB990` | 24 B | returns 1 when byte `+0x26E` or byte `+0x26D` of the object is non-zero, else 0 | `001EB999` cmp, `001EB9A5` mov |
| `001EC690` | 7 B | increments dword `01F832C4` (the `inc` at the entry; it is a counter write, not a read) and returns | `001EC696` ret |
| `00226BA0` | 24 B | returns 1 unless qword `01FD46B8` AND qword `01FD46A0` is all ones | `00226BA9` and, `00226BB4` setne |
| `002335D0` | 112 B | returns 0, 1 or -1 from the result bytes of `0036FFD0()` and `0036FF70()`: 0 when the first is negative, 1 when it has bit `0x20`, 0 when it has bit `0x40` and the second is non-negative without bit `0x20`, 1 when it has bit `0x10` and the second is non-negative without bit `0x20`, else -1 | `002335E0` js, `002335EB` lea, `0023360F` xor, `00233635` cmove |
| `00233700` | 122 B | combines `00229E20()` and `002DDDA0()`: one set of arms calls `00229ED0(0)` and clears dword `0208E6B4`; the others call `00229ED0(1 or 2)`, set `0208E6B4` to 1 and tail-call `00182FB0` with the same 1 or 2 | `0023373C` call, `00233741` mov, `00233760` mov, `0023376F` jmp |
| `002370A0` | 26 B | calls `00229ED0(0)` and clears dword `0208E6B4` | `002370A6` call, `002370AB` mov |
| `0023B020` | 21 B | sets bit 0 of dword `02089340`, stores its pointer argument at qword `0208E6A8` and its dword argument at `0208E6A4` | `0023B027` mov, `0023B02E` mov |
| `0024DE30` | 57 B | when qword `02F97348` is non-null, writes its byte `+0x3AC`, word `+0x3AE` and word `+0x3A2` plus one to its three out-pointers | `0024DE43` mov, `0024DE53` mov, `0024DE63` inc |
| `00250180` | 22 B | stores 0 in dword `020927DC` when its argument is non-zero, else increments it | `00250188` inc, `0025018C` cmovne, `0025018F` mov |
| `002506D0` | 82 B | when dword `02064AA0` is 0 adds `00184950()` to dword `0208F570`; then runs `002481A0`, `00248030(*0208EA48)`, `00248190`, `002481C0`, `00244970(*0208EA48)`, `00250CA0` and tail-calls `003676B0(1)` | `002506E2` add, `002506F4` call, `0025071D` jmp |
| `00254440` | 51 B | when the second argument is negative writes `0x80` (first argument non-zero) or 0 to dword `01E0C320`, else sets bit `0x40` there; stores the two arguments at `02092744` / `020927EC` and tail-calls `00255330` | `00254452` mov, `0025445B` or, `00254462` mov, `0025446E` jmp |
| `00254E50` | 27 B | tail-calls `0027EFA0` when `002805D0()` returns non-zero | `00254E54` call, `00254E61` jmp |
| `00255810` | 64 B | writes -1 to four dwords (`-0x2E0`, `0`, `+0x2E0`, `+0x5C0`) of every `0xBB0`-byte step from `02092C94` up to `02096704` | `00255820` mov, `00255844` add |
| `002578F0` | 259 B | stores its argument at qword `02096508`; when that is null it walks lists 0 to 4 (`00263C30` count, `003587C0` entry), calls `0026A3B0(entry, 00358320(), low byte of 00263EB0(...))` for each entry `002EA6A0` accepts other than `*02096508`, and sets dword `02096510` to 1 when `00263EB0`'s word is negative | `002578F7` mov, `00257936` call, `0025798F` call, `002579A8` mov |
| `00259FB0` | 34 B | calls `00259620(float 02098DFC)` and tail-calls `0025A0C0(float 02098E00)` | `00259FBC` call, `00259FCD` jmp |
| `0025A620` | 90 B | for record `ecx` of the `0x860`-byte array at `02097D20`, sets float `+0x850` to float `01CEBBA8` when it is at least float `009156E0`, else moves it toward `01CEBBA8` by the factor float `008F3108` | `0025A63A` comiss, `0025A64B` movss, `0025A664` mulss, `0025A670` movss |
| `0025D580` | 76 B | calls `00238B00(0)`; if byte `02099DA7` is set calls `00250960(0, 0)` and clears it; then `002E1CD0(1, 0)`, `003601C0(0xC)`, `00225CD0(0x13, -1)` and tail-calls `00226280` | `0025D58B` cmp, `0025D59D` mov, `0025D5BE` call, `0025D5C7` jmp |
| `0025D950` | 109 B | sets byte `02099DA3` to 1, keeps it only when qword `*00226B10(0)` has bit 34 set, zeroes it when `002E15F0()` is non-zero, replaces it with byte `02099DA5` when byte `02099DA4` is set, stores the result and tail-calls `002E8700` with it | `0025D973` test, `0025D980` mov, `0025D9A7` cmovne, `0025D9B8` jmp |
| `00263B50` | 41 B | returns word `+0x1D8 + 2*edx` of actor-manager slot `ecx` (`0x288`-byte stride from `02098E10`) when the slot's `+0x10` bit 0 is set, else 0 | `00263B64` test, `00263B6D` movzx |
| `00263C50` | 41 B | returns word `+0x1D0 + 2*edx` of actor-manager slot `ecx` (`0x288`-byte stride from `02098E10`) when the slot's `+0x10` bit 0 is set, else 0 | `00263C64` test, `00263C6D` movzx |
| `00264610` | 33 B | returns qword `+0x48` of actor-manager slot `ecx` (`0x288`-byte stride from `02098E10`) when the slot's `+0x10` bit 0 is set, else 0 | `00264621` test, `00264628` mov |
| `002677B0` | 40 B | returns 1 when `003148D0()` has bit 3 set and bit 4 clear, else 0 | `002677BD` test, `002677C6` test, `002677CD` cmove |
| `00268650` | 63 B | clears dword `0209A2C0`; when dwords `0209A2B4` and `0209A2B8` are both non-negative and `003587C0` of them returns an entry, stores `003589B0(entry)` in `0209A2C0` | `0026865A` mov, `00268672` call, `00268684` mov |
| `0026B730` | 25 B | when bit 0 of byte `02098E20` is set and qword `02098E58` is non-null, stores its word argument through that pointer | `0026B739` mov, `0026B745` mov |
| `0026E260` | 37 B | when qword `0209A670` is non-null, its dword `+0x120` non-zero and its `+0x138` pointer non-null, tail-jumps through that pointer | `0026E26C` cmp, `0026E275` mov, `0026E281` jmp |
| `0027EFA0` | 143 B | when `002EFD20(3)` is non-zero calls `002EFA70(3, 0, 1, 0)`; then `0035C7B0(0xB, 0)` and `00252B40(0xB, 1)`, sets dword `+0xC8` of the `+0xC0` object of `*0209AC30` to 2, calls `00245020` on its `+0xB8`, clears byte `+0xDEE`, calls `00251E80`, sets byte `+0xDEF` and tail-calls `003EF750` | `0027EFBE` call, `0027EFC8` call, `0027EFE8` mov, `0027F00C` mov, `0027F01F` mov |
| `002805D0` | 127 B | returns 0 unless `0035C740()` is non-zero, the `*0209AC30` block has non-null `+0xC0` and `+0xB8`, that `+0xB8` object's dword `+0xD4` is 0 and dword `02092730` minus 2 is at most `0x11`; then dispatches through the byte table `0028065C` and the offset table `00280650`, whose read arm returns 1 unless the object's dword `+0xC4` is `0x40` to `0x42` | `002805D4` call, `002805FA` cmp, `00280623` mov, `0028062E` jmp, `00280639` cmp |
| `002C63D0` | 121 B | calls `00861EC0(object, 0, 0x1D90)`, appends the `0x5F` records of `0x40` bytes from `+0x40` to the end of the `+0x18` chain (each record's `+0x20` set to its predecessor), then sets `+0x1D60` to the object, word `+0x1D78` to 0 and floats `+0x1D7C` / `+0x1D80` to 5.0 / 17.0 | `002C63E1` call, `002C640D` mov, `002C6411` mov, `002C642F` mov, `002C6439` mov |
| `002E0670` | 59 B | zeroes the eight qwords `0215F1C0` to `0215F1F8` | `002E0679` mov, `002E06A3` mov |
| `002E0940` | 90 B | when word `0215F1AC` differs from word `0215F1B0`, stores (`0215F1AC` non-zero) at byte `0215F1A2`, calls `00254440(that flag, word 0215F1B4 non-zero)` and clears `0215F1B4`; then copies `0215F1AC` into `0215F1B0` | `002E094B` cmp, `002E096D` mov, `002E0976` call, `002E0982` mov, `002E098E` mov |
| `002E4330` | 74 B | returns 0 for a null argument or a first dword of -1; otherwise, when its word id is not -1 and that `0x740`-byte record of the array at `*022C6F28` has a non-zero dword `+0x284`, calls `00427280` on the record; then returns 1 | `002E4339` cmp, `002E434B` imul, `002E435B` cmp, `002E4364` call, `002E4369` mov |
| `002E7E50` | 59 B | returns 0.0 for a null object, a null `+0xC0` or an id of -1 there; otherwise tail-calls `003E6150(id, 0x9000606)` when the second argument is at most 0, else `003E6150(id, 0x9000000)` | `002E7E61` mov, `002E7E73` mov, `002E7E7D` mov, `002E7E87` xorps |
| `002E8CC0` | 32 B | sets bit 0 of dword `+0x48818` of `*022C6F28` when byte `0215FD56` is 0, else clears it | `002E8CD0` or, `002E8CD8` and |
| `002F18A0` | 33 B | calls `002E1CA0(0xA, 1)` and clears qword `022BE7D0` | `002F18AC` call, `002F18B1` mov |
| `002FC350` | 103 B | unlinks the record from the `+0x28` / `+0x30` list headed by `02EC3D60` / `02EC3D68`, pushes it at the front of the list headed at `02EC3D70`, masks its first dword with `0xF000003F` and clears its `+0x10` | `002FC35D` mov, `002FC37D` mov, `002FC391` mov, `002FC3A5` and, `002FC3AF` mov |
| `002FC830` | 41 B | when the handle's low 6 bits are below `0x30` and the `0x38`-byte record at `02EC32E0 + 0x38*low` holds that handle in its first dword, clears bits 2-3 and sets bits 0-1 of the record's byte `+0x23` | `002FC835` cmp, `002FC84C` cmp, `002FC850` and, `002FC854` or |
| `002FCAC0` | 115 B | returns 0 when qword `02EC3D70` is null; otherwise adds the low 5 bits of word `+4` of entry `02EC19C0[word +0x20]` over the `02EC3D60` list's records whose state nibble (`+0x23` low 4 bits) is 1 to 3 or 5, adds the argument's own entry, and returns whether the total is at most `0x18` | `002FCAF0` movzx, `002FCB07` movzx, `002FCB1C` movzx, `002FCB28` cmp, `002FCB2B` setle |
| `003045A0` | 72 B | returns the float `003204E0(0031ABF0(3), 1, &out)` writes, multiplied by float `01CEBC08` when bit 1 of dword `+0x5AE0` of `*02EBF190` is set | `003045B2` mov, `003045CA` call, `003045D5` test, `003045DA` mulss |
| `003143D0` | 59 B | calls `003DAA20`, `003DA2F0(0.0)`, `003DD210(0.0)`, `00255810` and `0037D890`, then `0025E3F0(i)` for i = 0 to 4 | `003143DE` call, `003143EB` call, `003143F9` call, `00314400` cmp |
| `00314410` | 39 B | when dword `01EED060` is negative, calls `0026A5F0(4)` and stores its argument in `01EED060` | `00314426` call, `0031442B` mov |
| `00314940` | 17 B | copies float `01CEBBA8` into float `022C2544` | `00314948` movss |
| `0031A230` | 36 B | returns 2 for an argument of -1, else 1 when `002FCAC0(argument)` is non-zero and 0 otherwise | `0031A239` lea, `0031A241` call, `0031A24A` setne |
| `00325060` | 18 B | advances dword `022C2578` by one, modulo 8 | `00325066` inc, `00325068` and, `0032506B` mov |
| `00325B40` | 104 B | returns 0 unless the unit is non-null, has byte `+0` bit 4 and a non-null `+0x698` record, and (when that record's dwords `+0x64` or `+0x3C` carry any of bits `0x80000003`) `00313F60()` is non-zero; then tail-calls `003DCCF0(unit +0x10, second argument, 00325AD0(unit))` | `00325B54` test, `00325B6B` test, `00325B7E` call, `00325B96` jmp |
| `00328360` | 13 B | returns -1 for an argument of -1, else tail-calls `0042FCE0` | `00328365` or, `00328368` jmp |
| `0032A650` | 64 B | zeroes the `0x100` bytes at `022C26A0`, raises dword `022C2568` to dword `022C2564` when smaller, and clears `022C2564` | `0032A663` call, `0032A674` cmovl, `0032A67B` mov, `0032A681` mov |
| `0032A6B0` | 14 B | returns dword `+0x22C` of the object at `*0209A670` | `0032A6B7` mov |
| `0032A6C0` | 25 B | returns dword `3*ecx` of the dword array that `+0x1D8` of `*0209A670` points to | `0032A6CE` mov, `0032A6D5` mov |
| `003334B0` | 107 B | for a non-null table of 16 pointers, releases every entry whose word `+8` differs from the argument (`0046EE70`, then `003697F0`) and nulls it, then calls `003A8660(argument)` | `003334DD` movzx, `003334E5` call, `003334ED` call, `003334F2` mov, `00333501` call |
| `00333740` | 112 B | for a non-null table of 16 pointers, releases the first entry whose word `+8` equals the argument (`0046EE70`, then `003697F0`) and nulls it, then calls `003A8510(argument)` | `00333768` movzx, `0033377D` call, `0033378D` call, `00333792` mov, `0033379B` call |
| `0033B6D0` | 28 B | calls `00338490`, then clears bit 0 of dword `022C7D04` and byte `022C7CE9` | `0033B6D4` call, `0033B6D9` and, `0033B6E0` mov |
| `003574B0` | 115 B | calls `00267E10(r9)` and `00267F90(r9, 0)`, forwards its four arguments to `00340970`, calls `00263FF0(0)`, `002348E0` and `0035A6F0`, and tail-calls `00269800` with `00263FF0`'s result | `003574D3` call, `003574EE` call, `003574F5` call, `00357502` call, `0035751E` jmp |
| `003586A0` | 31 B | sets bit `ecx` of byte `022C7F9A` when `edx` is non-zero, else clears it | `003586AB` bts, `003586B5` btr, `003586B8` mov |
| `00358C60` | 71 B | copies the 16 bytes at `008C5FD0` to `022C7FD0`, calls `0025A520(2, 0)`, and tail-calls `00358CB0` when dword `022C7FEC` is non-zero or when `002671F0()` is non-zero and dword `022C7FE0` is positive | `00358C6D` movaps, `00358C77` call, `00358C84` jne, `00358C97` jle, `00358C9D` jmp |
| `00359800` | 115 B | steps on word `022C8010`: 1 tail-calls `00359A30`; 3 clears words `022C8024` / `022C8028`, sets 4 and calls `0037C910`, then continues as 4; 4 sets 5 and tail-calls `00359880` when `0037CB40()` is non-zero; 5 tail-calls `00359880`; other values return | `0035980E` je, `00359828` mov, `0035983B` mov, `00359855` mov, `00359860` jmp, `00359869` jmp |
| `0035A6F0` | 44 B | calls `00473830(0, 1)`, `00238B70(0)` and `00238AE0(0)`, and tail-calls `00267D40(2, 0)` | `0035A6FB` call, `0035A702` call, `0035A709` call, `0035A717` jmp |
| `0035AB20` | 33 B | calls `00238B70(1)` and `00238AE0(1)`, and tail-calls `0035A590` | `0035AB29` call, `0035AB33` call, `0035AB3C` jmp |
| `0035B5D0` | 126 B | calls `0035B1A0` on each non-zero dword of the eight at `022C8030` and zeroes it; then, for each `0x20`-byte record from `02EC0B82` to `02EC0F82` whose preceding flag byte is set, calls `0035B1A0(word << 8 OR index)` with the index counted from 1 | `0035B5F6` call, `0035B5FB` mov, `0035B620` cmp, `0035B629` shl, `0035B62E` call |
| `0035C700` | 61 B | returns 1 when dword `022C83E8` has bit `0x100` or dword `02092730` is `0x0B` or `0x18`, else whether `002E12D0()` is non-zero | `0035C704` test, `0035C720` cmp, `0035C728` je, `0035C72A` call, `0035C733` setne |
| `0035C740` | 12 B | returns bit 1 of dword `022C83E8` | `0035C746` shr, `0035C748` and |
| `003606E0` | 46 B | sets byte `022CB9BC` to 1 when any of the three dwords `022CB9DC` to `022CB9E4` is non-zero, else to 0 | `003606F0` cmp, `003606FE` mov, `00360706` mov |
| `00361700` | 44 B | stores its second argument at byte `022CBA9B` and its float argument, clamped to at most float `01CEBBA8` when the second argument is 0 and to at least 0.0, at float `022CBB28` | `0036170F` minss, `00361719` mov, `0036171F` maxss, `00361723` movss |
| `0036EEB0` | 262 B | when byte `022D9B40` is 1 and any `0x18`-byte record in `022D9AB0`..`022D9B40` has state byte 1 or 2, repeats `0032E040`, `0036D890`, `0035EA30(2)` until `0036F000()` is non-zero; then calls `002DF430(0)` and sets the byte to 2; byte `022D9B41` gets the same treatment with `002DF430(1)` | `0036EEF5` cmp, `0036EF20` call, `0036EF34` call, `0036EF3F` call, `0036EF44` mov, `0036EF4B` cmp, `0036EFA7` mov |
| `0036F460` | 110 B | stores its float argument at float `02AD9B50` (reduced by repeated adds of float `01CEBC9C` while at least float `01CEBBA8`), passes (argument minus the previous `02AD9B50`) times float `008F8D80`, divided by float `01DFE0B8` times float `008F8D80`, to `004678E0` and tail-calls `00468520` | `0036F472` subss, `0036F47A` movss, `0036F490` addss, `0036F4B9` divss, `0036F4C0` call, `0036F4C9` jmp |
| `0036F530` | 25 B | calls `0026E260` and `003ECCA0`, then tail-calls `003ED7F0(0)` | `0036F534` call, `0036F539` call, `0036F544` jmp |
| `0036FD90` | 83 B | for index 0 or 1 zeroes the six words `02AD9E24`, `02AD9E28`, `02AD9E2C`, `02AD9E08`, `02AD9E0C`, `02AD9E10` plus twice the index; any other index calls `00809728` | `0036FD9A` cmp, `0036FDA9` mov, `0036FDD1` mov, `0036FDDE` call |
| `00374060` | 80 B | returns 0 when the record's `+0x1C` bit 1 is set and dword `+0x24` is below dword `+0x6C`, provided `00254A70(record)` is non-zero, or word `020926E4` lacks bit `0x800`, or dword `+0x68` equals `002EF9F0(3)`; otherwise returns 1 | `00374069` call, `00374077` test, `0037408A` cmp, `0037408F` test, `00374098` cmp, `0037409D` xor |
| `003A1D50` | 82 B | calls `004FE3C0` on `02EBEFC0` and `02EBEFD8`, clears dword `02EBEFF0`, calls `004FE420(02EBEFC0, 0x200, 0)` and tail-calls `004FE420(02EBEFD8, 0x200, 0x200)` | `003A1D5B` call, `003A1D6F` mov, `003A1D85` call, `003A1D9D` jmp |
| `003A7300` | 85 B | calls `003A7360`, then, for the four dwords `+0x110` to `+0x11C` of `*02F97348`, calls `002FC340` on each non-zero one and zeroes it | `003A730A` call, `003A7327` mov, `003A732E` call, `003A733A` mov, `003A7341` cmp |
| `003A76F0` | 50 B | zeroes the 256 qwords from `+8` of the block at `*02EBEFA8`, then its dword `+0` | `003A7707` mov, `003A7710` cmp, `003A771F` mov |
| `003A7D00` | 44 B | allocates `0x400` bytes with `0036A100`, stores the pointer through `*02EBEFA0` and tail-calls `00861EC0(block, 0, 0x400)` | `003A7D09` call, `003A7D1D` mov, `003A7D27` jmp |
| `003A7EE0` | 127 B | walks the `+0xF0` list from `**02EBEF98` clearing bit 0 of byte `+0x103` on every node, then walks it again calling `004FF0D0(node, float argument)` on each node whose bit is still clear | `003A7F00` and, `003A7F30` test, `003A7F43` call |
| `003A9560` | 44 B | allocates `0xA00` bytes with `0036A100`, stores the pointer through `*02EBEF90` and tail-calls `00861EC0(block, 0, 0xA00)` | `003A9569` call, `003A957D` mov, `003A9587` jmp |
| `003A9920` | 44 B | allocates `0x1800` bytes with `0036A100`, stores the pointer through `*02EBEF78` and tail-calls `00861EC0(block, 0, 0x1800)` | `003A9929` call, `003A993D` mov, `003A9947` jmp |
| `003A9CC0` | 57 B | zeroes qwords `+0`, `+8`, `+0x10` and words `+0x18`, `+0x1A` of the block at `*02EBEF70` | `003A9CC9` mov, `003A9CDE` mov, `003A9CF4` mov |
| `003B22D0` | 57 B | searches the `0x30`-byte records from `02EBE5E0` (up to `02EBEBE0`, stopping at a zero entry) for one whose dword `+0` equals the argument, and sets that record's dword `+0x1C` to 3 | `003B22E8` je, `003B22EA` cmp, `003B22FA` cmp, `003B2300` mov |
| `003B6C20` | 73 B | zeroes the `0x20` dwords at `02EBCBE0`, the dwords `02EBCC70`, `02EBCC60`, `02EBCBC0`, `02EBCAA0` and the 32 bytes at `02EBCA80` | `003B6C33` mov, `003B6C39` rep stosd, `003B6C46` mov, `003B6C58` movdqu, `003B6C60` movdqu |
| `003DBAE0` | 127 B | calls `003DBCF0(record, third argument, 2)`; when that returns 1 and the record is not the second argument, it turns state byte 1 into 2 in the `+0x89` entries of `0x14` bytes at `+0xA0` (when byte `+0x63` is set), calls `003DB6E0(record)` and halves byte `+0x63`; returns `003DBCF0`'s result | `003DBB01` call, `003DBB12` cmp, `003DBB35` mov, `003DBB45` call, `003DBB4A` shr |
| `003DC710` | 108 B | for each of the 16 `0x14`-byte records at `02B57F70` with state byte `+6` 3, byte `+7` 0 and word `+4` 0, adds `0x10` to dword `+8`, sets the state to 4 and dword `02B58170` to 1, and when bits 4 to 19 of `+8` wrap to zero replaces it with byte `+0x13` OR `0x10` | `003DC72A` cmp, `003DC743` add, `003DC752` mov, `003DC758` mov, `003DC76D` mov |
| `003DC780` | 125 B | for a positive handle whose record `02B57F70[handle AND 0xF]` (`0x14` bytes) holds it at `+8`, decrements word `+4`, and at 0 or below stores 0 there and sets dword `02B58170` to 1; then tail-calls `003DCF20` when byte `+7` is 0 (the body ends at `003DC7C9`; the listed 125-byte extent runs into the next function) | `003DC79A` cmp, `003DC7A4` dec, `003DC7B1` mov, `003DC7BB` mov, `003DC7C3` je |
| `003DF670` | 108 B | clears bit 0 of dword `02B59D18` when `003588B0(003590D0())` returns an actor that `002EA6A0` accepts, else sets it; when the dword is then 0 tail-calls `003DF810`, otherwise calls `0029CAB0(0, 0, 0, 0)` and zeroes dwords `02B59D14`, `02B59D10` and qwords `02B59D08`, `02B59D00` | `003DF67B` call, `003DF691` and, `003DF69A` or, `003DF6A7` jmp, `003DF6B6` call, `003DF6D0` mov |
| `003E1310` | 54 B | when its second argument is 0 and `0020E600` resolves the record's dword `+0`, stores the low byte of its third argument at byte `+7` of the resolved object | `003E1326` call, `003E1337` mov |
| `003E8990` | 124 B | clears bits 3 and 4 of word `+0`; when word `+2` is non-negative calls `00473500(it, float 01CEBC9C, float 01CEBC9C)` and `004735D0(it, 0.0)`; when word `+0x10` is at most `0x3E7` calls `00363A90(it, (byte +0x14 >> 4) != 1, 1)` | `003E89A8` and, `003E89C3` call, `003E89CD` call, `003E89D2` cmp, `003E89F7` call |
| `003E8A10` | 38 B | calls `0037A3B0(0, first argument)` when the second argument is non-zero, else `0037A310(0, first argument)`; returns 0 | `003E8A1C` call, `003E8A2A` call, `003E8A2F` xor |
| `003E8A40` | 38 B | calls `0037A1D0(0, first argument)` when the second argument is non-zero, else `0037A130(0, first argument)`; returns 0 | `003E8A4C` call, `003E8A5A` call, `003E8A5F` xor |
| `003E8A70` | 38 B | calls `0037B190(0, first argument)` when the second argument is non-zero, else `0037B0F0(0, first argument)`; returns 0 | `003E8A7C` call, `003E8A8A` call, `003E8A8F` xor |
| `003E9100` | 30 B | calls `00408200` when byte `02B5D090` is set, then clears the byte | `003E910D` call, `003E9112` mov |
| `003EB6C0` | 59 B | for an index up to `0x1F`, releases the pointer `02B5EA20[index]` with `003EB470` when it is non-null and nulls it | `003EB6C4` cmp, `003EB6E5` call, `003EB6EA` mov |
| `003EC5F0` | 42 B | for i = 0 to 15 calls `003EB6C0(i)` whenever `00377C20()` returns 0 | `003EC5F8` call, `003EC608` call, `003EC60F` cmp |
| `003EC690` | 47 B | when dword `02B5EC94` is non-zero, calls `002EBD60(it, 0)` and `002E3DC0(it)` and clears it | `003EC6A0` call, `003EC6AB` call, `003EC6B0` mov |
| `003ED170` | 21 B | copies the 16 bytes at its argument to `02EBB7D0` when the argument's first dword is greater than the dword at `02EBB7D0` | `003ED176` cmp, `003ED17D` movups |
| `00428F10` | 31 B | sets bit 5 of dword `+0x304` to (second argument non-zero) and sets bit 28 of dword `+0x290` | `00428F19` sbb, `00428F1E` or, `00428F24` or |
| `0042FCE0` | 11 B | increments dword `02CA4ED4` (the `inc` at the entry) and tail-calls `002FCBF0` | `0042FCE6` jmp |
| `00466170` | 30 B | returns byte `+0` OR byte `+4` << 8 OR byte `+8` << 16 OR dword `+0xC` << 24 of its argument | `00466177` shl, `00466183` shl, `0046618B` or |
| `00466AD0` | 53 B | for an index below dword `02EBB6E0` whose `0x50`-byte entry at `*02EBB6F0` has a non-null `+8`, returns bit 2 of the entry's dword `+0x4C`; otherwise returns 1 | `00466AD4` cmp, `00466AEE` cmp, `00466AF8` shr, `00466AFF` mov |
| `00466BB0` | 51 B | for a valid index of the `0x50`-byte table at `*02EBB6F0` (count dword `02EBB6E0`), returns float `+0x24` of the entry's `+8` object, else 0.0 | `00466BD5` mov, `00466BD9` movss, `00466BDF` xorps |
| `00466C40` | 51 B | for a valid index of the `0x50`-byte table at `*02EBB6F0` (count dword `02EBB6E0`), returns float `+0x20` of the entry's `+8` object, else 0.0 | `00466C65` mov, `00466C69` movss, `00466C6F` xorps |
| `00467660` | 82 B | for a valid entry of the same table, stores its two float arguments at `+0x3C` and `+0x40`, raising `+0x3C` to the `+8` object's float `+0x20` and lowering `+0x40` to its float `+0x24` when they lie outside | `00467689` movss, `0046768E` movss, `0046769D` movss, `004676AC` movss |
| `004676C0` | 50 B | for a valid entry of the same table, sets bit 1 of dword `+0x4C` to bit 0 of the second argument | `004676E5` and, `004676EE` or |
| `00467700` | 43 B | for a valid entry of the same table, stores its float argument at `+0x38` | `00467725` movss |
| `004678E0` | 86 B | when qword `02EBB6F8` is non-null, adds the float argument times float `+0x38` to float `+0x48` of every `0x50`-byte entry at `*02EBB6F0` (count dword `02EBB6E0`) whose dword `+0x4C` has bit 0 | `00467907` test, `00467911` mulss, `00467917` addss, `0046791D` movss |
| `00468520` | 82 B | for each `0x40`-byte entry at `*02CA6010` (count dword `02CA6020`) whose dword `+4` is 0, calls `003CD820` with its dword `+0x14` | `00468547` cmp, `0046854E` mov, `00468552` call |
| `0046FFA0` | 85 B | when bit `edx` of the record's dword `+0` is clear, sets it, adds 2 to byte `+7` keeping its bit 0, and stores in byte `+5` the lowest set bit among bits 0 to 13 (`0xFF` when none) | `0046FFB6` or, `0046FFC1` mov, `0046FFC9` add, `0046FFCE` mov, `0046FFF0` mov |
| `00470050` | 97 B | when bit `edx` of the record's dword `+0` is set, clears it, subtracts 2 from byte `+7` keeping its bit 0, and stores in byte `+5` the lowest set bit among bits 0 to 13 (`0xFF` when none) | `0047006B` and, `00470076` mov, `0047007D` dec, `00470083` mov, `004700AC` mov |
| `0050D240` | 42 B | calls `00267E10(r9)`, passes the result to `0017D280` with the constant at `00D22998`, and tail-calls `0026A5F0` with it | `0050D249` call, `0050D259` call, `0050D265` jmp |
| `0051DBF0` | 109 B | when bit `edx` of dword `+0x10` is clear, sets it and rederives the bytes: `+0x19` is 2 with bit 2, else 3 with bit 3, else `0xFF`; `+0x31` is 0 with bit 0, else 1 with bit 1, else `0xFF`; `+0x33` is bit 4 | `0051DC08` or, `0051DC18` mov, `0051DC2E` mov, `0051DC3D` mov, `0051DC54` mov |
| `0051DDC0` | 111 B | when bit `edx` of dword `+0x10` is set, clears it and rederives bytes `+0x19`, `+0x31` and `+0x33` from the remaining bits exactly as `0051DBF0` does | `0051DDDF` and, `0051DDEA` mov, `0051DE00` mov, `0051DE0F` mov, `0051DE26` mov |
| `0051E620` | 69 B | zeroes dword `+0xD4`; when the `+0x10` member is non-null, calls `003E1350(member, 3)` and clears bit 2 of byte `+0x1C` of the object `0020E600` resolves from the member's dword `+8` | `0051E62A` mov, `0051E641` call, `0051E65B` and |
| `0051E670` | 78 B | sets dword `+0xD4` to 1; when the `+0x10` member is non-null, calls `003E1610(member, 3)` unless dword `+0xD0` is non-zero, and sets bit 2 of byte `+0x1C` of the object resolved from the member's dword `+8` | `0051E67A` mov, `0051E689` cmp, `0051E69A` call, `0051E6B4` or |
| `0051E700` | 60 B | zeroes dword `+0xF8`, calls `0051DDC0(object +0x70, 0)` and, when the `+0x10` member is non-null, tail-calls `003E1350(member, 7)` | `0051E709` mov, `0051E719` call, `0051E731` jmp |
| `0051E740` | 60 B | sets dword `+0xF8` to 1, calls `0051DBF0(object +0x70, 0)` and, when the `+0x10` member is non-null, tail-calls `003E1610(member, 7)` | `0051E749` mov, `0051E759` call, `0051E771` jmp |
| `0051E800` | 60 B | stores 0 (not 1) in dword `+0x128`; when the `+0x10` member is non-null, calls `003E1350(member, 6)` and tail-calls `0016D6A0(member, 0)` | `0051E809` mov, `0051E821` call, `0051E831` jmp |
| `0051E840` | 63 B | sets dword `+0x128` to 1; when the `+0x10` member is non-null, calls `003E1610(member, 6)` and tail-calls `0016D6A0(member, 1)` | `0051E849` mov, `0051E861` call, `0051E874` jmp |
| `0051E9C0` | 78 B | zeroes dword `+0xD0`; when the `+0x10` member is non-null, calls `003E1610(member, 3)` when dword `+0xD4` is non-zero, and clears bit 1 of byte `+0x1C` of the object resolved from the member's dword `+8` | `0051E9CA` mov, `0051E9D9` cmp, `0051E9EA` call, `0051EA04` and |
| `0051EA10` | 78 B | sets dword `+0xD0` to 1; when the `+0x10` member is non-null, calls `003E1350(member, 3)` when dword `+0xD4` is non-zero, and sets bit 1 of byte `+0x1C` of the object resolved from the member's dword `+8` | `0051EA1A` mov, `0051EA29` cmp, `0051EA3A` call, `0051EA54` or |
| `0051EAE0` | 93 B | zeroes dword `+0xC4`, calls `00470050(object +0x20, 0)` and tail-calls `00428F10(record, 0)`, the record being the `0x740`-byte entry of `*022C6F28` that word `+4` names (null for -1 or an entry whose dword `+0x284` is 0) | `0051EAEF` mov, `0051EAFB` call, `0051EB1C` cmp, `0051EB38` jmp |
| `0051EB40` | 89 B | sets dword `+0xC4` to 1, calls `0046FFA0(object +0x20, 0)` and tail-calls `00428F10(record, 1)` with the same record lookup as `0051EAE0` | `0051EB49` mov, `0051EB59` call, `0051EB7C` cmp, `0051EB94` jmp |
| `0051EBA0` | 109 B | zeroes dword `+0xCC`, calls `00428F10(record, 0)` (record as in `0051EAE0`) and `0051DDC0(object +0x70, 4)`, and when the `+0x10` member is non-null tail-calls `003E1310(member, 0, 0)` | `0051EBAF` mov, `0051EBDC` call, `0051EBEA` call, `0051EC02` jmp |
| `0051EC10` | 117 B | sets dword `+0xCC` to 1, calls `00428F10(record, 1)` and `0051DBF0(object +0x70, 4)`, and when the `+0x10` member is non-null tail-calls `003E1310(member, 0, 1)` | `0051EC1D` mov, `0051EC53` call, `0051EC61` call, `0051EC7A` jmp |
| `00797A20` | 172 B | copies its string argument into a stack buffer sized to it (`00808F10` stack probe, `00861EBA` copy), cuts the copy at the first comma after its first character, calls `0079FB10(first argument, buffer)` and checks the stack cookie (`00808C40`) | `00797A53` cmp, `00797A74` call, `00797A84` call, `00797A99` cmp, `00797AA4` mov, `00797AAD` call |

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**CombatFormula — CLIENT.** `BattleFormula_DispatchPostResultEvents`, owned by that layer, calls `0046AB10` on this page. That caller is the post-result dispatch, 1,904 bytes working from a `0x70`-byte frame; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Audio — CLIENT both ways.** `003A7050`'s slot-eviction arm calls `00332750`, which calls into Audio (`00332C40`); in the other direction Audio (`00360B50`, `003635E0`) calls the shared free helper `003697F0` this page cites. The tick holds no audio state - the crossing is one Audio callee inside a helper the timer channel uses, plus Audio borrowing a shared deallocator.

**Presentation — member work hosted in the tick.** `003A7050` and `003A8390` are Presentation-owned bodies the world tick drives, and `003A7050`'s slot-maintenance callees (`00332750`, `00333350`, `003334B0`, `00333740`) plus the shared free `003697F0` carry the rest of their traffic to and from Presentation callers - the tick drives Presentation-owned timer channels rather than owning presentation behaviour itself.

**Input — shared helpers.** The batch-146 slot-table entries name `0046E990` and `0046EE70`, which bottom out in the `0035B1A0`-family lookups that Input bodies also call, and `00861EBA`, the shared block-move Input reaches through `00797A20` - the scheduled-marker executor borrows shared utility code; no Input behaviour lives on this page.

**Resource — SERVICE.** The batch-147 async-submit arms `003B2310` and `002FC860` dispatch through the shared submit helpers `0032E400` and `0032E620`, which that layer owns (`003B25D0`/`002FCF00` reach `0032E4D0` the same way), and most of those helpers' callers are that layer's own (`00249210`, `0024AC30`, `00259DF0`, `00324510`, `0032EB40`, `00379E90`, `00384420`, `0039C3F0`, `0051ED10`) - the tick borrows the shared submit plumbing; it owns no resource state.

**ActorEntity — CLIENT of the same helpers.** `0032E400` and `0032E620` are also called by `0032FCA0`, `00330310` and `003306E0` of this layer - actor code borrowing the same shared submit plumbing, not actor work the tick drives.

**Save_Load_Settings — CLIENT of the same helpers.** `002EF300` of that layer is one more caller of the shared submit helper `0032E620` - the same borrow pattern, nothing the tick drives.

**Script_VM_Native_Bridge — CLIENT of the same helpers.** `0032E400`/`0032E620` are called by the script VM native bridge's `0050DF70`/`0050DFE0`, and the `003B2310` entry's fallback `002DEBB0` is itself called by `0034B650` of that layer - the shared submit plumbing reaches the bridge in both directions; no bridge behaviour lives on this page.

**Movement — CLIENT of shared helpers (SWE2-EC7, batch 166).** Movement bodies (`0025DF00`,
`00334220`, `003347C0`) call the shared accessors `001EDDA0`, `001EDE80` and `00202B10` that this
page's tick machinery also cites - the walk-tick borrows movement accessors the same way other
subsystems do; the tick owns no Movement behaviour.

**UI — CLIENT of the manager plumbing (SWE2-EC7, batch 166).** UI bodies (`003C8B70`,
`0024B9B0`, `00276960`, `0027C870`) reach the shared shims `0017DDC0`, `00181DD0` and `001E0C10`,
and batch-166's `00290320`/`00290B90`/`0028FA50` are `[0209BE80]`-manager plumbing that UI callers
(`0027DE30` among them) ride - consultation through shared plumbing, not UI work owned here.
- **CombatAI — CLIENT and SERVICE (54 edges).** 43 inbound (CombatAI bodies `AiOrder_EvaluateTargetSelector` (00301AD0), `BattleUnit_UpdateCombatFrame` (00308610), `AiOrder_BuildCandidateTargetBufferFromStoredRangeAndStatus` (0030F130) call page-cited `BattleEncodedId_IsValidForClass` (00322C50), `BattleUnit_GetBySlotIndex` (00236820), `FieldData_GetActiveFieldRecordBit15` (00313F60)); 11 outbound (page-cited `BattleUnit_UpdateLifecycleAndCombatFrame` (00233F70), `BattleSystem_RunFieldFrameOrchestrator` (00234590), `BattleUnit_RebuildPerceptionCandidateCache` (003247F0) call CombatAI bodies `BattleUnit_SelectAndCommitNextAction` (00305AB0), `BattleUnit_UpdateCombatFrame` (00308610), `BattleUnit_RebuildPerceptionCandidateCache` (003247F0)). Substantive edges include `BattleUnit_UpdateLifecycleAndCombatFrame` (00233F70) calls `BattleUnit_RebuildPerceptionCandidateCache` (003247F0); `002341C0` calls `BattlePerception_ResetCandidateCacheGeneration` (00325080); `BattleSystem_RunFieldFrameOrchestrator` (00234590) calls `BattlePerception_AdvanceCandidateCacheGeneration` (00325060); `BattleSystem_RunFieldFrameOrchestrator` (00234590) calls `BattlePerception_ResetSpatialVisibilityCacheFrameState` (0032A650); the remaining edges run through shared helpers the page cites.
- **Items_Equipment_Shops_License — CLIENT and SERVICE (37 edges).** 34 inbound (Items_Equipment_Shops_License bodies `InventoryEquipment_SnapshotAndClearTemporaryState` (0030FBE0), `BattleIdClassD_ResetPurchasedEntryAndNestedPrerequisiteState` (0030B180), `InventoryEquipment_RestoreTemporarySnapshotAndClearBackup` (0030FAA0) call page-cited `BattleEncodedId_IsValidForClass` (00322C50), `Inventory_ModifyEncodedItemAndUpdateDiscoveryState` (003008A0), `BattleStats_GetByMappedBattleSlot` (00320AB0)); 3 outbound (page-cited `Inventory_ModifyEncodedItemAndUpdateDiscoveryState` (003008A0), `00308DE0`, `00329220` call Items_Equipment_Shops_License bodies `Inventory_QueryEncodedItemStateByClass` (00309F30), `Inventory_ModifyEncodedItemAndUpdateDiscoveryState` (003008A0), `BattleStats_CountLicenseBits00To17` (00324020)). Substantive edges include `00308DE0` calls `Inventory_ModifyEncodedItemAndUpdateDiscoveryState` (003008A0); `00329220` calls `BattleStats_CountLicenseBits00To17` (00324020); `FieldData_GetActiveFieldRecordBit15` (00377C20) is called by `Equipment_UnequipEncodedItemFromActiveRoster` (0030FD10); `FieldData_GetActiveFieldRecordBit15` (00377C20) is called by `Inventory_QueryOwnedCountIncludingReservedActionItems` (00309FB0); the remaining edges run through shared helpers the page cites.
- **Party — CLIENT and SERVICE (159 edges).** 92 inbound (Party bodies `PartyControl_ApplyAnalogLocomotionToActor` (00358CB0), `PartyControl_RecomputeSuppressionFromLeaderBattleState` (0023B040), `PartyFocus_ProcessActorControlPresentationState` (00358F90) call page-cited `BattleEncodedId_IsValidForClass` (00322C50), `PartyRoster_GetActorBySlot` (00263750), `PartyFocus_GetCurrentPackedActorHandle` (003590D0)); 67 outbound (page-cited `PartyControl_RecomputeSuppressionFromLeaderBattleState` (0023B040), `00226BE0`, `BattleSystem_RunFieldFrameOrchestrator` (00234590) call Party bodies `PartyFocus_GetCurrentPackedActorHandle` (003590D0), `BattleUnit_GetPartyLeader` (003272A0), `BattleUnit_ResolveByFocusHandle` (0031B7E0)). Substantive edges include `0017DFC0` is called by `PartyControl_BuildAnalogMovementVectorFromInputHistory` (003594E0); `001E0C10` is called by `PartyControl_BuildAnalogMovementVectorFromInputHistory` (003594E0); `0022A770` calls `PartyFocus_CommitPendingPackedActorHandle_Thunk` (00358BB0); `MainLoop_UpdateAndRenderFrame` (0022B8C0) calls `PartyFocus_CommitPendingPackedActorHandle_Thunk` (00358BB0); the remaining edges run through shared helpers the page cites.
- **RNG_Random_Selection — SERVICE (2 edges).** 2 outbound (page-cited `0022B6E0`, `BattleSystem_InitializeAreaState` (002342F0) call RNG_Random_Selection bodies `RNG_MT19937_NextU32_Thunk` (00379CD0), `RNG_SharedGameplayLCG_SetState` (00328D80)). Substantive edges include `BattleSystem_InitializeAreaState` (002342F0) calls `RNG_SharedGameplayLCG_SetState` (00328D80); the remaining edges run through shared helpers the page cites.
- **Spawn_Encounter_Lifecycle — CLIENT and SERVICE (56 edges).** 49 inbound (Spawn_Encounter_Lifecycle bodies `SpawnLifecycle_CheckAndRetireByNativeRange` (002350C0), `Spawn_ValidateCandidateDistanceToPlayers` (00234DA0), `SpawnGroup_RecordMemberDeathAndHandleCompletion` (00306F00) call page-cited `ActorWork_GetBattleUnit` (0031B760), `BattleUnit_TeardownAndDespawn` (00300E40), `Actor_GetWorldPosition` (00265020)); 7 outbound (page-cited `BattleUnit_UpdateLifecycleAndCombatFrame` (00233F70), `BattleSystem_InitializeAreaState` (002342F0), `BattleSystem_RunFieldFrameOrchestrator` (00234590) call Spawn_Encounter_Lifecycle bodies `SpawnLifecycle_CheckAndRetireByNativeRange` (002350C0), `SpawnGroup_HasPendingCompletionSignal` (003070E0), `SpawnKeep_RotatePersistenceBanksForAreaTransition` (00233780)). Substantive edges include `00233D20` is called by `SpawnGroup_DispatchPendingCompletionSignals` (00307030); `BattleUnit_UpdateLifecycleAndCombatFrame` (00233F70) calls `SpawnLifecycle_CheckAndRetireByNativeRange` (002350C0); `BattleUnit_UpdateLifecycleAndCombatFrame` (00233F70) calls `SpawnGroup_HasPendingCompletionSignal` (003070E0); `BattleSystem_InitializeAreaState` (002342F0) calls `SpawnKeep_RotatePersistenceBanksForAreaTransition` (00233780); the remaining edges run through shared helpers the page cites.
- **Status_Periodic_Terminal — CLIENT and SERVICE (26 edges).** 21 inbound (Status_Periodic_Terminal bodies `BattleUnit_RunPeriodicCombatMaintenance` (00310DB0), `BattleStats_ChangeStatusAndProcessSideEffects` (0030E360), `BattleUnit_RecoverFromTerminalStatusSetIfClear` (00301140) call page-cited `BattleEncodedId_IsValidForClass` (00322C50), `GameClock_GetRawTickCounter` (0032A150), `FieldData_GetActiveFieldRecordBit15` (00377C20)); 5 outbound (page-cited `BattleUnit_RunPeriodicCombatMaintenance` (00310DB0), `BattleUnit_UpdateLifecycleAndCombatFrame` (00233F70), `BattleSystem_InitializeAreaState` (002342F0) call Status_Periodic_Terminal bodies `BattleUnit_RunPeriodicCombatMaintenance` (00310DB0), `BattleStats_RemoveStatusMode0` (0030E990), `BattleUnit_ResetActionControlForStatusTransition` (00300140)). Substantive edges include `BattleUnit_UpdateLifecycleAndCombatFrame` (00233F70) calls `BattleUnit_RunPeriodicCombatMaintenance` (00310DB0); `BattleSystem_InitializeAreaState` (002342F0) calls `BattleStats_RemoveStatusMode0` (0030E990); `BattleSystem_RunFieldFrameOrchestrator` (00234590) calls `BattleUnit_ResetActionControlForStatusTransition` (00300140); `00265680` is called by `BattleUnit_RunPeriodicCombatMaintenance` (00310DB0); the remaining edges run through shared helpers the page cites.
- **StoryEvent — CLIENT (3 edges).** 3 inbound (StoryEvent bodies `001ED240` call page-cited `001C50C0`, `001EC560`, `FieldData_GetVariable0` (00265270)). Substantive edges include `001C50C0` is called by `001ED240`; `001EC560` is called by `001ED240`; `FieldData_GetVariable0` (00265270) is called by `001ED240`.
- **Story_Event_Quest_Hunt — CLIENT and SERVICE (15 edges).** 13 inbound (Story_Event_Quest_Hunt bodies `PersistentFlag_QueryAuthoredThresholdSchedule` (00377970), `PersistentFlag_QueryBank64B` (0032AA00), `PersistentFlag_QueryPrimaryOrAuthoredThresholdGate` (0032A8A0) call page-cited `SaveImage_GetPersistentPayloadBase` (002EF2B0), `FieldData_GetVariable0` (00265270)); 2 outbound (page-cited `InputGameplay_ArbitrateDigitalInputAndModalState` (00253C70), `ActorManager_BindLoadedDefinitionPayload` (0026C8C0) call Story_Event_Quest_Hunt bodies `PersistentFlag_QueryPrimaryOrAuthoredThresholdGate` (0032A8A0), `EventMemory_QueryDefinitionIdAbsent` (00377440)). Substantive edges include `FieldData_GetVariable0` (00265270) is called by `PersistentFlag_QueryAuthoredThresholdSchedule` (00377970); `ActorManager_BindLoadedDefinitionPayload` (0026C8C0) calls `EventMemory_QueryDefinitionIdAbsent` (00377440); the remaining edges run through shared helpers the page cites.
## The `0032FC30` exclusive subtree — all 2 members bound (SWE2-FRONTIER, followup queue)

`0032FC30` `WorldSimulation_ProcessDeferredModeRequest` (66 B) — the
deferred world-mode dispatch: `003EA6E0` (`0032FC4B`), `00408B30`
result `== 1` early-out (`0032FC55`), `00408B10` `== 3` early-out
(`0032FC5F`), `005C5230` contract check on `rbx+5` (`0032FC67`),
`003319D0` (`0032FC72`), tail `0032FCA0` (`0032FC7B`).

| member | role | interior |
| --- | --- | --- |
| `0025D4D0` (23 B) | registry-record flag clear — `imul rcx, movsxd(ecx), 0x288` index into the `02098E10` array, `and byte[rcx+rax+0x10], 0xFD` clears bit 1 (`0025D4D0`–`0025D4E6`); the `+0xB8`/`+0xD8`/`0x60` payload probe is sibling `0025D4F0` | [`0025D4E1`](../../_index/ADDRESS-INDEX.md) |
| `003EA6E0` | pending-count compare — `00264ED0` (`003EA6E8`) vs `dword[02B5E0B8]` (`003EA6ED`), `test ebx` (`003EA6F5`), jmp into the `003EA820` tail (`003EA700`) | [`003EA6ED`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `00408B30`, `00408B10`, `005C5230`,
`003319D0`, `0032FCA0`, `00264ED0`, `003B42B0`. The `02098E10` cell is
the shared stop-registry context; `02B5E0B8` is the pending-request
count cell.

## The `0030C970` exclusive subtree — all 2 members bound (SWE2-FRONTIER, followup queue)

`0030C970` `BattleAction_ReleasePresentationSlot` (50 B) — slot `cl ≤
0x1F` bounds-check (`0030C983`), record `rbx = 022C17B0 + cl*48`
(`rax+rax*2` then `shl 4`, `0030C98C`–`0030C994`), `cl == 0xFF` → out
(`0030C99C`).

| member | role | interior |
| --- | --- | --- |
| `00317EC0` (13 B) | guard thunk — `eax = ecx+1`; `ecx ∉ {0, −1}` → `jmp 0042FCC0`, else `ret` (`00317EC0`–`00317ECC`) | [`00317EC3`](../../_index/ADDRESS-INDEX.md) |
| `00325A00` (19 B) | dispatch thunk — `test ecx, 0x7FFFFFFE` / `cmp ecx, 1`, tail `003DC780` (`00325A00`–`00325A0D`) | [`00325A00`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `0042FCC0`, `003DC780`. The
`022C17B0` array is the shared 48-byte presentation-slot records.

## The `0031ADB0` exclusive subtree — all 2 members bound (SWE2-FRONTIER, followup queue)

`0031ADB0` (616 B) — a per-actor service pass gated repeatedly on the
`02089340` flag word: bit `0x10` at `0031ADF1`/`0031AE73`/`0031AED6`,
bits `0x600` at `0031AF34`; actor resolves through `003588B0` ×3 and
`003589B0` (`0031AE08`/`0031AE7F`/`0031AEE2`/`0031AE4C`), `00265020`
×3 (`0031AE98`/`0031AEC1`/`0031AEFB`), `00322280` (`0031AF17`), then
member `00320E10` (`0031AF82`).

| member | role | interior |
| --- | --- | --- |
| `0030A160` (36 B) | max-of-two helper — `00265090` fills `[rsp+0x38]`/`[rsp+0x40]`, returns `maxss xmm0, [rsp+0x40]` (`0030A16E`/`0030A179`); the `[02EBF138]`/`0020E600` row fetch is sibling `0030A190` | [`0030A179`](../../_index/ADDRESS-INDEX.md) |
| `00320E10` (580 B) | actor-object stage — `02089340` bit-`0x10` gate (`00320E31`), `dword[rcx+0x710]` → `003588B0` (`00320E3A`/`00320E40`) | [`00320E40`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `003588B0`, `003589B0`, `00265020`,
`00322280`, `00265090`, `0020E600`. The `02089340` word is the shared
service/test flag cell.

## The `0034DB30` exclusive subtree — all 2 members bound (SWE2-FRONTIER, followup queue)

`0034DB30` (171 B) — a record-field update/check: `ecx =
dword[r8+4]`, `edi = 1`, `dword[r8]` → `00360A20` (`0034DB59`),
`00229EB0` result vs `byte[rbx+8]` (`0034DB8A`/`0034DB8F`), then
`003608D0` (`0034DBAC`), `00360D60` (`0034DBBC`), `002F1A30`
(`0034DBCE`).

| member | role | interior |
| --- | --- | --- |
| `003608D0` (136 B) | counter-bounded table op — `dword[022CB9B0]` nonzero gate (`003608D4`), `002DE350` (`003608E2`), `dword[022CB9B8]` + `edx = 0x10` (`003608E7`/`003608ED`) | [`003608E7`](../../_index/ADDRESS-INDEX.md) |
| `00360A20` (35 B) | count wrapper — `00360A50` (`00360A26`), result to `ebx`, `003601C0` with `ecx = 0xF` (`00360A31`/`00360A36`) | [`00360A36`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `00229EB0`, `00360D60`, `002F1A30`,
`00360A50`, `003601C0`, `002DE350`. The `022CB9B0`/`022CB9B8` cells are
the shared counters; `00360A50` touches the `022CB730` base.

## The `00360710` exclusive subtree — all 2 members bound (SWE2-FRONTIER, followup queue)

`00360710` ~~(64 B) — an 8-byte-element range bound~~ (360 B, `ret` at `00360710+0x167`) *(corrected 2026-10-02, OPUS: measured)* — a 16-byte-entry index: `rsi =
movsxd(edx)` count, `r14 = movsxd(ecx)` start, `edx == 0` → return 0
(`00360728`); else ~~`rdi = r14 + rsi*8` over the `022CB730` array~~ `rdi = 022CB730 + (r14 + rsi*8) × 16`, a 16-byte entry *(corrected 2026-10-02, OPUS: `00360710+0x3B` `lea rdi, [r14+rsi*8]`, `+0x41` `shl rdi, 4`, `+0x45` `add rdi, rax`)*
(`00360744`/`0036074B`).

| member | role | interior |
| --- | --- | --- |
| `002273E0` (53 B) | gated init — `01FD46D4` bit `0x8000000` gate (`002273E4`), `-1` writes (`002273F2`/`002273FD`), `00226BE0` (`0022740B`), second `0x40000` gate (`00227424`) | [`002273E4`](../../_index/ADDRESS-INDEX.md) |
| `002DEDD0` (11 B) | count thunk — `ecx = dword[0215EF44]`, tail `001DBC30` (`002DEDD0`/`002DEDD6`) | [`002DEDD6`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `00226BE0`, `001DBC30`. The
`022CB730` array is the shared element bank `00360A50` also walks;
`01FD46D4` and `0215EF44` are the shared flag/count cells.

## The `002E5180` exclusive subtree — all 2 members bound (SWE2-FRONTIER, followup queue)

`002E5180` (506 B) — an actor-state update: `byte[rcx+0x18] == 1` → out
(`002E5197`), `003590D0` (`002E51AC`), `[rbx+0xC0]` payload →
`and byte[rax+0x151], 0xFB` clears bit 2 (`002E51BD`), `ecx = -1` →
`00264010` (`002E51C7`).

| member | role | interior |
| --- | --- | --- |
| `002E8000` (78 B) | record probe — `[rcx+0xC0]` null-gate (`002E8005`), `dword[rax] == -1` / `cx == -1` (`002E8011`/`002E8019`), float `00D0F8E0` (`002E801F`), `rcx += [022C6F28]` then `dword[rcx+0x284]` (`002E8033`/`002E803C`) | [`002E803C`](../../_index/ADDRESS-INDEX.md) |
| `003DADE0` (18 B) | safe float getter — `rcx` null-gate → `xmm0 = [rcx+0xAC]` else `xorps` (`003DADE0`–`003DADF1`) | [`003DADE5`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `003590D0`, `00264010`. The
`022C6F28` cell is the shared attach-record table the field-map pages
already document.

## The `003DAC70` exclusive subtree — all 2 members bound (SWE2-FRONTIER, followup queue)

`003DAC70` (131 B) — a record-bank walk over the `02B4E4C0` table:
`word[02B57CC0]` index (`003DAC76`), per-element `003DAAB0`
(`003DACB8`) and `003DAB50` (`003DACD3`), the index written back at
`003DAD3C`; a second loop walks `word[02B57CC4]` (`003DAD93`,
write-back `003DADD8`).

| member | role | interior |
| --- | --- | --- |
| `003DAAB0` (155 B) | pair-write helper — `r9` → `02B57EE0`/`02B57EE8` (`003DAAB3`/`003DAABA`), `movdqu` copy of the `02B57EE0` record (`003DAAC5`/`003DAAED`), `test cl, 1` (`003DAAD4`) | [`003DAAC5`](../../_index/ADDRESS-INDEX.md) |
| `003DAB50` (283 B) | table-walk helper — `02B4E4C0`/`02B57EE0` record bases (`003DAB6C`/`003DAB76`), `(rcx, rdx, r9)` | [`003DAB76`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none beyond the members — the bank
cells `02B57CC0`/`02B57CC4`/`02B57EE0`/`02B57EE8` are the shared
record indices.

## The `00473680` exclusive subtree — all 2 members bound (SWE2-FRONTIER, followup queue)

`00473680` (5 B) — `jmp 0026FA80` thunk. `0026FA80` (~80 B) gates on
`byte[02F8F238]` (`0026FA99`) and, when set, builds the 3-byte message
`{2, cx}` on the stack (`0026FAA2`–`0026FAAC`) and delivers it through
`0024E7D0` (`0026FAB1`).

`0024E7D0` (318 B) — the per-type record recycler/dispatcher: the record's
`byte[0]` selects the list head `qword[020910A0 + type*8 + 0x50]`
(`0024E7F3`/`0024E7FA`), the walk matches `word[+6]` (`0024E820`/
`0024E82B`), and on match the node is unlinked through its `+0x348`/`+0x350`
prev/next pair (`0024E835`–`0024E862`). The detached record is published
to `02F97348`/`02EBEF98` and the `003A81E0`/`003A72E0`/`003A8D70` results
to `02EBEFB0`/`02EBEF88` (`0024E870`–`0024E8A4`); `[rbx+0x380]` is then
inserted into the `020910A0+0x8B0` free list indexed by `word[0209216A]`
against the `0x100` cap (`0024E8B5`/`0024E8CC`), and `00182CA0`/`003697F0`
close out (`0024E8C2`/`0024E8DE`).

| member | role | interior |
| --- | --- | --- |
| `0026FA80` (78 B) | gated notify — `byte[02F8F238]` set → `0024E7D0({2, cx})` | [`0026FAB1`](../../_index/ADDRESS-INDEX.md) |
| `0024E7D0` (318 B) | record recycler — type-indexed list walk, unlink, free-list insert | [`0024E835`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `003A81E0`, `003A72E0`, `003A8D70`,
`00182CA0`, `003697F0`, `00808C40`.

## The `002350C0` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`002350C0` (`SpawnLifecycle_CheckAndRetireByNativeRange`, ~600 B) — the
range retire that sets flag-word bit 0 (`002352A6`, per the flag table);
member `002672F0` supplies the bit-6/7 input to the fresh test.

| member | role | interior |
| --- | --- | --- |
| `002672F0` (11 B) | `(byte[rcx+0xD] >> 6) & 1` getter (`002672F0`/`002672F7`) | [`002672F0`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none beyond the retire walk.

## The `00236300` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`00236300` (`BattleUnit_SnapshotWorldActorRuntimeState`) — copies
`byte[+0xEA9]` to `byte[+0x1F7]` (`0023630A`/`00236314`), then
`00263CC0([rcx+0x10])` into `float[+0x15C]` (`00236323`/`00236328`).

| member | role | interior |
| --- | --- | --- |
| `00263C80` (50 B) | kind-dispatched float getter — `(byte[+3] >> 5) - 1`: 0 → `[[rcx+0xB8]+0xA0]`, 1 → second arm, else `xorps` (`00263C84`/`00263C95`) | [`00263C95`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `00263CC0`.

## The `0023A070`/`00265A20` exclusive-subtree pair — both roots bound (SWE2-FRONTIER, followup queue)

`0023A070` (`BattleUnit_ApplyMovementIntentToWorldActor`, ~97 B) —
gates on `dword[02089340] & 0x600`, non-null `rcx` and `qword[+0x698]`,
`byte[+5]` (`0023A076`–`0023A09A`), then applies through the member.

| member | role | interior |
| --- | --- | --- |
| `0026A060` (97 B) | kind-dispatched angle apply — `(byte[+3] & 0xE0) == 0x60` → `[[rcx+0xB8]+0xA0]`; sign of `xmm1` picks `+π` (`0x40490FDB`) or `−π` (`0xC0490FDB`) (`0026A067`/`0026A084`) | [`0026A067`](../../_index/ADDRESS-INDEX.md) |

`00265A20` (`ActorSystem_BindBattleUnitsForEligibleRecords`~~, ~200 B~~, 320 B) *(corrected 2026-10-02, OPUS: `ret` at `00265A20+0x13F`)* —
loops `dword[rcx+0x20]` slots (`00265A2C`/`00265A3C`), binding eligible
records through the member.

| member | role | interior |
| --- | --- | --- |
| `00234A00` (4 B) | `dword[rcx+0x20] = edx` setter | [`00234A00`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none beyond the walk.

## The `0025B740` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`0025B740` (~140 B) — `003590D0()` index → `003588B0(eax)` record →
null-gated body (`0025B746`/`0025B74D`).

| member | role | interior |
| --- | --- | --- |
| `00238B20` (29 B) | `02089340` bit-13 toggle — `btr eax, 0xD`; `neg/sbb` on `ecx` selects `edx & 0x2000`; `or`, store (`00238B26`/`00238B36`) | [`00238B2A`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `003590D0`, `003588B0`.

## The `002E0D90` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`002E0D90` (5 B) — `jmp 00253C50` thunk.

| member | role | interior |
| --- | --- | --- |
| `00253C50` (26 B) | paired call — `00253C70()` into `ebx`, then `003C9550()`, returns `ebx` (`00253C56`/`00253C5D`) | [`00253C56`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `00253C70`, `003C9550`.

## The `0022BC20`/`00234520`/`002EF910` exclusive-subtree triple — all 3 roots bound (SWE2-FRONTIER, followup queue)

`0022BC20` ~~(~80 B)~~ (463 B, through the tick call at `0022BC20+0xA8`) *(corrected 2026-10-02, OPUS: measured)* — `0016D6A0(3)`, `0017F740(0)`, `0036F2F0`, then a
`"PAD CONTROL"` tagged block (`0022BC29`/`0022BC3A`).

| member | role | interior |
| --- | --- | --- |
| `00375EC0` | `02EBF9F0`/`02EC07F0` clear twin — `and dword[rax], 0xFFFFFFFE` under the same `+0x58` gate (`00375ED0`/`00375ED6`) | [`00375ED0`](../../_index/ADDRESS-INDEX.md) |

`00234520` ~~(~220 B)~~ (109 B, `ret` at `00234520+0x6C`) *(corrected 2026-10-02, OPUS: measured)* — 64-aligned stack frame; `ecx == 0` runs
`0023B040` (`00234531`/`00234533`).

| member | role | interior |
| --- | --- | --- |
| `00313CD0` | `byte[02089340] & 0x20` gate, else `022BE984` walk (`00313CD4`/`00313CEB`) | [`00313CD4`](../../_index/ADDRESS-INDEX.md) |

`002EF910` (~21 B) — thin forward under a six-register save.

| member | role | interior |
| --- | --- | --- |
| `001D6C80` | `001DADA0()` resolve then tail `001DA290` (`001D6C84`/`001D6C90`) | [`001D6C84`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `0016D6A0`, `0017F740`, `0036F2F0`,
`0023B040`, `001DADA0`, `001DA290`.

## The `00304440`/`00307D10` exclusive-subtree pair — both roots bound (SWE2-FRONTIER, followup queue)

`00304440` ~~(~27 B)~~ (345 B, `ret` at `00304440+0x158`) *(corrected 2026-10-02, OPUS: measured)* — `byte[02EBF190 + 0x5AE0] & 1` gate, then
`0017D380()` (`0030444B`/`00304458`).

| member | role | interior |
| --- | --- | --- |
| `0017D380` | `001D50D0()` → `byte[rax+0xE1D] != 0` bool getter — `0017D3A0`'s twin (`0017D384`/`0017D38B`) | [`0017D38B`](../../_index/ADDRESS-INDEX.md) |

`00307D10` (`BattleUnit_UpdateEngagementStateFlag`, ~129 B) —
`qword[+0x698]` non-null gate (`00307D1D`/`00307D24`).

| member | role | interior |
| --- | --- | --- |
| `0030BF20` | `01EEC320` byte + `00120000` base — function-table index prologue (`0030BF25`/`0030BF2D`) | [`0030BF25`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `001D50D0`.

## The `00313760` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`00313760` (~27 B) — `byte[02EBF190 + 0x5AD0] & 2` gate, then
`0017D3C0()` (`0031376B`/`00313774`).

| member | role | interior |
| --- | --- | --- |
| `0017D3C0` | `001D50D0()` then `byte[rax+0xE1C] != 0` bool getter — third of the `+0xE1x` triple (`0017D3C4`/`0017D3CB`) | [`0017D3CB`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `001D50D0`.

## The `00360A50` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`00360A50` (~170 B) — six-register frame body (`00360A50`/`00360A66`).

| member | role | interior |
| --- | --- | --- |
| `003E3B80` | `qword[022C6F28]` base, `dword[+0x48800] == -1` sentinel gate (`003E3B84`/`003E3B94`) | [`003E3B84`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none.

## Interior citations — frontier leaf hubs (2026-09-17, SWE2-EC7)

Three leaf helpers the tick's callers share, read against the shipping image:

- `00203080` — 81 B, 44 frontier callers (Audio-tagged census domain). Interior verified:
  [`00203088`](../../_index/ADDRESS-INDEX.md) is `subss xmm0, [r8]` — a plain `vec4` subtract:
  `*rcx = *rdx - *r8` element-wise through a stack temp. A math leaf; the audio concentration is
  caller domain, not ownership.
- `00202C70` — 31 B, 38 frontier callers (same caller band). Interior verified:
  [`00202C73`](../../_index/ADDRESS-INDEX.md) is the first `movups` store — a 64-byte
  (`4×vec4`) copy `rdx → rcx`; the sibling of `00202C90`'s 16-byte copy.
- `001EDDA0` — 27 B, 38 frontier callers. Interior verified: [`001EDDA9`](../../_index/ADDRESS-INDEX.md)
  is the second global compare — the body is a two-global enable predicate returning 1 iff
  ~~`dword[01FCE0C0] != 0` **or** `dword[0209DE38] == 0`~~ `dword[01DFE0C0] != 0` **or** `dword[01F82E38] == 0` *(corrected 2026-10-02, OPUS: `001EDDA0+0x0` `cmp [01DFE0C0], 0`, `+0x9` `cmp [01F82E38], 0`)*; equivalently it returns 0 only when the
  first flag is clear while the second is set. Callers treat it as "is the field frame's auxiliary
  path live".

NOT claimed: which subsystem owns either global (both sit in shared `.data`; the scheduling tag
is census-derived, not owner evidence).

## Interior citation — frontier hubs `00226280`, `003ABCA0` (2026-09-18, SWE2-EC7)

`00226280` — 952 B, 9 A-measured callers; the table scan this page already places next to
`00226BE0`. Interior verified: gated on byte `01FD46D0` (`00226287`); the loop at
[`002262E4`](../../_index/ADDRESS-INDEX.md) walks ~~a packed table~~ the 28 `0x18`-byte stop records rooted at `01FD4410` ~~with `ebp = 0x3FF` as the~~
~~element mask and `0x20000000000` as a validity bit~~ (ANDing record A's first qword into `rdi` and record B's into `rbx`, and setting bit 41, `0x20000000000`, in record B), tracking the minimum slot dword in `ecx`
(`cmp ecx,edx` / `cmov` shape at `002262F4`–`00226301`) — ~~a best-fit/free-slot search over a~~ an AND over all 28 slots
~~1024-entry index space, not a linear lookup.~~ *(corrected 2026-10-02, OPUS: `00226280+0x57` `lea rax, [01FD4410]`, `+0x64`/`+0x6B` the two ANDs, `+0x8E`–`+0x95` stride `0x18` up to `01FD46B0`; `ebp = 0x3FF` seeds the mask built after the loop; CONTRACT-system-stop-registry.md SS-1)*

`003ABCA0` — 94 B, 8 callers; the intrusive-list remove-by-key the parent-init runs ×6.
Interior verified: the list head is `02B3F508`, tail pointer `02B3F510`, node count byte
`02B3F500`. The scan at `003ABCB0` compares `[node]` against `ecx` and walks `+0x10` links;
on a hit it decrements the count ([`003ABCBE`](../../_index/ADDRESS-INDEX.md)), clears `[node]`, and splices
`prev(+0x08)`/`next(+0x10)` at `003ABCD7`–`003ABCF5`, updating head/tail when the edge node
is removed.

## Interior citation — frontier hubs `00263660`, `0032E520` (2026-09-18, SWE2-EC7)

`00263660` — 133 B, 7 A-measured callers; the mode dispatcher that drives `00226280`'s scan.
Interior verified: `00265680()` answers the mode flag (`bl`), published to the `02099DE0`
byte at `00263674`; when `[02098E20]` bit 0 is set and the `02098E21` byte's bits 0/7 are
both clear it runs `00226260()` or `00227640()` by `bl`, then `00226280()` at
[`002636A2`](../../_index/ADDRESS-INDEX.md). The tail is symmetric: `bl` set runs `002E1CD0(1, 6)` +
`002E23D0(1)` + `jmp 002EF350(1)`; clear runs `002E1CD0(0, 6)` + `jmp 002E23D0(0)` — flag
set/clear on slot 6 vs 0 through the `0215F1C0` table.

`0032E520` — 107 B, 7 callers; the drain/status pair to `0032E040`'s kick. Interior
verified: `ecx == 0` loops `0032E070(0)` at [`0032E563`](../../_index/ADDRESS-INDEX.md), re-polls ~~`[020C51C0]`~~ `[022C51C0]` *(corrected 2026-10-02, OPUS: `0032E520+0x48` `cmp qword [022C51C0], 0`)* and
`0046DFE0()`, and re-invokes `0035EA30(0)` while either is still busy — the blocking drain.
`ecx != 0` is the non-blocking status read: returns ~~`([020C51C0] != 0) | !0046DFE0()`~~ `([022C51C0] != 0) or !0046DFE0()` *(corrected 2026-10-02, OPUS: `0032E520+0x16` reads `022C51C0`)*.


## Interior citation — frontier hubs `00263C30`, `002EFD20`, `00263BE0` (2026-09-18, SWE2-EC7)

`00263C30` — 32 B, 6 A-measured callers; the flag-gated dword fetch off the `0x288`-stride
record table at `02098E10`. Interior verified: `movsxd` index, `imul rcx, rax, 0x288`
([`00263C33`](../../_index/ADDRESS-INDEX.md)), `byte [rec+0x10] & 1` gates `dword [rec+0x20]`,
else 0 (`00263C41`–`00263C4F`).

`002EFD20` — 40 B, 6 A-measured callers; the mode→byte clamp lookup. Interior verified:
`ecx` clamped to `[0, 6]` (`cmovg` at `002EFD2F`), then `byte [022BDD64 + ecx*24]` — a
24-byte-stride table's first lane — at [`002EFD43`](../../_index/ADDRESS-INDEX.md).

`00263BE0` — 50 B, 6 A-measured callers; the kind-nibble bucket map. Interior verified:
`byte [rcx+0xE] & 0xF` (`00263BE5`) maps `0→1`, `3→2`, `1|2|7→0` (`00263BF4`–`00263C0F`) —
the eligibility class this frame's dispatch consults before the tick.


## Interior citation — frontier hubs `0024B3A0`, `00182CA0`, `0024CFF0` (2026-09-18, SWE2-EC7)

`0024B3A0` — 321 B, 6 A-measured callers (`002FC4A0`, `003B2220` among this page's
dispatch/init bodies); the 0x890 state-record clone-and-register. Interior verified:
`0036A100(0x890)` allocates ([`0024B3C0`](../../_index/ADDRESS-INDEX.md)), a 17-iteration
`movups` loop copies the source verbatim (`0024B3D3`–`0024B426`), then the clone is pushed onto
the type-bucketed chain at `020910A0[byte[rdi] * 8]` with the `[+8]`/`+0x10` backlink fixup
(`0024B435`–`0024B457`), its interior rows `+0x18`/`+0x38`/`+0x840`/`+0x848`/`+0x850` are
published to the `02EC5xxx`/`02F92Fxx` globals, and five sub-initialisers
(`003A9CC0`/`003A76F0`/`003A7D00`/`003A9560`/`003A9920`) wire the copied state live.

`00182CA0` — 45 B, 5 A-measured callers; the `001B6C40`-guarded tail into `001B68D0`.
Interior verified: `001B6C40()` supplies the shared object, non-null required
(`00182CAD`–`00182CB5`), then `001B68D0(obj, rcx)` runs at
[`00182CC2`](../../_index/ADDRESS-INDEX.md). Same adapter shape as `001EB150`/`0017F370`.

`0024CFF0` — 58 B, 5 A-measured callers; the high-nibble class dispatch. Interior verified:
`(ecx >> 28) & 0xF` minus one indexes a 9-entry rel32 jump table at `0024D008`
([`0024D013`](../../_index/ADDRESS-INDEX.md) `jmp rdx`), landing on tails `002FC340`,
`003B0770`, `00375470`, `003B1700` (and five more entries); values outside 1..9 return without
acting. The tag nibble selects which subsystem step runs.


## Interior citation — frontier hub `001243B0` (2026-09-18, SWE2-EC7)

`001243B0` — 3 B, 59 callers; another `ret 0` folded leaf, same idiom as `0016D6A0`.
Interior verified at [`001243B2`](../../_index/ADDRESS-INDEX.md): `c2 00 00` — a no-op
callback site in the shipped image.


## Interior citation — frontier hub `003601B0` (2026-09-18, SWE2-EC7)

`003601B0` — 14 B, 20 callers; the `022CB720` bit-set publish. Interior verified:
`eax = 1 << cl` then `or [022CB720], eax` at
[`003601B5`/`003601B7`](../../_index/ADDRESS-INDEX.md) — a one-hot flag OR'd into the shared
mask; the world's "this lane ran" bookkeeping.

## Interior citation — frontier hub `0033D3E0` (2026-09-18, SWE2-EC7)

`0033D3E0` — 631 B, 11 callers; `Navigation_CheckDirectRouteAcrossRooms` confirmed in full.
`00384130` maps each endpoint's X/Z pair to a grid cell (0xFF = off-map: returns 0 for the
source, 1 for the target), then a bounded walk (`r13d < 0x80` iterations, `0033D605`) steps
the `[rbp+0xA]`-count column index from the source cell toward the target. Each step rebases
through `0020E600` twice — the `[rbp+0x1C]` table gives the `word [rax+rcx*2]` edge id, the
`[rbp+0x14]` table the per-edge bytes whose `+5` predicate (`0032A780`) or `+6` direction
mask (`(1<<r15b) & byte`) decides whether the crossing is allowed — then loads the edge's
endpoint vectors out of the `[rbp+0xC]` table and calls `00468880` for the segment test
([`0033D5D2`](../../_index/ADDRESS-INDEX.md)); a hit swaps the walk's current cell to the far
side (`0033D5EB`). Exhaustion or equality with the target cell returns 0/1. This is the
"can the foe walk straight there" predicate the field frame's steering consults.

## Interior citation — frontier hub `002E4A40` (2026-09-18, SWE2-EC7)

`002E4A40` — 382 B, 7 callers; the position-push behind `0037CF00`'s four-slot clear pass
(`002E49B0(obj,0)` + this, §619 row). Gates: `00377DB0` non-zero, the `[rcx+0xC0]` record
present and its `[+0]` word not `-1`, and `[rbx+0xC0]` non-null (`002E4A7B`–`002E4A8B`).
`00265970` resolves the source record; flag `0x20` at `[rdx+0x151]` substitutes the constant
float triple at `01CEBBA8` for the source's `[+0x20..28]` vec3, and flag `0x10` skips the
`002ED6A0` call on `[rdx+0x138]`. Then `002EDD70(handle, vec3)` is issued to each of the
record's `+0x30`, `+0x60`, `+0x90` handle slots and the caller's `[rsi]` word, each skipped
when its `dword` is `-1` ([`002E4B44`](../../_index/ADDRESS-INDEX.md) and `002E4B53`/`002E4B79`/
`002E4B8D`). The same write an actor's position broadcast makes to its four render-side
sub-records.


### Interior citation — frontier hubs `003DF760`, `003098D0` (2026-09-18, SWE2-EC7)

`003DF760` — 48 B, 6 callers. An indexed registry-slot setter: index `edx`
selects parallel arrays — ~~`qword[0x2A39C40 + i*8] = r9`,~~ `qword[02B59C40 + i*8] = r9`,
~~`qword[0x2A39C80 + i*8] = stack arg`, `dword[0x2A39CC0 + i*4] = r8d`,~~ `qword[02B59C80 + i*8] = stack arg`, `dword[02B59CC0 + i*4] = r8d`,
~~`dword[0x2A39CE0 + i*4] = ecx`~~ `dword[02B59CE0 + i*4] = ecx` *(corrected 2026-10-02, OPUS: the displacements are image-base relative, `003DF760+0x8` `lea rdx, [00120000]`)* ([`003DF76F`](../../_index/ADDRESS-INDEX.md)).
Four field stores, no validation, returns void.

`003098D0` — 182 B, 5 callers, `BattleAction_SelectGlobalSequenceP…`. Bit 31 of
`[rcx]` short-circuits to `0x203D`. Otherwise `ecx = [table+0xC]` is resolved
through `ImageAddress_ResolveRuntimePointer` (`0020E600`), the `r9d - eax`
difference is divided by `word[rec+8]` ([`0030992B`](../../_index/ADDRESS-INDEX.md)),
and the quotient is range-tested — `(ax - 0xD0) <= 0x21` takes the record's own
`[+0x30]` when nonzero, while `ax >= 0xE2` or the `dword[022C2160] - 5 <= 1` gate
selects `[rdi*3+8]` from the `01EEC1F0` triple-table. The sequence-picker the
action layer consults.

### Interior citation — frontier hub `00267330` (2026-09-18, SWE2-EC7)

`00267330` — 39 B, 8 callers: the `02098E10` record's two-bit decode.
`ecx * 0x288` strides the record array; `byte[+0x10] & 1` gates — when set the
answer is `byte >> 7` at [`0026734D`](../../_index/ADDRESS-INDEX.md), when
clear it returns the constant 1. A flag-valid bit-7 field read the frame
consumers poll.

### Interior citation — frontier hubs `003A81E0`, `00312700` (2026-09-18, SWE2-EC7)

`003A81E0` — 85 B, 7 callers: the shared callee the census keeps outside.
Walks the `+0xF0` next-chain under `[02EBEF98]`, invoking `003697F0` per node
at [`003A8207`](../../_index/ADDRESS-INDEX.md) — a per-node callback drain the
frame's tail runs.

`00312700` — 35 B, 6 callers: the bit-1 arm's tail — `003125E0(rbx)` first,
`edx = (eax == 0)`, then `jmp 0026DC60` on `[rbx+0x10]` at
[`00312709`](../../_index/ADDRESS-INDEX.md). The two-step the dispatch table
reserves.
## SWE2-EC7-18 update (2026-05-15) — `002EF350`/`003137F0`/`0036D890` per-frame fragments

`002EF350` (17 B) is the set-side tail this page describes (`002E23D0(1)` + `jmp 002EF350(1)` — the flag writer behind the clear twin `002E1CD0`): `test edx,edx` + `mov eax,2` + `cmovs edx,eax` (`002EF352`..`002EF357` — a negative `edx` is floored to `2`), then `ecx=edx` and `jmp 00229EC0` (`002EF35C`) — the normalized-value forward into the shared flag writer, not an independent entry.

`003137F0` (15 B) is the registry-slot reader row 20 names (`02EBF190` record byte `+0x5AD5` → `BattleUnit_FindByCombatantId`): `rax=[02EBF190]` (`003137F0`), `movzx eax, byte[rax+0x5AD5]` (`003137F7`), `ret` — a three-instruction byte getter over the registry record, exactly the masked-byte source the row's `003135C0` branch consumes.

`0036D890` (23 B) is the three-call chain the `0022xxxx` per-frame callers (`0022A770`/`0022B6E0`/`0022B8C0`/`0022BC20`) and `0036EEB0` reach: calls `00360B50` (`0036D894`) and `003A0EA0` (`0036D899`), then tails `0016D6A0` (`0036D8A2`) — a resolve-then-publish sequence the tick runs before tailing into the shared `0016D6A0` continuation.

## SWE2-EC7-19 update (2026-05-15) — `0035B1A0` slot-table acquire + `00306570` singleton release

`0035B1A0` (158 B) is the `02EC0B80`-table slot acquire the page lists (`0035B5D0` calls it ×2): `r9d = cl-1` selects the `0x20`-stride row (`r8 = table + (cl-1)*0x20`, `0035B1AB`..`0035B1B8`); `word[r8+2]` must equal `ecx>>8` or it returns (`0035B1C0`); on a hit it updates the `02EC0B60`/`02EC0B61` byte cursors — chasing the `02EC0B61` chain of row-lead bytes until it finds one keyed `r9d` (`0035B1C4`..`0035B20A`) — then `word[r8+2]++`, `[r8]=byte[02EC0B60]`, `[r8+1]=0`, `[r8+8]=0`, `byte[02EC0B60]=r9b` (`0035B21A`..`0035B236`) — the register-and-advance the listener/scene-cell records run per claim.

`00306570` (87 B) is the `022C2168` singleton release this page's step-11 registration names: `rcx` non-null and unequal to `[022C2168]` returns early (`00306585`), else `002671F0(3)` (`0030658F`) gates — a nonzero result exits; on the quiet path it clears `022C2158`'s low two bits, zeroes `022C215C` and `022C2168` (`00306598`..`003065A8`), runs `00238A60` (`003065AF`), and tails `00332190(3)` (`003065BD`) — the teardown arm the unit-side pair shares.

## SWE2-EC7-20 update (2026-09-18) — `0079E6A0` device-probe arm + `0046DFE0` status-read fragment

`0079E6A0` (44 B) is the bank-indexed control-code activity read the input backend
gates on (`InputBackend_IsControlCode28To283ActiveForBank`): `r8d` is bound-checked
below 7 (the bank index), `rcx = [rcx + r8*8 + 0x118]` selects the bank's record
pointer, `edx - 0x1C` must stay under `0x100` (control codes 28–283), and
`al = byte[rcx + rax + 0x30] != 0` returns the active flag — the `0017DE10` arm's
probe this page names. Interior anchor `0079E6A9` (the `+0x118` bank-table load).
Seven callers — `0017DDC0`/`0017DE10`/`0017DEA0`/`0017DFC0`/`00197160`/
`00197990`/`001E0E70` — the tick-arm device probes.

`0046DFE0` (18 B) is the non-blocking status read the drain loop polls — a
five-instruction select: `eax = 0`, `ecx = 2`, `cmp dword[0215EFF4], -1`,
`cmove eax, ecx`, `ret`. It returns 2 while the `0215EFF4` status word sits at `-1`
(the pending sentinel), else 0 — the value `0032E070(0)` reads on the non-blocking
path. Interior anchor `0046DFE7` (the `-1` status compare). Three callers:
`0032E070`/`0032E520`/`0032E870` — the non-blocking read path this page's state
table names.

## SWE2-EC7-21 update (2026-09-18) — `001C50C0` stream-feed arm + `004FE3C0`/`00427280`/`0042FB80` fragments

`001C50C0` (73 B) is a record constructor the tick's copy loops share: `rcx`'s
`+0x00`/`+0x08`/`+0x10` qwords are zeroed, `001EDF00` initializes `&rcx+0x18` from
the `01F832E0` static record, then `001A4BF0` publishes the object against the
`01F832C8`/`01F832D0` global pair and returns `rbx`. Interior anchor `001C50EA`
(the `01F832D0` global fetch). Six callers — `0028F2F0`/`0028F8B0`/
`0028FA70`/`0028FAF0`/`003A1D50`/`00465F60` — the copy-side callers this page's
frame path drives.

`004FE3C0` (14 B) is the three-qword record clear: `rax = 0`, then `[rcx]` /
`[rcx+8]` / `[rcx+0x10]` are zeroed and the body returns — the reset half of the
`001C50C0` constructor's field layout. Interior anchor `004FE3C2` (the `[rcx]`
store).

`00427280` (25 B) is the `+0x294` flag rewrite the secondary-context writers share:
`eax = [rcx+0x294]`, `& 0xFFFDFA5F` drops the `0x205A0` bits, `| 4` re-arms bit 2,
the word goes back to `+0x294`, then `jmp 00422C20` rejoins the shared tail.
Interior anchor `00427286` (the mask `and`). Callers `002E28E0`/`002E42D0`/`002E4330`/
`002E6BD0` — the secondary-context writers.

`0042FB80` (291 B) is the `"makeid"`-keyed word-id resolver: the six-byte
`"makeid"` constant is staged on the stack, `003AB7F0` resolves the context object
and `00409090` walks the `01EFF940` chain for the key — on a hit its `0x20`-byte
record is copied, then `[022C6F28]`'s `+0x4880C` count must stay below `0xA0`
before `byte[+0x48808]` is appended to the key string and `004279B0` is called on
the `{key, record, edx, r8d}` set; the result is `movsx eax, word[rax]` or `-1`
on any failed step. Interior anchor `0042FB9F` (the `"makeid"` head load).
Callers `002E28E0`/`002E42D0`/`002E4330`/`002E6BD0` zone.

## SWE2-EC7-22 update (2026-09-18) — `00265830` kind-0x60 guarded accessor

`00265830` (34 B) is the guarded accessor the tick's object scans call:
`byte[rcx+3] & 0xE0 == 0x60` (the top-three-bit kind lane) else `xorps; ret`;
on match, `[rcx+0xB8]` object fetch. Interior anchor `00265834` (the mask).
Callers route the tick's secondary-context and locomotion passes through it.

## SWE2-EC7-23 update (2026-09-18) — `003B7730` ready predicate + `003B0770` record find

`003B7730` (27 B) is the two-global ready predicate the tick's gates consult:
`[02B40530] != 0 && [02B40534] != 0` -> 1, else 0 — the paired-init check the
frame path runs before touching the subsystem. Interior anchor `003B7739`.

`003B0770` (172 B) is the keyed record find over `[02EBEC00..02EBEF60)`:
`0036C1D0(8)` context call, then a `0x18`-stride scan matching `[rcx] == esi`
— the bounded lookup the tick's per-record passes share. Interior anchor
`003B07A2` (the key compare loop head).

## SWE2-EC7-24 update (2026-09-18) — seven more shared arms

`00384130` (40 B) forwards a `{float, float}` pair — `[rcx]`/`[rcx+8]` staged
into a stack record — into `00383F10`. Interior anchor `0038414E`.

`0036DE70` (179 B) sweeps the `022D94B0` 24-byte-stride table with `ebx`
clamped to `min(ebx, ebx+0x1F)`: on `byte[+8] == cl` and `word[+4] & 0xFFFB`
set, it stores ~~`bx+4`~~ the constant 4 *(corrected 2026-10-02, OPUS: `r15d = ebx + 4` is computed once at `0036DE70+0x32`, before the loop, while `ebx` is 0; `0036DE70+0x78` `mov word [rdi+4], r15w`)* into `word[+4]` then runs `003B24C0`/`003B1700` on the
entry's head dword. Interior anchor `0036DEBB` (the `movsx`).

`003669D0` (27 B) classifies `word[022CBE1A]`: `&1` clear returns 0, `&4`
returns `setne + 1` — the two-or-three-way mode byte the frame reads.
Interior anchor `003669D7`.

`00374FD0` (277 B) is the `02EBF9E0` 0x70-stride walker the `0022xxxx`
application trio calls: skips empty `+0x68` heads and flagged `[+0x10]&1`
entries, then dispatches on `byte[0]-1` (max 0xC) through the `0x2550E8` jump
table — each arm tests `+0x1C`/`+0x1D`/`+0x1E`/`+0x1F` flags before running.
Interior anchor `00375010` (the `imul 0x70`).

`003636A0` (136 B) dedupe-scans the `021ABB44` dword table: outer `edi` over
`[022CBB50]` rows, inner `eax` over `[022CBB70]`-bounded `021ABB64` slots, and
only calls `002DF050` when no earlier slot already holds the value.
Interior anchor `003636D0` (the row fetch).

`003601C0` (16 B) clears bit `cl` of `dword[022CB720]` (`~(1<<cl)` mask).
Interior anchor `003601C9`.

`0035A240` (10 B) resets `word[022C8010]` to zero — the `00266D10`/`002695A0`
callers run it on their init paths. Interior anchor `0035A242`.

## SWE2-EC7-25 update (2026-09-18) — five more shared arms

`003DE0A0` (112 B) tears down the four `02B58A80` 0x68-stride records:
`0024CFF0`-releases each non-null head and zeroes the slot. Interior anchor
`003DE0E5` (the release call).

`00375470` (135 B) removes a record from the `02EBF9E0` 0x70-stride table by
head-dword `ecx`: finds the slot between `02EBFA48` and `02EC0848`, then
`rep movsq` shifts the tail down over it and clears `02EC07D8`. Interior
anchor `00375490` (the scan loop head).

`00368AC0` (9 B) stores `~cl` into `byte[02EC0B38]` — the complement-write
half of the flag byte batch-24's `00368A50` family publishes. Interior
anchor `00368AC2` (the store).

`003323B0` (19 B) forwards `[022C6F20] + 0xD98` into `0046E1B0` — the deep
slot of the shared object handed to the callee. Interior anchor `003323B7`.

`00324510` (417 B) is the `022C2678` message-buffer state machine the
`0022xxxx` application trio drives: `022C27A0` state 1 publishes the
`003244F0` handler into `022C2690`/`022C2688` and arms the `0x12D`-count /
`+0x4BC` buffer pair (`022C3148`, `022C3150`) before promoting to state 2;
state 2 reads the `022C27A8` cursor; state 3 releases `022C27B0` through
`003697F0` and clears all three globals. Interior anchor `00324543` (the
release call).

## SWE2-EC7-26 update (2026-09-18) — `00314DF0` three-global arm/clear

`00314DF0` (21 B) — reached through `00266D10`/`002695A0`/`0026CE60` —
writes `dword[022C2538] = ecx` and zeroes `byte[022C253C]`/
`byte[022C253D]` — the three-global state arm the tick-path callers
run. Interior anchor `00314DF6` (the first clear).

## SWE2-EC7-27 update (2026-09-18) — `002F1A30` / `002F1710` / `002DF150` channel helpers

`002F1A30` (58 B) is the `002F1A30(1)` wait the states 1-3 sequence and
the fade scheduler issue: walks the `022BE7C0` bitmask, and for each set
bit compares the matching `022BDEDE` record's `word[+0]` (0x48 stride)
against the argument — true on any match. Interior anchor `002F1A48`
(the `bt`).

`002F1710` (87 B) — reached through `00253C70`/`002628B0` — is the
complement release: pulls `dword[022BE7D0 + 4]` into `[rbx]`, builds
`1 << [rbx+0x18]`, fires the optional `[rbx+8]` callback, stamps
`word[+0x1C] = 1`, and ANDs the bit out of `022BE7C0` — the channel
release behind the mask query. Interior anchor `002F1756` (the mask
clear).

`002DF150` (17 B) forwards `(1, ecx, edx, 0)` into `001DBF00` — the
constant-first-arg call the tick path issues. Interior anchor `002DF15C`
(the tail jump).

## SWE2-EC7-29 update (2026-09-18) — `0032E040`/`002A2830` pump gate + ownership forward

`0032E040` (38 B) is the once-per-frame pump gate this page's `0032E520`
drain pairs with: `001EDE80()` or `0017D930()` non-zero forwards
`ecx = 0` into `0032E070` (the `022C51C0` loader state-machine pump);
both zero returns without touching it — the either-source test that
keeps the request pump off the tick when no loader is live. Interior
anchor `0032E05C` (the `jmp 0032E070` forward).

`002A2830` (47 B) is the ownership-gated forward the tick's `0209C4D0`
record table shares: null `rcx` fails closed;
`dword [0209C4D0 + sbyte[rcx+0x3B8]*8]` must equal `ecx` — the record
must still own the slot its `+0x3B8` index names — and
`dword [rcx+0x40]` must have bit `0x400` CLEAR to tail-jump `00245020`;
any failure returns without dispatch. Interior anchor `002A2858` (the
`je 00245020` gate).

## SWE2-EC7-30 update (2026-09-18) — `0027E9E0` `0209AC18` ensure+publish (via `0022A770`/`0022B8C0`/`0022BC20`)

`0027E9E0` (142 B) — reached through `0022A770`, `0022B8C0` and
`0022BC20` — is the `0209AC18` singleton ensure: while the slot is
null it allocates `00244F50(0xC0, 002878E0)`, publishes the object,
sets `0209AC50` and `0209AC14` to 1, initialises via
`00247570(obj, 0)`, then registers it into the `0208EA40` bank with
`00246AD0(bank, obj)` — stack-cookie protected throughout.
Interior anchor `0027EA1F` (the `call 00244F50` allocation).
## SWE2-EC7-31 update (2026-09-18) — `002548F0` row-8 bit writer

`002548F0` (74 B) is `002548F0(on)` as the row table describes:
`ecx != 0` picks `002E1C20`, else `002E1CA0` — the set and clear
halves of one bit writer — then runs it four times, always with
row id 8 in `ecx` and bit ids `8`, `9`, `0xB`, `6` in `edx` (the
last a tail `jmp`). Row 8's bits 6/8/9/11 go on or off together.
Interior anchor `00254937` (the `jmp rbx` fourth call).

## SWE2-EC7-34 update (2026-09-19) - `002878E0`

`002878E0` (824 B) is a bank-slot resolver - `001E0B90(9)` kind read, `+1`/`+6` id adjust, `0017E270`, then the `00289xxx` bank family (`00285F60`/`002891A0`/`00287C02`/`00289390`/`00289040`/`00288DB0`/`00288A60`). Interior anchor `00287900` (the `001E0B90` call).

## SWE2-EC7-35 update (2026-09-19) - `0037D4C0`

`0037D4C0` (808 B) is a field-frame record body - `02ADDA34`/`02ADE974`/`02EBF3C0`/`02EBF380` records, `00382B70`/`0037D970`/`00358320`/`002563F0`. Interior anchor `0037D4EC` (an `00808C40` call).

## SWE2-EC7-35 update (2026-09-19) - `004742A0`

`004742A0` (777 B) is a field-frame helper - `008F30E4`/`01DFE0B8`/`008F8D80`/`00915734`/`01CEBD80` rdata run, `00861F14`/`00861F02` libfn pairs plus `00380800`/`002DDCF0`. Interior anchor `004742E7` (an `00861F14` call).

## SWE2-EC7-35 update (2026-09-19) - `00391410`

`00391410` (758 B) is a battle-unit field body - `02AEE090`/`02AEE078`/`02AEE070` records, `00468E50`/`00468D50`/`003A1920`/`003912E0`/`00383840`/`0032A6E0`. Interior anchor `00391443` (an `00808C40` call).

## SWE2-EC7-35 update (2026-09-19) - `00256F60`

`00256F60` (714 B) is a field-frame record body - `02096508`/`02AEDEF0`/`02AEDDB0` state, `00358320`/`002EA6A0`/`00263EB0`/`00255CF0` pairs plus `003587C0`/`0026A3B0`. Interior anchor `00256F8E` (an `00808C40` call).

## SWE2-EC7-35 update (2026-09-19) - `00392740`

`00392740` (702 B) is a battle-unit sibling - `02AEE0A0`/`02AEE0BC`/`02AEE060`/`02AEE064` records, `00861EC0`/`00392200` triples plus `0032A6B0`/`00383840`/`00358940`/`0032A6E0`. Interior anchor `003927BB` (an `00861EC0` call).

## SWE2-EC7-36 update (2026-09-19) - `002FBA60`

`002FBA60` (618 B) is the element-type name getter - `jmp rcx` into ~90 parallel `lea rax, "TsElementType_*"`/`"NhElementType_*"` arms ending `"NONE TYPE NAME"`. Interior anchor `002FBA8A` (the `TsElementType_NONE` arm).

## SWE2-EC7-38 update (2026-09-19) - `00468880`

`00468880` (496 B) is a field-frame body - `01F44830`, `00203080` sextuple plus `00202E10` quadruple and `00808C40`. Interior anchor `0046893B` (an `00203080` call).

## SWE2-EC7-38 update (2026-09-19) - `003ECAC0`

`003ECAC0` (477 B) is a world-tick sibling - `01F44830`/`00D11C20`/`009088D8`, `00466140` pair plus `00466170`/`00808C40`. Interior anchor `003ECBA5` (a `00466140` call).

## SWE2-EC7-38 update (2026-09-19) - `00258B90`

`00258B90` (472 B) is a world-tick body - `02092628`/`02092631`/`02092632` fields, `0025A520` quadruple plus `001EDDA0`/`003D9150`. Interior anchor `00258BBE` (a `0025A520` call).

## SWE2-EC7-38 update (2026-09-19) - `003E8690`

`003E8690` (460 B) is a `003Exxxx` perception-update sibling - `01CEBC9C`/`01CEBBA8`/`003E82D0`, `003E8190` quadruple plus `00473500`/`004735D0`/`0037A270`/`0037B190`/`0037A1D0`. Interior anchor `003E86DF` (a `00473500` call).

## SWE2-EC7-39 update (2026-09-19) - `003DEE10`

`003DEE10` (432 B) is the `0x38`-stride streaming-slot drain the page names - `003697F0` quadruple frees plus `0032E520`/`0035EA30` pairs and `002DEE90`/`00379E30`/`003DEB30`/`002DF050`, over `02B59360`/`02B59C20`. Interior anchor `003DEE9F` (a `002DEE90` call).

## SWE2-EC7-39 update (2026-09-19) - `00255FF0`

`00255FF0` (422 B) is a world-tick body - `02096508`/`022C6F28`, `00263C30`/`003587C0`/`002EA6A0`/`00358320`/`00263EB0`/`00263E80`/`0026A3B0`. Interior anchor `00256028` (a `00263C30` call).

## SWE2-EC7-39 update (2026-09-19) - `002EEB20`

`002EEB20` (416 B) is the ring-roll helper `002EED80` runs twice - `01EEBAA8`/`01EEBAB0`/`0215FD58`/`0215FD78`/`02164210`/`0216421C`/`02164220`/`022C6F28`, `0042F250`/`002EAEB0` pairs plus `002ED470`/`002E99C0`/`003E5E20`/`0042FAE0`. Interior anchor `002EEB59` (a `0042F250` call).

## SWE2-EC7-39 update (2026-09-19) - `0017E270`

`0017E270` (407 B) is a call-free locale-id resolver - `[01F82D20]` index into the `01DF0030` string-pointer table, byte-compares against `008C5904`+ rdata strings (`jpn`/`eng`/`fra`/`deu`), returns a small enum. Interior anchor `0017E288` (the first rdata byte compare).

## SWE2-EC7-40 update (2026-09-19) - `00255CF0`

`00255CF0` (389 B) is the scene/camera state writer the page names - `01CEBBA8`/`01CEBDA0`/`01F44830`, `00202B70` triple plus `00265020`/`00265090`/`00263940`/`00808C40`. Interior anchor `00255D3A` (a `00265020` call).

## SWE2-EC7-40 update (2026-09-19) - `00307E70`

`00307E70` (379 B) is a field-frame body - `01CEBCAC`/`01DFE0B8`/`022C1788`/`022C1F40`/`022C1F44`/`022C1F48`, `0032A150` pair plus `0031B810`/`00377C20`. Interior anchor `00307E9A` (a `0031B810` call).

## SWE2-EC7-40 update (2026-09-19) - `00339A60`

`00339A60` (390 B) is a world-tick body - `022C7E00`/`022C7E30`/`022C7F80` fields, `002646C0`/`00265090` pairs plus `003272A0`. Interior anchor `00339A70` (a `003272A0` call).

## SWE2-EC7-40 update (2026-09-19) - `003B18E0`

`003B18E0` (379 B) is a world-tick sibling - `02EBE5E0`/`02EBEBB0`/`02EBEBE0`/`02EBEBE4` fields, `0036C140` triple plus `0036C1D0`/`0032E4D0`/`0032E520`/`003B21E0`/`0032E590`. Interior anchor `003B194D` (a `0036C1D0` call).

## SWE2-EC7-40 update (2026-09-19) - `003D8190`

`003D8190` (366 B) is a field-frame body - `01CEBC08`/`02B4D7A0`/`02B4D7A8`/`02B4D7B0`, `0020E600` octuple plus `00181DD0`/`003D8E50`. Interior anchor `003D81D1` (an `00181DD0` call).

## SWE2-EC7-40 update (2026-09-19) - `003E8020`

`003E8020` (366 B) is a `003Exxxx` perception sibling - `02B5D088`, `003E8C50` pair plus `003E8990`/`003E8350`/`003E8440`/`003E8690`/`003E85B0`. Interior anchor `003E808E` (a `003E8990` call).

## SWE2-EC7-40 update (2026-09-19) - `00426C90`

`00426C90` (392 B) is a field-frame body - `01F44830`/`022C6F28`, `004268D0` pair plus `00426FA0`/`00427320`/`003E5CF0`/`0042F310`/`00808C40`. Interior anchor `00426CEE` (a `00426FA0` call).

## SWE2-EC7-40 update (2026-09-19) - `0051E3A0`

`0051E3A0` (362 B) is a world-tick body - `01CEBBA8`/`01F44830`, `003E7450`/`00428940`/`003B6B10`/`003B6B30`/`00808C40`. Interior anchor `0051E494` (a `003E7450` call).

## SWE2-EC7-41 update (2026-09-19) - `003E8440`

`003E8440` (354 B) is a field-frame body - `01CEBBA8`/`01CEBC9C`, `004735E0`/`00473500`/`004735D0`/`003E8190` triple/`0037B030`/`0037A270`. Interior anchor `003E847E` (a `004735E0` call).

## SWE2-EC7-41 update (2026-09-19) - `003DEB30`

`003DEB30` (341 B) is the audio teardown sibling the page names - `02B59360`/`02B59380`/`02B59C20`/`02B59C34`, `002DEE90` triple/`003697F0`/`002DF070`. Interior anchor `003DEBA5` (a `002DEE90` call).

## SWE2-EC7-41 update (2026-09-19) - `003E7EC0`

`003E7EC0` (339 B) is a field-frame body - `02B5D080`, `00265920`/`003E8020` pair. Interior anchor `003E7EC6` (a `00265920` call).

## SWE2-EC7-41 update (2026-09-19) - `003E8AA0`

`003E8AA0` (335 B) is a field-frame body - `02B5D080`, `00265920`/`0037A500` pair. Interior anchor `003E8AA8` (a `00265920` call).

## SWE2-EC7-42 update (2026-09-19) - `00336390`

`00336390` (315 B) is a field-frame body - `01F44830`, `0032A6A0` quintuple plus `00808C40`. Interior anchor `003363BD` (a `0032A6A0` call).

## SWE2-EC7-45 update (2026-09-19) - `0037D970`

`0037D970` (245 B) is the table step - `00237420`/`00358320`/`003D83A0`/`00808C40`; `003D83A0`'s only caller per the world-tick page. Interior anchor `0037D989` (a `00237420` call).

## SWE2-EC7-45 update (2026-09-19) - `002F82F0`

`002F82F0` (239 B) is a record accessor - `0030C300` x2 + `003148F0`/`003EC700`, the `022BE944`/`02EC3EA0` records the page names. Interior anchor `002F832E` (a `0030C300` call).

## SWE2-EC7-45 update (2026-09-19) - `003B25D0`

`003B25D0` (247 B) is a body - `0032E4D0`/`003B2220`/`003B2310`. Interior anchor `003B2623` (a `0032E4D0` call).

## SWE2-EC7-45 update (2026-09-19) - `003EB500`

`003EB500` (239 B) is a body - `00265F90`/`002EB870`/`002ED470`. Interior anchor `003EB539` (a `00265F90` call).

## SWE2-EC7-45 update (2026-09-19) - `004307C0`

`004307C0` (238 B) is a body - `003D8E50` single call. Interior anchor `00430836` (the `003D8E50` call).

## SWE2-EC7-46 update (2026-09-19) - `003B4840`

`003B4840` (229 B) is a body - `00181DD0` single call. Interior anchor `003B4870` (the `00181DD0` call).

## SWE2-EC7-46 update (2026-09-19) - `003EB9A0`

`003EB9A0` (225 B) is a body - `00226BA0`/`00229EA0`/`00265680`/`002672B0`/`00267330`/`002673F0`/`0035E790`. Interior anchor `003EB9A4` (a `00226BA0` call).

## SWE2-EC7-47 update (2026-09-19) - `003E85B0`

`003E85B0` (216 B) is a body - `0026FAD0`/`002700F0`/`00363AD0`/`0037A130`/`0037A310`/`003E8190`/`004735D0`. Interior anchor `003E85E8` (a `0026FAD0` call).

## SWE2-EC7-48 update (2026-09-19) - `0036E080`

`0036E080` (209 B) is a call-free ~~dual-table~~ triple-table slot clearer - `022D97B0`/`022D98B0`/`022D99B0` 64-entry dwords (`lea` at `0036E086` / `0036E0D1` / `0036E110`; corrected 2026-10-01, OPUS, on SWE2-AUDIT-SPEC's [review](../../_index/candidates/auditspec-review-sd121-0930/REVIEW.md), matching this page's own table row), `(v >> 0x10) & 0xF == ecx` clears by index clamp. Interior anchor `0036E086` (the first table load).

## SWE2-EC7-48 update (2026-09-19) - `00473500`

`00473500` (207 B) is a body - `00466BB0`/`00466C40`/`00467660`/`004676C0`/`00467700`/`00467730`. Interior anchor `00473525` (a `00466BB0` call).

## SWE2-EC7-48 update (2026-09-19) - `00258D70`

`00258D70` (205 B) is a float evaluator - `00229EA0`/`0024B9B0`/`0026F9D0`/`002FCF00`/`0036C140`/`0036C1D0`/`00374950`. Interior anchor `00258D82` (a `00229EA0` call).

## SWE2-EC7-48 update (2026-09-19) - `003D7DC0`

`003D7DC0` (203 B) is a body - `00181DD0`/`002DEE80`/`002DF050`. Interior anchor `003D7E02` (an `00181DD0` call).

## SWE2-EC7-48 update (2026-09-19) - `003EB5F0`

`003EB5F0` (201 B) is a body - `00265F90`/`002EB870`/`002ED470`. Interior anchor `003EB63E` (a `00265F90` call).

## SWE2-EC7-49 update (2026-09-19) - `00233640`

`00233640` (189 B) is a body - `00182FB0`/`00229E20`/`00229ED0`/`002335D0`/`002DE250`. Interior anchor `00233646` (an `00182FB0` call).

## SWE2-EC7-50 update (2026-09-19) - `0030C300`

`0030C300` (186 B) is a body - `00320AB0`/`00377C20`. Interior anchor `0030C337` (a `00320AB0` call).

## SWE2-EC7-50 update (2026-09-19) - `001B68D0`

`001B68D0` (185 B) is a body - `001B6990` single call. Interior anchor `001B6974` (the `001B6990` call).

## SWE2-EC7-50 update (2026-09-19) - `002EECC0`

`002EECC0` (183 B) is a body - `003E5E20`/`0042FAE0`. Interior anchor `002EED41` (an `003E5E20` call).

## SWE2-EC7-51 update (2026-09-19) - `00358EE0`

`00358EE0` (175 B) is `PartyFocus_UpdatePrimarySecondaryActorProcessing` - `0025A620`/`002671F0`/`00358F90`. Interior anchor `00358EF3` (a `0025A620` call).

## SWE2-EC7-51 update (2026-09-19) - `0030A190`

`0030A190` (177 B) is a body - `0020E600` single call. Interior anchor `0030A1AC` (the `0020E600` call).

## SWE2-EC7-51 update (2026-09-19) - `002B6260`

`002B6260` (172 B) is a body - `00244F00`/`00273A20`/`0029DF20`. Interior anchor `002B6293` (a `00244F00` call).

## SWE2-EC7-52 update (2026-09-19) - `00288A60`

`00288A60` (846 B) is a `00289xxx` bank-family body - `002AB860`/`00285F40`/`002F9860`/`0020E620`/`0029FA40` shared skeleton plus `01E0C3F0`. Interior anchor `00288A86` (a `002AB860` call).


## SWE2-EC7-52 update (2026-09-19) - `00288DB0`

`00288DB0` (649 B) is a `00289xxx` bank-family body - `002AB860`/`001E0E70` plus `01E0C3F0`. Interior anchor `00288DC5` (a `002AB860` call).

## SWE2-EC7-53 update (2026-09-19) - `002891A0`

`002891A0` (491 B) is a bank-slot resolver tail - `00287D10`/`00289830`/`002AB860`/`00808C40` plus `00915D50`-`00915DC0` rdata. Interior anchor `002891C2` (a `002AB860` call).

## SWE2-EC7-54 update (2026-09-19) - `00289040`

`00289040` (343 B) is a bank-slot resolver sibling - `001E0E70`/`002AB860`. Interior anchor `00289050` (a `002AB860` call).


## SWE2-EC7-54 update (2026-09-19) - `00287D10`

`00287D10` (328 B) is a bank-slot resolver sibling - `001E0BD0`/`001E0DA0`/`001E0E70`/`002AB860`. Interior anchor `00287D38` (a `002AB860` call).


## SWE2-EC7-54 update (2026-09-19) - `00289830`

`00289830` (315 B) is a bank-slot resolver sibling - `001E0DA0`/`001E0DC0`/`001E0E70`/`002AB860`. Interior anchor `00289854` (a `002AB860` call).

## SWE2-EC7-55 update (2026-09-19) - `00468E50`

`00468E50` (281 B) is a battle-unit field body - `00468580`/`004691A0`/`00861F14`. Interior anchor `00468E77` (a `004691A0` call).


## SWE2-EC7-55 update (2026-09-19) - `00468D50`

`00468D50` (250 B) is a battle-unit field body - `004691A0`/`00861F14`. Interior anchor `00468DC8` (a `004691A0` call).


## SWE2-EC7-55 update (2026-09-19) - `00426FA0`

`00426FA0` (249 B) is a field-frame body - `00426220`/`0042EF90`/`00808C40` plus `022C6F28`. Interior anchor `00426FEB` (a `00426220` call).


## SWE2-EC7-55 update (2026-09-19) - `003E8C50`

`003E8C50` (248 B) is a `003Exxxx` perception sibling - `0026FE50`/`002700F0`/`00270130`/`0037A130`/`0037A310`/`0037B0F0`/`003E8190`/`004735D0`. Interior anchor `003E8C81` (a `004735D0` call).

## SWE2-EC7-56 update (2026-09-19) - `00468580`

`00468580` (325 B) is a battle-unit field body - `00861F14` single call plus `009002C8`/`00915624`/`00D10820`/`00D10828`. Interior anchor `00468652` (a `00861F14` call).


## SWE2-EC7-56 update (2026-09-19) - `004691A0`

`004691A0` (315 B) is a call-free point-in-triangle/barycentric test - `subss` edge deltas on `[rdx]`/`[r9]` pairs, `divss` ratio, `comiss` bounds, boolean return. Interior anchor `0046924B` (the `divss` ratio).


## SWE2-EC7-56 update (2026-09-19) - `00422C20`

`00422C20` (237 B) is the shared tail the field-frame rejoins via `jmp 00422C20` - `0020E600`/`0020E620`/`002ED570`/`0051BA40`. Interior anchor `00422C42` (a `0020E600` call).


## SWE2-EC7-56 update (2026-09-19) - `003E8350`

`003E8350` (231 B) is a `003Exxxx` perception sibling - `0026FDB0`/`00362E30`/`0037B030`/`003E8190`/`004735E0`/`00834D40`. Interior anchor `003E839C` (a `004735E0` call).


## SWE2-EC7-56 update (2026-09-19) - `001B6990`

`001B6990` (213 B) is a field-frame body - `0016D6D0`/`0016DA60`/`00199DB0`/`005CD4F0`/`005CD820` plus one vcall. Interior anchor `001B69C0` (a `005CD4F0` call).

## SWE2-EC7-57 update (2026-09-19) - `0037B030`

`0037B030` (183 B) is a call-free `02EBF420` table lookup - `r10*0x10` records, `[rbx+4]`-counted word scan for `edi`, `word[rcx+rax*2+8]` to `imul 0x70` follow-on. Interior anchor `0037B072` (the word compare scan).

## SWE2-EC7-58 update (2026-09-19) - `003E75A0`

`003E75A0` (168 B) is a field-frame body - `0024CFF0`/`00470000`/`0051DC60` plus `022C6F28`/`02B59EA8`. Interior anchor `003E760E` (a `0024CFF0` call).


## SWE2-EC7-58 update (2026-09-19) - `003605A0`

`003605A0` (165 B) is a call-free multi-table flag writer - ~~`0x21AB9C0`/`0x21AB9D8`~~ `022CB9C0`/`022CB9D8` dword tables *(corrected 2026-10-02, OPUS: image-base relative, `003605A0+0x1A` `lea rcx, [00120000]`)*, `022CB732` `rax<<7` records, byte-pair writes and `shl` masks. Interior anchor `00360604` (the record byte write).

## SWE2-EC7-59 update (2026-09-19) - `002EB5E0`

`002EB5E0` (163 B) is a field-frame body - `002E2660`/`002EB690`/`002EB9D0` plus `02161DA0`. Interior anchor `002EB5FD` (a `002EB9D0` call).


## SWE2-EC7-59 update (2026-09-19) - `00320BB0`

`00320BB0` (162 B) is a world-tick body - `00236820` single call. Interior anchor `00320BC0` (a `00236820` call).


## SWE2-EC7-59 update (2026-09-19) - `0037A500`

`0037A500` (162 B) is a call-free `02EBF420` table word-scan - `r10*0x10` records, `[rbx+4]`-counted scan for `edi` (`0037B030` sibling). Interior anchor `0037A542` (the word compare scan).


## SWE2-EC7-59 update (2026-09-19) - `002FCF00`

`002FCF00` (161 B) is a field-frame body - `002FC350`/`002FC4A0`/`002FC860`/`0032E4D0` plus `02EBEBE4`/`02EC3D60`/`02EC3D7C`. Interior anchor `002FCF4F` (a `0032E4D0` call).


## SWE2-EC7-59 update (2026-09-19) - `0037A450`

`0037A450` (161 B) is a call-free per-element flag/float walker - `r10w` bound by `word[rax+0xA]`, `byte[+0x13]` mask bits 1/2/4, `+0x2C` vs `+0x28` `comiss` with `01DFE0BC` adds. Interior anchor `0037A483` (the `byte[+0x13]` test load).

## SWE2-EC7-60 update (2026-09-19) - `00466DD0`

`00466DD0` (157 B) is a field-frame body - `00467730` single call plus `02EBB6E0`/`02EBB6F0`/`02EBB6F8`. Interior anchor `00466E3A` (a `00467730` call).


## SWE2-EC7-60 update (2026-09-19) - `0046E1B0`

`0046E1B0` (156 B) is the `[022C6F20]+0xD98` deep body the world-tick page names - `002ED570`/`00537170`/`00537180`. Interior anchor `0046E1CB` (a `00537170` call).

## SWE2-EC7-61 update (2026-09-19) - `0025A0C0`

`0025A0C0` (152 B) is the second-rate tick tail the world-tick page names - `0032B880` single call plus `00915620`/`01CEBC50`/`01CEBC78`/`02097FE0`. Interior anchor `0025A136` (a `0032B880` call).


## SWE2-EC7-61 update (2026-09-19) - `003DD380`

`003DD380` (151 B) is a `02B5xxxx` record-bank body - `0020E600`/`00369800`/`0041E490` plus `022C6F28`/`02B581A4`. Interior anchor `003DD3D1` (a `0020E600` call).

## SWE2-EC7-62 update (2026-09-19) - `00308DE0`

`00308DE0` (149 B) is a world-tick body - `003008A0` single call plus `01EEBD54`/`01EEBF0C`. Interior anchor `00308E14` (a `003008A0` call).


## SWE2-EC7-62 update (2026-09-19) - `00374950`

`00374950` (149 B) is a world-tick body - `001EDDA0`/`00374060`/`00375470` plus `02EBF9E0`. Interior anchor `0037498A` (a `001EDDA0` call).


## SWE2-EC7-62 update (2026-09-19) - `003E8190`

`003E8190` (149 B) is an indirect-only `02B5D080` word-list dispatcher - `movsx word[rdx+rax*2+2]` record index, `[rsi]`-counted gate, `call r14` per element. Interior anchor `003E81DB` (the `call r14` element dispatch).


## SWE2-EC7-62 update (2026-09-19) - `0026FDB0`

`0026FDB0` (148 B) is a `003Exxxx` perception body - `0024F650`/`0024F680`/`00808C40` plus `01F44830`. Interior anchor `0026FDE8` (a `0024F680` call).


## SWE2-EC7-62 update (2026-09-19) - `002A2720`

`002A2720` (146 B) is a request/mailbox body - `00244DD0`/`00861EC0` plus `0209C4D0`/`0209C700`/`0209C980`/`0209C988`. Interior anchor `002A275E` (a `00244DD0` call).


## SWE2-EC7-62 update (2026-09-19) - `0037A270`

`0037A270` (146 B) is a call-free `02EBF420` word-scan - `[r11+4]`-counted `word[]` scan from `[r11+0xA]` for `bx` match (`0037A500`/`0037B030` family). Interior anchor `0037A2B0` (the `word[rcx]` scan load).



## SWE2-EC7-63 update (2026-09-19) - `0037A130`

`0037A130` (145 B) is a call-free `02EBF420` flag body - `r10*0x10` record index, `[r10+0x28]` sublist `[rbx+4]`-counted scan, `word[+8]` -> `x0x70` record, `and byte[+0x13], ~2` (clear bit 1). Interior anchor `0037A1B1` (the `and byte[+0x13], ~2`).



## SWE2-EC7-63 update (2026-09-19) - `0037A1D0`

`0037A1D0` (145 B) is a call-free `02EBF420` flag body sibling - same scan shape, `or byte[+0x13], 2` (set bit 1). Interior anchor `0037A251` (the `or byte[+0x13], 2`).



## SWE2-EC7-63 update (2026-09-19) - `0037A310`

`0037A310` (145 B) is a call-free `02EBF420` flag body sibling - same scan shape, `and byte[+0x13], ~4` (clear bit 2). Interior anchor `0037A391` (the `and byte[+0x13], ~4`).



## SWE2-EC7-63 update (2026-09-19) - `0037A3B0`

`0037A3B0` (145 B) is a call-free `02EBF420` flag body sibling - same scan shape, `or byte[+0x13], 4` (set bit 2). Interior anchor `0037A431` (the `or byte[+0x13], 4`).



## SWE2-EC7-63 update (2026-09-19) - `0037B0F0`

`0037B0F0` (145 B) is a call-free `02EBF420` flag body sibling - same scan shape, `or byte[+0x13], 1` (set bit 0). Interior anchor `0037B171` (the `or byte[+0x13], 1`).



## SWE2-EC7-63 update (2026-09-19) - `0037B190`

`0037B190` (145 B) is a call-free `02EBF420` flag body sibling - same scan shape, `and byte[+0x13], ~1` (clear bit 0). Interior anchor `0037B211` (the `and byte[+0x13], ~1`).



## SWE2-EC7-64 update (2026-09-19) - `002EDAA0`

`002EDAA0` (141 B) is a stop-registry sibling - `00420CF0`/`00420F20` plus `022C6F28`. Interior anchor `002EDAF4` (a `00420CF0` call).



## SWE2-EC7-64 update (2026-09-19) - `002E06F0`

`002E06F0` (138 B) is a request/mailbox body - `002A2720`/`002F1C50` plus `0215F1B6`/`0215F200`. Interior anchor `002E072D` (a `002A2720` call).



## SWE2-EC7-65 update (2026-09-19) - `002E2660`

`002E2660` (136 B) is a call-free dual zero-fill - `[r8]` dword + `[rax]` word over `r9` elements, `+0x48`/`+0x50`/`+0x58` null, `0215FD70`. Interior anchor `002E2690` (the zero-fill loop head).


## SWE2-EC7-67 update - `00360DD0`

`00360DD0` (128 B) is the listener/scene-cell body - `002DEC00`/`002DEDE0`/`002DEC20` plus `022CB9F1`/`022CBA51`. Interior anchor `00360DE4` (a `002DEC00` call).

## SWE2-EC7-68 update (2026-09-19) - `002DF050` non-negative guard forwarder

`002DF050` (9 B) is the index guard the tick bodies run before the
shared worker: a non-negative `ecx` tail-jumps `001DBE40`, a
negative one returns without touching anything. Interior anchor
`002DF052` (the `jns` forward).

## SWE2-EC7-69 update (2026-09-19) - `001E0E70` tick-arm probe measured

`001E0E70` (111 B) is the probe the `00288xxx` bank-family bodies run per
arm: `ecx > 0x80` returns 0 immediately; otherwise it resolves the operand
through `00198790` → `00197800`, then dispatches on the result -
`(eax-1) & ~2 == 0` (result 1 or 3) takes `0079E6D0([00796E20()+0xDF8],
result)`, any other result takes `0079E6A0([00796E20()+0xDF8], result, 0)`
with `r8d` zeroed; the byte result returns widened. The two-arm split is a
strict/non-strict variant on the same `[+0xDF8]` sub-object.
Interior anchor `001E0E94` (the `test ecx, 0xfffffffd` arm select).

## SWE2-EC7-69 update (2026-09-19) - `002ED470` slot teardown measured

`002ED470` (103 B) is the slot reset the record-bank teardown runs: `bx ==
-1` skips straight to the tail; otherwise it indexes the slot table
`[022C6F28] + movsx(bx)*0x740`, and when the slot's `+0x284` word is nonzero
it zeroes `qword[+0x108]` and calls `003E5E20(slot, 0)` on the same record
(a second `+0x284` check after the pointer reload gates the call). Every
path tails to `0042FAE0(bx & 0xFFFF)` - the same slot id published onward.
Interior anchor `002ED48A` (the `imul rdx, rax, 0x740` slot scale).

## SWE2-EC7-70 update (2026-09-19) - `003E5E20` record-flag copy measured

`003E5E20` (43 B) is the `+0x284`-record field copy the slot teardown calls:
NULL `rdx` or `dword[rdx] != 0x30` is a no-op; otherwise it copies
`byte[+0x10]` to `[rcx+0x40D]` and the two 16-byte rows `+0x20`/`+0x30` to
`[rcx+0x530]`/`[+0x540]`. The `0x30` leading dword is the record tag the
`022C6F28` slot rows carry.
Interior anchor `003E5E34` (the first `movups` store).

## SWE2-EC7-70 update (2026-09-19) - `0042FAE0` slot-resolve forwarder measured

`0042FAE0` (51 B) is the resolver `002ED470` tails into: `cx == -1` passes
NULL to `00429140`; otherwise it resolves `022C6F28 + movsx(cx)*0x740` and
substitutes NULL when the slot's `+0x284` dword reads 0, then tails
`00429140(slot)`. The same empty-slot NULL substitution `002ED470` applies
before calling `003E5E20`.
Interior anchor `0042FAF3` (the `imul rdx, rax, 0x740` slot scale).

## SWE2-EC7-70 update (2026-09-19) - `0042F310` two-slot flag op measured

`0042F310` (151 B) is the pair-wise slot op the record-bank teardown runs:
either `cx` or `dx` equal to `-1` vetoes outright. Source slot `dx`
(`022C6F28 + movsx*0x740`, NULL-substituted when its `+0x284` is 0) gets
`+0x284` bit `0x1E` set only when bit 2 was already up; destination slot
`cx` then receives `word[+0x3CE] = dx`, `word[+0x3CC] = r8w`, and `+0x290`
masked `0xFFEBFFFF` (clears bits 18 and 20) with `bts` bit 19.
Interior anchor `0042F39C` (the `bts eax, 0x13` flag commit).

## SWE2-EC7-71 update (2026-09-19) - `002700F0` + `0025A520` flag-table setters measured

`002700F0` (49 B) is the `02F8F220` 64-entry byte-flags setter: `ecx >=
0x40` is a no-op; `edx == 0` clears bit 0 then sets bit 2 if bit 3 was
already up; `edx != 0` clears bit 2 and sets bit 0 - the enable/arm pair
the `003E8440`-`003E8C50` family writes through.
Interior anchor `0027010A` (the `and al, 0xfe` clear).

`0025A520` (27 B) is the `02098DEC` single-bit setter: `edx` truthy ORs
`1 << cl`, else ANDs `~(1 << cl)` - a 32-bit flag word shared by the
tick-path callers.
Interior anchor `0025A52B` (the `or` into `02098DEC`).

## SWE2-EC7-71 update (2026-09-19) - `0017DE60` key-`0x49` check measured

`0017DE60` (56 B) is the binding check the tick bodies run:
`00796E20()` resolves the input state object, `[rax+0xDF8]` is its
sub-object, and `0079AE90(obj, 0x49, 0)` polls binding `0x49`; on true
it runs `001E1100(0)` and returns 1.
Interior anchor `0017DE77` (the `0079AE90` poll).

## SWE2-EC7-72 update (2026-09-19) - `00426E20` one-bit latch measured

`00426E20` (21 B) is the `+0x290` latch the tick setters call: when bit
0 of `dword[+0x290]` is clear it `bts` bit `0xC` and stores - set-once
arm flag.
Interior anchor `00426E2A` (the `bts eax, 0xc` latch).

## SWE2-EC7-74 update (2026-09-19) - `00363AD0` + `0031BD60` + `002F1C50` tick helpers measured

`00363AD0` (37 B) is the resolved-record bit-4 setter: `00362DC0()`
yields the record, and when non-NULL `byte[rax+8]` is masked `0xEF`
then OR'd `(edx & 1) << 4`.
Interior anchor `00363AE2` (the `and byte [rax+8]` mask).

`0031BD60` (30 B) is the result capture: `022C2674` zeroed,
`0031AC00()` runs, its dword return lands in `022C2670` - the
tick-side side-effect pair.
Interior anchor `0031BD6E` (the `0031AC00` call).

`002F1C50` (114 B) is the `022BE7D0` task-record init: when the
singleton is NULL `002F16B0()` allocates (the verified
ScheduledTaskRecord allocator), `[rax+8]` gets the `002F18A0`
descriptor and `+0x20` clears; then `002E1C20(0xA, 1)`, `001EDDA0()`,
`ecx = eax ? [01DFE0B4] : 1` scaled by `ebx`, and the record's
`word[+0x1C] = 1`, `[rax] = 0`, `[rax+4] = ecx` are stamped - the
first task the scheduler registers.
Interior anchor `002F1C8B` (the `002E1C20` call).

## SWE2-EC7-75 update (2026-09-19) - `002EF9F0` + `002EB9D0` + `002EAE20` + `002EAEB0` + `002EA8B0` tick-side helpers measured

`002EF9F0` (39 B) is the `022BDD60` clamped indexed getter: `ecx`
clamped to [0,6], then `dword[022BDD60 + ecx*24]` - the seven-slot
record read.
Interior anchor `002EFA13` (the indexed `mov`).

`002EB9D0` (253 B) is the dual-bitmap allocator: `ebx >= 0` tries bit
`1<<ebx` in `[rdi+0x28]` - taken returns -1 unless already set in
`[rdi+0x2C]`; free sets it, runs `002E9920([rdi+0x14], ecx)`, and a
positive return also sets `[rdi+0x2C]`'s bit. `ebx < 0` calls
`002ED6F0([rcx+0x14], &two, &one)` for a count capped at 0x20, then
scans bits 1..count for the first that passes the same protocol.
Interior anchor `002EBA0C` (the `002E9920` check call).

`002EAE20` (113 B) is the `0215FD58`/`0215FD78` find-or-create sibling
of `002EB540`: walks both lists for `+0x14 == ecx`, allocates via
`002E25E0` on a miss, pushes onto the `0215FD78` head, and ORs
`word[+0x20]` bit 0 - the holder-bit-0 insertion the script-names page
describes.
Interior anchor `002EAE63` (the `002E25E0` allocation call).

`002EAEB0` (192 B) is the matching unlink-and-relist: `+0x18` bit 1 or
`+0x19` bit 2 already set just ORs `+0x18` bit 2 and returns; otherwise
it sign-extends `word[+0x1E]` into `02161DA0 + idx*0x120`, re-stamps
the sub-record's `+0x5C` from the owner's incremented `+0x24`, clears
`+0x18` bit 1 and `+0x26`, splices the entry out of whichever of
`0215FD58`/`0215FD78` heads it, and pushes it onto the `0215FD88`
list - the release path the holder-bit protocol pairs with.
Interior anchor `002EAF46` (the `[rcx] = rax` splice write).

`002EA8B0` (46 B) is the `0215FD45` bit writer: `edx` picks `bts`/`btr`
of bit `ecx` on the byte, then tails `003E7C70` with 1 or 0 - the
flag-plus-notify the tick bodies share.
Interior anchor `002EA8BB` (the `bts` arm).

## SWE2-EC7-76 update (2026-09-19) - `0026FE50` + `00254940` + `00254850` tick helpers measured

`0026FE50` (95 B) is the `02F8F238`-gated record push: flag set
builds a stack record (type 2, `word = ecx`), calls `0024DB80`, then
clears `02F8F23C + rbx` bits `0x0C` - the flagged push the tick
bodies share.
Interior anchor `0026FE86` (the `0024DB80` call).

`00254940` (50 B) is the conditional picker: `ebx` nonzero selects
`002E1CA0`, zero `002E1C20`, called with `ecx = 8`; then `002547D0`
tails with `ebx` - the variant dispatch.
Interior anchor `00254964` (the `call rax`).

`00254850` (148 B) is the ten-arm `002E1C20` registration sweep:
`ecx` nonzero runs `002E1C20` ten times with `(8, {0, 0x14, 0xB, 1,
2, 4, 5, 6, 7, 9})` - the bulk verb registration.
Interior anchor `00254861` (the first `002E1C20` call).

## SWE2-EC7-77 update (2026-09-20) - `00253BC0` + `0024F680` tick helpers measured

`00253BC0` (53 B) is the masked-id set test: `(ecx & 0x7FFF) - 2` must
be `<= 0x14`; the 21-entry jump table at `0012FBF8`/`+0x133C00` lands
every arm on `mov eax,1; ret` - membership in the 2..22 id band
(after the mask) returns 1, anything else 0.
Interior anchor `00253BD8` (the table byte load).

`0024F680` (53 B) is the `020910F0` bucket-chain find: the head is
`[020910F0 + byte[rcx]*8]`; the walk follows `+0x348` links until
`word[+4]` equals `word[rcx+4]`, returning the node or 0.
Interior anchor `0024F6A0` (the `+4` word compare).

## SWE2-EC7-81 update (2026-09-20) - `00537180` tick-modulo measured

`00537180` (25 B) is the modulo the frame callers run:
`00879750()` supplies the tick and `eax` returns
`tick % dword[rbx+0x20]` - the period-bounded phase.
Interior anchor `00537189` (the `00879750` call).

## SWE2-EC7-82 update (2026-09-20) - `0051DC60` + `00470000` + `004735E0` measured

`0051DC60` (34 B) is the small field reset the frame callers share:
`+0x19`/`+0x18`/`+0x31`/`+0x30` go to `0xFF`, `+0x28`/`+0x40`/`+0x33`
go to 0 - an init-to-empty with no calls.
Interior anchor `0051DC68` (the `+0x28` clear).

`00470000` (69 B) is the release-side sibling: `byte[+7]` keeps only
bit0, `[+0]` zeroes, `word[+4]` goes `0xFFFF`, and live `+8`/`+0xC`
ids release through `003ABCA0` before zeroing - the same
`003E75A0`/`003E7D50` caller pair drives both helpers.
Interior anchor `00470020` (the first `003ABCA0` call).

`004735E0` (23 B) is the `00466AD0()` probe the tick callers gate
on: returns 1 when the callee's result is 0, else 0.
Interior anchor `004735E4` (the `00466AD0` call).

## SWE2-EC7-83 update (2026-09-20) - `00467730` element-broadcast measured

`00467730` (112 B) is the indexed broadcast the tick callers run:
`ecx` bounds-checks against ~~`dword[01EAB6D8]`, selects the x80 record~~ `dword[02EBB6E0]`, selects the `0x50`-byte record
~~in `01EAB6E0`~~ at `*02EBB6F0` *(corrected 2026-10-02, OPUS: `00467730+0x4` `cmp ecx, [02EBB6E0]`, `+0xC`–`+0x17` index × `0x50` + `[02EBB6F0]`)*, and on a live `[+8]` clears `+0x4C` bit2 then sets
bit3, stores `xmm1` to `+0x44` and 0 to `+0x48`; then `word[+0x30]`
elements of the `[+0x20]` table each take `xmm1` at `+i*0x18+8` and
0 at `+i*0x18+0x10` - a per-record flag set plus payload fan-out.
Interior anchor `0046778B` (the `+0x18`-stride `movss` store).

## SWE2-EC7-87 update (2026-09-20) - `003DAA20` + `003CCF20` + `003CBFA0` measured

`003DAA20` (17 B) is the two-pointer clear the tick callers
run: `02B57CC8` and `02B57CD0` are both zeroed, call-free.
Interior anchor `003DAA29` (the second qword clear).

`003CCF20` (887 B) is the timed-dispatch pass the tick runs over
the `02B47778` chain: each node gates on `byte[+1] & 0x80` (with
an `00181DD0` liveness re-check and `+0x38` counter compare),
normalizes `+0x40`/`& 0x7F`, resolves its `+8`/`0036B130` slot,
then walks the `[+0x28]` sub-list counting `word[+0xA]` down by
the frame delta, accumulating `word[+0x34]`, unlinking
`02B47798`-table rows whose `+0x30` count expires (refcount dec,
`+0x38`/`+0x40` splice), and computing `+0x36` progress from
`word[+0x10]` before an 8-arm `byte - 1` jump table dispatches
`0050AC20`/`00506B40`/`005080A0`/`00509BB0`/`00507490`/
`00508C90`/`00507120`/`0050A100`; `003D2B60` closes the node.
Interior anchor `003CD0F6` (the jump-table index read).

`003CBFA0` (72 B) is the vec3 delta the tick callers run:
`[rdx] = [+0xA0]-[+0x90]`, `[+4] = [+0xA4]-[+0x94]`,
`[+8] = [+0xA8]-[+0x98]`, and `dword[+0xAC]` copies into
`[rdx+0xC]` - one position delta plus a trailing word, call-free.
Interior anchor `003CBFC9` (the third `subss`).

## SWE2-EC7-88 update (2026-09-20) - `003CB440` + `003C9550` measured

`003CB440` (168 B) is the one-time big-table install the tick
callers run: when `[02B47760]` is null, `00244F50(0x179E0,
003CB650, &desc)` builds the record through the `003CB650`
callback and stores it; `00249580()` supplies the context for
`00404060(ctx, record+0x190)` and `00249410(ctx)`, then
`003BC450(0, 1, record)` arms it - all under a stack cookie.
Interior anchor `003CB489` (the `00244F50` call).

`003C9550` (20 B) is the single-bit clear the tick callers run:
when `[02B47730]` is live, `dword[+0xC0] &= ~8`.
Interior anchor `003C955C` (the `and` arm).

## SWE2-EC7-90 update (2026-09-20) - `003B08F0` conditional slot sweep measured

`003B08F0` (73 B) is the conditional sweep the tick callers run:
the 36-slot `02EBEC00` table is walked and `003B0770(key)` fires
for each live entry whose `byte[+0x13]` bit 0 is clear and whose
`byte[+0x10]` is not `0x63`.
Interior anchor `003B0915` (the `003B0770` call).

## SWE2-EC7-91 update (2026-09-20) - `0024EE10` intrusive unlink measured

`0024EE10` (74 B) is the removal the tick callers run on the
`+0x348`/`+0x350` doubly-linked list: when `qword[+0x350]` is
null the head slot in the `rip`-indexed bucket table
(`byte[rcx]` selects it) takes `qword[+0x348]`, otherwise
`[+0x350]`'s `+0x348` back-link is patched - then `+0x348`'s
`+0x350` forward-link is patched symmetrically. `0024B1F0`'s
inverse.
Interior anchor `0024EE32` (the head-slot store).

## SWE2-EC7-92 update (2026-09-20) - `00382B70` + `00377520` measured

`00382B70` (119 B) is the vec4-pair publish the `0037D4C0`/
`0037D890` camera-path callers run: `[rcx]`'s four floats and `[rdx]`'s
four floats land contiguously at `02A19F64`, then `xmm2` and `xmm3`
follow at `02A19F58`/`02A19F54`.
Interior anchor `00382B89` (the second vec4's first store).

`00377520` (58 B) is the once-per-change gate the `0022A770` frame
walker runs: when `02A8D107` is set and either `02FC99B4` or
`02A8D0D7` is set, it calls `003ED170` on the `02A8D0E2` block and
clears `02A8D0BF` — a dirty-flag consumption, not a per-frame cost.
Interior anchor `00377546` (the `003ED170` call).

## SWE2-EC7-93 update (2026-09-20) - `00363180` + `00362E30` measured

`00363180` (23 B) is the flag-arm the `003E8440`/`003E8690` tick
callers run: `00362DC0()`'s record, when non-null, gains byte `+8`
bit 3.
Interior anchor `0036318E` (the `or`).

`00362E30` (31 B) is the paired query: same `00362DC0()` fetch,
returning `[rax+8] & 1` when the record exists (and whatever `eax`
held when it does not - the null path leaves the register unset).
Interior anchor `00362E3E` (the `movzx` flag read).

## SWE2-EC7-94 update (2026-09-20) - `00362DC0` + `003604D0` measured

`00362DC0` (104 B) is the word-offset fetcher the four `0036xxxx`
callers share (`00362E30`, `00363180`, `00363A90`, `00363AD0`): two
rip-globals at `02CBB5F4`/`02CBB5DE` gate the walk, the second's
`+0xC` dword goes through `0020E600` to a resolved index, and the
result reads a word-counted offset table - `word[base]` is the count
the argument must sit under, `word[base + 2 + arg*2]` is the offset
added back to the table base (0 offset returns NULL).
Interior anchor `00362DF1` (the `0020E600` call).

`003604D0` (194 B) is the 5-by-8 bit-clear sweep `002628B0` and
`00266D10` run: an outer 0-4 slot loop wraps an inner 0-7 bit loop
that ANDs `~(1<<n)` out of the two ~~`02CDC4xx`-region~~ dword masks at
~~`+0x21AB9C0`/`+0x21AB9D8`~~ `022CB9C0`/`022CB9D8` *(corrected 2026-10-02, OPUS: image-base relative, `003604D0+0x23` `lea r15, [00120000]`)* per slot, while a parallel 0x10-stride
record gets `byte[+0]=bit`, `byte[-1]=slot`, `byte[-2]=counter` and
`qword[+6]=0`; the `02CDBB2D` byte is re-cleared on exit.
Interior anchor `00360541` (the `1<<n` shift inside the bit loop).

## SWE2-EC7-97 update (2026-09-20) - `002EB870` measured

`002EB870` (29 B) is the countdown clamp `003EB500` and
`003EB5F0` run per tick: `word[+0x1C]` decrements, and once it
reaches 0 or below a `byte[+0x19] & 3` test decides whether it
is re-armed (left alone) or pinned at 0 - the expiry latch the
frame loop consults.
Interior anchor `002EB880` (the `& 3` flag test).

## SWE2-EC7-98 update (2026-09-20) - `002E3F00` + `002E3DC0` + `002E25E0` measured

`002E3F00` (255 B) is the two-list keyed find `002E6BD0` and
`0037B4D0` call: the `022CBD58` chain then the `022CBD78`
chain are walked for `dword[+0x14] == ecx`, and a hit with
`edx >= 0` resolves the `0x120`-stride record `word[+0x1E]`
indexes into the `022C9DA0` table, validates `dword[+0x5C]
== [+0x24]`, then per slot (`edx` first, slot 0 second)
either pins the `+0xE0` word to 0 (mask bit set in
`[+0x3C]|[+0x38]`) or runs `002EAFA0` - the per-slot
fire-or-clear pass.
Interior anchor `002E3F9D` (the `002EAFA0` call).

`002E3DC0` (96 B) is the sibling find `0037B4D0`, `003EC630`
and `003EC690` call on the same two chains: a hit with
`word[+0x1C] <= 0` either pins it (`byte[+0x19] & 3` set) or
tails `002EAEB0` - the countdown-expiry arm `002EB870`'s
decrement feeds.
Interior anchor `002E3E14` (the `002EAEB0` tail jmp).

`002E25E0` (113 B) is the pop `002EAE20` and `002EB540` call
on the sibling `022CFD60` list: the head node's `dword[+0x24]`
increments, `byte[+0x19]` keeps only bits 3/6/7, `+0x14`
takes `ecx`, `+0x1E` is stamped `-1`, `+0x30` and `+0x38`
take `-1`, the head pointer advances, and the node is
unlinked from its doubly-linked list - the detach-and-reset
that recycles a request node.
Interior anchor `002E2618` (the head-pop store).

## SWE2-EC7-104 update (2026-09-20) - `0026A3B0` + `002678C0` measured

`0026A3B0` (102 B) is the bounded word write
`00255FF0` and `00256F60` run: `002E97B0`
resolves the destination array, and when the
result is non-null with `[rax] != -1` it
clamps `edx` into `[0, 1]` and stores `r8w`
at `word[rax + edx*2 + 0x20]`, returning 1;
unresolved or sentinel rows return 0.
Interior anchor `0026A3C0` (the `002E97B0`
call).

`002678C0` (99 B) is the full reset sequence
`0025B600` and `0036FCC0` run: `00238B00(1)`,
then - only while `byte[02099DA7]` is clear -
`002509A0(0, 0)` plus arming that flag; then
`002E1CD0(0, 0)`, `003601B0(0xC)`, and
`00226BE0(0x13, 0, 0, -1, -1)`, tailing
`00226280` - the ordered cold-start chain the
frame arms share.
Interior anchor `002678C9` (the `00238B00`
call).

## SWE2-EC7-105 update (2026-09-20) - `00263EB0` measured

`00263EB0` (81 B) is the bounded word read
`00255FF0`, `00256F60` and `002578F0` call -
the reader twin of `0026A3B0`'s write:
`002E97B0` resolves the array, and when the
result is non-null with `[rax] != -1` it
clamps `edx` into `[0, 1]` and answers
`word[rax + edx*2 + 0x20]`; unresolved or
sentinel rows answer 0.
Interior anchor `00263EB8` (the `002E97B0`
call).

## SWE2-EC7-107 update (2026-09-20) - `00235EA0` measured

`00235EA0` (78 B) is the
default-vs-record float `00358A20`
and `00358CB0` call: `00303EC0()`
nonzero tails `003045A0`; otherwise
`003272A0()` resolves the record -
a null record answers `5.0 /
(1.0 * 30.0)` - `float[009146E4]`
over `float[01DFE0B8]` times
`float[008F8D80]`, a live one
`float[rax + 0x17C]` - the
scale the frame arms share.
Interior anchor `00235EE1` (the
`+0x17C` read).

## SWE2-EC7-110 update (2026-09-20) - `001E0DC0` measured

`001E0DC0` (62 B) is the
three-byte setter `00289830`
and `002B5B60` run:
`00198790()` fetches the
target object unconditionally
(no null gate this time), then
the tail `00197870(object,
cl, dl, r8b)` forwards all
three byte arguments as
`movzx` widened values - the
world-tick and cutscene-slot
pages' shared three-channel
apply.
Interior anchor `001E0DDE`
(the `movzx r9d, bl` third
argument widening).

~~`0050A100` (2842 B) is the flag-pack scan `003CCF20` and `003CD2C0` run inside the timed dispatch: a `[rbp-0x40]` flag block is built from `word[r8+0xE]`/`byte[r9+0x26]`/`+0x14`/`+0x12`/`+0x24` fields with `sbb`/`neg`/`not` folding, then `movups` stores publish it - a call-free jump-threaded packer.~~ **Corrected 2026-09-30 (SWE2-EC7, SD-120):** `0050A100` (2842 B) is binding operation 4 of the palette (CLUT) animation machine `003CCF20` and `003CD2C0` dispatch: it fades the record's entry range (`+0x12` entries from `+0x14`) toward another binding's current palette, entry by entry, over the `+0x24` duration, in the two modes of operation 3 (`+0x26`: a weighted cross-fade, or per-lane unit steps); the `sbb` folds apply the `+0x03` lane mask. It is call-free: the dispatcher decodes the target palette before the call (SWE2-ORACLE's M4, [sd120-binding-ops-0930](../../_index/candidates/sd120-binding-ops-0930/README.md); consumer check [ec7-sd120-oneliners-0930](../../_index/candidates/ec7-sd120-oneliners-0930/README.md)).

Interior anchor `0050A407` (function `0050A100`).

`0028F2A0` (73 B) is the drain loop `00253A30`'s reset battery tails into and `00252DE0` also runs: while `[0209BE80]+0x7C70` stays nonzero, `003FA4E0(rax+0x57E0, [rax+0x7C70])` processes the pending entry and the field is re-checked - the pending-request drain on the `0209BE80` global, terminating only when the queue empties.

Interior anchor `0028F2CE` (function `0028F2A0`).

`00507120` (867 B) is the timed-dispatch bodies `003CCF20` and `003CD2C0` call: ~~`word[r8+0xE]` supplies the count, `word[r8+0x36]` divides by it for the stride, and `0053DB50` runs the per-item step across the record - the dispatch pass's divisor-keyed walker.~~ **Corrected 2026-09-30 (SWE2-EC7, SD-120):** binding operation 8: it cross-fades the entry range toward another binding's palette with weight `(int)(256·curve(t))`. The `+0x36`/`+0x0E` division is time, not a count and a stride: `t` is the record's local time `+0x36` over its divisor `+0x0E`. `0053DB50` is called once per call, on the `+0x28` curve, for that weight; the per-entry loop is the operation's own lane blend (M8, [sd120-binding-ops-0930](../../_index/candidates/sd120-binding-ops-0930/README.md)).

Interior anchor `005071B3` (function `00507120`).

`002887B0` (678 B) is the first bank-pass `002878E0` runs: `002AB860` context, `rbx+0x60` -> `+0x38` chain walk, `+0x50 & 0x3FFFC` element loops with `byte[+8]&0x3C==4` filter, `+0x18` -> `+0x60` -> `+0x10` sub-records, `+8>>16` searched in `01E0C3F0` (21 entries), byte-pair table at `+0x30`/`+0x14`, `001E0E70` input reads - the resolver's `+0x38`-chain half.

Interior anchor `002887C5` (function `002887B0`).

`00288500` (678 B) is the second bank-pass `002878E0` runs: identical shape on the `+0x30` chain instead of `+0x38` - the resolver's twin pass over the other attachment list.

Interior anchor `00288515` (function `00288500`).

`00287E60` (577 B) is the per-record arm `002878E0` calls: `002AB860` resolves, `rbx+0x60` -> `+0x18` -> `+0x18` -> `+0x60` -> `+8` -> `+0x18` chases the chain to `rsi`, `dword[rsi+0x50] & 0x3FFFC` bounds the loop, then `00285F40`/`0029FA40`/`002F9860`/`001E0E70`/`001E0EE0`/`0020E620` run per slot - the tick's record walk.

Interior anchor `00287E7A` (function `00287E60`).

`002880B0` (561 B) is the sibling record walk `002878E0` calls: `002AB860` resolves, the same `+0x60`->`+0x18`->..->`+0x18` chain to `rsi`, `dword[rsi+0x50] & 0x3FFFC` bounds the loop, and per slot `[rdi+8] & 0x3C == 0x14` selects `00285F40(rsi,4)` -> `001E0F00(2)` -> `002F9860(0x58E or 0x547)` -> `0020E620` -> `0029FA40` - the tick's per-slot emit with the two-way text pick.

Interior anchor `002880CA` (function `002880B0`).

`002882F0` (521 B) is the third sibling record walk `002878E0` calls: `002AB860` resolves, the `+0x60`->`+0x28`->`+0x18`->`+0x60`->`+8`->`+0x18` chain to `r13`, `dword[r13+0x50] & 0x3FFFC` bounds the loop, and per slot `[rdi+8] & 0x3C == 4` selects the `001E0E70` arm - the same walk shape as `00287E60`/`002880B0` on a different record field.

Interior anchor `00288306` (function `002882F0`).

~~`0053DB50` (437 B) is the call-free curve lookup `00507120` calls: `edx = [rcx+4]` counts `(key, value)` pairs at `rcx+0x10`, `comiss` short-circuits below the first key and above a linear probe, and the `sar eax, 1` loop bisects the `8`-byte pairs for `xmm1` - the tick's interpolation table search.~~ **Corrected 2026-09-30 (SWE2-EC7, SD-120):** `0053DB50` (437 B) is the call-free curve evaluator operation 8 (`00507120`) calls once for its blend weight: `edx = [rcx+4]` counts 16-byte keys `(time, value, in-tangent +8, out-tangent +0xC)` from `rcx+0x10`; it clamps outside the keys, the `sar eax, 1` loop bisects them (`add rcx, rcx` then `[r9 + rcx*8]` at `0053DBA9` is the 16-byte stride), and it interpolates a cubic Hermite with the tangents scaled by the key interval - keys (0, 0) and (10, 1) give 0.15625 at t = 2.5, not the linear 0.25 (K3, [sd120-binding-ops-0930](../../_index/candidates/sd120-binding-ops-0930/README.md)).

Interior anchor `0053DBA0` (function `0053DB50`).

`00181DD0` (21 B) is the `+0x118` byte getter: `001EBA40()` supplies the context, `movzx byte[rax+0x118]` returns it - the single-field read the tick and its peers share.

Interior anchor `00181DD9` (function `00181DD0`).

`0024B9B0` (1500 B) is the mode-indexed record-state driver the three world-tick arms call: `edx` selects one of eight list heads at `020910F0` (mode 8 bails immediately), each record's `qword[+0x348]` links the walk and `word[+0x3A8]` must still equal `00181DD0()`'s generation; a `byte[+0x370]` state byte (1..8) drives the inner jump table - state 2 decays `word[+0x364]` by 2 per pass, the mode-3/8/0xA arms test `word[+0x36A]` bits `0x10`/`0x8000` against `00254A70`/`002EF9F0(3)` and the `02EBD480`/`02F8F23C` flag tables, `byte[+0x373] == 0x63` forces state 0, and `003A7EE0`/`003A7050`/`003A7300` push float angles into the transform queue before `byte[+0x370]` advances; the mode-2 tail then runs a SIMD `pcmpeqb` scan over the `02F8F23C` byte table. The per-tick state stepper for the eight slot lists.

Interior anchor `0024BA50` (function `0024B9B0`).

`003A7050` (581 B) is the twin timer-decay channel the world tick runs on singleton `02F97348`: each armed bit of `+0x368` (0x1000/0x2000) subtracts the frame float from word `+0x35A`, and on expiry sweeps the 16-slot `02EBEFB0` table through `003334B0`/`00333740` before clearing the bit - live channels instead store remaining/total at `+0x35C`; then `003A8390` runs, the frame time accumulates into `[02EBEFB0+0x84]` (integer image at `+0x80`), every live slot is probed by `00332750` and evicted through `00333350`+`003697F0` when it fails, and the return flag reports whether any slot fired or the `02EBEF88` list changed.

Interior anchor `003A7213` (function `003A7050`).

`00333350` (91 B) is the 16-slot teardown the world tick's `003A7050` runs on a drained slot object: after `00332FA0` priming it walks the `rsi + i*8` pointer table and for every non-null entry calls `0046EE70` then `003697F0` before clearing the slot - the symmetric release of the table `00332750` populates.

Interior anchor `00333381` (function `00333350`).

`00332750` (1262 B) is the per-slot scheduled-marker executor `003A7050` probes each tick: when `[rdi+0x290]` is set a `00250000`/`001EDDA0` double gate can clear it and early-return 1; otherwise the frame float accumulates into `[rdi+0x8C]` (its integer image cached in a stack slot), the `[rdi+0x93]`-counted `0x30`-stride marker array at `+0xB0` is probed by `00332C40` and compacted by an `00861EBA` move when an entry leaves state 1 (`+0x260` reset, count decremented), each of the object's 16 pointer slots is ticked by `0046E990` - expired entries dispatch to `003A9070`/`003A8130` by their `+8`/`+0x10` keys and are freed through `0046EE70`/`003697F0` once absent from the `02EC0F88` shadow registry - and, gated on `02F97348` word `+0x378` bit 0x400, due markers of the `[rdi+0x80]` table (word `+0x18`/`+0x1A` deadlines against the `+0x88` clock, `+0x2C`-indexed payloads resolved by `0020E600`) fire through `003331A0`, with `[rdi+0x92]-1` published into `02F97348+0x388` on the first lane; the `+0x90`/`+0x91`/`+0x94`/`+0x98` flags and interval accumulator then chain `003A3E30`-resolved follow-on markers until the slot drains, returning 1 while work remains and 0 once empty.

Interior anchor `003329F0` (function `00332750`).

`003B2310` (337 B) is the flag-keyed async submit `003B25D0` arms once per record: while `02EBEBE4` is set it only stamps `[rcx+0x1C]` = 1 and returns 1; otherwise it derives the request kind from `[rcx+4]` - bit 0x1000 toggles the bit and adds `0x200`, bit 0x2000 toggles and adds `0x240`, bit 0x8000 forces `0x1FF`, and the literal `0xC3` falls back to `0x1FE` when `002DEBB0` reports clear - then retries `0032E400(0xC, kind)` through the `0x200`/`0x240` fallbacks until positive, and dispatches `0032E620` with continuation `003B22D0` on the `01FD4A30` context; the ticket lands in `[rbx+0x18]`, `[rbx+0x1C]` becomes 2 and `02EBEBE4` is armed.

Interior anchor `003B23AD` (function `003B2310`).

`002FC860` (323 B) is the once-armed async submit sibling of `003B2310` the `002FCF00` probe runs: with `02EC3D7C` armed it only remasks `[rcx+0x23]` (`& 0xF1 | 1`) and returns 1; otherwise the request index comes from the `02EC19C0` word table indexed by `[rcx+0x20]` while `02EC3D7D` permits, else from the `002DEBB0`-gated `0032E400` probe of kinds `0xB`/`0x26` with `0x78..0x89` and `0x8A..0x99` band clamps applied before each retry, and the dispatch goes through `0032E620` with continuation `002FC830` on `01FD4A30` - storing the ticket at `[rbx+0x18]`, writing `[rbx+0x23]` `& 0xF2 | 2`, and arming `02EC3D7C`.

Interior anchor `002FC8F8` (function `002FC860`).

`004308D0` (212 B) is the ease-shape dispatcher `00430B90` runs: `xmm2 == 0` returns `xmm1`; `(u16[+0xE] >> 4) & 0xF` selects from a `001309A4` jump table (`<= 5`) - arms compute `xmm1+xmm3`, `xmm1-xmm3`, `xmm3*2+xmm1-xmm2`, `xmm1*xmm3+xmm1` and the remaining polynomial blends - the per-record interpolation curve selector

Interior anchor `0043092D` (function `004308D0`).

`00197870` (186 B) is the flag-selected stat-field getter `001E0DC0` calls per record: byte `[rcx+0x3A]`'s bit1 or bit4 route to the `01F80970` table, bit2 to `01F80550`, both `dl * 0x15C`-sized rows; `r8b == 0` reads `dword[base + (dl*0x57 + r9)*4]` directly (a `0x57`-dword column inside the same row, `r9 < 0x10`), while `r8b == 1` reads `+0x48` when `r9 == 0`, else `+0x4C + (r9 & ~1) * 8` for `r9 < 8` - the two-lane accessor the field frame consults for packed record stats

Interior anchor `0019788D` (function `00197870`).

`002EB690` (171 B) is the queue relink `002EB5E0` runs when a frame flag transitions: `word[rcx + idx*2 + 0xE0]` accumulates `r8w`, `1 << cl` clears the `+0x2C` bit and sets it in `+0x48 + r9*4`; if the bit was absent from all of `+0x24`/`+0x28`/`+0x34` it also arms `+0x28` and the node relinks - any of `0215FD68`/`0215FD70`/`0215FD80` that named the node is advanced past `[+8]`, the node unlinks from its list, and it re-heads the `0215FD80` chain

Interior anchor `002EB6C7` (function `002EB690`).

`00290320` (34 B) is the five-arg forward thunk `0027DE30` and `00328530` call on the `0209BE80` manager: it spills `r9d` to `[rsp+0x20]` as a fifth argument, reorders `ecx -> edx`, `edx -> r8d`, `r8d -> r9d`, loads `rcx = [0209BE80]` and tail-calls `00291320` - a plain argument-shuffle into the manager's dispatcher.

Interior anchor `00290338` (function `00290320`).

`00290B90` (78 B) is the `+0x10F10` list sweep `0027DE30` and `00319140` call: it walks the `0209BE80` manager's node chain (`next` at `+0x868`), and for every node whose `dword[+0x810]` matches `ecx` it bumps `word[+0x850]` from `2` to `loopindex+3` (`r8d = eax+3`, `eax` counting hits) and latches `1` - a mark-all-matching pass over the manager's tracked set.

Interior anchor `00290BC4` (function `00290B90`).

`0028FA50` (22 B) is the free forwarder `003F24D0` and `003F7050` call: `rcx = [[0209BE80] + 0x10FC0]`, `rdx = arg`, tail `00273B40` - releases a node through the manager's `+0x10FC0` allocator object.

Interior anchor `0028FA5A` (function `0028FA50`).

`00291320` (667 B) is the `0209BE80`-manager dispatcher `00290320` shuffles into: `00273780` validates both id args, the `[rbp+0x10F10]` chain is walked for an existing `(+0x810, +0x814)` pair record (a `+0x840` mode match ending at `291564`), else `00273A30` carves an `0x890` record from the manager's `+0x10FC0` allocator (the pool batch-166's `0028FA50` free-forwarder serves), `00275550` zeroes it twice, fields `+0x838`/`+0x83C`/`+0x850` get `0x3E000000`/1.0f/1, `+0x810`/`+0x814` take the ids, `+0x7E8` gets the lazy `0024A5A0` child (`rbp+0x10F50`), and `00181540`/`00181250`/`00181000`/`00271140`/`002711E0` fill it from the word-offset name tables - the pair-record constructor the manager fan-in drives.

Interior anchor `002913B9` (function `00291320`).

`00332FA0` (141 B) is the slot teardown `00333350`'s tick machinery runs over its `0x30`-stride entries: for each populated slot `002DEE80` runs first, then `003B3EA0` with size `0x10` on the payload, the slot is zeroed, and the count byte is reset when the sweep ends - the prime/clear helper the world-tick timer channel reuses each pass.

Interior anchor `00332FDB` (function `00332FA0`).

## Interior citations for the entry-cited functions (FABLE, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's disassembly pack and re-read by FABLE against the certified image; verified by [`interior_applier.py`](../../_index/candidates/fable-the-world-tick-and-the-field-frame-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `00340970` | 118 B | takes `p = 002640C0()` (incoming registers still in place) and `v = 00267E10(r9)`, then calls `0025AE00(p, k, v)` for `k` = 0, 1, 4, 2 and tail-jumps to `0025AE00(p, 3, v)` | `0034097D`, `00340988`, `00340997`, `003409C7`, `003409E1` |
| `003DF810` | 208 B | scans the dwords from `02B59CDC` down to `02B59CC0` (indices 7 to 0) for the first non-zero value `v` at index `i`; when one is found calls `0029CAB0(dword 02B59CE0[i], v, qword 02B59C40[i], qword 02B59C80[i])` and stores those values in `02B59D14`, `02B59D10`, `02B59D00` and `02B59D08`; when none is found calls `0029CAB0(0, 0, 0, 0)` and zeroes qwords `02B59D00`, `02B59D08` and dwords `02B59D10`, `02B59D14` | `003DF832`, `003DF84B`, `003DF88D`, `003DF8AC`, `003DF8D4` |
| `003EB470` | 129 B | returns without work when `rcx` is null; otherwise calls `002ED470(dword +0x10)`, `002EB870(qword +0x18)` and `00265F90(rcx+0x10)`, unlinks `rcx` from its neighbours through qwords `+0` and `+8` (each side patched only when non-null) and zeroes both, then pushes it at the head of the list whose head qword is `02B5EB70` (`+0` = old head, `+8` = `02B5EB70`, the old head's `+8` = `rcx` when non-null) and clears byte `+0x40` | `003EB485`, `003EB497`, `003EB4AD`, `003EB4C9`, `003EB4E7` |
| `003EF750` | 20 B | tail-jumps to `00244F50(0x108, 003EF830, 0)` | `003EF753`, `003EF75A`, `003EF75F` |

## Homed bodies re-homed here for host fit (FABLE, 2026-10-03; move drafted by OPUS)

*Each body below was homed on another page by FABLE's homing stream (cloud-drafted, FABLE-verified). SWE2-AUDIT-SPEC reviewed its sentence, site and anchors exact, and rejected only the host: that page cites the caller as a foreign or boundary mention (commit `4522aeff6`). The row is moved here because this page cites the caller in its own text. The sentence is unchanged except where `moves.json` records a bits-as-values edit. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Verified by [`move_rows.py`](../../_index/candidates/opus-fable-home-host-moves-1003/move_rows.py): every site transfers to its function, this page cites the caller outside this section, and every anchor is an instruction boundary inside its function that decodes to the recorded mnemonic.*

| function | size | entered from | what the body does | interior anchors | moved from |
|---|---|---|---|---|---|
| `003EBD70` | 78 B | `002628B0` + 0x1CD | stores 0 in qword `02B5EC60`; when qword `02B5EC68` is non-null, makes the call at `003EBD70` + 0x1B with it and stores 0 there; then stores 0 in qwords `02B5EC70`, `02B5EC78`, `02B5EC80` and `02B5EC88` and returns 0 | Interior anchor `003EBD7B`; Interior anchor `003EBD8B`; Interior anchor `003EBD90`; Interior anchor `003EBD9D`; Interior anchor `003EBDB2` | [CONTRACT-ui-request-router](../../16-UI/CONTRACT-ui-request-router.md) |

## Homed bodies re-homed here for host fit (FABLE, 2026-10-03; AUDIT-SPEC batch 4)

*Each body below was homed on another page by FABLE's homing stream (cloud-drafted, FABLE-verified). SWE2-AUDIT-SPEC reviewed its sentence, site and anchors exact, and rejected only the host: that page cites the caller as a foreign or boundary mention (commit `95d495604`). The row is moved here because this page cites the caller in its own text. The sentence is unchanged. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Verified by [`move_rows.py`](../../_index/candidates/fable-home-host-moves-b4-1003/move_rows.py): every site transfers to its function, this page cites the caller outside this section, and every anchor is an instruction boundary inside its function that decodes to the recorded mnemonic.*

| function | size | entered from | what the body does | interior anchors | moved from |
|---|---|---|---|---|---|
| `0036F510` | 18 B | `0022A770` + 0x12F | calls the site `0036F510` + 0x4 with the incoming registers, then tail-jumps at `0036F510` + 0xD with no argument set up between the two, returning what that target returns | Interior anchor `0036F514`; Interior anchor `0036F51D` | [active-party-reserve-and-the-moment-the-leader-changes](../../11-Party/active-party-reserve-and-the-moment-the-leader-changes.md) |
| `00314820` | 18 B | `0022A770` + 0x1D8 | calls `00314820` + 0x4 with the incoming registers unchanged, then tail-jumps (+ 0xD) without setting up any argument or reading the call's result | Interior anchor `00314824`; Interior anchor `0031482D` | [keymap-ini-file-format-and-default-controls](../../15-Input/Binding-Profiles/keymap-ini-file-format-and-default-controls.md) |

## Homed bodies: functions reached only indirectly whose callees this page cites (FABLE, 2026-10-03, F homing)

*No page cited these functions and none of their callers is documented: they are reached by table or pointer dispatch or through undocumented callers. Each one calls something this page documents, which the sentence names. Each sentence states what the body does (access and representation, not purpose); the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's F homing pack and re-read by FABLE against the certified image; verified by [`interior_applier.py`](../../_index/candidates/fable-the-world-tick-and-the-field-frame-homing-1003/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `002DF1E0` | 54 B | when `edx` is 0 or less (signed) tail-jumps to `001DBF00(1, 0, ecx, r8d)`; otherwise makes the call at `002DF1E0` + 0x2C with (1, 0, `ecx`, `edx`, `r8d` as the fifth stack argument) and returns its result | Interior anchor `002DF1E6`; Interior anchor `002DF1F7`; Interior anchor `002DF1FF`; Interior anchor `002DF20C` |
| `002EC630` | 74 B | returns 0 when `rcx` is null or dword `[rcx]` is -1; otherwise, when word `[rcx]` is not `0xffff`, forms the record at qword `022C6F28` + sign-extended word * 0x740 and, when that pointer is non-null and its dword `+0x284` is non-zero, calls `00426E20` on it; returns 1 on every path past the first guard | Interior anchor `002EC639`; Interior anchor `002EC641`; Interior anchor `002EC64B`; Interior anchor `002EC65B`; Interior anchor `002EC664` |
| `003EB190` | 111 B | does nothing when `ecx` is above 0x1f (unsigned); otherwise, when qword slot `02B5EA20[ecx]` (stride 8) is non-null, calls `003EB470` on it and clears the slot, then stores into the slot, and returns, the result of the call at `003EB190` + 0x52 with (`rdx`, `r8d`, `r9d`, the fifth (stack) argument) | Interior anchor `003EB193`; Interior anchor `003EB1C9`; Interior anchor `003EB1CE`; Interior anchor `003EB1E2`; Interior anchor `003EB1F1` |
| `00473490` | 43 B | calls `00466C40(ecx)`, then the call at `00473490` + 0x17 with the same `ecx`, and returns in `xmm0` the second float minus the first | Interior anchor `0047349D`; Interior anchor `004734A7`; Interior anchor `004734AC` |
| `004734C0` | 46 B | calls `00466BB0(ecx)`, then `00466C40(ecx)`, and returns in `xmm0` the first float minus the second | Interior anchor `004734CD`; Interior anchor `004734D7`; Interior anchor `004734DC`; Interior anchor `004734E0` |

## SWE2-EC7-217 update (2026-10-03) - the nearfade override bytes `02099DA4`/`02099DA5`

`0026AB50` (13 B) writes the two override bytes that the `0025D950` row above reads: it stores `cl` at byte `02099DA4` and `dl` at byte `02099DA5`, and returns. It is reached by tail jumps from two verb handlers. `set_force_char_nearfade` `0x0552` passes 1 and the popped integer; `clear_force_char_nearfade` `0x0553` passes 0 and 0. While the flag `02099DA4` is set, `0025D950` therefore stores the script's byte `02099DA5` in `02099DA3` in place of the value it computed, and passes it sign-extended to `002E8700`.

Interior anchor `0026AB56` (function `0026AB50`).
