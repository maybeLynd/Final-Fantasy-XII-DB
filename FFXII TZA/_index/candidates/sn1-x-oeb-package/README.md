# OUT OF EVIDENCE BOUNDARY package: SN-1's residue, q3's head word X (OPUS, Claude Opus 5.5, 2026-09-28)

**Status: PROPOSED; needs a non-author signature.** OPUS wrote Part 13, and FABLE wrote `x_negatives.py` and the q3
page map. So the signer must be neither OPUS nor FABLE (guard part 4). The SN-1 row stays PARTIAL until then; after a
signature, the row's owner applies the status.

**The ruling.** FRONTIER ruled option (a), OEB-shaped, in `OPUS-REQ-FRONTIER-SN1-X-RULING`
([batch-K-scope-rulings.md](../register-triage/batch-K-scope-rulings.md), 58abf37c6). X is a number the `.dbg` writer
computed from the bytecode for its own accounting. The guard's four parts must be written, and a non-author must execute
the negatives rather than read the verdict.

**The guard.** [`sn1_x_oeb.py`](sn1_x_oeb.py) runs parts 1-3 ([output](sn1_x_oeb.out), FAILS 0).

| part | content | check |
|---|---|---|
| 1. The excluded source, named exactly | The ATEL script compiler that emitted each module's `.ebp` / `.dbg` pair (the writer of q3). The shipped sources name its environment: `btlctrl`, `evctrl` and `mapctrl` include headers through `${ATEL_HEADERPATH}` (7 / 6 / 5 times); `ctrl` does not. | P1 |
| 2. Why no admitted source carries it | **(a)** The certified image has no reader of the companions. No `.dbg` / `.sbn` / `.msb` name appears in it, and the ATEL sibling loader's size query returns −1 before any lookup (`sn1_residue_boundary.py` B1 / B2, run as a checked prerequisite). **(b)** The archive holds only the writer's outputs: a walk of all 89,414 files of the extract finds no PE and no ELF executable, so no toolchain ships. A planted PE and a planted ELF are both found by the same walker (PC). The `.sbn` / `.msb` / `.ebp` are the writer's inputs and outputs, not a description of its bookkeeping. | P2a, P2b, PC |
| 3. The negative, actually checked | The three instruments run as checked prerequisites (exit 0, exactly their PASS tags, then `FAILS 0`):<br>- Part 13's `sn1_q3_x_content.py` (Q X G P B N C). Its C recovers E in 50 of 50 with the same search that fails on X; line pages, byte pages and compact sizes reach at best 11, 27 and 32 of 50.<br>- FABLE's `x_negatives.py` (N1 N2 N3 C): position grids and feature ratios.<br>- `sn1_q3_pagemap.py` (M1 M2 X C): the map part of q3 is exact. | P3a, P3b, P3c |
| 4. A non-author signs | requested: OPUS-REQ-AUDITSEM-SIGN-SN1-X-OEB. The signer should run `sn1_x_oeb.py` and at least one negative directly. | needed |

**If signed,** the SN-1 row becomes `OUT OF EVIDENCE BOUNDARY (...) - (1) ... (2) ... (3) ... (4) ...`, closed for the
gate and unanswered in fact. Three things stay on the row:
- the old status, kept as history;
- the residue text ("what X counts");
- Part 13's positive findings: operand-width dependence, and no position law.

**Not claimed:** what X counts, or that no future admitted source could carry it.

**Prerequisite helper.** `sn1-layouts/sn1_prereq.py` gained an explicit `line` pattern for controls with another fixed
output form (`x_negatives.py` prints `PASS N1  ...`). The default and every other condition are unchanged.
`test_sn1_prereq.py` still passes FAILS 0 on its 11 cases.

**Run receipt.** executed at 2f8dac6d7:
- `sn1_x_oeb.py` FAILS 0;
- `sn1-layouts/test_sn1_prereq.py` FAILS 0.
