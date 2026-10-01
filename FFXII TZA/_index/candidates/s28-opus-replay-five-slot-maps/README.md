# S-28: slot maps, battle-state block, roster, focus and control suppression executed as shipped code (OPUS, 2026-09-25, block 338)

**Evidence class: NATIVE-REPLAY (unicorn), `live_game: false`.** S-28's exposure note (block 301) found three of the
row's four contracts with no execution, among them `CONTRACT-the-five-parallel-slot-maps.md` (SM-1..SM-8). This harness
executes its bodies as shipped code: the initialiser `00329CC0`, the refresher `BattleGroup_RefreshFourActorDefinitions`
(`003266C0`) and the resolver `BattleSlotMap_ResolveMappedBattleSlot` (`0031B9F0`).

## What was run

`check.py`, with `world.py` / `world.json` / `printf_bridge.py` / `shipped_pack.py` from block 337. The `battle_pack`
tables are bound by shipped code. **No application stub and no stop boundary.**

**Fixtures:**
- six idle objects;
- the map region's prior contents: zeroed, or a stale `5A5A` fill;
- map 0 selectors where a case sets them.

**3 / 3 pass, and `result.json` is byte-identical over three runs** (md5 `5113bbdbdbba555aa819190b8dd29f17`).

| case | contract item | observed |
|---|---|---|
| `SM4_SM8_born_identical` | SM-4, SM-8 | See below |
| `SM5_refresh_order` | SM-5 | With map 0 = `0100..0108`, afterwards: **map 3 = map 0** (copied before the clear); map 1 keeps `[0..3]` and has `[4..8]` = `FFFF`; **maps 2 and 4 equal the cleared map 1** |
| `SM1_SM2_SM3_resolver` | SM-1, SM-2, SM-3 | The resolver returns the **low byte** of the `u16` selector: `0x1234` → `34`, an empty `FFFF` → `FF`, `0x00AB` → `AB`. An id past the class-23 gate (9) **and** class 5 both return `FF`, through the same epilogue. Class 3 reads map 3 |

### SM-4 and SM-8, over two starting states

- **Zeroed maps.** `00329CC0` writes map 0 from the authored table at `01EED260` (`00 FF FF FF FF FF FF FF FF` in the
  shipped image; `0xFF` becomes `FFFF`), then copies it into maps 1–4, so all five are identical. `+0x5AA4` holds the
  table's first byte.
- **Stale selectors `5A5A`.** For a `0xFF` table entry, the initialiser first releases the member the **old** selector
  names (`00323540`), and writes `FFFF` only if that old low byte is ≤ `0x27`. With `5A` it **skips the write**. The
  stale `5A5A` survives in map 0, and the copies carry it into maps 1–4.

## The battle-state block — `check_block.py`

`CONTRACT-battle-state-block.md` (BS-1..BS-5), run the same way: the binder `00233C10` in every arm and the reset
`002370C0`, with the resolver reading the result. **No application stub and no stop boundary.**

**2 / 2 pass, and `result_block.json` is byte-identical over three runs** (md5 `864f8597cbcab9e7b979bbd9b4690777`).

| case | contract item | observed |
|---|---|---|
| `BS1_BS2_binder_arms` | BS-1, BS-2 | See the arms table below |
| `BS3_BS5_reset_leaves` | BS-3, BS-5 | The reset zeroes exactly `0x7410` bytes and **rewrites the magic** `05071901`. It fills **only map 0** with `FFFF`; maps 1–4 stay 0. So the resolver answers `FF` for class 0 and **`00`** for classes 1–4, a slot-zero reading |

The binder's arms, measured:

| arm | what runs |
|---|---|
| unbound | The cell becomes **the active save buffer + `0x4E68C`** (BS-1), and `BattleSystem_ResetRuntimeState` `00237DF0` runs **twice**, each time running the block reset. The second run takes a block whose magic the first already wrote |
| bound, magic wrong | The reset runs once, and the body is not entered |
| bound, magic right, reference matching | The body at `00233C5E` runs, and no reset |
| bound, magic right, reference differing | The reset runs once, and the body is not entered |

**Finding: the magic-right arm depends on a comparison BS-2 does not list.** The binder's first call, `00235AF0`
(`00233C14`), compares the block with a reference image at the active save buffer + `0x2200`: the magic, the flag
dword, `+0x5B42` and `+0x5B12`. When they differ, it rebuilds the block, and the magic test then sends it to the reset.
So "bound with the right magic → neither" holds only when the block already agrees with that reference. Routed to
FABLE with the SM-4 note.

## The roster — `check_roster.py`

`CONTRACT-party-slot-assignment.md`, run the same way: the per-slot writer `PartyRoster_AssignActorToSlot` (`00269C70`),
the bulk clears `002695A0` / `0026DB30`, the pending-mask consumer `0025BFB0` and the reader `00263750`. **No application
stub and no stop boundary.** The fixtures are five planted `ActorStorageRecord`s (`+0x12`, `+0x0F`, a zeroed `+0xC0`
context each).

**3 / 3 pass, and `result_roster.json` is byte-identical over three runs** (md5 `fcf9bdf7bb8ae734318bb27abe81f5fd`).

