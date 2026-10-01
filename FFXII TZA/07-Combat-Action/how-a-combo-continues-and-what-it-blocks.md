---
system: How a combo continues, and what it blocks
category: 07-Combat-Action
status: DOCUMENTED — GR-3 is ANSWERED and the combo label is read (the localised "Hits" cell of battle_4_c) (owner re-status 2026-09-30, OPUS, on SWE2-STRUCT's DD batch 11) — what the battle HUD's per-frame walk draws for a combo-count entry was GR-3, since answered (the HUD routine itself only records the entry, §8 UQ-115); unit flag bit 22 read 2026-09-30 (§2.5 test 3, an engage auto-attack in progress), the +0x6B4 note reconciled with UQ-118 (§4.2), the 0023B146 comparison read (§8), upstream callers added (§5); status brought up to date 2026-09-30 (FABLE)
owner_layer: PrimaryOwner:CombatAction
evidence_tier: 1
verified_against:
  gzf_sha256: fb9b5e7ea002c1626a53d47da0b0b69a2443e246f7ce2b64329be4e034a2d3f7
  snapshot_sha256: a9cead8777597cdca58f2a47f27153f5231d60ad2bc16c3da9df8253820b09bd
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity - every function this document cites has byte-identical per-function records in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: 16 cited function entries, 0 of them among the 128 records that changed across GN158..GN161 (check_delta_additivity.py, check_transfer_eligible.py); re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS-REQ-FABLE-PROVENANCE-TRANSFER-144 (9bedb5e0); re-targeted GN160 -> GN161 under EVIDENCE-STANDARD addendum 2026-09-14bh
    previously: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708 (GN160), superseded 2026-09-14
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  parent_tag: GN159
last_reviewed: 2026-09-30
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-combo-continue-pass-1
  crossref_clean: false
  reopened_count: 0
---

# How a combo continues, and what it blocks

`unit + 0x6B7` is one byte with **seven instructions touching it across six functions**, and until
this read no document named it. [`../08-Combat-Formula/combos-and-the-guard-parry-flag.md`](../08-Combat-Formula/combos-and-the-guard-parry-flag.md)
found the byte from the formula side, recorded that a non-zero value suppresses the combo roll
entirely, and listed **"who writes `+0x6B7`" as unestablished**. This document answers that, and the
answer changes what the byte means — see 6.

**Extents checked**: `0030FA00` 146 B, complete, ends `ret` at `0030FA91`; `0031B860` 83 B,
complete; sites in `00236A60`, `003105D0`, `00325D90`, `0023B040`, `00385680`, `00388660` read in
context.

## 1. What the player sees

A physical attack that combos does not decide its length once and play an animation. **It commits the
same action again, hit after hit**, and each commit asks whether there is another hit due. The number
of hits was decided on the **first** hit and stored; every hit after that only asks *have I done
enough yet?*

Two things a player can feel, both from the same byte:

- **You cannot move while your combo is running.** A non-zero counter is an unconditional early
  `return 0` in `BattleUnit_CanAdvanceCombatNavigation`.
- **A combo in progress overrides the party-control suppression state** computed for the leader,
  wholesale, rather than contributing one more flag to it.

## 2. Native mechanism

### 2.1 The counter, and the pair it belongs to

`+0x6B7` and `+0x6B8` are **one two-byte pair**, and the clearest proof is the reset, which writes
both with a single store:

```asm
00310649  xor   ebp, ebp
...
003106EB  mov   word ptr [rbx + 0x6b7], bp     ; clears +0x6B7 AND +0x6B8
003106F2  mov   byte ptr [rbx + 0x6b4], bpl
```

> **A `word` store at `+0x6B7` is not evidence that `+0x6B7` is two bytes wide.** It bounds the bytes
> touched, not the field. Every other access in the image reads or writes `+0x6B7` as a **byte**
> (`0030FA0F`, `0030FA79`, `0023B124`, `00325DDF`, `003857C6`, `0038868A`), so the pair is two
> one-byte fields cleared together, not one `u16`.

`BattleUnit_ResetStateForReuse` (`00236A60`) does not touch `+0x6B7` itself — it reaches it by
calling `003105D0` at `00236A77` with arg 1 unchanged.

### 2.2 The only writer that changes it is the continue path

`BattleAction_TryContinueComboSequence` (`0030FA00`) is 146 bytes and does one thing:

```asm
0030FA0F  movzx edi, byte ptr [rcx + 0x6b7]   ; the counter
0030FA19  movzx esi, byte ptr [rcx + 0x6b8]   ; its partner, saved
0030FA20  call  0x30c010                      ; may this action continue?
0030FA27  jne   0x30fa3b                      ; yes -> re-commit below; a zero answer falls through to return 0
                                              ; (comment corrected 2026-09-12: it said "no -> return 0" on the taken branch)
0030FA3B  mov   r9d, dword ptr [rbx + 0x710]  ; \
0030FA45  movzx r8d, word  ptr [rbx + 0x714]  ;  | the SAME action, again
0030FA4D  mov   rdx, qword ptr [rbx + 0x708]  ; /
0030FA5C  call  0x30f760                      ; BattleUnit_CommitAction
0030FA63  je    0x30fa29                      ; commit failed -> return 0
0030FA65  mov   byte ptr [rbx + 0x6b8], sil   ; restore the partner
0030FA6C  inc   dil
0030FA79  mov   byte ptr [rbx + 0x6b7], dil   ; counter + 1
0030FA80  mov   byte ptr [rbx + 0x6b4], 5
```

**It re-commits the identical action** — same context `+0x708`, same action id `+0x714`, same target
focus `+0x710` — and **only on success does the counter advance**. The write to `+0x6B8` stores back
the value read before the two calls, so its effect is to preserve it across them.

### 2.3 The roll happens once per combo, not once per hit

`BattleFormula_RollAndStoreComboCount` (`00388660`) reads the counter off the **owning unit** and
branches on it:

```asm
00388679  call  0x31b860                      ; stats -> owning BattleUnit
0038868A  movzx ebx, byte ptr [rax + 0x6b7]   ; the counter (0 if no owner)
003886F5  test  ebx, ebx
003886F7  jne   0x38886b                      ; already combo-ing -> NO ROLL
```

- **Counter is 0 (the first hit):** roll, and store the result in the **high nibble of
  `record + 0x12`** — `0038885D and byte [rdi+0x12], 0xf` / `00388865 or byte [rdi+0x12], r14b`.
- **Counter is non-zero (every later hit):** no roll at all —

```asm
0038886B  movzx eax, byte ptr [rdi + 0x12]
0038886F  shr   eax, 4                        ; the count decided on hit 1
00388872  cmp   ebx, eax                      ; progress vs. that count
00388874  jae   0x38887e                      ; done enough -> combo ends
0038887A  or    dword ptr [rax + 0x18], 2     ; otherwise: another hit
```

**So the stored nibble is the memoised result of the first hit's roll, and the counter is progress
against it.** The two are different objects: `rdi` is the 64-byte record (`0208D480 + kind * 0x40`),
`rax` is the BattleUnit. That distinction is the whole of section 6.

### 2.4 The base pointer is a BattleUnit in all six, and two of them prove it

Four functions take the unit as arg 1 and touch known unit fields alongside `+0x6B7`
(`+0x698`, `+0x708`, `+0x714`, `+0x6B4`). The other two receive it from a getter, and one of those
getters **establishes the identity by construction**:

```asm
0031B860  BattleStats_FindOwningBattleUnit(stats)
0031B87D  call  0x236850                      ; BattleUnit_GetSlotCount
0031B888  call  0x236820                      ; BattleUnit_GetBySlotIndex
0031B892  cmp   qword ptr [rax + 0x698], rdi  ; whose +0x698 is this stats object?
0031B899  je    found
```

**It walks the battle-unit slot pool and returns the unit whose `+0x698` equals the argument.** The
return value is a BattleUnit because it came out of `BattleUnit_GetBySlotIndex` — not because of its
name. **And it identifies `+0x698` as the unit's stats pointer**, which is the same field the gambit
cascade reads.

`0023B040` gets its pointer from `BattleUnit_GetPartyLeader` (`003272A0`) at `0023B089`.

### 2.5 The gate — `0030C010` answers *may the combo continue* (2026-09-12)

Read whole (179 B); the same reading is on [force fight mode](../00-Engine-Core-Runtime/Force-Fight-Mode/force-fight-mode.md) §`AN-4`. It returns 1 only when
**all** of these hold, in this order:

| # | test | instructions | meaning |
|---:|---|---|---|
| 1 | the unit's status has Confuse or Berserk (`0x08000020`), **or** `00253B90()` is false | `0030C016`–`0030C035` | outside those two statuses the party must not be **fleeing** — force fight on ([the R2 toggle's](../00-Engine-Core-Runtime/Force-Fight-Mode/force-fight-mode.md) `FLEEING` state stops combos) |
| 2 | the target buffer's first entry exists (`+0x780` non-null) and its outcome word has **bit 10** | `0030C03B`–`0030C04F` | *the combo continues* — the resolved result's flag, [the field map](../04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md) `+0x788` |
| 3 | unit flag bit 22 clear | `0030C051`–`0030C058` | bit 22 is set by `BattleUnit_TryCommitEngageAutoAttack` (`003130D2`); ~~its meaning is not read~~ *read 2026-09-30 (FABLE), below the table:* **an engage auto-attack is in progress**, so no combo continues out of one |
| 4 | the focus target `+0x710` resolves to a unit with a stats record, and that record has none of KO, Stone, X-Zone — unless the field's bit 15 permits | `0030C05A`–`0030C08A` | no combo onto a downed, petrified or vanished target |
| 5 | if battle-state bit 0 is set, the unit's handle `+8` equals `0208E6A4` | `0030C08C`–`0030C09F` | while a one-shot combat callback is armed — a special sequence's owner ([the world tick](../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md) §2.5 bit 0) — only that unit may chain |
| 6 | the special-sequence state `022C2160` is 0 or 7 | `0030C0A1`–`0030C0AE` | no summon, Quickening or mount presentation in progress ([the mode ladder](../00-Engine-Core-Runtime/Battle-Runtime-Mode/battle-runtime-mode-ladder.md) §2d) |

