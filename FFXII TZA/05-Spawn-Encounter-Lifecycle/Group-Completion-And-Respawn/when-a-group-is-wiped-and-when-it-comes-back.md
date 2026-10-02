---
system: Group completion and respawn timing — the dead-member ledger and the cooldown clock
category: 05-Spawn-Encounter-Lifecycle
status: AUDITED
owner_layer: PrimaryOwner:Spawn_Encounter_Lifecycle
evidence_tier: 1
level: L1
readiness: BEHAVIORALLY UNDERSTOOD
confidence: PROVEN
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: six function bodies disassembled from the shipping EXE; every RIP target computed with a
    tool; the ledger extent derived from the reset loop's own bounds; names taken as leads from
    Collaboration research prose and then re-derived, which corrected one of them. 2026-09-10 (FABLE):
    fourteen more bodies read from the same EXE; every function addressing the ledger enumerated by a
    from-entry scan of all 34,270 bodies with a positive control; the unit's group-id and mode bytes
    given a from-entry displacement sweep with a positive control; the reaction handler's jump table
    decoded from the image
last_reviewed: 2026-09-12
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-when-a-group-is-wiped-pass-1
  last_pass_kind: authored
  crossref_clean: true
  reopened_count: 0
---

# Group completion and respawn timing

> **Imported from the research backlog, then re-derived** — and the re-derivation **corrected one of
> the imported names**. See [`../../_index/RESEARCH-IMPORT-BACKLOG.md`](../../_index/RESEARCH-IMPORT-BACKLOG.md).

## 1. What the player sees

Enemies in FFXII come in **groups**, and the game tracks them as a set rather than one at a time. Kill
four of five wolves and nothing happens; kill the fifth and the encounter *completes* — the moment
that ends a hunt, opens a gate, or lets an area go quiet.

**The game does not count corpses. It keeps a checklist**, one bit per member, and asks whether every
bit it was expecting is now set. That is why killing the same enemy twice, or a member that was never
part of the group, does not advance anything — the bit is already set, or it is not a bit the group
was waiting for.

And when a defeated enemy is allowed back, the wait is measured in **seconds of play**, not frames.
The game divides its frame counter by the current frame rate before comparing, so **a group's respawn
delay is the same wall-clock wait at 30 fps and at 60 fps** — the same conversion that keeps every
other authored duration honest.

**Which enemies belong to which group is not engine knowledge — each enemy's own script declares it**
(§4, *Who writes `memberMask`*), one call per member, every time the area is entered. And "the
encounter completes" means something specific: the party's controls are locked and the group's number
is posted where the field script can read it (§5), either at once or only after the last member's
death animation has been handled — the script chooses which when it registers the member.

## 2. Finding a spawn record — the shared accessor prologue

Nine accessors in this family open with the **same seven checks**, instruction for instruction. Read
once here rather than nine times:

```c
SpawnRecord *resolve(int lane /*edx*/)
{
    BattleUnit *u = ActorWork_GetBattleUnit();      /* 0031B760 */
    if (!u)                       return NULL;
    u8 *map = u->p_40;                              /* the lane map */
    if (!map)                     return NULL;
    if (lane < 0)                 return NULL;
    if (lane > map[0] - 1)        return NULL;      /* map[0] is the count */
    u8 slot = map[1 + lane];                        /* the slot for this lane */
    if (slot == 0xFF)             return NULL;      /* 0xFF marks an empty lane */
    SpawnRecord *r = *(char**)0x0208E690 + slot * 0x250;
    if (r == NULL)                return NULL;
    return r;
}
```

~~Every one of the nine returns **`-1`** when this fails, so `-1` is *"no such lane"*, never a value.~~ **Corrected 2026-09-13: `SpawnEntry_GetScriptSelection` (`00236140`) returns `-2`, and `-2` *is* inside its value range** — see the falsification pass.

**The record stride is `0x250` = 592 bytes**, and the array base is a pointer read from `0x0208E690`
— the records are heap, not image.

> **One dead branch, recorded because it looks like a check and is not.** After
> `movzx eax, dl` the code runs `test eax, eax / js`. A byte zero-extended into a 32-bit register can
> never be negative, so that arm is unreachable. It appears in **all nine** accessors — one template,
> copied.

## 3. The respawn fields, and the formula that reads the clock

| offset | width | field | read by |
|---|---|---|---|
| `+0x08` | `u16` | **death count** | `SpawnEntry_GetDeathCount` `00235F50` |
| `+0x0C` | `u32` | **second-stamp of the last death** | `00235FB0`, below |
| `+0x10` | `u16` | **respawn cooldown** | `SpawnEntry_GetRespawnCooldownTicks` `002366E0` |

`00235FB0` is the only one of the three that computes anything:

```asm
00235FFA  call  0x32A150                 ; GameClock_GetRawTickCounter -> *(u32*)0208D45C
00235FFF  movss xmm0, [01DFE0B8]         ; the frame-rate scale: 1.0f or 2.0f
00236009  mulss xmm0, [008F8D80]         ; 30.0f
00236011  cvttss2si ecx, xmm0
00236015  div   ecx                      ; unsigned, edx = 0
00236017  sub   eax, [rbx + 0xC]
```

```c
divisor = (int)(*(float*)0x01DFE0B8 * 30.0f);       /* 30 at FrameLimit=30, 60 at FrameLimit=60 */
elapsed = (*(u32*)0x0208D45C) / divisor - record->u32_0C;
```

> **The divisor is frames-per-second, so the quotient is seconds.** `0x01DFE0B8` is the frame-rate
> scale this database documents under `FrameLimit` — `1.0f` at 30, `2.0f` at 60 — so the divisor is
> literally 30 or 60. **A respawn wait is therefore the same number of seconds at either frame rate.**

### ⚠ The imported name was wrong, and the binary says so

The research prose calls `00235FB0` **`SpawnEntry_GetElapsedTicksSinceLastDeath`**. It does not return
ticks. It divides the tick counter by the frame rate first, so **it returns seconds**, and `+0x0C`
holds a **second**-stamp rather than a tick-stamp.

**This is exactly why an imported name is a lead and not a source.** Carried across unchecked, it
would have put a factor of 30 or 60 into any reimplementation of respawn timing — and the error would
have been invisible at 30 fps in a system that also has a 30-vs-60 scale in it.

*(`GetRespawnCooldownTicks` at `+0x10` is left with its imported name: this document has not seen it
compared against `00235FB0`'s result, so whether its unit is seconds is **unverified**. `EE-1`.)* *(2026-09-13: the
scripts compare them — every `btlAtelGetRespawnTime` is `btlAtelGetElapseTime(i) > btlAtelGetRespawnTime(i)`; seconds. §8.)*

### The write side of `+0x08` and `+0x0C` — added 2026-09-10

Both are written on **the lethal branch of `BattleStats_ModifyHPAndProcessLethalState`
(`00300530`)**, the death handler's only caller. When the unit is spawn-backed (`003007F4` — the record
byte `+5 == 1`, the same gate §5 uses), it takes the spawn record pointer from unit `+0x6A0`
(`003007FA`) and:

```asm
00300801  inc  word ptr [rax + 8]           ; death count += 1
00300805  call 0x32A150                     ; GameClock_GetRawTickCounter
0030080A  movss xmm0, [01DFE0B8]            ; the same frame-rate scale
00300814  mulss xmm0, [008F8D80]            ; × 30.0f
0030081C  cvttss2si ecx, xmm0
00300820  div  ecx                          ; ticks / fps = SECONDS
00300829  mov  [rcx + 0xC], eax             ; second-stamp of this death
0030082F  call 0x306F00                     ; then the group ledger, §5
```

**The stamp is written in seconds by the same formula that reads it back**, which closes the unit
question for `+0x0C` from both sides. ~~`+0x10` is still not seen written anywhere in this family —
`EE-1` stands.~~ *(Corrected 2026-09-29, FABLE, Claude Opus 5.5; [`pkg-gp-spawn-respawn`](../../_index/candidates/pkg-gp-spawn-respawn/README.md) W:)*
the keep entry's initialiser writes `+0x10` = the row's base + `rand % (range + 1)`, or 0 when the base is 0
([the keep-entry field map](../Spawn-Record/the-spawn-keep-entry-field-map.md) §2.4; the sites are in the record); `EE-1` is
ANSWERED. And `unit + 0x6A0` is the spawn record itself. **For a spawn-backed unit** the
"kind block" at `+0x698` is the same record `+0x80`, so `[+0x698]+5` is record byte `+0x85`; but
that is the spawn-backed case of `+0x698` — for party units it points at a different record, the BattleSystemState element (reworded 2026-09-13 from "one of the two homes of the same record") — `BattleUnit_ApplyUnitDefinition` stores the spawn
record's `+0x80` page there only for definition ids with high byte 1, and for high byte 0 (party
characters) stores a `BattleSystemState` element and a **null** `+0x6A0` instead
(`0023AA49`–`0023AAC1`, `0023ABFA`–`0023AC01`; resolved 2026-09-10 under `OPUS-CONTRA-BU698`,
[the kind byte page](../../04-Actor-Entity/Battle-Record-Kind/battle-record-kind-byte.md) §2).
Every gate in this family tests `[+0x698]+5 == 1`, which is exactly the high byte of the definition
id, so the ledger only ever sees units of the first kind.

## 4. The group ledger — a checklist, not a counter

`SpawnGroup_ResetLifecycleLedger` (`00307090`, 73 B) walks a fixed table and its bounds give the
structure exactly:

```asm
00307090  lea rax, [02EC13D0]          ; note the +0x10 bias
00307099  lea rdx, [02EC19D0]
003070A0  and byte [rax],      0xFE    ; four flag bytes, bit 0 cleared
003070A3  and byte [rax+0x18], 0xFE
003070A7  and byte [rax+0x30], 0xFE
003070AB  and byte [rax+0x48], 0xFE
          ... eight qwords zeroed at rax-0x10, -0x08, +0x08, +0x10, +0x20, +0x28, +0x38, +0x40
003070CF  add rax, 0x60
003070D6  jl  0x3070A0
```

**The `0x60` stride is four entries unrolled, not one 96-byte entry.** The death handler settles it by
indexing the same table with `lea rax,[rcx+rcx*2]` then `[rdi + rax*8]` — a **× 24** stride from base
`0x02EC13C0`:

```c
struct SpawnGroupLedger {          /* 24 bytes */
    u64 memberMask;                /* +0x00  the members this group is waiting for */
    u64 deadMask;                  /* +0x08  the members confirmed dead */
    u8  flags;                     /* +0x10  bit 0 set on one completion path */
};                                 /* +0x11..+0x17 padding */
```

```
base 0x02EC13C0 · walked to 0x02EC19C0 · 1,536 bytes / 24 = exactly 64 groups
```

**64 groups, each tracking up to 64 members** — one bit per member in a `u64`. The table is in
`.data` **past `SizeOfRawData`**, so it is BSS and starts at all zeros.

### The reset zeroes ~~all three fields~~ both masks and flag bit 0 only — added 2026-09-10 *(corrected 2026-10-02, OPUS: `003070A0`–`003070AB` are `and byte ptr [...], 0xFE`)*

The `0x10` bias puts the eight qword stores on **both masks of all four entries**, not on `deadMask`
alone. With `rax` at entry 0's `flags` byte and `rcx = 0` from `00307097 xor ecx, ecx`:

| store | address written | field |
|---|---|---|
| `003070B3 mov [rax-0x10], rcx` | base `+0x00` | entry 0 `memberMask` |
| `003070AF mov [rax-0x08], rcx` | base `+0x08` | entry 0 `deadMask` |
| `003070BB mov [rax+0x08], rcx` | base `+0x18` | entry 1 `memberMask` |
| `003070B7 mov [rax+0x10], rcx` | base `+0x20` | entry 1 `deadMask` |
| `003070C3 mov [rax+0x20], rcx` | base `+0x30` | entry 2 `memberMask` |
| `003070BF mov [rax+0x28], rcx` | base `+0x38` | entry 2 `deadMask` |
| `003070CB mov [rax+0x38], rcx` | base `+0x48` | entry 3 `memberMask` |
| `003070C7 mov [rax+0x40], rcx` | base `+0x50` | entry 3 `deadMask` |

**A reset zeroes both masks of every group and clears the pending flag's bit 0.** Its only caller is
`BattleSystem_InitializeAreaState` (`002342F0`), so **membership does not survive an area change; it
is rebuilt by script on every entry** (next subsection). *The contract's §7 previously said the reset
kept `memberMask`. Corrected 2026-09-10 from this arithmetic; the contract keeps the trail.*

