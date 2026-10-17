---
title: "Game settings: the GameSetting.ini object and its options, the ini file's load and save, the quality presets, FrameLimit, DecideButton, the Config screen's commands, Active and Wait battle mode and the FF12CONFIG file"
kind: "system"
category: "Saving, loading and settings"
addresses: "001DE050, 001DED50, 001DE5D0, 001DF350, 001DEE90, 001DFD40, 001DE4F0, 0022BDF0, 001EDDC0, 0017E6E0, 0022A4F0, 002407F0, 002403F0, 002DDE60, 002DE060, 00255290, 00408C30, 001DF2C0, 00628690"
---

## What the player sees

Two sets of options exist.

- The launcher-level options (language, resolution, screen mode, graphics quality, VSync, frame
  limit, confirm button, mouse sensitivity, camera auto-rotation) live in GameSetting.ini in the
  game's folder under Documents and are written back whenever they change.
- Picking Low, Medium or High sets ten graphics options at once; Custom leaves them as they are.
  The 60 fps frame limit does not speed the game up: every authored duration is doubled so that it
  lasts the same time.
- The in-game Config screen edits options that travel with the save: battle mode (Active or Wait),
  battle speed, subtitles, vibration, screen shake, cursor position, camera axes, target lines,
  the speed-mode multiplier, the voice language, the music version and the three volumes. In Wait
  mode the battle menu stops the field; in Active mode it does not.

## How it works

### The settings object

`007980A0`, the program's main routine, allocates `0x65C` bytes, builds the object with
`001DE050(object, path)` (`00798257`) and keeps it at `01F82D20` (`00798261`). The path is the
save directory (see the [saving and loading page](saving-and-loading.md)) joined with
`GameSetting.ini` (`01CB35F8`, `00798218`) and stored at `+0x450` as a wide string.

`001DE050` fills the object in three steps:

1. column 0 of the defaults table `00900CE0` (31 rows of 16 bytes) into the 31 dwords at `+0x00`;
2. Resolution and WindowSize from the desktop size (`GetSystemMetrics(0) << 16 |
   GetSystemMetrics(1)`);
3. Language from the Windows LANGID (see the [languages page](languages.md)).

`001DED50` then opens the file: when it is missing, the value tables are initialised (`001DF240`)
and the file is written from the defaults (`001DFD40`); otherwise the text is parsed (`001DE5D0`).

### The 31 settings

The defaults table has four columns, one per quality level (Low, Medium, High, Custom); column 0 is
the start-up default. The reset flag at `00900CC0 + index` marks the ten settings the quality
presets control.

| # | Key (`01DFD050`) | Defaults Low, Medium, High, Custom | Preset | Value names (`01DFD150`) |
|---|---|---|---|---|
| 0 | Language | 1 | no | jp, en, fr, de, it, es, kr, ch, cn |
| 1 | Resolution | `0x07800438` (1920 x 1080) | no | `width*height` |
| 2 | ScreenMode | 1 | no | SM_WINDOW, SM_FULLSCREEN, SM_BORDERLESS |
| 3 | Quality | 1, 1, 2, 3 | no | VQ_LOW, VQ_MEDIUM, VQ_HIGH, VQ_CUSTOM |
| 4 | Brightness | 50 | no | number |
| 5 | VSync | 1 | no | Off, On, Adaptive |
| 6 | Anisotropic | 2, 2, 4, 0 | yes | 1, 2, 4, 8, 16 |
| 7 | Shadow | 0, 1, 2, 0 | yes | Low, Medium, High |
| 8 | MSAA | 1, 2, 3, 0 | yes | Off, MSAA2X, MSAA4X, MSAA8X, CSAA16x, CSAA16XQ, MSAA16x |
| 9 | PostAA | 1, 1, 1, 0 | yes | FXAA, SMAA_1x |
| 10 | HDAO | 1, 1, 2, 0 | yes | Off, HalfResolution, FullResolution |
| 11 | WindowSize | 0 | no | `width*height` |
| 12 | DepthofField | 1, 1, 1, 0 | yes | Off, On |
| 13 | Glare | 1, 1, 1, 0 | yes | Off, On |
| 14 | SoftParticle | 1, 1, 1, 0 | yes | Off, On |
| 15 | CharacterSelfShadow | 0, 1, 1, 0 | yes | Off, On |
| 16 | WaterQuality | 1, 1, 1, 0 | yes | Low, High |
| 17 | BackBufferCount | 0, 1, 1, 0 | no | DoubleBuffer, TripleBuffer |
| 18 | FrameLimit | 0 | no | 30, 60 |
| 19 | DeviceID | 0 | no | number |
| 20 | LUIDLow | 0 | no | number |
| 21 | LUIDHigh | 0 | no | number |
| 22 | CameraRevise | 1 | no | Off, On |
| 23 | MouseSensityX | 4 | no | number |
| 24 | MouseSensityY | 4 | no | number |
| 25 | DecideButton | 0 | no | Circle, Cross |
| 26 | Monitor | 1 | no | number |
| 27 | WindowPosX | 0 | no | number |
| 28 | WindowPosY | 0 | no | number |
| 29 | LastX | 0 | no | number |
| 30 | LastY | 0 | no | number |

