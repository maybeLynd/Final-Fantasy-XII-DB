# GG-1: the two message-2 readers are placed through the reconcile walks over their layer (FABLE, Claude Opus 5.5, 2026-09-28)

affected: GG-1 (register row)

[`../gg1-chain-procs/`](../gg1-chain-procs/README.md) left `0027AA70` and `005519E0` unplaced. They read `02F9736A` in
their message-2 (reconcile) arm, and the reconcile sender `00248030` is called from several places. This record follows
the reconcile to these two windows. [`gg1_msg2.py`](gg1_msg2.py) ([output](gg1_msg2.out)) was verified at b3e15c71d,
FAILS 0.

- **S1.** Both readers read the word only in their message-2 arm.
- **S2. Both windows sit under the layer root `[0208EA28]`.**
  - `0027AA70`'s window is created inside `00279E20`'s object and linked under `00279E20`'s window.
    - `00276650` creates `00279E20`'s window and attaches it with `00246AC0`.
  - `005519E0` runs only as the base proc of `00551E00` / `00551F00`, which forward every message to it.
    - Their windows are linked under `005528C0`'s.
    - `00552250` attaches that window to `[0208EA28]` at `005524E1`.
- **S3.** `00246AC0` is `00246AD0([0208EA28], w)`, which links a window that has no parent.
- **S4. The reconcile walk `00248030` sends `{2}` to every window under the root it is given.**
  - These walks reach `[0208EA28]`:
    - `002507C0`;
    - `00250730`;
    - the UI pass `00250540` on its main path (a loop over three roots from `0208EA20`).
  - These do not:
    - `002506D0` (EA48);
    - `002508E0` (EA38, EA40, EA48);
    - `00250540`'s early path (EA48);
    - the walk that `002284F0` makes once, inside the arbiter, when it creates its widget (EA40).
- **S5.** Each pump function opens and closes its own walk generation (`002481A0` / `00248190`). So each call reaches
  every window under its roots once, even though a window already visited in a generation is skipped.
- **S6. No other `{2}` reaches a window proc.**
  - `002A6190`'s `{2}` record is a layout record: `00247570` only stores it at `+0x48`.
  - The stack-built `{2}` records go to a manager (`003C2190`) or through object vtables.
- **Controls.**
  - **C1.** The window link found by [`../gg1-msg31-arbiter/`](../gg1-msg31-arbiter/README.md) reproduces.
  - **C2.** The frame call sites [`../gg1-static-order/`](../gg1-static-order/README.md) uses reproduce.

**Placement.** The two readers read the snapshot at every reconcile over layer EA28.
- **Field frame `0022A770`:** before the world tick (`002507C0` at `0022AB83`, under that call's gate) and after it
  (`0022AC17`). These are the same two positions as the message-10 readers.
- **Full-menu and capture frames (`0022B8C0`, `0022BC20`):** after the world tick, in the UI pass's main path. Its
  early path and its `002508E0` branch do not walk EA28.
- **Frames `0022B6E0` and `0022B7E0`:** these reach EA28 through `00250730` and `002507C0`. They make no direct call to
  the world tick, and whether the arbiter runs in them is not established here.
- **Inside the arbiter:** neither reader is reached. Its creation walk covers EA40 only.

**Tally: 39 of 51 placed.**

**Not placed (12):**
- `0023FBE0` (message 12);
- the mixed helper `002D3900`;
- ten that no decoder or caller walk places.

**Limit.** A window with bit 18 of `+0x40` set is walked without the send. One with bit 10 set takes `002482E0`, which is
not read here.

| consumer | action | agreement |
|---|---|---|
| `_index/OPEN-QUESTIONS.md` GG-1 | 39 of 51 placed; stays OPEN | revised-here |
