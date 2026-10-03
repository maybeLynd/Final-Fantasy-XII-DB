---
system: Battle action handler table
category: 07-Combat-Action
status: DOCUMENTED
owner_layer: CombatAction (dispatch) + CombatAI (precondition)
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
  method: unnamed-pointer-run census over all data sections; capstone read of both
    referencing functions; table walked over the range its own bound check defines
last_reviewed: 2026-09-12
registry_slots:
  - "0x02EBF188"
audit:
  passes: 4
  last_pass: 2026-09-02
  last_pass_state: survived-and-gained-a-third-consumer
  crossref_clean: true
  reopened_count: 0
---

# Battle action handler table

> **A unit's action id is one of two disjoint spaces sharing one field.** Ids **at or below `0x21E`**
> are ordinary actions and carry a **target buffer** — that is where the player's Attack, Magick,
> Technick and Item selections live. Ids **`0x4000`–`0x4166`** are **internal orders** with no target,
> and it is those 359 that this table dispatches. **An empty slot means the order does not exist**:
> the AI will not consider it and dispatch refuses it.
>
> **CORRECTED 2026-09-02.** This document previously opened *"every action a unit can take in battle
> carries an id between `0x4000` and `0x4166`"*. **That was wrong** — it described the order space as
> if it were the action space. Section 9.

**For a player.** Almost nothing here is a menu entry. This table drives what a unit does *between*
and *around* the things you choose — moving into range, turning, changing state, gaining and losing
statuses. Your Attack, your Magick, your Item all take the **other** path, because they need a
**target**, and this space has no target buffer at all.

That is also why **249 of the 341 live ids share one handler**: they were never 249 abilities. Large
runs of them are the *same* order with a number attached — 64 ids in this space are literally
"set status *n*" and "clear status *n*" for 32 values of *n* (section 10).

---

## 1. The table

| | |
|---|---|
| base | **`0x01EEC460`** |
| slots | **359** (`0x4000` .. `0x4166`) |
| span | `0x01EEC460` .. `0x01EECF90` |
| index | `actionId - 0x4000` |
| bound | `if ((unsigned)(actionId - 0x4000) > 0x166) reject` |
| live entries | **341** |
| empty entries | **18** |
| distinct handlers | **8** |

## 2. Both consumers, read in full

> **EI-2 answered by this page and its neighbours (2026-09-12, FABLE): what lies above action id
> 542 is the order space.** `BattleUnit_AdvanceActionState` (§11) sends a `+0x714` word above `0x21E`
> to `BattleUnit_AdvanceExtendedActionState`, and that function is nothing but the order
> dispatcher read below: it first posts presentation event `0x2001` — or `0x2010` for a party-table
> unit of type `0x1A` while the registry-slot `02EBF190` record's `+0x5AE0` has bit 1
> (`003050A0`–`003050CB`, `BattleUnit_DispatchActorPresentationEvent`) — then tail-jumps to the
> handler at `01EEC460[id − 0x4000]`, returning `−1` for an id outside `0x4000`–`0x4166` or an empty
> slot (`003050D0`–`0030510E`). So the "eighth of the machinery" is the 359-id AI-order vocabulary
> this page maps (locomotion goals, direct state commands, waits — [the locomotion page](../../06-Movement-And-Navigation/Battle-Locomotion/battle-locomotion-steering-and-recovery.md)), and
> `BattleAction_CheckTargetEligibility` rejects the ids because an order carries no action target:
> the goal decoders resolve their own (§8). Nothing above `0x21E` is an action.

**Dispatch** - `00305080` `BattleUnit_AdvanceExtendedActionState`, owner `CombatAction`:

```asm
003050D0  movzx eax, di                    ; actionId
003050D3  add   eax, 0xFFFFC000            ; -= 0x4000
003050D8  cmp   eax, 0x166
003050DD  ja    0x305101                   ; out of range -> return -1
003050DF  cdqe
003050E1  lea   rdx, [rip + 0x1BE7378]     ; -> 0x01EEC460
003050E8  mov   rdx, [rdx + rax*8]
003050EC  test  rdx, rdx
003050EF  je    0x305101                   ; empty slot  -> return -1
003050F1  mov   rcx, rbx                   ; this = the battle unit
003050FE  jmp   rdx                        ; TAIL-CALL the handler
```

**Precondition** - `00301830` `AiOrder_CheckActionPreconditions`, owner `CombatAI`:

```asm
003018DD  lea   eax, [rdx - 0x4000]
003018E3  cmp   eax, 0x166
003018E8  ja    reject
003018F0  lea   rcx, [rip + 0x1BEAB69]     ; -> 0x01EEC460
003018F7  cmp   qword ptr [rcx + rax*8], rsi   ; rsi = 0
003018FB  je    reject                     ; empty slot -> action not available
          ... then id-specific tests: 0x4124, 0x4022, 0x4050, 0x4091 ...
```

**These two are the whole story: the table is referenced by exactly two instructions in the
executable, and both are these.** A corrected scan over all three addressing forms - rip-relative,
image-base + RVA + index, and absolute - finds no other reference anywhere.

The pair is a clean **"may I?" / "do it"** split: the AI reads the same slot the dispatcher will use,
and treats null as *unavailable* rather than discovering it at execution time. Compare
[battle command availability and reason codes](../Action-Availability/battle-command-availability-and-reason-codes.md),
which is the *player-facing* availability test; this is the AI-facing one.

## 3. The handlers

| count | address | name | size |
|---:|---|---|---:|
| **249** | `002FDDA0` | `BattleUnit_ExecuteDirectStateCommandOrder` | 1,937 B |
| 57 | `002FDA60` | `caseD_4000` — **the goal-following handler** (read whole 2026-09-12, FABLE: phase byte `+0x6B4`, goal from `BattleLocomotion_DecodeOrderGoal`, ends on `BattleLocomotion_IsApproachConstraintActive`; [the locomotion page](../../06-Movement-And-Navigation/Battle-Locomotion/battle-locomotion-steering-and-recovery.md), DE-3) | 464 B |
| 25 | `002FDC30` | `BattleUnit_AdvanceTargetedMovementOrder` | 353 B |
| 6 | `002FE660` | — | 282 B |
| 1 | `002FE7D0` | **the wait handler of `0x4021`** (read 2026-09-12, FABLE — §5); absent from the function census because nothing calls or jumps to it | 106 B |
| 1 | `002FE840` | — | 137 B |
| 1 | `002FE8D0` | — | 56 B |
| 1 | `002FE910` | — | 52 B |

**73 % of live actions share one handler.** Three handlers cover 331 of 341. The remaining five
handlers serve one or six ids each - the genuinely special cases.

**What the handlers are named is the GFZ's judgement, not a reading.** `ExecuteDirectStateCommandOrder`
and `AdvanceTargetedMovementOrder` are suggestive of a command/movement split and are **not treated
as evidence here**. What is measured is the shape: one dominant handler, two secondary, five
singletons. **AT-1.**

## 4. The empty slots

```
0x4025
0x4036 0x4037 0x4038 0x4039 0x403A 0x403B 0x403C 0x403D
0x403E 0x403F 0x4040 0x4041 0x4042 0x4043 0x4044 0x4045
0x4128
```