Its only other caller, `0031ADB0` (reached through `0031B4B0`, for which no static reference was found by
`E8` / `E9`, `lea`, qword or RVA — only its `.pdata` entry), publishes the answer as bit 1 of its output record's
`+0x3C` when asked with flag `0x10` (`0031B0C4`–`0031B0DB`).

**Test 3 — what unit flag bit 22 marks (read 2026-09-30, FABLE).** Bit 22 is the "engage auto-attack in progress" flag.
It is raised and lowered around one action:
- **Raised.** `BattleUnit_TryCommitEngageAutoAttack` (`00312FA0`) runs only for an engaged unit (flag bit 23,
  `00313059`). It suspends the unit's own action (`BattleUnit_SnapshotAndSuspendActionState` at `0031307B`) and saves
  `+0xDC8` / `+0xE58` into a 12-byte per-slot table at `022C1DB0` (`003130A7`–`003130C7`). Then it sets bit 22
  (`003130D2`) and commits action `0x96`, Attack, through `BattleUnit_CommitAction` (`00313096`, `003130DC`). On success it
  sets `+0x6B4 = 5` (`003130F2`), the same phase entry as a combo hit.
- **Lowered.** `00308270` (120 B, read whole) does nothing unless bit 22 is set (`0030827B`). When it is, it clears the
  retaliation handle `+0x28` (`00308282`), releases the presentation slot, puts `+0xDC8` / `+0xE58` back from `022C1DB0`
  (`0030829C`–`003082C0`), restores the suspended action (`003082C6`), and clears bits 22 and 46 (`003082CB`–`003082DF`).
  Its callers are `BattleUnit_UpdateCombatFrame` (`003086AA`, `003087B9`), `BattleUnit_SelectAndCommitNextAction`
  (`00305AC8`), `BattleUnit_ReleaseTargetRelationAndActionState` (`00310806`), and the auto-attack's own failed-commit
  path (`00313109`).
- **Read.** Besides this gate, two sites read it, and both skip a step while it is set. `Battle_ProcessActionTarget`
  does not record the source as the target's retaliation handle (`0030778E`–`00307798`). `BattleUnit_CommitAction` does
  not count the source in the target's attacker mask (`0030F937`–`0030F962`).
