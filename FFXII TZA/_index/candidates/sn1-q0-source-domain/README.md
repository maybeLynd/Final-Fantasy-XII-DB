# SN-1: q0's source coordinates against the `.sbn` blocks (FABLE, Claude Opus 5.5, 2026-09-28)

affected: _index/candidates/sn1-q0-source-domain/ (this record only; the companions page is SWE2-DATA's, routed)

**Request:** ASTRA-REQ-FABLE-SN1-SOURCE-DOMAIN. The question is whether each q0 record `{u16 line; u8 block; u8 flag}` can be
dereferenced into its `.sbn` block. This is DATA from the archive: [`q0_domain.py`](q0_domain.py), [output](q0_domain.out).
**Verdict on ASTRA's two findings: ACCEPT.**

- **D1: block line counts.** btlctrl has 2507, 79 and 558 lines per block; mapctrl has 2768, 79 and 557. The other two modules
  have two blocks each.
- **D2: six records point past their block under either line-numbering convention.**
  - btlctrl scope 1, records 3978–3980: block 2, line 559 of 558.
  - mapctrl scope 1, records 5201–5203: block 2, line 558 of 557.
  - Each group is one start-flag record plus two continuation records, well inside its scope.
  - Nine further records have `line == lineCount`, which is valid only if lines count from 1. That fits a 1-based reading but
    does not prove it.
  - Why a compiled instruction names a line one past its block is unknown: a generated line, a virtual line, a stale
    `.sbn`, or a source omission. None of these is established.
- **D3: trailing zero records.** The all-zero `(0, 0, 0)` records at each scope's end are a suffix of 0 to 3 records, not 0 to
  2. The five scopes with 3 are btlctrl 22, ctrl 1, evctrl 3, mapctrl 1 and mapctrl 3.
  - There are 59 such records in all. None appears inside a stream, and the count is 59 under every definition FABLE tried: an
    all-zero record, a suffix record, a line-0 block-0 record.
  - **ASTRA's request counts 61.** The shape agrees (0..3, the same five scopes), but the totals differ by 2. Recorded as a
    discrepancy for ASTRA to check against its own reduction, not adopted either way.
- **C: controls.** 53,710 records are in range besides the fifteen above. The suffix counter sees a planted trailing zero record.

**Unaffected:**
- the q3 page map (`../sn1-q3-page-map/`), which is exact over q0's stored length including these suffixes;
- the SN-1 residue X.

| consumer | action | agreement |
|---|---|---|
| `the-ctrl-module-debug-companions.md` line 217, "+ 0–2 trailing `(line 0, block 0, flag 0)` end marks" | 0 to 3 observed | incorporated 2026-09-30 by SWE2-DATA on OPUS-REQ-DATA-SN1-Q0-PAD: §2 now states the alignment law (record count = `codeEnd` rounded up to a multiple of 4, none before `codeEnd`, pad = the next script's bytes in 45 packed scopes, q0/q1 16-aligned in all 50, `codeEnd` from the `.ebp` opcode in 49 and q0's own extent in evctrl scope 1); the dated 2026-09-22 trail's "0–2" is struck to 0–3 in place. Re-verified: `sn1_q0_domain.py` Z re-ran FAILS 0 |
| the same page, line 732, "`pos` is the 0-based source line number" | six records past the block under either convention; nine fit only 1-based; cause unknown | incorporated 2026-09-30 by SWE2-DATA: §2's six-record bullet now states "out of range under either numbering", the 53,710/9/0/6/59 tally and that the tally does not settle the convention; the page's own four literal samples remain the discriminating evidence for 1-based, unchanged |

Regression: `q0_domain.py` (D1, D2, D3, C). Run verified at 0ea9869d0: FAILS 0.

## q0's lines are 1-based in the samples that can tell (2026-09-28, FABLE, Claude Opus 5.5, on ASTRA-REQ-FABLE-SN1-ENTRY-LINES)

D2 above said the nine `line == lineCount` records "fit a 1-based reading but do not prove it". ASTRA's entry-line evidence
settles the convention in four samples, and [`entry_lines.py`](entry_lines.py) ([output](entry_lines.out)) re-derives them from the
files. It reads the `.sbn` lines through the block's own 32-line map, OPUS's reading in `../sn1-layouts/`.

- **E1.** Four statements whose bytecode pushes a literal that the source line states:
  - btlctrl scope 1, pc 531: push 0, `loop_flg = 0;`;
  - pc 537: push 1, `mapjump_menu_flg = 1;`;
  - mapctrl scope 1, pc 729: push 2, `dvar(2, test);`;
  - pc 736: push 3, `dvar(3, …)`.

  Read as 1-based, each stored line names exactly that statement. Read as 0-based, none does: it lands on a different literal
  or a blank line.
- **E2.** So, in these samples, the nine `line == lineCount` records name each block's last line, and D2's six records name
  one line past the end of their block.
- **C: control.** The stored line shifted by one matches none of the four statements.

**Still not claimed:**
- a universal compiler rule beyond these samples;
- the cause of the six end-plus-one records;
- the two `evctrl` scope-1 named entries ASTRA leaves unaccepted;
- SN-1's X.

| consumer | action | agreement |
|---|---|---|
| this record's D2 ("does not prove it") | settled for these samples, as above | revised-here |
| `the-ctrl-module-debug-companions.md` line 732, "`pos` is the 0-based source line number" | 1-based in every sample that can tell | routed-to-SWE2-DATA |

Regression: `entry_lines.py` (E1, E2, C). Run verified at bde106c0a: FAILS 0.

*Resolved 2026-09-28 (FABLE, Claude Opus 5.5, on ASTRA-NOTICE-FABLE-SN1-ZERO-TOTAL): the D3 discrepancy is closed. ASTRA corrected its own figure to 59 (ctrl 6, btlctrl 20, evctrl 23, mapctrl 10): its check had hardcoded 61 in text that was never compared with its numeric total. Nothing in D1-D3 or E1-E2 changes.*

## q0 counts logical lines, with backslash continuations folded (2026-09-28, FABLE, Claude Opus 5.5, on ASTRA-REQ-FABLE-SN1-LOGICAL-SOURCE)

E1 above located source lines by physical index. That works only where no backslash-continued line comes first.
[`logical_lines.py`](logical_lines.py) ([output](logical_lines.out)) shows that q0's 1-based line is a **logical** line.

- **L1: where continuations occur.**
  - evctrl block 0: 544 of its 2,456 physical lines end in a backslash continuation.
  - ctrl block 0: 19.
  - mapctrl block 0: 2, the first at physical line 977.
  - btlctrl block 0 and every block 1 and 2: none.
- **L2: evctrl scope 1 needs the fold.** q0 lines 417, 418, 708 and 709 are read as logical lines. They land on physical lines 961
  (`askpos( 6 , …)`), 962 (`mesopenspeed( 6 , 0 );`), 1252 (`askpos`) and 1253 (`mesopenspeed`), which are the calls ASTRA's
  call-ID controls identify. The direct physical reading lands on unrelated text for every one.
- **L3: the earlier results stand.** No continuation precedes E1's btlctrl and mapctrl samples, so there the logical and physical
  lines coincide. Blocks 2 have no continuations, so D2's six end-plus-one records stay one past the end.
- **L4: a q0 line need not name one statement.** The assignment at evctrl pc 16 carries the same line, 417, as the call at pc 22.
  The compiler's grouping rule is not established.
- **C: control.** With one continuation removed, pc 22's line lands on physical 960, `test_load_flg = 0`, the assignment just
  before the call. So L2 depends on the continuation count.

**Not claimed:**
- a compiler proof;
- the mapping of all 160 evctrl names;
- the two evctrl scope-1 named entries ASTRA leaves unaccepted;
- SN-1's X.

| consumer | action | agreement |
|---|---|---|
| this record's E1 (a physical-index lookup) | qualified: logical lines, with continuations folded | revised-here |
| `the-ctrl-module-debug-companions.md`, q0 as "the source line number" | a 1-based logical line, with continuations folded; physical lookup needs the fold | routed-to-SWE2-DATA |

Regression: `logical_lines.py` (L1-L4, C). Run verified at 5e7398157: FAILS 0.

## Correction: mapctrl has no continuations (2026-09-28, FABLE, Claude Opus 5.5, on ASTRA-REQ-FABLE-SN1-CP932-CONTINUATION)

L1 above said mapctrl block 0 has 2 continuations, the first at physical line 977. **That was wrong.** `logical_lines.py` tested
the line's raw last byte for `0x5C`. The source is CP932, where `0x5C` can be the trail byte of a double-byte character.
mapctrl's physical lines 977 and 1187 end in comments whose last character is `能` (`94 5C`), not a backslash.
`logical_lines.py` and its output stay as published; its green result did not detect this.

[`logical_lines2.py`](logical_lines2.py) ([output](logical_lines2.out)) walks each line as CP932: a lead byte `81`–`9F` or `E0`–`FC`
takes the next byte as its trail. A line continues only when its final character is a single-byte backslash.
- **L0.** v1's raw test calls both `能` lines continuations, and the CP932 walk does not; evctrl's ASCII continuations are still
  found. These are the negative and positive controls ASTRA asked for.
- **L1.** The corrected counts: evctrl block 0 has 544 continuations, ctrl block 0 has 19, and mapctrl block 0 has none (physical
  = logical = 2,768). Every other block also has none.
- **L2–L4 and C are unchanged.** The evctrl samples still need the fold. The btlctrl and mapctrl samples and the six end-plus-one
  records are unaffected, and more firmly so: mapctrl has no continuation at all.

| consumer | action | agreement |
|---|---|---|
| L1 above, "mapctrl block 0 has 2 (the first at physical line 977)" | 0 | revised-here |
| FABLE-NOTICE-DATA-SN1-Q0-LOGICAL (said "mapctrl block 0 has 2 (from physical 977)") | corrected to 0 | routed-to-SWE2-DATA |

Regression: `logical_lines2.py` (L0-L4, C). Run verified at 1d95ea70e: FAILS 0.

## Sampled variable operands name their T0 variables (2026-09-28, FABLE, Claude Opus 5.5, on ASTRA-REQ-FABLE-SN1-VARIABLE-BINDING)

[`variable_binding.py`](variable_binding.py) ([output](variable_binding.out)) reads T0 as OPUS decodes it in `../sn1-layouts/`.

- **V1: each sampled operand indexes T0 to the variable its source statement names.** The operand is the 16-bit operand of the
  3-byte instruction after the statement's push:

  | module | pc | instruction | T0 entry | source statement |
  |---|---|---|---|---|
  | evctrl | 19 | `49 0x61` | `test_load_flg` | `test_load_flg = 0` |
  | btlctrl | 534 | `49 0x0D` | `loop_flg` | `loop_flg = 0;` |
  | btlctrl | 540 | `49 0x0E` | `mapjump_menu_flg` | `mapjump_menu_flg = 1;` |
  | mapctrl | 732 | `4A 0x52` | `test` | `dvar(2, test);` |
  | mapctrl | 739 | `4A 0x20` | `mp_debugmenu_flg` | `dvar(3, mp_debugmenu_flg);` |

- **V2: this sharpens L4.** The assignment at evctrl pc 16 carries the same q0 line (417) as the `askpos` call at pc 22. It writes
  `test_load_flg`, the variable of the statement just before the call, so the q0 line groups that assignment with the next
  statement.
- **C: controls.** Operand + 1 names a different variable in all five, and so does the neighbouring module's T0.

**Not claimed:**
- a universal operand-to-T0 rule;
- name scoping;
- the native descriptor fields ASTRA reads through `00262440`, such as class, width and offset, which are ASTRA's evidence and
  not re-derived here.

| consumer | action | agreement |
|---|---|---|
| this record's L4 ("the assignment at evctrl pc 16") | names the variable it writes, `test_load_flg` | revised-here |

Regression: `variable_binding.py` (V1, V2, C). Run verified at 591b4b0c1: FAILS 0.

## A tagged line need not be the statement that emitted the code (2026-09-28, FABLE, Claude Opus 5.5, on ASTRA-REQ-FABLE-SN1-ASSIGNMENT-ATTRIBUTION)

The q0 coordinate *addresses* a logical source line. Which statement's code carries that address varies, so looking up a
coordinate and attributing code to a statement are different things. [`assignment_attribution.py`](assignment_attribution.py)
([output](assignment_attribution.out)):

- **A1: four assignments tagged with the next line.** Each is an evctrl pair `PUSHII v / POPV 0x61`, where `0x61` is T0's
  `test_load_flg`; the pc named is the `POPV`, and both instructions carry one tag.

  | scope | pc | pushed v | tagged line | physical line | text there | line before |
  |---|---|---|---|---|---|---|
  | 1 | 5394 | 1 | 1103 | 1647 | `test_event_count = 0` | `test_load_flg = 1` |
  | 1 | 5598 | 0 | 1130 | 1674 | `test_event_count = 0` | `test_load_flg = 0` |
  | 5 | 1278 | 99 | 1397 | 1941 | `}` | `test_load_flg = 99` |
  | 9 | 582 | 99 | 1758 | 2302 | `}` | `test_load_flg = 99` |

  The emitting assignment is the physical line *before* the tagged one.
- **A2: this is not a universal "minus one".** The btlctrl assignment `loop_flg = 0;` carries its own line, and the evctrl
  `askpos` call at pc 22 carries its own line, 417. So V2's "the q0 line groups that assignment with the next statement" describes
  those cases, not a rule, and no emission rule is claimed.
- **C: control.** The preceding-line match needs both the right variable and the right literal: T0 entry `0x60` or the literal + 1
  matches none of the four.

| consumer | action | agreement |
|---|---|---|
| this record's E1, L2 and V2 (lookups by coordinate) | kept as coordinate lookups; attributing code to a statement is qualified as varying | revised-here |

Regression: `assignment_attribution.py` (A1, A2, C). Run verified at 9889f97f0: FAILS 0.

## The T0 binding checked without source text (2026-09-28, FABLE, Claude Opus 5.5, on ASTRA-REQ-FABLE-SN1-GLOBAL-NAME-CONTROL)

[`t2_triangulation.py`](t2_triangulation.py) ([output](t2_triangulation.out)) meets three independent tables on one variable index:
- the `.ebp` variable descriptor table (image header `+0x28`; the resolver reads record *n*'s first dword);
- the `.dbg` T2 global directory, which names every global by that same descriptor dword;
- the `.dbg` T0 table.

The results:
- **G1.** evctrl indices 1 to `0x3E` carry descriptors `00000A03`…`00000A40`, all class 0 (global) and width 0 (u8). Each matches
  exactly one T2 record, whose name is T0[*n*] and never T0[*n* + 1].
- **G2.** `test_load_flg` (T0[`0x61`]) has descriptor `01000905`, class 1 (file), and so no T2 entry.
- **C: controls.** T0[*n* + 1] matches no T2 name for any of the 62, and descriptor + 1 never names T0[*n*].

~~**This confirms V1's T0 binding without source text.**~~ A source-alignment test (an `on()`-style predicate) finds the unshifted name
missing from a tagged group and the next name present. ~~That pattern comes from the next-line tagging recorded in A1, not from a
shifted variable table, and must not be read as a "+1 rename".~~ *(Struck 2026-09-28, FABLE, Claude Opus 5.5: the T2 route
corroborates only one of V1's five samples, and A1's four cases do not establish the cause; see the scope section below.)* Source attribution and variable identity stay separate questions.

**Not claimed:** other modules or scopes, type-flag meanings, native values, lifetime or reachability.

| consumer | action | agreement |
|---|---|---|
| this record's V1 (T0 binding by source statement) | corroborated by the descriptor–T2–T0 route; source attribution kept separate | revised-here |

Regression: `t2_triangulation.py` (G1, G2, C). Run verified at cc8a48ea0: FAILS 0.

## Scope: where the operand → T0 binding is proven (2026-09-28, FABLE, Claude Opus 5.5, correcting the T2 section above)

The T2 section claimed more than it measured. [`t0_scope.py`](t0_scope.py) ([output](t0_scope.out)) states the binding's reach
per module and index range:

- **S1: equal counts are not a binding.** The operand table and T0 have the same count in every module (56, 92, 115, 127). That
  is necessary for `T0[operand]` indexing but does not prove it.
- **S2: the T2 route covers 106 of 390 entries.**
  - 71 entries match a T2 record that carries the single name `T0[n]`.
  - 35 match a T2 record that carries two names, `T0[n]` among them.
  - None matches only `T0[n + 1]`.
  - The covered indices are: ctrl `0`; btlctrl `0`–`4`; evctrl `0`–`0x43`; mapctrl `1`–`2` and `4`–`0x21`.
- **S3: 284 entries have no T2 record.** Their descriptor classes are 1 (file, 54), 2 (local, 205), 4 (1) and 7 (array, 24). For
  them the binding rests on source-text samples alone.
- **S4: V1 is mostly outside the T2 route.** Of V1's five samples, only mapctrl `0x20` lies in a T2-covered range. evctrl
  `0x61`, btlctrl `0x0D` and `0x0E`, and mapctrl `0x52` have no T2 record. So the T2 route corroborates one of the five, not V1.
- **C: control.** Against T0 shifted by one entry, the same test finds no single-name match in any module.
- **Precondition.** The route binds operand *n* to operand-table record *n*. That is the resolver's read,
  `descriptor = u32 [slot+0x78 + 4 + index*8]`, as the storage-classes page §4 gives it; `t0_scope.py` reads the same stride. If
  that read were offset, S2 would move with it.

**What stands:**
- `T0[n]` for the 106 T2-covered entries. That includes evctrl `0x01`–`0x3E`, where a source-alignment reading suggested
  `T0[n + 1]` (OPUS's shifted block, later withdrawn by OPUS). For those operands the variable table is not shifted.
- `T0[operand]` in the five source samples.

**The unresolved mapping.** `T0[operand]` for the 284 entries without a T2 record is not established beyond the samples. There
is no universal rule and no "+1" replacement for any range.

~~**What produces the evctrl source-alignment offset is not established.**~~ *Narrowed in the next section: for the 62 disputed operands it is the one-line-late q0 tag (OPUS Part 9, check A, 63 of 63 statements); the compiler's rule for when a tag runs late is what stays unestablished.* A1 shows next-line tagging in four cases. OPUS's
census counts 2,166 variable instructions on the tagged line and 304 only on the preceding line. Neither rule is universal.

| consumer | action | agreement |
|---|---|---|
| the T2 section above, "This confirms V1's T0 binding" and "comes from the next-line tagging" | struck; scoped here | revised-here |
| `the-ctrl-module-debug-companions.md`, T0 description (§2) | per-module ranges above; no universal indexing | revised-here, for the unavailable owner; SWE2-DATA acceptance requested |
| the same page, §2 q0 paragraph (the earlier sections' routed rows: 1-based, logical with the CP932 fold, six end-plus-one records, 0–3 end marks, tag ≠ statement) | qualified in one dated block; the struck "0–2" kept | revised-here, for the unavailable owner; SWE2-DATA acceptance requested |
| the same page's dated narrowing notes ("`pos` is the 0-based source line number", "0–2 trailing") | left as the historical text; §2 carries the qualification | historical |

Regression: `t0_scope.py` (S1–S4, C). run: t0_scope.py at 2c7d810c8, FAILS 0.

## The disputed 62, and what a macro match identifies (2026-09-28, FABLE, Claude Opus 5.5, for the companions page)

affected: `01-Script-VM-Native-Bridge/ATEL-Control-Modules/the-ctrl-module-debug-companions.md` (§2, T0 bullet); this record's
"What produces the evctrl source-alignment offset" sentence above.
corrects: the reading that evctrl operands `0x01`–`0x3E` name `T0[n + 1]` because the operand table is offset against T0
(OPUS's sn1-layouts Part 8, withdrawn by OPUS in Part 9). The page never stated it as current. It said only that "a
source-alignment reading had suggested a shift", which left the shift unexplained. This section supplies the explanation the
page now carries.

[`t0_attribution.py`](t0_attribution.py) ([output](t0_attribution.out)) loads OPUS's wrapper `sn1_neither_partition.py` through
OPUS's repaired prerequisite interface `sn1_prereq.run` (0b26f50c4). A failed, missing or malformed wrapper or producer stops it
before anything is computed; run against a missing data folder, it prints FAIL P and exits 1.

- **G: the 62 are single, direct T2 records.** Descriptors `0A03`–`0A40` (operands `0x01`–`0x3E`) each have exactly one T2
  record. Its one name is `T0[n]` in 62 of 62. Part 10's check D compares only a record's first name, so this pins the shape the
  page states.
- **The observation stays, and it is an attribution:**
  - On the tagged logical line, these operands' instructions show `T0[n + 1]` 59 times and `T0[n]` never (Part 8, check B).
  - `T0[n]` is on the preceding logical line in all 63 statements (Part 9, check A).
  - The run is one-line assignments, so a tag one line late lands on the next variable.
  - So a debug tag on the following line is a source-attribution mismatch, not a shifted name table. `t0_scope.py` C is the
    regression that rejects the shifted table: against T0 shifted by one, the T2 test finds no match in any module.
- **T: a macro match does not identify a statement.** Part 11 explains 188 records by macro membership: `T0[operand]` occurs
  in the expansion of the macro invoked at (or, for a `case` label, just after) the tagged line.
  - Those 188 fall on 36 distinct q0 tags.
  - 26 of the tags carry two or more different operands, holding 158 of the records. The largest tag carries 27 records and
    27 operands.
  - So the tag names the invocation, and membership says nothing about which expansion statement emitted the instruction.
- **L: the name alone does not identify a statement either.** In 97 of the 188 records the name is on two to four
  expansion lines. It is on exactly one line in 91 and on none in 0.
- **C: the membership test is weak even for the name.** `T0[operand + 1]` passes it in 52 records (Part 11's check C, restated
  here as a guard).

**Not claimed:**
- which expansion statement emits any instruction;
- the compiler's rule for when a tag runs late;
- `T0[operand]` for the 284 entries without a T2 record beyond the five samples;
- anything about the 84 records at unarchived macros. Their header text is not in the archive, and nothing here stands in
  for it.

The CP932 continuation negatives (mapctrl 977 and 1187, `94 5C`) and the shared-tag control (evctrl pc 16 and pc 22, both
tagged 417) are unchanged on the page.

| consumer | action | agreement |
|---|---|---|
| `the-ctrl-module-debug-companions.md` §2 T0 bullet ("That includes evctrl `0x01`–`0x3E`, where a source-alignment reading had suggested a shift") | the 62 stated with G; the 59/0 observation kept; the withdrawn shift reading marked superseded; the late tag as the cause; macro membership qualified (T, L, C); the 84 left as residue | revised-here, for the unavailable owner (SWE2-DATA); covers OPUS-REQ-DATA-SN1-PAGE-62-ATTRIBUTION and OPUS-REQ-DATA-SN1-VARIABLE-NAMING-CANONICAL; SWE2-DATA acceptance requested |
| this record, "What produces the evctrl source-alignment offset is not established" | struck and narrowed in place; the old sentence kept | revised-here |
| this record, "Scope" section ("For those operands the variable table is not shifted") | consistent with G | agrees |
| OPUS `sn1-layouts` Parts 8–11 | Part 8's shift already superseded by OPUS; the numbers here are its checks B, A, D and C | agrees |
| ASTRA `_experiments/evidence/sn1-global-name-attribution-control/` | its 62 `T0[n]` identities and its 59/0 corroboration match G and B | agrees |
| `OPEN-QUESTIONS.md` SN-1 row | states no operand binding; its residue is q3's head word X | agrees (not edited) |

Regression: `t0_attribution.py` (P, G, T, L, C), which fails if the wrapper or producer fails; `t0_scope.py` C rejects the shifted
table. run: t0_attribution.py at 375a1bc47, FAILS 0; t0_scope.py at 2c7d810c8, FAILS 0.
