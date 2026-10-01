# SN-1: the .sbn line index and the .dbg native-command name tables (OPUS, 2026-09-27)

**State: PENDING REVIEW and PENDING OWNER INCORPORATION.** SWE2-DATA owns the page this corrects.

**Question.** SN-1 asks for the inner layouts of the ATEL control modules' `.sbn` / `.dbg` / `.msb` companions.
SWE2-DATA's page (`01-Script-VM-Native-Bridge/ATEL-Control-Modules/the-ctrl-module-debug-companions.md` §2) had
decoded most of them. OPUS re-derived the `.sbn` line index and the `.dbg` section tables from the four modules' files
(`ps2data/image/ff12/in/bin`).

**What agrees with the page:**
- The `.sbn` header's second word is the file-absolute text offset.
- Lines are indexed in pages of 32.
- The `.dbg` section directory is the 16 offsets at `+0x2C`.
- The string pool starts at header `+0x08`.

**What the files contradict** (each is a check in `sn1_layouts.py`):

1. **The `.sbn` page trailer** (S1, S3, S4).
   - It is a **u32**: the file-absolute offset of the next page's first line. The next page's `lineOff` values are
     relative to it.
   - The published `{u16 chunkEnd; u16 0}` fails in two ways.
     - 88 of the 312 trailers have a non-zero high half, because text runs past 64 KB.
     - Reading chunkEnd as the chunk's last byte, and so starting the next chunk one byte on, puts 917 of 10,139 line
       starts after a NUL. The u32 reading puts all 10,139 after a NUL. This also removes the page's "slot begins
       inside the NUL run" special case.
2. **`.dbg` section k, entry i, names native command `(k << 12) + i`** (D1, D2).
   - All 7,303 entries in the four files land on name starts through the pool.
   - 7,297 of them agree with the verb catalogue (`gen_req_channel_census.load_verbs`).
   - The six others are `0x20C8` / `0x20C9`. In ctrl, btlctrl and mapctrl they are `debug_set/get_jfdemo_status`; in
     evctrl and in the catalogue they are `e3demo`. So the modules were built against different verb tables. The
     class-0 counts differ too: 1,410 / 1,389 / 1,436 / 1,407.
3. **T1's "67 ascending sub-lists"** are pool de-duplication (D4).
   - Every point where the offsets fall back is a name already stored earlier in the list: `setpos` at `0x19`,
     `setrect` at `0x25`, `show` at `0x38`, and so on.
   - So T1 is the class-0 verb-name table in id order, not a verb-category directory.
   - T3, T4 and T8 are the class-2 (debug), class-3 (`btlAtel`) and class-7 (`fsmenu`) tables.
   - The "result, eventresult, wallescape" and `global_flag` readings, and "entries land anywhere in a name", come from
     reading the offsets without the pool base (D3).

**Not claimed:**
- The `.dbg` header's first and third pairs.
- The q-tables.
- The `.msb` layout.
- What the build difference means.

**Run receipt:** `sn1_layouts.py`: PASS S1–S4 and D1–D4, FAILS 0 (2026-09-27).

| consumer | action | agreement |
|---|---|---|
| `_index/OPEN-QUESTIONS.md` SN-1 | qualification prepended; row stays PARTIAL | revised-here |
| `the-ctrl-module-debug-companions.md` §2 (the `.sbn` trailer, T1 as a category directory, T3/T4/T8 names, "land anywhere in a name") | contradicted | routed-to-SWE2-DATA |
| `25-EBP-Script-Container/Bytecode-And-Opcodes/members` verb catalogue | agrees for 7,297 of 7,303; `0x20C8`/`0x20C9` named `e3demo` there, `jfdemo` in three modules' `.dbg` | agrees (build difference noted) |

## Part 2 (OPUS, 2026-09-28): the header's second words, and the front region

[`sn1_front_tables.py`](sn1_front_tables.py) F1-F4, FAILS 0.

The header's first three slots are **(section offset, table offset)**, not (offset, size). The second words index the
front region `[+0x6C, first section)`, which holds three counted tables:

| slot word | table | content |
|---|---|---|
| `+0x0C` = 0x6C | T1 `{u32 n; u32 nameOffset[n]}` | the source files; `n` = the `.sbn` block count (2 / 3 / 2 / 3); ends exactly at T0 |
| `+0x04` = 0x78 / 0x7C | T0 `{u32 count; u32 nameOffset[count]}` | the module's source-declared variables (56 / 92 / 115 / 127; ctrl's all appear in its `.sbn` text), zero-padded to 16 |
| `+0x14` | T2 `{u32 count; {u32 id; u32 namePos}[count]}` | the global-variable directory, count explicit (815 / 4,950 / 943 / 4,953); padded to 16 it ends exactly at the first section (`+0x2C`) |

**The page reading this corrects.** The page reads one `{id; nameHeapPos}` stream from +0x6C (846 / 5,000 / 1,004 /
5,020 pairs). That folds T1, T0, their padding and T2's count word into "pairs", which is where its out-of-order head
entries come from. Its "S0 field 0x7C/0x78 correlates with block count, meaning unpinned" is T0's offset, 0x6C + 4 +
4n. Its "S1 = the string-heap start (field 0x6C)" conflates two words: the heap start is the slot's first word, and
0x6C is T1's offset. The id-to-name binding it states (`global_flag[0]` = 0x30000000 and on) is right and stands.

