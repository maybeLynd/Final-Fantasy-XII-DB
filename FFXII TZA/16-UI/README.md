# UI

**Engine category.** Screens, the native request router, menus, HUD, lists and transitions.

| | |
|---|---|
| Classification source | PrimaryOwner: UI |
| Functions | 544 |
| Status | see [`../_index/COVERAGE.md`](../_index/COVERAGE.md) |

## Systems in this category

- [`Handbook/the-handbooks-monster-viewer.md`](Handbook/the-handbooks-monster-viewer.md) -
  **DOCUMENTED, tier 1.** The bestiary's 3D monster, end to end: the `MonsterId` entry reader, the staged
  model loader (body, two weapons, motion set), the viewer singleton, and the render-record flag that keeps
  the model unculled and lets it be drawn only in the full-menu frame.

- [`License-Board-View/the-license-board-grid-build-and-its-change-sweep.md`](License-Board-View/the-license-board-grid-build-and-its-change-sweep.md) -
  **PARTIAL, tier 1.** The board's runtime grid takes its dimensions from **`licd`'s own header**
  (`+0x04` width, `+0x06` height) **plus one**, selected by the character's job with `0xFF` for
  no board. The change sweep that decides which squares need redrawing - `0055B310` - **is not in
  the function census**; it compares two nibbles of each square's `+0x18` and collects **exactly 32**
  changed squares, silently dropping the 33rd.

- [`Dynamic-Geometry-Instances/dyngeo-instance-family.md`](Dynamic-Geometry-Instances/dyngeo-instance-family.md) —
  **DOCUMENTED, tier 1.** Eight `DynGeo*` classes in three vtable shapes, and a **Shadow ×
  Final 2×2 matrix implemented by prefix code plus a tail-call into one shared body**. The
  UI text drop shadow is a separate draw, not a shader effect.
- [`Request-Router/ui-request-router.md`](Request-Router/ui-request-router.md) - request IDs 1..24, the policy refusal gate, and the fullscreen-mode translator
- [`CONTRACT-ui-request-router.md`](CONTRACT-ui-request-router.md) - **subsystem scope (FABLE, 2026-09-21)**: the router's interface and dispatch tables, the single-slot mailbox, the three refusals that all return 0, and the request word that latches the router and the input arbiter together
- [`Map-Screens/the-map-screens-and-their-shared-map-data.md`](Map-Screens/the-map-screens-and-their-shared-map-data.md) -
  **PARTIAL, tier 1.** Track map, location map and world map, identified by the readers of their layout keys. Two of them
  share one `0x179E0` page-flip container class, and all three share one `0x278` map-data widget (108 functions).
- [`Menu-Screen-Atlas/the-menu-screen-atlas.md`](Menu-Screen-Atlas/the-menu-screen-atlas.md) -
  **PARTIAL, tier 1.** The 80 menu widget procedures in `00550000`–`00580000`, labelled by the layout keys they read, the
  files they request and their installers. 913 of the 1,065 frontier functions under them now have a screen; 1,830 of 2,648 across all 267 handler-census procedures.
- [`Text-And-Number-Rendering/font-data-kerning-and-expansion.md`](Text-And-Number-Rendering/font-data-kerning-and-expansion.md) -
  **DOCUMENTED, tier 1.** `.ker` kerning pairs and `.fex` keyed character lists, requested by bits 0 and 1 of the
  font `.dat` flags for the fonts a language's `fontlist.ah` names. Every requested file parses; the two `us` `.fex`
  that do not are the two nothing requests.
- [`Text-And-Number-Rendering/the-text-control-code-language.md`](Text-And-Number-Rendering/the-text-control-code-language.md) -
  **PARTIAL, tier 1.** `002AC5F0`, **the largest unclassified function in the executable (7,489 B)** —
  and **it draws nothing.** It is the sole interpreter for the codes embedded in game text: bytes
  `0x01`-`0x0F`, with `0x0F` + an ASCII letter for an extended set of **32 arms**. Both jump tables
  decoded and shown to tile with no gap. **Every pass that walks a string calls it**, two of them
  mutually recursively, which is why it is the size it is.
- [`Widget-Object-Model/the-widget-constructor-and-object-sizes.md`](Widget-Object-Model/the-widget-constructor-and-object-sizes.md) -
  **PARTIAL, tier 1.** One constructor builds every widget: **zero `size` bytes, install the handler
  at `+0`, write a fixed header, call the handler once.** **49 sites, 26 object sizes**, each with its
  handler — so a displacement row can now be *typed* by the size of the object it lives in. **A parent
  builds its children inside its own allocation.** Also records a third way a field access hides from
  a displacement census: **a size passed as an immediate is never a memory operand.**
- [`Message-Windows/the-message-window-layout-readers.md`](Message-Windows/the-message-window-layout-readers.md) -
  **PARTIAL, tier 1.** The MsgWin layout-key readers placed at their use sites — the message-window
  helper families' geometry, font and band parameters.
- [`Battle-Hud/the-battle-hud-layout-readers.md`](Battle-Hud/the-battle-hud-layout-readers.md) -
  **PARTIAL, tier 1.** The battle-HUD layout-key readers — HP gauge, boss gauge, number effects,
  battle command — placed at their use sites by helper chain.

## How to add a system here

1. Copy [`../_templates/SYSTEM.md`](../_templates/SYSTEM.md) into a descriptively-named
   subfolder (or as a `.md` file if it is a single mechanism).
2. Fill all eight sections. A missing section means `STUB` or `PARTIAL`, never `DOCUMENTED`.
3. Mirror every "What is not known" entry into
   [`../_index/OPEN-QUESTIONS.md`](../_index/OPEN-QUESTIONS.md).
4. Register any cross-subsystem chain in
   [`../_index/CALL-CHAINS.md`](../_index/CALL-CHAINS.md).
5. Obey [`../_index/EVIDENCE-STANDARD.md`](../_index/EVIDENCE-STANDARD.md).
   No banned evidence class, ever.

## Systems in this category

- [`Layout-Parameter-System/ui-layout-parameters-and-editor-schema.md`](Layout-Parameter-System/ui-layout-parameters-and-editor-schema.md) -
  **DOCUMENTED, tier 1.** 231 layout parameters in `jsondata/uisize/uisize.json`, plus the
  developers' own **editor schema** (229 trackbars with min/max, 36 sections).

## Cross-subsystem neighbours — SWE2-STRUCT (pass-22 dispositions)

- **Presentation - CLIENT and SERVICE (2 edges).** `002AC5F0` is called by bodies filed to Presentation: `002AAE40`; `002AC5F0` reaches bodies filed to Presentation: RenderCommand_SubmitCurrentBufferAndSwap (`003A1DB0`) - shared machinery across the layer boundary, no shared ownership.
