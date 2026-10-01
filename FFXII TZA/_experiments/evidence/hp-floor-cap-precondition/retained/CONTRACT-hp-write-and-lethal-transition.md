---
contract: apply a change to a combatant's current HP and, when it reaches the floor, carry out the death transition
category: 08-Combat-Formula
scope: transition
level: L1
readiness: BEHAVIORALLY UNDERSTOOD
confidence: PROVEN
implements: 08-Combat-Formula/Current-HP/the-hp-write-and-the-lethal-transition.md
entries: ["00300530", "00300520"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-14 (OPUS) - 116 addresses cited - 3 data, 20 entry, 93 interior, every one resolving
    into a known section of the authority image. **This records a check performed on
    that date, NOT the method of the original derivation**, which this block never
    carried; see this document's own Evidence section and `audit.last_pass_state`
    for that.
last_reviewed: 2026-09-12
audit:
  passes: 1                    # falsification passes survived. 0 = NOT yet fact.
  last_pass: 2026-09-12        # YYYY-MM-DD
  last_pass_state: opus-hp-write-pass-1      # snapshot SHA the pass ran against
  crossref_clean: false        # audit_crossrefs.py reports nothing for this document
  reopened_count: 0
---

# Contract — the HP write and the lethal transition

`BattleStats_ModifyHPAndProcessLethalState` (`00300530`). **Every change to a combatant's current HP
in the game goes through this one function**, and so does every death. It is the single most
consequential state transition in combat, and almost all of its complexity is in what it does
*besides* the store — two eligibility gates, a clamp with two status modifiers, two publishers that
run before the write, and a six-step death sequence.

## 1. Purpose

Something has decided a combatant should gain or lose HP. This function decides whether that is
allowed, how far it is allowed to go, who gets told, and — if the result is death — everything death
entails, from the killer's identity to the encounter ledger.

## 2. Interface

| | |
|---|---|
| entry point | `00300530`, or `00300520` for the absolute-set thunk |
| calling convention | Microsoft x64, **four parameters, all in registers** |
| `rcx` | the target's stats record (`BattleStatsRecord`, the unit's `+0x698`) |
| `edx` | the delta, signed |
| `r8` | the source's stats record; **may be null** |
| `r9d` | the flag word (§3) |
| return | none used |

**Corrected 2026-09-12 (`OPUS-HPWRITE-ABI-AND-ISOLATED`): this is a four-parameter function.** The
contract previously read `[rsp+0xB8]` and `[rsp+0xC0]` as a fifth and sixth argument. They are the
function's own spills of `edx` and `r8`, written by its first two instructions —
`00300530 mov [rsp+0x18], r8` and `00300535 mov [rsp+0x10], edx`, the `r8` and `rdx` home slots —
and read back after a frame of `0xA8` (seven pushes plus `sub rsp, 0x70`). **A fifth and sixth
argument would be at `[rsp+0xD0]` and `[rsp+0xD8]`, and neither is ever touched.** All three callers
set only `rcx`/`edx`/`r8`/`r9d`, and the one at `0030F3DC` reserves only `0x20` of shadow space,
which has no room for a stack argument. So "arg5" below is **the delta** and "arg6" is **the source's
stats record**; both are named that way from here on.

**`00300520` is a two-instruction absolute-set thunk**: `sub edx, [rcx+0x48]` turns a target value
into a delta and falls through into `00300530`. It shares every behaviour in this contract.

Both records are mapped to their battle units immediately — `BattleStats_FindOwningBattleUnit`
(`0031B860`) at `00300553` for the source and `0030055E` for the target — and **either may be null**;
every side effect below re-checks.

## 3. The flag word

| bit | effect | site |
|---:|---|---|
| 0 | skip **both** eligibility gates | `003005A0`, `00300605`, `0030072F` |
| 1 | skip `00469BB0(sourceRecord, targetRecord)` on the lethal path | `00300588`, `0030079C` |
| 2 | no presentation event; the notify predicate is `unit && !bit2` | `003005D2` |
| 4 | suppress the reaction publisher | `0030058D`, `003006AC` |
| 5 | when `delta == 0`, supplies `isHeal` — **and `isHeal` reaches only the reaction publisher's third argument, never the outcome branch** (§9) | `003005AB`–`003005C0` |
| 6 | suppress the *alive* event even when notifying | `003005E5`, `0030086C` |
| 7 | suppress the number publisher | `003005F6`, `003006D8` |
| 8 | the death event is `0x200E` rather than `0x2007`/`0x2008` | `00300846` |

**`delta == 0` is a real case, not a no-op** — but **not a heal** (corrected 2026-09-12). Bit 5 makes
it one for the reaction publisher's third argument and for nothing else: the outcome branch tests the
delta itself, so a zero delta takes the damage path, cannot revive, and on a combatant already at the
floor runs the lethal sequence again (§9, §10).

## 4. Preconditions · postconditions · invariants

**Preconditions.** A stats record in `rcx`. Nothing else is required — a null source, a null target
unit and a zero delta are all ordinary.

**Postconditions.** At most one write of current HP, at `00300749`, of the clamped value. The
publishers and the event dispatch may have run; on the lethal path up to six further effects have.

**Invariants.** `floor <= hp <= cap` after any call that stores, with both bounds recomputed from
current state rather than cached. **The store is the only write of `+0x48` on this path.**

> **CORRECTED 2026-09-25 (OPUS, owner), on the S-23 stub-exposure analysis
> (`_index/candidates/s23-runtime-per-invariant-exposure.md`, block 300).** The two single-store claims above,
> "at most one write of current HP, at `00300749`" and "the store is the only write of `+0x48` on this path",
> hold for **`00300530`'s own instructions only**. After its store, `00300530` calls the status transition
> (`0030077A` / `003007CF`). On the paths where that transition runs the unit's stat recompute, **HP is stored
> again**, clamped to a cap recomputed from current status.
> - The call chain and the recompute's store site are in the candidate note.
> - EXP-148 executed that store.
> - EXP-093 stubbed the recompute and logged it as fired.