**Sixteen consecutive ids, `0x4036`-`0x4045`, are empty**, plus two isolated ones. A contiguous block
of exactly sixteen reads as a reserved range that was never populated - but *reads as* is not
evidence, and nothing here says what they were for. **AT-2.**

> **AT-2 closed 2026-09-12 (FABLE) — the purpose is not in the image; the shape is.** Four whole-image
> facts. **(1) Neighbours:** the block sits between the sixteen *go-to-the-unit-with-definition-
> selector-n* ids `0x4026`–`0x4035` (one shared handler `002367A0`, index = id − `0x4026`, [the locomotion page](../../06-Movement-And-Navigation/Battle-Locomotion/battle-locomotion-steering-and-recovery.md))
> and the direct-state family that `BattleUnit_ExecuteDirectStateCommandOrder` opens at `0x4046`
> (`002FDE08`: `sub 0x4046; cmp 0x4B`) — a sixteen-wide gap exactly the width of the sixteen-wide
> family before it. **(2) The decoder rejects it:** `BattleLocomotion_DecodeOrderGoal` sends every id
> above `0x4035` to one arm (`0031297D`) that matches only `0x4124`, `0x4125`, `0x414A`, `0x414E` and
> `0x4165` and returns 0 for the rest. **(3) No authored data uses it:** the 50,050 shipped enemy-order
> records name `0x4020` ×973, `0x4021` ×3,018, `0x4023` ×2,111, `0x4024` ×1,845, then nothing until
> `0x4046` ×281 — no record in `0x4025`–`0x4045` (so `0x4026`–`0x4035` are handled but unused too).
> **(4) No code names it in this id space:** an image-wide scan of every instruction immediate in
> `0x4035`–`0x4046` finds only other spaces — the animation-event ids `0x4035` / `0x4036` that
> `00426130` passes to `00427320` on the `0x740`-stride animation object (the `0x2008`-style
> presentation events, not orders), a colour triple `0x4040` / `0x40` at `002C82A3`, and stack
> offsets. What the sixteen were *for* is authoring history the image does not carry; what a
> reconstruction needs is that they are rejected everywhere and never authored.

**`0x4025` is not arbitrary.** It is the first id *past* the locomotion-order sub-range that
`BattleLocomotion_DecodeOrderGoal` bounds at `0x4024` - two independent derivations meeting at the
same id. Section 7.

The first and last slots are both live (`0x4000` and `0x4166`), so the table is not padded at either
end; 359 is its real extent, fixed by the bound check rather than inferred from where the pointers
stop.

## 5. Two corrections this pass had to make to its own method

**The table is not four tables.** The pointer-run census reported four separate runs here - 33, 16,
226 and 62 slots. They are one table; the runs break at null entries and at one address the census
does not recognise. `33 + 16 + 226 + 62 = 337`, and the true count of live entries is **341**. The
four missing entries sit in the "gap" at `0x01EEC568`, which holds `002FE7D0` followed by three more
live pointers. **A run-splitting scan reports the shape of its own break rule, not the shape of the
data** - which is why the extent here is taken from the *bound check in the code*, not from where the
pointers happen to stop.

**`002FE7D0` is a live handler that the function census does not contain.** It is dispatched to by
the same tail-jump as the other 340 and has no entry in `functions.tsv`, so it has no size, no
domain and no owner. That is a gap in the ledger, not in this table. **AT-3.**

> **AT-3 answered 2026-09-12 (FABLE).** *Why it is missing:* a scan of every `call` and `jmp` in every
> censused function finds **no direct reference to `002FE7D0`** — its only reference is the pointer in
> this table (slot `0x4021`, and no other slot), which the auto-analysis does not follow as code, so no
> function was ever defined there. The bytes decode cleanly as a self-contained **106-byte function**
> (`002FE7D0`–`002FE839`, then `int3` padding to `002FE840`). *What it is:* **the `0x4021` "wait"
> handler.** Phase byte `+0x6B4` 0: zero `+0x750` (the follower copy of the group target focus,
> [the battle-unit field map](../../04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md)) and advance to phase 1 (`002FE7F0`–`002FE7FB`); phase 1: with the order's second word
> `n` (`[order + 2]`, `002FE801`), complete — phase 2, return 1 — once the action age counter `+0x75C`
> reaches `n × trunc(1.0 × 30.0)` = **`30 n` advances** (`002FE80B`–`002FE836`; the floats at `01DFE0B8`
> and `008F8D80`); **`n = 0` never completes** (`002FE806`–`002FE809`, returns 0 each tick), which is the
> engine's own default record `{0x4021, 0}` at `01EEC298` ([the locomotion page](../../06-Movement-And-Navigation/Battle-Locomotion/battle-locomotion-steering-and-recovery.md), DE-2) — idle until
> something else is chosen. In the shipped enemy order sets the 3,018 `0x4021` records carry `n` = 0
> (1,315), 1 (354), 2 (581), 3 (78), 4 (622), 5–12 (68): a wait of up to twelve units.

An earlier attempt at this section over-extended the table to 380 slots by walking outward until the
values stopped looking like pointers. That swept in numeric data - `0x3F000000` is `0.5f` - and was
wrong. **The bound check is the authority on how long a table is.**

## 6. What is not known

- What distinguishes the 249 ids sharing one handler. The answer is presumably in the action's
  authored record, not in this table. **AT-4.**
- Which ids correspond to which player-visible commands. This table gives the id space and the
  dispatch; it does not name a single action. **AT-5.**
