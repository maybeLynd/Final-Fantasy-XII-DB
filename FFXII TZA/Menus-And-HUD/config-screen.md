---
title: "Config screen: the Config, Graphics Settings and Controls rows, what each change runs, and where each setting is saved"
kind: "system"
category: "Menus and HUD"
addresses: "0023FBE0, 002407F0, 0023BD40, 0017DB90, 001D1660, 0023CE10, 0215E6E0, 01F82D20"
---

## What the player sees

- Config holds the battle, camera, sound and language settings, and two rows that open Graphics Settings and Controls.
- Graphics Settings changes quality presets and display options; some changes ask for confirmation or a restart.
- Controls rebinds keys and sets mouse sensitivity, camera auto-rotation and the confirm button.
- Volumes slide while a direction is held; most other rows step once per press or repeat.

## How it works

### The screens

| Screen | Procedure | Opened by |
|---|---|---|
| Config (menu text `4BE`<sub>h</sub>) | `0023FBE0` | the main menu's Config entry, `00240680`; the title's New Game list, `002406F0` |
| Graphics Settings (`503`<sub>h</sub>) | `0023BD40` | Config's row command `20`<sub>h</sub> (`002401FD`), `0023BCC0` |
| Controls (`504`<sub>h</sub>) | `0023CE10` | Config's row command `21`<sub>h</sub> (`002401CC`), `0023CC90` |

The main menu's list builder `00281AE0` always adds Config (`00281C86`) and never adds the other three, so the player
reaches Graphics Settings and Controls only through Config. Leaving either reopens Config on its row (`0023C537`,
`0023D430`-`0023D467`).

Config's rows come from the row-list table at `01E0BF60`, 45 pointers indexed by the screen's mode byte `+C0`<sub>h</sub>
(`0023FBE0`, `0023D4F0`). Each row list is a 4-byte header followed by
6-byte rows (below); a row with label `FFFF`<sub>h</sub> is a separator.

`002405B0(mode, row)` returns a row of list `mode`,
or 0 for a mode of 45 or more, an empty entry or a row past the header's count `+2`; Config reads the row's help id
`+4` through it and shows it on the help line (`0023FF5D`-`0023FF8A`). The opener
(`002406D2`) picks mode 0 (`01E0B670`, 27 rows) when the story counter (`00265270`) is 26 or more, otherwise mode 2
(`01E0B7D0`, the same rows without the last three). Mode 1 (`01E0B720`) is the title's New Game list.

`0023D610(screen, mode, origin)`, called from `0023BD40` (`0023BE66`), stores the mode byte `+C0`<sub>h</sub>, the origin
`+C2`<sub>h</sub>, the row list `01E0BF60[mode]` at `+C8`<sub>h</sub> and its layout kind at `+C1`<sub>h</sub>; it loads the layout named by
byte `+1` of the kind's `01E0B638` entry (`00394700`) and sets the draw priority from its word `+2`.

Leaving Config runs `0023ED10`: it closes the screen and, unless the row command waiting at `+4D0`<sub>h</sub> is `20`<sub>h</sub> or
`21`<sub>h</sub>, returns to the Party Menu on Config (`002814E0(4BEh)`) for origin 0 or 2, or clears the help line
(`00291D80(0, 0)`) for origin 1. `0023EF80(screen, command)` finds a row's `18`<sub>h</sub>-byte slot among the 42 at
`+E0`<sub>h</sub> by its first byte; Config uses it to drop the slot's `+08`<sub>h</sub> or `+10`<sub>h</sub> when a row posts `12`<sub>h</sub> or `1C`<sub>h</sub>
with its command (`0023FF11`-`0023FF4D`).

The row list header:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u8` | layoutKind | indexes `01E0B638` |
| `01`<sub>h</sub> | `u8` | b1 | - |
| `02`<sub>h</sub> | `u16` | rowCount | rows that follow |

A row:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u8` | command | the command |
| `01`<sub>h</sub> | `u8` | flag | - |
| `02`<sub>h</sub> | `u16` | label | label text, `FFFF`<sub>h</sub> for a separator |
| `04`<sub>h</sub> | `u16` | help | help text |

### Config rows

