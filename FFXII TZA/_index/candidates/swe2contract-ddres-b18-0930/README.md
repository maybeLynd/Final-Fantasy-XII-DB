# DD residue closure, batch 18: the lifetime evidence note brought current (SWE2-CONTRACT for OPUS, 2026-10-01)

Request: `OPUS-REQ-CONTRACT-DD-RESIDUE-CLOSURE-0929`, batch 18. A Claude session ran the batch in the SWE2-CONTRACT lane,
started by OPUS. It used no subagents, no board operations and no commits.

One page: `02-Resource-And-Asset-Pipeline/authored-reference-lifetime-evidence.md`, the evidence note batch 7 regrouped
under a Limits section. It was clean at HEAD before the edit (`git status --short` empty) and is LF-only. Every line
keeps its LF ending (`git diff --numstat`: 122 added, 46 removed; the 46 removed lines are the 44 lines that gained a
pointer note and the two lines of Limits item 7 that are now struck). No status word was moved. One statement is struck
with a *Corrected 2026-10-01 (SWE2-CONTRACT for OPUS, DD batch 18)* note; see [`consumer-check.md`](consumer-check.md).

The brief estimated about 31 open-residue sentences. A full read of sections 1–20 found **57** that say "remains open",
"not established", "unresolved", "pending" or "next bounded review". Fourteen already carried a batch-7 Limits pointer;
the other 43 now carry a dated note *(2026-10-01, SWE2-CONTRACT for OPUS, DD batch 18: …)*. The Limits section gained a
note on item 3, a correction on item 7, and items 17–23.

Legend, as in batches 13 and 15: **STALE** = already answered elsewhere, now pointed to. **BOUNDARY** = another page
owns the fact. **RESIDUE, answered** = open and in scope, answered here with a pinned check.

| disposition | count | sentences |
|---|---:|---|
| RESIDUE, answered | 3 | §2 the prefix tag's name (Limits 17); §14 the table ids' admission bounds (Limits 20); §16 `0024D050`'s call frequency and effects (Limits 22) |
| BOUNDARY | 4 | §10 `002628B0`'s callees and scheduling (world-tick page, Limits 19); §13 the fallback `003EE2D0` (parent page, Limits 21); §14 `+0x282` against the element types (FABLE's OV-41 record, Limits 21); §20 the descriptor's last four bytes (parent §8) |
| STALE, new pointer | 36 | placement (§11, Limits 2), the base (Limits 3), the map (Limits 4), arena 11's replacement (FABLE's arena-residue record, Limits 18), sections answered later on the page (§14–§19), and the 28 review and correction requests now DONE on the board (Limits 23) |
| STALE, batch-7 pointer verified current | 14 | items 2–16 as cited; item 7's target changed, see below |

## The answers (SWE2-CONTRACT for OPUS)

