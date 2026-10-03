---
system: Spawn placement height, the minimum-distance flags, and the authored tunable set
category: 05-Spawn-Encounter-Lifecycle
status: AUDITED
owner_layer: PrimaryOwner:Spawn_Encounter_Lifecycle
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
  last_pass: 2026-09-07
  last_pass_state: GN160-xiionline-61-constants-installer-and-corrections
  crossref_clean: true
  reopened_count: 0
  falsification_passes: 1
  last_falsification: 2026-09-03
  last_falsification_by: repos-9e
  last_falsification_state: GN158 checkpoint, project GFZ_H9E
  falsification_result: 0 overturned, 11 claim groups survived, 2 refinements - see section 11
---

# Spawn placement height, the minimum-distance flags, and the authored tunable set

> How a chosen spawn point becomes a monster actually standing on the ground in front of
> you — what decides its height, what decides whether it may appear on top of you, and which
> zone script installs the numbers that govern both.

This document closes **L-7**, **L-9** and **L-10** from
[`spawn-placement-and-retirement.md`](spawn-placement-and-retirement.md), and corrects two
claims in that document (§8, *Superseded readings*).

## 1. What the player sees

**Monsters stand on the ground, and the game asks the ground where that is.** When a zone
generates a spot for a wandering monster, it only picks a spot on the flat map — a distance
and a direction. It does not pick a height at all. The height is filled in a moment later, at
the instant the monster is actually placed, by asking the terrain *"what is the floor under
this spot?"* and dropping the monster onto it, plus a small per-monster lift authored into
that monster's own definition. That lift is why a flying enemy hovers and a ground enemy does
not.

**Not every monster gets asked.** Whether a monster is dropped onto the terrain is a switch in
its authored definition. A monster whose definition does not set that switch is placed at
whatever height the engine happened to be carrying — the game never computes one for it.

**Monsters can absolutely materialise on top of you — but only once.** The rule that keeps a
monster from appearing in your face is a *minimum distance*, and it is switched off by default
for a monster that has never been alive yet in this visit. That is why the first monsters you
meet on entering a zone can be standing almost anywhere, including right next to you — that
placement is the zone populating itself. Once a monster has been alive once, the engine
remembers it, and every later respawn of it is pushed out to the minimum distance. So the
"it spawned in my face" experience belongs to arrival, not to fighting.

A zone author can override this. There is an authored instruction meaning *"this is not an
arrival placement — treat it as a respawn"*, and a zone that uses it gets the minimum distance
enforced even on the very first placement. **167 zone scripts use it.**

**The famous 39-to-42 spawn ring is a script default, and most zones that care replace it.**
The engine *holds* those numbers — they sit in the executable as constants — but **it never applies
them by itself.** The tunables they are copied into start every run empty, and stay empty until a
zone installs them. Every zone that can spawn anything
begins its battle setup by installing a default set — a ring of 39 to 42 units, a retirement
range of 43, a forward half-circle, and one placement attempt — and then, if it wants
something else, overwrites it. Most zones that override do so drastically: the commonest
authored ring is **5 to 12 units**, not 39 to 42, so monsters in those zones appear much
closer than the default suggests. Two zones open the arc to the **full 360°**, so in those two
places monsters genuinely can appear behind you.

**The 28-monster ceiling is essentially never the real one.** 167 zone scripts set their own
active-actor cap, and every one of them sets it between **2 and 9**. A zone that feels
crowded is a zone authored to allow six or seven at once, not twenty-eight.

## 2. Native mechanism

### 2a. Nothing generates a Y coordinate — L-7

Area-mode placement in `Spawn_TrySelectCandidatePosition` (`00234AF0`) builds the candidate
point through `FUN_00319390`, a polar-offset helper. Its complete 139-byte body writes
**two** floats:

```asm
00319411  movss dword ptr [rdx], xmm3        ; out.x
00319415  movss dword ptr [rdx + 8], xmm5    ; out.z
0031941A  ret
```

`[rdx + 4]` — the Y — is never touched. The caller passes `rdx = rsp+0x50`, a stack slot it
never initialises either: mapping the whole frame of `00234AF0` (`sub rsp,0x100` after five
pushes, so `rsp+0x50` is `entry_rsp - 0xD8`) shows every one of its own stores landing
elsewhere, and every callee's frame lying *below* `rsp`, where it cannot reach that slot.
**The Y that comes out of area-mode generation is whatever the stack happened to hold.**

It is then read and forwarded. On success the function copies all three components into the
caller's output vector:

```asm
00234CD2  movss xmm0, dword ptr [rsp + 0x50]   ; x
00234CDD  movss xmm1, dword ptr [rsp + 0x54]   ; y  <- the uninitialised slot
00234CE3  movss dword ptr [rbx], xmm0
00234CE7  movss xmm0, dword ptr [rsp + 0x58]   ; z
00234CED  movss dword ptr [rbx + 8], xmm0
00234CF2  movss dword ptr [rbx + 4], xmm1
```

**It does not affect whether the point is accepted.** The only filter on the area-mode path is
`FieldRegion_ContainsWorldPosition` (`002374E0`), and neither it nor the transform it calls,
`Vector3_RotateTranslatedXZOffsetByEncodedAngle` (`00325EA0`), ever reads component `[1]`:
the transform reads `[rcx]` and `[rcx+8]` only, and the containment test compares the two
values the transform returns. So the stale height rides along unexamined — it is carried, not
consulted.

`Spawn_SelectAndPrepareAutomaticEntry` (`00235720`) then stores the candidate into the
spawn-keep entry as two whole 16-byte moves, so the stale Y is banked with everything else:

```asm
00235A08  movups xmmword ptr [rdi + 0x60], xmm9
00235A0F  movups xmmword ptr [rdi + 0x50], xmm9
```

### 2b. What actually supplies the height — the ground probe

The height is decided at activation, not at generation.
`SpawnUnit_FinalizeSpawnEntryActivation` (`0023A410`) is the function that turns a prepared
entry into a placed actor, and it opens with a per-unit gate:

```asm
0023A49E  test byte ptr [rbx + 0x1f6], 8      ; height-probe opt-in
0023A4A5  je   0x23a4da                       ; not set -> skip the probe entirely
0023A4A7  mov  rax, qword ptr [rbx + 0x6a0]   ; the spawn-keep entry (BKEI)
0023A4AE  movss xmm1, dword ptr [rax + 0x68]  ; candidate Z
0023A4B3  lea  r8, [rax + 0x64]               ; OUT: the Y slot
0023A4B7  movss xmm0, dword ptr [rax + 0x60]  ; candidate X
0023A4BC  call 0x3208c0                       ; ground probe
0023A4C1  mov  rax, qword ptr [rbx + 0x6a0]
0023A4C8  movss xmm0, dword ptr [rbx + 0x188] ; per-unit vertical offset
0023A4D0  addss xmm0, dword ptr [rax + 0x64]
0023A4D5  movss dword ptr [rax + 0x64], xmm0  ; Y = ground + offset
0023A4DA  mov  rdx, qword ptr [rbx + 0x6a0]
0023A4E7  add  rdx, 0x60                      ; the position vector
0023A4F1  call 0x300310                       ; BattleUnit_PublishLocomotionPosition
```

So `BKEI + 0x60 / +0x64 / +0x68` are the X / Y / Z the actor is placed at, and **the Y is
overwritten by the probe before the placement call — when the gate bit is set.**

`FUN_003208C0` (119 B, Movement) is the probe. It builds a 4-float query, seeds the height
slot with `1.0`, asks the field for the surface under (X, Z), and reports whether it found
one:

```c
float probe[4] = { x, 1.0f, z, 1.0f };          // 003208E1 .. 00320900
short r = FUN_0026E3C0(g_field, &probe);        // 00320900
*outY = ((short)r != -1) ? probe[1] : 0.0f;     // 00320905 .. 0032091A
return ((short)r != -1);                        // 0032091E
```

Two consequences worth stating plainly:

- **A failed probe yields `0.0`, not the leader's height.** If the chosen point has no
  collision surface under it, the monster is placed at absolute world height zero.
- **`SpawnUnit_FinalizeSpawnEntryActivation` ignores the return value.** It calls the probe,
  adds the offset and publishes, without ever testing whether a surface was found. A spawn
  point over a hole in the collision data therefore produces a monster at world `Y = 0 +
  offset` and no error.

### 2c. Which monsters get the probe

The gate byte `BattleUnit + 0x1F6` has exactly **one writer in the whole binary** and exactly
one reader. The writer is `FUN_00239E10` (`00239E10`, 594 B, ActorEntity) — the routine that
applies a unit's authored definition, called from
`BattleUnit_ActivateAppliedDefinitionRuntime` at `00233B51`:

```asm
00239E70  mov   ebp, 8                          ; unconditional, straight-line
...
00239F93  mov   rax, qword ptr [rdi + 0x698]    ; pBkbi
00239F9F  movzx eax, byte ptr [rax + 5]
00239FA5  jne   0x239fab                        ; spawn-backed -> definition path
00239FA7  mov   ecx, esi                        ; NOT spawn-backed -> esi (1, 2 or 3)   # <- corrected 2026-10-02, OPUS - esi is 1 here (00239E33 mov esi, 1, not rewritten before 00239FA7); 2 and 3 are later values for +0x1F4 (00239FEC, 00239FF9)
00239FA9  jmp   0x239fd4
00239FAB  mov   rax, qword ptr [rdi + 0xe68]    ; the applied definition record
00239FB2  movzx edx, byte ptr [rax + 0x18]      ; definition flags byte
00239FB6  test  dl, 0x10
00239FB9  jne   0x239fc9                        ; bit 4 SET  -> keep ebp = 8
00239FBB  test  dl, 0x20
00239FBE  mov   ebp, 0
00239FC3  setne bpl
00239FC7  inc   ebp                             ; bit 4 clear -> ebp = 1 or 2
00239FC9  mov   ecx, ebp
00239FCB  or    ecx, 4
00239FCE  and   dl, 0x40
00239FD1  cmove ecx, ebp                        ; bit 6 adds +4
00239FD4  mov   byte ptr [rdi + 0x1f6], cl
```

`ebp` is loaded with `8` unconditionally at `00239E70` and is callee-saved across the twelve
intervening calls, so the value `8` survives to `00239FC9` whenever the definition's byte
`+0x18` has **bit 4** set.

**Therefore the ground probe runs if and only if the unit is spawn-backed *and* its authored
definition sets bit 4 of definition byte `+0x18`.** The possible values of `BattleUnit+0x1F6`
are `1, 2, 5, 6` (no probe) and `8, 12` (probe). A non-spawn-backed unit takes the `esi` path,
whose ~~values are 1, 2 and 3~~ value is 1 *(corrected 2026-10-02, OPUS: `esi` is set to 1 at `00239E33` and not written again before `00239FA7`; it becomes 2 or 3 only afterwards, for `+0x1F4`, at `00239FEC`/`00239FF9`; §7 says a party unit gets 1)* — never 8 — so a party member never goes through this path at all.

