---
system: The status write and its side effects — what adding or removing a status actually does, in order
category: 10-Status-Periodic-Terminal
status: AUDITED
owner_layer: PrimaryOwner:Status_Periodic_Terminal
evidence_tier: 1
readiness: BEHAVIORALLY UNDERSTOOD
confidence: PROVEN
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: BattleStats_ChangeStatusAndProcessSideEffects (1,323 B) read to every ret from the
    shipping EXE with every RIP target computed by a tool; its per-status terminal jump table
    decoded from the image; five helpers read; caller counts checked with check_caller_claims
    (control memcpy 632). The mode table and the terminal cases for statuses 0, 1 and 31 were
    already read by two other pages and are cited, not re-derived.
last_reviewed: 2026-09-10
audit:
  passes: 1
  last_pass: 2026-09-12
  last_pass_state: opus-the-status-write-pass-1
  last_pass_kind: authored
  crossref_clean: true
  reopened_count: 0
---

# The status write and its side effects

> One function owns every status transition in the game. Two pages had read its mask table and its
> terminal switch; this page reads the rest — the gates, the party-side shortcut, the two per-status
> arrays it initialises, the "only a change fires anything" rule, the status's own result record,
> the cascade from the authored status table, and what each terminal status does — and puts the
> whole function in execution order.

## 1. What the player sees

A status icon appearing or disappearing, and everything that comes with it: the Petrify countdown,
the stone statue at the end of it, a character dropping when KO'd and the party collecting the
rewards, a Reflect that Slow cannot be cast through. All of it goes through
`BattleStats_ChangeStatusAndProcessSideEffects` (`0030E360`, 1,323 B), fourteen call sites in ten
functions. The rules it enforces:

1. **A source that may not affect the target changes nothing**, and for the three terminal statuses
   a second gate applies.
2. **~~A party-type unit~~ A summoned Esper given KO, Stone or Vanished goes straight to defeat cleanup** *(corrected 2026-09-26, FABLE: type `0x1B..0x27` is exactly the thirteen Esper rows of the 40-row party table)* — no mask
   write, no event, no rewards.
3. **Adding a status a unit already has, or removing one it lacks, is a complete no-op.** *(In this function. One level up, a re-cast restarts the timers of fourteen statuses - see §6. Scoped 2026-09-29, FABLE, Claude Opus 5.5.)*
4. **Adding a status gives it a parameter and a timer**, from the caller or from the authored
   status table.
5. **If the status was already present in the other mask, nothing fires** — presence is the union
   of two words.
6. **A status applies its own result record** through the ordinary applier, and **clears the
   statuses its definition says it clears**.
7. **The terminal statuses end the unit** and one of them plays the death reaction; four others
   have small terminal effects of their own.

## 2. Native mechanism

### 2.1 Signature, and the decisions made at entry

```c
void BattleStats_ChangeStatusAndProcessSideEffects(
        BKBI    *target  /* rcx */, BKBI *source /* rdx, may be NULL */,
        uint8_t  status  /* r8b, 0..31 */, int paramA /* r9d, < 0 = default */,
        int paramB /* [rsp+0x20], < 0 = default */, uint32_t flags /* [rsp+0x28] */,
        int mode /* [rsp+0x30], 0..5 */);
```

Both records are mapped to their units (`BattleStats_FindOwningBattleUnit` at `0030E39A`,
`0030E3A7`). Then, at `0030E3BB`–`0030E41C`:

| local | value | meaning |
|---|---|---|
| `adding` | `mode == 3 \|\| mode == 4` | the two *set* modes on the status words (`0030E3C2`–`0030E3CB`) |
| `initialises` | `mode == 0 \|\| mode == 3` | the two modes on the **first** word `+0x64` — only these write the parameter and timer (`0030E3CF`–`0030E3E0`) |
| `showReaction` | `!(flags & 0x10)` | (`0030E3EF`–`0030E3FC`) |
| `extraEffect` | `!(flags & 0x02)` | (`0030E3F2`–`0030E400`) |
| `bit` | `1 << status` | (`0030E40A`–`0030E410`) |
| `wasPresent` | `((+0x3C \| +0x64) & bit) != 0` | presence is the OR of the two status words (`0030E404`–`0030E41C`) |

### 2.2 The gates, and the ~~party-side~~ Esper shortcut *(corrected 2026-10-02, OPUS)*

With flag bit 0 clear, `BattleTarget_HasLow16EligibilitySuppression(targetUnit, sourceUnit)`
(`0030B9B0`) non-zero **refuses** (`0030E424`–`0030E433`), and when adding,
`BattleTarget_HasHigh16EligibilitySuppression` (`0030B8E0`) non-zero refuses **only for a terminal
status** — `bit & 0x80000003` (`0030E443`–`0030E45A`). The two are the halves of the packed mask
[the periodic tick](../Periodic-Tick/what-the-periodic-tick-does.md) §"two suppression gates" decoded.

Then, when adding (`0030E460`):

- **the ~~party-side~~ Esper shortcut** *(corrected 2026-10-02, OPUS: type `0x1B..0x27` is the thirteen Esper rows; §1 and CONTRACT-status-write.md §10 row 3)*: a target unit whose record has kind byte `+5 == 0` and type byte
  `+4` in `0x1B..0x27` (`0030E478`–`0030E488` — the same thirteen-value range
  [the kind byte page](../../04-Actor-Entity/Battle-Record-Kind/battle-record-kind-byte.md) §2 found
  the type-keyed classification testing) given a **terminal** status runs `00300FC0(unit, 0)` —
  the defeat cleanup — **and returns without touching the masks** (`0030E48A`–`0030E49C`);
- otherwise a terminal status on a unit that **already has one** is refused unless
  `FieldData_GetActiveFieldRecordBit15()` (`0030E4A1`–`0030E4BD`) — the same pair the HP write and
  the retire code test.

### 2.3 The mask write — six modes over three words

Already decoded by [the definition-record flag pair](../../04-Actor-Entity/the-definition-record-flag-pair.md)
§2 from the jump table at `0030E88C`: modes 0/1/2 **clear** the bit in `+0x64` / `+0x3C` / `+0x38`,
modes 3/4/5 **set** it, and **every case refuses when the bit is already in the requested state**
(`0030E4EA`, `0030E500`, `0030E516`, `0030E529`, `0030E546`, `0030E55A`); mode 3 additionally
refuses when the bit is set in `+0x38` (`0030E531`). A mode above 5 returns (`0030E4CB`–`0030E4CE`).

### 2.4 Two per-status arrays, initialised only by the `+0x64` modes

When `initialises` (`0030E567`):

```asm
0030E56E  mov  ecx, [rsp+0x48]              ; paramA
0030E572  test ecx, ecx / jns keep          ; negative = default:
0030E581  call 0x387730                     ;   BattleStatus_ComputeDefaultDwordParameter(0, target, status)
0030E594  mov  [rsi + status*4 + 0xBC], ecx ; TARGET +0xBC[status]  (u32)
0030E58D  mov  eax, [rsp+0x220]             ; paramB
0030E59B  test eax, eax / jns keep          ; negative = default:
0030E5A2  call 0x3876D0                     ;   BattleStatus_ComputeDefaultShortTimer(status)
0030E5AF  mov  [rsi + status*2 + 0x13C], ax ; TARGET +0x13C[status] (u16)
```

**So a BKBI record carries a dword and a word per status** — `+0xBC[32]` and `+0x13C[32]` — and
they are exactly where [the result applier](../../07-Combat-Action/applying-a-result-to-a-target.md)
§"The decode" step 9 copies its `+0x5C[32]` / `+0xDC[32]` arrays to (`+0x60` past their record
positions is `+0xBC` and `+0x13C`). The applier's status loop passes those same values as `paramA`
/ `paramB`; a caller that passes `-1` gets the authored default.

`BattleStatus_ComputeDefaultShortTimer` (`003876D0`, 88 B) reads the status's definition record —
the table at registry slot `02EBF118`, stride `*(u16*)(base+8)`, relocated through
`ImageAddress_ResolveRuntimePointer` (`003876D6`–`0038770E`) — takes its byte **`+9`**, and returns
`byte9 × [01DFE0B4] × 30` (`00387714`–`0038771F`): the definition's duration unit, scaled by the
status timer scale, in thirtieths. `BattleStatus_ComputeDefaultDwordParameter` (`00387730`, 645 B)
~~is not read here (`FA-1`).~~ *(answered: see §2.4a and §7 `FA-1` — the default duration; 2026-10-02, OPUS)* **These are not the eight `+0x17C` timers the periodic tick decrements**;
those come from the applier's `+0x42`–`+0x50`. ~~What reads `+0xBC` and `+0x13C` is `FA-2`.~~ *(answered: see §2.4a and §7 `FA-2` — the periodic tick's stage 2, `00386C70`; 2026-10-02, OPUS)*

### 2.4a What the two arrays are: a duration countdown and a beat timer, both driven by the periodic tick (FA-1 / FA-2, 2026-09-12)

**`+0xBC[s]` is the status's remaining duration; `+0x13C[s]` is its periodic beat timer.** Both are
consumed by stage 2 of [the periodic tick](../Periodic-Tick/what-the-periodic-tick-does.md), `BattleFormula_AdvanceStatusTimersAndBuildResult`
(`00386C70`, 935 B, read whole), and written back through the result record — which is why the
typed census found no reader: the loop addresses the target's arrays as *record + (target − record
+ 0x60)* (`00386CA9`–`00386CB2`, `00386CC6`; `[rcx + r15]` at `00386CEB` is `+0x13C[s]`, `[r14]` at
`00386E3E` / `00386EE4` is `+0xBC[s]`) and stores the new values into the record's `+0x5C[s]` /
`+0xDC[s]`, which the applier's step 9 copies back (non-negative values only).

**The default duration** (`00387730`; its first argument is never read — `rcx` is overwritten at
`003877A3`; the second is the *target* record, the third the status id):

```
if s == 2 or s == 6:                     return 11                          ; Petrify / Doom: a count, not a time
row  = status_data[s]                                                       ; 02EBF118, stride *(u16*)(base+8)
if row.+8 == 0xFF:                       return 0                           ; no duration
vit  = target ? target.+0x2C : 0                                            ; Vitality
if row.+6 & 0x2000:  v = trunc(2·row.+8 − row.+8 · vit / 100.0)             ; harmful class: Vitality shortens
else:                v = trunc(row.+8 + row.+8 · vit / 100.0)               ; beneficial class: Vitality lengthens
                     if target.+0x6B bit 6 or target.+0x7B bit 6: v = trunc(v · 1.5)   ; effect id 30 in either layer
return [01DFE0B4] · v · 300
```