| Limits item | disposition | answer | checks |
|---|---|---|---|
| 17 | RESIDUE, answered | The field at payload −0x22 (header `+0x1E`) is a **free-form 16-bit caller tag**. Both taggers (`0036C660`, `0036C6C0`) store the low 16 bits of argument 3 there. Of `0036C660`'s 63 call sites, 25 pass a constant with a source basename (`0xF3`–`0x16E6`), 13 pass zero with a label, 3 pass a size with a label (`EVTMEM` `0x100000` stores 0) and 22 pass a register value. In the arena code it is read only to be copied into a rebuilt header (four reads), plus one zero test in the report `0036A570` that decides whether to print the name. The free clears it. "Line number" fits the 25 basename callers only | T1–T5 |
| 18 | STALE (FABLE's arena-residue record T), re-pinned | `0037B3D0` reports arena 11, disables it, frees the old backing `01FD4A18` through `0036D250` → `0019C590` → IAT `008C2B48` (`free`), then allocates and re-initialises | A1–A3 |
| 19 | BOUNDARY (world-tick page §3, EX-9 ANSWERED) | `002628B0` has two direct callers, the manager-request drain `0025BFB0` and `0032FCA0`. The drain's one caller is the simulation tick `00314020`, before its first mode test | U1–U3 |
| 20 | RESIDUE, answered | Capacities 320 (`0x800`, `003A9560`) and 768 (`0xA00`, `003A9920`). Over all 4,229 shipped EFX streams (53,351 and 48,868 chunks, the published counts), the largest ids are 296 and 722. No chunk uses id 0 (the slot teardown and rebase skip), and no id repeats in a stream | B1–B5 |
| 21 | BOUNDARY (FABLE's OV-41 record; the parent page) | `+0x282` is the `0x800` family's own subtype byte (chunk `+0xE`, copied at `003A974F`), not the `0xA00` element type (`+0x44`); shipped values stay in 0–8. `003EE2D0` is read on the parent | B2, B6, P1 |
| 22 | RESIDUE, answered at the call level | `0024D050`'s one caller is the game-over widget's task `003EF2E0`, which runs it once when its countdown `+0xC8` reaches zero. Its per-instance callees call no release front, so the traversal frees nothing | G1–G5 |
| 23 | STALE (board) | The 28 review and correction requests sections 6–19 route are DONE. Still open on the board: item 1's SECTION-06 acceptance (READY) and item 3's base read (BLOCKED) | Q1 |
| 7 | STALE, corrected | SD-166 is ANSWERED at HEAD (restated by SWE2-DATA, `06c849caf`). The bullet saying it still read OPEN is struck | R1, Z1 |

## The answers, in player terms (SWE2-CONTRACT for OPUS)

- **Debug labels on memory blocks.** Every labelled block of game memory carries a seven-letter name and a small
  number. The number is whatever the code that asked for the block chose to put there: often a source-line number,
  sometimes a size or an id. The game never acts on it; it only shows up in the memory report.
- **Resizing arena 11.** When the game switches arena 11 between its two sizes, it reports what was still in the old
  block, throws the whole block away and makes a new one. Nothing is carried across.
- **Effect files never overfill their tables.** Every shipped effect file numbers its pieces within the space the game
  sets aside, never uses piece 0 and never uses a number twice. Only a modded file could break that.
- **The game-over screen** runs one extra pass over the playing effects, once, when its timer runs out. That pass
  clears their sub-slots and frees no memory.

## What the evidence rests on, and its limits (SWE2-CONTRACT for OPUS)

- **T3's read census** covers the arena code range `00369000..0036E000` and register-plus-displacement forms. **T4's
  image-wide census** is a word-width `[reg - 0x22]` pattern over the listed bodies. A read through another base, or a
  block copy of the header, is not seen.
- **T2's classes** come from the argument setup within 25 instructions before each call. "Basename" means a call to
  `0036C750` within the last 12 instructions and `rdx` = `rbx`.
- **B4–B6** walk the extract `D:/FFXII_TZA_extract` with `type_census.py`'s stream walker; the published chunk counts
  are the positive control. Each EFX stream is taken as one context, which is how the constructor and the EFB wrapper
  build them (§14, §16).
- **G4** checks direct calls only, one level deep. Deeper callees are named call boundaries.
- **Q1** reads `TEAM.json` only; it pins DONE states, which do not move back. The two open items are printed, not
  pinned.
- **Batch 7's receipt** (`../swe2contract-ddres-b7-0930/b7_lifetime.out`) pinned SD-166 OPEN. Rerun at HEAD, its R1
  fails on that one row, by design: the row moved. b18 R1 pins the row's current state. The batch-7 record is not
  edited.

## Receipts (SWE2-CONTRACT for OPUS)

Static work on the certified shipping image (`73461d08…`) through `retool.py`; the game extract `D:/FFXII_TZA_extract`
(every `.efx` / `.efb` and the 531 embedded-stream files of `efx-embedded-stream-files.txt`); the register, the pages and
the records cited; `TEAM.json` read only.

| script | result |
|---|---|
| `b18_checks.py` (`b18_checks.out`) | T1–T5, A1–A3, U1–U3, B1–B6, G1–G5, S1, R1, Q1, P1, Z1–Z4: 99 PASS, FAILS 0 |
| `documented_rule.py` (`documented_rule.out`) | `READY` (boxes 0, no live id, no unknown id), `TALLY READY=1 of 1`, FAILS 0 |

run: _index/candidates/swe2contract-ddres-b18-0930/b18_checks.py at b0e414d9d (FAILS 0)

Positive controls in the checker: §2's known tag `0x95C` at `003303A4`; the frame pointer of the one stack hit
(`0041888C`); the chunk counts 53,351 / 48,868 that `type_census.py` publishes; the IAT name from
`iat-any-reference.tsv`; the game-over ids of batch 15's P1.

## documented_rule verdict (SWE2-CONTRACT for OPUS)

**READY**, before and after this batch. SD-166's move to ANSWERED already cleared the one live id that batch 7 recorded.
This batch adds no box and no live or unknown register id: the notes name SD-166, OV-41 and EX-9 (all ANSWERED), J-C,
CD-2 and BW-2 (SUPERSEDED), and board ids, which the rule does not read as register ids.

## Proposed status line (SWE2-CONTRACT for OPUS)

No status word is moved. FABLE's ruling says a class-2 carrier need not be DONE for DOCUMENTED, so for OPUS's owner read:

`status: "DOCUMENTED — evidence note for the ownership-to-disposal page; its residue is consolidated under Limits (2026-09-30, SWE2-CONTRACT, DD batch 7; brought current 2026-10-01, DD batch 18, items 17–23): each item is answered by a cited record or check, owned by a named page, or carried by a closed register row (SD-164, SD-165 and SD-166 ANSWERED; J-C, CD-2, BW-2 and OV-24 SUPERSEDED; OV-27 and OV-28 NOT A QUESTION); the base's live read is ASTRA's carrier OPUS-REQ-ASTRA-ARENA-BASE-AT-RUNTIME, and SECTION-06 package acceptance is a class-2 process item carried by board request SWE2CONTRACT-REQ-AUDITSPEC-SECTION06-ACCEPT-0930."`

## Proposed rows (SWE2-CONTRACT for OPUS)

**None.** No sentence needed a new register row:
- The one runtime question left, whether anything outside the image writes the base `01F83530`, already has ASTRA's
  carrier `OPUS-REQ-ASTRA-ARENA-BASE-AT-RUNTIME` (BLOCKED, parked live-only in ASTRA's queue) behind the SUPERSEDED row
  CD-2. Limits item 3 now says so.
- "Actual scheduling" (§10, §15–§18) is answered at the call level (items 13, 19 and 22). How often an area change or a
  game over happens is a property of play, and the whole-schedule claim is OV-24's declared limit.
- Which context produced EXP-079's arena-7 bytes stays out of scope (item 10): it is a property of one past sample.

## Routed, not edited (SWE2-CONTRACT for OPUS)

- **The page's own status line** still says arena 7's row is open. It is untouched; the proposed line above replaces it.
- **The arena page** (`where-the-games-memory-comes-from.md`, line 160) still reads "is not established (`SD-166`, …)".
  The row is ANSWERED. That page is FABLE's; it is listed in `consumer-check.md`, not edited.
- **`CONTRACT-resource-request-queue.md`** has someone else's uncommitted change in the shared tree. It was not touched.