| Command | Label | Options | Stored in the options record | Runs at once |
|---:|---|---|---|---|
| `20`<sub>h</sub>, `21`<sub>h</sub> | Graphics Settings, Controls | - | - | opens the screen |
| `04`<sub>h</sub> | Battle Mode | Wait, Active | dword 0 bit 3 (`002DE060`) | - |
| `05`<sub>h</sub> | Battle Speed | 6 steps | dword 0 bits 4-11 (`002DE0F0`) | - |
| `06`<sub>h</sub> | Target Lines | On, Off | dword 1 bit 22 (`002DE2D0`) | - |
| `08`<sub>h</sub> | Cursor Position | Last Selection, Default | dword 0 bit 15 (`002DE1E0`) | clears the saved cursors (`002526D0`) |
| `09`<sub>h</sub> | Vibration Function | On, Off | dword 0 bit 13 (`002DE080`) | `0035FF30` |
| `0A`<sub>h</sub> | Screen Shake | On, Off | dword 0 bit 14 (`002DE200`) | `0037DDC0` |
| `0B`<sub>h</sub> | Subtitles | On, Off | dword 0 bit 12, set for Off (`002DE230`) | - |
| `0C`<sub>h</sub>, `0D`<sub>h</sub> | Camera Y-Axis, Camera X-Axis | Normal, Inverted | dword 1 bits 8, 9 (`002DE190`, `002DE160`) | `001E1020`, `001E0FF0` |
| `0E`<sub>h</sub> | Speed Mode Multiplier | x2, x4 | dword 1 bits 23-26 (`002DE250`) | the game speed through `0023B2E0` |
| `10`<sub>h</sub> | Language | Japanese, English | dword 1 bit 10 (`002DE2F0`) | - ([Voices](../Sound-And-Music/voices.md)) |
| `11`<sub>h</sub> | Music | Original, Reorchestrated, and OST when offered | `+0E`<sub>h</sub> (`002DE110`); OST falls back to 1 when bit 0 of `0017E490` is clear | the soundtrack switch, `002DF530(v, 1)` |
| `12`<sub>h</sub> | Volume | - | - | a heading over the three volume rows |
| `13`<sub>h</sub>, `14`<sub>h</sub>, `15`<sub>h</sub> | Music, Sound Effects, Voice, indented | 0-100 | `+08`<sub>h</sub>, `+0A`<sub>h</sub>, `+0C`<sub>h</sub> | the volume of category 1, 2 or 3 ([Sound effects](../Sound-And-Music/sound-effects.md)) |
| `17`<sub>h</sub> | Restore Defaults | - | the whole record | below |
| `24`<sub>h</sub>, `25`<sub>h</sub> | Max. LP, Max. Gil | Acquire | - | below; mode 0 only |

Every row reaches `00240750(command, index)` and the setter switch `002407F0` (`00240818`-`00240959`). The options record
is `*0215E6E0`, inside the save image. The labels are `menu_command.bin` and the help lines `help_menu.bin`.

### Restore Defaults, Max. LP and Max. Gil

- Restore Defaults asks "Restore all settings to their default values?" (`0023E560`) and Yes rebuilds the options
  record with `002DDE60`: soundtrack 1, the three volumes 100, camera axes and multiplier cleared, and the language bit
  from the game's language.
- Max. LP and Max. Gil ask "If you change the Max. LP setting, you won't be able to change it back. Are you sure?"
  (`0023DFC0`). Yes sets 99,999 LP in each party record (`00305A00`) or 99,999,999 gil (`003058B0`, `00254EE0`).
- On the Parameter Settings screen `00240AD0` each of the two rows is painted by `00240A60`: its label from the
  `{label, help}` pairs at `00914C60` (Max. LP `53B`<sub>h</sub>, Max. Gil `53C`<sub>h</sub>) and the option Acquire (`53D`<sub>h</sub>).
- Rows 4, 5, 6, 8, 9 and 10 can be locked by bits `1E`<sub>h</sub>-`23`<sub>h</sub> of `[020927C0] + 32C4h` (`002405F0`): a locked row
  is greyed and plays sound 5 (`002400AC`).

### Graphics Settings rows

The rows are the table at `00914710`, 24 records `{ordinal, kind, class, label, help}`; rows 0, 2, 3, 11, 14 and 17 are
headings. A press runs `0017DB90(row, value, direction)`, which calls the settings dispatcher `001D1660` through
`001CD040` and reads the value back with `0017E070`.

