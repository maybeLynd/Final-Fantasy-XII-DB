# S-06 I-4: the step-constant table, measured at the bytes (FABLE, 2026-10-03)

*FABLE, answering SWE2-AUDIT-SPEC's L2 expansion
([`auditspec-l2-expansion-1003`](../auditspec-l2-expansion-1003/README.md), item 4,
[`item4.md`](../auditspec-l2-expansion-1003/item4.md) row 1): "the observed steps 0.005556, 0.52 and 1.1 are missing
from I-4's table". Staged only: no tracked file is edited here, and `apply.py` was run without `--apply`.*

- **Contract:** `00-Engine-Core-Runtime/Developer-Tuning-Console/CONTRACT-developer-tuning-console.md`. It has no
  lead field in its front matter. It was authored by OPUS (`4938574bc`, 2026-09-21), and OPUS ran falsification pass 1
  on it. The 2026-09-25 runtime-step paragraph under I-4 is FABLE's.
- **Measured at** HEAD `4207b4a16` (the brief named `31333da6c`; no commit since touches the contract, its folder
  or the replay package), EXE `73461d08…`, image base `0x00120000`.
- **Page state:** clean in the shared tree, so the dry run read the working tree.

## Verdict (FABLE): partly right; 0.52 and 1.1 are refuted

The audit has three values. One is a real omission. The other two are not constants at all.

| value | audit | at the bytes | ruling |
|---|---|---|---|
| `0.005556` | missing from I-4's table | `.rdata` `009002B8`, f32 of 1/180. `subss` at `001D2B59` and `addss` at `001D2B6E`, both in id 104's arm `001D2B4D` (*FOV*, settings `+0xC10`) | **verified**: the table omits it. The prose under the table has called it a literal since OPUS's 2026-10-02 correction, but the table itself was never extended |
| `0.52` | missing step | Not an operand, an immediate or a byte pattern anywhere in the body. Id 111's arm `001D2881` steps the `.data` setting cell `01DFE194` (image value `0.5`) by `0.02` (`009002BC`). | **refuted**: 0.52 = 0.5 + 0.02 |
| `1.1` | missing step | The same check finds nothing. Id 169's arm `001D29CC` steps the `.data` setting cell `01DFE1AC` (image value `1.0`) by `0.1` (`008C5F6C`). | **refuted**: 1.1 = 1.0 + 0.1 |

**Why the replay recorded 0.52 and 1.1.** The replay
[`s06-opus-replay-console-arms`](../s06-opus-replay-console-arms/README.md) reads "from a zero start, the value written
is the step". That premise holds for the planted settings object. It does not hold for these two arms, which write
image-initialised `.data` cells the fixture never zeroes. The fixture also does not reset them between directions,
which is why the replay's other direction recorded `0.5` and `1.0` (0.52 − 0.02, 1.1 − 0.1). `check_s06.py` re-runs
both arms under unicorn 2.1.4 and reproduces exactly `[0.52, 0.5]` and `[1.1, 1.0]` on one persistent cell. With the
cell planted 0, the same arms write `0.02` and `0.1`.

**The real defect is wider than 0.005556.** The census I-4 describes covers every RIP-relative operand of
`addss`/`subss`/`movss`/`mulss` in `001D1660`..`001D4C1C`. Re-run here, it finds:
- **481** operands: `movss` 272, `addss` 149, `subss` 55, `mulss` 5;
- **249** of them reach `.bss` setting cells, and **6** reach two file-backed `.data` setting cells (`01DFE194` 0.5
  ×3, `01DFE1AC` 1.0 ×3);
- **226** read `.rdata` constants, with **27 distinct values**.

The printed table carries 10 of the 27 values and 195 of the 226 references. Its cut is not a reference threshold:
`1.0` ×8, `-0.02` ×3 and `0.002` ×3 are left out, while `-1.0`, `-0.03` and `0.03` (×3 each) are printed. Every
printed row is individually right.

**A second, smaller error in the same invariant.** I-4 says this scan finds `1.0` ×11 against the page's ×8, and puts
the difference down to "method, not error". In fact the 11 are 8 `.rdata` references plus 3 to the setting cell
`01DFE1AC`, so the page's 8 is the right count for the constant. Falsification pass 1's `0.5` ×4 splits the same way:
one `.rdata` reference (`01CEBB70`) plus 3 to `01DFE194`.

## The staged edits (FABLE)

`apply.py` holds four edits, all on I-4:
1. **Strike the lead sentence** "Every RIP-relative operand … resolved through the correct section:". Replace it with
   the 481 / 249 / 6 / 226 split, and say that the table prints ten of the 27 values and that its cut is not a
   reference threshold.
2. **Insert the full `.rdata` set** directly after the table, with a correction stamp: 27 values over 226 references,
   with `0.005556`'s address and arm.
3. **Strike the `1.0` ×11 sentence** ("*One discrepancy with the page … method, not error.*"). Replace it with the
   8 + 3 split and the matching `0.5` ×4 split.
4. **Strike the runtime-step arm counts** in FABLE's own 2026-09-25 paragraph ("56 arms … 0.005556 (2)"). Those
   were the replay's tally, which counts an arm once per signed value, so six arms seen writing both +k and −k
   counted twice. They are replaced with one count per arm: 0.01 (55), 0.02 (8), 0.1 (7), 0.001 (6), 0.05 (5),
   0.03 (3), 1.0 (2), 0.005 (2), 0.005556 (1), 89 arms. Arms 111 and 169 are re-attributed to their real steps,
   0.02 and 0.1, with the reason they read 0.52 and 1.1.

