---
system: The periodic combat tick — what it runs, what it drains, and what ends a status
category: 10-Status-Periodic-Terminal
status: AUDITED
owner_layer: CodeDomain — Battle; no PrimaryOwner recorded for the tick
evidence_tier: 1
verified_against:
  gzf_sha256: fb9b5e7ea002c1626a53d47da0b0b69a2443e246f7ce2b64329be4e034a2d3f7
  snapshot_sha256: a9cead8777597cdca58f2a47f27153f5231d60ad2bc16c3da9df8253820b09bd
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity - every function this document cites has byte-identical per-function records in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: 19 cited function entries, 0 of them among the 128 records that changed across GN158..GN161 (check_delta_additivity.py, check_transfer_eligible.py); re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS-REQ-FABLE-PROVENANCE-TRANSFER-144 (9bedb5e0); re-targeted GN160 -> GN161 under EVIDENCE-STANDARD addendum 2026-09-14bh
    previously: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708 (GN160), superseded 2026-09-14
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  parent_tag: GN159
last_reviewed: 2026-09-03
audit:
  passes: 1
  last_pass: 2026-09-12
  last_pass_state: opus-what-the-periodic-tick-does-pass-1
  crossref_clean: true
  reopened_count: 0
---

# The periodic combat tick — what it runs, what it drains, and what ends a status

> Companion to [two-layer-effect-model.md](../Status-And-Augment-Layers/two-layer-effect-model.md),
> which establishes the two 128-bit effect layers at BKBI `+0x68` and `+0x78`. **That document covers
> how a status is *stored* and *merged*. This one covers what happens to it every tick.**

## 1. What the player sees

Poison chipping your HP at a steady beat. Regen trickling it back. A Slow that runs out on its own
while you are still fighting. **All three are the same function running once per unit per frame**, and
~~the beat you can feel is a single remainder test — the drain only lands on ticks that divide evenly
into an interval the game computes from one global.~~ each status's beat is its own countdown. It is reloaded from the
status's `status_data +9`, and lasts `+9` / 10 seconds: Poison 12 s, Sap 0.1 s, Regen 1.5 s. The remainder test on one
global belongs to the field drains of stage 4 (a third of a second). *(Corrected 2026-09-29, FABLE, Claude Opus 5.5;
`_index/candidates/pkg-gp-status-poison/beat.py`.)*

## 2. ~~Nothing happens at all unless six gates pass~~ Three gates stop everything, four more skip to the tail (OPUS, 2026-10-02)

`BattleUnit_RunPeriodicCombatMaintenance` (`00310DB0`, 1,338 B) spends its first ninety instructions
refusing to run:

| gate | test |
|---|---|
| the unit has a stats block | `[unit + 0x698] != 0` |
| a global mode is not 5 or 6 | `(mode - 5) > 1` |
| the field permits action | `FieldData_GetActiveFieldRecordBit15()` returns 0 |
| *(added 2026-10-02, OPUS)* the actor manager is ready - fails to the tail | `00265680()` is non-zero (`00310F12`-`00310F19`) |
| no global target suppression | `BattleTarget_ComputeGlobalEligibilityMask()` is 0 |
| no per-unit suppression | `BattleTarget_ComputeUnitEligibilityMask(unit, 0)` is 0 |
| a 64-bit unit flag is clear | `!(unit->qwFlags & 0x1000000000)` |

*(Corrected 2026-10-02, OPUS - section 14, the tick after its first apply: only the first three gates stop everything (they exit to `003112D1`). The readiness probe, the two masks and the flag exit to the common tail `003112A1`, which still runs the enmity decay `00321530` and `002FE950`. Between gate 3 and the probe, a party Esper record whose HP is gone or whose summoner is unavailable is dismissed (`003138D0(0)` at `00310EF8`), and then nothing else runs.)*

**And a deadline check that is not a gate but an expiry**, run before any of them:

```asm
00310DEF  call  GameClock_GetRawTickCounter
00310DF4  cmp   dword ptr [rsi + 0xdd0], eax    ; a stored deadline tick
00310DFA  jae   0x310e02
00310DFC  and   dword ptr [rsi], 0xbfffffff     ; ~0x40000000 — clear the bit
```

**`unit + 0xDD0` is a tick deadline, and passing it clears flag bit `0x40000000`.** A timed unit flag
that expires on the clock rather than on a counter, checked whether or not the rest of the tick runs.

**A seventh sighting of the functional predicate.** The same
`((status0 | status1) & 0x80000003)` test with the `FieldRecordBit15` waiver appears here at
`00310EE6`, in a block guarded by a combatant-type range check (`(type - 0x1B) <= 0xC`).

## 3. The tick body is a five-stage pipeline, then the ordinary action path

Once the gates pass, the tick zeroes a **`0x148`-byte result record** on its stack and fills it:

```asm
00310F6C  mov   r8d, 0x148
00310F7A  call  memset                            ; the result record, 328 bytes
00310F8B  call  BattleFormula_BuildPeriodicStatusResult
00310FAC  call  BattleFormula_ApplyTargetResult    ; (result, 0, bkbi, 0xFFFF, 0)
```

> **Poison damage is not a special case anywhere in the engine.** The tick builds a result record and
> hands it to `BattleFormula_ApplyTargetResult` — **the same function that applies the outcome of a
> sword swing.** Statuses ride the ordinary damage path; only the *builder* differs.

`BattleFormula_BuildPeriodicStatusResult` (`00385DF0`) is 83 bytes and is a pure sequencer — five
calls, same two arguments, in a fixed order, with the last as a tail call:

```c
BattleFormula_InitializeResultRecord(result, 0, bkbi);   /* 003848E0 */
BattleFormula_AdvanceStatusTimersAndBuildResult(bkbi, result);   /* 00386C70, 935 B */
BattleFormula_AdvanceStatusLinkedAuxTimers(bkbi, result);        /* 00385570 */
BattleFormula_ApplyGlobalPeriodicDrainModes(bkbi, result);       /* 00385CA0 */
return BattleFormula_BuildRuntimeCounterPeriodicHpCredit(bkbi, result);  /* 00386860 */
```

**Every tick runs all five stages for every eligible unit.** There is no per-status dispatch table and
no "does this unit have poison" short-circuit at this level — the stages themselves decide.

## 4. What ends a status: a countdown, one step per tick

> **Scope, corrected 2026-09-29 (FABLE, Claude Opus 5.5; `PKG-GP-STATUS-POISON` Q4).** This section is stage 3: the eight
> effect-slot timers `+0x17C` of the **effect layers**. The 32 battle statuses (Poison, Slow and the rest) end through
> stage 2's duration `+0xBC[s]`, as the 2026-09-12 correction below establishes. Read "status" in this section as
> "effect-layer id".

`BattleFormula_AdvanceStatusLinkedAuxTimers` (`00385570`, 262 B) is the expiry mechanism, and it reads
**both** effect layers:

```asm
003855CD  test  byte ptr [rax + r14 + 0x68], dl   ; layer 0 — inflicted statuses
003855D4  test  byte ptr [rax + r14 + 0x78], dl   ; layer 1 — derived statuses
003855D9  je    skip                              ; neither -> this id is not present
          ...resolve the status's authored record...
00385619  movzx edx, byte ptr [rcx + 6]           ; the record's timer-slot index
0038561D  cmp   edx, 0xff
00385623  je    skip                              ; 0xFF = this status never expires
00385625  movzx ecx, word ptr [r14 + rdx*2 + 0x17c]  ; the live timer
0038562E  test  cx, cx
00385631  jle   skip                              ; already run out
00385636  dec   ecx                               ; ONE step per tick
0038563A  jg    keep
0038563C  mov   byte ptr [rdi + rsi + 0x3e], bl   ; reached zero -> append this status id
00385640  inc   rdi                               ;                 to a list in the result
00385645  mov   word ptr [rsi + rdx*2 + 0x42], cx ; write the new timer into the result
```

Four things this fixes exactly:

