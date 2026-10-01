# GR-9 answered: nothing outside an enemy's own order set enters its subgroups, so the 155 sets' unreached subgroups are authored and never entered (OPUS, 2026-09-30)

Register row GR-9 asks what enters the subgroups that 155 enemy order sets populate but never switch into from inside
the set. The count comes from UQ-121's census of 166 `.ard` directories, 1,422 sets and 50,050 records. Two routes
were already excluded: another variant set, and a script literal. What the row left open was a subgroup command
(`0x4116`–`0x4121`, stored by `002FE0BB`) whose id is computed at run time. The page is
[gambit-evaluation-and-enmity.md](../../../09-Combat-AI-And-Gambits/gambit-evaluation-and-enmity.md) §7, the UQ-121
box.

Method: static, the certified image. The checker is `gr9_subgroup_check.py` (output `gr9_subgroup_check.out`,
**`FAILS 0`**). It uses the kit's `retool.py` and `regval.py`.

## The answer (OPUS)

**No run-time id can reach an enemy's subgroup.** A unit's subgroup changes in only three ways:

- a subgroup order its **own current set** commits (authored);
- a variant switch, which sets it to 0;
- a reset, which also sets it to 0.

**What sets a non-zero subgroup (K1, K2).** The subgroup byte `+0x6B5` has exactly three byte writers in the image:

| writer | value |
|---|---|
| `002FE0BB`, the subgroup arm of the direct-state order dispatcher `002FDDA0` | `dl` = the low byte of the unit's committed order id `+0x714` (`002FDDB0`) minus `0x16`. So order `0x4116 + k` enters subgroup `k`. |
| `002FE09F`, the variant switch | 0 |
| `BattleUnit_ResetStateForReuse` (`00236BA3`) | 0 |

Every other access whose width covers `+0x6B5` is a wider access at `+0x6B0` / `+0x6B4` on another base. The one in
battle-adjacent code, `002E03C4`, is a store into a global function-pointer table.

**Where the committed order id comes from (K3, K4).** Only `BattleUnit_CommitAction` (`0030F806`) writes an id to
`+0x714`. `BattleUnit_CancelAndResetCurrentAction` (`0031071B`) and the reset (`00236B55`) store `0xFFFF`; FE-7 R3 did
not list those two writers, but neither changes its conclusion. CommitAction has five call sites (FE-7 R3):

| call site | where the id comes from |
|---|---|
| `00305DF4` | the evaluated record of the unit's **own** order set (authored) |
| `00305C9B` | the static `0x4021` record `01EEC298` |
| `0030FA5C` | `+0x714` again (a combo) |
| `003130DC` | the constant `0x96` |
| `00305B2F` | the issued-command word `+0xBA0` |

**Where the issued-command word comes from (K5).** `+0xBA0` is written only by `BattleUnit_IssueCommand` (`00311CF0`
at `00311D7A`), from its `r9w`. Its callers pass one of:

- `0x9C`, `0x9D` or `0x113`;
- a battle-menu word from `BattleMenu_UpdateCommandSelectionAndDispatch` `002778C0` (`0027868A`, `0027875A`) or
  `0027C3D0` (`0027C591`). These arrive through the focus-handle issuers `00311B20` and `00311CD0` (called from
  `002778C0`, `0027AA70` and `0027C3D0`);
- `0x113`, from `003138D0`.

So the only run-time order id is the player's battle-menu command for the focus units. With UQ-121's census, which
covers switches reachable from subgroup 0, the sibling-set union and script literals, the unreached subgroups of the
155 sets are **authored and never entered**.

**In player terms:** some enemies carry AI behaviours in their data that they can never switch to. Nothing in the
game, script or engine, ever moves them into those behaviour groups.

## Limits

- **Which units the menu issues for.** That the battle menu's focus handles are always the player's controllable units
  (never an enemy) is the menu's contract. It is not re-proven here.
- **What the menu lists.** The menu word's own value set (the listed command ids) is not enumerated.
- **Indirect callers.** An indirect caller of `BattleUnit_IssueCommand` or `BattleUnit_CommitAction` would not appear in
  the direct call census. The K4 and K5 sets are direct callers only.

## Consumers (routed, not edited here)

- The gambit page's §7 UQ-121 box (FABLE's page), and register row **GR-9**, via a DATA restatement request.
- FE-7's record (`fe7_order_reach.py` R3) lists the id-bearing writer only; the two `0xFFFF` writers can be added as a
  note. Routed to its author, FABLE.