- **Scope of the "only".** An `and` / `btr` sweep of `[reg]` stores in `00230000`–`003A0000` found nine candidate clears
  of bit 22. `003082DF` is the only one on a BattleUnit. The other eight are computed single-bit clears on bitmaps,
  pool-node headers, a lane mask and a bit-field packer, none of them on a unit. The same sweep finds `003130D2` as the
  only constant `or` of the bit on a unit. A whole-qword store to the flag word is not covered by this sweep.

**So the auto-attack a unit makes on engaging is a single Attack that interrupts, and then restores, what the unit was
doing.** Test 3 keeps it from growing into a combo.

## 3. Key addresses

| Address | Name | Size | Verified |
|---|---|---:|---|
| `0030FA00` | `BattleAction_TryContinueComboSequence` | 146 B | read here — **previously undocumented** |
| `0031B860` | `BattleStats_FindOwningBattleUnit` | 83 B | read here, complete |
| `00325D90` | `BattleUnit_CanAdvanceCombatNavigation` | 203 B | site read — **previously undocumented** |
| `003105D0` | `BattleUnit_CancelAndResetCurrentAction` | 418 B | site read |
| `0023B040` | `PartyControl_RecomputeSuppressionFromLeaderBattleState` | 447 B | site read; read as a gate in 11-Party |
| `00385680` | `BattleFormula_EvaluateTargetPreview` | 1153 B | site read |
| `00388660` | `BattleFormula_RollAndStoreComboCount` | 602 B | site read; the roll is in 08-Combat-Formula |
| `003272A0` | `BattleUnit_GetPartyLeader` | 55 B | read here, complete |
| `0030C010` | the continue predicate | 179 B | read whole 2026-09-12 (§2.5) |
| `00308610` | `BattleUnit_UpdateCombatFrame` | 461 B | site read 2026-09-30: the continue path's only direct caller (`0030879F`, §5) |
| `00312FA0` | `BattleUnit_TryCommitEngageAutoAttack` | 382 B | `00313041`–`00313109` read 2026-09-30: sets flag bit 22 (§2.5 test 3) |
| `00308270` | ends an engage auto-attack (clears flag bit 22) | 120 B | read whole 2026-09-30 (§2.5 test 3) |

### Data addresses cited by this document

| Address | What | Anchor |
|---|---|---|
| `02EBF188` | global holding the last unit resolved by `BattleStats_FindOwningBattleUnit` | `003857BA`, `0038867E`, `003886C3` |
| `0208D480` | 64-byte per-kind record table | `003886AB` |
| `0208DE80` | the second 64-byte record table, indexed by `byte [unit + 0xEA9]` | `003886D6` |
| `02AEDFE4` | threshold the first combo roll compares against | `00388716` |
| `02AEDFC4`, `02AEDFC8` | zeroed together when a combo is accepted | `003888A1`, `003888AB` |
| `01EFA610` | calculator slot 10 of the step table `01EFA5C0`: the qword `00388660` (§5) | read from the image 2026-09-30 |
| `022C1DB0` | 12-byte per-slot save of `+0xDC8` / `+0xE58` across an engage auto-attack (§2.5 test 3) | `003130A7`–`003130C7`, `0030829C`–`003082C0` |

## 4. Data structures and formulas

### 4.1 What each of the four readers does with it

| function | test | consequence |
|---|---|---|
| `00388660` | `!= 0` | **skip the roll**, compare progress against the stored nibble |
| `00325D90` | `> 0` (`00325DE6 ja`) | **return 0** — combat navigation cannot advance |
| `0023B040` | `> 0` (`0023B12D cmova`) | `ebx` **replaced wholesale** by `r14d`, discarding flags accumulated above |
| `00385680` | `!= 0` | clear the preview byte's high nibble and install `r14b`'s instead |

**Three of the four are `> 0` or `!= 0` on a byte — none tests a specific value**, so nothing read
here distinguishes hit 2 from hit 9 outside `00388660`'s comparison.

### 4.2 A note on `+0x6B4`, from three documents' reads

`+0x6B4` sits immediately before this pair and is written with a small set of literals by code read
across three documents: **`0` by the reset** (`003106F2`), **`2` by all 25 arms of the direct-command
dispatcher** (25 `mov byte ptr [rbx + 0x6b4], 2` stores, `002FDE50`–`002FE516`, in
`BattleUnit_ExecuteDirectStateCommandOrder` `002FDDA0`, counted 2026-09-30; the arm map is
[the gambit-set page](../09-Combat-AI-And-Gambits/which-gambit-set-fires-and-how-a-command-switches-it.md) §5,
"The dispatcher's complete arm map"), **`5` by the combo continue path** (`0030FA80`), and **compared against `9`** at
`0023B146`. It is a phase enumeration with at least four reachable values. *(The full static store census is on
[the field map](../04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md) row `+0x6B4`, 2026-09-12: a commit writes 0, and no displacement store explains
6–9 on the action path.)* ~~**No document has read
what any value means**, and this one does not either — the observation is recorded because three
separate reads now constrain it.~~

> **Corrected 2026-09-30 (FABLE).** The struck sentence was overtaken on 2026-09-14 by this page's own §8 (`UQ-118`).
> The values are entry points into the 13-phase machine (phases 0–12) of `BattleUnit_AdvanceStandardActionState`
> ([the command seam page](Command-And-Action-Seam/native-command-seam.md) §7, `UQ-108`). `2` enters at action setup,
> `5` at *arrived*, and `9` is the execution phase, where the target set is built. `6`–`9` are reached by the machine's
> own `inc byte [rsi + 4]` with `rsi = unit + 0x6B0`. That is why the displacement census quoted in the parenthesis
> above found no store for them; the field map's `+0x6B4` row carries the same correction (2026-09-14, UQ-108).

## 5. Call chain

