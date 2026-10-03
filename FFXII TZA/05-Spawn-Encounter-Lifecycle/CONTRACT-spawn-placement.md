---
contract: choose where a spawn appears relative to the party leader - an authored point validated against an arc and a distance band, or a random point filtered only by field-region containment
category: 05-Spawn-Encounter-Lifecycle
scope: subsystem
readiness: BEHAVIORALLY UNDERSTOOD
confidence: PROVEN
implements: 05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md
entries: ["00234AF0", "003209C0", "00234DA0", "00265200", "00316DA0"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: the placement modes, the return window and the polar construction are the page's reading
    with site citations; the modded-settings behaviour is ASTRA's falsification package. OPUS
    assembled and scoped this contract on 2026-09-20 and did not re-derive the bodies. RE-DERIVED
    2026-09-29 (OPUS, falsification pass 1, falsify_spawn_placement.py P0-P8) - see the end of this page.
last_reviewed: 2026-09-29
audit:
  by: OPUS
  date: 2026-09-20
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-spawn-placement-falsification-pass-1
---

# Contract — spawn placement and the return window

> **Provenance, stated once.** **[page]** marks what is carried from
> [the spawn page](spawn-placement-and-retirement.md). **[FALSIF]** marks ASTRA's
> `spawn-lifecycle-falsification` package (methods A and B, no live game, 2026-09-12). **[live]**
> marks what only a running game settles.
>
> **A live record was deliberately NOT cited.** `EXP-080` is live (`live_game: true`, method C,
> COMPLETE) and sits in this subsystem's evidence directory, but it is about an older save
> restoring battle state and **touches no placement body**. Citing it would have given this
> contract a live runtime row it has not earned.

## 1. Purpose

When an encounter spawns, something has to decide **where**. That decision is made relative to the
**party leader**, either by validating a position the field data authored or by drawing one at
random inside an arc in front of them.

## 2. Interface

| | |
|---|---|
| choose a position | `Spawn_TrySelectCandidatePosition` (`00234AF0`), candidate index in `ECX` **[page]** |
| fetch the candidate | `FieldData_CopyFormat0Candidate` via `003209C0` — **0 on success, −1 on failure** **[page]** |
| return window | `SpawnKeep_GetReturnWindow` / `SpawnKeep_SetReturnWindow` **[page]** |
| returns | non-zero placed, `0` not placed **[page]** |

## 3. Types

The format-class-0 candidate record: **byte `+0x00` selects the mode**, `+0x10` carries the
authored position **[page]**.

## 4. Preconditions · postconditions · invariants

**I1 — A NEGATIVE RETURN WINDOW RESTORES THE DEFAULT, IT IS NOT AN ERROR.**
`SpawnKeep_SetReturnWindow` is `test ecx,ecx / mov eax,0x12C / cmovs ecx,eax`: **strictly negative →
300**. It is neither rejected nor clamped to zero. **The unit is seconds**, multiplied by the frame
rate before comparison with a raw tick delta **[page]**.

**I2 — THE CALLER REJECTS A NEGATIVE RETURN, NOT A ZERO ONE.** `003209C0` returns **0 on success**
and **−1 on failure**, and the placement code tests for negative. A reconstruction that treats
`0` as failure inverts the whole path **[page]**.

**I3 — THE TWO MODES ARE EXCLUSIVE, AND THEY ARE VALIDATED DIFFERENTLY.** Branching on the
record's first byte:

* **POINT mode** — the authored position is used, gated by an **arc test** about the leader's
  heading, `|wrap(leaderYaw − toCandidate)| ≤ (arcDeg / 2) · 2π / 360`, and **then** by the
  distance-band validator.
* **AREA mode** — a position is **drawn at random**: `r = (RNG() % ((max−min)·100)) / 100 + min`,
  `θ = wrap(leaderYaw + ((RNG() % arcDeg) − arcDeg/2) · 2π/360)`, and **the only filter is whether
  it lands inside the field region**. **No distance validation runs in area mode** **[page]**.

**I4 — THE LEADER ALONE IS CONSULTED, NOT THE PARTY.** `BattleUnit_GetPartyLeader`, and a null
leader returns 0. **No other party member is considered** in the radius calculation **[page]**.
*Made exact 2026-09-29 (OPUS, falsification pass 1). Point mode's band reaches the leader through a slot walk:
`00234DA0` measures to the party-focus slot among 0-3, and that is the handle `003272A0` resolves. So the leader
must also be one of those slots and pass their status gate, or point mode returns 0.*

**I5 — AN EMPTY BAND IS REFUSED FIRST.** `max_radius − min_radius == 0.0` → `0`, before the
candidate is even fetched **[page]**.

**I6 — AREA MODE DOES NOT PUBLISH `out_observed`, AND THE AUTOMATIC CALLER READS ITS SLOT ANYWAY.**
The same uninitialised-read shape found elsewhere in this engine: the producer leaves the slot
untouched on one path while the consumer reads it regardless **[page]**.
**RULED 2026-09-25 (FABLE, Claude Opus 5.5), on `FABLE-REQ-OPUS-S16-I6-SLOT-GATES-ACCEPTANCE`: the slot is consumed
meaningfully. It decides whether a successful candidate is accepted.** **[static]**
- **The caller's use.** The automatic caller `Spawn_SelectAndPrepareAutomaticEntry` passes a stack slot as
  `out_observed`. When the placement returns non-zero it reads the slot back and compares
  it with the threshold `[02F973B8]`, loaded once into `xmm6` at entry. A value **below** the threshold accepts
  the candidate. Otherwise the attempt counts as a miss and is retried, up to `[0208D457]` times.
- **Nothing else writes the slot.** The caller never writes that slot. The placement writes it only on the point
  path, and only when the unit is the party focus (`PartyFocus_IsCurrentPackedActorHandle`, the page's §11
  pseudocode).
- **So two cases read a value this call did not produce:** the area path, and the point path for a non-focus unit.
  They read the value left by an earlier point-mode call in the same loop, or older stack contents. If it is not
  below the threshold, every successful candidate on that path is refused and the loop exhausts its retries.

*Not established:* which values the slot holds in ordinary play. That is `L-12`'s live question on the page.

**I7 — THE POLAR CONSTRUCTION DOES NOT WRITE `Y`, AND THE CALLER COPIES THE UNWRITTEN LOCAL.** Only `X`
and `Z` are set; **what supplies the vertical coordinate is unresolved** and recorded as `L-7`
**[page]**. **NARROWED 2026-09-25 (OPUS), consuming EXP-145:** `00319390` writes `[rdx]` and
`[rdx+8]` only (`00319411`, `00319415`); `00234AF0` hands it `rdx = rsp+0x50` (`00234CB2`) and later
copies `[rsp+0x54]` into `result.y` (`00234CDD` → `00234CF2`) with **no write to `rsp+0x50..0x5B`
anywhere in its body**, and `FieldRegion_ContainsWorldPosition` (`002374E0`, handed the same buffer)
makes no memory write of its own. So in area mode **`result.y` is uninitialised stack** — EXP-145
observed its `0xCD` fill replacing an authored `y = 7.5` **[exec]**, and the static read agrees
**[static]**. Whatever supplies the real `Y` runs **downstream** of `00234AF0`.

**I8 — the trig is a table, and its convention is shared.** A **32,768-entry** sine table at
`01F004E0`, indexed `(θ/2π)·scale & 0x7FFF`, with `cos = sin[(0x2000 − i) & 0x7FFF]`. The
convention `X = sin(θ)·r, Z = cos(θ)·r` is **identical** to `Movement_ComputeDeltaFromHeadingSpeed`,
and `Vector3_ComputeXZHeadingOrFallback` is its exact inverse `atan2(dx, dz)`, falling back to the
supplied heading when the two points coincide **[page]**.

## 5. State

`g_nSpawnKeepReturnWindow` (seconds, default 300), the authored format-class-0 candidate records,
and the sine table at `01F004E0`. *Added 2026-09-29 (pass 1):* the arc width `arcDeg` is the global `02089358`. It is read only by `00234AF0`, stored as
180 by `0023A520`, and set by script through `VM_Spawn_SetCandidateHeadingArcDegrees` (`0050F470` → `0023A1F0`).
The verbs are `btlAtelSetupActorStart` and `btlAtelSetSpawnLimitDegree`. Their zone census, including the two zones that
open the arc to 360°, is on [the tunables page](spawn-placement-height-and-authored-tunables.md).

## 6. Relationships

`00265200` reads the leader's class-dependent heading; `00316DA0` wraps an angle;
`FieldRegion_ContainsWorldPosition` is area mode's only filter; the distance validator is point
mode's **[page]**.

## 7. State transitions

```
place(candidateIndex):
    if (max - min == 0.0)                      return 0        (I5)
    if (003209C0(candidateIndex, &rec) < 0)    return 0        (I2)
    leader = GetPartyLeader(); if (!leader)    return 0        (I4)
    if (rec[0] == 0)   POINT: arc test, then distance band     (I3)
    else               AREA:  random r,theta; region test only (I3)
```

## 7a. Range retirement, the return window and the keep-bank rotation (FABLE, 2026-10-03)

*Added for SWE2-AUDIT-SPEC's SCOPE-SHORT on S-16 ([`auditspec-l2-expansion-1003`](../_index/candidates/auditspec-l2-expansion-1003/README.md) item 3): the
registry subject is "spawn placement, the keep window and retirement", and §1–§7 contract only the placement. Static and
isolated original-code; every fact below is checked by [`check_s16.py`](../_index/candidates/fable-l2exp-s16-mech-1003/check_s16.py) (FAILS 0).
The mechanisms are described on [the spawn page](spawn-placement-and-retirement.md) §2 ("Retirement — two opposite senses",
"The persistence banks") and [the respawn page](why-the-enemies-you-killed-come-back.md); the keep entry's bytes are
[the field map](Spawn-Record/the-spawn-keep-entry-field-map.md)'s. What retirement does to the group ledger is
[the group contract](CONTRACT-group-completion-and-respawn.md)'s §6 and §10 ("Range retirement is not a death"), and is
not restated here. This section states the trigger, the two senses, the mark retirement leaves for the selector, and
when the banks are kept.*

**Interface.** Two entries, each with one caller.

| entry | its one caller | when it runs |
|---|---|---|
| `SpawnLifecycle_CheckAndRetireByNativeRange` `002350C0(actorWork)` → 1 retired, 0 kept | `00234022` in `BattleUnit_UpdateLifecycleAndCombatFrame` `00233F70`, with `rcx = [unit+0x10]` (`0023401E`) | once per field-runtime pass for each bound unit whose callback runs: `00233F70` is named only by `lea r13` at `00265A4F` and stored at record `+0x38` (`00265AA8`); the drive loop calls it at `0025E222` ([the world-tick page](../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md) §2.4). Inside, only on the ACTIVE branch: unit flag bit 3 set, bit 16 clear, bit 4 set (`00233FAD`–`00233FC3`) and the stats status gate passed (`00233FD8`–`00233FEC`) |
| `SpawnKeep_RotatePersistenceBanksForAreaTransition` `00233780()` | `00234423` in `BattleSystem_InitializeAreaState` `002342F0` (chained body `002343CD`) | once per area initialisation, on both arms of `002343CB`, unless `[02089300]` is 0 (`002342F4`). It runs after the area's reset route `00239960` (`00234349`). `002342F0`'s callers are `00267136` and `0026CEC6` |

The return window `0208936C` has a getter `00235330` and a setter `00235340` (§4 I1). Each has one caller, a script
verb wrapper: the getter `00510819` in `00510810`, the setter `00510802` in `005107F0` (verb `0x306C`
`btlAtelSetMapJumoKeep`).

**Reads and writes.**
- **The retire reads** the record's `+0x0D` bit 6 through `002672F0` (`002350DE`), the unit's mode byte `+0x50`
  (`00235104`, `00235162`), its anchor index `+0x51` (`0023518A`) and threshold `+0x4C` (`0023519C`), the stats record
  `[unit+0x698]` (`+0x05`, `+0x3C`, `+0x64`), the keep entry's flag bit 4 (`00235159`), and the global range
  `02089368` (`00235205`, its only reader).
- **The retire writes** the keep entry's flag bit 0 (`002352A6` `or dword ptr [rcx], 1`), then calls
  `BattleUnit_TeardownAndDespawn(unit, 1)` (`002352B1`) and `00306E60(unit, 0)` (`002352BB`).
- **The opt-in bit is the drive loop's.** The loop clears record `+0x0D` bit 6 at `0025E1AD` and sets it at `0025E217`,
  just before it calls the record's `+0x38` callback. The unit is record `+0x30` (`00263E30`), and unit `+0x10` is the
  record (the binder `002344EF`, `002134A0`). So the opt-in gate reads "this record's callback was scheduled in this pass".
- **Who sets the inputs.**
  - The global range `02089368` is written by `0023A1D0` (verb `0x300B` `btlAtelSetSpawnDistance`, `0023A1E0`) and by
    `0023A520`, which installs 43.0 (`0023A540`, verb `0x3053`). It is BSS, so it is 0 until one of them runs.
  - The mode, threshold and anchor are written by `00238FC0` (verb `0x3019` `btlAtelSetDeSpawnType`). It stores the
    mode always (`00238FE1`), but the threshold and anchor only for mode 2 (`00238FE4`–`0023900B`).
- **The rotation reads**:
  - the bank pointers `[0208E690]` and `[0208E698]` (`0023378D`, `0023379B`);
  - the field id from `003148F0` (save-image payload `+0x1044`, clamped to `>= 0` at `00314903`);
  - the clock through `0032A150`;
  - the previous-field word `02089372`, sign-extended (`002337CD`);
  - the stamp `02089374` (`002337F0`), the scale `[01DFE0B8]` × 30.0 (`002337DE`, `002337E8`), and the window
    (`002337FA`, its only native reader).
- **The rotation writes**:
  - both banks' contents;
  - the parity byte `0208D454` (`00233933` and `002339C6`);
  - on a wipe, the 64 u16 counters at `0208D354 + parity × 0x80` (`002339CC`–`002339E2`);
  - the history and the stamp, in its tail: `02089372 = 02089370` (`00233A11`), `02089370 = field` (`002339F4`) and
    `02089374 = clock` (`00233A03`).
- **The history and stamp have three writers in all**: that tail, the reset `00237DF0` (stamp 0 at `00237E53`, both
  words −1 at `00237E5D`/`00237E64`), and the slot-0 restore `00233550`, which writes the two field words only
  (`002335BC`, `002335C7`). The serializer stores only the field words (`00233529`, `00233533`). **The window and the
  stamp are in no save.**

**Invariant I9 — one trigger, two opposite senses.** `002350C0` refuses, in order, at each of these:
- the opt-in bit (`002350E5`);
- a null unit or mode 0 (`002350FE`, `00235108`);
- a stats record with `+0x05 == 0` (`00235120`);
- unit flag bit 4 clear, or no stats record (`00235129`, `00235132`);
- the `0x80000003` status mask without the field's bit-15 waiver `00313F60` (`0023513E`–`0023514C`);
- the keep entry's inhibit bit 4 (`00235159`).

It then splits on the mode byte (`00235173`–`0023517B`):
- **Mode 1 — leave and it goes.** For slots 0–3 (`0031B810`; loop bound `0023528D`), each eligible slot is checked. A
  slot is eligible when its flag bit 4 is set, it has a stats record, the status gate passes, and it is the party focus
  (`003273B0`). The unit is **kept** if any eligible slot is strictly nearer than the range: `comiss xmm6, xmm0` / `ja`
  at `0023527D`, squared XZ through `0031E620` → `003A1960`. It **retires** when at least one slot was eligible and
  none was nearer (`00235292`). At exactly the range it retires.
- **Mode 2 — come near and it goes.** It needs the leader (`003272A0`) and the anchor from `00320940(unit+0x51)`, which
  must not be negative (`0023519A`). It **retires** when the leader's squared XZ distance to the anchor is at most
  `(+0x4C)²`: `comiss xmm0, xmm6` / `jbe` at `002351B6`/`002351B9`.
- **Any other mode** returns 0.

The executed cases (K7, Unicorn 2.1.4):

| mode | setting | case | result |
|---|---|---|---|
| 1 | range 43 | focus member at 10 | kept |
| 1 | range 43 | focus member at 43 | retired |
| 1 | range 43 | focus member at 50 | retired |
| 1 | range unset (0.0) | focus member at 0.5 | retired |
| 2 | threshold 6 | leader at 5 | retired |
| 2 | threshold 6 | leader at 6 | retired |
| 2 | threshold 6 | leader at 7 | kept |
| 1 or 2 | — | an unordered (NaN) distance | retired |

**Invariant I10 — retirement leaves a mark, and it is the only teardown that keeps one.**
- The retire sets keep-entry bit 0 (`RANGE_REENTRY_PENDING`) **before** it tears the unit down. It passes the
  teardown's second argument as 1 (`002352A9`). For a unit with a keep record, `00300E40` calls the record clear
  `00237080` (`and dword ptr [rcx], 0xFFFFFF7A`: bits 0, 2 and 7, `00237085`) only when that argument is 0
  (`00300F5D`–`00300F68`).
- `00300E40` has ten call sites. The retire's `002352B1` is the only one that passes 1; the other nine pass 0
  (`xor edx, edx`). That includes the idle teardown in the same frame function (`002340FB`/`00234100`). So a unit that
  dies, despawns or is torn down by any other route loses bit 0, and a retired one keeps it.
- Executed (K7h): the record's flags are `0x03` when the teardown is entered. Then the unregister runs with `edx = 0`,
  and the call returns 1.
- **The mark's consumer is the automatic selector.** `00235720` tests the death limit first (`002358A1`–`002358B0`).
  For an entry whose bit 0 is set, it then skips the cooldown test (`002358B9`/`002358BB` → `002358DD`). A retired
  entry is therefore re-admitted **without a cooldown**. Retirement is not a death (the group contract §10), and
  `002350C0` itself writes neither the death count `+0x08` nor the stamp `+0x0C`.
- The script view `SpawnEntry_QueryRangeReentryPending` `00236670` has one caller, verb wrapper `0050FC90`
  (`btlAtelGetRespawnCause`). Its "bit 1 set and bit 2 clear" condition is the field map's §2.3.

**Invariant I11 — the banks are kept only on A → B → A inside the window, and the test is unsigned.**
- `00233780` restores when both of these hold:
  - the entered field equals `02089372`, the field from **two** transitions ago (`002337D6`);
  - `(uint32)(clock − stamp) <= (uint32)((int)(30.0 × scale) × window)` (`002337F0`–`00233803`, `ja` to the wipe).

  Otherwise it wipes.
- **Restore** exchanges the two banks' **contents** through a `0x9400`-byte stack buffer: bank 2 → stack, bank 1 →
  bank 2, stack → bank 1. The pointers stay where they are. The parity is flipped (`00233933`), and the counters are
  not touched.
- **Wipe** copies bank 1 over bank 2 and zeroes bank 1 with one `memset(bank1, 0, 0x9400)` (`002339B0`). It flips the
  parity (`002339C1`/`002339C6`) and sets the 64 counters of the **new** parity's half to 1 (`rep stosw`, `002339E2`);
  the other half is left alone.
- **Both branches** then shift the history and stamp the clock (`002339E5`–`00233A11`).
- A null bank pointer returns before all of this (`00233795`, `002337A3` → `00233A18`): the history, stamp and parity
  stay as they were.

Executed (K6, Unicorn 2.1.4):

| case | result |
|---|---|
| A → B → A after 4,500 of 9,000 ticks | contents exchanged, pointers kept, parity 0 → 1, counters untouched |
| elapsed 9,000 ticks | restores |
| elapsed 9,001 ticks | wipes |
| scale 2.0 | the limit is 18,000 ticks |
| a third field | wipes; counters at `0208D3D4` set to 1, those at `0208D354` untouched |
| entering B again from B (field == last) | wipes |
| a stamp later than the clock | wipes (`FFFFFC18 > 9000`) |

**Invariant I12 — the window is a native constant in shipped play, and a reset always breaks the chain.**
- The window's writers are `002368D0`, which stores 300 (`00236A0D`), and the setter. The setter is reachable only
  from verb `0x306C`, and no shipped US script calls it ([the tunables page](spawn-placement-height-and-authored-tunables.md),
  0 of 1,114). So in shipped play the window is **300 s at either frame rate**.
- The window and the stamp are never saved. After `00237DF0` the previous-field word is −1. `003148F0` never returns
  a negative id, so **the first rotation after any reset wipes**. The executed fields 0, 1 and `0x7FFF` all wipe (K6e).
  The only exception is when the slot-0 restore `00233550` rewrites the two words before that rotation.
- One consequence: a `-2` request makes area initialisation run the reset (`00239960`, reached at `00234349`). That
  happens before the rotation at `00234423` in the same call, so the request also wipes bank 1, unless the slot-0
  restore intervenes.
- What a slot-0 load imports into bank 2, and what the restored stamps then mean to the cooldown, is the staged S-17
  section 10a's G9d ([`fable-l2exp-s17-mech-1003`](../_index/candidates/fable-l2exp-s17-mech-1003/section.txt)); it is
  not restated here.

**Failure paths.**
- **An unset range retires a mode-1 unit at once.** This happens when a zone sets mode 1 through `0x3019` and never
  runs `0x3053` or `0x300B`: the range is 0.0 and nothing is strictly nearer. The tunables page measures that every
  shipped script that defines a unit calls `0x3053` first, so in shipped play this needs a modified script.
- **A party with no eligible focus slot never retires a mode-1 unit.** This covers a leader outside slots 0–3, or one
  that is status-gated without the waiver. **Mode 2 never retires** when the anchor fetch fails or there is no leader.
- **An unordered distance retires in both modes**, so a NaN position despawns rather than keeps.
- **The inhibit bit 4** (`002391C0`) stops both modes.
- **A retired entry skips its cooldown** (I10). A reimplementation that routes retirement through the death path, or
  clears bit 0 in the teardown, changes respawn timing for every mode-1 and mode-2 unit.
- **A wipe is total.** Every keep entry's flags, death counts, stamps, enmity and stats page are zeroed in one
  `memset`; the field map's §2.5 lists what the entry carries. A restore brings all of them back.
- **A stamp later than the clock takes the wipe**, because the difference wraps. The reset zeroes the two together
  (`00237E37`, `00237E53`) and neither is saved, so this needs the 32-bit clock to wrap.

**Evidence class.**
- **Static:** K1–K5 of `check_s16.py`. They use the raw index in every form (E8/E9, 0F 8x, EB/7x, rip-relative,
  image-base-relative, pointer constants) and read whole bodies: `002350C0`, `00233780`, `00300E40`, `00237080`,
  `00238FC0`, `0023A1D0`, `0023A520`, `002672F0`, `003148F0`, `003A1960`.
- **Isolated original-code:** K6 runs `00233780` whole under Unicorn 2.1.4, with `003148F0`, `__chkstk` and `memset`
  answered by hooks. K7 runs `002350C0` whole, with the slot, focus, leader, position, anchor, waiver, teardown and
  unregister calls answered by hooks.
- **Sensitivity controls:** five, and each turns a check to FAIL:
  - `ja`→`jg` at `00233803`;
  - the compare reading `02089370` instead of `02089372`;
  - `jbe`→`ja` at `002351B9`;
  - the teardown argument 1→0 at `002352A9`;
  - the claim "an unset range never retires a unit 0.5 away".
- **Live: none.**
- **Not traced:**
  - which shipped scripts set mode 1 or 2 through `0x3019`;
  - whether the calls `00233F70` makes before `00234022` can change record `+0x0D` bit 6;
  - what the teardown's callees (`00300FC0`, `003105D0`, `00319E30`, `0023A570`) write in the keep entry;
  - whether the slot release `00234200` (bit 2) runs after a retirement;
  - the player-visible re-entry timing.

### Crossings into other layers (FABLE, 2026-10-03)

*The edges this section's citations add, each with what crosses it.*

- **CoreRuntimeScheduling — SERVICE (5 edges).**
  - The rotation `00233780` and the selector `00235720` read the clock through `GameClock_GetRawTickCounter`
    `0032A150` (`mov eax, [0208D45C]; ret`).
  - The reset `00237DF0` calls the clock's zero store `0032A160` (`00237E37`) and the one-store setter `00229ED0` (`00237E83`).
  - `BattleStorage_InitializeWorkArrays` `002368D0`, which installs the window (`00236A0D`), is called by the core
    runtime's startup hub `0022A0B0` (`0022A41A`).

  The spawn keep reads the core runtime's clock and is set up by its startup chain. The ownership is not shared.
- **Platform/Online/Achievements — CLIENT (1 edge).** The rotation's field source, `WorldTransition_GetActiveOrPendingFieldId`
  `003148F0`, is also called by `003160C0` (`003160F3`), so achievement logic reads the same field id. It is a shared getter, not
  shared ownership.
- **Resource — SERVICE (1 edge).** `002368D0` calls `003843F0` (`002369CE`), a 36-byte forwarder into `00384420` with constant
  arguments, while it sets up the work arrays. The spawn keep does not own it.
- **Save/Load/Settings — CLIENT and SERVICE (3 edges).**
  - The reset `00237DF0` is reached from the save-image rebind `SaveRuntime_RebindImageBackedGameplayState` `00238A80`.
  - `003148F0` reads the field id through `SaveImage_GetPersistentPayloadBase` `002EF2B0` (payload `+0x1044`).
  - `SaveImage_FinalizeHeaderAndChecksum` `00583D60` also calls `003148F0` (`00583F35`).

  The field id the rotation compares is save-image state; the window and the stamp are not (I12).

## 8. Script · resource · event interactions

The candidate records are **authored field data**; the script selects which encounter spawns, not
where it lands **[page]**.

## 9. Determinism

**Area mode is NOT deterministic** — it draws twice from the generator, once for the radius and once
for the angle, so placement consumes RNG state and **the draw count is part of the contract** in the
same way S-10's is. Point mode draws nothing. *(2026-09-29, pass 1: each draw is one call to `00328370`, which
steps the LCG three times, so an area placement advances the shared stream by six steps.)*