> ### The masks are zeroed. The flag byte is not. (corrected 2026-09-13, `OPUS-LEDGER-RESET-BIT0`)
>
> This paragraph used to read *"empties every group completely — members, deaths and the pending
> flag"*, and the contract's §6 said *"empties everything — both masks and the flag"*. **The masks
> are whole-qword zero stores; the flag is not zeroed.** `003070A0`–`003070AB` are four
> `and byte ptr [...], 0xFE` — **bit 0 only. Bits 1–7 survive a reset untouched.**
>
> **So the reset's postcondition is `memberMask == 0 && deadMask == 0 && (flags & 1) == 0`, not
> `flags == 0`.** A reimplementation or a parity check that asserts the whole byte is zero
> over-specifies: it happens to hold today, and it is not what the code guarantees.
>
> **Why it happens to hold — the whole-byte census.** Every reference into the ledger
> `02EC13C0`–`02EC19C0` is a rip-relative `lea`, and there are **exactly six** image-wide
> (`00306EBC`, `00306F5D`, `00307049`, `00307090`, `003070E0`, `0030712C`), confirming §6's "six
> functions" from a second direction. Across all of them, **every access to the flags byte touches
> bit 0 and nothing else**:
>
> | site | instruction | bits |
> |---|---|---|
> | `00306FE0` | `or byte ptr [rdi + rcx*8 + 0x10], 1` | sets bit 0 |
> | `00307133` | `or byte ptr [rax + rcx*8], 1` | sets bit 0 |
> | `00307053` | `test al, 1` | reads bit 0 |
> | `00307057`/`00307061` | `and al, 0xFE` then store | clears bit 0 |
> | `003070A0`–`003070AB` | `and byte ptr [...], 0xFE` ×4 | clears bit 0 |
>
> **No instruction in the image sets, clears or tests any other bit of this byte.** Bits 1–7 are
> never written and never read, so in the shipped game the byte only ever holds 0 or 1 and the
> stronger assertion is *observationally* true. That is a fact about the rest of the image, not a
> guarantee of the reset — which is exactly why the two must be recorded separately.
>
> The same loop settles two more figures from the code rather than from the table: `00307030`
> walks with `add rdi, 0x18` and `cmp ebx, 0x40`, so **stride 24 and count 64**, and it clears bit 0
> as it consumes each pending signal — the `flags &= ~1` edge in §7's state machine.

### Who writes `memberMask`, and when — `EE-2` answered 2026-09-10

Every function that addresses the ledger, by any addressing form, from every function entry in the
image — `data_xref_scan.py --range 0x02EC13C0 0x02EC19C0`, control `02089340` = 126 references —
is one of **six**, and four of them were unread on 2026-09-08:

| entry | size | GFZ name — a lead, re-derived here | caller(s) |
|---|---:|---|---|
| `00306E60` | 158 B | `SpawnGroup_UpdateExpectedMemberLaneMask` — **the writer** | `00239710` (adds), `002350C0` (removes) |
| `00307030` | 82 B | `SpawnGroup_DispatchPendingCompletionSignals` | `BattleSystem_RunFieldFrameOrchestrator` `00234590` |
| `003070E0` | 39 B | `SpawnGroup_HasPendingCompletionSignal` | `BattleUnit_UpdateLifecycleAndCombatFrame` `00233F70` |
| `00307110` | 40 B | `SpawnGroup_MarkCompletionPendingAfterReaction` | `BattleUnit_HandleReactionAnimationEvent` `003250F0` |
| `00306F00`, `00307090` | | §5 and above | |

(`02EC19C0`, which five more functions address, is the first byte **past** the ledger — entry 63
ends at `02EC19BF` — and belongs to the next object.)

`00306E60(BattleUnit *u /*rcx*/, int add /*edx*/)` opens with **the same gates as the death
handler** — null unit (`00306E60`), null record at `+0x698` (`00306E7F`), record byte `+5 != 1`
(`00306E84`), group id `0` at `+0xE98` (`00306E96`) — resolves the slot the same way (`00263D30` at
`00306E9E`, `002360D0` at `00306EA9`, a negative rejected at `00306EB0`), computes the same 32-bit
shift (`00306ECE shl edx, cl`), and then:

```asm
00306ED0  test esi, esi            ; the second argument
00306ED2  je   0x306EDC
00306ED4  movsxd rax, edx          ; add:    memberMask |= sx32(bit)
00306ED7  or   [r8], rax
00306EDA  jmp  0x306EE5
00306EDC  mov  eax, edx            ; remove: memberMask &= sx32(~bit)
00306EDE  not  eax
00306EE0  cdqe
00306EE2  and  [r8], rax
00306EE5  not  edx                 ; BOTH:   deadMask &= sx32(~bit)
00306EE7  movsxd rax, edx
00306EEA  and  [r8+8], rax
```

**Three things this settles.**

1. **`memberMask` is per-unit and additive.** One call registers, or unregisters, *one* member — its
   own slot bit. There is no bulk populate; a group of five wolves is five calls.
2. **Registering a member clears its dead bit**, whether adding or removing. A member that dies,
   comes back and is registered again is *alive* to the checklist once more — this is what re-arms a
   group after a respawn.
3. **The bit is the same sign-extended 32-bit shift the death handler uses** (contract §12), so the
   two writers agree with each other: slot 31 registers bits 31–63 at once and slots ≥ 32 alias onto
   `slot & 31`, and the aliasing is invisible in play as long as a group's slots stay under 31.

#### The `add` caller is a script verb — membership is authored

`00239710` (`SpawnGroup_ConfigureUnitMembershipAndMode`, 114 B) has exactly one caller, `0050F8C0`:
the wrapper for **verb `0x3030`, `btlAtelSetEventFlagGroup`** in
[the verb table](../../01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-verb-table.tsv) (`pops_int = 2`).
The wrapper pops two integers and tail-jumps:

```asm
0050F8D8  call 0x267E10             ; first pop  -> ebx -> edx   (mode)
0050F8E2  call 0x267E10             ; second pop -> r8d          (group)
0050F8FE  jmp  0x239710
```

and `00239710`, on the battle unit of the verb's target context (`ActorWork_GetBattleUnit` at
`0023971F`; returns `-1` at `0023972C` when there is none):

```asm
0023973A  and  byte [rax+0xE99], 0xFE          ; clear mode bit 0
00239746  mov  byte [rax+0xE98], dil           ; +0xE98 = group      THE group-id writer
0023974D  cmp  ebx, 1 / sete cl                ; bit 0 = (mode == 1)
00239759  and  cl, 0xFD                        ; clear bit 1
0023975C  cmp  ebx, 2 / sete al / add al, al   ; bit 1 = (mode == 2)
00239766  mov  byte [r9+0xE99], cl             ; +0xE99 = mode bits  THE mode writer
00239770  call 0x306E60                        ; edx = 1 (00239741): ADD this unit to its group
```

**So "when, relative to the first death" is: whenever the member's own script says so.** The engine
never populates the mask itself. A unit whose script has not yet run `btlAtelSetEventFlagGroup` has
`+0xE98 == 0`, is invisible to the ledger and can complete nothing; the moment the verb runs it is an
awaited member with a clear dead bit. The ordering is a property of the authored script, and the
"zero mask completes on the first death" edge of §5 needs a unit with a non-zero `+0xE98` whose
group has an empty mask — which the writers as read do not produce, because **the only writer of
`+0xE98` registers the unit in the same call.** (Sweep: every function entry, memory operands with
displacement `0xE98` or `0xE99`, positive control the `00239746` write. Byte writers of either:
`00239710` only. `00791FC2` writes a **qword** at `+0xE98` inside a long zeroing run over a
different, larger object — excluded by width and context. Readers of `+0xE98`: the six ledger
functions, `00233EA0`, and the four `SpawnGroup_*ByGroupMask` teardown helpers at `00234880`,
`00234990`, `00234A10`, `00234A80`, plus `00237690`.)

Both mode bits are consumed: bit 0 selects the completion arm (§5); bit 1 is tested by
`BattleUnit_TeardownAndDespawn` at `00300F89` and, when set, **skips two actor-work calls**
(`0025AB30`, `002697E0` at `00300F96`/`00300F9F`) on the spawn-backed teardown path — noted, not read
further. `EE-10`.

> **Script-side argument order — ~~inferred, not observed~~ observed 2026-09-13 (`EE-11`, below).** The first pop is the *last* pushed
> ([the calling convention](../../01-Script-VM-Native-Bridge/Spawn-Verbs/the-script-to-native-calling-convention.md)
> §2), so as written in a script the verb is `btlAtelSetEventFlagGroup(group, mode)`. The decompiler
> catalog types its parameters `INT, INT|FLOAT`, consistent with a small mode literal second. ~~No~~
> ~~shipped script has been decompiled to confirm it — the two `.ebp` files on hand are containers the~~
> ~~decompiler rejects unpacked.~~ *(answered: see the next paragraph - `EE-11` observed in the shipped scripts 2026-09-13; 2026-10-02, OPUS)* `EE-11`.
>
> **`EE-11` answered 2026-09-13 (FABLE),** **observed in the shipped scripts.** The 1,114 decompiled `us` scripts contain **6,746** calls in **502** files, and every one sits in a `spawnGroup` block's entry function (`entry00` 2,056, `entry01` 2,014, … `entry07` 84), after `btlAtelSetUnit` and immediately after `btlAtelSetLevel` — a fixed authored preamble (`btlAtelSetUnit`, `…SetDirection`, `…SetDefaultLogic`, `…SetHpLowLimit`, `…SetLevel`, **`…SetEventFlagGroup`**, `…SetCallGroup`, `…SetUnitType`, `…SetBelong`, e.g. `bds_e01` `BOSS_カオス`). So registration runs when the spawned unit's entry script starts, before it can act or die. The argument values fit `(group, mode)` and not the reverse: the **second argument is only ever 0, 1 or 2** — exactly the values `00239710` distinguishes (`== 1`, `== 2`) — while the first ranges 0–5: `(0, 0)` 6,206 (no group — the unit stays outside the ledger), `(1, 0)` 438, `(1, 1)` 74, `(1, 2)` 13, `(2, 1)` 4, `(2…5, 0)` two each and `(3…5, 1)` one each. So 540 registrations join a group, 81 with mode 1 (the flag-and-`0x2005` arm), 13 with mode 2 (the teardown skip of `EE-10`), and groups 2–5 appear only 6, 3, 3 and 3 times against group 1's 525.

#### The `remove` caller is range retirement

`SpawnLifecycle_CheckAndRetireByNativeRange` (`002350C0`), documented in
[spawn placement and retirement](../spawn-placement-and-retirement.md), ends its retire action with
`002352BB call 0x306E60` and **`edx = 0`** (`002352B6 xor edx, edx`), after
`BattleUnit_TeardownAndDespawn(unit, 1)` at `002352B1`. **A unit retired for distance is struck off
its group's checklist**, its dead bit cleared with it. It is not a death — `00306F00` is not called —
so a group whose last living member walks out of range does not complete; it has one member fewer to
wait for until that unit is respawned and its script registers it again.

**Live corroboration, 2026-09-10 (ASTRA, [EXP-019](../../_experiments/EXP-019-group-ledger-live.md)) —
a separate evidence tier, not a static claim:** on a loaded save at the Stepping, group 1's ledger
entry read `memberMask = 1`, `deadMask = 0`, `flags = 0`, and slot 3 of the table at `*(02098E68)`
read 0, **before any attack**; pool slot 4 was a kind-1 unit (HP 134, mode 1) resolving to member
bit 0. That is what the static reading above predicts for the state after the script's
`btlAtelSetEventFlagGroup` calls and before the first death. The registration writer and its timing
were not traced live, no enemy was killed, so the completion flag and the slot-3 post remain
untested at runtime (`FABLE-REQ-ASTRA-LEDGER` is blocked on a route to the grouped actor).

## 5. Recording a death, and the completion test

`SpawnGroup_RecordMemberDeathAndHandleCompletion` (`00306F00`, 303 B):

```c
bool RecordMemberDeath(BattleUnit *u)
{
    if (!u)                        return false;
    void *k = u->p_698;
    if (!k)                        return false;
    if (k->b_05 != 1)              return false;      /* kind gate */

    u8 group = u->b_E98;                              /* 1-based group id */
    if (group != 0) {
        int bkei = FUN_00263D30(u->p_10);
        int lane = SpawnLaneMap_ResolveBkeiIndex(u->p_40, bkei);   /* 002360D0 */
        if (lane >= 0) {
            Ledger *L = (Ledger*)(0x02EC13C0 + (group - 1) * 24);
            L->deadMask |= (1ull << lane);   # <- corrected 2026-10-02, OPUS - a sign-extended 32-bit shift, (int64)(int32)(1u << (lane & 31)); 00306F6F mov eax, 1 / 00306F74 shl eax, cl / 00306F76 cdqe / 00306F78 or [rdx+8], rax; contract section 12
            if ((L->memberMask & L->deadMask) == L->memberMask)
                goto complete;                        /* every awaited member is dead */
        }
    }
    return false;

complete:
    FUN_00307140(1);  FUN_00238B70(1);  FUN_00238AE0(1);

    if (u->b_E99 & 1) {
        u->q_00 &= 0xFFFF7FFFFFFFFFFF;                /* CLEAR bit 47 */
        ((Ledger*)(0x02EC13C0 + (u->b_E98 - 1) * 24))->flags |= 1;
        BattleUnit_DispatchActorPresentationEvent(u, 0x2005);
    } else {
        u->q_00 |= 0x0000800000000000;                /* SET bit 47 */
        BattleUnit_DispatchActorPresentationEvent(u, 0x2008);
    }
    return true;
}
```

**The completion test is `(memberMask & deadMask) == memberMask`**, not a count reaching a total. Three
consequences follow directly and are worth stating because they are the observable behaviour:

- **Killing the same member twice does nothing.** The bit is already set; the mask is unchanged.
- **A member outside `memberMask` cannot complete a group**, however many of them die.
- **A group whose `memberMask` is `0` completes on the first death**, because `0 & anything == 0`.
  The ledger is BSS and starts at zero, so **whatever writes `memberMask` must run before the first
  death** or the group completes immediately. ~~That writer is not identified here — `EE-2`.~~
  **Identified 2026-09-10: `00306E60`, driven by each member's own script (§4).** The edge stays
  as a reimplementation edge case; the writers as read do not reach it.

### There is no one-shot — and why that does not double anything in play

Nothing in `00306F00` or its caller remembers that a group has already completed. The caller is the
lethal branch of `BattleStats_ModifyHPAndProcessLethalState` (`00300530`, §3): it bumps the spawn
record's statistics, calls `0030082F call 0x306F00`, and on a reported completion **skips the
normal death presentation event** (`00300836 jne`) — otherwise it dispatches one itself
(`0x2007`/`0x2008` at `00300854`–`0030085F`, or `0x200E` when its argument has bit 8, `00300846`).
No flag is consulted first, so a second completion of the same group re-runs the whole path.

