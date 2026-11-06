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
| `0x18` | Start a new game | - | - | closes the title list and starts a new game; mode 1 only |
| `0x1A` | Begin New Game+ | - | - | `0x00238A20` (`0x0024018C`), then as `0x18` ([New Game+ and New Game-](../Rewards-EXP-Gil-And-Loot/strong-and-weak-mode.md)); mode 1 only |
| `0x19` | Begin New Game- | - | - | `0x00238A50` (`0x00240182`), then as `0x18`; mode 1 only |
| `0x20`, `0x21` | Graphics Settings, Controls | - | - | opens the screen |
| `0x04` | Battle Mode | Wait, Active | dword 0 bit `0x8` (`0x002DE060`) | - |
| `0x05` | Battle Speed | 6 steps | dword 0 bits `0xFF0` (`0x002DE0F0`) | - |
| `0x06` | Target Lines | On, Off | dword 1 bit `0x400000` (`0x002DE2D0`) | - |
| `0x08` | Cursor Position | Last Selection, Default | dword 0 bit `0x8000` (`0x002DE1E0`) and bit `0x10000` (`0x002DE1C0`) | clears the saved cursors (`0x002526D0`) |
| `0x09` | Vibration Function | On, Off | dword 0 bit `0x2000` (`0x002DE080`) | `0x0035FF30` |
| `0x0A` | Screen Shake | On, Off | dword 0 bit `0x4000` (`0x002DE200`) | `0x0037DDC0` |
| `0x0B` | Subtitles | On, Off | dword 0 bit `0x1000`, set for Off (`0x002DE230`) | - |
| `0x0C`, `0x0D` | Camera Y-Axis, Camera X-Axis | Normal, Inverted | dword 1 bits `0x100`, `0x200` (`0x002DE190`, `0x002DE160`) | `0x001E1020`, `0x001E0FF0` |
| `0x0E` | Speed Mode Multiplier | x2, x4 | dword 1 bits `0x7800000` (`0x002DE250`) | the game speed through `0x0023B2E0` |
| `0x10` | Language | Japanese, English | dword 1 bit `0x400` (`0x002DE2F0`) | - ([Voices](../Sound-And-Music/voices.md)) |
| `0x11` | Music | Original, Reorchestrated, and OST when offered | `+0x0E` (`0x002DE110`); OST falls back to 1 when bit `0x1` of `0x0017E490` is clear | the soundtrack switch, `0x002DF530(v, 1)` |
| `0x12` | Volume | - | - | a heading over the three volume rows |
| `0x13`, `0x14`, `0x15` | Music, Sound Effects, Voice, indented | 0-100 | `+0x08`, `+0x0A`, `+0x0C` | the volume of category 1, 2 or 3 ([Sound effects](../Sound-And-Music/sound-effects.md)) |
| `0x17` | Restore Defaults | - | the whole record | below |
| `0x24`, `0x25` | Max. LP, Max. Gil | Acquire | - | below; mode 0 only |

Every row but `0x18`, `0x19` and `0x1A` reaches `0x00240750(command, index)` and the setter switch `0x002407F0`
(`0x00240818`-`0x00240959`). `0x00240750` is called only by the row widgets `0x0023D6B0`, `0x0023DB40`, `0x0023E770` and
`0x0023EBE0`. The three title rows get no widget: their lists `0x01E0BF60[0x18]`-`[0x1A]` (`0x01E0A880`, `0x01E0A930`,
`0x01E0A9E0`) have layout kind 13, which the builder's switch skips (`0x0023EE6C`-`0x0023EE74`), and their confirm is
`0x00240173` (`0x00240065`-`0x00240080`).

The options record is `*0x0215E6E0`, inside the save image. The labels are
`menu_command.bin`, except the three title rows' labels, which are `menu_message.bin` 34, 191 and 190 (ids 2034,
2191 and 2190 through `0x002F9860`); the help lines are `help_menu.bin` (117, 396 and 397 for the title rows).

