# GG-1: the message-12 reader runs only inside message-10 handling (FABLE, Claude Opus 5.5, 2026-09-28)

affected: GG-1 (register row)

[`../gg1-dispatch-sim/`](../gg1-dispatch-sim/README.md) left `0023FBE0` unplaced. It reads `02F9736A` in its
message-12 arm, and message 12 is sent from many kinds of arm. The census of senders could not place it, but the
sub-code can. [`gg1_msg12.py`](gg1_msg12.py) ([output](gg1_msg12.out)) was verified at a0468e5fa, FAILS 0:

- **E1.** The read (`0023FFF6`) sits under the message's sub-code `qword [msg+8]` == **0x8002**
  (`0023FF96`-`0023FFA6`).
- **E2.** Exactly seven calls to the notifier `00247510` send 0x8002:
  - **Four originate it inside message-10 handling:** `00557B90` twice and `0055C740` (helpers reached only from
    message-10 arms), and `0057C480`'s message-10 arm.
  - **Three forward it:** `002C59D0`, `0056F810` and `005742D0` re-send 0x8002 from their message-12 arm only
    when the incoming sub-code is 0x8002.
- **E3.** No other sender of message 12 can carry 0x8002. Each of the other 15 `00247510` calls resolves to one of:
  - a literal;
  - a small `lea` of a zeroed register (`eax` is exactly 3 at `0057A507`);
  - `003EF050`'s pass-through of the code it received;
  - `0057C480`'s code table, which `0057C140` fills only from `0057C320`'s five literals, 0x8100-0x8106, and which
    is reset to 0;
  - a stack address: `00293170`, and `00292390`'s create-time replay of `00293170`'s context (message 1 is
    `{1, ctx+8, ctx+0x10}`, `002465F0`).
- **E3b.** The stack-built `{12}` records are exactly five, and none carries 0x8002. `00241A70` and `005519E0` send
  0x8101 (the `.rdata` pair at `00915270`), `00241B40` sends 0x8100 or 0x8101, and `002BF8C0` sends 0.
- **E4.** `00247510` delivers synchronously, calling the window's proc through `[window + 0]`.
- **C1, C2 (controls).** The simulator's decode of `0023FBE0` puts message 1 at `0023FC23` and message 12 at
  `0023FEE2`, and the census finds the known literal at `002C5DBE`.

**Placement.** Every 0x8002 notification starts in a message-10 handler and reaches `0023FBE0` while that handler is
still running. So the read has the message-10 readers' placement
([`../gg1-static-order/`](../gg1-static-order/README.md)): in the field frame on both sides of the world tick, and in
the full-menu and capture frames after it.

**Tally: 50 of 51 placed.** The one left is `003C87B0`. It is reached from message-1, message-10, message-12 and
message-18 arms, and from four roots that are not procs.

**Limits.**
- A message record copied from a queue, rather than sent through `00247510` or built on the stack, is outside the
  census, as in the earlier records.
- A forwarder that re-broadcasts the message it received passes a notification along; it never originates one.

| consumer | action | agreement |
|---|---|---|
| `_index/OPEN-QUESTIONS.md` GG-1 | 50 of 51 placed; stays OPEN | revised-here |