```
the per-unit lifecycle frame (by role; the only caller of the next line)
  -> BattleUnit_UpdateCombatFrame (00308610)
       0030879F, only when target-buffer entry 0 exists (+0x780) and its outcome has bit 10 (00308786-0030879A)
       -> BattleAction_TryContinueComboSequence (0030FA00)   re-commits the same action, ++counter
            -> 0030C010  (continue predicate, §2.5)
            -> BattleUnit_CommitAction (0030F760)

calculator step table 01EFA5C0, slot 10 (the qword at 01EFA610 holds 00388660)
  <- BattleFormula_ResolveTargetResult (00385F60)      recipe loop, call at 003863D0
  <- BattleFormula_EvaluateTargetPreview (00385680)    recipe loop, call at 003859FF
       -> BattleFormula_RollAndStoreComboCount (00388660)
            -> BattleStats_FindOwningBattleUnit (0031B860)
                 -> BattleUnit_GetSlotCount (00236850) / BattleUnit_GetBySlotIndex (00236820)
            sets the result's flag word B bit 1 (0038887A) when another hit is due

BattleUnit_ResetStateForReuse (00236A60)
  -> BattleUnit_CancelAndResetCurrentAction (003105D0)  clears +0x6B7 and +0x6B8 in one store
```

**Upstream (who causes this)** *(added 2026-09-30, FABLE, from `rawcalls.json` and the bodies):*
- **`BattleAction_TryContinueComboSequence` has one direct caller**, `BattleUnit_UpdateCombatFrame` at `0030879F`. The call
  is reached only when the unit's first target-buffer entry exists and its outcome word has **bit 10** (`00308786`–`0030879A`).
  That is the "combo continues" bit, which `Battle_ProcessActionTarget` copies from the resolved result's flag word B
  bit 1 ([the scratch block](../08-Combat-Formula/Scratch-Block/the-formula-scratch-block.md) §2.4). `00308610` itself
  has one caller, the per-unit lifecycle frame.
- **`BattleFormula_RollAndStoreComboCount` has no direct call site.** It is **calculator slot 10** of the step table at
  `01EFA5C0`: the qword at `01EFA610` holds `00388660`, read from the image. So it runs whenever a recipe that lists
  slot 10 is interpreted, by the resolver's recipe loop (`003863D0`) or the preview's (`003859FF`)
  ([the step table](../08-Combat-Formula/Step-Table/combat-formula-step-table.md), "The interpreter, read"). Its first
  argument is the **source's** stats (`003863CD`, `003859FC`), so the unit it reads the counter from is the attacker.

**Downstream (what this causes):** the continue path re-commits through `BattleUnit_CommitAction` and, on success, sets
`+0x6B4 = 5` (§2.2). The roll writes the count nibble and flag word B bit 1 (§2.3). That bit reaches target-buffer entry 0
as bit 10, which is the condition `BattleUnit_UpdateCombatFrame` tests before calling the continue path. **That loop is the
whole combo: roll, flag, entry bit 10, continue, re-commit.**

**Do not confuse with:**
- the guard/parry and knockback pre-rolls (slots 8, and 5 / 6). They run in the same recipe loop, and an accepted combo
  clears their outcomes ([the guard/parry note](../08-Combat-Formula/combos-and-the-guard-parry-flag.md));
- the engage auto-attack (§2.5 test 3). It commits the same Attack id, but it blocks continuation.

## 6. The correction this read forces

[`../08-Combat-Formula/combos-and-the-guard-parry-flag.md`](../08-Combat-Formula/combos-and-the-guard-parry-flag.md)
says, of the same branch:

> *"If the source's **record byte** `+0x6B7` is non-zero, no roll happens at all... **A forced combo
> count is a field, not a special case.**"*

**The branch is read correctly; the byte is attributed to the wrong object.** In `00388660` the
record is `rdi` and the unit is `rax`, and they are established separately:

```asm
0038868A  movzx ebx, byte ptr [rax + 0x6b7]   ; rax = owning BattleUnit
003886A7  movzx edi, byte ptr [rsi + 4]       ; \  rdi = 0208D480 + kind*0x40
003886B2  shl   rdi, 6                        ;  |  the RECORD
003886B6  add   rdi, rax                      ; /
0038886B  movzx eax, byte ptr [rdi + 0x12]    ; the stored nibble IS on the record
```

`+0x6B7` is a **BattleUnit runtime field**, written only by `BattleAction_TryContinueComboSequence`
(increment) and `BattleUnit_CancelAndResetCurrentAction` (clear). **It is not authored data and there
is no forced-value path.** The roll is skipped on hits 2..N because **the count was already decided
on hit 1 and memoised in the record's high nibble** — the suppression is caching, not an override.

**Which matters for modding, not just for accuracy:** an authored record byte would be a per-action
designer knob; a runtime counter cleared by the action reset is not patchable in the same way.

That document's own falsification entry — *"Is the forced-value path a debug feature? Not
established... nothing here says who writes `+0x6B7`"* — is the reason the error was visible and
correctable rather than load-bearing. **It marked its own uncertainty in the right place.**

## 7. Modding notes

- **`unit + 0x6B7` is combo progress, `+0x6B8` is cleared with it, and `+0x6B4` becomes 5 while a
  combo runs.** Forcing `+0x6B7` non-zero pins a unit into "mid-combo": it cannot advance combat
  navigation and its party-control suppression is overridden.
- **The combo length lives in the high nibble of `0208D480 + kind * 0x40 + 0x12`** and is rewritten
  on the first hit of every combo, so patching it statically is overwritten by the next roll.
- **The clear is a single `word` store at `+0x6B7`.** A hook that resets only `+0x6B7` leaves
  `+0x6B8` stale.
- **Unit flag bit 22 blocks continuation, but it is not a combo switch** (added 2026-09-30). The retaliation-handle store
  (`0030778E`) and the attacker count (`0030F937`) read the same bit, and `00308270` treats a set bit as a suspended
  action to restore (§2.5 test 3). Forcing it to stop combos would disturb all three.

## 8. What is not known

- [x] ~~What `0030C010` (179 B) tests to permit continuation~~ **Answered 2026-09-12, §2.5** — six conditions. ~~— **the actual gate on whether a combo
      continues at all** is behind this call and is not read.~~
