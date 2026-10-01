# Consumer check: falsification pass 1 on CONTRACT-authored-expression-evaluation (OPUS, 2026-09-29)

corrects: 02-Resource-And-Asset-Pipeline/Authored-Expressions/CONTRACT-authored-expression-evaluation.md (I2's draw column holds only for b != 0; I4 scoped; §3 sixteen bytes read; §5 cells named)
corrects: 02-Resource-And-Asset-Pipeline/Authored-Expressions/how-an-authored-number-gets-its-randomness.md (the "first fifteen bytes" sentence)

## What was corrected

- **I2's draw column.** `00431350` tests `b` before dispatching. With `b == 0`:
  - ops 0-4 return `a` without calling `f`;
  - op 5 draws `f(−a)` only when `a ≠ 0`.

  The contract's table gave ops 1-4 one draw each, unconditionally. The page already had it right. `CON-162`.
- **I4, scoped.** From this evaluator a zero bound reaches `f` only through op 3 with `b = 0x80000000`, where `2b` wraps.
  The seven-step cost stays true of `f` itself.
- **"The first fifteen bytes."** The operator is loaded as a `u16` at `+0x0E`, so sixteen bytes are read, and fifteen decide
  anything. Both the contract and the page carried the sentence, and both are qualified.
- **§5, named.** The "scratch" is the VU0 register bank: ACC (`022D91A0`), vf20 (`022D92E0`) and vf21 (`022D92F0`). The
  `1.0f` is vf00.w (`01EF93FC`), and its two writers store the `.rdata` 1.0.
- **What survives.** Checks A0-A2 and A5-A7: sizes, the tail call, the leaf, the operand kinds, the six arms for `b ≠ 0`,
  seven steps with the first store after five, the mode gate, the arithmetic order and the six writes.

## Current consumers

- consumer: [how-an-authored-number-gets-its-randomness.md](../../../02-Resource-And-Asset-Pipeline/Authored-Expressions/how-an-authored-number-gets-its-randomness.md):
  revised-here, for the byte count. Its zero-`b` section and its `b == 0` checkbox already agree with `CON-162`.
- consumer: `_index/CONTRADICTIONS.tsv`: revised-here (`CON-162`).
- consumer: [EXP-070](../../../_experiments/EXP-070-procedural-rng-controls.md) agrees. It executed `f` in isolation, where a zero
  bound costs seven steps. That is I4 as scoped here.
- consumer: the shared transform workbench's register census (`00-Engine-Core-Runtime/Shared-Transform-Workbench/members/ee-register-census.tsv`)
  agrees. It already lists `003A6E60` among the bank's users.

## Regression

regression: `Database/Tools/analysis-kit/gfz-scripts/falsify_authored_expression.py`, checks A0-A7.
- A3 fails if the zero-`b` path gains an `f` call or loses its op-5 branch, which rejects the unconditional draw column.
- A5 fails if vf00.w gains a writer that stores anything but 1.0.

run: verified at 11e788a3b (BROKEN 0), against the certified image `73461d08…`.