> The bound `floor <= hp <= cap` survives, because the second store also clamps. The single-store statement does not.
> A reconstruction must reproduce the re-clamp.

## 5. The two gates are not alike

1. **`BattleTarget_HasLow16EligibilitySuppression`** (`0030B9B0`) at `0030060F`: non-zero **returns
   before anything is touched**.
2. Then, for a **negative delta only** (`0030061C jns`), a target whose `(+0x64 | +0x3C) &
   0x80000003` is non-zero — statuses 0, 1 and 31, KO / Stone / Vanished — is refused unless
   `FieldData_GetActiveFieldRecordBit15()` says otherwise (`00300621`–`00300635`). **A downed
   combatant takes no further damage.**
   *The same mask with the same override guards the gambit condition evaluation*
   (`00301531 test eax, 0x80000003` then `00301538 call 00377C20`), so `0x80000003` + bit 15 is one
   rule applied at both ends: a downed combatant neither acts nor is further harmed.
3. **`BattleTarget_HasHigh16EligibilitySuppression`** (`0030B8E0`) at `00300740`: non-zero **skips
   only the store** (`00300747 jne 0030074D`) — the publishers have already run and the outcome
   branches still run. **It is only asked at all when bit 0 is clear AND the delta is not positive**
   (`0030072F cmp [rsp+0x50], edi / jne` then `00300735 test r12d, r12d / jg`, on the reloaded `r12`,
   which by then holds the delta). **A heal is never gate-3 suppressed.**

> Gate 3 is the one to get right. It does **not** abort the call: the reaction and the number are
> already published on a value that is then not written. A reimplementation that returns early here
> loses both publications; one that stores anyway corrupts HP.

## 6. The clamp

```c
old   = target->hp_48;                       /* 0030063B */
new   = delta + old;                         /* 0030063E */
floor = targetUnit ? targetUnit->+0x48 : 0;  /* 0030056D-00300579, kept at [rsp+0xB0] */
if (new < floor) new = floor;                /* 0030064C-00300651 */
else {
    st = target->+0x64 | target->+0x3C;      /* 00300656-0030065F */
    if (st & 0x10000)      cap = max(old,1); /* 00300665-00300673, cmovl against 1 */
    else { cap = target->maxHp_24;           /* 00300679 */
           if (st & (1<<28)) cap *= 2; }     /* 0030067C bt ecx, 0x1c */
    if (new > cap) new = cap;
}
```

**The floor is a battle-unit field, not zero.** A unit with a non-zero `+0x48` cannot be taken below
it by any delta, and a reimplementation that clamps to 0 will hold HP at the wrong value.
**Status bit 16 freezes HP at its current value, never below 1. Status bit 28 doubles the cap.**

> ### The clamp is numeric. It is not protection. (corrected 2026-09-13, `OPUS-HPFLOOR-NOT-INVULNERABILITY`)
>
> This paragraph used to gloss a non-zero floor as *"the shape of a scripted 'cannot be killed'"*.
> **That is false, and §12's own executed run already said so** — *"the floor is reached, not
> crossed; damage landing exactly on a non-zero floor is death"*. The two sentences sat four
> sections apart in one document.
>
> **The lethal test compares against the same floor the clamp uses.** At `00300784` the function
> reloads `[rsp+0xB0]` — the floor, the identical slot filled at `0030056D` — and at `0030078B`
> runs `cmp dword ptr [rsi+0x48], eax` / `jg`. Strictly greater survives. The clamp guarantees
> `hp >= floor`, so the only value the clamp can produce at the bottom is `hp == floor`, and
> `hp == floor` **falls through into the death sequence**. There is no floor-is-zero test anywhere
> on that path: `003007AD` onward runs `0030E360`, the killer-identity write, the kill counter, the
> time field, `00306F00` and the death event unconditionally.
>
> **So a non-zero floor does not remove the death threshold; it moves it up.** A unit with a floor
> of 1000 does not become unkillable — it runs the lethal sequence the moment HP reaches 1000,
> which is *earlier*, in HP terms, than a floor-0 unit. The engine's own verb name says this
> plainly: `btlAtelSetHpLowLimit` sets a **low limit**, not a shield.
>
> **Keep these two separate when reimplementing.** *Numeric clamping* — `new = max(new, floor)`,
> and the store — is §6. *Lethal consequence* — `storedHp <= floor` runs the death sequence — is
> §9. A reimplementation that clamps correctly and then tests `hp <= 0` for death will leave every
> non-zero-floor unit alive at its floor forever, which is the bug this gloss would have caused.
>
> What the floor is *for* in the shipped game — a scripted end to a fight at a chosen HP value
> rather than at zero — is a semantic reading and is **routed to FABLE**
> (`OPUS-REQ-FABLE-HPFLOOR-MEANING`), not asserted here.

## 7. Ordering, which is most of the contract

1. gate 1, then the status refusal — §5 steps 1 and 2 (`0030060F`–`00300635`)
2. compute and clamp (`0030063B`–`003006A4`)
3. **publish the reaction** `003283D0(targetUnit, delta, isHeal, 0)` unless bit 4 (`003006C5`) —
   the **requested delta**, not the clamped one, and the only place `isHeal` is used
4. **publish the number** `0028F1F0(targetUnit->+0x08, old, new, 0)` unless bit 7 (`003006E7`)
5. fetch the event-variant bit from the **source** (§8)
6. gate 3 — only for a non-positive delta with bit 0 clear — then **the store** (`00300749`)
7. the outcome branch, **decided by the sign of the delta** (§9)

