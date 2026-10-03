---
system: The moment an action is committed
category: 07-Combat-Action
status: AUDITED
owner_layer: PrimaryOwner:CombatAction
evidence_tier: 1
verified_against:
  gzf_sha256: fb9b5e7ea002c1626a53d47da0b0b69a2443e246f7ce2b64329be4e034a2d3f7
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: additive-annotation across GN159 -> GN161 - every step of the certified lineage is additive on the canonical record (internal 38161, owner 9409 and finalNo 585 constant at all five generations; each step's codeDomain and explicit rise equals its unresolved fall). Of the functions classified since GN159 this document cites none of batch R109's 109; the 21 classified before GN160 are named in AUDIT-LOG's batch records and not in a tracked machine-readable list, so identity is not claimed. Voided by any delta that removes or rewrites a comment, tag, name, prototype or body range.; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md, lineage extension (twenty ledger figures across five generations)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  snapshot_sha256: a9cead8777597cdca58f2a47f27153f5231d60ad2bc16c3da9df8253820b09bd
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-03
falsification_passes: 1
audit:
  passes: 1
  last_pass: 2026-09-03
  last_pass_state: first-read-repos-55
  crossref_clean: true
  reopened_count: 0
---

# The moment an action is committed

`BattleUnit_CommitAction` at **`0030F760`**, 570 bytes.

**Nine documents cited this function and not one had opened it.** It is the instant a character
locks in a command — the frame where "attack that enemy" stops being a menu selection and becomes
the thing the unit is doing. Everything downstream, from the swing animation to who the enemy turns
to face, reads state this function writes.

## What the player sees

**Four things happen at the moment of commitment, and three of them are about everyone else.**

1. The action and its target are written into the unit, **with a full copy kept beside them**.
2. If the acting unit is the **group leader**, its target is **broadcast to every eligible member of
   the group** — which is why the rest of the party turns to face what the leader picked without
   anyone issuing them an order.
3. The target learns it is being attacked: **the attacker's bit is set in the target's attacker mask,
   an attacker count is incremented, and enmity is registered — once while that attacker's bit remains set.**
4. A queued repeat is dropped if the action or the target has changed *(for a stats kind-0 unit; kind 1 keeps it whatever changed, and any other kind drops it — corrected 2026-10-02, OPUS: `0030F841`–`0030F85F`)* — compared against the last **cancelled** action's record at `+0x740` / `+0x744` (the cancellation section below).

**Nothing about damage, cost or timing happens here.** This function decides *who is doing what to
whom, and who else needs to know.*

## The signature, read from the call

```c
int BattleUnit_CommitAction(BattleUnit *unit, void *actionData,
                            uint16 actionId, uint32 targetId, int alsoPrepare)
```

`alsoPrepare` non-zero calls `003105D0` first. `targetId` is resolved to a unit pointer through
`0031B7E0` (the decode contract: [the slot-pool page](../04-Actor-Entity/battleunit-slot-pool-and-actor-class.md) §11), and **a failure to resolve is not an error** — the commit still happens; only the
broadcast and enmity steps are skipped.

## Two accepted id ranges, and the second is easy to misread

```asm
0030F8B2  cmp  di, r13w              ; actionId vs 0x21E  (r13d = 0x21E at 0030F798; JA refuses ids above it — corrected 2026-09-11, ASTRA-REQ-FABLE-COMMIT-ID-ANNOTATION)
0030F8B6  ja   0030F97A   # <- corrected 2026-10-02, OPUS - this ja accepts, it does not refuse; 0030F97A is mov eax, 1 (committed). It skips the propagation walk and the attacker mask for ids above 0x21E (band two); the refusal is 0030F7EC ja 0030F981
```

Ids **below `0x21F`** take the normal path. Everything else is refused **unless
`(uint16)(actionId + 0xC000) <= 0x166`** — which is the compiler's way of writing **`0x4000` through
`0x4166`**, a second, disjoint block of action ids.

> **A range test written as an addition and an unsigned compare does not look like a range test.**
> Read as a magnitude it says "large ids are allowed"; read as modular arithmetic it names a specific
> 359-entry window.

Only ids below `0x21F` take the target-buffer reset/append path at `unit + 0x778`,
so the two ranges are **not** interchangeable. This is an embedded `0x208`-byte
`BattleTargetBuffer`: `00316CF0` clears the buffer while preserving its flag bit 0,
then `00316CD0` appends the `ActorWork*` from `*(target + 0x10)` as a sixteen-byte
entry's first qword and increments the count. The previous wording called these
operations handle release/assignment; corrected 2026-09-11 from
[EXP-043](../_experiments/EXP-043-target-buffer-boundary.md) and
[EXP-046](../_experiments/EXP-046-target-buffer-reset.md). The reset's sole call is
an imported `memset`; these helpers establish no actor lifetime release/acquisition.

## The commit block, and the copy beside it

| offset | written |
|---|---|
| `+0x700` | low two bits **cleared** |
| `+0x708` | the `actionData` pointer (8 bytes) |
| `+0x710` | `targetId` |
| `+0x714` | `actionId` (16-bit) |
| `+0x6B4` | zeroed |
| `+0x718 … +0x72F` | **a verbatim copy of `+0x700 … +0x717`** |

**Six dwords are committed and the same six are immediately copied ~~eight bytes~~ twenty-four bytes
further on** — `movups` of `+0x700`–`+0x70F` to `+0x718` and `movsd` of `+0x710`–`+0x717` to `+0x728`
(`0030F80D`, `0030F823`, `0030F82A`; the table above had it right, this sentence did not — corrected
2026-09-11, ASTRA-REQ-FABLE-COMMITCOPY-PROSE). The copy
is unconditional and nothing here reads it back, so **what it is for is not established by this
function** — but a shadow written at commit time, before anything can modify the live copy, has the
shape of *what the unit was told to do*, kept next to *what it is doing now*.

### What cancellation does with the copy — read 2026-09-11 (ASTRA-REQ-FABLE-CANCEL-LOCAL)

`BattleUnit_CancelAndResetCurrentAction` (`003105D0`, 418 bytes) is the other writer of this block,
and it answers what the shadow is for. **Two gates return without touching the unit**: a null unit
(`003105D0`–`003105D3`) and a unit with no stats record (`+0x698 == 0`, `003105DE`–`003105E9`) —
a cancel on either is a no-op, not a reset. Past them, in order: the target relation and action
state are released (`BattleUnit_ReleaseTargetRelationAndActionState` `00310780` at `00310605`),
`+0x6B6` is zeroed (`0031060A`), the two presentation slots `+0x695` / `+0x696` are released and
set to `0xFF` (`BattleAction_ReleasePresentationSlot` `0030C970`, `00310618`, `0031062B`), reserved
execution resources are refunded (`BattleAction_RefundReservedExecutionResources` `00300280`,
`0031063A`), flag bits are cleared on `+0x00` and `+0x04` and `+0x690` is zeroed
(`0031063F`–`00310658`, `00310663`–`0031066F`), this unit's bit is removed from every unit's
`+0xEA0` (`0031067B`–`003106AB`; the mask section below), and the target buffer is reset
(`003106AD`–`003106B4`). **Then the command block:**

| store | site | what |
|---|---|---|
| `+0x718 … +0x72F` → `+0x730 … +0x747` | `003106B9`, `003106CC`, `003106D7`, `003106E3` | **the shadow becomes the cancelled record**: `+0x730` its flags, `+0x738` its `actionData`, **`+0x740` its `targetId`, `+0x744` its `actionId`** |
| `+0x700` | `003106C5` | low two bits cleared |
| `+0x6B7` / `+0x6B8` | `003106EB` | the combo progress word zeroed |
| `+0x6B4` | `003106F2` | phase zeroed |
| `+0x768`, `+0x760`, `+0x6D8`, `+0x6D0` | `003106F9`–`0031070E` | zeroed |
| `+0x75C` | `00310715` | zeroed |
| `+0x714` | `0031071B` | `0xFFFF` — no action |
| `+0x708`, `+0x710` | `00310722`, `00310729` | context and target cleared |

after which the locomotion path is reset (`BattleLocomotion_ResetPathAndSetTargets` `003291B0` on
the unit's `+0x80` sub-object), `+0x1A4` / `+0x1A0` / `+0x6D8` / `+0x6D4` are zeroed and `+0x1F0`
bit 5 cleared (`00310734`–`00310751`), and `0033C9B0` runs on the same sub-object.

**So the queued-repeat check in step 4 compares against the last *cancelled* action**: `cmp di,
[unit+0x744]` and `cmp ebp, [unit+0x740]` at `0030F84E`–`0030F857` read the cancelled record's
action id and target — ~~a re-issued action that matches what was just cancelled keeps `+0x770`,~~
~~any other clears it~~ for a unit whose stats kind byte `[+0x698]+5` is 0, a re-issued action that matches what was just cancelled keeps a non-zero `+0x770`; a kind-1 unit keeps it whatever it commits, and any other combination clears it (`0030F85F`) *(corrected 2026-10-02, OPUS: `0030F841` loads the kind byte, `0030F849 cmp ecx, 1` and `0030F85D je 0030F865` keep the latch for kind 1 without the id and target compares; CONTRACT-commit-action.md §13a)*. The shadow at `+0x718` is written by the commit and read by
nothing but the cancel; the cancelled record at `+0x730` is written by the cancel and read by the
next commit.

ASTRA's [EXP-040](../_experiments/EXP-040-cancel-snapshot-control.md) executed the command block
(`003106B9`–`0031072F`) and the two gates in isolation over a synthetic unit — the stores above,
the 24-byte copy, and the two no-op returns, seven cases — which is isolated execution of original
code with the callees omitted, not a live cancellation; the static reading above is this section's
evidence tier, and the callees' effects are theirs to read.

## The leader test, and the broadcast

```asm
0030F8D5  mov  eax, dword ptr [rbx + 0x24]
0030F8D8  cmp  dword ptr [rbx + 0x8], eax
0030F8DB  jnz  0030F937               ; not the leader -> skip the broadcast
```

**`+0x08` is the unit's own id and `+0x24` is its group id; a unit whose two are equal is the group's
leader.** The engine needs no "is leader" flag — **leadership is an identity, not a property.**

The broadcast walks every actor (`00236850` counts, `00236820` fetches) and writes the leader's
`targetId` into each eligible member's **`+0x754`**:

```asm
0030F8F5  mov  rax, qword ptr [rax + 0x698]   ; the actor's battle record
0030F901  mov  ecx, dword ptr [rax + 0x64]
0030F904  or   ecx, dword ptr [rax + 0x3c]
0030F907  test ecx, 0x80000003                ; two status words, one mask
0030F90D  jz   0030F918                       ; clear -> eligible
0030F90F  call 0x00377C20                     ; set -> one appeal, and only one
0030F914  test eax, eax
0030F916  jz   0030F926                       ; still ineligible -> skip
0030F918  mov  eax, dword ptr [rbx + 0x24]
0030F91B  cmp  dword ptr [rdi + 0x24], eax    ; same group?
0030F920  mov  dword ptr [rdi + 0x754], ebp   ; take the leader's target
```

**A member is skipped when either of two status words has any of bits 0, 1 or 31 set** — and gets one
appeal, through `FieldData_GetActiveFieldRecordBit15` at `00377C20`. A field-level condition can
therefore override a per-unit one, which is the only place in this function where the *world* has a
say in a *battle* decision.

**Three separate reads matter here and only the third is a broadcast:** `+0x754` is written on the
leader itself **before** the loop (`0030F8CF`), on each member **inside** it (`0030F920`), and
`+0x750` is written **after** it (`0030F931`). The pre-loop write means **the leader takes its own
target through the same field it hands to everyone else.**

The whole broadcast is gated on `0030AB40(unit, target, 0)` returning **greater than 1** — a
classification of the action or target that this function does not compute and this document does not
claim to know.

## Enmity: duplicate suppression while the attacker bit remains set

```asm
0030F937  mov   eax, dword ptr [rbx]
0030F939  bt    rax, 0x16                     ; bit 22 of the unit's flag word
0030F93E  jc    0030F97A                      ; set -> no enmity at all
0030F940  movzx ecx, byte ptr [rbx + 0xea9]   ; this unit's slot number
0030F94C  shl   edx, cl                       ; 1 << slot
0030F94E  mov   ecx, dword ptr [r15 + 0xea4]  ; the TARGET's attacker mask
0030F955  test  edx, ecx
0030F957  jnz   0030F97A                      ; already counted -> nothing to do
0030F959  inc   byte ptr [r15 + 0xea8]        ; attacker count
0030F962  mov   dword ptr [r15 + 0xea4], ecx  ; mask |= my bit
0030F975  call  0x00313B30                    ; register enmity
```

> **The mask is the memory.** Repeated commits skip this registration step while the same slot's
> bit remains set. The count at `+0xEA8` counts these newly recorded attacker slots, not blows.

The former **"once per attacker, ever"** wording overstated that local duplicate check.
`00322050` clears the unit's `+0xEA4` mask and `+0xEA8` count before calling `003220E0`;
`00322080` does the same when its actor has a unit. These reset boundaries remove the
recorded bits, allowing a later otherwise-eligible commit to take the registration path again.
[EXP-047](../_experiments/EXP-047-attacker-mask-reset.md) preserves isolated original-code
controls for those writes and separates them from the ~~unexecuted~~ delegate's effects. *(Updated 2026-09-25, FABLE, Claude
Opus 5.5, on OPUS block 305: the delegate `003220E0` is no longer unexecuted —
[EXP-151](../_experiments/EXP-151-rekey-inner-exec.md) executes it.)*
Corrected 2026-09-11. The frequency of these resets in live fights and the delegate's full
effects are not established here; this is not a claim that all enmity updates use this path.

**Bit 22 of the unit's flag word suppresses the whole step**, so an attacker can act on a target
without ever entering its attacker set.

## A second mask four bytes below, found by the pair frontier

**`+0xEA4` is not alone.** `+0xEA0` is a second per-unit bitmask, indexed the same way, and **three
functions touch it that no document mentioned together** — the pair ranking's second candidate.

```asm
0031069C  and dword ptr [rax + 0xea0], edx   ; cancel: edx = ~(1 << slot), inside a loop
                                             ;   over every actor (00236850 counts, jl back)
00307511  and dword ptr [rbx + 0xea0], eax   ; target processing: one unit, one bit cleared
00300EEE  cmp dword ptr [rdi + 0xea0], esi   ; teardown: the WHOLE mask tested before proceeding
```

**All three build the bit the same way** — `mov 1` / `shl by cl` / `not` / `and` — **the same
`1 << slot` idiom this function uses to set `+0xEA4`.**

> **One bit index, two adjacent masks, opposite directions.** Committing an action **sets** your bit in
> the target's `+0xEA4`; cancelling **clears** your bit from **every actor's** `+0xEA0`.

**The cancel path's loop is the strongest part:** it walks the whole actor list and clears one bit from
each. **A field cleared from everyone at once is a field that everyone could have been holding** — so
`+0xEA0` records a relationship *from* each unit *to* the cancelling one, not a property of the unit
that owns it.

**And the teardown compares the entire dword** rather than testing a bit, so **a unit is torn down on
the mask being some specific whole value** — most plausibly empty, though the compared register's
source is outside the window read here and **this document does not claim it is zero.**

> **Three functions, one field, three different verbs — clear-one, clear-from-all, test-all — and no
> document mentioned two of them.** That is what the comparison ranking is for.

## Three slot handles in a row, and the stage that moves them

> **Corrected 2026-09-13 (FABLE, on `OPUS-CONTRA-SLOT-HANDOFF`).** This section called `+0x695`/`+0x696`
> a pair released by one idiom in three functions, citing `0030688B` as a `0xFF` store. **`0030688B` is
> `mov byte ptr [rbx + 0x696], al`** — the handle in `+0x695` moving into `+0x696` — so only two of the
> three functions release `+0x696`, and the census missed a third releaser that reaches the byte through
> a pointer. The re-read below replaces the pair reading; the original listing is kept, struck, after it.

**`+0x694`, `+0x695` and `+0x696` are three stages of one presentation-slot handle**, each a one-byte
index into the 32-record, `0x30`-byte pool at `022C17B0` (`0030C983`–`0030C994`), `0xFF` meaning empty:

| stage | filled by | released (`0030C970`, then `0xFF`) by |
|---|---|---|
| `+0x694` | `BattleAction_AcquirePresentationSlot` `0030CFB0`, given `unit + 0x690`: only when `[+4]` is `0xFF` (`0030CFBF`), stores `BattleAction_AllocatePresentationSlot`'s byte (`0030D051`–`0030D056`, which can itself return `0xFF`); callers `00304E24` and `0030EF00` | `00300060` (`00300100`–`0030010C`), `BattleUnit_ReleaseTargetRelationAndActionState` (`00310812`–`00310825`), `BattleUnit_AdvanceStandardActionState` through `r12 = unit + 0x690` (`00304B6F`–`00304B7A`) |
| `+0x695` | moved from `+0x694` when `+0x694` is live and `+0x695` is empty, then `+0x694 = 0xFF`: `00306760` (`00306766`–`0030678B`), `BattleAction_DispatchResolvedPresentationEvent` (`0030FE23`–`0030FE3D`), `00313120` (`003132C9`–`003132E3`) | `00308270` (`00308289`–`00308295`), `00309990` (`00309A49`–`00309A55`), the cancel (`00310611`–`0031061D`), `00304850` (`00304B80`–`00304B8B`) |
| `+0x696` | moved from `+0x695` on the same test, then `+0x695 = 0xFF`: `BattleAction_UpdateSpecialPresentationSequence` only (`00306877`–`00306891`) | `003065D0` (`003066D8`–`003066E4`), the cancel (`00310624`–`00310633`), `00304850` (`00304B91`–`00304B9C`) |

`BattleUnit_ResetStateForReuse` sets all three to `0xFF` without releasing (`00236A7C` word, `00236A8C`).
Displacement census of `0x694`–`0x696` plus the `lea [reg + 0x690]` sites that feed `r12`/`rcx`
(`00304886`, `0030EEEB`); an access through some other pointer would escape it. **Not claimed:** what a
slot record presents, why only the special-sequence update advances into `+0x696`, and whether a stage is
ever skipped live.

~~**Another pair row: `+0x696`, six sites across three functions**, one documented and two not, **and no
document citing two of them.** All three do the identical three-instruction sequence:~~ *(superseded
above; the listing below is the original transcription, with its `0030688B` line wrong)*

```asm
; BattleUnit_CancelAndResetCurrentAction — and it does it TWICE, for two adjacent bytes
00310618  call  0x0030C970                        ; release the handle already in ecx
0031061D  mov   byte ptr [rbx + 0x695], 0xff      ; mark +0x695 empty
00310624  movzx ecx, byte ptr [rbx + 0x696]       ; read the second handle
0031062B  call  0x0030C970                        ; release it through the same function
00310633  mov   byte ptr [rbx + 0x696], 0xff      ; mark it empty

; and the same read / release / 0xFF in two other functions
003066E4  mov   byte ptr [rbx + 0x696], 0xff
0030688B  mov   byte ptr [rbx + 0x696], 0xff
```

> ~~**`+0x695` and `+0x696` are two one-byte handles side by side, `0xFF` meaning empty, released through
> one shared function.** The cancel path frees **both**; the other two functions free only the second.~~
> *Superseded 2026-09-13:* they are the last two of three stages; `00306760` moves a handle into
> `+0x696` rather than freeing it, and `00304850` frees all three.

**`0xFF` as the empty marker is the fourth sighting of that convention** — the trigger record's
*"set no flag"*, the slot resolver's failure return, the unbindable-input table's terminator, and now
these handles. **A one-byte handle space in this engine reserves `0xFF` rather than `0`.**

**What the handles refer to is not established here.** `0030C970` takes the byte and returns nothing
used at these sites; **three functions agree on the protocol and none of them names the resource.**

## Falsification pass — 2026-09-03

| attack | result |
|---|---|
| Is `+0x08` vs `+0x24` really leader-vs-group, or two unrelated fields? | **Corroborated inside the same function**: the loop tests `[rdi+0x24] == [rbx+0x24]` for *group membership*, so `+0x24` is a group id in both uses; only `+0x08` differs. |
| Does the decompiler's `param_1[2] != param_1[9]` mean byte offsets 2 and 9? | **No — and this is why the assembly was read.** They are dword indices: `[rbx+0x8]` and `[rbx+0x24]`. A document quoting the decompiled indices as offsets would be wrong by a factor of four. |
| Is the `0x718` block a second live copy rather than a shadow? | ~~**Not established either way, and left that way.**~~ *(answered: a shadow - the cancel `003105D0` copies it to the cancelled record `+0x730`–`+0x747` (`003106B9`–`003106E3`), which the next commit reads; see the cancellation section above; 2026-10-02, OPUS)* Nothing in this function reads it. |
| Is `+0xEA0` the same kind of thing as `+0xEA4`? | **Same `1 << slot` construction at all four sites**, four bytes apart, in the same object. **Same indexing; the roles differ and are not asserted to be complementary.** |
| Does the cancel loop really clear the bit from every actor? | The loop calls the actor **count** function each iteration and branches back while the index is below it — **the same walk shape as this function's own broadcast loop.** |
| Are `+0x695` and `+0x696` the same kind of field? | **Adjacent, both one byte, both set to `0xFF`, both released through `0030C970`** — and the cancel path does the two in immediate succession. **Same protocol; whether they name the same kind of resource is not established.** *2026-09-13: yes — the same handle at two stages; `00306877`–`00306891` moves it from `+0x695` to `+0x696`, and `+0x694` is the stage before.* |
| Is `0x80000003` explained here? | **No.** Its *use* is established — a two-word eligibility gate on receiving the broadcast — ~~and its *meaning* is not~~ *(answered: KO, Stone and X-Zone / Vanished - how-a-combo-continues-and-what-it-blocks.md, condition 4, and how-an-action-gathers-its-targets.md; 2026-10-02, OPUS)*. See `PROPOSED-repos46-5`. |

**What this document does not claim:** ~~what `0030AB40` classifies, what `00313B30` does with the~~
~~enmity it is handed, what the `0x4000`–`0x4166` id block contains, or what the byte table at~~
~~`022C1DB8` (indexed by slot × 12, read into `+0x6B9` when `+0x6B0` bit 1 is set) holds.~~ *(answered: `0030AB40` in the interior citation below; `00313B30` is the notify, CONTRACT-commit-action.md §13a; the `0x4000`–`0x4166` block is the order space, Action-Dispatch/battle-action-handler-table.md; `022C1DB8` is byte `+8` of a 12-byte per-slot row at `022C1DB0`, the reserve-member slot `BattleUnit_IssueCommand` parks (`00311DA5`) and `00385756`–`0038575D` hands to `00320A40` as a battle-stats record index - Post-Result-Events/the-post-result-events-and-the-battle-message-table.md, the reserve route; 2026-10-02, OPUS)*

## Why it was never opened

It sits in this database's **"leaned on and never opened"** cut: **570 bytes, cited by nine
documents, no interior anchor anywhere.** Every gate passed on all nine — the address resolved, the
links worked, the name was in the index.

> **A name cited by nine documents is load-bearing whether or not anyone opened it.**

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. MECHANICAL-only crossings (the image-address resolver, the audio request chain) are recorded in the registry, not here.*

- **Items_Equipment_Shops_License — SERVICE and CLIENT.**
  - `BattleAction_RefundReservedExecutionResources` (`00300280`) gives items back through
    `Inventory_ModifyEncodedItemAndUpdateDiscoveryState` and restores gil through `GameState_GetGil` / `GameState_SetGil`.
  - `Inventory_QueryOwnedCountIncludingReservedActionItems` and `Equipment_UnequipEncodedItemFromActiveRoster` read the
    field action-permission bit.
  - `BattleStats_ClearAllEquipmentSlotsByMapp…` walks the unit table.
- **Spawn_Encounter_Lifecycle — CLIENT.** `Spawn_CountActiveCapTrackedActors` walks the unit table
  (`BattleUnit_GetBySlotIndex` / `BattleUnit_GetSlotCount`).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**CombatFormula — SERVICE.** `00304850` on this page calls `BattleRuntime_ResolveAndCacheEffectiveActionId`, owned by that layer. What it reaches is the writing half of the effective-action-id pair: it resolves the same two definition tables - `0208D480` by `byte[+4]` when `byte[+5] == 0`, `0208DE80` by the owning unit's `byte[+0xEA9]` otherwise - and **stores** the recomputed id into the row's `word[+0x10]` when the unit's `word[+0x714]` is `0x9F`, returning `0xFFFF` when there is no owning unit at all; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Gameplay — CLIENT.** `BattleUnit_UpdateEngagementStateFlag`, owned by that layer, calls `00377C20` on this page. That caller is the engagement test, which reads the actor's `+0x698` block and tests `+0x3C` OR `+0x64` against its own mask; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Rewards_Progression_Economy — CLIENT.** `BattleUnit_ProcessDefeatRewardsAndLoot`, owned by that layer, calls `00377C20` on this page. That caller is defeat-and-loot processing, which reads the defeated unit's `+0x698` block, needs `byte[+5] == 1`, and is suppressed entirely by bit 3 of `byte[+0xE9A]`; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**CombatAI — CLIENT (SWE2-CONTRACT 2026-09-15, 24 edges).** The commit path is where the AI's selected action enters:
`AiOrder_EvaluateTargetSelector` shares six of the page's helpers (`00236820`/`00236850`/`0030AB40`/
`00316CF0`/`0031B7E0`/`00377C20`); `BattleUnit_SelectAndCommitNextAction` shares `00308270`/
`0030F760`/`00377C20`; `AiOrder_EvaluateAndResolveActionTarget`, `AiOrder_SelectFinalTargetFromCandidates`,
`AiOrder_BuildCandidateTargetBufferFromStoredRangeAndStatus`, `AiOrder_ComputeBoundedSelectorScalar`,
`BattleUnit_TrySelectAndCommitAiOrderFromSet`, `BattleTarget_MatchesRelationMode` and the enmity/
perception bodies (`BattleEnmity_PropagateToPerceivingFoes`, `BattleUnit_RebuildPerceptionCandidateCache`,
`BattlePerception_RefreshCandidateCacheGeneration`, `BattleUnit_UpdateCombatFrame`) neighbour the
same commit helpers. AI order selection commits through the machinery this page describes — a real
adjacency: the layer drives this page's path, not shared ownership.

