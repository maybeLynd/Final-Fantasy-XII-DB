# S-25: the gambit walk executed with its real evaluator (OPUS, 2026-09-26)

**Evidence class: NATIVE-REPLAY (unicorn), `live_game: false`.** S-25's runtime cell says that `CONTRACT-gambit-walk`'s
invariants *"rest on EXP-095's stubbed walk"*. EXP-095 scripted the evaluator and `ret`-stubbed the commit and the slot
resolver. This harness runs the walk `00305CC0` with its **real** evaluator `003014C0`, and the real commit on the
path.

## What was run

`check.py` loads block 332's world (`../s21-opus-replay-applier-stub-free/check.py`) under its own module name. That
world's cases run first, unchanged. It supplies:
- the image and the IAT traps, with memset bridged by name;
- the shipped battle_pack bindings;
- the unit pool.

**No application stub.** The allowed set grows by the static closure of `00305CC0`.

**The evaluator is kept on the path §4a documents.** With bit 5 of `[02089340]` ("combat AI suspended") set,
`003014C0` returns 0 at `00301511`. Every order is therefore offered to the real evaluator, nothing is committed, and
the walk's own logic is what is measured. **Planted data only:** a gambit set (count bytes from `+0`, 24-byte orders from
`+0x20`) and the unit.

**4 / 4 pass, and `result.json` is byte-identical over two runs** (md5 `468798ad7cc9da5852cd06f0366a7760`).

| case | contract item | observed |
|---|---|---|
| `G1_first_order_is_the_prefix_sum_and_one_offer_per_count` | §4 | the counts are `[2, 3, 1, 0, 4, 5]`. Subgroups 0, 1, 2 and 4 offer orders from `+0x20 + (sum of the preceding counts) × 24`, one per count, 24 bytes apart: offsets `0x20, 0x38`, then `0x50, 0x68, 0x80`, then `0x98`, then `0xB0 …`. Both the two-accumulator loop and the odd leftover are exercised |
| `G2_empty_subgroup_and_null_set_offer_nothing` | §4 | subgroup 3 (count 0) offers nothing and returns 0. A null set returns 0 |
| `G3_count_byte_reread_every_iteration` | §4 (added 2026-09-11) | a disclosed perturbation rewrites the count at the evaluator's entry. `set[4]` 4 → 2 on the second offer stops the walk after 2; `set[1]` 3 → 5 on the first offer makes it offer 5. **The count is re-read on every iteration, not latched** |
| `G4_bit5_evaluator_decodes_the_order_then_returns_no_commit` | §4a | with bit 5 set the evaluator returns 0 and **the commit is never reached**. But it does **not** return "before doing anything": ahead of the test it zeroes `*param` and decodes the order through `00308EC0` into `*out`. `00308EC0` and the cookie check are the only functions entered below it. **§4a is corrected accordingly** (OPUS's own contract) |

## A walk that commits, with the real evaluator, target selectors and commit (OPUS, 2026-09-26, `commit_walk.py`)

**The gap.** The two items above: the evaluator with bit 5 clear, including the target-selector evaluator `00301AD0`, and a
walk that commits. EXP-095 stubbed both `00301AD0` and the commit `0030F760`.

**The world.** `commit_walk.py` runs over block 345's world (`../s25-opus-replay-enmity/check.py`, whose cases run first;
`result.json` keeps md5 `49662471…`). Its foes are installed by the shipped installer `0023A570` from a shipped area file.
**No application stub.**

**The gambit list is authored, not planted:**
- the shipped preset loader `00327CB0` reads **preset 11** (`0x500B`): *Foe: flying → Telekinesis; Foe: party leader's
  target / targeting self / targeting ally / nearest visible / any → Attack*;
- the gambit screen's commit `003282D0` banks it and rebuilds the runtime set through `00328140`;
- the foe's grudge is written by the shipped enmity writer `00321850` (20 → 30, E-6a's first-grudge boost).

**Disclosed fixtures and bindings:**
- `[02EBF0D8]` (the gambit target conditions) is bound by `00238880`'s first call, as block 332 makes `00237FC0`'s. The
  menu lookup (heap 6) is not built.
- Unit byte `+0` bit 4 is set on both units: the evaluator's gate `0030151A`.
- Each unit handle gets its `+0x30` back-pointer and a zeroed definition at `+0xC0`, so `002E9C00` returns 0. The handles'
  matrices are zero.
- The party unit's sighted buffer `+0xBC0` is planted as `{1, the foe's handle}`. The perception update is not run.
- `00217150`, reached by the real code through the thunk `00202D70` (a tail jump), is admitted to the allowed set.

**6 / 6 pass; `commit_walk_result.json` is byte-identical over two runs (md5 `63924898…`).**

| case | observed |
|---|---|
| `W1_authored_set_from_preset_11` | six records. Conditions `605A 6000 6004 6005 6001 6002`; actions `00AA`, then `0096` ×5 |
| `W2_first_match_commits_with_real_conditions` | line 1 (Telekinesis) is refused by `BattleAction_CheckActionAvailabilityReason` `002FFCF0` (non-zero) before any selector. Lines 2–4 pass it and reach `00301AD0`, which finds **no target**. Line 5 (*Foe: nearest visible*) finds one, the evaluator returns 1, and `0030F760` commits Attack (`0x96`). **Line 6 is never offered**, and the walk returns 1 |
| `W3_commit_block_names_the_committed_record` | `+0x708` = the committed record's address (`set + 0x20 + 4 × 24`), `+0x710` = the target, `+0x714` = `0x96`, and the copy at `+0x718` |
| `W4_no_grudge_no_target_no_commit` | control: with no grudge, lines 5 and 6 find no target, and nothing is committed (returns 0). **A party member's "Foe" relation takes only a foe that holds a positive grudge** (`0030BD6D`–`0030BDA7` → `BattleEnmity_HasAnyPositive` `00321840`) |
| `W5_resume_reaches_its_record_and_returns_1_unevaluated` | §6, on real committed state: a resume-mode walk over the same set evaluates lines 1–4, then reaches the record `+0x708` points at and **returns 1 without evaluating it**. No commit |
| `W6_resumed_commit_makes_the_third_call_with_the_latched_word` | §7's third call. `+0x714` is set to `0x4021` first (a disclosed perturbation, so the two words differ). A resume-mode walk over party row 1's set commits line 5, and the success tail calls **`004697C0([unit + 0x698], 0x96, 0x4021, 4)`**. W2's normal-mode commit makes no third call |

**Two corrections to my contract (§7), from W2, W3 and W6:**
- **The stack slot initialised to `0xFFFF` is the action, not the target.** `[rsp+0x70]` receives the evaluator's decoded
  action id (`00301500`) and goes to the commit as `r8w`. `[rsp+0x30]` (initialised to 0) receives the target id
  (`003017E7`) and goes as `r9d`.
- **The third call's second argument is that action word** (`00305E44`), not "the resolved target word".

## Not covered

- the perception update that fills the sighted buffer `+0xBC0` (planted in `commit_walk.py`), and target selection among
  several candidates;
- a real commit refusal after a matched condition (FABLE's §7 qualification: the band bound cannot refuse one);
- a live game.
