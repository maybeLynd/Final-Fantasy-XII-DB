---
system: Spawn placement, retirement and the keep window
category: 05-Spawn-Encounter-Lifecycle
status: DOCUMENTED — owner re-status 2026-10-01 (OPUS, for FABLE; documented_rule READY-WITH-POINTER): FABLE's 2026-09-30 conditions are met - a fresh graph audit of this page reports 0 findings (_index/candidates/opus-spawn-restatus-1001/xref_report.md) and the DD pass is read. History: REOPENED 2026-09-12 by ASTRA's independent falsification (§11), whose corrections are integrated; the two rows it opened are closed as L-12 SUPERSEDED (2026-09-26) and L-13 SUPERSEDED (2026-09-27), and L-13's live-only residue is routed for a runtime carrier (§7)
owner_layer: PrimaryOwner:Spawn_Encounter_Lifecycle
evidence_tier: 1
verified_against:
  gzf_sha256: 2ed8affb732f0def0a7852e0788298ae36b81206099dd1712f59825fc1c00bb9
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: additive-annotation across GN158 -> GN161 - every step of the certified lineage is additive on the canonical record (internal 38161, owner 9409 and finalNo 585 constant at all five generations; each step's codeDomain and explicit rise equals its unresolved fall). Of the functions classified since GN158 this document cites `003BA7B0`, `004058E0`; the 21 classified before GN160 are named in AUDIT-LOG's batch records and not in a tracked machine-readable list, so identity is not claimed. Voided by any delta that removes or rewrites a comment, tag, name, prototype or body range.; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md, lineage extension (twenty ledger figures across five generations)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  snapshot_sha256: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-30
audit:
  passes: 3
  last_pass: 2026-09-12
  last_pass_state: ASTRA independent falsification; signed attempt byte, output state and one-bank restore corrected; consumer propagation and remaining caller questions open (§11)   # <- corrected 2026-10-02, OPUS - superseded by the status line (2026-10-01); L-12 and L-13 are SUPERSEDED, section 7
  crossref_clean: true
  reopened_count: 5
---

# Spawn placement, retirement and the keep window

> How authored settings place monsters near you, why they vanish when you walk far enough
> away, and why turning around quickly finds the same ones still there.

**Status raised from `PARTIAL` to `DOCUMENTED` on 2026-09-02.** Every function in §3 has now
been read at tier 1; the earlier version rested on GFZ annotation for all but two accessors, and
several of those annotations turned out to be wrong. See §8d.

*Reconciled 2026-09-30 (FABLE): that raise is history. The page went back to `DOCUMENTED` on 2026-09-12 (§8g) and
was reopened the same day by ASTRA's independent falsification (§11); the current status is the front-matter line.*

## 1. What the player sees

Four behaviours a player notices without ever thinking about them.

**Some placements use a forward ring; others use an authored point.** In area mode, the selector
picks a point at a random distance in a band around the party leader and at a random angle
inside the authored heading arc. The script reset installs **180 degrees** (the forward half-plane)
and a **39 to 42** world-unit band. Scripts can change these values, and the 39-unit minimum is
used only for units with flag bit 45 or 49; otherwise the minimum is zero. These are conditional
native rules, not a claim that every enemy appears in that ring during ordinary play.

**Monsters disappear behind you.** Walk far enough from a spawned monster and the engine retires
it. The reset default range is **43** units — deliberately just outside the ring it spawned in,
so a monster does not pop in and immediately pop back out. Distance here is measured **flat on
the ground**: height difference does not count, so a monster on a cliff directly above you is
"zero away".

**The range-retire check follows the character you are steering.** Mode 1 consults *only* the party
member you are currently controlling, not the whole party. Two characters can be far apart; what
decides this retirement test is where **you** are. Mode 2 instead retires on the party leader's
approach to an authored point; it uses the leader's navigation position.

**Turn around quickly and they are still the same ones.** There is a **return window**. If you
leave an area and come back to it — specifically, if the area you are entering is the one you
were in *before* the one you just left — and you do it within **300 seconds**, the whole spawn
state is handed back: the same monsters, their positions, their facing, how many times each has
died, and how much enmity each holds against each party member. Miss the window, or arrive from
somewhere else, and the bank is wiped and everything is generated fresh.

The automatic selector also checks a script-settable active count cap, initialised to **28**,
against the active actor count. This is a selection gate, not a universal count of every actor.

## 2. Native mechanism

### The tunables, and who owns them

Seven tunables are listed below. All live in `.data` BSS — **zero at image load** — and are
installed at runtime. Every one is reachable from authored script.

| Address | Name | Installed value | Installed by | Read by |
|---|---|---|---|---|
| `02089358` | `g_nSpawnCandidateHeadingArcDegrees` (i32) | **180** | `FUN_0023A520` (script reset) | `Spawn_TrySelectCandidatePosition` |
| `02089360` | `g_flAutomaticSpawnMinPlayerDistance` | **39.0** | same | `Spawn_SelectAndPrepareAutomaticEntry` |
| `02089364` | `g_flAutomaticSpawnMaxPlayerDistance` | **42.0** | same | same |
| `02089368` | `g_flNativeLifecycleRange` | **43.0** | same | `SpawnLifecycle_CheckAndRetireByNativeRange` |
| `0208D457` | `g_bSpawnPositionAttemptLimit` (u8) | **1** | same | `Spawn_SelectAndPrepareAutomaticEntry` |
| `0208936C` | `g_nSpawnKeepReturnWindow` (i32) | **300** | `BattleStorage_InitializeWorkArrays` | `SpawnKeep_GetReturnWindow`, bank rotation |
| `0208D458` | `g_bAutomaticSpawnActiveCap` (u8) | **28** (`0x1C`) | `BattleSystem_InitializeAreaState` | `Spawn_SelectAndPrepareAutomaticEntry` |

**Two of these are true engine defaults and five are authored.** The return window and the active
cap are written by native initialisers. The four radii/arc values and the attempt limit are
written **only** by `FUN_0023A520` and by their individual setters — and `FUN_0023A520`'s single
call site in the whole binary is `thunk_FUN_0023a520` (`00510710`), owned by the Script VM. So
`39 / 42 / 43 / 180 / 1` is *the default set a script installs*, not a value the engine holds on
its own; a zone that never calls the reset primitive sees zeros.

Each has a ScriptVM entry point:

| Native setter | ScriptVM wrapper |
|---|---|
| `Spawn_SetCandidateHeadingArcDegrees` (`0023A1F0`) — truncates a float to int | `VM_Spawn_SetCandidateHeadingArcDegrees` (`0050F470`) |
| `Spawn_SetNativeLifecycleRanges` (`0023A1D0`) — `(retireRange, maxSpawn, minSpawn)` | `VM_SpawnSetNativeLifecycleRanges` (`0050F410`) |
| `Spawn_SetPositionAttemptLimit` (`00239020`) | `VM_Spawn_SetPositionAttemptLimit` (`0050FC00`) |
| `SpawnKeep_SetReturnWindow` (`00235340`) | `VM_SpawnKeep_SetReturnWindow` (`005107F0`) |
| *(cap, written directly)* | `VM_Spawn_SetAutomaticActiveCap` (`00510320`) |
| `Spawn_CountActiveCapTrackedActors` (`00308D90`) | `VM_Spawn_GetActiveCapTrackedCount` (`00510390`) |

A seventh float at `0208935C` is written `5.0` by `BattleStorage_InitializeWorkArrays` and
**never read anywhere in the binary** — a dead tunable.

### The return window

```c
int SpawnKeep_GetReturnWindow(void)          { return g_nSpawnKeepReturnWindow; }

void SpawnKeep_SetReturnWindow(int window)   // test ecx,ecx / mov eax,0x12C / cmovs ecx,eax
{
    if (window < 0)                          // strictly negative - cmovs tests the sign flag
        window = 300;
    g_nSpawnKeepReturnWindow = window;
}
```

**300 is the built-in default** and a negative argument restores it rather than being rejected or
clamped to zero. **The unit is seconds** — see the rotation rule below, where the window is
multiplied by the frame rate before being compared with a raw tick delta.

### Candidate generation and validation — two exclusive modes

`Spawn_TrySelectCandidatePosition` (`00234AF0`) asks the authored field data for **format-class 0,
at the candidate index supplied in ECX**, and branches on the first byte of that record.
The wrapper `003209C0` (§11) returns **0 on
success, -1 on failure**; the caller rejects a negative return, not zero:

```c
if (max_radius - min_radius == 0.0)                      return 0;
if (FieldData_CopyFormat0Candidate(candidateId, &rec) < 0) return 0; // 003209C0

out_position = rec.position;                             // record + 0x10
leader = BattleUnit_GetPartyLeader();                    // NOT any party member - the leader
if (!leader) return 0;
Actor_GetWorldPosition(leader->pActorWork, &lx, &ly, &lz);
leaderYaw = FUN_00265200(leader->pActorWork);            // class-dependent heading read

if (rec[0] == 0) {                        /* ---- POINT MODE: validate the authored point ---- */
    minD2 = min_radius * min_radius;                     // squared here, by the caller
    maxD2 = max_radius * max_radius;
    toCand = Vector3_ComputeXZHeadingOrFallback(&leaderPos, out_position, leaderYaw);
    if (|wrap(leaderYaw - toCand)| <= (arcDeg / 2) * 2PI / 360)
        return Spawn_ValidateCandidateDistanceToPlayers(out_position, &minD2, &maxD2,
                                                        observed, flags);
    return 0;
}
                                          /* ---- AREA MODE: generate a random point ---- */
r     = (RNG() % (int)((max_radius - min_radius) * 100.0)) / 100.0 + min_radius;
theta = FUN_00316DA0(leaderYaw, ((RNG() % arcDeg) - arcDeg / 2) * 2PI / 360);   // wrapped
cand.x = leader.x + r * sin(theta);
cand.z = leader.z + r * cos(theta);
if (FieldRegion_ContainsWorldPosition(&cand, &rec)) { out_position = cand; return 1; }
return 0;
```

**The two modes never both run.** In point mode the position is authored and the distance
validator decides; in area mode the position is drawn at random and the *only* filter is whether
it lands inside the field region. Its radius calculation uses the requested interval around
the **leader alone**; normal band reasoning assumes finite, nonnegative ordered radii, a nonzero
integer radius divisor and a positive arc. No other party member is consulted there. AREA mode does **not** publish
`out_observed`; the automatic caller nevertheless consumes its stack slot (§11).

The polar construction uses a **32,768-entry sine table** at `DAT_01F004E0` indexed by
`(theta / 2PI) * scale & 0x7FFF`, with cosine taken as `sin[(0x2000 - i) & 0x7FFF]`. Its
convention — `X = sin(theta) * r`, `Z = cos(theta) * r` — is **identical** to the one
`Movement_ComputeDeltaFromHeadingSpeed` uses, and `Vector3_ComputeXZHeadingOrFallback` is its
exact inverse: `atan2(dx, dz)`, falling back to the supplied heading when the two points
coincide.

The generated `Y` is **not written** by the polar construction; only `X` and `Z` are. What
supplies the vertical coordinate ~~is recorded as **L-7**~~ is nothing at generation; a terrain probe supplies it at activation *(answered: see §7, L-7 ANSWERED, and spawn-placement-height-and-authored-tunables.md; 2026-10-02, OPUS)*.

### Distance validation

`Spawn_ValidateCandidateDistanceToPlayers` (`00234DA0`) — read at tier 1, and it is not what the
recorded signature suggested:

```c
int Spawn_ValidateCandidateDistanceToPlayers(
        FFXII_Vec4f *candidate, float *minD2, float *maxD2,
        float *out_observed, int include_all_party_slots)
{
    int accepted = 0;
    for (int i = 0; i < 4; i++) {
        unit = BattleUnit_FindMappedDefinitionSelectorByIndex(i);   // a FUNCTION, not a table
        if (!unit) continue;
        bkbi = unit[0x698]; if (!bkbi) continue;
        if (((bkbi[0x64] | bkbi[0x3C]) & 0x80000003) != 0
            && FieldData_GetActiveFieldRecordBit15() == 0) continue;      // status filter
        if (!include_all_party_slots
            && !PartyFocus_IsCurrentPackedActorHandle(unit[0x08])) continue;

        Actor_GetWorldPosition(unit[0x10], &px, &py, &pz);
        d2 = Vector3_ComputeSquaredXZDistance(candidate, &px);            // SQUARED, XZ only
        if (minD2 && d2 <  *minD2) return 0;
        if (maxD2 && d2 >  *maxD2) return 0;
        if (out_observed && PartyFocus_IsCurrentPackedActorHandle(unit[0x08]))
            *out_observed = d2;
        accepted = 1;
    }
    return accepted;
}
```

Four facts the earlier reading did not have:

1. **The bounds are squared distances.** `003A1960` returns `(dx² + dz²)`; both callers square
   their bounds before passing them (`min*min` in `00234AF0`, `x*x` in `00308040`). Passing a raw
   distance gives a radius of `sqrt(bound)`.
2. **Distance is planar.** `Vector3_ComputeSquaredXZDistance` reads components `[0]` and `[2]`
   only. Vertical separation is invisible to every spawn and retire test in this document.
3. **Rejection is universal, acceptance is existential.** The first eligible slot that violates a
   bound returns `0` immediately, so *every* eligible slot must satisfy the bounds — but
   `accepted` starts at `0` and is set only inside the eligible branch, so **if no slot is
   eligible the function returns 0**. "Nobody to measure against" is a rejection, not a free pass.
   The mathematical bounds statement assumes ordered floating-point values: a NaN distance
   does not take either `COMISS/JA` rejection branch under masked floating-point exceptions (§11).
4. **`include_all_party_slots` widens, it does not merely include an odd mode.** With `0` — what
   the spawn path passes — the loop keeps only the **party focus**, so exactly one character is
   measured. With `1` all four mapped slots count.

The observed distance is published only when the out-pointer is given **and** the slot is the
party focus. It is an immediate per-slot write: if a later eligible slot rejects, an earlier
focus distance remains published. A zero result therefore does not guarantee an unchanged output.

### Retirement — two opposite senses

`SpawnLifecycle_CheckAndRetireByNativeRange` (`002350C0`) is gated first:

```c
if (((actorWork[0x0D] >> 6) & 1) == 0)                      return 0;   // per-actor opt-in bit
unit = ActorWork_GetBattleUnit(actorWork);
if (!unit || unit->bLifecycleMode == 0)                     return 0;
if (bkbi && bkbi[0x05] == 0)                                return 0;   // spawn-backed only
if ((unit->qwUnitFlags & 0x10) == 0 || !bkbi)               return 0;
if (((bkbi->dwStatusMaskMode0_3 | bkbi->dwStatusMaskMode1_4) & 0x80000003) != 0
    && FieldData_GetActiveFieldRecordBit15() == 0)          return 0;
if (unit->pBkei->lifecycleFlags & RANGE_RETIRE_INHIBITED)   return 0;
```

then splits on `bLifecycleMode`:

```c
/* mode 1 - RANGE retire: go away and I disappear */
myPos  = Actor_GetWorldPosition(actorWork);
thresh = g_flNativeLifecycleRange * g_flNativeLifecycleRange;
any = false;
for (i = 0; i < 4; i++) {
    u = BattleUnit_FindMappedDefinitionSelectorByIndex(i);
    if (!u || (u[0] & 0x10) == 0) continue;
    bkbi = u[0x698]; if (!bkbi) continue;
    if (((bkbi[0x64] | bkbi[0x3C]) & 0x80000003) && !FieldData_GetActiveFieldRecordBit15()) continue;
    if (!PartyFocus_IsCurrentPackedActorHandle(u[0x08])) continue;    // FOCUS ONLY, always
    if (SquaredXZ(myPos, pos(u)) < thresh) return 0;                  // someone near - keep it
    any = true;
}
if (any) retire;

/* mode 2 - POINT retire: come close to an authored point and I disappear */
leader = BattleUnit_GetPartyLeader();  if (!leader) return 0;
if (FieldData_GetFormat0RecordVectorByIndex(unit->bLifecyclePointId, &pt) < 0) return 0;
if (unordered_or_less_equal(SquaredXZ(leader.locomotion.aAfCurrentNavigationPosition, pt),
                            unit->flLifecyclePointThreshold ^ 2)) retire; // COMISS/JBE
```

with the retire action itself:

```c
unit->pBkei->lifecycleFlags |= RANGE_REENTRY_PENDING;
BattleUnit_TeardownAndDespawn(unit, 1);
SpawnGroup_UpdateExpectedMemberLaneMask(unit, 0);
```

**Mode 2 is the opposite of a range retire** — it fires when the *leader approaches* an authored
field point within a per-unit threshold. Calling this function "the range check" describes only
mode 1.

`RANGE_REENTRY_PENDING` is the flag the automatic spawner later tests to decide a retired unit
may come back — the mechanical link between retirement and the return window.

### Automatic spawn selection

`Spawn_SelectAndPrepareAutomaticEntry` (`00235720`) is the caller of the candidate selector and
carries the rest of the policy:

```c
if (Spawn_CountActiveCapTrackedActors() >= (i8)g_bAutomaticSpawnActiveCap) return -1;   // cap 28
seconds = GameClock_GetRawTickCounter() / (int)(DAT_01DFE0B8 * 30.0);
for each lane 1 .. laneCount-1:
    bkei = &g_pBtlKeepCharWork1[laneToBkeiIndex[lane]];       if index == 0xFF: skip
    if (bkei->wDeathLimit != 0 && bkei->wDeathCount >= bkei->wDeathLimit) skip;   // died out
    if (!( (bkei->lifecycleFlags & RANGE_REENTRY_PENDING)
        || !(bkei->lifecycleFlags & ACTIVATION_COMMITTED)
        ||  bkei->wRespawnCooldownTicks == 0
        ||  seconds - bkei->dwLastDeathTick >= bkei->wRespawnCooldownTicks )) skip;

    minR = (unit->qwUnitFlags & 0x2200000000000) ? g_flAutomaticSpawnMinPlayerDistance : 0.0;
    for each candidate in the lane:
        limit = (int8_t)g_bSpawnPositionAttemptLimit;
        for (attempt = 0; attempt < limit; attempt++)
            if (Spawn_TrySelectCandidatePosition(candId, &pos, minR,
                    g_flAutomaticSpawnMaxPlayerDistance, &observed, 0)
                && unordered_or_less(observed, DAT_02F973B8)) break; // COMISS/JB
        if (attempt != limit) { remember this lane and position }
if (found) {
    bkei->afPersistedWorldPosition = pos;
    bkei->candidateStateSecondary = pos;
    unit->qwUnitFlags |= 0x4000000;
    return lane;
}
return -1;
```

Three things worth pulling out:

- **The minimum distance is conditional.** It is applied only when the unit carries flag bit 45
  or bit 49 (`0x0002200000000000`) — see §8f. Every other spawn-backed unit is given `minR = 0.0` and **may be
  placed on top of you.**
- **`DAT_02F973B8` is initialised to `+INF`.** It is written once, by `BattleStorage_InitializeWorkArrays`,
  from the constant at `00914700` = `0x7F800000`. So the "observed distance must be under X"
  filter accepts finite distances and unordered comparisons, but rejects positive infinity against
  positive infinity. It is not wholly disabled. The same global is read by `AiOrder_EvaluateTargetSelector`,
  `AiOrder_SelectFinalTargetFromCandidates` and `Loot_FindNearestActivePickupPosition` — it is a
  shared "maximum considered squared distance", not a spawn-only value.
- **`wDeathLimit` / `wDeathCount` retire a monster permanently.** Once a keep entry has died its
  authored number of times it is skipped forever (until the bank is wiped), and
  `wRespawnCooldownTicks` is compared in **seconds** derived from the same `× 30` frame rate.

**What the cap counts** *(read whole 2026-09-30, FABLE)*. `Spawn_CountActiveCapTrackedActors` (`00308D90`, 69 B)
walks every battle-unit slot and counts the units whose flag word has **bit 21** (`0x200000`) set —
`test dword ptr [rax], 0x200000` at `00308DB3`, one increment per hit. That is the bit the spawn entry bind sets
([the battle-unit field map](../04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md), flag table row 21). So the
cap of 28 limits units bound to spawn entries, not every occupied slot.

### The persistence banks — `btlKeepCharWork1` and `btlKeepCharWork2`

Two banks are allocated in `BattleStorage_InitializeWorkArrays` with the authored tags
**`"btlKeepCharWork1"`** and **`"btlKeepCharWork2"`** (strings at `009146B8` and `009146D0`),
each **`0x9400` = 37,888 bytes**, zeroed. The rotation loops run `0x128` = **296** iterations
of a 128-byte block copy — that is the copy chunking, **not** the entry stride:
every accessor indexes the bank with `imul <idx>, 0x250`, so each bank holds **64 entries
of `0x250` = 592 bytes** (`0x9400 / 0x250 = 64` exactly). See §8f. Bank 1 is the live bank; bank 2 is the history.

`SpawnKeep_RotatePersistenceBanksForAreaTransition` (`00233780`):

```c
if (!bank1 || !bank2) return;                 // no copy or field/tick updates
fieldId = WorldTransition_GetActiveOrPendingFieldId();
ticks   = GameClock_GetRawTickCounter();

if (fieldId == g_wSpawnKeepPreviousFieldId
    && (uint32_t)(ticks - g_uSpawnKeepTransitionTick)
       <= (uint32_t)((uint32_t)(int32_t)(DAT_01DFE0B8 * 30.0)
                      * (uint32_t)g_nSpawnKeepReturnWindow))
{
      /* RESTORE: three-way exchange through a 0x9400 stack buffer */
      tmp   = bank2;  bank2 = bank1;  bank1 = tmp;
      historyBankIndex ^= 1;
}
else {
      /* WIPE: bank2 <- bank1, bank1 zeroed, 64 history counters reset to 1 */
      bank2 = bank1;
      memset(bank1, 0, 0x9400);
      historyBankIndex ^= 1;
      for (i = 0; i < 64; i++) spawnHistoryCounter[historyBankIndex][i] = 1;
}
g_wSpawnKeepPreviousFieldId   = g_wSpawnKeepMostRecentFieldId;
g_wSpawnKeepMostRecentFieldId = fieldId;
g_uSpawnKeepTransitionTick    = ticks;
```

**The restore condition is not "you came back to this area."** It is `fieldId ==
g_wSpawnKeepPreviousFieldId`, and `previous` holds the field from *two* transitions ago. So the
restore fires on the pattern **A → B → A**, within `30 × window` raw ticks. At the default that
is `30 × 300 = 9,000` ticks — **300 seconds**, which is how the window's unit is established.

`SpawnKeep_SerializePersistenceBanks` (`00233440`) copies **both** banks whole — 296 iterations of a
128-byte copy, i.e. all `0x9400` bytes, which is 64 entries — into
a `0x20010`-byte buffer, plus `g_wSpawnKeepPreviousFieldId` and `g_wSpawnKeepMostRecentFieldId`;
`SpawnKeep_RestorePersistenceBank` (`00233550`) restores the two field-id
registers **but copies only bank 2 from buffer +0x10**, not bank 1 from +0x10010.
The earlier claim that this helper reverses both bank copies was false. The pair
(`previous`, `mostRecent`) is restored; neither helper serialises/restores the transition tick
or window setting. Whole-load continuation requires its caller's policy~~, still open here (§11)~~.
*Reconciled 2026-09-30 (FABLE): the caller's policy is read in §12 — `005843E0` restores keep image A, image B or
neither, never both in one call — and L-13, the row that carried the rest of the load sequence, is SUPERSEDED on its
static answer (§7).*

**These copy loops are structure-blind.** Serialize, restore and both rotation branches move
**eight `movups` per ~~entry~~ iteration — 128 bytes, wholesale** — and reference no field at all *(the entry is
`0x250` bytes; 128 is the copy chunk, §8f — propagated 2026-09-12)*:

```asm
00233566  lea    rax, [rax + 0x80]              ; SpawnKeep_RestorePersistenceBank
0023356D  movups xmm0, xmmword ptr [rdx]
00233577  movups xmmword ptr [rax - 0x80], xmm0
...                                             ; x8 = 128 bytes
002335B3  sub    r8, 1
002335B7  jne    0x233566                       ; x 0x128 = 296 iterations = 0x9400 B = 64 entries of 0x250
```

That matters for what the loops can be cited *for*: they prove **the whole ~~128-byte~~ entry is
carried** *(all `0x9400` bytes, so every `0x250`-byte entry)*, and nothing about which byte holds what. Any field identity has to come from a function
that actually addresses that offset. Two of them do, and they establish the entry's most
interesting field at tier 1:

```asm
0032156D  lea rdi, [rax + 0x19]     ; BattleEnmity_UpdatePeriodicDecay,   rax = unit[0x6A0] = BKEI
00321D61  lea r9,  [rax + 0x19]     ; BattleEnmity_WriteAllCombatantIds,  same base
00321DA3  cmp ebx, 0x28             ; the write loop bound: 40 combatant ids
```

**The enemy threat table lives inside the spawn-keep entry** — `BKEI + 0x19` is the decay timer and
`BKEI + 0x1A + id` is the enmity toward combatant `id`, for `id` in `0..39`, ending at `+0x41`.
Because the bank copy is blind and that range is inside the ~~128 bytes~~ `0x250`-byte entry, **enmity is banked, wiped
and restored with everything else**: come back inside the window and the monsters remember not just
where they were but who they were angry at; arrive any other way and every threat value in the zone
is zeroed at once. `09-Combat-AI-And-Gambits` §8k carries the consequences for gambit behaviour.

The remaining per-entry field names — `lifecycleFlags`, `wDeathCount`, `wDeathLimit`,
`dwLastDeathTick`, `wRespawnCooldownTicks`, `bStealAvailabilityFlags`, `bRangeRetireInhibitTag`,
`bScriptSelection`, `bPersistenceKey`, `bPersistenceRestoreValue`, `afPersistedWorldPosition[4]`,
`candidateStateSecondary[0x10]`, `flPersistedFacingYaw`, `dwTransientState_78`,
`bTransientState_7C` — come from the **GFZ struct definition, tier 3**, except where a function
elsewhere in this document addresses them directly: `lifecycleFlags`, `wDeathCount`, `wDeathLimit`,
`dwLastDeathTick` and `wRespawnCooldownTicks` are all read at tier 1 by
`Spawn_SelectAndPrepareAutomaticEntry`, and `lifecycleFlags` is written at tier 1 by the retire
path. See §8e.

**The save buffer's layout is exact**: a 16-byte header holding the two field-id registers
(`+0x00` previous, `+0x02` most-recent), then bank 2 at `+0x10` and bank 1 at `+0x10010` — each
bank given a padded `0x10000` of the `0x20010` total, of which `0x9400` is used.

### Group operations

All five iterate the battle-unit slot pool (`g_nBattleUnitSlotCount`, `32`) through
`BattleUnit_GetBySlotIndexIfUnitFlag4Set`:

| Function | What it does |
|---|---|
| `SpawnGroup_TeardownAllGroupedSpawnUnits` | tear down every spawn-backed unit whose `bSpawnGroupId != 0` |
| `SpawnGroup_TeardownUnitsByGroupMask` | the same, filtered by `(mask >> (groupId & 31)) & 1` |
| `SpawnGroup_SetUnitFlag800ByGroupMask` | `qwUnitFlags \|= 0x800` on the masked subset, then `FUN_00312700(unit)` |
| `SpawnGroup_ClearUnitFlag800ByGroupMask` | `qwUnitFlags &= ~0x800` on the masked subset, then the same notify |
| `Spawn_SetAllSpawnBackedUnitsCurrentHPZero` | `BattleStats_SetCurrentHP(bkbi, 0, NULL, 0)` on every spawn-backed unit |

The **group mask is a 32-bit set of spawn-group ids**, tested as `1 << (bSpawnGroupId & 31)`, and
group `0` is exempt from the "all" teardown. "Spawn-backed" is the predicate `bkbi[0x05] == 1`
throughout.

`Spawn_SetAllSpawnBackedUnitsCurrentHPZero` goes through `BattleStats_SetCurrentHP`, which
forwards a signed delta into `BattleStats_ModifyHPAndProcessLethalState` — so it **runs death
processing**, it does not silently write zero.

Flag `0x800` is the script's **hide** bit (`hideenemy` / `showenemy`, answered 2026-09-11 — §7,
**L-3**): bit 11 of the low dword of `qwUnitFlags`, and the notify after every change recomputes
the actor's presentation visibility from the suppression mask it belongs to.

## 3. Key addresses

| Address | Name | Body | Verified |
|---|---|---|---|
| `00235330` | `SpawnKeep_GetReturnWindow` | 7 B | tier 1 |
| `00235340` | `SpawnKeep_SetReturnWindow` | 17 B | tier 1, disassembly |
| `00234DA0` | `Spawn_ValidateCandidateDistanceToPlayers` | 290 B | **tier 1 (was: signature only)** |
| `00234AF0` | `Spawn_TrySelectCandidatePosition` | 584 B | **tier 1**, plus disassembly of the arc gate |
| `002350C0` | `SpawnLifecycle_CheckAndRetireByNativeRange` | 529 B | **tier 1** |
| `00235720` | `Spawn_SelectAndPrepareAutomaticEntry` | 841 B | **tier 1** — the caller of `00234AF0` |
| `00235360` | `Spawn_SelectContinuousEntry` | 390 B | tier 1, ~~partially read~~ read whole (L-11, §7; reconciled 2026-09-30) |
| `00233440` | `SpawnKeep_SerializePersistenceBanks` | 260 B | **tier 1** |
| `00233550` | `SpawnKeep_RestorePersistenceBank` | 127 B | **tier 1** |
| `00233780` | `SpawnKeep_RotatePersistenceBanksForAreaTransition` | 672 B | **tier 1** |
| `00234880` / `00234990` | `SpawnGroup_Teardown*` | 81 / 102 B | **tier 1** |
| `00234A10` / `00234A80` | `SpawnGroup_Set/ClearUnitFlag800ByGroupMask` | 99 / 99 B | **tier 1** |
| `002352E0` | `Spawn_SetAllSpawnBackedUnitsCurrentHPZero` | 75 B | **tier 1** |
| `002368D0` | `BattleStorage_InitializeWorkArrays` | 353 B | disassembly — allocates both banks |
| `0023A520` | *(unnamed)* spawn tunable reset *(the handler of verb `0x3053` `btlAtelSetupActorStart` through the thunk `00510710`, L-10; 2026-10-01, SWE2-STRUCT for OPUS, DD batch 21)* | 66 B | disassembly — installs 39/42/43/180/1 |
| `0023A1D0` | `Spawn_SetNativeLifecycleRanges` | 25 B | disassembly |
| `0023A1F0` | `Spawn_SetCandidateHeadingArcDegrees` | 11 B | disassembly |
| `00239020` | `Spawn_SetPositionAttemptLimit` | 19 B | tier 1 |
| `0031B810` | `BattleUnit_FindMappedDefinitionSelectorByIndex` | 70 B | **tier 1 — a function, not a table** |
| `003A1960` | `Vector3_ComputeSquaredXZDistance` | 31 B | **tier 1, disassembly** |
| `0031E620` | thunk → `003A1960` | 5 B | thunk flag + identical body |
| `00328370` | `RNG_SharedGameplayLCG_NextU32` | 91 B | tier 1 |
| `00320940` | `FieldData_GetFormat0RecordVectorByIndex` | 117 B | tier 1 |
| `003209C0` | field-record copy wrapper, class 0 | 29 B | tier 1 |
| `00308040` | `BattleUnit_HasNonPartyEngagementEvidence` | 237 B | **tier 1 — the second caller of `00234DA0`** |
| `00308D90` | `Spawn_CountActiveCapTrackedActors` | 69 B | **tier 1, read whole 2026-09-30** — counts slots whose unit has flag bit 21 set (`00308DB3`, §2); ~~named; body not read here~~ |
| `003272A0` | `BattleUnit_GetPartyLeader` | 55 B | tier 1 |
| `003273B0` | `PartyFocus_IsCurrentPackedActorHandle` | 28 B | tier 1 |
| `00265020` | `Actor_GetWorldPosition` | 61 B | tier 1 |
| `003148F0` | `WorldTransition_GetActiveOrPendingFieldId` | 27 B | tier 1 (§8b) |

All resolve in the current parent with the extents shown (`DumpFullCoverageGraph`, 2026-09-02). Re-checked
2026-09-30 (FABLE) against `Database/Tools/work/graph/functions.tsv`: all 32 extents in the table agree.

## 4. Data structures and formulas