**Both publishers run before the store and neither runs without a target unit** (`003006A7`), which
is why the spawn-time writers are silent. **The number publisher carries the clamped value** — `old`
and `new`, after the floor and the cap — **while the reaction carries the requested delta**, so the
two disagree on exactly the hits the clamp bites.

## 8. The event variant comes from the source's target buffer

```asm
00300704  lea   rcx, [rbp + 0x778]                 ; the SOURCE unit's target buffer
0030070B  call  00316D70                           ; BattleTargetBuffer_FindActorWorkIndex
00300710  cmp   eax, -1 / je                       ; not found -> variant 0
00300717  add   rax, rax
0030071A  mov   r13d, dword ptr [rbp + rax*8 + 0x788]   ; entries[idx].entryFlags
00300722  shr   r13d, 8 / and r13d, 1
```

`r13` selects the variant of **every** event this function dispatches: alive `0x2005`/`0x2006`, dead
`0x2007`/`0x2008`. It is `0` when either unit is missing. This is a consumer of
`CONTRACT-battle-target-buffer.md` — both of its `-1` return and of `entryFlags`, whose width this
site establishes.

## 9. The two outcomes

**The branch is on the sign of the delta, not on `isHeal`** (corrected 2026-09-12). `r12` carries
`isHeal` only as far as the reaction publisher; `003006B7`, `003006D0` and `003006EE` — one on every
path — reload it with the spilled delta, so `0030074D test r12d, r12d / jle` tests the delta.

**Heal**, a **strictly positive** delta (`0030074D`–`00300784`). If the old HP was above zero, done.
If it was zero, **revive**:
`BattleStats_ChangeStatusAndProcessSideEffects(target, sourceRecord, status 0, 0, 0, flags, mode 0)`
— clear KO. **Healing from zero is the only status side effect a heal has here.**

> ### The two thresholds are different fields (found 2026-09-13, `OPUS-HPFLOOR-NOT-INVULNERABILITY`)
>
> **Death is tested against the floor. Revive is tested against zero.**
>
> | | site | tested against |
> |---|---|---|
> | death | `0030078B cmp [rsi+0x48], eax`, `eax` reloaded from the floor slot `[rsp+0xB0]` | **the unit's `+0x48` floor** |
> | revive | `00300752 cmp [rsp+0x54], edi`, `edi` zeroed at `00300563` | **literal zero** |
>
> `[rsp+0x54]` is the **old** HP, captured at `003005EF` *before* the clamp — `mov eax, [rsi+0x48]`
> / `mov [rsp+0x54], eax`. The revive arm fires only when that value is at or below zero.
>
> **Consequence for a non-zero floor.** Such a unit runs the lethal sequence at `hp == floor`, and
> step 2 sets KO. A later heal through this function finds `oldHp == floor > 0`, takes `jg` at
> `00300756`, and returns **without clearing KO** — this function's revive arm can never fire for
> it. Whether anything *else* in the game clears that KO is not read here and is not claimed;
> the scope of this finding is `00300530` alone.
>
> A reimplementation that uses one threshold for both directions — floor for both, or zero for
> both — gets one of the two arms wrong for every non-zero-floor unit.

**Damage, or a zero delta** (`00300784`). If the stored HP is still above the floor (`0030078E jg`),
dispatch the **alive event** `0x2005 + r13` when notifying and bit 6 is clear. Otherwise the lethal
sequence:

| # | site | what |
|---|---|---|
| 1 | `0030079C` | `00469BB0(sourceRecord, targetRecord)` unless bit 1 |
| 2 | `003007AD` | `ChangeStatusAndProcessSideEffects(target, sourceRecord, 0, -1, -1, flags, mode 3)` — **set KO**, refused if already set |
| 3 | `003007DD` | `targetUnit->+0x30 = sourceUnit->+0x08` — **the killer's handle, kept on the unit** |
| 4 | `003007E8` | spawn-backed targets only (`record +5 == 1`): spawn record `+0x08++`, `+0x0C = seconds` |
| 5 | `0030082F` | `SpawnGroup_RecordMemberDeathAndHandleCompletion` — **a completion returns 1 and the function ends with no death event of its own** (`00300836`) |
| 6 | `00300838` | otherwise, when notifying: `0x200E` with bit 8, else **`0x2008` for variant 0 and `0x2007` for variant 1** |

> **The dead pair is INVERTED relative to the alive pair** (corrected 2026-09-12). The alive path is
> `0030087A lea edx, [r13 + 0x2005]` — variant 0 gives `0x2005`. The dead path is `00300854 neg r13d`
> / `sbb edx, edx` / `add edx, 0x2008`, which gives `0x2008` when `r13` is **zero** and `0x2007` when
> it is one. Reading the dead pair in the same order as the alive pair gets **both** death events
> wrong, and nothing in the shape of the code suggests it: the two sites are forty bytes apart and
> written in different idioms.

Steps 3–6 all require a target unit (`003007D4`). **A record with no unit is KO'd and nothing else
happens.**

> **Why step 5 is silent, and what else it does — verified 2026-09-11.** The completion branch does
> more than return 1. At `00306F9F` it calls `00238B70(1)`, which sets **bit 5 of the battle state
> word at `02089340` — "combat AI suspended"** — and at `00306FA9` it calls `00238AE0(1)`, setting
> **bit 7, the presentation veto**, in the adjacent instruction. Only then does it dispatch with
> `edx = 0x2005`. So a kill that wipes a group does not merely suppress *this* function's death
> event: it stops every gambit in the game from being evaluated (see
> [`../09-Combat-AI-And-Gambits/CONTRACT-gambit-walk.md`](../09-Combat-AI-And-Gambits/CONTRACT-gambit-walk.md)
> §5) and vetoes battle-line presentation, until `0035A6F0` clears them. A reimplementation that
> reproduces step 5 as "return without an event" reproduces a third of it.

