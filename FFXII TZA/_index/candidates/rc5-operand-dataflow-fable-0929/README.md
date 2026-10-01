# RC-5 residue: the variable event-id operands, computed by script dataflow (FABLE, Claude Opus 5.5, 2026-09-29)

Register row RC-5 belongs to SWE2-CONTRACT; ORACLE's record is `../rc5-event-slot-routes-0930/`. The row's residue lists
"the values of the non-constant operands", and says "script dataflow can bound those further, so nothing is routed to
ASTRA yet". FABLE ran that dataflow (`FABLE-RC5-OPERAND-DATAFLOW-0929`, target keys only) and routes the result for
incorporation.

## Method

- **Sites.** Every row of ORACLE's `rc5_verbs.tsv` whose event-id operand is `dyn:PUSHV` ('us' scripts): 381
  `startscene`, 5 `startscene_4b3` and 19 `eventread_e8`, 405 in all.
- **Store census:** [`rc5_dataflow.py`](rc5_dataflow.py) -> [`rc5_dataflow.tsv`](rc5_dataflow.tsv) /
  [`.out`](rc5_dataflow.out). For each site it finds the `PUSHV` and the variable's descriptor. It then collects every
  `POPV` into the same variable, what each store pushes, and any `PUSHP` reference.
  - Every `startscene` / `startscene_4b3` operand is a **file-class** variable.
  - Its stores are `var = constant` and `var = var + c` (`OPADD`).
  - No variable has a reference passed.
- **Value propagation:** [`rc5_constprop.py`](rc5_constprop.py) -> [`rc5_constprop.tsv`](rc5_constprop.tsv) /
  [`.out`](rc5_constprop.out). It propagates constant-value sets over each script's control-flow graph: the function
  entries and the jump table from the script directory, per the section-000 page, section 4.
  - **No value-stack model.** The shared decoder does not model the REQ family's stack effects, and an earlier version
    that guessed them hit depth mismatches in 25 of 38 files. Instead, only file variables are tracked. Each store and
    each operand is read by a backward parser that accepts only pure expressions (constants, `PUSHV`, `+ - *`), which is
    exact wherever it applies.
  - **Function entry.** Every function starts with each file variable = {0} plus every value any function of the file
    stores into it, iterated to a fixpoint.
  - **Non-convergence.** A variable that has not converged after 12 rounds, such as a counter that keeps growing across
    entries, goes to TOP. An earlier version reported the truncated sets instead; that was wrong, and it was caught
    before this record.
  - **Jumps.** Opcode meanings come from the interpreter page's opcode table:
    - `0x51` JMP and `0x60` JMPINTERNAL are unconditional;
    - the compare-jumps `0x52`–`0x57` and `0x5A` POPXJMP / `0x5B` POPXCJMP / `0x5C` POPXNCJMP take the jump and also
      fall through. This over-approximates `0x5A`, which is sound;
    - an earlier version missed the `0x5A`–`0x5C` edges and left 3 sites unreached.

## Controls (all PASS)

- **All sites found.** Each of the 405 sites is found at its (file, pc), as a call of the same id with a `PUSHV`
  operand (`rc5_dataflow.out`).
- **All sites reached.** Every variable site is reached with a non-empty state, and no file has an unresolvable jump or
  function entry.
- **Positive control.** All 20 **constant** `startscene` sites in the same files evaluate to exactly their
  `rc5_verbs.tsv` value.

## Result

| verb | sites | exact single value | unbounded here |
|---|---:|---:|---:|
| `startscene` | 381 | **341** (58 distinct scene ids, 0-57) | 40, in 8 files |
| `startscene_4b3` | 5 | **5** (ids 2-16) | 0 |
| `eventread_e8` (set id) | 19 | **13** (set id 0: never-stored, un-aliased file arrays; see below) | 6 |