```
Globals (all .data BSS - zero at load)
  02089358  i32  g_nSpawnCandidateHeadingArcDegrees   script-installed 180
  0208935C  f32  written 5.0, never read
  02089360  f32  g_flAutomaticSpawnMinPlayerDistance  script-installed 39.0
  02089364  f32  g_flAutomaticSpawnMaxPlayerDistance  script-installed 42.0
  02089368  f32  g_flNativeLifecycleRange             script-installed 43.0
  0208936C  i32  g_nSpawnKeepReturnWindow             native default 300 (seconds)
  0208D457  u8   g_bSpawnPositionAttemptLimit         byte storage; signed i8 loop use; reset 1
  0208D458  u8   g_bAutomaticSpawnActiveCap           byte storage; signed i8 compare; init 28
  0208E690  ptr  g_pBtlKeepCharWork1                  0x9400 bytes = 64 x 0x250
  0208E698  ptr  g_pBtlKeepCharWork2                  0x9400 bytes = 64 x 0x250
  0208E6A0  i32  g_nBattleUnitSlotCount               32; BattleUnit stride 0xF50
  02F973B8  f32  max considered squared distance      +INF; shared with AI targeting and loot

Constants (.rdata, read from the image)
  01CEBC78  6.2831855   TWO_PI          00902438  360.0
  01CEBC50  3.1415927   PI              00915620  -PI        00915624  -TWO_PI
  008F3134  100.0       radius quantum  008F8D80  30.0 (frame rate)

BattleUnit                       BattleKeepEntry (BKEI, 0x250 B; was "128 B", §8f)
  +0x00 qwUnitFlags                +0x00 lifecycleFlags   RANGE_REENTRY_PENDING,
  +0x08 packed actor handle              ACTIVATION_COMMITTED, RANGE_RETIRE_INHIBITED
  +0x10 pActorWork                 +0x08 wDeathCount   +0x0A wDeathLimit
  +0x698 pBkbi                     +0x0C dwLastDeathTick (seconds)
  +0x6A0 pBkei                     +0x10 wRespawnCooldownTicks (seconds)
  +0xE98 bSpawnGroupId                   bStealAvailabilityFlags, bRangeRetireInhibitTag,
        bLifecycleMode  0 off /              bScriptSelection, bPersistenceKey,
                        1 range /            bPersistenceRestoreValue
                        2 authored point +0x14.. bEnmityTableHeader + aEnmityByCombatantId[0x2E]   # <- corrected 2026-10-02, OPUS - +0x14 is bStealAvailabilityFlags (0023A7AE-0023A7D3); the decay byte is +0x19 and the enmity table +0x1A..+0x41, 40 bytes (0032156D, 00321D61, bound 0x28 at 00321DA3); the field map is the authority
        bLifecyclePointId                afPersistedWorldPosition[4]
        flLifecyclePointThreshold        candidateStateSecondary[0x10]
                                         flPersistedFacingYaw, dwTransientState_78
BattleStats record (BKBI)
  +0x05 == 1  -> spawn-backed        +0x3C dwStatusMaskMode1_4
  +0x48 current HP                   +0x64 dwStatusMaskMode0_3
                                     +0x38 dwStatusMaskMode2_5  (NOT in the retire gate)

WorldActor
  +0x0D bit 6  -> range-retire opt-in (FUN_002672F0)
```

**Return-window setter**

```
setReturnWindow(w):  g_nSpawnKeepReturnWindow = (w < 0) ? 300 : w
```

**Bank rotation trigger** — this routine's exchange condition, with both bank pointers valid:

```
restore  iff  enteringFieldId == g_wSpawnKeepPreviousFieldId          // the A -> B -> A pattern
         and  uint32(rawTicks - g_uSpawnKeepTransitionTick)
                   <= low32(int32(DAT_01DFE0B8 * 30.0) * g_nSpawnKeepReturnWindow)
                                                                      // 30 * 300 = 9000 ticks
otherwise: bank2 <- bank1; zero bank1; reset 64 history counters to 1
```

**Candidate acceptance, point mode**

```
toCand = (cand.x == leader.x && cand.z == leader.z) ? leaderYaw : atan2(cand.x - leader.x,
                                                                        cand.z - leader.z)
delta  = |wrap(leaderYaw - toCand)|                                   // wrap into (-PI, PI]
gate   = ((int)(arcDeg / 2)) * TWO_PI / 360                           // integer divide, toward 0
accept iff delta <= gate
       and Spawn_ValidateCandidateDistanceToPlayers(cand, min^2, max^2, ...) != 0
```

**Candidate generation, area mode**

```
r     = ((int)RNG() % (int)((max - min) * 100.0)) / 100.0 + min       // quantised to 1/100
theta = wrap(leaderYaw + ((int)RNG() % arcDeg - arcDeg / 2) * TWO_PI / 360)
cand.x = leader.x + r * sin(theta)
cand.z = leader.z + r * cos(theta)
accept iff FieldRegion_ContainsWorldPosition(cand, regionRecord)
```

**Distance validation** — all comparisons in **squared XZ**, assuming ordered operands:

```
eligible(p) :=  p exists
            and p.bkbi exists
            and ( ((p.bkbi[0x64] | p.bkbi[0x3C]) & 0x80000003) == 0
                  or FieldData_GetActiveFieldRecordBit15() != 0 )
            and ( include_all_party_slots or p is the party focus )

accept(cand) iff  (exists an eligible p among slots 0..3)
             and  (for every eligible p:  (min == NULL || d2 >= *min)
                                      and (max == NULL || d2 <= *max) )
             where d2 = (cand.x - p.x)^2 + (cand.z - p.z)^2          // Y ignored
```

**Range retirement, mode 1**

```
retire iff  (actorWork[0x0D] >> 6) & 1
       and  unit.bLifecycleMode == 1  and  unit.qwUnitFlags & 0x10
       and  bkbi[0x05] != 0  and  not (pBkei.lifecycleFlags & RANGE_RETIRE_INHIBITED)
       and  the party focus exists and is eligible
       and  (focus.x - me.x)^2 + (focus.z - me.z)^2  >=  g_flNativeLifecycleRange ^ 2
                                                          // 43^2 = 1849 at the installed default
```

**Authored-point retirement, mode 2**

```
retire iff  unit.bLifecycleMode == 2
       and  FieldData_GetFormat0RecordVectorByIndex(unit.bLifecyclePointId, &pt) >= 0
       and  unordered_or_less_equal(SquaredXZ(leader.navigationPosition, pt),
                                    unit.flLifecyclePointThreshold ^ 2) // COMISS/JBE
```

**Respawn eligibility**

```
seconds = GameClock_GetRawTickCounter() / (int)(DAT_01DFE0B8 * 30.0)
eligible iff  (wDeathLimit == 0 or wDeathCount < wDeathLimit)
         and  ( lifecycleFlags & RANGE_REENTRY_PENDING
             or not (lifecycleFlags & ACTIVATION_COMMITTED)
             or wRespawnCooldownTicks == 0
             or seconds - dwLastDeathTick >= wRespawnCooldownTicks )
```

**Group mask**

```
selected(unit) iff  bkbi[0x05] == 1  and  (mask >> (unit.bSpawnGroupId & 31)) & 1
```

## 5. Call chain

```
per-frame actor lifecycle
  -> BattleUnit_UpdateLifecycleAndCombatFrame (00233F70) [ActorEntity]
     -> SpawnLifecycle_CheckAndRetireByNativeRange (002350C0)
        -> FUN_002672F0                        per-actor opt-in bit
        -> ActorWork_GetBattleUnit / Actor_GetWorldPosition
        -> BattleUnit_FindMappedDefinitionSelectorByIndex (0031B810) x4    [ActorEntity]
        -> PartyFocus_IsCurrentPackedActorHandle (003273B0)                [Party]
        -> FieldData_GetActiveFieldRecordBit15 (00313F60 thunk -> 00377C20) [WorldAreaField]
        -> Vector3_ComputeSquaredXZDistance (0031E620 -> 003A1960)
        -> mode 2: BattleUnit_GetPartyLeader, FieldData_GetFormat0RecordVectorByIndex (00320940)
        -> retire: BattleUnit_TeardownAndDespawn (00300E40)                [ActorEntity]
                   SpawnGroup_UpdateExpectedMemberLaneMask (00306E60)

spawn attempt
  -> Spawn_SelectAndPrepareAutomaticEntry (00235720)
     -> Spawn_CountActiveCapTrackedActors (00308D90)      cap gate, 28
     -> GameClock_GetRawTickCounter / DAT_01DFE0B8 * 30   -> seconds
     -> Spawn_TrySelectCandidatePosition (00234AF0), up to g_bSpawnPositionAttemptLimit times
        -> FUN_003209C0 -> FieldData_CopyIndexedRecordByFormatClass   [WorldAreaField]
        -> BattleUnit_GetPartyLeader (003272A0)                       [Party]
        -> Actor_GetWorldPosition (00265020) / FUN_00265200           [ActorEntity, Movement]
        -> point mode: Vector3_ComputeXZHeadingOrFallback (0031AC90) -> atan2f
                       Math_NormalizeAngleDifference (0031A930)
                       Spawn_ValidateCandidateDistanceToPlayers (00234DA0)
        -> area  mode: RNG_SharedGameplayLCG_NextU32 (00328370) x2    [RNG]
                       FUN_00316DA0 (angle wrap) / FUN_00319390 (sin-table polar offset)
                       FieldRegion_ContainsWorldPosition (002374E0)   [WorldAreaField]

area transition
  -> SpawnKeep_RotatePersistenceBanksForAreaTransition (00233780)
     -> WorldTransition_GetActiveOrPendingFieldId (003148F0)          [WorldAreaField]
     -> GameClock_GetRawTickCounter
     -> restore (A->B->A within the window) or wipe

save / load
  -> SpawnKeep_SerializePersistenceBanks (00233440) / RestorePersistenceBank (00233550)

script
  -> VM_SpawnKeep_SetReturnWindow / VM_SpawnSetNativeLifecycleRanges /
     VM_Spawn_SetCandidateHeadingArcDegrees / VM_Spawn_SetPositionAttemptLimit /
     VM_Spawn_SetAutomaticActiveCap / VM_Spawn_GetActiveCapTrackedCount
  -> thunk_FUN_0023a520 (00510710) -> FUN_0023A520   install the default tunable set
```

**`Spawn_ValidateCandidateDistanceToPlayers` has two callers, not one.** The second is
`BattleUnit_HasNonPartyEngagementEvidence` (`00308040`), which passes
`include_all_party_slots = 1`, supplies only a minimum, squares it itself, and **inverts the
result** — a `0` return means "no party member is within that radius", which it reports as
engagement evidence. That is a Combat-side consumer of a Spawn-owned predicate.

**Upstream:** ~~encounter/spawn controllers,~~ the per-actor lifecycle frame, area transition, and
authored script. *Corrected 2026-09-30 (FABLE): the direct call sites name no encounter controller. The raw call
index gives each entry point one or two sites, each resolved to its containing function and read there:*

| entry point | its call sites | reached from |
|---|---|---|
| `Spawn_SelectAndPrepareAutomaticEntry` `00235720` | one call site, in `0050F520` | the ScriptVM adapter `VM_Spawn_SelectAutomaticEntry` (`0050F520`), verb `0x301A` `btlAtelDecideEntryPointAuto`: a zone script asks for each placement |
| `Spawn_SelectContinuousEntry` `00235360` | one call site, in `00510260` | the verb `305F` adapter `00510260` (§7, L-11) |
| `SpawnLifecycle_CheckAndRetireByNativeRange` `002350C0` | `00234022` only | `BattleUnit_UpdateLifecycleAndCombatFrame` (`00233F70`), which the field runtime pass calls through the actor record's `+0x38` callback ([the field runtime pass](../04-Actor-Entity/the-field-runtime-pass.md)) |
| `SpawnKeep_RotatePersistenceBanksForAreaTransition` `00233780` | `00234423` only | `BattleSystem_InitializeAreaState` (`002342F0`), whose two callers §13 reads |
| `SpawnKeep_SerializePersistenceBanks` `00233440` | `00229CF2`; `005845AA`, `005845E1` | the two captures `00229B40` and `00584580` (§12) |
| `SpawnKeep_RestorePersistenceBank` `00233550` | `0058443B`, `0058445E` | `005843E0`, one image per call (§12) |

**Downstream:** actor creation and teardown, the save image. *Anchored 2026-09-30 (FABLE):* retirement tears the
unit down through `BattleUnit_TeardownAndDespawn` (`00300E40`) and updates its group's expected-member lane mask (§2);
automatic selection does not create the actor — it writes the keep entry's position and sets unit flag `0x4000000`,
and activation places the unit later ([height and tunables](spawn-placement-height-and-authored-tunables.md), L-7);
the banks reach the save image through the two captures above (§12).

**Do not confuse with:** actor identity and world placement, which are separate owners. This
category owns *encounter generation, spawn, retire and respawn lifecycle* only. Note also that
`SpawnLifecycle_CheckAndRetireByNativeRange`'s mode 2 is **not** a range check despite the
function's name.

## 6. Modding notes

- **The validator takes squared bounds.** `003A1960` returns `dx² + dz²`. Square radii before
  calling the validator directly. The global spawn/retire ranges and per-unit mode-2 threshold
  store radii; their callers square them. Keep these representations distinct.
- **Height never counts.** Every distance in this system is XZ-planar. A monster directly above
  or below you is at distance zero for spawn, retire and engagement purposes.
- **Point-mode validation and mode-1 retirement use focus.** The spawn validator passes
  `include_all_party_slots = 0`, and mode 1 hard-codes the focus test. AREA generation and mode-2
  retirement use the leader through different position paths.
- **"No eligible player" rejects point-mode distance validation.** AREA mode does not call that
  validator; a missing focus cannot be used to infer rejection of every placement mode.
- **The 39/42/43/180/1 defaults are script-installed, not engine constants.** The globals are
  zero at load and only `FUN_0023A520` (via a ScriptVM thunk) or the individual setters ever
  write them. Do not assume a value is in force; read the global.
- **Keep the retire range above the spawn ring.** The default gap is one unit (42 → 43). Set
  `retireRange <= maxSpawn` through `VM_SpawnSetNativeLifecycleRanges` and a newly selected
  position can satisfy mode-1 retirement immediately. Actual same-frame activation/retirement
  requires caller scheduling and the other gates, not established by these inequalities alone. *(2026-10-01, SWE2-STRUCT for OPUS, DD batch 21: a stated limit of this note, not an open question. The note claims the inequality; whether one frame both places and retires a unit is scheduling, which this page does not claim.)*
- **The minimum spawn distance is opt-in per unit.** Without flag bit 45 or 49
  (`0x0002200000000000`) the minimum is forced to `0.0` and a monster may appear on top of the
  player. This is the mechanism behind "it spawned in my face", and it is a unit flag, not a bug.
- **The arc is a half-angle in disguise.** `arcDeg` is halved with a signed integer divide, so
  an odd value loses the half degree, and `180` means ±90° — the forward half-plane.
- **The return window default is 300 seconds** and negatives reset it. It only applies to the
  A → B → A pattern; any other route wipes the bank regardless of how fast you were.
- **`wDeathLimit` is a permanent kill count.** A keep entry that has died its authored number of
  times never respawns until the bank is wiped by a failed rotation.
- **The active cap is 28 of 32 slots**, reinstalled at every area-state init, and script-settable.
  Raising it past the pool size will not help; the pool is `g_nBattleUnitSlotCount = 32`.
- **Keep the attempt setting in 1..127.** The setter clamps only below 1, then stores a byte.
  Values 128..255 make the signed loop skip attempts but accept stale position data; 256 stores
  zero. The active-cap byte is also compared signed, so 128..255 rejects even a zero active count.
- **Do not infer output validity from a return alone.** Distance rejection can leave an earlier
  focus result; AREA selection leaves the distance slot untouched, and the outer `JB` accepts
  an unordered comparison. See §11 for raw controlled evidence and native limits.
- **`Spawn_SetAllSpawnBackedUnitsCurrentHPZero` kills, it does not erase.** It routes through the
  lethal-state modifier, so death handling, drops and enmity teardown all run.
- **XIIOnline:** the distance rule consults the *local* focus handle
  (`PartyFocus_GetCurrentPackedActorHandle`, a receiver-local packed handle that is explicitly
  not network-stable), so two clients with different focus characters will legitimately reach
  different spawn and retire verdicts on the same frame. Any shared spawn model has to decide
  whose focus is authoritative before this validator runs — and note that the random path
  consumes the **shared gameplay LCG** (`00328370`), so a divergent spawn attempt desynchronises
  every other consumer of that stream.

## 7. What is not known

- [x] **L-12 — AREA output state and ordinary caller context.** The selector's AREA branch ~~*(closed — the register row is WITHDRAWN.)*~~ *(closed — corrected 2026-09-30 (FABLE): the register row reads **SUPERSEDED 2026-09-26** under the runtime rule, not WITHDRAWN. The static reading is complete — §11, "L-12's static half": nothing in the caller's frame writes the slot and the test is loop-invariant, so one stack word decides the call — and the live value of that word is one read, which the register does not queue.)*
      leaves `out_observed` untouched and the automatic caller does not initialise that stack
      slot. Its branch can depend on earlier stack contents. Local reads/writes are proved in
      §11; the values reached during ordinary initialized gameplay and their practical effect
      remain unobserved. Do not promote a stubbed candidate service to a live observation.
- [x] **L-13 — complete load continuation.** `00233550` restores bank 2 and the field-id pair, ~~*(closed — the register row is WITHDRAWN.)*~~ *(closed — corrected 2026-09-30 (FABLE): the register row reads **SUPERSEDED 2026-09-27**, not WITHDRAWN; see the reconciliation at the end of this entry.)*
      not bank 1 or transition tick. **Caller selection answered in §12:** `005843E0` restores
      A, B or neither; it never calls both branches in one invocation. The enclosing controller
      event and area-init rotation call are identified. Still open: the complete ordering between
      successful loading, area initialization/rotation and live bank/timer preparation, including
      intervening native callees. **§29 adds one ordinary older-manual-load observation:**
      compatibility battle records already restored at Load complete; history/parity changed
      by field entry. Both keep banks were zero, so their preparation remains indistinguishable.
      Current-to-old session reuse and nonzero persistence/respawn remain open. Earlier L-5
      remains answered for the rotation routine itself.
      *Reconciled 2026-09-30 (FABLE) with the register; the two "still open" / "remain open" clauses above are as of
      §29 (2026-09-13).* The static question is answered: the transition stamp `02089374` and the clock `0208D45C`
      have two writers each, and bank 1 is captured into the snapshot by `00233440` but never read back by
      `00233550`, which is why a session's bank 1 survives a load (OPUS, 2026-09-27; control
      `_index/candidates/l13-bank-writers/l13_bank_writers.py`). FRONTIER's ruling
      (`_index/candidates/register-triage/batch-K-scope-rulings.md`, extension 2026-09-27e) closed the row
      SUPERSEDED on that answer. **What stays unobserved is live only:** a slot-0 field-transition autosave load with
      non-zero keep banks, and whether the requeued area init's rotation then brings the same enemies back. The ruling
      named `FABLE-REQ-ASTRA-L13-BANKS` as the carrier of that residue, but the board shows that request DONE on
      2026-09-13, before the ruling, closed on EXP-080 (§29: both banks zero). By the ruling's own HM-1 rule, live
      residue without a carrier goes to the runtime-surrogate carrier; routed 2026-09-30 to SWE2-FRONTIER for that
      routing, not registered here. *(2026-10-01, SWE2-STRUCT for OPUS, DD batch 21: still without a carrier. FRONTIER-RT-RUNTIME-SURROGATE lists seven other rows and not this one, so the batch 21 [record](../_index/candidates/swe2struct-ddres-b21-1001/README.md) proposes the residue to OPUS as one runtime row.)*

- [x] ~~Whether candidate bounds must hold for every player slot or just one.~~ **L-1 ANSWERED** —
      neither, exactly: **every eligible slot** must pass, **and at least one** must exist; with
      the flag the spawn path passes, "eligible" is a single character (the focus).
- [x] ~~The unit of the return window.~~ **L-2 ANSWERED — seconds.** The rotation compares a raw
      tick delta against `(int)(DAT_01DFE0B8 * 30.0) * window`.
- [x] ~~What flag `0x800` means on a spawn unit. **L-3.** Narrowed: bit 11 of the low dword of
      `qwUnitFlags`, set/cleared by group mask, each change followed by `FUN_00312700(unit)`.~~
      **ANSWERED 2026-09-11 — "hidden by the script".** The set / clear pair are the handlers of
      the verbs **`hideenemy`** (`0479`, `00349940` → `SpawnGroup_SetUnitFlag800ByGroupMask`) and
      **`showenemy`** (`0478`, `00349200` → `…Clear…`), and the notify `00312700(unit)` is
      `Actor_SetPresentationVisibilityEnabled(actor, BattleUnit_ComputePresentationSuppressionMask(unit) == 0)`:
      `003125E0` folds bit 11 in as reason bit 1 of the mask (`0031268A`–`00312690`), beside bits 10
      (→ 4) and 9 (→ 8), unit `+4` bit 2 (→ `0x20`), flag bit 1 with a terminal status (→ `0x10`),
      the spawn record's flag bits 4 / 3 (→ `0x40` / `0x80`) and the mode-2 early exit (→ 1);
      any non-zero mask hides the actor. **L-3.**
- [x] ~~The retirement range and what "native range" is measured against.~~ **L-4 ANSWERED** —
      `g_flNativeLifecycleRange` (script-installed `43.0`), squared, against the squared XZ
      distance from the retiring actor to the **party focus**. Plus a second, opposite mode.
- [x] ~~Persistence bank layout, count and rotation rule.~~ **L-5 ANSWERED** — two banks tagged
      `btlKeepCharWork1` / `btlKeepCharWork2`, `0x9400` bytes each, **64 entries of `0x250` = 592 bytes**;
      rotation exchanges them on the A → B → A pattern inside the window and wipes bank 1
      otherwise.
- [x] ~~Whether `003A1960` returns squared or true distance.~~ **L-6 ANSWERED** — squared, and
      **XZ only**: `(p1.z-p2.z)² + (p1.x-p2.x)²`.
- [x] ~~**L-7.** What supplies the **Y** coordinate of a generated spawn position.~~
      **ANSWERED — nothing does, at generation.** `FUN_00319390` writes `[0]` and `[2]`
      only and the caller never initialises `[1]`, so the generated Y is stale stack; the region
      test ignores it. The height is supplied later, at activation, by a terrain probe in
      `SpawnUnit_FinalizeSpawnEntryActivation` — gated on a per-unit definition bit, and
      yielding world `0.0` when no surface is found. See [`spawn-placement-height-and-authored-tunables.md`](spawn-placement-height-and-authored-tunables.md).
- [x] ~~**L-8 (new).** The meaning of the status mask `0x80000003` tested against BKBI `+0x3C` and
      `+0x64`, and of the `FieldData_GetActiveFieldRecordBit15()` escape that overrides it. The
      same pair appears in the validator and in the retire loop.~~ **ANSWERED 2026-09-11 (by
      propagation)** — bits 0, 1 and 31 are **KO, Stone and X-Zone** (bank 5 names; help text
      *lost consciousness*, *turned to stone*, *vanished without a trace*), the three terminal
      statuses [the status write](../10-Status-Periodic-Terminal/Status-Write/the-status-write-and-its-side-effects.md)
      §2.7 handles; the bit-15 escape is the field-record permission
      [the bit-15 page](../03-World-Area-Field/Field-Record-Table/field-record-bit15-action-permission.md)
      decodes; the whole list is on [the statuses sheet](../10-Status-Periodic-Terminal/the-thirty-two-statuses.md). `L-8`.
- [x] ~~**L-9.** What unit flags bit 49 and bit 53 denote.~~ **ANSWERED, and the bit
      numbering was wrong: the mask `0x0002200000000000` is bits 45 and 49.** Bit 49 is set by
      `BattleUnit_ActivateAppliedDefinitionRuntime` on a unit's first activation; bit 45 by the
      ScriptVM primitive `0x304D btlAtelCanselInitialSpawnFlag`. The minimum therefore applies to
      a unit that has been alive once, or that a zone script declares not to be an initial
      placement. See [`spawn-placement-height-and-authored-tunables.md`](spawn-placement-height-and-authored-tunables.md).
- [x] ~~**L-10.** Whether `FUN_0023A520` is invoked by every zone.~~ **ANSWERED — no,
      but it is invoked by every zone that can place anything.** It is ScriptVM primitive `0x3053`
      `btlAtelSetupActorStart`. Across the 828 decompiled US scripts, 406 call it, exactly once
      and first; all 400 that define a unit and all 172 that run the spawn selector are among
      them, with zero exceptions. The all-zero state is also self-announcing: spawning becomes
      impossible and every mode-1 unit retires on its first frame. See [`spawn-placement-height-and-authored-tunables.md`](spawn-placement-height-and-authored-tunables.md).
- [x] ~~**L-11 (new).** The `bPersistenceKey` / `bPersistenceRestoreValue` pair and the exact policy
      in `Spawn_SelectContinuousEntry` (`00235360`), read only in part.~~ **ANSWERED 2026-09-11 —
      read whole.** The verb `btlAtelDecideEntryGroupByContinuous` (`305F`, `00510260`, no
      arguments, result = the lane ordinal or −1) walks the calling unit's lane map (`unit +0x40`:
      count, then slot ids; a `0xFF` slot ends the walk) and, for the **first** lane whose live
      keep entry (`[0208E690] + slot × 0x250`) carries a non-zero `bPersistenceKey` (`+0x17`),
      searches the 64 entries of the history bank (`[0208E698]`) for one with the **same key** whose
      `lifecycleFlags` has `ACTIVATION_COMMITTED` **and** `RANGE_REENTRY_PENDING` **or** `released`
      (`test r8b, 2` then `test r8b, 5`, `00235413`–`0023541D`) — a monster that was committed and
      then left — and **copies that whole `0x250`-byte entry over the live one** (`00235460`–`002354DD`),
      returning the lane's ordinal; no key, no match, no bank → −1. `bPersistenceRestoreValue`
      (`+0x18`) is only what the two resets restore `+0x17` from ([the keep entry](Spawn-Record/the-spawn-keep-entry-field-map.md)).
- [x] ~~The name/body disagreement on `BattleUnit_GetBySlotIndexIfUnitFlag4Set` (`00321170`): the
      name says flag 4, the body tests `qwUnitFlags & 0x10`. Recorded, not renamed.~~ **Resolved
      2026-09-12 (FABLE): there is no disagreement.** "Flag 4" in the name is *bit* 4, whose mask is
      `0x10` — the row [the battle-unit field map](../04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md)'s flag table keeps for bit 4 (set by
      `BattleUnit_UpdateLifecycleAndCombatFrame` at activation, cleared by `BattleUnit_ResetStateForReuse`).
      The body (`00321174`–`00321181`: `BattleUnit_GetBySlotIndex`, then `test byte ptr [rax], 0x10`)
      returns the unit only while that bit is set.

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| Return window default 300, negative resets | complete bodies of `00235330` / `00235340`; `mov eax,0x12C; cmovs ecx,eax` at `00235342` | 1 |
| 300 is also the load-time value | `mov dword ptr [0208936C], 0x12C` at `00236A0D` in `BattleStorage_InitializeWorkArrays` | 1 |
| Return window is in seconds | `(int)(DAT_01DFE0B8 * 30.0) * g_nSpawnKeepReturnWindow` compared against a raw tick delta in `00233780`; the same `/(DAT_01DFE0B8*30)` converts ticks to the unit of `wRespawnCooldownTicks` in `00235720` | 1 |
| `003A1960` is squared, XZ-only | disassembly: `movss xmm1,[rcx]; movss xmm0,[rcx+8]; subss…; mulss; addss; ret` | 1 |
| Bounds are compared squared | `min*min`, `max*max` at `00234C48`-`00234C60`; independently, `x*x` before the call in `00308040` | 1 |
| Validator quantifier: all eligible, at least one | complete body of `00234DA0` — early `return 0` inside the loop, `accepted` initialised to `0` outside it | 1 |
| Spawn path measures only the focus | `Spawn_TrySelectCandidatePosition(..., flags = 0)` at the `00235720` call site, and the `!include_all_party_slots` branch in `00234DA0` | 1 |
| Arc gate `\|Δ\| ≤ (arcDeg/2)·2π/360` | disassembly `00234BE7`-`00234C1A`: `call 0031AC90; movaps xmm1,xmm0; movaps xmm0,xmm9; call 0031A930; cdq; sub; sar 1; cvtdq2ps; mulss TWO_PI; divss 360; comiss; jb` | 1 |
| `atan2(dx, dz)` heading convention | disassembly of `0031AC90`: `xmm0 = to.x-from.x`, `xmm1 = to.z-from.z`, `jmp atan2f` | 1 |
| Area mode is RNG-driven polar placement | complete body of `00234AF0`; two `RNG_SharedGameplayLCG_NextU32` calls; `FUN_00319390` sine-table polar add | 1 |
| Installed tunable values 39 / 42 / 43 / 180 / 1 | disassembly of `FUN_0023A520`; floats read from the image at `009146EC` / `F0` / `F4`; `mov dword [02089358], 0xB4` | 1 |
| Every tunable has a ScriptVM setter | exact call-site census: each native setter has exactly one caller and it is a `VM_*` function | 1 + 11 |
| `FUN_0023A520` is reached only via a ScriptVM thunk | exact call-site census over all 38,161 bodies: one site, `thunk_FUN_0023a520` (`00510710`); zero address-taking data references | 1 + 11 |
| Active cap 28, reinstalled per area | `mov byte [0208D458], 0x1C` at `0023433C` in `BattleSystem_InitializeAreaState`; read at `00235758` | 1 |
| `DAT_02F973B8` is `+INF` | written once from `00914700`, whose four bytes are `00 00 80 7F` | 1 |
| Retire mode 1 uses the focus and the squared range | complete body of `002350C0` | 1 |
| Retire mode 2 fires on *approach* to an authored point | same body, `bLifecycleMode == 2` branch | 1 |
| Retire sets `RANGE_REENTRY_PENDING`, which the spawner tests | `002350C0` retire block; `00235720` eligibility test | 1 |
| Banks are 64 × `0x250` B, tagged `btlKeepCharWork1`/`2` | `0x9400` allocations in `002368D0` with the two literal strings at `009146B8` / `009146D0`; `0x128` × 128 B copy loops in `00233780` / `00233440` covering all `0x9400` bytes; the `0x250` entry stride from sixteen `imul` sites, see §8f | 1 + 2 |
| Rotation restores only on A → B → A inside the window | complete body of `00233780`; `fieldId == g_wSpawnKeepPreviousFieldId` before the two history registers are advanced | 1 |
| The two field-id registers are serialised | `00233440` / `00233550` tails | 1 |
| Enmity is banked per combatant | the table base is `BKEI + 0x19` (`lea` at `0032156D` and `00321D61`) with a `cmp ebx, 0x28` loop bound, and the bank copy moves all ~~128 bytes of the entry~~ `0x9400` bytes, so every `0x250`-byte entry (2026-09-12) | 1 |
| The four bank loops are structure-blind 128-byte-chunk `movups` copies | disassembly of `00233440`, `00233550` and both branches of `00233780` | 1 |
| Save buffer: 16-byte header, bank 2 at `+0x10`, bank 1 at `+0x10010` | `lea rdx, [rbx + 0x10]` / `lea rcx, [rbx + 0x10010]` in `00233440`; `memset` size `0x20010` | 1 |
| Group mask is `1 << (bSpawnGroupId & 31)`; group 0 exempt from "all" | complete bodies of `00234880` / `00234990` / `00234A10` / `00234A80` | 1 |
| HP-zero routes through lethal-state processing | `002352E0` → `BattleStats_SetCurrentHP` (`00300520`) → `BattleStats_ModifyHPAndProcessLethalState` | 1 |
| `0031B810` is a function, not a table | complete body: index → `BattleEncodedId_IsValidForClass(0x17, i)` → selector table at `DAT_02EBF190 + 0x5A5A + i*2` → `BattleUnit_FindByDefinitionSelector` | 1 |
| `00234DA0` has two callers | fresh call graph + exact call-site census | 1 + 11 |
| Unit flag bit 11 is "hidden by the script" (L-3) | `hideenemy` / `showenemy` handlers `00349940` / `00349200`; `003125E0` folds bit 11 as reason 2 (`0031268A`–`00312690`), re-read 2026-09-12 | 1 |
| `0x80000003` is KO, Stone and X-Zone (L-8) | propagated from [the status write](../10-Status-Periodic-Terminal/Status-Write/the-status-write-and-its-side-effects.md) §2.7 and [the statuses sheet](../10-Status-Periodic-Terminal/the-thirty-two-statuses.md) | 1 (by propagation) |
| The continuous-entry restore (L-11) | `Spawn_SelectContinuousEntry` `00235360` read whole: flag tests `00235413`–`0023541D`, key compare `0023541F`, the `0x250`-byte copy `00235460`–`002354DD` (4 × `0x80` + `0x50`), re-read 2026-09-12 | 1 |
| `00321170` tests bit 4 (mask `0x10`) | `00321174`–`00321181` | 1 |
| The active cap counts units with flag bit 21 (2026-09-30) | complete 69-byte body of `00308D90`: a loop over the battle-unit slots, `test dword ptr [rax], 0x200000` at `00308DB3`, one increment per hit | 1 |
| Each entry point's call sites (§5 upstream, 2026-09-30) | the raw direct-call index `Database/Tools/work/FABLE/pub140-scratch/tools/rawcalls.json`, each site resolved to its containing function in `functions.tsv` and read there: the sites in `0050F520` and `00510260`, `00234022`, `00234423`, `00229CF2`, `005845AA` / `005845E1`, `0058443B` / `0058445E` | 1 + 11 |
| `004058E0` is not a spawn function (2026-09-30 correction of the residual placement) | complete 828-byte body: counter `+0x178` against `+0x17A`, child `[+0xD0]` extents `+0x4A` / `+0x48` and scale `+0x98`, completion bits of `+0x130`; no spawn, keep-entry or battle-unit reference | 1 |
| SWE2-FRONTIER subtree sizes and copy widths (2026-09-30 corrections) | extents from `functions.tsv`, each body disassembled to its last instruction; the copy helpers' loop counts `mov edx, 0x400` / `4` / `0xC0` with 128 bytes moved per iteration | 1 |

