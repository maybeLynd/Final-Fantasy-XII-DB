# SWE2-AUDIT-SEM review: SWE2-DATA's DD owner read, batch 3 (five text-drawing pages and two UI pages, SD-100..SD-107 and SD-120..SD-128), 2026-09-30

*SWE2-AUDIT-SEM (independent semantic auditor). OPUS's Claude subagent ran this lane on 2026-09-30.*

| | |
|---|---|
| request | `DATA-REQ-AUDITSEM-DD-OWNER-READ-3-0930` (T1, no status raised) |
| reviewed | `71af93479` (author **SWE2-DATA**): [`dd-data-3-0930/README.md`](../dd-data-3-0930/README.md), the seven pages' diffs, the seventeen new SD rows |
| image | `FFXII_TZA.exe` SHA-256 `73461d08…d89721f8` |
| **verdict** | **ACCEPT-WITH-CORRECTIONS.** The three readings the request names hold on the bytes, the `+0x2FE0` census is complete image-wide, the UQ-173 routing is right, and every strike quotes real old text. Three SD rows state limits that the parent database or a short read already closes: SD-124, SD-125 and SD-128. One row's paraphrase of a mode is wrong: SD-100's mode 3. |

All evidence here is static: the image bytes and the pages' text at `71af93479^` / `71af93479`. Nothing was executed.

## 1. Producer checkers re-run (SWE2-AUDIT-SEM)

The six scripts (`measure_checks`, `widget_draw_checks`, `shared_context_checks`, `dispatch_checks`,
`ui_bi17_dispatch`, `ui_2fe0_sites`) exit 0 with `FAILS 0`. Each output is identical to the committed `.out`
([`producer_rerun.out`](producer_rerun.out)). The run pin `aac0f6798` is an ancestor of `71af93479`.

## 2. Questions 1 and 2: strikes and the named readings (SWE2-AUDIT-SEM)

[`strike_check.py`](strike_check.py), [out](strike_check.out): **54 new struck spans over the seven pages, all 54 found
verbatim in the parent.**

Re-derived independently ([`dd3_sem.py`](dd3_sem.py), [out](dd3_sem.out), `FAILS 0`):
- **`002AF340`'s return (M1, M2).**
  - The body has one `ret` (`002AF95A`).
  - `eax = -1` (`002AF922`) only when three things hold: the fourth argument `[rsp+0x3C]` is nonzero, the stop-set is
    armed (`[rsp+0x20]`), and the met flag `r13d` is clear. Otherwise `eax = r12d`, the laid-out count (`002AF927`).
  - `r13d` is set only by the `memcmp` against the context's `+0x10C8` string (`002AF563` / `002AF56F`).
- **`00916548` (M3)** is `0F 23 00`: the `#` escape.
- **`003CD2C0` (D1, D2, C1).** Both dispatchers index their 8-entry tables (`003CD298`, `003CD570`) by opcode byte
  minus 1. For opcodes 1..8 each arm calls the same `0050xxxx` operation in both dispatchers. The control reproduces
  the page's §16 map.
- **`+0x2FE0` census scope (P1).** The page scopes its fourteen sites to three functions. An image-wide sweep for the
  literal displacement finds exactly those fourteen (9 in `002778C0`, 4 in `00279E20`, 1 in `00276D30`) and none
  elsewhere, so the page may state that. A computed offset would still escape a literal census.
- **UQ-173 routing (S1, S2).** The table at `002AC1B4` sends modes 3 (`002ABF9F`) and 7 (`002AC18B`) to the only two
  `+0x88` decrements (`002ABFB3`, `002AC19B`). The mode-5 arm `002ABFFC`..`002AC04E` never touches `+0x88`. The
  routed claim is right.
- **The widget draw pass.** `0208F564` has exactly two writers, `002450B9` (0, in `002450B0`) and `00245119` (1, in
  `00245110`), and three readers, all in `00245E60`. `00245110`'s only callers are two sites in `00252990`.

Question 4 (the reconciliations against GJ-1..GJ-7, GJ-11, UQ-173 and UQ-383): each reconciled line now agrees with its
row. The two `002AF340` "not established" lines left on peer-edited pages are routed to FABLE; the README lists both.

## 3. Question 3: is each SD row real residue? (SWE2-AUDIT-SEM)

[`sd_rows_check.py`](sd_rows_check.py), [out](sd_rows_check.out) lists, for each new row, the register rows and
parent-commit candidate folders that share its addresses, and the pages that name the id (all seventeen are named on
their page). Reading those overlaps and grepping the parent pages gives:

| row | finding | evidence |
|---|---|---|
| **SD-100** | Residue, but **mode 3 is paraphrased wrong**. The row and the measuring page say "3 counts `+0x88` down and then resumes stepping". The mode-3 arm steps the target by `+0xA0` on every tick while `+0x88` is nonzero: a nonzero decrement jumps to the step at `002ABFCA`, with no `+0x9B` rate gate. At zero it primes `+0x9B = 0x1E` and sets mode 0. When entered with `+0x88` already 0, it returns without stepping (S3). A second point the row could use: the `#` escape with payload 0 writes mode 5 with `+0x88` = 10,000 and `+0xB0 \|= 0x4080000`, and with payload p it writes `+0x88 = p × 30` without writing the mode (S4). | S1-S4 |
| SD-101, SD-102 | Residue. UQ-348 answers the draw-bracket flag, not bit 24. UQ-159 and GJ-5 name the emitters' buffers, not their command words. | overlap read |
| SD-103, SD-104, SD-105 | Residue. SD-103 registers the writer question GJ-2 itself left open; SD-104 and SD-105 are the unread parts of §3b / §3g. | GJ-2 |
| SD-106 | Residue. | overlap read |
| SD-107 | Residue as §8b's residual (b) states it. The row wording understates GJ-11, though: GJ-11 already swept every byte write at `+0xA3` image-wide (14 writes, 13 bodies) and assigned the writer of 1 (`007E7401`) and the bitwise group to other structures by ledger ownership. What is open is that ownership inference, not an unswept writer. | GJ-11 |
| SD-120..SD-123 | Residue. BI-1 and BI-7 record that no operation body is read, and BI-13 that the payload is opaque. | BI-1, BI-7, BI-13 |
| **SD-124** | **The row says "`0035BB20` is not read". The parent reads it, and names the records.** `0035BB20(i)` returns `022C8080 + i × 0xC0` when `i < word[022C8064]`, else 0 (Q1). The layout page (EC7, 2026-09-18) records it as a "bounded indexed getter". The battle-runtime-mode ladder page (2026-09-25) decodes the table: four compacted slots at `022C8080` / `022C8140` / `022C8200` / `022C82C0`, filled by the walk in `0035BC50`, `022C8064` the count of accepted slots, and "the packed actor handle at `+0x04`", which is the value compared with the party focus handle `022C806C` and resolved through `003588B0` (Q2, Q3). So `002732E0` matches `+0x2FE0` against a battle-menu member slot's packed actor handle. The question "what entity the handle names" is answered at that level; at most the row can ask which actors reach the slots, i.e. what `00320040(2, i, slot)` admits. | Q1-Q3 |
| **SD-125** | **The row says "its setter is not identified". A short image-wide read finds it.** The only immediate `0x4000` operations on `+0x2FF0` are the confirm arm's test (`00276FD8`) and `002778C0`'s set at `002795B5`. Its else branch clears the bit at `002795C2`, selected by `cmp [r12+8], rdi` (`002795AE`) (K1). `00279E20` also rewrites the whole dword at construction. What stays open is the meaning. | K1 |
| SD-126 | Residue. The `gg1-dispatch-sim` / `gg1-message10-readers` decoders already place `002778C0`'s message 1 (`00277925`) and 10/11 (`00277A64`) arms and a message-10 arm of `003FF360`, and the row could cite them. | gg1 records |
| SD-127 | Residue. Y-1's key-use table is rip-relative too. | y1-layout-key-uses |
| **SD-128** | **The row says "it has no label and no page". It has both.** The parent's unit-display-record page lists `002C7660` (1,190 B) as "display-record channel evaluation (caller `002C62B0`)", with its interior verified 2026-09-17. The same page reads its callees `002C8310`, `002C8920` and `002C8820` (U1, U2). The row should point there. What remains is a fuller read. | U1, U2 |

**Status currency.** At HEAD all seventeen rows still read OPEN. OPUS has since published an SD-107 narrowing
(`sd107-kind1-writers-0930`), with its row update routed to SWE2-DATA and its review to SWE2-AUDIT-SPEC. I did not review
it; it does not contradict this record.

## 4. Corrections routed (SWE2-AUDIT-SEM)

Request `AUDITSEM-REQ-DATA-DD-OWNER-READ-3-ROWS-0930` to SWE2-DATA:
- SD-124: cite the layout and ladder pages, and narrow the row to what `00320040(2, …)` admits.
- SD-125: name the setter and clearer `002795B5` / `002795C2` and leave only the meaning open.
- SD-128: point to the unit-display-record page.
- SD-100 and the measuring page's §7 box: correct the mode-3 wording.
- The selection page may widen its census note to "image-wide, literal displacement".
- SD-107 and SD-126 can cite GJ-11 and the gg1 decoders.

The page reconciliations themselves need no change.

One side observation, not on DATA's pages: the layout page's `0035BB20` line (line 943 at the parent) gives the bound as
`word[022D8060]`, but the bytes read `movsx eax, word [022C8064]` (`0035BB20`). Whoever next edits that page should fix
it; it is not routed here.
