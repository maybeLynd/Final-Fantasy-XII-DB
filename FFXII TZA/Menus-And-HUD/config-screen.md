---
title: "Config screen: the Config, Graphics Settings and Controls rows, what each change runs, and where each setting is saved"
kind: "system"
category: "Menus and HUD"
addresses: "0x0023FBE0, 0x002407F0, 0x0023BD40, 0x0017DB90, 0x001D1660, 0x0023CE10, 0x0215E6E0, 0x01F82D20"
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
| Config (menu text `0x4BE`) | `0x0023FBE0` | the main menu's Config entry, `0x00240680`; the title's New Game list, `0x002406F0` |
| Graphics Settings (`0x503`) | `0x0023BD40` | Config's row command `0x20` (`0x002401FD`), `0x0023BCC0` |
| Controls (`0x504`) | `0x0023CE10` | Config's row command `0x21` (`0x002401CC`), `0x0023CC90` |

The main menu's list builder `0x00281AE0` always adds Config (`0x00281C86`) and never adds the other three, so the player
reaches Graphics Settings and Controls only through Config. Leaving either reopens Config on its row (`0x0023C537`,
`0x0023D430`-`0x0023D467`).

Config's rows come from the row-list table at `0x01E0BF60`, 45 pointers indexed by the screen's mode byte `+0xC0`
(`0x0023FBE0`, `0x0023D4F0`). Each row list is a 4-byte header followed by
6-byte rows (below); a row with label `0xFFFF` is a separator.

`0x002405B0(mode, row)` returns a row of list `mode`,
or 0 for a mode of 45 or more, an empty entry or a row past the header's count `+2`; Config reads the row's help id
`+4` through it and shows it on the help line (`0x0023FF5D`-`0x0023FF8A`). The opener
(`0x002406D2`) picks mode 0 (`0x01E0B670`, 27 rows) when the story counter (`0x00265270`) is 26 or more, otherwise mode 2
(`0x01E0B7D0`, the same rows without the last three). Mode 1 (`0x01E0B720`) is the title's New Game list.

`0x0023D610(screen, mode, origin)`, called from `0x0023BD40` (`0x0023BE66`), stores the mode byte `+0xC0`, the origin
`+0xC2`, the row list `0x01E0BF60[mode]` at `+0xC8` and its layout kind at `+0xC1`; it loads the layout named by
byte `+1` of the kind's `0x01E0B638` entry (`0x00394700`) and sets the draw priority from its word `+2`.

Leaving Config runs `0x0023ED10`: it closes the screen and, unless the row command waiting at `+0x4D0` is `0x20` or
`0x21`, returns to the Party Menu on Config (`0x002814E0(0x4BE)`) for origin 0 or 2, or clears the help line
(`0x00291D80(0, 0)`) for origin 1. `0x0023EF80(screen, command)` finds a row's `0x18`-byte slot among the 42 at
`+0xE0` by its first byte; Config uses it to drop the slot's `+0x08` or `+0x10` when a row posts `0x12` or `0x1C`
with its command (`0x0023FF11`-`0x0023FF4D`).

The row list header:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` | layoutKind | indexes `0x01E0B638` |
| `+0x01` | `u8` | b1 | - |
| `+0x02` | `u16` | rowCount | rows that follow |

A row:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` | command | the command |
| `+0x01` | `u8` | flag | - |
| `+0x02` | `u16` | label | label text, `0xFFFF` for a separator |
| `+0x04` | `u16` | help | help text |

### Config rows

