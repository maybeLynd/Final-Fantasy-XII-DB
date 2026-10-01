# Consumer check: falsification pass 1 on the-unit-shape-distance-primitives (OPUS, 2026-09-29)

corrects: 06-Movement-And-Navigation/the-unit-shape-distance-primitives.md (the D4B0 planter; the "zero inbound references" audit; "callers" read as call sites)

## What was corrected

- **The D4B0 planter.** F430 does not take D4B0's address. Its caller `002315E0` does (`lea` at `0023160E`), stores it in
  its stack context, and calls F430, which invokes the callback.
- **The "dead" siblings are planted callbacks.**
  - `0022D7E0`'s address is taken by `lea` in `00231690` (reached from `0032BCC0`, `0032CA70`) and in `002327D0` (from
    `00380C40`).
  - `0022DE60`'s is taken in `00230C10` (from `00230C00`).
  - `00230790` and `0022E7D0` are called by `0022D7E0`, and `003810B0` by both.

  So "zero inbound references of any kind - no `lea`" is false, and "dead code" is excluded. They are runtime-dispatched,
  the page's other alternative.
- **Wording.** "15-86 callers" holds as call sites (86, 16, 81, 15), the same counts EXP-139 prints. As calling functions
  the range is 43, 11, 52 and 10.

## Current consumers

- consumer: [EXP-139](../../../_experiments/EXP-139-nav-region-query-exec.md): routed-to-OPUS-NOTICE-ORACLE-EXP139-LEA-PLANTS.
  Its post-scope audit says "no `lea`". It is an executed-experiment record in its author's lane, so it is not edited here.
- consumer: [how a unit finds its way across the navigation mesh](../../../06-Movement-And-Navigation/how-a-unit-finds-its-way-across-the-navigation-mesh.md)
  agrees. It cites neither D4B0 nor the five siblings, so it makes no claim either correction touches. The unit-shape page's
  pointer to it for "the executed wiring" rests on EXP-138, not on that page's text.

## Regression

regression: `Database/Tools/analysis-kit/gfz-scripts/falsify_unit_shape.py`, checks U0-U7.
- U5 fails if the three `lea` plants or the three direct calls disappear, which rejects "zero inbound references".
- U4 fails if F430 itself takes D4B0's address.

run: verified at f8605b36e (BROKEN 0), against the certified image `73461d08…`.
