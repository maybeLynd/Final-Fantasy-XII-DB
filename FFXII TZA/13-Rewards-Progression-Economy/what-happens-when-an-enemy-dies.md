---
system: What happens when an enemy dies
category: 13-Rewards-Progression-Economy
status: DOCUMENTED — the SECTION-03 reopening is resolved: its independent peer acceptance is recorded (GR-16, SWE2-AUDIT-SEM ACCEPT-WITH-NARROWING, 2026-10-01), and two non-author passes re-derived the page's claims (10 of SECTION-03's 24 bodies; GR-19's drop gate instruction by instruction, CORRECTED C1-C3 applied); the drop gate answered (GR-19: the death position must be one the party leader could stand on); the rest of the page's residue answered or cross-referenced 2026-09-30 (FABLE) (owner re-status 2026-10-01, OPUS)
owner_layer: PrimaryOwner:Rewards_Progression_Economy
evidence_tier: 1
verified_against:
  gzf_sha256: fb9b5e7ea002c1626a53d47da0b0b69a2443e246f7ce2b64329be4e034a2d3f7
  snapshot_sha256: a9cead8777597cdca58f2a47f27153f5231d60ad2bc16c3da9df8253820b09bd
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: "snapshot-identity - every function this document cites has byte-identical per-function records in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30"
    verified: "8 cited function entries, 0 of them among the 128 records that changed across GN158..GN161 (check_delta_additivity.py, check_transfer_eligible.py); re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS"
    adjudicated: OPUS-REQ-FABLE-PROVENANCE-TRANSFER-144 (9bedb5e0); re-targeted GN160 -> GN161 under EVIDENCE-STANDARD addendum 2026-09-14bh
    previously: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708 (GN160), superseded 2026-09-14
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-22
falsification_passes: 2
audit:
  passes: 2
  last_pass: 2026-10-01
  last_pass_kind: falsification
  last_pass_state: auditsem-section03-and-gr19-review-pass-2
  crossref_clean: false
  reopened_count: 1
production_review:
  section: SECTION-03
  status: locally validated; independently accepted 2026-10-01 (SWE2-AUDIT-SEM for OPUS, ACCEPT-WITH-NARROWING, f41194772, auditsem-review-section03-1001; GR-16 ANSWERED)
  scope: original reward consumers, selected caller instructions and retained binding observations
  new_live_session: false

---

# What happens when an enemy dies

> **SECTION-03 production review, 2026-09-22; ~~independent peer acceptance pending~~** (registered as GR-16, 2026-09-30). *(OPUS, 2026-10-01: independently accepted with a narrowing 2026-10-01 (SWE2-AUDIT-SEM, [review](../_index/candidates/auditsem-review-section03-1001/REVIEW.md), GR-16; N1: `run_review.py` reproduces against the pinned pre-image of the reward-binding checker, and the sealed checker agrees with the preserved observation).)*
> Corrected against original EXE instructions, 71 bounded native controls and independent review
> of four retained EXP-081 samples. The historical audit/provenance metadata below/above is not
> a new audit pass. No new live game session or complete defeat-orchestrator execution was performed.
> [Evidence, changed claims and limitations](../_experiments/evidence/continuation-section03-reward-bindings/REVIEW.md).

~~`BattleUnit_ProcessDefeatRewardsAndRetire`~~ `BattleUnit_ProcessDefeatRewardsAndLoot` at **`00312280`**, 857 bytes.
*(Corrected 2026-09-30 (FABLE): `…AndLoot` is the function table's name and the one this page's own crossings below
already use; `…AndRetire` named a retirement step that step 6 withdrew on 2026-09-28. PKG-GP-HP-LETHAL item G5 let
the label pair stand as a label, not a claim; the owner read of 2026-09-29 asked for the page to agree with itself.)*
Three documents leaned on it
and none had opened it — **and it is where experience, LP, ~~gil, levelling~~ levelling, gil and the item drop all
happen, in that order, in one function.** *(corrected 2026-10-02, OPUS: the level walk and advance, `0031244A`–`003124A3`, run inside the per-recipient step, before gil at `0031251D`; steps 2 and 4 below)*

## What the player sees (FABLE, 2026-09-30)

*(Section added 2026-09-30 (FABLE); every sentence is backed by a numbered step or section below.)*

When an enemy falls, the spoils arrive at once, while the fight goes on around them. The party's experience and
license points go up. A character who crosses a threshold levels up, and one big kill can raise a character several
levels in a single step, though never past 99. The party's gil goes up. The enemy may leave loot where it fell. The
same kill also extends the chain, counts toward the kill achievement, and is tallied for that kind of monster.

**Who is paid.** Up to nine party records are paid, but not a member who is KO'd, or under Stone or X-Zone (the two
other statuses in the same test); a flag on the area can waive that exclusion. Experience is shared among up to four
fighters, or goes whole to the summoner while an Esper is out
([how experience is divided](how-experience-is-computed-and-divided.md)). License points are not shared out.