(`00387740`–`00387759`; `003877A6`; `003877BA`; `00387801`–`003878AB`, constant `100.0` at
`008F3134`; `003878B4`–`0038797B`, `1.5` at `00901B3C`; `0038797F`–`00387992`.) `[01DFE0B4]` is the
frame base — 1 at 30 fps, 2 at 60 ([the boot page](../../00-Engine-Core-Runtime/what-the-engine-fixes-at-boot.md)) — so the dword is `v × 300` frame-units at
30 fps and the beat timer `row.+9 × 30`. In the shipped table `row.+8` is a base duration on 21
statuses and `0xFF` on the other eleven, and bit 13 of `row.+6` is set on exactly the harmful ids
0–16, 29 and 31 ([the thirty-two statuses](../the-thirty-two-statuses.md) §2.1); the `×1.5` on the beneficial class through an effect id 30
of the `+0x68` / `+0x78` layers is the shape of a duration-extending augment, whose authored name
is not read here.

**Stage 2 spends them like this**, once per present status `s` (`00386CD0`–`00386F72`; the loop
skips every status but Stop itself while Stop (bit 3) is present, `00386CDE`–`00386CE5`,
`00386E97`–`00386E9E`):

| step | what happens |
|---|---|
| beat | `t = +0x13C[s] − 10`; if `t > 0` → record `+0xDC[s] = t` and the status does nothing this tick (`00386CEB`–`00386CF5`, `00386E84`) |
| beat expired, `s` = 2 / 6 | record `+0x5C[s] = +0xBC[s] − 1` — the Petrify / Doom count steps down; the beat reloads to `row.+9 × [01DFE0B4] × 30`, or to `ComputeDefaultShortTimer(s) / 4` when the new count is 1 (`00386E3E`–`00386E72`) |
| beat expired, `s` = 8 (Poison) | flag A `\|= 0x140`; HP delta `−= floor(maxHP / 16)` with max HP doubled under Bubble (bit 28), or `max(currentHP, 1) / 16` under Disease (bit 16); a zero share becomes `−1`; flag C `\|= 0x4000` (`00386D9B`–`00386E39`) |
| beat expired, `s` = 10 (Sap) | if current HP `> 1`: flag A `\|= 0x100`, HP delta `−= 1` — Sap cannot kill (`00386D89`–`00386D99`) |
| beat expired, `s` = 25 (Regen) | flag A `\|= 0x500`; HP delta `+= (rand % level) + 1` — `RNG_MT19937_NextU32_Thunk`, unit level at `+0x1C2` (`00386D20`–`00386D3D`) |
| beat expired, other | the beat reloads only (`00386E48`–`00386E50`, `00386D44`) |
| duration | for a status in `+0x64` but not `+0x3C` (`r13 = +0x64 & ~+0x3C`, `00386C8C`–`00386CA2`): if `row.+8 != 0xFF`, record `+0x5C[s] = +0xBC[s] − 10`; when the value is `≤ 0`: Petrify (2) → apply mask `\|= bit 1` (**Stone**), Doom (6) → flag A `\|= 0x108`, HP absolute `0` (**KO**); and for any status with a `row.+8` duration the remove mask `+0x58 \|= bit` (`00386E88`–`00386F55`) |
| after the loop | ~~when the record carries an HP write (flag A bit 8):~~ **on every call** *(corrected 2026-09-29, FABLE, Claude Opus 5.5, on OPUS's replay ced7c61fd; bytes `00386F78`–`00386F95` re-read: flag A bit 8 only chooses the compared value, the new HP (absolute when bit 3) with an HP write, else the current HP)*: the resulting HP against `max HP / 5` (Bubble doubled, Disease → `max(current, 1)`) adds HP Critical (29) below the line and removes it at or above it, or when HP is `≤ 0` (`00386F78`–`00386FF3`). *Independently accepted: ASTRA/SOL, Method A on the original bytes (`df93a1eb7`, `_experiments/evidence/poison-q6-independent/`), ratified by SWE2-AUDIT-SPEC (`a95c664bf`). Five planted boundary cases at max HP 1,000: HP 199 applies bit 29; HP 200 and HP 0 remove it; Stop with Poison gives no HP delta; Bubble doubles the line to 400. Current HP is in `r8d` at `00386F95` with bit 8 clear. Limits: planted state; scheduling, caller reachability and lifetime are not observed.* |

So a status in **word 2 (`+0x3C`) never runs out** — only word-1 statuses count down — and the
Petrify / Doom **count is what the player sees**: `+0xBC[s] − 1` is copied into
[the unit display record](../../04-Actor-Entity/Unit-Display-Record/the-record-00329220-builds.md) at `+0x66 + s` (`00329500`–`00329539`), and two lookalike readers, `0031FC70`
(actor → 32 bytes of `count − 1`, `0xFE` elsewhere; called by `002C6F70`) and
`00320CF0(slotIndex, s)` (the raw count for a present status 2 / 6, else `−1`; called by
`00470780` / `00470B70`), read nothing else from the arrays. The default count 11 therefore shows as **10**; the count steps down every beat
(`row.+9` = 45 for Petrify, 100 for Doom), the last step at a quarter beat, and the status resolves
one tick after the count reaches 0.

**A Poison tick can KO its target.** *(Added 2026-09-29, FABLE, Claude Opus 5.5; `PKG-GP-STATUS-POISON` Q7;
`_index/candidates/pkg-gp-status-poison/poison_ko.py` A S H M, static.)* The chain has three links:
1. The Poison arm sets flag A bits 6 and 8 (`0x140`).
2. The result applier's HP step runs on bit 8. From `0x140` it derives the HP-write flags `0x40`, which suppress only the
   *alive* event, and it uses the delta writer.
3. [The HP write](../../08-Combat-Formula/Current-HP/the-hp-write-and-the-lethal-transition.md) §2.3 and §2.5 clamps the
   new HP to the unit's floor and takes the lethal branch when the stored HP is at or below that floor. Nothing on the path
   tests for a tick.

So a target at 40 of 1,000 HP loses its share of 62, is clamped to floor 0, and dies. The kill is then the Poison-tick kill
whose rewards `EZ-6` and `FA-4` describe (the target's `+0xE9A` bit 2, set by the same apply). Sap is the exception: it acts
only above 1 HP, as the table says. The two eligibility gates can still suppress a tick's damage for a particular unit, as
they can any damage.

**The other two writers of the arrays' record slots** are calculator slot 118 (`0038FCE0`, the
apply-mask writer of [the result record](../../07-Combat-Action/Result-Record/the-result-record-field-map.md)): for each status of the action row's `+0x18` mask that the
candidate mask allows, is absent from the target's `+0x38` / `+0x3C`, is not refused by
`row.+6` bit 8 on a non-kind-0 target and is not excluded by `row.+0x20` against the context's `+8` (and is never KO, `0038FE19`),
it sets the apply bit and writes `+0x5C[s] = 00387730(·, target, s)` when the *first* argument's
record already has the bit in its `+0x3C`, else copies that record's own `+0xBC[s]` / `+0x13C[s]`
(`0038FD60`–`0038FEA9`); and `BattleFormula_AppendStatusAddOperation` (`00387BB0`), which writes
the default dword, forces 11 for ids 2 / 6, and the default beat (`00387C57`–`00387C86`).

### 2.5 Nothing fires unless presence changed

```asm
0030E5B7  mov  eax, [rsi+0x3C] ; or eax, [rsi+0x64]
0030E5BD  test edi, eax ; setne al                     ; present now?
0030E5C7  cmp  eax, [rsp+0x4C]                         ; same as before?
0030E5CB  je   return                                  ; -> no side effects at all
```

Presence is the OR of `+0x3C` and `+0x64`, so **setting a status in one word while the other already
holds it writes the bit and fires nothing** — the same rule the status-layer function applies to its
two layers ([two-layer effect model](../Status-And-Augment-Layers/two-layer-effect-model.md) §11).

### 2.6 The side effects, in order

| # | site | gate | what |
|---|---|---|---|
| 1 | `0030E5D1`–`0030E60E` | — | a `0x148`-byte result record is zeroed and built, `(target, status, &record)`: **adding** → `00386A50`, **removing** → `00386A70`. Both start with `BattleFormula_InitializeResultRecord(&record, 0, target)` (`003848E0`, at `00386A61` / `00386A8F`). **On add the record is then marked inactive** (`00386A66 and [+0x2C], ~1`) — nothing is applied. **On remove, only status 28 with current HP non-zero does anything**: `+0x2C \|= 0x108` (apply HP, absolute) and `+0x24 = (HP + 1) / 2` (`00386A94`–`00386AB0`); every other removal is marked inactive (`00386AC3`) |
| 2 | `0030E610`–`0030E638` | record `+0x2C` bit 0 | `BattleFormula_ApplyTargetResult(&record, NULL, target, 0xFFFF, flags)` — so in the shipped data this fires for exactly one transition: **removing status 28 halves the unit's current HP, rounded up**, through the ordinary HP write. Status 28 is also the bit that doubles the HP cap ([the HP write](../../08-Combat-Formula/Current-HP/the-hp-write-and-the-lethal-transition.md) §2.3); the two mechanics together are the shape players know as Bubble, ~~and the name is still not attached here (`EY-1`)~~ and status 28 is **Bubble** *(answered: see the thirty-two statuses §2, row 28; 2026-10-02, OPUS)* |
| 3 | `0030E63D`–`0030E6D7` | adding | **the cascade**: the status's definition record (`02EBF118`, stride from `+8`, relocated as in 2.4) gives a 32-bit mask at **`+0x0C`**; for every set bit *i*, **`0030E360(target, source, i, 0, 0, flags \| 0x200, mode 0)`** — *clear* status *i*, without the final recompute. This is the `clearMask` [the field-record page](../../03-World-Area-Field/Field-Record-Table/field-record-table-navimapdata.md) §10 used to check the help-text alignment (Stone clears Petrify, Haste clears Slow) |
| 4 | `0030E6E7`–`0030E6FF` | `showReaction`, adding, target unit | `003284D0(unit, status)`: behind `002FA3B0(unit->p_10)` (`003284E4`; the gate reads only `rcx` — "within 24 units of the party leader", corrected 2026-09-12, `EY-5`), enqueues `{p_10, status, 2}` through `BattlePresentation_EnqueueReactionWithRandomizedVariant` (`00328513`) — **the status-applied reaction** |
| 5 | `0030E704`–`0030E727` | `extraEffect` | adding → `0046A800(target, status)`: only for status **1** (`0046A83A` → `0x12`) and **31** (`0046A847` → `0x11`), behind `002FA390()`, into `0046AB10(target, code, &zeros)` — **the battle event poster**: `0x12` posts "… turns to stone." and `0x11` "… is cast into the void.", rows `0x12` / `0x11` of `battle_message.bin` ([the post-result events page](../../07-Combat-Action/Post-Result-Events/the-post-result-events-and-the-battle-message-table.md) §2.7; `FA-3`'s poster half, **answered**); removing → the 3-byte stub `0016D6A0`, reached by the same `call rax` through a `cmovne` — the call happens either way, only the callee differs |
| 6 | `0030E729`–`0030E759` | target unit, status ≤ 31 | **the terminal switch**, section 2.7 |
| 7 | `0030E816`–`0030E828` | `!(flags & 0x200)` | `BattleStats_RecomputeDerivedStateAndAutoStatuses(target, flags)` |

### 2.7 The per-status terminal table

The jump table at `0030E8A4` (eight targets) is indexed by the byte table at `0030E8C4` (one per
status id, decoded from the image):

| status | case | what |
|---:|---|---|
| **0** (KO) | `0030E80A` | adding → `00300FC0(unit, 0)` and `BattleUnit_ProcessDefeatRewardsAndLoot(source, unit)` (`00312280`); removing → `BattleUnit_RecoverFromTerminalStatusSetIfClear` (`00301140`) |
| **1** (Stone) | `0030E850` | adding → event `0x200C`, then the same defeat cleanup and rewards; removing → recover |
| **31** (Vanished) | `0030E85E` | adding → event `0x200E`, then the same; removing → recover |
| **2** (Petrify, tier 6) | `0030E7DD` | unit `+0xE9A` bit 1 := `adding && source is a kind-0 record` (`0030E7E1`–`0030E801`) |
| **8** | `0030E7B3` | unit `+0xE9A` bit 0 := the same predicate (`0030E7B7`–`0030E7D4`) |
| **4** | `0030E75B` | event `0x2001`, add or remove |
| **5**, **27** | `0030E770` | `BattleUnit_ResetActionControlForStatusTransition(unit, flag)` with `flag = 0` when the unit has bit 24, or `+0x714 ≤ 0x21E` with `+0x6B4 ≥ 9`, or `+0x714 == 0x113` (`0030E770`–`0030E79F` — the field frame's reset loop uses the identical filter), then `BattleUnit_UpdateEngagementStateFlag` (`00307D10`) |
| all others | `0030E816` | ~~nothing~~ the shared tail: `0030FED0` runs unless `flags` bit 9 is set *(corrected 2026-10-02, OPUS: `0030E816`–`0030E828`; "Falsification pass 1" below)* |

The three terminal cases were already read by the field-record page §2d; the other four are new
here. Events go through `BattleUnit_DispatchActorPresentationEvent` (`003299B0`) with `r8d = 0`.

### What the defeat cleanup does

`00300FC0(unit, flag)` (371 B) is entered by the three terminal adds and by the party-side
shortcut (with `flag = 0`), and by `BattleUnit_TeardownAndDespawn` (`00300E59`, with `1`).

- **~~Party-type unit~~ Esper, `flag == 0`** (kind 0, type `0x1B..0x27`, the thirteen Esper rows, `00300FD3`–`00300FEF`):
  `BattleUnit_CancelAndResetCurrentAction` (`003105D0`) and a tail call `003138D0(0)` — nothing else.
- **Otherwise**: `BattleUnit_ReleaseTargetRelationAndActionState` (`00310780`); `002ED180(unit->d_08)`;
  unit `+4 &= ~4`; unit flags `&= 0xFFFFFFFDFFE7FFFD` — bits 1, 19, 20 and 33 cleared (`0030101E`–
  `00301034`); `0026DAC0(work, -1.0f)`; `Actor_SetMovementSpeed(work, 0)`;
  `BattleEnmity_PropagateToPerceivingFoes(type, 0, 0, 1)` (`0030105E`). Then **the party-state
  requests are raised immediately, not left to the field frame**: `002372E0()` → `02089340 \|= 0x400`,
  `003001D0()`, UI request `0x0B` and a tail call to `PartyControl_RecomputeSuppressionFromLeaderBattleState`
  (`0030106C`–`0030108F`); else `00237260()` → `\|= 0x200`, request `0x18` (`0030109D`–`003010C0`);
  else `002373C0()` → `\|= 0x800` (`003010CE`); and when the defeated unit is the party focus
  (`PartyFocus_GetCurrentPackedActorHandle_Thunk` = unit `+0x08`) → `\|= 0x100`, request `0x17`
  (`003010D8`–`003010F1`). With `flag == 0`, battle mode 1 and the unit being the registry's designated
  combatant (`02EBF190` record byte `+0x5AD5` → `BattleUnit_FindByCombatantId`): `003138D0(0)` and
  the party recompute (`003010F6`–`00301123`).

**So bits `0x100`, `0x200`, `0x400` and `0x800` of `02089340`** — three of which
[the capability policy](../../15-Input/Gameplay-Capability-Policy/capability-inhibition-policy.md)
§10 lists as unexplained — are the *defeat-condition latches*: set here on a defeat that leaves the
party without an eligible member (`0x400`, with the `0x0B` request), without a low-type member
(`0x200`, `0x18`), by `002373C0`'s condition (`0x800`), or that took the party focus (`0x100`,
`0x17`); [the field frame](../../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md)
§2.3 re-evaluates the same predicates every frame with the same request ids.

### 2.8 The status-layer function, for the applier's step 14

`BattleStats_ModifyStatusLayerStateAndProcessSideEffects` (`0030E130`, 553 B) is the sibling over
the two 128-bit layers at `+0x68` / `+0x78`, read in full by the two-layer page §11. Its mode
argument is `0` = clear `+0x68`, `1` = clear `+0x78`, `2` = set `+0x68`, `3` = set `+0x78`
(`0030E1EB`–`0030E24E`). So the applier's two bytes at `+0x3C`/`+0x3D` (mode 2) **add** to the
mutable layer and its four at `+0x3E`–`+0x41` (mode 0) **remove** from it — which closes `EZ-1`.

### 2.7a The defeat cleanup's unread steps, read (FA-3, 2026-09-12)

The four callees and two predicates §2.7 left unread, from their bodies:

| step | what it is |
|---|---|
| `002ED180(unitId)` | resolves the unit's actor registry entry (`003588B0`) and, when its render record (`+0xC0`) is live (index not −1, the `0x740`-stride entry's `+0x284` non-zero), tail-calls `003E6B40(renderRecord)` — the render side's defeat call, unread |
| `0026DAC0(work, −1.0)` | stores the float into the render record's `+0x148` and mirrors it into the record's `+0x138` link at `+8` (`0026DACC`–`0026DAFE`); with `Actor_SetMovementSpeed(work, 0)` next, this is the actor stopping where it fell |
| `003001D0()` | collects the active members (slots 0–3, `0031B810`) that are not down — no terminal status, or the `00377C20()` waiver — into a four-entry table at `022C1788` and calls `002ECEC0([member + 0x10])` on each (`003001F8`–`00300263`): **the survivors' pass**, run only before requests `0x0B` and `0x18` |
| `003138D0(flag)` | **dismisses the summoned Esper**: only in mode 1 ([the mode ladder](../../00-Engine-Core-Runtime/Battle-Runtime-Mode/battle-runtime-mode-ladder.md) §2c), it takes the slot-3 unit (`0031B8C0(3)`), and unless its current or remembered command (`+0x714`, or `+0xBA0` when flag bit 14 is set) is already `0x113` **Dismiss** ([the handler table](../../07-Combat-Action/Action-Dispatch/battle-action-handler-table.md)), issues `00311CF0(actor, combatantId, 0, 0x113, 0)` — then toggles `+0x5AD0` bit 0 by `flag` (`003138D8`–`00313981`) |
| `002372E0()` | **the whole roster is down**: every active slot 0–3 and reserve entry 0–8 holding a kind-0 unit of type ≤ 6 carries a terminal status (with the `00313F60` waiver) — request `0x0B`, the same predicate [the world tick](../../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md) §2.5 reads for battle-state bit 10 |
| `002373C0()` | **the leader is down during a summon**: `003135C0()` is `mode == 1` (`getsummonmode`), and `BattleUnit_FindByCombatantId(003137F0())` — the summoner recorded at `+0x5AD5` — carries a terminal status — ~~request `0x17`~~ latch `0x800` only (`003010CE`); request `0x17` belongs to the party-focus test, with `0x100` (`003010D8`–`003010F1`) *(corrected 2026-10-02, OPUS: checked at `003010C5`–`003010F1`; §2.7)* |

So the cleanup's tail reads as a whole: a fallen **Esper** (the party shortcut, kind 0 and type
`0x1B`–`0x27`) has its action cancelled and is dismissed; any other fallen unit is stopped and
released, the party-state requests go up (all down → `0x0B` with the survivors' pass; all active
non-guests down → `0x18` with the survivors' pass; the summoner down → the bit; the focus unit
down → `0x17`); and when `flag` is 0, the mode is 1 and the fallen unit is the summoner
(`BattleUnit_FindByCombatantId(+0x5AD5)`, `003010FA`–`0030111A`), **the Esper is dismissed and
party control recomputed** — the summoner's fall ends the summon.

