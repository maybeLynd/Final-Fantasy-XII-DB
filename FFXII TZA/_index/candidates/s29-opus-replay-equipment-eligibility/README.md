# S-29: equipment compatibility executed as shipped code — EQ-1..EQ-8 and the recommender (OPUS, 2026-09-25, block 323)

**Evidence class: NATIVE-REPLAY (unicorn), `live_game: false`.** S-29's exposure note (block 301) found the equipment
contract's EQ-1..EQ-8 **unexecuted**. Its §13 says so too: "None. No experiment executes these bodies". The inventory
half of the row is executed cross-row by S-30's EXP-092. This harness runs the equipment half.

## What was run

`check.py`, with `world.py` / `world.json` / `printf_bridge.py` from block 322. `Session.call` gains stack arguments
(the chain's fifth argument sits at `[rsp+0x28]`).

**Every body runs as shipped.** There is no application stub and no stop boundary:
- `002F7EC0`, `00317930`, `00317B20`, `00323C60` and `002F9F20`;
- their callees:
  - the validator `00322C50`;
  - `00309440` and the owned-count query `00309EC0` → `002FD8D0`;
  - the board lookup `00323BB0`, which `00323C60` tail-jumps to, with `002F8FA0`, `00323890` and `003241D0`;
  - the stats lookup `00320AB0` → `0031B9F0`;
  - the weapon comparator `002F7A10` / `002F7C80`.

**Imports.** `memset` is the only import reached, bridged by name.

**The authored tables are planted fixtures.** The engine loads them from its data files; in the image their cells are
null.

| cell | fixture |
|---|---|
| `[02EBF0F8]` | the equipment-definition header `{+4 count 0x1A4, +8 stride, +0xC offset}`. The codec base `[01F83530]` is 0 in the built world, so the offset is the table's address. Records: `+7` slot / exemption, `+9` class, `+0x11` partner class. Every record not named by a case is slot 7 (never a slot) and class 31 |
| `[02EBF130]` | the class table: the forbidden mask per stats index. Bit 31 is set by default |
| `[02EBF038]` | the licence records `{+5 kind 1, +8 ids[8]}`. Kind 1 maps to licence class 0 through `003241D0` → `00323890`, which is the class `00323BB0` asks for |
| the `[02EBF190]` block | the stats records (`+8 + i*0x1C8`) and the mode-3 character → stats-index bytes at `+0x5A7E` |
| `[01EEBD20]` | the family-1 `+0x08` pointer to the packed owned words |

**9 / 9 pass, and `result.json` is byte-identical over three runs** (md5 `444fc5d98378a3c056dad3f3f52ae079`).

| case | contract item | observed |
|---|---|---|
| `EQ1_partner_test_asymmetric` | EQ-1, §12 | `002F7EC0(off, main)` = 1 when `main[+0x11] == off[+0x09]`. **Swapping the arguments gives 0.** Either side `0xFFFF` gives 1 |
| `EQ2_shield_exempt_only_inline` | EQ-2 | Main hand requires class 23. The chain admits a shield (class `0x12`) in slot 1 and the standalone refuses it. The two agree on class 23 (admit) and 24 (refuse). An empty main hand passes both |
| `EQ3_packed_slot_and_exemption` | EQ-3 | `+7` bits 7..5 = 2 is eligible in slot 2 only. With no licence bits the gate returns 0 **through the board lookup**. With bit 4 set it returns 1 and **never enters `00323BB0`** |
| `EQ5_forbidden_mask` | EQ-5, §12 | The item's own class bit **set rejects**. Every other bit set still admits. With the mask clear, a missing licence bit still rejects |
| `EQ6_selector_and_index_bypass` | EQ-6, §12 | `stats[+5] = 2` admits past a mask that forbids everything **and** an empty licence board. The gate alone returns 1 for it, and for `stats[+4]` = 7 and `0x27`. **6 still needs the board** |
| `EQ7_two_classes_one_range` | EQ-7 | The validator is entered as `(6, id)` from the chain, then `(1, id)` from the gate. **Each reaches the same class-6 arm `00322D02`.** An id at the header count fails both, and that is the gate's one 0 exit |
| `wrapper_owned_test_always_on` | §16a | `00317B20` always passes 1 as the chain's fifth argument, and refuses a stats index above `0x27`. The count tested is the inventory contract's kind 0, `(word & 0x3FF) − (word >> 10)`, and it must be ≥ 1: total 1 / reserved 1 is refused, total 3 / reserved 2 admitted. The chain with the flag 0 admits all four |
| `EQ8_EQ4_recommender_order` | EQ-8, EQ-4 | The full call order is asserted; see below. `out = [1020, 1190, FFFF, FFFF, 1234]` |
| `EQ8b_empty_main_forced_then_offhand_dropped` | EQ-8 | With no slot-0 candidate admitted, the epilogue writes `0x1000`. Then `002F7EC0(0x10D5, 0x1000)` fails and the carried shield becomes `0xFFFF` |

### The recommender's order (EQ-8 / EQ-4)

The stats record carries `[FFFF, 10D5 shield, FFFF, FFFF, 1234]`. The candidates are `0x1020` (slot 0, requires
class 23), the shield `0x10D5`, and `0x10D6` / `0x1190` (slot 1, class 23). The run, in order:

1. **Slot 0** walks `0x1000..0x10C7` (200 ids). `0x1000` is admitted by the short-circuit, then `0x1020` beats it in
   the comparator.
2. **Inside that comparison**, `002F7C80` scores `0x1020`. Its `+0x11` is in 23..26, so it walks ids
   **`0x1184..0x11A3` through the slot-1 wrapper** and compares the matching `0x1190` in mode 0 (`002F7D97`–`002F7E24`).
3. **The slot-0 epilogue** tests the **carried** off-hand `0x10D5` against `0x1020`: `002F7EC0` at `002FA069`.
4. **Slot 1** walks `0x10C8..0x11A3`, 220 ids: EQ-4's `hi[1] = 0x11A4`, containing slots 2 and 3. **Every candidate
   the chain admits is re-tested by `002F7EC0` at `002FA013` against `out[0]`**. The shield is admitted by the chain
   and refused there, before any comparison. `0x10D6` is taken (mode 1), then `0x1190` beats it in **mode 0**
   (`002FA021`–`002FA033`).
5. **Slots 2 and 3** walk `0x10DC..0x1117` and `0x1118..0x1153`.
6. **`out[4] = 0x1234` is passed through untouched.**

## What the execution adds

1. **EQ-1 through EQ-8 are executed.** All eight hold, and so do §12's reproduction steps.
2. **EQ-2's stated consequence is out of order.** It says *"the recommender's inner loop admits any shield for slot 1
   whatever the main hand is, and the slot-0 epilogue then … drops it"*. Measured:
   - the slot-1 loop re-tests each admitted candidate itself (`002FA013`), and the shield is refused there;
   - the slot-0 epilogue runs **before** slot 1's walk and acts on the off-hand **carried in from the stats record**.

   The two guards are real. The first is the chain's (it exempts shields) and the second is the standalone (it does
   not), **applied per candidate in the same loop**, not one cleaning up after the other. Routed to FABLE.