**What can make the test true twice** is a further death in that group after every registered member
is dead, and there are two ways to get one:

- a dead member respawns and its script registers it again — `00306E60` clears its dead bit, the
  group is *incomplete* again, and its next death is a genuine second completion. **That is the
  design**: the room is cleared twice.
- a unit carrying the group id whose slot is **not** in `memberMask` dies. Registration and death
  resolve the slot from the same two fields, so this needs a lane map that changed between them, or
  a unit whose registration failed at `00306EB0` but whose death resolves — which fails the same
  check at `00306F55`. **Not reachable from the code as read.**

And what completion *does* is idempotent bit-setting plus one deferred signal that is consumed once
per frame (next two subsections), so "duplicate rewards" is not on the table: **no reward code is on
this path.**

### The two arms are two routes to one flag — `EE-3`, `EE-4` answered 2026-09-10

The arm is chosen by **mode bit 0 of `+0xE99`**, which `btlAtelSetEventFlagGroup` sets exactly when
its mode argument is `1` (§4). Both arms end at the same place by different routes:

```
mode == 1   00306FC9 clear unit bit 47 · 00306FE0 ledger.flags |= 1 · 00306FE8 dispatch 0x2005
mode != 1   0030700C SET unit bit 47   ·                             · 00307012 dispatch 0x2008
                 |
                 v  BattleUnit_HandleReactionAnimationEvent (003250F0), events 0x2007/0x2008/0x200C/0x200E
                    (jump-table case 00325185, decoded from the index bytes at 00325224 and offsets at 00325208):
                    00325185 unit |= bit 33 ; 0032519C test bit 47 ; 003251A4 call 00307110
                        00307110: 0030711A clear bit 47 ; 00307133 ledger[+0xE98 - 1].flags |= 1
                 |
                 v  SpawnGroup_DispatchPendingCompletionSignals (00307030), once per field frame
                    gate 00233D20: (02089340 & 0xF00) == 0  (00233D24)  and  bit 10 of 01FD46D4 clear (00226BD8)
                    for i in 0..63 (00307050..00307071): if flags & 1 { flags &= ~1 (00307061); 0026ADC0(3, i + 1) (00307063) }
```

`0026ADC0(index, value)` stores `value` as a ~~`u16`~~ 16-bit word *(corrected 2026-10-02, OPUS: the store carries no sign; the getter `00264D20` zero-extends it at `00264D3D`, and its consumer `00321190` sign-extends that result at `003211C2` `movsx ecx, ax`, so signedness is per reader)* into a 64-entry table reached through the pointer at
`02098E68` (`0026ADDD`), provided `index < 64` (`0026ADC0`), byte `02098E20` has bit 0 (`0026ADC5`)
and the pointer is non-null (`0026ADD5`). **So a completed group's number is posted into slot 3 of
that table, and the flag that requested it is cleared in the same frame.** The pointer is `+0x48` of
the ActorManager slot-0 record whose live bit is that byte
([the audio boundary](../../18-Audio/Audio-Boundary/how-a-sound-request-becomes-a-voice.md) §7:
`02098E20`, stride `0x288`, bit 0 = live). The table's other known reader is
`AiTargetSelector_ResolveOperandValue` (`00321190` → `00264D20`, same gate at `00264D25`, `movzx` of
the same table at `00264D3D`); ~~which script or operand reads slot 3 is `EE-9`~~ the zone script reads slot 3, by `waitv` on `scratch1` *(answered: see §8, `EE-9` 2026-09-18; 2026-10-02, OPUS)*.

**Bit 47 of the unit's first qword therefore means "this unit's group completion is waiting for its
death reaction to be handled."** Set at `0030700C`, cleared at `00306FC9` and `0030711A`, tested at
`0032519C` — and *nowhere else*: an immediate-operand sweep of every function body for
`0x0000800000000000` / `0xFFFF7FFFFFFFFFFF` and `bt* reg, 0x2F`, with the first two of those as
positive controls, returned exactly those four sites. Mode 1 skips the wait: the flag is raised in the
same call, and its event `0x2005` is routed by the reaction handler (`0032515E`) to
`BattleUnit_TryCommitEngageAutoAttack` (`00312FA0`), not to any death case.

> ### ⚠ The deferred route's consumer has no static route — found 2026-09-10, same day
>
> `00307110` has exactly one caller, `003250F0`, and **nothing in the image reaches `003250F0`**.
> Routes enumerated, each with a positive control: `E8` call and `E9` tail jump, and `LEA` in both
> encodings (`48`–`4F 8D` and bare `8D`), swept **linearly over all of `.text` without regard to
> function boundaries** (controls: the `lea` at `00265A4F` that takes `00233F70`'s address, and the
> `call` at `003251A4` that reaches `00307110`); 64-bit pointers anywhere in the file (control: the
> 27,392 `.rdata` slots this database already counts); 32-bit absolute and image-relative words
> (noise-prone, cited only as negatives). **Zero.** And the same is true of its two neighbours,
> `00325090` (86 B) and `BattleUnit_HandleActionTimelineEvent` (`00325260`, 1,215 B) — three adjacent
> `(actor, u16 *event)` handlers (`003250F0`, `00325090`, `00325260`) with ~~no caller of any form~~ **— REFUTED, see below —**, while the functions on either side of
> them (`00325060`, `00325080`) are reached by ordinary calls.
>
> **STRUCK AT THE POINT IT IS MADE, 2026-09-16 (FABLE), on `OPUS-REQ-FABLE-EE12-SIBLING-SENTENCE-KEPT-ON-PURPOSE`.** The correction was already eighteen lines below, and that was not good enough: **this is the judgement I overturned OPUS on the same morning** — their `UQ-1` repair struck the body sentences and left the heading stating the rejected figure, and I ruled that the first thing read has to carry the correction. It applies to my own sentence identically. **All three are reached**, and by the encoding the original sweep omitted: `002E7099 je → 00325090`, `002E70B0 jne → 003250F0`, `002E70C9 je → 00325260`, re-derived independently here with the `00392A05` conditional jump as a decode control. **One correction to the reading, on the same evidence:** the three sites are **not one if/else-if chain**. They lie in **three separate listed functions** — `002E7090`, `002E70A0` and `002E70C0` — each a small stub that tests and conditionally jumps to its own handler. That is the **same guard-stub shape** as `00392A00 → 00392A10` on the nine-patch page, which makes it a recurring idiom in this image rather than a local accident, and it is why a call-and-jmp census misses all four.
>
> What the presentation dispatch actually does is different from what a "handler" name suggests:
> `003299B0` writes the event to actor-work `+0xF0` (`002EB04D`, via `002EB030`), and `002EB0D0`
> passes it to `00427320` on the `0x740`-stride animation object at `*(022C6F28)` — **the animation
> layer consumes the event; no native handler is called with it.** If the animation layer ever
> calls back into `003250F0`, it does so through a pointer this image never materialises in code
> or data, which the evidence standard does not allow this page to assume.
>
> **~~So the static reading of arm B is: bit 47 is set, `0x2008` is played, and nothing observed~~
> ~~clears bit 47 or raises the ledger flag.~~** ~~Only mode-1 groups post their completion to slot 3.~~ *(corrected 2026-10-02, OPUS: arm B posts - `002EA4C5` registers the guard `002E70A0` in slot 0xC (`0041D6C0` stores `[02CA4410 + 0xC*8]` = `02CA4470`), the engine calls the slot at `0041DC9E`/`0041DD1D`/`0041CEE3`, `002E70B0` is `jne 003250F0`, and `003251A4` calls `00307110`, which clears bit 47 (`0030711A`) and sets the ledger flag (`00307133`); `EE-12`, §8)*
> ~~Whether the three handlers run at all is a runtime question — a breakpoint on `00325260` in any
> fight falsifies "dead" in one hit and its stack answers the route — filed as
> `FABLE-REQ-ASTRA-HANDLERS`, `EE-12`.~~ The route description above is kept because it is what the
> bytes of `003250F0` do *if* it runs; the two paragraphs before this box should be read with that
> caveat.

> ### The route was one opcode away, and it terminates — FABLE, 2026-09-16 (`EE-12`)
>
> **The box above is right that arm B never posts, and wrong that nothing reaches the three
> handlers.** The enumerated routes were `E8`, `E9` and both `LEA` encodings. **They omit
> `0F 8x rel32`, the conditional near jump**, and that is exactly how all three are reached:
>
> | | |
> | --- | --- |
> | `002E7099` | `je 00325090` |
> | `002E70B0` | `jne 003250F0` |
> | `002E70C9` | `je 00325260` |
>
> Each jump is the tail of a sixteen- to twenty-three-byte guard that tests `byte [actor+0x0D] & 1`.
> So *"with no caller of any form"* and *"a pointer this image never materialises in code or data"*
> are both false as written: **the pointer is materialised.** `0041D6C0(id, fn)` is fifteen bytes —
> `mov qword [02CA4410 + id*8], fn` — and the registrars pass **id 4 → `002E70C0`, id 6 →
> `002E7090`, id 0xC → `002E70A0`**, running from `BattleStorage_InitializeWorkArrays` and from the
> actor-system bootstrap `00266D10`.
>
> ~~**No reader of that table is found.**~~ **SUPERSEDED - see below.** A sweep of **every 4-byte rip-relative displacement anywhere
> in `.text`** — opcode-agnostic, boundary-free, so it sees the unlisted blocks too, controls
> `02B57EF0` and `0215FD70` returning seven real instructions each — finds **exactly two**
> references to `02CA4410` in the whole image: the clear at `0041CCA5` and the registration at
> `0041D6C3`.
>
> **And then the census of that table inverted my own reading, so it is recorded here rather than
> quietly dropped.** I first read *no reader* as *never dispatched*, on the strength of five
> registrations. **The table has thirty-four**: the ten from `002EA320` / `002EA5F0`, and **twenty-four
> more from `CharacterRenderSystem_Initialize`** (`00426A2B`–`00426B84`, the `00520xxx` band, among
> them `RelationLook_SetTrackingEnabled`). **Thirty-four handlers registered by a core render
> initialiser and never dispatched would be extraordinary**, and an instrument that has already
> failed a control once today is the likelier thing to be wrong. **So the reader is probably formed
> in a way a rip-relative sweep cannot see, and I have not found it.**
>
> **What survives is the refutation, not the inference.** The three `jcc`s are there and *"with no
> caller of any form"* is false. **What this box concluded about arm B is back to being a live
> question rather than a static one**: whether the arm posts depends on whether `02CA4410` is ever
> dispatched.
>
> **AND THE SECOND INSTRUMENT, RE-RUN WITH CONTROLS THAT WORK, GIVES SOMETHING BETTER THAN A ZERO.** The earlier stored-pointer scan was discarded because its controls returned zero. Re-run against two real `GameApplication` vtable slots, it works: `0017CC70` and `0079F9E0` appear in `.rdata`, in VA and RVA form. **And then the decisive control:** `01F000A0` — a base this engine demonstrably *does* dispatch through — also returns **0/0/0**. So *not stored* proves nothing on its own, because **bases in this engine travel by `lea`, not by being stored**. **Which gives the shape of the argument.** The worked example is complete: `CharacterRenderSystem_Initialize` does `lea rcx, [rip → 01F000A0]`, hands it to `0041D6E0`, which stores it at `02CA4668`; `PresentationAuthoredCommand_Class0B_SelectOrSwitchEmbeddedRecord` reads that slot and calls `[rax + idx*16 + 8]`. **So a table is dispatched here by being `lea`'d and then either indexed in place or passed out to a holder.** `02CA4410` is `lea`'d **exactly twice** — inside its own clear and inside its own registrar — and **neither passes it out**. **So two lines now point opposite ways and I am not picking between them:** the mechanism argument says nothing can dispatch `02CA4410`, and the plausibility argument says thirty-four handlers from a core initialiser are unlikely to be dead. **That is exactly what a read watchpoint on `02CA4410` settles**, and it is why the runtime request was re-scoped onto it rather than withdrawn.
>
> **The one hole, and the runtime request is re-scoped onto it rather than withdrawn.** A dispatcher
> forming the table address other than rip-relative — a base carried in a register, or computed —
> would be invisible to that sweep. So the live check is a **read watchpoint on `02CA4410`**, not a
> breakpoint on `00325260`: the latter would only confirm the static route, and could fail to fire
> for a reason unrelated to the question, since it sits behind a bit set on a minority of
> standard-motion starts.
>
> *A second instrument was tried and is not counted:* a stored-pointer scan for `02CA4410`, whose
> **controls also returned zero** and which therefore discriminates nothing.

`SpawnGroup_HasPendingCompletionSignal` (`003070E0`) is the read side of the same flag — true if any
of the 64 entries has bit 0 (`003070F0`, walked `02EC13D0`→`02EC19D0` at `+0x18`) — and its one
caller, the unit frame at `00234095`, sets bit 1 of `02089340` when **nothing** is pending
(`0023409E or [02089340], 2`).

### The three prologue calls — `EE-5` answered at the write level

All three run before either arm, each with the literal `1` (`00306F95`, `00306F9F`, `00306FA9`):