- [x] ~~**UQ-115.** What `+0x6B8` holds. It is saved and restored across the continue call and cleared with the
      counter; nothing here reads its value.~~
      **Answered 2026-09-14 (FABLE): the combo's running hit tally, and it is read.** The one reader the page
      lacked is in `Battle_ProcessActionTarget`.
      - **The count.** For action id `150` (`cmp r15w, 0x96`, `00307651`–`0030765A`), each processed target
        increments byte `+0x6B8` (`0030765C`–`00307665`). The handler table's authored census names action 150 as
        *Attack*.
      - **The display.** When the new value exceeds `r12b` (`1` on that path, `0030746E`), it calls a 26-byte
        forwarder with the unit id `[unit+8]` and the count (`00307670`–`00307676`). The forwarder passes them to
        the HUD object `[0209BE80] + 0x5380`, the object the EXP / LP presentation also uses. The HUD routine
        refuses counts below 2, formats the count with `"%2.2d"` (`00915FA4`), and caps a derived glyph value at
        `0x12`. *(Anchored 2026-09-30, FABLE: `00289D70`–`00289D74` refuse a count below 2. `00289DE7`–`00289E08` pack the two
        formatted digits one per nibble, tens in the high nibble, and cap the packed value at `0x12` with `cmovg`. In that
        packing `0x12` reads "12", which matches the twelve-hit ceiling of
        [the roll](../08-Combat-Formula/combos-and-the-guard-parry-flag.md).)*
      - **Why continue saves it.** `BattleAction_TryContinueComboSequence` reads the tally before
        `BattleUnit_CommitAction` and writes it back afterwards (`0030FA19`, `0030FA65`). The re-commit therefore
        does not reset the number on screen. The cancel / reset word store clears it together with the counter.
      - **Scope.** In the `00230000`–`00400000` range the raw sweep finds four byte-width `+0x6B8` sites, all in these
        two functions. The reset's word store addresses `+0x6B7`. The qword `+0x6B8` sites at `002E03D9` and `003704C2`–`003705A5`
        belong to other objects.
      - ~~**Not read:** what the HUD draws beyond the formatted number.~~ *Narrowed 2026-09-30 (FABLE):* the HUD routine
        **draws nothing itself; it records a popup.** It finds the unit's entry in a linked list at HUD object `+0x428`
        (`00289DB6`–`00289DCE`), or claims one of six 40-byte slots (`00289E73`–`00289E92`). It fills a new entry with a
        position looked up from the unit id (`00289D9F`, `00289EB1`–`00289EE6`) and the unit id itself (`00289EEB`), and
        stores the packed count in every entry it updates (`00289F24`). A walk of the same list head elsewhere in the HUD
        code calls a per-entry routine. **What that routine puts on screen is not read (`GR-3`).** *(2026-09-30, SWE2-STRUCT for OPUS: answered - GR-3, the `GR-3` item below: `0028AAA0` draws a label and the count; the label is the word "Hits" in the English pack.)*
- [x] ~~**UQ-116.** What `r14` holds at `003857D5` in the preview path, so what count it installs.~~ **Answered
      2026-09-14 (FABLE): it installs no new count.** `r14` is the record's own `+0x12` byte from before the reset,
      so the step **restores** the combo count that hit 1 stored.
      - **`0038579C`**: `movzx r14d, byte [rbx + 0x12]` saves the byte, and `r15w` saves the word at `+0x10`.
      - **`003857AB`–`003857B2`**: the record's `+0x00` and `+0x08` qwords and its `+0x10` dword are zeroed. That
        erases `+0x12` too.
      - **If the owning unit's counter `+0x6B7` is non-zero** (`003857C6`–`003857CF`), the low nibble is kept and the
        saved high nibble is put back (`003857D1`–`003857D9`). That nibble is the count `00388660` rolled on hit 1
        (§2).
      - **In every case**, bit 0 is then set and the saved `+0x10` word is restored (`003857DD`, `003857E1`).
      - **The effect.** Re-evaluating a preview in the middle of a combo does not lose the rolled count. On a first
        hit (counter 0) the high nibble stays zero until `00388660` rolls. So §4.1's "install `r14b`'s instead" is
        installing the value the byte already had.
- [x] ~~**UQ-117.** What `02EBF188` is read by, if anything — three sites write it, none here reads it. *Narrowed 2026-09-12:*
      the image holds **93 rip-relative stores and no rip-relative read** of it (`ripscan`; the same scan finds
      reads of `022C2160`); a register-based read is not excluded.~~
      **Answered 2026-09-14 (FABLE): nothing reads it statically. It is a write-only scratch.**
      - **The writes.** The 93 stores are all `mov qword [02EBF188], rax`. They sit in the battle formula, runtime and
        post-result functions. 88 of the 93 follow a `call` directly, storing its return value; for example the store
        at `003857BA` follows `BattleStats_FindOwningBattleUnit`. The other five follow a register reset.
      - **No register route either.** No instruction in the image takes its address with a `lea`.
        - Its `lea`'d neighbours `02EBF008`–`02EBF170` are single-qword pointer globals, each passed on its own as
          `rcx` to a section-descriptor bind such as `AreaData_BindAndRebaseSectionDescriptor`.
        - `02EBF178`–`02EBF188` have no `lea` at all.
        - So no base register points at or just below it.
      - **What remains possible:** a debugger or instrumentation reading the global, or a block copy of the whole
        `.bss` range. Neither is visible as code.
- [x] ~~**UQ-118.** What the `+0x6B4` values `2`, `5` and `9` denote.~~ **Answered 2026-09-14 (FABLE):**
      they are entry points into the 13-phase machine of `BattleUnit_AdvanceStandardActionState`. The full table is
      [the command seam page](Command-And-Action-Seam/native-command-seam.md) §7, UQ-108.
      - **`2`**, stored by the direct-state order arms, enters at the second `inc` of phase 1's exit. It skips
        preparation (phase 0) and the `+0x760` accumulation (phase 1), and goes straight to action setup (3).
      - **`5`**, stored by the combo continue and the engage auto-attack, enters at *arrived*. It skips setup and
        the approach (3–4), so a combo hit does not re-run setup, the approach or the accumulation.
      - **`9`** is compared, not stored. It is the execution phase: `Battle_BuildActionTargetSet` runs there.
        The entry test at `003048BD` (`jae` on 9) therefore asks whether the targets are built. ~~The comparison at
        `0023B146` was not re-read here.~~ *Read 2026-09-30 (FABLE):* in
        `PartyControl_RecomputeSuppressionFromLeaderBattleState` it is the second half of one test. After the combo
        override (`0023B12D`), suppression bit 1 is set again (`0023B14F`) when the leader's unit flag bit 24 is set
        (`0023B131`–`0023B136`), or when its action id is at most `0x21E` (`0023B138`–`0023B144`) **and** its phase
        has reached 9 (`0023B146`–`0023B14D`). So a leader whose real action has reached execution is suppressed whether
        or not it is mid-combo. The `cmova` override (§4.1) therefore replaces only the flags accumulated **before**
        `0023B124`; the bit set at `0023B14F`, and bits 0 and 2 under a status mask (`0023B159`–`0023B16B`), still apply
        after it.
      - **`6`–`9` are reached** by the machine's own `inc byte [rsi + 4]` with `rsi = unit + 0x6B0`. That is why no
        `[reg + 0x6B4]` store explains them.