`0x0023EFC0(screen)`, run by `0x0023FBE0` (`0x0023FCB6`), sets up Config's list widget. The row count comes from list
`0x01E0BF60[origin]` (`+0xC2` 0-2, any other as 0), the row painter `0x0023F8B0` goes to list `+0x120` (`0x0023F06E`),
and the cursor starts on the row saved as cursor kind 6 (`0x002526F0`). When that row's command names a kind-`0x0B`
list, the cursor goes to the first row whose command does not, or to row 0.

The painter `0x0023F8B0(screen, row widget, -, row)` reads the layout kind of the list the row's command names:

- kind `0x0B`: the eight parts listed at `0x00914CA0` show, and of the seven at `0x00914CA8` only entry n, with n = 1-6
  for commands 7, `0x0F`, `0x16`, `0x1F`, `0x22` and `0x23` and 0 for any other; part 1 is then placed after that
  entry's text width (`0x0029FE20`);
- any other kind: the part at `0x00914C98` shows unless the kind is `0x0C`, and part 2 takes the label (`0x002F9860`)
  unless it is `0xFFFF`. Part 2 is recoloured by `0x00393240(part, 1)` while the row's lock flag is set, and with 0
  otherwise: flag `0x1E` for command 4, `0x1F` for 5, `0x23` for 6, `0x22` for 8, `0x20` for 9, `0x21` for 10
  (`0x00254DD0`; the flags of Restore Defaults, Max. LP and Max. Gil below).

### Restore Defaults, Max. LP and Max. Gil

- Restore Defaults asks "Restore all settings to their default values?" (`0x0023E560`) and Yes rebuilds the options
  record with `0x002DDE60`: soundtrack 1, the three volumes 100, camera axes and multiplier cleared, and the language bit
  from the game's language.
- Max. LP and Max. Gil ask "If you change the Max. LP setting, you won't be able to change it back. Are you sure?"
  (`0x0023DFC0`). Yes sets 99,999 LP in each party record (`0x00305A00`) or 99,999,999 gil (`0x003058B0`, `0x00254EE0`).
- On the Parameter Settings screen `0x00240AD0` each of the two rows is painted by `0x00240A60`: its label from the
  `{label, help}` pairs at `0x00914C60` (Max. LP `0x53B`, Max. Gil `0x53C`) and the option Acquire (`0x53D`).
- Rows 4, 5, 6, 8, 9 and 10 can be locked by flags `0x1E`, `0x1F`, `0x23`, `0x22`, `0x20` and `0x21` of the byte array at `[0x020927C0] + 0x32C4` (`0x002405F0`, read by `0x00254DD0`; flag n is bit `1 << (n & 7)` of byte `n >> 3`): a locked row
  is greyed and plays sound 5 (`0x002400AC`).
- Only row 4's flag `0x1E` has a setter:
  - `0x00253A80` zeroes the array, and a save load copies it back with the rest of the block
    ([Save data](../Saving-Loading-And-Settings/save-data-fields.md)).
  - Otherwise only `0x00254E00` writes it, clearing a flag at `0x00254E27` and setting it at `0x00254E3D`. Its one caller is
    `0x002E23E0`, which the `setpartymenustatus` handler `0x00342590` calls.
  - `0x002E13C0` maps kinds 0-7 to flags 0, 1, 9 and `0x12`-`0x16`, kind 9 to `0x1E` and any other kind to `0x1D`.
  - Rows 5, 6, 8, 9 and 10 are never locked.
- The only script that would lock row 4 is `パーティメニュー抑制.コンフィグ禁止` in `naf_a02` (`setpartymenustatus(9, 1)`, with `(8, 1)` for flag `0x1D`); its `コンフィグ開放` clears both (`(9, 0)`, `(8, 0)`). No other line of the 1,114 decoded `us` scripts names that actor (`evt_t0020`, the 1,115th, has no EBP2 header), so no script runs either function and row 4 stays unlocked.