- Whether the id-specific tests in `AiOrder_CheckActionPreconditions` (`0x4124`, `0x4022`, `0x4050`,
  `0x4091`) are gambit-relevant special cases. **AT-6.**

  > **AT-6 answered 2026-09-12 (FABLE): not gambit cases — enemy-order preconditions, read whole.**
  > `AiOrder_CheckActionPreconditions(unit, order)` (`00301830`) has one caller,
  > `AiOrder_EvaluateAndResolveActionTarget` (`003015DA`), itself reached only from
  > `BattleUnit_TrySelectAndCommitAiOrderFromSet` (`00305DD2`) — the enemy order-set walk of
  > [the gambit page](../../09-Combat-AI-And-Gambits/gambit-evaluation-and-enmity.md); a party member's gambits never pass through it. It copies the unit's
  > 0x620-byte context at `+0x80` to the stack, requires the order's id in this table's band with a
  > live slot (`003018DD`–`003018FB`), and then branches on the id:
  >
  > | order id | precondition |
  > |---|---|
  > | `0x4022`, `0x4124` | **a goal decode**: the context copy's float `+0xD4` (unit `+0x154`) must not be negative (`00301975`–`00301980`), `BattleLocomotion_DecodeOrderGoal(unit, order, &a, &b, &dist)` must succeed (`003019A9`, [the locomotion order decoder](../../06-Movement-And-Navigation/Battle-Locomotion/battle-locomotion-steering-and-recovery.md)), `dist` gains the constant at `009153EC` and `BattleLocomotion_IsApproachConstraintActive(copy, id)` must return 0 (`003019E4`); **`0x4022` alone** then stores `BattleRuntime_GetModeDependentDistanceThreshold()` at unit `+0x6D0` and the decoded vector at `+0x6C0` (`003019F5`–`00301A0F`) |
  > | `0x4051`–`0x4121` except `0x4091`; `0x414B` | **a percent roll on the record's second word**: 0 passes outright, otherwise `RNG_SharedGameplayLCG_NextU32 % 100 < word` (`0030193B`–`00301969`, [the shared gameplay LCG](../../21-RNG-And-Determinism/rng-streams.md)) |
  > | `0x414D` | for a party-kind unit (`[+0x698]+5 == 0`) `BattleUnit_ComputePartyBattleStance(unit)`, otherwise `BattleUnit_HasNonPartyEngagementEvidence(unit, 0)`, **XOR unit flag bit 23** (`00301A62`–`00301AA2`) |
  > | `0x4165` | `BattleLocomotion_DecodeOrderGoal`'s result alone (`00301A38`–`00301A60`) |
  > | everything else in the band (`≤ 0x4050`, `0x4091`, `0x4122`–`0x4123`, `0x4125`–`0x414A`, `0x414C`, `0x414E`–`0x4164`, `0x4166`) | none — returns 1 (`00301A31`) |
  >
  > So `0x4050` and `0x4091` are the *edges* of the rolled band, not cases of their own. **What the
  > shipped enemy order sets use** (50,050 records in the 166 `in` area files): `0x4022`, `0x4124`,
  > `0x4050`, `0x4091` and `0x414D` **never occur**; `0x414B` 1,735 times (second word 0 ×1,711,
  > 100 ×24) and `0x4165` 22 times; the rolled band 20,361 times, its second word 100 (18,784), 0
  > (359) or a real chance 5–80 (1,218 — almost all in the `0x4116`–`0x411F` family: `0x411D` ×310,
  > `0x411C` ×181, `0x411B` ×174 …). The resolver applies the same roll to a **raw action order**
  > (`< 0x4000`, 6,002 records — `150` Attack ×799, `51` Protect, `52` Shell, `60` Silence …) after
  > `BattleAction_CheckActionAvailabilityReason` (`0030160F`–`00301637`; second word 0 ×3,043, else
  > 5–100), and to a weighted `0x8xxx` selector after resolution (`003014F6`). So **the order
  > record's second word is a percent chance for actions and for the rolled band**, and an operand
  > of another kind for the rest of the band (values 1, 2, 4, 31, negatives, 260–340 occur there).

## Open questions

- [x] ~~Whether the handler names imply a command/movement split.~~ **SUPPORTED** — the id partition
      matches the names: the movement handler serves the locomotion block, the state handler owns the
      status-change runs. Section 11. **AT-1.**
- [x] ~~What the sixteen consecutive empty ids `0x4036`-`0x4045` were reserved for.~~ **AT-2 closed
      2026-09-12 (FABLE): not in the image** — the block is a sixteen-wide gap between the sixteen
      definition-selector ids and the direct-state family, rejected by the goal decoder, absent from
      all 50,050 shipped order records, and named by no immediate in the order id space (§4).
- [x] ~~Why `002FE7D0` is absent from the function census.~~ **AT-3 answered 2026-09-12 (FABLE):** nothing calls or jumps to it — the table pointer is its only reference; it is the 106-byte `0x4021` wait handler (§5).
- [x] ~~What distinguishes the 249 ids that share `002FDDA0`.~~ **ANSWERED — mostly nothing does.**
      Nested switches resolve 130 ids to 11 bodies, and **64 of them are `set status n` / `clear
      status n` for 32 values of *n***, where the id's low bits are a parameter. Section 10. **AT-4.**
- [x] ~~Which action ids map to which player-visible commands.~~ **CLOSED as far as this binary
      allows** — the question was mis-posed (this table holds orders, not commands) and the naming
      half is a hard negative: **the executable contains no action-name table**. Section 11. **AT-5.**
- [x] What the `<= 0x21E` action space contains — 543 ids, target-carrying, the player's actual
      commands. Needs authored records from outside the executable. **AT-8.**
      *Answered by reference 2026-09-14 (FABLE, `OPUS-REQ-FABLE-AT8-DISPOSITION`), box left for the ledger mirror:* the
      space's contents are read, not only its file. Each id is one 60-byte row of the action table (`battle_pack.bin`
      directory `+0x3C`; `action_data.bin` is a copy). [The action definition row](../Action-Definition-Row/the-action-definition-row.md)
      tallies every byte of all 543 rows and cites a reader for each named field. The category `+0x1E` separates magicks (81),
      technicks (24), item uses (51) and the other kinds; `+0x34` names each row through bank 0 of the battle text; the
      power, recipe, charge, element, status, License and Esper fields are named there. The bytes still marked "shape only"
      on that page are that page's open questions about field meaning, not a gap in what the space contains.
- [x] ~~What command ids `0x113` and `0x95` are. The only two the engine hard-codes, tested against
      `BattleUnit+0xBA0` in five functions.~~ **AT-9 ANSWERED 2026-09-11:** `0x113` is **Dismiss** and
      `0x95` **Dismount** — bank 0 of [the battle text banks](../../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/battle-text-banks.md)
      at the rows' own `+0x34` index; the two commands that end an Esper summon and a chocobo ride
      are the ones the engine keeps issuable and remembers at `+0xBA0`.
- [x] ~~Whether `0x4124` / `0x4022` / `0x4050` / `0x4091` are gambit special cases.~~ **AT-6 answered 2026-09-12 (FABLE):** enemy-order preconditions — a goal decode for `0x4022` / `0x4124` / `0x4165`, a percent roll on the record's second word for `0x4051`–`0x4121` (minus `0x4091`) and `0x414B`, a stance test for `0x414D`; the four ids are the cases' edges (the note under the AT-6 bullet above).
- [x] ~~What the byte table at `BattleLocomotion_DecodeOrderGoal` maps ids to.~~ **ANSWERED** - it is
      a **switch case-index table**, not a goal map: 37 ids, **6 cases**, 32 sharing case 0, and
      `0x4021` deliberately routed to the reject body. Section 8. **AT-7.**
- [x] ~~What register the `-0x3FFF` adjustment in case 0 applies to, and whether it is an id-to-index
      conversion.~~ **DE-4** *(relabelled 2026-09-14, FABLE: this box carried `AT-8`, which is the action-space
      question above; the register tracks this one as `DE-4`)*. **ANSWERED 2026-09-12:** the value is the order opcode,
      and `opcode − 0x3FFF` is the one-based record number `00312DF0` fetches from the area's `FF12POS3` position table.
      The zeroed pointer is the NULL reference that selects the table path.

## 7. Falsification pass 2026-09-02 - survived, and the id space is confirmed from outside

**Three attacks, chosen against the three claims that would hurt most if wrong.**

### Attack 1 - "referenced by exactly two instructions" (survived)

A scan for the table base as an 8-byte value in **every data section** finds **none**. Nothing stores
a pointer to it, so there is no indirect consumer hiding behind a global. Combined with the corrected
three-form instruction scan, the two references are the complete set.

### Attack 2 - "359 slots" (survived)

