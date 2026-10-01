# GG-1: eleven more message-10 readers, by an extended dispatch decode (FABLE, Claude Opus 5.5, 2026-09-28)

affected: GG-1 (register row)

This extends [`../gg1-message10-readers/`](../gg1-message10-readers/README.md). That decoder read MSVC jump tables
whose offset register was an `e`-register. It missed two shapes: tables loaded through `r8d`, and `sub` / `je`
chains in which the message id accumulates across the subtractions.
[`gg1_chain_procs.py`](gg1_chain_procs.py) ([output](gg1_chain_procs.out)) reads both. Run verified at 71a9b49f3, FAILS 0:

- **D1.** 11 more readers read `02F9736A` only in a message-10 arm:
  `0023B6F0`, `0023C5C0`, `0023D6B0`, `0023DB40`, `0027EA70`, `002C59D0`, `003C8B70`, `003EF050`, `003F4330`,
  `00572600`, `005789D0`. Message 10 has one sender, `002481C0` (M3 of the message-10 record), so they share its frame
  placement ([`../gg1-static-order/`](../gg1-static-order/README.md)).
- **D2. Not placed: `0027AA70` and `005519E0`.** They read under **message 2**, the per-frame reconcile. Its sender
  `00248030` has five other callers but is also called from `002284F0`, which is not a fixed frame position.
- **C1. Control.** The extended decoder agrees with the first decoder on all 16 of its readers.
- **C2. Control.** The chain decode of `0023B6F0` matches its head: ids 1, 4, 10 and 12 by `sub` / `je`, and 13 by the
  `cmp` / `jne` fall-through.

**Tally: 36 of 51 placed.** That is 27 message-10 procs, 7 message-10 helpers, and the arbiter with its callee
`002287D0` ([`../gg1-helper-readers/`](../gg1-helper-readers/README.md)).
**15 are not placed.** This list was computed from the 51 readers minus the 36 placed:
- the two message-2 readers, `0027AA70` and `005519E0`;
- `0023FBE0`, which reads the word in its **message-12** arm. Its message-10 arm is the one that places the helper
  `0023F240`;
- `003CAB00`, which reads it in its **message-31** arm. No sender of 12 or 31 is placed yet;
- `002D3900`, which is mixed: one path comes through a message-9 arm (`../gg1-helper-readers/` N);
- 10 that neither decoder reads as a message proc and no caller walk places: `002878E0`, `002A9980`, `002C2320`,
  `003C87B0`, `003FDAD0`, `003FF360`, `00564D30`, `00564E10`, `0056CA60`, `0056DED0`.

**Limit.** For a chain, "the arm that holds a read" is the nearest preceding arm target in address order. Code shared
between arms, or reached by a jump across arm boundaries, would escape that reading.

| consumer | action | agreement |
|---|---|---|
| `_index/OPEN-QUESTIONS.md` GG-1 | 36 of 51 placed; stays OPEN | revised-here |