**CombatFormula — CLIENT and SERVICE (SWE2-CONTRACT 2026-09-15, 11 edges).** `00304850` calls
`BattleRuntime_ResolveAndCacheEffectiveActionId`/`BattleRuntime_GetEffectiveActionId`;
`003065D0` trades calls with `BattleStats_ModifyHPAndProcessLethalState`; `00306760` calls
`BattleStats_GetByBattleSlotIndex`; `003105D0` is reached by
`BattleStats_RebuildEffectiveStatsAndAffinityState`; `00236820`/`00236850` are shared with
`BattleStats_FindOwningBattleUnit`/`BattleStats_GetOwningActorHandle`/`00384F40`. Commit resolves
the effective action id and applies the result through the formula layer — a real crossing.


*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page.*

**Input and InputGameplay — CLIENT (2 edges).** `InputGameplay_ArbitrateDigitalInputAndModalState` `00253C70` and the capability / UI-request inhibit reconciliation `00313A00` call `FieldData_GetActiveFieldRecordBit15` `00377C20`. The input arbiter and the inhibit reconciliation read the same per-area bit the commit uses at `0030F90F` for its one appeal; they consult the field record and do not reach the commit.

**Movement — CLIENT and SERVICE (35 edges).** The locomotion bodies `BattleLocomotion_QueryDynamicActorObstruction` `003357B0`, `BattleLocomotion_BuildSolverContext` `00336710`, `BattleLocomotion_ResolveTargetSpacingAndAvoidance` `00338140`, `PartyFollow_SolveFormation` `00338490`, `00326D60`, `003278D0`, `003377C0`, `0033C310`, `0033CEF0` and `0033D200` call `BattleUnit_GetBySlotIndex` `00236820`, and `00326D60`, `003278D0`, `00337C10` and `00337D90` call `BattleUnit_GetSlotCount` `00236850`; `00335760` and `00338490` call `ActorRuntime_GetClassNibble` `00263C20`; `BattleLocomotion_DecodeOrderGoal` `00312730`, `00336710`, `00337A50` and `00338140` call `BattleUnit_ResolveByFocusHandle` `0031B7E0`; `0025B470`, `0026C3E0`, `002E28E0`, `00310920` and `00313670` call `00377C20`. In the other direction the standard action state `BattleUnit_AdvanceStandardActionState` `00304850` calls `BattleLocomotion_SetApproachAndReferenceTargets` `00319110`, `BattleUnit_UpdateCombatNavigationStep` `00325BB0`, `BattleLocomotion_ResetPathAndSetTargets` `003291B0` and `0033A1E0`; the cancel `BattleUnit_CancelAndResetCurrentAction` `003105D0` calls `003291B0` and `0033C9B0`; `003291B0` calls `Navigation_ResetPathPredecessors` `003839F0`; and `0033C9B0`, called by `00325BB0`, calls `00336710` and `BattleLocomotion_ResetAvoidanceStateRandomized` `0033E1F0`. Locomotion walks the same unit table, class nibble and focus resolver the leader broadcast uses, and an action's approach, and its cancel, reset the locomotion path and avoidance state; the commit hands movement its targets and does not own the solver.

