# MS-4 narrowed: the map preload page is opened by its container, with the current field's sub-location (OPUS, 2026-09-30)

Register row MS-4 asks who sends the field-time map container `02B47760` message 14 (its opening), and with which index.
The page is [the map screens](../../../16-UI/Map-Screens/the-map-screens-and-their-shared-map-data.md) §2.6 and §7.
Static, the certified image. The checker is [`ms4_check.py`](ms4_check.py) (output [`ms4_check.out`](ms4_check.out),
**`FAILS 0`**).

## The answer, and what stays open (OPUS)

Two different message-14 deliveries exist, and only one carries an index.

1. **The page's message 14, which opens the preload (M3, M4).** The container's own procedure `003CB650` sends it. When
   the container receives message **`0x20`** (arm `003CB7DB`), it:
   - activates itself;
   - takes an index from one of two sources:
     - by default, `003BFDF0()`. That is `003C0380(field)`, where `field` is the current field id from `00264790`
       (`003148F0` is the fallback). In other words, the current field's sub-location.
     - when container `+0x179D8` is 6, `003BC160()` instead;
   - stores that index at `+0x179D0`;
   - when the index is not negative, creates the page (`00244F50(0xC0, 003CB4F0)`) and calls the page procedure
     directly with `{14, 0, index, 0}` (`003CB835`-`003CB85F`).

   The page's id-14 arm (`003CB581`) is the preload §2.6 describes.
2. **The container's own message 14 (M1, M2).** The generic activation helper `00246AC0` / `00246AD0` ends by handing
   every widget it activates the static message `01E0C0E0` = `{14, 0, 0, 0}`, so it delivers index 0.
   - The container receives that copy only when it activates itself in the same `0x20` arm (`003CB7DE`).
   - Its procedure ignores id 14: id 14 falls to the default arm `003CB9CF`.
   - None of the eleven rip references to `02B47760` activates the container or hands it to a message call. They test
     it, copy its `+0x190` block (the track and location map openers `002B6570` and `002BA040`), destroy it
     (`003CB410`), or build it (`003CB440`).
   - The control: `003CA2F0`, which does activate a widget, reads the neighbouring global `02B47758`. The census keeps
     the two apart.
3. **Image-wide (M5).** Only two stack-built message 14s are handed to a procedure: `003CB835` and `00292AB2` (an
   unrelated procedure). The only static message-14 struct handed to a procedure is `01E0C0E0`.

**In player terms:** when the field's map container receives its trigger message, it immediately starts loading the
map image of the sub-location you are standing in. A map screen opened later then finds it already cached.

**Still open, so the row is narrowed rather than answered:**
- **Who sends the container message `0x20`.** No code that names `02B47760` sends it a message, and no stack-built
  `0x20` sits beside a reference to it, so the sender reaches the container through the widget framework, for example
  a parent's dispatch to its children. That route is not traced here.
- **What container `+0x179D8` = 6 selects.** It is copied from the creation message's byte `+0x10` (`003CB6B2`).

## Proposed row text for SWE2-DATA, pipe-free (OPUS)

> **NARROWED 2026-09-30 (OPUS, record opus-ms4-0930, ms4_check.py FAILS 0):** the preload page's message 14 is sent by
> the container's own procedure 003CB650 when the container receives message 0x20 (arm 003CB7DB). It creates the page
> 003CB4F0 and passes the current field's sub-location index: 003C0380 of the field id from 00264790, or 003BC160() in
> mode 6. The container itself receives message 14 only as the activation helper's static copy (index 0, 00246AD0 with
> 01E0C0E0) and ignores it. Still open: who sends the container message 0x20.

## Review (OPUS)

Reviewed by SWE2-AUDIT-SPEC (request filed at publish). The row and its page box are the register owner's and the page
owner's. FRONTIER holds active tasks on this box, so the page is not edited here.