`cmp <reg>, 0x166` occurs in **exactly two places in the executable**, and they are the two functions
in section 2. No third consumer shares the bound, and no consumer uses a *different* bound on the
same table - which would have meant the extent was a per-caller convention rather than the table's.

### Attack 3 - "0x2001 is a sibling id space" (**refuted, and it was my own hypothesis**)

`BattleUnit_AdvanceExtendedActionState` loads `edx, 0x2001` immediately before the dispatch, which
looked like a parallel `0x2000`-based space. **Zero functions in the image subtract `0x2000` from
anything.** `0x2001` is an ordinary constant argument to
`BattleUnit_DispatchActorPresentationEvent`, not a base. The hypothesis is dead.

### What the attack found instead: a third subsystem in the same id space

Sixteen sites in thirteen functions touch `0x4000`. Most are unrelated - `002D8050` uses it as a
pointer-alignment constant (`and rax, ~0x3FFF` / `add rax, 0x4000`), which is exactly the kind of
coincidence that makes a bare constant search worthless on its own. **One is not:**

```asm
00312730  BattleLocomotion_DecodeOrderGoal        [owner: Movement, 965 B]
   00312798  sub   ecx, 0x4000
   0031279E  cmp   ecx, 0x24                 ; ids 0x4000 .. 0x4024  (37)
   003127A1  ja    reject
   003127AA  lea   r8, [rip - 0x1F27B1]
   003127B1  movzx eax, byte ptr [r8 + rax + 0x1F2B10]   ; BYTE table, not pointers
```

**Movement decodes the same `0x4000`-based id through its own byte table.** Two subsystems, two
different tables, one id space - which is far stronger evidence that `0x4000` is a real id base than
a single `sub` in one function could ever be.

### The boundary agrees, and that is the sharpest result

Movement's range is `0x4000`-**`0x4024`**. This table's **first empty slot is `0x4025`**.

The two were derived independently - one from a `cmp 0x24` bound in Movement, the other from reading
361 qwords out of `.data` - and they meet exactly at the same id. **The low block of the action id
space is locomotion orders**, and the null at `0x4025` is the end of that block rather than an
arbitrary hole.

That also explains the handler named `caseD_4000` (57 slots): the slot map puts almost all of its
entries at the bottom of the range, where Movement's orders live. See
[battle locomotion steering and recovery](../../06-Movement-And-Navigation/Battle-Locomotion/battle-locomotion-steering-and-recovery.md).

**Not claimed:** that ids `0x4000`-`0x4024` are *only* locomotion, or that the byte table's values
are goals rather than an index into something further. Both need the byte table read. **AT-7.**

## 8. The locomotion sub-range decoded - AT-7 answered

The byte table in `BattleLocomotion_DecodeOrderGoal` is **not** a map from order id to goal. It is
the index half of an ordinary MSVC two-level switch:

```asm
00312798  sub   ecx, 0x4000
0031279E  cmp   ecx, 0x24                            ; 37 ids
003127A1  ja    0x312AD4                             ; -> default
003127AA  lea   r8, [rip - 0x1F27B1]                 ; r8 = image base 0x00120000
003127B1  movzx eax, byte ptr [r8 + rax + 0x1F2B10]  ; BYTE  case index
003127BA  mov   ecx, dword ptr [r8 + rax*4 + 0x1F2AF8] ; DWORD case offset
003127C2  add   rcx, r8
003127C5  jmp   rcx
```

**Layout:** dword offsets at `0x00312AF8` (6 entries, 24 bytes), byte indices immediately after at
`0x00312B10` (37 entries) - both inside `.text`, past the function body.

### 37 ids, 6 cases, and 32 of them share one

| case | body | ids |
|---:|---|---|
| **0** | `003127C7` | **`0x4000`-`0x401F`** - 32 ids |
| 1 | `003127D7` | `0x4020` |
| 5 | `00312AD4` | `0x4021` - **this is the default/reject body**, shared with out-of-range |
| 2 | `0031289E` | `0x4022` |
| 3 | `00312804` | `0x4023` |
| 4 | `00312913` | `0x4024` |

`0x4021` being routed to the same body the bound check rejects to means **that id explicitly resolves
to no goal** - it is not missing, it is deliberately null. The body returns `eax = 0` and restores.

### The special cases read the battle record

Three of the five reach into the actor's own record at offsets this database has already documented
in [the battle record kind byte](../../04-Actor-Entity/Battle-Record-Kind/battle-record-kind-byte.md)
(`unit+0x6A0` = record base, `unit+0x698` = base+0x80, kind at `record[5]`):

```asm
case 1 (0x4020)   mov rax,[rdi+0x698] / test rax,rax / je default
                  cmp byte ptr [rax+5], 1           <- the KIND byte, tested against 1
                  mov rcx,[rdi+0x6A0] / add rcx,0x50 <- the record base + 0x50
case 2 (0x4022)   mov rax,[rdi+0x698] / movzx eax, byte ptr [rax+5]   <- kind byte as a VALUE
case 3 (0x4023)   mov ecx,[rdi+0x710] / call 0x31B7E0                 <- lookup by an id on the unit
case 4 (0x4024)   call 0x3272A0 / cmp rax, rdi                        <- fetch an actor, compare to self
```

**This is independent corroboration of the record layout**, arrived at from a different subsystem
(Movement) than the document that established it. `+0x698` -> `[+5]` and `+0x6A0` both appear here
exactly as recorded.

Case 0 - the 32-id majority - adjusts a value by `-0x3FFF`, zeroes a pointer argument and joins
common code at `0x312A60`. **`-0x3FFF` is `-(0x4000 - 1)`, which is suggestive of an id-to-one-based
index conversion and is not treated as established** - the register's contents at that point are not
traced here. ~~**AT-8.**~~ **DE-4, answered 2026-09-12:** it is that conversion. `opcode − 0x3FFF` is the one-based
record number of the area's `FF12POS3` position table, and the zeroed pointer is the NULL reference.

### AT-7 answered

The byte table's values are **case indices, not goals**. The 37 locomotion order ids have **six**
distinct resolution behaviours, 32 sharing the first. Whether the sub-range is *exclusively*
locomotion is still not shown - what is shown is that Movement's decoder accepts exactly
`0x4000`-`0x4024` and that five of those ids get bespoke goal resolution.

### A method error caught in this pass

The dword table address was first taken as "immediately after the byte table" - an assumption - and
that produced offsets of `0xCCCCCCCC` (`int3` padding) and three values that were plainly instruction
bytes. **The instruction states the address: `0x1F2AF8`.** It was in the disassembly already
transcribed into this document.

**The tables are laid out dwords-first, bytes-second**, the reverse of the reading order, so
"the table after the one I found" was wrong by construction. Recorded because the wrong answer was
*checkable in one glance* - `0xCCCCCCCC` is never a code offset - and the check is what caught it.

## 9. Two id spaces in one field — the correction

`BattleUnit_CommitAction` (`0030F760`, owner `CombatAction`) branches on the id **before** storing it,
and the branch is the whole story:

