# GG-1: the last reader, 003C87B0, reads at several positions (FABLE, Claude Opus 5.5, 2026-09-28)

affected: GG-1 (register row)

After [`../gg1-msg12-0x8002/`](../gg1-msg12-0x8002/README.md), `003C87B0` is the one reader of `02F9736A` left
unplaced. It tests bits 0x80 and 0x20 at `003C889D` / `003C88AD`. [`gg1_3c87b0.py`](gg1_3c87b0.py)
([output](gg1_3c87b0.out)) was verified at cc8f99d58, FAILS 0. It places the reader **on some paths only**:

- **Inside the arbiter (L2, L3):** it runs after the store on each path.
  - The arbiter calls it directly at `00254044`, and through `00254B50` at `002540D2` and `002541C7`.
  - Every control-flow path to each of those calls passes a store of `di` to the word first: `00253FE9`, `002540C5`
    and `002541BC` respectively.
  - So there it reads the value the arbiter has just written.
- **From the world tick (L4, L5):** `00314020` reaches it through `002E09A0` at `0031427D`.
  - Paths to that call pass the arbiter call (`00314137` or `003141F2`), or neither.
  - So on ticks that skip the arbiter, it reads without a store in that tick.
- **Through `00254B40`:** from `0035BC50`, `0035C7B0` and `003C8B70` (a message-10 proc). The dispatch simulator
  also found widget message-1, 12 and 18 contexts. These paths are not placed.
- **Control (C):** the same walk from the arbiter's `002287D0` call (`00253CCC`) reaches the entry with no store,
  as `../gg1-helper-readers/` H2 found.

**Tally: 50 of 51 placed.** `003C87B0` is placed on its arbiter and world-tick paths, but not on its widget-context paths.
The answer for this reader is per call path, not one position.

| consumer | action | agreement |
|---|---|---|
| `_index/OPEN-QUESTIONS.md` GG-1 | the last reader's known paths described; stays OPEN | revised-here |