> Step 5 is the subtle one: when a death completes a spawn group, **this function emits no death
> event at all** — the group completion path owns the presentation from there. A reimplementation
> that always emits one will double up exactly on the kill that ends an encounter.

## 10. Failure paths and edge conditions

1. Gate 1 returns before anything; gate 3 skips only the store (§5).
2. A downed target refuses *negative* deltas only — healing a KO'd combatant is allowed and is how
   revival happens.
3. **`delta == 0` is not a heal, with or without bit 5** (corrected 2026-09-12). Bit 5 makes it look
   like one to the reaction publisher and to nothing else: the outcome branch tests the delta, so a
   zero delta takes the damage path, **cannot revive**, and — because the status refusal guards only
   a *negative* delta — **runs the whole lethal sequence again on a combatant already at the floor**,
   killer handle, spawn counter and death event included. The KO status change is refused as already
   set; nothing else in the sequence is.
4. A null source gives variant `0`, no killer handle, and `r8d = 0` on the events.
5. A group completion suppresses the death event (§9 step 5).
6. The status refusal is overridable by the active field record's bit 15.

## 11. Observable behaviour

In memory: `record+0x48` before and after; the clamp is visible by driving a delta past the cap or
below the floor. On screen: the damage number and the hit reaction appear even when gate 3 suppresses
the store, which is the cheapest observable discriminator for §5. In the save: a spawn-backed kill
increments the spawn record's `+0x08`.

## 12. Reproduction formula

See §6 for the clamp and §7 for the ordering; both are written to be implemented directly. The one
thing not to reorder: **publish, then gate, then store.**

## 13. Runtime validation

**Evidence class: isolated original-code, over the whole transition — and since 2026-09-18 over the
CALLEES TOO, as shipped bytes rather than as oracles (§13a). Live capture: still absent.**
(2026-09-12; callee execution 2026-09-18)

**What ran:** `00300530` and its thunk `00300520`, as shipped bytes under Unicorn at their real
virtual addresses, with all **twelve callees supplied as scripted oracles at their own real
addresses** — `0031B860`, `0030B9B0`, `00377C20`, `003283D0`, `0028F1F0`, `00316D70`, `0030B8E0`,
`0030E360`, `00469BB0`, `0032A150`, `00306F00`, `003299B0`. None of them is this contract's subject
and what this function *does* is call them in an order, so the comparison is of **the trace of calls
with their arguments** as well as of the memory written. **What did not run:** anything inside those
twelve, and no caller.

**Instrument:** [`diff_hp_write.py`](../../../Reconstruction/Tests/Differential/diff_hp_write.py)
against [`hp_write.c`](../../../Reconstruction/Game/Combat/hp_write.c).

**Result: 1588 commands, 846 compared lines, 0 mismatches** — 755 traced calls, 32 death events and
27 alive events, all five event ids observed.

### 13a. The twelve callees, executed — 2026-09-18 (OPUS, consuming SWE2-ORACLE's EXP-093)

**What changed:** §13's central limitation — *"all twelve callees supplied as scripted oracles"* — is
retired. EXP-093 ran `00300530` with all twelve real, **64 bodies, 64/64 cases and 12/12 mutants
killed across two processes**. **What did not change: the evidence class.** The experiment discloses
itself as **NATIVE-REPLAY on hand-built fixtures, not live-game proof**, and this contract carries it
at that class. Live capture is still absent.

**Every finding below was re-read from the shipping bytes before it was written here.** Three of the
ten did not survive that reading unchanged, and one of them is a correction to the experiment rather
than to this contract.

#### Refused: the field/status gate is `delta < 0`, not `delta <= 0`

EXP-093 finding 2 states the refusal *"applies for `delta <= 0`, not only negative deltas"*. **The
instruction says otherwise.** `0030061C test r14d, r14d` / `0030061F jns 0x30063b` jumps **over** the
whole gate when the delta is not negative, and `r14d` is the delta, loaded at `00300550 mov r14d, edx`
and untouched until `0030063B`. A delta of zero skips the `(+0x64 | +0x3C) & 0x80000003` test and the
`00377C20` override entirely. **§5.2 already says "for a negative delta only (`0030061C jns`)" and is
correct**; it is not being changed. Routed back to the experiment's author rather than absorbed,
because the record should not keep a finding the bytes refuse.

#### Already held here, and more precisely than the findings state them

- **Finding 7, the floor.** §6 already reads `floor = targetUnit ? targetUnit->+0x48 : 0` from
  `0030056D`–`00300579`, kept at `[rsp+0xB0]`. Worth keeping visible because it is the trap in this
  body: **`[rsi+0x48]` and `[rbx+0x48]` are the same displacement on two different objects** — the
  record's current HP and the owning battle unit's floor — and `0030063B add r14d, [rsi+0x48]` uses
  the first while `0030064C cmp r14d, [rsp+0xB0]` uses the second.
- **Finding 1, the alive event.** The id is not flatly `0x2005`: §8 establishes that `r13` selects the
  variant of every event this function dispatches, re-derived at `0030071A` from the **source unit's
  target-buffer** `entryFlags >> 8 & 1`, so the tail at `0030087A lea edx, [r13 + 0x2005]` posts
  `0x2005` **or `0x2006`**. Read the finding as "the alive variant", not as a constant.

#### Accepted, and what each one buys a reimplementation