| Command | Label | Options | Stored in the options record | Runs at once |
|---:|---|---|---|---|
| `0x20`, `0x21` | Graphics Settings, Controls | - | - | opens the screen |
| `0x04` | Battle Mode | Wait, Active | dword 0 bit 3 (`0x002DE060`) | - |
| `0x05` | Battle Speed | 6 steps | dword 0 bits 4-11 (`0x002DE0F0`) | - |
| `0x06` | Target Lines | On, Off | dword 1 bit 22 (`0x002DE2D0`) | - |
| `0x08` | Cursor Position | Last Selection, Default | dword 0 bit 15 (`0x002DE1E0`) | clears the saved cursors (`0x002526D0`) |
| `0x09` | Vibration Function | On, Off | dword 0 bit 13 (`0x002DE080`) | `0x0035FF30` |
| `0x0A` | Screen Shake | On, Off | dword 0 bit 14 (`0x002DE200`) | `0x0037DDC0` |
| `0x0B` | Subtitles | On, Off | dword 0 bit 12, set for Off (`0x002DE230`) | - |
| `0x0C`, `0x0D` | Camera Y-Axis, Camera X-Axis | Normal, Inverted | dword 1 bits 8, 9 (`0x002DE190`, `0x002DE160`) | `0x001E1020`, `0x001E0FF0` |
| `0x0E` | Speed Mode Multiplier | x2, x4 | dword 1 bits 23-26 (`0x002DE250`) | the game speed through `0x0023B2E0` |
| `0x10` | Language | Japanese, English | dword 1 bit 10 (`0x002DE2F0`) | - ([Voices](../Sound-And-Music/voices.md)) |
| `0x11` | Music | Original, Reorchestrated, and OST when offered | `+0x0E` (`0x002DE110`); OST falls back to 1 when bit 0 of `0x0017E490` is clear | the soundtrack switch, `0x002DF530(v, 1)` |
| `0x12` | Volume | - | - | a heading over the three volume rows |
| `0x13`, `0x14`, `0x15` | Music, Sound Effects, Voice, indented | 0-100 | `+0x08`, `+0x0A`, `+0x0C` | the volume of category 1, 2 or 3 ([Sound effects](../Sound-And-Music/sound-effects.md)) |
| `0x17` | Restore Defaults | - | the whole record | below |
| `0x24`, `0x25` | Max. LP, Max. Gil | Acquire | - | below; mode 0 only |

Every row reaches `0x00240750(command, index)` and the setter switch `0x002407F0` (`0x00240818`-`0x00240959`). The options record
is `*0x0215E6E0`, inside the save image. The labels are `menu_command.bin` and the help lines `help_menu.bin`.

`0x0023EFC0(screen)`, run by `0x0023FBE0` (`0x0023FCB6`), sets up Config's list widget. The row count comes from list
`0x01E0BF60[origin]` (`+0xC2` 0-2, any other as 0), the row painter `0x0023F8B0` goes to list `+0x120` (`0x0023F06E`),
and the cursor starts on the row saved as cursor kind 6 (`0x002526F0`). When that row's command names a kind-`0x0B`
list, the cursor goes to the first row whose command does not, or to row 0.

The painter `0x0023F8B0(screen, row widget, -, row)` reads the layout kind of the list the row's command names:

- kind `0x0B`: the eight parts listed at `0x00914CA0` show, and of the seven at `0x00914CA8` only entry n, with n = 1-6
  for commands 7, `0x0F`, `0x16`, `0x1F`, `0x22` and `0x23` and 0 for any other; part 1 is then placed after that
  entry's text width (`0x0029FE20`);
- any other kind: the part at `0x00914C98` shows unless the kind is `0x0C`, and part 2 takes the label (`0x002F9860`)
  unless it is `0xFFFF`. Part 2 is recoloured by `0x00393240(part, 1)` while the row's lock bit is set, and with 0
  otherwise: bit `0x1E` for command 4, `0x1F` for 5, `0x23` for 6, `0x22` for 8, `0x20` for 9, `0x21` for 10
  (`0x00254DD0`).

### Restore Defaults, Max. LP and Max. Gil

- Restore Defaults asks "Restore all settings to their default values?" (`0x0023E560`) and Yes rebuilds the options
  record with `0x002DDE60`: soundtrack 1, the three volumes 100, camera axes and multiplier cleared, and the language bit
  from the game's language.
- Max. LP and Max. Gil ask "If you change the Max. LP setting, you won't be able to change it back. Are you sure?"
  (`0x0023DFC0`). Yes sets 99,999 LP in each party record (`0x00305A00`) or 99,999,999 gil (`0x003058B0`, `0x00254EE0`).
- On the Parameter Settings screen `0x00240AD0` each of the two rows is painted by `0x00240A60`: its label from the
  `{label, help}` pairs at `0x00914C60` (Max. LP `0x53B`, Max. Gil `0x53C`) and the option Acquire (`0x53D`).
- Rows 4, 5, 6, 8, 9 and 10 can be locked by bits `0x1E`-`0x23` of `[0x020927C0] + 0x32C4` (`0x002405F0`): a locked row
  is greyed and plays sound 5 (`0x002400AC`).

### Graphics Settings rows

The rows are the table at `0x00914710`, 24 records `{ordinal, kind, class, label, help}`; rows 0, 2, 3, 11, 14 and 17 are
headings. A press runs `0x0017DB90(row, value, direction)`, which calls the settings dispatcher `0x001D1660` through
`0x001CD040` and reads the value back with `0x0017E070`.