## 3. Key addresses

| address | size | what |
|---|---:|---|
| `0030E360` | 1,323 B | `BattleStats_ChangeStatusAndProcessSideEffects` — 14 call sites in 10 functions |
| `0030E990` / `0030EAE0` | 35 / 38 B | `RemoveStatusMode0` / `AddStatusMode3` wrappers (field-record page §3) |
| `0030F690` | 196 B | `BattleStats_RemoveStatusesFromMaskAndRecompute` — a caller, ~~unread~~ *(answered: see §4 — it passes the flags literal `0x217` at `0030F721` and recomputes once itself; 2026-10-02, OPUS)* |
| `0030E130` | 553 B | the status-layer sibling; modes in 2.8 |
| `00387730` | 645 B | `BattleStatus_ComputeDefaultDwordParameter(unused, target, status)` — the default duration, §2.4a |
| `003876D0` | 88 B | `BattleStatus_ComputeDefaultShortTimer(status)` = definition `+9` × `[01DFE0B4]` × 30 — the beat timer, §2.4a |
| `00386C70` | 935 B | `BattleFormula_AdvanceStatusTimersAndBuildResult` — the tick's stage 2, the only consumer of both arrays, §2.4a |
| `0038FCE0` / `00387BB0` | 567 / 254 B | calculator slot 118 (the apply-mask writer) and `BattleFormula_AppendStatusAddOperation` — the other writers of the record's `+0x5C` / `+0xDC` slots, §2.4a |
| `00386A50` / `00386A70` | 32 / 103 B | the two transition-result builders (add / remove) |
| `003284D0` | 83 B | the status-applied reaction |
| `0046A800` | 106 B | the extra effect for statuses 1 and 31; reached only by `call rax` |
| `00300FC0` | 371 B | defeat cleanup |
| `00312280` | 857 B | `BattleUnit_ProcessDefeatRewardsAndLoot` |
| `00301140` | 452 B | `BattleUnit_RecoverFromTerminalStatusSetIfClear` |
| `00300140` / `00307D10` | 135 / 224 B | the reset and engagement calls for statuses 5 and 27 |
| `0020E600` | 10 B | `ImageAddress_ResolveRuntimePointer` — the registry relocation |
| `0030B9B0` / `0030B8E0` | 116 / 109 B | the two eligibility gates |
| `00377C20` | 78 B | `FieldData_GetActiveFieldRecordBit15` |
| `0030FED0` | 1,787 B | `BattleStats_RecomputeDerivedStateAndAutoStatuses` |
| `003112F0` | 2,040 B | `BattleFormula_ApplyTargetResult` |
| `003848E0` | 205 B | `BattleFormula_InitializeResultRecord` — both builders start here; decoded on the result-record page's *create* row (FA-5) |
| `00310780`, `003105D0`, `003219D0` | 225 / 418 / 296 B | defeat cleanup callees: release target relation, cancel the current action, propagate enmity |
| `002372E0`, `002373C0`, `003001D0`, `003138D0` | 188 / 88 / 174 / 195 B | the defeat-condition predicates and the two ~~unread~~ steps *(answered: see §2.7a; 2026-10-02, OPUS)* |