A single default means the four columns are equal. The key table is null-terminated at index 31
(`01DFD148`); the value-name rows hold up to nine pointers and the strings sit at `008C5904`
onward. The old value-name rows for the numeric settings hold only the `none` pointer.

### Parsing the file

`001DE5D0(object, text)` reads the file line by line:

1. A line without `=` is logged as `[ConfigFile] invalid line`.
2. The key is matched case-insensitively against the 31 keys; a key outside the table is logged
   as `[ConfigFile] invalid key`.
3. `001DF350(object, index, value)` stores the value:
   - Resolution and WindowSize take `width*height` (split at the `*` that `00900B10` holds; a value without
     one is logged as `[ConfigFile] invalid Resolution`), each clamped to at least 640 x 360, packed as
     `width << 16 | height`;
   - a setting whose row holds exactly one name (the numeric settings' `none`) takes
     `atoi(value)`;
   - otherwise the value is matched case-insensitively against the row's names and its position
     is stored; a name that matches nothing (or a row with no names at all) is logged as
     `[ConfigFile] <key> value invalid`.
4. After the last line, every setting the file did not name, and every preset-controlled setting
   while Quality is not 3 (Custom), is reloaded from the defaults column selected by Quality.
5. When Language is neither `jp` (0) nor `kr` or `ch` (6, 7), three value-table pairs at
   `01DFDA58`, `01DFDBA8` and `01DFDCF8` are set to `{12, 13}`.

The parser reads the text through a string stream: `001DF7D0` copies the text into the stream's
buffer and sets its pointers, `001A9E10` builds the key and value strings, `001DFA00` returns a
string's characters (the heap copy once its capacity is above 15) and `001DF760` frees a buffer.

### Writing the file

`001DEE90` serialises all 31 settings as `Key=Value`: Resolution and WindowSize as
`width*height`, a setting with one value name as its number, and any other setting as the name of
its current value (`DecideButton=Circle`). It builds the text in a string stream, takes it out with
`001E00D0` (which calls `001E0100` on the stream's buffer at `+8`), and releases the buffer with
`001DF8C0`. `001DFD40` writes that text to the ini path with `_wfopen_s("wb")`.

### The three writers

| Writer | Site | What it writes |
|---|---|---|
| `001DE050` | `001DE099` | the defaults copy at start-up |
| `001DF350` | `001DF6AE` | the parsed file value |
| `001DF340(object, index, value)` | `001DF343` | the runtime setter the Config screen uses |

### The quality presets

`001DE4F0(object, quality)` returns at once when Quality already equals the argument; otherwise it
stores it at `+0x0C` and, for every setting whose reset flag is set, copies the defaults table's
column `quality` unless the quality is 3. Its one caller is `001D5120` (`001D5139`), the
graphics-settings apply, which then pushes five settings to their consumers in this order:

1. WaterQuality (`+0x40`) to `001A5B00(001A9930(), value)`.
2. Shadow (`+0x1C`) as the pair `00900F00[Shadow % 3]` (`001DE5A0`), the shadow map size for Low,
   Medium and High: 512, 1024 and 2048 on each axis, to `001EF520(001F0850(), high, low)`.
3. MSAA (`+0x20`) as a non-zero flag to byte `+0xDBA` of `00189120()`, and as the sample count
   `00900EE8[MSAA % 5]` = 1, 2, 4, 8 or 9 (`001DE570`) to `00189520`.
4. PostAA (`+0x24`) == 1 to byte `+0x4A3` of `00193D50()`.
5. SoftParticle (`+0x38`) == 1 to the virtual slot `+0x60` of the object at the caller's `+0xA80`.

| Setting | Low | Medium | High |
|---|---|---|---|
| Anisotropic | 2 (4x) | 2 (4x) | 4 (16x) |
| Shadow | Low | Medium | High |
| MSAA | MSAA2X | MSAA4X | MSAA8X |
| HDAO | HalfResolution | HalfResolution | FullResolution |
| CharacterSelfShadow | Off | On | On |
| PostAA, DepthofField, Glare, SoftParticle, WaterQuality | 1 | 1 | 1 |

### The supported MSAA modes

The dword `+0x44C` is a bit set of the MSAA values the display adapter supports. The constructor
sets it to 1 (bit 0, Off), and `0017D9C0(bit)` adds one more bit through `001DF2B0(object, bit)`.

The device setup `00628690` asks the device at its `+0x108` for the quality level count of format
`0x1C` (`R8G8B8A8_UNORM`) at sample counts 2 to 32 (virtual slot `+0xF0`, `CheckMultisampleQualityLevels`
in the `ID3D11Device` layout). For every count with a non-zero level count it sets:

| Sample count | Bit, MSAA value |
|---|---|
| 2 | 1, MSAA2X |
| 4 | 2, MSAA4X |
| 8 | 3, MSAA8X; also 4, CSAA16x, when the level count is above 16 |
| 16 | 5, CSAA16XQ |

`001DF2C0(object, value, forward)` steps from `value` to the next value (or, with `forward` 0, the
previous one) in 0-4 whose bit is set, wrapping around, and stores it as MSAA (`+0x20`) of the
object at `01F82D20`. Its one caller is the Graphics Settings dispatcher `001D1660` (`001D4A53`), which the
Config screen's Anti-Aliasing row reaches through `0017DB90` and `001CD040` ([Config screen](../Menus-And-HUD/config-screen.md));
it then sets byte `+0xDBA` of `00189120()` to whether the result is non-zero.

### FrameLimit

`0017D8F0` returns FrameLimit (`+0x48`). `0022BDF0`, the first call of the boot frame mode
`0022A0B0`, reads it, scans the command line for `-nologo` (which calls `00314DE0(1)`), and calls
`001EDDC0(FrameLimit == 1)`:

| FrameLimit | `01DFE0B4` | `01DFE0B8` | `01DFE0BC` | `01F82E38` |
|---|---|---|---|---|
| 0 (30) | left at the image value 1 | left at 1.0 | left at 1.0 | untouched |
| 1 (60) | 2 | 2.0 (`01CEBC08`) | 0.5 (`01CEBB70`) | 1 |

The 30 fps arm writes none of the triple; it begins a multimedia timer period instead
(`timeGetDevCaps`, then `timeBeginPeriod(wPeriodMin)`, keeping the period at `01F82E40` and
setting `01F82E3C` = 1). The 60 fps arm also calls `0033F020` and ends that period when one was
begun. Both arms then call `0032AE70`, `003333D0`, `00337A00` and `002BDA90`.

The triple is the game's time base: authored frame counts are multiplied by `01DFE0B8` (for
example the loot pickup lifetime, see the [loot pickups page](../Rewards-EXP-Gil-And-Loot/loot-pickups.md)),
and per-frame fades by `01DFE0BC`, so durations keep their wall-clock length at 60 fps.

### DecideButton

The Config screen's command `0x26` calls `0017E6E0(value)`: `001DF340(object, 25, value)`, then
`00198960(00198790(), value == 0)` for the input manager, then `0022A4F0`, which sets the confirm
mask `01E0C2A0` and the cancel mask `01E0C2A4` to `0x2000` and `0x4000` for value 0 and the
reverse otherwise, and `01FD4A64` to whether the value is non-zero. The same masks are set at boot
(see the [languages page](languages.md)).

The Controls screen's Default calls `0017E520`, which runs `001DEE70` on the object: CameraRevise
(`+0x58`) = 1, MouseSensityX (`+0x5C`) = 4, and one 8-byte store that sets MouseSensityY (`+0x60`) to
4 and DecideButton (`+0x64`) to 0. Its caller `0023E020` then applies the masks with `0022A4F0`.

### The Config screen's commands

Two dispatchers switch on command ids 4-38 through 35-slot tables: the setter `002407F0` (table
`00240968`; each arm loads the row's value, calls the setter and jumps to the empty stub
`0016D6A0`) and the getter `002403F0` (table `00240518`). Two wrappers normalise values around
them: `00240750` (set: normalise, then `002407F0`) and `00240330` (get: `002403F0`, then
normalise), switching on the id through their index tables at `002407C0` and `002403CC`:

| Selector | Ids | Normalisation |
|---|---|---|
| 0 | 4, 12, 13 | `v != 0` |
| 1 | 5, 29, 30 | `v + 1` on set, `v - 1` on get |
| 2 | 6, 8, 9, 10, 11, 16, 28 | `v == 0` |
| 4 | 38 | `v != 1` |
| 3, 5 | 17; every other id | unchanged |

The in-game options are an `0x28`-byte record inside the save image: `002DDE60` sets `0215E6E0`
to `002536A0() + 8`, writes the template `{0x00000035, 0x00620400}` and patches it (bit 17 of
dword 0 from `005C5230() == 2`; bit 12 of dword 0 set for locale ids 1 and 6; bit 10 of dword 1
set for locale ids 0, 7, 8, 10 and 11), clears the camera-axis bits and pushes them to `001E1020`
and `001E0FF0`, sets the music version to 1 (`002DF530(1, 1)`), clears the speed-mode field, sets
the three volumes to 100 (`001DBA60(1.0, channel)`), and runs the platform applier `002DDA30(1)`.

| Command | Option | Setter | Field | Getter |
|---|---|---|---|---|
| 4 | Battle Mode (Wait, Active) | `002DE060` | dword 0 bit 3 | `002DDC30` |
| 5 | Battle Speed | `002DE0F0` | dword 0 bits 4-11, signed | `002DDC90` |
| 6 | Target Lines | `002DE2D0` | dword 1 bit 22 | `002DDE00` |
| 8 | Cursor Position | `002DE1E0`, `002DE1C0` | dword 0 bits 15 and 16 | `002DDD50` |
| 9 | Vibration | `002DE080` | dword 0 bit 13, pushed to `0035FF30` | `002DDC40` |
| 10 | Screen Shake | `002DE200` | dword 0 bit 14, pushed to `0037DDC0` | `002DDD60` |
| 11 | Subtitles | `002DE230` | dword 0 bit 12 | `002DDD70` |
| 12 | Camera Y-Axis | `002DE190` | dword 1 bit 8, pushed to `001E1020` | `002DDD20` |
| 13 | Camera X-Axis | `002DE160` | dword 1 bit 9, pushed to `001E0FF0` | `002DDD00` |
| 14 | Speed Mode Multiplier | `002DE250`, `0023B2E0` | dword 1 bits 23-26 | `002DDDA0` |
| 16 | Voice language | `002DE2F0` | dword 1 bit 10 | `002DDE20` |
| 17 | Music version | `002DE110` | `+0x0E` u16, pushed to `002DF530` | `002DDCA0` |
| 19, 20, 21 | Music, Sound Effects, Voice volume | `002DE0B0`, `002DE290`, `002DE310` | `+0x08`, `+0x0A`, `+0x0C` u16, at most 100, pushed to `002DF2B0` on channels 1-3 | `002DDC70`, `002DDDE0`, `002DDE40` |
| 28 | Camera Auto-Rotation | `0017E740` | `001DF340(object, 22)` CameraRevise | `0017E260` |
| 29, 30 | Mouse Sensitivity | `0032E020`, `0032E030` | `001DF340(object, 24)`, `001DF340(object, 23)`, values 1-6 | `0017E420`, `0017E430` |
| 38 | Confirm Button | `0017E6E0` | `001DF340(object, 25)` DecideButton | `0017E210` |

Because the record lives in the save image, loading a save also loads these options.

### Active and Wait

`002DE060(value)` writes bit 3 of the options dword (`0215E6E0`) and `002DDC30` reads it (1 =
Active). `00255290(mode)` maps a UI mode to a halt class, -1 meaning no halt:

| UI mode | Halt class |
|---|---|
| 1 | -1 when the bit is set, 0 when clear |
| 4 | 0 when the bit is set, -1 when clear |
| 2, 6, `0xF`, `0x11`, `0x12`, `0x13`, `0x16` | `0xD` |
| 3, `0x18` | 2 |
| `0x14` | 0 |
| other | -1 |

`00254740(mode)` applies a class other than -1 through `00226BE0`, which sets that halt bit on every
actor, so in Wait mode entering UI mode 1 halts the field and in Active mode it does not. The bit's
readers are the Config getter, `00254740`, `00255290`, `00225CD0`, `00225EB0` and `00227680`.

### The FF12CONFIG file

`003692D0` resets the block at `02B62DA8` with `00408BA0` (`00369323`) and then runs `00408C30`
(`0036943F`), which reads `PS2Data/SQUARE_FF12/FF12CONFIG` from the archive (`001D6F20`, `0x800`
bytes) and copies its bytes into the globals listed in the layout below.

- The u16 at file `+0x0A` goes to `02B62DB4` unless the dword `01E02804` is not negative, in which
  case its low word is stored instead.
- `02B62DAB` is always set to 1, and `02B62DB4` is zeroed when the second command-line argument is
  `debug`. The arguments come from `0017D240(&vector, &count)`, which returns the pointer and count
  the application object keeps at `01F7F480` and `01F7F488` (its `+0x1130` and `+0x1138`, stored by
  `0017CEB0`).
- When the file loads, `02B62DAD` is first set to `01E02804 >= 0`.
- The `01E02810` branch (a `FFXII_%03d` or `PS2Data//oldsave//new%03d` probe that sets `02B62DAD`
  = 2) runs only when that dword is not negative.
- Both dwords are -1 in the image, so `02B62DAD` stays 0 and neither branch runs in the shipped
  game.

## Layouts

`GameSettingObject` (`0x65C` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000` | `u32[31] settings` | the 31 settings, offset = index * 4; 001DE050, 001DF350, 001DF340 |  |
| `+0x07C` | `u8[972] tables` | the value tables 001DF240 fills from 01DFD850, 01DFD9A0 and 01DFDAF0 (81 dwords each at +0x7C, +0x1C0 and +0x304) |  |
| `+0x448` | `u32` | count | 81 after `001DF240` |
| `+0x44C` | `u32` | msaa | bit set of the supported MSAA values: 1 from `001DE050`, more bits from `001DF2B0`; read by `001DF2C0` |
| `+0x450` | `u16[260] path` | the ini path, wcscpy_s by 001DE050 |  |
| `+0x658` | `u16` | fresh | `0x0101` from `001DE050`, 0 after a file load (`001DED50`) |
| `+0x65A` | `u8` | fresh2 | 1 from `001DE050`, 0 after a file load |
| `+0x65B` | `u8` | pad | not written by `001DE050`, `001DED50` or `001DF240` |

`Ff12Config` (`0x17` bytes, offsets from the start of the file):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` | unread00 | not copied by `00408C30` |
| `+0x01` | `u8` | unread01 | not copied |
| `+0x02` | `u8` | opt02 | to `02B62DA8` (reset value 3) |
| `+0x03` | `u8` | opt03 | to `02B62DA9` |
| `+0x04` | `u8` | opt04 | to `02B62DAA` |
| `+0x05` | `u8` | unread05 | not copied |
| `+0x06` | `u8` | opt06 | to `02B62DAC` |
| `+0x07` | `u8` | unread07 | not copied |
| `+0x08` | `u8` | opt08 | to `02B62DAE` |
| `+0x09` | `u8` | opt09 | to `02B62DAF` (reset value 1) |
| `+0x0A` | `u16` | fieldId | to `02B62DB4` unless `01E02804` is not negative |
| `+0x0C` | `u8` | opt0C | to `02B62DB0` |
| `+0x0D` | `u8` | opt0D | to `02B62DB1` |
| `+0x0E` | `u8` | opt0E | to `02B62DB2` |
| `+0x0F` | `u8` | opt0F | to `02B62DB3` |
| `+0x10` | `u8` | opt10 | to `02B62DB6` |
| `+0x11` | `u8` | opt11 | to `02B62DB7` |
| `+0x12` | `u8` | opt12 | to `02B62DB8` |
| `+0x13` | `u8[2] unread13` | not copied |  |
| `+0x15` | `u8` | opt15 | to `02B62DBB` (not reset by `00408BA0`) |
| `+0x16` | `u8` | opt16 | to `02B62DBC` |

## Operations

| Function | Role |
|---|---|
| `001DE050` | build the settings object: defaults, desktop size, Windows language, path |
| `001DED50` | load the ini, or create it from the defaults |
| `001DE5D0`, `001DF350` | parse the text, parse one value |
| `001DEE90`, `001DFD40` | serialise, write the file |
| `001DE4F0` | apply a quality preset |
| `00628690`, `001DF2B0`, `001DF2C0` | record the supported MSAA values, step MSAA through them |
| `001DEE70` | reset the four control settings |
| `0022BDF0`, `001EDDC0` | read FrameLimit at boot, set the time base |
| `0017E6E0`, `0022A4F0` | DecideButton setter, mask applier |
| `002407F0`, `002403F0` | the Config screen's set and get dispatchers |
| `002DDE60` | install the in-game options record defaults |
| `00408BA0`, `00408C30` | reset and load the FF12CONFIG block |

## State

| Address | Width | Meaning | Written by |
|---|---|---|---|
| `01F82D20` | `void*` | the settings object | `007980A0` |
| `0215E6E0` | `void*` | the in-game options record, `002536A0() + 8` inside the save image | `002DDE60` |
| `01DFE0B4` / `01DFE0B8` / `01DFE0BC` | `i32` / `f32` / `f32` | the time base | `001EDDC0` |
| `01F82E38` | `i32` | the 60 fps gate | `001EDDC0` |
| `01E0C2A0` / `01E0C2A4` | `u16` | confirm and cancel masks | `0022A4F0`, boot mode 0 |
| `02B62DA8`-`02B62DC1` | bytes | the FF12CONFIG block | `00408BA0`, `00408C30` |

## Modding notes

- Values in GameSetting.ini are matched by name, case-insensitively; a numeric value is accepted
  only for settings without value names. A key outside the table is ignored and logged.
- Quality Low, Medium and High overwrite the ten preset settings on every load; set Quality to
  Custom to keep edited values.
- FrameLimit is the only setting that rescales timed behaviour; everything that reads
  `01DFE0B8` follows it.
- The Config screen's options are stored in the save image, so editing a save edits them.

## Related

- [Languages: the Language setting, the nine language codes, the locale id each maps to, the data folder it selects, the Windows-locale default, and the confirm and cancel buttons](languages.md)
- [Saving and loading: the save slots and their files, the save screen's states, the six-step save transaction, the storage queue, the file layer's read and write rules, the area-change autosave and what a load runs](saving-and-loading.md)
- [Save file format: the SAFH container, its zlib and RC4 layers, the save image and its header fields, the four in-memory copies and the format stamps](save-file-format.md)
- [Loot pickups: the ten-slot pool, creation and eviction, the one-minute lifetime and blink, collection on contact, and the pickup object](../Rewards-EXP-Gil-And-Loot/loot-pickups.md)