### Graphics Settings rows

The rows are the table at `0x00914710`, 24 records `{ordinal, kind, class, label, help}`; rows 0, 2, 3, 11, 14 and 17
are headings. A press runs `0x0017DB90(row, value, direction)`, which calls the settings dispatcher `0x001D1660` through
`0x001CD040` and reads the value back with `0x0017E070`. Rows 5 and 6 do not reach the dispatcher. Resolution runs
`0x001DC940(display, direction == 0)` on the display object `0x001DDAB0()` and then `0x001DC730` when `[0x01F82D20] + 8` is 0
(`0x0017DC1E`, `0x0017DC3C`), and neither while `0x001DDAB0()` returns 0 (`0x0017DC08`).

Screen Mode steps the passed value through 0, 1, 2, up by one for direction 0 and down by one otherwise, wrapping at
both ends, and returns it without the read-back (`0x0017DC46`-`0x0017DC69`). A heading dispatches nothing and reads back
-1. While the console object `0x001D50D0()` is 0 no row dispatches or steps and every row reads back through `0x0017E070`
(`0x0017DBB9`).

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
   or `0x002413E0` (the other two), each a single step with the list's `+0xE4` bit `0x4` set around it.
3. When the step answered 4 to 6, or the list's `+0xE4` bit `0x2000` is set, it first puts the cursor back (`0x002D47C0`) and
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

Every Config and Graphics Settings input, with the values it takes, the other writers of the same setting and which one wins, when a change takes effect, every reader and when the input changes nothing, is in [config-screen-inputs.tsv](config-screen-inputs.tsv).

### Columns of config-screen-inputs.tsv

One row per row of the two screens, 39 rows: `input` is the Config row id (`0x04` to `0x25`) or `g` and the
Graphics Settings row number (`g1` to `g23`).

| Column | Holds |
|---|---|
| `domain` | the values the row offers and how they are stored: the option names (`Wait or Active`, `On or Off`, `6 steps` ...), the setter that stores them, and the bit or field of the options record or settings object that holds them |
| `precedence` | every writer of the same setting and which one lands last: the row itself, the defaults installer or the start-up defaults, a loaded save, `GameSetting.ini` at start-up, and for some rows a script verb, the speed keys or FF12CONFIG; for the three action rows that store no setting (`Max. LP`, `Max. Gil` and `Start a new game`), what the row writes instead |
| `consumers` | every reader of the stored value: the getter and the code that calls it, with addresses, and the Config painter that draws the row |
| `visible_effect` | what the player sees change, with the page that describes it |
| `inert_when` | when a change does nothing: a value equal to the one already set, a list mode that does not hold the row, No to a restart notice or dialog, a row locked by its flag in the byte array at `[0x020927C0] + 0x32C4`, or a condition of the effect itself (the speed mode off, a post-process switch clear, a display mode the adapter lacks, the mouse for an invert row) |

## Layouts

### Graphics Settings row slots

Each of the 24 slots at `+0x4D8` of the Graphics Settings screen (next) is `0x18` bytes.