## 10. Failure paths and edge conditions

* **Empty band** (I5), **negative fetch** (I2), **null leader** (I4) → `0`.
* **Arc miss in point mode** → `0` without a distance test.
* **Region miss in area mode** → `0` without a distance test (I3).
* **`out_observed` unset in area mode** while the caller reads it (I6).
* **`Y` unwritten** (I7).
* **Two unguarded divisors in area mode** *(2026-09-29, pass 1, static)*: `(int)((max − min) · 100)` and `arcDeg`
  reach `idiv` untested. A band narrower than 0.01, but not exactly 0.0, and an arc of 0 divide by zero. A NaN band
  is not refused by I5 (`jp` proceeds).
* **MODDED SETTINGS CAN SKIP PLACEMENT ENTIRELY.** ASTRA's falsification found that **large modded
  attempt settings can skip choosing a position and accept old coordinates** — normal spawn rules
  survived the other checks **[FALSIF]**.

## 11. Observable behaviour

Foes appear in front of the party leader at a plausible distance. Under modded settings they can
appear where the last thing was (§10) **[FALSIF]**.

## 12. Reproduction formula

Implement §7 in order. **Take I2 literally** — `0` is success. **Do not add a distance check to area
mode**; the absence of one is the contract. **Do not initialise `out_observed` on the area path**
unless you also change the consumer, because I6 describes a real asymmetry rather than a bug to be
tidied. Draw exactly twice in area mode (§9).

