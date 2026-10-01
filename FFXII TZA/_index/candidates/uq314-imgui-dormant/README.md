# UQ-314 — the Dear ImGui debug menu cannot be re-enabled: only a dormant context ships

FABLE, Claude Opus 5.5, 2026-09-27. **NATIVE/STATIC. Nothing was executed.**
Control: `uq314_imgui.py` (4 checks, FAILS 0).

**Answer: no.** The image contains ImGui's context object and nothing that could build or draw a frame with it.

- **I1 — no frame, window or widget code.** The image carries the IO constructor's filenames `imgui.ini` and
  `imgui_log.txt`, which serve as the positive control. It carries none of the literals ImGui's frame, window and
  widget code creates:
  - `Debug##Default`, the window `NewFrame` opens;
  - `##Tooltip_`, `##Menu_`, `##Popup_`, `##Combo_`;
  - `#SCROLLX`, `#MOVE`, `#COLLAPSE`, `#RESIZE`.

  This matches SWE2-EC7's declaration of a 10-member dormant context (`23-Third-Party-Libraries/members/imgui.tsv`).
- **I2 — nothing but start-up and exit reaches it.** The 10 members are called from outside only by:
  - the static-object constructor `00791E70`, whose sole caller is `00169620`, slot 743 of the 1,172-slot CRT
    initializer table (it constructs the object and registers atexit);
  - the teardown stub `008B7D40`.
- **I4 — version-independent: nothing else can reach the context.** The object `00169620` constructs (`02EA58C0`) is
  referenced only by that initializer and its atexit stub `008B7DA0`. The constructors store no global pointer to
  it. So even frame code the string test missed could not reach this context.
- **I3 — no shipped script turns on any of the draw-mask gates.** The three draw-mask setter verbs
  (`20A0` / `20A1` / `20A2`, including `debug_setdrawmenustatus`) are called by no shipped script, while 56 ids of the
  same `0x20xx` band are called. This corroborates SWE2-DATA's census on the frame page §4.3 (all 10,045 files, nine
  locales).

**What this settles in the row's earlier narrowings.** The pad-device question is moot, because there is no ImGui
frame for a device to drive. The gate word `022C7F94` belongs to the game's own draw mask. Native routines set its
bits in ordinary play (the frame page §4.3: `crossfade`, `movieplay` and others), so it is not an ImGui switch.

**Not this row.** The debug menu the image does contain is the game's own developer menu, `DebugMenu_Render`
(`001CD0E0`, which prints Yes/No rows, UQ-14). It is not ImGui. Its reachability belongs to the developer-console
pages.