| Row | Label | Values | Setting | Runs at once |
|---:|---|---|---|---|
| `1` | Graphical Quality | Low, Medium, High, Custom | Quality | the preset, `0x001D5120` |
| `4` | Display Adapter | the adapter | DeviceID, LUIDLow, LUIDHigh | waits for a dialog |
| `5` | Resolution | width x height | Resolution or WindowSize | applied at once only in Windowed mode (`0x001DC730`) |
| `6` | Screen Mode | Windowed, Full-Screen, Borderless | ScreenMode | waits for a dialog |
| `7` | Brightness | `0`-`100` | Brightness | - |
| `8` | Vsync | Off, On, Adaptive | VSync | the swap chain (`0x00796E20` vtable `+0x90`) |
| `9` | Display Buffer | Double, Triple Buffer | BackBufferCount | the same call |
| `10` | Frame Rate Limit | 30 FPS, 60 FPS | FrameLimit | waits for a dialog |
| `12` | Anisotropic Filtering | 1x-16x | Anisotropic | the samplers (`0x0018AC50`, `0x001BD940`) |
| `13` | Water Shader | Low, High | WaterQuality | `0x001A5B00` |
| `15` | Shadows | Low, Medium, High | Shadow | the shadow map size (`0x001EF520`) |
| `16` | Character Self-Shadowing | Off, On | CharacterSelfShadow | - |
| `18` | Anti-Aliasing | Off, MSAA 2x-16x | MSAA | `0x00189520` |
| `19` | Post-Process Anti-Aliasing | FXAA, SMAA 1x | PostAA | `0x00193D50` byte `+0x4A3` |
| `20` | Ambient Occlusion | Off, Half-Resolution, Full Resolution | HDAO | - |
| `21`-`23` | Depth of Field, Glare, Soft Particles | Off, On | DepthofField, Glare, SoftParticle | Soft Particles: `[manager + 0xA80]` vtable `+0x60` |

The row painter `0x0023BB20`, which `0x0023BD40` installs (`0x0023BEDD`), hides parts 0-17 of the row widget and
shows the one whose number is the row's class. For a heading (kind 0) it places part 14 after the class part's text
width (`0x0029FE20`). For any other row it puts the label (`0x002F9860`) in the class part and colours it with
`0x002DD7E0(2)` when the row's bit in screen `+0x720` is set, `0x002DD7E0(0)` otherwise.

The settings are `GameSetting.ini` keys at `[0x01F82D20]` ([Game settings](../Saving-Loading-And-Settings/game-settings.md)).

The samplers take the anisotropy from `0x001DE540(settings)`: entry `+0x18 % 5` of `0x00900ED0`, the floats 1, 2, 4, 8
and 16 (`0x0018A840`, `0x0018AC50`, `0x001BC9D0`, `0x001BD940`).

- The preset `0x001D5120` copies column `q` of `0x00900CE0` into every preset setting, unless `q` is Custom, and pushes
  anisotropic filtering, water, shadow size, MSAA, post-process anti-aliasing and soft particles again (`0x001DE4F0`).
- Changing any row from 12 to 23 sets Quality to Custom (`0x001D4B65`).
- Rows 4, 5, 6 and 10 keep a pending value. Leaving the row with a change opens a dialog: "Change the resolution of
  Full-Screen Mode?", "Change screen mode?", or for the adapter and the frame rate limit a restart notice. Yes on the
  restart notice writes `GameSetting.ini` and closes the game (`0x0017E050`, `PostMessageW(WM_CLOSE)`); No restores the
  old value.

The row widget `0x0023B6F0` keeps the shown value at `+0xC4` and the applied one at `+0xC8`. On the notice `0x2CA5`
it applies the shown value and keeps it; on `0x2CA4` it applies the kept value again (`0x0023B769`-`0x0023B7B2`). Both
go through `0x0017E540(row, value)`:

- Display Adapter: `0x001DC650` and `0x001DC7A0` on the display object `0x001DDAB0`.
- Resolution: `0x001DC920`, which stores the index at display `+0x38` when `[0x01F82D20] + 8` is 0 and at `+0x24`
  otherwise; the apply then runs `0x0017DB40`, which calls `0x001DC730`.
