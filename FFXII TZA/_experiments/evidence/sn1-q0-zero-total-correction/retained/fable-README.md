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
| `the-ctrl-module-debug-companions.md` line 217, "+ 0–2 trailing `(line 0, block 0, flag 0)` end marks" | 0 to 3 observed | routed-to-SWE2-DATA |
| the same page, line 732, "`pos` is the 0-based source line number" | six records past the block under either convention; nine fit only 1-based; cause unknown | routed-to-SWE2-DATA |

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