### Named callees and their entries

| name | entry |
|---|---|
| `BattlePresentation_EnqueueReactionWithRandomizedVariant` | `003BBD00` |
| `BattleSpecialSequence_CommitAccumulatedTargetHp` | `0030EB10` |
| `BattleStats_FindOwningBattleUnit` | `0031B860` |
| `BattleStats_ModifyHPAndProcessLethalState` | `00300530` |
| `BattleUnit_AdvanceStandardActionState` | `00304850` |
| `BattleUnit_DispatchActorPresentationEvent` | `003299B0` |
| `BattleUnit_ExecuteDirectStateCommandOrder` | `002FDDA0` |
| `BattleUnit_CancelAndResetCurrentAction` | `003105D0` |
| `BattleUnit_ReleaseTargetRelationAndActionState` | `00310780` |
| `BattleEnmity_PropagateToPerceivingFoes` | `003219D0` |
| `PartyFocus_GetCurrentPackedActorHandle_Thunk` | `003272E0` — a 5-byte thunk over `PartyFocus_GetCurrentPackedActorHandle` `003590D0` |
| `PartyControl_RecomputeSuppressionFromLeaderBattleState` | `0023B040` |
| `BattleUnit_FindByCombatantId` | `0031B770` |
| `Actor_SetMovementSpeed` | `0026A330` |

### Data

| address / offset | what |
|---|---|
| `02EBF118` | registry slot: the status definition table (`status_data.bin` by the field-record page); record stride at `+8`, records reached through the relocation; ~~`+9` = duration unit~~ `+9` = beat, `+8` = duration base (§2.4a) *(corrected 2026-10-02, OPUS: `003876D0` reads `+9`, `00387730` reads `+8`)*, `+0x0C` = the mask of statuses this one clears |
| `01DFE0B4` | the status timer scale (u32) |
| BKBI `+0x38`, `+0x3C`, `+0x64` | the three status words; presence = `+0x3C \| +0x64` |
| BKBI `+0xBC[32]` u32 | per-status parameter A, written on the `+0x64` modes |
| BKBI `+0x13C[32]` u16 | per-status timer word, written on the `+0x64` modes; default from the definition |
| unit `+0xE9A` | bit 0 (status 8) and bit 1 (status 2): "applied by a party-side source" markers |

## 4. Data structures and formulas

**Default timer**: `+0x13C[s] = status_data[s].byte9 × timerScale × 30` when the caller passes a
negative `paramB`; **default parameter**: `+0xBC[s] = 00387730(0, target, s)` when `paramA < 0`.

**Refusal**: `!bit0 && Low16 → refuse`; `adding && !bit0 && High16 && terminal → refuse`;
`adding && terminal && (+0x3C|+0x64) & 0x80000003 && !Bit15 → refuse`; the mode's own
already-in-state test → refuse; `mode > 5 → refuse`.

**The ~~party~~ Esper shortcut** *(corrected 2026-10-02, OPUS: §2.2)*: `adding && kind == 0 && 0x1B ≤ type ≤ 0x27 && terminal → 00300FC0(unit,0); return`.

**Side-effect gate**: `presentAfter != presentBefore`, over `+0x3C | +0x64`.

**Flag bits consumed here**: 0 (skip gates), 1 (skip the extra effect), 4 (skip the reaction),
9 (skip the final recompute; also set on every cascade call — and passed as the literal `0x217`
by `BattleStats_RemoveStatusesFromMaskAndRecompute`, `0030F721`, which recomputes once itself; no
other of the fourteen call sites sets it, 2026-09-12). The whole word is forwarded to
`BattleFormula_ApplyTargetResult` as its fifth argument at `0030E62F`.

## 5. Call chain

```
callers (14 sites): BattleStats_ModifyHPAndProcessLethalState (KO, modes 3 / 0),
  BattleFormula_ApplyTargetResult (+0x54 add / +0x58 remove loops),
  BattleUnit_AdvanceStandardActionState, BattleUnit_ExecuteDirectStateCommandOrder,
  BattleSpecialSequence_CommitAccumulatedTargetHp, BattleStats_RemoveStatusesFromMaskAndRecompute,
  BattleStats_RecomputeDerivedStateAndAutoStatuses, the two mode wrappers, and itself (the cascade)

ChangeStatus(target, source, s, A, B, flags, mode)
  -> gates ; party shortcut -> 00300FC0 ; terminal-on-terminal refusal
  -> mask write (six modes, already-in-state refuses)
  -> +0xBC[s] / +0x13C[s] on modes 0 / 3 (defaults from 00387730 / 003876D0 <- status_data +9)
  -> presence unchanged? return
  -> build result (00386A50 | 00386A70) -> ApplyTargetResult(&r, NULL, target, 0xFFFF, flags)
  -> adding: for each bit of status_data[s].+0x0C: ChangeStatus(..., i, 0, 0, flags|0x200, mode 0)
  -> adding: 003284D0 reaction ; 0046A800 extra effect (statuses 1, 31)
  -> terminal switch (2.7): defeat cleanup + rewards / recover / events / markers / reset
  -> RecomputeDerivedStateAndAutoStatuses unless flags bit 9
```

## 6. Modding notes

- **To add or remove a status natively, call `0030E360` with mode 3 or 0** and negative parameters
  to get the authored defaults; pass `flags | 0x200` to batch several changes and recompute once.
- **Re-applying a status the unit has is a no-op, and so is setting it in one word when the other
  holds it.** ~~A mod that needs a status "refreshed" must remove it first.~~ *(Scoped 2026-09-29, FABLE, Claude Opus 5.5, on
  AUDIT-SEM's fresh-reader note for PKG-GP-STATUS-POISON Q10: the no-op is this function's. One level up, the candidate
  resolver lets an already-present status through only when its `status_data` word `+6` has bit 5 (fourteen statuses),
  and the applier's copy-through step then installs its default duration and beat, so re-casting Haste restarts it; Poison's bit is clear, so re-casting Poison does nothing. The rule and the list:
  [`CONTRACT-status-write.md`](../CONTRACT-status-write.md) invariant 3; control
  `_index/candidates/pkg-gp-status-poison/refresh.py`.)*
- **The cascade is data**: `status_data.bin` record `+0x0C` is the mask of statuses cleared when
  this one is applied. Editing it changes what cures what without touching code.
- ~~**The duration unit is data too**: byte `+9`, scaled by `01DFE0B4` and `× 30`. A status with
  byte 9 = 0 gets timer 0.~~ **The beat is data too**: byte `+9`, scaled by `01DFE0B4` and `× 30` (`003876D0`); a status with byte 9 = 0 gets beat 0. The duration is byte `+8` (`00387730`, §2.4a) *(corrected 2026-10-02, OPUS: §2.4a, 2026-09-12)*.
- **KO, Stone and Vanished are the terminal three** — and for ~~party-type units~~ **summoned Espers** they bypass
  the masks entirely (defeat cleanup only), ~~which is why a party member's KO never posts rewards~~ so an Esper's KO
  never posts rewards. *Corrected 2026-09-26 (FABLE): party members take the full path (`row3.py` E1/E2).*
- **Statuses 5 and 27 reset the unit's action control** the way the field frame does every second
  frame; statuses 2 and 8 record whether a party-side source applied them.

## 7. What is not known

- [x] ~~**What `BattleStatus_ComputeDefaultDwordParameter` (`00387730`, 645 B) computes** for
  `+0xBC[s]` when the caller passes a negative parameter.~~ **ANSWERED 2026-09-12:** the default
  duration — `status_data +8`, scaled by the target's Vitality (shortened for the harmful class,
  lengthened for the beneficial one, ×1.5 with effect id 30), × frame base × 300; 11 for Petrify /
  Doom; 0 when `+8` is `0xFF` (§2.4a). `FA-1`.
- [x] ~~**Who reads `+0xBC[32]` and `+0x13C[32]`** on the BKBI record.~~ **ANSWERED 2026-09-12:**
  the periodic tick's stage 2, `00386C70`, through a record-relative address the typed census could
  not follow; plus the display record and its two lookalike readers for the Petrify / Doom count
  (§2.4a). `FA-2`.
- [x] ~~**What `0046AB10(target, 0x12 / 0x11, …)` does** for Stone and Vanished behind `002FA390`,
  and what the defeat cleanup's unread steps `002ED180`, `0026DAC0`, `003001D0`, `003138D0` and
  the predicates `002372E0` / `002373C0` are.~~ **ANSWERED 2026-09-12:** `0046AB10` is the battle
  event poster (the ledger's 2026-09-11 narrowing — events `0x12` / `0x11` are "turns to stone" /
  "is cast into the void"); the cleanup's steps are §2.7a — the render side's defeat call, the
  stop-where-fallen writes, the survivors' pass, the Esper dismiss, and the two party-down
  predicates. What `003E6B40` ~~and `002ECEC0` do~~ does on the render record ~~and the actor~~ is not read *(`002ECEC0` answered: see "Interior citation — frontier hub `002ECEC0`" below, 2026-09-18 — a context-to-render-record resolve that tails to `003AEEF0`; 2026-10-02, OPUS)*. `FA-3`.
- [x] ~~**The names of statuses 4, 5, 8 and 27**, the four with terminal cases of their own; and
  what unit `+0xE9A` bits 0–1 ("applied by a party-side source", statuses 8 and 2) are read by.~~
  **ANSWERED 2026-09-12:** Sleep, Confuse, Poison and Berserk ([the thirty-two statuses](../the-thirty-two-statuses.md)); the two bits are
  read once, by `BattleUnit_ProcessDefeatRewardsAndLoot` (`003122F4`–`0031232A`): a defeated
  kind-1 record posts rewards without a kind-0 killer when bits 0 and 2 are both set (party-applied
  Poison whose HP write fired the sound flag) or when it is Stoned (status bit 1) with bit 1 set
  (party-applied Petrify); bit 3 (taken, not struck) refuses rewards outright. `FA-4`.
- [x] ~~**What `BattleFormula_InitializeResultRecord` (`003848E0`) puts into a fresh record**~~
  **ANSWERED 2026-09-12** by cross-reference: the result-record page's *create* row had it —
  `memset(+8, 0, 0x140)`, `0xFFFF` at `+0x30` / `+0x11C`, `−1` in the sentinel words and in both
  33-entry status arrays, `+0x2C |= 1`. `FA-5`.