- Screen Mode: `0x001DC830`, after `0x0017E540` logs "Change Screen Mode By Config Menu!!!!" (`0x005CDAA0`).
- Every other row: `0x001DF340([0x01F82D20], index, value)` with the index below.

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

The read-back `0x0017E070` takes Resolution's index through `0x001DD050`: display `+0x38` when display `+0x18` is 0,
`+0x24` otherwise. `0x0017FF20` returns the resolution as `width << 16 | height` from that mode's list of `0x1C`-byte
entries (`0x001DD0B0`), or `[0x01F82D20] + 4` when the index is past the list's end.

### Controls rows

The 41 rows are the table at `0x0208E6E0`, built by `0x002414B0`. Rows 2-32 rebind keys ([Control remapping](../Controls-And-Input/control-remapping.md)).
The row painter `0x0023CD20` puts the row's text `+8` in the row widget's first part for a row of type 0, with the
third part placed after the text's width (`0x0029FE20`) and the fourth hidden, and in its fourth part for types 1-4,
with the first and third hidden; it paints nothing for any other type. The other settings rows are:

| Row | Label | Options | Setting | Runs at once |
|---:|---|---|---|---|
| `34` | Mouse Sensitivity: Left/Right | 1-6 | MouseSensityY `+0x60` (`0x0017E760`) | - |
| `35` | Mouse Sensitivity: Up/Down | 1-6 | MouseSensityX `+0x5C` (`0x0017E780`) | - |
| `36` | Camera Auto-Rotation | On, Off | CameraRevise `+0x58` (`0x0017E740`) | - |
| `38` | Confirm Button | Type A, Type B | DecideButton `+0x64` (`0x0017E6E0`) | swaps the keyboard Circle and Cross (`0x00198960`) and the confirm and cancel masks (`0x0022A4F0`) |
| `40` | Default | - | - | "Revert all control settings to default?"; Yes resets the four settings (`0x0017E520`) and the key bindings (`0x001E0F70`) |

The key names cross over: the Left/Right row writes `MouseSensityY`, and the horizontal camera reader `0x0032D3D0` reads
that same `+0x60`, so the row does what its label says. Type A makes Cross confirm.

### Press or repeat

| Row widget | Rows | Steps on |
|---|---|---|
| `0x0023EBE0` | the three volumes | every frame while a direction is held (`0x02F97368`, `0x0023EC24`) |
| `0x0023E770` | Config choice and On/Off rows, Camera Auto-Rotation, Confirm Button | each repeat (`0x02F9736C`), clamped; Confirm steps to the next option and wraps |
| `0x0023D6B0`, `0x0023DB40` | Battle Speed, mouse sensitivity | each repeat |
| `0x0023B330` | Brightness | each repeat |
| `0x0023B6F0` | the other Graphics rows | each new press (`0x02F9736A`) |

### The cursor skips rows

Config moves its list cursor with `0x0023F240` (`0x0023FE31`), and Graphics Settings and Controls with
`0x00240DE0(list, skip, hold)` (`0x0023C27F`, `0x0023D2B2`), each with the wheel added the way
[Controls](../Controls-And-Input/controls.md) describes:

1. The list steps once (`0x002D3BA0`).
2. When the new row may not take the cursor, it steps again, up to the row count times, through `0x0023F7D0` (Config)
   or `0x002413E0` (the other two), each a single step with the list's `+0xE4` bit 2 set around it.
3. When the step answered 4 to 6, or the list's `+0xE4` bit 13 is set, it first puts the cursor back (`0x002D47C0`) and
   tries steps with the list's bytes `+0x107`, `+0x108` and `+0xF6` set to 1, then 2 (`0x0023F660`-`0x0023F710`).
4. When no row qualifies the cursor goes back where it was (`0x002D47C0`).

For Config, `0x0023F190(screen)` decides: the row under the cursor may take it unless its command is `0x12`, or its
command names a row list in `0x01E0BF60` whose layout kind is `0x0B` or `0x0C`. The other two screens pass their own
test, kept at `+0x728` on Graphics Settings and `+0x4B8` on Controls; a non-zero answer skips the row.

Graphics Settings' test `0x00241840` skips a row whose kind (`0x00914714` + 20 x row) is 0, a heading; Controls' test
`0x00241890` skips a row whose type (`0x0208E6E4` + 20 x row) is not 2, 3 or 4. With `hold` set
and a direction pressed, `0x00240DE0` posts `0x8003` to the list (`0x002D1AC0`) instead of moving; Graphics Settings sets
it while a row's `+0xC8` differs from its `+0xC4` (`0x0023C25F`-`0x0023C26B`).