| call | what `(1)` writes | `(0)` |
|---|---|---|
| `00307140` (183 B) | selects `002E1C20` over `002E1CA0` (`0030715C cmovne`) and calls it ten times with `(12, n)`, `n ∈ {0, 3, 4, 5, 6, 7, 8, 11, 12, 20}` (`00307162`–`003071BE`): `row[12] \|= 1 << n` in the 16-row capability-inhibition table at `0215F1C0` (`002E1C3C`; the clearing twin at `002E1CBE`). Then `PartyControl_SetMovementSuppressionBit` (`00359200`) with `(arg, 2)` at `003071C7`, `PartyControl_SetSuppressionMaskByteBit` (`00359330`) with `(2, 1, arg)` at `003071D7` — neither body read here — and a tail call `0026BD20(2, arg == 0)` → `byte 0209A2C4[2] = 0` (`0026BD2F`) | the same ten bits cleared; the byte set to `1` |
| `00238B70` (120 B) | `02089340 = (02089340 & ~0x20) \| 0x20` (`00238B80`–`00238B90`); then for every battle-unit slot `i < [0208E6A0]` in the array at `[0208E688]`, stride `0xF50`, whose first byte has `0x10` (`00238BB0`): `002E7C10(unit->p_10, unit->p_10, 0x30B, 0)` (`00238BC5`) | bit `0x20` cleared, same loop |
| `00238AE0` (29 B) | `02089340 = (02089340 & ~0x80) \| 0x80` (`00238AEA`–`00238AF6`) | bit `0x80` cleared |

So completion **raises ten capability inhibitions in row 12, suppresses party movement, and sets
bits `0x20` and `0x80` of the battle-state word** — the shape of an event lock, consistent with the
verb's catalog name *EventFlagGroup*. What each row-12 bit inhibits
([the capability policy](../../15-Input/Gameplay-Capability-Policy/capability-inhibition-policy.md)
documents rows 1 and 2 only) and what message `0x30B` is to `002E7C10` are not established here
(`EE-7`, `EE-8`). All three have other callers (`0026C5D0`; `00359A30`, `0035A6F0`, `0035AB20`), so
they are shared event-lock primitives, not group-specific.

## 5b. From the script that names a group to the script that wakes when it dies *(synthesis, 2026-09-18, FABLE)*

*No new reading. Sections 4, 5 and 8 answer this in pieces; this is the whole loop in order, for someone who has to
reproduce it, with the place each step is evidenced.*

| step | what happens | evidence |
|---|---|---|
| 1. authoring | Every spawned unit's entry function runs a fixed preamble that includes `btlAtelSetEventFlagGroup(group, mode)`, right after the level is set. Of 6,746 shipped calls, 6,206 are `(0, 0)`: **group 0 is "no event group"**, and only groups 1 to 5 mean anything downstream. | section 4 (`EE-11`); section 8 (`EE-9`) |
| 2. who counts | Only a unit built from the **enemy definition table** is entered in the ledger or can complete a group; party members, guests and Espers are outside it whatever group a script gave them. | section 8 (`UQ-99`) |
| 3. the ledger | Per group: a member mask filled as units register, a dead mask set bit by bit as they die, and flags. Completion is *every expected bit is set*, not a count, so a repeated or foreign death changes nothing. | sections 4 and 5 |
| 4. the hold | A completed group is not announced at once. The dispatcher waits while any of four party-down states holds, while time-stop request 10 is raised (a time-stop spell, or the player choosing a target), and announces on the first frame none does. | section 8 (`EE-9`, the blockers) |
| 5. the post | The announcement is one store: the group's number into `u16` slot 3 of the actor manager's 64-word table - which is the script VM's `scratch1` bank, so to a script it is the variable `scratch1 short @0x06`. | sections 5 and 8 (`EE-9`) |
| 6. the wake | 239 shipped scripts import that variable and 236 of them are parked on it with `waitv`, which waits while it is zero. The woken script runs the aftermath - close the boss gauge, suspend battle, play the quest effect, advance the hunt's flags (the sampled hunt script) - and some scripts assign the variable themselves to re-arm it. | section 8 (`EE-9`) |
| 7. the side effects | On completion every flagged unit's own render record also receives a type-3 relation-look event and has its `+0x24C` cleared; the message id the call carries is dead. | section 8 (`EE-7`) |
| 8. forgetting | `scratch1` is cleared on every field transition, so an announcement nobody was waiting for is gone when the player leaves; the respawn clock of section 3 is separate and runs in seconds of play. | [the storage-class page](../../01-Script-VM-Native-Bridge/Interpreter-Core/script-variables-and-their-storage-classes.md); section 3 |

**For a reimplementation, and for a shared-world mod in particular.** The contract between engine and script is
one non-zero word appearing in `scratch1 @0x06` *after* the hold of step 4. Post it early - while a character is
down or a target cursor is open - and the aftermath script runs over a state it was written never to see; post 0
and nothing wakes. *Reading, not evidence:* because the word lives in a bank every client clears on zoning and every client's script waits on
locally, two machines agree on an encounter's end only if both ledgers reach completion; the word itself is not
something to replicate.

**Still not known:** whether the three posting functions for groups whose mode is not 1 ever run (~~`EE-12`, a live
question~~ `EE-12` is ANSWERED: see [the contract](../CONTRACT-group-completion-and-respawn.md) §14, whose EE-12 handlers were verified ~~live~~ statically, by the slot registration and the engine's `call rax` sites; no live verification is recorded *(corrected 2026-10-02, OPUS: `002EA4C5`, `0041DC9E`/`0041DD1D`/`0041CEE3`)*), and the reset forms of the respawn clock beyond section 3.

## 5c. After the death: when the body goes, and when its slot is freed *(FABLE, Claude Opus 5.5, 2026-09-29)*

Evidence: [`pkg-gp-spawn-respawn`](../../_index/candidates/pkg-gp-spawn-respawn/README.md) `teardown.py` G, K and R, FAILS 0, static.
The addresses are in the record; this section names each step by its role.

1. **Told to die.** On the death events (`0x2007` / `0x2008` / `0x200C` / `0x200E`), the reaction handler sets the unit's flag
   bit 33 (§5).
2. **The animation reaches its point.** The unit's actor-timeline handler sets flag bit 34 on timeline event kind 6, and on
   kind 4 unless the field's bit forbids it. ~~What posts those kinds is not read here.~~ *(Replaced 2026-09-29, FABLE,
   teardown.py P, T and U.)* **Both kinds come from authored action tracks.** Every post into that handler comes from two
   places:
   - the action-timeline interpreter
     ([§12 of the ownerless-functions page](../../00-Engine-Core-Runtime/Ownership-Boundary/intentionally-ownerless-functions-and-shared-scratch.md));
   - one other walker, which posts only kinds 0 and 1.

   In the interpreter:
   - an opcode-26 entry posts kind 6 when its dword `+4` is 1 (0, 2 and 3 give kinds 3, 7 and 8);
   - an opcode-37 entry posts kind 4.

   Both post to the **acting unit** of the current action, and the bit is set on that unit's record. So a body is released
   when an action track played by the dying unit reaches one of those entries.

   **Not established:** which tracks carry these entries (a data census of the per-action tracks), and whether any other code
   sets bit 34 (no image-wide writer census was run).
3. **Torn down in the idle path of the per-unit frame**
   ([the world tick](../../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md), the IDLE branch).
   The teardown runs only when all three hold:
   - bit 33 is set;
   - bit 34 is set;
   - the unit's presentation handle is missing, or its encoded-id class state is below 3.

   While that state is 3 or more, the body stays. Which presentation that handle names, and what the states mean, is not
   claimed.
4. **The slot is freed later, and elsewhere.** The routine that releases the unit's slot (and marks the keep entry released)
   has one caller: the actor system's release of its manager records. There it runs for an actor record whose byte `+0x14` is
   at least `0x80` and that has a bound unit. So death tears the body down, and the slot goes back to the pool when the actor
   records are released, not at the kill.

## 6. Key addresses

| address | size | what |
|---|---:|---|
| `00306F00` | 303 B | `SpawnGroup_RecordMemberDeathAndHandleCompletion` |
| `00307090` | 73 B | `SpawnGroup_ResetLifecycleLedger` — 64 entries, four unrolled per iteration |
| `00235F50` | 93 B | `SpawnEntry_GetDeathCount` → `u16` at `+0x08` |
| `00235FB0` | 121 B | elapsed **seconds** since last death — **name corrected**, §3 |
| `002366E0` | 93 B | `SpawnEntry_GetRespawnCooldownTicks` → `u16` at `+0x10` |
| `002360D0` | 39 B | `SpawnLaneMap_ResolveBkeiIndex` |
| `0031B760` | 13 B | `ActorWork_GetBattleUnit` |
| `0032A150` | 7 B | `GameClock_GetRawTickCounter` → `*(u32*)0x0208D45C` |
| `003299B0` | 83 B | `BattleUnit_DispatchActorPresentationEvent` |
| `00306E60` | 158 B | `SpawnGroup_UpdateExpectedMemberLaneMask` — **the `memberMask` writer**, add/remove one slot, always clears the dead bit |
| `00239710` | 114 B | `SpawnGroup_ConfigureUnitMembershipAndMode` — writes `+0xE98`/`+0xE99`, then adds; native side of verb `0x3030` |
| `0050F8C0` | 67 B | `VM_SpawnGroup_ConfigureUnitMembershipAndMode` — verb `0x3030` `btlAtelSetEventFlagGroup`, two int pops |
| `00307030` | 82 B | `SpawnGroup_DispatchPendingCompletionSignals` — per frame: clear each pending flag, post the group to table slot 3 |
| `003070E0` | 39 B | `SpawnGroup_HasPendingCompletionSignal` — any flag bit 0 set |
| `00307110` | 40 B | `SpawnGroup_MarkCompletionPendingAfterReaction` — clear bit 47, set the flag |
| `00307140` | 183 B | event lock: capability row 12 bits, party suppression, `0209A2C4[2]` |
| `00238B70` | 120 B | `02089340` bit `0x20`, then `002E7C10(…, 0x30B, 0)` per flagged unit |
| `00238AE0` | 29 B | `02089340` bit `0x80` |
| `0026ADC0` | 35 B | `table[index] = (u16)value` through `02098E68`, gated on `02098E20` bit 0 |
| `00233D20` | 47 B | the dispatch gate: `02089340 & 0xF00` clear and bit 10 of `01FD46D4` clear |
| `00300530` | 880 B | `BattleStats_ModifyHPAndProcessLethalState` — the death handler's only caller; writes `+0x08`/`+0x0C` |
| `002350C0` | 529 B | `SpawnLifecycle_CheckAndRetireByNativeRange` — the `remove` caller |
| `003250F0` | 279 B | `BattleUnit_HandleReactionAnimationEvent` — routes `0x2007/0x2008/0x200C/0x200E` to `00307110` |

### Data

| address | what |
|---|---|
| `0x02EC13C0` | the ledger, **64 × 24 bytes**, BSS; addressed by exactly six functions (from-entry scan, control positive) |
| `0x0208E690` | pointer to the spawn-record array, stride `0x250` |
| `0x0208D45C` | the raw frame counter |
| `0x01DFE0B8` | frame-rate scale, `1.0f` / `2.0f` |
| `0x008F8D80` | `30.0f` |
| `0x02098E68` | pointer to a 64-entry `u16` table; slot 3 receives the completed group's number |
| `0x02098E20` | ActorManager slot-0 flag byte; bit 0 gates the table write |
| `0x02089340` | battle-state word; completion sets `0x20` and `0x80`, dispatch needs `0xF00` clear, "nothing pending" sets `0x2` |
| `0x0215F1C0` | the 16-row capability-inhibition table; completion sets ten bits of row 12 |
| `0x01FD46D4` | the time-stop registry's active-request bitset; **bit 10 = request id 10** — `settimestopmagic` or the target-selection cursor ([the time-stop registry](../../00-Engine-Core-Runtime/System-Stop-Registry/the-time-stop-and-system-stop-registry.md) §6) — blocks signal dispatch |

### Fields

| offset | on | meaning |
|---|---|---|
| `+0x08`, `+0x0C`, `+0x10` | spawn record | death count · last-death **second** · respawn cooldown; the first two written at `00300801`/`00300829` |
| `+0x40` | battle unit | the lane map: `[0]` count, then one slot byte per lane, `0xFF` = empty |
| `+0x698` | battle unit | the spawn record `+0x80`; byte `+0x05` (record `+0x85`) must be `1` |
| `+0x6A0` | battle unit | the spawn record itself; `00300530` bumps `+0x08`/`+0x0C` through it |
| `+0xE98` | battle unit | **1-based group id**; `0` disables the whole path; **written only at `00239746`** |
| `+0xE99` | battle unit | mode bits, written only at `00239766`: bit 0 = `mode == 1` (immediate arm), bit 1 = `mode == 2` (teardown skips two calls) |
| `+0x00` | battle unit | bit 47 = completion signal deferred until the death reaction is handled; bit 33 set by the reaction handler on the same case |

## 7. Modding notes

- **To make a group complete, set its `deadMask` bits, not a counter.** Nothing counts deaths for
  completion; `+0x08` is a separate statistic.
- **A group with `memberMask == 0` completes on the very first death.** Since the table is BSS, that
  is the state before anything populates it.
- **`+0xE98` is 1-based.** Group `0` means *no group*, and the death is recorded nowhere.
- **Respawn waits are in seconds and already frame-rate corrected.** Do not scale them again.
- **Only 64 groups and 64 members per group exist.** Both are hard structural limits — a `u64` mask
  and a 1,536-byte table. **In practice keep a group's slots below 31**: slot 31 registers and kills
  bits 31–63 together, and slots ≥ 32 alias onto `slot & 31` in both writers.