The vertical offset added afterwards, `BattleUnit + 0x188`, is written by the same definition
applier at `0023A026`, from the same authored record.

### 2d. The two flags that decide the minimum spawn distance — L-9

The mask is read at exactly one place in the binary:

```asm
0023581D  movabs r10, 0x2200000000000       ; 49 ba 00 00 00 00 00 20 02 00
...
002358EB  test  qword ptr [rsi], r10        ; rsi = the BattleUnit
002358EE  jne   0x2358f5
002358F0  xorps xmm7, xmm7                  ; minR = 0.0
002358F3  jmp   0x2358fd
002358F5  movss xmm7, dword ptr [rip + 0x1e53a63]   ; minR = g_flAutomaticSpawnMinPlayerDistance
```

The immediate's eight bytes are `00 00 00 00 00 20 02 00`, little-endian
`0x0002200000000000` — nibble 12 = `2` (bits 48-51 → **bit 49**) and nibble 11 = `2`
(bits 44-47 → **bit 45**). **The bits are 45 and 49.** The existing document's "bit 49 or
bit 53" is arithmetically wrong; `bit 49 | bit 53` would be `0x0022000000000000`, a different
constant that does not appear in this instruction.

An exhaustive census over all 38,161 ledger bodies — every 64-bit immediate carried into a
memory `or` / `and` / `bts`, plus every `bt`/`bts`/`btr`/`btc` with an immediate of 45 or 49 —
finds these and only these:

| Bit | Written by | Instruction |
|---:|---|---|
| 49 | `BattleUnit_ActivateAppliedDefinitionRuntime` (`00233AD0`) | `or qword ptr [rbx], rax` at `00233B8C` |
| 45 | `FUN_005102D0`, ScriptVM primitive **`0x304D btlAtelCanselInitialSpawnFlag`** | `or qword ptr [rax], rcx` at `005102EB` |

Neither bit is cleared anywhere. `BattleUnit_ResetStateForReuse` (`00236A60`) masks
`qwUnitFlags` with `0xFFFF7FFDFFE7FFFD`, whose complement is `0x0000800200180002` — it clears
bits 1, 19, 20, 33 and 47 and **preserves both 45 and 49 across unit reuse**.

**Bit 49 is the activation latch.** It is set in the once-per-unit initialisation block of
`BattleUnit_ActivateAppliedDefinitionRuntime`, on the straight line between `or dword ptr
[rbx], 8` (the "initialised" marker) at `00233B4B` and the spawn-backed
`ACTIVATION_COMMITTED` write at `00233BA8`. Every battle unit that has ever been activated
carries it; a unit that has never been activated does not.

**Bit 45 is script's override.** `btlAtelCanselInitialSpawnFlag` is three lines:

```c
unit = ActorWork_GetBattleUnit(arg);         // 005102D7 -> 0031B760
if (unit) unit->qwUnitFlags |= 0x0000200000000000;   // 005102EB
```

Its authored name says exactly what it does — *cancel the initial-spawn flag* — and the
compiled zone scripts confirm the placement. It is called on the branch taken when a unit is
**not** being restored from the spawn-keep bank, i.e. the fresh-placement path:

```
if (<not restorable>) goto L4;
    g = btlAtelDecideEntryGroupByContinuous();      if (g == -1) goto L3;
    g = btlAtelDecideEntryGroupByPreviousMap();
    if (g >= 0) { btlAtelSetKeepWorkGroup(g, -1); setentrygroup(g); requestreentry(); return; }
L3: goto L5;
L4: btlAtelCanselInitialSpawnFlag();                 // -> minimum distance enforced
L5: ...
```

So the reading is: **the minimum spawn distance applies to a unit that has already been
activated once (bit 49), or that the zone script has explicitly declared not to be an initial
placement (bit 45).** Everything else — a fresh unit at zone arrival — gets `minR = 0.0` and
may be placed on top of the player.

### 2e. Who installs the tunables, and does every zone do it — L-10

`FUN_0023A520` (`0023A520`, 66 B) is the only writer of the whole default set. Its complete
body:

```asm
0023A520  movss xmm0, [00 91 46 EC]        ; 39.0
0023A528  movss xmm1, [00 91 46 F0]        ; 42.0
0023A530  movss [02089360], xmm0           ; g_flAutomaticSpawnMinPlayerDistance = 39.0
0023A538  movss xmm0, [00 91 46 F4]        ; 43.0
0023A540  movss [02089368], xmm0           ; g_flNativeLifecycleRange           = 43.0
0023A548  movss [02089364], xmm1           ; g_flAutomaticSpawnMaxPlayerDistance = 42.0
0023A550  mov   dword ptr [02089358], 0xb4 ; arc = 180
0023A55A  mov   byte  ptr [0208D457], 1    ; attempt limit = 1
0023A561  ret
```

Its only call site is `thunk_FUN_0023a520` (`00510710`), which is **table record 83 of the
`0x30xx` ScriptVM primitive group** — primitive `0x3053`, whose authored name is
**`btlAtelSetupActorStart`**.

The primitive table's records are reached at `01F281D0 + 0x20*i`, indexed by the low byte of
the opcode.

> **Corrected 2026-09-02 (repos-d2, self).** Two errors, both of classes this session has been
> finding in other documents. **(a) The extent is 147 records, not 252.** `01F281D0` is not a table
> base: it is `01F281B0 + 0x20`, the **result-callback column** of ScriptVM command family 3, whose
> record count is the dword at `01F281B0` and is **147** — a bound
> `VMNativeCommandDispatch_Get*Callback` enforces on every access. The 252 came from walking while
> the entries *looked* like code-or-null, which ran 105 records past the end into the abutting
> family 5 and 7 tables. **The extent was inferred from contents when the consumer states it.**
> **(b) The frame is one column off.** Each record is three callbacks — `begin` at `+8`, `poll`
> at `+16`, `result` at `+32` — and every handler named below is a **result** callback, with
> `begin` and `poll` null. **No mapping below changes**: the highest index used here is `0x06C`,
> well inside 147, and all nine were re-verified in the correct frame. See
> [the dispatch table](../01-Script-VM-Native-Bridge/scriptvm-native-dispatch-table.md) §14.

The index-to-opcode mapping is established from the binary and corroborated at eight independent
points, three of them consecutive and in order:

Each cell names the address it belongs to. The **handler** is the function the table record
holds; the **native target** is what that handler tail-calls or wraps, and is a different
function with a different name — they are listed together only to show the hop.

| Primitive | Handler (in the table record) | Native target it reaches | Arity agrees |
|---|---|---|---|
| `0x300B` `btlAtelSetSpawnDistance` | `0050F410` `VM_SpawnSetNativeLifecycleRanges` | `0023A1D0` `Spawn_SetNativeLifecycleRanges` | 3 args, 3 pops |
| `0x301A` `btlAtelDecideEntryPointAuto` | `0050F520` `VM_Spawn_SelectAutomaticEntry` | `00235720` `Spawn_SelectAndPrepareAutomaticEntry` | 0 args, returns |
| `0x3038` `btlAtelSetDecidingEntryPointTimes` | `0050FC00` `VM_Spawn_SetPositionAttemptLimit` | `00239020` `Spawn_SetPositionAttemptLimit` | 1 arg |
| `0x304D` `btlAtelCanselInitialSpawnFlag` | `005102D0` `FUN_005102d0` | *(no callee — sets unit flag bit 45 inline)* | 0 args |
| `0x304E` `btlAtelSetActiveActorMax` | `00510320` `VM_Spawn_SetAutomaticActiveCap` | *(no callee — writes the cap byte inline)* | 1 arg |
| `0x304F` `btlAtelGetActiveActorMax` | `00510360` `FUN_00510360` | *(no callee — reads the cap byte inline)* | 0 args |
| `0x3050` `btlAtelGetActiveActorNow` | `00510390` `VM_Spawn_GetActiveCapTrackedCount` | `00308D90` `Spawn_CountActiveCapTrackedActors` | 0 args |
| `0x3053` `btlAtelSetupActorStart` | `00510710` `thunk_FUN_0023a520` | `0023A520` `FUN_0023a520` | 0 args |
| `0x305B` `btlAtelSetSpawnLimitDegree` | `0050F470` `VM_Spawn_SetCandidateHeadingArcDegrees` | `0023A1F0` `Spawn_SetCandidateHeadingArcDegrees` | 1 arg |
| `0x306C` `btlAtelSetMapJumoKeep` | `005107F0` `VM_SpawnKeep_SetReturnWindow` | `00235340` `SpawnKeep_SetReturnWindow` | 1 arg |

`0x3054 btlAtelSetupActorFinish` and the four other block-end markers (`0x3055`-`0x3058`) all
resolve to `_guard_check_icall` (`0016D6A0`), a 3-byte `ret 0` — they are **markers with no
native effect**.

**The measured answer.** The corpus is the 1,115 US-locale `.ebp` scripts in
`FFXII_TZA.vbf` (0 MD5 mismatches on extraction); 828 of them carry a script section and
decompiled cleanly with `ff12-script` v3.00 (602 `plan_map` zone scripts, 226 `event`
scripts). ~~The remaining 287 containers hold no `0x8000000B` script section.~~ **Corrected
2026-09-12 (FABLE):** every one of the 1,114 containers carries a slot-000 section beginning
`0x8000000B` (read from all 1,114 files; [the EBP container page](../25-EBP-Script-Container/Container/ebp2-container.md) §5 counts the same). The 287 are the one
non-container file plus the **286 containers with no slot 002** (167 `plan_map`, 119 `event`): the
carving driver took slot 002's offset (`+0x18`) as the script's end, so an absent slot 002 gave an
empty blob and a "bad magic" — a driver artefact, not a corpus property. **Re-carved 2026-09-12 (FABLE):** the 286 were cut to the next present offset (or EOF) and
decompiled — 286 of 286, no failures — so the counts below give both populations: the original
828 and the **whole corpus of 1,114**.

| Primitive | Files (828) | Calls (828) | Files (1,114) | Calls (1,114) |
|---|---:|---:|---:|---:|
| `btlAtelSetupActorStart` | **406** | 406 (exactly once per file) | **515** | 515 (once per file) |
| `btlAtelSetupActorFinish` | 0 | 0 | 0 | 0 |
| `btlAtelSetUnit` (an enemy definition) | 400 | 5,130 | 502 | 6,746 |
| `btlAtelDecideEntryPointAuto` (the spawn selector) | 172 | 7,696 | 258 | 11,250 |
| `btlAtelCanselInitialSpawnFlag` | 167 | 8,119 | 253 | 11,571 |
| `btlAtelSetActiveActorMax` | 167 | 167 | 234 | 234 |
| `btlAtelSetDecidingEntryPointTimes` | 146 | 146 | 210 | 210 |
| `btlAtelSetSpawnDistance` | 38 | 38 | 70 | 70 |
| `btlAtelSetSpawnLimitDegree` | 12 | 12 | 12 | 12 |
| `btlAtelSetMapJumoKeep` | 0 | 0 | **0** | **0** |