- ~~**The 341 + 5 exact sites are constants in effect.**~~ *(narrowed 2026-09-30, FABLE, on SWE2-AUDIT-SEM's [review](../auditsem-review-rc5-dataflow-0930/REVIEW.md) §4, N1:)* 249 sites are exact: their counter is assigned in one function only. 97 more (in dgl_g0100, gil_c0201, grm_c0101, hne_b0100, hne_b0101, mrm_c0100, mrm_c0101, rui_c0100) are exact along their own function's path, provided no other function of the file steps the same counter between steps. That is the same request-order fact as the 40 unbounded sites. *Was:* each is a scene counter set by a constant and stepped by
  constants on every path that reaches the call: `var = 7; ...; var = var + 1; startscene(var)` (`dgl_g0100`). Their
  per-site values are in `rc5_constprop.tsv`.
- **The 40 unbounded `startscene` sites** are in `dgl_g0100`, `enw_a0580`, `gil_a0200`, `mnt_c0100`, `rwf_d0100`,
  `rwf_d0101`, `rwg_a0181` and `str_z0000`. Their counter is also stepped in functions entered by request. In
  `dgl_g0100`, the function at script offset `+0x408` does `var = var + 1; startscene(var)`. **The fact left, stated
  as the user's rule requires:** how many times those request-entered functions run before each site. That is the
  order in which other actors request them, which the scripts author but no constant fixes. It is decidable per event
  by modelling the event's request order, which is further static work. It is not yet a live-only fact.
- **The 19 `eventread_e8` sites** read their set id from array-class variables (15) or file variables with computed
  stores (4). [`rc5_e8_arrays.py`](rc5_e8_arrays.py) reads the array headers. All the arrays are in the `image/ff12/in`
  controllers `ctrl.ebp` and `evctrl.ebp`, and their element descriptors are **file-class**, 4-byte, int:
  - **13 sites, 4 arrays:** `ctrl.ebp` header `9E0` (elements at file offset `0`), and `evctrl.ebp` headers `1B40`
    (`0x64`), `1B90` (`0x288`) and `1C40` (`0x510`, 10 of the sites). **No `POPV` in the file writes these arrays**, so
    the values read are the file storage's initial contents.
  - **2 sites:** `evctrl.ebp` header `1C50` has computed stores.
  - **4 sites:** file scalars whose stores are other variables or a verb result (`aask`, a menu answer).

  **Resolved for the 13 never-stored sites** ([`rc5_e8_arrays.out`](rc5_e8_arrays.out), FAILS 0):
  - **Layout.** The header's dimensions are signed dwords from `+8`, per the storage-class page (`002624B3`-`002624C6`).
    An earlier read took `u16` at `+6` and gave 0.
  - **Values.** Each index is clamped into `[0, dim-1]`, so the value read is always one of the elements. The elements
    are the file home's initial bytes, at `section + [section + 0x38]`.
    - `ctrl.ebp` `9E0`: 10 elements;
    - `evctrl.ebp` `1B40`: 10 elements;
    - `evctrl.ebp` `1B90`: 4 elements;
    - `evctrl.ebp` `1C40`: 24 elements.

    **Every element is 0.**
  - **Alias check.** No `POPV` or `PUSHP` in either file names storage overlapping any of these element ranges, under
    any descriptor, scalar or array.
  - **Control.** The same alias scan finds the stores into the stored array `1C50` (4 sites for each of its 2 reads,
    PASS).

  **So these 13 `eventread_e8` sites pass set id 0**, which `rc5_paths.tsv` lists no kind-8 name for. The same model
  assumption applies as above: ~~native code does not write file-class storage.~~ *(narrowed 2026-09-30, FABLE, on SWE2-AUDIT-SEM's [review](../auditsem-review-rc5-dataflow-0930/REVIEW.md) §4, N2:)* Native code writes file-class storage once, at manager initialisation, through `0026D3E0` (class 1 → `[manager+0x40]`, `memcpy` at `0026D4D5`) from authored initial-value entries. The model takes initial values from the file home's bytes, so the 13 set-id-0 sites are 0 only if no such entry targets their arrays (not checked). The other 6 sites (array `1C50`'s 2, and
  4 file scalars stored from another variable or from the `aask` menu answer) stay unbounded here.

## The `debug_eventload` operands: all constant

This is the row's residue item "the operands of the battle-family verb `0x202D` `debug_eventload` (`0050D0C0`)".
[`rc5_debug_eventload.py`](rc5_debug_eventload.py) -> [`.tsv`](rc5_debug_eventload.tsv) / [`.out`](rc5_debug_eventload.out)
reads every CALL-family site of call id `0x202D` in all 10,036 shipped `.ebp` files and resolves its two operands (arity
2 in the verb table).
- **Control:** the same walk reproduces ORACLE's 3,789 `startscene` sites exactly.
- **Result: 274 sites, every operand a constant.** They sit only in the `image/ff12/ch` and `image/ff12/in` controllers,
  with identical counts in each copy: `mapctrl.ebp` 82 + 82, `btlctrl.ebp` 49 + 49, `ctrl.ebp` 3 + 3, `evctrl.ebp`
  3 + 3.
- **What the handler does** (`0050D0C0`, read to its returns): the first operand is the manager and the second the set
  id.
  - A manager of 4 goes to `00314410(id)` (`0050D0DC`-`0050D0E5`).
  - Any other manager is checked through `00263FF0()`'s flags, then `0026A5F0(m)` runs, then
    `0032FC30(m, id)` (`0050D0EC`-`0050D115`).
- **Values:**

| manager operand | sites | set ids |
|---|---:|---|
| 1 | 248 | 1, 4, 9, 16, 19, 20, 22, 23, 80, 81, 82, 83, 84, 85, 86, 505 |
| 4 | 26 | 2, 3, 4, 5 |

So this residue item is closed: the operands are authored constants. Whether a shipped session reaches these debug
controllers is not part of this item.

## The `+0x24` word `00306BD0` hands to `00309230`: enumerated from the action tables

This is the row's residue item 2. ORACLE called it "battle data, not enumerated here... the one non-debug route by which
a `sum_<x>0001` name, and so flag A, could be set".

**The route**, per ASTRA's `ov42-special-action-preconditions` packet ("Original path"), re-read here at `00309230`:
- `0030CE10` tests the action row's flags `+0x0C` bit 30 (`0030CE93`) and reaches `00306BD0` only when it is set
  (`0030CF0D`).
- `00306BD0` calls `00309230` (`00306C4D`), which returns the row's unsigned `word +0x24` (`003092C5`).
- `00306BD0` then hands that value to `0032FC30` as the set id (`00306C56`).
- One exception: the row whose pointer equals the computed special entry indexes the 13-entry actor-type table instead
  (`003092CB`).

[`rc5_action_word24.py`](rc5_action_word24.py) -> [`.out`](rc5_action_word24.out) reads the nine retained action
tables.
- **Control (PASS in all nine packs):** ASTRA's invariants reproduce: 543 rows, stride 60, 68 `FFFF` words, and rows
  511-534 hold `FFFF` with flags `0x40000211`.
- **All nine languages give the same bit-30 multiset:** 87 rows per pack.

| `+0x24` of a bit-30 row | rows ('us') | set id's name (ORACLE's `rc5_paths.tsv`) |
|---|---|---|
| 41, 44, 47, ..., 77 (13 values) | 183, 185, ..., 207 (one row each) | the 13 `sum_<x>0001`, which **set flag A** |
| 40, 43, 46, ..., 76 (13 values) | 262-274 | the 13 `sum_<x>0000` (cutscene JSON only) |
| 210 | 34 rows (208-219, ...) | `spc_z0000`, which **sets flag B** |
| 355 | 149 | `chb_z0000` |
| 0 | 148 | no kind-8 name |
| `FFFF` | 275 (`0x113`, the special-identity row) and 511-534 | none; ASTRA's OV-42 packet covers these |

**So the non-debug route to flag A exists in authored data.** Each of the 13 flag-A set ids is the `+0x24` of exactly
one bit-30 action row. Which of those actions a battle performs is play, but the set of ids this route can load is
the table above. This residue item is closed as an enumeration. Row 275 takes the actor-type branch, so it yields
42, 45, ..., 78 (the `sum_<x>0002` names).

## Limits

- **'us' scripts only**, matching ORACLE's TSV. ORACLE's 3,429 / 45 figures count every language copy; the other
  copies were not re-run.
- **Native writes.** ~~The model assumes native code does not write file-class variables, which are the script image's
  own data. It rests on the storage-class page's section 3.~~ *(narrowed 2026-09-30, FABLE, on SWE2-AUDIT-SEM's [review](../auditsem-review-rc5-dataflow-0930/REVIEW.md) §4, N2:)* Native code writes file-class storage once, at manager initialisation, through `0026D3E0` (class 1 → `[manager+0x40]`, `memcpy` at `0026D4D5`) from authored initial-value entries. The model takes initial values from the file home's bytes, so the 13 set-id-0 sites are 0 only if no such entry targets their arrays (not checked).