**What changes the payout:**
- **The Cat-ear Hood** turns the wearer's license points into gil. The wearer gets no license points from the kill,
  and the party gets level × license points × 5 extra gil.
- **Three accessories** double or zero experience and license points: the Embroidered Tippet, the Golden Amulet
  and the Firefly ([the award page](experience-and-license-point-award.md)).
- **A New Game Minus run.** In a game begun from the title screen's New Game Minus option, no character ever gains
  experience. Kills still pay license points and gil, and the victory tally shows 0 EXP.

**If this broke**, a kill would leave the party's totals unchanged, or would level a character one step at a time
instead of all at once.

## The order of events

0. *(Step added 2026-09-30 (FABLE), from the body and the pages that already read its parts.)* **Before any reward**,
   when the defeated unit's stats record is an enemy's (kind byte `+5` = 1) and the killer's is a party record,
   `EnemyChain_UpdateOnDefeat` (`00317ED0`) advances the chain ([the chain page](the-chain-and-its-sticky-coin.md)).
   Then `003171C0` (106 bytes, read whole) adds 1 to achievement counter 4 and, unless the actor's class nibble is 3,
   counts the defeat for its species through `00315820`
   ([event memory](../14-Story-Event-Quest-Hunt/event-memory-at-actor-bind.md); `003171DF`–`0031721F`). Steps 1–6
   run only for an enemy-kind record whose unit byte `+0xE9A` lacks bit 3, and then only for a party killer or a death
   by party-applied Poison or Petrify (`003122DA`–`0031232A`; the reading and FA-4 are on
   [the status-write page](../10-Status-Periodic-Terminal/Status-Write/the-status-write-and-its-side-effects.md)).
1. **Build the recipient list** — up to nine, each fetched by index and admitted only if its two
   status words clear `0x80000003`, or a field-level check overrides.
2. **Per recipient**: compute experience and LP, clamp, award, **re-derive the level**, notify.
   *(Detail added 2026-09-30 (FABLE).)* The experience add is skipped for everyone while the New Game Minus flag
   `00236780` is up (`00312429`–`00312430`, ahead of `00312432`–`00312444`). The LP add feeds achievement counter 11
   (`0xB`) with that recipient's awarded LP (`00312489`, `00312496`).
3. **Once for presentation**: recompute with a NULL recipient, apply fresh caps and a field-flag
   EXP suppression, and pass the resulting amounts onward. EXP remains mode-dependent; LP has no divisor.
4. **Gil**, from the same two tables as experience.
5. **The drop**, placed at the defeated unit's position.
6. ~~**Retire the unit.**~~ **Feed achievement counter 0x11** ~~with the reward row's word +0 times
   the level span (`00317090` → `00316A50`)~~ (17) with `span × perLevelRow.u16[+0] + baseRow.u16[+0]`: the same
   shape as experience and gil, on the two reward rows' first word, with span the defeated unit's level minus its
   baseline (`003170AA`–`003170D1`). It goes through the thunk `00253770` into `00316A50` (`003170D3 mov ecx, 0x11` /
   `003170D8 jmp`), and only for an enemy-kind stats record (`003170A4`). *(Corrected 2026-09-30 (FABLE): the old
   wording dropped the flat term and the thunk. `00317090` is 78 bytes, read whole. The achievement catalogue names
   counter 17 `ACH_COUNT_SCORE`, "Record Breaker"; its feeder census did not follow this tail jump, see Related.)*
   Nothing here removes the body — the function's only
   calls after the drop are `00317090` and the stack-cookie check. *(corrected 2026-09-28 per
   `_index/candidates/pkg-gp-hp-lethal/hp_lethal_checks.py` R — `00312280` retires nothing)*

**SECTION-03 correction:** NULL skips recipient checks/modifiers, not the shared-mode EXP
roster/divisor. The original computers return EXP 9 and LP 19 for synthetic raw values 19 with
two passing members; a doubled recipient gets EXP 18. NULL EXP becomes 19 in designated mode.
`003124BC/003124C6` (`xor ecx, ecx`, ahead of the calls at `003124BE` and `003124CA`) establish the NULL arguments, while `00312505` and `00312513` establish a
separate flag-based EXP suppression before the presentation call. This is not a new observed
on-screen value. See the [award contract](CONTRACT-experience-and-licence-award.md).

## The caps

| quantity | cap | where *(anchors added 2026-09-30 (FABLE))* |
|---|---:|---|
| experience per award | **999,999** (`003124E6`) | per recipient `003123E5`–`003123F4`; the presentation value `003124DE`–`003124E8`, with `0xF423F` in `esi` (`003123A6`, `003124B4`) |
| LP per award | **999** (`003124FB`) | per recipient `003123F7`–`00312406`; the presentation value `003124F3`–`00312502` |
| accumulated experience | **99,999,999** | `00312438 mov eax, 0x5F5E0FF`, `00312441 cmova`, stored to `+0x18C` at `00312444` |
| accumulated LP | **99,999** | `0031247C mov eax, 0x1869F`, `0031248B cmova`, stored to `+0x190` at `0031248F` |