- **Ordinary non-lethal damage emits the alive event** — the tail runs on every non-lethal
  non-positive write, not only on kills; positive heals emit nothing.
- **Gate-3 refusal suppresses the store and the lethal block and still posts the alive event.**
  `00300747 jne 0x30074d` jumps over exactly one instruction, the store `00300749 mov [rsi+0x48],
  r14d`, and lands on the outcome selection at `0030074D`. §5.3's warning — *"a reimplementation that
  returns early here loses both publications"* — now has the event as a third thing it would lose.
- **Monster-band targets (`atype 0x1B`–`0x27`) take a single `ST(rec, src, status=0, mode=-1)` and
  skip the KO cascade** — no KO bit write, no defeat-cleanup chain.
- **GD completion emits its own alive event**, and the main body's death event is suppressed on that
  path while GD's is not.
- **Delta zero on a dead target re-enters the full lethal cascade, and the bytes say why.** Flag
  bit 5 supplies the heal argument **only when the delta is zero**: `003005AB test r14d, r14d` /
  `je 0x3005b9` sends the zero case to `r12d = (flags >> 5) & 1` while a non-zero delta takes
  `r12d = setg` at `003005B3`. Bit 5 then cannot divert control flow, because **`r12d` is reloaded
  from the delta spill `[rsp+0xB8]` on BOTH arms** — at `003006B7` and again at `003006D0` — before
  the gate-3 and lethal tests. The experiment names one of the two reloads; the second is what makes
  the conclusion unconditional.
- **The reaction-queue insert is real**: `QUEUE+0` is the work pointer and `QUEUE+0xC` the
  `0x80808080` sentinel written by `002DD7E0`'s fill — **not** the damage magnitude.
- **`003F8980` callback ABI**: `(rcx = view, edx = 1, r8 = &{oldHP, newHP})`; the no-callback arm
  clears view bit `+0x26`.
- **Killer id copies source-unit `+8` → target-unit `+0x30`**; spawn-backed targets increment the
  spawn counter and write the tick-derived respawn time, and the kill ring dedupes on
  `{kind, tick-window}`.

#### One reading note on the mutation table, so nobody disassembles at those addresses

The campaign records the cap-double mask patched *"at both test sites (`0x30067F`, `0x3006A1`)"*.
**Neither is an instruction boundary.** The instructions are `bt ecx, 0x1c` at **`0030067C`** and
**`0030069E`**, four bytes each, and the two quoted addresses are their **immediate bytes** — which
is the right thing for a byte-patching harness to name and the wrong thing to read as a call site.
The finding stands: patching only one of the two left the mutant alive, which is why both exist.

### The positive control

A green differential proves nothing until the suite is shown to fail, so the **two corrections below
were each re-applied to the reconstruction as the contract originally had them**, rebuilt from a
deleted executable, and re-run:

| control | what it restored | result |
|---|---|---|
| the dead pair read in the alive pair's order (`0x2007 + variant`) | §9 step 6 as written before | **FAIL** — every death event inverted |
| the outcome branch on `isHeal` instead of the delta | §9 as written before | **FAIL**, first at a zero-delta case: the original writes the killer handle and the reconstruction healed instead |

The suite was then **restructured** — the twelve callees were given their true arities instead of one
uniform seven-argument hook — and the second control was **re-run against the restructured suite**
and failed again. The first was not re-run after the restructure; its result stands for the suite as
it was when it ran, and the claim it guards is carried by the campaign below, which kills every
mutant of the dead-event pair.

### The mutation campaign, and what it took to make it readable

**102 mutants: 89 KILLED, 4 SURVIVED, 9 EQUIVALENT, 0 INVALID, 0 NO_BUILD**, with
`production_inputs_stable: true` and all four input hashes re-checked against the files as published.

Getting there took two instrument corrections, and both were the same fault — **a catch the
instrument could not read**:

1. **The uniform hook.** The reconstruction first routed all twelve callees through one
   seven-argument hook and padded the unused tail with zeros. Twenty-seven mutants survived, every
   one of them a padding zero that nobody passes on and nobody compares. The twelve callees were
   given **their own arities**, read off the call sites, so every literal left at a call site is one
   the original really sets. Survivors fell from 38 to 4.
2. **The unreadable failure.** `mutation_test` recognises a killed mutant from the harness's stdout,
   in one of five shapes. This harness raised as soon as the two sides differed in **length**,
   printing none of them — so **36 of 102 mutants were scored INVALID when the suite had caught
   them**. A length difference is now reported as mismatches: killed rose from **53 to 87**. The last
   two unreadable cases were mutated pointer offsets that killed the driver outright, which was
   raised rather than reported for the same reason; reporting a dead driver as mismatches took the
   campaign to **89 killed and nothing unreadable**.

The same blindness is in nine other harnesses, filed as `OPUS-CONTRA-HARNESS-LINECOUNT-INVALID`:
**their published KILLED counts are floors.**

**The 4 survivors are equivalences, by reasoning rather than by byte-identity.**
`(old < 1) ? 1 : old` and `(old < 2) ? 1 : old` differ only at `old == 1`, where both
give 1; the two `? 1 : 0` predicates are read only for truth, so a `2` changes nothing;
and `30.0f` mutated to `30.1f` truncates to the same divisor at every scale the suite
drives. The mutants that would have mattered — `30.0f` to `31.0f`, the `: 1` of the
freeze cap, every offset and every event id — are killed.

Nothing came back unreadable.

### The signature, decided by execution as well as by reading

The suite calls the original with **four arguments and nothing else**, over a stack deliberately
planted with `0xCD` above the shadow space. Had a fifth or sixth argument been real, the status
change and the kill hook would have received that pattern and the two sides would have parted
company on the first kill. They do not: **`[rsp+0xB8]` and `[rsp+0xC0]` are the delta and the source
record, spilled by the function itself** (§2).