### Where each setting is saved

| Settings | Kept in | Written |
|---|---|---|
| Config rows | the options record `*0x0215E6E0`, part of the save image | only when the game is saved; Config writes no file |
| Graphics rows | `[0x01F82D20]` and the display object `[0x01F82D18]` | `GameSetting.ini` (`0x0017E530`) when Graphics Settings closes (`0x0023C501`) and on Yes to a restart notice |
| Controls settings | `[0x01F82D20]` `+0x58`-`+0x64` | `GameSetting.ini` when Controls is left (`0x0023D268`, `0x0023D428`) |
| key bindings | the keymap profiles | `keymap.ini` when Controls is left with Cancel (`0x0023D263`, [keymap.ini](../Controls-And-Input/keymap-file.md)) |

## State

Each of the three screens is opened by a function that creates its widget through `0x00244F50` only while its global
is 0 and keeps the widget there; leaving clears it. All three are 0 in the file.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x0208E6C0` | `void*` | 0 | the open Graphics Settings screen: the `0x730`-byte widget with procedure `0x0023BD40` | `0x0023BCC0` (`0x0023BD0E`); `0x0023BD40`, 0 when it reopens Config (`0x0023C517`) | `0x0023BCC0`, which opens the screen only while it is 0 (`0x0023BCD7`); `0x0023BD40`, which closes it with `0x00244F00` (`0x0023C3B1`); the row widget `0x0023B6F0`, which forwards a command `0x1C` to the screen's procedure (`0x0023B7F2`), hands the screen to the row's arm on a new press (`0x0023B86A`) and compares its row with the screen's selected row `+0x718` (`0x0023B916`); the question box `0x0023E020` (`0x0023E222`) and `0x00240A00` (`0x00240A13`, reached from `0x0017DB80`), which send it notice `0x2CA6` (message 13) |
| `0x0208E6D0` | `void*` | 0 | the open Controls screen: the `0x4C0`-byte widget with procedure `0x0023CE10` | `0x0023CC90` (`0x0023CCDF`); `0x0023CE10`, 0 when it reopens Config (`0x0023D43F`) | `0x0023CC90`, which opens the screen only while it is 0 (`0x0023CCA8`); the binding row `0x0023C5C0`, which sends it messages 2 and 4 through `0x005841B0` (`0x0023C7A8`, `0x0023C8C3`); `0x0023CE10`, which closes it with `0x00244F00` when the player leaves with the cancel button (`0x0023D281`) |
| `0x0208E6D8` | `void*` | 0 | the open Config screen: the `0x4D8`-byte widget with procedure `0x0023FBE0`, which stores itself on message 1 | `0x0023FBE0`: itself (`0x0023FC51`); 0 when it goes, after opening Graphics Settings or Controls for a waiting row command `0x20` or `0x21` (`0x00240284`, `0x0024026B`), or after `0x002E1CA0(1, 0x15)` for origin 1 (`0x00240252`) | the openers `0x00240680` (`0x002406B8`) and `0x002406F0` (`0x00240703`) and the two screens that reopen Config, `0x0023BD40` (`0x0023C510`) and `0x0023CE10` (`0x0023D438`), which create it only while it is 0; the row widgets `0x0023D6B0` (`0x0023D794`), `0x0023D890` (`0x0023D8BA`) and `0x0023DD10` (`0x0023DD3A`), which step only while Config's `+0xD0` bit 0 is clear |

No other instruction reaches these three: no other RIP-relative, image-base-relative or 32-bit offset reference names
them. The one 32-bit hit on `0x0208E6C0`'s offset is the displacement of the RIP-relative `lea` at `0x00359951`, which
names `0x022C8018`.
## Modding notes

- Config's rows and their order are the row lists of `0x01E0BF60`; the mode lists at `0x01E0B670`, `0x01E0B7D0` and
  `0x01E0B720` pick which commands show, with which label and help line.
- A Config setting lives in the save, so loading another save brings its battle, camera and sound settings with it.
- The Graphics preset values are the columns of `0x00900CE0`.

## Related

- [Menus](menus.md) - how the main menu opens Config.
- [Game settings](../Saving-Loading-And-Settings/game-settings.md) - `GameSetting.ini` and its keys.
- [Control remapping](../Controls-And-Input/control-remapping.md) - the binding rows.
- [Sound effects](../Sound-And-Music/sound-effects.md) - the volume categories.
