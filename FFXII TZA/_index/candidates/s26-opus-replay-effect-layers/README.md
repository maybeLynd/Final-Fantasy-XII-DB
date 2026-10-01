# S-26: the two effect layers executed — mutate, rebuild and merge as shipped code (OPUS, 2026-09-25, block 341)

**Evidence class: NATIVE-REPLAY (unicorn), `live_game: false`.** S-26's runtime cell is MIXED on EXP-086 alone. EXP-086
executed the status write with fourteen `ret`-stubbed deep callees and a scripted `0031B860`. Its contract,
[`CONTRACT-effect-layers.md`](../../../10-Status-Periodic-Terminal/CONTRACT-effect-layers.md), says in §13 that *"No
experiment executes these three bodies."* This harness executes all three and tests L-1..L-6 and §12's reproduction
formula:
- `BattleStats_ModifyStatusLayerStateAndProcessSideEffects` (`0030E130`);
- `BattleStats_RecomputeDerivedStateAndAutoStatuses` (`0030FED0`);
- `BattleFormula_BuildEvaluationContext` (`003847C0`).

## What was run

`check.py`, with `world.py` / `world.json` / `printf_bridge.py` / `shipped_pack.py` from block 334. The `battle_pack`
tables (party rows, equipment, licences) are bound by shipped code. `0031B860`, the validator `00322C50`, the set/clear
handlers, `0030EA40` and the party arm of `002FEF30` all run real. **No application stub.**

There is **one stop boundary**, in the foe case only: the run ends at `002FEF30`'s entry. That body's foe arm reads the
loaded area's unit-definition slot `[02EBF150]`, an ARD resource this world does not load. The arguments `(rec, 0)` are
recorded, and the reconcile being tested precedes the boundary.

**Fixtures:**
- four idle objects;
- the unit pool with owning units (`+0x698` → stats record, `+0x55` a marker byte);
- stats records (`+4` character, `+5` party/foe, `+0x50` five equipment words `0xFFFF`, `+0x194` licence bits);
- an action byte for the merge's second argument.

**9 / 9 pass, and `result.json` is byte-identical over three runs** (md5 `bbe5ac78f25aa16ab5a2921c408e8774`).

| case | contract item | observed |
|---|---|---|
| `L3_merge_is_the_or_of_both_layers` | L-3 | Caster `+0x68` = A, `+0x78` = B over all 128 ids (40 only-mutable, 37 only-derived, 26 both). The context's `+0x1A` equals A \| B exactly |
| `L4_alias_bit_16` | L-4 | Bit 16 in either layer (Disease or Weatherproof) gives the **same** merged context |
| `L5_id15_revocation` | L-5 | See the L-5 table below |
| `L5_owner_global_written_by_the_merge` | §3, §5, §10 | See the L-5 table below |
| `L2_mutate_takes_the_layer_as_a_parameter` | L-2 | See the mutate list below |
| `mutate_side_effects_key_on_the_merged_presence` | L-2, §10 | See "What the execution adds", item 3 |
| `L1_rebuild_never_writes_the_mutable_layer` | L-1 | See the rebuild list below |
| `L6_rebuild_reconciles` | L-6, §12 | See the rebuild list below |
| `foe_derived_layer_is_the_unit_E80_bitmap` | L-6, §8 | A foe record (`+5` = 1): the derived layer equals the owning unit's `+0xE80` bitmap. There are 59 ids and 59 mode-3 mutates; the mutable layer is untouched |

**L-5: the id-15 revocation and the owner global.** Id 15 is set in the caster's mutable layer, with id 3 as a control:

| case | id 15 | context `+8` | `+0x18` | `02EBF188` |
|---|---|---|---|---|
| target owned, action bit 5 clear | kept | `00811000` | `0021` (the unit's `+0x55`) | the unit |
| target not owned | revoked | `00810000` | `FFFF` | `0` |
| target null | revoked | `0` | `0000` | unchanged |
| action bit 5 set | revoked | `0` | `0021` | the unit |

**The mutate, `0030E130(rec, id 40, 0, flags 0x202, mode)`:**
- mode 2 sets and mode 0 clears the mutable layer;
- mode 3 sets and mode 1 clears the derived layer;
- a repeat in the reached state writes nothing and runs no side effect.

**The rebuild:**
- **L-1.** With all `0x169` licence bits set and mutable `{2, 16}`, the rebuild fills the derived layer with 87 ids from the
  shipped tables. **Every write to `+0x68..+0x87` lands in `+0x78`, at `0030E212`, inside the mutate.** The mutable layer
  is unchanged.
- **L-6.** A second rebuild with unchanged inputs makes **0** writes and **0** mutate calls.
- **L-6.** Then a stale id 0 is planted and desired id 5 is dropped. The third rebuild makes **exactly 2** mutate calls:
  mode 1 clears the stale id and mode 3 re-adds id 5.

## What the execution adds

1. **The merge writes `02EBF188`. The contract says it does not.**
   - §5 lists *"the global at `02EBF188`"* under *"Read, never written here"*.
   - Measured: the merge **stores** `0031B860(target)` there at `00384870` whenever the target is non-null. The global is
     overwritten with the unit, or 0 when there is none.
   - §3's *"a value from the global record at 02EBF188 (+0x55), or 0xFFFF when it is null"* is the lookup result itself,
     and the global's prior value plays no part. With a **null target**, `+0x18` is `0x0000` (the prologue's clear), not
     `0xFFFF`.
2. **L-5 is conditioned on the target, and the merged bits come from the caster.**
   - The loop reads the **third** argument's layers (`r8` → `r11`).
   - The owner test and `+8` read the **fourth** (`r9` → `rdi`).
   - So *"a record with no owning battle unit loses id 15"* (§10) means the **target** record. A caster that holds id 15
     loses it in the context whenever the target has no owner, or is null.
3. **The mutate's side effects key on either-layer presence.** Setting id 40 in the derived layer while the mutable layer
   already holds it writes the layer but enters **no** handler. The same set with neither layer holding it enters the set
   handler `00386AE0`. The mechanism: `0030E27B` compares either-layer presence before and after. So the side effects
   are a function of the merged state, not of the written layer. §10 defers side effects to the operation contract;
   this is the cross-layer half that no single operation contract can state.
4. **The rebuild's derived writes go through the mutate.**
   - The rebuild never stores `+0x78` itself. It builds a desired bitmap, computes add = `(D^C)&D` and
     clear = `(D^C)&C` (`00310310`–`00310336`), and calls `0030E130` in mode 3 or mode 1 per id, with `flags | 0x202`.
     Bit 9 stops the mutate's own call back into the rebuild; bit 1 skips its second handler pair.
   - **L-1's "three `+0x78` sites"** counts two (`0031043F`, `00310484`) that address `[unit + 0x6A0] + 0x78..0x7C`, a
     different object. That object is copied to and from `rec + 0x40..0x44`.
   - L-1 still holds for this fixture, but its evidence is the mutate's mode argument, not a site count.

All four are routed to FABLE (contract author).

## Not covered

- the foe arm of `002FEF30` and the rebuild's foe tail (`0030E360` per `+0xE90` bit, the `+0x6A0` copy), which need a
  loaded area;
- the mutate's second handler pair (flags bit 1 clear) and the `003279B0` arm (ids `0x68`–`0x71`);
- equipment-sourced derived ids (every equipment word was `0xFFFF`);
- a live game.