## 8. Evidence

| claim | evidence | tier | confidence |
|---|---|---|---|
| The entry decisions (`adding`, `initialises`, the two flag bits, `wasPresent`) | `0030E3BB`–`0030E41C` | 1 | PROVEN |
| The gates and the terminal-only second gate | `0030E424`–`0030E45A` | 1 | PROVEN |
| The party-side shortcut and its type range | `0030E467`–`0030E49C` | 1 | PROVEN |
| Terminal-on-terminal refusal unless Bit 15 | `0030E4A1`–`0030E4BD` | 1 | PROVEN |
| Six modes, already-in-state refusals | the definition-record page §2, re-read at `0030E4E7`–`0030E564` | 1 | PROVEN |
| `+0xBC[s]` / `+0x13C[s]` written on modes 0 / 3, defaults from `00387730` / `003876D0` | `0030E567`–`0030E5AF` | 1 | PROVEN |
| The default timer formula | `003876D6`–`0038771F` | 1 | PROVEN |
| Side effects only on a presence change over the OR of two words | `0030E5B7`–`0030E5CB` | 1 | PROVEN |
| The self-applied result, the cascade mask at `+0x0C`, the reaction, the extra effect | `0030E5D1`–`0030E727` | 1 | PROVEN |
| The per-status terminal table | `0030E8A4` / `0030E8C4` decoded from the image; cases `0030E75B`–`0030E889` | 1 | PROVEN |
| Statuses 0 / 1 / 31 are KO / Stone / Vanished; 2 is Petrify | the field-record page §2d (tier 1) and its cited enum (tier 6) | 1 / 6 | PROVEN / PROBABLE |
| `0030E130`'s four modes | the two-layer page §11; `0030E1EB`–`0030E24E` | 1 | PROVEN |
| 14 call sites in 10 functions; `0046A800` reached only by register | `check_caller_claims --addr`, control 632 | 1 | PROVEN |
| `00387730`: the default duration formula, its classes and the `×1.5` | `00387740`–`00387992` read whole; constants `008F3134` = 100.0, `00901B3C` = 1.5; `status_data.bin` rows `+6` / `+8` for all 32 ids (`repos-2d` VBF extract, byte-identical to the copy inside `battle_pack.bin` at `+0x1B178`) | 1 | PROVEN (static) |
| `00386C70` consumes both arrays through `record + (target − record + 0x60)` and writes them back through `+0x5C` / `+0xDC` | `00386C70`–`00387016` read whole; the applier's step 9 | 1 | PROVEN (static) |
| The Petrify / Doom count is displayed as `count − 1` | `00329500`–`00329539`, `0031FCA0`–`0031FCD8`, `00320D13`–`00320D3A` | 1 | PROVEN (static) |
| `+0xE9A` bits 0–1 read only by the defeat-rewards function | the battle-unit census (`0xE9A`: 7 writes in two functions, one read) and `003122F4`–`0031232A` | 1 | PROVEN (static) |
| The defeat cleanup's steps and predicates | `00300FC0`, `002ED180`, `0026DAC0`, `003001D0`, `003138D0`, `002372E0`, `002373C0`, `BattleUnit_FindByCombatantId` read whole; `003135C0` = `getsummonmode` (the mode ladder §2c); the `−1.0` at `01CEBC9C` | 1 | PROVEN (static) |
| What `0046AB10` posts | the ledger's 2026-09-11 narrowing (the event poster; the steal-roll page §2.5) | 1 | PROVEN |
| What the two builders do beyond the initialiser | ~~**not established**~~ the add builder clears `+0x2C` bit 0; the remove builder, for status 28 with HP non-zero, sets `0x108` and halves HP into `+0x24` (§2.6 row 1) — `00386A50`, `00386A70`, executed in CONTRACT-status-write.md §13 *(corrected 2026-10-02, OPUS: checked at `00386A70`; CONTRACT-status-write.md `SW-2`, answered 2026-09-12)* | ~~—~~ 1 | ~~UNKNOWN~~ PROVEN |

## 9. Related

- [`../../04-Actor-Entity/the-definition-record-flag-pair.md`](../../04-Actor-Entity/the-definition-record-flag-pair.md)
  — the three words and the six-mode table.
- [`../../03-World-Area-Field/Field-Record-Table/field-record-table-navimapdata.md`](../../03-World-Area-Field/Field-Record-Table/field-record-table-navimapdata.md)
  — KO / Stone / Vanished, `status_data.bin`, the three terminal cases.
- [`../Status-And-Augment-Layers/two-layer-effect-model.md`](../Status-And-Augment-Layers/two-layer-effect-model.md)
  — the status-layer sibling, read in full.
- [`../Periodic-Tick/what-the-periodic-tick-does.md`](../Periodic-Tick/what-the-periodic-tick-does.md)
  — the eligibility gates and the `+0x17C` timers this page distinguishes from `+0x13C`.
- [`../../07-Combat-Action/applying-a-result-to-a-target.md`](../../07-Combat-Action/applying-a-result-to-a-target.md)
  — the applier this function both serves and calls.
- [`../../08-Combat-Formula/Current-HP/the-hp-write-and-the-lethal-transition.md`](../../08-Combat-Formula/Current-HP/the-hp-write-and-the-lethal-transition.md)
  — the KO add and remove this function receives from the HP write.
- [`../../13-Rewards-Progression-Economy/what-happens-when-an-enemy-dies.md`](../../13-Rewards-Progression-Economy/what-happens-when-an-enemy-dies.md)
  — the reward path the terminal cases enter.

## Falsification pass 1 — 2026-09-12 (OPUS)

**passes: 1 · last_pass: 2026-09-12**

Nine claims re-derived from the shipping bytes. **All nine hold**, and two of them are now stated
more precisely than the page states them.

| claim | measured |
|---|---|
| thirty-three stated function sizes (§3) | **33 of 33 agree** |
| `0030E360` — **14 call sites in 10 functions** | **14 in 10** — and **zero tail jumps**, so the unit is settled rather than assumed |
| the jump table at `0030E8A4` has **eight** targets | **8 distinct targets**; the byte table at `0030E8C4` has max index **7**, one byte per status |
| the byte table's split | **8 statuses named, 24 on the default** — `0`→case 0, `1`→1, `2`→2, `4`→3, `5` and `27`→4, `8`→5, `31`→6, everything else→7 |
| the clear mask `0xFFFFFFFDFFE7FFFD` clears bits **1, 19, 20, 33** | **[1, 19, 20, 33]** |
| presence is `+0x3C` OR `+0x64` | `0030E5B7 mov eax,[rsi+0x3c]` / `0030E5BA or eax,[rsi+0x64]` |
| the case-4 filter (statuses 5, 27) | exact, **including the conjunction**: `bt rax,0x18`, **or** (`+0x714 ≤ 0x21E` **and** `+0x6B4 ≥ 9`), **or** `+0x714 == 0x113` |
| `0046A800` fires only for statuses **1 → `0x12`** and **31 → `0x11`** | `cmp di,1` → `0x12`; `cmp di,0x1f` → `0x11`; every other status returns |
| `003876D0` = definition `+9` × `[01DFE0B4]` × 30 | `movzx eax,[rcx+9]` · `imul eax,[01DFE0B4]` · `imul eax,eax,0x1e` |

### `0030E816` is the shared tail, and the two sections that name it should be read together

§2.6 row 7 gives `0030E816`–`0030E828` as **side effect #7, the recompute gate**. §2.7's last row
gives `0030E816` as what the **24 default statuses** do, and calls it *"nothing"*. Both are true of
the same address, and a reader reconciling them could conclude that the default statuses skip the
recompute. **They do not.** The address is the tail every case converges on, which the image shows
three different ways:

- **case 7 *is* `0030E816`** — the jump table's default entry points at the tail itself, not at a
  do-nothing body;
- **six cases reach it by `jmp`** (`0030E76B`, `0030E7B1`, `0030E7B5`, `0030E7DB`, `0030E7DF`,
  `0030E808`);
- **case 0 falls through into it** — `0030E811 call 00301140` is followed immediately by
  `0030E816`, with no jump between them.

So "nothing" is right about the *case body* and wrong about the *address*: **every status that
reaches the switch runs the recompute**, gated only on `flags & 0x200`. What genuinely skips it is
the **early-out** at `0030E5CB`, which jumps to `0030E82D` — past the gate, into the epilogue. That
makes §1's rule 3 literally true: adding a status a unit already has is a no-op **including derived
state**.

### The one negative claim, with controls — and the mechanism behind it

§3 says `0046A800` is *"reached only by `call rax`"*. The negative half was checked over **38,161
disassembled bodies**: **zero** direct call or jump sites. A negative over a population is worth
nothing without a control, so the same sweep counted four addresses that must be non-zero —
`00300140` **5**, `0030FED0` **25**, `003284D0` **1**, `0046AB10` **48**. The sweep can see callers;
this function has none.

The address is also spelled out **nowhere in the image** — one hit, in `.pdata`, which is its own
unwind entry, not a pointer to it. So the positive half needed its own evidence, and it is a single
instruction:

```asm
0030E704  cmp    dword ptr [rsp+0x60], 0      ; extraEffect
0030E709  je     0x30E729
0030E70B  movzx  edx, byte ptr [rsp+0x40]     ; status
0030E710  lea    rcx, [rip+0x15C0E9]          ; -> 0046A800   the real handler
0030E717  test   edi, edi                     ; adding?
0030E719  lea    rax, [rip-0x1A1080]          ; -> 0016D6A0   _guard_check_icall, C2 00 00
0030E720  cmovne rax, rcx
0030E724  mov    rcx, rsi                     ; target
0030E727  call   rax
```

**`0030E710` is the only instruction in the image that materialises `0046A800`**, and it lives
inside `0030E360` itself — which is why there is no call site and no stored pointer: a `lea` encodes
a displacement, not an address.

Two things follow that the prose should say out loud. First, **the call happens either way** — the
selection is a branchless `cmovne`, so "removing → the stub, i.e. nothing" is right about the effect
but not about the control flow; removing does not skip the call, it calls `ret 0`. Second, a
branchless two-way call **needs a *callable* no-op** — you cannot `cmov` a null and then call it —
and the compiler had one to hand.