- **Timers are per status, live at `statsRecord + 0x17C + slot*2`, `u16`** (the `BattleStatsRecord` behind unit `+0x698` — corrected 2026-09-11 from "unit"; the unit's own `+0x17C` is a float), and the slot index is authored —
  it is a byte at `+6` of ~~the status's own record~~ the id's row in the effect table `02EBF040`, not of `status_data` (whose `+6` is the flag word) *(corrected 2026-10-02, OPUS: `00385585`, `003855FD`–`00385604`; §13's 2026-09-12 correction)*, not the status id.
- **`0xFF` in that byte means "no timer"** — the status is permanent until something removes it.
- **One decrement per tick, unconditionally**, for every status the unit holds in either layer. There
  is no rate field: every timed status ticks at the same speed and the *duration* is the start value.
- **Expiry does not remove the status here.** The id is appended to a list at result `+0x3E` and the
  zeroed timer written to result `+0x42 + slot*2`. **Removal is the apply stage's job**, which is why
  a status wearing off looks identical to one being cured — both arrive through
  `BattleFormula_ApplyTargetResult`.

## 5. The beat: the drain fires only on an exact interval

`BattleFormula_ApplyGlobalPeriodicDrainModes` (`00385CA0`, 336 B) gates itself on a remainder:

```asm
00385D78  call  GameClock_GetRawTickCounter        ; -> r8d
00385D7D  imul  ecx, dword ptr [rip + 0x1A78330], 0x1e ; [01DFE0B4] x 30 -- the frame base (corrected 2026-09-12)
00385D87  mov   eax, 0xaaaaaaab
00385D8C  mul   ecx
00385D95  shr   ecx, 1                             ; /3   -> interval = global * 10
00385D97  div   ecx
00385D99  test  edx, edx
00385D9B  jne   done                               ; remainder != 0 -> nothing this tick
00385D9D  or    dword ptr [rdi + 0x2c], 0x4000     ; interval reached: set the result flag
```

**The interval is `[01DFE0B4] × 30 / 3` = `frame base × 10` ticks**, and the drain lands only when the
raw tick counter is an exact multiple of it. That is the beat a player feels.

> **Corrected 2026-09-12 (FABLE).** The earlier text read the instruction's displacement
> (`0x1A78330`) as the global's address. Resolved from the instruction, the operand is **`01DFE0B4`**
> — the frame-base word, 1 at 30 fps and 2 at 60 ([the boot page](../../00-Engine-Core-Runtime/what-the-engine-fixes-at-boot.md)). So the beat is
> **10 ticks at 30 fps and 20 at 60: a third of a second either way**, and there is no separate
> drain-interval tunable; the same word scales every status duration and beat on
> [the status write](../Status-Write/the-status-write-and-its-side-effects.md) §2.4a.

### The amount is stored negative, and the divisors are negative

```asm
00385DAE  movsx ecx, word ptr [rbx + 0x28]
00385DB2  cmp   ecx, 0x32                          ; needs to be at least 50
00385DB5  jl    fallback
00385DBC  mov   eax, 0xae147ae1
00385DC1  imul  ecx
00385DC3  sar   edx, 4                             ; -> ecx / -50
00385DCD  mov   word ptr [rdi + 0x2a], dx          ; the per-interval delta
```

`0xAE147AE1` with `sar 4` computes **`v / −50`**, and the same magic with `sar 5` (used earlier, into
result `+0x24`) computes **`v / −100`**. Both were checked against integer division across ±20,000
sampled values, **with a control against 101 that fails** — and the sign is the point:

> **The divisors are negative, so the stored delta is a loss, not a magnitude with a sign applied
> later.** A drain of one-fiftieth is written as `v / −50` directly into the result record.

The `≥ 50` guard means a source value below fifty produces a **fallback** written from a different
register rather than a rounded-to-zero drain. ~~**What the field at `+0x28` is has not been
established**, so "one-fiftieth of *what*" is not claimed here.~~ *(answered: see §10 and §13 "Still not established" — the base is the stats record and `+0x28` is max MP, resolved 2026-09-11; 2026-10-02, OPUS)*

## 6. What refuses a status on the way in

`BattleStats_ChangeStatusAndProcessSideEffects` (`0030E360`, 1,323 B) is the application entry. Before
any layer is touched it computes:

```asm
0030E404  mov   eax, dword ptr [rsi + 0x3c]
0030E407  or    eax, dword ptr [rsi + 0x64]        ; the unit's two status words  <- corrected 2026-10-02, OPUS: rsi is the target's stats record, which holds them (§13)
0030E410  shl   edi, cl                            ; 1 << status id
0030E412  test  edi, eax                           ; already present?
0030E42C  call  BattleTarget_HasLow16EligibilitySuppression
0030E433  jne   refuse
0030E44B  call  BattleTarget_HasHigh16EligibilitySuppression
0030E454  test  edi, 0x80000003                    ; ...and the status is one of these
0030E45A  jne   refuse
```

**Two independent suppression checks stand in front of every status application**, and the second only
refuses when the status being applied is itself in the `0x80000003` set — **an eighth sighting of that
mask, and the first where it selects which status is blocked rather than whether a unit may act.**

The caller also passes a mode (~~`0`–`3`~~ `0`–`5` *(corrected 2026-10-02, OPUS: `0030E4CB cmp eax, 5` / `ja`)*) and a flags word whose **bit 1** and **bit 4** are each
inverted into a local — two independent "do not suppress" switches supplied by the caller.

## 7. Key addresses

| Address | Name | Body | Role |
|---|---|---:|---|
| `00310DB0` | `BattleUnit_RunPeriodicCombatMaintenance` | 1,338 B | the tick: gates, build, apply |
| `00385DF0` | `BattleFormula_BuildPeriodicStatusResult` | 83 B | the five-stage sequencer |
| `00386C70` | `BattleFormula_AdvanceStatusTimersAndBuildResult` | 935 B | stage 2 — read whole on [the status write](../Status-Write/the-status-write-and-its-side-effects.md) §2.4a: the 32 statuses' own durations and beats (§13, corrected) |
| `00385570` | `BattleFormula_AdvanceStatusLinkedAuxTimers` | 262 B | stage 3 — the countdown |
| `00385CA0` | `BattleFormula_ApplyGlobalPeriodicDrainModes` | 336 B | stage 4 — the interval and the drain |
| `00386860` | `BattleFormula_BuildRuntimeCounterPeriodicHpCredit` | 485 B | stage 5 — the conditional credit (§13) |
| `0030E360` | `BattleStats_ChangeStatusAndProcessSideEffects` | 1,323 B | application and refusal |
| `0030B9B0` | `BattleTarget_HasLow16EligibilitySuppression` | 116 B | first refusal gate |
| `0030B8E0` | `BattleTarget_HasHigh16EligibilitySuppression` | 109 B | second refusal gate |

### The `00310DB0` exclusive subtree — all 7 members bound (SWE2-FRONTIER, followup queue)

The exclusive-callee census assigns the periodic tick **7 frontier functions**. Interior cites
are one instruction inside each declared extent (`interior_cite.py scan`; no boundary
crossings).

| cluster | members | role | interior |
|---|---|---|---|
| status result | `00385DF0` `BattleFormula_BuildPeriodicStatusResult` (83 B) | the five-stage sequencer §3 describes: `003848E0`, `00386C70`, `00385570` (the per-status loop), `00385CA0`, tail `00386860` | `00385E08` (`call 003848E0` — stage 1) |
| owner lookup | `0031E800` `BattleStats_GetOwningActorHandle` (91 B) | scans `00236820(i)` records for `[rec+0x698] == arg` across the `00236850` count, returns `[rec+8]` — the unit that owns a stats block | `0031E82C` (`cmp [rax+0x698], rdi` — the match) |
| enmity decay | `00321530` `BattleEnmity_UpdatePeriodicDecay` (142 B) | `+0x698`-gated (`[rec+5]==1`): the counter byte at `[[+0x6A0]+0x19]` increments until it reaches `cvttss2si([01DFE0B8] × [008F8D80])` — the frame-scaled decay threshold — then `00321D30(unit, −0xA, 0)` resets the row | `00321587` (`mulss xmm0, [008F8D80]` — the rate mul, constant 30.0f) |
| combatant writes | `00321D30` `BattleEnmity_WriteAllCombatantIds` (141 B) | the 0x28-slot loop the decay reset calls: per slot, `+0x6A0`/`+0x698` records present and `([+0x64] | [+0x3C]) & 0x80000003` nonzero → `00313F60` gate → `00321850(unit, slot, edx, r8)` | `00321D9C` (`call 00321850`) |
| world pickups | `00319830` `Loot_RemoveWorldPickupByIndexWithoutGrant` (26 B), `00319A00` `Loot_CollectWorldPickupByIndex` (26 B) | twin index adapters: `idx × 0x60` into the ~~`02EB0FA0`~~ `02EC0FA0` *(corrected 2026-10-02, OPUS: `0031983B`, `00319A0B`)* pickup table, tail to `003197B0` (remove) / `00319920` (collect-grant) | `00319833` / `00319A03` (`lea rcx, [rax+rax*2]` — the ×0x60 index) |
| kind-8 dispatch | `00469E30` (73 B) | builds a `0x28` stack block; when ~~`002F8E90(unit)`~~ `002F8E90(stats)` *(corrected 2026-10-02, OPUS: the tick passes the stats record, `00311114`)* returns 8, `0046AB10(unit, 0x4E, &block)` — ~~the kind-8 periodic-effect spawn~~ a post through the battle event poster *(corrected 2026-10-02, OPUS: the status write §2.6 row 5 names `0046AB10` the battle event poster; §13 "Still not established" ties category 8 to the post-result "steals your loot" message)* | `00469E5E` (`cmp eax, 8`) |

`00322C50`/`0020E600`/`00307CE0`/`00236820`/`00236850`/`00313F60`/`00321850`, the
`0038xxxx` stage helpers, `003197B0`/`00319920`, `002F8E90`, `0046AB10` are shared
callees — deliberately not census members.

## 8. Call chain

```
BattleUnit_RunPeriodicCombatMaintenance 00310DB0
  gates: [unit+0x698], mode != 5|6, FieldRecordBit15, global+unit eligibility masks, qwFlags 0x1000000000
  expiry: tick >= [unit+0xDD0]  ->  clear flag 0x40000000
  memset(result, 0, 0x148)
  -> BattleFormula_BuildPeriodicStatusResult 00385DF0
       -> BattleFormula_InitializeResultRecord            003848E0
       -> BattleFormula_AdvanceStatusTimersAndBuildResult 00386C70
       -> BattleFormula_AdvanceStatusLinkedAuxTimers      00385570   (per-status countdown)
       -> BattleFormula_ApplyGlobalPeriodicDrainModes     00385CA0   (interval + drain)
       -> BattleFormula_BuildRuntimeCounterPeriodicHpCredit 00386860 (tail call)
  -> BattleFormula_ApplyTargetResult 003112F0             the ordinary action apply path
```

## 9. Modding notes

- **A status's duration is its starting timer value** — for the 32 statuses of the status words,
  the dword at `statsRecord + 0xBC + id*4` that stage 2 spends 10 per tick (`status_data +8` ×
  Vitality factor × frame base × 300, [the status write](../Status-Write/the-status-write-and-its-side-effects.md) §2.4a); for the effect-table timers, the word at
  `statsRecord + 0x17C + slot*2` that stage 3 spends one per tick (corrected 2026-09-12; "unit" until
  2026-09-11). Neither has a rate field: duration is entirely in the number you start with.
- ~~**A status record whose byte `+6` is `0xFF` never expires.**~~ **An effect id whose effect-table row (`02EBF040`) has byte `+6` = `0xFF` has no stage-3 timer**; in the shipped table only rows 55, 56 and 57 carry a slot (3, 4 and 5) *(corrected 2026-10-02, OPUS: `003855FD`–`00385604`; checked against `battle_pack.bin` slot 29)*. That is the difference between a timed
  ailment and a permanent one, and it is one authored byte.
- **The drain beat is `frame base × 10` ticks** — a third of a second at either frame rate. The
  word is `01DFE0B4`, the frame base itself (corrected 2026-09-12), so it is not a drain tunable:
  changing it changes every timer in the game. Poison, Sap and Regen have their own beats besides
  (`status_data +9`, on the status-write page).
- **Hook `BattleFormula_ApplyTargetResult` and you see everything** — swings, spells, poison ticks and
  statuses wearing off all arrive there. Hooking the tick alone misses cures; hooking the apply misses
  nothing.

## 10. What is not known

- [x] ~~Stages 2 and 5 are not read.~~ **Read — see §13.** ~~Stage 2 advances **no** duration timer
      despite its name~~ — **corrected 2026-09-12:** stage 2 advances the 32 statuses' own durations
      and beats through a record-relative address (§13, last block); **stage 3 is the only decrementer
      of the `+0x17C` array**, and stages 2 and 5 ~~accumulate~~ write the HP delta besides, stage 5 by overwriting it (`00386A23`) *(corrected 2026-10-02, OPUS)*.
- [x] ~~**What the field at `+0x28` is**, so the `/−50` drain is "one fiftieth" of an unnamed quantity.~~
      **Resolved 2026-09-11 in §13:** the base is the stats record and `+0x28` is max MP.
- [x] ~~What the two suppression gates test.~~ **Read — see §13.** They are one shape on **two halves
      of a packed 32-bit eligibility mask**, with the variant chosen by
      `BattleTarget_ClassifyRelationshipClass`.
- [x] ~~Which global sits at `01A78330` and sets the drain interval.~~ **ANSWERED 2026-09-12 (FABLE):**
      none — `0x1A78330` was the displacement; the operand is `01DFE0B4`, the frame base (§5).
- [x] ~~What flag `0x40000000` on a unit means, and what sets the deadline at `unit + 0xDD0`.~~
      **ANSWERED 2026-09-12 (FABLE):** a timed **post-recovery mark** — set with its deadline by
      `BattleUnit_RecoverFromTerminalStatusSetIfClear` (`003012AD`, `003012DB`), cleared by this tick
      when the deadline passes, and consumed by exactly one reader: the presentation builder
      `002F6AB0` (`002F701D`), which while the bit is set stores its `r8` argument into the unit's
      `0xE0`-byte presentation entry (index word `+8` into `[rsi + 0x1D0]`) at `+0xC0`
      (`002F7025`–`002F7037`). An image-wide sweep for every test, set or clear of bit 30 on a dword
      at displacement 0 finds exactly those three sites (`002F701D`, `003012AD`, `00310DFC`).
- [x] ~~The layout of the `0x148` result record beyond `+0x24` (**the HP delta accumulator, §13**),
      `+0x2A`, `+0x2C`, `+0x3E`, `+0x42` and `+0x140`.~~ **ANSWERED by cross-reference 2026-09-12:**
      [the result-record field map](../../07-Combat-Action/Result-Record/the-result-record-field-map.md) — `+0x24` the HP value, `+0x2A` the target MP value, `+0x2C` flag word A, `+0x3E`
      the four status-layer effects to clear, `+0x42` the eight timers, `+0x140` flag word C.

## 11. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| The tick's six gates and the deadline expiry | complete decode of `00310DB0`'s first 90 instructions | 1 |
| The result record is `0x148` bytes | `mov r8d, 0x148` into `memset` at `00310F6C` | 1 |
| Poison uses the ordinary apply path | `BattleFormula_ApplyTargetResult` called directly by the tick at `00310FAC` | 1 |
| The five-stage pipeline and its order | `00385DF0` decoded in full — 83 bytes, five calls, last is a tail call | 1 |
| Timers are `u16` at `statsRecord+0x17C + slot*2` (the record behind unit `+0x698`; "unit" until 2026-09-11), slot from record `+6`, `0xFF` = none | complete decode of `00385570` | 1 |
| One decrement per tick; expiry appends the id to the result | `dec ecx` and the `[rdi+rsi+0x3e]` store in the same block | 1 |
| The interval is `frame base × 10` | `imul …, 0x1E` then the `0xAAAAAAAB`/`shr 1` divide-by-3, then `div`/`test edx,edx`; the operand resolved by the disassembler from `00385D7D` (rip `0x1A78330` → `01DFE0B4`), 2026-09-12 | 1 |
| Stage 2 advances the 32 statuses' durations and beats | `00386C70` read whole on the status-write page §2.4a — `record + (target − record + 0x60)` addressing, `00386CA9`–`00386CB2`, `00386CEB`, `00386E3E`, `00386EE4` | 1 |
| Bit 30 has exactly one reader | capstone sweep of `.text` for `test` / `and` / `or` / `bt` with `0x40000000` (or bit 30) on a displacement-0 memory operand: three hits, the set, the clear and `002F701D` (2026-09-12) | 1 |
| Stage 5's ramp and its refusal on a perceived foe | `003868F1`–`00386A2C` read whole; `002F8E70` = `002F8E90(BattleStats_GetOwningRecord(unit)) & 7`; the `+0xBC4` / `+0xBC8` writers from the unit census | 1 |
| Stage 5's two tables are one 64-byte-record array | `00386885` `lea 0208D494` indexed by the type byte `+4` for kind-0 records; `003868AD` `lea 0208DE94` = `0208D494 + 40 × 64`, indexed by the owning unit's slot index `+0xEA9`; ~~index `0x14`~~ the raw pointer value `0x14`, not an index, when no owner (`003868BD`; read through at `003869A2`) *(corrected 2026-10-02, OPUS)* | 1 |
| The drain divisors are `−50` and `−100` | `0xAE147AE1` with `sar 4` / `sar 5` evaluated against integer division over ±20,000 values, **control against 101 fails** | 1 |
| Two suppression gates refuse an application | both calls and both `jne refuse` edges decoded in `0030E360` | 1 |

**Controls.** The absence claim is *"the tick has no per-status dispatch"*: the same reading that
finds five sequential calls in `00385DF0` finds the per-status **loop** in `00385570`, so the flat
sequence at the top level is a measurement rather than a missed table. The divisor claims each carry a
failing control on an adjacent divisor, because **a magic constant identifies a family and only the
shift picks the member.**

**Checked before starting:** `check_already_answered.py` on `00310DB0`, `00385570`, `00385CA0`,
`0030EA40`, `00300140` returned **no citing document** for any of them; `0030E360` and `00301140`
appear only in a field-record document and the address index. The register's one hit, **AH-9**, is an
audit-pass row on the two-layer document, not an answer to any question here.

## 12. Related

- [../Status-And-Augment-Layers/two-layer-effect-model.md](../Status-And-Augment-Layers/two-layer-effect-model.md)
  — the two 128-bit layers this tick reads at `+0x68` and `+0x78`
- [../../09-Combat-AI-And-Gambits/gambit-evaluation-and-enmity.md](../../09-Combat-AI-And-Gambits/gambit-evaluation-and-enmity.md)
  — the same `0x80000003` predicate and `FieldRecordBit15` waiver, and the enmity decay that is the
  other periodic loop in battle

## 13. Reopened 2026-09-03 — stages 2 and 5 read, and the two suppression gates

Section 10 filed three unknowns. Two are answered, and the answer to the first corrects a working
name.

### ~~Stage 2 does not advance the duration timers~~ — and the name says it does *(heading struck 2026-09-29, FABLE: stage 2 is the 32 statuses' timer; see "Corrected 2026-09-12" below)*

`BattleFormula_AdvanceStatusTimersAndBuildResult` (`00386C70`, 935 B) was left unread with the open
question *"are stage 2's timers the same timers stage 3 decrements?"* — filed rather than assumed,
because both names say "timers".

~~**They are not the same, and stage 2 does not touch the duration array at all.**~~ **They are not the same arrays, but stage 2 does reach the duration array**: it addresses the target's `+0xBC[s]` through `r14` (`00386EEC`) and writes the result's `+0xDC[s]` word array through `r15` (`00386E84 mov word ptr [r15], ax`) *(corrected 2026-10-02, OPUS: see "Corrected 2026-09-12" below; only the heading had been struck)*. Scanning all three
stages for the timer array's displacement, **with stage 3 as its own positive control**:

| stage | touches `0x17C` | writes a `[base + idx*2]` word array | accumulates into result `+0x24` |
|---|---|---|---|
| 2 — `AdvanceStatusTimersAndBuildResult` | **no** | ~~none~~ result `+0xDC[s]` through `r15` (`00386E84`) *(corrected 2026-10-02, OPUS)* | **yes** |
| 3 — `AdvanceStatusLinkedAuxTimers` | **yes** | `0x17C` and `0x42` | no |
| 5 — `BuildRuntimeCounterPeriodicHpCredit` | **no** | none | ~~**yes**~~ **overwrites** it (`00386A23`) *(corrected 2026-10-02, OPUS)* |

> **Stage 3 is the only decrementer of ~~status durations~~ the `+0x17C` array in the whole pipeline.** The control matters:
> the same scan that reports "no" for stages 2 and 5 reports `0x17C` and `0x42` for stage 3, so the
> zeros are measurements — **of that displacement.** See the correction at the end of this section:
> stage 2's own arrays sit at `+0xBC` / `+0x13C` and are reached through a record-relative address
> no displacement scan can see.

**What stage 2 actually does is accumulate a per-status delta.** It reads the combined status words
~~`[unit+0x3C] | [unit+0x64]`~~ `[stats+0x3C] | [stats+0x64]` of the stats record, not the unit *(corrected 2026-10-02, OPUS: "Still not established" below and CONTRACT-periodic-tick.md §5)*, and per status either decrements the result accumulator or subtracts a
unit field from it:

```asm
00386D96  dec   dword ptr [rbx + 0x24]            ; rbx = the RESULT record
00386DA2  mov   ecx, dword ptr [rsi + 0x3c]
00386DA5  or    ecx, dword ptr [rsi + 0x64]       ; rsi = the UNIT  <- corrected 2026-10-02, OPUS: rsi is the stats record, not the unit (see below)
00386DC0  mov   eax, dword ptr [rsi + 0x24]
00386DC3  bt    ecx, 0x1c                         ; status bit 28...
00386E18  neg   eax
00386E1A  add   dword ptr [rbx + 0x24], eax       ; ...subtract it from the accumulator
00386E1D  or    dword ptr [rbx + 0x140], 0x4000
```

~~**`AdvanceStatusTimers` is a misleading working name for this body.** It advances no timer this
document can find; it builds the delta. The name is GFZ type work and is left as-is here, but a reader
should not take it as evidence of what the function does.~~ *(Struck 2026-09-29, FABLE, Claude Opus 5.5: the name is
right. Stage 2 advances the 32 statuses' duration and beat through computed pointers, and builds the HP delta too; see
the 2026-09-12 correction below.)*

### Result `+0x24` is an accumulator, and three stages write it

Section 5 recorded the drain writing `result + 0x24` and could not say what it was. It is the **HP
delta accumulator**, and ~~**stages 2, 4 and 5 all add into it**~~ **stages 2 and 4 add into it and stage 5 overwrites it**: `00386A23 mov dword ptr [r13 + 0x24], edx` whenever its gates pass and the counter is a multiple of `fb × 30`, storing 0 when the beat count is below 10 (`003869AF jl 003869EB`), so the stage order matters for `+0x24` *(corrected 2026-10-02, OPUS: checked at `00386A23`)*; stage 3 never does. Its flag words are
`+0x2C` (stages 2, 4, 5) and `+0x140` (stage 2).

> **A caution for anyone reading these bodies: `+0x24` appears on two different bases.** `[rbx+0x24]`
> and `[r13+0x24]` are the result accumulator; `[rsi+0x24]` and `[rdi+0x24]` are a field of the unit's
> stats block. **The same displacement on two structures in one function is exactly the shape that
> produces a confident wrong reading**, and the two are told apart only by which register is live.

### Stage 5 is a conditional credit with its own blocking bits

`BattleFormula_BuildRuntimeCounterPeriodicHpCredit` (`00386860`, 485 B) refuses far more often than it
fires:

```asm
00386881  movzx ebx, byte ptr [rcx + 4]      ; a type byte selects a 64-byte record
0038688C  shl   rbx, 6                       ; from one of two tables; default index 0x14
003868CE  call  0x2f8e90
003868D3  cmp   eax, 8
003868D6  jne   exit                         ; a state must be exactly 8
003868F1  mov   eax, dword ptr [rdi + 0x64]
003868F4  or    eax, dword ptr [rdi + 0x3c]
003868F7  test  eax, 0x10010
003868FC  jne   exit                         ; two status bits block it outright
00386908  bt    eax, 0x10                    ; bit 16 -> use max([unit+0x48], 1)
0038691A  bt    eax, 0x1c                    ; else bit 28 -> DOUBLE [unit+0x24]
00386923  add   eax, eax
00386925  cmp   eax, dword ptr [rdi + 0x48]
00386928  je    exit                         ; already at the target -> nothing to credit
```

**Status bits `0x10` and `0x10000` suppress the credit entirely**, and **bit 16 and bit 28 each select
a different source quantity**, with bit 28 doubling it.

**Bit 28 appears in stage 2 and stage 5, doing the same job in both** — selecting and doubling a
unit-stat-derived amount. Two independently-read stages agreeing on one status bit's role is the
strongest thing this section has; ~~what the bit is named is still unknown~~ (Bubble, above).

**The rest of stage 5, read 2026-09-12 (FABLE): an out-of-combat regeneration ramp.** After the
gates — category 8, neither Sleep nor Disease, HP not already at the cap — the stage walks the
unit's **perception candidate cache** (`+0xBC4` count, `+0xBC8` entries of 16 bytes, rebuilt by
`BattleUnit_RebuildPerceptionCandidateCache` and `BattlePerception_RefreshCandidateCacheGeneration`,
[the battle-unit field map](../../04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md)): for each entry it resolves the actor's unit (`ActorWork_GetBattleUnitRaw`) and
asks `002F8E70` — `002F8E90(BattleStats_GetOwningRecord(unit)) & 7` — and **one non-zero answer,
a perceived foe, refuses the credit** (`0038693F`–`00386986`); unit `+0xEA8` must be zero too
(`0038698C`). The 64-byte record's first word is then a per-unit tick counter: it increments every
tick (`00386A27`), and on every multiple of `frame base × 30` ticks — once a second at a per-frame
tick — the stage credits **1 %** of max HP after ten such beats, **2 %** after thirty and **5 %**
from fifty on, parking the counter at `1500 × base` so it stays there (`003869A2`–`00386A23`; the
amount is `(max HP, doubled under Bubble, or current HP under Disease) × pct / 100`, flag A
`|= 0x100`). Any failed gate zeroes the counter (`00386A2C`). So a kind-1 record of category 8
that perceives no foe heals a rising fraction of its HP each second — the reason a disengaged
enemy comes back at full health.

### The two suppression gates are one function on two halves of a packed mask

`BattleTarget_HasLow16EligibilitySuppression` (`0030B9B0`) and
`BattleTarget_HasHigh16EligibilitySuppression` (`0030B8E0`) are the same 110-byte shape:

```c
if (!unit || !other) return 0;
variant = (BattleTarget_ClassifyRelationshipClass(unit, other, 0) > 1);   /* 0030AB40 */
g = BattleTarget_ComputeGlobalEligibilityMask();
u = BattleTarget_ComputeUnitEligibilityMask(unit, variant);
/* Low16 :  return (g & 0xFFFF) != 0 || (u & 0xFFFF) != 0;   */
/* High16:  return (g >> 16)   != 0 || (u >> 16)   != 0;     */
```

**So the eligibility mask is a packed pair of 16-bit masks and a caller picks a half.** The tick tests
`bx`/`ax` directly — **the low half**, the same question `HasLow16` asks.

**And the variant argument comes from the relationship class.** `BattleTarget_ClassifyRelationshipClass`
is the subject of **Z-13** in the gambit document; here its return is reduced to `> 1`, so ~~**whatever
values above 1 exist, this caller only distinguishes "1 or less" from "more than 1."** That is a
constraint on Z-13 from a second subsystem, not an answer to it.~~ `> 1` means the classifier returned 2 *(answered: see CONTRACT-auto-status-rebuild.md §13f, EXP-197 — it returns `(computed == expected) + 1`, 1 or 2; 2026-10-02, OPUS)*.

### Still not established

- [x] ~~What the field at `unit + 0x28` is (the `/ −50` drain source) — unchanged from section 10.~~ **Resolved 2026-09-11:** the base is the stats record, not the unit, and [its field map](../../08-Combat-Formula/Battle-Stats-Record/the-battle-stats-record-field-map.md) names `+0x28` as the MP capacity (max MP) — the drain is max MP / 50 per ~~tick~~ beat, every `frame base × 10` ticks *(corrected 2026-10-02, OPUS: §5 and CONTRACT-periodic-tick.md §11)*. The `[unit+0x24]` / `[unit+0x48]` in §10's listing are likewise the record's max HP and current HP.
- [x] ~~What status bits `0x10`, `0x10000`, bit 16 and bit 28 are named.~~ **ANSWERED by
      cross-reference 2026-09-12:** bit 4 **Sleep**, bit 16 **Disease** (both spellings of the same
      bit), bit 28 **Bubble** ([the thirty-two statuses](../the-thirty-two-statuses.md)) — so the credit is refused to a sleeping or diseased
      unit, and Bubble doubles the max-HP source exactly as it doubles the HP cap.
- [x] ~~What the 64-byte records in stage 5's ~~two tables~~ table hold.~~ **ANSWERED 2026-09-12
      (FABLE), for the word the stage uses:** one array ~~at `0208D494`~~ based at `0208D480` (stage 5 addresses field `+0x14` of each record, hence `0208D494`) — forty 64-byte records
      indexed by a kind-0 record's type byte `+4`, then from ~~`0208DE94`~~ `0208DE80` (field `+0x14` at `0208DE94`) records indexed by the
      owning unit's slot index `+0xEA9`, ~~`0x14` when no owning unit is found~~ and, when no owning unit is found, the raw address `0x14` as the record pointer, not an index (`003868BD mov ebx, 0x14`, read by `movzx eax, word ptr [rbx]` at `003869A2`) *(corrected 2026-10-02, OPUS)* — and word ~~`+0` of the
      record~~ `+0x14` of the record is the unit's **out-of-combat tick counter** driving the 1 / 2 / 5 % ramp (§13, "the
      rest of stage 5"). ~~The other 62 bytes are unread.~~ The other bytes are not all unread: `+0x18` is the walk-MP carry, read and written by `002F9400` *(corrected 2026-10-02, OPUS: `00386885` / `003868AD` and `002F9439` / `002F9461` / `002F9474`; where-mp-comes-from.md §5, CS-6)*.
- [x] ~~What the `[rbp+0xBC8]` list stage 5 walks (count at `+0xBC4`, stride `0x10`) contains.~~
      **ANSWERED 2026-09-12:** the unit's perception candidate cache — the actors it currently
      perceives — and the stage refuses the credit when any of them is of a non-zero relationship
      class (`002F8E70 & 7`), i.e. when a foe is in view.
- [x] ~~What state value `8` from `002F8E90` means.~~ **Narrowed by cross-reference 2026-09-12:**
      [the kind-byte page](../../04-Actor-Entity/Battle-Record-Kind/battle-record-kind-byte.md) — category 8 is a kind-1 (enemy-table) record whose owner's `00263C20` class is
      1, 2 or 7; the post-result page's "steals your loot" message keys on the same value. ~~What the
      class itself names is **AL-3**.~~ **AL-3 answered 2026-09-12 (FABLE):** the class is the actor's
      **free-target type** (`setfreetargettype` / `btlAtelSetUnitType`, the kind-byte page) — so
      category 8 is an enemy-table unit of free-target type 1, 2 or 7, and category 4 one of type 3.

### Corrected 2026-09-12 — stage 2 does advance timers, through an address the displacement scan could not see

The reading above scanned the three stages for the `0x17C` displacement and concluded that stage 2
"advances no timer this document can find". The scan was right about `+0x17C` and wrong about the
function: stage 2 computes `rcx = target − record + 0x60` once (`00386CA9`–`00386CB2`) and then
addresses the *target's* `+0x13C[s]` as `[rcx + r15]` (`r15 = record + 0xDC + 2s`) and its
`+0xBC[s]` as `[r14]` (`r14 = target + 0xBC + 4s`, `00386C90`), so no instruction carries the
displacement a scan would look for. Read whole on [the status write](../Status-Write/the-status-write-and-its-side-effects.md) §2.4a, stage 2 is **the timer of
the 32 status-word statuses**: `+0xBC[s]` is a per-status remaining duration (10 spent per tick,
default `status_data +8` × Vitality factor × frame base × 300; the Petrify / Doom count), `+0x13C[s]`
a per-status beat (`status_data +9` × frame base × 30) on which Poison, Sap and Regen land and the
Petrify / Doom count steps; a word-1 status whose duration runs out goes into the remove mask
(Petrify adds Stone, Doom writes HP 0), and HP Critical is maintained against max HP / 5. The
decrements it accumulates into `+0x24` (the block above) are those beats landing. Section 4's
countdown is the *other* timer — the eight-slot `+0x17C` array keyed by the effect table at
`02EBF040` (`003855FD`–`00385604`), not `status_data`; the two coexist, and "stage 3 is the only
decrementer" holds for `+0x17C` alone.

## 14. The tick after its first apply - the Esper dismiss, the traps, walk MP, the pickup and the common tail (OPUS, 2026-10-02)

**Scope and reading.** `BattleUnit_RunPeriodicCombatMaintenance` (`00310DB0`, 296 instructions, `00310DB0`–`003112E9`) was read whole from the shipping image (`retool.py dis 00310DB0`, image `73461d08…`). This draft orders what the existing pages leave unordered: the Esper check between gate 3 and gate 4, the gate before the eligibility masks that the pages do not list, and everything after the first apply at `00310FAC`. `unit` = `rsi` (`00310DD3`). `stats` = `[unit+0x698]`. `result` = the `0x148`-byte stack record at `rsp+0x40`. Paths are relative to `Database/FFXII TZA/`.

**Execution order.** Steps 1–3 come after the documented gates 1–3 (`00310DCB`, `00310E08`, `00310E14`). Steps 4–6 come after the documented build and first apply (`00310F5D`–`00310FAC`).

1. **Esper dismiss check, before any eligibility gate (`00310E21`–`00310EFD`).** The tick re-reads `stats` (`00310E21`). It skips this block, going to `00310F02`, when `stats` is null (`00310E38`), when the kind byte `[stats+5]` is not 0 (`00310E41`–`00310E47`, so the record is not a party record), or when the type byte `[stats+4]` is outside `0x1B`–`0x27` (`00310E4D`–`00310E55`). That range is the thirteen Esper rows (`00-Engine-Core-Runtime/Battle-Runtime-Mode/battle-runtime-mode-ladder.md:335-339`). Otherwise it dismisses when any of these holds:
   - current HP `[stats+0x48]` ≤ 0 (`00310E5B`–`00310E5F`);
   - the summoner is missing. The summoner is found by `BattleUnit_FindByCombatantId` (`0031B770`) on the byte `[[02EBF190]+0x5AD5]` (`00310E65`–`00310E7B`), the caster's type byte that the summon sequence stores (`battle-runtime-mode-ladder.md:335`);
   - the summoner's unit byte `+0` lacks bit `0x10` (`00310E93`), the unit-present flag (`04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md:1347-1348`);
   - the summoner has no `+0x698` (`00310EA8`–`00310EB0`);
   - the summoner's `([+0x3C] | [+0x64]) & 0x80000003` is non-zero (`00310EE0`–`00310EEB`, the functional predicate) **and** `FieldData_GetActiveFieldRecordBit15` (`00377C20`) returns 0 (`00310EED`–`00310EF4`).

   The dismiss is `003138D0(0)` (`00310EF6`–`00310EF8`). That function acts only when `BattleRuntime_GetMode0To5FromFlagsAndFieldBit15` returns 1, summon mode (`003138D8`–`003138E0`; ladder `:82`). It resolves `0031B8C0(3)` (`003138E6`–`003138F1`) and issues command `0x113`, Dismiss (ladder `:388`), through `BattleUnit_IssueCommand` `00311CF0(unit, handle, 0, 0x113, 0)` (`0031394A`–`0031395D`). It then sets bit 0 of the word `[02EBF190]+0x5AD0` to its argument, 0 (`00313962`–`00313981`). The issue and the bit write are both skipped when the slot unit already has `0x113` pending at `+0xBA0` (with flag bit 14 set) or committed at `+0x714` (`00313903`–`0031391C`). **After the dismiss the tick jumps to `003112C1` (`00310EFD`), which only restores registers and returns.** That skips gates 4–7, every result build, walk MP, pickups, enmity decay and `002FE950`.
2. **Gate 4 (not in the pages' gate list): `00265680() != 0` (`00310F12`–`00310F19`).** A failure goes to `003112A1`. `00265680` is the actor-manager readiness probe: manager slot 0 live, every live slot's `+0x17` bits 0–1 set, `002E0540`, then `00265720` (`00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md:929-933`). The documented global and per-unit eligibility masks (`0030B770` at `00310F1F`, `0030B7F0(unit, 0)` at `00310F2B`) and the unit flag `0x1000000000` (`00310F42`–`00310F4F`) follow as gates 5–7. Each also fails to `003112A1`, not to the epilogue.
3. **Build 1 and apply 1** are documented (`00310F7A` memset, `00310F8B` `00385DF0(stats, &result)`, `00310FAC` `003112F0(&result, 0, stats, 0xFFFF, 0)`; the fifth argument `[rsp+0x20] = 0` is at `00310FA7`).
4. **Authored trigger point, then build 2 and apply 2 once per affected unit (`00310FB1`–`003110BA`).** The tick writes 4 to a count at `[rsp+0x30]` (`00310FB6`) and calls `BattleUnit_TryTriggerNearbyAuthoredFieldAction` `002F8060(unit, &list[rsp+0x190], &count)` (`00310FBE`–`00310FC9`). That function zeroes the count at entry (`002F80A7`) and, on a hit, writes the number of affected units (`002F8274`). It returns the chosen outcome word, the 75/25 roll, or `0xFFFF` (`002F82C6`; `03-World-Area-Field/walking-into-an-authored-trigger-point.md:36-102`). The id is checked with `BattleEncodedId_IsValidForClass(0x14, id, 0)` (`00310FD2`–`00310FE7`); class 20 is the action table `02EBF138` (`00-Engine-Core-Runtime/the-encoded-id-class-registry.md:150`). The block runs only if the id is valid and `count > 0` (`00310FF0`–`00310FF5`). **Loop:** `ebp` runs from 0 to `count`, `rbx` steps by 8 through the pointer list (`00311003`, `003110B0`–`003110BA`); the list has 4 slots, `rsp+0x190`–`0x1AF`, below the cookie at `0x1B0`. Per affected unit `u`:
   - (a) `memset(result, 0, 0x148)` (`00311003`–`00311010`);
   - (b) the action row for `id` is resolved through `ImageAddress_ResolveRuntimePointer` `0020E600([02EBF138]+0xC)` plus `word[02EBF138+8] × id` (`00311015`–`0031104B`). **The row address is computed in 32 bits** (`imul ecx, edi` / `add ecx, eax`, `00311048`–`0031104B`). If the table or the resolve is null, the row pointer becomes 0 (`0031104F`) and is still dereferenced at `0031105A`;
   - (c) `002EACD0([u+8], 1, &u+8, row.+0x24 & 0x7FFF)` (`00311052`–`0031106B`), the attached-effect creator, and the "trap applier" use of row `+0x24` (`07-Combat-Action/Action-Definition-Row/the-action-definition-row.md:79`). Its handle goes to `0024ED50` (`00311070`–`00311072`), the handle-class router (`99-Unresolved-Residual/Largest-Unclassified-Code/the-largest-unclassified-functions.md:1596`). For the class-5 handle that `002EACD0` creates, the router reaches `003B0F30`, which sets bit `0x800` of the presentation record's `+0x36A` word (`003B0F71`–`003B0F76`);
   - (d) `BattleFormula_ResolveTargetResult` `00385F60(id, 0, [u+0x698], &result)` (`00311077`–`0031108C`);
   - (e) `003112F0(&result, 0, [u+0x698], id, 0)` (`00311091`–`003110AB`).
5. **Walk MP (`003110C0`–`003110D7`).** This step is reached whether or not step 4 ran (`00310FE7` and `00310FF5` both target `003110C0`). The tick calls `BattleUnit_ResolvePeriodicPrimaryResourceRecoveryStep` `002F9400(unit)`, which returns 0 or 1, then `BattleStats_ModifyPrimaryResource` `00300CE0(stats, ret, 0x90)` with no test of `ret` (`10-Status-Periodic-Terminal/where-mp-comes-from.md:277-321`).
6. **World pickup and Chain Bonus (`003110DC`–`00311284`).** All exits from this step go to `00311289`. For the reading see `13-Rewards-Progression-Economy/world-loot-pickups-the-ten-slot-pool-and-the-despawn.md:285-299` and `13-Rewards-Progression-Economy/loot-drops-and-enemy-chain.md:653-680`.
   - **Qualify.** The unit qualifies if `PartyFocus_IsCurrentPackedActorHandle([unit+8])` is true (`003110DC`–`003110E6`) or its committed action `+0x714 == 0x4165` (`003110E8`–`003110F4`). `0x4165` is the walk-to-nearest-pickup goal (`06-Movement-And-Navigation/Battle-Locomotion/battle-locomotion-steering-and-recovery.md:368`).
   - **Find.** `Loot_FindOverlappingPickupIndex` `002FB150(unit, [01CEBBA8])` (`003110FA`–`00311105`); a negative result exits (`0031110E`). The slot is kept in `ebx`.
   - **Post.** `00469E30(stats)` (`00311114`–`0031111B`) posts battle event `0x4E` (`00469E6B`–`00469E6E`) when `002F8E90(stats) == 8`, the "steals your loot" message (`07-Combat-Action/Post-Result-Events/the-post-result-events-and-the-battle-message-table.md:348`).
   - **Remove.** If `stats` is re-read null (`00311120`–`0031112A`) or `[stats+5] != 0` (`00311130`–`00311136`), the tick calls `Loot_RemoveWorldPickupByIndexWithoutGrant(slot, [unit+8])` (`0031127F`–`00311284`).
   - **Collect.** Otherwise it calls `Loot_CollectWorldPickupByIndex(slot, [unit+8])` (`0031113C`–`00311141`), then the chain-rank outcome selector `00319530()` (`00311146`; `13-Rewards-Progression-Economy/CONTRACT-loot-rolls-and-the-chain.md:136`). It exits unless the outcome is 1–6 (`0031114E`–`0031115D`).
   - **Gather loop** (`ebp` 0..8, `00311173`–`003111B7`). Per slot it takes `s = BattleStats_GetByMappedBattleSlot(i, 1)` (`0032117A`). It keeps a non-null `s` whose `([s+0x64] | [s+0x3C]) & 0x80000003` is 0. When that value is non-zero it keeps `s` only if `00377C20()` is non-zero (`00311182`–`0031119C`). **Store:** `qword [022C1740 + n×8] = s` (`003111A4`, guarded by `n < 9`, `0031119E`). That is the same global the chocobo collector fills (`battle-runtime-mode-ladder.md:353`). If no member is kept, the step exits (`003111BC`–`003111BF`).
   - **Bonus loop** (`rbx` 0..n−1, `003111D0`–`00311277`). It takes `h = BattleStats_GetOwningActorHandle(member)` (`003111D0`–`003111D8`; stored to `[rsp+0x30]`, `003111E1`). For outcomes 3 and 5 (`r15−3 ∈ {0, 2}`, `003111DD`–`003111EC`), a member whose `h` differs from `[unit+8]` is skipped (`003111EE`–`003111F1`). When `h != 0` it calls `002EACD0(h, 1, &h, 0x76)` (`003111F3`–`00311208`), the return discarded. Then it runs `memset(result)` (`0031120D`–`0031121A`). **Store:** `result+0x00` bits 3–4 `= table[outcome] & 3`, where the table at `00D102C0` holds `{−1, 0, 1, 2, 2, 3, 3}` (`0031121F`–`00311241`). Next is build 3, `00385F60(0xF5, 0, member, &result)` (`00311245`–`0031124D`), then apply 3, `003112F0(&result, 0, member, 0xF5, 0)` (`00311252`–`0031126C`). Action `0xF5` is "Chain Bonus" (`loot-drops-and-enemy-chain.md:662`).
7. **Common tail (`003112A1`–`003112AC`).** It is reached from step 6 (`00311289` restores `r12`, `rbp` and `r14`) and from every failure of gates 4–7. It calls `BattleEnmity_UpdatePeriodicDecay` `00321530(unit)` (`003112A4`; `09-Combat-AI-And-Gambits/CONTRACT-enmity.md:52`), then `002FE950(unit)` (`003112AC`). `002FE950` is the HP-stage pulse for category-`0xF` foes, which writes unit `+0xEAC`/`+0xEB0` (`the-battle-unit-field-map.md:504`; its own gate is `[+0x698]+5 == 1` and `[unit+0x56] == 0xF`, `002FE974`–`002FE97E`). After that come the register restores (`003112B1`–`003112C9`), the cookie check `00808C40` (`003112DC`) and `ret`.

**Exit map.**
- Gates 1–3 (`00310DD6`, `00310E0E`, `00310E1B`) → `003112D1`: nothing below them runs, not even the decay.
- The Esper dismiss (`00310EFD`) → `003112C1`: the dismiss runs, then nothing else.
- Gates 4–7 (`00310F19`, `00310F33`, `00310F3C`, `00310F4F`) → `003112A1`: only the decay and `002FE950` run.
- The normal path runs steps 3–7 in order.

**Loops.** There are exactly three: the trap list (step 4), the party gather (step 6) and the bonus loop (step 6). There is no other back-edge in the body. Of the three `003112F0` calls, the first runs once; the second runs once per affected unit (at most 4); the third runs once per gathered member, or only for the picker on outcomes 3 and 5.

## Falsification pass 1 — 2026-09-12 (OPUS)

**passes: 1 · last_pass: 2026-09-12**

This page has been reopened once and corrected twice, so the pass targets what those rounds did not:
the structural counts, the beat arithmetic re-derived rather than read, and the two division magics
re-checked **with better controls than the page uses**.

| claim | measured |
|---|---|
| six stated sizes — `00310DB0` 1,338 · `00385DF0` 83 · `00386C70` 935 · `00385CA0` 336 · `003848E0` 205 · `003112F0` 2,040 | **6 of 6 exact** |
| `00310DB0` "spends its first ninety instructions refusing to run" | the body is **296 instructions**; the last gate call (`BattleTarget_ComputeUnitEligibilityMask`, `00310F2B`) falls inside the first 90, and the `0x148` `memset` that begins the tick body is **instruction 95**, at `00310F7A`. **Ninety is right.** |
| `unit + 0xDD0` is a deadline, and passing it clears `0x40000000` | `00310DF4 cmp dword ptr [rsi+0xdd0], eax` / `jae` / `and dword ptr [rsi], 0xbfffffff` — which clears **bit 30**, and bit 30 is `0x40000000` |
| `00385DF0` is a pure sequencer: five calls, fixed order, the last a tail call | **five targets in exactly that order**, the last a `jmp`, and — the stronger form — **the body contains no `ret` at all** |
| the beat is `[01DFE0B4] × 30 / 3` = base × 10 | `imul ecx, [01DFE0B4], 0x1e`; `0xaaaaaaab` / `mul` / `shr ecx, 1` is **÷ 3**; `div ecx` on the raw tick; `test edx, edx` / `jne`; `or dword ptr [rdi+0x2c], 0x4000` |
| the `≥ 50` guard and the `0x148` record | `cmp ecx, 0x32` / `jl`; `mov r8d, 0x148` / `call memset` |
| `0xAE147AE1` with `sar 4` is `v / −50`, with `sar 5` is `v / −100` | **both exact over −20,000…20,000** |

### The controls this deserves are not 101

§ says the magics were "checked against integer division across ±20,000 sampled values, **with a
control against 101 that fails**". Both magics reproduce exactly. But **101 is the wrong control for
the claim the section is making.** The section's own headline is *"the divisors are negative"* — and
a control against 101 does not test the sign at all; it only shows the magic is not *some other
number*.

Three controls that do test it, all of which fail as they must:

| control | what it rules out |
|---|---|
| `v / −49` | the shift being one too small |
| `v / −51` | the shift being one too large |
| **`v / +50`** | **the sign — the section's actual claim** |

`+50` is the control that earns the sentence. With it, "the stored delta is a loss, not a magnitude
with a sign applied later" is established rather than asserted; without it, every number in the
section is equally consistent with a positive divisor and a later negation.

Samples over the reachable domain (the `≥ 50` guard means only `v ≥ 50` reaches the `sar 4` path):
`50 → −1`, `99 → −1`, `100 → −2`, `12345 → −246`. Truncation toward zero, and negative throughout.

### A note on how this nearly went wrong

My first run of the arithmetic reported **both magics as failing**. The fault was in my harness, not
the image: I applied the sign correction as *"add 1 when the input is negative"*, where the code adds
the **sign bit of the quotient** — `mov eax, edx` / `shr eax, 0x1f` / `add edx, eax`, reading `edx`
*after* the shift.

The tell was that **the control failed at the same time**. A control exists to fail when the claim is
wrong; when it fails *alongside* a claim that should hold, the instrument is the first suspect, not
the claim. Recorded because the same shape will recur: every compiler-emitted division by a constant
carries this correction, and reading it off the input is the natural mistake.

**Not claimed:** nothing here was executed or observed live. ~~`+0x28` — "one-fiftieth of *what*" —
remains unestablished, as §5 says;~~ *(answered: `+0x28` is max MP — see §10 and §13, resolved 2026-09-11; 2026-10-02, OPUS)*; the five-stage bodies were not re-read beyond their entry sizes,
and the two suppression gates were left to §13's treatment.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

- **Audio, Items and Rewards — through stage 5's apply.** `BattleFormula_ApplyTargetResult` (`003112F0`) touches
  several other layers:
  - **Audio:** it plays its sound directly through the sound resolver and player;
  - **Items_Equipment_Shops_License:** it grants stolen items (`Inventory_ModifyEncodedItemAndUpdateDiscoveryState`);
  - **Rewards_Progression_Economy:** it calls `BattleStats_AdvanceLevelToTargetAndRecomputeGrowth`, `GameState_SetGil`
    and `GameState_GetGil`.

  The tick body `00310DB0` itself calls the world-pickup functions `Loot_FindOverlappingPickupIndex`,
  `Loot_CollectWorldPickupByIndex` and `Loot_RemoveWorldPickupByIndexWithoutGrant`; that is the chain-bonus pickup
  path §13 of [which roll](../../21-RNG-And-Determinism/which-roll-is-on-which-generator.md) cites. `0030E360` reaches
  `BattleUnit_ProcessDefeatRewardsAndLoot`.
- **RNG_Random_Selection.** Stage 2's timer body `BattleFormula_AdvanceStatusTimersAndBuildResult` (`00386C70`) draws
  the gameplay MT (`RNG_MT19937_NextU32_Thunk`). Status-timer ticks are therefore on the combat-formula stream, not on
  the loot LCG.
- **Party.** `00310DB0` tests `PartyFocus_IsCurrentPackedActorHandle`.
- **Gameplay.**
  - `00301140` and `0030E360` dispatch presentation events, and `0030E360` updates the engagement flag.
  - `00310DB0` calls `BattleEncodedId_IsValidForClass`.
  - `BattleTarget_ClassifyRelationshipClass` (`0030AB40`, the `variant` test) is also used by the three relationship
    predicates `BattleUnit_HasRelationshipClass2PlusInSlotMask`, `…InTrackedActorList` and
    `BattleUnit_HasCurrentFocusEngagementEvidence`.
- **Movement — consumers of the same small queries.**
  - The perceived-foe query `002F8E70` (`002F8E90(owner) & 7`) is also asked by the locomotion stall-recovery code:
    `BattleLocomotion_TryRecoverFromStalledPath`, `BattleLocomotion_UpdateStallRecoveryState` and three unnamed
    locomotion bodies.
  - The class nibble `00263C20` is read by `PartyFollow_SolveFormation` and a 66-byte movement helper.
  - The presentation builder `002F6AB0`, the one reader of the post-recovery mark, is called from two 109–126-byte
    movement helpers and itself calls movement code: a 936-byte body and three helpers in the `003EDxxx` range.
  - `00301140` calls a 448-byte locomotion helper.

  These make the tick's two predicates shared services, not tick-private state.

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **CombatFormula — SERVICE and CLIENT, 35 edges.**
  - Cited tick functions call `BattleStats_FindOwningBattleUnit` (4), `BattleFormula_ApplyTargetResult` (2), `BattleStats_ModifyPrimaryResource` (2), `BattleFormula_BuildConditionalStatusHpTransitionResult` and `BattleFormula_BuildInactiveStatusTransitionResult`.
  - They are called by `BattleStats_ModifyHPAndProcessLethalState` (3), `BattleFormula_ApplyTargetResult` (2) and formula bodies of 199, 510 and 681 bytes.
- **CoreRuntimeScheduling — SERVICE.** Three cited tick functions read `GameClock_GetRawTickCounter`.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**UI — CLIENT (7 edges, one fan-in).** All 7 edges are UI bodies reaching `00263C20` on this page. `FUN_002c7660` is the worked example - it is a 1,190-byte routine in a `0xD8`-byte frame with a stack cookie and one preserved SSE register. The crossing is **one shared subject with 7 callers on that layer**, not 7 separate relationships. Edge count from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page.*

**ActorEntity — CLIENT and SERVICE (32 edges).** The tick `BattleUnit_RunPeriodicCombatMaintenance` `00310DB0` is called by `BattleUnit_UpdateLifecycleAndCombatFrame` `00233F70` and calls `BattleUnit_FindByCombatantId` `0031B770`; the owner lookup `BattleStats_GetOwningActorHandle` `0031E800` walks the pool through `BattleUnit_GetBySlotIndex` `00236820` and `BattleUnit_GetSlotCount` `00236850`, which `0031B770` and `BattleUnit_GetBySlotIndexIfUnitFlag4Set` `00321170` also call; `BattleFormula_BuildRuntimeCounterPeriodicHpCredit` `00386860` calls `ActorWork_GetBattleUnitRaw` `00263E30`; the class nibble `ActorRuntime_GetClassNibble` `00263C20` is read by `002F8E90`, `BattleTarget_ClassifyRelationshipClass` `0030AB40`, `00273750`, `00273A00` and `0046BAC0`; `BattleUnit_RecoverFromTerminalStatusSetIfClear` `00301140` calls `BattleUnit_RefreshActorRuntimeFromDefinition` `00238BF0`; the status write `BattleStats_ChangeStatusAndProcessSideEffects` `0030E360` calls the defeat-condition check `00300FC0`; `BattleUnit_ResetActionControlForStatusTransition` `00300140` is called by `00233EA0`, `ActorSystem_ReleaseBattleUnitSlotForActor` `00234200` and `002348E0`; the field predicate thunk `FieldData_GetActiveFieldRecordBit15` `00313F60` is called by nine actor bodies, among them `BattleUnit_ActivateAppliedDefinitionRuntime` `00233AD0`, `00233F70`, `BattleUnit_ApplyUnitDefinition` `0023A570` and `BattleGroup_RefreshFourActorDefinitions` `003266C0`; and the id validator `BattleEncodedId_IsValidForClass` `00322C50` is called by `BattleUnit_FindByDefinitionSelector` `002367A0`, `0023A570`, `BattleUnit_FindMappedDefinitionSelectorByIndex` `0031B810`, `003266C0` and `BattleSlotMap_InitializeMappingClasses` `00329CC0`. The unit's per-frame lifecycle is what runs the tick, the tick's stages read units and actors only through the pool accessors this page tabulates, and the remaining edges are other actor bodies using the same accessors, predicate and validator.

**CombatAI — SERVICE and CLIENT (36 edges).** The tick `00310DB0` calls the enmity decay `BattleEnmity_UpdatePeriodicDecay` `00321530`, which calls `BattleEnmity_WriteAllCombatantIds` `00321D30` and `BattleUnit_HasActiveEngagementEvidence` `00307CE0`; `00321D30` calls `BattleEnmity_WriteForCombatantId` `00321850`, which calls `BattleEnmity_AnyAboveThreshold` `00321770` and `BattleEnmity_ClampAndStore` `00321E40` and is also called by `BattleEnmity_ApplyActionParameters` `003216E0` and `BattleEnmity_PropagateToPerceivingFoes` `003219D0`; `00313F60` is called by `00321850`, `BattleEnmity_AdjustOtherRelevantCombatants` `00321B00`, `00321D30`, `BattleUnit_RebuildPerceptionCandidateCache` `003247F0` and `BattlePerception_RefreshCandidateCacheGeneration` `00324F20`; `00236820` and `00236850` are called by `AiOrder_EvaluateTargetSelector` `00301AD0`, `003219D0`, `003247F0` and (`00236820` only) `AiOrder_ComputeBoundedSelectorScalar` `00308C20` and `00324F20`; `0030AB40` is called by `00301AD0` and `BattleTarget_MatchesRelationMode` `0030BD00`; `BattleTarget_HasLow16EligibilitySuppression` `0030B9B0` is called by `00301AD0`; and `00322C50` is called by `00301AD0`, the enmity bodies from `BattleEnmity_ReadForCombatantId` `003215C0` to `00321E40`, `GambitConfig_ClassifyActionTargetPairCompatibility` `00327A10` and `GambitConfig_LoadAuthoredPresetAndRebuildRuntimeOrders` `00327CB0`. One stage of the tick is the AI layer's enmity decay (the table row above: a frame-scaled counter that resets the row through the all-ids write); the rest is the AI's own use of the pool accessors, the relationship classifier, the eligibility gate, the field predicate and the id validator that this page also cites.

**Input — CLIENT (1 edge).** `InputGameplay_ArbitrateDigitalInputAndModalState` `00253C70` calls `00313F60`. The input arbiter reads the same field action-permission bit; it is another consumer of the thunk, not part of the tick.

**Spawn_Encounter_Lifecycle — CLIENT (4 edges).** `Spawn_CountActiveCapTrackedActors` `00308D90` calls `00236820` and `00236850`; `Spawn_ValidateCandidateDistanceToPlayers` `00234DA0` and `SpawnLifecycle_CheckAndRetireByNativeRange` `002350C0` call `00313F60`. The spawn code counts and range-tests units through the same pool accessors and field predicate; it shares them with the tick and nothing else.

## SWE2-EC7-83 update (2026-09-20) - `00466140` byte-split measured

`00466140` (34 B) is the byte-lane split the tick callers share:
`edx`'s four bytes land at `[rcx]`/`[+4]`/`[+8]`/`[+0xC]` low-to-high -
a u32 unpack into four dword slots, call-free.
Interior anchor `00466147` (the `>> 8` lane).