## 13. Runtime validation

**EXECUTED — [EXP-145](../_experiments/EXP-145-spawn-placement-exec.md)** (method B, no live game;
SWE2-ORACLE; 20/20, stable ×3). `00234AF0` ran on shipped bytes in both modes with planted
field-data, leader and unit fixtures: I1's window (negative → 300, **zero NOT clamped**), I2's
`0/−1` fetch convention, I3's modes and region shapes (`1` box, `2` ellipsoid), I4's null leader
copying the authored position out **before** failing, I5's empty band refused before the fetch,
I7's unwritten `Y` (above), and §9's draw counts (point **0**, area **exactly 2**, including on a
region miss). **Consumed by OPUS 2026-09-25:** I7 was re-read statically and agrees; the other
verdicts are recorded as executed, not re-derived. *The section's former "No placement body has
been executed" is superseded by this record.*

What also exists is **ASTRA's `spawn-lifecycle-falsification`** (methods A and B, **no live game**), which
is genuine evidence *about this subsystem* and produced §10's modded-settings finding **[FALSIF]**.

**`EXP-080` IS NOT CITED, AND THE OMISSION IS DELIBERATE.** It is live, complete, and filed under
this subsystem's evidence — but it concerns an older save restoring battle state and **touches no
placement body**. An adjacent live record is not evidence for a mechanism it never ran.

