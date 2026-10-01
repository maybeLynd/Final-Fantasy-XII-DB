---
system: The steal roll — calculator slot 195, the three chances, and the debug override
category: 08-Combat-Formula
status: AUDITED
owner_layer: PrimaryOwner:CombatFormula
evidence_tier: 1
level: L1
readiness: BEHAVIORALLY UNDERSTOOD
confidence: PROVEN
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: 00390390 (741 B) read to its ret from the shipping EXE with every RIP target computed by a
    tool; its table slot found by scanning .data for its address; the console option it consults
    matched to the tuning-console catalogue by offset; the recipe that names the slot decoded from
    01EF96C0 and the action that names the recipe found in action_data.bin (archive copies in, kr);
    the resolver 00385F60, the post-result dispatcher 00469EC0 and the event poster 0046AB10 read at
    the sites that consume the scratch globals
last_reviewed: 2026-09-10
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-steal-roll-pass-1
  last_pass_kind: falsification
  crossref_clean: true
  reopened_count: 0
---

# The steal roll — calculator slot 195

> Steal is a formula like any other: a slot in the calculator table, fed the target's stats record
> and the action context. It reads the enemy row's three item words and the spawn record's three
> availability bits, then rolls — three independent rolls at 80 / 30 / 6 % when the action carries
> one flag, one first-hit roll at 55 / 10 / 3 % when it does not — and leaves its answer in five
> scratch globals. The resolver that ran it copies the three "won" bytes into the result record at
> `+0x32`–`+0x34` for the applier, turns "failed" into result kind 6, and the post-result dispatcher
> turns kind 6 on action `0xA9` into one of two battle messages. A developer-console option can
> force a tier.

## 1. What the player sees

A steal attempt on an enemy that still has something to take succeeds by chance: the common item
most of the time, the uncommon one sometimes, the rare one rarely — and with the right accessory
all three can come at once. An enemy with nothing left to steal fails every time with a distinct
message. Behind the message: three words in the enemy's definition row, three bits in its spawn
record, and this function.

## 2. Native mechanism

### 2.1 Where it sits

`00390390` has **no `call` or `jmp` site in the executable**; its address is the qword at
**`01EFABD8`** — slot **195** (`0x618 / 8`) of the calculator function table at `01EFA5C0` that
[the recipe machinery](../Recipe-System/ranged-weapon-recipes.md) dispatches through. The route to
it is exact:

- **recipe 49** — the qword at `01EF96C0 + 49 × 8` is `01EFA198`, a list with an **empty preview
  segment and a committed segment of exactly `[195]`**; no other recipe's segment holds 195;