**Party — SERVICE and CLIENT (12 edges).** `00304850`, `00309990`, `BattleAction_ReleasePresentationSlot` `0030C970`, `BattleUnit_CommitAction` `0030F760`, `BattleUnit_ReleaseTargetRelationAndActionState` `00310780` and `00313120` call `0031B7E0`, and `00304850` also calls `PartyFocus_IsCurrentPackedActorHandle` `003273B0`; the enmity delegate `003220E0` calls `PartyFocus_SelectAndRequestDefaultActor` `00326500`; `PartyConfiguration_ReconcileRosterFromCurrentSelectors` `003261D0` and `PartyConfiguration_SetSelectorsAndReconcileRoster` `003273D0` call `00236820`, and `003273D0` calls `00236850`; `00304180` calls `00377C20`. Every slot handle and target on this page is a focus handle the party layer resolves, the enmity delegate can ask the party layer to pick a default actor, and the roster code shares the unit-table accessors.

**Presentation — SERVICE and CLIENT (7 edges).** `0030F760` (at `0030F975`) and `00310780` call `BattleUnit_BroadcastPartyCombatTargetRelation` `00313B30`, which calls `CharacterRender_DispatchCombatRelationEvent` `002ED2A0`; `PartyCombat_UpdateStanceState` `00307E70`, `BattleUnit_ComputePresentationSuppressionMask` `003125E0`, `00313B30` and `AddMotion_ApplyBonePose` `003714A0` call `00377C20`. The commit's enmity registration broadcasts the new target relation to the character renderer, and stance, suppression and bone-pose code read the same field bit; the commit decides the relation and the renderer shows it.