> **Corrected later the same day (OPUS).** I wrote that this is "why a `ret 0` stub exists at all",
> and that `0016D6A0` serves "four unrelated subsystems because the linker folded their identical
> 3-byte bodies". **Both are wrong about the cause, and the number is off by three orders of
> magnitude.** `0016D6A0` is **`_guard_check_icall`, the Control Flow Guard check thunk** — named not
> by a symbol file but by the **PE Load Config directory itself**: `GuardCFCheckFunctionPointer` is
> the slot at `008C31C0`, and that slot holds `0016D6A0`. It is `ret 0` because this build is
> CF-*instrumented* (`GuardFlags = 0x100`) and ships with an **empty guard table** —
> `GuardCFFunctionTable = 0`, `GuardCFFunctionCount = 0` — so the check is a no-op **by
> construction**, not by folding.
>
> **Narrowed 2026-09-19 (FABLE): both causes are real, for different callers.** The body is the guard's default,
> as this note says - but a guard check reaches it *through the slot* `008C31C0`, and only one CRT thunk references
> that slot (eleven call sites, all CRT). The thousands of sites that call `0016D6A0` **directly** - including the
> `lea` above, which takes its address as a do-nothing callback - are not guard checks: they are empty functions the
> linker folded onto the same three bytes. Measured on
> [image hardening](../../24-Compiler-And-CRT-Runtime/Binary-Hardening-And-Hooking/image-hardening-cfg-aslr-dep-and-stack-cookies.md),
> section 9a.
>
> It has **2,868 direct call sites in 2,480 functions**: it stands in front of indirect calls across
> the whole image, not in four subsystems. What survives of my reading is the narrow part — its
> address is also *materialised* as a do-nothing function pointer, at **53 `lea` sites**, and
> `0030E719` is one of them.

### One value worth naming

`[01DFE0B4]` is an **integer, not a float** — the image initialises it to **1**.

> **Corrected later the same day (OPUS).** I first called it "a tuning slot currently set to unity",
> which is wrong in implication. It is the **frame base**, and it is not constant: across the whole
> image the word has **212 references and exactly one writer** — `001EDDF2 mov dword ptr [rip], 2`,
> inside `001EDDC0`, on that function's `ecx != 0` branch. So the beat timer is definition `+9` × 30
> at 30 fps and × 60 at 60 fps — **a constant wall-clock duration, not a constant tick count**, which
> is the conversion §2.4a already describes. One writer and 212 readers is the sharpest statement of
> what this word is: a single global set once and read everywhere.

*(Incidentally `0020E600` is called twice on the same `+0xC` at `003876E7` and `003876FB`, the first
result discarded.)*

**Not claimed:** nothing here was executed or observed live. The rewards call following
`0030E877 call 00300FC0` was not re-read. **Correction to this section, same day:** `FA-3` is
**answered**, not open — `0046AB10` is the battle event poster and `0x12` / `0x11` are the
"turns to stone" / "cast into the void" rows of `battle_message.bin`, decoded from the archive
on 2026-09-12. What remains open under that id is only `003E6B40` ~~/ `002ECEC0`~~ *(`002ECEC0` answered: see "Interior citation — frontier hub `002ECEC0`" below; 2026-10-02, OPUS)*, as §7 already
says. ~~`EY-1` remains open.~~ *(answered: status 28 is Bubble — see the thirty-two statuses §2, row 28; 2026-10-02, OPUS)*

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

- **Audio.**
  - `BattleFormula_ApplyTargetResult` (`003112F0`) plays its sound directly through the sound resolver and player.
  - `002C6F70`, a caller of the lookalike reader `0031FC70`, plays a sound through the gated wrapper.
    Interior read (2026-09-17, SWE2-FRONTIER): it first indexes the `0035D4F0` table by `r8d`
    ([`002C6FA1`](../../_index/ADDRESS-INDEX.md) → `[rax+r12*8]`), then walks the `[rbp+0x1D70]`
    linked list matching `[rbx+0x10]==edx`, and fans out to the `0028F5B0` ×4 / `002647D0` ×3 /
    `002EA040` ×2 helper set.
  - `PartyFocus_GetCurrentPackedActorHandle` is read by a 1,036-byte Audio-filed body that converts the focus actor's
    world position with `atan2f`, which reads as positional sound placement. That function is not read.
- **Items_Equipment_Shops_License.**
  - `003112F0` grants stolen items (`Inventory_ModifyEncodedItemAndUpdateDiscoveryState`).
  - The recompute `0030FED0` and the owner lookup `0031B860` are driven by the three equipment-slot setters and
    `BattleStats_SetLicenseNodeStateAndApplySideEffects`.
  - `BattleUnit_FindMappedDefinitionSelectorByIndex` (`0031B810`) and `FieldData_GetActiveFieldRecordBit15`
    (`00377C20`), the two helpers of `003001D0`, are also called by `Inventory_QueryOwnedCountIncludingReservedActionItems`.
  - `00377C20` is also called by `Equipment_UnequipEncodedItemFromActiveRoster`.
  - [The unit display record](../../04-Actor-Entity/Unit-Display-Record/the-record-00329220-builds.md)'s builder counts
    licence bits through `BattleStats_CountLicenseBits00To17`.
- **PlatformOnlineAchievements.** `BattleUnit_ProcessDefeatRewardsAndLoot` (`00312280`) fires achievement counters 11
  and 4, so a lethal status write reaches the counters
  ([the achievement catalogue](../../20-Platform-Online-Achievements/steam-integration-and-achievement-catalogue.md) AB-7).

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **CoreRuntimeScheduling — SERVICE and CLIENT.** Cited functions read `GameClock_GetRawTickCounter` (three times), and one is called by the 146-byte core start-up helper.
- **Gameplay — SERVICE and CLIENT, 31 edges.** The Gameplay-labelled neighbours are battle runtime bodies.
  - Cited status functions call `BattleUnit_DispatchActorPresentationEvent` (4), `BattleEncodedId_IsValidForClass` (4), `BattleRuntime_GetMode0To5FromFlagsAndFieldBit15` (3), `BattleTargetBuffer_FindActorWorkIndex` and `BattleAction_FindApproachGeometryAroundTarget`.
  - They are called by `BattleUnit_SubmitResultReactionMode` (2), `Battle_EmitReactionPresentationForSlot` (2), `BattleUnit_CollectMappedFourSlotUnitsByFlags` (2), `CombatantId_HasActiveBattleActionOrUnitFlag14` and a 552-byte body.
- **Input — CLIENT.** `InputGameplay_ArbitrateDigitalInputAndModalState` (twice) and a 1,936-byte Input body call cited status functions.
- **InputGameplay — CLIENT.** The single function labelled InputGameplay (289 bytes, inside the Input layer) calls a cited status function.

- **UI — MECHANICAL (SWE2-EC7-170, 74 edges).** `0028A090`'s emit helpers
  `00202C90`, `002B3400`, `00270550`, `003588B0`, `00203080` and `00271AB0` are
  shared by UI bodies (`002915C0`, `002C7660`, `0028AAA0`, `0027AD70`,
  +70 more) — the command-record constructor and the measure/transform
  primitives' fan-in, not a UI relationship to the status write. Edge list
  from `edges.tsv` 2026-09-22.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**CombatAI — CLIENT.** `BattleEnmity_WriteAllCombatantIds`, owned by that layer, calls `00313F60` on this page. That caller is the all-ids write over the same byte table, taking its value and its mode from the two arguments; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Movement — CLIENT (44 edges through 18 of this page's functions).** The Movement layer reaches this page at `003590D0`, `00377C20`, `00304850`, `00313F60` and 14 more. `FUN_0031bac0` is the worked example, read in full - it is a 668-byte steering computation in a `0x138`-byte frame with a stack cookie, working from the vector at `[+0]`/`[+8]` against the constants `0.6`, `0.8`, `1.0` and `-1.0`; **3 of the 33 bodies on that layer are read, the rest are counted**. The crossing is that those functions are consulted by that layer, not a shared responsibility. Edge count and subject list from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).

**Spawn_Encounter_Lifecycle — SERVICE.** `00300530` on this page calls `SpawnGroup_RecordMemberDeathAndHandleCompletion`, owned by that layer. What it reaches is the death record: `byte[+5] == 1` on the stats record, then `byte[+0xE98]` decides whether the group's completion path runs at all; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Presentation — SERVICE on twenty-two edges, CLIENT on seven (29 edges; seven neighbour bodies
read).** Twenty-two of the twenty-nine are the presentation layer reading four functions cited here,
and the shape is fan-in rather than four relationships. Twelve reach
`PartyFocus_GetCurrentPackedActorHandle`, **two instructions**, `mov eax, [022C7FE0] / ret`. Four
reach `FieldData_GetActiveFieldRecordBit15`, which bounds the field index against
`dword[02ADD100+4]` and returns bit 15 of the entry, answering **0 for an unknown field rather than
failing**. Two reach `00320CF0`, which accepts only indices 2 and 6 and returns
`dword[block + index*4 + 0xBC]`. Two reach `BattleUnit_FindMappedDefinitionSelectorByIndex`, from
`PartyCombat_UpdateStanceState` and `BattleUnit_BroadcastPartyCombatTargetRelation`. The last of the
twenty-two is `BattleUnit_ComputePartyBattleStance` calling `BattleUnit_UpdateEngagementStateFlag`,
then testing `dword[+0x64] | dword[+0x3C]` against the mask `0x8000020`.

Seven edges run the other way, and two of them state their own refusal conditions.
`BattleUnit_RecoverFromTerminalStatusSetIfClear` and `0031B8C0` reach
`BattleUnit_ComputePresentationSuppressionMask`, which reads `dword[unit]` and **returns early the
moment bit 4 is set**, and needs the `+0x698` block before it will look at bit 3.
`BattleUnit_ReleaseTargetRelationAndActionState` reaches
`BattleUnit_BroadcastPartyCombatTargetRelation`, which also requires `[unit+0x698]`.
`BattleUnit_ProcessDefeatRewardsAndLoot` reaches `Reward_PublishExpLpPresentation`. `003284D0`
reaches `BattlePresentation_EnqueueReactionWithRandomizedVariant`, which works the queue at
`[02B457D0]` against the byte at `02B443C0`, and that in turn reaches `00506700`. And `00470780` and
`00470B70` both reach `00428CD0`, which takes `word[rcx]` as an index, **short-circuits on `-1`**,
and otherwise strides `0x740` bytes per record.

So the crossing is four shared reads with a layer's worth of callers, plus seven ordinary calls out
to presentation. Edge count and subject list from `edges.tsv`. Read from the shipping bytes
2026-09-14 (OPUS).

**Script VM — CLIENT.** `00356160` on the script bridge calls `00203170`, one of the basis-compose helpers `003F1530` uses — the ribbon updater's transform work is reachable from script.

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page.*

**Combat — CLIENT (1 edge).** `003206E0`, a 176-byte body filed to that domain, calls the raw unit getter `ActorWork_GetBattleUnitRaw` `00263E30`. It is one more reader of the shared getter the status paths reach through `0031B8C0`; what it does with the unit is not read here.

