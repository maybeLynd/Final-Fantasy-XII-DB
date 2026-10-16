---
title: "Config screen: the Config, Graphics Settings and Controls rows, what each change runs, and where each setting is saved"
kind: "system"
category: "Menus and HUD"
summary: "The three settings screens: how Config opens and leads to Graphics Settings and Controls, every row with its shipped label and the setting it edits, what a change runs at once (vibration, screen shake, camera axes, speed multiplier, soundtrack, volume categories, graphics presets, display buffer, the confirm-button swap), the rows whose change waits for a confirm dialog or a restart, Restore Defaults and the Max. LP and Max. Gil rows, which rows step per press and which repeat, and where each setting is stored and when it is written."
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
| Config (menu text `0x4BE`) | `0023FBE0` | the main menu's Config entry, `00240680`; the title's New Game list, `002406F0` |
| Graphics Settings (`0x503`) | `0023BD40` | Config's row command `0x20` (`002401FD`), `0023BCC0` |
| Controls (`0x504`) | `0023CE10` | Config's row command `0x21` (`002401CC`), `0023CC90` |

The main menu's list builder `00281AE0` always adds Config (`00281C86`) and never adds the other three, so the player
reaches Graphics Settings and Controls only through Config. Leaving either reopens Config on its row (`0023C537`,
`0023D430`-`0023D467`).

Config's rows come from the row-list table at `01E0BF60`, 45 pointers indexed by the screen's mode byte `+0xC0`
(`0023FBE0`, `0023D4F0`). Each row list is a header `{u8 layout kind (01E0B638), u8, u16 row count}` followed by
6-byte rows `{u8 command, u8 flag, u16 label, u16 help}`; a row with label `0xFFFF` is a separator. The opener
(`002406D2`) picks mode 0 (`01E0B670`, 27 rows) when the story counter (`00265270`) is 26 or more, otherwise mode 2
(`01E0B7D0`, the same rows without the last three). Mode 1 (`01E0B720`) is the title's New Game list.

### Config rows

| Command | Label | Options | Stored in the options record | Runs at once |
|---:|---|---|---|---|
| `0x20`, `0x21` | Graphics Settings, Controls | - | - | opens the screen |
| 4 | Battle Mode | Wait, Active | dword 0 bit 3 (`002DE060`) | - |
| 5 | Battle Speed | 6 steps | dword 0 bits 4-11 (`002DE0F0`) | - |
| 6 | Target Lines | On, Off | dword 1 bit 22 (`002DE2D0`) | - |
| 8 | Cursor Position | Last Selection, Default | dword 0 bit 15 (`002DE1E0`) | clears the saved cursors (`002526D0`) |
| 9 | Vibration Function | On, Off | dword 0 bit 13 (`002DE080`) | `0035FF30` |
| 10 | Screen Shake | On, Off | dword 0 bit 14 (`002DE200`) | `0037DDC0` |
| 11 | Subtitles | On, Off | dword 0 bit 12, set for Off (`002DE230`) | - |
| 12, 13 | Camera Y-Axis, Camera X-Axis | Normal, Inverted | dword 1 bits 8, 9 (`002DE190`, `002DE160`) | `001E1020`, `001E0FF0` |
| 14 | Speed Mode Multiplier | x2, x4 | dword 1 bits 23-26 (`002DE250`) | the game speed through `0023B2E0` |
| 16 | Language | Japanese, English | dword 1 bit 10 (`002DE2F0`) | - ([Voices](../Sound-And-Music/voices.md)) |
| 17 | Music | Original, Reorchestrated, and OST when offered | `+0x0E` (`002DE110`); OST falls back to 1 when bit 0 of `0017E490` is clear | the soundtrack switch, `002DF530(v, 1)` |
| `0x12` | Volume | - | - | a heading over the three volume rows |
| 19, 20, 21 | Music, Sound Effects, Voice, indented | 0-100 | `+0x08`, `+0x0A`, `+0x0C` | the volume of category 1, 2 or 3 ([Sound effects](../Sound-And-Music/sound-effects.md)) |
| `0x17` | Restore Defaults | - | the whole record | below |
| `0x24`, `0x25` | Max. LP, Max. Gil | Acquire | - | below; mode 0 only |

Every row reaches `00240750(command, index)` and the setter switch `002407F0` (`00240818`-`00240959`). The options record
is `*0215E6E0`, inside the save image. The labels are `menu_command.bin` and the help lines `help_menu.bin`.

### Restore Defaults, Max. LP and Max. Gil

- Restore Defaults asks "Restore all settings to their default values?" (`0023E560`) and Yes rebuilds the options
  record with `002DDE60`: soundtrack 1, the three volumes 100, camera axes and multiplier cleared, and the language bit
  from the game's language.
- Max. LP and Max. Gil ask "If you change the Max. LP setting, you won't be able to change it back. Are you sure?"
  (`0023DFC0`). Yes sets 99,999 LP in each party record (`00305A00`) or 99,999,999 gil (`003058B0`, `00254EE0`).
- Rows 4, 5, 6, 8, 9 and 10 can be locked by bits `0x1E`-`0x23` of `[020927C0] + 0x32C4` (`002405F0`): a locked row
  is greyed and plays sound 5 (`002400AC`).

### Graphics Settings rows