**Every clamp is two-sided** — a negative computed award is written as **0**, not as itself.
*(Scope added 2026-09-30 (FABLE): that holds for the two per-award clamps, a `jns` floor and then a `cmovg` ceiling.
The two accumulated caps are ceilings only, unsigned `cmova` on the old total plus an award already floored at zero.)*

## Levelling is a search, not an increment

```c
level = recipient[+0x1C2];
need  = ExpForLevel(level);
while (need > 0 && need <= recipient[+0x18C]) { level++; need = ExpForLevel(level); }
BattleStats_AdvanceLevelToTarget(recipient, level, 0);
```

> **The engine does not add a level; it walks the threshold table until the next threshold is out of
> reach.** One kill can therefore raise a character several levels in a single step, and **a
> threshold table returning zero terminates the walk** — the loop's other exit.

*Reconciled 2026-09-30 (FABLE).* `ExpForLevel` is a function, not a stored table. It is the experience curve
`002F8F20`, stated on [the unit-definition page](../04-Actor-Entity/Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md)
§4. It returns 0 for level 0 and −1 for any level above 98 (`002F8F2C`–`002F8F2F`, `002F8F96`). The walk leaves on
any value ≤ 0 (`0031245A`, `00312473`), so in practice the "other exit" is the level-99 cap.

## Gil comes from the same two tables as experience

```asm
0031251D  mov   rax, qword ptr [r14 + 0x698]
00312524  movzx edi, byte ptr [rax + 0x1c2]      ; the same two bytes the
          movzx e.., byte ptr [rax + 0x88]       ;   experience formula subtracts
          imul  ...  [r14 + 0xE78] + 0x30        ; multiplier   (exp uses +0x34)
          add   ...  [r14 + 0xE70] + 0x30        ; flat term    (exp uses +0x34)
```

**The identical shape, the identical difference, the identical two tables — one field earlier.**

> **`+0x30` is gil and `+0x34` is experience, in the same two records.** Two functions read hours apart
> agree on the difference and differ by four bytes in the table, which is as strong a corroboration as
> this database has produced.

The caller floors `old + award` to zero, passes that requested total to `00254EE0`, then
passes `requested - old` to `00469E80`. The setter meters that same difference before imposing
its upper cap, assuming the compared old balance has not changed between reads. The notifier
only dispatches a positive-delta event; it is not another stored balance.