**CombatFormula — CLIENT and SERVICE (97 edges).** The result sink `BattleFormula_ApplyTargetResult` `003112F0` calls the status write `BattleStats_ChangeStatusAndProcessSideEffects` `0030E360`, the layer function `BattleStats_ModifyStatusLayerStateAndProcessSideEffects` `0030E130` and the recompute `BattleStats_RecomputeDerivedStateAndAutoStatuses` `0030FED0`, and is called back by `0030E360` and `0030E130`; the status paths build their own results through `BattleFormula_BuildInactiveStatusTransitionResult` `00386A50`, `BattleFormula_BuildConditionalStatusHpTransitionResult` `00386A70` and `BattleFormula_BuildRandomElementStatusTransitionResult` `00386AE0`, which the result initialiser `BattleFormula_InitializeResultRecord` `003848E0` also serves for `BattleFormula_EvaluateTargetPreview` `00385680` and `BattleFormula_ResolveTargetResult` `00385F60`; the HP write `BattleStats_ModifyHPAndProcessLethalState` `00300530` is called by `BattleStats_SetCurrentHP` `00300520`, `BattleStats_ReconcileCurrentHpToEffectiveMaximum` `0030F340`, `003112F0` and `BattleSpecialSequence_CommitAccumulatedTargetHp` `0030EB10`; the status-add appender `BattleFormula_AppendStatusAddOperation` `00387BB0` calls the default status-parameter helpers `BattleStatus_ComputeDefaultShortTimer` `003876D0` and `BattleStatus_ComputeDefaultDwordParameter` `00387730`; the post-result dispatcher `BattleFormula_DispatchPostResultEvents` `00469EC0` calls the event poster `0046AB10`; the owner resolver `BattleStats_FindOwningBattleUnit` `0031B860` is called by 35 formula bodies such as `BattleFormula_BuildEvaluationContext` `003847C0`, `BattleFormula_RollAndStoreComboCount` `00388660` and `BattleFormula_SelectPoachRewardItem95_5` `00390680`; and the periodic tick `BattleUnit_RunPeriodicCombatMaintenance` `00310DB0` calls `00385F60`, `003112F0`, `BattleStats_ModifyPrimaryResource` `00300CE0`, `BattleStats_GetOwningActorHandle` `0031E800` and `BattleStats_GetByMappedBattleSlot` `00320AB0`. A result's status mask reaches this page through the sink's step that calls the status write, and a status change that moves HP or needs a result (the transition builders, and the KO arm) goes back through that layer's result records and sink, so the two layers call each other; the remaining edges are shared helpers: the owner resolver, the result initialiser, the effective-action-id resolvers `BattleRuntime_GetEffectiveActionId` `00387090` and `BattleRuntime_ResolveAndCacheEffectiveActionId` `00387A50` (called by `BattleUnit_AdvanceStandardActionState` `00304850`, and `00387090` also by the display builder `00329220`), and formula bodies that call this page's field predicate, id validator and presentation-event dispatcher.

**RNG_Random_Selection — SERVICE (1 edge).** `BattleFormula_AdvanceStatusTimersAndBuildResult` `00386C70` calls `RNG_MT19937_NextU32_Thunk` `00379CD0`. The status-timer advance takes its one draw from the shared MT19937 stream.

**Resource — OUT-OF-SCOPE (1 edge).** The menu draw `0028EAB0` (`display UI : menu`) calls `0024A5A0`, the lazily built child record the UI pair-record constructor also uses. This page cites `0028EAB0` only in the interior anchors of the EC7 notes for its message-record helpers; the resource edge is part of the menu draw, not of the status write.

**Rewards_Progression_Economy — SERVICE and CLIENT (25 edges).** The status write `0030E360` calls `BattleUnit_ProcessDefeatRewardsAndLoot` `00312280`, which calls `GameState_GetGil` `00253690`, `GameState_SetGil` `00254EE0`, `Reward_ComputeExperienceForRecipient` `002F8BB0`, the experience-threshold function `002F8F20`, `Reward_ComputeLicensePointsForRecipient` `002F90C0`, `BattleStats_AdvanceLevelToTargetAndRecomputeGrowth` `0030C650`, `EnemyChain_UpdateOnDefeat` `00317ED0`, `Loot_RollDropEntries` `003180F0`, `Loot_CreateWorldPickup` `00319CA0`, `00320AB0` and `FieldData_GetActiveFieldRecordBit15` `00377C20`; `003112F0` calls the gil pair and `0030C650`; `0030C650` and the level-set `0030C470` call `0030FED0`, and `0030C470` also calls `BattleStats_RemoveStatusesFromMaskAndRecompute` `0030F690`; `002F8BB0` calls `getsummonmode` `003135C0`, `BattleUnit_FindMappedDefinitionSelectorByIndex` `0031B810` and `0031B860`; the tick `00310DB0` calls `Loot_FindOverlappingPickupIndex` `002FB150`, `Loot_RemoveWorldPickupByIndexWithoutGrant` `00319830` and `Loot_CollectWorldPickupByIndex` `00319A00`; and the display-record builder `00329220` calls `002F8F20`. A KO written through this page's terminal table is what starts the defeat rewards (experience, licence points, gil, chain, drops), and a level change runs this page's status strip and recompute in return.

**Story_Event_Quest_Hunt — OUT-OF-SCOPE (1 edge).** `InputGameplay_ArbitrateDigitalInputAndModalState` `00253C70` calls `PersistentFlag_QueryPrimaryOrAuthoredThresholdGate` `0032A8A0`. This page names `00253C70` only as a caller of the five-gate readiness test `00267720` in the EC7-104 note; the story-flag query is the input arbiter's own business.

### Interior citation — frontier hub `002ECEC0` (2026-09-18, SWE2-EC7)

`002ECEC0` — 73 B, 5 callers. The same context-to-render-record resolve idiom as
`002E73C0` — `[rcx+0xC0]` null-gate, `dword[rax] == -1` / `word[rax] == -1`
sentinels, `imul rcx, rax, 0x740` into the render-record array — but gated on
`[+0x284] != 0` and offset by `+0x550` before the tail
[`002ECF03`](../../_index/ADDRESS-INDEX.md) to `003AEEF0`. The sibling accessor
the status write consults on the occupied-record arm.

### Interior citation — frontier hub `0031B8C0` (2026-09-18, SWE2-EC7)

`0031B8C0` — 31 B, 6 callers: the guard-and-forward — `00263750()` at
[`0031B8C4`](../../_index/ADDRESS-INDEX.md); null returns silently, non-null
tails `00263E30(rax)`. The shared resolve-then-dispatch stub the status paths
call through.
## SWE2-EC7-30 update (2026-09-18) — `0028F5B0` override-or-flag read

`0028F5B0` (53 B) is the value read the status fan-out calls x4: when
the `0209BE80` bank's `+0x10EF0` override record is set it answers
`dword[rec+0xD2C]`; otherwise it reads `word[+0x7EC8]` and returns
`dword[+0x7EC4]` only when bit 0 is set and bit 1 is clear — every
other arrangement returns 0. An override-first, flag-second reader
on the bank's `+0x7ECx` state. Interior anchor `0028F5C3` (the
`+0x7EC8` word test).

## SWE2-EC7-61 update (2026-09-19) - `002EA040`

`002EA040` (152 B) is a status-write helper - `003588B0`/`00426770`/`00808C40` plus `01F44830`/`022C6F28`. Interior anchor `002EA058` (a `003588B0` call).


## SWE2-EC7-95 update (2026-09-20) - `00321850` measured

`00321850` (381 B) is the clamped byte-table write `003216E0`,
`003219D0` and `00321D30` drive: `+0x6A0` supplies the `+0x19`
base, `+0x698`'s `+0x64 | +0x3C` is tested against `0x80000003`
with a `00313F60` re-check, and `byte[+5] == 1` must hold. The
`00322C50(2, index, 1)` predicate gates each step; the head path
reads `[r14+rbp+1]`, applies the `r15`-armed `ebx` add with
sign/floor clamps, falls back through `00321770` to `+0xA`, and
`00321E40` publishes. The tail loop walks 0x28 entries calling
`00322C50` again, then clamps each byte to 0..0xFF in place.
Interior anchor `003218F9` (the first `00322C50` call).

## SWE2-EC7-96 update (2026-09-20) - `00321E40` + `0030BC40` + `00307CE0` measured

`00321E40` (83 B) is the single-entry writer `00321850` and
`00321B00` call: `00322C50(2, edx, 1)` gates the write, then `ebx`
is clamped 0..0xFF and lands at `[rdi + rsi + 1]` - the primitive
the clamped-table pass calls per index.
Interior anchor `00321E64` (the `00322C50` call).

`0030BC40` (109 B) is the one-shot apply `00304850` and `00309990`
run: `+0x690` bit 2 already set skips; otherwise `byte[+0x695] <=
0x1F` indexes a `0x30`-stride row in `02CD1784` for its `+0x24`
dword (-1 fallback), `00322310` must accept it, `002EB4A0` runs on
`[rbx+0x10]`, `+0x690 |= 4` marks it done, and the return is
`(flags & 5) == 5`.
Interior anchor `0030BC7D` (the `00322310` call).

`00307CE0` (47 B) is the two-check gate `00307D10` and `00321530`
call: `0030C210(rcx)` or `0030BB30(rcx)` returning nonzero yields
1, anything else falls through void - the either-of-two predicate
the callers branch on.
Interior anchor `00307CF5` (the `0030BB30` call).

## SWE2-EC7-97 update (2026-09-20) - `002EB4A0` + `00322310` + `002E8100` measured

`002EB4A0` (76 B) is the canonical `0x740`-stride resolve-and-
dispatch this page's `0030BC40` (and `003057D0`, `00325260`) call:
`rcx` and its `[+0xC0]` block must be non-null, `dword[block] !=
-1`, `word[block] != -1`, then `rcx = signextend(word) * 0x740 +
[022C6F28]` must be non-null with `dword[+0x284] != 0` - only then
does it tail `004278D0`. Every early-out falls to `ret`.
Interior anchor `002EB4DA` (the `004278D0` dispatch test).

`00322310` (49 B) is the two-shape acceptor `0030BC40` calls on
the `+0x24` dword: `ecx + 1 <= 1` (ids 0 and -1) returns 1
inline; anything else returns `0024DE70() == 0` - the
sentinel-passes-free / else-validated gate the apply path uses.
Interior anchor `00322320` (the `0024DE70` call).

`002E8100` (98 B) is the resolve-through variant `0023B040` and
`00310DB0` call: `003588B0(rcx)` first, then the same
`[+0xC0]`/word/`0x740`/`+0x284` chain, and a live record tails
`0041FCA0` - `-1` on a null resolver, `0` on a dead record.
Interior anchor `002E815D` (the `0041FCA0` tail jmp).

## SWE2-EC7-103 update (2026-09-20) - `002736B0` measured

`002736B0` (87 B) is the capability chain
`002C64C0` and `002C6F70` call: `002647D0()`
nonzero feeds `0025B4C0` into `ebx`; a zero falls
to `0028FA00()` and then `00273950()`; the answer
is `00267720()` nonzero and `ebx` nonzero and
`002E0FA0()` bit 4 clear - the three-source
enable the status-write arms consult.
Interior anchor `002736EB` (the `002E0FA0`
call).

## SWE2-EC7-104 update (2026-09-20) - `00267720` measured