| Row | Label | Values | Setting | Runs at once |
|---:|---|---|---|---|
| `1` | Graphical Quality | Low, Medium, High, Custom | Quality | the preset, `001D5120` |
| `4` | Display Adapter | the adapter | DeviceID, LUIDLow, LUIDHigh | waits for a dialog |
| `5` | Resolution | width x height | Resolution or WindowSize | applied at once only in Windowed mode (`001DC730`) |
| `6` | Screen Mode | Windowed, Full-Screen, Borderless | ScreenMode | waits for a dialog |
| `7` | Brightness | `0`-`100` | Brightness | - |
| `8` | Vsync | Off, On, Adaptive | VSync | the swap chain (`00796E20` vtable `+90`<sub>h</sub>) |
| `9` | Display Buffer | Double, Triple Buffer | BackBufferCount | the same call |
| `10` | Frame Rate Limit | 30 FPS, 60 FPS | FrameLimit | waits for a dialog |
| `12` | Anisotropic Filtering | 1x-16x | Anisotropic | the samplers (`0018AC50`, `001BD940`) |
| `13` | Water Shader | Low, High | WaterQuality | `001A5B00` |
| `15` | Shadows | Low, Medium, High | Shadow | the shadow map size (`001EF520`) |
| `16` | Character Self-Shadowing | Off, On | CharacterSelfShadow | - |
| `18` | Anti-Aliasing | Off, MSAA 2x-16x | MSAA | `00189520` |
| `19` | Post-Process Anti-Aliasing | FXAA, SMAA 1x | PostAA | `00193D50` byte `+4A3`<sub>h</sub> |
| `20` | Ambient Occlusion | Off, Half-Resolution, Full Resolution | HDAO | - |
| `21`-`23` | Depth of Field, Glare, Soft Particles | Off, On | DepthofField, Glare, SoftParticle | Soft Particles: `[manager + A80h]` vtable `+60`<sub>h</sub> |

The settings are `GameSetting.ini` keys at `[01F82D20]` ([Game settings](../Saving-Loading-And-Settings/game-settings.md)).

- The preset `001D5120` copies column `q` of `00900CE0` into every preset setting, unless `q` is Custom, and pushes
  anisotropic filtering, water, shadow size, MSAA, post-process anti-aliasing and soft particles again (`001DE4F0`).
- Changing any row from 12 to 23 sets Quality to Custom (`001D4B65`).
- Rows 4, 5, 6 and 10 keep a pending value. Leaving the row with a change opens a dialog: "Change the resolution of
  Full-Screen Mode?", "Change screen mode?", or for the adapter and the frame rate limit a restart notice. Yes on the
  restart notice writes `GameSetting.ini` and closes the game (`0017E050`, `PostMessageW(WM_CLOSE)`); No restores the
  old value.

The row widget `0023B6F0` keeps the shown value at `+C4`<sub>h</sub> and the applied one at `+C8`<sub>h</sub>. On the notice `2CA5`<sub>h</sub>
it applies the shown value and keeps it; on `2CA4`<sub>h</sub> it applies the kept value again (`0023B769`-`0023B7B2`). Both
go through `0017E540(row, value)`:

- Display Adapter: `001DC650` and `001DC7A0` on the display object `001DDAB0`.
- Resolution: `001DC920`, which stores the index at display `+38`<sub>h</sub> when `[01F82D20] + 8` is 0 and at `+24`<sub>h</sub>
  otherwise; the apply then runs `0017DB40`, which calls `001DC730`.
- Screen Mode: `001DC830`, after `0017E540` logs "Change Screen Mode By Config Menu!!!!" (`005CDAA0`).
- Every other row: `001DF340([01F82D20], index, value)` with the index below.

| Row | Index | Row | Index |
|---:|---:|---:|---:|
| `1` | `3` | `15` | `7` |
| `7` | `4` | `16` | `15` |
| `8` | `5` | `18` | `8` |
| `9` | `17` | `19` | `9` |
| `10` | `18` | `20` | `10` |
| `12` | `6` | `21` | `12` |
| `13` | `16` | `22` | `13` |
|  |  | `23` | `14` |

The read-back `0017E070` takes Resolution's index through `001DD050`: display `+38`<sub>h</sub> when display `+18`<sub>h</sub> is 0,
`+24`<sub>h</sub> otherwise. `0017FF20` returns the resolution as `width << 16 | height` from that mode's list of `1C`<sub>h</sub>-byte
entries (`001DD0B0`), or `[01F82D20] + 4` when the index is past the list's end.

### Controls rows

The 41 rows are the table at `0208E6E0`, built by `002414B0`. Rows 2-32 rebind keys ([Control remapping](../Controls-And-Input/control-remapping.md)).
The row painter `0023CD20` puts the row's text `+8` in the row widget's first part for a row of type 0, with the
third part placed after the text's width (`0029FE20`) and the fourth hidden, and in its fourth part for types 1-4,
with the first and third hidden; it paints nothing for any other type. The other settings rows are:

| Row | Label | Options | Setting | Runs at once |
|---:|---|---|---|---|
| `34` | Mouse Sensitivity: Left/Right | 1-6 | MouseSensityY `+60`<sub>h</sub> (`0017E760`) | - |
| `35` | Mouse Sensitivity: Up/Down | 1-6 | MouseSensityX `+5C`<sub>h</sub> (`0017E780`) | - |
| `36` | Camera Auto-Rotation | On, Off | CameraRevise `+58`<sub>h</sub> (`0017E740`) | - |
| `38` | Confirm Button | Type A, Type B | DecideButton `+64`<sub>h</sub> (`0017E6E0`) | swaps the keyboard Circle and Cross (`00198960`) and the confirm and cancel masks (`0022A4F0`) |
| `40` | Default | - | - | "Revert all control settings to default?"; Yes resets the four settings (`0017E520`) and the key bindings (`001E0F70`) |

The key names cross over: the Left/Right row writes `MouseSensityY`, and the horizontal camera reader `0032D3D0` reads
that same `+60`<sub>h</sub>, so the row does what its label says. Type A makes Cross confirm.

### Press or repeat

| Row widget | Rows | Steps on |
|---|---|---|
| `0023EBE0` | the three volumes | every frame while a direction is held (`02F97368`, `0023EC24`) |
| `0023E770` | Config choice and On/Off rows, Camera Auto-Rotation, Confirm Button | each repeat (`02F9736C`), clamped; Confirm steps to the next option and wraps |
| `0023D6B0`, `0023DB40` | Battle Speed, mouse sensitivity | each repeat |
| `0023B330` | Brightness | each repeat |
| `0023B6F0` | the other Graphics rows | each new press (`02F9736A`) |

### The cursor skips rows

Config moves its list cursor with `0023F240` (`0023FE31`), and Graphics Settings and Controls with
`00240DE0(list, skip, hold)` (`0023C27F`, `0023D2B2`), each with the wheel added the way
[Controls](../Controls-And-Input/controls.md) describes:

1. The list steps once (`002D3BA0`).
2. When the new row may not take the cursor, it steps again, up to the row count times, through `0023F7D0` (Config)
   or `002413E0` (the other two), each a single step with the list's `+E4`<sub>h</sub> bit 2 set around it.
3. When the step answered 4 to 6, or the list's `+E4`<sub>h</sub> bit 13 is set, it first puts the cursor back (`002D47C0`) and
   tries steps with the list's bytes `+107`<sub>h</sub>, `+108`<sub>h</sub> and `+F6`<sub>h</sub> set to 1, then 2 (`0023F660`-`0023F710`).
4. When no row qualifies the cursor goes back where it was (`002D47C0`).

For Config, `0023F190(screen)` decides: the row under the cursor may take it unless its command is `12`<sub>h</sub>, or its
command names a row list in `01E0BF60` whose layout kind is `0B`<sub>h</sub> or `0C`<sub>h</sub>. The other two screens pass their own
test, kept at `+728`<sub>h</sub> on Graphics Settings and `+4B8`<sub>h</sub> on Controls; a non-zero answer skips the row. With `hold` set
and a direction pressed, `00240DE0` posts `8003`<sub>h</sub> to the list (`002D1AC0`) instead of moving; Graphics Settings sets
it while a row's `+C8`<sub>h</sub> differs from its `+C4`<sub>h</sub> (`0023C25F`-`0023C26B`).

### Where each setting is saved

| Settings | Kept in | Written |
|---|---|---|
| Config rows | the options record `*0215E6E0`, part of the save image | only when the game is saved; Config writes no file |
| Graphics rows | `[01F82D20]` and the display object `[01F82D18]` | `GameSetting.ini` (`0017E530`) when Graphics Settings closes (`0023C501`) and on Yes to a restart notice |
| Controls settings | `[01F82D20]` `+58`<sub>h</sub>-`+64`<sub>h</sub> | `GameSetting.ini` when Controls is left (`0023D268`, `0023D428`) |
| key bindings | the keymap profiles | `keymap.ini` when Controls is left with Cancel (`0023D263`, [keymap.ini](../Controls-And-Input/keymap-file.md)) |

## Modding notes

- Config's rows and their order are the row lists of `01E0BF60`; the mode lists at `01E0B670`, `01E0B7D0` and
  `01E0B720` pick which commands show, with which label and help line.
- A Config setting lives in the save, so loading another save brings its battle, camera and sound settings with it.
- The Graphics preset values are the columns of `00900CE0`.

## Related

- [Menus](menus.md) - how the main menu opens Config.
- [Game settings](../Saving-Loading-And-Settings/game-settings.md) - `GameSetting.ini` and its keys.
- [Control remapping](../Controls-And-Input/control-remapping.md) - the binding rows.
- [Sound effects](../Sound-And-Music/sound-effects.md) - the volume categories.