### What the run settled that reading alone had not

- **A zero delta is damage.** Driven with and without bit 5, above the floor and on it: the lethal
  sequence runs on a combatant already at the floor, and no revive happens.
- **Gate 3 is not asked for a heal.** Driven with gate 3 refusing, at a positive and a negative
  delta: the call appears in one trace and not the other.
- **The floor is reached, not crossed.** Damage landing *exactly* on a non-zero floor is death;
  one point above it is not.
- **The freeze bit's cap is `max(old, 1)`**, driven at old 0 (cap 1) and old 150.
- **The seconds field is `frames / (int)(scale × 30)`**, driven at three scales, where `scale` is the
  `.data` float at `01DFE0B8` that ships as `1.0f`.

### What is still owed, and it is live-only

~~Every callee here is scripted.~~ **Superseded 2026-09-18 by EXP-093 (§13a): the twelve are no longer
scripted — sixty-four bodies ran as shipped bytes.** What is still owed is narrower and still
live-only: the run is **NATIVE-REPLAY on hand-built fixtures**, so the object layouts are fixture
layouts consistent with the bodies' own offset arithmetic rather than layouts observed in a running
game, and nothing shows the `+0x48` floor being written by anything (§14).

**Experiment records that name this contract** — found by `OPUS-CONTRACT-RUNTIME-AUDIT`, 2026-09-13. Each names this
contract in its own `contract:` frontmatter while this section did not cite it back.

- [`EXP-060`](../_experiments/EXP-060-result-numeric-dispatch.md) — **method B**, isolated original-code execution.

**None of these is a live run**, so none of them changes the evidence-class statement at the
top of this section. They are listed because a reader auditing what has been executed against
this contract should not have to find them from the experiment side only.

## 14. Unresolved

1. ~~**Who writes the unit's `+0x48` floor**~~ — **answered, and it was already in the type store
   when this contract asked** (retired 2026-09-12). There are **two** writers and the difference
   between them is the mechanic: `BattleUnit_ApplyUnitDefinition` **zeroes** it on every apply
   (`0023ABDB`), so no authored unit definition can set it, and `00239820` sets it from a supplied
   value (`00239832`) reached **only from the script VM** — its one caller `005105E0` has no callers
   in the graph and is referenced by a single qword at `01F28DF0`, a slot in a VM native handler
   family table. **A non-zero floor is script-set and script-set only, and is lost if the definition
   is re-applied.** *(Corrected 2026-09-13: this used to read "that is exactly the 'cannot be
   killed' shape §6 reads off the clamp". §6 no longer says that and neither does this item — a
   script-set floor moves the death threshold up, it does not remove it.)* Nothing *observed here* sets it, which is what this item originally said and is a
   statement about this function rather than about the field.
2. ~~**What status bit 28 is called.** Its effect is exact — it doubles the cap — and its name is not
   cited (`EY-1`). Still open.~~ **Answered 2026-09-11 (FABLE, `EY-1`; corrected here 2026-09-20): the
   bit is Bubble** — `status_data.bin` row 28's name reference resolves to bank 5 `Bubble`, and
   `listhelp_status.bin` string 120,028 reads *brims with life, doubling max HP*, corroborating the
   doubled cap this function implements.
3. ~~**Who writes `entryFlags` bit 8**~~ — **answered on the page this contract formalises**
   (`EY-4`, 2026-09-11; retired here 2026-09-12): `Battle_ProcessActionTarget` copies the action
   result's flag word B bit 3 into it at `003075CB`, and that bit is
   `BattleFormula_RollKnockback`'s outcome. So **the variant this function selects is "knockback
   rolled"**, and `0x2006`/`0x2007` are the knockback variants of the alive and dead events — which
   also explains the inversion §9 records, since the *knockback* death is the lower id.

## 15. Evidence

**Claim table corrected and executed 2026-09-12 (`OPUS-HPWRITE-ABI-AND-ISOLATED`).** The first row
said the opposite of what it now says and was marked PROVEN; the two rows after it are new claims
that execution produced. "Executed" below means the shipped bytes ran against the reconstruction
(§13).

