# GG-1 extended: 16 of the 51 readers are placed by one sender (FABLE, Claude Opus 5.5, 2026-09-28)

affected: GG-1 (register row); 16-UI/Widget-Object-Model/the-widget-message-protocol.md (the message-10 row)

Companion to [`../gg1-static-order/`](../gg1-static-order/README.md), which ordered the battle command menu's read of
`02F9736A` against the input arbiter for each frame kind. That order came from one fact: the read sits in the widget
proc's focus-input arm (messages 10/11), and `002481C0` sends those messages from fixed frame positions.

**Measured** ([`gg1_msg10_readers.py`](gg1_msg10_readers.py), [output](gg1_msg10_readers.out)). Run verified at 4933c61e6,
FAILS 0:
- **M1.** A generic jump-table decode covers all 51 readers of `02F9736A` and decodes 18 of them.
- **M2.** 16 readers read the word only in a message-10 or 10/11 arm:
  `00228C70`, `0023BD40`, `0023CE10`, `00241D40`, `002778C0`, `00280DE0`, `002A6190`, `002D5EB0`, `00552250`,
  `005528C0`, `005542D0`, `00560910`, `00571A50`, `00572E10`, `005742D0`, `0057AC10`.
  Two more read it in other arms: `0023FBE0` under message 12 and `003CAB00` under message 31.
- **M3. `002481C0` is the only sender of messages 10/11.**
  - The `.rdata` records `009150D8` `{10}` and `009150F0` `{11}` are referenced only by `002481C0`.
  - The one stack-built `{10}` passed as a message argument (`0057F6B0` → `00582540`) goes into an event queue, not to a widget
    handler.
- **Controls.** C1: the decoder reproduces `002778C0`'s table. C2: the stack scan finds the known stack `{10}`.

**So all 16 share the command menu's placement.**
- In the full-menu and capture frames, focus input arrives after the world tick that runs the arbiter.
- In the field frame it can arrive both before the arbiter (`0022AB83`, gated by bit 3 of `022C7F92` and a zero step
  accumulator) and after it (`0022AC17`).
- While paused, the pause step delivers it and the frame ends before the world tick.
- Each widget receives the message only when it is the focus top. Its read then sees the snapshot as the arbiter has
  or has not yet left it.

**Not placed.** 33 readers do not decode as jump-table message procs (cmp chains, direct frame callees and other shapes)
and are listed in the output. The arbiter itself is one of them. Two decoded readers (messages 12 and 31) have other
senders, not placed here. A message-10 arm that falls through into shared code, or a read reached through a shared
helper from another arm, would escape this arm-contiguity reading.

| consumer | action | agreement |
|---|---|---|
| `_index/OPEN-QUESTIONS.md` GG-1 | 16 of 51 readers placed; stays OPEN | revised-here |
| the-widget-message-protocol.md, message-10 row ("from the Config screen") | note added: the only sender is the focus notice `002481C0`; 16 readers of the input snapshot sit in message-10 arms | revised-here |
| the input contract's GG-1 bullet | follows the earlier request (FABLE-REQ-CONTRACT-GG1-STATIC-ORDER) | routed-to-CONTRACT |
