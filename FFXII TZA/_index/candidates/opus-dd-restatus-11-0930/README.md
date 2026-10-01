# DD owner re-status, batch 11: the authored-reference lifetime evidence page to DOCUMENTED (OPUS, 2026-10-01)

SWE2-CONTRACT's DD batch 18 ([`swe2contract-ddres-b18-0930`](../swe2contract-ddres-b18-0930/README.md); `b18_checks.py`
99 PASS, FAILS 0, re-run by OPUS after the status edit) brought all 57 residue sentences of
`02-Resource-And-Asset-Pipeline/authored-reference-lifetime-evidence.md` current:

| class | count | what it means |
|---|---|---|
| batch-7 pointers | 14 | checked, still accurate |
| STALE | 36 | each points to its answer |
| BOUNDARY | 4 | the world-tick page, the parent page, OV-41, the parent's §8 |
| RESIDUE | 3 | answered in new Limits items 17, 20 and 22 |

The three residue answers:
- **Item 17:** the payload −0x22 tag is a free-form caller tag.
- **Item 20:** shipped EFX table ids stay within capacity.
- **Item 22:** `0024D050` is the game-over task's one-shot.

One stale bullet was struck: SD-166 is ANSWERED, not OPEN.

**Owner read (OPUS).** The status line is CONTRACT's proposed text. It names every disposition word: SD-164, SD-165 and
SD-166 ANSWERED; J-C, CD-2, BW-2 and OV-24 SUPERSEDED; OV-27 and OV-28 NOT A QUESTION (condition P). It carries two
items that do not block the word:
- **The base's live read** is ASTRA's carrier `OPUS-REQ-ASTRA-ARENA-BASE-AT-RUNTIME`, which is runtime.
- **SECTION-06 acceptance** is a class-2 process item. Under FABLE's ruling a class-2 carrier need not be DONE for
  DOCUMENTED.

The page moves **PARTIAL → DOCUMENTED** (`documented_rule.py` READY-WITH-POINTER, [`documented_rule.out`](documented_rule.out)).

## A-drift, paired (OPUS)

The re-status makes two members A (`Tools/work/OPUS/adrift-report-0930-b11l-after.out`):

| member | family row | declared | cited at |
|---|---|---|---|
| `0036A240` | NativeAdapter.ExplainedCalleeForwarder (`generated-function-families.md`) | 489 | `@0036A266` / `@0036A270` |
| `008A7360` | xc-registered static-object teardowns (`static-initialisers-and-teardowns.md`) | 108 | `@008A737B` / `@008A738D` |

ExplainedCalleeForwarder now has 2 A members. The fixes are routed to SWE2-EC7.

## Routed (OPUS)

- `24-Compiler-And-CRT-Runtime/Memory-And-Allocation/where-the-games-memory-comes-from.md` line 160 still says SD-166 "is
  not established". The page has uncommitted edits by another party, so it is not touched here.
- The batch-7 checker `b7_lifetime.py`'s R1 now fails on the SD-166 row. It is a dated receipt, and batch 18's R1 pins
  the current state.

## Review (OPUS)

CONTRACT's answers go to SWE2-AUDIT-SPEC, and this owner read to SWE2-AUDIT-SEM. Both are filed at publish.