`GraphicsRowSlot` (`0x18` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `i32` | row | the row number 0-23, stored by the construct message for a row that gets a widget (`0x0023C042`) |
| `+0x04` | `u8[4]` | pad04 | read and written by no function; nothing fixes its width |
| `+0x08` | `void*` | widget | the row's `0x1D8`-byte widget: procedure `0x0023B330` for kind 3 (Brightness) and `0x0023B6F0` for kinds 2 and 5, no widget for the others (`0x0023BFC0`-`0x0023C03F`); the input turn passes it on (`0x0023C2F5`), and for a kind-5 row, one that keeps a pending value, the input turn and the cancel compare its shown `+0xC4` with its applied `+0xC8` (`0x0023C257`, `0x0023C35E`) |
| `+0x10` | `void*` | dialog | the confirmation `0x0023DFC0` opens for the row on sub-command `0x8003`, with message `0x27`, `0x2B`, `0x2C` or `0x28` by the row's ordinal (`0x0023C3D8`-`0x0023C43E`); 0 again on sub-command `0x1C` (`0x0023C473`) |

### The Graphics Settings screen

Graphics Settings is the `0x730`-byte widget kept at `0x0208E6C0` with procedure `0x0023BD40` (The screens above).

`GraphicsSettingsScreen` (`0x730` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000` | `u8[192]` | header | the widget header, written by the constructor `0x002465F0` (Widgets, The header); procedure `0x0023BD40` |
| `+0x0C0` | `u8` | mode | the row-list mode: the construct message's argument a as 0, 1 or 2 (any other value gives 0), stored by `0x0023D610` (`0x0023D628`); read by no instruction of this screen |
| `+0x0C1` | `u8` | layoutKind | the layout kind of row list `0x01E0BF60`[mode], its first byte, or `0xFF` when there is no row list, stored by `0x0023D610` (`0x0023D652`), which loads the layout of that kind's `0x01E0B638` entry; read by no instruction of this screen |
| `+0x0C2` | `u8` | origin | the construct message's argument a unchanged, stored by `0x0023D610` (`0x0023D61A`); when the screen is destroyed (message 18) it reopens Config with it (`0x0023C51E`, `0x00244F50` at `0x0023C53E`), so Config returns where it was opened from |
| `+0x0C3` | `u8` | pad0C3 | read and written by no function; nothing fixes its width |
| `+0x0C4` | `u8[4]` | pad0C4 | read and written by no function; nothing fixes its width |
| `+0x0C8` | `void*` | rowList | the row list `0x01E0BF60`[mode], or 0 for a mode of 45 or more, stored by `0x0023D610` (`0x0023D66A`); read by no instruction of this screen, which takes its rows from the table `0x00914710` |
| `+0x0D0` | `u32` | cleared0D0 | set to 0 by the construct message (`0x0023BE1B`); read by no instruction |
| `+0x0D4` | `u8[4]` | pad0D4 | read and written by no function; nothing fixes its width |
| `+0x0D8` | `void*` | list | the row list widget, item 0's `+0x18` in the screen's layout (`0x0023BE5F`); 0 just before (`0x0023BE35`). The construct message sets it up (`0x0023BE6B`-`0x0023BF00`: 24 rows, the row painter `0x0023BB20` at its `+0x120`, the screen at its `+0xD8`); the tick reads its cursor (`0x0023C294`-`0x0023C2E4`) and moves it through `0x00240DE0` (`0x0023C278`); the draw places the row widgets from its row height `+0x100` (`0x0023C1A8`-`0x0023C217`) |
| `+0x0E0` | `u8[8]` | cleared0E0 | the first bytes of `+0xE0`-`+0x4CF`, which the construct message clears (memset `0x3F0` at `0x0023BE44`); read and written by nothing else; nothing fixes its width |
| `+0x0E8` | `u8[228]` | cleared0E8 | part of the span the construct message clears (`0x0023BE44`); read and written by nothing else; nothing fixes its width |
| `+0x1CC` | `u8[4]` | cleared1CC | part of the span the construct message clears (`0x0023BE44`); read and written by nothing else; nothing fixes its width |
| `+0x1D0` | `u8[4]` | cleared1D0 | part of the span the construct message clears (`0x0023BE44`); read and written by nothing else; nothing fixes its width |
| `+0x1D4` | `u8[772]` | cleared1D4 | the rest of the cleared span to `+0x4CF` (`0x0023BE44`), and `+0x4D0`-`+0x4D7`, which nothing touches; read and written by nothing else; nothing fixes its width |
| `+0x4D8` | `u8[576]` | rows | 24 GraphicsRowSlot records (above), one `0x18`-byte slot per row of the table `0x00914710` (GraphicsRowSlot above); the construct message fills them (`0x0023BFB0`-`0x0023C053`), the draw places their widgets (`0x0023C1CF`-`0x0023C227`), message 13 with notice `0x2CA6` reaches one row widget and `0x2CA7` all 24 (`0x0023C496`-`0x0023C4FD`) |
| `+0x718` | `i32` | cursorRow | the row under the cursor: the construct message starts it at the first row whose kind (`0x00914714` + 20 x row) is not 0, a heading (`0x0023BF1C`-`0x0023BF78`); the input turn (message 10) stores the list's cursor row (`0x0023C2EE`) and copies the row's class byte to the list's `+0x106` (`0x0023C2E4`); the input turn, the cancel `0x8002` and the confirm `0x8003` and `0x1C` pick the row's slot by it (`0x0023C22E`, `0x0023C344`, `0x0023C3D8`, `0x0023C466`); `0x0023B6F0` reads it (`0x0023B91D`) |
| `+0x71C` | `u8[4]` | pad71C | read and written by no function; nothing fixes its width |
| `+0x720` | `u64` | greyedRows | one bit per row: a set bit makes the row painter `0x0023BB20` draw the label greyed (`0x002DD7E0`(2)) and keeps the input turn (message 10) from reaching the row's widget (`0x0023C302`-`0x0023C30D`). The construct message stores 0 (`0x0023C059`) and then, like the tick, only ANDs it with `0x10` or `0x20` or stores 0 again (`0x0023C083`, `0x0023C105`, `0x0023C11F`, `0x0023C15C`, `0x0023C165`), so it stays 0 and no row is drawn greyed |
| `+0x728` | `void*` | skipTest | the cursor-skip test `0x00241840`, stored by the construct message (`0x0023BF15`) and passed to `0x00240DE0` (`0x0023C26E`); it skips a heading row (The cursor skips rows above) |

### Controls row slots

Each of the 41 slots at `+0xD0` of the Controls screen (next) is `0x18` bytes.

`ControlsRowSlot` (`0x18` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `i32` | row | the row number 0-40, stored for a row that gets a widget (`0x0023D0CB`) |
| `+0x04` | `i32` | type | the row's type from the table `0x0208E6E0` (`+0x04` of its 20-byte entry, `0x0023D0CF`-`0x0023D0D1`): 2 is a key-binding row, which the draw and the input turn treat apart (`0x0023D1AA`, `0x0023D226`, `0x0023D2F0`) |
| `+0x08` | `void*` | widget | the row's widget: `0x100` bytes with procedure `0x0023C5C0` for types 1 and 2 with a non-zero option count, `0xD8` bytes with `0x0023DB40` for type 3, `0x0023E710`'s widget for type 4, and 0 for any other type (`0x0023D020`-`0x0023D0D5`); the input turn passes it on (`0x0023D376`-`0x0023D392`) |
| `+0x10` | `void*` | dialog | the revert dialog `0x0023DFC0`(`0x29`, 0, screen) on row 40's slot (`0x0023D3C0`-`0x0023D3CA`); sub-command `0x1C` sets the cursor row's to 0 (`0x0023D408`) |

### The Controls screen

Controls is the `0x4C0`-byte widget kept at `0x0208E6D0` with procedure `0x0023CE10` (The screens above).

`ControlsScreen` (`0x4C0` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000` | `u8[192]` | header | the widget header, written by the constructor `0x002465F0` (Widgets, The header); procedure `0x0023CE10` |
| `+0x0C0` | `u8` | origin | the construct message's argument a (`0x0023CECC`-`0x0023CED3`); when the screen is destroyed (message 18) it reopens Config with it (`0x0023D446`, `0x00244F50` at `0x0023D467`) |
| `+0x0C1` | `u8[7]` | pad0C1 | read and written by no function; nothing fixes its width |
| `+0x0C8` | `void*` | list | the row list widget, item 0's `+0x18` in the screen's layout (`0x0023CEEE`): the construct message sets it up for 41 rows with the row painter `0x0023CD20` and the screen at its `+0xD8` (`0x0023CEF5`-`0x0023CF82`) and starts its cursor on the first row of type 2 or more (`0x0023CFA0`-`0x0023CFD0`); the draw places the row widgets from its row height `+0x100` (`0x0023D119`-`0x0023D19D`); the input turn moves its cursor through `0x00240DE0` (`0x0023D2AB`) and reads it back (`0x0023D2B7`-`0x0023D2E8`) |
| `+0x0D0` | `u8[984]` | rows | 41 ControlsRowSlot records (above), one `0x18`-byte slot per row of the table `0x0208E6E0` (ControlsRowSlot above), filled by the construct message (`0x0023D007`-`0x0023D0F0`) |
| `+0x4A8` | `i32` | cursorRow | the row under the cursor: the input turn (message 10) stores the list's cursor row after each move (`0x0023D2EA`) and passes the turn to that row's widget (`0x0023D367`); the draw, the input turn and sub-commands `0x8001` and `0x1C` pick the row's slot by it (`0x0023D19F`, `0x0023D210`, `0x0023D3AF`, `0x0023D3FA`); the confirm `0x8001` on row 40, Default, opens the revert dialog (`0x0023D3AF`-`0x0023D3CA`) |
| `+0x4AC` | `u32` | bindingArmed | 1 when the draw finds the cursor on a key-binding row (type 2) and posts it sub-command `0x8001` with `+0x4B0` (`0x0023D1C3`), 0 otherwise (`0x0023D204`) and at construction (`0x0023D0FB`); read by no instruction |
| `+0x4B0` | `i32` | savedBinding | the key-binding value `+0xE8` of the binding row's widget, kept when the cursor leaves a type-2 row, which is then sent `0x8002` (`0x0023D317`-`0x0023D343`); passed with the `0x8001` the draw posts to the binding row under the cursor (`0x0023D1B4`); 0 at construction (`0x0023CF97`) |
| `+0x4B4` | `u8[4]` | pad4B4 | read and written by no function; nothing fixes its width |
| `+0x4B8` | `void*` | skipTest | the cursor-skip test `0x00241890`, stored by the construct message (`0x0023CF90`) and passed to `0x00240DE0` (`0x0023D2A1`); it skips a row whose type is not 2, 3 or 4 (The cursor skips rows above) |

### Config row slots

Each of the 42 slots at `+0xE0` of the Config screen (next) is `0x18` bytes.

`ConfigRowSlot` (`0x18` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` | command | the row's command, byte `+0x00` of the row (`0x0023EE47`); `0x0023EF80` matches it (`0x0023EF90`); `0xFF` for no command (`0x0023FE84`) |
| `+0x01` | `u8` | layoutKind | the layout kind of the row list the command names, or `0xFF` (`0x0023EE69`): kinds 1-10 get a row widget (`0x0023EE6C`-`0x0023EEDD`); the input turn passes the turn on only for kinds 1, 2, 3, 6 and 8 (mask `0x14E`, `0x0023FE9D`-`0x0023FED9`) |
| `+0x02` | `u8[6]` | pad02 | read and written by no function; nothing fixes its width |
| `+0x08` | `void*` | widget | the row's widget, `0x0023E770`, `0x0023D6B0` (`0xD8`), `0x0023EBE0` (`0xD8`) or `0x0023E400` (`0xF0`) by the kind (`0x0023EEE2`); the draw places it (`0x0023FDE7`); sub-command `0x12` drops it (`0x0023FF4D`) |
| `+0x10` | `void*` | dialog | the confirmation the row opens: `0x0023E560` (`0x2E0` bytes, Restore Defaults, `0x002400D7`-`0x00240102`) or `0x0023DFC0` (`0x0024015B`-`0x0024016D`); sub-command `0x1C` drops it (`0x0023FF1D`) |

### The Config screen

Config is the `0x4D8`-byte widget kept at `0x0208E6D8` with procedure `0x0023FBE0` (The screens above).

`ConfigScreen` (`0x4D8` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000` | `u8[192]` | header | the widget header, written by the constructor `0x002465F0` (Widgets, The header); procedure `0x0023FBE0` |
| `+0x0C0` | `u8` | mode | the row-list mode, the index into the 45 row lists of `0x01E0BF60`, stored by `0x0023D4F0` (`0x0023D504`) from the construct message's argument a; the row lookup `0x002405B0` takes it for the help line (`0x0023FF53`) and the confirm (`0x00240046`); `0x0023EFC0` (`0x0023F097`), the row builder `0x0023ED80` (`0x0023EDA3`, `0x0023EE10`), the cursor test `0x0023F190` (`0x0023F1C8`) and the construct message's cursor search (`0x0023FCD4`) read their list through it |
| `+0x0C1` | `u8` | layoutKind | the layout kind of the row list, its first byte, or `0xFF` when there is no row list, stored by `0x0023D4F0` (`0x0023D533`) |
| `+0x0C2` | `u8` | origin | where Config was opened from, the construct message's argument a: 0 the main menu, 1 the title's New Game list, 2 the main menu before story counter 26 (`0x0023D4FD`; the opener `0x002406D2`). Leaving Config, `0x0023ED10` returns to the Party Menu for origin 0 or 2 and clears the help line for 1 (`0x0023ED37`); `0x0023EFC0` picks the row list `0x01E0BF60`, `0x01E0BF68` or `0x01E0BF70` by it (`0x0023EFCF`); the cancel is handled apart for origin 1 (`0x0023FFAC`); it is passed on to Graphics Settings and Controls (`0x002401C5`, `0x002401F6`, `0x0024025D`, `0x00240276`) and to the row widgets and dialogs (`0x0023EECC`, `0x002400E4`, `0x00240161`); on destruction origin 1 runs `0x002E1CA0` with the leaving bit `+0xD0` (`0x00240226`) |
| `+0x0C3` | `u8[5]` | pad0C3 | read and written by no function; nothing fixes its width |
| `+0x0C8` | `void*` | rowList | the row list `0x01E0BF60`[mode], or 0 for a mode of 45 or more, stored by `0x0023D4F0` (`0x0023D549`); `0x0023EFC0` reads its byte `+0x01` for `0x002526F0` (`0x0023F087`) |
| `+0x0D0` | `u32` | leaving | bit `0x1` set when a confirmed row's action makes Config close, after commands `0x19` and `0x1A` run `0x00238A50` and `0x00238A20` (`0x00240191`); while it is set Config's input turn does nothing (`0x0023FE24`) and the row widgets `0x0023D6B0`, `0x0023D890` and `0x0023DD10` ignore their input (`0x0023D7A0`, `0x0023D8C6`, `0x0023DD46`); on destruction with origin 1 it is passed to `0x002E1CA0` (`0x0024022F`). 0 at construction (`0x0023FC58`) |
| `+0x0D4` | `u8[4]` | pad0D4 | read and written by no function; nothing fixes its width |
| `+0x0D8` | `void*` | list | the row list widget, item 0's `+0x18` in the screen's layout, set up and stored by `0x0023EFC0` (`0x0023F16F`); 0 just before (`0x0023FC84`). Config's cursor code reads it (`0x0023F190`, `0x0023F24E`, `0x0023F7EA`) and so do the input turn (`0x0023FE3E`), the draw (`0x0023FD99`-`0x0023FDEF`) and the row builder `0x0023ED80` (`0x0023EDCE`, `0x0023EEED`, `0x0023EF13`) |
| `+0x0E0` | `u8[1008]` | rows | 42 ConfigRowSlot records (above), one `0x18`-byte slot per row (ConfigRowSlot above): cleared by the construct message (memset `0x3F0` at `0x0023FC93`), filled by the row builder `0x0023ED80` (`0x0023EE07`-`0x0023EF27`); `0x0023EF80` finds a row's slot by its command (`0x0023EF90`) |
| `+0x4D0` | `u16` | nextScreen | the row command waiting when Config closes: `0x20` for Graphics Settings (`0x002401E0`), `0x21` for Controls (`0x002401AF`), 0 at construction (`0x0023FC5E`). `0x0023ED10` does not return to the Party Menu while it is `0x20` or `0x21` (`0x0023ED26`); on destruction Config opens the screen it names (`0x00240215`) |
| `+0x4D2` | `u8[6]` | pad4D2 | read and written by no function; nothing fixes its width |

## State

Each of the three screens is opened by a function that creates its widget through `0x00244F50` only while its global
is 0 and keeps the widget there; leaving clears it. All three are 0 in the file.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x0208E6C0` | `void*` | 0 | the open Graphics Settings screen: the `0x730`-byte widget with procedure `0x0023BD40` | `0x0023BCC0` (`0x0023BD0E`); `0x0023BD40`, 0 when it reopens Config (`0x0023C517`) | `0x0023BCC0`, which opens the screen only while it is 0 (`0x0023BCD7`); `0x0023BD40`, which closes it with `0x00244F00` (`0x0023C3B1`); the row widget `0x0023B6F0`, which forwards a command `0x1C` to the screen's procedure (`0x0023B7F2`), hands the screen to the row's arm on a new press (`0x0023B86A`) and compares its row with the screen's selected row `+0x718` (`0x0023B916`); the question box `0x0023E020` (`0x0023E222`) and `0x00240A00` (`0x00240A13`, reached from `0x0017DB80`), which send it notice `0x2CA6` (message 13) |
| `0x0208E6D0` | `void*` | 0 | the open Controls screen: the `0x4C0`-byte widget with procedure `0x0023CE10` | `0x0023CC90` (`0x0023CCDF`); `0x0023CE10`, 0 when it reopens Config (`0x0023D43F`) | `0x0023CC90`, which opens the screen only while it is 0 (`0x0023CCA8`); the binding row `0x0023C5C0`, which sends it messages 2 and 4 through `0x005841B0` (`0x0023C7A8`, `0x0023C8C3`); `0x0023CE10`, which closes it with `0x00244F00` when the player leaves with the cancel button (`0x0023D281`) |
| `0x0208E6D8` | `void*` | 0 | the open Config screen: the `0x4D8`-byte widget with procedure `0x0023FBE0`, which stores itself on message 1 | `0x0023FBE0`: itself (`0x0023FC51`); 0 when it goes, after opening Graphics Settings or Controls for a waiting row command `0x20` or `0x21` (`0x00240284`, `0x0024026B`), or after `0x002E1CA0(1, 0x15)` for origin 1 (`0x00240252`) | the openers `0x00240680` (`0x002406B8`) and `0x002406F0` (`0x00240703`) and the two screens that reopen Config, `0x0023BD40` (`0x0023C510`) and `0x0023CE10` (`0x0023D438`), which create it only while it is 0; the row widgets `0x0023D6B0` (`0x0023D794`), `0x0023D890` (`0x0023D8BA`) and `0x0023DD10` (`0x0023DD3A`), which step only while Config's `+0xD0` bit `0x1` is clear |

No other instruction reaches these three.

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

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Input gameplay: `0x002E1CA0` is called by `0x00313A00`; those functions are documented on
  [force fight mode](../Engine-Core/force-fight-mode.md).
- Script VM: `0x002E23E0` is called by `0x00342590`; `0x00342590` calls `0x00267E10`; those functions are documented on
  [force fight mode](../Engine-Core/force-fight-mode.md).