**Honest weighting.** The previous version of this document carried **five** claims at tier 3
(GFZ annotation only). All five have now been re-derived from complete bodies; two were wrong
(§8d). Nothing in this document rests on annotation alone any more, and nothing rests on
`.pdata`, `.xdata`, unwind records, EH maps, address adjacency or caller ownership.

## 8b. Reopened 2026-09-02 — what the bank rotation reads

Cross-reference audit pass 3 found a call edge this document did not account for:

```
SpawnKeep_RotatePersistenceBanksForAreaTransition (00233780)
   -> WorldTransition_GetActiveOrPendingFieldId (003148F0)
```

`003148F0` was read at tier 1 and is three lines: it returns
`SaveImage_GetPersistentPayloadBase()[0x1044]`, clamped to 0 when negative.

**So "which area am I in" — the value that drives bank rotation — is a field of the save image's
persistent payload, not a separate runtime global.** That is the concrete mechanism behind §2's
claim that banks rotate on area transition, and it ties the return window directly to save state.

> **Extended 2026-09-02 (falsification pass 1).** The tie to save state is stronger than this note
> claimed. The field id is not merely *read* from the save payload — the two history registers
> the rotation compares against, `g_wSpawnKeepPreviousFieldId` and `g_wSpawnKeepMostRecentFieldId`,
> are themselves **written into and restored from the persistence buffer** by `00233440` /
> `00233550`. ~~The return window therefore survives a save/load in both directions.~~ The field-id pair survives a save/load; the transition stamp `02089374` and the window setting `0208936C` do not *(corrected 2026-10-02, OPUS: `00233440` stores only `02089372`/`02089370` at buffer `+0x00`/`+0x02` (`00233529`–`0023353A`) and `00233550` restores only those (`002335B9`–`002335C7`); the window test reads `02089374` at `002337F0`; §2)*.
>
> **L-5 is no longer open** — §2 now gives the bank layout, count and rotation rule.

## 8c. Audit pass 4 disposition - inherited hub neighbours

Crossref audit pass 4 reported two **NEW SINCE BASELINE** relationships for this document:
`Audio` and `PlatformOnlineAchievements`. Both are consequences of section 8b, not new discoveries.

| Edge | Explanation |
|---|---|
| `003148F0` caller `00261F90` (Audio) | a caller of the area-id hub |
| `003148F0` caller `003160C0` (Platform) | a caller of the area-id hub |

Section 8b added `WorldTransition_GetActiveOrPendingFieldId` (`003148F0`) to this document. That
function has **49 callers across 10 subsystems**, so citing it imported its whole neighbourhood
into this document's audit surface.

**Disposition: accounted for by reference.** These edges belong to the hub, and the complete caller
census is enumerated in [`../00-Engine-Core-Runtime/Shared-State-Accessors/cross-subsystem-accessor-hubs.md`](../00-Engine-Core-Runtime/Shared-State-Accessors/cross-subsystem-accessor-hubs.md). They are not
spawn-lifecycle relationships and are not restated here.

The genuinely spawn-relevant direction is the one section 8b already states: bank rotation *reads*
the area id.

## 8d. Corrections, falsification pass 1 (2026-09-02)

### Correction 1 — `0031B810` is a function, not a table (OVERTURNED)

**Was believed.** §3 listed `0031B810` as *"party/player slot table (up to 4)"* and §4 as
*"party/player slot table, iterated up to 4 entries"*; §2 said the validator *"iterates up to four
party/player slots from a table at `0x0031B810`"*.

**Now believed.** `0031B810` is `BattleUnit_FindMappedDefinitionSelectorByIndex`, a **70-byte
function** owned by ActorEntity with 27 direct callers. It validates the index against encoded-id
class `0x17`, maps it through a two-byte selector table at `DAT_02EBF190 + 0x5A5A`, and resolves
the corresponding active `BattleUnit`. The **table it consults is at `02EBF190`**, not at
`0031B810`.

**What proved it.** It appears in the fresh call graph as a function with a body extent, and it is
in the validator's *callee* list. Its complete body was then read.

**Why the earlier reading was reachable.** The GFZ annotation for `00234DA0` described the
mechanism as reading a slot table and quoted this address as its source; the document copied the
address into a table of "key addresses" without checking which kind of thing it was. **An address
in a document is a claim about what lives at that address, and it is separately checkable from the
claim about behaviour.** The behavioural half — "up to four party/player slots" — is correct.

### Correction 2 — the placement rule is not one rule (OVERTURNED)

**Was believed.** §1: *"A spawn candidate position is checked against every party member, and a
placement that is too close — or too far — is rejected. That is a distance rule, not luck."*
§2: *"This is validation, not construction … `Spawn_TrySelectCandidatePosition` (`00234AF0`) is
the caller that does [choose one]."*

**Now believed.** `Spawn_TrySelectCandidatePosition` has **two exclusive modes**, selected by the
first byte of an authored field record. In *point* mode it validates an authored position through
the distance validator and an arc gate. In *area* mode it **draws the position at random** from
the shared gameplay LCG — a random radius in `[min, max)` and a random heading inside the arc,
around the party leader — and the distance validator is **never called**; the bounds hold by
construction, and only against the leader.

Every sentence of the "every party member" reading is also wrong in the other direction: the spawn
path passes `include_all_party_slots = 0`, so even in point mode the loop keeps **only the party
focus**.

**What proved it.** Reading `00234AF0` in full, then its caller `00235720`, then the disassembly of
the arc gate. The `RNG` edge was the thread: `audit_crossrefs.py` reported
`00234AF0 callee 00328370` as an `UNACCOUNTED NEIGHBOUR` under `RNG_Random_Selection` — a
subsystem this document never mentioned. Pulling that thread produced the whole second mode.

**Why the earlier reading was reachable.** The GFZ annotation for `00234DA0` is accurate about
`00234DA0` and describes it as *validation*; the document correctly repeated that, then made the
unforced inference that the caller must therefore be the thing that *chooses*. It does — but only
in one of its two modes, and in the other mode the validator it was named as calling is not called
at all. **"X validates, so its caller constructs" is a guess about the caller, not a fact about X.**

### Correction 3 — "the caller" was one of two

§2's *"`Spawn_TrySelectCandidatePosition` (`00234AF0`) is the caller"* is wrong as a uniqueness
claim. `00234DA0` has two callers; the second, `BattleUnit_HasNonPartyEngagementEvidence`
(`00308040`), is not a spawn function, passes the opposite flag value, and inverts the result.

### Correction 4 — the retire function has a second, opposite mode

§2's *"the engine's own range check that retires spawned units once the player is far enough
away"* describes `bLifecycleMode == 1` only. Mode 2 retires a unit when the **leader comes within**
`flLifecyclePointThreshold` of an authored field-data point. The name
`SpawnLifecycle_CheckAndRetireByNativeRange` is misleading for half its behaviour and is kept
unchanged, with the caveat recorded here and in §5.

### Correction 5 — the observed-distance publication has a second condition

§2 said *"The observed distance is published only when an out-pointer is given."* It is published
when the out-pointer is given **and** the slot being measured is the party focus.

### What survived unchanged

The return-window default of `300`, the negative-resets-to-default behaviour, the "up to four
slots" iteration, the optional-pointer semantics of the two bounds, the banked persistence scheme
rotating on area transition, the group-mask set/clear pairing on flag `0x800`, and §8b's finding
that the field id driving rotation comes from the save image's persistent payload. All were
attacked and all held.

## 8e. Correction, falsification pass 2 (2026-09-02) — a decompiler's struct is not a body

**Was believed** (written in falsification pass 1, earlier the same day): *"Per-entry fields
visible in the copy loops: `lifecycleFlags`, `wDeathCount`, … `aEnmityByCombatantId[0x2E]` …"*,
cited in §8 at **tier 1** against *"copied in all four bank loops"*.

**Now believed.** The four loops reference **no fields at all**. Each is eight `movups`
instructions moving 128 bytes per ~~entry~~ iteration, repeated 296 times *(§8f: the entry is `0x250` bytes)*. They prove the *entry* is carried
whole; they say nothing about its contents.

**What proved it.** Disassembling them. Ghidra's decompiler rendered the block copies as long
field-by-field assignments — `pFVar29->flPersistedFacingYaw = pFVar27->flPersistedFacingYaw;` and
sixty more like it — because a struct type is applied at those addresses. **Those names are painted
onto a `memcpy`.** The give-away was available and unread: `SpawnKeep_RestorePersistenceBank` has a
**127-byte body** and decompiled to roughly a hundred lines of member copies. A function cannot
copy sixty named fields in 127 bytes.

**Why the earlier reading was reachable.** Decompiler output *looks* like a body, and this database
correctly treats "complete exact-current function body" as tier 1. But the tier attaches to **what
the instructions do**, not to what the decompiler prints about them. A struct annotation is a GFZ
claim — tier 3 — and it does not become tier 1 by being rendered inside a tier-1 listing. **When a
decompilation names fields, check that the instruction stream addresses them.** A body size that
cannot hold the printed work is the cheapest possible check and it was skipped.

**The conclusion survives, on better evidence.** "Enmity is banked and restored" is now proven from
the *other* direction — `BattleEnmity_UpdatePeriodicDecay` and `BattleEnmity_WriteAllCombatantIds`
both compute the table base as `unit[0x6A0] + 0x19`, and the write loop's bound is `0x28` = 40, so
the block occupies `BKEI + 0x19 .. +0x41`, entirely inside the 128 bytes the loops move. The
earlier claim was right and the evidence for it was wrong; the corrected evidence is stronger than
the original, because it fixes the block's extent (`+0x19..+0x41`, 41 bytes) where the struct
annotation had implied `0x2E` bytes of enmity alone.

**Scope of the damage, checked.** Every other tier-1 row in §8 was re-examined for the same defect.
All of them cite either a disassembly listing quoted in this document or a decompilation whose
printed work fits its body size; none rests on a struct rendering. The affected row has been split
and re-cited.

## 8f. Corrections from the L-7 / L-9 / L-10 block (2026-09-02)

Two claims above were overturned while closing L-7, L-9 and L-10. The full evidence is in
[`spawn-placement-height-and-authored-tunables.md`](spawn-placement-height-and-authored-tunables.md) §8; the summary belongs here because this is the document that was wrong.

### Correction 6 — the minimum-distance flags are bits 45 and 49 (OVERTURNED)

**Was believed.** §2, §6 and §7: *"flag bit 49 or bit 53
(`0x2200000000000`)"*.

**Now believed.** The mask was transcribed correctly and decomposed wrongly.
`0x0002200000000000` has bits **45 and 49** set; `bit 49 | bit 53` would be
`0x0022000000000000`, which appears nowhere in the binary.

**What proved it.** The `movabs` bytes at `0023581D`: `49 ba 00 00 00 00 00 20 02 00`.

**Why the earlier reading was reachable.** Counting nibbles from the left of a value printed
without its leading zeros shifts every bit index by four. **Publish a mask together with the
bit list derived from it**, so the two can be checked against each other.

### Correction 7 — the keep banks hold 64 entries of 592 bytes (OVERTURNED)

**Was believed.** §2 and §4: *"each bank holds 296 entries of 128 bytes"*,
from the `0x128`-iteration, eight-`movups` copy loops.

**Now believed.** `0x9400` partitions as **64 entries of `0x250` = 592 bytes**. The loops move
128 bytes per iteration because that is how a `0x9400`-byte block copy is unrolled.

**What proved it.** Sixteen Spawn / SpawnKeep / SpawnEntry functions compute an entry address as
`imul <idx>, 0x250` followed by `add <reg>, [g_pBtlKeepCharWork1]`, among them
`Spawn_SelectAndPrepareAutomaticEntry` (`0023588B`), `Spawn_SelectContinuousEntry`,
`Spawn_SelectPreviousMapEntry`, `SpawnEntry_GetDeathLimit` and `SpawnKeep_ResolvePrimaryEntry`.
`0x9400 / 0x250 = 64` with no remainder. The wipe branch of
`SpawnKeep_RotatePersistenceBanksForAreaTransition` resetting exactly **64** history counters
— already stated in §2 — is the independent corroboration.

**Why the earlier reading was reachable.** This is the defect §8e already recorded, caught
one step short: §8e retracted the *field names* painted onto the `memcpy` but kept the
*entry count* the same loops appeared to imply. **A block copy's iteration count gives the buffer
size divided by the chunk size and says nothing about the record size.** The stride was available
from any of sixteen sites and none was consulted.

**Nothing else here is disturbed.** The enmity block at `BKEI + 0x19..+0x41` is still inside the
entry, the copies still carry the whole bank, and the rotation rule is unchanged. ~~The per-entry~~
~~field offsets in §4 stand;~~ The per-entry field offsets in §4 do not all stand - its `+0x14..` enmity label is wrong: `+0x14` is the steal-flag byte and the enmity block is `+0x19..+0x41` *(corrected 2026-10-02, OPUS: `0023A7AE`–`0023A7D3` write the steal bits at `[rbp + 0x14]`; `0032156D` and `00321D61` `lea …, [rax + 0x19]`, loop bound `0x28` at `00321DA3`; the field map is the authority, §8g)*; the 128-byte extent implied around them was never
load-bearing.

## 8g. Returned to `DOCUMENTED` — 2026-09-12 (FABLE)

Reopen 4 (`repos-d2`, 2026-09-02) was triggered by corrections 6 and 7 and by three questions closing. This
pass checked every trigger against the current state before changing the status:

- **Trigger 1, unaccounted neighbours:** `audit_crossrefs.py` against the current function list and edge set
  reports **0 findings** for this page. The same run on the time-stop registry page reports two, so the
  instrument detects neighbours and the zero is a real negative.
- **Trigger 7, questions that closed since:** L-3, L-8, L-11 and the `00321170` name are integrated in §7 and
  now carry §8 rows; L-3 and L-11 were re-read in the body.
- **Propagation of corrections 6 and 7:** the 128-byte entry reading survived in five places here — §2's
  copy-loop narrative and listing comment, §4's entry label, two §8 rows — and in `OPEN-QUESTIONS` L-5 and
  the L-section banner ("bit 49 or 53"). All are struck or corrected in place; the §8e trail keeps its
  wording with a pointer. [The keep-entry field map](Spawn-Record/the-spawn-keep-entry-field-map.md) is the authority for offsets.
- **Trigger 4, contradictions:** no row of the contradiction ledgers names this page.

**Not done here:** a falsification pass. `AUDITED` needs an independent attempt to break the page; this pass
was bookkeeping and propagation by an editor of the page, and does not count as one.

## 9. Related

- [`../03-World-Area-Field/Weather/weather-probability-and-transition-roll.md`](../03-World-Area-Field/Weather/weather-probability-and-transition-roll.md) — weather is an input to conditional spawn eligibility
- [`../04-Actor-Entity/`](../04-Actor-Entity/) — actor identity, a separate owner
- [`../06-Movement-And-Navigation/heading-speed-to-position-delta.md`](../06-Movement-And-Navigation/heading-speed-to-position-delta.md) — the identical `X = sin(θ)·r`, `Z = cos(θ)·r` convention, and `FUN_00265200`'s class-dependent heading read
- [`../00-Engine-Core-Runtime/Shared-State-Accessors/cross-subsystem-accessor-hubs.md`](../00-Engine-Core-Runtime/Shared-State-Accessors/cross-subsystem-accessor-hubs.md) — the area-id accessor this system consults
- [`../21-RNG-And-Determinism/rng-streams.md`](../21-RNG-And-Determinism/rng-streams.md) — `RNG_SharedGameplayLCG_NextU32`, which area-mode placement consumes twice per attempt
- [`../11-Party/`](../11-Party/) — `PartyFocus_*` and `BattleUnit_GetPartyLeader`, which decide *whose* position every rule here measures

## 10. Falsification pass 1 — 2026-09-02

**Program state:** parent `2ed8affb…`, snapshot `46f02e26…`, embedded EXE `73461d08…`, ledger
38,161 / 38,003 / 158 unresolved, verified before any reading (`Verify-GfzCheckpoint.ps1`,
`CHECKPOINT VERIFIED`).
**Instruments:** `DumpFullCoverageGraph.java` regenerated fresh (38,161 functions);
`audit_crossrefs.py` against that graph; `DecompileAddressFileBounded.java` (83 bodies, 83/83, 0
fail, 0 miss); and an **independent** instruction-level census — capstone over the exact body
extent of every one of the 38,161 functions, reading the authorized EXE directly (3 functions
incompletely disassembled, reported). All numeric constants were read from the PE image by VA →
file-offset resolution, not from a decompiler rendering.

> **Instrument caveat and re-verification, 2026-09-02.** "Exact body extent" is the ledger's
> extent, and the ledger's extent is not always exact: **29 of the 38,161 functions carry a
> `body_bytes` that over-runs the next function's entry** (1,917 bytes in total), so a naive
> `entry + body_bytes` walk reads the *following* function's code as part of the first. The
> canonical example is `00350320` — ledger size 56, real function 11 bytes ending in a tail jump,
> then `int3` padding, then a different function at `00350330`.
>
> The census was rebuilt with the extent clamped to the next entry **and** truncated at the first
> `int3` following a terminator, and the two runs were diffed:
>
> | | raw extent | clamped | spurious |
> |---|---:|---:|---:|
> | call sites | 155,220 | 155,179 | **41** (0.026 %) |
> | caller→callee pairs | 110,611 | 110,580 | **33** (0.030 %) |
> | RIP-relative memory references | 164,489 | 164,460 | **29** (0.018 %) |
>
> **Every figure this document cites is byte-identical under both walks** — all ten call-count
> claims, the Movement share of the slot hub, every writer census and the empty vtable/array
> intersection. None of the 29 affected functions calls anything counted here. The diff is the
> positive control: the instruments genuinely differ, and the difference lands elsewhere.


### Killer observations named, and hunted

| Claim | What would kill it | Result |
|---|---|---|
| `0031B810` is a party/player slot table | the address being a function in the current program | **KILLED.** It is a 70-byte function. Rewritten. |
| bounds compare against a true distance | `003A1960` returning a squared value, or a caller squaring its bounds | **KILLED twice.** The body is `dx²+dz²`, and *both* callers square their bounds first. |
| distance is 3-D | the distance function ignoring a component | **KILLED.** `[0]` and `[2]` only; `Y` never read. |
| placement is "a distance rule, not luck" | an RNG edge on the placement path | **KILLED.** Two LCG draws per attempt in area mode, and the validator is not called there at all. |
| the candidate rule consults every party member | the caller passing a flag that narrows the loop | **KILLED.** `flags = 0` at the only spawn call site → focus only. |
| `00234AF0` is the caller of the validator | a second caller | **KILLED.** `00308040`, a Combat-side predicate, with the opposite flag and an inverted result. |
| retirement is a range check | a branch that retires on *proximity* | **KILLED.** `bLifecycleMode == 2` retires when the leader comes close to an authored point. |
| the return window is measured in frames or ticks | finding the conversion | **ANSWERED: seconds.** `30 × window` raw ticks. |
| "banks rotate on area transition" | the rotation having a narrower trigger | **NARROWED, not killed.** It rotates on every transition; it *restores* only on A → B → A inside the window. |
| return window default 300, negative resets | any other immediate, or a different condition than the sign flag | **SURVIVED.** `mov eax,0x12C; cmovs`, and a second writer installs `300` at init. |
| bounds are optional pointers | either bound being dereferenced unconditionally | **SURVIVED.** Both are null-checked before use. |
| "up to four slots" | any loop bound other than 4 | **SURVIVED.** `i < 4` in the validator and in the retire loop. |
| flag `0x800` has a dedicated set/clear pair by group mask | the two functions differing in anything but the bit operation | **SURVIVED.** Identical bodies apart from `\|= 0x800` versus `&= ~0x800`. |

### What was tried and failed to break it

- **Tried to break the `300` default two ways.** First by re-reading the `cmovs` (it tests the
  sign flag, so only strictly negative resets — `0` is accepted and stored). Second by looking for
  a *different* writer that might install something else at startup: the exhaustive memory-operand
  census over all 38,161 bodies found exactly four references to `0208936C`, and the only other
  writer stores `0x12C` as well. The default is confirmed, not merely repeated.
- **Tried to break "up to four slots" by looking for a fifth.** The loop bound is a literal `4` in
  both consumers, and the mapped-selector resolver is the only way in.
- **Tried to make the tunables engine constants.** They are not: an exhaustive writer census
  showed the radii, arc and attempt limit have exactly two writers each — one script-facing setter
  and `FUN_0023A520` — and `FUN_0023A520`'s only call site is a ScriptVM thunk. This *weakened* a
  claim the document was about to make, and is recorded as **L-10** rather than papered over.
- **Ran a positive control before every absence claim.** Before reporting that `0208935C` is
  written and never read, the same query was run against `0208936C`, which returned two readers.
  Before reporting `FUN_0023A520` has no direct callers in the Ghidra graph, the capstone census
  was run on the same address and **found the thunk edge the graph had missed** — which is why the
  document says "reached through a ScriptVM thunk" rather than "unreachable". **The two
  instruments disagreed and the disagreement was resolved by looking, not by preferring one.**
- **Checked every citation for banned evidence.** No `.pdata`, `.xdata`, unwind record, EH map or
  `_IMAGE_RUNTIME_FUNCTION_ENTRY` appears in any reasoning here. Address adjacency was available
  and deliberately refused: `02089358`-`0208936C` sit in one contiguous run just past the global
  battle-state word at `02089340`, which *looks* like a config block — but the grouping is
  asserted **only** where a single function writes the whole set (`FUN_0023A520`), never from the
  addresses being neighbours.
- **Attacked the ownership boundary.** Everything claimed for Spawn here is a Spawn-owned body.
  The Party, WorldAreaField, ActorEntity, RNG and CombatFormula functions are cited as
  dependencies and are named as such; none of them is claimed by this category, and none of this
  document's conclusions is inherited from a caller.

### Crossref findings, dispositioned

`audit_crossrefs.py` reported **8 findings** for this document, all `UNACCOUNTED NEIGHBOUR`, and
**zero** `GHOST ADDRESS`, `BODY DRIFT` or `CLASSIFICATION`.

| Finding | Disposition |
|---|---|
| `RNG_Random_Selection` — `00234AF0` callee `00328370` | **REAL, and it overturned §2.** Area-mode placement draws twice from the shared gameplay LCG. Now documented in §2, §4, §5 and §6, and §9 links the RNG document. |
| `CombatFormula` — `002352E0` callee `00300520` | **REAL.** `Spawn_SetAllSpawnBackedUnitsCurrentHPZero` calls `BattleStats_SetCurrentHP`, which routes into lethal-state processing. Now stated in §2 and §6; the ownership stays CombatFormula's. |
| `Gameplay` — `00234DA0` caller `00308040` | **REAL, and it overturned §2's uniqueness claim.** The validator has a second, non-spawn caller. Now in §5 and §8d correction 3. |
| `Gameplay` / `CombatAI` / `CombatAction` / `CombatFormula` / `Items` / `Presentation` / `Rewards` — the 12 edges on `0031B810` | **Accounted for by reference.** `0031B810` is a 27-caller ActorEntity hub; its census belongs to `cross-subsystem-accessor-hubs.md`. This document's claim about it is only that the spawn and retire loops call it with indices 0-3. Not spawn relationships. |
| `CombatAction` / `Presentation` — `003148F0` callers `002F8060`, `002FA740`, `002B7B80`, `002BAF80` | **Accounted for by reference**, as §8c already dispositions for the same hub. |
| `Rewards_Progression_Economy` — `003A1960` caller `00319850` | **Accounted for and now stated.** `Loot_FindNearestActivePickupPosition` uses the same squared-XZ leaf *and* the same `DAT_02F973B8` threshold. `003A1960` is a shared geometry leaf with **7 direct callers plus the thunk `0031E620`, which carries 4 more** - the two instruments differ by exactly the thunk, and both are right; §2 now says what it computes. Not a spawn relationship. |

**Re-run after the amendment: 8 findings down to 1**, and the survivor is second-order. Quoting a
finding verbatim puts the neighbour's address into this document's own citation surface, so the
addresses named in the table above now import *their* neighbours.

| Residual finding | Disposition |
|---|---|
| `Resource` — `002368D0` callee `003843F0` | **Real and expected, not a spawn relationship.** `003843F0` (36 B, Resource) is the tagged allocator `BattleStorage_InitializeWorkArrays` calls to obtain the two `0x9400` banks and the `BtlWork` array. §2 cites `002368D0` for the *sizes and the authored tags*; where the memory comes from is the Resource layer's transaction, and ownership stays there. |
| `Resource` — `002B7B80` / `002BAF80` callee `00249580` | **Accounted for by reference, second-order.** Both are Presentation callers of the area-id hub `003148F0`, named only inside §8c's quoted disposition; `00249580` is their own Resource callee and has no connection to spawn lifecycle. |

**Third-order residue after falsification pass 2 (2026-09-02).** Naming a neighbour in order to
dispose of it makes that neighbour a cited address, whose own neighbours then surface on the next
run. Two survive, both at the third hop and neither a spawn relationship:

| Residual finding | Disposition |
|---|---|
| `InputGameplay` — `00377C20` caller `00313A00` | `00313F60`, cited in §5, is a five-byte `JMP rel32` thunk; §5 now names its target `00377C20`, which brought that address onto this surface. The predicate has **65 direct callers plus 47 through the thunk, 110 distinct functions in all**; `00313A00` (289 B, ~~untagged~~ — **corrected 2026-09-14: the certified parent classifies it
`GFZ.V121.CodeDomain.InputGameplay.FieldBattleCapabilityAndUIRequestInhibitMaskReconciliation`.
"Untagged" was true against GN158 and is not true now; the count of 110 is unaffected**) is one of
them. The complete census belongs to [`../03-World-Area-Field/Field-Record-Table/field-record-bit15-action-permission.md`](../03-World-Area-Field/Field-Record-Table/field-record-bit15-action-permission.md). |
| `SaveLoad` — `00249580` caller `00582790` | `00249580` appears in this document only inside the disposition row directly above, which itself only exists to explain a Presentation caller of the area-id hub. `00582790` (197 B, untagged) is a caller of that Resource helper. Three hops from anything this document claims. |

**This is a property of dispositioning by name, and it terminates.** Each hop's explanation is
shorter than the last because the addresses get further from the subject; the alternative —
dispositioning by reference without naming the address — leaves the finding unexplained. Naming it
and bounding it is the better trade, and the count falls (8 → 2 → 2) rather than growing.

### Reopening propagation

- **`21-RNG-And-Determinism/rng-streams.md` should reopen.** It gains a consumer it may not list:
  area-mode spawn placement draws `RNG_SharedGameplayLCG_NextU32` **twice per attempt**, up to
  `g_bSpawnPositionAttemptLimit` times per candidate, per lane. That is a meaningful draw count on
  a stream whose determinism the document is about.
- **`13-Rewards-Progression-Economy/loot-drops-and-enemy-chain.md` should reopen** if it discusses
  pickup range: `Loot_FindNearestActivePickupPosition` shares both `Vector3_ComputeSquaredXZDistance`
  and the `+INF`-by-default threshold at `02F973B8` with this system, so "nearest pickup" is a
  squared-XZ search with no distance cap unless something sets that global.
- **Any document describing the BattleUnit slot pool** should note that
  `BattleUnit_GetBySlotIndexIfUnitFlag4Set` (`00321170`) tests `qwUnitFlags & 0x10`, not `& 4`,
  contrary to its name.
- `06-Movement-And-Navigation/heading-speed-to-position-delta.md` is amended in the same pass; the
  two documents now agree on the `X = sin(θ)`, `Z = cos(θ)` convention and on `FUN_00265200`'s
  class discriminator, and neither contradicts the other.


### Correction — the three status masks, and which offset carries which name

**This table previously paired `dwStatusMaskMode0_3` with `+0x3C` and `dwStatusMaskMode1_4` with
`+0x64`. Both were reversed.** The corrected pairing is:

| offset | GFZ name | in the `0x80000003` retire gate |
|---|---|---|
| `+0x64` | `dwStatusMaskMode0_3` | yes |
| `+0x3C` | `dwStatusMaskMode1_4` | yes |
| `+0x38` | `dwStatusMaskMode2_5` | **no** |

**There are three 32-bit status masks per combatant, not two.** "Both effect layers" is retired as a
description of the structure — though every published expression built on it stays correct, because
the gate is `(+0x3C | +0x64) & 0x80000003` and `|` is symmetric. These are a different structure from
the 128-bit layers at `+0x68`/`+0x78`.

#### How it was settled, and why the first route needs no decompiler

`BattleStats_ChangeStatusAndProcessSideEffects` selects among six operation modes through a jump
table at `0030E88C`. Read directly from the authorized EXE in the certified project — six
image-relative dwords:

```
0030E88C  e7e41e00 fde41e00 13e51e00 26e51e00 43e51e00 57e51e00
          mode0    mode1    mode2    mode3    mode4    mode5
       -> 0030E4E7 0030E4FD 0030E513 0030E526 0030E543 0030E557
```

Each arm's opening bytes give its field as a **real displacement in the instruction encoding**, not a
decompiler subscript — `8b 4e 64` is `mov ecx,[rsi+0x64]`, `89 46 64` is `mov [rsi+0x64],eax`,
`85 7e 38` is `test [rsi+0x38],edi`:

```
0030E4E7  8b 4e 64 ...   mode 0: read+write +0x64
0030E4FD  8b 4e 3c ...   mode 1: read+write +0x3C
0030E513  8b 4e 38 ...   mode 2: read +0x38, jumps to the shared store
0030E526  8b 4e 64 85 f9 0f 85 fc 02 00 00 85 7e 38 ...
                         mode 3: read +0x64, TEST +0x38, write +0x64
0030E543  8b 4e 3c ...   mode 4: read+write +0x3C
0030E557  8b 46 38 ...   mode 5: read +0x38, falls through
0030E564  89 46 38       the store modes 2 and 5 share
```

**The table partitions the modes `{0,3} → +0x64`, `{1,4} → +0x3C`, `{2,5} → +0x38`, and the GFZ names
are `Mode0_3` / `Mode1_4` / `Mode2_5`.** This is the load-bearing route because **the partition is
not the one a reader would guess** — the obvious grouping is `{0,1} {2,3} {4,5}`, and the real one is
remove/add of the same field, six modes over three fields. A name of the form `…Mode0_3` landing on
the field modes 0 and 3 actually touch is a genuine agreement between an authored naming convention
and a jump table, not a restatement of either.

Two further routes, neither relying on case ordering:

- **Mode 3's arm is the only one with two different reads** (`8b 4e 64` then `85 7e 38`), and the
  decompiled case 3 is likewise the only case reading two fields. A unique fingerprint on both sides
  pins `Mode0_3` = `+0x64` (read and written) and `Mode2_5` = `+0x38` (tested only).
- **Modes 2 and 5 converge on one store** at `0030E564` — mode 2 jumps to it (`eb 3e`), mode 5 falls
  through — and the decompiled cases 2 and 5 are exactly the pair sharing a store, both naming
  `Mode2_5`.

`+0x3C` = `Mode1_4` then follows by elimination and is independently consistent with both.

> **Provenance note.** This correction was reported by a parallel session and **held blanked, not
> flipped**, until the bytes were read independently. `0030E88C`'s six dwords, mode 0's `8b 4e 64`,
> and mode 3's `8b 4e 64 … 85 7e 38` were each re-read from the certified program before the names
> were restored. A reversed pairing published on report would have been no better evidenced than the
> un-reversed one it replaced.

#### The asymmetry worth pulling on

**Mode 3's guard is on a different mask from the one it writes.** Adding a status through mode 3
refuses if the bit is already set in `+0x64` **or** in `+0x38`; modes 4 and 5 guard only their own
field. So whatever `+0x38` holds, mode 3 treats it as **authoritative over `+0x64`** — and `+0x38` is
the one mask the `0x80000003` retire gate ignores. That cross-mask exclusion, unique to one mode, is
the thread to pull if anyone wants to name the third mask.

## Independent re-derivation of `002350C0` — 2026-09-03, session `repos-78`

`002350C0` appeared on the *leaned on and never opened* cut — four citing documents, **all at its
entry only**. It was read from the image without reference to this document, and **§ "Retirement — two
opposite senses" is confirmed in full**: the gate chain in order, both `bLifecycleMode` branches, the
four-slot focus loop, the squared comparison in each mode, and the three-step retire action all agree.
**Nothing was found that this document does not already say.**