**A cap does not by itself make the two reported deltas differ.** With old balance 99,999,995
and award 10, both delta calculations yield 10, but the stored balance increases by only 4.
With old balance 5 and award -10, the caller requests zero: the setter sees a spend of 5 and
the notifier receives -5 (and sends no positive event). These are bounded static arithmetic
consequences, not new full-path runtime tests. See the sixth invariant of the
[defeat contract](CONTRACT-defeat-rewards-sequence.md), "two reporting paths can both exceed the stored gain"
*(reworded 2026-09-30 (FABLE): the contract's invariant label is not a register id, and written as an id it failed
`documented_rule.py`'s unknown-id check)*.

## An equipment effect that turns LP into gil (FABLE, 2026-09-30)

```c
if (recipient[+0x69] & 0x10 || recipient[+0x79] & 0x10) {
    accumulated += recipient[+0x1C2] * lp * 5;   // level x LP x 5
    lp = 0;                                      // and the recipient gets none
}
```

**Byte 1 of each ~~status~~ effect layer, bit 4** — under the layer rule, ~~**status id 12.**~~ **effect id 12**, whose
shipped help text is *"Convert all license points earned to gil."* A recipient carrying
it **receives no LP at all**, and instead **`level × LP × 5` is added to the party's gil**.

*Corrected 2026-09-30 (FABLE); the heading read "A status that turns LP into gil".* `+0x68` and `+0x78` are the two
16-byte effect layers, not the status words. The status words are `+0x3C` / `+0x64`, the pair the recipient test reads
([the award page](experience-and-license-point-award.md) §2, N-3). So layer bit 12 is an effect id; status 12 is
Reverse. Row 12 of the augment table carries description id 13012, which `listhelp_ability.bin` resolves to that help
text. The one equipment row whose augment byte `+0x1A` is 12 in a category the auto-status rebuild reads is the
**Cat-ear Hood** (`0x117F`, category 22). Controls: rows 27 and 28 of the same table read "Doubles EXP earned." and
"Doubles license points earned.", and the Embroidered Tippet, Golden Amulet and Firefly carry 27 / 28 / 29, the award
page's N-2 names. Scripts and output:
[`augment12.py`](../_index/candidates/dd-content-fable-0930/augment12.py),
[`augment12_equipment.py`](../_index/candidates/dd-content-fable-0930/augment12_equipment.py)
([output](../_index/candidates/dd-content-fable-0930/augment12.out.txt),
[output](../_index/candidates/dd-content-fable-0930/augment12_equipment.out.txt)).

> **It is not a bonus on top; it is a conversion.** And the converted amount is pooled into the same
> accumulator the gil award uses, so **one character's status changes what the whole party is paid.**

## Historical falsification pass — 2026-09-03 (one inference corrected)

| attack | result |
|---|---|
| Does zero ECX prove undivided EXP? | **No; corrected in SECTION-03.** The NULL argument is real, but the callee still takes the shared divisor when that mode is selected. LP has no divisor in either case. |
| Is the LP conversion a bonus or a replacement? | **Replacement** — ~~`lp` is overwritten with the running total's previous value before the award~~ `lp` is set to zero (`ebp` zeroed at `003122A9`, `0031241F mov esi, ebp`) *(corrected 2026-10-02, OPUS: the running total is never copied into LP; see the listing in "An equipment effect that turns LP into gil")*, so the recipient's LP add is zero. |
| Are gil and experience really the same tables? | Same two pointers (`+0xE70`, `+0xE78`), same difference of the same two bytes, **fields `+0x30` and `+0x34`.** |
| Does the recipient list admit nine or fewer? | The store is guarded at `< 9` and the counter increments in the same branch, **so the count cannot exceed the array** — both move together. |
| Could the level walk be an off-by-one? | It advances **while the next threshold is reachable**, then applies the level it stopped at — the exit condition is the first unreachable threshold, and a zero threshold also exits. |

~~**What this document does not claim:** what `00317ED0`, `003171C0`, `00317090`, `00319490`,
`003180F0` or `00319CA0` do internally — the last three are the **drop placement chain** and are named
here only by position — the semantic purpose of `00236780` beyond its verified suppression branch, or which status id 12 is called.~~
*Reconciled 2026-09-30 (FABLE).* Each item in that list is now read, either here or on the page that owns it:
- `00317ED0` is the chain update, read on [the chain page](the-chain-and-its-sticky-coin.md) and in
  [the loot page](loot-drops-and-enemy-chain.md) §8b;
- `003171C0` is step 0's kill counter and species tally, and `00317090` is step 6's counter-17 feed; both were read
  whole today;
- `003180F0` rolls the drop entries ([the loot contract](CONTRACT-loot-rolls-and-the-chain.md)) and `00319CA0` places
  the pickup ([the pickup pool](world-loot-pickups-the-ten-slot-pool-and-the-despawn.md));
- `00319490` (148 bytes, read whole) is the gate in front of them. The drop is attempted only when it returns nonzero
  (`00312588`–`00312597`). It takes the party focus actor's battle unit, but only while bit `0x10` of `02089340` is
  set and the unit's first byte has bit 3 (`003194A8`–`003194D2`); otherwise it passes null, which answers 0 (no drop).
  It hands the unit and the death position to a 565-byte body that gathers and counts nearby actors, and returns that
  body's answer. ~~**What that body decides is GR-19.**~~ **Answered 2026-09-30 (FABLE, GR-19; record [`gr19-gr11-placement-fable-0930`](../_index/candidates/gr19-gr11-placement-fable-0930/README.md)):** `00319490` asks whether **the party leader could stand at the death position**. It passes the focus actor's battle unit (none, and so no drop, unless `02089340` bit `0x10` is set and the unit's first byte has bit 3) and the point `{x, y, z, 1.0}` to `003377C0`, which answers 0 (no drop) in two cases. (a) **Another body is in the way:** the gather (`00391D10`, or `003920F0` when ~~x is~~ any coordinate is NaN *(C1, 2026-10-01, OPUS)*) lists the actors within the leader's radius (`ActorRuntime_GetClass3FloatPair` `00265090`), and any one of them other than the leader whose movement body would pair with the leader's in the separation pass (`00314EB0`: equal layer `+6`, owner `+0x119` zero or different; [the movement body](../06-Movement-And-Navigation/the-movement-body-pool-and-the-separation-pass.md)) refuses. The relation query `00313F80` that follows does not change the answer: both of its counters refuse (`0033798D`-`0033799C`). A unit whose `+0xE68` class is 1 is skipped when the leader's is 4, and the actor check is skipped when `002EA7F0` refuses the leader (the actor tested is `rbp`, resolved from unit `+0xEA9` through GTAB / MABE; C3, 2026-10-01, OPUS). (b) **The ground refuses the point** (`00337700`): the corridor family's `LQUERY` (`00391410`) must hit nothing at the point, `00384130` must map its X/Z to a grid cell (not `0xFF`, off-map), and `00336390` must pass the point and the four corners of a square of half-width max(radius A, radius B) through the point query `0032A6A0` under the leader's `+0x1F4` mask ([the corridor query family](../06-Movement-And-Navigation/CONTRACT-corridor-query-family.md)). ~~So a kill leaves no loot when the enemy dies where the leader could not stand: in another colliding body's reach, inside static geometry, off the map grid or off walkable ground.~~ *(Narrowed 2026-10-01, OPUS, on SWE2-AUDIT-SEM's C2, [review](../_index/candidates/auditsem-review-gr19-gr11-0930/REVIEW.md), which accepts the mechanism instruction by instruction:)* So a kill leaves no loot when the enemy dies where the leader could not stand. That means another actor in the leader's movement-body layer within the leader's radius (the separation pass's pairing rule, not a contact test), a hit in `LQUERY` at the point, a point off the navigation grid, or a refusal from the point query `0032A6A0` at the point or a corner. `LQUERY` and `0032A6A0` are the two queries the leader's forward-step clearance test (`00335B60`) also applies, and what they test is not named. How the defeated unit's own body is kept out of the gather (filter `0x1C`, or release before the gate) is not read. The gather's filter word `0x1C` and the `+0x1F4` mask are not named. *(Narrowed 2026-09-30, FABLE, on SWE2-AUDIT-SEM's [review](../_index/candidates/auditsem-review-dd-gameplay-0930/REVIEW.md) C4; record [`dd-gameplay-corrections-fable-0930`](../_index/candidates/dd-gameplay-corrections-fable-0930/README.md))*: `003377C0` and `00337700` are not drop-specific. `003377C0` is also called by `00334E00` (twice, the random detour's reachability test), `00339630` and `0033BD70` (the landing probe), and `00317DE0` takes both by `lea` as the placement test that DE-4 (ANSWERED) names for wander positions: `00337700` for a zero radius, `003377C0` otherwise. So the drop gate asks the shared placement test whether something can be placed at the death position, and a kill drops nothing where that test refuses. Open: what the test accepts - the counted relation (`00314EB0`, `00313F80`) and `00337700`'s world test `00336390` ([battle locomotion](../06-Movement-And-Navigation/Battle-Locomotion/battle-locomotion-steering-and-recovery.md)).
- `00236780` is the New Game Minus flag (below), and "status id 12" is effect id 12 (above).

## The flag that suppresses experience is New Game Minus (FABLE, 2026-09-30)

*(Added 2026-09-30 (FABLE).)* `00236780` returns bit 14 of the battle-state block's flag dword `[[02EBF190]+4]`. The
battle-state block field map's writer census gives that bit exactly three writes, all in the scenario/preset apply
that `BattleSystem_InitializeAreaState` runs ([the SetSaveData presets](../11-Party/the-setsavedata-presets-test-battle-scenarios.md)
§2.2). Two carry the bit across the block reset, and one sets it from bit 2 of the request dword `02089344` and then
clears the request. Bit 2 is set by one 8-byte setter, which has two callers in the raw call index:
- the result callback of script verb `0x308B`, which the verb table names `btlAtelResetNgMinus`. Its one shipped call
  (in the `us` corpus) is in the title script `ttl_d01`, on the confirming choice, right before
  `fsttl_newgamestart()`. Verb `0x308A`, `btlAtelResetNgPlus`, does the same for bit 13 in `ttl_b01`.
- a native state handler, when its selection byte is `0x19`. The same handler makes the New Game Plus call when the
  byte is `0x1A`.

So a game started as New Game Minus carries the bit in its battle-state block, which the save keeps, and two things
follow: the per-recipient experience add is skipped (step 2), and the presentation EXP is zeroed (`00312505`–`00312513`).
The save finaliser copies the same bit into the save header, and that is the Save_Load_Settings crossing below.

Sources:
- the writer census: [the battle-state block field map](../11-Party/Battle-State-Block/the-battle-state-block-field-map.md)
  §2 (flag table, bit 14);
- the request bits and title scripts:
  [version stamps and what loading normalises](../19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/version-stamps-and-what-loading-normalises.md)
  (FV-2, "the two sibling bits").

What the code shows is the flag and its effect. The name "New Game Minus" is the verb's catalogue name, matched to
the title script that calls it.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. The image-address resolver fan-out is MECHANICAL and recorded in the registry.*

- **PlatformOnlineAchievements — SERVICE.** `BattleUnit_ProcessDefeatRewardsAndLoot` (`00312280`) fires counter 11
  with the licence points *(each recipient's awarded LP, `0xB` at `00312489`; and, through `00317090`, counter 17 —
  step 6; added 2026-09-30 (FABLE))*. ~~Its wrapper~~ Its callee *(corrected 2026-09-30 (FABLE): `00312280` calls it at
  `003122D5`; it wraps nothing)* `003171C0` fires counter 4 for the defeat and then asks the actor class nibble
  (see the next item) ([the achievement catalogue](../20-Platform-Online-Achievements/steam-integration-and-achievement-catalogue.md)
  AB-7 and crossings).
- **ActorEntity — SERVICE.**
  - `00312280` reads the defeated unit's world position.
  - `003171C0` asks `ActorRuntime_GetClassNibble` and skips class 3.
  - `00319490` resolves the party focus actor (`ActorHandle_ResolveRegistryEntryByPackedId`,
    `ActorWork_GetBattleUnitRaw`).
- **Presentation — SERVICE.**
  - The award is published through `Reward_PublishExpLpPresentation`.
  - `Loot_CreateWorldPickup` (`00319CA0`) picks the pickup's presentation tier
    (`Loot_DeriveWorldPickupPresentationTier`).
- **Movement — SERVICE.** `00312280` calls the 148-byte focus-actor helper, and that helper calls a 565-byte movement
  body.
- **Gameplay — SERVICE.** `00319A20` calls `0031E9F0` mid-loop at `00319AC0` — a `byte[rcx+9]` dispatch
  bounded at `0x1A` (`0031E9F0`–`0031E9F9`) that classifies the dying unit for the defeat path.
  (edge: `edges.tsv`)
- **Save_Load_Settings — CLIENT.** The 17-byte flag getter `00236780` (bit 14 of `[[02EBF190]+4]`) is also read by
  `SaveImage_FinalizeHeaderAndChecksum`. The same flag bit this page reads is therefore also consulted when a
  save header is finalised. ~~What the bit means is not read.~~ *Answered 2026-09-30 (FABLE): it is the New Game Minus
  flag (the section above).*

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**CombatFormula — SERVICE.** `00312280` on this page calls `BattleStats_GetByMappedBattleSlot`, owned by that layer. What it reaches is a 49-byte accessor over the battle stats table: the mapped slot byte is rejected above `0x27`, and the rest index `[02EBF190] + 8` at a stride of `0x1C8` - the same **40 records of `0x1C8` bytes** the battle runtime reset walks; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page.*

**CoreRuntimeScheduling — SERVICE, MECHANICAL (1 edge).** `EnemyChain_UpdateOnDefeat` (`00317ED0`) calls `00229E40` three times, a 7-byte getter of the dword at `01E02814` (10 in the file image), and branches on its value around the chain-count updates. The chain update reads one global setting through a scheduler-filed getter; ~~what the value means is not read here, and the page still does not claim what `00317ED0` does beyond that.~~ *answered 2026-09-30 (FABLE) by cross-reference: the dword is the locale id, and it moves the chain's clamp between 999 and 998 ([the chain page](the-chain-and-its-sticky-coin.md), pass-22 crossings); what `00317ED0` does is read there and in [the loot page](loot-drops-and-enemy-chain.md) §8b.*

**Audio — SERVICE, through the level advance (2 edges; added 2026-09-30 (FABLE)).** `BattleStats_AdvanceLevelToTargetAndRecomputeGrowth` (`0030C650`), which step 2 calls for each recipient, plays the level-up fanfare: it resolves bank-local sound 7 through `003A1180` and plays it through `002DF220` at centre pan `0x40` and full volume `0x7F` (`0030C831`–`0030C84B`; [what happens when a character levels up](what-happens-when-a-character-levels-up.md) §6). The defeat body itself calls no audio function. The fanfare belongs to the level advance, and a kill that raises no level plays none of it.

**Status_Periodic_Terminal — CLIENT (1 edge).** `BattleStats_ChangeStatusAndProcessSideEffects` (`0030E360`) calls `BattleUnit_ProcessDefeatRewardsAndLoot` (`00312280`) at `0030E884`, on the arm that first dispatches presentation event `0x200C` or `0x200E`. A status change is one of the routes into the defeat sequence this page describes: the status layer decides the unit is down, and this page's rewards and loot run from there.

**CombatAI — CLIENT, MECHANICAL (2 edges; added 2026-09-30 (FABLE), with the GR-19 answer).** The placement test the drop gate asks reads two helpers that CombatAI bodies also call: `0030F130` calls `ActorRuntime_GetClass3FloatPair` (`00265090`), and `003247F0` calls the nearby-actor gather `00391D10`. They are shared accessors (a unit's radius pair, a gather around a point); this page's reading of the drop gate does not depend on those callers, and no shared ownership is implied.

## The `00319CA0` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`00319CA0` (`Loot_CreateWorldPickup`, 394 B *(corrected 2026-09-30 (FABLE) from "~227 B": 227 B is the member
`00319A20`'s extent, `0xE3`; `00319CA0` is `0x18A`, the pickup pool page's 394 B)*) — pickup-create body under
a four-register save, `ebp = 0` accumulator (`00319CB4`).

| member | role | interior |
| --- | --- | --- |
| `00319A20` | large record body under a seven-register save (`00319A20`/`00319A36`) | [`00319A20`](../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none.

## Key addresses (FABLE, 2026-09-30)

*(Sections from here to Related added 2026-09-30 (FABLE). The addresses are the ones this page already cites, and each
body size is the function table's extent, `0x…` in parentheses.)*

| Address | Working name | Body | Role |
|---|---|---:|---|
| `00312280` | `BattleUnit_ProcessDefeatRewardsAndLoot` | 857 B (`0x359`) | the whole defeat sequence, steps 0–6 |
| `0030E360` | `BattleStats_ChangeStatusAndProcessSideEffects` | 1,323 B (`0x52B`) | its only direct caller (`0030E884`) |
| `00317ED0` | `EnemyChain_UpdateOnDefeat` | 529 B (`0x211`) | step 0: the chain |
| `003171C0` | — | 106 B (`0x6A`) | step 0: counter 4 and the species tally |
| `002F8BB0` | `Reward_ComputeExperienceForRecipient` | 430 B (`0x1AE`) | experience for a recipient, or for NULL |
| `002F90C0` | `Reward_ComputeLicensePointsForRecipient` | 179 B (`0xB3`) | LP for a recipient, or for NULL |
| `00236780` | — | 17 B (`0x11`) | the New Game Minus flag |
| `002F8F20` | — | 122 B (`0x7A`) | the experience curve the level walk searches |
| `0030C650` | `BattleStats_AdvanceLevelToTargetAndRecomputeGrowth` | 570 B (`0x23A`) | applies the level the walk stopped at |
| `00316A50` | — | 411 B (`0x19B`) | the achievement-counter updater (counters 11, 4, 17) |
| `0028FB80` | `Reward_PublishExpLpPresentation` | 88 B (`0x58`) | the EXP / LP presentation call |
| `00469E80` | — | 60 B (`0x3C`) | the gil-delta notifier (positive deltas only) |
| `00319490` | — | 148 B (`0x94`) | the drop gate (GR-19) |
| `003180F0` | `Loot_RollDropEntries` | 641 B (`0x281`) | the drop roll |
| `00319CA0` | `Loot_CreateWorldPickup` | 394 B (`0x18A`) | places the pickup |
| `00317090` | — | 78 B (`0x4E`) | step 6: counter 17 |

### Data addresses cited by this document (FABLE, 2026-09-30)

| Address | Name | Kind | Contents |
|---|---|---|---|
| `02EBF190` | battle-state block pointer | `.data` qword | its `+4` dword carries the New Game Minus bit 14 |
| `02089344` | load-route and new-game request flags | `.data` dword | bit 0 = the load came through load mode 3 (FV-2); bits 1 / 2 = the New Game Plus / Minus requests, consumed by the preset apply |
| `022C1740` | recipient scratch array | `.data` (zero-init) | the nine recipient pointers (`00312391`) |

## Call chain (FABLE, 2026-09-30)

```
a status change that downs an enemy
  BattleStats_ChangeStatusAndProcessSideEffects (0030E360), at 0030E884
    -> BattleUnit_ProcessDefeatRewardsAndLoot (00312280)        <- THIS PAGE, the owner transition
         -> EnemyChain_UpdateOnDefeat (00317ED0)                  chain
         -> 003171C0                                              counter 4, species tally
         -> per recipient: 002F8BB0, 002F90C0, 002F8F20 walk, 00316A50 (counter 11), 0030C650
         -> 002F8BB0(NULL), 002F90C0(NULL) -> 0028FB80           presentation
         -> GameState_GetGil / GameState_SetGil, then 00469E80   gil
         -> 00319490 -> 003180F0 -> 00319CA0                      drop
         -> 00317090 -> 00253770 -> 00316A50                      counter 17
```

**Upstream.** The status change is the only direct caller (the raw call index lists the one site `0030E884`). How HP
reaching zero becomes that status change is the lethal-transition page's subject
([the HP write](../08-Combat-Formula/Current-HP/the-hp-write-and-the-lethal-transition.md)). That is the trigger;
this function is the owner transition.

**Downstream.** Experience and LP land in the recipients' stats records (`+0x18C`, `+0x190`, the level `+0x1C2`
through the level advance). Gil lands in the party purse through the setter, which clamps and meters it
([gil storage](gil-storage-clamp-and-every-path-that-moves-it.md)). The drop becomes a world pickup. Three achievement
counters advance.

**Do not confuse with:** the level advance itself ([what happens when a character levels up](what-happens-when-a-character-levels-up.md)),
which this body only calls; and the unit's removal from the battle, which this body does not do (step 6).

## Modding notes (FABLE, 2026-09-30)

- **Best intervention point:** the two reward rows a unit caches at install (`+0xE70` / `+0xE78`). One authored change
  moves experience (`+0x34`), gil (`+0x30`), LP (`+0x2F`) and the counter-17 score (`+0`) together, and the defeat body
  needs no patch ([how a unit is built](../04-Actor-Entity/Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md)).
- **Regenerates itself:** the level. Writing `+0x18C` alone does nothing until the next kill's walk, and writing the
  level byte bypasses growth. Call the level advance instead.
- **Breaks if:** the caps are raised past what the setters and the level walk assume. Experience beyond the curve's
  level-99 answer cannot raise a level, and gil is clamped again by its setter whatever the caller asks.
- **Multiplayer / XIIOnline:** the defeat is one authoritative event, and its results (per-recipient experience and LP,
  gil, the drop, the chain) are world state that one peer should compute and broadcast. The presentation values are
  derived and local. The New Game Minus bit is per-save state, so two peers can disagree about experience for the same
  kill.
- **Mod compatibility:** the reward rows and the equipment augment bytes are authored data that other mods may edit;
  the effect-12 conversion follows whatever equipment carries augment 12.

## What is not known (FABLE, 2026-09-30)

Every entry is also a register row.

- [x] **Section 03's independent peer acceptance** (GR-16). The production review on which this page's corrections
      rest has had the owner's review but no independent auditor verdict. *(GR-16 answered 2026-10-01: SWE2-AUDIT-SEM's independent review `f41194772`, [record](../_index/candidates/auditsem-review-section03-1001/REVIEW.md), ACCEPT-WITH-NARROWING; register restated by OPUS for SWE2-DATA.)*
- [x] **What the drop gate's nearby-actor test decides** (GR-19) *(answered 2026-09-30, FABLE: whether the party leader could stand at the death position; see the answer above)*: the 565-byte body behind `00319490`, and so under
      what circumstances a kill leaves no loot. *(Narrowed 2026-09-30, C4: it is the shared placement test `003377C0` that DE-4 names; ~~open is what that test accepts.~~)* *(answered: GR-19's question is answered — the gate asks whether the party leader could stand at the death position, see the drop-gate answer above, "Answered 2026-09-30"; what the shared test accepts in full is a residual of the placement test, not of GR-19; 2026-10-02, OPUS)*

## Evidence (FABLE, 2026-09-30)

| Claim | Evidence | Tier |
|---|---|---:|
| one body, 857 B, does steps 0–6 in that order | complete body of `00312280` (`00312280`–`003125D8`) | 1 |
| only caller is the status change | raw call index: one site, `0030E884` | 1 |
| recipient admission, nine at most | `00312360`–`003123A1` | 1 |
| per-award and accumulated caps | the anchors in the caps table | 1 |
| New Game Minus skips the experience add and zeroes the shown EXP | `00312429`–`00312444`, `00312505`–`00312513`; `00236780` read whole | 1 |
| bit 14's writers and what arms them | the block field map's writer census; `02089344`'s rip-relative writers (`ripscan.py`, six sites, one sets bit 2); that setter's two raw callers; verb table row `0x308B`; `ttl_d01` in the decompiled script corpus | 1 (writers), 9 (script) |
| effect id 12 converts LP to gil | `00312409`–`00312425`; augment row 12 and `listhelp_ability.bin` 130012 with the 27 / 28 control | 1 (code), 9 (authored text) |
| counter 11 fed with each awarded LP, counter 17 with the row-word score | `00312489`–`00312496`; `00317090` read whole, `003170D3`–`003170D8` | 1 |
| the level walk stops at 99 | `002F8F20` read whole; `0031245A`, `00312473` | 1 |
| gil from the same rows as experience, four bytes apart | `0031251D`–`00312546` | 1 |
| the drop gate | `00319490` read whole; `00312588`–`003125B4` | 1 |

The SECTION-03 native controls and the retained-sample review are in the
[review](../_experiments/evidence/continuation-section03-reward-bindings/REVIEW.md).

**Superseded readings:** "…AndRetire" and the retirement step (2026-09-28, 2026-09-30); "status id 12" (2026-09-30);
counter 0x11's formula (2026-09-30); NULL implying an undivided award (SECTION-03).

## Related (FABLE, 2026-09-30)

- [How experience is computed and divided](how-experience-is-computed-and-divided.md) — the experience computer's note
- [Experience and License Point award](experience-and-license-point-award.md) — both computers, their gates and modifiers
- [Defeat-rewards contract](CONTRACT-defeat-rewards-sequence.md) — the invariants of this body
- [Loot drops and the enemy chain](loot-drops-and-enemy-chain.md), [the chain and its sticky coin](the-chain-and-its-sticky-coin.md), [the pickup pool](world-loot-pickups-the-ten-slot-pool-and-the-despawn.md) — steps 0 and 5
- [What happens when a character levels up](what-happens-when-a-character-levels-up.md) — the level advance
- [Gil storage and every path that moves it](gil-storage-clamp-and-every-path-that-moves-it.md) — step 4's setter
- [The achievement catalogue](../20-Platform-Online-Achievements/steam-integration-and-achievement-catalogue.md) — counters 4, 11 and 17.
  Its AB-8 census, as of HEAD 9aac223bf, says nothing feeds counter 17; step 6 feeds it. Routed to the page owner
  2026-09-30 (FABLE, `consumer-check-0930-dd7.md`).