```asm
0030F798  mov   r13d, 0x21E
0030F7A1  cmp   di, r13w
0030F7A5  ja    0x30F7D9              ; > 0x21E -> the extended space
          ;--- id <= 0x21E : ordinary action, TAKES A TARGET ---
0030F7B3  call  BattleTargetBuffer_ResetPreservingFlag0      (rcx = unit + 0x778)
0030F7CD  call  BattleTargetBuffer_TryAppendActorWork
0030F7D7  jmp   store
          ;--- id > 0x21E : extended order, validate against THIS table ---
0030F7D9  mov   ecx, 0x4000
0030F7E1  sub   ax, cx
0030F7E4  mov   ecx, 0x166
0030F7E9  cmp   ax, cx
0030F7EC  ja    reject
          ;--- both paths converge ---
0030F806  mov   word ptr [rbx + 0x714], di
```

| space | count | target buffer | dispatched by |
|---|---:|---|---|
| **`0x0000`–`0x21E`** | 543 | **yes** — `unit+0x778` | not this table |
| **`0x4000`–`0x4166`** | 359 | **no** | **this table** |

**`BattleUnit+0x714` holds either kind**, which is why the dispatcher in section 2 subtracts `0x4000`
and bounds at `0x166` — it is reading the same field and must first establish which space it is in.

The same store also fills `+0x708` (a pointer), `+0x710` (a focus handle, resolved by
`BattleUnit_ResolveByFocusHandle` — the same call the
[locomotion order decoder](../../06-Movement-And-Navigation/Battle-Locomotion/battle-locomotion-steering-and-recovery.md)
makes from `[unit+0x710]`), and masks `+0x700`.

