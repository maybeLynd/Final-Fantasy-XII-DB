# SWE2-AUDIT-SEM review: FABLE's DD content work on the 15 gameplay-folder pages (2026-09-30)

*SWE2-AUDIT-SEM (independent semantic auditor). Requested by FABLE; assigned by OPUS.*

| | |
|---|---|
| request | `FABLE-REQ-AUDITSEM-REVIEW-DD-GAMEPLAY-0930` |
| reviewed | `797b72780` (author **FABLE**): the 15 pages of folders 04-13, register section GR (GR-1..GR-19), record [`dd-content-fable-0930`](../dd-content-fable-0930/README.md) and its two consumer checks. None of the 15 pages or the GR rows changed between `797b72780` and the HEAD this review ran at (`288ba0e89`). |
| image | `FFXII_TZA.exe` SHA-256 `73461d08…d89721f8` |
| checkers | [`ddgp_sem.py`](ddgp_sem.py), [out](ddgp_sem.out): 60 PASS, `FAILS 0` (capstone on the image, the shipped `battle_pack.bin` through the UQ-80 parser). [`gr_rows_check.py`](gr_rows_check.py), [out](gr_rows_check.out): register and candidate overlap per GR row. [`documented_rule.out`](documented_rule.out). [`producer_rerun/`](producer_rerun/): the record's ten scripts re-run. |
| **verdict** | **ACCEPT-WITH-NARROWING.** The corrections sampled hold at the byte level: 24 of the 40, on 13 of the 15 pages. So do the newly cited claims sampled, and the rule verdicts reproduce. 15 GR rows are real residue as registered. Four need their premise corrected or narrowed: GR-2, GR-7, GR-12 and GR-19. The register rows GR-3 and GR-8 carry leaked draft placeholders. GR-16 is review debt, not a game question. |

Evidence classes are kept apart below:
- **static** means read from the image;
- **data** means the shipped tables or scripts;
- **record** means what the package's own files say.

Nothing here is live.

## 1. The corrections (static and data)

FABLE's consumer checks list 21 corrections (`-dd-a`) and 19 more (`-dd7`). The sample below covers every page with
corrections except the spawn page's call-list and copy fixes and the ranged page's slot-22 claim. Each line is a
`ddgp_sem.py` check.

