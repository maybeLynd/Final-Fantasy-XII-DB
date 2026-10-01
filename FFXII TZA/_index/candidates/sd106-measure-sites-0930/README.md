# SD-106: the five `002B3280` sites measure a message line and the confirm dialog's caption and choices (OPUS, 2026-09-30)

Register row SD-106 was registered by SWE2-DATA ([the-text-element-dispatch-table.md](../../../99-Unresolved-Residual/Glyph-Run-Rendering/the-text-element-dispatch-table.md)
section 7). It asks what the five `002B3280` sites display. The wrapper builds kind-0 text elements outside the
message window.

This record is static. The checker is `sd106_sites.py` (output `sd106_sites.out`, `FAILS 0`).

## The answer (OPUS)

~~**`002B3280` builds a kind-0 element on a text and hands back its measured width and height.**~~ **`002B3280`
builds a kind-0 element on a text and, called with `r9d` ≠ 0 (as all five sites call it), hands back its measured
width (`+0x94` + 8) and height (`+0x96`). With `r9d` = 0 it builds through `002B3D50` and takes the element's size
from the same two pointers instead.** *(narrowed 2026-10-01, SWE2-CONTRACT for OPUS, on SWE2-AUDIT-SPEC's [review](../auditspec-review-sd106-0930/REVIEW.md) item 1)* It forwards to the
kind-0 builder `002B32D0` with two out-pointers (M1). So each site sizes a window to a text; none draws
through the wrapper. The layout keys each caller reads are already listed on
[the message-window layout readers](../../../16-UI/Message-Windows/the-message-window-layout-readers.md) and
[the UI layout parameters](../../../16-UI/Layout-Parameter-System/ui-layout-parameters-and-editor-schema.md).

| site | caller | text | what the size is for | keys the caller reads |
|---|---|---|---|---|
| `00227FE3` | `00227EE0` | the message argument's `+8`, in the window's element `+0xC0` | **a one-line message, ~~centred on screen~~ centred on the UI canvas `[01E0C1D8]` x `[01E0C1DC]` (512 x 448, or 1920 x 1080 when `0024B120` selects it)** *(narrowed 2026-10-01, SWE2-CONTRACT for OPUS, on SWE2-AUDIT-SPEC's [review](../auditspec-review-sd106-0930/REVIEW.md) item 3)*: x = (`[01E0C1D8]` − w) / 2, y = (`[01E0C1DC]` − h) / 2 (M2) | `GeneralFrame`, `MessageLine`, `NobuMessage` |
| `00241DEB` | `00241D40` | **the confirm dialog's caption** buffer `+0x1B0` (given a leading byte 4 when empty), in element `+0xE0` | the dialog's width, raised to the minimum at `01E0C0D4` (M3) | `ConfirmCaption`, `ConfirmCursor`, `ConfirmWindow` |
| `0057C1E2` | `0057C140` | **one confirm-dialog choice**: the string it adds to the dialog's choice table (id word `+0x5B8`, flag `+0x5BC`, count `+0x636`), measured in a frame element | the choice list's width: w + 2 × `[01E0CDC0]`, against the rows' widths (M4) | `ConfirmWindow` |
| `0057C58B`, `0057C5DB` | `0057C480` | ~~**the confirm caption** again (`+0x1B0`, element `+0xE0`), on two paths: after `002B3400` initialises the element on it, and after a 0x400-byte clear~~ **the confirm caption** again (`+0x1B0`, element `+0xE0`), on two of the message arm's three paths. `0057C58B` measures the caption copied from the argument when `+0x630` bit 0x20 is clear (with the bit set the caption goes through `002B3400` / `002B3050` and `002B3280` is not called). `0057C5DB` runs when the argument has no caption: the buffer is cleared by `memset` (`00861EC0`, 0x400 bytes), and the measured size is discarded for height 0 and width 2 x `[01E0CDC0]`. On every path the width is then raised to 0x60. *(narrowed 2026-10-01, SWE2-CONTRACT for OPUS, on SWE2-AUDIT-SPEC's [review](../auditspec-review-sd106-0930/REVIEW.md) item 2)* | ~~the size read back at `[rbp+0x58]` / `[rbp+0x50]` (M5)~~ the dialog's caption width and height, `[rbp+0x58]` / `[rbp+0x50]` (M5) *(narrowed 2026-10-01, SWE2-CONTRACT for OPUS, on SWE2-AUDIT-SPEC's [review](../auditspec-review-sd106-0930/REVIEW.md) item 2)* | `ConfirmCaption`, `ConfirmWindow` |

**For modding:** a longer confirm caption or choice widens the dialog by itself, down to the minimum at `01E0C0D4`.
A centred one-line message is centred on the text's measured size.

## Limits (OPUS)

- **The leading byte 4.** What it does in the caption (a control code, by position) is not read here.
- **The messages themselves.** Which authored messages reach `00227EE0` is not traced.
- **Static only.**

**Review:** routed to SWE2-AUDIT-SPEC (OPUS production → FABLE-side review). The register row belongs to SWE2-DATA's page.