- [x] **`GR-3`** (registered 2026-09-30, FABLE). What the battle HUD draws for a combo-count entry. The entry is
      recorded as above (UQ-115); the per-entry draw routine reached from the list walk is not read. It settles
      statically by reading that routine whole, or at runtime by capturing the popup during a combo.
      *(Answered 2026-09-30, SWE2-ORACLE for OPUS `125b3a5c1`; register row GR-3, record [`hud-blocks-identified-0930`](../_index/candidates/hud-blocks-identified-0930/README.md) (its GR-3 section): `0028AAA0` draws a label sprite and the one- or two-digit count, slammed in from double size with a fading echo over about 0.53 s, then held 2 s following the unit and faded; at the cap of 12 it grows 20 % and pulses. Which glyph the label is stays unread.)* *(Answered 2026-09-30, SWE2-STRUCT for OPUS, DD batch 11, static and shipped data; record [`swe2struct-ddres-b11-0930`](../_index/candidates/swe2struct-ddres-b11-0930/README.md), `b11_struct.py` C1-C6 and D1-D4, FAILS 0: **the label is a word, "Hits", localised per language pack.** The sprite set `[0209AC30]+0x338` is the UI atlas `battle_4_c`: `00280750` registers ten atlas names into `+0x338`..`+0x380` (`002807E8`-`00280839`), and `00280670` binds `tex2pack_ys.bin` directory entry *i* to the *i*-th of those slots (`0028068E`-`002806CA`); `+0x360` is `partytop_4_c`. `0028AAA0` draws the label as sub-image code `0x0001`, frame 14, of `battle_4_c` (`0028AC36`-`0028AC68`, the same lookup as `0029F4F1`-`0029F50F`). In all nine full-size packs that is the 130 x 60 cell at (120, 0), and it reads "Hits" (`us`), "Treffer!" (`de`), "coups" (`fr`), "golpes" (`es`), "colpi!" (`it`) and "Hits!" (`in`, `kr`, `ch`, `cn`); the low-resolution `in_sdver` pack has a 37 x 17 "Hits". The digits are `partytop_4_c` code 2 (28 x 38 cells) below the cap and code 1 (36 x 50 cells) at it, with the digit value as the frame (`0028AE49`-`0028AF24`). In player terms: the popup is the hit count beside the word "Hits" ("Treffer!" in German), and at 12 its digits switch to the larger style.)*

## 9. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| Seven sites, six functions | whole-image displacement census over 38,161 functions with a body | 2 |
| `+0x6B7` and `+0x6B8` are cleared by one `word` store | `00310649 xor ebp, ebp`; `003106EB mov word ptr [rbx+0x6b7], bp` | 1 |
| Every other access is byte-wide | `0030FA0F`, `0030FA79`, `0023B124`, `00325DDF`, `003857C6`, `0038868A` | 1 |
| The continue path re-commits the same action | `0030FA3B`-`0030FA5C` reading `+0x710`, `+0x714`, `+0x708` | 1 |
| The counter advances only on a successful commit | `0030FA63 je 0x30fa29` guarding `0030FA6C inc dil` | 1 |
| The roll is skipped when the counter is non-zero | `003886F5`-`003886F7` | 1 |
| Later hits compare progress against a stored nibble | `0038886B`-`00388874` | 1 |
| The nibble is on the record, the counter is on the unit | `003886A7`-`003886B6` (record) vs `00388679`-`0038868A` (unit) | 1 |
| `0031B860` returns a BattleUnit | it returns a value from `BattleUnit_GetBySlotIndex` matched on `+0x698` — `0031B888`-`0031B899` | 1 |
| A non-zero counter blocks navigation | `00325DDF`-`00325DE6`, target `00325DA5` is `xor eax,eax; ret` | 1 |
| A non-zero counter overrides party suppression | `0023B124`-`0023B12D`, `cmova ebx, r14d` | 1 |
| Two globals are zeroed on an accepted combo | `003888A1`, `003888AB` | 1 |
| The continue path has one direct caller, gated on entry bit 10 | `0030879F` in `00308610`, after `00308786`–`0030879A`; `rawcalls.json` lists no other site | 1 |
| The roll is calculator slot 10 and has no direct call site | the qword at `01EFA610` is `00388660`; indirect calls at `003863D0` and `003859FF` | 1 |
| Flag bit 22 is raised for an engage auto-attack and lowered by `00308270` | `003130D2` before the commit at `003130DC`; `0030827B`, `003082CB`–`003082DF` | 1 |
| No other clear of bit 22 on a unit | `and` / `btr` sweep of `[reg]` stores, `00230000`–`003A0000`: nine candidates, one on a unit | 2 |
| `+0x6B4 = 2` is stored by 25 arms | 25 byte stores `002FDE50`–`002FE516` in `002FDDA0` | 1 |
| The HUD packs the formatted count into nibbles and caps it at `0x12` | `00289DE7`–`00289E08` | 1 |
| The HUD routine records a popup entry rather than drawing | `00289DB6`–`00289DCE`, `00289E73`–`00289F29` | 1 |
| `0023B146` is the phase-9 half of a suppression test after the combo override | `0023B131`–`0023B14F` | 1 |
| The combo popup's label is `battle_4_c` code `0x0001` frame 14, the localised "Hits" (added 2026-09-30, SWE2-STRUCT for OPUS) | `002807E8`–`00280839`, `0028068E`–`002806CA` (slot `+0x338` = `battle_4_c`); `0028AC36`–`0028AC68` (the lookup, `+0x70`); the ten `tex2pack_ys.bin` packs in the archive; `b11_struct.py` in [`swe2struct-ddres-b11-0930`](../_index/candidates/swe2struct-ddres-b11-0930/README.md) | 1 (code) / data (the packs; the words read from the rendered cells) |