~~UNLINKED / nothing-executed~~ — **LINKED to EXP-145** (2026-09-25). No exemption was ever added.

## 14. Unresolved

* **What supplies `Y`** — `L-7` (I7). **Narrowed, not closed:** nobody at this level; the area-mode
  `result.y` is uninitialised stack, so the supplier (a ground snap or similar) is **downstream of
  `00234AF0`** and not yet identified **[exec + static]**.
* ~~**Whether I6's uninitialised slot is ever consumed meaningfully**, or merely read and discarded.~~ **Ruled
  2026-09-25 (FABLE, Claude Opus 5.5): meaningfully.** It gates acceptance against `[02F973B8]` (I6). What values it
  holds in play stays `L-12` **[live]**.
* **Whether the modded skip is reachable unmodified** **[FALSIF]**.
* **No live evidence** for placement **[live]** — EXP-145 is original-code execution on planted
  fixtures, not a game session.

## 15. Evidence

The modes, the window, the polar construction and the shared trig convention are the page's
**[page]**; the modded-settings behaviour is ASTRA's **[FALSIF]**. This contract's contribution is
I1–I8 stated as a contract, §12's three "do not tidy this" notes, and §13's explicit refusal to
borrow an adjacent live record.

## 16. Parity plan

Test I2 first with a `0` return and assert **success** — a reimplementation that inverts it fails
everything downstream and looks like a data problem. Then point mode at the arc boundary, area mode
for region containment only, and **assert the generator advances exactly twice per area placement**
(§9). **Do not assert anything about `Y`** (I7) or about `out_observed` on the area path (I6): both
are contract holes, and a fixture that pins them would be testing the harness.

