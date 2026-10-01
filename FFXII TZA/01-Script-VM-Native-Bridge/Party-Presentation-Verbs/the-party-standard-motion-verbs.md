---
system: The party standard-motion verbs — one motion, four slots, and a 2x2 of variants
category: 01-Script-VM-Native-Bridge
status: DOCUMENTED — every register row is closed (owner re-status 2026-09-30, OPUS) — the push/pop pairing and where the -1.0f goes answered 2026-09-30 (it is the standard-motion blend; in the plain verbs a negative blend takes the 004272E0 arm, in the without-same verbs it is not consulted); the two arms answered (RC-19: a negative blend is a hard cut, a positive one a cross-fade) and the Movement float pushers answered (RC-20: seven movement verbs' begin callbacks) (SWE2-CONTRACT); 00233F50 and 002ED020 read 2026-09-18 (the per-actor prologue: reset action control, despawn a terminal-status actor the field does not keep, notify the render record)
owner_layer: Script_VM_Native_Bridge — from the ledger, not inferred from callers
evidence_tier: 1
level: L1
readiness: BEHAVIORALLY UNDERSTOOD
confidence: PROVEN
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-14 (OPUS) - 50 addresses cited - 3 data, 31 entry, 16 interior, every one resolving
    into a known section of the authority image. **This records a check performed on
    that date, NOT the method of the original derivation**, which this block never
    carried; see this document's own Evidence section and `audit.last_pass_state`
    for that.
last_reviewed: 2026-09-30
falsification_passes: 1
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-party-std-motion-pass-1 - EVERY figure reproduces and there is no correction: the four body sizes, all four discriminating instructions at their published addresses, the identical call multisets apart from the leading discard, the loop bound, the call order, 0035AE10's two-step shape, 003580C0's two Int32Coerce pops and one discard and its seven other callees, and all nine stated body sizes; added - each body has exactly three edx writes of which only the third differs, and 00263750's bound 0..3 and base 0209A1F0 both resolve from its 23 bytes
  crossref_clean: false
  reopened_count: 0
---

# The party standard-motion verbs — one motion, four slots, and a 2×2 of variants

## 1. What the player sees

In a cutscene the whole party reacts at once. Everybody nods, everybody looks up, everybody drops
into the same stance — not the leader alone, and not one character at a time. A scene author asks for
**one motion** and the party performs it together.

There is a second thing the player sees, or rather does not: **the motion does not restart when it is
already running.** If a scene asks for the same stance twice — because two script lines overlap, or
because a loop re-issues it — the characters do not visibly hitch back to the first frame. That is
not a smoothing feature in the animation system. **It is a different script command**, and the
script author chose it.

## 2. Four verbs, and they are a 2×2

| Call id | Verb | Handler | Body |
|---|---|---|---:|
| `053E` | `partystdmotionplay` | `0034F060` | 154 B |
| `053F` | `partystdmotionplaywithoutsame` | `0034F890` | 151 B |
| `0540` | `partystdmotionplay_540` | `00350050` | 157 B |
| `0541` | `partystdmotionplaywithoutsame_541` | `003507B0` | 154 B |

All four have **the same call set**. They differ in exactly two independent binary choices, both
readable as single instructions:

| verb | pops an extra argument first | third pushed value |
|---|---|---:|
| `053E` `partystdmotionplay` | no | **1** |
| `053F` `…withoutsame` | no | **0** |
| `0540` `…_540` | **yes** (`VMValueStack_PopNumericDiscard`) | **1** |
| `0541` `…withoutsame_541` | **yes** | **0** |

- **The "withoutsame" bit is `mov edx, 1` versus `xor edx, edx`** immediately before the third
  `VMValueStack_PushInt32` — `0034F0C1` and `003500B4` set 1; `0034F8F1` and `00350814` zero it.
  The verb names corroborate the constants, but the constants are the evidence.
- ~~**The `_540`/`_541` bit is a whole extra argument that is read and thrown away.** Both call
  `VMValueStack_PopNumericDiscard` (`00267DB0`) before anything else. The verb accepts a parameter
  from the script and **does not use it**. Whatever it once meant, in the shipped binary it is
  discarded before the first slot is touched.~~ **Refuted 2026-09-14 (FABLE): the extra argument is the float.** `00267DB0`
  returns the popped value in `xmm0`, and `0540` / `0541` keep it (`movaps xmm6, xmm0` at `00350077` / `003507D7`). They
  push it as the float argument where `053E` / `053F` push `-1.0f` (`003500A9`–`003500AF`). See [§7's 2026-09-14 correction](#7-falsification-checklist).

*(Enumeration: all four verbs whose name begins `partystdmotion` and whose body is 151–157 bytes were
disassembled and their call sequences compared instruction by instruction. The call multiset is
identical apart from the leading discard.)* Disposition **B**.

## 3. The shape

`partystdmotionplay` in full:

```c
void partystdmotionplay(/* ... */ VMValueStack *stack)
{
    int32_t motion = VMValueStack_PopInt32CoerceFloat32(stack);   /* 00267E10 */
    const float k = -1.0f;                                        /* 01CEBC9C = 0xBF800000 */

    for (int slot = 0; slot < 4; slot++) {                        /* cmp ebx, 4 */
        void *actor = PartyRoster_GetActorBySlot(slot);           /* 00263750 */
        if (!actor) continue;

        FUN_0035AE10(actor, 1);                                   /* 27 B, see below */

        VMValueStack_PushInt32(stack, motion);                    /* 00267F90 */
        VMValueStack_PushFloat32Bits(stack, k);                   /* 00267F60, -1.0f */
        VMValueStack_PushInt32(stack, 1);                         /* 0 in the "withoutsame" pair */

        FUN_003580C0(actor, stack);                               /* 240 B */
    }
}
```

Three things worth stating plainly.

**Four slots — and a different *source* for the party, not merely a different function.** The loop
bound is the immediate `4` at `0034F0DB`, the same count the appearance verbs use. What differs is
where the four come from:

| verb family | how it finds the party | what that is |
|---|---|---|
| appearance, `040D`-`0413` | `0031B5A0`: read `[02EBF190] + 0x5A5A + 2*slot`, validate with class `0x17`, resolve through `BattleUnit_FindByDefinitionSelector`, then three gates and a 7..25 range split | an **authored id table** — slot map 1, [the combat-processing set](../../11-Party/active-party-reserve-and-the-moment-the-leader-changes.md) |
| motion, `053E`-`0541` | `PartyRoster_GetActorBySlot` (`00263750`, 23 B) | the **live four-pointer roster array at `0209A1F0`**, per [party roster and control suppression](../../11-Party/party-roster-and-control-suppression.md) |

**These are not two accessors onto one thing.** One walks an authored table of ids and resolves them
through the battle-unit registry, applying three gates and a range test on the way; the other reads
four actor pointers out of a runtime array. Nothing in either function reconciles them, and nothing
requires them to agree.

**A reimplementation that unified them would be inventing an agreement the binary does not contain**
— and the two would diverge exactly where it matters: an actor that is in the roster array but fails
the appearance verbs' gates gets its motion changed and its shadow left alone. Whether that ever
happens in shipped content is `SP-2`.

**The per-actor arguments travel through the VM value stack, not through registers.** The verb pushes
three values and calls `003580C0(actor, stack)`; `003580C0` then performs three pops of its own —
`VMValueStack_PopInt32CoerceFloat32` twice and `VMValueStack_PopNumericDiscard` once. So the shared
routine is written the way a *verb* is written: it reads its arguments off the script stack. The
party verbs reuse it by **synthesising a call frame** for each actor in turn.

**The float is ~~always~~ `-1.0f` for `053E` / `053F`.** It is loaded once, before the loop, from the `.rdata` constant at
`01CEBC9C` (`0xBF800000`), and pushed unchanged for every actor. ~~No verb in this family varies it.~~ *(Corrected
2026-09-14: `0540` / `0541` push the script's own extra argument instead, loop-invariant in the same way. See [§7's 2026-09-14 correction](#7-falsification-checklist).)*

### The prologue call

`0035AE10` (27 B) is a two-step adapter run once per actor *before* the pushes:

```text
0035AE19  call 00233F50        ; (actor, 1)  -- 28 B, unnamed
0035AE26  jmp  002ED020        ; (actor)     -- 31 B, unnamed, tail call
```

~~Both targets are unnamed and **were not read**.~~ What is established is the ordering: whatever this
does, it happens to each actor before that actor's motion request is submitted.

**Both read 2026-09-18 (FABLE).** `00233F50(actor, 1)` is `ActorWork_GetBattleUnit` (`0031B760`) followed by a tail call of `00233EA0(unit, 1)`, 167 bytes: when the unit's flag byte has bit 4, it runs `BattleUnit_ResetActionControlForStatusTransition` (`00300140`, argument 1), clears flag bits 8..9 and `+4` bit 6 (`00233EC7`, `00233ECD`); then, because the mode is 1, it tests the definition's status words `+0x64 | +0x3C` against `0x80000003` (KO, Stone, X-Zone, `00233EE9`) and returns if none is set; if one is, it asks `FieldData_GetActiveFieldRecordBit15` (`00313F60`) and returns when the field keeps such units; otherwise it spares a class-1 definition (`byte +5 == 1`) that is still referenced (`+0xE98` above 0) or whose record `[+0xE68]` has `+0x18 & 0xE == 4`, and tears every other one down with `BattleUnit_TeardownAndDespawn` (`00300E40`, argument 0, `00233F37`). `002ED020(actor)` returns unless the actor and its record at `+0xC0` exist and the record's dword is not -1; then it takes the record's `u16` id and calls `003E6A60`, which is `00426870(id, 003E74C0, 0)`: a call on the character-render record `022C6F28 + id × 0x740` with the presentation routine `003E74C0` (`00426870` returns at once for id -1). So the prologue clears a terminal-status actor out of the field where the field does not keep it, and notifies the surviving actor's render record, before its motion request is submitted. What the `-1.0f` means to the pop that consumes it is still open.
*Answered 2026-09-30 (SWE2-CONTRACT), static; control [`motion_pop_pairing.py`](../../_index/candidates/swe2contract-ddres-b1-0930/motion_pop_pairing.py) (P1–P5, FAILS 0).* The stack is last-in first-out,
so `003580C0` pops the **flag** first (`00267E10` → `r12d`), the **-1.0f** second (`00267DB0` → `xmm6`; that routine is
a float pop, not a discard — [the script-to-native bridge contract](../CONTRACT-script-to-native-bridge.md) §3 names it
misnamed in the ledger) and the **motion id** last (`00267E10` → `r15d`). It passes the motion in `r8d` and the float in
`xmm3`, and the flag chooses `003DDB40` (non-zero: `partystdmotionplay`) or `003DDBB0` (zero: the without-same pair);
each moves the float to `xmm2` and tail-jumps to the standard-motion starts `002EB3E0` / `002EB4F0`. There the float is
the **blend** argument ([the record behind every actor](../../04-Actor-Entity/Actor-Storage-Record/the-record-behind-every-actor.md),
eleventh pass: four of the six start entries hard-code `-1.0f` as this argument, so the verbs pass the engine's default).
Inside `002EB0D0` the blend is consulted only when the start's fourth argument is zero, which is `002EB3E0`'s case: a
blend at or above the compared value (0.0, per that page) calls `004270A0`, a blend below it — this `-1.0f` — calls
`004272E0` on the character render record. For `002EB4F0` the blend is not consulted and `00427860` commits instead.
**What the `004272E0` and `004270A0` arms do is RC-19.**

## 4. Key addresses

| Address | Working name | Body | Role |
|---|---|---:|---|
| `0034F060` | `partystdmotionplay` handler | 154 B | verb `053E`; third push = 1 |
| `0034F890` | `partystdmotionplaywithoutsame` handler | 151 B | verb `053F`; third push = 0 |
| `00350050` | `partystdmotionplay_540` handler | 157 B | verb `0540`; leading discard, third push = 1 |
| `003507B0` | `partystdmotionplaywithoutsame_541` handler | 154 B | verb `0541`; leading discard, third push = 0 |
| `00263750` | `PartyRoster_GetActorBySlot` | 23 B | slot -> actor, for slots 0-3 |
| `00267E10` | `VMValueStack_PopInt32CoerceFloat32` | 78 B | reads the motion id |
| `00267DB0` | `VMValueStack_PopNumericDiscard` (ledger name; it is a float pop) | 84 B | pops the `-1.0f` inside `003580C0`, and the discarded extra argument of `0540`/`0541` |
| `00267F90` | `VMValueStack_PushInt32` | 39 B | motion, and the same/without-same flag |
| `00267F60` | `VMValueStack_PushFloat32Bits` | 41 B | the constant `-1.0f` |
| `0035AE10` | per-actor prologue adapter | 27 B | `00233F50(actor,1)` then tail `002ED020(actor)` |
| `00233F50` | *unnamed* | 28 B | ~~**not read**~~ read 2026-09-18: `ActorWork_GetBattleUnit` then `00233EA0(unit, 1)` (§3) |
| `002ED020` | *unnamed* | 31 B | ~~**not read**~~ read 2026-09-18: notifies the actor's render record (§3) |
| `003580C0` | the shared per-actor motion routine | 240 B | read 2026-09-30: pops flag, blend, motion; commits through `003DDB40` / `003DDBB0` (§3) |
| `01CEBC9C` | `.rdata` constant | 4 B | `0xBF800000` = `-1.0f` |

## 5. What this document does not establish

- **Which pushed value is which argument of `003580C0`.** Three values go on (`int`, `float bits`,
  `int`) and three pops come off (`Int32Coerce`, `Int32Coerce`, `NumericDiscard`). **The pairing was
  not traced**, so which pop consumes the `-1.0f` is unproven. Stating an order here would be
  inference dressed as a formula. *Answered 2026-09-30 (§3): the pops are int, float, int — flag, blend, motion.*
- **What `003580C0` does with them.** 240 bytes, read only for its call targets. It reaches
  `WorldActor_GetDefinitionByte12OrMinus1` (`002E9C00`) and seven other routines, none read. *Answered 2026-09-30
  (§3; the interior citation below reads the body in full).*
- **What `-1.0f` means.** Universally a "no value / use the default" sentinel in this codebase's
  shape, but that is a pattern argument, not evidence from this function, and it is **not claimed**. *Answered as far
  as the image goes, 2026-09-30 (§3): it is the standard-motion blend, the default four start entries hard-code, and a
  negative blend selects the `004272E0` arm.*
- [x] **RC-19.** What the character render record's two blend arms do — `004272E0` (taken for a blend below the
  compared value, which the party verbs' `-1.0f` is) and `004270A0` (a blend at or above it) — as called from
  `002EB0D0` (`002EB29F`, `002EB2C9`). Registered 2026-09-30 (SWE2-CONTRACT); static.
  *Applied 2026-09-30 (records) RC-19:* **ANSWERED 2026-09-30 (static; ORACLE's record `rc18-map1-blend-arms-0930`, commit `1e4537034`): a negative blend is a hard cut, a positive blend a cross-fade of that length.** `004272E0` (blend < 0) only sets the render record's dirty request bit 5; `004270A0` with 0.0 also takes `00426FA0`'s reset mark; with a positive blend it stores it at `+0x308` and requests bit 8, which `00429F70` carries as a fade. So the party verbs' `-1.0f` means "switch to the new standard motion without interpolation".
- **Whether the two definitions of "the party" ever disagree.** Filed as `SP-2`.
  > *Answered statically 2026-09-12 (FABLE): they can, and only in windows a named few writers open.*
  > The writers of the live roster `0209A1F0` ([the roster page](../../11-Party/party-roster-and-control-suppression.md)) and of the authored slot map
  > `+0x5A5A` ([the battle-state block](../../11-Party/Battle-State-Block/the-battle-state-block-field-map.md)) were censused through the call graph. **Ordinary party changes write
  > both in one pass**: `PartyConfiguration_ReconcileRosterFromCurrentSelectors` (`003261D0`) and
  > `PartyConfiguration_SetSelectorsAndReconcileRoster` (`003273D0`) each assign the roster first
  > (`PartyRoster_AssignActorToSlot` at `00326416` / `00326435`), then set the selectors
  > (`PartyConfiguration_SetDefinitionSelectorForIndex`, `00326459`) and refresh the slot map's four
  > definitions last (`BattleGroup_RefreshFourActorDefinitions`, `003264BF`) — no frame boundary
  > between, so the two agree once the call returns. **One-sided writers exist on both sides:**
  > the roster alone is written by the end of the durative verb `setupbattle` (`0x0056`, end thunk
  > `003523B0` → `PartyRoster_ReapplyActorStoredSlot`), by the debug verb `debug_setpc` (`0x2021`,
  > `0050C610`), by `ActorStorage_InitializeRecord` when a record is (re)initialised with a slot
  > byte, and by the field-transition reset that zeroes the four pointers (`0026DB30`); the slot map
  > alone by `00233CF0` — reached from the read-in verbs `partyallread` (`0x03EB`), `partyallread2`
  > (`0x046F`), `summonread` (`0x0203`) and `summontopartyread` (`0x0207`) through `0037C980` /
  > `0037CA00` / `0037CA80` ([the verb table](../Verb-Dispatch/scriptvm-verb-table.tsv); the task they install runs
  > [the party read-in state machine](the-party-read-in-state-machine.md), 2026-09-14) and by `BattleSystem_ResetRuntimeState` →
  > `BattleSlotMap_InitializeMappingClasses`. So the appearance verbs (slot map) and the
  > standard-motion verbs (roster) can see different parties **between** one of those one-sided
  > writes and the next reconcile — after a field transition, after `setupbattle`'s end, after a
  > party read-in verb — and never inside a reconcile. Whether a shipped script actually issues an
  > appearance verb and a standard-motion verb inside such a window is a question about the
  > scripts; the mechanism is proven, the divergence not demonstrated.
- ~~**What the discarded argument of `0540`/`0541` was for.** It is popped and dropped.~~ *(Corrected 2026-09-14: it is not
  dropped. It replaces the `-1.0f` float passed to `003580C0`.)* What that float means is the open question above
  ("What `-1.0f` means"). Which values the shipped scripts pass is a question about the script data, not the
  executable.
- **Any runtime observation.** Every claim is static disassembly at the certified hash.

- [x] **RC-20.** Which script verbs the four Movement-filed bodies that call `VMValueStack_PushFloat32Bits`
  (`00267F60`) serve (the pass-22 crossing below). Registered 2026-09-30 (SWE2-CONTRACT); static: join each body to
  the verb table's handler addresses.
  *Applied 2026-09-30 (records) RC-20:* **ANSWERED 2026-09-30 (static; ORACLE's record `_index/candidates/rc20-float-push-verbs-0930/`, commit `1e4537034`):** the four bodies are the `begin` callbacks of seven family-0 movement verbs — `003548B0` (`rcmove`, `cmove`), `003488B0` (`rmove`, `move`), `00349680` (`ramove`; `amove` through the thunk `0033F850`), `00345430` (`ucmove`) — each pushing one float for `VM_ActorSteerToPosition` (`00357A20`); nothing else reaches them.

## Call chain (SWE2-CONTRACT, 2026-09-30)

```
zone script: CALL 053E / 053F / 0540 / 0541
  -> the verb handler (0034F060 / 0034F890 / 00350050 / 003507B0): pop the motion (0540/0541 also pop an extra value)
       for slot 0..3: PartyRoster_GetActorBySlot 00263750 (the live roster 0209A1F0)
         -> 0035AE10: 00233F50(actor, 1) then 002ED020(actor)                       <- the per-actor prologue
         -> push motion, -1.0f (or the extra value), flag; 003580C0(actor, stack)  <- THIS SYSTEM
              pops flag, blend, motion -> 003DDB40 (flag set) | 003DDBB0 (flag clear)
                -> 002EB3E0 | 002EB4F0 -> 002EB0D0 on the character render record 022C6F28 + id x 0x740
```

**Upstream (who causes this):** authored zone scripts, for the whole party at once.

**Downstream (what this causes):** a standard motion started on each present party member's render record, after
terminal-status actors the field does not keep are torn down.

**Do not confuse with:** the party appearance verbs, which collect slot map 1 rather than the live roster
([how a script changes how the party looks](how-a-script-changes-how-the-party-looks.md)).

## Modding notes (SWE2-CONTRACT, 2026-09-30)

- **Best intervention point:** the four handlers; each builds a per-actor call frame on the script stack, so a mod can
  vary the blend by pushing a different float before `003580C0` (the `0540` / `0541` pair already pushes the script's
  own extra argument there).
- **Breaks if:** the pushes are reordered — `003580C0` pops flag, blend, motion in that order.
- **Side effect to know:** the prologue can despawn a party member in a terminal status when the field does not keep
  such units (`00233F50` → `BattleUnit_TeardownAndDespawn`).
- **Multiplayer / XIIOnline:** script-driven; every client runs it.

## Claims, evidence and tier (SWE2-CONTRACT, 2026-09-30)

| claim | evidence | tier |
|---|---|---|
| Four verbs form a 2 × 2 (constant, flag) | the four handlers; the third `edx` write differs only (falsification pass 1) | 1 |
| The party is the live roster `0209A1F0`, slots 0–3 | `00263750`: `cmp ecx, 3 / ja`, `lea rcx, [0209A1F0]` | 1 |
| `003580C0` pops flag, blend, motion and commits through `003DDB40` / `003DDBB0` | `motion_pop_pairing.py` P1–P4 | 1 |
| The blend is consulted only for the plain verbs; `-1.0f` takes `004272E0` | `motion_pop_pairing.py` P5; the record page's eleventh pass | 1 |
| The prologue resets action control and may despawn a terminal-status actor | `00233F50` → `00233EA0` read 2026-09-18 (§3) | 1 |

## 6. Related

- [How a script changes how the party looks](how-a-script-changes-how-the-party-looks.md) — the other
  party verb family, and the *other* definition of "the party".
- [Party roster and control suppression](../../11-Party/party-roster-and-control-suppression.md) —
  `PartyRoster_GetActorBySlot` and the four-pointer roster array at `0209A1F0`, both read there.
- [Active party, reserve, and the moment the leader changes](../../11-Party/active-party-reserve-and-the-moment-the-leader-changes.md)
  — slot map 1, the authored table the appearance verbs read instead.

## 7. Falsification checklist

- [x] **The four verbs are a 2×2 over two independent bits.** *Killer:* a third difference. The call
      multisets are identical apart from the leading `00267DB0`, and the only differing immediate is
      the third push's `1`/`0`.

> **KILLER TEST RUN — 2026-09-13 (OPUS). No third difference exists, and the byte counts prove it
> rather than merely allowing it.** This page's §8 already asserts the multiset identity, so this is
> a **test of a standing claim, not a discovery.**
>
> **Call multisets, disassembled:**
>
> | verb | calls |
> |---|---|
> | `053E` `0034F060` | `00267F90`×2, `00267E10`, `00263750`, `0035AE10`, `00267F60`, `003580C0` |
> | `053F` `0034F890` | **identical to `053E`** |
> | `0540` `00350050` | the same **plus `00267DB0`×1** |
> | `0541` `003507B0` | **identical to `0540`** |
>
> Pairwise, the only difference anywhere among the four is that single `00267DB0`.
>
> **And the sizes close the argument: 154 / 151 / 157 / 154.** A third variable would have to show up
> as unexplained bytes; there are none. Diffing `053E` against `053F` leaves exactly one semantic
> instruction:
>
> ```
> -  mov edx, 1        ; 5 bytes  BA 01 00 00 00
> +  xor edx, edx      ; 2 bytes  31 D2
> ```
>
> **Three bytes — exactly 154 − 151.** Everything else in the diff is relocated branch targets and
> the same `.rdata` constant reached from a different address, which is what two copies of one
> function at two addresses must look like. The `_540` pair is `+3` for the extra `call`, `+2`… and
> lands at 157/154 on the same arithmetic.
>
> **One refinement to this checklist's wording.** It calls the differing value *"the third push's
> `1`/`0`"*. It is **not a push** — it is `edx`, the second integer argument in the Win64 register
> convention. The distinction matters for a reconstruction writing the call, not for the claim.
>
> **So the 2×2 holds on both axes, and the two bits are now named exactly:** the presence of the
> `00267DB0` discard pop, and `edx = 1` versus `edx = 0`.
- [x] **"withoutsame" is the third pushed value.** *Killer:* the constant not tracking the name.
      `053E`/`0540` push 1, `053F`/`0541` push 0, and the two `withoutsame` names are exactly the
      two zeros.
- [x] ~~**`0540`/`0541` discard their extra argument.**~~ **REFUTED 2026-09-14 (FABLE).** *Killer:* any use of its result.
      `VMValueStack_PopNumericDiscard` returns into nothing, and the next instruction begins the
      motion read.
- [x] **These verbs use a different roster than the appearance verbs.** *Killer:* the same callee.
      `00263750` here, `0031B5A0` there — different functions, computed with a tool.
- [x] **The float is loop-invariant.** *Killer:* a reload inside the loop. `movss xmm6` is at
      `0034F084`, before the loop head at `0034F090`, and `xmm6` is callee-saved across the body.

> **KILLER TESTS RUN — 2026-09-14 (FABLE). Three hold. One is refuted, and so is a refinement of OPUS's.**
> - **REFUTED: `0540`/`0541` discard their extra argument.** The killer is "any use of its result", and there is one.
>   `VMValueStack_PopNumericDiscard` `00267DB0` is misnamed. It decrements the stack count and **returns the popped
>   value in `xmm0`**: an int slot through `cvtdq2ps` (`00267DE0`), a float slot raw (`00267DD1`), and `0.0` on an
>   underflow or other tag. `0540` does `movaps xmm6, xmm0` right after the call (`00350077`; `0541` at `003507D7`)
>   and pushes `xmm6` per actor through `VMValueStack_PushFloat32Bits` (`003500A9`–`003500AF`). That is the slot where
>   `053E` pushes the constant `-1.0f` loaded at `0034F084`. **So `_540` / `_541` are the same verbs with a
>   script-supplied float in place of the `-1.0f` default.**
> - **Holds: "withoutsame" is the third pushed value.** `053E` loads `mov edx, 1` at `0034F0C1` before the third
>   `VMValueStack_PushInt32`, and `053F` loads `xor edx, edx` at `0034F8F1`. The names are `partystdmotionplay` /
>   `…withoutsame` (verb table). **OPUS's refinement above ("It is not a push — it is `edx`") does not stand:** `edx`
>   is the value argument of that `VMValueStack_PushInt32` call, so the constant *is* the third value pushed onto the
>   VM stack for `003580C0` to pop.
> - **Holds: a different roster.** `00263750` is `PartyRoster_GetActorBySlot` (bound `≤ 3`, table `0209A1F0`). The
>   appearance verbs' collector is `0031B5A0` (slot map 1 at `+0x5A5A`).
> - **Holds: the float is loop-invariant.** `053E` loads it at `0034F084`, and `0540` takes it once at `00350077`.
>   Both are before the loop head, and `xmm6` is not rewritten inside the loop.
>
> `00267DB0` has **440** direct calls and its name appears in 27 documents. The misname is routed rather than fixed
> here (`FABLE-NOTICE-OPUS-POPNUMERIC-MISNAMED`).

## 8. Falsification pass 1 — 2026-09-13 (OPUS)

*(Static only. Every figure below was re-measured from the shipped image and the function list by an
instrument that was given the addresses and not the claims. Nothing executed.)*

### ✔ Everything reproduces — there is no correction to make

This is the rare page where the pass finds nothing to fix, so the useful thing it can add is the
measurement itself.

| claim | measured |
|---|---|
| the four handlers are **154 / 151 / 157 / 154 B** | **154 / 151 / 157 / 154** |
| the withoutsame bit is `mov edx, 1` at `0034F0C1` and `003500B4`, `xor edx, edx` at `0034F8F1` and `00350814` | **all four instructions, at all four addresses** |
| the `_540` / `_541` pair pops an extra argument first | **`00267DB0` is the first call in both**, and in neither of the others |
| "the call multiset is identical apart from the leading discard" | **identical** — the only difference between any two bodies' call multisets is one `00267DB0` |
| the loop bound is the immediate `4` at `0034F0DB` | **`cmp ebx, 4` at `0034F0DB`**, and at `0034F908` / `003500CE` / `0035082B` in the others |
| §3's call order | **exactly**: `00267E10`, then per slot `00263750`, `0035AE10`, `00267F90`, `00267F60`, `00267F90`, `003580C0` |
| `0035AE10` is `00233F50(actor, 1)` then a tail `jmp 002ED020` | **`call 0x233F50` at `0035AE19`, `jmp 0x2ED020` at `0035AE26`** — both addresses as published |
| `003580C0` pops `Int32Coerce` twice and `NumericDiscard` once | **`00267E10` ×2, `00267DB0` ×1** |
| `003580C0` reaches `002E9C00` **and seven other routines** | **exactly seven**, once the three VM-stack calls and the two internal jump targets are set aside: `00263A30`, `002E97B0`, `002ED6F0`, `002E4C30`, `002EAC90`, `003DDB40`, `003DDBB0` |
| the nine stated body sizes in §4 (23 / 78 / 84 / 39 / 41 / 27 / 28 / 31 / 240) | **all nine** |

### ➕ Two things the measurement can add

**The discriminating instruction is uniquely identified, not merely named.** Each of the four bodies
contains **exactly three writes to `edx`**, and the first two are the same in all four — `mov edx, 1`
and `mov edx, ebp`. **Only the third differs**, and it is the one §2 names. So "the constants are the
evidence" is stronger than it reads: there is no other candidate instruction in any of the four
bodies.

**The roster array resolves from the code, not from a citation.** `00263750` is
`cmp ecx, 3 / ja` — slots **0–3** — then `lea rcx, [rip + 0x1E36A91]`, which is **`0209A1F0`**, the
live four-pointer array the roster page names. The bound and the base are both in the 23 bytes.

**Not claimed.** Everything in §5 stands: which pushed value pairs with which pop, what `003580C0`
does, what `-1.0f` means, and `SP-2` as FABLE narrowed it. *(The first three are answered since, 2026-09-30, §3; the two
functions below were read 2026-09-18.)* `00233F50` and `002ED020` remain unread *(read since, 2026-09-18, FABLE: the note at the section on `00233F50`; pointer 2026-09-30, OPUS)* —
**this pass measured that `0035AE10` calls them in that order, not what they do.** Nothing executed.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited.*

- **Movement — CLIENT and SERVICE.**
  - `PartyRoster_GetActorBySlot` (`00263750`) is read by three movement bodies (67–250 B).
  - `002E97B0` is read by `WorldActor_UpdateRuntimeAndScriptExecutionState` and a 193-byte body.
  - `002ED020` and `0035AE10` are read by a 475-byte movement body.
  - `PartyRoster_AssignActorAndCommitFocus…` (`0050C610`) calls the 10-byte movement-body-pool consumer.
  - `00233CF0` calls a 7-byte helper.
  - `VMValueStack_PushFloat32Bits` (`00267F60`) is also called by four Movement-filed bodies (88–233 B), which push floats onto the script stack. Which verbs they serve is not read. *(Registered as RC-20, 2026-09-30, SWE2-CONTRACT.)*
  - The id-validity query is also asked by two locomotion bodies.
- **Input — CLIENT.** `PartyRoster_GetActorBySlot` is read by the ~~unread~~ 1,936-byte Input body *(read since: `00226BE0`, the system-stop registry's request start — [its contract](../../00-Engine-Core-Runtime/System-Stop-Registry/CONTRACT-system-stop-registry.md) §2; pointer 2026-09-30, SWE2-CONTRACT)*.
- **Items_Equipment_Shops_License — CLIENT and MECHANICAL.** `0037CA80` is run by
  `BattleStats_ClearAllEquipmentSlotsByMappedId`; the id-validity query is shared with thirteen licence and equipment
  functions.
- **Resource — CLIENT.** `002ED6F0` is read by a 295-byte Resource body.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Status_Periodic_Terminal — CLIENT.** `BattleEncodedId_IsValidForClass` is also called by three status bodies: `BattleStats_RecomputeDerivedStateAndAutoStatuses`, `BattleStats_ModifyStatusLayerStateAndProcessSideEffects` and `BattleUnit_RunPeriodicCombatMaintenance`. The class check is shared with the status layer, not owned by the verbs.

## Crossings into other layers — FINAL-AUDIT pass 22 (OPUS, 2026-09-18)

**Spawn, encounter and lifecycle — thirty-one edges, and twenty-four of them arrive through one
thirteen-byte accessor.** The carrier is `ActorWork_GetBattleUnit` (`0031B760`), named above as the
first step of `00233F50`. Its entire body is a null guard and a forward — `test rcx, rcx` / `jne` /
`xor eax, eax` / `ret`, else a `jmp` — and the spawn and encounter layer calls it from **twenty-four
distinct bodies**: the entry selectors, the death-count and cooldown getters, the candidate and group
setters, and the ranged retire scan. **Citing a thirteen-byte accessor imports every caller it has.**
None of those callers is a claim by this page, whose subject is what the standard motion verbs
submit; the accessor is simply the one step that turns an actor handle into its battle unit.

**Five more through the teardown, and only one runs in this page's direction.**
`BattleUnit_TeardownAndDespawn` (`00300E40`, 375 B) is reached here from `00233EA0`'s terminal-status
branch. Four of its five edges into that layer are its own **callers** — the grouped, the
mask-selected and the ungrouped group teardowns, and the ranged retire scan — so the encounter layer
drives the same teardown this page arrives at by another route. The fifth is its callee: a 29-byte
routine that clears an entry's transient selection state before the unit goes.

**Two through the field-record thunk.** `00313F60` is five bytes of `jmp`. The ranged retire scan and
the candidate-distance check ask it the same question about the same bit that this page asks before
tearing a KO, Stone or X-Zone unit down. **The bit is the field's, not this page's**, and both layers
consult it independently.

*Nothing in that layer is owned here.* All thirty-one edges are fan-out from three shared entries
this page names in passing while reading a motion verb's prologue — the class this pass recorded on
`static-initialisers-and-teardowns.md` and `five-small-bin-tables.md`, at a smaller carrier than
either.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**CombatAI — CLIENT.** `BattleEnmity_AnyAboveThreshold`, owned by that layer, calls `00322C50` on this page. That caller is the threshold scan over the same enmity bytes at `[+0x6A0] + 0x19`, id by id; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**CombatFormula — CLIENT.** `BattleStats_RebuildEffectiveStatsAndAffinityState`, owned by that layer, calls `00322C50` on this page. That caller is the effective-stats re-form, and it says where its output lives: with no explicit destination it writes the record's **own `+0x24` block, `0x24` bytes wide**, and the block at `+0x50`, taking its mode from the flag word at `+0x3C`; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Save_Load_Settings — SERVICE.** `0026DB30` on this page calls `SaveImage_GetPersistentPayloadBase`, owned by that layer. What it reaches is a 20-byte accessor returning `002EF640() + 0x200` - **the base the persistent flag banks are indexed off**, so those banks live inside the save payload; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**UI — CLIENT.** `BattleMenu_BuildCommandEntryList`, owned by that layer, calls `00322C50` on this page. That caller is the command-list build, and the ceiling is in the first instruction: the menu kind is bounded at **`0x22`** into a jump table, after which `dword[+0x40]` is zeroed and `dword[+0x44]` set to `-1` before any entry is written; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

> **Dispositioned 2026-09-14 (OPUS).** Pass 22 reports a neighbouring subsystem this
> page never mentions. These are shared entry points — the relationship is that this
> page's code asks a common question, not that the two subsystems interact here. Each
> was read from the shipping bytes; the reading is in
> [`the shared neighbours pass 22 keeps finding`](../../00-Engine-Core-Runtime/Shared-State-Accessors/the-shared-neighbours-pass-22-keeps-finding.md).

| this page cites | which calls | owned by | and that is |
|---|---|---|---|
| `0031B5A0` | `00322C50` | **Gameplay** | `BattleEncodedId_IsValidForClass`, the shared *is this encoded id valid for this class* query — a 32-entry jump table on the class |


## Interior citation — frontier hub `002E97B0` (2026-09-18, SWE2-EC7)

`002E97B0` — 16 B, 31 callers; the `+0xC0` record getter the motion verbs consult.
Interior verified: null-guard then `mov rax, [rcx+0xC0]` at
[`002E97B5`](../../_index/ADDRESS-INDEX.md) — the actor's secondary record, the same field
`002E8FD0`/`002E8EE0` dereference for render records.


### Interior citation — frontier hub `003580C0` (2026-09-18, SWE2-EC7)

`003580C0` — 240 B, 8 callers: the dispatch body the call multiset above
belongs to, read in full. `00263A30(word[rcx], byte[rcx+0x15])` resolves the
context; `002E97B0` and the `00267E10`/`00267DB0` pair pull the live state;
`002E9C00` returns a status whose negative arm substitutes
`002ED6F0([rbx+0x14], &out, &out2)` at
[`0035814E`](../../_index/ADDRESS-INDEX.md) (esi = 1 vs `result+2`); then
`002E4C30`, `002EAC90`, and the `003DDB40`/`003DDBB0` tail pair run the
motion commit. The verb's whole shape in one body.

### Interior citation — frontier hub `002E9C00` (2026-09-18, SWE2-EC7)

`002E9C00` — 33 B, 8 callers, `WorldActor_GetDefinitionByte12OrMinus1`: the
status read `003580C0` consults mid-dispatch. `rcx` or `[rcx+0xC0]` null
returns `-1`; otherwise `movsx eax, byte [rax+0x12]` at
[`002E9C1C`](../../_index/ADDRESS-INDEX.md) — the signed definition byte the
verb predicates on.

### Interior citation — frontier hub `0037CA80` (2026-09-18, SWE2-EC7)

`0037CA80` — 113 B, 5 callers: the init-and-run — `002F16B0()` result is
stored to `02EBF400` and its `+0x10` slot gets a function pointer
(`0037C730`) at [`0037CAA3`](../../_index/ADDRESS-INDEX.md); three sibling
globals get field resets (`+8` = 0, `dword` = 0, `+4` = 4, `+0x1C` = 0) and
two flag bytes, then it tails `00233CF0`. The null arm returns silently.

*Crossing note (SWE2-EC7, 2026-09-18):* `002F16B0`, the accessor this init
calls, is itself called from the Audio layer — the crossing is that call,
not a shared responsibility.

## SWE2-EC7-27 update (2026-09-18) — `002EAC90` / `002E4C30` the two shared callees

`002EAC90` (44 B) null-safely digs `[rcx+0xC0]` and forwards
`movsx byte[+0x12]` — `edx = -1` when the chain is dead — into
`002EC6B0`. Interior anchor `002EACB3` (the `+0x12` read).

`002E4C30` (63 B) checks the caller's `word[+0x1E]` against the
`02161DA0` row table (`index * 9 << 5` = 0x120 stride): the row's
`dword[+0x5C]` must equal `[rcx+0x24]`, then `edx` either `bt`-tests
`dword[+0x24]` (non-negative bit) or returns 1 (`edx < 0`); a dead
row returns `-1`. Interior anchor `002E4C4E` (the row compare).

## SWE2-EC7-28 update (2026-09-18) — `002EC6B0` channel-commit dispatcher

`002EC6B0` (420 B) is the body `002EAC90` digs to: stores `sil` into
`[[rcx+0xC0]+0x12]` first. For `edx >= 0` it resolves the `02161DA0`
row (`word[+0x1E]` index, `0x120` stride), verifies `+0x5C ==
[+0x24]`, and `bt [+0x24], esi` gates a `dword[+0x60 + esi*4]` read
into `002EDD20(word[rbx], edx)`; a second pass on bit 0 feeds
`dword[+0x60]` into `002EDE20`. For `esi < 0x10` it also runs the
`022C6F28` `0x740` row of `word[rbx]` (`+0x284`-gated): two
`0020E620` calls commit `+0x42C`/`+0x430`, and `btr [+0x284], 0x12`
clears the consumed bit. Interior anchor `002EC73D` (the `bt`).
## SWE2-EC7-31 update (2026-09-18) — `00233F50` resolve-and-forward

`00233F50` (28 B) is the two-step the motion verbs share:
`0031B760()` resolves the current object, then a tail
`jmp 00233EA0` runs the verb body on it with `edx` passed through
— resolve-then-dispatch, no work of its own. Interior anchor
`00233F67` (the `jmp 00233EA0` tail).

## SWE2-EC7-41 update (2026-09-19) - `002ED6F0`

`002ED6F0` (356 B) is a call-free encoded-id dispatcher - `cx` low 16 is the index, `ecx >> 16 - 0x43` selects among `0x34` cases via the image-base tables at `+0x1CD854`/`+0x1CD888`; each case writes a kind dword and `stride * index` to the two out pointers. Interior anchor `002ED724` (the `jmp rcx` dispatch).

## SWE2-EC7-77 update (2026-09-20) - `00233CF0` three-call step measured

`00233CF0` (36 B) is the fixed sequence the party-presentation verbs
share: `0030D8B0(0)`, `003266C0()`, `00311E10(1)` in order, then
return 1 - a three-phase step with hardcoded 0/1 parameters, not a
dispatch.
Interior anchor `00233CFB` (the `003266C0` call).