| # | page | correction | check | result |
|---|---|---|---|---|
| a1 | where-a-stat-number | the helpers take base HP / base MP, not a level | X7. `002F8E50` (30 B) = `(r8+1)·ecx·edx/100`, called with `r8 = row+0x18`, `edx = row+0x19` and `ecx = stats+0x08` (`002FF06F`–`002FF07B`). `002F9180` (21 B) = `ecx·edx/100` with the s16 `stats+0x0C` and `row+0x1D`. | holds |
| a2 | where-a-stat-number | the "affinity" dwords are status masks | X9. `rsi = stats+0x24` (`002FEFAB`). `row+0x4C` is ORed into `+0x38` (`002FF0D3`) and `row+0x48` into `+0x3C` (`002FF0D9`). | holds |
| a3 | where-a-stat-number | max HP floors at 1 | X8. `r15d = 1` (`002FF5A7`); `cmp r14, r15` / `mov r8, r15` (`002FF7B1`–`002FF7B6`). | holds |
| a4 | action row | `+0x0A` is the MP cost, read as a byte | X10: byte reads at `002F962B` and `0031DBD2`. G5: all four `+0x0A` sites in the UQ-106 hop census are width 1. | holds |
| a6, a7 | action row | `+0x3A` is 10–16; `+0x28` is on the 26 Quickening-family rows | X11 (data, this review's own tally). `+0x3A` holds 10–16 on 68 rows, with 10 and 11 once each. `+0x28` holds 120–153 on rows `0xD0`–`0xE5`, `0xE7`, `0xEA`, `0xED` and `0xF1`. | holds |
| a9 | ranged recipes | the first list runs at execution | X12. `BattleUnit_AdvanceStandardActionState` calls `BattleAction_EvaluateTargetPreviews` at `00304F1D`, which calls `00385680` at `00303910`. `003859FF` is its indirect step call. | holds |
| a13 | field-runtime pass | wait `+0x27` is set by kinds 3, 6 and 7 | X13. The jump table at image `+0x13E3CC` decodes to kind 3 → `0025E027`, 6 → `0025E058` and 7 → `0025E083`. Kind 7's arm jumps to kind 6's test at `0025E06E` (`0025E08F`). | holds |
| a15 note | battle-record-kind | `00321810` stores 0 at `+0x19` | X14: `lea rcx, [rax+0x19]`, then `mov [rcx], dl` with `dl = 0` (`0032181F`). | holds |
| a18 | spawn | the FRONTIER-subtree sizes | X24: 563 / 143 / 233 / 1,001 / 491 / 21 B are the extents | holds |
| a20, bit 22 | combo pair | unit flag bit 22: set `003130D2`, cleared by `00308270` | X15: `or qword [rbx], 0x400000`; mask `0xFFFFBFFFFFBFFFFF` at `003082DF` | holds |
| HUD cap | combo page | two digits packed one per nibble, capped at `0x12` | X15 (`00289DF2`–`00289E08`). The packing makes `0x12` the decimal "12", not an interpretation. | holds |
| dd7 C2 | gambit page | the window is `(int)([01DFE0B8]·30.0)·window` | X19. `[008F8D80]` = 30.0 and `[0208936C]` is the window. | holds |
| dd7 C3 | gambit page | chaining only under the flag pair; otherwise the original list; buffer 0 only | X20 (`003016BE`–`003017BF`) | holds; see N4 |
| dd7 P1 | party page | `00321100` returns the index when the class-`0x17` check fails **or** when the selector is `0xFF` | X17 | holds. The consumer check's note that the five-maps page has it backwards is also right. |
| dd7 P2 | party page | the teardown copy is `0xB0` bytes, from `+0x7A0` to `+0x6F0` | X18: eleven `movups` pairs | holds |
| dd7 S1 | shop page | `shop_first_open_entry` returns an entry pointer (the last entry on no match) | X21 (`002FAD4F`, `002FADB0` / `002FADBF`, `002FAE2D`) | holds |
| dd7 S2 | shop page | `002536A0` is an 8-byte getter of `[020927C0]`; the mask is `1 << (i & 7)` | X21 | holds |
| dd7 R1 | death page | `00312280` is `…AndLoot` | X1 (function table) | holds |
| dd7 R2 | death page | counter `0x11` = `span·perLevel.u16 + base.u16`, through the thunk | X3. `003170AA`–`003170D8`; `00253770` (5 B) is `jmp 00316A50`; `002E2380` (12 B) is the second counter-17 feeder. | holds |
| dd7 R3 | death page | effect id 12, not status 12 | X4: byte `+0x69` / `+0x79` bit 4 is bit 12 of the 16-byte layers `+0x68` / `+0x78`. `augment12*.py` re-run identical. | holds |
| dd7 R5 | death page | `00319CA0` is 394 B; 227 B is `00319A20` | X25 | holds |
| NG− section | death page | `00236780` is bit 14 of `[[02EBF190]+4]`, set from request bit 2 of `02089344`; the EXP add is skipped and the shown EXP zeroed | X5, X6. The name "New Game Minus" is the verb catalogue's, and the page says so. | holds |
| counter 11 | death page | LP feeds counter `0xB` | X2. `mov cl, 0xb` (`00312489`), `edx = esi` (`00312484`), call `00316A50` (`00312496`). | holds |

**The producer's scripts reproduce.**
- `augment12.py`, `augment12_equipment.py`, `eq_action_names.py`, `eq_slot5_census.py` and `eq_slot5_party.py`: each
  output is byte-identical to the committed one.
- `adr_tally.py`, `rwr_recipes.py`, `rwr_slots.py`, `wsn_lists.py` and `record_flag_or_sites.py` have no committed
  output (N3). Their outputs from this run are in `producer_rerun/` and agree with the numbers on the pages:
  - 39 / 68 / 436;
  - `+0x0B` on rows 182–207;
  - recipe 25 / 26 lists;
  - three status lists of 16 / 16 / 12;
  - 15 `or` sites, with the 8 of 8 control.

**The rule verdicts reproduce.** `documented_rule.py` on the 15 published pages gives:
- PARTIAL: 12;
- READY: where-a-stat-number and ranged-weapon-recipes;
- READY-WITH-POINTER: spawn placement.

This matches the record's table, and no status word was raised. The self-test passes (32 cases).

## 2. The GR rows: real residue, correct premises? (static, data, record)

`gr_rows_check.out` lists, for each row, the register rows and parent-commit candidate folders that share its
addresses. Every row is named on its page. Reading the overlaps gives:

| row | finding |
|---|---|
| GR-1 | **Residue; the premise holds** (G1). The displacement sweep over `0025DF00`, `0025E4C0` and `002621D0` finds the 2 sets and the 10 interpreter clears (the positive control), and no other access covering `+0x27` at any width. The two callees handed `slot+0x18` (`002674B0`, `00267420`) touch only its `+4`, `+0xA` and `+0xE`. The row's image-wide question stands. |
| GR-2 | **Premise stale in part (correction C3).** "No reading names the values themselves", and the static plan to "census the immediate values … `setfreetargettype` … `btlAtelSetUnitType`", were half done before this commit. SD-160's record (`af6684173`, an ancestor of `797b72780`) decoded all 63,432 calls of both verbs; every argument is a constant (`sd160_census.out`: `btlAtelSetUnitType` 0–3, `setfreetargettype` 1 / 3 / 4 / 6). It already joined value 3 to its scripts (allied third parties and event combatants). GR-2 cites none of it (F2), and its list of reader values omits 6, which 45 `setfreetargettype` sites pass. |
| GR-3 | Residue (G3). `0028AAA0` (1,692 B) has one caller, `00289A10` at `00289B7C`, and is unread. |
| GR-4 | Residue. The hop census has no `+0x28` site (G5). UQ-106 is SUPERSEDED, with its pointer on the page. |
| GR-5 | Residue. Every `+0x0A` reader is byte-wide (G5), and `+0x0B` is non-zero only on rows 182–207 (X11). |
| GR-6 | Residue (G6). `00325476` / `00325968` compare with `di = 0xFFFF` (`00325384`) and branch to `00325702` / `003259E3`. |
| GR-7 | **"Who reads kind 10" is one caller query away (correction C2).** `AiTargetSelector_ResolveOperandValue` (`00321190`) is called with kind 10 by `AiOrder_EvaluateTargetSelector` (`00303084` `ecx = 0xA`, call `00303088`). It is also called by `002FE660`, which forces kind 10 for action ids `0x4122` / `0x4123` (`002FE6B3`–`002FE6CD`) and then sets, adds, `bts` or `btr`s the value (`002FE71A`–`002FE73D`). `002FE660` has no direct caller, so it is reached through a table. `00312170` itself reads and rewrites kind 10 (`00312248`, `0031225E`). The residue is what the `00303088` selector arm tests against the mask, and what orders `0x4122` / `0x4123` are. (OPUS holds GR-7; this bears on the premise only.) |
| GR-8 | Residue. FD-2 and CS-6 map the prefix and the index, as the row says. |
| GR-9 | Residue. UQ-121 closed on "subgroups have no table-wide meaning" and left exactly this entry route unregistered. |
| GR-10 | Residue; its cited sites exist (G10). The kind and mask writers were not re-traced here. |
| GR-11 | Residue. **Wording nit N2:** `+0x138` is a pointer. The install copies `[[[actor+0xC0]+0x138]+0x30..+0xDF]` (G11), so "the `+0x138` block" should read "the block `[+0x138]` points to". The same applies to the static plan. |
| GR-12 | **The second question's premise is wrong in part (correction C1).** "Why an empty failure answer is `0` where the entry's empty marker is `0xFFFF`": `00273270` answers **`0xFFFF`** on both early exits (id 0 at `0027328F`, no actor at `00273299`, both to `002732C1 mov eax, 0xffff`; F12). It answers 0 only when `0031FF70` leaves the preset: `[rsp+0xCC] = 0x0000FFFF` (`002732A7`) is returned `>> 16` (`002732BC`), and the filler stores the item as `word << 16`. The preset puts the sentinel in the low half, which the shift discards. So the "asymmetry" has a mechanical reading, and the open part is what actions `0x9C` / `0x9D` do. The data half holds: rows `0x9C` / `0x9D` point at bank-0 entries 156 / 157, with `+0x1E` = 13 (X11). |
| GR-13 | Residue (G13). The layout-A driver reads `+8` / `+0x10`; layout B keeps the price at `+8`, with the bit-31 zero sentinel. |
| GR-14 | Residue (G14). The build is at `005656AE` and the move at `0056E55A` / `0056E561`. |
| GR-15 | Residue; not re-traced. |
| GR-16 | **Not a game question (N1).** The premise is true: a board search for SECTION-03 finds OPUS's owner review and publications (`OPUS-PUB-186-SECTION03`, `-230-`) and `ASTRA-REVIEW-RETAINED-REWARD-BINDINGS` (a different package). There is no auditor verdict on `continuation-section03-reward-bindings`. But what closes it is a board review, and no request for that review exists, so the debt has no owner. File the request (to SWE2-AUDIT-SPEC per REVIEW-POLICY), and let the row point to it. |
| GR-17 | Residue (G17). The slots are referenced only by `lea` in the binder `0023A160`, which is what the static plan orders against the retire path. |
| GR-18 | Residue; not re-derived. |
| GR-19 | **Framing to narrow (correction C4).** `003377C0` is not a drop-specific body. Besides `00319490` it is called by `00334E00` (×2), `00339630` and `0033BD70`, and `00317DE0` takes both it and `00337700` by `lea`. That is DE-4's (ANSWERED) wander-position validator: "each validated by `00317DE0` (`00337700` / `003377C0` by `param != 0`)" (F19). The row should cite DE-4 and the other callers, and ask what the shared position test accepts. That gives what a drop at that position is refused for. |

**Register hygiene (correction C5).** Rows GR-3 and GR-8 carry the draft placeholders `FD-n401` and `FD-n601` in their
page cells (F0). The pages carry none.

## 3. Notes

- **N3, the record.** The README describes batch A only: 8 pages, the 8 rows of `new_rows.tsv`, "this pass does not
  edit the register". It lists `apply.py`, `drafts/*.edits.md`, `consumer-check.md` and `ids.tsv`, and none of them is
  in the installed folder. Batch B (7 pages, GR-9..GR-19) has only `consumer-check-0930-dd7.md`. The pages cite five
  scripts whose outputs are not committed (`adr_tally`, `rwr_recipes`, `rwr_slots`, `wsn_lists`,
  `record_flag_or_sites`). Add a batch-B paragraph, correct the file table, and commit the outputs; this review's
  re-runs can be used.
- **N4, gambit page §8l.** The unstruck lead sentence still says the code "copies **512 bytes** (`edx = 4` iterations
  of `0x80`)", next to the correction's (right) `0x208` bytes "four `0x80` blocks and a trailing qword". Strike or
  amend the lead.
- **N5, action row page §2.2.** Both `+0x1C` ("the action category 0–9", the presentation-event index) and `+0x1E`
  ("the category", the id-class selector) are now called "the category". Qualify one of them.
- The routed consumers in both consumer checks were spot-read, not re-derived. They are the owners' to adopt:
  - the stat contract's L61;
  - the foe cap `0x3B9ACA00`;
  - the actor-storage page's kind 7;
  - the field map's `00321810`;
  - AB-8 and counter 17.

## 4. Corrections routed

To FABLE (the pages' and the GR rows' owner), as `AUDITSEM-REQ-FABLE-DD-GAMEPLAY-ROWS-0930`:
- **C1: GR-12, the second question.**
- **C2: GR-7's "who", which is also routed to OPUS, the holder.**
- **C3: GR-2, citing and narrowing by SD-160's census.**
- **C4: GR-19, citing DE-4 and the shared callers.**
- **C5: remove the placeholders from GR-3 / GR-8.**
- **Notes N1 to N5.**

This review changes no page or register row.