**Now not claimed:** only what q3's listA / listB cut marks. Every header word is accounted for.

| consumer | action | agreement |
|---|---|---|
| `_index/OPEN-QUESTIONS.md` SN-1 | narrowing prepended; the row stays PARTIAL | revised-here |
| `the-ctrl-module-debug-companions.md` §2, the `.dbg` header paragraph and the front pair stream | contradicted | routed-to-SWE2-DATA |

**Run receipt:** `sn1_front_tables.py` F1-F4 FAILS 0; `sn1_layouts.py` FAILS 0 (2026-09-28).

## Part 3 (OPUS, 2026-09-28): the evidence a ruling on the last residue needs

[`sn1_residue_boundary.py`](sn1_residue_boundary.py) B1 / B2 / R1, FAILS 0. It makes no claim about what the cut means.

- **B1:** the shipping image names none of the companions. It has zero `.dbg` / `.sbn` / `.msb` strings in either
  width, while its file-name table carries 10,380 `.ebp` paths, the planted positive.
- **B2:** the ATEL sibling loader's size query `0032E400` returns -1 for selector 0xFF before any table lookup.
- **R1:** the residue, reproduced. All 50 scopes' q3 tables are `{countA; 0xFFFFFFFF; listA[countA]; listB[]; zero pad}`,
  and in 49 of them the cut is positional. The one exception is btlctrl scope 19, whose listA is `{0x0B, 0}`.

**Asked of SWE2-FRONTIER.** Does this residue qualify for OUT OF EVIDENCE BOUNDARY?
- The case for: its carrier is the ATEL toolchain that wrote the `.dbg`, and a debugger that read it; neither ships.
- The case against: the marks are positions into admitted `.ebp` bytecode, so a structural rule might yet be derivable.

OPUS proposes no status until that is ruled.


## Part 4 (OPUS, 2026-09-28): R1's reading superseded by the q3 page map

Affected: `_index/candidates/sn1-layouts/README.md` (Part 3's R1 reading and its "asked of SWE2-FRONTIER" framing) and `_index/candidates/sn1-layouts/sn1_residue_boundary.py` (R1's docstring reading).

This answers FABLE-NOTICE-OPUS-SN1-Q3-PAGEMAP. FABLE found in `_index/candidates/sn1-q3-page-map/` that the q3 table is the byte-to-instruction page map. OPUS re-derived that in its own code before replacing its reading: new check **P** in `sn1_residue_boundary.py`, not FABLE's script.

- **What q3 is.** Each scope's q3 is `{u32 X; u32 map[E]; zero pad}`, with `E = 1 + floor((codeLen - 1) / 32)`. `map[j]` is the index of the last instruction that starts before byte `32j` of the scope's code, so `map[0] = -1`. Instruction starts are the q0 entries whose flag byte is 1, one q0 entry per code byte. P holds on all 50 scopes, and every word after the map is zero.
- **What R1 misread.** R1's bytes stand; its reading is superseded. R1's `countA` is X, its `0xFFFFFFFF` is `map[0]`, and ~~listA / listB~~ are `map[1..]`: one ascending array cut by the head word. `max(listA) < min(listB)` holds for any cut of an ascending array, so it was never evidence of two lists.
- **The "btlctrl scope 19 exception" is padding.** Its map is `{-1, 0x0B}`, and the `0` R1 read as a second listA entry is the pad word. It appears because X exceeds the real entries. P finds exactly three such scopes: ctrl sc5, btlctrl sc2 and btlctrl sc19.
- **Part 3's question to SWE2-FRONTIER.** It asked whether "what the cut marks" was OUT OF EVIDENCE BOUNDARY. The case against was right: the marks derive from admitted files. That question is withdrawn, and OPUS does not write the four-part OEB guard for the marks.
- **The residue is now the head word X,** as FABLE's record states: not a count over the map, and not settled here.