## SWE2-EC7-107 update (2026-09-20) - `00234DA0` measured

`00234DA0` (290 B) is the four-slot
range probe `00234AF0` and
`00308040` run: `edi = 0..3` walks
`0031B810(edi)` slots - each must
be live with `[+0x698]` populated
and pass the `([+0x64] | [+0x3C]) &
0x80000003` / `00313F60()` gate
(`r12d == 0` additionally requires
`003273B0(dword[+8])`); surviving
slots resolve a triple through
`00265020([+0x10], &out)` and score
it through `0031E620(rcx, &out)`,
which must fit inside the optional
`[r15]` lower / `[r14]` upper
bounds; `rbp` non-null with
`003273B0(dword[+8])` writes the
score to `[rbp]` and returns 1 -
the bounded placement probe the
spawn arms share.
Interior anchor `00234DE2` (the
first `0031B810` call).

Mechanical neighbours introduced by
this section's citations: the shared
helpers `00265020`, `00313F60`,
`0031B810`, `003273B0` and
`00308040` carry caller fan-in from
ActorEntity (24 edges), Gameplay
(11), Presentation (10), CombatAI
(9), UI (4), CombatFormula,
Status_Periodic_Terminal and
Rewards_Progression_Economy (3
each), Audio, Input and
Items_Equipment_Shops_License (1
each). These are edges of the
helpers, not of the placement
contract - noted so the audit
accounts for them.