The set relations are the answer:

- **Every one of the 400 scripts that defines a battle unit calls `btlAtelSetupActorStart`.**
  Zero exceptions — and over the whole corpus, **every one of the 502**.
- **Every one of the 172 scripts that runs the automatic spawn selector calls it.** Zero
  exceptions — **every one of the 258** over the whole corpus.
- Six scripts call it and define no units — they install defaults and spawn nothing (13 over the
  whole corpus).
- 422 of the 828 scripts never call it, and none of those defines a unit or spawns (599 of 1,114).

So `FUN_0023A520` is **not** invoked by every zone — but it is invoked by every zone that can
place anything, and the reset always comes first. In the zones that override, the order in the
compiled script is unambiguous:

```
actor setup(0) { function battle() {
    CALLPOPA  btlAtelSetupActorStart      // install 39 / 42 / 43 / 180 / 1
    PUSHII 0x5  PUSHII 0xc  PUSHII 0x2b
    CALLPOPA  btlAtelSetSpawnDistance     // -> min 5, max 12, retire 43
    PUSHII 0x4
    CALLPOPA  btlAtelSetActiveActorMax    // -> cap 4
    ...
} }
```

**The all-zero state is therefore unreachable in the shipped corpus — and it would be
self-announcing if it ever occurred.** With the globals at their BSS value of zero,
`Spawn_TrySelectCandidatePosition` returns `0` on its first line (`max - min == 0.0`), so no
automatic spawn can ever succeed; and `g_flNativeLifecycleRange² = 0` makes the mode-1 range
retire fire for every spawn-backed unit on its first lifecycle frame, because `d² < 0` is
never true. A zone in that state would contain no wandering monsters at all.

### 2f. What the zones actually author

Measured over the same 828 files, with the whole-corpus figures added 2026-09-12 in brackets.
This is the population that matters for a modder: the 39/42/43/180/1 defaults are what most zones
keep, but the zones that override do so hard.

**`btlAtelSetSpawnDistance(min, max, retire)` — 38 zones [70]:** the 32 added by the re-carve
are the `bts_*` battle-test zones and `tst_j`, every one passing **`(0, 25, 30)`** through three
file variables rather than immediates — a zero minimum, the only one in the game, in test zones.

| min | max | retire | zones |
|---:|---:|---:|---:|
| 5 | 12 | 43 | 8 |
| 8 | 12 | 43 | 7 |
| 6 | 20 | 43 | 6 |
| 4 | 12 | 43 | 5 |
| 50 | 60 | 70 | 3 |
| 10 | 90 | 100 | 2 |
| 6 | 8 | 43 | 2 |
| 4 | 24 | 43 | 2 |
| 39 | 100 | 110 | 2 |
| 12 | 16 | 43 | 1 |

Every one of the ten distinct triples keeps `retire > max`, preserving the hysteresis the
default set builds in at 42 → 43 [so does the eleventh, `(0, 25, 30)`]. Note that 26 of the 38 keep
the retire range at exactly the default 43 while shrinking the ring to a quarter of its default
size [31 of 70].

**`btlAtelSetSpawnLimitDegree` — 12 zones:** `180` ×9 (a redundant restatement of the
default), **`360` ×2**, `270` ×1. The two 360° zones are the only places in the shipped game
where a spawn may be placed behind the party leader.

**`btlAtelSetDecidingEntryPointTimes` — 146 zones, all set `3`** [210 of 515, still all `3`]. Never any other value. So in
146 of the 406 spawn-capable zones the placement loop gets three attempts, not the default one.

**`btlAtelSetActiveActorMax` — 167 zones:** `6` ×100, `7` ×22, `5` ×18, `4` ×12, `8` ×9,
`3` ×4, `9` ×1, `2` ×1 [234 zones: `6` ×147, `7` ×30, `5` ×27, `4` ×12, `8` ×11, `3` ×5, `2` ×1, `9` ×1]. The engine default of 28 is never authored.

## 3. Key addresses

| Address | Working name | Body | Role |
|---|---|---:|---|
| `00234AF0` | `Spawn_TrySelectCandidatePosition` | 584 B | generates the candidate; forwards the unwritten Y |
| `00319390` | `FUN_00319390` | 139 B | polar offset; writes `[0]` and `[2]` only — **never `[1]`** |
| `002374E0` | `FieldRegion_ContainsWorldPosition` | 334 B | area-mode accept test; XZ only |
| `00325EA0` | `Vector3_RotateTranslatedXZOffsetByEncodedAngle` | 152 B | its transform; reads `[rcx]` and `[rcx+8]` only |
| `00235720` | `Spawn_SelectAndPrepareAutomaticEntry` | 841 B | the sole reader of unit flag bits 45/49; banks the candidate |
| `0023A410` | `SpawnUnit_FinalizeSpawnEntryActivation` | 270 B | **the height source**: ground probe + offset, then place |
| `003208C0` | `FUN_003208c0` | 119 B | ground probe; `0.0` on miss; return value discarded by its caller |
| `0026E3C0` | `FUN_0026e3c0` | 313 B | the field surface query the probe wraps — cell (`00233050`), cell height (`00231890`), kind-6 volume escape (`00232490`), segment refinement (`00230B60`); returns the cell index (read 2026-09-12) |
| `00300310` | `BattleUnit_PublishLocomotionPosition` | 214 B | the placement call that consumes `BKEI + 0x60` |
| `00233AD0` | `BattleUnit_ActivateAppliedDefinitionRuntime` | 316 B | sets flag bit 49; clears bit 26; calls the definition applier |
| `00239E10` | `FUN_00239e10` | 594 B | applies the definition; sole writer of `+0x1F6` and `+0x188` |
| `005102D0` | `FUN_005102d0` | 35 B | primitive `0x304D` `btlAtelCanselInitialSpawnFlag`; sets bit 45 |
| `0031B760` | `ActorWork_GetBattleUnit` | 13 B | null-guard wrapper |
| `00263E30` | `ActorWork_GetBattleUnitRaw` | 5 B | `return aw->field_0x30` |
| `0023A520` | `FUN_0023a520` | 66 B | primitive `0x3053` `btlAtelSetupActorStart`: installs 39/42/43/180/1 |
| `00510710` | `thunk_FUN_0023a520` | 5 B | its only call site; table record 83 |
| `0023A1D0` | `Spawn_SetNativeLifecycleRanges` | 25 B | `(retire, max, min)` in `xmm0..xmm2` |
| `0050F410` | `VM_SpawnSetNativeLifecycleRanges` | 78 B | primitive `0x300B`; three pops, reversed onto the native order |
| `0023A1F0` | `Spawn_SetCandidateHeadingArcDegrees` | 11 B | truncates a float to the arc int |
| `0050F470` | `VM_Spawn_SetCandidateHeadingArcDegrees` | 21 B | primitive `0x305B` |
| `00239020` | `Spawn_SetPositionAttemptLimit` | 19 B | writes the attempt-limit byte |
| `0050FC00` | `VM_Spawn_SetPositionAttemptLimit` | 23 B | primitive `0x3038` |
| `0050F520` | `VM_Spawn_SelectAutomaticEntry` | 32 B | primitive `0x301A`; **the only caller of `00235720`** |
| `00510320` | `VM_Spawn_SetAutomaticActiveCap` | 23 B | primitive `0x304E` |
| `00510360` | `FUN_00510360` | 12 B | primitive `0x304F`, the matching getter |
| `00510390` | `VM_Spawn_GetActiveCapTrackedCount` | 29 B | primitive `0x3050` |
| `005107F0` | `VM_SpawnKeep_SetReturnWindow` | 23 B | primitive `0x306C` `btlAtelSetMapJumoKeep`; unused by the corpus |
| `0016D6A0` | `_guard_check_icall` | 3 B | `ret 0`; the handler every no-op marker primitive points at |
| `00267DB0` | `VMValueStack_PopFloat32Coerce` (GFZ: `VMValueStack_PopNumericDiscard`, wrong - see BQ-8) | 84 B | the VM argument pop — decrements the count, so LIFO |
| `00236A60` | `BattleUnit_ResetStateForReuse` | 452 B | masks `qwUnitFlags` with `0xFFFF7FFDFFE7FFFD` — **clears exactly bits 1, 19, 20, 33, 47** and preserves the other 59, including 45 and 49 (§11) |
| `002355A0` | `Spawn_PrepareRandomCandidateForCurrentEntry` | 376 B | another `0x250`-stride keep-bank indexer |
| `002354F0` | `Spawn_SelectPreviousMapEntry` | 166 B | same |
| `00235360` | `Spawn_SelectContinuousEntry` | 390 B | same |
| `002395A0` | `SpawnKeep_InitializeEntriesFromDefinitionTable` | 268 B | same |
| `00239840` | `SpawnUnit_BindEntryAndMarkCapTracked` | 168 B | same |
| `002D81D0` | `FUN_002d81d0` | 478 B | the discriminated false positive — a 14-bit field packer, not a unit flag |

### Data addresses cited by this document

| Address | Name | Kind | Contents |
|---|---|---|---|
| `01F281B0` | ScriptVM command table, **family 3** | `.data` array | record count `147` in the first dword, then 147 × `0x20` records of `begin`/`poll`/`result` |
| `01F281D0` | family 3's **result-callback column** | `.data` | `01F281B0 + 0x20`; the `0x30xx` handlers this document names |
| `009146EC` | — | `.rdata` float | `39.0` — the installed minimum spawn distance |
| `009146F0` | — | `.rdata` float | `42.0` — the installed maximum spawn distance |
| `009146F4` | — | `.rdata` float | `43.0` — the installed retire range |
| `01F004E0` | sine table | `.data` array | 32,768 floats, `table[i] = sin(2πi/32768)`; `table[0x2000] = 1.0` |
| `00D10820` | — | `.rdata` float | `+32768.0` — sine-table index scale |
| `00D10828` | — | `.rdata` float | `-32768.0` — the negated scale used for the cosine index |
| `0208E690` | `g_pBtlKeepCharWork1` | `.data` pointer | live keep bank; `0x9400` B = **64 entries of `0x250`**. Identified by this pointer, **not** by the stride — §11 found a third of the `0x250` stride sites in an unrelated Presentation structure |
| `0208E698` | `g_pBtlKeepCharWork2` | `.data` pointer | history keep bank, same shape |
| `02089358` | `g_nSpawnCandidateHeadingArcDegrees` | `.data` BSS i32 | `180` after the reset |
| `02089360` | `g_flAutomaticSpawnMinPlayerDistance` | `.data` BSS f32 | `39.0` after the reset |
| `02089364` | `g_flAutomaticSpawnMaxPlayerDistance` | `.data` BSS f32 | `42.0` after the reset |
| `02089368` | `g_flNativeLifecycleRange` | `.data` BSS f32 | `43.0` after the reset |
| `0208D457` | `g_bSpawnPositionAttemptLimit` | `.data` BSS byte — **u8 storage, consumed as signed `i8`** | `1` after the reset. The setter `00239020` clamps only below 1 (`cmp ecx, 1` / `cmovl`) and stores `CL`, so an argument of 128–255 is stored as that byte and 256 as 0; the loop in `00235720` tests it signed (`test dl, dl` / `jle` at `00235929`, `movsx` at `00235964` and `0023597A`), so a byte ≥ `0x80` runs **zero** candidate attempts. Every shipped call passes `3` (the census in §2 of this page), so the signed path is not reached by authored data — see [spawn placement and retirement](spawn-placement-and-retirement.md) §11 |

