# RC-5 residue: the action rows that set flag A, the debug loads, and the operand domains (SWE2-ORACLE, 2026-09-30; array-pop-order fix 2026-10-02)

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
- it resolves every operand of the target verbs with the database's bytecode decoder and a local stack resolver,
  `resolve_args7`, that models the engine's array pop order: a class-7 `PUSHV`/`POPV` pops one index **per
  dimension** before the element/value (F1 fix, verified at `00262440`/`00267E60`; the dimension count is
  `w[header+4]`, per-dimension bounds `d[header+8+4k]`, and each index is clamped to `[0, dim-1]` at
  `0026250C`-`0026251B`);
- for each script-variable operand, it decodes the variable descriptor and gathers every `POPV` into that variable
  (array stores are keyed by header offset and record value and index producers side by side);
- it recognises the increment idiom `x = x + k`.

Its controls:
- C1: RC-5's `startscene` count of 34,125 is reproduced;
- C2: every descriptor decodes to a legal class and width;
- C3: class-7 `POPV` producer resolution — the header census reports {1: 3,005,859, 2: 35,424} (two-dimensional
  arrays exist in the wider population; every controller array is single-indexed). 9 stores are unresolved — all
  the same site, `mfr_a04.ebp+55B5` in the nine locale copies: its directory block begins with a `RET`-headed stub
  (`RET; CALL; PUSHII 0; POPV`), and the resolver does not cross the block boundary to the real producers.

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
- **`eventread_e8`: 40 non-constant operand instances** (20 unique sites in the `ch`/`in` copies of `ctrl.ebp` and
  `evctrl.ebp`). Corrected 2026-10-02 under F1 (`FABLE-REQ-ORACLE-RC5-ARRAY-POPV-ORDER-1002`,
  `rc5-counter-loops-fable-1002` at `52fb48cd`): the engine pops an array `POPV`'s **index before its value** —
  `00267E60` calls `00262440` (`00267E7F`), which decrements the same stack count at `002624D2`-`002624E1`, before
  the helper pops the value at `00267E9C`-`00267EA7`. Earlier runs took the stack top as the value, so array index
  producers were recorded as stored values and operands below an array `PUSHV` were misattributed.
  - **The 4 "counter" operands are element reads of `evctrl`'s `class7+0x1c50` (`file_var_s1_12[2]`), not counters.**
    `[0, 3]` was the domain of the store *index* `class1+0x904` (`file_var_s1_4`), not of the operand. The array's 4
    stores write `0` to elements 0 and 1, and `class1+0x8dc` (`file_var_s1_2`) at index `+0x904`; `+0x8dc` has no
    `POPV` store in the file (declared 0). The operand's domain is **{0} exactly**.
  - **13 element reads of never-stored arrays return declared initialiser elements** (the engine clamps each popped
    index into `[0, dim-1]` — `0026250C`-`0026251B`, `cmovns`/`cmovl` against the dimension count dword at
    header `+8`):
    - `class7+0x1c40` = `file_var_s7_1[24]` — 10 reads indexed by `file_var_s1_4 - 1` → {0, 715-719, 737, 738};
    - `class7+0x1b40` = `file_var_s1_5[10]` — 1 read indexed by `s1_4 - 1` → {17, 18, 96, 15, 90, 87, 10, 95, 7, 92};
    - `class7+0x1b90` = `file_var_s1_7[4]` — 1 read indexed by `s1_4 - 1` → {121, 121, 211, 214};
    - `ctrl.ebp`'s `class7+0x9e0` — 1 read; that file's own declared elements.
    - The offset↔name map is proven by the descriptor headers: element counts at `+8` read 24, 10, 4 and 2 for
      `+0x1c40`, `+0x1b40`, `+0x1b90` and `+0x1c50`, matching `s7_1`, `s1_5`, `s1_7`, `s1_12`.
  - **3 scalar reads of `class1+0x8dc` (`file_var_s1_2`)** return its declared value 0 — it has no `POPV` store in
    the file (the previous run's "takes one of the `s5_*`/`s9_2` elements" was the same misattribution).
  - **1 read of `class1+0x8ec` (`file_var_s1_9`)** is the open `aask` value below; **1 `OPSUB`** in `ctrl.ebp`.
  - **The one open value:** `evctrl.ebp`'s `event_menu` passes `file_var_s1_9 = aask(0, 0x01000012, …)` when it lies
    in 1 to 9999. Message `0x12` is not a choice list in this file's text section, so the value is whatever the
    player enters at that debug prompt, within 1 to 9999.

## The remaining per-session fact

- **Named:** the number entered at `evctrl.ebp`'s `event_menu` prompt (message `0x12`), within 1 to 9999.
- **Otherwise the value at a site depends only on:**
  - which menu choice is taken (within the enumerated domains above);
  - which path an event script takes to a given `startscene` (within its counter interval).

## Not claimed

- **Loop analysis for the counter intervals.** The bound assumes each increment runs once per pass through its code.
  A loop around an increment would widen it; no loop check was run. (FABLE's `rc5c_loops.py` ran it for the counter
  populations; its corrections stand alongside this record.)
- **Element aliasing.** Class-7 element stores are keyed by header offset; a store whose flattened element address
  overlaps a scalar (`+0x8dc`/`+0x904`) is not tracked through the scalar's key (FABLE's caveat, retained).
- **Per-element precision.** An array's domain is the flat union over its element stores, not a per-element map;
  for `+0x1c50` the clamp makes that union {0} regardless.
- **Multi-index audit detail.** For `ndim>1` stores (35,424 sites in the population — none in the controllers) the
  record keeps the value producer and the top index producer only.
- **Retail reachability** of the `evctrl`/`ctrl` debug controllers (RC-5's own caveat).
- **Text meaning.** The menu option counts come from the choice header byte and the option separators, not from
  decoded text.
