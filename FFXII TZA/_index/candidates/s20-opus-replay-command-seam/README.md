# S-20: the native command seam and the commit funnel executed, and followed into the dispatch (OPUS, 2026-09-25, block 351)

**Evidence class: NATIVE-REPLAY (unicorn), `live_game: false`.**
[`CONTRACT-native-command-seam.md`](../../../07-Combat-Action/CONTRACT-native-command-seam.md) §13 reads *"None. No
experiment executes this seam."* This harness runs:
- the intent seam `BattleUnit_IssueCommand` (`00311CF0`);
- the commit funnel `BattleUnit_CommitAction` (`0030F760`);
- the handler-table dispatch `00305080`, to close the chain.

It tests CS-1, CS-2 and CS-5.

## What was run

`check.py`, with `world.py` / `world.json` / `printf_bridge.py` / `shipped_pack.py` from block 350. **No application
stub.**

**One stop boundary, in CS-5 only:** the entry of the handler `table[5]` = `002FDA60`, which the dispatcher tail-jumps to
(block 350's boundary).

**Fixtures:**
- six idle objects at `0x76300000`;
- unit 0 (`+8` its id `0x100001`, `+0x10` a zeroed handle object, `+0x698` battle-state row 0);
- a zeroed order context;
- status words, where a case sets them.

**4 / 4 pass, and `result.json` is byte-identical over three runs** (md5 `c1302ba72f7a94efe5f4fa58b3eb312c`).

| case | contract item | observed |
|---|---|---|
| `CS1_seam_records_pending_not_commit` | CS-1 | See the CS-1 list below |
| `CS1_seam_refusals` | CS-1 | See the refusals table below |
| `CS2_commit_writes_the_three_fields` | CS-2 | `0030F760(unit, ctx, id 0x4005, focus 0x100001, reset)` stores `+0x708` = ctx, `+0x710` = focus, `+0x714` = id and phase `+0x6B4` = 0 (from 7). Its fifth argument runs the reset `003105D0` first; without it the reset is not entered |
| `CS5_dispatch_reads_the_committed_id` | CS-5 | After the seam alone (`+0xBA0` = `0x4005`, `+0x714` = 0), the dispatcher returns **−1**. After the commit it reaches `table[5]` = `002FDA60` |

**CS-1, the seam.** `00311CF0(unit, target, r8b, command 0x4005)` returns 0 and records the command as **pending**:
- `+0xBA0` = `0x4005`;
- `+0xBB8` = the target, or the unit's own id from `+8` when the target is 0;
- then it calls `00317E60`.

It writes **nothing** in `+0x708..+0x71F`.

**The seam's refusals.** Three refusal paths give two return values, and none records anything:

| condition | returns |
|---|---|
| a status bit in `0x8800203B` only (bit 3) | **0**, the same value as success |
| status bit 0 (`0x80000003`, with `00377C20` false) | **−2** |
| command `0x113` over a current `0x113` | **−2** |
| a null stats pointer | **−2** |

## What the execution adds

1. **The seam does not commit.**
   - CS-1 calls `00311CF0` the intent seam and CS-2 calls `0030F760` the commit funnel. Measured: the seam records a
     **pending** command at `+0xBA0` / `+0xBB8` and never touches the commit fields.
   - A dispatch after the seam alone sees `+0x714` = 0 and returns −1.
   - So intent and commit are separated in time, and something else (not read here) carries `+0xBA0` into the funnel.
2. **A refused command and an accepted one can return the same value.** A status in `0x8800203B` but not in `0x80000003`
   returns **0** with nothing recorded, exactly what success returns. The caller cannot tell them apart from the return
   value.
3. **CS-5 closes as an execution.** The commit's `+0x714` is what the dispatch reads: the committed id `0x4005` reaches
   `table[5]`, and the pending one does not.

Routed to FABLE.

## Not covered

- the step that moves a pending command (`+0xBA0`) into the commit funnel;
- CS-3 / CS-4 (the two 64-entry rings);
- CS-2's image-wide writer census (static, already measured by the contract);
- the funnel's later preparation calls beyond what this fixture reaches;
- a live game.
