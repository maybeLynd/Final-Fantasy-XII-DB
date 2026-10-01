# GG-1: nine more readers placed through their callers (FABLE, Claude Opus 5.5, 2026-09-28)

affected: GG-1 (register row)

This builds on [`../gg1-static-order/`](../gg1-static-order/README.md), which gives the frame placement of widget
message-10 delivery, and [`../gg1-message10-readers/`](../gg1-message10-readers/README.md), which covers the 16 readers
that are themselves message-10 procs. It takes the readers that are not message procs and places them by who calls them.
[`gg1_helpers.py`](gg1_helpers.py) ([output](gg1_helpers.out)), run verified at a68a949c1, FAILS 0:

- **H1. Seven helpers are reached only from message-10 arms.** `00240DE0`, `002A5CC0`, `002A5F40`, `0023F240`,
  `00284EC0`, `0029B870` and `0055C740`. None of them is address-taken. Every direct-caller path ends at a
  decoded proc whose call site sits in its message-10 arm. They therefore share the message-10 placement.
- **H2. `002287D0` is the arbiter's own callee.** Its only caller is `00253C70`, at `00253CCC`. That call comes
  before every one of the arbiter's five clears (`00253F70`, `00253FE9`, `002540C5`, `0025415F`, `002541BC`), so it
  reads the snapshot before the arbiter clears it, whatever the frame kind.
- **H3.** The arbiter reads the word itself.
- ~~**N. Not placed: `002D3900`.** Most of its paths come from message-10 arms, but one comes through `002BD680`'s
  message-9 (focus lost) arm, whose sender is the focus switch rather than a frame position.~~
  *Corrected 2026-09-28 (FABLE, Claude Opus 5.5): the call sites are in `002BD680`'s message-**10** arm.* The first
  decoder did not model `002BD680`'s `lea eax, [rcx - 1]`, so it read every id one too low. The table itself sends
  message 10 to `002BD714`, which holds both calls (`002BD71F`, `002BD745`), and message 9 to `002BD834`. With that,
  all 22 paths into `002D3900` come from message-10 arms, and it is placed.
  [`../gg1-dispatch-sim/`](../gg1-dispatch-sim/README.md) (`gg1_sim.py` P2 and control C1) is the regression. `N` in
  this record's output is kept as the historical receipt.
- **C. Control.** A known message-10 proc (`002778C0`) has no direct callers, so the helper test does not claim it.

**Tally for GG-1's 51 readers:** 16 message-10 procs, 7 message-10 helpers, the arbiter and its callee `002287D0`, for
**25 placed**. 26 are not placed:
- 2 readers in message-12 and message-31 arms;
- the mixed helper `002D3900`;
- `003C87B0`, reached from several frame positions;
- the procs and helpers whose dispatch this decoder does not read. Their list is in
  [`../gg1-message10-readers/gg1_msg10_readers.out`](../gg1-message10-readers/gg1_msg10_readers.out).

| consumer | action | agreement |
|---|---|---|
| `_index/OPEN-QUESTIONS.md` GG-1 | 25 of 51 placed; stays OPEN | revised-here |
