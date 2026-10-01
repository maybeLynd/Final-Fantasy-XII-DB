# SD-101: bit 24 is a per-subtree "draw in the second pass" switch, set by six screens (OPUS, 2026-09-30)

Register row SD-101 was registered by SWE2-DATA ([the-widget-tree-draw-pass.md](../../../99-Unresolved-Residual/the-widget-tree-draw-pass.md)
section 9). It asks what the second widget-draw bracket pass draws: which widgets carry flag bit 24, and so what the
player sees drawn in pass 1.

This record is static. The checker is `sd101_pass1.py` (output `sd101_pass1.out`, `FAILS 0`). It sweeps all 38,161
bodies of the `pe` module for writers of the bit.

## The answer (OPUS)

- **P1: the gate.** The draw walker compares widget node `+0x40` bit 24 with the pass index `0208F564`. The second
  bracket `00252990` walks both UI roots, `[0208EA28]` and `[0208EA40]`, with pass 1.
- **P2: widgets start in pass 0.** The constructor `002465F0` writes only bits 17, 11/3/1 and 14 of `+0x40`, so a new
  widget has bit 24 clear.
- **P3: the setters.** Image-wide, bit 24 is set in only five places:
  - two immediate ORs, `005728E6` and `00573AF5` (both handbook);
  - three shifted ORs (`on << 24`): `00247754` in the subtree setter, and `0057390E` / `00573952` in the handbook
    toggle.
- **P4: the switch is per subtree.** `00247730(widget, on)` clears bit 24, sets it to `on & 1`, and recurses through
  the children list (`+0x18`, siblings `+0x20`). A screen moves a whole panel between the passes in one call.
- **P5: who calls it.** 32 call sites: 19 pass 1, 3 pass 0 and 10 pass a variable. By the page the address index files
  the caller under:

  | screen (page) | sites (`:1` / `:0` / `:var`) |
  |---|---|
  | [UI layout parameters](../../../16-UI/Layout-Parameter-System/ui-layout-parameters-and-editor-schema.md) | 7 × `:1` |
  | the license board ([grid build](../../../16-UI/License-Board-View/the-license-board-grid-build-and-its-change-sweep.md), [screen widgets](../../../16-UI/License-Board-View/the-license-board-screen-widgets.md)) | 6 × `:1`, 2 × `:0`, 3 × `:var` |
  | [the handbook](../../../16-UI/Handbook/the-handbook-screen.md) | 3 × `:1`, 1 × `:0`, 2 × `:var` |
  | [the menu-screen atlas](../../../16-UI/Menu-Screen-Atlas/the-menu-screen-atlas.md) | 5 × `:var` (one toggle, `00561DC0`) |
  | the bazaar recipe screen | 1 × `:1` (`002A8BC5`) |
  | the field frame | 1 × `:1` (`00287BFD`) |
  | not indexed | 1 × `:1` (`002D6D51` in `002D6CA0`) |

- **P6: the handbook toggles as a set.** `005738D0(on)`:
  - stores `on` at `[0209AC30]+0xDEA` and calls `00247920(on)`;
  - sets the bit on its pane `[02CA9718]+0x110` and on `[[02CA9718]+0xF8]+0xE0`;
  - sets it on the subtrees `[02CA9718]+0xE8` and `0028F570()`.

  `00572890` and `00573980` also put the `+0x110` pane in pass 1. That pane is built from a template by `002CCCA0`
  the first time it is needed.

**What the player sees.**
- Pass 1 draws the panels those screens switch: layout-parameter panels, license-board and handbook panels, the menu
  atlas when its toggle is on, the bazaar recipe panel, and one field-frame widget.
- Pass 1 draws them in the frame's second bracket (`00252990`). The field frame calls it (`0022B8C0` / `0022BC20`)
  after the layer-6 work (`002590F0(6)` / `00375500(6)`). So these panels are drawn later in the frame than
  everything drawn in pass 0.
- That they appear *on top of* the pass-0 UI and the late VFX layers is the natural reading of that order. It is not
  shown here.

**For modding:** to lift a panel above the rest of the UI, call `00247730(panel, 1)` on it. The engine does this
itself for the screens above.

## Limits (OPUS)

- **Variable callers.** Ten sites pass a variable. Whether each passes 1 in practice depends on its caller.
- **Stacking.** The on-top reading (above) is inferred from frame order.
- **Wholesale copies.** A write that copies a whole `+0x40` word from another widget is not swept. The constructor
  does not do it.
- **Static only.**

**Review:** routed to SWE2-AUDIT-SPEC (OPUS production → FABLE-side review). The register row belongs to SWE2-DATA's page.