| claim | evidence | tier | confidence |
|---|---|---|---|
| four parameters, all in registers | `00300530`/`00300535` spill `r8` and `edx` into their own home slots before the seven pushes, and the `0xA8` frame puts those slots at `[rsp+0xC0]`/`[rsp+0xB8]`; a fifth and sixth would be at `0xD0`/`0xD8` and are never read. All three callers set four registers, and `0030F3DC` reserves only `0x20` of shadow space. Executed over a stack planted above the shadow space | 1 (isolated original-code) | PROVEN |
| the outcome branch is on the sign of the delta, not on isHeal | `r12` is reloaded from the spilled delta at `003006B7`, `003006D0` and `003006EE`, one on every path, before `0030074D test r12d, r12d`. Executed, and the control that restored the old reading FAILED on the zero-delta case | 1 (isolated original-code) | PROVEN |
| the dead event pair is inverted relative to the alive pair | `00300854 neg r13d` / `sbb edx, edx` / `add edx, 0x2008` against `0030087A lea edx, [r13 + 0x2005]`. Executed at both variants on both paths; the control that read the dead pair in the alive order FAILED | 1 (isolated original-code) | PROVEN |
| both records are mapped to units and may be null | `00300553`, `0030055E`, with re-checks at `003006A7`, `003007D4`. Executed with each of the two units present and absent | 1 (isolated original-code) | PROVEN |
| gate 3 skips only the store, and is asked only for a non-positive delta with bit 0 clear | `00300740 call 0030B8E0` / `00300745 test eax, eax` / `00300747 jne 0030074D`, landing after `00300749`, reached only past `0030072F` and `00300735`. Executed refusing, at both signs of delta and with bit 0 set: the publishers appear in the trace and the store does not happen | 1 (isolated original-code) | PROVEN |
| the store is the only HP write | `00300749 mov dword ptr [rsi + 0x48], r14d`. Executed: the record's HP is compared after every command in the suite | 1 (isolated original-code) | PROVEN |
| the floor is a unit field | `0030063B`/`00300641`/`0030064C` against `[rsp+0xB0]`, filled at `0030056D`–`00300579`. Executed at a non-zero floor, a negative floor, and with no unit at all (floor 0) | 1 (isolated original-code) | PROVEN |
| damage landing exactly on the floor is death | `0030078B cmp [rsi+0x48], eax` / `0030078E jg` — strictly greater survives. Executed at the floor and one point above it | 1 (isolated original-code) | PROVEN |
| status bit 16 freezes at max(old,1) | `00300665 and r8d, 0x10000` / `0030066E cmp edx, 1` / `00300673 cmovl`. Executed at old 0 and old 150 | 1 (isolated original-code) | PROVEN |
| status bit 28 doubles the cap | `00300679 mov eax, dword ptr [rsi + 0x24]` / `0030067C bt ecx, 0x1c`. Executed set and clear, from both status words | 1 (isolated original-code) | PROVEN |
| the variant bit comes from the source's buffer | `00300704`–`00300726`, a dword read at `+0x788 + 16 × index`. Executed with the search failing and at three indices, with the bit set and clear | 1 (isolated original-code) | PROVEN |
| a group completion suppresses the death event | `0030082F` then `00300836`. Executed: the trace ends at the completion with no event | 1 (isolated original-code) | PROVEN |
| the spawn counter and the seconds field are written only for a spawn-backed target | `003007E8`–`00300829`, and the kind byte is read through the **unit's** own record pointer, not the record the call was given. Executed with the kind byte set and clear, with the pointer NULL, and with it pointing at a different record | 1 (isolated original-code) | PROVEN |
| the seconds field is frames divided by (int)(scale × 30) | `0030080A`–`00300820`, an unsigned divide by the truncation of the `.data` float at `01DFE0B8` times `30.0f`. Executed at three scales | 1 (isolated original-code) | PROVEN |
| **the predicate is the engine's UNIVERSAL downed-combatant test, not a rule with two ends** | **measured 2026-09-12 (§15a)**: `0x80000003` appears at **173 instructions image-wide**, about 150 of them in battle, AI, menu, enmity, reward, perception and party code. Changing what the mask means changes all of them | 1 | PROVEN |
| **the override is `00377C20 FieldData_GetActiveFieldRecordBit15`** | **re-read 2026-09-12**: both guards call it and bail when it returns zero, so **the active field record's bit 15 decides** whether a downed combatant is still actionable and still harmable | 1 | PROVEN |
| **that override returns `0` — deny — whenever the field record table is absent or the index is out of range** | [the field record accessors](../03-World-Area-Field/CONTRACT-field-record-accessors.md) §10: the failure path is `0xFFF >> 15`, which is `0`, **indistinguishable from a field whose bit 15 is genuinely clear**. `00377C20` is reached by **110 distinct functions across 16 subsystems** — 65 directly, 47 through the thunk `00313F60` | 1 | PROVEN |
| the same 0x80000003 mask with the same bit-15 override guards the gambit condition evaluation | `00301531 test eax, 0x80000003` then `00301538 call 00377C20` — one rule applied at both ends, so a downed combatant neither acts nor is further harmed. **In a different function**, which this contract's pilot does not execute | 1 (static) | PROVEN |
| nothing observed live | — see §13 | none | UNKNOWN |

## 15a. Falsification pass 1 — 2026-09-12 (OPUS), SURVIVED

### The cross-subsystem claim is exact, and bigger than it says

§15 claims *"the same `0x80000003` mask with the same bit-15 override guards the gambit condition
evaluation"* — **a cross-subsystem claim, which is where contradictions hide.** Read at both ends:

```asm
00300621  mov  eax, dword ptr [rsi + 0x64]      ; the HP write
00300624  or   eax, dword ptr [rsi + 0x3c]
00300627  test eax, 0x80000003
0030062C  je   …
0030062E  call 0x377c20
00300633  test eax, eax
00300635  je   …                                 ; bail

0030152B  mov  eax, dword ptr [rcx + 0x64]      ; the gambit evaluation
0030152E  or   eax, dword ptr [rcx + 0x3c]
00301531  test eax, 0x80000003
00301536  je   …
00301538  call 0x377c20
0030153D  test eax, eax
0030153F  je   …                                 ; bail
```

**The same five instructions, the same two status words `+0x64 | +0x3C`, the same mask, the same
callee, the same branch shape.** The claim understates itself: it is not "the same mask", it is the
same composed predicate. And the override has a name — `00377C20`
**`FieldData_GetActiveFieldRecordBit15`** — so *the active field record's bit 15* is what decides
whether a downed combatant is still actionable and still harmable.

**What the pass adds: it is not a two-ended rule.** `0x80000003` appears at **173 instructions
image-wide**, and roughly 150 of them sit in battle, AI, menu, enmity, reward, perception and party
code — `BattleMenu_BuildCommandEntryList`, `BattleEnmity_WriteForCombatantId`,
`Reward_ComputeExperienceForRecipient`, `BattleUnit_RunPeriodicCombatMaintenance` among them.
**It is the engine's universal downed-combatant predicate.** For anyone changing what "downed" means,
that is the number that matters: not two sites, about a hundred and fifty.

### The rest, verified at the exact cited instructions

