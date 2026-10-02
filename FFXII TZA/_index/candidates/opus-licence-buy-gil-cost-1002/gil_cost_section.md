**What `00309060` is.** `BattleAction_ComputeGilCost(unit, actionId)`, 168 B (`00309060`–`00309107`), read whole from the shipping bytes, with its callees and both callers read. It returns the action's **gil cost** as an `int`. Zero means "costs no gil". The function writes nothing: there is no store in its body, and neither of its callees stores either. Static read only; nothing was executed.

**Arguments.**

- `rcx` is the battle unit (`rbx`, `0030906D`). Its `+0x698` is the stats record (`00309075`).
- `dx` is the action id, zero-extended (`0030906A`).

**Callers.**

| caller | site | what it does with the cost |
|---|---|---|
| `BattleAction_CheckExecutionResourceAvailability` `00303BD0` (← `002FFCF0` at `002FFEB0`) | `00303C7B` | **the check**: reason `0x15` (see below) |
| `BattleAction_PrepareExecutionResources` `0030EF20` (← `00304850` at `00304962`, `00307300` at `003073AB`) | `0030EFBB` | **the debit**: reserve at unit `+0xE58`, then gil −= cost |

**The rule.**

```
stats = unit ? unit[+0x698] : NULL;
if (stats && stats.b[+5] == 1)              return 0;   // kind-1 record: 00309070-00309085 -> 003090FB
if (actionId > 0x21E)                       return 0;   // 00309087-0030908F (543 rows, ids 0..0x21E)
row = res(02EBF138.+0xC) + actionId * 02EBF138.w[+8];   // 00309091-003090CA (NULL -> 0 at 003090CE)
if ((u8)(row.b[+0x1E] - 5) <= 1)            return 0;   // row kinds 5 and 6: 003090D0-003090D8
if (!BattleUnit_UsesGilActionCostChannel(unit)) return 0;  // 002F9820: 003090DA-003090E4
return BattleAction_ComputeModifiedResourceCostAmount(unit, actionId);   // tail jump 002F95D0 at 003090F6
```

**Callee `BattleUnit_UsesGilActionCostChannel` `002F9820` (51 B).**

- It returns 0 if `stats.b[+5] == 1` (`002F9825`–`002F9837`).
- Otherwise it returns 1 if `stats.b[+0x6C]` bit 0 **or** `stats.b[+0x7C]` bit 0 is set (`002F983A`–`002F984D`). That bit is effect id 32 in the mutable status layer `+0x68` or the derived augment layer `+0x78`.
- It has no null guard. For a null `unit` the `je` at `002F9823` falls through to `mov rax, [rcx + 0x698]` at `002F983A`, which faults. A null `stats` faults at `002F9841`. `00309060` itself does not filter a null unit (`00309070`–`00309073` only skip the kind test). Both callers prevent this: `00303BD0` refuses a null unit (`00303BE0`) and only calls when `stats` is non-null and kind 0 (`00303C68`–`00303C73`), and `0030EF20` does the same (`0030EF60`–`0030EF77`).

**Callee `BattleAction_ComputeModifiedResourceCostAmount` `002F95D0` (589 B), on the path `00309060` lets through.**

```
base = row.b[+0x0A];                                    // 002F95E4-002F962B: the authored MP byte
if (stats.kind != 1 && (id in 0xD0..0xE1 || id in 0x106..0x112))  return base;   // 002F962F-002F9667, 002F9806
if (stats.b[+0x6C] & 1 || stats.b[+0x7C] & 1)          // 002F9674-002F9682: tested FIRST
    return 10 * (int)trunc( f32(f32(base) * 64.0f) / 50.0f );   // 002F97E4-002F9802
// (Channeling 91-93, effect 51 zero, effect 36 halve: 002F9688-002F97DE - never reached on the gil path)
```

- The constants were read from the image: `00916318` = `64.0f` (`00 00 80 42`) and `008F3130` = `50.0f` (`00 00 48 42`).
- `cvttss2si` (`002F97FB`) truncates. `lea eax, [rax + rax*4]` / `add eax, eax` multiplies by 10 (`002F97FF`–`002F9802`).
- There is **no cap and no level term**. The cost is a pure function of `row.b[+0x0A]`.
- Because effect 32 is tested first, the gil cost is **not** reduced by Channeling, halved, or zeroed by the other MP effects.
- For every shipped base (1–72), the result equals `10 × floor(32 × base / 25)`. Base 31 gives 390 gil.
- **Shipped table** (`battle_pack.bin` `action_data`, 543 × 60): 115 rows reach the formula with a non-zero `+0x0A`, costing 10 gil (base 1) up to 920 gil (base 72, row 14). Rows whose `+0x0A` is 0 cost nothing, and the availability check skips them (`00303C84`).

**The exemption arm cannot be reached through either wrapper on shipped data.**

- Row byte `+0x1E` is 6 on exactly ids `0xD0`–`0xE1` (18 rows) and 5 on exactly `0x106`–`0x112` (13 rows).
- So `00309060`'s kind-5/6 test (`003090D4`–`003090D8`) and the MP twin's test (`0030916D`–`00309171`) return 0 before `002F95D0` ever sees those ids.
- The id ranges in `002F9646`–`002F9667` only matter for the third caller of `002F95D0`, the menu builder `0031EB20` (`0031F06D`). It calls the formula directly to show the cost word (`0031F072`), and uses `002F9820` to pick the gil marker `8` or the MP marker `2` (`0031F00C`–`0031F029`).

**Where gil is checked: `00303BD0`.**

```
if (stats && stats.b[+5] == 0) {                    // 00303C68-00303C73
    cost = BattleAction_ComputeGilCost(unit, id);   // 00303C75-00303C80
    if (cost && GameState_GetGil() < cost           // 00303C82-00303C8D; GetGil 00253690 = [02092758]+8
             && unit.d[+0xE58] < cost)              // 00303C8F-00303C95 (both compares signed, jge)
        return 0x15;                                 // 00303C97
}
```

This check runs after the reasons `0x12` (`003037A0`), `0x13` (MP: `stats.w[+0x4C]` < `00309110`) and `0x14` (`stats.b[+0x4E]` < `00308FF0`) (`00303BF5`–`00303C53`).

**Where gil is debited: `0030EF20`.**

```
id = (row - res(02EBF138.+0xC)) / 02EBF138.w[+8];   // 0030EF2F-0030EF5E (before any guard)
if (unit && stats && stats.b[+5] == 0) {            // 0030EF60-0030EF77
    ... reserve/consume the item (+0xDC8) ...       // 0030EF79-0030EFB0
    cost = BattleAction_ComputeGilCost(unit, id);   // 0030EFB5-0030EFBB
    unit.d[+0xE58] = cost;                          // 0030EFC0: the reservation, stored even when 0
    if (cost) GameState_SetGil( (GetGil() - cost) >= 0 ? GetGil() - cost : 0 );   // 0030EFC8-0030EFD8 (cmovns)
}
```

`GameState_SetGil` `00254EE0` then clamps to `[0, 99,999,999]` (gil-storage page). The refund `00300280` adds `+0xE58` back to gil and the consume path `00305640` clears it. Neither is re-read here; see `using-an-item-is-an-action-that-costs-an-item.md` §4.

**So `+0xE58` is a reservation, not a second purse.** The check's second compare lets an action through when its own cost is already reserved. That covers an action that was prepared, and so already paid, then re-checked while gil sits below the cost.