- **To put an enemy in a group, its script calls `btlAtelSetEventFlagGroup(group, mode)`** —
  verb `0x3030` — with `group` 1–64. Nothing else registers members, and the registration is redone
  on every area entry because the reset empties the ledger. `mode == 1` posts the completion at once
  with event `0x2005`; any other mode plays the death reaction (`0x2008`) first and posts when it has
  been handled; `mode == 2` additionally skips two calls during the unit's teardown.
- **To make a member stop counting without killing it, unregister it** — `00306E60(unit, 0)` — which
  is what range retirement does. It also clears the member's dead bit.
- **To observe completion natively, watch the flag byte or the table write**: ledger `+0x10` bit 0 is
  raised on completion and consumed by `00307030` in the next field frame, which writes the group
  number to `u16` slot 3 of the table at `*(0x02098E68)`. A hook on `0026ADC0` with `index == 3` sees
  every completion the field script sees.
- **Completion locks the party.** Ten row-12 capability bits, movement suppression and two bits of
  `02089340` are set by the three prologue calls; a mod that raises its own completion must also
  release them (the `(0)` forms) or the party stays locked.

## 8. What is not known

- [x] ~~**Whether `+0x10`'s cooldown is in seconds**, matching `00235FB0`'s output. The two are never
  seen compared here, and `+0x10` is not seen written here either.~~ **`EE-1` ANSWERED 2026-09-13 (FABLE):** **yes — ~~the only consumer~~ the script consumer compares it with the elapsed seconds.** *(corrected 2026-10-02, OPUS: `Spawn_SelectAndPrepareAutomaticEntry` compares it too, below)* In the 1,114 decompiled `us` scripts, `btlAtelGetRespawnTime` (`0x304A`, reading `+0x10` through `002366E0`) is called **1,765** times in 285 files, and **every call is the right-hand side of `btlAtelGetElapseTime(i) > btlAtelGetRespawnTime(i)`** for the same entry `i` (`0x3036`, `00235FB0`, whole seconds), in a condition `(… > … || btlAtelGetDeadCountNow(i) == 0)` (1,737) or `(… > … || btlAtelGetRespawnCause() == −1)` (28). So the authored cooldown is consumed as a whole number of seconds, compared strictly (a respawn needs elapsed seconds **greater** than the cooldown), and by script~~, not native code~~ *(corrected 2026-10-02, OPUS: and natively - `Spawn_SelectAndPrepareAutomaticEntry` skips while elapsed < cooldown, `002358D1`–`002358D7` `sub`/`cmp`/`jb`, so it re-admits at elapsed ≥ cooldown; the contract's 2026-09-29 correction)*; an entry that has never had a death passes regardless.
- [x] ~~**What writes `memberMask`**, and when relative to the first death.~~ `00306E60`, from each
  member's script through verb `0x3030`; range retirement removes. `EE-2` **answered 2026-09-10**.
- [x] ~~**What distinguishes the `0x2005` and `0x2008` completion arms**, and what sets `+0xE99` bit 0.~~
  The verb's mode argument; both arms converge on the ledger flag. `EE-3` **answered 2026-09-10**.
- [x] ~~**What bit 47 of the unit's first qword means**~~ — completion signal deferred until the death
  reaction is handled; four sites in the whole image. `EE-4` **answered 2026-09-10**.
- [x] ~~`00307140`, `00238B70`, `00238AE0`, all called with the constant `1` on completion.~~ Read at the
  write level: capability row 12, party suppression, `02089340` bits. `EE-5` **answered 2026-09-10**;
  what the bits *inhibit* is `EE-8`.
- [x] **UQ-99.** *(answered 2026-09-18, at the end of this item)* What the kind gate `[+0x698]+0x05 == 1` selects. It is the authored record kind byte of
  [the battle-record kind byte](../../04-Actor-Entity/Battle-Record-Kind/battle-record-kind-byte.md),
  which stops at "two kinds, type-keyed and owner-keyed"; in this family every ledger access and the
  spawn-record statistics are behind it. `EE-6` — **partially answered**, the meaning is that
  document's `AL` question.
  **ANSWERED 2026-09-18 (FABLE), by propagation: it selects units built from the enemy definition table.** The meaning this box was waiting on was settled on [the kind-byte page](../../04-Actor-Entity/Battle-Record-Kind/battle-record-kind-byte.md) as `AL-1` on 2026-09-10 and never carried back here: the byte is the high byte of the encoded definition id, **0 = the party table** (the forty rows of player characters, guests, the chocobo and the thirteen Espers, `AL-2`) and **1 = the enemy table**. So in this family the gate means: **only enemy-table units are entered in the group ledger, can complete a group by dying, and feed the spawn-record statistics**; a party member, a guest or an Esper falling is outside the mechanism altogether, whatever group number a script may have given it. Static, on that page's evidence; nothing new was read for this box.
- [x] ~~**What message `0x30B` is to `002E7C10`**, sent to every battle unit with flag `0x10` on
  completion.~~ **`EE-7` ANSWERED 2026-09-11 (FABLE): it is nothing — the argument is dead.**
  `00238B70` is `002E7C10`'s only caller on the call graph and passes the unit's actor work as
  *both* first and second argument with `r8d = 0x30B`, `r9d = 0` (`00238BB6`–`00238BC5`);
  `002E7C10` resolves the actor's render record and the controller's first dword and tail-jumps
  `003E6C10(record, controllerHandle, 0x30B, 0)` (`002E7C2B`–`002E7C62`), and **`003E6C10` never
  reads its third argument** (`r8` is untouched in its 169 bytes). What the call does per flagged
  unit: when the record's `+0x18` resource resolves (`003E6C2B`–`003E6C66`) it builds a 16-byte
  event `{u16 type = 3, +4 recordIndex, +8 recordIndex, +0xC controllerHandle}` and hands it to
  `RelationLook_ApplyRelationEvent` `00512F30` on the record's `+0x650` (`003E6C68`–`003E6C8A`);
  then, because `r9d = 0`, it stores `−1` at the record's `+0x24C` (`003E6C8F`–`003E6C98`). So
  completion posts a type-3 relation-look event for every flagged unit's own record and clears
  `+0x24C`; what the relation-look applier does with a type-3 event whose two indices are the same
  record is its page's business. *(Corrected 2026-09-13, `OPUS-CONTRA-RELATION-WALK`: this said the
  applier "matches the event against a 32-entry table at `02CA81F0`, `00512F53`–`00512F8A`". Those
  instructions walk one owner's linked list — head `[r11 + 0xC]`, next `+0xE`, `0xFF`-terminated —
  through the 32 × 16-byte pool whose size the initialiser `00512EF0` fixes (`00512F10`–`00512F1F`);
  and **a type-3 event never reaches them**: the applier branches on the event's first byte before the
  walk (`00512F3C`–`00512F4D`), and type 3 goes to `005130CB`. There, with `+1` clear (the builder
  stores a `u16` 3, `003E6C7F`), it compares the event's `+8` (the record's own index) with `+0xC` (the
  controller handle): equal clears the owner's kind nibble `+0xF & 0xF0` (`00513110`); otherwise it
  copies `+4`/`+8`/`+0xC` into the owner's `+0`/`+4`/`+8` and sets the nibble to 3 (`005130D9`–`005130F3`).
  So completion writes the unit's inline relation slot and touches no pool record. The EE-7 answer
  does not use the table reading anywhere else.)*
- [x] ~~**What the ten row-12 capability bits and `0209A2C4[2]` inhibit**, and what `02089340` bits
  `0x20`, `0x80` and `0x2` gate downstream.~~ **`EE-8` ANSWERED 2026-09-12 (FABLE), with two bits
  left as residue.**
  - **Row-12 bits.** A row's bits act only through the OR-reduced aggregate (`002E0FA0`, 29 call
    sites read whole). Through [the capability policy](../../15-Input/Gameplay-Capability-Policy/capability-inhibition-policy.md)'s
    UI projection table (`01E0C2C0`, `00254500`), completion's set `{0, 3, 4, 5, 6, 7, 8, 11, 12, 20}`
    inhibits **UI requests 2 (bits 0, 3), 5 (bit 5), 14 (bit 6) and 1 + 21 (bit 8)** — the Party
    Menu, free-target cycling, the Battle Menu and two unnamed slots. The bits with no UI
    projection are consumed directly: **bit 4** (`0x10`) by the menu functions `002736B0`,
    `00273950`, `002C64C0` (interior read 2026-09-17, SWE2-FRONTIER: 1,248 B — `002647D0` first at [`002C6524`](../../_index/ADDRESS-INDEX.md), `003DF6F0`/`0028F5B0` ×2); bits **7, 11, 12, 20** reach no direct test at any of the 29 sites — they
    are visible only to the callers that test the aggregate against a mask of their own
    (`00252B60`, `003C8B70`), which is the residue. (Interior read 2026-09-17, SWE2-FRONTIER:
    `003C8B70` is a thrice-repeated eight-call sequence — `00249C60` sound-play wrapper →
    `0035D060` → `002470C0` → `0035C080` → `0028FFE0` → `00252D90` → `002E1CA0` → `0035C150`,
    first block at [`003C8C42`](../../_index/ADDRESS-INDEX.md) — consistent with a per-member
    announce/state pass; `003C9250` ×4 frame it.) (The direct tests at the 29 sites are bits 0 —
    the three UI-request mailbox functions `002E1A60` / `002E1B10` / `002E25B0` — 4, 10, 18 and 21.)
  - **`0209A2C4[2]`** is one of **four party-movement suppression bytes `0209A2C4`–`0209A2C7`** that
    the party-follow gate `0026DFB0` reads together (`0026E01F`–`0026E044`) after resolving the focus
    actor: any non-zero byte stops the followers' tick. Completion's byte 2 is therefore one of
    four independent suppressors of party following (the others are written by `0025AAD0`,
    `0025D650`, `00266D10`, `00268D10`, `0026BC60`, `0026BD40`).
  - **`02089340` bit `0x20`** gates party following directly: `PartyFollow_ApplyGoal` (`003246C0`)
    and `0033D890` test it (`test byte, 0x20`). **Bit `0x80`** is part of the global target-eligibility
    mask: `BattleTarget_ComputeGlobalEligibilityMask` tests `0x3080` (bits 7, 12, 13) on the word
    (`0030B78C`), so completion makes targets ineligible while set; `00238AE0` is its clearer
    (`btr eax, 7`). **Bit `0x2`** has no direct test on any enumerated route (the orchestrator tests
    bits 2, 8, 9; `PartyControl_RecomputeSuppression…` tests `0x600`; the `0050F1xx` family bits 23,
    26, 29) — residue.
- [x] **EE-9.** *(answered 2026-09-18, at the end of this item)* **Who reads slot 3 of the table at `*(02098E68)`** — the consumer of the posted group number.
  ~~and what `01FD46D4` bit 10 and `02089340 & 0xF00` represent as dispatch blockers.~~ *The blockers are
  answered 2026-09-12 (FABLE):* `02089340 & 0xF00` are the battle-state word's four party-down states — the
  focus actor down, every active member incapacitated, the whole roster down, the leader down
  ([the world tick](../../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md) §2.5) — and
  `01FD46D4` bit 10 is **time-stop request id 10**, raised by `settimestopmagic` and by the target-selection
  cursor `00313DB0` ([the time-stop registry](../../00-Engine-Core-Runtime/System-Stop-Registry/the-time-stop-and-system-stop-registry.md)).
  So a wiped group does not post its completion while the party is down, a time-stop is active or the player
  is choosing a target; it posts on the first frame none holds. `EE-9`.
  **ANSWERED 2026-09-18 (FABLE): the zone script reads it, by sleeping on it.** The 64-entry table is the script VM's `scratch1` bank ([the storage-class page](../../01-Script-VM-Native-Bridge/Interpreter-Core/script-variables-and-their-storage-classes.md), class 4, the static bank at `02099DF0` that every field transition clears), so `u16` slot 3 is the script variable `scratch1 short` at byte offset `0x06`. *Native side:* the table pointer has exactly two references in the image, the setter `0026ADC0` and the getter `00264D20`, and the getter's one caller is arm 1 of the AI operand resolver - OPUS's structural half on [the actor record page](../../04-Actor-Entity/Actor-Storage-Record/the-record-behind-every-actor.md) - for which the gambit page's shipped census lists scratch word 1 and no word 3. *Script side, from the 1,114 decompiled `us` scripts:* `import scratch1 short ... = 0x06` is the **most imported scratch variable in the game, 239 scripts**, and **236 of them call `waitv(&var)` on it**. `waitv` (verb 5) re-reads the variable each poll and keeps waiting while it is zero (`00354275`..`00354296`: load by width, `test`, `sete`), so the script parks until the engine posts a non-zero group number. What follows the wait is the encounter's aftermath - in `asp_b03` the mark's victory sequence: close the boss gauge, suspend battle, play the quest effect, advance the hunt's flags. The other uses are assignments (scripts re-arm it), a few comparisons and `switch` statements on the posted number. **So the posted group number is the rendezvous between native group completion and the authored script that was waiting for that fight to end**, and because the bank is `scratch1` the signal does not survive leaving the field. *Group 0 is the quiet default, by authoring:* of the 6,746 shipped `btlAtelSetEventFlagGroup(group, mode)` calls, 6,206 are `(0, 0)` and the rest use groups 1 to 5 (group 1 alone 525), so nine units in ten belong to a group whose number, if posted, is a zero `waitv` cannot see - only the evented groups wake a script. Static for the accessors and the poll; authored-data census for the use.