## Falsification pass 1 — 2026-09-29 (OPUS): every invariant survives; the bodies re-derived, four facts added

**Attack.** The frontmatter said the bodies were never re-derived. This pass derives them. Every clause of §2-§10 became a
check that fails if the shipping image says otherwise. The checks decode every listed body in `.text`, so caller counts and
reference censuses are whole-image. Script: `Tools/analysis-kit/gfz-scripts/falsify_spawn_placement.py`, output
`falsify_spawn_placement.out`, image `73461d08…`, 0 BROKEN.

| # | Clause attacked | Killer | Result |
|---|---|---|---|
| P0 | §2 the interface | another caller, or other argument registers | **survives, made exact** (below) |
| P1 | I1 the negative window restores 300 | another body | **survives**: `test ecx, ecx / mov eax, 0x12c / cmovs ecx, eax`, cell `0208936C` |
| P2 | I5 before the fetch; I2 `js`; I4's null leader after the copy-out | another order or test | **survives**; a NaN band is not refused (`jp` proceeds) |
| P3 | I3 point mode's arc test, then the distance band | another comparison or unsquared bounds | **survives**: `|wrap(yaw − toCandidate)|` (`0031A930` ends in `andps`) ≤ integer `arcDeg / 2` × 2π/360; bounds squared by the caller |
| P4 | I4 "the leader alone ... no other party member is considered" | a band measured to a unit other than the leader | **survives, made exact** (below): the band walks four slots, but the one caller admits only the leader's |
| P4b | that the focus slot is the leader | the leader getter and the focus test read different handles | **survives**: both read `003590D0` |
| P5 | I3 area mode's formula and its one filter | another formula or a distance test | **survives, made exact**: both remainders are integer `idiv` (below) |
| P6 | §9 two draws in area mode, none in point mode | a third call, or a draw on the point path | **survives**, and each draw steps the LCG three times (below) |
| P7 | where `arcDeg` comes from | nothing; the contract did not say | **global state** `02089358` (below) |
| P8 | I7 the polar writer writes X and Z only; I8's table | a `Y` write | **survives**: `00319390` writes `[rdx]` and `[rdx+8]` through `01F004E0` with `& 0x7fff` and the `0x2000` offset |

