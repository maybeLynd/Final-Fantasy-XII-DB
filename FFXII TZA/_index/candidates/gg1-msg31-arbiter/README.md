# GG-1: the message-31 reader reads the snapshot inside the arbiter, one instruction before its first clear (FABLE, Claude Opus 5.5, 2026-09-28)

affected: GG-1 (register row)

This continues [`../gg1-chain-procs/`](../gg1-chain-procs/README.md), which left `003CAB00` unplaced: it reads
`02F9736A` in its **message-31** arm. [`gg1_msg31.py`](gg1_msg31.py) ([output](gg1_msg31.out)), verified at 022a8d431,
FAILS 0:

- **S1.** `003CAB00` sends message 31 to arm `003CAC6A`, and only message 31 goes there. Both of its reads of the
  word lie in that arm. They test it against the masks that `0029DBE0` returns for actions `0x10E` and `0x10D`.
  On `0x10E` it broadcasts `{30}` to its children; on `0x10D` it calls `00249C60`.
- **S2.** The census used for message 10 finds three `{31}` builders and no `.rdata` `{31}` record: `003CA200`,
  `00551E00` and `00551F00`.
- **S3.** `003CA200` calls the proc of the window at `[02B47758] + 0x2A0`.
  - The only non-zero store to `02B47758` is `003CA280`'s: the window `00244F50` creates with the proc
    `003CA860`.
  - The window initialiser stores the proc at `+0`.
  - `003CA860` creates its `+0x2A0` child with the proc `003CAB00`. That is the only reference to `003CAB00`.
- **S4.** `00551E00` and `00551F00` are installed only by `005528C0`. They send their `{31}` through `00275440`
  on their own window, and `00275440` walks that window's child list. `003CAB00`'s window is linked under
  `003CA860`'s, so their broadcasts do not reach it.
- **S5.** `003CA200`'s only caller is the arbiter `00253C70`, at `00253F6B`. The next instruction, `00253F70`, is the
  first of the arbiter's five clears of `02F9736A`.
- **C1 (control).** The decoder reads message 1 as `003CAB54`, the instruction after the table jump.
- **C2 (control).** The same census finds the known message-12 sender `00247510`'s store at `00247523`.

**Placement.** `003CAB00` reads the snapshot inside the arbiter, in the world tick
([`../gg1-static-order/`](../gg1-static-order/README.md)). It reads before the clear at `00253F70` that ends that
path, so it sees the value as the world tick found it.

**Tally: 37 of 51 placed.**

**Not placed (14):**
- `0023FBE0` (message 12). Five builders send `{12}`, including the generic sender `00247510` with over ten callers,
  and the proc is installed in four places.
- the message-2 readers `0027AA70` and `005519E0`;
- `002D3900`;
- the ten that no decoder or caller walk places.

**Limit.** A message record copied from a queue or an argument, instead of built by constant stores, is outside the
census. This is the same limit the message-10 record carries.

| consumer | action | agreement |
|---|---|---|
| `_index/OPEN-QUESTIONS.md` GG-1 | 37 of 51 placed; stays OPEN | revised-here |
