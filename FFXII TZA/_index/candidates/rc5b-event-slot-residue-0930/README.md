# RC-5 residue: the action rows that set flag A, the debug loads, and the operand domains (ORACLE, 2026-09-30)

## The question

`../rc5-event-slot-routes-0930/` left RC-5 NARROWED with four residue items:
1. the domains of the non-constant operands of `startscene`, `startscene_4b3`, `eventread_e8` and `summoneventread`;
2. the authored `+0x24` word of every record `00306BD0` hands to `00309230`, and which `sum_<x>0001` names it reaches;
3. the operands of the battle-family verb `0x202D` `debug_eventload`;
4. whether the region arm changes the answer.

## Method

Four scripts. Their paths are relative to this folder. All report FAILS 0.

| script | output | covers |
|---|---|---|
| [`rc5b_actions.py`](rc5b_actions.py) | [`rc5b_actions.out`](rc5b_actions.out) | item 2: the gate and the `+0x24` read, checked against the image (K1, K2); the 543-row action table in all nine `battle_pack.bin` copies (K3); the names, from RC-5's kind-8 path table |
| [`rc5b_operands.py`](rc5b_operands.py) | [`rc5b_operands.out`](rc5b_operands.out), [`rc5b_operands.tsv`](rc5b_operands.tsv) | items 1 and 3; details below |
| [`rc5b_evctrl.py`](rc5b_evctrl.py) | [`rc5b_evctrl.out`](rc5b_evctrl.out) | the controller `evctrl.ebp`, decompiled with ff12-script (section 000): its variable-operand lines, the arrays they index, and the option counts of the menus they read |

`rc5b_operands.py` runs over every shipped `.ebp`:
- it resolves every operand of the target verbs with the database's bytecode decoder and stack resolver;
- for each script-variable operand, it decodes the variable descriptor and gathers every `POPV` into that variable;
- it recognises the increment idiom `x = x + k`.

Its controls:
- C1: RC-5's `startscene` count of 34,125 is reproduced;
- C2: every descriptor decodes to a legal class and width.

## Result

**RC-5: NARROWED to one named per-session fact. Items 2, 3 and 4 are answered, and item 1 is bounded.**

**Item 2: flag A is reached through the summon actions.**
- `BattleAction_TryEnterGlobalSpecialSequence` (`0030CE10`) calls `00306BD0` only for an action row whose `+0x0C` has
  bit 30 (`0030CE93`).
- `00306BD0` loads manager 3 with the row's `+0x24`. Row `0x113` instead indexes the Esper table.
- 87 rows carry the bit, identical in all nine locales:

| rows | `+0x24` set ids | names | effect |
|---|---|---|---|
| 183, 185, …, 207 (13) | 41, 44, …, 77 | `sum_a0001` … `sum_m0001` | **set flag A** `01F832E8` (K4: exactly the 13 `sum_<x>0001` ids) |
| 262 … 274 (13) | 40, 43, …, 76 | `sum_<x>0000` | none |
| 275 | the Esper table, 42 … 78 | `sum_<x>0002` | none |
| 208 … 241 (34) | 210 | `spc_z0000` | **set flag B** `01F832E9`; these rows are skipped while `[022C2160]` is 5 or 6 |
| 149 | 355 | `chb_z0000` | the path is not in the archive |
| 148 | 0 | no kind-8 path | none |
| 511 … 534 (24) | `0xFFFF` | no kind-8 path | none |

So the non-debug route to flag A that RC-5 left open is real: the 13 Esper summon actions.

**Item 3: every `debug_eventload` operand is constant** (274 sites, in `btlctrl`, `ctrl`, `evctrl` and `mapctrl`).
- Manager 1 is loaded with set ids 1, 4, 9, 16, 19, 20, 22, 23, 80-86 and 505.
- Manager 4 is loaded with 2, 3, 4 and 5; `0050D0DC` diverts manager 4 to `00314410`.

The per-tuple counts are in `rc5b_operands.out`.

**Item 4: the arm choice does not change the answer.** RC-5 measured the `(set id, name)` pairs identical in all 13
region arms; only the locale directory differs. The action table is identical in all nine `battle_pack.bin` copies
(K3).

**Item 1: the variable operands are bounded.**
- **`startscene`: 3,429 variable operands.**
  - 3,141 read a file variable that is only ever set to constants or advanced by `x = x + k`. It is the scene counter,
    reset and then incremented before each `startscene`. Its values lie in [smallest constant, largest constant + the
    file's total increments], which is at most 0 to 102 overall and never wider than 95 for one variable.
  - The other 288 are counters with no constant store in scope. Each starts from its declared value and advances by up
    to 13.
  - The exact value at a site is fixed by the straight-line order of resets and increments on the path the event
    takes.
- **`startscene_4b3`: 45 variable operands**, all of the same counter kind, within 1 to 67.
- **`summoneventread`: 4 sites, all in `evctrl.ebp`.** The set id is `choice + 39` on menu message 7, or
  `choice + 57` on message 8:
  - message 7 has 20 options: 0 is refused, 19 turns the page, and choices 1-18 give **40-57**;
  - message 8 has 13 options: 0 is refused, 12 turns back, and choices 1-11 give **58-68**;
  - so the domain is **40-68**. Page 2's offset is one short, so its first entry is unselectable and ids 69-78 cannot
    be chosen;
  - among 40-68, flag A is set by 41, 44, …, 68 (10 of the 13).
- **`eventread_e8`: 66 variable operands, all in the controllers `ctrl.ebp` and `evctrl.ebp`.**
  - Array reads clamp their index, so they return initialiser elements:
    - `file_var_s1_5` = {17, 18, 96, 15, 90, 87, 10, 95, 7, 92};
    - `file_var_s1_7` = {121, 121, 211, 214};
    - `file_var_s7_1` = {0, 715-719, 737, 738};
    - `file_var_s1_2` takes one of the `file_var_s5_1..10` / `s9_2` elements listed in `rc5b_evctrl.out`.
  - `file_var_s1_12` is always 0.
  - 4 sites are counters within 0-3.
  - **The one open value:** `evctrl.ebp`'s `event_menu` passes `file_var_s1_9 = aask(0, 0x01000012, …)` when it lies in
    1 to 9999. Message `0x12` is not a choice list in this file's text section, so the value is whatever the player
    enters at that debug prompt, within 1 to 9999.

## The remaining per-session fact

- **Named:** the number entered at `evctrl.ebp`'s `event_menu` prompt (message `0x12`), within 1 to 9999.
- **Otherwise the value at a site depends only on:**
  - which menu choice is taken (within the enumerated domains above);
  - which path an event script takes to a given `startscene` (within its counter interval).

## Not claimed

- **Loop analysis for the counter intervals.** The bound assumes each increment runs once per pass through its code.
  A loop around an increment would widen it; no loop check was run.
- **Retail reachability** of the `evctrl`/`ctrl` debug controllers (RC-5's own caveat).
- **Text meaning.** The menu option counts come from the choice header byte and the option separators, not from
  decoded text.