**Per the standard, the writers decide.** `BattleUnit+0x714` has exactly **three** writers image-wide:
`BattleUnit_CommitAction`, `BattleUnit_ResetStateForReuse` and `BattleUnit_CancelAndResetCurrentAction`.
~~Four~~ Nine other `[reg+0x714]` writes, in eight bodies, exist and are **different structures** — ~~three store the float~~
~~`0x3F490FDB` (π/4) and one is `Audio`.~~ five store the float `0x3F490FDB` (π/4), in `007084E0`, `00708540`, `007085A0` and `00708600`, and the others are in `00542740`, `006FEF20`, `00708470` and `007D2150` *(corrected 2026-10-02, OPUS: `retool.py grep "+ 0x714],"`, nine sites, one in each of those functions (two in `00708600`), listed in FABLE's record readiness-apply-fable-1002; a census over the known extents, so a lower bound)*. Separated by operand size and owner, not assumed away.

### The player's command id is a different field again

`BattleUnit_IssueCommand` (`00311CF0`) is the **only** writer of **`BattleUnit+0xBA0`**, the issued
command id. Combat code tests `+0xBA0` against exactly two constants, repeatedly and in five separate
functions: **`0x113`** and **`0x95`** — both in the `<= 0x21E` space. `0x113` is also special-cased
inside `IssueCommand` itself.

**They are the only command ids the engine hard-codes.** What they are is not established — naming
them needs data this executable does not contain. **AT-9.** *(Answered since — `AT-9`, 2026-09-11: `0x113` is Dismiss and `0x95` Dismount, from the battle text; the struck checkbox under *Open questions*.)*

## 10. AT-4 answered — the large runs are `base + index`, not distinct commands

The handlers that appeared to swallow hundreds of ids contain **nested switches keyed on the id**,
recovered structurally with entry counts taken from each `cmp` bound:

| handler | switch at | ids | count |
|---|---|---|---:|
| `BattleUnit_ExecuteDirectStateCommandOrder` | `002FDE37` | `0x4046`–`0x4091` | 76 |
| `FUN_002FE660` | `002FE718` | `0x4122`–`0x4157` | 54 |

**130 ids resolve to 11 distinct case bodies**, and two of those bodies are the interesting ones:

```
0x4051 - 0x4070   (32 ids)  ->  BattleStats_ChangeStatusAndProcessSideEffects(s, s, id-0x51, -1, .., 0, 3)
0x4071 - 0x4090   (32 ids)  ->  the same callee with                        (id-0x71,  0, .., 0, 0)
```

**Two 32-wide runs, one callee, the same selector arithmetic, different mode arguments** — set-status
and clear-status for 32 statuses. **In those runs the id's low bits are a parameter, not a command.**
That is the general shape of this space, and it is the answer to *"what distinguishes the 249 ids that
share one handler"*: mostly nothing does, because they are one order with an index.

**A trap worth recording.** In `FUN_002FE660`'s switch, 48 of the 54 ids land on `or eax, -1; ret` —
which is the **default arm**, not a shared behaviour. Read as a group it would have been the largest
"behaviour" in the space; it is the opposite of one. Only `0x4122`/`0x4156`, `0x4123`/`0x4157` and
`0x4149` have real bodies.

## 11. AT-5 — the question was mis-posed, and the naming half is a hard negative

**Mis-posed:** "which ids map to which player-visible commands" cannot be answered *of this table*,
because this table does not hold player commands. They are in the `<= 0x21E` space.

**Hard negative on naming:** the executable contains **no action, ability or command name table** —
searched in ASCII and UTF-16 for the obvious terms (Attack, Magick, Technick, Gambit, Mist,
Quickening, Steal, Libra, Cure, Fire, Blizzard, Esuna, Phoenix Down, Potion, Flee, Defend). **Every
hit is a UI layout parameter identifier** — `mGambitPositionOffsetX`, `GambitIconOffsetX`,
`BattleCommandMistPosX` — menu geometry keys that happen to contain the words. There is no id→string
table indexed by either space.

> **id → player-visible command name cannot be completed from `FFXII_TZA.exe`.**

**What would settle it, now narrower than before:** the authored records indexed by the **`<= 0x21E`**
space, from the game data outside the executable. **The `0x4000` space needs no external data** — it
is fully described by the 359-slot table plus the two nested switches, and section 10 is the complete
behavioural map for the 130 ids that carry one. **AT-5 closed as far as this binary allows.**

### AT-1 resolved as a by-product

The handler names `ExecuteDirectStateCommandOrder` and `AdvanceTargetedMovementOrder` were held as a
lead — possibly decompiler naming. **The id partition supports them**: the movement handler serves the
locomotion block, and the state handler owns the status-change runs. The names describe what the
bodies do. **AT-1.**

## 12. AT-5 revisited — the command list is recovered, the join is not (2026-09-02)

Section 11 closed AT-5 with a hard negative: the executable holds no action-name table, and naming
needs authored records. **Those records are now open**, and the result splits cleanly.

### Recovered: the player's battle command list

`word.bin` block 3 in the game archive, decoded from a custom character set
([format](../../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/vbf-archive-and-st2e-tables.md)
section 7):

```
Attack · Magicks · Technicks · Items · Summon · Quickening · Foecraft · Dismiss · Gambits · Mist
White / Black / Time / Green / Arcane Magicks
```

**And the retail data labels its own dead slots.** Ten entries read `NOT USED`:

```
concentration · trap · cancellation · all-cancel · escape · escape-cancel · order · crown · etc · monshands
```

**A cancelled "concentration" command, a trap command, an order command and a three-way
cancel/escape group** — commands that reached the shipped string table and never reached the menu.

### Still not recovered: id → name

**The 543-record `action_data.bin` does not reference the text by string id.** Every `u16` and `u32`
field at every byte alignment was scanned against nine string tables' id sets; **no field resolves.**

The description ids are `40000 + category*100 + slot` — a **category grid**, not the flat `0..0x21E`
space. So the two id systems are genuinely different, and the join between them is a third thing that
has not been found.

**AT-5's negative therefore stands in its exact original form**: ~~*id → player-visible command name~~
~~cannot be completed*~~ *(answered: each id is named through its row's `+0x34` into bank 0 of the battle text - AT-8 answered by reference 2026-09-14 and AT-9 answered 2026-09-11, section 6 above; Action-Availability AI-2; 2026-10-02, OPUS)* — not from the executable, and not yet from the archive either. What has changed
is that **the names themselves now exist in readable form**, and the missing piece is narrowed to a
single join. **AY-9.**

~~**AT-9 is blocked on the same join.**~~ *(answered: AT-9 ANSWERED 2026-09-11, `0x113` Dismiss and `0x95` Dismount, section 6; 2026-10-02, OPUS)* Command ids `0x113` and `0x95` are indices into the 543 space,
so naming them needs exactly the mapping that does not resolve.

## The `0x21E` boundary from the code side — three consumers, and the engine's own names — 2026-09-08

`AT-8` established the **543-id action space** from the data: ~~`action_data.bin`~~ the table in `battle_pack.bin`'s directory `+0x3C` *(corrected 2026-09-12, [the VBF page](../../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/vbf-archive-and-st2e-tables.md) §12; `action_data.bin` is a four-language copy)*, count `0x21F`, 60-byte
records, the file length confirming the executable's `cmp di, 0x21E`. **This section adds the code
side**, from three functions imported out of the research backlog and re-derived.

**The boundary is not a single bounds check.** At least three functions test it independently, and two
of them name what lies on either side.

### 1. `BattleUnit_AdvanceActionState` (`00307BE0`, 137 B) — the split has names

```c
int BattleUnit_AdvanceActionState(BattleUnit *u)
{
    if (u->p_708 == NULL) return -1;                  /* no action in progress */
    u->d_1F0 &= ~0x00000100;                          /* clear bit 8 */

    int r = (u->u16_714 > 0x21E)
          ? BattleUnit_AdvanceExtendedActionState(u)  /* 00305080,  249 B */
          : BattleUnit_AdvanceStandardActionState(u); /* 00304850, 2034 B */

    if (u->i_768 >= u->i_76C) u->i_75C++;
    if (r == 1) FUN_004697C0(u->p_698, u->u16_714, 0xFFFF, 0);
    return r;
}
```

> **The two halves of the action space have different advancers, and the ledger already names them
> `Standard` and `Extended`.** The size ratio is the striking part: **2,034 bytes for ids ≤ 542
> against 249 for the rest.** Whatever lives above the boundary needs an eighth of the machinery.

**`-1` means "no action in progress"** — the `+0x708` pointer is the gate, and it is distinct from a
failed advance.

### 2. `BattleAction_CheckTargetEligibility` (`003083B0`, 596 B) — above the boundary, nothing is targetable

```asm
003083F5  mov eax, 0x21E
003083FA  cmp si, ax
003083FD  ja  0x3083E7        ; -> xor eax,eax ; ret   (INELIGIBLE)
```

**An action id above 542 is rejected outright**, before the function looks at anything else. `AT-8`
called the `≤ 0x21E` space *"target-carrying"* on the strength of the data file; **this is the same
statement made by the code**, and the two derivations are independent.

### 3. The shared kind gate — and it points opposite ways

Both `BattleAction_CheckTargetEligibility` and
[`SpawnGroup_RecordMemberDeathAndHandleCompletion`](../../05-Spawn-Encounter-Lifecycle/Group-Completion-And-Respawn/when-a-group-is-wiped-and-when-it-comes-back.md)
open on the **same two-step gate** — a block pointer at `BattleUnit + 0x698`, then a byte at `+0x05`
compared against `1`:

| function | test | when `+0x05 == 1` |
|---|---|---|
| `BattleAction_CheckTargetEligibility` | `cmp byte [rax+5], 1` / `jne` continue | ~~**returns 0 — not targetable**~~ **returns 0 — no objection** (corrected 2026-09-11, below) |
| `SpawnGroup_RecordMemberDeathAndHandleCompletion` | `cmp byte [rax+5], 1` / `jne` return false | **proceeds to record the death** |

> ~~**Kind `1` is exactly the class that can complete a spawn group and cannot be targeted.**~~
> **Corrected 2026-09-11 (FABLE) — the polarity was inverted, and the gate tests the source, not the
> target.** `BattleAction_CheckTargetEligibility(source, candidate, actionId)` returns **0 for
> "eligible"** and non-zero for an objection: its only caller, `AiOrder_SelectFinalTargetFromCandidates`
> `003087E0`, appends the candidate to the output buffer exactly when the call returns 0
> (`00308848`–`00308860`, and the same at every other call site in it); the objection paths set `r14 = 1`
> only inside the flagged rule branches (`0030848A`, `003084C4`, `00308508`, `0030856C`, `00308588`)
> and return it (`003085E6`), while the rule-passing exits return 0 (`003083E7`, `003084E3`,
> `003085E2`). The kind test at `003083E1` reads `[rcx + 0x698]`, and `rcx` is the caller's `r15` — the
> **source** unit the selection is being made for (`003087F1`, `00308845`). So a source built from the
> enemy table (kind 1 by the [kind page's](../../04-Actor-Entity/Battle-Record-Kind/battle-record-kind-byte.md)
> corrected block: `0` = party table, `1` = enemy table) is exempt from the party-side rules that
> follow — the row-`+0x36` licence and category checks, the HP / MP thresholds behind row `+0x2C`
> bits 12 and 15, the committed-attacker mask tests — and every candidate passes. The two consumers
> therefore agree rather than oppose: **enemy-table units are the ones whose deaths complete a spawn
> group, and enemy-table sources are the ones the party's target rules do not bind.** `EI-1` answered;
> no dying-or-dead state is needed.

### 4. `BattleRuntime_ResetPersistentStatePrefix` (`00386C10`, 95 B) — two parallel tables

```c
void ResetPersistentStatePrefix(Ctx *c)
{
    void *base; unsigned idx;
    if (c && c->b_05 == 0) {                     /* the SAME +0x05 byte, tested against 0 */
        idx = c->b_04;  base = (void*)0x0208D480;
    } else {
        BattleUnit *u = BattleStats_FindOwningBattleUnit();   /* 0031B860 */
        *(void**)0x02EBF188 = u;                 /* cached */
        if (!u) return;
        idx = u->b_EA9; base = (void*)0x0208DE80;
    }
    u64 *p = (u64*)((char*)base + (idx << 6));   /* 64-byte stride */
    p[0] = p[1] = p[2] = p[3] = 0;               /* first 32 bytes cleared */
}
```

**Two parallel tables of 64-byte entries**, `0x0208D480` and `0x0208DE80`, chosen by whether a context
was supplied with `+0x05 == 0`. Only the **first 32 bytes** of an entry are cleared — the second half
survives a reset, which is the same shape of finding as the actor initialiser's masks and deserves
the same caution: **what survives is not established here.**

### What this section does not claim

- **Not what lies above id 542.** ~~`AT-8` remains open on the contents of the space;~~ *(answered: EI-2, 2026-09-12 - above 542 is the order space, section 2; 2026-10-02, OPUS)* this adds that the
  engine advances it with a different, much smaller routine and refuses to target it.
- ~~**Not the meaning of kind `1`.** `EI-1`.~~ Answered 2026-09-11 in §3: the enemy-table kind, and the gate's polarity was inverted.
- ~~**Not what `FUN_004697C0` does**~~ *(answered: it posts battle message `0x05`, `0x06` or `0x07` - Post-Result-Events/the-post-result-events-and-the-battle-message-table.md, the SWE2-EC7-21 update; 2026-10-02, OPUS)* with `(p_698, actionId, 0xFFFF, 0)` on a successful advance.
- **Not the rest of `CheckTargetEligibility`** — only its two opening gates were read; the 596-byte
  body past `003083FF` ~~is unread,~~ *(answered: its subtree is bound in the section on the `003083B0` exclusive subtree below; 2026-10-02, OPUS)* and the `02EBF138` action-table lookups it then performs are not
  followed.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. MECHANICAL-only crossings (the image-address resolver, the audio request chain) are recorded in the registry, not here.*

**Rewards_Progression_Economy — SERVICE and CLIENT.**

- `BattleLocomotion_DecodeOrderGoal` (`00312730`) asks `Loot_FindNearestActivePickupPosition`. By the callee's name, an
  order's goal can be the nearest active world pickup.
- `BattleStats_FindOwningBattleUnit` is also used by the level-up path and `Reward_ComputeExperienceForRecipient`.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**CombatFormula — CLIENT and SERVICE (SWE2-CONTRACT 2026-09-15, 38 edges).** The dispatch consults the formula
layer's effective-action-id resolvers directly: `00304850` ~~both calls and is called by~~ calls
`BattleRuntime_GetEffectiveActionId` `00387090` and `BattleRuntime_ResolveAndCacheEffectiveActionId`
`00387A50` — the handler table resolves the effective action id through them before dispatching. *(corrected
2026-10-02, FABLE: neither calls `00304850` directly; the getter's only calls are its two owner-resolver calls,
and the raw census gives `00304850` one direct caller elsewhere; FABLE review of ASTRA `ov42-effective-id-source`)*
The other ~34 edges are `0031B860` caller fan-in: the `BattleFormula_*`/`BattleStats_*` bodies
(`BattleFormula_ApplyTargetResult`, `BattleFormula_RollAvoidGuardParryOutcome`,
`BattleFormula_RollGuardParryMode`, `BattleStats_ModifyHPAndProcessLethalState`,
`BattleRuntime_MarkTargetHistoryBit`, `BattleFormula_EvaluateTargetPreview`,
`BattleStats_ModifySecondaryResource`, …) all call the same owner resolver the table cites. The
resolver pair is the real crossing; the `0031B860` share is mechanical.

**Resource — SERVICE (SWE2-CONTRACT 2026-09-15, 1 edge).** Handler `00427320` resolves its table row
through `ResourceTable_ResolveEntryByIndex` `002ED570`. The dispatch owns the handler; the row
lookup belongs to the resource layer.

**Script_VM_Native_Bridge — CLIENT (SWE2-EC7 2026-09-19, 3 edges).** `004686D0`, a callee this table's
`0033A120` section cites, is also called by three bridge-filed bodies (`00344390`, `003448F0`,
`00345630`). The bridge callers are mechanical verb users of a shared helper.

**InputGameplay — MECHANICAL (SWE2-EC7-96, 1 edge).** `00253B90` — the gate this table's `00309A90`
section cites — is reached through `00313A00` on the InputGameplay layer. Shared-helper fan-in; no
InputGameplay relationship to the dispatch.

**ActorEntity / CombatAI / Gameplay / Movement / Party / RNG_Random_Selection / Spawn_Encounter_Lifecycle — MECHANICAL (SWE2-EC7 batch-149).** The `00312DF0` entry names its caller `00312730` and the three shared leaves the picker draws on - `00320940` (default seed), `00317DE0` (accept test) and `00328370` (the random draw). Those leaves fan in from across combat: `00328370` is also called by ActorEntity `00236210`/`002394C0`, CombatAI `003014C0`/`00301830`/`003087E0`, Gameplay `00312B40`, Movement `00239210`, Party `003081E0`, the RNG layer's `00308EC0` and Spawn-side `00234AF0`/`002355A0`/`00236450`/`002395A0`/`002398F0`; `00320940` by Spawn `002350C0`, CombatAI `00301AD0`, Gameplay `00312B40` and Movement `003394A0`/`0033DB60`; and `00317DE0` calls Movement's `00337700`/`003377C0`. Shared-leaf fan-in around a placement picker - not dispatch ownership of those layers.

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page.*

**Items_Equipment_Shops_License — CLIENT (4 edges).** `BattleStats_SetEquipmentSlotByStatsIndex` `0031A410`, `BattleStats_SetEquipmentSlotByMappedId` `0031A510`, `BattleStats_SetEquipmentSlotDirect` `0031A630` and `BattleStats_SetLicenseNodeStateAndApplySideEffects` `00323910` call the owner resolver `BattleStats_FindOwningBattleUnit` `0031B860`. The equipment and licence setters find a stats record's battle unit through the same resolver section 4 cites; it is fan-in on the resolver, not a route into the handler table.

**Presentation — CLIENT, SERVICE and MECHANICAL (30 edges).** The four-float subtract helper `00203080` is called by 13 presentation bodies, among them `00274CB0`, `003C72F0`, `003F1A60`, `005621A0` and the two jump-table arms `00505570` and `00505E00`; `BattleUnit_ComputePartyBattleStance` `00308130` calls the gate `00253B90` and is called by `AiOrder_CheckActionPreconditions` `00301830`; `WorldActor_TestBoundsAgainstViewFrustumAtPosition` `003223C0` calls `ActorRuntime_GetClass3FloatPair` `00265090`; `BattleUnit_ComputePresentationSuppressionMask` `003125E0` calls the battle-mode query `BattleRuntime_GetMode0To5FromFlagsAndFieldBit15` `0030D9A0`; the commit `BattleUnit_CommitAction` `0030F760` calls `BattleUnit_BroadcastPartyCombatTargetRelation` `00313B30`; and on the `0x740`-stride animation object `00426130` calls `00426C90` and `00427320`, while `00427320` calls `CharacterRenderRecord_GetFCPPresentationConfigurationPayload` `003E55F0`, `003E7D10`, `00420890`, `00423230` and `0042F310` and is called by `00426130`, `00426520`, `00426560`, `00426C90` and `00521000`. Three different things cross here: a vector-subtract leaf every layer uses (mechanical), presentation-filed stance, frustum, suppression and relation bodies that share this page's action-side gates, and the animation-event dispatch that section 4 met only because `00426130` passes event ids `0x4035` / `0x4036`, which are not order ids.

**Status_Periodic_Terminal — SERVICE and CLIENT (11 edges).** The direct-state handler `BattleUnit_ExecuteDirectStateCommandOrder` `002FDDA0` calls `BattleStats_ModifyStatusLayerStateAndProcessSideEffects` `0030E130`, `BattleStats_ChangeStatusAndProcessSideEffects` `0030E360`, `BattleStats_RemoveAllMode0StatusesAndRecompute` `0030E8F0`, `BattleStats_ClearStatusLayer0AndProcessSideEffects` `0030E970` and `BattleStats_RecomputeDerivedStateAndAutoStatuses` `0030FED0`; `BattleUnit_AdvanceStandardActionState` `00304850` calls `0030E360`; and `BattleUnit_ResolvePeriodicPrimaryResourceRecoveryStep` `002F9400`, `0030E360`, `BattleStats_RemoveStatusesFromMaskAndRecompute` `0030F690`, `0030FED0` and `BattleFormula_BuildRuntimeCounterPeriodicHpCredit` `00386860` call `0031B860`. The direct-state family from `0x4046` changes statuses by calling the status layer's write, layer and recompute functions, the standard action state writes a status the same way, and the status bodies share the owner resolver.

**UI — MECHANICAL (10 edges).** `00203080` is called by 10 UI bodies, among them `0027BED0`, `002C7660`, `003F6BB0`, `003F9720` and `005512B0`. The UI uses the same four-float subtract leaf this page reaches through the solver body of the EC7-58 note; nothing in the UI reaches the handler table.

## The `003083B0` exclusive subtree — all 2 members bound (SWE2-FRONTIER, followup queue)

`003083B0` `BattleAction_CheckTargetEligibility` (~~307 B~~ 596 B *(corrected 2026-10-02, OPUS: `003083B0`–`00308603 ret`, int3 padding to `00308610`)*) — the
eligibility battery: three `[02EBF138]` context loads each feeding a
`0020E600` row lookup (`003083FF`/`00308413`, `0030841D`/`00308427`,
`0030842C`), the row fields then compared against the action/target
record.

| member | role | interior |
| --- | --- | --- |
| `00320AF0` (51 B) | row-field check — `(rcx, rdx)` null-gates, `003875D0` (`00320B06`), then `dword[rbx+0x64]` (`00320B0B`) and the `[02EBF0A8]` context (`00320B3C`) | [`00320B06`](../../_index/ADDRESS-INDEX.md) |
| `003875D0` (256 B) | table-row accessor — `[02EBF138]` + `dword[r9+0xC]` key → `0020E600` (`003875DA`/`003875EC`/`003875F0`), second row pass at `003875FA`/`00387601` | [`003875F0`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `0020E600`. The `02EBF138` cell is
the shared authored-table context; `02EBF0A8` is the sibling context
`00320AF0` also consults.

## The `002FE910` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`002FE910` ~~(~55 B)~~ (52 B *(corrected 2026-10-02, OPUS: `002FE910`–`002FE943 ret`, as the handler table in section 3 states)*) — `byte[+0x6B4] == 0` selects `qword[+0x708]`,
`word[rax+2]` (`002FE916`/`002FE929`).

| member | role | interior |
| --- | --- | --- |
| `0046A6E0` | `movzx cx + 0x5D` table index under an `r11 = rsp` frame (`0046A6E9`/`0046A6EC`) | [`0046A6E9`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none.

## SWE2-EC7-41 update (2026-09-19) - `002FDC30`

`002FDC30` (353 B) is `BattleUnit_AdvanceTargetedMovementOrder` - `00312B40` pair/`00265090`/`003291B0`/`0033A120`/`00325BB0`. Interior anchor `002FDC95` (a `00312B40` call).

## SWE2-EC7-57 update (2026-09-19) - `0033A120`

`0033A120` (188 B) is the `IsApproachConstraintActive` body the handler table names - `00335640`/`00336710`/`0033D3E0`/`004686D0`/`00808C40` plus `01F44830`. Interior anchor `0033A14C` (a `00336710` call).

## SWE2-EC7-58 update (2026-09-19) - `00335640`

`00335640` (273 B) is a solver-internal body the handler table names - `00203080`/`0033CB70`/`004687F0`/`00808C40` plus `008C5B2C`/`01CEBBA8`/`01CEBD80`/`01F44830`. Interior anchor `00335691` (a `0033CB70` call).



## SWE2-EC7-66 update (2026-09-19) - `003448F0`

`003448F0` (130 B) is a battle-action body - `00264010`/`00265060`/`00267DB0`/`00267E10`/`0026B4C0`/`004686D0` plus `01F44830`. Interior anchor `00344912` (a `00267DB0` call).


## SWE2-EC7-96 update (2026-09-20) - `00309A90` measured

`00309A90` (78 B) is the three-way float select `00301830`,
`00312730` and `00336040` call: `00253B90` returning zero yields
the `05E964F0` constant outright; otherwise `0030D9A0` picks
`068F6A78 + 05E964C0` (mode 1) or `05DA8F54 + 05E96A6C` - the
sum-of-two-constants shape the handler reads as a bound.
Interior anchor `00309A9D` (the `0030D9A0` call).

`00312DF0` (237 B) is the jittered-point picker `00312730` runs: it seeds a vec3 from `rcx` (or `00320940` default, fail `-> -1`), then up to 9 tries draw two `00328370()` values `idiv`-bounded to `+-r8d` jitter added to base x/z and ask `00317DE0(r14, out, r8d!=0)`; first accept returns 0, exhaustion `-2`

Interior anchor `00312E81` (function `00312DF0`).

## Interior citations for the entry-cited functions (FABLE, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's disassembly pack and re-read by FABLE against the certified image; verified by [`interior_applier.py`](../../_index/candidates/fable-battle-action-handler-table-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `00265060` | 38 B | returns qword `+0xB8` of `rcx` when `rcx` is non-null and the top three bits of byte `+3` (`>> 5`) equal 1 or 3; otherwise (null `rcx` or any other value) returns the address `02099DC0` | `00265063`, `00265069`, `00265071`, `00265076`, `0026507E` |
| `00344390` | 124 B | calls `00344390 + 0x1D` and then `00344390 + 0x27`, each with `r9` (results A and B), passes A to `00344390 + 0x30` and B to `00344390 + 0x3A`, passes those two results to `00344390 + 0x4D` and `00344390 + 0x42` respectively, calls `004686D0` with the mapped A in `rcx` and the mapped B in `rdx`, and tail-jumps to `00344390 + 0x77` with the incoming `rcx` and the returned `xmm0` in `xmm1` | `003443AD`, `003443C0`, `003443D2`, `003443E8`, `00344407` |
| `00426520` | 59 B | returns without work when `cx` is -1 or when dword `+0x284` of row `(movsx cx) * 0x740` plus qword `022C6F28` is 0 (the row pointer is then zeroed by `cmove`); otherwise ORs 0x40 into byte `+0x4B7` of that row and tail-jumps to `00427320(row, 0x1001)` | `00426524`, `0042653A`, `00426540`, `00426549`, `00426555` |