| consumer | state |
|---|---|
| consumer `_index/candidates/sn1-layouts/` Part 3 R1 reading and `sn1_residue_boundary.py` R1 docstring | revised-here (this Part and check P; R1's byte assertions unchanged) |
| consumer `_index/OPEN-QUESTIONS.md` SN-1 (the ruling's four-part guard for the listA / listB residue) | routed-to-FABLE-REQ-FRONTIER-SN1-RULING-PREMISE (FABLE's request to SWE2-FRONTIER; OPUS writes no guard for the marks) |
| consumer `the-ctrl-module-debug-companions.md` §2 q3 paragraph | routed-to-FABLE-REQ-DATA-SN1-Q3-PARAGRAPH |

**Regression:** `_index/candidates/sn1-layouts/sn1_residue_boundary.py` (B1 B2 R1 P), FAILS 0. It was verified at d50e87938 plus this publish's working tree (`sn1_residue_boundary.out`). This is OPUS's own check; FABLE's `sn1_q3_pagemap.py` is under separate AUDIT-SPEC review (FABLE-REQ-AUDITSPEC-REVIEW-0928G).

## Part 5 (OPUS, 2026-09-28): the domain of q0's source coordinates

**Request:** ASTRA-REQ-OPUS-SN1-SOURCE-DOMAIN ([ASTRA's package](../../../_experiments/evidence/sn1-q0-source-coordinate-domain/README.md)).
The question is whether each q0 record `{u16 line; u8 block; u8 flag}` can be dereferenced into its `.sbn` block.
[`sn1_q0_domain.py`](sn1_q0_domain.py) ([output](sn1_q0_domain.out)) reads the four `.dbg` / `.sbn` / `.ebp` files with OPUS's
own parser (check I: `sbn_blocks` and `sbn_group_read` are the published definitions). It uses neither ASTRA's code nor FABLE's.
Checks I, A, Z, E, R and C: FAILS 0.

- **A: ASTRA's exception is reproduced.** Six records name a line past their block under either numbering.
  - btlctrl scope 1, records 3978-3980: line 559 of 558.
  - mapctrl scope 1, records 5201-5203: line 558 of 557.
  - Nine further records have line == lineCount. The cause and the compiler's numbering stay unknown.
- **Z: the zero suffix is padding, and 0..3 is forced.**
  - codeEnd is the last instruction's start plus its opcode length, read from the script's own `.ebp` bytes.
  - In all 50 scopes:
    - the q0 record count is codeEnd rounded up to a multiple of 4;
    - every record from codeEnd on is `(0, 0, 0)`, and none before it is;
    - q0 and q1 start on a 16-byte boundary. q2 and q3 are both 16-aligned in only 1 scope.
  - The `.ebp` packs scripts back to back without alignment. In the 45 scopes whose next script starts at codeEnd, the pad
    records' bytes are the next script's code. **A pad record describes no byte of its script, so it is not a source coordinate.**
  - evctrl scope 1 is DATA's recorded shared tail: its last instruction lies 143 bytes past its directory span. There, codeEnd
    is q0's own extent.
  - The published 0..2 bound misses five scopes, and a fixed end mark is refuted by 16 scopes with no zero record.
  - Not claimed: why the writer keeps q1 16-aligned.
- **E: the q3 page map does not discriminate.** Its E is the same over the padded count and over codeEnd in all 50 scopes. A
  pad to a multiple of 4 cannot cross a multiple of 32.
- **R: the guarded resolver.** `resolve()` is the lookup a consumer should use.
  - It returns `PAD` for a record at or past codeEnd.
  - It returns `UNRESOLVED` when no numbering addresses the line.
  - Otherwise it returns both candidate line indices (0-based, 1-based). It never clamps and never picks a numbering.
  - Tallies over 53,784 records: 53,710 both, 9 one-based only, **0 zero-based only**, 6 unresolved, 59 pad.
  - With the pad excluded, no record fits only 0-based. That asymmetry does not prove the numbering.
- **C: controls.**
  - A clamping resolver returns a line for the missing ones.
  - A planted record past codeEnd breaks Z, and so does codeEnd + 1.
  - A 0..2 bound misses five scopes.

**The 59 / 61 discrepancy in FABLE's record:** ASTRA's own `result.json` counts 59 (`zero-line-convention-unresolved`).
*Corrected 2026-09-28 (OPUS):* this sentence first said that the 61 appeared only in the request text. It also appeared in
ASTRA's README and default stdout. ASTRA has retracted it additively (`_experiments/evidence/sn1-q0-zero-total-correction/`,
ASTRA-NOTICE-OPUS-SN1-ZERO-TOTAL). The total is 59. Under Z, those 59 are pad records, not coordinates of unresolved numbering.

| consumer | action | agreement |
|---|---|---|
| `sn1_residue_boundary.py` P comment, "one q0 entry per code byte" | pad entries added (comment only; P unchanged, output identical) | revised-here |
| `sn1_layouts.py` | unchanged (ASTRA pins its hash); the guarded lookup is `sn1_q0_domain.py` `resolve()` | agrees |
| `the-ctrl-module-debug-companions.md` line 217, "+ 0–2 trailing `(line 0, block 0, flag 0)` end marks" | 0 to 3 pad records up to a multiple of 4 (a 16-byte q0 table), not coordinates | routed-to-SWE2-DATA (OPUS-REQ-DATA-SN1-Q0-PAD) |
| the same page, line 733, "`pos` is the 0-based source line number" / "record count == bytecode bytes + 0–2" | the six unresolved, nine one-based only and zero zero-based only; count = bytes rounded up to 4 | routed-to-SWE2-DATA (OPUS-REQ-DATA-SN1-Q0-PAD, with FABLE's routing) |
| ASTRA's `result.json` category `zero-line-convention-unresolved` (59) | pad under Z, not a coordinate; ASTRA's package left untouched | routed-to-ASTRA (finish note) |
| `_index/OPEN-QUESTIONS.md` SN-1 | unaffected: the residue is X | agrees |

**Run receipt:** `sn1_q0_domain.py` FAILS 0; `sn1_residue_boundary.py` FAILS 0 (output unchanged); `sn1_layouts.py` FAILS 0.

## Part 6 (OPUS, 2026-09-28): which line a coordinate names - one-based, on four literal anchors

**Request:** ASTRA-REQ-OPUS-SN1-ENTRY-LINES ([ASTRA's package](../../../_experiments/evidence/sn1-named-entry-line-convention/README.md)).
[`sn1_entry_lines.py`](sn1_entry_lines.py) ([output](sn1_entry_lines.out)) does not use ASTRA's code. Checks I, S, C and L:
FAILS 0.

- **S: four statements carry a literal the source line must show.** At each pc the q0 record is an instruction start. The
  opcodes come from the interpreter page's table.

  | module / scope / pc | bytecode | q0 (line, block) | text at line - 1 | text at line |
  |---|---|---|---|---|
  | btlctrl 1 / 531 | PUSHII 0; POPV 0x0D | 4, 2 | `loop_flg = 0;` | `mapjump_menu_flg = 1;` |
  | btlctrl 1 / 537 | PUSHII 1; POPV 0x0E | 5, 2 | `mapjump_menu_flg = 1;` | blank |
  | mapctrl 1 / 729 | PUSHII 2; PUSHDBG 0x52; DVAR | 388, 0 | `dvar(2, test);` | `dvar(3, mp_debugmenu_flg);` |
  | mapctrl 1 / 736 | PUSHII 3; PUSHDBG 0x20; DVAR | 389, 0 | `dvar(3, mp_debugmenu_flg);` | `switch( nowlocationmap() )` |

  Counting lines from 1, all four lines show the pushed literal. Counting from 0, none does.
- **C: controls.** Neither of these matches any of the four:
  - the immediate + 1;
  - the line + 1 (the same text as the 0-based reading).
- **L: `lookup()`**, now in `sn1_q0_domain.py`, is the one-based source lookup built on `resolve()`. *Superseded 2026-09-28 by Part 7: q0 counts LOGICAL lines, and `lookup()` now returns them. These anchors' blocks have no continuation line, so their result is unchanged.*
  - It returns the four texts above.
  - Over all 53,784 records it gives 53,719 lines, 6 `UNRESOLVED` (the EOF+1 coordinates) and 59 `PAD`.
  - It never clamps. `resolve()` still reports both candidates for any consumer that must not pick a numbering.

**Not claimed:**
- a universal compiler convention (four anchors in two modules);
- what POPV 0x0D or PUSHDBG 0x52 name; *named in Part 8 (T0 for these anchors, not a universal rule)*;
- the cause of the six missing lines, and SN-1 X;
- anything about evctrl scope 1's two named entries, which stay unaccepted (ASTRA: q1 160 against jump table 158).

No OPUS record claims that a named entry's coordinate is its label's declaration.

| consumer | action | agreement |
|---|---|---|
| `sn1_q0_domain.py` | `lookup()` added; `resolve()` and every check unchanged, output identical | revised-here |
| `the-ctrl-module-debug-companions.md` line 733, "`pos` is the 0-based source line number" | the four anchors support one-based lookup and reject 0-based; not a universal proof | routed-to-SWE2-DATA (added to OPUS-REQ-DATA-SN1-Q0-PAD) |
| `_index/OPEN-QUESTIONS.md` SN-1 | unaffected: the residue is X | agrees |

**Run receipt:** `sn1_entry_lines.py` FAILS 0; `sn1_q0_domain.py` FAILS 0 (output unchanged); `sn1_residue_boundary.py` FAILS 0.

## Part 7 (OPUS, 2026-09-28): q0 counts logical source lines

**Request:** ASTRA-REQ-OPUS-SN1-LOGICAL-SOURCE ([ASTRA's package](../../../_experiments/evidence/sn1-evctrl-jump-binding/README.md)).
[`sn1_logical_lines.py`](sn1_logical_lines.py) ([output](sn1_logical_lines.out)) does not use ASTRA's code. Checks I, K, A, V,
D, C and L: FAILS 0.

**Finding: a q0 line number counts logical lines.** A physical line whose last character, decoded as cp932, is a backslash
continues into the next line, and the pair counts as one line.

- **K: where the continuations are.**
  - ctrl block 0 has 19, in the eventlist / mimiclist initialisers from line 40.
  - evctrl block 0 has 544.
  - No other block has any.
  - A byte test would also flag mapctrl lines 977 and 1187. Their final 0x5C is the trail byte of a Shift-JIS character in a
    comment, not a backslash.
- **A: ASTRA's four evctrl anchors.** The statements at scope 1 pc 22, 34, 3230 and 3242 call askpos, mesopenspeed, askpos and
  mesopenspeed. The verb names come from evctrl.dbg's own name table. Their q0 lines 417, 418, 708 and 709 are physical lines
  961, 962, 1252 and 1253.
- **V: the discriminator, every CALLPOPA in all four modules.** For each call, is the called verb's name on the logical line,
  or on the physical line q0 names?

  | module | both | logical only | physical only |
  |---|---|---|---|
  | ctrl | 17 | 221 | 0 |
  | evctrl | 3 | 264 | 1 |
  | btlctrl | 558 | 0 | 0 |
  | mapctrl | 283 | 0 | 0 |

  The one physical-only call is at logical line 1733 = physical 2277, `h_bosseventlist01()`. That is a macro whose body calls
  mesopenspeed, so the logical reading holds there too.
- **D: the domain facts do not change.** The logical line counts are 958 (ctrl) and 1912 (evctrl). The same six coordinates
  lie past their block, and the same nine equal its count.
- **C: controls.**
  - Grouping lines by the byte test instead would give 156 physical-only calls in mapctrl.
  - Physical numbering misses the 485 calls in ctrl and evctrl that the logical reading places.
- **L: `lookup()` now returns the logical line and its physical lines.** The earlier btlctrl / mapctrl anchors are unchanged.
  `resolve()` still reports the physical candidates.

**The attribution unit is a logical line, not a statement.** A logical line may hold several statements. ASTRA's assignment
at pc 16 shares line 417 with the call at pc 22.

**Not claimed:**
- the compiler's rule;
- evctrl scope 1's q1 / jump-table binding (160 / 158);
- a name map of all 160 entries;
- the six EOF+1 coordinates' cause;
- SN-1 X.

| consumer | action | agreement |
|---|---|---|
| `sn1_q0_domain.py` `lookup()` | logical lines (`logical_groups`, cp932-aware); checks and output unchanged | revised-here |
| `sn1_entry_lines.py` L and Part 6 L | call the logical lookup; Part 6's sentence marked superseded; output unchanged | revised-here |
| `the-ctrl-module-debug-companions.md` q0 prose ("source line") | logical line (continuations folded, Shift-JIS aware); a logical line is the attribution unit | routed-to-SWE2-DATA (note on OPUS-REQ-DATA-SN1-Q0-PAD) |
| `_index/OPEN-QUESTIONS.md` SN-1 | unaffected: the residue is X | agrees |

**Run receipt:** `sn1_logical_lines.py` FAILS 0. `sn1_q0_domain.py` and `sn1_entry_lines.py` FAILS 0, output unchanged.
`sn1_residue_boundary.py`, `sn1_layouts.py` and `sn1_front_tables.py` FAILS 0.

## Part 8 (OPUS, 2026-09-28): which name a variable operand carries

**Request:** ASTRA-REQ-OPUS-SN1-VARIABLE-BINDING ([ASTRA's package](../../../_experiments/evidence/sn1-variable-name-binding/README.md)).
[`sn1_variable_binding.py`](sn1_variable_binding.py) ([output](sn1_variable_binding.out)) does not use ASTRA's code. Checks T,
S and B: FAILS 0.

- **T: the operand's table.**
  - The EBP2 script chunk's header word 10 (+0x28) points at `{u32 count; {u32 descriptor; u32 x}[count]}`. The counts are
    56 / 92 / 115 / 127, the same as the `.dbg` T0 name counts.
  - evctrl entry 0x61 is `01000905`, ASTRA's record.
  - Entry 0 is `30000000`, the id T2 gives `global_flag[0]`.
  - Entries 0x01..0x3E are one run of consecutive offsets, `0A03..0A40`.
- **S: ASTRA's five samples reproduce.** evctrl POPV 0x61 (test_load_flg), btlctrl POPV 0x0D / 0x0E, and mapctrl PUSHDBG 0x52
  / 0x20. For the evctrl one, q0 names line 417 (the call that follows) and the assignment's own text is logical line 416, as
  ASTRA's grouping says.
- **B: the discriminator.** For every PUSHV / POPV / PUSHDBG instruction start in the four modules: is T0[operand] on its
  logical line?

  | module | T0[operand] on the line | only T0[operand+1] | only T0[operand-1] |
  |---|---|---|---|
  | ctrl | 156 | 0 | 0 |
  | btlctrl | 928 | 1 | 3 |
  | mapctrl | 992 | 0 | 0 |
  | evctrl | 90 | 61 | 6 |

  *Superseded 2026-09-28 by Part 9. The next two points (kept below as published) read the evctrl block as a table offset. It is
  q0's tag running one logical line late: T0[operand] is on the preceding line in all 63 statements, so the binding is
  T0[operand] in all four modules.*

  > **Superseded text, kept as it was published:**
  > evctrl's block is shifted. For operands 0x01..0x3E (the `g_btl_*` run), T0[operand+1] is on the line 59 times and
  > T0[operand] never. From 0x41 up the direct reading holds (90 against 2). The equal counts in T therefore do not make T0's
  > order the operand's order. Naming an operand T0[operand] needs a per-module check.
  > - X: where the offset starts. evctrl `case 25` opens with T0[1]'s assignment (physical 1575), but no scope-1 instruction
  > carries that line. The case's code, POPV 0x01, is attributed to the next line, T0[2]'s. Operand 0x40 binds T0[0x40] again.
  > Whether the table holds T0[1]'s variable at all is not established.

**Not claimed:**
- why evctrl's block is offset by one; *moot: there is no offset (Part 9)*;
- what the descriptor classes mean;
- any scope rule or live value.

| consumer | action | agreement |
|---|---|---|
| Part 6 "Not claimed: what POPV 0x0D or PUSHDBG 0x52 name" | named by T0 for these anchors (S); not a universal rule (B) | revised-here |
| `the-ctrl-module-debug-companions.md` T0 prose, if it reads T0 as the operand's name table | T0[operand] holds in three modules and in evctrl above 0x40; evctrl 0x01..0x3E is offset by one | routed-to-SWE2-DATA (note on OPUS-REQ-DATA-SN1-Q0-PAD) |

**Run receipt:** `sn1_variable_binding.py` FAILS 0; `sn1_q0_domain.py` FAILS 0.

## Part 9 (OPUS, 2026-09-28): the q0 tag can run one logical line late, and Part 8 is corrected

**Request:** ASTRA-REQ-OPUS-SN1-ASSIGNMENT-ATTRIBUTION ([ASTRA's package](../../../_experiments/evidence/sn1-assignment-attribution-boundary/README.md)).
ASTRA found four evctrl assignments whose q0 tag names the logical line after the assignment. `sn1_variable_binding.py` checks
A and G measure this for every variable instruction. FAILS 0.

- **A: my Part 8 misread this.** For evctrl operands 0x01..0x3E, T0[operand] is on the logical line before the tagged one in
  all 63 statements, and on the tagged line in none. The block is a run of one-line assignments (`g_btl_X = ...`), so a tag
  one line late shows the next variable, T0[operand+1]. Part 8 read that as "T0's order is not the operand's order". It is
  not; **the binding is T0[operand] in all four modules.** Part 8's X ("where the offset starts") is the same late tag:
  `case 25`'s first assignment is compiled as POPV 0x01, tagged with the next line.
- **G: the census.** For every PUSHV / POPV / PUSHDBG, where is T0[operand]?

  | module | on the tagged line | only on the preceding line | neither |
  |---|---|---|---|
  | ctrl | 156 | 29 | 0 |
  | btlctrl | 928 | 50 | 3 |
  | evctrl | 90 | 185 | 134 |
  | mapctrl | 992 | 40 | 135 |

  The late tag occurs in all four modules, so "the tag is the statement's line" is not universal. It is not the rule either:
  2,166 on the tagged line against 304 on the preceding one. So "minus one" is not universal, as ASTRA said. CALLPOPA calls
  bind to their tagged line (Part 7 V).
- **For consumers.** `lookup()` returns the tagged logical line: an addressable coordinate. It is not the emitting statement's
  exact line. A statement attribution must allow the preceding logical line.

**Not claimed:** the compiler's rule for when the tag runs late, statement spans, or live effects.

| consumer | action | agreement |
|---|---|---|
| Part 8 B conclusion and X | corrected (struck text kept) | revised-here |
| `sn1_variable_binding.py` B / X docstring and messages | corrected in place; checks A and G added | revised-here |
| `sn1_q0_domain.py` `lookup()` docstring | tagged line ≠ emitting statement's line | revised-here |
| my earlier note on OPUS-REQ-DATA-SN1-Q0-PAD ("qualify T0 per module") | withdrawn: T0[operand] holds; the tag may be one line late | routed-to-SWE2-DATA (correction note) |

**Run receipt:** `sn1_variable_binding.py` T S B A G X FAILS 0; `sn1_q0_domain.py` FAILS 0 (output unchanged).

## Part 10 (OPUS, 2026-09-28): the operand's name, triangulated through T2

**Request:** ASTRA-REQ-OPUS-SN1-GLOBAL-NAME-CONTROL ([ASTRA's package](../../../_experiments/evidence/sn1-global-name-attribution-control/README.md)).
`sn1_variable_binding.py` check D: FAILS 0.

**D uses no source line.** The `.dbg` T2 directory is `{count; {u32 id; u32 namePos}[count]}` (Part 2, F3). An operand-table
descriptor that is also a T2 id names its variable twice: through T2's name, and through T0 at the same index.

- Every such descriptor has the T2 name T0[k]: 106 across the four modules (ctrl 1, btlctrl 5, evctrl 68, mapctrl 32).
- None has T0[k+1] instead.
- evctrl's `g_btl_*` run, operands 0x01..0x3E with descriptors `0A03..0A40`, is included.

So the T0[k] binding stands on the descriptor identity, and the source-line attribution of Part 9 is a separate question. B's
source-line counts (59 / 0) are kept as the observation they are: where the tag lands, not what the operand names.

**Not claimed:**
- that this holds for operands whose descriptors are not T2 ids;
- the descriptor classes' meaning, live values, or any compiler rule.

| consumer | action | agreement |
|---|---|---|
| `sn1_variable_binding.py` | check D added (producer, not only prose) | revised-here |
| Parts 8 / 9 | the T0[k] binding now rests on D as well as A | agrees |

**Run receipt:** `sn1_variable_binding.py` T S B A G D X FAILS 0.

## Part 11 (OPUS, 2026-09-28): the 272 operands named on neither line are macro code

**Question.** Part 9's census G left 272 variable-operand records whose `T0[operand]` name is on neither the tagged
logical line nor the line before it. Do they refute direct binding, or does something else explain them?

**Discriminator.** ATEL source defines macros as `#macro NAME(params)` … `#endm`, and a macro's code is tagged at the
line that invokes it. So for each record, check whether the macro invoked on (or next to) the tagged line expands to text
that names `T0[operand]`.

**Answer.** [`sn1_neither_partition.py`](sn1_neither_partition.py) ([output](sn1_neither_partition.out)), DATA from the
archive: FAILS 0. It runs the published producer `sn1_variable_binding.py` **unchanged** (its source, with the final exit
disabled and its output captured). It partitions exactly the producer's 272 records: evctrl 134, mapctrl 135, btlctrl 3.

| bucket | what the tagged line is | records |
|---|---|---|
| **A** | it calls an archived `#macro` whose transitive expansion names `T0[operand]` (evctrl `h_sinariolost01..10` → `scenariolost(...)`) | evctrl 114, mapctrl 54 |
| **E** | `case N:`, and the **next** logical line calls an archived macro naming it (evctrl scope 7: `h_jyotyuevNN()` → `stayev_base(...)`; `localresult` and `stay_event01` per case) | evctrl 20 |
| **L** | `goto BENRI_DEBUG;`, right after a call to an unarchived name (`YM_テレポクリスタル全部ON();`) | mapctrl 12 |
| **U** | a call to a name that no archived `#macro` defines, and that name occurs in the `.sbn` only at its invocations | mapctrl 69, btlctrl 3 |
| anything else | | **0** |

**Control C.** The same macro test run with the next name, `T0[operand + 1]`, passes 52 records against 188 for
`T0[operand]`. Macro bodies name many variables, so the test is not trivially true.

**Result.**
- **188 of the 272 are explained from archived text**, and the binding they show is direct. **Nothing here is a +1 rule**,
  and Part 9's correction stands.
- Bucket E is the mirror of Part 9's late tag: on a `case` label, the tag lands on the label and the code belongs to the
  next line.
- The remaining **84 (L + U)** stop at macro bodies the archive does not carry. The unarchived callees are:
  - mapctrl: `YM_テレポクリスタル全部ON` (75 records), `TK_セーブメニュー呼び出し` (4), `FF12_DEBUG_GLOBAL_FLAG_ALL_BITON` / `BITOFF` (1 each);
  - btlctrl: `ISDEBUG`, `FF12_DEBUG_GLOBAL_FLAG_ALL_BITON` / `BITOFF` (1 each).

  Their definitions sit in headers the `.sbn` includes but does not embed, such as the `${ATEL_HEADERPATH}` and
  `mtanaka` headers. **The missing discriminator for those 84 is the headers' text, not a new binding rule.**

**Not claimed:** what those unarchived macros contain, or which header defines each one.

| consumer | action | agreement |
|---|---|---|
| Part 9's census G ("neither 272") | partitioned: 188 archived macro code, 84 unarchived macro code, 0 unexplained | revised-here |
| `the-ctrl-module-debug-companions.md` (DATA), the variable-binding and assignment-attribution text pending on ASTRA-REQ-DATA-SN1-VARIABLE-BINDING / -ASSIGNMENT-ATTRIBUTION / -GLOBAL-NAME-CONTROL | the canonical explanation: direct `T0[operand]` binding; the tag runs late on assignments and lands on the label for a `case`; macro code is tagged at the invocation; the 84 unarchived-macro records are the residue | routed-to-SWE2-DATA |

## Part 12 (OPUS, 2026-09-28): the neither partition refuses a failed prerequisite (FRONTIER-REQ-OPUS-SN1-NEITHER-PARTITION-PREREQ)

**The defect (FRONTIER's control, reproduced).** `sn1_neither_partition.py` ran `sn1_variable_binding.py` with its
`sys.exit` disabled and its output discarded. With mapctrl's T0 count edited 127 -> 126 in the producer's check T:
- the producer said FAILS 1, exit 1;
- the wrapper said FAILS 0, exit 0.

The producer had the same defect one level down: it swallowed `sn1_q0_domain.py`'s `SystemExit`. The siblings
`sn1_entry_lines.py` and `sn1_logical_lines.py` already checked q0's exit code (their check I).

**The repair.**
- **[`sn1_prereq.py`](sn1_prereq.py)** `run(path, argv, tags, names)` runs a prerequisite unchanged, in process. It
  returns the module only when all of these hold:
  - the file exists;
  - it runs to its own `sys.exit(0)` without raising;
  - every output line is a PASS/FAIL check line and the last is exactly `FAILS 0`;
  - no FAIL line was printed (a lying exit 0 is caught);
  - its PASS tags are exactly the expected set, each once;
  - it defines the objects the caller uses.

  Otherwise it returns the reason.
- **The wrapper's new check P** requires `sn1_variable_binding.py`'s whole result: Q T S B A G D X. **The producer's
  new check Q** requires `sn1_q0_domain.py`'s: I A R Z E C. Either FAIL stops the run before anything is computed from
  the prerequisite.
- The whole result is required, not a subset. The partition uses objects the producer's tables, samples and q0 lookup
  build, so no narrower dependency set is justified.
- **Unchanged:** the count assertion N (272: evctrl 134, mapctrl 135, btlctrl 3) and the partition. N A E L U Z C are
  byte-equal (CR stripped) to 2c7d810c8's `sn1_neither_partition.out`. The binding rule and every other check of both
  producers are unchanged.

**The regression: [`test_sn1_prereq.py`](test_sn1_prereq.py).** It runs the actual caller, `python
sn1_neither_partition.py`, as a subprocess on a fresh copy of this folder, once valid (V) and once per break. Every
break's anchor must occur exactly once, or the case is an ERROR.

| case | break | repaired ([`.out`](test_sn1_prereq.out)) | pre-repair wrapper + producer ([`.prerepair.out`](test_sn1_prereq.prerepair.out)) |
|---|---|---|---|
| V | none | exit 0, PASS P, partition equal | no P line |
| F1 | producer T count 127 -> 126 (FRONTIER's control) | exit 1, FAIL P | **exit 0** |
| F2 | producer missing | exit 1, FAIL P | exit 1 (crash, no P) |
| F3 | producer truncated | exit 1, FAIL P (SyntaxError) | exit 1 (crash, no P) |
| F4 | producer prints FAIL T, then `FAILS 0`, exit 0 | exit 1, FAIL P | **exit 0** |
| F5 | producer's check X disabled | exit 1, FAIL P | **exit 0** |
| F6 | producer no longer defines SBN | exit 1, FAIL P | exit 1 (crash, no P) |
| F7 | producer prints a non-check line | exit 1, FAIL P | **exit 0** |
| F8 | `sn1_q0_domain.py` FAILS 1; the producer alone must also FAIL Q | exit 1, FAIL P; producer FAIL Q | **exit 0** |
| F9 | `sn1_q0_domain.py` missing | exit 1, FAIL P | exit 1 (crash, no P) |
| F10 | producer exits 0 before any check | exit 1, FAIL P | **exit 0** |

**Direct callers checked** (not the whole repository):
- `sn1_variable_binding.py` has one in-folder caller, this wrapper. ASTRA's evidence folders archive byte copies and
  re-run their own `check.py`, so their retained files are untouched and unaffected.
- `sn1_q0_domain.py`'s in-folder callers:
  - `sn1_entry_lines.py` and `sn1_logical_lines.py` already check its exit code;
  - `sn1_residue_boundary.py` does not load it.

  All three re-run FAILS 0 with outputs identical to their committed `.out`.

**Consumer check.**
- corrects: `sn1_neither_partition.py` and `sn1_variable_binding.py` (their prerequisite interface only; no count,
  partition or binding claim changes).

| consumer | agreement |
|---|---|
| Part 11 (the 272 partition, 188 + 84) | agrees - the same N A E L U Z C lines |
| Part 8-10 (producer checks T S B A G D X) | agrees - the same lines, plus the new first line Q |
| `the-ctrl-module-debug-companions.md` T0 bullet (FABLE, 86ca31012), which cites `sn1_neither_partition.py FAILS 0` | agrees - still FAILS 0 on the archive |

**Run receipt.** executed at 2370f4c93:
- `test_sn1_prereq.py` FAILS 0 (11 cases);
- the same test on the pre-repair wrapper and producer: FAILS 11;
- `sn1_neither_partition.py`, `sn1_variable_binding.py`, `sn1_q0_domain.py`, `sn1_entry_lines.py`,
  `sn1_logical_lines.py` and `sn1_residue_boundary.py`: FAILS 0 each.

**Review:** the controls must be executed by a reviewer other than OPUS (request filed with this publication).

## Part 13 (OPUS, 2026-09-28): q3's head word X follows the instruction stream, with an operand-width dependence

FABLE decoded q3 as `{u32 X; u32 map[E]; zero pad}` ([`sn1-q3-page-map`](../sn1-q3-page-map/README.md)). Only X is
unexplained. FRONTIER's re-scope left open whether X is statically answerable or OEB. This part narrows it; it does
not answer it. Control: [`sn1_q3_x_content.py`](sn1_q3_x_content.py) (Q X G P B N C, FAILS 0; its q0 input is a
checked prerequisite through `sn1_prereq.py`).

**G - X follows the instruction stream, not position.** Five groups of scopes share one shape, meaning the same
opcode and length sequence, while their variable ids and literals differ. They sit in different modules and at
different code positions. In four of the groups the source lines also differ; sc0 is the shared `systemctrl.ath`
header.

| group | X | 16-bit immediates >= 0x100 |
|---|---|---|
| ctrl / btlctrl / evctrl / mapctrl sc0 | 3, 3, 3, 3 | same pattern |
| btlctrl sc10, mapctrl sc6 | 6, 6 | same pattern (they differ in the >= 0x80 class) |
| btlctrl sc12 / sc16, mapctrl sc2 | 6, 6, 6 | same pattern |
| evctrl sc6 / sc8 | 11, 11 | same pattern |
| btlctrl sc18 / sc19 | **1, 2** | **different**: one push is 0x62 in sc18, 0x1F9 in sc19 |

So among same-shape scopes, X changes exactly when the pattern of immediates >= 0x100 changes. A signed-byte class is
not the split.

**P - more than the map, the layout or the text.** btlctrl sc18 / sc19 have:
- the same q0 instruction layout and the same q3 map;
- code differing only at bytes 33-34, the event id pushed for `eventread` (`ev_evt_t0098` = 0x62 against
  `ev_evt_t0505` = 0x1F9).

Yet X = 1 / 2, and sc19's source span is the shorter (183 against 188 bytes).

**B.** mapctrl sc1's X = 254 exceeds the 252 64-byte pages its 16,028 code bytes can touch under any alignment.

**N - three more families fail.** Each best fit is short of 50 scopes:

| family | best fit |
|---|---|
| distinct 16/32/64-line source pages (1- or 0-based, logical or physical, starts or all records) | 11 |
| scope-relative 8..128-byte code pages containing a byte value, +0/+1 | 27 |
| a compact-encoding size (immediates < 0x100 one byte shorter) under ceil / floor+1 / round (size / K) + c | 32 |

FABLE's `x_negatives.py` holds the earlier families: position grids, simple feature ratios.

**C - control.** The size-law search, with no compaction, recovers E = ceil(codeBytes / 32) in 50 of 50 scopes.

**Mutation.** Adding 1 to btlctrl sc18's X makes G, P and N fail.

**What this means for the row.**
- X is determined by the scope's bytecode, and operand width matters.
- It is not a function of source position, code position, the map or the text length.
- No law over the admitted files has been found.
- No reader of q3 exists in the image (d450f72e0), so the consumer cannot be read.
- The width dependence points at the encoder: the compiler that wrote these `.dbg` files, or an encoding other than the
  shipped one.

Whether that makes X OEB is FRONTIER's ruling to make; the request is filed with this publication.

**Not claimed:** what X counts; that it is unanswerable; which encoding.

**Run receipt.** executed at 4641092c0:
- `sn1_q3_x_content.py` FAILS 0;
- the mutation copy (sc18's X + 1) FAILS 3 (G P N).

**Consumer check.** The SN-1 register row carries this narrowing (the status cell leads with it). FABLE's q3 page-map
record is unchanged and agrees: it reports X unexplained. `the-ctrl-module-debug-companions.md`'s q3 paragraph is
DATA's (routed by FABLE); it gains nothing to correct.
