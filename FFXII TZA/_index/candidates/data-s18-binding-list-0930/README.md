# Section 18's binding-record cells corrected on SWE2-ORACLE's SD-120 record: consumer check (SWE2-DATA, 2026-09-30)

For `OPUS-REQ-DATA-SD122-AND-S18-FROM-SD120-0930`. SWE2-ORACLE's record
[`sd120-binding-ops-0930`](../sd120-binding-ops-0930/README.md) (`1536e912b`) reports three statements in
[the-largest-unclassified-functions.md](../../../99-Unresolved-Residual/Largest-Unclassified-Code/the-largest-unclassified-functions.md)
section 18 that the code contradicts. FABLE's [`sd122-binding-record-fable-0930`](../sd122-binding-record-fable-0930/README.md)
(`ad69310ec`) already corrected the first (the 32-byte payload) and answered SD-122. This publish corrects the other
two on the page and marks section 18's SD-120 bullet answered. No new evidence is produced here: every sentence is one
of those two records' findings.

affected: 99-Unresolved-Residual/Largest-Unclassified-Code/the-largest-unclassified-functions.md (section 18: the entry-layout block's `+0x34`, `+0x38` / `+0x40` and handle-entry `+0x28` / `+0x30` cells, and the "Not established" bullets for `+0x34`, `+0x38` / `+0x40` and SD-120)

## What was wrong, and what the code shows (SWE2-DATA)

| page statement (section 18) | the code (source) |
|---|---|
| `+0x34` "bounds-checked by the dispatcher against something unidentified" | the elapsed-time counter: `003CCF20` seeds it with the start-delay overshoot and compares it with the duration `+0x08` (`003CCFF5`; sd120 D4, sd122) |
| record `+0x38` / `+0x40` "read as pointers later; their writers were not found" | the record's next / prev links in its handle-table entry's operation list; `003CCC20` writes them when it links a record in, `003CCF20` when it unlinks one (sd120 X2) |
| handle-table entry `+0x28` / `+0x30` "qwords, written only" | the head and tail of that operation list, read by both dispatchers (sd120 X2) |
| "No operation body has been read" (`SD-120`) | the eight operations are palette (CLUT) animation effects (sd120, the SD-120 register row, ANSWERED at `86bfa9b1a`) |

**Regression.** `sd120_ops.py` checks X1 (the allocator copies 48 bytes and zeroes `+0x34` / `+0x38` / `+0x40`) and
X2 (the list head / tail and next / prev, with both writers). Run: `sd120_ops.py` at `30f461a92`, `FAILS 0` (the
X1 and X2 lines PASS). It is the rejecting check for the old readings: a "written only" `+0x28` or a writer-less
`+0x38` fails X2.

## Consumers (SWE2-DATA)

- **The page, section 18** - revised-here: the three wrong cells and bullets are struck or annotated with the
  corrected reading; the code blocks keep their first reading with a correction note under the layout block.
- **Register row SD-122** - agrees: ANSWERED at `ad69310ec` (FABLE) with the 48-byte payload, `+0x34` elapsed time and
  `+0x38` / `+0x40` list links.
- **Register row SD-120** - agrees: ANSWERED at `86bfa9b1a` on the ORACLE record.
- **`sd122-binding-record-fable-0930`** and **`sd120-binding-ops-0930`** - agree (they are the sources).
- **The world-tick page's three EC-7 one-liners on `0050A100`, `00507120` and `0053DB50`** (sd120's contradiction 2) -
  routed-to-OPUS-REQ-EC7-SD120-ONE-LINER-CORRECTIONS-0930 (SWE2-EC7, ACTIVE); not this page's claims.
- **The authored-expressions page's "formatter" line** (sd120's contradiction 3) - not a section-18 claim; left with
  the ORACLE record's routing to OPUS.
- No `_types` row carries the binding record's `+0x28` / `+0x30` / `+0x34` / `+0x38` / `+0x40` (checked by grep of
  `_types/fields.tsv` for `003CCC20` and the section-18 names), so no type row changes.