- **action `0xA9`** — the only record of the 543 in `action_data.bin` whose recipe byte `+0x08` is
  49 (the archive's `in` and `kr` copies agree byte for byte on that record);
- **the slot loop** — `BattleFormula_ResolveTargetResult` (`00385F60`) reads the action's recipe
  byte (`0038617E`, bound `< 0x6D`), walks the committed segment (`00386350`–`003863A3`) and calls
  each slot at `003863D0` (`call [01EFA5C0 + slot × 8]`) with `(sourceStats, targetStats,
  &context)`, stopping early when `02AEDFB8` reads 1 (`003863D7`–`003863DE`).

So this function takes `(_, targetStats /*rdx*/, context /*r8*/)`: the target's stats record and
the evaluation context `BattleFormula_BuildEvaluationContext` (`003847C0`) filled at `003860BA`,
whose `+0x10` is the result record and whose `+0x1C` is a flag byte.

### 2.2 In execution order

| step | site | what |
|---|---|---|
| the row | `003903AD`–`003903DB` | `BattleStats_FindOwningBattleUnit(stats)` (`0031B860`), stored in `02EBF188`; for a kind-1 owner, `rdi = unit +0xE60` — the enemy definition row ([the unit-definition page](../../04-Actor-Entity/Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md)); otherwise `rdi = 0` |
| **nothing to steal?** | `003903DB`–`003903F3` | if all three item words `row.w_32`, `row.w_34`, `row.w_36` are `0xFFFF` → step "nothing" |
| **availability** | `003903F9`–`00390488` | each authored slot must still be available: `spawnRecord.b_14` bit 0 for `w_32` (`0039041E`), bit 1 for `w_34` (`0039044D`), bit 2 for `w_36` (`0039047E`) — the bits [the unit-definition page](../../04-Actor-Entity/Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md) §2.2 sets at a fresh spawn and the applier clears; a slot that is authored but already taken sends the whole attempt to "nothing" |
| **nothing** | `0039048A`–`003904A0` | `resultRecord.dw_2C \|= 0x800000` (the result record at `context +0x10`); `02AEDFBC = 1`; return |
| the branch | `003904A5` | `context.b_1C` bit 1 set → **the three-roll branch**; clear → **the one-roll branch** |
| **three rolls** (bit 1 set) | `003904AF`–`0039057C` | `r = RNG_MT19937_NextU32() % 100` (`00379CD0`, three times): **rare** (`w_36`) wins on `r < 6` or override `== 2` (`003904CD`–`003904EB`); **uncommon** (`w_34`) on `r < 30` or override `== 1` (`0039050A`–`00390527`); **common** (`w_32`) on `r < 80` or override `== 0` (`00390546`–`0039055B`); each win sets its own byte — `02AEE04E` (rare), `02AEE04D` (uncommon), `02AEE04C` (common) — **independently, so all three can be won**; if none was won, `02AEDFBC = 1` and `02AEDFB8 = 1` (`00390563`–`00390584`) |
| **one roll** (bit 1 clear) | `0039059F`–`00390670` | rare on `r < 3` or override `== 2` (`003905B8`–`003905CA`, `0039065B`–`0039066A`); else uncommon on `r < 10` or override `== 1` (`003905E9`–`003905F7`, `00390641`–`00390650`); else common on `r < 55` or override `== 0` (`00390612`–`0039061F`, `0039062B`–`00390635`); **first hit wins**: it sets its byte and jumps to `00390584` (`02AEDFB8 = 1` — the roll is over); a won tier whose word is `0xFFFF` fails instead (`0039057E`; the common tier goes back to "nothing", `00390495`); no hit → `00390621`–`00390626` → `0039057E`: `02AEDFBC = 1`, `02AEDFB8 = 1` |
| the override | `0017D450` (20 B) | `[001D50D0() + 0xE5C]` — **the developer tuning console's arm 243, "Enable 100% successful steal"** ([the console catalogue](../../00-Engine-Core-Runtime/Developer-Tuning-Console/arm-catalogue-slice-H-ids-236-267.md)): 0 forces the common tier, 1 the uncommon, 2 the rare |

Every `% 100` is the `0x51EB851F` multiply-shift idiom (`mul`, `shr edx, 5`, `× 100`, subtract).

### 2.3 The five scratch globals

| global | meaning | written |
|---|---|---|
| `02AEE04C` | the common slot was won | `0039055B`, `00390635` |
| `02AEE04D` | the uncommon slot was won | `00390527`, `00390650` |
| `02AEE04E` | the rare slot was won | `003904EB`, `0039066A` |
| `02AEDFB8` | **the roll is over — run no further calculator slots** (the resolver's loop reads it after every slot, `003863D7`); reached from every one-roll outcome and from a three-roll blank — a three-roll win leaves it 0 | `00390584` |
| `02AEDFBC` | the attempt failed — nothing to steal, or no tier won; the resolver turns it into **result kind 6** | `0039049A`, `0039057E` |

They belong to the formula scratch family beside `02AEE054`
([attack versus defence](../Attack-Vs-Defense/attack-defense-preparation-and-stat-scaling.md) §2):
global, one attempt at a time. `BattleFormula_ResetScratchState` (`003849B0`) zeroes all five before
every resolution — `02AEDFB8` / `02AEDFBC` at `003849BC`–`003849C2`, `02AEE04C` as a byte and
`02AEE04D`–`02AEE04E` as a word at `00384A1C`–`00384A23` — and the resolver calls it at `00386001`
before it runs any slot.

### 2.4 Where the answer goes

`BattleFormula_ResolveTargetResult` (`00385F60`) consumes all five after the slot loop and
`BattleFormula_ApplyTargetStatusActionPostModifiers` (`00390F20`, called at `003863F8`):

| scratch | what the resolver does | site |
|---|---|---|
| `02AEDFB8 = 1` | leaves the committed segment early — for the steal there is no later slot, so this only ends the loop | `003863D7`–`003863DE` |
| `02AEDFBC ≠ 0` | **result byte `+4` (the kind) = 6**; then `+4 == 6` → `result.dw_18 &= ~0xD` (bits 0, 2, 3 cleared) | `003866C1`–`003866CA`, `003866E7`–`003866EB` |
| `02AEE04C` | → `result.b_32` | `003867F1`–`003867F8` |
| `02AEE04D` | → `result.b_33` | `003867FB`–`00386802` |
| `02AEE04E` | → `result.b_34` | `00386805`–`0038680C` |

Those three bytes are the "three slots at `+0x32`" [the applier](../../07-Combat-Action/applying-a-result-to-a-target.md)
§2 step 4 reads: for each non-zero one it adds the row's item and clears the spawn record's
availability bit. `BattleFormula_EvaluateTargetPreview` (`00385680`) reads `02AEDFB8` / `02AEDFBC`
too (`003859AC`, `00385A07`, `00385A3A`), but recipe 49's preview segment is empty, so no steal
preview ever runs.

### 2.5 The message

`result +0x2C` bit 23 (`0x800000`, set by "nothing" at `0039048E`) has **one reader in the
executable**: a `.text` scan for the memory-operand encodings of the test (`test [r+0x2C], 0x800000`,
`test byte [r+0x2E], 0x80`, `bt [r+0x2C], 23`, with and without REX) finds one site, and the
positive control — this function's own `or [r+0x2C], 0x800000` — is found; the register-form
`bt r32, 23` has eleven sites, none of them preceded by a load from a `+0x2C` field (two of the
eleven are byte patterns inside longer instructions, not `bt`s). The reader is
`BattleFormula_DispatchPostResultEvents` (`00469EC0`) at `0046A3C4`–`0046A3F0` — when
the action id in `cx` is **`0xA9`** and the result kind byte `+4` is **6**, it posts ~~event **`0x34`** if bit 23 is set ("nothing to steal") and **`0x33`** if it is clear ("the steal failed")~~ event **`0x33`** if bit 23 is set — the row "…'s steal failed. … has nothing to steal." — and **`0x34`** if it is clear ("… couldn't steal from …."), through `0046AB10(stats, eventId, &context)`. **CORRECTED 2026-09-11:** the first publication had the two ids swapped; the `lea edx, [r13 - 0x76]` at `0046A3E6` is the one taken with the bit set, and the decoded table settles the texts ([the post-result events page](../../07-Combat-Action/Post-Result-Events/the-post-result-events-and-the-battle-message-table.md) §2.2, §2.5).

`0046AB10` (371 B) is the battle event poster the HP page and the status page had left unread
(`EY-3`, `FA-3` narrow here): it drops the event when `context.dw_28 ≥ 0x1FF` (`0046AB19`), when
the global flags word `02089340` has `0x3080` set or the unit's byte `+4` has `0x20` set
(`0046AB42`–`0046AB56`), or when the filter `00469570(eventId, ctx.q_00, ctx.q_08)` returns 0
(`0046AB65`); then, if the event's row in the authored table at `02EBF018` (registry slot 7) has
byte `+4` bit 0, it suppresses a repeat of the same `(event, unit)` pair still inside the window
`entry.dw_04 + 0x1C2 × [01DFE0B4]` of `GameClock_GetRawTickCounter` (`0032A150`)
(`0046ABD4`–`0046ABF5`); otherwise it writes a 32-byte entry `{ w_00 = event, dw_04 = tick,
q_08 = stats }` into the ten-entry ring at `02EBB560` (index `02EBB54C`, advanced mod 10,
`0046AC00`–`0046AC5D`) and calls `005369C0(stats, eventId)` (`0046AC66`), which reads the same
table's row — the display side, ~~unread (`FK-4`)~~ answered on 2026-09-11 under `FK-4`: four message-argument slots filled from the row bytes, with the text from `battle_message.bin` (superseded 2026-09-26 (FABLE, Claude Opus 5.5)).

## 3. Key addresses

| address | size | what |
|---|---:|---|
| `00390390` | 741 B | the steal roll; calculator slot 195 (`01EFABD8`) |
| `01EF96C0` | | the recipe pointer table; entry 49 = `01EFA198`, committed segment `[195]` |
| `00385F60` | 2,302 B | `BattleFormula_ResolveTargetResult` — the slot loop (`003863D0`), the copy to `+0x32`–`+0x34`, kind 6 |
| `003849B0` | 340 B | `BattleFormula_ResetScratchState` — zeroes the five scratch globals |
| `003847C0` | 273 B | `BattleFormula_BuildEvaluationContext` — the context this function receives |
| `00469EC0` | 1,904 B | `BattleFormula_DispatchPostResultEvents` — the only reader of result bit 23 (`0046A3D7`) |
| `0046AB10` | 371 B | the battle event poster: ring `02EBB560` (10 × 32 B, index `02EBB54C`), table `02EBF018`, then `005369C0` |
| `00379CD0` | | `RNG_MT19937_NextU32_Thunk` — the roll, the thunk of `RNG_MT19937_NextU32` (`00863BF0`) ([which roll is on which generator](../../21-RNG-And-Determinism/which-roll-is-on-which-generator.md)) |
| `0017D450` | 20 B | the console override, `[001D50D0() + 0xE5C]` |
| `0031B860` | 83 B | `BattleStats_FindOwningBattleUnit` |
| `02AEE04C`–`02AEE04E`, `02AEDFB8`, `02AEDFBC` | | the scratch globals |

## 4. Data structures and formulas

```
available(i) = row.w[0x32 + 2i] != 0xFFFF && (spawnRecord.b_14 >> i) & 1
if no slot authored, or an authored slot is unavailable:   result.dw_2C |= 0x800000 ; failed = 1
elif context.b_1C bit 1:   won[2] = r0 % 100 < 6  || ov == 2
                           won[1] = r1 % 100 < 30 || ov == 1
                           won[0] = r2 % 100 < 80 || ov == 0        ; independent; none -> failed
else:                      rare if r0 % 100 < 3  || ov == 2
                           else uncommon if r1 % 100 < 10 || ov == 1
                           else common   if r2 % 100 < 55 || ov == 0   ; first hit; none -> failed
```

## 5. Call chain

```
action 0xA9 (action_data.bin +0x08 = 49) -> recipe 01EF96C0[49] = 01EFA198, committed [195]
  -> BattleFormula_ResolveTargetResult 00385F60: ResetScratchState 003849B0 ; slot loop 003863D0
     -> calculator table 01EFA5C0[195] -> 00390390(_, targetStats, context)
        -> BattleStats_FindOwningBattleUnit -> unit +0xE60 (row) ; unit +0x6A0 (spawn record +0x14)
        -> RNG_MT19937_NextU32 x3 ; 0017D450 (console arm 243)
        -> 02AEE04C/4D/4E, 02AEDFB8, 02AEDFBC ; result +0x2C bit 23
     -> 02AEDFBC -> result +4 = 6 ; 02AEE04C/4D/4E -> result +0x32/+0x33/+0x34
  -> the applier 00311402 (three slots at +0x32 -> inventory, spawn record +0x14 bit cleared)
  -> BattleFormula_DispatchPostResultEvents 00469EC0: action 0xA9 & kind 6 -> event 0x33 / 0x34 (bit 23)
     -> 0046AB10 (ring 02EBB560, table 02EBF018) -> 005369C0 (display, unread)
```

## 6. Modding notes

- **The chances are literals in this function**: `6 / 30 / 80` with the flag, `3 / 10 / 55` without.
  A mod that changes steal rates patches these immediates.
- **"All three at once" is the flag branch's independence**, not a separate mechanic; the one-roll
  branch cannot give more than one item.
- **An enemy that was stolen from is "nothing to steal" until its spawn record is fresh again**,
  because the availability bits live on the spawn record and only a fresh spawn resets them.
- **Console arm 243 is a real override in the shipped binary**: the value at `+0xE5C` of the object
  `001D50D0` returns is consulted on every roll.
- **Giving another action a steal roll is a data edit**: set its `action_data.bin` recipe byte
  `+0x08` to 49 (or put 195 in another recipe's committed segment). The message side will not
  follow — the dispatcher's steal messages are keyed to action `0xA9` by an immediate.
- **The two failure messages are events `0x33` and `0x34`** of the table at `02EBF018`; the
  "nothing to steal" one is distinguishable in the result record by `+0x2C` bit 23 alone.

## 7. What is not known

- [x] ~~**Which accessory or effect sets `context.b_1C` bit 1** — the three-roll branch is the
  behaviour the Thief's Cuffs are known for, but the writer of that bit is not read here.~~ **FK-1**
  — answered 2026-09-11: `BattleFormula_BuildEvaluationContext` (`003847C0`) fills context
  `+0x1A`–`+0x29` with the **source's merged status / augment layers** — for every id `0..127`, bit
  `id & 7` of byte `+0x1A + (id >> 3)` when either the stats record's `+0x68` (status) or `+0x78`
  (augment) layer has it (`00384820`–`00384858`) — so `+0x1C` bit 1 is **id 17**: augment
  **Thievery** (the Thief's Cuffs) *or* status **Lure**, the two names id 17 carries in
  [the two-layer model](../../10-Status-Periodic-Terminal/Status-And-Augment-Layers/two-layer-effect-model.md)
  §3; the merge does not distinguish them.
- [x] ~~**Who copies `02AEE04C`–`02AEE04E` into the result record's `+0x32`–`+0x34`** that the
  applier reads, and what reads `02AEDFB8` / `02AEDFBC` (the message and the result flag `0x800000`'s
  consumer).~~ **FK-2** — answered 2026-09-11: the resolver, §2.4; the dispatcher and the event
  poster, §2.5.
- [x] ~~**What `001D50D0` returns** — the object whose `+0xE5C` is the console option — and whether
  arm 243 is reachable outside the developer console.~~ **FK-3 ANSWERED 2026-09-13 (FABLE):** `001D50D0` returns the parameter dispatcher's settings singleton: a `0x10E8`-byte object built on first use by `001CCB20` and cached at `01F81428` (`001D50DD`–`001D5106`). The constructor stores `−1` at `+0xE5C` (`001CCE1F`). A census of every `.text` access with displacement `0xE5C` finds only that store, arm 243's cycle in `001D1660` (`001D3B5F`–`001D3B97`), the arm's label lookup in `001CD0E0` (`001CFBDB`), the steal roll's reader `0017D450`, float reads in `001E8580` (object not typed here — **since typed, 2026-09-15 (SWE2-FRONTIER):** it is the glyph-run state object, `001E8580`'s 21-member family opened on [painting-a-line-of-text-into-a-render-target.md](../../99-Unresolved-Residual/Glyph-Run-Rendering/painting-a-line-of-text-into-a-render-target.md)) and a store in `001E9C80`, whose object is at least `0x237A` bytes and so not the singleton. And id 243 (`0xF3`) is not reachable: the dispatcher `001D1660` has one way in: the three-instruction adapter `001CD040` tail-jumps to it (`001CD049`), `001CD040` has one call site (`0017DD34` in `0017DB90`), and neither address is held in any data qword. `0017DB90` — called only by the Config screen's two row procs (`0023B3D0` in `0023B330`, `0023B84C` in `0023B6F0`) — passes the id as a literal `mov r8d` in each of its arms, and the arms carry exactly **16** ids: `0x86`, `0xA6`, `0x10A`, `0x110`–`0x119`, `0x11B`–`0x11D`. So the other 266 ids — every developer arm among them — are linked but issued by no code in the retail image. The override therefore stays at `−1` — no forced tier — in normal play; only a memory edit reaches it.
- [x] ~~**What `005369C0` (1,000 B) does with an event** — the text or effect events `0x33` / `0x34`
  produce, which file fills the table at `02EBF018`, and what the filter `00469570` (303 B) tests.~~ **FK-4** — answered 2026-09-11: the realiser, the filter and the table `battle_message.bin` ([the post-result events page](../../07-Combat-Action/Post-Result-Events/the-post-result-events-and-the-battle-message-table.md)).

## 8. Evidence

| claim | evidence | tier | confidence |
|---|---|---|---|
| The availability test and the "nothing" exit | `003903DB`–`003904A0` | 1 | PROVEN |
| The two branches and their thresholds | `003904A5`–`00390670`; immediates `6`, `0x1E`, `0x50`, `3`, `0xA`, `0x37` | 1 | PROVEN |
| The override is console arm 243 | `0017D454`–`0017D459` (`+0xE5C`); the catalogue's row 243 (`001D3B5B`, `rdi+0xE5C`) | 1 | PROVEN |
| Slot 195 of the calculator table | `.data` scan: the qword `00390390` at `01EFABD8` = `01EFA5C0 + 0x618`; no E8/E9 site (`check_caller_claims`, control 632) | 1 | PROVEN |
| Recipe 49 is the only recipe naming slot 195 | all 109 entries of `01EF96C0` decoded; entry 49 = `01EFA198`, segments `[]` / `[195]` | 1 | PROVEN |
| Action `0xA9` is the only action with recipe 49 | `action_data.bin` (`st2e`, 543 × 60 B) from the archive, `in` and `kr` copies: one record with `+0x08 == 49` | 1 (authored data) | PROVEN |
| The resolver's copy and kind 6 | `003867F1`–`0038680C`; `003866C1`–`003866CA`, `003866E7`–`003866EB` | 1 | PROVEN |
| The scratch reset | `003849BC`–`003849C2`, `00384A1C`–`00384A23`; called at `00386001` | 1 | PROVEN |
| Bit 23 has one reader | `.text` scan for `test [r+0x2C], 0x800000` / `test byte [r+0x2E], 0x80` / `bt [r+0x2C], 23`: `0046A3D7` only; control: the `or` at `0039048E` found | 1 | PROVEN |
| The two events and the poster's ring | `0046A3C4`–`0046A3F0`; `0046AB19`–`0046AC66` | 1 | PROVEN |
| What the events display | ~~**not established** (`FK-4`)~~ four message-argument slots filled from the row bytes, rows gated by a filter, text from `battle_message.bin` (`FK-4`, answered 2026-09-11; row restated 2026-09-26, FABLE, Claude Opus 5.5) | — | ~~UNKNOWN~~ PROVEN |

## 9. Related

- [`../../07-Combat-Action/applying-a-result-to-a-target.md`](../../07-Combat-Action/applying-a-result-to-a-target.md) — the applier's steal step.
- [`../../04-Actor-Entity/Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md`](../../04-Actor-Entity/Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md) — the steal words and the availability bits at spawn.
- [`../../05-Spawn-Encounter-Lifecycle/Spawn-Record/the-spawn-keep-entry-field-map.md`](../../05-Spawn-Encounter-Lifecycle/Spawn-Record/the-spawn-keep-entry-field-map.md) — `+0x14` on the record.
- [`../Recipe-System/ranged-weapon-recipes.md`](../Recipe-System/ranged-weapon-recipes.md) — the calculator table and the recipe lists.
- [`../../07-Combat-Action/Post-Result-Events/the-post-result-events-and-the-battle-message-table.md`](../../07-Combat-Action/Post-Result-Events/the-post-result-events-and-the-battle-message-table.md) — the two messages, decoded.
- [`../Current-HP/the-hp-write-and-the-lethal-transition.md`](../Current-HP/the-hp-write-and-the-lethal-transition.md) — `0046AB10` on the lethal path (`EY-3`).
- [`../../10-Status-Periodic-Terminal/Status-Write/the-status-write-and-its-side-effects.md`](../../10-Status-Periodic-Terminal/Status-Write/the-status-write-and-its-side-effects.md) — `0046AB10` for Stone and Vanished (`FA-3`).
- [`../../00-Engine-Core-Runtime/Developer-Tuning-Console/arm-catalogue-slice-H-ids-236-267.md`](../../00-Engine-Core-Runtime/Developer-Tuning-Console/arm-catalogue-slice-H-ids-236-267.md) — arm 243.

## 9. Falsification pass 1 — 2026-09-13 (OPUS)

**The route was re-derived end to end, from the image and the shipped archive, without reading the
prose — and every link of it holds.**

| link | measured |
|---|---|
| the slot index | `(01EFABD8 − 01EFA5C0) / 8` = **195** |
| what that slot holds | the qword is **`00390390`** |
| recipe 49's list | the pointer at `01EF96C0 + 49×8` is **`01EFA198`**, and its dwords are **`FFFFFFFF, 195, FFFFFFFF`** — an empty preview segment and a committed segment of exactly `[195]` |
| "no other recipe's segment holds 195" | all **109** lists decoded: slot 195 appears **once**, in recipe 49 |
| "action `0xA9` is the only record of the 543 with recipe byte 49" | `battle_pack.bin`'s `st2e` section decoded directly: **row 169 = `0xA9`, and it is the only one** |

The rolls are exact too, all six thresholds and both override ladders:

```asm
003904CD  cmp r8d, 6      ; rare      003905B8  cmp r8d, 3       ; rare
0039050A  cmp r8d, 0x1e   ; 30        003905E9  cmp r8d, 0xa     ; 10
00390546  cmp r8d, 0x50   ; 80        00390612  cmp r8d, 0x37    ; 55
          cmp eax, 2 / cmp eax, 1 / test eax, eax   ; the override's rare / uncommon / common
```

So does the modulo idiom §2.2 describes, verbatim and **six times** (three per branch):

```asm
003904BC  mov  eax, 0x51eb851f
003904C1  mul  r8d
003904C4  shr  edx, 5
003904C7  imul ecx, edx, 0x64
003904CA  sub  r8d, ecx
```

— as do the kind-1 owner test (`cmp byte ptr [rcx + 5], 1`) and the three "nothing to steal" word
tests at `[rdi + 0x32]`, `[rdi + 0x34]`, `[rdi + 0x36]`.

### The "no call site anywhere" claim, with a control that works

§2.1 says `00390390` has **no `call` or `jmp` site in the executable**. A direct-target census over
every function body in the graph (41,366 distinct targets collected) finds **0** for it — and the
control says the instrument is working rather than silent:

| function | direct `call`/`jmp` sites |
|---|---:|
| **`00390390`** (the claim) | **0** |
| `00385F60` `BattleFormula_ResolveTargetResult` | 7 |
| `003847C0` `BattleFormula_BuildEvaluationContext` | 2 |
| `0031B860` `BattleStats_FindOwningBattleUnit` | 136 |
| `00267E10` `VMValueStack_PopInt32CoerceFloat32` | 1,565 |

**And it generalises.** Of the **152 distinct** functions the 202-slot table holds, **151 have zero
direct call sites**: the table is the only route into 99 % of the calculators, not just this one.

### The single exception is the folded no-op — and 42 slots are empty

The one table entry with call sites is `0016D6A0`, the `ret 0` fold, and it occupies **42 of the 202
slots**. **This is not new**: [the native command lifecycle](../../01-Script-VM-Native-Bridge/Native-Command-Lifecycle/native-command-lifecycle.md)
already records "the same address filling 42 of its 202 slots" and reads it as `/OPT:ICF` folding.
It is recorded here because this pass reached it by a different route — a call-site census over the
table rather than an address scan — which makes it **an independent confirmation**.

> The consequence is worth stating in the table's own terms: **160 of the 202 slots hold a real
> calculator, over 151 distinct functions.** "202 slots, 152 distinct functions" is right about the
> addresses, and forty-two of those slots do nothing when a recipe names them.

### The branch bit is id 17, and two pages meet on one instruction

```asm
003904A5  test byte ptr [rsi + 0x1c], 2
```

Byte `+0x1C` of the evaluation context holds ids 16–23, so bit 1 is id **`8 × 2 + 1 = 17`** — which
[the evaluation context](../Evaluation-Context/the-evaluation-context-field-map.md) §2.3 names
**Lure / Thievery (Thief's Cuffs)**, listing this very site. That page reached the id from the
context's merge; this one reaches it from the roll that consumes it. **The accessory that makes
Steal roll three times and the Lure status are the same bit, by construction of the merge** — which
is why §6's modding note about the collision is a consequence of the layout rather than a
coincidence.

**Nothing was found wrong.** Every figure, address, threshold and structural claim this pass could
reach reproduced.

**Not claimed:** §2.5's message-id correction and its one-reader scan, the applier chain in §2.4,
and the console arm 243 mapping were not re-derived. Nothing was executed or observed live; the
archive figures come from the `us` copy under `work/repos-2d`.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. The image-address resolver fan-out is MECHANICAL and recorded in the registry.*

**The console override's singleton is not console-private.** `001D50D0` returns the parameter dispatcher's settings
object (FK-3), and callers well outside the console read it:

- **Presentation:** `CharacterRenderObject_SubmitMaterialsWithFad…` and four more bodies of 660–3,397 bytes;
- **Input:** `InputManager_TranslateBindingProfileToContro…` and two helpers (100 B and 105 B).

So the object that carries arm 243's steal override is also read by material submission and by binding translation. Which of its fields
those callers read is not read here. `001D50D0` itself reaches the 1,210-byte builder, and that builder asks the
**Platform** QPC timer (78 B).

**The console machinery the page cites has further edges:**

- `001D1660`, the console body, calls three Presentation console bodies and a 295-byte **Resource** helper. It also
  calls the console's two audio legs, which are recorded in the registry.
- The debug-menu renderer `001CD0E0` reads the achievement counters (**PlatformOnlineAchievements**;
  [the counters contract](../../20-Platform-Online-Achievements/CONTRACT-achievement-counters.md) §2 note). It also
  calls an 8-byte **Resource** getter and a 190-byte Presentation helper, and it is called by Presentation bodies of 251
  and 704 bytes.
- `001CD040` is the 14-byte forwarder into the console body.

**Other crossings:**

- **Party — CLIENT.** `BattleUnit_SeedPartyCombatStanceRecheckTimer` reads the raw tick counter. On the
  **Presentation** side, so do `PartyCombat_UpdateStanceState` and `BattleUnit_ComputePartyBattleStance`.
- **Items_Equipment_Shops_License, Rewards_Progression_Economy and Movement — CLIENT.** `BattleStats_FindOwningBattleUnit`
  is shared with the equipment and licence setters, the level-up path, `Reward_ComputeExperienceForRecipient` and two
  locomotion bodies. The event poster `0046AB10` has a 160-byte client that locomotion reaches.
- **Rewards_Progression_Economy — CLIENT.** The HP and MP growth functions draw the same gameplay MT as the steal roll.
  **A level-up therefore moves the steal stream.**

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page.*

**ActorEntity — SERVICE (2 edges).** `BattleStats_FindOwningBattleUnit` `0031B860` calls `BattleUnit_GetSlotCount` `00236850` and `BattleUnit_GetBySlotIndex` `00236820`. The owner lookup the steal roll uses to find the target's unit (stored in `02EBF188`) is a walk of the battle-unit table through that layer's two accessors.

**CoreRuntimeScheduling — SERVICE and CLIENT, MECHANICAL (5 edges).** The glyph-run body `001E8580` calls `001A1470`, a 93-byte bump allocator (size rounded to 16, cursor advanced, wrapped to the arena base when it would pass the end); `003939B0` calls `001EDE70`, a 7-byte getter of the global dword at `01F82E38`; the event poster `0046AB10` calls `GameClock_GetRawTickCounter` `0032A150`; and the boot frame `0022B6E0` and its sibling init frame `0022B7E0` each call `RNG_MT19937_NextU32_Thunk` `00379CD0` once. These are generic machinery (an allocator, a getter, the raw clock) under bodies this page cites for other reasons, plus two start-up frames that draw from the same generator as the roll — which only matters as a further consumer of the stream.

**RNG_Random_Selection — SERVICE, DEPENDENCY (3 edges).** The steal roll `00390390` calls `00379CD0`, and `RNG_MT19937_NextU32` `00863BF0` calls `RNG_MT19937_TwistState` `00866B90` and `RNG_MT19937_SeedState` `00866D60`. The three `% 100` draws of §2.2 come from the shared MT19937 stream, which seeds and twists itself inside that layer; every other consumer of the stream moves what the steal draws.

**Script_VM_Native_Bridge — CLIENT (2 edges).** The verb bodies `00354BF0` and `00355140` (57 and 29 bytes) call `00379CD0`. Script verbs draw from the same generator as the steal roll; that is fan-in on the shared stream, not a script route into the roll.

**Spawn_Encounter_Lifecycle — CLIENT (3 edges).** `SpawnKeep_RotatePersistenceBanksForAreaTransition` `00233780`, `Spawn_SelectAndPrepareAutomaticEntry` `00235720` and `SpawnEntry_GetElapsedTicksSinceLastDeath` `00235FB0` call `0032A150`. The spawn layer times deaths and respawns on the same raw clock the steal re-arm reads (§4's re-arm term); the clock is shared, the spawn timing is that layer's.

**Status_Periodic_Terminal — CLIENT (10 edges).** `0031B860` is called by `BattleUnit_ResolvePeriodicPrimaryResourceRecoveryStep` `002F9400`, `BattleStats_ChangeStatusAndProcessSideEffects` `0030E360`, `BattleStats_RemoveStatusesFromMaskAndRecompute` `0030F690`, `BattleStats_RecomputeDerivedStateAndAutoStatuses` `0030FED0` and `BattleFormula_BuildRuntimeCounterPeriodicHpCredit` `00386860`; `0032A150` by `BattleUnit_RecoverFromTerminalStatusSetIfClear` `00301140`, `BattleUnit_RunPeriodicCombatMaintenance` `00310DB0` and `BattleFormula_ApplyGlobalPeriodicDrainModes` `00385CA0`; `00379CD0` by `BattleFormula_AdvanceStatusTimersAndBuildResult` `00386C70`; and `00310DB0` calls the resolver `BattleFormula_ResolveTargetResult` `00385F60`. The status layer shares the owner lookup, the raw clock and the generator with the steal roll, and its periodic tick drives the same slot resolver that runs calculator slot 195 — so a periodic status draw also advances the steal stream.

**WorldAreaField — SERVICE and CLIENT (7 edges).** The debug-menu renderer `001CD0E0` calls `FieldData_GetVariable0` `00265270` and `WorldTransition_GetTransitionFieldId` `00314910`; `005369C0`, which the event poster calls with the event id, calls `MapRef_GetAreaArdFieldResourceIndex` `00264ED0` and `WorldTransition_GetActiveOrPendingFieldId` `003148F0`; `BattleSystem_RunFieldFrameOrchestrator` `00234590` calls `0032A150`; the weather transition chooser `0025ABA0` and `0025ACA0` call `00379CD0`. The steal message's poster passes through a body that asks for the current field id and its area resource index, the console's debug-menu renderer reads field state, and the field frame and the weather transition roll are further consumers of the clock and the generator.

## SWE2-EC7-107 update (2026-09-20) - `0023B530` measured

`0023B530` (402 B) is the
`0x100`-byte message composer
`0023B330` and `0023B6F0` call:
`ecx - 1` indexes a `0x16`-entry
jump table (byte index at
`r14 + 0x11B6D8` selects a dword
offset at `r14 + 0x11B6C4`);
arms clear two `0x100` buffers,
resolve names through `0017FDC0` /
`0017FF20` and the `0x24`-stride
dword table at `r14 + 0x7F4900`
via `002F9860`, then
format through `002B4090(0x100,
rdx, name, ebx)` into the caller's
buffer - the text arm the steal
roll shares. Out-of-range `ecx`
answers 0.
Interior anchor `0023B575` (the
jump-table load).

## SWE2-EC7-108 update (2026-09-20) - `002B5AB0` measured

`002B5AB0` (171 B) is the
word-table text encoder `0023B530`
and `003939B0` call: `0039C4A0()`
resolves the charset record and
`0020E600(dword[+0x14])` its word
table; each of `r8d` source bytes
maps through
`word[table + (cl - 0x20) * 2]` -
a space (`0x20`) emits byte `4`,
an encoded word emits its low byte
plus its high byte when
`(dx - 0x20) > 0xDF` - and the
answer is the total emitted width
in `ebp`.
Interior anchor `002B5B08` (the
`word[r10 + rcx*2]` table read).
