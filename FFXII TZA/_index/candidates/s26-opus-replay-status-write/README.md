# S-26: the status write's five invariants executed with no stubbed callee (OPUS, 2026-09-26)

**Evidence class: NATIVE-REPLAY (unicorn), `live_game: false`.**

**The gap.** S-26's runtime cell reads: *"`CONTRACT-status-write`'s five invariants rest on EXP-086's stubbed run"*.
EXP-086 `ret`-stubbed fourteen callees of `0030E360`.

**What this harness runs.** `BattleStats_ChangeStatusAndProcessSideEffects` (`0030E360`), over block 348's world
(`../s32-opus-replay-level-advance/check.py`, imported: its five cases run first, and its `result.json` md5 `82259cd6…`
is unchanged).
- The static closure of `0030E360` is allowed, with **no application stub**. Every callee EXP-086 stubbed runs as
  shipped when it is reached.
- The status definition table is the shipped `battle_pack`'s, bound by shipped code.
- **Fixtures:** the target is battle-state row 0, zeroed per case with the named words planted. There is no source,
  and no owning unit.

**10 / 10 cases pass, and `result.json` is byte-identical over two runs** (md5 `0951776445d905875546e008e22f8508`).

| case | invariant | observed |
|---|---|---|
| `I1_mode5_sets_+38_and_fires_nothing` | 1 | mode 5 on an absent status sets `+0x38` bit 4. **No side-effect function is entered**, and there is no re-entry |
| `I1_I2_bit_written_into_the_other_word_fires_nothing` | 1, 2 | adding into `+0x64` while `+0x3C` holds the bit writes the bit and fires nothing. The same holds for `+0x3C` while `+0x64` holds it |
| `control_presence_change_fires_side_effects_with_real_callees` | control | adding from absent (flags `0x200`) sets `+0x3C` and enters the extra-effect `0046A800`. The instrument does see side effects when presence changes |
| `I1_addendum_the_real_recompute_rewrites_+3C_after_the_add` | 1 (addendum) | with flags 0, the add sets the bit, and then the **real** recompute `0030FED0` zeroes and rebuilds `+0x24..+0x47`, including `+0x3C`, from the record's other state. **Invariant 1's addendum ("the presence word is not this operation's alone"), executed** |
| `I3_every_mode_refuses_when_already_in_the_requested_state` | 3 | for all six modes (clears on an absent bit; adds on a present bit): the three words, `+0xBC[]` and `+0x13C[]` are unchanged, and there is no side effect and no re-entry |
| `I4_cascade_calls_are_mode_0_and_one_level_deep` | 4 | status 10 → one inner mode-0 clear (status 25); status 20 → one (status 15). **KO → 25 inner mode-0 calls**, all at one depth |
| `I4_present_bit_cleared_absent_bit_refused` | 4 | a present bit 25 is cleared by the inner call. An absent one is refused inside the inner call (only the outer add lands) |
| `I5_no_heap_import_and_no_operator_new_in_any_case` | 5 | no `malloc` or `_aligned_malloc` import, and no `operator new` (`00210EC0`) entry, in any of the 16 calls |
| `no_fence_no_fault_in_any_case` | — | every call returns |

**EXP-086's stubbed callees that ran real here:** `0031B860` (the owning-unit search), `0030B9B0` and `0030B8E0` (the
eligibility gates), `0030FED0` (the recompute) and `0046A800` (the extra effect).

## With an owning battle unit: §10 row 3 and the unit-dependent side effects (OPUS, 2026-09-26, `row3.py`)

`row3.py` runs `0030E360` on a battle-state row that **a unit owns**. It uses block 345's world
(`../s25-opus-replay-enmity/check.py`, whose cases run first; `result.json` keeps md5 `49662471…`), which installs party units
whose `+0x698` is a battle-state row. The owner search `0031B860` runs as shipped. **No application stub.** The type byte `+4`
of party row 0 is planted per case, as block 345 plants it.

**The exception, read from the bytes** (`0030E467`–`0030E49C`):
- The trigger is an owning unit whose stats kind `+5` is 0 and whose type `+4` is in `0x1B`–`0x27` (`sub al, 0x1B` /
  `cmp al, 0xC` / `ja`), receiving a terminal status (`bit & 0x80000003`).
- It calls `00300FC0(unit, 0)` at `0030E497` and jumps to the exit, before any mask write.
- **In the shipped party table** (`battle_pack` directory `+0x44`), rows 27–39 are the thirteen **Espers**. So
  `0x1B`–`0x27` is exactly the Esper rows.

**5 / 5 pass; `row3_result.json` is byte-identical over two runs (md5 `677c0267…`).** KO is status 0, mode 3, flags `0x200`.

| case | observed |
|---|---|
| `E1_esper_rows_defeat_cleanup_only_masks_untouched` | types `0x1B` and `0x27`, both ends of the band: `00300FC0` is called with the owning unit and 0. There is **no reaction and no rewards**, and `+0x38` / `+0x3C` / `+0x64` are untouched |
| `E2_outside_the_band_the_full_KO_path_and_the_bit` | types `0x1A` and `0x28` (just outside) and `0x00` (Vaan's row): the full KO path runs, **reaction `003284D0` → defeat cleanup `00300FC0` → rewards `00312280`**, and the KO bit lands in `+0x64` |
| `E3_nonterminal_on_an_esper_row_is_written_no_defeat` | status 5 on an Esper row is not the exception: the bit is written, and `00300FC0` is not called |
| `E4_removing_KO_clears_the_bit_then_enters_the_recovery_boundary_00238BF0` | removing KO from the Vaan row (mode 0) clears the bit first, then enters the recovery `00301140`. **Recorded boundary:** the recovery calls `BattleUnit_RefreshActorRuntimeFromDefinition` `00238BF0`, which reads the unit's actor runtime. That is a zeroed fixture handle in block 345's world, and it faults there, so the recovery's own effects are not executed |
| `no_fault_except_the_recorded_boundary` | every other run returns |

## Not covered

~~The unit-dependent side effects are not reached, because no battle unit owns the record~~ (in `check.py`; `row3.py`
runs them with an owning unit, above). What remains:
- the event dispatch `003299B0`;
- the recovery's own effects past `00238BF0` (the actor runtime; `row3.py` E4);
- `00377C20`, `00300140` and `00307D10`;
- `003112F0` (unreachable in the shipped build, per EXP-086 F1);
- a live game.