All function rows resolve in the current parent with the extents shown
(`DumpFullCoverageGraph`, 2026-09-02, 38,161 functions).

## 4. Data structures and formulas

```
BattleUnit
  +0x0000  u64   qwUnitFlags
                   bit  2 (0x00000004)  unit is active
                   bit  3 (0x00000008)  applied-definition done (one-shot latch)
                   bit 26 (0x04000000)  a spawn entry point has been prepared
                   bit 45 (0x0000200000000000)  script: not an initial placement
                   bit 49 (0x0002000000000000)  has been activated at least once
  +0x0188  f32   flSpawnVerticalOffset      added to the probed ground height
  +0x01F6  u8    bPlacementHeightMode       bit 3 (value 8) -> run the ground probe
  +0x0698  ptr   pBkbi                      [+5] == 1  <=> spawn-backed
  +0x06A0  ptr   pBkei                      the spawn-keep entry
  +0x0E68  ptr   pAppliedDefinition         [+0x18] holds the placement-mode flags

Applied definition record
  +0x18    u8    flags   bit 4 (0x10) -> height mode 8 (ground probe)
                         bit 5 (0x20) -> height mode 2 rather than 1, when bit 4 is clear
                         bit 6 (0x40) -> adds 4 to the height mode

BattleKeepEntry (BKEI) - stride 0x250 = 592 B, 64 per bank
  +0x00    u32   lifecycleFlags   bit0 RANGE_REENTRY_PENDING, bit1 ACTIVATION_COMMITTED
  +0x08    u16   wDeathCount      +0x0A u16 wDeathLimit
  +0x0C    u32   dwLastDeathTick  +0x10 u16 wRespawnCooldownTicks
  +0x19..+0x41   enmity decay timer + 40 per-combatant enmity bytes
  +0x50    f32[4] live persisted world position
  +0x60    f32   candidateX   +0x64 f32 candidateY   +0x68 f32 candidateZ
```

**Polar candidate construction** — the exact arithmetic of `FUN_00319390`, with
`local = (0, ?, r)` and `base` the party leader's position:

```c
t     = theta / 6.2831855f;                       // 01CEBC78
i_sin = ((int)(t *  32768.0f)) & 0x7FFF;          // 00D10820
i_cos = (0x2000 - (int)(t * -32768.0f)) & 0x7FFF; // 00D10828, == (0x2000 + i_sin) & 0x7FFF
S = sinTable[i_sin];   C = sinTable[i_cos];       // 01F004E0

out.x = base.x + (local.x * C + local.z * S);     // = base.x + r*sin(theta)
out.z = base.z + (local.z * C - local.x * S);     // = base.z + r*cos(theta)
out.y = /* NOT WRITTEN - the caller's stack slot is passed through untouched */
```

**Height resolution at activation** — the whole of it:

```c
if (unit->bPlacementHeightMode & 8) {             // 0023A49E
    float probe[4] = { bkei->candidateX, 1.0f, bkei->candidateZ, 1.0f };
    short r = FieldSurfaceQuery(g_field, probe);  // 0026E3C0 via 003208C0
    bkei->candidateY = ((short)r != -1) ? probe[1] : 0.0f;   // failure -> world zero
    bkei->candidateY += unit->flSpawnVerticalOffset;         // 0023A4D5
}
BattleUnit_PublishLocomotionPosition(unit, &bkei->candidateX, 0, 1);   // 0023A4F1
```

**Height mode selection**, evaluated once per activation in `FUN_00239E10`:

```c
if (unit && unit->pBkbi && unit->pBkbi[5] != 1)        // not spawn-backed
    mode = esi;                                        // 1, 2 or 3 - never 8   # <- corrected 2026-10-02, OPUS - esi is 1 here (00239E33); and the test above is pBkbi[5] == 0 (00239FA3 test eax, eax / jne), with a null unit or pBkbi taking the definition path (00239F91, 00239F9D)
else {
    d = unit->pAppliedDefinition[0x18];
    base = (d & 0x10) ? 8 : ((d & 0x20) ? 2 : 1);
    mode = (d & 0x40) ? (base | 4) : base;              // -> 1,2,5,6,8,12
}
unit->bPlacementHeightMode = (u8)mode;
```

**The minimum-distance gate**, the sole reader of bits 45 and 49:

```c
minR = (unit->qwUnitFlags & 0x0002200000000000) ? g_flAutomaticSpawnMinPlayerDistance : 0.0f;
//                          ^ bit 49 (activated once) | bit 45 (script: not an initial placement)
```

**The default set installed by `btlAtelSetupActorStart`:**

```c
g_flAutomaticSpawnMinPlayerDistance = 39.0f;   // [009146EC]
g_flAutomaticSpawnMaxPlayerDistance = 42.0f;   // [009146F0]
g_flNativeLifecycleRange            = 43.0f;   // [009146F4]
g_nSpawnCandidateHeadingArcDegrees  = 180;     // 0xB4
g_bSpawnPositionAttemptLimit        = 1;
```

**Script argument order.** `FUN_00267DB0` decrements the VM argument count before reading, so
pops are last-in-first-out. `VM_SpawnSetNativeLifecycleRanges` pops three values into
`xmm0, xmm1, xmm2` in that order and tail-jumps to `Spawn_SetNativeLifecycleRanges`, which
stores `xmm0 → retire`, `xmm1 → max`, `xmm2 → min`. Therefore:

```
btlAtelSetSpawnDistance(a, b, c)  =>  min = a,  max = b,  retireRange = c
```

which is corroborated by every one of the ten authored triples: all ten satisfy
`min < max < retire` under this mapping and all ten are incoherent under the reverse.

**Zero-tunable consequences**, if the reset were ever skipped:

```
max - min == 0.0                 -> Spawn_TrySelectCandidatePosition returns 0 immediately
g_flNativeLifecycleRange^2 == 0  -> mode-1 retire fires always, since d^2 < 0 is never true
```

## 5. Call chain

```
zone script, actor `setup`, function `battle()`
  -> btlAtelSetupActorStart (0x3053)
       -> thunk_FUN_0023a520 (00510710) -> FUN_0023A520 (0023A520)    [AUTHORITY 01 -> 05]
          installs 39 / 42 / 43 / 180 / 1
  -> btlAtelSetSpawnDistance / SetSpawnLimitDegree / SetDecidingEntryPointTimes /
     SetActiveActorMax                                                 optional overrides
  -> btlAtelCanselInitialSpawnFlag (0x304D) -> FUN_005102D0
       -> ActorWork_GetBattleUnit (0031B760) -> ActorWork_GetBattleUnitRaw (00263E30)
       -> unit->qwUnitFlags |= bit 45

placement
  -> btlAtelDecideEntryPointAuto (0x301A) -> VM_Spawn_SelectAutomaticEntry (0050F520)
     -> Spawn_SelectAndPrepareAutomaticEntry (00235720)                THIS SYSTEM
        -> reads qwUnitFlags bits 45|49 -> minR                        (the only reader)
        -> Spawn_TrySelectCandidatePosition (00234AF0)
           -> RNG_SharedGameplayLCG_NextU32 (00328370) x2              [RNG]
           -> FUN_00319390            X and Z only; Y left as stack residue
           -> FieldRegion_ContainsWorldPosition (002374E0)             [WorldAreaField]
              -> Vector3_RotateTranslatedXZOffsetByEncodedAngle (00325EA0)   XZ only
        -> banks the candidate at BKEI +0x50 and +0x60; sets qwUnitFlags bit 26

activation
  -> BattleUnit_ActivateAppliedDefinitionRuntime (00233AD0)            [ActorEntity]
     -> FUN_00239E10 (00239E10)     writes BattleUnit +0x1F6 and +0x188 from the definition
     -> unit->qwUnitFlags |= bit 49
  -> SpawnUnit_FinalizeSpawnEntryActivation (0023A410)                 THIS SYSTEM
     -> if (+0x1F6 & 8): FUN_003208C0 (003208C0) -> FUN_0026E3C0 (0026E3C0)  [Movement]
     -> BKEI.candidateY = ground + BattleUnit[+0x188]
     -> BattleUnit_PublishLocomotionPosition (00300310)                [Movement]
```

**Upstream (who causes this):** the zone's authored `setup`/`battle()` script, through the
`btlAtel` ScriptVM primitive group. Nothing in this system starts on its own — the tunables,
the spawn attempt and the initial-spawn override are all authored calls.

**Downstream (what this causes):** the world position an actor is placed at, and the persisted
candidate carried in the spawn-keep bank.

**Do not confuse with:**

- **The height probe is not the candidate filter.** `FieldRegion_ContainsWorldPosition` decides
  whether the *XZ* point is inside the authored region; the ground probe decides the *Y*, later,
  in a different function, and its failure is not checked.
- **Bit 26 (`0x04000000`) is not one of the minimum-distance bits.** It is the
  "entry point prepared" marker, set by `00235720` and cleared by `00233AD0`.
- **`btlAtelSetupActorStart` is not a per-zone initialiser** in the sense of running once per
  map load by the engine. It is an authored primitive; a script that never calls it leaves the
  globals at their previous values, which at process start are zero.
- **`btlAtelSetupActorFinish` does nothing.** It resolves to `_guard_check_icall`, and no
  shipped script calls it.

## 6. Modding notes

- **`009146EC`–`009146F4` is the one place where the default ring changes for every zone at once.**
  Those twelve bytes hold `39.0`, `42.0` and `43.0`, and every zone that can spawn anything copies
  them at battle setup before deciding whether to override. **Editing a zone script changes one
  zone; editing these three floats changes the default every zone starts from.** *(Added by the
  2026-09-07 falsification pass — the mechanism was already in §2e and the consequence was never
  stated.)*

- **Best intervention point for spawn geometry:** `btlAtelSetSpawnDistance` in the zone's
  `setup` actor, immediately after `btlAtelSetupActorStart`. Calling it *before* the reset is
  useless — the reset overwrites all three values.
- **The order in `battle()` is load-bearing.** `btlAtelSetupActorStart` must come first. Every
  one of the 406 shipped scripts that calls it calls it exactly once, first.