3. **§14's first question has an execution answer.** It asks what the ids `0x1184..0x11A3` are, which the recommender
   compares under mode 0:
   - They are the range that **`002F7C80` searches for the partner of a weapon whose `+0x11` is 23..26**, the classes
     §3 labels ammunition.
   - The weapon's score is taken with its best matching item from that range, through the same mode-0 comparator.
   - The recommender's mode-0 compare for those ids in slot 1 matches that.

   The ammunition label is §3's, not measured. Routed to FABLE.
4. **§14's fourth question** asks whether EQ-7's class-6 and class-1 validations can disagree for a real id.
   - **For an id with high nibble 1, they cannot.** The class-1 arm looks up the id's family code (`00309440`,
     `01EEBCF8`: family 1's code is 6) and re-dispatches to class 6's range test, `[0x1000, 0x1000 + header+4)`. This
     is measured, and read at `00322C7E`–`00322C8B`.
   - An id reaching the gate through the chain has already passed class 6.
   - Ids of other nibbles reaching the gate from other callers would go to their family's own arm; that is not
     measured here.
5. **The wrapper's owned test is the available count** (total − reserved), measured.

## Not covered

- the recommender's callers and the application of `out`;
- the comparator's scoring beyond these cases (`002F7A10`'s other fields);
- the licence board's real data;
- the S-29 inventory half: EXP-092 (cross-row) and `diff_inventory_query.py`, not re-run;
- a live game.