* **P4: I4 survives, but its mechanism is a slot walk, not the leader pointer.**
  * Point mode's band is `Spawn_ValidateCandidateDistanceToPlayers` (`00234DA0`). It walks party slots 0-3 through
    `0031B810`, never calls the leader getter, and rejects on the first eligible slot outside `[min², max²]`.
  * Its ~~sixth argument~~ fifth argument (`00234AF0`'s sixth) decides eligibility *(corrected 2026-10-02, OPUS: `00234DC3` `mov r12d, dword ptr [rsp + 0xb0]` is the first stack argument; both callers store it at `[rsp + 0x20]`, `00234C2B` and `003080C0`; P0 below agrees)*. With 0, only the slot whose actor handle equals
    `PartyFocus_GetCurrentPackedActorHandle` (`003590D0`, through `003273B0`) is eligible.
  * `BattleUnit_GetPartyLeader` (`003272A0`) resolves that same handle. So with 0 the band is measured to the leader's
    own slot, and the one caller, `Spawn_SelectAndPrepareAutomaticEntry`, passes 0 (`mov dword ptr [rsp + 0x28], 0`
    before `00235950`).

  I4 holds for shipped play. What the slot walk adds is a failure path I4 did not state: the leader must also be one of
  slots 0-3 and pass the slot's status gate (`([+0x64] | [+0x3C]) & 0x80000003` → `00313F60`). Otherwise no slot is
  eligible and point mode returns 0. A non-zero flag, which no caller of `00234AF0` passes, would require every eligible
  slot inside the band. *A first draft of this pass read the slot walk as refuting I4. P4b, which pins the shared handle,
  withdrew that before publication.*
* **P0: the signature, exact.**

  ```
  00234AF0(ECX = candidateIndex, RDX = outPosition, XMM2 = minRadius, XMM3 = maxRadius,
           arg5 = out_observed (float *), arg6 = slotFlag)
  ```

  `ECX` reaches `003209C0` untouched. `out_observed` is `r14` (`[rbp + 0x77]`), handed to `00234DA0` as its `r9`.
  `slotFlag` is `[rbp + 0x7f]`, passed on as the validator's fifth argument.
* **P5: quantisation and two unguarded divisors.**
  * The radius is `(RNG % (int)((max − min) · 100)) / 100 + min`: `cvttss2si` truncates the divisor, so the radius comes
    in steps of 0.01.
  * The angle offset is `(RNG % arcDeg) − arcDeg / 2` whole degrees. For an even arc that is `[−arcDeg/2, arcDeg/2 − 1]`,
    one degree short on the positive side.
  * Neither divisor is tested. A band with `0 < (max − min) · 100 < 1`, or `arcDeg = 0`, reaches `idiv` with a zero
    divisor. I5 refuses only an exact `0.0`. *Static, not executed; §10 records it.*
* **P6: two draws, six LCG steps.** `RNG_SharedGameplayLCG_NextU32` (`00328370`) steps the `0x41C64E6D` LCG **three
  times** per call and stores once. It returns at most 31 bits, so the signed `idiv` never sees a negative dividend. An
  area placement therefore advances the shared stream by six steps. A reproduction that counts "two draws" as two LCG
  steps drifts. The point path's closure, 23 functions, draws nothing.
* **P7: `arcDeg` is global, script-set state.** The cell `02089358` is read only by `00234AF0`. Two functions write it:
  * `Spawn_SetCandidateHeadingArcDegrees` (`0023A1F0`), called only by the script verb's native
    `VM_Spawn_SetCandidateHeadingArcDegrees` (`0050F470`);
  * `0023A520`, which stores **180** (`0xB4`).

  §5 did not list it. It is recorded there now.
* **Currency.** The frontmatter's "did not re-derive the bodies" is superseded by this pass. EXP-145 remains the executed
  evidence.

Consumer record: [`_index/candidates/spawn-placement-falsification-pass-1-0929/`](../_index/candidates/spawn-placement-falsification-pass-1-0929/README.md).
No contradiction row: nothing the contract asserted was false.

## Cross-subsystem neighbours — SWE2-EC7 (pass-22 dispositions)

- **ActorEntity - CLIENT and SERVICE (38 edges).** `00265020` is also called by bodies filed to ActorEntity: `00236300`; `00234AF0`, `00234DA0` reach bodies filed to ActorEntity: `00265020`, `0031B810` - shared machinery across the layer boundary, no shared ownership.
- **Audio - CLIENT (2 edges).** `00265020`, `003590D0` are also called by bodies filed to audio: `00362850` - shared machinery across the layer boundary, no shared ownership.
- **CombatAI - CLIENT (14 edges).** `00308040`, `00313F60` are also called by bodies filed to combat AI: `00301830`, `00321850`, `00321B00` - shared machinery across the layer boundary, no shared ownership.
- **CombatAction - CLIENT (15 edges).** `00265020`, `00265200` are also called by bodies filed to combat action: `002F8060`, `00307300`, `00320E10` - shared machinery across the layer boundary, no shared ownership.
- **CombatFormula - CLIENT (3 edges).** `00265020`, `00313F60`, `0031B810` are also called by bodies filed to combat formula: `00384F40`, `00388D50` - shared machinery across the layer boundary, no shared ownership.
- **Gameplay - CLIENT and SERVICE (14 edges).** `00234DA0`, `00265020` are also called by bodies filed to Gameplay: `00308040` (Combat), `0031ADB0` (CombatAction), `00339630` (Combat); `00308040` reaches bodies filed to Gameplay: `0030B050` (Combat) - shared machinery across the layer boundary, no shared ownership.
- **Input - CLIENT (2 edges).** `00313F60`, `003590D0` are also called by bodies filed to input: `00253C70`, `00226BE0` (ActorControlMaskPropagationRuntime) - shared machinery across the layer boundary, no shared ownership.
- **Items_Equipment_Shops_License - CLIENT (1 edge).** `0031B810` is also called by bodies filed to items/equipment: `00309FB0` - shared machinery across the layer boundary, no shared ownership.
- **Movement - CLIENT and SERVICE (56 edges).** `00265020` is also called by bodies filed to movement: `0024B6F0`, `002E45E0`, `002EBFA0`; `00234AF0` reaches bodies filed to movement: `00265200` - shared machinery across the layer boundary, no shared ownership.
- **Party - CLIENT and SERVICE (20 edges).** `00265020` is also called by bodies filed to party: `00303CC0`, `00304180`; `00234AF0`, `00234DA0` reach bodies filed to party: `003272A0`, `003273B0` - shared machinery across the layer boundary, no shared ownership.
- **Presentation - CLIENT (22 edges).** `00265020` is also called by bodies filed to presentation: `002B7B80` (UI), `00322360`, `0037AD40` (EffectConstraint) - shared machinery across the layer boundary, no shared ownership.
- **RNG_Random_Selection - CLIENT and SERVICE (2 edges).** `00328370` is also called by bodies filed to random selection: `00308EC0`; `00234AF0` reaches bodies filed to random selection: `00328370` - shared machinery across the layer boundary, no shared ownership.
- **Rewards_Progression_Economy - CLIENT (3 edges).** `00265020`, `0031B810` are also called by bodies filed to rewards/progression: `002FB150`, `00312280`, `002F8BB0` - shared machinery across the layer boundary, no shared ownership.
- **Script_VM_Native_Bridge - CLIENT (50 edges).** `0023A1F0`, `00265020` are also called by bodies filed to script VM / native bridge: `0050F470`, `0033FD60`, `00344AF0` - shared machinery across the layer boundary, no shared ownership.
- **Status_Periodic_Terminal - CLIENT (3 edges).** `00313F60`, `003273B0` are also called by bodies filed to status/periodic terminal: `00320450`, `00329A20`, `00310DB0` - shared machinery across the layer boundary, no shared ownership.
- **UI - CLIENT (7 edges).** `00265020`, `00265200`, `00313F60` are also called by bodies filed to UI: `003C5130`, `0031EB20`, `00322A80` (BattleMenu) - shared machinery across the layer boundary, no shared ownership.
- **World - CLIENT (2 edges).** `003590D0` is also called by bodies filed to World: `0025E400` (ActorManager), `002623A0` (ActorManager) - shared machinery across the layer boundary, no shared ownership.
- **WorldAreaField - CLIENT and SERVICE (6 edges).** `00313F60` is also called by bodies filed to WorldAreaField (world area): `00234590`; `00234AF0`, `00234DA0` reach bodies filed to WorldAreaField (world area): `002374E0`, `003209C0`, `00313F60` - shared machinery across the layer boundary, no shared ownership.

## Interior citations for the entry-cited functions (OPUS, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../_index/candidates/opus-contract-spawn-placement-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `0023A1F0` | 11 B | converts the float in `xmm0` to a 32-bit integer with truncation at the entry and stores it to dword `02089358`, returning that integer in `eax` | `0023A1F4` |