`00267720` (131 B) is the predicate chain
`00253C70` and `002736B0` call: it fails fast
when `byte[0209A2AA]` is clear, then resolves
`003590D0()` (a count) and `003588B0()` (the
bound record) - a zero count returns 0. With
the record live it requires `002373A0(rec)`,
`00233D70(rec)`, `002E05C0() == 0` and
`00265680() != 0` in that order, and finally
answers `dword[02099DB4] == 0` - the
five-gate readiness test the write arms
consult.
Interior anchor `00267737` (the `003590D0`
call).

## SWE2-EC7-107 update (2026-09-20) - `002373A0` measured

`002373A0` (32 B) is the bit-4
probe `00267720`, `0026DFB0` and
`003509E0` call on the same
`0031B760()` record - null answers
0, live answers `(dword[rax] >> 4)
& 1` - the sibling flag fetch to
`00237650`'s bit-2 read.
Interior anchor `002373B5` (the
`shr eax, 4`).

`002C8A60` (350 B) is the slot allocator `002C6F70` calls: two entries at `rcx + 0x19B0` stride `0x1C0`, `byte[r9 + 4] & 1` free slots remember `r10 + 0x1800 + i*0x1C0`, a `[r9] == [rdx + 0x10]` match exits early; no free slot falls back to `word[r10 + 0x1D7A] >> 7 & 1` picking the side - the status write's slot pick.

Interior anchor `002C8B4D` (function `002C8A60`).

`003BBB60` (288 B) is the ring sweep `00252A70` calls: `02B457D0` null or (`01EFE31D & 2` clear with `01EFE320 <= 0`) exits; `003F1520` opens the `rsp+0x20` block, then 64 slots walk the `02B443C0` byte-indexed ring into `02B457D0`'s 0x50-stride records - `byte[+0x3C] == 2` collects through `0028A090` into `rsp+0x80` at 0x130 stride (count in `edi`), the rest take `00505560` with the `01EFE320` float; `003F1530` and `0028EE10` close - the status pass that gathers the live `+0x3C==2` records into the scratch page.

Interior anchor `003BBC37` (function `003BBB60`).

`0028A090` (704 B) is the billboard emit `003BBB60`'s sweep collects into the 0x130-stride scratch page: `word[rcx+0x38] >= 0x100` caps the ring; the float scale x `008F3A2C` truncates into `edi`; `003588B0([rcx+8])` resolves the source record for `002EA0E0`'s vec4 (missing records copy `[+0x20..+0x2B]` back with w = 1.0f), `00203080` transforms through the `02AED5F0` constant block and `00270550` measures the result - zero exits 0; a width past `30.0f` rescales `edi` by `1 - (w - 30)` clamped at 0, and the alpha ramp `6.2832 / w + 0.15` clamps into `[0.8, 0.9]`; `00271AB0(&rsp+0x30, 7, 00915E40, word[+0x38])` gives the centred offset pair before `002B3400([+0x30], rsi, 0)`; `rsi` then takes `+0x9F = byte[+0x3D]`, `+0x34 = ramp`, RGBA `+0x30..+0x32 = byte[+0xC..0xE] x ecx >> 7` capped `0xFF` with `+0x33` modulated a second time by `edi`, `+0xF0/+0xF2 = (centre - half extent + +0x14/+0x18) x ramp` and `+0xF4/+0xF6 = word[+0x40]/+0x42`; `00202C90` constructs `+0xD0`, `+0xE0/+0xE8/+0xF8/+0x100/+0x120` clear, and `003F14D0(rbp, rsi)` publishes - the per-status floating label the write pass stamps.

Interior anchor `0028A164` (function `0028A090`).

`0028A090` (704 B) is the billboard emit `003BBB60`'s sweep collects into the 0x130-stride scratch page: `word[rcx+0x38] >= 0x100` caps the ring; the float scale x `008F3A2C` truncates into `edi`; `003588B0([rcx+8])` resolves the source record for `002EA0E0`'s vec4 (missing records copy `[+0x20..+0x2B]` back with w = 1.0f), `00203080` transforms through the `02AED5F0` constant block and `00270550` measures the result - zero exits 0; a width past `30.0f` rescales `edi` by `1 - (w - 30)` clamped at 0, and the alpha ramp `6.2832 / w + 0.15` clamps into `[0.8, 0.9]`; `00271AB0(&rsp+0x30, 7, 00915E40, word[+0x38])` gives the centred offset pair before `002B3400([+0x30], rsi, 0)`; `rsi` then takes `+0x9F = byte[+0x3D]`, `+0x34 = ramp`, RGBA `+0x30..+0x32 = byte[+0xC..0xE] x ecx >> 7` capped `0xFF` with `+0x33` modulated a second time by `edi`, `+0xF0/+0xF2 = (centre - half extent + +0x14/+0x18) x ramp` and `+0xF4/+0xF6 = word[+0x40]/+0x42`; `00202C90` constructs `+0xD0`, `+0xE0/+0xE8/+0xF8/+0x100/+0x120` clear, and `003F14D0(rbp, rsi)` publishes - the per-status floating label the write pass stamps.

Interior anchor `0028A164` (function `0028A090`).

`003F1530` (1027 B) is the per-frame ribbon/trail updater: it builds the two basis transforms (`008626C0` init, `00203170` + `00202D70` compose over the `009152xx`/`009003xx` constants and the `00183280` divides), then walks the `[+0x40]`-chained particle list - `+0xEC` bit0 gates the `002720F0` distance write into `+0x120`, `0024ABC0`/`0024ABA0` noise scales `+0xE0`/`+0xE4`, `00249EE0` screen-tests the `+0xF0..+0xF6` quad and `003F1940` emits the node - followed by the `+0x108`/`+0x110`/`+0x118` sibling/parent depth walk under the `002B4710`/`002B4700` braces - the visual-effect frame the status-write and per-frame callers share.

Interior anchor `003F16E0` (function `003F1530`).

`0030BB30` (257 B) is the entry-kind probe `00307CE0` runs: the `[rcx+0x714]` word must not exceed `0x21E`, `0031B7E0` resolves `[rcx+0x710]` into the bank record and `0030AB40` must return `<= 1`; the `02EBF138` bank then indexes `di * word[+8] + offset`, and the answer is 1 when `byte[+0x1C]-1` tops 7 else `([rbx+0x2C] >> 0xE) & 1` - a bit out of the bank row's flags word

Interior anchor `0030BB5B` (function `0030BB30`).

`0028EE10` (228 B) is the formatted post `003BBB60` runs into the `0209BE80 + 0x5380` object: under an `0x80B8` stack frame it builds a `rsp+0x30` record through `00271450` + `0016D6A0` + `00271010(1)` twice plus `00271720`, formats into `rsp+0x70`/`rsp+0x90` (`0x80` buffer) via `003F12D0`/`003F1220`, sets `+0x88` bit `0`, submits through `00289A10` with the caller's `xmm0` in `xmm3`, and runs the `003F0170` teardown

Interior anchor `0028EEA9` (function `0028EE10`).

`003F12D0` (9 B) is the record clear `0028EAB0` and `0028EE10` run before formatting: `qword [rcx] = 0`, `dword [rcx+0x18] = 0` - two fields and out, the `0x20`-byte message record's constructor

Interior anchor `003F12D5` (function `003F12D0`).

`003F1220` (14 B) is the two-field store `0028EAB0` and `0028EE10` run after the `003F12D0` clear: `qword [rcx] = rdx`, `dword [rcx+0x18] = r8d` (the `+8` qword write of `rdx` is immediately rewritten - the live stores are the pointer at `+0` and the dword at `+0x18`)

Interior anchor `003F1226` (function `003F1220`).

`00271720` (64 B) is the record-tag fixup `0028EAB0` and `0028EE10` run between `00271010` calls: it writes `0x03000000`/`0x02000200` into `[rcx+0x10]`'s `+8`/`+0xC`, runs `0016D6A0` on the stack-held pointer, and stores the possibly-moved record back into `+0x10`

Interior anchor `00271745` (function `00271720`).

## Homed frontier bodies called from this page's functions (FABLE, 2026-10-02, cloud-drafted)

*Functions no page cited until now. Each is entered directly from a function this page already cites (the site is given as caller + offset). Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's homing pack and re-read by FABLE against the certified image; verified by [`homing_applier.py`](../../_index/candidates/fable-home-the-status-write-and-its-side-effects-1002/homing_applier.py): every site transfers to its function, the page cites the caller, and every anchor is an instruction boundary inside its function that decodes to the recorded mnemonic.*

| function | size | entered from | what the body does | interior anchors |
|---|---|---|---|---|
| `002C7620` | 60 B | `002C6F70` + 0x126 | unlinks node `rdx` from a doubly linked list (qword `+0x18` and qword `+0x20` links): when its `+0x20` neighbour is non-null that neighbour's qword `+0x18` takes `rdx`'s `+0x18`, when its `+0x18` neighbour is non-null that neighbour's qword `+0x20` takes `rdx`'s `+0x20`, and both of `rdx`'s links are zeroed; it returns `rcx`, or `rcx`'s qword `+0x18` (read before the unlink) when `rdx` equals `rcx` | Interior anchor `002C7628`; Interior anchor `002C7639`; Interior anchor `002C764A`; Interior anchor `002C7650`; Interior anchor `002C7654` |
| `002EA1E0` | 79 B | `002C6F70` + 0xD2 | returns 1 when `rcx` is null, its qword `+0xC0` is null, or the dword at that pointer is -1; otherwise takes the word at that pointer, returns 0 when it is -1, when the `0x740`-stride record it indexes from qword `022C6F28` has a zero address, or when that record's dword `+0x284` is zero, and else returns 1 when bit 3 (`0x8`) of that dword is clear and 0 when it is set | Interior anchor `002EA1F1`; Interior anchor `002EA1F9`; Interior anchor `002EA216`; Interior anchor `002EA225`; Interior anchor `002EA229` |
| `0035D570` | 45 B | `002C6F70` + 0xF1 | scans the dword `022C83F0` (signed count) dwords starting at `022C83F8` and returns 1 when one of them equals `ecx`, otherwise 0 (also 0 when the count is zero or less) | Interior anchor `0035D57C`; Interior anchor `0035D585`; Interior anchor `0035D58F`; Interior anchor `0035D594`; Interior anchor `0035D597` |
| `003F19D0` | 131 B | `003F0170` + 0xB1 | zeroes qwords `+0xB0`, `+0xB8` and `+0xC0` of node `rdx` on every path, then returns `rdx` when `rcx` is null; otherwise descends a binary tree from `rcx`, taking qword `+0xB8` when the current node's float `+0xC8` is greater than `rdx`'s float `+0xC8` and qword `+0xB0` otherwise (equal or unordered included), stores `rdx` into the first null child slot, stores that parent into `rdx`'s qword `+0xC0`, and returns `rcx` | Interior anchor `003F19D5`; Interior anchor `003F1A08`; Interior anchor `003F1A2F`; Interior anchor `003F1A41`; Interior anchor `003F1A48` |