| case | contract item | observed |
|---|---|---|
| `writer_keeps_its_own_side_only` | the invariant, §4 | See below |
| `bulk_clears_break_it` | §4 exception, §7 | `002695A0`, `0026DB30` and `0025BFB0`'s bit-0 arm zero the roster and **touch no record**: every former member keeps `+0x12` = its slot. `0025BFB0` without bit 0 leaves the roster |
| `readers` | §2 | `00263750` returns the occupant, and NULL past slot 3 |

**The per-slot writer does NOT maintain the invariant on its own**, which contradicts the contract's *"Both per-slot
writers maintain it"*. Measured:

- **Records 0..3 into slots 0..3:** roster `[0,1,2,3]`, each `+0x12` = its slot, `+0x0F` = 2. The bijection holds.
- **Assigning a record over an occupant (record 4 into slot 2):**
  - The writer vacates the **incoming** record's old slot and resets that record (`00269CB7`–`00269CD9`).
  - The **displaced occupant** (record 2) keeps `+0x12 = 2` and `+0x0F = 2`. Only its context's `+0x152` is set and
    `002681E0` called (`00269C91`–`00269CAD`).
  - So roster[2] = record 4 while record 2 still believes it holds slot 2. **The writer itself breaks the bijection.**
  - The same holds when moving record 0 over record 3.
- **A null actor** stores nothing (`00269CB5`).
- **Slot 7:** the eviction block is guarded by `cmp ebx, 3` / `ja`, but the store at `00269CE1` only tests the sign
  (`js`). So slot 7 is **stored at roster[7], past the four-entry array at `0209A1F0`**, with `+0x12` = 7 and
  `+0x0F` = 3. Any positive slot above 3 writes out of bounds.

## Focus and control suppression — `check_focus.py`

`CONTRACT-party-focus-and-control-suppression.md` PF-3 to PF-8, run as shipped code with **no application stub and no
stop boundary**:
- the request `003594B0` and the summon upgrade `003594C0`;
- the commit `00358BB0` → `00358BC0`, with its real release `00358B40`, teardown `0025A6A0` (both thunks) and push
  `002681D0`;
- the suppression recompute `0023B040`, through the real leader derivation `003272A0` (`003590D0` → `003588B0` →
  `00263E30`).

**Fixtures.** The leader chain EXP-145 disclosed:
- the focus handle;
- the enable bit;
- the manager `00263FF0` returns;
- two objects and their leaders.

It adds the leader's current motion, so that the class tests `00322920` / `00322600` give a clean baseline:
- motion entry 0 of the `0x740` table behind `[022C6F28]`: `+0x284` set, `+0xC8` = −1, `+0xCC` = `0x2001`;
- leader `+0x5C` = `0x2001`.

**6 / 6 pass, and `result_focus.json` is byte-identical over three runs** (md5 `e34f42f4a1f18ad553b44688bd9f8129`).

| case | contract item | observed |
|---|---|---|
| `leader_derived` | §2 | `003272A0` resolves the focus handle to the planted leader |
| `PF3_deferred_until_commit` | PF-3 | The request writes pending and kind 1 and moves nothing: the leader getter still returns the old leader. The commit installs the new handle |
| `PF4_redundant_commit_still_pushes` | PF-4 | With pending = current, `00358BE4` jumps straight to the store (no release, no teardown, no re-read). The store, the kind clear, the resolve and the push all still run |
| `PF5_PF6_order_and_the_summon_call` | PF-5, PF-6 | See the commit order below |
| `PF7_bit14_raises_0_and_2_only` | PF-7 | See the suppression-bits table below |
| `PF8_null_stats_faults_mid_function` | PF-8 | A leader whose `+0x698` is null passes the first check. The unguarded second load **faults at `0023B15E`, reading `0x64`** |

**The commit order for a real change:**
1. release the outgoing leader (`00358B40`), which pushes;
2. `00259800`;
3. the teardown;
4. **only then** re-read pending, store it, clear the kind, resolve, and tail-push.

Kind 1 takes thunk `0025A680` (flag 1). Kind 2, set by the summon upgrade, takes `0025A690` (flag 0), and **only that
path calls `003D9B80`**. The commit does not clear the pending handle.

The suppression bits, read at the three setters:

| status | bit 0 | bit 1 | bit 2 |
|---|---|---|---|
| 0 | clear | clear | clear |
| **bit 14 only** | set | **clear** | set |
| bit 3 | set | set | set |
| bit 27 | set | set | set |
| gate bit 1 | set | set | set |

So `0x8800403B` and `0x8800003B` differ by bit 14 alone.

## What the execution adds

1. **SM-1 to SM-5 and SM-8 are executed.** In particular SM-5's copy order is observed: map 3 is taken before the clear,
   and maps 2 and 4 are taken from the cleared map 1.
2. **SM-4's initialiser is conditional per entry.** It does not unconditionally write the authored table. A `0xFF`
   entry is written only after releasing the previous selector's member, and a previous selector whose low byte is
   above `0x27` blocks the write. So *"all five are born identical"* holds, but *"from the authored table"* holds only
   over a map region whose old selectors are valid or zero. Routed to FABLE.

## Not covered

- SM-6 and SM-7 (the `PartyConfiguration_*` writers of map 0);
- BS-4 (a carried field map), `00266530`'s record-init assignment, `00263770`'s focus arm, SM-6 / SM-7, and PF-1 / PF-2 (image
  censuses);
- a live game.
