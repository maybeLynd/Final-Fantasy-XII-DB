# S-20: the moment an action is committed (CM-1..CM-6) executed as shipped code (OPUS, 2026-09-26)

**Evidence class: NATIVE-REPLAY (unicorn), `live_game: false`.** S-20's runtime cell lists CM-1..CM-6 as not covered.
`CONTRACT-the-moment-an-action-is-committed.md` has two entries: the commit `0030F760` and the cancel `003105D0`. This
harness runs both.

## What was run

`check.py` imports block 332's world (`../s21-opus-replay-applier-stub-free/check.py`). That world's cases run first and
unchanged; its `result.json` keeps md5 `baf273ee…`. The world supplies:
- the image and the IAT traps, with memset bridged by name;
- the shipped battle_pack bindings;
- the unit pool with two planted units whose `+0x698` are stats records.

**No application stub.** The allowed set grows by the two entries' static closures.

**Signature**, read from the prologue: `0030F760(rcx = unit, rdx = a qword stored at +0x708, r8w = action id, r9d =
target id, [rsp+0x28] = cancel first)`. The target resolves through `0031B7E0`, which returns null while the leader
gate `[02089340]` bit `0x10` is clear. That is the world's default, and it serves as the "target does not resolve" case.
The target buffer is at unit `+0x778`: a flag byte at `+0`, the count at `+4`, and entries at `+8 + 16i`.

**5 / 5 pass, and `result.json` is byte-identical over two runs** (md5 `9577e70c9a61a3589fca495e98f6d92b`).

| case | contract item | observed |
|---|---|---|
| `M1_unresolved_target_is_not_an_error_and_appends_a_null_entry` | CM-1, CM-4 | action `0x10` with an unresolved target: the commit completes. The buffer (count 3, flag bit 0 set) is reset **keeping bit 0**, and **a null entry is appended**: count 1, entry 0 = 0 |
| `M2_two_disjoint_ranges` | CM-2 | ids 0, `0x21E`, `0x4000` and `0x4166` are accepted (block written, target `0x120034` stored). `0x21F`, `0x3FFF` and `0x4167` are refused: no command block is written |
| `M3_high_range_never_touches_the_target_buffer` | CM-3 | id `0x4010` writes the command block. **There is no write into `+0x778..`**; count 3 and entry `0x1111` survive |
| `M4_block_shadowed_verbatim` | CM-5 | `+0x700` has its low two bits cleared, `+0x708` = rdx, `+0x710` = target, `+0x714` = id. `+0x700..+0x717` is copied verbatim to `+0x718..+0x72F` |
| `M5_cancel_is_a_no_op_without_unit_or_stats` | CM-6 | the cancel with a null unit returns. With `+0x698` = 0 it returns **without a single write to the unit** |

## CB-2 / CB-6: the combo continuation executed (OPUS, 2026-09-26, `cb26.py`)

`cb26.py` loads `check.py` under its own module name, and both suites run first, unchanged. It runs the continuation
`0030FA00` with the real gate `0030C010`, the real commit and the real cancel inside it. **No application stub.**

**Planted data only**, chosen so the gate passes:
- `[01E0C2B8]` = 1;
- target-buffer entry 0 non-null, with `+0x788` bit `0x400`;
- `[022C2160]` = 0;
- a target handle `1 << 20` that resolves to unit 1: leader gate bit `0x10`, and descriptor 0 at `02098E10` pointing at
  an object with generation 1 whose `+0x30` is the unit.

**3 / 3 pass; `cb26_result.json` is byte-identical over two runs (md5 `4b340877…`).**

| case | observed |
|---|---|
| `A_success_recommits_its_own_action_and_advances` | the commit receives the unit's **own** `+0x708` (`0xABC`), `+0x714` (`0x10`) and `+0x710` (`1 << 20`), with cancel-first 1. The cancel runs and **clears `+0x6B7`/`+0x6B8` with its word store at `003106EB`**. The commit succeeds; then `0030FA65` writes the partner back (`0x77`), the counter goes 2 → **3**, `+0x6B4` = 5, and the call returns 1 |
| `F_failed_recommit_returns_0_after_the_cancel_ran` | the unit's `+0x714` = `0x21F`, which CM-2 refuses: the commit's cancel has **already run** when it refuses. `0030FA00` returns 0 without restoring, so **the counter ends at 0 and the partner at 0**. They are not left untouched |
| `G_gate_refusal_touches_nothing` | gate refused (`[01E0C2B8]` = 0): return 0 before any commit or cancel. Counter 2 and partner `0x77` are untouched |

**A correction to CB-2, routed to FABLE (the contract's author).** *"A failed commit returns 0 with the counter
untouched"* holds only when the **gate** refuses. When the re-commit itself fails, its cancel-first has already zeroed the
counter and the partner, and `0030FA00` does not restore them on that path. CB-1 (the width census) is a static fact.

## Not covered

- ~~the resolved-target path of a fresh commit, where it goes on to `0030AB40` (broadcast / enmity);~~ executed by `resolved.py` (next section);
- CS-3/4/6 (the command seam);
- a live game.

## The resolved-target continuation executed: `resolved.py` (OPUS, 2026-09-26)

`resolved.py` loads `cb26.py`, which loads `check.py`, which loads block 332's world. **All their cases run first,
unchanged**, and `result.json` / `cb26_result.json` are byte-identical before and after.
- It plants cb26's resolving target (handle `1 << 20` → unit 1), and runs the commit `0030F760` with that target.
- **No application stub.**
- **Planted data per case:**
  - both units' byte `+0` bit `0x10` (the classifier's eligibility bit);
  - the target's stats kind byte `+5`;
  - the actor's status bit 5;
  - the group dwords `+0x24`, and the actor's `+0x08`;
  - a status-mask bit on unit 1.

**The classifier `0030AB40`, read whole.**
- It returns 0 if either unit is null, either class `00263C20(+0x10)` is 5, or either unit lacks bit `0x10`.
- Otherwise it returns `1 + (bit5(actor status) == same_side)`. So it returns **2** for an opposite-side pair with the
  actor unconfused, or for a same-side pair with the actor confused.
- **The commit walks only when the relation is > 1** (`0030F8CA`).

**7 / 7 pass, and `resolved_result.json` is byte-identical over two runs** (md5 `f33c1358b2fde271a9b412c1ae6b2504`).

| case | observed |
|---|---|
| `R1_relation_2_walks_the_group_writes_754_then_750` | an opposite-side target → relation **2**. `0030F8CF` writes actor `+0x754` = the target handle. The walk (`0030F920`) writes `+0x754` on **every unit of the actor's group** (both units). `0030F931` writes actor `+0x750` = the handle |
| `R2_relation_1_skips_the_whole_walk` | a same-side target with the actor unconfused → relation **1**: no `+0x750` / `+0x754` write at all |
| `R3_confused_actor_on_same_side_is_relation_2` | the same pair with the actor's status bit 5 set → relation **2**, and the walk runs |
| `R4_only_the_actors_group_is_written` | unit 1 in group 7 → it is not written; the actor still is |
| `R5_actor_handle_not_equal_group_skips_the_walk_after_the_first_store` | actor `+0x08` ≠ `+0x24` → the walk is skipped, but `+0x754` (`0030F8CF`) and `+0x750` (`0030F931`) are still written, as the contract's pseudo-code places them |
| `R6_status_masked_unit_skipped` | unit 1 with status `+0x3C` & `0x80000003` → skipped (the field bit-15 override is clear) |
| `no_fault` | every run returns |