- **Keep `retire > max`.** All 38 authored triples do. Setting `retire <= max` makes a monster
  spawn and retire on the same frame; setting `min == max` disables automatic spawning outright,
  because `Spawn_TrySelectCandidatePosition` returns 0 when `max - min == 0.0`.
- **To stop monsters materialising on top of the player at zone entry**, call
  `btlAtelCanselInitialSpawnFlag` on the fresh-placement branch, as the 167 shipped zones that
  care already do. There is no global switch — it is per unit, and it is the *only* way to get
  the minimum enforced before a unit's first activation.
- **The vertical offset and the height mode are authored per enemy**, in definition byte
  `+0x18` bit 4 and the definition's offset field. A monster that sinks into or floats above
  the floor is an authored-definition problem, not a placement one.
- **Regenerates itself:** `BattleUnit + 0x1F6` and `+0x188` are rewritten from the definition
  on every activation pass — do not patch them at runtime, patch the definition.
- **Breaks if:** you clear `qwUnitFlags` bit 49 to force the "free placement" behaviour back.
  Nothing in the engine clears it, including `BattleUnit_ResetStateForReuse`, so a mod that
  clears it is introducing a state the engine never produces.
- **Multiplayer / XIIOnline:** the placement Y comes from a *local* terrain query and the
  candidate Y is uninitialised stack, so **two clients running the same spawn will not agree on
  the height** even given an identical XZ candidate — the XZ can be made deterministic by
  synchronising the shared LCG, the Y cannot. Any shared spawn model must transmit the resolved
  position after `SpawnUnit_FinalizeSpawnEntryActivation`, not the candidate before it. Note
  also that bit 49 is per-client activation history, so two clients can legitimately disagree
  about whether the minimum distance applies to the same unit.
- **Mod compatibility:** the `btlAtel` primitives are the authored surface other mods use.
  Changing `plan_map/<map>/global/<map>.ebp` collides with any mod that edits the same zone
  script; changing the native defaults in `FUN_0023A520` changes only the 368 zones that do not
  override, and none of the 38 that do.

## 7. What is not known

- [x] ~~**PROPOSED-reposd2-1.** What definition byte `+0x18` bits 5 and 6 select.~~ **ANSWERED
      2026-09-12 (FABLE) as a whole-image negative.** A displacement census of `+0x1F6` over all
      of `.text` finds exactly one writer of the unit byte, `00239E10` (`00239FD4`; called only by
      `BattleUnit_ActivateAppliedDefinitionRuntime`), and exactly one reader,
      `SpawnUnit_FinalizeSpawnEntryActivation` (`0023A49E`, `test … 8`) — the other two hits are a
      word read on a Presentation record (`00454A2C`, floats at `+0x1EC` / `+0x1F0` beside it) and
      the DirectInput mouse state. The writer's values (`00239E33`, `00239E70`, `00239FAB`–`00239FD4`):
      a party unit gets **1**; an enemy gets **8** when the definition's `+0x18` bit 4 is set (the
      `ebp = 8` seeded at `00239E70` survives the skipped bit-5 computation), else **1** or **2** by
      bit 5, and **`| 4`** by bit 6 in either case. So **bit 4 is the probe bit** the reader tests,
      and the values 1, 2, 5, 6, 12 that bits 5 and 6 produce are consumed by nothing in the
      image — dead in the shipped executable, whatever they meant on the PS2.
- [x] **UQ-100.** **PROPOSED-reposd2-2.** What the uninitialised candidate Y actually contains in practice *(closed — the register row is WITHDRAWN.)*
      for a unit whose definition does not set the probe bit. It is stale stack from an earlier
      call at the same depth; establishing the value requires runtime evidence (tier 10), and
      whether any shipped enemy definition leaves the probe bit clear is unmeasured — the
      definition records were not extracted for this block.
      ***NARROWED 2026-09-18 (FABLE), DATA: the shipped definitions leave the probe bit clear far more often than they set it, so the uninitialised Y is the common path, not the exception.** Reading every `.ard` in the archive (332 files: 166 areas under `in` and the same 166 under `ch`, byte-identical pair for pair), the slot-0 `st2e` table, the 84-byte class row the definition page names as the unit's definition, holds 954 rows per locale set; byte `+0x18` bit 4 is **set in 59 and clear in 895**. (The slot-2 88-byte rows, 1,146 per set, carry it set in 8 and clear in 1,138.) So for 895 of 954 definitions the activation reader sees no probe bit and the area-mode candidate's Y is whatever `[rsp+0x54]` held, exactly the case the box asks about; what that stale word holds in practice remains runtime evidence (tier 10) and stays open. DATA from the archive.*
- [x] ~~**PROPOSED-reposd2-3.** Whether `FUN_0026E3C0` (313 B, Movement) queries collision
      geometry or a height field, and what its `short` return identifies.~~ **ANSWERED 2026-09-12
      (FABLE): the navigation dataset, and the cell index.** Read whole (`0026E3C0`–`0026E4F7`):
      `00231900(field, probe, 1)` resolves the probe's **cell** through the same `00233050` the
      placement writer uses ([the movement body page](../06-Movement-And-Navigation/the-movement-body-pool-and-the-separation-pass.md) §"the cell words") and returns its index as a `short`,
      **−1 outside every cell, which the query returns at once** (`0026E3F1`); `00231890(field,
      probe, cell)` gives the cell's **height**, written into the probe's Y (`0026E41E`) — the height
      the same page reads for a body's `+0xC0`. The query then raises a copy of the point by `1.0`
      (`01CEBBA8`) up to thirty times while `00232490(field, point, 1)` — a `{cell, kind 6, flags}`
      request to the dataset query `0022F830` — reports the point inside a kind-6 volume
      (`0026E460`–`0026E486`); when it clears, `00230B60(field, out, raised, original, 0xFFFF, 0)`
      runs the segment from the raised point back down and, on a hit, replaces Y with the hit's
      (`0026E4B8`–`0026E4ED`). So it is a **height-field walk over the field's cell dataset with a
      kind-6 volume escape**, not a query of collision primitives, and the `short` is the cell.
- [x] ~~**PROPOSED-reposd2-4.** The remaining 242 records of the `0x30xx` primitive table.~~
      **ANSWERED 2026-09-12 (FABLE), all 147 checked — and the count corrected.** The `0x30xx`
      table has **147** records, not 252: the dword at `01F281B0` is the count, the records run
      from `01F281B8` at `0x20` each with the callbacks at `+0x00` begin / `+0x08` poll / `+0x18`
      result ([the dispatch-table page](../01-Script-VM-Native-Bridge/scriptvm-native-dispatch-table.md)), and `01F281D0 + 0x20 × i` is record *i*'s **result** callback — the
      column this page read as "the handler at `+0x00`". The 252 came from reading past the
      family boundary at `01F29418`: 147 (family 3) + 1 (family 5) + 104 (family 7). Read against
      [the verb table](../01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-verb-table.tsv): **every family-3 record's result callback equals the catalogue row's `result`
      — 143 non-null and the four null ones (`0x3020` *btlAtelRemoveAllEquip*, `0x3051` / `0x3052`
      *btlAtelOpenTreasureStart* / *Finish*, `0x3092`) where the catalogue records none**; the
      "handlers" this page names for its ten primitives are therefore their result callbacks, and
      the 30 non-null pointers between records 148 and 245 belong to family 7.
- [x] ~~**PROPOSED-reposd2-5.** `btlAtelSetMapJumoKeep` (`0x306C`, the return-window setter) is
      called by **no** script in the 828-file corpus~~ — **and by none of the 286 re-carved either
      (2026-09-12, FABLE): 0 of all 1,114 US scripts**, so the 300-second window is always the
      native default in the shipped US game. Non-US-locale scripts remain unmeasured (the corpus
      extracted is the `us` tree).
