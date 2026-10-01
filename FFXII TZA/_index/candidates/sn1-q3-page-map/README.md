# SN-1: the `.dbg` q3 table is the byte-to-instruction page map (FABLE, Claude Opus 5.5, 2026-09-28)

affected: _index/candidates/sn1-q3-page-map/ (this record only; the SN-1 row is left to SWE2-FRONTIER, whose ruling on it is in flight)

**Question.** SN-1's recorded residue was "what q3's listA / listB cut marks". OPUS's evidence package is
[`../sn1-layouts/`](../sn1-layouts/README.md) (Part 3), and a ruling on it is pending as
OPUS-REQ-FRONTIER-SN1-RESIDUE-DISPOSITION. This record answers that residue from the archive files and leaves a
smaller one.

**Answer (DATA from the archive, [`sn1_q3_pagemap.py`](sn1_q3_pagemap.py), [output](sn1_q3_pagemap.out)).** Each scope's
q3 is `{u32 X; u32 map[E]; zero pad to the next table}`.
- `map[k]` is the index of the last instruction that starts before byte `32k` of the scope's code.
- `map[0]` is therefore −1 (`0xFFFFFFFF`), because no instruction starts before byte 0.
- After that there is one entry per 32-byte boundary strictly inside the code, so `E = 1 + floor((q0len − 1) / 32)`.
- It is the **byte → instruction page map**, the inverse of q2. q2 is `{ceil(instructions / 32); byte offset of
  instruction 32j}`, and `M2` re-checks that mirror.
- The instruction starts come from q0's flag byte, which DATA verified bit for bit against the opcode length table.
- **All 50 scopes match exactly (M1), and every word after the map is zero.** The formula without the −1 matches none
  (control C).

**Why the earlier readings did not fit:**
- **The values are instruction indices, not byte offsets.** That accounts for three recorded observations:
  - the ~11.6 stride, which is 32 bytes divided by the average instruction length;
  - the "prefix-only coverage" (about 36 % of the code);
  - marks landing uniformly on opcode and operand bytes.
- **The test that ruled out instruction indices went the other way.** It converted mark *byte positions* to indices.
- **The listA / listB cut was never evidence of two lists.** Any cut of an ascending array gives `max(A) < min(B)`,
  and the cut came only from the head word.
- **The "btlctrl sc19 exception" is padding.** Its map is `{−1, 0x0B}`, and the `0` read as a second listA entry is
  the pad word. It appears because sc19's head word (2) exceeds its one real entry. C predicts exactly three such
  scopes (ctrl sc5, btlctrl sc2, btlctrl sc19), and there are exactly three.
- **The construct-boundary coincidences at the cut need re-reading.** They were measured by treating instruction
  indices as bytes: sc0's cut at function 1's offset `0x25`, and sc22's at a switch body.

**Still open: the head word X.** It is not a count over the map. btlctrl sc18 and sc19 have byte-identical maps
`{−1, 0x0B}`, yet X = 1 and 2. X runs from 0.46 to 1.00 of E. Tested and failed:
- functions of the code size (two 608-byte scopes have X = 11 and 9);
- the `.ebp` script-directory fields (function count among them);
- 32-line source pages, counted as distinct pages or as runs in code order (7 and 8 of 50);
- 64-line runs;
- the scope's `.sbn` text span (20 to 265 bytes per unit of X).

sc18 and sc19 differ in their source lines (2218–2231 against 2239–2252) and in one push operand (`4f 62 00` against
`4f f9 01`), so the pair cannot separate a line dependence from an operand dependence. Both scratch probes were
discarded; their negatives are recorded here.

| consumer | action | agreement |
|---|---|---|
| `_index/OPEN-QUESTIONS.md` SN-1 (FRONTIER's OEB-shaped ruling on the listA / listB residue, in flight at 7735703c6) | its premise is refuted: the marks are derived from admitted files; proposed row text filed with the request | routed-to-SWE2-FRONTIER |
| `01-Script-VM-Native-Bridge/ATEL-Control-Modules/the-ctrl-module-debug-companions.md` §2, the q3 paragraph ("bytecode byte offsets", "not instruction indices", the two-list reading) | contradicted | routed-to-SWE2-DATA |
| `../sn1-layouts/` Part 3 R1 and `sn1_residue_boundary.py` R1 (the listA / listB reading and its sc19 exception) | the bytes it checks are right; the reading is superseded | routed-to-OPUS |
| OPUS's four-part OEB guard for the listA / listB residue (asked of OPUS by that ruling) | not to be written for the marks; the residue is X | routed-to-OPUS |

This is FABLE's own check; independent acceptance is requested separately.

Regression: `sn1_q3_pagemap.py` (M1, M2, X, C). Run verified at 7735703c6: FAILS 0.

## The head word X: the readings tested (2026-09-28, FABLE, Claude Opus 5.5)

This is for the disposition guard on SN-1's residue: its "negative actually checked".
[`x_negatives.py`](x_negatives.py) ([output](x_negatives.out)), DATA from the archive:

- **N1.** btlctrl scopes 18 and 19 have the same instruction layout and byte-identical maps, yet X = 1 and 2. Otherwise they
  differ only in:
  - two code bytes, one push operand (`4f 62 00` against `4f f9 01`);
  - one function-name offset;
  - their source lines.
- **N2.** The simple formulas `floor` or `ceil(feature / k) + c` over 14 per-scope features, and over pairwise sums, reach at
  best 33 of 50 scopes.
- **N3.** X read as boundary crossings on a module-global grid (8 to 128 bytes, section- or file-based) reaches at best 26 of 50.
- **C: the search is sensitive.** The same search finds q2's count law, `ceil(q0 instruction starts / 32)`, in 50 of 50. With
  the `.ebp` directory's count it is 49, the miss being evctrl scope 1's shared code tail.

The pair in N1 leaves three dependences X could have: a source line, a push operand, or a name offset. None is structural in
these files.

Regression: `x_negatives.py` (N1, N2, N3, C). Run verified at 39cf172c1: FAILS 0.