**So this was a false positive on that cut, and the interior addresses are supplied here so it stops
being one** — the same disposition as `0022A0B0` in `00-Engine-Core-Runtime`. The cut measures *"cited
by entry only"* as a proxy for *"never read"*, and this function was read to tier 1.

| claim already made above | interior address that carries it |
|---|---|
| the per-actor opt-in gate | `002350DE` — `call 002672F0`, `test eax,eax` |
| `bkbi[5] == 0` rejects non-spawn-backed units | `0023511A` |
| the `0x80000003` predicate with the `Bit15` waiver, **twice** | `0023513E` and `00235239` |
| the retire-inhibited flag on `pBkei` | `00235159` — `test byte ptr [rax], 0x10` |
| the mode split on `bLifecycleMode` | `00235162`–`0023517B` |
| mode 1's four-slot loop and its bound | `00235213` … `0023528D` — `cmp edi, 4` |
| mode 1 keeps the unit when any focused member is near | `0023527D` — `comiss xmm6, xmm0 ; ja` |
| mode 2's per-unit squared threshold | `0023519C` — `movss xmm6, [rsi+0x4C]` ; `mulss xmm6, xmm6` |
| mode 2 retires on approach | `002351B6` — `comiss xmm0, xmm6 ; jbe` |
| the retire action, in order | `002352A6`, `002352B1`, `002352BB` |

**One detail worth stating explicitly**, because it is consistent with this document's note that
`g_flNativeLifecycleRange` is *script-installed*: **`02089368` is in the zero-filled tail of `.data`
and has no value in the file at all.** A reader who dumps the shipped image sees `0`, not `43.0` — the
`43.0` in the table above is the installed runtime value, and the distinction matters to anyone
patching it statically.

## 11. Independent falsification — ASTRA, 2026-09-12

**REOPENED, not AUDITED.** FABLE requested an independent attack after §8g. The five suggested
core claims survive with the qualifications below, but the attempt-loop abstraction, output
contract, fixed candidate index and two-bank restore statement do not. This is a bounded
subsystem review, not the programme's final audit.

**Player version.** The default spawn ring is a setting with exceptions. For mods, a large
attempt count can skip choosing a position altogether and reuse old position data. The game
can also leave a distance value behind after rejecting a candidate. Save loading needs a more
careful account: the helper described here restores one of the two saved banks, not both.

### Evidence and method

[Raw evidence, executed probe and replay checker](../_experiments/evidence/spawn-lifecycle-falsification/README.md).
Shipping EXE SHA-256 remains `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`,
image base `00120000`. Capstone 5.0.7 captured 14 complete original bodies with contiguous
instruction bytes and per-body hashes. The validator is 290 B, candidate selector 584 B,
automatic selector 841 B, retirement 529 B and bank rotation 672 B. Complete local CFG checks
find the point-mode validator edge and exclude it from the AREA branch; that positive control
is essential to the negative claim. Serializer/restorer are independently read at 260/127 B.

Method B uses the established Unicorn 2.1.4 mapping/trace approach: six original bodies, 40
completed entry-to-return cases, with injected Windows x64 ABI/state and masked FP exceptions.
Slot lookup, focus-handle getter, field permission, actor positions, actor-to-unit lookup,
clock, active count and candidate service are explicit controlled providers. The cookie-check
boundary preserves RAX without checking the cookie. The actual distance leaf, thunk, focus
comparison, validator, attempt setter and automatic selector execute shipping instructions.
This does not prove the stubs' native effects, initialized gameplay, ordinary reachability or
the full candidate/retirement/rotation routines executing live.

Two feasibility controls first returned 0 for no slots and 1 for one in-range slot, with the
expected distinct output effects. The first larger run was **incomplete**, failing when a stub
page lacked a trap sentinel; it is not a pass. Adding sentinels stopped speculative decoding
past those controlled boundaries. The complete rerun preserved stack/nonvolatile state and
code bytes, with no invalid access. Independent replay reconciled **609 reads and 117 writes**
against retained initial/final bytes. Removing the early distance publication from a private
trace copy was rejected. No historical experiment or full mutation campaign was rerun.

### Killer observations and results

| Claim attacked | Distinguishing observation | Result |
|---|---|---|
| Every eligible slot, and at least one | Empty, one, two, late failing slot, missing focus, status waiver, equality controls | **Survives for ordered operands.** Empty returns 0; an eligible failing slot rejects even after an earlier pass. |
| Return 0 leaves no accepted observation | Focus slot publishes 25, later slot measures 200 against max 100 | **Killed.** `00234E7D` writes 25 before the later rejection; reversing the slots leaves the initial output untouched. |
| Mathematical interval formula covers all floats | Quiet-NaN distance versus finite bounds; positive-infinity control | **Narrowed.** Both rejection branches are `COMISS/JA`; unordered values do not reject. Infinity exceeds a finite maximum and rejects. NaN Y alone has no effect because Y is not read. |
| AREA never calls distance validator | Complete branch walk, with point path as positive control | **Survives.** AREA reaches the two RNG calls but no `00234DA0` call. It never passes `out_observed` to a callee or writes through it for disjoint valid state. |
| Candidate source always format-0 record 0 | Follow ECX through `003209C0` | **Killed.** ECX becomes the record index in EDX; the wrapper puts zero in ECX for the format class. It converts the underlying success result to 0, failure to -1. |
| Positive attempt limit means that many attempts | Setter and complete automatic selector at 0, 1, 127, 128, 255, 256, 257 | **Killed.** Byte storage and signed use disagree; details below. |
| `+INF` disables the outer distance test | Finite, quiet NaN and +INF outputs, plus candidate success with no output write | **Killed as an unconditional claim.** `COMISS/JB` accepts finite/NaN here, but rejects +INF against +INF. No-output cases change result when only the initial stack slot changes. |
| Minimum radius uses bit 45 or 49 | Original call arguments with each selected bit and adjacent-bit controls | **Survives.** Bits 45/49 pass float 39; bits 44/48 pass float 0. Mask at `0023581D` is `0002200000000000`. |
| A -> B -> A restores inside the window | Complete rotation compare, all copy loops and update order | **Survives as local bank exchange.** Both bank pointers required; equality accepted; tick subtraction and multiplied threshold are low-32-bit values compared unsigned (`00233803 JA`). Other restoration paths are not excluded. |
| Mode 2 retires on approach | Read both opposing comparison branches and action sequence | **Survives for finite distances.** Mode 2 uses `JBE` after distance versus squared per-unit threshold; mode 1 keeps on strict `<` and therefore retires at equality. Unordered mode-2 comparison also takes the retire branch; no claim that ordinary gameplay supplies NaN. |
| The restore helper reverses the serializer | Complete 260-B serializer versus 127-B restore, both pointer references as control | **Killed.** Serializer copies both banks; restore copies only buffer +10 to bank 2, then the field-id pair. It does not access bank 1, tick or window globals. |

### The signed attempt-byte failure

`00239020` compares the signed input with 1, clamps values below 1, then writes **CL** to
`0208D457`. There is no upper clamp. Setter inputs 128/255 remain those bytes; 256 becomes 0;
257 becomes 1. In `00235720`, `TEST DL,DL / JLE` at `00235929` skips the candidate loop for
signed-negative bytes. Afterward `MOVSX EAX,DL; CMP EBX,EAX; JE` at `0023597A` treats the
initial attempt count 0 as unequal to that negative limit, and enters the success bookkeeping.

With a valid injected single lane and keep entry, limit 128 or 255 therefore makes **zero
candidate calls**, returns lane 1, writes the seeded stack vector `(10,20,30,40)` first to
keep-entry `+60`, then `+50`, and sets unit flag `04000000`.
Limit 0 makes zero calls and returns -1; limits 1/127 make exactly 1/127 controlled failing
calls and return -1. A normal successful candidate at limit 1 supplies the positive output
control. These are caller effects under injected preconditions, not monsters observed live.

The active cap separately uses `MOVSX ECX,byte[0208D458]` and a signed comparison at
`00235758`–`00235761`: cap byte 128 rejects even active count 0. Storage can remain `u8` in a
layout, but executable consumers must retain the signed interpretation.

### Output lifetime and boundary qualifications

The automatic caller's observed-distance slot is `[rsp+34]`; no initialization precedes its
address being passed at `00235930`. AREA mode never writes that output, yet the caller reads it
at `00235959` after success. `JB` accepts unordered comparisons, unlike C's plain `<`. In the
controlled provider cases, changing only that stack slot from finite to +INF flips acceptance.
The AREA producer statement is method A; the isolated test substitutes a service that succeeds
without publishing output. Combining them establishes the local dependency, not the actual
stack contents of ordinary gameplay. L-12 remains open. *[Reconciled 2026-09-30 (FABLE): L-12 is SUPERSEDED since; §7.]*

### L-12's static half, and why the live question is one bit (FABLE, Claude Opus 5, 2026-09-20)

*Consumer-side follow-up to §11, from the caller's own frame. It does not touch §11's findings; it narrows what
is left for a live measurement.*

**Nothing in `00235720`'s frame writes that slot.** A sweep of every `rsp`-relative access in the whole 841-byte
body finds exactly two touching `+0x34` — the `lea rax, [rsp + 0x34]` that passes its address at `00235930` and
the `movss` that reads it back at `00235959`. The neighbours are written (`+0x30` at `002357D5` and `00235989`,
`+0x38` at `002357FE`), which is the control that the sweep can see writes at all. The frame is `0xD8` bytes plus
two pushes, so `+0x34` is a local of this function, not the caller's argument area.

**And nothing it calls can write it either, except the callee it is handed to.** Every callee's frame lies below
`rsp`, so no call inside `00235720` can reach `rsp + 0x34`; the only writer is
`Spawn_TrySelectCandidatePosition` through the pointer, and on the AREA branch it never uses it — the validator
`00234DA0` that would write it is called at `00234C37`, which the AREA path branches around on its way to the two
RNG calls. **So the value the caller reads dates from before `00235720` was entered.**

**What it decides.** After a *successful* candidate:

```asm
00235955  test eax, eax
00235957  je 00235964            ; candidate failed -> next attempt
00235959  movss xmm0, [rsp + 0x34]
0023595F  comiss xmm0, xmm6
00235962  jb 00235973            ; BELOW (or unordered) -> accept and leave the loop
00235964  movsx edx, byte [0208D457] ; otherwise: next attempt, against the limit
```

So a successful candidate is accepted **only if the published distance is below `xmm6`**, and because the branch is
`jb` after `comiss`, an unordered comparison also accepts.

**The consequence §11 does not draw: on the AREA path the test is loop-invariant.** Neither operand changes
between attempts — nothing writes `+0x34`, and `xmm6` is not written between `00235930` and `0023596F`. *So the
AREA path cannot accept on a later attempt than the first.* Either the first successful candidate is accepted, or
**every** attempt is retried and the function returns failure at the limit, and which of the two happens is fixed
for the whole call before it begins.

**Which makes the live question one bit, at one address, at one moment:** is the word at `rsp + 0x34` on entry to
`00235720` below the bound in `xmm6`? *It is not a distribution over attempts and not a per-candidate effect.* That
is what L-12 now asks, and it is a much cheaper measurement than "the values reached during ordinary initialized
gameplay".

**Not established here:** what that word actually holds in ordinary play — still live-only; whether any caller of
`00235720` reliably leaves a particular value at that address, which would need the callers' own frames read. *(Answered 2026-10-01, SWE2-STRUCT for OPUS, DD batch 21, static: no caller leaves a value there. `00235720` has one caller, the verb adapter `0050F520` (`0x301A` `btlAtelDecideEntryPointAuto`, reached only through its `.data` slot `01F28510`), which pushes `rbx`, reserves `0x20` bytes and calls, with no other store. The word sits `0xBC` bytes below that adapter's stack pointer, so no frame that is live at the call owns it. It holds whatever the last deeper call through that stack depth left, and that depends on what the script VM ran before. The first half stays live-only, and L-12 is closed SUPERSEDED under the runtime rule (section 7). [Record](../_index/candidates/swe2struct-ddres-b21-1001/README.md), checks W1-W7.)*

AREA's two `IDIV` instructions also need nonzero divisors. A nonzero floating radius span is
not enough: `(max-min)*100` is truncated to an integer at `00234C52`, which can be zero for a
small nonzero span. `arcDeg == 0` reaches a second zero-divisor boundary. The native RNG body
returns at most `7FFFFFFF` (11+10+10 selected bits), so its signed treatment does not itself
make the normal radius negative. No divisor-fault execution is claimed in this package.

Retirement's spawn-backed byte gate is **nonzero**, not exactly 1 (`0023511A`–`00235120`);
its early `pBkei` flag read assumes a valid pointer even though the later pending-flag write
checks for null. Mode-1 comparisons with unordered distances do not take the near/keep `JA`;
with an eligible slot they therefore reach retirement. These are original branch facts, not
evidence that a native valid unit has a null keep pointer or nonfinite position.

### Propagation and remaining work

Active prose, formulas, modding notes and this page's status are corrected. The earlier audit
history remains intact. FABLE/OPUS receive the signed-byte, output-state and save-restore
corrections for dependent types, contracts, executable specifications, probes and scientific
questions; those consumer changes remain open until their owners agree. ~~The sibling
`why-the-enemies-you-killed-come-back.md` also still describes 296 records of 128 bytes and
needs the already-proved 64-by-592-byte correction. This page does not silently edit it.~~

> **THE SIBLING WAS CORRECTED THE NEXT DAY, and this paragraph did not notice (checked 2026-09-21,
> FABLE).** [`why-the-enemies-you-killed-come-back.md`](why-the-enemies-you-killed-come-back.md)
> carries *"Correction — 2026-09-13 (ASTRA's independent falsification, consumed by FABLE)"*, which
> states **"The bank is 64 entries of `0x250` bytes, not `0x128` records of `0x80`"**, reconciles it
> as `64 x 0x250 = 0x128 x 0x80 = 0x9400`, opens with *"Two banks of 37,888 bytes each — 64 keep
> entries of `0x250`, copied in `0x128` chunks of `0x80`"*, and annotates the old row in place rather
> than deleting it. **That is exactly the correction this sentence asks for, and it was made nine
> days before this reading.** Not silently editing the sibling was right; leaving the request
> standing after it was answered is what this note fixes. **The other consumer changes named above
> are not re-checked here** — only the one this paragraph names by file.

*Reconciled 2026-09-30 (FABLE): the three corrections' consumers, found by grep for the restore helper and the attempt
byte.* [The placement contract](CONTRACT-spawn-placement.md) and [height and tunables](spawn-placement-height-and-authored-tunables.md)
carry the signed attempt byte (**agree**). [The save payload map](../19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/the-save-payload-field-map.md)
lists no restore read of either image's bank 1 (**agrees**). [Gambit evaluation and enmity](../09-Combat-AI-And-Gambits/gambit-evaluation-and-enmity.md)
still says the restore helper "copies them back" of both banks (**disagrees; routed to that page's owner**, not edited
here). No open board item names this page other than FABLE's DD task (101 DONE, 1 ACTIVE, board revision 41540). *(Rechecked 2026-10-01, SWE2-STRUCT for OPUS, DD batch 21: the routed disagreement still stands, because the gambit page still says the restore helper "copies them back", so it stays with that page's owner. The two review requests on this section, ASTRA-CONTRA-FABLE-SPAWN-LIFECYCLE and ASTRA-CONTRA-OPUS-SPAWN-LIFECYCLE, are DONE.)*

L-12 and L-13 are open above *(as of 2026-09-12; both SUPERSEDED since, §7 — reconciled 2026-09-30, FABLE)*. The 2026-09-12 crossref-clean result in §8g is historical;
~~`crossref_clean` is now false because this amended citation surface has not had a fresh graph~~
~~audit.~~ *(answered: see the front matter, `crossref_clean` true, and the status line - a fresh graph audit of this page reports 0 findings, owner re-status 2026-10-01; 2026-10-02, OPUS)* Neither a green local replay nor this independent pass completes L1/L2 or warrants
the programme's final audit.

## 12. Save-image selection and continuation — ASTRA, 2026-09-12

> **Reading §§12-29 after 2026-09-27 (reconciled 2026-09-30, FABLE).** These sections are ASTRA's dated packages.
> Each closing line that calls L-12 or L-13 open was true when it was written; L-12 is SUPERSEDED (2026-09-26) and
> L-13 SUPERSEDED (2026-09-27), and §7 gives both dispositions and where L-13's live-only residue went. Lines that say
> FABLE, OPUS or peer review "remains pending" record the routing at the time: at board revision 41540 no open item
> names this page except FABLE's DD task, and all 101 other items that name it are DONE. The remaining "not
> established here" statements bound what each package read of the load menu, the save container and the resource
> queue. They are not spawn residue of this page; a question about those mechanisms belongs to the page that owns it
> (the request router, the save-image pipeline, the map pack).
>
> *Itemized 2026-10-01 (SWE2-STRUCT for OPUS, DD batch 21, [record](../_index/candidates/swe2struct-ddres-b21-1001/README.md)).* The record dispositions each such line in sections 11 to 29. Every review those lines call pending is DONE: no open board item names this page except the batch 21 task. The lines about live delivery, timing and chronology on an actual load are L-13's live-only residue, which still has no carrier; the record proposes it to OPUS as one runtime row. The other "not established here" lines are stated limits of their packages, as above. Two were answerable statically and are answered in place: the script verbs behind `00354B20` and `00354E80` (section 15) and the child sort (section 19.4).

**Player version.** Two enemy snapshots in a save are alternatives used by different runtime
branches. The restore routine chooses one or can skip both; it does not put both snapshots
back into the game in sequence. Area initialization has its own bank exchange afterward or
elsewhere in the lifecycle. Their full ordering remains L-13, not an assumed load round-trip. *[Reconciled 2026-09-30 (FABLE): L-13 is SUPERSEDED since; §7.]*

[Complete original bodies and dispatch-table bytes](../_experiments/evidence/spawn-load-continuation/README.md)
support method A only: 20 bodies with exact byte/hash coverage, no new emulator or live run.
Previously completed EXP-057 execution is not replayed. Active/staging getters are re-read
only to establish each address origin in this caller analysis.

### Three mutually exclusive restore outcomes

`005843E0` is 174 B, SHA-256
`fb33b31d11a773e9918dab464e7ffd3ba75b409cf00498514d68f83f19e2f046`.
Its two `002EF640` calls return the fixed active **whole-image** base `02164280`.
Define `state = *(02EBF190)`, `f = (state[+4] >> 12) & 1` (the entire 17-B
`00236760`), `mode = byte[02AEE4D8]` (8-B `00394450`) and `h = active[+57] & 1`.
These are numeric branch inputs; no gameplay names are inferred from them here.

| Condition at entry to the branch | Native calls in order | Following direct effects |
|---|---|---|
| `f == 0` | `002EF410(active+4E660)` metadata restore; `00269A20(active+E240)` group restore; `00233550(active+E440)` keep restore | Publish byte `active[+4E660]` to `0208D455`. |
| `f != 0` and (`mode != 3` or `h != 0`) | `00269A20(active+2E450)` group restore; `00233550(active+2E650)` keep restore | Clear state `+5B04` bit 1, then publish the same metadata byte. |
| `f != 0`, `mode == 3`, `h == 0` | Neither group nor keep restore | Still clear state `+5B04` bit 1 and publish the metadata byte. |

The branch after the A call jumps directly to the common byte publication. B is not a
second call following A. The group helper copies **0x200 bytes**, four iterations of 128,
into `02099FF0`; its inverse `0025D8E0` supplies the positive size/direction control.
Each keep-helper invocation still writes only bank 2, as §11 proves.

The metadata helper `002EF410` copies metadata `+8..17` to state `+5AE0..5AEF` and metadata
`+28` to state `+5B04`. If metadata `+18` bit 1 is set, it copies `+18..27` to state
`+5AD0..5ADF` and passes float `+20` to `003139D0`. If metadata `+8` bit 0 is set, it passes
floats `+C/+10` to `00304790/003047C0`, then sets state `+5B04` bit 1 and clears bit 0.
Those three wrappers call `003EBC50` and tail-jump `003EBD00` with selectors 1/2. Their
downstream effects are not established here; the absence of a direct spawn-tick reference
in the metadata helper is not a transitive no-effect proof. *(2026-09-30, FABLE: the records these wrappers arm are
the value / bound / rate / arrived countdown rows that [the battle runtime mode ladder](../00-Engine-Core-Runtime/Battle-Runtime-Mode/battle-runtime-mode-ladder.md)
reads together with their row updater; its §2c and the register's FO-1 place them in the summon sequence. What those
countdowns drive is that page's question, not this one's.)*

### Capture maintains the alternative snapshot

`00584580` (143 B) works from staging whole-image base `021BA940`, returned by `002EF620`.
With `f == 0`, it captures group A, keep image A and metadata, then stores sign-extended
`byte[0208D455]` as metadata dword `+0`. With `f != 0`, it captures B, updates metadata through
`002EF510`, and then **copies A from the active image into staging**: `002EF7C0` copies group
A's `0x200` bytes, and `002EF740` copies keep image A's `0x20010` bytes. It ends with the
same signed-byte-to-dword metadata store. Both copies are complete original loops, not an
inference from a function name.

The address coordinate matters: the payload starts after the `0x200` header. Therefore:

| Object | Whole-image offset (hex) | Payload offset (hex) | Size (hex) |
|---|---:|---:|---:|
| Group A | `E240` | `E040` | `200` |
| Keep image A | `E440` | `E240` | `20010` |
| Group B | `2E450` | `2E250` | `200` |
| Keep image B | `2E650` | `2E450` | `20010` |
| Transition metadata | `4E660` | `4E460` | `2C` |

`00229B40` (469 B) is another capture path: after its own native prelude and explicit copy
loops, input ECX zero selects A and nonzero selects B, then `002EF540` copies `2C` bytes of
metadata from `021B28E0`. Its preceding calls and snapshot-coherency policy are not silently
included in these local copy/selection conclusions.

### Where the restore and rotation are reached

The complete 1,777-B `00582860` controller and its actual 19-entry dispatch table at `00582F54`
place the restore branch under **message code 18** (`[RDX]`), at `00582E81`. Controller `+C4`
bit 4 must be set; controller byte `+598` must be zero to call `005843E0`. That call is
preceded by `001831A0` and a dword store of 1 to `0209AC10`, and followed by `00182D40`.
The same outer bit-4 branch proceeds through `00394520`, conditional `00394400` and then
`00584210`. The table's message-1 entry points elsewhere, providing a dispatch control.
This proves an original-code caller path, not a live successful-load event or the meaning of
every controller message.

The complete 390-B `002342F0` checks global `02089300` before any area work. Its active branch
sets cap 28, executes the listed native initialization calls, and calls rotation `00233780`
at `00234423` before later initialization calls. The rotation's exact exchange/wipe and tick
write were already read in §11. This identifies a second local path; it does **not** by itself
order that path relative to controller message 18, prove intervening calls preserve the banks,
or prove which tick/current-bank state an actual load reaches. L-13 remains open at that
specific boundary. *[Reconciled 2026-09-30 (FABLE): L-13 is SUPERSEDED since; §7.]* FABLE/OPUS own propagation to the save payload map and dependent contracts.

## 13. The immediate load wrappers do not initialize the area — ASTRA, 2026-09-12

**Player version.** The routines immediately around restoring a save perform small runtime/input
updates. Enemy-area initialization comes through separate callers. One broad initialization path
also clears the group-persistence table after the bank-rotation call, so a correct load sequence
must account for when the saved group data is imported relative to that reset.

[Original bodies, constants and local call controls](../_experiments/evidence/spawn-load-area-order/README.md)
are method A only. Eleven catalogued complete bodies and the exact three-byte shipping
`0016D6A0` body (`RET 0`, **not a harness stub**) were read. No new original-code execution or
live observation. Existing EXP-056/057 and the normalization page were recovered before reading
new boundaries; their omitted native effects remain omitted evidence.

### The two calls around restoration

`001831A0` calls `001D8A60`, then tail-jumps to `001D8A90` with the returned pointer. The getter
reads `01F82CD8` after calling the shipping no-op with a non-null predicate; that call is not a
null guard. `001D8A90` reads float object `+8`: only ordered zero, including negative zero,
sets byte `+1D` to 1 and stores positive zero at `+8`. Nonzero and unordered values leave both
fields alone. The pointed object must be valid.

`00182D40` instead gets `*(01F7FFE0)` through `00198790`, then tail-jumps `001986E0`. If object
byte `+3A` bit 2 is set, the callee stores byte `+3B = 1` and clears that bit in `+3A`, in that
order. It otherwise returns. Both complete call chains have only these local effects and the
getter/no-op calls; neither invokes area initialization. The actual `002342F0` edges in the
two callers below are positive controls for distinguishing such an invocation. These pointer
field operations do not establish ordinary object initialization or arbitrary alias safety.

### The actual area-init callers

The 1,185-B `00266D10` calls `002342F0` at `00267136` after a broad initialization sequence.
Later it supplies two **0x200-byte zero fills**, first to `02099DF0` (`0026717A`) and then to
the group-persistence bank `02099FF0` (`0026718E`). They are native memset calls with explicit
zero/size arguments. They do not clear the two heap keep banks by these addresses.
The existing [boot page](../00-Engine-Core-Runtime/what-the-engine-fixes-at-boot.md) places
`00266D10` under `0022A0B0`; this package does not infer how often boot is reached from that name.

The other caller, `0026CE60` (1,332 B), selects a field-manager record at
`02098E10 + sign32(ECX) * 0x288`, saves/restores global current-manager pointer `02099D70`, and
skips initialization when manager `+10` bit 0 is already set or byte `+13` is zero. On the
admitted path it obtains/stores manager `+8`, calls `00266C50(manager)`, and **only for index
zero** calls `002342F0` at `0026CEC6`. Other indices do not invoke this area initializer.
There is no local manager-index bounds check before forming that address. Subsequent authored
record processing and native callbacks remain distinct from proving that the area call occurs.
Direct caller leads are `0025BFB0` and `0032F1B0`; their integration/order is still L-13. *[Reconciled 2026-09-30 (FABLE): L-13 is SUPERSEDED since; §7.]*

### Metadata callback effects narrowed

The previously unread `003EBC50`/`003EBD00` pair operates on 20-byte records at
`02B5EBC0 + sign32(selector)*20`. `003EBC50` stores truncated input float as dword `+0`, target
R8D at `+4`, a signed step at float `+C`, clears byte `+10`, assigns byte `+11` according to
whether that step is ordered zero, and finally stores the **original input float** at `+8`.
Its earlier integer-to-float `+8` write is overwritten; native order is retained in the raw body.
`003EBD00` compares dwords `+0/+4`: unequal sets byte `+10`, equal sets byte `+11`; it does
not clear the other byte.

The called `00290180` is the actual six-byte shipping `MOV EAX,2; RET`, so this path selects
step magnitude bits `3C889A05` (about 0.016675) from `00D1181C`; the alternative 0.02 constant
is not selected by that original callee. Integer start >= target negates the step by XOR of
the sign bit. The two wrappers using `MAXSS` compare with **2.0**, not zero, before calling
this setter. Selectors 1/2 from §12 address the corresponding records; none of these bodies
calls the area initializer or directly addresses the spawn transition tick. The later consumer
of these records and its scheduling are not established here, so this is not a transitive
no-timer-effect claim *(the records are the countdown rows noted in §12, 2026-09-30)*. L-13 remains open for the native load-to-area dispatch sequence. *[Reconciled 2026-09-30 (FABLE): L-13 is SUPERSEDED since; §7.]*

## 14. Queued teardown and resource completion enter area initialization — ASTRA, 2026-09-13

**Player version.** Preparing an area involves queued work and resource completion, not just
copying saved enemy data. One queued request can initialize actors, clear the party roster,
and then unload the selected managers. The order matters: requests added during a pass may
run immediately, wait until later, or be cleared by the operation already in progress.

[Original instructions and controlled queue evidence](../_experiments/evidence/spawn-manager-dispatch/README.md)
retain ten complete catalog extents, reuse the previously read `002628B0` body, and execute
only the 179-byte `0025BFB0` in isolation. Its two callbacks are controlled providers. Twelve
complete cases follow two feasibility controls; callback arguments, boundary state, reads,
writes and final memory are checked. Neither callback's native effects nor actual load
scheduling are established by that execution. No live game or PC control was used.

### The world-tick prologue consumes a mutable queue

`00314020` calls `0025BFB0` at `00314078`, before its mode-dependent field/menu loops and the
deferred mode request at `003140BA`. This entry is not gated by the tick's field-mode test.
It does not mean the full battle frame advances behind a menu; it means the prologue can
process queued lifecycle work there when its own conditions admit it.

`0025BFB0` reads dword `02099ABC`. Zero returns immediately. With **bit 0 set in the initial
read**, it first visits selected manager indices **4, 3, 2, 1, 0**, calling `0026CE60(index)`
at `0025BFF6`. It reloads the mask after each call. After that sweep it zeroes the four roster
pointers at `0209A1F0..0209A20F`, using two 16-byte stores at `0025C017`/`0025C01F`.
This clear still occurs if a callback has removed bit 0 after admission.

Then, whether or not initial bit 0 was set, it visits selected indices **4 down to 0** again,
calling `002628B0(index)` at `0025C036`. After each return it reloads the global, clears that
index's bit, and stores the result at `0025C047`. The first sweep does not itself clear bits.
The loop never visits bit 5 or above; a high bit alone remains pending and does not clear the
roster. With inert providers, mask `1F` produces all five initialization calls, the roster
clear, then all five unload calls. Mask `10` produces only unload(4) and leaves the roster.

