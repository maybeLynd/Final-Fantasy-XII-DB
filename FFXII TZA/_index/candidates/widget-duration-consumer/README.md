# Consumer check: the widget deferred dispatch and the two durations (FABLE, Claude Opus 5.5, 2026-09-28)

affected: 16-UI/Widget-Object-Model/CONTRACT-widget-object.md, 16-UI/Layout-Parameter-System/ui-layout-parameters-and-editor-schema.md

Consumes three ASTRA returns, each with the verdict **ACCEPT**, re-derived from the listing in
[`widget_check.py`](widget_check.py) ([output](widget_check.out)):
- **WIDGET-DEFERRED-DISPATCH-DOMAIN.** Mode 2 zeroes `+0x70` when `+0x40` bit 16 is **set** (D1). The contract said
  "clear" (struck); the layout page already said "set". `+0x40` bit 0 gates the nibble dispatch (D2). Nibbles other
  than 0, 2 and 3 return before the tail. So the tail's nibble 4 and "always ORs `0x34`" hold only on the schedule and
  rebase paths; bit 0 clear sets nibble 1.
- **WIDGET-TIMED-DURATION-SELECTION.** The record's u16 is zeroed when `00181C90` returns 1, then replaced by the
  `+0x7C` override when bit 11 is armed, and that bit is consumed (D3). The unsigned conversion is exact over every
  u16 value (D4).
- **WIDGET-TRANSITION-DURATION-DOMAIN.** `+0x90` uses a 32-bit product and a signed division that truncates toward
  zero (D5, D5m): −17 gives −1, and 35,791,395 gives −2,147,483. The two conversions agree only on non-negative,
  non-overflowing input.

The layout page's other two errors are corrected too:
- 00181C90 does not run "on" the u16; it is a getter whose result gates it.
- "Divide-by-60" was ×60/1000.

| consumer | action | agreement |
|---|---|---|
| CONTRACT-widget-object.md, DL-3 paragraph | bit-16 polarity corrected; delay order, bit-0 gate and bail set added; tail limited to its paths | revised-here |
| CONTRACT-widget-object.md, `002468A0` paragraph | `+0x90` domain qualified (32-bit product, signed truncation, no clamp) | revised-here |
| ui-layout-parameters-and-editor-schema.md, the SWE2-EC7 `00244DD0` paragraph | getter / conversion / tail wording struck and corrected; its bit-16 wording kept | revised-here (SWE2-EC7 text; independent review requested) |

Regression: `widget_check.py` (D1-D5, D5m, control C). Run verified at cc9f6e6f8: FAILS 0.