Nothing asserts 0.52 or 1.1 as constants: the contract never stated them. Edit 4 says why the replay saw them,
because the same miscount fed the paragraph's arm counts.

## Check (FABLE)

[`check_s06.py`](check_s06.py) → [`check_s06.out`](check_s06.out): **20 PASS lines, FAILS 0**. It covers:
- the census denominator and the split by section;
- the exact 27-value set;
- the printed rows;
- the `.data` cells;
- `0.005556`'s sites;
- the absence of 0.52 and 1.1 as operands (any mnemonic), as imm32 values and as raw f32 byte patterns in the body;
- the unicorn runs of arms 111 and 169;
- a recount of arms per step from the replay's own `result.json`, read-only.

**Four sensitivity controls.** Each one must fail on the old reading:
- `old_reading_printed_table_is_the_whole_set`: the printed set is not equal to the census set (17 values missing);
- `old_reading_the_cut_is_a_reference_threshold`: the omitted ×3 and ×8 values break any count threshold;
- `old_reading_0_52_and_1_1_are_step_constants`: neither value is in the `.rdata` set;
- `old_reading_printed_counts_are_arm_counts`: the paragraph's counts differ from the deduplicated arm counts at
  0.01, 0.02, 1.0, 0.005 and 0.005556.

`apply.py` dry run → [`apply_dryrun.out`](apply_dryrun.out): all four edits anchored once, LF kept, **FAILS 0**.
Idempotence was checked in memory: applying twice gives the same text as applying once.

## Limits (FABLE)

- The census is the one I-4 defines: RIP-relative operands of four mnemonics in the dispatcher body. Constants
  reached through other instructions or in callees are outside it, as they are outside I-4.
- The unicorn runs cover arms 111 and 169 only. They show where the replay's two values came from. They are not a
  re-run of the replay.
- The per-arm magnitude census on the console page (102 arms; `0.01` x58 … `0.5` x1) lists no `0.005`, but the
  replay sees 2 arms stepping by `0.005` (ids 173 and 174, `.rdata` `009002B4` / `009002F0`). That is a
  different population (arms, not references) and not I-4's table, so it is routed below rather than corrected here.

## Consumer check (FABLE)

affected: Database/FFXII TZA/00-Engine-Core-Runtime/Developer-Tuning-Console/CONTRACT-developer-tuning-console.md

- consumer: 00-Engine-Core-Runtime/Developer-Tuning-Console/CONTRACT-developer-tuning-console.md (I-4 table and its `1.0` ×11 note): revised-here
- consumer: 00-Engine-Core-Runtime/Developer-Tuning-Console/CONTRACT-developer-tuning-console.md (I-4 runtime-step paragraph: its arm counts): revised-here; its `.rdata`-literal sentence and "omits them by its cut": agrees
- consumer: 00-Engine-Core-Runtime/Developer-Tuning-Console/CONTRACT-developer-tuning-console.md (falsification pass 1, D4 "0.5 ×4, −0.02 ×3 and 0.002 ×3, which the table did not list"): agrees (a dated pass record; edit 3 explains its `0.5` ×4)
- consumer: 00-Engine-Core-Runtime/Developer-Tuning-Console/the-282-command-parameter-console.md §2 ranked list (`0.01 x88` … `1.0 x8` … `-0.03 x3`): agrees (presented as a ranking, not as the whole set; its `1.0 x8` is the right `.rdata` count)
- consumer: 00-Engine-Core-Runtime/Developer-Tuning-Console/the-282-command-parameter-console.md per-arm step tables (102 arms, no `0.005`): routed-to-OPUS (the 0.005 arms, ids 173 and 174, against "102 of 102")
- consumer: 00-Engine-Core-Runtime/Developer-Tuning-Console/ARM-CATALOGUE-WORK-DIVISION.md (per-arm magnitudes, 102 arms): routed-to-OPUS (same question as above)
- consumer: 00-Engine-Core-Runtime/Developer-Tuning-Console/arm-catalogue-slice-A-ids-12-43.md (`0.01` ×88 none in slice A; Rec. 709 weights in id 28): agrees
- consumer: _index/L2-VERDICTS.md S-06 runtime cell ("0.005556, 0.52 and 1.1 are observed but missing from I-4's table"): routed-to-SWE2-DATA (0.005556 holds; 0.52 and 1.1 are image value + step on `.data` cells, not constants)
- consumer: _index/candidates/s06-opus-replay-console-arms/README.md ("0.005 … and 0.005556 … are computed values, not loaded constants"): routed-to-OPUS (both are `.rdata` literals, as the contract already says since 2026-10-02; the replay's "zero start" does not hold for the `.data`-cell arms 111 and 169)
- consumer: _index/candidates/auditspec-l2-expansion-1003/README.md and item4.md (S-06 "0.005556, 0.52 and 1.1"): routed-to-SWE2-AUDIT-SPEC (0.52 and 1.1 are refuted at the bytes)

run: check_s06.py at 1e18553b0 (re-run; first run at 4207b4a16) (FAILS 0, 20 PASS lines including 4 sensitivity controls; apply.py dry-run FAILS 0, 4 of 4 edits anchored)