The [existing field-gate contract](../04-Actor-Entity/CONTRACT-field-runtime-pass.md#13-runtime-validation)
already ran the original writer `0026A5F0`: requesting manager 0 recursively requests 1, 2,
and 3 before setting bit 0. Its 74-byte body agrees; that completed experiment was not rerun.
This is one established producer, not an exhaustive census of every possible writer.

The new isolated controls distinguish a changing queue from an entry snapshot:

| Controlled callback intervention | Observed original-wrapper behavior |
|---|---|
| init(4) clears bit 0 from initial mask `0x11` | init(0) is skipped; the roster still clears; unload(4) follows |
| init(4) adds bit 2 to initial mask `0x11` | init(2) and unload(2) occur in the same pass |
| unload(4) adds bit 2 to initial mask `0x10` | unload(2) occurs in the same pass; no initialization sweep is retroactively started |
| unload(0) adds bit 4 to initial mask `0x1` | bit 4 remains for a later pass, because index 4 has already been passed |
| unload(2) requests its own bit again | the caller's post-return clear removes that request |

These are **explicit callback interventions**, not observations that ordinary FF12 callbacks
perform those changes. The replay checker catches a corrupted roster publication; the outcome
check catches swapped initialization order. Returns alone would not distinguish these effects.

The reused 1,689-byte `002628B0` explains why the outer routine is not merely a roster clear:
it has a live-manager branch, calls record release `0025B070` except for manager 4, and later
clears manager `+10` bit 0 and byte `+13` (`00262DA8`/`00262DB3`). It can call the manager's
`+108` callback at `00262F1E` before zeroing that pointer. Reading these instructions does not
establish every callee's effects or prove which new requests that callback issues.

### Resource completion is a second route

The 136-byte `0032F1B0` performs its lighting-related prelude only when signed manager index
is **positive**. A non-null `022C6E20[index]` enables binding through `0037AA90` and a write of
`0037B290(index) + 1` to manager `+1FC`. The common tail calls `0026CE60(index)` at `0032F227`;
**zero and negative inputs branch straight to that tail**. The manager initializer's own
gates still apply (§13). The final tail is the 32-byte `00263C30`: it returns manager `+20`
when `+10` bit 0 is set, otherwise zero. Neither routine locally bounds the manager index.

The resource callbacks use a different mask: qword `022C6E48[index]`. The 122-byte `00330110`
stores its packed input's low-32-bit, low-nibble-cleared pointer in `022C6E20[index]`, clears
pending **bit 16**, then calls `0032F1B0` only when the **old mask was nonzero and the new
mask is zero**. If only bit 0 remains, it clears manager `+11` bit 3 but does not finalize.
An already empty mask does not finalize again. The original directory route and its wider
resource barrier are described in [section 014](../25-EBP-Script-Container/Sections/section-014.md).

`0032F850` has the corresponding bit-1 completion path only after a **nonempty definition
payload**. An empty payload clears the availability byte for a valid manager and returns
before clearing that pending bit. For nonempty input, the native order is definition binding
through `0026C8C0`, callback installation through `00268630`, the pending-bit update, and the
same nonzero-to-zero finalization test. Its catalog extent ends in the out-of-range branch's
call to `00809728`; that failure path and the native binders were not executed here.

The complete 936-byte `0032FCA0` calls unload `002628B0` and then load-state reset `0032ED80`
during setup, before publishing requested resource IDs, submitting resources and setting pending bits. The complete
110-byte `0032FC30` calls it, then `0025D4D0`, and **only after those calls** ORs bit 0 into
manager 0's pending mask. Thus resource bits draining while bit 0 remains is not sufficient
for these callbacks to finalize. The primary EBP dispatcher `003304A0` similarly clears its
own bit 17 at the tail and applies the same transition test after section callbacks.

**L-13 remains open.** *[Reconciled 2026-09-30 (FABLE): L-13 is SUPERSEDED since; §7.]* The queue admission and two area-init routes are now explicit. Still
needed are manager-0 pending-bit-0 release and its scheduling, the connection from actual
save-controller completion to the resource request, and the intervening native bank/timer
effects. No save/load roundtrip or integrated parity follows from these local paths. The
party-clear contract and world-tick prose need peer-owned propagation of the newly read
prologue behavior; the existing save/type/specification return also remains pending.

## 15. Map setup releases the pending latch — ASTRA, 2026-09-13

**Player version.** Finishing the map setup can release the hold that keeps actors from being
initialized too early. Pictures, placement and navigation are prepared before that release.
Other resources can still delay initialization. This establishes a piece of the loading order;
it does not yet prove the whole sequence after selecting a saved game.

[Primary latch and caller evidence](../_experiments/evidence/spawn-pending-latch/README.md)
is **method A only**. Ten whole catalog extents were read and checked against the shipping
image; no new isolated test or live control. The adjacent `0032F6F0` lead was a path-string
rewrite helper, not a pending-state helper, and is retained as a rejected lead.

The 93-byte `00332130(index)` is the separate release. It sign-extends the index, reads qword
`022C6E48[index]`, clears **bit 0** and publishes the new mask at `00332154`. If the result is
zero it clears manager byte `+11` bit 3 through the getter `00263FF0`. It calls the finalizer
`0032F1B0(index)` at `00332178` **only when the old mask was nonzero and the new mask is zero**.
Thus old mask `1` finalizes; `0` clears the manager flag but does not finalize; `3` becomes `2`
and does neither yet. These are readings of the original branch conditions, not new executed
cases. There is no local index bound or returned-manager-pointer null guard.

One caller is the 266-byte map setup `00378120`. Its original order is:

1. Publish the current map pointer; upload picture 0 through `003C63A0`; apply placement 0
   through `00379870(0)`.
2. Conditionally hand over the mode-0 map through `0026E7D0`; process the current map through
   `0026E760`; publish navigation pointer `02ADD008` and call `00384160`.
3. Copy three resulting navigation globals, set `02ADD108 = 10`, and prepare the final
   `003AFD40` input using the object at `0209A660`. That object is dereferenced without a
   null guard; ordinary initialization of the object is not proved by this caller.
4. **Tail-call `00332130(0)`** at `00378225`.

The 296-byte map binder `003775D0` reaches that setup at `003776DD` when bind-mask
`02ADD0F0` bit 3 is set. It clears that bind bit **after** setup returns, at `003776E2`, then
stores ready word `02ADD0D8 = 1`. Consequently actor finalization reached through the tail
above can occur before those two outer publications. The [map-pack page](../03-World-Area-Field/Map-Pack/the-map-ctrl-pack.md#34-binding--003775d0-and-00378120)
already establishes the resource-completion route into this binder. Its remaining native
callees are not proved effect-free by the call order recorded here.

The release is not exclusive to manager 0. The two complete script adapters `00354B20` and
`00354E80` form a signed, clamped **1..3** index from a popped argument plus one; two further
gates precede the release call. Their actual script invocation and those gates' meanings are
not established here. *(Answered in part 2026-10-01, SWE2-STRUCT for OPUS, DD batch 21, static: the two adapters are the script verbs `eventplay` (`0x00EB`, `00354E80`) and `eventplay_ec` (`0x00EC`, `00354B20`) in the dispatch table, so a script reaches them by playing an event. Which scripts call them is a script census this note did not run, and what the two gates mean is a stated limit here; [the event-slot panel](../00-Engine-Core-Runtime/Developer-Tuning-Console/the-event-slot-panel-and-its-dead-feeder.md) reads the event-queue call inside both. Checks E1-E3.)* `003C9FD0` is a separate manager-3 state controller: only input 3 with
`02B47750 != 0` and `0032F6E0(3) == 0` enters its state handling. State 3 calls release(3)
when `0032F6C0(3) == 0`; state 1 begins a resource request; state 4 calls `00332190`. The
special-presentation caller `00306760` was already documented elsewhere and was not replayed.

Two setup distinctions prevent another false dependency. `0025D4D0` is a 23-byte manager
`+10` **bit-1 clear**; it does not release the resource mask's bit 0. `0032ED80` resets the
**whole resource mask to zero** at `0032F0FF` after its resource-pointer cleanup, without
calling this finalizer. Its later index check is after earlier indexed accesses; its failure
branch ends in a call to `00809728`. Native resource cleanup and that failure path were not
executed. Neither a zeroed mask nor a cleared busy flag alone proves actors were initialized.

The existing image-base reference export finds the known indexed reset `0032F0FF` but omits
the known RIP-base release in `00332130`. The receipt retains this positive blind-spot control:
the export supplies leads and cannot prove an exhaustive writer set.

**L-13 is narrowed, still open.** *[Reconciled 2026-09-30 (FABLE): L-12 and L-13 are SUPERSEDED since; §7.]* The manager-0 latch release and its map-bind ordering are
now identified. The remaining connection is actual save-controller completion to the field
resource request, plus the native binding/initialization that establishes field IDs, current
bank and transition tick in that sequence. L-12 and consumer review also remain open.

## 16. Field binding and persistence preparation — ASTRA, 2026-09-13

**Player version.** Fields can share a persistence group, letting their scripts retain saved
state while the player moves within that group. A different temporary table is cleared each
time the field-reset routine runs. Loading introduces further guards. The original code now
connects these resets to field-data binding and connects field requests to snapshot capture;
the complete sequence after choosing a saved game still needs proof.

[Original bodies and source checks](../_experiments/evidence/spawn-field-bank-preparation/README.md)
are **method A only**: nine bodies, no new isolated execution or live game. FABLE's existing
[script-storage section2.5](../01-Script-VM-Native-Bridge/Interpreter-Core/script-variables-and-their-storage-classes.md#25-what-a-field-group-is--the-map-reference-rows-persistence-group-id-fz-24-2026-09-12)
already identifies the persistence-group comparison and corrects the bit-5 interpretation.
That meaning is recovered here; the new integration concerns binding and transition order.

### Binding establishes the small banks before resetting them

`0026C8C0(index, definition, optionalAllocator)` computes manager
`02098E10 + sign32(index)*0x288`, saves and replaces current-manager global `02099D70`,
stores the definition pointer and index, and initializes manager fields. Its common binding
stores are distinct from the spawn-keep heap banks:

| manager field | value published by original binding |
|---|---|
| `+48` | persistent payload returned by `002EF2B0` |
| `+50` | definition base plus **zero-extended u32** at definition `+48` |
| `+58` | `02099DF0`, the `0x200`-byte `scratch1` script bank |
| `+60` | `02099FF0`, the `0x200`-byte group-persistent `scratch2` bank |
| `+68`, `+70`, `+78`, `+80` | definition base plus **sign32** offsets at `+20`, `+24`, `+28`, `+2C` respectively |
| `+98` | native local-variable resolver `00264E30` |

It writes word `+13 = 0x0101` at `0026CC6C`. After the binding stores and additional native
work, **only manager0** calls `0026DB30` at `0026CD60`. The common tail restores the prior
current-manager pointer at `0026CDC0` before tail-calling `003DD790(index)`. These are local
store/call facts; many native callees and the initial state remain outside this package.
There is no local manager-index bound or section-offset range validation in the binding body.

The first byte collector incorrectly treated catalog count 1,330 as a contiguous length and
stopped at `0026CDEE` inside the second range-failure call. The corrected whole extent is
byte-verified: instructions end at `0026CDF3`, so `[0026C8C0,0026CDF3)` holds 1,331 bytes —
1,330 of them instruction bytes, which is the catalog count. The `INT3` at `0026CDF3` is
counted into the extent by the same post-noreturn pattern as `0026CDED` — both sit after
calls to the noreturn `__report_rangecheckfailure` `00809728` — and `INT3` fill runs to the
next body at `0026CE00`: extent **`[0026C8C0,0026CDF4)`, 1,332 bytes**. The incomplete
receipt is preserved as a failed collection.

### Exact reset guards

The 270-byte `0026DB30` first performs other reset calls and clears the 32-byte party roster,
then clears `scratch1` at `0026DB80` with size `0x200`. Its group decision reads `u16 +6` of
two 8-byte rows in the **map-reference table at `02099D88`**, not the field-record table at
`02ADD100`. Each lookup requires both `02099D88` and `02099D90` non-null; the row base is
root plus **sign32(header+4)** and the signed field index is multiplied by8. The row address
is also tested for null; no table-bound check follows. The current-field getter `003148F0`
clamps negative payload `+1044` to0; previous-field getter `00314870` returns signed `+104C`
without that clamp. A skipped lookup contributes group value0.

If current and previous group values differ (`0026DBEB`), the routine clears `scratch2`
at `0026DC11`. Payload `+1062` bit5 gates **only** the preceding call to `003149E0`, whose
original 21-byte body clears bit2 of the same byte (`AND 0xFB`). It does not prevent the
bank wipe. Independently, options getter `003148D0` returns payload `+1054`; bit3 triggers
another `scratch2` wipe at `0026DC2E`. Both conditions true can therefore wipe the bank twice.
Which named fields share these authored group values is not established by this code reading. *(2026-09-30, FABLE:
the authored data answers it. The group is word `+6` of each `map_ref.bin` row, and
[the map-menu location graph](../02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/lmap-menumap-location-graph.md)
§10.4 joins it to the 48 named sub-locations, 47 distinct groups; FZ-24.)*

The 88-byte `00268320` has a different policy:

| operation | original admission |
|---|---|
| clear `scratch2`, size`0x200`, call`00268345` | dword`0209AC10 == 0` **and** dword`01E0C3EC != 0` |
| clear `scratch1`, size`0x200`, call`00268359` | unconditional within this body |
| set payload`+1061 = 1`, store`0026836C` | a **fresh read** of dword`0209AC10` is zero |

The last branch leaves `+1061` unchanged when the dword is nonzero; it does not clear that
byte. This answers the local guard portion of weather question **F-3**, pending its owner's
integration. *(2026-09-30: the register's F-3 reads ANSWERED 2026-09-13 with this guard.)* Meanings, all writers and actual lifetime of the two controlling globals remain
separate. The earlier controller receipt (§12) proves `00582860` writes `0209AC10 = 1` at
`00582E98` **before** save restore `005843E0`. Preservation of that value until a later reset
has not been proved. The broad initializer `00266D10` still has the independent two-bank wipe
recorded in §13; these guarded paths do not establish that every possible wipe is guarded.

### The field request also prepares a snapshot

The complete 563-byte `003145E0(fieldId, secondValue, options, nonblocking)` can return1
before staging when nonblocking is nonzero and native `0032E520(1)` returns nonzero. Otherwise
it queues manager teardown1,2,3 and writes the following after native preparation calls:

1. Old payload`+1044` goes to `+104C`; the requested field goes to `+1044` and deferred-request
   global `01EED064` at `0031467F`.
2. Old `+1048` goes to `+1050`; the second input becomes `+1048`; options become `+1054`.
   `00264F90(fieldId)` supplies `+1058`, and the field is repeated at `+105C`.
3. Payload`+1062` bit5 is cleared at `003146DE` before later preparation. In the nonnegative
   request branch, field12 reaches a write of `01E0C3EC = 1` at `00314759`.
4. If the nonnegative-request path's `0020E500` gate succeeds, three stack buffers are zeroed,
   then calls occur in order: `00229B40` metadata/capture selection (`003147BB`), `005844A0`
   header preparation (`003147DF`), `00584580` group/keep capture (`003147E4`), `00583260`
   storage work (`003147E9`). The selection argument comes from the state-bit12 getter
   `00236760`. Those capture bodies were already recovered in §12; they were not replayed.

The earlier whole `00314020` receipt (§14) consumes **the same deferred-request global** and
calls `0032FC30(0, request)` at `003140BA` after the queue prologue `0025BFB0`. This supplies
a native request/capture-to-resource edge. It does not establish that every request captures,
that the downstream storage succeeds, or that actual successful save loading invokes this
stage in the required order.

**L-13 stays open:** actual save completion to field request, intervening flag writers and
native initialization must still establish the restore/rotation/current-bank/tick sequence.
The earlier physical bank copies and local call edges are valid evidence, not integrated
parity. L-12 and peer-owned type/contract/specification corrections remain open. *[Reconciled 2026-09-30 (FABLE): L-12 and L-13 are SUPERSEDED since; review routing in the note under §12's heading.]*

## 17. The restore request and its controller bridge — ASTRA, 2026-09-13

**Player version.** Loading has its own way to request the saved field again. The load menu
sets a request flag that the area controller reads before resetting small script tables and
requesting that field. The code connects those stages. Their completion-message order
relative to restoring the saved enemy snapshots still needs proof.

[Primary route and caller evidence](../_experiments/evidence/spawn-restore-request/README.md)
contains thirteen whole method-A bodies, two original script-dispatch records and exact
anchors reused from the earlier load-controller receipt. No B/live run. The runtime-header
validator was already established by [EXP-058](../_experiments/EXP-058-save-validator-controls.md);
its included body corroborates the caller branch without another experiment.

### Requeue differs from staging a new transition

The 173-byte `00314530` calls `001831A0`, requests teardown for managers1,2,3,0, sets payload
`+1062` bit5, and copies payload`+1044` into deferred-request global`01EED064` at `00314575`.
It copies that global to payload`+105C` at `00314586`. The body then prepares overlay/input
state, sets first-start word`022C2528 = 1`, calls `001D6C40(request)`, and tail-calls
`00182D80`. Its direct body has neither the pending-request admission test nor the
metadata/group/keep capture calls of `003145E0`. Native effects of unread callees remain
separate; this is not a transitive absence claim.

The five-byte `00267C90` is an actual shipping jump to `00314530`. The call-edge export lists
callers of this thunk separately; finding no incoming edge to the final address alone would
miss them. Existing raw-call leads were recovered and then checked in whole original bodies.

The 233-byte ordinary requester `00314440` supplies a useful distinction. It can replace
field0 with field12 when `00408B00()` is zero. This is an explicit shipping condition:
`00314465` skips the substitution when the getter is nonzero. The getter reads byte
`02B62DB9`; reset`00408BA0` writes0 to it at`00408BBC`. On a path where that reset
remains the last write, field0 becomes12. The reported exact-target RIP-reference
census does not by itself establish a lifetime invariant covering alias or overlapping
stores, so the conditional form is retained. No alternate writer or normal-play
nonzero has been demonstrated. [Primary review and limits](../_experiments/evidence/config-gate-review/README.md)
return that proof boundary to OPUS; the config-page/PC-2 consumer review remains open.
*Status 2026-09-26 (FABLE, Claude Opus 5.5): that propagation was made. OPUS adjudicated the review on 2026-09-13 in the config page section 6, narrowing "unreachable" to "unreachable unless the byte is written from outside the image or through a runtime-computed pointer", and the register's `PC-2` now reads ANSWERED at that scope. The conditional form kept here is unchanged by it.*
If deferred request`01EED064` is already nonnegative, it returns0 without staging. Otherwise it calls `003145E0`; the nonblocking
branch propagates a nonzero result before later work. Successful staging is followed by
manager0 teardown request at `003144A1`, conditional overlay preparation and further
input/control calls. Thus a return0 alone does not prove a new field was staged.

### The area controller reads the load controller's request bits

The complete 924-byte `00280140` is a message handler. Its message1 branch stores
`*(0209AC30) + 0x3F8` into handler`+C0` at `0028044C`. The pointed-to dword`+8` is therefore
**context`+400`**. That branch clears its bits8,9,10 and initializes related fields.

For message18, after other native preparation, the handler chooses between two routes:

| pointed-to flags | original route |
|---|---|
| bit9 set | clear bits9/10; call`00268320` at`002801FF`; if`0020E5A0()==5`, clear payload`+1061` and call`0020E4E0`; call requeue thunk`00267C90` at`0028021F` |
| bit9 clear, bit8 set | clear bit8; destination12 calls`003603E0`; other destinations call ordinary requester`00314440(destination,0,0,0)` at`0028027C` |
| neither bit9 nor bit8 set | skip both request routes |

After the route, the common tail performs further calls and clears fields on the object
currently in `0209AC30`. The code does not independently prove the object's lifetime or that
its pointer stays unchanged between all these reads.

The **55-byte `00285E60` writes the matching flags**: it ORs bit9 into `*(0209AC30)+400` at
`00285E6B` and bit10 at `00285E7C`, then calls `00233C10` and tail-calls `002CFD10(-1)`.
The input argument is unused by these stores.

The earlier whole `00582860` receipt proves where this setter is reached. Its shipping
dispatch table maps **message12** to `00582B2C`; the handler compares the qword at message`+8`.
Subtype **16** reaches `00582CB3`, sets the load controller's own `+C4` bit4, and calls
`00285E60` in either branch of its mode test (`00582CD0` / `00582CE6`). The same controller's
**message18** reaches the restore/normalization path in §12: with bit4 set and byte`+598`
zero it sets `0209AC10 = 1` before `005843E0`; normalization follows the outer bit4 path.
Its later helper `00582FC0` handles two resource fields and optional pointer frees; it has
no direct requeue call. Unread resource-callee effects are not excluded.

This establishes the **shared request storage and native producer/consumer edges**. It does
not yet order the two controllers' message18 deliveries. In particular, it does not prove
the bank restore and the load-mode store happen before the area controller's reset/requeue.
The earlier frontier's search for a save-to-`003145E0` connection was too narrow: this
restore-specific route must be accounted for without requiring the ordinary staging path.

### Additional callers and a script-visible lifetime

The 130-byte `0036FCC0` calls `00268320` then the requeue thunk, with native logging calls
between them. The 530-byte `00394130` has a message2/state1/countdown-zero path gated by
native readiness. It tests active image`+68` through `00255260`. A rejected stamp resets the
active image and uses ordinary requester`00314440(0,0,0,0)`; an accepted stamp restores
40 bytes from controller`+C8` to the state-block fields, calls `00268320`, then the requeue
thunk. The already-proved validator accepts a null pointer or zero/zero stamp as well as
the exact magic/size pair, so its true result alone is not proof of a valid initialized save.
Neither additional caller's ordinary gameplay trigger is established by the call sequence.

Two shipping VM dispatch records add a concrete lifetime lead. Call ID **`05BE`** points to
`00355940`, which gets dword`0209AC10` through `00286000` and passes it to result helper
`0026B4E0`. Call ID **`05BF`** points to `00355E80`, which clears ECX and tail-calls setter
`00287D00`, storing0 to that same dword. The bytecode catalog labels them `unkCall_5be` and
`unkCall_5bf`; these are labels, not native semantic proof. FABLE's existing decompiled
`tri_a01` has getter uses during Trial-controller initialization and a later clear. Those
are authored-bytecode and scheduling leads for peer review, not proof of when a real load
executes them or that the flag belongs exclusively to Trial mode.

**L-13 is narrowed, not closed.** The producer, area-controller consumer, requeue thunk and
deferred field request are now connected statically. Remaining work includes message delivery
order, current-context identity, native effects between restoration/reset/init, and the final
heap-bank/field-ID/transition-tick sequence. L-12 and peer consumer integration remain open. *[Reconciled 2026-09-30 (FABLE): L-12 and L-13 are SUPERSEDED since; §7.]*

## 18. Widget destruction order at the load boundary — ASTRA, 2026-09-13

**Player version.** Closing a menu sends its destruction notice to that menu before its
children. Releasing their storage visits the children first. Those different orders matter
because the load and area controllers restore state in their destruction handlers. Their
actual relationship and closing path still need to be established.

[Original teardown and helper evidence](../_experiments/evidence/spawn-widget-teardown/README.md)
contains nine whole method-A bodies and the original message constants. No B/live run, no
synthetic hierarchy presented as initialized game state, and no repeat of the existing widget
constructor campaign. The [widget protocol](../16-UI/Widget-Object-Model/the-widget-message-protocol.md#9-the-lifecycle-end-to-end)
already identifies messages15 and18; its deferred-path question DL-3 is narrowed below.

### Notification order and release order are different

`00244F00` is a null-safe 68-byte destroy request (null check `00244F00`–`00244F03`). It
first sets flags`+40` bit6 (`00244F0A`). When bits0
and5 are both set (`AND 0x21; CMP 0x21` at `00244F14`–`00244F19`), it tail-calls `00244DD0`
(`00244F20`). Otherwise it sends
**message15** to its own non-null handler (indirect call through `[rcx]` with `rdx` =
`00915058` at `00244F25`–`00244F34`), then calls `00245020` (`00244F39`).

The 132-byte `00245020` runs focus-removal work `002448D0` and `00244700(self,1)` first.
It then **saves first-child pointer`+18` before calling self's handler with message18** at
`0024505A`. It calls `002473B0` for that saved child and reads the child's next-sibling
pointer`+20` **after** recursion returns. The 55-byte `002473B0` repeats the same order:
save first child, notify self with18, recurse through children, read each next sibling after
its recursion. With a stable hierarchy this is parent before descendants. Callback changes
to links or object lifetime must be considered; neither walker snapshots the whole subtree.

After notification, `00245020` reads flags`+40` bit5 **again**, so the final choice is after
the handlers. Bit5 clear tail-calls `002482E0`; bit5 set calls `002473F0(self,0)`, clears bit1
and sets bit10, retaining the object on that local path.

The complete 302-byte `002482E0` instead visits **children before self**, saving each child's
next sibling before its recursive cleanup. It then unlinks self from its parent/siblings,
decrements the parent's child count, and conditionally releases resources reached through
`+60`. Before clearing self's handler it calls that handler with **message24**, from the
24-byte record`00915040 = {24,0,0}` at `002483B2`. This additional lifecycle notification
is absent from the earlier contract's simplified destroy transition.

After message24, it clears bit10 and the low nibble of`+7C`, calls `00228450`, reads the
current flags and **saves pointer`+8`**, then nulls handler`+0`. Bit14 chooses either a heap
release through `003697F0` or pool release by clearing bit14 and byte`+A2`. A non-null saved
`+8` pointer is **tail-called after that storage-release path**, without new argument setup.
Do not type this as an ordinary `callback(self)` or assume self remains usable from that
tail alone. Native allocator, resource and callback effects remain outside this reading.

### The deferred request prepares animation state

The 301-byte `00244DD0` does not directly call teardown or send18. It initializes rate`+B8`
to1.0 and conditionally adjusts it through the existing mode/rate getters, then examines
flags`+40` bit0 and the **signed low nibble** of`+7C`.

- Bit0 clear selects low-nibble state1 and reaches the notification tail.
- Bit0 set with state0 or3 selects an animation descriptor, stores it at`+68`, establishes
  timestamp/progress/duration fields, then selects state4.
- Bit0 set with state2 adjusts the timestamp using the current tick and duration, then
  selects state4.
- Other low-nibble states return without the notification tail, after the earlier rate work.

The admitted tail sets`+7C` bits4/5 and sends **message15** if a handler exists, using a
different but byte-identical constant at`01E0C0F8`. Thus this is an exit-animation request
with a conditional15 notification, not an immediate18 broadcast. Section19 now reads the
general completion path; its actual timing remains open. No universal15-before18 guarantee
follows from these entries.

The retained-object helper `002473F0` locally requires flags`+40` bit1 and a differing bit0
state. For the teardown call's input0, it clears bit0 and emits message7, then calls child
helper`00247490`. Its other input values and native child effects are separate. Only the
message ID dword is initialized in its stack message here; the remaining payload is not
proved zero. The focus helpers remove occurrences from the focus stack; tree unlinking is
later in `002482E0`. Neither a focus removal nor the misleading “attach manager” name of
`00244960` proves which controller is an ancestor of another.

**L-13 remains open.** If the area controller and load controller belong to one destroyed
subtree, notification18 follows the traversal above; separately destroying the load widget
can produce a different chronology. Their actual initialized hierarchy, the chosen destroy
path and native completion order must be established before ordering snapshot restoration
against reset/requeue. FABLE/OPUS own the widget protocol/contract propagation; L-12 and the
native field/bank/tick sequence also remain pending. *[Reconciled 2026-09-30 (FABLE): L-12 and L-13 are SUPERSEDED since; §7.]*

## 19. Native widget roots and completion — ASTRA, 2026-09-13

**Player version:** the UI creates real parent objects. A database claim that the parent
pointer stays empty missed a loop in startup. The load and area controllers can attach to
the same parent; that does not make one the child of the other. Sorting and separate closing
conditions still matter when ordering restored enemy state against an area reset.

[Evidence and controls](../_experiments/evidence/spawn-widget-hierarchy/README.md): method A,
18 newly collected whole original bodies and three reused bodies, all matched to the exact
reference EXE. No original-code execution, live observation or PC controls. The existing
constructor campaigns and EXP069 were recovered, not repeated; EXP069's factory stub did
not establish native hierarchy. A guessed pre-update message17 failed the first static
checker; shipping bytes prove **25**. The failed assertion and correction are preserved.

### 19.1 A register-walk initializer writes the allegedly permanent-null root

The [widget contract](../16-UI/Widget-Object-Model/CONTRACT-widget-object.md) §5 CLAIMED
`0208EA28` has no writer, remains null for the process lifetime, and must be passed as null
in reconstruction. **The native initializer contradicts that argument — and the contract has
since agreed.**

> **SETTLED 2026-09-13. The claim was WITHDRAWN at its source**, in that contract, on
> `ASTRA-CONTRA-OPUS-WIDGET-ROOTS`: "`0208EA28` is written, and a reimplementation must NOT
> pass NULL". Re-verified here at the image rather than taken from either page — `00247CF2
> mov ebp, 3`, the store `00247D9F mov qword ptr [rdi], rbx`, `00247DAC add rdi, 8` and the
> `00247DB0`/`00247DB4` loop back to `00247D40`: three iterations, an 8-byte stride, base
> `0208EA20`, so the stores land on `0208EA20`, `0208EA28` and `0208EA30`. **This section is
> kept as the record of how the error was found, not as a live dispute** — it read as open
> until now because the withdrawal landed in the contract and nothing updated the page that
> raised it. Its cited
`00247D20` is inside the complete `00247AE0` body, not a standalone base-only store:

| Original site | Effect relevant to the root array |
|---|---|
| `00247CFE`–`00247D18` | Allocate `0x7E00` bytes through `00249810(3, size)`, publish the pool at `0208EA58`, and zero it |
| `00247CF2`, `00247D1D`–`00247D2C` | Set loop count3, `R14=0`, `RSI=0`, **RDI=`0208EA20`** |
| `00247D40`–`00247D9A` | Put current RSI in descriptor`+8`; obtain pool/heap storage and construct a `0xC8` object with handler`002445D0` through `002465F0` |
| **`00247D9F`** | **Store object RBX to `[RDI]`** |
| `00247DA2`–`00247DB4` | Increment RSI; reload pool base; **RDI+=8**, decrement RBP and loop while nonzero |

Thus, if this initialization path completes with valid storage, its three stores target
**`0208EA20`, `0208EA28`, `0208EA30`**, carrying descriptor values0/1/2. The second store
is not encoded as a RIP-relative reference to`0208EA28`; scanning only literal references
to that slot misses it. The body subsequently constructs more roots and stores one directly
to`0208EA38` at`00247E11`, a positive direct-store control. This is original-code writer
evidence, not an observed allocation or proof that every initialization dependency succeeds.

The other cited base reference, `0025061C` in `00250540`, also **walks all three cells**.
It reads `[RDI]`, tests that root's `+18`, optionally calls`00248030`, then adds8 and repeats
three times (`00250630`–`00250647`). Its later loop calls`00244970`/`00244980` for nonempty
roots in the same array (`00250675`–`0025068C`). It is a reader, not a writer; its dereference
also contradicts treating these cells as deliberately unused null arguments.

`00244960`'s tiny body does not itself dereference RCX, but its admitted tail **does**:
`00248220(parent=RCX, child=RDX)` immediately loads`[RCX+18]`. It appends the child, links
the prior last sibling's`+20` and child's`+28`, increments parent`+30`, and writes
**child`+10=parent`**. Parent flag bit5 propagates to the child and its descendants through
additional helpers; parent bits0/5 and child bit1 can invoke`002473F0(child,1)`. Finally
parent bit13 is set. Unread descendant/helper effects remain separate; **the parent argument
is not universally ignored**. OPUS owns withdrawal and propagation of the permanent-null
claim through contract, types and executable consumers; independent review is pending.

### 19.2 Attach is not close; the load controller attaches on message16

`00247950(self, flag)` loads root`*(0208EA28)`. Null self returns. If self has no parent,
it replaces flags`+40` bit1 with `flag&1`, then tail-calls`00248220(root,self)`; an existing
parent instead leads to`00247870(self,flag)`. That helper updates bit1 and, when bit5 is set,
uses`002473F0` for the enabled-state notification. **Neither body directly calls teardown.**
The [request-router page](../16-UI/Request-Router/ui-request-router.md) calls`00247950` a
“close” in its request-family frontier; that interpretation needs correction. The actual
request-preparation handler `0027FB70` calls`00245020` separately at`0027FD62`, after its
message2 state machine leaves`+CC` zero. Its message18 clears context`+B8`. `0027FB70`'s
full 10-member exclusive subtree is bound on
[the request-router page](../16-UI/Request-Router/ui-request-router.md): message1 opens and
publishes self at `*(0209AC30)+0xB8`, message2 ticks the `+0xD0` state machine into the
18-arm close table `00280048`, and message18 unpublishes.

The generic factory sequence from EXP069 constructs`0027FB70` then`00280140`. Their
message1 handlers publish self into `*(0209AC30)+B8/+C0` and call`00247950(self,0)` at
`00280033`/`002804CA`. The native constructor zeros the allocation before its message1
callback; if intermediate callbacks preserve its parent field, those attach paths use the
same root. This identifies a concrete candidate sibling relationship, not a live snapshot
or a guarantee against callback-driven relinking.

**`00583930` opens the load controller**: it constructs `0x5A0` bytes with handler`00582860`
and message payload`+8=(input ECX!=0)`, `+10=(input EDX!=0)`. Reused raw dispatch bytes
prove that message1 goes to`005828AC`, **message16 to`005829C0`**, and18 to`00582E81`.
Message1 performs resource setup through`00582790`; that helper requests the resources
and returns through`00249410`. Section20 now reads that batch-completion entry; the actual
resource materialization and delivery timing remain separate.
It is **message16**, after other resource work, that sets priority100, loads`*(0208EA28)`
and calls`00244960(root,self)` at`00582A14`, then`00247870(self,0)` and sets its own C4bit1.
`00244960` attaches only when self`+10` is zero. Normal message16 delivery, any preexisting
parent, and the initialized root value are not established by a factory stub.

The nearby `00583260` from ordinary field-stage capture constructs **`0057E4D0`, size`0x178`**,
the write-operation controller. It is not the `00582860` load-controller factory. Keep
those two routes separate when connecting load restoration with field staging.

### 19.3 Deferred completion can enter teardown, after another callback

`00244980` is the general recursive completion pass; five-byte`00244970` tail-jumps to it.
With self flag0 set it optionally calls`002479B0` while flag13 is set, then calls`00246C20`.
Only a nonzero return followed by **current** low state`(+7C&15)==1` admits the final choice:
flag6 set → tail`00245020`; otherwise bit5 can call`002473F0(self,0)`, and bit1 is cleared.
Other paths recurse into children and read the next sibling after each return.

`00246C20` first sends the original constant **message25** when a handler exists, performs
separate property-animation work, and then reads the signed two-bit direction at`+7C[5:4]`.
Zero direction yields no completion. It scales the unsigned32 elapsed tick difference by
the selected float rate, truncates to signed32, and compares that result with duration`+70`
using a **signed** comparison. Before completion it calls easing`00248F40`; its native
implementation and exceptional rate values are outside this package.

On completion, positive direction sets low state3 and sends **19**; negative direction
sets low state1 and sends **20**. The notification runs **before** the function clears the
direction bits and returns1. The local message has its ID dword and two payload qwords
written, but the intervening padding dword is not initialized. The outer`00244980` then
rereads state and flags, so callback mutations can change whether teardown occurs. In the
ordinary unchanged-callback path, section18's deferred exit direction reaches20 and then,
with flag6 still set,18 via`00245020`. This is a bounded native path, not a promise that an
animation ends on a particular game frame or that every caller previously sent15.

The earlier candidate `00248700` is a different message1/2 readiness widget: it records a
pointer/token, invokes`002F8040`/`002FA560`, and on an admitted message2 calls`002494F0`
when required before`00245020`. Its local teardown call does not make it the general
animation-completion driver.

### 19.4 Creation order does not settle restore order

`002479B0` builds 16-byte records from each child: signed word`+44`, original child index,
and pointer. It calls sorting helper`00249CE0` with comparator`00244610`, then rewrites
parent first-child and sibling links. The comparator subtracts the first record's priority
from the second's; equal priorities use first index minus second index. The sort helper's
full implementation is not read here. *(Answered 2026-10-01, SWE2-STRUCT for OPUS, DD batch 21, static: the order does not depend on it. The comparator `00244610` returns the second priority minus the first, then the first index minus the second. The priorities are sign-extended words, so the subtraction cannot overflow, and the indices are distinct. That is a strict total order, so any correct sort gives the same result: the highest `+0x44` first, and equal priorities in their old sibling order. `00249CE0` is the shared sort (eight call sites) and takes a negative result as "first". Checks S1-S7.)* Attachment and priority changes set the parent's
sort flag, so treating the original append order as permanent is unjustified.

The area controller's message2 state2 path additionally requires nonzero`00251D50()` and
`003CA0F0()`, empty context`+300/+308`, and **no children under roots`0208EA30` and`0208EA20`**
before `00280335` calls teardown. Those are different root cells from the shared attachment
root`0208EA28`. The body then reads its own`+C0` after teardown; the retained-bit5 path and
actual lifetime must be respected rather than assuming an unconditional free at that call.

**L-13 stays open.** Native root initialization and explicit attach/completion routes are
now identified, but actual load/area message18 chronology, intervening callbacks and bank,
current-field and timer initialization still need sufficient evidence. L-12 and peer
consumer propagation remain pending. No final audit or integrated-parity claim follows. *[Reconciled 2026-09-30 (FABLE): L-12 and L-13 are SUPERSEDED since; §7.]*

## 20. Root retention and resource-ready delivery — ASTRA, 2026-09-13

**Player version:** a UI parent passes down the setting that lets a menu keep its storage
after a closing notice. That supplies a reason the area controller can still read its state
afterward. Resource completion supplies the message that attaches the load menu, but equal
request counts do not prove that its content loaded successfully.

[Original evidence and checks](../_experiments/evidence/spawn-widget-retention/README.md):
method A,13 new whole bodies plus eight reused bodies checked against shipping bytes. No
isolated execution, live observation or PC controls. This follows the native call and state
chain left open by section19; it does not replace missing scheduling with a stub assumption.

### 20.1 Root flags explain the retained-object branch

`002445D0`, the root handler installed by`00247AE0`, handles message1 locally:
**flags`+40 |= 0x23`** sets bits0/1/5, descriptor`+8` becomes root`+C0`, position`+98` is
zeroed, and words`+9C/+9E` take the low16 display dimensions from`01E0C1D8/DC`.
Every other message returns0 without forwarding to the default handler. This is a concrete
exception to assuming all unhandled widget messages tail-call`005C5230`.

On attachment to a root with bit5 set, `00248220` sets child bit5 and calls
`002463F0(descendant,002418E0,1)` for each existing child subtree. `002418E0` replaces
bit5 with the input's low bit. `002463F0` caches first-child before its callback, invokes
that callback on self, recurses and reads next-sibling after return. Under stable links,
this propagates bit5 throughout the attached subtree.

That is a native producer for `00245020`'s retained branch: if callbacks preserve bit5,
its post-message18 test avoids`002482E0`, calls`002473F0(self,0)`, clears bit1 and sets
bit10. The area controller's post-teardown `+C0` read (section19) therefore has a concrete
retention route. This does **not** make later reclamation or callback-driven changes safe
by assumption. Section21 now identifies the generation-gated release path; actual lifetime
and the ordering of interleaved callbacks remain open.

`00247490`, the descendant enabled-state helper, has a different traversal rule from the
unconditional callback walk. **If this node's bit1 is clear, or its bit0 equals the full
input EDX, it returns without visiting its children.** Otherwise it changes bit0 from the
input low bit, sends the caller's existing message pointer to its handler if present, and
then recurses. Both failed gates jump beyond the recursive loop. Thus an unchanged or
disabled intermediate node prunes its entire subtree; it is not merely a skipped notice
followed by an unconditional descendant walk. The ordinary0/1 inputs and arbitrary EDX
values must not be conflated.

### 20.2 A batch owns the load widget and can deliver16 synchronously at sealing

`00249580(owner)` scans **12 records of `0x20` bytes at`02090790`** for bit0 clear. It
zeros all32 bytes, sets bit0, stores owner at`+8`, and returns the slot; all busy returns
null. `00582790` passes the load widget as this owner, retains the returned batch across
resource requests, and tail-calls`00249410(batch)`. There is no null-result check in that
caller. This is a separate bookkeeping pool from the resource queue's64 request slots.

| Batch field | Native use in these bodies |
|---|---|
| `+0` dword bit0 | Allocator availability; cleared after the widget notification branch |
| `+0` dword bit1 | Set by sealing; completion paths require it |
| `+4` dword | Zero chooses widget message16; nonzero chooses indirect callback`+10` |
| `+8` qword | Widget owner for the zero-mode branch |
| `+10` qword | Custom callback, not null-checked in its selected branch |
| `+18`, `+1A` words | Requested and completed counts; increment instructions wrap at16 bits |

`00249410` sets bit1, compares those two words, and dispatches when equal. In zero mode it
loads the owner, builds message16 with zero payload qwords, calls `[owner+0]` if both owner
and handler exist, and **only then clears batch bit0**. The padding dword between ID and
payload is not initialized. If the counts are already equal, including0/0, this notification
occurs inside the sealing call. The same body does not wait for a later frame.

The load handler's original dispatch table (section19) makes that16 notification enter
`005829C0`, whose resource work precedes the attach at`00582A14`. This closes the local
owner-to-notification connection. Whether sealing sees equal counts in an actual load, the
resources it binds, and any callback-driven reentrancy require further evidence.

### 20.3 Member completion runs before the batch count advances

`00249210` obtains a member record from a separate **48-slot pool at`*(0208F578)`, stride
`0x28`**, using bit0 of member`+20`. It stores the batch at member`+0`, prepares a descriptor
whose callback is`002495C0`, and writes only the **low32 member pointer** into that
descriptor's`+8`. A positive file-size result admits allocation/request submission through
`0032E620`, then increments batch requested`+18`. A nonpositive size follows a different
path without this increment. Exhaustion yields a null member followed by an unchecked
member store; do not model it as a clean refusal. Native allocation and submission effects
are not replaced by assertions about these local branches.

The resource callback `002495C0` starts with **`MOVSXD RBX,ECX`**, explicitly interpreting
the callback token as a signed32 address. It invokes member`+10(member)` if present,
**then** reads the member's batch and increments completed`+1A`. With sealed bit1 and equal
counts it chooses custom callback or owner message16. After that path it clears member
`+20` bit0. The widget branch clears batch bit0 after notifying; the custom branch does not.
This token decoding does not prove where the game allocates this member pool in a live run.

The load-resource wrappers install native member callbacks`00249660` and`00249670` after
their `00249210` calls. `003933F0` fills pointers through`00249320`; `00393460` uses24-byte
descriptors through`002493D0`, then writes the returned object's`+40`. Section21 recovers
the arguments forwarded by`00249660/70`; actual materialization in their native callees
is recovered locally in section23, while downstream graphics effects remain separate.
A completion count is still **not proof of successful or initialized resource content**.

`002494F0(batch, advance)` is another completion entry: nonzero advance increments
completed`+1A`, then the same sealed/equal test and widget/custom choice apply. None of
these three local completion paths checks active bit0 before notifying. Clearing bit0
alone is **not a one-shot guard**; repeated calls with unchanged sealed/equal state can
reach the notification again. This is local reachability, not observed repeated delivery.

**The custom callback ABI is not uniform.** `00249410` and`002494F0` call batch`+10` while
RCX still identifies the batch. `002495C0` keeps the batch in RDI but does not reload RCX
before its call at`00249606`; the optional earlier member callback can also clobber RCX.
Do not type that site as `callback(batch)` without recovering the selected producer and
native expectations. Default widget notification sites do explicitly prepare owner/message.

FABLE/OPUS own UI, resource and type/contract propagation and high-impact review. Root
retention, pruned descendants and the local16-delivery chain are now bounded facts;
actual restore/reset order, later widget reclamation, native resource contents, callback
lifetime, L-12/L-13 and required full-database reviews remain open. *[Reconciled 2026-09-30 (FABLE): L-12 and L-13 are SUPERSEDED since; §7.]*

## 21. Generation-gated reclamation — ASTRA, 2026-09-13

**Player version:** a menu can receive its closing notice and keep its storage until a
later update pass releases it. The update-suppression flag prevents the usual menu update
message; the database described that flag backwards. Both facts matter when connecting
the load menu's restoration work to the area controller's reset.

[Original evidence and controls](../_experiments/evidence/spawn-widget-reclaim/README.md):
method A, six new whole bodies, three reused bodies, and raw message constants, all checked
against the same shipping EXE. No isolated or live execution and no PC controls. The primary
branches settle these bounded claims; no synthetic tree is claimed as initialized gameplay.

### 21.1 Message2 is suppressed when bit18 is set

The [widget protocol](../16-UI/Widget-Object-Model/the-widget-message-protocol.md) §9 and
[widget contract](../16-UI/Widget-Object-Model/CONTRACT-widget-object.md) §7 describe
`00248030` as sending2 when bit18 is set. **The branch is the reverse**:

```asm
002480DB  or   ecx, 4                 ; mark bit2 on this admitted node
002480DE  mov  [rbx+40h], ecx
002480E1  bt   ecx, 12h               ; bit18 -> carry
002480E5  jb   00248101               ; SET skips the handler
002480E7  mov  rax, [rbx]
002480EA  test rax, rax
002480ED  je   00248101
002480EF  lea  rdx, [00915108]        ; actual {2,0,0}
002480F9  call rax
```

This branch is reached only when node bit17 differs from the **full** global dword
`0208ED5C` and bit10 is clear. Bit18 clear and a nonnull handler admit2; bit18 set skips2.
After the notification it reloads the global, clears node bit17 and **sets that bit to
the current global's low bit** (`00248101`–`00248110`). Thus the protocol's “then clears
bit17” is incomplete: global1 produces node bit17 set. The callback can change the global
before the reload. This is not a gate on the old global value alone.

### 21.2 The same traversal releases retained widgets before updating them

On a generation mismatch, bit10 is checked **before** the message2 path. If set, the
function caches next-sibling`+20` and parent`+10`, then calls`002482E0` at`00248097`.
That is the children-first24/storage-release path from section18; it does not first send
another18. It reloads generation after release and chooses the cached sibling or parent.
This supplies the consumer of bit10 that `00245020` sets in its retained branch.

If message2 itself invokes teardown and sets bit10, this visit has already passed that
release test. It synchronizes bit17 afterward and continues traversal. With a stable
generation/global and callbacks, **bit10 is released on a later generation-mismatched
visit**, not merely because it became set during this callback. An exact frame number or
guaranteed survival through arbitrary reentrant callbacks is not established here.

The traversal is not an unconditional recursive walk. At a candidate first-child whose
generation already matches, it proceeds to the current node's sibling/parent logic,
skipping that child list. At a matching next-sibling it ascends rather than scanning all
later siblings. After release it similarly considers the cached sibling's generation.
These decisions rely on native generation/topology invariants; an arbitrary mixed-generation
fixture must not be assumed to visit every node. The entry also updates root`+B4` before
the first generation comparison: zero when `001EDDA0()` is nonzero, otherwise increment;
newly entered mismatched children/siblings use that same saved mode result.

### 21.3 One native caller orders reconciliation before animation completion

`002481A0` XORs global`0208ED5C` with1 and sets `0208F560=1`; `00248190` clears
`0208F560`. Reused `00250540`'s ordinary non-mode5 path orders:

1. `002481A0` (`00250617`): change generation and mark the update phase.
2. `00248030` for the three nonempty roots`0208EA20/28/30`, then roots`0208EA40/48`.
3. `00248190` then`002481C0` (`00250661/666`).
4. `00244970`/`00244980` for the corresponding roots: the animation-completion pass.

This is one concrete caller path, not a census of every UI mode. `002465F0` reads both
globals when seeding a new widget. Outside the marked phase, bit17 takes the generation's
low bit. **During the marked phase, bit17 becomes zero**: `00246665`–`0024666D` XORs the
same global-derived bit with the already seeded bit. This is not a logical inversion when
generation is0; an initial draft's “flips the seed” description was corrected before
publication. The constructor's phase behavior and the traversal's generation checks
therefore have a native connection; their effects under actual nested construction still
require the relevant state and callbacks.

`002481C0` is **not** the release operation. It starts at focus`*(0208EBC0)` and walks its
ancestors while bits0 and3 are both set. A node failing either bit returns without a
notification. Encountering bit9 sends original **message11** (`009150F0`) to the original
focus handler; reaching the top sends **message10** (`009150D8`). It chooses only the first
encountered gate/result along that walk. Both records are `{id,0,0}` and both handler
transfers are tail calls. Focus/input effects of the receiving handler remain separate.

### 21.4 The resource adapters still lead to native materialization

`00249660` is9 bytes: load member`+8` into RCX and tail`002A00F0`. `00249670` is13:
load member`+8` into RDX and member`+18` into RCX, then tail`0024A1D0`. Those are the actual
arguments supplied by section20's member callbacks. Section23 now reads both native
destinations and their bounded helpers; the adapters alone did not establish those effects.
Validation, actual input identity and downstream graphics behavior retain their own limits.

Peer review and propagation of the bit18 polarity, generation synchronization, deferred
release and affected type/executable consumers remain required. Actual initialized topology,
ordinary load/area message18 chronology, native resource/bank/field/timer state and L-12/L-13
stay open. No final audit, integrated parity or database completion is claimed. *[Reconciled 2026-09-30 (FABLE): L-12 and L-13 are SUPERSEDED since; §7.]*

## 22. The load-close request can admit the area transition — ASTRA, 2026-09-13

**Player version:** the load menu has a route that restores saved data, asks its full-screen
menu to close, and lets the area transition continue. Closing the menu alone does not prove
that restoration happened: separate flags select those operations. This section establishes
that conditional route in the shipping code, not a recording of an ordinary load.

[Original evidence and controls](../_experiments/evidence/spawn-load-close/README.md) bank
17 collected whole bodies and reuse eight previously banked bodies. Method A only: exact EXE,
complete instruction bytes, request-table entries, message constants and branch/order checks.
No isolated original-code execution, live game or PC controls were used. The
[request router](../16-UI/Request-Router/ui-request-router.md) already identifies request6
from save-crystal scripts and reads the full-screen request table; those findings are
re-derived here and connected to the close/state producer, not claimed as new discoveries.

### 22.1 Request6 constructs the load controller with a close-on-exit flag

`0027F540(request, parameter, third)` checks context `*(0209AC30)+100` for null. If occupied,
it skips construction. Otherwise it packages the three input dwords and calls the existing
widget factory `00244F50` with size`0xF0` and handler`0027F5D0`. In that handler, message1
publishes self at context`+100`, stores `request & 0x7FFF` at self`+D0`, and parameter at
self`+D4`. Its message18 later clears context`+100`.

On message19, the handler selects from **21 image-relative dwords at`0027FAD0`**, indexed
by unsigned `(self.D0 - 2) <= 20`. The original request6 entry reaches`0027F8DB`. Neighboring
requests5/7 go to`0027FA31`; request2 reaches`0027F9C1`. These are distinguishing controls,
not a guessed switch arm. The table agrees with FABLE's existing router evidence.

Within the request6 arm, a zero parameter calls`003C60F0`, rechecks the parameter, and, if
still zero, prepares stack records before`005844A0` and`0020E5C0`. A nonzero parameter uses
`00584490`. Both admitted branches converge on **`00583930(self.D4,1)` at`0027F984`**.
The earlier save-buffer pages cover the preparation calls; this section does not re-prove
their complete native effects.

The reused factory `00583930` converts the second argument to a boolean qword at message
`+10` and constructs size`0x5A0`, handler`00582860`. Its message1 sets self`+C4` bit3 when
that qword equals1. Thus the request6 producer supplies the flag tested by its later
close-on-exit branch. Actual allocation, initialized context and message delivery remain
preconditions; a factory call alone is not an observed menu.

### 22.2 Restoration precedes this close request, but the two have separate gates

The original load-handler table at`00582F54` maps message18 to`00582E81`. The local path is:

| Gate / step | Shipping operation |
|---|---|
| `self.C4` bit4 clear | Skip the restoration and normalization block entirely |
| Bit4 set, `self+598` byte zero | `001831A0`; set`0209AC10=1`; **`005843E0` at`00582EA2`**; `00182D40` |
| Bit4 set, `+598` nonzero | Skip that restore call, join at`00582EAC` |
| Either bit4-set branch | Conditional`00394400`, then **`00584210` at`00582EBA`** |
| Common cleanup | `00582FC0`, release/clear`+588/+590`, clear global`02CA99B8` |
| `self.C4` bit3 set | **`002814E0(-2)` at`00582F0E`** |

Accordingly, **if this message18 admits the restore call and reaches its close request,
the restore call and normalization return before that request is issued**. This follows
from the original branches and call order; it does not depend on guessing sibling priority.
The bit3 close path also exists with bit4 clear, so observing closure would not establish
that a save was restored. The `+598` alternate branch is a second such boundary.
Section24 supplies the selected-slot producer of `+598` and the success/close
notifications; other writers and initialized native delivery remain open.

### 22.3 The close request reaches the producer of area state2

`002814E0(-2)` follows an explicit comparison at`002814FB`, reads context`+100`, and, when
nonnull, tail-calls`00244F00` at`00281558`. Other requests use other branches; none of the
large compressed request table is needed to establish the explicit`-2` route.

`00244F00` **sets widget flag bit6 before dispatch**. With flags0/5 both set it delegates
to`00244DD0`; otherwise it sends message15 immediately, then calls`00245020`. The deferred
helper also sends15 on its admitted modes, but some modes return without that notice
(section18). Both original message records, `00915058` and`01E0C0F8`, are `{15,0,0}`.

For a context`+100` widget still using handler`0027F5D0`, message15 checks bit6 and then
calls`00295CE0` and **`0027F2E0` at`0027F63C`**. The close helper supplies that bit6; native
calls or callbacks changing the handler/flags/context still have to be accounted for.
`0027F2E0` chooses a duration of1 when context`+400` bit11 is set, otherwise200, and calls
`002C98C0`, `00250F30`, `002CC960`. It then **reloads the context and flags** and writes:

| Context`+400` bits at this reload | New low byte at context`+400` |
|---|---|
| Bit9 clear, either bit10 | 2 |
| Bit9 set, bit10 clear | 1 |
| Bits9 and10 both set | 2 |

The last two rows are `BT bit10; SETB AL; INC AL`; the bit9-clear branch directly stores2.
It reloads context again and clears bit11 afterward. The other high bits survive these
local writes. Reused `00285E60`, called from the load handler's message12/subtype16 arm,
sets bits9/10. If those bits and the relevant context survive until this close callback,
the new low state is2.

The reused area handler `00280140` binds self`+C0` to context`+3F8` during message1. Its
message2 reads the low byte at that bound pointer`+8` — the same context`+400`. State2
waits for `00251D50` and`003CA0F0`, null context`+300/+308`, and empty root`0208EA30/20`
child lists before `00245020(self)` at`00280335`. Its message18, with bit9 still set,
clears9/10 and calls **`00268320` before`00267C90`**, the reset/requeue path in section17.

This closes the **conditional producer-to-consumer connection**: restore/normalize,
close request, admitted full-screen15, state2, admitted area2, area18 reset/requeue.
The full-screen15 can occur synchronously inside the load handler's18, before that outer
handler returns; it need not wait for final storage release. It is not a universal
chronology: context identity, initialization, native callback effects, reentrancy, prior
state2 writers and the actual trigger still matter. `002814E0(-1)` is already a separate
direct route to`0027F2E0`; no complete census of context-state producers is claimed.

### 22.4 Recovered side paths constrain the interpretation

`002CFD10` is **not a direct close request**. It overwrites its inputs and calls
`002527B0(6,4,0)`, then tail-calls`0028E880`. The former writes a zero word to
`*(020927C0)+38` (selector6 uses word entries at`+30`, signed index clamped0..31).
The latter, when `*(0209BE80)` is nonnull, clears`0xC4` bytes at its`+AA60`. The caller's
`ECX=-1` is therefore not a close-selector argument to this function. `002804E0` likewise
contains presentation-related calls selected by context`+3F0`; its native callees were not
used as proof of a close request.

`00233C10` re-derives the save-map binding and stamp check. Its null-pointer branch calls
`002EF640`, adds`0x4E68C`, and stores the result in`02EBF190`: **this local code binds into
the active image; it does not directly allocate a fresh block**. It calls`0030B6A0`, then
calls`00237DF0` at`00233C3F` and tail-calls it again at`00233C48` if the first call returns.
A nonnull stamp mismatch takes only the tail at`00233C59`. The
[version-stamp page](../19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/version-stamps-and-what-loading-normalises.md)
calls the null path an allocation; the [payload map](../19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/the-save-payload-field-map.md)
already describes the image binding. Route that wording correction and the double-entry
detail to the owners; the callee's complete initialization effects are separate.

`00583040` advances storage-status UI. Status0 scans200 slot records: with mode byte`+C1`
zero, a slot qualifies when its first dword is2 or second dword is nonzero; with mode
nonzero, first-dword values2 or4 qualify. Status1 also admits the next screens in mode0;
other status branches choose error/empty codes. After closing self`+F0`, an eligible result
constructs handlers`0057EDB0`/`0057FE80` and writes state4; an ineligible result calls
`00583990`, `0057EC60(self,1)` and writes state3. This advancement is not the saved-image
restore at`005843E0`. `0057EC60` stores the owner and passes callback`0057EBB0` plus a low32
token through`00582540`; the native callback effects remain outside this package.

There is also a concrete retention boundary: the separate handler`00228130` **clears its
own bit5 during message18 at`002281DE`**, while its message2 calls`00245020` and later
writes self`+CC`. Thus root-inherited retention is not immutable across native callbacks.
This is not evidence that area handler`00280140` clears bit5, nor proof that the other
controller's post-call write is safe in an actual initialized tree. `00285EA0` separately
replaces context bit13 from the input low bit; `00285EC0` sets bit8 and stores context`+3FC`.

The candidate search that led to this route was deliberately incomplete: it used the
existing RIP-reference index and literal operand fragments, with known`00285E60`/`00280140`
controls. It is not an alias or writer census. An incorrectly repeated `--addr` option also
produced an invalid no-coverage headline in the first existing-work search; the retained
correction records the proper multi-address invocation and the existing documents it found.

*[Reconciled 2026-09-30 (FABLE): L-12 and L-13 are SUPERSEDED since; §7.]* FABLE/OPUS review and propagation remain pending. L-12/L-13 stay open for initialized
ordinary delivery, native resource/bank/field/timer effects, competing producers and the
remaining cross-system sequence. No live observation, integrated parity, final audit or
full L1/L2 completion is claimed.

## 23. Resource preparation runs before the load-menu ready notice — ASTRA, 2026-09-13

**Player version:** before the load menu receives its ready notice, its resource callbacks
can adjust references inside menu data and prepare image data. A callback finishing still
does not prove that the right file was loaded or that a valid image reached the screen.

[Original evidence and controls](../_experiments/evidence/spawn-resource-materialization/README.md)
bank ten collected whole bodies, eight reused bodies and the load menu's literal resource
descriptors. This is method A only: exact shipping bytes, branch and call-order checks;
no original-code execution, live game or PC controls. The reference encoder/resolver is
re-derived existing [reference-contract evidence](../02-Resource-And-Asset-Pipeline/CONTRACT-authored-table-row-lookup.md).

### 23.1 The load constructor selects these two callback families

Reused `00582790` requests one descriptor at`00D23D80` through`00393460`, placing its
result at load-widget`+100`. The original24 bytes contain resource index **127**, name
pointer`00D23EB8` (**`dataface_c`**, eleven bytes including NUL), and extra dword0. The
wrapper supplies kind7, obtains an object through`002493D0`, and writes that extra dword
to object`+40`. The second request, through`003933F0`, uses the original dword **111** at
`00D23D98`, also kind7, and stores its buffer at load-widget`+108`.

`002493D0` installs member callback`00249670`, whose arguments to`0024A1D0` are
`(member+18 object, member+8 buffer)`. `00249320` installs`00249660`, which passes its
buffer to`002A00F0`. These are literal request identifiers and a label, **not resolved
archive paths, a file-content capture or proof of live binding**.

The reused completion adapter `002495C0` calls member`+10` at`002495E8`, then reads the
batch and increments its completed word at`002495ED`. Only afterward can it send16 to
the widget. Thus the preparation below precedes that completion increment when its native
callback returns. No success return from either preparation function is tested there.

### 23.2 The buffer callback rewrites references using three different origins

`002A00F0(buffer)` first checks byte`+3`. **Exactly1 skips all preparation**; any other
value follows the rewrite path, and byte`+3` becomes1 only at the end. It encodes the
buffer-relative dword at`+8`, calls`002A1A80` for one table, then handles a second table:

| Location | Rewrite origin and traversal |
|---|---|
| Buffer`+8` dword | Buffer address |
| Buffer`+20` dword, inside`002A1A80` | Buffer address; decode the result to obtain table A |
| Table A row`+10` dword | **That row's address**; rows are`0x14` bytes, count from buffer`+1C` |
| Buffer`+28` dword | Buffer address; decode the result to obtain table B |
| Table B row`+8` dword | **Table B's base**, not the current row; rows are`0x0C` bytes, count from buffer`+24` |

Each rewrite adds the selected origin's low32 bits to the old dword in a32-bit register,
then calls`0020E620`, which subtracts the low32 bits of global`01F83530`. Decoding uses
`0020E600`: **full64 base plus zero-extended32 encoded value**, modulo64. The established
reference-window limits apply; do not replace this with unrestricted64-bit pointer addition
or assume the runtime base is zero. The different row/table origins are explicit:
`002A1AD0 ADD ECX,EBX` versus`002A0147 ADD ECX,EBP`.

Both counts are compared unsigned. In table A the index is sign-extended from EDI before
the address calculation, so arbitrary counts crossing`0x80000000` cannot be modeled as
an ordinary unbounded positive array walk. Zero counts skip row writes but not the table
reference rewrite or final byte`+3` marker. There is no local file-size validation of these
offset/count combinations. This is a guarded relocation operation, not a parser that has
proved a file valid; calling`002A1A80` directly also omits the outer byte`+3` guard.

### 23.3 The image object comes from a separate64-record pool

`0024A4E0(name, flags)` scans **64 records of`0x48` bytes at`0208F580`** for flag bit5
clear, using four unrolled tests per iteration. All busy returns null. This is distinct
from section20's12 batch records and48 member records. The caller`002493D0` stores the
result at member`+18` without a null-result branch; a valid record remains a precondition
for its later preparation callback.

On admission, the allocator copies a nonnull name through its NUL terminator, with no
local length comparison; a null name zeros the first16 bytes. It sets flags`+38` to
`(old & 0x3FF10) | (input & 0xF) | 0xA0`, clears qword`+28` and qword`+40`, and increments
global`02090780`. It **does not zero the whole record**. In particular, bit6 is cleared by
this mask; later preparation sets it. Native name and reuse preconditions must not be
replaced by a fresh-allocation assumption.

### 23.4 Header branches prepare different data, then share the same flag write

`0024A1D0(object, buffer)` uses `H = buffer+0x10`. It derives positional pointers
`P = H + u16[H+0x0C]` and `Q = P + u32[H+8]`, stores buffer at object`+18` and H at`+20`,
and copies header-qword`[H+18]` bits20..25 to object flags bits8..13 and bits51..54 to
flags bits14..17. The format selector is that first six-bit value. Both arguments already
need readable memory at entry; the first header read has no preceding local null refusal.

| Selector | Local preparation |
|---|---|
| `0x13` | Store Q at object`+10`; call`00181250` with P and the two dimension words at H`+14/+16`; then call`00181000` with trailing/override data |
| `0x14` | Optionally use object`+28` as the source instead of Q; allocate and reorder trailing data into object`+10`; call`00181190` with P and dimensions, then`00180E70` |
| Every other six-bit value | Skip both detailed arms and jump to`0024A427` |

**All locally returning arms reach`0024A427 OR [object+38],0x40`.** Therefore bit6 does
not by itself prove that either detailed format arm ran. Native callees before or within
these branches retain their own effects; the local flag is not a GPU-success result.

In the`0x14` arm, count N is u16`[H+0x0E]`, or flags`>>18` when object`+28` supplies an
override. It requests `((N+255)>>8)<<10` bytes through`0036A190` and copies`N>>4` groups
of64 source bytes. For group i, destination base is `128*(i>>1)+32*(i&1)`; four16-byte
chunks land at base offsets0,16,64,80. The first two groups thus interleave into one128-byte
region. This loop has no tail for `N & 15`, and it does not initialize unused allocation
padding. A null allocation or malformed header is not converted to a local clean refusal.

`00181190` and`00181250` reduce dimensions to16 bits, form a next-power-of-two value by
bit spreading and a **16-bit increment**, then call`00183EE0` or`00184140` respectively.
The derived value wraps to0 for zero or for a next power of65536; it is not an unlimited
width clamp. Both then forward a result through`001B21D0`. The auxiliary helpers
`00180E70`/`00181000` use signed division toward zero by16/256, skip nonpositive group
counts, optionally rearrange groups for six packed selector values, and call`0017F3B0`
then`001B20B0` per group. The two source strides are`0x40` and`0x400`.

Those downstream creation/binding functions are separate native boundaries in this
package. No texture on screen, graphics-device success, complete image-format identity,
actual input sizes or ordinary request timing is established by these calls. The
architectural result is narrower and useful: **content preparation precedes the ready
count, while the ready count and preparation flag still do not certify valid content**.

FABLE/OPUS own semantic/type/contract propagation and independent review. The earlier
L-12/L-13, live initialization/delivery and pending widget contradictions remain open. *[Reconciled 2026-09-30 (FABLE): L-12 and L-13 are SUPERSEDED since; §7.]*
No final audit, integrated parity or full L1/L2 completion is claimed.

## 24. Selected-save success and the later close are separate notifications — ASTRA, 2026-09-13

**Player version:** choosing a save, successfully reading it, and leaving the load menu
are separate steps. The selected slot affects which restoration steps run afterward.
An error path restores only part of the active save image, so it must not be described
as a full rollback. These are findings from the original code; no game was controlled.

[Evidence and limits](../_experiments/evidence/spawn-load-success/README.md) bank
18 collected bodies/code spans and reuse seven original bodies. Method A only, exact
shipping identity as in section23. This connects the section22 close/area chain to its
success producer. It does **not** establish actual storage-worker delivery, initialized
objects, popup input delivery or L-13 integrated behavior. Existing header-access and
widget-message evidence is re-derived and attributed in the evidence README.

### 24.1 The earlier operation result only advances to slot selection

`0057F360` receives message12/subtype29 with packet tag13 and calls `0057F6B0`.
Packet status dword`+8` greater than1 unsigned makes its result `{tag10, device byte,
status}` at self`+E0/+E4/+E8` and state byte`+CC=4`. Status0/1 instead registers
callback `0057F630` through packet1, submits packet10 with buffer self`+D8` and
size`0xA0`, then enters state2. The storage-queue implementation is still a separate
boundary here; packet submission is not an observed read.

`0057F630(operation, status, token)` reconstructs self by **zero-extending R8D**.
Operation10 stores tag10/device/status. On status0 it calls `0057F280`: that scans
up to200 slots from byte`+CF`, looking for slot-state2 and the corresponding
`0xA0`-byte record's dword`+4==0`. A found slot submits packet6, advances `+CF`,
and returns0; exhaustion returns1. The callback sets state3 while that scan is
pending, state4 on exhaustion or nonzero operation10 status. Operation6 continues
the scan and eventually sets state4. These are metadata-stage operations, distinct
from the later full-image operation9.

That scan description assumes the initialized `+CF<=200` range: exactly200 returns
exhausted, but an injected value above200 skips the loop and takes the non-equal
submission branch. The byte width is not a general out-of-range refusal.

In state4, `0057F360` waits for its signed elapsed-tick gate of60, except status4
forces admission. It sends parent message12/subtype29 with the tag10 packet at
`0057F493`, calls `00244F00(self)` at `0057F49B`, then reads its result and writes
state5 afterward. The native lifetime and reentrancy conditions from sections18–21
therefore apply. `00583040` consumes that tag10 and may construct the slot-selection
handler `0057FE80`, storing it in the parent at`+D8`. It is not the restore-success
notification. `0057E950` is the preceding tag13 producer for operations4/5; its
operation4/status0/owner-bit1 path submits packet5 instead of reporting immediately.

### 24.2 Selection records the actual slot and submits the full-image request

`00583040` constructs a separate `0057EDB0` details widget at parent`+E0`, and
`0057FE80` with parent, details pointer, mode byte, flags, metadata array and UI
resource arguments. Selection message1 stores these at `+C0/+C8/+EA/+E0/+1C0`
and initializes state byte`+E9=0xFF` before requesting state0. Metadata records have
stride`0xA0`; the displayed index maps to a slot byte through self`+EF[index]`.
The initial enumeration starts at slot1 when mode`+EA==0`, otherwise slot0. This
alone does not establish the player-facing name or native meaning of slot0.

The original selection message table at `005807B8` admits message12 at `00580401`.
Within that arm, subtype`0x8001` takes the supplied index from message`+10`, looks
up its slot byte, stores it in self`+EB`, and **also writes that slot to
`(*(02CA99B8))+598` at `0058052A`**. There is no local index bound or parent-null
refusal on this path; initialized list and parent state remain preconditions.
Subtype`0x8000` instead updates the details view. Neither is by itself a successful
load. Subtype29 dispatches packet tags3/13/15 to `00580A80/00580B40/00580CD0`.
Flag bit4 of self`+E0` suppresses these result handlers once closure is requested.

`00580B40` selects later states from mode, packet status and flags. In nonzero mode,
status0 chooses state6 only when `00394450()!=3` and the selected metadata record's
byte`+57` bit0 is set; otherwise it chooses state8. State6's result-message path
can subsequently select state8. State8 in `00580EB0`, proven by original table
`00581268`, registers callback `00580840` with a low32 self token, obtains the active
image from `002EF640`, builds a name through `005837F0(1, self+EB, 1)`, and submits
packet9 with that image pointer and **size`0x56690`** at `0058111E`. The third argument
does not select a branch in the read `005837F0` body; do not infer behavior from the
call signature alone. Native name-generation callees, queue effects and file validity
remain outside this package.

`00580EB0` first compares the requested byte state with self`+E9`. Equal states
return without repeating setup, even if the auxiliary argument changed. Different
states run their effects, may create a popup, and only then publish the new state at
`00581246`. Thus synchronous callbacks during setup cannot be assumed to see the
new state. State4 constructs another operation widget (`005819F0`); state11 submits
packet12; they are not interchangeable with the state8/packet9 path.

### 24.3 Operation9/status0 produces the restore notification

`00580840` starts with `MOV EBX,R8D`: its callback token requires a controller address
representable in the low32 bits, unlike a general64-bit widget pointer. It exits before
effects when self`+E0` bit4 is set. For operation9 it closes self`+D8`, clears that
pointer, marks the optional global popup helper's state4, and branches on status:

| Operation9 result | Original local continuation |
|---|---|
| Status0 | `005813E0`, then `00247510(parent,16,4)` at `005808E6`, then request state9 |
| Status8 | Set optional global error flag; restore the controller's saved prefix with `00583C00`; set the selected slot's status pair to `{4,1}` and, for slot<200 with a parent, its bit in parent`+568`; clear/hide the details selection; request state14 with argument10 |
| Other nonzero status | Set optional global error flag; `00583C00`; request state13 with argument6 |

These numeric statuses are not assigned platform error names without the worker's
primary evidence. Operation12 has its own path: status0 clears self`+E0` bit0, sets
bit3 and requests state12; failure requests state13/argument4. It does not send the
operation9 success notification. Callback operation identity, result code and close
flag are all required controls, not merely a label saying a test was validated.

`00247510` constructs a **synchronous message12** on its stack, copying the full
incoming RDX and R8 to message`+8/+10`. Null parent or null handler returns0;
otherwise it calls the handler immediately. Here the caller initializes them as
subtype16 and argument4. This is distinct from resource-batch message16, and from
the earlier subtype29/tag10 metadata result.

With `00582860` as the initialized parent handler, subtype16 sets parent`+C4` bit4
and calls `00285E60(-1)` through either `00394450` mode branch, establishing the
section17 context bits9/10 route. The notification occurs **before** the selector's
state9 setup. Its return is not checked to certify successful parent handling.

### 24.4 The later result message closes the selector and its parent

State9 in `00580EB0` selects popup identifier23 through `00583990` and then stores
state9. The popup's actual ordinary input-to-message delivery is not established
here. **If** selector message12/subtype`0x8100`, `0x8101` or `0x8102` arrives while
state9 is retained, original table `00580800` selects `005806CC`: set self`+E0` bit4,
then call `00244F00(self)`. The table uses R9=image base established at entry;
the intervening `0057ED40` leaf does not alter R9 or R8. No arbitrary survival of
volatile registers across an unknown callee was assumed.

The selector's message15 sends parent message12/subtype15/argument4. That parent
arm calls `00581310` with the pointer at parent`+D0` and closes its details widget
at`+E0` if nonnull.
`00581310` calls `00244F00` first, then its UI helpers; it dereferences the global
parent without a null guard and conditionally takes a bit3 path. The selector's
message18 sends parent subtype18
with argument4. Parent table `00582FA0` maps4 to `00582C38`: clear parent`+D8`,
close the three optional global helpers, then **`00244F00(parent)` at `00582C77`**.
Section18's immediate/deferred close and retention limits remain in force. Closing
the selector through another admitted route can reach this parent close without a
successful operation9, so closure is still not proof of restoration.

Finally, on parent message18, bit4 admits normalization `00584210`. The preceding
persistence restore `005843E0` additionally requires **parent`+598==0`**. Section24.2
now supplies one concrete producer: the actual selected slot byte. Under the same
parent with no intervening writer, selecting a nonzero slot skips `005843E0`, while
slot0 admits it. This is a conditional original-code distinction; the reason for
that slot split, a complete writer census and actual initialized delivery remain
open. Parent bit3 independently closes the outer controller and continues the
section22 context-state2/area-admission chain.

### 24.5 Error recovery restores a prefix, and the extraction failures stay visible

`00583C00` checks only the global parent for null, obtains the active image, reads
the backup pointer from parent`+588`, copies `0x1C4` blocks of`0x80` bytes and four
final16-byte chunks. **Exactly`0xE240` bytes** return to active-image offset0.
The parent constructor allocates`0xE240` at`+588` and calls `00583CB0` to populate
it; that helper's detailed effects and successful allocation remain separate here.
This is distinct from the full-image request of`0x56690` and from the fourth global
backup buffer `022676C0`. The function's historical “Header” name must not be read
as a proof that only the small header changes, or that all failed-read effects roll
back. `00580CD0` separately updates the active counter, copies one`0xA0` metadata
record and changes slot state on its tag15/status0 path; it is not the operation9
restore-success producer.

The `0057FE80` catalog count 2,105 first truncated an instruction. Treating its entire
registered 2,484-byte span as code then decoded into trailing jump tables and stopped.
A third rejected assumption equated the catalog count with conditional CFG coverage.
The corrected evidence separates **2,360 instruction bytes** from **124 original
table bytes** and resolves every direct/table target; the span's last table dword at
`00580830` is followed by an `INT3` alignment run before the next registered body,
`SaveLoad_FullImageStorageCompletionCallback`, at `00580840`. The catalog mismatch is
retained; the earlier outputs were never passed or counted as successful extractions.
See the evidence receipt for raw bytes and rejected scripts.

FABLE owns semantic and slot/rollback propagation; OPUS owns field widths, callback
ABI, state/notification contracts and affected executable consumers. Their primary
reviews remain required. The queue's true completion criteria, low32 token provenance,
popup delivery, same-object lifetime and current-context initialization remain open.
No final audit, reconstruction phase, integrated parity or full L1/L2 completion is claimed.
Section25 supplies the queue/PC-read continuation and the backup copy direction,
including an isolated partial-copy result; actual initialized delivery remains open.

## 25. Storage completion can follow a partial decoded-buffer read — ASTRA, 2026-09-13

**Player version:** the game first opens save data into a memory buffer, then copies
from that buffer into the active save image. The original copy routine can copy only
part of the requested data and return zero. Its caller does not distinguish that zero
from other nonnegative read results before closing the record. This explains a possible
route to a misleading load-success result; no damaged save was loaded in the live game.

[Evidence](../_experiments/evidence/spawn-storage-completion/README.md): 22 collected
original bodies and five reused bodies, two original tables. Method A connects their
conditional control flow. Method B executes only `00862590` and `00866A00`, without
stubs, against injected memory and the Windows x64 ABI. Seven complete cases, preceded
by two feasibility controls, retain90 reads and37 writes outside the stack. No original
file open, container decoding, close, game process or PC controls were used. This extends
section24's worker/prefix boundaries without establishing integrated live behavior.

### 25.1 The widget queue owns packet copies, not all pointed-to data

`00582540` copies a complete`0x58`-byte request to
`self+0xD8 + count*0x58`, then clears that copied request's flags dword`+4`.
The count is byte`+398`. **Exactly8 rejects admission**; it is not a `>=8` guard
for arbitrary injected counts. Ordinary constructor state starts it at0 and clears
the first dword of eight request slots. Null self also returns before copying.

Packet8 additionally copies a byte-counted array of`0x38`-byte records to the
auxiliary area at`+3A0`, using cursor byte`+39B`. If cursor+count exceeds16 it
resets the cursor to0, but does not clamp an oversized incoming count. It rewrites
the queued packet's pointer to that copied area. Other packet pointers, including
packet9's image destination, are merely copied. The caller's stack packet can end
after enqueue; pointed-to data and callback target lifetime remain separate.

After incrementing the count, an idle queue calls `00582040`. That entry refuses
null self, count0 or an already-started front record (flags bit0). Original table
`0058220C` maps packet1 to callback/token registration at self`+C0/+C8`, packet2
to device selection, and packet9 to `003BB440(name,0,destination,size)`. Immediate
operations return1; the queued native-operation arms mark bit0 and return0. The
packet9 arm **does not test `003BB440`'s return value**. Enqueue either completes
an immediate operation through `00582240`, or sets queue state byte`+CC=1`.

Queue handler `005823B0` message2 performs its initialization once, enables the
existing storage-pump gate through `0036FD80(1)`, and, while queue state is active,
waits for `003BB430()==0`. It completes the front request, then can consume several
immediate requests in the same update before stopping at a pending operation.
This is widget-driven polling. It is not proof that a new worker thread was created.
The existing [resource queue page](../02-Resource-And-Asset-Pipeline/the-resource-request-queue.md)
already identifies `003BB790` as the separate storage pump and its gate; that service
identity is re-derived here, not new. Actual tick ordering and initialized ownership
are still required for an integrated account.

`00582240` captures the front operation's low byte and notification-suppression
bit1, **decrements count and shifts remaining packets before calling the callback**.
It clears only the trailing slot's first dword. It does not locally reject count0;
calling completion with an empty queue would underflow its byte count. The callback
is the current self`+C0`, with zero-extended operation byte in ECX, result byte in
EDX and the stored32-bit token in R8D. Result is normally `003BB420()`'s low byte
(operations1/2 force zero), with additional overrides from `0017E470()`.
That getter reads `+10DC` on the existing `001D50D0` object; it is not an OS error
getter or a constant stub. Values1/3 override operations7/9 to9/8 respectively;
value2 overrides operations other than4 to3. These conditions can change a final
menu result independently of the memory-copy result.

### 25.2 Packet9 reaches a PC record backed by a decoded memory buffer

`003BB440` rejects an already-busy global job or size0 with return0. On admission
it copies the name through NUL, stores destination/size/offset at
`02B40EF0/02B40EF8/02B40EFC`, sets busy`02B40E10=1`, job kind`02B40E1C=1`, and
writes qword`02B40E14=1`, setting substate1 and result`02B40E18=0` together.
Its callers must preserve the single-job precondition; queue admission alone does
not certify that this second layer accepted a new job.

`003BB790` polls `00862600(1,null,&result)`. The PC adapter returns1, optionally
zeros its second argument, and copies global`02EAF8E0` into the third. The first
argument is ignored in this body. Thus it is an immediate result adapter; its return
does not itself perform or prove an I/O operation. The pump classifies errors and
dispatches job kind1 to `003BA7B0`. That function's original table at`003BA944`
resolves the read sequence:

| Substate | Local operation and next state |
|---|---|
| 1 | `008620D0` clears the PC result; advance to2 |
| 2, previous result0 | `008624D0(device,name,1)`; advance to6 |
| 6, result nonnegative | Store pseudo-handle result; seek first if offset>0, otherwise call `00862590`; next15 after seek, or8 after read |
| 15, result nonnegative | Call `00862590` with stored pseudo-handle; advance to8 |
| 8, result nonnegative | Call `008620E0`; advance to9 |
| 9, close result0 | Clear substate and outer result together, then clear busy |

Negative read results map to outer result8 for −3, otherwise9. Other preceding
failures take their own result9 path. **Substate8 checks only the sign of the read
result; it does not compare that result with requested size.**

`008624D0` first releases an existing global object if present, formats a path and
calls `008666B0`. With mode1, that function opens the physical file, reads it into
temporary memory and closes the CRT stream. It allocates a separate`0x210`-byte
record: cursor dword`+0`, mode dword`+4`, stored wide path at`+8`. Global`02EAF8E8`
therefore holds this **opaque cursor record**, not the CRT stream used earlier.
The corresponding data lives in the vector at`01F44D40/+8/+10` (begin/end/capacity).

`008666B0` recognizes the four bytes `SAFH`. Its container branch checks physical
length, a header dword at`+8<=31` and declared length`+4<=0x100000`, then calls
`00865D90` and checks returned output length before appending data. A non-SAFH
branch copies the file bytes into the vector. Several refused container branches
still return the allocated cursor record; a nonnull open result therefore does
not alone prove a populated vector. The transformation helper, allocation failure,
physical short-read effects and complete container contract remain open. No
reconstruction of that transformation or malformed-file live test was performed.

### 25.3 Original execution proves partial copying and its result encoding

`00866A00(record,destination,requested)` walks the shared vector from the record's
cursor, copying bytes and incrementing the cursor until the request is satisfied
or the cursor reaches the current vector length. It returns **1 only when the copied
count equals the requested signed32 count**, otherwise0 *(the count of iterations. With a destination that overlaps the
cursor dword, the store at `00866A4D` is followed by the cursor increment at `00866A54` on the same bytes, so the
copied content and the cursor both change. See the storage read contract's precondition; noted 2026-09-28, FABLE,
Claude Opus 5.5, on ASTRA's storage-read-cursor-alias)*. It does not undo writes
already made, or clear the unwritten destination tail. `00862590` calls it only for
pseudo-handle0 and stores `return_value * requested` in `02EAF8E0`; a nonzero
pseudo-handle instead stores −4. Thus a short copy becomes result0.

| Injected isolated condition | Observed original effects |
|---|---|
| 8 available, request8 | Copies8, cursor8, result8 |
| 3 available, request8 | **Copies3, cursor3, result0; remaining destination stays at its original sentinel values** |
| Empty vector, request8 | No destination writes, result0 |
| Cursor2, 12 available, request4 | Copies source bytes2–5, cursor6, result4 |
| Cursor8, only4 available | No destination writes, cursor remains8, result0 |
| Nonzero pseudo-handle | No memory-reader call, no destination writes, result−4 |
| Request0 | No destination writes, result0; this entry boundary bypasses the normal issuer's size0 refusal |

Both functions ran as verified shipping instructions with **no callback stubs**.
Every case returned with the stack/nonvolatile registers preserved, no invalid
memory access and unchanged code. Raw traces reject the proposed shortcuts
“zero means no writes occurred” and “short reads clear the remaining buffer.”
This is method B evidence for those entries, not an observation of a real save load.
The first feasibility attempt failed while importing the existing emulator and ran
zero instructions; that failure stays recorded as NOT RUN. Supported sandbox
escalation restored read access to the existing package; no tools were installed
or rebuilt. Python/emulator identities and raw evidence are retained.

Under the original substate8 sign check, that zero proceeds to close. For the normal
read-mode cursor record, `00866200`'s nonzero-mode branch frees the record, resets
the shared vector end to begin and returns0. `008620E0` clears the global record
and stores close result0. Substate9 then clears outer result0, which can reach the
section24 operation9/status0 callback if notification is enabled and no override
applies. **This last chain is conditional A composition.** The seven B cases did
not execute native open/decode/free/close, scheduler or parent notification, and
do not prove that any particular live save produces this condition.

### 25.4 Seek, close and prefix recovery have distinct effects

`008625D0` is **not a close operation**. For pseudo-handle0 it calls `00866A80`,
which computes a new cursor from start/current/end according to origin0/1/2 and
stores it only when the unsigned result is strictly less than vector length.
Seeking exactly to the end is refused. The adapter discards that return and
publishes result0, including when the nonzero pseudo-handle skips the seek.
`008620E0` is the close adapter. The resource queue page and FZ-18 ledger's
`008625D0 closes the handle` wording need peer-owned correction.

The read-mode close branch above must also be separated from `00866200`'s mode0
branch, which constructs a save container and uses temporary/backup file handling.
The full original body is retained, but its transformation and physical replacement
effects were not executed or established as atomic here. Treating this entire
function as a direct CRT `fclose` would lose native behavior.

`00583CB0` completes section24's backup direction: it copies exactly`0xE240` bytes
from active-image offset0 into the pointer at parent`+588`, using the same
`0x1C4*0x80+0x40` shape that `00583C00` copies back. The parent constructor
allocates that size and calls the backup function before normal resource setup.
**CORRECTED after FABLE primary review:** this prefix **excludes group bank A**.
The earlier statement that it included group A and ended at SpawnKeep A mixed
payload offsets with whole-image offsets, despite the correct table in section12.
The backup covers whole-image`[0,0xE240)`: the`0x200` header and payload
`[0,0xE040)`. Group A starts at whole-image`0xE240` (payload`0xE040`);
SpawnKeep A starts at whole-image`0xE440` (payload`0xE240`). Therefore neither
group A nor the SpawnKeep images are restored by this prefix copy.
[Five original bodies compared](../_experiments/evidence/spawn-prefix-boundary-correction/README.md)
confirm the copy and capture/restore coordinates; historical byte receipts and
measured copy length were correct and remain unchanged. It is not the fourth
global backup buffer and is not a full`0x56690`-byte rollback. Allocator success, original initialized
contents and all failure-path consequences remain separate.

FABLE/OPUS primary review and owned semantic/type/executable propagation remain
pending, including the seek/close correction. The container recipe is now traced
in section26; native file and allocation effects, callback lifetime and overrides,
and initialized save-to-area execution remain open. FABLE's slot0 producer review
is in the [request router section2](../16-UI/Request-Router/ui-request-router.md);
other slot-field writers and ordinary integration remain separate. L-12/L-13 and full L1/L2 with final
reviews remain open; no live automation restart or primary reconstruction is implied. *[Reconciled 2026-09-30 (FABLE): L-12 and L-13 are SUPERSEDED since; §7.]*

## 26. The SAFH save body is compressed, then encrypted — ASTRA, 2026-09-13

**Player version:** a save file wraps the game data in compression and encryption.
The small header number selects how a fixed game string is rearranged before the
encryption key is made. Reading that wrapper successfully is separate from checking
whether the resulting game state is valid. No save file or running game was used here.

Method A, [original bytes and checks](../_experiments/evidence/spawn-save-container/README.md):
ten collected bodies and two reused bodies from section25, shipping EXE SHA256
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`, base`00120000`.
The earlier V-9/V-10 questions and unsuccessful DEFLATE scans were read before this
work. They are historical evidence; encrypted bytes explain the lack of a visible
compression stream. No scan was replayed. The existing zlib family disposition is
retained and connected to actual save callers, rather than claiming a whole-library
implementation audit. Native library/provider execution and integrated parity remain separate.

### 26.1 The writer and reader establish the order

`00866200`'s **mode0** branch computes the shared vector length as a low32 pointer
difference, writes the 12-byte header, allocates two temporary buffers of that length,
and calls `0087AF40` with compression level **9** (`00866464`–`0086646C`). Only result0
continues to `00865AE0` (`00866493`). The compressor's destination capacity is the
uncompressed length, not a larger worst-case bound; a nonzero compressor result takes
the failure branch. Actual CRT writes/replacement/backup effects are not exercised here.

`0087AF40` has the zlib `compress2` shape: `0087C9F0` (`deflateInit_`), repeated
`0087BD60` calls, then `0087C6C0`; terminal result1 becomes0. Its initializer supplies
method8, window bits15, memory level8 and strategy0 to `0087C760`, with version string
**`1.2.11` at `01CC73A4`** and stream structure size`0x58`. This identifies the zlib
wrapper/DEFLATE path at the save boundary, not a raw-DEFLATE or gzip request.

The reader `008666B0` calls `00865D90(destination,&length,body,file_length-12)`.
`00865D90` allocates temporary space of the caller's declared output length, calls
**`00865840` first**, and only its true result admits **`0080C5A0`**. The latter is the
by-value source-length wrapper around `0080C5C0`, matching zlib `uncompress`/
`uncompress2`; `0080C5C0` initializes through `0080E040` (window bits15), calls
`0080C750`, publishes the output count and ends through `0080DF00`.
The original wrapper's zero-capacity scratch byte, consumed-input subtraction and
return-code mapping agree with [zlib 1.2.11 uncompr.c](https://github.com/madler/zlib/blob/v1.2.11/uncompr.c).

`00865D90` returns false on transform failure or nonzero decompressor result. Only
decompressor result0 updates the caller's length and returns true; the temporary
buffer is released on both paths. A failed decompressor may already have written to
its private destination. The outer reader appends those bytes to the shared vector
only after success and its additional size checks below.

### 26.2 The header word is a rotation selector, not a slot or payload seed

| Physical offset | Shipping writer / reader meaning |
|---|---|
| `+0x00` u32 | bytes `53 41 46 48`, `SAFH` |
| `+0x04` u32 | declared uncompressed vector length |
| `+0x08` u32 | selector `k`, admitted range **0..31** |
| `+0x0C` onward | encrypted zlib-compressed bytes |

The writer calls imported CRT `rand` at`008663C5`, takes the magnitude/remainder
modulo32 and stores the result both in header`+8` and global **`02EB3868`**. Under
the CRT nonnegative `rand` result, this is `rand()%32`; no uniform-distribution or
seeding claim follows. The reader restores that global from the header after its
selector check and **before** rejecting an oversized declared length.

Both `00865840` (decode) and `00865AE0` (encode) do the same setup:

1. Acquire provider **`Microsoft Enhanced Cryptographic Provider v1.0`**, type1,
   named container **`RSA_SQEX_FFXII_TZA`**, flags0. Any initial failure retries
   with flags8 (`CRYPT_NEWKEYSET`), without checking a specific error first.
   These are original import arguments, not provider operations performed by this research.
2. Copy the 32 ASCII bytes **`FINAL FANTASY XII THE ZODIAC AGE`** from `01CCFCF8`.
   Copy its last`32-k` bytes first, then its first`k` bytes: a left rotation by`k`.
3. **Overwrite rotated byte31 with NUL**, then find the string length. Because
   the original 32 bytes contain no NUL, exactly **31 bytes** are hashed. The
   terminator store is `00865961` / `00865C01`; hashing all32 would be wrong.
4. `CryptCreateHash` receives algorithm`0x8003`; `CryptHashData` receives the
   shortened string; `CryptDeriveKey` receives algorithm`0x6801` and flags`0x00800000`.

Microsoft's [algorithm identifiers](https://learn.microsoft.com/en-us/windows/win32/seccrypto/alg-id)
identify MD5 and RC4; [CryptDeriveKey](https://learn.microsoft.com/en-us/windows/win32/api/wincrypt/nf-wincrypt-cryptderivekey)
defines those flags as a128-bit key and derives this RC4 key from the hash bytes.
Thus the source/API recipe is **RC4 with the MD5 digest of the first31 bytes of
that rotated title**. The provider/container names do not make it an RSA payload.
The retry flag is documented by [CryptAcquireContextW](https://learn.microsoft.com/en-us/windows/win32/api/wincrypt/nf-wincrypt-cryptacquirecontextw).
No account-specific input is passed to the hash in either complete helper body.

For `k=0`, the hashed text ends in `AG`, omitting the final `E`; for`k=31` it is
`EFINAL FANTASY XII THE ZODIAC A`. These are source-derived illustrations, not
executed original-code fixtures or evidence of a native roundtrip. The full selector
range is local to the outer reader; the two transform helpers do not clamp an
independently injected global selector before their signed size/pointer arithmetic.

### 26.3 Chunking, cleanup and validity must be specified separately

Each transform copies at most **1000 decimal (`0x3E8`)** source bytes to its output,
then calls `CryptDecrypt` or `CryptEncrypt` in place using the same derived key.
The API's `Final` argument becomes1 only for a nonzero chunk shorter than1000.
After an exact multiple of1000, the next zero chunk exits successfully **without
another transform call**. Output advances by the API-returned byte count; source
advances by1000. Zero input still passes through setup but skips transformation.
This is the original call sequence, not a provider execution trace.

Decode does not read its output-length pointer as a capacity before these copies;
it only writes the resulting length on success. Encode reads its capacity and
passes the remaining value to `CryptEncrypt`, **after** copying the next input
chunk. Successful allocation and sufficient output storage are preconditions.
The outer reader caps declared output at`0x100000` but does not establish
`encrypted_body_length <= temporary_allocation_length` before decode. This is a
missing local length guard, not a demonstrated file or gameplay failure.

Failure of acquisition, hash creation/data, key derivation or a transform call
returns false after attempted cleanup of nonzero key/hash/provider handles.
Partial buffer effects are not rolled back. Cleanup return values do not overturn
a previously successful transform result; a successful boolean is not proof that
all OS handles were actually released. No provider resources were acquired here.

The outer reader's exact alternatives are significant:

- Physical length **<=4**, or a nonmatching magic, takes the raw-byte branch. A
  four-byte file containing exactly`SAFH` is raw by this test.
- Matching magic with length5..12 yields no decoded append. With length>12,
  selector>31 or declared length>`0x100000` also yields no append.
- Otherwise it requires transform/decompression success, returned length equal
  to the header declaration, and declared length>0 before appending the image.
- These rejected container branches still return the allocated opaque cursor
  record described in section25. A nonnull record does not certify decoded data.
- `0080C5A0` discards the consumed-source count returned by`0080C5C0`; the save
  wrapper does not separately enforce consumption of every body byte. Complete
  input consumption must not be invented as an established validity rule.

The gate does not compare declared length with the current`0x56690` image size,
nor call the image-stamp or gameplay-checksum routines. The stamp predicate in
EXP-058, checksum work in EXP-057, PC buffer read, queue status and later menu
notification remain distinct. A smaller decoded vector can reach section25's
partial-memory-read behavior under its stated conditions. No such file was loaded.

Checks re-read all12 byte spans, fresh instruction decodes, local branch targets,
import/branch/order anchors and four exact terminated literals. Two earlier guessed
UTF-16 lengths failed the terminator assertion and remain rejected in the receipts;
the accepted extraction scans within a fixed bound. No B/live cases were run or
counted, and historical mutations remain intact. V-9/V-10 and the middleware's
save-codec wording were routed to FABLE/OPUS for primary review and owned propagation.
FABLE independently completed the codec/selector explanation in commit`397c170`
and reports nine offline backup-file decodes with a32-byte-hash negative control
([save pipeline section8b](../19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/save-image-buffers-header-and-payload.md));
that is separate evidence from this A-only package and was not replayed here.
Its raw decode receipts still need ASTRA review. Section27 challenges the broader
no-conversion/session-retention conclusion against the native guard prelude;
remaining owned contract/native boundary agreement is not inferred from a report.
End-to-end native codec/file behavior, OS cleanup, ordinary callback/state delivery,
and L-12/L-13 integration remain open. This package does not complete L1/L2. *[Reconciled 2026-09-30 (FABLE): L-12 and L-13 are SUPERSEDED since; §7.]*

## 27. Load preparation can convert an earlier battle-state region — ASTRA, 2026-09-13

**Player version:** the load code has a compatibility step that copies an earlier
save-data region into the current battle-state block and rebuilds gambit records.
The earlier prediction that an old save merely keeps the session's existing block
missed this step. Its actual party, inventory and presentation consequences still
need initialized evidence; this package does not report a live load.

Method A, [original code and review](../_experiments/evidence/spawn-old-save-boundary/README.md):
eight collected bodies, three reused, exact shipping bytes and local branch targets
checked. FABLE's`397c170`/`401e080` reported decoding old`0x4E690` and current
`0x56690` images. Those completed decodes were not repeated here. This review
challenges the resulting no-conversion claim against its original native callers.

### 27.1 The stamp check has a mutating prelude

Section25's original memory reader can leave an unwritten tail unchanged. That
fact alone does not establish the state after the load's other code has run.
`00233C10` first calls **`00235AF0` at`00233C14`**, before testing either the block
pointer or its stamp. `00285E60`, reached through the selected-save success path,
calls this guard as described in section22.

Let`B = *(02EBF190)` and`L = active_image + 0x2200`. `00235AF0` returns on a null
`B` (and has a separate null`L` test). With both present, it compares in order:

| Field relative to each base | Width | Difference branch |
|---|---:|---|
| `+0` | u32 | `00235B1E` |
| `+4` | u32 | `00235B27` |
| `+0x5B42` | u8 | `00235B37` |
| `+0x5B12` | u16 | `00235B48` skips preparation only on equality |

All four equal means no preparation. **Any difference calls`002EF4A0`**, then
rebuilds records. This is not a complete-buffer comparison, an old-version number
test, or a length check. A modern image can take this branch if those values differ.

`002EF4A0` copies **`0xC0` iterations of`0x80` bytes = `0x6000` bytes**, from
**`02166480` to`021B290C`**. Against the original active base`02164280`, these are
**whole-image`+0x2200` to`+0x4E68C`**. The source is whole-image`[0x2200,0x8200)`,
or payload`[0x2000,0x8000)`. Its destination is the first`0x6000` bytes of the current
battle-state block. The copy uses fixed image addresses, while later preparation
uses the pointer`B`: agreement that`B == active+0x4E68C` is an initialized-state
precondition, not supplied by an arbitrary nonnull pointer.

The old image length`0x4E690` overlaps the current block's stamp at`0x4E68C` by
**four bytes**. ASTRA initially considered whether that overlap would force reset.
That hypothesis was incomplete: the prelude can replace the stamp from`L` first.
The compatibility source's end`0x8200` is entirely inside an old-sized image.
The reported presence of the stamp at`+0x2200` therefore cannot by itself prove
that the image lacks state suitable for this native import path.

### 27.2 The record rebuild extends beyond the copied region

After the copy, `00235AF0` iterates **40** times. Its destination bank group begins
at`B+0x5B10+i*0x9C`; the source record base advances by`0x1C8` per iteration.

- Bank0 receives exactly`0x34` bytes from`B+i*0x1C8+0x90`: three16-byte moves
  plus one dword, `00235BC4`–`00235BF8`.
- Banks1/2 are prepared as two`0x34`-byte records. The row selected from the
  table behind`02EBF130` supplies word`+0x14`; `00322C50(10,word,0)` gates a
  lookup into the table behind`02EBF0E0`, indexed by`word-0x5000`.
- A selected preset supplies at most12 pairs of u16s, from row offsets0 and
  `0x20` with two-byte progression. Either word`0xFFFF` terminates the copy.
  Filled pairs set corresponding bits in bank`+0x30`; remaining pairs become
  `0xFFFFFFFF` and their bits clear. Bank`+0x32` receives the source byte at
  `B+i*0x1C8+0xC2`. The complete helper does not write bank padding byte`+0x33`
  in these two reconstructed banks.
- The selected-bank index array is zeroed at`B+0x7370+i*4`, selecting bank0
  for every record. Forty bank groups span
  `0x5B10..0x736F`; the dword array spans`0x7370..0x740F`.

The [battle-state field map](../11-Party/Battle-State-Block/the-battle-state-block-field-map.md)
already identifies these three gambit banks and the available-entry byte. The
new connection is their preparation **before** the load guard's stamp decision.
Encoded table pointers, valid row definitions, callee behavior and initialization
remain required. The [original-instruction boundary review](../_experiments/evidence/gambit-import-null-boundary/primary-review.json)
distinguishes two failures: a null party-table descriptor or zero first resolver
result branches to`00235C4C` (`xor edi,edi`), then`00235C4E` attempts to read
word`[rdi+0x14]`. It does **not** safely reach the empty-preset fallback.
With a readable party row, a rejected preset id, null preset descriptor or zero
first preset resolver result instead reaches`00235CA9` and the empty-pair path.
That path fills twelve pair dwords with`0xFFFFFFFF`, clears only the **low twelve**
mask bits at`+0x30` and copies the available-entry byte to`+0x32`; the upper four
mask bits and padding`+0x33` are not changed by this bank loop. Empty pairs do not
mean a zeroed`0x34`-byte bank. Both banks repeat the lookups, so identical presets
also require stable source state. This is method A, not a live malformed-data
fault or proof of ordinary reachability; it does not establish that all padding
or the entire`0x7410`-byte block is freshly initialized.

After the prelude returns, a null`B` makes`00233C10` bind the active image and call
then tail-call`00237DF0`; a nonnull block with a mismatching stamp tail-calls it
once. `00237DF0 -> 0023AF50 -> 002370C0` begins by passing the current block,
zero, length`0x7410` to the imported CRT`memset` thunk`00861EC0`, then writes
stamp`0x05071901`. Further initializer calls remain distinct. `00237DF0` also
explicitly resets the spawn-history transition tick`02089374` to0, field ids
`02089372/02089370` to`0xFFFF` and byte`0208D454` to0 after its preceding native
calls return. This is one conditional reset path; it is not an all-load timer rule.

### 27.3 Both capture writers independently establish the larger copy

The save-payload page's earlier “first`0x80` bytes” mirror description counts one
iteration rather than the complete loop. There are two independent producers:

| Writer | Original loop | Source → destination | Complete length |
|---|---|---|---:|
| `005844A0` | ECX=`0xC0` at`0058451C`, eight16-byte moves, decrement/back edge`0058456E/72` | active`+4E68C` → active`+2200` | `0x6000` |
| `00229B40` | R8D=`0xC0` at`00229B7B`, eight16-byte moves, decrement/back edge`00229BDE/E2` | active`+4E68C` → active`+2200` | `0x6000` |

Both call`00234ED0` before this copy; section28 resolves its selected-bank export.
`005844A0` skips it and the copy when the first byte of the
current block is0. `00229B40` later copies a separate **`0x8000`** bytes from the
current block into staging`+4E68C`, then the **`0xE240`** image prefix into staging.
Neither of these lengths should be replaced with the block's`0x7410` logical size.
These are actual copy operands and loop bounds, not native snapshot-coherency proof.

FABLE/OPUS have P1 primary contradictions for the no-conversion/session-retention
claim and requests to propagate the copy extent through save maps, types, contracts
and the live-test prediction. FABLE's existing decoder script is a separate
reconstruction: it does not enforce all native container gates, and its built-in
32-byte alternative runs only after a31-byte decode fails. The reported standalone
negative control may have another receipt; that receipt, input/tool hashes and
old-image scan output were requested, not assumed absent or rerun.

Checks cover11 complete original byte spans, fresh decoding/local branch targets,
the prelude-before-stamp order, full copy extents, record bounds and stamp overlap.
No B/live or file decode was performed. User live permission was explicitly renewed
on2026-09-13 and recorded in the existing handoff/board; a new stop/takeover pauses
it again. *[Reconciled 2026-09-30 (FABLE): L-13 is SUPERSEDED since; §7.]* Native initialized old-save and L-13 bank/timer consequences remain open,
alongside peer consumer agreement. Full L1/L2 and final reviews are still required.

## 28. Compatibility export preserves the selected gambit set — ASTRA, 2026-09-13

**Player version:** before the compatibility save copy, FF12 puts each character's
selected gambit set into the older record. When the compatibility import runs,
that set becomes bank0 and is selected; the other two banks are prepared from
authored presets. This is a source-derived rule, not an observed older-save load.

Method A, [complete source and checks](../_experiments/evidence/spawn-compatibility-export/README.md):
`00234ED0` is a489-byte leaf function with no calls. For stable initialized
`B = *(02EBF190)` and `i=0..39`, it reads a **signed dword selector** from
`B+0x7370+4*i`, then copies `0x34` bytes from
`B+0x5B10+(3*i+selector)*0x34` to `B+0x90+i*0x1C8`.
Each record uses three16-byte moves followed by one dword, including padding.
Eight iterations of five unrolled records transfer `0x820` bytes across40
separate destination spans. The pointer is reloaded for each record.

This helper changes neither bank selection nor the other current banks. Its
only conditional branch is the loop back edge. **No selector clamp, range or
null guard exists here.** Valid selectors and stable binding are caller
preconditions; arbitrary injected selections can alias other memory. Preserve
the ordered moves if modeling such aliasing rather than assuming a snapshot.

Joined with section27: both writers call this exporter before copying the
`0x6000` compatibility region. The qualifying importer subsequently copies the
old per-record set into bank0, prepares banks1/2 and writes selection0. Its
four-field comparison still gates that conversion; this does not imply that
every current-format load discards two sets. `00229B40` also captures the separate
modern block. Native authored-data validity, initialized binding, actual load
trigger and presentation remain distinct evidence requirements.

The previous source receipt's `counters` interval key at `0x7370..0x740F` was a
generic label for these **selected-bank indices**, as the existing
[field map](../11-Party/Battle-State-Block/the-battle-state-block-field-map.md)
already establishes. The recorded interval and raw instructions are unchanged;
the prose now names their role. FABLE/OPUS own dependent contract/type propagation.

Checks verify all489 shipping bytes, each copy operand, signed selection and
complete loop extent, plus exact reused importer/writer bodies. One failed
source-file lookup was retained and corrected before a valid receipt; it was
not a failed live experiment. No original-code execution, save decode or game
control occurred. Initialized older-save and L-13 consequences remain open. *[Reconciled 2026-09-30 (FABLE): L-13 is SUPERSEDED since; §7.]*

## 29. An ordinary older-save load restores battle data before popup dismissal — ASTRA, 2026-09-13

**Player version:** the older-format test save loaded Rabanastre's Southgate and
restored six level21 character records. Their first gambit banks match the saved
compatibility records. The title screen's previous battle state was not retained.

[EXP-080](../_experiments/EXP-080-older-save-live-load.md) provides method-C
evidence: ordinary launch, manual slot004 load, Load complete popup, then area
entry. The preserved7066-byte file declares decoded size`0x4E690` and matches
EXP015's exact backup bytes. The verified reference process PID46768 was read
without game-memory writes, injected calls, hooks, debugger attach or suspension.
All three states/two samples each passed full-text and read controls. The first
module-list attempt was INVALID under sandbox access and retained; supported
read access allowed the unchanged observer to proceed.

At **Load complete, before dismissal**, the bound pointer is the native active
image block`021B290C`. Its first six stats levels changed from1,1,1,1,2,1 at title
to all21. The block's first`0x5B10` bytes equal the saved compatibility region's
prefix, and all40 bank0 records exactly equal its older per-record52-byte sets.
The full block differs from title in1545 bytes. These observations support the
source composition in §27/28 and contradict session-block retention for this
fresh-title case. They do not directly trace the importer calls.

| Window state | Field id | Last / previous history | Transition stamp | Raw tick samples | Parity |
|---|---|---|---:|---|---:|
| Fresh title | `000C` | FFFF / FFFF | 0 | 0,0 | 0 |
| Load complete | `0132` | FFFF / FFFF | 0 | 0,0 | 0 |
| Visible Southgate | `0132` | 0132 / FFFF | 0 | 1414,1429 | 1 |

Both keep banks were entirely zero at stable native pointers in every sample.
This state cannot discriminate bank retention, copy, swap or wipe. Selected-bank
indices were already zero at title, so final zero alone cannot prove the reset
write. The field/history/parity transition brackets some native area work;
intervening writers and exact call chronology remain open. No enemy death/respawn
test or visible post-load gambit/inventory menu inspection occurred.

FABLE's additional conditional clock-reset claim is accepted on primary evidence:
`0032A160` is eleven shipping bytes, zeroing dword`0208D45C` then returning;
the already captured`00237DF0` calls it at`00237E37`. This resolves that helper's
effect, without claiming that the reset occurred during this particular load.
FABLE's static compatibility correction`5895b65` is separate from this live run.

Mouse selection/confirmation worked. Down,k and the configured R input produced
no observed game response; keyboard-dependent same-session comparison was left
open pending existing input-receipt review. This is not a claim that all keyboard
delivery fails. FF12 exited normally; all26 original save/config hashes were
restored, backup unchanged, read handles closed and PC control released.
*[Reconciled 2026-09-30 (FABLE): L-13 is SUPERSEDED since; its live-only residue is routed, §7.]*
L-13 remains open for current-to-old session reuse, initialized nonzero banks,
native scheduling/caller order and player-visible consequences. Peer consumer
review, full L1/L2 and required final reviews remain outstanding.

## Residual placements — 2026-09-14 (SWE2-FRONTIER, residual-placement package)

| function | size | role (call-signature read) |
|---|---:|---|
| `004058E0` | 828 | ~~spawn-record body~~ **not a spawn function — corrected 2026-09-30 (FABLE), body read whole.** A per-frame step on the object in `rcx`: it advances a frame counter at `+0x178` against a limit at `+0x17A` (or, with `+0x130` bit 8 set, a table-driven step), writes two 16-bit extents at child `[+0xD0]` `+0x4A` / `+0x48` and a reciprocal scale at child `+0x98` (`004059A9`, `004059CC`, `00405A18`), and on completion clears bit 0 or bit 1 of `+0x130` (`00405BDB`–`00405BFC`). Nothing in it addresses a spawn or keep record, a battle unit or a spawn global, so the placement on this page, made from the call signature, does not hold; returned to SWE2-FRONTIER's residual placement. Signature as first recorded (callers `004061F0`/`00406770`): `[rcx+0x48]`/`+0x130`/`+0x178`, `[rbx+0x180..0x18C]`; `0035D460` context getter, `004076B0`, `00248F40` x2, `00245020` |

## 30. The `00582860` subtree — 9 exclusive members + one shared callee bound (SWE2-FRONTIER, followup queue; census corrected 8 → 10 on `AUDITSPEC-REQ-FRONTIER-582860-MISSED-PAIR`; exclusivity narrowed on `AUDITSEM-CONTRA-FRONTIER-582860-238A30`)

`SaveLoad_ControllerLifecycleHandler` (`00582860`, the `0x5A0`-byte load controller §12/§14
documents) owns **9 exclusive frontier functions** — the setup/teardown pair, the size selector, and the
status-step helpers its dispatch table reaches — plus **`00238A30`, bound here but shared**: two of
its three entry paths are in-subtree; the third is the script-verb thunk `0050F5A0`
(`mov ecx, 1; jmp 00238A30`), which sets the same bit unconditionally. Every member was disassembled
from the shipping image; interior cites are one instruction inside each extent.

| member | role | interior |
| --- | --- | --- |
| `00582790` (197 B) | the message-1 resource setup: `00249580`, `00393460`/`003933F0` table ops on `+0x100`/`+0x108` against the `00D23D80`/`00D23D98` descriptors, a `+0xC1`-gated pair of `00249210` lookups retaining `[rax+8]` at `+0x110`/`+0x118`, `00393600(2)` → `+0x120`, tails `00249410` | [`005827BC`](../_index/ADDRESS-INDEX.md) |
| `00582FC0` (114 B) | the common cleanup: `00393900(+0x100,1)`, `003938B0(+0x108,1)`, and when `+0xC1` is clear releases `+0x110`/`+0x118` via `003697F0` and nulls them | [`00582FCE`](../_index/ADDRESS-INDEX.md) |
| `00583040` `SaveLoad_HandleStorageStatusResultAndAdvanceController` (540 B) | the status-0 slot scan and advance: `003BB3E0`, `00244F00`, `00581350`, `00244DD0`, the `00244F50` widget creates for the `0057EDB0`/`0057FE80` handlers, `00583990`, `0057EC60` | [`005831A3`](../_index/ADDRESS-INDEX.md) |
| `00285E60` (55 B) | raises bits `0x200`/`0x400` of `[0209AC30]+0x400`, runs the `00233C10` battle-state guard, tails `002CFD10(-1)` — the request-flag writer §"capability" rows 9–10 document | [`00285E6B`](../_index/ADDRESS-INDEX.md) |
| `00581310` (56 B) | `00244F00`/`00291D40`/`002CA110`, then when `[02CA99B8]+0xC4` bit 3 is set runs `002CC9B0` → `002CC9C0` — a status probe on the controller object | [`0058132A`](../_index/ADDRESS-INDEX.md) |
| `005819A0` (80 B) | lazy init on `[02CA99C8]`: while `+0xCC` bit 0 is clear it runs `00249C60(0x42)` → `+0xE8` and raises the bit; always writes `cl` at `+0xD0` | [`005819C7`](../_index/ADDRESS-INDEX.md) |
| `00393600` (48 B) | the record-size selector: `cl` 0 → `0x3C4`, 1 → `0xE240`, 2–4 → `0x8398`, else 0 | [`00393614`](../_index/ADDRESS-INDEX.md) |
| `00394400` (17 B) | `[02AEE4C0]` non-null → `00244F00` — the conditional UI-state dispatch the bit-4 branch uses | [`00394400`](../_index/ADDRESS-INDEX.md) |
| `00238A30` (26 B) — **shared, not exclusive** | sets or clears bit 0 of `02089344` by its `ecx` arg — called twice in the `+0xC4`==3 arm (`00238A30(1)` at `00582CC8`, `00238A30(0)` at `00582CDE`) and once unconditionally via the script-verb thunk `0050F5A0` | [`00238A40`](../_index/ADDRESS-INDEX.md) |
| `00394520` (13 B) | `02CA9AC0` non-null probe — the guard the `00582EA2`/`00182D40` sequence tests at `00582EAC` | [`00394520`](../_index/ADDRESS-INDEX.md) |

`00244F00`/`00244F50`/`00249580`/`00249210`/`00249410`/`00249C60`, the `0039xxxx` table helpers,
`003697F0`, `00233C10`, `002CFD10` and `0057EDB0`/`0057FE80`/`00583990`/`0057EC60`/`00581350` are
shared callees — deliberately not census members.

## 31. The `003304A0` exclusive subtree — all 5 members bound (SWE2-FRONTIER, followup queue)

`ActorResource_OnPrimaryPayloadLoadedAndDispatchSubresources` (`003304A0`, 570 B) is the
EBP primary-payload dispatcher this page already names at its teardown mirror. The id it
receives is a **tagged pointer**: `tag = id & 0xF` selects one of sixteen subresource
channels and `rdi = id & ~0xF` is the payload descriptor (`003304C5`–`003304D9`).

The descriptor's `+4` dword is a section-count watermark; the body is a flat ladder of
`count > N && offset word nonzero → binder((rdi + off) | tag)` tests. Between
`0017FB70`/`0017FBE0` (`003304B7`, `0033056A`) it binds, in order:

| count | section offset | binder |
| --- | --- | --- |
| `> 0` | `+0x10` | `0032F850` |
| `> 2` | `+0x18` | **`00330190`** (member) |
| `> 3` | `+0x1C` | **`00330220`** (member) |
| `> 6` | `+0x28` | **`00330060`** (member) |
| `> 8` | `+0x30` | `0032FA10` |
| `> 9` | `+0x34` | `0032FAC0` |
| `> 0xA` | `+0x38` | `00331610` |
| `> 0xB` | `+0x3C` | `003316B0` |
| `> 0xC` | `+0x40` | `0032FB70` |
| `> 4` | `+0x20` | `00332100` |
| `> 0x10` | `+0x50` | `003320E0` |
| `> 0x11` | `+0x54` | **`00332110`** (member) |
| `> 0x13` | `+0x5C` | **`003320D0`** (member) |
| `> 0xE` and `tag != 0` | `+0x48` | `00330110` |

The per-tag state word `022C6E48[tag]` is a pending-work bitmap: the root sets bit 1 on
entry and bit 9 when the `> 0xC` section exists (`003304CD`–`003304F5`); the epilogue
clears bit 17 and runs the shared completion check — `word & ~1 == 0` fires
`00263FF0(tag)` and clears `+0x11` bit 3 of the channel record, and a nonzero→zero
transition calls `0032F1B0(tag)` (`0033068F`–`003306BF`).

| member | role | interior |
| --- | --- | --- |
| `00330060` (170 B) | section-`+0x28` bind: stores `base` into the per-tag pointer table `022C6CF0[tag]`, calls `0026C860(tag, base)`, clears **bit 6** of `022C6E48[tag]` and runs the same completion check, then `0017F790(id, base)` and tails `0029CAC0(base)` | [`00330097`](../_index/ADDRESS-INDEX.md) |
| `00330190` (138 B) | section-`+0x18` bind: stores `base` into `022C6CA0[tag]`, calls `0026C880(tag)`, clears **bit 4** of `022C6E48[tag]`, completion check | [`003301BB`](../_index/ADDRESS-INDEX.md) |
| `00330220` (138 B) | section-`+0x1C` bind: stores `base` into `022C6CC8[tag]`, calls `0026C8A0(tag)`, clears **bit 5** of `022C6E48[tag]`, completion check | [`0033024B`](../_index/ADDRESS-INDEX.md) |
| `00332110` (20 B) | section-`+0x54` bind: forwards `(1, base)` to `003DFE60` — a one-argument op on the aligned block | [`0033211A`](../_index/ADDRESS-INDEX.md) |
| `003320D0` (13 B) | section-`+0x5C` bind: forwards `base` to `003EAA00` — the block release | [`003320D5`](../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: the `0032F850`/`0032FAC0`/`0032FA10`/`003316B0`/
`00331610`/`0032FB70`/`003320E0`/`00332100`/`00330110` binders, the `0026C8xx` tag
handlers, `00263FF0`/`0032F1B0` (the completion pair), `0017F790`/`0029CAC0`,
`003DFE60`/`003EAA00`, and the lock pair `0017FB70`/`0017FBE0`. All three per-tag
pointer tables are `0x120000`-relative RVA tables — `lea r15,[rip-0x210084]`-style
bases, i.e. the image base plus a `.data` offset.

## The `003145E0` exclusive subtree — all 3 members bound (SWE2-FRONTIER, followup queue)

`WorldTransition_StageFieldTransition` (`003145E0`, ~~168 B~~ **563 B** — *corrected 2026-09-30 (FABLE): the extent
is `0x233` bytes, last instruction the `ret` at `00314812`; the description below stops at `0031467F`, and §16 reads
the whole body*) stages a field
transition: `r9d` chooses the `0032E520(1)` gate (early-out `eax = 1`,
`00314617`) vs `0032E520(0)` (`00314623`); then the once-only `0026E0D0`
(`00314634`), `003601B0(0xC)` (`0031463E`), three `0026A5F0` posts (1/2/3,
`00314648`–`0031465C`), and `002EF2B0` ×3 copying `dword[+0x1044]` →
`[+0x104C]` between records (`0031466E`–`00314674`) before `esi` lands in
`01EED064` (`0031467F`).

| member | role | interior |
| --- | --- | --- |
| `0020E500` (62 B) | two-call adapter — `001C18E0()` then `001C1720(rax, esi, edi, ebx)` (`0020E516`–`0020E526`) | [`0020E516`](../_index/ADDRESS-INDEX.md) |
| `0026E0D0` (30 B) | once-only gate — first entry runs `002509A0` and sets `byte[02099DA7]` (`0026E0D4`–`0026E0E2`), then forwards through `0209A6F0`/`0209A670`/`0209A678` to tail `00231400` (`0026E0F0`–`0026E11E`) | [`0026E0E2`](../_index/ADDRESS-INDEX.md) |
| `00583260` (76 B) | handler registrar — `00244F50(0x178, 0057E4D0)` under the `01F44830` cookie (`00583283`–`00583295`), `00808C40` epilogue | [`00583288`](../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `0032E520`, `003601B0`, `0026A5F0`,
`002EF2B0`, `001C18E0`, `001C1720`, `002509A0`, `00231400`, `00244F50`,
`00808C40`. *(2026-09-30: this list covers the part described above; the whole body calls 20 distinct targets, §16.)*

## The `00584580` exclusive subtree — all 2 members bound (SWE2-FRONTIER, followup queue)

`00584580` `WorldTransitionSnapshot_CapturePersistencePairForActiveSlot`
(~~238 B~~ **143 B** — *corrected 2026-09-30 (FABLE): the extent is `0x8F` bytes, last instruction the `ret` at
`0058460E`, as §12 says; a 238-byte window runs into the following function*) — the persistence-pair capture: `002EF620`, `00236760`,
`0025D8E0`, `00233440`, `002EF3C0` (`00584586`–`005845B6`), the
active-slot index `movsx byte[0208D455]` (`005845BB`), a second
`0025D8E0` + `00233440` pair (`005845D5`/`005845E1`), `002EF510`, ~~and
`003935C0` (`00584652`)~~ then the two members `002EF7C0` and `002EF740` (`005845F2`, `005845F7`). *(Corrected
2026-09-30: `00584652` lies past this body's end, in the next function.)*

| member | role | interior |
| --- | --- | --- |
| `002EF740` (122 B) | ~~0x400-byte block move~~ **keep image A copied from the active image to staging, `0x20010` bytes: `0x400` iterations of 128 bytes plus a 16-byte tail** (corrected 2026-09-30, FABLE; as §12 says) — ~~`021C8D80` → `021726C0`~~ `021726C0` → `021C8D80`, `edx = 0x400` the iteration count (`002EF740`/`002EF747`/`002EF74C`) | [`002EF74C`](../_index/ADDRESS-INDEX.md) |
| `002EF7C0` (116 B) | ~~4-element copy~~ **group A copied from the active image to staging, `0x200` bytes: 4 iterations of 128 bytes** (corrected 2026-09-30, FABLE; as §12 says) — ~~`021C8B80` → `021724C0`~~ `021724C0` → `021C8B80`, `edx = 4` the iteration count (`002EF7C0`/`002EF7C7`/`002EF7CC`) | [`002EF7CC`](../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `002EF620`, `00236760`, `0025D8E0`,
`00233440`, `002EF3C0`, `002EF510`~~, `003935C0`~~. `0208D455` is the
shared active-slot byte.

## The `001831A0` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`001831A0` (~~17 B~~ **21 B**, corrected 2026-09-30: the tail `jmp` at `001831B0` ends the `0x15`-byte extent) — singleton forwarder: `call 001D8A60` then tail `jmp
001D8A90` on the returned object (`001831A4`/`001831B0`).

| member | role | interior |
| --- | --- | --- |
| `001D8A90` (27 B) | zero-float latch — when `float[+8]` compares `== 0` (`ucomiss`, unordered-or-equal path) sets `byte[+0x1D] = 1` and clears `dword[+8]` (`001D8A98`/`001D8A9F`) | [`001D8A9F`](../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `001D8A60`.

## The `00235AF0` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`00235AF0` (~700 B) — a transition-record compare/copy pass:
`002EF640()` yields the record, `rax + 0x2200` the compare block
(`00235AF4`/`00235B00`); each `dword`/`word` of `qword[02EBF190]` is
compared against it (`00235B19`/`00235B1E` …), `002EF4A0` ~~copies the~~
~~matched row~~ copies the `0x6000`-byte block when any of the four compared values differs *(corrected 2026-10-02, OPUS: `00235B1E`, `00235B27` and `00235B37` `jne 0x235b4e` to the call; only all-equal reaches `00235B48` `je 0x235dac`, the skip; §27)* (`00235B76`), and four `0020E600` scratch reads plus
`00322C50` finish (`00235C20`–`00235C85`).

| member | role | interior |
| --- | --- | --- |
| `002EF4A0` (103 B) | record copy — ~~`movups` over `0x30`-stride rows~~ **`0xC0` iterations of 128 bytes = `0x6000` bytes** (`mov edx, 0xC0` at `002EF4A7`); the `[rax-0x30]` at `002EF4E8` is an offset inside the 128-byte chunk, not a stride (corrected 2026-09-30, FABLE; as §27 says) (`002EF4E8`) | [`002EF4E8`](../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `002EF640`, `0020E600`, `00322C50`.

## The `00314440` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`00314440` (`WorldTransition_RequestFieldTransition`, ~~\~117 B~~ **233 B**, corrected 2026-09-30 (FABLE): `0xE9`
bytes, last instruction the `ret` at `00314528`; §17 reads it whole) — arg
shuffle `esi = r9d` (`00314454`).

| member | role | interior |
| --- | --- | --- |
| `00254AC0` | `dword[02092744] == 0` gate, then `01E0C320 & 0xC0 == 0xC0` check (`00254AC4`/`00254AD8`) | [`00254AC4`](../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: ~~none~~ *corrected 2026-09-30 (FABLE): the whole body makes 13 direct calls to 12
distinct targets — the member, the staging function `003145E0` twice (`0031448C`, `0031449A`; §17) and ten others;
their exclusivity is not re-derived here.*

## The `0032ED80` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`0032ED80` (`ActorResource_ResetManagerLoadState`, ~~\~62 B~~ **1,001 B**, corrected 2026-09-30 (FABLE): `0x3E9`
bytes, the last instruction the range-failure call at `0032F164`; §14 and §15 read its resource-mask reset at
`0032F0FF`) —
five-register reset body (`0032ED80`/`0032ED96`) *(its prologue only)*.

| member | role | interior |
| --- | --- | --- |
| `0029CB10` | `0209C320` base, `rcx` pointer-identity scan (`0029CB16`/`0029CB20`) | [`0029CB16`](../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: ~~none~~ *corrected 2026-09-30 (FABLE): the whole body makes 60 direct calls to 18
distinct targets; their exclusivity is not re-derived here.*

## The `0037AA90` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`0037AA90` (~~\~78 B~~ **491 B**, corrected 2026-09-30 (FABLE): `0x1EB` bytes, last instruction the `ret` at
`0037AC7A`) — `movsxd r12, edx`, `r13 = rcx`
(`0037AA98`/`0037AA9B`).

| member | role | interior |
| --- | --- | --- |
| `0037A9B0` | `ecx x10` into `02EBF420` — same 80-byte-stride record family as `0037B290` (`0037A9B0`/`0037A9BD`) | [`0037A9B0`](../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: ~~none~~ *corrected 2026-09-30 (FABLE): the body makes three direct calls, to the
member and two other targets; their exclusivity is not re-derived here.*

## The `00510710` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`00510710` (5 B) — `jmp 0023A520` thunk.

| member | role | interior |
| --- | --- | --- |
| `0023A520` | `009146EC`/`009146F0` floats -> `02089360` — spawn defaults (`0023A520`/`0023A530`) | [`0023A520`](../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none.

## The `00584490` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`00584490` (`SaveImage_BackupActiveRuntimeBuffer`, 5 B) — `jmp 002EF570`.

| member | role | interior |
| --- | --- | --- |
| `002EF570` | `022676C0` dest + `edx = 0xACD` size + `02164280` source — the runtime-buffer backup (`002EF570`/`002EF57C`) | [`002EF570`](../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none.

## Cross-subsystem neighbours — SWE2-EC7 (pass-22 dispositions)

- **Actor - CLIENT and SERVICE (3 edges).** `0037A9B0` is also called by bodies filed to Actor: `0037AA90` (ResourceAuxiliaryTable); `0032F1B0`, `003775D0` reach bodies filed to Actor: `0037AA90` (ResourceAuxiliaryTable) - shared machinery across the layer boundary, no shared ownership.
- **ActorEntity - CLIENT and SERVICE (302 edges).** `0017F790`, `0017FB70`, `0017FBE0` are also called by bodies filed to ActorEntity: `00330060`, `003304A0`; `0022A0B0` reaches bodies filed to ActorEntity: `002368D0` - shared machinery across the layer boundary, no shared ownership.
- **Audio - CLIENT and SERVICE (21 edges).** `001EDDA0` is also called by bodies filed to audio: `003B99D0`; `00261F90` reaches bodies filed to audio: `002DEC00`, `002DEE50`, `00360D30` - shared machinery across the layer boundary, no shared ownership.
- **CombatAI - CLIENT and SERVICE (32 edges).** `00308040` is also called by bodies filed to combat AI: `00301830`; `00233C10`, `00233F70` reach bodies filed to combat AI: `00327F80`, `00308610`, `003247F0` - shared machinery across the layer boundary, no shared ownership.
- **CombatAction - SERVICE (68 edges).** `00233F70`, `002342F0` reach bodies filed to combat action: `0030CA50`, `00306570`, `0030E010` - shared machinery across the layer boundary, no shared ownership.
- **CombatFormula - CLIENT and SERVICE (11 edges).** `00265020` is also called by bodies filed to combat formula: `00384F40`; `002352E0`, `00237DF0`, `00300520` reach bodies filed to combat formula: `00300520`, `0023AC80`, `00300530` - shared machinery across the layer boundary, no shared ownership.
- **CoreRuntimeScheduling - CLIENT (43 edges).** `00182D40`, `001831A0`, `00198790` are also called by bodies filed to core runtime: `0022B8C0`, `0017D4C0`, `0017D670` - shared machinery across the layer boundary, no shared ownership.
- **Gameplay - CLIENT and SERVICE (28 edges).** `00234DA0`, `0023AF50` are also called by bodies filed to Gameplay: `00308040` (Combat), `00237DF0` (Combat); `00233C10`, `00235AF0` reach bodies filed to Gameplay: `00237DF0` (Combat), `00322C50` (Combat) - shared machinery across the layer boundary, no shared ownership.
- **Input - SERVICE (72 edges).** `00182D40`, `00182D80` reach bodies filed to input: `001986E0`, `00198790`, `00198700` - shared machinery across the layer boundary, no shared ownership.
- **InputGameplay - CLIENT (1 edge).** `00377C20` is also called by bodies filed to InputGameplay: `00313A00` (FieldBattleCapabilityAndUIRequestInhibitMaskReconciliation) - shared machinery across the layer boundary, no shared ownership.
- **Items_Equipment_Shops_License - CLIENT and SERVICE (20 edges).** `002370C0` is also called by bodies filed to items/equipment: `0023AF50`; `00233C10`, `00237DF0`, `0023AF50` reach bodies filed to items/equipment: `0030B6A0`, `0023AF50`, `00300BA0` - shared machinery across the layer boundary, no shared ownership.
- **Movement - CLIENT and SERVICE (106 edges).** `001EDDA0` is also called by bodies filed to movement: `0025DF00`; `00231400` reaches bodies filed to movement: `0022F830`, `00233050`, `00233110` - shared machinery across the layer boundary, no shared ownership.
- **Party - SERVICE (42 edges).** `00234AF0`, `00234DA0`, `002350C0` reach bodies filed to party: `003272A0`, `003273B0` - shared machinery across the layer boundary, no shared ownership.
- **PlatformOnlineAchievements - CLIENT and SERVICE (3 edges).** `003148F0`, `003160C0` are also called by bodies filed to PlatformOnlineAchievements: `003160C0`, `00315E90`; `00584210` reaches bodies filed to PlatformOnlineAchievements: `00316810` - shared machinery across the layer boundary, no shared ownership.
- **Presentation - CLIENT and SERVICE (158 edges).** `0017F3B0` is also called by bodies filed to presentation: `00180E70` (Graphics), `00181000` (Graphics); `0017F3B0`, `0017F790` reach bodies filed to presentation: `0061E200` (EffectFont), `001B47A0` (EffectFont) - shared machinery across the layer boundary, no shared ownership.
- **RNG_Random_Selection - SERVICE (7 edges).** `0022A0B0`, `002342F0`, `00234AF0` reach bodies filed to random selection: `00379CF0`, `00328D80`, `00328370` - shared machinery across the layer boundary, no shared ownership.
- **Resource - CLIENT (80 edges).** `00180E70`, `00181000`, `00181190` are also called by bodies filed to resource: `0024A1D0` - shared machinery across the layer boundary, no shared ownership.
- **Rewards_Progression_Economy - CLIENT and SERVICE (8 edges).** `00265020` is also called by bodies filed to rewards/progression: `002FB150`, `00312280`; `002342F0`, `00306760` reach bodies filed to rewards/progression: `00319B10`, `0030C470` - shared machinery across the layer boundary, no shared ownership.
- **SaveLoad - CLIENT (31 edges).** `001C1720`, `001C18E0`, `0020E4E0` are also called by bodies filed to SaveLoad (save/load settings): `0020E500` (WorldTransition), `00280140` (RuntimeLifecycleSupport) - shared machinery across the layer boundary, no shared ownership.
- **Save_Load_Settings - CLIENT and SERVICE (226 edges).** `0017E470`, `00182D40`, `001831A0` are also called by bodies filed to save/load/settings: `00582240`, `00582860`; `001C1720` reaches bodies filed to save/load/settings: `002EF390` - shared machinery across the layer boundary, no shared ownership.
- **Script_VM_Native_Bridge - CLIENT (135 edges).** `001831A0`, `00234990`, `00234A10` are also called by bodies filed to script VM / native bridge: `00354D00`, `00349500`, `00349940` - shared machinery across the layer boundary, no shared ownership.
- **Status_Periodic_Terminal - CLIENT and SERVICE (13 edges).** `002F8060`, `003125E0` are also called by bodies filed to status/periodic terminal: `00310DB0`, `00301140`; `00233F70`, `002342F0` reach bodies filed to status/periodic terminal: `00310DB0`, `0030E990` - shared machinery across the layer boundary, no shared ownership.
- **Story_Event_Quest_Hunt - CLIENT and SERVICE (15 edges).** `002EF2B0` is also called by bodies filed to story/event: `0032A8A0`, `0032A930`, `0032A9A0`; `0026C8C0` reaches bodies filed to story/event: `00377440` - shared machinery across the layer boundary, no shared ownership.
- **UI - CLIENT (216 edges).** `00181000`, `00181250` are also called by bodies filed to UI: `00291010`, `002917E0` - shared machinery across the layer boundary, no shared ownership.
- **World - CLIENT and SERVICE (8 edges).** `002342F0`, `0026DB30` are also called by bodies filed to World: `00266D10` (NativeSupport); `0022A0B0`, `00314020` reach bodies filed to World: `00266D10` (NativeSupport), `002623A0` (ActorManager) - shared machinery across the layer boundary, no shared ownership.
- **WorldAreaField - CLIENT (192 edges).** `00182D80`, `001831A0`, `001D6C40` are also called by bodies filed to WorldAreaField (world area): `00314440`, `00314530` - shared machinery across the layer boundary, no shared ownership.

`004058E0` (827 B) is the spawn-record field apply `004061F0` runs: the signed 16-bit `+0x178` field classifies, bit `0x08` of `+0x130` gates the arm, `0035D460` resolves the record row, and `00245020`, `00248F40` and `004076B0` write the derived fields - the placement-parameter stage of the retirement/respawn record update.

Interior anchor `00405AC5` (function `004058E0`).