- [x] ~~**What `0025AB30` and `002697E0` do in teardown**, the two calls mode bit 1 skips.~~ **`EE-10`
  ANSWERED 2026-09-11 (FABLE):** both take the unit's actor work (`+0x10`). `0025AB30` is the actor's
  **per-type presentation release**: it dispatches on the actor's type byte `+4` — type 1 →
  `002E3AF0` (`002E6BD0(actor, 0, 0)`, `0025D4F0`, `0025D690`, then the controller's render
  record, `002E3B08`–`002E3B58`), type 2 → `003DE5F0` (frees the `0x70`-byte slot at
  `02958C50 + byte(+5) × 0x70` through `003ABCA0` and zeroes it), type 3 → `002E3D00` (releases the
  controller's `+0x138` node through `003DAD00` and nulls it) — and then writes the word `+4` as
  `0xFF00`: type 0, slot `0xFF` (`0025AB3A`–`0025AB9B`). `002697E0` is `00269860(actor, 0)`: when the
  byte at `02099DE1` is set, it takes the actor's `+0x15` slot into the `0x288`-stride table at
  `02098E10`, requires flag `+0x1C` bit 14 (bit 7 in mode 1) and, unless `+0x18 == 1`, resolves a
  word from the table row to an index and calls `003DBB60(actor, 2, index, 0)` before `00269640(actor)`
  (`0026986F`–`002699BB`) — the render-side detach. Mode 2 skips both, so a mode-2 unit's actor
  keeps its type byte and its render-side slot through the despawn.
- [x] ~~**The script-side argument order of `btlAtelSetEventFlagGroup`** and where authored scripts
  place the call — a decompiled shipped script would settle both. `EE-11`.~~ **ANSWERED 2026-09-13 (FABLE), observed in
  the shipped scripts:** 6,746 calls in 502 of the 1,114 decompiled `us` scripts, each in a `spawnGroup` entry function
  right after `btlAtelSetLevel`, inside the fixed authored preamble. *(Ticked 2026-09-14, FABLE: the register's `EE-11` verdict answers this box; the page box had been left open.)*
- [x] **EE-12.** ***ANSWERED 2026-09-19 (FABLE): all three run, and none needs a breakpoint to show it.** The command stream is an `@FMC` block of the character's `.ca` animation container; parsed out of every block in the game (62,208 blocks, 2,348,027 commands, no structural failure) class `0x04` is authored 27,631 times in attack / magic / item / ability blocks and its invoker routes subtypes 0 to 9 - 20,392 commands - to `002E70C0` -> `00325260`; class `0x06` is authored 7,008 times -> `002E7090` -> `00325090`; and id `0x0C` is not a command class at all - nothing authors it, and slot `02CA4470` is called by the engine when a track ends or is switched (~~`0041DC84`, `0041DD03`, `0041CEC0`~~ `call rax` at `0041DC9E`, `0041DD1D`, `0041CEE3` *(corrected 2026-10-02, OPUS: the struck sites are the two `mov rax, [02CA4470]` loads and the entry of `0041CEC0`, whose load is at `0041CEC6`)*), so `003250F0` is the unit being told its animation finished. [Where the commands are authored](../../17-Presentation-Rendering/Authored-Commands/the-authored-presentation-command-handlers.md). The runtime request is withdrawn; a live session could add confirmation, not discovery.* ~~**Whether `003250F0`, `00325090` and `00325260` ever run.**~~ ~~No static route of any enumerated~~
  ~~form reaches them; if they are dead, mode ≠ 1 groups never post their completion.~~ *(corrected 2026-10-02, OPUS: they run and mode ≠ 1 groups post - `002EA4C5` registers the guard `002E70A0` in slot 0xC (`0041D6C0` stores `[02CA4410 + 0xC*8]` = `02CA4470`), the engine calls the slot at `0041DC9E`/`0041DD1D`/`0041CEE3`, `002E70B0` is `jne 003250F0`, and `003251A4` calls `00307110`)* `EE-12`.

      **THE STATIC HALF IS NOW CLOSED TO A HIGHER STANDARD 2026-09-13 (OPUS), AND THE CLAIM
      SURVIVES.** *"No static route of any enumerated form"* was worth re-testing precisely because
      it is the kind of absence this database has been wrong about before. **Four routes, each with a
      control:**

      | route tested | `003250F0` | `00325090` | `00325260` |
      |---|---|---|---|
      | direct `call` / `jmp` in `.text` | **0** | **0** | **0** |
      | the 64-bit pointer value anywhere in the file | **0** | **0** | **0** |
      | `lea` taking the address | **0** | **0** | **0** |
      | the 32-bit **RVA** in any table | `.pdata` ×1 | `.pdata` ×1 | `.pdata` ×1, `.rdata` ×2 |

      **Control:** the same RVA sweep run against `002650E8` — a target of the jump table at
      `00265180` — finds its single `.text` occurrence, so the method does see real dispatch tables.

      **The `.rdata` hits are an exception-handling scope table, not a dispatch table**, and they are
      **banned evidence** either way. The records around `01D76870` are four dwords —
      `{00325260, 003254D8, 01D52A2C, int}` — and **`003254D8` lies inside `00325260`** itself
      (`00325260`–`0032571F`): a begin/handler pair with a type pointer, which is the shape of a C++
      EH scope record, not a callable target. **Nothing in `.text` references that `.rdata` block at
      all** — `0 of 13` addresses across `01D76840`–`01D768A0` — so it is read by the runtime
      unwinder, never indexed by game code.

      > **AND THE EVIDENCE STANDARD CUTS BOTH WAYS HERE.** `.pdata`, `.xdata` and EH maps are banned
      > as support (pass 6). That ban is usually invoked to stop someone *proving* a claim from
      > unwind data; it applies identically in reverse — **these entries cannot be used to argue the
      > three functions are reachable.** Finding them and dismissing them is the whole result.

      ~~**The box stays open, and it must.**~~ *Superseded 2026-09-26 (FABLE): `EE-12` was answered on 2026-09-19. All
      three run: they are authored as `@FMC` commands in the characters' `.ca` animation containers, parsed out of every
      block in the game ([the authored presentation command handlers](../../17-Presentation-Rendering/Authored-Commands/the-authored-presentation-command-handlers.md)).
      The rest of this box is the reasoning as it stood before that.* EE-12 asks whether they *ever run*, which no static sweep
      can answer: an indirect call through a computed address remains possible, and only ASTRA can
      observe the negative. **What changed is that "no static route" is now a measured negative with
      four routes and a control behind it, rather than a search that did not find one.**

## 9. Evidence

| claim | evidence | tier | confidence |
|---|---|---|---|
| `memberMask` carries the members before the first death; `deadMask`, `flags` and slot 3 are 0 then | ASTRA EXP-019, one loaded save, read-only, with executable/full-text and pool/read controls | live | OBSERVED (one save, pre-kill only) |
| The shared 7-check accessor prologue | three bodies disassembled and compared instruction for instruction | 1 | PROVEN |
| Record stride `0x250`, base from `0x0208E690` | `imul rcx, rax, 0x250` + `add rcx, [rip]` in all three | 1 | PROVEN |
| `00235FB0` returns **seconds** | `GameClock_GetRawTickCounter` divided by `(int)(scale × 30.0f)`, both constants read from their RIP targets | 1 | PROVEN |
| Ledger is 64 × 24 bytes at `0x02EC13C0` | reset loop bounds `02EC13D0`–`02EC19D0` with a `0x10` bias, against the death handler's × 24 index; 1,536 / 24 = exactly 64 | 1 | PROVEN |
| The ledger is BSS | its `.data` offset exceeds `SizeOfRawData` — checked, not assumed | 1 | PROVEN |
| Completion is `(member & dead) == member` | `and`/`cmp`/`je` at `00306F7C`–`00306F86` | 1 | PROVEN |
| The two arms and their event codes | `0x2005` / `0x2008` into `003299B0`, with the bit-47 mask literals | 1 | PROVEN |
| Whether `+0x10` is seconds | ~~**not established**~~ yes, whole seconds - `EE-1` 2026-09-13, and the selector compares it with seconds natively (`002357F9` divide, `002358D7` `jb`) *(answered: see §8; 2026-10-02, OPUS)* | ~~—~~ 1 + authored-data census | ~~UNKNOWN~~ PROVEN |
| `00306E60` writes `memberMask`, add or remove by slot, and always clears the dead bit | `00306ED4`–`00306EEA` read from the image; same gates and slot resolution as `00306F00` | 1 | PROVEN |
| Exactly six functions address the ledger | from-entry scan of 34,270 bodies over `02EC13C0`–`02EC19C0`, both addressing forms; control `02089340` = 126 | 1 | PROVEN |
| `+0xE98`/`+0xE99` have one byte writer, `00239710` | from-entry displacement sweep, control `00239746`; the one other `+0xE98` write is a qword in an unrelated zeroing run | 1 | PROVEN |
| `00239710` is the native side of verb `0x3030` `btlAtelSetEventFlagGroup` | sole caller `0050F8C0`; verb table row `3030`; two `call 0x267E10` then `jmp 0x239710` | 1 | PROVEN |
| Mode bit 0 = `mode == 1`, bit 1 = `mode == 2` | `0023974D`–`00239766` | 1 | PROVEN |
| Range retirement removes the member | `002352B6 xor edx, edx` / `002352BB call 0x306E60` | 1 | PROVEN |
| The reset zeroes `memberMask` too | the eight stores against the `+0x10` bias, tabulated in §4 | 1 | PROVEN |
| Bit 47 is touched at exactly four sites | immediate-operand sweep of every body; positive controls `00306FBF`, `00306FFD` | 1 | PROVEN |
| Events `0x2007/0x2008/0x200C/0x200E` reach `00307110` **inside `003250F0`** | the jump table at `00325208`/`00325224` decoded from the image; `0032519C`–`003251A4` | 1 | PROVEN |
| ~~`003250F0`, `00325090`, `00325260` have no static route~~ *(corrected 2026-10-02, OPUS: refuted - `002EA4C5` registers the guard `002E70A0` in slot 0xC (`0041D6C0` stores `[02CA4410 + 0xC*8]` = `02CA4470`), the engine calls the slot at `0041DC9E`/`0041DD1D`/`0041CEE3`, `002E70B0` is `jne 003250F0`, and `003251A4` calls `00307110`; `EE-12`, §8)* | linear boundary-free `.text` sweep for `E8`/`E9`/both `LEA` encodings (controls `00265A4F`→`00233F70`, `003251A4`→`00307110`); whole-file 64-bit pointer search; 32-bit VA and RVA words | 1 | ~~PROVEN (as a negative over the listed routes)~~ REFUTED |
| The presentation event is consumed by the animation layer | `003299B0` → `002EB030` (`002EB04D` store at `+0xF0`) → `002EB0D0` → `00427320` on the `0x740` object | 1 | PROVEN |
| The flag is consumed per frame into table slot 3 | `00307050`–`00307071`, `0026ADDD`; caller `00234590` | 1 | PROVEN |
| `+0x08`/`+0x0C` are written on the lethal path in seconds | `00300801`, `00300805`–`00300829` | 1 | PROVEN |
| No one-shot exists in the helper or its caller | `00300530` consults no flag before `0030082F`; `00306F00` tests only the masks | 1 | PROVEN |
| Script-side argument order `(group, mode)` | inferred from the pop-order law; ~~no decompiled script seen~~ observed in 6,746 shipped calls *(answered: see §8, `EE-11` 2026-09-13; 2026-10-02, OPUS)* | ~~2~~ 2 + authored-data census | ~~PROBABLE~~ OBSERVED |
| What the row-12 bits and slot 3's reader are | ~~**not established**~~ `EE-8` answered 2026-09-12 (bits 7, 11, 12 and 20 left as residue); `EE-9` answered 2026-09-18 - the zone script sleeps on slot 3 *(answered: see §8; 2026-10-02, OPUS)* | ~~—~~ 1 + authored-data census | ~~UNKNOWN~~ PROVEN, with the EE-8 residue |
| `0x30B` is unread — `003E6C10` posts a type-3 relation-look event and clears record `+0x24C` | the single call chain `00238B70` → `002E7C10` → `003E6C10` read in full, 2026-09-11 | 1 | PROVEN |

## 10. Related

- [`../../_index/RESEARCH-IMPORT-BACKLOG.md`](../../_index/RESEARCH-IMPORT-BACKLOG.md) — the import
  these six came from.
- [`../../19-Save-Load-Settings/Game-Settings-Config/game-settings-ini-and-runtime-config.md`](../../19-Save-Load-Settings/Game-Settings-Config/game-settings-ini-and-runtime-config.md)
  §12 — `FrameLimit` and the `0x01DFE0B8` scale this formula divides by.
- [`../CONTRACT-group-completion-and-respawn.md`](../CONTRACT-group-completion-and-respawn.md) — the
  contract over this page.
- [`../spawn-placement-and-retirement.md`](../spawn-placement-and-retirement.md) — range retirement,
  the `remove` caller.
- [`../../04-Actor-Entity/Battle-Record-Kind/battle-record-kind-byte.md`](../../04-Actor-Entity/Battle-Record-Kind/battle-record-kind-byte.md)
  — the kind byte behind every gate here.
- [`../../01-Script-VM-Native-Bridge/Spawn-Verbs/the-script-to-native-calling-convention.md`](../../01-Script-VM-Native-Bridge/Spawn-Verbs/the-script-to-native-calling-convention.md)
  — the pop order that fixes the verb's argument order.
- [`../../15-Input/Gameplay-Capability-Policy/capability-inhibition-policy.md`](../../15-Input/Gameplay-Capability-Policy/capability-inhibition-policy.md)
  — the row table completion writes into.
- [`../../18-Audio/Audio-Boundary/how-a-sound-request-becomes-a-voice.md`](../../18-Audio/Audio-Boundary/how-a-sound-request-becomes-a-voice.md)
  §7 — the ActorManager slot flag byte that gates the table write.

## Falsification pass 1 — 2026-09-13 (OPUS)

| claim | measured |
|---|---|
| the record stride is `0x250` | **592**, as `imul rcx, rax, 0x250` in every accessor of the family |
| the array base is a pointer at `0208E690` | **20 functions** read it; the nine small accessors are the family §2 describes |
| **seven checks**, and the sixth is the unreachable one | **seven**, in this order: no battle unit · no lane map · `lane < 0` · `lane > map[0]−1` · `slot == 0xFF` · **`test eax, eax / js` after `movzx eax, dl`** · null record |
| the same prologue "instruction for instruction" | the five lane-in-`edx` accessors share **five identical instructions**, and diverge at the sixth **only in the branch displacement** — `je rel+67` in four, `rel+95` in the one with a longer body. A relocation difference, not a code difference |
| the respawn divisor | `008F8D80` is **30.0f** and `01DFE0B8` is **1.0f** in the image, so the divisor is 30 or 60 exactly as § says |

### One of the nine does not return −1 — and for it, −1 would not have worked either

`SpawnEntry_GetDeathLimit` (`00235EF0`) and `SpawnEntry_GetScriptSelection` (`00236140`) are the
same function twice over. Their listings differ in exactly **two** instructions:

| | `00235EF0` | `00236140` |
|---|---|---|
| the field read | `movzx eax, word ptr [rcx+0xA]` | `movsx eax, byte ptr [rcx+0x16]` |
| the failure return | `or eax, 0xffffffff` → **−1** | `mov eax, 0xfffffffe` → **−2** |

**And the two differences are the same difference.** `GetDeathLimit` **zero-extends a word**, so its
values are `0…65535` and **−1 lies outside them** — a safe sentinel, exactly as § argues.
`GetScriptSelection` **sign-extends a byte**, so its values are `−128…127` — and **−2 lies inside
them**. The sentinel is a legal script selection.

So §'s conclusion holds for the accessors that zero-extend and fails for the one that does not:
`−1` is "never a value" *because of the zero-extension*, not because the family agreed on a
convention. A caller testing `== -1` on `GetScriptSelection` would never see its failure; a caller
testing `== -2` cannot tell failure from a real selection of −2.

*(`SpawnEntry_ResetTransientState` (`00236860`) is also not one of the −1 returners: it takes the
lane in **`r8d`**, not `edx`, and is a setter with no failure sentinel at all.)*

### The dead branch, counted

§ records the unreachable `test eax, eax / js` after `movzx eax, dl` and says it appears in all nine.
Searched across the twenty functions that read `0208E690`, that exact three-instruction shape appears
in **seven**: `00235EF0`, `00235F50`, `00235FB0`, `00236100`, `00236140`, `002366E0`, `00236860`. In
six of them it sits at the same index; in `00236100` it sits earlier, because that function takes a
record pointer rather than a lane and so skips the earlier checks.

**Not claimed:** the two accessors §'s shape-search does not cover — `00236030` and `00236670` — ~~were~~
~~not read here, so whether they carry the same branch in a different form is open.~~ carry it in another register form, so the dead arm is in all nine *(corrected 2026-10-02, OPUS: `00236071` `movzx ecx, al` / `00236074` `test ecx, ecx` / `00236076` `js`, and `002366A3` `movzx eax, cl` / `002366A6` `test eax, eax` / `002366A8` `js`)*. §§3–5, the ledger,
the completion test and `EE-2`–`EE-5` were not re-derived; nothing here was executed or observed live.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Core — CLIENT.** A cited function is called by a 62-byte body labelled Core.
- **CoreRuntimeScheduling — SERVICE and CLIENT.** Cited functions read `GameClock_GetRawTickCounter` (three times) and a 72-byte core helper. One is called by `MainLoop_UpdateAndRenderFrame`, and one by the 978-byte core start-up root.
- **Status_Periodic_Terminal — SERVICE and CLIENT.**
  - Cited functions call `BattleUnit_ResetActionControlForStatusTransition` (twice), `BattleUnit_RunPeriodicCombatMaintenance`, `BattleStats_RemoveStatusMode0` and `BattleStats_ChangeStatusAndProcessSideEffects`.
  - They are called by `BattleUnit_RecoverFromTerminalStatusSetIfClear` (twice), `BattleStats_ChangeStatusAndProcessSideEffects`, `BattleUnit_RunPeriodicCombatMaintenance` and `BattleFormula_ApplyGlobalPeriodicDrainModes`.
- **Actor - CLIENT and SERVICE (9 edges).** `00269D60`, `002E8FD0` are also called by bodies filed to Actor: `002E35B0` (PresentationBinding), `00265B60` (PresentationState); `002E3AF0` reaches bodies filed to Actor: `002E35B0` (PresentationBinding) - shared machinery across the layer boundary, no shared ownership.
- **ActorEntity - CLIENT and SERVICE (186 edges).** `00233D20`, `00233EA0` are also called by bodies filed to ActorEntity: `0025C830`, `00233F50`; `00233EA0`, `00233F70` reach bodies filed to ActorEntity: `00300E40`, `00236300` - shared machinery across the layer boundary, no shared ownership.
- **Audio - CLIENT and SERVICE (3 edges).** `002E0FA0` is also called by bodies filed to audio: `00229AF0`; `00266D10`, `00313DB0` reach bodies filed to audio: `00362F70`, `002DEE70` - shared machinery across the layer boundary, no shared ownership.
- **Gameplay - CLIENT (17 edges).** `00263E30`, `002EB030` are also called by bodies filed to Gameplay: `003176E0` (Combat), `0031ADB0` (CombatAction), `00321380` (Combat) - shared machinery across the layer boundary, no shared ownership.
- **Input - CLIENT and SERVICE (9 edges).** `00252B60`, `002647D0`, `0026BC60` are also called by bodies filed to input: `00253C70`; `00266D10` reaches bodies filed to input: `00226BE0` (ActorControlMaskPropagationRuntime) - shared machinery across the layer boundary, no shared ownership.
- **InputGameplay - CLIENT and SERVICE (4 edges).** `002E1C20`, `002E1CA0` are also called by bodies filed to InputGameplay: `00313A00` (FieldBattleCapabilityAndUIRequestInhibitMaskReconciliation); `00234590`, `00313DB0` reach bodies filed to InputGameplay: `00313A00` (FieldBattleCapabilityAndUIRequestInhibitMaskReconciliation) - shared machinery across the layer boundary, no shared ownership.
- **Movement - SERVICE (80 edges).** `00233F70` reaches bodies filed to movement: `0023A070`, `0026A330`, `0033A240` - shared machinery across the layer boundary, no shared ownership.
- **Party - SERVICE (22 edges).** `00234590`, `002350C0` reach bodies filed to party: `0023B040`, `003272A0`, `003273B0` - shared machinery across the layer boundary, no shared ownership.
- **Presentation - CLIENT and SERVICE (146 edges).** `0024CFF0` is also called by bodies filed to presentation: `004200A0`, `0042C410`; `00234590`, `00266D10` reach bodies filed to presentation: `00307E70`, `00259E90` - shared machinery across the layer boundary, no shared ownership.
- **RNG_Random_Selection - SERVICE (1 edge).** `002342F0` reaches bodies filed to random selection: `00328D80` - shared machinery across the layer boundary, no shared ownership.
- **Resource - SERVICE (2 edges).** `003E6C10`, `00427320` reach bodies filed to resource: `002ED570` - shared machinery across the layer boundary, no shared ownership.
- **Rewards_Progression_Economy - SERVICE (2 edges).** `002342F0`, `00234590` reach bodies filed to rewards/progression: `00319B10`, `00319600` - shared machinery across the layer boundary, no shared ownership.
- **SaveLoad - CLIENT (1 edge).** `00252D90` is also called by bodies filed to SaveLoad (save/load settings): `00280140` (RuntimeLifecycleSupport) - shared machinery across the layer boundary, no shared ownership.
- **Save_Load_Settings - CLIENT and SERVICE (5 edges).** `002E1C20`, `002E1CA0` are also called by bodies filed to save/load/settings: `005823B0`, `00582860`; `00266D10` reaches bodies filed to save/load/settings: `002EF2D0` - shared machinery across the layer boundary, no shared ownership.
- **Script_VM_Native_Bridge - CLIENT (47 edges).** `00234990`, `00234A10`, `00234A80` are also called by bodies filed to script VM / native bridge: `00349500`, `00349940`, `00349200` - shared machinery across the layer boundary, no shared ownership.
- **World - CLIENT (3 edges).** `002342F0`, `002EA320`, `00314D30` are also called by bodies filed to World: `00266D10` (NativeSupport) - shared machinery across the layer boundary, no shared ownership.
- **WorldAreaField - SERVICE (32 edges).** `00233EA0`, `00233F70`, `002342F0` reach bodies filed to WorldAreaField (world area): `00313F60`, `002FA520`, `00377C20` - shared machinery across the layer boundary, no shared ownership.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**CombatAI — SERVICE.** `00234590` on this page calls `BattlePerception_AdvanceCandidateCacheGeneration`, owned by that layer. What it reaches is **eighteen bytes** that give the generation counter its width: `[022C2578] = ([022C2578] + 1) & 7`, which is the same three bits the cache check compares `byte[+0xEA9] & 7` against; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**CombatFormula — CLIENT.** `BattleStats_SetCurrentHP`, owned by that layer, calls `00300530` on this page. That caller is **eight bytes** that turn the delta-based HP path into an absolute set: it subtracts `dword[+0x48]` from the value it is given and jumps straight into the modification entry point - which is what fixes `+0x48` as the current value; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Combat — CLIENT.** `00322710` on this page calls `00263E30`, owned by that layer — **five bytes**, `mov rax, [rcx + 0x30]; ret`, the unit→sub-record getter whose result `00322710` then probes at `+0x698`/`+5`. The crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-15 (SWE2-FRONTIER).

**UI — CLIENT (shared-callee edges, SWE2-EC7 batch-161).** The `003C8A50` completion emit names the shared teardown helpers `0035D060`/`002470C0`/`0035C080`/`0028FFE0`/`00252D90`/`002E1CA0`; the UI layer calls several of them from its own screen/menu paths (`00279E20`/`0035CF50` calling `00252D90`, `0035C7A0`/`0035C880` under `00234590`/`00252B60`). The crossing is the UI layer consulting shared helpers this page names, not UI ownership of the respawn path. Edge list from `edges.tsv`.

## The `00427320` exclusive subtree — all 7 members bound (SWE2-FRONTIER, followup queue)

`00427320` — the animation object's reaction-event receiver the falsification pass describes —
owns **7 frontier functions**. Every member was disassembled from the shipping image; interior
cites are one instruction inside each declared extent (`interior_cite.py scan`; no boundary
crossings).

| member | size | role | interior |
|---|---:|---|---|
| `003DC7D0` | 244 B | the 16-entry reaction-table scan: `ebp = 002E96B0(unit)`, `r14d = 002E9C00(unit)`; per `0x14`-stride entry of `02B57F70` it requires `[+6]==3`, `[+0xC]==ebp`, `[+0x10]==arg2`, `00322710(unit)!=0`, and `[+0x12]!=r14d` — returns `[+8]` on match | `003DC839` |
| `003DCA00` | 36 B | the single-entry variant: `ecx & 0xF` selects a `02B57F70` row directly; `[+8]==ecx` and `[+6]==3` → returns `[+0]`, else 0 | `003DCA16` |
| `003DD740` | 38 B | a second lookup table `02B581A0`: element `(ecx*16 + edx)` at `0x1C` stride, `[+4]==4` → returns `[+0]`, else 0 | `003DD758` |
| `00322710` | 71 B | sub-record probe the scanner calls per candidate: `00263E30(unit)` → `[+0x698]`; absent sub-record returns **1**, present returns `byte[+5] != 0` | `0032272F` |
| `00422DE0` | 15 B | sign-extended byte fetch from the ~~`01E6B410`~~ `01F00410` priority map (~~`movsx eax, byte[rcx + 01E6B410]`~~ `lea rax, 01F00410` then `movsx eax, byte [rcx + rax]`; corrected 2026-10-01, OPUS) | `00422DEA` |
| `00423230` | 74 B | pending-reaction clear: when `+0xC4 != -1`, resolves `[+0x10]` → `0020E600` → `[+0xDA8]` → `0051B9E0(+0xC4)`, then `btr [rec+0x2C8], 0xC` | `00423268` |
| `00423790` | 385 B | the reaction-eligibility predicate: resolves the pending record the same way (`+0xC4`, `0020E600`, `[+0xDA8]`, `0051B9E0`), rejects `arg4` when `arg4 != 0 && !(arg4 & 0xF000)`, decodes both ids' class nibble (`>>12 & 0xF`: class 4 → `0x2035`/`0x2036` by low `0x35/0x36`, class 3 → `0x2036`, `&0xF000==0x5000` → `0x203E`), then class-1 → `[+0x284] < 0x80000000` and class-2 → the ~~`01E6B410`~~ `01F00410` byte-map compare *(corrected 2026-10-01, OPUS; the `arg4` above is the third argument, `r8` = `word[rec + 0x3B4]`)* `map[a&0xFFF] >= map[b&0xFFF]` | `00423902` |

`00263E30`, `0020E600`, `002E96B0`, `002E9C00`, `0051B9E0`, `002D1AC0`-family callees are
shared — deliberately not census members.

## The `002E3AF0` exclusive subtree — all 6 members bound (SWE2-FRONTIER, followup queue)

`002E3AF0` — the type-1 presentation release `0025AB30` dispatches to (EE-10) — owns **6
frontier functions**. Every member was disassembled from the shipping image; interior cites
are one instruction inside each declared extent. The root itself (294 B) is the detach
battery: `002E6BD0(actor, 0, 0)`, `0025D4F0`, `0025D690`, the `+0xC0` record's `0x740`
resolve → `00428FE0(rec, 0)`, `0031B750([+0x30])` → `003E7D50`, `+0x14F` bit-0 clear,
`002E35B0` (returns its result), `[+0xC0][+0x138]` → `003DAD00` then NULL, `0025D480`,
`0026DF40`, `byte[+0x20]` → `0036EC10` then `0xFF`, `+8 |= 4`, and the `0026B450` /
`00269E20` / `00269E40` zero-float tails.

| member | size | role | interior |
|---|---:|---|---|
| `0025D4F0` | 78 B | kind-`0x60` (movement-context) release: `[[actor+0xB8]+0xD8]` → `003B42B0` when nonzero, then zeroes the cell | `0025D507` |
| `0025D690` | 173 B | the `+0x108` table drain: for kind-`0x60` actors, four dword slots `[+0xB8]+i*4+0x108` (i clamped 0–3), each nonzero entry → `003ABCA0` then zeroed | `0025D6F0` |
| `00269E40` | 26 B | writes `xmm1` to `[actor+0xC0]+0x144` then tails `00268380` — the last of the root's three zero-float writes | `00269E4C` |
| `0026DF40` | 101 B | six `002EBC90(actor, i, 0)` calls, i = 0–5 — clears the six flag slots in one pass | `0026DF4E` |
| `002E35B0` | 1,189 B | the detach engine: clears two `0x30`-stride slot entries at `[+0xC0]+0xC0`/`+0xF0` plus the `+0x30`/`+0x60`/`+0x90` slots — each live slot gets `0042F250(word[+0])`, `+0x11` normalized (`&0x9F \|6`), `+0x10 |= 0xB`, `002ED470([+0])`, and both `0215FD58`/`0215FD78` observer lists scanned for `[+4]` with a `+0x1C` refcount decrement (zeroed when ≤0 while `+0x19 & 3`); then the `+0xC0` record's own `0x740` pair gets `[+0x108]` cleared and `003E5E20(rec, 0)`, `0042FAE0(word)` runs, the same `0215FD58`/`0215FD78` pair is scanned once more for the record's `[+4]`, `002E8FD0(actor)` finishes, and the function returns whether a live `+0xC0` record existed | `002E3658` |
| `003E7D50` | 133 B | the `0x150`-stride presentation-slot teardown at `02B59D80`: `word[+4]` resolves a `0x740` record whose `+0x6A4` is set to `-1` when `+0x284` is live, `word[slot]` cleared, `[+0x128]` released via `0024CFF0`, then `00470000(+0x20)` and tail `0051DC60(+0x70)` | `003E7D7B` |

`002E6BD0`, `0031B750`, `003DAD00`, `0025D480`, `0036EC10`, `0026B450`, `00269E20`,
`0042F250`, `002ED470`, `0042FAE0`, `003E5E20`, `00269D60`, `002E8FD0`, `002EBC90`,
`00428FE0`, `003B42B0`, `003ABCA0`, `0024CFF0`, `00470000`, `0051DC60` and `00268380` are
shared callees with other callers — deliberately not census members. `003E7D50` also pins
the `02B59D80` table's record shape (`0x150` stride; `+0x128` releasable handle; `+0x20` and
`+0x70` sub-objects; `+4` a `0x740` index) — the identity residual the world-tick page's
EX-3 leaves open narrows to: **an eight-slot presentation-registration table torn down per
released actor**.


## The readers of `02CA4410`, found (FABLE, 2026-09-16)

**THE READERS EXIST, AND THE PAGE'S OWN DOUBT WAS RIGHT - 2026-09-16 (FABLE).** The sweep that found *exactly two* references searched for **`02CA4410` itself**, the table's BASE. **Every reader references its own SLOT**, so a base-exact sweep cannot see one. This is the same exact-displacement-versus-whole-range distinction that corrected six rows earlier today. **Censused by overlapping range instead.** Over `02CA4410`–`02CA466F`, across every listed body: **35 reads, 4 writes and 2 `lea`, in 37 distinct functions.** The second table `02CA4670`–`02CA480F` has **2 reads and 4 `lea`**. **Both are read.** **And the readers are one per command class, with the slot index equal to the class number.** `0041D6C0(id, fn)` writes `[02CA4410 + id*8]`, so slot *N* sits at `02CA4410 + 8N` - and the accessors line up exactly: `02CA4430` is **id 4** and is read by `PresentationAuthoredCommand_Class04_DispatchGlobalPresentationControl`, which also **calls through it** at three sites (`call qword ptr [02CA4430]`, `00417B52`/`00417B69`/`00417B80`); `02CA4438` is **id 5** and `Class05_Dispatch`; `02CA4498` is **id 0x11** and `Class11_Callback`; `02CA44A0` id `0x12` and `Class12_Callback`; `02CA44A8` id `0x13` and `Class13_Callback`, and so on up to `Class48_Callback` at `02CA4650`. **So the table is dispatched, not dead.** The page wrote *thirty-four handlers registered by a core render initialiser and never dispatched would be extraordinary, and an instrument that has already failed a control once today is the likelier thing to be wrong.* **That judgement was correct and this is the confirmation** - the instrument was base-exact, the code is slot-relative, and the reader family is `PresentationAuthoredCommand_Class*`. *What the census still cannot see.* An **indexed** read - `lea` the base, then `[base + id*8]` with a runtime `id` - leaves no rip-relative displacement at any slot. The two `lea` sites in table A's range are exactly that shape, so **the dispatch may well also happen through the base**, and the per-slot accessors may be only one of two routes. I have shown the readers exist; I have not shown these are all of them.

## Interior citation — frontier hub `003DBB60` (2026-09-17, SWE2-EC7)

`003DBB60` — 120 B, 10 A-measured callers at census; `ActorResource_SubmitRequestDescriptor`,
called here as `003DBB60(actor, 2, index, 0)` before `00269640(actor)`. Interior verified
against the shipping image: `r9-1` maps to 0, `r9-2` maps to 2, other kinds keep `r9` and set
flag bit 0 ([`003DBB7B`](../../_index/ADDRESS-INDEX.md)–`003DBB9D`); the nine-byte stack descriptor
`{kind, 1, dl, r8w, 0x8000, flags}` packs at `003DBBA0`–`003DBBC9`, and `call 003DBCF0` at
`003DBBCE` submits it. The kind-2 call this page makes therefore submits a mapped-kind request
with the flag bit clear.


## Interior citation — frontier hub `0035C080` (2026-09-18, SWE2-EC7)

`0035C080` — 68 B, 6 A-measured callers; the reset/respawn helper this page's group-wipe path
reaches. Interior verified: singleton `022C83E0`'s dword `+0xC4` nonzero → `00290990` then
cleared (`0035C090`–`0035C0A5`), `003C53E0(0)` resets the channel, and `0028E900` +
tail-jmp `0028E8B0` ([`0035C0B6`/`0035C0BF`](../../_index/ADDRESS-INDEX.md)) run the two-stage
teardown the respawn side relies on.

## SWE2-EC7-21 update (2026-09-18) — `0042F250` SSE-lane scatter fragment

`0042F250` (70 B) is a `022C6F28` `0x740`-row flag commit: `cx == -1` exits
(`0042F250`/`0042F295`); else `rcx = [022C6F28] + movsx(cx)*0x740` resolves the
row (`0042F256`..`0042F263`) and a zero `dword[+0x284]` vetoes to null
(`0042F26A`..`0042F277`). A live row takes `[+0x290] = (old & 0xFFF3FFFF) | 0x100000`
— bits 18/19 cleared, bit 20 set (`0042F279`..`0042F28A`) — then tails into
`003E6770` (`0042F290`). The per-row state update the respawn-side evaluators
share. Callers `00431830`/`0044xxxx`/`0045xxxx`/`0046xxxx` zone — the evaluator
cluster.

## SWE2-EC7-27 update (2026-09-18) — `002EBC90` kind-indexed flag-slot setter + `002EB0D0` presentation-event flush

`002EBC90` (170 B) is the `002EBC90(actor, i, 0)` slot writer the
six-clear pass runs: kind `edx` selects a `[rcx+0xC0]` sub-record —
1 -> `+0x60`, 2 -> `+0x30`, 3 -> `+0x90`, 4/5 -> `(edx-4+4)`-indexed
0x30 rows, else the base — then replaces `byte[+0x10]`'s low nibble
with `r8b << 4`. Interior anchor `002EBD2D` (the nibble compose).

`002EB0D0` (604 B) is the animation-layer event consume the
`003299B0 -> 002EB030` write arms: on `dword[rdx] != -1` it
`00269D60`-prepares the record, dispatches `byte[+0x11]` bit `0x10`
through `002EDCC0`, then works the `022C6F28` `0x740`-row of
`word[rbx]` (every hop gated on `dword[+0x284] != 0`): `00427320` on
the direct path, `00427880`/`004278B0`/`004272C0` keyed on
`word[+0x2a]`'s sign, `00427860` or `004270A0`/`004272E0` keyed on the
extra float arg, `004272A0` fed `byte[+0x11] >> 3 & 1`, and
`00314D30(1)` on bit `8`. Between hops it resets `+0x14`/`+0x18`/
`+0x1C` to `-1.0f` and `word[+0x2a]` to `0xFFFF`, clearing
`byte[+0x11]` bits `0x10` and `8` on the way out. Interior anchor
`002EB154` (the first `00427320` call).

## SWE2-EC7-28 update (2026-09-18) — `00269D60` two-bit flag pack

`00269D60` (29 B) is the `002EB0D0` record-prepare's flag write: clears
`byte[rcx+0x29]` bits 0-1, then sets bit 0 = (`edx != 0`) and bit 1 =
(`r8d != 0`) via `setne`/`add al,al` — the two-condition pack the
presentation-event flush carries. Interior anchor `00269D75` (the bit-1
compose).
## SWE2-EC7-31 update (2026-09-18) — `00254500` per-bit mask fold

`00254500` (67 B) is the mask translator the respawn checks share:
`002E0FA0()` returns a source bitmask, then an 11-iteration loop
(`ecx` rotated left one bit per pass) ORs a dword out of the
`01E0C2C4`-based table for every set bit — `rdx` advancing by 8
per iteration, reading `rdx-4` on the first pass and `rdx`
thereafter — so each source bit contributes its own mapped flag
word to the result. Interior anchor `00254526` (the first `or
edx`-table accumulate).

## SWE2-EC7-43 update (2026-09-19) - `003C9250`

`003C9250` (280 B) ~~is a group-respawn body~~ is not shown to be a group-respawn body: it references no ledger, keep bank or spawn global, and its callers are `003C87B0` and `003C8B70` *(corrected 2026-10-02, OPUS: body read)* - `01F44830`/`02B47730`, `0035BAD0`/`0035D3E0`/`0035DC90`/`0035DCC0`/`0035DEB0`/`00808C40`. Interior anchor `003C9276` (a `0035BAD0` call).

## SWE2-EC7-43 update (2026-09-19) - `003E6770`

*(Corrected 2026-09-19, FABLE: `003E6770` is not a group-respawn body and has no part in respawning. It builds, or
switches off, a render record's bone trails from the model's FCP section 4;
[bone trails](../../17-Presentation-Rendering/Character-Render-Records/the-bone-trails.md). The anchor cited below,
`003E6823`, is a call to the constructor `0051CC30`; the `0051CC10` call is at `003E685A`.)*

`003E6770` (276 B) ~~is a group-respawn body~~ is not a group-respawn body *(corrected 2026-10-02, OPUS: see FABLE's 2026-09-19 correction directly above)* - `003E679E`/`003E6869`/`0051CC10`/`0051CC30`. Interior anchor `003E6823` (a `0051CC10` call).

## SWE2-EC7-89 update (2026-09-20) - `003B42B0` intrusive-list removal measured

`003B42B0` (94 B) is the keyed unlink the group callers run: the
`02B404C8` chain is walked for the node whose `dword` matches
`ecx`; on the hit `02B404C0` decrements, the node's key is
zeroed, and the `+0x8`/`+0x10` links are resewn - with
`02B404C8`/`02B404D0` head/tail fixups when the edge nodes go.
Interior anchor `003B42CE` (the count decrement).

## SWE2-EC7-97 update (2026-09-20) - `002E96B0` measured

`002E96B0` (25 B) is the `+4` twin of the same getter
`0037B4D0` and `003DC7D0` call: `rcx` and `[rcx+0xC0]` non-null
yields `dword[block+4]`, anything else `-1` - the second-dword
read the respawn check issues.
Interior anchor `002E96C1` (the `dword[rax+4]` read).

## SWE2-EC7-102 update (2026-09-20) - `0028C940` measured

`0028C940` (46 B) is the two-slot flag arm
`00290990` and `002909F0` call: `word[rcx + 0x28]`
gains bit 1, then a two-iteration `0x20`-stride loop
at `+0x44` arms bit 1 on each entry word that has
bit 0 set but bit 1 clear - the paired enable the
wipe-rebuild paths post.
Interior anchor `0028C950` (the loop head).

`003C8A50` (173 B) is the completion-kind emit `003C8B70` runs on the `02B47730` record: `ecx-1` in 0..6 rides a jump table (one arm forcing `ecx=3`, another `ebx=1`, default `ecx=5`) into `00249C60`, then `0035D060(1)`, `002470C0` on the record, `ebx` committed to `[rax+0xD0]`, `0035C080`, `[rax+0xC8]` cleared, `0028FFE0(1,0)`, `00252D90`, and a tail `002E1CA0(8,0)`

Interior anchor `003C8A77` (function `003C8A50`).