| claim | what the bytes say |
|---|---|
| gate 3 skips only the store | `00300740 call 0x30B8E0` / `00300745 test eax, eax` / `00300747 jne 0x30074D` — **the jump lands past the store and nowhere else** |
| the store is the only HP write | `00300749 mov dword ptr [rsi + 0x48], r14d`, and it is the only write to `+0x48` in the body |
| damage landing exactly on the floor is death | `0030078B cmp dword ptr [rsi + 0x48], eax` / `0030078E jg 0x300861` — **`jg`, so equal falls through to the death path** |

**Mechanical:** every stated body size matches the current census — **no drift**; a banned-evidence
sweep for `.pdata`, `.xdata`, unwind, EH-map and IP-to-state found **nothing**; all cited entries
resolve, and the 79 further cited addresses are instruction sites inside them, as they should be.

> **What this pass did not do.** It read instructions. §15's executed claims were executed by this
> contract's own pilot and are not re-run here, and **claim 14 remains static by the contract's own
> words — "in a different function, which this contract's pilot does not execute."** The 173-site
> census is a static measurement too.

## 16. Parity plan

`STATE-TRANSITION` — damage to exactly the floor, and one point above it, asserting alive versus dead.
`CALCULATION` — the clamp with status bits 16 and 28 set and clear.
`EDGE-CASE` — `delta == 0` with bit 5 on a combatant at zero HP must **not** revive: it takes the
damage path and runs the lethal sequence (corrected 2026-09-12; this line asked for the opposite).
Gate 3 must publish without storing, and must not be asked at all for a heal.
`INTEGRATION` — a kill that completes a spawn group must emit no death event from this function.

## 17. Related

- `08-Combat-Formula/Current-HP/the-hp-write-and-the-lethal-transition.md` — the page this formalises.
- `07-Combat-Action/CONTRACT-battle-target-buffer.md` — §8 is a consumer of it.
- `05-Spawn-Encounter-Lifecycle/CONTRACT-group-completion-and-respawn.md` — what step 5 hands off to.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. The image-address resolver fan-out is MECHANICAL and recorded in the registry.*

- **Items_Equipment_Shops_License — CLIENT.** The owner lookup `BattleStats_FindOwningBattleUnit` is driven by the three
  equipment-slot setters and the licence-node setter. The action-permission bit is read by
  `Equipment_UnequipEncodedItemFromActiveRoster` and `Inventory_QueryOwnedCountIncludingReservedActionItems`.
- **Movement — CLIENT.**
  - The permission thunk `00313F60` is read by four movement bodies of 114–1,005 bytes, and the bit by five more.
  - Two locomotion bodies use the owner lookup.
  - The presentation dispatcher is also called by the 68-byte stance-bit setter.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**CoreRuntimeScheduling — SERVICE.** `00300530` on this page calls `GameClock_GetRawTickCounter`, owned by that layer. What it reaches is **seven bytes** returning the counter at `[0208D45C]`, with no scaling of any kind; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Gameplay — CLIENT.** `BattleUnit_UpdateEngagementStateFlag`, owned by that layer, calls `00377C20` on this page. That caller is the engagement test, which reads the unit record's `+0x698` block and tests `+0x3C` OR `+0x64` against its own mask; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Rewards_Progression_Economy — CLIENT.** `BattleUnit_ProcessDefeatRewardsAndLoot`, owned by that layer, calls `00377C20` on this page. That caller is defeat-and-loot processing, which reads the defeated unit's `+0x698` block, needs `byte[+5] == 1`, and is suppressed entirely by bit 3 of `byte[+0xE9A]`; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**ActorEntity — SERVICE on thirteen edges, CLIENT on six (19 edges, four neighbour bodies read).**
Thirteen of the nineteen are fan-in on two functions cited here. Nine ActorEntity bodies reach
`00313F60` — `BattleGroup_RefreshFourActorDefinitions`, `BattleUnit_UpdateLifecycleAndCombatFrame`,
`BattleUnit_ApplyUnitDefinition`, `BattleUnit_ActivateAppliedDefinitionRuntime`,
`ActorSystem_ReleaseBattleUnitSlotForActor` and four unnamed — and two more reach `00377C20`
`FieldData_GetActiveFieldRecordBit15`, which bounds the field index against `dword[02ADD100+4]` and
**answers 0 for an unknown field rather than failing**. Two further edges are
`BattleUnit_DispatchActorPresentationEvent` reached by `BattleUnit_ActivateAppliedDefinitionRuntime`,
and `0035A6F0` by `002628B0`.

The six in the other direction are ordinary lookups, and three of them state their own refusals.
`00239820` calls `ActorWork_GetBattleUnit` `0031B760`, which returns 0 for a null argument and
otherwise tail-jumps to `00263E30`. `BattleStats_FindOwningBattleUnit` `0031B860` calls both
`BattleUnit_GetSlotCount` `00236850` — two instructions, `mov eax, [0208E6A0] / ret` — and
`BattleUnit_GetBySlotIndex` `00236820`, which bounds the slot against **that same global** and
strides `0xF50` per record. `003283D0` calls `ActorRuntime_GetClassNibble` `00263C20`, which returns
0 for null and otherwise the **low nibble of `byte[+0xE]`**. The remaining two are `0030E360` to
`00300FC0` and `005105E0` to `00239820`.

The crossing is a bounded pool consulted in one direction and two shared readers consulted in the
other. Read from the shipping bytes 2026-09-14 (OPUS).

## The `0028F1F0` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`0028F1F0` (~62 B) — HP-write body under a four-register save.

| member | role | interior |
| --- | --- | --- |
| `003F8980` | `qword[+0x38]` non-null gate (`003F8986`/`003F8990`) | [`003F8986`](../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none.