- [x] ~~**PROPOSED-reposd2-6.** The 287 extracted `.ebp` containers whose first section is not a
      `0x8000000B` script. What they hold, and whether any carries `btlAtel` calls in another
      form.~~ **ANSWERED 2026-09-12 (FABLE) as a correction** (§"The measured answer"): their first
      section *is* a `0x8000000B` script; they were skipped because the carving driver ended the
      script at slot 002's offset and 286 of them have no slot 002 (the 287th is the non-container
      file). Their `btlAtel` calls are in the ordinary form and simply unmeasured. **Follow-up
      (data):** re-carve the 286 to the next present offset and re-run the per-primitive census —
      which can move PROPOSED-reposd2-5's "no script calls `btlAtelSetMapJumoKeep`" and the other
      828-file counts.

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| `FUN_00319390` writes only `[0]` and `[2]` | complete 139-byte body; the two `movss` stores at `00319411` / `00319415` and the `ret` at `0031941A` | 1 |
| The Y slot is never written by the caller either | complete body of `00234AF0` with the frame mapped: `mov rax,rsp` / 5 pushes / `sub rsp,0x100`, so `rsp+0x54` is `entry_rsp-0xD4`; no store in the body reaches it and every callee frame lies below `rsp` | 1 |
| The stale Y is forwarded to the caller | `movss xmm1,[rsp+0x54]` at `00234CDD` and `movss [rbx+4],xmm1` at `00234CF2` | 1 |
| The region test ignores Y | complete bodies of `002374E0` and `00325EA0`; the transform reads `[rcx]` and `[rcx+8]` only | 1 |
| The height comes from a ground probe at activation | complete body of `0023A410`: gate at `0023A49E`, probe call at `0023A4BC` with `lea r8,[rax+0x64]`, offset add at `0023A4D5`, placement at `0023A4F1` | 1 |
| The probe yields `0.0` when no surface is found | complete body of `003208C0`: `probe[1]=1.0f`, `cmp ecx,-1`, `xorps xmm0,xmm0` at `00320915`, store at `0032091A` | 1 |
| Its caller discards the success flag | `0023A4BC` is followed by a reload of `unit[0x6A0]`, not a test of `eax` | 1 |
| The probe gate is definition bit 4 | `mov ebp,8` at `00239E70` (unconditional, rbp callee-saved across the intervening calls) and the `test dl,0x10` / `jne` at `00239FB6` that preserves it | 1 |
| `+0x1F6` has one writer and one reader | exhaustive operand census over all 38,161 bodies for any memory operand whose byte range covers offset `0x1F6`: 310 hits, of which exactly one writes `[reg+0x1F6]` (`00239FD4`) and one reads it (`0023A49E`); the rest are `+0x1F4` accesses on other structures | 1 |
| The mask is bits 45 and 49, not 49 and 53 | the `movabs` bytes `49 ba 00 00 00 00 00 20 02 00` at `0023581D` → `0x0002200000000000`; nibble 12 = 2 → bit 49, nibble 11 = 2 → bit 45. `bit49\|bit53` is `0x0022000000000000` and appears nowhere | 1 |
| Bit 49 has exactly one writer | census of every 64-bit immediate reaching a memory `or`/`and`/`bts` across all bodies, plus every `bt*` with immediate 45/49 (zero of those exist): one site, `00233B8C` | 1 |
| Bit 45 has exactly one writer | same census: one site, `005102EB`, in the primitive-`0x304D` handler | 1 |
| Neither bit is cleared | same census in the clear direction; the only `and`-mask omitting either is `002D82DD`, which clears the contiguous 14-bit field bits 37-50 and is immediately followed by `shl rax,0x25` / `or [rsi],rax` at `002D82FB` — a field packer, not a flag | 1 |
| `BattleUnit_ResetStateForReuse` preserves them | `movabs rax,0xFFFF7FFDFFE7FFFD` at `00236A9C`, `and qword ptr [rdi],rax` at `00236AB1`; complement `0x0000800200180002` = bits 1, 19, 20, 33, 47 | 1 |
| Bit 49 is set on the once-per-unit init path | complete body of `00233AD0`: `test byte [rbx],8` / `jne` return at `00233B3A`, `or dword [rbx],8` at `00233B4B`, straight line (only a `cmov`, no branch) to `00233B8C` | 1 |
| `0031B760` is `aw ? aw->[0x30] : NULL` | complete 13-byte body, tail `jmp 0x263e30`; `00263E30` is `mov rax,[rcx+0x30]; ret` | 1 |
| `FUN_0023A520` installs 39/42/43/180/1 | complete 66-byte body with each RIP target resolved: `[009146EC]=39.0`, `[009146F0]=42.0`, `[009146F4]=43.0` read from the PE image; `mov dword [02089358],0xB4`; `mov byte [0208D457],1` | 1 |
| Its only call site is the `0x3053` thunk | Ghidra's graph reports zero callers for `0023A520`; the independent capstone census finds the single `jmp` at `00510710`. **Two instruments disagreed; the graph is wrong because thunks are sinks in it.** | 1 + 11 |
| `00510710` is table record 83 of the `0x30xx` group | the record at `01F281D0 + 83*0x20 = 01F28C30` holds `00510710`; ~~the table is 252 records of `0x20` with the handler at `+0x00`~~ **corrected 2026-09-12:** 147 records from `01F281B8`, `01F281D0` being the result-callback column (`+0x18`); 252 spans families 3, 5 and 7 | 1 |
| The table index is the opcode low byte | eight independent hits at exactly the right index, three of them consecutive and in native-address order (`0x304E/0x304F/0x3050` → `00510320/00510360/00510390`), plus arity agreement between the catalog's parameter counts and the native setters' arities | 1 + 9 |
| Primitive names | `ff12-script` v3.00 `CScriptContainerInitializers.cpp` catalog — authored-schema evidence, cited as the *name* for an already-exact native mapping, never as its source | 9 |
| `0x3054`-`0x3058` are no-op markers | their table records all hold `0016D6A0`, whose complete 3-byte body is `ret 0` | 1 |
| VM argument pops are LIFO | complete body of `00267DB0`: `mov eax,[rcx]` / `dec eax` / `mov [rcx],eax` before the indexed read | 1 |
| `btlAtelSetSpawnDistance(a,b,c)` = (min, max, retire) | pop order in `0050F410` into `xmm0..xmm2`, then `0023A1D0` storing `xmm2→02089360`, `xmm1→02089364`, `xmm0→02089368`; corroborated by all ten authored triples satisfying `min<max<retire` and none doing so reversed | 1 + 9 |
| Corpus counts and set relations | 1,115 US `.ebp` extracted from `FFXII_TZA.vbf` with 0 MD5 mismatches; 828 decompiled by `ff12-script` v3.00, 0 failures; `comm` over the per-primitive file sets. **Corrected 2026-09-12:** the 287 not decompiled are 286 containers without slot 002 (the driver's end offset) plus the non-container; all 1,114 carry a script | 9 |
| Zero radii make spawning impossible | first branch of `00234AF0`: `subss xmm8,xmm7` / `ucomiss` / `jp`+`jne` → `return 0` when `max-min == 0.0` | 1 |
| Zero retire range retires everything | `002350C0` mode 1 keeps a unit only when `d² < thresh`; with `thresh = 0` that is never true | 1 |
| The keep-entry stride is `0x250`, not `0x80` | sixteen distinct Spawn/SpawnKeep/SpawnEntry functions pair `imul <reg>, <idx>, 0x250` with `add <reg>, [0208E690]`; `0x9400 / 0x250 = 64` exactly | 1 |

**Superseded readings.**

### Correction 1 — the flag bits are 45 and 49, not 49 and 53

**Was believed.** [`spawn-placement-and-retirement.md`](spawn-placement-and-retirement.md) §2,
§6 and §7 (L-9): *"flag bit 49 or bit 53 (`0x2200000000000`)"*.

**Now believed.** The constant is right and the bit numbering is wrong. `0x0002200000000000`
has bits **45 and 49** set. `bit 49 | bit 53` is `0x0022000000000000`, a different value.

**What proved it.** Reading the `movabs` bytes at `0023581D` and decomposing the immediate.

**Why the earlier reading was reachable.** `0x2200000000000` printed without leading zeros is
13 hex digits, and counting nibbles from the left of a 16-digit field rather than from the
right shifts every bit index by four. The value was transcribed correctly and only the
decomposition was wrong — which is exactly why a mask should be published together with the
bit list derived from it, not instead of it.

### Correction 2 — the keep banks hold 64 entries of 592 bytes, not 296 of 128

**Was believed.** That document's §2 and §4: *"each bank holds 296 entries of 128 bytes"*,
from the `0x128`-iteration, 8-`movups` copy loops.

**Now believed.** `0x9400` bytes partition as **64 entries of `0x250` = 592 bytes**. The copy
loops move 128 bytes per iteration × 296 iterations because that is how a `0x9400`-byte block
copy is unrolled — the chunk size is not the structure stride.

**What proved it.** Every accessor of the bank computes its entry address as `index * 0x250 +
g_pBtlKeepCharWork1`. Sixteen functions do it, including `Spawn_SelectAndPrepareAutomaticEntry`
(`0023588B`), `Spawn_SelectContinuousEntry`, `Spawn_SelectPreviousMapEntry`,
`SpawnEntry_GetDeathLimit`, `SpawnEntry_GetDeathCount`, `SpawnKeep_ResolvePrimaryEntry` and
`SpawnUnit_BindEntryAndMarkCapTracked`. `0x9400 / 0x250 = 64` with no remainder. The wipe branch
of `SpawnKeep_RotatePersistenceBanksForAreaTransition` resetting exactly **64** history counters
is the independent corroboration, and it was already in the document.

**Why the earlier reading was reachable.** It is the same defect that document recorded in its
own §8e — *a decompiler's rendering of a block copy is not a field-by-field body* — caught one
step short. §8e correctly retracted the *field names* painted onto the `memcpy` but kept the
*entry count* those loops appeared to imply. **A block copy's iteration count tells you the
buffer size divided by the chunk size, and nothing at all about the record size.** The stride
was available from any one of sixteen `imul` sites and none was consulted.

This correction does not disturb any conclusion in that document: enmity at `BKEI + 0x19..0x41`
is still inside the entry, the whole entry is still carried, and the rotation rule is unchanged.

### Correction 3 — `0031B760` is not a leaf accessor

That document names `0031B760` `ActorWork_GetBattleUnit` and treats it as the accessor. It is a
13-byte null guard that tail-jumps to `ActorWork_GetBattleUnitRaw` (`00263E30`), a 5-byte
`mov rax,[rcx+0x30]; ret`. Minor, but the tail jump means call-graph queries on `00263E30` will
under-report the guard's callers for the same reason `0023A520` appeared callerless.

## 9. Related

- [`spawn-placement-and-retirement.md`](spawn-placement-and-retirement.md) — the ring, the
  retirement rule, the keep banks and the return window; this document closes its L-7, L-9 and
  L-10 and corrects two of its claims
- [`../06-Movement-And-Navigation/heading-speed-to-position-delta.md`](../06-Movement-And-Navigation/heading-speed-to-position-delta.md) — the same `X = sin(θ)·r`, `Z = cos(θ)·r` sine-table convention, and `BattleUnit_PublishLocomotionPosition`, which is the placement call this system ends in
- [`../21-RNG-And-Determinism/rng-streams.md`](../21-RNG-And-Determinism/rng-streams.md) — the shared gameplay LCG the candidate radius and heading are drawn from
- [`../11-Party/`](../11-Party/) — `BattleUnit_GetPartyLeader`, whose position is the origin of every generated candidate
- [`../03-World-Area-Field/`](../03-World-Area-Field/) — the field region test and the surface query the height probe reaches

## 10. Adversarial work performed (not yet a full falsification pass)

**Program state:** parent `2ed8affb…`, snapshot `46f02e26…`, embedded EXE `73461d08…`, ledger
38,161 / 38,003 / 158 unresolved. `Verify-GfzCheckpoint.ps1` reported `CHECKPOINT VERIFIED`
before any reading, in project `proj_hd2` / `GFZ_HD2`.

**Instruments:** `DumpFullCoverageGraph.java` regenerated fresh (38,161 functions, 90,525
edges); an independent capstone census over every ledger body read from the authorized EXE
directly, with extents clamped to the next entry and truncated at the first `int3` after a
terminator (1,786,589 instructions walked); all numeric constants resolved by VA → file-offset
against the PE image, never from a decompiler rendering; `ff12-script` v3.00 over 828 scripts
extracted from `FFXII_TZA.vbf`.

~~`audit_crossrefs.py` has **not** been run against this document, and no independent party has~~
~~attacked it. `status` is `DOCUMENTED`, `audit.passes` is `0`.~~ *(answered: see §11 and §12, the later passes, and the front matter - `status` AUDITED, `audit.passes` 1, `crossref_clean` true; 2026-10-02, OPUS)* What follows is what was tried
during authoring, recorded so the eventual pass does not repeat it.

### Killer observations named and hunted

| Claim | What would kill it | Result |
|---|---|---|
| the mask is bits 49 and 53 | the instruction bytes decoding to a different pair | **KILLED.** Bits 45 and 49. |
| bits 45/49 have one writer each | a second `or`/`bts` site, or any `bt*` with immediate 45/49 | **SURVIVED.** Zero `bt*` sites exist; the memory-`or` census returns exactly the two, plus one field packer discriminated by its adjacent `shl 0x25`. |
| neither bit is ever cleared | any `and`-mask omitting the bit, or a whole-qword zero of a BattleUnit's flags | **SURVIVED for `and`.** The one candidate is a contiguous-field clear at `002D82DD`. **Not closed for bulk zeroing** — 387 sixteen-byte zero stores at displacement 0 exist and cannot be attributed to a BattleUnit statically. The counter-argument is `BattleUnit_ResetStateForReuse`'s existence: a routine that masks flags bit-by-bit implies the unit is *not* wholesale zeroed on reuse. Recorded as a limit, not as proof. |
| `FUN_00319390` writes a Y somewhere | any third store in its 139 bytes | **SURVIVED.** Two stores, then `ret`. |
| the garbage Y changes whether a spawn is accepted | the region test or its transform reading component `[1]` | **KILLED the worry.** Both read `[0]` and `[2]` only, so the stale value is carried but never consulted. |
| nothing ever fixes the Y | a later writer of the candidate's Y | **KILLED.** `SpawnUnit_FinalizeSpawnEntryActivation` overwrites it from a ground probe — which is the actual answer to L-7 and was found by chasing the *consumer* of the banked position rather than the producer. |
| the probe always runs | a gate on the probe | **NARROWED.** It runs only when `BattleUnit+0x1F6 & 8`, which comes from definition byte `+0x18` bit 4. |
| `btlAtelSetupActorStart` is called by every zone | a script defining units or spawning without it | **SURVIVED, and the claim was narrowed to fit.** 422 of 828 scripts never call it — but zero of the 400 unit-defining scripts and zero of the 172 spawning scripts are among them. "Every zone" is false; "every zone that can place anything" is true. |
| the three spawn-distance arguments map the other way | a triple that is coherent reversed | **SURVIVED.** All ten distinct authored triples satisfy `min < max < retire` under the derived mapping and none does reversed. |
| the keep entry is 128 bytes | any accessor using a different stride | **KILLED.** Sixteen accessors use `0x250`. |

### Positive controls run

- **Before claiming bits 45 and 49 are never cleared**, the identical query was run for **bit
  47**, which `BattleUnit_ResetStateForReuse` is known to clear. It returned **4** sites,
  including `00236AB1`. The instrument fires on exactly the instruction form the absence claim
  depends on, and the shape of its answer is right — a flag clear, where the single hit for
  bits 45/49 is a contiguous-field clear instead.
- **Before claiming the primitive table maps by opcode low byte**, the mapping was checked
  against three *consecutive* primitives (`0x304E`/`0x304F`/`0x3050`) whose handlers are three
  consecutive native functions in the same order, and against parameter arity from an
  independent source. A coincidence would not preserve order and arity simultaneously.
- **Before trusting the EXE reads at all**, the file's SHA-256 was compared with the authorized
  value and the `Import`/`Verify` pair reproduced the ledger, snapshot, embedded EXE and
  residual.
- **The PE image base was re-derived rather than assumed.** A first pass assumed `0x140000000`
  and found zero references to the primitive handlers; reading the optional header showed the
  ImageBase field is `0x00120000`, and the same query then found every one. An absence result
  from a wrong base is indistinguishable from a real absence.

### Two instruments disagreeing

Ghidra's call graph reports **zero** edges for `0023A520`; the capstone census finds the thunk
`jmp` at `00510710`. Ghidra models thunk forwarding, so the thunk is a sink in its graph. This
document uses the capstone result and says so. The same effect is why `00263E30`'s callers are
under-reported through `0031B760`.

### Banned evidence

No `.pdata`, `.xdata`, unwind record, EH map, IP-to-state map or
`_IMAGE_RUNTIME_FUNCTION_ENTRY` appears in any reasoning here. The PE parser in the census tool
reads the section table and `.text`/`.rdata`/`.data` contents only. Address adjacency was
available and refused: the primitive table's extent was bounded by walking records whose first
qword is code-or-null, and the index mapping is asserted from the eight confirmed hits and their
ordering, never from the records being neighbours.

### Reopening propagation

- **[`spawn-placement-and-retirement.md`](spawn-placement-and-retirement.md) must reopen.** Two
  of its claims are corrected here (§8 corrections 1 and 2), and three of its open questions
  close.
- **Any document describing the spawn-keep bank layout** inherits correction 2.
- **`06-Movement-And-Navigation`** gains an edge it may not list:
  `SpawnUnit_FinalizeSpawnEntryActivation` (Spawn) calls `FUN_003208C0` and
  `BattleUnit_PublishLocomotionPosition`, both Movement-owned. The owner of the placement
  transaction is Movement; Spawn owns the decision to place.
- **Any document about the ScriptVM dispatch tables** gains the `0x30xx` group's location and
  record shape.

## 11. Falsification pass 1 — 2026-09-03, session `repos-9e`

**The first independent attempt to destroy this document.** Its author recused on measured grounds:
it had been corrected twice, both times by them doing adjacent work rather than by review, and both
errors had survived their own writing *and* their own adversarial pass. They asked for whoever next
read a ScriptVM command table or a strided `.data` record array. This pass is by a session that had
done both that day and had not read this document.

**Nothing was overturned.** Two refinements, two instrument notes, and a list of what was not
attacked. **A survived pass is a result, and this one was not cheap to get** — every figure below was
re-derived from the image, and the two claims that had already been wrong once were attacked first.

### Everything re-derived, and what it cost to check

| Claim | Attack | Result |
|---|---|---|
| **36 body sizes** in §3 | re-derived from the certified function list | **36 of 36 exact** |
| `009146EC/F0/F4` = 39.0 / 42.0 / 43.0 | read from `.rdata` | **exact** |
| `00D10820` / `00D10828` = ±32768.0 | read from `.rdata` | **exact** |
| sine table at `01F004E0`, 32,768 floats, `table[i]=sin(2πi/32768)` | 338 entries sampled across the full extent | **0 mismatches**, worst \|Δ\| 1.2e-08 |
| `table[0x2000] == 1.0` | direct read | **exactly 1.0** |
| the table is 32,768 entries | read one past the end | **`table[32768]` is `1.0`, not `sin(2π)≈0`** — a different table starts there, so the claimed extent ends exactly where the pattern breaks |
| family 3 holds `147` in its first dword | direct read; control: family 0 reads 1496 as documented | **147, control PASS** |
| **ten** primitive → handler mappings | walked the 147 × `0x20` records at `01F281D0` | **10 of 10**, including `0x3053` at **record 83** exactly as stated |
| keep bank `0x9400` B = 64 × `0x250` | three independent routes | **all three agree** |
| flag bits are **45 and 49** (Correction 1) | full immediate/shift/BT sweep of all four cited functions | **exact** |
| `00233AD0` clears bit 26 | same sweep | **exact** — `bt qword, 26` |

**The keep bank, corroborated three ways** because Correction 2 had already changed this claim once
(from "296 entries of 128"):

```
stride    'imul reg, reg, 0x250' -> 50 sites, concentrated in Spawn*/SpawnKeep*/SpawnEntry*   # <- corrected 2026-10-02, OPUS - 27 sites in 18 functions (retool.py grep and a raw .text scan agree), 16 Spawn-owned, 10 in 0043F450; section 12 Finding 3
size      'mov reg, 0x9400'      -> 8 sites, in BattleStorage_InitializeWorkArrays
                                      and SpawnKeep_RotatePersistenceBanksForAreaTransition
arithmetic 0x9400 / 0x250 = 64 exactly, no remainder
```

**The flag bits, settled by the encoding.** Bits 45 and 49 cannot be reached by `test r/m64, imm32`,
so they compile as a 64-bit immediate — and the immediate is the same one in both places the
document says reads them together:

```
00235720 +0x0FD   mov r64, 0x0002200000000000     bits 45 and 49
00235720 +0x290   mov r64, 0x0002200000000000     bits 45 and 49
00233AD0 +0x0B2   mov r64, 0x0002000000000000     bit 49
005102D0 +0x011   mov r64, 0x0000200000000000     bit 45
```

Correction 1 is right, and the two bits genuinely travel together as one mask.

### Refinement 1 — the reset mask clears five bits, and naming two preserved ones understates it

§3 describes `00236A60` as *"masks `qwUnitFlags`; preserves bits 45 and 49"*. True, and the mask is:

```
0xFFFF7FFDFFE7FFFD
bits CLEARED : 1, 19, 20, 33, 47
bits preserved : 59 of 64, including 45 and 49
```

**It preserves 59 bits; naming two of them describes the reset by what it does not do.** The
informative half is the five it clears. Nothing here contradicts the document — but a reader asking
*"what does reuse actually reset?"* gets no answer from the current phrasing, and the answer is those
five bits.

### Refinement 2 — the `0x250` stride is not unique to the keep bank

The stride sweep found **~~18 of its 50 sites~~ 10 of its 27 sites inside one function** *(corrected 2026-10-02, OPUS: `retool.py grep` and a raw `.text` scan both give 27 `imul r, r, 0x250` sites in 18 functions, ten of them in `0043F450`; §12 Finding 3)*, `0043F450` — which is
`PrimaryOwner:Presentation`, 9,092 bytes, **references neither `0208E690` nor `0208E698`**, and whose
RIP targets are all in `02EBxxxx`/`02EC0xxx`/`02F97xxx`. It is an unrelated structure that happens to
share a 592-byte record size. Interior read 2026-09-17 (SWE2-FRONTIER): the body is a
`0036A230` battery — 47 calls to the same per-element helper, first at
[`0043F58E`](../_index/ADDRESS-INDEX.md), plus `0043EF40`/`0043F210`/`004FF440`/`00250000` once
each — consistent with an ~18-record walk over the shared stride.

**The document's identification survives because it is anchored on the two bank pointers, not on the
stride** — which is the right anchor and is why this is a refinement rather than a finding. Recorded
so that a later reader does not treat `imul …, 0x250` as a keep-bank signature: **more than a third
of its occurrences are not.**

### Two notes on the attacking instruments, because both were nearly wrong

- **The flag-bit matcher was too narrow at first.** It looked only for the `BT`/`BTS`/`BTR`/`BTC`
  family and found **bit 26 in `00233AD0` and nothing else** — which could have been reported as
  "bits 45 and 49 are not tested here". They are; a 64-bit bit position simply cannot be encoded as
  a `BT` immediate operand against a memory operand in the form the compiler chose, so it emits
  `mov r64, imm64`. **The absence was suspicious rather than conclusive precisely because bit 26 did
  appear** — a partial positive inside the same function is what said the matcher, not the code, was
  the problem.
- **The `0x9400` scan needed both the REX and non-REX `mov reg, imm32` encodings.** The first version
  had only the non-REX form and would have under-reported the allocation sites.

### What this pass did not attack

- **§2b's ground probe and §2a's "nothing generates a Y coordinate"** — the central mechanism. Read
  for structure; no body re-derived.
- **§2e's census** — *"who installs the tunables, and does every zone do it"*. This is the largest
  remaining surface and the one most like the population claims that failed in two other documents
  this session. It needs an independently built census, which this pass did not build.
- **§4's formulas** beyond the constants checked above.
- **Correction 3** (`0031B760` is not a leaf accessor) — its 13-byte body was size-checked only.
- The `002D81D0` "discriminated false positive" analysis in §3.

## 12. Independent falsification pass 2026-09-07 — `xiionline-61`

**First independent pass.** The auditor had not read this document before, and did not read
`repos-9e`'s or `repos-d2`'s notes on it. Program state **GN160**
`fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708`; every figure below re-derived by
decoding the authorized EXE, never from the ledger or from this document's own citations.

### Survived — every measurable claim attacked reproduced exactly

| claim | this pass |
|---|---|
| `009146EC` / `F0` / `F4` hold **39.0 / 42.0 / 43.0** | **confirmed**, read as `float` from `.rdata` |
| `FUN_0023A520` is 66 B and its listed body is complete | **confirmed instruction for instruction**, including the `0xB4` arc store and the `1` byte store |
| The five tunables are installed, not resident | **confirmed** — `02089358`, `02089360`, `02089364`, `02089368` and `0208D457` all lie **past `.data`'s raw backing**, so all five are **zero at image load** |
| **Correction 1** — `0x0002200000000000` is bits **45 and 49** | **confirmed** by decomposition |
| **Correction 2** — stride `0x250`, `0x9400 / 0x250 = 64` exactly | **confirmed** |
| **Correction 2** — *"sixteen functions"* compute `index * 0x250 + base` | **confirmed, exactly sixteen** Spawn-owned functions, and every one this document names by title is among them |

**The `0x250` census was run with a positive control first** — the document names `0023588B` as a
site, and the scan found it inside `Spawn_SelectAndPrepareAutomaticEntry` before any other result was
believed.

> **Correction 2 deserves specific credit for what it does *not* rest on.** `0x9400` partitions
> exactly **both** ways — `64 × 592` and `296 × 128` — so the arithmetic alone could never have
> settled it. The correction rests on sixteen `imul` sites and a 64-counter wipe instead, which is
> the right kind of evidence for a claim whose obvious form is undecidable.

### Finding 1 — §1's central negative is true as meant and false as written

§1 states:

> *"Nothing in the executable holds those numbers at rest."*

**Under the intended reading — the tunable globals are unset until a zone installs them — this is
exactly right**, and this pass confirmed it: all five are BSS.

**Under the reading a modder will take, it is false.** 39.0, 42.0 and 43.0 **are** in the executable,
as `.rdata` constants, and **this document prints their addresses three sections later** in §2e.
§1 is the section written for a reader with *no technical knowledge*, who cannot be expected to know
that *"at rest"* means *"in BSS before the installer runs"* — and who, on reaching §2e, meets
`movss xmm0, [009146EC] ; 39.0`.

**Rewritten** to say what is actually true: *the engine holds the numbers but does not apply them;
every zone installs them at battle setup.*

**And the ambiguity was hiding a modding consequence this document never states:**

> **`009146EC`–`009146F4` is the one place where the default ring changes for every zone at once.**
> Editing a zone script changes one zone; editing those twelve bytes changes the default that every
> zone installs before deciding whether to override it. **That is the difference between a mod and a
> patch**, and it follows directly from the mechanism §2e already establishes.

Added to §6.

### ~~Finding 2 — the provenance stamp is a checkpoint out of date~~ — WITHDRAWN, and the withdrawal is the finding

**This pass filed the GN158 `verified_against` stamp as a defect and updated it to GN160. That was
wrong, and reverted.**

`xiionline-8d` caught it: **the stamp records what the document was verified against**, and it was
last reviewed on 2026-09-02 when GN158 was current. That is the frontmatter working exactly as
designed. The standing rule is explicit — **never edit a provenance stamp to make a check pass** —
and what is stale here is the **review**, not the stamp. The fix for a stale review is a
re-verification that then updates it, never a re-stamp.

**And a partial pass cannot update a whole-document stamp anyway.** This pass examined the constants,
the installer body, the tunable residency and the two numeric corrections; it did **not** examine
§2a-§2f, §3, §4 or §5. Stamping the document as verified against GN160 would have claimed coverage
this pass did not have.

> **The error is worth more than the finding it replaced.** *"Bring the stamp to current"* is a
> one-line change that looks like tidying, passes every gate, and **quietly destroys the audit
> trail** — and it was made by the session that had just flagged the stamp as suspicious. Recorded in
> `COVERAGE.md`.

**Genuinely stale, and left alone:** §10's ledger figures (`38,003 / 158`) record what *that* session
observed against *that* parent, which is what a pass record is for.

### Finding 3 — a scoping ambiguity in the census, minor

*"Sixteen functions do it"* is **exact for Spawn-owned functions**. Image-wide, `imul r, r, 0x250`
appears in **18 functions across 27 sites** — a UI function once and a Presentation function ten
times, both unrelated uses of the same immediate. **The claim is correct as scoped and a reader
re-running the census gets 18**, so the scope should be stated.

### Not examined

§2a, §2b, §2c, §2f, §3, §4, §5, and the `167 zone scripts` count in §1. **This pass attacked the
constants, the installer body, the tunable residency and both numeric corrections** — everything
else in this document remains unaudited and must not be recorded as having passed.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. MECHANICAL-only crossings are recorded in the registry, not here.*

**CoreRuntimeScheduling — SERVICE.** `00235720` reads the raw tick counter (`GameClock_GetRawTickCounter`), so any
timing this page derives from that function is in the counter's units. What advances the counter is not restated here.
- **ActorEntity - CLIENT and SERVICE (53 edges).** `00233AD0` is also called by bodies filed to ActorEntity: `0037B4D0`; `00233AD0` reaches bodies filed to ActorEntity: `00238BF0`, `00239E10`, `0031B760` - shared machinery across the layer boundary, no shared ownership.
- **Gameplay - CLIENT and SERVICE (9 edges).** `00263E30` is also called by bodies filed to Gameplay: `003176E0` (Combat), `0031ADB0` (CombatAction), `00321380` (Combat); `00233AD0` reaches bodies filed to Gameplay: `003299B0` (Combat) - shared machinery across the layer boundary, no shared ownership.
- **Movement - CLIENT (74 edges).** `0022F830` is also called by bodies filed to movement: `0022E340`, `00230C10`, `00231400` - shared machinery across the layer boundary, no shared ownership.
- **Party - CLIENT and SERVICE (10 edges).** `00263E30` is also called by bodies filed to party: `0031B7E0`; `00234AF0`, `002350C0` reach bodies filed to party: `003272A0`, `003273B0` - shared machinery across the layer boundary, no shared ownership.
- **Presentation - CLIENT (26 edges).** `00230B60`, `00231890`, `00232490` are also called by bodies filed to presentation: `00258350` (ScriptedCamera), `003CC970`, `0032BB00` - shared machinery across the layer boundary, no shared ownership.
- **RNG_Random_Selection - CLIENT and SERVICE (4 edges).** `00328370` is also called by bodies filed to random selection: `00308EC0`; `00234AF0`, `002355A0`, `002395A0` reach bodies filed to random selection: `00328370` - shared machinery across the layer boundary, no shared ownership.
- **Script_VM_Native_Bridge - CLIENT (18 edges).** `00235340`, `00235360`, `002354F0` are also called by bodies filed to script VM / native bridge: `005107F0`, `00510260`, `00510230` - shared machinery across the layer boundary, no shared ownership.
- **Status_Periodic_Terminal - CLIENT and SERVICE (3 edges).** `00263E30` is also called by bodies filed to status/periodic terminal: `00386860`; `00236A60`, `0023A410` reach bodies filed to status/periodic terminal: `00320450`, `0030FED0` - shared machinery across the layer boundary, no shared ownership.
- **UI - CLIENT (1 edge).** `00263E30` is also called by bodies filed to UI: `0031EB20` - shared machinery across the layer boundary, no shared ownership.
- **WorldAreaField - SERVICE (6 edges).** `00233AD0`, `00234AF0`, `002350C0` reach bodies filed to WorldAreaField (world area): `00313F60`, `002374E0`, `003209C0` - shared machinery across the layer boundary, no shared ownership.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Combat — CLIENT.** `FUN_003206e0`, owned by that layer, calls `00263E30` on this page. That caller is a 176-byte routine behind the same `byte[02089340] & 0x10` gate, resolving through `003588B0`; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**CombatAI — CLIENT.** `BattleUnit_SelectAiOrderSetVariantFromAuthoredTable`, owned by that layer, calls `0031B760` on this page. That caller is the variant choice, bounded at **four** indices: `word[[+0xE60] + 0x50 + index*2]` names a row in the table at `[02EBF168]`, and the resolved pointer is stored at the unit's `+0x6E0`; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**CombatFormula — SERVICE.** `0023A410` on this page calls `BattleStats_SetCurrentHP`, owned by that layer. What it reaches is **eight bytes** that turn the delta-based HP path into an absolute set: it subtracts `dword[+0x48]` from the value it is given and jumps straight into the modification entry point - which is what fixes `+0x48` as the current value; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

## SWE2-EC7-26 update (2026-09-18) — `0031A930` angular-delta magnitude

`0031A930` (89 B) computes `|wrap(x0 - x1)|`: subtracts the angles,
folds into [-pi, pi] by repeated `addss` of the +/-pi constants at
`00915620`/`00915624`, then `cvtss2sd`/`andps 0x7FFF...`/`cvtsd2ss`
takes the absolute value — the angular-delta magnitude the placement
and heading paths measure with (sibling of `00316DA0` and batch-22's
`0026B5A0`). Interior anchor `0031A97D` (the abs mask).
## SWE2-EC7-32 update (2026-09-18) — `00233050` cell-index resolver

`00233050` (114 B) is the cell resolve the probe table and the
`00231900` paragraph both name: `xmm1 = int[rcx+0x38] + float[rdx]`,
`xmm0 = int[rcx+0x3C] + float[rdx+8]` — either going negative
returns `0xFFFF`. `trunc(xmm1) / dword[r8+0x10]` gives the column
(`r9d`); an odd column adds `-((width - remainder) >> 1)` to `xmm0`'s
truncated row before `row / dword[r8+0x14]`. Column `< [r8+8]` and
row `< [r8+0xC]` must hold, and the answer is
`row * [r8+8] + column` — the probe's grid linearization with a
centering nudge on odd columns. Interior anchor `00233086` (the
`idiv [r8+0x10]`).

## SWE2-EC7-41 update (2026-09-19) - `002374E0`

`002374E0` (334 B) is a spawn-placement body - `01CEBB70`/`01CEBBA8`/`01CEBDA0`/`01F44830`, `00325EA0` pair/`00808C40`. Interior anchor `0023755E` (a `00325EA0` call).

## SWE2-EC7-59 update (2026-09-19) - `0043F210`

`0043F210` (159 B) ~~is a spawn-placement body~~ is not a spawn-placement body: its only caller is the Presentation function `0043F450` (`0043F488`, §11), and it reads no spawn global or keep entry *(corrected 2026-10-02, OPUS: `retool.py callers 0043F210`, body read)* - `003697F0` single call. Interior anchor `0043F22B` (a `003697F0` call).

## SWE2-EC7-61 update (2026-09-19) - `00325EA0`

`00325EA0` (152 B) is the `Vector3_RotateTranslatedXZOffsetByEncodedAngle` the placement page names - call-free `cvttss2si` index `&0x7FFF` into the `01F004E0` trig table, `00D10820`/`00D10828` scale constants. Interior anchor `00325EF8` (the `01F004E0` table index).

