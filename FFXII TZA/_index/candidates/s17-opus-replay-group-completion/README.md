# S-17: group completion's invariants with the completion's callees real (OPUS, 2026-09-26)

**Evidence class: NATIVE-REPLAY (unicorn), `live_game: false`.**

**The gap.** S-17's runtime rests on EXP-011, which executed the completion logic with its three event-lock callees and the
dispatch **stubbed** (the contract's §13: *"The callee bodies (`00307140`, `00238B70`, `00238AE0` and the dispatch target)
are stubbed, so their outputs, ownership effects and scheduling are unproved"*). Live capture of the transition is still
absent.

## What was run

`check.py` runs over block 345's world (`../s25-opus-replay-enmity/check.py`, whose cases run first; `result.json` keeps md5
`49662471…`). Two foes are installed there by the shipped installer `0023A570` from a shipped area file. They are
spawn-backed (stats kind 1), each with its own spawn list at `+0x40`.
- **Registration** goes through the verb's own native target, `00239710(actor, mode, group)` (verb `0x3030`'s tail). It sets
  the unit's group byte `+0xE98` and calls `00306E60`.
- **The only planted field** is each unit handle's `+0x30` back-pointer, as in `commit_walk.py`.
- **The group ledger** is the image's BSS at `02EC13C0`: `0x18` bytes per group, 1-based.
- **Each scenario starts** with the ledger reset `00307090`, as an area entry does.
- **No application stub.**

**8 / 8 pass; `result.json` is byte-identical over two runs (md5 `8ed61e4a…`).**

| case | contract invariant | observed |
|---|---|---|
| `G1_registration_sets_member_bits` | registration | two foes into group 1: group bytes 1 / 1, `memberMask` = 3, `deadMask` = 0 |
| `G2_death_recorded_no_completion_while_a_member_lives` | completion is a mask test | F0's death sets `deadMask` = 1 and returns 0. Nothing else runs |
| `G3_death_is_idempotent` | a death is idempotent | F0 dying again changes nothing |
| `G4_last_death_completes_with_real_locks_and_dispatch` | completion | F1's death returns **1**. It runs, **for real**, `00307140(1)`, `00238B70(1)` and `00238AE0(1)`; `02089340` gains bits `0x20` and `0x80`. It then runs **`003299B0(unit, 0x2005)`**, and the ledger flag `+0x10` bit 0 rises |
| `G5_outsider_death_cannot_complete` | a member outside `memberMask` never completes | with F1 unregistered (`00306E60(F1, 0)`, so `memberMask` = 1), F1's death returns 0. F0's death then completes the group |
| `G6_reregistration_clears_dead_bit_no_one_shot` | registration clears the dead bit; no one-shot | after a completion, re-registering F0 clears its dead bit (`deadMask` 3 → 2). F0 dying again **completes the group a second time** |
| `G7_group_zero_registers_nothing` | the group id is 1-based | `00239710(actor, mode, 0)` leaves the group byte 0 and every ledger unchanged, and that unit's death returns 0 |
| `G8_reset_zeroes_masks_clears_flag_bit0_only` | the reset | over all 64 entries, both masks become 0 and flags `0xFF` becomes **`0xFE`**: bit 0 only |

## Not covered

- The per-frame consumer `00307030` and the field-table post `0026ADC0`, slot 3.
- The flag raise after the death reaction, `00307110`.
- **A live capture of the transition.** That is the contract's own §13 debt.