**Script_VM_Native_Bridge — CLIENT (5 edges).** `003495A0` calls `00313120`, and `00344740`, `00352FA0`, `003537D0` and `00355680` call `00377C20`. `00313120` is the special-sequence stage that moves `+0x694` into `+0x695`, re-fills the target buffer and dispatches a presentation event, and a script body can run it directly; four script bodies read the field bit.

**Status_Periodic_Terminal — SERVICE and CLIENT (6 edges).** `00304850` calls `BattleStats_ChangeStatusAndProcessSideEffects` `0030E360`; `BattleUnit_ResetActionControlForStatusTransition` `00300140` and `BattleUnit_RecoverFromTerminalStatusSetIfClear` `00301140` call the cancel `003105D0`; `0030E360`, `BattleStats_RemoveStatusesFromMaskAndRecompute` `0030F690` and `BattleUnit_RunPeriodicCombatMaintenance` `00310DB0` call `00377C20`. A status transition cancels the current action through this page's cancel, the standard action state can change a status, and the status code reads the field bit that waives disabling statuses.

**UI — CLIENT (14 edges).** `BattleMenu_BuildCommandEntryList` `0031EB20` and `00322A80` call `00236820` and `00236850`, and `0031EB20` calls `0031B7E0`; `002734F0`, `BattleMenu_RecordSelectedTargetAndCursorContext` `0027D330`, `002BF0E0`, `002C7660`, `00322A80`, `003C5130` and `003C8B70` call `00263C20`; `0027FB70` calls `00300060`; `BattleAction_UpdateSpecialPresentationSequence` `00306760` calls `0035C620`, a 12-byte stub that tail-jumps into a UI body with one fixed UI object. Menus read the unit table, the class nibble and the focus resolver, and `00300060` (which walks the flagged units and reads each one's action id at `+0x714` against the action rows) is called from a menu body; the special sequence pokes one UI object. None of these writes the commit's state.

## Interior citation — frontier hub `0030AB40` (2026-09-18, SWE2-EC7)

`0030AB40` — 266 B, 13 callers; `BattleTarget_ClassifyRelationshipClass`, the `> 1` gate
this page's broadcast already names. Interior verified: null-guards on both operands
(`0030AB64`/`0030AB6D`), `r8d & 1` saved as a flag (`0030AB54`–`0030AB5C`), then
`00263C20` — `ActorRuntime_GetClassNibble`, measured this batch — reads the class nibble of
each side's `[+0x10]` record ([`0030AB7F`/`0030AB8B`](../_index/ADDRESS-INDEX.md)). Nibble
5 on either is an early-out (`0030AB93`–`0030ABA0`); both records must carry flag `0x10` at
`+0` (`0030ABA6`–`0030ABB2`); the classification proper reads `+0x698` lists from both
operands ([`0030ABB8`](../_index/ADDRESS-INDEX.md)). This is the relationship matrix the
"greater than 1" threshold compares against.

## Homed frontier bodies called from this page's functions (FABLE, 2026-10-02, cloud-drafted)

*Functions no page cited until now. Each is entered directly from a function this page already cites (the site is given as caller + offset). Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's homing pack and re-read by FABLE against the certified image; verified by [`homing_applier.py`](../_index/candidates/fable-home-the-moment-an-action-is-committed-1002/homing_applier.py): every site transfers to its function, the page cites the caller, and every anchor is an instruction boundary inside its function that decodes to the recorded mnemonic.*

| function | size | entered from | what the body does | interior anchors |
|---|---|---|---|---|
| `00310D30` | 94 B | `00310920` + 0x147 | calls `00310D30` + 0x15 with the incoming registers and returns when it yields null; otherwise, on that returned pointer, calls + 0x33 with the three floats at `rcx+0x0`, `rcx+0x4` and `rcx+0x8` in `xmm1`, `xmm2` and `xmm3`, then calls + 0x3E and + 0x49 each with the incoming float `xmm1` | Interior anchor `00310D45`; Interior anchor `00310D50`; Interior anchor `00310D63`; Interior anchor `00310D6E`; Interior anchor `00310D79` |