**Control on "seven sites, six functions".** The claim is an absence — that nothing else touches the
byte. The same census positively returns **84** sites for `+0x6B4`, **4** for `+0x6B5` and **15** for
`+0x6B6`, so it is not silently failing in this neighbourhood. **The census is tier 2, not tier 1**:
it decodes `[reg + disp]` forms only, so an access that computes its address arithmetically would not
appear. No such form was seen in any of the six bodies read here, but that is six bodies, not the
image.

**Scope limit.** `+0x6B8` has 65 sites image-wide, most of them in the `0053xxxx` and `007Cxxxx`
regions and **not this structure**. Nothing above counts a census hit as a battle-unit hit: the
`+0x6B8` claims rest only on `0030FA00` and `003105D0`, both proven to hold a unit pointer.

## 10. Related

- [`../08-Combat-Formula/combos-and-the-guard-parry-flag.md`](../08-Combat-Formula/combos-and-the-guard-parry-flag.md)
  — the roll itself, the health bands, and the guard/parry flag this counter's acceptance clears;
  section 6 above corrects one attribution in it
- [`the-moment-an-action-is-committed.md`](the-moment-an-action-is-committed.md) — `BattleUnit_CommitAction`,
  which the continue path calls again with the same three arguments
- [`../09-Combat-AI-And-Gambits/which-gambit-set-fires-and-how-a-command-switches-it.md`](../09-Combat-AI-And-Gambits/which-gambit-set-fires-and-how-a-command-switches-it.md)
  — `+0x6B4`'s other writers, and `+0x698` as the stats pointer from the other direction
- [`../11-Party/party-roster-and-control-suppression.md`](../11-Party/party-roster-and-control-suppression.md)
  — `0023B040`, whose suppression result this counter overrides

## 9. Falsification pass 1 — 2026-09-13 (OPUS)

