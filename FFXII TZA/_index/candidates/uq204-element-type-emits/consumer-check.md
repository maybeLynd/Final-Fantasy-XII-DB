# Affected-consumer check: "0xA4 and 0xA7 emit nothing" corrected (FABLE, Claude Opus 5.5, 2026-09-27)

affected: 17-Presentation-Rendering/Effect-File-Formats/effect-element-type-dispatch.md (the 2026-09-20 paragraph on `0xA4` / `0xA7`, the "Not read here" list, the UQ-204 box)

run: uq204_emits.py at bbd3af82a (worktree = that HEAD plus this package), 5 checks, FAILS 0. E4 is the check that
measures the correction; E3 would fail on the old reading, because `0xA4`'s methods reach `003A3010` and `0xA7`'s
reach `003A34D0`.

**The change.** On 2026-09-20 I wrote that the element types `0xA4` (`00522300`) and `0xA7` (`00526A10`) "emit nothing
… put nothing on the draw list … contribute state, not draws". It is right that neither reaches a `0054xxxx` terminal
and that neither tail-calls. It is wrong that they draw nothing:
- `005227C5` is `call 003A3010`, which appends a raw-packet entry to the draw list (one the PC drain never submits);
- `00526D2D` is `call 003A34D0`, which registers a GiVmax run of program `004ECC50`.

The heading clause and the "state, not draws" sentence are struck with a dated note. The "Not read here" item is
marked read.

| consumer | what it says | state |
|---|---|---|
| dispatch page, the 2026-09-20 paragraph | `0xA4`/`0xA7` emit nothing | revised-here (struck; dated correction) |
| dispatch page, the type-to-pair table (`0xA4`/`0xA7` rows, terminal "none") | no `0054xxxx` pair | agrees (they have none; the table names pairs, not emits) |
| dispatch page, the interior citations of `00522300` (`003A3010` among the packet emitter's drivers) and `00526A10` (`003A34D0` under the cookie check) | the two calls | agrees (they were the contradicting evidence, already on the page) |
| `the-element-types-40-42-a0-ab-d0-d1.md` rows `0xA4`, `0xA7` / `0xAA` | methods and sizes only | agrees (no emit claim) |
| `members/effect-type-methods.tsv` | the handler addresses | agrees |
| register UQ-204 | "what each type is remains unread" | revised-here (answered by this record) |

Grep of "emit nothing", "state, not draws", `00522300` and `00526A10` across the database, 2026-09-27. Inbox and
audit-log mentions are receipts and are not edited.