The rows are the table at `00914710`, 24 records `{ordinal, kind, class, label, help}`; rows 0, 2, 3, 11, 14 and 17 are
headings. A press runs `0017DB90(row, value, direction)`, which calls the settings dispatcher `001D1660` through
`001CD040` and reads the value back with `0017E070`.

| Row | Label | Values | Setting | Runs at once |
|---:|---|---|---|---|
| 1 | Graphical Quality | Low, Medium, High, Custom | Quality | the preset, `001D5120` |
| 4 | Display Adapter | the adapter | DeviceID, LUIDLow, LUIDHigh | waits for a dialog |
| 5 | Resolution | width x height | Resolution or WindowSize | applied at once only in Windowed mode (`001DC730`) |
| 6 | Screen Mode | Windowed, Full-Screen, Borderless | ScreenMode | waits for a dialog |
| 7 | Brightness | 0-100 | Brightness | - |
| 8 | Vsync | Off, On, Adaptive | VSync | the swap chain (`00796E20` vtable `+0x90`) |
| 9 | Display Buffer | Double, Triple Buffer | BackBufferCount | the same call |
| 10 | Frame Rate Limit | 30 FPS, 60 FPS | FrameLimit | waits for a dialog |
| 12 | Anisotropic Filtering | 1x-16x | Anisotropic | the samplers (`0018AC50`, `001BD940`) |
| 13 | Water Shader | Low, High | WaterQuality | `001A5B00` |
| 15 | Shadows | Low, Medium, High | Shadow | the shadow map size (`001EF520`) |
| 16 | Character Self-Shadowing | Off, On | CharacterSelfShadow | - |
| 18 | Anti-Aliasing | Off, MSAA 2x-16x | MSAA | `00189520` |
| 19 | Post-Process Anti-Aliasing | FXAA, SMAA 1x | PostAA | `00193D50` byte `+0x4A3` |
| 20 | Ambient Occlusion | Off, Half-Resolution, Full Resolution | HDAO | - |
| 21-23 | Depth of Field, Glare, Soft Particles | Off, On | DepthofField, Glare, SoftParticle | Soft Particles: `[manager + 0xA80]` vtable `+0x60` |

The settings are `GameSetting.ini` keys at `[01F82D20]` ([Game settings](../Saving-Loading-And-Settings/game-settings.md)).

- The preset `001D5120` copies column `q` of `00900CE0` into every preset setting, unless `q` is Custom, and pushes
  anisotropic filtering, water, shadow size, MSAA, post-process anti-aliasing and soft particles again (`001DE4F0`).
- Changing any row from 12 to 23 sets Quality to Custom (`001D4B65`).
- Rows 4, 5, 6 and 10 keep a pending value. Leaving the row with a change opens a dialog: "Change the resolution of
  Full-Screen Mode?", "Change screen mode?", or for the adapter and the frame rate limit a restart notice. Yes on the
  restart notice writes `GameSetting.ini` and closes the game (`0017E050`, `PostMessageW(WM_CLOSE)`); No restores the
  old value.

### Controls rows

The 41 rows are the table at `0208E6E0`, built by `002414B0`. Rows 2-32 rebind keys ([Control remapping](../Controls-And-Input/control-remapping.md));
the other settings rows are:

| Row | Label | Options | Setting | Runs at once |
|---:|---|---|---|---|
| 34 | Mouse Sensitivity: Left/Right | 1-6 | MouseSensityY `+0x60` (`0017E760`) | - |
| 35 | Mouse Sensitivity: Up/Down | 1-6 | MouseSensityX `+0x5C` (`0017E780`) | - |
| 36 | Camera Auto-Rotation | On, Off | CameraRevise `+0x58` (`0017E740`) | - |
| 38 | Confirm Button | Type A, Type B | DecideButton `+0x64` (`0017E6E0`) | swaps the keyboard Circle and Cross (`00198960`) and the confirm and cancel masks (`0022A4F0`) |
| 40 | Default | - | - | "Revert all control settings to default?"; Yes resets the four settings (`0017E520`) and the key bindings (`001E0F70`) |

The key names cross over: the Left/Right row writes `MouseSensityY`, and the horizontal camera reader `0032D3D0` reads
that same `+0x60`, so the row does what its label says. Type A makes Cross confirm.

### Press or repeat

| Row widget | Rows | Steps on |
|---|---|---|
| `0023EBE0` | the three volumes | every frame while a direction is held (`02F97368`, `0023EC24`) |
| `0023E770` | Config choice and On/Off rows, Camera Auto-Rotation, Confirm Button | each repeat (`02F9736C`), clamped; Confirm steps to the next option and wraps |
| `0023D6B0`, `0023DB40` | Battle Speed, mouse sensitivity | each repeat |
| `0023B330` | Brightness | each repeat |
| `0023B6F0` | the other Graphics rows | each new press (`02F9736A`) |

### Where each setting is saved

| Settings | Kept in | Written |
|---|---|---|
| Config rows | the options record `*0215E6E0`, part of the save image | only when the game is saved; Config writes no file |
| Graphics rows | `[01F82D20]` and the display object `[01F82D18]` | `GameSetting.ini` (`0017E530`) when Graphics Settings closes (`0023C501`) and on Yes to a restart notice |
| Controls settings | `[01F82D20]` `+0x58`-`+0x64` | `GameSetting.ini` when Controls is left (`0023D268`, `0023D428`) |
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