*(`check_already_answered.py --addr 0030FA00 --term 0x6B7` run first, per
[`EVIDENCE-STANDARD.md`](../_index/EVIDENCE-STANDARD.md)'s 2026-09-13 amendment.)*

| claim | measured |
|---|---|
| `0030FA00` **146 B**, `0031B860` **83 B** | **146** and **83** |
| "**seven instructions** touching it across **six functions**" | **7 in 6** — no more, no fewer |
| the six byte-wise sites §2.1 lists | `0030FA0F`, `0030FA79`, `0023B124`, `00325DDF`, `003857C6`, `0038868A` — **all six, address for address**, with `003106EB` the seventh |
| "the reset writes a **word**, clearing `+0x6B7` and `+0x6B8`" | `003106EB mov word ptr [rbx + 0x6b7], bp` — the only non-byte access of the seven |

### Both player-facing claims are single instructions, and both are exact

§1 says a running combo makes movement impossible and **overrides** the leader's suppression state
*wholesale*. Each is one instruction:

```asm
00325DDF  cmp   byte ptr [rdi + 0x6b7], 0
00325DE6  ja    0x325da5                    ; non-zero -> straight out

0023B121  or    ebx, 2                      ; ebx has been ACCUMULATING flags
0023B124  cmp   byte ptr [rdi + 0x6b7], 0
0023B12D  cmova ebx, r14d                   ; non-zero -> ebx REPLACED, not or'd
```

**`cmova` is the word "wholesale".** The suppression value has been built up with `or` immediately
above; a non-zero counter **discards all of it** and substitutes `r14d`. The distinction §1 draws —
*overrides … rather than contributing one more flag to it* — is the difference between that `cmova`
and the `or` two instructions before it, and a reimplementation that OR-ed a combo flag into the
same accumulator would be wrong in exactly the way the sentence warns about.

### Nothing to add

The two-byte pair and the word store — what this pass had ready — are **already** §2.1's opening
claim, with the same instruction offered as its proof. Found by searching before claiming.

**Not claimed:** §3's roll-and-store path, §4's focus fields at `+0x708`/`+0x710`, and §6's
reinterpretation of what the byte means were **not** re-derived — this pass checked the census and
the two gates. Nothing was executed or observed live.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. MECHANICAL-only crossings (the image-address resolver, the audio request chain) are recorded in the registry, not here.*

- **RNG_Random_Selection — SERVICE.** `BattleFormula_RollAndStoreComboCount` (`00388660`) draws the gameplay MT
  (`RNG_MT19937_NextU32_Thunk`). **The combo count is a combat-formula roll**, so it is on the stream that save loads
  reseed from the clock ([which roll](../21-RNG-And-Determinism/which-roll-is-on-which-generator.md)).
- **Rewards_Progression_Economy — CLIENT.** `BattleStats_FindOwningBattleUnit` is also used by the level-up path and
  `Reward_ComputeExperienceForRecipient`.
- **Items_Equipment_Shops_License — CLIENT.** The owner lookup is driven by the equipment-slot and licence-node setters.
  `BattleStats_ClearAllEquipmentSlotsByMapp…` walks the unit table.
- **Spawn_Encounter_Lifecycle — CLIENT.** `Spawn_CountActiveCapTrackedActors` walks the unit table.
  `Spawn_TrySelectCandidatePosition` and `SpawnLifecycle_CheckAndRetireByNativeRange` read `BattleUnit_GetPartyLeader`.
- **InputGameplay — CLIENT.** The 12-byte `00253B90` is read by a 289-byte Input-filed helper that also reads the field
  action-permission bit.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Gameplay — CLIENT.** `BattleUnit_UpdateEngagementStateFlag`, owned by that layer, calls `00253B90` on this page. That caller is the engagement test, which reads the actor's `+0x698` block and tests `+0x3C` OR `+0x64` against its own mask; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**UI — CLIENT.** `FUN_00322a80`, owned by that layer, calls `00236820` on this page. That caller is a 456-byte lookup that resolves its row through the `[02EBF138]` table and the image-base helper before comparing the caller's word; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page.*

**CombatAI — CLIENT (14 edges).** `BattleUnit_GetBySlotIndex` `00236820` and `BattleUnit_GetSlotCount` `00236850` are called by `AiOrder_EvaluateTargetSelector` `00301AD0`, `BattleEnmity_PropagateToPerceivingFoes` `003219D0` and `BattleUnit_RebuildPerceptionCandidateCache` `003247F0`, and `00236820` also by `AiOrder_ComputeBoundedSelectorScalar` `00308C20` and `BattlePerception_RefreshCandidateCacheGeneration` `00324F20`; `BattleUnit_CommitAction` `0030F760` is called by `BattleUnit_SelectAndCommitNextAction` `00305AB0` and `BattleUnit_TrySelectAndCommitAiOrderFromSet` `00305CC0`; `BattleUnit_UpdateCombatFrame` `00308610` calls the continue path `BattleAction_TryContinueComboSequence` `0030FA00`, the fleeing test `00253B90` and `BattleUnit_CancelAndResetCurrentAction` `003105D0`; `00301AD0` calls `BattleUnit_GetPartyLeader` `003272A0`. The AI's per-unit combat frame is what reaches the continue path, and the AI commits the actions whose combo this page tracks; the unit-table walks are shared accessors.

**CombatFormula — CLIENT and SERVICE (49 edges).** `BattleStats_FindOwningBattleUnit` `0031B860`, which walks the unit table through `00236820` and `00236850` (as `BattleStats_GetOwningActorHandle` `0031E800` and `00384F40` do), is called by 35 formula bodies, among them `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30`, `BattleStats_ModifyHPAndProcessLethalState` `00300530`, `BattleFormula_ApplyTargetResult` `003112F0`, `BattleFormula_ResolveTargetResult` `00385F60`, `BattleFormula_RollGuardParryMode` `003884F0` and the combo-count roll `BattleFormula_RollAndStoreComboCount` `00388660`; `002FEF30` calls `003105D0`; and the preview `BattleFormula_EvaluateTargetPreview` `00385680` calls `0031B860`, `BattleStats_GetByBattleSlotIndex` `00320A40`, `BattleStats_ResolveByActorHandle` `00320A70`, `BattleFormula_BuildEvaluationContext` `003847C0`, `BattleFormula_InitializeResultRecord` `003848E0`, `BattleFormula_ResetScratchState` `003849B0` and one more. The combo count is rolled once per combo inside the formula layer (§2.3), and that roll and the preview reader resolve the unit through the same owner lookup every formula body uses.

**Movement — CLIENT and SERVICE (32 edges).** `00236820` is called by ten locomotion bodies, among them `BattleLocomotion_QueryDynamicActorObstruction` `003357B0`, `BattleLocomotion_BuildSolverContext` `00336710`, `BattleLocomotion_ResolveTargetSpacingAndAvoidance` `00338140` and `PartyFollow_SolveFormation` `00338490`, and `00236850` by four; `003272A0` by nine, among them `BattleLocomotion_DecodeOrderGoal` `00312730` and `PartyFollow_LookupDestination` `00339A60`; `0031B860` by `0033CB10` and `0033D890`; `BattleUnit_ResetStateForReuse` `00236A60` calls `003839C0` and `Navigation_ResetPathPredecessors` `003839F0`; `003105D0` calls `BattleLocomotion_ResetPathAndSetTargets` `003291B0` and `0033C9B0`; `BattleUnit_CanAdvanceCombatNavigation` `00325D90` calls `0030BCD0` and is called by `BattleUnit_UpdateCombatNavigationStep` `00325BB0`; `00234520` calls `PartyControl_RecomputeSuppressionFromLeaderBattleState` `0023B040`. Cancelling an action or recycling a unit resets its path, and combat navigation refuses to advance while the counter is above zero (`00325D90`, one of the four readers in §4.1); the remaining edges are locomotion walking the unit table and asking for the leader.

**Party — SERVICE and CLIENT (13 edges).** `PartyConfiguration_ReconcileRosterFromCurrentSelectors` `003261D0` and `PartyConfiguration_SetSelectorsAndReconcileRoster` `003273D0` call `00236820` (and `003273D0` `00236850`); `0023B040` calls `003272A0`, `PartyControl_SetMovementSuppressionBit` `00359200` and `PartyControl_SetSuppressionMask1Bit` `003592C0`, and `003272A0` calls it back; the gate `0030C010`, `0030F760` and `0031ADB0` call `BattleUnit_ResolveByFocusHandle` `0031B7E0`; `0031ADB0`, `00325D90` and `003272A0` call `PartyFocus_GetCurrentPackedActorHandle` `003590D0`. The combo gate and the commit resolve the unit behind the player's focus handle, and the party-suppression recompute `0023B040` — another of §4.1's four readers, which replaces its accumulated flags while the counter is above zero — is the party layer's own body.

**Presentation — CLIENT (2 edges).** `BattleUnit_ComputePartyBattleStance` `00308130` calls the fleeing test `00253B90`, and `0030F760` calls `BattleUnit_BroadcastPartyCombatTargetRelation` `00313B30`. The party battle-stance computation reads the same one-dword fleeing flag (`01E0C2B8`) that test 1 of the combo gate reads, and committing an action broadcasts the combat target relation to the presentation layer.

**Status_Periodic_Terminal — CLIENT (8 edges).** `003105D0` is called by `BattleUnit_ResetActionControlForStatusTransition` `00300140` and `BattleUnit_RecoverFromTerminalStatusSetIfClear` `00301140`; `0031B860` by `BattleUnit_ResolvePeriodicPrimaryResourceRecoveryStep` `002F9400`, `BattleStats_ChangeStatusAndProcessSideEffects` `0030E360`, `BattleStats_RemoveStatusesFromMaskAndRecompute` `0030F690`, `BattleStats_RecomputeDerivedStateAndAutoStatuses` `0030FED0` and `BattleFormula_BuildRuntimeCounterPeriodicHpCredit` `00386860`; `00236A60` calls `BattleUnit_TakeAndClearPrimaryResourceRecoveryAccumulator` `00320450`. A status transition cancels the unit's current action through the same reset that ends a combo, and the status paths share the owner lookup.