- **The shared decoder mislabels opcodes.** `gen_req_channel_census.py`'s `OPN` names `0x52`–`0x57` `JMPPOPX`..
  `JMPYC` and `0x5A`–`0x5C` `UNK5A`..`UNK5C`, against the interpreter page's `POPCMPY*JMP` / `POPXJMP` family. Its
  `resolve_args` stops at these ops, so its outputs stay conservative. The labels are routed to the file's owner.

## For SWE2-CONTRACT (RC-5 owner)

RC-5's operand residue narrows:
- ~~346 of 386 scene-id operands are exact constants (`rc5_constprop.tsv`);~~ *(narrowed 2026-09-30, FABLE, on SWE2-AUDIT-SEM's [review](../auditsem-review-rc5-dataflow-0930/REVIEW.md) §4, N1:)* 249 exact, 97 exact under no interleaving, 40 unbounded (`rc5_constprop.tsv`);
- 40 depend on request order in 8 named event scripts;
- 13 of 19 `eventread_e8` set ids are 0 (never-stored, un-aliased file arrays); 6 stay unbounded;
- `debug_eventload`'s operands are all constant, and the `+0x24` action word is enumerated (both residue items close).

None is live-only.

## Residue item 4: the live region arm and the size entries

- **The region arm is the boot language.** `ResourcePath_Init` indexes the twelve-name table `JP US FR DE IT ES UK KR CH
  ASIA IN CN` with the language id it receives (`002E03F5`-`002E0410`; file-size-tables-fst.md). ORACLE showed that
  every arm yields the same (set id, name) pairs and only the locale directory differs, so the arm changes no answer
  above.
- **The three sets whose paths the archive lacks have no size entry** ([`rc5_fst_missing.py`](rc5_fst_missing.py) ->
  [`.out`](rc5_fst_missing.out), FAILS 0):
  - 355 `chb_z0000` (kind-8 rows 1420-1423), 398 `msg_z0000` (1592-1595) and 440 `men_z0004` (1760-1763) are **-1 in all
    twelve** `FileSizeTable_<lang>.fst`;
  - the kind-8 FST id is ORACLE's `row` column (set × 4), not the set id. A first version indexed by set id failed its
    own control;
  - control: sets 30 and 31 (in the archive) have four positive entries each in the US table.
- **One of them is named by authored battle data, and the loader skips it.** Set **355** is the `+0x24` of bit-30 action
  row **149** (table above), so a shipped battle action can hand `0032FC30` a set whose size entry is -1.
  - The event loader builds no request for it. In `0032FCA0` / `00330310`, each request is skipped when the size for
    its (kind, row) is negative: `test ebx, ebx` / `js` at `0032FE5E`; `jl` at `0032FED2`, `0032FF38`, `0032FFA3` and
    `00330378` (FABLE's OV-33 static pass, `../ov33-no-status-exits-fable-0929/`).
  - So the set's resources are silently not loaded; the read issuer's -1 refusal is never reached from this route.
  - The first two skips were re-read here.
