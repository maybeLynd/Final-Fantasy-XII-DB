# `_types`: two battle-HUD blocks identified - `+0x7FB0` is the level-up blink controller, `+0x8FA0` the target-info window (OPUS, 2026-09-30)

`ManagerSub0209BE80_7FB0` with its record type `ManagerSub7FB0Record`, and `ManagerSub0209BE80_8FA0`, sat at DISCOVERED /
PROBABLE. Their fields were
mapped on 2026-09-18/20, but the type rows never said what the block is. The battle HUD singleton (`0209BE80`) also
carries the battle menu widget at `+0xAB30`, the selection marker at `+0x10F00` and the target arrows at `+0x10F30`.

Static, the certified image. The checker is `hud_panes_check.py` (output `hud_panes_check.out`, **`FAILS 0`**).

## The identification (OPUS)

- **H1.** The per-frame update gate's group `0x0080` (flag byte bit 7 at `0028E450`) calls `00296860(hud + 0x7FB0, 6)`
  (`0028E459`–`0028E465`). That is the function's only caller.
- **H2.** `00296860` walks six records of `0x110`. A record's widget is built only when both of these hold:
  - its claim flag `+0xF0` is set;
  - its widget slot is free (`00273A20`).

  The build makes a `0xF0`-byte widget (`00245000`, then `00246AC0`) with procedure `00299D10` (`lea r8` at
  `002968B5`). It passes two values: the queued value at the consumer cursor (`+0xF8 + 4 × [+0x104]`) and the key
  `+0xF4`. The routine then clears the entry, advances the cursor mod 3, and drops the claim when the next entry is
  empty.
- **H3.** `00299D10` is the procedure that [the layout-parameter page](../../../16-UI/Layout-Parameter-System/ui-layout-parameters-and-editor-schema.md)
  and [the battle HUD layout readers](../../../16-UI/Battle-Hud/the-battle-hud-layout-readers.md) bind to the
  `LevelupBlink…` keys; it takes `LevelupBlinkSpeed` as its timer speed. Its per-row fade driver `00299FC0` resolves the
  entry through the actor getter `003588B0`, so the queued value is an actor ordinal.

**So:**
- **`ManagerSub0209BE80_7FB0`** is the **level-up blink controller**: six HUD slot records.
- **`ManagerSub7FB0Record`** is **one slot's level-up blink queue**. It holds the claim flag, the key, three queued actor
  ordinals, the consumer / producer cursors and the blink widget it spawns.

Both move to **SEMANTICALLY IDENTIFIED / PROVEN**. No field row changes: the per-field meanings recorded on 2026-09-20
already say this mechanically.

**In player terms:** this is the flashing "Level Up" marker on the party HUD. Each of six slots can queue up to three
level-ups, and each one plays as its own blink.

## `+0x8FA0`: the target-info window (OPUS)

- **H4.** The HUD constructor `00291750` builds `ManagerSub0209BE80_8FA0` at `hud + 0x8FA0` through `002BE450`
  (`002917AA`–`002917B1`). It is a `0x1110`-byte widget (`00245000`) with procedure `002BE490`. That size is the one
  CON-124 settled.
- **H5.** The pane's open / close router is `002BE1A0(hud + 0x8FA0, mode, …)`, reached only through `0028FE40` /
  `0028FEA0` (each does `add rcx, 0x8fa0` on `[0209BE80]`).
  - Mode 1 runs the teardown `002BEED0`.
  - Any other mode runs `002BE300(hud + 0x8FA0 + 0xAC0)`. When its record is live, that tail-jumps to `002C0F30`,
    which builds a `0x2B8`-byte widget with procedure `002C0870`, the procedure the layout-parameter page binds to the
    `TargetInfo…` keys.
  - `0028FEA0`'s one caller is `0027B880`, an arm of the battle menu's `BattleMenu_UpdateCommandSelectionAndDispatch`
    `002778C0`.

**So `ManagerSub0209BE80_8FA0` is the battle HUD's target-info window.** Its `+0xAC0` sub-object holds the live
TargetInfo widget (`+0x570`), its id (`+0x578`) and its flags (`+0x57E`). It moves to **SEMANTICALLY IDENTIFIED /
PROVEN**.

**In player terms:** this is the small window that shows the target's details while you pick a target from the battle
menu.

## Limits

- `+0x8FA0`: what the pane draws beyond the TargetInfo child, and `0028FE40`'s caller `0035C150`, a 5-byte thunk with
  five callers, are not read.

- Which six HUD slots the records serve is not read, nor who produces into the queue. The producer is the writer of
  `+0xF0` / `+0x106`, already cited on the field rows.
- The tail `+0x660`–`+0xFEF` of the `0xFF0` span is still unobserved. Its size is still the next sibling's start.
